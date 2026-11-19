---
id: baseline
title: 2.3 Baseline the current state
description: "Baseline current state before introducing Agentic PDLC."
sidebar_label: 2.3 Baseline the current state
---

:::note Section summary
Baseline current state before introducing Agentic PDLC.
:::

Before introducing Agentic PDLC, establish a clear baseline of how the team delivers today. The
objective is not simply to document the formal SDLC, but to understand how work actually moves from
demand through requirements, design, build, test, release and operation, including the tools,
artefacts, hand-offs, approvals and workarounds used in practice.

## What the baseline should capture

| Area | What to understand |
|---|---|
| **Delivery approach** | Whether the team works through Agile, Waterfall or a hybrid approach; the ceremonies, stages and approval points used in practice; and how consistently the stated methodology is followed. |
| **Project and change types** | The types of work typically delivered, such as greenfield development, enhancements, regulatory changes, modernisation or integration, and their frequency and size. |
| **Current SDLC / PDLC** | How work flows today from idea or request through requirements, design, backlog, planning, implementation, testing, release and operations, including key hand-offs and dependencies. |
| **Roles and ways of working** | Who performs each activity, who reviews or approves it, where specialist input is required, and where work waits for another person or team. |
| **Tools and workflow** | The systems used to manage requirements, backlog, source code, testing, CI/CD, approvals and operational work, and how information moves between those tools. |
| **Documentation and source of truth** | Where requirements, decisions, designs, standards, user stories and technical documentation are maintained (Jira, Confluence, repositories or other systems), and whether teams consistently use the agreed source of truth. |
| **Existing artefacts and context** | What approved requirements, architecture, design, code, standards, templates, test assets and other reusable context already exist; who owns them; and whether they are current and usable. |
| **Pain points and constraints** | Where teams experience delays, rework, duplication, unclear requirements, fragmented context, manual effort, repeated hand-offs, quality issues or other delivery challenges. |
| **Team needs** | What teams need in order to deliver more effectively: better context, clearer specifications, improved tooling or integration, faster feedback, reduced manual work, or stronger review and governance support. |
| **Current performance** | What evidence is already available to establish the starting point for delivery performance, quality and flow so that future improvement can be measured rather than assumed. |

## Reflect practice, not documentation

The baseline should reflect the way delivery actually works today, not only how the process is
documented. Understand how work moves through the lifecycle in practice, where teams experience
delays, rework or dependency on manual hand-offs, and where the actual way of working differs from
the intended process.

Where data is available, complement this qualitative view with existing measures of delivery
performance, such as lead time, cycle time, quality, rework and other relevant flow measures. The
objective is not to introduce a new measurement framework, but to establish an evidence-based
starting point against which changes introduced through Agentic PDLC can be assessed.

## Output

A concise current-state baseline of the delivery flow, roles, tools, artefacts, pain points, needs
and available performance measures. It provides the reference point for identifying where agents
could add value, what context or documentation needs to be strengthened, which existing practices
should be retained, and how improvement will ultimately be demonstrated.

Use the toolkit template `.github/templates/squad-baseline-template.md` and store the result in
`docs/discovery/squad-baseline.md`.
