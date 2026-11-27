# RWB-P5-E1054-APP Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P5-E1054-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-document |
| Service epic | RWB-SVC-P5 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-054 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P5-E1054-APP-16) |
| Contract baseline version | RWB-P5-E1054-CON, version Not specified in the source documents (DOR-RWB-P5-E1054-APP-23) |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P5-G |
| Ready to start | After RWB-P5-E1049-APP, RWB-P5-E1032-APP |
| Depends on (build) | RWB-P5-E1054-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P5-E1049-APP, RWB-P5-E1032-APP, RWB-P5-E1050-CON, RWB-P5-E1053-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P3-E1035-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md (FR-P5-015, FR-P5-017, FR-P5-018, FR-P5-024) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the review queue of RWB-E1-054 moves into `rwb-document` with the schema `rwb_document`, the topic `rwb.document.events.v1`, the REST base `/api/recovery/document/v1`, the task queue `rwb-document` in namespace `rwb-recovery` and the contract baseline RWB-P5-E1054-CON; the seventeen legacy criteria, the thirteen exception paths, the ten business rules, the eleven messages, the nineteen data rows and the nineteen legacy test cases are kept word for word in intent and values, and the two legacy paths that carried `/api/recovery/v1` are rebased by DP-13. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P5-E1054-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 30 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer**, I want **a queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set**, so that **no document is attached wrongly and the models improve**.

Inside `rwb-document` this is the review-queue and review-completion capability of the document hub, and the same user story holds with the target service frame:

