---
title: SCBX AI-First SDLC Toolkit
description: "Agents, rules, templates, MCP servers and the standard repository structure that product squads install to run the SCBX AI-First SDLC Playbook"
---

Everything a product squad installs to run the
[SCBX AI-First SDLC Playbook](../aisdlc-playbook/README.md): the lifecycle agents, the rules and
templates they follow, the MCP servers they call, and the standard repository structure that keeps
context, requirements, run output and traceability in predictable places. The same agent sources
install for **GitHub Copilot in VS Code** and for **Claude Code**; the playbook explains *how and
why*, this toolkit holds *the files the agents read and follow*.

| Path                  | What it holds                                                                                  | Where it goes                                           |
|-----------------------|------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| `repo-template/`      | Agents, rules, prompts, templates, scripts, VS Code and Claude Code MCP configuration, Claude Code subagents and commands, and the standard folder layout | Copied into each product repository by `install.sh`     |
| `install.sh`          | Installs the template into a product repository; `--update` refreshes toolkit-owned files      | Run from this folder                                    |
| `mcp/`                | Jira, Confluence and GitLab MCP servers (TypeScript, stdio)                                    | Built once per developer machine; see [mcp/README.md](mcp/README.md) |
| `docs/agent-framework/` | Reference documentation for the agent framework: architecture, spec-driven workflow, context management, MCP configuration, Claude Code runtime | Read by toolkit maintainers and FDEs |

## Prerequisites

* VS Code with GitHub Copilot (Agent mode) and the **HVE Core All** extension (pre-release) for
  the planning agents: BRD Builder, PRD Builder, ADR Creation, Jira/ADO Backlog Manager, Code
  Review and Azure Deploy. The toolkit agents below cover context, specification, planning,
  implementation, testing, review, documentation and traceability.
* Or Claude Code (terminal or desktop app) to run the twelve toolkit agents as subagents. The
  HVE Core planning agents are a VS Code extension and do not appear in Claude Code; see
  [docs/agent-framework/CLAUDE_CODE.md](docs/agent-framework/CLAUDE_CODE.md).
* Node.js 20.12 or later (`node -v`) for the MCP servers and Playwright.
* Python 3.11 or later if the squad uses the Figma scripts in `.github/scripts/`.
* Jira, Confluence and GitLab access tokens for the servers the squad uses.

## Install into a product repository

```bash
cd ap2510-aisdlc/aisdlc-toolkit

# 1. Build the MCP servers once per machine
(cd mcp && npm install && npm run build)

# 2. Install the template into the product repository
./install.sh /path/to/product-repo
```

`install.sh` copies every template file that does not exist yet, never overwrites existing files,
replaces the `__TOOLKIT_DIR__` token in `.vscode/mcp.json` and `.mcp.json` with the absolute path of
this toolkit, and adds `.env`, `.claude/settings.local.json`, `generated_tests/_mcp-artifacts/` and
`__pycache__/` to the repository `.gitignore`. Use `--dry-run` to preview.

To take a newer toolkit version later:

```bash
./install.sh /path/to/product-repo --update
```

`--update` replaces toolkit-owned files only: `.github/agents`, `.github/rules`, `.github/prompts`,
`.github/templates`, `.github/scripts`, `.github/instructions`, `.github/copilot-instructions.md`,
`.claude/agents`, `.claude/commands` and `CLAUDE.md`. It never touches project-owned files:
`.github/contexts/`, `.vscode/mcp.json`, `.mcp.json`, `docs/`, `requirement/`, `output/` and
`.gitignore`.

Then open the repository in VS Code, start the MCP servers (**MCP: List Servers**), create the
increment card (`docs/increments/`, from `.github/templates/increment-card-template.md`) and start
**Context Builder** from the Copilot agent picker.

To use the same agents in Claude Code, open the repository with `claude` and pick a subagent from the
`@` typeahead (or type `@agent-<name>`), and run `/mcp` to confirm the four servers. Stage names and
tool mapping are in [docs/agent-framework/CLAUDE_CODE.md](docs/agent-framework/CLAUDE_CODE.md).

## Product repository layout after install

