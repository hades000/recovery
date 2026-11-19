# Increment Card — INC-054-epic-1-RWB-E1-006

**RWB-E1-006 — Data quality rules v1**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-054` |
| Title | Data quality rules v1 |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-006` |
| RUN_ID | `INC-054-epic-1-RWB-E1-006` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | No |
| Depends on | RWB-E1-002, RWB-E1-003, RWB-E1-043 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **ten data quality rules (missing owner, duplicate account, days past due mismatch, stale balance, missing collateral link and five more) run on every load, with a reason code on every failed row**, so that **the case list can be trusted**.

**Main flow:**
1. System: a load completes for a data product (for example INT-01 for DP01), or the case list step of JOB-04 completes for DP03.
2. System: reads the dq_rule rows in force for that data product on the business date.
3. System: builds the SQL for each rule from its rule type template and its parameters, using only table and column names that sys_fields holds for P1-owned tables.
4. System: runs each rule and collects the failing records.
5. System: writes one dq_exception row per failing record with the rule code as check and reason code, the rule version, the record key and the business date.
6. System: sets CLEARED on any OPEN exception of the same rule and record that no longer fails.

**Out of scope:**
- Working a data quality break to closure with an owner and a date (FEAT-RPT-09, Epic 2).
- The Data quality screen SCR-45 (Epic 2).
- The daily reconciliation to ALS (RWB-E1-011).
- Merging duplicate cases (R-UNI-17, P3).
- Rules on tables owned by other modules, which those modules run in their own stories.

**Business outcome and value hypothesis:** Today a wrong owner, an account on two cases or a balance that does not add up is found only when a case owner works the case. This story runs ten row-level rules, held as versioned data rows, after every load and after the daily case list build, and writes each failed row with its rule code to the exception list that the data steward and Power BI read. It meets REQ-RDF-008 and serves the data quality measures completeness 99.9 percent, validity 99.5 percent and uniqueness 100 percent.

**Constraints and guardrails:**
- No business value in code: rules, thresholds and product lists are rule rows and parameters; only the seven rule type templates are code.
- No personal data in logs, tests or prompts. record_key holds account keys or record IDs, never names or contact values.
- No read of another module's tables. Rules on case data read case_list_row, which P1 builds from the P3 published interface.
- No rule text is executed as SQL: identifiers come from sys_fields and values are bound parameters.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 006 Data quality rules v1 v1.md` |
| Requirement IDs | REQ-RDF-008 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
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
| SY-DATALOAD, data load from COLLINS | Runs the rules; writes dq_exception and the load_run results |
| RW-REFADM, reference data administrator | Loads a rule version (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Approves a rule version as its owner; reads exceptions (Platform administration R) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read exceptions (Platform administration R) |
| RW-BIANAL, reporting and BI analyst | Builds the Power BI data quality report (Reporting CRUD) |

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
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p1.dq-rules`. Off: no rule runs; loads complete as before.
- **Critical path:** No; **depends on:** RWB-E1-002, RWB-E1-003, RWB-E1-043.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: rules, thresholds and product lists are rule rows and parameters; only the seven rule type templates are code.
  - No personal data in logs, tests or prompts. record_key holds account keys or record IDs, never names or contact values.
  - No read of another module's tables. Rules on case data read case_list_row, which P1 builds from the P3 published interface.
  - No rule text is executed as SQL: identifiers come from sys_fields and values are bound parameters.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 006 Data quality rules v1 v1.md` |
| Specification | `output/INC-054-epic-1-RWB-E1-006/specify/spec.md` |
| Compliance validation | `output/INC-054-epic-1-RWB-E1-006/specify/compliance-validation.md` |
| Agent run log | `output/INC-054-epic-1-RWB-E1-006/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-054-epic-1-RWB-E1-006/plan/` (TBC) |
| Implementation evidence | `output/INC-054-epic-1-RWB-E1-006/implement/` (TBC) |
| API / functional test reports | `output/INC-054-epic-1-RWB-E1-006/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-054-epic-1-RWB-E1-006/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-054-epic-1-RWB-E1-006/specify/compliance-validation.md`) |
| Acceptance criteria | 9 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC9) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 006 Data quality rules v1 v1.md` |
| Output run | `output/INC-054-epic-1-RWB-E1-006/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
