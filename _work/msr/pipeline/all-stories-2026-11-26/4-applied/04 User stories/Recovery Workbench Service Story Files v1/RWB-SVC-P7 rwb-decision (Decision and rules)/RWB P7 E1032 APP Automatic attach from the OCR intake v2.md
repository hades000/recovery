# RWB-P7-E1032-APP Automatic attach from the OCR intake

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 |
| Parallel lane | L-P7-K |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1032-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-002) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-032 for `rwb-decision`; the `DOCATT` decision record of an automatic attach and of a reviewer's attach, the fail-closed path of legacy X13 and the two decision-log reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E1032-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal auditor (RW-AUDIT) and a case owner (RW-CASEOWN) who has to show why a document sits on a case**, I want **one decision record for every document the OCR intake attaches automatically and for every document a reviewer attaches by hand, in the central decision ledger of `rwb-decision`, carrying the decision code `DOCATT`, the classifier version, the confidence, the match method, the approver where a person decided, the inputs reference, the final call, append only, hash chained and readable by case through `GET /api/recovery/decision/v1/decision-log`**, so that **no document is on a case without the decision that put it there, a scan filed by hand is as explainable as one filed by the machine, and an attach that cannot be recorded never happens at all**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E1-032:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record library of DP-03.
- One deliverable and nothing else: the `DOCATT` record of an attach. It is appended to `decision_log_entry` when the `DecisionRecorded` fact of an attach reaches `rwb.decision-record.v1`, carries the classifier model version, the confidence, the match method `CASE_ID`, `ACCOUNT_NO` or `PERSON`, the approver where a reviewer decided, the document reference and the intake item reference, and it is served by the two decision-log reads.
- What stays with `rwb-document` (P5, RWB-P5-E1032-APP with RWB-P5-E1032-CON): the `matchStep` of JOB-12, the `CaseMatcher`, the five match outcomes, the store, the `review_status` and `write_once` rule, the `rwb-docs` container, the `DocumentAttached` event on `rwb.document.events.v1`, the reviewer's `resolve` operation and the Unmatched list on SCR-31. This story consumes their outcome and decides none of it.
- What stays with `rwb-access` (P4): the Documents right `C` on the chosen case and the scope answer behind the reviewer's attach, and the decision-log area right `R` behind the two reads. This story consumes the answer and writes no access entry.
- What stays with `rwb-case` (P3): the case, its status, its owner, the open cases of an account number and the reference lists and parameters behind DP-06 and DP-07. This story reads none of them as a table.
- The record is written before the attach stands (legacy BR5, principle 5, R-UNI-39). A record that cannot be written refuses the attach: nothing is stored, the automatic item stays `PENDING` for the next run, the manual attach answers 503 with MSG-P7-003, and an incident is raised (legacy X13, TC-E1-032-17).
- The database login is the per-service login of DP-02; its name is Not specified in the source documents (GAP-2449; ASM-4057), so the story says "the rwb-decision login (DP-02)" and never the legacy shared login.
- The values are the legacy ones and no new business value is introduced: case `RW-2026-000123` with account `TEST-ACC-0001`, case `RW-2026-000456` with account `TEST-ACC-0002`, the closed case `RW-2026-000789`, the accounts `TEST-ACC-0003`, classifier version `CLS-1.0`, confidences 0.93, 0.88 and 0.62, the threshold 0.80, reviewer `TEST-LIT-01` holding `RW-LITOFF`, and the item version 3.

### 2. Business rationale

A document on a case is evidence the bank will produce in court, and the legacy story proves it arrived; this slice proves the decision that filed it. Today the `DOCATT` entry is written inside the same monolith transaction as the document, so an auditor cannot tell the record from the change, and a reviewer's decision is a row that looks exactly like a machine's. Under Architecture v5 the document is `rwb-document`'s and the ledger is `rwb-decision`'s, so the explanation lives in the one place every service's record is collected and read.

This story carries the record half of REQ-DRI-004 and REQ-DCM-007 and the measure `Decisions within the delegation of authority` at 100 percent for the intake-match path. It carries R-UNI-39 (no action without its record), R-UNI-40 (a repeat writes one entry), NFR-033 (a decision is reproducible from the log), NFR-034 (the version and the approver travel on the record), NFR-035 (the chain is checked daily) and the guardrail that OCR text and account numbers are never logged.

The realignment changes the mechanism, not the business rule:

1. The in-process decision-log write of the monolith becomes the local record of `rwb-document` plus `DecisionRecorded` on `rwb.decision-record.v1`; this service appends the central entry in `rwb_decision` through the library of DP-03, with the append-only rule and the hash chain (FEAT-DRI-01, FEAT-DRI-03).
2. A reviewer's attach becomes a decision with an approver: the entry names `TEST-LIT-01` as approver and `PERSON` as the match method, so a person's filing is never indistinguishable from the matcher's (legacy BR5, FEAT-DRI-04).
3. The legacy feature flag `rwb.dochub.autoattach` becomes a source fact only: with it off every classified item is held and no `DOCATT` record of an automatic attach reaches this service, while a reviewer's attach still does (legacy section 13).
4. The one in-process decision-log read becomes two operations on this service's own base (DP-13 through 12.1), reached through the gateway-bff composite route the screens already use (DP-19); the nightly copy of the log to the data lake is retired with the data lake (DP-17).
5. The decision code `DOCATT`, the final call set and the ledger parameters become reference rows and parameter rows of their owners (principle 1); nothing is a constant of this service.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E1032-CON | The published intake-match contract of `rwb-document` (P5): the four operations, the seven `matchStatus` values, the `Document` answer, the `DOCATT` record declaration on `rwb.decision-record.v1` with the match method `CASE_ID`, `ACCOUNT_NO` or `PERSON`, the classifier version and the confidence, and the contract fakes. Which fields of the fact this service consumes is Not specified in the source documents (GAP-2447; ASM-4055), and the fact set used is that of ASM-4055 |
| RWB-PLT-E1027-CON | The decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, `prev_hash`, `entry_hash`, the append-only rule and the fail-closed `DecisionLogUnavailableException` |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the ledger ingest target (5 minutes) and the daily chain-check time (02:00, JOB-14) at the version in force; the parameter names are Not specified in the source documents (GAP-2449; ASM-4057) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): the decision code list with `DOCATT` in force and the approval level list; whether the list carries `DOCATT` is the gap of GAP-2445 |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one entry under a repeated fact, and the outbox row of the append |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-E1071-CON | The workflow kit (DP-10), named because the intake trigger is a Temporal Schedule; this story creates no Schedule and adds no activity |
| RWB-P4-E1037-CON | The authorise contract of `rwb-access` (P4) behind the two reads: area `DECISION_LOG`, right `R`, scope applied (GAP-2448; ASM-4056) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) the reader of a case reaches the two operations through |

Business preconditions carried from RWB-E1-032:

- Case `RW-2026-000123` is open, owned by `TEST-CO-01` and linked to account `TEST-ACC-0001`; case `RW-2026-000456` is open and linked to `TEST-ACC-0002`; case `RW-2026-000789` is closed (legacy section 7 Background). The cases are `rwb-case`'s and reach this service as facts.
- The parameter `CLASSIFY_THRESHOLD` is 0.80 and the patterns `CASE_NO_PATTERN` and `ACCOUNT_NO_PATTERN` are in force; they are the store's parameters, and this story applies none of them.
- A reviewer resolving an unmatched item holds Documents `C` on that case; an item with no candidate is visible only to roles with scope `ALL` (legacy section 10).
- No build dependency and no integration dependency: the story builds against RWB-P5-E1032-CON, the platform contracts of the DP table and their fakes on Day 1 (Template and Rules §R5.7 rule 8).

