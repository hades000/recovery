---
id: claude-code
title: 4.1a Run the agents in Claude Code
description: "Use the toolkit lifecycle agents as Claude Code subagents: install, pick them from the @ typeahead, run one stage per invocation, and connect the MCP servers."
sidebar_label: 4.1a Claude Code
---

:::note Section summary
The same twelve toolkit agents that run in GitHub Copilot also install as Claude Code subagents.
Claude Code reads them from `.claude/agents/`; the rules, templates and MCP servers are the same files.
:::

The toolkit keeps one definition of each agent. `.github/agents/*.agent.md` is the source for the
VS Code / GitHub Copilot runtime, and `.claude/agents/*.md` is generated from it for Claude Code.
Both runtimes follow the same `.github/rules/` and write the same artefacts under
`output/<RUN_ID>/`.

:::warning HVE Core planning agents are not available in Claude Code
BRD Builder, PRD Builder, ADR Creation, Backlog Manager, Code Review and Azure Deploy come from the
HVE Core All VS Code extension. They do not appear in Claude Code. Use Copilot for those stages, or
start the lifecycle at specification when an approved requirement already exists.
:::

## Install and check

1. Install the toolkit into the product repository, as in
   [4.1 Environment](/getting-started/environment):

   ```bash
   cd ap2510-aisdlc/aisdlc-toolkit
   (cd mcp && npm install && npm run build)     # once per machine
   ./install.sh /path/to/product-repo
   ```

2. Open the repository with Claude Code:

   ```bash
   cd /path/to/product-repo
   claude
   ```

   On first use, approve the project MCP servers that `.mcp.json` defines.

3. Type `@` and start typing an agent name. The twelve toolkit subagents should be offered in the
   typeahead (the entry is labelled as an agent):

   | Stage | Subagent |
   |---|---|
   | Context | `context-builder`, `context-updater` |
   | Specification | `technical-specifier` |
   | Planning | `implementation-planner` |
   | Build | `implementation-builder` |
   | Validation | `api-tester`, `functional-automation-test`, `qa-test-case-generator`, `figma-extractor` |
   | Gates and close-out | `compliance-reviewer`, `technical-documenter`, `traceability-manager` |

4. Run `/mcp` and confirm `playwright`, `jira`, `confluence` and `gitlab` are connected.

If no agents appear in the typeahead, check that `.claude/agents/` exists at the repository root.
Claude Code does not pick up a newly created `agents` directory in an already-running session;
restart it.

## Run one stage

Every PDLC stage is still started by a human. Start a new session for each stage, invoke one
subagent, read its result and `NEXT_STEP`, then stop. The stage agents stop at their review gates;
they do not start the next stage.

| Stage | Example prompt |
|---|---|
| Intake | `/intake-to-spec requirement/legacy MyApp_v1` |
| Specification | `@agent-technical-specifier RUN_ID=E2-031` |
| Planning | `@agent-implementation-planner RUN_ID=E2-031` |
| Build | `@agent-implementation-builder RUN_ID=E2-031` |
| API tests | `@agent-api-tester RUN_ID=E2-031` |
| Functional tests | `@agent-functional-automation-test RUN_ID=E2-031` |
| QA test cases | `@agent-qa-test-case-generator ABCAPP-123` |
| Review | `@agent-compliance-reviewer` with the artefact to review |
| Documentation | `@agent-technical-documenter RUN_ID=E2-031` |
| Traceability | `@agent-traceability-manager` |

Claude Code may offer to delegate a matching task to a subagent on its own. The generated
descriptions mark every lifecycle stage as human-started and instruct the agent never to start a
later stage. Treat that as guidance, not enforcement: keep starting each stage deliberately. The
Compliance Reviewer is the only subagent a stage agent may spawn at its gate, besides the Figma
Extractor during specification.

`/intake-to-spec` and `/intake-to-implementation` mirror the two prompt runbooks in
`.github/prompts/`. Both obey the same one-stage-per-invocation rule.

## MCP servers

Claude Code reads `.mcp.json` at the repository root. `install.sh` writes the absolute toolkit path
into it; it contains no credentials. The Jira, Confluence and GitLab servers read their credentials
from `.env` files in the toolkit (`mcp/jira/.env`, `mcp/confluence/.env`, `mcp/gitlab/.env`). If you
prefer not to use `.env`, the toolkit's `mcp/README.md` shows the `claude mcp add -e` form.

Never commit tokens, customer data or production data. If a server cannot start because Claude Code
cannot find `node`, replace `"command": "node"` in `.mcp.json` with the absolute path from
`which node` (or `where node` on Windows).

:::tip Windows paths
Claude Code on Windows needs a Windows path such as `C:/Users/you/aisdlc-toolkit/mcp/jira/dist/index.js`.
If the installer wrote a `/mnt/c/...` or `/c/...` path, replace it with the Windows form.
:::

## Differences from the Copilot runtime

| | GitHub Copilot in VS Code | Claude Code |
|---|---|---|
| Choose an agent | Agent picker in Copilot Chat | `@` typeahead, `@agent-<name>`, or delegation |
| Toolkit agents | `.github/agents/*.agent.md` | `.claude/agents/*.md` (generated) |
| HVE Core planning agents | Yes, from the extension | No |
| Agent handoff buttons | Yes | No; read `NEXT_STEP` |
| Per-agent model pin | Yes, in frontmatter | Inherited from the session by default |
| Workflow runbooks | `.github/prompts/*.prompt.md` | `/intake-to-spec`, `/intake-to-implementation` |
| Lifecycle rules | `.github/rules/` | Same files, imported by `CLAUDE.md` |
| MCP configuration | `.vscode/mcp.json` with prompted inputs | `.mcp.json` with server `.env` files |
| Human-started stages | Enforced by the picker and review gates | Stated in `CLAUDE.md` and the generated descriptions; the squad still starts each stage |

## Keep the two runtimes in step

`.claude/agents/` and `.claude/commands/` are generated. Do not edit them. After changing an
`.agent.md` or `.prompt.md` source, run:

```bash
node .github/scripts/sync-claude-agents.mjs
```

`./install.sh /path/to/product-repo --update` refreshes the generated files in a product repository.
Use `node .github/scripts/sync-claude-agents.mjs --check` in CI to fail when the two sides drift.
The field and tool mapping is documented in the toolkit's `docs/agent-framework/CLAUDE_CODE.md`.

Next: [4.2 Convert raw requirements into a BRD](/getting-started/brd), or go straight to
[4.7 Specify](/getting-started/specify) when an approved requirement already exists.
