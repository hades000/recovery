# RWB-P3-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P3-E1032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-case |
| Service epic | RWB-SVC-P3 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P3-M |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1032-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md (no FR mapped to REQ-DCM-007, REQ-DRI-004, REQ-DCM-005) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-032 for rwb-case; the document hub keeps the intake, classification and store work in RWB-P5-E1032-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)** and the **rwb-case service**, I want **the case-directory answers the document matcher calls (a case by its case number, the open cases of an ACE account number) and, when rwb-document publishes that a document was stored, one case document link on the right case with its timeline entry, its decision record and one review task when the document is held for review**, so that **a classified document lands on the right case without a person and no document lands on a wrong case**.

### 2. Business rationale

Scans, partner files and emails arrive without a case link; today a person reads each one and files it. The legacy story matched each classified intake item to one open case by the case ID or the account number in its text and stored it on that case with no person involved (FSD P5 A2.12), and wrote the document attached record required from Epic 1 (REQ-DRI-004, RWB-E1-027). An item that matched no case, more than one case, a closed case or no agreed type was held for a person.

This story is one half of that legacy story. The intake (`POST /documents`), the OCR, the classification and extraction, the matching decision itself and the store stay in the document hub, rwb-document (P5), in RWB-P5-E1032-APP. rwb-case owns only what belongs to the case: the case identity that the matcher asks for, the case-side link to the stored document, the timeline record on the case, the review task when a document is held for review, and the decision record of that link (DP-03). rwb-case reads no document table and rwb-document reads no case table (DP-01); the only cross-service paths are one-hop REST with a 2 s timeout (DP-11) and the events `rwb.document.DocumentStored.v1` (EV-16) and `rwb.document.DocumentFieldsExtracted.v1` (EV-17) on the document hub's topic (DP-09).

The split keeps the case the system of record for its own documents list: SCR-30 Case documents and the case timeline read one owner, and a document stored for a case that rwb-case does not hold is never silently attached.

### 3. Preconditions

- RWB-P5-E1032-CON is published: the document metadata, intake-item and review-item resources, the `rwb.document.events.v1` schemas for DocumentStored (EV-16) and DocumentFieldsExtracted (EV-17) with the CloudEvents envelope, the error envelope, the Idempotency-Key rule and the contract fakes.
- Build dependencies: none. The story has no same-service story to wait for and no H dependency; it builds Day 1 against the published P5 contract and its fake.
- RWB-P3-E1042-CON is published: the parameters contract of rwb-case with the client library (DP-06). RWB-P3-E1043-CON is published: the reference-data contract of rwb-case (DP-07), holding LOV-CASE-STATUS, LOV-TASK-STATUS and the task codes.
- The platform libraries are consumed as published interfaces and are not build dependencies of this story: the outbox and inbox library (RWB-PLT-TE006-CON, DP-09), the Temporal workflow kit in namespace `rwb-recovery` (RWB-PLT-E1071-CON, DP-10), the per-service Flyway sequence (RWB-PLT-E1044-CON, DP-15) and the local decision-record library with the shared topic `rwb.decision-record.v1` (RWB-PLT-E1027-CON, DP-03).
- RWB-PLT-N001-CON is published: the gateway-bff composite route that serves SCR-30, SCR-03 and SCR-04 (DP-19).
- The rwb_case tables `recovery_case`, `case_account`, `task` and the case interaction projection exist before this story runs its own migration.
- The rwb-case login (DP-02) is Not specified in the source documents (GAP-0748; ASM-1369).

### 4. Flow

