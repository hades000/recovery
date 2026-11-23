# RWB-P5-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1024-APP |
| Depends on (build) | RWB-P5-E1032-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1024-APP, RWB-P5-E1050-CON, RWB-P5-E1053-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-P5-E1032-INF, RWB-P5-E1032-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018, FR-P5-019, FR-P5-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the match and attach path of RWB-E1-032 moves into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the `matchStep` activity of `DocumentIntakeWorkflow` on queue `rwb-document` and the contract baseline RWB-P5-E1032-CON; the fifteen legacy criteria, the fourteen exception paths, the seven messages and the seventeen test cases are kept word for word in intent and values. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **documents from the OCR intake attached to their case automatically when the case ID or the account number is read, with unmatched or ambiguous documents held for a person who sees the OCR text and the candidate cases and attaches the document**, so that **no document is filed by hand when the case is clear and none is filed on the wrong case when it is not**.

Inside `rwb-document` this is the auto-attach capability of the document hub, and the same user story holds with the target service frame:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The matcher reads its three parameters `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` through the parameters contract and client library of `rwb-case` (DP-06, H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON). The rows they resolve to stay in `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5 (ASM-1748).
- The match outcomes, the review reasons and the review states are read as reference data through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON): LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW. No list value is typed in code.
- The case and the account are resolved through the `rwb-case` contract (RWB-P3-E1018-CON, one hop, 2 s timeout, DP-11), never from a case table of another service and never from a `recovery_case` copy: `GET /api/recovery/case/v1/cases/by-no/{caseNo}` for a case number and the open-cases-by-account read for an account number, whose exact path is Not specified in the source documents (GAP-0991; ASM-1749).
- The document is stored through the store capability of RWB-P5-E1024-APP, which stays the only writer of the `document` table and the DOCATT decision record; this story writes `document_intake` and reads `document_text`, and calls the store in the same service.
- The decision is recorded through the local decision-record library of DP-03 (H RWB-PLT-E1027-CON; the central ledger contract is RWB-P7-E1027-CON) with decision code DOCATT and the match method. A failed record means nothing is stored and the item stays `PENDING` (MSG-P7-003, R-UNI-39).
- The attach outcome is published as `rwb.document.DocumentAttached.v1` on `rwb.document.events.v1` (the legacy DocumentStored, EV-16, carried through the store), keyed by caseId, written to the outbox in the same transaction as the store (DP-09, H RWB-PLT-TE006-CON); the difference from the event catalogue of Arch v5 slide 42 is recorded as GAP-0991 and ASM-1752.
- JOB-12 Document intake becomes a Temporal Schedule started through the workflow kit (DP-10, H RWB-PLT-E1071-CON), and `matchStep` is one activity of `DocumentIntakeWorkflow` on queue `rwb-document`, registered by RWB-P5-E1049-APP, which owns the workflow. The Schedule is deployed and monitored by RWB-P5-E1032-OPS.
- The `document_intake` and `document_text` tables are created by this service's own per-service Flyway step in `rwb_document` (DP-15, H RWB-PLT-E1044-CON), and the Unmatched list reaches SCR-31 through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-0991); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.
- The legacy feature flag `rwb.dochub.autoattach` is retired with the monolith and replaced by `rwb.document.intake-autoattach` (ASM-1751).

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, flow, fourteen exception paths, seven business rules, seven messages, authority, data fields, fifteen acceptance criteria and seventeen test cases, adapted to the target service's schema, topic, API base and workflow template.

### 2. Business rationale

Scans, partner files and emails arrive without a case link; today a person reads each one and files it. This story matches each classified intake item to one open case by the case ID or the account number in its text and stores it on that case with no person involved (FSD P5 A2.12). An item that matches no case, more than one case, a closed case or no agreed type is held as unmatched, and a person attaches it from the review queue with the OCR text and the candidates in front of them. It meets REQ-DCM-007 and writes the document attached record required from Epic 1 (REQ-DRI-004, RWB-E1-027). The measure is fields extracted without review (FSD P5 A2.12.1).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01). No table of another service is read and no monolith table name survives; the legacy story names no monolith API path, so DP-13 is not in this story's pattern list.
2. The case is no longer read in process through `CaseDirectory`: it arrives through the `rwb-case` contract with a mock and a 2 s timeout (DP-11, ASM-1749), so the matcher builds against a published shape and its fake on Day 1.
3. The decision log write becomes the local decision-record library of DP-03, written in the same transaction as the `document_intake` update and the store's outbox row, and published on `rwb.decision-record.v1`; `rwb-decision` collects it into the central ledger.
4. The Quartz step of JOB-12 becomes the `matchStep` activity of the `DocumentIntakeWorkflow` template of the workflow kit, started by a Temporal Schedule on queue `rwb-document` (DP-10).
5. The account view read of the legacy flow (`v_ace_account` through `CaseDirectory`) is removed with the in-process call: the account number is matched inside the `rwb-case` answer and this service reads no ACE view (DP-05).
6. The three parameters arrive through the parameters contract and the five lists through the reference-data contract (DP-06, DP-07); the document-hub parameter rows sleep in `rwb_document`, which is P5's own store for them.
7. The attach event is written to the outbox inside the store transaction and published once per stored document by the relay (DP-09); the intake item update commits with it.
8. The intake tables are created in the per-service Flyway sequence (DP-15), and the Unmatched list and the item detail are served through the gateway-bff composite route (DP-19).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E1032-CON | The published baseline of the four intake operations, the IntakeItem, IntakeItemPage, Document and IntakeAttachRequest shapes, the five match outcomes, the error envelope and the `Idempotency-Key` rule |
| RWB-P5-E1024-APP | The store: `DocumentStoreService`, the DOCATT record, the `document` row, the duplicate check on case, type and hash, and the outbox row |
| RWB-PLT-E1027-CON | The decision-record library: the DOCATT record inside the caller's transaction, published on `rwb.decision-record.v1` (DP-03) |
| RWB-PLT-E1042-CON | The parameters client library for `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` (DP-06) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library, so the attach event and the item update share the store transaction (DP-09) |
| RWB-PLT-E1071-CON | The workflow kit with the L3 "Document intake" template, the activity registration and the retry policy (DP-10) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the intake migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the Unmatched list and the item detail to SCR-31 (DP-19) |
| RWB-P5-E1050-CON | The classification output the matcher reads: `predicted_type`, `classification_confidence`, `type_candidates`, `classifier_version`, `review_reason` |
| RWB-P5-E1053-CON | The extracted fields `case_no` and `account_no` of an item, where they were read |
| RWB-P3-E1042-CON | `rwb-case`'s parameters contract, which resolves the three parameters (DP-06) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the five lists (DP-07) |
| RWB-P5-E1032-INF | The compute of the intake workers, the OCR text storage, the hold container `rwb-quarantine`, the topic with retry and `.dlt`, the ACLs and the network path (the X dependency) |
| RWB-P5-E1032-OPS | The Helm release, the 15-minute intake Schedule, the dashboards, the alerts and the runbook (the X dependency) |

Business preconditions carried from RWB-E1-032, in the target wording:

- RWB-E1-024 is done: DocumentStore stores a document and writes the DOCATT decision log entry. In the target this is RWB-P5-E1024-APP in the same service, called through its published operation.
- RWB-E1-050 is done: intake items carry predicted_type, classification_confidence, type_candidates, classifier_version and review_reason.
- RWB-E1-053 is done: the extracted fields case_no and account_no are available for an item where they were read.
- Parameters loaded in document_hub_parameter: CASE_NO_PATTERN = "RW-[0-9]{4}-[0-9]{6}", ACCOUNT_NO_PATTERN = "[0-9]{10}" (assumed; DL21) and CLASSIFY_THRESHOLD = 0.80. The rows are read through the parameters contract of DP-06 (ASM-1748).
- The P3 published interface CaseDirectory returns a case by case number and the open cases for an account number. In the target CaseDirectory is the `rwb-case` contract RWB-P3-E1018-CON with its fake, one hop and a 2 s timeout (ASM-1749).
- A person resolving unmatched items holds Documents C; items with no candidate are visible only to roles with scope ALL.
- Feature flag `rwb.document.intake-autoattach` is on; it replaces the legacy `rwb.dochub.autoattach` (ASM-1751).
- The store of RWB-P5-E1024-APP is reachable, the hold container `rwb-quarantine` holds the file of a held item, and the intake Schedule of JOB-12 runs every 15 minutes in business hours.
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1746), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1747).

The field-level names of the four operations and the exact path of the open-cases-by-account read are Not specified in the source documents (GAP-0991; ASM-1749); the baseline RWB-P5-E1032-CON fixes the names this story is built against.

### 4. Flow

1. JOB-12 Document intake: the intake Schedule starts `DocumentIntakeWorkflow` on queue `rwb-document` every 15 minutes in business hours; it runs `matchStep` after the extraction step, as one activity of the same workflow (DP-10).
2. `matchStep`: selects `document_intake` rows with `ocr_status` DONE, `match_status` PENDING, no `document_id` and a predicted type (`review_reason` empty or LOW_CONFIDENCE), locking each row with `SELECT ... FOR UPDATE`; items with `review_reason` UNKNOWN_TYPE or MODEL_UNAVAILABLE get `match_status` NO_TYPE and are held for a person.
3. `CaseMatcher`: collects case numbers from the extracted field `case_no` and from the OCR text of `document_text` with `CASE_NO_PATTERN`, and account numbers from the extracted field `account_no` and the same text with `ACCOUNT_NO_PATTERN`; both patterns arrive through the parameters contract (DP-06).
4. `CaseMatcher`: resolves each case number through the `rwb-case` contract `GET /api/recovery/case/v1/cases/by-no/{caseNo}` and each account number through the open-cases-by-account read, and returns one of MATCHED, NO_MATCH, MULTIPLE, CONFLICT or CASE_CLOSED with the candidates. A contract error, a 2 s timeout or an open breaker fails the activity and leaves the item PENDING for the next run.
5. `matchStep`: for MATCHED, calls the store of RWB-P5-E1024-APP with the case ID, `predicted_type`, the intake source, the file of the hold container, its SHA-256 and the extracted fields; the store writes the DOCATT entry with the classifier version, the confidence and the match method, the `document` row and the attach event.
6. `matchStep`: on the stored document sets `classification_confidence`, `document_type` and `type_candidates`; for `review_reason` LOW_CONFIDENCE sets `review_status` PENDING and `write_once` false, so it is held in `rwb-docs` and listed on SCR-31 (RWB-E1-054).
7. `matchStep`: sets the `document_intake` row `match_status` MATCHED, `case_id` and `document_id`; for any other result sets `match_status` to the result and `candidate_case_ids`, and the item is held for a person. The row update, the store row and the outbox row commit in that order inside one transaction of `rwb_document`.
8. Reviewer: opens the Unmatched list on SCR-31 through the gateway-bff composite route (`GET /api/recovery/document/v1/intake-items`), opens an item to see the scan, the OCR text of `document_text` and the candidates (`GET /intake-items/{intakeItemId}` and `GET /intake-items/{intakeItemId}/content`), picks the case and the type, and attaches it (`POST /intake-items/{intakeItemId}/resolve`).
9. `ManualAttachService`: checks with `rwb-case` that the case is in the reviewer's scope and with the type table that the type is in force, calls the store with the reviewer as approver on the DOCATT entry, sets the item `match_status` MATCHED, `review_outcome` ATTACHED and `resolved_by`, and returns the Document. The `version` of the item is the optimistic lock.
10. Outbox relay: publishes `rwb.document.DocumentAttached.v1` to `rwb.document.events.v1` and the decision record to `rwb.decision-record.v1`, once per committed attach, keyed by caseId, with no personal data; the store's own `DocumentStored` row for the same document is the legacy EV-16 carried through (12.3, GAP-0991).

The decision record is written before the change takes effect and inside the store transaction, so a failed record leaves the document, the intake item and the outbox unchanged, and an automatic attach stays PENDING for the next run (R-UNI-39).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No readable case ID or account number | Item held, match_status NO_MATCH, OCR text held for the reviewer | MSG-P5-003 | AC2 |
| X2 | The account number matches two or more open cases | Item held, match_status MULTIPLE, every candidate offered | MSG-P5-003 | AC3 |
| X3 | The case ID and the account point to different cases | Item held, match_status CONFLICT, both cases offered | MSG-P5-003 | AC5 |
| X4 | A case ID is read that does not exist | No candidate; NO_MATCH | MSG-P5-003 | AC6 |
| X5 | The only candidate case is closed | Item held, match_status CASE_CLOSED | MSG-P5-003 | AC7 |
| X6 | The same file is already on the matched case | The item is linked to the existing document; no second document | None | AC8 |
| X7 | The job runs again over attached items | No second attach, entry or event | None | AC9 |
| X8 | Classification confidence below the threshold and one case matched | Stored with review_status PENDING and write_once false | MSG-P5-003 | AC10 |
| X9 | No agreed type from classification | Item held, match_status NO_TYPE | MSG-P5-003 | AC11 |
| X10 | The reviewer picks a case outside their scope | Refused with 403; item stays held | MSG-P4-003 | AC13 |
| X11 | The reviewer picks a type not in force | Refused with 422 | MSG-P5-006 | AC14 |
| X12 | Two reviewers attach the same item at the same time | The first succeeds; the second gets 409 | MSG-GEN-004 | AC15 |
| X13 | The decision log write fails during an attach | Nothing stored; an automatic attach stays PENDING for the next run; a manual attach returns 503; incident raised (R-UNI-39) | MSG-P7-003 | TC-E1-032-17 (Principle 5) |
| X14 | A role without Documents C attaches an item | Refused with 403 | MSG-P4-002 | TC-E1-032-16 (Access) |

Three target-service notes:

- JOB-12 is no longer a Quartz job: it is a Temporal Schedule on queue `rwb-document` in namespace `rwb-recovery`, registered from the values of RWB-P5-E1032-OPS, and `matchStep` is an activity of `DocumentIntakeWorkflow` on the same queue (DP-10). A run that leaves items PENDING is retried by the next run of the Schedule, exactly as the legacy restart behaviour states.
- The `rwb-case` contract answers two calls per item; a 2 s timeout, a 503 or an open breaker fails the activity, leaves the item PENDING and raises MSG-GEN-006 with {system} = "Case service"; the breaker shields `rwb-case`, and this service adds no retry of its own beyond the activity retry of the kit.
- The legacy `POST /intake-items/{intakeItemId}/attach` is published as `POST /intake-items/{intakeItemId}/resolve` (12.1, GAP-0991; ASM-1750); the refusal shapes of X10 to X14 are unchanged by the rename.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the store (RWB-P5-E1024-APP), the classification output (RWB-P5-E1050-CON), the extracted fields (RWB-P5-E1053-CON), the case contract (RWB-P3-E1018-CON), the decision-record library, the parameters and reference-data libraries, all earlier or contract work |
| Negotiable | The two patterns, the threshold, the outcomes and the reviewer action are data rows or fixed behaviour; the shapes come from the contract baseline |
| Valuable | Ends hand filing for every scan that names its case or account, and gives every other scan one place to be filed |
| Estimable | One job activity, one matcher, four endpoint operations, one list tab, one migration |
| Small | Fits within two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake

  Background:
    Given case "RW-2026-000123" is open, owned by "TEST-CO-01" and linked to account "TEST-ACC-0001"
    Given case "RW-2026-000456" is open and linked to account "TEST-ACC-0002"
    Given case "RW-2026-000789" is closed
    Given parameter CLASSIFY_THRESHOLD is 0.80
    Given the rwb-case contract mock returns case "RW-2026-000123" open with account "TEST-ACC-0001"
    Given the rwb-case contract mock returns case "RW-2026-000456" open with account "TEST-ACC-0002"
    Given the rwb-case contract mock returns case "RW-2026-000789" closed
    Given the rwb-case contract mock returns the open cases "RW-2026-000321" and "RW-2026-000654" for account "TEST-ACC-0003"

  Scenario: AC1 Auto attach (legacy RWB-E1-032 AC1)
    Given a scanned notice with the case ID "RW-2026-000123" read by OCR, classified "COURT_NOTICE" at 0.93 by classifier version "CLS-1.0"
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCATT"
    When intake completes
    Then the system stores the document on case "RW-2026-000123" with type "COURT_NOTICE", source "SCAN", classification_confidence 0.9300 and review_status "NOT_NEEDED" without a person
    Then one decision log entry "DOCATT" holds model version "CLS-1.0", confidence 0.93 and match method "CASE_ID"
    Then the system writes documentStored and the intake item has match_status "MATCHED" and the document ID

  Scenario: AC2 No match (legacy RWB-E1-032 AC2)
    Given a scan with no readable case ID and no readable account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"
    Then GET /intake-items/{intakeItemId} returns its OCR text pages
    Then the system writes no document row

  Scenario: AC3 Two candidates (legacy RWB-E1-032 AC3)
    Given a scan whose account number "TEST-ACC-0003" is linked to open cases "RW-2026-000321" and "RW-2026-000654"
    When intake completes
    Then the intake item has match_status "MULTIPLE"
    Then candidate_case_ids holds both cases and the Unmatched list on SCR-31 offers both
    Then the system writes no document row

  Scenario: AC4 Match by account number (legacy RWB-E1-032 AC4)
    Given a scan with no case ID and the account number "TEST-ACC-0002", classified "DEMAND_LETTER" at 0.88
    When intake completes
    Then the system stores the document on case "RW-2026-000456"
    Then the decision log entry holds match method "ACCOUNT_NO"

  Scenario: AC5 Case ID and account disagree (legacy RWB-E1-032 AC5)
    Given a scan with the case ID "RW-2026-000123" and the account number "TEST-ACC-0002"
    When intake completes
    Then the intake item has match_status "CONFLICT" and candidates "RW-2026-000123" and "RW-2026-000456"

  Scenario: AC6 Case ID that does not exist (legacy RWB-E1-032 AC6)
    Given a scan with the case ID "RW-2026-999999" and no account number
    When intake completes
    Then the intake item has match_status "NO_MATCH"

  Scenario: AC7 Only candidate is closed (legacy RWB-E1-032 AC7)
    Given a scan with the case ID "RW-2026-000789"
    When intake completes
    Then the intake item has match_status "CASE_CLOSED" and candidate "RW-2026-000789"
    Then the system writes no document row

  Scenario: AC8 The same file is already on the case (legacy RWB-E1-032 AC8)
    Given the court notice from AC1 is stored on case "RW-2026-000123"
    Given a second intake item holds the same file with the same hash
    When intake completes
    Then the second item has match_status "MATCHED" and the document ID from AC1
    Then the case holds one copy of that court notice and one "DOCATT" entry for it

  Scenario: AC9 Repeat run (legacy RWB-E1-032 AC9)
    Given 15 intake items already "MATCHED"
    When JOB-12 runs again
    Then no further document row, decision log entry or DocumentStored event is written for them

  Scenario: AC10 Low classification confidence with one case (legacy RWB-E1-032 AC10)
    Given a scan with the case ID "RW-2026-000123" classified "APPRAISAL_REPORT" at 0.62 with candidates APPRAISAL_REPORT 0.62 and TITLE_DEED 0.30
    When intake completes
    Then the system stores the document on case "RW-2026-000123" with review_status "PENDING", write_once false and the file in "rwb-docs"
    Then the document carries document_type "APPRAISAL_REPORT" and both candidates for SCR-31

  Scenario: AC11 No agreed type (legacy RWB-E1-032 AC11)
    Given a scan with the case ID "RW-2026-000123" and review_reason "UNKNOWN_TYPE" from classification
    When intake completes
    Then the intake item has match_status "NO_TYPE" with candidate "RW-2026-000123"

  Scenario: AC12 A reviewer attaches an unmatched item (legacy RWB-E1-032 AC12)
    Given the item from AC3 and reviewer "TEST-LIT-01" holding RW-LITOFF with both candidate cases in scope
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCATT"
    When "TEST-LIT-01" attaches it to "RW-2026-000654" with type "GUARANTOR_NOTICE"
    Then the system stores the document on "RW-2026-000654" with type "GUARANTOR_NOTICE"
    Then the "DOCATT" entry names "TEST-LIT-01" as approver and match method "PERSON"
    Then the intake item has match_status "MATCHED"

  Scenario: AC13 Reviewer picks a case outside their scope (legacy RWB-E1-032 AC13)
    Given reviewer "TEST-LIT-02" whose scope does not include case "RW-2026-000654"
    When "TEST-LIT-02" attaches the item from AC3 to "RW-2026-000654"
    Then the system refuses the request with 403 and MSG-P4-003
    Then the item keeps match_status "MULTIPLE"

  Scenario: AC14 Reviewer picks a type not in force (legacy RWB-E1-032 AC14)
    Given the item from AC2 and a reviewer with scope ALL
    When the reviewer attaches it to "RW-2026-000123" with type "PAYSLIP"
    Then the system refuses the request with 422 and MSG-P5-006 naming "PAYSLIP"

  Scenario: AC15 Two reviewers attach the same item (legacy RWB-E1-032 AC15)
    Given the item from AC2 at version 3
    When two reviewers attach it at the same time with version 3
    Then one request returns 201 and the other returns 409 with MSG-GEN-004
    Then one document row exists for the item
```

