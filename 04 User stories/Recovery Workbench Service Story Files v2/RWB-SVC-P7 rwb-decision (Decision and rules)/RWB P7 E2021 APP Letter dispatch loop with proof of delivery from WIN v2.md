# RWB-P7-E2021-APP Letter dispatch loop with proof of delivery from WIN

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2021-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P7-AC |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2021-CON, RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-P3-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-OCC-003, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-P7-E2021-APP-16) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-021 for rwb-decision; the D7.1 decision record of the letter dispatch loop in the central decision ledger, and its two reads. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2021-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 40 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **conduct and QA officer (RW-CONDUCT), a litigation officer (RW-LITOFF) and an internal auditor (RW-AUDIT)**, I want **every decision of the letter dispatch loop that a rule decides — the conduct-check hold under R-LIT-04 or R-LIT-05, and the delivery result under R-LIT-07, R-LIT-08 or R-LIT-09 — appended once as a D7.1 entry of the central decision ledger of `rwb-decision`, carrying the notice reference, the notice type, the case reference, the rule id with its rule version, the final call HELD, DELIVERED or UNSERVED, the hold reason or the delivery status and the notice period start date where one applies, and carrying no WIN payload, no address and no customer value**, so that **a held, a served or an unserved letter can be explained years later from the rule and the version that decided it, and a record that cannot be appended stops the decision instead of disappearing from the history**.

Inside `rwb-decision` this is the decision-record slice of legacy RWB-E2-021:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record path of DP-03.
- One deliverable and nothing else: the appender of the D7.1 dispatch record and the two decision-log reads. The loop's decisions are taken by the service that owns the notice; this service appends each record once, chained and append only, and serves `GET /decision-log/{entryId}` for one entry and `GET /decision-log` for the entries of a case in a date range.
- What stays with `rwb-comms` (P6, RWB-P6-E2021-CON, RWB-P6-E2021-APP and RWB-P6-E2021-OPS): the notice, its states, the conduct check of the four gates, the template check and the notice hold, the dispatch selection, the INT-14 WIN dispatch file, the INT-15 proof capture, the result-code map, the dispatch messages and the JOB-10 Schedule at 16:00. None of it is rebuilt here.
- What stays with `rwb-case` (P3): the legal hold flag of the case, the case state, the queue transfer with reason NOTICE_UNSERVED and the NOTICE_PERIOD timer started from the call-back date. What stays with `rwb-source-data` (P1, DP-18) is the interaction ledger entry, and with `rwb-integration` (P2) the WIN interface configuration, the file window and the file runs. This story writes none of them.
- The record and the decision are one pair under DP-03: the owning service writes the record through the decision-record path inside the transaction of the decision it records, and this service appends it to the ledger in one idempotent transaction of its own, so a record with no decision behind it is never appended and a decision whose record cannot be appended does not proceed (BR13).
- The service appends and exposes; it selects no notice, runs no conduct check, writes no hold reason, dispatches nothing, captures no proof, moves no case and starts no timer (BR9). The database login is the per-service login of DP-02, and the story refers to "the rwb-decision login (DP-02)".

The legacy behaviour carried into the decision service is unchanged in meaning: one entry for every decision of the loop and no exception, the rule id and the rule version on the entry, the hold reason of a held letter and the result of an unserved letter on the entry, a delivery that starts the notice period and a proof window that does not, a record that can never be altered, and no held or unserved outcome standing without its record (legacy RWB-E2-021 AC3, AC6, AC7, AC8, AC9 and BR2, BR5, BR6, BR7, BR8, BR9).

Which fields of the record this service consumes, and where the notice reference, the hold reason or the delivery status and the notice period start date sit in the entry, are Not specified in the source documents (GAP-1276; ASM-2246). The rule version label carried by the letter rules is Not specified in the source documents (GAP-1276; ASM-2247), and so is the enforcement of the right and scope behind the two reads (GAP-1276; ASM-2249).

### 2. Business rationale

A notice period counted from the print date can be challenged, and a letter sent while a contact stop or a legal hold is in force is a conduct breach. The WIN dispatch loop proves the serving of the letter: a conduct check before the file, a barcode from the acknowledgement, a call-back date from the proof, and an unserved outcome when the proof never comes. That loop is only defensible if each decision inside it is recorded with the rule and the version that made it: which rule held the letter and why, which rule served it and from which date, which rule closed it as unserved and on which result. The monolith wrote that record with the notice row in one process and one schema, so the two could not drift apart. In the target the notice is `rwb-comms`'s and the evidence of every decision is collected in `rwb-decision` (Architecture v5 slides 14, 27, 28 and 41), so the record of the loop has to be appended there, chained, unchangeable, and readable by the officer who follows the letter and by the auditor who later asks why the case was transferred.

Under Architecture v5 the central decision ledger, the rule registry and the approvals are `rwb-decision` (slides 14 and 41); every service writes its decision record through the local library in the same transaction as the change it records and publishes `DecisionRecorded` on `rwb.decision-record.v1` (slide 20, "every service"; slide 42, event 08); `rwb-decision` collects the records into the ledger within 5 minutes and seals it daily in write-once storage (slide 28); and the ledger is read through the decision-log operations (slide 14). The realignment changes the mechanism, not the business rule:

1. The in-process `DecisionLogApi.write` call of the monolith becomes the decision-record path of DP-03: the record is written where the decision commits and is appended here on the shared topic `rwb.decision-record.v1`, with the append-only rule and the hash chain the FSD already carries (FEAT-DRI-01, FEAT-DRI-03).
2. The entry is not a copy of the notice and not a copy of the file record: it names the notice, the notice type, the case, the rule and version, the final call, the hold reason or the delivery status and the notice period start date, and it names no address, no barcode payload, no WIN field and no customer value (BR5, BR13).
3. The final call and the five rule ids are data rows and registry rows, never literals in the code (BR8); the conduct check, the template check, the hold, the dispatch file, the proof read, the timer and the ledger entry stay with their owners, and this story reads none of their tables (DP-01, DP-18).
4. The one decision-log read of the monolith becomes two operations on the service's own base (DP-13): the entries of a case in a date range, and one entry with its rule version and its chain fields.
5. The data-lake copy of the log is retired with the data lake (DP-17); the ingest of `rwb.decision-record.v1` is continuous Kafka (JOB-13) and the daily chain check JOB-14 at 02:00 covers these entries like any other.
6. The record is append only and hash chained, so a decision that fails leaves no entry, a repeated record leaves one entry, and a break in the chain is a reportable event rather than a silent edit.

