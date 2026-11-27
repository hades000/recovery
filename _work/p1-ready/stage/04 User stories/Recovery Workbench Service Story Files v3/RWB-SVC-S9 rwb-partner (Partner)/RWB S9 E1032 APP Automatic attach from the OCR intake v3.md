# RWB-S9-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: legacy RWB-E1-032 is split for the partner service. The primary slice, the match and attach of a classified intake item, stays in `rwb-document` as RWB-P5-E1032-APP with its contract RWB-P5-E1032-CON and owns AC1 to AC15. This story is the secondary slice, the partner-origin file channel of the same intake: the submission row and its partner reference in `rwb_partner`, the case hint the matcher resolves, the accept record, the attach state read back from rwb-document, the reconcile Schedule and the read on SCR-35, on `/api/recovery/partner/v1`. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (32 resolved, 44 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S9-E1032-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 1 (contract-only slice: partner identity and partner document path published in wave 1; the rest in wave 4 per Arch v5 slide 41; wave-map conflicts GAP-3139 and GAP-3174 kept per R5.6, one conflict row per service and business epic; the rwb-partner service wave governs the later stories) |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S9-E1032-APP-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Platform H rows (GAP-3140) | H empty for this slice. The seven platform rows of DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19 (RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON) are the shared baseline of wave 0, not H; revisit if one is not published before the wave 1 entry check |
| Parallel lane | L-S9-B |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1032-CON; RWB-S9-E1032-CON |
| Contract version | v1 of RWB-S9-E1032-CON, path /api/recovery/partner/v1; frame per GAP-3137 |
| Integration dependencies | None |
| External dependencies | None |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S9-E1032-APP-14); confirm with the epic design record |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to REQ-DCM-007, REQ-DRI-004, REQ-DCM-005) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6.


### 1. Story

As a **partner portal user of an instructed firm (PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC)**, I want **the file I submit on my instruction to reach the OCR intake carrying the case its instruction names, and to show its attach state on the instruction**, so that **no partner file is filed by hand when the firm and the instruction are clear, and none is filed on a case the firm was not instructed on**.

This is the secondary slice of legacy RWB-E1-032 (FEAT-DCM-12). The legacy story names partner files as one of the three sources that arrive without a case link. The case owner, the reviewer, the matcher and the store are the primary slice's; this story owns the partner side of the same attach, a boundary no source states and this story fixes (GAP-3138; ASM-5504), and **owns no legacy AC**: AC1 to AC15 and TC-E1-032-01 to TC-E1-032-17 stay with RWB-P5-E1032-APP, which is where the case is matched, the document is stored and the reviewer resolves a held item (GAP-3144; ASM-5510).

