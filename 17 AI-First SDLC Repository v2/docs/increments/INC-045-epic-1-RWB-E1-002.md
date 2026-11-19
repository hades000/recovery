# Increment Card — INC-045-epic-1-RWB-E1-002

**RWB-E1-002 — Case list v1 with case ID, owner and queue**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-045` |
| Title | Case list v1 with case ID, owner and queue |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-002` |
| RUN_ID | `INC-045-epic-1-RWB-E1-002` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 45 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-018, RWB-E1-020, RWB-E1-069, RWB-E1-007, RWB-E1-015 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **team manager (RW-TEAMMGR)**, I want **one case list with case number, account, product, stage, status, owner, queue, route, total balance and days past due for every account at 90 days past due or more, built from the open cases and the ACE account view on each ACE business date and available in Power BI**, so that **every recovery team works from one list that is dated to the ACE batch it was built from**.

**Business outcome:** Each recovery team keeps its own list of accounts today, and the lists do not agree with each other or with the source. This story builds one case list each business date from the open cases and `v_ace_account`, with the account number, balance and days past due read live from ACE rather than copied, and publishes it to Power BI. The count is checked daily against ACE by REC-01 in RWB-E1-011, and a business key with no ACE row is listed by REC-05. It meets REQ-RDF-007 and serves the measure "case list built and released by 07:30 on 99 percent of days".

**Main flow:**
1. Quartz: JOB-04 Daily reconciliation reaches its case list step after JOB-03 completes for the business date, and only when the daily completeness gate of RWB-E1-015 reports COMPLETE for the sources the case list reads.
2. System: reads the business date and completion time of the ALS batch from `v_ace_batch_status` (source_system ALS, is_complete true).
3. System: reads the open case accounts from `CaseQueryApi.openCaseAccounts(businessDate)`, each with its `account_key`.
4. System: joins each account_key to `v_ace_account` for the account number (`account_code`), total balance and days past due, for the business date in `data_as_of`.
5. System: reads the latest contact and action code per account_key from `v_ace_efs_action`.
6. System: replaces the case_list_row rows for the business date in one transaction, each with the refresh time and publish status PENDING.

**Acceptance criteria:**
- AC1: List built and reconciled
- AC2: Columns present
- AC3: Daily refresh
- AC4: Last contact from EFS through ACE
- AC5: ACE batch not complete
- AC6: Allocation not finished
- AC7: Run repeated for the same date
- AC8: Case interface error
- AC9: Transfer to the lake fails
- AC10: Case account without an ACE account row
- AC11: Case list access refused

**Out of scope:**
- The reconciliation by product, the balance reconciliation, the break list and the hold of the publish (RWB-E1-011).
- The ACE batch gate and the freshness stamp (RWB-E1-015).
- The Workbench case list screen with queue and owner filters and export (RWB-E1-031).
- Row-level security by team in Power BI (RWB-E1-016).
- Queue measures and ageing (RWB-E1-030).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-002-case-list-v1-with-case-id-owner-and-queue-v1.md` |
| Requirement IDs | REQ-RDF-007 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| Decision | D6 entry; D-RCV-35 (U1, U4); ADR-010 |
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
| recovery_svc, recovery service identity | Runs the case list step; writes case_list_row and reads the ACE views |
| SY-CASEWF, case workflow module | Serves `CaseQueryApi` |
| RW-PLATADM, platform administrator | Lists the runs (Platform administration R) and restarts the step (Platform administration U) |
| RW-DATASTEW, RW-COE, RW-AUDIT, RW-COMPLY, RW-SECADM | List the runs (Platform administration R) |
| RW-BIANAL, reporting and BI analyst | Builds and schedules the Power BI data set (Reporting CRUD) |
| RW-TEAMMGR, RW-CASEOWN, RW-PHONECOL | Read the case list report in Power BI (Reporting R); row-level security by team follows RWB-E1-016 |

## Contract extract

**Job step** | Item | Value | |---|---| | Trigger | JOB-04 Daily reconciliation, case list step, chained after JOB-03 completes, or at 07:15 if JOB-03 has not completed; only when the daily completeness gate of RWB-E1-015 returns COMPLETE for the sources it reads | | Job name | JOB-04 Daily reconciliation | | Input | `CaseQueryApi.openCaseAccounts(businessDate)`; `v_ace_account`; `v_ace_efs_action`; `v_ace_batch_status`; parameters | | Output | case_list_row for the business date; check results ROWS_BELOW_ENTRY (count), ALLOCATION_COMPLETE (YES or NO), PUBLISHED (YES or NO); extract file `case-list/<businessDate>.csv` held for the publish step and sent to the data lake through the outbound adapter (INT-19) when publish_status is RELEASED | | Events published | None | | Idempotency key | business_date; the step deletes and inserts the rows of that date in one transaction | | Restart | A…

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

- No business value in code: the threshold, the tolerance and the wait time are parameters. - No personal data in logs, tests or prompts. The list holds no customer name, ID number or contact value. - No read of another module's tables. recovery_case, case_account and queue are read only through `CaseQueryApi`. - ACE data only through `recovery.v_ace_*` views; the step holds no copy of an account and no foreign key into ACE. - The extract file goes to the data lake only through the outbound file adapter.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-002-case-list-v1-with-case-id-owner-and-queue-v1.md` |
| Specification | `output/INC-045-epic-1-RWB-E1-002/specify/spec.md` |
| Compliance validation | `output/INC-045-epic-1-RWB-E1-002/specify/compliance-validation.md` |
| Agent run log | `output/INC-045-epic-1-RWB-E1-002/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-045-epic-1-RWB-E1-002/plan/` |
| Implementation evidence | `output/INC-045-epic-1-RWB-E1-002/implement/` |
| API / functional test reports | `output/INC-045-epic-1-RWB-E1-002/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-045-epic-1-RWB-E1-002/review/` |
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
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-002-case-list-v1-with-case-id-owner-and-queue-v1.md` |
| Output run | `output/INC-045-epic-1-RWB-E1-002/` |