### 4. Flow

1. A scan, a partner file or an email reaches `rwb-document`; JOB-12 classifies and extracts it, and `matchStep` matches it to one open case by the case ID or the account number read from its text (legacy section 4 steps 1 to 4; the work of RWB-P5-E1032-APP).
2. For a `MATCHED` item the store writes the document and the `DOCATT` record in its own transaction, writes the `DocumentAttached` event and `DecisionRecorded` on `rwb.decision-record.v1`, and sets the item `MATCHED`; for any other outcome it holds the item and writes no record (legacy section 4 steps 5 to 7; BR6).
3. `rwb-decision` `IntakeAttachDecisionListener`: reads the fact into the inbox of DP-09, deduplicates by event ID and by the idempotency key the fact carries (R-UNI-40), and passes the decision facts to `IntakeAttachDecisionRecorder`: the case, the decision code, the document reference, the intake item ID, the match method, the classifier version, the confidence, the approver reference where a person decided, the final call and the inputs reference.
4. `IntakeAttachDecisionRecorder`: reads the decision code list and the approval level list through the reference-data contract of DP-07 and the ledger parameters through the parameters contract of DP-06, at the version in force on the business date, and composes the entry. It decides nothing about the match: it applies no pattern, no threshold and no outcome of its own (BR2, BR7).
5. `DecisionLogAppender`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash`, computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with its `inputs_ref`, and writes the outbox row of the append (DP-03; BR2, BR9).
6. `DecisionLogAppender`: a repeated fact with the same idempotency key returns the first entry's ID, adds one to the repeat count for R-UNI-40, and appends nothing (BR8).
7. When the append cannot be made, the library raises `DecisionLogUnavailableException` to its caller inside the store's transaction; the store's attach does not stand, the automatic item stays `PENDING` for the next run, the manual attach answers 503 with MSG-P7-003, and an incident is raised (legacy X13; BR4).
8. A reviewer opens a held item, picks the case and the type and attaches it through the `resolve` operation; that attach carries the same decision record with the reviewer as approver and `PERSON` as the match method (legacy section 4 steps 8 and 9; BR3).
9. An auditor or a case owner reads the entries with `GET /api/recovery/decision/v1/decision-log` by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, each behind the authorise answer of DP-11 (BR11).
10. `IntakeAttachCompletenessChecker`, on the ledger ingest window: reads the documents of a case from the document contract and compares them with the `DOCATT` entries of the case, and reports a document with no entry as a gap, which is the missing-record alert of Architecture v5 slide 28 (BR12).
11. Nothing in this story moves a document, an intake item, a review item or a case: the entry is appended beside them and the screens keep reading the intake facts through `rwb-document`'s contract (BR10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The `DOCATT` record cannot be written, because the library is unavailable or the chain cannot be taken | Nothing is written: no entry, no chain position, no outbox row. Nothing is stored, an automatic item stays `PENDING`, a manual attach answers 503, and an incident is raised | MSG-P7-003 | AC5, TC-E1-032-17 |
| X2 | The same attach fact is delivered again, or the same file arrives in a second intake item, or two reviewers attach the same item at version 3 | One entry exists: the inbox dedupe, the idempotency key and the partial unique key all hold, and the repeat is counted | None | AC4, TC-E1-032-08, TC-E1-032-09, TC-E1-032-15 |
| X3 | An item is held as `NO_MATCH`, `MULTIPLE`, `CONFLICT`, `CASE_CLOSED` or `NO_TYPE` | No entry and no chain position, because no document was stored and no attach decision was taken; the held status stays on the item in `rwb_document` | MSG-P5-003 (produced by `rwb-document`) | AC6, TC-E1-032-02 to TC-E1-032-07, TC-E1-032-11 |
| X4 | An attach is refused for a type not in force, a case out of scope, or a changed version | No entry: the refusal is the store's or the access answer's and is recorded there | MSG-P5-006, MSG-P4-002, MSG-P4-003, MSG-GEN-004 | AC6, TC-E1-032-13, TC-E1-032-14 |
| X5 | An entry names a decision code outside the list in force, or a rule id with no rule version | The append is refused with MSG-P7-009 naming `decisionCode` or `ruleVersion`, and nothing is written | MSG-P7-009 | AC1 |
| X6 | The fact carries no case reference, no document reference or no match method | The append is refused for that fact and the incident names the fact ID; no entry is made on a guessed document | MSG-GEN-006 | AC1 |
| X7 | A caller attempts to change or delete an entry | The statement is refused, by the missing grant for the service login and by the append-only rule of the table; a correction is a new entry naming the one it corrects in `corrects_entry_id` | None | AC8 |
| X8 | A caller holds no right in the `DECISION_LOG` area, or asks for a case out of scope | 403 with MSG-P4-002, or 403 with MSG-P4-003; no row is returned | MSG-P4-002, MSG-P4-003 | AC7, TC-E1-032-16 |
| X9 | The documents of a case and the `DOCATT` entries of the case disagree inside the ingest window | The checker reports the document with no entry as a gap and raises the missing-record alert; no entry is invented for it | MSG-GEN-006 | AC7 |

The entry, its chain position and its outbox row commit in one transaction, so a fact can never leave a half record and a record can never exist for a document that was not stored (BR9).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the intake-match contract of RWB-P5-E1032-CON, the platform contract libraries of its DP table and the fakes; no matching, store, classification, extraction, review or access behaviour is rebuilt here |
| Negotiable | The decision code, the final call set, the document types, the parameters and the message ids are data of their owners; the story fixes only the record, the fail-closed refusal, the append-only rule, the chain and the two reads |
| Valuable | Every document on a case, filed by the matcher or by a person, can be explained, counted and shown unchanged to an auditor |
| Estimable | One listener, one recorder, one appender with the chain, one query controller with two operations, one completeness checker, one migration, one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the nine criteria in section 7 runs as one automated test against the contract fakes with a fixed business date and a fixed chain |

### 7. Acceptance criteria

```gherkin
Feature: Automatic attach from the OCR intake — the rwb-decision DOCATT decision record

  Background:
    Given the environment is SIT
    Given the rwb-document contract mock returns case "RW-2026-000123" open with account "TEST-ACC-0001", case "RW-2026-000456" open with account "TEST-ACC-0002" and case "RW-2026-000789" closed
    Given the rwb-case reference-data contract mock returns the decision code list with "DOCATT" in force and the rwb-case parameters contract mock returns the ledger ingest target and the chain-check time in force

  Scenario: AC1 One DOCATT record per automatic attach, with its version, its confidence and its method (new, D-RCV-60)
    Given a scanned notice with the case ID "RW-2026-000123" read by OCR, classified "COURT_NOTICE" at 0.93 by classifier version "CLS-1.0", attached with match method "CASE_ID" and stored as document "DOC-2026-0009981" from intake item "II-2026-000123"
    When the DecisionRecorded fact of that attach reaches rwb.decision-record.v1
    Then one decision_log_entry row exists in rwb_decision for case "RW-2026-000123" with decisionCode "DOCATT", modelVersion "CLS-1.0", the confidence 0.9300, the match method "CASE_ID", finalCall "ATTACHED" and the document reference "DOC-2026-0009981"
    Then the entry carries the ruleId and ruleVersion in force, its inputsRef naming intake item "II-2026-000123", and its chainSeq, prevHash and entryHash
    Then GET /api/recovery/decision/v1/decision-log for case "RW-2026-000123" returns that entry and GET /api/recovery/decision/v1/decision-log/{entryId} returns it with its modelVersion, its confidence and its match method
    Then a document stored at 0.62 with candidates "APPRAISAL_REPORT" 0.62 and "TITLE_DEED" 0.30 leaves one entry carrying the confidence 0.6200 and the type "APPRAISAL_REPORT", and the review state stays in rwb_document

  Scenario: AC2 The record names the account number as the method when no case ID was read (new, D-RCV-60)
    Given a scan with no case ID and the account number "TEST-ACC-0002", classified "DEMAND_LETTER" at 0.88 and attached to case "RW-2026-000456" with match method "ACCOUNT_NO"
    When the DecisionRecorded fact of that attach reaches rwb.decision-record.v1
    Then the entry carries the match method "ACCOUNT_NO", the case "RW-2026-000456" and the confidence 0.8800
    Then the entry names no case number it did not receive, and the account number is not written into the entry, the fact or the log line

  Scenario: AC3 A reviewer's attach names the reviewer as approver (new, D-RCV-60)
    Given the rwb-document contract mock returns the MULTIPLE item of cases "RW-2026-000321" and "RW-2026-000654", resolved by reviewer "TEST-LIT-01" holding "RW-LITOFF" to case "RW-2026-000654" with type "GUARANTOR_NOTICE" at item version 3
    When the DecisionRecorded fact of that resolve reaches rwb.decision-record.v1
    Then one entry exists with approverUserId "TEST-LIT-01", the match method "PERSON", finalCall "ATTACHED" and the document reference of the resolve
    Then the entry of a person's attach carries an approver and the entry of AC1 carries none, and both are readable beside each other for the case

  Scenario: AC4 One record per document, however often the fact arrives (new, D-RCV-60)
    Given 15 intake items of a business date are already "MATCHED" and their 15 DOCATT entries exist
    When JOB-12 runs again over the same items, the same file arrives in a second intake item with the same hash, and two reviewers attach the same item at version 3
    Then no second decision_log_entry is written for any of the 15 documents and the count for the case stays as it was
    Then the first entry's ID is returned for the repeated fact and the repeat count is incremented for R-UNI-40
    Then the chain of the case is unchanged and GET /api/recovery/decision/v1/decision-log returns the same entries in the same order

  Scenario: AC5 A record that cannot be written stops the attach (new, D-RCV-60)
    Given the rwb-document contract mock returns three items of case "RW-2026-000123"
    Given the decision-record library fake is forced to fail the record write
    When the store asks for the three records of the three items inside its transaction
    Then the call returns status 503 with "MSG-P7-003" and no item is accepted
    Then no decision_log_entry exists for any of the three items and no chainSeq is used
    Then no document row is written for the three items, the automatic item stays "PENDING" for the next run, and an incident is raised

  Scenario: AC6 A held item, or a refused attach, leaves no record (new, D-RCV-60)
    Given a scan with no readable case ID and no readable account number, a scan of account "TEST-ACC-0003" linked to open cases "RW-2026-000321" and "RW-2026-000654", a scan whose case ID and account point to different cases, a scan of the closed case "RW-2026-000789", a scan with review_reason "UNKNOWN_TYPE", and a resolve refused with 422 for type "PAYSLIP"
    When intake completes for the six items and the resolve is refused
    Then no DOCATT entry exists for any of the seven and no chainSeq is used
    Then the item statuses "NO_MATCH", "MULTIPLE", "CONFLICT", "CASE_CLOSED" and "NO_TYPE" stay on the items in rwb_document
    Then GET /api/recovery/decision/v1/decision-log for the cases returns no entry for any of them

  Scenario: AC7 The records are read by case and by entry, and a role without the right is refused (new, D-RCV-60)
    Given the entries of AC1 and AC3 exist and the documents of case "RW-2026-000123" on the document contract
    When an auditor holding "RW-AUDIT" reads the entries of the case and one entry, and the completeness checker compares the documents with the entries of the case
    Then the reader sees the entries in chain order with the document reference, the classifier version, the confidence, the match method, the approver where one decided, the final call and the message id of a refusal if any
    Then the checker reports no gap for the case, and reports a document with no entry as a gap for a case where the mock holds one
    When a role holding Documents R only, and no right in the decision log, calls either operation
    Then the answer is 403 with "MSG-P4-002", and a case out of the caller's scope answers 403 with "MSG-P4-003", and no row is returned

  Scenario: AC8 The record cannot be changed or deleted, and the chain holds (new, D-RCV-60)
    Given one entry of AC1 with its chainSeq, its prevHash and its entryHash and a second entry of the same case after it
    When an UPDATE setting final_call and a DELETE of the first entry are attempted through the rwb-decision login (DP-02) and again through the schema owner role
    Then all four statements are refused, the first two by the missing grant for the service login and the last two by the append-only rule of the table
    Then the first entry is unchanged and its entryHash still equals the SHA-256 of its canonical form
    Then the prevHash of the second entry equals the entryHash of the first, and the prevHash of the first entry of the chain is 64 zeros
    Then the refused attempts are written to the ACE audit log with the table, the operation and the entry ID

  Scenario: AC9 No OCR text and no personal value in the record, the fact, the outbox or the logs (new, D-RCV-60)
    Given the entries, the DecisionRecorded payloads and the log lines of AC1 to AC3
    When they are inspected
    Then they carry the case reference, the document reference, the intake item ID, the decision code, the classifier version, the confidence, the match method, the approver reference, the final call and dates only
    Then no OCR page text, no file byte and no account number of "TEST-ACC-0001" or "TEST-ACC-0002" appears in any of them
    Then the text and the file stay in rwb_document behind the masked read of the item
