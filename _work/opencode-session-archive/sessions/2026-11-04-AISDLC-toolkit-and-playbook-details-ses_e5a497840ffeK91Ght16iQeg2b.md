# AISDLC toolkit and playbook details

- **Session ID:** `ses_e5a497840ffeK91Ght16iQeg2b`
- **Created:** 2026-11-04 15:39  |  **Last activity:** 2026-11-05 18:56
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `build`
- **Tokens:** 98,400 in / 4,900 out / 1,621 reasoning
- **Messages:** 11

---

### User - 2026-11-04 15:39

give me details on @aisdlc-toolkit-main\  and @aisdlc-playbook-main\

### Assistant - 2026-11-04 15:39 | opencode-go/deepseek-v4.1-flash | build

I'll explore both directories to give you a detailed overview.

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\README.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\README.md, lines 1-144
1: ---
2: title: SCBX AI-First SDLC Toolkit
3: description: "Agents, rules, templates, MCP servers and the standard repository structure that product squads install to run the SCBX AI-First SDLC Playbook"
4: ---
5: 
6: Everything a product squad installs to run the
7: [SCBX AI-First SDLC Playbook](../aisdlc-playbook/README.md): the lifecycle agents, the rules and
8: templates they follow, the MCP servers they call, and the standard repository structure that keeps
9: context, requirements, run output and traceability in predictable places.
10: 
11: The playbook explains *how and why*; this toolkit holds *the files the agents read and follow*.
12: 
13: | Path                  | What it holds                                                                                  | Where it goes                                           |
14: |-----------------------|------------------------------------------------------------------------------------------------|---------------------------------------------------------|
15: | `repo-template/`      | Agents, rules, prompts, templates, scripts, workspace MCP config and the standard folder layout | Copied into each product repository by `install.sh`     |
16: | `install.sh`          | Installs the template into a product repository; `--update` refreshes toolkit-owned files      | Run from this folder                                    |
17: | `mcp/`                | Jira, Confluence and GitLab MCP servers (TypeScript, stdio)                                    | Built once per developer machine; see [mcp/README.md](mcp/README.md) |
18: | `docs/agent-framework/` | Reference documentation for the agent framework: architecture, spec-driven workflow, context management, MCP configuration | Read by toolkit maintainers and FDEs |
19: 
20: ## Prerequisites
21: 
22: * VS Code with GitHub Copilot (Agent mode) and the **HVE Core All** extension (pre-release) for
23:   the planning agents: BRD Builder, PRD Builder, ADR Creation, Jira/ADO Backlog Manager, Code
24:   Review and Azure Deploy. The toolkit agents below cover context, specification, planning,
25:   implementation, testing, review, documentation and traceability.
26: * Node.js 20.12 or later (`node -v`) for the MCP servers and Playwright.
27: * Python 3.11 or later if the squad uses the Figma scripts in `.github/scripts/`.
28: * Jira, Confluence and GitL
... truncated (12,338 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\README.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\README.md, lines 1-46
1: ---
2: title: SCBX AI-First SDLC Playbook (site)
3: description: "Docusaurus site for the SCBX AI-First SDLC Playbook with clickable draw.io diagrams; how to run, build and edit it"
4: ---
5: 
6: The interactive playbook for product squads delivering with Agentic PDLC, built from the
7: *SCBx AI PDLC Product Squad Playbook* draft (sections 1 to 5 and Appendix A). The agents, rules,
8: templates and MCP servers it refers to live in the toolkit one folder up (`../aisdlc-toolkit`).
9: 
10: * **Docs** are Markdown under `docs/`; the sidebar is `sidebars.js`.
11: * **Diagrams** are draw.io files under `diagrams/` (the editable source). `npm run diagrams` exports
12:   them to `static/diagrams/*.svg` with the diagram embedded, so the SVG itself can be opened in
13:   draw.io, and with the hyperlinks kept. Shapes link to playbook pages and sections. Edit the
14:   `.drawio`, re-export, commit both.
15: * **Site** is Docusaurus 3.
16: 
17: ```bash
18: cd ap2510-aisdlc/aisdlc-playbook
19: npm install
20: npm run build      # static site in build/
21: npm run diagrams   # re-export the SVGs after editing a .drawio
22: npm start          # http://localhost:3000
23: ```
24: 
25: `npm run diagrams` uses the draw.io desktop app when it is installed and otherwise the bundled
26: renderer in `diagrams/render.mjs`, which covers the shapes used by these diagrams.
27: 
28: To publish under a sub-path, set `url` and `baseUrl` in `docusaurus.config.js` and prefix the links
29: in the diagrams (they are absolute site paths such as `/overview/tailoring`).
30: 
31: ## Structure
32: 
33: ```text
34: docs/
35: ├── intro.md                 About this playbook
36: ├── introduction/            1. What Agentic PDLC means, four changes, the lifecycle
37: ├── overview/                2. End-to-end flow, project types, baseline, tailoring, select agents
38: ├── paths/                   3. Greenfield, brownfield, modernisation, hybrid
39: ├── getting-started/         4. Environment, BRD, PRD, backlog, specify, plan, implement, API and functional tests
40: ├── roles/                   5. Squad roles and role evolution
41: ├── agents/                  Appendix A. Agent catalogue
42: ├── toolkit.md               The toolkit and the standard repository structure
43: └── diagrams.md              How the diagrams are made and edited
44: diagrams/                    *.drawio 
... truncated (2,613 chars total)
```

### Assistant - 2026-11-04 15:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me explore the structures more.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\" | Select-Object -ExpandProperty FullName"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\.gitignore
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\install.sh
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\README.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\AGENTS_GUIDE.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\AGENTS_SETUP.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\ARCHITECTURE.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\CONTEXT_MANAGEMENT_GUIDE.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\CONTEXT_MANAGEMENT_IMPLEMENTATION_SUMMARY.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\CONTEXT_MANAGEMENT_QUICKSTART.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\CONTEXT_MANAGEMENT_VERIFICATION_CHECKLIST.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\MCP_CONFIGURATION.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\MCP_QUICK_START.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\SPEC_DRIVEN_WORKFLOW.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\.gitignore
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\package-lock.json
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\package.json
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\README.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\tsconfig.base.json
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\confluence\.env.example
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\confluence\package.json
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\m
... truncated (11,657 chars total)
```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Recurse -File \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\" | Where-Object { $_.FullName -notmatch 'node_modules' } | Select-Object -ExpandProperty FullName"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\.gitignore
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docusaurus.config.js
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\package-lock.json
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\package.json
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\README.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\sidebars.js
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\diagrams\agent-chain.drawio
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\diagrams\end-to-end-flow.drawio
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\diagrams\export.sh
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\diagrams\lifecycle-paths.drawio
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\diagrams\render.mjs
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\diagrams\stage-run.drawio
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\diagrams.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\intro.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\toolkit.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\api-testing.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\azure-deploy.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\backlog-manager.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\brd-builder.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\catalogue.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\context-builder.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\functional-testing.md
C:\Users\SahilMore\Downloads\Recovery Workbench Sh
... truncated (7,239 chars total)
```

### Assistant - 2026-11-04 15:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read key files: install.sh, copilot-instructions.md, lifecycle-governance.md, pdlc.md, docusaurus.config.js, sidebars.js, package.json, and playbook intro/toolkit.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\install.sh"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\install.sh, lines 1-117
1: #!/usr/bin/env bash
2: #
3: # install.sh - Install or update the SCBX AI-First SDLC toolkit in a product repository.
4: #
5: # Copies repo-template/ (agents, rules, prompts, templates, scripts, contexts folder,
6: # workspace MCP configuration and the standard folder structure) into a product
7: # repository and points the Jira, Confluence and GitLab MCP servers at this toolkit.
8: #
9: # Usage:
10: #   ./install.sh <product-repo>            install; existing files are never overwritten
11: #   ./install.sh <product-repo> --update   also replace toolkit-owned files with this version
12: #   ./install.sh <product-repo> --dry-run  show what would be done
13: #
14: # Toolkit-owned files (replaced by --update): .github/agents, .github/rules,
15: # .github/prompts, .github/templates, .github/scripts, .github/instructions,
16: # .github/copilot-instructions.md.
17: # Project-owned files (never overwritten): .github/contexts, .vscode/mcp.json,
18: # docs, requirement, output, .gitignore.
19: 
20: set -euo pipefail
21: 
22: SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
23: readonly SCRIPT_DIR
24: readonly TEMPLATE_DIR="${SCRIPT_DIR}/repo-template"
25: readonly GITIGNORE_ENTRIES=(".env" "generated_tests/_mcp-artifacts/" "__pycache__/")
26: 
27: usage() {
28:   sed -n '9,19p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
29: }
30: 
31: log() {
32:   printf "%s\n" "$*"
33: }
34: 
35: err() {
36:   printf "ERROR: %s\n" "$1" >&2
37:   exit 1
38: }
39: 
40: is_toolkit_owned() {
41:   case "$1" in
42:     .github/agents/* | .github/rules/* | .github/prompts/* | .github/templates/* | \
43:       .github/scripts/* | .github/instructions/* | .github/copilot-instructions.md)
44:       return 0 ;;
45:     *)
46:       return 1 ;;
47:   esac
48: }
49: 
50: main() {
51:   local target="" update=false dry_run=false
52:   for arg in "$@"; do
53:     case "$arg" in
54:       --update) update=true ;;
55:       --dry-run) dry_run=true ;;
56:       -h | --help) usage; exit 0 ;;
57:       -*) err "Unknown option: $arg" ;;
58:       *) target="$arg" ;;
59:     esac
60:   done
61:   [[ -n "$target" ]] || { usage; err "Missing <product-repo>"; }
62:   [[ -d "$target" ]] || err "Target is not a directory: $target"
63:   [[ -d "$TEMPLATE_DIR" ]] || err "repo-template not found next to install.sh"
64: 
65:   target="$(cd "$target" && pwd)"
66:   local copied=
... truncated (4,520 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\repo-template\\.github\\copilot-instructions.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\copilot-instructions.md, lines 1-131
1: # Copilot Instructions - Spec-Driven Development
2: 
3: This repository uses a spec-driven PDLC workflow for software development.
4: 
5: ## Default Behavior
6: - Prefer the agents in `.github/agents/`.
7: - Follow centralized rules in `.github/rules/`.
8: - Use templates in `.github/templates/`.
9: - Preserve traceability through every artifact.
10: - Treat GitHub issues, branches, commits, and pull requests as trace metadata when available.
11: 
12: ## SCBX AI-First SDLC Playbook
13: This repository follows the SCBX AI-First SDLC Playbook. Increment-level governance (project
14: path, lifecycle tailoring, human approval gates) is defined in `.github/rules/lifecycle-governance.md`.
15: Every bounded increment has an increment card and a lifecycle tailoring record in `docs/increments/`
16: (templates: `.github/templates/increment-card-template.md`,
17: `.github/templates/lifecycle-tailoring-record.md`). Agents read the increment card to understand the
18: selected path, reused artefacts and approval status before producing output.
19: 
20: ## Context Management (Prerequisite for All Workflows)
21: 
22: **Context creation and maintenance is foundational to all PDLC workflows.**
23: 
24: ### Context Loading For Every Agent
25: 
26: Before starting a task, every agent must inspect `.github/contexts/` and read the files relevant to its scope. Keep using the existing context filenames, and also consider any additional files added to the folder. Read explicitly designated Word/PDF context files as well as Markdown files; use the project-context index when available. Do not load unrelated files. Treat context as guidance alongside task requirements and current source evidence. Context Builder creates new context only, Context Updater owns context maintenance, and other agents must not modify context files unless explicitly assigned that work.
27: 
28: ### Initial Context Setup
29: For new projects or when context does not exist, use a single unified agent:
30: 
31: ```text
32: Context Builder (Unified - Merged)
33:   → Uses a Confluence link when provided; otherwise uses attached Word/PDF documents
34:   → Inspects available legacy project documentation, source code, configuration, and tests
35:   → Extracts tech stack from source code (package.json, config files, folder structure)
36:   → Gathers business 
... truncated (8,965 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\mcp\\README.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\mcp\README.md, lines 1-463
1: ---
2: title: Team MCP Servers
3: description: Shared Model Context Protocol (MCP) servers for Jira, Confluence, and GitLab, with setup steps for GitHub Copilot and Claude Code
4: ---
5: 
6: ## Overview
7: 
8: This folder holds MCP servers the team can share instead of building their own. Each server lives in
9: its own subfolder and runs locally over stdio, so it works with any MCP client.
10: 
11: | Server       | Folder        | What it can do                                                                                    |
12: |--------------|---------------|---------------------------------------------------------------------------------------------------|
13: | `jira`       | `jira/`       | Search (JQL), read, create, update, comment, transition, link issues; list projects, fields, users |
14: | `confluence` | `confluence/` | Search (CQL), read, create, update (replace/append/prepend) pages; comment; list spaces, children |
15: | `gitlab`     | `gitlab/`     | Projects, files, branches, commits, issues, merge requests (incl. diffs), pipelines and job logs  |
16: 
17: The Jira and Confluence servers support Atlassian **Cloud** (`*.atlassian.net`) and
18: **Server / Data Center**. The GitLab server targets **self-managed (on-prem) GitLab** through REST
19: API v4, and also works with GitLab.com.
20: 
21: ### Jira tools
22: 
23: | Tool                       | Purpose                                                        |
24: |----------------------------|----------------------------------------------------------------|
25: | `jira_search_issues`       | Search with JQL                                                |
26: | `jira_get_issue`           | Get an issue with description, subtasks, links, comments       |
27: | `jira_create_issue`        | Create an issue (Story, Task, Bug, Epic, Sub-task, ...)        |
28: | `jira_update_issue`        | Update summary, description, labels, assignee, custom fields   |
29: | `jira_add_comment`         | Add a comment                                                  |
30: | `jira_get_transitions`     | List the status changes available for an issue                 |
31: | `jira_transition_issue`    | Change status (for example to "In Progress" or "Done")         |
32: | `jira_list_projects`       | List projects                                                  |
33: | `jira_get_cre
... truncated (22,632 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\docs\\intro.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\intro.md, lines 1-64
1: ---
2: id: intro
3: title: SCBX AI-First SDLC Playbook
4: description: "Overview and intended audience. Draft, October 2026."
5: slug: /
6: sidebar_position: 0
7: sidebar_label: About this playbook
8: ---
9: 
10: :::note Section summary
11: Overview and intended audience. Draft, October 2026.
12: :::
13: 
14: This playbook helps product squads use **Agentic PDLC** in a consistent, practical and controlled way.
15: It is written for the people shaping products, translating needs into specifications, designing
16: solutions, building and testing software, deploying releases and operating services in production.
17: 
18: It is designed to answer straightforward questions:
19: 
20: | Question | Where to look |
21: |---|---|
22: | What is Agentic PDLC and what changes in the way the squad works? | [1. Introduction](/introduction/what-is-agentic-pdlc) |
23: | What steps should I follow to adopt Agentic PDLC as my primary delivery approach? | [2. Overview](/overview/end-to-end-flow), [4. Getting started](/getting-started/overview) |
24: | What delivery path applies to my increment? | [2.2 Identify the project type](/overview/project-types), [3. Project paths](/paths/overview) |
25: | Which lifecycle activities and agents are relevant for my project type? How do I adapt for Greenfield and Brownfield? | [2.4 Tailor lifecycle activities](/overview/tailoring), [2.5 Select relevant agents](/overview/select-agents) |
26: | What must be prepared, reviewed and approved? | [Human approval gates](/overview/end-to-end-flow#human-approval-gates), [Getting started](/getting-started/overview) |
27: | Who remains accountable for each decision and output? | [5. Product squad roles](/roles/squad-roles), [Agent catalogue](/agents/catalogue) |
28: | How does the squad demonstrate value and safe use? | [2.3 Baseline the current state](/overview/baseline), [Lifecycle tailoring controls](/overview/tailoring#mandatory-controls-remain-in-place) |
29: 
30: ## How to read it
31: 
32: The playbook is interactive. Diagrams are clickable: select a stage, a gate or an agent in any
33: diagram to open the page that explains it. Start with the
34: [end-to-end flow](/overview/end-to-end-flow), then follow your project path.
35: 
36: ```text
37: Introduction  →  Overview  →  Project paths  →  Getting started  →  Roles  →  Agent catalogue
38:  (why)           (lifecycle,  
... truncated (3,807 chars total)
```

### Assistant - 2026-11-04 15:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read more key files: lifecycle-governance.md, pdlc.md, sidebars.js, docusaurus.config.js, package.json, playbook toolkit.md, and agent catalogue maybe. Also read the agent framework architecture doc.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\repo-template\\.github\\rules\\lifecycle-governance.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\rules\lifecycle-governance.md, lines 1-81
1: ---
2: description: Lifecycle governance for the SCBX AI-First SDLC - standard lifecycle, project paths, tailoring and human approval gates.
3: ---
4: 
5: # Lifecycle Governance
6: 
7: These rules apply the SCBX AI-First SDLC Playbook to every bounded increment delivered with the
8: agents in this repository. They complement `pdlc.md` (stage-level review policy) with the
9: increment-level controls the playbook requires.
10: 
11: ## Standard lifecycle
12: 
13: ```text
14: 0 Mobilise and assess -> 1 Discover and frame -> 2 Contextualise -> 3 Define requirements
15: -> 4 Design experience and architecture -> 5 Create backlog and specification
16: -> 6 Plan and decompose -> 7 Build -> 8 Validate -> 9 Release -> 10 Operate and improve
17: ```
18: 
19: ## Bounded increments
20: 
21: * Classify the bounded increment, not the programme: Greenfield development, Brownfield enhancement
22:   or Modernisation & upgrade. A programme may contain several paths; each increment records its own.
23: * Every increment has an increment card (`.github/templates/increment-card-template.md`) in
24:   `docs/increments/` before any agent is started.
25: * Every increment has a lifecycle tailoring record
26:   (`.github/templates/lifecycle-tailoring-record.md`). Phases are Mandatory, Conditional,
27:   Reusable, Skippable with evidence or Not applicable.
28: * Where a phase is skipped or an artefact is reused, record the reason, the approved artefact, its
29:   owner, version or link, the approving authority, the risk created and the downstream controls.
30:   Reused artefacts must be confirmed suitable for the increment, versioned and linked to it.
31: 
32: ## Path emphasis
33: 
34: | Path          | Contextualise                                          | Define requirements                                                    |
35: |---------------|--------------------------------------------------------|------------------------------------------------------------------------|
36: | Greenfield    | Enterprise, domain, project and engineering context    | BRD and PRD from approved discovery outputs; business, product, architecture approval |
37: | Brownfield    | Existing requirements, architecture, APIs, dependencies, code, decisions, incidents, technical debt | Start from the approved change; clarify and update accept
... truncated (5,989 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\sidebars.js"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\sidebars.js, lines 1-68
1: // @ts-check
2: /** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
3: const sidebars = {
4:   playbook: [
5:     'intro',
6:     {
7:       type: 'category',
8:       label: '1. Introduction to Agentic PDLC',
9:       link: { type: 'doc', id: 'introduction/what-is-agentic-pdlc' },
10:       items: ['introduction/four-changes', 'introduction/lifecycle'],
11:     },
12:     {
13:       type: 'category',
14:       label: '2. Overview of Agentic PDLC',
15:       link: { type: 'doc', id: 'overview/end-to-end-flow' },
16:       items: ['overview/project-types', 'overview/baseline', 'overview/tailoring', 'overview/select-agents'],
17:     },
18:     {
19:       type: 'category',
20:       label: '3. Execute in different project types',
21:       link: { type: 'doc', id: 'paths/overview' },
22:       items: ['paths/greenfield', 'paths/brownfield', 'paths/modernisation', 'paths/hybrid'],
23:     },
24:     {
25:       type: 'category',
26:       label: '4. Pilot pre-initiation and getting started',
27:       link: { type: 'doc', id: 'getting-started/overview' },
28:       items: [
29:         'getting-started/environment',
30:         'getting-started/brd',
31:         'getting-started/prd',
32:         'getting-started/backlog',
33:         'getting-started/specify',
34:         'getting-started/plan',
35:         'getting-started/implement',
36:         'getting-started/api-tests',
37:         'getting-started/functional-tests',
38:       ],
39:     },
40:     {
41:       type: 'category',
42:       label: '5. Product squad roles',
43:       link: { type: 'doc', id: 'roles/squad-roles' },
44:       items: ['roles/role-evolution'],
45:     },
46:     {
47:       type: 'category',
48:       label: 'Appendix A. Agent catalogue',
49:       link: { type: 'doc', id: 'agents/catalogue' },
50:       items: [
51:         'agents/context-builder',
52:         'agents/brd-builder',
53:         'agents/prd-builder',
54:         'agents/backlog-manager',
55:         'agents/spec-clarify',
56:         'agents/task-planner',
57:         'agents/task-implementor',
58:         'agents/api-testing',
59:         'agents/functional-testing',
60:         'agents/azure-deploy',
61:         'agents/supporting-agents',
62:       ],
63:     },
64:     'toolkit',
65:     'diagrams',
66:   ],
67: };
68: export default sidebars;
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\docusaurus.config.js"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docusaurus.config.js, lines 1-77
1: // @ts-check
2: // SCBX AI-First SDLC Playbook. Serve locally with `npm start`, build with `npm run build`.
3: // If the site is published under a sub-path, change `url` and `baseUrl` and re-export the diagrams
4: // (their links are absolute site paths: see diagrams/export.sh).
5: 
6: /** @type {import('@docusaurus/types').Config} */
7: const config = {
8:   title: 'SCBX AI-First SDLC Playbook',
9:   tagline: 'How product squads deliver with agents across the lifecycle, with people accountable at every gate',
10:   favicon: 'img/favicon.svg',
11:   url: 'https://aisdlc-playbook.scbx.internal',
12:   baseUrl: '/',
13:   onBrokenLinks: 'throw',
14:   onBrokenAnchors: 'throw',
15:   markdown: { hooks: { onBrokenMarkdownLinks: 'throw' } },
16:   i18n: { defaultLocale: 'en', locales: ['en'] },
17:   presets: [
18:     [
19:       'classic',
20:       /** @type {import('@docusaurus/preset-classic').Options} */
21:       ({
22:         docs: {
23:           routeBasePath: '/',
24:           sidebarPath: './sidebars.js',
25:           editUrl: undefined,
26:           showLastUpdateTime: false,
27:         },
28:         blog: false,
29:         theme: { customCss: './src/css/custom.css' },
30:       }),
31:     ],
32:   ],
33:   themeConfig:
34:     /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
35:     ({
36:       colorMode: { respectPrefersColorScheme: true },
37:       docs: { sidebar: { hideable: true, autoCollapseCategories: false } },
38:       navbar: {
39:         title: 'SCBX AI-First SDLC Playbook',
40:         items: [
41:           { to: '/', label: 'Playbook', position: 'left' },
42:           { to: '/overview/end-to-end-flow', label: 'Lifecycle', position: 'left' },
43:           { to: '/paths/overview', label: 'Project paths', position: 'left' },
44:           { to: '/getting-started/overview', label: 'Getting started', position: 'left' },
45:           { to: '/agents/catalogue', label: 'Agent catalogue', position: 'left' },
46:           { to: '/toolkit', label: 'Toolkit', position: 'right' },
47:           { to: '/diagrams', label: 'Diagrams', position: 'right' },
48:         ],
49:       },
50:       footer: {
51:         style: 'dark',
52:         links: [
53:           {
54:             title: 'Playbook',
55:             items: [
56:               { label: 'Introduction', to: '/introduction/wh
... truncated (3,391 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\package.json"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\package.json, lines 1-22
1: {
2:   "name": "scbx-aisdlc-playbook",
3:   "version": "0.1.0",
4:   "private": true,
5:   "description": "SCBX AI-First SDLC Playbook: how product squads deliver with agents across the lifecycle. Built with Docusaurus.",
6:   "scripts": {
7:     "start": "docusaurus start",
8:     "build": "docusaurus build",
9:     "serve": "docusaurus serve",
10:     "clear": "docusaurus clear",
11:     "diagrams": "sh diagrams/export.sh"
12:   },
13:   "dependencies": {
14:     "@docusaurus/core": "3.10.2",
15:     "@docusaurus/preset-classic": "3.10.2",
16:     "@mdx-js/react": "^3.0.0",
17:     "prism-react-renderer": "^2.3.0",
18:     "react": "^19.0.0",
19:     "react-dom": "^19.0.0"
20:   },
21:   "engines": { "node": ">=20.0" }
22: }
```

### Assistant - 2026-11-04 15:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me read a few more: playbook toolkit.md, agent catalogue, pdlc.md, and an agent file to show structure. Also the agent-framework ARCHITECTURE.md. And maybe the lifecycle.md for phases.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\docs\\toolkit.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\toolkit.md, lines 1-128
1: ---
2: id: toolkit
3: title: Toolkit
4: description: "The agents, rules, templates, MCP servers and standard repository structure that this playbook refers to."
5: sidebar_label: Toolkit
6: ---
7: 
8: :::note Section summary
9: The agents, rules, templates, MCP servers and standard repository structure that this playbook refers to.
10: :::
11: 
12: The toolkit lives next to this playbook at `ap2510-aisdlc/aisdlc-toolkit/`. The playbook explains
13: how and why; the toolkit holds the files the agents read and follow.
14: 
15: | Path | What it holds |
16: |---|---|
17: | `repo-template/` | Agents, rules, prompts, templates, scripts, workspace MCP configuration and the standard folder layout, copied into each product repository |
18: | `install.sh` | Installs the template into a product repository; `--update` refreshes toolkit-owned files; `--dry-run` previews |
19: | `mcp/` | Jira, Confluence and GitLab MCP servers (TypeScript, stdio) |
20: | `docs/agent-framework/` | Reference documentation for the agent framework: architecture, spec-driven workflow, context management, MCP configuration |
21: 
22: ## Install
23: 
24: ```bash
25: cd ap2510-aisdlc/aisdlc-toolkit
26: (cd mcp && npm install && npm run build)     # once per machine
27: ./install.sh /path/to/product-repo
28: ```
29: 
30: The installer copies every template file that does not exist yet, never overwrites existing files,
31: replaces the `__TOOLKIT_DIR__` token in `.vscode/mcp.json` with the absolute toolkit path, and adds
32: `.env`, `generated_tests/_mcp-artifacts/` and `__pycache__/` to the repository `.gitignore`.
33: 
34: `./install.sh /path/to/product-repo --update` replaces toolkit-owned files only (`.github/agents`,
35: `rules`, `prompts`, `templates`, `scripts`, `instructions`, `copilot-instructions.md`) and never
36: touches project-owned files (`.github/contexts/`, `.vscode/mcp.json`, `docs/`, `requirement/`,
37: `output/`).
38: 
39: ## Standard repository structure
40: 
41: ```text
42: <product-repo>/
43: ├── .github/
44: │   ├── copilot-instructions.md   Repository-wide instructions every agent follows
45: │   ├── agents/                   Lifecycle agents (*.agent.md)
46: │   ├── rules/                    Lifecycle governance, PDLC policy, execution gates, standards
47: │   ├── templates/                Increment card, tailoring record, squad baseline, requ
... truncated (8,547 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\repo-template\\.github\\rules\\pdlc.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\rules\pdlc.md, lines 1-60
1: ---
2: description: PDLC rules for spec-driven workflows.
3: ---
4: 
5: # PDLC Standards
6: 
7: ## Flow
8: 
9: ```text
10: Context -> BRD -> Requirements -> Spec -> Plan -> Implement -> Test -> Review -> Document -> Trace
11: ```
12: 
13: For existing documents:
14: 
15: ```text
16: Intake -> Gap Report -> Consolidated Requirements -> Spec -> Plan -> Implement
17: ```
18: 
19: ## Human Checkpoints
20: - Every PDLC stage is human-initiated. Each stage agent produces its output, stops, and emits `NEXT_STEP`; the human reviews the output and manually starts the next stage.
21: - Technical Specifier, Implementation Planner, and Technical Documenter automatically invoke Compliance Reviewer at the spec, plan, and post-test code gates, respectively. These bounded reviews do not start the next stage.
22: - Critical, High, and Medium review findings block the handoff. Keep the review status as `FAIL`, make every finding visible, and stop until a human records remediation or explicit acceptance. After remediation, rerun the review before continuing; an explicitly accepted finding must remain visible in the handoff.
23: - A finding that causes review failure must remain `FAIL` regardless of severity; severity controls blocking, not the reported status. Low-severity findings do not automatically block the handoff. If a review has only Low findings, preserve its `FAIL` status and emit `REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.` Keep all findings visible for human disposition.
24: - Review status and automatic stop policy are separate: never relabel a `FAIL` as `PASS` merely because its findings do not block the handoff. If findings have mixed severities, apply the highest-severity outcome; any Critical, High, or Medium finding blocks.
25: - Independent stage hard gates still block completion, including failed required unit tests or coverage below 80%. A nonblocking review result cannot override them.
26: - Workflow prompts pause after every step and continue only on explicit human instruction.
27: 
28: > [!WARNING]
29: > Only a review failure containing Low-severity findings and no Critical, High, or Medium findings may proceed with a warning. Critical, High, or Medium findings block the handoff until a hum
... truncated (4,090 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\docs\\agent-framework\\ARCHITECTURE.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\ARCHITECTURE.md, lines 1-42
1: # Copilot Configuration Architecture
2: 
3: ## Structure
4: 
5: ```text
6: .github/
7: ├── agents/
8: ├── instructions/
9: ├── prompts/
10: ├── rules/
11: ├── templates/
12: ├── copilot-instructions.md
13: ├── SPEC_DRIVEN_WORKFLOW.md
14: └── README.md
15: ```
16: 
17: ## Design
18: - Agents define who performs each PDLC role.
19: - Rules define how work must be done.
20: - Instructions apply rules to file patterns.
21: - Templates define canonical artifact shape.
22: - Prompts provide reusable workflow chains.
23: 
24: ## Traceability
25: All major outputs should map:
26: 
27: ```text
28: CTX -> BRD -> FR/NFR -> US -> SPEC -> TASK -> CODE -> TEST -> REVIEW -> DOC
29: ```
30: 
31: ## Banking Domain Scope
32: The configuration is generic for any software system and supports:
33: - Customer onboarding.
34: - KYC and AML.
35: - Risk profiling.
36: - Suitability.
37: - Portfolio view.
38: - Product catalogue.
39: - Advisory recommendations.
40: - Order capture.
41: - Statements and documents.
42: - Alerts and servicing.
```

### Assistant - 2026-11-04 15:39 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Now let me check a couple agent files for their structure/scope, plus the agent catalogue and lifecycle docs. Also, check whether there are any dependencies counts. Let me read the agent catalogue and the lifecycle doc, plus one agent file (specify.agent.md head) and .vscode/mcp.json.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\docs\\agents\\catalogue.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\agents\catalogue.md, lines 1-54
1: ---
2: id: catalogue
3: title: Appendix A. Agent catalogue
4: description: "Agent catalogue: operating contracts for every agent in the chain."
5: sidebar_label: A.1 How to use the catalogue
6: ---
7: 
8: ## A.1 How to use the catalogue
9: 
10: :::note Section summary
11: Agent catalogue: operating contracts for every agent in the chain.
12: :::
13: 
14: The agent catalogue translates the lifecycle into usable delivery components. Each entry explains
15: the activity an agent supports, the context it requires, the output it creates and the human role
16: that reviews or accepts that output. Use the catalogue **after** the squad has
17: [classified the increment](/overview/project-types) and [tailored the lifecycle](/overview/tailoring),
18: so the selected agents correspond to actual delivery needs rather than being added because they are
19: available.
20: 
21: Catalogue entries should be read as **operating contracts**:
22: 
23: | Field | Meaning |
24: |---|---|
25: | Purpose | The problem the agent helps solve. |
26: | Use when | The lifecycle activity and project conditions for which the agent is relevant. |
27: | Approved inputs | The artefacts and context the agent may use. |
28: | Outputs | The artefacts or evidence the agent produces, not what is automatically accepted. |
29: | Human review | The role that checks the output and the decision that remains human. |
30: | Limitations and stop conditions | When the output must be clarified, escalated or rejected. |
31: 
32: <object type="image/svg+xml" data="/diagrams/agent-chain.svg" className="diagram" aria-label="The agent chain with lifecycle groups and human reviewers">
33:   The agent chain grouped by lifecycle group.
34: </object>
35: Click an agent to open its entry. [draw.io source](/diagrams/agent-chain.drawio)
36: 
37: ## The agents
38: 
39: | Agent | One-line description | Source |
40: |---|---|---|
41: | [Context Builder](/agents/context-builder) | Creates a unified project context from business, technical, compliance, standards, documentation and codebase sources to support downstream agent-enabled delivery. | Toolkit `context-builder.agent.md` |
42: | [BRD Builder](/agents/brd-builder) | Converts business problems, objectives and discovery inputs into a structured and traceable Business Requirements Document for stakeholder review and approval. | HVE Co
... truncated (4,505 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-playbook-main\\docs\\introduction\\lifecycle.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-playbook-main\docs\introduction\lifecycle.md, lines 1-48
1: ---
2: id: lifecycle
3: title: 1.3 The AI PDLC lifecycle
4: description: "AI PDLC lifecycle framework: the agent chain from business requirements to deployment."
5: sidebar_label: 1.3 The AI PDLC lifecycle
6: ---
7: 
8: :::note Section summary
9: AI PDLC lifecycle framework: the agent chain from business requirements to deployment.
10: :::
11: 
12: The AI PDLC lifecycle connects the agents used from business requirements through deployment to
13: Azure. Each step produces or develops an artefact that becomes an input to subsequent activities,
14: with human approval of generated artefacts across the lifecycle.
15: 
16: <object type="image/svg+xml" data="/diagrams/agent-chain.svg" className="diagram" aria-label="The agent chain from Context Builder to Azure Deploy, with the human reviewer for each step">
17:   The agent chain: Context Builder, BRD Builder, PRD Builder, ADR Creation, Backlog Manager, Spec-Clarify, Task Planner, Task Implementor, API and Functional Testing, Azure Deploy.
18: </object>
19: Click an agent to open its catalogue entry. [draw.io source](/diagrams/agent-chain.drawio)
20: 
21: | Step | Agent / capability | Activity / output |
22: |---|---|---|
23: | 1. Context Builder | [`context-builder`](/agents/context-builder) | Capture context from Confluence and project sources to contextualise agents. |
24: | 2. Business Requirements | [`brd-builder`](/agents/brd-builder) | Business requirements creation. |
25: | 3. Product Requirements | [`prd-builder`](/agents/prd-builder) | Create the PRD from discoveries. |
26: | 4. Architecture | `adr-creation` and `arch-diagram-builder` | Record key architecture decisions and diagrams. |
27: | 5. Backlog Manager | [`backlog-manager`](/agents/backlog-manager) | Create the user-story backlog. |
28: | 6. Spec, Clarify | [`spec-clarify`](/agents/spec-clarify) | The specification becomes the source for implementation and is built using project or domain knowledge in the context. Clarify ambiguities and unknowns in the story with the BA. |
29: | 7. Plan and Task | [`task-planner`](/agents/task-planner) | Plan and create implementation tasks using the context. |
30: | 8. Implementation and Unit Test | [`task-implementor`](/agents/task-implementor) | Execute plans with validation. |
31: | 9. Deploy | [Azure deployment pipeline](/agents/azure-deploy) | `azure-prepare` → 
... truncated (3,451 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\repo-template\\.vscode\\mcp.json"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.vscode\mcp.json, lines 1-104
1: {
2:   "inputs": [
3:     {
4:       "type": "promptString",
5:       "id": "jira-url",
6:       "description": "Jira base URL (e.g. https://your-company.atlassian.net or https://jira.your-company.com)"
7:     },
8:     {
9:       "type": "promptString",
10:       "id": "jira-email",
11:       "description": "Jira Cloud account email (leave empty when using a Server/Data Center Personal Access Token)"
12:     },
13:     {
14:       "type": "promptString",
15:       "id": "jira-api-token",
16:       "description": "Jira API token (Cloud) or Personal Access Token (Server/Data Center)",
17:       "password": true
18:     },
19:     {
20:       "type": "promptString",
21:       "id": "confluence-url",
22:       "description": "Confluence base URL (Cloud: https://your-company.atlassian.net/wiki)"
23:     },
24:     {
25:       "type": "promptString",
26:       "id": "confluence-email",
27:       "description": "Confluence Cloud account email (leave empty when using a Server/Data Center Personal Access Token)"
28:     },
29:     {
30:       "type": "promptString",
31:       "id": "confluence-api-token",
32:       "description": "Confluence API token (Cloud) or Personal Access Token (Server/Data Center)",
33:       "password": true
34:     },
35:     {
36:       "type": "promptString",
37:       "id": "gitlab-url",
38:       "description": "GitLab base URL (e.g. https://gitlab.your-company.com)"
39:     },
40:     {
41:       "type": "promptString",
42:       "id": "gitlab-token",
43:       "description": "GitLab Personal Access Token (api scope for read/write, read_api for read-only)",
44:       "password": true
45:     }
46:   ],
47:   "servers": {
48:     "playwright": {
49:       "type": "stdio",
50:       "command": "npx",
51:       "args": [
52:         "-y",
53:         "@playwright/mcp@0.0.83",
54:         "--browser",
55:         "chromium",
56:         "--isolated",
57:         "--viewport-size",
58:         "1280x720",
59:         "--test-id-attribute",
60:         "data-testid",
61:         "--timeout-action",
62:         "10000",
63:         "--timeout-navigation",
64:         "30000",
65:         "--output-dir",
66:         "${workspaceFolder}/generated_tests/_mcp-artifacts",
67:         "--save-session",
68:         "--allowed-origins",
69:         "http://localhost:4201;http://127.0.0.1:4201;http://localho
... truncated (3,672 chars total)
```

### Assistant - 2026-11-04 15:40 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

Let me get some quick metrics and a peek at an agent file frontmatter to characterize them. Also check docs count, word counts, and the toolkit agent file formats.

</details>

**Tool `shell`** - completed

```json
{"command": "$root=\"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\"\n$t=\"$root\\aisdlc-toolkit-main\"\n$p=\"$root\\aisdlc-playbook-main\"\n\"TOOLKIT total files: \" + (Get-ChildItem -Recurse -File $t).Count\n\"TOOLKIT repo-template files: \" + (Get-ChildItem -Recurse -File \"$t\\repo-template\").Count\n\"PLAYBOOK docs md files: \" + (Get-ChildItem -Recurse -File \"$p\\docs\" -Filter *.md).Count\n\"PLAYBOOK total md lines: \" + ((Get-ChildItem -Recurse -File \"$p\\docs\" -Filter *.md | Get-Content | Measure-Object -Line).Lines)\n\"TOOLKIT total size KB: \" + [math]::Round(((Get-ChildItem -Recurse -File $t | Measure-Object Length -Sum).Sum/1KB),1)\n\"PLAYBOOK total size KB (no node_modules): \" + [math]::Round(((Get-ChildItem -Recurse -File $p | Where-Object {$_.FullName -notmatch 'node_modules'} | Measure-Object Length -Sum).Sum/1KB),1)\n\"---- agent frontmatter ----\"\nGet-ChildItem \"$t\\repo-template\\.github\\agents\\*.agent.md\" | ForEach-Object { $n=$_.Name; $d=(Select-String -Path $_.FullName -Pattern '^description:' | Select-Object -First 1).Line; \"$n :: $d\" }"}
```

```text
TOOLKIT total files: 89
TOOLKIT repo-template files: 56
PLAYBOOK docs md files: 40
PLAYBOOK total md lines: 2140
TOOLKIT total size KB: 649.4
PLAYBOOK total size KB (no node_modules): 1179.9
---- agent frontmatter ----
api-tester.agent.md :: description: "Use when: running backend API tests with Playwright after Implementation Builder, using output/{RUN_ID}/specify/spec.md to determine API scope and contracts."
context-builder.agent.md :: description: "Use when: creating new project context from Confluence, attached Word/PDF documents, existing project code, and user-provided standards."
context-updater.agent.md :: description: "Use when: updating project context from changes to Confluence or attached documents, legacy project code, dependencies, domain guidance, or user-provided standards."
figma-extractor.agent.md :: description: "Use when: extracting Figma design artifacts from a requirement file. Runs the Python pipeline to produce parent JSON, parent PNG, locally cropped screen PNGs, effective screen table, and figma_report.md."
functional-automation-test.agent.md :: description: "Use after Implementation Builder to execute frontend functional tests from output/{RUN_ID}/specify/spec.md and report evidence-backed results."
implement.agent.md :: description: "Use when: implementing code from approved plans and task files, including unit tests."
planner.agent.md :: description: "Use when: deriving implementation plans and task DAGs from technical specifications."
qa-test-case-generator.agent.md :: description: "Use when a QA engineer provides a Jira user story or story content and needs comprehensive test cases covering Acceptance Criteria, Business Logic, Exception/Error Handling, and other independently testable requirements; on first use, invite an optional identified sample test case to establish a reusable template, otherwise use the workspace template; triggers: generate qa test cases, qa test generator, create test cases from story, jira test cases."
reviewer.agent.md :: description: "Use when: reviewing specs, plans, code, tests, or docs for compliance, security, quality, and traceability."
specify.agent.md :: description: "Use when: generating technical specifications from canonical project requirements."
technical-documenter.agent.md :: description: "Use when: generating initial or final technical documentation from specs or implementation."
traceability-manager.agent.md :: description: "Use when: updating or validating end-to
... truncated (2,609 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\\repo-template\\.github\\agents\\specify.agent.md", "limit": 60}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\agents\specify.agent.md, lines 1-60
1: ---
2: description: "Use when: generating technical specifications from canonical project requirements."
3: name: "Technical Specifier"
4: tools: [read, edit, search, execute, agent]
5: agents: ["Figma Extractor", "Compliance Reviewer"]
6: user-invocable: true
7: argument-hint: "Enter Jira key (e.g., ABCAPP-123), requirement file path, or press Enter for active file."
8: disable-model-invocation: true
9: ---
10: 
11: You are a Technical Specifier for a software application project.
12: 
13: ## Human-Initiated Stage
14: - Run only when a human explicitly starts this agent. Do not run as a subagent or as part of an automatic chain.
15: - Do not invoke Implementation Planner or any later-stage agent.
16: - After all specification artifacts are complete, automatically invoke Compliance Reviewer as the spec gate. Provide the run ID, source requirements, `spec.md`, `compliance-validation.md`, and the updated traceability matrix.
17: - If the review cannot be invoked or returns no usable status/findings, stop and report the review as blocked; do not emit a success handoff.
18: - If the review reports Critical, High, or Medium findings, stop and make every finding visible; the human must resolve them and rerun this stage and its review, or explicitly accept them before the handoff. For a `FAIL` with only Low findings, emit `REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.` Preserve the `FAIL` status and all findings; independent stage hard gates still block.
19: - Follow the severity-based review policy in `.github/rules/pdlc.md`.
20: 
21: ## Your Job
22: - Accept Jira story keys, requirement markdown files, or PRD files as input.
23: - For Jira input: Fetch issue details via Jira MCP, extract requirements, and create a canonical requirement markdown file automatically.
24: - Transform canonical requirements into implementation-ready technical specifications.
25: - Preserve traceability from `FR-*` and `NFR-*` to `SPEC-*`.
26: - Assess frontend and backend separately against the user story. Specify required changes, applicable contracts/models/controls, and files to change; explicitly document unchanged or not-applicable surfaces with evidence.
27: - Apply domain-specific controls (privacy, complian
... truncated (7,629 chars total)
```

### Assistant - 2026-11-04 15:40 | opencode-go/deepseek-v4.1-flash | build

<details><summary>Reasoning</summary>

I have enough. Let me also quickly check documentation counts, the toolkit .gitignore, and the diagrams doc maybe. But I think I have enough for a detailed brief. Let me maybe grab the agent-framework doc titles and the playbook's fuller doc list already obtained. Let me summarize.

I should present a clear, thorough briefing of both packages: what each is, structure, contents, how they relate, how to use/run them, notable features, and observations. Keep it organized but detailed.

Let me note a couple of observations:
- Both are "SCBX AI-First SDLC" deliverables, draft Oct 2026.
- Toolkit is the implementation assets (agents, rules, templates, prompts, MCP servers, installer).
- Playbook is Docusaurus documentation site for the same methodology, with draw.io diagrams.
- Cross reference: playbook references `../aisdlc-toolkit`.
- 11 toolkit agents + 6 supporting = 12 agent files total (count: api-tester, context-builder, context-updater, figma-extractor, functional-automation-test, implement, planner, qa-test-case-generator, reviewer, specify, technical-documenter, traceability-manager = 12).
- 14 rules files, 6 templates, 2 prompts, 1 instruction file.
- 3 MCP servers, 43 tools total (12 Jira, 7 Confluence, 24 GitLab? let me count: GitLab tools listed: list_projects, get_project, list_tree, get_file, list_branches, create_branch, list_commits, commit_files, search, list_issues, get_issue, create_issue, update_issue, add_issue_note, list_merge_requests, get_merge_request, get_merge_request_diffs, create_merge_request, update_merge_request, add_merge_request_note, list_pipelines, get_pipeline, get_job_log = 23). Jira 12, Confluence 7, GitLab 23 = 42.
- Playbook: Docusaurus 3.10.2, React 19, 40 md docs ~2,140 lines, 4 draw.io diagrams exported to SVG with hyperlinks, sections 1-5 + Appendix A, sections 6-9 pending.
- Playbook docs 3.10.2 requires node >=20.
- Playbook has broken-link throw settings and absolute internal URL.
- Note: playbook is standalone Docusaurus site; not installed, just built.

Also mention gaps/caveats: toolkit is bash installer (needs Git Bash/WSL on Windows), install.sh requires bash; MCP needs build. Playbook `npm run diagrams` uses `sh diagrams/export.sh`. Also the playbook uses the HVE Core All extension for planning agents, which is external and not in this repo. Jira/ADO backlog etc. Actually toolkit's README says "HVE Core All extension (pre-release)".

Also the playbook mentions Azure Deploy as lifecycle endpoint, while toolk

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "Requirement Intake Consolidator|User Story Generator", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main", "include": "*.md"}
```

```text
Found 17 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\AGENTS_GUIDE.md:
  Line 41:    Requirement Intake Consolidator (role, see intake prompts)

  Line 76: These arrows show the recommended order, not automatic execution. Each numbered stage requires a human start and review before the next stage. The intake prompt performs intake and the intake traceability gate, then stops before specification. User Story Generator and Requirement Intake Consolidator are workflow roles, not standalone agents.

  Line 555: -> Requirement Intake Consolidator

  Line 571: -> User Story Generator (workflow role, not a standalone agent)


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\requirement\README.md:
  Line 11: | `BRD_{ProjectName}.md`                        | Requirement Intake Consolidator / BRD Builder |

  Line 13: | `{ProjectName}_Requirements.md`               | Requirement Intake Consolidator               |

  Line 15: | `Intake_Gap_Report_{ProjectName}.md`          | Requirement Intake Consolidator               |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\SPEC_DRIVEN_WORKFLOW.md:
  Line 14: -> Requirement Intake Consolidator

  Line 33: -> User Story Generator


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\copilot-instructions.md:
  Line 76: -> Requirement Intake Consolidator

  Line 93: -> User Story Generator


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\prompts\intake-to-implementation.prompt.md:
  Line 16: 1. Requirement intake: act as `Requirement Intake Consolidator`.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\prompts\intake-to-spec.prompt.md:
  Line 16: 1. Act as `Requirement Intake Consolidator`.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\docs\agent-framework\CONTEXT_MANAGEMENT_VERIFICATION_CHECKLIST.md:
  Line 287: - [x] Existing Requirement Intake Consolidator still works

  Line 288: - [x] Existing User Story Generator agent still works


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\aisdlc-toolkit-main\repo-template\.github\rules\traceability-standards.md:
  Line 27: - `Requirement Intake Consolidato
... truncated (2,606 chars total)
```

**Tool `shell`** - completed

```json
{"command": "$t=\"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\aisdlc-toolkit-main\"\n\"rules: \" + (Get-ChildItem \"$t\\repo-template\\.github\\rules\" -File).Count\n\"templates: \" + (Get-ChildItem \"$t\\repo-template\\.github\\templates\" -File).Count\n\"prompts: \" + (Get-ChildItem \"$t\\repo-template\\.github\\prompts\" -File).Count\n\"agents: \" + (Get-ChildItem \"$t\\repo-template\\.github\\agents\\*.agent.md\").Count\nGet-Content \"$t\\mcp\\package.json\""}
```

```text
rules: 14
templates: 6
prompts: 2
agents: 12
{
  "name": "team-mcp-servers",
  "private": true,
  "description": "Shared MCP servers (Jira, Confluence, GitLab, ...) for GitHub Copilot and Claude Code",
  "type": "module",
  "workspaces": [
    "jira",
    "confluence",
    "gitlab"
  ],
  "scripts": {
    "build": "npm run build --workspaces",
    "typecheck": "npm run typecheck --workspaces"
  },
  "engines": {
    "node": ">=20.12"
  }
}

```

### Assistant - 2026-11-04 15:40 | opencode-go/deepseek-v4.1-flash | build

Here's a detailed briefing on both packages.

## Big picture

These are two halves of one deliverable: the **SCBX AI-First SDLC** (Agentic PDLC) capability, draft October 2026.

| | `aisdlc-toolkit-main` | `aisdlc-playbook-main` |
|---|---|---|
| Role | The **implementation assets** — files agents actually read and run | The **documentation site** — how and why the lifecycle works |
| Form | Shell installer + VS Code/Copilot agent pack + 3 MCP servers | Docusaurus 3 static site + draw.io diagrams |
| Size | 89 files, ~650 KB | 40 Markdown docs (~2,140 lines) + 4 diagrams, ~1.2 MB excluding `node_modules` |
| Audience | Developers/FDEs installing into a product repo | Product squads, leads, governance readers |
| Depends on | Node 20.12+, VS Code + Copilot, HVE Core All extension | Node 20+, the toolkit (referenced as `../aisdlc-toolkit`) |

They explicitly cross-reference each other: the playbook states *"the playbook explains how and why; the toolkit holds the files the agents read and follow."*

---

## 1. `aisdlc-toolkit-main` — the toolkit

### What it does
It installs a standard, agent-ready repository skeleton into any product repo, so every squad runs the same lifecycle with the same context, requirements, output and traceability conventions.

```text
aisdlc-toolkit-main/
├── install.sh          # installer / updater
├── repo-template/      # everything copied into a product repo
├── mcp/                # jira, confluence, gitlab MCP servers (TypeScript, stdio)
└── docs/agent-framework/  # 10 maintainer reference docs
```

### `install.sh` — the installer
A ~117-line Bash script with three modes:

```bash
./install.sh /path/to/product-repo            # install; never overwrites existing files
./install.sh /path/to/product-repo --update   # refresh toolkit-owned files only
./install.sh /path/to/product-repo --dry-run  # preview
```

It does four things:
1. Copies every file under `repo-template/` that doesn't already exist.
2. Substitutes the `__TOOLKIT_DIR__` token in `.vscode/mcp.json` with the toolkit's absolute path (so MCP servers resolve).
3. Merges `.env`, `generated_tests/_mcp-artifacts/`, `__pycache__/` into the target `.gitignore` without duplicating lines.
4. Warns if the MCP servers haven't been built yet.

Ownership policy is the key design: `--update` replaces `.github/agents`, `rules`, `prompts`, `templates`, `scripts`, `instructions`, `copilot-instructions.md`; it **never** touches project-owned `.github/contexts/`, `.vscode/mcp.json`, `docs/`, `requirement/`, `output/`, `.gitignore`.

### The agent pack — 12 agents in `repo-template/.github/agents/`

| Agent | Phase | Output |
|---|---|---|
| Context Builder | 2 Contextualise | `.github/contexts/*`, `requirement/Context_*.md` |
| Context Updater | 2 / 10 Operate | Updated contexts, `CTX-UPDATE-*` |
| Figma Extractor | 4 Design / 5 Specify | `output/<RUN_ID>/specify/figma/` |
| Technical Specifier | 5 Specify | `spec.md` |
| Implementation Planner | 6 Plan | `plan.md`, `tasks.md` |
| Implementation Builder | 7 Build | Code, unit tests, evidence |
| API Tester | 8 Validate (backend) | `api-tests/attempt-<n>/` |
| Functional Automation Test | 8 Validate (frontend) | `functional-tests/attempt-<n>/` |
| QA Test Case Generator | 8 Validate (manual) | `output/test-cases/<story-key>/` |
| Compliance Reviewer | Gates | `REVIEW-*` findings |
| Technical Documenter | 8 / 9 Release | `DOC-*` |
| Traceability Manager | Between phases | `Traceability_Matrix.md` |

Design principles embedded in the agents:
- **Human-initiated stages only.** Every stage stops, emits `NEXT_STEP`, and is never auto-chained.
- **Bounded subagent reviews.** Specifier, Planner and Documenter may invoke Compliance Reviewer only at their own gate.
- **Severity policy.** Critical/High/Medium findings block handoff; Low-only `FAIL` proceeds with `REVIEW_GATE_WARNING` while keeping the `FAIL` status visible.
- **Figma is never a blocker.** Falls back to Jira/Confluence screenshots or manual uploads; only a frontend story with *zero* design evidence blocks.
- **Independent hard gates** (e.g. 80% unit coverage, failing tests) can't be overridden by a non-blocking review.

Note: `Requirement Intake Consolidator` and `User Story Generator` appear in the flow but are explicitly **workflow roles**, implemented by the intake prompts, not standalone agent files.

### Rules, templates, prompts
- **14 rule files** in `.github/rules/`: `lifecycle-governance.md` (paths, tailoring, 12 human approval gates), `pdlc.md` (stage flow/review policy), `requirement-standards.md`, `traceability-standards.md`, three execution-gate files (spec/plan/implementation), `architectural-`, `security-quality-`, `environment-`, `versioning-standards.md`, `mcp-usage-guide.md`, `figma-interactive-selection-guide.md`, `qa-test-case-generator.rules.md`.
- **6 templates**: increment card, lifecycle tailoring record, squad baseline, requirements input, user story, QA test case.
- **2 prompts**: `intake-to-spec` (stops before specification) and `intake-to-implementation` (one stage per invocation).
- **1 instruction file** for the QA test case generator.

The lifecycle governance is phase `0 Mobilise` → `10 Operate and improve`, with three project paths (Greenfield, Brownfield, Modernisation) and gate owners like Product Owner, Forward Deployed Engineer/Architect, Quality/Security.

### MCP servers — `mcp/`
TypeScript npm workspaces, built once per machine (`npm install && npm run build`), 42 tools total:

| Server | Tools | Coverage |
|---|---|---|
| `jira` | 12 | JQL search, read/create/update, comments, transitions, projects, users, link types, issue links |
| `confluence` | 7 | CQL search, page read/create/update (replace/append/prepend), comments, spaces, children |
| `gitlab` | 23 | Projects, files, branches, commits, search, issues, MRs + diffs, pipelines, job logs |

Supports Jira/Confluence **Cloud and Server/Data Center** (API token or PAT), self-managed GitLab, internal CA via `NODE_EXTRA_CA_CERTS`. Deliberately **no MR merge tool** — merging stays a human action. Credentials are supplied through VS Code `promptString` inputs (encrypted) in `.vscode/mcp.json`, never committed.

The MCP README is unusually complete: setup for VS Code Copilot, Copilot CLI, Claude Code CLI, and Claude Desktop, plus a troubleshooting table.

### `docs/agent-framework/`
10 maintainer docs: architecture, agents guide/setup, spec-driven workflow, context management (guide, quickstart, implementation summary, verification checklist), MCP configuration and quick start.

---

## 2. `aisdlc-playbook-main` — the playbook site

### What it is
A Docusaurus 3.10.2 / React 19 documentation site (private, v0.1.0) titled **"SCBX AI-First SDLC Playbook"**, tagline *"How product squads deliver with agents across the lifecycle, with people accountable at every gate."*

```bash
npm install
npm start        # http://localhost:3000
npm run build    # static site in build/
npm run diagrams # re-export draw.io -> SVG
```

### Content structure (`sidebars.js`)

| Section | Pages |
|---|---|
| About | `intro.md` |
| 1. Introduction to Agentic PDLC | what Agentic PDLC means, the four changes, the lifecycle |
| 2. Overview of Agentic PDLC | end-to-end flow, project types, baseline, tailoring, select agents |
| 3. Execute in different project types | overview, greenfield, brownfield, modernisation, hybrid |
| 4. Pilot pre-initiation & getting started | environment, BRD, PRD, backlog, specify, plan, implement, API tests, functional tests |
| 5. Product squad roles | squad roles, role evolution |
| Appendix A. Agent catalogue | catalogue + 10 agent entries + supporting agents |
| Reference | `toolkit.md`, `diagrams.md` |

Sections **6–9 are still to come** ("Mobilising the squad", "Governance and controls", "Measurements", "Templates and reference"). The playbook is explicitly a living draft based on sections 1–5 + Appendix A of the source draft.

### Diagrams
Four `.drawio` sources → exported to `static/diagrams/*.svg`:
- `agent-chain` — agents grouped by lifecycle stage with human reviewers
- `end-to-end-flow` — full lifecycle flow
- `lifecycle-paths` — greenfield/brownfield/modernisation/hybrid
- `stage-run` — how a single stage executes

SVGs embed the source so they reopen in draw.io, and shapes keep **hyperlinks** to playbook pages. `diagrams/export.sh` uses the draw.io desktop app if installed, otherwise the bundled `render.mjs`.

### Config details
- `onBrokenLinks: 'throw'`, broken anchors/markdown links also throw — strict build.
- `routeBasePath: '/'` — docs are the site root.
- Navbar + footer wired to the main sections; local search not enabled.
- Configured for `https://aisdlc-playbook.scbx.internal` at `/`; changing `url`/`baseUrl` for a sub-path requires re-exporting diagrams because their links are absolute.
- No blog, single locale (`en`), custom CSS at `src/css/custom.css`.

---

## How they work together

1. Build the MCP servers once: `cd aisdlc-toolkit-main/mcp && npm install && npm run build`
2. Install into a product repo: `./install.sh /path/to/product-repo`
3. Open in VS Code, start MCP servers (`MCP: List Servers`).
4. Create an increment card in `docs/increments/` and a lifecycle tailoring record.
5. Run **Context Builder**, then the lifecycle stage by stage; each stage stops for human review.
6. Read the playbook for the *why*, tailoring rules and the operating contract of each agent.

Artifact chain the whole system enforces:

```text
CTX → BRD → FR/NFR → US → SPEC → TASK → CODE → APT/FT/TEST → REVIEW → DOC
```

Everything lands in predictable places: `requirement/` for canonical requirements, `output/<RUN_ID>/` per run, `.github/contexts/` for project context, `docs/increments/` for increment governance.

---

## Observations worth flagging

- **Bash dependency on Windows.** `install.sh` and `npm run diagrams` (`sh diagrams/export.sh`) need Git Bash or WSL. There's no PowerShell equivalent.
- **Two different lifecycle narratives.** The playbook's introduction describes a 9-step chain ending at **Azure Deploy**, while the toolkit's `lifecycle-governance.md` defines an 11-phase lifecycle (`0 Mobilise` → `10 Operate and improve`) with Release and Operate phases. The playbook's early sections read like the original draft; the toolkit is the more evolved model. Expect drift until the playbook's sections 6–9 land.
- **HVE Core All extension is a hard dependency** for BRD Builder, PRD Builder, ADR Creation, Backlog Manager, Code Review and Azure Deploy — none of those live in this repo (and it's marked pre-release).
- **Scope is banking-flavoured but generic.** Context rules call out KYC/AML, risk profiling, suitability, PDPA/GDPR, maker-checker — applied only when in scope.
- **Governance is taken seriously.** 12 named approval gates, explicit reuse/skip justification requirements, and a rule that agents never promote to production autonomously.
- **Security posture is sound for a local tool:** tokens via `promptString` or git-ignored `.env`, no secrets in config, PII prohibition written into `copilot-instructions.md`, and GitLab write scope controllable via `read_api`.

Want me to dig deeper into any part — e.g. the execution-gate rules, the full agent contract for one stage, or what it would take to actually run the playbook/toolkit on this machine?

<details><summary>Reasoning</summary>

Good — that resolves the apparent gap: they're workflow roles, not standalone agents. I'll mention that.

Now let me write a detailed briefing. Structure:

1. Big picture / relationship
2. aisdlc-toolkit-main — what it is, layout, install behavior, agents table, rules/templates/prompts, MCP servers, docs, prerequisites
3. aisdlc-playbook-main — what it is, site structure, sections, diagrams, how to run, config
4. How they fit together / workflow
5. Observations & things worth knowing
6. Quick-start commands

Keep it readable, use tables. Mention concrete file paths.

Metrics: toolkit 89 files, ~649 KB; template 56 files; playbook 40 markdown docs, ~2,140 lines, ~1.18 MB excluding node_modules.

Counts of agent files 12; rules 14; templates 6; prompts 2; instructions 1; MCP servers 3; MCP tools 42 (12 Jira + 7 Confluence + 23 GitLab).

Let me count GitLab again: 1 list_projects, 2 get_project, 3 list_tree, 4 get_file, 5 list_branches, 6 create_branch, 7 list_commits, 8 commit_files, 9 search, 10 list_issues, 11 get_issue, 12 create_issue, 13 update_issue, 14 add_issue_note, 15 list_merge_requests, 16 get_merge_request, 17 get_merge_request_diffs, 18 create_merge_request, 19 update_merge_request, 20 add_merge_request_note, 21 list_pipelines, 22 get_pipeline, 23 get_job_log. Yes 23. Total 42.

Mention no merge tool by design.

Notable: install.sh is bash; on Windows use Git Bash/WSL. Playbook `npm run diagrams` uses sh.

Mismatch note: playbook lifecycle narrative ends with Azure Deploy (9 steps) and reflects the original draft, while toolkit governance has phases 0-10 including Release and Operate; toolkit also adds modernisation/hybrid path handling. This may be intentional layering but is a discrepancy. Actually playbook catalog includes azure-deploy as the final step, and toolkit has 0-10 lifecycle. Worth flagging gently.

Also playbook sidebar shows sections 6-9 not present ("Mobilising the squad", "Governance and controls", "Measurements", "Templates and reference"), draft status.

Also note the playbook URL config points to internal `https://aisdlc-playbook.scbx.internal` with onBrokenLinks throw.

Let me write it.

</details>
