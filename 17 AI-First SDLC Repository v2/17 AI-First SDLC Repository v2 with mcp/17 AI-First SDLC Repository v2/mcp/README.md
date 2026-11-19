---
title: Team MCP Servers
description: Shared Model Context Protocol (MCP) servers for Jira, Confluence, and GitLab, with setup steps for GitHub Copilot and Claude Code
---

## Overview

This folder holds MCP servers the team can share instead of building their own. Each server lives in
its own subfolder and runs locally over stdio, so it works with any MCP client.

| Server       | Folder        | What it can do                                                                                    |
|--------------|---------------|---------------------------------------------------------------------------------------------------|
| `jira`       | `jira/`       | Search (JQL), read, create, update, comment, transition, link issues; list projects, fields, users |
| `confluence` | `confluence/` | Search (CQL), read, create, update (replace/append/prepend) pages; comment; list spaces, children |
| `gitlab`     | `gitlab/`     | Projects, files, branches, commits, issues, merge requests (incl. diffs), pipelines and job logs  |

The Jira and Confluence servers support Atlassian **Cloud** (`*.atlassian.net`) and
**Server / Data Center**. The GitLab server targets **self-managed (on-prem) GitLab** through REST
API v4, and also works with GitLab.com.

### Jira tools

| Tool                       | Purpose                                                        |
|----------------------------|----------------------------------------------------------------|
| `jira_search_issues`       | Search with JQL                                                |
| `jira_get_issue`           | Get an issue with description, subtasks, links, comments       |
| `jira_create_issue`        | Create an issue (Story, Task, Bug, Epic, Sub-task, ...)        |
| `jira_update_issue`        | Update summary, description, labels, assignee, custom fields   |
| `jira_add_comment`         | Add a comment                                                  |
| `jira_get_transitions`     | List the status changes available for an issue                 |
| `jira_transition_issue`    | Change status (for example to "In Progress" or "Done")         |
| `jira_list_projects`       | List projects                                                  |
| `jira_get_create_metadata` | List issue types, or fields required to create an issue type   |
| `jira_search_users`        | Find a user ID for assignment                                  |
| `jira_get_link_types`      | List issue link types (Tests, Blocks, Relates) and directions  |
| `jira_create_issue_link`   | Link two issues, for example a test-case Task to its Story     |

### Confluence tools

| Tool                           | Purpose                                                  |
|--------------------------------|----------------------------------------------------------|
| `confluence_search`            | Search with CQL                                          |
| `confluence_get_page`          | Get a page by ID or by space + title (storage or text)   |
| `confluence_get_page_children` | List child pages                                         |
| `confluence_list_spaces`       | List spaces                                              |
| `confluence_create_page`       | Create a page, optionally under a parent                 |
| `confluence_update_page`       | Update title/body; replace, append, or prepend content   |
| `confluence_add_comment`       | Add a page comment                                       |

### GitLab tools

Projects accept a numeric ID or a full path such as `group/subgroup/project`. Issues and merge
requests use the project-level number (`#123`, `!45`).

| Tool                             | Purpose                                                            |
|----------------------------------|--------------------------------------------------------------------|
| `gitlab_list_projects`           | List projects you're a member of, optionally filtered              |
| `gitlab_get_project`             | Get project details (default branch, clone URLs)                   |
| `gitlab_list_tree`               | List files and folders in a repository                             |
| `gitlab_get_file`                | Read a file from a branch, tag, or commit                          |
| `gitlab_list_branches`           | List branches                                                      |
| `gitlab_create_branch`           | Create a branch                                                    |
| `gitlab_list_commits`            | List commits by branch, path, or date range                        |
| `gitlab_commit_files`            | Create, update, delete, or move files in a single commit           |
| `gitlab_search`                  | Search code, commits, issues, MRs, and more (project or global)    |
| `gitlab_list_issues`             | List issues in a project or across projects                        |
| `gitlab_get_issue`               | Get an issue with description and comments                         |
| `gitlab_create_issue`            | Create an issue                                                    |
| `gitlab_update_issue`            | Update fields, labels, assignees; close or reopen                  |
| `gitlab_add_issue_note`          | Comment on an issue                                                |
| `gitlab_list_merge_requests`     | List merge requests in a project or across projects                |
| `gitlab_get_merge_request`       | Get an MR with description, pipeline status, and comments          |
| `gitlab_get_merge_request_diffs` | Get the MR file diffs for code review                              |
| `gitlab_create_merge_request`    | Open an MR (optionally as draft, with reviewers)                   |
| `gitlab_update_merge_request`    | Update fields, labels, assignees, reviewers; close or reopen       |
| `gitlab_add_merge_request_note`  | Comment on an MR                                                   |
| `gitlab_list_pipelines`          | List CI/CD pipelines                                               |
| `gitlab_get_pipeline`            | Get a pipeline and its jobs                                        |
| `gitlab_get_job_log`             | Get the tail of a job log to diagnose failures                     |

