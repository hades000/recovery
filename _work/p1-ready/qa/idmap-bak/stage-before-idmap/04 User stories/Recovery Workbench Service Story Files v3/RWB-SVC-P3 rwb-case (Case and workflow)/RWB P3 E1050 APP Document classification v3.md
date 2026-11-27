# RWB-P3-E1050-APP Document classification

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1050-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-050 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP10, DP11, DP15, DP19 |
| Readiness decisions | RD-P1-008 |
| Parallel lane | L-P3-P |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-DCM-005) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- The decision event type reads `rwb.decision.DecisionRecorded.v1`; the topic `rwb.decision-record.v1` is unchanged (RD-P1-008).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-050 for rwb-case; the OCR text, the classifier and the type table stay with rwb-document (P5). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (HELD-RWB-P3-E1050-APP-L228, X20 RWB-P3-E1050-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 33 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **the document type code, the classifier version and the confidence that rwb-document returns for a scanned document applied to exactly one item of the document checklist of the case, one case review task raised when the document hub marks the result for review, and one decision record behind the result**, so that **the type and confidence of a classified document land on the right checklist item and only doubtful documents cost a person's time**.

### 2. Business rationale

A scan arrives with no type, and a document filed under the wrong type is filed against the wrong checklist item, so the stage gate, the pack check and the timers that follow the checklist all follow the wrong type (FSD P5 A2.8; legacy section 2). The legacy story read the OCR text, called the classifier, ranked the scores and applied the threshold inside the document hub, and then let attach store the document on the case. In the target the document hub owns the file, the OCR text, the classifier, the threshold and the type table (P5, RWB-P5-E1050-APP), and rwb-case owns what happens to a case when the answer arrives: the checklist item, the review task, the timeline record, the decision record and the queue the review task sits on.

rwb-case classifies nothing and computes nothing: it reads the answer the document hub published or served, keeps the type code, the classifier version and the confidence as they were given, maps the code to one checklist item of the checklist the document hub returns for the case, and raises one review task when the answer carries a review reason. No document table is read (DP-01): `document`, `document_intake`, `document_type`, `document_checklist_item` and `case_document_check` stay with rwb-document and are reached only through its contract, one hop with a 2 s timeout (DP-11). A low-confidence or unknown-type document then costs one person one task, and every other document costs nobody.

It meets REQ-DCM-005 (a document is classified into an agreed type with a confidence and a doubtful one goes to review) from the case side only, and it serves the measure of fields extracted without review (FSD P5 A2.8.1) by keeping the answer traceable on the case.

### 3. Preconditions

- The parameters contract and the reference-data contract of rwb-case are published and in force, with the client library (DP-06, DP-07): the review reasons of LOV-INTAKE-REVIEW (`LOW_CONFIDENCE`, `MODEL_UNAVAILABLE`, `UNKNOWN_TYPE`, `RESCAN`, `UNREADABLE_FILE`), the task codes of the review task, the case document checklist states and the switch parameter of section 13 are read through them, never from code.
- The rwb-document published contract is available for the document metadata, the case checklist and the field answers: `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` and `GET /api/recovery/document/v1/documents/{documentId}`, with its WireMock fake. No contract story for it is listed for this story, so the build starts against the published contract and its fake, and the contract is taken as carrying the document type, the review status, the review reason, the classifier version and the two candidate types with their confidence; the build assumes this extension of the published contract and its fake until a contract story is raised (GAP-0761; ASM-1384).
- The Temporal workflow kit is in namespace `rwb-recovery` (DP-10) and CaseWorkflow runs on task queue `rwb-case`, started by the case router from the events of section 12.4.
- `case_document_link` exists in schema `rwb_case` from the attach story RWB-P3-E1032-APP; this story adds the classification columns to it and creates no second link table.
- The review queue, the task model and the task completion are the ones of RWB-P3-E1054-APP: its queue codes, task codes and outcome codes are read through the reference-data contract, and the review screen and the correction of a type are that story's.
- The gateway-bff composite route that serves the case documents screen is published (DP-19).
- The login is the rwb-case login (DP-02), named that way until the login name is agreed with the ACE DB team and recorded in the service catalogue (GAP-0762; ASM-1385).

### 4. Flow

1. rwb-document (P5): the document hub classifies a scanned document, stores it against the case and publishes DocumentStored (EV-16) with `documentId`, `caseId`, `type` and `source` on `rwb.document.events.v1`; it publishes DocumentFieldsExtracted (EV-17) when the fields of the document are ready.
2. rwb-case: the case router consumes EV-16 through the inbox row it writes in `processed_event` in schema `rwb_case` (one action per event id), and calls `signalWithStart` on CaseWorkflow with the workflow ID equal to the case ID on task queue `rwb-case`.
3. CaseWorkflow: the `ApplyClassification` activity reads the checklist of the case through the rwb-document contract, one hop with a 2 s timeout (DP-11), and reads the classification answer of the document through the same contract.
4. ApplyClassification: holds the `documentType`, the `classificationConfidence`, the `classifierVersion`, the `reviewStatus`, the `reviewReason` and the two candidate types with their confidence exactly as the answer carries them. rwb-case reads no threshold, calls no model and holds no type table.
5. ApplyClassification: maps the type code to exactly one checklist item of the checklist answer. A type code with a matching item satisfies that item; a type code with no matching item adds no item, and the result is treated as the contract carried it, reason code `UNKNOWN_TYPE`.
6. ApplyClassification: a result with no `reviewReason` writes the classification columns on the case document link, sets the checklist item state to SATISFIED and the classification state to CLASSIFIED. A result with a `reviewReason` keeps the link UNCLASSIFIED, records the reason, the two candidates and the confidence, and adds no satisfied item.
7. `RaiseReviewTask`: a result marked for review — `LOW_CONFIDENCE`, `MODEL_UNAVAILABLE` or `UNKNOWN_TYPE` — raises exactly one case review task in the review queue of the case, `element_type` HUMAN_TASK, status OPEN, carrying the document reference, the review reason, the two candidate types and the confidence. An OPEN task for the same document is reused, never doubled.
8. `RecordAndApply`: in one `rwb_case` transaction the activity writes the link columns, the checklist item state, the task row and the local decision record. A failed write rolls the whole result back, so no satisfied item, task or record exists from a partial answer.
9. The case router also consumes EV-17 and updates the extracted field count on the same link; it creates no second link, applies no second classification and re-classifies nothing.
10. `RedriveClassificationLinks`, started by the daily Schedule of section 12.6 (DP-10), re-drives the links whose classification answer arrived before the case document link existed: it reads the documents of the case through the rwb-document contract and applies every answer the link does not hold yet, once.
11. Case owner: opens the case documents screen through gateway-bff, which calls `GET /api/recovery/case/v1/cases/{caseId}` on rwb-case and the checklist answer on rwb-document in parallel, and merges the two answers so that the type label comes from the document hub and the type code, the classifier version and the confidence come from the case.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer carries `LOW_CONFIDENCE` | One review task with the two candidates and the confidence; the link keeps the type code and stays UNCLASSIFIED | MSG-P5-003 | AC3 |
| X2 | The answer carries `MODEL_UNAVAILABLE` | One review task, no type code on the link and no satisfied item; the link stays UNCLASSIFIED | MSG-P5-003 | AC3, AC7 |
| X3 | The answer carries `UNKNOWN_TYPE` | No checklist item is added, no type code is written, one review task carries the reason code as the contract gave it | MSG-P5-003 | AC4 |
| X4 | The same event id is delivered again, or two deliveries run at once | The inbox row in `processed_event` drops the duplicate and the unique key on the link keeps one row; no state, task or record changes | None | AC5 |
| X5 | The classification answer was produced before the case document link existed | The daily Schedule applies the answer once and writes the one link, the one decision record and, if the reason says so, the one task | None | AC6 |
| X6 | rwb-document does not answer inside the REST budget | One hop, 2 s timeout (DP-11); the link stays unchanged, no candidate is invented, the result is counted as failed and the next Schedule run retries | MSG-GEN-006 | AC7 |
| X7 | A role without Case record R reads the tasks or the case | The call is refused with 403 before any read; the review task and the link are unchanged | MSG-P4-002 | AC8 |
| X8 | A document of a case outside the reader's scope is read | The read is refused with 404 and no document, type code or confidence is returned | MSG-P4-003 | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Day 1 against the rwb-document contract fake and the platform libraries' published contracts; it has no same-service story to wait for and no build dependency |
| Negotiable | The switch, the task codes, the checklist item states and the review reasons are data or contract values; the one-item, one-task and stored-as-received rules are fixed |
| Valuable | Puts the type and confidence of every classified document on the right checklist item and sends only doubtful documents to a person |
| Estimable | One event handler, one workflow with two activities, one Schedule, three endpoints and one migration |
| Small | Fits two weeks with its tests |
| Testable | Every criterion of section 7 has a test case in section 16; every cross-service answer is stubbed in the contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Document classification on the case (the rwb-case side)

  Background:
    Given case "RW-2026-000123" is open and owned by "U-CO-01"
    Given case "RW-2026-000456" is open and owned by "U-LIT-01"
    Given the rwb-document contract mock returns the checklist of case "RW-2026-000123" with checklist version 3 and the items DEMAND_LETTER, COURT_NOTICE, APPRAISAL_REPORT, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE, COURT_NOTICE required
    Given case_document_link holds document "DOC-0001" for case "RW-2026-000123" with the classification state "UNCLASSIFIED"

  Scenario: AC1 A classified document satisfies its checklist item and writes the decision record (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0001" with documentType "COURT_NOTICE", classificationConfidence 0.8000, classifierVersion "TEST-CLF-0007" and reviewStatus "NOT_NEEDED"
    When rwb-case consumes rwb.document.DocumentStored.v1 with event id "EVT-1001" for document "DOC-0001" and case "RW-2026-000123"
    Then the case document link holds checklist item "COURT_NOTICE" with item state "SATISFIED" and the classification state "CLASSIFIED"
    Then the checklist answer of the case reports COURT_NOTICE with present count 1 and no item is added to the checklist
    Then one decision record names the case, the document and event id "EVT-1001"
    Then no case review task exists for document "DOC-0001"

  Scenario: AC2 The case keeps the type code, the classifier version and the confidence as received (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0002" with documentType "APPRAISAL_REPORT", classificationConfidence 0.8000, classifierVersion "TEST-CLF-0007" and reviewStatus "NOT_NEEDED"
    Given rwb-document holds parameter CLASSIFY_THRESHOLD at 0.90 for the same document
    When rwb-case consumes rwb.document.DocumentStored.v1 with event id "EVT-1002" for document "DOC-0002" and case "RW-2026-000123"
    Then case_document_link holds document type code "APPRAISAL_REPORT", classifier version "TEST-CLF-0007" and confidence 0.8000 exactly as the answer carried them
    Then rwb-case reads no threshold, calls no model and holds no document type table
    Then no OCR text, no field value and no personal data is written into rwb_case

  Scenario: AC3 A low-confidence result raises exactly one review task with both candidates (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0003" with documentType "COURT_NOTICE", classificationConfidence 0.6200, reviewStatus "PENDING", reviewReason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100
    When rwb-case consumes rwb.document.DocumentStored.v1 with event id "EVT-1003" for document "DOC-0003" and case "RW-2026-000123"
    Then exactly one case review task exists for case "RW-2026-000123" and document "DOC-0003" with status "OPEN" and reason "LOW_CONFIDENCE"
    Then the task carries the candidate types "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100 and the confidence 0.6200
    Then the link keeps document type code "COURT_NOTICE" and the classification state "UNCLASSIFIED"
    When the same event id "EVT-1003" is delivered again
    Then still exactly one case review task exists for document "DOC-0003"

  Scenario: AC4 An unknown type adds no checklist item and raises one task (new, D-RCV-60)
    Given the rwb-document contract mock returns the checklist of case "RW-2026-000456" without an item for type "LOAN_CONTRACT"
    Given the rwb-document contract mock returns document "DOC-0004" with reviewStatus "PENDING", reviewReason "UNKNOWN_TYPE", no documentType and the candidates "TITLE_DEED" 0.4100 and "SETTLEMENT_AGREEMENT" 0.3300
    When rwb-case consumes rwb.document.DocumentStored.v1 with event id "EVT-1004" for document "DOC-0004" and case "RW-2026-000456"
    Then no checklist item is added to the case and the present count of every item is unchanged
    Then no document type code is written on the case document link and the link stays "UNCLASSIFIED"
    Then exactly one case review task exists with reason "UNKNOWN_TYPE", both candidate types and the message MSG-P5-003

  Scenario: AC5 A duplicate event for the same document changes nothing (new, D-RCV-60)
    Given the event id "EVT-1001" of AC1 has been consumed for document "DOC-0001"
    When the same event id "EVT-1001" is delivered again
    Then processed_event holds one row for event id "EVT-1001"
    Then no second link, no second checklist item state, no second review task and no second decision record is written
    When rwb.document.DocumentStored.v1 arrives for document "DOC-0001" with the new event id "EVT-1005" and the same answer
    Then the case document link still holds one row with the same type code, classifier version and confidence

  Scenario: AC6 A classification that arrives before the link exists is applied by the daily Schedule run (new, D-RCV-60)
    Given document "DOC-0006" was classified on 2026-11-29, before case_document_link held a row for it
    Given the rwb-document contract mock returns the documents of case "RW-2026-000123" with document "DOC-0006", documentType "TITLE_DEED", classificationConfidence 0.9100, classifierVersion "TEST-CLF-0007" and reviewStatus "NOT_NEEDED"
    When RedriveClassificationLinks runs on 2026-11-30
    Then one case document link exists for document "DOC-0006" with item state "SATISFIED" and the classification state "CLASSIFIED"
    Then no second link exists for the document and exactly one decision record is written

  Scenario: AC7 A rwb-document timeout leaves the link unchanged and the next run retries (new, D-RCV-60)
    Given the rwb-document contract mock does not answer within 2 s for document "DOC-0007"
    When rwb-case consumes rwb.document.DocumentStored.v1 with event id "EVT-1007" for document "DOC-0007" and case "RW-2026-000123"
    Then the case document link stays "UNCLASSIFIED" with no type code, no classifier version and no confidence
    Then no decision record and no case review task is written for the document
    Then the run records MSG-GEN-006 for the document hub and the next Schedule run applies the answer once the hub answers

  Scenario: AC8 A role without Case record R is refused and a case out of scope is not found (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /me/tasks
    Then the system refuses the call with status 403 and MSG-P4-002
    Given the rwb-access contract mock returns Case record R with a scope that excludes case "RW-2026-000456"
    When a case owner calls GET /cases/{caseId} for "RW-2026-000456"
    Then the system refuses the read with status 404 and MSG-P4-003
    Then no document, type code or confidence of the case is returned

  Scenario: AC9 A failed write leaves none of its parts, and the type label is read from the document hub at read time (new, D-RCV-60)
    When the write of the decision record, the link columns, the checklist item state and the task row for document "DOC-0001" fails part way
    Then none of the decision record, the link columns, the checklist item state and the task row is committed
    When the same write is retried after the failure
    Then the decision record, the link columns, the checklist item state and the task row are committed once together
    Given the rwb-document contract mock returns document "DOC-0001" with documentType "COURT_NOTICE"
    When a case owner reads the case document link of "DOC-0001"
    Then the type label is taken from the rwb-document answer at read time and the case holds the type code and the classifier version only

  Scenario: AC10 An error answer from a provided operation is 401 when the caller is not authenticated (new, D-RCV-60)
    Given the caller holds no valid token
    When the caller calls a provided operation of section 12.1
    Then the system answers with status 401 and no case data is returned

  Scenario: AC11 A replay of a write with the same idempotency key changes nothing (new, D-RCV-60)
    Given a write call for document "DOC-0001" and case "RW-2026-000123" was applied with an idempotency key
    When the same write is replayed with the same idempotency key
    Then the replay answers the same result as the first call
    Then no second decision record, link row, checklist item state or case review task is written
```

Every criterion above is new for the case side of the legacy story; the legacy criteria AC1 to AC10 stay with RWB-P5-E1050-APP, where the classifier, the threshold and the type table live, and the real cross-service behaviour is proved in RWB-ITG-E1050-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | rwb-case never classifies a document and never calls a model: it applies only the type code, the review reason and the confidence that the rwb-document answer carries | Legacy AC1 to AC10; FSD P5 A2.8; DP-01 |
| BR2 | A type code is applied to exactly one checklist item of the checklist the document hub returns for the case, or to none; rwb-case adds no item the checklist answer does not hold | Legacy AC5; FSD P5 A2.8; FEAT-DCM-08 |
| BR3 | A review reason always raises exactly one case review task; a result with no review reason satisfies its checklist item, and an OPEN task for the same document is reused | Legacy AC2, AC4, AC5; RWB-E1-054 BR1 |
| BR4 | The confidence and the classifier version are stored as received and never recomputed, rounded or compared with a threshold in rwb-case | Legacy AC3, AC9; DF-DOC-007, DF-DOC-073 |
| BR5 | An event acts once: the event id is recorded in `processed_event`, a duplicate changes nothing, and the unique key on the case document link keeps one row per case and document | R-UNI-40; Architecture v5 slide 11 |
| BR6 | The decision record, the link columns, the checklist item state and the task row commit in one transaction; a failed write leaves none of them | Principle 5; R-UNI-39; REQ-DRI-004 |
| BR7 | No `rwb_document` table is read and no foreign key crosses the service boundary: the document is held by its id from the document hub, and no OCR text, field value or file reference is copied into `rwb_case` | DP-01; ADR-010; D-RCV-35 U4; CTL-11 |
| BR8 | The type label shown to a person is read from the document hub answer at read time; the case holds the code and the classifier version only | DP-01; FSD P3 A2.45 (documents on the case record) |
| BR9 | The review reasons, the task codes and the checklist item states are read from the reference lists of rwb-case with their version in force, never from a Java constant | DP-07; BR-P3-003; LOV-INTAKE-REVIEW |

### 9. State transitions

No case status change: this story writes no value of `recovery_case.status` and moves no LOV-CASE-STATUS value. It moves the case document link and the review task.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| case document link (classification state) | UNCLASSIFIED | A classification answer is applied | The type code maps to one checklist item and the answer carries no review reason | CLASSIFIED |
| case document link (classification state) | UNCLASSIFIED | A classification answer is applied | The answer carries LOW_CONFIDENCE, MODEL_UNAVAILABLE or UNKNOWN_TYPE | UNCLASSIFIED, with the reason, the two candidates and the confidence recorded |
| case document link (type state) | CLASSIFIED | A reviewer confirms or corrects the type | Worked in RWB-P3-E1054-APP | CONFIRMED or CORRECTED |
| case review task | None | A classification answer with a review reason, and no OPEN task for the document | — | OPEN |
| case review task | OPEN | The reviewer completes the review | Worked in RWB-P3-E1054-APP | DONE |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Consumes EV-16 and EV-17; reads the checklist and the document answer through the rwb-document contract; writes the link columns, the checklist item state, the review task and the decision record; runs the daily re-drive Schedule |
| rwb-document service identity (the document hub) | Owns the document, the OCR text, the classifier, the threshold and the type table; publishes EV-16 and EV-17 and serves the checklist and document answers; reads no case table |
| RW-CASEOWN, case owner | Reads the case documents screen in scope; works the review tasks of own cases |
| RW-LITOFF, litigation officer | Reads the case documents screen in scope; works the review tasks of litigation cases |
| RW-TEAMMGR, team manager | Reads the case documents screen and the review tasks of the team in scope; completes no review task |
| Roles with Documents R only | See the documents of a case in their scope on the case documents screen; apply no classification and work no task |
| RW-REFADM | Has no Case record right; refused on the task and case reads |

The rwb-case login name is Not specified in the source documents (GAP-0762; ASM-1385); the story names it "the rwb-case login (DP-02)" until it is agreed.

The rwb-access authorise check that the REST operations call (DP-08) is Not specified in the source documents (DOR-RWB-P3-E1050-APP-6).

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-026 | case_account | account_key (physical column account_id) | Read |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write |
| DF-WRK-019 | task | task_code | Write |
| DF-WRK-022 | task | status | Write |
| DF-WRK-023 | task | owner_role | Write |
| DF-INT-001 to DF-INT-029 | interaction (the case timeline projection in `rwb_case`) | one DOCUMENT entry per applied result | Write |
| DF-DEC-001 to DF-DEC-018 | decision record (local table in `rwb_case`) | all fields | Write |
| Not specified in the source documents (GAP-0765; ASM-1388) | case_document_link | `document_type_code`, `classifier_version`, `classification_confidence`, `review_reason`, `candidate_one_type`, `candidate_one_confidence`, `candidate_two_type`, `candidate_two_confidence`, `classification_state`, `checklist_item_state`, `classified_at`, `source_event_id` | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | the switch parameter of section 13 and its version in force | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | LOV-INTAKE-REVIEW, the task codes and the checklist item states | Read |

The classification columns are added to the case-side link that RWB-P3-E1032-APP created; the table is not an Owner row of the Ownership Map and its field IDs are not in the Logical Data Model and Data Dictionary v9: Not specified in the source documents (GAP-0765; ASM-1388).

The decision record is a local row in `rwb_case.decision_record`, the PLT library object created in every service schema (Microservice Ownership Map v1, Tables row 97): DP-03 is not among this story's patterns, the central ledger `decision_log_entry` stays with rwb-decision (P7), no `DecisionRecorded` event is published and no platform dependency is claimed (GAP-0767).

Document side, read only through the rwb-document contract and never stored: the document id, the case id, the document type code, the review status, the review reason, the classifier version, the confidence, the two candidate types with their confidence, the type label, the checklist version of the case and the checklist items with their present counts. The classifier version is stored as an opaque string of up to 40 characters as received (the shape of DF-DOC-073); no source names a version label, so every version value in this story is a synthetic test fixture: Not specified in the source documents (GAP-0764; ASM-1387).

Field IDs are those in the Logical Data Model and Data Dictionary v9. No OCR text, no field value, no file reference and no personal data is written into `rwb_case`.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases/{caseId}` | Read one case with its status and the classification state of its document links (type code, classifier version, confidence, checklist item state) for the case screen | Case record R, scope applied | Not applicable |
| GET | `/me/tasks` | List the caller's open review tasks with the case, the document reference, the review reason, the two candidate types and the confidence | Case record R, scope applied | Not applicable |
| PATCH | `/tasks/{taskId}` | Complete or reassign a task; for a review task the outcome codes and the correction rules are those of RWB-P3-E1054-APP | Case record U, scope applied | Task version in the body; a stale version answers 409 MSG-GEN-004 |

Response fields per the case contract story: case `id`, `caseNo`, `productGroup`, `status`, `entryDate`, `totalOutstandingAtEntry`, `deviationOpen`, `legalHold`, and per document link `documentId`, `documentTypeCode`, `classifierVersion`, `classificationConfidence`, `classificationState`, `checklistItemState`, `reviewReason`, `classifiedAt`; task `id`, `caseId`, `documentRef`, `taskCode`, `status`, `ownerRole`, `reviewReason`, `candidateTypes`, `confidence`, `dueAt`, `outcomeCode`, `completedAt`. The type `label` is not part of the case answer: it is read from the rwb-document contract at read time (BR8). Errors: 401 no session (MSG-P4-001), 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 409 stale task version (MSG-GEN-004), 503 a dependency down (MSG-GEN-006).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/document-checklist` | rwb-document (P5) | The checklist in force for the case: the checklist version, the items, the type of each item, the label and the present count | One hop, 2 s (DP-11) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | rwb-document (P5) | The classification answer of the document: type code, review status, review reason, classifier version, confidence and the two candidates | One hop, 2 s (DP-11) |

The checklist answer matches the published `DocumentChecklist` schema: `checklistVersion`, `stageCode`, `items` with `documentType`, `label`, `required` and `presentCount`, `missingCount` and `complete`. The document answer is taken as carrying `classifierVersion`, `reviewReason` and the two candidate types with their confidence in addition to the fields the published schema names, and those three additions are Not specified in the source documents (GAP-0761; ASM-1384).

#### 12.3 Events published

None. No case status changes in this story, so no `rwb.case.CaseStateChanged.v1` is published; DP-03 is not among the patterns applied, so no `rwb.decision.DecisionRecorded.v1` is published either, and the decision record of section 11 is a local write only.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 | Case router, inbox row in `processed_event`, `signalWithStart` of CaseWorkflow; `ApplyClassification` then `RaiseReviewTask` |
| `rwb.document.DocumentFieldsExtracted.v1` (EV-17) | `rwb.document.events.v1` | P5 | Case router; updates the extracted field count on the same link, applies no classification |

The published payloads are `documentId`, `caseId`, `type`, `source` for EV-16 and `documentId`, `fields`, `confidence` for EV-17, so the review reason, the classifier version and the two candidates are read from the contract answer of section 12.2 and never from the event (GAP-0761; ASM-1384).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Receives the signal from the case router and runs the classification step of the case |
| ApplyClassification | Activity | `rwb-case` | Reads the checklist and the document answer, maps the type code to one item, writes the link columns, the item state and the decision record |
| RaiseReviewTask | Activity | `rwb-case` | Raises exactly one case review task for a result marked for review, reusing an OPEN task for the same document |
| RedriveClassificationLinks | Workflow started by the daily Schedule | `rwb-case` | Applies the answers of documents that were classified before their case document link existed |

#### 12.6 Schedules

| Schedule | Cadence | Trigger | Legacy reference |
|---|---|---|---|
| RedriveClassificationLinks | Daily; the time of day is Not specified in the source documents (GAP-0766; ASM-1389) | Temporal Schedule in namespace `rwb-recovery`, overlap policy SKIP and a catch-up window (DP-10) | Legacy RWB-E1-050 section 12 restart behaviour: "unfinished items stay unclassified and are taken by the next run"; the case side of that rule is new |

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| case_document_link | P3 (rwb_case) | The case-side link per case and document; this story adds the classification columns and the two states of section 11 |
| task | P3 (rwb_case) | The review task row, with `task_code`, `status`, `owner_role` and the case-side review columns |
| recovery_case | P3 (rwb_case) | Read only: the case header for the screen |
| case_account | P3 (rwb_case) | Read only: the accounts the checklist is keyed on |
| interaction (case timeline projection) | P3 (rwb_case) | One DOCUMENT entry per applied result |
| processed_event | PLT library object created in `rwb_case` | The inbox row that makes an event act once; this story publishes nothing, so `outbox_event` is not used |

rwb-case reads no table of another service and holds no foreign key across services (DP-01); `document`, `document_intake`, `document_type`, `document_checklist_item` and `case_document_check` stay with rwb-document (P5) and are reached only through the contract of section 12.2.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The P5 contract | `GET /cases/{caseId}/document-checklist` for checklist version 3 and the six agreed types; `GET /documents/{documentId}` for a satisfied type at 0.8000, a `LOW_CONFIDENCE` answer `COURT_NOTICE` 0.6200 and `DEMAND_LETTER` 0.2100, a `MODEL_UNAVAILABLE` answer, an `UNKNOWN_TYPE` answer with `TITLE_DEED` 0.4100 and `SETTLEMENT_AGREEMENT` 0.3300, and a no-answer stub for the 2 s timeout |
| rwb-access permission fixture | The P4 cached permission answer used by the guard | Case record R granted, granted with a scope that excludes case "RW-2026-000456", and refused for RW-REFADM; the fixture serves the 403 and 404 paths only and adds no build dependency |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 2 consumed | Case, task and task-write provided; the checklist and the document answer consumed, one hop with a 2 s timeout |
| Kafka | None published, 2 consumed | `rwb.document.events.v1` for EV-16 and EV-17 only |
| Temporal | 2 workflows, 2 activities | CaseWorkflow and RedriveClassificationLinks; ApplyClassification and RaiseReviewTask |
| File | None | This story reads and writes no file and holds no document blob |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `classification`, Java package `th.co.scb.ace.workbench.recovery.case.classification`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The DP-06, DP-07, DP-10, DP-15 and DP-19 rows name the dependency the pattern adds in the DP table of Template and Rules v1 §R5.5; WP B-P3-09 records Depends on (build) None and Contract dependencies None for this story, which therefore starts Day 1 against the platform libraries' published contracts and their fakes. DP-03, DP-09 and DP-14 are not applied: this story publishes no event and writes no outbox row, so it claims neither the decision-record topic nor the event naming library.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ClassificationRouter | Consumer | Consumes EV-16 and EV-17, writes the inbox row in `processed_event` and signals CaseWorkflow with the case ID |
| DocumentAnswerClient | Client | Calls the rwb-document contract for the case checklist and the document answer, one hop with a 2 s timeout; masks nothing and stores no answer payload beyond the fields of section 11 |
| ApplyClassification | Activity | Maps the type code to one checklist item, holds the values as received, writes the link columns, the item state and the decision record in one transaction |
| ChecklistItemMapper | Service | Reads the checklist answer and returns the one item of the type code, or none; adds no item |
| ReviewTaskRaiser | Service | Raises one case review task for a result marked for review on the review queue of the case, reusing an OPEN task for the same document |
| ClassificationStateCatalog | Service | Reads the review reasons, the task codes and the checklist item states through the reference-data contract; no Java enum of reasons |
| CaseDocumentLinkRepository | Repository | `case_document_link`, `task` and the interaction projection in schema `rwb_case` only |
| RedriveClassificationLinks | Workflow | Daily Schedule that applies the answers whose link did not exist when the event arrived |
| CaseController | Controller | `GET /cases/{caseId}`, `GET /me/tasks`, `PATCH /tasks/{taskId}`; declares capability area Case record and the right, and applies the caller's scope |

**Database and migrations**

- The classification migration `case_document_classification`, named in the `Vnnnn` form of the service's own Flyway sequence as Service Template Specification v1 §3 requires (its number is Not specified in the source documents (CG-ALL-3790)), adds to `rwb_case.case_document_link`: `document_type_code varchar(30)`, `classifier_version varchar(40)`, `classification_confidence numeric(5,4)`, `review_reason varchar(20)`, `candidate_one_type varchar(30)`, `candidate_one_confidence numeric(5,4)`, `candidate_two_type varchar(30)`, `candidate_two_confidence numeric(5,4)`, `classification_state varchar(15) not null default 'UNCLASSIFIED'`, `checklist_item_state varchar(15)`, `classified_at timestamptz`, `source_event_id uuid`.
- Constraint: the unique key `ux_case_document_link ON case_document_link (case_id, document_id)` from V1032_1 keeps one link per case and document, so a duplicate event and a re-drive apply once.
- Constraint: a partial index `ix_case_document_link_unclassified ON case_document_link (linked_at) WHERE classification_state = 'UNCLASSIFIED'` serves the re-drive run.
- The scale of `classification_confidence` matches the document side (DF-DOC-007, numeric(5,4)), so 0.8000 is stored as received and never rounded (BR4).
- No column carries OCR text, a field value, a file reference or a candidate label; the candidates are stored as type codes and confidences only (BR7).

**Configuration and reference data**

- The switch of this capability is a boolean parameter read through the parameters contract of rwb-case (DP-06); its key is Not specified in the source documents (GAP-0766; ASM-1389). Off means no classification answer is applied and the re-drive Schedule does not run.
- LOV-INTAKE-REVIEW with its five values, the task codes of the review task and the checklist item states are loaded through the reference-data contract (DP-07), not written in code.
- The classifier threshold, the pages read, the timeout and the type table are rwb-document's and are read by nobody in this story.

**Build steps**

1. The classification migration in the `Vnnnn` form with the classification columns, the indexes and the state default; unit test on the columns and the unique key.
2. DocumentAnswerClient against the rwb-document WireMock, one hop with the 2 s timeout and no retry inside the call; test for AC7.
3. ChecklistItemMapper and the map of a type code to one item, with the no-item case; tests for AC1 and AC4.
4. ApplyClassification holding the values as received and writing the link, the item state and the decision record in one transaction; tests for AC1, AC2 and AC7.
5. ReviewTaskRaiser with the one-task-per-document rule and the reuse of an OPEN task; tests for AC3, AC4 and AC5.
6. ClassificationRouter with the inbox row, the duplicate rule and the second-event rule; test for AC5.
7. RedriveClassificationLinks on the daily Schedule with overlap policy SKIP; test for AC6.
8. Controller endpoints with the declared right, the scope and the 409 on a stale task version; test for AC8.
9. Contract-fake run of both answers in isolation, so the story builds before the document hub is on the environment.

**Feature switch.** The legacy flag `rwb.dochub.classify` stays with rwb-document (P5) and is not read here. The rwb-case switch is a parameter read through the parameters contract (DP-06): off means the router applies no answer and the re-drive Schedule is idle, and the links stay UNCLASSIFIED with no review task.

**Done when.** The tests in section 16 pass, every applied result names the document, the type code, the classifier version and the confidence it was given, no test writes an OCR text or a field value into `rwb_case`, and the contract tests of the rwb-document fake stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document is marked for review on the case and the review task is raised | Some fields need checking. The document is in the review queue. |
| MSG-P4-001 | A request without a session | Not specified in the source documents (DOR-RWB-P3-E1050-APP-9) |
| MSG-P4-002 | A read or a task write without Case record R or U | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A case or a document outside the reader's scope | This case is not in your scope. |
| MSG-GEN-004 | A task write with a task version other than the one in force | Read from the message catalogue at build time; the wording is Not specified in the source documents (GAP-0763; ASM-1386) |
| MSG-GEN-006 | rwb-document does not answer inside the 2 s budget | Read from the message catalogue at build time, naming the document hub; the wording is Not specified in the source documents (GAP-0763; ASM-1386) |

Thai text for each message follows decision DL10, which stays open. It rests on assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

SCR-30 Case documents (Loading; empty; list; filtered; error with MSG-GEN-006 when the document hub does not answer inside the 2 s budget; no access with 403 MSG-P4-002 or 404 MSG-P4-003; no other state is named in the source documents, CG-ALL-3792) shows the documents of the case with the type label read from the rwb-document answer, the received date, the checklist item state and, for a document held for review, MSG-P5-003 with its two candidates. SCR-03 Case record (Loading; read only; empty; error with MSG-GEN-006 when the document hub does not answer inside the 2 s budget; no access with 403 MSG-P4-002 or 404 MSG-P4-003; no other state is named in the source documents, CG-ALL-3791) shows the case and its documents on the same screen model. Both are served by the gateway-bff composite route, which calls rwb-case and rwb-document in parallel, one hop each, and merges the two answers so the label comes from the document hub and the code and the version come from the case (DP-19, BR8).

The review queue screen, the queue filters and the correction of a type are RWB-P3-E1054-APP's. The field-level masking of the document list and the composite route specification are Not specified in the source documents (GAP-0761; ASM-1384).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-050-11 | AC8, BR9 | Component | RW-REFADM calls GET /me/tasks and is refused with MSG-P4-002; a case outside the scope answers 404 with MSG-P4-003 |
| TC-E1-050-01 | AC1, BR1, BR2 | End to end | Labeled sample of 180 synthetic documents, 30 per type; the evaluation itself stays with rwb-document (P5) |
| TC-E1-050-02 | AC3, BR3, BR4 | End to end | Answer COURT_NOTICE 0.6200, DEMAND_LETTER 0.2100, reason LOW_CONFIDENCE |
| TC-E1-050-03 | AC1, BR2 | End to end | Answer APPRAISAL_REPORT 0.8000 with no review reason |
| TC-E1-050-04 | AC7, BR1 | End to end | No answer from the document hub for 2 s |
| TC-E1-050-05 | AC4, BR2, BR3 | End to end | Answer with reason UNKNOWN_TYPE, no type code, candidates TITLE_DEED 0.4100 and SETTLEMENT_AGREEMENT 0.3300 |
| TC-E1-050-06 | AC1, BR2 | End to end | Document stored with the type TITLE_DEED given at upload; no classification answer, the type is taken as given |
| TC-E1-050-07 | AC6, BR5 | End to end | Answer produced before the link existed, applied by the daily re-drive |
| TC-E1-050-08 | AC5, BR5 | End to end | 20 documents already applied, the same events delivered again |
| TC-E1-050-09 | AC2, BR4 | End to end | CLASSIFY_THRESHOLD changed to 0.90 in rwb-document; the case receives the answer unchanged |
| TC-E1-050-10 | AC2, BR7 | End to end | Synthetic page with national ID number "0000000000000" and account number "TEST-ACC-0001"; no text reaches `rwb_case` |
| TC-E1-050-12 | BR1, BR7 | Contract | Each operation, event and activity of sections 12.1 to 12.5, checked against the rwb-document contract |
| TC-E1-050-13 | BR5, BR7 | Component | Boundary values of the tables of section 12.7 (ASM-3438): classifier version of 40 characters and of 41 characters (varchar(40) in the classification migration) |
| TC-E1-050-14 | AC9, BR6, BR8 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1050-APP-AC11) |
| TC-E1-050-15 | AC10 | Contract | Not specified in the source documents (NEWAC-RWB-P3-E1050-APP-AC12) |
| TC-E1-050-16 | AC11, BR5 | Component | Not specified in the source documents (NEWAC-RWB-P3-E1050-APP-AC13) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end and Access to Component. The classifier version is an opaque string of up to 40 characters, stored as rwb-document returns it; every fixture uses a synthetic value; the version label and its format are Not specified in the source documents (GAP-0764).

### 17. Guardrails

- No business value in code: the review reasons, the task codes, the checklist item states and the switch are data read through the parameters and reference-data contracts; the type codes and the labels belong to rwb-document.
- rwb-case never calls a model and never holds the classifier, the prompt, the OCR text or a threshold: it applies what the document hub answers, and the type table stays in `rwb_document`.
- No OCR text, no extracted field value and no document blob is copied into `rwb_case`; the link holds the document id, the type code, the classifier version, the confidence, the review reason and the two candidates with their confidences only.
- No personal data in logs, workflow inputs or events: the case router writes the document id, the case id and the event id, never a name, an address or an identity number, and workflow payloads pass the payload codec.
- No read of another service's tables and no foreign key across services: the checklist, the document and the type label come only through the rwb-document contract (DP-01).
- The confidence and the classifier version are stored as received; no rounding, no re-ranking and no comparison with a threshold happens in rwb-case (BR4).
- The review task carries IDs and codes only; MSG-P5-003 is shown on the screen, never written into the task row.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Classified into an agreed type with a confidence; below the threshold to review | Business Requirements Epic 1, section 3.5; Program, section 5.5 | FEAT-DCM-08 | 13 Manage documents and correspondence | R-UNI-32, R-UNI-40 | TC-E1-050-01 to TC-E1-050-16 |
| D-RCV-60 | Split of RWB-E1-050: the document hub keeps the OCR text, the classifier, the threshold and the type table; rwb-case keeps the checklist item, the review task, the timeline record, the decision record and the queue | Decision log, D-RCV-60; Template and Rules v1 §R6 | FEAT-DCM-08 | 13 Manage documents and correspondence | DP-01, DP-11 | TC-E1-050-01 to TC-E1-050-16 |

### 19. Out of scope

- The OCR of a scanned document and its intake item (legacy RWB-E1-049).
- The classifier, the model call, the threshold, the two candidates' ranking and the accuracy evaluation (legacy RWB-E1-050 AC1 to AC10, RWB-E1-060); they are built in RWB-P5-E1050-APP.
- The type table, the checklist master and the checklist completeness check `case_document_check` (P5, legacy RWB-E1-025 and RWB-E1-040).
- Field extraction and its confidence (legacy RWB-E1-053).
- The attach of the document to the case, the case-directory answers and the link itself (RWB-P3-E1032-APP).
- The review queue screen, the queue filters, the correction of a type and the outcome codes of a review task (RWB-P3-E1054-APP).
- Any change to `recovery_case.status` or to a stage, the timers that follow a checklist item and the case-list measures.
- The deployment of this capability: topic and queue provisioning, the Schedule registration, dashboards and the runbook (the OPS stories of the epic).
