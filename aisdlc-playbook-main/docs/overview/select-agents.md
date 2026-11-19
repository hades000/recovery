---
id: select-agents
title: 2.5 Select relevant agents
description: "Select the agents required for the project type and lifecycle activities being delivered."
sidebar_label: 2.5 Select relevant agents
---

:::note Section summary
Select the agents required for the project type and lifecycle activities being delivered.
:::

Once the project type and lifecycle activities have been determined, identify the agents required to
support the bounded increment. The current SCBx agent set spans **requirements and discovery**,
**design, backlog and specification**, **plan and build**, and **quality and release**.

Agents are either **Core** (part of the standard chain) or **Custom** (built for SCBx). Agent
applicability also varies by project type. Greenfield delivery uses the requirements-building agents
as part of the standard flow, while Brownfield and Modernisation may reuse existing approved
artefacts and therefore treat some requirements and backlog agents as optional.

<object type="image/svg+xml" data="/diagrams/agent-chain.svg" className="diagram" aria-label="The agent chain grouped by lifecycle group, with the human reviewer for each agent">
  The agent chain grouped into requirements and discovery, design backlog and spec, plan and build, quality and release.
</object>
Click an agent to open its catalogue entry. [draw.io source](/diagrams/agent-chain.drawio)

## Greenfield

For Greenfield delivery, the agent chain supports the lifecycle from establishing context and
requirements through planning, implementation, testing and deployment.

| Lifecycle group | Agent | Purpose | Type |
|---|---|---|---|
| Requirements and discovery | [Context Builder](/agents/context-builder) | Ingest reference material to form context. | Custom |
| Requirements and discovery | [BRD Builder](/agents/brd-builder) | Drafts the BRD from discovery notes and Excel requirements. | Core |
| Requirements and discovery | [PRD Builder](/agents/prd-builder) | Converts the approved BRD into a product requirements document. | Core |
| Design, backlog and spec | [Jira Backlog Manager](/agents/backlog-manager) | Splits epics into Jira user stories and maintains the backlog. | Core |
| Design, backlog and spec | [Spec-Clarify](/agents/spec-clarify) | Builds the specification from context and resolves gaps with the BA. | Core |
| Plan and build | [Task-Planner](/agents/task-planner) | Breaks the specification into tasks using project context. | Core |
| Plan and build | [Task-Implementor](/agents/task-implementor) | Writes code and unit tests against the plan, with validation. | Core |
| Quality and release | [Code Review](/agents/supporting-agents#compliance-reviewer) | Reviews generated code and pull requests before merge. | Core |
| Quality and release | [API Testing](/agents/api-testing) | Generates and runs API tests from approved specifications. | Custom |
| Quality and release | [Functional Testing](/agents/functional-testing) | Turns requirements into Playwright scripts and test evidence. | Custom |
| Quality and release | [Azure-Deploy](/agents/azure-deploy) | Prepares, validates and deploys releases to Azure. | Core |

## Brownfield and Modernisation

Brownfield and Modernisation use the same agent capability set, but the starting point depends on
the approved artefacts and context already available.

The **Context Builder** remains relevant to bring existing project and application material into
context. **BRD Builder, PRD Builder and Jira Backlog Manager are optional** because existing
approved requirements or backlog artefacts may already be available and suitable for reuse.

| Lifecycle group | Agent | Purpose | Applicability | Type |
|---|---|---|---|---|
| Requirements and discovery | [Context Builder](/agents/context-builder) | Ingest reference material to form context. | Applicable | Custom |
| Requirements and discovery | [BRD Builder](/agents/brd-builder) | Drafts the BRD from discovery notes and Excel requirements. | Optional | Core |
| Requirements and discovery | [PRD Builder](/agents/prd-builder) | Converts the approved BRD into a product requirements document. | Optional | Core |
| Design, backlog and spec | [Jira Backlog Manager](/agents/backlog-manager) | Splits epics into Jira user stories and maintains the backlog. | Optional | Core |
| Design, backlog and spec | [Spec-Clarify](/agents/spec-clarify) | Builds the specification from context and resolves gaps with the BA. | Applicable | Core |
| Plan and build | [Task-Planner](/agents/task-planner) | Breaks the specification into tasks using project context. | Applicable | Core |
| Plan and build | [Task-Implementor](/agents/task-implementor) | Writes code and unit tests against the plan, with validation. | Applicable | Core |
| Quality and release | [Code Review](/agents/supporting-agents#compliance-reviewer) | Reviews generated code and pull requests before merge. | Applicable | Core |
| Quality and release | [API Testing](/agents/api-testing) | Generates and runs API tests from approved specifications. | Applicable | Custom |
| Quality and release | [Functional Testing](/agents/functional-testing) | Turns requirements into Playwright scripts and test evidence. | Applicable | Custom |
| Quality and release | [Azure-Deploy](/agents/azure-deploy) | Prepares, validates and deploys releases to Azure. | Applicable | Core |

## Applying the agent chain

The selected project type determines which parts of the agent chain are needed.

**Greenfield** typically begins by establishing context and developing business and product
requirements before progressing into backlog, specification, planning, implementation, testing and
deployment.

**Brownfield and Modernisation** may begin from existing approved requirements, backlog or other
project artefacts. Where those artefacts remain suitable for the increment, the corresponding BRD,
PRD or backlog-generation activities do not need to be repeated. The squad can instead establish
the required context and progress to specification clarification and the downstream delivery
agents.

:::tip
Agent selection follows the lifecycle activities required for the bounded increment rather than
activating every available agent. Record the selection in the increment card.
:::

Where each agent comes from (HVE Core extension or the toolkit) is described on the
[toolkit page](/toolkit#agents).
