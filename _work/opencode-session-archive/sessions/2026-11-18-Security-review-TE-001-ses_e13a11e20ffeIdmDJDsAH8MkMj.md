# Security review TE-001

- **Session ID:** `ses_e13a11e20ffeIdmDJDsAH8MkMj`
- **Created:** 2026-11-18 08:56  |  **Last activity:** 2026-11-18 09:25
- **Model:** `opencode-go/deepseek-v4.1-flash`  |  **Agent:** `general`
- **Parent session:** Implementation verification (`ses_e13fa37feffeVx4Vlyz4X6NtKl`)
- **Tokens:** 71,327 in / 2,529 out / 1,920 reasoning
- **Messages:** 19

---

### User - 2026-11-18 08:56

You are a subagent spawned by another session.
You are the security reviewer performing the mandatory pre-merge **security review** for story RWB-TE-001.

Read `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\RUN-BRIEF.md`, `AGENTS.md`, `aisdlc\.github\rules\security-quality-standards.md`, `aisdlc\.github\contexts\backend-standards.md`, `frontend-standards.md` and the TE-001 spec at `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md`.

Review the whole story diff:
`git -C "C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001" diff develop-recovery...feature/RWB-TE-001-module-boundary`
and the changed files in full where needed.

The change is structural: package relocation, module boundary rules, a YAML module map loader, ArchUnit/Modulith tests, a coverage gate and a frontend ESLint import-boundary test. Check specifically:
- any secret, credential, token, connection string or PII in code, tests, fixtures, YAML or logs;
- unsafe file/path handling in the module-map loader (path traversal, symlink, YAML bomb/alias, duplicate keys, entity expansion, unbounded input);
- dependency or build-script injection (no new dependency, no arbitrary code execution, no untrusted input into Gradle/ESLint);
- authorization/authentication regressions from moving `SecurityConfig`, `ApiExceptionHandler`, `ProblemFactory` or controllers (package-private/public visibility changes, method security still applies, no endpoint left unguarded);
- the frontend ESLint rule cannot be bypassed by the allowed import list or by a path alias;
- log lines and test fixtures contain no personal data or real identifiers.

Every finding needs a concrete exploit or failure case, severity (Critical/High/Medium/Low), file:line, and the smallest fix. Do not invent issues; if clean, say clean and list what you checked.

Write only `aisdlc/output/INC-002-epic-1-RWB-TE-001/review/security-review.md`. Do not edit code, tests, plans or shared files. Do not ask the user anything.

Report in under 200 words: overall verdict, counts by severity, and finding headlines.

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