1. rwb-document (P5): the DocumentIntakeWorkflow classifies a stored intake item and the matcher needs the case. It calls the rwb-case case-directory answers, one hop with a 2 s timeout (DP-11).
2. rwb-case: `CaseLookupService` answers by case number on `GET /cases?caseNo=...` with the case id, the case number and the status, and the outcome MATCHED, or NO_MATCH when no case holds that number.
3. rwb-case: for an account number the matcher passes the ACE account number. `AccountKeyResolver` calls the rwb-source-data contract once for the `account_key` of that account number (DP-05), then reads `case_account` in schema `rwb_case` for the open cases on that key.
4. rwb-case: the answer carries the outcome MATCHED, NO_MATCH, MULTIPLE or CASE_CLOSED with the candidates as case id, case number and status. rwb-case never chooses among candidates and never resolves a doubt.
5. rwb-document (P5): the matcher stores the document on the case it chose and publishes DocumentStored (EV-16) to its outbox in the same transaction as its own rows (DP-09).
6. rwb-case: the case router consumes EV-16 from `rwb.document.events.v1` through its inbox (one action per event id) and calls `signalWithStart` on CaseWorkflow with the workflow ID equal to the case ID, on task queue `rwb-case`.
7. rwb-case: the `LinkDocument` activity writes one `case_document_link` row for the case and the document with the checklist state LINKED, and one timeline entry of type DOCUMENT in the case interaction projection.
8. rwb-case: when the event carries a `review_status` of PENDING, `ReviewTaskRaiser` raises exactly one case review task in the review queue, status OPEN, owned by the case role.
9. rwb-case: the `RecordAndApply` activity writes the decision record (DP-03) and the outbox row in the same transaction as the link and the timeline entry; a failed write rolls the link back, so no partial record exists.
10. rwb-document (P5): when the extracted fields are ready it publishes DocumentFieldsExtracted (EV-17). rwb-case updates the extracted field count on the same link; it never creates a second link.
11. rwb-case: the daily reconcile Schedule (DP-10) compares the documents that rwb-document holds for a case with the links in `rwb_case` and writes the links that a timeout left uncreated.
12. rwb-case: the review queue entry raised in step 8 is worked in RWB-P3-E1054-APP; the reviewer confirms or corrects the document type and the link moves to CONFIRMED or CORRECTED.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No case holds the case number, or no open case is on the account | The answer carries NO_MATCH and no candidate; rwb-case writes nothing; the matcher holds the item for a person | MSG-P5-003 | AC1, AC2 |
| X2 | The account number carries two or more open cases | The answer carries MULTIPLE with every candidate as case id, case number and status; rwb-case chooses neither and writes no link | MSG-P5-003 | AC3 |
| X3 | The only case on the account is closed | The answer carries CASE_CLOSED with that case and its status; rwb-case writes no link | MSG-P5-003 | AC4 |
| X4 | rwb-source-data does not answer inside the REST budget | One hop, 2 s timeout (DP-11); the answer is 503 and no candidate is invented; the caller holds the item and calls again | MSG-P1-001 | AC2 |
| X5 | The document metadata read times out, or the decision record write fails | Nothing is written: no link, no timeline entry and no decision record; the event is retried, so no partial record exists | MSG-P7-003 | AC5, TC-E1-032-17 |
| X6 | The same event id is delivered again, or two deliveries run at once | The inbox drops the duplicate and the unique key on the link keeps one row; nothing changes | None | AC6 |
| X7 | An event names a case that rwb-case does not hold | No link, no timeline entry and no decision record; the event is retried and then parked for the operations team | None | AC8 |
| X8 | The case is outside the reader's scope | The read is refused with 404 and MSG-P4-003; no document link shows | MSG-P4-003 | AC8 |
| X9 | A role without Case record R calls a case-directory answer | The call is refused with 403 and MSG-P4-002; no case and no document link are returned | MSG-P4-002 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds Day 1 against the RWB-P5-E1032-CON contract fake and the rwb-source-data fake; it has no same-service story to wait for |
| Negotiable | The switch, the review task code and the link field names are data or contract values; the outcomes and the one-link rule are fixed |
| Valuable | Puts every OCR-read document on the right case with no person, and gives every document held for review one task on the case |
| Estimable | One controller with three reads, two event handlers, one workflow with three activities, one Schedule and one migration |
| Small | Fits two weeks with its tests |
| Testable | Every criterion in section 7 has a test case in section 16; every cross-service answer is stubbed in a contract fake |

