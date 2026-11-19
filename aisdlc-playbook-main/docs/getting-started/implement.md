---
id: implement
title: 4.9 Implement the approved plan
description: "Implementation Builder (Task-Implementor): bounded implementation with unit tests and evidence, against approved tasks only."
sidebar_label: 4.9 Implement
---

:::note Section summary
Implementation Builder (Task-Implementor): bounded implementation with unit tests and evidence, against approved tasks only.
:::

**Lifecycle phase:** 7 Build · **Agent:** [Implementation Builder](/agents/task-implementor) (`.github/agents/implement.agent.md`) · **Gate:** code review (FDE)

:::warning Context reset
Start a new chat session before invoking the Implementation Builder. Use only the reviewed and approved plan and task set.
:::

## Invoke the Implementation Builder agent

Provide the same `RUN_ID`, the approved `output/<RUN_ID>/plan/tasks.md`, and the associated
specification and project context. Include `output/<RUN_ID>/plan/frontend/components.md` when the
plan contains frontend work.

Select **Implementation Builder** in Copilot Chat and use a prompt such as:

```text
Implement the approved tasks for RUN_ID=<RUN_ID> from output/<RUN_ID>/plan/tasks.md.
Follow the approved specification and project standards, create unit tests with the implementation,
and record implementation and verification evidence. Do not start later-stage testing agents.
```

The agent creates implementation artefacts under:

```text
output/<RUN_ID>/implement/
├── backend/
├── frontend/
└── integration/
```

together with the source code and unit tests in the repository.

## Review the implementation

Confirm that:

* [ ] Only approved tasks were implemented, and task-to-specification traceability is retained
  (`TASK-*` → `CODE-*`, `TEST-*`).
* [ ] Frontend and backend work are both complete where required, including related unit tests.
* [ ] Focused checks pass, and implementation evidence records the commands and results. Unit-test
  coverage meets the 80% gate for each supported metric on changed surfaces.
* [ ] Design fidelity, security, privacy and other applicable controls have been addressed.
* [ ] No unresolved blocker or unapproved gap is represented as complete.

The Application Engineer remains accountable for understanding the change, resolving failures and
confirming that the pull request is suitable for review. The FDE approves the pull request.

After human review, start the **API Tester** manually as the next stage, using the same `RUN_ID`
and the approved API contract artefacts.

Next: [4.10 Test the backend APIs](/getting-started/api-tests).
