# Plan gate review round 1: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-PLAN-001` |
| Gate | Plan gate, round 1 |
| Story | RWB-E1-042 Central configuration service and parameter catalog (EPIC-001, P3/P4 recovery) |
| Artifacts under review | `plan/plan.md` v1, `plan/tasks.md` v1, `plan/data-model.md` v1, `plan/contracts/backend-apis.json`, `plan/contracts/frontend-integrations.json`, `plan/tests/scenarios.md`, `plan/assumptions.md` (PA-E1-042-01 to -17), `plan/document-gaps.md` (PG-E1042-01/02 and carried rows), `plan/shared-updates.md`, `plan/agent-run-log.md` |
| Compared with | Approved `specify/spec.md` revision 13 (1302 lines, file 2026-11-18 06:01:50); spec gate review 12 `REVIEW-RWB-E1-042-SPEC-014` `PASS` 0/0/0/0 (`review/spec-gate-review-12.md`); story v7 RWB-E1-042 §1-§19; Physical Schema v6 lines 1386-1434; the 10 Nov pack CSV and SQL under `_v2-baseline/implement/`; API Specification v4; Users, Roles and Permissions v4; Error and Message Standard v4; Personal Data Inventory v4; RWB-TE-001 plan v7; RWB-E1-044 plan v1; `AI-SDLC-BUILD-LOG.md` decisions D-RUN-07 to D-RUN-22 |
| Rules | `compliance-reviewer.md`; `.github/rules/planning-execution-gates.md`; `pdlc.md`; `traceability-standards.md`; `security-quality-standards.md`; `implementation-execution-gates.md`; `AGENTS.md` §7 and §9; `RUN-BRIEF.md` |
| Repository | Read only. This review file is the only file written; no shared file, build log, plan file or code was edited. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | None. This is the first plan gate for this run. |

## Status

**FAIL** — 1 High, 1 Medium and 9 Low findings.

The plan is structurally strong: 27 SPEC rows, 57 requirement-logic rows and 46 test
cases are mapped; one migration is named with a merge-time `<seq>`; the 19 catalog rows and 40
value rows are enumerated; the coverage gate is four JaCoCo counters at 0.80; both contract
JSON files parse; and no human approval is claimed. However, the data model does not follow
the approved Physical Schema v6, and the plan's catalog-description gap is false. The High and
Medium findings block the handoff; the Lows require remediation under D-RUN-09.

## 1. Findings

