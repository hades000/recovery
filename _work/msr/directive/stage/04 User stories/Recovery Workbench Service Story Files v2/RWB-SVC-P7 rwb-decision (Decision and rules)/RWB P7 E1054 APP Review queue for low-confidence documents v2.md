# RWB-P7-E1054-APP Review queue for low-confidence documents

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E1054-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-054 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP09, DP11, DP13, DP15, DP19 |
| Parallel lane | L-P7-O |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement. Not specified in the source documents (DOR-RWB-P7-E1054-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E1054-CON |
| Contract version | Builds against the /v1 path of the contract dependencies above. No fixed version number is specified in the source documents (DOR-RWB-P7-E1054-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DCM-005, REQ-DCM-019) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-054 for rwb-decision — the record of every review decision of the document hub, collected from the shared decision-record topic into the chained ledger of `rwb_decision`, validated against the review item it names. The queue, the screen, the OCR text, the field corrections and the labeled set stay with rwb-document (P5); the review task and its scope with rwb-case (P3); the access answer and the masking with rwb-access (P4). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E1054-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 24 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **internal auditor (RW-AUDIT) and a center of excellence analyst (RW-COE)**, I want **the record of every review decision of the document review queue — the attach, the confirm, the correct and the discard — to arrive on the shared decision-record topic from the service that took it, to be checked against the review item it names, and to be appended once to the chained ledger in `rwb_decision` with the actor, the outcome, the versions and the entry before it**, so that **no doubtful document is attached, confirmed, corrected or discarded without an entry that cannot be changed, so a review decision is reproducible from the log years later, and so a record that names an item that does not exist, or claims an outcome the item does not carry, is refused and reported instead of being filed as fact**.

Inside `rwb-decision` this is the decision-record side of legacy RWB-E1-054:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, shared topic `rwb.decision-record.v1` (DP-03, DP-13, DP-14).
- The capability is the **ingest of the review decisions** of `rwb.decision-record.v1` — the attach record the legacy story calls the DOCATT entry, and the record of the review completion — validated against the review item and appended to `decision_log_entry` with its chain link, its dedupe key and its actor.
- The screen, the queue rows, the OCR text, the candidates, the fields, the type change, the attach, the discard and the labeled examples stay in `rwb-document` (P5) and are RWB-P5-E1054-APP's; the review task, its queue and its scope are RWB-P3-E1054-APP's; the rights, the scope answer and the masking are RWB-P4-E1054-APP's. This story builds no screen, corrects no value, holds no document and publishes no business event of its own.
- The decision codes, the outcome values and the reasons are reference rows in force, read through the reference-data contract (DP-07). The review decision codes and the placement of the review facts inside the record's `actions` and `outcome` are Not specified in the source documents (GAP-2456; ASM-4079) and (GAP-2456; ASM-4080).
- No REST operation is declared here as the write path: the Ownership Map gives P7 the two decision-log reads (RWB-P7-E2005-APP) and no append operation, so the ledger of this service is written by the consumer only (DP-01, DP-03).

### 2. Business rationale

A wrong type or a wrong hearing date on a court notice puts the wrong date on a case and the litigation timers run from it, which is why RWB-E1-054 sends every item the pipeline could not type, read or match to a person. The process answer to "who checked this document and what did they decide" is not the document — it is the record. The legacy story makes the record a condition of the action: `DocumentStore` writes the DOCATT decision log entry first (legacy BR6), a person who cannot get it written gets nothing stored and an incident (legacy X13, TC-E1-054-19), and every discarded item keeps its reason and the person (REQ-DCM-019, legacy BR9). Principle 5 and CTL-12 hold the same line.

Architecture v5 changes where the record is written, not why. Every service writes its decision where the decision is taken and announces it on `rwb.decision-record.v1`; rwb-decision collects it into the ledger in `rwb_decision`, within five minutes, chained entry to entry, the chain checked every day (Architecture v5 slides 20, 28 and 44; ADR-022; DP-03). The review decision is therefore written in rwb-document's own transaction and lands here as an envelope. What the target adds is the part the monolith never needed: a second writer with a different clock, so the ledger must prove that each record it files names a review item that exists and an outcome that item carries, must file it once when the envelope is delivered twice, and must refuse and report it when neither holds — otherwise the log says a document was attached that was discarded, and the audit answer of RWB-P7-E2005-APP repeats the lie at scale.

This story is that check and that append. It meets REQ-DCM-005 and REQ-DCM-019 on the record side, and serves REQ-DRI-003 and REQ-DRI-004, NFR-033, NFR-034 and NFR-035 (TSD P7 v2 T7). The measure is that every review outcome of the document hub has exactly one verifiable ledger entry, that a repeated delivery adds no entry and no chain position, and that no entry exists for an item that does not exist or an outcome the item does not carry.

### 3. Preconditions

- RWB-P5-E1054-CON is published: the review item read with its review reason, review outcome and review status, the document read with its `review_status`, the resolve call and the review completion, the error envelope and the contract fake. The record of the review action is declared on `rwb.decision-record.v1` with the decision code DOCATT, the confirmed or corrected type, the item ID as `inputsRef` and the reviewer where a person decided.
- The shared topic `rwb.decision-record.v1` exists with its retry topic and its `.dlt`, and the `DecisionRecorded` envelope of the platform library is fixed: `rwb.decision-record.DecisionRecorded.v1`, CloudEvents 1.0 binary mode, key `caseId` where there is a case and the entry id where there is not, with the record fields `decisionCode`, `caseId`, `inputsRef`, `recommendation`, `approverUserId`, `finalCall`, `actions`, `outcome`, `actorUserRef`, `decidedAt` and `idempotencyKey` (DP-03, DP-09).
- `decision_log_entry` exists in `rwb_decision` with the canonical form, the chain columns `chain_seq`, `prev_hash` and `entry_hash`, the append-only rule and the verifier (RWB-P7-E1008-APP), and `processed_event`, `outbox_event` and `idempotency_key` exist in the same schema (DP-09).
- The reference-data contract of rwb-case is live (RWB-P3-E1043-CON through RWB-PLT-E1043-CON, DP-07) and carries LOV-DECISION and the outcome list in force. The review decision codes and the final-call values are Not specified in the source documents (GAP-2456; ASM-4079).
- The per-service Flyway sequence of rwb-decision runs (RWB-PLT-E1044-CON, DP-15), and the gateway-bff composite route exists (RWB-PLT-N001-CON, DP-19) for the screens other stories serve; this story serves no screen of its own.
- The rwb-decision service identity exists as one login for this service (DP-02). Its name is Not specified in the source documents (GAP-2456; ASM-4083).
- The document hub publishes the record of a review action in the same transaction as the action and answers 503 with MSG-P7-003 when it cannot, so the record of a review action exists or the action does not (legacy BR6 and X13; RWB-P5-E1054-CON).
- Depends on (build) is None: the story builds on Day 1 against the P5 contract fake and the published platform contracts.

### 4. Flow

1. rwb-document: an officer attaches, confirms, corrects or discards a review item; the action and the DOCATT record commit in one transaction, and the outbox relay publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case where the item has one and by the entry id where it does not (DP-03, DP-09).
2. rwb-decision: `DecisionRecordIngestListener` of consumer group `rwb-decision-ledger` reads the envelope, validates the CloudEvents attributes and the required record fields, and dedupes on `ce_id` and `idempotencyKey` in `processed_event` and `idempotency_key`.
3. `ReviewRecordValidator`: where the record carries a review decision code, it reads the review item through `GET /intake-items/{intakeItemId}` and, for a stored document, `GET /documents/{documentId}` on the P5 contract — one hop, 2 s (DP-11) — and checks that the item exists, that its review outcome agrees with the record's final call, and that its `review_status` agrees with the record's `actions`.
4. `DecisionChainAppender`: in one `rwb_decision` transaction it takes the next `chain_seq`, reads the `entry_hash` of the entry before it (64 zeros for the first), writes `decision_log_entry` with the record fields, `prev_hash`, `entry_hash` and the actor, and writes the `processed_event` row.
5. The entry is appended once: a repeated `ce_id` or `idempotencyKey` returns the first entry reference with `repeated` true and adds one to the repeat count of R-UNI-40; no second chain position is used.
6. A refusal — an item the P5 contract does not return, an outcome the item does not carry, or a code outside LOV-DECISION — appends nothing, consumes no chain position, and writes the envelope to the exception queue with its reason and its owner `RW-PLATADM`, raising incident `LEDGER_WRITE_FAILED` (FSD P7 v3 AC-EXC-P7-026-05).
7. A P5 answer outside the 2 s budget or a store failure retries the delivery; after four attempts in all the envelope goes to the `.dlt` topic with owner `RW-PLATADM` and the incident, and nothing is appended.
8. A replay from the `.dlt` topic or the exception queue appends the entry once, because the dedupe and the chain are both idempotent.
9. rwb-decision: the entry is now part of the ledger the two reads of RWB-P7-E2005-APP answer from, diffed by case, decision code, actor and date, with `chainVerified` on each row.
10. Nothing else moves: this story writes no document, no review status, no field and no queue row, and publishes no event of its own.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The same envelope arrives twice | One entry; the first reference is returned with `repeated` true and the repeat count rises by one; no second chain position | None | AC2 |
| X2 | The review item the record names is not returned by the P5 contract (404) | No entry, no chain position; the envelope goes to the exception queue with reason "review item not found" and owner RW-PLATADM; incident raised | MSG-P4-003 | AC4 |
| X3 | The record's final call disagrees with the review item's outcome, or its `review_status` disagrees with the document | No entry; the envelope goes to the exception queue with reason "outcome mismatch"; incident raised; earlier entries unchanged | None | AC6 |
| X4 | The decision code is outside LOV-DECISION in force | Refused at validation with MSG-P7-009 naming the field; nothing appended | MSG-P7-009 | AC5 |
| X5 | A required field is missing or the envelope is malformed | Refused at validation with MSG-P7-009 naming the field; nothing appended | MSG-P7-009 | AC5 |
| X6 | The P5 contract does not answer inside 2 s, or answers 503 | The delivery is retried; after four attempts in all the envelope goes to `.dlt` with owner RW-PLATADM and the incident; nothing appended | MSG-GEN-006 | AC8 |
| X7 | The ledger store is unavailable | Nothing is appended and no chain position is consumed; the delivery is retried; the incident is raised after the last attempt | MSG-P7-003 | AC8 |
| X8 | An update or a delete of a stored entry is attempted | Refused by the append-only grant and the store; a correction arrives as a new envelope naming the entry it corrects | None | AC7 |
| X9 | The consumer's transaction rolls back after the append | No entry and no `processed_event` row remain; a redelivery appends the entry once | None | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Ready on Day 1: the consumer, the validator and the appender build against the P5 contract fake and the platform topic; no build dependency and no waiting story |
| Negotiable | The decision codes, the outcome values and the reasons are reference rows; the retry count, the dedupe keys and the exception-queue owner follow the platform standards of DP-09 and the FSD of the ledger |
| Valuable | Every review decision of the document hub has one immutable, chained entry, or a refusal that names why, so "no document without its record" survives the split into 19 services |
| Estimable | One consumer, one validator, one chain appender, one exception path, two consumed operations and one migration |
| Small | Fits two weeks with its tests; no screen, no document, no approval and no rule evaluation |
| Testable | Every scenario of section 7 is one test against the P5 fake and a topic fixture with synthetic items, documents and users |

### 7. Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents — the record of every review decision

  Background:
    Given the shared topic rwb.decision-record.v1 is consumed on queue rwb-decision with its retry and .dlt topics
    Given LOV-DECISION is in force with the review decision codes and the outcome list in force carries "ATTACHED", "DISCARDED", "CONFIRMED" and "CORRECTED"
    Given the ledger of rwb_decision is empty at chain_seq 0 with the genesis hash of 64 zeros

  Scenario: AC1 The record of a review attach is appended once and chained (new, D-RCV-60)
    Given a DecisionRecorded envelope with ce_id "EV-7f3a-0001", ce_type "rwb.decision-record.DecisionRecorded.v1", ce_source "/rwb-document", decision code "DOCATT", inputsRef "IN-0101", case "RW-2026-000201", final call "ATTACHED", actor "U-LIT-01" and decidedAt "2026-12-04T09:30+07:00"
    Given the rwb-document contract mock returns review item "IN-0101" with review_outcome "ATTACHED" and document "DOC-0101" with review_status "CORRECTED"
    When the ingest consumes the envelope
    Then exactly one decision_log_entry exists with decision_code "DOCATT", inputs_ref "IN-0101", the case_id of "RW-2026-000201", chain_seq 1 and prev_hash of 64 zeros
    Then entry_hash equals the SHA-256 of the canonical form of the entry
    Then the actions carry documentRef "DOC-0101" and reviewStatus "CORRECTED" and no field value and no page of OCR text
    Then one processed_event row and one idempotency_key row commit in the same transaction as the entry

  Scenario: AC2 The same record delivered twice gives one entry (new, D-RCV-60)
    Given the envelope of AC1 is appended as chain_seq 1
    When the same ce_id "EV-7f3a-0001" with the same idempotency key arrives again
    Then one entry exists for "IN-0101" and its chain_seq stays 1
    Then the reference returns repeated true and the repeat count of R-UNI-40 is one
    Then the next accepted envelope takes chain_seq 2

  Scenario: AC3 The record of a completion follows the record of the attach (new, D-RCV-60)
    Given the attach record of "IN-0103" is chain_seq 1 with final call "ATTACHED"
    Given a DecisionRecorded envelope for the completion of "IN-0103" whose decision code is the review-completion code in force, final call "CORRECTED", actor "U-LIT-01" and decidedAt "2026-12-04T10:05+07:00"
    Given the rwb-document contract mock returns review item "IN-0103" with review_outcome "ATTACHED" and document "DOC-0103" with review_status "CORRECTED"
    When the ingest consumes the envelope
    Then the entry is chain_seq 2 with prev_hash equal to the entry_hash of chain_seq 1
    Then the actions carry reviewOutcome "ATTACHED", the review status and the field count of the record
    Then the entry names the actor "U-LIT-01" and the decided time of the envelope
    Then no field name, no field value and no OCR text is stored in rwb_decision

  Scenario: AC4 A record for a review item that does not exist is refused (new, D-RCV-60)
    Given a DecisionRecorded envelope for inputsRef "IN-9999" with decision code "DOCATT"
    Given the rwb-document contract mock returns 404 with MSG-P4-003 for the item "IN-9999"
    When the ingest consumes the envelope
    Then no entry is appended and no chain position is used
    Then the envelope is in the exception queue with reason "review item not found" and owner "RW-PLATADM"
    Then incident "LEDGER_WRITE_FAILED" is raised and the next accepted envelope takes chain_seq 1

  Scenario: AC5 A code or a field outside the lists in force is refused (new, D-RCV-60)
    Given the reference-data contract mock returns LOV-DECISION with "DOCATT" and without "D99"
    Given a DecisionRecorded envelope with decision code "D99" for item "IN-0105"
    When the ingest consumes the envelope
    Then the response of the ingest is a refusal with MSG-P7-009 naming "decisionCode"
    Then no entry is appended and the envelope goes to the retry topic once
    Given an envelope with no inputsRef at all
    When the ingest consumes it
    Then it is refused with MSG-P7-009 naming "inputsRef" and nothing is appended

  Scenario: AC6 A record whose outcome disagrees with the item is refused (new, D-RCV-60)
    Given the rwb-document contract mock returns review item "IN-0106" with review_outcome "DISCARDED"
    Given a DecisionRecorded envelope for "IN-0106" with final call "ATTACHED"
    When the ingest consumes the envelope
    Then no entry is appended and no chain position is used
    Then the envelope is in the exception queue with reason "outcome mismatch" and owner "RW-PLATADM"
    Then one incident "LEDGER_WRITE_FAILED" is raised and the ledger still verifies

  Scenario: AC7 The ledger is append only and a correction is a new entry (new, D-RCV-60)
    Given the review entries of "IN-0101" and "IN-0103" are chain_seq 1 and 2
    When an update of the entry at chain_seq 1 and a delete of it are attempted on the ledger
    Then both are refused by the append-only grant and the store
    Given a correcting envelope arrives with corrects_entry_id of the entry at chain_seq 1
    Then the new entry is chain_seq 3 and names the corrected entry
    Then the entry at chain_seq 1 is unchanged and the chain still verifies

  Scenario: AC8 A P5 timeout sends the envelope to the dead-letter topic (new, D-RCV-60)
    Given the rwb-document contract mock returns no answer inside 2 s for the item "IN-0108"
    When the ingest consumes a valid envelope for "IN-0108"
    Then the delivery is tried four times in all and no entry is appended
    Then the envelope is on the .dlt topic with owner "RW-PLATADM" and incident "LEDGER_WRITE_FAILED" is raised
    When the item then answers and the envelope is replayed from the .dlt topic
    Then exactly one entry is appended for "IN-0108"

  Scenario: AC9 The append commits with the inbox and the ledger has no write path (new, D-RCV-60)
    Given the published operations of /api/recovery/decision/v1 are the two decision-log reads of RWB-P7-E2005-APP
    When the ingest consumes a valid envelope and the consumer's transaction rolls back after the append
    Then no decision_log_entry row and no processed_event row remain
    Then no POST, PUT, PATCH or DELETE operation exists on the ledger of this service
    When the envelope is delivered again
    Then exactly one entry is appended with the next chain_seq

  Scenario: AC10 The chain is contiguous and an altered link fails verification (new, D-RCV-60)
    Given the review entries of "IN-0101" and "IN-0103" and the correcting entry of AC7 are chain_seq 1, 2 and 3
    When the chain of rwb_decision is verified
    Then every entry's prev_hash equals the entry_hash of the entry before it and chain_seq 1 has prev_hash of 64 zeros
    Given a copy of the ledger with the prev_hash of chain_seq 2 altered
    When the chain of the copy is verified
    Then the verification fails at chain_seq 2


```

The criteria above are new under D-RCV-60 and test the rwb-decision deliverable only: the ingest, the validation against the review item, the single append with its chain link, the exception queue and the append-only rule. This story owns no legacy acceptance criterion; legacy AC1 to AC17 are the document hub's, where the queue, the screen, the corrections, the type change, the attach and the labeled set are proved, and the case-side criteria are RWB-P3-E1054-APP's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One entry per review action: the entry is appended from the envelope of the service that took the decision; a repeated `ce_id` or `idempotencyKey` gives one entry and a repeat count, and never a second chain position | R-UNI-40; FSD P7 v3 AC-EXC-P7-002-03; DP-09 |
| BR2 | The record carries the decision code, the item, the document, the case, the outcome, the actor and the decided time — never a field value, an OCR page, a document body or a personal datum | RWB-E1-054 section 17; DP-09 |
| BR3 | A review record is validated against the review item before it is appended: an item the P5 contract does not return, an outcome the item does not carry and a code outside LOV-DECISION are refused and reported | DP-11; RWB-P5-E1054-CON |
| BR4 | The ledger is append only: no update, no delete and no write path over REST; a correction is a new entry naming the entry it corrects in `corrects_entry_id` | RWB-P7-E1008-APP; FSD P7 v3 AC-ALT-P7-001-01 |
| BR5 | The chain is contiguous: every entry's `prev_hash` equals the `entry_hash` of the entry before it, and the first is 64 zeros | FSD P7 v3 AC-ALT-P7-001-01; TSD P7 v2 DF-DEC-017, DF-DEC-018 |
| BR6 | The record names the versions: the rule version and rule ID where a rule decided, the model and agent versions where a model or an agent decided, the actor reference and the decided time | NFR-033, NFR-034; TSD P7 v2 T3.1 |
| BR7 | The record of a review action is written by its owner in the owner's transaction; when it cannot be written the action is not taken and the actor is answered MSG-P7-003, and this service never writes a record on behalf of another service | RWB-E1-054 BR6 and X13; Principle 5; CTL-12 |
| BR8 | The decision codes, the outcome values and the reasons are reference rows in force read through the reference-data contract; no code, outcome or reason is a constant | DP-07; BR-P7-rule of the service baseline |
| BR9 | No business value in code and no personal data in the ledger, the events, the logs or the tests: the actor is a user reference and the decided time is a timestamp | Template and Rules §R7.2 s17; RWB-E1-054 section 17 |
| BR10 | The ledger is `rwb_decision`'s: the review item and the document are read through the P5 contract and are never stored as rows of this schema beyond their identifiers | DP-01; DP-11 |

Where each rule lives in the target: BR1, BR4 and BR5 in `DecisionChainAppender`, the `processed_event` inbox and the append-only grant; BR2 and BR9 in the validator and the record shape; BR3 in `ReviewRecordValidator` and the P5 contract; BR6 in the record shape of DP-03; BR7 in the library of the acting service, which this story consumes and never replaces; BR8 in the reference-data client; BR10 in the schema boundary of `rwb_decision`.

### 9. State transitions

This story moves no case status and writes no value of LOV-CASE-STATUS, and it changes no review status and no document field. It moves the delivery of an envelope and appends an immutable entry.

| Object | From | Event | Condition | To |
|---|---|---|---|---|
| Envelope delivery | RECEIVED | The attributes and the record fields validate | The fields are present and the code is in LOV-DECISION | VALIDATED |
| Envelope delivery | VALIDATED | The P5 item read agrees | The item exists and its outcome matches the record | APPENDED |
| Envelope delivery | VALIDATED | A refusal holds | Item not found; outcome mismatch; code outside the list | EXCEPTION (reason, owner RW-PLATADM) |
| Envelope delivery | VALIDATED | The P5 answer times out or the store fails | Retries remain | RETRY |
| Envelope delivery | RETRY | Four attempts in all are spent | No answer | DEAD LETTER (`.dlt`, owner RW-PLATADM) |
| Envelope delivery | DEAD LETTER or EXCEPTION | A replay after the cause is cleared | The dedupe key is new | APPENDED |
| decision_log_entry | — | An append | The chain link is written in the same transaction | APPENDED, immutable |
| decision_log_entry | APPENDED | An update or a delete | — | refused, unchanged |

The delivery states are the consumer's own and are held in `processed_event` and the topic offsets; they are not a business state machine and add no list of values to the reference data.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The rwb-decision service identity (the rwb-decision login, DP-02) | Consumes the topic, reads the review item and the document through the P5 contract, appends the entry and writes the exception and incident records |
| The decision-record library identity of the acting service | Writes the local record of the review action and its outbox row in the actor's transaction; this service neither writes it nor repeats it |
| SY-DECLOG, decision log writer (service identity) | Owns the append and the chain; the legacy role is carried as the service identity of DP-03 |
| RW-AUDIT, internal audit | Reads the entries through the two decision-log reads of RWB-P7-E2005-APP (Decision log R, TSD P7 v2 T6.1); reads no topic and appends nothing |
| RW-COE, center of excellence analyst | Reads the entries of the review decisions for the model evaluations and the quality measures (Decision log R) |
| RW-PLATADM, platform administrator | Owns the exception queue and the `.dlt` topic; replays an envelope once the cause is cleared |
| Compliance and the risk and model risk officer | Receives the incident of a missing or refused record (NFR-035, NFR-078) |
| Every RW- role of TSD P7 v2 T6.1 | Holds Decision log R and no append; no role in the source documents holds a ledger write |

Every role in this table is a role code held as data in rwb-access (P4) and asked through the authorise contract with the guard library where a user calls a read of this service's ledger; the ingest itself is a service identity and needs no user answer. The per-service login name is Not specified in the source documents (GAP-2456; ASM-4083), so the story names it "the rwb-decision login (DP-02)" until it is allocated.

### 11. Data

| BR Field ID | Entity in rwb_decision | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id | Write (the case of the item where there is one) |
| DF-DEC-003 | decision_log_entry | decision_code | Write (from LOV-DECISION in force) |
| DF-DEC-004, DF-DEC-005 | decision_log_entry | rule_id, rule_version | Write (empty where no rule decided) |
| DF-DEC-006, DF-DEC-007 | decision_log_entry | model_version, agent_version | Write (empty where no model or agent decided) |
| DF-DEC-008 | decision_log_entry | inputs_ref | Write (the review item ID) |
| DF-DEC-009, DF-DEC-012, DF-DEC-014, DF-DEC-015 | decision_log_entry | recommendation, final_call, actions, outcome | Write (the review facts of ASM-4080) |
| DF-DEC-010, DF-DEC-011 | decision_log_entry | approver_user_id, approval_level | Write (the reviewer where a person decided; empty otherwise) |
| DF-DEC-016 | decision_log_entry | decided_at | Write (from the envelope) |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | decision_log_entry | prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Write (on a correcting entry only) |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write |
| Not specified in the source documents (DOR-RWB-P7-E1054-APP-7) | decision_log_entry | created_at, created_by, version | Write (append only; no update) |
| — | processed_event, idempotency_key | dedupe and repeat count of R-UNI-40 | Write (DP-09 library tables) |
| DF-DOC-008 | document | review_status | Read, through the P5 contract, never stored |
| DF-DOC-081, DF-DOC-084 | document_intake | review_outcome, discard_reason | Read, through the P5 contract, never stored |

Field IDs are those in the Logical Data Model and Data Dictionary. Nothing of the review item is copied into `rwb_decision` beyond the identifiers and the codes that the record carries, and the field names inside `actions` and `outcome` are a convention of the contract, not columns (GAP-2456; ASM-4080). The ledger holds no OCR text, no document body and no personal datum. The CloudEvents attributes ce_id, ce_specversion, ce_type, ce_source and the other envelope attributes of section 4 are transport attributes of the CloudEvents standard, not fields of the Logical Data Model or Data Classification v5; ce_id is held only as the dedupe key of processed_event.

### 12. Contract

#### 12.1 REST operations provided

None. The Ownership Map gives P7 the two decision-log reads under `/api/recovery/decision/v1` and no append operation; those reads belong to the audit query story RWB-P7-E2005-APP, and this story declares nothing on them. The write path of the ledger is the consumer of section 12.4 and the service-local `DecisionLogStore.append` of RWB-P7-E1008-APP. A REST append is absent from the Ownership Map and is therefore not invented here (DP-01, DP-13).

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | `/api/recovery/document/v1/intake-items/{intakeItemId}` | rwb-document (P5) | The review item: it exists, its review reason, its review outcome and its version, checked against the record before the append | One hop, 2 s (DP-11) |
| GET | `/api/recovery/document/v1/documents/{documentId}` | rwb-document (P5) | The `review_status` of the stored document the record names, checked against the `actions` of the record | One hop, 2 s (DP-11) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | rwb-case (P3) | LOV-DECISION and the outcome list in force, referred to and never copied into code | One hop, 2 s (DP-07) |

The first two rows are the review contract of RWB-P5-E1054-CON, the recorded contract dependency. The third is the reference-data contract of DP-07 (RWB-P3-E1043-CON through RWB-PLT-E1043-CON) and is carried in the pattern table of section 13 rather than in the metadata row. No other service is called at run time.

#### 12.3 Events published

None. The service topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1` (DP-14) carries `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` — EV-08, EV-09 and EV-30 — and every one of them belongs to the approval and rule-registry stories of this service. An append seals an entry and publishes nothing; the sealed-entry announcement on `rwb.decision-record.v1` is the store story's (RWB-P7-E1008-APP).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Handler |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` (shared topic of DP-03), with its retry topic and `.dlt` | P7 ledger library of RWB-PLT-E1027-CON; published here by `rwb-document` (the DOCATT and review-completion records) | `DecisionRecordIngestListener`: validate, dedupe on `ce_id` and `idempotencyKey`, `ReviewRecordValidator`, `DecisionChainAppender` |

The envelope is CloudEvents 1.0 in binary mode with `ce_specversion` 1.0, `ce_type`, `ce_source`, `ce_subject` (the case ID where there is one, the entry id where there is not), `ce_id`, `ce_time` and the trace header, keyed by the case or the entry id. The type is `rwb.decision.DecisionRecorded.v1` as fixed by Kafka Topic and Event Catalog v1 (EV-08), which takes precedence over the platform library baseline; the topic stays `rwb.decision-record.v1`.

#### 12.5 Workflows and activities

None. The ingest is event driven and has no workflow, no activity and no timer; the append is the store's own transaction, so a redelivery and a replay are absorbed by the inbox and the chain rather than by a retry loop in workflow code.

#### 12.6 Schedules

None. JOB-13 of the legacy design is continuous Kafka ingest in the target and JOB-14 at 02:00 is the chain check of RWB-P7-E1008-APP; JOB-20 belongs to that story as well. This story adds no Temporal Schedule and moves no clock.

#### 12.7 Tables owned

| Table | Schema | Owner (ownership map) | This story |
|---|---|---|---|
| decision_log_entry | rwb_decision | P7 | Appends the review entry with its chain link, its codes, its actor and its dedupe key |
| processed_event | PLT library, created in `rwb_decision` | PLT | The inbox of the consumer: one row per `ce_id` |
| idempotency_key | PLT library, created in `rwb_decision` | PLT | The stored `idempotencyKey` of the record and its repeat count |
| outbox_event | PLT library, created in `rwb_decision` | PLT | Not written here; named because the table exists in the schema |

`approval` is P7's but belongs to RWB-P7-E2013-APP; `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are P7's but belong to RWB-P7-E1073-CON and its app story. The document hub's `document`, `document_field`, `document_intake`, `document_text`, `document_type` and `document_hub_parameter` are P5's in `rwb_document` and are never read; the reference rows are P3's in `rwb_case` and are reached over the contract only. No statement in this story names a table in another schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-document WireMock | The P5 review contract of RWB-P5-E1054-CON | `GET /intake-items/{intakeItemId}` with an item in each review outcome and a 404 MSG-P4-003; `GET /documents/{documentId}` with `review_status` PENDING, CONFIRMED and CORRECTED, a 404 and a 2 s timeout |
| rwb-case reference-data fake | The lists row of DP-07 | LOV-DECISION with DOCATT and without D99; the outcome list with ATTACHED, DISCARDED, CONFIRMED and CORRECTED |
| DecisionRecorded topic fixture | The shared topic of RWB-PLT-E1027-CON | One valid DOCATT envelope; one repeated `ce_id`; one envelope with no `inputsRef`; one with an unknown code; one whose final call disagrees with the item; one with no case |
| Chain fixture | The chain rule of BR5 | The genesis hash of 64 zeros; a second entry linked to the first; the recomputed digests; a refused update and a refused delete |
| Store fake | `DecisionLogStore.append` of RWB-P7-E1008-APP | An append that answers the entry reference; an append refused because the store is unavailable, raising `DecisionLogUnavailableException` with MSG-P7-003 |
| Outbox and inbox fake | `OutboxWriter` and `ProcessedEventStore` of RWB-PLT-TE006-CON | The row present after a commit and absent after a rollback; the repeat count of a duplicated `ce_id` |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 3 consumed | The review item and the document read on RWB-P5-E1054-CON and the two lists on DP-07; one hop, 2 s |
| Kafka | 1 consumed, 0 published | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` with the retry topic and `.dlt` |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | No file is read or written; the document body never reaches this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `reviewrecord`, Java package `th.co.scb.ace.workbench.recovery.decision.reviewrecord`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency: RWB-P5-E1054-CON) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The dependency-added column records the platform contract stories this story builds on; they arrive as platform CON work, so Depends on (build) stays None and the story is ready on Day 1. DP-19 adds nothing at run time here because this story serves no screen: the review queue screen of legacy SCR-31 is P5's and the decision log screen SCR-38 is RWB-P7-E2005-APP's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionRecordIngestListener | Consumer | Reads `rwb.decision-record.v1`, validates the envelope, dedupes in `processed_event`, drives the validator and the appender, and routes the refusals |
| EnvelopeValidator | Service | The CloudEvents attributes, the required record fields and the decision code against LOV-DECISION |
| ReviewRecordValidator | Service | Reads the review item and the document through the P5 contract and compares the outcome and the review status with the record |
| DecisionChainAppender | Service | Takes the next `chain_seq`, computes `prev_hash` and `entry_hash`, appends the entry and writes the inbox row in one transaction |
| ReferenceDataClient | Client | LOV-DECISION and the outcome list in force (DP-07) |
| ExceptionRouter | Service | Writes the exception-queue row with its reason and owner, raises incident `LEDGER_WRITE_FAILED`, and routes to the retry topic or `.dlt` |

**Database and migrations**

- Migration `V1054_1__review_decisions.sql`, on the per-service Flyway sequence after the V0001 baseline (DP-15), adds no table and no column: it adds `ix_declog_inputs ON decision_log_entry (inputs_ref)` for the review correlation and `ix_declog_decision_time ON decision_log_entry (decision_code, decided_at)` for the decision filter of the audit reads. The chain columns and the append-only grant are RWB-P7-E1008-APP's and are not redefined.
- No review column is added: the review facts sit in `actions` and `outcome`, whose key names are a contract convention (GAP-2456; ASM-4080).

**Configuration.** The consumer group `rwb-decision-ledger`, the maximum of four delivery attempts, the retry topic and the `.dlt` topic of the naming library (DP-14), the exception-queue owner `RW-PLATADM`, the incident name `LEDGER_WRITE_FAILED`, the genesis hash of 64 zeros and the 5-minute collection target of Architecture v5 slide 28. Everything but the target, the owner and the incident name is the platform standard of DP-09 and the store's own configuration.

**Build steps**

1. Write the migration and the two indexes; assert that no review column exists and that the append-only grant is in force.
2. Build `EnvelopeValidator` and `ReferenceDataClient` over the reference-data fake and the topic fixture; tests for AC5.
3. Build `DecisionRecordIngestListener` with the inbox dedupe and the repeat count; tests for AC2 and AC9.
4. Build `ReviewRecordValidator` over the P5 fake: item found, item absent, outcome match, outcome mismatch, document status match, and the 2 s timeout; tests for AC1, AC3, AC4, AC6 and AC8.
5. Build `DecisionChainAppender` with the genesis hash, the link to the entry before, the correction through `corrects_entry_id` and the store refusal; tests for AC1, AC3, AC7 and the store-unavailable path.
6. Build `ExceptionRouter`: the reason, the owner, the incident and the `.dlt` route, and the replay path from `.dlt` and from the exception queue; tests for AC4, AC6 and AC8.
7. Run the full ingest against the topic fixture with the P5 fake in place, so the story builds before the document hub publishes anything.

**Feature switch.** None is added. Skipping a decision record breaks NFR-033, NFR-034 and NFR-035, so the ingest has no off state; the store's own flag `rwb.decision.log-store` of RWB-P7-E1008-APP pauses collection and is not this story's.

**Done when.** The tests in section 16 pass, every review outcome of the fixture has exactly one chained entry, a repeated delivery adds no entry and no chain position, no entry exists for an item that does not exist or an outcome the item does not carry, the ledger holds no field value and no OCR text, and the contract tests of RWB-P5-E1054-CON stay green.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-009 | A record is refused at validation: a field missing, a decision code outside LOV-DECISION, or an item or an outcome that does not answer | The decision record was refused: {field} is missing or not valid. |
| MSG-P7-003 | The ledger store is unavailable at the append | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The review item or the document does not answer inside the budget, or answers 503 | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-003 | The review item the record names is not returned by the P5 contract | This case is not in your scope. |

The checks of section 4 raise these four; the refusals of X2, X3 and X6 to X9 also carry a reason value of the exception queue — "review item not found", "outcome mismatch", "no answer in the budget" and "store unavailable" — which is data of the platform standard and not a message ID. MSG-P7-003 and MSG-P4-003 keep the wording of the P7 module of the source documents and the legacy story, and MSG-P7-009 takes the wording of the Error and Message Standard v4; MSG-GEN-006 is the shared platform message. Thai text for each message follows decision DL10.

### 15. Screens and states

This story serves no screen of its own. The review queue screen SCR-31 and its Loading, list, reviewed and empty states are RWB-P5-E1054-APP's, reached through the gateway-bff composite route (DP-19); the decision log screen SCR-38 is RWB-P7-E2005-APP's. What this story adds is what those screens can then show.

| Screen | State | What the user sees and does |
|---|---|---|
| SCR-31 Document review queue | Reviewed | The item has left the queue and its review decision has one chained entry, so the case record can point at it |
| SCR-31 Document review queue | Loading | Not specified in the source documents (CG-ALL-7019) |
| SCR-31 Document review queue | Empty | Not specified in the source documents (CG-ALL-7019) |
| SCR-31 Document review queue | Error | Not specified in the source documents (CG-ALL-7019) |
| SCR-31 Document review queue | No access | Not specified in the source documents (CG-ALL-7019) |
| SCR-38 Decision log query | List | The review entries appear with their decision code, actor, decided time and `chainVerified` on each row, answered by RWB-P7-E2005-APP from this service's ledger |
| SCR-38 Decision log query | Chain warning | An entry that does not verify is returned flagged and one incident is raised per entry; nothing is hidden and nothing is corrected |
| SCR-38 Decision log query | Loading | Not specified in the source documents (CG-ALL-7020) |
| SCR-38 Decision log query | Empty | Not specified in the source documents (CG-ALL-7020) |
| SCR-38 Decision log query | Error | Not specified in the source documents (CG-ALL-7020) |
| SCR-38 Decision log query | No access | Not specified in the source documents (CG-ALL-7020) |
| Operator console | Exception queue | The refused or dead-lettered envelope with its reason and owner RW-PLATADM, and the replay action once the cause is cleared |

No layout, no field-level masking and no screen text is fixed here; the entries carry identifiers and codes only, so no screen of this story shows a field value, an OCR page or a personal datum.

### 16. Test cases

The nineteen legacy test case ids of RWB-E1-054 are kept in their legacy order (18, 19, then 01 to 17). Legacy levels map System to End to end, Access to Component and Resilience to NFR. A legacy test whose screen behaviour moved to rwb-document is re-pointed at the record-side fact it now proves: a committed review action appends exactly one chained entry, a refused review action appends none, and a repeated delivery adds no chain position.

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-054-18 | AC9, BR9 | Component | RW-TEAMMGR user (Documents R) is refused the resolve by the document hub and the P5 fake answers 403 with MSG-P4-002; no envelope is produced and no entry exists |
| TC-E1-054-19 | AC4, AC8, BR7 | NFR | The record write is refused on the acting side with MSG-P7-003 and the item read then times out; no entry, no chain position, incident LEDGER_WRITE_FAILED, replay appends once |
| TC-E1-054-01 | AC1, AC3, BR2 | End to end | Item IN-0101 classified COURT_NOTICE 0.6200 and DEMAND_LETTER 0.2100 with reason LOW_CONFIDENCE; the attach loops back to one entry with its code and no candidate confidence copied |
| TC-E1-054-02 | AC1, AC3, BR6 | End to end | Hearing date corrected on the document side for synthetic case RW-2026-000201; one chained entry naming the actor, the outcome and the decided time |
| TC-E1-054-03 | AC3, BR2 | End to end | Document DOC-0103 with one field in review; the completion record is appended once with the review status and the field count only |
| TC-E1-054-04 | AC4, BR3 | End to end | Empty correction refused by the document hub; no record, no envelope and no entry |
| TC-E1-054-05 | AC5, BR8 | End to end | Type PAYSLIP refused by the P5 answer with MSG-P5-006 and a decision code outside LOV-DECISION refused here with MSG-P7-009 |
| TC-E1-054-06 | AC4, BR3 | End to end | Date 2569-12-16 refused by the P5 answer; no record and no entry, chain unchanged |
| TC-E1-054-07 | AC4, BR3 | End to end | Two fields in review and one confirmed; the attach is refused by the P5 answer and no entry is appended |
| TC-E1-054-08 | AC4, BR3 | End to end | Reason CASE_CLOSED with candidate case RW-2026-000150 closed; no record and no entry |
| TC-E1-054-09 | AC2, BR1 | End to end | Two sessions on one item version 3 and 4; the second action gives no second entry and the chain keeps one position |
| TC-E1-054-10 | AC3, BR2 | End to end | Demand letter changed to guarantor notice; the completion record carries the outcome and the count, never the field values |
| TC-E1-054-11 | AC1, AC2, BR1 | End to end | Same file hash already on the case; the linked document is recorded once and a repeated envelope adds no entry |
| TC-E1-054-12 | AC3, BR2, BR9 | End to end | Unreadable item discarded with reason "Blank page from the branch scanner"; the entry carries the outcome DISCARDED and the reason code, not the free text |
| TC-E1-054-13 | AC4, BR3 | End to end | Discard with an empty reason refused by the document hub; no record and no entry |
| TC-E1-054-14 | AC4, BR1 | End to end | Five review items across teams LIT-BKK and HP-NE, three resolved and two still queued; three entries exist and the queued two have none |
| TC-E1-054-15 | AC4 | End to end | No review item for team LIT-BKK; no envelope, no entry and the chain unchanged |
| TC-E1-054-16 | AC4, BR10 | Component | Document of team HP-NE read by the LIT-BKK officer is 404 with MSG-P4-003 on the P5 fake; the record naming it is refused to the exception queue |
| TC-E1-054-17 | AC2, BR1 | End to end | The same completion sent twice; one entry, repeated true, repeat count one, no second chain position |
| TC-E1-054-20 | AC6, BR3 | End to end | Item IN-0106 returns DISCARDED and the envelope with final call ATTACHED is refused with reason "outcome mismatch"; it is in the exception queue, no entry is appended and the ledger still verifies |
| TC-E1-054-21 | AC7, BR4 | Component | Entries at chain_seq 1 and 2 of IN-0101 and IN-0103; an update and a delete of chain_seq 1 are refused by the append-only grant and the store; a correcting envelope naming chain_seq 1 appends chain_seq 3 and leaves chain_seq 1 unchanged |
| TC-E1-054-22 | Boundary of the tables of section 12.7 (ASM-3438) | Not specified in the source documents (DOR-RWB-P7-E1054-APP-12) | Not specified in the source documents (DOR-RWB-P7-E1054-APP-12) |
| TC-E1-054-23 | AC10, BR5 | End to end | Entries at chain_seq 1, 2 and 3 as in AC1, AC3 and AC7; the chain verifies, and a copy of the ledger with one prev_hash altered fails verification |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision codes, the outcome values and the reasons are reference rows read through DP-07, and the retry count, the exception owner and the incident name are the platform standard of DP-09.
- No field value, no OCR text, no document body and no personal datum in `rwb_decision`, in the topic or in the logs. The entry carries identifiers, codes, an actor reference and a timestamp; test data uses synthetic items, documents, cases and users only.
- No read of another service's table (DP-01): the review item and the document come through the P5 contract, the lists through the reference-data contract, and no foreign schema appears in a statement.
- One hop and a 2 s timeout on every consumed call, with the fake in place from Day 1, so a P5 outage sends the envelope to the retry and `.dlt` path instead of holding a topic partition (DP-11).
- The ledger is append only: no update, no delete, no REST write path and no writer other than the consumer; a correction is a new entry that names the entry it corrects (DP-01, DP-03).
- Every append commits with its inbox row in one transaction, so a redelivery and a replay add no entry and consume no chain position (DP-09).
- The record is never written on behalf of another service: the acting service writes its own record in its own transaction, and this service only collects it (BR7; DP-03).
- Nothing is removed silently: a refused or dead-lettered record is kept with its reason and its owner until it is replayed, and a discarded review item keeps its reason in the document hub and in its entry (REQ-DCM-019).
- Personal data rule: no field classed as personal data is carried in rwb_decision, the topic, the logs or the tests; the actor is a user reference and the decided time a timestamp.
- Open decision DL10 stays open until its owner closes it; it rests on the assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-005 | Inbound documents classified with a confidence; below the threshold to a review queue, and every review decision recorded | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-01 to TC-E1-054-17, TC-E1-054-20, TC-E1-054-21, TC-E1-054-22 |
| REQ-DCM-019 | A discarded document is never removed silently; the reason and the person are kept with the file and with the record | Business Requirements Program, section 5.5; Epic 1, section 3.5 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-12, TC-E1-054-13 |
| D-RCV-60 | Split of RWB-E1-054: rwb-document keeps the queue, the screen, the OCR text, the corrections, the type change, the attach and the labeled set; rwb-case the task and its scope; rwb-access the rights and the masking; rwb-decision the record of every review decision in the chained ledger | Decision log, D-RCV-60 | FEAT-DCM-10, FEAT-DCM-11 | 13 Manage documents and correspondence | R-UNI-39, R-UNI-40 | TC-E1-054-18, TC-E1-054-19 |

The feature identifiers are those of the legacy story; FEAT-DCM-11 covers the check of a low-confidence extraction, which this service records as the outcome of the review decision. The ledger requirements the record serves — REQ-DRI-003, REQ-DRI-004, NFR-033, NFR-034 and NFR-035 — are traced by the store and audit stories of this service (RWB-P7-E1008-APP, RWB-P7-E2005-APP) and are named here in sections 2 and 8, not claimed as this story's own.

### 19. Out of scope

- The review queue, its rows, its ordering, the scope rule, the review task, the case timeline and the case-side review state: RWB-P3-E1054-APP.
- The rights, the scope answer and the masked markers of a review item or a document: RWB-P4-E1054-APP.
- The queue endpoint, the item read and content, the resolve actions, the field confirm and correct, the type change and the re-run of extraction, the attach and the duplicate link, the discard, the review completion and the labeled set: RWB-P5-E1054-APP.
- Setting the review reasons: OCR (legacy RWB-E1-049), classification (legacy RWB-E1-050), extraction (legacy RWB-E1-053) and matching (legacy RWB-E1-032), all in rwb-document.
- The model evaluations that read the labeled examples (legacy RWB-E1-060, rwb-agent P10).
- Writing the local decision record in the service that takes the action: the platform library RWB-PLT-E1027-CON and the acting story; this story collects what they publish.
- The ledger store, the canonical form, the chain verifier, the WORM seal, JOB-13's continuous ingest, JOB-14's 02:00 chain check and the missing-record alert: RWB-P7-E1008-APP.
- The audit query, the filters, the export and the access records of a query: RWB-P7-E2005-APP.
- The approval items of the service and the rule packages: RWB-P7-E2013-APP and RWB-P7-E1073-CON.
