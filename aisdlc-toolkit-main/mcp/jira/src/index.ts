#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { JiraClient, loadConfig } from "./client.js";

const API = "/rest/api/2";
const SUMMARY_FIELDS = [
  "summary", "status", "issuetype", "priority", "assignee", "reporter",
  "labels", "components", "fixVersions", "parent", "created", "updated", "duedate",
];

let client: JiraClient | undefined;
function jira(): JiraClient {
  return (client ??= new JiraClient(loadConfig()));
}

async function run(fn: () => Promise<unknown>) {
  try {
    const data = await fn();
    return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
  } catch (e) {
    return { isError: true, content: [{ type: "text" as const, text: e instanceof Error ? e.message : String(e) }] };
  }
}

function user(u: any) {
  if (!u) return null;
  return { displayName: u.displayName, id: u.accountId ?? u.name, email: u.emailAddress };
}

function summarizeIssue(issue: any, extraFields: string[] = []) {
  const f = issue.fields ?? {};
  const out: Record<string, unknown> = {
    key: issue.key,
    url: jira().issueUrl(issue.key),
    summary: f.summary,
    status: f.status?.name,
    issueType: f.issuetype?.name,
    priority: f.priority?.name,
    assignee: user(f.assignee),
    reporter: user(f.reporter),
    labels: f.labels,
    components: f.components?.map((c: any) => c.name),
    fixVersions: f.fixVersions?.map((v: any) => v.name),
    parent: f.parent?.key,
    created: f.created,
    updated: f.updated,
    dueDate: f.duedate,
  };
  if ("description" in f) out.description = f.description;
  for (const name of extraFields) out[name] = f[name];
  return out;
}

const server = new McpServer({ name: "jira", version: "1.0.0" });

server.registerTool(
  "jira_search_issues",
  {
    title: "Search Jira issues",
    description:
      "Search Jira issues with JQL, e.g. 'project = ABC AND status = \"In Progress\" ORDER BY updated DESC' or " +
      "'assignee = currentUser() AND resolution = Unresolved'. Returns a compact summary per issue.",
    inputSchema: {
      jql: z.string().describe("JQL query"),
      maxResults: z.number().int().min(1).max(100).default(25),
      extraFields: z.array(z.string()).optional().describe("Additional field IDs to return, e.g. ['description','customfield_10016']"),
      nextPageToken: z.string().optional().describe("Jira Cloud pagination token from a previous result"),
      startAt: z.number().int().min(0).optional().describe("Jira Server/DC pagination offset"),
    },
    annotations: { readOnlyHint: true },
  },
  ({ jql, maxResults, extraFields = [], nextPageToken, startAt }) =>
    run(async () => {
      const fields = [...SUMMARY_FIELDS, ...extraFields].join(",");
      if (jira().config.isCloud) {
        const res = await jira().request("GET", `${API}/search/jql`, { query: { jql, maxResults, fields, nextPageToken } });
        return { issues: res.issues.map((i: any) => summarizeIssue(i, extraFields)), nextPageToken: res.nextPageToken ?? null };
      }
      const res = await jira().request("GET", `${API}/search`, { query: { jql, maxResults, fields, startAt } });
      return {
        total: res.total,
        startAt: res.startAt,
        issues: res.issues.map((i: any) => summarizeIssue(i, extraFields)),
      };
    }),
);

server.registerTool(
  "jira_get_issue",
  {
    title: "Get Jira issue",
    description: "Get a Jira issue by key (e.g. ABC-123) including description, subtasks, links and comments.",
    inputSchema: {
      issueKey: z.string().describe("Issue key, e.g. ABC-123"),
      includeComments: z.boolean().default(true),
      extraFields: z.array(z.string()).optional().describe("Additional field IDs to return, e.g. ['customfield_10016']"),
    },
    annotations: { readOnlyHint: true },
  },
  ({ issueKey, includeComments, extraFields = [] }) =>
    run(async () => {
      const fields = [...SUMMARY_FIELDS, "description", "subtasks", "issuelinks", ...(includeComments ? ["comment"] : []), ...extraFields];
      const issue = await jira().request("GET", `${API}/issue/${encodeURIComponent(issueKey)}`, { query: { fields: fields.join(",") } });
      const f = issue.fields ?? {};
      return {
        ...summarizeIssue(issue, extraFields),
        subtasks: f.subtasks?.map((s: any) => ({ key: s.key, summary: s.fields?.summary, status: s.fields?.status?.name })),
        links: f.issuelinks?.map((l: any) => {
          const other = l.outwardIssue ?? l.inwardIssue;
          return { type: l.outwardIssue ? l.type?.outward : l.type?.inward, key: other?.key, summary: other?.fields?.summary };
        }),
        comments: includeComments
          ? f.comment?.comments?.map((c: any) => ({ id: c.id, author: user(c.author)?.displayName, created: c.created, body: c.body }))
          : undefined,
      };
    }),
);