| ID | Severity | Finding | Evidence | Required fix | Trace | Status |
|---|---|---|---|---|---|---|
| PLAN-001 | **High** | The plan's `data-model.md` table shapes do not follow Physical Schema v6, although its own §1 says the migration uses the columns "exactly as Physical Schema v6" and `plan.md` adopts `data-model.md` §4 for the DDL. `parameter_catalog` omits `is_active` and `state`; its `description` loses `NOT NULL`; `version` is `bigint NOT NULL DEFAULT 0` instead of `integer NOT NULL DEFAULT 1`; `environments` and `used_by` are made `NOT NULL` where v6 allows null; and `kind`, `value_type`, `scope`, `owner_role`, `min_value`, `max_value`, `environments` widths differ. `parameter_value.version` is also `bigint DEFAULT 0` instead of `integer NOT NULL DEFAULT 1`, and `environment`, `product_group` and `status` widths differ. TC-13 asserts tables, constraints and indexes but not every v6 column, and TC-14 on a v6 schema would pass because `CREATE TABLE IF NOT EXISTS` does nothing. | `plan/data-model.md` §4.1 lines 99-121 and §4.2 lines 123-148; `plan/plan.md` line 236; `specify/spec.md` SPEC-002 line 166 and §12.3 lines 665-666; Physical Schema v6 lines 1386-1434; the 10 Nov pack SQL `_v2-baseline/implement/sql/V0042__rwb_e1_042_parameter_catalog_and_seed.sql` lines 19-80; `plan/agent-run-log.md` line 24 records that the planner did not read the v6 DDL or the pack SQL | Copy the exact v6 column definitions for both tables into §4.1 and §4.2, including `is_active`, `state`, `description NOT NULL`, `environments`/`used_by` nullability, `version integer NOT NULL DEFAULT 1` and the exact widths. Add a TC-13 assertion for every v6 column and its nullability. Re-read Physical Schema v6 lines 1386-1434 and the pack SQL, and record the read. | SPEC-001, SPEC-002, TASK-14, TASK-15 | Open |
| PLAN-002 | **Medium** | `PG-E1042-01` and `PA-E1-042-06` state that no source gives catalog-description text for any of the 19 rows, so the plan authors one line per row. That is false for the first 13 rows: the 10 Nov pack CSV has a `description` column with text for every one of its 13 rows, and the pack SQL seeds the same text. The gap should cover only the six D-RCV-36 rows, which have no pack text. | `plan/document-gaps.md` line 15 (PG-E1042-01); `plan/assumptions.md` line 12 (PA-E1-042-06); `plan/data-model.md` line 65; `plan/shared-updates.md` line 25; `_v2-baseline/implement/config/parameter-catalog.csv` header and rows (for example `case.entry.dpd` → "Days past due at which an account enters recovery (DL16)."); pack SQL lines 349 onward; `plan/agent-run-log.md` line 24 records that the pack CSV and SQL were not read | Use the 13 pack descriptions in `data-model.md` §2 and TASK-03. Narrow PG-E1042-01, PA-E1-042-06 and the `shared-updates.md` row to the six D-RCV-36 rows, and record the pack CSV/SQL as the source. | SPEC-003, SPEC-005, TASK-03 | Open |
| PLAN-003 | Low | The load-check cross-references point to `data-model.md` §7, which is the message catalogue; the twelve checks are §5.2. | `plan/plan.md` line 242; `plan/tasks.md` TASK-18 line 52; `plan/data-model.md` §5.2 line 189 and §7 line 227 | Change both references to `data-model.md` §5.2 (or `spec.md` §12.5). | SPEC-012, TASK-18, TASK-19 | Open |
| PLAN-004 | Low | TASK-16 says "each of the twelve type conversions of §12.2"; the spec defines ten value types. | `plan/tasks.md` line 50; `specify/spec.md` §7.1 line 265 and §12.2 lines 656-658 list STRING, INTEGER, DECIMAL, BOOLEAN, DATE, TIME, DURATION, CODE, CODE_LIST and JSON | Say ten, or enumerate the ten types. | SPEC-007, TASK-16 | Open |
| PLAN-005 | Low | The release section says "RWB-E1-044 then RWB-TE-001 merge first", contrary to D-RUN-17, which puts TE-001 before E1-044. | `plan/plan.md` line 447; `AI-SDLC-BUILD-LOG.md` D-RUN-17; `plan/plan.md` lines 19 and 23 already require the TE-001 merge before the Builder starts | State "RWB-TE-001 then RWB-E1-044 merge first", or simply "both merge before this story; TE-001 first". | D-RUN-17, SPEC-001, TASK-00, TASK-15 | Open |
| PLAN-006 | Low | The file-scope statements omit test resources and TE-001 test edits that the plan itself lists. The one-module "Non-Java files touched" row omits `backend/src/test/resources/architecture/recovery-modules.yaml`, `backend/src/test/resources/architecture/magic-number-baseline.csv` and the fixture corpus. TASK-25 says the shared file edited is `backend/build.gradle.kts` only, and the pre-submit check says "the two YAML files, the two CSV resources and the migration are the only other non-Java files"; both omit the test YAML, baseline CSV, fixtures and the edits to `RecoveryBoundaryTest` and `ApiExceptionHandlerTest`. | `plan/plan.md` line 89; `plan/tasks.md` TASK-25 line 59 and pre-submit line 106; `plan/plan.md` test-file table lines 174-177 and 185 | List every file from the file tables, with a separate main/test/shared classification, and update TASK-25 and the pre-submit check accordingly. | TASK-25, PRE-7 | Open |
| PLAN-007 | Low | The contract JSON contains an invalid SPEC reference: `(SPEC-007, —24)`. There is no `—24` SPEC ID; the intended reference is SPEC-024 (ENV value source). | `plan/contracts/backend-apis.json` line 62 | Change to `SPEC-007, SPEC-024`. | SPEC-007, SPEC-024, CON1 | Open |
| PLAN-008 | Low | TASK-25 ends with the undefined reference `[IEG]`; no path legend or rule defines it. | `plan/tasks.md` line 59; no other occurrence or definition in the plan files | Replace it with `implementation-execution-gates.md`, or define the abbreviation in the path legend. | TASK-25 | Open |
| PLAN-009 | Low | The Migrations section says "The folder is empty today", but the folder holds `README.md`; the plan's own Code base row and the run log say so. | `plan/plan.md` line 309 versus line 21; `plan/agent-run-log.md` line 36 | Say "holds `README.md` and no `.sql` file". | SPEC-001, TASK-15 | Open |
| PLAN-010 | Low | The unit test plan does not name a case for `ParameterService.entry(String)` or for the product-group `get(ParameterKey, String, LocalDate)` overload, though both are part of the published interface and the METHOD counter must cover them. | `plan/plan.md` line 106; `plan/data-model.md` §3 and §6; `plan/tasks.md` TASK-16 line 50; `specify/spec.md` §7.5 and §12.2 | Add explicit `ParameterServiceTest` cases: `entry` returns the catalog view; the product-group overload resolves the product row first, then the GLOBAL row; a PRODUCT scope key throws. State where TC-31 covers the controller path. | SPEC-007, TASK-16 | Open |
| PLAN-011 | Low | "No value row exists for ... an ENV key" is ambiguous and false if read as kind `ENVIRONMENT`: four ENVIRONMENT-kind keys with `value_source=TABLE` are seeded (`refdata.cache.ttl-seconds`, `config.cache.ttl-seconds`, `temporal.taskqueue.platform`, `temporal.retention.days`). | `plan/data-model.md` line 181; §2 rows 2, 3, 16 and 17 | Say "a `value_source=ENV` key". | SPEC-006, TASK-15 | Open |

