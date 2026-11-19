# Technical Specification — RWB-E1-029 Rule load, validation and rollback

| Field | Value |
|---|---|
| Story | RWB-E1-029 — Rule load, validation and rollback |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-019-epic-1-RWB-E1-029` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 029 Rule load validation and rollback v1.md` |
| Upstream IDs | BRD-RWB-003, BRD-RWB-020; FR-RWB-008; REQ-CWC-013, REQ-CWC-014, REQ-DRI-004; US-RWB-E1-029; CTX-FEATURE-003; CTL-08; R-UNI-38; DL24 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Rule versions are loaded by file and read through the API; SCR-39 is Epic 8. |
| Logic In Scope | `YES` — template parsing, five checks, test runner, dry run, version state, approval, effective dating, rollback and change log. |
| API In Scope | `YES` — this story first delivers `POST/GET /admin/rule-versions`, `POST /admin/rule-versions/{versionId}/approve` and `POST /admin/rule-versions/{versionId}/rollback` (P4). The contract is in API Specification v2; no OpenAPI delta. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | P4 `rule_row` and `rule_version`; rule evaluator (SY-RULES); change log; SCR-39 (Epic 8, not built here). |
| New Nodes Required | `YES` — `RuleTemplateParser`, `RuleLoadValidator`, `RuleTestRunner`, `RuleDryRun`, `RuleVersionController`, `RuleVersionService`, `RuleEffectiveDateJob`, `rule_version` and three `rule_row` columns. |
| Inherited Existing Behavior | RWB-E1-044 migrations; RWB-E1-042 parameter `rules.testcases.min`; RWB-TE-005 harness; P4 lists; RWB-E1-048 change log. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A version passes schema, overlap, unreachable row, default row and test case checks before it is stored. | SPEC-RWB-E1-029-002..006 | DIRECT | Checks run in that order; any failure refuses the load whole. | COVERED |
| BR2 | A load with any failed check is refused in full. | SPEC-RWB-E1-029-008 | DIRECT | No version, no rows and no partial write. | COVERED |
| BR3 | Hit policy Unique: for one table, trigger and row order, one condition holds. | SPEC-RWB-E1-029-003 | DIRECT | Overlap check; two matching rows at one order is a failure. | COVERED |
| BR4 | The allocation table always has a default row. | SPEC-RWB-E1-029-005 | DIRECT | Last row must match every case; ALLOCATION only. | COVERED |
| BR5 | A version takes effect on its valid from date after approval; open cases keep the version they were decided under. | SPEC-RWB-E1-029-010 | DIRECT | `RuleEffectiveDateJob` at 00:01; decision log keeps the version. | COVERED |
| BR6 | The author cannot approve; Risk signs rule version changes. | SPEC-RWB-E1-029-009 | DIRECT | RW-RISK holds Rules and parameters A; separation of duty. | COVERED |
| BR7 | Rollback returns the previous version in one call. | SPEC-RWB-E1-029-011 | DIRECT | One transaction; previous version IN_FORCE. | COVERED |
| BR8 | Every load, approval and rollback is in the change log with author, approver, time and test result. | SPEC-RWB-E1-029-012 | DIRECT | `rule_version` header and change log entry. | COVERED |
| AC1 | A valid 26-row, 50-test load is approved and in force from 2026-12-15; the change log records both users, times, 50/50 and the dry run count. | SPEC-RWB-E1-029-007..010, SPEC-RWB-E1-029-012 | DIRECT | ALLOC-2026.12. | COVERED |
| AC2 | Two rows matching at row order 12 refuse the load naming both. | SPEC-RWB-E1-029-003 | DIRECT | ALLOC-031 and ALLOC-032; previous version stays. | COVERED |
| AC3 | Failing test cases TA-07 and TA-19 refuse the load naming both. | SPEC-RWB-E1-029-006 | DIRECT | Expected MTG-BKK-CO, actual MTG-CEN-CO. | COVERED |
| AC4 | Rollback of version 7 returns version 6; the change log records it; a case allocated under version 7 keeps that version. | SPEC-RWB-E1-029-010..012 | DIRECT | Previous version IN_FORCE; decision log unchanged. | COVERED |
| AC5 | A value outside its list refuses the load naming row and column. | SPEC-RWB-E1-029-002 | DIRECT | Row 9, reason QUICK. | COVERED |
| AC6 | A row covered by an earlier row refuses the load naming it. | SPEC-RWB-E1-029-004 | DIRECT | ALLOC-040 covers ALLOC-041. | COVERED |
| AC7 | No default row refuses the load. | SPEC-RWB-E1-029-005 | DIRECT | ALLOCATION only. | COVERED |
| AC8 | The author cannot approve; the version stays LOADED. | SPEC-RWB-E1-029-009 | DIRECT | MSG-P7-002. | COVERED |
| AC9 | Rollback with no earlier version is refused and the current version stays in force. | SPEC-RWB-E1-029-011 | DIRECT | TRANSFER TRF-2026.11; MSG-P3-015. | COVERED |
| AC10 | The same version label loaded twice is refused with 409. | SPEC-RWB-E1-029-013 | DIRECT | MSG-GEN-004. | COVERED |
| AC11 | A valid from before today is refused with 422. | SPEC-RWB-E1-029-014 | DIRECT | MSG-GEN-003. | COVERED |
| AC12 | An empty file is refused with 422. | SPEC-RWB-E1-029-001 | DIRECT | MSG-GEN-001 names `rows`. | COVERED |
| X1..X11 | Exceptional paths in the table below map to SPEC-002..014 and the access rule. | SPEC-RWB-E1-029-002..014 | DIRECT | Overlap, test, schema, unreachable, default, author, rollback, duplicate, past date, empty, access. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **an Excel template for the five rule tables, validation on load (schema, overlaps, unreachable rows, missing default, 50 test cases and a dry run), a load with a version, approval, rollback by one call and a change log**, so that **a rule change goes from template to production without a code release**.

