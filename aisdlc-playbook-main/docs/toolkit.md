---
id: toolkit
title: Toolkit
description: "The agents, rules, templates, MCP servers and standard repository structure that this playbook refers to."
sidebar_label: Toolkit
---

:::note Section summary
The agents, rules, templates, MCP servers and standard repository structure that this playbook refers to.
:::

The toolkit lives next to this playbook at `ap2510-aisdlc/aisdlc-toolkit/`. The playbook explains
how and why; the toolkit holds the files the agents read and follow.

| Path | What it holds |
|---|---|
| `repo-template/` | Agents, rules, prompts, templates, scripts, VS Code and Claude Code MCP configuration, Claude Code subagents and commands, and the standard folder layout, copied into each product repository |
| `install.sh` | Installs the template into a product repository; `--update` refreshes toolkit-owned files; `--dry-run` previews |
| `mcp/` | Jira, Confluence and GitLab MCP servers (TypeScript, stdio) |
| `docs/agent-framework/` | Reference documentation for the agent framework: architecture, spec-driven workflow, context management, MCP configuration, Claude Code runtime |

## Install

```bash
cd ap2510-aisdlc/aisdlc-toolkit
(cd mcp && npm install && npm run build)     # once per machine
./install.sh /path/to/product-repo
```

The installer copies every template file that does not exist yet, never overwrites existing files,
replaces the `__TOOLKIT_DIR__` token in `.vscode/mcp.json` and `.mcp.json` with the absolute toolkit
path, and adds `.env`, `.claude/settings.local.json`, `generated_tests/_mcp-artifacts/` and
`__pycache__/` to the repository `.gitignore`.

`./install.sh /path/to/product-repo --update` replaces toolkit-owned files only (`.github/agents`,
`rules`, `prompts`, `templates`, `scripts`, `instructions`, `copilot-instructions.md`, `.claude/agents`,
`.claude/commands` and `CLAUDE.md`) and never touches project-owned files (`.github/contexts/`,
`.vscode/mcp.json`, `.mcp.json`, `docs/`, `requirement/`, `output/`).

## Standard repository structure

```text
<product-repo>/
├── .github/
│   ├── copilot-instructions.md   Repository-wide instructions every agent follows
│   ├── agents/                   Lifecycle agents (*.agent.md)
│   ├── rules/                    Lifecycle governance, PDLC policy, execution gates, standards
│   ├── templates/                Increment card, tailoring record, squad baseline, requirements, user story, QA test case
│   ├── prompts/                  Workflow runbooks (intake-to-spec, intake-to-implementation)
│   ├── instructions/             File-pattern instructions
│   ├── scripts/                  Figma REST pipeline, agent token estimation, Claude Code sync
│   └── contexts/                 Project context (Context Builder writes, Context Updater maintains)
├── .claude/
│   ├── agents/                   Claude Code subagents (generated from .github/agents)
│   └── commands/                 Claude Code slash commands (generated from .github/prompts)
├── .vscode/mcp.json              Playwright, Jira, Confluence and GitLab MCP servers (VS Code)
├── .mcp.json                     The same four MCP servers for Claude Code
├── CLAUDE.md                     Claude Code instructions; imports copilot-instructions.md
├── docs/
│   ├── increments/               Increment cards and lifecycle tailoring records
│   ├── discovery/                Problem framing, personas, journeys, squad baseline
│   ├── brds/                     BRD Builder output
│   ├── prds/                     PRD Builder output
│   └── architecture/decisions/   ADR Creation output
├── requirement/
│   ├── legacy/                   Existing source documents for intake
│   ├── <Project>_<JiraKey>_Requirements.md
│   └── Traceability_Matrix.md    CTX → BRD → FR/NFR → US → SPEC → TASK → CODE → APT/FT/TEST → REVIEW → DOC
├── output/<RUN_ID>/              specify/, plan/, implement/, api-tests/, functional-tests/, review/, docs/
└── generated_tests/              Playwright MCP session artefacts (git-ignored)
```

## Agents

