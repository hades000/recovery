# RWB-P7-E2017-APP Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | L-P7-AA |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P7-E2017-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2017-CON; contract story for the P7 record path not yet created (DOR-RWB-P7-E2017-APP-21) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DCM-012, REQ-OCC-002, REQ-OCC-009) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-008 |

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.
- Backfill the published Test Cases v9 cross-references.
- RD-P1-008: the event type of DecisionRecorded reads `rwb.decision.DecisionRecorded.v1` (ledger acceptance criterion); the topic `rwb.decision-record.v1` is unchanged.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-017 for rwb-decision; the correction and the send decision records of the document set in the central ledger, and the two decision-log reads that serve them. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 25 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3 aligns the story with RD-P1-008. Tool: Claude Code / Claude Sonnet 5.5.

### 1. Story

As a **restructuring officer (FCR), a case owner and an internal audit reader**, I want **the two decision records the document screens cause — the correction of an overridable value, with decision code D6.4 and the reason as override_reason, and the send for signature, with final call SENT_FOR_SIGNATURE — appended once to the central decision ledger of `rwb-decision`, chained, append only and readable by case and by entry**, so that **a corrected value and a sent set can be traced to the decision that allowed them, an action whose record cannot be written does not proceed, and the record that explains a customer document can never be quietly changed**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-017:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record path of DP-03.
- One deliverable and nothing else: two entries. (1) The correction entry: decision code D6.4 with `override_reason` carrying the reason the officer gave, the corrected field, the old value and the new value as identifiers, the document reference, the template code and version, the case and the requesting role. (2) The send entry: final call SENT_FOR_SIGNATURE with the document set reference, the template versions of the set, the write-once reference, the case and the requesting role.
- Each appended once, in the transaction of the action it records, through the decision-record path of DP-03 on `rwb.decision-record.v1`, hash chained and append only, and served by the two decision-log reads of this service (API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1).
- What stays with `rwb-document` (P5, RWB-P5-E2017-APP and RWB-P5-E2017-CON): the generation screens SCR-14 and SCR-30, the draft store, the regeneration as the next `doc_version`, the locked-value checks, the write-once copy, the signature request and the document states DRAFT, REVIEWED and SENT. None of it is rebuilt here. The screen states of SCR-14, SCR-30 and SCR-38 are placeholders in section 15 until their owner settles them; the owner of SCR-38 is Not specified in the source documents (DOR-RWB-P7-E2017-APP-10).
- What stays elsewhere: the template catalog, the template versions and their Legal approval with `rwb-comms` (P6, RWB-P6-E1046-APP and RWB-P6-E1034-APP); the treatment and its D6.4 approval with `rwb-treatment` (S2, RWB-S2-E2026-APP); the session, the role, the scope and the Documents right U with `rwb-access` (P4, RWB-P4-E2017-APP); the e-signature flow with `rwb-comms` (P6, the successor of RWB-E2-018); and the D6.4 GENERATED record at generation time, which is RWB-P7-E2026-APP and is not touched here.
- The record and the action are one pair under DP-03: the producing service writes the record through the record path inside the action's transaction, and this service appends it to the ledger in one atomic transaction of its own, so an action with no record is refused with MSG-P7-003 and a record with no action is never appended (ASM-2256). The service records and exposes the two decisions; it corrects no value, sends no document, starts no signature request and writes no document, treatment, template or case (BR9).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1278; ASM-2261); this story uses the phrase "the rwb-decision login (DP-02)" and never the shared monolith login.

The legacy behaviour carried into the decision service is unchanged in meaning: a correction of an overridable value is recorded with its reason, its field, its old and new value and its document; a send is recorded with the final call SENT_FOR_SIGNATURE; each leaves one entry and not a second; and an action whose entry cannot be written does not proceed (legacy RWB-E2-017 AC2, AC3, AC9 and BR4, BR9).

### 2. Business rationale

The officer today copies case facts into three Word files, prints them and walks them to signature, and a late change is made by hand on the printed copy with no record. The generation engine of `rwb-document` now fills each Legal-approved template version from the case facts and refuses a missing value or an unapproved version, and the screens let the officer correct an overridable value with a reason and send the reviewed set as write-once documents. Those two actions are only defensible if the decision behind them is recorded: which value changed, from what to what, with what reason, in which document and from which template version; and which set was sent, on which template versions, with which write-once reference and under which requesting role. The monolith wrote the entry with the document row in one process and one schema, so the two could not drift apart. In the target the document work is `rwb-document`'s and the evidence of every decision is collected in `rwb-decision` (Architecture v5 slides 14, 28 and 41), so the record has to be chained and unchangeable there, and readable by the officer who asked and by the auditor who later asks why.

Under Architecture v5 the central decision ledger is `rwb-decision` (slides 14, 28 and 41); each service writes its decision record through the local library in the same transaction as the change it records and publishes `DecisionRecorded` on `rwb.decision-record.v1` (slides 20 and 42, event 08); `rwb-decision` collects the records into the ledger and seals it daily in write-once storage (slide 28); and the ledger is read through the decision-log operations (slide 14). The realignment changes the mechanism, not the business rule:

1. The synchronous `DecisionLogWriter` call of the monolith becomes the decision-record path of DP-03: the record is written where the correction or the send commits and is appended here on `rwb.decision-record.v1`, with the append-only rule and the hash chain the FSD already carries (FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-04, FEAT-DRI-05).
2. The record is not a copy of the document and not a copy of the values: it names the case, the treatment, the template code and version, the value pair as identifiers, the document reference, the set reference and the write-once reference. The transfer price, the title deed number, the borrower name, the Thai long date and the file stay in `rwb_document` (BR7).
3. The decision code D6.4 and the final call SENT_FOR_SIGNATURE are data: the code is a value of LOV-DECISION read through the reference-data contract of `rwb-case` (DP-07), and the final calls are rows of this service's own vocabulary, never literals (BR13).
4. The template catalog and the Legal approval stay with `rwb-comms`, the treatment with `rwb-treatment`, the correction and the send with `rwb-document` and the authorise answer with `rwb-access`; this story reads none of their tables (DP-01, DP-11) and rebuilds none of their rules.
5. The one decision-log read of the monolith becomes two operations on the service's own base (DP-13): search the ledger by case, decision code, rule, approver and date, and read one entry with its inputs reference and its chain fields. The record is append only and hash chained, so a refused correction or send leaves no entry, a repeated record leaves one entry, and a break in the chain is a reportable event rather than a silent edit.

This story meets REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009 on the record side: it proves which value was corrected and with what reason, which approved template version produced each document of the set and that the set's send is recorded before anything reaches the customer, and it carries the principle that no action proceeds unlogged (CTL-06, R-UNI-39) with the correction control CTL-07. It puts the decision half of the screens in place and leaves the render, the store, the write-once copy, the signature path, the template approval, the treatment and the access answer where their owners have them.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P5-E2017-CON | The published contract of the review, correction and send actions of `rwb-document` (P5): the correction for case `RW-2026-000401`, document `DOC-0411` and the value pair `contract_date` "2026-12-10" to "2026-12-12" with the reason, the send of treatment `TRT-0401` under Idempotency-Key `S-0401`, the declaration of the two records on `rwb.decision-record.v1` with decision code D6.4 and final call SENT_FOR_SIGNATURE, and the contract fakes. Which fields of the two records this service consumes is Not specified in the source documents (GAP-1278; ASM-2257), and the field set this story assumes is that of ASM-2257 |
| RWB-PLT-E1027-CON | The decision-record path and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule and the idempotency key the record carries |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06): the page-size bound of the search and the completeness target of the ingest; the parameter names are Not specified in the source documents (GAP-1278; ASM-2258) |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION, which holds D6.4, and the final-call list, with the version in force on the business date (GAP-1278; ASM-2257) |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one entry under a repeated record, the inbox dedupe and the outbox row of the append |
| RWB-PLT-E1044-CON, RWB-PLT-N001-CON | The per-service Flyway sequence of `rwb_decision` (DP-15), in which this story adds one index step and no table; and the gateway-bff composite route (DP-19) through which SCR-38 Decision log query and the auditor's view reach the two operations |
| The `rwb-decision` decision-log store baseline | `decision_log_entry` with the columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE, the unique key on the idempotency key and the chain check JOB-14 at 02:00. The baseline is the service's own earlier work and is in no H row of this story: the dependency is carried in GAP-1278 and ASM-2261 |
| The authorise answer of `rwb-access` (P4) | `POST /api/recovery/access/v1/authorise` (Architecture v5 slide 14) for the Decision log right R and the caller's scope behind the two reads; consumed, faked and in no C row of this story (GAP-1278; ASM-2261) |

