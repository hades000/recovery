# Increment Card — INC-040-epic-1-RWB-E1-018

**RWB-E1-018 — Case ID issuance and case record v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-040` |
| Title | Case ID issuance and case record v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-018` |
| RUN_ID | `INC-040-epic-1-RWB-E1-018` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P3 Case and workflow |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-016, RWB-E1-027, RWB-E1-042 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P3 Case and workflow. **Build group:** P3a.

## Scope

**Story:** As a **product owner**, I want **every account at 90 days past due or more that is not excluded placed on one recovery case per customer and product, with a case ID in the form RW-YYYY-NNNNNN issued at creation and never reused, a status and its linked accounts, created by rule from the daily load**, so that **every team, letter and document refers to one case ID**.

**Main flow:**
1. JOB-01: publishes LoadCompleted for source COLLINS and business date 2026-12-01.
2. CaseCreationJob (JOB-02): starts on LoadCompleted and reads the entry threshold parameter `case.entry.dpd`.
3. CaseCreationJob: asks the P1 interface for every account with days_past_due at or above 90 on the business date that has no open case link.
4. EntryRuleEvaluator (SY-RULES): evaluates the exclusion rows in force for each account; an excluded account gets an exclusion record with the reason code, rule ID and version, and no case.
5. CaseGrouping: groups the remaining accounts by primary customer and product group; an existing open case for the same pair receives the new account link instead of a new case.
6. CaseNumberIssuer: takes the next number from the sequence for the entry year and formats RW-2026-000123.

**Out of scope:**
- Allocation to a queue and an owner (RWB-E1-020).
- Prescription date at creation (RWB-E1-028).
- Hand-over of collections history from EFS (RWB-E2-001).
- Merging a duplicate case (R-UNI-17) and canceling a case created in error (R-UNI-16), Epic 2.
- The read-only case record view (RWB-E1-023).

**Business outcome and value hypothesis:** Recovery teams keep their own lists today, so one account can be on several trackers under different references, and some accounts at 90 days past due have no owner at all (control CTL-01 answers this audit finding). This story creates the case by rule the morning after the account reaches 90 days past due, blocks excluded accounts with a logged reason, and gives the case an ID that every later document carries. It meets REQ-CWC-001 to REQ-CWC-005 and REQ-CWC-016, and supports reconciliation REC-01 (accounts at 90 days past due against open cases, zero unexplained).

**Constraints and guardrails:**
- No business value in code: the threshold, the exclusion reasons, the bands and the status list are data.
- No personal data in logs, tests, events or prompts. Test data uses synthetic account and customer IDs only.
- No read of another module's tables: account and party data come through RecoveryDataQuery (P1); rules through RuleTableReader (P4).
- The case number is printed on every outbound document; other modules take it from CaseRecordService, never from a copy.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 018 Case ID issuance and case record v1 v1.md` |
| Requirement IDs | REQ-CWC-001, REQ-CWC-002, REQ-CWC-003, REQ-CWC-004, REQ-CWC-005, REQ-CWC-016, REQ-CHO-004 |
| BRD section | Business Requirements Epic 1, section 3.3; Business Requirements Program, section 5.3 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| SY-DATALOAD | Publishes LoadCompleted; no case write in this story |
| SY-CASEWF | Creates the case, the account links and the party link (Case record CRU) |
| SY-RULES | Evaluates the exclusion rows (Rules and parameters R) |
| SY-DECLOG | Writes the decision log entry (Decision log C) |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL and every role with Case record R | Read the case and its accounts, within their scope |
| RW-COE | Owns the exclusion rows and the threshold parameter; loads them through RWB-E1-029 and RWB-E1-042 |
| RW-REFADM | Has no Case record right; refused on the read endpoints |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p3.casecreation`. Off: JOB-02 does not create cases.
- **Critical path:** Yes; **depends on:** RWB-E1-016, RWB-E1-027, RWB-E1-042.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: the threshold, the exclusion reasons, the bands and the status list are data.
  - No personal data in logs, tests, events or prompts. Test data uses synthetic account and customer IDs only.
  - No read of another module's tables: account and party data come through RecoveryDataQuery (P1); rules through RuleTableReader (P4).
  - The case number is printed on every outbound document; other modules take it from CaseRecordService, never from a copy.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 018 Case ID issuance and case record v1 v1.md` |
| Specification | `output/INC-040-epic-1-RWB-E1-018/specify/spec.md` |
| Compliance validation | `output/INC-040-epic-1-RWB-E1-018/specify/compliance-validation.md` |
| Agent run log | `output/INC-040-epic-1-RWB-E1-018/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-040-epic-1-RWB-E1-018/plan/` (TBC) |
| Implementation evidence | `output/INC-040-epic-1-RWB-E1-018/implement/` (TBC) |
| API / functional test reports | `output/INC-040-epic-1-RWB-E1-018/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-040-epic-1-RWB-E1-018/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — regated 2026-11-06: clarifications resolved by the D-RCV rulings; gate-002 compliance PASS |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-040-epic-1-RWB-E1-018/specify/compliance-validation.md`) |
| Acceptance criteria | 12 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9, AC10, AC11, AC12) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 018 Case ID issuance and case record v1 v1.md` |
| Output run | `output/INC-040-epic-1-RWB-E1-018/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