| Agent | Where it comes from | Catalogue |
|---|---|---|
| Context Builder, Context Updater | Toolkit `.github/agents/` | [A.2](/agents/context-builder), [A.11](/agents/supporting-agents#context-updater) |
| BRD Builder, PRD Builder | HVE Core All extension | [A.3.1](/agents/brd-builder), [A.3.2](/agents/prd-builder) |
| ADR Creation, Arch Diagram Builder | HVE Core All extension | Phase 4 on the [greenfield path](/paths/greenfield#4-design-experience-and-architecture) |
| Jira / ADO Backlog Manager | HVE Core All extension | [A.4](/agents/backlog-manager) |
| Technical Specifier (Spec-Clarify) | Toolkit `specify.agent.md` | [A.5](/agents/spec-clarify) |
| Implementation Planner (Task-Planner) | Toolkit `planner.agent.md` | [A.6](/agents/task-planner) |
| Implementation Builder (Task-Implementor) | Toolkit `implement.agent.md` | [A.7](/agents/task-implementor) |
| API Tester | Toolkit `api-tester.agent.md` | [A.8](/agents/api-testing) |
| Functional Automation Test | Toolkit `functional-automation-test.agent.md` | [A.9](/agents/functional-testing) |
| QA Test Case Generator | Toolkit `qa-test-case-generator.agent.md` | [A.11](/agents/supporting-agents#qa-test-case-generator) |
| Compliance Reviewer (Code Review) | Toolkit `reviewer.agent.md`; HVE Core Code Review for pull requests | [A.11](/agents/supporting-agents#compliance-reviewer) |
| Technical Documenter, Traceability Manager, Figma Extractor | Toolkit `.github/agents/` | [A.11](/agents/supporting-agents) |
| Azure Deploy (`azure-prepare`, `azure-validate`, `azure-deploy`) | HVE Core All extension | [A.10](/agents/azure-deploy) |

### Claude Code

The twelve toolkit agents also install as Claude Code subagents in `.claude/agents/`, with kebab-case
names: `api-tester`, `compliance-reviewer`, `context-builder`, `context-updater`, `figma-extractor`,
`functional-automation-test`, `implementation-builder`, `implementation-planner`,
`qa-test-case-generator`, `technical-documenter`, `technical-specifier` and `traceability-manager`.
Pick one from the `@` typeahead, type `@agent-<name>`, or name it in a prompt. The prompt runbooks
install as `/intake-to-spec` and `/intake-to-implementation`.

The Claude Code files are generated from the same `.agent.md` and `.prompt.md` sources:

```bash
node .github/scripts/sync-claude-agents.mjs           # regenerate
node .github/scripts/sync-claude-agents.mjs --check   # CI drift check
```

HVE Core planning agents remain a VS Code extension and do not appear in Claude Code; see
[4.1a Run the agents in Claude Code](/getting-started/claude-code).

## Rules

| Rule file | What it governs |
|---|---|
| `lifecycle-governance.md` | Playbook paths, bounded increments, lifecycle tailoring and the human approval gates |
| `pdlc.md` | Stage flow, human checkpoints, Compliance Reviewer severity policy, quality gates, stop conditions, output directories |
| `requirement-standards.md` | Canonical requirement structure and IDs (`BRD-*`, `FR-*`, `NFR-*`, `AC-*`, `BR-*`, `INT-*`, `ERR-*`) |
| `traceability-standards.md` | The required ID chain and the traceability matrix |
| `specification-execution-gates.md`, `planning-execution-gates.md`, `implementation-execution-gates.md` | Hard gates for each stage |
| `architectural-standards.md`, `security-quality-standards.md`, `environment-standards.md`, `versioning-standards.md` | Engineering standards applied by every agent |
| `mcp-usage-guide.md`, `figma-interactive-selection-guide.md`, `qa-test-case-generator.rules.md` | Tool-specific rules |

## Templates

| Template | Playbook section | Stored at |
|---|---|---|
| `increment-card-template.md` | [2.2 Project type](/overview/project-types), [3.5 Hybrid](/paths/hybrid) | `docs/increments/<id>-<slug>.md` |
| `lifecycle-tailoring-record.md` | [2.4 Tailoring](/overview/tailoring) | `docs/increments/<id>-tailoring.md` |
| `squad-baseline-template.md` | [2.3 Baseline](/overview/baseline) | `docs/discovery/squad-baseline.md` |
| `requirements-input-template.md` | Intake | `requirement/` |
| `user-story-template.md` | [A.4 Backlog Manager](/agents/backlog-manager) | Jira / ADO |
| `qa-test-case-template.md` | [QA Test Case Generator](/agents/supporting-agents#qa-test-case-generator) | `output/test-cases/` |

## MCP servers

| Server | Provider | Used by |
|---|---|---|
| `playwright` | `@playwright/mcp` via `npx` | API Tester, Functional Automation Test |
| `jira` | `mcp/jira` (toolkit) | Technical Specifier (story intake), QA Test Case Generator, Backlog Manager |
| `confluence` | `mcp/confluence` (toolkit) | Context Builder, Context Updater |
| `gitlab` | `mcp/gitlab` (toolkit) | Code review, merge-request and pipeline evidence |

Credentials are requested by VS Code through `promptString` inputs in `.vscode/mcp.json` and stored
encrypted; never commit tokens. Claude Code reads the same servers from `.mcp.json`, taking
credentials from the toolkit server `.env` files or from variables added with `claude mcp add -e`.
The Jira server includes `jira_get_link_types` and `jira_create_issue_link` so that approved test
cases can be linked to their story. Configuration for Copilot CLI and Claude Code is in the
toolkit's `mcp/README.md`.

## Maintaining the toolkit

* Edit agents, rules, prompts and templates under `repo-template/.github/`; product repositories
  take the change with `./install.sh <repo> --update`.
* After editing an `.agent.md` or `.prompt.md` source, regenerate the Claude Code files with
  `node .github/scripts/sync-claude-agents.mjs` and commit both sides.
* Edit MCP servers under `mcp/<server>/src/` and run `npm run build` in `mcp/`.
* Keep this playbook in step: the [agent catalogue](/agents/catalogue) and
  [getting-started](/getting-started/overview) pages describe these files.