- Service `rwb-document`, schema `rwb_document`, REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.document.<Event>.v1`, Temporal task queue `rwb-document` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.document`.
- The queue, the item read, the item content, the resolve, the field patch and the review completion are six REST operations of this service on the one base `/api/recovery/document/v1` (12.1); the legacy field-patch path and the legacy document read of AC16 sat under the base `/api/recovery/v1` and are rebased by DP-13, keeping their operation, their shape and their message IDs.
- Every table this story reads or writes is in `rwb_document` (DP-01): `document_intake`, `document_text`, `document`, `document_field`, `document_type` and `document_hub_parameter`. The Ownership Map gives all six to P5; `recovery_case`, `recovery.*`, `document_hub_parameter` copies in another schema and every `recovery.*` view are gone.
- The review reasons, the review outcomes, the review statuses and the document types are reference data read through the reference-data contract of `rwb-case` (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON): LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE. No list value is typed in code.
- The case is resolved through the `rwb-case` case record contract (RWB-P3-E1035-CON, one hop, 2 s timeout, DP-11), never from a case table of another service and never from a `recovery_case` copy: `GET /api/recovery/case/v1/cases/{caseId}` for the status, the team and the owner, and the by-number read for a case number typed on the screen, whose path is the one RWB-P5-E1032-APP consumes and is Not specified in this key's source documents (GAP-1010; ASM-1808).
- Attach stores through the store of RWB-P5-E1024-APP in the same service, which stays the only writer of the `document` and `document_field` rows, of the DOCATT decision record and of the write-once container; this story writes `document_intake` and calls the store's published operation inside one transaction.
- The decision is recorded through the local decision-record library of DP-03 (H RWB-PLT-E1027-CON; the central ledger is P7's): the DOCATT record is written before the document exists, so a failed record leaves the item unchanged and answers MSG-P7-003 (R-UNI-39; X13).
- The extraction output the officer confirms or corrects is written by RWB-P5-E1053-CON in `document_field`; a type change re-runs extraction through the published extraction operation of RWB-P5-E1053-APP in the same service (ASM-1814).
- The resolved item is published as `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1` (the legacy EV-17), keyed by caseId, written to the outbox in the same transaction as the item update and the store row (DP-09, H RWB-PLT-TE006-CON). The store's `rwb.document.DocumentStored.v1` (EV-16) is published by the store for the same document, and this key adds no third event.
- The four review parameters `REVIEW_TEAM_UNATTACHED`, `REVIEW_DATE_MIN`, `REVIEW_DATE_MAX` and `REVIEW_PAGE_SIZE` are rows of `document_hub_parameter` in `rwb_document`, which the Ownership Map gives to P5, and this key reads them from its own table because the parameters contract of DP-06 is not claimed in its pattern list (ASM-1807).
- The two intake tables and the four review columns are created by this service's own per-service Flyway step in `rwb_document` (DP-15, H RWB-PLT-E1044-CON), and SCR-31 and SCR-30 reach the service through the gateway-bff composite route (DP-19, H RWB-PLT-N001-CON).
- The database login is one per service (DP-02). Its name is Not specified in the source documents (GAP-1010); this story uses the phrase "the rwb-document login (DP-02)" and never a shared login.
- The legacy package `recovery.dochub.review` and the legacy Java interfaces `LabeledSetReader`, `DocumentTypeCatalog`, `CaseDirectory`, `DocumentStore` and `FieldExtraction` are retired: the labeled example is read on the item read, the type list in force is read from `document_type` in `rwb_document`, the case from the P3 contract, the store from the same service and extraction from RWB-P5-E1053-APP (ASM-1811).
- The legacy feature flag `rwb.dochub.review` is replaced by `rwb.document.review` (ASM-1813).

The legacy behaviour is carried unchanged in intent and values: the same user story, rationale, preconditions, ten-step flow, thirteen exception paths, ten business rules, eleven messages, authority, data fields, seventeen acceptance criteria and nineteen test cases, adapted to the target service's schema, topic, API base, reference-data and case contracts and same-service calls.

### 2. Business rationale

A wrong type or a wrong hearing date on a court notice puts the wrong date on the case and the litigation timers run from it. This story shows in one queue every intake item the pipeline could not type, read or match, and every stored document with a field below its threshold; one officer confirms or corrects the type, the case and the fields on one screen, and each correction is kept as a labeled example for the model evaluations. It meets REQ-DCM-005 and moves the measure "fields extracted without review", because each correction improves the next model version. It also carries REQ-DCM-019: a discarded item is never removed silently — the file stays in the intake container and the reason and the person are recorded with it (BR9, AC12, AC13).

The realignment changes the mechanics, not the business rule:

1. One schema, one topic, one API base: `rwb_document`, `rwb.document.events.v1` and `/api/recovery/document/v1` (DP-01, DP-13). No table of another service is read and no `recovery.*` table name survives; the two legacy paths that carried `/api/recovery/v1` are rebased and keep their verbs.
2. The case is no longer read in process through `CaseDirectory`: it arrives through the `rwb-case` case record contract with a mock and a 2 s timeout (DP-11, C RWB-P3-E1035-CON), so the closed-case refusal of X5 and AC8 and the scope rule of BR2 are built on a published shape and its fake on Day 1.
3. The review reasons, outcomes, statuses and types arrive through the reference-data contract and the client library (DP-07, H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON), and the type list in force is the versioned `document_type` of this service (ASM-1810). The four review parameters are rows of this service's own `document_hub_parameter` (ASM-1807).
4. `DocumentStore` becomes the store's published operation of RWB-P5-E1024-APP, called inside the service (DP-11 in its same-service form), and the DOCATT entry becomes the local decision record of DP-03 written inside that transaction.
5. `ParameterCatalog`, `DocumentTypeCatalog` and the four new columns are created by the per-service Flyway sequence (DP-15), so the review-outcome columns and the two indexes land in `rwb_document` and in no other schema.
6. `DocumentFieldsExtracted` (EV-17) becomes `rwb.document.DocumentFieldsExtracted.v1` on the service topic, written to the outbox inside the transaction that sets the item outcome (DP-09), with no field value and no personal data in the payload.
7. `LabeledSetReader` is retired as a Java interface: the labeled example — predicted type, confirmed type, extracted value and corrected value — is answered by the item read of this service, so the evaluation path reads a published shape instead of an in-process call (ASM-1811).
8. SCR-31 and SCR-30 are served through the gateway-bff composite route (DP-19), which calls the owner once and merges the answer into the screen model.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E1054-CON | The published baseline of the seven review operations, the `ReviewItem`, `ReviewItemPage`, `IntakeItem`, `IntakeResolveRequest`, `IntakeResolution`, `Document`, `FieldReview`, `DocumentField` and `DocumentReviewRequest` shapes, the three actions, the two outcome values, the error envelope and the `Idempotency-Key` rule |
| RWB-P5-E1049-APP | The intake item base record, its source and received time, and `document_text` with the OCR pages the reviewer reads |
| RWB-P5-E1032-APP | The match outcome that holds an item in the queue — NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED and NO_TYPE — and the LOW_CONFIDENCE hold of a stored document with `review_status` PENDING |
| RWB-P5-E1050-CON | The classification output the queue shows: `predicted_type`, `classification_confidence`, `type_candidates`, `classifier_version` and `review_reason` |
| RWB-P5-E1053-CON | The extracted fields, their `extracted_value`, their `state` and the field list per type, including the four "GUARANTOR_NOTICE" fields of AC10 |
| RWB-PLT-E1027-CON | The decision-record library: the DOCATT record inside the caller's transaction, published on `rwb.decision-record.v1` (DP-03); the attach code is DOCATT and the actions and outcome keys are Not specified in the source documents (GAP-2456) |
| RWB-PLT-E1043-CON | The reference-data client library for LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE (DP-07) |
| RWB-PLT-TE006-CON | The outbox, inbox and idempotency library, so the item update, the store row and the event share one transaction (DP-09) |
| RWB-PLT-E1044-CON | The per-service Flyway sequence that carries the review-outcome migration as one step (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route that publishes the queue and the item panel to SCR-31 (DP-19) |
| RWB-P3-E1043-CON | `rwb-case`'s reference-data contract, which resolves the four lists (DP-07), the case review task code, element type and status values, Not specified in the source documents (GAP-0746) |
| RWB-P3-E1035-CON | `rwb-case`'s case record contract, which returns the case, its status, its team and its owner (DP-11) |

Business preconditions carried from RWB-E1-054, in the target wording:

- RWB-E1-049, RWB-E1-050, RWB-E1-053 and RWB-E1-032 are done: intake items carry review_reason (LOW_CONFIDENCE, UNKNOWN_TYPE, MODEL_UNAVAILABLE, RESCAN, UNREADABLE_FILE, EXTRACTION_FAILED, NO_MATCH, MULTIPLE, CONFLICT, CASE_CLOSED), candidates, candidate cases and extracted fields; stored documents carry review_status PENDING when a field is in REVIEW. In the target these are RWB-P5-E1049-APP, RWB-P5-E1050-CON, RWB-P5-E1053-CON and RWB-P5-E1032-APP in the same service.
- RWB-E1-024 is done: `DocumentStore.store` writes the document, its fields and the DOCATT decision log entry. In the target this is the store of RWB-P5-E1024-APP, called through its published operation, which writes the document, the fields, the write-once placement and the DOCATT record in one transaction.
- RWB-E1-035 shows documents on the case record view: in the target SCR-30 is served by the document list and read of RWB-P5-E1026-APP behind the gateway-bff composite route.
- Rows in document_hub_parameter: REVIEW_TEAM_UNATTACHED "DOC-SVC" (assumed), REVIEW_DATE_MIN 2000-01-01, REVIEW_DATE_MAX 2100-12-31, REVIEW_PAGE_SIZE 50. The rows are P5's own in `rwb_document` and are read by this story from its own table (ASM-1807) for its screen; the queue reads REVIEW_TEAM_UNATTACHED from the rwb-case row loaded through RWB-P3-E1043-CON, and its production value per environment is agreed by RW-COE and is Not specified in the source documents (GAP-0755; GAP-1010; ASM-1807).
- The officer holds RW-LITOFF (Documents CRU) with team scope. The role, the team and the scope are held as data in `rwb-access` and reach this service as the cached permission decision of the service template; this key's C list carries no `rwb-access` row and the story adds no guard of its own (ASM-1815); until a P4 row is added, the cached decision is the only source (GAP-1010).
- Feature flag `rwb.document.review` is on; it replaces the legacy `rwb.dochub.review` (ASM-1813).
- The store of RWB-P5-E1024-APP is reachable, the write-once container `rwb-docs-legal` accepts a legal type and the intake container `rwb-quarantine` still holds the file of a discarded item.
- The release date 30 November 2026 is the legacy one and is tentative (ASM-1806), and the story carries Status Draft (realignment v1) because no approval of the realigned story is recorded (ASM-1747).

The by-number case path is read through the case read published on RWB-P3-E1035-CON, the one path both P5 keys consume (GAP-1010). The field-level names of the seven operations' resources, the production value of the review team and the not-found message are Not specified in this key's source documents (GAP-1010; ASM-1808; ASM-1816); the baseline RWB-P5-E1054-CON fixes the names this story is built against.

### 4. Flow

1. Litigation officer: opens SCR-31 Document review queue through the gateway-bff composite route (DP-19).
2. System: lists, oldest first, the intake items with a review_reason and no case that belong to the officer's review team, the intake items whose candidate cases are in the officer's scope, and the stored documents with review_status PENDING on cases in scope; each row shows the reason, the proposed type, the two candidates, confidence and age. The queue read is `GET /api/recovery/document/v1/review-items`; the team of an item with no case comes from the REVIEW_TEAM_UNATTACHED row of `document_hub_parameter`, and the scope of an item with candidates comes from the `rwb-case` answer of the candidate cases and the officer's cached permission decision.
3. Litigation officer: opens an item (`GET /api/recovery/document/v1/intake-items/{intakeItemId}`); the system shows the file (`GET /intake-items/{intakeItemId}/content`), the OCR text of `document_text`, the type with its candidates, the candidate cases and the fields of `document_field`, with fields in state REVIEW marked and values masked by role.
4. Litigation officer: keeps the type or chooses another type from the list in force — the versioned `document_type` of this service, whose values are checked against LOV-DOC-TYPE; a new type re-runs extraction for that type through the published extraction operation of RWB-P5-E1053-APP and shows the new fields, each in state REVIEW (ASM-1814). The action travels as `POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve` with action SET_TYPE.
5. Litigation officer: chooses the case from the candidates, or enters a case number that the system looks up through the `rwb-case` case record contract, one hop with a 2 s timeout and a mock in the build (DP-11).
6. Litigation officer: confirms each marked field with Confirm, or enters the value with Correct (`PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId}`); the system checks it against the field data type and the range REVIEW_DATE_MIN to REVIEW_DATE_MAX and keeps the extracted value beside the corrected one.
7. Litigation officer: chooses Attach; the system calls the store of RWB-P5-E1024-APP with the case, the type and the fields, which writes the document, its fields and the DOCATT decision record, and stores a legal type in the write-once container `rwb-docs-legal`. The action travels as the resolve operation with action ATTACH.
8. System: sets the intake item review_outcome ATTACHED and the document review_status CONFIRMED (nothing changed) or CORRECTED (type, case or a value changed), and writes `rwb.document.DocumentFieldsExtracted.v1` to the outbox (EV-17). The item update, the store row, the decision record and the outbox row commit together or not at all.
9. Litigation officer: for a stored document with a field in REVIEW, confirms or corrects the field and completes the review with `POST /api/recovery/document/v1/documents/{documentId}/review` and action COMPLETE; the document review_status moves to CONFIRMED or CORRECTED.
10. Center of excellence analyst: the model evaluations (RWB-E1-060) read the resolved items as labeled examples through the item read of this service — predicted type, confirmed type, extracted value and corrected value — instead of the retired `LabeledSetReader` interface (ASM-1811).

The decision record is written before the document exists and inside the store transaction, so a failed record leaves the item, the document and the outbox unchanged and answers MSG-P7-003 (R-UNI-39; X13). The queue read itself is a GET with no side effect and no `Idempotency-Key`; the resolve (POST), the field correction (PATCH) and the review completion (POST) each carry an `Idempotency-Key`, and a repeat returns the first answer.

Screen states: SCR-31 shows the empty state of X9 and AC15; its loading, error and no-access states are Not specified in the source documents (DOR-RWB-P5-E1054-APP-10). SCR-30 has its empty, loading, error and no-access states Not specified in the source documents (DOR-RWB-P5-E1054-APP-10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Correct is chosen with an empty value | 422; nothing saved | MSG-GEN-001 | AC4 |
| X2 | The chosen type is not in the type list in force | 422; nothing saved | MSG-P5-006 | AC5 |
| X3 | A corrected date is outside the allowed range | 422; nothing saved | MSG-GEN-002 | AC6 |
| X4 | Attach or complete with a field still in REVIEW | 422; nothing stored | MSG-GEN-001 | AC7 |
| X5 | The chosen case is closed | 422; nothing stored | MSG-P5-005 | AC8 |
| X6 | Another officer saved the same item first | 409; the officer reloads | MSG-GEN-004 | AC9 |
| X7 | The same file is already on the chosen case | The item is linked to the existing document; no second document | MSG-P5-024 | AC11 |
| X8 | Discard without a reason | 422 | MSG-GEN-001 | AC13 |
| X9 | No item in the officer's queue | Empty state on SCR-31 | None | AC15 |
| X10 | A document outside the officer's scope | 404 | MSG-P4-003 | AC16 |
| X11 | The same confirmation is sent twice | Second call returns the saved field; nothing changes | None | AC17 |
| X12 | The user holds Documents R only | 403 | MSG-P4-002 | AC18 |
| X13 | The decision log write fails on attach | Nothing stored; item unchanged; incident raised | MSG-P7-003 | AC19 |

Four target-service notes:

- X1 to X9 and X11 are refusals of a body or of a version and keep their legacy statuses and message IDs unchanged; the RFC 9457 problem response carries `messageId`, `detail` and `instance`, and the status mapping is the legacy one (14).
- X10 is a 404 and not a 403 because a document outside the scope must not be distinguishable from a document that does not exist; the scope comes from the candidate cases of the `rwb-case` answer and the officer's cached permission decision, and MSG-P4-003 is returned by the document read of RWB-P5-E1024-APP, which this story calls and does not change (ASM-1815).
- X12 is enforced before the body is read, at the resolve and the review POST and at the field patch, with MSG-P4-002 naming the action; the officer's role and its rights are data in `rwb-access` and this story inherits the shape (ASM-1815).
- X13 is the store's local decision record of DP-03 inside one transaction: the record, the `document` row, the `document_field` rows, the `document_intake` update and the outbox row commit together or not at all, and a failure answers 503 with MSG-P7-003 and raises the incident of R-UNI-39 (ASM-1812).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the intake item and its text (RWB-P5-E1049-APP), the match hold (RWB-P5-E1032-APP), the classification output (RWB-P5-E1050-CON), the extracted fields (RWB-P5-E1053-CON), the case contract (RWB-P3-E1035-CON), the reference-data library and contract, the decision-record library, the outbox library, the Flyway sequence and the gateway route, all earlier or contract work |
| Negotiable | The review team, the date limits and the page size are data rows; the type list is the versioned `document_type`; the layout follows the ACE components (DL31); the shapes come from the contract baseline |
| Valuable | No low-confidence or unmatched document reaches a case without a person checking it, and every correction becomes a labeled example |
| Estimable | Six operations, three services, one queue service, one review service, one migration, one screen with two components |
| Small | Fits in two weeks with its tests |
| Testable | Each criterion below is one test case in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents

  Background:
    Given DOCTYPE-2026.11 is in force and the classify_threshold of every type is 0.8000
    Given REVIEW_TEAM_UNATTACHED is "LIT-BKK" for this test
    Given a litigation officer with role RW-LITOFF in team "LIT-BKK" with team scope
    Given the rwb-access contract mock returns role RW-LITOFF in team "LIT-BKK" with Documents CRU and team scope
    Given the rwb-case contract mock returns case "RW-2026-000201" open, of team "LIT-BKK" and in the officer's scope
    Given the rwb-case contract mock returns case "RW-2026-000202" open, of team "LIT-BKK" and in the officer's scope
    Given the rwb-case contract mock returns case "RW-2026-000203" open, of team "LIT-BKK" and in the officer's scope
    Given the rwb-case contract mock returns case "RW-2026-000150" with status "Closed"
    Given the rwb-decision contract mock returns the central ledger reference for decision code "DOCATT"

  Scenario: AC1 Queued (legacy RWB-E1-054 AC1)
    Given intake item "IN-0101" on which classification returned "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100
    Given its review_reason is "LOW_CONFIDENCE"
    When the officer opens SCR-31
    Then the system lists "IN-0101" with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21"

  Scenario: AC2 Corrected (legacy RWB-E1-054 AC2)
    Given intake item "IN-0101" in the review queue with hearing_date "2026-12-15" in state "REVIEW"
    When the officer sets type "COURT_NOTICE", corrects hearing_date to "2026-12-16", confirms the other fields, chooses case "RW-2026-000201" and chooses Attach
    Then the system stores a document on "RW-2026-000201" with type "COURT_NOTICE" and hearing_date field_value "2026-12-16", extracted_value "2026-12-15", state "CORRECTED" and confirmed_by the officer's user ID
    Then the document review_status is "CORRECTED" and "IN-0101" has review_outcome "ATTACHED"
    Then the store writes one DOCATT decision log entry
    Then LabeledSetReader returns "IN-0101" with predicted type, confirmed type, extracted value and corrected value

  Scenario: AC3 A stored document with a field to check (legacy RWB-E1-054 AC3)
    Given document "DOC-0103" on case "RW-2026-000202" has black_case_no "Por 2001/2569" in state "REVIEW" and review_status "PENDING"
    When the officer chooses Confirm on black_case_no and completes the review
    Then black_case_no has state "CONFIRMED" and confirmed_by the officer's user ID
    Then the document review_status is "CONFIRMED"

  Scenario: AC4 An empty correction is refused (legacy RWB-E1-054 AC4)
    Given document "DOC-0103" has court_name in state "REVIEW"
    When the officer chooses Correct on court_name with an empty value
    Then the response is 422 with MSG-GEN-001 naming "Court name"
    Then court_name is unchanged

  Scenario: AC5 A type not in the list is refused (legacy RWB-E1-054 AC5)
    Given intake item "IN-0104" in the review queue
    When the officer sets the type to "PAYSLIP"
    Then the response is 422 with MSG-P5-006 naming "PAYSLIP"

  Scenario: AC6 A date outside the allowed range is refused (legacy RWB-E1-054 AC6)
    Given REVIEW_DATE_MIN is 2000-01-01 and REVIEW_DATE_MAX is 2100-12-31
    When the officer corrects hearing_date on "IN-0101" to "2569-12-16"
    Then the response is 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31"

  Scenario: AC7 Attach with a field still in review is refused (legacy RWB-E1-054 AC7)
    Given intake item "IN-0105" has two fields in state "REVIEW" and the officer has confirmed one
    When the officer chooses Attach
    Then the response is 422 with MSG-GEN-001 naming the field still in review
    Then the system stores no document

  Scenario: AC8 A closed case is refused (legacy RWB-E1-054 AC8)
    Given intake item "IN-0106" with review_reason "CASE_CLOSED" and candidate case "RW-2026-000150" with status "Closed"
    When the officer chooses case "RW-2026-000150" and chooses Attach
    Then the response is 422 with MSG-P5-005 naming "RW-2026-000150"
    Then the system stores no document

  Scenario: AC9 Two officers on the same item (legacy RWB-E1-054 AC9)
    Given two officers opened intake item "IN-0107" at version 3
    Given the first officer attached it, so the item is at version 4
    When the second officer chooses Attach with version 3
    Then the response is 409 with MSG-GEN-004
    Then one document exists for "IN-0107"

  Scenario: AC10 A type change re-runs extraction for the new type (legacy RWB-E1-054 AC10)
    Given intake item "IN-0108" was classified "DEMAND_LETTER" with five extracted fields
    Given the rwb-document contract mock returns the four "GUARANTOR_NOTICE" fields of "IN-0108", each in state "REVIEW"
    When the officer sets the type to "GUARANTOR_NOTICE"
    Then extraction runs for "GUARANTOR_NOTICE" and the item shows its four fields, each in state "REVIEW"
    Then the DEMAND_LETTER fields are no longer offered

  Scenario: AC11 The file is already on the chosen case (legacy RWB-E1-054 AC11)
    Given document "DOC-0109" on case "RW-2026-000203" holds a file with hash "H109"
    Given intake item "IN-0109" holds the same file
    When the officer attaches "IN-0109" to "RW-2026-000203"
    Then the system stores no second document and "IN-0109" is linked to "DOC-0109"
    Then the screen shows MSG-P5-024 naming "DOC-0109"

  Scenario: AC12 Discard an unreadable item (legacy RWB-E1-054 AC12)
    Given intake item "IN-0110" with review_reason "UNREADABLE_FILE"
    When the officer chooses Discard with reason "Blank page from the branch scanner"
    Then "IN-0110" has review_outcome "DISCARDED" with the reason, the officer's user ID and the time
    Then it leaves the queue and no document is stored

  Scenario: AC13 Discard without a reason is refused (legacy RWB-E1-054 AC13)
    Given intake item "IN-0112" with review_reason "RESCAN"
    When the officer chooses Discard with an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "IN-0112" stays in the queue

  Scenario: AC14 The queue lists items in scope, oldest first (legacy RWB-E1-054 AC14)
    Given 3 review items for team "LIT-BKK" received on 2 November, 4 November and 3 November
    Given 2 review items of team "HP-NE"
    When the officer opens SCR-31
    Then 3 items show, in the order 2 November, 3 November, 4 November
    Then no item of team "HP-NE" shows

  Scenario: AC15 An empty queue (legacy RWB-E1-054 AC15)
    Given no review item for team "LIT-BKK"
    When the officer opens SCR-31
    Then the screen shows the empty state "No documents are waiting for review."

  Scenario: AC16 A document outside the officer's scope (legacy RWB-E1-054 AC16)
    Given document "DOC-0111" belongs to a case of team "HP-NE"
    Given the rwb-case contract mock returns that the case of "DOC-0111" is of team "HP-NE"
    When the officer calls GET /api/recovery/document/v1/documents/DOC-0111
    Then the response is 404 with MSG-P4-003

  Scenario: AC17 The same confirmation sent twice (legacy RWB-E1-054 AC17)
    Given the officer confirmed black_case_no on "DOC-0103"
    When the same PATCH with confirmed true and the same value arrives again
    Then the response is 200 with the saved field
    Then confirmed_by and updated_at are unchanged

  Scenario: AC18 A user without Documents U is refused (X12) (new, D-RCV-60)
    Given a team manager with role RW-TEAMMGR in team "LIT-BKK" with Documents R
    Given intake item "IN-0101" in the review queue
    When the team manager calls POST /api/recovery/document/v1/intake-items/IN-0101/resolve with action SET_TYPE
    Then the response is 403 with MSG-P4-002 naming "SET_TYPE"
    Then "IN-0101" is unchanged

  Scenario: AC19 The decision log write fails on attach (X13) (new, D-RCV-60)
    Given intake item "IN-0101" with type "COURT_NOTICE" and the officer has confirmed its fields
    Given the decision log write fails
    When the officer chooses Attach
    Then the response carries MSG-P7-003 with a status code Not specified in the source documents (X13)
    Then the system stores no document, "IN-0101" is unchanged and an incident is raised

  Scenario: AC20 A call without a session or with Documents R only is refused with 401 or 403 (new, D-RCV-60)
    Given the officer's session token is missing
    When the officer calls GET /api/recovery/document/v1/review-items
    Then the response is 401
    Given a team manager with role RW-TEAMMGR in team "LIT-BKK" with Documents R only
    When the team manager calls POST /api/recovery/document/v1/intake-items/IN-0101/resolve with action SET_TYPE
    Then the response is 403

  Scenario: AC21 A retried or timed-out attach does not store twice (new, D-RCV-60)
    Given the attach of intake item "IN-0107" times out after the document is stored
    When the officer retries the attach with the same item version
    Then the system stores no second document
    Then the retry returns the stored document

  Scenario: AC22 A consumed call that fails or does not answer stores nothing (new, D-RCV-60)
    Given the rwb-case contract mock does not answer for case "RW-2026-000201"
    When the officer chooses case "RW-2026-000201" and chooses Attach for intake item "IN-0101"
    Then the system stores no document
    Then "IN-0101" is unchanged
```

Every Given, When and Then line above is the legacy line unchanged. The only added lines are AC18 to AC22 for the exception, access and resilience paths X12, X13 and the consumed-call failure, the six Background mocks on the `rwb-access` and `rwb-case` contracts and the `rwb-decision` contract, the extraction mock of AC10 and the case mock of AC16, and the one rebased path: AC16's legacy document read under the base `/api/recovery/v1` is published as `GET /api/recovery/document/v1/documents/DOC-0111` by DP-13, with the same operation, the same 404 and the same MSG-P4-003. The legacy interfaces and paths map to the target as `GET /review-items` → `GET /api/recovery/document/v1/review-items`, `GET /intake-items/{id}` → `GET /api/recovery/document/v1/intake-items/{intakeItemId}`, `POST /intake-items/{id}/resolve` → `POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve`, the legacy field patch under the base `/api/recovery/v1` → `PATCH /api/recovery/document/v1/documents/{documentId}/fields/{fieldId}`, `POST /documents/{documentId}/review` → `POST /api/recovery/document/v1/documents/{documentId}/review`, and `LabeledSetReader` → the item read, which answers the labeled example of AC2 with the predicted type, the confirmed type, the extracted value and the corrected value (ASM-1811).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The queue holds intake items with a review_reason and no outcome, and documents with review_status PENDING | RWB-E1-049, RWB-E1-050, RWB-E1-053, RWB-E1-032; LOV-REVIEW |
| BR2 | An item with no case is shown to the review team named in REVIEW_TEAM_UNATTACHED and to roles with scope All; an item with candidate cases and a document are shown by case scope | Permission matrix scope; CTL-09; REVIEW_TEAM_UNATTACHED (DOC-SVC assumed) |
| BR3 | Attach and complete are allowed only when no field is in REVIEW, the type is in force and the case is open | LOV-REVIEW; DocumentTypeCatalog; DF-CAS-005 |
| BR4 | review_status becomes CONFIRMED when type, case and values are kept, CORRECTED when any changes | LOV-REVIEW |
| BR5 | A corrected value keeps the extracted value in extracted_value and the corrector in confirmed_by | DF-DOC-017; FEAT-DCM-11 |
| BR6 | Attach stores through DocumentStore, which writes the DOCATT decision log entry first and places a legal type in the write-once container | RWB-E1-024; Principle 5; CTL-12 |
| BR7 | Each resolved item is a labeled example for the model evaluations | FEAT-AGT-04; FEAT-DCM-11 |
| BR8 | A change saved against an old version is refused | Optimistic lock column version; MSG-GEN-004 |
| BR9 | A discarded item keeps its file in the intake container and records the reason and the person | REQ-DCM-019 (never removed silently) |
| BR10 | Field values are masked unless the role may see them | DF-DOC-015; CTL-11; DL26 |

Target-service statements that make the rules hold in `rwb-document`:

- BR1 is executed by the queue query over `document_intake` and `document` in `rwb_document`: `review_reason IS NOT NULL AND review_outcome IS NULL` for the item half, and `review_status = 'PENDING'` for the document half, both oldest first by `received_at` and `created_at` and both filtered by BR2 before the page is cut (index `ix_intake_review`, index `ix_document_review`).
- BR2 is executed in two steps. The scope of an item with candidates and of a stored document comes from the `rwb-case` answer of the case and the officer's cached permission decision, which this story reads and does not build (ASM-1815); the review team of an item with no case comes from the REVIEW_TEAM_UNATTACHED row, and a role with scope All sees every item with no candidate. The parameter is a row of `document_hub_parameter` in `rwb_document` and no team code is typed in code (ASM-1807).
- BR3 is executed before the store is called: the resolve operation rejects a type outside the versioned `document_type` (MSG-P5-006), a field still in state REVIEW (MSG-GEN-001), and a closed case read through the `rwb-case` case record contract (MSG-P5-005).
- BR4 is executed by comparing the submitted type, case and field values with the stored ones at the moment of the store call, and by writing CORRECTED when any of the three differs and CONFIRMED when none does.
- BR5 is executed by the field patch: the corrected value goes to `field_value`, the extracted value stays in `extracted_value`, the caller goes to `confirmed_by` and the row increments `version`.
- BR6 is executed by the store operation of RWB-P5-E1024-APP: the DOCATT record of DP-03 is written inside the same transaction as the `document` row, the `document_field` rows, the write-once placement in `rwb-docs-legal` and the outbox row, so a failed record leaves nothing behind (R-UNI-39; ASM-1812).
- BR7 is executed by answering the labeled example on the item read and by publishing `rwb.document.DocumentFieldsExtracted.v1` for the resolved item; the evaluation path of RWB-E1-060 is P10's and this story only exposes the shape.
- BR8 is executed by the optimistic lock on `document_intake.version` for the resolve and on `document_field.version` and the `If-Match` document version for the field patch; a stale version answers 409 with MSG-GEN-004.
- BR9 is executed by the discard action: `review_outcome` DISCARDED, `discard_reason`, `resolved_by` and `resolved_at` are written, the file stays in `rwb-quarantine` and the content read still returns it; nothing is deleted.
- BR10 is executed by the masking the service applies to a `document_field` value and to a page of `document_text` before the answer leaves the service, by role; the masking rule is `rwb-access` data (DF-DOC-015, DL26) and every read of the item is written to the PII access log by the ACE common module, never by this package.
- DP-01 keeps every read in `rwb_document`; DP-07 keeps the four lists out of the code; DP-09 puts the event in the outbox inside the transaction; DP-15 puts the migration in the per-service sequence; DP-19 puts the two screens behind the gateway-bff composite route.

### 9. State transitions

None for the case. This story does not change a case status. It sets document_intake.review_outcome (ATTACHED or DISCARDED), document.review_status (PENDING to CONFIRMED or CORRECTED) and document_field.state (REVIEW to CONFIRMED or CORRECTED).

| From | Event | Condition | To |
|---|---|---|---|
| Intake item with review_reason | Attach | BR3 passes; store succeeds | review_outcome ATTACHED |
| Intake item with review_reason | Discard | Reason given | review_outcome DISCARDED |
| document.review_status PENDING | Review completed | Nothing changed | CONFIRMED |
| document.review_status PENDING | Review completed | A value changed | CORRECTED |

| From (`document_field.state`) | Event | Condition | To |
|---|---|---|---|
| REVIEW | Confirm | The value is kept and the row version matches | CONFIRMED |
| REVIEW | Correct | A new value passes the type and range check and the row version matches | CORRECTED |
| CONFIRMED or CORRECTED | The same confirmation arrives again | Same value, same flag, same version | CONFIRMED or CORRECTED, unchanged with 200 |

The intake states are the field values of `review_outcome` and of `review_status` and not a workflow: an item that is attached or discarded leaves the queue for good, and a document whose review is completed stops being PENDING. An item in any held state is not selected by the queue query of BR1 again, and an item whose store call failed on the decision record stays in the queue untouched (X13). The document state machine COPY_PENDING to STORED belongs to RWB-P5-E1024-APP and is not changed by this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Lists, reads, corrects, attaches and discards review items in scope (Documents CRU) |
| RW-CASEOWN, case owner | Lists, reads, corrects and attaches review items of own cases (Documents CRU) |
| RW-TEAMMGR, team manager | Reads the queue for the team (Documents R); cannot correct or attach |
| SY-OCR, OCR and extraction pipeline | Re-runs extraction on a type change (Documents CRU) |
| SY-DECLOG, decision log writer | Writes the DOCATT entry through DocumentStore |
| RW-COE, center of excellence analyst | Reads the labeled examples through the model evaluations (Documents R) |

Every "who" in this table is a **role code** held as data in `rwb-access` (P4): roles as data, scope and masking policy are P4's and reach this service as the cached permission decision of the service template. This story adds no guard of its own and inherits the 403 shapes of MSG-P4-002 and the 404 shape of MSG-P4-003; its C list carries no `rwb-access` row, which is recorded in ASM-1815. Each REST operation of this story calls the authorise check of `rwb-access` (DP-08) before the body is read. SY-DECLOG is the local decision-record library of DP-03 in the target, called by the store inside the caller's transaction, and it publishes the DOCATT record on `rwb.decision-record.v1`. SY-OCR is the extraction operation of RWB-P5-E1053-APP in the same service. The worker runs as the rwb-document service identity (DP-02), carried by the chart as a secret reference; the login name is Not specified in the source documents (GAP-1010).

### 11. Data

| BR Field ID | Table in `rwb_document` | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | `rwb-case` case, through the contract | case_no | Read |
| DF-CAS-005 | `rwb-case` case, through the contract | status | Read |
| DF-DOC-001 to DF-DOC-011 | `document`, through the store of RWB-P5-E1024-APP | all fields | Write, through the store |
| DF-DOC-008 | `document` | review_status | Write, through the store |
| DF-DOC-015 | `document_field` | field_value | Write |
| DF-DOC-017 | `document_field` | confirmed_by | Write |
| DF-DOC-034 | `document_field` | extracted_value | Read |
| Standard column | `document_field` | state, version | Write |
| DF-DOC-080 | `document_intake` | review_reason | Read |
| DF-DOC-070 | `document_intake` | predicted_type | Read |
| DF-DOC-072 | `document_intake` | type_candidates | Read |
| DF-DOC-076 | `document_intake` | candidate_case_ids | Read |
| DF-DOC-077 | `document_intake` | extracted_fields | Read |
| DF-DOC-081 | `document_intake` | review_outcome | Write |
| DF-DOC-082 | `document_intake` | resolved_by | Write |
| DF-DOC-083 | `document_intake` | resolved_at | Write |
| DF-DOC-084 | `document_intake` | discard_reason | Write |
| DF-DOC-089 | `document_text` | text_content | Read |
| DF-DOC-088 | `document_text` | page_no | Read |
| DF-REF-244 to DF-REF-250 | `document_hub_parameter` | the four review parameter rows | Read |
| (document type) | `document_type` | type code, version in force, field list | Read |
| (decision record) | decision-record library table in `rwb_document` | chain_seq, inputsRef, ruleId, finalCall, decidedAt, prev_hash, entry_hash | Write, through the library |
| (outbox) | outbox library table in `rwb_document` | the row for `rwb.document.DocumentFieldsExtracted.v1` | Write, through the library |

Field IDs are those in the Logical Data Model and Data Dictionary and the TSD P5 T3.1 table. No `recovery_case` row is copied and no ACE view is read by this service: DF-CAS-002 and DF-CAS-005 arrive inside the `rwb-case` case record answer, and DP-01 forbids a foreign-schema read. The intake columns DF-DOC-070 to DF-DOC-084 come from RWB-P5-E1050-CON, RWB-P5-E1053-CON and RWB-P5-E1032-APP, and this story adds no new intake column except the four it writes. Personal data never enters the event payload, the outbox row or the log: field values and OCR text are masked by role on the screen and are never logged; a log line carries the intake item ID or the document ID, the action, the outcome and the version, never a value, a text page, a file name or an account number in clear.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-document (P5); base `/api/recovery/document/v1`; the shapes are those of RWB-P5-E1054-CON.

| Method | Path | Owner | Notes |
|---|---|---|---|
| GET | `/api/recovery/document/v1/review-items` | P5 | The review queue of SCR-31 (legacy `GET /review-items`, API-P5-010): query `kind` (INTAKE, DOCUMENT or ALL, default ALL), `reason`, `page`, `size` (default the REVIEW_PAGE_SIZE row, 50); answer 200 `ReviewItemPage`, oldest first, filtered by BR2 before the page is cut; Documents R, scope applied; no `Idempotency-Key` |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}` | P5 | One held item as `IntakeItem` (API-P5-011): source, received time, review reason, predicted type, the type candidates, the candidate cases with their status, the OCR text pages, the extracted fields masked by role, the review outcome and the version; each read written to the PII access log |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}/content` | P5 | The file of the held item as `application/octet-stream` (API-P5-012), read from `rwb-quarantine` through the storage product; a discarded item still answers with its file (BR9) |
| POST | `/api/recovery/document/v1/intake-items/{intakeItemId}/resolve` | P5 | Set the type, attach the item to a case in scope with confirmed fields, or discard it with a reason (API-P5-013): request `IntakeResolveRequest` with action SET_TYPE, ATTACH or DISCARD; answer 200 `IntakeResolution` carrying the item and, for ATTACH, the stored `Document`; Documents U, scope applied; `Idempotency-Key` required; `version` in the body is the optimistic lock |
| PATCH | `/api/recovery/document/v1/documents/{documentId}/fields/{fieldId}` | P5 | Confirm or correct one field of a stored document (the legacy field patch under the base `/api/recovery/v1`, rebased by DP-13; API-P5-006): request `FieldReview` with `value` (required when `confirmed` is false) and `confirmed`, header `If-Match` with the document version; answer 200 `DocumentField`; a repeat with the same value and flag answers 200 and changes nothing (AC17) |
| POST | `/api/recovery/document/v1/documents/{documentId}/review` | P5 | Complete the review of a stored document with action COMPLETE (API-P5-014): request `DocumentReviewRequest` with `action` and `version`; answer 200 `Document` with the final review_status; 422 with MSG-GEN-001 when a field is still in REVIEW; Documents U |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5, owned by the document read of RWB-P5-E1024-APP | The document, its type, its fields with state and values, its review_status and its version, behind AC16's 404 with MSG-P4-003 and the drill-down after an attach; this story declares it for the baseline and changes none of its fields |

The seven operations are the ones RWB-ITG-E1054-ITG consumes, and the six of this key's own are declared in RWB-P5-E1054-CON. The legacy `/review-queue` name of the controller and the `DocumentHubController` split of the legacy section 13 are not published: one controller serves the queue and one the item, and the field patch keeps its own operation (ASM-1808). The 404 of X10 belongs to the document read and is inherited, not reimplemented.

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | RWB-P3-E1035-CON | The case, its status, its team and its owner, for the closed-case refusal of X5 and AC8 and the scope filter of BR2; one hop, 2 s timeout, breaker per downstream, one GET retry with jitter (DP-11) |
| GET | `/api/recovery/case/v1/cases/by-no/{caseNo}` | P3 rwb-case | RWB-P3-E1035-CON | The case the officer types on the screen in step 5; the same owner document, one hop and 2 s; the path is the one RWB-P5-E1032-APP consumes and this key's sources do not restate it (GAP-1010; ASM-1808) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | RWB-P3-E1043-CON | LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE (DP-07), cached for 5 minutes |

The other calls are inside the service and are not contracts of another service: the store operation of RWB-P5-E1024-APP writes the `document` and `document_field` rows, the write-once placement and the DOCATT record of one attach; the extraction operation of RWB-P5-E1053-APP re-runs the extraction of a new type in AC10; and the document read of RWB-P5-E1024-APP answers the drill-down and AC16. They appear in 12.9 as REST consumed inside the service. A failed case read maps to 503 with MSG-GEN-006 naming the system that failed and leaves the item untouched; it never becomes a 404 and never a silent pass.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload |
|---|---|---|---|---|
| `rwb.document.DocumentFieldsExtracted.v1` (the legacy DocumentFieldsExtracted, EV-17) | `rwb.document.events.v1`, with the retry topics at 1 min, 10 min and 1 h and the `.dlt` topic | P5 | caseId | documentId, confidence, fields |
| decision record (DOCATT) | `rwb.decision-record.v1` | PLT library, consumed by P7 | caseId | the hash-chained record with decision code DOCATT, the confirmed or corrected type, the item ID as `inputsRef` and the reviewer's user ID where a person decided |

CloudEvents 1.0 envelope, binary mode; no personal data, no field value and no OCR text in either payload. The event and the record are written to the outbox inside the store transaction, so they exist exactly when the document row, the field rows and the item update exist. `rwb.document.DocumentStored.v1` (EV-16) is published by the store of RWB-P5-E1024-APP for the same document and is not re-declared here; this key adds no third event to the two the catalogue gives `rwb-document` (Arch v5 slides 16 and 42).

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| None | — | — | The queue is read on demand and the item enters it when RWB-P5-E1050-CON and RWB-P5-E1053-CON set `review_reason` and the field states in `rwb_document`; no event starts this story. The classification event Arch v5 slide 16 gives `rwb-document` (`AgentRunCompleted`) is consumed by the classification path of RWB-P5-E1050-APP, not here |

#### 12.5 Workflows and activities

| Name | Kind | Queue | Note |
|---|---|---|---|
| None in this story | — | — | The queue, the item read, the resolve, the field patch and the review completion are synchronous operations with no durable step. The items of the queue are produced by `DocumentIntakeWorkflow` of RWB-P5-E1049-APP and by the `matchStep` activity of RWB-P5-E1032-APP, and this story neither registers nor signals a workflow |

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| None | — | — | — | The legacy story has no job and no timer; the person opens the queue. No Temporal Schedule is registered, changed or retired by this story |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `document_intake` | P5 | Read for the queue and the item panel; written with `review_outcome`, `resolved_by`, `resolved_at` and `discard_reason`; `version` is the optimistic lock of the resolve |
| `document_text` | P5 | Read only: the OCR pages the officer reads, masked by role |
| `document` | P5 | Read for the queue half, the review completion and AC16; written only through the store of RWB-P5-E1024-APP, never by this story directly |
| `document_field` | P5 | Read and written for the confirm, the correct and the review completion: `field_value`, `confirmed_by`, `state`, `version` |
| `document_type` | P5 | Read only: the type list in force and the field list of a type for the re-run of AC10 |
| `document_hub_parameter` | P5 | Read only: the four review parameter rows, since DP-06 is not claimed by this key (ASM-1807) |
| decision-record library table | PLT library, created in `rwb_document` | The DOCATT record, in the store transaction |
| outbox, inbox and idempotency library tables | PLT library, created in `rwb_document` | The `DocumentFieldsExtracted` row; the `Idempotency-Key` rows of the resolve and the review completion |

No foreign-schema table is read (DP-01) and no ACE view is read by this service. `recovery_case`, `case_account` and `lov_value` are P3's and arrive only inside the two contracts.

Personal data: the `document_text` pages and the `document_field` values that this service reads and writes are personal data and are masked by role (section 4, step 3).

#### 12.8 Contract fakes

| Fake | Story | Used for |
|---|---|---|
| review-queue baseline fake | RWB-P5-E1054-CON | The seven operations and the nine shapes, so the tests build before the app code lands |
| rwb-case case fake (`GET /cases/{caseId}` and `GET /cases/by-no/{caseNo}`) | RWB-P3-E1035-CON | The open cases "RW-2026-000201", "RW-2026-000202" and "RW-2026-000203", the closed case "RW-2026-000150", the absent case of AC16's team and the 2 s timeout path |
| rwb-access session fake | the cached permission decision of the service template | RW-LITOFF with Documents CRU and team scope, RW-CASEOWN with own cases only, and RW-TEAMMGR with Documents R only for TC-E1-054-18 |
| reference-data fake | RWB-P3-E1043-CON (through RWB-PLT-E1043-CON) | LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE, including the two outcome values ATTACHED and DISCARDED |
| decision-record fake | RWB-PLT-E1027-CON | The local DOCATT record, and a refusing write for TC-E1-054-19 |
| central ledger fake | P7 rwb-decision | The collection of the record into the central ledger |
| store fake or stub | RWB-P5-E1024-APP | The `Document` answer, the duplicate link of AC11 and the COPY_PENDING state |
| extraction fake | RWB-P5-E1053-APP | The four "GUARANTOR_NOTICE" fields of AC10 and the five "DEMAND_LETTER" fields they replace |
| classifier fake | RWB-P5-E1050-CON | The 0.6200 and 0.2100 candidates of AC1 and the review reasons of the Background |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 7, consumed 2 cross-service plus 3 in-service | The queue, the item read, the content read, the resolve, the field patch, the review completion and the document read; the case read by ID and by number; the reference-data read; inside the service the store, the extraction re-run and the document read |
| Kafka | Published 1 event and 1 decision record; consumed 0 | `rwb.document.DocumentFieldsExtracted.v1` on `rwb.document.events.v1` and the DOCATT record on `rwb.decision-record.v1` |
| Temporal | 0 | No workflow, no activity and no Schedule belongs to this story; the queue is filled by RWB-P5-E1049-APP and RWB-P5-E1032-APP |
| File | The held file and the stored file | The held file is read from `rwb-quarantine` through the storage product; the store writes the file to `rwb-docs-legal` for a legal type and keeps a non-legal type out of the write-once container |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.document`, module `review`; front end folder `recovery/documents`. The legacy Java package `recovery.dochub.review` is retired.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ReviewQueueController | Controller | `GET /review-items`, the item read and the content read, with the scope filter, the masking and the RFC 9457 error mapping |
| ReviewQueueService | Service | Builds the queue and the item answer with the scope rule of BR2 and the oldest-first order of BR1 |
| ReviewResolutionService | Service | SET_TYPE, ATTACH and DISCARD on an item: BR3 to BR9, the type check against `document_type`, the case check through the contract, the store call and the item update |
| FieldReviewService | Service | Confirm and correct one field: the empty-value check, the type and range check of `REVIEW_DATE_MIN` to `REVIEW_DATE_MAX`, the `If-Match` document version and the idempotent repeat of AC17 |
| DocumentReviewService | Service | Completes the review with action COMPLETE and sets `review_status` CONFIRMED or CORRECTED |
| LabeledExampleProjection | Read model | Answers the labeled example on the item read — predicted type, confirmed type, extracted value and corrected value — in place of the retired `LabeledSetReader` |
| ReviewQueueRepository | Repository | Reads and writes `document_intake` and `document_field`, reads `document`, `document_text`, `document_type` and `document_hub_parameter`; `version` is the optimistic lock |
| ReviewQueuePage | React component | The SCR-31 list, the filters, the paging and the empty state |
| ReviewItemPanel | React component | The file and OCR text viewer, the type chooser with candidates, the case chooser, the fields with Confirm and Correct, Attach and Discard |

**Database.**

- One migration in the per-service Flyway sequence (DP-15): `V1054_1__review_outcome.sql` adds to `document_intake` `review_outcome` varchar(12), `resolved_by` uuid, `resolved_at` timestamptz and `discard_reason` varchar(400); the classification, extraction and match columns come from the migrations of RWB-P5-E1050-CON, RWB-P5-E1053-CON and RWB-P5-E1032-APP.
- Index `ix_intake_review ON document_intake (received_at) WHERE review_reason IS NOT NULL AND review_outcome IS NULL`; index `ix_document_review ON document (review_status, Not specified in the source documents (CG-ALL-6009)) WHERE review_status = 'PENDING'`. Both are partial, so the queue query of BR1 never scans a resolved row.

**Configuration and reference data.**

- `document_hub_parameter` rows REVIEW_TEAM_UNATTACHED "DOC-SVC" (assumed), REVIEW_DATE_MIN 2000-01-01, REVIEW_DATE_MAX 2100-12-31 and REVIEW_PAGE_SIZE 50, loaded by the reference data administrator and read from this service's own table (ASM-1807); the production value of the review team is Not specified in the source documents (GAP-1010).
- DOCTYPE version in force through the versioned `document_type` of this service (RWB-E1-025; DL19), and the type codes checked against LOV-DOC-TYPE (DP-07). No type code is typed in code.
- Reference lists LOV-INTAKE-REVIEW, LOV-INTAKE-OUTCOME, LOV-REVIEW and LOV-DOC-TYPE read through the reference-data contract (DP-07, ASM-1809).
- Decision code DOCATT, assumed, with the LOV-DECISION list loaded by the data steward.
- Feature flag `rwb.document.review` (ASM-1813). Off: SCR-31 is hidden and review items stay in the queue untouched, exactly as the legacy flag states.

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

DP-01 moves the six tables the legacy story reads and writes into `rwb_document` and stops the module reaching into the recovery schema: `document_intake`, `document_text`, `document`, `document_field`, `document_type` and `document_hub_parameter` are all P5's, and the case is never a local copy. DP-03 replaces `DecisionLogWriter` and the `DocumentStore`-internal write with the local decision-record library, so the DOCATT record, the document row, the field rows, the item update and the outbox row share one transaction and the record is published on the shared topic. DP-07 keeps the review reasons, the two outcome values, the four review statuses and the type codes out of the code through the client library and the `rwb-case` contract. DP-09 puts `rwb.document.DocumentFieldsExtracted.v1` in the outbox inside the same transaction and fixes the CloudEvents envelope and the retry and `.dlt` topics. DP-11 is the two case reads: in-process `CaseDirectory` becomes one hop on a published shape with a fake in the build and a 2 s timeout; the same-service calls to the store, the extraction and the document read keep the one-hop rule without a contract of another service. DP-13 rebases the two legacy paths that carried `/api/recovery/v1` — the field patch of legacy section 12 and the document read of AC16 — onto `/api/recovery/document/v1`, with no change of verb, shape or message. DP-15 puts the four review columns and the two partial indexes in the service's own Flyway sequence. DP-19 puts the queue and the item panel behind the gateway-bff composite route, so SCR-31 calls the owner once and the screen model merges the case and reference answers.

**Build steps**

1. Write the migration and the indexes; test that the held index returns only unresolved items, that the document index returns only PENDING documents and that the optimistic lock refuses a stale `version`.
2. Build `ReviewQueueService` with the scope rule of BR2 and the oldest-first order; test AC14 and AC15 and the two scope halves of AC1 and AC14.
3. Build the item read and the content read with masking and the PII access log; test AC1, AC16 and the access test TC-E1-054-18.
4. Build SET_TYPE with the type check and the extraction re-run through RWB-P5-E1053-APP; test AC5 and AC10.
5. Build the field confirm and correct with the empty-value check, the range check and the `If-Match` version; test AC3, AC4, AC6, AC9 and AC17.
6. Build ATTACH through the store with BR3, the duplicate link and the outcome; test AC2, AC7, AC8, AC11 and the decision-record failure TC-E1-054-19.
7. Build DISCARD and `LabeledExampleProjection`; test AC12, AC13 and the labeled example of AC2.
8. Build `ReviewQueuePage` and `ReviewItemPanel` on SCR-31 with the Loading, List, Reviewed and Empty states; browser tests (RWB-TE-010).

**Done when.** The tests in section 16 pass, the seventeen legacy criteria hold on synthetic data, SCR-31 passes the browser and accessibility tests of RWB-TE-010, and no review item leaves the queue without one of the two outcome values, one store row and — for an attach — one DOCATT record and one `DocumentFieldsExtracted` event.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-003 | An item or document is in the review queue | Some fields need checking. The document is in the review queue. |
| MSG-P5-005 | The chosen case is closed (new) | Case {case} is closed. Choose an open case. |
| MSG-P5-006 | The chosen type is not in force (new) | {value} is not a document type in force. Choose a type from the list. |
| MSG-P5-024 | The file is already on the case | This file is already on the case as {document}. |
| MSG-GEN-001 | Empty value, empty reason, or field still in review | Enter {field}. |
| MSG-GEN-002 | Date outside the allowed range | {field} must be between {min} and {max}. |
| MSG-GEN-004 | Saved against an old version | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-005 | Field, attach or discard saved | Saved. |
| MSG-P7-003 | Decision log write failed on attach | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Caller lacks Documents U | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Item or document outside the caller's scope | This case is not in your scope. |
| MSG-P4-001 | No authenticated caller | Not specified in the source documents (GAP-1010; ASM-1816) |
| MSG-GEN-006 | A consumed read failed or timed out | Not specified in the source documents (GAP-1010; ASM-1816) |
| not-found message | An intake item or a document that does not exist | Not specified in the source documents (GAP-1010; ASM-1816) |

Thai text for each message follows decision DL10.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The HTTP mapping is the legacy one and is fixed by AC4 to AC13 and the baseline RWB-P5-E1054-CON: 401 for MSG-P4-001, 403 for MSG-P4-002, 404 for MSG-P4-003 and for an item or a document that does not exist, 409 for MSG-GEN-004, 422 for MSG-GEN-001, MSG-GEN-002, MSG-P5-005 and MSG-P5-006, and 503 for MSG-P7-003 and MSG-GEN-006. MSG-P5-003 is not an error response: it is the label of a held item on SCR-31. MSG-GEN-005 is the confirmation of a saved action and not an error. The three platform rows — MSG-P4-001, MSG-GEN-006 and the not-found message — are named by the target error envelope and their exact texts are Not specified in this key's source documents, so they carry the placeholder above.

### 15. Screens and states

| Screen | State | What the user does |
|---|---|---|
| SCR-31 Document review queue | Loading | Skeleton rows while the queue loads through the gateway-bff composite route |
| SCR-31 Document review queue | List | Sees review items oldest first with reason, candidates, confidence and age; opens one; sets type and case, confirms or corrects fields, attaches or discards |
| SCR-31 Document review queue | Item detail | Sees the file, the OCR text masked by role, the type with its candidates and confidence, the candidate cases with their status, and the fields with the ones in REVIEW marked; a type change re-runs extraction and replaces the field list |
| SCR-31 Document review queue | Refused | An empty correction answers MSG-GEN-001, a type outside the list MSG-P5-006, a date outside the range MSG-GEN-002, a field still in REVIEW MSG-GEN-001, a closed case MSG-P5-005, a stale version MSG-GEN-004 and a role without Documents U MSG-P4-002; nothing is saved and the item keeps its state |
| SCR-31 Document review queue | Reviewed | After attach, discard or complete the item leaves the list and MSG-GEN-005 shows |
| SCR-31 Document review queue | Empty | Sees "No documents are waiting for review." |
| SCR-31 Document review queue | Error | Not specified in the source documents (CG-ALL-6027) |
| SCR-31 Document review queue | No access | Not specified in the source documents (CG-ALL-6027) |
| SCR-30 Case documents | List | Sees the attached document with its confirmed or corrected type and fields |
| SCR-30 Case documents | Loading | Not specified in the source documents (CG-ALL-6026) |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-6026) |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-6026) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-6026) |

