#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { GitLabClient, loadConfig, projectPath } from "./client.js";

let client: GitLabClient | undefined;
function gitlab(): GitLabClient {
  return (client ??= new GitLabClient(loadConfig()));
}

async function run(fn: () => Promise<unknown>) {
  try {
    const data = await fn();
    const text = typeof data === "string" ? data : JSON.stringify(data, null, 2);
    return { content: [{ type: "text" as const, text }] };
  } catch (e) {
    return { isError: true, content: [{ type: "text" as const, text: e instanceof Error ? e.message : String(e) }] };
  }
}

const project = z.string().describe("Project ID or full path, e.g. 'group/subgroup/project'");
const page = z.number().int().min(1).optional();
const perPage = z.number().int().min(1).max(100).default(20);

const csv = (v?: string[]) => (v ? v.join(",") : undefined);
const usernames = (users?: any[]) => users?.map((u) => u.username);

async function userIds(names: string[]): Promise<number[]> {
  return Promise.all(
    names.map(async (username) => {
      const [u] = await gitlab().request<any[]>("GET", "/users", { query: { username } });
      if (!u) throw new Error(`GitLab user '${username}' not found`);
      return u.id;
    }),
  );
}

async function defaultBranch(p: string): Promise<string> {
  return (await gitlab().request("GET", projectPath(p))).default_branch;
}

async function notes(path: string) {
  const { items } = await gitlab().list(`${path}/notes`, { sort: "asc", order_by: "created_at", per_page: 100 });
  return items
    .filter((n: any) => !n.system)
    .map((n: any) => ({ id: n.id, author: n.author?.username, created: n.created_at, body: n.body }));
}

function summarizeIssue(i: any) {
  return {
    iid: i.iid,
    project: i.references?.full?.split("#")[0],
    title: i.title,
    state: i.state,
    labels: i.labels,
    author: i.author?.username,
    assignees: usernames(i.assignees),
    milestone: i.milestone?.title,
    dueDate: i.due_date,
    created: i.created_at,
    updated: i.updated_at,
    url: i.web_url,
  };
}

function summarizeMr(m: any) {
  return {
    iid: m.iid,
    project: m.references?.full?.split("!")[0],
    title: m.title,
    state: m.state,
    draft: m.draft ?? m.work_in_progress,
    sourceBranch: m.source_branch,
    targetBranch: m.target_branch,
    author: m.author?.username,
    assignees: usernames(m.assignees),
    reviewers: usernames(m.reviewers),
    labels: m.labels,
    mergeStatus: m.detailed_merge_status ?? m.merge_status,
    hasConflicts: m.has_conflicts,
    created: m.created_at,
    updated: m.updated_at,
    url: m.web_url,
  };
}

function summarizePipeline(p: any) {
  return { id: p.id, status: p.status, ref: p.ref, sha: p.sha?.slice(0, 8), source: p.source, created: p.created_at, url: p.web_url };
}

const server = new McpServer({ name: "gitlab", version: "1.0.0" });

// ---------- Projects & repository ----------

server.registerTool(
  "gitlab_list_projects",
  {
    title: "List GitLab projects",
    description: "List GitLab projects, optionally filtered by name/path.",
    inputSchema: {
      search: z.string().optional(),
      membership: z.boolean().default(true).describe("Only projects you are a member of"),
      perPage,
      page,
    },
    annotations: { readOnlyHint: true },
  },
  ({ search, membership, perPage, page }) =>
    run(async () => {
      const { items, nextPage } = await gitlab().list("/projects", {
        search, membership, simple: true, order_by: "last_activity_at", per_page: perPage, page,
      });
      return {
        nextPage,
        projects: items.map((p: any) => ({
          id: p.id, path: p.path_with_namespace, name: p.name, defaultBranch: p.default_branch, url: p.web_url, lastActivity: p.last_activity_at,
        })),
      };
    }),
);

server.registerTool(
  "gitlab_get_project",
  {
    title: "Get GitLab project",
    description: "Get project details (default branch, URLs, description).",
    inputSchema: { project },
    annotations: { readOnlyHint: true },
  },
  ({ project }) =>
    run(async () => {
      const p = await gitlab().request("GET", projectPath(project));
      return {
        id: p.id, path: p.path_with_namespace, name: p.name, description: p.description, defaultBranch: p.default_branch,
        visibility: p.visibility, url: p.web_url, sshUrl: p.ssh_url_to_repo, httpUrl: p.http_url_to_repo,
        openIssues: p.open_issues_count, lastActivity: p.last_activity_at,
      };
    }),
);