### 7. Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake (the rwb-case side)

  Background:
    Given case "RW-2026-000123" is open, owned by "U-CO-01" and linked to account key "A-5001"
    Given case "RW-2026-000456" is open and linked to account key "A-5002"
    Given case "RW-2026-000789" is closed and linked to account key "A-5009"
    Given the rwb-document contract mock returns document "DOC-0001" stored for case "RW-2026-000123" with review_status "NOT_NEEDED"

  Scenario: AC1 The case-number answer (new, D-RCV-60)
    Given the rwb-document contract mock returns the case number "RW-2026-000123" read from a classified notice
    When the matcher calls GET /cases?caseNo=RW-2026-000123
    Then the answer holds one case with its case id, case number "RW-2026-000123" and status and the outcome is MATCHED
    When the matcher calls GET /cases?caseNo=RW-2026-999999
    Then the answer holds no case and the outcome is NO_MATCH

  Scenario: AC2 The account-number answer through the source-data contract (new, D-RCV-60)
    Given the rwb-source-data contract mock returns account_key "A-5002" for the ACE account number "TEST-ACC-0002"
    When the matcher calls GET /cases?accountNo=TEST-ACC-0002
    Then rwb-case reads case_account for account_key "A-5002" and answers one open case "RW-2026-000456" with its case id, case number and status
    Then the outcome is MATCHED and the call to rwb-source-data is one hop with a 2 s timeout

  Scenario: AC3 Two open cases on one account (new, D-RCV-60)
    Given cases "RW-2026-000321" and "RW-2026-000654" are open and both linked to account key "A-5003"
    Given the rwb-source-data contract mock returns account_key "A-5003" for the ACE account number "TEST-ACC-0003"
    When the matcher calls GET /cases?accountNo=TEST-ACC-0003
    Then the answer holds both cases with case id, case number and status and the outcome is MULTIPLE
    Then rwb-case chooses neither case and writes no case document link

  Scenario: AC4 A closed case only (new, D-RCV-60)
    Given the rwb-source-data contract mock returns account_key "A-5009" for the ACE account number "TEST-ACC-0009"
    When the matcher calls GET /cases?accountNo=TEST-ACC-0009
    Then the answer holds case "RW-2026-000789" with its closed status and the outcome is CASE_CLOSED
    Then rwb-case writes no case document link

  Scenario: AC5 DocumentStored links the document once (new, D-RCV-60)
    Given the rwb-document contract mock raises rwb.document.DocumentStored.v1 (EV-16) with event id "EVT-0001", document "DOC-0001", case "RW-2026-000123" and review_status "NOT_NEEDED"
    When rwb-case consumes the event
    Then case_document_link holds one row for case "RW-2026-000123" and document "DOC-0001" with the checklist state "LINKED"
    Then the case timeline holds one entry of type DOCUMENT naming the case and the document
    Then one decision record names the case, the document and event id "EVT-0001"
    Then no case review task is raised

  Scenario: AC6 A repeated event and a later field extraction change no rows twice (new, D-RCV-60)
    Given the event "EVT-0001" from AC5 has been consumed
    When the same event id "EVT-0001" is delivered again
    Then no second link, timeline entry or decision record is written
    When rwb.document.DocumentFieldsExtracted.v1 (EV-17) arrives for document "DOC-0001" with extracted field count 5
    Then the one link holds extracted field count 5 and no second link exists
    When a further EV-17 arrives for document "DOC-0001" with extracted field count 5
    Then the link still holds one row and no second timeline entry or decision record is written

  Scenario: AC7 A document held for review raises one task (new, D-RCV-60)
    Given the rwb-document contract mock raises EV-16 with event id "EVT-0002", document "DOC-0002", case "RW-2026-000456" and review_status "PENDING"
    When rwb-case consumes the event
    Then exactly one case review task exists on case "RW-2026-000456" with status OPEN in the review queue
    When the same event id "EVT-0002" is delivered again
    Then still exactly one case review task exists on the case

  Scenario: AC8 A document for a case rwb-case does not hold (new, D-RCV-60)
    Given the rwb-document contract mock raises EV-16 with event id "EVT-0003", document "DOC-0003" and case "RW-2026-999999" that rwb-case does not hold
    When rwb-case consumes the event
    Then no case_document_link row, timeline entry or decision record is written
    Then the event is retried and then parked for the operations team
    Given the rwb-access contract mock returns Case record R with a scope that excludes case "RW-2026-000654"
    When a case owner calls GET /cases/{caseId} for "RW-2026-000654"
    Then the system refuses the read with status 404 and MSG-P4-003

  Scenario: AC9 A role without Case record R (new, D-RCV-60)
    Given user "U-5001" holds RW-REFADM, which has no Case record right
    Given the rwb-access contract mock returns no Case record right for role "RW-REFADM"
    When "U-5001" calls GET /cases?caseNo=RW-2026-000123
    Then the system refuses the call with status 403 and MSG-P4-002
    Then no case and no document link are returned