The queue and the item panel are reached through the gateway-bff composite route (DP-19), which calls this service once for the queue and once for the item and merges the case answer for the drill-down. The case document list on SCR-30 is RWB-P5-E1026-APP and the release work that hides SCR-31 behind the flag is this story's. The route specification and the screen field list beyond the legacy section 15 are Not specified in the source documents (GAP-1010; ASM-1808).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-054-18 | AC18, Access (legacy), BR2, BR10 | Component | RW-TEAMMGR user (Documents R) calls POST /api/recovery/document/v1/intake-items/{intakeItemId}/resolve; refused with 403 and MSG-P4-002 |
| TC-E1-054-19 | AC19, Principle 5 (legacy), BR6, X13 | NFR | Decision log write forced to fail on Attach; no document, item unchanged, MSG-P7-003, incident raised |
| TC-E1-054-01 | AC1, BR1 | End to end | Intake item classified at 0.62 with two candidates |
| TC-E1-054-02 | AC2, BR4, BR5, BR6, BR7 | End to end | Hearing date corrected; synthetic case RW-2026-000201 |
| TC-E1-054-03 | AC3, BR4 | End to end | Stored document with one field in review |
| TC-E1-054-04 | AC4 | End to end | Empty correction |
| TC-E1-054-05 | AC5, BR3 | End to end | Type PAYSLIP not in force |
| TC-E1-054-06 | AC6 | End to end | Date 2569-12-16 entered as a Gregorian year |
| TC-E1-054-07 | AC7, BR3 | End to end | Two fields in review, one confirmed |
| TC-E1-054-08 | AC8, BR3 | End to end | Candidate case with status Closed |
| TC-E1-054-09 | AC9, BR8 | End to end | Two sessions on one item version |
| TC-E1-054-10 | AC10 | End to end | Demand letter changed to guarantor notice |
| TC-E1-054-11 | AC11 | End to end | Same file hash already on the case |
| TC-E1-054-12 | AC12, BR9 | End to end | Unreadable item discarded with a reason |
| TC-E1-054-13 | AC13 | End to end | Discard with an empty reason |
| TC-E1-054-14 | AC14, BR2 | End to end | Five review items across two teams |
| TC-E1-054-15 | AC15 | End to end | No review item for team LIT-BKK |
| TC-E1-054-16 | AC16, BR10 | End to end | Document of team HP-NE |
| TC-E1-054-17 | AC17 | End to end | Same PATCH sent twice |
| TC-E1-054-20 | Contract (operations, events and activities of §12) | Component | Operations, events and activities of §12 checked against RWB-P5-E1054-CON |
| TC-E1-054-21 | Boundary (tables of §12.7, ASM-3438) | Component | Rows of each table of §12.7 at the boundary of each column |
| TC-E1-054-22 | AC20, Access (legacy), BR2 | Component | Call without a session answers 401; RW-TEAMMGR with Documents R only calls POST resolve and is refused with 403 |
| TC-E1-054-23 | AC21, Resilience (legacy) | NFR | Attach retried after a timeout on the same item version; no second document, retry returns the stored document |
| TC-E1-054-24 | AC22 | Component | rwb-case contract mock does not answer for the chosen case; Attach stores nothing and the item is unchanged |

