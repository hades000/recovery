---
title: "Spec gate review: RWB-E1-044 (v14 re-baseline, spec v14-1)"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
gate: Specification (Compliance Reviewer, spec-gate mode)
round: 1 (v14 re-baseline; earlier rounds are history in `_v2-baseline/review/`)
date: 2026-11-17
result: FAIL
---

# Spec gate review: RWB-E1-044

## 1. Scope

Reviewed, all under `aisdlc/output/INC-001-epic-1-RWB-E1-044/specify/`: `spec.md`, `compliance-validation.md`,
`assumptions.md`, `document-gaps.md`, `shared-updates.md`, `contracts/backend-apis.json`,
`contracts/frontend-integrations.json`, `figma/figma_report.md`, `agent-run-log.md`.

Checked against:

- The increment card `aisdlc/docs/increments/INC-001-epic-1-RWB-E1-044.md`.
- User story RWB-E1-044, story files v7, §1 to §19 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md`).
- Decision Log v10, row D-RCV-28 and row D-RCV-35 (`01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md`).
- `aisdlc/docs/decisions/` (`decision-register.md`, `INC-001-decisions.md` with D-RCV-28 in full, `d-rcv-35-ace-db-alignment.md`).
- ADR v3, ADR-002 and ADR-010 (`05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md`).
- Environment and Deployment Design v4, §5 (`05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md`).
- Physical Schema v6, header and Section A (`06-data/recovery-workbench-physical-schema-v6.sql`).
- RWB-E1-056 and RWB-E1-069 story files v7; API Specification v4 `/admin/jobs`; Build Sequence v6.
- Error and Message Standard v4 (MSG-P3-016, MSG-P4-002); NFR specification v3 (NFR-027, NFR-052); Business Requirements Program v4 §5.1; FSD P3 v4 A2.24.
- `aisdlc/.github/rules/specification-execution-gates.md`, `implementation-execution-gates.md`, `pdlc.md`; `aisdlc/.github/contexts/backend-standards.md`, `testing-standards.md`.
- `aisdlc/evidence/phase0-standards-audit.md` (A-01, A-04, A-07, A-17, A-19).
- Code: `backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/RecoveryFlywayConfig.java`, `RecoveryProperties.java`, `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java`, `RecoveryDatabaseIT.java`, `backend/build.gradle.kts`, `backend/src/main/resources/application.yaml`, `backend/src/main/resources/db/modulemigration/recovery/README.md`, `infra/postgres/init/`.
- `aisdlc/requirement/Traceability_Matrix.md`, `aisdlc/docs/architecture/migration-merge-order-map.md`, `aisdlc/docs/open-items.md`.

No git command was run. No code, source document or shared file was edited. No question was put to the user (L-RCV-03).

## 2. Statements verified (no finding)

| Spec statement | Source checked | Result |
|---|---|---|
| E1-044 ships no production migration file (§1, CLAR-005) | Decision Log v10 D-RCV-28 ("RWB-E1-044 ships no production migration file"); story v7 §13; merge-order map "Excluded" | Agrees |
| Schema `recovery`, `${recoverySchema}`, not `rwb_case` (SPEC-002, DG-L01) | Decision Log v10 D-RCV-28; story v7 §13; L-RCV-07; D-RCV-35 / ADR-010 | Agrees; precedence applied and recorded |
| `rwb.schema` can be overridden by `RWB_SCHEMA` through relaxed binding (SPEC-002) | `application.yaml` (`rwb.schema: recovery`), `RecoveryProperties` record; audit A-17 owner RWB-E1-044 | Agrees |
| Inherited bean settings (§1, SPEC-001, CON-001) | `RecoveryFlywayConfig.java`: history table constant, `outOfOrder(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`, `validateMigrationNaming(true)`, placeholder `recoverySchema`, migrator data-source branch | Agrees; `validateOnMigrate` is not set today, as the spec says |
| Inherited lint rules and "new" rules (SPEC-005, SPEC-006) | `RecoveryMigrationLintTest.java`: duplicate sequence reported as a gap, `U*.sql` falls into the name rule, `-- Fix: ` detection, `.sql` filter | Agrees, except L-SEARCH-PATH (REVIEW-...-S06) |
| IT task, tag, fail without Docker; coverage tasks read `test` only with LINE and BRANCH limits | `build.gradle.kts` lines 105–158 | Agrees |
| Container image `postgres:16.16-alpine` | `RecoveryDatabaseIT.java` line 37 | Agrees |
| MSG-P3-016 wording and parameters `{schema}`, `{object}`; MSG-P4-002 | Error and Message Standard v4 rows MSG-P3-016, MSG-P4-002 | Agrees |
| NFR-027 rollback by previous tag; NFR-052 secrets in key store | NFR specification v3 | Agrees |
| REQ-RDF-001, REQ-RDF-014 | Business Requirements Program v4 §5.1 | Agrees |
| Real-environment drift parked; job monitor deferred | D-RCV-05, D-RCV-12 (Active); PO rulings CLAR-001 A and CLAR-002 A in the 10 Nov spec; OPEN-027 confirmed 10 Nov | Agrees |
| AC8 failure record on PostgreSQL | Flyway 12.4.0 is the resolved version (Gradle cache); DG-L03 and ASM-E044-02 label the deviation | Labelled assumption; acceptable |
| Build order E1-044 = 1, E1-042 = 3, E1-001 = 9, E1-069 = 10, E1-056 = 18 | Build Sequence v6 | Agrees |
| Trace RWB-E1-044 to BR-RWB-013 / FR-RWB-013; 10 Nov spec used FR-RWB-020 | Traceability Matrix v2.0 §3 row 001; `_v2-baseline/specify/spec.md` | Agrees |
| Audit A-01, A-04, A-17, A-19 | `phase0-standards-audit.md` | Agrees (A-07 is owned by RWB-TE-011 and is cited only as a caution) |
| UI out of scope; no API change; design evidence not required | Story v7 §15 ("No new screen in this story"); D-RCV-12 | Agrees |
| No new dependency | `build.gradle.kts` already has Flyway, Testcontainers PostgreSQL and JaCoCo | Agrees |
| No personal data | Fixture names are synthetic (`queue`, `timer`, `note_x`, `team_code`) | Agrees |

Restated ACs AC1, AC3, AC4, AC5 (line 2 instead of line 1), AC6, AC7 and AC9 are each settled by D-RCV-28 precedence or labelled; DG-L01 records the story conflict. No invented financial, regulatory or security requirement was found: SPEC-002, SPEC-004, SPEC-014 and SPEC-015 each trace to a decision, the audit or a labelled assumption.

## 3. Findings

Finding IDs use `REVIEW-RWB-E1-044-S<nn>` so they do not collide with the 10 Nov rounds (`REVIEW-RWB-E1-044-001` to `-025`).

### REVIEW-RWB-E1-044-S01: Literal-schema rule blocks the ADR-010 view migrations; conflict not recorded

- **Severity:** High
- **Affects:** SPEC-RWB-E1-044-007, SPEC-RWB-E1-044-010, T-044-02, CON-RWB-E1-044-002; `document-gaps.md`; §16 `REQUIREMENT_COVERAGE_RESULT [CONTRADICTIONS: 0]`
- **Evidence:**
  - Spec SPEC-007: L-LITERAL-SCHEMA fails any qualified name after `FROM` or `JOIN` unless the qualifier is `${recoverySchema}`, `information_schema` or `pg_catalog`. The inherited `public.` check "stays". T-044-02 asserts that each listed position fails.
  - ADR v3, ADR-010 "Decision": "30 views in two migrations", shipped by RWB-E1-069 "as the next free sequence after the V0001 baseline". The views read the ACE tables.
  - Environment and Deployment Design v4 §5: Section A views "ships with RWB-E1-069 as the next free sequence after V0001"; "Schema names are parameters, so the same script runs in every environment".
  - Physical Schema v6, Section A, view `recovery.v_ace_account`: `FROM public.account a LEFT JOIN public.product p … LEFT JOIN public.branch b` (proposed migration `V0002__rwb_e1_069_ace_source_views.sql`).
  - RWB-E1-069 story v7 flow 1 and flow 7: V0002 and V0003 hold the views over `public`.
- **Problem:** Every ADR-010 view migration must name the ACE tables in `public`. Under SPEC-007, and under the inherited `public.` check, that migration cannot pass the lint, and no `${recoverySchema}` form can express it. ADR v3 ranks above Decision Log v10 (RUN-BRIEF precedence), so the spec cannot settle this by applying D-RCV-28 (2). It also does not record the conflict as a gap. DG-L05 records the parallel GRANT conflict with E1-069 and Environment and Deployment Design v4 §5, but not this one, and §16 reports zero contradictions. No source names a placeholder for the ACE schema, so the spec cannot invent one.
- **Required fix:** Add a document-gap row that cites ADR v3 ADR-010, Environment and Deployment Design v4 §5, Physical Schema v6 Section A and RWB-E1-069 v7 against D-RCV-28 (2), BS-2.6 and the baseline lint. State the blocker decision and its reason: for E1-044 it is not a blocker if the rule stays as D-RCV-28 (2) and E1-069 owns the change. Add an open-item candidate in `shared-updates.md` (owner: recovery tech lead with BA) that asks how a recovery migration references the ACE source schema (a parameter, as Env v4 §5 says, or a named exception). In SPEC-007, name this as a seam: the plan must keep the rule set extensible for that resolution. Do not invent a placeholder name. Update the §16 status line so it does not claim zero contradictions without this entry.

### REVIEW-RWB-E1-044-S02: Deferred job-monitor work is assigned to RWB-E1-056, which does not carry it

- **Severity:** Medium
- **Affects:** §4 rows "AC8 (job monitor display)" and "Story §10, TC-E1-044-10, `GET /admin/jobs?type=MIGRATION`, SCR-44, MSG-P4-002, `MigrationRunRecorder`"; §12; CLAR-002; `contracts/backend-apis.json` `deferredEndpoints`; `contracts/frontend-integrations.json` `deferred`
- **Evidence:**
  - D-RCV-12 (`INC-001-decisions.md`, decision register) defers these parts "to the story that builds the job monitor" and names no story.
  - RWB-E1-056 story v7: no mention of migration runs, `MIGRATION`, `MigrationRunRecorder`, Flyway, SCR-44 or RWB-E1-044. Its `GET /admin/jobs` lists Workbench jobs from `job_catalog`.
  - API Specification v4, `/admin/jobs` (operationId `getAdminJobs`): no `MIGRATION` type.
  - Story v7 §16 TC-E1-044-10 is the story's only access-control test (RW-CASEOWN refused with MSG-P4-002).
- **Problem:** The spec says these parts are deferred to RWB-E1-056 (build order 18). The receiving story, and the API contract it builds, do not include them. The access-control test case TC-E1-044-10 and the "failed on the job monitor" outcome of AC8 can then drop out of every story. The deferral is valid (D-RCV-12), but the choice of receiving story is the specifier's inference and is not labelled as an assumption.
- **Required fix:** Label "deferred to RWB-E1-056" as an assumption in `assumptions.md` and cite D-RCV-12. Add a document-gap row: D-RCV-12 against RWB-E1-056 v7 and API Specification v4 `/admin/jobs`. Add an open-item candidate (owner: BA or Product Owner) to add `MigrationRunRecorder`, `type=MIGRATION` with version, checksum and drift result, the SCR-44 migration-run display, and TC-E1-044-10 to RWB-E1-056, or to name the story that will build them.

### REVIEW-RWB-E1-044-S03: The 80% coverage gate is waived for the lint and comparator because of tooling

- **Severity:** Medium
- **Affects:** SPEC-RWB-E1-044-014; §11 rows "Backend test tooling: migration lint" and "Backend test tooling: schema comparator"; ASM-E044-07
- **Evidence:**
  - Spec §11 sets the lint's coverage gate to "Rule-level" because the lint is a "Test-scope class; JaCoCo `recoveryCoverage*` measures main classes". The comparator also gets "Rule-level".
  - `specification-execution-gates.md`: a surface that changes has unit tests `REQUIRED` with an 80% threshold for lines, statements, branches and functions. `implementation-execution-gates.md` (lines 56 and 58): missing tasks or tooling "cannot justify an exemption", and the same 80% gate applies "to all layers, including validation".
  - Repository precedent: D-RCV-40 and D-RCV-43 (2) add RWB-TE-001's test-scope boundary tooling to `recoveryCoverageReport` and `recoveryCoverageVerification` at 80%. `testing-standards.md` line 76 says "test-scope boundary tooling included for RWB-TE-001".
- **Problem:** The lint holds most of this story's new logic: 14 rule IDs, comment and string stripping, and keyword-position parsing. Under the spec, the only class held to 80% is `RecoveryFlywayConfig`. The exemption rests on how the JaCoCo tasks are wired today, which is the kind of exemption the gates reject. Rule-level fixtures are needed, but they do not replace measured coverage.
- **Required fix:** In SPEC-014 and §11, require 80% LINE, INSTRUCTION, BRANCH and METHOD for the test-scope lint and comparator classes. Add their class directory to the recovery JaCoCo tasks, as D-RCV-43 (2) did for TE-001. For the comparator, either feed `recoveryIntegrationTest` execution data into the report, or split its pure comparison logic into a class that unit tests cover. Name the `build.gradle.kts` change for the plan.

### REVIEW-RWB-E1-044-S04: The container setup in SPEC-011 cannot run T-044-17, and it skips the bean that T-044-12 and T-044-14 assert on

- **Severity:** Low
- **Affects:** SPEC-RWB-E1-044-011, T-044-12, T-044-14, T-044-17; §6 AC4 and AC8 restatements
- **Evidence:** SPEC-011 says the container test "creates schema `recovery` in setup and builds the recovery Flyway with the production settings, changing only `locations`". T-044-17 runs "as `rwb_migrator`" with `public` revoked (`infra/postgres/init/20-grants.sql.inc`); a plain container has neither the role nor the grants. `RecoveryDatabaseIT` gets them by copying `infra/postgres/init` into the container. AC4 and AC8 as restated, and T-044-14, assert an ERROR `MSG-P3-016` and "the context does not start". That behaviour lives in the bean (SPEC-003), not in a Flyway object built directly.
- **Required fix:** State that T-044-17 runs on a container built from `infra/postgres/init`, as `RecoveryDatabaseIT` does, with a synthetic `public` table. State that cases which assert MSG-P3-016 or a failed start go through `RecoveryFlywayConfig#recoveryFlyway` (or a Spring context), with only `locations` overridden.

### REVIEW-RWB-E1-044-S05: SPEC-003 does not have to name the version, and its no-SQL-in-logs claim is too broad

- **Severity:** Low
- **Affects:** SPEC-RWB-E1-044-003, CON-RWB-E1-044-001 `failureReport`, T-044-09, T-044-12, T-044-14
- **Evidence:** SPEC-003 allows `object="recoveryFlyway" when none is exposed`, but AC4 as restated requires the ERROR line to name `0001`, and AC8 requires it to name the version. SPEC-003 also says "the log line holds no SQL values". The bean rethrows, and Spring then logs the Flyway exception, whose message for a failed migration includes the failing statement.
- **Required fix:** Make the version mandatory for a checksum mismatch and for a failed migration (from the Flyway validate result or migrate exception). Keep the fallback only for failures that have no version. Narrow the claim to the bean's own line, or state how the rethrown exception text is handled. That text holds DDL only and no personal data, which is acceptable if stated.

### REVIEW-RWB-E1-044-S06: L-SEARCH-PATH is described as inherited "in any form", but the baseline check does not cover every form

- **Severity:** Low
- **Affects:** SPEC-RWB-E1-044-004, SPEC-RWB-E1-044-007, T-044-02
- **Evidence:** D-RCV-28 (2) (`INC-001-decisions.md`): "any `SET search_path` fails in every form". The baseline regex in `RecoveryMigrationLintTest` is `(?i)\bset\s+search_path`. It misses `SET LOCAL search_path`, `SET SESSION search_path`, `set_config('search_path', …)` and `ALTER ROLE|DATABASE … SET search_path`. The spec also strips string literals before matching, which would hide the `set_config` form.
- **Required fix:** List the forms the rule must catch and mark the extension as New. Run the search-path check before string stripping, or exempt it from stripping. Add a failing fixture for each form.

### REVIEW-RWB-E1-044-S07: The D-RCV-48 test is not fully covered

- **Severity:** Low
- **Affects:** §1 "Inherited Existing Behavior"; §10, last paragraph
- **Evidence:** D-RCV-48 (Active): "A test proves that the first recovery migrate on a non-empty … baselines at 0 and applies `V0001`". `RecoveryDatabaseIT.recoveryFlywayBaselinedItsOwnHistoryTable` checks only that a version-0 row exists, and the production folder is empty. The spec's container cases T-044-10 to T-044-17 all start from an empty schema.
- **Required fix:** Add a container case. On a non-empty `recovery` schema with no history table, apply a fixture `V0001`, then assert the baseline row at 0 and `V0001` applied. Otherwise, record why D-RCV-48's second clause is out of scope for this story.

### REVIEW-RWB-E1-044-S08: Some story lines are not mapped

- **Severity:** Low
- **Affects:** §4 Requirement-to-SPEC Logic Coverage; §10 Tests
- **Evidence:** Story v7 §10 Authority: RW-PLATADM "runs deployments and reruns a failed migration job"; RW-DATASTEW and RW-AUDIT read runs; the pipeline migration account. Only the read path appears, under the deferred row. Story v7 §16 TC-E1-044-01 to TC-E1-044-09 are not mapped to T-044-01 to T-044-17. Story v7 §3 precondition "a read-only account for the drift check" is not marked deferred. `specification-execution-gates.md` requires every business-rule line to be mapped or marked inherited, with rationale.
- **Required fix:** Add §4 rows for the §10 authority lines (no Workbench endpoint, so no method-security check in this story; run and rerun happen outside the repository; reads are deferred under D-RCV-12) and for the §3 read-only account (deferred, D-RCV-05). Add a TC-E1-044-nn to T-044-nn column or table to §10.

### REVIEW-RWB-E1-044-S09: Some deviations rest on squad-register text that the spec attributes to Decision Log v10

- **Severity:** Low
- **Affects:** §0 precedence statement; SPEC-002; SPEC-003 (clean); SPEC-007; SPEC-013; CLAR-007; `document-gaps.md`
- **Evidence:** The Decision Log v10 row D-RCV-28 holds the naming, header, fix-line and schema rulings only. Parts (2) literal-schema scope, (3) Testcontainers and JaCoCo tasks, and (4) "a refused Flyway clean shows Flyway's own message (accepted deviation from the story's §14)" are in the squad register (`INC-001-decisions.md`), not in Decision Log v10. Spec §0 says "Where the story v7 conflicts with D-RCV-28 (Decision Log v10), D-RCV-28 is applied". Story v7 §5 X5, §7 AC7 and §14 require MSG-P3-016 for a refused clean, and no document-gap row records that deviation. SPEC-002 attributes "no per-environment override" to D-RCV-28, but that phrase is from story v7 §13; Decision Log v10 says "recovery in every environment".
- **Required fix:** Cite the squad register (`INC-001-decisions.md`, D-RCV-28 (2) to (4)) for those parts. Add a document-gap row for the clean-message deviation (story v7 X5, AC7 and §14 against squad D-RCV-28 (4)) that states the basis on which it is applied: register status Active, signed off by the recovery tech lead. Correct the SPEC-002 attribution.

### REVIEW-RWB-E1-044-S10: Some spec fields use values outside the gate vocabulary

- **Severity:** Low
- **Affects:** §1 heading, §4 and §11
- **Evidence:** `specification-execution-gates.md` requires `## Change Scope Declaration` and `## Unit Test Applicability` headings; the spec numbers them (`## 1. …`, `## 11. …`). Coverage Type must be `DIRECT` or `INHERITED_EXISTING_BEHAVIOR`; the spec uses "INHERITED + DIRECT", "DIRECT + INHERITED" and "DEFERRED". Status must be `COVERED` or `BLOCKED`; the spec uses "COVERED (restated)" and "DEFERRED". Unit Tests must be `REQUIRED` or `NOT_APPLICABLE`; the spec uses "YES (…)" and "N/A".
- **Required fix:** Use the exact headings and allowed values. Put "restated" and "deferred by D-RCV-xx" in Implementation Notes, and choose the Coverage Type that names the main source of each row.

### REVIEW-RWB-E1-044-S11: The proposed traceability rows do not match the matrix layout

- **Severity:** Low
- **Affects:** `shared-updates.md` § `Traceability_Matrix.md`
- **Evidence:** Traceability Matrix v2.0 §3 "Story trace" has the columns `INC | Story | Business | Functional | Spec / plan / evidence | Status`. The proposed row uses `Story | Requirement | FR / NFR | SPEC | Spec path | Status`. §2 lists the stories for BR-RWB-013 without RWB-E1-044, and no update is proposed there. The NFR IDs are source IDs (NFR-027, NFR-052), not matrix IDs.
- **Required fix:** Rewrite the §3 row in the matrix's own columns, with the SPEC range in "Spec / plan / evidence". Propose adding RWB-E1-044 to the §2 BR-RWB-013 row. Map NFR-027 and NFR-052 to the matrix NFR IDs, or state that they are cited by source ID.

## 4. Required checks

| Check | Result |
|---|---|
| Authentication and authorization | No endpoint in scope. The read path and its access test TC-E1-044-10 are deferred (D-RCV-12), but the receiving story does not carry them (S02). §10 authority lines are unmapped (S08) |
| Customer and account data protection | Pass. No personal data. Fixtures are synthetic. BR8 (no FK into `public`) is a dedicated rule with database-level proof planned (T-044-17; see S04) |
| Audit logging for sensitive financial actions | Not applicable. No case or decision change. The migration record is the history table and the MSG-P3-016 ERROR line (ASM-E044-02, open-item candidate OI-E044-A) |
| KYC, AML, suitability, consent, approval | Not in scope |
| Frontend integration versioning and error contract | Not applicable. UI and API out of scope; contracts record the deferrals |
| Secrets and environment configuration | Pass. Migrator credentials come from the environment or key store (BS-4.5, NFR-052); `application.yaml` holds no secret. The schema pin closes A-17 |
| Test coverage and evidence | Fail: the 80% gate is waived for test-scope tooling (S03). Container evidence is required before every MR (D-RCV-44) |
| Frontend and backend applicability | Frontend `NOT_APPLICABLE` is justified (story §15; no UI node). Backend applicability is `REQUIRED` |
| Precedence and invented requirements | Story deviations are settled by D-RCV-28, D-RCV-05 and D-RCV-12, or labelled (ASM-E044-01 to -10). The higher-precedence ADR-010 conflict is unrecorded (S01). Squad-register attribution needs correcting (S09). No invented requirement found |

## 5. Result

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | — |
| High | 1 | S01 |
| Medium | 2 | S02, S03 |
| Low | 8 | S04 to S11 |

The High and Medium findings block the hand-off to the Implementation Planner until they are fixed and a second round (`spec-gate-review-2.md`) passes. The Low findings stay visible for disposition in that round.

No REVIEW_GATE_WARNING line is given: the gate fails on blocking findings, so it does not apply (`pdlc.md`).

**Overall: FAIL**
