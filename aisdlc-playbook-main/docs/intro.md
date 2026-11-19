---
id: intro
title: SCBX AI-First SDLC Playbook
description: "Overview and intended audience. Draft, October 2026."
slug: /
sidebar_position: 0
sidebar_label: About this playbook
---

:::note Section summary
Overview and intended audience. Draft, October 2026.
:::

This playbook helps product squads use **Agentic PDLC** in a consistent, practical and controlled way.
It is written for the people shaping products, translating needs into specifications, designing
solutions, building and testing software, deploying releases and operating services in production.

It is designed to answer straightforward questions:

| Question | Where to look |
|---|---|
| What is Agentic PDLC and what changes in the way the squad works? | [1. Introduction](/introduction/what-is-agentic-pdlc) |
| What steps should I follow to adopt Agentic PDLC as my primary delivery approach? | [2. Overview](/overview/end-to-end-flow), [4. Getting started](/getting-started/overview) |
| What delivery path applies to my increment? | [2.2 Identify the project type](/overview/project-types), [3. Project paths](/paths/overview) |
| Which lifecycle activities and agents are relevant for my project type? How do I adapt for Greenfield and Brownfield? | [2.4 Tailor lifecycle activities](/overview/tailoring), [2.5 Select relevant agents](/overview/select-agents) |
| What must be prepared, reviewed and approved? | [Human approval gates](/overview/end-to-end-flow#human-approval-gates), [Getting started](/getting-started/overview) |
| Who remains accountable for each decision and output? | [5. Product squad roles](/roles/squad-roles), [Agent catalogue](/agents/catalogue) |
| How does the squad demonstrate value and safe use? | [2.3 Baseline the current state](/overview/baseline), [Lifecycle tailoring controls](/overview/tailoring#mandatory-controls-remain-in-place) |

## How to read it

The playbook is interactive. Diagrams are clickable: select a stage, a gate or an agent in any
diagram to open the page that explains it. Start with the
[end-to-end flow](/overview/end-to-end-flow), then follow your project path.

```text
Introduction  →  Overview  →  Project paths  →  Getting started  →  Roles  →  Agent catalogue
 (why)           (lifecycle,   (greenfield,     (step-by-step        (who is     (operating
                  tailoring,    brownfield,      with the toolkit)    accountable) contracts)
                  agents)       modernisation)
```

## The toolkit

The agents, rules, templates, MCP servers and the standard repository structure that this playbook
refers to are packaged in the [AI-First SDLC Toolkit](/toolkit) (`ap2510-aisdlc/aisdlc-toolkit`).
The toolkit agents run in GitHub Copilot in VS Code and in Claude Code; the
[Claude Code page](/getting-started/claude-code) covers the second runtime.
Install it into a product repository before running the lifecycle.

## Contents

1. [Introduction to Agentic PDLC](/introduction/what-is-agentic-pdlc)
2. [Overview of Agentic PDLC](/overview/end-to-end-flow)
3. [How to execute in different project types](/paths/overview)
4. [Pilot pre-initiation and getting started](/getting-started/overview)
5. [Product squad roles and responsibilities](/roles/squad-roles)
6. Mobilising the squad *(later draft)*
7. Governance and controls *(later draft)*
8. Measurements *(later draft)*
9. Templates and reference *(later draft; current templates are in the [toolkit](/toolkit#templates))*

Appendix A. [Agent catalogue](/agents/catalogue)

This is a living document. Sections 6 to 9 are planned and will be added as the pilot squads
progress.
