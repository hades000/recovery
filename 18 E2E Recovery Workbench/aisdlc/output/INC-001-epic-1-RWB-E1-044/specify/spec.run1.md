---
title: "Specification: RWB-E1-044 Database migrations versioned with parameterized schema names"
run_id: INC-001-epic-1-RWB-E1-044
story: RWB-E1-044
increment: INC-001 (build order 1 of 72, Build Sequence v6)
spec_version: v14-1 (re-baseline for D-RCV-35; replaces the 10 Nov 2026 spec kept in `_v2-baseline/`)
date: 2026-11-17
status: SUCCESS
---

# RWB-E1-044 Specification

## 0. Sources and precedence

Paths are relative to `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` unless they start with `aisdlc/` or a repository path.

| Ref | Document (name, version, section) | Path |
|---|---|---|
| S-STORY | User story RWB-E1-044, story files v7, §1–§19 | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-044-database-migrations-versioned-with-parameterized-schema-names-v1.md` |
| S-DL10 | Recovery Workbench Decision Log v10, row D-RCV-28 (DL42) | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| S-ADR3 | Architecture Decision Records v3, ADR-002, ADR-010 | `05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| S-ENV4 | Environment and Deployment Design v4, §5 | `05-technical-architecture/recovery-workbench-environment-and-deployment-design-v4-docx.md` |
| S-EMS4 | Error and Message Standard v4, MSG-P3-016, MSG-P4-002 | `07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| S-FSD | FSD P3 Case and Workflow v4, A2.24 (FEAT-CWC-24) | `03-requirements-and-specifications/recovery-workbench-functional-specifications-by-module-v6_extracted/recovery-workbench-fsd-p3-case-and-workflow-v4.md` |
| S-BRP | Business Requirements Program v4, §5.1 (REQ-RDF-001, REQ-RDF-014) | `03-requirements-and-specifications/recovery-workbench-business-requirements-program-v4-docx.md` |
| S-NFR | Non-functional specification v3, NFR-027, NFR-052 | `03-requirements-and-specifications/recovery-workbench-non-functional-specification-v3-docx.md` |
| S-BSEQ | Build Sequence Epic 1 and Epic 2 v6 | `11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| S-PS6 | Physical Schema v6 (header) | `06-data/recovery-workbench-physical-schema-v6.sql` |
| S-D35 | Client decision D-RCV-35 ACE DB alignment | `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md` |
| S-REG | Decision register: D-RCV-05, -12, -28, -34, -40, -44, -48; L-RCV-03, L-RCV-07 | `aisdlc/docs/decisions/decision-register.md`, `INC-001-decisions.md` |
| S-AUD | Phase 0 standards audit, A-01, A-04, A-17, A-19 | `aisdlc/evidence/phase0-standards-audit.md` |
| S-BS | Backend standards BS-2.1–2.9, BS-4.5, BS-7.2 | `aisdlc/.github/contexts/backend-standards.md` |
| S-AGENTS | `AGENTS.md` §2, §3.6, §3.7, §4.5, §4.6 | `<repo>/AGENTS.md` |
| S-V2 | 10 Nov 2026 spec (history; CLAR-001/002/004 rulings reused) | `aisdlc/output/INC-001-epic-1-RWB-E1-044/_v2-baseline/specify/spec.md` |

Precedence (RUN-BRIEF): D-RCV-35/36 > ADR v3 > Decision Log v10 > story files v7 > older maps and drafts. Where the story v7 conflicts with D-RCV-28 (Decision Log v10), D-RCV-28 is applied and the conflict is recorded in `document-gaps.md`.

## 1. Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `ENHANCEMENT_LOGIC_ONLY` |
| UI In Scope | NO |
| Logic In Scope | YES |
| API In Scope | NO |
| API Impact Type | NO_API_CHANGE |
| Impacted Existing Nodes | `backend/src/main/java/th/co/scb/ace/demo/recovery/platform/internal/RecoveryFlywayConfig.java`; `backend/src/test/java/th/co/scb/ace/demo/recovery/architecture/RecoveryMigrationLintTest.java`; `backend/src/main/resources/db/modulemigration/recovery/README.md`; `backend/build.gradle.kts` (coverage counters only, see SPEC-014) |
| New Nodes Required | YES: one test-scope container test class, one test-scope schema comparator, lint fixture folders, Flyway fixture folders (test resources only); story and plan convention files (SPEC-015) |
| Inherited Existing Behavior | Recovery Flyway bean settings (own history table `flyway_schema_history_recovery`, `outOfOrder(false)`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `cleanDisabled(true)`, `createSchemas(false)`, `validateMigrationNaming(true)`, placeholder `recoverySchema`); migrator data source selection; baseline migration lint rules; `recoveryIntegrationTest` / `recoveryCoverage*` tasks; `RecoveryDatabaseIT` baseline-on-non-empty check (S-AUD A-04, S-REG D-RCV-28, D-RCV-48) |
| Frontend Changes Required | NO |
| Backend Changes Required | YES |