Business preconditions carried from RWB-E2-017:

- Case `RW-2026-000401` with product group `MORTGAGE` in team `FCR-BKK`; treatment `TRT-0401` of type `DEED_IN_LIEU` approved at D6.4 with no outcome; treatment `TRT-0402` of the same type with no `decision_log_id`, which reaches no record at all.
- The set for `DEED_IN_LIEU` is `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, all approved by Legal; the contract draft is `DOC-0411` at `doc_version` 1 with `contract_date` "2026-12-10", and the three drafts are REVIEWED before the send.
- The merge field catalog marks amounts, parties, title numbers and the treatment terms locked and the dates of signing and the witness details overridable; `transfer_price` is locked, and its attempted move from 1250000.00 to 1200000.00 is refused by `rwb-document`. This story reads none of it.
- The caller holds RW-RESTRUCT with Documents CRU on the case in scope; RW-CASEOWN holds the same; RW-TEAMMGR holds Documents R; RW-LEGAL holds Documents CRUA; and every role of TSD P7 v2 T6.1 holds R on the decision log.
- The two records under test are produced by the contract fake of RWB-P5-E2017-CON: the correction of `DOC-0411` and the send of `TRT-0401` under Idempotency-Key `S-0401`; Day 1, with no build dependency.

### 4. Flow

1. A restructuring officer corrects an overridable value on `DOC-0411` and enters the reason "Signing appointment moved by the customer"; `rwb-document` checks the field against the merge field catalog, checks the state and the version, writes the correction in one transaction and, through the decision-record path of DP-03, the D6.4 correction record: the reason as `override_reason`, the corrected field `contract_date`, the old value and the new value as identifiers, the document reference `DOC-0411`, template `DIL-CONTRACT` version 2, case `RW-2026-000401` and requesting role `RW-RESTRUCT` (RWB-P5-E2017-APP; Architecture v5 slide 28, step 1).
2. The record path publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID, with the record's entry ID and its idempotency key (DP-09; slide 42, event 08).
3. `rwb-decision` `DocumentRecordListener` reads the fact into the inbox of DP-09, deduplicates by event ID and by the record's idempotency key (R-UNI-40), keeps the D6.4 correction facts and the SENT_FOR_SIGNATURE send facts, and passes them to `DecisionLogAppendService`. Every other decision code is the decision-log baseline's general ingest and not this story's.
4. `DecisionLogAppendService` reads LOV-DECISION and the final-call list through the reference-data contract of DP-07 at the version in force, requires the decision code, the final call and, for a correction, the reason, the document reference and the template code with its version; a record that fails the check is refused with MSG-P7-003 naming the missing field and nothing is written (BR11).
5. `DecisionLogAppendService`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash` (64 zeros for the first), computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row, and writes the inbox row of the fact and the idempotency row of the key. A failed append changes nothing: no entry, no chain position and no inbox row (BR5, BR12).
6. The officer marks the drafts reviewed and chooses Send for signature; `rwb-document` checks that every document of the set is REVIEWED and on the current template version, copies each final file to the write-once container by its content hash through ContentHashGuard, starts one signature request in `rwb-comms` and, in the same transaction, writes the SENT_FOR_SIGNATURE send record: the document set reference, the template versions of the set, the write-once reference, case `RW-2026-000401` and requesting role `RW-RESTRUCT` (legacy step 9; BR2).
7. The send record is appended here exactly as the correction record is: one entry for the set and not three, chained after the correction entry, with the idempotency key `S-0401` on the record (BR3). A restructuring officer, a case owner or an internal audit reader reads the ledger with `GET /api/recovery/decision/v1/decision-log` by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and reads one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`; each row holds the entry ID, the `chainSeq`, the case, the decision code, the final call, the inputs reference, the corrected field and value-pair identifiers or the set and write-once references, the template versions, the requesting role, `decidedAt`, `prevHash` and `entryHash` (BR10).
8. A caller whose authorise answer carries no Decision log right is refused with 403 and MSG-P4-002; a case outside the caller's scope is refused with 404 and MSG-P4-003, and no entry of that case is returned. Nothing in this story moves a document, a treatment, a case or a template: the entry is written beside the action and the owners of those records keep their own state (BR9).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The correction record names no reason, or no document reference, or a template code with no version; or the decision code is not a value of LOV-DECISION at the version in force, or the final call is not a row of the list | The append is refused, nothing is written, no chain position is used and the fact stays on the topic for redelivery | MSG-P7-003 | AC1, AC3, AC9 |
| X2 | The decision log store is unavailable, or the chain position cannot be taken, on a correction | The correction is not recorded: `rwb-document` answers 503, its `doc_version` is unchanged and no file is added; an incident is raised as in R-UNI-39 | MSG-P7-003 | AC4 |
| X3 | The decision log store is unavailable, or the chain position cannot be taken, on a send | The send does not proceed: no file is copied to the write-once container, the documents stay REVIEWED, no signature request starts and an incident is raised as in R-UNI-39 | MSG-P7-003 | AC5 |
| X4 | The same record is delivered again, or replayed from the topic | One entry exists; the inbox dedupe and the idempotency key both hold, and the repeat is counted for R-UNI-40 | None | AC7 |
| X5 | A correction is refused by its own checks: a locked field, an empty reason, a document already SENT, or a stale version | The record path is never called, so no correction entry is appended for the refused request and no chain position is used | MSG-P5-014, MSG-GEN-001, MSG-P5-002, MSG-GEN-004 (produced by the owners of the checks) | AC9 |
| X6 | A send is refused by its own checks: a document not REVIEWED, a template version no longer current, a treatment not approved or not open | The record path is never called, so no SENT_FOR_SIGNATURE entry is appended; no file is copied and no signature request starts | MSG-P5-013, MSG-P5-011 (produced by `rwb-document`) | AC8 |
| X7 | The signature request is refused after the send was prepared | The send does not commit: the documents stay REVIEWED, no signature request exists and no SENT_FOR_SIGNATURE entry is appended for the refused send; the retry after the service returns completes once (ASM-2256) | MSG-GEN-006 | AC11 |
| X8 | A correction of an entry is needed, or an UPDATE or a DELETE is attempted through the service role or the schema owner | A correction appends a new entry with `corrects_entry_id` naming the entry it corrects, and the corrected entry is unchanged; an UPDATE or a DELETE is refused by the missing grant and by `tr_declog_append_only` and the attempt is audited | None | AC6 |
| X9 | The caller holds no Decision log right, or asks for a case outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; no entry is returned | MSG-P4-002, MSG-P4-003 | AC10 |

An entry is only ever appended beside the action that caused it: the entry, its chain position, its inbox row and its idempotency row are written in one transaction, so a correction or a send can never leave a half record and a record can never exist for an action that was refused (BR12).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the document contract RWB-P5-E2017-CON, the decision-record path of DP-03, the reference-data and parameters libraries and the fakes; no screen, correction, regeneration, write-once copy, signature request or document state is rebuilt here |
| Negotiable | The decision code, the final-call set, the record payload field set, the parameter names and the message ids are data, parameters or contracts of their owners; the story fixes only the two records, the append-only rule, the chain and the two reads |
| Valuable | Every corrected value and every sent set can be traced to the decision that allowed it, with its template versions and its references, and that explanation cannot be quietly changed |
| Estimable | The scope is fixed to two records, two reads and one fake set; the size is Not specified in the source documents (DOR-RWB-P7-E2017-APP-16) |
| Small | One listener, one appender with the chain, one query controller with two operations, one index step and one fake set; fits one sprint with its tests and is the decision-record slice of the legacy key |
| Testable | Each of the eleven criteria in section 7 and AC12 runs as one automated test against the contract fakes, with a fixed business date and a fixed chain |

### 7. Acceptance criteria

No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E2-017, and every legacy criterion of the key corrects a value, renders a draft, sends a set, checks a lock or answers an access question, which belongs to RWB-P5-E2017-APP, RWB-P5-E2017-CON or RWB-P4-E2017-APP. The eleven criteria below are new for the `rwb-decision` slice and test only the two records and their two reads; each keeps the legacy values of RWB-E2-017 — case `RW-2026-000401` in team `FCR-BKK`, treatment `TRT-0401` of type `DEED_IN_LIEU`, treatment `TRT-0402` with no `decision_log_id`, the set `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1, document `DOC-0411`, `contract_date` "2026-12-10" to "2026-12-12", the reason "Signing appointment moved by the customer", `transfer_price` 1250000.00 and 1200000.00, "12 December 2569 BE", Idempotency-Key "S-0401", role `RW-RESTRUCT`, decision code D6.4, final call SENT_FOR_SIGNATURE and the messages MSG-P7-003, MSG-P5-002, MSG-P5-013, MSG-P5-014, MSG-P5-011, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P4-002 and MSG-P4-003 — and adds no business value.