Every Given, When and Then line above is the legacy line unchanged: the only added lines are the four Background mock Givens on the `rwb-case` contract and the `rwb-decision` contract Given in AC1 and AC12, and the legacy endpoints map to the target operations of 12.1 as `GET /review-items` → `GET /api/recovery/document/v1/intake-items`, `GET /intake-items/{id}` → `GET /api/recovery/document/v1/intake-items/{intakeItemId}`, `POST /intake-items/{id}/attach` → `POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve`, and `JOB-12` → the intake Schedule that starts `DocumentIntakeWorkflow` with its `matchStep` activity.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A classified document attaches to its case without a person when exactly one open case is found | REQ-DCM-007; FEAT-DCM-12 |
| BR2 | The case is found by the case ID or the account number read from the document; the account number is the join to other systems | DL21; parameters CASE_NO_PATTERN and ACCOUNT_NO_PATTERN in document_hub_parameter (New) |
| BR3 | No match, more than one candidate, disagreement, a closed case or no agreed type goes to a person | REQ-DCM-005; FSD P5 A2.12.4 |
| BR4 | A document classified below the threshold is stored for review in the standard container, not write-once, until a person confirms its type | Parameter CLASSIFY_THRESHOLD in document_hub_parameter (New); RWB-E1-054; CTL-12 |
| BR5 | Each attach is written to the decision log with the classifier version, the confidence and the person where one decided, before the document is stored | Principle 5; R-UNI-39; REQ-DRI-004 |
| BR6 | An item attached once is not attached again | R-UNI-40 |
| BR7 | A reviewer attaches only to a case in their scope | CTL-09 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 and BR3 are executed by `CaseMatcher` over the answer of the `rwb-case` contract: the five outcomes are fixed behaviour, not rule rows, and the matcher never picks one of several candidates. An item with no candidate reaches a role with scope ALL only.
- BR2 is executed by the two patterns read through the parameters contract (DP-06): the patterns are compared against the extracted fields and the `document_text` pages, and no pattern is typed in code.
- BR4 is executed by `matchStep` setting `review_status` PENDING and `write_once` false on the stored document, so the store keeps the file in `rwb-docs` and not in `rwb-docs-legal` (RWB-P5-E1024-APP); the confirmation of the type and the fields is RWB-P5-E1054-APP.
- BR5 is executed by the decision-record library of DP-03 inside the store transaction: the DOCATT record, the `document` row, the `document_intake` update and the outbox row commit together or not at all (R-UNI-39).
- BR6 is executed by the selection rule of `matchStep` (`match_status` PENDING and no `document_id`), by the store's duplicate check on case, type and hash (`uk_document_case_type_hash`) and by the optimistic lock on `document_intake.version`.
- BR7 is executed by the authorisation decision the service template's guard holds against `rwb-access`, and by the case read of the chosen case before the store call; every read of the item detail is written to the PII access log by the ACE common module, never by this package.
- DP-05 keeps ACE data out of this service: the account number is matched inside the `rwb-case` answer and no `v_ace_*` view is read. DP-09 puts the attach event in the outbox; DP-15 puts the intake migration in the per-service sequence; DP-19 puts the two screens behind the gateway-bff composite route.

