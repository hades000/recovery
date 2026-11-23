# RWB-P5-E1040-APP Document checklist per case type as reference data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1040-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-040 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-012) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: moved RWB-E1-040 into `rwb-document` unchanged in behaviour; the checklist rows and the completeness flag now sit in `rwb_document`, the case stage and route are read through the rwb-case contract instead of an in-process call, the load goes through the rwb-case reference-data contract, and the refresh step of JOB-12 becomes a Temporal activity on queue `rwb-document`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the required documents per case type and route held as a versioned reference table that the case documents screen, the case list and the review queue read**, so that **a missing document shows on the case without a person checking a list**.

Inside `rwb-document` this is the checklist capability of the document hub:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1` (DP-13), topic `rwb.document.events.v1` with event names `rwb.document.<Event>.v1` (DP-09), Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The story owns two tables in its own schema, `document_checklist_item` and `case_document_check` (DP-01, DP-15), and reads `document` and `document_type` of the same schema. It reads nothing of another service: the stage, the route and the owner of a case arrive from `rwb-case` over one REST hop with a mock (DP-11).
- The checklist table version, its rows and their valid-from dates come through the reference-data contract of rwb-case (DP-07, C RWB-P3-E1043-CON); the load is submitted and approved through that contract, so the reference data has one owner and one change process.
- The recompute is event driven: `rwb.document.DocumentStored.v1` from the store of RWB-P5-E1024-APP and `rwb.case.CaseStateChanged.v1` from `rwb-case`, both through the outbox and inbox library (DP-09). The refresh of a version that has just taken effect is one activity of the JOB-12 document-intake Schedule on queue `rwb-document` (DP-10).
- The screens are published by gateway-bff through the composite route (DP-19): the checklist panel of SCR-30 is RWB-P5-E1026-APP's tab, this story fills its required items, and the missing count of SCR-02 is read by `rwb-case` through this service.

The legacy behaviour is unchanged: the same rules, messages, required types, acceptance criteria and test cases with their values, the same authority letters and the same fields.

### 2. Business rationale

Litigation packs and guarantee claims fail when a required document is missing, and today the gap is found by a person reading a paper list, often at filing (CTL-19, R-LIT-17). This story holds the checklist per case stage and route as data and keeps a completeness flag per case, recomputed whenever a document is stored or the case changes stage. It meets REQ-DCM-011 and gives the pack checks of Epics 4 and 5 (R-LIT-16, R-GUA-07) one checklist source. The measure is fields extracted without review (FSD P5 A2.16.1).

In the target the same intent needs three decoupling moves and no new behaviour: the two tables become `rwb_document` tables (DP-01), the case facts become the rwb-case contract with a mock and a 2 s budget (DP-11), and the flag becomes an operation the case list reads one hop away (DP-07, DP-19). A change to the items is still a data change with a valid-from date and no deployment (BR3).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-PLT-E1043-CON | The reference-data client library, so the checklist version, its rows and their dates arrive as versioned data and never as code (DP-07) |
| RWB-PLT-TE006-CON | The outbox and inbox library and the CloudEvents envelope for the two consumed events (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit and Schedules, so the refresh step of JOB-12 runs as a Temporal activity on queue `rwb-document` (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence, so the migration that creates the two tables belongs to `rwb_document` (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the Documents tab and the case list (DP-19) |
| RWB-P5-E1024-APP | The document store and `rwb.document.DocumentStored.v1`, so documents are stored and the event exists to listen to |
| RWB-P5-E1025-APP | Document type table version "DOCTYPE-2026.11" in force with the six agreed types |
| RWB-P5-E1026-APP | The `GET /cases/{caseId}/document-checklist` placeholder and the SCR-30 panel this story fills |
| RWB-P3-E1043-CON | The reference-data contract of rwb-case; a contract dependency, so it never blocks the build |

Business preconditions carried from RWB-E1-040:

- Checklist version "CHK-2026.11" loaded and approved with valid from 30 November 2026, assumed until the bank list is signed (DL19): stage LITIGATION requires DEMAND_LETTER, COURT_NOTICE, TITLE_DEED and APPRAISAL_REPORT; stage DEED_IN_LIEU requires TITLE_DEED, APPRAISAL_REPORT and SETTLEMENT_AGREEMENT.
- The rwb-case contract returns stage_code, route_code and owner of a case, and `rwb.case.CaseStateChanged.v1` (EV-05) is published by `rwb-case`. The operation ID and the field names of that read are Not specified in the source documents (GAP-2337; ASM-3889).
- The reference-load and approval operations of table "DOCUMENT_CHECKLIST" are Not specified in the source documents (GAP-2337; ASM-3889); the load is submitted and approved through the rwb-case reference-data contract (DP-07 default ruling).
- Feature flag `rwb.document.checklist` is on, the service-scoped name of the legacy flag `rwb.dochub.checklist`. Off: the endpoint returns the RWB-P5-E1026-APP placeholder and no flag is written.

### 4. Flow

1. Reference data administrator: loads the checklist file through the rwb-case reference-data contract, table "DOCUMENT_CHECKLIST", with its valid-from date; the approver with Reference data A approves it, and the load is handed to this service for validation.
2. ChecklistLoader: validates every row: stage in LOV-STAGE, route in LOV-ROUTE or empty, document type in the type table in force, no duplicate row; it refuses the load whole on any error and answers the row error to the contract.
3. ChecklistEvaluator: on `rwb.document.DocumentStored.v1` (EV-16), on `rwb.case.CaseStateChanged.v1` (EV-05) and when a checklist version takes effect, takes the stage and the route of the case through the rwb-case contract, one hop, 2 s timeout, circuit breaker and one GET retry with jitter.
4. ChecklistEvaluator: picks the rows of the version in force for that stage, using the rows of the route where they exist and the rows with no route otherwise.
5. ChecklistEvaluator: counts the active documents of each required type on the case and writes `case_document_check`: checklist version, required count, present count, missing types and complete.
6. Litigation officer: opens the Documents tab (SCR-30) through gateway-bff; `GET /api/recovery/document/v1/cases/{caseId}/document-checklist` returns each required item marked present or missing.
7. Case owner: sees the number of missing documents for each case on the case list (SCR-02); `rwb-case` reads it from this service, at most 500 case IDs per call.
8. ChecklistRefreshActivity: on the JOB-12 document-intake Schedule (every 15 minutes) finds checklist versions whose valid-from date has been reached since the last run and recomputes the cases of the stages they change.

The evaluation is read-only for the case: it writes `case_document_check` and never moves a case. A failure between step 3 and step 5 leaves the previous flag in place and the event is retried (section 5, X3 and X6).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The case stage has no checklist rows | The checklist shows "No checklist for this case type"; complete is empty | None | AC6 |
| X2 | A checklist load names a document type not in the type table, or a stage not in LOV-STAGE | Load refused in full; the version in force is unchanged | MSG-P3-027 | AC7 |
| X3 | The same `DocumentStored` event arrives twice | One recompute result; the second is ignored and counted as a repeat in the inbox | None | AC8 |
| X4 | A document type is present only as an inactive earlier version | Counted once, through its active version | None | AC9 |
| X5 | A role without Documents R opens the checklist | Refused with 403 | MSG-P4-002 | TC-E1-040-10 (Access) |
| X6 | The rwb-case contract does not answer inside the 2 s budget, or answers with an error | No flag is written; the event is retried; after the retry limit it goes to `rwb.document.events.v1.dlt` with the platform administrator as owner | None | Section 13, build step 4 |
| X7 | The case is outside the user's scope | Refused with 403; no item list is returned | MSG-P4-003 | TC-E1-040-10 (Access) |

X6 is the only new path: it replaces the in-process call of the legacy story with a contract call, and it changes nothing in the case.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store, the type table and the placeholder endpoint (RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP) and the five platform contracts, all earlier in the wave or Day 1 |
| Negotiable | The items per stage and route are data under DL19; the story fixes only how they are applied |
| Valuable | Missing documents show on the case and on the case list before a pack is built |
| Estimable | Two tables, one loader, one evaluator, two listeners, one activity, one operation and two screen parts |
| Small | Fits within one week with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Document checklist per case type as reference data

  Background:
    Given checklist version "CHK-2026.11" is in force
    Given stage "LITIGATION" requires DEMAND_LETTER, COURT_NOTICE, TITLE_DEED and APPRAISAL_REPORT
    Given stage "DEED_IN_LIEU" requires TITLE_DEED, APPRAISAL_REPORT and SETTLEMENT_AGREEMENT
    Given the rwb-case contract mock returns the stage, the route and the owner of the case under test

  Scenario: AC1 Checklist by type (legacy RWB-E1-040 AC1)
    Given case "RW-2026-000123" at stage "LITIGATION" holds a demand letter and a court notice
    When the litigation officer opens the Documents tab
    Then the checklist shows the 4 items from version "CHK-2026.11" for "LITIGATION"
    Then DEMAND_LETTER and COURT_NOTICE are marked present
    Then TITLE_DEED and APPRAISAL_REPORT are marked missing

  Scenario: AC2 Change as data (legacy RWB-E1-040 AC2)
    Given version "CHK-2026.12" adds GUARANTOR_NOTICE for "DEED_IN_LIEU" and is approved with valid from 1 December 2026
    Given the rwb-case reference-data contract mock returns version "CHK-2026.12" in force from 1 December 2026
    When case "RW-2026-000456" at stage "DEED_IN_LIEU" is opened on 1 December 2026
    Then the checklist shows 4 items including GUARANTOR_NOTICE
    Then no code was deployed between 30 November and 1 December 2026

  Scenario: AC3 Completeness flag (legacy RWB-E1-040 AC3)
    Given case "RW-2026-000456" at stage "DEED_IN_LIEU" holds a title deed and an appraisal report
    Given the rwb-case contract mock returns the case list read for the case owner's cases
    When the pack check runs after the appraisal report is stored
    Then case_document_check for the case has complete false, missing count 1 and missing type SETTLEMENT_AGREEMENT
    Then the case owner sees "1 missing" for the case on the case list

  Scenario: AC4 The missing document arrives (legacy RWB-E1-040 AC4)
    Given the case from AC3 with SETTLEMENT_AGREEMENT missing
    When a settlement agreement is stored on the case
    Then case_document_check has complete true and missing count 0
    Then the case list shows no missing documents for the case

  Scenario: AC5 Stage change (legacy RWB-E1-040 AC5)
    Given case "RW-2026-000789" at stage "DEED_IN_LIEU" with complete true
    Given the rwb-case contract mock returns CaseStateChanged moving the case to stage "LITIGATION"
    When CaseStateChanged moves it to stage "LITIGATION"
    Then the pack check uses the "LITIGATION" rows
    Then case_document_check has complete false with the missing litigation types

  Scenario: AC6 No checklist for the stage (legacy RWB-E1-040 AC6)
    Given case "RW-2026-000321" at stage "DEBT_SALE" and no rows for "DEBT_SALE"
    When the Documents tab opens
    Then the checklist shows "No checklist for this case type"
    Then case_document_check has complete empty and missing count 0

  Scenario: AC7 Load with an unknown type (legacy RWB-E1-040 AC7)
    Given a load file for table "DOCUMENT_CHECKLIST" with a row for stage "LITIGATION" and type "POWER_OF_ATTORNEY"
    Given the rwb-case reference-data contract mock returns the "DOCUMENT_CHECKLIST" load for validation
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P3-027 naming the row and "document type not in the type table"
    Then version "CHK-2026.11" stays in force

  Scenario: AC8 The same event twice (legacy RWB-E1-040 AC8)
    Given DocumentStored for one document on case "RW-2026-000123" is delivered twice with the same event ID
    When the evaluator handles both
    Then the system writes case_document_check once for that event
    Then the system counts the second delivery as a repeat

  Scenario: AC9 Earlier version of a document (legacy RWB-E1-040 AC9)
    Given case "RW-2026-000123" holds an appraisal report at version 2 with version 1 inactive
    When the pack check runs
    Then APPRAISAL_REPORT counts as present once
```