```gherkin
Feature: The correction and send decision records of rwb-decision

  Background:
    Given case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4 with no outcome
    Given the set for "DEED_IN_LIEU" is "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given a restructuring officer with role RW-RESTRUCT in scope of the case
    Given the rwb-document contract mock returns the correction of "DOC-0411" from contract_date "2026-12-10" to "2026-12-12" with reason "Signing appointment moved by the customer" as doc_version 2
    Given the rwb-document contract mock returns the send of the three reviewed documents of "TRT-0401" under Idempotency-Key "S-0401"
    Given the rwb-access contract mock returns the authorise answer allowing role RW-RESTRUCT the Decision log right R on case "RW-2026-000401"
    Given the rwb-treatment fake returns treatment "TRT-0401" of type "DEED_IN_LIEU" with decision_log_id set and no outcome
    Given the decision-record library fake returns the D6.4 correction record and the SENT_FOR_SIGNATURE send record on rwb.decision-record.v1

  Scenario: AC1 One D6.4 correction entry with the reason, the field and the document (new, D-RCV-60)
    Given the contract draft "DOC-0411" at doc_version 1 has contract_date "2026-12-10"
    Given the rwb-document contract mock returns the D6.4 correction record of "DOC-0411" with the corrected field "contract_date", the old value identifier and the new value identifier, the reason, template "DIL-CONTRACT" version 2 and requesting role "RW-RESTRUCT"
    When the ledger consumes rwb.decision.DecisionRecorded.v1 for that record
    Then one decision_log_entry exists with decision code "D6.4", case reference "RW-2026-000401", override_reason "Signing appointment moved by the customer", the corrected field "contract_date" and the document reference "DOC-0411"
    Then the entry carries template code "DIL-CONTRACT", template version 2 and requesting role "RW-RESTRUCT"
    Then GET /api/recovery/decision/v1/decision-log/{entryId} returns that entry with the same override_reason and the same document reference

  Scenario: AC2 The correction entry carries the value pair as identifiers and no merge value (new, D-RCV-60)
    Given the rwb-document contract mock returns the correction record of "DOC-0411" with the merge snapshot reference behind the value pair
    When the ledger appends the record
    Then the entry carries the old value identifier, the new value identifier and the merge snapshot reference
    Then neither "2026-12-10", nor "2026-12-12", nor "12 December 2569 BE", nor a formatted amount appears in the entry, its event payload or its audit line
    Then the corrected value, the PDF and the merge snapshot itself stay in rwb_document

  Scenario: AC3 One SENT_FOR_SIGNATURE entry for the sent set (new, D-RCV-60)
    Given the three drafts of "TRT-0401" are in state "REVIEWED"
    Given the rwb-document contract mock returns the send record of "TRT-0401" with the document set reference, the write-once reference, template "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, and requesting role "RW-RESTRUCT"
    When the ledger consumes the SENT_FOR_SIGNATURE record
    Then exactly one decision_log_entry is appended for that send and not three
    Then the entry carries final call "SENT_FOR_SIGNATURE", the document set reference, the three template versions, the write-once reference, case "RW-2026-000401" and requesting role "RW-RESTRUCT"
    Then the entry carries no file byte, no signature image and no merge value

  Scenario: AC4 The correction whose record cannot be written does not proceed (new, D-RCV-60)
    Given the decision-record library fake returns a refused append
    Given the rwb-document contract mock holds the correction of "DOC-0411" open in one transaction with the decision-record path of rwb-decision
    When the decision-record path refuses the append
    Then the record path answers the correction with status 503 and MSG-P7-003
    Then no entry exists for "DOC-0411" and no chain_seq is consumed
    Then "DOC-0411" stays at its doc_version and no file is added, and an incident is raised as in R-UNI-39
    When the same correction is retried and the store accepts the append
    Then one entry is appended and it takes the chain_seq the refused write did not use

  Scenario: AC5 The send whose record cannot be written does not proceed (new, D-RCV-60)
    Given the decision log store does not accept writes
    Given the rwb-document contract mock holds the send of "TRT-0401" open in one transaction with the decision-record path
    When the record path refuses the append
    Then the send answers 503 with MSG-P7-003 and no file is copied to the write-once container
    Then the three documents stay in state "REVIEWED" and no signature request starts
    Then no entry with final call "SENT_FOR_SIGNATURE" exists for "TRT-0401", no chain_seq is consumed, and an incident is raised as in R-UNI-39

  Scenario: AC6 The ledger is append only and hash chained (new, D-RCV-60)
    Given an entry for case "RW-2026-000401" with chain_seq 1 and final call "SENT_FOR_SIGNATURE" is stored
    Given its prev_hash equals the entry_hash of the entry before it, and the first prev_hash of the ledger is 64 zeros
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the rwb-decision login and again through the schema owner role
    Then all four statements are refused: by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged and the refused attempts are written to the ACE audit log with the table, the operation and the entry ID
    When a correction of the entry is needed
    Then a new entry is appended with corrects_entry_id naming it, and the corrected entry is still unchanged

  Scenario: AC7 A repeated send record gives one entry (new, D-RCV-60)
    Given the send of "TRT-0401" with Idempotency-Key "S-0401" was recorded and the ledger returned its entry ID
    When the same record with Idempotency-Key "S-0401" arrives again
    Then one entry exists for the send, the first entry ID is returned and the repeat count of R-UNI-40 is raised by one
    Then no second entry and no second chain position are written

  Scenario: AC8 A send refused by its own checks leaves no SENT_FOR_SIGNATURE entry (new, D-RCV-60)
    Given two drafts of "TRT-0401" are "REVIEWED" and "DIL-MORTGAGE" is still "DRAFT"
    Given treatment "TRT-0402" of type "DEED_IN_LIEU" has no decision_log_id
    Given "DIL-CONTRACT" version 3 became current after the drafts were made
    When the send of "TRT-0401" is refused with MSG-P5-013 naming the mortgage document and naming the contract and "template version 3", and the send of "TRT-0402" is refused with MSG-P5-011
    Then the record path is never called and no SENT_FOR_SIGNATURE entry names "TRT-0401" or "TRT-0402" for those requests
    Then no file is copied to the write-once container and no signature request starts
    Then the last entry of the ledger keeps its entry_hash

  Scenario: AC9 A correction refused by its own checks leaves no D6.4 entry (new, D-RCV-60)
    Given transfer_price is locked in the merge field catalog
    Given "DOC-0411" is in state "SENT"
    Given two officers opened "DOC-0411" at version 4 and the first saved a correction, so the record is at version 5
    When the correction of transfer_price from 1250000.00 to 1200000.00 is refused with MSG-P5-014 naming "Transfer price"
    When a correction of contract_date with an empty reason is refused with MSG-GEN-001 naming "Reason"
    When a correction of "DOC-0411" in state "SENT" is refused with MSG-P5-002
    When the second officer saves a correction with version 4 and is refused with MSG-GEN-004
    Then the record path is never called and no D6.4 correction entry exists for any of those requests
    Then "DOC-0411" keeps its doc_version and the last entry_hash of the ledger is unchanged

  Scenario: AC10 The two reads return the entries with the chain fields and are scoped (new, D-RCV-60)
    Given the correction entry of AC1 and the send entry of AC3 are stored for case "RW-2026-000401"
    When an authorised reader sends GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000401&decision=D6.4 with the page-size bound in force
    Then the page holds the correction entry in decidedAt order with its chainSeq, prevHash and entryHash, and the total count of the case
    When the same reader sends GET /api/recovery/decision/v1/decision-log/{entryId} for the send entry
    Then the response is 200 with final call "SENT_FOR_SIGNATURE", the document set reference, the write-once reference, the template versions and the requesting role
    Given the rwb-access contract mock returns MSG-P4-002 for a caller without the Decision log right and MSG-P4-003 for a case outside the caller's scope
    When those callers send the two reads
    Then the responses are 403 with MSG-P4-002 and 404 with MSG-P4-003, and no entry is returned

  Scenario: AC11 The signature service refuses the send (new, D-RCV-60)
    Given the rwb-document contract mock returns "UNAVAILABLE" from the signature request of "TRT-0401"
    When the send of "TRT-0401" is taken
    Then the send answers 503 with MSG-GEN-006 naming "e-signature" and the three documents stay in state "REVIEWED"
    Then the record path commits no SENT_FOR_SIGNATURE entry for the refused send
    When a second send after the service returns completes
    Then one SENT_FOR_SIGNATURE entry exists for "TRT-0401" and one signature request exists

  Scenario: AC12 The record path changes no other owner's record and takes its codes from reference data (new, D-RCV-60)
    Given the correction entry of AC1 and the send entry of AC3 are stored for case "RW-2026-000401"
    Then "DOC-0411", treatment "TRT-0401", the template set and case "RW-2026-000401" keep their state and no row of them is written
    Then the decision code and the final call of both entries are the values the reference-data contract returns, and a change to that list needs no release
```

