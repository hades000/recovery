# Technical Specification — RWB-E1-048 Rule change audit report

| Field | Value |
|---|---|
| Story | RWB-E1-048 — Rule change audit report |
| Epic / module | E1 / P3 Case and workflow |
| RUN_ID | `INC-072-epic-1-RWB-E1-048` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-020, FR-RWB-008); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 048 Rule change audit report v1.md` |
| Upstream IDs | BRD-RWB-020, BRD-RWB-003; FR-RWB-020, FR-RWB-008; REQ-CWC-013, REQ-DRI-011; US-RWB-E1-048; CTX-FEATURE-020; R-UNI-38; CTL-08 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. Internal audit and the centre of excellence read the report through the endpoint and open the CSV in Excel; SCR-39 is Epic 8. |
| Logic In Scope | `YES` — checklist validation, separation of duty, verification date check, effect calculation, period query, JSON/CSV report. |
| API In Scope | `YES` — new `GET /admin/change-log`; new `POST /admin/reference-loads/{loadId}/verify`; three new form fields on the existing P4 load and approval endpoints. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `reference_version`, `reference_row`; P4 `POST /admin/reference-loads`; P4 `POST /admin/reference-loads/{loadId}/approve`; P4 `ReferenceVersionRegistry`; API-P3-019; `ChangeLogPage`, `VerifyRequest`. |
| New Nodes Required | `YES` — `ChangeChecklistValidator`, `ChangeEffectCalculator`, `ChangeLogService`, `ChangeLogController`; extension of `ReferenceVersionRepository`. |
| Inherited Existing Behavior | Reference data registry and approval (RWB-E1-043); permission matrix (RWB-E1-037); data quality report (RWB-E1-011); rule version load (RWB-E1-029); rule test harness result (RWB-TE-005). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A version can be approved only when it carries a change request reference, an impact summary, a rollback plan and a test result of PASSED. | SPEC-RWB-E1-048-001, -002 | DIRECT | `ChangeChecklistValidator` called from `approve`; MSG-P3-022 names the first missing item. | COVERED |
| BR2 | The approver is not the author. | SPEC-RWB-E1-048-003 | DIRECT | Compare `approver_user_id` with `author_user_id`; MSG-P7-002. | COVERED |
| BR3 | A version that is not approved never takes effect. | SPEC-RWB-E1-048-004 | DIRECT | The applier serves only APPROVED/IN_FORCE versions; the report shows VALIDATED. | COVERED |
| BR4 | Verification is recorded on or after the valid from date. | SPEC-RWB-E1-048-005 | DIRECT | Compare the business date with `valid_from`; MSG-GEN-003. | COVERED |
| BR5 | The report lists every version of every reference and rule table whose load, approval, valid from or verification falls in the period. | SPEC-RWB-E1-048-007, -018 | DIRECT | Period query across four dates; all table codes. | COVERED |
| BR6 | The effect of a version is the count of rows added, changed and removed against the version it replaces, and for rule tables the rule IDs changed. | SPEC-RWB-E1-048-006 | DIRECT | Compare `reference_row` by `row_key` and `row_data`; list rule IDs for `RULE_` tables. | COVERED |
| BR7 | A rollback appears as its own entry naming the version it returns to. | SPEC-RWB-E1-048-006, -007 | DIRECT | Rollback writes a version record with `rollback_reason`; the report includes it. | COVERED |
| AC1 | A SERVICE_LEVEL v4 change shows table, version, request CR-2026-0042, PASSED, author, approver, approval date, valid from, 1 changed/0 added/0 removed; approval before valid from. | SPEC-RWB-E1-048-001, -002, -006, -007 | DIRECT | All checklist fields and the effect count. | COVERED |
| AC2 | An unapproved version 5 is not served; the report shows VALIDATED with an empty approver. | SPEC-RWB-E1-048-004, -007 | DIRECT | Applier gate; report reads the registry. | COVERED |
| AC3 | A HOLIDAY v2 with no rollback plan is refused with MSG-P3-022 naming "rollback plan"; it stays VALIDATED. | SPEC-RWB-E1-048-002 | DIRECT | Checklist validation before status change. | COVERED |
| AC4 | A rule version with a FAILED harness result is refused with MSG-P3-022 naming "test result". | SPEC-RWB-E1-048-002 | DIRECT | Test result must be PASSED. | COVERED |
| AC5 | Verification on the valid from date records verified by and verified at. | SPEC-RWB-E1-048-005, -007 | DIRECT | Inclusive date check. | COVERED |
| AC6 | A period with no changes returns an empty list with total 0. | SPEC-RWB-E1-048-009 | DIRECT | Empty page. | COVERED |
| AC7 | Verification before valid from is refused with MSG-GEN-003 naming "verified at" and "valid from". | SPEC-RWB-E1-048-005, -010 | DIRECT | Date check. | COVERED |
| AC8 | A period whose end is before its start is refused with MSG-GEN-003 naming "to" and "from". | SPEC-RWB-E1-048-010 | DIRECT | Parameter validation. | COVERED |
| AC9 | CSV output has one header row and one row per version, with no party identifier or case data. | SPEC-RWB-E1-048-008 | DIRECT | CSV writer over the same columns. | COVERED |
| X1 | A version reaches its valid from date with no approver. | SPEC-RWB-E1-048-004 | DIRECT | Not served; report shows VALIDATED. | COVERED |
| X2 | Approval with a checklist item missing. | SPEC-RWB-E1-048-002 | DIRECT | MSG-P3-022. | COVERED |
| X3 | Approval of a version whose test result is FAILED. | SPEC-RWB-E1-048-002 | DIRECT | MSG-P3-022. | COVERED |
| X4 | The report period has no changes. | SPEC-RWB-E1-048-009 | DIRECT | Empty list. | COVERED |
| X5 | Verification before valid from. | SPEC-RWB-E1-048-005 | DIRECT | MSG-GEN-003. | COVERED |
| X6 | The period ends before it starts. | SPEC-RWB-E1-048-010 | DIRECT | MSG-GEN-003. | COVERED |

## User story intent interpretation

As a **center of excellence analyst (RW-COE)**, I want **the parameter change and rule change checklist
(request, impact, test result, approver, load, verify, rollback plan) recorded on every change and reported
for audit**, so that **a configuration change is as controlled as a code change**.

The story completes the reference and rule change process that RWB-E1-043 started. It does not add the
load, validation and rollback of rule versions (RWB-E1-029), the rule test harness (RWB-TE-005), the rules
and parameters screen (SCR-39, Epic 8) or the QA sample against the rule version applied (FEAT-ADM-08).

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A version is loaded, approved or verified; audit or the centre of excellence reads the change log. |
| Preconditions | RWB-E1-043 done (every reference table version is a `reference_version` row with author and approver); RWB-E1-037 done (Rules and parameters R for RW-COE, RW-RISK, RW-AUDIT); RWB-E1-011 done (data quality report); rule versions loaded through RWB-E1-029 with table code `RULE_<route set>`; the harness result is written to the version. |
| Input | Load form: `changeRequestRef`, `impactSummary`, `rollbackPlan`; approve call; verify call with `note`; report query `from`, `to`, `table`, `format`, `page`, `size`. |
| Output | Checklist fields on `reference_version`; approval or refusal; verification record; `ChangeLogPage` or CSV. |
| Feature flag | `rwb.p3.change-log`. Off: approval runs the RWB-E1-043 checks only; the report endpoint returns 404. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `reference_version` | `change_request_ref` | Load form | Editable at load | Max 30; required at approval |
| `reference_version` | `impact_summary` | Load form | Editable at load | Max 1000; required at approval |
| `reference_version` | `rollback_plan` | Load form | Editable at load | Max 1000; required at approval |
| `reference_version` | `test_result` | Load checks or harness | System-written | PASSED or FAILED; PASSED required at approval |
| `reference_version` | `status` | Load | System-written | VALIDATED → APPROVED → IN_FORCE |
| `reference_version` | `author_user_id`, `approver_user_id`, `approved_at` | Load and approval | System-written | Approver must differ from the author |
| `reference_version` | `verified_by`, `verified_at`, `verify_note` | Verify call | System-written | Date on or after `valid_from`; note required |
| `ChangeLogEntry` | All columns | Registry query | Read only | One row per version |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| VALIDATED | Approve | Checklist complete, test PASSED, approver ≠ author | APPROVED | `approver_user_id`, `approved_at` set |
| VALIDATED | Approve | Checklist incomplete or test FAILED | VALIDATED | Refused with MSG-P3-022; no change |
| APPROVED | Valid from reached | None | IN_FORCE | Served by the reference data service |
| APPROVED / IN_FORCE | Verify | Business date ≥ `valid_from` | Unchanged | `verified_by`, `verified_at`, `verify_note` set |
| Any | Rollback | A previous version exists | ROLLED_BACK | Its own report entry naming the version returned to |

No case status changes. This story adds the checklist conditions to the reference version statuses of
RWB-E1-043.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | A version reaches its valid from date with no approver | Not served; the report shows VALIDATED with an empty approver | None |
| X2 | Approval with a checklist item missing | Refused; version stays VALIDATED | MSG-P3-022 naming the item |
| X3 | Approval with a FAILED test result | Refused; version stays VALIDATED | MSG-P3-022 naming "test result" |
| X4 | Report period with no changes | Empty list, total 0 | None |
| X5 | Verification before valid from | Refused; nothing written | MSG-GEN-003 naming "verified at" and "valid from" |
| X6 | Period end before start | Refused | MSG-GEN-003 naming "to" and "from" |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| Existing endpoints changed | P4 `POST /admin/reference-loads` and `POST /admin/rule-versions` accept `changeRequestRef`, `impactSummary`, `rollbackPlan`; P4 `POST /admin/reference-loads/{loadId}/approve` applies the checklist and separation-of-duty checks. |
| New endpoints | `POST /admin/reference-loads/{loadId}/verify` (new, `VerifyRequest` with `note`); `GET /admin/change-log` (API-P3-019) with `from`, `to`, `table`, `format`, `page`, `size`, returning `ChangeLogPage` or CSV. |
| Contract delta | Additive request fields; two new endpoints. No field removed. |
| Backward compatibility | Existing load calls without the new fields still load; approval then refuses until the fields are present. |
| Authorization | Reference data U for verify; Rules and parameters R for the report. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-P3-022; 422 MSG-GEN-001, MSG-GEN-003; 503 store unavailable. |
| Versioning | No version bump; additive fields and new endpoints. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, label or state change; the report is consumed as JSON or CSV. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-CWC-013, REQ-DRI-011; SPEC-RWB-E1-048-001..018 | New validator, effect calculator, report service, controller and repository extension; migration. | Each checklist item missing; FAILED test; author approves; verify on/before valid from; period boundaries; empty period; effect counts; CSV columns; authority. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ChangeChecklistValidator` | Service | BR1 and BR2 checks called by `approve(...)`. |
| `ChangeEffectCalculator` | Service | Compares a version with the version it replaces by `row_key` and `row_data`; lists changed rule IDs for `RULE_` tables. |
| `ChangeLogService` | Service | Builds the report for a period and a table; paging; CSV writer. |
| `ChangeLogController` | Controller | `GET /admin/change-log` and `POST /admin/reference-loads/{loadId}/verify`; problem responses. |
| `ReferenceVersionRepository` | Repository | Period query on loaded, approved, valid from and verified dates. |

