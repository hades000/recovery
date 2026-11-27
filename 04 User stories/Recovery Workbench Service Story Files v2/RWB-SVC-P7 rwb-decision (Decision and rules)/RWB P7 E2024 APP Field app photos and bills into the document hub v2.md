# RWB-P7-E2024-APP Field app photos and bills into the document hub

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2024-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-024 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 |
| Parallel lane | L-P7-AE |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E2024-APP-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2024-CON, RWB-P4-E1037-CON, RWB-P3-E1043-CON, RWB-P3-E1042-CON |
| Contract version | v1 (the /v1 path on every REST row of sections 12.1 and 12.2); the minor version is Not specified in the source documents (DOR-RWB-P7-E2024-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DCM-013) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-024 for rwb-decision; the decision record of a field capture and its two reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2024-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (26 resolved, 21 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN) and the internal auditor (RW-AUDIT) who has to show what happened to an inspection**, I want **one decision record for every field capture the document hub stores on a case and one for every item it refuses, in the central decision ledger of `rwb-decision`, carrying the rule and its version, the inputs reference, the document and the client file ID, the capture kind and the final call, append only, hash chained and readable by case through `GET /api/recovery/decision/v1/decision-log`**, so that **an inspection is proved the day it is made — what was stored, what was refused and why — and no photo or bill on a case is a document nobody can explain**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-024:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record library of DP-03.
- One deliverable and nothing else: the field-capture decision record. For every document stored from a field capture and for every item the store refuses, the service appends one entry to `decision_log_entry` through the decision-record path of DP-03, carrying the case, the decision code, the rule id and rule version, the inputs reference, the object reference (the document ID of a stored capture, the client file ID of a refused item), the document type and capture kind, the final call and the message id of a refusal, with its hash-chain position; and it serves the two decision-log reads so the entries of a case can be read and one entry can be read with its inputs and versions.
- The decision code the entry carries is `DOCATT`, the attach entry the document store writes for a stored document (legacy section 4 step 6, section 11 and decision D-RCV-31). The legacy story's `Decision` field `D6.5` stays the routing-decision tag it is carried from and is not read as the code of this entry; which of the two the entry carries is Not specified in the source documents (GAP-1283; ASM-2275).
- One entry per stored document and one per item the store refuses; a `DUPLICATE` item resolves to the entry of the item received first and writes no second entry. Whether a refused item leaves an entry is Not specified in the source documents (GAP-1284; ASM-2276).
- What stays with `rwb-document` (P5, RWB-P5-E2024-APP with RWB-P5-E2024-CON): the field-capture endpoint, the manifest and file matching, the duplicate check on `client_file_id`, the file type and size checks, the clock skew and the age limit, the malware scan and the quarantine, the store, the capture columns and the partial unique index, the `DocumentStored` event, the OCR intake, the `UTILITY_BILL` extraction and the review queue, the SCR-30 panel and the switch `rwb.dochub.field-capture`. This story consumes those facts and decides none of them.
- What stays with `rwb-access` (P4, RWB-P4-E2024-APP): the authorise answer for capability area `DOCUMENTS` with rights `C`, `R` and `U`, the scope answer with the task on the case as the `OWN` test, the masking of `captured_at`, `capture_latitude`, `capture_longitude`, `capture_kind` and the review state, and the `AC-READ` and `AC-DENY` entries. This story consumes the answer for its reads and writes no access entry.
- What stays with `rwb-case` (P3, RWB-P3-E2024-APP): the case, its entry date, the field inspection task and its state, and the reference lists and parameters behind DP-06 and DP-07. This story reads none of them as a table.
- What stays with `rwb-agent` (P10): the agent policies, prompts and runs, and the agent version an entry may name in DF-DEC-007. No agent runs on the field-capture path, so this story writes no `agent_version`.
- The service records and exposes the decision; it changes no document, no capture row, no review item, no task and no case status (BR10).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1281; ASM-2272); this story uses the phrase "the rwb-decision login (DP-02)" and never the shared login of the legacy module.

The values carried from the legacy story are unchanged: case `RW-2026-000501` with entry date `2026-10-02` and a field inspection task for field collector `FC-01` with role `RW-FIELDCOL`, an inspection of ten synthetic files (eight `INSPECTION_PHOTO` and two `UTILITY_BILL`) synced at `2026-12-15 14:20` at latitude `13.7563` and longitude `100.5018`, a capture made with no signal at `2026-12-14 10:05` synced at `2026-12-15 08:30`, a utility bill showing amount `1,284.50` and due date `28/12/2569` read as `1284.50` and `2026-12-28`, the clock skew of 5 minutes and the age limit of 30 days, and case `RW-2026-000502` where `FC-01` has no task.

### 2. Business rationale

An inspection that reached the document hub without a record of it is evidence with no chain of custody, and a capture that was silently dropped is a visit the bank paid for and cannot show. The legacy story proved the capture; this slice proves the record of it. Today the decision is written inside the same monolith transaction as the document, so the two cannot be told apart in an audit, and an item the store refused leaves no trace at all. Under Architecture v5 the store is `rwb-document`'s and the ledger is `rwb-decision`'s, so the explanation has to live in the one place every service's record is collected and read: the central decision ledger of `rwb-decision`, through `GET /api/recovery/decision/v1/decision-log`.

This story carries the record half of REQ-DCM-013 and the measure `Decisions within the delegation of authority` at 100 percent for the field-capture path. It carries CTL-11 (the GPS position and the photos of a home are personal data, masked by role and never logged) on the record side, NFR-033 (every decision reproducible from the log, with the versions and the inputs), NFR-035 (the chain is checked daily) and the principle that no action stands without its record (legacy BR10, R-UNI-39, R-UNI-40).

The realignment changes the mechanism, not the business rule:

1. The in-process decision-log write of the monolith becomes the decision record of the owning service: `rwb-document` writes its local record in the same transaction as the document, publishes `DecisionRecorded` on `rwb.decision-record.v1`, and this service appends the entry to the central ledger through the library of DP-03, with the append-only rule and the hash chain that FEAT-DRI-01 and FEAT-DRI-03 already carry (Architecture v5 slide 28).
2. The refusal is recorded rather than discarded: an item the store refuses is a decision the service declined to take, so it leaves one entry with its message id and no document reference, and an auditor can count refusals per case instead of inferring them from an absence.
3. The entry never becomes a copy of the capture: the position, the file, the photo and the bill value stay in `rwb_document`, and the entry names the field, the type and the version that decided it (legacy BR9; CTL-11; DL26).
4. The decision code and the final calls are reference data of `rwb-case` read through DP-07, and the ledger's completeness target and chain-check time are parameters read through DP-06, so none of them is a constant of this service (legacy BR1 to BR10 as data; principle 1).
5. The one decision-log read of the monolith becomes two operations on the service's own base (DP-13 through the base of section 12.1), reached through the gateway-bff composite route the screens already use (DP-19); the nightly copy of the log to the data lake is retired with the data lake (DP-17), and the ingest of `rwb.decision-record.v1` is continuous Kafka as JOB-13 states.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2024-CON | The published field-capture contract of `rwb-document` (P5): the case `RW-2026-000501` with entry date `2026-10-02`, the ten items of the inspection (eight `INSPECTION_PHOTO` and two `UTILITY_BILL`) with capture time `2026-12-15 14:20` at `13.7563` and `100.5018`, the offline capture at `2026-12-14 10:05` synced at `2026-12-15 08:30`, the `DUPLICATE`, `REFUSED` and `QUARANTINED` item results with their message ids, the out-of-scope case `RW-2026-000502`, and the `DecisionRecorded` fact of a capture on `rwb.decision-record.v1` with its contract fakes. Which fields of that fact this service consumes is Not specified in the source documents (GAP-1281; ASM-2271), and the fact set this story assumes is that of ASM-2271 |
| RWB-PLT-E1027-CON | The decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule and the fail-closed exception the store's transaction rolls back on |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the completeness target of the ledger ingest (5 minutes, Architecture v5 slide 28) and the daily chain-check time (02:00, JOB-14) with the version in force on the business date; the parameter names are Not specified in the source documents (GAP-1281; ASM-2273) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): the decision code list `LOV-DECISION` of TSD P7 v2 T3.2 and the document type codes with the version in force. The list carries the value `DOCATT` on every document-attach entry (GAP-1283); the legacy Decision tag D6.5 is the routing decision that produced the capture and is not the entry code |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one entry under a repeated fact, and the outbox row of the append |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-P4-E1037-CON | The authorise contract of `rwb-access` (P4) and its cached answer behind the two reads: capability area `DECISION_LOG`, right `R`, scope applied (GAP-1282; ASM-2274) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19): the route the reader of a case reaches the two decision-log operations through |

Business preconditions carried from RWB-E2-024:

