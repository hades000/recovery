---
id: tailoring
title: 2.4 Tailor lifecycle activities
description: "Apply lifecycle tailoring rules to determine which activities are mandatory, conditional, reusable, skippable with evidence or not applicable for the bounded increment."
sidebar_label: 2.4 Tailor lifecycle activities
---

:::note Section summary
Apply lifecycle tailoring rules to determine which activities are mandatory, conditional, reusable, skippable with evidence or not applicable for the bounded increment.
:::

The SCB Agentic PDLC provides a standard end-to-end lifecycle, but not every project needs to
execute every activity in the same way. For each phase, the squad determines whether the activity is
**mandatory, conditional, reusable, skippable with evidence or not applicable** for the bounded
increment.

The decision should reflect the project type, lifecycle entry point, approved artefacts already
available and the specific requirements of the increment. Existing approved work should be reused
where appropriate rather than recreated unnecessarily.

<object type="image/svg+xml" data="/diagrams/lifecycle-paths.svg" className="diagram" aria-label="The eleven-phase standard lifecycle with one row per project path showing which phases are mandatory, conditional or reusable">
  The standard lifecycle phases 0 to 10 with Greenfield, Brownfield and Modernisation rows.
</object>
Click a phase for its tailoring guidance, or a path for its execution page. [draw.io source](/diagrams/lifecycle-paths.drawio)

## Lifecycle tailoring rules

| Classification | Application |
|---|---|
| **Mandatory** | The activity is required for the bounded increment. |
| **Conditional** | The activity is required when the conditions relevant to that phase or project are present. |
| **Reusable** | Existing approved artefacts or outputs can be used as inputs rather than recreated. |
| **Skippable with evidence** | The activity can be bypassed where sufficient approved evidence already exists and the decision is recorded. |
| **Not applicable** | The activity does not apply to the bounded increment. |

### Recording a skip

Where a phase or activity is skipped, record:

* Reason for skipping
* Existing approved artefact
* Artefact owner
* Version or link
* Approving authority
* Risk created by the bypass
* Controls applied downstream

The toolkit template `.github/templates/lifecycle-tailoring-record.md` captures these fields for
every phase.

## Standard lifecycle

Lifecycle tailoring is applied against the standard SCB Agentic PDLC:

0. Mobilise and assess
1. Discover and frame
2. Contextualise
3. Define requirements
4. Design experience and architecture
5. Create backlog and specification
6. Plan and decompose
7. Build
8. Validate
9. Release
10. Operate and improve

For each lifecycle phase, the playbook defines: purpose; when the phase is mandatory; entry criteria;
required inputs; applicable agents; required context; human activities; expected outputs; quality
checks; approval authority; exit criteria; traceability requirements; applicable project types;
metrics; and stop and rollback signals. The project-path pages
([greenfield](/paths/greenfield), [brownfield](/paths/brownfield),
[modernisation](/paths/modernisation)) describe each phase for that path.

## Tailoring by project type

Project type informs how the lifecycle is applied, particularly in the earlier phases where existing
context and artefacts may already be available.

### 0. Mobilise and assess

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Select an appropriate project and bounded delivery increment before activating agents. | Select the bounded change and assess the existing project, artefacts, environment and readiness. | Select the bounded modernisation increment and assess the existing application and environment. |

### 1. Discover and frame

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| **Mandatory for net-new products and journeys.** Define the customer or employee problem, personas, desired outcomes, journey, value hypothesis, business constraints and policy or regulatory requirements. | Use when the enhancement is poorly defined, existing requirements conflict, the user problem is not validated, or a rebuild decision requires reframing. | Apply where the underlying problem or desired outcome requires reframing before modernisation proceeds. |

### 2. Contextualise

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Establish the approved enterprise, domain, project and engineering context required by the agents. | Establish the approved context package, including relevant existing requirements, architecture, APIs, dependencies, code and decisions. | Establish the approved current-state context needed to understand the application, architecture, dependencies and engineering environment. |

### 3. Define requirements

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Use approved discovery outputs to develop the BRD and PRD, followed by business, product and architecture approval. | Start from the existing approved requirement or change request. Clarify requirements and update acceptance criteria. **BRD or PRD regeneration should not occur unless existing artefacts are incomplete or materially outdated.** | Analyse the source, obtain SME verification, then develop the BRD and PRD and obtain architecture approval. |

### 4. Design experience and architecture

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Emphasise journey and interaction design, design-system compliance, target architecture, API and event contracts, data design, security and observability by design. | Emphasise impact analysis, compatibility, existing architecture constraints, reuse of established components, and interface and regression risk. | Emphasise current-to-target mapping, coexistence strategy, data migration, strangler or phased replacement patterns, decommissioning, rollback and feature-control strategy. |

### 5. Create backlog and specification

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Transform approved requirements and designs into implementable and traceable work. | Reuse existing approved backlog and specifications where sufficient; clarify or regenerate where the existing material cannot support implementation. | Create the backlog and specification required to deliver the approved modernisation approach. |

### 6. Plan and decompose

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Create a dependency-aware implementation plan for the approved specification. | Create a dependency-aware implementation plan for the approved change. | Plan implementation of the modernisation or migration increment, including coexistence and cut-over steps. |

### 7. Build

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Implement the bounded increment against the approved plan and specification. | Implement the approved change within the defined scope and architecture. | Implement the approved modernisation or migration increment within the defined scope. |

### 8. Validate

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Demonstrate that the increment meets approved business, technical, security and operational requirements. | Demonstrate that the change meets approved requirements, including relevant integration and regression requirements. | Validate the modernised solution against the approved requirements and target state. |

### 9. Release

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Prepare and authorise a controlled release. | Prepare and authorise the change for controlled release. | Prepare and authorise the modernised increment for controlled release, including the required rollback approach. |

### 10. Operate and improve

| Greenfield | Brownfield | Modernisation |
|---|---|---|
| Monitor operational outcomes and continuously improve the product, context packages and agent chain. | Monitor the changed application, feed production learning back into requirements and tests, and update relevant context. | Monitor the modernised environment and use operational learning to improve the product, context and subsequent modernisation increments. |

## Mandatory controls remain in place

Lifecycle tailoring changes **how the lifecycle is traversed**, not the requirement for evidence and
accountability.

Where existing artefacts are reused, the squad should establish that the artefact is appropriate
for the increment rather than regenerating it automatically. Where an activity is skipped, the
reason, supporting evidence, ownership, approval, resulting risk and downstream controls must be
recorded.

Human approval gates continue to apply where required. Across the lifecycle these include:

* intake approval
* context readiness
* requirements approval
* design and architecture approval
* backlog and specification approval
* plan approval
* pull request approval
* quality approval
* production readiness

:::warning Rule
No implementation should begin until the approved plan satisfies the required planning gate, and no autonomous production promotion is permitted.
:::

Next: [2.5 Select relevant agents](/overview/select-agents).