The story is the rule-administration capability for Epic 1. It covers ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (DL24, option A), refuses a bad table whole, records who loaded and approved it, and makes a rollback a single call. It adds no screen; the file is the interface.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | `POST /admin/rule-versions` with the Rules and Tests sheets; `POST /admin/rule-versions/{versionId}/approve`; `POST /admin/rule-versions/{versionId}/rollback`; daily `RuleEffectiveDateJob` at 00:01 Asia/Bangkok. |
| Preconditions | The five Epic 1 rule tables are agreed (DL24); each has 50 test cases in the Tests sheet; loader holds RW-COE; approver holds RW-RISK; live cases exist for the dry run (RWB-E1-018); RWB-TE-005 harness is available. |
| Input | XLSX template, `routeSet=UNIVERSAL_RULES`, `validFrom`, caller identity. |
| Output | `rule_version` and `rule_row` rows; validation report; dry run counts; change log entry; version in force. |
| Feature flag | `rwb.p3.ruleload`. Off: the load and rollback endpoints return 404; the version in force stays. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `rule_version` | `rule_table`, `version_label` | Template | New row only | Unique (rule_table, version_label); label format `ALLOC-YYYY.NN`. |
| `rule_version` | `status` | Service | LOADED → APPROVED → IN_FORCE → SUPERSEDED / ROLLED_BACK; REFUSED | One state at a time; only the effective-date job moves APPROVED to IN_FORCE. |
| `rule_version` | `author_user_id`, `approver_user_id`, `loaded_at`, `approved_at` | Session | System-managed | Approver must differ from author. |
| `rule_version` | `valid_from`, `test_result`, `dry_run_counts` | Template / service | System-managed | Test result 50/50 or the failing IDs; dry run counts by product and queue. |
| `rule_row` | `rule_table`, `row_order`, `target_queue_code` | Template | New row only | New columns; `row_order` is unique within a table and version. |
| `rule_row` | `rule_id`, `from_state`, `event_code`, `condition_expr`, `to_state`, `owner_role`, `timer_spec`, `test_case_id` | Template | New row only | Schema checked against LOV lists; `test_case_id` required. |
| Change log | author, approver, times, check result, dry run, rollback reason | Service | Append-only | Read through RWB-E1-048. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Load | Every check passes | LOADED | Rows and header written; change log entry. |
| None | Load | Any check fails | REFUSED | No rows stored; failing rows/tests named. |
| LOADED | Approve | Approver not author, holds A | APPROVED | Approver and time recorded. |
| APPROVED | `RULE_VERSION_EFFECTIVE` | Valid from reached | IN_FORCE | Previous version SUPERSEDED; engines read the new rows. |
| IN_FORCE | Rollback | Earlier version exists | ROLLED_BACK | Previous version IN_FORCE; reason recorded. |