Classification evidence: a prior trace chain exists (S-V2; traceability matrix row RWB-E1-044 to FR-RWB-013) and the code already holds the Flyway bean and the lint (S-AUD A-04). This story changes rules and checks only; no route, screen or endpoint.

**Production migration file.** None. Decision Log v10 D-RCV-28 and story v7 §13 both state that RWB-E1-044 "ships no production migration file"; `docs/architecture/migration-merge-order-map.md` excludes it. No source fixes a `<seq>` for this story. All `V<seq>__…` files written by this story are test fixtures outside `db/modulemigration/recovery/`.

## 2. Intent

Every change to schema `recovery` is a versioned, checksummed, forward-only Flyway migration that names the schema only as `${recoverySchema}`, carries its story key, and is checked by a build-time lint and a container test before merge (S-STORY §1, §8 BR1–BR8; S-DL10 D-RCV-28; S-BRP REQ-RDF-001, REQ-RDF-014).

## 3. Trigger and preconditions

| Trigger | Precondition | Source |
|---|---|---|
| Service start with `rwb.flyway.enabled=true` (default) | Schema `recovery` exists and is owned by `rwb_migrator` (`createSchemas(false)`); migrator credentials from environment or key store | S-ADR3 ADR-010; S-BS BS-4.5; S-NFR NFR-052; `infra/postgres/init/` |
| `./scripts/dev.ps1 test` (Gradle `test`) | none; the lint needs no database | S-REG D-RCV-05, D-RCV-28 (3) |
| `./scripts/dev.ps1 it` (Gradle `recoveryIntegrationTest`, tag `recovery-it`) | Docker available; fails, not skips, without Docker | S-REG D-RCV-28 (3), D-RCV-44 |