```

These nine criteria are new for the `rwb-decision` slice of RWB-E1-032 and are the record and read criteria of the key. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key matches, stores, holds or refuses a document, and those changes belong to RWB-P5-E1032-APP, RWB-P4-E1032-APP and RWB-P3-E1032-APP. The values are the legacy values of RWB-E1-032 — cases `RW-2026-000123`, `RW-2026-000456`, `RW-2026-000789`, `RW-2026-000321`, `RW-2026-000654`, accounts `TEST-ACC-0001`, `TEST-ACC-0002`, `TEST-ACC-0003`, classifier version `CLS-1.0`, confidences 0.93, 0.88 and 0.62, threshold 0.80, reviewer `TEST-LIT-01` with role `RW-LITOFF`, item version 3, the 15 `MATCHED` items, the types `COURT_NOTICE`, `DEMAND_LETTER`, `APPRAISAL_REPORT`, `TITLE_DEED`, `GUARANTOR_NOTICE` and `PAYSLIP`, and the messages MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-P4-003, MSG-P5-003, MSG-P5-006 and MSG-GEN-004 — and no new business value is introduced.

The decision code `DOCATT` and the match methods `CASE_ID`, `ACCOUNT_NO` and `PERSON` are the legacy values; whether the code list in force carries `DOCATT` has no source and is carried in GAP-2445 with ASM-4053. The final call `ATTACHED`, the payload field set of the fact and of the entry, the read shape, the parameter names and the login name have no source and are carried in GAP-2444, GAP-2447 and GAP-2449 with ASM-4052, ASM-4055 and ASM-4057.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document the OCR intake attaches, automatically or by a reviewer, leaves exactly one decision record; no attach stands without it | Legacy BR1 and BR5; R-UNI-39; FSD P7 v3 A2.2; FEAT-DRI-02 |
| BR2 | The record is written on the decision-record path of DP-03: it is appended to the chain, it names the rule and the rule version in force, and the entry, its chain position and its outbox row commit together or not at all | FSD P7 v3 A2.1 and A2.3; TSD P7 v2 T5.3; DP-03 |
| BR3 | The entry names the case, the decision code `DOCATT`, the document reference, the intake item, the classifier model version, the confidence, the match method, the approver where a person decided, the inputs reference, the final call and the decided time | Legacy AC1, AC10 and AC12; TSD P7 v2 T3.1; ASM-4052 and ASM-4055 |
| BR4 | A record that cannot be written refuses the attach: the library raises `DecisionLogUnavailableException`, the store's transaction rolls back, the automatic item stays `PENDING`, the manual attach answers MSG-P7-003 and an incident is raised | Legacy X13 and TC-E1-032-17; FSD P7 v3 VR-P7-001-2 and AC-EXC-P7-002-02; principle 5 |
| BR5 | The entry is append only and hash chained: an UPDATE and a DELETE are refused, a correction is a new entry naming the one it corrects in `corrects_entry_id`, and every `entry_hash` is the SHA-256 of the entry's canonical form | FEAT-DRI-01; FSD P7 v3 AC-P7-001-01 and AC-ALT-P7-001-01; NFR-035 |
| BR6 | An item that is held as no match, multiple, conflict, a closed case or no agreed type, and an attach refused for its type, its scope or its version, leaves no record, because no document was stored and no attach decision was taken | Legacy BR3 and section 9; the reading is Not specified in the source documents (GAP-2446; ASM-4054) |
| BR7 | The service applies no match rule: the patterns, the threshold, the outcomes and the store's review rule are `rwb-document`'s, and the entry copies their outcome | Legacy BR2 and BR4; FSD P4 v3 A2.4; DP-01 |
| BR8 | One entry per stored document under a repeated fact, a repeated file or two reviewers: the inbox dedupe, the idempotency key and the partial unique key on the document reference make a second entry impossible, and the repeat is counted | Legacy BR6, AC8 and AC9; R-UNI-40; FEAT-DRI-02 |
| BR9 | The record is written before the document stands, in one transaction with its chain position and its outbox row; a failed append leaves nothing and the fact is redelivered | Legacy BR5; R-UNI-39; DP-03 |
| BR10 | The story records and exposes; it writes no document, no intake item, no review item and no case status, and it reads no table of another service | Architecture v5 slides 14 and 41; DP-01 |
| BR11 | The two reads declare the `DECISION_LOG` capability area and the right `R` with the scope applied; a role without the right is refused with MSG-P4-002 and a case out of scope with MSG-P4-003 | TSD P7 v2 T-A.1 and T6.1; legacy section 10 and AC13 |
| BR12 | The ledger is reconciled: the documents of a case are compared with the `DOCATT` entries of the case inside the ingest window, and a document with no entry is reported as a gap and alerted; no entry is invented for it | Architecture v5 slide 28; NFR-035; ASM-4058 |

Target-service statements that make the rules hold in `rwb_decision`:

- BR1 and BR2 are one append on the `DecisionRecorded` fact of the owning service through the library of DP-03; the store's transaction is `rwb-document`'s and this story supplies the path, its fail-closed contract and its exception.
- BR3 is the entry composition: the columns of TSD P7 v2 T3.1 plus the document reference, the intake item, the match method and the confidence of the assumed shape of ASM-4055; `model_version` carries the classifier version and `recommendation` carries the type candidates.
- BR4 is the exception mapping: `DecisionLogUnavailableException` becomes MSG-P7-003 for the attach and an incident for the platform administrator queue.
- BR5 is the table's trigger `tr_declog_append_only` and the missing `UPDATE` and `DELETE` grant on the service login, inherited from the decision-log baseline of RWB-P7-E1008-APP.
- BR6 is the absence: the listener has no path that writes an entry without a stored document reference, and a fact with no document reference is refused as X6.
- BR8 is the partial unique key on the document reference and the inbox dedupe by event ID and idempotency key.
- BR11 is the guard inherited from the decision-log baseline's authorise path; the Java code holds no role, no scope and no delegation row.
- BR12 is the checker of flow step 10: one read of the document contract per case per window, one comparison, one gap alert.

### 9. State transitions

None for a document, an intake item, a review item, a task or a case; the intake item's `match_status` moves PENDING to MATCHED, or to a held value, in `rwb-document` and under RWB-P5-E1032-APP (legacy section 9). The states below are the states of an entry of this story, and an entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A `DecisionRecorded` attach fact arrives with a document reference | The decision code, the rule version and the match method are readable at the version in force | Appended, with the next `chain_seq`, its `prev_hash` and its `entry_hash`, in one transaction with its outbox row |
| Absent | A `DecisionRecorded` attach fact arrives | The decision code is unknown, or the match method or the document reference is absent | Absent: refused with MSG-P7-009 or MSG-GEN-006, and nothing is written |
| Absent | A `DecisionRecorded` attach fact arrives | The library is unavailable or the chain cannot be taken | Absent: the attach is refused with MSG-P7-003, nothing is stored, and the fact stays for redelivery |
| Absent | No attach fact arrives, because the item is held or the attach was refused | The store wrote no document | Absent: no entry and no chain position (BR6) |
| Appended | The same fact arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A correction of the record is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`, and the corrected entry stays unchanged |
| Appended | An UPDATE or a DELETE is attempted | Any caller, including the schema owner | Unchanged: the statement is refused by the append-only rule |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-OCR, the OCR and extraction pipeline | Its attach is recorded: the entry names it as the actor of an automatic attach |
| SY-DECLOG, the decision log writer | Appends the entry through the library; writes no document |
| RW-LITOFF and RW-CASEOWN, reviewers with Documents `C` | Their attach is recorded with them as approver and the match method `PERSON`; they read the entries of the cases in their scope |
| RW-LEGAL, role with scope `ALL` | Reads the entries of any case, including the items that no candidate named |
| RW-AUDIT and RW-COMPLY | Read the `DOCATT` entries of a case and one entry with its versions and its chain position (`DECISION_LOG` R) |
| RW-TEAMMGR and the other roles of TSD P7 v2 T6.1 | Hold `R` on the decision log and read the entries of the cases in their scope; no attach |
| A role holding Documents R only, or a role outside the matrix | Refused with MSG-P4-002; a case out of scope is refused with MSG-P4-003 |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, and appends the entry and its outbox row (DP-02) |
| `rwb-document` | Owns the match, the store, the review queue and the reviewer's `resolve`; this story holds no authority over any of them |
| `rwb-access` | Owns the Documents right, the scope answer and the masking; this story consumes the answer for its reads |
| `rwb-case` | Owns the case, the open cases of an account and the reference and parameter rows this story reads through DP-06 and DP-07 |
| No approval level from the delegation of authority applies to an automatic attach | It is a system decision and carries no approver; a reviewer's attach names the reviewer and no level, and whether a level is recorded is Not specified in the source documents (GAP-2444; ASM-4052) |

