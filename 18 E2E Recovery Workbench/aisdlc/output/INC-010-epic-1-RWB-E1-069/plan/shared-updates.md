# Shared-file updates proposed by INC-010-epic-1-RWB-E1-069 (Implementation Planner, plan v1, 18 Nov 2026)

Under RUN-BRIEF hard rule 3 this stage edits no shared file. The orchestrator applies the rows below after the plan gate.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

### §3 Story trace: replace row 010 (columns `INC | Story | Business | Functional | Spec / plan / evidence | Status`)

| 010 | `RWB-E1-069` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` (SPEC-RWB-E1-069-001..020); `output/INC-010-epic-1-RWB-E1-069/plan/plan.md` v1, `tasks.md` (TASK-00..TASK-19), `data-model.md`, `contracts/`, `tests/scenarios.md` | Planned (plan gate per `review/plan-gate-review.md`) |

### §6 Coverage summary

- "Current spec/plan, not built": add `RWB-E1-069` (INC-010) with the plan path above; remove the earlier "Current spec, no plan" line if the orchestrator added it after the spec gate.
- Epic 1 stories row: "Current spec" unchanged at 5; "Planned, not built" 1 → 2 if `RWB-E1-044` is counted there.

### §7 Evidence index: add

| INC-010 `RWB-E1-069` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md`; `output/INC-010-epic-1-RWB-E1-069/plan/plan.md` | `output/INC-010-epic-1-RWB-E1-069/review/plan-gate-review.md` (when the orchestrator runs it) | not built |

### SPEC-to-test detail (plan stage; mirrors `plan.md` "SPEC to task map")

| SPEC | Tasks | Tests |
|---|---|---|
| 001 | TASK-03, -04, -09 | T-E1-069-11; `MigrationFolderCoverageTest` |
| 002 | TASK-09 | T-E1-069-09, -10; TC-06 |
| 003 | TASK-08, -09 | TC-01, TC-06 |
| 004 | TASK-08, -09 | TC-01, TC-02 |
| 005 | TASK-10, -11 | TC-03; T-E1-069-13 |
| 006 | TASK-10, -11 | TC-03; T-E1-069-14 |
| 007 | TASK-08, -09 | TC-01, TC-07 |
| 008 | TASK-07, -08, -09, -14 | TC-01..05; T-E1-069-16, -17 |
| 009 | TASK-08, -09 | TC-02 |
| 010 | TASK-08, -09 | TC-05, TC-06 |
| 011 | TASK-08, -09 | TC-07 |
| 012 | TASK-12, -13 | TC-08; `Bnd6RuleTest` |
| 013 | TASK-05, -06, -07 | T-E1-069-12; `MigrationFolderCoverageTest` |
| 014 | TASK-03, -04 | T-E1-069-11 |
| 015 | TASK-07, -14, -15, -17 | T-E1-069-16; `RecoveryDatabaseIT` |
| 016 | TASK-13, -19 | TC-08; scope check |
| 017 | TASK-08, -09, -14 | TC-01, TC-03; T-E1-069-14 |
| 018 | TASK-10, -11 | TC-03; T-E1-069-13 |
| 019 | TASK-08, -09, -16 | T-E1-069-15 |
| 020 | TASK-08, -09 | T-E1-069-09, -10 |

## 2. `aisdlc/docs/increments/INDEX.md` and the INC-010 card

- **INDEX row 010:** status "Planned"; plan column `output/INC-010-epic-1-RWB-E1-069/plan/plan.md`; gate column per the orchestrator's plan gate.
- **Card INC-010:** Planning "SUCCESS 2026-11-18 (plan v1, 20 tasks TASK-00..TASK-19)"; Compliance review per the plan gate file the orchestrator writes.

## 3. `aisdlc/docs/open-items.md` (proposed)

No new item is proposed by the plan stage. The spec's items stay open and unchanged:

