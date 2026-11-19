---
id: project-types
title: 2.2 Identify the project type
description: "Greenfield, brownfield and modernisation paths."
sidebar_label: 2.2 Identify the project type
---

:::note Section summary
Greenfield, brownfield and modernisation paths.
:::

Project classification determines the starting context and the lifecycle emphasis:

* **Greenfield development** creates a new target solution.
* **Brownfield enhancement** changes an application that will be retained.
* **Modernisation** changes the technical shape of an existing application, such as its
  architecture, runtime or deployment model.
* **Integration or localisation** connects or adapts a reusable capability.

:::tip Classify the increment, not the programme
Classification should be applied to the **bounded increment** rather than the entire programme,
because one programme may contain several paths. See [3.5 Hybrid programmes](/paths/hybrid).
:::

## Classification questions

Before selecting agents, classify the project using the following questions. Record the answers in
the increment card (`.github/templates/increment-card-template.md` in the toolkit).

1. Is this a completely new capability?
2. Does a running application already exist?
3. Are business requirements documented and approved?
4. Is business logic embedded mainly in source code?
5. Is the goal enhancement, replacement, modernisation or technical upgrade?
6. Is the target technology already approved?
7. Is there a current architecture and dependency inventory?
8. Are user journeys and design-system standards available?
9. Is the change primarily integration or localisation?
10. Is a production-safe rollback path available?
11. Which lifecycle artefacts can be reused?
12. Which artefacts must be recovered or regenerated?

## Standard project types

| Path | Use when | Starting context | Primary focus |
|---|---|---|---|
| [Greenfield development](/paths/greenfield) | Create a new product, service, journey or application, including replacing a legacy solution with a newly built target state. | Business opportunity, user need or problem statement and, where applicable, legacy behaviour, rules, data and exception paths. | Shape outcomes → define product and target architecture → build and validate → transition from legacy where required. |
| [Brownfield enhancement](/paths/brownfield) | Retain the existing application and deliver a feature, regulatory change or increment. | Approved backlog, specification, design or code. | Reuse context → clarify change → implement. |
| [Modernisation and upgrade](/paths/modernisation) | Transform an existing application by modernising its architecture, technology stack, framework, runtime, database, infrastructure or deployment model. | Source code, application behaviour, architecture documentation, component inventory, dependency maps and compatibility information. | Understand the current state → assess dependencies and constraints → define the target architecture → modernise, migrate, upgrade and validate. |

Once the path is known, [baseline the current state](/overview/baseline) and
[tailor the lifecycle](/overview/tailoring).