The eleven criteria are new, and `acs` is empty for this story: no legacy criterion of RWB-E2-017 is owned verbatim here, because each of them corrects a value, sends a set, checks a lock, checks a template version or answers an access question, and each of those belongs to its own slice. The final call of the correction entry, the record payload field set, the shape of the document set reference and of the write-once reference and the message id set of this slice have no source and are carried in GAP-1278 with ASM-2256 to ASM-2259. The `-ITG` copies of the test cases belong to RWB-ITG-E2017-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The correction leaves one entry with decision code D6.4, the reason in `override_reason`, the corrected field, the old and new value as identifiers, the document reference, the template code and version, the case and the requesting role | Legacy RWB-E2-017 AC2, BR3, BR4; TSD P7 v2 T3.1; FSD P7 v3 A2.4; CTL-07 |
| BR2 | The send leaves one entry with final call SENT_FOR_SIGNATURE, the document set reference, the template versions of the set, the write-once reference, the case and the requesting role, for the set and not for each document | Legacy RWB-E2-017 AC3, BR6, BR7; FSD P7 v3 A2.2 |
| BR3 | Each record is appended once: the inbox dedupe by event ID and the idempotency key, `S-0401` for the send, make a second entry impossible and count the repeat | Legacy RWB-E2-017 AC10, BR10; FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40 |
| BR4 | The log is append only: an entry is never changed and never deleted, and a correction of an entry is a new entry naming the one it corrects in `corrects_entry_id` | FSD P7 v3 AC-P7-001-01 and A2.1; Architecture v5 slide 28 |
| BR5 | Every entry is hash chained: a `chain_seq`, a `prev_hash` equal to the previous entry's `entry_hash` (64 zeros for the first) and an `entry_hash` equal to the SHA-256 of the entry's canonical form; JOB-14 at 02:00 covers it, and the ingest of `rwb.decision-record.v1` is continuous Kafka so the entries reach the ledger inside the completeness target of Architecture v5 slide 28 | FSD P7 v3 AC-ALT-P7-001-01; Architecture v5 slides 28 and 44; TSD P7 v2 T5.3 |
| BR6 | A correction or a send whose record cannot be written does not proceed: MSG-P7-003, nothing changes and an incident is raised under R-UNI-39 | Legacy RWB-E2-017 AC9, BR9; FSD P7 v3 AC-EXC-P7-002-02 and A2.5; CTL-06 |
| BR7 | The two records carry identifiers and references only: no merge value, no formatted value, no Thai long date, no file byte and no signature | Legacy RWB-E2-017 section 17; DL26; Template and Rules §R7.2 s17 |
| BR8 | The old and the new value of a correction are carried as identifiers of the value pair, so the entry proves the change without holding the value; the values stay in `rwb_document` | Legacy RWB-E2-017 AC2 and section 12; GAP-1278 with ASM-2257 |
| BR9 | The story records and exposes; it corrects no value, regenerates no draft, copies no file, starts no signature request and changes no document, treatment, template or case | Architecture v5 slides 14 and 41; DP-01 |
| BR10 | The two reads declare the Decision log right R with the scope applied; a role without it is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003 | TSD P7 v2 T-A.1, T6.1 and T6.2 |
| BR11 | A record that lacks its decision code, its final call or, for a correction, its reason, its document reference or a template version is refused with MSG-P7-003 and appends nothing; no entry is written from an assumed value | FSD P7 v3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05 read on this slice |
| BR12 | The entry, its chain position, its inbox row and its idempotency row commit in one transaction; a failed append leaves nothing and the fact is redelivered | Principle 5; FSD P7 v3 A2.5; DP-03 |
| BR13 | The decision code is a value of LOV-DECISION and the final calls are data rows, never literals; a change to either is a reference-data change and not a release | BR-P7-002; TSD P7 v2 T3.2; GAP-1278 with ASM-2257 |

### 9. State transitions

None for a document, a template, a treatment or a case: the document states DRAFT, REVIEWED and SENT are `rwb_document`'s (legacy section 9, RWB-P5-E2017-APP). The states below are the states of the two entries of this story, and an entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A D6.4 correction record arrives | The code is in LOV-DECISION, the reason, the document reference and the template version are present, and the chain head is known | Appended at the next `chain_seq`, with its `prev_hash`, its `entry_hash`, its inbox row and its idempotency row in one transaction |
| Absent | A SENT_FOR_SIGNATURE record arrives | The final call is in the list, the set reference, the template versions and the write-once reference are present, and the chain head is known | Appended at the next `chain_seq`, in one transaction with its inbox and idempotency rows |
| Absent | Either record arrives, and the store or the chain is unavailable | The append cannot commit | Absent: MSG-P7-003, nothing written, the action rolled back and an incident raised |
| Appended | The same record arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A correction is taken on an entry, or an UPDATE or a DELETE is attempted | The correction names the entry it corrects; any caller, including the schema owner, is refused an UPDATE or a DELETE | A correction appends a new entry with `corrects_entry_id` and the corrected entry stays unchanged; an UPDATE or a DELETE changes nothing |
| Appended | The daily chain check and the daily seal run | JOB-14 and the seal of the baseline | Sealed: the entry is unchanged and the chain is verified |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | Takes the correction and the send that produce the two records (Documents CRU on a case in scope) and reads the entries of that case (Decision log R) |
| RW-CASEOWN, case owner | The same, for the treatment of the case in scope |
| RW-LEGAL, legal counsel | Owns which merge fields are overridable, and reads the entries (Decision log R) |
| RW-TEAMMGR, team manager | Reads the entries of the cases in scope (Decision log R) |
| SY-DECLOG, decision record writer | Writes the two records through the record path inside the action transaction at the producer and appends them to the ledger here; the append is the service identity's and not a person's |
| RW-AUDIT, internal audit | Reads the ledger by case, by decision code and by date range, and one entry with its references and its chain fields (Decision log R, scope ALL) |
| Every role of TSD P7 v2 T6.1 | Holds R on the decision log and reads the entries of the cases in its scope |
| A role outside the matrix, or a case out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, and appends the entry, its inbox row and its idempotency row (DP-02) |
| `rwb-document` | Owns the screens, the draft store, the regeneration, the locked-value checks, the write-once copy, the signature request and the document states; this story holds no authority over any of them |
| `rwb-comms`, `rwb-treatment`, `rwb-access` | Own the template version and its Legal approval, the treatment and its `decision_log_id`, and the role, scope and right answer; this story writes none of them |
| No approval level from the delegation of authority applies | The treatment was approved at D6.4 before generation; this story records the correction and the send and reads no `delegation_limit` row |

