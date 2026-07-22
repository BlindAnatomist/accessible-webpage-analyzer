# Initial repository audit

Audit date: 2026-07-21

Repository assessed: `BlindAnatomist/accessible-webpage-analyzer`

Upstream: `Phlypper/accessible-webpage-analyzer`

Assessed branch: `work/accessibility-analyzer-audit`

## Purpose

This audit establishes what the existing prototype actually does, where its strongest idea lies, which defects should be repaired before expansion, and how a contribution can be offered upstream without taking control of Jason Washburn's project.

## Audit scope and limits

The complete tracked source was inspected:

- `app.py`
- `README.md`
- `requirements.txt`
- `.gitignore`

This is a static source audit. The application requires macOS, Chrome, ChromeDriver, PyQt6, and a graphical session. Those runtime conditions were not available in the audit environment. No claim of successful execution, VoiceOver compatibility, or rendered-browser behavior is made here.

## Architectural baseline

The application is a single-file PyQt6 desktop program.

The interface offers three controls:

1. analyze a live URL;
2. select a local HTML file;
3. open the temporary output folder.

Selenium opens the page in Chrome, waits for a `body` element, scrolls through the document, and inspects every DOM element. JavaScript retrieves selected computed-style values and a `getBoundingClientRect()` result. Elements are grouped under the nearest `header`, `main`, `footer`, `aside`, `nav`, or `section` ancestor. Reports are written to four fixed files under `/tmp`, and a summary is passed to the macOS `say` command.

## What is already valuable

The prototype contains a serious and useful premise:

> A blind developer needs more than conformance errors. The developer also needs a linguistic account of spatial organization, typography, grouping, emphasis, and layout relationships that sighted collaborators inspect visually.

The current code begins that translation by collecting:

- font families and sizes;
- text and background CSS values;
- CSS display modes;
- element rectangles;
- broad semantic-container groupings;
- machine-readable JSON alongside human-readable reports.

The JSON export is especially important because it could become the stable intermediate representation used by later semantic, visual, and language-generation layers.

## Findings by priority

### Priority 0: Preserve upstream control

The fork is correctly isolated. Its `main` branch matches the upstream initial commit, and this audit is on a separate branch. No upstream pull request should be opened until the fork owner authorizes it.

### Priority 1: Remove command execution through untrusted page content

`app.py` constructs a shell command with:

```python
os.system(f"say \"{full_spoken}\"")
```

`full_spoken` contains computed CSS strings obtained from the analyzed webpage. A webpage controls values such as custom font-family names. Passing those strings through a shell command permits shell interpretation and command substitution.

This is the most urgent defect because the application is specifically designed to inspect arbitrary webpages.

Required repair:

```python
subprocess.run(["say", full_spoken], check=False)
```

Speech should also be optional, bounded, and reported separately from analysis success.

### Priority 1: Escape untrusted values in the HTML report

The HTML report interpolates computed webpage strings directly into HTML list items and a summary paragraph. These strings must be escaped before insertion. A report should describe an analyzed page, not reproduce executable or misleading markup from it.

Required repair:

- use `html.escape` for every untrusted string;
- include a complete document structure and UTF-8 declaration;
- treat the report as data, not trusted markup.

### Priority 1: Guarantee browser cleanup and expose failures

Chrome is not managed with `try/finally`. Failures during driver creation, navigation, scrolling, extraction, report generation, or speech can leave a Chrome process running.

The extraction loop also catches every exception and silently continues. This can produce an apparently successful but materially incomplete report.

Required repair:

- create the driver inside a guarded lifecycle;
- call `quit()` in `finally`;
- record extraction failures and affected element counts;
- replace bare or broad silent exception handling with narrow handling and useful diagnostics.

### Priority 1: Correct element coordinates

The program scrolls to the bottom of the page before collecting rectangles. `getBoundingClientRect()` returns coordinates relative to the current viewport, not stable document coordinates. Many reported `top` values will therefore be negative or otherwise dependent on the final scroll position.

Required repair:

