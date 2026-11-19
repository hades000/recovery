---
id: plan
title: 4.8 Plan the implementation
description: "Implementation Planner (Task-Planner): from the reviewed specification to a dependency-aware plan and task breakdown."
sidebar_label: 4.8 Plan
---

:::note Section summary
Implementation Planner (Task-Planner): from the reviewed specification to a dependency-aware plan and task breakdown.
:::

**Lifecycle phase:** 6 Plan and decompose · **Agent:** [Implementation Planner](/agents/task-planner) (`.github/agents/planner.agent.md`) · **Gate:** plan approval (FDA), task approval (FDE); Compliance Reviewer plan gate

:::warning Context reset
Start a new chat session before invoking the Implementation Planner. Begin planning only after the specification has been reviewed and its clarifications have been resolved.
:::

## Invoke the Implementation Planner agent

Provide the same `RUN_ID` and the specification artefacts in `output/<RUN_ID>/specify/`. Ensure the
applicable project context files in `.github/contexts/` are available to the agent.

Select **Implementation Planner** in Copilot Chat and use a prompt such as:

```text
Create the implementation plan and task breakdown for RUN_ID=<RUN_ID>.
Use the reviewed specification, preserve requirement traceability, and define dependencies,
verification, and unit-test work for each implementation task. Do not implement the tasks.
```

The agent creates planning artefacts under:

```text
output/<RUN_ID>/plan/
├── plan.md
├── tasks.md
├── contracts/backend-apis.json      (when APIs are in scope)
├── tests/scenarios.md
└── frontend/components.md           (when UI is in scope)
```

## Review the plan

Review `plan.md` and `tasks.md`, including the contracts, test scenarios and frontend component
inventory where applicable. Confirm that:

* [ ] Every in-scope specification item maps to implementation tasks and verification evidence
  (`SPEC-*` → `TASK-*`).
* [ ] Dependencies are explicit, and frontend work does not precede required backend contract
  verification.
* [ ] Unit tests are planned alongside implementation, with functional test scenarios identified
  separately.
* [ ] Clarifications are resolved, and design-evidence gates are met before dependent tasks proceed.
* [ ] `tasks.md` includes the required pre-submit checks.

The FDE or engineering lead checks that the plan covers the approved scope and does not introduce
unsupported design decisions.

## Compliance review

Complete the required **Compliance Reviewer** plan review (invoked automatically by the planner) and
address its findings before implementation. Then review the agent's `NEXT_STEP` status and start
the next stage manually.

:::warning Rule
No implementation begins until the approved plan satisfies the planning gate.
:::

Next: [4.9 Implement the approved plan](/getting-started/implement).