## 2. Coverage table

| Check | Coverage | Result |
|---|---|---|
| SPEC-001 to SPEC-027 | 27 of 27 mapped to TASK-00..TASK-25; no orphan | **PASS** |
| Requirement-to-SPEC logic rows | 57 of 57 `COVERED`; 0 `BLOCKED`; 0 dropped, merged or weakened | **PASS** |
| AC, BR, exception, flow, precondition, transition, authority, contract, message and guardrail rows | AC1..AC11, BR1..BR7, X1..X10, FL1..FL10, PRE1..PRE5, ST1..ST3, AUTH, CON1..CON5, MSG and GR1..GR4 all mapped to tasks and named tests | **PASS** |
| Test cases TC-E1-042-01 to TC-E1-042-46 | 46 of 46 mapped, one per spec TC; TC-E1-042-12 is `Blocked` with its exit criterion (`OI-E1-042-001`) and is not counted as passed | **PASS** (TC-12 blocked) |
| Clarification rows | 28 of 28 accounted: 25 `OPEN` with a labelled default each, `CLAR-020` `RESOLVED`, `CLAR-025` and `CLAR-027` `SETTLED` by unratified D-RUN-21 and D-RUN-20, `CLAR-028` not decided; spec gate 12 records `BLOCKING: 0` | **PASS** with upstream exception (see §6) |
| Scope bullets S-1 to S-13 | 13 of 13 mapped | **PASS** |
| Tasks TASK-00 to TASK-25 | 26 of 26; every row has Description, Files, Trace, `BLOCKED_BY` and Verification | **PASS** |
| File paths | Main, test and resource paths are exact; every `[TE-001]` path exists in TE-001 plan v7; the `[E1-044]` lint dependency is recorded | **PASS** for paths; PLAN-006 for the summary statements |
| Migration | One file `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, line 1 `-- Story: RWB-E1-042`, `${recoverySchema}` only, no `SET search_path`, no `GRANT`/`REVOKE`, forward only, no fixed number | **PASS** for form; PLAN-001 for table shape |
| Seed rows | 19 catalog rows and 40 value rows; version 1, `APPROVED`, `valid_from` 2026-11-02, seed identity `00000000-0000-0000-0000-0000000e1042`, approver NULL, `load_id` NULL, all four environments | **PASS** for rows; PLAN-002 for description source |
| Coverage gate | One `BUNDLE` rule with `LINE`, `INSTRUCTION`, `BRANCH` and `METHOD` each at 0.80; `test` execution data only; outside `check`; `architecture.parameters` added to both JaCoCo tasks; no new task, rule, counter or threshold | **PASS** |
| Contracts | `backend-apis.json` and `frontend-integrations.json` both parse; the endpoint has 16 `Parameter` fields; the three load operations are interface-only; frontend is `NOT_APPLICABLE` with evidence | **PASS**; PLAN-007 for the reference typo |
| Human approval | No plan/spec approval or D-RUN ratification is claimed; OPEN-016 is not triggered; OPEN-050 remains unratified | **PASS** |
| Document set | Story v7 §1-§19, Physical Schema v6, the 10 Nov pack CSV/SQL, API v4, S-07, S-08 and S-28 checked against the plan | **FAIL** — PLAN-001, PLAN-002; `agent-run-log.md` line 24 records the story file, pack CSV/SQL and v6 DDL were not read |

## 3. Plan-execution gate checks

| Gate | Result | Evidence |
|---|---|---|
| Upstream spec ready | **PASS** | Spec revision 13 `SUCCESS_WITH_ASSUMPTIONS`; spec gate 12 `PASS` 0/0/0/0; `REQUIREMENT_COVERAGE_RESULT` 57/57, `MISSING_RULES: 0`, `CONTRADICTIONS: 0` |
| Clarification readiness | **PASS with upstream exception** | 25 `OPEN` rows with labelled defaults; spec gate 12 `BLOCKING: 0`; no question asked; see §6 |
| Every SPEC in scope mapped | **PASS** | `plan.md` "SPEC to task map" 001..027; no orphan |
| Every FR/NFR covered | **PASS** | All SPEC rows trace to `FR-RWB-010`; no separate NFR row in the spec; `shared-updates.md` carries the FR trace |
| Every scope bullet mapped | **PASS** | `plan.md` S-1..S-13; `tasks.md` "Scope bullet to task map" |
| Effective-screen coverage | **PASS (N/A)** | UI In Scope NO; `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SCREENS: 0]`; `SCR-39` is Epic 8 |
| Task table schema, `BLOCKED_BY`, verification | **PASS** | 26 tasks; six columns; explicit `NONE` only for TASK-00; verification commands and evidence paths |
| Requirement Logic To Task Coverage structure | **PASS** | `REQ_REF`, Mapped SPEC, Mapped TASK, Coverage Type, Verification, Status; 57 rows; no `BLOCKED` row |
| Security, privacy and compliance tasks | **PASS** | TASK-11, -13, -17, -19, -25; method check, maker-checker, secrets, personal data, audit |
| API impact tasks | **PASS** | `NEW_API_REQUIRED`; TASK-17 and TASK-20; no OpenAPI change |
| Frontend/backend applicability and 80% gate | **PASS** | Frontend `NOT_APPLICABLE` with evidence; backend `REQUIRED`; four counters at 0.80; no integration substitute |
| `## Pre-submit checks` answered | **PASS** | `tasks.md` lines 96-111; every check ticked |
| No placeholder screen/node IDs | **PASS** | No `DUMMY-*`, `TBD` or `TBA` in the plan files |
| No dangling references | **FAIL (Lows)** | PLAN-003, PLAN-007 and PLAN-008; plus the PLAN-001/PLAN-002 document-set defects |
| Document-set reads recorded | **FAIL** | `agent-run-log.md` line 24 says the story file v7, the 10 Nov pack CSV/SQL and the Physical Schema v6 DDL were not read; PLAN-001 and PLAN-002 are the consequences |