This story changes no case status.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Two rows match at one row order | Load refused; both row IDs named | MSG-P3-027 |
| X2 | A test result differs from expected | Load refused; failing test case IDs named | MSG-P3-027 |
| X3 | Required column missing or value outside its list | Load refused; row and column named | MSG-P3-027 |
| X4 | A row can never match because an earlier row covers it | Load refused; row named | MSG-P3-027 |
| X5 | Allocation table has no default row | Load refused | MSG-P3-027 |
| X6 | Approver is the author | Approval refused; version stays LOADED | MSG-P7-002 |
| X7 | Rollback with no earlier version | Refused; current version stays | MSG-P3-015 |
| X8 | Same version label loaded twice | Refused with 409 | MSG-GEN-004 |
| X9 | Valid from before today | Refused with 422 | MSG-GEN-003 |
| X10 | Empty file | Refused with 422 | MSG-GEN-001 |
| X11 | Role without Rules and parameters C loads a file | 403; nothing written | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Endpoints delivered | `POST /api/recovery/v1/admin/rule-versions`; `GET /api/recovery/v1/admin/rule-versions?routeSet=&status=`; `POST /api/recovery/v1/admin/rule-versions/{versionId}/approve`; `POST /api/recovery/v1/admin/rule-versions/{versionId}/rollback`. |
| Contract delta | None against API Specification v2. `RuleVersion` already carries ruleId, ruleVersion, routeSet, fromState, eventCode, conditionExpr, actionText, toState, ownerRole, timerSpec, validFrom, validTo, approvedBy and testCaseId; `RollbackRequest` carries the reason. |
| Backward compatibility | Additive; no existing endpoint changes. |
| Authorization | Rules and parameters C to load; A to approve; U to roll back; R to list. 401 MSG-P4-001; 403 MSG-P4-002; 404; 409 MSG-GEN-004/MSG-P7-002/MSG-P3-015; 422 MSG-P3-027/MSG-GEN-001/MSG-GEN-003; 503. |
| Versioning | No API version change; the OpenAPI file is unchanged. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-39 is Epic 8. | Existing frontend tests remain green. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | FR-RWB-008; SPEC-RWB-E1-029-001..016 | New parser, validator, test runner, dry run, version service, effective job and controller. | Positive, negative, boundary and error-path tests: valid load, overlap, unreachable, default, test failure, author approval, rollback, duplicate, past date, empty file, access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `RuleTemplateParser` | Service | Reads the Rows and Tests sheets; keeps row numbers. |
| `RuleLoadValidator` | Published interface | Schema, overlap, unreachable-row and default-row checks; returns `ValidationReport`. |
| `RuleTestRunner` | Service | Runs each test case against the draft rows with the same evaluator the engines use. |
| `RuleDryRun` | Service | Counts open cases whose result changes, by product and queue; reads case fields through P3. |
| `RuleVersionController` | Controller | P4 list, load, approve and rollback endpoints. |
| `RuleVersionService` | Service | Stores rows, checks approval, applies the effective date and rolls back in one transaction; writes the change log. |
| `RuleTableReader` | Published interface | P4 version in force for a table and a date, cached per version. |
| `RuleEffectiveDateJob` | Job | Daily at 00:01 sets APPROVED versions with today's valid from IN_FORCE. |

### Package and boundaries

Validation, test runner and dry run live in `recovery.casewf.rules`; the endpoints and `rule_row`
writes live in the P4 package `recovery.accessadmin.ruleversions`, which owns `rule_row`. P3 receives
draft rows and never writes P4 tables. Engines read through `RuleTableReader`.