The four extra Givens mock the rwb-case contract, the CaseStateChanged message and the rwb-case reference-data load; every value of the legacy criteria is kept unchanged, and no business value is added.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The checklist per case type is held as reference data so a missing document is visible | REQ-DCM-011; FEAT-DCM-16 |
| BR2 | The case type is the case stage, with route rows taking precedence over rows with no route | LOV-STAGE; LOV-ROUTE; checklist table (New) |
| BR3 | A checklist version takes effect on its valid from date, without a deployment | refdata.txt change process; R-UNI-38; DT02 |
| BR4 | Only active documents count, once per type | FEAT-DCM-20 |
| BR5 | The completeness flag is recomputed on every document stored and every stage change | EV-16; EV-05 |
| BR6 | A repeated event changes nothing | R-UNI-40 |
| BR7 | The checklist is the source the pack checks read in later epics | R-LIT-16, R-LIT-17, R-GUA-07, R-GUA-08 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 and BR3 are held by DP-07: the rows carry `table_version`, `valid_from` and `valid_to`, the service reads the version in force with the business date, and a new version is a new load, never a code change.
- BR2 is executed by the query on `document_checklist_item`: rows of the route where they exist, rows with no route otherwise, ordered by `sort_order`.
- BR4 counts `document` rows of the case with `is_active` true and the required type, once per type.
- BR5 and BR6 are held by the inbox: both listeners run inside the inbox transaction, `processed_event` holds the event ID, and a repeat returns without a write.
- BR7 is held by the operation, which the pack checks of Epics 4 and 5 and the case list of `rwb-case` read; DP-01 keeps every read and write in `rwb_document`.

