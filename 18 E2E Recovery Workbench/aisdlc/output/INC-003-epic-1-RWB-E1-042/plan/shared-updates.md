# Shared updates requested: RWB-E1-042 plan, revision 2

RUN_ID `INC-003-epic-1-RWB-E1-042`, stage `plan`, 2026-11-18, run 2. Revision 2 narrows the `PG-E1042-01` row and the catalog-owner request; no other row changed. This stage did not edit any shared file (RUN-BRIEF rule 3). The orchestrator applies these rows in order and assigns IDs where needed. The spec stage's `specify/shared-updates.md` (revision 13) is applied separately and is not repeated here; its rows 1-40 and §2-§6 stand.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

| Change | Row |
|---|---|
| Story row 003 (line 51), status column | Replace the spec-stage text with: "Planned — plan v2 (plan run 2, 18 Nov 2026; `output/INC-003-epic-1-RWB-E1-042/plan/plan.md`); plan gate round 2 pending. Spec revision 13 passed its gate on 18 Nov 2026. Build not started" |
| Add a plan trace for `FR-RWB-010` | `FR-RWB-010` → `SPEC-RWB-E1-042-001` .. `-027` → `TASK-00` .. `TASK-25` (`output/INC-003-epic-1-RWB-E1-042/plan/tasks.md`) → tests `TC-E1-042-01` .. `-46` (`plan/tests/scenarios.md`; `TC-E1-042-12` Blocked, `OI-E1-042-001`) → code: pending, branch cut after RWB-E1-044 and RWB-TE-001 merge → modules `casewf.config`, `casewf.config.api`, additive `access.api` / `access.internal` |
| Add the migration trace | `FR-RWB-010` → `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` (`backend/src/main/resources/db/modulemigration/recovery/`); `<seq>` assigned at merge (D-RUN-07); record the assigned number here once the orchestrator sets it |

## 2. `aisdlc/docs/increments/INC-003-epic-1-RWB-E1-042.md` and `aisdlc/docs/increments/INDEX.md`

| File | Change |
|---|---|
| `aisdlc/docs/increments/INC-003-epic-1-RWB-E1-042.md`, Status (lines 21 and 147) | "Planned — plan v2 (plan run 2, 18 Nov 2026; `plan/plan.md`, `plan/tasks.md`); plan gate round 2 pending. The 10 Nov 'Implemented' status refers to the ACE monorepo pack, not this repository" |
| The same file, files table (if it carries one) | Add `backend/src/main/resources/config/parameter-catalog.csv`, `backend/src/main/resources/access/interim-capability-grants.csv`, `backend/build.gradle.kts` (generator task and coverage include), `backend/src/main/resources/application.yaml`, `backend/src/main/resources/application-local.yaml`, one recovery migration |
| `aisdlc/docs/increments/INDEX.md`, status column (line 18) and summary (line 94) | "Planned" instead of "Specified"; keep RWB-E1-042 out of the "Implemented" summary |

## 3. `aisdlc/DOCUMENT-GAPS.md` (candidates)

| Local ID | Document (name, version, section) | Gap or conflict | Second source | Blocker? | Why | How the plan proceeded |
|---|---|---|---|---|---|---|
| PG-E1042-01 | Technical specification RWB-E1-042 revision 13, §7.1: `description` required | The six D-RCV-36 catalog rows have no description text in any source; the 13 rows from the 10 Nov pack do (pack CSV `_v2-baseline/implement/config/parameter-catalog.csv` lines 2-14; pack SQL lines 353-430) | Spec §12.4 ("Source" column names owners, ranges and defaults, never description text); the pack covers 13 of the 19 keys | No | A documentation field: nothing served (API v4 `Parameter` has no description) and no rule reads it | The 13 pack texts are used verbatim; one short line is written for each of the six D-RCV-36 rows; the owner may reword any (`PA-E1-042-06`) |
| PG-E1042-02 | Technical specification RWB-E1-042 revision 13, §7.5 and §11.3: `ParameterLoadResult.repeat`, and a 201 with the same body for an identical repeat | API v4 `ReferenceLoad` (lines 8832-8846) has `id`, `table`, `validFrom`, `status`, `rows` and no repeat field | `OI-E1-042-011`, `CLAR-011`; API v4 `postAdminReferenceLoads` (line 3167) | No | The flag is internal to this story's interface; RWB-E1-043's endpoint decides how to expose it, and the API owner already holds the request | `repeat` stays on the interface record and is asserted at interface level (`TC-16`, `TC-33`); no JSON field invented; `api/recovery-api-v4.yaml` not edited |

## 4. `aisdlc/docs/open-items.md`