The authorisation decision behind the two reads is `rwb-access`'s role, scope and right data, taken through the authorise answer the service already holds; this story adds no guard of its own and holds no role, scope or delegation row (ASM-2261). The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1278; ASM-2261).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id (the case reference `RW-2026-000401`) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code (D6.4, a value of LOV-DECISION) | Write |
| DF-DEC-004 to DF-DEC-007 | `decision_log_entry` | rule_id, rule_version, model_version, agent_version | Not written: no rule, no model and no agent take part in a correction or a send, and the treatment approval that allowed it is its own entry |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the merge snapshot reference of the correction, the document set reference of the send) | Write; the shape of the reference is Not specified in the source documents (GAP-1278; ASM-2257) |
| DF-DEC-009 to DF-DEC-011 | `decision_log_entry` | recommendation, approver_user_id, approval_level | Not written: a correction follows an approved treatment and proposes nothing, and the approval of the treatment is the decision center's and another story's |
| DF-DEC-012 | `decision_log_entry` | final_call (SENT_FOR_SIGNATURE on the send; the correction final call is read from the list in force) | Write |
| DF-DEC-013 | `decision_log_entry` | override_reason (the reason "Signing appointment moved by the customer" on the correction) | Write on the correction only |
| DF-DEC-014 | `decision_log_entry` | actions (the corrected field, the old and new value identifiers, the document reference, the template codes and versions, the set reference, the write-once reference and the requesting role) | Write; the container is TSD P7 v2 T3.1 and its content is Not specified in the source documents (GAP-1278; ASM-2257) |
| DF-DEC-015 | `decision_log_entry` | outcome (the `doc_version` the correction produced, the sent state the send produced, as identifiers only) | Write |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017 | `decision_log_entry` | prev_hash | Write |
| DF-DEC-018 | `decision_log_entry` | entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write on a correction of an entry only |
| DF-DEC-030 | `decision_log_entry` | actor_user_id (the service identity of the append) | Write |
| DF-DEC-031 | `decision_log_entry` | idempotency_key (`S-0401` on the send) | Write |
| DF-CAS-001, DF-CAS-002 | `recovery_case` (P3) | id, case_no | Read as facts of the record, never a table |
| DF-TRT-001, DF-TRT-003, DF-TRT-004, DF-TRT-013 | `treatment` (S2) | id, decision_log_id, treatment_type, outcome | Read as facts of the record, never a table |
| DF-REF-046, DF-REF-047, DF-REF-051 | `template` (P6) | template_code, template_version, approved_by_legal | Read as facts of the record; the catalog itself is never read here |
| DF-DOC-001, DF-DOC-004, DF-DOC-011 | `document` (P5) | id, document_type, doc_version | Read as facts of the record; the document row is never read here |
| (reference lists) | reference data (P3) | LOV-DECISION and the final-call list, with the version in force | Read through the reference-data contract of DP-07, never a table |
| (parameters) | `parameter_value` (P3) | the page-size bound and the completeness target | Read through the parameters contract of DP-06, never a table |
| (inbox) | `processed_event` | event_id, consumer, processed_at | Write |
| (outbox) | outbox library table in `rwb_decision` | the outbox row of the append where the service publishes one | Write |
| (idempotency) | `idempotency_key` | the record's key `S-0401` and the first entry ID | Write |

No row of `recovery_case`, `treatment`, `template`, `merge_field`, `document`, `document_hub_parameter` or `delegation_limit` is copied into `rwb_decision`: the case, the treatment, the template and the document reference arrive as facts of the record, and the merge snapshot and the file stay in `rwb_document` (DP-01). The transfer price 1250000.00 and 1200000.00, the contract date "2026-12-10" and "2026-12-12", the Thai long date "12 December 2569 BE" and the reason are named in this document as legacy values only and are written in no entry except the reason, which the legacy story puts in `override_reason` (BR1, BR7, BR8). Field IDs are those of the Logical Data Model and Data Dictionary v9 and TSD P7 v2 T3.1.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007) and the Ownership Map gives to P7. The service's task queue is `rwb-decision` in namespace `rwb-recovery` and its Java package is `th.co.scb.ace.workbench.recovery.decision`. The request and response field set of a correction or send entry is Not specified in the source documents (GAP-1278; ASM-2257).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | API-P7-006: search the ledger by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | API-P7-007: read one entry with its decision code, its final call, its reason, its references, its template versions, its requesting role and its chain fields; 200 with the DecisionLogEntry | Decision log, right R, scope applied | Not applicable, read only |

The DecisionLogEntry body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `finalCall`, `inputsRef`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`, and for the two records of this story the corrected field with its old and new value identifiers and the document reference, or the document set reference with the write-once reference and the template versions, and the requesting role. The DecisionLogPage body carries `items`, `page`, `size` and `total`. The field-level shape is the reading of ASM-2257.

Errors: 401 no session (Not specified in the source documents (CG-ALL-7221)); 403 the role lacks the Decision log right (MSG-P4-002); 404 the entry or the case is absent or outside the scope (MSG-P4-003); 422 a query value is outside its list (Not specified in the source documents (CG-ALL-7221)); 503 the ledger is unavailable (Not specified in the source documents (CG-ALL-7221)). Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001), the approval operations (API-P7-002 to API-P7-005 and API-P7-008) and the rule-registry paths belong to the other P7 stories of this service; this story declares none of them.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access (Architecture v5 slide 14) | The cached role, scope and Decision log right decision behind the two reads; consumed, faked, one hop with a 2 s timeout and a breaker (DP-11), and in no C row of this story (GAP-1278; ASM-2261) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION, which holds D6.4, and the final-call list, at the version in force (DP-07); faked |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | The page-size bound of the search and the completeness target of the ingest (DP-06); faked |

The fakes named in 12.8 stand behind those rows and behind the two records under test: the **rwb-document E2017 contract fake** (RWB-P5-E2017-CON) poses the correction and the send with their records, the **rwb-comms template catalog fake** supplies the template code and version each record names, the **rwb-treatment fake** supplies the treatment with its `decision_log_id`, the **rwb-access fake** answers the authorise call, the **decision-record library fake** (RWB-PLT-E1027-CON) supplies the append, the chain and the append-only refusal, and the **central ledger fake** supplies the ledger reference and the completeness reading. The two records themselves arrive on `rwb.decision-record.v1` and not over REST.

#### 12.3 Events published

None. This story publishes no event of its own: the two records are facts of `rwb-document` on `rwb.decision-record.v1` and the entries of the ledger are read through the operations of 12.1. `rwb.decision.DecisionRecorded.v1` is published by the owning service of each decision and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42, event 08). The service's own topic `rwb.decision.events.v1`, with the event names `rwb.decision.ApprovalRequested.v1`, `rwb.decision.ApprovalDecided.v1` and `rwb.decision.RulePackageInForce.v1`, belongs to the approval and rule-registry stories of this service and is not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger and its shared topic; published by `rwb-document` for the correction and the send decisions | `DocumentRecordListener`: inbox dedupe by event ID and by the record's idempotency key, then `DecisionLogAppendService` for the decision code, the final call, the reason, the value pair identifiers, the document reference, the set reference, the write-once reference, the template versions, the case and the requesting role |

The fact carries IDs, codes, versions, references and the reason only; no merge value, no formatted value, no party name and no file byte travels on the topic (BR7). Which fields of the fact this service requires is Not specified in the source documents (GAP-1278; ASM-2257); the reading this story applies is that of ASM-2257.

#### 12.5 Workflows and activities

None. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09. The correction, the regeneration, the write-once copy and the signature request run in `rwb-document` and are neither started nor signalled here. This story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit.

#### 12.6 Schedules

None. The ingest of `rwb.decision-record.v1` is continuous Kafka, as JOB-13 states (Architecture v5 slide 44), and the daily chain check JOB-14 at 02:00 is the decision-log baseline's and covers these entries like any other; the daily seal of the ledger to write-once storage is the baseline's too. This story creates no Temporal Schedule and starts nothing on a clock.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The correction entry and the send entry, their reason, their references, their final calls and their chain positions; append only |
| `approval` | P7 (`rwb_decision`) | Not read and not written here: the approval of the treatment is the decision center's |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | Not read in this story: no rule package is evaluated |
| decision record (local library) | P7 rows in `rwb_decision`, written through the record path | The append of DP-03 and its hash chain |
| `outbox_event`, `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Outbox, inbox and idempotency objects (DP-09) |