In the target frame the service is `rwb-partner`, schema `rwb_partner`, REST base `/api/recovery/partner/v1`, topic `rwb.partner.events.v1` with the retry and `.dlt` topics of the platform convention and event names `rwb.partner.<Event>.v1`, Temporal task queue `rwb-partner` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.partner` (Template and Rules R4; GAP-3137; ASM-5503). It builds:

- the submission `POST /partner/instructions/{instructionId}/documents` on the service base (DP-13) and the read `GET /partner/instructions/{instructionId}/documents`, behind the partner gateway for partners and the gateway-bff composite route for staff (DP-19);
- the row `partner_intake` in `rwb_partner` (DP-01) with its own Flyway step (DP-15), holding the firm, the instruction, the document type, the file SHA-256, the case ID of the instruction, the state and the intake item ID;
- one local decision record per accepted file in the same transaction (DP-03), so an accepted partner file exists only with the record that proves the acceptance;
- the fact `rwb.partner.PartnerDocumentSubmitted.v1` on `rwb.partner.events.v1`, written to the outbox in that transaction and keyed on the case ID (DP-09), so the document hub's matcher receives the case the instruction names and the partner source;
- the consumption of `rwb.document.DocumentAttached.v1` and the read of `GET /api/recovery/document/v1/intake-items/{intakeItemId}` of RWB-P5-E1032-CON (DP-11), so the submission closes with the document ID or carries the held match outcome back to the partner;
- the reconcile Schedule `partner-intake-reconcile` on queue `rwb-partner` in the legacy JOB-12 cadence (DP-10);
- the document type list and the intake bound as reference data and parameter, never as code (DP-06, DP-07).

The file, the OCR, the classification, the extraction, the match, the case, the account and the document row are not this service's (section 19).

### 2. Business rationale

Scans, partner files and emails arrive without a case link; today a person reads each one and files it (legacy RWB-E1-032 section 2). A partner file is the one source whose party knows, at the moment of sending, which instruction and therefore which case it belongs to, and that knowledge is the only thing the partner service can add to the intake: the firm, the instruction and its case ID. Without it the matcher has to read the case out of the OCR text alone, and a partner file whose instruction is clear is held as if it were an anonymous scan.

Architecture v5 moves that fact once and in one direction. The partner reaches the partner gateway (FAPI 2.0) that fronts S9, so the submission is a REST operation on the service base; the case and the document live in other services, so the partner service sends the case hint as a fact on `rwb.partner.events.v1` and reads the outcome back through the published contract of the document hub, one hop with a 2 s budget. It writes no document row, no intake item, no case row and stores no file.

The one rule that must hold is that an accepted partner file exists only with its record (principle 5; R-UNI-39). The submission row, the local record and the outbox row are one `rwb_partner` transaction; if the record cannot be written nothing happens and the partner sees MSG-P7-003. The second rule is that a file is submitted once (R-UNI-40): the write key on the instruction and the file hash, with the `Idempotency-Key` on the operation, make the repeat return the first answer.

No business value is invented. The states are the legacy match states (`PENDING`, `MATCHED`, `NO_MATCH`, `MULTIPLE`, `CONFLICT`, `CASE_CLOSED`, `NO_TYPE`); the types are the legacy document types of the LOV; the hold rule is legacy BR3 and the record rule is legacy BR5. The requirement rows are REQ-DCM-007 (a classified document attaches without a person), REQ-DCM-005 (a document that cannot be matched goes to a person) and REQ-DRI-004 (the attached record), read for their partner half.

### 3. Preconditions

- `RWB-P5-E1032-CON` is published: the IntakeItem shape, the item read `GET /intake-items/{intakeItemId}`, the five match outcomes, the error envelope and the `Idempotency-Key` rule. The contract dependency never blocks the build (§R5.4, §R5.7); the partner service builds against the published shape and its fake on Day 1.
- The document-hub operation that creates an intake item for a partner file is reachable; The exact path and shape are Not specified in the source documents (GAP-3141; ASM-5507). The four operations RWB-P5-E1032-CON publishes are the resolve, the list, the item read and the content read, and the creation is outside them.
- `rwb_partner` and its login exist, and the service's own Flyway sequence is at the version that carries the library tables; this story adds the next version of the service's own sequence, Not specified in the source documents (CG-ALL-11744), and never edits an applied migration.
- `partner`, `partner_user`, `partner_instruction` exist with the columns of the S9 module tables (DF-PRT-001 to DF-PRT-016, DF-REF-212 to DF-REF-217), and the instruction carries `case_id`, `partner_id`, `instruction_type`, `due_at` and `status`.
- A partner instruction of type `COLLECT` on a case sits with the firm in status `SENT`, `ACCEPTED` or `IN_PROGRESS`, so a file may be submitted on it.
- The partner user reaches the service through the partner gateway, holds Partner portal C, and the instruction belongs to the user's own firm (NFR-050).
- The reference lists LOV-DOC-TYPE and LOV-INSTR-STATUS are in force at their version and the intake bound parameter is in force; no source names the bound or the parameter row this service reads (GAP-3142; ASM-5508).
- The decision code of the acceptance and the version in force are read as values at their version; which code and version the record names is Not specified in the source documents (GAP-3142; ASM-5508).
- MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-GEN-006 are unchanged from FSD and the legacy story.
- The ACE account number resolves to `account_key` through a rwb-source-data operation Not specified in the source documents (GAP-0743); the query form is agreed with rwb-source-data in its contract story before integration (GAP-0743).
- No approval stop: FSD S9 and TSD S9 are not approved in this run and the story is Draft (realignment v1) (ASM-5512).
- Wave 1 is the W-MAP wave of EP01 and is earlier than the Arch v5 wave 4 of rwb-partner; the W-MAP wave is kept as R5.6 requires and the release date is copied unchanged and marked tentative (GAP-3139; ASM-5505).

### 4. Flow

1. The partner user, on the partner portal screen of the instruction, submits a file with its document type on `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/documents`, behind the partner gateway.
2. The guard library resolves the identity and the right; a role without Partner portal C is refused before any read (MSG-P4-002).
3. The service reads `partner_instruction`, `partner` and `partner_user` in `rwb_partner` and checks that the instruction belongs to the firm of the partner user (404 otherwise, disclosing nothing).
4. It checks the state: a file is accepted only from `SENT`, `ACCEPTED` or `IN_PROGRESS`; `DONE`, `DECLINED` and `RECALLED` answer 409 and change nothing (X1).
5. It validates the submission: a file present, a `documentType` in LOV-DOC-TYPE, the body within the intake bound; a missing or refused element answers 422 with MSG-GEN-001 and the field (X2).
6. It computes the SHA-256 of the file, takes the case ID of the instruction as the case hint, and assembles the record naming the case, the document and the event ID only, until the decision code is agreed (GAP-0747).
7. In one `rwb_partner` transaction: the `partner_intake` row is written with state `PENDING`, the firm, the instruction, the type, the hash and the case ID; the record is written through `DecisionRecordWriter.record`; the outbox row is written (DP-03, DP-09).
8. If the record write refuses, nothing at all is written and the answer is MSG-P7-003 (AC6, X3).
9. After the commit the service calls the document hub's intake creation with the file reference, the partner source and the case ID, one hop with a 2 s timeout and a breaker (DP-11; the path is GAP-3141); a failure leaves the row `PENDING` and the reconcile run retries it (X4).
10. The relay publishes `rwb.partner.PartnerDocumentSubmitted.v1` on `rwb.partner.events.v1` keyed on the case ID; the document hub's matcher resolves the case, stores the document and publishes `rwb.document.DocumentAttached.v1` (that journey is RWB-P5-E1032-APP's).
11. On the attach event the service matches the submission by its intake item ID and sets `MATCHED` with the document ID, and signals `documentAttached` to `PartnerInstructionWorkflow` (AC2).
12. The reconcile Schedule runs every 15 minutes in business hours over the rows still `PENDING`: it reads `GET /api/recovery/document/v1/intake-items/{intakeItemId}` and copies the match state and the candidate case IDs onto the row; a held value is shown to the partner read only, and the item is resolved by a person holding Documents C in rwb-document (AC3).
13. The submission list and its states reach the partner portal and SCR-35 through the composite route, one hop; no screen writes (DP-19).
14. The same `Idempotency-Key` and the same hash under the same instruction return the first answer and write no second row and no second event (AC4).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The instruction is `DONE`, `DECLINED` or `RECALLED`, or belongs to another firm | 409 for a closed instruction, 404 for a foreign firm; nothing written, nothing called | MSG-GEN-001 for the closed case is Not specified in the source documents (GAP-3141; ASM-5507) | AC5 |
| X2 | A required element is missing or the body exceeds the intake bound | The whole submission is refused; no row, no record, no event, no intake call | MSG-GEN-001 | AC5 |
| X3 | The local decision record cannot be written | Nothing is written: no row, no event, no intake call | MSG-P7-003 | AC6 |
| X4 | The intake creation misses the 2 s budget or its breaker is open | The row stays `PENDING`; the reconcile run retries with jitter; the partner is told it is queued | MSG-GEN-006 | AC8 |
| X5 | The same file and the same `Idempotency-Key` are submitted twice | The first answer returns, the repeat is counted, one row and one event exist | None | AC4 |
| X6 | The attach outcome never arrives and the item is held | The reconcile run copies the held match state and the candidates; this service attaches nothing; no decision record and no DOCATT entry is written for a held item, and the hold stays a status on the intake item in rwb-document | MSG-P5-003 to the partner, read only | AC3 |
| X7 | A component or test reaches a document, intake, case or ledger table | The grant refuses and the boundary test fails the build | None (pipeline log) | AC9 |

X1 to X6 are this slice's paths; X7 is the inherited boundary rule. The legacy X1 to X12 (no match, two candidates, conflict, a case that does not exist, a closed case, a duplicate file, a repeat run, low confidence, no type, a reviewer outside scope, a type not in force, two reviewers at once) are the matcher's and the reviewer's and stay with RWB-P5-E1032-APP; this slice receives their outcome as a state and never decides it.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 with no H row and one C row; the document hub is a mock and the case arrives inside the instruction |
| Negotiable | The operation path, the activity names, the intake bound and the write key are this story's design choice; the states, the types and the messages are fixed |
| Valuable | A partner file that names its instruction is attached without a person and is never filed on a case the firm was not instructed on |
| Estimable | One operation, one read, one migration, one record adapter, one event in and one out, one Schedule, one screen fragment |
| Small | Fits two weeks with its tests, as the secondary slice of one legacy key |
| Testable | Each of the seven criteria of section 7 is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake — the partner file channel

  Background:
    Given partner instruction of type "COLLECT" on case "RW-2026-000123" for firm "TEST-PT-001" and account "TEST-ACC-0001", in status "ACCEPTED"
    Given the partner user holds Partner portal C and the instruction belongs to the user's own firm
    Given the lists LOV-DOC-TYPE and LOV-INSTR-STATUS are in force at their version and the intake bound parameter is in force
    Given the rwb-document contract mock returns intake item "TI-0001" with match_status "PENDING" for the submission of case "RW-2026-000123"

  Scenario: AC1 A partner file on an open instruction is recorded and announced (new, D-RCV-60)
    Given the partner user submits a file of type "APPRAISAL_REPORT" with SHA-256 "H1" on the instruction
    When the submission operation validates it and writes the transaction
    Then partner_intake holds one row with state "PENDING", the firm ID, the instruction ID, type "APPRAISAL_REPORT", hash "H1" and case_id "RW-2026-000123"
    Then exactly one local decision record is written in the same transaction, naming the case, the document and the event ID only, until the decision code is agreed (GAP-0747)
    Then exactly one PartnerDocumentSubmitted event is written to the outbox in that transaction, keyed on the case ID
    Then the event carries the submission ID, the instruction ID, the case ID, the document type and the hash, and no personal data and no file content
    Then the document hub intake is called once with the file reference, the partner source and case "RW-2026-000123", and the row records the intake item ID it answers
    Then this service writes no document row, no intake item, no case row and stores no file

  Scenario: AC2 The attach outcome closes the submission (new, D-RCV-60)
    Given the submission of AC1 holds state "PENDING" with intake item "TI-0001"
    Given the rwb-document contract mock returns the attach event for "TI-0001" on case "RW-2026-000123" with document "DOC-0001"
    When the attach event is consumed
    Then partner_intake holds state "MATCHED" and document_id "DOC-0001"
    Then PartnerInstructionWorkflow receives the documentAttached signal once
    Then a second delivery of the same event changes no column and writes no second record

  Scenario: AC3 A held file is copied to the partner side and attached by no one here (new, D-RCV-60)
    Given the rwb-document contract mock returns intake item "TI-0002" with match_status "MULTIPLE" and candidate cases "RW-2026-000321" and "RW-2026-000654"
    When the reconcile run reads the item
    Then partner_intake holds state "MULTIPLE" and both candidate case IDs
    Then this service attaches nothing, stores no file and writes no document row
    Then the partner portal and SCR-35 show state "MULTIPLE" with both candidate cases, read only
    Then the item is resolved by a person holding Documents C in rwb-document, and the next run copies state "MATCHED" and the document ID

  Scenario: AC4 The same file under the same instruction writes one submission (new, D-RCV-60)
    Given the submission of AC1 is complete
    When the partner user submits the same file with the same SHA-256 "H1" on the same instruction with the same Idempotency-Key
    Then the first answer is returned and the repeat is counted
    Then partner_intake holds one row for hash "H1" and the instruction
    Then rwb.partner.events.v1 holds one event for it

  Scenario: AC5 A submission that cannot be accepted writes nothing (new, D-RCV-60)
    Given an instruction in status "DONE", an instruction of another firm and a submission with no document type
    When the partner user submits on each
    Then the closed instruction answers 409 and the foreign instruction 404
    Then the submission without a type answers 422 with MSG-GEN-001
    Then a role without Partner portal C answers 403 with MSG-P4-002
    Then no partner_intake row, no decision record and no event is written, and the intake is not called

  Scenario: AC6 A refused record leaves no trace (new, D-RCV-60)
    Given the decision record cannot be written
    When the partner user submits a file on an open instruction
    Then the answer is 503 with MSG-P7-003
    Then no partner_intake row and no outbox row exists
    Then the document hub intake is not called

  Scenario: AC7 The submission and its attach state read on SCR-35 (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-35 Placement and allocation
    Given the instruction holds two submissions, one "MATCHED" and one "MULTIPLE"
    When a case owner holding Partner portal R opens SCR-35 for the case
    Then SCR-35 lists both submissions with their type, received time and state, read only
    Then the browser calls no owner service directly and no screen writes anything

  Scenario: AC8 An intake creation that misses its budget leaves the submission queued (new, D-RCV-60)
    Given the intake creation of the submission of AC1 misses the 2 s budget or its breaker is open
    When the partner user submits a file on an open instruction
    Then the row stays in state PENDING and the partner is told the submission is queued with MSG-GEN-006
    Then the reconcile run retries the intake call once with jitter, and no second row or event is written

  Scenario: AC9 A component that reaches a document, intake, case or ledger table is refused (new, D-RCV-60)
    Given a component of this service reaches the document, document_intake, recovery_case or task table
    When the boundary test runs
    Then the grant refuses the access and the boundary test fails the build, with the pipeline log as the only record

  Scenario: AC10 A contract read or call that misses the 2 s budget changes nothing and is retried once with jitter (new, D-RCV-60)
    Given a contract read or call of this service misses the 2 s budget
    When the call times out
    Then no column changes and no record, row or event is written, and the call is retried once with jitter

  Scenario: AC11 A call to a provided operation without valid credentials answers 401 (new, D-RCV-60)
    Given the caller holds no valid credentials
    When the caller calls the submission operation of /api/recovery/partner/v1
    Then the answer is 401, and no partner_intake row, decision record or event is written

  Scenario: AC12 A redelivered consumed event changes no state (new, D-RCV-60)
    Given the attach event for "TI-0001" on case "RW-2026-000123" has been consumed once
    When the same attach event is redelivered
    Then partner_intake holds state "MATCHED" unchanged, PartnerInstructionWorkflow receives no second documentAttached signal, and no row is added to the inbox or outbox

```

