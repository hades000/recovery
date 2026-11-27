# RWB-P3-E1054-APP Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- D-RCV-60 finishing pass: RD-P1-004.

| Item | Value |
|---|---|
| Story key | RWB-P3-E1054-APP |
| Work type | APP (App development) |
| Size | Not specified in the source documents (DOR-RWB-P3-E1054-APP-16) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-054 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P3-R |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1054-CON |
| Contract version | /v1 path of RWB-P5-E1054-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-DCM-005, REQ-DCM-019) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-054 for rwb-case; the review screen, the field corrections and the labeled set stay with rwb-document (P5). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P3-E1054-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (30 resolved, 23 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

### 1. Story

As a **litigation officer**, I want **the review task of every doubtful document on my cases to sit on one rwb-case review queue with the reason the pipeline could not settle it, the two candidate types, the confidence and the age, and the case record to show what was decided on it**, so that **no doubtful document is attached to a case without a person working it, and every work item on a case has a queue, an owner and a recorded outcome**.

### 2. Business rationale

A wrong type or a wrong hearing date on a court notice puts the wrong date on the case and the litigation timers run from it. Today the officer works a case without a record of which document was doubtful, why it was doubtful, or what was decided: the doubtful document sits in a queue of the document hub while the case shows only the stored file, so a case manager cannot see the outstanding work on a case and the litigation clock starts from a date nobody has confirmed.

**The split under D-RCV-60.** OCR, classification, extraction, matching, the review screen, the field confirm and correct, the type change, the attach and the labeled set are rwb-document's (P5): rwb-document holds the intake items, the OCR text, the fields, the type list in force, the review reasons and the labeled examples, and it renders the document. rwb-case owns the work side: the review queue, the task that points at the document, the scope rule that decides who sees the task, the case timeline entry and the decision record. This story builds no screen content of its own and corrects no value.

Under the target rules rwb-case reads no document table (DP-01): the review item, the two candidate types, the confidence, the reason and the outcome come through the P5 review contract, one hop with a 2 s timeout (DP-11), and the review reason and task codes come as reference data through the contracts of rwb-case (DP-07). `DocumentStored` reaches rwb-case as an event through the inbox, one action per event (DP-09). The queue counts and ageing are published from rwb-case for the case list and for reporting, so the measure "fields extracted without review" moves with each worked item. It meets REQ-DCM-005 and REQ-DCM-019, and it keeps the audit position that a discarded item is never removed silently, because the reason stays on the closed task and on the case timeline.

### 3. Preconditions

- RWB-P5-E1054-CON is published: the review-item resource, the review outcomes, the field review resources, the error envelope, the Idempotency-Key rule and the contract fake. The review item carries the document ID, the case number when it has one, the review reason, the predicted type, the two candidate types with their confidence, the received time and the item version.
- The rwb-case queue model is in force: `queue`, `queue_member` and `queue_measure` exist in `rwb_case` (RWB-P3-E1019-APP), and the queues of the review teams are loaded as data with their team code, their role code and their overflow queue.
- The reference lists are in force through the contracts of rwb-case (DP-07): the review reasons LOW_CONFIDENCE, UNKNOWN_TYPE, MODEL_UNAVAILABLE, RESCAN, UNREADABLE_FILE, EXTRACTION_FAILED, NO_MATCH, MULTIPLE, CONFLICT and CASE_CLOSED as the legacy story lists them, the task codes of the review task, and the review outcomes the P5 answer reports (ATTACHED, DISCARDED, CONFIRMED, CORRECTED).
- The task model is in force: `task` carries `task_code`, `element_type`, `status`, `owner_role`, `due_at`, `completed_at` and `outcome_code`; `assignment` carries the queue a task sits on.
- The case review task code, its element type and its status values are held as reference data in the rwb-case reference tables and loaded with RWB-P3-E1043-CON before this story starts; their values are Not specified in the source documents (GAP-0746).
- The review task code, the review state values and the case-side decision code are reference rows loaded through the reference-data contract; the field IDs of the four review link columns on `task` (`document_ref`, `review_reason`, `item_version`, `review_state`) are Not specified in the source documents (GAP-0757) until the next data dictionary version.
- The review team parameter the case loads, `REVIEW_TEAM_UNATTACHED`, is in force as data. Its production value is Not specified in the source documents (GAP-0755; ASM-1376).
- The review queue switch of rwb-case is a parameter read through the parameters contract and stored in the platform flag library; its name is Not specified in the source documents (GAP-0756). Off means no review task is raised and the review queue answers no row.
- The gateway-bff composite route is published (RWB-PLT-N001-CON, DP-19), with the review queue screen route that calls rwb-case for the queue and rwb-document for the item detail and the file.
- The rwb-case service identity (DP-02) exists in the environment as one login for this service. Its name is Not specified in the source documents (GAP-0758; ASM-1379).
- Depends on (build) is None: the story builds on Day 1 against the P5 contract fake and the published contracts of the platform.

### 4. Flow

1. rwb-document: the intake workflow stores the document, its fields and its review reason, and publishes `DocumentStored` (EV-16) on `rwb.document.events.v1` through its outbox (DP-09).
2. rwb-case: the case router consumes the event through its inbox, so a duplicate delivery never acts twice, and signals `CaseWorkflow` on task queue `rwb-case` with the document ID and the item version.
3. `CaseWorkflow`: the `RaiseReviewTask` activity reads the review item through `GET /review-items` on the P5 contract — reason, predicted type, the two candidate types with their confidence, received time, case number, item version — and matches the case number to `recovery_case` by `case_no`.
4. `RaiseReviewTask`: `RecordAndApply` writes, in one `rwb_case` transaction, the `task` row (task code from the reference list, `element_type` HUMAN_TASK, status OPEN, `owner_role` from the role code of the queue), the `assignment` row that places the task on the review queue, `task.document_ref`, `task.review_reason` and `task.item_version`, and the `review_state` PENDING_REVIEW. A task for the same document that is still OPEN or IN_PROGRESS is reused, never doubled.
5. Officer: opens the review queue through gateway-bff; the composite route calls `GET /queues` and `GET /queues/{queueId}/cases` on rwb-case for the rows and, for the open item, `GET /documents/{documentId}` and the file on rwb-document.
6. `ReviewScopeResolver`: the queue answers only the rows in scope — an item with a case is shown to the queue of the case's team and to roles whose scope covers the case, an item with no case is shown to the review team named in the parameter the case reads — oldest first, paged.
7. Officer: opens the case and works the item on the case screen; the type, the case and the field corrections are made on the P5 screen through the P5 contract, and rwb-case holds references only.
8. Officer: completes the task with `PATCH /tasks/{taskId}` and status DONE; `RecordReviewOutcome` calls `POST /documents/{documentId}/review` on the P5 contract with the `Idempotency-Key` and the item version.
9. The P5 answer reports ATTACHED, DISCARDED, CONFIRMED or CORRECTED. `RecordAndApply` writes, in one transaction, the one interaction (timeline) entry of the case, the decision record of the library (DP-03) and the task completion with its `outcome_code`, moves `task.review_state` from PENDING_REVIEW to CONFIRMED or CORRECTED as the answer reports it, and puts `DecisionRecorded` in the outbox.
10. A stale item version (409) or an answer outside the allowed states leaves the task open, reloads the item at the version in force and writes nothing.
11. A P5 timeout leaves the task open; the next run of `CaseWorkflow` retries the completion once with the same `Idempotency-Key`, and the outcome is recorded once when the answer arrives.
12. rwb-case: `queue_measure` takes the count and the age of the review queue and publishes them for the case list and for reporting; the case documents screen shows the confirmed type.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Another officer saved the same review item first, so the item version is stale | The task stays open, nothing is written, the item is reloaded at the version in force and the officer resends | MSG-GEN-004 | AC6 |
| X2 | rwb-document does not answer inside the 2 s budget or answers 503 | One hop, 2 s timeout (DP-11); the task stays open with no timeline entry and no decision record, and the next run retries once | MSG-GEN-006 | AC7 |
| X3 | The decision record cannot be written on completion | Nothing is recorded; the task stays open, the timeline holds no entry and the review state stays PENDING_REVIEW; an incident is raised | MSG-P7-003 | AC10 |
| X4 | A role without Case record R reads or completes a review task | 403 before any write; the task is unchanged | MSG-P4-002 | AC3 |
| X5 | The task or the queue is outside the caller's scope | 404; nothing is returned and nothing is written | MSG-P4-003 | AC3 |
| X6 | The P5 answer refuses the attach because the chosen case is closed | The task stays open with the P5 reason on it; no timeline entry and no decision record | MSG-P5-005 | AC6 |
| X7 | The P5 answer refuses a type that is not in force | The task stays open; the officer picks a type from the list in force | MSG-P5-006 | AC6 |
| X8 | The P5 answer refuses a field still in review or an empty value | The task stays open; no outcome is recorded | MSG-GEN-001 | AC6 |
| X9 | The same file is already on the chosen case | The P5 answer links the existing document; the case records one outcome and names that document | MSG-P5-024 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Ready on Day 1: rwb-case builds against the published P5 review contract and its fake, the rwb-case queue model, the task model and the gateway-bff route; no build dependency and no waiting story |
| Negotiable | The review team, the page size, the review reasons, the task codes and the review states are data loaded through the contracts of rwb-case; the story fixes the behaviour and the scope rule |
| Valuable | Puts the doubtful document on the case as a work item with a queue, an owner, a reason and a recorded outcome, so no wrong type or wrong date reaches a litigation clock unseen |
| Estimable | One event handler, three activities, four read and update endpoints, one scope resolver, one timeline writer and one decision record |
| Small | Fits two weeks with its tests; no document table, no OCR text and no field value is stored or rendered |
| Testable | Every scenario of section 7 is one test against the P5 fake with synthetic documents and cases; the reason, the candidates and the confidence are asserted as the P5 answer carries them |

### 7. Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents

  Background:
    Given DOCTYPE-2026.11 is in force and the classify_threshold of every type is 0.8000
    Given the review team parameter the case loads, REVIEW_TEAM_UNATTACHED, is "LIT-BKK" for this test
    Given queue "LIT-BKK-OFF" is in force with team code "LIT-BKK" and role code RW-LITOFF
    Given a litigation officer "U-LIT-01" with role RW-LITOFF in team "LIT-BKK" with team scope

  Scenario: AC1 The review queue lists the review tasks in scope, oldest first (new, D-RCV-60)
    Given the rwb-document contract mock returns review items "IN-0101" received 2026-11-02, "IN-0102" received 2026-11-04 and "IN-0103" received 2026-11-03, each with reason "LOW_CONFIDENCE" and a candidate case of team "LIT-BKK"
    Given a review item of team "HP-NE" received 2026-11-02
    When "U-LIT-01" reads GET /api/recovery/case/v1/queues/{queueId}/cases for queue "LIT-BKK-OFF"
    Then the page lists three review tasks in the order 2026-11-02, 2026-11-03, 2026-11-04
    Then no task of team "HP-NE" is in the page
    Then each row carries the document ID, the review reason, the two candidate types, the confidence and the age in days

  Scenario: AC2 An item with no case goes to the named review team only (new, D-RCV-60)
    Given the rwb-document contract mock returns review item "IN-0110" with reason "UNREADABLE_FILE", no case number and no candidate case
    Given the review team parameter the case loads is "LIT-BKK"
    When the review task for "IN-0110" is raised and "U-LIT-01" reads the review queue
    Then "IN-0110" is listed as one review task on queue "LIT-BKK-OFF"
    When an officer "U-LIT-02" of team "HP-NE" reads the review queue
    Then "IN-0110" is not in that page

  Scenario: AC3 An out-of-scope task is 404 and a role without Case record R is 403 (new, D-RCV-60)
    Given review task "TSK-0111" belongs to a case of team "HP-NE"
    Given the rwb-document contract mock returns the review item of "DOC-0111" with a case number of team "HP-NE"
    When "U-LIT-01" calls GET /api/recovery/case/v1/queues/{queueId}/cases for a queue of team "HP-NE"
    Then the response is 404 with MSG-P4-003
    Given user "U-REF-01" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-REF-01" calls GET /api/recovery/case/v1/me/tasks
    Then the response is 403 with MSG-P4-002
    When "U-REF-01" calls PATCH /api/recovery/case/v1/tasks/{taskId} with status "DONE"
    Then the response is 403 with MSG-P4-002 and the task is unchanged

  Scenario: AC4 Completing an item records one timeline entry, one decision record and closes the task (new, D-RCV-60)
    Given review task "TSK-0101" on case "RW-2026-000201" with status "OPEN", document "DOC-0103" and review state "PENDING_REVIEW"
    Given the rwb-document contract mock returns outcome "CORRECTED" for the review call on "DOC-0103" with review_status "CORRECTED"
    When "U-LIT-01" calls PATCH /api/recovery/case/v1/tasks/{taskId} with status "DONE" and outcomeCode "CORRECTED"
    Then the task status is "DONE" with completed_at set, outcome_code "CORRECTED" and review state "CORRECTED"
    Then the case timeline of "RW-2026-000201" holds exactly one entry that names "DOC-0103", the reason "LOW_CONFIDENCE" and the outcome "CORRECTED"
    Then exactly one decision record exists for the task and DecisionRecorded is published on rwb.decision-record.v1
    Then the case status is unchanged

  Scenario: AC5 A second completion changes nothing (new, D-RCV-60)
    Given review task "TSK-0101" is "DONE" with outcome "CORRECTED", the timeline holds one entry and one decision record exists
    When the same PATCH with status "DONE" and outcomeCode "CORRECTED" arrives again
    Then the response is 200 with the saved task
    Then completed_at and the outcome_code are unchanged
    Then the timeline still holds one entry and no second decision record is written
    Then a duplicate DocumentStored for "DOC-0103" raises no second task and changes no review state

  Scenario: AC6 A stale item version leaves the task open with MSG-GEN-004 (new, D-RCV-60)
    Given review task "TSK-0107" is "IN_PROGRESS" with the review item at version 3
    Given the rwb-document contract mock returns 409 with MSG-GEN-004 for the review call at version 3
    When "U-LIT-01" calls PATCH /api/recovery/case/v1/tasks/{taskId} with status "DONE" and the item version 3
    Then the response is 409 with MSG-GEN-004
    Then the task stays open and the case timeline holds no entry for it
    Then the item is reloaded through the P5 contract at the version in force

  Scenario: AC7 A P5 timeout leaves the task open and the next run retries (new, D-RCV-60)
    Given review task "TSK-0108" is "IN_PROGRESS" with the review item at version 5
    Given the rwb-document contract mock returns no answer inside 2 s on the review call
    When "U-LIT-01" completes "TSK-0108"
    Then the task stays open with no timeline entry and no decision record
    Then the next run of CaseWorkflow retries the completion once with the same Idempotency-Key
    When the P5 answer then reports "CONFIRMED" at version 5
    Then exactly one timeline entry and exactly one decision record exist for the task

  Scenario: AC8 An empty queue returns the empty state (new, D-RCV-60)
    Given no review task for queue "LIT-BKK-OFF"
    When "U-LIT-01" reads GET /api/recovery/case/v1/queues/{queueId}/cases for queue "LIT-BKK-OFF"
    Then the page holds no row
    Then the screen shows the empty state "No documents are waiting for review."

  Scenario: AC9 The queue shows the reason, both candidates and the confidence exactly as the P5 answer carries them (new, D-RCV-60)
    Given the rwb-document contract mock returns review item "IN-0101" with reason "LOW_CONFIDENCE", predicted type "COURT_NOTICE" at 0.6200 and the candidates "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100
    When "U-LIT-01" reads the review queue
    Then the row shows reason "LOW_CONFIDENCE", the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21", and confidence 0.6200
    Then the row carries no OCR text, no field value and no personal data
    Then the task row in rwb_case holds the document ID, the reason, the item version and the review state only

  Scenario: AC10 A failed decision record leaves the task open (new, D-RCV-60)
    Given review task "TSK-0101" is "IN_PROGRESS" and the decision-record library is switched to fail by the agreed test-only switch
    When "U-LIT-01" calls PATCH /api/recovery/case/v1/tasks/{taskId} with status "DONE"
    Then the response is 503 with MSG-P7-003
    Then the task stays open, the timeline holds no entry and the review state stays "PENDING_REVIEW"
    Then an incident is raised and the officer retries after the record can be written

  Scenario: AC18 The rules BR1, BR8, BR9 and BR10 hold on the rwb-case side (new, D-RCV-60)
    Given review task "TSK-0101" is "OPEN" on document "DOC-0103"
    When a duplicate DocumentStored for "DOC-0103" arrives
    Then the task is reused and no second task is created for "DOC-0103"
    Then the task row holds the document ID, the reason, the item version and the review state only
    Then the review team, the page size, the review reasons and the review states are read from the rwb-case parameter rows, and a changed row changes the result with no code change
    Then the queue measure rows publish the count and the age of the queue from rwb_case and no threshold is applied

  Scenario: AC19 A request without a valid token to a provided operation is 401 (new, D-RCV-60)
    Given the request carries no valid token
    When the request calls GET /api/recovery/case/v1/me/tasks
    Then the response is 401
    When the request calls PATCH /api/recovery/case/v1/tasks/{taskId} with status "DONE"
    Then the response is 401 and the task is unchanged

  Scenario: AC20 A status change the model does not allow is refused (new, D-RCV-60)
    Given review task "TSK-0101" is "DONE" with outcome "CORRECTED"
    When "U-LIT-01" calls PATCH /api/recovery/case/v1/tasks/{taskId} with status "OPEN"
    Then the request is refused with the code Not specified in the source documents (NEWAC-RWB-P3-E1054-APP-AC20)
    Then the task stays "DONE" with outcome "CORRECTED" and the case timeline is unchanged
```

The criteria above are new under D-RCV-60 and test the rwb-case deliverable only: the queue, the task, the scope rule, the timeline entry, the decision record and the case-side review state. This story owns no legacy acceptance criterion; the legacy AC1 to AC17 are P5's, where the screen, the OCR text, the field corrections, the type change, the attach and the labeled set are proved.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One review task per review item: a task for a document that is still OPEN or IN_PROGRESS is reused, and a duplicate `DocumentStored` raises no second task | RWB-E1-054 BR1; DP-09 inbox |
| BR2 | The review queue, the task, the scope rule, the timeline entry and the decision record are rwb-case's; the correction, the type change, the attach, the OCR text, the fields and the labeled set are rwb-document's | D-RCV-60 split; Arch v5 slide 41 (P3 queues and tasks, P5 metadata and OCR) |
| BR3 | Scope decides visibility: an item with a case is shown to the queue of the case's team and to roles whose scope covers the case; an item with no case is shown to the review team named in the rwb-case parameter row, which RW-COE agrees for each environment | RWB-E1-054 BR2; CTL-09; GAP-0755; ASM-1376 |
| BR4 | The queue lists the review tasks oldest first by the received time of the P5 answer, and pages through the queue read | RWB-E1-054 AC14; FSD P3 v4 A2.38 |
| BR5 | The outcome is recorded once, with the decision record and the review state of the task, in one transaction; a failure of the decision record rolls the whole completion back | R-UNI-39; Principle 5; DP-03 |
| BR6 | A completion saved against an old item version is refused with 409 and leaves the task open; a repeated completion returns the saved task and changes nothing | RWB-E1-054 BR8; MSG-GEN-004 |
| BR7 | Nothing is deleted when an item is discarded: the P5 answer keeps the file and its reason, and the case keeps the closed task with the outcome DISCARDED and the reason on its timeline | REQ-DCM-019 |
| BR8 | No intake field and no document field is stored in `rwb_case`: the task holds the document ID, the reason, the item version and the review state, and the item is read through the P5 contract; the task carries no P2 field classed as personal data, and such a field is read through the P5 contract only | DP-01; D-RCV-60 split |
| BR9 | No business value in code: the review team, the page size, the review reasons, the task codes and the review states are data read through the contracts of rwb-case | DP-07; BR-P3-006; the task codes are Not specified in the source documents (GAP-0757; ASM-1378); the case-side decision code is Not specified in the source documents (GAP-2456) and is read through the reference-data contract of rwb-case |
| BR10 | The queue measures publish the count and the age of the queue as taken from `rwb_case`; no threshold is set in this story | TSD P3 v3 T3.1 `queue_measure` (DF-RPT-020 to DF-RPT-030); FSD P3 v4 A2.38 |

Where each rule lives in the target: BR1, BR2, BR5 and BR8 are answered inside `rwb_case`; BR3 is answered by the scope of the rwb-access authorise answer and by the queue's team code; BR4, BR9 and BR10 are answered from `rwb_case` rows and the reference data of rwb-case. The item, its reason and the outcome come from rwb-document only, never from a document table (DP-01, DP-11).

### 9. State transitions

No case status change: this story moves no `recovery_case.status` and writes no value of LOV-CASE-STATUS. It moves the review task and the case-side review state of the document link.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| task | None | DocumentStored (EV-16) or a P5 review item read | The item is in the review queue and its case is found | OPEN |
| task | OPEN | The officer opens the item | The caller holds Case record R in scope | IN_PROGRESS |
| task | IN_PROGRESS | P5 answer ATTACHED, CONFIRMED or CORRECTED | The decision record and the timeline entry commit in one transaction | DONE |
| task | IN_PROGRESS | P5 answer DISCARDED | The reason is present and the decision record commits | DONE (outcome_code DISCARDED) |
| task | OPEN or IN_PROGRESS | A refusal, a stale version or a timeout | Nothing is written | unchanged, retried on the next run |
| task.review_state | PENDING_REVIEW | P5 answer CONFIRMED | — | CONFIRMED |
| task.review_state | PENDING_REVIEW | P5 answer CORRECTED | — | CORRECTED |
| task.review_state | PENDING_REVIEW | P5 answer DISCARDED | No document is linked to the case | unchanged; the task closes with outcome DISCARDED and the reason stays on the timeline |

The task status vocabulary is LOV-TASK-STATUS (OPEN, IN_PROGRESS, DONE, CANCELED) in TSD P3 v3 T3.2. Every task status in the table, including the From values, is a LOV-TASK-STATUS value; DONE carries the outcome in task.outcome_code. The review state values PENDING_REVIEW, CONFIRMED and CORRECTED are read from the reference list in force; the case-side list is data (BR9). They are not values of LOV-CASE-STATUS, which governs recovery_case.status only. The state table has no row for recovery_case.status; each status value in it belongs to the task or task.review_state named in its Object column.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Raises the review task, reads the item through the P5 contract, writes the timeline entry, the decision record and the task completion |
| RW-LITOFF, litigation officer | Reads the review queue and works and completes the review tasks in scope (Case record RU; Queue and allocation R) |
| RW-CASEOWN, case owner | Reads and works the review tasks of own cases (Case record R; Queue and allocation R) |
| RW-TEAMMGR, team manager | Reads the queue and the review tasks of the team (Case record R; Queue and allocation CRUA); completes no review task |
| RW-COE, center of excellence analyst | Reads the queue and its measures (Case record R; Queue and allocation R); owns the reasons and the task codes as data |
| The document hub identity (P5) | Owns the item, the reason, the candidates, the OCR text, the fields, the type list, the outcome and the labeled set; answers the review call |
| RW-REFADM | Has no Case record right; refused on the read and the update endpoints |
| Decision-record library identity | Writes the local decision record and its outbox row (Decision log C) |

Every "who" in this table is a **role code** held as data in rwb-access (P4); rwb-case asks the rwb-access authorise contract through the guard library, caches the answer for the life of the call and never reads an `rwb_access` table (DP-01, DP-08; RWB-P4-E1037-CON). The per-service login name is Not specified in the source documents (GAP-0758; ASM-1379), so the story names it "the rwb-case login (DP-02)" until it is agreed.

### 11. Data

| BR Field ID | Entity in rwb_case | Field | Read or write |
|---|---|---|---|
| DF-WRK-001 to DF-WRK-008, DF-WRK-037, DF-WRK-038 | queue | queue code, name, team code, role code, assignment method, cap, overflow queue, cursor, table version | Read |
| DF-WRK-045 to DF-WRK-052 | queue_member | membership, capacity, skills and validity of the review teams | Read |
| DF-RPT-020 to DF-RPT-030 | queue_measure | depth, unassigned, average age, maximum age, owner spread, breaches, status | Write |
| DF-WRK-017 to DF-WRK-026 | task | all fields, including `task_code` (DF-WRK-019) and `owner_role` (DF-WRK-023), plus `document_ref`, `review_reason`, `item_version` and `review_state` | Write |
| DF-WRK-009 to DF-WRK-016, DF-WRK-039, DF-WRK-040 | assignment | the queue a task sits on, the assignee and the assignment reason | Write |
| DF-CAS-001, DF-CAS-002, DF-CAS-005 | recovery_case | id, case_no, status | Read |
| DF-CAS-009, DF-CAS-010, DF-CAS-011, DF-CAS-012 | recovery_case | owner, queue, team code, region code | Read |
| DF-CAS-026 | case_account | account_id | Read |
| DF-INT-001 to DF-INT-029 | interaction | the case timeline entry of the review outcome (`event_code`, `summary`, `source_ref`, `decision_log_id`, `actor_type`, `actor_ref`) | Write |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write |
| DF-REF-132 to DF-REF-158 | parameter_catalog, parameter_value | the review team parameter and the rwb-case switch | Read |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row | the review reasons, the task codes and the review states in force | Read |

The document side is read only through the P5 contract and never stored: the document ID, the case number, the review reason, the predicted type, the two candidate types with their confidence, the received time, the item version and the review outcome. No OCR text, no field value, no personal data and no intake row is written into `rwb_case` (BR8). `task.document_ref`, `task.review_reason`, `task.item_version` and `task.review_state` are the case-side review link columns added by this story; their field IDs in the Logical Data Model and Data Dictionary are Not specified in the source documents (GAP-0757; ASM-1378), so the table cites DF-WRK-017 to DF-WRK-026 and names the four columns. The task code and the case-side decision code are likewise data values loaded through the reference-data contract, not constants (BR9).

Field IDs are those in the Logical Data Model and Data Dictionary v9. rwb-case reads no table of another service and holds no foreign key across services (DP-01).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3, ownership map).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/queues` | List the queues in the caller's scope with their count and age, including the review queue of the team | Queue and allocation R, scope applied | Not applicable |
| GET | `/queues/{queueId}/cases` | List the work rows of a queue, oldest first, paged; for the review queue each row is one review task with the document ID, the case number, the reason, the two candidates, the confidence and the age | Queue and allocation R, scope applied | Not applicable |
| GET | `/me/tasks` | List the caller's open review tasks | Case record R, scope applied | Not applicable |
| PATCH | `/tasks/{taskId}` | Complete a review task with status, outcome code and a comment | Case record U, scope applied | Not applicable |

The paging operation is the one named `GET /queues/{queueId}/cases` in the ownership map (API-P3-011). For a case queue each row is a case; for the review queue each row is one review task of the queue, so the answer carries the task fields of section 12.1 in place of the case fields. Response fields per the case contract story: task `id`, `caseId`, `documentRef`, `taskCode`, `status`, `ownerRole`, `reviewReason`, `reviewState`, `itemVersion`, `dueAt`, `outcomeCode`, `completedAt`; queue `id`, `queueCode`, `teamCode`, `roleCode`, `depth`, `avgAgeDays`, `maxAgeDays`. Errors: 401 no session (MSG-P4-001), 403 no Case record R or no Queue and allocation R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 409 stale version (MSG-GEN-004), 422 a page size outside its range (MSG-GEN-002), 503 store or dependency down (MSG-GEN-006).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/review-items` | rwb-document (P5) | The reason, the predicted type, the two candidates, the confidence, the received time, the case number and the item version of a review item | One hop, 2 s (DP-11) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | rwb-document (P5) | The document, its type, its `review_status` and its state after the review call | One hop, 2 s (DP-11) |
| POST | `/api/recovery/document/v1/documents/{documentId}/review` | rwb-document (P5) | Complete the review of the item with the officer's action, the item version and the `Idempotency-Key`, and receive the outcome ATTACHED, DISCARDED, CONFIRMED or CORRECTED | One hop, 2 s (DP-11) |

The three operations are the review contract of RWB-P5-E1054-CON. A repeated POST with the same `Idempotency-Key` returns the first result and changes nothing (BR6). The item detail and the file of the screen are read by gateway-bff on the same contract and are not called by rwb-case.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 | caseId | caseId, taskId, documentRef, review reason code, review outcome, decision record reference |

The event is written to the outbox in the same transaction as the task completion and the timeline entry, and relayed with the CloudEvents envelope; no personal data, no field value and no OCR text is carried (DP-09). The decision code of the case-side record is a data value from the reference list in force (BR9).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 | Case router, inbox dedupe, `signalWithStart` of `CaseWorkflow` for the document ID, which raises one review task |

A duplicate delivery is absorbed by the inbox and raises no second task (BR1).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case-{caseId}) | `rwb-case` | Carries the review task of each doubtful document on the case from the event to the recorded outcome |
| Human task with SLA | Workflow kit template (RWB-PLT-E1071-CON) | `rwb-case` | Holds the review task, its owner role and its due time; the escalation policy is the platform template's |
| RaiseReviewTask | Activity | `rwb-case` | Reads the review item through the P5 contract and raises or reuses the one task on the review queue |
| RecordReviewOutcome | Activity | `rwb-case` | Calls the P5 review operation with the `Idempotency-Key` and the item version and returns the outcome |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the timeline entry, the decision record, the task completion and the outbox row in one transaction |

Workflow code reads no clock, does no I/O and calls no contract directly; every call is inside an activity.

#### 12.6 Schedules

None. The review task is raised by `DocumentStored` (EV-16) and by the P5 review item, and worked by the officer; this story adds no Temporal Schedule and moves no clock. The queue measure snapshot is taken by the queue measure story of RWB-E1-030.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| queue | rwb_case | P3 | Reads the review queue, its team code and its role code |
| queue_member | rwb_case | P3 | Reads the membership of the review teams |
| queue_measure | rwb_case | P3 | Writes the count, the age and the breach count of the review queue |
| task | rwb_case | P3 | Writes the review task, its outcome and the four review link columns |
| assignment | rwb_case | P3 | Writes the row that places the task on the review queue |
| recovery_case | rwb_case | P3 | Reads the case, its team code and its scope; writes no status |
| case_account | rwb_case | P3 | Reads the account link of the case for the scope answer |
| interaction | rwb_case | P3 | Writes the one timeline entry of the review outcome |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | PLT | Outbox, inbox and idempotency objects (DP-09) |

`document`, `document_field`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` are P5 tables in `rwb_document` and are **never read**; the item comes through the P5 contract only (DP-01). `role`, `permission`, `masking_rule` and `delegation_limit` are P4 tables in `rwb_access` and are reached over the authorise contract only. No statement in this story names a table in another schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The P5 review contract of RWB-P5-E1054-CON | `GET /review-items` with items in and out of scope, with and without a case, and with the ten review reasons; `GET /documents/{documentId}` with `review_status` PENDING, CONFIRMED and CORRECTED; `POST /documents/{documentId}/review` answering ATTACHED, DISCARDED, CONFIRMED, CORRECTED, 409 MSG-GEN-004, 422 MSG-P5-005, MSG-P5-006, MSG-GEN-001, MSG-P5-024 and a 2 s timeout |

The rwb-access authorise answer and the decision-record library come from the platform contract stories (RWB-PLT-E1037-CON, RWB-PLT-E1027-CON) and are not faked here.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | Queue and task reads and the task update provided; the P5 review item, document and review call consumed; one hop, 2 s timeout |
| Kafka | 1 published, 1 consumed | `rwb.decision-record.v1` published; `rwb.document.events.v1` consumed |
| Temporal | 1 workflow, 3 activities | CaseWorkflow with the kit Human task template; RaiseReviewTask, RecordReviewOutcome, RecordAndApply |
| File | None | This story reads and writes no file; the file of the item is gateway-bff's call on the P5 contract |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `reviewqueue`, Java package `th.co.scb.ace.workbench.recovery.case.reviewqueue`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the platform contract stories this story builds on; they arrive as platform CON work, so Depends on (build) stays None and the story is ready on Day 1.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReviewQueueService | Service | Builds the review queue rows with the scope rule, the oldest-first order and the paging, and takes the queue measure snapshot |
| ReviewScopeResolver | Service | Answers the scope of one row: the case scope for an item with a case, the review team of the parameter for an item without one |
| ReviewTaskRepository | Repository | `task`, `assignment`, `queue_measure` and the review link columns; writes only schema `rwb_case` |
| ReviewItemClient | Client | Calls the P5 review contract for the item, the document and the review call; one hop, 2 s, `Idempotency-Key` on the POST |
| TimelineWriter | Service | Writes the one interaction entry of the outcome with its event code, source reference and actor |
| DecisionRecordClient | Client | Writes the local decision record through the library and the outbox row (DP-03) |
| TaskController | Controller | `GET /me/tasks` and `PATCH /tasks/{taskId}` with the access check and the scope |
| QueueController | Controller | `GET /queues` and `GET /queues/{queueId}/cases` with the access check, the scope, the order and the paging |
| ReviewTaskActivities | Activity | `RaiseReviewTask`, `RecordReviewOutcome` and `RecordAndApply` inside `CaseWorkflow` |

**Database and migrations**

- Migration `V1054__review_queue.sql`, on the per-service Flyway sequence after the V0001 baseline (DP-15), adds to `task`: `document_ref` varchar(40), `review_reason` varchar(20), `item_version` integer, `review_state` varchar(15); creates the partial unique index `ux_task_review_document ON task (document_ref) WHERE status IN ('OPEN','IN_PROGRESS')` so one document has at most one open review task; creates `ix_task_review_status ON task (task_code, status, due_at)` and `ix_assignment_queue_task ON assignment (queue_id, task_id)` for the queue read and the oldest-first page.
- No other column and no other table is added. The four review link columns hold references and code values only, never a field value or an OCR text (BR8).

**Configuration and reference data**

- The review team parameter the case loads (`REVIEW_TEAM_UNATTACHED`), the page size and the rwb-case feature switch, through the parameters contract (DP-06); the values are data and the production values are Not specified in the source documents (GAP-0755; ASM-1376) and (GAP-0756; ASM-1377).
- The review reasons, the review task codes and the review states, through the reference-data contract (DP-07); no code constant holds a reason, a task code or a state (BR9). Their exact values are Not specified in the source documents (GAP-0757; ASM-1378).

**Build steps**

1. Write `V1054__review_queue.sql` and the two indexes; repository tests for the one-task-per-document constraint.
2. Build `ReviewItemClient` over the P5 fake: the review item, the document and the review call with the `Idempotency-Key`, the 409, the 422 answers and the 2 s timeout; tests for AC6, AC7 and AC9.
3. Build `RaiseReviewTask` and the inbox handler of `DocumentStored` with the reuse of an open task; tests for AC1 and AC4 (duplicate event).
4. Build `ReviewScopeResolver` with the case scope and the review team of the parameter; tests for AC1, AC2 and AC3.
5. Build `QueueController` with the oldest-first order and the paging; tests for AC1 and AC8.
6. Build `TaskController` and `RecordReviewOutcome` with the access check and the scope; tests for AC3 and AC6.
7. Build `RecordAndApply`, `TimelineWriter` and the decision record in one transaction, with the failed-record rollback; tests for AC4, AC5 and AC10.
8. Build the queue measure snapshot for the review queue and the contract-fake run of every cross-service answer, so the story builds before P5 exists.

**Feature switch.** The legacy flag `rwb.dochub.review` stays with rwb-document (P5). The rwb-case switch is a parameter read through the parameters contract; off means no review task is raised and the review queue answers no row, while the document hub's own review queue is unaffected. Its name is Not specified in the source documents (GAP-0756; ASM-1377).

**Done when.** The tests in section 16 pass, the review queue of each team reconciles to the P5 review-item count of the day with zero unexplained difference, no document field and no OCR text is stored in `rwb_case`, every completed review task has one timeline entry and one decision record, and the contract tests of RWB-P5-E1054-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | An item or document is in the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P5-005 | The P5 answer refuses the attach because the chosen case is closed | Case {case} is closed. Choose an open case. |
| MSG-P5-006 | The P5 answer refuses a type that is not in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-P5-024 | The file is already on the chosen case | This file is already on the case as {document}. |
| MSG-GEN-001 | A field still in review or an empty value on the P5 answer | Enter {field}. |
| MSG-GEN-002 | A page size or a date outside the allowed range | {field} must be between {min} and {max}. |
| MSG-GEN-004 | The completion was saved against an old item version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-006 | The P5 contract does not answer inside the budget or answers 503 | {system} is not available. Try again in a few minutes. |
| MSG-P7-003 | The decision record cannot be written on completion | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-001 | Not specified in the source documents (DOR-RWB-P3-E1054-APP-9) | Not specified in the source documents (DOR-RWB-P3-E1054-APP-9) |
| MSG-P4-002 | The caller lacks Case record R or Queue and allocation R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The queue or the task is outside the caller's scope | This case is not in your scope. |

The message IDs and the wording are copied from RWB-E1-054, where they exist there; MSG-GEN-006 is copied from the shared message list. No new message ID is added by this story. Thai text for each message follows decision DL10, which is open under assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863, all confirmed by the programme directive.

### 15. Screens and states

The screen itself is rwb-document's: the review screen, the file, the OCR text, the type chooser, the case chooser and the field confirm and correct belong to P5. This story serves the queue rows and the task update that the screen shows, through the gateway-bff composite route (DP-19), which calls rwb-case for the queue and rwb-document for the item detail and the file.

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the queue loads through the composite route |
| SCR-31 Document review queue | List | Review tasks oldest first with the reason, the two candidates, the confidence and the age; a row opens the item detail from rwb-document and the case from rwb-case |
| SCR-31 Document review queue | Reviewed | After the completion the task leaves the queue, the case timeline shows the outcome and the case documents screen shows the confirmed type |
| SCR-31 Document review queue | Empty (common state) | "No documents are waiting for review." |
| SCR-31 Document review queue | Error | The queue read answers 503 or the P5 contract does not answer inside the 2 s budget (DP-11): the screen shows MSG-GEN-006 and offers a retry; no row is dropped and the task stays open |
| SCR-31 Document review queue | No access | The caller lacks Queue and allocation R or asks for a queue outside the caller's scope: the screen shows MSG-P4-002 or MSG-P4-003 and returns no row |
| SCR-30 Case documents | List | The document with the confirmed or corrected type, and the review task of the case closed with its outcome |
| SCR-30 Case documents | Loading | Skeleton rows while the case documents and the review task of the case load through the composite route |
| SCR-30 Case documents | Empty | The case holds no document and no review task: the list shows no row and the screen states that no document is on the case |
| SCR-30 Case documents | Error | The case read or the P5 document read answers 503 or times out (DP-11): the screen shows MSG-GEN-006 and offers a retry |
| SCR-30 Case documents | No access | The caller lacks Case record R or the case is outside the caller's scope: 403 with MSG-P4-002 or 404 with MSG-P4-003, and no document is shown |

The layout, the field-level masking and the composite route specification of the two screens are P5's and the platform's, contracted in RWB-P5-E1054-CON and RWB-PLT-N001-CON; this story fixes the queue rows, the task update and the states only.

### 16. Test cases

The nineteen legacy test case ids of RWB-E1-054 are kept in their legacy order (18, 19, then 01 to 17). Legacy levels map System to End to end, Access to Component and Resilience to NFR. A legacy test whose behaviour moved to rwb-document is re-pointed at the case-side criterion it now proves: the P5 refusal leaves the task open, and the P5 answer is recorded once.

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-054-18 | AC3, BR2 | Component | RW-REFADM without Case record R reads GET /me/tasks and completes a review task; 403 with MSG-P4-002, the task unchanged |
| TC-E1-054-19 | AC10, AC7, BR5 | NFR | Decision-record write forced to fail on completion, then the P5 answer timed out; the task open, no timeline entry, MSG-P7-003, incident raised |
| TC-E1-054-01 | AC9, AC1, BR4 | End to end | Review item IN-0101 classified COURT_NOTICE 0.6200 and DEMAND_LETTER 0.2100 with reason LOW_CONFIDENCE, listed with its candidates, confidence and age |
| TC-E1-054-02 | AC2, BR5, BR7 | End to end | Hearing date corrected on the P5 side for synthetic case RW-2026-000201; one timeline entry, one decision record, task DONE |
| TC-E1-054-03 | AC3, BR5 | End to end | Document DOC-0103 with one field in review; the completion of its task records one outcome and one decision record |
| TC-E1-054-04 | AC4, BR6 | End to end | The P5 answer refuses an empty correction with MSG-GEN-001; the task stays open and nothing is written |
| TC-E1-054-05 | AC5, BR6 | End to end | Type PAYSLIP refused by the P5 answer with MSG-P5-006; the task stays open |
| TC-E1-054-06 | AC6, BR6 | End to end | Date 2569-12-16 refused with MSG-GEN-002 naming Hearing date, 2000-01-01 and 2100-12-31; the task stays open |
| TC-E1-054-07 | AC7, BR6 | End to end | Two fields in review and one confirmed; the P5 answer refuses with MSG-GEN-001 and the task stays open |
| TC-E1-054-08 | AC8, BR6 | End to end | Reason CASE_CLOSED with candidate case RW-2026-000150 closed; the P5 answer refuses with MSG-P5-005 and the task stays open |
| TC-E1-054-09 | AC9, BR6 | End to end | Two sessions on one item at version 3 and 4; the second completion is 409 with MSG-GEN-004 and the task stays open |
| TC-E1-054-10 | AC10, BR5 | End to end | Demand letter changed to guarantor notice on the P5 side; one outcome and one decision record on the case |
| TC-E1-054-11 | AC11, BR5 | End to end | Same file hash on the chosen case; the P5 answer links the existing document, MSG-P5-024, one outcome recorded |
| TC-E1-054-12 | AC12, BR7 | End to end | Unreadable item discarded with reason "Blank page from the branch scanner"; the task closes with DISCARDED and the reason stays on the timeline |
| TC-E1-054-13 | AC13, BR6 | End to end | Discard with an empty reason refused by the P5 answer with MSG-GEN-001; the task stays open |
| TC-E1-054-14 | AC14, BR3, BR4 | End to end | Five review items across teams LIT-BKK and HP-NE received on 2, 3 and 4 November, one of them with no case; order and scope asserted |
| TC-E1-054-15 | AC15 | End to end | No review task for queue LIT-BKK-OFF; empty page and the empty state |
| TC-E1-054-16 | AC16, BR3 | Component | Review task of a case of team HP-NE read by the LIT-BKK officer; 404 with MSG-P4-003 |
| TC-E1-054-17 | AC17, BR6 | End to end | The same completion of TSK-0101 sent twice; 200 with the saved task, one timeline entry and one decision record |
| TC-E1-054-20 | BR2, BR8 | Component | Contract test of the operations, events and activities of section 12 against RWB-P5-E1054-CON; each operation returns the answer section 12 declares |
| TC-E1-054-21 | BR8 | Component | Boundary test of the tables of section 12.7: the story reads and writes only the tables it marks, and no P5 or P4 table is read |
| TC-E1-054-22 | BR1 | Component | Two review items for one document with status OPEN or IN_PROGRESS and a duplicate DocumentStored; one task reused, no second task created |
| TC-E1-054-23 | BR8 | Component | Task row after a completion holds the document ID, the reason, the item version and the review state; no intake or document field stored in rwb_case |
| TC-E1-054-24 | BR9 | Component | Review team, page size, review reasons, task codes and review states read from the rwb-case contracts; a changed parameter row changes the result with no code change |
| TC-E1-054-25 | BR10 | End to end | Queue measure rows publish the count and the age of the queue from rwb_case; no threshold is applied in this story |
| TC-E1-054-26 | AC18, BR1, BR8, BR9, BR10 | Component | Duplicate DocumentStored for DOC-0103 with task OPEN; one task reused; task row holds only document ID, reason, item version and review state; parameter change with no code change; queue measures with no threshold |
| TC-E1-054-27 | AC19 | Component | No valid token on GET /me/tasks and on PATCH of a task; 401 on each, nothing written |
| TC-E1-054-28 | AC20 | Component | Task TSK-0101 in DONE moved to OPEN by PATCH; refused with the code Not specified in the source documents (NEWAC-RWB-P3-E1054-APP-AC20); status and timeline unchanged |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v9.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the review team, the page size, the review reasons, the task codes, the review states and the decision code are data in the parameters and the reference tables of rwb-case, read through their contracts (DP-06, DP-07; BR-P3-006).
- No field value, no OCR text and no personal data in `rwb_case`, in events or in logs. The task holds the document ID, the reason code, the item version and the review state only; the timeline entry carries the outcome and the reason code; test data uses synthetic documents, cases and users only.
- The queue holds references only: the case, the document and the account are named by business key (`case_no`, document ID, `account_id`) with no foreign key across services (DP-01).
- No document table is read: the item, its reason, its candidates, its confidence and its outcome come through the P5 review contract (DP-01, DP-11), and the platform-owned document tables are never named in a statement.
- One hop and a 2 s timeout on every consumed call, with the `Idempotency-Key` on the review call, so a retry records the outcome once (DP-11; BR6).
- The scope answer comes from the rwb-access authorise contract and the queue's team code, never from a cached table or an assumed role list (DP-08).
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only (DP-09).
- Nothing is removed silently: a discarded item keeps its file in P5 and its reason on the case timeline (REQ-DCM-019).
- One evaluator of work, one writer of records: the task, the timeline entry and the decision record are rwb-case's, and rwb-case writes no document and no field.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue, worked by a person | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-01 to TC-E1-054-25 |
| REQ-DCM-019 | A discarded document is never removed silently; the reason and the person are kept with the file | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-12, TC-E1-054-13 |
| D-RCV-60 | Split of RWB-E1-054: rwb-document keeps the screen, the OCR text, the field corrections, the type change, the attach and the labeled set; rwb-case takes the review queue, the task, the scope rule, the timeline and the decision record | Decision log, D-RCV-60 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-01 to TC-E1-054-25 |

The feature identifiers are those of the legacy story; FEAT-DCM-11 covers the check of a low-confidence extraction, which the case side records as the outcome of the task.

### 19. Out of scope

- Setting the review reasons: OCR (legacy RWB-E1-049), classification (RWB-P3-E1050-APP and its rwb-document slice), extraction (legacy RWB-E1-053) and matching (RWB-P3-E1032-APP and its rwb-document slice).
- The review screen, the file, the OCR text, the field confirm and correct, the type change, the attach and the labeled set, all of them rwb-document's (P5).
- The labeled set and the model evaluations that read it (legacy RWB-E1-060).
- Assigning review work to named people by queue rules (legacy RWB-E2-011); this story uses the queue the case owns.
- The case checklist build on the review screen (legacy RWB-E1-040).
- The queues, the membership and the queue measures as reference data (RWB-P3-E1019-APP) and the queue measure snapshot story of RWB-E1-030.
- The deployment of this capability: Helm values, topic and queue provisioning, dashboards and the runbook (a separate OPS story of this legacy key).
