# Increment Card — INC-040-epic-1-RWB-E1-013

**RWB-E1-013 — Baseline measures**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-040` |
| Title | Baseline measures |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-013` |
| RUN_ID | `INC-040-epic-1-RWB-E1-013` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P9 Reporting |
| Story type | User story |
| Priority | Must |
| Build order | 40 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-043, RWB-E1-018 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P9 Reporting.

## Scope

**Story:** As the **Tribe lead (RW-TRIBE)**, I want **cases by route, age and queue, realized recovery, time in stage and turnaround per route published as the baseline, with definitions agreed by the Tribe**, so that **every later epic is measured against the same baseline**.

**Business outcome:** Measures are counted by hand from spreadsheets at month end today, and each team counts a case differently. This story holds each measure's definition, data product and formula as an approved data row, publishes the values for business date 27 November 2026 as a frozen baseline, and sends the nightly extract to the data lake for the Power BI data set. It serves REQ-RDF-012 and NFR-065 (measures from Workbench records, not a separate count), and the FSD P9 measure "measures read from the decision log and Workbench records, 100 percent".

**Main flow:**
1. Reference data administrator: loads the measure definition file through POST /admin/reference-loads with table "measure_definition".
2. System: checks each row has a measure code, name, formula, data product, unit, approver and approval date; any failure refuses the whole load.
3. JOB-15 Reporting extract, nightly 01:30: reads the case facts of the previous business date through the P3 reporting interface and the payments since entry through the P1 interface.
4. System: computes each measure in force by its definition: counts by route, age band and queue; realized recovery; median time in stage; median turnaround per route.
5. System: writes one measure_snapshot row per measure, product and dimension value, with the definition version and business date.
6. System: on the baseline business date, marks the rows as baseline and frozen; frozen rows are never changed.

**Acceptance criteria:**
- AC1: Definitions agreed
- AC2: Baseline published
- AC3: Power BI data set
- AC4: Definition without a formula refused
- AC5: Baseline published twice
- AC6: Batch of the baseline date not complete
- AC7: Data lake unavailable
- AC8: Measure with no definition in force

**Out of scope:**
- The steering dashboard data set, SCR-37 and the measures endpoint (RWB-E2-009).
- Queue and ageing measures for team managers (FEAT-RPT-02, RWB-E1-030).
- Benefit realisation tracking against the baseline (FEAT-RPT-06, Epic 6).
- The decision log copy to the data lake (RWB-E1-014).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-013-baseline-measures-v1.md` |
| Requirement IDs | REQ-RDF-012 |
| BRD section | Business Requirements Epic 1, sections 3.8 and 4 |
| Decision | None |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, Tribe lead and squad members | Agrees the definitions; named as approver on each row; reads the report (Reporting R) |
| RW-REFADM, reference data administrator | Loads the definition file (Reference data C) |
| RW-BIANAL, Reporting and BI analyst | Builds the Power BI data set; reads the snapshot (Reporting CRUD) |
| RW-DATASTEW, data steward | Reads the run record and the freshness stamp (Reporting CRU) |
| RW-FINANCE, Finance and CFO delegate | Reads the baseline (Reporting R) |
| RW-PLATADM, platform administrator | Reruns JOB-15 from SCR-44 |

## Contract extract

No endpoint in Epic 1. GET /api/recovery/v1/reports/measures reads the snapshot from RWB-E2-009. **Job JOB-15 Reporting extract** | Item | Value | |---|---| | Trigger | Quartz, nightly 01:30 Asia/Bangkok | | Input | Case facts and payments of the previous business date; definitions in force | | Output | measure_snapshot rows; INT-19 extract files with business date, freshness stamp and trailer | | Events published | None (events.txt lists no P9 event) | | Idempotency key | Measure code, definition version, business date, product and dimension value (unique); frozen rows are skipped | | Restart | Rerun from SCR-44 for a business date; non-frozen rows of that date are replaced, frozen rows stay | **Published interfaces** ```java // Offered by P9 public interface MeasureCatalog { List<MeasureDefinition> inForce(LocalDate onDate); } // Called, owned elsewhere Stream<CaseFact> CaseReportingA…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: measures, formulas, age bands and the baseline date are data or configuration. - No personal data in logs, tests or prompts. The extract carries case IDs, codes, counts and amounts only; a field marked personal in sys_fields is never written. - No read of another module's tables. Case and payment facts come through the P3 and P1 reporting interfaces. - Frozen baseline rows are protected by a database trigger as well as by the service.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-013-baseline-measures-v1.md` |
| Specification | `output/INC-040-epic-1-RWB-E1-013/specify/spec.md` |
| Compliance validation | `output/INC-040-epic-1-RWB-E1-013/specify/compliance-validation.md` |
| Agent run log | `output/INC-040-epic-1-RWB-E1-013/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-040-epic-1-RWB-E1-013/plan/` |
| Implementation evidence | `output/INC-040-epic-1-RWB-E1-013/implement/` |
| API / functional test reports | `output/INC-040-epic-1-RWB-E1-013/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-040-epic-1-RWB-E1-013/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-013-baseline-measures-v1.md` |
| Output run | `output/INC-040-epic-1-RWB-E1-013/` |