### Approval and verification rules

1. On load, store `changeRequestRef`, `impactSummary`, `rollbackPlan`; store `test_result` from the load checks or the harness. A missing field does not refuse the load.
2. On approve, check in order: change request reference, impact summary, rollback plan, test result PASSED, approver ≠ author. The first failure returns 409 MSG-P3-022 naming the item; the version stays VALIDATED.
3. On verify, require a note; compare the business date with `valid_from`; a date before `valid_from` returns 422 MSG-GEN-003. A second verification returns the first record and changes nothing.
4. The applier serves only APPROVED or IN_FORCE versions whose `valid_from` has been reached; a VALIDATED version is never served.

### Report algorithm

1. Validate `from` and `to` (both required; `to` not before `from`); `size` default 50, maximum 200.
2. Select every `reference_version` whose load, approval, valid from or verification date falls in the inclusive period; optionally filter by `table_code`.
3. For each version, compute rows added, changed and removed against the version it replaces; for a `RULE_` table, list the rule IDs changed.
4. Order by `valid_from`, then `table_code`, then `version_no`.
5. Return `ChangeLogPage` with `items`, `page`, `size`, `total`; for `format = csv`, write one header row and one row per version with the same columns.
6. The CSV carries staff user IDs only; no party identifier and no case data.