server.registerTool(
  "gitlab_list_tree",
  {
    title: "List repository files",
    description: "List files and folders in a repository path.",
    inputSchema: {
      project,
      path: z.string().optional().describe("Folder path; repository root if omitted"),
      ref: z.string().optional().describe("Branch, tag or commit; default branch if omitted"),
      recursive: z.boolean().default(false),
      perPage: z.number().int().min(1).max(100).default(100),
      page,
    },
    annotations: { readOnlyHint: true },
  },
  ({ project, path, ref, recursive, perPage, page }) =>
    run(async () => {
      const { items, nextPage } = await gitlab().list(`${projectPath(project)}/repository/tree`, {
        path, ref, recursive, per_page: perPage, page,
      });
      return { nextPage, entries: items.map((e: any) => ({ path: e.path, type: e.type })) };
    }),
);

server.registerTool(
  "gitlab_get_file",
  {
    title: "Get repository file",
    description: "Read a file's contents from a repository.",
    inputSchema: {
      project,
      filePath: z.string().describe("Path in the repository, e.g. 'src/app.ts'"),
      ref: z.string().optional().describe("Branch, tag or commit; default branch if omitted"),
      maxChars: z.number().int().min(1000).default(200_000),
    },
    annotations: { readOnlyHint: true },
  },
  ({ project, filePath, ref, maxChars }) =>
    run(async () => {
      const r = ref ?? (await defaultBranch(project));
      const text = await gitlab().raw(`${projectPath(project)}/repository/files/${encodeURIComponent(filePath)}/raw`, { ref: r });
      return text.length > maxChars ? `${text.slice(0, maxChars)}\n\n[truncated: ${text.length} chars total]` : text;
    }),
);

server.registerTool(
  "gitlab_list_branches",
  {
    title: "List branches",
    description: "List repository branches.",
    inputSchema: { project, search: z.string().optional(), perPage, page },
    annotations: { readOnlyHint: true },
  },
  ({ project, search, perPage, page }) =>
    run(async () => {
      const { items, nextPage } = await gitlab().list(`${projectPath(project)}/repository/branches`, { search, per_page: perPage, page });
      return {
        nextPage,
        branches: items.map((b: any) => ({
          name: b.name, default: b.default, protected: b.protected, merged: b.merged,
          lastCommit: { sha: b.commit?.short_id, title: b.commit?.title, author: b.commit?.author_name, date: b.commit?.committed_date },
        })),
      };
    }),
);

server.registerTool(
  "gitlab_create_branch",
  {
    title: "Create branch",
    description: "Create a new branch from an existing branch, tag or commit.",
    inputSchema: { project, branch: z.string(), ref: z.string().optional().describe("Source ref; default branch if omitted") },
  },
  ({ project, branch, ref }) =>
    run(async () => {
      const r = ref ?? (await defaultBranch(project));
      const b = await gitlab().request("POST", `${projectPath(project)}/repository/branches`, { query: { branch, ref: r } });
      return { name: b.name, from: r, sha: b.commit?.short_id, url: b.web_url };
    }),
);

server.registerTool(
  "gitlab_list_commits",
  {
    title: "List commits",
    description: "List commits on a branch, optionally limited to a file/folder path or date range.",
    inputSchema: {
      project,
      ref: z.string().optional(),
      path: z.string().optional(),
      since: z.string().optional().describe("ISO 8601 date"),
      until: z.string().optional().describe("ISO 8601 date"),
      perPage,
      page,
    },
    annotations: { readOnlyHint: true },
  },
  ({ project, ref, path, since, until, perPage, page }) =>
    run(async () => {
      const { items, nextPage } = await gitlab().list(`${projectPath(project)}/repository/commits`, {
        ref_name: ref, path, since, until, per_page: perPage, page,
      });
      return {
        nextPage,
        commits: items.map((c: any) => ({ sha: c.short_id, title: c.title, author: c.author_name, date: c.committed_date, url: c.web_url })),
      };
    }),
);

