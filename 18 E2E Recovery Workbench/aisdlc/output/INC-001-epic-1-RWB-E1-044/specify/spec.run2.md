---
title: "Specification: RWB-E1-044 Database migrations versioned with parameterized schema names"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
increment: INC-001 (build order 1 of 72, Build Sequence v6)
spec_version: v14-2 (remediation run 1 after spec gate round 1; v14-1 kept as `spec.run1.md`)
date: 2026-11-17
status: SUCCESS (pending spec gate round 2, `../review/spec-gate-review-2.md`)
---

# RWB-E1-044 Specification

What changed from v14-1, finding by finding, is in `gate-response.md`. The first version is kept in `spec.run1.md`.

## Sources and precedence

Paths are relative to `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` unless they start with `aisdlc/` or a repository path.

| Ref | Document (name, version, section) | Path |
|---|---|---|
| S-STORY | User story RWB-E1-044, story files v7, §1–§19 | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` |
| S-E069 | User story RWB-E1-069, story files v7 (Section A views, grants) | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-069-read-only-ace-source-views-grants-and-boundary-rule-v1.md` |
| S-E056 | User story RWB-E1-056, story files v7 (`GET /admin/jobs` from `job_catalog`) | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-056-run-books-and-monitoring-for-every-epic-1-job-v1.md` |
| S-DL10 | Recovery Workbench Decision Log v10, row D-RCV-28 (DL42): naming, header, fix line, schema `recovery` via `${recoverySchema}`, "RWB-E1-044 ships no production migration file" | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| S-SQREG | Squad decision register, `INC-001-decisions.md` and `decision-register.md`: D-RCV-05, -12, -28 parts (1)–(4), -40, -43, -44, -48; L-RCV-03, L-RCV-07 | `aisdlc/docs/decisions/` |
| S-D35 | Client decision D-RCV-35 ACE DB alignment (U4; Section A views ship with RWB-E1-069) | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` |
| S-ADR3 | Architecture Decision Records v3, ADR-002, ADR-010 | `05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| S-ENV4 | Environment and Deployment Design v4, §5 (two-migration rule; "Schema names are parameters") | `05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md` |
| S-PS6 | Physical Schema v6, header and Section A (`FROM public.account …`) | `06-data/recovery-workbench-physical-schema-v6.sql` |
| S-API4 | API Specification v4, `GET /admin/jobs` (`getAdminJobs`, `x-module: P1`) | `05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| S-EMS4 | Error and Message Standard v4, MSG-P3-016, MSG-P4-002 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| S-FSD | FSD P3 Case and Workflow v4, A2.24 (FEAT-CWC-24) | `03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-p3-case-and-workflow-v4.md` |
| S-BRP | Business Requirements Program v4, §5.1 (REQ-RDF-001, REQ-RDF-014) | `03-requirements-and-specifications/recovery-workbench-business-requirements-program-v4-docx.md` |
| S-NFR | Non-functional specification v3, NFR-027, NFR-052 | `03-requirements-and-specifications/recovery-workbench-non-functional-specification-v3-docx.md` |
| S-BSEQ | Build Sequence Epic 1 and Epic 2 v6 (E1-044 = 1, E1-069 = 10, E1-056 = 18) | `11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| S-RUN | RUN-BRIEF (precedence, D-RUN-07, D-RUN-08); build log (D-RUN-07, D-RUN-08, D-RUN-13; orchestrator triage 2026-11-17T23:40) | `aisdlc/RUN-BRIEF.md`; `<repo>/AI-SDLC-BUILD-LOG.md` |
| S-AUD | Phase 0 standards audit, A-01, A-04, A-07, A-17, A-19 | `aisdlc/evidence/phase0-standards-audit.md` |
| S-BS | Backend standards BS-2.1–2.9, BS-4.5, BS-4.6, BS-7.2 | `aisdlc/.github/contexts/backend-standards.md` |
| S-TS | Testing standards §6 coverage rules | `aisdlc/.github/contexts/testing-standards.md` |
| S-GATES | Specification and implementation execution gates | `aisdlc/.github/rules/specification-execution-gates.md`, `implementation-execution-gates.md` |
| S-AGENTS | `AGENTS.md` §2, §3.6, §3.7, §4.5, §4.6, §4.7, §6, §7 | `<repo>/AGENTS.md` |
| S-V2 | 10 Nov 2026 spec (history; CLAR-001 A, CLAR-002 A, CLAR-004 A reused) | `aisdlc/output/INC-001-epic-1-RWB-E1-044/_v2-baseline/specify/spec.md` |

**Precedence** (RUN-BRIEF): D-RCV-35/36 > ADR v3 > Decision Log v10 > story files v7 > older maps and drafts.

- Where story v7 conflicts with Decision Log v10 D-RCV-28, Decision Log v10 is applied (DG-L01).
- D-RCV-28 parts (2) literal-schema scope, (3) Testcontainers and JaCoCo tasks and (4) Flyway's own message for a refused clean are **not** in Decision Log v10. They are in the squad register (S-SQREG, `INC-001-decisions.md`, row D-RCV-28, status Active). The squad register is not named in the RUN-BRIEF precedence list. This spec applies it where it details the Decision Log v10 row of the same ID and where story v7 is silent or lower. That choice is labelled ASM-E044-11. The one place it overrides story text (refused clean) is recorded as DG-L11.
- ADR v3 ADR-010 and D-RCV-35 rank above Decision Log v10. They require views over ACE `public` tables, shipped as a recovery migration by RWB-E1-069. The D-RCV-28 lint, as this story ships it, rejects that text. The conflict is DG-L09. Its resolution is a seam owned by RWB-E1-069 (SPEC-016).

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `ENHANCEMENT_LOGIC_ONLY` |
| UI In Scope | NO |
| Logic In Scope | YES |
| API In Scope | NO |
| API Impact Type | NO_API_CHANGE |
| Impacted Existing Nodes | `backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/RecoveryFlywayConfig.java`; `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java` (logic moves to the test-scope tooling package, SPEC-016); `backend/src/main/resources/db/modulemigration/recovery/README.md`; `backend/build.gradle.kts` (coverage tasks only, SPEC-014) |
| New Nodes Required | YES. Test scope only: the migration-lint and schema-comparator tooling classes (SPEC-016, SPEC-012), their unit tests, one container test class, and lint and Flyway fixture folders. Also story and plan convention files (SPEC-015) |
| Inherited Existing Behavior | Recovery Flyway bean settings: own history table `flyway_schema_history_recovery`, `outOfOrder(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`, `validateMigrationNaming(true)`, placeholder `recoverySchema`. Also the migrator data-source selection, the baseline migration lint rules, the `recoveryIntegrationTest` and `recoveryCoverage*` tasks, and `RecoveryDatabaseIT` (S-AUD A-04; S-SQREG D-RCV-28, D-RCV-48) |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

**Classification evidence.** A prior trace chain exists: S-V2, and Traceability Matrix v2.0 §3 row 001 (RWB-E1-044 to BR-RWB-013 / FR-RWB-013). The code already holds the Flyway bean and the lint (S-AUD A-04). This story changes rules and checks only. It adds no route, screen or endpoint.

**Production migration file.** None. Decision Log v10 D-RCV-28 and story v7 §13 both say RWB-E1-044 "ships no production migration file". No `<seq>` is fixed in this spec (D-RUN-07). Every `V<seq>__…` file named below is a test fixture under `backend/src/test/resources/`, never in `db/modulemigration/recovery/`. Fixtures need concrete numbers because the lint checks contiguity from `V0001` (ASM-E044-14).

**Dependencies (D-RUN-08).** This spec depends only on code in this repository: the Flyway bean, the lint, `RecoveryDatabaseIT`, `infra/postgres/init/` and the JaCoCo tasks. E1-044 is build order 1 (S-BSEQ), so no earlier story is relied on. Work owned by later stories is named as a seam in SPEC-016 and SPEC-017 and is out of scope.

## Intent

Every change to schema `recovery` is a versioned, checksummed, forward-only Flyway migration. It names the schema only as `${recoverySchema}`, carries its story key, and is checked by a build-time lint and a container test before merge (S-STORY §1, §8 BR1–BR8; S-DL10 D-RCV-28; S-BRP REQ-RDF-001, REQ-RDF-014).

## Trigger and preconditions

| Trigger or precondition | Condition | Source |
|---|---|---|
| Service start with `rwb.flyway.enabled=true` (default) | Schema `recovery` exists and is owned by `rwb_migrator` (`createSchemas(false)`). Migrator credentials come from the environment or the key store | S-ADR3 ADR-010; S-BS BS-4.5; S-NFR NFR-052; `infra/postgres/init/` |
| `./scripts/dev.ps1 test` (Gradle `test`) | None. The lint and the comparator unit tests need no database | S-SQREG D-RCV-05, D-RCV-28 (3) |
| `./scripts/dev.ps1 it` (Gradle `recoveryIntegrationTest`, tag `recovery-it`) | Docker is available. The task fails, not skips, without Docker | S-SQREG D-RCV-28 (3), D-RCV-44 |
| Story §3: recovery tables defined in LDM and Physical Schema v6 | Satisfied by the documents. No table is created by this story | S-STORY §3; S-PS6 |
| Story §3: module folder and boundary test exist (RWB-TE-001) | Satisfied by the repository baseline: `backend/src/main/java/th/co/scb/ace/demo/recovery/` and `RecoveryBoundaryTest` exist. Nothing from RWB-TE-001's story is relied on (D-RUN-08) | S-AUD A-01, A-04 |
| Story §3: migration account and read-only drift account in the key store | Migration account: inherited (`rwb.flyway.user`, SPEC-001). Read-only drift account: out of scope (D-RCV-05; SPEC-017) | S-STORY §3; S-SQREG D-RCV-05 |
| Story §3: `RWB_SCHEMA` set per environment | Replaced by the pin to `recovery` (SPEC-002; DG-L01) | S-DL10 D-RCV-28 |
| Story §3: deployment slots booked (DL35) | Outside the repository. No code or test applies | S-STORY §3 |

## Requirement-to-SPEC Logic Coverage

Coverage Type names the main source of each row. "Restated" and "out of scope by decision" are given in Implementation Notes.

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| AC1 / BR1 / BR5 | A pending migration applies once. Version and checksum are recorded in `flyway_schema_history_recovery`. A rerun applies nothing | SPEC-001, SPEC-011 | INHERITED_EXISTING_BEHAVIOR | Bean behaviour exists. The container proof is new (T-044-10) | COVERED |
| AC2 / BR7 / X1 | Drift between the migration result and a target fails with MSG-P3-016 naming `<schema>.<table>.<column>` | SPEC-012 | DIRECT | Restated: container-to-container comparison before every MR (CLAR-001) | COVERED |
| AC2 / BR7 (real SIT/UAT/PROD, flag `rwb.p3.migration-drift-gate`); story §3 read-only account for the drift check | Drift check against real environments, gating deployment | SPEC-017 | DIRECT | Out of scope by decision: parked by D-RCV-05; CLAR-001 A (S-V2). DG-L02 | COVERED |
| AC3 / BR2 | The schema comes from a parameter. The same file produces the table in schema `recovery` in two databases | SPEC-001, SPEC-002, SPEC-007, SPEC-011 | DIRECT | Restated: value fixed to `recovery` (Decision Log v10 D-RCV-28; story §13). `RWB_SCHEMA=rwb_case` not applied (CLAR-003) | COVERED |
| AC4 / BR5 / X2 | An applied migration edited later fails validation. MSG-P3-016 names the version. The service does not start | SPEC-001, SPEC-003, SPEC-011 | DIRECT | `validateOnMigrate(true)` made explicit. The version is mandatory (SPEC-003) | COVERED |
| AC5 / BR2 / X3 | A literal schema qualifier fails the build with MSG-P3-016 naming file and line | SPEC-004, SPEC-007, SPEC-010 | DIRECT | Rule scope from squad register D-RCV-28 (2) | COVERED |
| AC6 / BR3 / X4 | Two non-fix files with the same key, or a file with no key, fail the build naming both files and the key | SPEC-004, SPEC-006, SPEC-010 | DIRECT | Second-non-fix and line-1 checks are inherited. The finding format is new | COVERED |
| AC7 / BR4 / X5 | Clean is refused, undo files are refused, forward only | SPEC-001, SPEC-005, SPEC-011, SPEC-013 | INHERITED_EXISTING_BEHAVIOR | `cleanDisabled(true)` exists. The refused clean shows Flyway's own message (squad register D-RCV-28 (4); DG-L11). The L-UNDO rule ID is new | COVERED |
| AC8 / X6 | A migration that fails part way rolls back fully. The failure is recorded. The service does not start | SPEC-003, SPEC-011 | DIRECT | Restated: the record is the ERROR log with MSG-P3-016 and the version. No failed history row remains on PostgreSQL (CLAR-006; DG-L03) | COVERED |
| AC8 (job monitor display) | The run shows "failed" on the job monitor | SPEC-017 | DIRECT | Out of scope by decision D-RCV-12. No receiving story is named (DG-L10; OI-E044-G) | COVERED |
| AC9 / X7 | Two instances starting together apply a pending migration exactly once. Both start | SPEC-011 | INHERITED_EXISTING_BEHAVIOR | Flyway's PostgreSQL lock. The proof is new (T-044-16) | COVERED |
| BR6 | Own history table | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | `HISTORY_TABLE` constant | COVERED |
| BR8 | No FK into `public`. The lint names the file | SPEC-008, SPEC-010 | DIRECT | Dedicated rule. Database defence in depth (T-044-17) | COVERED |
| D-RCV-28 (1) (Decision Log v10 and squad register) | Name, contiguous seq, one non-fix per key, fix rule, no `R__` | SPEC-005, SPEC-006 | INHERITED_EXISTING_BEHAVIOR | Duplicate-seq, multi-key-line and fix-without-base findings are new | COVERED |
| D-RCV-28 (2) (squad register) | Literal schema in object-name positions, qualified types, bare `SCHEMA`; `SET search_path` in every form | SPEC-007 | DIRECT | Search-path forms widened (SPEC-007). The ADR-010 conflict is DG-L09, with a seam (SPEC-016) | COVERED |
| Decision Log v10 D-RCV-28; story v7 §13 | Schema `recovery` in every environment; story §13 "no per-environment override" | SPEC-002 | DIRECT | Closes audit A-17 | COVERED |
| D-RUN-13 (build log) | The schema-prefix lint checks SQL identifiers only. It ignores string literals and comments (`--`, `/* */`) | SPEC-007, SPEC-008 | DIRECT | New compared with the baseline lint. Physical Schema v6 holds 297 `'public.…'` dictionary literals that RWB-E1-001 seeds (T-044-21) | COVERED |
| D-RCV-48 (squad register) | First recovery migrate on a non-empty schema baselines at 0 and applies `V0001` | SPEC-001, SPEC-011 | INHERITED_EXISTING_BEHAVIOR | Settings exist. The full proof is new (T-044-18). The register text says schema `ace` (DG-L12) | COVERED |
| NFR-027 | Rollback by redeploying the previous tag | SPEC-013 | DIRECT | `*:future` default and `outOfOrder(false)` | COVERED |
| NFR-052 / BS-4.5 | Migration account credentials stay outside the repository | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | No change | COVERED |
| Story §10: pipeline migration account | Applies migrations with the migration database account from the key store; not a Workbench role | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | `rwb.flyway.user` / `password` from the environment or key store | COVERED |
| Story §10: RW-PLATADM runs deployments | Deployment is a pipeline action outside this repository | SPEC-017 | DIRECT | No Workbench endpoint in this story, so no method-security check applies (AGENTS §3.3 applies to endpoints) | COVERED |
| Story §10: RW-PLATADM reruns a failed migration job; reads runs on SCR-44. RW-DATASTEW and RW-AUDIT read runs | Role-based access to migration runs | SPEC-017 | DIRECT | Out of scope by decision D-RCV-12. No receiving story is named (DG-L10) | COVERED |
| Story §12 `GET /admin/jobs?type=MIGRATION`; `MigrationRunRecorder`; §14 MSG-P4-002; §15 SCR-44; §16 TC-E1-044-10 | Record and read migration runs; refuse a role without Platform administration R | SPEC-017 | DIRECT | Out of scope by decision D-RCV-12. No receiving story is named (DG-L10; OI-E044-G) | COVERED |
| Story §14 MSG-P3-016 | Drift, checksum mismatch, lint failure, refused clean or undo, failed migration | SPEC-003, SPEC-004, SPEC-012, SPEC-013 | DIRECT | ID and parameters only (CLAR-004). Refused clean uses Flyway's message (DG-L11) | COVERED |
| Audit A-19 | The first story sets the story and plan file convention | SPEC-015 | DIRECT | ASM-E044-08 | COVERED |
| ADR v3 ADR-010; D-RCV-35 U4; Env v4 §5 (Section A views over `public` ship as a recovery migration with RWB-E1-069) | A recovery migration must be able to create `v_ace_*` views over ACE `public` tables | SPEC-016 | DIRECT | Seam owned by RWB-E1-069 (D-RUN-08; orchestrator triage). Not built here. DG-L09; OI-E044-F | COVERED |

## Backend Specification

### SPEC-RWB-E1-044-001 Recovery Flyway bean (extend, do not duplicate)

- Keep `RecoveryFlywayConfig` in `th.co.scb.ace.demo.recovery.platform.internal` with every inherited setting listed under Change Scope Declaration (S-AUD A-04; S-SQREG D-RCV-28, D-RCV-48; S-BS BS-2.3).
- Add `validateOnMigrate(true)` explicitly. Story §12 sets it. Flyway's default is the same, so behaviour is unchanged and the intent becomes visible.
- Leave `ignoreMigrationPatterns` at Flyway's default (`*:future`). A previous tag then starts against a database that holds a later version (NFR-027, SPEC-013).
- Data-source selection stays as is: the migrator account when `rwb.flyway.user` is set, otherwise the main data source. Credentials come from the environment or the key store only (BS-4.5, NFR-052).
- The story §13 package `recovery.casewf.migration` is not created. Module mapping belongs to RWB-TE-001 (S-AUD A-01). Recorded as gap DG-L06.

### SPEC-RWB-E1-044-002 Schema pinned to `recovery`

- On bean creation, if `rwb.schema` is not exactly `recovery`, start fails with a configuration error. The error names the property, the value found and D-RCV-28. Flyway is not built and nothing is migrated.
- Reason: `application.yaml` binds `rwb.schema: recovery`, but relaxed binding lets the environment variable `RWB_SCHEMA` override it (S-AUD A-17). Decision Log v10 D-RCV-28 says the schema "is recovery in every environment". Story v7 §13 says "no per-environment override".
- The error is a start-up configuration error, not a user message. No message ID applies (ASM-E044-03).

### SPEC-RWB-E1-044-003 Migration failure reported as MSG-P3-016

- The migrate call made when the bean is initialised is wrapped so that it can report. Today it is `@Bean(initMethod = "migrate")`.
- When it throws a `FlywayException`, the bean logs **one** ERROR line with message ID `MSG-P3-016` and parameters `schema=recovery` and `object=<…>`. It then rethrows, so the application context fails and the service does not start (S-STORY X2, X6; S-EMS4 MSG-P3-016).
- `object` is set as follows:

| Failure | `object` | Mandatory | Where the version comes from |
|---|---|---|---|
| Validation failure on an applied migration: checksum mismatch, applied file missing, lower version pending under `outOfOrder(false)` | The version or versions concerned, comma-separated | Yes | Flyway's validate result: the invalid-migration entries and their versions (`validateWithResult()`) |
| Migration that fails part way | The version of the failed migration | Yes | The failed migration is rolled back on PostgreSQL and stays pending, so it is the first pending version in `info()` after the failure |
| Failure with no version: connection refused, lock timeout, missing schema | `recoveryFlyway` | — | Fallback only for these |

- The Flyway calls named in the table are the expected public API of the resolved Flyway 12.4.0 (ASM-E044-12). The plan may use another public Flyway API that yields the same version. T-044-09, T-044-12 and T-044-14 are the acceptance.
- Code holds the message ID and parameters only, with no message text (S-AGENTS §3.6; CLAR-004 A in S-V2).
- **What is logged.**
  - The bean's own ERROR line holds only the message ID and the two parameters. It holds no SQL and no credentials (S-BS BS-4.6).
  - The rethrown exception is logged by Spring when the context fails. It carries Flyway's own message. For a failed migration, that message includes the failing SQL statement.
  - This is accepted, not redacted. Recovery migrations hold DDL and reference data only, never personal data (S-AGENTS §4.7; S-STORY §17). The password is a separate property and is not part of the JDBC URL (ASM-E044-12).
  - Audit A-07 (log masking) is owned by RWB-TE-011 and is not built here.
- A refused `clean()` is not wrapped. It shows Flyway's own message (squad register D-RCV-28 (4); DG-L11).

### SPEC-RWB-E1-044-004 Lint finding format

- Every lint finding is one line: `MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>`.
- The line number is 1-based. It is 0 for file-level rules such as naming, sequence and duplicates.
- The test fails listing all findings, not only the first (S-STORY X3, AC5, AC6; ASM-E044-04).
- Rule IDs: `L-NAME`, `L-UNDO`, `L-REPEATABLE`, `L-SEQ-GAP`, `L-SEQ-DUP`, `L-HEADER`, `L-HEADER-MULTI`, `L-KEY-DUP`, `L-FIX-NO-BASE`, `L-FIX-LINE2`, `L-SEARCH-PATH`, `L-LITERAL-SCHEMA`, `L-FK-OUTSIDE`, `L-GRANT`.

### SPEC-RWB-E1-044-005 File-level naming rules (D-RCV-28 (1))

| Rule | Check | Status |
|---|---|---|
| L-NAME | Name matches `^V(\d{4})__(rwb_[a-z0-9]+_\d{3})_[a-z0-9_]+\.sql$` | Inherited |
| L-REPEATABLE | Any `R__*.sql` fails | Inherited |
| L-UNDO | Any `U*.sql` fails with its own rule ID. Today it falls into L-NAME | New |
| L-SEQ-DUP | Two files with the same `<seq>` fail, naming both | New. Today it is reported as a gap |
| L-SEQ-GAP | Sequences must be contiguous `0001..N` | Inherited |

Any non-`.sql` file other than `README.md` in the folder is reported under L-NAME (ASM-E044-05).

### SPEC-RWB-E1-044-006 Header and story-key rules

| Rule | Check | Status |
|---|---|---|
| L-HEADER | Line 1 equals `-- Story: <KEY>`, where `<KEY>` is derived from the file name (`rwb_e1_044` gives `RWB-E1-044`) | Inherited |
| L-HEADER-MULTI | A second `-- Story:` line anywhere in the file fails | New |
| L-KEY-DUP | At most one non-fix file per key. The finding names both files and the key | Inherited; the finding format is new |
| L-FIX-LINE2 | A file whose line 2 starts with `-- Fix:` must give a non-empty reason | New |
| L-FIX-NO-BASE | A fix file needs exactly one non-fix file of the same key with a lower `<seq>` | New |

### SPEC-RWB-E1-044-007 Literal-schema and search-path rules (squad register D-RCV-28 (2))

**Text preparation.**

- Remove `--` comments to end of line, including a comment that follows code on the same line, and `/* … */` block comments, including ones that span lines.
- For L-LITERAL-SCHEMA and L-FK-OUTSIDE only, also blank out the contents of single-quoted string literals. This covers doubled quotes (`''`) and `E'…'` literals. Blanking keeps the line structure, so line numbers stay correct.
- Dollar-quoted bodies (`$$ … $$`, `$tag$ … $tag$`) are scanned as SQL. A single-quoted literal inside one is still blanked.
- Split the text into statements on `;` outside quotes and dollar bodies. Each statement keeps the line number where it starts, and each match keeps its own line.

**Identifiers only (D-RUN-13).** The schema-prefix rules L-LITERAL-SCHEMA and L-FK-OUTSIDE check SQL identifiers only. They ignore string literals and comments (`--` and `/* */`). Two sources support this:

- Build log D-RUN-13: "A literal is not a schema reference".
- Physical Schema v6 holds 297 lines with a `'public.…'` literal, in the `sys_fields` dictionary rows (from line 5826). RWB-E1-001 seeds those rows, and each value is data, not a schema reference.

This agrees with squad register D-RCV-28 (2), where schema names inside string literals are "an accepted gap left to code review". It differs from the baseline lint in two ways, both marked New:

- The baseline lint skips only whole lines that start with `--`, so a trailing `--` comment or a `/* */` comment that names a schema fails today.
- The baseline lint does not strip strings, so `'public.account'` fails today.

L-SEARCH-PATH is not a schema-prefix rule. It keeps running before strings are blanked (below).

**L-SEARCH-PATH.** D-RCV-28 (2) says "any `SET search_path` fails in every form". The rule runs on the comment-stripped text **before** string literals are blanked. It fails on any occurrence of the identifier `search_path`, quoted or not, in any case. That is a superset of every form, including:

| Form | Status |
|---|---|
| `SET search_path …` | Inherited |
| `SET LOCAL search_path …`, `SET SESSION search_path …` | New |
| `SELECT set_config('search_path', …)` | New (inside a string, so it must run before stripping) |
| `ALTER ROLE … SET search_path …`, `ALTER DATABASE … SET search_path …`, `ALTER FUNCTION … SET search_path …` | New |
| `RESET search_path` | New (fails too, as the rule matches the identifier) |

**L-LITERAL-SCHEMA.** It fails any of the following unless the qualifier is `${recoverySchema}`, `information_schema` or `pg_catalog`:

1. A qualified name in an object-name position. That is the name after `TABLE`, `VIEW`, `MATERIALIZED VIEW`, `SEQUENCE`, `INDEX … ON`, `TRIGGER … ON`, `FUNCTION`, `PROCEDURE`, `TYPE`, `DOMAIN`, `REFERENCES`, `FROM`, `JOIN`, `INTO`, `UPDATE`, `TRUNCATE`, `COMMENT ON <kind>` or `OWNED BY`. Quoted identifiers (`"rwb_case".t`) count.
2. A qualified type: after `::`, after `AS` inside `CAST(`, and as a column data type in a column definition.
3. A bare schema name after `SCHEMA`.
4. Inherited: `recovery.`, `ace.` or `public.` followed by an identifier anywhere in the prepared text, meaning identifiers only, after comments and strings are removed (D-RUN-13). This is folded into the same rule ID, so the qualifier decision is made in one place (SPEC-016).

The position list is the minimum. The plan may extend it but not narrow it (ASM-E044-06).

This replaces the story §13 approach of matching names from `sys_objects`. That table does not exist until RWB-E1-001, and Decision Log v10 D-RCV-28 and the squad register take precedence (DG-L01).

**Consequence (DG-L09).** Under this rule, `CREATE VIEW ${recoverySchema}.v_ace_account AS … FROM public.account a` fails. That is the text that ADR v3 ADR-010, D-RCV-35 and Physical Schema v6 Section A need. This story ships the rule as D-RCV-28 defines it (orchestrator triage, logged in AI-SDLC-BUILD-LOG.md). The narrow exception is a seam owned by RWB-E1-069 (SPEC-016). No placeholder for the ACE schema is invented: Env v4 §5 says "Schema names are parameters", but no source names one.

### SPEC-RWB-E1-044-008 No foreign key outside the recovery schema (BR8)

- L-FK-OUTSIDE fails `REFERENCES <qualifier>.<table>` when the qualifier is not `${recoverySchema}`. The detail is `BR8 foreign key outside recovery schema` (S-STORY BR8; S-ADR3 ADR-010; S-D35 U4).
- An unqualified `REFERENCES` passes. It resolves to `recovery` through Flyway's default schema and the migrator's `search_path`.
- A finding may be reported under both L-LITERAL-SCHEMA and L-FK-OUTSIDE.
- The SPEC-016 seam exception never applies to this rule.

### SPEC-RWB-E1-044-009 GRANT and REVOKE (inherited)

- L-GRANT stays as in the baseline lint: GRANT or REVOKE at the start of a line fails (S-BS BS-2.5, BS-2.6).
- RWB-E1-069 v7 and Env and Deployment Design v4 §5 put grants inside a migration. That conflict is recorded as DG-L05 and left to RWB-E1-069 (SPEC-016, seam SEAM-E044-02).

### SPEC-RWB-E1-044-010 Lint testability and fixtures

- The lint takes a folder and returns the findings. The production test scans `src/main/resources/db/modulemigration/recovery`. The fixture tests scan folders under `backend/src/test/resources/migration-lint/`.
- Each rule in SPEC-004 has at least one failing fixture and one passing fixture. Each test asserts the exact rule ID, file and line.
- The production-folder test stays green on the empty folder (README only).
- Fixtures use synthetic table and column names and no personal data (RUN-BRIEF rule 7).

### SPEC-RWB-E1-044-011 Container proof of Flyway behaviour

**Database.**

- A new test class tagged `@Tag("recovery-it")` runs in `recoveryIntegrationTest`.
- It builds PostgreSQL `postgres:16.16-alpine` from `infra/postgres/init`, as `RecoveryDatabaseIT` does, with `RWB_LOAD_REFERENCE_SCHEMA=false`.
- Init then creates the roles (`rwb_migrator`, `recovery_svc`, `ace_view_owner`). It loads ACE schema v1 into `public`, creates an empty schema `recovery` owned by `rwb_migrator`, and revokes `public` from everyone except `ace_view_owner` (`10-load-ace-database.sh`, `20-grants.sql.inc`).
- Passwords are synthetic test values passed as container environment, as in `RecoveryDatabaseIT`.
- AC2 and AC3 need two databases, so they use two such containers.

**Flyway under test.**

- Every case builds Flyway through `RecoveryFlywayConfig#recoveryFlyway`, so the production settings are the ones tested. A Spring context does this, for example `ApplicationContextRunner` with the configuration class.
- Only `rwb.flyway.location` is set to a fixture folder under `backend/src/test/resources/flyway-fixtures/`.
- `rwb.flyway.url`, `user` and `password` select `rwb_migrator`, as in production.
- Cases that assert MSG-P3-016 or a failed start (T-044-12, T-044-13 lower-version part, T-044-14) assert on the context failure and the captured log.

**Fixtures.** Fixture names follow D-RCV-28 and use key `rwb_e1_044`. The cases are T-044-10 to T-044-18 in the Tests section.

### SPEC-RWB-E1-044-012 Drift comparison (AC2 and BR7, restated)

**Tooling.** Two test-scope parts:

- `SchemaSnapshotReader` reads one database. For schema `recovery` it lists the tables, the columns with data type and nullability, the constraints, the indexes and the views, from `information_schema` and `pg_catalog`. It maps catalog rows into a snapshot value. The mapping takes row data, so unit tests can feed it rows in memory. Only the JDBC query call needs a database.
- `SchemaComparator` is pure logic. It compares two snapshots and formats each difference as `MSG-P3-016 schema=recovery object=recovery.<table>.<column>`, or with the constraint, index or view name.

**Tests.**

- T-044-19 (unit) covers the comparison and the row mapping: added, missing and changed column, constraint, index and view, and equal snapshots.
- T-044-15 (container) applies the same fixtures to two clean databases and adds column `note_x` by hand to table `queue` in one. It asserts exactly one difference, naming `recovery.queue.note_x`.

**Not built.** There is no real-environment comparison, no read-only account and no flag `rwb.p3.migration-drift-gate` (D-RCV-05, D-RCV-44; CLAR-001 A in S-V2; SPEC-017).

### SPEC-RWB-E1-044-013 Forward only and rollback by previous tag (NFR-027)

- `clean()` is refused with Flyway's own message, and no object changes (squad register D-RCV-28 (4); DG-L11).
- A database that holds a later version than the files on the classpath (a previous tag) validates and starts, with nothing applied (`*:future` default).
- With `outOfOrder(false)`, a pending file with a lower version than the highest applied one fails validation. It is reported as in SPEC-003, with the version.

### SPEC-RWB-E1-044-014 Coverage gate (80%, no waiver)

**Scope.** Two surfaces in this story change. Each must reach at least 80% on LINE, INSTRUCTION, BRANCH and METHOD in JaCoCo (S-GATES: lines, statements, branches and functions; S-BS BS-7.2):

1. Changed main classes: `RecoveryFlywayConfig` and any main class the plan adds.
2. Test-scope tooling: the migration lint and the schema comparator classes (SPEC-016, SPEC-012).

This follows the repository precedent: squad register D-RCV-40 and D-RCV-43 (2) bring RWB-TE-001's test-scope boundary tooling into the recovery JaCoCo tasks at 80%, and S-TS §6 says so. The orchestrator triage on S03 also rules that there is no waiver.

**`build.gradle.kts` changes, named for the plan.** This is a shared file, so the plan must name it (D-RCV-40).

- `recoveryCoverageReport` and `recoveryCoverageVerification` add a second class set: `sourceSets.test.get().output.classesDirs`, filtered to the test-scope tooling package (SPEC-016), excluding the JUnit classes (`**/*Test.class`, `**/*Test$*.class`, `**/*IT.class`, `**/*IT$*.class`). The test source directories are added to `sourceDirectories`.
- `recoveryCoverageVerification` adds INSTRUCTION and METHOD limits at 0.80 to the existing LINE and BRANCH limits.
- Execution data stays `test` (unit tests). No class is excluded to make the gate pass, and no threshold is lowered (S-GATES).
- Integration or container coverage does not replace unit coverage (S-GATES). That is why SPEC-012 splits the comparator so that unit tests reach its logic.
- Before the change, the plan records the current INSTRUCTION and METHOD figures for the existing recovery classes. If an existing class falls below 80% on a counter the gate did not check before, that is a plan-gate finding. It is never an exclusion (ASM-E044-07).

### SPEC-RWB-E1-044-015 Documentation and convention (audit A-19)

- **Migration-folder README.** Update `db/modulemigration/recovery/README.md`:
  - List the rule IDs in SPEC-004 and the MSG-P3-016 finding format.
  - Name the RWB-E1-069 seam (SPEC-016).
  - Reword "When RWB-E1-001 ships V0001 to V0003" so that it fixes no numbers (D-RUN-07). The `RWB_LOAD_REFERENCE_SCHEMA=false` instruction stays, tied to the merge of the baseline and the view migrations (DG-L04, DG-L07).
- **Story and plan convention.**
  - `docs/stories/RWB-E1-044/story.md` holds the story key, a link to the story v7 path and this spec, and the restated ACs.
  - `docs/stories/RWB-E1-044/plan.md` is written by the Implementation Planner.
  - Both are in the code repository (S-AGENTS §6, §7; ASM-E044-08).

### SPEC-RWB-E1-044-016 Lint structure, extension point and RWB-E1-069 seam

**Structure.**

- The lint moves out of `RecoveryMigrationLintTest` into a dedicated test-scope tooling package, for example `th.co.scb.ace.demo.recovery.tooling.migration`. The package name is the plan's choice. It holds tooling classes only; JUnit tests may share the package, and SPEC-014 excludes them by name.
- `MigrationLint` scans a folder and returns findings (SPEC-004, SPEC-010).
- A parsed file model holds the name, the lines, the comment-stripped text and the statements with their start lines (SPEC-007).
- Each rule ID in SPEC-004 is one implementation of a single rule interface (`ruleId()`, `check(file, folderContext)`).
- All rules are listed in **one** ordered registry. Adding a rule is one new class plus one registry entry, and no other rule changes.
- `RecoveryMigrationLintTest` stays as the JUnit entry point for the production folder and the fixtures.

**Single extension point for the qualifier decision.** L-LITERAL-SCHEMA decides whether a qualifier is allowed in one named method, for example `isAllowedQualifier(statement, qualifier)`. It gets the whole statement, so a later rule can depend on the statement kind. Today it returns true only for `${recoverySchema}`, `information_schema` and `pg_catalog`. No exception for `public` is built (orchestrator triage on S01).

**Seams (D-RUN-08). Out of scope here; owners are later stories in Build Sequence v6.**

| Seam | Owner | What the owner adds | Basis |
|---|---|---|---|
| SEAM-E044-01 | RWB-E1-069 (build order 10) | A narrow exception in `isAllowedQualifier`: `public` is allowed **only** inside a `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` statement. It never applies to L-FK-OUTSIDE or to any other statement kind. E1-069 also adds its own passing and failing fixtures | ADR v3 ADR-010, D-RCV-35 and Env v4 §5 outrank Decision Log v10 (RUN-BRIEF precedence), so the exception is legitimate when E1-069 adds it. DG-L09; OI-E044-F |
| SEAM-E044-02 | RWB-E1-069 | Resolution of GRANT/REVOKE inside the view migrations, and of two non-fix files per key, against L-GRANT and L-KEY-DUP | DG-L05; OI-E044-B |
| SEAM-E044-03 | None named | Job-monitor parts (SPEC-017) | D-RCV-12; DG-L10; OI-E044-G |
| SEAM-E044-04 | RWB-TE-001 | Adds its own test-scope tooling class directory to the coverage tasks (D-RCV-43 (2)). The SPEC-014 class-set wiring accepts more than one directory | S-SQREG D-RCV-43 |

T-044-02 contains a **seam-marker fixture**: `CREATE VIEW ${recoverySchema}.v_ace_x AS SELECT a.id FROM public.t a`, with synthetic names. It must give L-LITERAL-SCHEMA, which shows that this story ships D-RCV-28 as written. When RWB-E1-069 adds SEAM-E044-01, it replaces this fixture with its own pass and fail fixtures. That is a rule change made by the owning story, not a weakened test.

### SPEC-RWB-E1-044-017 Out of scope, with no owner built here

| Item | Basis | Owner |
|---|---|---|
| `MigrationRunRecorder`; `GET /api/recovery/v1/admin/jobs?type=MIGRATION` with version, checksum and drift result; SCR-44 migration-run display; AC8 "failed" on the job monitor; TC-E1-044-10 (RW-CASEOWN refused with MSG-P4-002); story §10 read and rerun authority for RW-PLATADM, RW-DATASTEW and RW-AUDIT | D-RCV-12 (squad register, Active): deferred "to the story that builds the job monitor". CLAR-002 A (S-V2) says the same. No story is named | **None named.** No receiving story is inferred (orchestrator triage on S02). DG-L10; OI-E044-G |
| Drift check against real SIT, UAT and PROD; read-only account; flag `rwb.p3.migration-drift-gate` | D-RCV-05 (parked); CLAR-001 A (S-V2) | Parking lot (D-RCV-05). DG-L02 |
| Deployment run by RW-PLATADM | Pipeline action outside this repository | Not applicable in this repository |
| ACE-only items: D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step | No counterpart here (`README.md`, local-versus-target table) | ACE port (ASM-E044-09; OI-E044-D) |

Until an owner is named, a migration run is visible in `flyway_schema_history_recovery` and in the MSG-P3-016 ERROR line (SPEC-003).

## Restated acceptance criteria (D-RCV-28 and recorded rulings applied)

| AC | Restatement used for tests | Why restated |
|---|---|---|
| AC1 | Fixture `V0001__rwb_e1_044_add_queue.sql` (line 1 `-- Story: RWB-E1-044`) applies once. Its version, as Flyway records it, and its checksum are in `flyway_schema_history_recovery`. A second migrate applies nothing | V12 and the `RWB_SCHEMA` background conflict with D-RCV-28 (DG-L01) |
| AC2 | See SPEC-012 | D-RCV-05; CLAR-001 |
| AC3 | The same fixture creates `recovery.timer` in two clean databases. The classpath resource is identical and the recorded checksums are equal | Schema fixed to `recovery` |
| AC4 | `V0001` applied, then the file changed: migrate fails validation, the ERROR `MSG-P3-016` line names that version, and the context does not start | Naming |
| AC5 | Fixture line 2 `CREATE INDEX ix_a ON recovery.queue (team_code)` gives `MSG-P3-016 … object=<file>:2 rule=L-LITERAL-SCHEMA` | Line 1 is the header under D-RCV-28 |
| AC6 | Two non-fix files with key `rwb_e1_028` give one L-KEY-DUP finding naming both files and `RWB-E1-028` | Naming |
| AC7 | `clean()` is refused with Flyway's message. A `U0001__…sql` file gives L-UNDO | Squad register D-RCV-28 (4); DG-L11 |
| AC8 | A fixture whose second statement references a missing table: the first statement's object is absent, there is no history row for that version, the ERROR `MSG-P3-016` line names the version, and the context does not start | PostgreSQL transactional DDL (CLAR-006). The job monitor is out of scope (SPEC-017) |
| AC9 | Two contexts migrate concurrently with one pending fixture: one history row for the version, and both start | Naming |

## Field matrix (configuration)

| Field | Source | Rule | Validation |
|---|---|---|---|
| `rwb.schema` | `application.yaml` | Must equal `recovery` | SPEC-002 |
| `rwb.flyway.enabled` | `application.yaml` | Default `true`; inherited | — |
| `rwb.flyway.url` / `user` / `password` | Environment or key store | Never in the repository | BS-4.5, NFR-052 |
| `rwb.flyway.location` | `application.yaml` | `classpath:db/modulemigration/recovery`. Overridden only in container tests (SPEC-011) | Inherited |
| History table | Code constant | `flyway_schema_history_recovery` | BR6 |
| Placeholder | Code | `recoverySchema` = `rwb.schema` | Decision Log v10 D-RCV-28 |

## Status-transition matrix

| From | Event | To | Record |
|---|---|---|---|
| (no history table, non-empty schema) | First migrate | Baseline row at version 0, then `V0001` and later applied | History table (D-RCV-48; T-044-18) |
| (no history table, empty schema) | First migrate | Migrations applied, no baseline row | History table |
| Pending | Migrate succeeds | Applied (history row with checksum) | History table |
| Pending | Migrate fails part way | Pending (rolled back, no row) | ERROR log MSG-P3-016 with the version (SPEC-003) |
| Applied | File checksum changed | Validation failed; service does not start | ERROR log MSG-P3-016 with the version |

No case status changes (S-STORY §9).

## Exceptions

| ID | Condition | Behaviour | Message | Spec / Test |
|---|---|---|---|---|
| X1 | Schema difference | Comparator reports each object | MSG-P3-016 | SPEC-012 / T-044-15, T-044-19 |
| X2 | Applied file edited | Validation fails, start stops | MSG-P3-016 with the version | SPEC-003 / T-044-12 |
| X3 | Literal schema | Lint fails with file and line | MSG-P3-016 | SPEC-007 / T-044-02 |
| X4 | Duplicate or missing key | Lint fails | MSG-P3-016 | SPEC-006 / T-044-03 |
| X5 | Clean or undo | Clean refused (Flyway's message, DG-L11); undo file fails the lint | Flyway's message / MSG-P3-016 | SPEC-005, SPEC-013 / T-044-04, T-044-13 |
| X6 | Fails part way | Rollback, ERROR log, start stops | MSG-P3-016 with the version | SPEC-003 / T-044-14 |
| X7 | Two instances | One applies, the other finds nothing pending | None | SPEC-011 / T-044-16 |
| — | `rwb.schema` is not `recovery` | Start fails with a configuration error | None (ASM-E044-03) | SPEC-002 / T-044-08 |
| — | Search path set in any form | Lint fails | MSG-P3-016 | SPEC-007 / T-044-20 |

## Tests

| Test | Level | Covers | Assertion |
|---|---|---|---|
| T-044-01 | Unit (lint fixtures) | SPEC-005 | L-NAME, L-UNDO, L-REPEATABLE, L-SEQ-DUP and L-SEQ-GAP each fail on their fixture and pass on a compliant one |
| T-044-02 | Unit | SPEC-007, SPEC-016, AC5 | Each listed position, each qualified type and a bare schema fail. `${recoverySchema}`, `information_schema`, `pg_catalog`, commented-out text and a string literal pass. A dollar-quoted body is scanned. The seam-marker view fixture fails with L-LITERAL-SCHEMA |
| T-044-03 | Unit | SPEC-006, AC6 | L-HEADER, L-HEADER-MULTI, L-KEY-DUP (both files named), L-FIX-LINE2, L-FIX-NO-BASE |
| T-044-04 | Unit | SPEC-005, AC7 | `U0001__rwb_e1_044_x.sql` gives L-UNDO |
| T-044-05 | Unit | SPEC-008, BR8 | `REFERENCES public.account(id)` gives L-FK-OUTSIDE. `REFERENCES ${recoverySchema}.t(id)` and an unqualified reference pass |
| T-044-06 | Unit | SPEC-004 | Finding text format, 1-based line, all findings listed |
| T-044-07 | Unit | SPEC-010 | The production folder (README only) passes |
| T-044-08 | Unit | SPEC-002 | `rwb.schema=rwb_case` fails start naming D-RCV-28. `recovery` passes |
| T-044-09 | Unit | SPEC-003, SPEC-001 | With Flyway mocked: a validation failure logs one ERROR `MSG-P3-016` naming the version from the validate result. A failed migration names the first pending version. A failure with no version uses `recoveryFlyway`. Each rethrows. The success path logs no error. Both data-source branches are covered |
| T-044-10 | Container | AC1 | Applies once, checksum recorded, rerun applies nothing |
| T-044-11 | Container | AC3 | Two databases; `recovery.timer` exists in both; equal checksums |
| T-044-12 | Container | AC4 | A changed file fails validation. The ERROR line names the version. The context fails |
| T-044-13 | Container | AC7, SPEC-013 | `clean()` refused, object count unchanged. Previous-tag start passes. A lower pending version fails, naming its version |
| T-044-14 | Container | AC8 | First statement rolled back, no history row, ERROR MSG-P3-016 names the version, context fails |
| T-044-15 | Container | AC2, SPEC-012 | Exactly one difference: `recovery.queue.note_x` |
| T-044-16 | Container | AC9 | Concurrent migrate from two contexts: one history row, both start |
| T-044-17 | Container | BR8 | A fixture with `REFERENCES public.account(…)` applied as `rwb_migrator` fails in the database: `public` access is revoked (`20-grants.sql.inc`), and `public.account` comes from ACE schema v1 loaded by init. This is defence in depth; the fixture folder is outside the lint's production scan |
| T-044-18 | Container | D-RCV-48, SPEC-001 | `recovery` made non-empty with a synthetic table and no history table, then migrate with fixture `V0001`: a baseline row at version 0 and `V0001` applied above it |
| T-044-19 | Unit | SPEC-012 | Comparator: added, missing and changed column, constraint, index and view each give one finding in the MSG-P3-016 format. Equal snapshots give none. Snapshot mapping from in-memory catalog rows |
| T-044-20 | Unit | SPEC-007, SPEC-009 | L-SEARCH-PATH fails each form in the SPEC-007 table, including `set_config('search_path', …)`. L-GRANT fails GRANT and REVOKE at line start, and a compliant file passes |
| T-044-21 | Unit | SPEC-007, SPEC-008, D-RUN-13 | **Positive (passes, no finding):** `INSERT INTO ${recoverySchema}.sys_fields (source_field) VALUES ('public.account.account_key');`, a literal with a doubled quote (`'it''s public.account'`), `E'public.branch'`, a trailing `-- reads public.account` comment and a multi-line `/* public.product */` comment. **Negative (fails):** `SELECT a.id FROM public.account a` (L-LITERAL-SCHEMA), a `"public".account` quoted identifier (L-LITERAL-SCHEMA) and `REFERENCES public.account(id)` (L-FK-OUTSIDE and L-LITERAL-SCHEMA), each reported on the right line when a literal or comment with a schema prefix is on an earlier line. All names are synthetic |

`RecoveryDatabaseIT.recoveryFlywayBaselinedItsOwnHistoryTable` stays as it is. T-044-18 adds the second half of D-RCV-48 ("applies `V0001`").

**Story test cases to spec tests.**

| Story v7 §16 | Spec tests | Note |
|---|---|---|
| TC-E1-044-01 (AC1) | T-044-10 | V12 restated to the `V0001` fixture (DG-L01) |
| TC-E1-044-02 (AC2) | T-044-15, T-044-19 | SIT container restated to a container-to-container check (D-RCV-05) |
| TC-E1-044-03 (AC3) | T-044-11, T-044-08 | `RWB_SCHEMA=rwb_case` restated to `recovery` |
| TC-E1-044-04 (AC4) | T-044-12, T-044-09 | — |
| TC-E1-044-05 (AC5) | T-044-02, T-044-06 | — |
| TC-E1-044-06 (AC6) | T-044-03 | — |
| TC-E1-044-07 (AC7) | T-044-13, T-044-04 | There is no PROD profile here. Clean is disabled in every profile (inherited) |
| TC-E1-044-08 (AC8) | T-044-14, T-044-09 | The job-monitor part is out of scope (SPEC-017) |
| TC-E1-044-09 (AC9) | T-044-16 | — |
| TC-E1-044-10 (Access) | None | Out of scope, no owner named (SPEC-017; DG-L10; OI-E044-G) |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | UI In Scope NO. Story v7 §15 says "No new screen in this story". SCR-44 is out of scope (SPEC-017). No file under `frontend/` changes | — |
| Backend (main): `RecoveryFlywayConfig` and any main class the plan adds | YES | REQUIRED (T-044-08, T-044-09) | 80% LINE, INSTRUCTION, BRANCH, METHOD | SPEC-001, -002, -003, -014 | Logic added: schema pin, failure reporting with version | Positive: start with `recovery`. Negative: wrong schema. Error path: each failure kind in SPEC-003. Branch: both data sources. All four counters at or above 80% |
| Backend (test-scope tooling): migration lint and schema comparator | YES | REQUIRED (T-044-01 to T-044-07, T-044-19 to T-044-21) | 80% LINE, INSTRUCTION, BRANCH, METHOD, measured by `recoveryCoverageVerification` from `test` execution data (SPEC-014) | SPEC-004 to -010, -012, -016 | New logic: 14 rules, text preparation, statement split, comparison. D-RCV-40 and D-RCV-43 (2) precedent; S-TS §6; orchestrator triage on S03 (no waiver) | Every rule ID has a failing and a passing fixture. Boundary: line 1 versus line 2, `0001` start, empty folder. Error path: unreadable or non-`.sql` file. All four counters at or above 80% |

**Verification beyond unit tests** (kept separately, S-GATES):

| Check | Level | When | Evidence |
|---|---|---|---|
| T-044-10 to T-044-18 | Container (`recoveryIntegrationTest`) | Before every MR that touches `db/modulemigration/recovery/**` or `RecoveryFlywayConfig` (D-RCV-44) | Test report attached to implementation evidence |
| `build.gradle.kts` coverage wiring | Build | `./scripts/dev.ps1 test` | `recoveryCoverageVerification` fails below 80% on any of the four counters for either class set |
| README and story/plan files | Review | Code gate | Content matches SPEC-004, SPEC-015 and SPEC-016 |

## API Change Assessment

- No endpoint is added or changed (NO_API_CHANGE).
- `GET /api/recovery/v1/admin/jobs` exists in API Specification v4 (`getAdminJobs`, `x-module: P1`, "List Workbench jobs and outbound files with status"). Its `type` parameter is a free string, and the operation does not describe migration runs.
- The migration-run part of story §12 is out of scope with no named owner (SPEC-017; DG-L10). See `contracts/backend-apis.json`.
- No backward-compatibility impact.

## Frontend Specification

N/A. UI In Scope = NO. Story v7 §15 says "No new screen in this story". The SCR-44 migration-run display is out of scope with no named owner (SPEC-017). `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`.

## Not applicable in this repository (carried to the ACE port)

The ACE-specific D-RCV-45 `db-migrate` guard, the H2 skip and the Jenkins step have no counterpart here. There is no H2, no `db-migrate` profile, no ACE core Flyway and no Jenkins (`README.md`, local-versus-target table). They are recorded as ASM-E044-09 and open-item candidate OI-E044-D.

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC2, BR7, story §13 flag | Real-environment drift gate, read-only account, flag | Scope of the drift check | Settled from sources: CLAR-001 A as recorded in S-V2; D-RCV-05, D-RCV-44. Container-to-container comparison before every MR | RESOLVED | SPEC-012, SPEC-017 |
| CLAR-002 | AC8 (monitor), §10, §12 endpoint, §15, TC-E1-044-10 | Job-monitor parts: who builds them? | Deferred surfaces | Settled from sources: D-RCV-12 puts them out of this story's scope "to the story that builds the job monitor". No story is named and none is inferred (orchestrator triage on S02). DG-L10; OI-E044-G | RESOLVED (out of scope; owner open as OI-E044-G) | SPEC-017 |
| CLAR-003 | AC1–AC9 background, §12 | `RWB_SCHEMA=rwb_case`, `${schema}`, V12–V18 names versus D-RCV-28 | Test data and configuration | Precedence: Decision Log v10 D-RCV-28 over story v7. Restated in the restated-AC table | RESOLVED | SPEC-002, SPEC-011 |
| CLAR-004 | §14 MSG-P3-016 | Message text in code? | Logging and lint output | CLAR-004 A in S-V2; AGENTS §3.6: ID and parameters only | RESOLVED | SPEC-003, SPEC-004 |
| CLAR-005 | `<seq>` for this story | Which number does E1-044 take? | Production file | None. Decision Log v10 D-RCV-28 and story §13 say E1-044 ships no production migration. Numbers are assigned at merge (D-RUN-07) | RESOLVED | Change Scope Declaration |
| CLAR-006 | AC8, X6 | "History records version 17 as failed" versus PostgreSQL transactional DDL | Failure record | Assumption ASM-E044-02: the ERROR log with MSG-P3-016 and the version is the record. DG-L03 | RESOLVED (assumption) | SPEC-003 |
| CLAR-007 | AC7, X5, §14 | Message on a refused clean | Message | Squad register D-RCV-28 (4): Flyway's own message. Story v7 says MSG-P3-016: DG-L11, ASM-E044-11 | RESOLVED (assumption on register precedence) | SPEC-013 |
| CLAR-008 | Story §13 package | `recovery.casewf.migration` versus `platform.internal` | Class location | Audit A-01 is owned by RWB-TE-001. The baseline location is kept (ASM-E044-01). DG-L06 | RESOLVED (assumption) | SPEC-001 |
| CLAR-009 | A-17 | Message for a wrong schema value | Error type | ASM-E044-03: configuration error, no message ID | RESOLVED (assumption) | SPEC-002 |
| CLAR-010 | A-19 | Story and plan file location | Convention | ASM-E044-08 | RESOLVED (assumption) | SPEC-015 |
| CLAR-011 | Coverage | INSTRUCTION and METHOD counters missing from the build; test-scope tooling outside the class set | Gate evidence | SPEC-014: both added; no waiver (orchestrator triage on S03). ASM-E044-07 covers only the baseline-figures step | RESOLVED | SPEC-014 |
| CLAR-012 | ADR-010, D-RCV-35, Env v4 §5 versus D-RCV-28 lint | How does a recovery view migration reference ACE `public`? | Lint rule L-LITERAL-SCHEMA | Ship D-RCV-28 as written. The narrow exception is a seam owned by RWB-E1-069 (orchestrator triage on S01). DG-L09; OI-E044-F | RESOLVED (seam) | SPEC-007, SPEC-016 |

No question was put to the user (L-RCV-03). Assumptions are in `assumptions.md`. Candidate open items are in `shared-updates.md`.

## Status

- `MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); none is needed for a backend-only story.`
- `MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]`
- `CHANGE_CLASSIFICATION_SUMMARY: Existing Flyway bean and lint are extended; test-scope tooling added; no UI or API change.`
- `CHANGE_CLASSIFICATION_RESULT: ENHANCEMENT_LOGIC_ONLY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: baseline Flyway bean and lint exist (audit A-04); rules and checks change]`
- `REQUIREMENT_COVERAGE_SUMMARY: 27 rows: 9 ACs, 8 BRs, D-RCV-28 (1)(2), D-RUN-13, D-RCV-48, NFR-027, NFR-052, story §3/§10/§12/§14/§15/§16 lines, A-17, A-19 and the ADR-010 view need are mapped; job-monitor and real-environment drift parts are mapped to SPEC-017 as out of scope by D-RCV-12 and D-RCV-05.`
- `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 27] [COVERED_RULES: 27] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 7]` The 7 contradictions between sources are DG-L01, -L02, -L04, -L05, -L09, -L11 and -L12 in `document-gaps.md`. Each is settled by RUN-BRIEF precedence, a recorded decision or the orchestrator triage, and none is a blocker. DG-L03 (story versus tool behaviour), DG-L06, -L07 and -L08 (repository and history text) and DG-L10 (a source that is silent) are gaps, not contradictions.
- `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]`
- `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` Open-item candidates for other owners are in `shared-updates.md`; none blocks this story.
