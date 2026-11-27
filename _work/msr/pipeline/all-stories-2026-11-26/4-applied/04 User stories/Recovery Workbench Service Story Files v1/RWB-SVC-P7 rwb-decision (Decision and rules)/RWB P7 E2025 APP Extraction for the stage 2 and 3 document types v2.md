# RWB-P7-E2025-APP Extraction for the stage 2 and 3 document types

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2025-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-025 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P7-AF |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2025-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DCM-006, REQ-DCM-005, REQ-DCM-017, REQ-DCM-018) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-025 for rwb-decision; the extraction decision record and its two reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E2025-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal auditor or compliance reviewer (RW-AUDIT, RW-COMPLY)**, I want **the extraction decision of every stage 2 and 3 document recorded in the central decision ledger of `rwb-decision` — for each extracted field, the field pattern or rule id and version that decided it, the parameter version in force, the confidence, the threshold reading and the final call of accepted or sent to the review queue — append only, hash chained and readable by case and by document**, so that **the litigation pack and the treatment record can be explained field by field to an auditor, and no value in them came from an extraction nobody can reproduce**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-025:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record library of DP-03.
- One deliverable and nothing else: the extraction decision record. For each document of a stage 2 or stage 3 type and for each extracted field, the service appends one entry to `decision_log_entry` through the decision-record path of DP-03, carrying the field pattern or rule id and version, the parameter version in force, the confidence, the threshold reading and the final call of `accepted` or `sent to the review queue`, with its inputs reference and its hash chain; and it serves the two decision-log reads so an auditor can read the entries by case and by document.
- What stays with `rwb-document` (P5, RWB-P5-E2025-APP): classification, the OCR text, the field patterns and their definitions in the type table, the confidence computation, the field state, the review queue and the JOB-12 intake window. This story consumes those facts and decides none of them.
- What stays with `rwb-litigation` (S4, RWB-S4-E2025-APP): the write of a legal action, a hearing and a judgment. What stays with `rwb-treatment` (S2, RWB-S2-E2025-APP): the write of the treatment record. This story writes neither, and it writes nothing into `legal_action`, `hearing` or `treatment`.
- What stays with `rwb-case` (P3): the reference lists and the parameters, read through the parameters and reference-data contracts of DP-06 and DP-07. The threshold, its value and its version are `rwb-case`'s rows and arrive here as facts.
- The service records and exposes the decision; it changes no document, no field, no case and no treatment (BR10).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1285; ASM-2277); this story uses the phrase "the rwb-decision login (DP-02)" and never the shared monolith login.

The legacy behaviour carried into the decision service is unchanged in meaning: one record per decision and no exception, the rule or pattern identifier and version on every record, the inputs reference so a decision can be reproduced, a record that cannot be altered once written, and no action standing without its record (REQ-DRI-001, REQ-DRI-002, REQ-DRI-005).

### 2. Business rationale

The litigation pack and the treatment record now fill themselves from a scanned contract, court filing or judgment (legacy RWB-E2-025). That only becomes an asset for the bank if each value in them can be explained: which pattern or rule accepted it, under which version of the type table and of the threshold parameter, at what confidence, and whether it was accepted or sent to a person. The monolith wrote `document_field` rows and a decision log row inside one process and one schema, so the two could not drift apart. In the target the extraction happens in `rwb-document` and the litigation and treatment records are written in `rwb-litigation` and `rwb-treatment`, so the explanation has to live in the one place every service's record is collected: the central ledger of `rwb-decision`, read through `GET /api/recovery/decision/v1/decision-log`.

Under Architecture v5 the decision ledger, the rule registry and the approvals are `rwb-decision` (slides 14, 27, 28 and 41), the decision records are written locally by each service in the same transaction as its change and collected centrally on `rwb.decision-record.v1` (slide 28), and the log is read by case, rule, approver and date through the decision-log operations (slide 14). The realignment changes the mechanism, not the business rule:

1. The in-process decision-log write of the monolith becomes the decision record of the owning service, published as `DecisionRecorded` on `rwb.decision-record.v1` and appended here through the decision-record library of DP-03, with the append-only rule and the hash chain that FEAT-DRI-01 and FEAT-DRI-03 already carry.
2. The decision log stays the evidence of a rule or a pattern answer and never becomes a copy of the extracted value: the entry names the field, its confidence and the versions in force, and the value stays in `rwb_document` (BR10, REQ-DRI-001).
3. The type table of `rwb-document`, the threshold parameter of `rwb-case` and the reference lists of `rwb-case` are read as facts and as versioned data, never as constants here (DP-06, DP-07): the entry names the version that was in force, which is the only way a later re-run can be told apart from the original.
4. The `JOB-12` intake window and the review queue become `rwb-document`'s event-started `DocumentIntakeWorkflow` (DP-10); the clock is not this story's and this story starts no Schedule.
5. The one decision-log read of the monolith becomes two operations on the service's own base (DP-13), and the data-lake copy of the log is retired with the data lake.

