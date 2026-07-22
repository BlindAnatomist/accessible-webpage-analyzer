# Accessible Webpage Analyzer

Accessible Webpage Analyzer is a macOS desktop prototype that converts selected visual and layout properties of a rendered webpage into text, Markdown, HTML, JSON, and spoken summaries.

It is designed as an exploratory tool for blind developers and screen-reader users who need a linguistic account of how a webpage is visually organized.

This version is not yet a complete accessibility rules engine, does not inspect the browser accessibility tree, and does not use an AI model.

## Current capabilities

- Analyze a live webpage URL in Chrome.
- Analyze a local HTML file.
- Read selected computed CSS properties.
- Record document-relative element rectangles.
- Group visible elements under broad semantic containers such as `header`, `main`, `nav`, `article`, `section`, and `footer`.
- Summarize common fonts, sizes, colors, backgrounds, and CSS display values.
- Export one source-identified report run in four formats:
  - plain text;
  - Markdown;
  - escaped HTML;
  - structured JSON.
- Speak the summary through the macOS `say` command without passing webpage content through a shell.

## Important limitations

The current reports describe selected rendered CSS and geometry. They do not establish that a page is accessible.

This version does not yet test:

- heading order;
- accessible names or roles;
- landmarks beyond broad DOM grouping;
- form labels;
- keyboard order or focus behavior;
- live regions;
- WCAG contrast ratios;
- actual VoiceOver announcements;
- touch or mobile interaction.

Automated analysis cannot replace manual screen-reader testing.

## Requirements

- macOS;
- Python 3;
- Google Chrome;
- the packages listed in `requirements.txt`.

ChromeDriver is obtained through `webdriver-manager` when the application starts an analysis.

## Installation

```bash
git clone https://github.com/Phlypper/accessible-webpage-analyzer.git
cd accessible-webpage-analyzer
python3 -m venv web
source web/bin/activate
pip install -r requirements.txt
```

## Run the application

```bash
python app.py
```

The interface provides these controls:

- `Analyze Live URL`: enter a webpage address.
- `Browse HTML File`: choose a local `.html` or `.htm` file.
- `Open Reports Folder`: open the most recent report directory, or the main reports directory before the first run.

## Report location

Each run creates a separate timestamped directory under:

```text
/tmp/accessible-webpage-analyzer/
```

Each run contains:

```text
webpage_report.txt
webpage_report.md
webpage_report.html
webpage_report.json
```

The temporary directory is not a durable archive. Copy reports elsewhere when they need to become project evidence.

## Development checks

The pure report, coordinate, output, and speech utilities can be tested without Chrome, PyQt6, or macOS:

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py accessible_analyzer tests
```

A GitHub Actions workflow runs the same checks for repository changes.

## Project direction

The intended architecture separates four layers:

1. visual and layout description;
2. semantic document analysis;
3. accessible-name, state, and interaction analysis;
4. manual VoiceOver acceptance evidence.

The initial fork audit and contribution plan are recorded in `docs/`.

## Authorship and contribution status

Created by Jason Washburn.

The `BlindAnatomist` fork contains independently reviewable audit and repair branches. No fork change is part of the upstream project unless Jason reviews and merges a pull request.

## License

The upstream repository does not currently declare a license. A license should not be selected for Jason without his decision.