```

Every criterion above is new for the case side of the legacy story. The legacy criteria AC1 to AC15 stay with RWB-P5-E1032-APP, and the real cross-service behaviour is proved in RWB-ITG-E1032-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Exactly one open case on the case number or the account number is answered as one case with the outcome MATCHED; every other result carries NO_MATCH, MULTIPLE or CASE_CLOSED and is settled by a person in rwb-document | REQ-DCM-007; FEAT-DCM-12; legacy AC3, AC7 |
| BR2 | rwb-case never resolves a doubt: it returns every candidate and never picks one, and a closed case is never answered as an open one | REQ-DCM-005; legacy AC3, AC7 |
| BR3 | The case side links by business key only — `case_id` and the document reference from rwb-document — with no foreign key across services; no document table is read and no document row is copied into `rwb_case` | DP-01; ADR-010; D-RCV-35 U4 |
| BR4 | An event is processed once: the inbox records the event id, a duplicate changes nothing, and the unique key on the link keeps one row per case and document | DP-09; R-UNI-40 |
| BR5 | A document whose `review_status` is PENDING raises exactly one case review task; every other document raises none | Legacy AC10; REQ-DCM-005 |
| BR6 | The decision record is written with the link and the timeline entry in one transaction; a failed write leaves no link, no timeline entry and no decision record | Principle 5; R-UNI-39; REQ-DRI-004 |
| BR7 | The account number is resolved to `account_key` only through the rwb-source-data contract; the ACE account number is never stored in `rwb_case` and never logged | DP-05; CTL-09 |
| BR8 | The case-directory answers apply the caller's scope; a case outside it is invisible and answers 404, and a role without Case record R is refused with 403 | CTL-09; legacy AC13, AC14 |

### 9. State transitions

No case status changes in this story: a document attached to a case never moves the case.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| case document link | None | DocumentStored (EV-16) consumed for a case rwb-case holds | The link does not exist | LINKED |
| case document link | LINKED | A reviewer confirms or corrects the type | Worked in RWB-P3-E1054-APP | CONFIRMED or CORRECTED |
| case review task | None | DocumentStored (EV-16) with `review_status` PENDING | No review task exists for the document | OPEN |
| case review task | OPEN | The reviewer completes the review | Worked in RWB-P3-E1054-APP | DONE |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-case service identity (the rwb-case login, DP-02) | Answers the case-directory reads; consumes EV-16 and EV-17; writes the link, the timeline entry, the review task and the decision record; runs the reconcile Schedule |
| rwb-document service identity (the document hub) | Calls the case-directory answers; publishes EV-16 and EV-17; owns the document, the intake item and the checklist master |
| RW-CASEOWN | Reads the case-directory answers and the case document list in scope; works the review task raised on the case |
| RW-LITOFF | Reads the case-directory answers and the case document list in scope; works the review task on a litigation case |
| RW-TEAMMGR | Reads the case-directory answers and the case document list for the team in scope; opens no review task |
| Roles with Documents R only | See the documents of a case in their scope on SCR-30; attach nothing |
| RW-REFADM | Has no Case record right; refused on the case-directory answers |

The rwb-case and rwb-document login names are Not specified in the source documents (GAP-0748; ASM-1369); the story names them "the rwb-case login (DP-02)" and "the rwb-document service identity" until they are agreed.

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
| DF-INT-001 to DF-INT-029 | interaction (the case timeline projection in `rwb_case`) | one DOCUMENT entry per link | Write |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) | all fields | Write |
| case_document_link | rwb_case | case_id, document_id, checklist_state, extracted_field_count, linked_at, source_event_id | Write |

The `case_document_link` table is new in `rwb_case` and its field IDs are not in the Logical Data Model and Data Dictionary v8: Not specified in the source documents (GAP-0742; ASM-1363). The decision code and the final call written for the link are Not specified in the source documents (GAP-0747; ASM-1368).

Document metadata is read only through the rwb-document contract: document id, document type, `review_status`, the extracted field count and the file hash on `GET /documents/{documentId}`, and the documents of a case on `GET /cases/{caseId}/documents`. No document row, checklist master or file reference is copied into `rwb_case`. The account number is read only through the rwb-source-data contract and is not stored.

Field IDs are those in the Logical Data Model and Data Dictionary v8.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/case/v1`; owner rwb-case (P3).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/cases` | Cases in the caller's scope, with the exact `caseNo` filter and the `accountNo` filter that resolves through rwb-source-data and answers the case-directory outcomes | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}` | Read one case with its case number and status | Case record R, scope applied | Not applicable |
| GET | `/cases/{caseId}/accounts` | Read the linked accounts with `accountKey` and the primary flag | Case record R, scope applied | Not applicable |

