# Plan gate review, round 1: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-PLAN-001` |
| Gate | Plan gate, round 1 (Compliance Reviewer; bounded review of the plan stage) |
| Artefacts reviewed | `plan/plan.md` v1, `plan/tasks.md` v1, `plan/data-model.md` v1, `plan/assumptions.md`, `plan/document-gaps.md`, `plan/shared-updates.md`, `plan/tests/scenarios.md`, `plan/contracts/backend-apis.json` v1, `plan/contracts/frontend-integrations.json` v1, `plan/agent-run-log.md` (all 18 Nov 2026) |
| Gated spec | `specify/spec.md` revision 10; spec gate round 10 `REVIEW-RWB-E1-043-SPEC-010` `PASS` 0 Critical / 0 High / 0 Medium / 0 Low (`../review/spec-gate-review-10.md`) |
| Story | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-043-reference-data-service-with-versioned-tables-v2.md` |
| Sources checked | `AGENTS.md` sections 7 and 9; `planning-execution-gates.md`; `implementation-execution-gates.md`; `pdlc.md`; `AI-SDLC-BUILD-LOG.md` decisions D-RUN-07..22 and the RWB-E1-043 plan row; `infra/postgres/schema/03-recovery-physical-schema-v6.sql`; `api/recovery-api-v4.yaml`; Users, Roles and Permissions v4 lines 73-110; RWB-TE-001 plan v7; RWB-E1-044 plan v2; RWB-E1-042 plan v2 and spec revision 13; `aisdlc/docs/open-items.md` OPEN-050. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. One run; no question asked (L-RCV-03); only this review file written. |

## Status

**`PLAN_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 1 | Blocks the plan gate |
| Low | 7 | Remediated under D-RUN-09; not accepted |

`REVIEW_STATUS: FAIL`. The design and traceability work is substantially complete: 49/49
requirement rows, 32/32 SPEC, 10/10 AC, 9/9 BR, 7/7 X, 33/33 TC, 17/17 SEC and 20/20 CLAR are
mapped; the migration and 38 catalog rows match Physical Schema v6 and the spec; the 80% x 4
coverage gate is planned; no human approval or ratification is claimed. The Medium is an
execution-order defect in the migration test; the Lows are path, count, definition, wording and
consistency defects. None requires a design change.

## Findings

### PLAN-001 — Medium

**Title:** `ReferenceMigrationIT` compares the 38 database catalog rows to the CSV before TASK-04
writes the CSV, so TASK-02 cannot go green.

**Location:** `plan/tasks.md` TASK-01, TASK-02, TASK-03, TASK-04 and TASK-15; `plan/data-model.md`
section 7; `plan/plan.md` "Execution order".

**Evidence:**

- TASK-01 (line 33) says the migration IT checks "the 38 catalog rows equal the CSV rows".
- TASK-02 (line 34) verifies the migration with
  `./gradlew recoveryIntegrationTest --tests "*ReferenceMigrationIT"` **green**.
- TASK-03 (line 35) is red because the 38 catalog rows are absent; TASK-04 (line 36) adds the 38
  rows to `backend/src/main/resources/config/parameter-catalog.csv`. Both come after TASK-02 in
  the dependency graph.
- `plan/data-model.md` line 221 explicitly says "the migration IT compares the database rows to the
  parsed CSV".
- TASK-15 (line 47) repeats "The migration IT is green from TASK-02".

At TASK-02 the CSV holds only the 19 RWB-E1-042 rows, so the comparison cannot pass. The prescribed
red/green order is not executable as written.

**Why it matters:** TASK-02's verification is a hard green point for the one migration. A red IT
blocks the migration task; the builder would have to deviate from the plan's `BLOCKED_BY` order or
stop. The plan's "tests before code" sequence is otherwise sound; this one assertion crosses the
TASK-02/TASK-04 boundary.

**Required fix:** Move the catalog/CSV equality assertion out of `ReferenceMigrationIT` into
`ReferenceCatalogRowsTest` (TASK-03/TASK-04) or into a TASK-15 case. Keep `ReferenceMigrationIT` to
the DDL, column, constraint, trigger, re-run and 38-row count checks. Update `data-model.md` section
7 and TASK-15's "green from TASK-02" statement. Do not add the 38 CSV rows in TASK-02; the file
belongs to TASK-03/TASK-04.

