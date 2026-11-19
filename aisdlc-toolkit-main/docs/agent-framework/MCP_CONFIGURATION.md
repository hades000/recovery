---
description: "Workspace MCP server configuration (Playwright, Jira, Confluence, GitLab) and credential input handling."
---

# MCP Configuration

The product repository includes four MCP server entries in `.vscode/mcp.json` for VS Code and the
same four in `.mcp.json` for Claude Code (both installed from the toolkit `repo-template/`):

| Server       | Provider                                            | Used by                                           |
|--------------|-----------------------------------------------------|---------------------------------------------------|
| `playwright` | `@playwright/mcp` via `npx`                          | API Tester, Functional Automation Test            |
| `jira`       | Toolkit Jira server (`aisdlc-toolkit/mcp/jira`)       | Technical Specifier (story intake), QA Test Case Generator |
| `confluence` | Toolkit Confluence server (`aisdlc-toolkit/mcp/confluence`) | Context Builder, Context Updater              |
| `gitlab`     | Toolkit GitLab server (`aisdlc-toolkit/mcp/gitlab`)   | Code review, pipeline and merge-request evidence  |

The Jira entry looks like this:

```json
{
	"servers": {
		"jira": {
			"type": "stdio",
			"command": "node",
			"args": ["/ABSOLUTE/PATH/TO/aisdlc-toolkit/mcp/jira/dist/index.js"],
			"env": {
				"JIRA_URL": "${input:jira-url}",
				"JIRA_EMAIL": "${input:jira-email}",
				"JIRA_API_TOKEN": "${input:jira-api-token}",
				"JIRA_PAT": "${input:jira-api-token}"
			}
		}
	}
}
```

This excerpt omits the Playwright, Confluence and GitLab servers and the top-level
`inputs` array; use the full [workspace configuration](../../repo-template/.vscode/mcp.json),
not this excerpt, as the file. `install.sh` replaces the `__TOOLKIT_DIR__` token with the
absolute toolkit path. Inputs are VS Code `promptString` entries; tokens set
`password: true` and are stored encrypted by VS Code. Leave the email prompt empty when
your Jira or Confluence is Server/Data Center and the token is a Personal Access Token.
The Claude Code `.mcp.json` has no `inputs`; it reads credentials from `mcp/<server>/.env`
or from variables passed with `claude mcp add -e`. Do not add credentials, tokens, or
customer data to the repository. Build the servers
once per machine with `npm install && npm run build` in `aisdlc-toolkit/mcp/`; see the
[MCP README](../../mcp/README.md) for Copilot CLI and Claude Code configuration.

The [QA agent](../../repo-template/.github/agents/qa-test-case-generator.agent.md) explicitly allows this
server's issue search/read, create metadata, link-type, issue creation and link
creation tools (`jira_get_issue`, `jira_search_issues`, `jira_get_create_metadata`,
`jira_get_link_types`, `jira_create_issue`, `jira_create_issue_link`). The linked QA
rules/instructions use the same `jira_*` names. Jira Tasks and Tests links are created
only after explicit approval of generated test cases. See
[startup and troubleshooting](MCP_QUICK_START.md) to restart the server, enable tools
and refresh a chat's tool list.

Use MCP only when configured with approved sources such as:
- Jira project and issue metadata through the configured `jira` server.
- Architecture knowledge base.
- API catalogue.
- Product or risk-rule reference data.
- Compliance control library.
- Internal design-system reference.

Do not query, expose, or generate real customer data, account numbers, holdings, credentials, secrets, tokens, or production data.
