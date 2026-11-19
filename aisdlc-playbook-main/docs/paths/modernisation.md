---
id: modernisation
title: 3.4 Modernisation and upgrade
description: "Modernisation path: brownfield understanding combined with a new target-state design."
sidebar_label: 3.4 Modernisation and upgrade
---

:::note Section summary
Modernisation path: brownfield understanding combined with a new target-state design.
:::

Modernisation begins with the existing estate but aims to change its technical shape. The path
therefore combines brownfield understanding with a new target-state design. The squad documents
current behaviour and dependencies, defines the target architecture and migration approach,
divides the change into bounded increments and validates both functional equivalence and the
intended technical improvement.

Compatibility, rollback and operational readiness are central because the change affects the
platform or architecture on which existing behaviour depends.

## Phase emphasis

| Phase | Modernisation treatment |
|---|---|
| 0. Mobilise and assess | Select the bounded modernisation increment and assess the existing application and environment. |
| 1. Discover and frame | Apply where the underlying problem or desired outcome requires reframing before modernisation proceeds. |
| 2. Contextualise | Establish the approved current-state context needed to understand the application, architecture, dependencies and engineering environment. |
| 3. Define requirements | Analyse the source, obtain SME verification, then develop the BRD and PRD and obtain architecture approval. |
| 4. Design experience and architecture | Emphasise current-to-target mapping, coexistence strategy, data migration, strangler or phased replacement patterns, decommissioning, rollback and feature-control strategy. |
| 5. Create backlog and specification | Create the backlog and specification required to deliver the approved modernisation approach. |
| 6. Plan and decompose | Plan implementation of the modernisation or migration increment, including coexistence and cut-over steps. |
| 7. Build | Implement the approved modernisation or migration increment within the defined scope. |
| 8. Validate | Validate the modernised solution against the approved requirements and target state: functional equivalence **and** the intended technical improvement. |
| 9. Release | Prepare and authorise the modernised increment for controlled release, including the required rollback approach. |
| 10. Operate and improve | Monitor the modernised environment and use operational learning to improve the product, context and subsequent modernisation increments. |

## Starting context

Source code, application behaviour, architecture documentation, component inventory, dependency
maps and compatibility information. The [Context Builder](/agents/context-builder) extracts the
technology stack and architecture from the codebase; SMEs verify business logic that is embedded
mainly in source code before requirements are regenerated.

## Agents

The same capability set as brownfield applies (see
[Brownfield and Modernisation agents](/overview/select-agents#brownfield-and-modernisation)).
Because the target state is new, BRD and PRD are usually regenerated after source analysis, and
architecture decisions (ADRs) are mandatory for the current-to-target mapping.