### PLAN-002 — Low

**Title:** TE-001 test paths are written under the `T` recovery root, but the files live under
`th/co/scb/ace/demo`.

**Location:** `plan/plan.md` lines 46 and 219; `plan/tasks.md` TASK-00 and the pre-submit check
(names only).

**Evidence:**

- `plan/plan.md` line 113 defines `T` = `backend/src/test/java/th/co/scb/ace/demo/recovery`.
- `plan/plan.md` lines 46 and 219 name `T/testsupport/ApplicationYamlEnvironment.java`. RWB-E1-044
  plan v2 line 49 puts the helper at
  `backend/src/test/java/th/co/scb/ace/demo/testsupport/ApplicationYamlEnvironment.java`, outside
  the recovery root. `T/testsupport` would resolve to
  `backend/src/test/java/th/co/scb/ace/demo/recovery/testsupport`, which no base output creates.
- The same lines name `T/.../ModulithTest.java` and `T/.../e2e/PlatformE2ETest.java`. TE-001 plan
  v7 line 111 puts them at `backend/src/test/java/th/co/scb/ace/demo/ModulithTest.java` and
  `backend/src/test/java/th/co/scb/ace/demo/e2e/PlatformE2ETest.java`, also outside the recovery
  root.

**Why it matters:** The plan's own exact-path rule is breached; TASK-00's missing-home check could
stop on a file that is correct in the base; the "Files explicitly not changed" list names a path
that does not exist.

**Required fix:** Use the full path for every non-recovery test file. Correct
`ApplicationYamlEnvironment`, `ModulithTest` and `PlatformE2ETest` in `plan.md` lines 46 and 219 and
in any task that cites them. The RWB-TE-001 v7 text itself uses the `T/testsupport` shorthand, so
the plan should state the base's exact path rather than copy the shorthand.

### PLAN-003 — Low

**Title:** The data model fixes RWB-E1-001's migration number as `V0001`, contrary to D-RUN-07.

**Location:** `plan/data-model.md` section 11, `lov_value` row (line 298).

**Evidence:** "`lov_value` LOV-REF-TABLE | RWB-E1-001 (V0001) | PS6; GAP-32; D-RUN-08". D-RUN-07
says: "No spec or plan fixes a migration number. `<seq>` is the next free four-digit number in
`develop-recovery` at merge ... The numbers in the cards (E1-001 `V0001`, E1-042 `V0042`) and in the
squad migration merge-order map are recorded as document gaps." The plan's own `plan.md` line 7 says
"no number is fixed for the migration (D-RUN-07)"; line 223 says "**No number is fixed**".

**Why it matters:** The plan applies D-RUN-07 to its own migration but fixes another story's number
in the seed-ownership table. RWB-E1-001 is a later story (Build Sequence order 9); its migration
number is assigned at merge, not `V0001`.

**Required fix:** Replace "RWB-E1-001 (V0001)" with "RWB-E1-001's own migration; `<seq>` assigned at
merge" or "the PS6 local load; GAP-32", and keep the placeholder rule everywhere.

### PLAN-004 — Low

**Title:** `PRE-1`..`PRE-4` are cited as stop conditions but are never defined.

**Location:** `plan/plan.md` lines 24, 38, 57 and 236; `plan/tasks.md` TASK-00 (line 32) and the
pre-submit check (line 94); `plan/shared-updates.md` R23.

**Evidence:** "The plan stops if any is absent (PRE-1..PRE-3)" (`plan.md` line 38); "A missing home
is a stop-and-report (PRE-1..PRE-3)" (TASK-00); "PRE-2" (`plan.md` lines 57 and 236; `shared-updates.md`
R23); "PRE-1..PRE-4" (TASK-00 Trace). No table, assumption or section defines PRE-1..PRE-4.

**Why it matters:** A stop condition that cannot be looked up is not a check; the builder cannot
record which precondition failed; the plan gate's "no dangling references" check fails.