### 9. State transitions

None for the case. This story does not change a case status. It changes the intake item match_status: PENDING to MATCHED on an automatic attach; PENDING to NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED or NO_TYPE when held for a person; a held value to MATCHED when a reviewer attaches it. It creates a document record (COPY_PENDING, then STORED, in RWB-E1-024, now RWB-P5-E1024-APP).

| From (`document_intake.match_status`) | Event | Condition | To |
|---|---|---|---|
| PENDING | `matchStep` finds exactly one open case and the type is agreed | The store commits with the DOCATT record and the outbox row | MATCHED |
| PENDING | `matchStep` finds no case | No case number and no account number resolves | NO_MATCH |
| PENDING | `matchStep` finds two or more open cases for the account | The store is not called | MULTIPLE |
| PENDING | `matchStep` finds a case number and an account that point to different cases | The store is not called | CONFLICT |
| PENDING | `matchStep` finds only a closed case | The store is not called | CASE_CLOSED |
| PENDING | `matchStep` reads UNKNOWN_TYPE or MODEL_UNAVAILABLE from classification | The store is not called | NO_TYPE |
| NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED, NO_TYPE | A reviewer resolves the item | Scope and type checks pass, the store commits | MATCHED |

The held values are the same on a repeat run: an item in any held state is not selected by `matchStep` again, and an item that fails on the decision record stays PENDING. The document state machine COPY_PENDING to STORED belongs to RWB-P5-E1024-APP and is not changed by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, OCR and extraction pipeline | Matches and attaches automatically (Documents C) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry |
| Roles with Documents C and the candidate case in scope (for example RW-LITOFF, RW-CASEOWN) | See and attach unmatched items that name a candidate in their scope |
| Roles with Documents C and scope ALL (for example RW-LEGAL) | See and attach unmatched items with no candidate |
| Roles with Documents R only (for example RW-TEAMMGR) | See attached documents on cases in their scope; no attach |