server.registerTool(
  "jira_create_issue",
  {
    title: "Create Jira issue",
    description:
      "Create a Jira issue. Description uses Jira wiki markup (h2. Heading, *bold*, # numbered, * bullet, {code}...{code}). " +
      "Use jira_get_create_metadata first if unsure which fields are required.",
    inputSchema: {
      projectKey: z.string().describe("Project key, e.g. ABC"),
      issueType: z.string().describe("Issue type name, e.g. Story, Task, Bug, Epic, Sub-task"),
      summary: z.string(),
      description: z.string().optional(),
      priority: z.string().optional().describe("Priority name, e.g. High"),
      labels: z.array(z.string()).optional(),
      components: z.array(z.string()).optional().describe("Component names"),
      assignee: z.string().optional().describe("Cloud: accountId; Server/DC: username. Use jira_search_users to look up."),
      parentKey: z.string().optional().describe("Parent issue key (for sub-tasks, or epic parent on Cloud)"),
      dueDate: z.string().optional().describe("YYYY-MM-DD"),
      customFields: z.record(z.string(), z.any()).optional().describe("Raw field values keyed by field ID, e.g. {\"customfield_10016\": 5}"),
    },
  },
  (a) =>
    run(async () => {
      const fields: Record<string, unknown> = {
        project: { key: a.projectKey },
        issuetype: { name: a.issueType },
        summary: a.summary,
        ...(a.description !== undefined && { description: a.description }),
        ...(a.priority && { priority: { name: a.priority } }),
        ...(a.labels && { labels: a.labels }),
        ...(a.components && { components: a.components.map((name) => ({ name })) }),
        ...(a.assignee && { assignee: jira().userRef(a.assignee) }),
        ...(a.parentKey && { parent: { key: a.parentKey } }),
        ...(a.dueDate && { duedate: a.dueDate }),
        ...a.customFields,
      };
      const res = await jira().request("POST", `${API}/issue`, { body: { fields } });
      return { key: res.key, id: res.id, url: jira().issueUrl(res.key) };
    }),
);

server.registerTool(
  "jira_update_issue",
  {
    title: "Update Jira issue",
    description:
      "Update fields on an existing Jira issue. Only provided fields are changed. Description uses Jira wiki markup. " +
      "To change status use jira_transition_issue.",
    inputSchema: {
      issueKey: z.string(),
      summary: z.string().optional(),
      description: z.string().optional(),
      priority: z.string().optional(),
      labels: z.array(z.string()).optional().describe("Replace all labels"),
      addLabels: z.array(z.string()).optional(),
      removeLabels: z.array(z.string()).optional(),
      components: z.array(z.string()).optional().describe("Replace all components (names)"),
      assignee: z.string().nullable().optional().describe("Cloud: accountId; Server/DC: username; null to unassign"),
      dueDate: z.string().optional().describe("YYYY-MM-DD"),
      customFields: z.record(z.string(), z.any()).optional().describe("Raw field values keyed by field ID"),
    },
  },
  (a) =>
    run(async () => {
      const key = encodeURIComponent(a.issueKey);
      const fields: Record<string, unknown> = {
        ...(a.summary !== undefined && { summary: a.summary }),
        ...(a.description !== undefined && { description: a.description }),
        ...(a.priority && { priority: { name: a.priority } }),
        ...(a.labels && { labels: a.labels }),
        ...(a.components && { components: a.components.map((name) => ({ name })) }),
        ...(a.dueDate && { duedate: a.dueDate }),
        ...a.customFields,
      };
      const labelOps = [...(a.addLabels ?? []).map((l) => ({ add: l })), ...(a.removeLabels ?? []).map((l) => ({ remove: l }))];
      const body: Record<string, unknown> = {};
      if (Object.keys(fields).length) body.fields = fields;
      if (labelOps.length) body.update = { labels: labelOps };
      if (!Object.keys(body).length && a.assignee === undefined) throw new Error("Nothing to update");

      if (Object.keys(body).length) await jira().request("PUT", `${API}/issue/${key}`, { body });
      if (a.assignee !== undefined) await jira().request("PUT", `${API}/issue/${key}/assignee`, { body: jira().userRef(a.assignee) });

      return { key: a.issueKey, url: jira().issueUrl(a.issueKey), updated: true };
    }),
);