```text
<product-repo>/
├── .github/
│   ├── copilot-instructions.md   Repository-wide instructions every agent follows
│   ├── agents/                   Lifecycle agents (*.agent.md)
│   ├── rules/                    Lifecycle governance, PDLC policy, execution gates, standards
│   ├── templates/                Increment card, tailoring record, squad baseline, requirements, user story, QA test case
│   ├── prompts/                  Workflow runbooks (intake-to-spec, intake-to-implementation)
│   ├── instructions/             File-pattern instructions (QA test case generator)
│   ├── scripts/                  Figma REST pipeline, agent token estimation, Claude Code sync
│   └── contexts/                 Project context written by Context Builder, maintained by Context Updater
├── .claude/
│   ├── agents/                   Claude Code subagents (generated from .github/agents)
│   └── commands/                 Claude Code slash commands (generated from .github/prompts)
├── .vscode/mcp.json              Playwright, Jira, Confluence and GitLab MCP servers (VS Code)
├── .mcp.json                     The same four MCP servers for Claude Code
├── CLAUDE.md                     Claude Code instructions; imports .github/copilot-instructions.md
├── docs/
│   ├── increments/               Increment cards and lifecycle tailoring records (one per bounded increment)
│   ├── discovery/                Problem framing, personas, journeys, squad baseline
│   ├── brds/                     BRD Builder output
│   ├── prds/                     PRD Builder output
│   └── architecture/decisions/   ADR Creation output
├── requirement/
│   ├── legacy/                   Existing source documents for intake
│   ├── <Project>_<JiraKey>_Requirements.md   Canonical requirement (Technical Specifier input)
│   └── Traceability_Matrix.md    CTX -> BRD -> FR/NFR -> US -> SPEC -> TASK -> CODE -> APT/FT/TEST -> REVIEW -> DOC
├── output/<RUN_ID>/              specify/, plan/, implement/, api-tests/, functional-tests/, review/, docs/
└── generated_tests/              Playwright MCP session artefacts (git-ignored)
```

## Agents

Toolkit agents live in `repo-template/.github/agents/`. Every stage is started by a human, stops
for review and emits `NEXT_STEP`; stage agents are never chained automatically.

| Agent                      | File                                  | Playbook phase                                  | Output                                           |
|----------------------------|---------------------------------------|-------------------------------------------------|--------------------------------------------------|
| Context Builder            | `context-builder.agent.md`            | 2 Contextualise                                 | `.github/contexts/*`, `requirement/Context_*.md` |
| Context Updater            | `context-updater.agent.md`            | 2 Contextualise, 10 Operate and improve         | Updated contexts, `CTX-UPDATE-*`                 |
| Figma Extractor            | `figma-extractor.agent.md`            | 4 Design, 5 Specification (design evidence)     | `output/<RUN_ID>/specify/figma/`                 |
| Technical Specifier        | `specify.agent.md`                    | 5 Create backlog and specification              | `output/<RUN_ID>/specify/spec.md`                |
| Implementation Planner     | `planner.agent.md`                    | 6 Plan and decompose                            | `output/<RUN_ID>/plan/plan.md`, `tasks.md`       |
| Implementation Builder     | `implement.agent.md`                  | 7 Build                                         | Source code, unit tests, implementation evidence |
| API Tester                 | `api-tester.agent.md`                 | 8 Validate (backend APIs)                       | `output/<RUN_ID>/api-tests/attempt-<n>/`         |
| Functional Automation Test | `functional-automation-test.agent.md` | 8 Validate (frontend behaviour)                 | `output/<RUN_ID>/functional-tests/attempt-<n>/`  |
| QA Test Case Generator     | `qa-test-case-generator.agent.md`     | 8 Validate (manual test cases to Jira)          | `output/test-cases/<story-key>/`                 |
| Compliance Reviewer        | `reviewer.agent.md`                   | Spec, plan and code gates (invoked by stage agents) | `REVIEW-*` findings and status               |
| Technical Documenter       | `technical-documenter.agent.md`       | 8 Validate, 9 Release                           | `DOC-*` documentation                            |
| Traceability Manager       | `traceability-manager.agent.md`       | Between phases                                  | `requirement/Traceability_Matrix.md`             |

Planning-stage agents (BRD Builder, PRD Builder, ADR Creation, Jira/ADO Backlog Manager, Code
Review, Azure Deploy) come from the HVE Core All extension and write to `docs/brds/`, `docs/prds/`
and `docs/architecture/decisions/`.

