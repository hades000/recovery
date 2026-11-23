# Add backend and frontend standards to AI-First SDLC

- **Session ID:** `ses_e588a5fd8ffewGsi7SxEovtSEQ`
- **Created:** 2026-11-04 23:47  |  **Last activity:** 2026-11-05 18:56
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `plan`
- **Tokens:** 70,812 in / 5,163 out / 8,517 reasoning
- **Messages:** 19

---

> **Synthetic** - 2026-11-04 23:47

<system-reminder>
You are in Plan mode. Discuss the plan with the user directly in the conversation. Do not create or update plan files unless the user explicitly asks you to; when they do, write them only in:
C:\Users\SahilMore\.opencode\plan

Do not modify any other files or ask a subagent to do so.

You remain in Plan mode until the user switches agents. If the user asks you to implement changes, do not do so. Tell them they need to switch agents.
</system-reminder>

### User - 2026-11-04 23:47

need to add this context as well in @13 AI-First SDLC repository\  so find where this context will get added and then we can make those changes
Attached file: `C:\Users\SahilMore\Downloads\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\backend-standards.md`
Attached file: `C:\Users\SahilMore\Downloads\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\frontend-standards.md`

### Assistant - 2026-11-04 23:47 | opencode-go/deepseek-v4.1-flash | plan

