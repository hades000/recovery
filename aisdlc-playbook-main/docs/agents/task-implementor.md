---
id: task-implementor
title: A.7 Task-Implementor (Implementation Builder)
description: "Executes bounded tasks from the approved plan, producing source code and unit tests within the repository's standards and guardrails."
sidebar_label: A.7 Task-Implementor
---

:::note Section summary
Executes bounded tasks from the approved plan, producing source code and unit tests within the repository's standards and guardrails.
:::

**Type:** Core · **Lifecycle group:** Plan and build · **Phase:** 7 Build · **Toolkit file:** `.github/agents/implement.agent.md` (agent name: Implementation Builder)

Task-Implementor executes bounded tasks from the approved specification and plan. It produces
source-code changes and unit tests within the supplied repository context, standards and guardrails.
The Application Engineer remains accountable for understanding the change, resolving failures and
confirming that the pull request is suitable for review.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| Bounded, approved implementation work. | Approved `output/<RUN_ID>/plan/tasks.md`, codebase, standards (`.github/rules/`), context (`.github/contexts/`) and test expectations; `plan/frontend/components.md` for frontend work. | Source code and unit tests; implementation and verification evidence under `output/<RUN_ID>/implement/` (`CODE-*`, `TEST-*`). | Application Engineer remains accountable for implementation and pull-request quality. **Gate:** code review (FDE). |

## Guardrails

* Implements only approved tasks and retains task-to-specification traceability.
* Both frontend and backend are assessed against story scope; only changed surfaces require
  implementation and unit tests, with an 80% coverage gate per supported metric.
* Records the commands run and their results as evidence.
* Applies design fidelity, security, privacy and other in-scope controls.
* Never includes real customer data, credentials or secrets in code, tests or evidence.

## Limitations and stop conditions

* Does not start the testing agents; the human starts the API Tester next.
* Reports unresolved blockers and unapproved gaps explicitly rather than representing them as
  complete.
* Stops when a task depends on a design-evidence gate or a clarification that is not yet resolved.

Step-by-step: [4.9 Implement the approved plan](/getting-started/implement).
