# Increment Card — INC-038-epic-1-RWB-E1-018

**RWB-E1-018 — Case ID issuance and case record v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-038` |
| Title | Case ID issuance and case record v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-018` |
| RUN_ID | `INC-038-epic-1-RWB-E1-018` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Build order | 38 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-016, RWB-E1-027, RWB-E1-042, RWB-E1-069, RWB-E1-072, RWB-E1-073 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow.

## Scope

**Story:** As a **product owner**, I want **every account at 90 days past due or more in the ACE account view that is not excluded placed on one recovery case per customer and product, with a case ID in the form RW-YYYY-NNNNNN issued at creation and never reused, a status and its linked accounts read from ACE by business key, created by rule when the ACE ALS batch for the business date is complete**, so that **every team, letter and document refers to one case ID**.

**Business outcome:** Recovery teams keep their own lists today, so one account can be on several trackers under different references, and some accounts at 90 days past due have no owner at all (control CTL-01 answers this audit finding). Under D-RCV-35 the Workbench loads nothing: ACE ingests the ALS account, the SCBPDM customer and the EFS collections history, and P3 reads them through `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation`. This story creates the case by rule when the ALS batch for the business date reaches COMPLETED in `v_ace_batch_status`, blocks excluded accounts with a logged reason, and gives the case an ID that every later document carries.

**Main flow:**
1. ACE: the ALS batch for business date 2026-12-01 completes, and `v_ace_batch_status` holds the row with status "COMPLETED" and `is_complete` true.
2. RWB-E1-015: raises AceDataReady (EV-26) for source ALS and business date 2026-12-01.
3. CaseCreationJob (JOB-02): starts on AceDataReady and reads the entry threshold parameter `case.entry.dpd`.
4. CaseCreationJob: reads `v_ace_account` for every account with `days_past_due` at or above 90 and `data_as_of` equal to the business date, and skips an account that already has an open `case_account` row (`linked_to` is null).
5. CaseCreationJob: for each account reads `v_ace_ca_relation` for the BORROWER `person_key` and `v_ace_customer` for that key; an account whose borrower key has no `v_ace_customer` row is not grouped and gets no case.
6. RuleEvaluator (SY-RULES): calls `RuleEvaluator.evaluate("EXCLUSION", facts, businessDate)` for each account over `v_ace_account.tdr_flag`, `v_ace_customer.deceased_flag`, `account_ext.dispute_open` and `party_ext`; an excluded account gets a `case_entry_exclusion` row with the reason code, the rule ID and the package version, and no case.

**Acceptance criteria:**
- AC1: Case created at 90 days past due
- AC2: Exclusion applied
- AC3: One case per customer and product
- AC4: ID never reused
- AC5: State model as data
- AC6: Exclusion rules as data
- AC7: The entry threshold boundary
- AC8: A repeated run creates nothing new
- AC9: No cases before the ALS batch is complete
- AC10: The decision log write fails
- AC11: The yearly number range is used up
- AC12: Two products give two cases
- AC13: A key with no view row is listed, never invented
- AC14: A role without Case record R is refused
- AC15: No EXCLUSION package in force holds creation

**Out of scope:**
- Allocation to a queue and an owner (RWB-E1-020).
- Prescription date at creation (RWB-E1-028).
- The EFS collections history hand-over in Epic 2 (RWB-E2-001); the history itself is read from `v_ace_efs_action`, not copied.
- Merging a duplicate case (R-UNI-17) and canceling a case created in error (R-UNI-16), Epic 2.
- The read-only case record view (RWB-E1-023).
- The load, approval and rollback of the ENTRY and EXCLUSION packages (RWB-E1-073).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-018-case-id-issuance-and-case-record-v1-v2.md` |
| Requirement IDs | REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CWC-004, REQ-CWC-005, REQ-CWC-016, REQ-CHO-004 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| Decision | D-RCV-36; ADR-011; ADR-012 |
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
| recovery_svc, recovery service identity | Runs JOB-02; reads `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status`; creates the case, the account links and the party link |
| ACE batch record | Raises AceDataReady; no case write in this story |
| SY-RULES | Evaluates the ENTRY and EXCLUSION packages through `RuleEvaluator` (Rules and parameters R) |
| SY-DECLOG | Writes the decision log entry (Decision log C) |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL and every role with Case record R | Read the case and its accounts, within their scope |
| RW-COE | Owns the ENTRY and EXCLUSION packages and the threshold parameter; loads the packages through RWB-E1-073 and the parameter through RWB-E1-042 |
| ACE team lead | Owns the ACE tables and columns behind `v_ace_account`, `v_ace_customer` and `v_ace_ca_relation`; reads no Workbench table |
| RW-REFADM | Has no Case record right; refused on the read endpoints |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | AceDataReady (EV-26) for source ALS and the business date, raised by RWB-E1-015 from a COMPLETED row in `v_ace_batch_status` | | Job name | JOB-02 Case creation (Quartz, D-RCV-36 T2) | | Schedule | Daily, when the ALS batch completes | | Input | Accounts at or above the threshold from `v_ace_account` for the business date; borrower `person_key` from `v_ace_ca_relation`; customer from `v_ace_customer`; `account_ext` and `party_ext` flags; ENTRY and EXCLUSION package versions in force on the business date, through `RuleEvaluator` (RWB-E1-072); exposure band table | | Output | recovery_case, case_account, case_party and case_entry_exclusion rows, the last with reason code, rule ID and package version; decision log entries; job record counts | | Events published | CaseCreated (EV-01: caseId, caseNo, productGroup, accounts, businessDate) | | Ide…

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

- No business value in code: the threshold, the exclusion reasons, the bands and the status list are data in the packages, the parameter catalog and the lists. - No personal data in logs, tests, workflow history or prompts. JOB-02 reads `account_key` and `person_key` only: no name, address or identity number is read or written. Test data uses synthetic account and customer keys only. - No read of another module's tables; ACE data only through `recovery.v_ace_*` views: account, customer, relation and batch data come from `v_ace_account`, `v_ace_customer`, `v_ace_ca_relation` and `v_ace_batch_status`. The recovery schema holds no foreign key into a `public` table. - One evaluator: ENTRY and EXCLUSION are evaluated only through `RuleEvaluator`; no code reads `drl_source`, the workbook or a rule_row row directly (D-RCV-36 T3, T6). - `case_entry_exclusion` stores the rule ID (Drools rule nam…

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-018-case-id-issuance-and-case-record-v1-v2.md` |
| Specification | `output/INC-038-epic-1-RWB-E1-018/specify/spec.md` |
| Compliance validation | `output/INC-038-epic-1-RWB-E1-018/specify/compliance-validation.md` |
| Agent run log | `output/INC-038-epic-1-RWB-E1-018/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-038-epic-1-RWB-E1-018/plan/` |
| Implementation evidence | `output/INC-038-epic-1-RWB-E1-018/implement/` |
| API / functional test reports | `output/INC-038-epic-1-RWB-E1-018/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-038-epic-1-RWB-E1-018/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 15 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-018-case-id-issuance-and-case-record-v1-v2.md` |
| Output run | `output/INC-038-epic-1-RWB-E1-018/` |