- Case `RW-2026-000501` exists with entry date `2026-10-02` and a field inspection task for field collector `FC-01` with role `RW-FIELDCOL`, so the case is in that collector's `OWN` scope (legacy section 7 Background). The case and the task are `rwb-case`'s and reach this service as facts.
- The document type rows `INSPECTION_PHOTO` with no fields, `INSPECTION_CHECKLIST` with no fields and `UTILITY_BILL` with `bill_amount`, `due_date` and `account_ref` are in force as reference data (legacy section 3). The types are the store's and are named on the entry; this story classifies nothing.
- The parameters `CAPTURE_CLOCK_SKEW_MINUTES` 5, `CAPTURE_MAX_AGE_DAYS` 30, `CAPTURE_MAX_FILES` 50 and `INTAKE_MAX_FILE_MB` 25 are in force through the parameters contract (legacy sections 3 and 13; DL11). They are the store's checks; this story records their outcome and holds no default of its own.
- The bill of the inspection shows amount `1,284.50` and due date `28/12/2569`, read by `rwb-document` as `1284.50` and `2026-12-28`; the entry names the document and the type and carries no bill value (BR9).
- The decision-log operations exist with the access TSD P7 v2 T-A.1 fixes for them: capability area `DECISION_LOG`, right `R`, scope applied. Every role of TSD P7 v2 T6.1 holds `R`, and a role outside the matrix holds none.
- No build dependency and no integration dependency. Day 1: the story builds against RWB-P5-E2024-CON and its fakes, and against the platform contracts of section 13.

### 4. Flow