server.registerTool(
  "gitlab_commit_files",
  {
    title: "Commit file changes",
    description:
      "Create one commit that creates, updates, deletes or moves files on a branch. " +
      "Set startBranch to create the branch from another branch in the same call.",
    inputSchema: {
      project,
      branch: z.string().describe("Branch to commit to"),
      commitMessage: z.string(),
      startBranch: z.string().optional().describe("Create 'branch' from this branch if it doesn't exist"),
      actions: z
        .array(
          z.object({
            action: z.enum(["create", "update", "delete", "move"]),
            filePath: z.string(),
            previousPath: z.string().optional().describe("Required for 'move'"),
            content: z.string().optional().describe("Full file content for create/update"),
          }),
        )
        .min(1),
    },
  },
  ({ project, branch, commitMessage, startBranch, actions }) =>
    run(async () => {
      const c = await gitlab().request("POST", `${projectPath(project)}/repository/commits`, {
        body: {
          branch,
          commit_message: commitMessage,
          ...(startBranch && { start_branch: startBranch }),
          actions: actions.map((a) => ({
            action: a.action,
            file_path: a.filePath,
            ...(a.previousPath && { previous_path: a.previousPath }),
            ...(a.content !== undefined && { content: a.content }),
          })),
        },
      });
      return { sha: c.short_id, title: c.title, branch, url: c.web_url };
    }),
);

server.registerTool(
  "gitlab_search",
  {
    title: "Search GitLab",
    description:
      "Search GitLab. With a project: scopes blobs (code), commits, issues, merge_requests, notes, wiki_blobs. " +
      "Without a project: projects, issues, merge_requests (plus blobs/commits if advanced search is enabled).",
    inputSchema: {
      query: z.string(),
      scope: z.enum(["projects", "blobs", "commits", "issues", "merge_requests", "notes", "wiki_blobs", "milestones", "users"]),
      project: project.optional(),
      ref: z.string().optional().describe("Branch/tag for blobs and commits (project search only)"),
      perPage,
      page,
    },
    annotations: { readOnlyHint: true },
  },
  ({ query, scope, project, ref, perPage, page }) =>
    run(async () => {
      const path = project ? `${projectPath(project)}/search` : "/search";
      const { items, nextPage } = await gitlab().list(path, { search: query, scope, ref, per_page: perPage, page });
      const results = items.map((r: any) => {
        if (scope === "blobs" || scope === "wiki_blobs") return { path: r.path, ref: r.ref, startLine: r.startline, snippet: r.data };
        if (scope === "issues") return summarizeIssue(r);
        if (scope === "merge_requests") return summarizeMr(r);
        if (scope === "commits") return { sha: r.short_id, title: r.title, author: r.author_name, date: r.committed_date };
        if (scope === "projects") return { id: r.id, path: r.path_with_namespace, url: r.web_url };
        return r;
      });
      return { nextPage, results };
    }),
);

// ---------- Issues ----------

server.registerTool(
  "gitlab_list_issues",
  {
    title: "List GitLab issues",
    description: "List issues in a project, or across all projects you can access when project is omitted.",
    inputSchema: {
      project: project.optional(),
      state: z.enum(["opened", "closed", "all"]).default("opened"),
      labels: z.array(z.string()).optional(),
      assigneeUsername: z.string().optional(),
      authorUsername: z.string().optional(),
      milestone: z.string().optional(),
      search: z.string().optional().describe("Text in title or description"),
      scope: z.enum(["created_by_me", "assigned_to_me", "all"]).default("all"),
      perPage,
      page,
    },
    annotations: { readOnlyHint: true },
  },
  (a) =>
    run(async () => {
      const path = a.project ? `${projectPath(a.project)}/issues` : "/issues";
      const { items, nextPage } = await gitlab().list(path, {
        state: a.state, labels: csv(a.labels), assignee_username: a.assigneeUsername, author_username: a.authorUsername,
        milestone: a.milestone, search: a.search, scope: a.scope, order_by: "updated_at", per_page: a.perPage, page: a.page,
      });
      return { nextPage, issues: items.map(summarizeIssue) };
    }),
);

server.registerTool(
  "gitlab_get_issue",
  {
    title: "Get GitLab issue",
    description: "Get an issue by its project-level IID (the number shown as #123), including description and comments.",
    inputSchema: { project, issueIid: z.number().int(), includeNotes: z.boolean().default(true) },
    annotations: { readOnlyHint: true },
  },
  ({ project, issueIid, includeNotes }) =>
    run(async () => {
      const path = `${projectPath(project)}/issues/${issueIid}`;
      const i = await gitlab().request("GET", path);
      return { ...summarizeIssue(i), description: i.description, notes: includeNotes ? await notes(path) : undefined };
    }),
);