### 9. State transitions

None for the case. This story does not change a case status. It writes the completeness flag of the case in `case_document_check`: complete false while a required type is missing, true when every required type is present, empty when the stage has no checklist. The record is upserted once per case, with `checked_at` and the ID of the event that caused it in `last_event_id`.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-REFADM, reference data administrator | Loads the checklist (Reference data C) |
| Approver with Reference data A | Approves the load; no role holds Reference data A in the permission matrix today, assumed granted to the legal counsel as co-owner of the checklist (DL01; GAP-2338; ASM-3890) |
| RW-LITOFF, RW-CASEOWN and roles with Documents R | Read the checklist and the flag for cases in their scope |
| RW-LEGAL, legal counsel | Agrees the items per stage (DL19) |
| SY-CASEWF | Publishes CaseStateChanged that triggers the recompute |

The authorisation decision is taken by `rwb-access` (Recovery roles as data, scope and masking in `rwb_access`) and consumed as the cached permission decision the service holds; the refusal shapes stay 403 with MSG-P4-002 and MSG-P4-003. The guard itself is inherited from the service template (DP-08) and this story adds no guard. The loader acts for `rwb-case` on the reference-data contract and takes its identity from the per-service login (DP-02).

### 11. Data

| BR Field ID | Table in rwb_document | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` (read only through the rwb-case contract) | id | Read, through the contract |
| DF-CAS-006 | `recovery_case` (read only through the rwb-case contract) | stage_code | Read, through the contract |
| DF-CAS-008 | `recovery_case` (read only through the rwb-case contract) | route_code | Read, through the contract |
| DF-CAS-009 | `recovery_case` (read only through the rwb-case contract) | owner_user_id | Read, through the contract |
| DF-DOC-002 | `document` | case_id | Read |
| DF-DOC-004 | `document` | document_type | Read |
| Standard column | `document` | is_active | Read |
| DF-REF-234 to DF-REF-243 | `document_checklist_item` | all fields | Write (this story creates the record) |
| DF-DOC-036 to DF-DOC-044 | `case_document_check` | all fields | Write (this story creates the record) |
| DF-REF-219 | `document_type` | doc_type_code | Read |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |

Field IDs are those in the Logical Data Model and Data Dictionary. No table of another service is read (DP-01): the stage, the route and the owner are fields of the rwb-case contract response and are never joined from `rwb_case`. The flag holds type codes and counts only, so no personal data enters the table, the event or the log.

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/document/v1`, owned by P5, path and authorization taken from TSD P5 T-A.2 (API-P5-008).