The answer of `GET /cases` carries the outcome MATCHED, NO_MATCH, MULTIPLE or CASE_CLOSED, and for each candidate the case `id`, `caseNo` and `status`. Errors: 401 no session, 403 no Case record R (MSG-P4-002), 404 not found or out of scope (MSG-P4-003), 503 rwb-source-data unavailable (MSG-P1-001).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | rwb-document (P5) | Documents the hub holds for a case; the reconcile run and SCR-30 | One hop, 2 s (DP-11) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | rwb-document (P5) | Document type, `review_status` and extracted field count | One hop, 2 s (DP-11) |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | rwb-source-data (P1) | `account_key` for the ACE account number the matcher passes (DP-05) | One hop, 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | rwb-access (P4) | Role, right and scope check behind the case-directory reads (AC8, AC9) | One hop, 2 s (DP-11) |

The query form of the rwb-source-data account lookup (the filter that carries the ACE account number) is Not specified in the source documents (GAP-0743; ASM-1364).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 | caseId | decision code, final call "DOCUMENT_LINKED", case id, document id, event id, record reference |

No `rwb.case.*` event is published by this story: the link changes no case status, stage, queue or owner (section 9), so CaseStateChanged (EV-05) has no state change to carry here.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 | Case router, inbox dedupe, `signalWithStart` of CaseWorkflow; LinkDocument, ReviewTaskRaiser and RecordAndApply |
| `rwb.document.DocumentFieldsExtracted.v1` (EV-17) | `rwb.document.events.v1` | P5 | CaseDocumentLinkService, inbox dedupe, updates the extracted field count on the same link |

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| CaseWorkflow | Workflow (parent, one per case, workflow ID = case ID) | `rwb-case` | Receives the document signal through the case router and carries the link from entry to closure |
| LinkDocument | Activity | `rwb-case` | Writes the link, the timeline entry and the review task of the case side |
| RecordAndApply | Activity (workflow kit) | `rwb-case` | Writes the decision record, the link and the outbox rows in one transaction |
| EvaluateRules | Activity (workflow kit) | `rwb-case` | The shared four-step activity of the workflow model; this story adds no rule package of its own |

#### 12.6 Schedules