AC1 to AC12 are new under D-RCV-60 and test only the rwb-partner deliverable of the title. No legacy criterion is restated: the fifteen legacy criteria of RWB-E1-032 stay word for word with RWB-P5-E1032-APP (GAP-3144; ASM-5510). Every value above is a legacy value (case, account, types, states, messages, the JOB-12 cadence) or test data.

Screen states (DOR-RWB-S9-E1032-APP-10): on SCR-35 the empty state is Not specified in the source documents (DOR-RWB-S9-E1032-APP-10), the loading state shows while the submission list is read, the error state shows on a failed read with a message Not specified in the source documents (DOR-RWB-S9-E1032-APP-10), and the no-access state is the refusal, before any read, of a role without Partner portal R. SCR-30 and SCR-31 are named in the readiness item but are not screens of this story; their empty, loading, error and no-access states are Not specified in the source documents (DOR-RWB-S9-E1032-APP-10).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A partner file is accepted on an instruction of the user's own firm that is not closed; a closed instruction and a foreign instruction write nothing | legacy RWB-E1-032 sections 3 and 5; NFR-050 |
| BR2 | The case hint of a partner file is the `case_id` of its instruction; this service resolves no case by itself and reads no account | legacy BR2 (the case is found by the case read); DP-01 |
| BR3 | No match, more than one candidate, a disagreement, a closed case or no agreed type goes to a person, and the person resolves it in rwb-document | legacy BR3; REQ-DCM-005 |
| BR4 | A partner file is accepted only with a document type in force and within the intake bound, both read at their version | legacy BR1 and BR4; DP-06, DP-07 |
| BR5 | Each acceptance is written to the record before the row, the event and the intake call exist; a failed record means nothing happens | legacy BR5; principle 5; R-UNI-39 |
| BR6 | A contract read or call that misses the 2 s budget changes nothing and is retried once with jitter | ADR-020; legacy X13 |
| BR7 | A file submitted once under one instruction is not submitted again: one hash, one row, one event | legacy BR6; R-UNI-40 |
| BR8 | The partner sees the state of its own submission only, and read only; the item detail and the resolve are rwb-document's | legacy BR7; CTL-09 |
| BR9 | A submission carries identifiers, codes, a hash and dates only; no personal data and no file content reach the row, the record, the event or the log | legacy guardrails; Architecture v5 slide 22 |

