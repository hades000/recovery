---
id: supporting-agents
title: A.11 Supporting agents
description: "Agents that run at the gates and between stages: review, context maintenance, design evidence, documentation and traceability."
sidebar_label: A.11 Supporting agents
---

:::note Section summary
Agents that run at the gates and between stages: review, context maintenance, design evidence, documentation and traceability.
:::

These toolkit agents are not steps in the main chain, but the chain depends on them. All live in
`.github/agents/` after the toolkit is installed.

## Compliance Reviewer

**File:** `reviewer.agent.md` · **Invoked by:** Technical Specifier (spec gate), Implementation Planner (plan gate), Technical Documenter (post-test code gate); also user-invocable.

Reviews specifications, plans, code, tests and documentation against the rules in `.github/rules/`
and produces `REVIEW-*` findings with a `PASS` or `FAIL` status.

| Finding severity | Effect on the hand-off |
|---|---|
| Critical, High, Medium | Blocks until a human records remediation (and the review is re-run) or explicit acceptance. |
| Low only | `FAIL` status is preserved and `REVIEW_GATE_WARNING` is emitted; the hand-off is not automatically stopped, but findings stay visible for human disposition. |

Independent stage hard gates (failed required unit tests, coverage below 80%) still block
regardless of review outcome. This is the toolkit's implementation of the **Code Review** step in
the [agent chain](/overview/select-agents#greenfield); the HVE Core Code Review agent can be used in
addition for pull-request review.

## Context Updater

**File:** `context-updater.agent.md` · **Phase:** 2 Contextualise, 10 Operate and improve (on demand at any phase).

Keeps `.github/contexts/` synchronised as the project evolves: Confluence or document changes,
dependency and framework changes, domain guidance, custom standards or user request. Classifies
changes as MINOR, MODERATE or MAJOR, tracks them with `CTX-UPDATE-*` IDs, escalates MAJOR changes
for approval and flags conflicts between the detected state and approved specifications or plans.
This is how production learning flows back into context in the Operate and improve phase.

## Figma Extractor

**File:** `figma-extractor.agent.md` · **Phase:** 4 Design, 5 Specification · **Invoked by:** Technical Specifier when a requirement contains Figma links; also user-invocable.

Extracts design evidence (screens, components, styles) from Figma into
`output/<RUN_ID>/specify/figma/`. Figma failures never block: the specifier falls back to Jira or
Confluence screenshots or manual uploads with `SCR-*` IDs.

## QA Test Case Generator

**File:** `qa-test-case-generator.agent.md` · **Phase:** 8 Validate.

Generates manual test cases from a Jira story (acceptance criteria, business logic, error handling,
general scenarios) into `output/test-cases/<story-key>/`, using the template in
`.github/templates/qa-test-case-template.md`. After explicit QA approval it creates the cases as
Jira Tasks and links them to the story with the `Tests` link type through the `jira` MCP server
(`jira_get_issue`, `jira_search_issues`, `jira_get_create_metadata`, `jira_get_link_types`,
`jira_create_issue`, `jira_create_issue_link`).

## Technical Documenter

**File:** `technical-documenter.agent.md` · **Phase:** 8 Validate, 9 Release.

Produces `DOC-*` documentation from the specification, components, implementation and test
evidence. Before documenting, it invokes the Compliance Reviewer as the post-test code gate, using
implementation and unit-test evidence and both testing-stage reports.

## Traceability Manager

**File:** `traceability-manager.agent.md` · **Phase:** between phases (intake gate, final reconciliation).

Reconciles every ID in `requirement/Traceability_Matrix.md` along the chain
`CTX → BRD → FR/NFR → US → SPEC → TASK → CODE → APT/FT/TEST → REVIEW → DOC` and flags gaps:
orphaned IDs, requirements without specifications, specifications without tasks, tasks without
code, in-scope APIs or UI behaviour without test results, compliance requirements without review
evidence, and missing repository metadata.

## Workflow prompts

Two runbook prompts in `.github/prompts/` sequence the toolkit agents. Both pause after every stage
and continue only on explicit human instruction:

| Prompt | Use |
|---|---|
| `intake-to-spec.prompt.md` | Consolidate an existing requirement folder into canonical requirements and run the intake traceability gate; stops before specification. |
| `intake-to-implementation.prompt.md` | The full spec-driven run from existing documents to implementation, one stage per invocation. |