| Schedule | Cadence | Trigger | Legacy reference |
|---|---|---|---|
| Reconcile case document links | Daily; the time of day is Not specified in the source documents (GAP-0744; ASM-1365) | Temporal Schedule in namespace `rwb-recovery`, overlap policy SKIP and a catch-up window (DP-10) | RWB-E1-032 restart behaviour: "an attach that failed stays PENDING for the next run" |

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| recovery_case | P3 (rwb_case) | Case id, case number and status, read only in this story |
| case_account | P3 (rwb_case) | Account link by `account_key`; the account-number answer |
| task | P3 (rwb_case) | The case review task raised for a document held for review |
| interaction | P3 (rwb_case) projection | The case timeline entry of type DOCUMENT; the ledger itself stays with rwb-source-data (P1) |
| case_document_link | P3 (rwb_case), new | One row per case and document with the checklist state and the extracted field count |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_case | Outbox, inbox and idempotency objects (DP-09) |

rwb-case reads no document table and holds no foreign key across services (DP-01); the document tables `document`, `document_checklist_item` and `document_intake` stay with rwb-document (P5).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The P5 contract | `GET /cases/{caseId}/documents`, `GET /documents/{documentId}`, and the EV-16 and EV-17 event fixtures |
| rwb-source-data WireMock | The P1 contract | `GET /accounts/{id}` answering `account_key` for the ACE account number |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Case record R and its scope, and refusing it for RW-REFADM |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 3 provided, 4 consumed | Case-directory reads provided; document, source-data and access consumed; one hop, 2 s timeout |
| Kafka | 1 published, 2 consumed | `rwb.decision-record.v1` published; `rwb.document.events.v1` consumed |
| Temporal | 1 workflow, 3 activities, 1 Schedule | CaseWorkflow; LinkDocument, RecordAndApply, EvaluateRules; the daily reconcile Schedule |
| File | None | This story reads and writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.case`, module `casedocument`, Java package `th.co.scb.ace.workbench.recovery.case.casedocument`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The pattern rows above are the patterns of the legacy key; the build dependencies of this story are the contract dependencies in the metadata table (none in-lane, `RWB-P5-E1032-CON` cross-service).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CaseDirectoryController | Controller | `GET /cases` with the `caseNo` and `accountNo` filters, `GET /cases/{caseId}` and `GET /cases/{caseId}/accounts`; the access check and scope |
| CaseLookupService | Service | Answers by case number and builds the MATCHED, NO_MATCH, MULTIPLE and CASE_CLOSED answers with the candidates |
| AccountKeyResolver | Client | Resolves the ACE account number to `account_key` through the rwb-source-data contract, one hop with a 2 s timeout |
| DocumentEventHandler | Handler | Consumes EV-16 and EV-17 through the inbox and starts the workflow; no duplicate action per event id |
| CaseDocumentLinkService | Service | Writes and updates the link, the checklist state and the extracted field count; applies the review rule |
| ReviewTaskRaiser | Service | Raises exactly one case review task when `review_status` is PENDING |
| DecisionRecordClient | Client | Writes the decision record through the local decision-record library and its outbox row (DP-03) |
| CaseDocumentLinkRepository | Repository | `case_document_link`, `task` and the interaction projection in schema `rwb_case` only |

**Database and migrations**

- `V1032_1__case_document_link.sql` creates `case_document_link` in schema `rwb_case` with `case_id`, `document_id`, `checklist_state`, `extracted_field_count`, `linked_at` and `source_event_id`, and the unique index `ux_case_document_link ON case_document_link (case_id, document_id)`.
- `V1032_1` also adds the partial index `ix_case_document_link_held ON case_document_link (linked_at) WHERE checklist_state = 'LINKED'` for the reconcile run.
- No P5 table is created or altered and no document column is added: the document tables stay with rwb-document (DP-01).
- The link table has no source table in the legacy schema and no field IDs in the Logical Data Model and Data Dictionary v8: Not specified in the source documents (GAP-0742; ASM-1363).

**Configuration and reference data**

- Switch: a parameter read through the parameters contract (DP-06), key Not specified in the source documents (GAP-0745; ASM-1366). Off means no link, timeline entry, review task or decision record is written from an event and the document stays unlinked in rwb-document. The legacy flag `rwb.dochub.autoattach` is the document hub's and stays in RWB-P5-E1032-APP.
- LOV-CASE-STATUS and LOV-TASK-STATUS through the reference-data contract (DP-07); the case review task code and its values are Not specified in the source documents (GAP-0746; ASM-1367).
- Decision code and final call of the link decision: Not specified in the source documents (GAP-0747; ASM-1368).

**Build steps**

1. Write `V1032_1`; test the link columns, the unique index and the held-link index.
2. Build CaseDirectoryController with the access check, the scope filter and the `caseNo` filter; test AC1, AC8 and AC9.
3. Build AccountKeyResolver over the rwb-source-data contract and the `accountNo` answer with the four outcomes; test AC2, AC3 and AC4, including the 2 s timeout.
4. Build DocumentEventHandler with the inbox and the `signalWithStart` of CaseWorkflow; test AC5 and AC6.
5. Build LinkDocument and CaseDocumentLinkService with the link, the timeline entry and the EV-17 refresh; test AC5 and AC6.
6. Build ReviewTaskRaiser with the one-task rule; test AC7.
7. Build RecordAndApply with the decision record and the outbox row in the same transaction; test the failure path of TC-E1-032-17.
8. Build the reconcile Schedule against the rwb-document contract; test the missing-link case and the timeout case.
9. Run every cross-service answer against the contract fakes, so the story builds before rwb-document exists.

**Feature switch.** The rwb-case switch is the parameter above, read through the parameters contract; off means the case side writes nothing from an event. The legacy `rwb.dochub.autoattach` stays with RWB-P5-E1032-APP.

**Done when.** The tests in section 16 pass; on the SIT data set every EV-16 for a case rwb-case holds has exactly one link, one timeline entry and one decision record, no document reference on a `rwb_case` row is unresolved by the P5 contract, and the contract tests of RWB-P5-E1032-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | A document is held for a person or stored for review | Some fields need checking. The document is in the review queue. |
| MSG-P4-002 | A role without Case record R calls a case-directory answer | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The case is outside the reader's scope | This case is not in your scope. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-004 | Two deliveries change the same record at once | Someone else changed this record. Reload it to see their change. |
| MSG-P1-001 | The account data of the business date is not available | {product} is from {date}. Today's ACE batch has not arrived. |

Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-30 Case documents | loading | Skeleton rows while rwb-case and rwb-document answer through the composite route |
| SCR-30 Case documents | list | The documents linked to the case with type, received date and checklist state; a document held for review shows MSG-P5-003 |
| SCR-03 Case record | read only | The case and its linked accounts; the document tab opens SCR-30 |
| SCR-04 Case timeline | list | The DOCUMENT entry of each link, newest first, with the actor and the time |

All three screens are served by the gateway-bff composite route (DP-19), which calls rwb-case and rwb-document in parallel and merges the answers. The review queue itself (SCR-31) is built in RWB-P3-E1054-APP.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-032-17 | AC5, BR6 | NFR | Decision record write forced to fail during the link; nothing written, MSG-P7-003 |
| TC-E1-032-16 | AC9, BR8 | Component | RW-REFADM calls `GET /cases`; refused with MSG-P4-002 |
| TC-E1-032-01 | AC1, AC5, BR1 | End to end | Case RW-2026-000123 open on account key A-5001; document DOC-0001 |
| TC-E1-032-02 | AC1, BR1 | End to end | Case number RW-2026-999999 with no case |
| TC-E1-032-03 | AC3, BR2 | End to end | Account TEST-ACC-0003 with two open cases |
| TC-E1-032-04 | AC2, BR1 | End to end | Account number TEST-ACC-0002 only |
| TC-E1-032-05 | AC1, AC2, BR2 | End to end | A case number and an account number that point to different cases; two answers, no choice by rwb-case |
| TC-E1-032-06 | AC1, BR1 | End to end | Case number RW-2026-999999 read from a scan |
| TC-E1-032-07 | AC4, BR2 | End to end | Closed case RW-2026-000789 on account key A-5009 |
| TC-E1-032-08 | AC5, BR4 | End to end | The same file stored twice on case RW-2026-000123; one link |
| TC-E1-032-09 | AC6, BR4 | End to end | 15 duplicate EV-16 deliveries |
| TC-E1-032-10 | AC7, BR5 | End to end | Document DOC-0002 with review_status PENDING |
| TC-E1-032-11 | AC5, BR5 | End to end | An item with no agreed type; rwb-document raises no EV-16 and no link is written |
| TC-E1-032-12 | AC3, BR2 | End to end | A reviewer resolves a MULTIPLE answer in rwb-document; both candidates were returned |
| TC-E1-032-13 | AC8, BR8 | End to end | A scope that excludes case RW-2026-000654; 404 with MSG-P4-003 |
| TC-E1-032-14 | AC5, BR6 | End to end | A type not in force refused by rwb-document; no EV-16 and no link |
| TC-E1-032-15 | AC6, BR4 | End to end | Two parallel deliveries of the same document; one link |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Legacy levels map System to End to end, Access to Component and Resilience and Principle 5 to NFR.

### 17. Guardrails

- No business value in code: the switch is a parameter, the statuses and task codes are reference data, and no case number format, document type or threshold is written in Java.
- No PII in events, workflow inputs, workflow history or logs. The link carries the case id, the document id and the event id only; the account number is resolved through the rwb-source-data contract and is never stored or logged; test data uses synthetic keys only.
- No document table read and no case table read by the document hub: the case side reaches documents only through the rwb-document contract and its events, and rwb-document reaches the case only through the case-directory answers (DP-01). The `rwb_case` schema holds no foreign key into another schema.
- One link per case and document, enforced by the unique index and the inbox; a duplicate event never writes a second link, timeline entry, review task or decision record.
- The decision record and the link commit together or not at all (R-UNI-39, Principle 5).
- Every cross-service call is one hop with a 2 s timeout; a timeout leaves the link uncreated for the reconcile run, never a partial record.
- Every outbound event is written to the outbox in the same transaction as the state change and carries IDs and facts only (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-032-01 to TC-E1-032-17 |
| REQ-DRI-004 | The document attached record is written for every attach | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39 | TC-E1-032-01, TC-E1-032-17 |
| REQ-DCM-005 | No match, more than one candidate, a closed case or no agreed type goes to a person | Business Requirements Epic 1, section 3.5; Business Requirements Program, section 5.5 | FEAT-DCM-08 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-032-03, TC-E1-032-07, TC-E1-032-10, TC-E1-032-12 |
| D-RCV-60 | The legacy story is split between rwb-document (intake, classification, matching, store) and rwb-case (case identity, link, timeline, review task, decision record) | Decision log, D-RCV-60 | FEAT-DCM-12, FEAT-DCM-08 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-032-01 to TC-E1-032-17 |

### 19. Out of scope

- The intake, the OCR, the classification, the extraction, the matching decision and the store: RWB-P5-E1032-APP, against RWB-P5-E1032-CON.
- The P5 resources and event schemas themselves: the document metadata, intake-item and review-item resources and the EV-16 and EV-17 schemas are RWB-P5-E1032-CON.
- The document hub infrastructure and deployment: RWB-P5-E1032-INF and RWB-P5-E1032-OPS.
- The review queue screen and the confirm-or-correct action on a document held for review: RWB-P3-E1054-APP. A held document's type is never confirmed here.
- The case document checklist master and its item state as held by rwb-document (`GET /cases/{caseId}/document-checklist`); this story holds only the case-side link and its checklist state.
- The notice that names an attached document: RWB-P6-E1032-APP. The decision record on the central ledger: RWB-P7-E1032-APP. The partner-side attach: RWB-S9-E1032-APP.
- The real cross-service behaviour of the attach, with the document hub, rwb-source-data and rwb-access live: RWB-ITG-E1032-ITG.
- The gateway-bff composite route specification of SCR-30: RWB-PLT-N001-CON.
