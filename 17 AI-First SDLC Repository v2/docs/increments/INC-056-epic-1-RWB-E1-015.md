# Increment Card — INC-056-epic-1-RWB-E1-015

**RWB-E1-015 — Freshness stamp per data product**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-056` |
| Title | Freshness stamp per data product |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-015` |
| RUN_ID | `INC-056-epic-1-RWB-E1-015` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 56 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-069, RWB-E1-027 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **every data product to carry the business date, start time, completion time and status of the ACE batch it came from, exposed to every consumer and shown on the case record view, and every daily data job to start only when the sources it reads are complete for the business date**, so that **every decision input states how old it is, stale facts are visible, and no list is built from a half-loaded day**.

**Business outcome:** The Workbench loads no source data; ACE does (D-RCV-35 U1). A fact on the case can therefore be one day or one week old, and the Workbench cannot time its own load. ACE writes one `ace_batch_run` row per source and business date and the Workbench reads it through `v_ace_batch_status`. A stamp per product and business date, shown on the case record and copied into each decision's inputs snapshot, makes the age of every input visible to the person deciding and to audit. A product whose batch has not completed by its cut-off is flagged stale the same morning. The same reading closes the daily gate that the retired load checks used to provide: no data job for a business date starts until every source it reads is COMPLETED. Serves REQ-RDF-009; measure: the ACE batch is complete when the Workbench reads it on 99 percent of days.

**Main flow:**
1. System: reads `v_ace_batch_status`, one row per source system and business date, for a new or changed COMPLETED row.
2. FreshnessStampService: reads the product-to-source map (section 12) and, in one transaction, writes or updates one data_product_load row for each product the source feeds, with the business date, `source_extracted_at` from `started_at`, `loaded_at` from `completed_at` and status LOADED.
3. System: for a product fed by more than one source, sets the stamp to the oldest business date among its sources and marks it STALE while any of them is late.
4. System: at each product's `expected_by` time, checks that a COMPLETED row exists in `v_ace_batch_status` for the expected business date.
5. System: for a product with no COMPLETED row, marks its latest stamp in use (the previous complete business date) STALE with `stale_flagged_at`, publishes EV-27 AceDataLate and sends the operations alert. No row is written for a business date with no batch, because the stamp needs the source start and completion times.
6. System: on a FAILED batch row, marks the product STALE at once; the stamp for the last complete business date stays the one in use.

**Acceptance criteria:**
- AC1: Freshness from the ACE batch
- AC2: Stale product flagged at the cut-off
- AC3: Freshness in the decision log
- AC4: A failed ACE batch marks the product stale at once
- AC5: The same batch read twice
- AC6: A late batch clears the stale flag
- AC7: A batch one minute before the expected-by time
- AC8: A weekly product between its batches
- AC9: Daily completeness gate holds the case list
- AC10: Daily completeness gate releases when every source is complete
- AC11: A product fed by several sources

**Out of scope:**
- The MSG-P7-006 warning on a decision screen when an input is past its age limit (decision screens, Epic 2).
- Same-day data for named triggers (DL06).
- The data quality console SCR-45 (Epic 2) and the reconciliation report (RWB-E1-011).
- Freshness of the stage 2 data products (RWB-E2-010).
- ACE's own ingestion monitoring and its alerting (RWB-ACE-001).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-015-freshness-stamp-per-data-product-v1.md` |
| Requirement IDs | REQ-RDF-009 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-009) |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 open |
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
| recovery_svc, recovery service identity | Reads the batch view; writes data_product_load; marks products stale; publishes EV-26 and EV-27; runs the daily gate |
| SY-DECLOG, decision log writer | Reads stamps through FreshnessQuery for the inputs snapshot |
| RW-DATASTEW, data steward | Reads stamps and the gate result (Platform administration R); receives the stale alert |
| RW-PLATADM, platform administrator | Reads stamps and the gate result; receives the operations alert |
| Case roles with Case record R, for example RW-CASEOWN, RW-TEAMMGR | Read the stamp in the case record data panel |

## Contract extract

**Endpoints** | Item | Value | |---|---| | Method and path | GET /data-products/freshness | | Request | Query: product (optional, DP01 to DP14), asOf (optional, business date) | | Response | DataProductFreshness[]: productCode, productName, businessDate, sourceExtractedAt, loadedAt, status (LOADED or STALE), staleSince | | Errors | 400 malformed product or date (MSG-GEN-001); 401 no session (MSG-P4-001); 403 role lacks the right (MSG-P4-002); 503 store down (MSG-GEN-006) | | Authorization | Case record, R. No case scope applies: the stamp holds no case data | | Idempotency | Not applicable | | Item | Value | |---|---| | Method and path | GET /data/freshness | | Request | Query: sourceSystem (optional), businessDate (optional) | | Response | DataFreshness[]: sourceSystem, businessDate, startedAt, completedAt, status, recordCount, feedVersion, isComplete, ageDays | | Authorization | Case…

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

- No business value in code: expected-by times, cycles, the product-to-source map and the alert channel are data rows or properties. - No personal data in logs, tests or prompts; stamps carry product codes, source codes and times only. - No read of another module's tables: P3 and P7 read stamps only through FreshnessQuery; this story writes no P7 table. - ACE data only through `recovery.v_ace_*` views; the story never reads `public.ace_batch_run` directly and writes nothing to ACE. - The stale check never deletes or changes a loaded row; the previous complete business date stays in use.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-015-freshness-stamp-per-data-product-v1.md` |
| Specification | `output/INC-056-epic-1-RWB-E1-015/specify/spec.md` |
| Compliance validation | `output/INC-056-epic-1-RWB-E1-015/specify/compliance-validation.md` |
| Agent run log | `output/INC-056-epic-1-RWB-E1-015/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-056-epic-1-RWB-E1-015/plan/` |
| Implementation evidence | `output/INC-056-epic-1-RWB-E1-015/implement/` |
| API / functional test reports | `output/INC-056-epic-1-RWB-E1-015/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-056-epic-1-RWB-E1-015/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-015-freshness-stamp-per-data-product-v1.md` |
| Output run | `output/INC-056-epic-1-RWB-E1-015/` |