server.registerTool(
  "gitlab_create_issue",
  {
    title: "Create GitLab issue",
    description: "Create an issue. Description supports GitLab Flavored Markdown.",
    inputSchema: {
      project,
      title: z.string(),
      description: z.string().optional(),
      labels: z.array(z.string()).optional(),
      assignees: z.array(z.string()).optional().describe("Usernames"),
      milestoneId: z.number().int().optional(),
      dueDate: z.string().optional().describe("YYYY-MM-DD"),
      confidential: z.boolean().optional(),
    },
  },
  (a) =>
    run(async () => {
      const i = await gitlab().request("POST", `${projectPath(a.project)}/issues`, {
        body: {
          title: a.title,
          description: a.description,
          labels: csv(a.labels),
          assignee_ids: a.assignees ? await userIds(a.assignees) : undefined,
          milestone_id: a.milestoneId,
          due_date: a.dueDate,
          confidential: a.confidential,
        },
      });
      return summarizeIssue(i);
    }),
);

server.registerTool(
  "gitlab_update_issue",
  {
    title: "Update GitLab issue",
    description: "Update an issue. Only provided fields are changed. Use state 'close' or 'reopen' to change status.",
    inputSchema: {
      project,
      issueIid: z.number().int(),
      title: z.string().optional(),
      description: z.string().optional(),
      labels: z.array(z.string()).optional().describe("Replace all labels"),
      addLabels: z.array(z.string()).optional(),
      removeLabels: z.array(z.string()).optional(),
      assignees: z.array(z.string()).optional().describe("Usernames; empty array to unassign"),
      milestoneId: z.number().int().nullable().optional().describe("null to remove milestone"),
      dueDate: z.string().optional(),
      state: z.enum(["close", "reopen"]).optional(),
    },
  },
  (a) =>
    run(async () => {
      const i = await gitlab().request("PUT", `${projectPath(a.project)}/issues/${a.issueIid}`, {
        body: {
          title: a.title,
          description: a.description,
          labels: csv(a.labels),
          add_labels: csv(a.addLabels),
          remove_labels: csv(a.removeLabels),
          assignee_ids: a.assignees ? await userIds(a.assignees) : undefined,
          milestone_id: a.milestoneId === null ? 0 : a.milestoneId,
          due_date: a.dueDate,
          state_event: a.state,
        },
      });
      return summarizeIssue(i);
    }),
);

server.registerTool(
  "gitlab_add_issue_note",
  {
    title: "Comment on GitLab issue",
    description: "Add a comment to an issue (GitLab Flavored Markdown).",
    inputSchema: { project, issueIid: z.number().int(), body: z.string() },
  },
  ({ project, issueIid, body }) =>
    run(async () => {
      const n = await gitlab().request("POST", `${projectPath(project)}/issues/${issueIid}/notes`, { body: { body } });
      return { id: n.id, created: n.created_at };
    }),
);

// ---------- Merge requests ----------

server.registerTool(
  "gitlab_list_merge_requests",
  {
    title: "List merge requests",
    description: "List merge requests in a project, or across all projects you can access when project is omitted.",
    inputSchema: {
      project: project.optional(),
      state: z.enum(["opened", "closed", "merged", "all"]).default("opened"),
      scope: z.enum(["created_by_me", "assigned_to_me", "all"]).default("all"),
      authorUsername: z.string().optional(),
      reviewerUsername: z.string().optional(),
      labels: z.array(z.string()).optional(),
      sourceBranch: z.string().optional(),
      targetBranch: z.string().optional(),
      search: z.string().optional(),
      perPage,
      page,
    },
    annotations: { readOnlyHint: true },
  },
  (a) =>
    run(async () => {
      const path = a.project ? `${projectPath(a.project)}/merge_requests` : "/merge_requests";
      const { items, nextPage } = await gitlab().list(path, {
        state: a.state, scope: a.scope, author_username: a.authorUsername, reviewer_username: a.reviewerUsername,
        labels: csv(a.labels), source_branch: a.sourceBranch, target_branch: a.targetBranch, search: a.search,
        order_by: "updated_at", per_page: a.perPage, page: a.page,
      });
      return { nextPage, mergeRequests: items.map(summarizeMr) };
    }),
);