**GET /api/recovery/document/v1/cases/{caseId}/document-checklist** (API-P5-008)

| Item | Value |
|---|---|
| Request | Path caseId; the placeholder of RWB-P5-E1026-APP is extended with the repeatable query `caseId` for the batch count of up to 500 cases |
| Response | 200 DocumentChecklist: caseId, checklistVersion, stageCode, items [documentType, label, required, presentCount], missingCount, complete; for a batch call, one entry per case ID |
| Errors | 401; 403 no Documents R (MSG-P4-002) or out of scope (MSG-P4-003); 404; 422 more than 500 IDs; 503 |
| Authorization | Documents, right R, scope applied |
| Idempotency | Not applicable |
| Field names | The response field names above are the legacy item names; the published names are Not specified in the source documents (GAP-2337; ASM-3889) |

The batch form exists because the legacy published interface `DocumentChecklistService.missingCounts(Collection<UUID>)`, at most 500 IDs per call, is an in-process call that the rwb-case case list now has to make over REST; no operation for it appears in the TSD P5 inventory. Its operation ID and query name are Not specified in the source documents (GAP-2337; ASM-3889).

#### 12.2 REST operations consumed

| Operation | Owner | Note |
|---|---|---|
| GET `/api/recovery/case/v1/cases/{caseId}` | P3 | The CaseDirectory read: stage_code, route_code and owner_user_id; one hop, 2 s timeout, breaker, one GET retry with jitter. Its operation ID is Not specified in the source documents (GAP-2337; ASM-3889) |
| The reference-load and approval of table "DOCUMENT_CHECKLIST" | P3 behind the reference-data client of DP-07 | The file, its valid-from date, the approval and the version register; this service validates the rows and answers the row error. Path and operation ID are Not specified in the source documents (GAP-2337; ASM-3889) |
| The reference-data read of DP-07 | P3 behind the client library | The checklist version in force for the business date and its rows; cached, read through RWB-PLT-E1043-CON and RWB-P3-E1043-CON |