server.registerTool(
  "jira_add_comment",
  {
    title: "Add Jira comment",
    description: "Add a comment to a Jira issue. Body uses Jira wiki markup.",
    inputSchema: { issueKey: z.string(), body: z.string() },
  },
  ({ issueKey, body }) =>
    run(async () => {
      const res = await jira().request("POST", `${API}/issue/${encodeURIComponent(issueKey)}/comment`, { body: { body } });
      return { id: res.id, issueKey, created: res.created };
    }),
);

server.registerTool(
  "jira_get_transitions",
  {
    title: "List Jira transitions",
    description: "List workflow transitions currently available for an issue (use with jira_transition_issue).",
    inputSchema: { issueKey: z.string() },
    annotations: { readOnlyHint: true },
  },
  ({ issueKey }) =>
    run(async () => {
      const res = await jira().request("GET", `${API}/issue/${encodeURIComponent(issueKey)}/transitions`);
      return res.transitions.map((t: any) => ({ id: t.id, name: t.name, toStatus: t.to?.name }));
    }),
);

server.registerTool(
  "jira_transition_issue",
  {
    title: "Transition Jira issue",
    description: "Move an issue through its workflow (change status). Accepts a transition ID or name, or the target status name.",
    inputSchema: {
      issueKey: z.string(),
      transition: z.string().describe("Transition ID, transition name, or target status name (e.g. 'In Progress', 'Done')"),
      comment: z.string().optional(),
      fields: z.record(z.string(), z.any()).optional().describe("Fields required by the transition screen, e.g. {\"resolution\": {\"name\": \"Done\"}}"),
    },
  },
  ({ issueKey, transition, comment, fields }) =>
    run(async () => {
      const key = encodeURIComponent(issueKey);
      const { transitions } = await jira().request("GET", `${API}/issue/${key}/transitions`);
      const wanted = transition.toLowerCase();
      const match =
        transitions.find((t: any) => t.id === transition) ??
        transitions.find((t: any) => t.name?.toLowerCase() === wanted) ??
        transitions.find((t: any) => t.to?.name?.toLowerCase() === wanted);
      if (!match) {
        throw new Error(`Transition '${transition}' not available. Options: ${transitions.map((t: any) => `${t.id}:${t.name} -> ${t.to?.name}`).join(", ")}`);
      }
      await jira().request("POST", `${API}/issue/${key}/transitions`, {
        body: {
          transition: { id: match.id },
          ...(fields && { fields }),
          ...(comment && { update: { comment: [{ add: { body: comment } }] } }),
        },
      });
      return { key: issueKey, transition: match.name, newStatus: match.to?.name };
    }),
);

server.registerTool(
  "jira_list_projects",
  {
    title: "List Jira projects",
    description: "List Jira projects visible to the user, optionally filtered by name/key.",
    inputSchema: { query: z.string().optional().describe("Filter by project name or key") },
    annotations: { readOnlyHint: true },
  },
  ({ query }) =>
    run(async () => {
      let projects: any[];
      if (jira().config.isCloud) {
        projects = (await jira().request("GET", `${API}/project/search`, { query: { query, maxResults: 100 } })).values;
      } else {
        const q = query?.toLowerCase();
        projects = (await jira().request<any[]>("GET", `${API}/project`)).filter(
          (p) => !q || p.key.toLowerCase().includes(q) || p.name.toLowerCase().includes(q),
        );
      }
      return projects.map((p) => ({ key: p.key, name: p.name, id: p.id, type: p.projectTypeKey }));
    }),
);