1. Field collector: `FC-01` captures eight photos and two bills in the field app, ten synthetic files in the test data, and the app syncs them at `2026-12-15 14:20`; the capture, the scan and the store are `rwb-document`'s and are not rebuilt here.
2. `rwb-document` (P5): runs the manifest, duplicate, type, size, time and position checks and the malware scan, stores each accepted item, sets the capture columns, and for each stored item and each item it refuses writes its local decision record in the same transaction as the change (legacy section 4 steps 4 to 8; BR1).
3. `rwb-document` publishes `DecisionRecorded` on `rwb.decision-record.v1` for each of those records, keyed by the case ID, in the same transaction as its outbox row (DP-03, DP-09; Architecture v5 slide 28).
4. `rwb-decision` `FieldCaptureDecisionListener`: reads the fact into the inbox of DP-09, deduplicates by event ID and by the idempotency key the fact carries (R-UNI-40), and passes the decision facts to `FieldCaptureDecisionRecorder`: the case, the decision code, the object reference (document ID or client file ID), the document type and capture kind, the final call, the message id of a refusal, the rule id and rule version, the actor reference, the capture time and the inputs reference.
5. `FieldCaptureDecisionRecorder`: reads the decision code list and the document type codes through the reference-data contract of DP-07 and the ledger parameters through the parameters contract of DP-06, at the version in force on the business date, and composes the entry. It decides nothing about the capture: it applies no threshold, no clock skew and no age limit, and it holds no copy of the store's rules (BR2, BR11).
6. `DecisionLogAppender`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash`, computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with its `inputs_ref`, and writes the outbox row of the append. A failed append changes nothing: no entry, no chain position and no outbox row (DP-03; R-UNI-39; BR13).
7. `DecisionLogAppender`: a repeated fact with the same idempotency key returns the first entry's ID, adds one to the repeat count for R-UNI-40, and appends nothing (BR14).
8. When the append cannot be made, the decision-record library raises `DecisionLogUnavailableException` to its caller inside the store's transaction, and the caller answers MSG-P7-003: the item is refused, nothing is stored for it, and an incident is raised (legacy X12; BR4).
9. `FieldCaptureCompletenessChecker`, on the ingest window of the ledger: reads `GET /api/recovery/document/v1/cases/{caseId}/documents` for the case and compares the documents the case holds with the DOCATT entries of the case, and reports a document with no entry as a gap, which is the missing-record alert of Architecture v5 slide 28 (BR12, X8).
10. An auditor or a case owner reads the entries with `GET /api/recovery/decision/v1/decision-log` by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, each guarded by the authorise answer of DP-11 and refused with MSG-P4-002 or MSG-P4-003 as section 14 states (BR15).
11. Nothing in this story moves a document, a capture row, a review item, a task or a case: the entry is appended beside them, and the readers of the screens keep reading the capture facts through `rwb-document`'s contract (BR10).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The store refuses an item for its type, its size, its capture time or its position | The refusal leaves one entry with `finalCall` `REFUSED`, the message id of the refusal and the client file ID, and no document reference; the other items are unaffected | MSG-P5-001, MSG-P5-016, MSG-P5-017, MSG-GEN-002, MSG-GEN-003 (produced by `rwb-document`) | AC2, TC-E2-024-07 to TC-E2-024-11 |
| X2 | The same client file ID is sent again, and the store answers `DUPLICATE` | No second entry is written; the entry of the item received first stands, and the chain of the case is unchanged | None | AC3, TC-E2-024-04, TC-E2-024-05 |
| X3 | The same `DecisionRecorded` fact is delivered again or replayed from the topic | One entry exists; the inbox dedupe and the idempotency key both hold, and the repeat is counted for R-UNI-40 | None | AC3, TC-E2-024-04 |
| X4 | The record cannot be written, because the library is unavailable or the chain cannot be taken | Nothing is written: no entry, no chain position, no outbox row; the item is refused and nothing is stored for it, and an incident is raised | MSG-P7-003 | AC5, TC-E2-024-17 |
| X5 | An entry names a rule id with no rule version, or a decision code outside the list in force | The append is refused with MSG-P7-009 naming `ruleVersion` or `decisionCode`, and nothing is written | MSG-P7-009 | AC1 |
| X6 | A caller attempts to change or delete an entry | The statement is refused, by the missing grant for the service login and by the append-only rule of the table; a correction is a new entry naming the one it corrects in `corrects_entry_id` | None | AC4 |
| X7 | The fact carries no object reference, or names a case the document contract does not confirm | The append is refused for that fact and the incident names the fact ID; no entry is written on a guessed document or a guessed client file ID | MSG-GEN-006 | AC1 |
| X8 | The documents of a case and the DOCATT entries of the case do not agree inside the ingest window | The checker reports the document with no entry as a gap and raises the missing-record alert; no entry is invented for it | MSG-GEN-006 | AC1 |
| X9 | The decision code list or the parameters cannot be read at the version in force | The append is refused and the fact is retried; no entry is written with an assumed code or an assumed version | MSG-GEN-006 | AC1 |
| X10 | The caller holds no right in the `DECISION_LOG` area, or asks for a case out of scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; nothing is returned | MSG-P4-002, MSG-P4-003 | AC8, TC-E2-024-16 |
| X11 | A request never reached the store: a manifest and file mismatch, too many files, or a case outside the collector's scope | No `DOCATT` entry exists for it, because no decision was taken; the refusal is the store's or the access answer's and is recorded there | MSG-GEN-001, MSG-GEN-002, MSG-P4-003 (produced by `rwb-document` and `rwb-access`) | AC9, TC-E2-024-12, TC-E2-024-14, TC-E2-024-15 |

An entry is only ever appended beside the fact that caused it: the entry, its chain position and its outbox row commit in one transaction, so a fact can never leave a half record and a record can never exist for a capture that was not decided (BR13).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the field-capture contract of RWB-P5-E2024-CON, the platform contract libraries of its DP table and the fakes; no capture, scan, store, intake, extraction, review, case or access behaviour is rebuilt here |
| Negotiable | The decision code, the final call set, the parameter names, the document types and the message ids are data or parameters of their owners; the story fixes only the record, the append-only rule, the chain, the fail-closed refusal and the two reads |
| Valuable | Every capture on a case, stored or refused, can be explained, counted and shown unchanged to an auditor |
| Estimable | One listener, one recorder, one appender with the chain, one query controller with two operations, one completeness checker, one migration, one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the seven criteria in section 7 runs as one automated test against the contract fakes with a fixed business date and a fixed chain |

### 7. Acceptance criteria

```gherkin
Feature: Field app photos and bills into the document hub — the rwb-decision field-capture decision record

  Background:
    Given the environment is SIT
    Given the rwb-case reference-data contract mock returns the document types INSPECTION_PHOTO, INSPECTION_CHECKLIST and UTILITY_BILL in force, with no fields for INSPECTION_PHOTO and INSPECTION_CHECKLIST and with bill_amount, due_date and account_ref for UTILITY_BILL
    Given the rwb-case parameters contract mock returns the clock skew of 5 minutes, the age limit of 30 days and the file limit of 50 in force

  Scenario: AC1 Ten DOCATT records for one inspection, chained and readable (new, D-RCV-60)
    Given the rwb-document contract mock returns case "RW-2026-000501" with entry date 2026-10-02 and ten documents stored from the sync at 2026-12-15 14:20, eight "INSPECTION_PHOTO" and two "UTILITY_BILL", each with source "UPLOAD", its client file ID, capture time 2026-12-15 14:20, latitude 13.7563 and longitude 100.5018
    Given the rwb-case reference-data contract mock returns the decision code list in force and the rwb-case parameters contract mock returns the ledger parameters in force
    When the ten DOCATT records of that sync reach rwb.decision-record.v1 as DecisionRecorded facts
    Then ten decision_log_entry rows exist in rwb_decision for case "RW-2026-000501" with decision code "DOCATT", one per stored document, each keyed by its document ID and its client file ID
    Then each entry carries the ruleId and ruleVersion in force, the inputsRef, the document type ("INSPECTION_PHOTO" or "UTILITY_BILL"), the capture kind, the actor reference "FC-01" and finalCall "ACCEPTED"
    Then each entry carries chain_seq, prevHash and entryHash, every prevHash equals the entryHash of the entry before it, and the first prevHash is 64 zeros
    Then GET /api/recovery/decision/v1/decision-log for case "RW-2026-000501" returns the ten entries in chain order, and GET /api/recovery/decision/v1/decision-log/{entryId} returns one with its rule, its version, its inputsRef, its document reference and its decidedAt

  Scenario: AC2 An item the store refuses is recorded too (new, D-RCV-60)
    Given the rwb-document contract mock returns case "RW-2026-000501" with nine items accepted and one item refused with "MSG-P5-001" and no document written for it, each with its client file ID
    When the ten DOCATT records of that sync reach rwb.decision-record.v1 as DecisionRecorded facts
    Then ten entries exist for the case: nine with finalCall "ACCEPTED" and a document reference, and one with finalCall "REFUSED", the messageId "MSG-P5-001", its client file ID and no document reference
    Then the entry of the refused item is readable with GET /api/recovery/decision/v1/decision-log/{entryId} and names no document, no file name and no position
    Then the case has the nine documents of the store and one recorded refusal, and the two counts agree

  Scenario: AC3 A repeated item and a redelivered fact write no second record (new, D-RCV-60)
    Given the ten entries of AC1 exist for case "RW-2026-000501"
    When the field app sends the same ten client file IDs again and the rwb-document contract mock answers "DUPLICATE" with the first document ID for each of the ten
    When the same DecisionRecorded fact of one of the ten is delivered again on rwb.decision-record.v1
    Then no second decision_log_entry is written for any of the ten documents and the count for the case stays ten
    Then the repeat of the fact returns the first entry's ID and adds 1 to the repeat count for R-UNI-40
    Then the chain of the case is unchanged and GET /api/recovery/decision/v1/decision-log returns the same ten entries

  Scenario: AC4 The record cannot be changed (new, D-RCV-60)
    Given one entry of AC1 with its chain_seq, its prevHash and its entryHash
    When an UPDATE setting final_call and a DELETE of that entry are attempted through the rwb-decision login (DP-02) and again through the schema owner role
    Then all four statements are refused, the first two by the missing grant for the service login and the last two by the append-only rule of the table
    Then the entry is unchanged and its entryHash still equals the SHA-256 of its canonical form
    Then the refused attempts are written to the ACE audit log with the table, the operation and the entry ID

  Scenario: AC5 A record that cannot be written refuses the item (new, D-RCV-60)
    Given the rwb-document contract mock returns three items of case "RW-2026-000501"
    Given the decision-record library fake is forced to fail the record write
    When the store asks for the three records of the three items inside its transaction
    Then the call returns status 503 with "MSG-P7-003" and no item is accepted
    Then no decision_log_entry exists for any of the three items and no chain_seq is used
    Then no document, no capture row and no intake item is written for the three items
    Then an incident is raised for the failed record

  Scenario: AC6 The record carries no position, no file name and no bill value (new, D-RCV-60)
    Given the ten entries of AC1 and the ten DecisionRecorded payloads that produced them
    When the entries, the payloads and the log lines of this story are inspected
    Then they carry the case reference, the document reference, the client file ID, the document type, the capture kind, the capture time, the rule and rule version, the inputsRef, the actor reference, the final call and dates only
    Then neither "13.7563" nor "100.5018", no file name, no photo and no bill value of "1,284.50" appears in any of them
    Then the position, the file and the bill value stay in rwb_document

  Scenario: AC7 A capture made with no signal keeps its own capture time (new, D-RCV-60)
    Given the rwb-document contract mock returns the two documents of the offline capture, captured at 2026-12-14 10:05 with no signal and stored at 2026-12-15 08:30
    When the two DOCATT records reach rwb.decision-record.v1 as DecisionRecorded facts
    Then each entry carries the capture time 2026-12-14 10:05 as recorded at capture and the decidedAt 2026-12-15 08:30
    Then the server replaced no device time, because the entry's capture time equals the value the store sent
    Then the two entries are read for case "RW-2026-000501" beside the ten entries of the first sync

  Scenario: AC8 A read without the DECISION_LOG right or outside the scope is refused (new, D-RCV-60)
    Given the rwb-access contract mock returns no right in the DECISION_LOG area for role "RW-FIELDCOL" on case "RW-2026-000501" and returns case "RW-2026-000502" outside the scope of "FC-01"
    When GET /api/recovery/decision/v1/decision-log for case "RW-2026-000501" is called by the field collector "FC-01"
    Then the call returns 403 with "MSG-P4-002" and nothing is returned
    When GET /api/recovery/decision/v1/decision-log for case "RW-2026-000502" is called by "FC-01"
    Then the call returns 404 with "MSG-P4-003" and nothing is returned
    Then the rwb-document contract mock is never called

  Scenario: AC9 A request that never reached the store is refused by its owner, not decided (new, D-RCV-60)
    Given the rwb-document contract mock refuses a request of case "RW-2026-000502" before the store takes it, with "MSG-GEN-002"
    When the field app sends the request of case "RW-2026-000502" for "FC-01"
    Then no decision_log_entry exists for case "RW-2026-000502" with decision code "DOCATT"
    Then no chain_seq is used, and the refusal is recorded by rwb-document and rwb-access, not by this story

  Scenario: AC10 The decision code is read from reference data, a missing record is reported and nothing else is written (new, D-RCV-60)
    Given the rwb-case reference-data contract mock returns the decision code list in force without "DOCATT"
    When the ten DOCATT records of that sync reach rwb.decision-record.v1 as DecisionRecorded facts
    Then each is refused with "MSG-P7-009" naming "decisionCode" and no decision_log_entry is written
    Given the ten entries of AC1 exist for case "RW-2026-000501" and the rwb-document contract mock lists one document of that case with no DOCATT entry
    When the completeness checker runs over the ingest window
    Then the document with no entry is reported as a gap and alerted, and no entry is written for it
    Then the story writes no row of rwb_document, rwb_case or rwb_access and reads no table of another service

  Scenario: AC11 The rules without a criterion of their own hold on the record path (new, D-RCV-60)
    Given the ten entries of AC1 exist for case "RW-2026-000501" and the rwb-case reference-data contract mock returns the decision code list in force
    When the same DecisionRecorded fact of one of the ten is delivered again and the rwb-document contract mock lists one document of case "RW-2026-000501" with no DOCATT entry
    Then each entry is appended on rwb.decision-record.v1 with the rule and version in force, and its entry, chain position and outbox row commit together (BR1, BR2, BR13)
    Then the repeat adds no entry and adds 1 to the repeat count for R-UNI-40 (BR14)
    Then the document with no entry is reported as a gap and alerted, and no entry is written for it (BR12)
    Then the decision code is read from the reference list in force, and each entry is append only with its entryHash equal to the SHA-256 of its canonical form (BR8, BR5)
    Then the story writes no row of rwb_document, rwb_case or rwb_access and reads no table of another service (BR10)

  Scenario: AC12 A call with no authenticated session is refused with 401 (new, D-RCV-60)
    Given no authenticated session is presented to the two provided operations of section 12.1
    When GET /api/recovery/decision/v1/decision-log is called with no session
    Then the call returns 401 with "Not specified in the source documents (NEWAC-RWB-P7-E2024-APP-AC11)" and nothing is returned
    Then the rwb-access contract mock is never called
    Then the 403 and 404 answers of the same operations are those of AC8