| Item | Status after this stage | Note |
|---|---|---|
| OI-069-A | Open | P4(c)-(d) only; the ACE DBA and environment owner |
| OI-069-B | Open | RWB-ACE-001 Appendix A maps 12 columns into views that do not carry them (DG-L07) |
| OI-069-C | Open | RWB-ACE-001 AC4 against its §10/§12 (DG-L08) |
| OI-069-D | Open | Section B merge gate under `outOfOrder(false)` (DG-L20) |
| OI-069-E | Open | Align Environment and Deployment Design v4 and Security and Access Design v4 wording |
| OI-069-F | Open | BND-6 rulings for `information_schema` and the lower-case identifier rule (ASM-013) |
| OI-069-G | Open | Correct `ace_to_date` in ACE Source Views v1 and Physical Schema v6 |
| OI-069-H | Open | Security review of the definer-rights trade-off |
| OI-069-I | Open | `recovery_svc` DML on Workbench tables in SIT and above (DG-L25) |
| OI-069-J | Open | Correct `sys_fields.is_personal` in Physical Schema v6 to the inventory |
| OI-069-K | Open | Align story AC5 and TC-05 totals with the seeded figures (DG-L05) |
| OI-069-L | Open, **expanded** | (a) accept the retirement of the `RecoveryDatabaseIT` version-`0` assertion with the S2 stage and the SPEC-017 replacement (DG-L30, DG-P01); (b) schedule the external conformance run in DEV and SIT. Owners: recovery tech lead with RWB-E1-001 and the pipeline owner |
| OI-069-M (proposed OPEN-051) | Open | Ratify or replace D-RUN-14; no human approval claimed |
| OPEN-035 (existing) | Open | ACE Tier 1 tables at the baseline head in DEV/SIT; Blocker = No |
| OPEN-032 (existing) | Open | AMIS, RPS, LIT, WIN, GL and COLLINS scores ingested; Section B only; Blocker = No |

**DG-P02** is not an open item: TASK-00 records the merged `RecoverySchemaMigrationIT` path and stops if the class is absent. **DG-P03** is not an open item: the plan names the package the spec defers.

## 4. `aisdlc/DOCUMENT-GAPS.md` (proposed rows; full evidence in `plan/document-gaps.md`)

| Proposed | Gap | Blocker? |
|---|---|---|
| DG-INC010-14 | E1-001 hand-off "no assertion removed" and "keeps it in the S2 stage" against E1-069 SPEC-017 and DG-L30 (DG-P01) | No |
| DG-INC010-15 | E1-001's plan folder absent at E1-069 plan time; `RecoverySchemaMigrationIT` path and mechanism not yet fixed (DG-P02) | No |
| DG-INC010-16 | The spec defers `ViewConformanceTest`'s package to the plan; the file path fixes `th.co.scb.ace.demo.recovery` (DG-P03) | No |

## 5. `AI-SDLC-BUILD-LOG.md` (proposed row for the orchestrator)

| 2026-11-18 (time of the plan run) | RWB-E1-069 | Plan | implementation-planner | P2 | DONE | plan.md v1 with 20 tasks TASK-00..TASK-19; two migrations `V<seq>__rwb_e1_069_ace_source_views.sql` (A, first) and `V<seq>__rwb_e1_069_ace_tier2_views.sql` (B, after RWB-ACE-001), no number fixed; 42/42 requirement rows; sourceViews, BND-6, the two lint seams and the S2 switch; DG-P01..P03 Blocker No; one-module PASS under D-RUN-21 unratified; D-RUN-14 applied with OPEN-051 open and no human approval; plan gate next |

## 6. Repository files the build will change (for the plan, not applied here)

- `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_069_ace_source_views.sql` (new)
- `backend/src/main/resources/db/modulemigration/recovery/V<seq>__rwb_e1_069_ace_tier2_views.sql` (new)
- the test-scope files of `plan.md` "Files added or changed — test scope"; `backend/src/test/resources/architecture/recovery-modules.yaml` (the `sourceViews` key only)
- `infra/postgres/init/10-load-ace-database.sh`, `infra/postgres/init/20-grants.sql.inc`, `.env.example`, `docker-compose.yml`
- `README.md`, `backend/src/main/resources/db/modulemigration/recovery/README.md`

`backend/build.gradle.kts`, `application.yaml`, `api/recovery-api-v4.yaml`, `frontend/**`, `scripts/dev.ps1` and `.gitlab-ci.yml` are **not** changed.