### Claude Code

The twelve agents also install as Claude Code subagents in `.claude/agents/`. Claude Code subagent
names are kebab-case: `api-tester`, `compliance-reviewer`, `context-builder`, `context-updater`,
`figma-extractor`, `functional-automation-test`, `implementation-builder`, `implementation-planner`,
`qa-test-case-generator`, `technical-documenter`, `technical-specifier` and `traceability-manager`.
Pick one from the `@` typeahead, type `@agent-<name>`, or name it in a prompt.

The `.claude/agents/` files are generated from the `.agent.md` sources so both runtimes stay in step:

```bash
node .github/scripts/sync-claude-agents.mjs           # regenerate
node .github/scripts/sync-claude-agents.mjs --check   # CI / pre-commit drift check
```

The same script generates `/intake-to-spec` and `/intake-to-implementation` in
`.claude/commands/` from `.github/prompts/`. Each generated file carries a marker naming its source;
never edit it directly. `agent-frontmatter-reference.md` explains the agent file format for anyone
adding an agent; [docs/agent-framework/CLAUDE_CODE.md](docs/agent-framework/CLAUDE_CODE.md) explains
the field and tool mapping for Claude Code.

HVE Core planning agents are not available in Claude Code; use Copilot for those stages, or start
the lifecycle at the specification stage when approved requirements already exist.

## Rules, templates and prompts

| Folder       | Files                                                                                                                                                                                                                                                                                                                 |
|--------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `rules/`     | `lifecycle-governance.md` (playbook paths, tailoring, approval gates), `pdlc.md` (stage flow and review policy), `requirement-standards.md`, `traceability-standards.md`, `specification-execution-gates.md`, `planning-execution-gates.md`, `implementation-execution-gates.md`, `architectural-standards.md`, `security-quality-standards.md`, `environment-standards.md`, `versioning-standards.md`, `mcp-usage-guide.md`, `figma-interactive-selection-guide.md`, `qa-test-case-generator.rules.md` |
| `templates/` | `increment-card-template.md`, `lifecycle-tailoring-record.md`, `squad-baseline-template.md`, `requirements-input-template.md`, `user-story-template.md`, `qa-test-case-template.md`                                                                                                                                       |
| `prompts/`   | `intake-to-spec.prompt.md` (existing documents to canonical requirements, stops before specification), `intake-to-implementation.prompt.md` (end to end, one stage per invocation); mirrored as Claude Code commands in `.claude/commands/`                                                                               |
| `CLAUDE.md`  | Claude Code entry point: imports `.github/copilot-instructions.md`, then adds the subagent names, stage discipline, commands and MCP conventions                                                                                                        |

## MCP servers

| Server       | Provider                               | Used by                                                   |
|--------------|----------------------------------------|-----------------------------------------------------------|
| `playwright` | `@playwright/mcp` (npx)                | API Tester, Functional Automation Test                    |
| `jira`       | `mcp/jira` (toolkit)                   | Technical Specifier (story intake), QA Test Case Generator |
| `confluence` | `mcp/confluence` (toolkit)             | Context Builder, Context Updater                          |
| `gitlab`     | `mcp/gitlab` (toolkit)                 | Code review and pipeline evidence                         |

Credentials are requested by VS Code through `promptString` inputs in `.vscode/mcp.json` and stored
encrypted; never commit tokens. Claude Code reads the same servers from `.mcp.json`, taking
credentials from the toolkit server `.env` files or from variables added with `claude mcp add -e`.
The Jira server includes `jira_get_link_types` and `jira_create_issue_link` so the QA Test Case
Generator can link approved test cases to their story. For Copilot CLI and Claude Code
configuration, see [mcp/README.md](mcp/README.md).

## Maintaining the toolkit

* Edit agents, rules, prompts and templates in `repo-template/.github/`. Product repositories take
  the change with `./install.sh <repo> --update`.
* After editing an `.agent.md` or `.prompt.md` file, regenerate the Claude Code files with
  `node .github/scripts/sync-claude-agents.mjs` and commit both sides.
* Edit MCP servers in `mcp/<server>/src/` and run `npm run build` in `mcp/`.
* Keep the [playbook](../aisdlc-playbook/) in step: the agent catalogue and getting-started pages
  describe these files.