The legacy level System maps to End to end, Access to Component and Resilience to NFR; the nineteen legacy test cases are kept in the order of the legacy story. The wave-1 integration harness copies TC-E1-054-01 as TC-E1-054-01-ITG, TC-E1-054-19 as TC-E1-054-19-ITG and the rest of the sixteen in the same form, and they belong to RWB-ITG-E1054-ITG, where the real `rwb-case`, `rwb-access` and `rwb-decision` replace the fakes. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the review team, the date limits and the page size are rows of `document_hub_parameter`; the reasons, outcomes, statuses and types are reference data read through DP-07 and the versioned `document_type` of this service.
- No personal data in logs, tests or prompts: field values and OCR text are masked by role and never logged; a log line carries the item or document ID, the action, the outcome and the version; test data is synthetic.
- No read of another module's tables: the case is resolved through the `rwb-case` contract, one hop with a 2 s timeout, and no `v_ace_*` view and no `recovery.*` table is read by this service (DP-01, DP-11).
- Attach goes only through the store of RWB-P5-E1024-APP, so a document never exists without its DOCATT record and a legal type never reaches the write-once container without the record first.
- The decision record is written in the same transaction as the document, the fields, the item update and the outbox row; a failure stores nothing and raises the incident of R-UNI-39.
- A discarded item is never removed: the file stays in `rwb-quarantine`, the reason and the person are kept, and the content read still answers (REQ-DCM-019).
- The queue and the item read are GETs with no side effect and no `Idempotency-Key`; the resolve and the review completion are POSTs with the header, and the field patch is idempotent on the same value and flag.
- No field value and no OCR text enters the event payload or the decision record; the payload carries the item ID, the document ID, the type, the field count and the review status.
- The feature flag `rwb.document.review` removes the queue from the screen without a rollback of the schema.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-01 to TC-E1-054-21 |
| REQ-DCM-019 | A discarded document is never removed silently; the reason and the person are kept with the file | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-054-12, TC-E1-054-13 |

