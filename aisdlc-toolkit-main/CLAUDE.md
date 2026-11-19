# Claude Code — AI-First SDLC Toolkit

This repository is the **toolkit**, not a product repository. It holds the agent sources, rules,
templates, MCP servers and the installer that product repositories use. Nothing here runs the
lifecycle itself.

## See the agents in Claude Code

The Claude Code subagents live in the product template, not at this root:

* **Try them without a product repository:** open `repo-template/` in Claude Code
  (`cd repo-template && claude`) and type `@` to pick a subagent. That folder is a complete
  product-repository layout, so the subagents and their rules resolve. The MCP entries still hold the
  `__TOOLKIT_DIR__` placeholder until you install, so MCP-backed stages need an installed repository
  or a manual path edit.
* **Use them in a real repository:** run `./install.sh /path/to/product-repo`, then open that
  repository with `claude` and type `@` to pick a subagent.

`.claude/agents/` is generated from `.github/agents/*.agent.md`; never edit the generated files.

## Toolkit layout

| Path | What it is |
|---|---|
| `repo-template/` | Everything copied into a product repository: `.github/` agents, rules, prompts, templates and scripts; `.claude/` subagents and commands; `CLAUDE.md`; `.mcp.json`; `.vscode/mcp.json` |
| `install.sh` | Installs the template; `--update` refreshes toolkit-owned files; `--dry-run` previews |
| `mcp/` | Jira, Confluence and GitLab MCP servers (TypeScript, stdio) |
| `docs/agent-framework/` | Framework reference, including `CLAUDE_CODE.md` for the runtime mapping |

## Maintaining the Claude Code runtime

Run these from `repo-template/`:

```bash
node .github/scripts/sync-claude-agents.mjs           # regenerate after editing .agent.md or .prompt.md
node .github/scripts/sync-claude-agents.mjs --check   # fail when generated files are stale
claude plugin validate .claude/agents                 # validate subagent frontmatter
```

Edit the `.github/agents/*.agent.md` and `.github/prompts/*.prompt.md` sources, then regenerate.
The generator maps Copilot tool aliases (`read`, `search`, `edit`, `execute`, `agent`, `todo`,
`<server>/*`) to Claude Code tools and MCP names; the mapping table is in
`docs/agent-framework/CLAUDE_CODE.md`.

## Keep the playbook in step

`../aisdlc-playbook/` documents this toolkit. When an agent, command or MCP behaviour changes,
update its `docs/toolkit.md` and, when the runtime experience changes,
`docs/getting-started/claude-code.md`.