In the target the authorisation decision is taken by `rwb-access` (roles as data, scope, masking and DoA in `rwb_access`) and consumed as the cached permission decision the service holds; this story adds no guard of its own and inherits the 403 shapes of MSG-P4-002 and MSG-P4-003. SY-DECLOG is the local decision-record library of DP-03 in the target, called inside the store transaction, and it publishes the DOCATT record on `rwb.decision-record.v1`. The worker runs as the rwb-document service identity (DP-02), carried by the chart as a secret reference; the login name is Not specified in the source documents (GAP-0991).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `rwb-case` case, through the contract | id | Read |
| DF-CAS-002 | `rwb-case` case, through the contract | case_no | Read |
| DF-CAS-005 | `rwb-case` case, through the contract | status | Read |
| DF-CAS-026 | `rwb-case` case and account, through the contract | account_key | Read |
| DF-ACE-002 | `v_ace_account`, reached only inside the `rwb-case` answer | account_code | Read |
| DF-DOC-001 to DF-DOC-011 | `document`, through the store of RWB-P5-E1024-APP | all fields | Write, through the store |
| DF-DOC-004 | `document` | document_type | Write, through the store |
| DF-DOC-007 | `document` | classification_confidence | Write, through the store |
| DF-DOC-008 | `document` | review_status | Write, through the store |
| DF-DOC-010 | `document` | write_once | Write, through the store |
| DF-DOC-075 | `document_intake` | match_status | Write |
| DF-DOC-076 | `document_intake` | candidate_case_ids | Write |
| DF-DOC-060 | `document_intake` | case_id | Write |
| DF-DOC-061 | `document_intake` | document_id | Write |
| DF-DOC-081 | `document_intake` | review_outcome | Write |
| DF-DOC-082 | `document_intake` | resolved_by | Write |
| DF-DOC-083 | `document_intake` | resolved_at | Write |
| DF-DOC-070 | `document_intake` | predicted_type | Read |
| DF-DOC-071 | `document_intake` | classification_confidence | Read |
| DF-DOC-072 | `document_intake` | type_candidates | Read |
| DF-DOC-073 | `document_intake` | classifier_version | Read |
| DF-DOC-080 | `document_intake` | review_reason | Read |
| DF-DOC-056 | `document_intake` | file_sha256 | Read |
| DF-DOC-063 | `document_intake` | ocr_status | Read |
| DF-DOC-057 | `document_intake` | intake_ref | Read |
| DF-DOC-089 | `document_text` | text_content | Read |
| DF-DOC-088 | `document_text` | page_no | Read |
| DF-REF-244 to DF-REF-250 | `document_hub_parameter` | the three parameter rows | Read, resolved through DP-06 |
| (decision record) | decision-record library table in `rwb_document` | chain_seq, inputsRef, ruleId, finalCall, decidedAt, prev_hash, entry_hash | Write, through the library |
| (outbox) | outbox library table in `rwb_document` | the row for the attach event and the decision record | Write, through the library |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `recovery_case` row is copied and no ACE view is read by this service: DF-CAS-001, DF-CAS-002, DF-CAS-005, DF-CAS-026 and DF-ACE-002 arrive inside the `rwb-case` contract answer, and DP-01 forbids a foreign-schema read. Personal data never enters the event payload, the workflow input, the decision record or the log: OCR text is read by the reviewer's screen only, and a log line carries the intake item ID, the outcome and the match method, never a text page, a file name or an account number in clear.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`; the shapes are those of RWB-P5-E1032-CON.