I'll start by reading the required context files and the diff.

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\RUN-BRIEF.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\RUN-BRIEF.md, lines 1-97
1: # Run brief for every lifecycle agent in this repository
2: 
3: Read this before you start. It adapts the AISDLC v2 agent instructions to this repository's layout.
4: It does not change any gate, rule or output name in your instructions.
5: 
6: ## Paths
7: 
8: | Name in your instructions | Path here |
9: |---|---|
10: | Workspace root (`.github/`, `docs/`, `requirement/`, `output/`) | `<repo>/aisdlc/` |
11: | ACE monorepo / code repository / `ace-monorepo/` | `<repo>/` (this repository's root; local stand-in for ACE) |
12: | `ace-monorepo/AGENTS.md`, coding standard | `<repo>/AGENTS.md`, `<repo>/aisdlc/.github/contexts/backend-standards.md`, `frontend-standards.md` |
13: | `requirement/legacy/` (the converted document set v14) | `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` (read only) |
14: | Story file paths in the increment cards | relative to `<docset>/17 AI-First SDLC Repository v2/` |
15: | Earlier v2 artefacts for your story, if any | `<repo>/aisdlc/output/<RUN_ID>/_v2-baseline/` (history: reuse what is still correct, never overwrite) |
16: 
17: `<repo>` is `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench`.
18: `<docset>` is `C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14`.
19: 
20: ## Hard rules for this run
21: 
22: 1. **Never change anything in `<docset>` outside `<repo>`.** The document set is read only. A
23:    document that is wrong or silent is recorded as a gap (below), never edited.
24: 2. **Write only to your own stage folder**, `aisdlc/output/<RUN_ID>/<stage>/`. The Implementation Builder
25:    also writes code, and only in the git worktree it is given.
26: 3. **Shared files are not yours.** Do not edit `aisdlc/docs/open-items.md`,
27:    `aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/increments/INDEX.md`, the increment cards
28:    or `aisdlc/DOCUMENT-GAPS.md`. Agents run in parallel. Write the rows you would add to
29:    `aisdlc/output/<RUN_ID>/<stage>/shared-updates.md`, and the orchestrator applies them in order.
30:    The Traceability Manager is the exception: it may edit `Traceability_Matrix.md`.
31: 4. **No question to the user** (L-RCV-03). Record assumptions in your stage's `assumptions.md`.
32: 5. **No Jira, Confluence, GitLab or Figma MCP is connected.** Follow your instructions' fallback
33:    pa
... truncated (7,401 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\AGENTS.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\AGENTS.md, lines 1-194
1: # Recovery Workbench — AI engineering standards (v2)
2: 
3: This is the standards file the coding agent reads before every task, as defined in
4: `Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
5: module of the ACE service and to anyone using an AI tool on this repository.
6: 
7: **Owner:** Solution architect with the TechX tech leads.
8: **Change control:** pull request, reviewed like code.
9: **Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
10: (`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
11: **Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
12: and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.
13: 
14: ## 1. The seven working rules
15: 
16: 1. The person who merges a change owns it, whoever or whatever wrote it.
17: 2. The agent works from files: the standards file, the story file and the plan file. Anything the
18:    agent needs is in one of the three.
19: 3. The tests and the acceptance criteria exist before the code is generated.
20: 4. Every line that reaches production is read by a person.
21: 5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
22: 6. No personal data or production data goes into a prompt, a test or a log.
23: 7. The unit of work is one story. Work is merged at least once a working day.
24: 
25: ## 2. Structure and stack
26: 
27: - The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
28: - Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
29:   Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
30: - Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
31:   back end.
32: - Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
33:   `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
34:   versioned migrations, one migration per story, forward-only. Files are named
35:   `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence 
... truncated (12,923 chars total)
```

> **Synthetic** - 2026-11-18 08:56

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\AGENTS.md
# Recovery Workbench — AI engineering standards (v2)

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
(`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.

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
- Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
  `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
  versioned migrations, one migration per story, forward-only. Files are named
  `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order and line 1
  is `-- Story: <story key>`.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. From Epic 3 the case lifecycle runs on Temporal; case data stays in the recovery
  schema (D-RCV-36, ADR-011).
- Rules are versioned data, authored as Drools XLS decision-table packages and evaluated by embedded
  Drools (D-RCV-36, ADR-012).
- Hosting: the ACE namespace on the shared ACE AKS clusters; Temporal is self-hosted in the same
  namespace.

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
7. Make database changes by migration script only, one script per story. Name it
   `V<seq>__<story>_<name>.sql`; line 1 is `-- Story: <story key>`. A corrective script takes the
   next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>` (D-RCV-28).
8. Use Spring Batch and Quartz for every Epic 1...

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Let me continue reading the other required files. Note that paths given: `aisdlc\.github\rules\security-quality-standards.md`, `aisdlc\.github\contexts\backend-standards.md`, `frontend-standards.md`, and spec at `aisdlc/output/INC-002-epic-1-RWB-TE-001/specify/spec.md`. Note repo root is `18 E2E Recovery Workbench`. Let me read them.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\.github\\rules\\security-quality-standards.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\.github\rules\security-quality-standards.md, lines 1-43
1: ---
2: description: Security, privacy, quality, and review gates for in-scope PDLC changes.
3: ---
4: 
5: # Security & Quality Standards
6: 
7: ## Security
8: - Enforce authentication on protected routes, actions, and frontend integration calls.
9: - Enforce authorization using roles, entitlements, account ownership, relationship-manager assignment, and maker-checker rules where applicable.
10: - Enforce safe client-side input handling, output encoding, and platform-appropriate XSS/CSRF protections for Flutter and web deployments.
11: - Never log plaintext PII, account numbers, portfolio holdings, tokens, secrets, or credentials.
12: - Protect sensitive data in transit and in browser storage according to the approved platform standard.
13: - Use centralized secret management; no hardcoded secrets.
14: - Include correlation IDs in logs.
15: - Audit sensitive actions such as login, profile updates, risk-profile changes, suitability decisions, order submission, approval, cancellation, document access, and data export.
16: 
17: ## Privacy And Compliance
18: Apply only when in scope:
19: - Thailand PDPA consent and privacy controls.
20: - KYC and AML checks.
21: - Suitability and risk profiling.
22: - Product eligibility restrictions.
23: - Advisory disclosure and consent capture.
24: - Data retention and deletion rules.
25: - Regulatory reporting and audit evidence.
26: 
27: ## Quality
28: - Unit tests are mandatory for each frontend/backend surface requiring changes before implementation handoff. Use an 80% passing threshold independently for lines, statements, branches, and functions where supported; Flutter requires executable-line coverage. All layers, including validation, API endpoints, UI components, and utilities, use the same 80% gate; measured coverage may exceed it.
29: - Verify actual unit-test execution and native coverage reports. Show separate frontend/backend test counts, coverage metrics, commands, and evidence paths. Failed tests, below-threshold coverage, or missing execution/coverage evidence block implementation completion.
30: - Apply unit-test and coverage gates only to surfaces requiring changes in the story. If no backend changes are required or made, skip backend unit tests and coverage; apply the same rule to unchanged frontend. Report `NO
... truncated (3,506 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\.github\\contexts\\backend-standards.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\.github\contexts\backend-standards.md, lines 1-99
1: # Recovery Workbench — backend standards
2: 
3: **Context ID:** `CTX-BACKEND-STANDARDS-V2`
4: **Version:** 2.0, 16 November 2026
5: **Applies to:** `th.co.scb.ace.demo.recovery` in the ACE monorepo.
6: 
7: ## BS-1 Module structure
8: 
9: - **BS-1.1** One Spring Modulith application module `recovery`. Inside it, nested application modules
10:   for P1–P10 and S1–S9, each with `api` and `internal`.
11: - **BS-1.2** A module exposes only `api` interfaces; an `internal` class, entity or repository is never
12:   injected or imported by another module.
13: - **BS-1.3** The module map is `backend/src/test/resources/architecture/recovery-modules.yaml`; the
14:   build reads it, the jar does not package it.
15: - **BS-1.4** BND-1–BND-5 are ArchUnit/Modulith tests in `RecoveryBoundaryTest`. **BND-6** forbids a
16:   recovery class from naming a `public` table; it fails the build. BND-1/BND-2 use
17:   `allowEmptyShould(true)` until those packages exist.
18: - **BS-1.5** No new dependency without plan approval. Approved for this baseline: Testcontainers
19:   PostgreSQL, JaCoCo, Vitest (front end), Drools KIE runtime (ADR-012), Temporal SDK (ADR-011).
20: 
21: ## BS-2 Database and migrations
22: 
23: - **BS-2.1** Schema `recovery`. Always reference it as `${recoverySchema}`; never a literal.
24: - **BS-2.2** One migration file per story: `V<seq>__<story>_<name>.sql`; 4-digit contiguous sequence
25:   taken at merge; line 1 `-- Story: <key>`. A corrective file takes the next sequence, keeps the story
26:   key and adds line 2 `-- Fix: <reason>`. No `R__*.sql`.
27: - **BS-2.3** Flyway: own bean, folder `db/modulemigration/recovery/`, history table
28:   `flyway_schema_history_recovery`, `outOfOrder(false)`, `baselineVersion("0")`,
29:   `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`.
30: - **BS-2.4** Never edit a merged migration. A change is a new corrective file.
31: - **BS-2.5** Recovery migrations contain no `GRANT`/`REVOKE`; the view grants live in the view story
32:   and are executed by the migration account with the ACE DBA role for the release window.
33: - **BS-2.6** Lint as a unit test: name, sequence, one non-fix file per story, header, no literal
34:   schema, no `SET search_path`, no repeatable file, no `GRANT`/`REVOKE`.
35: - **BS-2.7
... truncated (6,629 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\.github\\contexts\\frontend-standards.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\.github\contexts\frontend-standards.md, lines 1-74
1: # Recovery Workbench — frontend standards
2: 
3: **Context ID:** `CTX-FRONTEND-STANDARDS-V2`
4: **Version:** 2.0, 16 November 2026
5: **Applies to:** `frontend/src/modules/recovery/` in the ACE front end.
6: 
7: ## FS-1 Structure and imports
8: 
9: - **FS-1.1** Every recovery screen, component, hook, type and test lives under
10:   `frontend/src/modules/recovery/`.
11: - **FS-1.2** Imports outside the folder are limited to `@/components/ui/**`, `@/lib/utils`, top-level
12:   `@/utils/*` except `cfsc*`, `@/contexts/ApiClientContext` and `@/api/schema`. Inside the folder,
13:   `@/modules/recovery/**` and `./…` are allowed. `../…` and every other `@/` import are forbidden.
14:   ESLint `no-restricted-imports` is scoped to the folder; a fixture test proves it fires.
15: - **FS-1.3** Routes live under `/recovery/*` and register in one "Recovery" menu group in `AceLayout`.
16:   The `App.tsx` and `AceLayout.tsx` edits are shared-file changes announced to the ACE team.
17: - **FS-1.4** No new UI library, icon set, state manager or HTTP client.
18: 
19: ## FS-2 Design system and visual rules
20: 
21: - **FS-2.1** Use ACE design-system components and tokens. The Henka screen specification gives layout,
22:   content, labels and behaviour; it does not override the ACE component look.
23: - **FS-2.2** One primary action per screen; destructive actions need a confirmation and a reason.
24: - **FS-2.3** Thai and English through i18next; default Thai; no string literal in a component.
25: - **FS-2.4** Use the bank timezone (Asia/Bangkok). Date-only and date-time are explicit.
26: - **FS-2.5** Amounts use the Thai baht format and the product currency; no float arithmetic in the UI.
27: - **FS-2.6** No pixel-perfect copy of a prototype; use tokens and the nearest design-system component.
28: 
29: ## FS-3 Screen behaviour
30: 
31: - **FS-3.1** Every screen has loading, empty, error, forbidden and expired-session states.
32: - **FS-3.2** Tables use the shared pagination, empty, loading and error patterns; server-side paging.
33: - **FS-3.3** Forms validate on blur and on submit; errors use the message ID and exact wording.
34: - **FS-3.4** Dialogs trap focus, close on Escape and return focus to the trigger.
35: - **FS-3.5** Long-running work shows progress, a cancel where allowe
... truncated (4,766 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\output\\INC-002-epic-1-RWB-TE-001\\specify\\spec.md"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\output\INC-002-epic-1-RWB-TE-001\specify\spec.md, lines 1-248
1: ---
2: title: "Technical Specification: RWB-TE-001 Recovery module folder and boundary test"
3: run_id: "INC-002-epic-1-RWB-TE-001"
4: story: "RWB-TE-001"
5: epic: "EPIC-001"
6: status: "SUCCESS"
7: revision: "v4 (spec gate round 2 remediation of REVIEW-RWB-TE-001-029..032; v3 kept as spec.run2.md). Round 3: text-only addition to SPEC-022 (d) for finding 033, no design change; the round-2 text is kept as spec.run3.md. Round 4: SPEC-022 (d) names all three E1-039 edges (finding 035), text only; the round-3 text is kept as spec.run4.md"
8: prepared: "2026-11-18"
9: ---
10: 
11: # Technical Specification: RWB-TE-001 Recovery module folder and boundary test
12: 
13: | Field | Value |
14: |---|---|
15: | Story / epic | `RWB-TE-001` / `EPIC-001` (increment card `aisdlc/docs/increments/INC-002-epic-1-RWB-TE-001.md`). The earlier Jira key `TB0001-1235` is history only (finding 028). |
16: | Module | P2 Integration (technical enabler); build order 2 of 72 (card) |
17: | RUN_ID | `INC-002-epic-1-RWB-TE-001` |
18: | Code repository | This repository (`<repo>`, RUN-BRIEF "Paths"). Backend root package `th.co.scb.ace.demo.recovery`; frontend folder `frontend/src/modules/recovery/`. |
19: | Source requirement | [S] story file v7, RWB-TE-001 v1 (28 Oct 2026), the canonical version (D-RCV-51) |
20: | Governing decisions | D-RCV-35 §8.2, D-RCV-36 §3.3 (client decisions, highest precedence); ADR v3 (ADR-002, ADR-010); Decision Log v10 (DL05 option B, DL07, DL36); D-RCV-02, -05, -10, -11, -19, -21, -28 (3), -37..-44, -51, -52; L-RCV-03, L-RCV-14 |
21: | Supersedes | `_v2-baseline/specify/spec.md` (16 Nov 2026). Its ACE-monorepo evidence (commit `96b0d1c6`, Nx, `DemoApplication`, 13 `Type.OPEN` packages) is **history only** and is not used here. |
22: | Status | `SUCCESS`. Every source conflict is settled by precedence or a labelled assumption (`assumptions.md`); no blocker gap (`document-gaps.md`). v4 fixes round-2 findings 029–032 (`gate-response.md` Round 2). Round 3 adds text for findings 033 and 034, and round 4 for finding 035, without a design change (`gate-response.md` Rounds 3 and 4). |
23: 
24: ## Source keys
25: 
26: | Key | Document (name, version) and path |
27: |---|---|
28: | [S] | Story file v7, RWB-TE-001 v1: `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-stor
... truncated (52,312 chars total)
```

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Let me read the rest of the spec, and then get the diff.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\18 E2E Recovery Workbench\\aisdlc\\output\\INC-002-epic-1-RWB-TE-001\\specify\\spec.md", "offset": 248}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\18 E2E Recovery Workbench\aisdlc\output\INC-002-epic-1-RWB-TE-001\specify\spec.md, lines 248-350
248: 
249: Output is the test report and ESLint output. No runtime metric, no flag; rollback is a revert merge request. The plan records the boundary test duration.
250: 
251: ### No UI change
252: 
253: `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`.
254: 
255: ## Test scenarios
256: 
257: | ID | Covers | Level | Data | Expected |
258: |---|---|---|---|---|
259: | TC-TE-001-01 | AC1, BR1 | Unit (fixture) | `recovery.casewf.internal.SampleService` → `collection.internal.CollectorRepository` | BND-1 fails; text names BND-1, both classes |
260: | TC-TE-001-02 | AC2, BR2 | Unit (fixture) | `SampleService` → interface in `common.api` | Passes |
261: | TC-TE-001-03 | AC3, BR3 | Unit (fixture) | `recovery.integration.internal` class → `recovery.decision.internal.DecisionLogRepository`; then → `recovery.decision.writer.DecisionLogWriter` (published in fixture map and `@NamedInterface`) | `verify()` fails (Modulith text); then passes |
262: | TC-TE-001-04 | AC4, BR4 | Unit (fixture) | `recovery.integration.internal` class using `@Entity recovery.casewf.internal.RecoveryCaseEntity`; and an entity outside the recovery root | BND-4 fails on both |
263: | TC-TE-001-05 | AC5, BR5 | Unit (fixture) | `java.net.http.HttpClient` and a `com.azure.storage` type in `recovery.casewf.internal`; same in `recovery.integration.adapter` | Fails in `casewf`; passes in `integration.adapter` |
264: | TC-TE-001-06 | AC6 | Unit (frontend, Vitest) | `src/modules/recovery/caselist/<File>.tsx` importing `@/modules/collection/worklist/WorkList` and `../../collection/worklist/WorkList` | `no-restricted-imports` error for each |
265: | TC-TE-001-07 | AC7, BR6 | Unit (fixture) | Package `recovery.vendorx` absent from the fixture map | Fails: `… recovery.vendorx is not in the module map` |
266: | T-TE001-01 | SPEC-003 | Unit | Valid map; with `sourceViews`; missing file; invalid YAML; missing field; duplicate code; duplicate name; bad pattern; `internal` as published; unknown key | Valid and `sourceViews` pass; each error names file and field |
267: | T-TE001-02 | SPEC-004 | Unit (fixture) | Map module without package; type in root package; `@NamedInterface` package not in map; published package without `@NamedInterface`; classes only in a sub-package of an unmapped package; public type in a module base package; type-level `@NamedI
... truncated (14,464 chars total)
```

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" status --short; git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" log --oneline -5; git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff --stat develop-recovery...feature/RWB-TE-001-module-boundary"}
```

```text
473f0af RWB-TE-001: frontend import boundary test, green (TASK-15, TASK-16)
8bad2e7 RWB-TE-001: coverage tests for the relocated classes, gate passes (TASK-12)
5df3097 RWB-TE-001: module skeleton, relocation and property split, green (TASK-11)
220138d RWB-TE-001: Modulith fixture proof, real-code boundary test and binding tests, red (TASK-08, TASK-09, TASK-10)
e34f42a RWB-TE-001: map-driven boundary rules, green (TASK-07)
 backend/build.gradle.kts                           |  24 +-
 .../{platform => access}/api/ApiError.java         |  10 +-
 .../api/ApiProblemException.java                   |   2 +-
 .../ace/demo/recovery/access/api/package-info.java |   3 +
 .../internal/ApiExceptionHandler.java              |   8 +-
 .../internal/ProblemFactory.java                   |   4 +-
 .../internal/RecoverySecurityProperties.java       |  14 +
 .../internal/SecurityConfig.java                   |  18 +-
 .../recovery/access/internal/package-info.java     |   2 +
 .../scb/ace/demo/recovery/access/package-info.java |   3 +
 .../ace/demo/recovery/agent/api/package-info.java  |   3 +
 .../demo/recovery/agent/internal/package-info.java |   2 +
 .../scb/ace/demo/recovery/agent/package-info.java  |   3 +
 .../ace/demo/recovery/asset/api/package-info.java  |   3 +
 .../demo/recovery/asset/internal/package-info.java |   2 +
 .../scb/ace/demo/recovery/asset/package-info.java  |   3 +
 .../admin}/TemporalAdminController.java            |  12 +-
 .../ace/demo/recovery/casewf/api/package-info.java |   3 +
 .../recovery/casewf/internal/package-info.java     |   2 +
 .../migration}/RecoveryFlywayConfig.java           |   8 +-
 .../migration/RecoveryMigrationProperties.java     |  15 +
 .../scb/ace/demo/recovery/casewf/package-info.java |   3 +
 .../api => casewf/rules}/CompiledRulePackage.java  |   2 +-
 .../rules}/DroolsProperties.java                   |   2 +-
 .../rules}/DroolsRuleEngine.java                   |  14 +-
 .../{rules/api => casewf/rules}/RuleEngine.java    |   2 +-
 .../{rules/api => casewf/rules}/RuleInput.java     |   2 +-
 .../{rules/api => casewf/rules}/RuleOutcome.java   |   2 +-
 .../{rules/api => casewf/rules}/RuleResult.java    |   2 +-
 .../demo/recovery/casewf/rules/package-info.java   |   3 +
 .../api => casewf/timers}/TimerScheduler.java      |   2 +-
 .../timers}/internal/QuartzTimerScheduler.java     |   4 +-
 .../demo/recovery/casewf/timers/package-info.java  |   3 +
 .../api => casewf/workflow}/WorkflowIds.java       |   2 +-
 .../workflow/in