```

These twelve criteria are new for the `rwb-decision` slice of RWB-E2-024 and are the record and read criteria of the key. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key stores, scans, extracts or refuses a capture, and those changes belong to RWB-P5-E2024-APP, RWB-P4-E2024-APP and RWB-P3-E2024-APP. The values are the legacy values of RWB-E2-024 — case `RW-2026-000501` with entry date `2026-10-02`, field collector `FC-01` with role `RW-FIELDCOL`, the ten items (eight `INSPECTION_PHOTO`, two `UTILITY_BILL`), the three document types, the syncs at `2026-12-15 14:20` and `2026-12-15 08:30`, the capture at `2026-12-14 10:05`, latitude `13.7563` and longitude `100.5018`, the bill amount `1,284.50`, the clock skew of 5 minutes and the age limit of 30 days, and the messages MSG-P5-001, MSG-P7-003 and MSG-P7-009 — and no new business value is introduced.

The decision code `DOCATT` and the final call set `ACCEPTED`, `REFUSED` and `QUARANTINED` are the reading of ASM-2275 and ASM-2276 and are carried in GAP-1283 and GAP-1284; the payload field set of the entry, the read shape, the message id set, the panel id, the parameter names and the login name have no source and are carried in GAP-1281 with ASM-2271, ASM-2272 and ASM-2273.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every document stored from a field capture and every item the store refuses leaves exactly one decision record; no capture is stored and no refusal is returned without it, and the record and the change are written in the same transaction | Legacy BR10; R-UNI-39; FSD P7 v3 A2.2; FEAT-DRI-02 |
| BR2 | The record is written on the decision-record path of DP-03: it is appended to the chain, it names the rule and the rule version in force, and the entry, its chain position and its outbox row commit together or not at all | FSD P7 v3 A2.1 and A2.3; TSD P7 v2 T5.3; DP-03 |
| BR3 | The entry names the case, the decision code, the object reference, the document type, the capture kind, the final call, the rule id and version, the inputs reference, the actor reference, the capture time and the decided time | TSD P7 v2 T3.1; legacy section 11; ASM-2271 |
| BR4 | A record that cannot be written refuses the item: the library raises `DecisionLogUnavailableException`, the store's transaction rolls back, the answer is MSG-P7-003 and an incident is raised; no item stands unlogged | Legacy X12 and TC-E2-024-17; FSD P7 v3 VR-P7-001-2 and AC-EXC-P7-002-02; principle 5 |
| BR5 | The entry is append only and hash chained: an UPDATE and a DELETE are refused, a correction is a new entry naming the one it corrects in `corrects_entry_id`, and every `entry_hash` is the SHA-256 of the entry's canonical form | FEAT-DRI-01; FSD P7 v3 AC-P7-001-01 and AC-ALT-P7-001-01; NFR-035 |
| BR6 | One entry per stored document and one per refused item, keyed on the object reference; a `DUPLICATE` item resolves to the entry of the item received first and writes none, and a repeated fact writes none | Legacy BR4; R-UNI-40; ASM-2276 |
| BR7 | The capture time is the device time recorded at capture, stored as sent; the server never replaces it, and the decided time is the server's | Legacy BR2 and section 17; FEAT-DCM-21 |
| BR8 | The decision code and the final call values are reference data of the `rwb-case` reference-data contract, not constants: an unknown code is refused with MSG-P7-009 naming `decisionCode`, and a rule id with no version with MSG-P7-009 naming `ruleVersion` | FSD P7 v3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05; BR-P7-001; DP-07 |
| BR9 | No personal data in the entry, the fact, the outbox or the logs: the position, the file name, the photo and the bill value stay in `rwb_document`, and the entry carries references, codes, the capture kind and dates only; the P2 fields classed as personal data are carried in none of them | Legacy BR9 and section 17; CTL-11; DL26; NFR-033 |
| BR10 | The story records and exposes; it writes no document, no capture row, no intake item, no review item, no task and no case status, and it reads no table of another service | Architecture v5 slides 14 and 41; DP-01 |
| BR11 | The service applies no capture rule: the type, the size, the clock skew, the age limit, the duplicate check and the malware result are `rwb-document`'s, and the entry copies their outcome | Legacy BR1, BR3, BR4; FSD P4 v3 A2.4 VR-P4-004-1 |
| BR12 | The ledger is reconciled: the documents of a case are compared with the DOCATT entries of the case inside the ingest window, and a document with no entry is reported as a gap and alerted; no entry is invented for it | Architecture v5 slide 28; NFR-035; ASM-2273 |
| BR13 | The entry, its chain position and its outbox row are written in one transaction; a failed append leaves nothing and the fact is redelivered | Principle 5; R-UNI-39; DP-03 |
| BR14 | One entry per fact under a repeated delivery: the inbox dedupe and the idempotency key make a second entry impossible, and the repeat is counted | FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40 |
| BR15 | The two reads declare the `DECISION_LOG` capability area and the right `R` with the scope applied; a role outside the matrix is refused with MSG-P4-002 and a case out of scope with MSG-P4-003 | TSD P7 v2 T-A.1 and T6.1; legacy section 10 |

Target-service statements that make the rules hold in `rwb_decision`:

- BR1 and BR2 are one append on the `DecisionRecorded` fact of the owning service, through the library of DP-03; the store's transaction is `rwb-document`'s and this story supplies the path, its fail-closed contract and its exception.
- BR3 is the entry composition: the columns of TSD P7 v2 T3.1 plus the object reference and the capture facts of the assumed shape of ASM-2271.
- BR4 is the exception mapping: `DecisionLogUnavailableException` from the library becomes MSG-P7-003 for the item and an incident for the platform administrator queue.
- BR5 is the table's append-only trigger `tr_declog_append_only` and the missing `UPDATE` and `DELETE` grant on the service login, both inherited from the decision-log baseline.
- BR6 is the partial unique key on the object reference and the inbox dedupe by event ID and idempotency key.
- BR8 is a read of the reference-data contract of DP-07 at the version in force; the Java code holds no decision code and no final call value.
- BR9 is a check on the entry writer: the entry's canonical form is built from references and codes, and a test scans the entry, the fact and the log line for any digit of `13.7563` and `100.5018` and for `1,284.50`.
- BR12 is the completeness checker of flow step 9: one read of the document contract per case per window, one comparison, one gap alert.
- BR15 is the guard on the two reads, inherited from the decision-log baseline's authorise path.

### 9. State transitions

None for a document, a capture row, a review item, a task or a case. The states below are the states of an entry of this story, and the entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A `DecisionRecorded` field-capture fact arrives | The decision code, the rule version and the object reference are readable at the version in force | Appended, with the next `chain_seq`, its `prev_hash` and its `entry_hash`, in one transaction with its outbox row |
| Absent | A `DecisionRecorded` field-capture fact arrives | The decision code is unknown, or the rule id has no version, or the object reference is absent | Absent: refused with MSG-P7-009 or MSG-GEN-006, and nothing is written |
| Absent | A `DecisionRecorded` field-capture fact arrives | The library is unavailable or the chain cannot be taken | Absent: MSG-P7-003 for the item, nothing stored, and the fact stays for redelivery |
| Appended | The same fact arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A correction of the decision is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`, and the corrected entry stays unchanged |
| Appended | An UPDATE or a DELETE is attempted | Any caller, including the schema owner | Unchanged: the statement is refused by the append-only rule |

The capture itself moves through `rwb-document`'s states — received, scanned, stored, intake item, extracted, in review — and the case stays in its stage; this story changes none of them (BR10, BR11).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-AUDIT, internal audit | Reads the DOCATT entries of a case and one entry with its inputs reference, its versions and its chain position (`DECISION_LOG` R), with scope `ALL` |
| RW-COMPLY, Compliance and PDPA officer | Reads the same, without a position, a file name or a bill value, which the entry never carries (`DECISION_LOG` R) |
| RW-CASEOWN, case owner | Reads the entries of the cases in own scope and shows the inspection beside the documents on the case (`DECISION_LOG` R) |
| RW-RESTRUCT, restructuring officer (FCR) | Reads the entries of a deed in lieu case in scope (`DECISION_LOG` R) |
| RW-FIELDCOL, field collector | Named on the entry as its actor reference; sends the capture through `rwb-document` and reads the entry only where its scope and the matrix allow |
| Every role of TSD P7 v2 T6.1 | Holds `R` on the decision log and reads the entries of the cases in its scope |
| A role outside the matrix, or a case out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, and appends the entry and its outbox row (DP-02) |
| The decision-record library identity | Provides the chain position, the `prev_hash`, the `entry_hash` and the fail-closed exception of the append (DP-03) |
| `rwb-document` | Owns the capture, the scan, the store, the capture columns, the intake, the extraction, the review queue and the SCR-30 panel; this story holds no authority over any of them |
| `rwb-access` | Owns the authorise, scope and masking answers and the access entries; this story consumes the answer for its reads and writes no entry |
| `rwb-agent` | Owns the agent version an entry may name; no agent runs on this path |
| No approval level from the delegation of authority applies | The field-capture decision is a system decision and carries no approver; the approval path of this service is another story's |