This story meets REQ-OCC-003, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010 on the record side: it proves which rule held a letter and why, that the notice period starts only from a proof, and that an unserved letter cannot reach the case without its entry. It carries control CTL-15 (the notice period starts from proof of delivery), CTL-16 (a contact stop blocks the contact) and the principle that no action proceeds unlogged (R-UNI-39).

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P6-E2021-CON | The published contract of the loop (P6): the declaration of `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` with the record reference, the decision code, the rule id, the rule version, the final call and the decision time; the closed vocabulary of the hold reasons CONTACT_STOP_X1, LEGAL_HOLD and TEMPLATE_WITHDRAWN with the rules R-LIT-05, R-UNI-20 and R-LIT-04; the unserved outcomes UNDELIVERABLE, REFUSED and PENDING with R-LIT-09 and R-LIT-08; and the contract fakes. Which further fields of the record this service consumes is Not specified in the source documents (GAP-1276; ASM-2246) |
| RWB-PLT-E1027-CON | The decision-record path and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule and the idempotency key the record carries |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): the inbox dedupe of a repeated record and the CloudEvents 1.0 envelope of the fact |
| RWB-PLT-E1044-CON | The per-service Flyway sequence of `rwb_decision` (DP-15), in which this story adds one index step and no table |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which SCR-38 Decision log query and the auditor's view reach the two operations |
| The baselines of this service | `decision_log_entry` with the columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only` (a database trigger of the store baseline, not a field or entity of LDM v9 or Data Classification v5), the missing grant for UPDATE and DELETE, the unique key on the idempotency key and the chain check JOB-14 at 02:00; and the rule registry `rule_package`, `rule_package_version` and `rule_row` read by rule id and version. Both are the service's own earlier work and are in no H row of this story (GAP-1277; ASM-2248) |
| The parameters and the edge answer | The page-size bound of the search and the completeness target of the ingest, read at the version in force with no default in code (GAP-1276; ASM-2251); and the capability area, the right and the scope of each operation, declared on the operations and enforced at gateway-bff, which asks `rwb-access` (GAP-1276; ASM-2249) |

Business preconditions carried from RWB-E2-021:

- Notice `N-0101` for case `RC-2026-000321` in state Approved, notice type `DEMAND`, template `DEMAND-SSME` "TH" version 1 approved; notices `N-0102` for case `RC-2026-000654` and `N-0103` for case `RC-2026-000655` in state Sent, sent on 2026-12-15 and 2026-12-16, no proof returned.
- Barcode `RR223344556TH`, call-back date `18122026`, delivered date 2026-12-18, business dates 2026-12-14, 2026-12-15, 2026-12-21 and 2026-12-22.
- The hold reasons are `CONTACT_STOP_X1`, `LEGAL_HOLD` and `TEMPLATE_WITHDRAWN`; the delivery statuses of an unserved letter are `UNDELIVERABLE` and `PENDING`; the final calls are `HELD`, `DELIVERED` and `UNSERVED`.
- The record under test is produced by the contract fake of RWB-P6-E2021-CON for the held, delivered, undeliverable, proof-window and legal-hold paths.
- No build dependency. Day 1: the story builds against RWB-P6-E2021-CON and its fakes, and the platform contracts of wave 0 and 1 are in place.
- Contract version: the story builds against RWB-P6-E2021-CON at its `/v1` path; the fixed version label is Not specified in the source documents (DOR-RWB-P7-E2021-APP-23).

### 4. Flow

1. `rwb-comms` runs the JOB-10 letter loop of the business date on its own Temporal Schedule: the proof-window step first, then the conduct check of each eligible notice. The Schedule is `rwb-comms`'s and this story registers none (12.6).
2. A notice fails the check, or a proof result closes it: the owning service takes the decision with the rule that decided it, and in the same transaction writes its notice change, its outbox row and, through the decision-record path of DP-03, the D7.1 record with the final call, the rule id and version, the notice reference, the notice type, the case reference and the hold reason or the delivery status (RWB-P6-E2021-APP; Architecture v5 slide 28).
3. The record path publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID, with the record reference, the decision code, the rule id, the rule version, the final call and the decision time (DP-09; slide 42, event 08).
4. `rwb-decision` `DispatchRecordListener` reads the fact into the inbox of DP-09, deduplicates by event ID and by the record reference (R-UNI-40), keeps the facts whose decision code is D7.1 and whose final call is HELD, DELIVERED or UNSERVED, and passes them to `DecisionLogAppendService`; every other decision code is the ledger baseline's general ingest.
5. `DecisionLogAppendService` checks the entry: the decision code D7.1 is a value of LOV-DECISION at the version in force; the final call is one of the three; the notice reference, the notice type and the case reference are present; the rule id carries a version, and the pair exists in the rule registry at the version in force; a held record carries a hold reason of the closed vocabulary and a delivery record carries a delivery status. A record that fails the check is refused with MSG-P7-009 naming the missing field and nothing is written (BR8, BR11).
6. `DecisionLogAppendService`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash` (64 zeros for the first), computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with `decided_at` from the record and the notice period start date where the record carries one, and writes the inbox row and the idempotency row of the record reference. A failed append changes nothing: no entry, no chain position and no inbox row (BR3, BR13).
7. A repeated fact with the same record reference returns the first entry's ID, adds one to the repeat count for R-UNI-40 and appends nothing (BR7). A held letter and its later delivery are two decisions and give two entries, chained in decision order (BR1).
8. A decision whose record cannot be appended does not proceed: the record path answers the owning service with MSG-P7-003, the notice stays Approved and is not written to the WIN file, no chain position is used and an incident is raised under R-UNI-39 (BR13).
9. A litigation officer, a conduct and QA officer or an internal audit reader reads one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`, and the entries of a case in a date range with `GET /api/recovery/decision/v1/decision-log?caseId=…&decision=D7.1&from=…&to=…`, one page at a time in `decidedAt` order with the total count of the range (BR10). A caller without the Decision log right is refused with 403 and MSG-P4-002; a case outside the caller's scope is refused with 404 and MSG-P4-003, and no entry of that case is returned.
10. Nothing in this story moves a notice, a case, a timer or a record on the WIN side: the entry is written beside the decision and the readers of `rwb-comms`, `rwb-case` and the auditor's screen keep their own state (BR9). The daily chain check JOB-14 and the daily seal are the baseline's, not rebuilt here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A held record carries a hold reason outside the closed vocabulary, or a delivery record carries no delivery status | The append is refused, nothing is written and no chain position is used | MSG-P7-009 | AC2, AC3, AC4, AC5 |
| X2 | The record carries a rule id with no rule version, or a pair absent from the registry at the version in force | The append is refused and the fact stays on the topic for redelivery | MSG-P7-009 | AC9 |
| X3 | The decision-log store is unavailable, or the chain position cannot be taken | The decision is not recorded: the record path answers MSG-P7-003, the notice stays Approved and is not written to the WIN file, no chain position is used and an incident is raised as in R-UNI-39 | MSG-P7-003 | AC6 |
| X4 | The same record is delivered again, or replayed from the topic | One entry exists; the inbox dedupe and the record reference both hold, and the repeat is counted for R-UNI-40 | None | AC7 |
| X5 | A passing dispatch arrives with no rule behind it, or a generation record with decision code D7.1 and rule R-LIT-03 | No entry is appended for the pass: this slice appends only a hold or a delivery result, and the generation entry is another story's | None | AC1 |
| X6 | The proof window expires for one notice of the run and not for the other | One entry is appended for the expired notice and no entry for the one inside its window | None | AC3 |
| X7 | The decision code is not a value of LOV-DECISION, or is not D7.1 | The fact is left to the ledger baseline's general ingest and this story appends nothing | None | AC1 |
| X8 | The caller holds no Decision log right, or asks for a case outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; no entry is returned | MSG-P4-002, MSG-P4-003 | AC8 |
| X9 | The record carries an address, a WIN field or a customer value it should not carry | The append refuses the field at the schema check: the record path answers MSG-P7-003 and nothing is written, because an entry is not a copy of the file | MSG-P7-003 | AC2, AC8 |
| X10 | The reference list, the parameters or the rule registry cannot be read at the version in force | The append or the read is refused rather than assumed, and the fact is retried; no entry is written with an assumed code, final call or rule version | MSG-P7-003 | AC9 |

An entry is only ever appended beside the decision that caused it: the entry, its chain position, its inbox row and its idempotency row are written in one transaction, so a decision can never leave a half record and a record can never exist for a decision that was not taken (BR13).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the loop contract RWB-P6-E2021-CON, the decision-record path of DP-03, the inbox library and the fakes; no conduct check, notice state, template check, file, proof read, timer or ledger entry is rebuilt here |
| Negotiable | The decision code, the final-call set, the hold reason and delivery status vocabulary, the payload field set, the parameter names and the message ids are data, registry rows or parameters of their owners; the story fixes only the entry, the append-only rule, the chain and the two reads |
| Valuable | Every held, served and unserved letter is explained by the rule and the version that decided it, and that explanation cannot be quietly changed |
| Estimable | One listener, one appender with the chain, one query controller with two operations, one index step and one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the nine criteria in section 7 runs as one automated test against the contract fakes, with a fixed business date and a fixed chain |

### 7. Acceptance criteria

No legacy acceptance criterion is owned verbatim by this story: `acs` is empty for RWB-E2-021, and every legacy criterion of the key acts on the notice, the WIN file or the proof — the notice state, the conduct check, the written file, the returned barcode and the case transfer — which belong to RWB-P6-E2021-APP, RWB-P6-E2021-CON, RWB-P6-E2021-OPS, `rwb-case` and RWB-ITG-E2021-ITG. The twelve criteria below, AC1 to AC12, are new for the `rwb-decision` slice and test only the D7.1 record and its two reads; each keeps the legacy values of RWB-E2-021 and introduces no business value.

```gherkin
Feature: The decision record of the letter dispatch loop in rwb-decision

  Background:
    Given the environment is SIT
    Given notice "N-0101" for case "RC-2026-000321" with notice type "DEMAND" and template "DEMAND-SSME" "TH" version 1
    Given the decision code "D7.1" is a value of LOV-DECISION at the version in force
    Given the final-call list holds "HELD", "DELIVERED" and "UNSERVED"
    Given a reader with the Decision log right R in scope of case "RC-2026-000321"

  Scenario: AC1 A passing dispatch appends no entry (new, D-RCV-60)
    Given the rwb-comms contract mock returns the sent notice "N-0101" with barcode "RR223344556TH", sent date 2026-12-15 and conduct check "PASSED", and returns notice "N-0101" with consent "WITHDRAWN" on notice type "DEMAND" as a statutory notice that was sent
    When the ledger consumes rwb.decision-record.DecisionRecorded.v1 for the run of 2026-12-14
    Then no decision_log_entry is appended for notice "N-0101" on 2026-12-14, because a pass is a conduct result and not a decision of a rule
    Then no chain_seq is consumed, and the consent status, the barcode and the conduct result stay in rwb-comms and rwb-source-data

  Scenario: AC2 A delivered letter is recorded with its notice period start (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0101", case "RC-2026-000321" and notice type "DEMAND" with rule "R-LIT-07", final call "DELIVERED", delivery status "DELIVERED" and the call-back date 2026-12-18
    When the ledger consumes that record
    Then one decision_log_entry exists with decision code "D7.1", rule "R-LIT-07", the rule version in force, notice reference "N-0101", notice type "DEMAND", case reference "RC-2026-000321", final call "DELIVERED" and delivery status "DELIVERED"
    Then the entry carries the notice period start date 2026-12-18, and the notice period itself is rwb-case's
    Then the entry carries no address, no customer name, no account number and no WIN payload

  Scenario: AC3 An unserved letter is recorded with its delivery status (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0101" with rule "R-LIT-09", final call "UNSERVED", delivery status "UNDELIVERABLE" and the outcome naming MSG-P6-008, and a D7.1 record for notice "N-0102" of case "RC-2026-000654" with rule "R-LIT-08", final call "UNSERVED" and delivery status "PENDING"
    Given notice "N-0103" for case "RC-2026-000655" is inside its proof window on 2026-12-22
    When the ledger consumes the records of the runs of 2026-12-21 and 2026-12-22
    Then one entry exists for "N-0101" with final call "UNSERVED", delivery status "UNDELIVERABLE", rule "R-LIT-09" and no notice period start date, naming MSG-P6-008
    Then one entry exists for "N-0102" with rule "R-LIT-08", delivery status "PENDING" and no notice period start date, and no entry exists for "N-0103"
    Then the case transfer with reason "NOTICE_UNSERVED" is a call to rwb-case's transfer operation, and the timer that does not start is rwb-case's; both are asserted through its fake

  Scenario: AC4 A contact stop holds the letter and the hold is recorded (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0101" with rule "R-LIT-05", final call "HELD" and hold reason "CONTACT_STOP_X1"
    When the ledger consumes that record
    Then one entry exists with final call "HELD", hold reason "CONTACT_STOP_X1", rule "R-LIT-05" and the rule version in force
    Then the entry carries no notice period start date and names MSG-P6-001 in its outcome
    Then the open deviation and its contact stop stay with rwb-deviation and are not copied into the entry

  Scenario: AC5 The other two holds are recorded with their own rule (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0101" with rule "R-LIT-04", final call "HELD", hold reason "TEMPLATE_WITHDRAWN" and template "DEMAND-SSME" "TH" version 1 withdrawn on 2026-12-13, and a D7.1 record for notice "N-0101" with rule "R-UNI-20", final call "HELD" and hold reason "LEGAL_HOLD"
    When the ledger consumes both records
    Then two entries exist, each with final call "HELD", its own rule and rule version, and the hold reason "TEMPLATE_WITHDRAWN" or "LEGAL_HOLD"
    Then the entry that names "TEMPLATE_WITHDRAWN" names the template "DEMAND-SSME" with version 1 as a reference and MSG-P6-003, and the entry that names "LEGAL_HOLD" names MSG-P3-004
    Then the template version and the legal hold flag stay in rwb_comms and rwb_case, and no template body is copied

  Scenario: AC6 A record that cannot be appended stops the decision (new, D-RCV-60)
    Given the decision log store does not accept writes
    Given the rwb-comms contract mock holds the decision of notice "N-0101" open in one transaction with the decision-record path of rwb-decision
    When the decision-record path refuses the append
    Then the record path answers the owning service with MSG-P7-003
    Then no entry exists for "N-0101" and no chain_seq is consumed
    Then the notice stays "Approved" and is not written to the WIN file, and an incident is raised under rule R-UNI-39
    When the same record reference is retried and the store accepts the append
    Then one entry is appended and it takes the chain_seq the refused write did not use

  Scenario: AC7 A repeated record gives one entry (new, D-RCV-60)
    Given the record under record reference "RR223344556TH-2026-12-21" was appended and the ledger returned its entry ID
    When the same record with the same record reference arrives again, and the topic is replayed from the first offset of the business date
    Then one entry exists for the record, the first entry ID is returned and the repeat count of R-UNI-40 is raised by one
    Then no second entry and no second chain position are written, and the chain is unchanged

  Scenario: AC8 The two reads return the entry and its chain and are scoped (new, D-RCV-60)
    Given the entry of AC2 and the held entry of AC4 are stored for case "RC-2026-000321" on 2026-12-18 and 2026-12-14
    When the reader sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 200 with final call "DELIVERED", rule "R-LIT-07", the rule version in force, notice reference "N-0101", notice type "DEMAND", case reference "RC-2026-000321", the notice period start date 2026-12-18, decidedAt, prevHash and entryHash
    Then the response carries no notice state, no address, no customer name, no account number and no WIN payload
    When the reader sends GET /api/recovery/decision/v1/decision-log?caseId=RC-2026-000321&decision=D7.1&from=2026-12-14&to=2026-12-22&page=1
    Then the page holds the two entries in decidedAt order with a total of 2, and the delivered entry's prevHash equals the held entry's entryHash
    Given the rwb-access contract mock returns no Decision log right R for one caller and the scope of team "MTG-BKK" for the reader, against case "RC-2026-000654" in team "HP-NE"
    When each caller sends the read
    Then the responses are 403 with MSG-P4-002 and 404 with MSG-P4-003, and no entry is returned

  Scenario: AC9 A record without a rule version is refused (new, D-RCV-60)
    Given the rwb-comms contract mock returns a D7.1 record for notice "N-0101" with rule "R-LIT-09" and an empty rule version
    When the ledger consumes that record
    Then the append is refused with MSG-P7-009 naming "ruleVersion" and nothing is written
    Then no chain_seq is consumed and the fact stays on the topic for redelivery
    When the record is corrected to the rule version in force of "R-LIT-09"
    Then one entry is appended with both the rule id and the rule version

  Scenario: AC10 The ingest is continuous and the reads are one hop through the gateway (new, D-RCV-60)
    Given the record "RR223344556TH-2026-12-21" is published on rwb.decision-record.v1
    When the ledger ingests the record through the continuous Kafka consumer
    Then the entry reaches the ledger inside the completeness target in force (GAP-1276; ASM-2251), and the daily chain check and the seal stay with the baseline
    Then the JOB-10 Schedule of the loop is rwb-comms's and is not registered in this service
    When the reader sends GET /api/recovery/decision/v1/decision-log/{entryId} through the gateway-bff composite route
    Then the read is one hop, the service reads no table of another service, and the notice, the case, the deviation, the timer and the ledger entry arrive as facts or stay with their owners

  Scenario: AC11 A read without a valid caller is refused with 401 (new, D-RCV-60)
    Given the reader sends no valid credential
    When the reader sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 401 and no entry is returned
    When the reader sends GET /api/recovery/decision/v1/decision-log?caseId=RC-2026-000321&decision=D7.1&from=2026-12-14&to=2026-12-22&page=1
    Then the response is 401 and no entry is returned

  Scenario: AC12 A consumed call that fails or does not answer leaves the record unchanged (new, D-RCV-60)
    Given the rwb-case contract mock fails the transfer call for notice "N-0101" with reason "NOTICE_UNSERVED" and does not answer it
    When the ledger consumes the D7.1 record for notice "N-0101" with rule "R-LIT-09", final call "UNSERVED" and delivery status "UNDELIVERABLE"
    Then one decision_log_entry exists for "N-0101" as the record states, and the failed call changes no entry
    Then rwb-decision does not record the transfer as done, and the failed call is left to rwb-case's own handling; the fake asserts the call was made and not answered
```

The twelve criteria are new, and `acs` is empty for this story: no legacy criterion of RWB-E2-021 is owned verbatim here, because each of them acts on the notice, the WIN file or the proof and belongs to its own slice. The values are the legacy values — notices `N-0101`, `N-0102` and `N-0103`, cases `RC-2026-000321`, `RC-2026-000654` and `RC-2026-000655`, barcode `RR223344556TH`, call-back date `18122026` and the delivered date 2026-12-18, the business dates 2026-12-14, 2026-12-15, 2026-12-21 and 2026-12-22, decision code D7.1, rules `R-LIT-04`, `R-LIT-05`, `R-LIT-07`, `R-LIT-08`, `R-LIT-09` and `R-UNI-20`, hold reasons `CONTACT_STOP_X1`, `LEGAL_HOLD` and `TEMPLATE_WITHDRAWN`, results `DELIVERED`, `UNDELIVERABLE` and `PENDING`, final calls `HELD`, `DELIVERED` and `UNSERVED`, notice type `DEMAND`, template `DEMAND-SSME`, and the messages MSG-P6-008, MSG-P6-001, MSG-P6-003, MSG-P7-003 and MSG-P3-004 — and no new business value is introduced. The payload field set of the record, the placement of the notice reference and of the delivery facts, the rule version label, the message ids of this slice and a panel id for the record have no source and are carried in GAP-1276 with ASM-2246, ASM-2247 and ASM-2250. The `-ITG` copies of the test cases belong to RWB-ITG-E2021-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One entry per decision of the loop: a held letter, a delivered letter and an unserved letter each give one entry, and a held letter and its later delivery are two entries chained in decision order | Legacy RWB-E2-021 AC3, AC6, AC7, AC8; FSD P7 v3 A2.2; REQ-OCC-003 |
| BR2 | The entry carries decision code D7.1 and one of the final calls HELD, DELIVERED or UNSERVED, written through the decision-record path of DP-03; the decision code is read from LOV-DECISION at the version in force and is never a literal | Legacy RWB-E2-021 sections 4 and 18; TSD P7 v2 T3.1 and T3.2; BR-P7-002 |
| BR3 | Every entry is hash chained and append only: a `chain_seq`, a `prev_hash` equal to the previous entry's `entry_hash` (64 zeros for the first), an `entry_hash` equal to the SHA-256 of the canonical form, no UPDATE and no DELETE, and a correction as a new entry with `corrects_entry_id` | REQ-DRI-002, REQ-DRI-003; FSD P7 v3 AC-P7-001-01 and AC-ALT-P7-001-01; Architecture v5 slide 28 |
| BR4 | The entry names the notice reference, the notice type, the case reference, the rule id with its version, the final call, the hold reason or the delivery status and the notice period start date where one applies; it carries no address, no customer name, no account number, no WIN field and no file payload | Legacy RWB-E2-021 section 17; Architecture v5 slides 42 and 43 notes; §R7.2 s17 |
| BR5 | The rule id and the rule version are both on the entry and the pair exists in the rule registry at the version in force; a record with a rule id and no version is refused | FSD P7 v3 AC-EXC-P7-002-01 and A2.3; Drools design slide 16 (rule id and version in the record) |
| BR6 | One entry under a repeated record: the inbox dedupe and the record reference make a second entry impossible, and the repeat is counted for R-UNI-40 | FSD P7 v3 AC-EXC-P7-002-03; R-UNI-40 |
| BR7 | The hold reason and the delivery status are validated against the closed vocabulary the loop contract fixes: `CONTACT_STOP_X1` under R-LIT-05, `LEGAL_HOLD` under R-UNI-20, `TEMPLATE_WITHDRAWN` under R-LIT-04, and `UNDELIVERABLE`, `REFUSED` and `PENDING` under R-LIT-09 and R-LIT-08; no value is written in code | RWB-P6-E2021-CON AC4; Routing Logic v4 rows R-LIT-04, R-LIT-05, R-LIT-08, R-LIT-09 |
| BR8 | The story appends and exposes; it selects no notice, runs no conduct check, writes no hold reason, dispatches no file, captures no proof, moves no case and starts no timer | Architecture v5 slides 14 and 41; DP-01 |
| BR9 | The two reads declare the Decision log right R with the scope applied; a role without it is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003 | TSD P7 v2 T-A.1, T6.1 and T6.2; REQ-DRI-012 |
| BR10 | A record that lacks its decision code, its final call, its notice reference or its rule version, or that carries a value outside its list, is refused with MSG-P7-009 and appends nothing; no entry is written from an assumed value | FSD P7 v3 AC-ALT-P7-002-01, AC-EXC-P7-002-01 and AC-EXC-P7-002-05 read on this slice |
| BR11 | A delivered record carries the notice period start date from the call-back date under R-LIT-07; the notice period, the timer and the end date stay with rwb-case and are never computed here | R-LIT-07; CTL-15; Routing Logic v4 row R-LIT-07 |
| BR12 | The entry, its chain position, its inbox row and its idempotency row commit in one transaction; a failed append leaves nothing, the fact is redelivered, and the decision that cannot be recorded does not proceed | Principle 5; R-UNI-39; FSD P7 v3 A2.5; DP-03 |
| BR13 | The ingest of `rwb.decision-record.v1` is continuous Kafka and the entries reach the ledger inside the completeness target of Architecture v5 slide 28; the daily chain check and the seal are the baseline's, and the JOB-10 Schedule of the loop is rwb-comms's | Architecture v5 slides 28 and 44 (JOB-10, JOB-13, JOB-14); TSD P7 v2 T5.3; DP-10 |
| BR14 | The two reads are one hop from the gateway-bff composite route, the service reads no table of another service, and the notice, the case, the deviation, the timer and the ledger entry arrive as facts or stay with their owners | Architecture v5 slides 13 and 41; DP-01; DP-11; DP-18; DP-19 |

### 9. State transitions

None for a notice, a case, a timer or a WIN file. The states below are the states of an entry of this story, and the entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | `DecisionRecorded` arrives with decision code D7.1 and final call HELD | The hold reason is in the closed vocabulary, the rule id carries a version present in the registry, and the chain head is known | Appended at the next `chain_seq` with its `prev_hash`, its `entry_hash`, its inbox row and its idempotency row in one transaction |
| Absent | `DecisionRecorded` arrives with decision code D7.1 and final call DELIVERED | The call-back date is present and the entry carries the notice period start date | Appended at the next `chain_seq`, as above |
| Absent | `DecisionRecorded` arrives with decision code D7.1 and final call UNSERVED | The delivery status is `UNDELIVERABLE`, `REFUSED` or `PENDING`, and no notice period start date is carried | Appended at the next `chain_seq`, as above |
| Absent | The record fails the check of BR10, or the store or the chain is unavailable | The record is refused, or the append cannot commit | Absent: MSG-P7-009 or MSG-P7-003, nothing written, no chain position used, the fact redelivered and the decision stopped |
| Absent | The run passes a notice with no rule fired | A pass is a conduct result and not a decision of a rule | Absent by design: no entry, and the conduct result stays on the ledger entry of rwb-source-data |
| Appended | The same record arrives again with the same record reference | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A later decision of the same notice arrives | The notice is held and then delivered, or held and then unserved | A second entry is appended at the next `chain_seq`, chained to the first |
| Appended | A correction is taken | The correction names the entry it corrects | A new entry is appended with `corrects_entry_id`, and the corrected entry stays unchanged |
| Appended | An UPDATE or a DELETE is attempted, or the daily check and seal run | Any caller, including the schema owner | Unchanged: the statement is refused by the append-only rule, and the seal verifies the chain |

The notice stays in the state `rwb-comms` gives it (Approved, Held, Sent, Delivered or Unserved), the case state and the queue are `rwb-case`'s, and the NOTICE_PERIOD timer is `rwb-case`'s; this story changes none of them (BR8, BR11).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CONDUCT, conduct and QA officer | Reads the held and blocked entries of the cases in scope (Decision log R in TSD P7 v2 T6.1) and uses them for the conduct review |
| RW-LITOFF, litigation officer; RW-ENFORCE, enforcement owner | Reads the entries of the notices of the case in scope: the hold, the delivery and the unserved outcome with the rule and version |
| RW-LEGAL, legal counsel | Reads the entries that name a withdrawn template and the holds it caused |
| RW-AUDIT, internal audit and RW-COMPLY, Compliance and PDPA officer | Reads one entry and the entries of a case in a date range, with the chain fields, and never a customer value (Decision log R, scope ALL) |
| Every role of TSD P7 v2 T6.1 | Holds R on the decision log and reads the entries of the cases in its scope |
| SY-DECLOG, decision record writer | Writes the D7.1 record inside the decision transaction at the producer and appends it to the ledger here; the append is the service identity's and not a person's |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, the rule registry and the reference lists, and appends the entry, its inbox row and its idempotency row (DP-02) |
| A role outside the matrix, or a case out of the caller's scope | Refused with MSG-P4-002, or 404 with MSG-P4-003 |
| No approval level from the delegation of authority applies | The approval of a notice is the D7.1 approval of another P7 story and RWB-P6-E2021-CON; this story reads no `delegation_limit` row and approves nothing |

The right and the scope behind the two reads are declared on the operations and enforced at gateway-bff (DP-19), which asks `rwb-access`; this story adds no guard of its own, holds no role, scope or delegation row, and makes no authorise call (GAP-1276; ASM-2249). The database login is per service (DP-02) and this story refers to "the rwb-decision login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id (the case reference `RC-2026-000321`) | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code (D7.1, a value of LOV-DECISION) | Write |
| DF-DEC-004 | `decision_log_entry` | rule_id (R-LIT-04, R-LIT-05, R-LIT-07, R-LIT-08, R-LIT-09 or R-UNI-20) | Write |
| DF-DEC-005 | `decision_log_entry` | rule_version | Write; the label of the version in force is Not specified in the source documents (GAP-1276; ASM-2247) |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | model_version, agent_version | Not written: no model and no agent take part in a letter decision |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the reference to the facts the check read, with their freshness) | Write; the shape is Not specified in the source documents (GAP-1276; ASM-2246) |
| DF-DEC-009, DF-DEC-010, DF-DEC-011, DF-DEC-013 | `decision_log_entry` | recommendation, approver_user_id, approval_level, override_reason | Not written: the rule answers and does not propose, the approval of the notice is another story's entry, and a letter decision is not an override |
| DF-DEC-012 | `decision_log_entry` | final_call (HELD, DELIVERED or UNSERVED) | Write |
| DF-DEC-014 | `decision_log_entry` | actions (the notice reference and the notice type) | Write; the container is TSD P7 v2 T3.1 and its content for this record is Not specified in the source documents (GAP-1276; ASM-2246) |
| DF-DEC-015 | `decision_log_entry` | outcome (the hold reason or the delivery status, the notice period start date where one applies, and the message id the notice showed) | Write; the placement is the reading of ASM-2246 |
| DF-DEC-016, DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | decided_at, prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-029, DF-DEC-030, DF-DEC-031 | `decision_log_entry` | corrects_entry_id, actor_user_id, idempotency_key (the record reference of the loop) | Write; `corrects_entry_id` on a correction only |
| DF-LEG-015, DF-LEG-016, DF-LEG-018, DF-LEG-031, DF-LEG-032, DF-LEG-021, DF-LEG-022 | `notice` (P6) | id, case_id, notice_type, template_id, hold_reason, callback_date, delivery_status | Read as facts of the record, never a table |
| DF-CAS-001, DF-CAS-002 | `recovery_case` (P3) | id, case_no | Read as facts of the record, never a table |
| DF-CAS-020, DF-WRK-030 | `recovery_case` and `timer` (P3) | legal_hold, timer_type | Not read and not written: the flag and the NOTICE_PERIOD timer are rwb-case's, and the flag reaches the entry only as the hold reason the owning service sends |
| DF-INT-005, DF-INT-011, DF-INT-012 | `interaction` (P1) | channel, summary, conduct_check | Not read and not written; the ledger entry is rwb-source-data's (DP-18) |
| (rule registry) | `rule_row`, `rule_package_version` (P7) | rule id and version at the version in force | Read, to prove that the rule that decided the letter exists at that version |
| (reference lists, parameters) | reference data and `parameter_value` (P3) | LOV-DECISION which holds D7.1, the final-call list, the page-size bound and the completeness target | Read at the version in force; a direct call would add one C row (GAP-1277; ASM-2248) |
| `processed_event`, `idempotency_key` | PLT library in `rwb_decision` | event_id, consumer, processed_at; the record reference and the first entry ID | Write |
| `outbox_event` | PLT library in `rwb_decision` | none | Not written: this story publishes no event |

The trigger `tr_declog_append_only` is a database trigger of the store baseline, not a field or entity of LDM v9 or Data Classification v5, so no field ID above names it (DOR-RWB-P7-E2021-APP-7).

No row of `notice`, `recovery_case`, `deviation`, `timer`, `interaction`, `interface_config` or `parameter_value` is copied into `rwb_decision`: the notice, the case and the result arrive as facts of the record, and the address, the file payload and the customer value never arrive at all (DP-01, DP-18). Which fields Data Classification v5 classes as personal data are Not specified in the source documents (DOR-RWB-P7-E2021-APP-11), so the statement that no customer value is carried stays open until they are. The barcode `RR223344556TH`, the call-back date `18122026`, the delivered date 2026-12-18 and the business dates are named in this document as legacy values only, and none of them is a customer value. Field IDs are those of the Logical Data Model and Data Dictionary v9; the container of the notice reference, the hold reason, the delivery status and the notice period start date inside `actions` and `outcome` is the reading of ASM-2246 and is Not specified in the source documents (GAP-1276; ASM-2246).

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007) and the Ownership Map gives to P7. The request and response field set of a dispatch entry is Not specified in the source documents (GAP-1276; ASM-2246).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | API-P7-006: the entries of a case in a date range, searched by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | API-P7-007: one entry with its decision code, final call, rule id and version, notice reference, notice type, hold reason or delivery status, notice period start date and chain fields; 200 with the DecisionLogEntry | Decision log, right R, scope applied | Not applicable, read only |

The DecisionLogEntry body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `ruleId`, `ruleVersion`, `inputsRef`, `finalCall`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`, and for a dispatch entry the notice reference, the notice type, the hold reason or the delivery status and the notice period start date; the DecisionLogPage body carries `items`, `page`, `size` and `total`. The field-level shape is the reading of ASM-2246.

Errors: 401 no session (messageId Not specified in the source documents (CG-ALL-7248)); 403 the role lacks the Decision log right (MSG-P4-002); 404 the entry or the case is absent or outside the scope (MSG-P4-003); 422 a query value is outside its list (messageId Not specified in the source documents (CG-ALL-7248)); 503 the ledger is unavailable (messageId Not specified in the source documents (CG-ALL-7248)). Every error is an RFC 9457 problem response with `messageId` set. `GET /api/recovery/decision/v1/cases/{caseId}/recommendation` (API-P7-001) and the approval operations (API-P7-002 to API-P7-005) are the decision center's and belong to the approval and recommendation stories of this service; this story declares them neither as provided nor as consumed.

#### 12.2 REST operations consumed

| Item | Value |
|---|---|
| Operations consumed | None. The record of the loop arrives as the `DecisionRecorded` fact of 12.4 and not over REST, and this story calls no operation of another service: the notice, the case, the deviation, the timer and the ledger entry stay with their owners and no value of them is read back |
| Owner | rwb-decision owns this operation set and its schema `rwb_decision` (DP-01); the schemas `rwb_comms`, `rwb_case`, `rwb_source_data` and `rwb_integration` belong to their services and are neither read nor written here |

The capability area, the right and the scope of the two reads are declared on the operations and enforced at gateway-bff through the composite route of DP-19, which asks `rwb-access`, so this story adds no `RecoveryAccessGuard` equivalent and no authorise call (GAP-1276; ASM-2249). The reference lists, the parameters and the rule registry of 12.7 are read inside the service or at the version in force carried by the record; if the reference-data contract of `rwb-case` is called directly at a later version of this story, one C row is added and the same reads move there (GAP-1277; ASM-2248).

#### 12.3 Events published

| Item | Value |
|---|---|
| Events published | None. This story publishes no event of its own: the record is a fact of `rwb-comms` on `rwb.decision-record.v1` and the entries of the ledger are read through the operations of 12.1 |

`rwb.decision-record.DecisionRecorded.v1` is published by the owning service of each decision and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42, event 08), and the ledger append needs no confirmation event because the letter loop is not a point of no return of the strict mode of slide 28. The `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` events of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here.

#### 12.4 Events consumed

| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger and its shared topic; published by `rwb-comms` for the decisions of the letter loop, and by all 19 services for their own | `DispatchRecordListener`: inbox dedupe by event ID and by the record reference, then `DecisionLogAppendService` for the decision code D7.1, the final call, the rule id and version, the notice reference, the notice type, the case reference, the hold reason or the delivery status and the notice period start date |

The fact carries IDs, codes, versions, a rule reference and dates only; no address, no customer value and no WIN payload travels on the topic (BR4, BR12). Which further fields of the fact this service requires is Not specified in the source documents (GAP-1276; ASM-2246). Records with any other decision code are the ledger baseline's general ingest.

#### 12.5 Workflows and activities

| Item | Value |
|---|---|
| Workflows and activities | None. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09 |

The loop's own workflow is `NoticeDispatchWorkflow` on task queue `rwb-comms`, and it is neither started nor signalled here: this story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit.

#### 12.6 Schedules

| Item | Value |
|---|---|
| Schedules | None. This story creates no Temporal Schedule and starts nothing on a clock: the JOB-10 notice dispatch run at 16:00 is `rwb-comms`'s Schedule (Architecture v5 slide 44), and the one Schedule of this service's ledger, the chain check JOB-14 at 02:00, is the decision-log baseline's |

DP-10 applies here only to the owning service's Schedule: a Schedule is registered by the service that owns the job, and the record ingest of this story is continuous Kafka and not a clock (BR13).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The dispatch entry: the notice reference and type, the case, the rule and version, the final call, the hold reason or delivery status, the notice period start date and the chain position; append only |
| `rule_package`, `rule_package_version`, `rule_row` | P7 (`rwb_decision`) | Read by rule id and version to prove the rule that decided the letter exists at the version in force |
| `approval`, `rule_test_case` | P7 (`rwb_decision`) | Not read and not written here: the approval of a notice is the decision center's, and no rule package is tested by this story |
| `processed_event`, `idempotency_key` | PLT library, created in `rwb_decision` | Inbox dedupe and the idempotency key of the record reference (DP-09) |
| `outbox_event` | PLT library, created in `rwb_decision` | Present but not written: this story publishes no event |

Not owned and never read: `notice`, `template`, `merge_field` (P6), `recovery_case`, `timer`, `task` (P3), `deviation` (S8), `interaction` (P1), `interface_config`, `outbound_item` (P2), `role`, `permission` and `delegation_limit` (P4). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms record fake | RWB-P6-E2021-CON | The D7.1 records of notice `N-0101` for case `RC-2026-000321`: held under `R-LIT-05` with `CONTACT_STOP_X1`, held under `R-LIT-04` with `TEMPLATE_WITHDRAWN` and template `DEMAND-SSME` version 1, held under `R-UNI-20` with `LEGAL_HOLD`, delivered under `R-LIT-07` with call-back 2026-12-18, unserved under `R-LIT-09` with `UNDELIVERABLE`; the record of `N-0102` under `R-LIT-08` with `PENDING`; the pass of a statutory notice with consent withdrawn; a record with no rule version; a record carrying a field outside its list |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the record reference and a forced failure for AC6 |
| central ledger fake | The ledger side of `rwb.decision-record.v1` | The ledger reference of the entry, the completeness reading of the ingest, the replay of the same record of AC7, and the chain head AC6 asserts against |
| rwb-access scope fake | The edge declaration of DP-19 | The allow answer with the Decision log right R and case `RC-2026-000321` in scope; the refusal of MSG-P4-002 and the scope `MTG-BKK` against case `RC-2026-000654` of team `HP-NE` for MSG-P4-003 |
| reference, parameter and registry fake | The lists, parameters and rule registry of the service | LOV-DECISION holding D7.1, the final-call list, the hold reason and delivery status vocabulary, the page-size bound, the completeness target, and `R-LIT-04`, `R-LIT-05`, `R-LIT-07`, `R-LIT-08`, `R-LIT-09` and `R-UNI-20` at the version in force with one rule id present and no version |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 0 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; no operation of another service is called, and the right and the scope are enforced at the edge (DP-19) |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed, with the inbox dedupe by event ID and record reference; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the letter loop runs on `rwb-comms` and the chain check is the baseline's |
| File | None | No file input and no file output; the WIN file, the INT-15 proof and the customer documents never reach this service |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/dispatch`, Java package `th.co.scb.ace.workbench.recovery.decision.dispatch`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record itself: the append through the decision-record path, the chain, the append-only rule and the shared topic. DP-01 is the boundary: the entry lives in `rwb_decision` and the notice, the case, the deviation, the timer and the ledger entry are never read as tables. DP-07 is the D7.1 code and the closed vocabulary of hold reasons and delivery statuses read at the version in force. DP-09 is the inbox dedupe, the record reference and the CloudEvents envelope. DP-10 is stated as a boundary and not as work: the 16:00 run is `rwb-comms`'s Schedule and this story registers none (12.6). DP-11 is the one hop with a 2 s timeout and a breaker behind the edge, and it is why no service call is made on the consumer path. DP-13 is the base `/api/recovery/decision/v1`; DP-19 is the gateway-bff route through which SCR-38 Decision log query reaches the two operations. DP-05 and DP-18 have an instance only as an absence: this service reads no `v_ace_*` view and no ACE table — the proof rows of the legacy story arrive only as the delivery status of a record — and it writes no interaction entry, because the ledger is `rwb-source-data`'s.

The platform H dependencies of the DP table and the published C dependencies of other services are not in the metadata rows of this story, which name None and `RWB-P6-E2021-CON`; they are the dependencies the DP table adds and they are recorded in GAP-1277 and ASM-2248, with the two baselines of 12.7. None of them blocks the build beyond Day 1.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DispatchRecordListener | Kafka consumer with the inbox | Reads `DecisionRecorded` on `rwb.decision-record.v1`, deduplicates by event ID and record reference, keeps the D7.1 facts with final call HELD, DELIVERED or UNSERVED and hands them to the appender |
| DecisionLogAppendService | Service | Checks the decision code, the final call, the notice reference and type, the rule id with its version and the hold reason or delivery status, and writes the entry, its chain position, its inbox row and its idempotency row in one transaction (BR2, BR5, BR7, BR10, BR12) |
| ChainHasher | Service | The canonical form of an entry and its SHA-256, the first `prev_hash` of 64 zeros and the `prev_hash` of every later entry (BR3) |
| RuleRegistryReader | Repository | Reads `rule_row` and `rule_package_version` by rule id and version to prove the rule that decided the letter (BR5) |
| DecisionLogQueryController | Controller | The two operations of 12.1 with the declared right, the scope, the paging and the problem mapping for 401, 403, 404, 422 and 503 |
| DecisionLogQueryService | Service | The date-range search of a case and the single read, the row shape of a dispatch entry, and the total count of the page |
| DecisionLogRepository | Repository | `decision_log_entry` in `rwb_decision`, insert only, with the search indexes and the idempotency key |
| ReferenceListClient, ParameterClient | Client | LOV-DECISION, the final-call list, the closed vocabulary, the page-size bound and the completeness target at the version in force |

**Database and migrations**

- Writes `decision_log_entry`, its inbox and idempotency rows in schema `rwb_decision`, and reads `rule_row` and `rule_package_version` in the same schema; reads no other schema (DP-01).
- The table, its columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only` (a database trigger, not a field or entity of LDM v9 or Data Classification v5), the missing grant for UPDATE and DELETE and the unique key on the idempotency key belong to the decision-log store baseline and are not rebuilt here (GAP-1277).
- One migration step in the per-service Flyway sequence (DP-15): `V2021_1__decision_log_dispatch_index.sql` adds the composite index `ix_declog_dispatch_case ON decision_log_entry (case_id, decision_code, decided_at)` that the date-range read uses. The index name is Not specified in the source documents (GAP-1276; ASM-2246).
- No row of `notice`, `recovery_case`, `deviation`, `timer`, `interaction` or `parameter_value` is written here.

**Configuration and reference data**

- LOV-DECISION which holds D7.1, the final-call list of HELD, DELIVERED and UNSERVED, and the closed vocabulary of hold reasons and delivery statuses are read at the version in force; the values are the legacy values and the list names are those of TSD P7 v2 T3.2 and RWB-P6-E2021-CON AC4.
- The page-size bound of the search and the completeness target of the ingest are parameters with no default in code; their names are Not specified in the source documents (GAP-1276; ASM-2251). The rule version label is read from the registry and never composed in code (GAP-1276; ASM-2247).
- The outbox retry policy and the inbox retention are the platform's (RWB-PLT-TE006-CON). No feature switch of this story's own is named by a source: the record appears wherever the loop takes a decision, and the switch of the loop is `rwb.comms.win-dispatch-loop` of RWB-P6-E2021-APP.

**Build steps**

1. `DecisionLogRepository` and the index step; test the date-range read of a case, the single read and the INSERT-only constraint (AC8).
2. `ChainHasher` and the canonical form: `chain_seq`, `prev_hash` from the previous entry, the first `prev_hash` of 64 zeros and `entry_hash` as the SHA-256 of the canonical form (AC2, AC8).
3. `DispatchRecordListener` with the inbox and the dedupe by event ID and record reference; test the replay and the repeated record of AC7, and the pass that appends nothing (AC1).
4. `DecisionLogAppendService` with the checks of BR10 and the fail-closed transaction; test the forced failure of AC6 and the chain position the refused write does not use.
5. `RuleRegistryReader` and the rule id with its version; test the record without a version of AC9 and a pair absent from the registry (X2).
6. `ReferenceListClient` and `ParameterClient` with the version in force, and the refusal rather than an assumed code, final call or rule version (BR10, X10).
7. The four record shapes: held under `R-LIT-04`, `R-LIT-05` and `R-UNI-20`, delivered under `R-LIT-07`, unserved under `R-LIT-09` and `R-LIT-08`; tests for AC2, AC3, AC4 and AC5.
8. `DecisionLogQueryController` with the declared right, the scope, the paging and the problem mapping; tests for AC8, MSG-P4-002 and MSG-P4-003.
9. The boundary test: no write to `rwb_comms`, `rwb_case`, `rwb_source_data` or `rwb_integration`, and no address, customer value or WIN payload in any entry, event payload or log line (AC2, AC8, BR4).
10. The contract-fake run of the whole slice from Day 1: the record, library, ledger, scope, reference and registry fakes green before the real services land.

**Done when.** The tests of section 16 pass, the chain of a SIT day verifies from the first entry with no break, a held letter and its later delivery leave two chained entries naming their own rule and version, a refused decision leaves none and does not consume a chain position, a repeated record leaves one entry, both reads answer inside the 2 s budget of the frame, and no notice, case, timer or ledger entry was changed by this story.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | A dispatch record cannot be appended, or the store or the chain is unavailable | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record path, on the append; the owning service stops the decision, the notice stays Approved and is not written to the WIN file, and an incident is raised under R-UNI-39 |
| MSG-P7-009 | A record lacks its decision code, its final call, its notice reference or its rule version, or carries a value outside its list | Not specified in the source documents (GAP-1276; ASM-2250) | This story, on the schema check of the append, naming the missing field |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | The edge, through the authorise answer of the read |
| MSG-P4-003 | The case or the entry is outside the caller's scope | This case is not in your scope. | The edge, through the authorise answer of the read |
| MSG-P6-008 | The notice was refused, undeliverable or had no proof in the window | {notice} for case {case} was not served: {reason}. The case is in your queue to choose another service method. | `rwb-comms`; asserted here and named in the outcome of the entry |
| MSG-P6-001 | A contact stop blocked the letter | Contact with this customer is stopped for {reason}. | `rwb-comms`; asserted and named in the outcome of the held entry |
| MSG-P6-003 | The template was withdrawn before dispatch | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-comms`; asserted and named in the outcome of the held entry |
| MSG-P3-004 | A legal hold or a deviation blocked the letter | This case is on hold for {deviation}. The prescription date is still {date}. | `rwb-case`; asserted and named in the outcome of the held entry |
| MSG-P6-005 | The POST answers 409: the notice's template is not approved | {template} version {version} has no Legal approval. It cannot be used. | Not specified in the source documents (GAP-1096) |
| MSG-P3-005 | Not specified in the source documents (GAP-1096) | Not specified in the source documents (GAP-1096) | Not specified in the source documents (GAP-1096) |

MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-P6-008, MSG-P6-001, MSG-P6-003 and MSG-P3-004 are copied unchanged from RWB-E2-021 section 14 and the FSD P7 v3 message set. MSG-P7-009 is named by FSD P7 v3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05; its English text is Not specified in the source documents (GAP-1276; ASM-2250), because Error and Message Standard v4 holds MSG-P7-009 for another meaning (CG-ALL-7250). Thai text for each message follows decision DL10, which is still open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863. Delivery shape: every error is an RFC 9457 problem response with `messageId` set, `detail` carrying the text with its placeholders filled and `instance` naming the request, with the status mapping 401 no session, 403 MSG-P4-002, 404 MSG-P4-003, 422 a query value outside its list and 503 MSG-P7-003 on the record path.

### 15. Screens and states

No screen is built in this story. The two reads are consumed by SCR-38 Decision log query, which searches the log by case, rule, approver and date with export (FSD P7 v3 Screens), and by the auditor's view of the ledger; both are reached through the gateway-bff composite route of DP-19 and are another story's. The notice screens stay `rwb-comms`'s (SCR-18 Notice approval of RWB-E2-014) and the case timeline stays `rwb-case`'s (SCR-04), and this story feeds neither of them.

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The D7.1 entries of the case in decidedAt order, each with its rule and version, its notice reference and type, its final call and its hold reason or delivery status |
| The entry read | One entry | The same row with the notice period start date where one applies, its `decidedAt`, its `prevHash` and its `entryHash`, and a `correctsEntryId` beside the entry it corrects |
| The read | 403, or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for a case outside the scope; no row is returned |

A panel or screen id for showing the dispatch record beside the notice on the notice screens, and the field list of SCR-38, are Not specified in the source documents (GAP-1276; ASM-2246). The screen field list and the composite route specification belong to RWB-PLT-N001-CON and to the story that owns SCR-38. SCR-04 and SCR-38: the loading state is as Screen Specifications v1 gives it for that screen; their empty, error and no access states are Not specified in the source documents (CG-ALL-7254, CG-ALL-7256). SCR-18: its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-7255; DOR-RWB-P7-E2021-APP-10).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-021-01 | AC1, BR1; legacy Covers "AC1, BR1" | Integration | N-0101 Approved and acknowledged with `RR223344556TH`; a pass appends no entry, and the dispatch itself is rwb-comms's |
| TC-E2-021-02 | AC2, BR11; legacy Covers "AC2, BR5" | Integration | INT-15 `DELIVERED` with call-back `18122026`; entry under `R-LIT-07` with the notice period start date 2026-12-18 |
| TC-E2-021-03 | AC3, BR7; legacy Covers "AC3, BR6" | Component | INT-15 `UNDELIVERABLE`; entry `UNSERVED` under `R-LIT-09` naming MSG-P6-008 |
| TC-E2-021-04 | AC4, BR7; legacy Covers "AC4, BR2" | Component | Open deviation `X1` with the contact stop on; entry `HELD` with `CONTACT_STOP_X1` under `R-LIT-05` |
| TC-E2-021-05 | AC1, BR4; legacy Covers "AC5, BR4, BR10" | Contract | Postal consent `WITHDRAWN` with notice type `DEMAND` statutory; the pass appends no entry and the consent value is in no entry |
| TC-E2-021-06 | AC3, BR1; legacy Covers "AC6, BR7" | Component | N-0102 sent 2026-12-15 and N-0103 sent 2026-12-16; run of 2026-12-22; one entry `UNSERVED` with `PENDING` under `R-LIT-08` |
| TC-E2-021-07 | AC5, BR4; legacy Covers "AC7, BR3" | Component | Legal hold true; entry `HELD` with `LEGAL_HOLD` under `R-UNI-20`, naming MSG-P3-004 |
| TC-E2-021-08 | AC5, BR5; legacy Covers "AC8, BR8" | Component | `DEMAND-SSME` "TH" version 1 withdrawn 2026-12-13; entry `HELD` with `TEMPLATE_WITHDRAWN` under `R-LIT-04` |
| TC-E2-021-09 | AC6, BR12; legacy Covers "AC9, BR9" | Component | Open deviation `X2` with the stop on; decision log store stubbed unavailable; MSG-P7-003 and the incident under `R-UNI-39` |
| TC-E2-021-10 | AC7, BR6; legacy Covers "AC10" | Contract | The same record reference delivered twice, and a replay from the first offset of the business date |
| TC-E2-021-11 | AC8, BR9; legacy Covers "AC11" | Component | N-0200 and case `RC-2026-000654` outside scope; the date-range read of `RC-2026-000321` from 2026-12-14 to 2026-12-22 |
| TC-E2-021-12 | AC9, BR5; legacy Covers "AC12" | Unit | A record with rule `R-LIT-09` and no rule version; one entry read by its identifier |
| TC-E2-021-13 | AC8, BR9; legacy Covers "Access" | Component | RW-CASEOWN reads the entry with no Decision log right; refused with MSG-P4-002 |
| TC-E2-021-14 | AC6, BR12; legacy Covers "Principle 5" | NFR | The decision log write forced to fail on 10 unserved records; no notice changes, no chain position used, MSG-P7-003 and the incident raised |
| TC-E2-021-15 | AC7, BR3; new for the section 12.7 tables | Component | Each table of section 12.7 with its use column; a read or write outside the use column is not made |
| TC-E2-021-16 | AC10, BR13, BR14; new for the section 8 rules | Integration | Record `RR223344556TH-2026-12-21` on `rwb.decision-record.v1`; entry reaches the ledger inside the completeness target; read through the gateway-bff route in one hop |
| TC-E2-021-17 | AC11, BR9; new for the section 7 answers | Component | Both reads sent with no valid credential; 401 returned and no entry returned |
| TC-E2-021-18 | AC12; new for the section 7 failed-call answer | Component | rwb-case transfer call for `N-0101` with reason `NOTICE_UNSERVED` fails and does not answer; no transfer recorded as done by rwb-decision and no entry changed |

The fourteen legacy test cases of RWB-E2-021 are kept in the order of the work package, and each is answered here on the record side: the entry, its rule and version, its notice facts, its chain, its two reads and its refusals. The notice, the conduct check, the WIN file, the proof and the case move are the contract fakes' and their own services'. The legacy level System maps to Component, Contract or Integration as the row shows, Access to Component and Resilience to NFR. The `-ITG` copies of these cases end in `-ITG` and belong to RWB-ITG-E2021-ITG, which runs the same values across the five contracts. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision code, the final-call set, the hold reason and delivery status vocabulary, the rule versions, the page-size bound, the completeness target and the message ids are reference rows, registry rows or parameters read at the version in force; nothing of them is a constant here.
- No personal data in the entry, the inputs reference, the event, the audit line, the tests or the logs: the notice reference, the notice type, the case reference, the rule id and version, the final call, the hold reason or delivery status, the dates and the hashes only. The address, the addressee name, the account number and the WIN payload stay with `rwb-source-data`, `rwb-comms` and `rwb-integration` (BR4).
- No read of another service's tables (DP-01, DP-18): the notice, the case, the deviation, the timer and the ledger entry arrive as facts of the record or are never touched.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all, and the proof rows of the legacy story arrive as the delivery status of a record through `rwb-integration` and `rwb-comms`.
- One appender and no mover: this story changes no notice, no case, no timer and no ledger entry, so a decision record can never move a case (BR8).
- No entry without its decision and no decision without its entry: the entry, its chain position, its inbox row and its idempotency row commit in one transaction, and a decision whose record cannot be appended is stopped with an incident (BR12, R-UNI-39).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the chain is verifiable from `chain_seq` 1 (BR3).
- One entry per decision: the inbox dedupe and the record reference make a second entry for the same decision impossible, and a later decision of the same notice is a second entry and not an edit (BR1, BR6).
- One base, one topic and one queue: `/api/recovery/decision/v1`, `rwb.decision-record.v1` for the record and `rwb.decision.events.v1` for this service's own events, with `rwb-decision` in namespace `rwb-recovery`; no monolith base and no other service's base or topic is declared here as this service's own (DP-13, DP-14).
- One hop and 2 s with a breaker per downstream on the reads behind the edge; an unreadable list, parameter or rule row refuses the append rather than writing an assumed value (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters dispatched for print and post, proof of delivery returns | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-06, TC-E2-021-10, TC-E2-021-11 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05, FEAT-OCC-06 | 16 Manage risk, control and compliance | R-LIT-04, R-LIT-05, R-UNI-20, R-UNI-39 | TC-E2-021-04, TC-E2-021-07, TC-E2-021-08, TC-E2-021-09, TC-E2-021-14 |
| REQ-OCC-006 | Withdrawn consent stops the channel; statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-05 | 16 Manage risk, control and compliance | R-UNI-10 | TC-E2-021-05 |
| REQ-ILG-010 | Dispatch results, including proof of delivery, written to the ledger | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-LIT-07, R-LIT-09 | TC-E2-021-01, TC-E2-021-02, TC-E2-021-03, TC-E2-021-13 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-021, disposition Split (rework) |
| Legacy criteria owned here | None verbatim: `acs` is empty, and the nine criteria of section 7 are new for the decision-record slice |
| Legacy behaviour carried | AC3, AC6, AC7, AC8 and AC9 on the record side, with BR2, BR4, BR5, BR6, BR7, BR8 and BR9 |
| Test cases | TC-E2-021-01 to TC-E2-021-18, the fourteen in the legacy order and four new tests, TC-E2-021-15 to TC-E2-021-18 |
| Decoupling patterns | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-016 (reusable Temporal layer, Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-LIT-04, R-LIT-05, R-LIT-07, R-LIT-08, R-LIT-09, R-UNI-10, R-UNI-20, R-UNI-39, R-UNI-40 |
| Messages | MSG-P7-003, MSG-P7-009, MSG-P4-002, MSG-P4-003, MSG-P6-008, MSG-P6-001, MSG-P6-003, MSG-P3-004 |

| Legacy reference | Where it is kept |
|---|---|
| One entry for the held, delivered and unserved decision of a letter | Sections 1, 2, 4, 7 (AC2, AC3, AC4), 8 (BR1, BR2), 9 |
| The rule id and rule version of every entry | Sections 4, 7 (AC2, AC9), 8 (BR5), 11, 13 |
| A delivered letter starts the notice period from the proof, an unserved one never does | Sections 7 (AC2, AC3), 8 (BR11), 11 |
| The hold reasons `CONTACT_STOP_X1`, `LEGAL_HOLD` and `TEMPLATE_WITHDRAWN` with their rules | Sections 7 (AC4, AC5), 8 (BR7), 11, 13 |
| A decision that cannot be recorded does not proceed (legacy AC9) | Sections 5 (X3), 7 (AC6), 8 (BR12), 14 |
| Append only and hash chained, with the first `prev_hash` of 64 zeros | Sections 4, 7 (AC7, AC8), 8 (BR3), 9 |
| The two decision-log reads, one entry and the entries of a case in a date range | Sections 4, 7 (AC8), 8 (BR9), 12.1, 15 |
| Notices `N-0101`, `N-0102` and `N-0103`, cases `RC-2026-000321`, `RC-2026-000654` and `RC-2026-000655` | Sections 3, 7, 16 |
| Barcode `RR223344556TH`, call-back date `18122026`, delivered date 2026-12-18, business dates 2026-12-14 to 2026-12-22 | Sections 3, 7, 11, 16 |
| Decision code D7.1, rules `R-LIT-04`, `R-LIT-05`, `R-LIT-07`, `R-LIT-08`, `R-LIT-09`, hold reasons and results | Metadata, sections 1, 3, 7, 8, 11 |
| Messages MSG-P6-008, MSG-P6-001, MSG-P6-003, MSG-P3-004, MSG-P7-003 and MSG-P7-009 | Section 14, exception paths |
| Legacy key RWB-E2-021, story RWB-P7-E2021-APP, contract RWB-P6-E2021-CON, test cases TC-E2-021-01 to TC-E2-021-14, patterns DP01 to DP19 as listed | Metadata, sections 3, 12, 16 |

The other slices of the key answer the rest: RWB-P6-E2021-CON, RWB-P6-E2021-APP and RWB-P6-E2021-OPS the notice, the conduct check, the hold, the dispatch, the WIN file, the proof capture and the run; `rwb-case` and its own stories the legal hold, the case state, the queue transfer and the NOTICE_PERIOD timer; `rwb-source-data` the interaction ledger entry (DP-18); `rwb-integration` the WIN interface configuration and the file window; RWB-P4-E2021-APP the access answer of the readers; and RWB-ITG-E2021-ITG the cross-service harness and the `-ITG` copies.

### 19. Out of scope

- The notice, its states Approved, Held, Sent, Delivered and Unserved, the conduct check of the four gates, the template check, the notice hold and the dispatch selection: RWB-P6-E2021-APP, with the contract in RWB-P6-E2021-CON. This story appends the record of a decision and changes no notice.
- The INT-14 WIN dispatch file, the INT-15 proof round trip, the proof capture, the result-code map and the acknowledgement: RWB-P6-E2021-APP, RWB-P6-E1046-APP, RWB-P6-E1055-APP and `rwb-integration` (P2, DP-16). No file layout, barcode payload or WIN field is designed or stored here.
- The NOTICE_PERIOD timer, the case transfer with reason NOTICE_UNSERVED and the case state: `rwb-case` (P3). The notice period start date is written on the entry and the period itself is never computed here.
- The legal hold flag of the case: `rwb-case` (P3, DF-CAS-020). It reaches this story only as the hold reason `LEGAL_HOLD` of a record.
- The interaction ledger entry, its conduct check column, its channel and its summary: `rwb-source-data` (P1, DP-18) and RWB-P6-E2021-APP.
- The WIN interface configuration, the file runs and the outbound items: `rwb-integration` (P2). The JOB-10 Schedule at 16:00 is `rwb-comms`'s, and this story registers no Schedule (12.6).
- The D7.1 approval of a demand and recall notice, the approval queue SCR-10, the decision screen SCR-11 and the recommendation read `GET /cases/{caseId}/recommendation`: the other P7 stories of this service. This story approves nothing and reads no `delegation_limit` row.
- The general ingest of every other decision code into the ledger, the append-only table itself, the daily chain check JOB-14 at 02:00 and the daily seal: the decision-log baseline of this service.
- The data-lake copy of the log, JOB-13 and lake retention: retired with the data lake (DP-17); the ingest of the ledger is continuous Kafka.
- SCR-38 Decision log query as a built screen, the notice panel and the composite route: the screen stories and RWB-PLT-N001-CON.
- SMS and LINE dispatch through NSS and LINE OA (RWB-E2-022), alternate service methods and substituted service (R-LIT-10, R-LIT-11, Epic 5), the breach path for a contact sent while a block is on (FEAT-DVF-10, Epic 7) and notice approval (RWB-E2-014), as the legacy story left them.
- The `-ITG` copies of the test cases and the cross-service harness: RWB-ITG-E2021-ITG. The Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: RWB-P6-E2021-OPS and an OPS story of this legacy key.