Not owned and never read: `document`, `document_type` and `document_hub_parameter` (P5), `template` and `merge_field` (P6), `treatment` (S2), `recovery_case`, `parameter_value`, `lov_value` and `reference_row` (P3), `role`, `permission`, `masking_rule` and `delegation_limit` (P4). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document E2017 contract fake | RWB-P5-E2017-CON | The correction of `DOC-0411` with the value pair `contract_date` "2026-12-10" to "2026-12-12" and the reason; the send of `TRT-0401` under `S-0401` with the set reference and the write-once reference; the refused correction of a locked `transfer_price`; the refusal of a SENT document and of a stale version; the refusal of a set with a DRAFT document, of a superseded template version and of the treatment `TRT-0402`; the signature start that answers UNAVAILABLE and then ACCEPTED; the refused append |
| rwb-comms template catalog fake | RWB-P6-E1046-CON | Template `DIL-CONTRACT` version 2, `DIL-CA` version 1 and `DIL-MORTGAGE` version 1 approved by Legal, and `DIL-CONTRACT` version 3 current after the drafts |
| rwb-treatment fake | The S2 treatment contract | Treatment `TRT-0401` of type `DEED_IN_LIEU` with `decision_log_id` set and no outcome; treatment `TRT-0402` with no `decision_log_id` |
| rwb-access fake | The P4 authorise contract of Architecture v5 slide 14 | The allow answer for role `RW-RESTRUCT` with the Decision log right R and the case in scope; the refusal of MSG-P4-002 for a caller without the right; the refusal of MSG-P4-003 for a case outside the scope |
| rwb-case contract fake | P3 rwb-case contract (DP-06, DP-07; library version Not specified in the source documents (DOR-RWB-P7-E2017-APP-22)) | LOV-DECISION with D6.4 and the final-call list at the version in force; the page-size bound of the search and the completeness target of the ingest |
| decision-record library fake, and the central ledger fake | RWB-PLT-E1027-CON, and the ledger side of `rwb.decision-record.v1` | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the idempotency key `S-0401` and a forced failure for AC4 and AC5; with the ledger reference of the entry, the completeness reading, the replay of the same fact and the chain head AC8 asserts against |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 3 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the authorise answer and the two `rwb-case` reads consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed; no event published on `rwb.decision.events.v1` and no new topic |
| Temporal | None | No workflow, no activity and no Schedule on `rwb-decision`; the correction and the send activities are `rwb-document`'s and the chain check is the baseline's |
| File | None | No file input and no file output; the rendered file, the write-once copy and the merge snapshot never leave `rwb-document` |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/documentscreens`, Java package `th.co.scb.ace.workbench.recovery.decision.documentscreens`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which pattern has an instance in this slice: DP-03 is the two records — the append through the decision-record path, the `prev_hash` and `entry_hash` chain, the append-only rule and the shared topic `rwb.decision-record.v1`, with its H RWB-PLT-E1027-CON. DP-01 is the boundary — the entries live in `rwb_decision`, and the document, the template, the treatment and the case are never read as tables. DP-07 is LOV-DECISION and the final-call list read as reference data with the version in force. DP-11 is the one hop with a 2 s timeout and a breaker on the authorise call and on the two `rwb-case` reads. DP-13 is the service's own base, so no operation of the monolith base is declared here. DP-19 is the gateway-bff route through which SCR-38 Decision log query and the auditor's view reach the two operations.

The platform H dependencies of the DP table — H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1044-CON and H RWB-PLT-N001-CON — and the C dependencies of the published contracts of other services — C RWB-P3-E1042-CON, C RWB-P3-E1043-CON and the authorise contract of P4 — are not in the metadata rows of this story, which name None and RWB-P5-E2017-CON; they are the dependencies the DP table adds and they are recorded in GAP-1278 and ASM-2258, ASM-2261. The decision-log store baseline of this service (`decision_log_entry`, its append-only trigger and its JOB-14 check) is not in the metadata H row either and is carried in the same gap and assumption. None of them blocks the build beyond Day 1: they are platform and store contracts of waves 0 and 1 and the published contracts of `rwb-case` and `rwb-access`, built against their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DocumentRecordListener | Kafka consumer with the inbox | Reads `DecisionRecorded` on `rwb.decision-record.v1`, deduplicates by event ID and by the record's idempotency key, keeps the D6.4 correction facts and the SENT_FOR_SIGNATURE send facts and hands them to the appender; every other decision code stays with the baseline's general ingest |
| DecisionLogAppendService | Service | Checks the decision code, the final call, the reason, the document reference and the template versions of the record, and writes the entry, its chain position, its inbox row and its idempotency row in one transaction (BR1, BR2, BR11, BR12) |
| ChainHasher | Service | The canonical form of an entry and its SHA-256, the first `prev_hash` of 64 zeros and the `prev_hash` of every later entry (BR5) |
| DecisionLogQueryController | Controller | The two operations of 12.1 with the declared right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogQueryService | Service | The search and the single read, the row shape of a correction entry and of a send entry, and the total count of the page |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, insert only, with the search indexes and the idempotency key |
| ReferenceListClient | Client | LOV-DECISION and the final-call list through the reference-data contract of DP-07 with the version in force |
| ParameterClient | Client | The page-size bound and the completeness target through the parameters contract of DP-06 |
| AuthoriseClient | Client | The cached authorise answer of `rwb-access` behind the two reads, one hop with a 2 s timeout and a breaker (DP-11) |

**Database and migrations**

- Writes `decision_log_entry`, its inbox and idempotency rows and its outbox row, all in schema `rwb_decision`; reads no other schema (DP-01).
- The table, its columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE and the unique key on the idempotency key belong to the decision-log store baseline of the service and are not rebuilt here (GAP-1278; ASM-2261).
- One migration step in the per-service Flyway sequence (DP-15): `V2026_2__decision_log_documentscreens_index.sql` adds the composite index `ix_declog_documentscreens_case ON decision_log_entry (case_id, decision_code, decided_at)`, sorted by `decided_at` descending, that the two searches use. The index name is Not specified in the source documents (GAP-1278; ASM-2257).
- No row of `document`, `template`, `treatment`, `recovery_case` or `parameter_value` is written here: those tables are their owners' and arrive as facts or through their contracts.
- The schemas `rwb_case`, `rwb_comms`, `rwb_document` and `rwb_treatment` are owned by their services; this story reads and writes none of them as tables (DP-01).

**Configuration and reference data**

- LOV-DECISION, which holds D6.4, and the final-call list are reference data read through DP-07 with the version in force; the decision code D6.4 and the final call SENT_FOR_SIGNATURE are the legacy values and the correction final call is read from the list (GAP-1278; ASM-2257).
- The page-size bound of the search and the completeness target of the ingest are parameters of DP-06; their names are Not specified in the source documents (GAP-1278; ASM-2258), and the story holds no default.
- The merge snapshot reference and the write-once reference are opaque strings supplied by the contract; this story validates nothing of their content and never resolves the snapshot (GAP-1278; ASM-2257). The outbox retry policy and the inbox retention are the platform's (RWB-PLT-TE006-CON).
- No feature switch of this story's own is named by a source; the capability is present wherever a record arrives. The screens switch `rwb.document.generation-screens` of the legacy story names the screens only and is `rwb-document`'s (GAP-1278; ASM-2260).

**Build steps**

1. `DecisionLogRepository` and the index step; test the search by case and by decision code and the single read, and that an INSERT outside a transaction is refused (AC10).
2. `ChainHasher` and the canonical form: `chain_seq`, `prev_hash` from the previous entry, the first `prev_hash` of 64 zeros and `entry_hash` as the SHA-256 of the canonical form (AC6).
3. `DocumentRecordListener` with the inbox and the dedupe by event ID and idempotency key; test the replay of the same fact and the repeat of AC7.
4. `DecisionLogAppendService` with the checks of BR11 and the fail-closed transaction; test the forced failures of AC4 and AC5 and the chain position the refused write does not use.
5. The correction row shape and the send row shape: the reason in `override_reason`, the corrected field, the old and new value identifiers and the document reference with the template code and version; and final call SENT_FOR_SIGNATURE with the set reference, the write-once reference and the three template versions, for the set and not for each document (AC1, AC2, AC3).
6. The append-only rule: the trigger and the grant, with the four statements of AC6 refused and the audit line written; and `ReferenceListClient` and `ParameterClient` with the version in force, refusing rather than assuming a code or a final call (BR11).
7. `DecisionLogQueryController` with the declared right, the scope, the paging and the problem mapping; tests for AC10, MSG-P4-002 and MSG-P4-003 (TC-E2-017-14).
8. `AuthoriseClient` against the authorise fake, the contract-fake run of the whole slice with the document, catalog, treatment, access and ledger fakes green from Day 1, and the boundary test: no write to `rwb_document`, `rwb_comms`, `rwb_treatment` or `rwb_case`, and no merge value, formatted value, Thai long date or file byte in any entry, event payload or log line (AC2, BR7).

**Done when.** The tests of section 16 pass, the chain of a SIT day verifies from the first entry with no break, a correction leaves one entry naming the field, the value pair identifiers and the document, a send leaves one entry with SENT_FOR_SIGNATURE and the set reference, a refused action leaves none and does not consume a chain position, a repeated record leaves one entry, both reads answer inside the 2 s budget of the frame, and no document, template, treatment or case was changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | A correction or send record cannot be appended, or the record lacks a value the entry requires | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record path, on the append; the action answers it with 503 and rolls back |
| MSG-GEN-004 | A correction is saved against an old version, or a duplicate record arrives for the same action | Someone else changed this record. Reload it to see their change. | `rwb-document` on the stale version; this story asserts it and never rewrites it |
| MSG-P5-002 | A correction of a document already SENT | Legal documents cannot be changed. Add a new version instead. | `rwb-document`; this story asserts it |
| MSG-P5-013 | A send with a document not REVIEWED or on an old template version | {document} cannot be sent yet: {reason}. | `rwb-document`; this story asserts it |
| MSG-P5-014 | A correction of a locked merge field | {field} comes from the approved treatment and cannot be changed here. | `rwb-document`; this story asserts it |
| MSG-P5-011 | A send for a treatment not approved or not open | Documents can be generated only for an approved {treatment} that is still open. | `rwb-document`; this story asserts it |
| MSG-GEN-001 | A correction without a reason | Enter {field}. | `rwb-document`; this story asserts it |
| MSG-GEN-006 | The signature service is unavailable | {system} is not available. Try again in a few minutes. | `rwb-document` through the signature contract; this story asserts it |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of the read |
| MSG-P4-003 | The case or the entry is outside the caller's scope | Not specified in the source documents (GAP-1278; ASM-2259) | This story, through the authorise answer of the read |

MSG-P7-003, MSG-P5-002, MSG-P5-013, MSG-P5-014, MSG-P5-011, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006 and MSG-P4-002 are copied unchanged from RWB-E2-017 section 14. The message id set of this slice beyond them has no source and is carried in GAP-1278 with ASM-2259. Thai text for each message follows decision DL10.

Open decisions DL10 and DL26 remain open. Each rests on its assumptions: DL10 on ASM-2250, ASM-2357, ASM-2377 and ASM-2863; DL26 on ASM-0247, ASM-0264, ASM-0275 and ASM-0355. The programme directive confirms each assumption.

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one: 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-GEN-004 on the action, and 503 with MSG-P7-003 on the record path.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by SCR-38 Decision log query, which searches the log by case, rule, approver and date with export (FSD P7 v3), and by the auditor's view of the ledger; both are reached through the gateway-bff composite route of DP-19 and are another story's. SCR-14 Treatment record and SCR-30 Case documents are `rwb-document`'s and RWB-P5-E2017-APP's, and this story feeds neither of them.

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The D6.4 correction entries and the SENT_FOR_SIGNATURE entries of the case in decidedAt order, each with its final call, its document or set reference and its requesting role |
| The entry read | One correction entry or one send entry | For the correction the reason, the field, the old and new value identifiers, the document reference and the template version; for the send the set reference, the write-once reference and the three template versions; both with `decidedAt`, `prevHash` and `entryHash` |
| The entry read | An entry with `correctsEntryId` | The correction beside the entry it corrects, and the corrected entry unchanged |
| The read | 403, or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for a case outside the scope; no row is returned |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-7227) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-7227) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-7227) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-7227) |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-7228) |
| SCR-30 Case documents | Loading | As in Screen Specifications v1, section SCR-30 |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-7228) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-7228) |
| SCR-38 Decision log query (P7) | Empty | Not specified in the source documents (CG-ALL-7229) |
| SCR-38 Decision log query (P7) | Loading | As in Screen Specifications v1, section SCR-38 |
| SCR-38 Decision log query (P7) | Error | Not specified in the source documents (CG-ALL-7229) |
| SCR-38 Decision log query (P7) | No access | Not specified in the source documents (CG-ALL-7229) |

A panel or screen id for showing the two records beside the documents on SCR-14 or SCR-30, and the field list of SCR-38, are Not specified in the source documents (GAP-1278; ASM-2260). The screen field list and the composite route specification belong to RWB-PLT-N001-CON and to the story that owns SCR-38.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-14 | AC10, BR10; legacy Covers "Access" | Component | RW-TEAMMGR user (Documents R) calls the send and the two reads; refused with MSG-P4-002 |
| TC-E2-017-01 | AC6, BR5; legacy Covers "AC1, BR1, BR2" (the generation is RWB-P5-E2017-APP and the GENERATED entry RWB-P7-E2026-APP) | Contract | Synthetic mortgage DIL treatment and a chain whose head is the D6.4 GENERATED entry |
| TC-E2-017-02 | AC1, AC2, BR1, BR8; legacy Covers "AC2, BR3, BR4, BR5" | Component | Contract date moved by two days on DOC-0411 with the reason |
| TC-E2-017-03 | AC3, BR2, BR3; legacy Covers "AC3, BR6, BR7, BR8" | Contract | Three reviewed drafts; the send record with the set and write-once references |
| TC-E2-017-04 | AC8, BR11; legacy Covers "AC4, BR2" | Component | Treatment TRT-0402 with no decision_log_id |
| TC-E2-017-05 | AC9, BR11; legacy Covers "AC5, BR3" | Component | Empty reason |
| TC-E2-017-06 | AC9, BR11; legacy Covers "AC6, BR3" | Component | Locked transfer price |
| TC-E2-017-07 | AC8, BR11; legacy Covers "AC7, BR6" | Component | One draft not reviewed |
| TC-E2-017-08 | AC9, BR11; legacy Covers "AC8, BR7" | Component | Document in state SENT |
| TC-E2-017-09 | AC4, BR6, BR12; legacy Covers "AC9, BR4" | Component | Decision log stub refusing writes on a correction |
| TC-E2-017-10 | AC7, BR3; legacy Covers "AC10, BR10" | Component | Same send key S-0401 twice |
| TC-E2-017-11 | AC9, BR11; legacy Covers "AC11" | Component | Two sessions on one draft |
| TC-E2-017-12 | AC11, BR6; legacy Covers "AC12" | Contract | P6 signature stub returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13 | AC8, BR11; legacy Covers "AC13, BR6" | Component | Template version 3 made current after the drafts |
| TC-E2-017-15 | AC5, BR6, BR12; legacy Covers "Principle 5" | NFR | Decision log write forced to fail on a send; nothing sent, documents stay REVIEWED, MSG-P7-003, incident raised |
| TC-E2-017-16 | ASM-3438; section 12.7 | Contract | Correction and send run once each; only decision_log_entry and its inbox and idempotency rows change; no row of document, treatment, template, case, approval or rule table changes |
| TC-E2-017-17 | AC12, BR9, BR13 | Component | The correction and the send entries with the reference-data contract in force; no row of document, treatment, template or case is written |
| TC-P7-E2017-APP-01 | AC1 | Component | Contract date moved by two days on DOC-0411 with the reason |

The fifteen legacy test cases of RWB-E2-017 are kept in the order of the work package, and each is answered here on the record side: the entry, its reason, its value pair, its references, its chain, its two reads and its refusals. The generation, the regeneration, the locked-value check, the write-once copy, the signature request and the document states are the contract fakes' and `rwb-document`'s. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The `-ITG` copies of these cases end in `-ITG` and belong to RWB-ITG-E2017-ITG, which runs the same values across the contracts. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision code, the final-call set, the page-size bound, the completeness target and the message ids are reference or parameter rows, and the template codes, treatment types and document types are facts of their owners; nothing of them is a constant here.
- No personal data in the entries, the event, the audit line, the tests or the logs: the case reference, the document reference, the template codes and versions, the decision code, the final call, the reason the officer typed, the hashes and dates only. The borrower name, the national ID number, the transfer price, the title deed number and the file byte stay in `rwb_document` (BR7).
- No read of another service's tables (DP-01): the template, the treatment and the document arrive as facts of the record, the case and the reference lists through the `rwb-case` contracts, and the authorise answer through `rwb-access`.
- One appender and no mover: this story changes no document, no template, no treatment and no case, so a decision record can never move a case (BR9).
- No entry without its action and no action without its entry: the entry, its chain position, its inbox row and its idempotency row commit in one transaction, and a correction or a send whose record cannot be written is rolled back with an incident (BR12, R-UNI-39).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the chain is verifiable from `chain_seq` 1 (BR4, BR5).
- One entry per action: the inbox dedupe, the idempotency key and the refusal of a duplicate make a second entry impossible, so a three-document set is one entry and not three (BR2, BR3).
- One base and one topic: `/api/recovery/decision/v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no monolith base and no other service's base or topic is declared here as this service's own.
- One hop and 2 s with a breaker per downstream on the authorise call and the two `rwb-case` reads; an unreadable list or parameter refuses the append rather than writing an assumed value (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Business Requirements Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-UNI-39, R-UNI-40 | TC-E2-017-01 to TC-E2-017-03, TC-E2-017-09, TC-E2-017-15, TC-E2-017-16 |
| REQ-OCC-002 | Letter templates versioned, with the Legal approval recorded against the version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03, R-UNI-38 | TC-E2-017-03, TC-E2-017-13 |
| REQ-OCC-009 | The signature path is chosen by product and Legal rule, and a set leaves only when every document is reviewed and on the current template version | Business Requirements Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu | R-DIL-18, R-RES-16, R-LIT-03 | TC-E2-017-07, TC-E2-017-12, TC-E2-017-13 |

REQ-DCM-012, REQ-OCC-002 and REQ-OCC-009 are carried on this story only for the two records and their two reads; the render, the store, the template approval, the treatment, the signature path and the access answer belong to their own slices. The ledger features the slice uses are FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-04 and FEAT-DRI-05 of FSD P7 v3, whose append-only table, chain check and seal are the baseline of this service.

| Legacy reference | Where it is kept |
|---|---|
| The correction entry with decision code D6.4 and the reason as override_reason, and the send entry with final_call SENT_FOR_SIGNATURE (legacy AC2, AC3, BR4, BR6, BR7) | Sections 1, 4, 7 (AC1, AC2, AC3), 8 (BR1, BR2, BR8), 11 |
| A correction or send whose record cannot be written does not proceed (legacy AC9, BR9) | Sections 5 (X2, X3), 7 (AC4, AC5), 8 (BR6, BR12), 14 |
| Append only and hash chained, with the first `prev_hash` of 64 zeros, and the repeat with the same Idempotency-Key "S-0401" (legacy AC10, BR10) | Sections 4, 5 (X4, X8), 7 (AC6, AC7), 8 (BR3, BR4, BR5), 9 |
| The refusals of the owners: locked field, empty reason, SENT document, stale version, reviewed set, current template version (legacy AC5, AC6, AC7, AC8, AC11, AC13) | Sections 5 (X5, X6), 7 (AC8, AC9), 14 |
| The signature request refused (legacy AC12) | Sections 5 (X7), 7 (AC11), 14 |
| Case RW-2026-000401, treatments TRT-0401 and TRT-0402, document DOC-0411, template codes DIL-CONTRACT, DIL-CA and DIL-MORTGAGE, team FCR-BKK, and the values contract_date "2026-12-10" to "2026-12-12", the reason, transfer_price 1250000.00 and 1200000.00, "12 December 2569 BE" | Sections 3, 7, 11, 16 |
| Messages MSG-P7-003, MSG-P5-002, MSG-P5-013, MSG-P5-014, MSG-P5-011, MSG-GEN-001, MSG-GEN-004, MSG-GEN-006, MSG-P4-002, MSG-P4-003 | Section 14, exception paths |
| Rules R-DIL-14, R-DIL-16, R-DIL-18, R-RES-16, R-LIT-03, R-UNI-38, R-UNI-39, R-UNI-40 | Sections 2, 8, 18 |
| Legacy key RWB-E2-017, story RWB-P7-E2017-APP, contract RWB-P5-E2017-CON | Metadata, sections 3, 12 |
| Test cases TC-E2-017-01 to TC-E2-017-15, and the decoupling patterns DP01, DP03, DP07, DP11, DP13, DP19 | Section 16; metadata; section 13 |

The other slices of the key answer the rest: RWB-P5-E2017-APP and RWB-P5-E2017-CON the screens, the correction, the regeneration, the locked-value checks, the write-once copy, the signature request and the document states; RWB-P6-E1046-APP and RWB-P6-E1034-APP the template catalog, the versions and the Legal approval; RWB-S2-E2026-APP the treatment and its `decision_log_id`, and writes no decision record of key RWB-E2-017; RWB-P4-E2017-APP the session, the scope, the rights and the access entries; RWB-P7-E2026-APP the D6.4 GENERATED record at generation time; and RWB-ITG-E2017-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope

- The generation screens SCR-14 and SCR-30, the draft store, the regeneration as the next `doc_version`, the locked-value checks, the write-once copy, the signature request and the document states DRAFT, REVIEWED and SENT: `rwb-document` (P5), RWB-P5-E2017-APP and RWB-P5-E2017-CON.
- The template catalog, the merge field catalog, the template versions and their Legal approval: `rwb-comms` (P6), RWB-P6-E1046-APP and RWB-P6-E1034-APP.
- The treatment, its approval at D6.4 and its `decision_log_id`: `rwb-treatment` (S2), RWB-S2-E2026-APP.
- The session, the role, the scope, the Documents right U and the access entries of a look or a refusal: `rwb-access` (P4), RWB-P4-E2017-APP.
- The D6.4 GENERATED record written at generation time: RWB-P7-E2026-APP, which this story neither writes nor changes.
- The e-signature flow and the return of the signed copy: `rwb-comms` (P6), the successor of RWB-E2-018; the signature path rule R-DIL-18 and R-RES-16 belong there.
- The recommendation read, the approval operations, the approval queue and the rule registry: the other P7 stories of this service. This story evaluates no rule package and loads no Drools kit.
- The general ingest of every other decision code into the ledger, the append-only table itself, the daily chain check JOB-14 at 02:00 and the daily seal: the decision-log baseline of this service.
- The data-lake copy of the log, JOB-13 and lake retention: retired with the data lake (DP-17); the ingest of the ledger is continuous Kafka.
- SCR-38 Decision log query as a built screen, the panels on SCR-14 and SCR-30 and the composite route: the screen stories and RWB-PLT-N001-CON.
- Rule-driven generation at TRANSFER_PRICE_SET (FEAT-TRT-18, Epic 3) and debt sale agreements and notices (FEAT-DBS-10, Epic 6), as the legacy story left them.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E2017-ITG.
- The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: an OPS story of this legacy key.