| Legacy reference | Where it is kept |
|---|---|
| DocumentFieldsExtracted (EV-17) through DocumentStore | Sections 1, 4, 8, 12.3, 17 |
| MSG-P5-003, MSG-P5-005, MSG-P5-006, MSG-P5-024, MSG-GEN-001, MSG-GEN-002, MSG-GEN-004, MSG-GEN-005, MSG-P7-003, MSG-P4-002, MSG-P4-003 | Section 14 and the exception paths |
| Parameters REVIEW_TEAM_UNATTACHED, REVIEW_DATE_MIN, REVIEW_DATE_MAX, REVIEW_PAGE_SIZE | Background, sections 3, 8, 13 |
| Rules R-UNI-39, R-UNI-40, CTL-09, CTL-11, CTL-12, DL10, DL11, DL19, DL26, DL31 | Sections 2, 8, 14, 17, 18 |
| Containers `rwb-quarantine` and `rwb-docs-legal`, the write-once placement | Sections 3, 4, 8, 12.9, 13 |
| Interfaces LabeledSetReader, DocumentTypeCatalog, CaseDirectory, DocumentStore, FieldExtraction | Sections 1, 4, 8, 13; retired for the item read, `document_type`, the P3 contract, the store and RWB-P5-E1053-APP |
| Legacy key RWB-E1-054, AC1 to AC17, TC-E1-054-01 to TC-E1-054-19 | Metadata, section 7, section 16 |

