---
id: greenfield
title: 3.2 Greenfield development
description: "Greenfield lifecycle: the fullest path, because both the product and the technical solution must be shaped."
sidebar_label: 3.2 Greenfield development
---

:::note Section summary
Greenfield lifecycle: the fullest path, because both the product and the technical solution must be shaped.
:::

Use the greenfield path when the target product, service, journey or application is being created as
a new solution. This is the fullest lifecycle because both the product and the technical solution
must be shaped. Work begins by bounding the increment and clarifying the opportunity and intended
outcome. The squad then assembles context, defines requirements, designs the experience and
architecture, creates the backlog and specification, plans, builds, validates, releases and learns.

## Lifecycle steps

| Lifecycle step | What the squad does | Agents | Gate |
|---|---|---|---|
| 0. Mobilise and assess | Bound the increment, name owners, confirm access, controls and baseline. | None (increment card, [baseline](/overview/baseline)) | Intake approval (PO) |
| 1. Discover and frame | Clarify the opportunity, user need, desired outcome and constraints. | Discovery notes in `docs/discovery/` | None |
| 2. Contextualise | Assemble approved domain, product, design, policy and technical context. | [Context Builder](/agents/context-builder) | Context readiness (FDE) |
| 3. Define requirements | Create and approve business and product requirements. | [BRD Builder](/agents/brd-builder), [PRD Builder](/agents/prd-builder) | Requirements approval (PO, FDA) |
| 4. Design experience and architecture | Define user experience, target solution, boundaries and architectural decisions. | ADR Creation, Arch Diagram Builder, Figma Extractor | Design and architecture approval (FDA) |
| 5. Create backlog and specification | Create epics and stories and convert approved context into an executable specification. | [Jira Backlog Manager](/agents/backlog-manager), [Spec-Clarify](/agents/spec-clarify) | Specification approval (PO) |
| 6. Plan and decompose | Define the solution plan, tasks and dependencies. | [Task-Planner](/agents/task-planner) | Plan approval (FDA), task approval (FDE) |
| 7. Build | Implement code and unit tests against approved tasks. | [Task-Implementor](/agents/task-implementor) | Code review (FDE) |
| 8. Validate | Complete code review, functional and non-functional testing and control checks. | [API Testing](/agents/api-testing), [Functional Testing](/agents/functional-testing), Compliance Reviewer | Quality and security gate (FDA) |
| 9. Release | Prepare the release, pass readiness gates and deploy with approval. | [Azure-Deploy](/agents/azure-deploy) | Release readiness (FDE), deployment approval (PO/PM) |
| 10. Operate and improve | Monitor production, learn and feed improvements into context and backlog. | Context Updater | Ongoing review (Ops) |

## Phase notes

### 0. Mobilise and assess

Select an appropriate project and bounded delivery increment before activating agents. Create the
increment card, name the accountable roles and confirm that repositories, tools and MCP servers are
accessible. See [Environment set-up](/getting-started/environment).

### 1. Discover and frame

**Mandatory for net-new products and journeys.** Define the customer or employee problem, personas,
desired outcomes, journey, value hypothesis, business constraints and policy or regulatory
requirements. Discovery outputs are the approved input to the BRD.

### 2. Contextualise

Establish the approved enterprise, domain, project and engineering context required by the agents.
For a greenfield project the Context Builder prompts for the business overview and technology stack
where existing project material is not yet available.

### 3. Define requirements

Use approved discovery outputs to develop the BRD and PRD, followed by business, product and
architecture approval. See [Convert raw requirements into a BRD](/getting-started/brd) and
[Convert the approved BRD into a PRD](/getting-started/prd).

### 4. Design experience and architecture

Emphasise journey and interaction design, design-system compliance, target architecture, API and
event contracts, data design, security and observability by design. Architecture decisions are
recorded as ADRs in `docs/architecture/decisions/`.

### 5. Create backlog and specification

Transform approved requirements and designs into implementable and traceable work. See
[Plan the implementation backlog](/getting-started/backlog) and
[Create the technical specification](/getting-started/specify).

### 6. Plan and decompose

Create a dependency-aware implementation plan for the approved specification. See
[Plan the implementation](/getting-started/plan).

### 7. Build

Implement the bounded increment against the approved plan and specification. See
[Implement the approved plan](/getting-started/implement).

### 8. Validate

Demonstrate that the increment meets approved business, technical, security and operational
requirements. See [Test the backend APIs](/getting-started/api-tests) and
[Test the frontend components](/getting-started/functional-tests).

### 9. Release

Prepare and authorise a controlled release through the Azure pipeline. Release approval and
production deployment authority remain with the named human roles.

### 10. Operate and improve

Monitor operational outcomes and continuously improve the product, context packages and agent chain.