The authorisation decision behind the two reads is `rwb-access`'s role, scope and right data, taken through the authorise contract of DP-11 and the guard the service's decision-log baseline already carries; this story adds no guard of its own and holds no role, scope or delegation row (ASM-2274). The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1281; ASM-2272); the story refers to "the rwb-decision login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id (the case of the capture) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code (`DOCATT`) | Write |
| DF-DEC-004 | `decision_log_entry` | rule_id (the rule that decided the item) | Write |
| DF-DEC-005 | `decision_log_entry` | rule_version (the version of that rule) | Write |
| DF-DEC-006 | `decision_log_entry` | model_version | Not written: no model decides a field capture |
| DF-DEC-007 | `decision_log_entry` | agent_version | Not written: no agent runs on this path |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the capture facts and their freshness) | Write |
| DF-DEC-009 | `decision_log_entry` | recommendation (the document type, the capture kind and the item result) | Write |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Not written: no approver |
| DF-DEC-011 | `decision_log_entry` | approval_level | Not written: no delegation level applies |
| DF-DEC-012 | `decision_log_entry` | final_call (`ACCEPTED`, `REFUSED` or `QUARANTINED`) | Write |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written: there is no override of a capture |
| DF-DEC-014 | `decision_log_entry` | actions (the object reference, the client file ID and the message id of a refusal) | Write |
| DF-DEC-015 | `decision_log_entry` | outcome | Write where the store names one |
| DF-DEC-016 | `decision_log_entry` | decided_at (the receipt and store time) | Write |
| DF-DEC-017 | `decision_log_entry` | prev_hash | Write |
| DF-DEC-018 | `decision_log_entry` | entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id (the field collector reference, or the service identity of a store-side refusal) | Write |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write |
| (assumed column) | `decision_log_entry` | object_ref (the document ID of a stored capture, the client file ID of a refused item), doc_type_code, capture_kind, capture_time, message_id | Write; the columns are Not specified in the source documents (GAP-1281; ASM-2271) |
| DF-DOC-001, DF-DOC-002, DF-DOC-004, DF-DOC-006, DF-DOC-010 | `document` (P5) | id, case_id, document_type, storage_ref, write_once | Read through the document contract of RWB-P5-E2024-CON, never a table |
| DF-DOC-027 to DF-DOC-031 | `document` (P5) | captured_at, capture_latitude, capture_longitude, client_file_id, capture_kind | Named on the entry as facts; the values are never copied into an entry (BR9) |
| DF-REF-219, DF-REF-224, DF-REF-246 | `document_type`, `document_hub_parameter` (P5) | doc_type_code, field_definitions, param_value | Read as facts of the document contract, with the version in force |
| (reference lists) | reference data (P3) | the decision code list `LOV-DECISION` with the version in force | Read through the reference-data contract of DP-07, never a table |
| (parameters) | `parameter_value` (P3) | the ledger ingest target 5 minutes and the chain-check time 02:00 with the version in force | Read through the parameters contract of DP-06, never a table |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_decision` | the append row | Write |

No row of `document`, `document_intake`, `document_field`, `document_type`, `document_hub_parameter`, `recovery_case`, `task`, `role`, `permission` or `masking_rule` is copied into `rwb_decision`: the capture facts arrive on the document contract and on `rwb.decision-record.v1`, and the other services' tables are never queried. Field IDs are those of the Logical Data Model and Data Dictionary v9; the object reference, the capture facts and the message id of a refusal have no field ID in TSD P7 v2 T3.1 and are written from the assumed shape of section 12.1, which is Not specified in the source documents (GAP-1281; ASM-2271).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007); this story fills them with the DOCATT entries of a field capture and adds no third path. The request and response field set of a field-capture entry is Not specified in the source documents (GAP-1281; ASM-2271).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the decision log by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and by the object reference of a field-capture entry; 200 with the DecisionLogPage | `DECISION_LOG`, right `R`, scope applied through the authorise contract | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs reference, its rule and version, its object reference, its capture facts, its final call and its hash chain; 200 with the DecisionLogEntry | `DECISION_LOG`, right `R`, scope applied | Not applicable, read only |

The DecisionLogEntry body this story reads and writes carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `inputsRef`, `recommendation` with the document type, the capture kind and the item result, `finalCall`, `objectRef`, `clientFileId`, `docTypeCode`, `captureKind`, `captureTime`, `messageId`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`. The DecisionLogPage body carries `items`, `page`, `size` and `total`. The object-reference filter of the search, the field names of the entry and the final call set are Not specified in the source documents (GAP-1281; ASM-2271).

Errors: 401 no session (Not specified in the source documents (CG-ALL-7276)); 403 the role lacks the right (MSG-P4-002); 404 the entry or the case is absent or out of scope (MSG-P4-003); 422 a query value is outside its list (MSG-GEN-001); 503 the log is unavailable (MSG-GEN-006) or the append could not be made (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document, on RWB-P5-E2024-CON | The documents the case holds, with their type, source, capture time and review state, for the completeness check of the ledger (BR12, X8); faked, one hop, 2 s timeout (DP-11) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access, on RWB-P4-E1037-CON | The cached role, scope and right decision behind the two reads: area `DECISION_LOG`, right `R` (BR15); faked. The contract is added by the DP table and is not in the metadata rows (GAP-1282; ASM-2274) |

The reference lists of `rwb-case` (DP-07, RWB-P3-E1043-CON) and the parameters of `rwb-case` (DP-06, RWB-P3-E1042-CON) are read in process through their client libraries, with their contract fakes, and are not cross-service REST rows; the capture facts arrive on `rwb.decision-record.v1` and not over REST. The contract dependency recorded on the story is RWB-P5-E2024-CON; the platform and published contracts the DP table adds are listed in section 13 and carried in the gap of GAP-1282.

#### 12.3 Events published

None. This story publishes no event of its own: the field-capture decision is a fact of `rwb-document` and the entries of the central ledger are read through the operations of 12.1. `DecisionRecorded` on `rwb.decision-record.v1` is published by the owning service of each decision, and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42). The `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` events of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger library, published by `rwb-document` for these decisions | `FieldCaptureDecisionListener`: inbox dedupe by event ID, then `FieldCaptureDecisionRecorder` and `DecisionLogAppender` for the object reference, the document type, the capture kind, the final call, the message id, the rule and version and the capture time |

The fact carries IDs, codes, versions, a message id and a time only; no file, no photo, no position and no bill value travels on the topic (BR9). Which fields of the fact this service requires, and whether the document reference travels on the fact or is read through the document contract, is Not specified in the source documents (GAP-1281; ASM-2271); the reading this story applies is that of ASM-2271 and the document read of 12.2 covers the gap.

#### 12.5 Workflows and activities

None of this story's own. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09; the store's transaction is `rwb-document`'s and this story neither starts nor signals it. The `DocumentIntakeWorkflow` on queue `rwb-document` is `rwb-document`'s and is observed through the document contract, not built here. This story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit.

#### 12.6 Schedules

None. The ingest of `rwb.decision-record.v1` is continuous Kafka, as JOB-13 states (Architecture v5 slide 44); the daily hash-chain check JOB-14 at 02:00 and the rule promote JOB-20 at 00:01 are `rwb-decision`'s decision-log and rule-governance baselines, and they cover the entries of this story like any other without being rebuilt or scheduled here. This story creates no Temporal Schedule and starts nothing on a clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The field-capture entry, its object reference, its chain position, its hashes, its inputs reference and its final call; append only |
| decision record (local library) | P7 rows in `rwb_decision`, written through the decision-record library | The append of DP-03 and its hash chain |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `document`, `document_intake`, `document_field`, `document_type` and `document_hub_parameter` (P5), `recovery_case`, `task`, `timer` and `parameter_value` (P3), and `role`, `permission` and `masking_rule` (P4). The other P7 tables — `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` — are not touched by this story. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document field-capture WireMock | RWB-P5-E2024-CON | Case `RW-2026-000501` with entry date `2026-10-02` and a field inspection task for `FC-01`; the ten items (eight `INSPECTION_PHOTO`, two `UTILITY_BILL`) with capture time `2026-12-15 14:20` at `13.7563` and `100.5018`; the offline capture at `2026-12-14 10:05` stored at `2026-12-15 08:30`; the `DUPLICATE` answer for the resent ten client file IDs; one item refused with `MSG-P5-001`; the three-item sync of the forced record failure; the case `RW-2026-000502` with no task for `FC-01`; and the document list of a case for the completeness check |
| rwb-access authorise fake | RWB-P4-E1037-CON, DP-11 | The allow answer for `DECISION_LOG` right `R` in scope, the refusal of a role without the right with MSG-P4-002, and the refusal of a case out of scope with MSG-P4-003 |
| rwb-case reference-data fake | RWB-P3-E1043-CON, DP-07 | `LOV-DECISION` with `DOCATT` in force, the document type codes `INSPECTION_PHOTO`, `INSPECTION_CHECKLIST` and `UTILITY_BILL` with their field definitions, and an unknown code for X5 |
| rwb-case parameters fake | RWB-P3-E1042-CON, DP-06 | The ledger ingest target, the chain-check time and the capture parameters `CAPTURE_CLOCK_SKEW_MINUTES` 5, `CAPTURE_MAX_AGE_DAYS` 30 and `CAPTURE_MAX_FILES` 50 with the version in force, and an unavailable answer for X9 |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash` and the `entry_hash`, the SHA-256 of the canonical form, the append-only refusal, and the forced failure that raises `DecisionLogUnavailableException` for AC5 and TC-E2-024-17 |
| outbox and inbox library fake | RWB-PLT-TE006-CON | The `DecisionRecorded` fact of each scenario, its replay under the same event ID and idempotency key, and the outbox row of the append |
| gateway-bff route fake | RWB-PLT-N001-CON | The route the reader of a case reaches the two decision-log operations through, so the scope and the refusals can be asserted |

Each fake is replaced by the real service as RWB-P5-E2024-APP, RWB-P4-E2024-APP and RWB-P3-E2024-APP land, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the document list and the authorise decision consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the store's transaction and the intake workflow are `rwb-document`'s |
| File | None | No file input and no file output; a photo and a bill never leave `rwb-document` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/fieldcapture`, Java package `th.co.scb.ace.workbench.recovery.decision.fieldcapture`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which patterns have an instance in this slice: DP-01 is the boundary — the entry lives in `rwb_decision` and the capture facts arrive on the document contract and on `rwb.decision-record.v1`, never as a read of `rwb_document`; DP-03 is the append path of the central ledger with its chain, its append-only rule and its fail-closed exception; DP-06 is the ingest target and the chain-check time read as parameters; DP-07 is `LOV-DECISION` and the document type codes read as reference data; DP-09 is the outbox, the inbox and the idempotency key; DP-11 is the document read of the completeness checker and the authorise decision behind the reads, each with a mock and a 2 s timeout; DP-15 is the one migration of the slice; DP-19 is the composite route the reads are reached through, not built here.

