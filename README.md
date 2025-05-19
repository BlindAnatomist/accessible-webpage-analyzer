# Accessible Webpage Analyzer

An AI-powered desktop app that visually analyzes webpages — both live React apps and static HTML files — and generates richly detailed, accessible layout summaries. Designed for blind developers and screen reader users, it extracts computed styles, identifies layout patterns, and creates natural language reports describing how the page looks.

## ✨ What It Does

- Detects font names, font sizes, and styling
- Analyzes text, background, and border colors (in plain names, not hex)
- Identifies Flexbox and Grid layout usage
- Reports element positions (top, left, width, height)
- Groups elements by semantic section: `header`, `main`, `footer`, etc.
- Summarizes page structure as natural, spoken text
- Exports:
  - 📝 Plain text summary
  - 🧾 JSON layout model
  - 🌐 HTML report
  - 📄 Markdown report
- Speaks the summary aloud using macOS `say`

---

## 🖥️ Features

| Feature                          | Supported |
| -------------------------------- | --------- |
| Analyze live React URLs          | ✅        |
| Analyze local HTML files         | ✅        |
| Extract computed styles          | ✅        |
| Layout detection (Flex/Grid)     | ✅        |
| Semantic section grouping        | ✅        |
| JSON layout model export         | ✅        |
| HTML + Markdown reports          | ✅        |
| Spoken paragraph summary         | ✅        |
| Keyboard accessible UI (no drag) | ✅        |

---

## 📦 Requirements

- macOS with Python 3.8+
- Google Chrome browser (installed)
- ChromeDriver (auto-installed via `webdriver-manager`)
- Recommended: macOS `say` command for spoken output

---

## ⚙️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/Phlypper/accessible-webpage-analyzer.git
cd accessible-webpage-analyzer
2. Set up Python environment
python3 -m venv web
source web/bin/activate
pip install -r requirements.txt

🚀 Running the App
python app.py
Once launched:
Click “Analyze Live URL” to scan a running React app (like http://localhost:3000)
Click “Browse HTML File” to select and analyze a local HTML file
Click “Open Temp Folder” to see the output reports

📁 Output Files
After each analysis, these files are saved to your /tmp folder:
File
Format
Description
webpage_grouped_and_spoken.txt
Text
Plaintext summary
webpage_report.md
Markdown
Developer-friendly report
webpage_report.html
HTML
Visual report viewable in browser
webpage_report.json
JSON
Structured layout model for tools
Use the “Open Temp Folder” button to open these easily on macOS.

🔊 Accessibility Notes
This tool was designed from the ground up with blind developers in mind:
All analysis is screen reader–friendly
Natural language summaries are spoken aloud via VoiceOver + say
No mouse required — full keyboard navigation
No drag-and-drop — just accessible file selection dialogs

🔧 Customization Ideas
Want to extend it?
Add PDF or CSV export
Add screenshot previews to the HTML report
Integrate WCAG contrast checks
Batch analyze multiple URLs or folders

📄 License
none

🙌 Credits
Created with ❤️ by Jason Washburn, for a more inclusive developer experience.
Built using:
Python
PyQt6
Selenium
WebDriver Manager
WebColors

🔗 Links
GitHub: github.com/Phlypper/accessible-webpage-analyzer
---
```