#### 12.3 Events published

None. This story publishes no event: it writes `case_document_check` inside the inbox transaction of the event that caused the recompute, and the case list reads the count through the operation of 12.1.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | The store of RWB-P5-E1024-APP | Recompute the checklist of the case |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | rwb-case | Recompute with the new stage and route |

Idempotency key is the CloudEvents event ID: a repeat is ignored and counted (BR6, R-UNI-40). A failed handling retries on the topic policy (1 min, 10 min, 1 h) and then goes to `rwb.document.events.v1.dlt` with the platform administrator as owner. No personal data travels in either payload: case ID, document ID, document type and stage code only.

#### 12.5 Workflows and activities

| Item | Name | Queue | Responsibility |
|---|---|---|---|
| Activity | `checklistRefresh` | `rwb-document` | Finds the checklist versions whose valid-from date has been reached since the last run and recomputes the cases of the stages they change |
| Workflow | `DocumentIntakeWorkflow` (owned by RWB-P5-E1026-APP's intake story, RWB-P5-E1049-APP) | `rwb-document` | Hosts the activity as the refresh step of JOB-12; this story adds no workflow |

#### 12.6 Schedules

The JOB-12 document-intake Schedule every 15 minutes (FSD P5 AC-BG-P5-016-01) runs `checklistRefresh` as one of its steps; the Schedule replaces Quartz (DP-10) and this story adds no Schedule of its own. The Schedule ID and the retention of its history are Not specified in the source documents (GAP-2337; ASM-3889).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_checklist_item` | P5 (`rwb_document`) | Write: the validated rows of a checklist version, their stage, route, type, order and dates |
| `case_document_check` | P5 (`rwb_document`) | Write: version, required count, present count, missing types, complete, checked_at, last_event_id; upsert by case |
| `document` | P5 (`rwb_document`) | Read: case_id, document_type, is_active |
| `document_type` | P5 (`rwb_document`) | Read: the types in force for the load validation |
| `processed_event` | PLT library in `rwb_document` | Write: the consumed event IDs of the inbox |

No table of another service is read, written or joined.

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case contract fake | the rwb-case case read, with RWB-P3-E1043-CON for the reference data | The stage, the route and the owner of the case under test; the CaseStateChanged message of AC5 |
| rwb-case reference-data fake | RWB-PLT-E1043-CON with RWB-P3-E1043-CON | Version "CHK-2026.11" and "CHK-2026.12" with their rows and valid-from dates; the load of table "DOCUMENT_CHECKLIST" |
| document store fake | RWB-P5-E1024-APP | `rwb.document.DocumentStored.v1` for AC3, AC4, AC8 and AC9, with the same event ID twice for AC8 |
| document type table fake | RWB-P5-E1025-APP | The six agreed types and "DOCTYPE-2026.11", so the load refuses POWER_OF_ATTORNEY in AC7 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 1, consumed 2 | The checklist read and its batch form provided; the case read and the reference-data read consumed through the contract and the client library |
| Kafka | Published 0, consumed 2 | `rwb.document.DocumentStored.v1` and `rwb.case.CaseStateChanged.v1`, through the inbox |
| Temporal | 1 activity | `checklistRefresh` on queue `rwb-document`, as a step of the JOB-12 Schedule |
| File | None | The checklist file is posted to the rwb-case reference-load operation, not to this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `checklist`; front end folder `recovery/documents`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChecklistLoader | Service | Implements the reference-table loader for table "DOCUMENT_CHECKLIST" and validates rows against LOV-STAGE, LOV-ROUTE and the type table |
| ChecklistEvaluator | Service | Picks the rows for the stage and route, counts the active documents and writes `case_document_check` |
| DocumentStoredChecklistListener, CaseStateChangedChecklistListener | Listener | Inbox listeners that call the evaluator and keep the event ID for repeats |
| ChecklistRefreshActivity | Temporal activity | The refresh step of JOB-12: versions whose valid-from date has been reached since the last run |
| DocumentChecklistController | Controller | `GET /cases/{caseId}/document-checklist`, single and batch, with the access check |
| ChecklistRepository, CaseDocumentCheckRepository | Repository | Read and write the two tables of `rwb_document` only |
| DocumentChecklistPanel | React component | Replaces the placeholder on SCR-30 with required items present or missing |
| MissingDocumentsBadge | React component | The count shown on the SCR-02 case list rows, read through gateway-bff |

**Database**

- Flyway migration in the per-service sequence of DP-15 (legacy name `V1_5_040__document_checklist.sql`; the sequence number is the service's own) creates `document_checklist_item` (id, stage_code varchar(20), route_code varchar(4), document_type varchar(30), required boolean, sort_order integer, table_version varchar(20), valid_from date, valid_to date, load_id uuid, standard columns) with unique (stage_code, route_code, document_type, table_version); and `case_document_check` (id, case_id uuid, checklist_version varchar(20), required_count integer, present_count integer, missing_types jsonb, complete boolean, checked_at timestamptz, last_event_id uuid, standard columns) with unique (case_id).
- Index `ix_checklist_stage` on `document_checklist_item` (stage_code, valid_from).

**Configuration and reference data**

- Checklist "CHK-2026.11", prepared by the reference data administrator, agreed with the legal counsel and the litigation officers (DL19), loaded through the rwb-case reference-data contract.
- No property beyond the feature flag `rwb.document.checklist`.

**Build steps**

1. Write the migration; test the unique keys on `document_checklist_item` and on `case_document_check`.
2. Build ChecklistLoader with the validation against LOV-STAGE, LOV-ROUTE and the type table; test AC7.
3. Build ChecklistEvaluator with the route precedence and the active-version rule; unit test AC1, AC6 and AC9.
4. Build the two inbox listeners with the repeat check and the 503 path of X6; test AC3, AC4, AC5 and AC8.
5. Build ChecklistRefreshActivity and wire it into the JOB-12 Schedule; test AC2 on 30 November and 1 December 2026.
6. Extend the checklist operation with the batch form and build DocumentChecklistPanel and MissingDocumentsBadge; component tests and the access test.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 and DP-15 move the two legacy tables into `rwb_document` with the service's own migration. DP-07 replaces the shared reference-data service with the rwb-case contract, so the checklist version and its rows are versioned data. DP-09 is the event path: both events arrive through the inbox with the event ID as the key. DP-10 replaces the Quartz step of JOB-12 with the `checklistRefresh` activity on the `rwb-document` queue. DP-11 is the change to the case facts: the published interface `CaseDirectory` becomes a REST call with a mock, one hop and a 2 s budget. DP-13 and DP-19 put the two screens on the service base and the gateway-bff composite route.

**Done when.** The tests in section 16 pass, and the case list shows the missing count for the synthetic litigation cases in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-023 | Required documents are missing on the case | {count} required documents are missing for this case: {types}. |
| MSG-P3-027 | Checklist load fails a check | The {table} load was refused: {error} at row {row}. The version in force is unchanged. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the scope | This case is not in your scope. |

Thai text for each message follows decision DL10. MSG-P3-027 is owned by the rwb-case reference-load operation: this service raises the row error and rwb-case answers the message, so the text and the ID stay unchanged. Every error is an RFC 9457 problem response carrying `messageId`.

### 15. Screens and states

SCR-30 Case documents and SCR-02 Case list are reached through gateway-bff and the composite route of DP-19 (H RWB-PLT-N001-CON); the browser never calls `rwb-document` directly.

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-30 Case documents | list | The checklist panel with each required type present or missing, and MSG-P5-023 above it when a type is missing |
| SCR-30 Case documents | Loading | Skeleton rows while the checklist loads |
| SCR-02 Case list | list | A "Documents missing" count per case; 0 shows as empty |
| SCR-02 Case list | filtered | The user can filter cases with one or more missing documents |

The panel is RWB-P5-E1026-APP's tab with the required items filled by this story; when the stage has no checklist the panel shows the text of AC6 and no count. The route path and the fields gateway-bff merges are RWB-PLT-N001-CON's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-040-01 | AC1, BR1, BR2 | End to end | Litigation case with a demand letter and a court notice |
| TC-E1-040-02 | AC2, BR3 | End to end | Version CHK-2026.12 valid from 1 December 2026 |
| TC-E1-040-03 | AC3, BR5 | End to end | Deed in lieu case with two of three types |
| TC-E1-040-04 | AC4, BR5 | End to end | Settlement agreement stored on that case |
| TC-E1-040-05 | AC5, BR5 | End to end | Stage change from DEED_IN_LIEU to LITIGATION |
| TC-E1-040-06 | AC6 | End to end | Case at DEBT_SALE with no rows |
| TC-E1-040-07 | AC7 | End to end | Row with POWER_OF_ATTORNEY |
| TC-E1-040-08 | AC8, BR6 | End to end | DocumentStored delivered twice |
| TC-E1-040-09 | AC9, BR4 | End to end | Appraisal report with two versions |
| TC-E1-040-10 | Access | Component | Capacity and workforce planner (RW-CAPACITY, no Documents right) opens the checklist; refused with MSG-P4-002 |
| TC-E1-040-01-ITG | AC1, BR1, BR2 | Integration | The same litigation case across the real rwb-case, rwb-document and reference-data services |
| TC-E1-040-02-ITG | AC2, BR3 | Integration | The real reference-data load of CHK-2026.12 taking effect on its valid-from date |
| TC-E1-040-05-ITG | AC5, BR5 | Integration | The real CaseStateChanged from rwb-case recomputing the flag |
| TC-E1-040-08-ITG | AC8, BR6 | Integration | The same event ID delivered twice through the real topic and the inbox |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to End to end and Access to Component. The four `-ITG` copies are the wave-1 integration run, where the rwb-case contracts and the reference data are the real services instead of fakes.

### 17. Guardrails

- No business value in code: stages, routes and required types are rows in `document_checklist_item` (BR-P5-016, DP-07).
- No personal data in logs, tests or prompts: the flag holds type codes and counts only.
- No read of another service's tables (DP-01): stage, route and owner come through the rwb-case contract, and `rwb-case` reads the flag through the operation of 12.1.
- The evaluator never blocks a case move; it reports only.
- The migration runs in `rwb_document` on the per-service Flyway sequence; no shared baseline is edited (DP-15).
- The feature flag `rwb.document.checklist` returns the placeholder without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-011 | Checklist per case type as reference data so a missing document is visible | Business Requirements Epic 1, section 3.5 | FEAT-DCM-16 | 13 Manage documents and correspondence | R-UNI-38, R-UNI-40, R-LIT-16, R-LIT-17 | TC-E1-040-01 to TC-E1-040-10; the four -ITG copies |

| Legacy reference | Where it is kept |
|---|---|
| Acceptance criteria AC1 to AC9 and test cases TC-E1-040-01 to TC-E1-040-10 | Sections 7 and 16 |
| Rules BR1 to BR7, R-UNI-38 and R-UNI-40 | Sections 8 and 18 |
| Checklist version "CHK-2026.11" and its rows for LITIGATION and DEED_IN_LIEU | Preconditions, section 8, section 13 |
| Messages MSG-P5-023, MSG-P3-027, MSG-P4-002 and MSG-P4-003 | Section 14 and the exception paths |
| Tables `document_checklist_item` and `case_document_check`, fields DF-REF-234 to DF-REF-243 and DF-DOC-036 to DF-DOC-044 | Section 11 and section 13 |
| Legacy key RWB-E1-040; store RWB-P5-E1024-APP, types RWB-P5-E1025-APP, tab RWB-P5-E1026-APP | Metadata, sections 1, 3 and 12 |
| Not specified in the source documents: the rwb-case read and reference-load operation IDs, the batch count operation name and the Schedule ID (GAP-2337; ASM-3889) | Sections 3, 12.1, 12.2, 12.6 |

### 19. Out of scope

- The litigation pack check against the defect list and the block at filing (FEAT-LIT-05, Epic 5; CTL-19).
- The guarantee claim checklist (FEAT-GUA-01, Epic 4).
- Retrieval requests for missing documents (R-LIT-17, Epic 5).
- The review queue screen that shows the case checklist (RWB-E1-054).
- The document store and its event (RWB-P5-E1024-APP), the type table (RWB-P5-E1025-APP) and the tab shell (RWB-P5-E1026-APP).
- The case list screen of `rwb-case`; this story only provides the count it reads.
- The end-to-end proof across the real services (the `-ITG` copies of section 16).
