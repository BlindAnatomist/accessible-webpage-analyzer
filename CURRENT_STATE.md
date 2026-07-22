# Current state

Last updated: 2026-07-21

Active implementation branch: `work/safety-testability-foundation`

Audit branch: `work/accessibility-analyzer-audit`

## Relationship to the upstream repository

This repository is a fork of `Phlypper/accessible-webpage-analyzer`.

The fork's `main` branch remains an unchanged copy of the upstream initial commit. The static audit is isolated on `work/accessibility-analyzer-audit`, and the first repair is isolated on `work/safety-testability-foundation`.

Nothing from the fork has been proposed to, merged into, or otherwise written to Jason Washburn's upstream repository.

## Upstream baseline

The upstream application is a small macOS desktop prototype consisting of:

- one PyQt6 interface;
- one Selenium and ChromeDriver webpage-inspection routine;
- plain-text, Markdown, HTML, and JSON report generation;
- spoken output through the macOS `say` command;
- support for a live URL or a local HTML file.

It reads selected computed CSS and element rectangles from the rendered DOM, groups elements under broad semantic containers, and summarizes common fonts, sizes, colors, backgrounds, and CSS display values.

## Completed fork work

### Initial audit

`docs/INITIAL_AUDIT_2026-07-21.md` records the complete static assessment, including the distinction between visual description, semantic analysis, accessible-interface analysis, and manual VoiceOver acceptance.

### Safety and testability foundation

The implementation branch now:

- prevents shell interpretation of webpage-derived speech text;
- escapes webpage-derived values in HTML reports;
- preserves raw evidence in structured JSON;
- guarantees Selenium cleanup through `finally`;
- converts viewport rectangles into stable document coordinates;
- creates a separate timestamped directory for every report run;
- identifies the analyzed source, time, viewport, and extraction counts;
- records omitted-element counts instead of silently hiding all extraction failures;
- uses safe local-file URLs;
- adds accessible names and descriptions to the principal interface elements;
- separates coordinate, report, output, and speech logic into testable modules;
- adds nine standard-library unit tests and a GitHub Actions quality workflow;
- replaces the malformed README with accurate installation, capability, limitation, and authorship information.

## Verification state

Passed locally:

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py accessible_analyzer tests
```

Result: nine tests passed and Python compilation passed.

Not yet verified:

- application startup on macOS;
- Chrome and ChromeDriver integration;
- live-URL analysis;
- local-file analysis;
- report-folder opening;
- spoken-output behavior on macOS;
- keyboard navigation and focus recovery;
- actual VoiceOver announcements.

These are runtime acceptance gates, not omissions that automated unit tests can erase.

## What the application still does not do

- run a general accessibility rules engine;
- inspect the browser accessibility tree;
- calculate WCAG contrast ratios;
- identify heading-order, accessible-name, landmark, form-label, focus, or live-region defects;
- capture or validate VoiceOver speech;
- use an AI model;
- perform analysis off the graphical main thread;
- support cancellation of a long analysis.

## Governing constraints for this fork

- Do not modify `main` directly.
- Do not open a pull request to upstream until the fork owner explicitly authorizes it.
- Preserve Jason Washburn's authorship and original repository history.
- Separate verified behavior from proposed behavior.
- Do not describe automated checks as substitutes for manual VoiceOver testing.
- Prefer small, reviewable changes with tests and explicit limitations.
- Do not introduce paid services or external AI dependencies without separate approval.
- Do not select a license on Jason's behalf.

## Next gate

The next responsible step is macOS runtime and VoiceOver acceptance testing of `work/safety-testability-foundation`. Only after those results are recorded should the fork owner decide whether to repair further, open a draft pull request, or keep the work private within the fork.
