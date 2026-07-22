# Safety and testability foundation

Status: planned

Parent branch: `work/accessibility-analyzer-audit`

Proposed implementation branch: `work/safety-testability-foundation`

## Objective

Preserve the prototype's present user-facing purpose while repairing the defects that make arbitrary webpage analysis unsafe, difficult to test, and easy to misrepresent.

## In scope

- remove shell interpretation from speech output;
- escape analyzed webpage strings in HTML reports;
- guarantee Selenium driver cleanup;
- correct document coordinates after scrolling;
- normalize local file URLs safely;
- record extraction warnings instead of silently discarding all failures;
- create timestamped output directories;
- extract report and speech logic into pure, testable modules;
- add standard-library unit tests and a lightweight GitHub Actions quality check;
- repair README formatting and describe implemented capabilities accurately.

## Deferred

- worker-thread conversion and cancellation;
- browser accessibility-tree inspection;
- WCAG contrast calculations;
- heading, landmark, name, role, and form-label rules;
- AI-generated descriptions;
- macOS VoiceOver acceptance testing;
- dependency pinning pending confirmation of Jason's supported Python and macOS versions;
- licensing decisions, which belong to Jason.

## Acceptance conditions

- no webpage-derived value is passed through a shell;
- HTML output escapes webpage-derived values;
- document coordinates remain stable after scrolling;
- driver cleanup occurs through `finally`;
- report generation can be tested without PyQt6, Selenium, Chrome, or macOS;
- tests cover HTML escaping, JSON schema metadata, coordinate normalization, timestamped output paths, and safe speech invocation;
- the quality workflow runs unit tests and Python compilation;
- README claims do not exceed implemented behavior;
- no pull request is opened upstream without explicit authorization.