BR1 is the firm and state check of steps 3 and 4; BR2 is the case hint of step 6; BR3 is the held states of step 12 and X6; BR4 is the validation of step 5; BR5 is `recordPartnerDocument` and the rollback of X3; BR6 is the retry of X4; BR7 is the write key and the `Idempotency-Key` of AC4; BR8 is the access of 12.1; BR9 is the payload rule of 12.3.

### 9. State transitions

The case status is rwb-case's and is not moved here. The document state machine is rwb-document's. The rows below are the states of a partner submission, and they are the legacy match states, copied and not extended.

| From (`partner_intake.state`) | Event | Condition | To |
|---|---|---|---|
| (none) | Submission accepted | Validation passes, the record and the outbox row commit | `PENDING` |
| (none) | Submission refused | A closed instruction, a foreign firm, a refused element or an unrecordable acceptance | No row (`X1`, `X2`, `X3`) |
| `PENDING` | Attach event for its intake item | The document hub stored the document | `MATCHED`, `document_id` set |
| `PENDING` | Reconcile run reads the item | The item holds `NO_MATCH`, `MULTIPLE`, `CONFLICT`, `CASE_CLOSED` or `NO_TYPE` | The same value, with the candidate case IDs |
| `PENDING` | Reconcile run reads the item | The item is still `PENDING` or the read fails | `PENDING`; retried by the next run |
| `NO_MATCH`, `MULTIPLE`, `CONFLICT`, `CASE_CLOSED`, `NO_TYPE` | Reconcile run reads the item | A person holding Documents C resolved it in rwb-document | `MATCHED`, `document_id` set |

`PENDING` is the only state a submission is created in, and a submission leaves the held set only through the document hub's own resolution: this service copies the state and never sets it on a document.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner portal users of the instructed firm: PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC (C on their own firm) | Submit a file on their own firm's instruction; read their own submissions |
| RW-AGENCYMG, partner and agency manager (CRUDA) | Read the submissions of any firm; submit on behalf of a firm through the portal |
| RW-CASEOWN, case owner (R) | Read the submissions and their attach state on the case |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT (R) | Read the submissions inside their capability area |
| RW-AUDIT, RW-COE (R) | Read the submission and the record it was accepted under |
| A person holding Documents C (in rwb-document) | Resolve a held item there; this service grants no attach right and holds no document |
| SY-PARTNER, service identity (login `rwb_partner`) | Writes `partner_intake`, the record and the outbox row in its own schema; no grant elsewhere |
| Role without Partner portal C | Refused with MSG-P4-002 before any read |