This story meets REQ-DCM-006 and REQ-DCM-005 on the record side and carries REQ-DCM-017 and REQ-DCM-018 only as the document version and date the entry names, not as extracted fields; it puts the reproducible-record half of REQ-DRI-001, REQ-DRI-002, REQ-DRI-003 and REQ-DRI-005 in place for the stage 2 and 3 types and leaves the classification, the extraction and the review where the document hub owns them.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2025-CON | The published document contract of `rwb-document` (P5): the document with its type, its version, its review status and its write-once flag, and the field rows with their name, confidence, state, pattern and pattern version; the `DecisionRecorded` fact of an extraction decision on `rwb.decision-record.v1`; and the contract fakes. Which fields of the extraction decision fact this service consumes is Not specified in the source documents (GAP-1285; ASM-2277), and the fact set this story assumes is that of ASM-2277 |
| RWB-PLT-E1027-CON | The decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash` and the append-only rule |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the field threshold 0.80 and the accuracy pass mark 0.90 with the version in force on the business date (legacy sections 3, 7 and 13; DL11); the parameter names are Not specified in the source documents (GAP-1285; ASM-2277) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): the decision code list, the approval level list and the document type codes with the version in force; the decision code list is LOV-DECISION of TSD P7 v2 T3.2 and does not name an extraction decision, which is the gap of GAP-1285 |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one entry per decision under a repeated fact, and the outbox row of the append |
| RWB-PLT-E1071-CON | The workflow kit in namespace `rwb-recovery` (DP-10). This story starts no workflow and registers no Schedule; the kit is a precondition only because the ingest path is designed to be replay safe |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the route the SCR-38 decision log query and an auditor's screen reach the two reads through |

Business preconditions carried from RWB-E2-025:

- Document type table version DOCTYPE-2026.12 is in force from 2026-12-31 with the eleven types, each with its `classify_threshold` and its `field_definitions`. Hearing notices stay under the Epic 1 type COURT_NOTICE. The types and fields are CONTRACT (contract_no, party_names, contract_amount, contract_date); CREDIT_APPROVAL (approval_no, approved_amount, approval_date, approval_level); MORTGAGE_DOCUMENT (title_doc_no, mortgage_amount, registration_date, land_office); COURT_FILING (court_name, black_case_no, filing_date, claim_amount); JUDGMENT (court_name, red_case_no, judgment_date, judgment_amount); COURT_NOTICE (court_name, black_case_no, notice_date, hearing_date). Each field carries a data type, an extraction method, `review_only` and an optional pattern (legacy section 13; DL19).
- The field threshold is 0.80 and the accuracy pass mark is 0.90 per field on the sample, and `document_hub_parameter` row `EXTRACT_ACCURACY_PASS` holds 0.90 (legacy sections 3, 7 and 13; DL11). The type table and the parameter belong to `rwb-document` and `rwb-case` and are read here as facts.
- The masked sample of 60 documents is staged: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE (legacy section 7 Background; RWB-TE-004). The sample is test data of the document hub and never enters an entry of this story.
- The classifier version that knows the eleven types is selected through the P10 agent runtime, so the record has an agent version to name where the type table is silent (legacy section 3). Which field of the entry carries it is Not specified in the source documents (GAP-1285; ASM-2277).
- The decision-log operations exist with the access TSD P7 v2 T-A.1 fixes for them: capability area DECISION_LOG, right R, scope applied; every role of TSD P7 v2 T6.1 holds R, and a role outside the matrix holds none.
- No build dependency. Day 1: the story builds against RWB-P5-E2025-CON and its fakes.

### 4. Flow

1. `rwb-document` (P5): intake, OCR, classification and extraction run behind the document contract, and for each document of a stage 2 or stage 3 type the extraction step accepts a field or sends it to the review queue. The classification, the OCR text, the confidence, the field state and the review queue are `rwb-document`'s and are not rebuilt here.
2. `rwb-document` writes its local decision record in the same transaction as the field rows and publishes `DecisionRecorded` on `rwb.decision-record.v1`, keyed by the case ID (DP-03, DP-09; Architecture v5 slide 28).
3. `rwb-decision` `ExtractionDecisionListener`: reads the fact into the inbox of DP-09, deduplicates by event ID and by the idempotency key the fact carries (R-UNI-40), and passes the decision facts to `ExtractionDecisionRecorder`: the case, the document reference and version, the document type, the field name, the field pattern or rule id and version, the parameter version in force, the confidence, the threshold and the threshold reading, and the final call.
4. `ExtractionDecisionRecorder`: reads the document through the document contract of RWB-P5-E2025-CON when the fact does not carry a field of the entry, and reads the threshold parameter and the decision-code list through the parameters and reference-data contracts of DP-06 and DP-07 with the version in force on the business date. It decides nothing about the extraction; it compares no confidence and applies no pattern (BR2, BR11).
5. `DecisionLogAppender`, one `RecordAndApply` transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash`, computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with `inputs_ref` pointing at the inputs snapshot and its freshness stamps, and writes the outbox row of the append. A failed append changes nothing: no entry, no chain position and no outbox row (DP-03; R-UNI-39; BR13).
6. `DecisionLogAppender`: a repeated fact with the same idempotency key returns the first entry's ID, adds one to the repeat count for R-UNI-40, and appends nothing (BR14).
7. An auditor or a reviewer reads the entries with `GET /api/recovery/decision/v1/decision-log` by case, by rule or pattern, by approver and by date range, or for one document; each row holds `entryId`, `chainSeq`, `inputsRef`, and for the extraction decisions the document reference and version, the document type, the field name, the pattern or rule id and version, the parameter version, the confidence, the threshold and its reading, the final call and `decidedAt`, `prevHash` and `entryHash`.
8. One entry is read with `GET /api/recovery/decision/v1/decision-log/{entryId}`, with its inputs snapshot and the freshness of each input it read.
9. A role outside the DECISION_LOG capability area is refused with MSG-P4-002, and a document of a case outside the caller's scope with MSG-P4-003; nothing is returned in either case (BR12).
10. Nothing in this story moves a document, a field, a case or a treatment: the entry is written beside them, and the readers of `rwb-litigation` and `rwb-treatment` keep reading the checked fields through the document contract of `rwb-document` (BR10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A field was below the threshold on the extraction side | The entry carries the threshold reading "below" and the final call `sent to the review queue`; the field state and the review item stay `rwb-document`'s | None | AC2 |
| X2 | A value failed its pattern at equal confidence | The entry carries the pattern as failed and the final call `sent to the review queue`; the sibling value that matched is `accepted` | None | AC3 |
| X3 | The extraction decision names a rule or pattern with no version | The append is refused with MSG-P7-009 naming `ruleVersion`, and nothing is written | MSG-P7-009 | AC1, AC4 |
| X4 | The decision code is not a value of the list in force | The append is refused with MSG-P7-009 naming `decisionCode`, and nothing is written | MSG-P7-009 | AC1 |
| X5 | The entry cannot be written, because the store is unavailable or the chain cannot be taken | Nothing is written and the fact stays on the topic for redelivery; no entry, no chain position and no outbox row | MSG-P7-003 | AC4, AC7 |
| X6 | The same decision fact is delivered again, or replayed from the topic | One entry exists; the inbox dedupe and the idempotency key both hold, and the repeat is counted for R-UNI-40 | None | AC5 |
| X7 | The document of the fact is not readable through the document contract, or is out of the caller's scope | The append is refused for that fact and the incident names the document reference; no entry is written on a guessed type or threshold | MSG-P4-003 | AC6, AC8 |
| X8 | The caller holds no right in the DECISION_LOG area, or asks for a document of a case out of scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; nothing is returned | MSG-P4-002, MSG-P4-003 | AC8, TC-E2-025-12 |
| X9 | The parameter or reference list cannot be read at the version in force | The append is refused and the fact is retried; no entry is written with an assumed threshold or an assumed decision code | MSG-GEN-006 | AC1, AC6 |
| X10 | A caller attempts to change or delete an entry | The statement is refused; a correction is a new entry that names the one it corrects in `corrects_entry_id` | None | AC4 |
| X11 | A step of another service asks this story to write a legal action, a hearing, a judgment, a treatment, a document or a field | Refused as out of scope; those writes are `rwb-litigation`'s, `rwb-treatment`'s and `rwb-document`'s and this story has no operation for them | None | AC7 |

An entry is only ever appended beside the fact that caused it: the entry, its chain position and its outbox row are written in one transaction, so a fact can never leave a half record, and a record can never exist for a fact that was not applied (BR13).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the document contract of RWB-P5-E2025-CON, the platform contract libraries of its DP table and the fakes; no classification, extraction, review, case, legal or treatment behaviour is rebuilt here |
| Negotiable | The decision code, the final call set, the parameter names, the pattern identifiers and the message ids are data or parameters of their owners; the story fixes only the record, the append-only rule, the chain and the two reads |
| Valuable | Every value in the litigation pack and the treatment record can be explained field by field, with the version that decided it, and the explanation cannot be quietly changed |
| Estimable | One listener, one recorder, one appender with the chain, one query controller with two operations, one migration, one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the eight criteria in section 7 runs as one automated test against the contract fakes with a fixed business date and a fixed chain |

### 7. Acceptance criteria

```gherkin
Feature: Extraction for the stage 2 and 3 document types — the rwb-decision extraction decision record

  Background:
    Given the environment is SIT
    Given the document type table version "DOCTYPE-2026.12" is in force from 2026-12-31
    Given the field threshold is 0.80 and the accuracy pass mark is 0.90
    Given the masked sample holds 60 documents: 10 each of CONTRACT, CREDIT_APPROVAL, MORTGAGE_DOCUMENT, COURT_FILING, JUDGMENT and COURT_NOTICE

  Scenario: AC1 One entry for the document and one for each accepted field (new, D-RCV-60)
    Given the rwb-document contract mock returns document "DOC-0601" on case "RW-2026-000601" classified "CONTRACT" with confidence 0.9300, with contract_amount "2400000.00" and contract_date "2026-11-01" accepted at or above the threshold of 0.80, and the field pattern of each field as held in "DOCTYPE-2026.12" with its identifier and version
    Given the rwb-case parameters contract mock returns the field threshold 0.80 in the parameter version in force on 2026-12-31
    When the extraction decisions of "DOC-0601" are recorded through the decision-record path
    Then one entry exists for the document and one for each of contract_amount and contract_date
    Then each entry carries chain_seq, inputsRef, the ruleId and ruleVersion of the field pattern that decided the field, the parameter version in force, the confidence 0.9300 and the threshold reading "at or above 0.80"
    Then each entry carries finalCall "accepted", decidedAt, prevHash and entryHash
    Then the entries commit in one transaction with their outbox row and are append only
    Then no entry carries the extracted value of contract_amount or contract_date, only the field name, the confidence and the versions

  Scenario: AC2 A field below the threshold is sent to the review queue (new, D-RCV-60)
    Given the rwb-document contract mock returns judgment "DOC-0602" whose judgment_amount is read with confidence 0.7100, below the threshold of 0.80, and held with state "REVIEW"
    When the extraction decision of judgment_amount is recorded
    Then the entry carries the confidence 0.7100, the threshold reading "below 0.80" and finalCall "sent to the review queue"
    Then the entry names the field judgment_amount, its pattern identifier and version and the parameter version in force
    Then the field state, the review item and the review queue stay rwb-document's and this story writes none of them

  Scenario: AC3 A value that does not match its pattern is sent to the review queue (new, D-RCV-60)
    Given the pattern for red_case_no is two to four letters, a space, digits, "/" and four digits
    Given the rwb-document contract mock returns red_case_no "Por345-2570" with confidence 0.9200, failing its pattern and held with state "REVIEW"
    Given the rwb-document contract mock returns a second value "Por 345/2570" with confidence 0.9200, matching its pattern and held with state "OK"
    When the two extraction decisions are recorded
    Then the entry for "Por345-2570" carries the threshold reading "at or above 0.80", the pattern as failed and finalCall "sent to the review queue"
    Then the entry for "Por 345/2570" carries the same confidence and the same pattern and finalCall "accepted"
    Then the two entries hold consecutive chain_seq values and the prevHash of the second equals the entryHash of the first

  Scenario: AC4 The log is append only and hash chained (new, D-RCV-60)
    Given 100 extraction entries are appended to the log of rwb_decision
    When the chain verifier runs from chain_seq 1 to 100
    Then every entry_hash equals the SHA-256 of the entry's canonical form
    Then every prev_hash equals the entry_hash of the entry before it, and the first prev_hash is 64 zeros
    Then the result holds count 100, last chain_seq 100 and that entry's entry_hash
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of an entry are attempted
    Then both statements are refused and the entry is unchanged
    Then a correction is a new entry that names the entry it corrects in corrects_entry_id

  Scenario: AC5 A repeated decision fact gives one entry (new, D-RCV-60)
    Given the decision of document "DOC-2026-0009981" on case "RW-2026-000123" was recorded under idempotency key "EV-7f3a-0001"
    When the same decision arrives again with the idempotency key "EV-7f3a-0001"
    Then one entry exists for the decision
    Then the ledger returns the first entry's ID and adds 1 to the repeat count for R-UNI-40
    Then no second entry, no second chain position and no second outbox row exist

  Scenario: AC6 The log reads by case and by document (new, D-RCV-60)
    Given entries exist for case "RW-2026-000601": the contract entries of "DOC-0601" and the two judgment entries of "DOC-0602"
    When an auditor calls GET /api/recovery/decision/v1/decision-log for case "RW-2026-000601"
    Then the answer holds the entries of both documents in chain order
    When the auditor calls the same operation for the document "DOC-0602"
    Then the answer holds the two entries of "DOC-0602" only
    Then each row holds entryId, chainSeq, inputsRef, ruleId and ruleVersion, the confidence, finalCall, decidedAt, prevHash and entryHash
    Then the same entry is readable with GET /api/recovery/decision/v1/decision-log/{entryId}

  Scenario: AC7 Nothing but the record changes (new, D-RCV-60)
    Given the rwb-document contract mock returns judgment "DOC-0604" held write-once with write_once true and four document_field rows
    When the four extraction decisions of "DOC-0604" are recorded
    Then four entries exist in the log
    Then the document, its four field rows, its file hash, its storage_ref and its write_once are unchanged
    Then no legal_action, hearing or judgment write is made in rwb-litigation and no treatment write is made in rwb-treatment
    Then no case status, task or timer is changed in rwb-case

  Scenario: AC8 The log is refused to a role without its right and to a case out of scope (new, D-RCV-60)
    Given a role without the right in the DECISION_LOG capability area
    Given document "DOC-0605" belongs to a case of team "LIT-NE" and the caller's scope is team "LIT-BKK"
    When that role calls GET /api/recovery/decision/v1/decision-log
    Then the response is 403 with MSG-P4-002
    When a reader in scope "LIT-BKK" asks for the entries of "DOC-0605"
    Then the response is 404 with MSG-P4-003 and no entry is returned
```

These eight criteria are new for the `rwb-decision` slice of RWB-E2-025 and are the record and read criteria of the key. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key changes a document, a field, a classification or a review item, and those changes belong to RWB-P5-E2025-APP. The values are the legacy values of RWB-E2-025 — case `RW-2026-000601`, documents `DOC-0601`, `DOC-0602`, `DOC-0604`, `DOC-0605` and `DOC-2026-0009981`, case `RW-2026-000123`, types CONTRACT and JUDGMENT and COURT_NOTICE, the type table version `DOCTYPE-2026.12` from 2026-12-31, the threshold 0.80, the pass mark 0.90, confidences 0.9300, 0.9200 and 0.7100, the red case number pattern of two to four letters, a space, digits, "/" and four digits, the values "Por345-2570" and "Por 345/2570", contract_amount "2400000.00", contract_date "2026-11-01", the four field rows of the write-once judgment, teams "LIT-BKK" and "LIT-NE", the idempotency key "EV-7f3a-0001", and the messages MSG-P7-009, MSG-P7-003, MSG-P4-002, MSG-P4-003 and MSG-GEN-006 — and no new business value is introduced. The decision code, the final call value set, the parameter names, the message ids of this story and the screen or panel id have no source and are carried in GAP-1285 and ASM-2277; the pattern identifiers and versions are `rwb-document`'s data and are not written here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The stage 2 and 3 types and their fields are those of the document type table version in force on the extraction date, and the entry names that version | Document types reference table; DL19; R-UNI-38; REQ-DCM-006 |
| BR2 | A field below the threshold, failing its pattern, or marked review-only has the final call `sent to the review queue`; a field at or above the threshold that matches its pattern has the final call `accepted`; the call is copied from the extraction and never recomputed here | RWB-E1-053 BR2, BR3; REQ-DCM-005 |
| BR3 | The threshold and its version are read at the moment of the record and named on the entry; an entry is never written with an assumed threshold, an assumed version or an assumed pass mark | REQ-DRI-010; DL11; DP-06 |
| BR4 | The pattern is data: the entry names the pattern identifier and version held for the field in the type table, and no pattern is a constant of this service | Principle 1; RWB-E1-053 BR5; DP-07 |
| BR5 | Readers of the decision log see the final call of each field; the reader of `rwb-litigation` and `rwb-treatment` still receives only fields in state OK, CONFIRMED or CORRECTED through the document contract, which is not this story's | FEAT-DCM-10; REQ-DCM-006 |
| BR6 | The extraction never changes the stored file of a write-once document, and this story changes no document and no field: it records the decision and nothing else | CTL-12; RWB-E2-025 AC10 |
| BR7 | Party names, amounts and other personal or financial field values are never copied into the entry, its inputs reference, its outbox row or its logs; the entry carries the field name, the confidence and the versions | DF-DOC-015; CTL-11; DL26; §R7.2 s17; ASM-2280 |
| BR8 | Dates read in Buddhist Era are stored as ISO dates by `rwb-document`, and the entry carries the date it decided on, never a converted date of its own | RWB-E1-053 BR6 |
| BR9 | One entry per decision and no exception: every extraction decision of a stage 2 or stage 3 document leaves one entry, and an action that cannot be recorded does not stand | FEAT-DRI-02; REQ-DRI-001; REQ-DRI-005 |
| BR10 | The story records and exposes; it writes no document, no field, no case, no legal action, no hearing, no judgment and no treatment, and it reads no table of another service | Architecture v5 slides 14 and 41; DP-01 |
| BR11 | The decision code is a value of the list in force; an unknown code is refused with MSG-P7-009 naming `decisionCode`, and a rule or pattern identifier with no version with MSG-P7-009 naming `ruleVersion` | FSD P7 v3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05; REQ-DRI-001 |
| BR12 | The two reads declare the DECISION_LOG capability area and the right R with the scope applied; a role outside the matrix is refused with MSG-P4-002 and a case out of scope with MSG-P4-003 | TSD P7 v2 T-A.1 and T6.1; REQ-DRI-012 |
| BR13 | The entry, its chain position and its outbox row are written in one transaction; a failed append leaves nothing and the fact is redelivered | Principle 5; R-UNI-39; DP-03 |
| BR14 | One entry per decision under a repeated fact: the inbox dedupe and the idempotency key make a second entry impossible, and the repeat is counted | FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40 |
| BR15 | The log is append only and hash chained: an entry is never changed or deleted, a correction is a new entry naming the one it corrects, and every `entry_hash` is the SHA-256 of the entry's canonical form | FEAT-DRI-01; REQ-DRI-002; REQ-DRI-003; FSD P7 v3 AC-P7-001-01 and AC-ALT-P7-001-01 |

### 9. State transitions

None for a document, a field, a case, a legal action or a treatment. The states below are the states of an entry of this story, and the entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A `DecisionRecorded` extraction fact arrives | The decision code, the pattern or rule version and the parameter version are readable at the version in force | Appended, with the next `chain_seq`, its `prev_hash` and its `entry_hash`, in one transaction with its outbox row |
| Absent | A `DecisionRecorded` extraction fact arrives | The decision code is unknown, or the rule or pattern has no version | Absent: refused with MSG-P7-009 and nothing is written |
| Absent | A `DecisionRecorded` extraction fact arrives | The store is unavailable, or the chain cannot be taken | Absent: MSG-P7-003, nothing is written, the fact stays for redelivery |
| Appended | The same fact arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A correction of the decision is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`, and the corrected entry stays unchanged |
| Appended | An UPDATE or a DELETE is attempted | Any caller, including the schema owner | Unchanged: the statement is refused by the append-only rule |

The document stays in whatever review state `rwb-document` set, the case stays in its stage, and the legal action, the hearing and the treatment are written by their own services; this story changes none of them (BR10).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Reads the decision log by case, by document, by rule or pattern and by date range, and one entry with its inputs reference (DECISION_LOG R) |
| RW-COMPLY, Compliance and PDPA officer | Reads the same, without the personal field values, which the entry never carries (DECISION_LOG R) |
| RW-COE, center of excellence analyst | Reads the decisions of the extraction to explain a field accuracy question (DECISION_LOG R) |
| Every role of TSD P7 v2 T6.1 | Holds R on the decision log and reads the entries of the cases in its scope |
| A role outside the matrix, or a case out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| The `rwb-decision` service identity | Consumes the extraction fact, reads its own `rwb_decision` rows, and appends the entry and its outbox row (DP-02) |
| The decision-record library identity | Provides the chain position, the `prev_hash` and the `entry_hash` of the append (DP-03) |
| `rwb-document` | Owns the classification, the OCR text, the patterns, the confidence, the field state, the review queue and the JOB-12 window; this story holds no authority over any of them |
| `rwb-litigation` and `rwb-treatment` | Own the legal action, the hearing, the judgment and the treatment writes; this story writes none of them |
| No approval level from the delegation of authority applies | The extraction decision is a system decision and carries no approver; the approval path of this service is another story's |

The authorisation decision behind the two reads is `rwb-access`'s role, scope and right data, taken through the guard the service's decision-log baseline already carries; this story adds no guard of its own and holds no role, scope or delegation row (ASM-2281). The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1285; ASM-2277); the story refers to "the rwb-decision login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write |
| DF-DEC-004 | `decision_log_entry` | rule_id (the field pattern or rule identifier that decided the field) | Write |
| DF-DEC-005 | `decision_log_entry` | rule_version (the version of that pattern or rule) | Write |
| DF-DEC-006 | `decision_log_entry` | model_version | Write where the extraction names one |
| DF-DEC-007 | `decision_log_entry` | agent_version (the classifier version of the extraction) | Write where the extraction names one |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the inputs snapshot, with the freshness of each input) | Write |
| DF-DEC-009 | `decision_log_entry` | recommendation (the confidence and the threshold reading) | Write |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Not written: the extraction decision has no approver |
| DF-DEC-011 | `decision_log_entry` | approval_level | Not written: no delegation level applies |
| DF-DEC-012 | `decision_log_entry` | final_call (`accepted` or `sent to the review queue`) | Write |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written: there is no override of an extraction |
| DF-DEC-014 | `decision_log_entry` | actions | Write the append facts |
| DF-DEC-015 | `decision_log_entry` | outcome | Write where the extraction names one |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017 | `decision_log_entry` | prev_hash | Write |
| DF-DEC-018 | `decision_log_entry` | entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id | Write as the service identity of the extraction |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write |
| (assumed column) | `decision_log_entry` | document_id, doc_version, doc_type_code, field_name, parameter_version, confidence, threshold_value, threshold_reading | Write; the columns are Not specified in the source documents (GAP-1285; ASM-2277) |
| DF-DOC-001, DF-DOC-002, DF-DOC-004, DF-DOC-006, DF-DOC-010 | `document` (P5) | id, case_id, document_type, storage_ref, write_once | Read through the document contract of RWB-P5-E2025-CON, never a table |
| DF-DOC-012 to DF-DOC-017, DF-DOC-034, DF-DOC-035 | `document_field` (P5) | field name, extracted value, confidence, state, extractor_version | Read through the document contract; the value is never copied into an entry (BR7) |
| DF-REF-219, DF-REF-224, DF-REF-233, DF-REF-246 | `document_type`, `document_hub_parameter` (P5) | doc_type_code, field_definitions, classify_threshold, param_value | Read as facts of the document contract, with the version in force |
| (parameters) | `parameter_value` (P3) | the field threshold 0.80 and the pass mark 0.90 with the version in force | Read through the parameters contract of DP-06, never a table |
| (reference lists) | reference data (P3) | the decision code list and the approval level list with the version in force | Read through the reference-data contract of DP-07, never a table |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_decision` | the append row | Write |

No row of `document`, `document_field`, `document_type`, `recovery_case`, `legal_action`, `hearing`, `judgment` or `treatment` is copied into `rwb_decision`: the document facts arrive on the document contract and the extraction facts on `rwb.decision-record.v1`, and the other services' records are never read. The extracted value, the party names and the amounts stay in `rwb_document`, which is the reading of ASM-2280. Field IDs are those of the Logical Data Model and Data Dictionary v9; the extraction columns of the entry have no field ID in TSD P7 v2 T3.1 and are written from the assumed shape of section 12.1, which is Not specified in the source documents (GAP-1285; ASM-2277).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007). The request and response field set of an extraction entry is Not specified in the source documents (GAP-1285; ASM-2277).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the decision log by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and by the document reference of an extraction entry; 200 with the DecisionLogPage | DECISION_LOG, right R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs reference, its versions, its confidence, its threshold reading, its final call and its hash chain; 200 with the DecisionLogEntry | DECISION_LOG, right R, scope applied | Not applicable, read only |

The DecisionLogEntry body the extraction stories read carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `parameterVersion`, `modelVersion`, `agentVersion`, `inputsRef`, `recommendation` with the confidence, `finalCall`, `thresholdValue`, `thresholdReading`, `documentId`, `docVersion`, `docTypeCode`, `fieldName`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`. The DecisionLogPage body carries `items`, `page`, `size` and `total`. The parameter name, the decision code for an extraction decision, the final call value set and the document filter of the search are Not specified in the source documents (GAP-1285; ASM-2277).

Errors: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 the entry, the document or the case is absent or out of scope (MSG-P4-003); 422 a query value is outside its list (MSG-GEN-001); 503 the log is unavailable (MSG-GEN-006) or the append could not be made (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document, on RWB-P5-E2025-CON | The document with its type, version, write-once flag and field rows with their confidence, state, pattern and pattern version, for a fact that does not carry a field of the entry; faked, one hop, 2 s timeout (DP-11) |
| — | the parameters read of `rwb-case` (DP-06) | P3 rwb-case, on RWB-P3-E1042-CON | The field threshold 0.80 and the pass mark 0.90 with the version in force on the business date; path not specified in the sources (GAP-1285; ASM-2277), read in process through its client library and faked |

The reference lists of `rwb-case` (DP-07, RWB-P3-E1043-CON) are read in process through their client library and are not a cross-service REST row; the extraction facts arrive on `rwb.decision-record.v1` and not over REST. The contract dependency recorded on the story is RWB-P5-E2025-CON; the platform and published contracts the DP table adds are listed in section 13 and carried in the gap of GAP-1286.

#### 12.3 Events published

None. This story publishes no event of its own: the extraction decision is a fact of `rwb-document` and the entries of the central ledger are read through the operations of 12.1. `DecisionRecorded` on `rwb.decision-record.v1` is published by the owning service of each decision, and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42). The `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` events of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by `rwb-document` for these decisions | `ExtractionDecisionListener`: inbox dedupe by event ID, then `ExtractionDecisionRecorder` and `DecisionLogAppender` for the fields, the versions, the confidence, the threshold reading and the final call |

The fact carries IDs, codes, versions, a confidence and a reading only; no extracted value, no party name and no amount travels on the topic (BR7). Which fields of the fact this service requires, and whether the document reference travels on the fact or is read through the document contract, is Not specified in the source documents (GAP-1285; ASM-2277); the reading this story applies is that of ASM-2277 and the document read of 12.2 covers the gap.

#### 12.5 Workflows and activities

None of this story's own. The append is a transactional write on the request and consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09; and the extraction's own `DocumentIntakeWorkflow` runs on queue `rwb-document` and is neither started nor signalled here. This story registers no workflow and no activity on the `rwb-decision` queue, and it adds none to the workflow kit (ASM-2279).

#### 12.6 Schedules

None. The ingest of `rwb.decision-record.v1` is continuous Kafka, as JOB-13 states (Architecture v5 slide 44); JOB-12 Document intake is an event-started workflow of `rwb-document` and belongs to RWB-P5-E2025-APP; the daily hash-chain check JOB-14 at 02:00 is `rwb-decision`'s and covers the entries of this story like any other, and it is not rebuilt or scheduled here. This story creates no Temporal Schedule and starts nothing on a clock (ASM-2279).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The extraction decision entry, its chain position, its hash, its inputs reference and its final call; append only |
| decision record (local library) | P7 rows in `rwb_decision`, written through the decision-record library | The append of DP-03 and its hash chain |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `document`, `document_field`, `document_type` and `document_hub_parameter` (P5), `recovery_case`, `task`, `timer` and `parameter_value` (P3), `legal_action`, `hearing` and `judgment` (S4) and `treatment` (S2). The other P7 tables — `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` — are not touched by this story. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | RWB-P5-E2025-CON | Document "DOC-0601" of case `RW-2026-000601`, type CONTRACT at confidence 0.9300, with contract_amount "2400000.00" and contract_date "2026-11-01" accepted and their pattern identifiers and versions; judgment "DOC-0602" with judgment_amount at 0.7100 in state REVIEW and red_case_no "Por345-2570" at 0.9200 in state REVIEW beside "Por 345/2570" at 0.9200 in state OK; judgment "DOC-0604" write-once with four field rows; document "DOC-0605" of a case of team "LIT-NE"; the out-of-scope 404 with MSG-P4-003 |
| rwb-case parameters fake | RWB-P3-E1042-CON, DP-06 | The field threshold 0.80 and the accuracy pass mark 0.90 with the version in force on 2026-12-31, and an unavailable answer for X9 |
| rwb-case reference-data fake | RWB-P3-E1043-CON, DP-07 | The decision code list and the approval level list with the version in force, and an unknown code for X4 |
| decision-record fake | RWB-PLT-E1027-CON | The append, the next chain position, the `prev_hash` and the `entry_hash`, the append-only refusal, the SHA-256 of the canonical form, and a forced failure for the 503 case of X5 |
| outbox and inbox library fake | RWB-PLT-TE006-CON | The `DecisionRecorded` fact of each scenario, its replay under the same event ID and idempotency key, and the outbox row of the append |
| rwb-access guard fake | The service baseline's authorise path | The allow answer for the roles of TSD P7 v2 T6.1 and the refusal of a role outside the DECISION_LOG area; the guard is the baseline's and this story adds none (ASM-2281) |

Each fake is replaced by the real service as RWB-P5-E2025-APP lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the document read and the parameters read consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the extraction workflow is `rwb-document`'s and is not started here |
| File | None | No file input and no file output; the documents themselves never leave `rwb-document` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/extraction`, Java package `th.co.scb.ace.workbench.recovery.decision.extraction`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the pattern the record itself travels on — the local decision-record library and the shared topic `rwb.decision-record.v1` — and it is applied here as the append path of the central ledger, with its H RWB-PLT-E1027-CON; it is not in the story's metadata list of patterns, and its dependency is carried in the gap of GAP-1286 beside the other DP-added dependencies. DP-01 is the boundary: the extraction entry lives in `rwb_decision` and the document facts arrive on the document contract, never as a read of `rwb_document`. DP-11 is the mockable boundary for the document read, one hop with a 2 s timeout and a breaker. DP-13 is the base: every path of 12.1 and 12.2 is on the owner's base `/api/recovery/<short>/v1`, and the monolith base appears nowhere. DP-19 is not built here: SCR-38 Decision log query and the auditor's screen are reached through the gateway-bff composite route of RWB-PLT-N001-CON, and this story adds no route to it.

DP-10 is the JOB-12 intake window, and the clock stays with `rwb-document`: under RWB-P5-E2025-APP the intake is the event-started `DocumentIntakeWorkflow` on queue `rwb-document`, so this story declares no Schedule (12.6) and registers no workflow or activity (12.5). No Schedule and no workflow is invented for the extract-and-record path, because the record is appended where the fact arrives.

The platform H dependencies of the DP table — H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON and H RWB-PLT-N001-CON — and the C dependencies of the published contracts of other services — C RWB-P3-E1042-CON and C RWB-P3-E1043-CON — are not in the metadata rows of this story, which name None and RWB-P5-E2025-CON; they are the dependencies the DP table adds and they are recorded in GAP-1286 and ASM-2278. None of them blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and two published contracts of `rwb-case`, built against their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ExtractionDecisionListener | Kafka consumer with the inbox | Reads `DecisionRecorded` for the stage 2 and 3 extraction, deduplicates by event ID and idempotency key, and hands the decision facts to the recorder |
| ExtractionDecisionRecorder | Service | Reads the document facts and the parameter and reference versions in force, composes the entry, and decides nothing about the extraction itself (BR2, BR3, BR11) |
| DecisionLogAppender | Service | Takes the next `chain_seq`, computes `prev_hash` and `entry_hash`, and writes the entry and its outbox row in one transaction (DP-03, BR13, BR15) |
| ChainVerifier | Service | Recomputes the chain from a start position and reports count, last `chain_seq` and last `entry_hash`, and the break if any |
| DecisionLogQueryController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the declared area and right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, with the append-only rule, the chain columns, the idempotency key and the search of 12.1 |
| DocumentFactClient | Adapter | The document read of RWB-P5-E2025-CON, one hop with a 2 s timeout and a breaker |
| ParameterVersionClient | Client | The threshold and the pass mark of DP-06 and the decision code list of DP-07, with the version in force on the business date |
| InputsSnapshotResolver | Service | Resolves the `inputs_ref` of the entry and the freshness stamp of each input the decision read |

**Database and migrations**

- Writes `decision_log_entry`, the local decision record of the append and the library objects, all in schema `rwb_decision`; reads no other schema (DP-01).
- Migration in this story, in the per-service Flyway sequence of the service: `V2025_1__decision_extraction_entry.sql` adds the extraction columns of section 11 that the decision-log store baseline does not hold — the document reference and version, the document type code, the field name, the parameter version, the confidence, the threshold and the threshold reading — and the unique key `ux_declog_idempotency ON decision_log_entry (idempotency_key) WHERE idempotency_key IS NOT NULL`, so one entry per decision is a constraint and not only a check (BR14). The column names and types are Not specified in the source documents (GAP-1285; ASM-2277).
- The append-only rule is the table's, with the trigger `tr_declog_append_only` that refuses an UPDATE and a DELETE from the schema owner and the missing grant for the service role, as FSD P7 v3 AC-P7-001-01 fixes it.
- No row of `document`, `document_field` or `parameter_value` is written here: the document hub's tables and the case's parameters are their owners'.

**Configuration and reference data**

- The field threshold 0.80 and the accuracy pass mark 0.90 are parameter rows of `rwb-case` read through DP-06 with the version in force; the parameter names are Not specified in the source documents (GAP-1285; ASM-2277), and the story holds no default.
- The decision code list and the approval level list are reference data of `rwb-case` read through DP-07; the value an extraction decision carries is Not specified in the source documents (GAP-1285; ASM-2277), because LOV-DECISION names D5.1 to D9.3 and the access events only.
- The final call values `accepted` and `sent to the review queue` are the reading of ASM-2277 and are held as data, not as constants: a change is a reference row and not a release.
- The outbox retry policy and the inbox retention are the platform's (RWB-PLT-TE006-CON).
- The feature switch of this capability, if one is wanted, is a parameter of DP-06 and is not named here, because no source names it (GAP-1285; ASM-2277).

**Build steps**

1. `DecisionLogRepository` and the migration, with the unique key on the idempotency key and the append-only trigger; test that a second entry for the same decision and an UPDATE are both refused (AC4, AC5).
2. `ExtractionDecisionListener` with the inbox, the dedupe by event ID and idempotency key, and the not-a-decision cases of X6; test the replay of the same fact (AC5).
3. `ExtractionDecisionRecorder` and `ParameterVersionClient`: the entry composed from the document facts and the versions in force, with the refusal of an unknown decision code and of a rule or pattern with no version (X3, X4; AC1).
4. `DecisionLogAppender` and the chain: `chain_seq`, `prev_hash`, `entry_hash` over the canonical form, the first `prev_hash` of 64 zeros, and the fail-closed transaction (AC4, X5).
5. `InputsSnapshotResolver` and the `inputs_ref` with the freshness stamp of each input (AC1, AC6).
6. `DecisionLogQueryController` with the two operations, the declared area and right, the scope, the paging and the problem mapping; tests for AC6 and the refusals of AC8 (TC-E2-025-12).
7. `ChainVerifier` over 100 entries, with the count, the last `chain_seq` and the last `entry_hash` reported (AC4).
8. The contract-fake run of the whole slice: the document fake, the parameters and reference-data fakes, the decision-record fake and the outbox fake, green from Day 1 (AC1 to AC8).
9. The boundary test: no write to `rwb_document`, `rwb_case`, `rwb_litigation` or `rwb_treatment`, and no extracted value in any entry, outbox row or log line (AC7, BR7).

**Feature switch.** None of its own is named by a source. The capability is selected by the reference row that enables the stage 2 and 3 types in `rwb-document`, which is RWB-P5-E2025-APP's switch `rwb.dochub.extraction-stage23`; with that switch off no extraction decision of a new type arrives, and this story appends nothing for a type it never receives. This story adds no second switch (GAP-1285; ASM-2277).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P5-E2025-CON stay green, and a SIT day shows one entry per document and per extracted field with its pattern or rule version, its parameter version, its confidence, its threshold reading and its final call; a chain of 100 entries verified with no break and no entry changed or deleted; one entry under a repeated fact; both reads answering by case and by document; and not one document, field, case, legal action, hearing, judgment or treatment changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-009 | An entry has no rule or pattern version, or a decision code outside the list in force | Not specified in the source documents (GAP-1285; ASM-2277) | This story, on the append, naming `ruleVersion` or `decisionCode` |
| MSG-P7-003 | The entry cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append transaction |
| MSG-P4-002 | The role holds no right in the DECISION_LOG area | You cannot {action} here. Your role does not include it. | This story, through the guard of the read |
| MSG-P4-003 | The entry, the document or the case is outside the caller's scope | This case is not in your scope. | This story, through the guard of the read |
| MSG-GEN-001 | A query value is outside its list, or a required field of the entry is absent | Enter {field}. | This story, on the read and on the append |
| MSG-GEN-006 | The log or the store is unavailable | {system} is not available. Your request is queued and will be retried. | This story, on the read and on the retried fact |

MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-GEN-001 and MSG-GEN-006 are copied unchanged from the FSD P7 v3 message set and the platform messages the guard and the library carry. The text of MSG-P7-009 is named by the FSD P7 v3 exception flows but is not written out in any source this story may read, so the placeholder stands; the message id set of this story beyond these six has no source and is carried in GAP-1285. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by SCR-38 Decision log query and by the auditor's view of the decision log, which are served through the gateway-bff composite route of DP-19 and are another story's; SCR-30 Case documents and SCR-31 Document review queue stay `rwb-document`'s and this story feeds neither of them. A panel or screen id for showing the extraction decisions beside a document on SCR-30 is Not specified in the source documents (GAP-1285; ASM-2277).

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The entries of the case or the document, in chain order, with the field, the pattern or rule version, the parameter version, the confidence, the threshold reading and the final call |
| The entry read | One entry | The same row with its inputs reference, its freshness stamps, its `decidedAt`, its `prevHash` and its `entryHash` |
| The entry read | An entry with `correctsEntryId` | The correction beside the entry it corrects, and the corrected entry unchanged |
| The read | 403, or 404 | MSG-P4-002 for a role without the right, MSG-P4-003 for a case out of scope; no row is returned |

The screen field list, the composite route specification and the masking of each field belong to RWB-PLT-N001-CON and to the story that owns SCR-38.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-025-12 | Access, BR12 | Component | RW-REFADM user with no right in the DECISION_LOG area calls the decision-log read; refused with MSG-P4-002 |
| TC-E2-025-01 | AC1, BR1 | Component | 10 masked court notices from the sample, with the type code COURT_NOTICE and the entries of court_name, black_case_no and hearing_date |
| TC-E2-025-02 | AC1, BR7 | Contract | Synthetic signed contract "DOC-0601" with two parties, contract_amount "2400000.00" and contract_date "2026-11-01"; the entry carries the field names and no value |
| TC-E2-025-03 | AC2, BR2 | Component | Judgment "DOC-0602" with judgment_amount at confidence 0.71 and final call `sent to the review queue` |
| TC-E2-025-04 | AC1, BR3 | Contract | 10 sample judgments, 8 amounts correct; the pass mark and its parameter version on the entries of the evaluation |
| TC-E2-025-05 | AC1, BR1 | Component | 50 sample documents of the five new types; one entry per document and per field, each naming the type table version in force |
| TC-E2-025-06 | AC1, BR1 | Contract | Judgment "DOC-0603" received the day before the valid-from date, recorded against the earlier table version |
| TC-E2-025-07 | AC1, BR8 | Unit | Judgment dated 5 March 2570; the entry carries the date the extraction decided on and converts none |
| TC-E2-025-08 | AC3, BR4 | Unit | Red case numbers "Por345-2570" and "Por 345/2570" at confidence 0.9200; two entries, one review call and one accepted call |
| TC-E2-025-09 | AC6, BR5 | Contract | Judgment with one OK field and one REVIEW field; the read returns both entries with their final calls and the reader contract is untouched |
| TC-E2-025-10 | AC7, BR6 | Component | Write-once judgment "DOC-0604" with four field rows; four entries and no change to the file hash, the storage_ref or write_once |
| TC-E2-025-11 | AC8, BR1 | Contract | Document "DOC-0605" of team LIT-NE read from scope LIT-BKK; 404 with MSG-P4-003 and no entry |

The legacy level System maps to Component or Contract as the row shows, and Access to Component. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Every case is asserted on the record side of this story: the entry, its versions, its confidence, its threshold reading, its final call, its chain and its two reads; the classification, the extraction and the review item are the document contract fake's. The `-ITG` copies of these cases belong to RWB-ITG-E2025-ITG and are not written here.

### 17. Guardrails

- No business value in code: the decision code, the final call set, the threshold and its version, the pass mark, the pattern identifiers and the message ids are reference rows, parameter rows or facts of another service; nothing of them is a constant here.
- No personal data in the entry, the inputs reference, the event, the outbox, the tests or the logs: the case ID, the document reference and version, the document type code, the field name, the pattern and parameter versions, the confidence, the threshold reading, the final call and dates only; the extracted value, the party names and the amounts stay in `rwb_document`.
- No read of another service's tables (DP-01): the document arrives on its contract, the extraction decision on `rwb.decision-record.v1`, the parameters and the reference lists in process; no `document`, `document_field`, `recovery_case`, `parameter_value`, `legal_action`, `hearing` or `treatment` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- One recorder and no mover: this story changes no document, no field, no case, no legal action, no hearing, no judgment and no treatment, so a decision record can never move a case (BR10).
- No entry without its record, and no record without its entry: the append, its chain position and its outbox row commit in one transaction, and a failure leaves nothing and redelivers the fact (BR13, R-UNI-39).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the chain is verifiable from `chain_seq` 1 (BR15).
- One entry per decision: the inbox dedupe and the unique key on the idempotency key make a second entry impossible (BR14).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call, with a breaker per downstream; a missing document fact or a missing parameter version never produces an entry from a guessed type, threshold or code (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-006 | Fields extracted into the index for the agreed types, in Thai and English | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | BR1, BR2, BR5 | TC-E2-025-01, TC-E2-025-02, TC-E2-025-04 to TC-E2-025-11 |
| REQ-DCM-005 | Classified with a confidence; below the threshold to the review queue | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | BR2, BR3 | TC-E2-025-03, TC-E2-025-05, TC-E2-025-09 |
| REQ-DCM-017 | Court evidence attributes | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | BR7, BR10 | TC-E2-025-02, TC-E2-025-10 |
| REQ-DCM-018 | Electronic discovery attributes | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-22 | 13 Manage documents and correspondence | BR7, BR10 | TC-E2-025-05, TC-E2-025-11 |
| REQ-DRI-001 | One record per decision with the rule, model, agent and prompt versions, the inputs snapshot, the recommendation and the outcome | Program, 5.6; Epic 1 | FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-03 | 17 Run the decision center | BR9, BR11 | TC-E2-025-01, TC-E2-025-03, TC-E2-025-06 |
| REQ-DRI-002 | The log is append only; a correction is a new record naming the one it corrects | Program, 5.6; Epic 1 | FEAT-DRI-01 | 17 Run the decision center | BR15 | TC-E2-025-04, TC-E2-025-08 |
| REQ-DRI-003 | The log is hash chained and checked daily | Program, 5.6; Epic 1 | FEAT-DRI-01 | 17 Run the decision center | BR15 | TC-E2-025-04, TC-E2-025-07 |
| REQ-DRI-005 | No action proceeds if its record cannot be written | Program, 5.6; Epic 1 | FEAT-DRI-05 | 17 Run the decision center | BR9, BR13 | TC-E2-025-10, TC-E2-025-12 |
| REQ-DRI-010 | A parameter catalog holds every threshold and limit, versioned | Program, 5.6; Epic 1 | FEAT-DRI-01 | 17 Run the decision center | BR3 | TC-E2-025-04, TC-E2-025-06 |
| REQ-DRI-012 | Audit can query the log for a population of cases with inputs, versions, approver and final call | Epic 2, 3.7; Program, 5.7 | FEAT-APD-01 | 17 Run the decision center | BR12 | TC-E2-025-09, TC-E2-025-12 |

REQ-DCM-017 and REQ-DCM-018 are carried on this story only as the document version and date an entry names: neither is an extracted field and neither adds an entry of its own, which is the boundary the legacy story draws in its section 19.

| Legacy reference | Where it is kept |
|---|---|
| One record per decision, with the rule or pattern and its version, and the inputs reference | Sections 1, 2, 4, 7 (AC1), 8 (BR9, BR11) |
| The threshold of 0.80 and the final call of a low-confidence field | Sections 3, 7 (AC2), 8 (BR2), 13 |
| The pattern check as data, and the two red case numbers at 0.9200 | Sections 3, 7 (AC3), 8 (BR4) |
| Append only, the hash chain, the first `prev_hash` of 64 zeros and the correction | Sections 7 (AC4), 8 (BR15), 9 |
| One entry under a repeated fact, idempotency key "EV-7f3a-0001", document "DOC-2026-0009981" | Sections 4, 7 (AC5), 8 (BR14) |
| The decision-log reads by case and by document, and the seven field groups | Sections 4, 7 (AC6), 12.1 |
| The write-once document and the boundary that nothing else changes | Sections 7 (AC7), 8 (BR6, BR10), 17 |
| Messages MSG-P7-009, MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-GEN-006 | Section 14, exception paths |
| Rule IDs R-UNI-38, R-UNI-39 and R-UNI-40 | Sections 4, 5, 8 |
| Legacy key RWB-E2-025, story RWB-P7-E2025-APP, contract RWB-P5-E2025-CON | Metadata, sections 3, 12 |
| Test cases TC-E2-025-01 to TC-E2-025-12 | Section 16 |
| Decoupling patterns DP01, DP06, DP07, DP09, DP10, DP11, DP13, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P5-E2025-APP the classification, the extraction, the confidence, the review queue and JOB-12; RWB-S4-E2025-APP the legal action, the hearing and the judgment; RWB-S2-E2025-APP the treatment record; RWB-P5-E2025-CON the document and extraction contracts and their fakes; and RWB-ITG-E2025-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope

- Classification, the OCR text, the field patterns and their definitions, the confidence computation, the field state, the review queue and the JOB-12 intake window: RWB-P5-E2025-APP, with the contract in RWB-P5-E2025-CON.
- The reader of the checked fields that `rwb-litigation` and `rwb-treatment` call: RWB-P5-E2025-APP. This story proves what the log says about a field, not what a reader returns.
- The write of a legal action, a hearing and a judgment: RWB-S4-E2025-APP, in schema `rwb_litigation`.
- The write of the treatment record: RWB-S2-E2025-APP, in schema `rwb_treatment`.
- The parameters and the reference data — the threshold, the pass mark, the decision code list, the approval level list and the document type codes: `rwb-case` (P3) under DP-06 and DP-07, and `rwb-document` for the type table itself.
- The approval path, the `ApprovalWorkflow`, the approval queue SCR-10, the decision screen SCR-11 and the approval records: the other P7 stories of this service.
- The rule registry, the rule package versions, the rule rows and the rule test cases: the rule-governance stories of this service. This story reads no rule model and evaluates none.
- The daily hash-chain check JOB-14 at 02:00 and its compliance report: rwb-decision's decision-log baseline. This story appends entries that the check covers like any other.
- The data-lake copy of the decision log, JOB-13 and the retention of the lake partitions: retired with the data lake (DP-17); the ingest of the ledger is continuous Kafka.
- SCR-38 Decision log query, the auditor's view, the SCR-30 panel and the SCR-31 review queue: the screen stories and RWB-PLT-N001-CON.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E2025-ITG.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
- Electronic discovery and the court evidence attributes as extracted fields (REQ-DCM-017, REQ-DCM-018): they enter only as the document version and date an entry names, as the legacy story's section 19 fixes.
