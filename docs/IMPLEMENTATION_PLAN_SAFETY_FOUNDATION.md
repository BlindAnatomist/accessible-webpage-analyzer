# Safety and testability foundation

Status: implemented on `work/safety-testability-foundation`; local verification passed; upstream review not requested

Parent branch: `work/accessibility-analyzer-audit`

Implementation branch: `work/safety-testability-foundation`

## Objective

Preserve the prototype's present user-facing purpose while repairing the defects that make arbitrary webpage analysis unsafe, difficult to test, and easy to misrepresent.

## Implemented

- removed shell interpretation from speech output;
- escaped analyzed webpage strings in HTML reports;
- guaranteed Selenium driver cleanup through `finally`;
- corrected document coordinates after scrolling;
- normalized local file URLs with `Path.as_uri()`;
- recorded extraction warning counts instead of silently discarding every failure;
- created timestamped output directories;
- extracted report, coordinate, output, and speech logic into pure, testable modules;
- added nine standard-library unit tests;
- added a lightweight GitHub Actions quality workflow;
- repaired README formatting and limited claims to implemented behavior;
- added accessible names and descriptions to the report field and principal controls.

## Local verification

The following commands passed in the implementation environment:

```bash
python -m unittest discover -s tests -v
python -m compileall -q app.py accessible_analyzer tests
```

Result: nine tests passed. Python compilation passed.

The graphical application itself was not run because the implementation environment did not provide macOS, a graphical session, Chrome, ChromeDriver, or VoiceOver. Runtime and VoiceOver acceptance remain separate gates.

## Deferred

- worker-thread conversion and cancellation;
- browser accessibility-tree inspection;
- WCAG contrast calculations;
- heading, landmark, name, role, and form-label rules;
- AI-generated descriptions;
- macOS VoiceOver acceptance testing;
- dependency pinning pending confirmation of Jason's supported Python and macOS versions;
- licensing decisions, which belong to Jason.

## Acceptance-condition status

- Passed: no webpage-derived value is passed through a shell.
- Passed by unit test: HTML output escapes webpage-derived values.
- Passed by unit test: document coordinates include scroll offsets.
- Passed by source inspection and compilation: driver cleanup occurs through `finally`.
- Passed: report generation is testable without PyQt6, Selenium, Chrome, or macOS.
- Passed: tests cover HTML escaping, JSON schema metadata, coordinate normalization, timestamped output paths, and safe speech invocation.
- Implemented: the quality workflow runs unit tests and Python compilation.
- Passed by source inspection: README claims do not exceed implemented behavior.
- Preserved: no pull request has been opened upstream.

## Remaining gate before upstream proposal

Run the application on Jason's supported macOS environment with Chrome and VoiceOver. Confirm startup, live-URL analysis, local-file analysis, report-folder behavior, speech behavior, failure recovery, and predictable keyboard focus. Any defect found there should be repaired in this fork before an upstream pull request is opened.
