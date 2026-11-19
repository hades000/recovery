> **HISTORICAL — do not build from this file.** This run was written on 10 November 2026 under
> D-RCV-47 (schema `ace`, `rwb_` prefix). Document set v14 (16 November 2026) reinstates schema
> `recovery` and `${recoverySchema}` through D-RCV-35 and ADR-010. Re-run the spec and plan before
> build (`OPEN-036`). The implementation evidence for the two current stories is in
> `output/INC-003-...` and `output/INC-002-...`.

---
title: "Implementation Plan — RWB-E1-043 Reference data service with versioned tables"
run_id: "INC-009-epic-1-RWB-E1-043"
story: "RWB-E1-043"
jira: "TB0001-1204"
status: "SUCCESS"
---

# Implementation Plan — RWB-E1-043 Reference data service with versioned tables

Design Source: NOT_REQUIRED (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`).

| Field | Value |
|---|---|
| Story | RWB-E1-043 (Jira `TB0001-1204`, epic `TB0001-1162`) |
| RUN_ID | `INC-009-epic-1-RWB-E1-043` |
| Input spec | `output/INC-009-epic-1-RWB-E1-043/specify/spec.md` (`status: SUCCESS`, SPEC-RWB-E1-043-001..014, `SPEC_CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]` — 8/8 CLAR resolved) |
| Upstream review | `output/INC-009-epic-1-RWB-E1-043/specify/compliance-validation.md` (`REVIEW_STATUS: PASS`, `[CRITICAL:0][HIGH:0][MEDIUM:0][LOW:3]`, gate-002 re-validation 2026-11-06) |
| Governing decisions | D-RCV-02, -05, -07, -11, -19, -20, -21, -28, -34, -36, -47, -48; ADR-RCV-001 (D-RCV-47/D-RCV-48, 2026-11-10, supersede D-RCV-18's schema/table-naming rule for this plan — approved disposition, Jira `TB0001-1204` comment `1783253`) |
| ACE baseline | Not available locally. `ace-monorepo/` does not exist in this workspace (CTX-GAP-020); Implementation Builder must record the actual `develop` HEAD SHA at task start in `output/INC-009-epic-1-RWB-E1-043/implement/`. |
| Prepared | 2026-11-10, Implementation Planner (agent run) |

## Plan approval preconditions (NOT met at plan time)

The plan is written but **not approved**. Implementation Builder must not start until every row below has a decision and a date. TASK-RWB-E1-043-00 checks them; every build task is `BLOCKED_BY` it.

| ID | Precondition | Owner | State on 2026-11-10 | Evidence when met |
|---|---|---|---|---|
| PRE-1 | Specification and backlog gate approval | Product Owner | **PENDING** (`TBC` in the increment card; GAP-006) | Decision and date in `docs/increments/INC-009-epic-1-RWB-E1-043.md` "Owners and approvals" |
| PRE-2 | Design and architecture approval | Forward Deployed Architect | **PENDING** (`TBC`; GAP-006). No new architecture decision is proposed by this plan — ADR-RCV-001 already covers the API style used by the three endpoints — so this gate is a confirmation, not a design review. | Decision and date in the increment card |
| PRE-3 | REVIEW-RWB-E1-043-001 (Low, spec gate-002): no role in the permission matrix holds Reference data A | Solution architect | **PENDING**. Recorded disposition is "load the RW-RISK grant through RWB-E1-037 before the first SIT approval" — a SIT precondition, not a code-time block; `CLAR-001` already lets the Builder assume RW-RISK holds the right. | RW-RISK Reference-data-A grant visible in the permission matrix load (RWB-E1-037) before SIT approval testing starts |
| PRE-4 | RWB-E1-044 Flyway bean merged to `develop` (own bean, own history table `flyway_schema_history_recovery`, `baselineVersion("0")`, `baselineOnMigrate(true)`, `createSchemas(false)`, tables unqualified with `rwb_` prefix in schema `ace` — D-RCV-47/D-RCV-48) | ACE tech lead / recovery tech lead | **PENDING to verify.** The RWB-E1-044 INDEX.md-vs-spec.md status conflict reported earlier is resolved as a document-status fact: `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` frontmatter now reads `status: "SPECIFIED"`, and its plan/task gates were approved 2026-11-10 13:41 by Jesniphat Pukkham (increment card). This confirms the document status, not that the Flyway bean is actually merged to `develop` — TASK-01 still verifies that directly as its own live check. | `ace-monorepo` `develop` contains the recovery Flyway `SampleModuleConfig`-pattern bean per D-RCV-47/D-RCV-48; TASK-01 checks it directly |
| PRE-5 | RWB-E1-042 configuration service merged (catalog entries mechanism, `refdata.cache.ttl-seconds`, table-code list) | ACE tech lead / recovery tech lead | **PENDING to verify** | TASK-01 checks the published `ConfigurationService` interface exists in `develop` |
| PRE-6 | RWB-E1-022 session/role mechanism available for the three new endpoints' authorization (`SessionResolver`, resolved roles, `RecoveryAccessGuard`/INT-34 403 path per D-RCV-36) | ACE tech lead / recovery tech lead | **PENDING to verify.** Not listed as a dependency in the RWB-E1-043 increment card (only RWB-E1-042 and RWB-E1-044 are listed), but the controllers in this plan cannot enforce "Reference data C/A/R" without it. `docs/increments/INC-031-epic-1-RWB-E1-022.md` shows that story `Status: In delivery` (same lifecycle stage as this one), not yet SUCCESS. Flagged as an undeclared cross-story dependency; see Risks. | `RecoveryAccessGuard` and the role-to-session mapping exist in `develop`; TASK-01 checks directly |
| PRE-7 | Plan approval | Forward Deployed Architect (D-RCV-15) | PENDING; only given after PRE-1..PRE-6 and the plan gate review | Decision and date in the increment card |
| PRE-8 | Task approval | Forward Deployed Engineer (D-RCV-15) | PENDING | Decision and date in the increment card |

If PRE-4, PRE-5 or PRE-6 is not yet true when Implementation Builder starts, Builder stops at TASK-01 and reports `NEXT_STEP` rather than stubbing the missing interface.

## Upstream review disposition (human, 2026-11-10)

Spec gate review, gate-002 re-validation (`specify/compliance-validation.md` §8, 2026-11-06): `REVIEW_STATUS: PASS`, `[CRITICAL:0][HIGH:0][MEDIUM:0][LOW:3]`. All three Low findings carry a "Recorded" disposition with a named owner; none changes the spec's scope or blocks this plan under the severity policy (`.github/rules/pdlc.md`: Low-only findings do not automatically stop a handoff).

| Finding | Severity | Recorded disposition (2026-11-06) | Effect on plan |
|---|---|---|---|
| REVIEW-RWB-E1-043-001 | Low | Owner: Solution architect. Load the RW-RISK grant through RWB-E1-037 before the first SIT approval | Carried forward as PRE-3 above; no code change |
| REVIEW-RWB-E1-043-002 | Low | Owner: Data steward. Table column definitions held as catalog entries is unusual for a schema design, accepted as the CLAR-003 resolution | None; TASK-06 implements `ReferenceTableSchemas` against RWB-E1-042 catalog entries as resolved |
| REVIEW-RWB-E1-043-003 | Low | Owner: Product Owner. Named Product Owner and FDA are TBC | Carried forward as PRE-1/PRE-2/PRE-7 above |

The `PASS` status and the three Low findings stay visible; they are not relabelled.

## Change scope (carried from spec)

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen; SCR-40 is Epic 8 |
| Logic In Scope | `YES` — versioning, load checks, approval, effective dating, cache, read logging, no-version handling |
| API In Scope | `YES` (`NEW_API_REQUIRED`) — `POST /api/recovery/v1/admin/reference-loads`, `POST /api/recovery/v1/admin/reference-loads/{loadId}/approve`, `GET /api/recovery/v1/admin/lists/{listCode}`, plus `POST /api/recovery/v1/admin/reference-loads/{loadId}/rollback` (CLAR-008) |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |
| Database / Flyway | One new migration: `rwb_reference_version`, `rwb_reference_row` (D-RCV-47/D-RCV-48, unqualified in schema `ace`) |
| Feature flag | `rwb.p3.refdata-versions`. Off: engines read the values loaded before this story |

## Plan-time verification of spec "plan confirms" items

| Item (spec) | Check run at plan time | Result | Plan decision |
|---|---|---|---|
| RWB-E1-044 Flyway bean (precondition) | `ace-monorepo` not present in this workspace (confirmed: `find . -maxdepth 2 -iname ace-monorepo` empty) | Cannot verify directly | TASK-01 re-checks against the real `develop` branch at task start; Builder stops and reports if the bean is absent, per PRE-4 |
| RWB-E1-042 `ConfigurationService` and `refdata.cache.ttl-seconds` (precondition) | Same — not verifiable from this workspace | Cannot verify directly | TASK-01 re-checks; Builder stops and reports if absent, per PRE-5 |
| LOV-REF-TABLE holds the 13 codes (spec precondition) | Not verifiable from this workspace; owning story for the seed data is not named in spec.md | Cannot verify directly | TASK-01 re-checks the row count for LOV-REF-TABLE at task start; if fewer than 13 rows exist, Builder stops rather than seeding business values itself (guardrail: "no business value in code") |
| `recovery.casewf` module root package-info (RWB-TE-001 main-scope skeleton) | `output/INC-002-epic-1-RWB-TE-001/plan/tasks.md` TASK-02 creates `recovery` + 19 nested module `package-info.java` only, no `refdata` sub-package | Skeleton for `casewf` exists; `refdata` does not | TASK-02 here adds only the `refdata` / `refdata.api` / `refdata.internal` sub-packages inside the existing `casewf` module |
| RecoveryBoundaryTest / module map already cover `casewf.api` (RWB-TE-001) | `output/INC-002-epic-1-RWB-TE-001/plan/data-model.md` §1 shows `recovery-modules.yaml` already lists `{ code: P3, name: casewf, published: [api], clientPackages: [] }` | No module-map change needed for this story | TASK-14 runs the existing `RecoveryBoundaryTest` against the new classes; no edit to `recovery-modules.yaml` |
| Rollback behaviour detail beyond CLAR-008 | spec.md's status-transition matrix states only "Rollback → ROLLED_BACK → Previous version in force again"; no row-level mechanics are given | Not specified at the field level | Flagged as **IMPL-NOTE-01** (see Risks): TASK-09 implements rollback as (a) the rolled-back version's own `status` becomes `ROLLED_BACK`, and (b) the version it had superseded has its `valid_to` cleared back to open-ended, since `valid_to` is the one editable field the append-only trigger allows on `reference_version` besides `status`/`approver_user_id`/`approved_at`. This is an implementation inference, not a spec fact; FDA/Technical Specifier should confirm before Builder codes it |

## Scope

Each bullet maps to tasks in `tasks.md`.

| # | Scope bullet | TASK-* |
|---|---|---|
| S1 | Check plan-approval preconditions; verify RWB-E1-044/RWB-E1-042/RWB-E1-022 merge state and LOV-REF-TABLE seed; create ACE branch | TASK-00, TASK-01 |
| S2 | `refdata` / `refdata.api` / `refdata.internal` package skeleton inside the existing `casewf` module | TASK-02 |
| S3 | Migration `V<seq>__rwb_e1_043_reference_versions.sql`: `rwb_reference_version`, `rwb_reference_row`, append-only triggers | TASK-03 |
| S4 | JPA entities, repositories | TASK-04, TASK-05 |
| S5 | `ReferenceTableSchemas` (catalog-backed column rules, LOV-REF-TABLE codes) | TASK-06 |
| S6 | `ReferenceVersionRegistryImpl`: load checks, numbering, idempotency | TASK-07 |
| S7 | `ReferenceVersionRegistryImpl`: approval, optimistic lock, `valid_to` supersede | TASK-08 |
| S8 | `ReferenceVersionRegistryImpl`: rollback (CLAR-008, IMPL-NOTE-01) | TASK-09 |
| S9 | `ReferenceDataServiceImpl`: version-in-force resolution, `NoVersionInForceException` | TASK-10 |
| S10 | `ReferenceRowCache` (TTL from RWB-E1-042) | TASK-11 |
| S11 | `ReferenceVersionLogger` | TASK-12 |
| S12 | Controllers for the three delivered endpoints plus rollback; authorization per role | TASK-13 |
| S13 | Module-boundary verification (no new rule code; run existing `RecoveryBoundaryTest`) | TASK-14 |
| S14 | Backend unit tests: load checks | TASK-15 |
| S15 | Backend unit tests: approval and version resolution | TASK-16 |
| S16 | Backend unit/integration tests: rollback, logging | TASK-17 |
| S17 | Backend unit tests: cache TTL | TASK-18 |
| S18 | Feature-flag catalog entry confirmation (verification only; engines that consume the flag are out of scope) | TASK-19 |
| S19 | Coverage gate, diff/guardrail check | TASK-20 |
| S20 | Release readiness, traceability update, risk escalation | TASK-21 |

## Backend Plan

### Package and file layout

`backend/src/main/java/th/co/scb/ace/demo/recovery/casewf/refdata/`:
- `api/` (published, `@NamedInterface("api")`): `ReferenceVersionRegistry`, `ReferenceDataService`, `VersionedRows`, `ReferenceVersion` (DTO view), `NoVersionInForceException`.
- `internal/`: `ReferenceVersionRegistryImpl`, `ReferenceDataServiceImpl`, `ReferenceRowCache`, `ReferenceTableSchemas`, `ReferenceVersionRepository`, `ReferenceRowRepository`, `ReferenceVersionLogger`, JPA entities `ReferenceVersionEntity`, `ReferenceRowEntity`, controllers `ReferenceLoadController`, `ReferenceListController`.

P4's load/approval handler and other recovery modules depend only on `refdata.api` types (spec §Package and boundaries). No module reads `rwb_reference_version`/`rwb_reference_row` directly; `lov_value` is read only through the P4 interface (unchanged by this story).

### Data model

`rwb_reference_version` / `rwb_reference_row` DDL, constraints, indexes and triggers are carried verbatim from spec §Data and migration into `data-model.md`, renamed with the `rwb_` prefix and no schema qualifier per D-RCV-47/D-RCV-48 (approved disposition, Jira `TB0001-1204` comment `1783253`, 2026-11-10). Migration file: `V<seq>__rwb_e1_043_reference_versions.sql` under `backend/src/main/resources/db/modulemigration/recovery/`, line 1 `-- Story: RWB-E1-043`. **`<seq>` is not pre-allocated**: `docs/architecture/migration-merge-order-map.md` names sequences only through the stories it lists, and RWB-E1-043 is not one of them (confirmed in the prior planning session for this story). Per D-RCV-28/D-RCV-34, the real 4-digit sequence is taken as the next free number at merge time, not assigned here.

### Load, approval, rollback, read (TASK-07..TASK-12)

Implements the seven load checks, the approval rule (approver present, different from author, holds Reference data A, optimistic lock, `valid_to` supersede), rollback (CLAR-008 plus IMPL-NOTE-01), and the engine-facing `rows(tableCode, businessDate)` resolution with `NoVersionInForceException`, exactly as given in spec §Load checks, §Approval and version resolution, §Cache and logging, §Transaction and events. One transaction per load; one transaction per approval (status + approver + replaced version's `valid_to`).

### Authorization (TASK-13)

Reference data C to load (RW-REFADM; RW-COE for tables it owns), A to approve (RW-RISK, assumed per DL01/CLAR-001), R to read lists (SY-CASEWF, SY-RULES, RW-AUDIT). HTTP/MSG mapping exactly as spec §API change assessment: 401 MSG-P4-001, 403 MSG-P4-002, 404 MSG-P4-003, 409 MSG-P3-027/MSG-P7-002/MSG-GEN-004, 422 MSG-P3-027/MSG-GEN-001, 503. Enforcement uses the role/session mechanism from RWB-E1-022 (PRE-6); the same-person RW-REFADM/RW-RISK exclusion (spec §Security and authority) is a permission-matrix rule, not code in this story.

## Frontend Plan

`NOT_APPLICABLE`. `Frontend Changes Required: NO` (spec Change Scope Declaration); no screen, component, route or label is touched. SCR-40 is Epic 8.

## Integration and cross-layer

- RWB-E1-044: Flyway bean this migration rides on (PRE-4).
- RWB-E1-042: `refdata.cache.ttl-seconds`, table-code catalog, and the column-schema catalog entries read by `ReferenceTableSchemas` (PRE-5).
- RWB-E1-022: authorization/session mechanism for the four endpoints (PRE-6, undeclared dependency — see Risks).
- RWB-E1-019: adds `QUEUE_MEMBER` to LOV-REF-TABLE later (CLAR-002); no action in this story.
- RWB-E1-037: loads the permission matrix, including the RW-RISK Reference-data-A grant (PRE-3).
- Allocation engine, timer engine, case service: impacted existing nodes that call `ReferenceDataService.rows(...)`; their own start-up wiring is out of scope for this story (spec "Impacted Existing Nodes", not "New Nodes Required").

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Trace | Reason | Tasks |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen/component/route/label change | — |
| Backend | YES | REQUIRED | 80% lines, statements, branches, functions on changed code (recovery-only JaCoCo tasks, D-RCV-28 (3)) | FR-RWB-012, FR-RWB-020; SPEC-RWB-E1-043-001..014 | New registry, read service, cache, schema checks, repositories, logger, controllers | TASK-15, TASK-16, TASK-17, TASK-18, TASK-20 |

## Requirement Logic To Task Coverage

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | SPEC-RWB-E1-043-002 | TASK-06, TASK-15 | DIRECT_IMPLEMENTATION | `ReferenceTableSchemasTest`; TC-E1-043-12 | COVERED |
| BR2 | SPEC-RWB-E1-043-001, -004 | TASK-03, TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | Migration DDL review; `ReferenceVersionRegistryImplTest`; TC-E1-043-01, -07 | COVERED |
| BR3 | SPEC-RWB-E1-043-006 | TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | `ReferenceDataServiceImplTest`; TC-E1-043-01, -05 | COVERED |
| BR4 | SPEC-RWB-E1-043-005 | TASK-08, TASK-16 | DIRECT_IMPLEMENTATION | `ReferenceVersionRegistryImplTest`; TC-E1-043-02 | COVERED |
| BR5 | SPEC-RWB-E1-043-003 | TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | TC-E1-043-04, -10 | COVERED |
| BR6 | SPEC-RWB-E1-043-003, -006 | TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | TC-E1-043-06 | COVERED |
| BR7 | SPEC-RWB-E1-043-008 | TASK-12, TASK-17 | DIRECT_IMPLEMENTATION | `ReferenceVersionLoggerTest`; TC-E1-043-03 | COVERED |
| BR8 | SPEC-RWB-E1-043-007 | TASK-08, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-01 | COVERED |
| BR9 | SPEC-RWB-E1-043-009 | TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-09 | COVERED |
| AC1 | SPEC-RWB-E1-043-004, -006, -007 | TASK-07, TASK-08, TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-01 | COVERED |
| AC2 | SPEC-RWB-E1-043-005 | TASK-08, TASK-13, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-02 | COVERED |
| AC3 | SPEC-RWB-E1-043-008 | TASK-12, TASK-17 | DIRECT_IMPLEMENTATION | TC-E1-043-03 | COVERED |
| AC4 | SPEC-RWB-E1-043-003 | TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | TC-E1-043-04 | COVERED |
| AC5 | SPEC-RWB-E1-043-005, -006 | TASK-08, TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-05 | COVERED |
| AC6 | SPEC-RWB-E1-043-003 | TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | TC-E1-043-06 | COVERED |
| AC7 | SPEC-RWB-E1-043-004 | TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | TC-E1-043-07 | COVERED |
| AC8 | SPEC-RWB-E1-043-010 | TASK-08, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-08 | COVERED |
| AC9 | SPEC-RWB-E1-043-009 | TASK-10, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-09 | COVERED |
| AC10 | SPEC-RWB-E1-043-003 | TASK-07, TASK-15 | DIRECT_IMPLEMENTATION | TC-E1-043-10 | COVERED |
| X1..X7 | SPEC-RWB-E1-043-003..010 | TASK-07, TASK-08, TASK-10, TASK-15, TASK-16 | DIRECT_IMPLEMENTATION | TC-E1-043-02, -04, -06, -07, -08, -09, -10 | COVERED |

No `BLOCKED` row. Every REQ_REF above is carried verbatim from spec.md's own "Requirement-to-SPEC Logic Coverage" table; SPEC-RWB-E1-043-011, -012, -013 are not individually claimed against a BR/AC/X row here because spec.md's coverage table does not tie them to one (only the Unit Test Applicability table's range notation "SPEC-RWB-E1-043-001..014" implies their existence) — per CLAUDE.md, this plan does not invent what they cover; Detailed-design subsections not tied to a numbered SPEC (Package and boundaries, Observability and operations, Performance, Feature flag and rollback) are cited by section header in the tasks below instead of by a fabricated SPEC-* claim.

## Functional Test Scenarios

API Tester is `Applicable` (API In Scope: YES); Functional Automation Test is `Not used` (increment card, UI In Scope: NO). The split below follows what each of the four delivered endpoints can actually exercise over HTTP, versus the engine-facing `rows(tableCode, businessDate)` call, which has no REST endpoint of its own and is therefore backend-test scope, not API Tester scope.

| Scenario | Owner | Applicability | Note |
|---|---|---|---|
| TC-E1-043-02 | API Tester + backend unit | Both | API Tester: `POST .../approve` by the author returns 409 MSG-P7-002. Backend: `ReferenceVersionRegistryImplTest` asserts the domain exception (TASK-16) |
| TC-E1-043-04 | API Tester | API-reachable | `POST /admin/reference-loads` with a bad row returns 422 naming row 12 and column |
| TC-E1-043-06 | API Tester | API-reachable | `POST /admin/reference-loads` with a past `valid_from` returns 422 |
| TC-E1-043-07 | API Tester | API-reachable | Same file twice returns the same `loadId`/version, no second version |
| TC-E1-043-08 | API Tester | API-reachable | Two concurrent `POST .../approve` calls: one 200, one 409 MSG-GEN-004 |
| TC-E1-043-10 | API Tester | API-reachable | Header-only file returns 422 MSG-GEN-001 naming `rows` |
| TC-E1-043-11 | API Tester | API-reachable | RW-CASEOWN calling `POST /admin/reference-loads` returns 403 MSG-P4-002 |
| TC-E1-043-01 | API Tester (version/status visibility) + backend unit (date resolution) | Split | API Tester confirms via `GET /admin/lists/EXPOSURE_BAND` that v3's `valid_to` is 2026-11-30 and v4 is `APPROVED`; the business-date-based "which version is served to an engine" half of this scenario has no REST path and is TASK-16's job |
| TC-E1-043-05 | API Tester (status visibility) + backend unit (serving) | Split | Same split as TC-E1-043-01: GET confirms HOLIDAY v2 stays `VALIDATED`; `ReferenceDataServiceImplTest` confirms v1 is still returned by `rows(...)` |
| TC-E1-043-03 | Backend unit/integration | Not API-reachable | Engine read + log line has no REST endpoint; TASK-17 |
| TC-E1-043-09 | Backend unit/integration | Not API-reachable | "Engine does not start" is an in-process call to `rows(...)`, not an HTTP response; TASK-16 |
| TC-E1-043-12 | Backend unit | Not API-reachable | Unknown table code, checked inside `ReferenceTableSchemas`; TASK-15 |
| TC-E1-043-13 (planner-added) | Backend unit/integration | Not in spec.md's test table | Rollback behaviour (CLAR-008 + IMPL-NOTE-01): asserts `ROLLED_BACK` status and the previous version's `valid_to` cleared. Recommend FDA/Technical Specifier confirm the exact rollback mechanics before Builder codes TASK-09 |
| TC-E1-043-14 (planner-added) | Backend unit | Not in spec.md's test table | Cache TTL expiry and "cache never serves non-APPROVED" (spec §Cache and logging); TASK-18 |

`recovery-workbench-api-specification-v2.yaml`'s exact query parameters for `GET /admin/lists/{listCode}` (e.g. whether a business-date filter exists) are not restated in spec.md beyond "returns `ListOfValues` with versions"; API Tester must read the OpenAPI contract directly rather than this plan asserting a parameter name.

## Screen-to-task mapping

`NOT_APPLICABLE` (`UI In Scope: NO`).

## Security, privacy, compliance

- Authorization table (spec §Security and authority): RW-REFADM (CRUD), RW-COE (C for owned tables), RW-RISK (A, assumed DL01), SY-CASEWF/SY-RULES (R), RW-AUDIT (R). Same person may not hold RW-REFADM and RW-RISK (separation of duty, permission-matrix rule, not code).
- DELEGATION_LIMIT approval follows `doa.txt` rule 11 (approved by Risk) — consistent with RW-RISK holding Reference data A.
- No personal data in logs: `ReferenceVersionLogger` carries table code, version, business date only (BR7/AC3).
- No business value in code: table codes, columns, bands, periods, limits are rows (catalog entries / LOV-REF-TABLE), not Java constants (guardrail, re-enforced at TASK-20's diff check).
- `lov_value` read only through the P4 interface; no module reads `rwb_reference_version`/`rwb_reference_row` directly (package-boundary rule, TASK-14).

## Risks

| Risk | Mitigation | Task |
|---|---|---|
| **Resolved.** RWB-E1-044 INDEX.md-vs-spec.md status conflict: `docs/increments/INDEX.md` showed `SUCCESS` while `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` frontmatter showed `status: "BLOCKED"`. The conflict is resolved as a document-status fact — spec.md now reads `status: "SPECIFIED"`, and RWB-E1-044's plan/task gates were approved 2026-11-10 13:41 by Jesniphat Pukkham. This confirms document status only, not that the Flyway bean is actually merged | TASK-01 still checks the Flyway bean's presence in `develop` directly as its own live check, independent of either status field | TASK-01, TASK-21 |
| RWB-E1-022 (session/role mechanism) is not listed as a dependency in this story's increment card, but the four endpoints cannot enforce authorization without it; that story is itself `Status: In delivery`, not `SUCCESS` | PRE-6 added to plan-approval preconditions; TASK-01 checks for `RecoveryAccessGuard`/role mapping directly; flag the missing increment-card dependency link to Context Updater/human | TASK-01, TASK-21 |
| Migration `<seq>` is not pre-allocated: RWB-E1-043 is excluded from `docs/architecture/migration-merge-order-map.md`'s build-order table | TASK-03 takes the next free 4-digit sequence at merge per D-RCV-28/D-RCV-34, not a number fixed in this plan | TASK-03 |
| Rollback field-level mechanics (IMPL-NOTE-01) go beyond the literal text of CLAR-008 and the status-transition matrix | Document the inferred behaviour explicitly, add TC-E1-043-13 as a planner-added test, recommend FDA/Technical Specifier confirmation before coding | TASK-09, TASK-17 |
| LOV-REF-TABLE's 13 codes are an entry precondition, but spec.md does not name which story seeds them | TASK-01 checks the row count at task start; Builder stops rather than seeding business values itself if the precondition is not met | TASK-01 |
| REVIEW-RWB-E1-043-001 (Low): no RW-RISK holder of Reference data A exists yet in the live permission matrix | Carried as PRE-3; does not block coding, blocks SIT approval testing | TASK-21 |
| **Resolved.** REVIEW-RWB-E1-043-PLAN-001 (Low, plan-gate review): rollback endpoint's 404 MSG-P4-003 and 422 MSG-P3-027 both named an unresolved-vs-not-APPROVED `loadId` with no rule distinguishing which applies | Approved disposition Option A — Jira `TB0001-1204` comment `1783253`, 2026-11-10: 404 only when `loadId` resolves to no `rwb_reference_version` row at all; 422 when it resolves but status is not APPROVED. Applied to `contracts/backend-apis.json` (EP-RWB-E1-043-04 errors/note), `tasks.md` TASK-09, and `tests/scenarios.md` (TC-E1-043-13b/-13c added) | TASK-09, TASK-13 |

## Out of scope

Rule-table load, validation and rollback (RWB-E1-029); permission and masking tables (RWB-E1-037); delegation content (RWB-E1-038); checklist fields and audit report (RWB-E1-048); product completeness checks (RWB-E1-045); screens SCR-39/40/42 (Epic 8); engine-side wiring of the `rwb.p3.refdata-versions` flag inside the allocation/timer engines themselves (those are impacted existing nodes, not new nodes, in spec.md's Change Scope Declaration).

## Plan-gate compliance review

Compliance Reviewer ran against `plan.md`, `tasks.md`, `data-model.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `tests/scenarios.md`; full review: `review/plan-gate-review.md`.

