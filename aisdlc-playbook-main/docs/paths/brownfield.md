---
id: brownfield
title: 3.3 Brownfield enhancement
description: "Brownfield lifecycle: start from the existing estate rather than from a blank page."
sidebar_label: 3.3 Brownfield enhancement
---

:::note Section summary
Brownfield lifecycle: start from the existing estate rather than from a blank page.
:::

Use the brownfield path when the application is retained and the increment changes existing
behaviour. The path starts from the existing estate rather than from a blank page. The first
priority is to understand the current code, architecture, interfaces, rules, dependencies,
incidents and technical debt that are relevant to the change.

Existing requirements, designs or backlog artefacts can be reused when they are current and
approved, but the squad must still clarify the change, assess impact, implement safely, test
affected behaviour and retain release evidence.

## What is optional, what is not

| Phase | Brownfield treatment |
|---|---|
| 1. Discover and frame | **Conditional.** Use when the enhancement is poorly defined, existing requirements conflict, the user problem is not validated, or a rebuild decision requires reframing. |
| 2. Contextualise | **Mandatory in practice.** The squad must understand the relevant code, architecture, interfaces, rules, dependencies, incidents and technical debt. The [Context Builder](/agents/context-builder) ingests existing project and application material. |
| 3. Define requirements | **Reusable.** Start from the existing approved requirement or change request. Clarify requirements and update acceptance criteria. BRD or PRD regeneration should not occur unless existing artefacts are incomplete or materially outdated. |
| 4. Design experience and architecture | Emphasise impact analysis, compatibility, existing architecture constraints, reuse of established components, and interface and regression risk. |
| 5. Create backlog and specification | **Reusable where sufficient.** Reuse the existing approved backlog and specifications; clarify or regenerate where the existing material cannot support implementation. [Spec-Clarify](/agents/spec-clarify) is applicable. |
| 6. Plan and decompose | Create a dependency-aware implementation plan for the approved change. |
| 7. Build | Implement the approved change within the defined scope and architecture. |
| 8. Validate | Demonstrate that the change meets approved requirements, including relevant integration and regression requirements. |
| 9. Release | Prepare and authorise the change for controlled release. |
| 10. Operate and improve | Monitor the changed application, feed production learning back into requirements and tests, and update relevant context. |

:::warning Reused artefacts must be versioned and linked
Any reused artefact must be versioned and linked to the increment. Record it in the increment card
and the lifecycle tailoring record, with the owner and the approving authority.
:::

## Agents

The [Brownfield and Modernisation agent table](/overview/select-agents#brownfield-and-modernisation)
shows BRD Builder, PRD Builder and Jira Backlog Manager as optional. The typical brownfield run is:

```text
Context Builder (existing code, architecture, incidents, technical debt)
→ Spec-Clarify (from the approved change request or Jira story)
→ Task-Planner → Task-Implementor → Code Review → API / Functional Testing → Azure-Deploy
```

The step-by-step execution starts at [Create the technical specification](/getting-started/specify)
once context is in place.