The platform H dependencies in the table — H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON — and the C dependencies of the published contracts of other services — C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the authorise contract RWB-P4-E1037-CON that DP-11 consumes — are not all in the metadata rows of this story: `Depends on (build)` = None, and `Contract dependencies` names RWB-P5-E2024-CON, RWB-P4-E1037-CON, RWB-P3-E1043-CON and RWB-P3-E1042-CON, while the H platform contracts are not named there. They are the dependencies the DP table adds (DP-added) and they are recorded in GAP-1282 and ASM-2274; Ready to start stays Day 1, and the metadata rows are corrected at the next version of the story set. None of them blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and published contracts of `rwb-case` and `rwb-access`, built against their fakes.

The work of the legacy key that sits with other slices: the field-capture endpoint `POST /cases/{caseId}/field-captures`, the manifest parsing and file matching, the duplicate check on `client_file_id`, the type, size, time and position checks, the malware scan and the quarantine, the store, the capture columns `captured_at`, `capture_latitude`, `capture_longitude`, `client_file_id` and `capture_kind`, the migration `V2_5_024__field_capture.sql` and its partial unique index, the `DocumentStored` event, the OCR intake, the `UTILITY_BILL` extraction, the review queue and the SCR-30 panel are `rwb-document`'s (RWB-P5-E2024-APP, with the contract RWB-P5-E2024-CON). The scope and masking answer is `rwb-access`'s (RWB-P4-E2024-APP) and the case, its entry date and the task are `rwb-case`'s (RWB-P3-E2024-APP). This story builds the record of the decision and nothing beside it.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| FieldCaptureDecisionListener | Kafka consumer with the inbox | Reads `DecisionRecorded` for the field capture, deduplicates by event ID and idempotency key, and hands the decision facts to the recorder |
| FieldCaptureDecisionRecorder | Service | Composes the entry from the decision facts, reads the decision code list, the document type codes and the ledger parameters at the version in force, and decides nothing about the capture (BR3, BR8, BR11) |
| DecisionLogAppender | Service | Takes the next `chain_seq`, computes `prev_hash` and `entry_hash`, and writes the entry and its outbox row in one transaction (DP-03, BR13, BR5) |
| DecisionRecordFailClosedHandler | Service | Maps the library's `DecisionLogUnavailableException` to MSG-P7-003 for the item and to an incident for the platform administrator queue, so the store's transaction rolls back and nothing is stored (BR4) |
| FieldCaptureCompletenessChecker | Service | Compares the documents of a case from the document contract with the DOCATT entries of the case inside the ingest window and reports a document with no entry as a gap (BR12) |
| DecisionLogQueryController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the declared area and right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, with the append-only rule, the chain columns, the object reference and the idempotency key |
| DocumentFactClient | Adapter | The document list of RWB-P5-E2024-CON for the completeness check, one hop with a 2 s timeout and a breaker |
| AccessCheckClient | Client | The cached authorise decision behind the two reads (DP-11) |
| ReferenceAndParameterClient | Client | `LOV-DECISION`, the document type codes and the ledger parameters at the version in force (DP-06, DP-07) |
| InputsSnapshotResolver | Service | Resolves the `inputs_ref` of the entry and the freshness stamp of each input the decision read |

**Database and migrations**

- Writes `decision_log_entry`, the local decision record of the append and the library objects, all in schema `rwb_decision`; reads no other schema (DP-01).
- Migration in this story, in the per-service Flyway sequence of `rwb_decision`: `V2024_1__decision_field_capture_entry.sql` adds the field-capture columns of section 11 that the decision-log store baseline does not hold — the object reference, the client file ID, the document type code, the capture kind, the capture time and the message id of a refusal — plus the partial unique key `ux_declog_capture ON decision_log_entry (case_id, inputs_ref, decision_code) WHERE decision_code = 'DOCATT' AND inputs_ref IS NOT NULL`, so one entry per stored document and one per refused item is a constraint and not only a check (BR6), and the search index for the case-and-decision read of 12.1. The column names and types are Not specified in the source documents (GAP-1281; ASM-2271).
- The append-only rule is the table's, with the trigger `tr_declog_append_only` that refuses an UPDATE and a DELETE from the schema owner and the missing grant for the service login, as FSD P7 v3 AC-P7-001-01 fixes it.
- No row of `document`, `document_intake`, `document_field` or `parameter_value` is written here: the document hub's tables and the case's parameters are their owners'.

**Configuration and reference data**

- `LOV-DECISION` and the document type codes are reference data of `rwb-case` read through DP-07 at the version in force; the value `DOCATT` and the final call set are the reading of ASM-2275 and ASM-2276 and are held as reference rows, not as constants (GAP-1283; GAP-1284).
- The ledger ingest target of 5 minutes and the daily chain-check time of 02:00 are parameter rows of `rwb-case` read through DP-06 with the version in force; the parameter names are Not specified in the source documents (GAP-1281; ASM-2273), and the story holds no default.
- The capture parameters `CAPTURE_CLOCK_SKEW_MINUTES` 5, `CAPTURE_MAX_AGE_DAYS` 30, `CAPTURE_MAX_FILES` 50 and `INTAKE_MAX_FILE_MB` 25 are the store's rows; this story reads them only as facts of a refusal it records, and applies none of them (BR11).
- The outbox retry policy, the inbox retention and the chain-check alert route are the platform's (RWB-PLT-TE006-CON).

**Build steps**

1. `DecisionLogRepository` and the migration, with the partial unique key on the object reference and the append-only trigger; test that a second entry for the same document and an UPDATE are both refused (AC4, AC3).
2. `FieldCaptureDecisionListener` with the inbox, the dedupe by event ID and idempotency key, and the not-a-decision cases of X11; test the replay of the same fact (AC3).
3. `FieldCaptureDecisionRecorder` and `ReferenceAndParameterClient`: the entry composed from the decision facts and the versions in force, with the refusal of an unknown decision code and of a rule id with no version (X5; AC1).
4. `DecisionLogAppender` and the chain: `chain_seq`, `prev_hash`, `entry_hash` over the canonical form, the first `prev_hash` of 64 zeros, and the one-transaction append (AC1, AC4).
5. `DecisionRecordFailClosedHandler`: the `DecisionLogUnavailableException` path to MSG-P7-003 with the store's rollback and the incident; the test of the three items of AC5 with the library fake forced to fail (AC5, TC-E2-024-17).
6. `InputsSnapshotResolver` and the `inputs_ref` with the freshness of each input, including the capture time of the offline capture (AC7).
7. `DecisionLogQueryController` with the two operations, the declared area and right, the scope, the paging and the problem mapping; tests for AC1 and the refusals of TC-E2-024-16.
8. `FieldCaptureCompletenessChecker` over the document list of a case, with the gap report of X8 and the ledger ingest window of DP-06.
9. The contract-fake run of the whole slice: the document fake, the access fake, the reference-data and parameters fakes, the decision-record fake and the outbox fake, green from Day 1 (AC1 to AC7).
10. The boundary test: no write to `rwb_document`, `rwb_case` or `rwb_access` (the schemas of rwb-document, rwb-case and rwb-access, owned by those services and named here as boundaries only), and no position, file name or bill value in any entry, fact, outbox row or log line (AC6, BR9).

