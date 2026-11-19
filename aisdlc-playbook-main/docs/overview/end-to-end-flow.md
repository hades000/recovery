---
id: end-to-end-flow
title: 2.1 End-to-end flow
description: "End-to-end flow and human approvals."
sidebar_label: 2.1 End-to-end flow
---

:::note Section summary
End-to-end flow and human approvals.
:::

Agentic PDLC uses the same governed end-to-end workflow for greenfield and brownfield delivery,
moving from enterprise context through specification, planning, implementation and validation to
production and ongoing learning. The lifecycle combines continuous validation with human approval
gates at defined points.

<object type="image/svg+xml" data="/diagrams/end-to-end-flow.svg" className="diagram" aria-label="The end-to-end flow: nine stages from Discover and Context to Operate and Learn, with the human approval gate after each stage and the agents that support it">
  Nine stages: Discover / Context, Specify, Plan, Tasks, Implement, Test and Validate, Build / Ship, GreenLane CI/CD, Operate and Learn. Each is followed by a human approval gate.
</object>
Click a stage, a gate or an agent to open its explanation. [draw.io source](/diagrams/end-to-end-flow.drawio)

Greenfield and brownfield delivery follow the same workflow but draw on different context.
Requirements context and design context provide inputs to the lifecycle, while brownfield delivery
also incorporates relevant existing code, architecture, dependencies, incidents and technical debt.

## Stages

### Discover / Context

Assemble the context required as input to the PDLC: requirements context such as PRDs, FRDs, user
stories, change requests, bugs and business rules; design context such as Figma files, design
systems, UI patterns and components; and, for brownfield delivery, existing code, architecture,
dependencies, incidents and technical debt.

**Typical output:** requirements context, design context and brownfield context
(`.github/contexts/`, `docs/brds/`, `docs/prds/`).

### Specify

Convert requirements and context into a clear technical specification.

**Typical output:** `spec.md` and acceptance criteria (`output/<RUN_ID>/specify/`).

### Plan

Define the solution approach, architecture impact and high-level design.

**Typical output:** `plan.md`, architecture and impact analysis (`output/<RUN_ID>/plan/`).

### Tasks

Break the solution down into dependent, actionable development tasks.

**Typical output:** `tasks.md` and task dependencies.

### Implement

Develop code according to the defined tasks, with guardrails and real-time feedback.

**Typical output:** source code and unit tests, with implementation evidence under
`output/<RUN_ID>/implement/`.

### Test and Validate

Conduct continuous testing in parallel with implementation.

**Typical output:** test results and quality and security evidence
(`output/<RUN_ID>/api-tests/`, `output/<RUN_ID>/functional-tests/`, review findings).

### Build / Ship

Create a releasable build after all required quality gates have passed.

**Typical output:** release candidate and build artefacts.

### GreenLane CI/CD

Automate promotion through environments from DEV → SIT → QA → PROD.

**Typical output:** deployed version and deployment logs.

### Operate and Learn

Monitor production, learn from operational outcomes and feed insights back into context,
particularly for brownfield delivery.

**Typical output:** operational insights and improvement recommendations, fed back into
`.github/contexts/` by the Context Updater.

## Human approval gates

Human oversight is maintained through approval gates across the lifecycle. Agents produce; named
roles approve.

| After | Gate | Accountable role |
|---|---|---|
| Specify | Specification approval | Product Owner |
| Plan | Plan approval | Forward Deployed Architect (FDA) |
| Tasks | Task approval | Forward Deployed Engineer (FDE) |
| Implement | Code review | Forward Deployed Engineer (FDE) |
| Test and Validate | Quality and security gate | Forward Deployed Architect (FDA) |
| Build / Ship | Release readiness | Forward Deployed Engineer (FDE) |
| GreenLane CI/CD | Deployment approval | Product Owner / Project Manager |
| Operate and Learn | Ongoing review | Ops / System Manager |

:::warning Rule
No implementation begins until the approved plan satisfies the planning gate, and no autonomous production promotion is permitted.
:::

## Continuous validation

Validation is continuous across the flow. Code changes trigger tests, test feedback guides fixes
during implementation, and production learning feeds back into brownfield context for continuous
improvement. In the toolkit the Technical Specifier, Implementation Planner and Technical Documenter
each invoke the **Compliance Reviewer** at their gate before handing off; see
[Supporting agents](/agents/supporting-agents#compliance-reviewer).

Next: [2.2 Identify the project type](/overview/project-types).