Each operation of the partner REST API is checked by the rwb-access authorise check (DP-08) before any read or write.

No delegation of authority level applies: submitting a file decides nothing about the customer, and the record names the code in force, not a person's level. No personal name or credential appears in the story, a test or a log.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008, DF-PRT-009, DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id | Read, the instruction, the case hint and the firm |
| DF-PRT-011, DF-PRT-013, DF-PRT-014 | partner_instruction (S9) | instruction_type, due_at, status | Read, the type and the state check |
| DF-PRT-015, DF-PRT-016 | partner_instruction (S9) | result_code, fee_amount | Not written here: the result and the fee are other S9 stories' |
| DF-PRT-001 to DF-PRT-007 | partner (S9, `rwb_partner`) | id, partner_code, partner_type, panel_status, contract_end, score | Read, the firm and its panel status |
| DF-REF-212 to DF-REF-217 | partner_user (S9, `rwb_partner`) | identity_ref, partner_id, role_code, valid_from, valid_to | Read, the firm and role binding |
| Not specified in the source documents (GAP-3143; ASM-5509) | partner_intake (S9, `rwb_partner`, created by this story) | id, partner_id, instruction_id, case_id, document_type, file_sha256, intake_item_id, state, candidate_case_ids, received_at | Write on acceptance; written again by the attach event and the reconcile run |
| Not specified in the source documents (GAP-3143; ASM-5509) | partner_intake (S9) | version, created_at, created_by, updated_at, updated_by | Write the audit columns; `version` is the optimistic lock |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, `rwb_partner`) | all fields, through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| DF-DOC-001 to DF-DOC-011 | document (P5, `rwb_document`) | the document and its ID | Not read and not written: they arrive in the attach event |
| DF-DOC-075, DF-DOC-076 | document_intake (P5) | match_status, candidate_case_ids | Read through the item read of RWB-P5-E1032-CON only |
| DF-CAS-001, DF-CAS-002, DF-CAS-005 | recovery_case (P3, `rwb_case`) | id, case_no, status | Not read: the case ID is the instruction's and travels as the event key |
| DF-ACE-002 | v_ace_account | account_code | Not read: this service resolves no account (DP-05) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_partner` | the outbox row, the inbox row and the write key | Write through the library, in the transaction (DP-09) |

`partner_intake` is the only table this story creates and writes, and the fields above are its design content, not source values: no published data model carries a partner-side intake row (GAP-3143). No foreign key leaves `rwb_partner`: `partner_id`, `instruction_id` and `case_id` are identifiers. No file and no OCR text is stored here.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). No source publishes these two operations (GAP-3141; ASM-5507).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/documents` | Multipart: file, documentType; `PartnerSubmission` out, 201; errors 401, 403, 404, 409, 415, 422, 503 | Partner portal C, own firm, guard library | `Idempotency-Key` header |
| GET | `/partner/instructions/{instructionId}/documents` | Query: state, page, size; `SubmissionPage` out; errors 401, 403, 404, 503 | Partner portal R, own firm, scope applied | Not applicable |

Both are reached through the partner gateway (FAPI 2.0) by partners and through the composite route by staff (DP-19). Errors are RFC 9457 problem bodies; the 409 body text is Not specified in the source documents (GAP-3141; ASM-5507).

#### 12.2 REST operations consumed

| Method | Path | Owner | Story | Note |
|---|---|---|---|---|
| POST | the intake creation of the document hub | P5 rwb-document | RWB-P5-E1032-CON carries the IntakeItem shape; the operation itself is Not specified in the source documents (GAP-3141) | One hop, 2 s timeout, breaker, one POST retry with jitter; a failure leaves the row `PENDING` (DP-11) |
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}` | P5 rwb-document | RWB-P5-E1032-CON (12.1 of RWB-P5-E1032-APP) | The match state and the candidate cases of a submission not yet concluded |
| GET | the parameters read of DP-06 | P3 behind the client library | RWB-P3-E1042-CON | The intake bound, cached for 5 minutes |
| GET | the reference-data read of DP-07 | P3 behind the client library | RWB-P3-E1043-CON | LOV-DOC-TYPE and LOV-INSTR-STATUS at their version |

The two list reads and the bound arrive through the client library of the service template, so the plan's C row names the document-hub contract only (GAP-3140; ASM-5506).

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.partner.PartnerDocumentSubmitted.v1` | `rwb.partner.events.v1` | `caseId` | submission ID, instruction ID, case ID, document type, file SHA-256, intake item ID, submitted time | Carries the partner source and the case hint to the document hub's matcher and the state to rwb-reporting; written to the outbox in the transaction |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary |
| ce_type | `rwb.partner.PartnerDocumentSubmitted.v1` |
| ce_source | rwb-partner |
| ce_subject and key | The case ID of the instruction |
| ce_id and traceparent | The event identifier and the W3C trace context of the call |
| Payload | Identifiers, a type code, a hash and a time only; no file content, no OCR text, no personal data, no file name |