### Data and migration

- Reads and writes `reference_version` and `reference_row` only.
- Migration `V048_1__change_checklist.sql` adds to `reference_version`: `change_request_ref varchar(30)`, `impact_summary varchar(1000)`, `test_result varchar(10)`, `rollback_plan varchar(1000)`, `verified_by uuid`, `verified_at timestamptz`, `verify_note varchar(1000)`; indexes on `(created_at)`, `(approved_at)` and `(valid_from)`.
- No personal data: the report holds staff user IDs, table codes and counts.

### Events

None. The change log is a read model over the registry; the approval and verification are synchronous calls.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data C, U; loads and verifies | All |
| RW-COE | Rules and parameters R; loads rule/reference versions; reads the report | All |
| RW-RISK | Rules and parameters A; approves; reads the report | All |
| RW-AUDIT | Rules and parameters R; reads and exports the report; changes nothing | All |
| RW-PLATADM | Rules and parameters R; reads the report | All |
| RW-PHONECOL | No Rules and parameters right; refused | — |

### Observability and operations

- Metrics: approvals refused by item; verifications; report reads; CSV exports; report latency.
- Alerts: approval refusal spike; report error rate; registry unavailable.
- Audit: the report itself is the audit evidence; every approval and verification is a registry row.
- Run book entry under RWB-E1-056.

### Performance

