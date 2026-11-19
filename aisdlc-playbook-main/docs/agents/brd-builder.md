---
id: brd-builder
title: A.3.1 BRD Builder
description: "Establishes why an initiative is required, what outcomes it must achieve, who is affected and what constraints apply."
sidebar_label: A.3.1 BRD Builder
---

## A.3 BRD and PRD Builder agents

This section describes how the HVE Core **BRD Builder** and [**PRD Builder**](/agents/prd-builder)
agents are used within the AI-enabled Product Development Lifecycle to create structured,
traceable and reviewable requirements documents.

## A.3.1 BRD Builder

:::note Section summary
Establishes why an initiative is required, what outcomes it must achieve, who is affected and what constraints apply.
:::

**Type:** Core · **Lifecycle group:** Requirements and discovery · **Phase:** 3 Define requirements · **Source:** HVE Core All extension

### Purpose

The Business Requirements Document (BRD) Builder supports the discovery, definition and governance
of business requirements. It helps teams convert an initial business idea, problem statement or
transformation objective into a structured BRD that can be reviewed and approved by business and
technology stakeholders.

### When to use

Use the BRD Builder when the team needs to:

* Define the business problem or opportunity.
* Establish business objectives and expected outcomes.
* Identify stakeholders, decision owners and impacted user groups.
* Document the current-state challenges and target-state aspirations.
* Define business scope and exclusions.
* Capture high-level business requirements.
* Record assumptions, dependencies, constraints and risks.
* Define measurable business success indicators.
* Establish governance and approval expectations before detailed product design begins.

### BRD lifecycle

| Phase | What the agent does |
|---|---|
| **Discover** | Establishes the business context and problem framing: business drivers and strategic goals, current-state challenges, stakeholders and decision owners, target users or business groups, initial scope and exclusions, expected business outcomes. |
| **Define** | Converts the discovered information into structured and traceable business requirements: business requirements, business rules and policies, success measures, assumptions and constraints, dependencies, business and delivery risks, requirement priorities, supporting evidence or source references. |
| **Govern** | Prepares the BRD for formal review and controlled hand-off: reviews completeness, identifies unresolved questions, confirms requirement ownership, records approval and governance expectations, establishes the approved BRD as the baseline for PRD development. |

### Typical inputs

Business problem statements, transformation objectives, workshop notes, stakeholder interviews,
existing process documents, policies and standards, customer or employee feedback, business metrics
and KPIs, existing architecture or programme documentation, known assumptions, risks and
dependencies.

### Expected outputs

Executive summary; business context and problem statement; business objectives and expected
outcomes; stakeholder and user-group details; current-state challenges; in-scope and out-of-scope
items; business requirements; business rules; success measures; assumptions and constraints;
dependencies and risks; governance and approval information; traceability to supporting sources.

Written to `docs/brds/<brd_name>.md`.

### Example SCBx usage

```text
Create a BRD for the SCBx AI-enabled Product Development Lifecycle initiative.

Business context:
- Product squads currently use different engineering practices and tools.
- The initiative should introduce reusable AI agents across requirements,
  design, development, testing, security, and release activities.
- Expected outcomes include improved delivery consistency, stronger
  traceability, reduced manual effort, and better governance.

Capture:
- Business problem and drivers
- Current-state challenges
- Stakeholders and decision roles
- In-scope and out-of-scope areas
- Target business outcomes
- Measurable success indicators
- Business requirements
- Assumptions, dependencies, constraints, and risks
- Governance and approval criteria
```

### Review guidance

The BRD should be reviewed by relevant business owners, product leadership, architecture, security,
governance and delivery stakeholders before it becomes the approved input to PRD creation.

The BRD should not contain detailed technical implementation decisions unless those decisions
represent confirmed business constraints. Its primary focus remains the business need, required
outcomes, stakeholder expectations and business boundaries.

### BRD-to-PRD hand-off

The BRD establishes the **business baseline**; the PRD translates that baseline into **product
behaviour and measurable product requirements**.

| The BRD provides | The PRD translates it into |
|---|---|
| Business problem and opportunity | Product users and personas |
| Business objectives and outcomes | Product capabilities and features |
| Stakeholders and decision owners | Functional requirements |
| Scope and exclusions | Non-functional requirements |
| Business requirements | Data and integration requirements |
| Success measures | Security and compliance requirements |
| Assumptions and constraints | Operational requirements |
| Dependencies and risks | Acceptance criteria and validation evidence |
| Governance and approval status | |

### Reference

* [BRD and PRD Builders | HVE Core](https://microsoft.github.io/hve-core/docs/agents/project-planning/brd-prd-builders)

Step-by-step: [4.2 Convert raw requirements into a BRD](/getting-started/brd).