## 4. D-RUN compliance

| Decision | Check | Result |
|---|---|---|
| D-RUN-07 | No fixed migration number; `<seq>` assigned at merge; line 1 story key; one file; forward only | **PASS** — `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, no number in any plan artefact |
| D-RUN-08 | Later-story work is a seam; only E1-044 and TE-001 are earlier stories | **PASS** — E1-043, E1-039, E1-045, E1-047, E2-041, E1-008/027, TE-006, E1-037/022 and E1-071/072 are named seams; no later-story file is built |
| D-RUN-10 | E1-043 owns the reference-load endpoint; E1-042 publishes `ParameterLoadHandler` | **PASS** — no controller for the three load operations; interface in `casewf.config.api`; rights, multipart and success status are E1-043's |
| D-RUN-11 | E1-043 publishes the handler registry; no `PARAMETER` SPI bean here | **PASS** — `ParameterLoadHandlerImpl` implements no `access.api` type; TC-22 checks the absence |
| D-RUN-17 | TE-001 v7 paths and merge order | **PASS** for paths and the Builder's base; PLAN-005 for the one wording slip in the release section |
| D-RUN-18 | Reference-load handler SPI published by P4 `access.api`; no P1 to P3 edge; P3 to P1 business-date read allowed | **PASS** — `CatalogParameterReader` is P4; `ParameterLoadHandlerImpl` is not an SPI; the business-date seam cites D-RUN-18 |
| D-RUN-19 | P1, P2 and P4 read parameters only through `access.api.CatalogParameterReader`, implemented in P3 | **PASS** — interface P4, implementation `casewf.config`, always registered; P3 callers keep `casewf.config.api` |
| D-RUN-20 | `PARAMETER` is a dispatcher branch of E1-043's registry, not a P4 SPI handler | **PASS** — no `PARAMETER` SPI bean; `ObjectProvider` and 404 MSG-P4-003 recorded as E1-043's contract |
| D-RUN-21 | "One module" means the ACE module, recovery; P3 and P4 are both recovery; OPEN-050 unratified | **PASS** — one-module check cites D-RUN-21 and OPEN-050; no analyst or tech-lead approval claimed |
| D-RUN-09 | Critical, High and Medium block; Lows are remediated, not accepted | **APPLIED** — this review's Lows are for remediation and re-gate, not acceptance; no finding is downgraded |

## 5. Contract and approval checks

- `plan/contracts/backend-apis.json` parses with PowerShell `ConvertFrom-Json` (18 Nov 2026) and
  records the one endpoint, the 16 `Parameter` fields, ten internal contracts, the problem
  mapping, cross-layer dependencies and an empty `newDependencies`. One invalid reference is
  PLAN-007.
- `plan/contracts/frontend-integrations.json` parses and records `NOT_APPLICABLE` with the
  evidence: UI In Scope NO, no screen, no OpenAPI change, no `frontend/src/api/schema.d.ts`
  regeneration and no file under `frontend/`.
- No human approval is claimed. `plan.md` line 449, `shared-updates.md` line 56, `tasks.md`
  line 111 and `assumptions.md` PA-16 say so. OPEN-050 remains unratified; OPEN-016 is not
  triggered. The sentence in `data-model.md` line 175 that the seed baseline is "approved by
  the reviewed catalog PR" is the spec's A-05 assumption, not an approval of this plan.
- The plan raises no new open item; `shared-updates.md` records the requests the orchestrator
  must apply and the `OPEN-050` note.

## 6. Clarification-gate note

`planning-execution-gates.md` says an `OPEN` `CLAR-*` item blocks planning, while the plan
records `PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 25]`. The spec gate review 12 passed
with `OPEN_ITEMS: 25` and `BLOCKING: 0`; the spec's status is `OPEN_ITEMS_RECORDED`, and
RUN-BRIEF rule 4, L-RCV-03 and `AGENTS.md` §10.6 forbid a question in an automated stage. The
plan applies the labelled defaults, cites each where it changes a file, and treats none as
`RESOLVED`. This review treats the upstream gate's disposition as binding and does not raise a
finding for the 25 rows; it records that no human approval is claimed and that a strict reading
of `planning-execution-gates.md` would block. That exception is visible here, not suppressed.

## 7. Document-gap consequence

`PG-E1042-01` is corrected by PLAN-002: the gap narrows to the six D-RCV-36 rows, and the
fix uses the 13 pack descriptions. `PG-E1042-02` (`repeat` has no API field) is accurate and carried. No
other new document gap is raised by this review.

## 8. Conclusion

The plan gate **fails**. The plan is well structured and externally traceable, but its data
model contradicts the approved Physical Schema v6 (PLAN-001) and its catalog-description gap
is false (PLAN-002). Both block the handoff. The nine Lows are cross-reference, count, file-scope
and clarity defects; under D-RUN-09 they are remediated, not accepted. The planner must fix
PLAN-001 to PLAN-011, update the affected plan artifacts, and submit a round-2 plan gate. No
implementation, code, test or later stage starts until the re-gate passes.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 1] [LOW: 9]