The event name and its catalogue ID are this story's design choice and are absent from the Arch v5 event list for this service (GAP-3141; ASM-5507). The retry and `.dlt` topics are the service template's and add no row here.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.document.DocumentAttached.v1` | `rwb.document.events.v1` | P5 rwb-document (RWB-P5-E1032-APP 12.3) | Matched to the submission by its intake item ID: sets `MATCHED` and `document_id` and signals the instruction workflow; a duplicate is discarded by the inbox row (AC2) |

The held match states do not travel as events: the reconcile run reads them through the item read of 12.2, so a held item is copied and never re-decided here.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `PartnerInstructionWorkflow` | Workflow, one execution per instruction, owned by the S9 instruction stories | `rwb-partner`, namespace `rwb-recovery` | Signal `documentAttached` with the submission ID and the document ID; a replay reuses the recorded outcome |
| `recordPartnerDocument` (name is this story's design choice) | Activity | `rwb-partner` | One `rwb_partner` transaction: the submission row, the record, the outbox row; then the intake call |
| `reconcilePartnerIntake` | Activity | `rwb-partner` | The item read per open submission, the state copy, the retry of a failed intake call |
| `PartnerIntakeReconcileWorkflow` | Workflow, started by the Schedule of 12.6 (overlap policy SKIP, catch-up window; time of day Not specified in the source documents (GAP-0744)) | `rwb-partner` | The L3 "Document intake" template applied to the partner channel: one activity over the open submissions |

The signal and activity names are fixed by no source (GAP-3141; ASM-5507).

#### 12.6 Schedules

| Schedule | Workflow | Queue | Interval | Note |
|---|---|---|---|---|
| `partner-intake-reconcile` | `PartnerIntakeReconcileWorkflow` | `rwb-partner` | Every 15 minutes in business hours (the legacy JOB-12 cadence); window bounds Not specified in the source documents (GAP-0994) | Registered by this story; overlap policy skip; catch-up of one run; a run that leaves a submission `PENDING` is retried by the next run, as the legacy restart behaviour states; run-failure, held-item age, KEDA and consumer-lag thresholds are Not specified in the source documents (GAP-0994); lag alert identifier Not specified in the source documents (GAP-0994) |

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `partner_intake` | `rwb_partner` | S9 | Creates it in its own Flyway step; writes the row, the state, the candidate case IDs and the intake item ID |
| `partner` | `rwb_partner` | S9 | Read only, the firm and its panel status |
| `partner_user` | `rwb_partner` | S9 | Read only, the firm and role scope |
| `partner_instruction` | `rwb_partner` | S9 | Read only, the case hint, the type and the state |
| `decision_record` | `rwb_partner` | PLT library applied here | Written through `DecisionRecordWriter.record`; the central `decision_log_entry` is P7's (DP-03) |
| `processed_event`, `outbox_event`, `idempotency_key` | `rwb_partner` | PLT library applied here | The inbox row, the outbox row and the write key |

Not owned and never read as a table: `document`, `document_intake` (P5), `recovery_case`, `task`, `timer` (P3), `decision_log_entry`, `rule_row` (P7) and `interaction` (P1). No foreign key leaves the schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `RWB-P5-E1032-CON` intake fake (rwb-document contract fake; library version Not specified in the source documents (DOR-RWB-S9-E1032-APP-22)) | An intake item ID with state `PENDING`; a held item with a match state and two candidates; a `MATCHED` item with a document ID; a 409 for a closed instruction; a 404 for a foreign firm; a 422 for a refused element | AC1, AC2, AC3, AC5 |
| Attach-event fixture | One `rwb.document.DocumentAttached.v1` per item keyed on the case ID, and the same event twice | AC2, AC4 |
| Record-writer fake (`RWB-PLT-E1027-CON`) | An accepted record with chain sequence and entry hash, and a refusal with MSG-P7-003 | AC1, AC6 |
| Composite-route fake (`RWB-PLT-N001-CON`) | The merged SCR-35 answer for the case | AC7 |

The fakes are test-only and are replaced by the real services in SIT; a drift is a build failure of the story that owns the fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The submission and the list on `/api/recovery/partner/v1`; the intake creation and the item read of rwb-document; the parameters and reference-data reads behind the client library |
| Kafka | 1 published, 1 consumed | `rwb.partner.PartnerDocumentSubmitted.v1` keyed on the case ID; `rwb.document.DocumentAttached.v1` in; the record library's `DecisionRecorded` on `rwb.decision-record.v1` (DP-03) |
| Temporal | 2 workflows, 2 activities, 1 Schedule | `PartnerInstructionWorkflow` signal and `PartnerIntakeReconcileWorkflow` with their activities on `rwb-partner`; the 15-minute Schedule |
| File | 1 inbound, 0 stored | The file is read for its SHA-256 and handed to the document hub; storage, OCR and retention are rwb-document's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.partner`, module `intake`; front end `src/modules/recovery/partner/InstructionDocuments.tsx`, the fragment SCR-35 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP table record (GAP-2448) | Dependency rows of DP-03, DP-06, DP-07, DP-09, DP-10, DP-15 and DP-19; the metadata rows stay as the work package fixes them (Depends on (build) None; Contract dependencies RWB-P5-E1032-CON; RWB-S9-E1032-CON) | Built against their fakes on Day 1 | H RWB-PLT-E1027-CON; H RWB-PLT-E1042-CON; H RWB-PLT-E1043-CON; H RWB-PLT-TE006-CON; H RWB-PLT-E1071-CON; H RWB-PLT-E1044-CON; H RWB-PLT-N001-CON; C RWB-P3-E1042-CON; C RWB-P3-E1043-CON; authorise RWB-P4-E1037-CON (named in GAP-2448) |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 moves the partner-side intake row into `rwb_partner` and stops this service reaching into the document schema. DP-03 is the transaction the story is built on: the row, the record and the outbox row commit together or not at all. DP-05 is applied by removal: the legacy matcher read `v_ace_account` through the case directory, and here the case is the instruction's `case_id` and no account is read. DP-06 and DP-07 keep the intake bound and the two lists out of the code through the client library. DP-09 writes the fact in the outbox and discards a duplicate through the inbox. DP-10 turns the legacy JOB-12 step into a Schedule in the same cadence. DP-11 is the document-hub call and read: one hop, a published shape and a 2 s timeout. DP-15 puts the migration in the service's own sequence, and DP-19 puts SCR-35 behind the composite route. The six platform CON rows the DP table names are the shared baseline of wave 0 and add no row to this plan's H list, which the work package fixes empty (GAP-3140; ASM-5506).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerDocumentController` | REST controller | The two operations, the multipart parse, the RFC 9457 mapping (BR1, BR4, BR7) |
| `PartnerDocumentService` | Service | Firm scope, state check, validation, the case hint, the version in force, the record assembly (BR2, BR4, BR8) |
| `PartnerIntakeRepository` | Repository | Reads and writes `partner_intake`; reads `partner`, `partner_user`, `partner_instruction` in `rwb_partner` only |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with the code and the version (DP-03, BR5) |
| `SubmissionOutboxWriter` | Library adapter | Writes the outbox row in the transaction (DP-09) |
| `DocumentHubClient` | Client | The intake creation and the item read, one hop, 2 s budget, breaker (DP-11) |
| `AttachEventConsumer` | Consumer | Matches the attach event to the submission, sets `MATCHED`, signals the workflow, discards a duplicate |
| `ReconcileActivity` | Temporal activity | Copies the state of the open submissions and retries a failed intake call |
| `InstructionDocuments` | React component | The submission list of SCR-35, read only |