**Required fix:** Add a "Preconditions" table defining PRE-1 (TE-001 merged), PRE-2 (E1-044's
identifier-only, quote-aware migration lint merged), PRE-3 (E1-042 merged) and PRE-4 (the coverage
or migration-runner baseline check), with the file or test that proves each; or remove the labels
and state the conditions in prose.

### PLAN-005 — Low

**Title:** The plan's provenance line says "40 test IDs"; the spec has 33 TC IDs and the plan's own
scenario file has 49 T-IDs.

**Location:** `plan/plan.md` line 49; `plan/agent-run-log.md` line 12.

**Evidence:** `plan/plan.md` line 49: "the 32 SPEC rows, 49 requirement rows, **40 test IDs**,
SEC-01..17, CLAR-001..020". The spec's "Test scenarios" table lists TC-E1-043-01..11 (11),
TC-RB-01/-02 (2), TC-HD-01..05 (5), TC-PB-01/-02 (2), TC-FL-01 (1), TC-MG-01 (1), TC-BR1 (1),
TC-TM-01..05 (5), TC-RP-01 (1), TC-FD-01 (1), TC-DR-01 (1), TC-BD-01 (1) and TC-CAT-01 (1): 33 TC
IDs, plus SEC-01..17. `plan/tests/scenarios.md` has T-E1-043-01..49 (49) plus SEC-01..17.
`plan/agent-run-log.md` line 81 says "49 test IDs".

**Why it matters:** A stale count in the plan's input provenance weakens the traceability check; the
spec gate rounds treated citation and count defects as findings.

**Required fix:** State "33 TC IDs + SEC-01..17" or "49 plan T-IDs + SEC-01..17" consistently in
`plan.md` and `agent-run-log.md`.

### PLAN-006 — Low

**Title:** The handler-defect test asserts 500 but not the `traceId` that SPEC-025 requires; the gap
is recorded but the spec requirement is not tested.

**Location:** `plan/tasks.md` TASK-15 (`#rowKeyAndHandlerDefect`),
`plan/contracts/backend-apis.json` `problemBody`, `plan/document-gaps.md` PG-E1-043-03.

**Evidence:** SPEC-025 says "Any other exception from `validate` is a defect -> 500 with `traceId`,
nothing written". The plan's `problemBody` says "The 500 is the existing
`ApiExceptionHandler.unexpected` body and carries no traceId (PG-E1-043-03)"; TASK-15 says the test
asserts "500 and nothing written", not `traceId`. The spec's own TC-HD-05 says "500, nothing
written" and does not assert `traceId`; the spec's "Impacted Existing Nodes" puts
`ApiExceptionHandler` and `ProblemFactory` out of scope.

**Why it matters:** A gated spec sentence is untested; the plan resolves it by a gap, not a spec
correction. The plan's recorded reason is sound, but the test is weaker than the spec text and the
deviation should not be silent.

**Required fix:** Assert the 500 body and explicitly record that `traceId` is absent (the current
`ApiExceptionHandler` body), or add the `traceId` field in a separately scoped change; keep
PG-E1-043-03 and R18 open. Do not describe the test as fully covering SPEC-025 without that note.

### PLAN-007 — Low

**Title:** The migration statement-group list is inconsistent: `plan.md` adds a drop of
`uk_reference_version_from_hash` that `data-model.md` and TASK-02 omit.

**Location:** `plan/plan.md` "Migration" group 3 (line 229); `plan/data-model.md` section 1 group 3
(line 30); `plan/tasks.md` TASK-02 (line 34).