## 4. Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| AC1 / BR1 / BR5 | A pending migration applies once; version and checksum are recorded in `flyway_schema_history_recovery`; a rerun applies nothing | SPEC-001, SPEC-011 | INHERITED_EXISTING_BEHAVIOR + DIRECT (test) | Bean behaviour exists; container proof is new (T-044-10) | COVERED |
| AC2 / BR7 / X1 | Drift between the migration result and a target fails with MSG-P3-016 naming `<schema>.<table>.<column>` | SPEC-012 | DIRECT | Restated to a container-to-container comparison before every MR (CLAR-001) | COVERED (restated) |
| AC2 / BR7 (real SIT/UAT/PROD, read-only account, flag) | Drift check against real environments, gating deployment | — | DEFERRED | Parked by D-RCV-05; PO ruling CLAR-001 | DEFERRED |
| AC3 / BR2 | The schema comes from a parameter; the same file produces the table in schema `recovery` in two databases | SPEC-001, SPEC-002, SPEC-007, SPEC-011 | DIRECT | Value fixed to `recovery` (D-RCV-28, story §13); `RWB_SCHEMA=rwb_case` not applied (CLAR-003) | COVERED (restated) |
| AC4 / BR5 / X2 | An applied migration edited later fails validation, MSG-P3-016 names the version, service does not start | SPEC-001, SPEC-003, SPEC-011 | DIRECT | `validateOnMigrate(true)` made explicit | COVERED |
| AC5 / BR2 / X3 | A literal schema qualifier fails the build with MSG-P3-016 naming file and line | SPEC-004, SPEC-007, SPEC-010 | DIRECT | Rule widened per D-RCV-28 (2) | COVERED |
| AC6 / BR3 / X4 | Two non-fix files with the same key, or a file with no key, fail the build naming both files and the key | SPEC-004, SPEC-006, SPEC-010 | DIRECT + INHERITED | Second-non-fix and line-1 checks exist; finding format is new | COVERED |
| AC7 / BR4 / X5 | Clean refused; undo files refused; forward only | SPEC-001, SPEC-005, SPEC-011, SPEC-013 | INHERITED + DIRECT | Clean refusal shows Flyway's own message (D-RCV-28 (4)) | COVERED |
| AC8 / X6 | A migration that fails part way rolls back fully; failure recorded; service does not start | SPEC-003, SPEC-011 | DIRECT | Record = ERROR log with MSG-P3-016; no failed history row on PostgreSQL (CLAR-006) | COVERED (restated) |
| AC8 (job monitor display) | Run shows "failed" on the job monitor | — | DEFERRED | D-RCV-12 to RWB-E1-056 (CLAR-002) | DEFERRED |
| AC9 / X7 | Two instances starting together apply a pending migration exactly once; both start | SPEC-011 | INHERITED + DIRECT (test) | Flyway PostgreSQL lock; proof is new | COVERED |
| BR6 | Own history table | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | `HISTORY_TABLE` constant | COVERED |
| BR8 | No FK into `public`; lint names the file | SPEC-008, SPEC-010 | DIRECT | Dedicated rule | COVERED |
| D-RCV-28 (1) | Name, contiguous seq, one non-fix per key, fix rule, no `R__` | SPEC-005, SPEC-006 | INHERITED + DIRECT | Duplicate-seq, multi-key-line, fix-without-base findings are new | COVERED |
| D-RCV-28 / story §13 | Schema fixed to `recovery`, no per-environment override | SPEC-002 | DIRECT | Closes audit A-17 | COVERED |
| NFR-027 | Rollback by redeploying the previous tag | SPEC-013 | DIRECT (test) | `*:future` default + `outOfOrder(false)` | COVERED |
| NFR-052 / BS-4.5 | Migration account credentials outside the repository | SPEC-001 | INHERITED_EXISTING_BEHAVIOR | No change | COVERED |
| Story §10, TC-E1-044-10, `GET /admin/jobs?type=MIGRATION`, SCR-44, MSG-P4-002, `MigrationRunRecorder` | Read migration runs on the job monitor | — | DEFERRED | D-RCV-12 to RWB-E1-056 (build order 18) | DEFERRED |
| Audit A-19 | First story sets the story/plan-file convention | SPEC-015 | DIRECT | Assumption ASM-E044-08 | COVERED |

## 5. Backend Specification

### SPEC-RWB-E1-044-001 Recovery Flyway bean (extend, do not duplicate)