**Database.** One migration in the per-service Flyway sequence (DP-15), `V1032_1__partner_intake.sql` (the version number is this story's choice): `partner_intake` with `partner_id`, `instruction_id`, `case_id`, `document_type`, `file_sha256`, `intake_item_id`, `state`, `candidate_case_ids` jsonb, `received_at`, the standard audit columns and `version`; unique key `uk_partner_intake_instr_hash` on (`instruction_id`, `file_sha256`) for BR7; index `ix_partner_intake_open` on (`state`, `received_at`) where `state = 'PENDING'` for the reconcile run.

**Configuration and reference data.** The intake bound and the two lists read at their version through DP-06 and DP-07; no list value and no bound is typed in code. The decision code of the acceptance is a reference value in force whose name is Not specified in the source documents (GAP-3142; ASM-5508). No feature flag of its own: `rwb.dochub.autoattach` belongs to the document-hub slice and the partner column keeps the partner portal as documented.

**Build steps.** (1) The migration, the entity and the write key; test BR7 and the stale `version`. (2) The two operations behind the contract fake; test AC1 and AC5. (3) The record adapter and the rollback; test AC6 (X3). (4) The outbox row and the event fixture; test AC1 and AC4. (5) The consumer, the inbox row and the signal; test AC2. (6) The reconcile Schedule and its activity against the item-read fake; test AC3 (X4, X6). (7) The screen fragment and the boundary, stale-data and no-PII tests; test AC7 and section 17. **Done when** the tests of section 16 pass, one accepted file writes one row, one record and one event, one attach outcome closes one submission, a held file is copied and never attached here, and SCR-35 shows the state through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element is missing or refused on submission (X2, AC5) | Enter {field}. |
| MSG-P4-002 | The identity has no Partner portal C on the submission or R on the read | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written and the submission is not accepted (AC6, X3) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The intake creation or the item read misses the budget, or its breaker is open (X4) | {system} is not available. Try again in a few minutes. |
| MSG-P5-003 | The submission is held for a person in the document hub (AC3) | Some fields need checking. The document is in the review queue. |
| Not specified in the source documents (GAP-3141; ASM-5507) | The instruction is closed (409) or belongs to another firm (404) (X1) | The 409 and 404 bodies carry no message ID in any source |

The five IDs and their texts are copied unchanged from the legacy story and the FSD; this story adds no message. Status mapping: 403 MSG-P4-002, 404 and 409 for a closed or foreign instruction, 415 for a wrong body type, 422 MSG-GEN-001, 503 MSG-GEN-006 or MSG-P7-003. Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-35 Placement and allocation | Loading | The composite-route placeholder while the submission list answers |
| SCR-35 Placement and allocation | List | The submissions of the instruction with type, received time and state, read only |
| SCR-35 Placement and allocation | Attached | State `MATCHED` with the document ID; the case owner opens the document on SCR-30 of rwb-document |
| SCR-35 Placement and allocation | Held | The legacy match state with the candidate cases and MSG-P5-003; no action on this screen |
| SCR-35 Placement and allocation | Refused | A role without Partner portal R reads MSG-P4-002 and nothing changes |
| SCR-35 Placement and allocation | Empty | Not specified in the source documents (CG-ALL-11748) |
| SCR-35 Placement and allocation | Error | Not specified in the source documents (CG-ALL-11748) |
| SCR-35 Placement and allocation | No access | Not specified in the source documents (CG-ALL-11748) |
| The partner portal screen of the instruction (one of PRT-01 to PRT-04; the exact number is Not specified in the source documents (GAP-3145); ASM-5511) | Submit, submitted, held, refused | The partner user submits a file with its type and reads the state of its own submissions, read only after submission |
| The partner portal screen of the instruction (one of PRT-01 to PRT-04; the exact number is Not specified in the source documents (GAP-3145); ASM-5511) | Empty | Not specified in the source documents (CG-ALL-11746) |
| The partner portal screen of the instruction (one of PRT-01 to PRT-04; the exact number is Not specified in the source documents (GAP-3145); ASM-5511) | Error | Not specified in the source documents (CG-ALL-11746) |
| The partner portal screen of the instruction (one of PRT-01 to PRT-04; the exact number is Not specified in the source documents (GAP-3145); ASM-5511) | No access | Not specified in the source documents (CG-ALL-11746) |

Both reads come through the composite route, which composes the case read of rwb-case with the submission read of this service, one hop each (DP-19). The route specification, the field list and the layout are the platform edge story's; this story fixes the service side of the answer only. SCR-31 Document review queue and SCR-30 Case documents are rwb-document's and are not built here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S9-E1032-APP-01 | AC1, BR2, BR5, BR9 | Component | A valuation report of type `APPRAISAL_REPORT`, hash `H1`, on an `ACCEPTED` `COLLECT` instruction of case `RW-2026-000123`; row, record, outbox row and intake call asserted |
| TC-S9-E1032-APP-02 | AC1, BR4 | Contract | The two operations against the `RWB-P5-E1032-CON` fake: the multipart shape, the 415, the 422 and the `Idempotency-Key` |
| TC-S9-E1032-APP-03 | AC2, BR5 | Component | The attach event for intake item `TI-0001` twice; one `MATCHED` row, one signal, one inbox row |
| TC-S9-E1032-APP-04 | AC3, BR3, BR8 | Component | Items holding `NO_MATCH`, `MULTIPLE`, `CONFLICT`, `CASE_CLOSED` and `NO_TYPE`, and one resolved by a person between two runs |
| TC-S9-E1032-APP-05 | AC4, BR7 | Component | The same hash twice under one instruction and one key, then a second key on the same hash |
| TC-S9-E1032-APP-06 | AC5, BR1, BR8 | Component | A `DONE` instruction, a foreign instruction, a submission without a type and a role without Partner portal C |
| TC-S9-E1032-APP-07 | AC6, BR5 | Component | A forced record refusal mid-transaction; no row, no event, no intake call |
| TC-S9-E1032-APP-08 | AC7, X4 | Component | The composite-route fake merging the case read and the submission list; a 2 s timeout on the item read |
| TC-S9-E1032-APP-09 | AC9, X7 | Component | Each table of section 12.7 read or written in `rwb_partner` only; a write attempt on `document`, `document_intake`, `recovery_case` or `task` is refused and the build fails |
| TC-S9-E1032-APP-10 | AC8, BR6, X4 | Component | An intake creation past the 2 s budget with the breaker open; the row stays `PENDING`, the partner gets MSG-GEN-006, one retry with jitter in the reconcile run |
| TC-S9-E1032-APP-11 | AC10, BR6 | Component | A contract read that misses the 2 s budget; no column changed, one retry with jitter |
| TC-S9-E1032-APP-12 | AC11 | Contract | A submission and a read on `/api/recovery/partner/v1` without credentials; the answer is 401 and nothing is written |
| TC-S9-E1032-APP-13 | AC12, BR7 | Component | The attach event for intake item `TI-0001` redelivered after consumption; no column changed, no second signal |

The seventeen legacy test cases TC-E1-032-01 to TC-E1-032-17 stay with RWB-P5-E1032-APP, which owns the criteria they test (GAP-3144; ASM-5510); this slice executes none of them and re-tests no legacy value. The full test is in Recovery Workbench Test Cases, tab Story test cases, and an integration copy would end in `-ITG`; no ITG story is planned for this key in wave 1.

### 17. Guardrails

- No business value in code: the states, the types, the intake bound, the decision code and the version are read at their version; a build check fails on a list member in source or configuration (BR4).
- No personal data and no document content in the row, the record, the event, logs or spans: identifiers, codes, a hash and dates only (BR9).
- No read of another service's tables and no cross-schema join: `document`, `document_intake` (P5), `recovery_case` (P3), `decision_log_entry`, `rule_row` (P7) and `interaction` (P1) are reached only through their owners.
- The record is written in the same transaction as the acceptance, and a failed write leaves no row, no event and makes no call (AC6, X3).
- One submission per instruction and file hash, and one event per submission: the unique key and the `Idempotency-Key` carry the rule (BR7, AC4).
- The file is hashed and handed over; this service stores no file, runs no OCR and writes no document row.
- No ACE view and no ACE grant in this service: the case arrives from the instruction (DP-05).
- An applied migration is never edited: `partner_intake` is a new version of the service's own sequence.
- The portal is reached only through the partner gateway with multi-factor authentication, and a scope filter applies to every query (NFR-050).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person — this story supplies the partner case reference the attach resolves | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39, BR2, BR5 | TC-S9-E1032-APP-01, TC-S9-E1032-APP-02 |
| REQ-DCM-005 | A document that cannot be matched is held for a person — this story copies the hold to the partner side and attaches nothing | Program, section 5.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | BR3, R-UNI-40 | TC-S9-E1032-APP-04 |
| REQ-DRI-004 | The attached record — this story writes the acceptance record of a partner file | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | BR5, BR9 | TC-S9-E1032-APP-01, TC-S9-E1032-APP-07 |

The three rows are the legacy requirement IDs; the BLOCK for them is the primary slice's and this story answers their partner half. No requirement ID is invented.

Open decision DL10 is still open: this story proceeds on its assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 and is re-opened if any of them fails.

| Story or item | Relation to this story |
|---|---|
| RWB-P5-E1032-APP | The primary slice: the matcher, the store, the reviewer path and AC1 to AC15 with TC-E1-032-01 to TC-E1-032-17 |
| RWB-P5-E1032-CON | C: the IntakeItem shape, the item read and the fakes; the intake creation is outside its four operations |
| RWB-S9-E6033-CON and the other S9 CON stories | The S9 contract baseline that publishes the operation shapes at the wave start (GAP-3141) |
| rwb-document (P5) | Owns the file, the OCR, the classification, the intake item, the document row and the hold queue |
| rwb-case (P3) | Owns the case; the case ID is read from the instruction, never from a case table |
| rwb-decision (P7) | Seals the local record in the central ledger |
| The other S9 stories | The panel, the instruction, the allocation and the fee; this story writes the instruction's documents state only |

### 19. Out of scope

- The match, the store, the document row, the review queue and the resolution of a held item — the match and attach of the primary slice: RWB-P5-E1032-APP.
- The document-hub contract and its four operations: RWB-P5-E1032-CON.
- The file storage, the OCR, the classification, the field extraction and the retention of a partner file: rwb-document (P5).
- The partner SFTP drop and the mailbox and branch intake of the document hub: RWB-P5-E1057-APP.
- The case, its status, its owner and its scope: rwb-case (P3).
- The central ledger, the chain check and the decision-log read: rwb-decision (P7).
- The instruction, the result, the panel, the allocation and the fee: the other S9 stories.
- The partner gateway route, the composite route and the SCR-35 field list and layout: the platform edge story and RWB-PLT-N001-CON.
- The physical schema files, the grants, the Helm release, the dashboards and the runbook of this story: the platform stories and the S9 deployment work.
- AC1 to AC15 and TC-E1-032-01 to TC-E1-032-17 of the legacy story: the primary slice.
