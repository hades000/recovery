---
id: backlog
title: 4.5–4.6 Plan and create the backlog
description: "Backlog Manager: discover work items from the PRD, review the plan, then create epics and stories."
sidebar_label: 4.5–4.6 Backlog
---

## 4.5 Plan the implementation backlog

:::note Section summary
Backlog Manager: discover work items from the PRD, review the plan, then create epics and stories.
:::

**Lifecycle phase:** 5 Create backlog and specification · **Agent:** [Jira / ADO Backlog Manager](/agents/backlog-manager) (HVE Core) · **Gate:** backlog approval (Product Owner)

:::warning Context reset
Start a new chat session before invoking the next task agent.
:::

### Invoke the Backlog Manager agent

Add the following context documents to the chat:

```text
docs/prds/<your-prd>.md
.copilot-tracking/research/<date>/<research_file_name>.md
```

Use the following prompt (shown for Azure DevOps; use the Jira Backlog Manager and Jira issue
types for Jira projects):

```text
Discover work items from the attached PRD. Plan an Azure DevOps backlog for the <project> project.

Use the research findings and architecture decisions to inform the work-item structure. Plan epics
as parent work items and user stories as child work items.

Use the "Epic" work-item type for epics and the "User Story" work-item type for user stories. Also
plan priority tags (P0-must-have, P1-should-have, P2-future) and domain tags (billing-agent,
technical-agent, general-agent, infrastructure, observability).

Each work item must include acceptance criteria.

Focus on P0 items first. These form the MVP sprint.

Important: Do not create work items in Azure DevOps yet. Only produce the discovery plan so that it
can be reviewed first. Tag all MVP stories with "P0-must-have" so that they can be implemented for
the initial MVP.
```

### Review the plan

Ensure that the plan places items in dependency order:

1. Create all epics.
2. Create issues under their planned parent epics.
3. Create tasks only when explicitly included in the plan, linking each task to its planned parent
   issue.

The Product Owner or Business Analyst retains responsibility for priority, scope, sequencing and
acceptance intent.

## 4.6 Create the approved work items

:::warning Context reset
Start a new chat session before invoking the next task agent.
:::

### Invoke the Backlog Manager agent

Add the plan documents from the previous step to the chat context. Use the following prompt:

```text
The discovery plan looks good. Now create all the planned work items in Azure DevOps.

Prefer the Azure DevOps MCP server tools to create the epics and user stories with their tags. If
the Azure DevOps MCP server is not available or any MCP tool call fails, fall back to the `az
boards` CLI to create work items instead.

Create epics first, then create user stories as child work items linked to their parent epics.
Apply the priority and domain tags to each work item.
```

For Jira projects the toolkit's `jira` MCP server provides `jira_create_issue`,
`jira_update_issue` and `jira_get_create_metadata`; see the [toolkit MCP servers](/toolkit#mcp-servers).

### Verify

After execution, verify that:

* [ ] all planned epics, user stories and work items have been created;
* [ ] the acceptance criteria are present in the user stories; and
* [ ] each user story is linked to its parent epic.

### Create the sprint

Create the iteration or sprint. Then use the Backlog Manager agent with the following prompt:

```text
Assign all work items tagged "P0-must-have" to the "MVP - Sprint 1" iteration.
```

The resulting sprint backlog can then be used for sprint planning.

Next: [4.7 Create the technical specification](/getting-started/specify).