### Data and migration

- Writes `rule_row` (all columns plus `rule_table`, `row_order`, `target_queue_code`) and
  `rule_version` (rule table, version label, status, author, approver, loaded and approved times,
  valid from, test result, dry run counts).
- `uk_rule_row (rule_id, rule_version)` exists. P4 migration `V029_1__rule_table_columns.sql` adds the
  three columns, creates `rule_version` with `UNIQUE (rule_table, version_label)`, and adds
  `ix_rule_table_version ON rule_row (rule_table, rule_version) WHERE is_active`.
- Rollback sets `is_active=false` on the rolled-back version and `true` on the previous one in one
  transaction.

### Validation and dry run

1. Schema: columns, types and values against LOV-ASSIGN, LOV-ASSIGN-REASON, LOV-PRODUCT, LOV-REGION
   and LOV-EXPOSURE.
2. Overlap: two rows with the same table, trigger and row order cannot both match.
3. Unreachable: a row covered by an earlier row is refused.
4. Default: ALLOCATION must have a last row that matches every case.
5. Tests: `RuleTestRunner` runs the Tests sheet against the draft rows; `rules.testcases.min` (50,
   assumed) is the minimum.
6. Dry run: `RuleDryRun` evaluates every open case and counts changed results by product and queue.
7. Any failure refuses the load whole and names every failed row or test case.

### Version lifecycle and rollback

- A successful load stores rows with status LOADED and writes the change log with author, time, check
  result and dry run counts.
- Approval requires a different user holding Rules and parameters A; the version stays LOADED
  otherwise.
- `RuleEffectiveDateJob` moves APPROVED to IN_FORCE on the valid from date and marks the previous
  version SUPERSEDED. New decisions use the new rows; open cases keep the version recorded on their
  decision log entry (R-UNI-38).
- Rollback requires a reason, sets the current version ROLLED_BACK and the previous version IN_FORCE
  in one transaction, and writes the change log.

### Transaction and events

Each load, approval and rollback is one transaction. No event is published by this story; engines
read the version in force through `RuleTableReader`.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-COE | Rules and parameters CRUD; loads and rolls back | All |
| RW-RISK | Rules and parameters A; approves | All |
| RW-AUDIT | Rules and parameters R; reads versions and change log | All |
| RW-REFADM | Prepares load files; may not approve | All |
| SY-RULES | Reads the version in force | All |

No delegation of authority level applies; a rule version is not a credit decision. A role without
Rules and parameters C receives 403 MSG-P4-002.

### Observability and operations

- Load response: version, status, rows, check results and failing IDs.
- Change log: author, approver, load and approval times, test result, dry run counts, rollback reason.
- Metrics: loads, refusals by check, approvals, effective versions, rollbacks, dry run duration.
- Alerts: failed effective-date job; a version in force with no approval.

### Performance

- The 26-row ALLOCATION load validates and dry-runs against the open-case set; the target is inside the
  administrator's wait (NFR-011 applies to evaluation, not to the load).
- The effective-date job is a single indexed update per table.
- `RuleTableReader` caches the version in force per table and date.

### Feature flag and rollback

- `rwb.p3.ruleload`: off means the load and rollback endpoints return 404 and the version in force
  stays.
- Rollback: turn the flag off; redeploy the previous tag. A rule rollback is a data action through the
  rollback endpoint.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-029-01 | AC1, BR1, BR5, BR8 | System | ALLOCATION 26 rows, 50 passing tests | In force 2026-12-15; change log 50/50 and dry run |