- add `window.scrollX` and `window.scrollY` to rectangle coordinates; or
- use a document-coordinate extraction method;
- record viewport dimensions and scroll position;
- distinguish viewport position from document position.

### Priority 1: Stop blocking the graphical interface

Navigation, scrolling, extraction, and report generation run synchronously on the PyQt main thread. Large pages can make the application appear frozen and prevent keyboard or screen-reader interaction during analysis.

Required repair:

- move analysis into a worker thread or Qt task abstraction;
- expose progress and cancellation;
- disable only controls that would conflict with the active task;
- return focus predictably when analysis completes or fails.

### Priority 2: Correct the product description

The README calls the application "AI-powered," but the source contains no AI model, inference service, model call, or language-generation component.

The README also presents the application as an accessibility analyzer, while the implementation currently reads selected CSS and DOM geometry. It does not inspect the accessibility tree or apply accessibility rules.

Required repair:

Describe the current version as a webpage visual-layout description prototype. Reserve "AI-powered" and broader accessibility claims for implemented and tested capabilities.

### Priority 2: Separate four analysis layers

The present report conflates visual description with accessibility analysis. Future architecture should distinguish:

1. Visual layer: typography, color, spacing, dimensions, alignment, layout, prominence.
2. Semantic layer: document language, title, headings, landmarks, lists, tables, forms, media, and structure.
3. Accessible-interface layer: roles, names, descriptions, states, focusability, keyboard order, live regions, and control relationships.
4. Manual acceptance layer: actual VoiceOver announcements, focus movement, touch ergonomics, and platform-specific behavior.

Automated output must never imply that layer 4 has been tested when it has not.

### Priority 2: Improve visibility and relevance filtering

The current visibility check excludes only `display: none` and `visibility: hidden`.

It does not account for:

- the HTML `hidden` attribute;
- `aria-hidden`;
- zero dimensions;
- clipping;
- opacity;
- elements positioned far outside the viewport;
- inert subtrees;
- duplicate or non-user-facing DOM nodes.

The application should report both rendered visibility and accessibility-tree exposure rather than treating either as a single Boolean.

### Priority 2: Capture content and accessible identity

The existing element model does not include visible text, role, accessible name, `aria-*` state, `alt`, label relationships, heading level, link destination, input type, tabindex, or focusability.

Without these, the report can describe how a control is styled but not what the control is or whether a screen-reader user can identify it.

### Priority 2: Add contrast calculation rather than color-name frequency alone

Exact CSS color values are counted, but no foreground/background compositing or WCAG contrast ratio is calculated. Color naming is not equivalent to accessibility analysis.

A future contrast layer must account for transparency, inherited backgrounds, gradients, images, and text size or weight. Results that cannot be calculated reliably should be marked indeterminate rather than guessed.

### Priority 2: Improve output identity and durability

Every run overwrites the same four files in `/tmp`. Reports do not identify the analyzed URL or file, analysis time, viewport, application version, or extraction warnings.

Required repair:

- create one timestamped result directory per run;
- include a source identifier and audit metadata;
- retain a stable JSON schema version;
- provide an explicit Save or Export destination;
- avoid implying that temporary files are durable project records.

### Priority 2: Make speech controlled and useful

The application automatically speaks the full summary after every run. Large pages may produce long, repetitive speech that cannot be previewed or selectively navigated.

The macOS `say` command is text-to-speech; it is not VoiceOver output and should not be described as such.

Required repair:

- make speech opt-in;
- offer concise and detailed summary levels;
- provide Stop Speech;
- preserve the textual report as the primary accessible artifact;
- test actual VoiceOver reading and focus behavior separately.

### Priority 3: Refactor the monolith into testable components

The current code combines interface creation, browser control, DOM extraction, aggregation, report rendering, file output, and speech in one class and one file.

Recommended modules:

