---
id: context-builder
title: A.2 Context Builder
description: "Creates the project context that every downstream agent reads."
sidebar_label: A.2 Context Builder
---

:::note Section summary
Creates the project context that every downstream agent reads.
:::

**Type:** Custom · **Lifecycle group:** Requirements and discovery · **Phase:** 2 Contextualise · **Toolkit file:** `.github/agents/context-builder.agent.md`

The Context Builder creates the project context needed to support downstream agent-enabled
delivery. It brings together available reference material, project documentation, source code,
configuration and tests, and supplements these with business, stakeholder, compliance and technical
context. For greenfield projects, it also prompts for the business overview and technology stack
where existing project material is not yet available.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| Creating comprehensive project context from scratch; starting a new project or onboarding an existing codebase; or establishing business, technical and standards documentation. | Confluence link where provided (through the `confluence` MCP server); otherwise attached Word or PDF documents; available legacy project documentation; source code, configuration and tests; business, client-domain, stakeholder and compliance information; and, for greenfield projects, technology stack and business overview. | Unified project context with `CTX-*` trace IDs; technology-specific standards based on best practices; and additional user-provided standards preserved and indexed under `.github/contexts/`. | Review the generated context for completeness and accuracy, confirm that the applicable project and standards material has been captured, and resolve material gaps before the context is used by downstream agents. **Gate:** context readiness (FDE). |

## Output files

```text
.github/contexts/project-context.md     business requirements, logic, rules, constraints, design intent, acceptance criteria
.github/contexts/domain-context.md      industry and domain references
.github/contexts/frontend-context.md    screens, themes, fonts, styles
.github/contexts/backend-context.md     APIs, data, integrations, operations
.github/contexts/testing-standards.md   testing and verification strategy, frameworks, coverage
requirement/Context_<ProjectName>.md    detailed context with CTX-* IDs
requirement/Traceability_Matrix.md      updated with CTX-* IDs
```

## Limitations and stop conditions

* Creates new context only. Maintenance is owned by the **Context Updater**; other agents must not
  modify context files.
* Stops and asks when the technology stack or business overview cannot be established from the
  supplied sources.
* Never includes real customer data, credentials or production data in the generated context.

Used in: [Greenfield](/paths/greenfield#2-contextualise), [Brownfield](/paths/brownfield),
[Modernisation](/paths/modernisation).