... truncated (14,182 chars total)
```

### Assistant - 2026-11-18 08:56 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Now let me look at the actual diff in full. It's large (3632 insertions). Let me get the diff to a file or read key files in full. I need to focus on security-critical files:

- `backend/build.gradle.kts` diff
- `access/internal/SecurityConfig.java`
- `access/internal/ApiExceptionHandler.java`, `ProblemFactory`
- `access/api/ApiError.java`, `ApiProblemException`
- `ModuleMapLoader.java` (path handling, YAML)
- `BoundaryRules.java`
- `RecoveryBoundaryTest.java`
- `frontend/src/modules/recovery/__tests__/importBoundary.test.ts`
- `frontend/eslint.config.js` (not changed but relevant)
- YAML fixtures
- Properties split files
- Test fixtures for PII

Let me get the diff into a temp file and read portions. Better: use shell to write diff to temp file then read. Let me first check the worktree files directly since they're full files.

Let me look at the structure and read the key files.

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff develop-recovery...feature/RWB-TE-001-module-boundary -- backend/build.gradle.kts \"backend/src/main/java/th/co/scb/ace/demo/recovery/access\" backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/ModuleMapLoader.java backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/boundary/ModuleMap.java > \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001-core.diff\"; (Get-Item \"C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001-core.diff\").Length"}
```