The GitLab server intentionally has no tool to merge an MR. Merging stays a human decision in the
GitLab UI.

## Prerequisites

* macOS, Linux, or Windows with **Node.js 20.12 or later** (`node -v`).
* A Jira and/or Confluence account with an API token (Cloud) or Personal Access Token (Server/DC).
* A GitLab Personal Access Token for your company's GitLab instance.

## Step 1: Install and build

From the repository root:

```sh
cd mcp
npm install
npm run build
```

This builds every server into `<server>/dist/index.js`. Re-run `npm run build` after pulling changes.

Get the absolute paths you'll need for client configuration:

```sh
echo "$(pwd)/jira/dist/index.js"
echo "$(pwd)/confluence/dist/index.js"
echo "$(pwd)/gitlab/dist/index.js"
which node
```

The rest of this guide uses `/ABSOLUTE/PATH/TO/mcp` as a placeholder. Replace it with your own path.

## Step 2: Configure credentials

Each server reads a `.env` file from its own folder. These files are git-ignored, so your tokens stay
on your machine and the client configurations below stay free of secrets.

```sh
cp jira/.env.example jira/.env
cp confluence/.env.example confluence/.env
cp gitlab/.env.example gitlab/.env
```

Then edit the files for the servers you use.

### Jira and Confluence Cloud

1. Create an API token at <https://id.atlassian.com/manage-profile/security/api-tokens>.
2. Fill in the files:

```dotenv
# jira/.env
JIRA_URL=https://your-company.atlassian.net
JIRA_EMAIL=you@your-company.com
JIRA_API_TOKEN=<token>
```

```dotenv
# confluence/.env  (note the /wiki suffix)
CONFLUENCE_URL=https://your-company.atlassian.net/wiki
CONFLUENCE_EMAIL=you@your-company.com
CONFLUENCE_API_TOKEN=<token>
```

The same Atlassian API token works for both Jira and Confluence.

### Jira and Confluence Server / Data Center

1. Create a Personal Access Token in each product (profile menu, then **Personal Access Tokens**).
2. Fill in the files, leaving the `*_EMAIL` variables empty:

```dotenv
# jira/.env
JIRA_URL=https://jira.your-company.com
JIRA_PAT=<token>
```

```dotenv
# confluence/.env
CONFLUENCE_URL=https://confluence.your-company.com
CONFLUENCE_PAT=<token>
```

Jira detects Cloud from the `*.atlassian.net` hostname. If your Cloud site uses a custom domain, add
`JIRA_DEPLOYMENT=cloud`.

### GitLab (self-managed)

1. In GitLab, open your avatar menu, then **Preferences** (or **Edit profile**), then
   **Access tokens** (older versions: **Personal Access Tokens**).
2. Create a token with the `api` scope for read and write access, or `read_api` for read-only.
   Set an expiry date that fits your company policy.
3. Fill in the file:

```dotenv
# gitlab/.env
GITLAB_URL=https://gitlab.your-company.com
GITLAB_TOKEN=<token>
```

If your GitLab runs under a sub-path, include it, for example `https://git.your-company.com/gitlab`.
Don't add `/api/v4`; the server adds it.

