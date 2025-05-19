import sys
import os
import json
import webcolors
import time
import subprocess
from collections import defaultdict
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit,
    QInputDialog, QMessageBox, QFileDialog
)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def rgb_to_name(value):
    try:
        if "rgb" in value:
            rgb = tuple(map(int, value.replace("rgb(", "").replace(")", "").split(",")))
            return webcolors.rgb_to_name(rgb)
        return value
    except Exception:
        return value


class WebDescribeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accessible Webpage Analyzer")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.button_url = QPushButton("Analyze Live URL (React App)")
        self.button_url.clicked.connect(self.analyze_live_url)
        layout.addWidget(self.button_url)

        self.button_file = QPushButton("Browse HTML File")
        self.button_file.clicked.connect(self.analyze_local_html)
        layout.addWidget(self.button_file)

        self.button_open_tmp = QPushButton("Open Temp Folder")
        self.button_open_tmp.clicked.connect(self.open_temp_folder)
        layout.addWidget(self.button_open_tmp)

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.setLayout(layout)

    def open_temp_folder(self):
        subprocess.run(["open", "/tmp"])

    def analyze_live_url(self):
        url, ok = QInputDialog.getText(self, "Enter URL", "URL of the React App:")
        if ok and url:
            self.analyze_url(url)

    def analyze_local_html(self):
        html_path, _ = QFileDialog.getOpenFileName(
            self, "Select HTML File", "", "HTML Files (*.html *.htm)"
        )
        if html_path:
            local_url = f"file://{html_path}"
            self.analyze_url(local_url)

    def analyze_url(self, url):
        self.text_area.setText("Analyzing page...")
        app.processEvents()

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
        except:
            self.text_area.setText("Timeout: page did not finish rendering.")
            driver.quit()
            return

        total_height = driver.execute_script("return document.body.scrollHeight")
        for i in range(0, total_height, 500):
            driver.execute_script(f"window.scrollTo(0, {i})")
            time.sleep(1)

        elements = driver.find_elements(By.XPATH, "//*")
        styles_by_section = defaultdict(list)
        spoken_phrases = []

        for elem in elements:
            try:
                tag = elem.tag_name
                if tag in ["script", "style", "meta", "link"]:
                    continue

                visible = driver.execute_script(
                    "const s = window.getComputedStyle(arguments[0]); "
                    "return s.display !== 'none' && s.visibility !== 'hidden';", elem
                )
                if not visible:
                    continue

                section = driver.execute_script("""
                    let el = arguments[0];
                    while (el && el.tagName.toLowerCase() !== 'body') {
                        if (['header','main','footer','aside','nav','section'].includes(el.tagName.toLowerCase())) {
                            return el.tagName.toLowerCase();
                        }
                        el = el.parentElement;
                    }
                    return 'body';
                """, elem)

                computed = driver.execute_script("""
                    const s = window.getComputedStyle(arguments[0]);
                    const r = arguments[0].getBoundingClientRect();
                    return {
                        tag: arguments[0].tagName.toLowerCase(),
                        font: s.fontFamily,
                        size: s.fontSize,
                        color: s.color,
                        bgColor: s.backgroundColor,
                        border: s.border,
                        display: s.display,
                        position: s.position,
                        top: r.top,
                        left: r.left,
                        width: r.width,
                        height: r.height
                    };
                """, elem)

                computed["color"] = rgb_to_name(computed["color"])
                computed["bgColor"] = rgb_to_name(computed["bgColor"])
                computed["section"] = section
                styles_by_section[section].append(computed)

            except Exception:
                continue

        driver.quit()

        # === Summary Output ===
        text_report = []
        html_report = ["<html><body><h1>Webpage Layout Report</h1>"]
        md_report = ["# Webpage Layout Report"]
        spoken_summary = []
        json_data = {}

        for section, items in styles_by_section.items():
            text_report.append(f"\n--- {section.upper()} ({len(items)} elements) ---")
            html_report.append(f"<h2>{section.title()}</h2><ul>")
            md_report.append(f"## {section.title()}")
            fonts, sizes, colors, bgs, layouts = defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int), defaultdict(int)

            for style in items:
                fonts[style["font"]] += 1
                sizes[style["size"]] += 1
                colors[style["color"]] += 1
                bgs[style["bgColor"]] += 1
                layouts[style["display"]] += 1

            json_data[section] = {
                "fonts": dict(fonts),
                "sizes": dict(sizes),
                "text_colors": dict(colors),
                "background_colors": dict(bgs),
                "layouts": dict(layouts),
                "elements": items
            }

            for label, group in [("Fonts", fonts), ("Sizes", sizes), ("Text Colors", colors), ("Backgrounds", bgs), ("Layouts", layouts)]:
                line = f"{label}: " + ", ".join(f"{k} ({v})" for k, v in group.items())
                text_report.append(line)
                html_report.append(f"<li>{line}</li>")
                md_report.append(f"- {line}")

            top_font = max(fonts, key=fonts.get) if fonts else "default font"
            top_color = max(colors, key=colors.get) if colors else "default text"
            top_bg = max(bgs, key=bgs.get) if bgs else "no background"
            layout_mode = ", ".join(layouts.keys()) if layouts else "normal flow"
            spoken_phrase = f"The {section} uses {top_font}, with {top_color} on {top_bg}, laid out using {layout_mode}."
            spoken_summary.append(spoken_phrase)
            html_report.append("</ul>")

        full_spoken = " ".join(spoken_summary)
        text_report.append("\n=== Spoken Layout Summary ===")
        text_report.append(full_spoken)
        html_report.append(f"<p><b>Summary:</b> {full_spoken}</p></body></html>")
        md_report.append("## Spoken Summary")
        md_report.append(full_spoken)

        with open("/tmp/webpage_grouped_and_spoken.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(text_report))
        with open("/tmp/webpage_report.md", "w", encoding="utf-8") as f:
            f.write("\n".join(md_report))
        with open("/tmp/webpage_report.html", "w", encoding="utf-8") as f:
            f.write("\n".join(html_report))
        with open("/tmp/webpage_report.json", "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2)

        self.text_area.setText("\n".join(text_report))
        os.system(f"say \"{full_spoken}\"")
        QMessageBox.information(self, "Done", "Reports saved to /tmp/")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WebDescribeApp()
    window.show()
    sys.exit(app.exec())
