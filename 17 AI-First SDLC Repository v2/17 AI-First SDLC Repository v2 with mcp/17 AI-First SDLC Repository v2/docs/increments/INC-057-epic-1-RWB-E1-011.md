# Increment Card — INC-057-epic-1-RWB-E1-011

**RWB-E1-011 — Reconciliation and data quality report**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-057` |
| Title | Reconciliation and data quality report |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-011` |
| RUN_ID | `INC-057-epic-1-RWB-E1-011` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 57 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-002, RWB-E1-015, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **a daily reconciliation of the case list to `v_ace_account`, of every business key on a Workbench table to its ACE view, and of treatments and payments to their ACE records, with the variance by product and the data quality results in one Power BI report**, so that **everyone sees whether today's case list and its links can be trusted**.

**Business outcome:** No one can say today whether the recovery teams' lists cover every account at 90 days past due, so missing accounts are found late or not at all. This story runs the five daily reconciliations REC-01 to REC-05 every business date: the account count and the balance by product against `v_ace_account`, approved treatments against `v_ace_plan`, payments against proceeds, and every business key on a Workbench table against the view that holds it. It lists every account or key that breaks, holds the publish of the case list when a product is outside the tolerance, and publishes the result with the data quality measures in one report. It meets REQ-RDF-007 and REQ-RDF-008, applies control CTL-01, and serves the accuracy measure "reconciliation breaks cleared within one day, 100 percent". No reconciliation runs against a source load: the Workbench loads nothing, and the ACE side of every check is a read-only view.

**Main flow:**
1. System: JOB-04 Daily reconciliation runs its reconciliation step after the case list step for the business date, on a COMPLETE gate result for the sources it reads.
2. System: reads the business date and completion time of the ALS batch from `v_ace_batch_status`, and uses that one business date for every check.
3. System: REC-01, for each product group, counts the accounts in `v_ace_account` at or above the entry threshold with `data_as_of` equal to the business date, less the accounts in `case_entry_exclusion` for the date, and counts the case_list_row rows at or above the threshold.
4. System: REC-02, for each product group, sums `v_ace_account.total_balance` and case_list_row.total_balance.
5. System: REC-03 counts approved restructure treatments whose case plan is not booked in `v_ace_plan` after two business days, and sums the offer amount.
6. System: REC-04 matches `v_ace_payment` rows of the business date to proceeds by `payment_code`, and counts and sums what is unmatched after one business day.

**Acceptance criteria:**
- AC1: Variance under limit
- AC2: Variance over limit
- AC3: Variance equal to the tolerance
- AC4: ACE batch not complete
- AC5: Rerun after a fix
- AC6: Two runs for the same date
- AC7: Business key without an ACE row
- AC8: View unavailable during the run

**Out of scope:**
- Working a break to closure with an owner and a date, and releasing a held publish by hand (FEAT-RPT-09 full scope, Epic 2).
- Reconciliation of write-offs (REC-06), assets taken on (REC-07), the decision log copy (REC-08, RWB-E1-014) and notice barcodes (REC-09, RWB-E1-055).
- Cross-source case count reconciliation in the reporting module (FEAT-RPT-05 full scope, Epic 2).
- The data quality console SCR-45 and the quality measure definitions (Epic 2 and Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-011-reconciliation-and-data-quality-report-v1.md` |
| Requirement IDs | REQ-RDF-007, REQ-RDF-008 |
| BRD section | Business Requirements Epic 1, sections 3.1 and 3.8; Business Requirements Program, section 5.1 |
| Decision | D-RCV-35 (U4); ADR-010 |
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
| recovery_svc, recovery service identity | Runs the reconciliation; writes reconciliation_result and the publish status; reads the ACE views |
| RW-DATASTEW, data steward and data product owner | Reads results and break rows (Platform administration R); signs the daily reconciliation to ACE |
| RW-PLATADM, platform administrator | Reads results; restarts the step (Platform administration U) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | Read results and break rows (Platform administration R) |
| RW-TEAMMGR, RW-BIANAL and other report readers | Read the Power BI report (Reporting R); RW-BIANAL builds it (Reporting CRUD) |

## Contract extract

**Job step** | Item | Value | |---|---| | Trigger | JOB-04 Daily reconciliation, reconciliation step, after the case list step and before the publish step | | Job name | JOB-04 Daily reconciliation | | Input | `v_ace_account`; case_list_row; case_entry_exclusion; treatment; `v_ace_plan`; `v_ace_payment`; proceeds; `v_ace_customer`, `v_ace_asset` and `v_ace_contact` for REC-05; `v_ace_batch_status`; parameters | | Output | reconciliation_result (REC-01 to REC-05); case_list_row.publish_status; extracts `reconciliation/<businessDate>.csv` and `data-quality/<businessDate>.csv` to the data lake through the outbound adapter (INT-19) | | Events published | None | | Idempotency key | rec_code, business_date and product_group (unique) | | Restart | The platform administrator restarts JOB-04 for the business date from the scheduler console; the step replaces the date's results | **Published inte…

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

- No business value in code: the tolerance, the waiting periods and the threshold are parameters. - No personal data in logs, tests or prompts. Break rows carry account keys, account numbers and business keys only. - No read of another module's tables. Exclusions come through `CaseQueryApi`; open case accounts come from case_list_row. - ACE data only through `recovery.v_ace_*` views; a break never changes an ACE row or a Workbench row. - A held case list is never published by hand from this story.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-011-reconciliation-and-data-quality-report-v1.md` |
| Specification | `output/INC-057-epic-1-RWB-E1-011/specify/spec.md` |
| Compliance validation | `output/INC-057-epic-1-RWB-E1-011/specify/compliance-validation.md` |
| Agent run log | `output/INC-057-epic-1-RWB-E1-011/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-057-epic-1-RWB-E1-011/plan/` |
| Implementation evidence | `output/INC-057-epic-1-RWB-E1-011/implement/` |
| API / functional test reports | `output/INC-057-epic-1-RWB-E1-011/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-057-epic-1-RWB-E1-011/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-011-reconciliation-and-data-quality-report-v1.md` |
| Output run | `output/INC-057-epic-1-RWB-E1-011/` |

