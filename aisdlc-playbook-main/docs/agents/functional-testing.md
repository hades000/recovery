---
id: functional-testing
title: A.9 Functional Testing (Functional Automation Test)
description: "Converts approved requirements, designs and acceptance criteria into repeatable functional tests and execution evidence."
sidebar_label: A.9 Functional Testing
---

:::note Section summary
Converts approved requirements, designs and acceptance criteria into repeatable functional tests and execution evidence.
:::

**Type:** Custom · **Lifecycle group:** Quality and release · **Phase:** 8 Validate · **Toolkit file:** `.github/agents/functional-automation-test.agent.md`

The Functional Testing agent converts approved product requirements, stories, designs and
acceptance criteria into repeatable functional tests. It can prepare test scenarios, cases, data,
executable Playwright scripts and execution evidence for functional, role-based, negative and
boundary conditions. The Quality Engineer reviews coverage and results and retains the quality
decision.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| Functional, role-based, negative and boundary testing in approved environments (`UI In Scope: YES` in `spec.md`). | `output/<RUN_ID>/specify/spec.md`, plan and implementation evidence, relevant context, optional `plan/frontend/components.md`, `APP_URL` for the running authorised application, test standards. | Test strategy, test cases, data, executable Playwright scripts and execution evidence under `output/<RUN_ID>/functional-tests/attempt-<n>/` (`FT-*`), or an evidence-backed `NOT_APPLICABLE` report. | Quality Engineer reviews coverage, scripts and results and retains the quality decision. **Gate:** quality and security gate (FDA). |

## Behaviour

* Reads UI scope from `spec.md`; when `UI In Scope: NO` and design evidence is `NOT_REQUIRED` it
  writes an N/A report and launches no browser.
* Traces every test case to specified UI behaviour, component IDs when available, planned scenarios
  and acceptance evidence.
* Reconciles case counts with the JUnit output and makes unavailable components or gaps explicit.
* Uses the `playwright` MCP server with `data-testid` selectors.

## Limitations and stop conditions

* Reports `BLOCKED` when `spec.md` is missing, does not declare UI scope, or does not identify the
  in-scope UI behaviour; it never substitutes screens or features.
* Does not modify application behaviour to make tests pass.
* Uses authorised environments and synthetic data only; keeps sensitive information out of reports
  and captured artefacts.
* Acceptance checks outside API and UI automation remain visible as human-verification gaps, not
  fabricated results.

## Related: QA Test Case Generator

For manual test cases managed in Jira, the toolkit's **QA Test Case Generator**
(`.github/agents/qa-test-case-generator.agent.md`) derives test cases from a story's acceptance
criteria, business logic, error handling and general scenarios, writes them under
`output/test-cases/<story-key>/`, and, only after explicit QA approval, creates them as Jira Tasks
linked to the story with the `Tests` link type through the `jira` MCP server. See
[Supporting agents](/agents/supporting-agents#qa-test-case-generator).

Step-by-step: [4.11 Test the frontend components](/getting-started/functional-tests).