- REVIEW_STATUS: `FAIL` (status preserved per `.github/rules/pdlc.md` — a finding exists — but severity is Low-only). The `FAIL` status is not retroactively changed to `PASS`: no new Compliance Reviewer run has taken place since `review/plan-gate-review.md`; what has changed is that a human disposition for the finding is now recorded and the plan artifacts have been updated to match it.
- Findings: `[CRITICAL:0] [HIGH:0] [MEDIUM:0] [LOW:1]`
- `REVIEW-RWB-E1-043-PLAN-001` (Low): rollback endpoint's 404/422 error-contract overlap — **disposition recorded**: Option A, Jira `TB0001-1204` comment `1783253` (2026-11-10, Jesniphat Pukkham). Applied to `contracts/backend-apis.json`, `tasks.md` TASK-09, and `tests/scenarios.md` (see §Risks above).
- `REVIEW_GATE_WARNING`: Low-severity review failure does not automatically stop this handoff; the finding remains visible (this section, §Risks) even though its remediation has now been applied. Independent stage hard gates (80% coverage, required unit tests) remain binding at Builder stage regardless. This recorded disposition resolves the Low finding only — it is not itself PRE-7 (Plan approval) or PRE-8 (Task approval), which remain separately pending (see §Plan approval preconditions).
- The reviewer independently re-verified the `SPEC-RWB-E1-043-011/-012/-013/-014` correction (§Requirement Logic To Task Coverage note) is applied consistently across all six files — no finding there.
- The reviewer independently assessed the RWB-E1-044/-042/-022 cross-dependency handling and IMPL-NOTE-01's disclosure — both adequate, no new findings.