The authorisation decision behind the two reads is `rwb-access`'s role, scope and right data, taken through the authorise contract of DP-11 and the guard the decision-log baseline already carries; this story adds no guard of its own. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-2449; ASM-4057).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id (the case of the attach) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code (`DOCATT`) | Write |
| DF-DEC-004 | `decision_log_entry` | rule_id (the rule that decided the match, where one is named) | Write where the fact names one |
| DF-DEC-005 | `decision_log_entry` | rule_version (the version of that rule) | Write with the rule id, never alone |
| DF-DEC-006 | `decision_log_entry` | model_version (the classifier version, for example `CLS-1.0`) | Write |
| DF-DEC-007 | `decision_log_entry` | agent_version | Not written: no agent decides an attach |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the intake item and the fields read) | Write |
| DF-DEC-009 | `decision_log_entry` | recommendation (the document type and its candidates) | Write |
| DF-DEC-010 | `decision_log_entry` | approver_user_id (the reviewer of a manual attach) | Write on a manual attach only |
| DF-DEC-011 | `decision_log_entry` | approval_level | Not written: a reviewer's attach carries no delegation level in any source |
| DF-DEC-012 | `decision_log_entry` | final_call (`ATTACHED`) | Write |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written: there is no override of an attach |
| DF-DEC-014 | `decision_log_entry` | actions (the document reference, the intake item and the match method) | Write |
| DF-DEC-015 | `decision_log_entry` | outcome (the stored document state named by the fact) | Write where the fact names one |
| DF-DEC-016 | `decision_log_entry` | decided_at (the receipt and attach time) | Write |
| DF-DEC-017 | `decision_log_entry` | prev_hash | Write |
| DF-DEC-018 | `decision_log_entry` | entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id (the reviewer, or the identity of the pipeline) | Write |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write |
| (assumed column) | `decision_log_entry` | object_ref (the document ID), intake_item_id, match_method, confidence, message_id | Write; the columns are Not specified in the source documents (GAP-2444; ASM-4052) |
| DF-DOC-001, DF-DOC-002, DF-DOC-004, DF-DOC-006, DF-DOC-010 | `document` (P5) | id, case_id, document_type, storage_ref, write_once | Read through the document contract of RWB-P5-E1032-CON, never a table |
| DF-DOC-007, DF-DOC-008 | `document` (P5) | classification_confidence, review_status | Named on the entry as facts |
| DF-DOC-060, DF-DOC-061, DF-DOC-075, DF-DOC-076 | `document_intake` (P5) | case_id, document_id, match_status, candidate_case_ids | Read as facts of the document contract |
| DF-DOC-070, DF-DOC-073, DF-DOC-080 | `document_intake` (P5) | predicted_type, classifier_version, review_reason | Named on the entry as facts |
| (reference lists) | reference data (P3) | the decision code list with `DOCATT` and the approval level list, at the version in force | Read through the reference-data contract of DP-07, never a table |
| (parameters) | `parameter_value` (P3) | the ledger ingest target and the chain-check time, at the version in force | Read through the parameters contract of DP-06, never a table |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_decision` | the append row | Write |

No row of `document`, `document_intake`, `document_text`, `document_type`, `document_hub_parameter`, `recovery_case`, `case_account`, `role`, `permission` or `masking_rule` is copied into `rwb_decision`: the attach facts arrive on the document contract and on `rwb.decision-record.v1`, and no other service's table is queried (DP-01). Field IDs are those of the Logical Data Model and Data Dictionary v9; the document reference, the intake item, the match method, the confidence and the message id have no field ID in TSD P7 v2 T3.1 and are written from the assumed shape of section 12.1.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007); this story fills them with the `DOCATT` entries of an attach and adds no third path. The request and response field set of an attach entry is Not specified in the source documents (GAP-2444; ASM-4052).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the decision log by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and by the document or intake item reference of an attach; 200 with the DecisionLogPage | `DECISION_LOG`, right `R`, scope applied through the authorise contract | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs reference, its versions, its document reference, its match method, its final call and its hash chain; 200 with the DecisionLogEntry | `DECISION_LOG`, right `R`, scope applied | Not applicable, read only |

The `DecisionLogEntry` body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `modelVersion`, `agentVersion`, `inputsRef`, `recommendation`, `approverUserId`, `approvalLevel`, `finalCall`, `objectRef`, `intakeItemId`, `matchMethod`, `confidence`, `messageId`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`. The `DecisionLogPage` body carries `items`, `page`, `size` and `total`.

