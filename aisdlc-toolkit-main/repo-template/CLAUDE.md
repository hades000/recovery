# Claude Code instructions — AI-First SDLC

This repository runs the SCBX AI-First SDLC Playbook. The shared workflow rules are maintained once
and imported below; the sections after the import describe what Claude Code uses instead of the
VS Code / GitHub Copilot runtime.

@.github/copilot-instructions.md

## Claude Code runtime

The lifecycle agents are Claude Code subagents in `.claude/agents/`. They are **generated** from the
VS Code / Copilot definitions in `.github/agents/*.agent.md`; edit the `.agent.md` source, then run:

```bash
node .github/scripts/sync-claude-agents.mjs
```

Run `/agents` for the definitions, or pick one in the `@` typeahead (for example
`@agent-technical-specifier`). The available subagents are:

| Stage | Subagent | Display name |
|---|---|---|
| Context | `context-builder`, `context-updater` | Context Builder, Context Updater |
| Specification | `technical-specifier` | Technical Specifier |
| Planning | `implementation-planner` | Implementation Planner |
| Build | `implementation-builder` | Implementation Builder |
| Validation | `api-tester`, `functional-automation-test`, `qa-test-case-generator`, `figma-extractor` | API Tester, Functional Automation Test, QA Test Case Generator, Figma Extractor |
| Gates and close-out | `compliance-reviewer`, `technical-documenter`, `traceability-manager` | Compliance Reviewer, Technical Documenter, Traceability Manager |

The `agents` allowlist in a `.agent.md` source becomes explicit guidance in the subagent's prompt.
Claude Code does not enforce a per-subagent allowlist, so follow that guidance and do not widen it.

## Stage discipline

Every PDLC stage is started by a human. Invoke one lifecycle agent per stage, let it finish and
report `NEXT_STEP`, then stop. Do not start the next stage on your own, and do not chain stage
agents. The Technical Specifier, Implementation Planner and Technical Documenter invoke
`compliance-reviewer` at their gates; a Critical, High or Medium finding blocks the handoff until a
human remediates and re-reviews or explicitly accepts it. Preserve every `FAIL` status and keep all
findings visible. The full severity policy is in `.github/rules/pdlc.md`.

## Commands

`.claude/commands/` provides the workflow runbooks as slash commands:

* `/intake-to-spec` — consolidate existing requirement documents, then stop before specification.
* `/intake-to-implementation` — run one stage per invocation from intake to implementation.

Both obey the same human-checkpoint rule as the prompt files in `.github/prompts/`.

## MCP servers

`.mcp.json` defines `playwright`, `jira`, `confluence` and `gitlab`. Credentials come from the
toolkit server `.env` files under `mcp/` on the machine where the servers are built, or from
variables you add with `claude mcp add -e`; never commit them. Run `/mcp` to check server status and
tool availability. `install.sh` replaces the `__TOOLKIT_DIR__` token in `.mcp.json` with the
absolute toolkit path.

## Convention

Follow the source of truth in `.github/`:

* `.github/rules/` — governance, stage gates, standards.
* `.github/templates/` — canonical artefact shapes.
* `.github/contexts/` — project context written by Context Builder and maintained by Context Updater.
* `docs/increments/` — the increment card and lifecycle tailoring record for the bounded increment.
* `output/<RUN_ID>/` — every stage artefact for one run.

Never include real customer data, credentials, secrets or production data in prompts, artefacts,
tests, commits or documentation.