**Evidence:** `plan.md` says "`ALTER TABLE ${recoverySchema}.reference_row DROP CONSTRAINT IF EXISTS
uk_reference_row` and `ALTER TABLE ${recoverySchema}.reference_version DROP CONSTRAINT IF EXISTS
uk_reference_version_from_hash` (the second is a no-op unless a partial run left it)".
`data-model.md` and TASK-02 list only the `uk_reference_row` drop, then the `DO` block adds
`uk_reference_version_from_hash`. The spec's SPEC-001 requires only the `uk_reference_row` drop; it
does not require the second.

**Why it matters:** The builder has three different statement-group descriptions for the one
migration; the extra drop is harmless on PS6, but a partial-run guard should be stated once, in the
detailed model.

**Required fix:** Add the second drop to `data-model.md` section 1 and TASK-02, or remove it from
`plan.md`; keep the eight statement groups identical in all three files.

### PLAN-008 — Low

**Title:** TASK-19's scope sentence allows a diff to touch "Files explicitly not changed".

**Location:** `plan/tasks.md` TASK-19 (line 51).

**Evidence:** "The diff touches only the files of `plan.md` 'Files added or changed' **and** 'Files
explicitly not changed'". The second list is the set that must not change
(`backend/build.gradle.kts`, `api/**`, `frontend/**`, `infra/**`, merged TE-001 and E1-042 files,
etc.).

**Why it matters:** A scope check written this way can pass while a file that must not change has
changed; the plan's own scope guard is weakened.

**Required fix:** Reword: "The diff touches only the files of 'Files added or changed' and leaves
every file of 'Files explicitly not changed' untouched."

## Coverage table

| Set | Required | Mapped | Missing | Evidence |
|---|---:|---:|---:|---|
| Requirement rows | 49 | 49 | 0 | `plan.md` lines 301-349 against `spec.md` lines 117-165; all `COVERED`, none `BLOCKED` |
| SPEC | 32 | 32 | 0 | `plan.md` "SPEC to task map"; SPEC-001..032 |
| AC | 10 | 10 | 0 | `tests/scenarios.md` section 2 |
| BR | 9 | 9 | 0 | `tests/scenarios.md` section 3 |
| X | 7 | 7 | 0 | `tests/scenarios.md` section 4 |
| TC | 33 | 33 | 0 | Spec "Test scenarios"; `tests/scenarios.md` sections 1 and 5 |
| SEC | 17 | 17 | 0 | `tests/scenarios.md` sections 1 and 5 |
| CLAR | 20 | 20 | 0 | `tests/scenarios.md` section 6 |
| 49/49 requirement logic | 49 | 49 | 0 | Plan table lines 301-349; 0 `BLOCKED`; plan line 351 |

The 16 requirement lines owned by other stories are listed as seams and are not counted. The 40
source contradictions remain settled in the spec; the plan introduces none. No orphan SPEC remains:
every SPEC-001..032 has at least one task and a named test.

## Gated-spec checks

| Check | Result |
|---|---|
| One migration | `V<seq>__rwb_e1_043_reference_versions.sql`; line 1 `-- Story: RWB-E1-043`; `<seq>` at merge; one file; forward only. Pass, with PLAN-003 (the `V0001` reference) and PLAN-007 (the extra drop). |
| `reference_version` | 29 columns, types, widths, nullability and defaults match Physical Schema v6 lines 1437-1468; `uk_reference_version`; the new uniqueness, CHECK, partial index, `load_id` index and append-only trigger are specified. Pass. |
| `reference_row` | 11 columns match Physical Schema v6 lines 1471-1484; `uk_reference_row` dropped; `uk_reference_row_version (version_id, row_key)` added; `fk_reference_row_version_id` and `ix_reference_row_version_id` kept. Pass. |
| 38 catalog rows | 12 `refdata.columns.<code>` (STRING, `none`, RW-REFADM) + 13 `rwb.refload.loader.<code>` + 13 `rwb.refload.approver.<code>`; CODE_LIST, required=false, owners/defaults as SPEC-029; 38 = 12 + 13 + 13; no `parameter_value` row. Pass. |
| 37 grant rows | One per RW- role for `Reference data`; matrix letters plus the six A roles of A-08; no `Rules and parameters` row changed. Pass. |
| 80% x 4 coverage | `recoveryCoverageVerification`: one `BUNDLE`, `LINE`, `INSTRUCTION`, `BRANCH`, `METHOD` each 0.80; native `recoveryCoverageReport.xml`/HTML; no exclusion or lowered threshold; frontend `NOT_APPLICABLE` with evidence. Pass. |
| No fixed number | The story's migration is placeholder-only; the only fixed number is the RWB-E1-001 `V0001` reference in `data-model.md` (PLAN-003). |
| Security and authority | Three operations with `@PreAuthorize` naming `referenceLoadAuthority`, area `Reference data` and C/A/U; per-table lists through `ParameterService`; 401/403/404; `MSG-P4-002` action text; SEC-01..17. Pass. |
| Personal data | `author_user_id`, `approver_user_id`, `created_by`, `updated_by` treated as staff identifiers; never logged, never in the response or audit; synthetic UUIDs only. Pass. |
| Audit | `REFERENCE_LOAD_AUDIT` for load, approve and rollback, DONE and REFUSED; `DECISION_RECORDED` AC-VERS; no user ID, row content or reason. Pass. |
| Frontend | `NOT_APPLICABLE` with UI In Scope NO, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0]`, no `plan/frontend/components.md`, no `frontend/` change. Pass. |
| No human approval | No ratification, approval or acceptance of D-RUN-18..21; OPEN-050 and the 15 owner-acceptance items stay open. Pass. |

## D-RUN decisions

| Decision | Evidence in the plan | Verdict |
|---|---|---|
| D-RUN-07 | One file, `V<seq>__rwb_e1_043_reference_versions.sql`; line 1; no fixed number; `data-model.md` `V0001` reference | Pass with PLAN-003 |
| D-RUN-08 | Later-story work named as seams: `/verify`, `/admin/lists`, table contents, `sys_fields`, QUEUE/QUEUE_MEMBER, business date, decision log, access log, permission matrix, actor, screens, rule packages, change checklist, data quality, message table | Pass |
| D-RUN-10/D-RUN-11 | E1-043 owns the shared endpoint and dispatches by table code; E1-042 publishes the parameter-load interface; the handler registry is in P3 and E1-001 registers `data_product` | Pass |
| D-RUN-17 | TE-001 v7 layout: P3 `casewf`/`config.api`/`refdata.api`, P4 `access.api`/`access.internal`; merge order TE-001, E1-044, E1-042; the `ApplicationYamlEnvironment` path is the exception | Pass with PLAN-002 |
| D-RUN-18/D-RUN-19/D-RUN-20 | Handler SPI in P4 `access.api`; `CatalogParameterReader` published by E1-042 and implemented in P3; `PARAMETER` is a dispatcher branch, not an SPI handler; no P1 -> P3 edge | Pass |
| D-RUN-21 | One ACE module (recovery); P3 `casewf.refdata` plus additive P4 `access`; no common or collection change; not ratified; OPEN-050 | Pass |
| D-RUN-09 | 1 Medium + 7 Low; the Medium blocks; the Lows are remediated, not accepted | Fail, remediate |

## Recorded gaps

- `PG-E1-043-01` (additive `ReferenceVersion.rollbackReason`): accepted; SPEC-011 requires
  `rollback_reason`, the section 12 record has 11 components, and the 12th is appended without
  reordering.
- `PG-E1-043-02` (unknown code passes the table right): accepted; SPEC-002/TC-BR1 need 422 for a
  rule code or HOLIDAY while SPEC-025 L4 and SEC-06 need 403 for a known code; the authority only
  decides the table right.
- `PG-E1-043-03` (500 `traceId`): **not accepted as written**; see PLAN-006. The gap stays in
  `document-gaps.md` and R18.
- `PG-E1-043-04` (plan-written descriptions): accepted; `description` is documentation only and no
  rule reads it.
- `PG-E1-043-05` (`table_code` case/matching): accepted; exact matching is the safe default and no
  rule changes.
- `PG-E1-043-06` (`CatalogCompletenessRules` and `byName`): accepted as a stop-and-report; TASK-00
  re-reads the merged rule.
- `GAP-59`/OPEN-050: unresolved and unratified; not closed by this plan or this review.

## Gate decision

The plan is substantially complete and well traced. The one Medium is an execution-order defect in
the migration IT; the seven Lows are path, count, definition, wording and consistency defects. Under
D-RUN-09 the seven Lows are remediated, not accepted; the Medium blocks.

`RATIFICATION_CLAIMS: none`. OPEN-050 remains open (owner: recovery tech lead); the 15
owner-acceptance items remain open; no human approval is claimed.

PLAN_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 7]