Errors: 401 no session; 403 the role lacks the right (MSG-P4-002) or the case is out of scope (MSG-P4-003); 404 the entry is absent; 422 a query value is outside its list (MSG-GEN-001); 503 the log is unavailable (MSG-GEN-006) or the append could not be made (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document, on RWB-P5-E1032-CON | The documents a case holds with their type and review state, for the completeness check of the ledger (BR12, X9); faked, one hop and 2 s (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access, on RWB-P4-E1037-CON | The role, scope and right decision behind the two reads: area `DECISION_LOG`, right `R` (BR11); faked. The contract is added by the DP table and is not in the metadata rows (GAP-2448; ASM-4056) |

The reference lists and the parameters of `rwb-case` (DP-07, RWB-P3-E1043-CON; DP-06, RWB-P3-E1042-CON) are read in process through their client libraries with their fakes and are not cross-service REST rows; the attach facts arrive on `rwb.decision-record.v1` and not over REST.

#### 12.3 Events published

None. This story publishes no event of its own: the attach fact is `rwb-document`'s and the entries of the central ledger are read through the operations of 12.1. `DecisionRecorded` on `rwb.decision-record.v1` is published by the owning service of each decision, and `rwb-decision` is its consumer. The `ApprovalRequested`, `ApprovalDecided` and the rule-registry events of `rwb.decision.events.v1` belong to the approval and rule stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by `rwb-document` for this key | `IntakeAttachDecisionListener`: inbox dedupe by event ID, then `IntakeAttachDecisionRecorder` and `DecisionLogAppender` for the case, the document reference, the intake item, the match method, the classifier version, the confidence, the approver, the final call and the message id |

The fact carries IDs, codes, versions, a confidence, a message id and a time only; no OCR text, no file and no account number travels on the topic (AC9, section 17). Which fields of the fact this service requires, and whether the document reference travels on the fact or is read through the document contract, is Not specified in the source documents (GAP-2447; ASM-4055).

#### 12.5 Workflows and activities

None of this story's own. The append is a transactional write on the consumer path and not a workflow step: the handler is a Kafka consumer with the inbox of DP-09, and the store's `matchStep` and `DocumentIntakeWorkflow` on queue `rwb-document` are `rwb-document`'s (RWB-P5-E1032-CON section 12.5). This story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit of DP-10.

#### 12.6 Schedules

None. The intake of a scan is JOB-12's, every 15 minutes in business hours, and after DP-10 it is a Temporal Schedule of `rwb-document`; this story neither owns that Schedule nor creates one. The daily hash-chain check JOB-14 at 02:00 is the decision-log baseline of this service and covers the entries of this story like any other. Whether the completeness check of flow step 10 runs on its own timer or on the ingest window is Not specified in the source documents (GAP-2450; ASM-4058); the reading applied is that of ASM-4058 and it creates no Schedule.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The attach entry, its document and intake item references, its versions, its chain position, its hashes and its final call; append only |
| decision record (local library) | P7 rows in `rwb_decision`, written through the decision-record library | The append of DP-03 and its hash chain |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `document`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` (P5), `recovery_case`, `case_account`, `task`, `timer` and `parameter_value` (P3), and `role`, `permission` and `masking_rule` (P4). The other P7 tables — `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` — are not touched by this story. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document intake-match WireMock | RWB-P5-E1032-CON | The notice of case `RW-2026-000123` at `0.93` with `CLS-1.0` and method `CASE_ID`; the demand letter of `TEST-ACC-0002` at `0.88` with method `ACCOUNT_NO`; the appraisal at `0.62` with candidates `APPRAISAL_REPORT` and `TITLE_DEED`; the `MULTIPLE` item of `RW-2026-000321` and `RW-2026-000654` resolved by `TEST-LIT-01` to `RW-2026-000654` with `GUARANTOR_NOTICE`; the held items of AC6; the 15 `MATCHED` items of the repeat run; the three-item sync of the forced record failure; and the document list of a case for the completeness check |
| rwb-access authorise fake | RWB-P4-E1037-CON, DP-11 | The allow answer for `DECISION_LOG` right `R` in scope, the refusal of a role without the right with MSG-P4-002, and the refusal of a case out of scope with MSG-P4-003 |
| rwb-case reference-data fake | RWB-P3-E1043-CON, DP-07 | The decision code list with `DOCATT` in force, the approval level list, and an unknown code for X5 |
| rwb-case parameters fake | RWB-P3-E1042-CON, DP-06 | The ledger ingest target and the chain-check time with the version in force, and an unavailable answer for the retried fact |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, `prev_hash` and `entry_hash`, the SHA-256 of the canonical form, the append-only refusal, and the forced failure that raises `DecisionLogUnavailableException` for AC5 and TC-E1-032-17 |
| outbox and inbox library fake | RWB-PLT-TE006-CON | The `DecisionRecorded` fact of each scenario, its replay under the same event ID and idempotency key, and the outbox row of the append |
| gateway-bff route fake | RWB-PLT-N001-CON | The route the reader of a case reaches the two operations through, so the refusals can be asserted |

Each fake is replaced by the real service as RWB-P5-E1032-APP, RWB-P4-E1032-APP and RWB-P3-E1032-APP land, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the document list and the authorise decision consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the intake Schedule and the intake workflow are `rwb-document`'s |
| File | None | No file input and no file output; a scan never leaves `rwb-document` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/intakeattach`, Java package `th.co.scb.ace.workbench.recovery.decision.intakeattach`.

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

Which patterns have an instance in this slice: DP-01 is the boundary — the entry lives in `rwb_decision` and the attach facts arrive on the document contract and on `rwb.decision-record.v1`, never as a read of `rwb_document`; DP-03 is the append path with its chain, its append-only rule and its fail-closed exception; DP-05 is applied by removal — the legacy `CaseDirectory` read of `v_ace_account` is gone, and the case and the account number arrive as facts on the fact and on the document contract; DP-06 is the ingest target and the chain-check time read as parameters; DP-07 is the decision code list and the approval level list read as reference data; DP-09 is the outbox, the inbox and the idempotency key; DP-10 is named because the intake trigger becomes a Temporal Schedule of `rwb-document` and this slice is event-started, holding no workflow of its own; DP-11 is the document read of the completeness checker and the authorise decision behind the reads, each with a mock and a 2 s timeout; DP-15 is the one migration; DP-19 is the composite route the reads are reached through, not built here.

The platform H dependencies in the table — H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON — and the C dependencies of the published contracts of other services — C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the authorise contract RWB-P4-E1037-CON that DP-11 consumes — are not in the metadata rows of this story, which name `Depends on (build)` = None and `Contract dependencies` = RWB-P5-E1032-CON. They are the dependencies the DP table adds and they are recorded in GAP-2448 and ASM-4056. None of them blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and published contracts of `rwb-case`, `rwb-access` and `rwb-document`, built against their fakes.

The work of the legacy key that sits with other slices: the `matchStep` of JOB-12, the `CaseMatcher` with its five outcomes, the store and the duplicate check on the file hash, the `review_status` and `write_once` rule, the `rwb-docs` container, the four intake operations, the `resolve` of a reviewer, the `DocumentAttached` event and the SCR-31 Unmatched list are `rwb-document`'s (RWB-P5-E1032-APP, RWB-P5-E1032-CON). The Documents right, the scope answer and the masking are `rwb-access`'s (RWB-P4-E1032-APP). The case, the open cases of an account number, the reference lists and the parameters are `rwb-case`'s (RWB-P3-E1032-APP). This story builds the record of the attach and nothing beside it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntakeAttachDecisionListener | Kafka consumer with the inbox | Reads `DecisionRecorded` for an attach, deduplicates by event ID and idempotency key, and hands the decision facts to the recorder |
| IntakeAttachDecisionRecorder | Service | Composes the entry from the attach facts, reads the decision code list and the ledger parameters at the version in force, and decides nothing about the match (BR3, BR7) |
| DecisionLogAppender | Service | Takes the next `chain_seq`, computes `prev_hash` and `entry_hash`, and writes the entry and its outbox row in one transaction (DP-03, BR2, BR9) |
| DecisionRecordFailClosedHandler | Service | Maps the library's `DecisionLogUnavailableException` to MSG-P7-003 for the attach and to an incident, so the store's transaction rolls back and nothing is stored (BR4) |
| IntakeAttachCompletenessChecker | Service | Compares the documents of a case from the document contract with the `DOCATT` entries of the case inside the ingest window and reports a document with no entry as a gap (BR12) |
| DecisionLogQueryController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the declared area and right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, with the append-only rule, the chain columns, the document reference and the idempotency key |
| DocumentFactClient | Adapter | The document list of RWB-P5-E1032-CON for the completeness check, one hop with a 2 s timeout and a breaker |
| AccessCheckClient | Client | The cached authorise decision behind the two reads (DP-11) |
| ReferenceAndParameterClient | Client | The decision code list, the approval level list, the ingest target and the chain-check time at the version in force (DP-06, DP-07) |

**Database and migrations**

- Writes `decision_log_entry`, the local decision record of the append and the library objects, all in schema `rwb_decision`; reads no other schema (DP-01).
- Migration in this story, in the per-service Flyway sequence of `rwb_decision`: `V1032_1__decision_intake_attach_entry.sql` adds the attach columns of section 11 that the decision-log store baseline does not hold — the document reference, the intake item, the match method, the confidence and the message id — plus the partial unique key `ux_declog_intake_attach ON decision_log_entry (object_ref) WHERE decision_code = 'DOCATT' AND object_ref IS NOT NULL`, so one entry per stored document is a constraint and not only a check (BR8), and the search index for the case-and-decision read of 12.1. The column names and types are Not specified in the source documents (GAP-2444; ASM-4052).
- The append-only rule is the table's, with the trigger `tr_declog_append_only` that refuses an UPDATE and a DELETE from the schema owner and the missing grant for the service login, as FSD P7 v3 AC-P7-001-01 fixes it.
- No row of `document`, `document_intake`, `document_type` or `parameter_value` is written here: the document hub's tables and the case's parameters are their owners'.

**Configuration and reference data**

- The decision code list with `DOCATT` and the approval level list are reference data of `rwb-case` read through DP-07 at the version in force; the value `DOCATT` and the final call `ATTACHED` are the reading of ASM-4052 and ASM-4053 and are held as reference rows, not as constants (GAP-2444; GAP-2445).
- The ledger ingest target of 5 minutes and the daily chain-check time of 02:00 are parameter rows of `rwb-case` read through DP-06 with the version in force; the parameter names are Not specified in the source documents (GAP-2449; ASM-4057).
- The match parameters `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN` and `CLASSIFY_THRESHOLD` are the store's rows; this story reads none of them (BR7).
- The outbox retry policy, the inbox retention and the chain-check alert route are the platform's (RWB-PLT-TE006-CON).

**Build steps**

1. `DecisionLogRepository` and the migration, with the partial unique key on the document reference and the append-only trigger; test that a second entry for the same document and an UPDATE are both refused (AC4, AC8).
2. `IntakeAttachDecisionListener` with the inbox and the dedupe by event ID and idempotency key; test the replay of the same fact (AC4).
3. `IntakeAttachDecisionRecorder` and `ReferenceAndParameterClient`: the entry composed from the attach facts with the versions in force, and the refusal of an unknown decision code and of a rule id with no version (X5; AC1 to AC3).
4. `DecisionLogAppender` and the chain: `chain_seq`, `prev_hash`, `entry_hash` over the canonical form, the first `prev_hash` of 64 zeros, and the one-transaction append (AC1, AC8).
5. `DecisionRecordFailClosedHandler`: the `DecisionLogUnavailableException` path to MSG-P7-003 with the store's rollback and the incident; test the three items of AC5 with the library fake forced to fail (AC5, TC-E1-032-17).
6. The absence path of AC6: a fact with no document reference, and a held item that produces no fact, leave no entry and no chain position.
7. `DecisionLogQueryController` with the two operations, the declared area and right, the scope, the paging and the problem mapping; tests for AC7 and the refusals of TC-E1-032-16.
8. `IntakeAttachCompletenessChecker` over the document list of a case, with the gap report of X9 and the ingest window of DP-06.
9. The contract-fake run of the whole slice: the document fake, the access fake, the reference-data and parameters fakes, the decision-record fake and the outbox fake, green from Day 1 (AC1 to AC9).
10. The boundary test: no write to `rwb_document`, `rwb_case` or `rwb_access`, and no OCR text, file or account number in any entry, fact, outbox row or log line (AC9).

**Feature switch.** None of its own, and the record path must have no off state: an attach that cannot be recorded must not be stored, so a switch that silenced the record would break BR4. The legacy flag `rwb.dochub.autoattach` stays `rwb-document`'s; with it off every classified item is held, no automatic attach fact arrives, and a reviewer's attach still leaves its record (GAP-2444; ASM-4052).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P5-E1032-CON stay green, and a SIT day shows one `DOCATT` entry per attached document with its classifier version, its confidence, its match method and its approver where a person decided; no entry for a held item or a refused attach; a chain with no break and no entry changed or deleted; an attach refused with MSG-P7-003 when the record cannot be written; both reads answering by case and by entry; and not one document, intake item, review item or case status changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The record of the attach cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the fail-closed handler; the legacy text is copied unchanged |
| MSG-P7-009 | An entry has an unknown decision code, or a rule id with no version | Not specified in the source documents (GAP-2444; ASM-4052) | This story, on the append, naming `decisionCode` or `ruleVersion` |
| MSG-P4-002 | The role holds no right in the `DECISION_LOG` area | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of the read |
| MSG-P4-003 | The entry or the case is outside the caller's scope | This case is not in your scope. | This story, through the authorise answer of the read |
| MSG-GEN-001 | A query value is outside its list, or a required field of the entry is absent | Enter {field}. | This story, on the read and on the append |
| MSG-GEN-006 | The log, the reference list or the parameters are unavailable, or the fact names no document | Not specified in the source documents (GAP-2444; ASM-4052) | This story, on the read, on the retried fact and on the gap report |
| MSG-P5-003, MSG-P5-006, MSG-GEN-004 | An item is held, a type is not in force, or the item changed under a second reviewer | The legacy texts of RWB-E1-032 section 14 | `rwb-document`, on the item; this story records the message id only where the fact names one |

MSG-P7-003, MSG-P4-002 and MSG-P4-003 are copied unchanged from the FSD P7 v3 message set and the platform messages the authorise contract carries; MSG-P5-003, MSG-P5-006 and MSG-GEN-004 are the legacy texts and are produced by `rwb-document`, not here. The texts of MSG-P7-009 and MSG-GEN-006 are named by the FSD P7 v3 exception flows but are not written out in a source this story may read, so the placeholders stand. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by the decision-log view of a case and by the decision screen SCR-11 of this service, which are served through the gateway-bff composite route of DP-19 and are another story's; SCR-30 Case documents and SCR-31 Document review queue stay `rwb-document`'s, and the Unmatched list with its scan viewer, OCR text, candidates and pickers belongs to RWB-P5-E1032-APP.

| Where | State | What the reader sees |
|---|---|---|
| The decision-log read (P7) | List | The `DOCATT` entries of the case in chain order, with the document reference, the type, the classifier version, the confidence, the match method, the approver where one decided and the final call |
| The entry read | One entry | The same row with its inputs reference, its `decidedAt`, its `prevHash` and its `entryHash` |
| The entry read | An entry of a reviewer's attach | `matchMethod` `PERSON`, the reviewer as approver and the document reference |
| The read | A held item | No row: the hold is shown by the Unmatched list on SCR-31, not here |
| The read | 403 or 404 | MSG-P4-002 for a role without the right, MSG-P4-003 for a case out of scope, and the not-found answer for an absent entry; no row is returned |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-032-17 | AC5, BR4 | NFR | Decision-record write forced to fail during an automatic and a manual attach; nothing stored, MSG-P7-003, no entry and no chain position used, incident raised |
| TC-E1-032-16 | AC7, BR11 | Component | A role holding Documents R only (RW-TEAMMGR) calls either read and is refused with MSG-P4-002 through the rwb-access fake; a case out of scope answers MSG-P4-003 and no row is returned |
| TC-E1-032-01 | AC1, BR1, BR3 | Contract | Synthetic notice with `RW-2026-000123` at 0.93 by `CLS-1.0`, method `CASE_ID`; one entry with the document reference, the model version and the confidence |
| TC-E1-032-02 | AC6, BR6 | Contract | A scan with no identifiers; no entry and no chain position, and the item keeps `NO_MATCH` |
| TC-E1-032-03 | AC6, BR6 | Contract | Account `TEST-ACC-0003` on two open cases; no entry for the `MULTIPLE` item |
| TC-E1-032-04 | AC2, BR3 | Contract | Account `TEST-ACC-0002` only; one entry with method `ACCOUNT_NO` and case `RW-2026-000456` |
| TC-E1-032-05 | AC6, BR6 | Contract | Case ID and account on different cases; no entry for the `CONFLICT` item |
| TC-E1-032-06 | AC6, BR6 | Contract | Case ID `RW-2026-999999`; no entry for the `NO_MATCH` item |
| TC-E1-032-07 | AC6, BR6 | Contract | Closed case `RW-2026-000789`; no entry for the `CASE_CLOSED` item |
| TC-E1-032-08 | AC4, BR8 | Contract | The same file in two intake items; one entry, keyed on the first document reference |
| TC-E1-032-09 | AC4, BR8 | Component | 15 items already `MATCHED` and a repeat run; no second entry, the entry count unchanged and the chain unchanged |
| TC-E1-032-10 | AC1, BR3 | Contract | A document at 0.62 with candidates `APPRAISAL_REPORT` 0.62 and `TITLE_DEED` 0.30; one entry with the confidence 0.6200 and the type, and the review state left in `rwb_document` |
| TC-E1-032-11 | AC6, BR6 | Contract | An item with review_reason `UNKNOWN_TYPE`; no entry for the `NO_TYPE` item |
| TC-E1-032-12 | AC3, BR3 | Contract | Reviewer `TEST-LIT-01` attaches a `MULTIPLE` item at version 3 with type `GUARANTOR_NOTICE`; one entry with `PERSON` and the reviewer as approver |
| TC-E1-032-13 | AC7, BR11 | Component | A resolve or a read on a case outside the caller's scope; 403 with MSG-P4-003 and no entry |
| TC-E1-032-14 | AC6, BR6 | Component | A resolve with type `PAYSLIP` refused with 422 and MSG-P5-006; no entry |
| TC-E1-032-15 | AC4, BR8 | Component | Two parallel attaches at version 3; one document and one entry, the second request refused with 409 and MSG-GEN-004 |

The legacy level System maps to Contract or Component as the row shows, Access to Component and Resilience to NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Every case is asserted on the record side of this story: the entry, its document reference, its versions, its match method, its approver, its final call, its chain and its two reads; the match, the store, the intake and the review are the document contract fake's. The `-ITG` copies of these cases belong to RWB-ITG-E1032-ITG and are not written here.

### 17. Guardrails

- No business value in code: the decision code, the final call, the match methods, the approval levels, the ingest target and the message ids are reference rows, parameter rows or facts of another service; nothing of them is a constant here.
- No personal data in the entry, the fact, the outbox, the tests or the logs: the case reference, the document reference, the intake item, the decision code, the classifier version, the confidence, the match method, the approver reference, the final call and dates only. OCR page text, file bytes and account numbers stay in `rwb_document`, and a test scans the entry, the fact and the log line for the account numbers of the scenarios.
- No read of another service's tables (DP-01): the attach facts arrive on the document contract and on `rwb.decision-record.v1`, the authorise answer on its contract, the reference lists and parameters in process; no `document`, `document_intake`, `document_text`, `recovery_case`, `case_account`, `role`, `permission`, `masking_rule` or `parameter_value` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views (DP-05): this story reads no ACE data at all, and the account number arrives as a fact of the intake.
- One recorder and no mover: this story changes no document, intake item, review item or case status, so a decision record can never move a case (BR10).
- No attach without its record and no record without a stored document: the entry, its chain position and its outbox row commit in one transaction, and a store transaction that cannot record its decision refuses the attach (BR4, BR9).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, and the chain is verifiable from `chain_seq` 1 (BR5).
- One entry per stored document: the partial unique key on the document reference, the inbox dedupe and the idempotency key make a second entry impossible (BR8).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own.
- One hop and 2 s on every call with a breaker per downstream; a missing document fact, reference list or parameter never produces an entry from a guessed type, code or version (DP-11).
- The record path has no off switch, because an attach that cannot be recorded must not stand.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-007 | A classified document attaches to its case without a person | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-032-01 to TC-E1-032-15 |
| REQ-DCM-005 | An uncertain match is held for a person | Business Requirements Epic 1, section 3.5 | FEAT-DCM-12 | 13 Manage documents and correspondence | R-UNI-40 | TC-E1-032-02 to TC-E1-032-07, TC-E1-032-11 |
| REQ-DRI-004 | Every decision is recorded before it takes effect | Business Requirements Epic 1, section 3.5 | FEAT-DRI-02 | 13 Manage documents and correspondence | R-UNI-39 | TC-E1-032-16, TC-E1-032-17 |

| Legacy reference | Where it is kept |
|---|---|
| One `DOCATT` entry per attach, carrying the classifier version, the confidence and the match method | Sections 1, 2, 4, 7 (AC1, AC2), 8 (BR1, BR3), 13 |
| The reviewer's attach recorded with the reviewer as approver and the method `PERSON` | Sections 1, 4 step 8, 7 (AC3), 8 (BR3), 10 |
| An item held, or an attach refused, leaves no record | Sections 5 (X3, X4), 7 (AC6), 8 (BR6), 9, 16 |
| A record that cannot be written refuses the attach, with MSG-P7-003 and an incident | Sections 1, 4 step 7, 5 (X1), 7 (AC5), 8 (BR4), 14, 16 (TC-E1-032-17) |
| Append only, the hash chain and the refusal of an UPDATE and a DELETE | Sections 7 (AC8), 8 (BR5), 9, 13 |
| No OCR text, no file and no account number in the record, the fact or the logs | Sections 7 (AC9), 11, 17 |
| The roles of the legacy section 10 and the decision-log right `R` of TSD P7 v2 T6.1 | Sections 7 (AC7), 10, 12.1 |
| Messages MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-GEN-006 and the item messages MSG-P5-003, MSG-P5-006, MSG-GEN-004 | Section 14, exception paths |
| Rule IDs R-UNI-39 and R-UNI-40, and the measure `Decisions within the delegation of authority` | Sections 1, 2, 4, 5, 8 |
| Legacy key RWB-E1-032, story RWB-P7-E1032-APP, contract RWB-P5-E1032-CON | Metadata, sections 3, 12 |
| Test cases TC-E1-032-01 to TC-E1-032-17, with the principle 5 and access cases first | Section 16 |
| Decoupling patterns DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP15, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P5-E1032-APP the matcher, the store, the review rule, the reviewer's `resolve` and the SCR-31 list, with the contract in RWB-P5-E1032-CON; RWB-P4-E1032-APP the Documents right, the scope answer and the masking; RWB-P3-E1032-APP the case, the open cases of an account and the reference and parameter rows; and RWB-ITG-E1032-ITG the cross-service harness and the `-ITG` copies of the test cases, which read the `DOCATT` entry of each attach through `GET /api/recovery/decision/v1/decision-log`.

### 19. Out of scope

- The `matchStep` of JOB-12, the `CaseMatcher` and its five outcomes, the case and account patterns, the store and the duplicate check on the file hash, the `review_status` and `write_once` rule, the `rwb-docs` container, the four intake operations, the reviewer's `resolve`, the Unmatched list on SCR-31 and the `DocumentAttached` event on `rwb.document.events.v1`: RWB-P5-E1032-APP, with the contract and fakes in RWB-P5-E1032-CON.
- The local decision record that `rwb-document` writes in its own schema and its outbox row: RWB-P5-E1032-APP. This story consumes the fact, not the store's table.
- The Documents right `C`, the scope answer, the masking of the OCR pages and the access entries: RWB-P4-E1032-APP, with the authorise contract RWB-P4-E1037-CON.
- The case, its status and owner, the open cases of an account number, the reference lists and the parameters `CASE_NO_PATTERN`, `ACCOUNT_NO_PATTERN`, `CLASSIFY_THRESHOLD` and `rwb.dochub.autoattach`: RWB-P3-E1032-APP under DP-06 and DP-07, and `rwb-document` for its own parameter table and switch.
- The rule registry, the rule packages, the approval path, the `ApprovalWorkflow` and the decision screen SCR-11: the other P7 stories of this service. This story adds no rule row and no approval row.
- The daily hash-chain check JOB-14 at 02:00 and its compliance report, and the rule promote JOB-20: the decision-log and rule-governance baselines of this service, which cover these entries like any other.
- The data-lake copy of the decision log with JOB-13 and INT-19/INT-20: retired with the data lake (DP-17).
- Moving an attached document to another case (Epic 2), confirming or correcting the type and the fields of a document stored for review (RWB-P5-E1054-APP), the intake item base record and the source pickup (RWB-P5-E1057-APP), and field app photos (RWB-P5-E2024-APP).
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E1032-ITG.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: the OPS story of RWB-E1-032 (RWB-P5-E1032-OPS), which carries the subscription of this consumer.