server.registerTool(
  "gitlab_get_merge_request",
  {
    title: "Get merge request",
    description: "Get a merge request by IID (the number shown as !123), including description, pipeline status and comments.",
    inputSchema: { project, mrIid: z.number().int(), includeNotes: z.boolean().default(true) },
    annotations: { readOnlyHint: true },
  },
  ({ project, mrIid, includeNotes }) =>
    run(async () => {
      const path = `${projectPath(project)}/merge_requests/${mrIid}`;
      const m = await gitlab().request("GET", path);
      return {
        ...summarizeMr(m),
        description: m.description,
        pipeline: m.head_pipeline ? summarizePipeline(m.head_pipeline) : null,
        changesCount: m.changes_count,
        notes: includeNotes ? await notes(path) : undefined,
      };
    }),
);

server.registerTool(
  "gitlab_get_merge_request_diffs",
  {
    title: "Get merge request diffs",
    description: "Get the file diffs of a merge request (for code review).",
    inputSchema: {
      project,
      mrIid: z.number().int(),
      maxChars: z.number().int().min(1000).default(100_000).describe("Truncate combined diff output at this size"),
    },
    annotations: { readOnlyHint: true },
  },
  ({ project, mrIid, maxChars }) =>
    run(async () => {
      const path = `${projectPath(project)}/merge_requests/${mrIid}`;
      let files: any[] = [];
      try {
        for (let p: number | null = 1; p && p <= 20; ) {
          const res: { items: any[]; nextPage: number | null } = await gitlab().list(`${path}/diffs`, { per_page: 100, page: p });
          files.push(...res.items);
          p = res.nextPage;
        }
      } catch (e) {
        // /diffs was added in GitLab 15.7; older instances only have /changes
        if ((e as { status?: number }).status !== 404) throw e;
        files = (await gitlab().request("GET", `${path}/changes`)).changes ?? [];
      }

      let out = "";
      const omitted: string[] = [];
      for (const f of files) {
        const header = `diff --git a/${f.old_path} b/${f.new_path}${f.new_file ? " (new)" : ""}${f.deleted_file ? " (deleted)" : ""}${f.renamed_file ? " (renamed)" : ""}\n`;
        const chunk = header + (f.diff || "(no textual diff: binary or too large)\n");
        if (out.length + chunk.length > maxChars) omitted.push(f.new_path);
        else out += chunk;
      }
      if (omitted.length) out += `\n[${omitted.length} file(s) omitted to stay under ${maxChars} chars: ${omitted.join(", ")}]`;
      return `${files.length} file(s) changed\n\n${out}`;
    }),
);

server.registerTool(
  "gitlab_create_merge_request",
  {
    title: "Create merge request",
    description: "Open a merge request. Description supports GitLab Flavored Markdown.",
    inputSchema: {
      project,
      sourceBranch: z.string(),
      targetBranch: z.string().optional().describe("Default branch if omitted"),
      title: z.string(),
      description: z.string().optional(),
      draft: z.boolean().default(false),
      labels: z.array(z.string()).optional(),
      assignees: z.array(z.string()).optional().describe("Usernames"),
      reviewers: z.array(z.string()).optional().describe("Usernames"),
      removeSourceBranch: z.boolean().default(true),
      squash: z.boolean().optional(),
    },
  },
  (a) =>
    run(async () => {
      const m = await gitlab().request("POST", `${projectPath(a.project)}/merge_requests`, {
        body: {
          source_branch: a.sourceBranch,
          target_branch: a.targetBranch ?? (await defaultBranch(a.project)),
          title: a.draft && !/^draft:/i.test(a.title) ? `Draft: ${a.title}` : a.title,
          description: a.description,
          labels: csv(a.labels),
          assignee_ids: a.assignees ? await userIds(a.assignees) : undefined,
          reviewer_ids: a.reviewers ? await userIds(a.reviewers) : undefined,
          remove_source_branch: a.removeSourceBranch,
          squash: a.squash,
        },
      });
      return summarizeMr(m);
    }),
);

