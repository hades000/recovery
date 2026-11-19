---
id: task-planner
title: A.6 Task-Planner (Implementation Planner)
description: "Decomposes the approved specification into ordered implementation tasks with explicit dependencies and expected outcomes."
sidebar_label: A.6 Task-Planner
---

:::note Section summary
Decomposes the approved specification into ordered implementation tasks with explicit dependencies and expected outcomes.
:::

**Type:** Core · **Lifecycle group:** Plan and build · **Phase:** 6 Plan and decompose · **Toolkit file:** `.github/agents/planner.agent.md` (agent name: Implementation Planner)

Task-Planner decomposes the approved specification and solution approach into ordered
implementation tasks. It makes dependencies, sequencing and expected outcomes explicit so work can
be executed in controlled increments. The FDE or engineering lead checks that the plan covers the
approved scope and does not introduce unsupported design decisions.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| After specification approval. | `output/<RUN_ID>/specify/spec.md`, project context and engineering standards. | `output/<RUN_ID>/plan/plan.md`, `tasks.md` and dependency sequence; `contracts/backend-apis.json`, `tests/scenarios.md`, `frontend/components.md` where applicable. | FDE or engineering lead validates completeness and ordering. **Gates:** plan approval (FDA) and task approval (FDE) after the Compliance Reviewer plan gate. |

## What the plan contains

* `TASK-*` items mapped to `SPEC-*` and back to requirements.
* Explicit dependencies; frontend work does not precede required backend contract verification.
* Unit-test work planned alongside each implementation task; functional test scenarios identified
  separately for the testing agents.
* Pre-submit checks in `tasks.md`.
* Design-evidence gates that must be met before dependent tasks proceed.

## Limitations and stop conditions

* Starts only after the specification review is complete and clarifications are resolved.
* Does not implement tasks and does not invoke the Implementation Builder.
* Invokes the Compliance Reviewer at the plan gate; Critical, High or Medium findings block the
  hand-off until a human records remediation or acceptance.

Step-by-step: [4.8 Plan the implementation](/getting-started/plan).