```text
67994

```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\ModuleMapLoader.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\ModuleMapLoader.java, lines 1-240
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import java.io.IOException;
4: import java.nio.file.Files;
5: import java.nio.file.Path;
6: import java.util.ArrayList;
7: import java.util.LinkedHashMap;
8: import java.util.LinkedHashSet;
9: import java.util.List;
10: import java.util.Map;
11: import java.util.Set;
12: import java.util.regex.Pattern;
13: 
14: import org.yaml.snakeyaml.LoaderOptions;
15: import org.yaml.snakeyaml.Yaml;
16: import org.yaml.snakeyaml.constructor.SafeConstructor;
17: import org.yaml.snakeyaml.error.YAMLException;
18: 
19: /**
20:  * RWB-TE-001 SPEC-003 (BR6): reads the module map into {@link ModuleMap}. Every malformed map is
21:  * refused with {@code <file>: <field path>: <problem>}; the optional {@code sourceViews} key is
22:  * carried unvalidated for RWB-E1-069. No package literal: the root comes from the map.
23:  */
24: public final class ModuleMapLoader {
25: 
26: 	private static final Pattern CODE = Pattern.compile("^(P([1-9]|10)|S[1-9])$");
27: 
28: 	private static final Pattern NAME = Pattern.compile("^[a-z][a-z0-9]*$");
29: 
30: 	private static final Pattern PACKAGE = Pattern.compile("^[a-z][a-z0-9]*(\\.[a-z][a-z0-9]*)*$");
31: 
32: 	private static final Pattern JAVA_NAME = Pattern.compile("^[A-Za-z_$][A-Za-z0-9_$]*(\\.[A-Za-z_$][A-Za-z0-9_$]*)*$");
33: 
34: 	private static final Set<String> TOP_LEVEL_KEYS = Set.of("rootPackage", "modules", "external", "clientLibraries",
35: 			"sourceViews");
36: 
37: 	private static final Set<String> MODULE_KEYS = Set.of("code", "name", "published", "clientPackages");
38: 
39: 	private static final Set<String> EXTERNAL_KEYS = Set.of("name", "rootPackage", "published");
40: 
41: 	private static final Set<String> EXTERNAL_NAMES = Set.of("common", "collection");
42: 
43: 	private ModuleMapLoader() {
44: 	}
45: 
46: 	public static ModuleMap load(Path file) {
47: 		String source = file.getFileName().toString();
48: 		Map<String, Object> root = mapping(parse(source, file), "$", source);
49: 
50: 		for (String key : root.keySet()) {
51: 			if (!TOP_LEVEL_KEYS.contains(key)) {
52: 				throw fail(source, key, "unknown key");
53: 			}
54: 		}
55: 
56: 		String rootPackage = requiredString(root, "rootPackage", "rootPackage", source);
57: 		if (!PACKAGE.matcher(rootPackage).
... truncated (10,324 chars total)
```

> **Synthetic** - 2026-11-18 08:57

Instructions from: C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\AGENTS.md
# Recovery Workbench — AI engineering standards (v2)

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
(`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.

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
- Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
  `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
  versioned migrations, one migration per story, forward-only. Files are named
  `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order and line 1
  is `-- Story: <story key>`.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. From Epic 3 the case lifecycle runs on Temporal; case data stays in the recovery
  schema (D-RCV-36, ADR-011).
- Rules are versioned data, authored as Drools XLS decision-table packages and evaluated by embedded
  Drools (D-RCV-36, ADR-012).
- Hosting: the ACE namespace on the shared ACE AKS clusters; Temporal is self-hosted in the same
  namespace.

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
7. Make database changes by migration script only, one script per story. Name it
   `V<seq>__<story>_<name>.sql`; line 1 is `-- Story: <story key>`. A corrective script takes the
   next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>` (D-RCV-28).
8. Use Spring Batch and Quartz for every Epic 1 and Epi...

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

The loader: reads a Path, uses Files.readString, SafeConstructor, setAllowDuplicateKeys(false). Missing: `setMaxAliasesForCollections`, `setCodePointLimit`, `setNestingDepthLimit`, `setAllowRecursiveKeys`. Default SnakeYAML LoaderOptions: maxAliasesForCollections = 50, nestingDepthLimit = 50, codePointLimit = 3MB. So YAML bomb is partially limited by default. SafeConstructor prevents arbitrary object instantiation. But `setAllowDuplicateKeys(false)` is good. Path traversal: the loader accepts an arbitrary Path from the caller — it's a test-scope loader only. But it might be called with a path derived from config? Let me check how it's invoked (RecoveryBoundaryTest). Also whether the loader resolves symlinks — test-scope only reads test resources. Need to consider whether this is exploitable. Since it's test-scope and the file path is fixed, path traversal is not a real risk. But maybe the loader is used with a fixture map under test resources. Let's check.

Also `sourceViews` carried unvalidated as raw object — potential YAML alias bomb? SnakeYAML resolves anchors into shared object graphs, bounded by maxAliasesForCollections=50 default. Fine.

Important: `root.get("sourceViews")` is an opaque object, never serialized. Fine.

Also `Files.readString(file)` on an arbitrary path, plus error message includes full path — info disclosure only in build logs, low. Test scope. Not a real finding.

Now check `ModuleMap.java` and `BoundaryRules.java`, `RecoveryBoundaryTest`, `SecurityConfig`, `build.gradle.kts`, frontend test, ESLint config.

Let me read the core diff file.

</details>

**Tool `read`** - error

```json
{"path": "C:\\Users\\SahilMore\\AppData\\Local\\Temp\\opencode\\te001-core.diff"}
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

The file was written by PowerShell with UTF-16 probably. Let me read it via shell with Get-Content, or better use `git diff` piped to `Out-File -Encoding utf8`. Let me just read the key files directly in the worktree instead of the diff.

Files to read in full:
1. backend/src/main/java/.../access/internal/SecurityConfig.java
2. .../access/internal/ApiExceptionHandler.java
3. .../access/internal/ProblemFactory.java
4. .../access/internal/RecoverySecurityProperties.java
5. .../access/api/ApiError.java
6. backend/build.gradle.kts (and diff)
7. boundary/BoundaryRules.java
8. boundary/ModuleMap.java
9. RecoveryBoundaryTest.java
10. frontend/.../importBoundary.test.ts
11. frontend/eslint.config.js
12. YAML map + fixtures
13. integration/PlatformInfoController.java and properties
14. casewf/admin/TemporalAdminController.java
15. casewf/migration/RecoveryFlywayConfig.java
16. Tests with possible PII: SecurityConfigTest, BlobDocumentStoreTest, etc.

Let's read in parallel.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\main\\java\\th\\co\\scb\\ace\\demo\\recovery\\access\\internal\\SecurityConfig.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\access\internal\SecurityConfig.java, lines 1-120
1: package th.co.scb.ace.demo.recovery.access.internal;
2: 
3: import java.util.Collection;
4: import java.util.List;
5: import java.util.Map;
6: 
7: import org.springframework.context.annotation.Bean;
8: import org.springframework.boot.context.properties.EnableConfigurationProperties;
9: import org.springframework.context.annotation.Configuration;
10: import org.springframework.core.convert.converter.Converter;
11: import org.springframework.http.HttpMethod;
12: import org.springframework.security.authorization.AuthorizationDecision;
13: import org.springframework.security.authorization.AuthorizationManager;
14: import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
15: import org.springframework.security.config.annotation.web.builders.HttpSecurity;
16: import org.springframework.security.config.http.SessionCreationPolicy;
17: import org.springframework.security.core.Authentication;
18: import org.springframework.security.core.GrantedAuthority;
19: import org.springframework.security.core.authority.SimpleGrantedAuthority;
20: import org.springframework.security.oauth2.core.DelegatingOAuth2TokenValidator;
21: import org.springframework.security.oauth2.core.OAuth2Error;
22: import org.springframework.security.oauth2.core.OAuth2TokenValidator;
23: import org.springframework.security.oauth2.core.OAuth2TokenValidatorResult;
24: import org.springframework.security.oauth2.jwt.Jwt;
25: import org.springframework.security.oauth2.jwt.JwtDecoder;
26: import org.springframework.security.oauth2.jwt.JwtValidators;
27: import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
28: import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
29: import org.springframework.security.web.SecurityFilterChain;
30: import org.springframework.security.web.access.intercept.RequestAuthorizationContext;
31: import org.springframework.web.cors.CorsConfiguration;
32: import org.springframework.web.cors.CorsConfigurationSource;
33: import org.springframework.web.cors.UrlBasedCorsConfigurationSource;
34: 
35: import th.co.scb.ace.demo.recovery.access.api.ApiError;
36: 
37: /**
38:  * Entra ID bearer tokens (BS-4.1). Locally the issuer is the mock OIDC server; in SIT/UAT/PROD it is
39:  * the bank tenant. Ap
... truncated (6,992 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\main\\java\\th\\co\\scb\\ace\\demo\\recovery\\access\\internal\\ApiExceptionHandler.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\access\internal\ApiExceptionHandler.java, lines 1-57
1: package th.co.scb.ace.demo.recovery.access.internal;
2: 
3: import java.util.Map;
4: 
5: import org.slf4j.Logger;
6: import org.slf4j.LoggerFactory;
7: import org.springframework.http.HttpStatus;
8: import org.springframework.http.ProblemDetail;
9: import org.springframework.security.access.AccessDeniedException;
10: import org.springframework.web.bind.annotation.ExceptionHandler;
11: import org.springframework.web.bind.annotation.ResponseStatus;
12: import org.springframework.web.bind.annotation.RestControllerAdvice;
13: import org.springframework.web.servlet.resource.NoResourceFoundException;
14: 
15: import th.co.scb.ace.demo.recovery.access.api.ApiError;
16: import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
17: 
18: /**
19:  * Maps exceptions to {@code application/problem+json}. No exception text or stack trace reaches the
20:  * client; the message ID goes to the log (Error and Message Standard v4 Â§2).
21:  */
22: @RestControllerAdvice(basePackages = "th.co.scb.ace.demo.recovery")
23: class ApiExceptionHandler {
24: 
25: 	private static final Logger log = LoggerFactory.getLogger(ApiExceptionHandler.class);
26: 
27: 	private final ProblemFactory problems;
28: 
29: 	ApiExceptionHandler(ProblemFactory problems) {
30: 		this.problems = problems;
31: 	}
32: 
33: 	@ExceptionHandler(ApiProblemException.class)
34: 	ProblemDetail problem(ApiProblemException ex) {
35: 		log.warn("Recovery API problem {}", ex.error().messageCode(), ex.getCause());
36: 		return problems.problem(ex.error(), ex.placeholders());
37: 	}
38: 
39: 	@ExceptionHandler(AccessDeniedException.class)
40: 	ProblemDetail forbidden(AccessDeniedException ex) {
41: 		return problems.problem(ApiError.NOT_PERMITTED, Map.of("action", "do this"));
42: 	}
43: 
44: 	@ExceptionHandler(NoResourceFoundException.class)
45: 	ProblemDetail notFound(NoResourceFoundException ex) {
46: 		return problems.problem(ApiError.NOT_IN_SCOPE, Map.of());
47: 	}
48: 
49: 	@ExceptionHandler(Exception.class)
50: 	@ResponseStatus(HttpStatus.INTERNAL_SERVER_ERROR)
51: 	ProblemDetail unexpected(Exception ex) {
52: 		log.error("Unhandled recovery API error", ex);
53: 		ProblemDetail p = ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);
54: 		p.setTitle("Internal Server Error");
55: 		return p;
56: 	}
57:
... truncated (2,502 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\main\\java\\th\\co\\scb\\ace\\demo\\recovery\\access\\internal\\ProblemFactory.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\access\internal\ProblemFactory.java, lines 1-52
1: package th.co.scb.ace.demo.recovery.access.internal;
2: 
3: import java.io.IOException;
4: import java.net.URI;
5: import java.util.Map;
6: 
7: import io.micrometer.tracing.Tracer;
8: import jakarta.servlet.http.HttpServletResponse;
9: import org.springframework.beans.factory.ObjectProvider;
10: import org.springframework.http.HttpStatus;
11: import org.springframework.http.MediaType;
12: import org.springframework.http.ProblemDetail;
13: import org.springframework.stereotype.Component;
14: import tools.jackson.databind.json.JsonMapper;
15: 
16: import th.co.scb.ace.demo.recovery.access.api.ApiError;
17: 
18: /** Builds API Specification v4 {@code Problem} bodies, in controllers and in the security filters. */
19: @Component
20: class ProblemFactory {
21: 
22: 	private final ObjectProvider<Tracer> tracer;
23: 	private final JsonMapper json;
24: 
25: 	ProblemFactory(ObjectProvider<Tracer> tracer, JsonMapper json) {
26: 		this.tracer = tracer;
27: 		this.json = json;
28: 	}
29: 
30: 	ProblemDetail problem(ApiError error, Map<String, String> placeholders) {
31: 		HttpStatus status = HttpStatus.valueOf(error.status());
32: 		ProblemDetail p = ProblemDetail.forStatusAndDetail(status, error.english(placeholders));
33: 		p.setType(URI.create("urn:rwb:problem:" + error.messageCode()));
34: 		p.setTitle(status.getReasonPhrase());
35: 		p.setProperty("messageCode", error.messageCode());
36: 		p.setProperty("messageTh", error.thai(placeholders));
37: 		p.setProperty("traceId", traceId());
38: 		return p;
39: 	}
40: 
41: 	void write(HttpServletResponse response, ApiError error, Map<String, String> placeholders) throws IOException {
42: 		response.setStatus(error.status());
43: 		response.setContentType(MediaType.APPLICATION_PROBLEM_JSON_VALUE);
44: 		response.setCharacterEncoding("UTF-8");
45: 		json.writeValue(response.getOutputStream(), problem(error, placeholders));
46: 	}
47: 
48: 	private String traceId() {
49: 		Tracer t = tracer.getIfAvailable();
50: 		return t != null && t.currentSpan() != null ? t.currentSpan().context().traceId() : null;
51: 	}
52: }
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\main\\java\\th\\co\\scb\\ace\\demo\\recovery\\access\\api\\ApiError.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\access\api\ApiError.java, lines 1-71
1: package th.co.scb.ace.demo.recovery.access.api;
2: 
3: import java.util.Map;
4: 
5: /**
6:  * Messages the platform raises itself, with the English and Thai text of the Error and Message
7:  * Standard v4 section 4. The message table (reference data) is the source of record; story code
8:  * reads its messages from there. These few are held here only because the platform must answer
9:  * before any reference data is reachable (sign-in, permission, Temporal down).
10:  *
11:  * <p>Errors go out as {@code application/problem+json} with the API Specification v4
12:  * {@code Problem} fields: type, title, status, detail, messageCode, messageTh, field, traceId.
13:  */
14: public enum ApiError {
15: 
16: 	/** E401: no valid session, or the person holds no Workbench role. */
17: 	NO_ROLE("MSG-P4-001", 401,
18: 			"You have no Recovery Workbench role. Ask your team manager to request one.",
19: 			"à¸„à¸¸à¸“à¸¢à¸±à¸‡à¹„à¸¡à¹ˆà¸¡à¸µà¸ªà¸´à¸—à¸˜à¸´à¹Œà¹ƒà¸Šà¹‰à¸‡à¸²à¸™ Recovery Workbench à¸à¸£à¸¸à¸“à¸²à¸•à¸´à¸”à¸•à¹ˆà¸­à¸œà¸¹à¹‰à¸ˆà¸±à¸”à¸à¸²à¸£à¸—à¸µà¸¡à¹€à¸žà¸·à¹ˆà¸­à¸‚à¸­à¸ªà¸´à¸—à¸˜à¸´à¹Œ"),
20: 
21: 	/** E403: the role lacks the right in the capability area. Placeholder {action}. */
22: 	NOT_PERMITTED("MSG-P4-002", 403,
23: 			"You cannot {action} here. Your role does not include it.",
24: 			"à¸„à¸¸à¸“à¹„à¸¡à¹ˆà¸ªà¸²à¸¡à¸²à¸£à¸–{action}à¹„à¸”à¹‰ à¹€à¸™à¸·à¹ˆà¸­à¸‡à¸ˆà¸²à¸à¸šà¸—à¸šà¸²à¸—à¸‚à¸­à¸‡à¸„à¸¸à¸“à¹„à¸¡à¹ˆà¸¡à¸µà¸ªà¸´à¸—à¸˜à¸´à¹Œà¸™à¸µà¹‰"),
25: 
26: 	/** E404: the record does not exist or is outside the caller's scope. */
27: 	NOT_IN_SCOPE("MSG-P4-003", 404,
28: 			"This case is not in your scope.",
29: 			"à¸à¸£à¸“à¸µà¸™à¸µà¹‰à¹„à¸¡à¹ˆà¸­à¸¢à¸¹à¹ˆà¹ƒà¸™à¸‚à¸­à¸šà¹€à¸‚à¸•à¸‡à¸²à¸™à¸‚à¸­à¸‡à¸„à¸¸à¸“"),
30: 
31: 	/** E503: the Temporal frontend is unreachable (RWB-E1-071). */
32: 	WORKFLOW_UNAVAILABLE("MSG-P3-036", 503,
33: 			"The workflow service is not available. Try again in a few minutes.",
34: 			"à¸£à¸°à¸šà¸šà¹€à¸§à¸´à¸£à¹Œà¸à¹‚à¸Ÿà¸¥à¸§à¹Œà¹„à¸¡à¹ˆà¸žà¸£à¹‰à¸­à¸¡à¹ƒà¸Šà¹‰à¸‡à¸²à¸™ à¸à¸£à¸¸à¸“à¸²à¸¥à¸­à¸‡à¹ƒà¸«à¸¡à¹ˆà¹ƒà¸™à¸­à¸µà¸à¹„à¸¡à¹ˆà¸à¸µà¹ˆà¸™à¸²à¸—à¸µ");
35: 
36: 	private final String messageCode;
37: 	private final int status;
38: 	private final String english;
39: 	private final String thai;
40: 
41: 	ApiError(String messageCode, int status, Stri
... truncated (3,296 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\main\\java\\th\\co\\scb\\ace\\demo\\recovery\\access\\internal\\RecoverySecurityProperties.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\access\internal\RecoverySecurityProperties.java, lines 1-14
1: package th.co.scb.ace.demo.recovery.access.internal;
2: 
3: import java.util.List;
4: 
5: import org.springframework.boot.context.properties.ConfigurationProperties;
6: 
7: /**
8:  * RWB-TE-001 SPEC-023: {@code rwb.security.*}, read by the resource-server configuration only. Keys
9:  * and defaults are those of the former shared record.
10:  */
11: @ConfigurationProperties(prefix = "rwb.security")
12: record RecoverySecurityProperties(String issuer, String jwkSetUri, String audience, String rolesClaim,
13: 		List<String> corsOrigins) {
14: }
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Now compare SecurityConfig to the baseline version to check for regressions. Let's get the diff for these files. Use git diff with a specific path and output in terminal (limited). Let me run git diff on the security-related files.

</details>

**Tool `shell`** - completed

```json
{"command": "git -C \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\" diff develop-recovery...feature/RWB-TE-001-module-boundary -- \"backend/src/main/java/th/co/scb/ace/demo/recovery/access\" backend/build.gradle.kts"}
```

```text
diff --git a/backend/build.gradle.kts b/backend/build.gradle.kts
index 9c61bb3..7c4fd28 100644
--- a/backend/build.gradle.kts
+++ b/backend/build.gradle.kts
@@ -127,17 +127,25 @@ val e2eTest by tasks.registering(Test::class) {
 	systemProperty("rwb.e2e.oidcUrl", System.getenv("RWB_E2E_OIDC_URL") ?: "http://localhost:8090/entra")
 }
 
-// Coverage on recovery packages only, 80% line and branch (BS-7.2)
+// Coverage on recovery packages plus the test-scope boundary tooling, 80% on four counters
+// (BS-7.2; RWB-TE-001 SPEC-020). Fixtures and *Test classes are not measured.
 val recoveryClasses = files(sourceSets.main.get().output.classesDirs.map {
 	fileTree(it) { include("th/co/scb/ace/demo/recovery/**") }
 })
 
+val boundaryToolingClasses = files(sourceSets.test.get().output.classesDirs.map {
+	fileTree(it) {
+		include("th/co/scb/ace/demo/recovery/architecture/boundary/**")
+		exclude("**/*Test.class", "**/*Test$*.class")
+	}
+})
+
 val recoveryCoverageReport by tasks.registering(JacocoReport::class) {
-	description = "JaCoCo report for th.co.scb.ace.demo.recovery."
+	description = "JaCoCo report for th.co.scb.ace.demo.recovery and the boundary tooling."
 	group = "verification"
 	executionData(tasks.named("test").get())
-	classDirectories.setFrom(recoveryClasses)
-	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs)
+	classDirectories.setFrom(recoveryClasses, boundaryToolingClasses)
+	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs, sourceSets.test.get().java.srcDirs)
 	reports {
 		xml.required = true
 		xml.outputLocation = layout.buildDirectory.file("reports/jacoco/recoveryCoverageReport.xml")
@@ -146,15 +154,17 @@ val recoveryCoverageReport by tasks.registering(JacocoReport::class) {
 }
 
 val recoveryCoverageVerification by tasks.registering(JacocoCoverageVerification::class) {
-	description = "Fails below 80% line or branch coverage on recovery packages."
+	description = "Fails below 80% line, instruction, branch or method coverage on recovery packages and the boundary tooling."
 	group = "verification"
 	executionData(tasks.named("test").get())
-	classDirectories.setFrom(recoveryClasses)
-	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs)
+	classDirectories.setFrom(recoveryClasses, boundaryToolingClasses)
+	sourceDirectories.setFrom(sourceSets.main.get().allSource.srcDirs, sourceSets.test.get().java.srcDirs)
 	violationRules {
 		rule {
 			limit { counter = "LINE"; minimum = "0.80".toBigDecimal() 
... truncated (20,992 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

The git diff shows these as new files, not renames, because rename detection in the range diff is showing added files. Need to compare with the baseline `platform/internal/SecurityConfig.java` in develop-recovery to check behaviour change. Let me check the baseline file.

Also `RecoverySecurityProperties` has no defaults vs. baseline `RecoveryProperties` (prefix `rwb`, fields with defaults and validation). Need to check baseline to see whether validation annotations/defaults are lost — could cause unauthenticated bypass? If jwkSetUri is null, bean fails to construct; not a security bypass. But losing @Validated could mean e.g. rolesClaim null → `getClaimAsStringList(null)` may throw. Still not a bypass.

More important: check whether security bean is still picked up under new package. `SecurityConfig` is package-private in `access.internal`, and `@SpringBootApplication` component scan at `th.co.scb.ace.demo` includes it. Fine.

Let me compare the baseline `platform/internal/SecurityConfig.java` and `RecoveryProperties.java`, plus baseline controllers and their method security annotations.

</details>

**Tool `shell`** - completed

```json
{"command": "cd \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\"; git show develop-recovery:backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/SecurityConfig.java; Write-Output \"=== PROPS ===\"; git show develop-recovery:backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/RecoveryProperties.java"}
```

```text
package th.co.scb.ace.demo.recovery.platform.internal;

import java.util.Collection;
import java.util.List;
import java.util.Map;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.convert.converter.Converter;
import org.springframework.http.HttpMethod;
import org.springframework.security.authorization.AuthorizationDecision;
import org.springframework.security.authorization.AuthorizationManager;
import org.springframework.security.config.annotation.method.configuration.EnableMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.oauth2.core.DelegatingOAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2Error;
import org.springframework.security.oauth2.core.OAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2TokenValidatorResult;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.security.oauth2.jwt.JwtDecoder;
import org.springframework.security.oauth2.jwt.JwtValidators;
import org.springframework.security.oauth2.jwt.NimbusJwtDecoder;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationConverter;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.access.intercept.RequestAuthorizationContext;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import th.co.scb.ace.demo.recovery.platform.api.ApiError;

/**
 * Entra ID bearer tokens (BS-4.1). Locally the issuer is the mock OIDC server; in SIT/UAT/PROD it is
 * the bank tenant. App roles in the {@code roles} claim become authorities with no prefix, so a
 * method check reads {@code hasAuthority('RW-PLATADM')}.
 *
 * <p>API Specification v4: E401 (MSG-P4-001) when there is no valid token <em>or</em> the person
 * holds no Workbench role; E403 (MSG-P4-002) when a role lacks the right. Every endpoint also
 * carries a method check naming its capability area (BS-3.2).
 */
@Configuration(proxyBea
... truncated (7,221 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

SecurityConfig unchanged in behaviour. One difference: baseline had `@EnableConfigurationProperties` maybe elsewhere. Now `@EnableConfigurationProperties(RecoverySecurityProperties.class)` added on SecurityConfig. Where was `RecoveryProperties` enabled before? Probably on AceRecoveryApplication or PlatformConfig. Need to check that the Flyway properties and p3 are still bound. Let me check application main class and PlatformConfig/RecoveryFlagProperties etc.

Also check whether `@EnableConfigurationProperties` was moved and whether `rwb.flyway` and `rwb.p3` still bind. Test could catch. Not a security issue.

Now, the important security concern: package-private `SecurityConfig` in `access.internal`. Since it's `@Configuration` and component scanned, fine. But what about `@RestControllerAdvice(basePackages = "th.co.scb.ace.demo.recovery")` - that's fine.

Potential security issue: moving `SecurityConfig` into a module whose published API includes `access.api` with `ApiError`. Not a security issue.

Check the controllers: `TemporalAdminController` moved to `casewf.admin` and `PlatformInfoController` to `integration.internal`. Check their method security annotations preserved. Let's diff those.

</details>

**Tool `shell`** - completed

```json
{"command": "cd \"C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\"; git diff -M develop-recovery...feature/RWB-TE-001-module-boundary -- \"backend/src/main/java/th/co/scb/ace/demo/recovery/workflow/internal/TemporalAdminController.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/admin/TemporalAdminController.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/PlatformInfoController.java\" \"backend/src/main/java/th/co/scb/ace/demo/recovery/integration/internal/PlatformInfoController.java\""}
```

```text
diff --git a/backend/src/main/java/th/co/scb/ace/demo/recovery/workflow/internal/TemporalAdminController.java b/backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/admin/TemporalAdminController.java
similarity index 91%
rename from backend/src/main/java/th/co/scb/ace/demo/recovery/workflow/internal/TemporalAdminController.java
rename to backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/admin/TemporalAdminController.java
index e4fae64..8b09d64 100644
--- a/backend/src/main/java/th/co/scb/ace/demo/recovery/workflow/internal/TemporalAdminController.java
+++ b/backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/admin/TemporalAdminController.java
@@ -1,4 +1,4 @@
-package th.co.scb.ace.demo.recovery.workflow.internal;
+package th.co.scb.ace.demo.recovery.casewf.admin;
 
 import java.time.Clock;
 import java.time.Duration;
@@ -30,9 +30,11 @@ import org.springframework.web.bind.annotation.RequestMapping;
 import org.springframework.web.bind.annotation.ResponseStatus;
 import org.springframework.web.bind.annotation.RestController;
 
-import th.co.scb.ace.demo.recovery.platform.api.ApiError;
-import th.co.scb.ace.demo.recovery.platform.api.ApiProblemException;
-import th.co.scb.ace.demo.recovery.workflow.api.WorkflowIds;
+import th.co.scb.ace.demo.recovery.access.api.ApiError;
+import th.co.scb.ace.demo.recovery.access.api.ApiProblemException;
+import th.co.scb.ace.demo.recovery.casewf.workflow.internal.PlatformSmokeWorkflow;
+import th.co.scb.ace.demo.recovery.casewf.workflow.internal.TemporalProperties;
+import th.co.scb.ace.demo.recovery.casewf.workflow.WorkflowIds;
 
 /**
  * Temporal operations, capability area Platform administration (module P3). Operational only: the
@@ -61,7 +63,7 @@ class TemporalAdminController {
 		this.clock = Clock.system(BANK_ZONE);
 	}
 
-	/** Backend-context §3 and §7: namespace state, retention and pollers per task queue. */
+	/** Backend-context Â§3 and Â§7: namespace state, retention and pollers per task queue. */
 	@GetMapping("/temporal/health")
 	@PreAuthorize("hasAnyAuthority('RW-PLATADM', 'RW-AUDIT')") // Platform administration, right R
 	TemporalHealth health() {
diff --git a/backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/PlatformInfoController.java b/backend/src/main/java/th/co/scb/ace/demo/recovery/integration/internal/PlatformInfoController.java
similarity index 77%
rename from backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/PlatformInfoController.java
rename to b
... truncated (4,791 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

Method security preserved. But note `TemporalAdminController` now imports `casewf.workflow.internal.PlatformSmokeWorkflow` and `TemporalProperties` from another package within same module — fine, but those are in `internal` sub-package not published. Since `casewf.admin` is within the same Modulith module `casewf`, internal access is allowed by Modulith (internal is module-wide internal, not package-private). The spec says `casewf.workflow.internal` is not published; other modules can't use it. Same module can. Fine.

Now check all controllers' `@PreAuthorize` still present. Search for controllers and PreAuthorize in main.

</details>

**Tool `grep`** - completed

```json
{"pattern": "@(RestController|Controller|RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping|PreAuthorize|PermitAll)", "path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\main\\java"}
```

```text
Found 11 matches
C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\access\internal\ApiExceptionHandler.java:
  Line 22: @RestControllerAdvice(basePackages = "th.co.scb.ace.demo.recovery")


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\integration\internal\PlatformInfoController.java:
  Line 18: @RestController

  Line 19: @RequestMapping("/api/recovery/v1/platform")

  Line 32: 	@GetMapping("/info")

  Line 33: 	@PreAuthorize("isAuthenticated()") // PLATFORM.READ_INFO: any signed-in Workbench user


C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\main\java\th\co\scb\ace\demo\recovery\casewf\admin\TemporalAdminController.java:
  Line 44: @RestController

  Line 45: @RequestMapping("/api/recovery/v1/admin")

  Line 67: 	@GetMapping("/temporal/health")

  Line 68: 	@PreAuthorize("hasAnyAuthority('RW-PLATADM', 'RW-AUDIT')") // Platform administration, right R

  Line 91: 	@PostMapping("/workflows/smoke")

  Line 93: 	@PreAuthorize("hasAuthority('RW-PLATADM')") // Platform administration, right C

```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\RecoveryBoundaryTest.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\RecoveryBoundaryTest.java, lines 1-204
1: package th.co.scb.ace.demo.recovery.architecture;
2: 
3: import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;
4: import static org.assertj.core.api.Assertions.assertThat;
5: 
6: import java.io.IOException;
7: import java.nio.file.Files;
8: import java.nio.file.Path;
9: import java.util.ArrayList;
10: import java.util.List;
11: import java.util.Map;
12: import java.util.Set;
13: import java.util.TreeMap;
14: import java.util.regex.Pattern;
15: import java.util.stream.Stream;
16: 
17: import com.tngtech.archunit.core.domain.JavaClass;
18: import com.tngtech.archunit.core.domain.JavaClasses;
19: import com.tngtech.archunit.core.domain.JavaModifier;
20: import com.tngtech.archunit.core.importer.ClassFileImporter;
21: import com.tngtech.archunit.core.importer.ImportOption;
22: import com.tngtech.archunit.lang.ArchRule;
23: import org.junit.jupiter.api.Test;
24: import org.springframework.modulith.core.ApplicationModule;
25: import org.springframework.modulith.core.ApplicationModules;
26: import org.springframework.modulith.core.NamedInterface;
27: 
28: import th.co.scb.ace.demo.AceRecoveryApplication;
29: import th.co.scb.ace.demo.recovery.architecture.boundary.BoundaryRules;
30: import th.co.scb.ace.demo.recovery.architecture.boundary.ModuleMap;
31: import th.co.scb.ace.demo.recovery.architecture.boundary.ModuleMapLoader;
32: 
33: /**
34:  * Recovery boundary rules that Spring Modulith does not cover (RWB-TE-001 SPEC-004..-010, -025,
35:  * -026). The rules read the module map; the published surface and package skeleton are asserted
36:  * against the real main classes.
37:  */
38: class RecoveryBoundaryTest {
39: 
40: 	private static final ModuleMap MAP = ModuleMapLoader
41: 		.load(Path.of("src/test/resources/architecture/recovery-modules.yaml"));
42: 
43: 	private static final Path SOURCES = Path
44: 		.of("src/main/java", MAP.rootPackage().replace('.', '/'));
45: 
46: 	private static final Set<String> PUBLISHED_PACKAGES = Set.of("casewf.rules", "casewf.timers",
47: 			"casewf.workflow", "integration.flags.api", "access.api", "dochub.api");
48: 
49: 	private final JavaClasses classes = new ClassFileImporter()
50: 		.withImportOption(ImportOption.Predefined.DO_NOT_INCLUDE_TESTS)
51: 		.importPackages(MAP.rootPackage());
52: 
53: 	/** MAP:
... truncated (9,848 chars total)
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

RecoveryBoundaryTest loads path `src/test/resources/...` relative to working dir. Fine.

Note that `PUBLISHED_PACKAGES` is a hard-coded literal set in the test, not from the map. That's a design issue (BR6) but not security.

Now read BoundaryRules.java and ModuleMap.java.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\BoundaryRules.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\BoundaryRules.java, lines 1-314
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import java.util.ArrayList;
4: import java.util.LinkedHashSet;
5: import java.util.List;
6: import java.util.Optional;
7: import java.util.Set;
8: 
9: import com.tngtech.archunit.core.domain.Dependency;
10: import com.tngtech.archunit.core.domain.JavaClass;
11: import com.tngtech.archunit.core.domain.JavaModifier;
12: import com.tngtech.archunit.core.domain.JavaPackage;
13: import com.tngtech.archunit.lang.ArchCondition;
14: import com.tngtech.archunit.lang.ArchRule;
15: import com.tngtech.archunit.lang.ConditionEvents;
16: import com.tngtech.archunit.lang.SimpleConditionEvent;
17: import com.tngtech.archunit.lang.syntax.ArchRuleDefinition;
18: import jakarta.persistence.Entity;
19: import org.springframework.data.repository.Repository;
20: import org.springframework.modulith.NamedInterface;
21: 
22: /**
23:  * RWB-TE-001 SPEC-004..-010 (BR1..BR6): the map-driven boundary rules. Every rule reports one line
24:  * per distinct violation with the SPEC-010 text; the map is the only source of module names,
25:  * packages, published packages, client packages and client libraries.
26:  */
27: public final class BoundaryRules {
28: 
29: 	private static final String TEMPLATE = "Rule %s broken: %s depends on %s. Use %s.api or an application event.";
30: 
31: 	private BoundaryRules() {
32: 	}
33: 
34: 	public static List<ArchRule> all(ModuleMap map) {
35: 		return List.of(moduleMap(map), bnd1(map), bnd2(map), bnd4(map), bnd5(map));
36: 	}
37: 
38: 	public static ArchRule moduleMap(ModuleMap map) {
39: 		return rule(new ModuleMapCondition(map));
40: 	}
41: 
42: 	public static ArchRule bnd1(ModuleMap map) {
43: 		return rule(new ExternalCondition(map, "BND-1", external(map, "collection"))).allowEmptyShould(true);
44: 	}
45: 
46: 	public static ArchRule bnd2(ModuleMap map) {
47: 		return rule(new ExternalCondition(map, "BND-2", external(map, "common"))).allowEmptyShould(true);
48: 	}
49: 
50: 	public static ArchRule bnd4(ModuleMap map) {
51: 		return rule(new EntityCondition(map));
52: 	}
53: 
54: 	public static ArchRule bnd5(ModuleMap map) {
55: 		return rule(new ClientLibraryCondition(map));
56: 	}
57: 
58: 	/** A dependency matches when it equals the entry or starts past its dot or dollar boundary. */

... truncated (12,678 chars total)
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\backend\\src\\test\\java\\th\\co\\scb\\ace\\demo\\recovery\\architecture\\boundary\\ModuleMap.java"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\backend\src\test\java\th\co\scb\ace\demo\recovery\architecture\boundary\ModuleMap.java, lines 1-47
1: package th.co.scb.ace.demo.recovery.architecture.boundary;
2: 
3: import java.util.List;
4: import java.util.Optional;
5: 
6: /**
7:  * RWB-TE-001 SPEC-002, SPEC-003 (BR6): immutable model of the module map. The map is the only
8:  * source of module names, packages, published packages, client packages and client libraries.
9:  */
10: public record ModuleMap(String source, String rootPackage, List<Module> modules, List<External> external,
11: 		List<String> clientLibraries, Object sourceViews) {
12: 
13: 	public ModuleMap {
14: 		modules = List.copyOf(modules);
15: 		external = List.copyOf(external);
16: 		clientLibraries = List.copyOf(clientLibraries);
17: 	}
18: 
19: 	/** One nested design module of the recovery module (P1..P10, S1..S9). */
20: 	public record Module(String code, String name, List<String> published, List<String> clientPackages) {
21: 
22: 		public Module {
23: 			published = List.copyOf(published);
24: 			clientPackages = List.copyOf(clientPackages);
25: 		}
26: 	}
27: 
28: 	/** One module outside the recovery root whose published packages may be used. */
29: 	public record External(String name, String rootPackage, List<String> published) {
30: 
31: 		public External {
32: 			published = List.copyOf(published);
33: 		}
34: 	}
35: 
36: 	public String modulePackage(Module module) {
37: 		return rootPackage + "." + module.name();
38: 	}
39: 
40: 	/** The module whose package equals {@code packageName} or is a prefix of it. */
41: 	public Optional<Module> moduleOf(String packageName) {
42: 		return modules.stream()
43: 			.filter(module -> packageName.equals(modulePackage(module))
44: 					|| packageName.startsWith(modulePackage(module) + "."))
45: 			.findFirst();
46: 	}
47: }
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

BoundaryRules: BND-5 uses `dependency.getTargetClass()` and checks name matching. ArchUnit `getDirectDependenciesFromSelf` includes dependencies to classes; may not catch string-based reflection, but that's expected.

Security issue: BND-5 only checks direct dependencies at the bytecode level; a class can bypass via reflection (`Class.forName("java.net.http.HttpClient")`) — but this is a build-time architectural guardrail, not a security control. Not a security finding really. Might note as defense-in-depth, but instructions say don't invent.

More relevant checks:
1. Secrets/PII in diff.
2. Module map loader unsafe path handling.
3. Build script injection.
4. Authorization regressions.
5. ESLint rule bypass.
6. Logs/fixtures PII.

Let me now read the frontend test and eslint config.

</details>

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\frontend\\src\\modules\\recovery\\__tests__\\importBoundary.test.ts"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\frontend\src\modules\recovery\__tests__\importBoundary.test.ts, lines 1-58
1: // @vitest-environment node
2: import { fileURLToPath } from "node:url";
3: import path from "node:path";
4: import { describe, it, expect, beforeAll } from "vitest";
5: import { ESLint } from "eslint";
6: 
7: // RWB-TE-001 SPEC-015, AC6 (T-TE001-07): the D-RCV-39 import allow-list lives in the real
8: // eslint.config.js. Each fixture is an in-memory source file under src/modules/recovery/, so the
9: // recovery block applies; no fixture file is written to disk.
10: const frontendRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../../..");
11: const fixturePath = "src/modules/recovery/caselist/BoundaryFixture.tsx";
12: 
13: const rejected = [
14:   "@/modules/collection/worklist/WorkList",
15:   "../../collection/worklist/WorkList",
16:   "@/hooks/cfsc/x",
17:   "@/api/tdr/config",
18:   "@/pages/x",
19:   "@/utils/cfscCaseList",
20:   "@/modules/other/x",
21:   "../x",
22: ];
23: 
24: const allowed = [
25:   "@/components/ui/button",
26:   "@/lib/utils",
27:   "@/utils/date",
28:   "@/contexts/ApiClientContext",
29:   "@/api/schema",
30:   "@/modules/recovery/casewf/x",
31:   "./sibling",
32: ];
33: 
34: let eslint: ESLint;
35: 
36: async function restrictedMessages(specifier: string): Promise<number> {
37:   const source = `import value from "${specifier}";\nexport const used = value;\n`;
38:   const results = await eslint.lintText(source, { filePath: fixturePath });
39:   const result = results[0];
40:   if (!result) {
41:     throw new Error(`ESLint returned no result for ${specifier}`);
42:   }
43:   return result.messages.filter((message) => message.ruleId === "no-restricted-imports").length;
44: }
45: 
46: describe("D-RCV-39 import boundary", () => {
47:   beforeAll(() => {
48:     eslint = new ESLint({ cwd: frontendRoot });
49:   }, 30_000);
50: 
51:   it.each(rejected)("rejects %s", async (specifier) => {
52:     expect(await restrictedMessages(specifier)).toBe(1);
53:   });
54: 
55:   it.each(allowed)("allows %s", async (specifier) => {
56:     expect(await restrictedMessages(specifier)).toBe(0);
57:   });
58: }, 30_000);
```

**Tool `read`** - completed

```json
{"path": "C:\\Users\\SahilMore\\Downloads\\Recovery Workbench SharePoint Set v14\\rwb-wt\\RWB-TE-001\\frontend\\eslint.config.js"}
```

```text
Read file C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\rwb-wt\RWB-TE-001\frontend\eslint.config.js, lines 1-43
1: import js from "@eslint/js";
2: import reactHooks from "eslint-plugin-react-hooks";
3: import globals from "globals";
4: import tseslint from "typescript-eslint";
5: 
6: // D-RCV-39 import allow-list for frontend/src/modules/recovery/**. Outside the folder only the
7: // shared ACE entry points are allowed; inside it, @/modules/recovery/** and ./ paths. ../ and the
8: // rest of @/ are forbidden. The same rule runs in the ACE front end.
9: const recoveryImportRule = {
10:   "no-restricted-imports": [
11:     "error",
12:     {
13:       patterns: [
14:         {
15:           group: ["../*", "../**"],
16:           message: "D-RCV-39: no ../ imports in the recovery module. Use @/modules/recovery/** or ./",
17:         },
18:         {
19:           regex: "^@/(?!components/ui/|lib/utils$|utils/(?!cfsc)[^/]+$|contexts/ApiClientContext$|api/schema$|modules/recovery/)",
20:           message:
21:             "D-RCV-39: outside the recovery folder only @/components/ui/**, @/lib/utils, @/utils/* (not cfsc*), @/contexts/ApiClientContext and @/api/schema are allowed.",
22:         },
23:       ],
24:     },
25:   ],
26: };
27: 
28: export default tseslint.config(
29:   { ignores: ["dist", "coverage", "playwright-report", "test-results", "src/api/schema.d.ts"] },
30:   {
31:     extends: [js.configs.recommended, ...tseslint.configs.recommended],
32:     files: ["**/*.{ts,tsx}"],
33:     languageOptions: { ecmaVersion: 2022, globals: globals.browser },
34:     plugins: { "react-hooks": reactHooks },
35:     rules: {
36:       ...reactHooks.configs.recommended.rules,
37:     },
38:   },
39:   {
40:     files: ["src/modules/recovery/**/*.{ts,tsx}"],
41:     rules: recoveryImportRule,
42:   },
43: );
```

### Assistant - 2026-11-18 08:57 | opencode-go/deepseek-v4.1-flash | general

<details><summary>Reasoning</summary>

ESLint rule bypass analysis:

The regex `^@/(?!components/ui/|lib/utils$|utils/(?!cfsc)[^/]+$|contexts/ApiClientContext$|api/schema$|modules/recovery/)`.

Potential bypasses:
- `@/components/ui/../../hooks/x`? The regex allows any import starting `@/components/ui/` including `@/components/ui/../hooks/x`. Node/TS resolution normalizes the path to `@/hooks/x`, which is outside the allow-list. Does ESLint's `no-restricted-imports` regex apply to the raw source string? Yes, raw import specifier. So `@/components/ui/../hooks/x` matches allowed prefix. TypeScript/bundler resolves `@/components/ui/../hooks` → `@/hooks` (assuming `@` alias to src). That bypasses.

Similarly `@/modules/recovery/../collection/worklist/WorkList` → resolves to `@/modules/collection/...`, which is outside the recovery folder. This is a real bypass.

Also `@/utils/foo/../cfsc`? The `utils/(?!cfsc)[^/]+$` part requires only one segment, so `@/utils/x/../cfsc/y` wouldn't match `utils/` alternative because `[^/]+$` requires no slash. So no.

`@/api/schema/../../hooks/x`? The regex allows `api/schema$` (end anchor), so extra path segments are not allowed. `lib/utils$` anchored. `contexts/ApiClientContext$` anchored. Only `components/ui/`, `modules/recovery/` and `utils/...` are prefix-unanchored. `components/ui/../...` and `modules/recovery/../...` bypass.

This is a genuine finding for the task: "the frontend ESLint rule cannot be bypassed by the allowed import list or by a path alias". Here the allowed list itself is bypassable via `..` inside an allowed prefix. But note the refresh: the rule is inherited (frontend/eslint.config.js is not changed by this story). The story adds a test proving the rule fires. Should I report a finding on unchanged inherited code? The review scope is the story diff; the frontend test is new and claims to prove the boundary. The rule itself is baseline, but the new test is supposed to be the evidence. The user specifically asks to check "the frontend ESLint rule cannot be bypassed by the allowed import list or by a path alias". So yes, this is in scope — the test does not cover the `@/components/ui/../...` / `@/modules/recovery/../...` bypass. Severity: Medium (build-time guard, no runtime impact; but it's the AC6 control). Actually the consequence: a developer could import `@/modules/collection/worklist/WorkList` via `@/modules/recovery/../collection/worklist/WorkList` and lint passes. Bundler resolves it (Vite alias `@` -> src, and path normalization by esb

_[truncated]_

</details>

> **Synthetic** - 2026-11-18 08:58

The previous response was interrupted. Continue from where you left off without repeating completed content.

### Assistant - 2026-11-18 09:25 | opencode-go/deepseek-v4.1-flash | general