server.registerTool(
  "gitlab_update_merge_request",
  {
    title: "Update merge request",
    description: "Update a merge request. Only provided fields are changed. Use state 'close' or 'reopen' to change status. Does not merge.",
    inputSchema: {
      project,
      mrIid: z.number().int(),
      title: z.string().optional(),
      description: z.string().optional(),
      targetBranch: z.string().optional(),
      labels: z.array(z.string()).optional().describe("Replace all labels"),
      addLabels: z.array(z.string()).optional(),
      removeLabels: z.array(z.string()).optional(),
      assignees: z.array(z.string()).optional().describe("Usernames; empty array to unassign"),
      reviewers: z.array(z.string()).optional().describe("Usernames; empty array to clear"),
      state: z.enum(["close", "reopen"]).optional(),
    },
  },
  (a) =>
    run(async () => {
      const m = await gitlab().request("PUT", `${projectPath(a.project)}/merge_requests/${a.mrIid}`, {
        body: {
          title: a.title,
          description: a.description,
          target_branch: a.targetBranch,
          labels: csv(a.labels),
          add_labels: csv(a.addLabels),
          remove_labels: csv(a.removeLabels),
          assignee_ids: a.assignees ? await userIds(a.assignees) : undefined,
          reviewer_ids: a.reviewers ? await userIds(a.reviewers) : undefined,
          state_event: a.state,
        },
      });
      return summarizeMr(m);
    }),
);

server.registerTool(
  "gitlab_add_merge_request_note",
  {
    title: "Comment on merge request",
    description: "Add a comment to a merge request (GitLab Flavored Markdown).",
    inputSchema: { project, mrIid: z.number().int(), body: z.string() },
  },
  ({ project, mrIid, body }) =>
    run(async () => {
      const n = await gitlab().request("POST", `${projectPath(project)}/merge_requests/${mrIid}/notes`, { body: { body } });
      return { id: n.id, created: n.created_at };
    }),
);

// ---------- CI/CD ----------

server.registerTool(
  "gitlab_list_pipelines",
  {
    title: "List pipelines",
    description: "List CI/CD pipelines for a project, newest first.",
    inputSchema: {
      project,
      ref: z.string().optional().describe("Branch or tag"),
      status: z.enum(["created", "waiting_for_resource", "preparing", "pending", "running", "success", "failed", "canceled", "skipped", "manual", "scheduled"]).optional(),
      perPage,
      page,
    },
    annotations: { readOnlyHint: true },
  },
  ({ project, ref, status, perPage, page }) =>
    run(async () => {
      const { items, nextPage } = await gitlab().list(`${projectPath(project)}/pipelines`, { ref, status, per_page: perPage, page });
      return { nextPage, pipelines: items.map(summarizePipeline) };
    }),
);

server.registerTool(
  "gitlab_get_pipeline",
  {
    title: "Get pipeline",
    description: "Get a pipeline with its jobs (stage, status, duration). Use gitlab_get_job_log for failed job output.",
    inputSchema: { project, pipelineId: z.number().int() },
    annotations: { readOnlyHint: true },
  },
  ({ project, pipelineId }) =>
    run(async () => {
      const path = `${projectPath(project)}/pipelines/${pipelineId}`;
      const p = await gitlab().request("GET", path);
      const { items: jobs } = await gitlab().list(`${path}/jobs`, { per_page: 100 });
      return {
        ...summarizePipeline(p),
        duration: p.duration,
        jobs: jobs.map((j: any) => ({
          id: j.id, name: j.name, stage: j.stage, status: j.status, duration: j.duration, allowFailure: j.allow_failure,
          failureReason: j.failure_reason, url: j.web_url,
        })),
      };
    }),
);

server.registerTool(
  "gitlab_get_job_log",
  {
    title: "Get job log",
    description: "Get the tail of a CI job's log (useful to diagnose failures).",
    inputSchema: { project, jobId: z.number().int(), tailLines: z.number().int().min(10).max(5000).default(200) },
    annotations: { readOnlyHint: true },
  },
  ({ project, jobId, tailLines }) =>
    run(async () => {
      const log = (await gitlab().raw(`${projectPath(project)}/jobs/${jobId}/trace`))
        // strip ANSI colors and GitLab collapsible-section markers
        .replace(/\x1b\[[0-9;]*[A-Za-z]/g, "")
        .replace(/section_(start|end):\d+:[^\r\n]*\r/g, "");
      const lines = log.split(/\r?\n/);
      const tail = lines.slice(-tailLines).join("\n");
      return lines.length > tailLines ? `[showing last ${tailLines} of ${lines.length} lines]\n${tail}` : tail;
    }),
);

await server.connect(new StdioServerTransport());
console.error("GitLab MCP server running on stdio");