## Status reporting

```text
PLANNER_STATUS_SUMMARY: Plan complete for RWB-E1-043; 22 tasks across migration, registry, data service, cache, logger, controllers and tests; no BLOCKED coverage row. Plan-gate review: FAIL (1 Low, non-blocking, REVIEW_GATE_WARNING) — human disposition now recorded (Jira `TB0001-1204` comment `1783253`, 2026-11-10, Option A) and applied to the plan artifacts; PRE-1..PRE-8 remain separately pending.
PLANNER_STATUS_DETAIL: [SUCCESS] [REASON: Upstream spec SUCCESS, 8/8 clarifications RESOLVED, spec-gate review PASS (3 Low, non-blocking), plan-gate review FAIL (1 Low, non-blocking per REVIEW_GATE_WARNING — REVIEW-RWB-E1-043-PLAN-001, disposition recorded and applied)] [Design Evidence Gate NOT_APPLICABLE (UI In Scope: NO)] [UNBLOCK_ACTION: REVIEW-RWB-E1-043-PLAN-001 disposition recorded (Jira comment 1783253) and applied to contracts/backend-apis.json, tasks.md, tests/scenarios.md; this is not PRE-7/PRE-8 — PRE-1..PRE-8 still all pending]
PLANNER_CLARIFICATION_STATUS: [READY] [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: [NOT_REQUIRED] [NOTE: UI In Scope: NO; DESIGN_EVIDENCE_STATUS: NOT_REQUIRED]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 9 BRs, 10 ACs and 7 exception paths map to at least one TASK-*; zero MISSING or CONTRADICTION.
PLAN_REQUIREMENT_COVERAGE_RESULT: [SUCCESS] [TOTAL_RULES: 20] [TASK_COVERED_RULES: 20] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```