- Keep `RecoveryFlywayConfig` in `th.co.scb.ace.demo.recovery.platform.internal` with every inherited setting listed in §1 (S-AUD A-04; S-REG D-RCV-28, D-RCV-48; S-BS BS-2.3).
- Add `validateOnMigrate(true)` explicitly (story §12 sets it; Flyway's default is the same, so behaviour is unchanged and the intent becomes visible).
- Leave `ignoreMigrationPatterns` at Flyway's default (`*:future`) so a previous tag starts against a database that holds a later version (NFR-027, SPEC-013).
- Data source selection stays: migrator account when `rwb.flyway.user` is set, otherwise the main data source. Credentials come from environment or key store only (BS-4.5, NFR-052).
- The story §13 package `recovery.casewf.migration` is not created; module mapping belongs to RWB-TE-001 (S-AUD A-01). Recorded as gap DG-L06.

### SPEC-RWB-E1-044-002 Schema pinned to `recovery`

- On bean creation, if `rwb.schema` is not exactly `recovery`, start fails with a configuration error that names the property, the value found and D-RCV-28. Flyway is not built and nothing is migrated.
- Reason: `application.yaml` binds `rwb.schema: recovery`, but relaxed binding lets the environment variable `RWB_SCHEMA` override it; D-RCV-28 and story §13 say "no per-environment override" (S-AUD A-17).
- The error is a start-up configuration error, not a user message; no message ID applies (ASM-E044-03).

### SPEC-RWB-E1-044-003 Migration failure reported as MSG-P3-016

- When `migrate()` (including its validate step) throws a `FlywayException`, the bean logs one ERROR line carrying message ID `MSG-P3-016` with parameters `schema=recovery` and `object=<failed version, or the validation subject Flyway reports, or "recoveryFlyway" when none is exposed>`, then rethrows so the application context fails and the service does not start (S-STORY X2, X6; S-EMS4 MSG-P3-016).
- Code holds the message ID and parameters only; no message text (S-AGENTS §3.6; S-V2 CLAR-004 A).
- The log line holds no SQL values and no connection credentials (S-BS BS-4.6; audit A-07).
- A refused `clean()` is not wrapped: it shows Flyway's own message (D-RCV-28 (4)).

### SPEC-RWB-E1-044-004 Lint finding format

Every lint finding is one line: `MSG-P3-016 schema=recovery object=<file>:<line> rule=<RULE-ID> <detail>`, with a 1-based line number (0 for file-level rules such as naming, sequence and duplicates). The test fails listing all findings, not only the first (S-STORY X3, AC5, AC6; ASM-E044-04). Rule IDs: `L-NAME`, `L-UNDO`, `L-REPEATABLE`, `L-SEQ-GAP`, `L-SEQ-DUP`, `L-HEADER`, `L-HEADER-MULTI`, `L-KEY-DUP`, `L-FIX-NO-BASE`, `L-FIX-LINE2`, `L-SEARCH-PATH`, `L-LITERAL-SCHEMA`, `L-FK-OUTSIDE`, `L-GRANT`.

### SPEC-RWB-E1-044-005 File-level naming rules (D-RCV-28 (1))

| Rule | Check | Status |
|---|---|---|
| L-NAME | Name matches `^V(\d{4})__(rwb_[a-z0-9]+_\d{3})_[a-z0-9_]+\.sql$` | Inherited |
| L-REPEATABLE | Any `R__*.sql` fails | Inherited |
| L-UNDO | Any `U*.sql` fails with its own rule ID (today it falls into L-NAME) | New |
| L-SEQ-DUP | Two files with the same `<seq>` fail, naming both | New (today reported as a gap) |
| L-SEQ-GAP | Sequences must be `0001..N` contiguous | Inherited |

Any non-`.sql` file other than `README.md` in the folder is reported under L-NAME (ASM-E044-05).

### SPEC-RWB-E1-044-006 Header and story-key rules

| Rule | Check | Status |
|---|---|---|
| L-HEADER | Line 1 equals `-- Story: <KEY>`, where `<KEY>` is derived from the file name (`rwb_e1_044` gives `RWB-E1-044`) | Inherited |
| L-HEADER-MULTI | A second `-- Story:` line anywhere in the file fails | New |
| L-KEY-DUP | At most one non-fix file per key; the finding names both files and the key | Inherited, finding format new |
| L-FIX-LINE2 | A file whose line 2 starts `-- Fix:` must have a non-empty reason | New |
| L-FIX-NO-BASE | A fix file needs exactly one non-fix file of the same key with a lower `<seq>` | New |

### SPEC-RWB-E1-044-007 Literal-schema rule (D-RCV-28 (2))

Before matching, remove `--` comments to end of line, `/* … */` block comments and the contents of single-quoted string literals (schema names in strings are an accepted gap, D-RCV-28 (2)). Dollar-quoted bodies (`$$ … $$`, `$tag$ … $tag$`) are scanned as SQL.

L-LITERAL-SCHEMA fails any of the following unless the qualifier is `${recoverySchema}`, `information_schema` or `pg_catalog`:

1. A qualified name in an object-name position: the name after `TABLE`, `VIEW`, `MATERIALIZED VIEW`, `SEQUENCE`, `INDEX … ON`, `TRIGGER … ON`, `FUNCTION`, `PROCEDURE`, `TYPE`, `DOMAIN`, `REFERENCES`, `FROM`, `JOIN`, `INTO`, `UPDATE`, `TRUNCATE`, `COMMENT ON <kind>`, `OWNED BY`. Quoted identifiers (`"rwb_case".t`) count.
2. A qualified type: after `::`, after `AS` inside `CAST(`, and as a column data type in a column definition.
3. A bare schema name after `SCHEMA`.

The inherited check for `recovery.`, `ace.` and `public.` anywhere in code text stays. L-SEARCH-PATH (`SET search_path` in any form, inherited) stays. The position list is the minimum; the plan may extend it but not narrow it (ASM-E044-06). This replaces the story §13 approach of matching names from `sys_objects`, which does not exist until RWB-E1-001 (D-RCV-28 takes precedence).

### SPEC-RWB-E1-044-008 No foreign key outside the recovery schema (BR8)

L-FK-OUTSIDE fails `REFERENCES <qualifier>.<table>` when the qualifier is not `${recoverySchema}`, with detail `BR8 foreign key outside recovery schema`. An unqualified `REFERENCES` resolves to `recovery` through Flyway's default schema and the migrator's `search_path`, so it passes (S-STORY BR8; S-ADR3 ADR-010; S-D35 U4). A finding may be reported under both L-LITERAL-SCHEMA and L-FK-OUTSIDE.

### SPEC-RWB-E1-044-009 GRANT and REVOKE (inherited)

L-GRANT (GRANT/REVOKE at line start fails) stays as in the baseline lint (S-BS BS-2.5, BS-2.6). The conflict with RWB-E1-069 v7 and Environment and Deployment Design v4 §5, which put grants inside a migration, is recorded as DG-L05 and left to RWB-E1-069.

### SPEC-RWB-E1-044-010 Lint testability and fixtures

- The lint logic takes a folder and returns the findings, so the production test scans `classpath:db/modulemigration/recovery` and fixture tests scan fixture folders under `backend/src/test/resources/migration-lint/`.
- Each rule in SPEC-004 has at least one failing fixture and one passing fixture, and the test asserts the exact rule ID, file and line.
- The production-folder test stays green on the empty folder (README only).
- Fixtures use synthetic table and column names and no personal data (RUN-BRIEF rule 7).

### SPEC-RWB-E1-044-011 Container proof of Flyway behaviour

A new test class tagged `@Tag("recovery-it")` runs in `recoveryIntegrationTest`, uses PostgreSQL `postgres:16.16-alpine` (as `RecoveryDatabaseIT`), creates schema `recovery` in setup, and builds the recovery Flyway with the production settings, changing only `locations` to a fixture folder under `backend/src/test/resources/flyway-fixtures/`. Fixture names comply with D-RCV-28 and use key `rwb_e1_044`. Cases are listed in §9 (T-044-10..T-044-17).

### SPEC-RWB-E1-044-012 Drift comparison (AC2, BR7 restated)

A test-scope schema comparator lists, for schema `recovery`, the tables, columns with data type and nullability, constraints, indexes and views from `information_schema` and `pg_catalog` in two databases, and reports each difference as `MSG-P3-016 schema=recovery object=recovery.<table>.<column>` (or the constraint, index or view name). The test applies the same fixtures to two clean databases, adds column `note_x` by hand to table `queue` in one, and asserts exactly one difference naming `recovery.queue.note_x`. No real-environment comparison, no read-only account and no flag `rwb.p3.migration-drift-gate` (D-RCV-05, D-RCV-44; S-V2 CLAR-001 A).

### SPEC-RWB-E1-044-013 Forward only and rollback by previous tag (NFR-027)

- `clean()` is refused with Flyway's own message and no object changes (D-RCV-28 (4)).
- A database that holds a later version than the files on the classpath (previous tag) validates and starts, with nothing applied (`*:future` default).
- With `outOfOrder(false)`, a pending file with a lower version than the highest applied one fails validation and is reported as SPEC-003.

### SPEC-RWB-E1-044-014 Coverage gate

Changed main classes (`RecoveryFlywayConfig` and any main class the plan adds) reach at least 80% on LINE, INSTRUCTION, BRANCH and METHOD in JaCoCo (S-BS BS-7.2; `.github/rules/specification-execution-gates.md`). Today `recoveryCoverageVerification` sets LINE and BRANCH only and reads execution data from `test` only. The plan adds INSTRUCTION and METHOD limits, or produces equivalent per-class evidence. A `build.gradle.kts` change is a shared-file change and must be named in the plan (D-RCV-40; ASM-E044-07). The test-scope lint and comparator are covered at rule level by SPEC-010 and SPEC-012.

### SPEC-RWB-E1-044-015 Documentation and convention (audit A-19)

- Update `db/modulemigration/recovery/README.md` to list the rule IDs in SPEC-004 and the MSG-P3-016 finding format, and reword the sentence "When RWB-E1-001 ships V0001 to V0003" so it no longer gives V0002 and V0003 to RWB-E1-001. The `RWB_LOAD_REFERENCE_SCHEMA=false` instruction stays, tied to the merge of the baseline and view migrations. The merge-time `<seq>` comes from D-RCV-28 (DG-L04, DG-L07).
- Set the story and plan convention: `docs/stories/RWB-E1-044/story.md`, which holds the story key, a link to the story v7 path and this spec, and the restated ACs from §6, and `docs/stories/RWB-E1-044/plan.md` (written by the Implementation Planner), in the code repository (S-AGENTS §6, §7; ASM-E044-08).

## 6. Restated acceptance criteria (applied D-RCV-28 and PO rulings)

| AC | Restatement used for tests | Why restated |
|---|---|---|
| AC1 | Fixture `V0001__rwb_e1_044_add_queue.sql` (line 1 `-- Story: RWB-E1-044`) applies once; version `0001` and its checksum are in `flyway_schema_history_recovery`; a second migrate applies nothing | V12 and the `RWB_SCHEMA` background conflict with D-RCV-28 |
| AC2 | See SPEC-012 | D-RCV-05; CLAR-001 |
| AC3 | The same fixture creates `recovery.timer` in two clean databases; the classpath resource is identical; the recorded checksums are equal | Schema fixed to `recovery` |
| AC4 | Version `0001` applied, then the file changed: migrate fails validation, ERROR `MSG-P3-016` names `0001`, the context does not start | Naming |
| AC5 | Fixture line 2 `CREATE INDEX ix_a ON recovery.queue (team_code)` gives `MSG-P3-016 … object=<file>:2 rule=L-LITERAL-SCHEMA` | Line 1 is the header under D-RCV-28 |
| AC6 | Two non-fix files with key `rwb_e1_028` give one L-KEY-DUP finding naming both files and `RWB-E1-028` | Naming |
| AC7 | `clean()` is refused (Flyway's message); a `U0001__…sql` file gives L-UNDO | D-RCV-28 (4) |
| AC8 | Fixture whose second statement references a missing table: the first statement's object is absent, no history row for that version, ERROR `MSG-P3-016` names the version, the context does not start | PostgreSQL transactional DDL (CLAR-006); job monitor deferred |
| AC9 | Two Flyway instances migrate concurrently with one pending fixture: one history row for the version, both calls return without error | Naming |

## 7. Field matrix (configuration)

| Field | Source | Rule | Validation |
|---|---|---|---|
| `rwb.schema` | `application.yaml` | Must equal `recovery` | SPEC-002 |
| `rwb.flyway.enabled` | `application.yaml` | Default `true`; inherited | — |
| `rwb.flyway.url` / `user` / `password` | Environment or key store | Never in the repository | BS-4.5, NFR-052 |
| `rwb.flyway.location` | `application.yaml` | `classpath:db/modulemigration/recovery` | Inherited |
| History table | Code constant | `flyway_schema_history_recovery` | BR6 |
| Placeholder | Code | `recoverySchema` = `rwb.schema` | D-RCV-28 |

## 8. Status-transition matrix

| From | Event | To | Record |
|---|---|---|---|
| (no history table) | First migrate on a non-empty schema | Baseline row version 0 | Inherited (D-RCV-48) |
| Pending | Migrate succeeds | Applied (history row with checksum) | History table |
| Pending | Migrate fails part way | Pending (rolled back, no row) | ERROR log MSG-P3-016 (SPEC-003) |
| Applied | File checksum changed | Validation failed; service does not start | ERROR log MSG-P3-016 |

No case status changes (S-STORY §9).

## 9. Exceptions

| ID | Condition | Behaviour | Message | Spec / Test |
|---|---|---|---|---|
| X1 | Schema difference | Comparator reports each object | MSG-P3-016 | SPEC-012 / T-044-15 |
| X2 | Applied file edited | Validation fails, start stops | MSG-P3-016 | SPEC-003 / T-044-12 |
| X3 | Literal schema | Lint fails with file and line | MSG-P3-016 | SPEC-007 / T-044-02 |
| X4 | Duplicate or missing key | Lint fails | MSG-P3-016 | SPEC-006 / T-044-03 |
| X5 | Clean or undo | Clean refused (Flyway message); undo file fails lint | Flyway message / MSG-P3-016 | SPEC-005, -013 / T-044-04, T-044-13 |
| X6 | Fails part way | Rollback, ERROR log, start stops | MSG-P3-016 | SPEC-003 / T-044-14 |
| X7 | Two instances | One applies, the other finds nothing pending | None | SPEC-011 / T-044-16 |
| — | `rwb.schema` ≠ `recovery` | Start fails, configuration error | None (ASM-E044-03) | SPEC-002 / T-044-08 |

## 10. Tests

| Test | Level | Covers | Assertion |
|---|---|---|---|
| T-044-01 | Unit (lint fixtures) | SPEC-005 | L-NAME, L-UNDO, L-REPEATABLE, L-SEQ-DUP, L-SEQ-GAP each fail on their fixture and pass on a compliant one |
| T-044-02 | Unit | SPEC-007, AC5 | Each listed position, qualified type and bare schema fails; `${recoverySchema}`, `information_schema`, `pg_catalog`, commented-out text and a string literal pass; dollar-quoted body is scanned |
| T-044-03 | Unit | SPEC-006, AC6 | L-HEADER, L-HEADER-MULTI, L-KEY-DUP (both files named), L-FIX-LINE2, L-FIX-NO-BASE |
| T-044-04 | Unit | SPEC-005, AC7 | `U0001__rwb_e1_044_x.sql` gives L-UNDO |
| T-044-05 | Unit | SPEC-008, BR8 | `REFERENCES public.account(id)` gives L-FK-OUTSIDE; `REFERENCES ${recoverySchema}.t(id)` and unqualified pass |
| T-044-06 | Unit | SPEC-004 | Finding text format, 1-based line, all findings listed |
| T-044-07 | Unit | SPEC-010 | Production folder (README only) passes |
| T-044-08 | Unit | SPEC-002 | `rwb.schema=rwb_case` fails start naming D-RCV-28; `recovery` passes |
| T-044-09 | Unit | SPEC-003, SPEC-001 | Mocked `FlywayException` gives one ERROR log with `MSG-P3-016` and rethrows; success path logs no error; both data-source branches |
| T-044-10 | Container | AC1 | Applies once, checksum recorded, rerun applies nothing |
| T-044-11 | Container | AC3 | Two databases, `recovery.timer` exists in both, equal checksums |
| T-044-12 | Container | AC4 | Changed file fails validation naming `0001` |
| T-044-13 | Container | AC7, SPEC-013 | `clean()` refused, object count unchanged; previous-tag start passes; lower pending version fails |
| T-044-14 | Container | AC8 | First statement rolled back, no history row, ERROR MSG-P3-016 |
| T-044-15 | Container | AC2, SPEC-012 | Exactly one difference `recovery.queue.note_x` |
| T-044-16 | Container | AC9 | Concurrent migrate: one history row, both succeed |
| T-044-17 | Container | BR8 | Applying a fixture with an FK into `public` as `rwb_migrator` fails in the database (defence in depth; `public` access revoked, `infra/postgres/init/20-grants.sql.inc`) |

Existing `RecoveryDatabaseIT.recoveryFlywayBaselinedItsOwnHistoryTable` stays and covers baseline-on-non-empty.

## 11. Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Backend main: `RecoveryFlywayConfig` | YES | YES (T-044-08, T-044-09) | 80% LINE, INSTRUCTION, BRANCH, METHOD | SPEC-001, -002, -003, -014 | Logic added: schema pin, failure reporting | All four counters ≥ 80% for the class |
| Backend test tooling: migration lint | YES | YES (T-044-01..07) | Rule-level: every rule has a failing and a passing fixture | SPEC-004..-010 | Test-scope class; JaCoCo `recoveryCoverage*` measures main classes | Every rule ID asserted |
| Backend test tooling: schema comparator | YES (new) | Container (T-044-15) | Rule-level | SPEC-012 | Needs two databases | One difference found, zero on equal databases |
| Container behaviour | YES (new IT) | N/A (integration) | Run before every MR (D-RCV-44) | SPEC-011, -013 | Flyway behaviour needs PostgreSQL | T-044-10..17 green, result attached to implementation evidence |
| Build file `build.gradle.kts` | Possibly (SPEC-014) | N/A | N/A | SPEC-014 | Shared file; plan names it | Verification fails below 80% on any counter |
| Migration folder README, story/plan files | YES | N/A | N/A | SPEC-015 | Documentation | Content matches SPEC-004 |
| Frontend | NO | N/A | N/A | — | UI In Scope NO | — |
| API | NO | N/A | N/A | — | NO_API_CHANGE | — |

## 12. API assessment

No endpoint is added or changed. `GET /api/recovery/v1/admin/jobs` (API Specification v4, `x-module` P1) and SCR-44 are built by RWB-E1-056 (build order 18, Build Sequence v6); the E1-044 parts are deferred there (D-RCV-12). See `contracts/backend-apis.json`.

## 13. Frontend Specification

N/A. UI In Scope = NO. Story §15 says "No new screen in this story"; SCR-44 display is deferred (D-RCV-12). `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`.

## 14. Not applicable in this repository (carried to the ACE port)

The ACE-specific D-RCV-45 `db-migrate` guard, the H2 skip and the Jenkins step have no counterpart here: there is no H2, no `db-migrate` profile, no ACE core Flyway and no Jenkins (`README.md`, local-versus-target table). They are recorded as ASM-E044-09 and a shared-update open-item candidate.

## 15. Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | AC2, BR7, story §13 flag | Real-environment drift gate, read-only account, flag | Scope of the drift check | Resolved from sources: PO ruling 2026-11-09 recorded in S-V2 CLAR-001 A; D-RCV-05, D-RCV-44. Container-to-container comparison before every MR | RESOLVED | SPEC-012 |
| CLAR-002 | AC8 (monitor), §10, §12 endpoint, §15, TC-E1-044-10 | Job-monitor parts | Deferred surfaces | D-RCV-12; S-V2 CLAR-002 A: deferred to the job-monitor story (RWB-E1-056) | RESOLVED | — (DEFERRED) |
| CLAR-003 | AC1–AC9 background, §12 | `RWB_SCHEMA=rwb_case`, `${schema}`, V12–V18 names vs D-RCV-28 | Test data and configuration | Precedence: Decision Log v10 D-RCV-28 over story v7; restated in §6 | RESOLVED | SPEC-002, SPEC-011 |
| CLAR-004 | §14 MSG-P3-016 | Message text in code? | Logging and lint output | S-V2 CLAR-004 A; AGENTS §3.6: ID and parameters only | RESOLVED | SPEC-003, SPEC-004 |
| CLAR-005 | `<seq>` for this story | Which number does E1-044 take? | Production file | None: D-RCV-28 (Decision Log v10) and story §13 say E1-044 ships no production migration | RESOLVED | §1 |
| CLAR-006 | AC8, X6 | "History records version 17 as failed" vs PostgreSQL transactional DDL | Failure record | Assumption ASM-E044-02: ERROR log with MSG-P3-016 is the record; DG-L03 | RESOLVED (assumption) | SPEC-003 |
| CLAR-007 | AC7 | Message on refused clean | Message | D-RCV-28 (4): Flyway's own message | RESOLVED | SPEC-013 |
| CLAR-008 | Story §13 package | `recovery.casewf.migration` vs `platform.internal` | Class location | Audit A-01 owned by RWB-TE-001; keep the baseline location (ASM-E044-01); DG-L06 | RESOLVED (assumption) | SPEC-001 |
| CLAR-009 | A-17 | Message for a wrong schema value | Error type | ASM-E044-03: configuration error, no message ID | RESOLVED (assumption) | SPEC-002 |
| CLAR-010 | A-19 | Story and plan file location | Convention | ASM-E044-08 | RESOLVED (assumption) | SPEC-015 |
| CLAR-011 | Coverage | INSTRUCTION and METHOD counters missing from the build | Gate evidence | ASM-E044-07: the plan adds them or gives per-class evidence | RESOLVED (assumption) | SPEC-014 |

No question was put to the user (L-RCV-03). Assumptions are in `assumptions.md`; candidate open items are in `shared-updates.md`.

## 16. Status

- `MCP_STATUS_SUMMARY: No Jira, Confluence, GitLab or Figma MCP is connected (RUN-BRIEF rule 5); not needed for a backend-only story.`
- `MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]`
- `CHANGE_CLASSIFICATION_SUMMARY: Existing Flyway bean and lint are extended; no UI or API change.`
- `CHANGE_CLASSIFICATION_RESULT: ENHANCEMENT_LOGIC_ONLY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: baseline Flyway bean and lint exist (audit A-04); rules and checks change]`
- `REQUIREMENT_COVERAGE_SUMMARY: 9 ACs, 8 BRs, D-RCV-28, NFR-027, NFR-052, A-17 and A-19 mapped; job-monitor and real-environment drift parts deferred by D-RCV-12 and D-RCV-05.`
- `REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 19] [COVERED_RULES: 16] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]` (3 DEFERRED by decision; contradictions between sources are settled by precedence, see `document-gaps.md`)
- `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]`
- `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`
