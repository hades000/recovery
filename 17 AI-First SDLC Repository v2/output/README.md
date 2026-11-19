---
title: Run Output
description: "Layout of output/RUN_ID artefacts written by each lifecycle stage"
---

Every lifecycle run writes its artefacts under `output/{RUN_ID}/`. The `RUN_ID` is chosen when the
Technical Specifier is started and reused by every later stage of the same increment.

```text
output/{RUN_ID}/
├── specify/            spec.md, compliance-validation.md, figma/ (design evidence)
├── plan/               plan.md, tasks.md, contracts/, tests/scenarios.md, frontend/components.md
├── implement/          implementation and unit-test evidence (backend/, frontend/, integration/)
├── api-tests/          attempt-<n>/ API test suites, JUnit results, reports
├── functional-tests/   attempt-<n>/ Playwright functional tests, results, reports
├── review/             Compliance Reviewer findings (REVIEW-*)
└── docs/               Technical Documenter output (DOC-*)
output/test-cases/<story-key>/   QA Test Case Generator output
```

Attempt directories are never overwritten; a re-run creates `attempt-<n+1>/`.