| TC-E1-029-02 | AC2, BR3 | System | ALLOC-031 and ALLOC-032 at order 12 | Refused; both named; previous version stays |
| TC-E1-029-03 | AC3, BR1 | System | TA-07 and TA-19 fail | Refused; both named |
| TC-E1-029-04 | AC4, BR5, BR7 | System | Versions 6 and 7 | Version 6 in force; decision log keeps 7 |
| TC-E1-029-05 | AC5, BR1 | System | Row 9 reason QUICK | Refused; row and column named |
| TC-E1-029-06 | AC6, BR1 | System | ALLOC-040 covers ALLOC-041 | Refused; ALLOC-041 named |
| TC-E1-029-07 | AC7, BR4 | System | No default row | Refused |
| TC-E1-029-08 | AC8, BR6 | System | U-41 loads and approves | Refused; version LOADED |
| TC-E1-029-09 | AC9, BR7 | System | TRANSFER with one version | Refused; version stays in force |
| TC-E1-029-10 | AC10 | System | Label ALLOC-2026.12 twice | 409; MSG-GEN-004 |
| TC-E1-029-11 | AC11 | System | Valid from 2026-11-01 on 2026-12-10 | 422; MSG-GEN-003 |
| TC-E1-029-12 | AC12 | System | Template with no rows | 422; MSG-GEN-001 |
| TC-E1-029-13 | X11 | Security | RW-CASEOWN loads a version | 403; MSG-P4-002 |
| TC-E1-029-14 | BR5 | Unit | Effective-date job | APPROVED to IN_FORCE; previous SUPERSEDED |

## Guardrails and out of scope

- No business value in code: rows, conditions, target queues, test cases and the test count are data.
- No personal data in logs, tests, the dry run report or prompts; the dry run reports counts only.
- P3 receives draft rows; `rule_row` is written only by P4 code; engines use the same evaluator as the
  test runner.
- Out of scope: the rule change audit report and checklist (RWB-E1-048); the other 448 routing rules
  (later epics; DL24); the administration screen (Epic 8); reference data loads for queues and lists
  (RWB-E1-019, RWB-E1-043).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | §3, §13; SPEC-006 | Is 50 test cases fixed or a parameter? | A hard-coded count would need a release. | `rules.testcases.min` = 50 (assumed); the count is data. | RESOLVED | SPEC-006 |
| CLAR-002 | §13; SPEC-001 | Which module owns `rule_row`? | Cross-module write risk. | P4 owns `rule_row`; P3 validates drafts and calls the P4 interface. | RESOLVED | SPEC-001 |
| CLAR-003 | §9; SPEC-008 | The story uses LOADED but LOV-VERSION-STATUS lists VALIDATED. Which status is stored? | The status value appears in the API and audit. | Use LOADED for rule versions; the list needs LOADED added by a list load. No code change. | RESOLVED | SPEC-008 |
| CLAR-004 | §4.5; SPEC-007 | Does the dry run read personal data? | PDPA. | It reads case fields needed for evaluation and reports counts only; no personal data in the report or logs. | RESOLVED | SPEC-007 |
| CLAR-005 | §13; SPEC-010 | When does a version become effective? | Timing of the switch. | Daily at 00:01 Asia/Bangkok on the valid from date. | RESOLVED | SPEC-010 |
| CLAR-006 | BR6; SPEC-009 | Who holds Rules and parameters A? | Approval cannot proceed without it. | RW-RISK; one person may not hold RW-COE and RW-RISK. | RESOLVED | SPEC-009 |
| CLAR-007 | Contract; SPEC-011 | Is a rollback reason mandatory? | Audit quality. | Yes; empty reason returns 422 MSG-GEN-001. | RESOLVED | SPEC-011 |
| CLAR-008 | BR5, AC4; SPEC-010 | Does rollback change the rule version on open cases? | Reproducibility. | No; open cases keep the version recorded when the decision was taken. | RESOLVED | SPEC-010 |
| CLAR-009 | §3; SPEC-001 | Which five tables are in Epic 1? | Scope. | ENTRY, EXCLUSION, ALLOCATION, ASSIGNMENT and TRANSFER (DL24, option A). | RESOLVED | SPEC-001 |

`CLARIFICATION_STATUS: RESOLVED` — all 9 items are answered from the story, DL24 or the API
specification. The LOADED value is a list addition, not a code change.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend rule-administration story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New rule load, validation, approval and rollback capability; four P4 endpoints delivered from the existing v2 contract; no screen.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: first delivery of the rule-version endpoints with no OpenAPI delta]
REQUIREMENT_COVERAGE_SUMMARY: All 8 business rules, 12 acceptance criteria, 11 exception paths and 5 version states are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 8] [COVERED_RULES: 8] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