| Change | Row |
|---|---|
| No new open item | The plan raises none. `OPEN-050` keeps the tech-lead ratification of D-RUN-18 to D-RUN-21 (owner: recovery tech lead); the plan treats none of them as ratified |
| Note against `OPEN-050` | "RWB-E1-042 plan v2 (18 Nov 2026) cites D-RUN-18 to D-RUN-21 as orchestrator rulings and applies them; no ratification is claimed. If any changes, revise `plan/plan.md` §4.3-derived design and RWB-E1-043's SPI together" |
| Note against `OI-E1-042-001` | "`TC-E1-042-12` stays Blocked in `plan/tests/scenarios.md` with its exit criterion; the plan does not schedule it as a pass" |
| Note against `OI-E1-042-011` | "`PG-E1042-02` records that `repeat` has no field in API v4 `ReferenceLoad`; the plan keeps the flag internal" |
| Carried | The 25 spec `OPEN` rows and `CLAR-028` stay open; the plan plans on the recorded defaults and decides none of them. `CLAR-025` and `CLAR-027` stay `SETTLED`, never `RESOLVED` |

## 5. Requests to document owners (no repository file edited)

| Target | Request | Evidence |
|---|---|---|
| Orchestrator (merge) | Assign the next free four-digit `<seq>` to `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql` at merge and record the assigned name in the traceability row and the increment card. No artefact of this stage fixes a number | D-RCV-28, D-RUN-07; `plan.md` "Migrations"; `tasks.md` TASK-15 |
| RWB-TE-001 owner (module map and published-surface test) | The merge request adds `config.api` to the `casewf` `published` list and extends T-TE001-14's expected sets with the eleven `casewf.config.api` types, `access.api` `MessageResolver`, `CapabilityCheck`, `CatalogParameterReader`, `CatalogParameterReader.Value`, and the `casewf` named interface `config.api`. Extension, not weakening: nothing removed, no assertion relaxed | Spec §12.12 T-1, T-2; `A-40`, `A-41`; `plan.md` "Plan-time checks" item 7; `tasks.md` TASK-08 |
| RWB-TE-001 owner (coverage wiring) | Add the test-output classes of `th/co/scb/ace/demo/recovery/architecture/parameters/` to `classDirectories` of `recoveryCoverageReport` and `recoveryCoverageVerification`, excluding JUnit classes and fixtures. RWB-TE-001 plan v7's `boundaryToolingClasses` does not take the package in; extend the merged filter, never replace it | Spec §12.11, §14; R6-1; §4 of the spec's shared updates (rev 7); `tasks.md` TASK-21 |
| RWB-E1-043 specifier | Confirmed at plan time (this stage re-read E43S revision 9 and revision 8): the names this story publishes are unchanged, the `PARAMETER` route stays a dispatcher branch with `ObjectProvider` and 404 `MSG-P4-003` when the flag is off, and `ParameterLoadHandlerImpl` implements no `access.api` type. No change is requested beyond the spec's existing rev 13 re-baseline row | `plan.md` "Plan-time checks" items 1 and 2; spec §4.3; `A-51` |
| RWB-TE-003 specifier | `ApiExceptionHandler.problem` gains a second branch for the status-and-message-ID form, where `error()` is null; that branch logs message ID (or `none`), status, `traceId`, cause class and "cause suppressed". Do not dereference `error()` on it | Spec §10.2; `A-43`; `plan.md` "Plan-time checks" item 5 |
| Recovery tech lead / catalog owner (RW-COE) | Review the 19 catalog `description` texts — the 13 from the 10 Nov pack used verbatim and the six plan-written D-RCV-36 lines — and the interim grants rows for the seven RW- roles before the build | `PG-E1042-01`; `PA-E1-042-06`; `PA-E1-042-10` |
| `README.md` owner | The coverage note ("not yet part of check. Add it once the first story's code lands") still contradicts D-RCV-40 (outside `check`). This stage did not edit it | `E1042-SP-DG-13`; `tasks.md` TASK-22 |

## 6. Notes for the orchestrator's plan gate

| Item | Value |
|---|---|
| Gate | Not run by this stage. `GATE_REVIEW: PENDING_ORCHESTRATOR`; the round-1 review (`../review/plan-gate-review.md`) was written by the orchestrator's reviewer, and this stage neither ran the gate nor spawned a reviewer |
| Clarifications | 25 `OPEN`, none blocking; `CLAR-020` `RESOLVED`; `CLAR-025`, `CLAR-027` `SETTLED` by unratified orchestrator decisions; `CLAR-028` not decided |
| Human approval claimed | None, anywhere |
| Frontend | `NOT_APPLICABLE` with evidence (`plan/contracts/frontend-integrations.json`); no `frontend/components.md` |
| Migration number | Placeholder only; no number in this stage's files |
