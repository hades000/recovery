---
id: spec-clarify
title: A.5 Spec-Clarify (Technical Specifier)
description: "Converts approved requirements, architecture, design and standards into an implementation-ready specification and surfaces what is unresolved."
sidebar_label: A.5 Spec-Clarify
---

:::note Section summary
Converts approved requirements, architecture, design and standards into an implementation-ready specification and surfaces what is unresolved.
:::

**Type:** Core · **Lifecycle group:** Design, backlog and spec · **Phase:** 5 Create backlog and specification · **Toolkit file:** `.github/agents/specify.agent.md` (agent name: Technical Specifier)

Spec-Clarify converts approved requirements, architecture, design and standards into an
implementation-ready specification. It identifies missing information, conflicting assumptions and
unresolved questions before planning or coding begins. The specification becomes the main
implementation reference only after the relevant business and technical owners resolve and approve
the open points.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| Before planning and implementation for a bounded increment. Applicable to every path. | Approved requirements (Jira story key, canonical requirement file or PRD), design, architecture, context (`.github/contexts/`) and standards (`.github/rules/`). | `output/<RUN_ID>/specify/spec.md`, `compliance-validation.md`, acceptance criteria and clarification questions; design evidence under `specify/figma/`. | FDE coordinates clarification; accountable business and technical roles approve resolved content. **Gate:** specification approval (PO) after the Compliance Reviewer spec gate. |

## What the specification contains

* `SPEC-*` items traceable to `FR-*`/`NFR-*` and `US-*`.
* Frontend and backend assessed separately against the story: required changes, contracts, models,
  controls and files to change; unchanged or not-applicable surfaces documented with evidence.
* `API In Scope: YES|NO` and `UI In Scope: YES|NO` declarations read by the testing agents.
* Design evidence status (`NOT_REQUIRED`, `AVAILABLE`, `PENDING_MANUAL_UPLOAD`).
* Domain controls (privacy, compliance, audit, security) applied only when in scope.
* Clarifications listed explicitly; no unanswered decision is treated as an assumption.

## Limitations and stop conditions

* Runs only when a human starts it; never as part of an automatic chain. It may invoke the Figma
  Extractor for design evidence and invokes the Compliance Reviewer at the spec gate.
* Does not invoke the Implementation Planner or later agents.
* Stops with `BLOCKED` when requirements are missing, when the review cannot be invoked, or when
  Critical, High or Medium review findings remain unresolved.
* A frontend story with no design evidence at all blocks downstream planning until screenshots are
  supplied and the specifier is re-run.

Step-by-step: [4.7 Create the technical specification](/getting-started/specify).