| Decision or pattern | Where it sits in this story |
|---|---|
| DP-01 | Six tables in `rwb_document`; the case consumed and never copied |
| DP-03 | The DOCATT record inside the store transaction and the ledger fake |
| DP-07 | The four lists through the reference-data contract and the versioned `document_type` |
| DP-09 | The `DocumentFieldsExtracted` outbox row, the topic and the CloudEvents envelope |
| DP-11 | The two case reads, one hop, 2 s, with a fake |
| DP-13 | The field patch and the AC16 document read rebased onto `/api/recovery/document/v1` |
| DP-15 | The review-outcome migration and the two partial indexes |
| DP-19 | SCR-31 and SCR-30 behind the gateway-bff composite route |
| ADR-013 | The service owns its schema inside ACE PostgreSQL |
| ADR-014 | The `rwb_document` schema and the rwb-document login |
| ADR-020 | Contract-first REST, one hop, 2 s timeout |
| ADR-021 | Per-service Flyway and migration ownership |
| DL31 | Open decision with no assumption yet; assumption Not specified in the source documents (DOR-RWB-P5-E1054-APP-18) |

The legacy key is RWB-E1-054; its AC1 to AC17 are owned by this story, its contract baseline is RWB-P5-E1054-CON, and the cross-service proof of the same values is RWB-ITG-E1054-ITG.

