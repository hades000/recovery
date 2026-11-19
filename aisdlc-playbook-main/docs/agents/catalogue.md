---
id: catalogue
title: Appendix A. Agent catalogue
description: "Agent catalogue: operating contracts for every agent in the chain."
sidebar_label: A.1 How to use the catalogue
---

## A.1 How to use the catalogue

:::note Section summary
Agent catalogue: operating contracts for every agent in the chain.
:::

The agent catalogue translates the lifecycle into usable delivery components. Each entry explains
the activity an agent supports, the context it requires, the output it creates and the human role
that reviews or accepts that output. Use the catalogue **after** the squad has
[classified the increment](/overview/project-types) and [tailored the lifecycle](/overview/tailoring),
so the selected agents correspond to actual delivery needs rather than being added because they are
available.

Catalogue entries should be read as **operating contracts**:

| Field | Meaning |
|---|---|
| Purpose | The problem the agent helps solve. |
| Use when | The lifecycle activity and project conditions for which the agent is relevant. |
| Approved inputs | The artefacts and context the agent may use. |
| Outputs | The artefacts or evidence the agent produces, not what is automatically accepted. |
| Human review | The role that checks the output and the decision that remains human. |
| Limitations and stop conditions | When the output must be clarified, escalated or rejected. |

<object type="image/svg+xml" data="/diagrams/agent-chain.svg" className="diagram" aria-label="The agent chain with lifecycle groups and human reviewers">
  The agent chain grouped by lifecycle group.
</object>
Click an agent to open its entry. [draw.io source](/diagrams/agent-chain.drawio)

## The agents

| Agent | One-line description | Source |
|---|---|---|
| [Context Builder](/agents/context-builder) | Creates a unified project context from business, technical, compliance, standards, documentation and codebase sources to support downstream agent-enabled delivery. | Toolkit `context-builder.agent.md` |
| [BRD Builder](/agents/brd-builder) | Converts business problems, objectives and discovery inputs into a structured and traceable Business Requirements Document for stakeholder review and approval. | HVE Core |
| [PRD Builder](/agents/prd-builder) | Translates approved business direction into detailed, measurable and testable product requirements for downstream design, engineering and validation. | HVE Core |
| [Jira Backlog Manager](/agents/backlog-manager) | Transforms approved product requirements or epics into a structured delivery backlog of epics, user stories and acceptance criteria. | HVE Core |
| [Spec-Clarify](/agents/spec-clarify) | Converts approved requirements, architecture, design and standards into an implementation-ready specification while identifying gaps, conflicts and unresolved questions. | Toolkit `specify.agent.md` |
| [Task-Planner](/agents/task-planner) | Decomposes the approved specification and solution approach into ordered implementation tasks with explicit dependencies and expected outcomes. | Toolkit `planner.agent.md` |
| [Task-Implementor](/agents/task-implementor) | Executes bounded implementation tasks against the approved specification and plan, producing source-code changes and associated unit tests. | Toolkit `implement.agent.md` |
| [API Testing](/agents/api-testing) | Generates and executes API tests against approved interface specifications and acceptance criteria, producing test results and evidence for review. | Toolkit `api-tester.agent.md` |
| [Functional Testing](/agents/functional-testing) | Converts approved requirements, designs and acceptance criteria into repeatable functional tests, executable scripts and test evidence. | Toolkit `functional-automation-test.agent.md` |
| [Azure-Deploy](/agents/azure-deploy) | Prepares deployment artefacts, validates configuration and executes approved Azure deployments after required quality, security and readiness checks. | HVE Core |

[Supporting agents](/agents/supporting-agents) (Compliance Reviewer, Context Updater, Figma
Extractor, QA Test Case Generator, Technical Documenter, Traceability Manager) run at the gates and
between stages.

Toolkit agents install for both runtimes. In Claude Code the subagent name is the kebab-case form of
the display name, for example Technical Specifier is `technical-specifier`; see
[4.1a Run the agents in Claude Code](/getting-started/claude-code).
