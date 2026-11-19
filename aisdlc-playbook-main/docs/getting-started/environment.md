---
id: environment
title: 4.1 Set up the environment
description: "Install the HVE Core agents, the toolkit agents and the MCP servers before starting the pilot workflow."
sidebar_label: 4.1 Environment
---

:::note Section summary
Install the HVE Core agents, the toolkit agents and the MCP servers before starting the pilot workflow.
:::

The squad needs two sets of agents: the **HVE Core** planning agents (BRD Builder, PRD Builder, ADR
Creation, Backlog Manager, Code Review, Azure Deploy) from the HVE Core All extension, and the
**toolkit** lifecycle agents (Context Builder, Technical Specifier, Implementation Planner,
Implementation Builder, API Tester, Functional Automation Test, Compliance Reviewer and others)
installed into the repository. The toolkit agents run in VS Code with GitHub Copilot and in
Claude Code; HVE Core runs only in VS Code.

## Choose the runtime

| Runtime | Agents available | Setup |
|---|---|---|
| VS Code with GitHub Copilot | HVE Core planning agents and the twelve toolkit agents | This page |
| Claude Code (terminal or desktop app) | The twelve toolkit agents | This page for `install.sh` and the MCP build, then [4.1a Claude Code](/getting-started/claude-code) |

The toolkit keeps one source per agent and generates the Claude Code subagents from it, so the rules,
templates and artefacts are identical in both runtimes.

## Add the HVE Core All extension

1. Open VS Code.
2. Search for the **HVE Core All** extension and install it.
3. After installation, switch to the **Pre-Release Version** to access the experimental agents.
4. Restart VS Code or use **Developer: Reload Window**.
5. Open GitHub Copilot Chat and check the Agent Picker. The HVE Core agents should appear in the
   list.

## Install the toolkit agents

There are two ways to add the toolkit's `.github/` folder to the product repository.

### Option A: install from the toolkit folder (recommended)

```bash
cd ap2510-aisdlc/aisdlc-toolkit
(cd mcp && npm install && npm run build)     # once per machine
./install.sh /path/to/product-repo
```

The installer copies the agents, rules, prompts, templates, scripts, `.vscode/mcp.json` and the
standard folder structure, and points the MCP servers at the toolkit. See the
[toolkit page](/toolkit) for the full layout.

### Option B: install packaged agents from a VSIX file

1. Open **Extensions** in VS Code and select **Install from VSIX**.
2. Choose and install the required VSIX file.
3. Open the command palette (`Ctrl/Cmd + Shift + P`), search for and select
   **Install Packaged Workspace Folder**.
4. Confirm that the `.github` folder has been added to the workspace.

## Start the MCP servers

The toolkit configures four MCP servers in `.vscode/mcp.json` for VS Code and in `.mcp.json` for
Claude Code: `playwright` (API and functional testing), `jira`, `confluence` and `gitlab`.

1. Run **MCP: List Servers** in the command palette.
2. Select each server, then **Start**, and approve the server trust prompt.
3. Enter the base URL, email (Cloud only) and token when prompted. Tokens are stored encrypted by
   VS Code; never paste them into chat or source files.
4. Open the chat tool picker (**Configure Tools**) and confirm the `jira_*`, `confluence_*`,
   `gitlab_*` and `playwright` tools are enabled.

If a server fails to start because VS Code cannot find `node`, replace `"command": "node"` in
`.vscode/mcp.json` with the absolute path from `which node`.

For Claude Code, the same servers are read from `.mcp.json`; credentials come from the toolkit
server `.env` files or from `claude mcp add -e`. See [4.1a Claude Code](/getting-started/claude-code).

## Confirm readiness

* [ ] HVE Core agents visible in the Agent Picker
* [ ] Toolkit agents visible in the Agent Picker (Context Builder, Technical Specifier, ...)
* [ ] Claude Code users: toolkit subagents offered in the `@` typeahead and servers connected in `/mcp`
* [ ] `.github/contexts/` present (empty until the Context Builder runs)
* [ ] MCP servers started and tools enabled
* [ ] Source documents (raw requirements, transcripts, statement of work) available
* [ ] Backlog platform (Jira or Azure DevOps) project and access confirmed
* [ ] Increment card created in `docs/increments/`

Next: [4.2 Convert raw requirements into a BRD](/getting-started/brd).