### 19. Out of scope

- The published contract baseline, its resources, its error mapping, its event schema, its fakes and its drift test (RWB-P5-E1054-CON).
- The document store, the `document` and `document_field` rows, the write-once container and the DOCATT record (RWB-P5-E1024-APP).
- Setting the review reasons: OCR (RWB-P5-E1049-APP), classification (RWB-P5-E1050-APP), extraction (RWB-P5-E1053-APP) and matching (RWB-P5-E1032-APP).
- The model evaluations that read the labeled examples (RWB-E1-060, P10); this story exposes the labeled example on the item read and calls nothing of P10.
- Assigning review work to named people by queue rules (RWB-E2-011).
- The case checklist on the review screen (RWB-E1-040, and the checklist read of this service).
- The generation and signature of documents, the field app capture and the retention and legal hold of a document (RWB-P5-E2017-APP, RWB-P5-E2024-APP, RWB-P5-AD021-APP).
- The compute, storage, topic and ACL provisioning of this service, the chart, the Schedule registration, the dashboards, the alerts and the runbook, which this key does not raise as a separate story.
- The parameters and reference-data catalogues themselves and their admin operations (P3 rwb-case) and the role, scope and masking data (P4 rwb-access).
- The cross-service proof of these values (RWB-ITG-E1054-ITG).