- Target: a report for a one-year period returns inside the user's wait; paging avoids a full materialisation.
- Indexes on the four date columns; the effect calculation is per version and cached by `content_hash`.
- Test with 500 versions and 20,000 rows in SIT.

### Feature flag and rollback

- `rwb.p3.change-log`. Off: approval runs the RWB-E1-043 checks only; the report endpoint returns 404.
- Rollback: turn the flag off; the migration is forward-only and the added columns remain nullable.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-048-01 | AC1, BR1, BR5, BR6 | System | SERVICE_LEVEL v3→v4, CR-2026-0042, one changed row | Entry with all checklist fields; 1 changed, 0 added, 0 removed; approval before valid from |
| TC-E1-048-02 | AC2, BR3 | System | SERVICE_LEVEL v5 never approved | v4 still served; v5 VALIDATED with empty approver |
| TC-E1-048-03 | AC3, BR1 | System | HOLIDAY v2 with no rollback plan | 409 MSG-P3-022 naming rollback plan; stays VALIDATED |
| TC-E1-048-04 | AC4, BR1 | System | RULE_UNIVERSAL_RULES v3 FAILED, 2 of 50 | 409 MSG-P3-022 naming test result |
| TC-E1-048-05 | AC5, BR4 | System | Verification on the valid from date | Verified by and at recorded |
| TC-E1-048-06 | AC6, X4 | System | Period 2026-11-01 to 2026-11-15 with no versions | Empty list, total 0 |
| TC-E1-048-07 | AC7, BR4 | System | Verification one day before valid from | 422 MSG-GEN-003 naming verified at and valid from |
| TC-E1-048-08 | AC8, X6 | System | Period 2026-12-31 to 2026-12-01 | 422 MSG-GEN-003 naming to and from |
| TC-E1-048-09 | AC9 | System | CSV export of December versions | One header row; one row per version; no party or case data |
| TC-E1-048-10 | X | Security | RW-PHONECOL reads the change log | 403 MSG-P4-002 |
| TC-E1-048-11 | BR2 | System | Author approves own version | 409 MSG-P7-002 |

## Guardrails

- No business value in code: the checklist items are fields; the report computes from rows.
- No personal data in logs, tests, the report or prompts; the report carries staff user IDs and no customer or case data.
- No read of another module's tables: rule versions reach the registry through the P4 handler calling the published interface.
- The report reads the registry; it never recomputes a version from the live tables.

## Out of scope

- The load, validation and rollback of rule versions (RWB-E1-029).
- The rule table test harness that produces the rule test result (RWB-TE-005).
- The rules and parameters screen (SCR-39, Epic 8).
- The QA sample against the rule version applied (FEAT-ADM-08, Epic 8).

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | FSD A2.16/A2.48; SPEC-007 | The FSD section A2.48 (rebalance) carries AC IDs `AC-P3-048-01..06`, which collide with the story key RWB-E1-048; the rule-change audit ACs are in A2.16 (`AC-P3-016-*`). | Determines the authoritative AC set. | The per-story file is authoritative; the A2.48 AC-ID prefix is a numbering defect and is recorded as a source finding. | RESOLVED | SPEC-007 |
| CLAR-002 | §13; SPEC-011 | Does the verify endpoint and report live in P3 or P4? | Determines module ownership and table access. | The code lives in the P4 reference data module because it reads and writes `reference_version`; the P3 requirement and API contract remain as specified. The story's package name is corrected to P4. | RESOLVED | SPEC-011 |
| CLAR-003 | BR5; SPEC-007 | Is the report period inclusive at both ends? | Determines which versions appear. | Yes; `from` and `to` are inclusive. | RESOLVED | SPEC-007 |
| CLAR-004 | BR6; SPEC-006 | What is the effect for a rule table? | Determines the report columns. | Rows added, changed and removed, plus the rule IDs changed for a `RULE_` table. | RESOLVED | SPEC-006 |
| CLAR-005 | BR1; SPEC-002 | Is the test result checked at load or at approval? | Determines when a load is refused. | At approval; a missing checklist field or a FAILED result refuses the approval, not the load. | RESOLVED | SPEC-002 |
| CLAR-006 | BR2; SPEC-003 | Is the separation-of-duty check new here or inherited from RWB-E1-043? | Determines whether this story adds the check. | This story enforces it at approval through `ChangeChecklistValidator`; RWB-E1-043 provides the approval pattern. | RESOLVED | SPEC-003 |
| CLAR-007 | AC9; SPEC-008 | Does the CSV carry staff user IDs? | Determines the PDPA position. | Yes, staff user IDs only; no party identifier and no case data. | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the API specification or the
architecture. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source; no UI change in this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New change-checklist validation, verification call and audit report; two new endpoints and additive load fields.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new change-log and verify endpoints plus checklist fields on the P4 load and approval]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 9 acceptance criteria and 6 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
