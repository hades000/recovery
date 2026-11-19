---
run_id: INC-008-epic-1-RWB-E1-043
story: RWB-E1-043
title: Reference data service with versioned tables
stage: specify
agent: Technical Specifier
date: 2026-11-17
status: SUCCESS
supersedes: _v2-baseline/specify/spec.md (historical; RUN_ID INC-009, D-RCV-47 schema basis; kept unchanged)
---

# Technical specification: RWB-E1-043 Reference data service with versioned tables

## 0. Sources and conventions

All `requirement/legacy/` paths are in `17 AI-First SDLC Repository v2` (read only). Short tags are
used in the tables below.

| Tag | Document, version, location |
|---|---|
| S7 | Story file v7, RWB-E1-043 (file v2, 16 Nov 2026): `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| CARD | Increment card INC-008: `aisdlc/docs/increments/INC-008-epic-1-RWB-E1-043.md` |
| REQ | Canonical requirements REQ-RWB-002 v2.0 (16 Nov 2026), FR-RWB-011, NFR-RWB-005/006/008/009: `requirement/RecoveryWorkbench_Requirements.md` |
| D35 / D36 | Client decisions D-RCV-35 and D-RCV-36: `aisdlc/docs/decisions/d-rcv-35-ace-db-alignment.md`, `d-rcv-36-temporal-and-drools.md` (line 145 lists the E1-043 changes) |
| ADR3 | Architecture Decision Records v3 (ADR-010, ADR-012): `requirement/legacy/05-technical-architecture/recovery-workbench-architecture-decision-records-v3.md` |
| DL10 | Decision Log v10 (D-RCV-28 migration rule): `requirement/legacy/01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` |
| PS6 | Physical Schema v6 (16 Nov 2026): `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| API4 | API Specification v4.0.0 (16 Nov 2026): `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| MSG4 | Error and Message Standard v4: `requirement/legacy/07-screens-and-experience/recovery-workbench-error-and-message-standard-v4-docx.md` |
| TC7 | Test Cases v7, TC-E1-043-01..11: `requirement/legacy/09-testing-and-quality/recovery-workbench-test-cases-v7-xlsx.md` |
| BS6 | Build Sequence Epic 1 and 2 v6: `requirement/legacy/11-delivery-and-operations/recovery-workbench-build-sequence-epic-1-and-epic-2-v6-xlsx.md` |
| BAT4 | Batch and Scheduling Design v4: `requirement/legacy/05-technical-architecture/recovery-workbench-batch-and-scheduling-design-v4-docx.md` |
| E42 | RWB-E1-042 preserved implementation: `aisdlc/output/INC-003-epic-1-RWB-E1-042/_v2-baseline/implement/` (README, `sql/V042_2__parameter_seed.sql`) |
| CTX | `aisdlc/.github/contexts/backend-context.md` v2.0, `backend-standards.md` (BS-x), `testing-standards.md` v2.0 |
| AUD | Phase 0 audit `aisdlc/evidence/phase0-standards-audit.md` (A-01, A-03, A-04, A-06) |
| AG | `AGENTS.md` v2 (repository root) |

- `A-nn` = labelled assumption in `assumptions.md`. `GAP-nn` = row in `document-gaps.md`.
- Precedence used (RUN-BRIEF): D35/D36, then ADR3, then DL10, then S7, then older maps and drafts.
- Baseline reuse: the `_v2-baseline` spec's structure and its CLAR-004..007 decisions are reused where
  still correct. Its 13-code list (HOLIDAY), HOLIDAY fixtures, FR-RWB-012/020 mapping, RWB-E1-029/048
  references and API v2 basis are dropped (D36 line 145; S7 BR1; REQ FR-RWB-011).

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — S7 §15 "No screen in this story" |
| Logic In Scope | `YES` |
| API In Scope | `YES` — S7 §12 and §13 step 7 |
| API Impact Type | `NEW_API_REQUIRED` — first implementation of two operations already in API4 (`POST /admin/reference-loads`, `POST /admin/reference-loads/{loadId}/approve`). No OpenAPI change is made by this story. |
| Impacted Existing Nodes | `platform.internal.ApiExceptionHandler` / `ProblemFactory` / `platform.api.ApiProblemException` (carry a story message, SPEC-020); `platform.api.RecoveryFlags`, `platform.internal.RecoveryProperties`, `application.yaml` (flag `rwb.p3.refdata-versions`, SPEC-018); `RecoveryBoundaryTest` (refdata table rule, SPEC-019). |
| New Nodes Required | Package `recovery.casewf.refdata` (+ `.api`, `.internal`): `ReferenceVersionRegistry`, `ReferenceDataService`, `ReferenceVersion`, `VersionedRows`, `NoVersionInForceException`, `ReferenceTableCodeSource` (SPI), `ReferenceVersionRegistryImpl`, `ReferenceDataServiceImpl`, `ReferenceRowCache`, `ReferenceVersionRepository`, `ReferenceRowRepository`, `ReferenceVersionEntity`, `ReferenceRowEntity`, `ReferenceVersionLogger`, `ReferenceTableColumns`, `ReferenceRowCheck`, `ContentHasher`, `BusinessDateSource`. P4 package `recovery.access` (+ `.internal`): `ReferenceLoadController`, `ReferenceLoadFileReader`, `LovReferenceTableCodes`, `CapabilityCheck`. Migration `V<seq>__rwb_e1_043_reference_versions.sql`. |
| Inherited Existing Behavior | Recovery Flyway bean and lint (RWB-E1-044 parts in baseline, AUD A-04); JWT resource server and `/api/recovery/**` role gate (`SecurityConfig`); Problem body (README decision 1); MSG-P4-001/002/003 in `ApiError` (README decision 5); Modulith verify and boundary test (RWB-TE-001). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## User story intent interpretation

The reference data administrator loads one of 12 reference tables (S7 BR1) as a new, immutable,
dated version; a different person with the approve right approves it; services read the approved
version in force for a business date and log which version they used. Business values move out of
code into versioned rows (S7 §1, §2; REQ FR-RWB-011). Rule tables are excluded (D36 line 145; AG §4.9).

## Entry trigger and preconditions

| # | Precondition (S7 §3) | State in this repository | Handling |
|---|---|---|---|
| P1 | RWB-E1-044 done (Flyway with schema placeholder) | Recovery Flyway bean, `${recoverySchema}` and lint exist (AUD A-04) | Inherited |
| P2 | RWB-E1-042 done: serves `refdata.cache.ttl-seconds` (300, DL11) | Catalog row exists in E42 seed; `ParameterService` Java is not in this repository | Read through `ParameterService` (SPEC-013); build sequenced after E1-042 code (A-14) |
| P3 | LOV-REF-TABLE loaded with the 12 codes, no rule code | PS6 seeds 25 codes incl. 5 rule codes and HOLIDAY | GAP-04; SPEC-002 refuses any code without a column definition |
| P4 | P4 load endpoint deployed | No P4 code exists | Built here per S7 §13 step 7 (SPEC-015/016); GAP-09 |
| P5 | Loader holds Reference data C; approver holds A (assumed RW-RISK) | PS6: no role holds REFERENCE_DATA A | SPEC-016, A-08, GAP-14 |
| P6 | Business date from the ACE batch record (`v_ace_batch_status`) | View exists (PS6); no rule picks one date | SPEC-017, A-01, GAP-12 |

Triggers: an HTTP load or approve call (S7 §4 steps 1, 5); a service call to `ReferenceDataService`
on engine start or cache expiry (S7 §4 step 8).

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| S7 BR1; D36 | 12 reference codes served; list is data (LOV-REF-TABLE); no rule code; holiday from `v_ace_holiday` | SPEC-002, SPEC-021 | DIRECT | Code accepted only if in LOV-REF-TABLE and has a column definition | COVERED |
| S7 BR2 | One load = one version, number = max+1; never changed after write | SPEC-001, SPEC-007 | DIRECT | Trigger refuses row changes | COVERED |
| S7 BR3 | Version in force = APPROVED with latest valid_from ≤ business date | SPEC-011 | DIRECT | | COVERED |
| S7 BR4 | Effective only after approval by a non-author | SPEC-008, SPEC-001 | DIRECT | Service check + DB CHECK | COVERED |
| S7 BR5 | Any failed check refuses the load in full | SPEC-003, SPEC-004, SPEC-005, SPEC-007 | DIRECT | One transaction | COVERED |
| S7 BR6 | valid_from before business date refused | SPEC-005 | DIRECT | Equal accepted (A-05) | COVERED |
| S7 BR7 | Every engine logs table code and version read | SPEC-014 | DIRECT | Logger delivered; engine hook calls are owned by engine stories (A-02) | COVERED |
| S7 BR8 | Approval sets valid_to of replaced version to day before new valid_from | SPEC-010 | DIRECT | | COVERED |
| S7 BR9 | Engine with no version in force does not run | SPEC-012 | DIRECT | Exception + alert; engines stop on it (A-02) | COVERED |
| S7 X1 / AC2 / AC5 | Author approval refused MSG-P7-002; version stays VALIDATED, never served | SPEC-008, SPEC-011 | DIRECT | 409 | COVERED |
| S7 X2 / AC4 | Schema or key failure refused MSG-P3-027 naming row and column; nothing written | SPEC-003 | DIRECT | 422 | COVERED |
| S7 X3 / AC6 | Past valid_from refused MSG-P3-027 naming valid from | SPEC-005 | DIRECT | 422 | COVERED |
| S7 X4 / AC7 | Same table, valid_from, hash: return first load, write nothing | SPEC-006 | DIRECT | 201 same body (A-06) | COVERED |
| S7 X5 / AC8 | Concurrent approvals: one wins, other MSG-GEN-004 | SPEC-009 | DIRECT | Optimistic lock on `version` | COVERED |
| S7 X6 / AC9 | No version in force: engine does not start, alert with MSG-P3-027 | SPEC-012 | DIRECT | | COVERED |
| S7 X7 / AC10 | Header-only file refused MSG-GEN-001 naming "rows" | SPEC-004 | DIRECT | 422 | COVERED |
| S7 AC1 | v4 approved with 5 rows; v3 keeps 4 rows, valid_to 2026-11-30; v3 served 30 Nov, v4 1 Dec | SPEC-007, SPEC-010, SPEC-011 | DIRECT | | COVERED |
| S7 AC3 | Services read tables via service, holiday via `v_ace_holiday`; one log line per table; no customer identifier | SPEC-014, SPEC-021 | DIRECT | Verified with a test consumer (A-02) | COVERED |
| S7 §9 | VALIDATED → APPROVED; ROLLED_BACK never served | SPEC-008, SPEC-011 | DIRECT | Rollback transition not in S7 §12/§13 (GAP-10) | COVERED |
| S7 §10 | Load C (RW-REFADM, RW-COE); approve A (assumed RW-RISK); read R | SPEC-015, SPEC-016 | DIRECT | Rights read from `permission` data (A-08) | COVERED |
| S7 §11 | DF-REF-159..171, 181..184 written; DF-REF-028/029 read through P4 | SPEC-001, SPEC-002 | DIRECT | | COVERED |
| S7 §12 load | 201 ReferenceLoad; 401/403/409/422/503; idempotency on table, valid_from, hash | SPEC-015, SPEC-006 | DIRECT | | COVERED |
| S7 §12 approve | 200; 401/403/404/409/503; repeat approval 200 same body | SPEC-016, SPEC-008 | DIRECT | | COVERED |
| S7 §12 lists | `GET /admin/lists/{listCode}` "Used by AC1 to read version 3" | SPEC-011 | DIRECT | AC1 read via `versions()`; endpoint not in §13 build steps (GAP-17) | COVERED |
| S7 §12 interfaces | `ReferenceVersionRegistry`, `ReferenceDataService`, records, `NoVersionInForceException`; no events | SPEC-007..012 | DIRECT | Signatures verbatim | COVERED |
| S7 §13 DB | Tables, constraints, append-only trigger | SPEC-001 | DIRECT | Guarded DDL over PS6 (GAP-01, GAP-02) | COVERED |
| S7 §13 cache | TTL from `refdata.cache.ttl-seconds`; never serves non-APPROVED | SPEC-013 | DIRECT | | COVERED |
| S7 §13 flag | `rwb.p3.refdata-versions`; off = previous path | SPEC-018 | DIRECT | | COVERED |
| S7 §13 done-when | Boundary test: no read of the two tables outside `casewf.refdata` | SPEC-019 | DIRECT | SIT version-1 loads are data, not code (SPEC-022) | COVERED |
| S7 §14 | MSG-P3-027, P7-002, GEN-001, GEN-004, P4-002 | SPEC-020 | DIRECT | Text from MSG4 (GAP-06) | COVERED |
| S7 §16 TC-11 | RW-CASEOWN load refused MSG-P4-002 | SPEC-015 | DIRECT | | COVERED |
| S7 §17 | Guardrails: no business literal, no personal data in logs, no foreign table read, append only, cache only APPROVED, no rule table | SPEC-001, SPEC-013, SPEC-014, SPEC-019, SPEC-021 | DIRECT | | COVERED |
| REQ FR-RWB-011 | Versioned lists, valid-from/to, maker-checker, load path (rollback path: GAP-10) | SPEC-001..017 | DIRECT | | COVERED |
| REQ NFR-RWB-005 | Method security, RBAC, audit | SPEC-015, SPEC-016 | DIRECT | Decision log entry deferred (GAP-07) | COVERED |
| REQ NFR-RWB-006 | No personal data in logs/tests | SPEC-014, SPEC-023 | DIRECT | | COVERED |
| REQ NFR-RWB-008 | Logs, metrics | SPEC-012, SPEC-014 | DIRECT | | COVERED |
| REQ NFR-RWB-009 | Flag-off path | SPEC-018 | DIRECT | | COVERED |
| AUD A-06 | Flags and parameters are config literals | SPEC-013, SPEC-018 | DIRECT | See §"A-06 split" | COVERED |

## SPEC definitions (Backend Specification)

### Frontend Specification

`NOT_APPLICABLE`. S7 §15: no screen; SCR-39, SCR-40, SCR-42 are Epic 8 (S7 §19). No frontend consumer
exists for the two endpoints in this story; they are backend-only and called by HTTP clients
(`contracts/frontend-integrations.json`).

### Backend Specification

**SPEC-RWB-E1-043-001 Schema migration.** One file `V<seq>__rwb_e1_043_reference_versions.sql` in
`backend/src/main/resources/db/modulemigration/recovery/`, line 1 `-- Story: RWB-E1-043`, schema only
as `${recoverySchema}` (DL10 D-RCV-28; lint in `RecoveryMigrationLintTest`; S7 §13 says `${schema}`: GAP-18). `<seq>` is the next
contiguous number at merge (GAP-15). Because PS6 (V0001 of RWB-E1-001) already creates both tables,
the file is guarded like E42 (`CREATE TABLE IF NOT EXISTS`, then add-if-absent) and must give the
same end state on an empty schema and on the PS6 baseline (GAP-02):
- `reference_version`: all PS6 columns (incl. `version_label`, `dry_run_counts`, `rollback_reason`,
  `change_request_ref`, `impact_summary`, `test_result`, `rollback_plan`, `verified_by`,
  `verified_at`, `verify_note`) and the 7 standard columns. Constraints: `uk_reference_version
  UNIQUE (table_code, version_no)` (PS6); `UNIQUE (table_code, valid_from, content_hash)`;
  `CHECK (approver_user_id IS NULL OR approver_user_id <> author_user_id)`; partial unique index on
  `(table_code, valid_from) WHERE status = 'APPROVED'` (S7 §13).
- `reference_row`: PS6 columns; drop `uk_reference_row UNIQUE (row_key)` if present and add
  `UNIQUE (version_id, row_key)` (S7 §13; GAP-01 — PS6's constraint makes AC1 impossible); keep
  `fk_reference_row_version_id ... ON DELETE RESTRICT` and `ix_reference_row_version_id` (PS6).
- Append-only triggers (S7 §13, §17): `BEFORE UPDATE OR DELETE` on `reference_row` refuses always;
  `BEFORE UPDATE OR DELETE` on `reference_version` refuses DELETE and any UPDATE that changes a
  column other than `status`, `approver_user_id`, `approved_at`, `valid_to` and the 7 standard
  columns (DELETE refusal: A-04; the column list conflicts with API4 verify/rollback: GAP-11).
- No `CREATE`/`GRANT`/`REVOKE`/`SET search_path`/`R__`; no seed rows in `reference_version`,
  `reference_row` or `lov_value` (seed ownership: §"Seed ownership").
- One INSERT block (guarded `ON CONFLICT (param_key) DO NOTHING`) of 12 `parameter_catalog` rows
  for the column-definition keys (SPEC-003, A-09). Catalog metadata only; `default_value` NULL.

**SPEC-RWB-E1-043-002 Table-code check.** `recordVersion` accepts `tableCode` only when (a) it is an
active `value_code` of `LOV-REF-TABLE` returned by `ReferenceTableCodeSource` (SPI in `.api`,
implemented in P4 by `LovReferenceTableCodes` reading `lov_value` with `lov_code = 'LOV-REF-TABLE'`
and `is_active`; S7 §11 DF-REF-028/029) and (b) a column definition exists for it (SPEC-003).
Otherwise MSG-P3-027, `{check}` = "table code is not a reference table", 422, nothing written. This
refuses the 5 rule codes and HOLIDAY that PS6 seeds (GAP-04) and any code another module owns
(PARAMETER, P5 codes, data_product; GAP-08). The SPI direction avoids a P3↔P4 cycle, which
`ModulithTest.verify()` rejects (A-10).

**SPEC-RWB-E1-043-003 Column definitions and row check.** `ReferenceTableColumns` reads one
definition per table code through RWB-E1-042 `ParameterService` (S7 §13 step 2), key
`refdata.columns.<code>` (lower case, `_`→`-`), kind BUSINESS, value_type JSON (A-09; GAP-13). A
definition lists columns `{name, type ∈ STRING|INTEGER|DECIMAL|BOOLEAN|DATE|CODE, required, key}`;
the `key` columns form `row_key` (joined by `|`, max 200 chars, PS6). `ReferenceRowCheck` checks
every data row: required present, value parses to its type, unknown column refused, `row_key`
unique in the file. All failures are collected; the load is refused in full with MSG-P3-027, 422,
`{check}` naming the first failing data row (1-based, header excluded; A-11) and column, `field` =
column name, and the count of failures in `detail` (AC4: "row 12", `limit_days`). Nothing written.
Definitions cover only the 12 codes (S7 §13 step 2); their content is data loaded by RW-REFADM (S7
§13 "Configuration and reference data"), not code.

**SPEC-RWB-E1-043-004 Empty file.** A file with no data rows (header only or zero bytes) is refused
with MSG-GEN-001, `{field}` = `rows`, `field` = `rows`, 422 (S7 X7, AC10, §12). Checked before the
row check.

**SPEC-RWB-E1-043-005 Valid-from check.** `validFrom` < current business date (SPEC-017) → MSG-P3-027,
`{check}` names the valid from date, `field` = `validFrom`, 422 (S7 BR6, X3, AC6). `validFrom` =
business date is accepted (A-05; baseline CLAR-004). Missing or unparseable `validFrom` → MSG-GEN-001
`{field}` = `validFrom`, 422 (A-12).

**SPEC-RWB-E1-043-006 Content hash and idempotency.** `content_hash` = lower-case hex SHA-256 of the
canonical rows: rows sorted by `row_key`; each row as JSON with keys sorted and values normalised to
their column type; rows joined by `\n`; UTF-8 (S7 §13 step 3; canonical form A-13). Order after
checks 002–005: (1) if a version exists with the same `(table_code, valid_from, content_hash)`, return
it unchanged, write nothing, HTTP 201 with the same `ReferenceLoad` body (S7 X4, AC7; A-06);
(2) else if an APPROVED version of the table has this `valid_from`, refuse MSG-P3-027, 409 (S7 §12).

**SPEC-RWB-E1-043-007 Record version.** `recordVersion(tableCode, validFrom, authorUserId, loadId, rows)`
(signature verbatim, S7 §12) in one transaction: `version_no` = max(`version_no`) of the table + 1
(1 if none) under a lock that serialises numbering per table (A-15); insert one `reference_version`
(status VALIDATED, `row_count`, `content_hash`, `load_id`, `author_user_id`) and one `reference_row`
per data row (`row_key`, `row_data` jsonb). Returns `ReferenceVersion`. `load_id` is supplied by the
P4 handler (a new UUID per HTTP call); the response `id` is `load_id` (API4 `ReferenceLoad.id`; the
approve path uses `loadId`). A unique-key race on `(table_code, version_no)` or `(table_code,
valid_from, content_hash)` is resolved by re-reading: the idempotent case returns the existing load,
otherwise MSG-GEN-004, 409 (A-15).

**SPEC-RWB-E1-043-008 Approve.** `approve(loadId, approverUserId)` (S7 §12):
unknown `loadId` → 404 MSG-P4-003 (S7 §12); `approverUserId` null → MSG-P7-002, 409 (S7 X1);
approver = author → MSG-P7-002, 409, status stays VALIDATED, no approver written (S7 AC2);
status APPROVED → return the current body, 200, write nothing (S7 §12 idempotency; a later different
approver also gets 200 and the recorded approver is unchanged); status not VALIDATED/APPROVED →
MSG-P3-027, 409 (A-16); `validFrom` < current business date → MSG-P3-027, 409 (A-17); an APPROVED
version of the table with the same `valid_from` → MSG-P3-027, 409 (partial unique index; A-16).
Success: status APPROVED, `approver_user_id`, `approved_at` = now (Asia/Bangkok), and SPEC-010, in one
transaction; response 200 `ReferenceLoad` with status APPROVED. The approve right is enforced at the
P4 endpoint (SPEC-016), because the interface carries no role (A-08).

**SPEC-RWB-E1-043-009 Concurrent approval.** The approve update is conditional on the `version` value
read (JPA `@Version` on the standard column). The losing transaction gets MSG-GEN-004, 409, and writes
nothing (S7 X5, AC8, §13 step 4).

**SPEC-RWB-E1-043-010 Replaced version.** In the approve transaction: the APPROVED version of the same
table with the greatest `valid_from` < new `valid_from` gets `valid_to` = new `valid_from` − 1 day
(S7 BR8, AC1). If an APPROVED version with a later `valid_from` exists, the new version's `valid_to`
= that `valid_from` − 1 day (A-18). `valid_to` is descriptive; resolution uses SPEC-011 only.

**SPEC-RWB-E1-043-011 Version in force and versions.** `versionInForce(tableCode, businessDate)` = the
APPROVED version with the greatest `valid_from` ≤ `businessDate`; VALIDATED and ROLLED_BACK are never
returned (S7 BR3, §17). `rows(...)` returns `VersionedRows` (rows ordered by `row_key`, values from
`row_data`). `versions(tableCode)` returns all versions of the table, newest `version_no` first, any
status (S7 §12; used for AC1 "version 3 stays readable with its 4 rows"). `IN_FORCE` is derived, never
stored (baseline CLAR-006; A-19).

**SPEC-RWB-E1-043-012 No version in force.** `rows`/`versionInForce` throw
`NoVersionInForceException(tableCode, businessDate)` (S7 §12). The service also writes one ERROR log
line with `messageCode=MSG-P3-027`, table code and business date, and increments the Micrometer
counter `rwb.refdata.no_version_in_force` tagged `table` (S7 X6, AC9; alert route A-03). A caller
that gets the exception does not start its run (S7 BR9); the engines that must do so are built by
later stories (A-02).

**SPEC-RWB-E1-043-013 Cache.** `ReferenceRowCache` keyed by `(tableCode, businessDate)`; entry TTL =
`refdata.cache.ttl-seconds` read through `ParameterService` (E42 seed: 300, ENVIRONMENT; S7 §13), no
YAML literal. Only APPROVED results are cached; a `NoVersionInForceException` is not cached. A
successful approve evicts every entry of that table (A-20). No new cache dependency (AG §4.4).

**SPEC-RWB-E1-043-014 Version logger.** `ReferenceVersionLogger.logRead(tableCode, versionNo,
businessDate)` writes one INFO line per table read with exactly those three values (S7 BR7, AC3,
§13 step 6). The line carries no row content, no user ID and no customer identifier (S7 §17; BS-4.6).
`ReferenceDataServiceImpl.rows` calls it once per cache fill, so a caller gets one line per table per
start or expiry (baseline CLAR-007).

**SPEC-RWB-E1-043-015 P4 load endpoint.** `POST /api/recovery/v1/admin/reference-loads`,
multipart (`file` CSV or XLSX one sheet, `table`, `validFrom` ISO date) (S7 §12; API4).
Method check names capability area and right: `@PreAuthorize("@capabilityCheck.has('REFERENCE_DATA','C')")`
(CTX API conventions; BS-3.2; A-08). Right C is checked per capability area; S7 §10's "tables it owns" for RW-COE has no source (GAP-19). `ReferenceLoadFileReader` turns the file into
`List<Map<String,Object>>` with the header row as column names (CSV RFC 4180, UTF-8; XLSX first sheet;
no new dependency, A-21). Author = caller's user ID (A-07). Responses: 201 `ReferenceLoad {id, table,
validFrom, status, rows}`; 401 MSG-P4-001 (existing filter); 403 MSG-P4-002 (TC-E1-043-11:
RW-CASEOWN holds R only, PS6); 409 / 422 per SPEC-002..006; 503 when the database is unreachable
(A-22). All errors are `application/problem+json` (API4 Problem). The preserved RWB-E1-042 spec
also delivers a `table=PARAMETER` branch, approve and rollback on these paths (E42 spec "Endpoints
delivered"); that Java is not in this repository, so this story builds only the registry path, and
the controller is the single place where a later story adds the PARAMETER branch (GAP-08).

**SPEC-RWB-E1-043-016 P4 approve endpoint.** `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`,
no body. `@PreAuthorize("@capabilityCheck.has('REFERENCE_DATA','A')")`. `CapabilityCheck` reads the
`permission` rows for the caller's role authorities (PS6 tables `role`, `permission`, owned by P4);
no role literal in code (AG §3.2; AUD A-03). PS6 grants A to no role, so RW-RISK's A (S7 §10
assumption) is data loaded by RWB-E1-037; tests insert it as synthetic fixture data (A-08; GAP-14).
Responses per SPEC-008/009: 200, 401, 403, 404, 409, 503.

**SPEC-RWB-E1-043-017 Business date.** `BusinessDateSource` (internal port, P3) returns the greatest
`business_date` in `recovery.v_ace_batch_status` with `is_complete = true` (S7 §3; PS6 view; BAT4;
A-01; GAP-12). Used only by SPEC-005 and SPEC-008; read callers pass their own business date (S7 §12).
No business date found → MSG-P3-027 `{check}` = "no business date", 503 (A-01).

**SPEC-RWB-E1-043-018 Feature flag.** `rwb.p3.refdata-versions` added to `RecoveryFlags` /
`RecoveryProperties` / `application.yaml` in the existing pattern, default `false` (S7 §13; AG §3.13).
Off: both endpoints answer 404 (no handler mapped) and no bean of `ReferenceDataService` is exposed to
callers — the previous path, because no engine reads reference data today (A-23).

**SPEC-RWB-E1-043-019 Module boundary.** Only `casewf.refdata.api` types are used outside
`casewf.refdata`; P4 depends on that API only; `casewf.refdata` does not depend on P4 (SPI, SPEC-002).
`RecoveryBoundaryTest` gains a rule: no class outside `recovery.casewf.refdata` references
`ReferenceVersionEntity`, `ReferenceRowEntity` or their repositories, and no native SQL outside it
names `reference_version`/`reference_row` (S7 §13 done-when; AG §3.11). Package home follows the
RWB-TE-001 v7 map (casewf = P3, access = P4) (A-24).

**SPEC-RWB-E1-043-020 Messages.** Story messages use MSG4 text (English and Thai) by message ID with
placeholders; `ApiProblemException`/`ProblemFactory` are extended to carry a story message and `field`
(README decision 1 and 5). MSG-P3-027 uses MSG4's wording "The version in force is unchanged", not
S7 §14's "Version {version} stays in force" (GAP-05). Text is held behind one resolver seam until a
message table exists (OI-E1-042-004; GAP-06).

| ID | HTTP | `{placeholders}` | Used by |
|---|---|---|---|
| MSG-P3-027 | 422 / 409 / 503 | `table`, `check` | SPEC-002, 003, 005, 006, 008, 012, 017 |
| MSG-GEN-001 | 422 | `field` (`rows`, `validFrom`, `file`, `table`) | SPEC-004, 005, 015 |
| MSG-P7-002 | 409 | — | SPEC-008 |
| MSG-GEN-004 | 409 | — | SPEC-007, 009 |
| MSG-P4-001/002/003 | 401/403/404 | `action` for P4-002 | SPEC-015, 016, 008 (existing `ApiError`) |

**SPEC-RWB-E1-043-021 Holiday and rule exclusion.** No code path loads, stores or serves HOLIDAY or a
rule table. The holiday calendar is ACE data in `v_ace_holiday`, read by RWB-E1-028's P1 query, not by
this service (S7 BR1, §12; D35). No `rule_row`/`rule_package*` access (S7 §11; D36; AG §4.9).

**SPEC-RWB-E1-043-022 First versions in SIT.** Version 1 of each of the 12 tables is loaded through
the endpoint by RW-REFADM and approved by an A holder before SIT exit (S7 §13 done-when). This is an
operational data task with content owned by each table's story (see §"Seed ownership"), not code or
a migration seed.

**SPEC-RWB-E1-043-023 Test data.** All fixtures synthetic, story-tagged; user IDs are random UUIDs
standing for U-REF-01, U-RSK-01, U-RSK-02 (S7 §7); no real name, ID or account (RUN-BRIEF rule 7;
CTX testing §2).

## Field-level behaviour matrix

| Field (DF ID, S7 §11) | Source | Rule | Error |
|---|---|---|---|
| `table` → `table_code` (DF-REF-160) | request | In LOV-REF-TABLE and has column definition; ≤ 30 chars (PS6) | MSG-P3-027 422; missing → MSG-GEN-001 |
| `validFrom` → `valid_from` (DF-REF-163) | request | ISO date ≥ business date | MSG-P3-027 422; missing → MSG-GEN-001 |
| `file` → rows | request | ≥ 1 data row; each row passes column definition | MSG-GEN-001 / MSG-P3-027 422 |
| `version_no` (DF-REF-161) | computed | max + 1 per table | — |
| `status` (DF-REF-165) | computed | VALIDATED on write; APPROVED on approve | — |
| `author_user_id` (DF-REF-166) | caller | caller's user ID (A-07) | 401 if absent |
| `approver_user_id` (DF-REF-167) | caller | ≠ author; DB CHECK | MSG-P7-002 409 |
| `approved_at` (DF-REF-168) | clock | set on approve | — |
| `valid_to` (DF-REF-164) | computed | SPEC-010 | — |
| `row_count` (DF-REF-169) | computed | data rows written | — |
| `content_hash` (DF-REF-170) | computed | SPEC-006, char(64) | — |
| `load_id` (DF-REF-171) | P4 | new UUID per call | — |
| `reference_row.row_key` (DF-REF-183) | computed | key columns, unique per version | MSG-P3-027 |
| `reference_row.row_data` (DF-REF-184) | file | jsonb of typed values | — |

## Status-transition matrix

| From | Event | Condition | To | SPEC |
|---|---|---|---|---|
| none | load | all checks pass, no identical load | VALIDATED | 007 |
| none | load | any check fails | not written | 002–006 |
| none | load | identical load exists | unchanged (existing returned) | 006 |
| VALIDATED | approve | approver present, ≠ author, holds A, `validFrom` ≥ business date, no APPROVED twin | APPROVED | 008, 016 |
| VALIDATED | approve | author / no approver | VALIDATED | 008 |
| APPROVED | approve | any | APPROVED (200, no change) | 008 |
| APPROVED | rollback | — | ROLLED_BACK: not built here (GAP-10) | — |

No case status changes (S7 §9).

## Exceptional-case behaviour

| Case | Behaviour | HTTP / message |
|---|---|---|
| Rule code or HOLIDAY as `table` | refused | 422 MSG-P3-027 |
| Two different VALIDATED loads with the same `valid_from`; second approved | refused by partial unique index | 409 MSG-P3-027 (A-16) |
| Approve after business date passed `valid_from` | refused; author reloads | 409 MSG-P3-027 (A-17) |
| Parallel identical loads | one written, other returns it | 201 (A-15) |
| Database unavailable | no write | 503 (A-22) |
| `ParameterService` cannot give a definition or TTL | refused / not started | 422 MSG-P3-027 (definition); TTL missing fails start (A-20) |
| Flag off | endpoints absent | 404 |

## API change assessment

| Operation | API4 | Delta in this story | Notes |
|---|---|---|---|
| `POST /admin/reference-loads` | exists (x-module P4, Reference data C) | none | API4 text adds checklist fields and MSG-P3-022 (RWB-E2-041, out of scope S7 §19) and P5 codes (GAP-08); `table`/`validFrom` not `required`, no `format: date` (GAP-16) |
| `POST /admin/reference-loads/{loadId}/approve` | exists (P4, A) | none | API4 says approval "writes a decision log entry" AC-VERS; writer RWB-E1-027 is built later (GAP-07) |
| `GET /admin/lists/{listCode}` | exists (P4, R) | not built here | GAP-17 |
| `/verify`, `/rollback` | exist (U) | not built here | GAP-10, GAP-11 |

Contract tests against API4 for the two operations (CTX testing §3 "API story").

## Seed ownership (orchestrator note)

| Rows | Owner | Evidence |
|---|---|---|
| `parameter_catalog` 13 rows, `parameter_value` 28 rows (incl. `refdata.cache.ttl-seconds`) | RWB-E1-042 | E42 `V042_2__parameter_seed.sql`; E42 README |
| `parameter_catalog` 12 column-definition keys (metadata only) | RWB-E1-043 (this migration) | S7 §13 step 2; A-09 |
| `lov_value` LOV-REF-TABLE and other LOVs, `role`, `permission` | RWB-E1-001 (V0001 per PS6 header and DL10 D-RCV-28) | PS6 lines 5125–5149, permission seed |
| `reference_version` / `reference_row` | none by migration: loaded through the endpoint (S7 §13 done-when "not a migration seed" intent; `Configuration and reference data`) | PS6 seeds none; E42 seeds none |
| Content of each of the 12 tables | the table's story: DELEGATION_LIMIT RWB-E1-038 (D-RCV-34); ROLE/TEAM/QUEUE RWB-E1-019; PRODUCT_PARAMETER RWB-E1-045; DOCUMENT_TYPE RWB-E1-025; TEMPLATE RWB-E1-046 | S7 §19; story files v7 of those stories |

The merge-order map's "seed rows are reference loads (RWB-E1-043)" names the mechanism, not the
content; its exclusion of E1-043 as having no migration is stale against S7 §13 (GAP-15).

## A-06 split (flags and parameters as config literals)

| Item | This story | Stays with |
|---|---|---|
| Cache TTL | read `refdata.cache.ttl-seconds` through `ParameterService`, no YAML literal (SPEC-013) | — |
| Business values of the 12 tables | move to versioned rows (SPEC-001..011) | content: owning stories |
| Flag `rwb.p3.refdata-versions` | added in the existing config-property pattern (SPEC-018) | flag table and registry: RWB-E1-047 (BS6 order 16) |
| Other E1-042 parameters, `rwb.drools.kiebase-cache-max`, `rwb.p3.temporal/drools` | unchanged | RWB-E1-042 / RWB-E1-047 |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | N/A | S7 §15 | No screen; no frontend consumer | N/A |
| Backend | YES | REQUIRED | 80% lines, statements, branches, functions on new/changed recovery classes (BS-7.2; CTX testing §1) | SPEC-001..020 | New services, controller, checks, hasher | One test per AC1–AC10 and TC-E1-043-11; one per BR1–BR9; each exception row above; contract test per operation; migration tests: empty schema, PS6 baseline, re-run, constraint negatives, lint (CTX testing §3) — integration tests under `@Tag("recovery-it")` |

## Test scenarios

| Test | Covers | Level | Synthetic data |
|---|---|---|---|
| TC-E1-043-01 | AC1, BR2, BR3, BR8 | IT | EXPOSURE_BAND v3 (4 rows, 2026-11-30), v4 (5 rows, 2026-12-01) |
| TC-E1-043-02 | AC2, BR4 | IT + API | DELEGATION_LIMIT 24 rows; author approves |
| TC-E1-043-03 | AC3, BR7 | IT | QUEUE v7, SERVICE_LEVEL v2 via a test consumer; captured log lines contain no identifier; `v_ace_holiday` read through view only |
| TC-E1-043-04 | AC4, BR5 | IT + API | SERVICE_LEVEL, row 12 `limit_days` = "five" |
| TC-E1-043-05 | AC5, BR3, BR4 | IT | LEGAL_PERIOD v1 approved, v2 VALIDATED 2026-12-01 |
| TC-E1-043-06 | AC6, BR6 | API | LEGAL_PERIOD validFrom 2026-11-24, business date 2026-11-25 |
| TC-E1-043-07 | AC7 | IT + API | REGION same file twice |
| TC-E1-043-08 | AC8 | IT | QUEUE v8, two parallel approvals |
| TC-E1-043-09 | AC9, BR9 | IT | TEAM with no approved version |
| TC-E1-043-10 | AC10, BR5 | API | DOCUMENT_TYPE header only |
| TC-E1-043-11 | Access | API | RW-CASEOWN → 403 MSG-P4-002 |
| Extra | BR1 | API | ALLOCATION and HOLIDAY as `table` → 422 |
| Extra | SPEC-001 | IT | UPDATE of `reference_row`, DELETE of `reference_version` refused; CHECK approver ≠ author |
| Extra | SPEC-018 | Unit | flag off → endpoints absent |

TC7 TC-E1-043-03 and -05 use HOLIDAY fixtures; S7 AC3/AC5 govern (GAP-03).

## Guardrails and out of scope

Guardrails: S7 §17 applies in full (SPEC-001, 013, 014, 019, 021). Out of scope: S7 §19; rollback,
verify and list endpoints (GAP-10, 11, 17); handler dispatch for codes other modules own (GAP-08);
decision-log entry on approval (GAP-07); the permission matrix change (RWB-E1-037); engine start-up
hooks (RWB-E1-018, -020, -028; A-02).

## Clarification Log

No question is put to the user (L-RCV-03; RUN-BRIEF rule 4). Each item is answered from a source or
by a labelled assumption; the owners' confirmations go to `shared-updates.md`.

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | S7 §13; PS6 `uk_reference_row` | Row-key uniqueness: global (PS6) or per version (S7)? | AC1 cannot pass with PS6 | S7 governs (GAP-01) | RESOLVED | 001 |
| CLAR-002 | S7 BR1; PS6 LOV-REF-TABLE | Rule codes and HOLIDAY in seeded list | Could accept forbidden loads | Refuse codes with no definition (GAP-04) | RESOLVED | 002 |
| CLAR-003 | S7 §13 step 2; E42 kind CHECK | Where column definitions live | Row check source | `ParameterService` JSON per code (A-09, GAP-13) | RESOLVED_BY_ASSUMPTION | 003 |
| CLAR-004 | S7 BR6 | valid_from = business date | AC6 boundary | Accepted (A-05) | RESOLVED_BY_ASSUMPTION | 005 |
| CLAR-005 | S7 §12; OI-E1-042-011 | Repeat-load status code | Contract | 201 same body (A-06) | RESOLVED_BY_ASSUMPTION | 006 |
| CLAR-006 | S7 §3; BAT4 | Single business date from per-source view | BR6 check | Latest complete date (A-01, GAP-12) | RESOLVED_BY_ASSUMPTION | 017 |
| CLAR-007 | S7 §10; PS6 permission | Who holds A | Approve impossible in SIT | Data via RWB-E1-037; fixture in tests (A-08, GAP-14) | RESOLVED_BY_ASSUMPTION | 016 |
| CLAR-008 | S7 §9; FR-RWB-011; API4 `/rollback` | Rollback owner | ROLLED_BACK transition | Not built here (GAP-10) | RESOLVED_BY_ASSUMPTION | 011 |
| CLAR-009 | S7 AC3/AC9 §13 step 6; BS6 | Engines built later | Hook calls | Logger and exception delivered; test consumer (A-02) | RESOLVED_BY_ASSUMPTION | 012, 014 |
| CLAR-010 | S7 BR6 vs approve | Approve after valid_from passed | Retroactive version | Refuse (A-17) | RESOLVED_BY_ASSUMPTION | 008 |
| CLAR-011 | S7 §14; MSG4 | MSG-P3-027 wording | Text | MSG4 governs (GAP-05) | RESOLVED | 020 |
| CLAR-012 | E1-001/013/016/025/040/041/046 v7 | Handler SPI for other modules' codes | Later stories | Not defined in S7; recorded (GAP-08) | RESOLVED_BY_ASSUMPTION | 002 |

`CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0] [ASSUMPTIONS: 24] [GAPS: 19, BLOCKERS: 0]`

## Status reporting

MCP_STATUS_SUMMARY: Not applicable: no Figma, Jira or Confluence MCP is connected (RUN-BRIEF rule 5) and the story has no screen.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend reference-data service with two P4 endpoints already in API Specification v4; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first implementation of API4 load and approve; no OpenAPI delta]
REQUIREMENT_COVERAGE_SUMMARY: 9 business rules, 10 ACs, 7 exception paths, 1 access test and the contract are mapped; 19 source conflicts settled by precedence or labelled assumption, none unresolved.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 9] [COVERED_RULES: 9] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