> [!NOTE]
> On-prem GitLab often uses a certificate signed by an internal company CA. If you see
> `self-signed certificate in certificate chain` or `unable to get local issuer certificate`, export the
> CA as a PEM file and set `NODE_EXTRA_CA_CERTS` in the client `env` block (see
> [Troubleshooting](#troubleshooting)). Node reads this variable only at startup, so it has no effect
> in `.env`.

> [!TIP]
> You can also skip the `.env` files and pass the same variables through the `env` block of any client
> configuration below. Values set by the client take precedence over `.env`.

## Step 3: Connect your AI client

> [!IMPORTANT]
> Desktop apps (VS Code, the GitHub Copilot app, the Claude app) often don't inherit your shell `PATH`,
> especially when Node is installed via nvm, fnm, or asdf. If a server fails to start, replace `"node"`
> with the absolute path from `which node`, for example `/opt/homebrew/bin/node`.

### GitHub Copilot in VS Code

1. Open the Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`) and run **MCP: Open User Configuration**.
   This makes the servers available in every workspace. For a single workspace, create
   `.vscode/mcp.json` instead.
2. Add the servers:

   ```json
   {
     "servers": {
       "jira": {
         "type": "stdio",
         "command": "node",
         "args": ["/ABSOLUTE/PATH/TO/mcp/jira/dist/index.js"]
       },
       "confluence": {
         "type": "stdio",
         "command": "node",
         "args": ["/ABSOLUTE/PATH/TO/mcp/confluence/dist/index.js"]
       },
       "gitlab": {
         "type": "stdio",
         "command": "node",
         "args": ["/ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js"]
       }
     }
   }
   ```

3. Select **Start** above each server in the editor, or run **MCP: List Servers** and start them.
4. Open Copilot Chat, switch to **Agent** mode, and select the tools icon to confirm the `jira_*`,
   `confluence_*`, and `gitlab_*` tools are listed.

To have VS Code prompt for tokens (stored encrypted) instead of using `.env`:

```json
{
  "inputs": [
    { "type": "promptString", "id": "atlassian-token", "description": "Atlassian API token", "password": true },
    { "type": "promptString", "id": "gitlab-token", "description": "GitLab Personal Access Token", "password": true }
  ],
  "servers": {
    "jira": {
      "type": "stdio",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/jira/dist/index.js"],
      "env": {
        "JIRA_URL": "https://your-company.atlassian.net",
        "JIRA_EMAIL": "you@your-company.com",
        "JIRA_API_TOKEN": "${input:atlassian-token}"
      }
    },
    "gitlab": {
      "type": "stdio",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js"],
      "env": {
        "GITLAB_URL": "https://gitlab.your-company.com",
        "GITLAB_TOKEN": "${input:gitlab-token}",
        "NODE_EXTRA_CA_CERTS": "/path/to/company-ca.pem"
      }
    }
  }
}
```

Omit `NODE_EXTRA_CA_CERTS` unless your GitLab uses an internal CA.

Logs: **Output** panel, then select the MCP server from the dropdown, or run **MCP: List Servers**,
choose a server, then **Show Output**.

### GitHub Copilot app and Copilot CLI

The GitHub Copilot app and Copilot CLI read user-level MCP servers from `~/.copilot/mcp-config.json`.
If the app has its own MCP settings screen, enter the same command, arguments, and environment values
shown below.

Option A: add from the terminal.

```sh
copilot mcp add jira -- node /ABSOLUTE/PATH/TO/mcp/jira/dist/index.js
copilot mcp add confluence -- node /ABSOLUTE/PATH/TO/mcp/confluence/dist/index.js
copilot mcp add gitlab -- node /ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js
copilot mcp list
```

To trust an internal CA for GitLab, add `--env NODE_EXTRA_CA_CERTS=/path/to/company-ca.pem` before `--`.

Option B: edit `~/.copilot/mcp-config.json` directly.

```json
{
  "mcpServers": {
    "jira": {
      "type": "local",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/jira/dist/index.js"],
      "tools": ["*"]
    },
    "confluence": {
      "type": "local",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/confluence/dist/index.js"],
      "tools": ["*"]
    },
    "gitlab": {
      "type": "local",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js"],
      "tools": ["*"]
    }
  }
}
```

Inside an interactive `copilot` session, run `/mcp` to check server status, or `/mcp show jira` to
list its tools.

> [!NOTE]
> Copilot CLI does not read `.vscode/mcp.json` because that file uses the `servers` key instead of
> `mcpServers`.

### Claude Code (terminal)

Add the servers at user scope so they're available in every project:

```sh
claude mcp add jira --scope user -- node /ABSOLUTE/PATH/TO/mcp/jira/dist/index.js
claude mcp add confluence --scope user -- node /ABSOLUTE/PATH/TO/mcp/confluence/dist/index.js
claude mcp add gitlab --scope user -- node /ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js
claude mcp list
```

Inside a `claude` session, run `/mcp` to check status and view tools.

To pass credentials through the client instead of `.env`, add `-e` flags before `--`:

```sh
claude mcp add jira --scope user \
  -e JIRA_URL=https://your-company.atlassian.net \
  -e JIRA_EMAIL=you@your-company.com \
  -e JIRA_API_TOKEN=<token> \
  -- node /ABSOLUTE/PATH/TO/mcp/jira/dist/index.js

claude mcp add gitlab --scope user \
  -e GITLAB_URL=https://gitlab.your-company.com \
  -e GITLAB_TOKEN=<token> \
  -e NODE_EXTRA_CA_CERTS=/path/to/company-ca.pem \
  -- node /ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js
```

Omit `NODE_EXTRA_CA_CERTS` unless your GitLab uses an internal CA.

To share a project-level setup, commit a `.mcp.json` at the project root. Claude Code prompts each
teammate to approve it on first use:

```json
{
  "mcpServers": {
    "jira": {
      "type": "stdio",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/jira/dist/index.js"]
    },
    "confluence": {
      "type": "stdio",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/confluence/dist/index.js"]
    },
    "gitlab": {
      "type": "stdio",
      "command": "node",
      "args": ["/ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js"]
    }
  }
}
```

### Claude app (desktop)

**Claude Code in the app** uses the same user configuration as the Claude Code CLI. Servers added with
`claude mcp add --scope user` show up there too.

**Claude chat in the app** uses a separate file:

1. Open **Settings**, then **Developer**, then **Edit Config**. This opens
   `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or
   `%APPDATA%\Claude\claude_desktop_config.json` on Windows.
2. Add the servers, using the absolute path to `node`:

   ```json
   {
     "mcpServers": {
       "jira": {
         "command": "/opt/homebrew/bin/node",
         "args": ["/ABSOLUTE/PATH/TO/mcp/jira/dist/index.js"]
       },
       "confluence": {
         "command": "/opt/homebrew/bin/node",
         "args": ["/ABSOLUTE/PATH/TO/mcp/confluence/dist/index.js"]
       },
       "gitlab": {
         "command": "/opt/homebrew/bin/node",
         "args": ["/ABSOLUTE/PATH/TO/mcp/gitlab/dist/index.js"]
       }
     }
   }
   ```

3. Quit the app completely (`Cmd+Q`) and reopen it. The tools appear under the tools/connectors menu
   in the chat input.

Logs: `~/Library/Logs/Claude/mcp-server-<name>.log`, for example `mcp-server-gitlab.log`.

## Step 4: Try it

Example prompts:

* "List my unresolved Jira issues in project ABC ordered by priority."
* "Create a Story in ABC titled 'Add SSO login' with acceptance criteria, then move it to In Progress."
* "Add a comment to ABC-123 summarizing the changes in this branch."
* "Find the Confluence page 'Release Process' in space ENG and summarize it."
* "Append a 'Release 2.4' section to page 123456 with the notes from ABC-100 to ABC-120."
* "Show my open merge requests in GitLab and which ones have failing pipelines."
* "Review MR !45 in group/payments-api and post your findings as a comment."
* "Why did the latest pipeline on main fail in group/payments-api? Check the job log."
* "Create GitLab issue in group/payments-api for the bug described in ABC-123 and link back to Jira."

Write tools (`create`, `update`, `transition`, `comment`, `commit`) run with **your** permissions.
Copilot and Claude ask for confirmation before calling them unless you've auto-approved the tools. Use a
`read_api` GitLab token if you want the GitLab server to be read-only.

## Troubleshooting

| Symptom                                   | Fix                                                                                                         |
|-------------------------------------------|-------------------------------------------------------------------------------------------------------------|
| `JIRA_URL is not set` / `Set JIRA_EMAIL`  | Create the server's `.env` (for example `jira/.env`) or pass the variables through the client `env` block   |
| Jira/Confluence `401 Unauthorized`        | Cloud requires email + API token (not your password). Server/DC requires a PAT with no email set            |
| Confluence `404` on Cloud                 | `CONFLUENCE_URL` must end with `/wiki`                                                                      |
| Jira search returns `404` or `410`        | The Cloud/Server detection is wrong. Set `JIRA_DEPLOYMENT=cloud` or `JIRA_DEPLOYMENT=server`                |
| GitLab `401 Unauthorized`                 | Token is wrong, expired, or revoked. Create a new one and update `GITLAB_TOKEN`                             |
| GitLab `403 Forbidden` on write tools     | Token has only `read_api`, or your project role is too low (for example Guest). Use an `api` token          |
| GitLab `404 Project Not Found`            | Use the full path (`group/subgroup/project`) or numeric ID, and check you're a member of the project        |
| `ENOTFOUND` / `ETIMEDOUT` for GitLab      | On-prem GitLab usually needs the company network or VPN. Confirm `curl -I $GITLAB_URL` works                 |
| `spawn node ENOENT` / server won't start  | Use the absolute path from `which node` as the `command`                                                    |
| `self-signed certificate` / TLS errors    | Add `NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem` to the client `env` block (it's ignored in `.env`)      |
| Tools missing after `git pull`            | Run `npm install && npm run build` in `mcp/`, then restart the server in your client                        |

To test a server outside any AI client, use the MCP Inspector:

```sh
npx @modelcontextprotocol/inspector node jira/dist/index.js
```

## Adding a new MCP server

1. Create a folder, for example `mcp/servicenow/`, with `package.json`, `tsconfig.json`
   (extending `../tsconfig.base.json`), `.env.example`, and `src/index.ts`. Use `jira/` as a template.
2. Add the folder name to `workspaces` in `mcp/package.json`.
3. Run `npm install && npm run build` from `mcp/`.
4. Add a row to the table in [Overview](#overview) and register the server in your clients as shown
   above.
