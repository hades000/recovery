---
id: prd-builder
title: A.3.2 PRD Builder
description: "Defines what the product must do, how it should behave, which quality attributes it must satisfy and how completion will be verified."
sidebar_label: A.3.2 PRD Builder
---

:::note Section summary
Defines what the product must do, how it should behave, which quality attributes it must satisfy and how completion will be verified.
:::

**Type:** Core · **Lifecycle group:** Requirements and discovery · **Phase:** 3 Define requirements · **Source:** HVE Core All extension

## Purpose

The Product Requirements Document (PRD) Builder converts an approved business direction into
detailed, measurable and actionable product requirements. It should normally be used after the
relevant business objectives, scope and stakeholder outcomes have been established through an
approved [BRD](/agents/brd-builder) or equivalent business baseline.

## When to use

Use the PRD Builder when the team needs to:

* Define product users and personas.
* Describe product capabilities and features.
* Capture functional requirements.
* Define non-functional requirements.
* Establish measurable acceptance criteria.
* Document user journeys and product behaviours.
* Identify data and integration requirements.
* Define security, privacy, compliance and audit requirements.
* Capture performance, scalability, availability and resilience expectations.
* Define observability and operational requirements.
* Maintain traceability from business objectives to product requirements.

## PRD lifecycle

| Phase | What the agent does |
|---|---|
| **Assess** | Reviews the available context and determines whether sufficient information exists to start the PRD. |
| **Discover** | Establishes the product problem, intended users, expected capabilities, scope and boundaries. |
| **Create** | Creates the initial PRD structure and establishes the working document and session state. |
| **Build** | Progressively gathers and documents functional requirements, non-functional requirements, user journeys and interactions, business rules affecting product behaviour, acceptance criteria, error and exception scenarios, requirement priorities. |
| **Integrate** | Incorporates information from approved documents, reference material, existing systems, architecture context and other relevant sources. Conflicts and unsupported assumptions are highlighted for human resolution. |
| **Validate** | Reviews the PRD for completeness, clarity, consistency, traceability and testability. Ambiguous or non-measurable requirements are refined before finalisation. |
| **Finalise** | Prepares the completed PRD for review and hand-off to architecture, backlog management, development, testing, security, release and operational teams. |

## Typical inputs

Approved BRD, product vision and roadmap, user personas, user research, existing process flows,
architecture constraints, regulatory and security requirements, source-system and integration
details, existing backlog items, service-level objectives, operational and support requirements,
reference applications or existing codebase context.

## Expected outputs

Product overview and problem statement; product goals and non-goals; target users and personas;
product scope; features and capabilities; functional requirements; non-functional requirements;
user journeys or workflows; data and integration requirements; roles and access requirements;
security, privacy, compliance and audit requirements; performance, scalability, availability and
resilience requirements; observability and operational requirements; error and exception handling;
measurable acceptance criteria; dependencies, assumptions, constraints and risks; traceability to
BRD objectives and source evidence.

Written to `docs/prds/<prd_name>.md`.

## Example SCBx usage

```text
Create a PRD for an AI-assisted backlog and requirements-management
capability for the SCBx AI-enabled Product Development Lifecycle.

Target users:
- Product owners
- Business analysts
- Solution architects
- Developers
- Test engineers

Define requirements for:
- Importing an approved BRD
- Generating and refining epics, features, and user stories
- Maintaining traceability from business requirements to backlog items
- Generating measurable acceptance criteria
- Identifying ambiguity, conflicts, and missing information
- Requiring human review before backlog changes are published
- Integrating with the approved engineering toolchain
- Recording source references and change history

Include:
- Functional and non-functional requirements
- Roles and access boundaries
- Data and integration requirements
- Security, privacy, audit, and observability requirements
- Error and exception handling
- Acceptance criteria and validation evidence
```

## Review guidance

The PRD should be reviewed by product owners, business analysts, solution architects, engineering
leads, security stakeholders, test leads, operations teams and other relevant decision owners.

Each requirement should be:

* Clear and unambiguous
* Traceable to a business objective or approved need
* Testable through defined acceptance criteria
* Measurable where applicable
* Prioritised
* Supported by an identified owner or source
* Free from unsupported assumptions

The approved PRD becomes a key input to solution architecture, backlog creation, detailed design,
development, testing, security validation, deployment and product operations.

## Reference

* [BRD and PRD Builders | HVE Core](https://microsoft.github.io/hve-core/docs/agents/project-planning/brd-prd-builders)

Step-by-step: [4.4 Convert the approved BRD into a PRD](/getting-started/prd).