**Feature switch.** None of its own is named by a source, and the record path must have no off state: a capture that cannot be recorded must not be stored, so a switch that silenced the record would break BR4 and the principle that no action stands unlogged. The legacy flag `rwb.dochub.field-capture` stays `rwb-document`'s and is a legacy reference here; with it off no capture reaches the store and no DOCATT record arrives (GAP-1281; ASM-2271).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P5-E2024-CON stay green, and a SIT day shows one DOCATT entry per stored document and one per refused item of a field capture, each with its rule and version, its inputs reference, its object reference and its final call; a chain with no break and no entry changed or deleted; a refused record that refuses the item with MSG-P7-003 and stores nothing; both reads answering by case and by entry; and not one document, capture row, review item, task or case status changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The record of the item cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the fail-closed handler; the legacy message text is copied unchanged |
| MSG-P7-009 | An entry has a rule id with no version, or a decision code outside the list in force | Not specified in the source documents (GAP-1281; ASM-2271) | This story, on the append, naming `ruleVersion` or `decisionCode` |
| MSG-P4-002 | The role holds no right in the `DECISION_LOG` area | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of the read |
| MSG-P4-003 | The entry or the case is outside the caller's scope | This case is not in your scope. | This story, through the authorise answer of the read |
| MSG-GEN-001 | A query value is outside its list, or a required field of the entry is absent | Enter {field}. | This story, on the read and on the append |
| MSG-GEN-006 | The log, the reference list or the parameters are unavailable | Not specified in the source documents (GAP-1281; ASM-2271) | This story, on the read and on the retried fact |
| MSG-P5-001, MSG-P5-016, MSG-P5-017, MSG-GEN-002, MSG-GEN-003, MSG-P5-003, MSG-P5-015 | An item is refused for its type, its malware, its size, its time or its position, or a bill field needs checking | The legacy texts of section 14 of RWB-E2-024 | `rwb-document`, on the item; this story only records the message id on the entry of a refusal |

MSG-P7-003, MSG-P4-002 and MSG-P4-003 are copied unchanged from the FSD P7 v3 message set and the platform messages the authorise contract carries; MSG-P5-001, MSG-P5-003, MSG-P5-015, MSG-P5-016, MSG-P5-017, MSG-GEN-001, MSG-GEN-002 and MSG-GEN-003 are the legacy texts and are produced by `rwb-document`, not here. The text of MSG-P7-009 is named by the FSD P7 v3 exception flows but is not written out in any source this story may read, and no source writes the text of MSG-GEN-006, so both placeholders stand; the message id set of this story beyond these six has no source and is carried in GAP-1281. Thai text for each message follows decision DL10. Open decisions of this story, each still open and run on its assumptions: DL03 (ASM-0189, ASM-0193, ASM-0578, ASM-2567); DL10 (ASM-2250, ASM-2357, ASM-2377, ASM-2863); DL11 (ASM-0553, ASM-0703, ASM-1051, ASM-1104); DL26 (ASM-0247, ASM-0264, ASM-0275, ASM-0355).

### 15. Screens and states

No screen is built in this story. The empty, loading, error and no access states of SCR-11 are not written here and are Not specified in the source documents (DOR-RWB-P7-E2024-APP-10); the states of SCR-30 and SCR-31 are in the table below (CG-ALL-7287; CG-ALL-7288). Screen Specifications v1 gives no empty, loading, error or no access state for SCR-11, so those states are Not specified in the source documents for SCR-11 (CG-ALL-7286). The two reads are consumed by the decision-log view of a case and by the decision screen SCR-11 of this service, which are served through the gateway-bff composite route of DP-19 and are another story's; SCR-30 Case documents and SCR-31 Document review queue stay `rwb-document`'s and this story feeds neither of them. A panel id for showing the DOCATT entries beside the captures on SCR-30 is Not specified in the source documents (GAP-1281; ASM-2271).

| Where | State | What the reader sees |
|---|---|---|
| The decision-log read (P7) | List | The DOCATT entries of the case in chain order, with the document or the client file ID, the document type, the capture kind, the capture time, the rule and version, the final call and the message id of a refusal |
| The entry read | One entry | The same row with its inputs reference, its freshness stamps, its `decidedAt`, its `prevHash` and its `entryHash` |
| The entry read | An entry of a refused item | `finalCall` `REFUSED` or `QUARANTINED`, the message id and no document reference |
| The entry read | An entry with `correctsEntryId` | The correction beside the entry it corrects, and the corrected entry unchanged |
| The read | 403, or 404 | MSG-P4-002 for a role without the right, MSG-P4-003 for a case out of scope; no row is returned |
| SCR-30 Case documents | Loading | The loading state of SCR-30 as given in Screen Specifications v1, section SCR-30 (CG-ALL-7287) |
| SCR-30 Case documents | Empty, error, no access | Not specified in the source documents (CG-ALL-7287) |
| SCR-31 Document review queue | Loading | The loading state of SCR-31 as given in Screen Specifications v1, section SCR-31 (CG-ALL-7288) |
| SCR-31 Document review queue | Empty, error, no access | Not specified in the source documents (CG-ALL-7288) |

The screen field list, the composite route specification and the masking of each field belong to RWB-PLT-N001-CON and to the story that owns each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-024-16 | AC8, Access, BR15 | Component | The legacy access case: a role holding `Documents` R only calls the read path and is refused with MSG-P4-002 through the rwb-access fake, and a read of a case out of the caller's scope is refused with MSG-P4-003; no entry is returned and the rwb-document fake is never called |
| TC-E2-024-17 | Principle 5, BR4, AC5 | NFR | Decision log write forced to fail during a sync of three files; no document stored, the three items returned with MSG-P7-003, no entry and no chain position used, incident raised |
| TC-E2-024-01 | AC1, BR3 | Contract | Ten synthetic files with positions in Bangkok, eight `INSPECTION_PHOTO` and two `UTILITY_BILL` at `13.7563` and `100.5018`; ten DOCATT entries chained, one per document |
| TC-E2-024-02 | AC7, BR7 | Contract | Capture one day before sync, `2026-12-14 10:05` synced at `2026-12-15 08:30`; the entry carries the capture time as sent and the decided time of the sync |
| TC-E2-024-03 | AC1, BR9 | Contract | Synthetic utility bill image showing `1,284.50` and `28/12/2569` read as `1284.50` and `2026-12-28`; the entry names the document and the type and carries no bill value |
| TC-E2-024-04 | AC3, BR6 | Contract | The same ten client file IDs twice; ten `DUPLICATE` results and ten entries, with no second entry and no second chain position |
| TC-E2-024-05 | AC3, BR6 | Component | Six of ten items received, then all ten resent; six `DUPLICATE`, four `ACCEPTED`, ten entries |
| TC-E2-024-06 | AC1, BR9 | Component | A photo with no position; the entry records the item and the capture kind and carries no latitude and no longitude |
| TC-E2-024-07 | AC2, BR11 | Component | Capture times 6 and 5 minutes after receipt at `2026-12-15 14:20`; the `14:26` item refused with MSG-GEN-002 and recorded, the `14:25` item accepted and recorded |
| TC-E2-024-08 | AC2, BR11 | Component | A capture one day before the entry date `2026-10-02`, refused with MSG-GEN-003 naming "Capture time" and "Case entry date"; one entry for the refusal |
| TC-E2-024-09 | AC2, BR11 | Component | Captures 31 days and 30 days before the sync; the first refused with MSG-GEN-003 and the second accepted, each with its entry |
| TC-E2-024-10 | AC2, BR11 | Component | A HEIC file refused with MSG-P5-001 while the other items of the same sync are accepted; one entry for the refusal with no document reference |
| TC-E2-024-11 | AC2, BR9 | NFR | An EICAR test file quarantined with MSG-P5-016; one entry with `finalCall` `QUARANTINED` and no document, and no file or position in it |
| TC-E2-024-12 | AC2, BR15 | Component | Case `RW-2026-000502` with no task for `FC-01`; 404 with MSG-P4-003, no document and no DOCATT entry for the case |
| TC-E2-024-13 | AC1, BR9 | Contract | A bill amount read at confidence 0.5500 against the threshold 0.80; the entry names the document and the type, the review state stays the store's, and no bill value is carried |
| TC-E2-024-14 | AC2, BR11 | Component | Three manifest items and two files; 422 with MSG-GEN-001 and no entry, because no decision was taken by the store |
| TC-E2-024-15 | AC2, AC9, BR11 | Component | 51 files against the parameter 50; 413 with MSG-GEN-002 and no entry, because no decision was taken by the store |
| TC-E2-024-18 | AC4, BR5 | Component | An UPDATE and a DELETE against an existing `decision_log_entry` row of a field capture are each refused; the row is unchanged and no chain position is used |
| TC-E2-024-19 | AC6, BR9 | Contract | Document types `INSPECTION_PHOTO`, `INSPECTION_CHECKLIST` and `UTILITY_BILL` in force from reference data; an entry for a `UTILITY_BILL` names the type and carries no bill value |
| TC-E2-024-20 | DP-01, section 12.7 | Contract | A read of `document`, `recovery_case`, `task`, `timer`, `parameter_value` or `role` from the `rwb_decision` schema is refused; no foreign key crosses a schema |
| TC-E2-024-21 | AC4, BR5 | Component | An entry of AC1 for case `RW-2026-000501`; an UPDATE setting `final_call` and a DELETE attempted through the rwb-decision login (DP-02) and through the schema owner role; all four refused, the entry unchanged, its entryHash equal to the SHA-256 of its canonical form, and each refusal written to the ACE audit log |
| TC-E2-024-22 | AC5, BR4 | Component | Three items of case `RW-2026-000501` with the decision-record library fake forced to fail the record write; 503 with MSG-P7-003, no item accepted, no entry, no chain_seq, no document, capture row or intake item, and an incident raised |
| TC-E2-024-23 | AC6, BR9 | Contract | The ten entries of AC1 and their ten DecisionRecorded payloads; no latitude `13.7563`, no longitude `100.5018`, no file name and no bill value `1,284.50` appears in any of them or in the log lines |
| TC-E2-024-24 | AC10, AC11, BR1, BR2, BR5, BR8, BR10, BR12, BR13, BR14 | Component | The ten DOCATT records of AC1 with the decision-record library fake, one repeated fact of one of them, and one completeness run over a document with no entry; every assertion of AC11 holds |
| TC-E2-024-25 | AC12 | Contract | A call to each of the two read operations of section 12.1 with no session; 401 with the message Not specified in the source documents (NEWAC-RWB-P7-E2024-APP-AC11), and nothing is returned |

