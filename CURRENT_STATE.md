# Current state

Last updated: 2026-07-21

Branch: `work/accessibility-analyzer-audit`

## Relationship to the upstream repository

This repository is a fork of `Phlypper/accessible-webpage-analyzer`.

The fork's `main` branch remains an unchanged copy of the upstream initial commit. All assessment work is isolated on `work/accessibility-analyzer-audit`. Nothing in this branch has been proposed to or merged into the upstream repository.

## What currently exists

The upstream application is a small macOS desktop prototype consisting of:

- one PyQt6 interface;
- one Selenium and ChromeDriver webpage-inspection routine;
- plain-text, Markdown, HTML, and JSON report generation;
- optional spoken output through the macOS `say` command;
- support for a live URL or a local HTML file.

The implementation reads computed CSS and element rectangles from the rendered DOM. It groups elements under broad semantic container names and summarizes common fonts, font sizes, colors, backgrounds, and CSS display values.

## What the prototype does not yet do

The current application does not yet:

- run an accessibility rules engine;
- inspect the browser accessibility tree;
- test keyboard or screen-reader interaction;
- capture or validate VoiceOver speech;
- use an AI model;
- calculate WCAG contrast ratios;
- identify heading-order, accessible-name, landmark, form-label, focus, or live-region defects;
- distinguish application defects from browser or operating-system defects;
- provide automated tests or continuous integration;
- protect report generation from untrusted webpage strings;
- preserve a durable, source-identified audit history.

## Current assessment

The concept is valuable: translate visually organized webpage information into language useful to a blind developer. The present implementation is a proof of concept rather than a reliable accessibility-analysis instrument.

The first contribution phase should preserve the original premise while establishing truthful scope, safe output handling, deterministic extraction, testable modules, and a layered analysis model:

1. visual and layout description;
2. semantic document analysis;
3. accessible-name and interaction analysis;
4. manual screen-reader acceptance evidence.

## Governing constraints for this fork

- Do not modify `main` directly.
- Do not open a pull request to upstream until the fork owner explicitly authorizes it.
- Preserve Jason Washburn's authorship and the original repository history.
- Separate verified behavior from proposed behavior.
- Do not describe automated checks as substitutes for manual VoiceOver testing.
- Prefer small, reviewable changes with tests and explicit limitations.
- Do not introduce paid services or external AI dependencies without separate approval.

## Immediate next work

The complete initial static audit is recorded in `docs/INITIAL_AUDIT_2026-07-21.md`.

The next implementation branch should be created from this audited branch only after the audit findings are reviewed. The recommended first implementation is a safety and testability foundation, not a large feature expansion.