| Method | Path | Owner | Notes |
|---|---|---|---|
| POST | `/api/recovery/document/v1/intake-items/{intakeItemId}/resolve` | P5 | Resolve a held item: attach it to a case in scope with a type in force. `IntakeAttachRequest` in, 201 `Document` out, Documents C on the chosen case, `Idempotency-Key` required, `version` as the optimistic lock. The legacy name `/attach` and the TSD right U are recorded in GAP-0991 and ASM-1750 |
| GET | `/api/recovery/document/v1/intake-items` | P5 | The Unmatched list of SCR-31 (legacy `GET /review-items`): query `matchStatus` (default the five held values NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE), `page`, `size` (default 50); answer 200 `IntakeItemPage`, oldest first, only items whose candidates are in scope, and items with no candidate for scope ALL |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}` | P5 | One held item as `IntakeItem`: source, received time, match status, predicted type, confidence, the type candidates, the candidate cases and the OCR text pages, masked by role; each read written to the PII access log |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/content` | P5 | The file of the held item as `application/octet-stream`, read from `rwb-quarantine` through the storage product; Documents R with scope applied |

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/by-no/{caseNo}` | P3 rwb-case | RWB-P3-E1018-CON | The case exists, its status and its owner; one hop, 2 s timeout, breaker per downstream, one GET retry with jitter (DP-11) |
| GET | the open-cases-by-account read of rwb-case | P3 rwb-case | RWB-P3-E1018-CON | The open cases of an account number for the MULTIPLE outcome; one hop, 2 s timeout; the exact path is Not specified in the source documents (GAP-0991; ASM-1749) |
| GET | the parameters read of DP-06 | P3 behind the client library | RWB-P3-E1042-CON | `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN`, `CLASSIFY_THRESHOLD`, cached for 5 minutes |
| GET | the reference-data read of DP-07 | P3 behind the client library | RWB-P3-E1043-CON | LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW, LOV-DOC-TYPE, LOV-DOC-SOURCE, LOV-REVIEW |

The store of RWB-P5-E1024-APP is the same service and is called through its published operation (`POST /api/recovery/document/v1/documents/{documentId}/store`), one hop with a 2 s budget; it is not a contract of another service and appears in 12.9 as REST consumed inside the service. A failed case read maps to 503 with MSG-GEN-006 naming "Case service" and leaves the item PENDING.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentAttached.v1` (the attach outcome; the legacy DocumentStored, EV-16) | `rwb.document.events.v1`, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | P5 | caseId | documentId, caseId, documentType, source, intakeItemId, matchMethod, attachedAt |
| decision record (DOCATT) | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with decision code DOCATT, the match method CASE_ID, ACCOUNT_NO or PERSON, the classifier version and the confidence |