The legacy level System maps to Contract or Component as the row shows, Access to Component and Resilience to NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. Every case is asserted on the record side of this story: the entry, its object reference, its capture facts, its versions, its final call, its message id, its chain and its two reads; the capture, the scan, the store, the intake and the extraction are the document contract fake's. The `-ITG` copies of these cases belong to RWB-ITG-E2024-ITG and are not written here. The field-app test client, its sync and offline-replay profile, the EICAR fixture, the intake container test profile, the SIT harness environment and seeding, and the evidence report format and retention are Not specified in the source documents (GAP-0406); the pass and fail gate of the wave 2 run is Not specified in the source documents (GAP-0406). Each stored document and each item the store refuses has one DOCATT entry, its final call carrying the item result (ACCEPTED, REFUSED or QUARANTINED) and the message id of a refusal; a DUPLICATE item has no entry of its own and resolves to the entry of the item received first; a refusal that the decision log write itself prevents has no entry, as TC-E2-024-17 and TC-E2-024-22 assert (GAP-1284).

### 17. Guardrails

- No business value in code: the decision code, the final call set, the document types, the ledger parameters and the message ids are reference rows, parameter rows or facts of another service; nothing of them is a constant here.
- No personal data in the entry, the fact, the outbox, the tests or the logs: the case reference, the document reference, the client file ID, the document type, the capture kind, the capture time, the rule and version, the inputs reference, the actor reference, the final call and dates only. The position, the file name, the photo and the bill value stay in `rwb_document`, and a test scans the entry, the fact and the log line for any digit of `13.7563` and `100.5018` and for `1,284.50`.
- No read of another service's tables (DP-01): the capture facts arrive on the document contract and on `rwb.decision-record.v1`, the authorise answer on its contract, the reference lists and parameters in process; no `document`, `document_intake`, `document_field`, `recovery_case`, `task`, `role`, `permission`, `masking_rule` or `parameter_value` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- One recorder and no mover: this story changes no document, no capture row, no review item, no task and no case status, so a decision record can never move a case (BR10).
- No entry without its change and no change without its entry: the entry, its chain position and its outbox row commit in one transaction, and a store transaction that cannot record its decision rolls back and refuses the item (BR4, BR13, R-UNI-39).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, and the chain is verifiable from `chain_seq` 1 (BR5).
- One entry per stored document and one per refused item: the partial unique key on the object reference and the inbox dedupe make a second entry impossible (BR6, BR14).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own.
- One hop and 2 s on every call, with a breaker per downstream; a missing document fact, a missing reference list or a missing parameter never produces an entry from a guessed type, code or version (DP-11).
- The record path has no off switch, because a capture that cannot be recorded must not be stored.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-013 | Field photographs and bills reach the same intake and index as scanned documents | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-DCM-21 | 13 Manage documents and correspondence | R-DIL-22, R-UNI-39, R-UNI-40 | TC-E2-024-01 to TC-E2-024-25 |

| Legacy reference | Where it is kept |
|---|---|
| One record per stored document and one per refused item, with the decision code `DOCATT` | Sections 1, 2, 4, 7 (AC1, AC2), 8 (BR1, BR6), 13 |
| The rule id and version, the inputs reference and the versions in force on every record | Sections 1, 4, 7 (AC1), 8 (BR2, BR3, BR8) |
| The capture time as sent and the server time of the sync, `2026-12-14 10:05` against `2026-12-15 08:30` | Sections 1, 7 (AC7), 8 (BR7), 16 (TC-E2-024-02) |
| Case `RW-2026-000501`, entry date `2026-10-02`, collector `FC-01`, the ten items, `13.7563` and `100.5018` | Background, AC1 to AC3, AC7, sections 3, 12.8, 16 |
| The three document types `INSPECTION_PHOTO`, `INSPECTION_CHECKLIST` and `UTILITY_BILL`, and the bill of `1,284.50` and `28/12/2569` | Background, AC6, sections 3, 8, 11, 16 |
| A record that cannot be written refuses the item, MSG-P7-003 and TC-E2-024-17 | Sections 1, 4 step 8, 5 (X4), 7 (AC5), 8 (BR4), 14, 16 |
| Append only, the hash chain and the refusal of an UPDATE and a DELETE | Sections 7 (AC4), 8 (BR5), 9, 13 |
| Case `RW-2026-000502` outside the collector's scope, and the refusals that reached no store | Sections 5 (X11), 16 (TC-E2-024-12, TC-E2-024-14, TC-E2-024-15) |
| Messages MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-P4-003, MSG-GEN-001, MSG-GEN-006 and the item messages MSG-P5-001, MSG-P5-003, MSG-P5-015, MSG-P5-016, MSG-P5-017, MSG-GEN-002, MSG-GEN-003 | Section 14, exception paths |
| Rule IDs R-DIL-22, R-UNI-39 and R-UNI-40, and controls CTL-11 and CTL-38 | Sections 1, 2, 4, 5, 8 |
| Legacy key RWB-E2-024, story RWB-P7-E2024-APP, contract RWB-P5-E2024-CON | Metadata, sections 3, 12 |
| Test cases TC-E2-024-01 to TC-E2-024-25, with the access and principle 5 cases first | Section 16 |
| Decoupling patterns DP01, DP03, DP06, DP07, DP09, DP11, DP15, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P5-E2024-APP the field-capture endpoint, the checks, the scan, the store, the capture columns, the intake, the extraction, the review queue and the SCR-30 panel, with the contract in RWB-P5-E2024-CON; RWB-P4-E2024-APP the authorise, scope and masking answers and the access entries; RWB-P3-E2024-APP the case, its entry date, the field inspection task and the parameter and reference rows; and RWB-ITG-E2024-ITG the cross-service harness and the `-ITG` copies of the test cases, which read the DOCATT entry of each stored document and of each refused item through `GET /api/recovery/decision/v1/decision-log`.

### 19. Out of scope

- The field-capture endpoint `POST /cases/{caseId}/field-captures`, the manifest and file matching, the duplicate check on `client_file_id`, the file type and size checks, the clock skew, the age limit, the malware scan and the quarantine, the store, the capture columns `captured_at`, `capture_latitude`, `capture_longitude`, `client_file_id` and `capture_kind`, the migration `V2_5_024__field_capture.sql` and the index `ux_document_client_file`, the `DocumentStored` event, the OCR intake, the `UTILITY_BILL` extraction, the review queue and the SCR-30 panel: RWB-P5-E2024-APP, with the contract and fakes in RWB-P5-E2024-CON.
- The local decision record and its outbox row that `rwb-document` writes in its own schema: RWB-P5-E2024-APP. This story consumes the fact, not the store's table.
- The authorise, scope and masking answers, the `AC-READ` and `AC-DENY` entries and the policy pack of `PM-2026.12` and `MASK-SIT-01`: RWB-P4-E2024-APP, with the guard and authorise contract RWB-P4-E1037-CON.
- The case, its entry date, the field inspection task and its state, the document types as reference rows and the parameters `CAPTURE_CLOCK_SKEW_MINUTES`, `CAPTURE_MAX_AGE_DAYS`, `CAPTURE_MAX_FILES` and `INTAKE_MAX_FILE_MB`: RWB-P3-E2024-APP under DP-06 and DP-07, and `rwb-document` for the type table itself.
- The field app itself and its offline store, and the agency field teams that reach the Workbench only through the external gateway (DL03; FEAT-PRM-15, Epic 7).
- The inspection task, the checklist rule and the asset unlock rule (`WITH_FIELD_INSPECTION`, R-DIL-22, FEAT-TRT-15, Epic 3), and the repossessed vehicle photo standard (CTL-38, Epic 7).
- The approval path, the `ApprovalWorkflow`, the approval queue SCR-10, the decision screen SCR-11 and the approval records, which are the other P7 stories of this service; the rule registry, the rule package versions, the rule rows and the rule test cases of the same service; and the agent version an entry may name, which is `rwb-agent`'s.
- The daily hash-chain check JOB-14 at 02:00 and its compliance report, and the rule promote JOB-20 at 00:01: the decision-log and rule-governance baselines of this service. This story appends entries that the check covers like any other.
- The data-lake copy of the decision log with JOB-13 and INT-19/INT-20: retired with the data lake (DP-17); the ingest of the ledger is continuous Kafka.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E2024-ITG.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
