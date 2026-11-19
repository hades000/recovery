# Technical Specification — RWB-E1-040 Document checklist per case type as reference data

| Field | Value |
|---|---|
| Story | RWB-E1-040 — Document checklist per case type as reference data |
| Epic / module | E1 / P5 Document hub |
| RUN_ID | `INC-071-epic-1-RWB-E1-040` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-DCM-011); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 040 Document checklist per case type as reference data v1.md`; FSD P5 A2.16; TSD P5 T3.1 |
| Upstream IDs | REQ-DCM-011; FEAT-DCM-16; US-RWB-E1-040; D7.2; DL01, DL19; R-UNI-38, R-UNI-40; R-LIT-16, R-LIT-17; R-GUA-07, R-GUA-08 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `YES` — SCR-30 DocumentChecklistPanel replaces the placeholder with required items present or missing; SCR-02 adds the MissingDocumentsBadge count and filter. |
| Logic In Scope | `YES` — checklist load validation, version selection, route precedence, document counting, completeness flag, event handling and refresh. |
| API In Scope | `YES` — `GET /cases/{caseId}/document-checklist` changes from the placeholder to the computed checklist; `POST /admin/reference-loads` is reused. |
| API Impact Type | `EXISTING_API_CHANGE` |
| Impacted Existing Nodes | `DocumentChecklist` endpoint (API-P5-008); reference-load endpoint (P4); SCR-30; SCR-02; JOB-12 (new `checklistRefreshStep`). |
| New Nodes Required | `YES` — `ChecklistLoader`, `ChecklistEvaluator`, `DocumentStoredChecklistListener`, `CaseStateChangedChecklistListener`, `ChecklistRefreshStep`, `DocumentChecklistService`, `ChecklistRepository`, `CaseDocumentCheckRepository`, `DocumentChecklistPanel`, `MissingDocumentsBadge`. |
| Inherited Existing Behavior | Document store and DocumentStored (RWB-E1-024); document types (RWB-E1-025); checklist placeholder (RWB-E1-026); reference data service (RWB-E1-043); case stage and route through `CaseDirectory` (P3); CaseStateChanged (EV-05). |
| Frontend Changes Required | `YES` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | The checklist per case type is held as reference data so a missing document is visible. | SPEC-RWB-E1-040-001, SPEC-RWB-E1-040-007 | DIRECT | `document_checklist_item`; endpoint returns items with present counts. | COVERED |
| BR2 | The case type is the case stage, with route rows taking precedence over rows with no route. | SPEC-RWB-E1-040-003 | DIRECT | Stage from `CaseDirectory`; route rows win where they exist. | COVERED |
| BR3 | A checklist version takes effect on its valid-from date, without a deployment. | SPEC-RWB-E1-040-002, SPEC-RWB-E1-040-010 | DIRECT | `valid_from`/`valid_to`; refresh step recomputes affected cases. | COVERED |
| BR4 | Only active documents count, once per type. | SPEC-RWB-E1-040-004 | DIRECT | `document.is_active`; one present count per type. | COVERED |
| BR5 | The completeness flag is recomputed on every document stored and every stage change. | SPEC-RWB-E1-040-006 | DIRECT | DocumentStored (EV-16) and CaseStateChanged (EV-05) listeners. | COVERED |
| BR6 | A repeated event changes nothing. | SPEC-RWB-E1-040-006 | DIRECT | Event ID idempotency; repeat counted and ignored. | COVERED |
| BR7 | The checklist is the source the pack checks read in later epics. | SPEC-RWB-E1-040-007, SPEC-RWB-E1-040-008 | DIRECT | `DocumentChecklistService.forCase` and `missingCounts` are published. | COVERED |
| AC1 | A LITIGATION case shows the 4 items; DEMAND_LETTER and COURT_NOTICE present; TITLE_DEED and APPRAISAL_REPORT missing. | SPEC-RWB-E1-040-003, SPEC-RWB-E1-040-007 | DIRECT | Stage rows from CHK-2026.11; active document counts. | COVERED |
| AC2 | A new checklist version adds GUARANTOR_NOTICE for DEED_IN_LIEU on 1 December without a deployment. | SPEC-RWB-E1-040-002, SPEC-RWB-E1-040-010 | DIRECT | Version in force by date; refresh step. | COVERED |
| AC3 | A DEED_IN_LIEU case with a title deed and an appraisal report has complete false, missing 1 and SETTLEMENT_AGREEMENT; the case list shows 1 missing. | SPEC-RWB-E1-040-005, SPEC-RWB-E1-040-008 | DIRECT | `case_document_check`; badge count. | COVERED |
| AC4 | A settlement agreement stored on that case sets complete true and missing 0; the case list shows no missing. | SPEC-RWB-E1-040-005, SPEC-RWB-E1-040-006 | DIRECT | Recompute on DocumentStored. | COVERED |
| AC5 | A stage change to LITIGATION uses the LITIGATION rows and sets complete false with the missing litigation types. | SPEC-RWB-E1-040-006 | DIRECT | Recompute on CaseStateChanged. | COVERED |
| AC6 | A DEBT_SALE case with no rows shows "No checklist for this case type", complete empty and missing 0. | SPEC-RWB-E1-040-003, SPEC-RWB-E1-040-005, SPEC-RWB-E1-040-009 | DIRECT | No rows; empty flag. | COVERED |
| AC7 | A load with POWER_OF_ATTORNEY is refused whole with MSG-P3-027; CHK-2026.11 stays in force. | SPEC-RWB-E1-040-001 | DIRECT | Type checked against the catalog in force. | COVERED |
| AC8 | A repeated DocumentStored event writes `case_document_check` once and counts the second as a repeat. | SPEC-RWB-E1-040-006 | DIRECT | Event ID idempotency. | COVERED |
| AC9 | An appraisal report at version 2 with version 1 inactive counts as present once. | SPEC-RWB-E1-040-004 | DIRECT | Active document only. | COVERED |
| X1 | The stage has no checklist rows. | SPEC-RWB-E1-040-009 | DIRECT | Message; complete empty; missing 0. | COVERED |
| X2 | A load names a type not in the type table or a stage not in LOV-STAGE. | SPEC-RWB-E1-040-001 | DIRECT | Load refused whole; MSG-P3-027. | COVERED |
| X3 | The same DocumentStored event arrives twice. | SPEC-RWB-E1-040-006 | DIRECT | One result; second counted. | COVERED |
| X4 | A document type is present only as an inactive earlier version. | SPEC-RWB-E1-040-004 | DIRECT | Count once through the active version. | COVERED |
| X5 | A role without Documents R opens the checklist. | SPEC-RWB-E1-040-011 | DIRECT | 403 MSG-P4-002. | COVERED |

## User story intent interpretation

As a **litigation officer**, I want **the required documents per case type and route held as a versioned reference table that the case documents screen, the case list and the review queue read**, so that **a missing document shows on the case without a person checking a list**. The story creates the checklist table and the per-case completeness flag, extends the existing checklist endpoint, and adds the panel on SCR-30 and the count on SCR-02. The evaluator reports only; it never blocks a case move.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | Reference-load of table DOCUMENT_CHECKLIST; DocumentStored (EV-16); CaseStateChanged (EV-05); a checklist version reaching its valid-from date; the user opens SCR-30 or SCR-02. |
| Schedule | `checklistRefreshStep` in JOB-12 when a version's valid-from date is reached. |
| Preconditions | RWB-E1-024 and RWB-E1-026 done; RWB-E1-025 done with the six types; RWB-E1-043 done with versioned reference tables; CHK-2026.11 loaded and approved; `CaseDirectory` returns stage, route and owner; flag `rwb.dochub.checklist` on. |
| Input | Checklist rows by stage, route and type; active documents on the case; case stage and route. |
| Output | `document_checklist_item` rows; `case_document_check`; checklist response; missing counts on the case list. |
| Feature flag | `rwb.dochub.checklist`. Off: the endpoint returns the RWB-E1-026 placeholder and no flag is written. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `document_checklist_item` | `stage_code` | Load file | Reference data administrator | LOV-STAGE. |
| `document_checklist_item` | `route_code` | Load file | Reference data administrator | LOV-ROUTE or empty. |
| `document_checklist_item` | `document_type` | Load file | Reference data administrator | Must be in the type table in force. |
| `document_checklist_item` | `required` | Load file | Reference data administrator | Boolean. |
| `document_checklist_item` | `sort_order` | Load file | Reference data administrator | Integer; display order. |
| `document_checklist_item` | `table_version`, `valid_from`, `valid_to` | Load file | Reference data administrator | Version in force by business date. |
| `case_document_check` | `checklist_version` | Version in force | System writes | String `CHK-YYYY.NN`. |
| `case_document_check` | `required_count`, `present_count` | Evaluation | System writes | Integers. |
| `case_document_check` | `missing_types` | Evaluation | System writes | JSON array of type codes. |
| `case_document_check` | `complete` | Evaluation | System writes | False, true or empty when no checklist. |
| `case_document_check` | `checked_at`, `last_event_id` | Evaluation | System writes | Timestamp and event ID. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| `case_document_check.complete` empty | Checklist evaluated | A required type is missing | `false` | Missing types and count written; badge shows the count. |
| `case_document_check.complete` false | DocumentStored | The last required type arrives | `true` | Missing count 0; badge clears. |
| `case_document_check.complete` true | CaseStateChanged | The new stage has a checklist with a missing type | `false` | New stage rows used; missing types updated. |
| `case_document_check.complete` any | Checklist evaluated | The stage has no checklist rows | empty | Missing count 0; message "No checklist for this case type". |
| `case_document_check` (existing) | Repeated event | Same event ID | unchanged | Second delivery counted; no write. |

No case status changes. The evaluator never blocks a case move.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No checklist rows for the case stage | Checklist shows "No checklist for this case type"; complete empty; missing 0 | None |
| X2 | Load names a type not in the type table, or a stage not in LOV-STAGE | Load refused whole; version in force unchanged | MSG-P3-027 |
| X3 | Same DocumentStored event delivered twice | One `case_document_check` write; second counted as repeat | None |
| X4 | A type is present only as an inactive earlier version | Counted once through its active version | None |
| X5 | Role without Documents R opens the checklist | 403; nothing returned | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `EXISTING_API_CHANGE` |
| Existing endpoints used | `GET /api/recovery/v1/cases/{caseId}/document-checklist` (API-P5-008); `POST /api/recovery/v1/admin/reference-loads` for table DOCUMENT_CHECKLIST. |
| Contract delta | The checklist response changes from the placeholder to computed items with `presentCount`, `missingCount` and `complete`. `checklistVersion` must be a string (`CHK-2026.11`), not the integer in the current schema; this is a schema defect to correct. |
| Backward compatibility | The placeholder shape is preserved; the values become real. No consumer is removed. |
| Authorization | Documents R with scope; Reference data C to load; Reference data A to approve; 403 MSG-P4-002/MSG-P4-003. |
| Error behaviour | 401; 403; 404; 409 duplicate version MSG-P3-027; 422 row errors MSG-P3-027; 503. |
| Versioning | No version change; the schema correction is backward compatible for existing clients. |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-011; SPEC-RWB-E1-040-007, -008, -009 | New DocumentChecklistPanel and MissingDocumentsBadge; placeholder replaced. | Component tests for present, missing, no-checklist, loading and badge/filter states. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-DCM-011; SPEC-RWB-E1-040-001..012 | New loader, evaluator, listeners, refresh step, service and repositories. | Unit tests for load validation, route precedence, version selection, active counts, complete flag, repeats, stage change, no checklist and access. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `ChecklistLoader` | Service | Implements `ReferenceTableLoader` for DOCUMENT_CHECKLIST; validates every row and refuses the load whole. |
| `ChecklistEvaluator` | Service | Picks the rows for the stage and route; counts active documents; writes `case_document_check`. |
| `DocumentStoredChecklistListener` | Listener | Calls the evaluator on DocumentStored; keeps the event ID for repeats. |
| `CaseStateChangedChecklistListener` | Listener | Calls the evaluator on CaseStateChanged; keeps the event ID. |
| `ChecklistRefreshStep` | Job step | Recomputes cases when a checklist version reaches its valid-from date. |
| `DocumentChecklistService` | Published interface | `forCase(caseId, businessDate)` and `missingCounts(caseIds)`. |
| `ChecklistRepository` | Repository | Reads and writes `document_checklist_item`. |
| `CaseDocumentCheckRepository` | Repository | Reads and writes `case_document_check`. |
| `DocumentChecklistPanel` | React component | Replaces the SCR-30 placeholder with required items present or missing. |
| `MissingDocumentsBadge` | React component | Count on SCR-02 rows and the filter. |

### Package and boundaries

`recovery/dochub/checklist`, Java package `recovery.dochub.checklist`; front end `recovery/documents`. Stage, route and owner come through `CaseDirectory`; P3 reads the flag through `DocumentChecklistService`; the reference load goes through the P4 loader. No module reads another module's tables.

### Data and migration

- Creates `document_checklist_item` (`id`, `stage_code`, `route_code`, `document_type`, `required`, `sort_order`, `table_version`, `valid_from`, `valid_to`, `load_id`, standard columns) with unique `(stage_code, route_code, document_type, table_version)`.
- Creates `case_document_check` (`id`, `case_id`, `checklist_version`, `required_count`, `present_count`, `missing_types`, `complete`, `checked_at`, `last_event_id`, standard columns) with unique `(case_id)`.
- Index `ix_checklist_stage ON document_checklist_item (stage_code, valid_from)`.
- Migration `V1_5_040__document_checklist.sql`; no business value in code: stages, routes and required types are rows.

### Checklist rules

1. Load: every row must have a stage in LOV-STAGE, a route in LOV-ROUTE or empty, a type in the type table in force, and no duplicate; any error refuses the whole load.
2. Version: choose the rows whose `valid_from <= businessDate` and `valid_to` is empty or later.
3. Stage and route: use the route rows where they exist; otherwise use the rows with no route.
4. Count: count active documents of each required type once; a type with an inactive earlier version counts through its active version.
5. Write: `required_count`, `present_count`, `missing_types`, `complete`, `checked_at` and `last_event_id`.
6. No rows for the stage: complete empty and missing count 0; the screen shows "No checklist for this case type".

### Transaction, events and idempotency

- One transaction per case evaluation; the `case_document_check` row is upserted by `case_id`.
- The listener keeps the event ID; a repeat is counted and ignored.
- A failed handling retries; after the retry limit the event goes to the exception queue with the platform administrator as owner.
- `checklistRefreshStep` runs in JOB-12 when a version's valid-from date is reached; it recomputes the cases of the stages the version changes.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-REFADM | Reference data C | All |
| Approver with Reference data A | Reference data A | All; assumed legal counsel under DL01 |
| RW-LITOFF, RW-CASEOWN, roles with Documents R | Documents R | Case scope |
| RW-LEGAL | Documents R; agrees the items (DL19) | All |
| SY-CASEWF | Publishes CaseStateChanged | All |

### Observability, performance and operations

- Metrics: checklist evaluations, complete rate, missing count, load refusals, refresh cases, repeat events.
- Alerts: load refused; refresh step failed; event handling in the exception queue.
- Run book: JOB-12 `checklistRefreshStep` in RWB-E1-056.
- Performance: one query per case; `missingCounts` accepts at most 500 case IDs per call; the case list uses the stored flag, not a live count.

### Feature flag and rollback

`rwb.dochub.checklist`. Off: the endpoint returns the RWB-E1-026 placeholder and no flag is written. Rollback: turn the flag off; the migration is forward-only and the new tables are additive.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-040-01 | AC1, BR1, BR2 | System | LITIGATION case with a demand letter and a court notice | 4 items; 2 present; 2 missing. |
| TC-E1-040-02 | AC2, BR3 | System | CHK-2026.12 valid from 1 December 2026 | 4 DEED_IN_LIEU items including GUARANTOR_NOTICE; no deployment. |
| TC-E1-040-03 | AC3, BR5 | System | DEED_IN_LIEU case with 2 of 3 types | complete false; missing 1; SETTLEMENT_AGREEMENT; badge 1. |
| TC-E1-040-04 | AC4, BR5 | System | Settlement agreement stored on that case | complete true; missing 0; badge clears. |
| TC-E1-040-05 | AC5, BR5 | System | Stage change DEED_IN_LIEU to LITIGATION | LITIGATION rows; complete false; missing litigation types. |
| TC-E1-040-06 | AC6 | System | DEBT_SALE with no rows | No-checklist message; complete empty; missing 0. |
| TC-E1-040-07 | AC7 | System | Row with POWER_OF_ATTORNEY | Load refused whole with MSG-P3-027; version unchanged. |
| TC-E1-040-08 | AC8, BR6 | System | DocumentStored delivered twice | One write; second counted as repeat. |
| TC-E1-040-09 | AC9, BR4 | System | Appraisal report with two versions | Counted once. |
| TC-E1-040-10 | X5 | Security | RW-CAPACITY without Documents R opens the checklist | 403 MSG-P4-002. |

## Guardrails

- No business value in code: stages, routes and required types are rows in `document_checklist_item`.
- No personal data in logs, tests or prompts: the flag holds type codes and counts only.
- No read of another module's tables: stage, route and owner come through `CaseDirectory`; P3 reads the flag through `DocumentChecklistService`.
- The evaluator never blocks a case move; it reports only.

## Out of scope

- The litigation pack check against the defect list and the block at filing (FEAT-LIT-05, Epic 5; CTL-19).
- The guarantee claim checklist (FEAT-GUA-01, Epic 4).
- Retrieval requests for missing documents (R-LIT-17, Epic 5).
- The review queue screen that shows the case checklist (RWB-E1-054).

## Traceability

| Requirement ID | Requirement (short) | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|
| REQ-DCM-011 | Checklist per case type as reference data so a missing document is visible | FEAT-DCM-16 | 13 Manage documents and correspondence | R-UNI-38, R-UNI-40, R-LIT-16, R-LIT-17 | TC-E1-040-01..10 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | Contract; SPEC-007 | The API schema types `checklistVersion` as an integer, but the story and TSD use `CHK-2026.11`. | A version string cannot be returned as an integer. | Treat `checklistVersion` as a string; correct the API schema before build. No behaviour change. | RESOLVED | SPEC-RWB-E1-040-007 |
| CLAR-002 | Authority; SPEC-011 | No role holds Reference data A in the permission matrix today. | Determines who approves a checklist load. | Assume the legal counsel as co-owner of the checklist under DL01; confirm the role matrix before go-live. | RESOLVED | SPEC-RWB-E1-040-011 |
| CLAR-003 | Preconditions; SPEC-001 | The CHK-2026.11 contents are assumed until the bank list is signed. | Determines the first checklist. | Load the assumed list under DL19; the data can change without a deployment. | RESOLVED | SPEC-RWB-E1-040-001 |
| CLAR-004 | BR2; SPEC-003 | Does "case type" mean the case stage, the route or both? | Determines row selection. | Stage with route precedence, as BR2 states; route is optional and a route row wins over a no-route row. | RESOLVED | SPEC-RWB-E1-040-003 |
| CLAR-005 | Contract; SPEC-008 | Why does `missingCounts` accept at most 500 IDs? | Determines the case-list call size. | The story's published interface sets 500 per call; the case list batches by 500. | RESOLVED | SPEC-RWB-E1-040-008 |
| CLAR-006 | AC6; SPEC-009 | What is `complete` when the stage has no checklist? | The flag must be nullable, not false. | Empty (null) and missing count 0, as AC6 states; the screen shows "No checklist for this case type". | RESOLVED | SPEC-RWB-E1-040-009 |
| CLAR-007 | Feature flag; SPEC-012 | What does the endpoint return when the flag is off? | Determines the fallback. | The RWB-E1-026 placeholder, and no flag is written. | RESOLVED | SPEC-RWB-E1-040-012 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or the decision log. No item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New checklist reference table and per-case completeness flag; the existing checklist endpoint returns computed items and the case list shows a missing count.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: YES] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: EXISTING_API_CHANGE] [REASON: existing checklist endpoint changes from placeholder to computed data; new UI panel and badge]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 9 acceptance criteria and 5 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: AVAILABLE [SOURCE: LOCAL_ARTIFACTS] [SCREENS: 2] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