I'll start by exploring the repository structure and the attached standards files to understand what needs to be added and where.

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\\backend-standards.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\backend-standards.md, lines 1-58
1: ---
2: title: "Backend standards for the new module (USER-PROVIDED)"
3: description: "Squad decisions for backend work on ACE that cannot be read from the code; Context Builder incorporates them into backend-context.md"
4: ---
5: 
6: Status: Draft, owner FDA. Every row is `USER-PROVIDED`. Rows marked **TBD** are open decisions:
7: agents must not fill them in and must raise them as open items when a story depends on them.
8: 
9: ACE rules still apply and are not repeated here: `ace-monorepo/AGENTS.md`,
10: `ace-monorepo/backend/AGENTS.md`, `ace-monorepo/docs/coding-standard.md` (Spring Data REST with HAL,
11: entities identified by URI, OpenAPI types to the front end, `AceException` errors, BDD and e2e tests).
12: Where this file and the ACE rules disagree, the ACE rules win until the FDA records an exception here.
13: 
14: ## BS-1 Module structure (Spring Modulith)
15: 
16: | ID | Standard |
17: |---|---|
18: | BS-1.1 | New capability is one Spring Modulith application module under `th.co.scb.ace.demo.<module>`, declared with `@ApplicationModule` in `package-info.java`. Module name: **`recovery`** → `th.co.scb.ace.demo.recovery` (D-RCV-02) |
19: | BS-1.2 | The 19 design modules (P1–P10, S1–S9) are **nested application modules** inside `recovery` (for example `recovery.casewf`, `recovery.decision`, `recovery.integration`), each with an `api` package (published: interfaces, DTOs, events; `@NamedInterface`) and an `internal` package; extra published packages (for example `decision.writer`) only where the RWB-TE-001 module map lists them. Package names come from the module map (D-RCV-02) |
20: | BS-1.3 | Modules talk to each other only through another module's `api` package or through application events (`@ApplicationModuleListener`); never through another module's entity, repository or table |
21: | BS-1.4 | Boundaries are tested in every build by unit tests, not by pipeline stages (D-RCV-05): `ApplicationModules.of(DemoApplication.class).verify()` (existing `ModulithTest`) plus the RWB-TE-001 rules as JUnit tests. Extra test libraries (for example ArchUnit) need plan approval |
22: | BS-1.5 | Existing ACE packages (`controller`, `service`, `model`, ...) are not extended for the new module; new code lives in the module package |
23: 
24: ## BS-2 Database and migrations
25: 
26: | ID | Standard |
27: |---|---|
28: | BS-2.1 | 
... truncated (5,462 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\\frontend-standards.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\frontend-standards.md, lines 1-42
1: ---
2: title: "Frontend standards for the new module (USER-PROVIDED)"
3: description: "Squad decisions for frontend work on ACE that cannot be read from the code; Context Builder incorporates them into frontend-context.md"
4: ---
5: Status: Draft, owner FDA with UX. Every row is `USER-PROVIDED`. Rows marked **TBD** are open decisions:
6: agents must not fill them in and must raise them as open items when a story depends on them.
7: 
8: ACE rules still apply and are not repeated here: `ace-monorepo/AGENTS.md`,
9: `ace-monorepo/frontend/AGENTS.md`, `ace-monorepo/docs/coding-standard.md` (backend owns business
10: logic, Ketting for HAL navigation, API types only from `frontend/src/api/schema.d.ts`).
11: 
12: ## FS-1 Module structure
13: 
14: | ID     | Standard                                                                                                                                                                                                                             |
15: | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
16: | FS-1.1 | Recovery screens, components and hooks live in `frontend/src/modules/recovery/` (RWB-TE-001 AC6; D-RCV-10)                                                                                                                         |
17: | FS-1.2 | The module's code does not import another business area's components or hooks (for example `cfsc`, `tdr`); shared pieces come only from `components/ui`, `hooks`, `lib`, `utils`. Enforcement (lint rule): **TBD** |
18: | FS-1.3 | Routes of the module are registered under one path prefix: **TBD**; menu entry and placement: **TBD**                                                                                                                    |
19: 
20: ## FS-2 UI and design
21: 
22: | ID     | Standard                                                                                                                                                                                                                                                                                                        |
23: | ------ | -----------------------------------------------
... truncated (5,882 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\AGENTS.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\AGENTS.md, lines 1-166
1: # Recovery Workbench — AI engineering standards
2: 
3: This is the standards file the coding agent reads before every task, as defined in
4: `Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
5: module of the ACE service and to anyone using an AI tool on this repository.
6: 
7: **Owner:** Solution architect with the TechX tech leads.
8: **Change control:** pull request, reviewed like code.
9: **Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
10: and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md`.
11: 
12: ## 1. The seven working rules
13: 
14: 1. The person who merges a change owns it, whoever or whatever wrote it.
15: 2. The agent works from files: the standards file, the story file and the plan file. Anything the
16:    agent needs is in one of the three.
17: 3. The tests and the acceptance criteria exist before the code is generated.
18: 4. Every line that reaches production is read by a person.
19: 5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
20: 6. No personal data or production data goes into a prompt, a test or a log.
21: 7. The unit of work is one story. Work is merged at least once a working day.
22: 
23: ## 2. Structure and stack
24: 
25: - The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
26: - Back end: Spring Boot (Java), Spring JPA, Spring Batch, Spring Security with method security,
27:   Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
28: - Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
29:   back end.
30: - Database: PostgreSQL. Schema changes use versioned migrations (Flyway or Liquibase), one migration
31:   per story, forward-only in production, schema names taken from parameters.
32: - Domain driven design, RESTful API, end-to-end type safety and validation.
33: - Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
34:   case file item. The collection module uses the same terms.
35: - Hosting: the ACE namespace on the shared ACE AKS clusters.
36: 
37: ## 3. The agent must
38: 
39: 1. Put recovery code in the recovery module fo
... truncated (10,194 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\README.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\README.md, lines 1-148
1: # Recovery Workbench — AI-First SDLC repository
2: 
3: This folder is the **working repository** for the Recovery Workbench document set. It follows the
4: SCBX AI-First SDLC toolkit's repository contract and uses the playbook's lifecycle. The twelve
5: numbered folders in the parent directory remain the **source library**; this folder holds the
6: agent-readable corpus, the context package, the increment records and the run output.
7: 
8: ## 1. Why this folder exists
9: 
10: The source set is organised by document type (decisions, business, requirements, stories, technical,
11: data, screens, AI, quality, policy, delivery, communication). The toolkit expects a repository
12: organised by lifecycle artefact:
13: 
14: ```text
15: .github/        agents, rules, prompts, templates, scripts, contexts
16: docs/           increments, discovery, brds, prds, architecture/decisions
17: requirement/    legacy corpus, canonical requirements, traceability
18: output/         per-RUN_ID stage output
19: ```
20: 
21: This folder is that contract. It does not rewrite the source documents; it converts them, indexes
22: them and gives the agents a stable place to read and write.
23: 
24: ## 2. Structure
25: 
26: ```text
27: 13 AI-First SDLC repository/
28: ├── .github/
29: │   ├── agents/ rules/ prompts/ templates/ scripts/ instructions/   # toolkit-owned
30: │   └── contexts/                                                   # project context
31: ├── .vscode/mcp.json                                                # Windows toolkit path
32: ├── AGENTS.md                                                       # Recovery Workbench standards file
33: ├── docs/
34: │   ├── increments/    INC-001 Epic 1, INC-002 Epic 2, tailoring
35: │   ├── discovery/     problem, architecture, journeys, TOM, glossary, features, measures
36: │   ├── brds/          Lean BRDs, Business Requirements Program/E1/E2
37: │   ├── prds/          FSD P1–P10/S1–S9, Epics 3–8, NFR, Reporting/MI
38: │   └── architecture/decisions/  ADR-001–009, ACE architecture decision
39: ├── requirement/
40: │   ├── legacy/        converted corpus, DOCUMENT_MAP.md, conversion report
41: │   ├── Context_RecoveryWorkbench.md
42: │   ├── BRD_RecoveryWorkbench.md
43: │   ├── RecoveryWorkbench_Requirements.md
44: │   ├── Intake_Gap_Report_RecoveryWorkbench.md
45: │   └── Traceability_Matrix.md
46:
... truncated (8,237 chars total)
```

> **Synthetic** - 2026-11-04 23:47

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\AGENTS.md
# Recovery Workbench — AI engineering standards

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md`.

## 1. The seven working rules

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files: the standards file, the story file and the plan file. Anything the
   agent needs is in one of the three.
3. The tests and the acceptance criteria exist before the code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
6. No personal data or production data goes into a prompt, a test or a log.
7. The unit of work is one story. Work is merged at least once a working day.

## 2. Structure and stack

- The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
- Back end: Spring Boot (Java), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL. Schema changes use versioned migrations (Flyway or Liquibase), one migration
  per story, forward-only in production, schema names taken from parameters.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. The collection module uses the same terms.
- Hosting: the ACE namespace on the shared ACE AKS clusters.

## 3. The agent must

1. Put recovery code in the recovery module folder only. Change the common or collection module only
   where the story file names it.
2. Read every threshold, limit, timer, queue, role, template and route from its versioned reference
   table. Never write one as a literal in code.
3. Put a Spring Security method check on every endpoint, naming the capability area and the operation.
4. Write a decision record entry for every change to a case and every decision, with the rule ID and
   version used.
5. Use the names in the business glossary for classes, fields, tables and endpoints.
6. Return each validation message from the message table by its rule ID.
7. Make database changes by migration script only, one script per story.
8. Use Spring Batch and Quartz for scheduled work.
9. Use the synthetic data generator for test data.
10. Write the test before the code. A change with no test is not complete.
11. Respect module boundaries: call another module only through its published interface or an
    application event. Never read another module's tables.
12. Keep unfinished or cross-squad work behind a feature flag that returns the previous code path
    when off.

## 4. The agent must never

1. Commit a credential, key or token.
2. Call or read the inside of another module.
3. Call a system of record directly. Data arrives through COLLINS and leaves through the integration
   adapters.
4. Add a workflow engine, a rules engine or any new dependency.
5. Disable, skip or weaken a test.
6. Change a migration script that is already merged.
7. Put personal data in code, test fixtures, prompts or log lines.
8. Write business values, thresholds or routes as literals instead of refe...

### Assistant - 2026-11-04 23:47 | opencode-go/deepseek-v4.1-flash | plan

I'll explore the context structure to find where these standards should live.

<details><summary>Reasoning</summary>

The user wants me to find where the backend-standards.md and frontend-standards.md context should be added in the "13 AI-First SDLC repository" folder. Let me explore the contexts folder and related structures.

I'm in Plan mode, so I should only discuss the plan, not make changes.

Let me explore the repository structure to find where context gets added.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts"}
```

```text
Read directory C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts, entries 1-6
backend-context.md
domain-context.md
frontend-context.md
project-context.md
README.md
testing-standards.md
```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Path \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\" -Recurse -Directory | Select-Object -ExpandProperty FullName"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.vscode
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\generated_tests
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\tools
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\instructions
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\prompts
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\rules
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\scripts
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\templates
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\architecture
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\brds
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\discovery
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\increments
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\prds
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\architecture\decisions
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\CONTEXT-20261104
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-001-epic-1-RWB-E1-044
C:\Users\SahilMore\Downloads\Recovery Workbench SharePo
... truncated (38,022 chars total)
```

### Assistant - 2026-11-04 23:47 | opencode-go/deepseek-v4.1-flash | plan

Now let me read the existing context files to understand their structure and where the standards fit.

<details><summary>Reasoning</summary>

Now let me read the existing context files to see their structure, especially backend-context.md and frontend-context.md, and the contexts README.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\README.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\README.md, lines 1-37
1: # Project context
2: 
3: This folder is the context package every agent reads before a task. It was created by the Context
4: Builder run `CONTEXT-20261104` and is maintained by Context Updater.
5: 
6: | File | Owns | Read by |
7: |---|---|---|
8: | `project-context.md` | Business truth: requirements, features, rules, data, compliance, delivery, AI, gaps | Every agent |
9: | `domain-context.md` | Banking, recovery and system vocabulary | Every agent |
10: | `frontend-context.md` | React/Vite stack, 53 screens, design system, accessibility, states | Technical Specifier, Planner, Builder, Functional Test |
11: | `backend-context.md` | Spring Boot stack, modules, APIs, data, integrations, security, observability | Technical Specifier, Planner, Builder, API Tester |
12: | `testing-standards.md` | Test levels, environments, data, gates, evidence | Planner, Builder, API Tester, Functional Test, QA |
13: 
14: ## Source register
15: 
16: The full register is in `project-context.md` §17. The primary sources are:
17: 
18: - `requirement/legacy/` — the converted corpus (411 entries).
19: - `docs/brds/` — the approved business requirements.
20: - `docs/prds/` — the FSD/TSD-level specifications.
21: - `docs/architecture/decisions/` — the nine ADRs and the ACE decision.
22: - `docs/discovery/` — the discovery artefacts.
23: 
24: ## Rules
25: 
26: 1. Do not load unrelated files. Read the context file for your scope and the source documents the
27:    story names.
28: 2. Context Builder creates new context only. Context Updater owns maintenance. Other agents must not
29:    modify context files.
30: 3. Mark unverified statements `GAP` or `ASSUMED` and name the decision log entry.
31: 4. No personal data, credentials or production data in context files.
32: 5. When the source and the context conflict, the approved source wins; record a `CLAR-*` item.
33: 
34: ## Status
35: 
36: `CONTEXT_CREATION_STATUS: READY` with the gaps in `project-context.md` §16. The full run log is
37: `output/CONTEXT-20261104/agent-run-log.md`.
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\backend-context.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\backend-context.md, lines 1-220
1: # Recovery Workbench — backend context
2: 
3: **Purpose:** the backend technology, module boundaries, contracts, data, integrations, security and
4: operational rules an agent needs to specify or build a Workbench service.
5: **Status:** documented from the approved architecture and design set. The ACE source code is not in
6: this workspace (`CTX-GAP-020`), so this file records intended behaviour, not verified implementation.
7: 
8: ## 1. Stack and runtime
9: 
10: | Layer | Position | Source |
11: |---|---|---|
12: | Language and framework | Spring Boot (Java) | Engineering Practices §2.3; AI Assisted Development Approach §3.1 |
13: | Persistence | Spring JPA; PostgreSQL | Engineering Practices §2.3 |
14: | Batch and scheduling | Spring Batch and Quartz | Engineering Practices §3; ADR-003 |
15: | Security | Spring Security with method security and OAuth; Spring Session; Entra ID and the bank IAM | Engineering Practices §2.3; Security and Access Design v2 |
16: | Cloud | Spring Cloud Azure; ACE namespace on the shared ACE AKS clusters | Engineering Practices §2.3 |
17: | API style | RESTful API; Spring Data REST and Spring HATEOAS where appropriate; OpenAPI 3.1 contract | Engineering Practices §2.3; API Specification v2 |
18: | Events | AsyncAPI 3.0; outbox and idempotency | Event and Messaging Design v2; TE-006 |
19: | Schema changes | Flyway or Liquibase; one migration per story; forward-only in production; schema names from parameters | RWB-E1-044; AGENTS.md §3 |
20: | Type safety | End-to-end type safety and validation; front-end types generated from the back end | Engineering Practices §2.3 |
21: 
22: ## 2. Module boundaries
23: 
24: ```text
25: ACE service (one repository, one deployable)
26: ├── common module        ACE team: sign-in, access check, audit and PII logging,
27: │                        shared case view, shared entities (customer, account, product,
28: │                        collateral, asset), shared tasks (TDR calculator)
29: ├── collection module    Collection squad: phone, field, FCR and TDR work before day 90
30: └── recovery module      TechX recovery squads: case stages and tasks, rules component,
31:                          decision centre and log, document hub, partner portal, data loads,
32:                          recovery screens and data products
33: ```
34: 
35: Ru
... truncated (17,859 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\frontend-context.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\frontend-context.md, lines 1-162
1: # Recovery Workbench — frontend context
2: 
3: **Purpose:** the frontend technology, screen inventory, design system, accessibility and interaction
4: rules an agent needs to specify or build a Workbench screen.
5: **Status:** documented from the approved design set. No live Figma file exists; the design evidence is
6: the screen inventory, screen specifications, design system and prototype (`CTX-GAP-019`).
7: 
8: ## 1. Stack and architecture
9: 
10: | Item | Position | Source |
11: |---|---|---|
12: | Framework | React on Vite | Engineering Practices §2.3; AI Assisted Development Approach §3.1 |
13: | Component primitives | Radix | Engineering Practices §2.3 |
14: | Data and server state | TanStack Query | Engineering Practices §2.3 |
15: | Language and types | TypeScript; front-end types generated from the back end, never written by hand or by an AI tool | Engineering Practices §2.2 |
16: | Host | The ACE front end; recovery screens live in the recovery module folder | ADR-001, ADR-002, ADR-006 |
17: | Identity | Entra ID SSO with MFA; the access check runs on each request | RWB-E1-022; Security and Access Design v2 |
18: | Styling | Bank web standards; design tokens from the design system | Design System and Component Library v1 |
19: | Accessibility | WCAG 2.2 AA; automated scan and keyboard checks on each screen | Accessibility Standard v2; Test Strategy §1 |
20: | Localisation | Thai and English; Thai labels and messages are proposed, not approved (DL10) | Content and Label Standard v2; R-11 |
21: | Error and message standard | Every validation message returned from the message table by rule ID | Error and Message Standard v3; AGENTS.md §3 |
22: 
23: ## 2. Screen inventory
24: 
25: 53 screens: 47 in the Workbench and 6 in the partner portal. Every screen is in the ACE front end and
26: the access check runs on each request. The full inventory is
27: `requirement/legacy/07-screens-and-experience/recovery-workbench-screen-inventory-and-navigation-v2-xlsx.md`.
28: 
29: | Area | Screens | Key screens | First release |
30: |---|---|---|---|
31: | Home and cases | SCR-01 to SCR-06 | My work, case list, case record, case timeline, transfer case, raise deviation | E1 read-only case record; E2 full |
32: | Queues | SCR-07 to SCR-09 | Team queues, deviation queue, exception queue | E2 |
33: | Approvals | 
... truncated (11,395 chars total)
```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

Let me inspect how the toolkit's Context Builder and agents reference context files, to place these standards correctly.

<details><summary>Reasoning</summary>

Now let me understand the toolkit's structure for context and instructions. Let me check `.github/instructions`, `.github/rules`, `.github/agents` to see how context is referenced. Also check the source documents that the standards mention (e.g., ADR-RCV-001, D-RCV decisions). And the toolkit's Context Builder agent spec.

The attached files are "backend-standards.md" and "frontend-standards.md" which are described as "Squad decisions for backend work on ACE that cannot be read from the code; Context Builder incorporates them into backend-context.md". So the natural place is:
- `.github/contexts/backend-standards.md` and `.github/contexts/frontend-standards.md` as standalone source files, and/or
- incorporate into `backend-context.md` / `frontend-context.md`.

Let me check the toolkit's context builder agent to see if it defines where "*-standards.md" go. Let me look at `.github/agents`, `.github/instructions`, and rules.

</details>

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Path \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\" -Recurse -File | Select-Object -ExpandProperty FullName"}
```

```text
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\copilot-instructions.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\agent-frontmatter-reference.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\api-tester.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\context-builder.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\context-updater.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\figma-extractor.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\functional-automation-test.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\implement.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\planner.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\qa-test-case-generator.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\reviewer.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\specify.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\technical-documenter.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\traceability-manager.agent.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\backend-context.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\domain-context.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\frontend-context.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\project-context.md
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-Fir
... truncated (6,565 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "backend-context|frontend-context|contexts/", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github", "limit": 100}
```

```text
Found 100 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\README.md:
  Line 10: | `frontend-context.md` | React/Vite stack, 53 screens, design system, accessibility, states | Technical Specifier, Planner, Builder, Functional Test |

  Line 11: | `backend-context.md` | Spring Boot stack, modules, APIs, data, integrations, security, observability | Technical Specifier, Planner, Builder, API Tester |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\functional-automation-test.agent.md:
  Line 43: - Inspect `.github/contexts/` and read all files relevant to the components, including newly added context files and explicitly designated Word/PDF files. Read applicable frontend, backend, testing, project, and domain guidance without changing context files.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\api-tester.agent.md:
  Line 21: - Use `.github/contexts/backend-context.md` to determine the backend tech stack, base path, port, versioning, auth scheme, response envelope, error model, and API standards.

  Line 29: - Read `.github/contexts/backend-context.md`. If it is empty or lacks the tech stack, derive it from backend manifests and source (for example, `pom.xml`, `build.gradle`, `package.json`, `requirements.txt`, `*.csproj`) and record the context gap in the report. Request a Context Updater run; do not modify context files.

  Line 30: - Inspect `.github/contexts/` and read other relevant files, including `testing-standards.md`, `project-context.md`, `domain-context.md`, and user-provided API or security standards.

  Line 41: - Required: `.github/contexts/backend-context.md`.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\traceability-manager.agent.md:
  Line 27: - **Context Standards** files (frontend-context.md, backend-context.md, testing-standards.md) are created by **Context Builder** and updated by **Context Updater**

  Line 44: - `.github/contexts/project-context.md`

  Line 45: - `.github/contexts/domain-context.md` (client industry/domain context and related CTX-* evidence)

  Line 46: - Inspect `.github/contexts/` for additional context files relevant to traceability; include their evidence and CTX-* mappings where applicable.


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint
... truncated (22,281 chars total)
```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

Let me check whether these standards are already referenced anywhere and whether the ADRs they cite exist.

<details><summary>Reasoning</summary>

The toolkit is clear: user-provided standards files should be preserved under `.github/contexts/` and indexed; and their contents incorporated into backend-context.md / frontend-context.md. The standards files themselves say "Context Builder incorporates them into backend-context.md" / "frontend-context.md".

Now, where exactly in backend-context.md and frontend-context.md? Let me check for existing mentions of BS-* and FS-* standards in the repo — maybe the standards are already partially present or referenced. Let me search.

Also check `docs/architecture/decisions/ADR-RCV-001-recovery-api-style.md` — the standards reference it. It may or may not exist. Let me check.

Let me also search for "D-RCV-02", "RWB-TE-001", "ADR-RCV-001" in the repo.

</details>

**Tool `grep`** - completed

```json
{"pattern": "BS-1\\.|FS-1\\.|ADR-RCV-001|D-RCV-0|backend-standards|frontend-standards", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository", "limit": 80}
```

```text
No matches found
```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Path \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\docs\\architecture\\decisions\" -File | Select-Object -ExpandProperty Name"}
```

```text
.gitkeep
ace-architecture-decision.md
adr-001-build-the-workbench-as-a-module-of-ace.md
adr-002-structure-ace-as-a-modular-monolith.md
adr-003-run-the-case-workflow-in-code-with-no-workflow-engine.md
adr-004-hold-every-rule-as-versioned-data.md
adr-005-take-data-through-collins-and-file-loads.md
adr-006-one-ace-front-end-with-a-recovery-module-folder.md
adr-007-build-the-document-hub-in-the-workbench.md
adr-008-trunk-based-development-with-feature-flags.md
adr-009-an-append-only-decision-log-that-blocks-an-action-it-cannot-record.md
README.md

```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Path \"C:\\Users\\SahilMore\\Downloads\\Fw__Recovery_workbench_-_Clarify_items_discussion_-_Sprint_1\" -File | Select-Object -ExpandProperty Name"}
```

```text
backend-standards.md
frontend-standards.md

```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Key findings:
1. The standards files are not referenced anywhere in the repo.
2. The ADR-RCV-001 referenced in the standards does not exist in `docs/architecture/decisions/`.
3. The standards reference "D-RCV-02..10" decision IDs that may not exist in the decision log (need to check).
4. The standards are explicitly designed to be incorporated into backend-context.md and frontend-context.md.

Let me check the decision log for D-RCV-* entries. And check whether RWB-TE-001 spec exists (module map). Also check the project-context.md structure for where user-provided standards might be indexed.

Let me read project-context.md key sections (maybe §17 source register and the CTX IDs). It's likely long. Let me check its size and headings.

</details>

**Tool `shell`** - completed

```json
{"command": "$f=\"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\project-context.md\"; (Get-Content $f | Measure-Object -Line).Lines; Select-String -Path $f -Pattern '^#{1,3} ' | ForEach-Object { $_.Line }"}
```

```text
306
# Recovery Workbench - project context
## 1. Business overview
## 2. Actors, roles and stakeholders
## 3. Process, case and rules model
## 4. Functional scope by module
## 5. Data requirements
## 6. Integration points
## 7. Non-functional requirements
## 8. Compliance, controls and policy
## 9. Delivery model
## 10. AI and agents
## 11. Constraints
## 12. Assumptions and open decisions
## 13. Feature catalogue
## 14. Business rule catalogue
## 15. Feature coverage reconciliation
## 16. Gaps and contradictions
## 17. Source register
## 18. Required guidance for SDD agents

```

**Tool `grep`** - completed

```json
{"pattern": "D-RCV-", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository", "limit": 60}
```

```text
No matches found
```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

The D-RCV decisions do not exist in the repo. So these standards come from an external sprint discussion. Let me read project-context §17 and §18 to see the source register and required guidance, which is where additional standards should be indexed.

Also read the context-builder agent's section on indexing additional standards (around line 348-360) to align.

Let me also check the `requirement/legacy/08-ai-and-agents` folder for AI assisted development approach references — maybe the standards belong there as source material too. But the user asked: "need to add this context as well in @13 AI-First SDLC repository\ so find where this context will get added and then we can make those changes". So they want placement recommendation + plan.

Let me read project-context.md §17-18 and the context-builder around 340-360, and check how the source register lists files.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\project-context.md", "offset": 230, "limit": 80}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\project-context.md, lines 230-309
230: 
231: The full rule table is 448 rows. These are the rule families an agent must recognise; the exact row
232: IDs are in `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-rules-and-routing-logic-v4-xlsx.md`.
233: 
234: | CTX ID | Rule family | What it decides | Example source IDs | Applies to |
235: |---|---|---|---|---|
236: | CTX-RULE-001 | Entry and exclusion | Whether an account at 90 DPD becomes a case; deceased, fraud, bankruptcy, active restructure and open dispute are excluded | R-UNI-16, R-UNI-17 | Case creation |
237: | CTX-RULE-002 | Allocation | Which queue a new case enters by product, region, exposure band, stage, route, deviation, segment and collateral | R-UNI-18, R-UNI-19 | P3 |
238: | CTX-RULE-003 | Assignment | Which owner receives the case by round robin, lowest load or continuity, within the cap and overflow | R-UNI-18, R-UNI-19 | P3 |
239: | CTX-RULE-004 | Transfer | When a case moves queue or role on stage change, route, timer, deviation, approval, document, payment or manual request | R-UNI-20..24 | P3 |
240: | CTX-RULE-005 | Service level and escalation | When a warning or breach fires and who is escalated, without moving the case | R-UNI-31, R-LIT-11 | P3 |
241: | CTX-RULE-006 | Route decision | Which route is recommended and approved, and what happens on cure, payment, deviation or override | R-RES-01..23, R-SET-* | S1, P7 |
242: | CTX-RULE-007 | Restructure and settlement | Offer range, floor, approval level, booking and plan timers | R-RES-01..23, R-SET-01.. | S2 |
243: | CTX-RULE-008 | Guarantee claim | Claim deadline, checklist, submission and result | R-GUA-01.. | S3 |
244: | CTX-RULE-009 | Litigation and notice | Notice template, approval, dispatch, proof of delivery, filing, hearing and judgment | R-LIT-01.. | S4, P6 |
245: | CTX-RULE-010 | Asset disposal | Take-on, valuation age, floor, listing, auction round, RAMC transfer | R-DIS-01.. | S5 |
246: | CTX-RULE-011 | Debt sale | Lot eligibility, reserve, buyer qualification, data room, bid and award | R-DS-01.. | S6 |
247: | CTX-RULE-012 | Write-off | Eligibility, tax criteria, committee, posting and recovery after charge-off | R-WO-01.. | S7 |
248: | CTX-RULE-013 | Deviation | X1–X7 raise, contact stop, handler, evidence, return to the same decision | R-UNI-04..11, R-DEV-01 | S8 
... truncated (11,261 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\agents\\context-builder.agent.md", "offset": 330, "limit": 90}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\agents\context-builder.agent.md, lines 330-419
330: 
331: **Documentation Standards**:
332: - **API Documentation**: OpenAPI/Swagger requirements, endpoint documentation format
333: - **Architecture Documentation**: C4 model or equivalent, ADR (Architectural Decision Records)
334: - **Runbooks**: Deployment runbooks, troubleshooting guides, on-call resources
335: - **Knowledge Base**: Setup guide, developer onboarding, FAQ
336: 
337: ### Phase 3: Create Unified Context Document (With Standards Embedded)
338: 
339: When `.github/contexts/project-context.md` is missing or objectively empty, create/populate it with:
340: 1. **Business Overview**: Product/project purpose, industry, target users, business drivers, scope, and intended outcomes.
341: 2. **Complete Business Requirements and Business Logic**: All sourced requirements, business workflows, rules/policies, invariants, calculations, states, exceptions, validations, acceptance criteria, trace IDs, and source references. Include the Application Feature Catalogue, per-feature workflows/business logic, Business Rule Catalogue, and Feature Coverage Reconciliation required by the Feature and Business Logic Completeness Gate. This is the canonical home for requirement-level business meaning and logic; an overview or technical-context links alone cannot satisfy it.
342: 3. **Business Constraints, Decisions, and Risks**: Business/regulatory/operational constraints, assumptions, exclusions, dependencies, success measures, unresolved questions, and decision history.
343: 4. **Stakeholders and Current State**: Business stakeholders, current business processes, pain points, and business-level system landscape.
344: 5. **Business Compliance and Domain Context**: Required business outcomes and obligations; link to supplemental `domain-context.md` material without duplicating requirements or rules.
345: 6. **Technical Context Index**: Links and applicability notes for the owning frontend, backend, and testing documents. This is an index, not a place to copy technical inventories.
346: 7. When `.github/contexts/domain-context.md` is missing or objectively empty, create/populate it with supplemental verified industry/domain terminology and reference material. Capture project-specific requirements, business rules, and constraints in `project-context.md`, and link between documents rather than duplicate content
... truncated (9,022 chars total)
```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I have a good picture. Let me confirm the remaining part of project-context §17-18, and check whether `testing-standards.md` has any user-provided standards precedent. Also check `copilot-instructions.md` context folder guidance.

Let me read the last part of project-context.md (lines 309-306? Actually 306 lines total, so read from 305). Wait, Measure-Object said 306 lines but grep headings showed §18. Let me read 300-306.

Actually earlier read output "lines 230-309" showed up to line 309 with truncation. The file may be longer than 306 (Measure-Object counts lines maybe). Let me just read from 309.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\project-context.md", "offset": 309, "limit": 60}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\project-context.md, lines 309-348
309: | ADR-001..009 | `docs/architecture/decisions/` | Architecture decisions |
310: | Engineering Practices v4 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md` | Stack, branching, tests, flags, pipeline |
311: | AI Assisted Development Approach v1 | `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md` | AI rules, story format, plan, review, gates |
312: | Agent Catalog v2 | `requirement/legacy/08-ai-and-agents/recovery-workbench-agent-catalog-and-specifications-v2.md` | Agent specifications, autonomy |
313: | AI Decision Governance v2 | `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-decision-governance-v2-docx.md` | Decision record, challenge, reversal |
314: | Model Integration Design v2 | `requirement/legacy/08-ai-and-agents/recovery-workbench-model-integration-design-v2-docx.md` | Model endpoint, inputs, change without release |
315: | Test Strategy v2 | `requirement/legacy/09-testing-and-quality/recovery-workbench-test-strategy-v2-docx.md` | Test levels, environments, gates |
316: | Definition of Ready and Done v3 | `requirement/legacy/09-testing-and-quality/recovery-workbench-definition-of-ready-and-done-v3-docx.md` | Story readiness and acceptance |
317: | Personal Data Protection Design v2 | `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-personal-data-protection-design-v2-docx.md` | PDPA, lawful basis, masking, access |
318: | Controls Catalog v2 | `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-controls-catalog-v2-xlsx.md` | 42 controls |
319: | Regulatory Requirements Map v2 | `requirement/legacy/10-policy-controls-and-compliance/recovery-workbench-regulatory-requirements-map-v2-xlsx.md` | Obligation-to-control mapping |
320: | Release Plan v3 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-release-plan-v3-xlsx.md` | 8 releases, 6 gates |
321: | Build Sequence Epic 1 and Epic 2 v4 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v4-xlsx.md` | 115 build items, dependencies, critical path |
322: | Risks, Assumptions, Issues and Dependencies v2 | `requirement/legacy/11-delivery-and-operations/recovery-workbench-risks-assumptions-issues-and-dependencies-v2-xlsx.md` | 12 
... truncated (5,105 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\testing-standards.md", "limit": 60}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\testing-standards.md, lines 1-60
1: # Recovery Workbench — testing standards
2: 
3: **Purpose:** the test levels, environments, data rules, gates and evidence an agent must plan for.
4: **Source:** `requirement/legacy/09-testing-and-quality/recovery-workbench-test-strategy-v2-docx.md`,
5: `Recovery Workbench Definition of Ready and Done v3`, `Recovery Workbench Test Data Plan v2`,
6: `Recovery Workbench Defect Management Process v2`, `Recovery Workbench Non Functional Test Plan v2`,
7: `Recovery Workbench Regression Suite v5`, `Recovery Workbench Requirements Traceability Matrix v4`.
8: 
9: ## 1. Test levels
10: 
11: | Level | What it covers | Who | Where | When | Exit |
12: |---|---|---|---|---|---|
13: | Unit | Every service method and rule evaluation | Developer | DEV and pipeline | Every commit | 80% line coverage on new code |
14: | Rule table | Each rule row against its test case | Developer with analyst | Pipeline | Every commit and every rule version | Every row passes |
15: | Integration | Modules with a real PostgreSQL database | Developer | Pipeline | Every pull request | All pass |
16: | API contract | Requests and responses against the OpenAPI file | Developer | Pipeline | Every pull request | All pass |
17: | System | Stories end to end against SCB test systems | QA engineer | SIT | Rolling, then SIT week | Every test case for the release passes; no open severity 1 or 2 |
18: | Regression | The regression suite | QA engineer | SIT | Each release | All pass |
19: | Non-functional | Performance, resilience, security | QA with SCB IT | SIT | Before each release | Targets in the NFR specification |
20: | Accessibility | Automated scan and keyboard checks | QA engineer | SIT | Each screen | No level A or AA failure |
21: | User acceptance | Business scripts | Business testers | UAT | UAT week | Scripts signed by the business lead |
22: 
23: ## 2. Environments and data
24: 
25: | Environment | Data | Use |
26: |---|---|---|
27: | DEV | Synthetic only | Developer and rule tests |
28: | SIT | Masked copies from the PII service | System, regression, non-functional |
29: | UAT | Masked copies | Business acceptance |
30: | PROD | Production | No test data; no production data in a prompt, test or log |
31: 
32: Rules:
33: 
34: - No production data below production.
35: - No personal data in a prompt, fixture, test log or screenshot.
3
... truncated (4,104 chars total)
```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I understand the structure. Let me check whether these standards should also be placed in `requirement/legacy/05-technical-architecture` or `08-ai-and-agents` as source. The standards files describe themselves as USER-PROVIDED squad decisions. The toolkit rule says: "When the user supplies additional standards, incorporate their contents into newly created context and record their sources. Create a separate Markdown context file under `.github/contexts/` when requested; never edit existing user-authored files."

But also: context-builder says explicitly designated files should be placed directly under `.github/contexts/` preserving contents. Since these are USER-PROVIDED standards and already named backend-standards.md/frontend-standards.md, the right approach per toolkit is:

1. Copy both files verbatim to `.github/contexts/backend-standards.md` and `.github/contexts/frontend-standards.md` (preserve user-authored content, do not rewrite).
2. Incorporate their rules into `backend-context.md` and `frontend-context.md` (as the standards themselves say: "Context Builder incorporates them into backend-context.md" / "frontend-context.md"), because downstream agents (planner, implement, api-tester) read backend-context.md and frontend-context.md explicitly, and "Discover and read all other applicable context and standards files" is generic.
3. Update `.github/contexts/README.md` table to index the new files.
4. Update `project-context.md` §17 Source register (and maybe §18 required guidance) to list the standards as user-provided sources.
5. Possibly add the missing ADR-RCV-001 file? That's a referenced document that doesn't exist. The standards cite it. But user only asked to add context. Could flag as gap.

Where in backend-context.md would the rules go? Let me map the standards to the existing sections:

Backend standards:
- BS-1 Module structure → backend-context §2 Module boundaries
- BS-2 Database and migrations → §4 Data model (migrations)
- BS-3 API → §3 API surface
- BS-4 Security/privacy/audit → §6 Security and access
- BS-5 Batch and scheduling → §9 Rules and workflow / §7 observability? Better a new section "Batch and scheduling" or fold into §9.

Frontend standards:
- FS-1 Module structure → frontend-context §1 Stack and architecture (host) or new "Module structure" section
- FS-2 UI and design → §5 Design system
- FS-3 Data and state → §6 Data and API integration
- FS-4 Testing → §8 Frontend testing

Given the context files already have structu

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\docs\\architecture\\decisions\\README.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\architecture\decisions\README.md, lines 1-21
1: # Architecture decisions
2: 
3: The nine ADRs and the ACE architecture decision. Each ADR is one page in MADR form, with context,
4: drivers, options, decision and consequences. The source is
5: `requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v1.md`.
6: 
7: | ID | Decision | Status |
8: |---|---|---|
9: | ADR-001 | Build the Workbench as a module of ACE | Accepted |
10: | ADR-002 | Structure ACE as a modular monolith with common, collection and recovery modules | Accepted |
11: | ADR-003 | Run the case workflow in code, in CMMN 1.1 terms, with no workflow engine | Accepted |
12: | ADR-004 | Hold every rule as versioned data and evaluate it with a decision table component | Accepted |
13: | ADR-005 | Take data through COLLINS and file loads; call no system of record directly | Accepted |
14: | ADR-006 | One ACE front end with a recovery module folder | Proposed |
15: | ADR-007 | Build the document hub in the Workbench as the system of record for recovery documents | Accepted |
16: | ADR-008 | Trunk-based development with feature flags | Accepted |
17: | ADR-009 | An append-only, hash-chained decision log that blocks an action it cannot record | Proposed |
18: | — | ACE architecture decision | Accepted |
19: 
20: The ADRs are **reused** for INC-001 and INC-002; the playbook's Design experience and architecture
21: phase is not re-run. The reuse record is in `docs/increments/INC-001-tailoring.md`.
```

**Tool `shell`** - completed

```json
{"command": "Get-ChildItem -Path \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\output\\INC-002-epic-1-RWB-TE-001\\specify\" -File | Select-Object -ExpandProperty Name; Select-String -Path \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\output\\INC-002-epic-1-RWB-TE-001\\specify\\*\" -Pattern 'module map|nested application module|recovery\\.casewf' | Select-Object -First 10 | ForEach-Object { \"$($_.Filename):$($_.LineNumber): $($_.Line)\" }"}
```

```text
agent-run-log.md
compliance-validation.md
spec.md
agent-run-log.md:57: | D-01 | The module map is the only place a package or owner is named. | BR6; story 13 | No package literal in the test. |
spec.md:30: | BR1 | BND-1: recovery classes depend on the collection module only through its published packages. | SPEC-RWB-TE-001-004 | DIRECT | ArchUnit rule built from the module map; `collection..internal..` is forbidden. | COVERED |
spec.md:35: | BR6 | Module names, packages and published packages are read from the module map, not written in the test. | SPEC-RWB-TE-001-002, SPEC-RWB-TE-001-003 | DIRECT | `ModuleMapLoader` parses the YAML; the test takes no package literal. | COVERED |
spec.md:39: | AC4 | Using another module's entity fails with BND-4. | SPEC-RWB-TE-001-007 | DIRECT | Fixture references `recovery.casewf.internal.RecoveryCaseEntity`. | COVERED |
spec.md:40: | AC5 | `HttpClient` in `recovery.casewf.internal` fails with BND-5; the same use in `recovery.integration.adapter` passes. | SPEC-RWB-TE-001-008 | DIRECT | Two fixtures; the allowed package is read from the map. | COVERED |
spec.md:42: | AC7 | A package absent from the module map fails the build naming the package. | SPEC-RWB-TE-001-003 | DIRECT | Loader compares every `recovery.**` package on the classpath with the map. | COVERED |
spec.md:48: | X6 | A new package is not in the module map. | SPEC-RWB-TE-001-003 | DIRECT | Build log names the package. | COVERED |
spec.md:53: The story is a repository-skeleton enabler. It creates one package per Workbench module with a published part (`api` or a package the module map lists) and an internal part, and it makes the build refuse a violation. It also wires the common module's access check for the recovery API. It adds no screen and no endpoint. Every later Epic 1 story builds inside this skeleton; a violation is a failed pull request, not a production defect.
spec.md:65: | `recovery-modules.yaml` | `module_code` | Module map, authored by TechX tech leads | Editable by pull request | Must be unique; `P1..P10`, `S1..S9` |
spec.md:66: | `recovery-modules.yaml` | `package` | Module map | Editable by pull request | Must be a `recovery.<module>` package that exists |

```

### Assistant - 2026-11-04 23:48 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Good. RWB-TE-001's module map exists as `recovery-modules.yaml` in the spec (intended). The standards reference it, consistent.

Now let me verify whether the attached standards files are exactly what should be copied verbatim, and check their full length. backend 58 lines, frontend 42 lines. They are complete.

Let me check the `.github/copilot-instructions.md` for the "additional standards" handling (lines 26-45), and check the `project-context.md` beginning (status/source) to see if there's a place to add a "user-provided standards" note. Also check the `context-updater` maybe says user-provided files are read-only. Already seen.

One important detail: The user says "need to add this context as well in @13 AI-First SDLC repository\ so find where this context will get added and then we can make those changes". They likely want the standards to become part of the repo's context so future agents use them. The best answer:

**Where they go:**
1. Verbatim copies at `.github/contexts/backend-standards.md` and `.github/contexts/frontend-standards.md` (preserves user-authored standards; toolkit explicitly says user-provided standards go there and are never rewritten).
2. Integrated normative rules into `.github/contexts/backend-context.md` and `.github/contexts/frontend-context.md` — because those are the files agents (Planner, Implement, API Tester) are explicitly instructed to read, and the standards' own front matter says Context Builder incorporates them there.
3. Index updates: `.github/contexts/README.md` (file table) and `project-context.md` §17 Source register (and possibly §18).

**Where inside each context file:**
Backend:
- New section 13 "Squad backend standards (USER-PROVIDED)" at end, OR integrate per section:
  - BS-1 → §2 (module boundaries)
  - BS-2 → §4 (data model/migrations)
  - BS-3 → §3 (API surface)
  - BS-4 → §6 (security)
  - BS-5 → §9 (rules and workflow) or §7 (operations)
  
The cleanest for traceability and preservation is a dedicated section that reproduces the BS IDs as a table, with cross-links to existing sections, plus small amendments in the existing sections where there is a conflict (e.g., API base path, plain JSON). But duplication is a concern: toolkit says link rather than duplicate across context files. However, the standards file itself says "Context Builder incorporates them into backend-context.md" — so the intended behavior is that the rules live in the context file, not only in a linked file. The standards file migh

_[truncated]_

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\copilot-instructions.md", "limit": 60}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\copilot-instructions.md, lines 1-60
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
36:   → Gathers business and cli
... truncated (4,339 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\rules\\architectural-standards.md", "limit": 30}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\rules\architectural-standards.md, lines 1-30
1: # Architectural Standards
2: 
3: ## Purpose
4: These standards define the required architecture for applications using this spec-driven PDLC workflow. They are mandatory unless the plan explicitly documents and approves an exception.
5: 
6: ## Architectural Principles
7: - Build from approved requirements and specifications only.
8: - Preserve traceability from requirements to code and tests.
9: - Prefer simple, explicit boundaries over implicit coupling.
10: - Keep regulated workflows auditable, deterministic, and secure.
11: 
12: ## Application Architecture
13: - Use feature-oriented folder structures and reusable UI components.
14: - Keep cross-cutting concerns in core services, not duplicated across features.
15: - Keep presentation logic focused on view composition and interaction; move business and integration logic to services or state management.
16: - Use explicit types and sound null safety; avoid hidden global dependencies and unchecked casts.
17: 
18: ## Layering and Dependency Direction
19: - Widgets may depend on feature services, shared widgets, and Flutter/platform libraries.
20: - Feature services may depend on generated API clients, domain mappers, and utility services.
21: - Shared UI must not depend on feature-specific pages.
22: - Domain models and mapping utilities must not depend on presentation components.
23: - Avoid circular dependencies across pages, shared components, and services.
24: 
25: ## Routing and Navigation Standards
26: - Use route-based feature boundaries and lazy loading where practical.
27: - Apply route guards/resolvers where required for authorization, entitlement checks, and critical prefetching.
28: - Use typed route params/query params and validate/normalize them before usage.
29: - Preserve deterministic navigation behavior for back/forward flows and deep links.
30: 
[Output truncated. Continue reading with offset: 31]
```

### Assistant - 2026-11-04 23:49 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

The `.github/rules/` are generic toolkit rules (mention Flutter, so clearly generic). Project-specific standards belong in `.github/contexts/`.

Now let me verify the exact line counts/contents of attached standards to plan integration. Already read fully (58 and 42 lines). Good.

I should also check the `docs/architecture/decisions` ADR file naming style, in case I recommend adding ADR-RCV-001. Let me read one ADR briefly.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\docs\\architecture\\decisions\\adr-006-one-ace-front-end-with-a-recovery-module-folder.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\docs\architecture\decisions\adr-006-one-ace-front-end-with-a-recovery-module-folder.md, lines 1-35
1: <!-- source: 05 Technical architecture/Recovery Workbench Architecture Decision Records v1.md -->
2: 
3: # ADR-006 One ACE front end with a recovery module folder
4: 
5: - Status: Proposed
6: - Date: 28 October 2026
7: - Deciders: the ACE team
8: - Decision log: DL07
9: 
10: ### Context and problem
11: 
12: ACE has one React front end. The recovery screens can live in a module folder of that front end, or the front end can be split into a workspace of modules.
13: 
14: ### Decision drivers
15: 
16: - Squads work from 2 November
17: - One look and one sign-in for staff
18: - Types generated from the back end
19: 
20: ### Options considered
21: 
22: 1. One ACE front end with a recovery module folder
23: 2. A workspace of front end modules with NX
24: 3. A separate recovery front end
25: 
26: ### Decision
27: 
28: Option 1 from 2 November. A move to option 2 is the ACE team's choice and does not change the recovery screens.
29: 
30: ### Consequences
31: 
32: - Good: no wait for a front end restructure.
33: - Bad: code owners per folder are needed to keep squads out of each other's screens (DL37).
34: 
35: ---
```

### Assistant - 2026-11-04 23:49 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

Now I have enough to propose a plan. Let me also double-check whether there's an existing "standards" file convention in contexts (e.g., testing-standards.md is the only one). Yes.

Let me check whether `backend-context.md` ends at 220 lines and if there is a section 13; read from 220 to end.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\backend-context.md", "offset": 211, "limit": 30}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\backend-context.md, lines 211-220
211: ## 12. Gaps and constraints
212: 
213: | ID | Gap | Impact |
214: |---|---|---|
215: | CTX-GAP-020 | The ACE source code is not in this workspace. | The context is intended behaviour from documents; implementation must verify against the ACE repository. |
216: | CTX-GAP-011 | RPO, RTO and availability targets are open (DL11). | Resilience tests cannot be baselined; use the ACE values until confirmed. |
217: | CTX-GAP-012 | Retention periods for the decision log, ledger and documents are open (DL26). | The retention job can be built with a placeholder class; the periods are loaded as data. |
218: | CTX-GAP-010 | Same-day data interfaces are not named (DL06). | The default is end-of-day; a story that needs same-day data is blocked until DL06. |
219: | CTX-GAP-013 | Partner external access is not live (DL03). | Partner portal integration tests are limited to the bank network until the gateway is live. |
220: | CTX-GAP-014 | The model endpoint is not approved (DL33). | Agents run in shadow with the rule fallback; no live model call is required for E1. |
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\.github\\contexts\\frontend-context.md", "offset": 150, "limit": 20}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\.github\contexts\frontend-context.md, lines 150-162
150: The Functional Automation Test agent reads `UI In Scope` from `spec.md`. A frontend story with no
151: design evidence is blocked until the evidence is added; the current set has local design artifacts,
152: so `DESIGN_EVIDENCE_STATUS: AVAILABLE` with `SOURCE: LOCAL_ARTIFACTS` is the correct status.
153: 
154: ## 9. Gaps and constraints
155: 
156: | ID | Gap | Impact |
157: |---|---|---|
158: | CTX-GAP-019 | No live Figma file or link. | Use the screen inventory, screen specifications, design system and prototype as design evidence; do not claim a Figma source. |
159: | CTX-GAP-021 | Thai labels and messages are proposed, not approved (DL10). | English can ship first; Thai is loaded as reference data when supplied. |
160: | CTX-GAP-025 | Some screens are first delivered in E8 (administration), while the underlying data can be loaded by file before then. | Do not specify an E8 screen for an E1 story; use the file-load path and record the screen as later. |
161: | CTX-GAP-013 | The partner portal depends on external access (DL03), first needed in E5. | Partner screens cannot be tested from outside the bank until the gateway is live. |
162: | CTX-GAP-020 | The front-end codebase is not in this workspace. | The context describes the intended stack and patterns; implementation must verify against the ACE repository. |
```

### Assistant - 2026-11-04 23:49 | opencode-go/deepseek-v4.1-flash | plan

<details><summary>Reasoning</summary>

I now have a complete picture. Let me formulate the plan and ask a couple of clarifying decisions.

Key recommendation:

**Placement (two layers):**

A. Source files (verbatim, user-owned):
- `.github/contexts/backend-standards.md`
- `.github/contexts/frontend-standards.md`
Reason: `.github/contexts/` is the project-context folder; the toolkit says user-provided standards are preserved there and indexed; the files' own front matter says they are USER-PROVIDED squad decisions.

B. Integrated context (agent-facing):
- `.github/contexts/backend-context.md` — add a new section 13 "Squad backend standards (USER-PROVIDED)" with a table of BS-1..BS-5 IDs and the normative rule text, plus cross-references in §2, §3, §4, §6, §9 where they change existing statements.
- `.github/contexts/frontend-context.md` — add new section 10 "Squad frontend standards (USER-PROVIDED)" with FS-1..FS-4, plus cross-references in §1, §5, §6, §8.
- Or alternatively integrate rows directly into existing sections. Need to decide.

C. Index/maintenance updates:
- `.github/contexts/README.md` — add both files to the table with "owns" and "read by".
- `.github/contexts/project-context.md` §17 Source register — add both files.
- Possibly `project-context.md` §18 — add rule that squad standards are binding.
- `README.md` §2 structure — add contexts files? The README structure tree only shows `.github/contexts/` generically, not file names. §3.1 lists five context files. Should add the two standards files to §3.1 reading list. Yes, README §3.1 "Every agent reads `.github/contexts/` before a task:" lists 5 files. Add the two standards.
- `AGENTS.md` §5 "What the agent reads besides the story" — add "Squad backend and frontend standards" row? This is the standards file the coding agent reads. Adding a row makes them binding. Yes, recommend.
- `.github/agents/*` — planner/implement already say "read all other applicable context and standards files", so no change needed. API tester reads backend-context only; since we integrate into backend-context, fine. Functional test reads all relevant context. Good.

**Conflicts / gaps to resolve in the same change (or flag):**

1. `ADR-RCV-001-recovery-api-style.md` is cited but absent. Options:
   - Add the ADR to `docs/architecture/decisions/` (MADR form, status Accepted, date 2026-11-04) and add it to the decisions README.
   - Or add a `CTX-GAP-026` in both context files saying the ADR is referenced but not present, and keep ACE HAL rule until it is.
   

_[truncated]_

</details>

**Tool `grep`** - completed

```json
{"pattern": "V[0-9]|flyway|migration|schema", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\output\\INC-001-epic-1-RWB-E1-044\\specify\\spec.md", "limit": 30}
```

```text
Found 30 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\output\INC-001-epic-1-RWB-E1-044\specify\spec.md:
  Line 1: # Technical Specification — RWB-E1-044 Database migrations versioned with parameterized schema names

  Line 5: | Story | RWB-E1-044 — Database migrations versioned with parameterized schema names |

  Line 8: | Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001, FR-RWB-020); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 044 Database migrations versioned with parameterized schema names v1.md` |

  Line 20: | UI In Scope | `NO` — SCR-44 Interface and job monitor already exists and only displays migration runs. No screen, component, route, label or state is added. |

  Line 21: | Logic In Scope | `YES` — migration lifecycle, lint, checksum validation, drift gate, forward-only guard, cluster lock and run recording. |

  Line 25: | New Nodes Required | `YES` — `RecoveryFlywayConfig`, `MigrationRunRecorder`, `MigrationLint`, `SchemaDriftCheck`, baseline `V1__rwb_e1_001_baseline.sql`. |

  Line 26: | Inherited Existing Behavior | RWB-TE-001 module folder and boundary test; RWB-E1-001 physical schema; RWB-E1-043 reference loads; ACE deployment pipeline and job monitor (RWB-E1-056). |

  Line 34: | BR1 | Every schema change is a versioned migration in the repository; no change is made by hand in any environment. | SPEC-RWB-E1-044-001, SPEC-RWB-E1-044-002, SPEC-RWB-E1-044-013 | DIRECT | Flyway is the only writer; baseline V1 is generated from Physical Schema v4; seed rows are excluded. | COVERED |

  Line 35: | BR2 | No migration file contains a literal schema name; the schema comes from `RWB_SCHEMA` through `${schema}` and the default schema. | SPEC-RWB-E1-044-001, SPEC-RWB-E1-044-004 | DIRECT | `spring.flyway.schemas`, `default-schema` and `placeholders.schema` all read `RWB_SCHEMA`; lint rejects `<name>.` before a known object. | COVERED |

  Line 36: | BR3 | One migration file per story that changes the database, carrying the story key in its header. | SPEC-RWB-E1-044-003 | DIRECT | Lint enforces exactly one `-- Story:` line, no key in two files, no `U*.sql`. | COVERED |

  Line 37: | BR4 | PROD runs forward only: clean disabled, undo files refused, a fix is a new compensating migration. | SPEC-RWB-E1-044-006 | DIRECT | `clean-disabled=true` in every profile; the PROD pipeline step refuse
... truncated (6,713 chars total)
```

**Tool `grep`** - completed

```json
{"pattern": "WCAG|accessibility target", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\13 AI-First SDLC repository\\requirement\\legacy\\07-screens-and-experience", "limit": 10}
```

```text
Found 5 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\07-screens-and-experience\recovery-workbench-design-system-and-component-library-v1-html.md:
  Line 7: Recovery Workbench design system**Built on**React on Vite with Radix primitives in the ACE front end; these tokens and components are the recovery screens' layer**Source**The ACE component library where one exists; this set fills the gaps until the bank design system is confirmed (DL08)**Accessibility**Every component meets WCAG 2.2 AA: contrast, focus, keyboard and target size**Language**Thai and English for every label; layouts allow Thai text to run 30 percent longer

  Line 56: | target.min | 24px | Smallest click target (WCAG 2.2 2.5.8) |


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\13 AI-First SDLC repository\requirement\legacy\07-screens-and-experience\recovery-workbench-accessibility-standard-v2-docx.md:
  Line 19: | Structure | WCAG 2.2 level AA |

  Line 23: Every Workbench and partner portal screen meets WCAG 2.2 level AA. The design system components meet it by construction; each screen is checked before release.

  Line 27: | Area | Rule | WCAG |

```

### Assistant - 2026-11-04 23:50 | opencode-go/deepseek-v4.1-flash | plan

I've traced where these belong. Short answer: they are **project-specific, user-provided standards**, so they belong in `.github/contexts/`, not `.github/rules/` (toolkit-owned) and not `requirement/legacy/` (the converted 411-entry corpus).

## Where the context gets added

### 1. Preserve the originals (new files)

| New file | Source |
|---|---|
| `.github/contexts/backend-standards.md` | attached `backend-standards.md`, copied verbatim |
| `.github/contexts/frontend-standards.md` | attached `frontend-standards.md`, copied verbatim |

This follows `.github/copilot-instructions.md` line 43 ("Preserves and indexes additional user-provided standards under `.github/contexts/`") and the Context Builder rule (line 61) that explicitly designated standards keep their original basename and contents. The files' own front matter says Context Builder incorporates them into `backend-context.md` / `frontend-context.md`, so the originals stay as the source of record.

### 2. Integrate the binding rules into the agent-read context

Downstream agents (Planner, Implement, API Tester) are explicitly told to read `backend-context.md` and `frontend-context.md`, but only generically told to "discover" other context files. So the rules must also live in the two main context files.

**`.github/contexts/backend-context.md`** — add a new section 13 after "Gaps and constraints":

- `## 13. Squad backend standards (USER-PROVIDED)` with the BS-1 to BS-5 rules and IDs
- BS-1 → cross-reference §2 Module boundaries
- BS-2 → cross-reference §4 Data model (migrations row)
- BS-3 → cross-reference §3 API surface (add `/api/recovery/v1`, plain JSON, no HAL)
- BS-4 → cross-reference §6 Security and access
- BS-5 → cross-reference §9 Rules and workflow
- Add open items to §12: BS-4.1 role names TBD, BS-4.2 masking TBD, BS-3.3 error mapping TBD

**`.github/contexts/frontend-context.md`** — add a new section 10:

- `## 10. Squad frontend standards (USER-PROVIDED)` with FS-1 to FS-4
- FS-1 → §1 Stack and architecture (`frontend/src/modules/recovery/`)
- FS-2 → §5 Design system (ACE design system, Henka specs for layout, no Henka visual tokens)
- FS-3 → §6 Data and API integration (plain JSON `/api/recovery/v1`, no Ketting/HAL)
- FS-4 → §8 Frontend testing (Playwright, ports 5173/8080)
- Add open items to §9: route prefix/menu TBD, lint rule TBD, Figma location TBD, accessibility target TBD

### 3. Update the indexes so the files are discoverable

| File | Change |
|---|---|
| `.github/contexts/README.md` | Add both files to the context table with owner and readers; add a rule that squad standards are binding and TBD rows stay open |
| `.github/contexts/project-context.md` §17 | Add both files to the source register |
| `.github/contexts/project-context.md` §18 | Add "read the squad backend/frontend standards" to required guidance |
| `README.md` §3.1 | Add both files to the read-first list |
| `AGENTS.md` §5 | Add a row "Squad backend and frontend standards" so the coding agent treats them as binding |

## Conflicts I found that must be decided

1. **`ADR-RCV-001-recovery-api-style.md` is cited but does not exist.** BS-3.1 relies on it as the recorded exception to ACE's HAL/Spring Data REST rule. Without it, the standards contradict `AGENTS.md` §2 and `backend-context.md` §1, and the "ACE rules win" preamble means the exception cannot apply.
2. **`D-RCV-02` to `D-RCV-10` are not in the repo.** No `D-RCV-*` entry exists in the decision log or decision folder. The standards cite these decisions throughout, so traceability is broken.
3. **BS-2.2 changes an already-written spec.** `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` currently says `db/migration/recovery`, `${schema}` and `V<number>__<description>.sql`. BS-2.2 says `db/modulemigration/<module>/`, `${recoverySchema}` and `V<epic>_<story>__<name>.sql`. That spec would need re-running, not hand-editing.
4. **FS-2.4 conflicts with an approved source.** It says accessibility target is TBD (example WCAG 2.1 AA), but `recovery-workbench-accessibility-standard-v2-docx.md` and the design system already mandate **WCAG 2.2 AA**. Per the standards' own preamble, the ACE/source rule wins; the TBD should be raised, not silently replaced.

## What I recommend

Copy both files verbatim, integrate the rules into the two context files, update the five indexes, and create the missing `adr-rcv-001-recovery-api-style.md` plus a small `D-RCV` decision register so the citations resolve. Leave every TBD row as an open item; do not fill them in.

Before I switch to implementation, three scope choices:

<details><summary>Reasoning</summary>

Confirmed conflicts:
- E1-044 spec uses `recovery/src/main/resources/db/migration/recovery`, `${schema}`, `V<number>__<description>.sql`, baseline `V1__rwb_e1_001_baseline.sql`. The new BS-2.1 says `db/modulemigration/<module>/`, `${recoverySchema}`, `V<epic>_<story>__<name>.sql` e.g. `V1_044__flyway_baseline.sql`, header `-- Story: <story key>`. So the standards directly change an already-specified story. That's a significant impact to flag.
- Accessibility: existing source says WCAG 2.2 AA; FS-2.4 TBD. So FS-2.4 conflicts with an approved ACE/source standard. Per the standards' own preamble, ACE rules win until exception. So carry existing WCAG 2.2 AA and mark FS-2.4 as "TBD — existing source states WCAG 2.2 AA; FDA to confirm". Do not overwrite.

Also `BS-4.1` says roles TBD but existing Users, Roles and Permissions v3 has 54 roles. Perhaps module role names are separate. Keep TBD.

`FS-1.3` route prefix TBD; existing ADR-006 just says module folder. Keep TBD.

Now, the user's request is likely simpler than all this. They want to know where to add the context. I should give a clear recommendation and plan, with the conflict flags, and ask whether to also create ADR-RCV-001 and the squad decision register, or just add the standards. Since Plan mode says discuss plan directly in conversation; do not create files. So I'll present:

1. Recommended placement (primary + integration + indexes).
2. Exact sections/edits.
3. Conflicts/open items to handle.
4. Ask for decisions on scope.

I should be concise but complete. Let me draft the plan.

Let me define exact insertion points:

### A. New files (verbatim)
- `.github/contexts/backend-standards.md` ← copy of attached backend-standards.md
- `.github/contexts/frontend-standards.md` ← copy of attached frontend-standards.md

Why not `docs/` or `.github/rules/`:
- `.github/rules/` is toolkit-owned generic rules (Flutter examples etc.).
- `requirement/legacy/` is the converted 411-entry corpus; adding new files there breaks the corpus/map.
- `.github/contexts/` is explicitly the project context + user-provided standards folder, and all agents inspect it.

### B. Integrate into existing context files
`backend-context.md`:
- Add a new section after §12: `## 13. Squad backend standards (USER-PROVIDED)` with a compact table:
  - BS-1.1–1.5 module structure (recovery module, nested modules, api/internal, no cross-module entity access, boundary tests, no extension of ACE controller/service/model)
  - BS-2.1–2.6 DB/migrati

_[truncated]_

</details>

**Tool `question`** - completed

```json
{"questions": [{"question": "How should the two standards files be added?", "header": "Placement", "options": [{"label": "Copy + integrate + index (Recommended)", "description": "Copy both files verbatim into .github/contexts/, add the rules to backend-context.md and frontend-context.md, and update README/AGENTS/project-context indexes."}, {"label": "Copy + index only", "description": "Preserve both files verbatim in .github/contexts/ and index them, but do not merge the rules into backend-context.md or frontend-context.md."}, {"label": "Integrate only", "description": "Merge the rules into backend-context.md and frontend-context.md without keeping standalone standards files."}]}, {"question": "Should I also create the documents the standards cite but that are missing?", "header": "Missing ADR/decisions", "options": [{"label": "Create ADR + decision register (Recommended)", "description": "Add adr-rcv-001-recovery-api-style.md and a D-RCV-01..10 register so BS-3.1 and the D-RCV citations resolve."}, {"label": "Record as gaps only", "description": "Do not create them; add CTX-GAP entries noting ADR-RCV-001 and D-RCV-* are referenced but absent."}, {"label": "Skip for now", "description": "Add the standards as-is and leave the dangling references unresolved."}]}, {"question": "How far should the index updates go?", "header": "Index scope", "options": [{"label": "All five indexes (Recommended)", "description": "Update contexts/README.md, project-context.md §17 and §18, repositor
... truncated
```

```text
User has answered your questions: "How should the two standards files be added?"="Unanswered", "Should I also create the documents the standards cite but that are missing?"="Unanswered", "How far should the index updates go?"="Unanswered". You can now continue with the user's answers in mind.
```

### Assistant - 2026-11-04 23:56 | opencode-go/deepseek-v4.1-flash | plan

The questions were left unanswered, so here is the concrete change set I recommend. Nothing has been modified.

## Proposed change set

### New files (verbatim copies)
- `.github/contexts/backend-standards.md`
- `.github/contexts/frontend-standards.md`

### Context integration
- **`.github/contexts/backend-context.md`** — new section `13. Squad backend standards (USER-PROVIDED)` covering BS-1 to BS-5, plus cross-references in §2 (module boundaries), §3 (API base path and plain JSON), §4 (migration location and naming), §6 (security), and §9 (batch/scheduling). Add the TBD items to §12.
- **`.github/contexts/frontend-context.md`** — new section `10. Squad frontend standards (USER-PROVIDED)` covering FS-1 to FS-4, plus cross-references in §1 (module folder), §5 (design system), §6 (plain JSON API, no HAL), and §8 (Playwright ports). Add the TBD items to §9.

### Index updates
- `.github/contexts/README.md` — add both files to the table and note that squad standards are binding, TBD rows are open.
- `.github/contexts/project-context.md` §17 — add both files to the source register.
- `.github/contexts/project-context.md` §18 — add the squad standards to required reading.
- `README.md` §3.1 — add both files to the read-first list.
- `AGENTS.md` §5 — add a "Squad backend and frontend standards" row.

### Missing references to resolve
- Create `docs/architecture/decisions/adr-rcv-001-recovery-api-style.md` and add it to `docs/architecture/decisions/README.md`. Without it, BS-3.1's HAL exception has no recorded basis and contradicts `AGENTS.md` §2.
- Add a small `D-RCV-01` to `D-RCV-10` register (in the decisions README or a new `squad-decisions.md`). The standards cite these but no such IDs exist in the repo.
- Record BS-2.2 as a change to `RWB-E1-044`: the existing spec uses `db/migration/recovery`, `${schema}` and `V<number>__<description>.sql`; the standard changes the folder, placeholder and naming. That spec needs re-running, not hand-editing.

### Do not do
- Do not rewrite the two standards files — they are user-owned.
- Do not fill in any **TBD** row.
- Do not place them in `.github/rules/` (toolkit-owned) or `requirement/legacy/` (canonical corpus).
- Do not edit generated specs by hand.

Confirm this scope (or tell me to drop the ADR/decision-register and index changes), then switch to the build agent and I'll make the edits.

<details><summary>Reasoning</summary>

The user didn't answer. They may have dismissed. I should provide a concise recommendation and await confirmation. Since I'm in Plan mode, I can't implement. Let me summarize the final proposed change set and ask them to confirm / switch agents.

I should be clear and not overly long. Provide the concrete file list and the exact edits. Then say "confirm and switch to build agent".

Let me make the final response actionable.

</details>