server.registerTool(
  "jira_get_create_metadata",
  {
    title: "Get Jira create metadata",
    description:
      "Without issueType: list issue types for a project. With issueType: list fields for creating that type " +
      "(field IDs, required flag, allowed values).",
    inputSchema: {
      projectKey: z.string(),
      issueType: z.string().optional().describe("Issue type name or ID"),
    },
    annotations: { readOnlyHint: true },
  },
  ({ projectKey, issueType }) =>
    run(async () => {
      const base = `${API}/issue/createmeta/${encodeURIComponent(projectKey)}/issuetypes`;
      const typesRes = await jira().request("GET", base, { query: { maxResults: 200 } });
      const types: any[] = typesRes.issueTypes ?? typesRes.values ?? [];
      if (!issueType) return types.map((t) => ({ id: t.id, name: t.name, subtask: t.subtask }));

      const type = types.find((t) => t.id === issueType || t.name.toLowerCase() === issueType.toLowerCase());
      if (!type) throw new Error(`Issue type '${issueType}' not found. Options: ${types.map((t) => t.name).join(", ")}`);

      const fieldsRes = await jira().request("GET", `${base}/${type.id}`, { query: { maxResults: 200 } });
      const fields: any[] = fieldsRes.fields ?? fieldsRes.values ?? [];
      return fields.map((f) => ({
        fieldId: f.fieldId ?? f.key,
        name: f.name,
        required: f.required,
        type: f.schema?.type,
        allowedValues: f.allowedValues?.slice(0, 50).map((v: any) => v.name ?? v.value ?? v.key ?? v.id),
      }));
    }),
);

server.registerTool(
  "jira_search_users",
  {
    title: "Search Jira users",
    description: "Find users by name or email. Returns the ID to use for assignee (accountId on Cloud, username on Server/DC).",
    inputSchema: { query: z.string() },
    annotations: { readOnlyHint: true },
  },
  ({ query }) =>
    run(async () => {
      const q = jira().config.isCloud ? { query } : { username: query };
      const users = await jira().request<any[]>("GET", `${API}/user/search`, { query: { ...q, maxResults: 20 } });
      return users.map(user);
    }),
);

server.registerTool(
  "jira_get_link_types",
  {
    title: "List Jira issue link types",
    description:
      "List the issue link types configured in Jira (for example Tests, Blocks, Relates) with their inward and " +
      "outward descriptions. Use before jira_create_issue_link to confirm the link type name and direction.",
    inputSchema: {},
    annotations: { readOnlyHint: true },
  },
  () =>
    run(async () => {
      const res = await jira().request("GET", `${API}/issueLinkType`);
      return (res.issueLinkTypes ?? []).map((t: any) => ({ id: t.id, name: t.name, inward: t.inward, outward: t.outward }));
    }),
);

server.registerTool(
  "jira_create_issue_link",
  {
    title: "Create Jira issue link",
    description:
      "Link two issues with a link type from jira_get_link_types. The outward issue is the one described by the " +
      "type's outward text (for example 'TC-1 tests STORY-1': outwardIssueKey=TC-1, inwardIssueKey=STORY-1, linkType=Tests).",
    inputSchema: {
      linkType: z.string().describe("Link type name, e.g. Tests, Blocks, Relates"),
      inwardIssueKey: z.string(),
      outwardIssueKey: z.string(),
      comment: z.string().optional().describe("Optional comment added with the link (Jira wiki markup)"),
    },
  },
  ({ linkType, inwardIssueKey, outwardIssueKey, comment }) =>
    run(async () => {
      await jira().request("POST", `${API}/issueLink`, {
        body: {
          type: { name: linkType },
          inwardIssue: { key: inwardIssueKey },
          outwardIssue: { key: outwardIssueKey },
          ...(comment ? { comment: { body: comment } } : {}),
        },
      });
      return { linkType, inwardIssueKey, outwardIssueKey, created: true };
    }),
);

await server.connect(new StdioServerTransport());
console.error("Jira MCP server running on stdio");
