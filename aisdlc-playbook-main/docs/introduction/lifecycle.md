---
id: lifecycle
title: 1.3 The AI PDLC lifecycle
description: "AI PDLC lifecycle framework: the agent chain from business requirements to deployment."
sidebar_label: 1.3 The AI PDLC lifecycle
---

:::note Section summary
AI PDLC lifecycle framework: the agent chain from business requirements to deployment.
:::

The AI PDLC lifecycle connects the agents used from business requirements through deployment to
Azure. Each step produces or develops an artefact that becomes an input to subsequent activities,
with human approval of generated artefacts across the lifecycle.

<object type="image/svg+xml" data="/diagrams/agent-chain.svg" className="diagram" aria-label="The agent chain from Context Builder to Azure Deploy, with the human reviewer for each step">
  The agent chain: Context Builder, BRD Builder, PRD Builder, ADR Creation, Backlog Manager, Spec-Clarify, Task Planner, Task Implementor, API and Functional Testing, Azure Deploy.
</object>
Click an agent to open its catalogue entry. [draw.io source](/diagrams/agent-chain.drawio)

| Step | Agent / capability | Activity / output |
|---|---|---|
| 1. Context Builder | [`context-builder`](/agents/context-builder) | Capture context from Confluence and project sources to contextualise agents. |
| 2. Business Requirements | [`brd-builder`](/agents/brd-builder) | Business requirements creation. |
| 3. Product Requirements | [`prd-builder`](/agents/prd-builder) | Create the PRD from discoveries. |
| 4. Architecture | `adr-creation` and `arch-diagram-builder` | Record key architecture decisions and diagrams. |
| 5. Backlog Manager | [`backlog-manager`](/agents/backlog-manager) | Create the user-story backlog. |
| 6. Spec, Clarify | [`spec-clarify`](/agents/spec-clarify) | The specification becomes the source for implementation and is built using project or domain knowledge in the context. Clarify ambiguities and unknowns in the story with the BA. |
| 7. Plan and Task | [`task-planner`](/agents/task-planner) | Plan and create implementation tasks using the context. |
| 8. Implementation and Unit Test | [`task-implementor`](/agents/task-implementor) | Execute plans with validation. |
| 9. Deploy | [Azure deployment pipeline](/agents/azure-deploy) | `azure-prepare` → `azure-validate` → `azure-deploy`. |

## Lifecycle flow

```text
Context Builder → BRD Builder → PRD Builder → ADR Creation → Backlog Manager
→ Spec, Clarify → Task Planner → Task Implementor & Unit Test → Azure Deploy
```

The lifecycle progressively moves from **context**, to **product requirements and architecture
decisions**, through **backlog creation, specification, implementation planning, implementation,
review and validation**, and finally **deployment to Azure**.

Human-in-the-loop approval remains part of the lifecycle. Generated artefacts are reviewed and
approved at defined points before work progresses to subsequent stages. This allows agents to
support and execute work across the lifecycle while people retain approval over key outputs and
progression. The full set of gates is listed in
[Human approval gates](/overview/end-to-end-flow#human-approval-gates).
