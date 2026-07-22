import re
import subprocess
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import webcolors
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QInputDialog,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from accessible_analyzer.coordinates import normalize_rect
from accessible_analyzer.output import create_run_directory, default_output_root, write_reports
from accessible_analyzer.reporting import build_report_data, render_text
from accessible_analyzer.speech import speak

_RGB_PATTERN = re.compile(
    r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*([0-9.]+))?\s*\)",
    re.IGNORECASE,
)


def rgb_to_name(value):
    """Return an exact CSS color name when one exists, otherwise preserve RGB."""

    if not isinstance(value, str):
        return str(value)

    match = _RGB_PATTERN.fullmatch(value.strip())
    if not match:
        return value

    red, green, blue = (int(match.group(index)) for index in range(1, 4))
    alpha = match.group(4)
    if alpha is not None and float(alpha) == 0:
        return "transparent"

    try:
        return webcolors.rgb_to_name((red, green, blue))
    except ValueError:
        return f"rgb({red}, {green}, {blue})"


class WebDescribeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accessible Webpage Analyzer")
        self.setGeometry(100, 100, 800, 600)
        self.last_output_directory = None

        layout = QVBoxLayout()

        self.button_url = QPushButton("Analyze Live URL")
        self.button_url.setAccessibleDescription(
            "Open a dialog to enter the address of a webpage to analyze."
        )
        self.button_url.clicked.connect(self.analyze_live_url)
        layout.addWidget(self.button_url)

        self.button_file = QPushButton("Browse HTML File")
        self.button_file.setAccessibleDescription(
            "Choose a local HTML file to analyze."
        )
        self.button_file.clicked.connect(self.analyze_local_html)
        layout.addWidget(self.button_file)

        self.button_open_tmp = QPushButton("Open Reports Folder")
        self.button_open_tmp.setAccessibleDescription(
            "Open the latest report folder, or the main reports folder if no analysis has run."
        )
        self.button_open_tmp.clicked.connect(self.open_reports_folder)
        layout.addWidget(self.button_open_tmp)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.text_area.setAccessibleName("Analysis report")
        self.text_area.setAccessibleDescription(
            "Contains analysis progress, warnings, and the generated text report."
        )
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def open_reports_folder(self):
        target = self.last_output_directory or default_output_root()
        target.mkdir(parents=True, exist_ok=True)
        subprocess.run(["open", str(target)], check=False)

    def analyze_live_url(self):
        url, ok = QInputDialog.getText(self, "Enter URL", "Webpage URL:")
        if ok and url.strip():
            self.analyze_url(url.strip())

    def analyze_local_html(self):
        html_path, _ = QFileDialog.getOpenFileName(
            self, "Select HTML File", "", "HTML Files (*.html *.htm)"
        )
        if html_path:
            self.analyze_url(Path(html_path).resolve().as_uri())

    def analyze_url(self, url):
        self.text_area.setText(
            "Analyzing page. The application may be less responsive until this run finishes."
        )
        QApplication.processEvents()

        driver = None
        warnings = []
        extraction_failures = 0

        try:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            driver.get(url)

            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            total_height = int(
                driver.execute_script(
                    "return Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);"
                )
                or 0
            )
            for offset in range(0, total_height, 500):
                driver.execute_script("window.scrollTo(0, arguments[0]);", offset)
                time.sleep(0.2)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.2)

            viewport = driver.execute_script(
                "return {width: window.innerWidth, height: window.innerHeight, "
                "devicePixelRatio: window.devicePixelRatio};"
            )
            elements = driver.find_elements(By.XPATH, "//*")
            styles_by_section = defaultdict(list)

            for element in elements:
                try:
                    tag = element.tag_name
                    if tag in {"script", "style", "meta", "link", "noscript"}:
                        continue

                    visible = driver.execute_script(
                        """
                        const element = arguments[0];
                        const style = window.getComputedStyle(element);
                        const rect = element.getBoundingClientRect();
                        return !element.hidden &&
                               style.display !== 'none' &&
                               style.visibility !== 'hidden' &&
                               style.opacity !== '0' &&
                               rect.width > 0 &&
                               rect.height > 0;
                        """,
                        element,
                    )
                    if not visible:
                        continue

                    section = driver.execute_script(
                        """
                        let current = arguments[0];
                        const regionTags = ['header', 'main', 'footer', 'aside', 'nav', 'article', 'section'];
                        while (current && current.tagName && current.tagName.toLowerCase() !== 'body') {
                            const tagName = current.tagName.toLowerCase();
                            if (regionTags.includes(tagName)) {
                                return tagName;
                            }
                            current = current.parentElement;
                        }
                        return 'body';
                        """,
                        element,
                    )

                    computed = driver.execute_script(
                        """
                        const element = arguments[0];
                        const style = window.getComputedStyle(element);
                        const rect = element.getBoundingClientRect();
                        return {
                            tag: element.tagName.toLowerCase(),
                            font: style.fontFamily,
                            size: style.fontSize,
                            color: style.color,
                            bgColor: style.backgroundColor,
                            border: style.border,
                            display: style.display,
                            position: style.position,
                            rect: {
                                top: rect.top,
                                left: rect.left,
                                width: rect.width,
                                height: rect.height
                            },
                            scrollX: window.scrollX,
                            scrollY: window.scrollY
                        };
                        """,
                        element,
                    )

                    coordinates = normalize_rect(
                        computed.pop("rect"),
                        scroll_x=computed.pop("scrollX", 0),
                        scroll_y=computed.pop("scrollY", 0),
                    )
                    computed.update(coordinates)
                    computed["color"] = rgb_to_name(computed["color"])
                    computed["bgColor"] = rgb_to_name(computed["bgColor"])
                    computed["section"] = section
                    styles_by_section[section].append(computed)
                except Exception:
                    extraction_failures += 1

            if extraction_failures:
                warnings.append(
                    f"{extraction_failures} DOM elements could not be extracted and were omitted."
                )

            metadata = {
                "source": url,
                "analyzed_at": datetime.now(timezone.utc).isoformat(),
                "viewport": viewport,
                "dom_element_count": len(elements),
                "reported_element_count": sum(
                    len(items) for items in styles_by_section.values()
                ),
                "extraction_failure_count": extraction_failures,
            }
            report = build_report_data(
                styles_by_section,
                metadata=metadata,
                warnings=warnings,
            )

            output_directory = create_run_directory()
            write_reports(report, output_directory)
            self.last_output_directory = output_directory
            self.text_area.setText(render_text(report))

            try:
                speech_return_code = speak(report["spoken_summary"])
                if speech_return_code != 0:
                    self.text_area.append(
                        "\nSpeech output did not complete successfully. "
                        "The written reports are unaffected."
                    )
            except FileNotFoundError:
                self.text_area.append(
                    "\nThe macOS say command was not available. "
                    "The written reports are unaffected."
                )

            QMessageBox.information(
                self,
                "Analysis complete",
                f"Reports saved to {output_directory}",
            )
        except TimeoutException:
            self.text_area.setText(
                "Analysis stopped: the page body did not become available within 20 seconds."
            )
        except Exception as error:
            self.text_area.setText(
                f"Analysis failed: {type(error).__name__}: {error}"
            )
        finally:
            if driver is not None:
                try:
                    driver.quit()
                except Exception:
                    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebDescribeApp()
    window.show()
    sys.exit(app.exec())
