---
id: backlog-manager
title: A.4 Jira Backlog Manager
description: "Turns approved product requirements or epics into a structured delivery backlog."
sidebar_label: A.4 Jira Backlog Manager
---

:::note Section summary
Turns approved product requirements or epics into a structured delivery backlog.
:::

**Type:** Core · **Lifecycle group:** Design, backlog and spec · **Phase:** 5 Create backlog and specification · **Source:** HVE Core All extension (Jira Backlog Manager, ADO Backlog Manager)

The Jira Backlog Manager turns approved product requirements or epics into a structured delivery
backlog. It drafts epics, user stories and acceptance criteria and can help maintain relationships
and consistency across backlog items. The Product Owner or Business Analyst retains responsibility
for priority, scope, sequencing and acceptance intent.

| Use when | Approved inputs | Output | Human review |
|---|---|---|---|
| Backlog decomposition or maintenance is required. Optional for brownfield and modernisation increments where an approved backlog already exists. | Approved PRD, epics, story standards (`.github/templates/user-story-template.md`) and backlog context. | Draft epics, stories and backlog updates, created in Jira or Azure DevOps after review. | Product Owner or Business Analyst reviews priority, scope and acceptance criteria. **Gate:** backlog approval (PO). |

## Working pattern

1. **Discover** work items from the PRD and produce a plan: epics as parents, user stories as
   children, priority tags (P0, P1, P2) and domain tags, acceptance criteria on every story. No
   items are created yet.
2. **Review** the plan: dependency order, acceptance criteria, MVP boundary.
3. **Create** the approved items through the backlog platform's MCP server (`jira_create_issue`,
   `jira_update_issue` for Jira; the Azure DevOps MCP server or `az boards` for ADO), epics first,
   then linked stories.
4. **Assign** P0 items to the MVP sprint.

## Limitations and stop conditions

* Does not decide priority or scope; it proposes them for the Product Owner.
* Stops before creating items until the discovery plan is explicitly approved.
* Reports MCP tool failures and falls back to the CLI only when instructed.

Step-by-step: [4.5–4.6 Plan and create the backlog](/getting-started/backlog).
