# iPhone-first contribution pivot

Date: 2026-07-21

Branch: `work/iphone-web-analyzer-foundation`

## Governing operating constraint

The fork owner develops, reviews, and accepts projects exclusively through an iPhone using Safari and VoiceOver. A Mac, Windows computer, laptop, desktop, local terminal, locally installed Python environment, or desktop screen reader cannot be an acceptance requirement.

This constraint governs architecture rather than merely testing instructions.

## Correction

The earlier `work/safety-testability-foundation` branch improved Jason Washburn's existing PyQt6 and Selenium desktop prototype, but it retained a Mac runtime as the delivery target. That branch is preserved as a private technical experiment and must not be proposed upstream as the primary contribution.

No Mac runtime or VoiceOver-on-macOS gate will be assigned to the fork owner.

## New product target

Create a hosted, mobile-first webpage analyzer that can be:

- opened in iPhone Safari;
- navigated and operated with VoiceOver;
- tested through a nonproduction web preview;
- developed through GitHub and connected deployment tools without local-computer work;
- used to submit a public webpage address or an HTML file;
- returned as structured, readable, downloadable analysis rather than desktop-only files.

## Proposed architecture

### Accessible web interface

A small browser interface will provide:

- a clearly labelled webpage-address field;
- an HTML-file upload alternative;
- an Analyze button with stable focus behavior;
- restrained status announcements;
- a structured results document with headings and landmarks;
- plain-text and JSON export;
- explicit distinction between visual-layout description and accessibility findings.

### Hosted analysis service

Live webpage analysis cannot rely solely on code running inside iPhone Safari because browser isolation prevents arbitrary cross-site DOM and computed-style inspection. A hosted serverless function will load the submitted public page in a headless browser, extract bounded evidence, and return structured JSON.

The first hosted proof will test whether Netlify Functions can run a serverless Chromium package within free-plan memory, execution, and deployment-size limits. This is an engineering hypothesis, not yet an accepted fact for this repository.

### Safety boundaries

The service must:

- accept only public HTTP and HTTPS targets;
- reject localhost, loopback, private-network, link-local, and metadata-service destinations;
- impose navigation and total execution timeouts;
- cap returned elements and response size;
- block downloads and unwanted protocols;
- close the browser in every outcome;
- escape all untrusted report content;
- avoid storing analyzed pages or reports by default;
- state clearly that automated analysis does not prove VoiceOver usability.

## Delivery sequence

1. Create the accessible iPhone-oriented interface with deterministic sample data.
2. Deploy a nonproduction preview and conduct iPhone Safari VoiceOver acceptance.
3. Add an HTML-file analysis path that does not require cross-origin navigation.
4. Add the bounded hosted live-URL proof.
5. Measure function deployment size, execution time, memory behavior, and free-plan consumption.
6. Keep the live-URL feature only if it works reliably without paid infrastructure.
7. Add semantic accessibility rules only after the delivery architecture passes.

## Acceptance rules

- No user acceptance step may require a laptop or desktop.
- Automated browser or unit tests may support the work but cannot replace manual iPhone Safari VoiceOver acceptance.
- A desktop-only success does not count as project success.
- No upstream pull request will be opened until the iPhone-accessible preview and bounded hosted architecture have passed.
- If free hosted browser execution proves unreliable, the repository will retain the iPhone interface and HTML-upload analysis, while live rendered-URL analysis will be documented as blocked rather than shifted back onto a desktop user.
