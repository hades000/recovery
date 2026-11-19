---
id: overview
title: 4. Pilot pre-initiation and getting started
description: "Step-by-step execution of one increment with the toolkit, from raw requirements to tested code."
sidebar_label: Overview
---

:::note Section summary
Step-by-step execution of one increment with the toolkit, from raw requirements to tested code.
:::

Before beginning the pilot workflow, confirm that the required development environment, approved
agents, source documents and backlog platform are available to the squad. Then run the stages
below, one at a time. Every stage is started by a human, produces its output, stops for review and
reports `NEXT_STEP`.

<object type="image/svg+xml" data="/diagrams/stage-run.svg" className="diagram" aria-label="How one stage runs: the human starts the agent in a new chat, the agent reads the toolkit context and rules, writes its output under output/RUN_ID, the Compliance Reviewer checks it at the gate, and the human reviews and approves before starting the next stage">
  Swimlanes: Squad, Agent, Toolkit files, Gate.
</object>
Click a step to open its explanation. [draw.io source](/diagrams/stage-run.drawio)

## The stages

| # | Stage | Agent | Output | Page |
|---|---|---|---|---|
| 4.1 | Set up the environment | HVE Core All extension, toolkit VSIX or `install.sh` | `.github/` in the repository | [Environment](/getting-started/environment) |
| 4.1a | Run the lifecycle agents in Claude Code | Claude Code subagents | `.claude/agents/`, `.mcp.json` | [Claude Code](/getting-started/claude-code) |
| 4.2 | Convert raw requirements into a BRD | BRD Builder | `docs/brds/<brd>.md` | [BRD](/getting-started/brd) |
| 4.4 | Convert the approved BRD into a PRD | PRD Builder | `docs/prds/<prd>.md` | [PRD](/getting-started/prd) |
| 4.5–4.6 | Plan and create the backlog | Jira / ADO Backlog Manager | Epics, user stories, sprint | [Backlog](/getting-started/backlog) |
| 4.7 | Create the technical specification | Technical Specifier (Spec-Clarify) | `output/<RUN_ID>/specify/spec.md` | [Specify](/getting-started/specify) |
| 4.8 | Plan the implementation | Implementation Planner (Task-Planner) | `output/<RUN_ID>/plan/plan.md`, `tasks.md` | [Plan](/getting-started/plan) |
| 4.9 | Implement the approved plan | Implementation Builder (Task-Implementor) | Source code, unit tests, `output/<RUN_ID>/implement/` | [Implement](/getting-started/implement) |
| 4.10 | Test the backend APIs | API Tester | `output/<RUN_ID>/api-tests/attempt-<n>/` | [API tests](/getting-started/api-tests) |
| 4.11 | Test the frontend components | Functional Automation Test | `output/<RUN_ID>/functional-tests/attempt-<n>/` | [Functional tests](/getting-started/functional-tests) |

## Working rules

:::warning Context reset
Start a new chat session before invoking each stage agent so that the context for the new phase is clear and only the approved artefacts of the previous stage are carried forward.
:::

* **One `RUN_ID` per increment.** It is chosen when the Technical Specifier starts and reused by
  every later stage. All run artefacts live under `output/<RUN_ID>/`.
* **Review before you proceed.** Each page lists what to confirm in the output. The agent's
  `NEXT_STEP` tells you which stage to start next; start it manually.
* **Compliance Reviewer at the gates.** The Technical Specifier, Implementation Planner and
  Technical Documenter invoke the Compliance Reviewer automatically. Critical, High or Medium
  findings block the hand-off until a human records remediation or explicit acceptance; a `FAIL`
  with only Low findings emits `REVIEW_GATE_WARNING` and needs human disposition.
* **Claude Code users.** Invoke the same stage agents from the `@` typeahead, for example
  `@agent-technical-specifier` or `@agent-implementation-planner`; [4.1a Claude Code](/getting-started/claude-code)
  mirrors the stage pages with Claude Code prompts.
* **No secrets in chat.** Keep credentials in named environment variables or the MCP server's
  prompted inputs; never paste tokens or customer data into a prompt.
* **Brownfield and modernisation increments** may skip 4.2 to 4.6 when approved requirements and
  backlog already exist; record the decision in the lifecycle tailoring record and start at 4.7.