CloudEvents 1.0 envelope, binary mode; no personal data and no OCR text in either payload. The attach event and the record are written to the outbox inside the store transaction, so they exist exactly when the document row and the item update exist. Arch v5 slide 42 lists DocumentStored and DocumentFieldsExtracted for this service and not the name above; the difference is recorded as GAP-0991 and ASM-1752, and the event catalogue owner confirms the final name before the wave 1 release.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The path is started by the intake Schedule, not by an event: the classification output of RWB-P5-E1050-CON and the extracted fields of RWB-P5-E1053-CON are written by other activities of the same workflow in `rwb_document`. `rwb.document.DocumentAttached.v1` and `rwb.document.DocumentStored.v1` are consumed by `rwb-case` and `rwb-agent`, not by this story |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| `DocumentIntakeWorkflow` | Workflow, from the L3 workflow kit template "Document intake" | `rwb-document` | OCR, classify, extract, match; owned and registered by RWB-P5-E1049-APP |
| `matchStep` | Activity | `rwb-document` | Contributed by this story: select, match, store or hold, and update the item; idempotent by the intake item ID and the store's case, type and hash rule |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None in this story | `DocumentIntakeWorkflow` | `rwb-document` | Every 15 minutes in business hours (JOB-12) | The Schedule is registered from the values of RWB-P5-E1032-OPS and its run book is that story's; this story contributes only the `matchStep` activity the Schedule-started workflow calls |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document` | P5 | Written only through the store of RWB-P5-E1024-APP, never by this story directly |
| `document_intake` | P5 | The item row: read for selection, written with `match_status`, `candidate_case_ids`, `case_id`, `document_id`, `review_outcome`, `resolved_by` and `resolved_at` |
| `document_text` | P5 | Read only: the OCR pages the patterns are compared against and the reviewer's screen returns |
| `document_hub_parameter` | P5 | Read only through the parameters contract of DP-06; the rows are P5's |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record, in the store transaction |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The attach event and the record; the `Idempotency-Key` row of the resolve operation |

No foreign-schema table is read (DP-01) and no ACE view is read by this service (DP-05).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| rwb-case case fake (`GET /cases/by-no/{caseNo}` and the open-cases read) | RWB-P3-E1018-CON | The five outcomes of AC2 to AC7, the scope check of AC13 and the 2 s timeout path |
| parameters fake | RWB-P3-E1042-CON (through RWB-PLT-E1042-CON) | `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` 0.80 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | The five lists, including the seven values of LOV-INTAKE-MATCH |
| decision-record fake | RWB-PLT-E1027-CON | The local DOCATT record and the publish on `rwb.decision-record.v1` |
| central ledger fake | RWB-P7-E1027-CON | The collection of the record into the central ledger |
| store fake or stub | RWB-P5-E1024-APP | The store answer, the duplicate answer of AC8 and the COPY_PENDING state |
| intake baseline fake | RWB-P5-E1032-CON | The four operations and the four shapes, so the tests build before the app code lands |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 4, consumed 2 cross-service plus 1 in-service | The resolve, the list, the item read and the content read; the two `rwb-case` reads; the store operation of the same service |
| Kafka | Published 1 event and 1 decision record; consumed 0 | `rwb.document.DocumentAttached.v1` on `rwb.document.events.v1`, the record on `rwb.decision-record.v1` |
| Temporal | 1 workflow observed, 1 activity contributed, 1 Schedule observed | `DocumentIntakeWorkflow` with `matchStep` on queue `rwb-document`; the 15-minute Schedule is registered by RWB-P5-E1032-OPS |
| File | The held file and the stored file | Read from `rwb-quarantine` through the storage product; the store writes it to `rwb-docs` or `rwb-docs-legal` under the type's write-once flag |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `intake/attach`; front end folder `recovery/documents`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| MatchStepActivity | Temporal activity | `matchStep`: select, lock, match, store or hold, update `document_intake`; idempotent by item ID |
| CaseMatcher | Service | Reads case numbers and account numbers from the extracted fields and `document_text`; resolves them through `rwb-case`; returns the outcome and the candidates |
| MatchPatterns | Library client | Reads `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` through the parameters contract, cached for 5 minutes |
| AutoAttachService | Service | Builds the store request with the classification inputs, applies the review rule of BR4 and updates the item |
| ManualAttachService | Service | Scope and type checks, optimistic lock on the item, store call with the reviewer as approver |
| IntakeItemController | Controller | The four operations of 12.1, with the access check, the scope filter and the RFC 9457 error mapping |
| IntakeItemRepository | Repository | Reads and writes `document_intake` only, and reads `document_text`; `version` is the optimistic lock |
| UnmatchedIntakeTab | React component | The Unmatched list on SCR-31 with the scan viewer, the OCR text, the candidates, the case picker and the type picker |

**Database.**

- One migration in the per-service Flyway sequence (DP-15): `V1032_1__intake_match.sql` adds to `document_intake` `match_status` varchar(12) not null default 'PENDING', `candidate_case_ids` jsonb, `review_outcome` varchar(12), `resolved_by` uuid and `resolved_at` timestamptz; the classification columns come from the RWB-P5-E1050-CON migration and the text table from the RWB-P5-E1049-APP migration.
- Indexes: `ix_intake_held ON document_intake (match_status, received_at) WHERE match_status NOT IN ('PENDING', 'MATCHED')`; `ix_intake_pending ON document_intake (match_status, received_at) WHERE match_status = 'PENDING'`; `ix_intake_sha ON document_intake (file_sha256)`.

**Configuration and reference data.**

- Parameters `CASE_NO_PATTERN` = "RW-[0-9]{4}-[0-9]{6}", `ACCOUNT_NO_PATTERN` = "[0-9]{10}" (assumed; DL21) and `CLASSIFY_THRESHOLD` = 0.80 in `document_hub_parameter`, read through the parameters contract (DP-06, ASM-1748).
- Reference lists LOV-INTAKE-MATCH, LOV-INTAKE-REVIEW, LOV-DOC-TYPE, LOV-DOC-SOURCE and LOV-REVIEW read through the reference-data contract (DP-07); no list value is typed in code.
- Decision code DOCATT, assumed, with the LOV-DECISION list loaded by the data steward; the match method is one of CASE_ID, ACCOUNT_NO or PERSON.
- Feature flag `rwb.document.intake-autoattach` (ASM-1751). Off: `matchStep` sets every classified item to `match_status` NO_MATCH and reviewers attach them by hand, exactly as the legacy flag states.

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

DP-01 moves the three tables the legacy story wrote into `rwb_document` and stops the module reaching into the recovery schema: `document_intake` and `document_text` are this service's, and the `document` row is written only through the store. DP-03 replaces `DecisionLogWriter` with the local library, so the DOCATT record, the item update and the outbox row share one transaction and the record is published on the shared topic. DP-05 is applied by removal: the legacy `AceSourceQuery` and `v_ace_account` read inside `CaseDirectory` are gone, because the account number is matched inside the `rwb-case` answer and this service reads no ACE view. DP-06 and DP-07 keep the three parameters and the five lists out of the code through the two client libraries, while the parameter rows themselves stay in `rwb_document` as the Ownership Map gives them to P5. DP-09 puts the attach event and the record in the outbox. DP-10 turns the Quartz step of JOB-12 into the `matchStep` activity of the kit's "Document intake" template, started by a Schedule that this story does not register. DP-11 is the case read: one hop, a published shape, a fake in the build and a 2 s timeout, replacing the in-process `CaseDirectory`. DP-15 puts the intake migration in the service's own sequence. DP-19 puts the Unmatched list and the item detail behind the gateway-bff composite route, so SCR-31 calls the owner once.

**Build steps**

1. Write the migration and the entities; test that the held index returns only held items and that the optimistic lock refuses a stale `version`.
2. Build `MatchPatterns` and the text scan; unit test the two patterns on synthetic Thai and English text around the numbers.
3. Build `CaseMatcher` against the case fake and unit test the five outcomes, AC2 to AC7, and the 2 s timeout path.
4. Build `AutoAttachService` with the store call, the review rule of BR4 and the item update; integration test AC1, AC4, AC8, AC10 and AC11.
5. Build `MatchStepActivity` selection and skip rules and register it with the kit on queue `rwb-document`; test AC9 and the repeat run.
6. Build `IntakeItemController` and `ManualAttachService`; API tests AC12 to AC15, the access test TC-E1-032-16 and the scope refusal of AC13.
7. Build `UnmatchedIntakeTab`; component tests for the list, the detail, the OCR text, the candidates and the attach dialog.
8. Test the decision-record failure path for the automatic and the manual attach (TC-E1-032-17) and confirm that nothing is stored and the item stays PENDING.

**Done when.** The tests in section 16 pass and, on the 180 synthetic samples in SIT, every item with one readable case ID and a confidence at or above 0.80 is attached in the same run, with one DOCATT record and one attach event per stored document.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | Item held for a person or document stored for review | Some fields need checking. The document is in the review queue. |
| MSG-P5-006 | Reviewer picks a type not in force | {value} is not a document type in force. Choose a type from the list. |
| MSG-GEN-001 | Case or type missing on attach | Enter {field}. |
| MSG-GEN-004 | Item attached by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Chosen case outside the scope | This case is not in your scope. |

Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The HTTP mapping is the legacy one and is fixed by AC13 to AC15 and the baseline RWB-P5-E1032-CON: 403 for MSG-P4-002 and MSG-P4-003, 409 for MSG-GEN-004, 422 for MSG-P5-006 and MSG-GEN-001, and 503 for MSG-P7-003 and MSG-GEN-006 naming "Case service". MSG-P5-003 is not an error response: it is the label of a held item and of a document stored for review on SCR-31 and SCR-30. A held item that a reviewer opens is a 200; an item that no longer exists answers 404 with a not-found message whose ID is Not specified in the source documents (GAP-0991).

### 15. Screens and states

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the Unmatched list loads through the gateway-bff composite route |
| SCR-31 Document review queue | list | The Unmatched tab: items oldest first with source, received time, match status, proposed type and candidate cases |
| SCR-31 Document review queue | held | An item in NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED or NO_TYPE shows MSG-P5-003, its OCR text pages by role and the candidates it has, and the attach dialog with the case picker and the type picker |
| SCR-31 Document review queue | refused | A case outside the scope answers MSG-P4-003 in the dialog and the item keeps its held status; a type not in force answers MSG-P5-006 naming the value |
| SCR-31 Document review queue | reviewed | The item is attached; it leaves the list and the document opens on SCR-30 of the chosen case |
| SCR-30 Case documents | list | An automatically attached document shows on its case; a PENDING document shows MSG-P5-003 |

The tab for documents pending type or field review on SCR-31 is built in RWB-E1-054 (now RWB-P5-E1054-APP), and the case document list is RWB-P5-E1026-APP; this story adds the Unmatched tab and the attach dialog only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-032-17 | X13, BR5 (legacy Principle 5) | NFR | Decision log write forced to fail during an automatic and a manual attach; nothing stored, MSG-P7-003, incident raised |
| TC-E1-032-16 | X14, BR7 (legacy Access) | Component | Team manager (RW-TEAMMGR, Documents R only) attaches an unmatched item; refused with MSG-P4-002 |
| TC-E1-032-01 | AC1, BR1, BR5 | End to end | Synthetic notice with RW-2026-000123 at 0.93 |
| TC-E1-032-02 | AC2, BR3 | End to end | Synthetic scan with no identifiers |
| TC-E1-032-03 | AC3, BR3 | End to end | Account TEST-ACC-0003 on two open cases |
| TC-E1-032-04 | AC4, BR2 | End to end | Account TEST-ACC-0002 only |
| TC-E1-032-05 | AC5, BR3 | End to end | Case ID and account on different cases |
| TC-E1-032-06 | AC6, BR3 | End to end | Case ID RW-2026-999999 |
| TC-E1-032-07 | AC7, BR3 | End to end | Closed case RW-2026-000789 |
| TC-E1-032-08 | AC8, BR6 | End to end | Same file in two intake items |
| TC-E1-032-09 | AC9, BR6 | End to end | 15 items already MATCHED |
| TC-E1-032-10 | AC10, BR4 | End to end | Scan classified APPRAISAL_REPORT at 0.62 on a matched case |
| TC-E1-032-11 | AC11, BR3 | End to end | Item with review_reason UNKNOWN_TYPE |
| TC-E1-032-12 | AC12, BR5 | End to end | Reviewer attaches a MULTIPLE item |
| TC-E1-032-13 | AC13, BR7 | End to end | Reviewer with a scope that excludes the chosen case |
| TC-E1-032-14 | AC14 | End to end | Type PAYSLIP |
| TC-E1-032-15 | AC15 | End to end | Two parallel attach requests at version 3 |

The legacy level System maps to End to end, Access to Component and Resilience to NFR. The wave-1 integration harness copies TC-E1-032-01 as RWB-ITG-E1032-ITG, where the real `rwb-case` and the real store replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the case number and account number patterns and the threshold are parameters read through DP-06, and the five lists are reference data read through DP-07.
- No personal data in logs, tests or prompts: account numbers and OCR text are never logged; logs carry the intake ID and the outcome; test accounts are synthetic.
- No read of another module's tables: cases and accounts are resolved through the `rwb-case` contract, one hop, 2 s timeout, and no `v_ace_*` view is read by this service (DP-01, DP-05).
- The matcher never picks one of several candidates; any doubt goes to a person, and an item with no candidate is visible only to a role with scope ALL.
- A document stored for type review is never put in the write-once container before its type is confirmed: `write_once` false and `rwb-docs` until RWB-P5-E1054-APP confirms the type (RWB-E1-054; CTL-12).
- The decision record is written in the same transaction as the document, the item update and the outbox row; a failure stores nothing (R-UNI-39).
- The attach is idempotent twice over: `Idempotency-Key` on the resolve POST, and the selection rule plus the store's duplicate check on case, type and hash.
- The feature flag `rwb.document.intake-autoattach` removes the automatic attach without a rollback of the schema (ASM-1751).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-032-01 to TC-E1-032-15, TC-E1-032-17 |
| REQ-DCM-005 | A document whose match is not certain is held for a person and never filed on a guess | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-032-02, TC-E1-032-03, TC-E1-032-05, TC-E1-032-06, TC-E1-032-07, TC-E1-032-11 |
| REQ-DRI-004 | Every decision is written to the decision log before it takes effect | Business Requirements Program, section 5.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39 | TC-E1-032-01, TC-E1-032-12, TC-E1-032-17 |

| Legacy reference | Where it is kept |
|---|---|
| DocumentStored (EV-16) through DocumentStore | Sections 1, 4, 12.3, 17 |
| MSG-P5-003, MSG-P5-006, MSG-GEN-001, MSG-GEN-004, MSG-P7-003, MSG-P4-002, MSG-P4-003 | Section 14 and the exception paths |
| Parameters CASE_NO_PATTERN, ACCOUNT_NO_PATTERN and CLASSIFY_THRESHOLD = 0.80 | Background, sections 1, 3, 8, 13 |
| Rules R-UNI-39, R-UNI-40, CTL-09, CTL-12, DL21 | Sections 2, 8, 17, 18 |
| Containers `rwb-docs` and `rwb-quarantine`, file in "rwb-docs" | Sections 4, 12.9, 13 |
| Legacy key RWB-E1-032, AC1 to AC15, TC-E1-032-01 to TC-E1-032-17 | Metadata, section 7, section 16 |

### 19. Out of scope

- Confirming or correcting the type and the fields of a document stored for review (RWB-P5-E1054-APP; legacy RWB-E1-054).
- Source pickup from scanners, SFTP and mailboxes, and the intake item base record (RWB-P5-E1049-APP; legacy RWB-E1-057).
- The store itself, the write-once container and the version history (RWB-P5-E1024-APP).
- OCR, classification and field extraction (RWB-P5-E1049-APP, RWB-P5-E1050-APP, RWB-P5-E1053-APP), which this story reads only.
- Moving an attached document to another case (Epic 2).
- Attach of field app photos (RWB-E2-024, now a wave 2 story of P5).
- The published contract documents, the fakes and their versioning (RWB-P5-E1032-CON).
- The compute, the storage, the topic and the ACL provisioning (RWB-P5-E1032-INF); the chart, the Schedule registration, the dashboards, the alerts and the runbook (RWB-P5-E1032-OPS).
