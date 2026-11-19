# Increment Card — INC-017-epic-1-RWB-E1-017

**RWB-E1-017 — Retention and archive rule for the data store**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-017` |
| Title | Retention and archive rule for the data store |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-017` |
| RUN_ID | `INC-017-epic-1-RWB-E1-017` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Should |
| Build order | 17 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-043, RWB-TE-012, RWB-E1-064 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **Compliance and PDPA officer (RW-COMPLY)**, I want **a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action**, so that **the store holds what the policy allows and nothing older**.

**Business outcome:** PDPA and the bank retention schedule limit how long personal data is kept, and today recovery records stay in spreadsheets and systems with no end date. A retention rule per data product and table, loaded as versioned data, lets Compliance set and change periods without a release. A monthly job archives rows past their period to a write-once archive container and removes them from the live store, keeps every row of a case under legal hold, and records what it did. Serves REQ-RDF-013 and the retention requirements NFR-031 and NFR-072.

**Main flow:**
1. Reference data administrator: loads a retention rule version through POST /admin/reference-loads with table retention_rule; the owner approves it.
2. RetentionRuleLoader: validates the rows (known product, known table in sys_objects, months between 1 and 600, table not decision_log_entry) and stores the version.
3. Quartz: starts JOB-17 Retention job on the first Sunday of the month.
4. RetentionService: reads the rules in force on the run date.
5. RetentionService: calls CaseHoldQuery.casesOnLegalHold() and excludes every row of those cases.
6. RetentionService: selects, per rule, the rows whose age-basis field is older than the run date minus the retention months.

**Acceptance criteria:**
- AC1: Retention rule applied
- AC2: Rule changed as data
- AC3: Legal hold
- AC4: A rule with months outside the allowed range
- AC5: The archive write fails
- AC6: A repeat run in the same month
- AC7: A row exactly at its retention age
- AC8: A rule for the decision log is refused
- AC9: A rerun while the job is running

**Out of scope:**
- Retention classes for documents and the document legal hold (RWB-E1-041).
- The retention class for ledger entries as its own reference row (FEAT-ILG-10, RWB-E2-034).
- The decision log retention period (NFR-030, DL26) and the lake copy (RWB-E1-014).
- Closing a case after its retention period (REQ-S7-008, Epic 6).
- The personal data screen SCR-47 (Epic 8).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-017-retention-and-archive-rule-for-the-data-store-v1.md` |
| Requirement IDs | REQ-RDF-013 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-013) |
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
| RW-COMPLY, Compliance and PDPA officer | Owns the retention periods; reads the run result (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the retention load (Reference data C) |
| Holder of Reference data A | Approves the retention load |
| RW-DATASTEW, data steward | Reads the run result for their products |
| RW-PLATADM, platform administrator | Reruns JOB-17 (Platform administration U) |
| SY-DATALOAD, data load | Runs JOB-17, writes the archive, deletes archived rows |
| SY-CASEWF, case workflow module | Answers CaseHoldQuery |

## Contract extract

**Job** | Item | Value | |---|---| | Trigger | Quartz cron `0 30 2 ? * SUN#1`, Asia/Bangkok | | Job name | JOB-17 Retention job | | Schedule | Monthly, first Sunday | | Input | Retention rules in force on the run date; rows of each named table; legal hold cases from CaseHoldQuery | | Output | Archive files and manifest under `retention/YYYY-MM-DD/<table>/` in the write-once container; deleted live rows; job run checks with counts per product and table, rule version, archive location and the hold report; summary alert MSG-P1-020 to Compliance | | Events published | None | | Idempotency key | Run date and rule version. Selection reads live rows, so a rerun finds only rows not yet archived | | Restart behavior | Each table and rule is one unit: archive, check, delete. A failure before the delete leaves the live rows; a rerun repeats the unit. A failure after the delete leaves a complete ar…

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

- No business value in code: periods, tables, age-basis fields and the archive location are data rows or properties. - No personal data in logs, tests or prompts: the job run and the hold report carry counts and case numbers only; test rows are synthetic. - No read of another module's tables: legal hold comes from CaseHoldQuery. - The decision log is never archived or deleted by this job, and no row is deleted before its archive copy is checked.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-017-retention-and-archive-rule-for-the-data-store-v1.md` |
| Specification | `output/INC-017-epic-1-RWB-E1-017/specify/spec.md` |
| Compliance validation | `output/INC-017-epic-1-RWB-E1-017/specify/compliance-validation.md` |
| Agent run log | `output/INC-017-epic-1-RWB-E1-017/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-017-epic-1-RWB-E1-017/plan/` |
| Implementation evidence | `output/INC-017-epic-1-RWB-E1-017/implement/` |
| API / functional test reports | `output/INC-017-epic-1-RWB-E1-017/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-017-epic-1-RWB-E1-017/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 9 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-017-retention-and-archive-rule-for-the-data-store-v1.md` |
| Output run | `output/INC-017-epic-1-RWB-E1-017/` |