- `models.py`: typed result and warning structures;
- `browser.py`: driver lifecycle and page loading;
- `extractor.py`: deterministic DOM and computed-style extraction;
- `analysis.py`: aggregation and rule evaluation;
- `reports.py`: plain text, Markdown, HTML, and JSON rendering;
- `speech.py`: optional platform speech adapter;
- `ui.py`: PyQt interface and worker coordination;
- `app.py`: minimal entry point.

Pure functions in `analysis.py` and `reports.py` should be testable without Chrome or a graphical session.

### Priority 3: Add automated quality gates

The repository currently has no automated tests or continuous integration.

The first implementation contribution should add tests for:

- RGB and RGBA parsing;
- HTML escaping;
- report generation from fixed fixtures;
- stable JSON schema output;
- coordinate normalization;
- extraction-warning accounting;
- safe speech invocation without a shell;
- URL and local-file normalization.

A lightweight GitHub Actions workflow can run formatting, linting, type checking, tests, and Python compilation without requiring a graphical browser session.

Browser integration tests should be a separate optional layer.

### Priority 3: Pin and document dependencies

`requirements.txt` contains four unbounded package names. Reproducibility will decline as Selenium, PyQt6, WebColors, and WebDriver Manager evolve.

The project should declare a supported Python range and use a controlled dependency strategy. Exact pinning, compatible-release constraints, or a lock file can be selected after the supported runtime is confirmed with Jason.

### Priority 3: Repair README structure and claims

The README's initial shell code fence is not closed at the correct point, causing installation instructions and much of the remaining document to be rendered as code. It also:

- conflates `say` with VoiceOver;
- claims AI functionality that is absent;
- claims accessibility behavior without recorded testing;
- omits troubleshooting and privacy boundaries;
- states that no license exists.

The lack of a license should be discussed with Jason before broader distribution or incorporation of the code into other products. This fork should not choose a license on his behalf.

## Recommended contribution sequence

### Contribution 1: Safety and testability foundation

Keep the user-visible feature set substantially unchanged while:

- eliminating shell execution and HTML injection;
- guaranteeing driver cleanup;
- correcting coordinate calculation;
- extracting pure report functions;
- adding tests and a basic quality workflow;
- repairing README accuracy.

This should be the first upstream pull request because it is bounded, defensible, and does not redefine Jason's product.

### Contribution 2: Semantic document report

Add deterministic checks and descriptions for:

- page title and language;
- heading hierarchy;
- landmarks;
- links and buttons;
- images and alternative text;
- forms and labels;
- lists, tables, and media.

The report should distinguish information, warnings, probable defects, and checks that require human judgment.

### Contribution 3: Accessible-interface model

Add roles, names, states, descriptions, focusability, tabindex, live regions, and control relationships. Where possible, compare DOM semantics with browser accessibility-tree information.

### Contribution 4: Visual relationship model

Improve spatial and visual language:

- stable document coordinates;
- grouping and alignment;
- dominant and exceptional typography;
- spacing and density;
- reading-order comparisons;
- responsive viewport comparisons;
- contrast analysis with explicit uncertainty.

### Contribution 5: Manual VoiceOver acceptance protocol

Create repeatable scenarios for macOS VoiceOver and, if the application later gains a web interface, iPhone Safari VoiceOver. Record exact behavior rather than claiming generic screen-reader accessibility.

## Acceptance gate before the first upstream pull request

The first proposed contribution should not be presented to Jason until all of the following are true:

- changes exist only on a dedicated feature branch;
- the original behavior and intended behavior are documented;
- automated tests pass;
- Python compilation passes;
- no shell is used with webpage-derived data;
- HTML output escapes webpage-derived data;
- Chrome cleanup is guaranteed;
- known untested runtime behavior is stated plainly;
- the pull request is narrow enough for Jason to understand and reject without affecting later work.

## Audit conclusion

This repository is not yet a full accessibility analyzer, but it contains the seed of a distinctive instrument: a system that explains visual webpage organization to a blind developer while also exposing semantic and interaction evidence.

The correct next move is not to bury the prototype under a large rewrite. It is to make its existing core safe, truthful, deterministic, and testable, then add the semantic and interaction layers one at a time.
