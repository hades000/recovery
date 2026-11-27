# RWB-P7-E2022-APP SMS and LINE dispatch through NSS and LINE OA

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2022-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 |
| Parallel lane | L-P7-AD |
| Ready to start | Day 1 |
| Size | Sized by the squad at refinement; no size is in the source documents (DOR-RWB-P7-E2022-APP-16) |
| Depends on (build) | None |
| Contract dependencies | RWB-P6-E2022-CON; RWB-P3-E1043-CON; RWB-P1-E1066-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-OCC-004, REQ-OCC-005, REQ-OCC-006, REQ-ILG-010, REQ-DRI-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-022 for rwb-decision; the contact-rule decision record of the SMS and LINE loop, appended once each and chained, plus the two decision-log reads of this service. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2022-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (15 resolved, 24 cross-document, 8 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story
As a **case owner who sends an SMS or a LINE message, the conduct officer who reads refusals and the auditor who reads the log**, I want **one decision entry for every contact check of the SMS and LINE loop — decision code "X6" with final call "contact refused" on a refusal caused by a contact stop, by no consent, by a legal hold or by a withdrawn template, with the rule id and rule version, the channel, the reason code, the case reference and the requesting role, appended once, chained and append only — and the two reads that let me read one entry and the entries of a case in a date range**, so that **every refused contact and every contact that was allowed can be traced to the rule that decided it, no contact stands without its record, and the record that explains a contact can never be quietly changed**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-022:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`, and the shared topic `rwb.decision-record.v1` through the decision-record path of DP-03.
- One deliverable and nothing else: the contact-rule decision record of the SMS and LINE loop. On a refusal of the contact check — a contact stop from a lost contact, a contact stop from a dispute or complaint, no consent on the channel, a legal hold, or a withdrawn template — the entry carries decision code "X6" with final call "contact refused", the rule id and rule version that fired, the channel (`SMS` or `LINE`), the reason code, the case reference and the requesting role. On a send that passed the check, the entry carries the same decision code, the channel, the case and the requesting role, and its final call has no source (GAP-1274; ASM-2253).
- The record is appended once for each refusal and once for each send it records, in the transaction of that refusal or that send, hash chained to the entry before it and never changed afterwards. A refusal whose record cannot be appended is not completed: the answer is MSG-P7-003, nothing is sent to NSS or to LINE OA, and an incident is raised under R-UNI-39. The record carries references, codes and the reason only: the message body, the phone number, the LINE identifier and every customer value stay outside it, because the contact point travels as a token and this service never sees it (BR5, BR12).
- What stays with `rwb-comms` (P6, RWB-P6-E2022-APP, RWB-P6-E2022-CON and RWB-P6-E2022-OPS): the send operation, the conduct check itself, the template check, the merge, the outbox, the retry limit of 5 with rule R-UNI-34 and the exception queue, the NSS and LINE OA dispatch, the delivery status on the interaction, the failed count and the message history. None of it is rebuilt here.
- What stays elsewhere: `rwb-source-data` (P1, DP-18) the interaction ledger, the contact point and its consent; `rwb-case` (P3) the case, the legal hold flag and the reference data; `rwb-deviation` (S8) the deviation and its contact stop; `rwb-integration` (P2) the NSS and LINE interface configuration; `rwb-access` (P4) the session, the role and the scope behind the two reads.
- The rule packages stay in the registry of this service, but the evaluation runs embedded in the owning service (DP-04); this story records the decision and does not evaluate the rule. It loads no rule model, calls no Drools runtime and reads no `rule_package` row on the request path.

The legacy behaviour carried into the decision service is unchanged in meaning: the contact check decides before anything leaves, a refusal is written before the answer, the entry names what fired, and no contact stands without its record (legacy RWB-E2-022 AC3, AC10, BR1, BR7 and exception X8).

### 2. Business rationale
A message can reach a customer under a contact stop or without consent only if the check that should have stopped it leaves no trace of its own. The legacy story answered the sending; this slice answers the evidence: which rule refused the contact, at which version, on which channel, for which reason, on which case and for which role — and the same evidence for a contact that was allowed, so a refusal and a permission can be read side by side by the officer who sent the message, by the conduct officer who reviews blocked contacts and by the auditor who later asks why a customer was contacted.

Under Architecture v5 the approvals, the rule registry and the central decision ledger are `rwb-decision` (slides 14, 27, 28 and 41); each service writes its decision record through the local library in the same transaction as the change it records and publishes `DecisionRecorded` on `rwb.decision-record.v1` (slides 20 and 28); `rwb-decision` collects the records into the ledger, seals it daily in write-once storage and answers the decision-log reads (slide 28). The realignment changes the mechanism, not the business rule:

1. The in-process decision-log write of the monolith becomes the decision-record path of DP-03: the record is written where the refusal or the send commits and is appended here from the shared topic, with the append-only rule and the hash chain the FSD already carries (FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-03).
2. The record is not a copy of the message: it names the case, the channel, the rule and its version, the reason code and the requesting role. The message body, the phone number, the LINE identifier and the template body stay in `rwb_comms`, `rwb_source_data` and the ACE notification path (BR5, BR12).
3. Decision code "X6", final call "contact refused" and the reason codes are data: the decision code is a value of LOV-DECISION read through the reference-data contract of `rwb-case` (DP-07), the final call is a row of the service's own vocabulary, and the reason codes are reference rows (BR8). None of them is a literal in code.
4. The evaluation stays embedded in the owning service (DP-04), so a rule version can change without a release of this service and every entry still names the version that answered (slide 27).
5. The two reads are one base (DP-13): the entries of a case in a date range and one entry with its chain fields; the data-lake copy of the log is retired with the data lake (DP-17) and the daily chain check JOB-14 at 02:00 covers these entries like any other.

Append only and hash chained means a refused contact leaves either a complete entry or nothing, a repeated record leaves one entry, and a break in the chain is a reportable event rather than a silent edit. This story meets REQ-OCC-004, REQ-OCC-005, REQ-OCC-006 and REQ-ILG-010 on the record side: it proves that the contact check decided before anything left, that the channel a customer withdrew is held, and that a dispatched message and a refused one both leave a record. It carries controls CTL-16 and CTL-17 as evidence rather than as behaviour, and it applies the principle that no action proceeds unlogged (R-UNI-39). REQ-DRI-006 is met in the strongest form available: this story calls no system of record, no channel platform and no PII service, so it cannot become a second path to NSS, LINE OA or ACE.

### 3. Preconditions
| Precondition | What it gives this story |
|---|---|
| RWB-P6-E2022-CON | The published dispatch contract of `rwb-comms`: `POST /cases/{caseId}/messages` with channel `SMS` or `LINE`, template code, language, party, the 202 interaction answer, the 409 refusals with MSG-P6-001, MSG-P6-002, MSG-P6-003 and MSG-P3-004, and the declaration of the decision record on `rwb.decision-record.v1`. Which fields of that record this service consumes is Not specified in the source documents (GAP-1274; ASM-2252) |
| RWB-PLT-E1027-CON | The decision-record path and the shared topic `rwb.decision-record.v1` (DP-03): the append, the chain position, the `prev_hash`, the `entry_hash`, the append-only rule, the idempotency key of a record and the local write inside the producer's transaction |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION, which holds "X6", the final-call list, which holds "contact refused", the reason-code list and LOV-CHANNEL with `SMS` and `LINE`, each at the version in force. The final-call list and the reason-code list have no name in the sources (GAP-1274; ASM-2253) |
| RWB-PLT-TE006-CON, RWB-PLT-N001-CON | The outbox and inbox library with CloudEvents (DP-09) for the inbox dedupe of the consumed records and the idempotency row of an append, and the gateway-bff composite route (DP-19) through which the case owner, the conduct officer and the auditor reach the two reads |
| The decision-log store baseline | `decision_log_entry` with the columns of TSD P7 v2 T3.1, the append-only trigger `tr_declog_append_only`, the missing grant for UPDATE and DELETE, the unique key on the idempotency key and the chain check JOB-14 at 02:00. The baseline is the service's own earlier work and is in no H row of this story (GAP-1274; ASM-2255) |
| The authorise answer of `rwb-access` (P4) | `POST /api/recovery/access/v1/authorise` (Architecture v5 slide 14) for the Decision log right R and the caller's scope behind the two reads; consumed, faked and in no C row of this story. DP-08 is not in the pattern set of this legacy key, so the right is declared at gateway-bff and this story keeps a local guard that refuses closed (GAP-1274; ASM-2255) |

Business preconditions carried from RWB-E2-022:

- Templates `SMS-REMIND` `TH` version 1 (channel `SMS`) and `LINE-REMIND` `TH` version 1 (channel `LINE`) are Approved and current; template status is `rwb-comms`'s and never changes the record of a decision already taken.
- Case `RC-2026-000777` is owned by `CO-0201` with borrower party `P-0077`, and it has no legal hold and no open deviation at the moment of the send. Party `P-0077` has a verified `MOBILE` contact point and a verified `LINE` contact point, each with consent `GIVEN`; the withdrawals and the stops named in the criteria are the legacy values (consent `WITHDRAWN`, deviation `X6` lost contact, deviation `X1` with contact stop on, legal hold true).
- The phone number and the LINE identifier stay tokens in the Workbench and the ACE notification path detokenizes them; no test, fixture, log line or entry of this story holds a number or an identifier (legacy section 17). No build dependency: the story builds against RWB-P6-E2022-CON and its fakes, and every platform contract of the DP table is a wave 0 or wave 1 contract.

### 4. Flow
1. `rwb-comms` (P6): receives `POST /cases/{caseId}/messages` on its own base for case `RC-2026-000777`, channel `SMS` or `LINE`, template `SMS-REMIND` or `LINE-REMIND`, language `TH` and party `P-0077`, and runs the contact check inside its own transaction (RWB-P6-E2022-APP).
2. `rwb-comms` evaluates the contact rules embedded in its own activity (DP-04) and takes one answer with the rule id and the rule version that fired: R-UNI-04 for a contact stop, R-UNI-10 for no consent on the channel, R-UNI-20 for a legal hold and R-LIT-03 for a withdrawn template.
3. `rwb-comms`, on a refusal, answers 409 with MSG-P6-001 naming the reason, MSG-P6-002 naming the channel, MSG-P6-003 naming the template or MSG-P3-004 for the legal hold, and writes in that same transaction the record with decision code "X6", final call "contact refused", the rule id and version, the channel, the reason code, the case reference and the requesting role `RW-CASEOWN`.
4. `rwb-comms`, on a send that passed the check, writes its interaction, its outbox row and in the same transaction the record of the send with decision code "X6", the channel, the case and the requesting role; the final call of that record is Not specified in the source documents (GAP-1274; ASM-2253).
5. The record path publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed by the case ID, with the entry ID, the record's idempotency key and the facts of the decision (DP-09; Architecture v5 slide 42, event 08).
6. `rwb-decision` `ContactRecordListener`: reads the fact into the inbox of DP-09, deduplicates it by event ID and by the record's idempotency key (R-UNI-40), keeps the facts whose decision code is "X6", and passes them to `ContactRecordAppendService`. Every other decision code is the decision-log baseline's general ingest and not this story's.
7. `ContactRecordAppendService`: reads LOV-DECISION, the final-call list, the reason-code list and LOV-CHANNEL through the reference-data contract of DP-07 at the version in force, requires the decision code, a final call from the list, the rule id, the rule version, the channel, the case reference and the requesting role, and refuses a record that lacks any of them with MSG-P7-003 naming the missing field; nothing is written (BR8, BR11). A repeated fact with the same idempotency key returns the first entry's ID, raises the repeat count for R-UNI-40 and appends nothing (BR7); a second append for the same refusal of the same case, channel and rule at the same decided time is refused with 409 and MSG-GEN-004 (BR6).
8. `ContactRecordAppendService`, one transaction in `rwb_decision`: takes the next `chain_seq`, computes `prev_hash` from the last entry's `entry_hash` (64 zeros for the first), computes `entry_hash` as the SHA-256 of the entry's canonical form, writes the `decision_log_entry` row with `inputs_ref` pointing at the inputs reference of the record, and writes the inbox row of the fact and the idempotency row of the key. A failed append changes nothing (BR3, BR13).
9. A case owner, a conduct officer or an auditor reads the entries of a case in a date range with `GET /api/recovery/decision/v1/decision-log` by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`, and one entry with `GET /api/recovery/decision/v1/decision-log/{entryId}`; each row holds `entryId`, `chainSeq`, the case, the decision code, the final call, the rule id and version, the channel, the reason code, the requesting role, the inputs reference, `decidedAt`, `prevHash` and `entryHash` and never a message body or a contact value. A caller without the right is refused with 403 and MSG-P4-002 and a case outside its scope with 404 and MSG-P4-003 (BR10).
10. Nothing in this story sends a message, moves a case, clears a deviation or changes a contact point: the refusal is `rwb-comms`'s, the case is `rwb-case`'s and the consent is `rwb-source-data`'s (BR9). Every entry commits with its chain position, its inbox row and its idempotency row in one transaction (BR13), and the ingest of the shared topic is continuous Kafka with no Schedule (12.6).

### 5. Exception paths
| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The record names no decision code, no final call, no rule id, no rule version, no channel, no case or no requesting role | The append is refused, nothing is written and no chain position is used | MSG-P7-003 | AC1, AC12 |
| X2 | The decision code is not a value of LOV-DECISION, or the final call is not in the final-call list at the version in force | The append is refused and the fact stays on the topic for redelivery; nothing is written from an assumed value | MSG-P7-003 | AC3, AC4 |
| X3 | The decision log store is unavailable, or the chain position cannot be taken | The refusal is not completed: `rwb-comms` answers 503, nothing is sent to NSS or to LINE OA, and an incident is raised as in R-UNI-39 | MSG-P7-003 | AC7 |
| X4 | The same record is delivered again, or replayed from the topic | One entry exists; the inbox dedupe and the idempotency key both hold, and the repeat is counted for R-UNI-40 | None | AC9 |
| X5 | A second append arrives for the same refusal of the same case, channel and rule at the same decided time | The second append is refused and the first entry stands | MSG-GEN-004 | AC9 |
| X6 | A delivery result of NSS or LINE OA arrives for a reference the ledger already holds (`FAILED`, `DELIVERED` or `READ`) | No entry is appended and no chain position is used: a delivery result is not a decision of this service and the delivery status is `rwb-comms`'s | None | AC6, AC9 |
| X7 | A correction of an entry is needed, or an UPDATE or a DELETE is attempted | A correction is a new entry with `corrects_entry_id` and the corrected entry stays unchanged; an UPDATE or a DELETE is refused by the missing grant and by `tr_declog_append_only`, and the attempt is audited | None | AC8 |
| X8 | The caller holds no Decision log right, or asks for a case outside its scope | 403 with MSG-P4-002, or 404 with MSG-P4-003; no entry is returned | MSG-P4-002, MSG-P4-003 | AC10, AC11 |
| X9 | The authorise answer or a reference list does not arrive inside the 2 s budget | The read or the append is refused closed rather than assumed, and the fact is retried; the answer is never widened to cover the failure | MSG-GEN-006, MSG-P7-003 | AC10, AC1 |
| X10 | A refusal was blocked by the contact check but its local record was not written in the producer's transaction | Nothing is sent, the send answers MSG-P7-003, and no fact reaches this service, so no entry and no chain position exist for it | MSG-P7-003 | AC7 |
| X11 | An entry carries a message body, a phone number, a LINE identifier or a customer value, in a fixture or in a payload | The boundary test fails the build: the record carries references, codes and the reason only | None | AC12 |

An entry is only ever appended beside the decision that caused it, so nothing of this story can send a message, and no message can leave with a decision that has no record (BR13).

### 6. INVEST check
| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E2022-CON and its fakes, the decision-record path of DP-03, the reference-data contract and the decision-log store baseline; no conduct check, template check, outbox, retry, dispatch, delivery status or ledger entry is rebuilt here |
| Negotiable | The decision code, the final-call list, the reason-code list, the channel list and the message ids are data or parameters of their owners; the story fixes only the entry, the append-only rule, the chain and the two reads |
| Valuable | Every refused contact and every contact that was allowed can be traced to the rule and the version that decided it, and that explanation cannot be quietly changed |
| Estimable | One listener, one appender with the chain, one query controller with two operations, one boundary test and one fake set |
| Small | Fits one sprint with its tests; it is the decision-record slice of a legacy key split five ways |
| Testable | Each of the twelve criteria in section 7 runs as one automated test against the contract fakes, on a fixed business date and a fixed chain |

### 7. Acceptance criteria
`acs` is empty for this story: no legacy acceptance criterion of RWB-E2-022 is owned verbatim here, because every criterion of the key sends a message, refuses a send, maps a delivery result or reads an interaction, and those belong to RWB-P6-E2022-APP, RWB-P1-E2022-APP, RWB-P4-E2022-APP and RWB-ITG-E2022-ITG. The fourteen criteria below are new for the `rwb-decision` slice and test only the record, its chain and its two reads. They add no business value: they keep the legacy values — decision code "X6" and final call "contact refused" exactly as the legacy story writes them, the channel values `SMS` and `LINE`, the templates `SMS-REMIND` and `LINE-REMIND` in `TH` at version 1, the case `RC-2026-000777` owned by `CO-0201` with borrower party `P-0077`, the deviations `X6` lost contact and `X1` dispute or complaint with the contact stop, the consent values `GIVEN` and `WITHDRAWN`, the contact types `MOBILE` and `LINE`, the hold and refusal reasons of the legacy story, legal hold true, the retry limit of 5 with rule R-UNI-34, the exception queue, the delivery status `FAILED`, the conduct checks `PASSED` and `BLOCKED`, the delivery statuses `DELIVERED` and `READ`, the message ids expected, the external reference "NSS-7781", the Idempotency-Key "c0ffee00-0001", the inputs reference "inputs/2026-12-03/7f3a", the rule version "UNI-2026.11" and the roles of the legacy story.

```gherkin
Feature: The contact-rule decision record of the SMS and LINE loop
  Background:
    Given templates "SMS-REMIND" "TH" version 1 channel "SMS" and "LINE-REMIND" "TH" version 1 channel "LINE" are Approved and current
    Given case "RC-2026-000777" is owned by "CO-0201" with borrower party "P-0077", no legal hold and no open deviation
    Given the rwb-case contract mock returns LOV-DECISION with "X6", the final-call list with "contact refused", the reason-code list and LOV-CHANNEL with "SMS" and "LINE" at the version in force
    Given the rwb-access contract mock returns the Decision log right R on case "RC-2026-000777"
    Given the decision-record library fake appends on the chain of case "RC-2026-000777" and returns the next chain_seq
  Scenario: AC1 Contact stop from a lost contact records one entry (new, D-RCV-60)
    Given case "RC-2026-000777" has an open deviation "X6" lost contact
    Given the rwb-comms contract mock returns the refusal with MSG-P6-001 naming "X6 Lost contact" and the record with decision code "X6", final call "contact refused", rule id "R-UNI-04", rule version "UNI-2026.11", channel "SMS", reason code "X6 Lost contact" and requesting role "RW-CASEOWN"
    When the ledger consumes rwb.decision.DecisionRecorded.v1 for that record
    Then one decision_log_entry exists with decision code "X6", final call "contact refused", the channel "SMS", the reason code "X6 Lost contact", the case reference "RC-2026-000777" and the requesting role "RW-CASEOWN", with a chain_seq, a prev_hash and an entry_hash
    Then GET /api/recovery/decision/v1/decision-log/{entryId} returns it with finalCall "contact refused", rule id "R-UNI-04" and rule version "UNI-2026.11"
  Scenario: AC2 Contact stop from a dispute or complaint records one entry (new, D-RCV-60)
    Given case "RC-2026-000777" has an open deviation "X1" with contact stop on
    Given the rwb-comms contract mock returns the refusal with MSG-P6-001 naming "X1 Dispute or complaint" and the record with decision code "X6", final call "contact refused", rule id "R-UNI-04", channel "LINE" and reason code "X1 Dispute or complaint"
    When the ledger consumes that record
    Then one decision_log_entry exists for case "RC-2026-000777" with decision code "X6", final call "contact refused", the channel "LINE" and the reason code "X1 Dispute or complaint", and it carries no message body, no phone number, no LINE identifier and no contact value
  Scenario: AC3 No consent on the channel records one entry (new, D-RCV-60)
    Given party "P-0077" has a "MOBILE" contact point with consent "WITHDRAWN"
    Given the rwb-comms contract mock returns the refusal with MSG-P6-002 naming "SMS" and the record with decision code "X6", final call "contact refused", rule id "R-UNI-10", channel "SMS" and reason code "No consent on the channel"
    When the ledger consumes that record
    Then one decision_log_entry exists with decision code "X6", final call "contact refused", the channel "SMS" and rule id "R-UNI-10", and it names neither the contact type "MOBILE" nor the party "P-0077"
  Scenario: AC4 A legal hold records one entry (new, D-RCV-60)
    Given case "RC-2026-000777" has legal hold true
    Given the rwb-comms contract mock returns the refusal with MSG-P3-004 and the record with decision code "X6", final call "contact refused", rule id "R-UNI-20", channel "LINE" and reason code "Legal hold"
    When the ledger consumes that record
    Then one decision_log_entry exists with decision code "X6", final call "contact refused", rule id "R-UNI-20", the channel "LINE" and the reason code "Legal hold", and it records the refusal and changes no case flag: legal hold stays rwb-case's
  Scenario: AC5 A withdrawn template records one entry (new, D-RCV-60)
    Given template "SMS-REMIND" "TH" version 1 is Withdrawn and no later version is Approved
    Given the rwb-comms contract mock returns the refusal with MSG-P6-003 naming "SMS-REMIND" and the record with decision code "X6", final call "contact refused", rule id "R-LIT-03", channel "SMS" and reason code "Template withdrawn"
    When the ledger consumes that record
    Then one decision_log_entry exists with decision code "X6", final call "contact refused", rule id "R-LIT-03" and the reason code "Template withdrawn", and it carries no template code, no template version and no template body, because the template and its status are rwb-comms's
  Scenario: AC6 A send that passed the check records its entry in the send transaction (new, D-RCV-60)
    Given party "P-0077" has a verified "MOBILE" contact point with consent "GIVEN"
    Given the rwb-comms contract mock returns the send of channel "SMS" accepted with reference "NSS-7781", an interaction with conduct check "PASSED" and delivery status "DELIVERED", and the record with decision code "X6", channel "SMS" and requesting role "RW-CASEOWN" and no reason code
    When the ledger consumes that record
    Then one decision_log_entry exists for case "RC-2026-000777" with decision code "X6", the channel "SMS" and the requesting role "RW-CASEOWN", appended once with a chain_seq and no reason code, and its final call is Not specified in the source documents (GAP-1274; ASM-2253)
    When a later delivery result of "FAILED" arrives for the same reference
    Then no second entry is appended and no chain position is used
  Scenario: AC7 A refusal whose record cannot be appended is not completed (new, D-RCV-60)
    Given case "RC-2026-000777" has an open deviation "X6" lost contact
    Given the decision-record library fake refuses the append of the record that rwb-comms holds in the refusal transaction
    Given the rwb-comms contract mock answers the send with status 503 and MSG-P7-003, sends nothing to NSS and raises an incident under rule R-UNI-39
    When the ledger consumes nothing, because no record reaches rwb.decision-record.v1
    Then no decision_log_entry exists for that refusal, no chain_seq is consumed and the refusal is not shown as taken
    When the same refusal is retried and the record path accepts the append
    Then one entry is appended and it takes the chain_seq the refused write did not use
  Scenario: AC8 The ledger is append only and hash chained (new, D-RCV-60)
    Given an entry for case "RC-2026-000777" with chain_seq 1 and final call "contact refused" is stored
    When an UPDATE setting final_call to "contact allowed" and a DELETE of the entry are attempted through the rwb-decision login and again through the schema owner role
    Then all four statements are refused: by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged and the refused attempts are written to the ACE audit log with the table, the operation and the entry ID
    When a correction of the entry is taken
    Then a new entry is appended with corrects_entry_id naming it, and the corrected entry is still unchanged
  Scenario: AC9 A repeated record gives one entry and a duplicate append is refused (new, D-RCV-60)
    Given the record of the refusal with Idempotency-Key "c0ffee00-0001" was appended and the ledger returned its entry ID
    When the same record with Idempotency-Key "c0ffee00-0001" arrives again
    Then one entry exists for the refusal, the first entry ID is returned, the repeat count of R-UNI-40 is raised by one, and no second entry and no second chain position are written
    When a second append arrives for the same refusal of case "RC-2026-000777", channel "SMS", rule "R-UNI-04" at the same decided time under a different key
    Then the second append is refused with status 409 and MSG-GEN-004 and the first entry stands
  Scenario: AC10 A case owner, the conduct officer and an auditor read one entry (new, D-RCV-60)
    Given the entry of AC1 is stored for case "RC-2026-000777"
    When the case owner with role "RW-CASEOWN", the conduct officer with role "RW-CONDUCT" and the auditor with role "RW-AUDIT" send GET /api/recovery/decision/v1/decision-log/{entryId}
    Then each response is 200 with the decision code "X6", the final call "contact refused", the rule id "R-UNI-04", the rule version "UNI-2026.11", the channel "SMS", the reason code "X6 Lost contact", the case reference "RC-2026-000777", the requesting role "RW-CASEOWN", decidedAt, prevHash and entryHash
    Given the rwb-access contract mock returns MSG-P4-002 for the caller's Decision log right R
    When that caller sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the response is 403 with MSG-P4-002 and no entry is returned
  Scenario: AC11 The entries of a case are read in a date range (new, D-RCV-60)
    Given the entries of AC1 and AC2 are stored for case "RC-2026-000777" on 2026-12-03
    When the case owner sends GET /api/recovery/decision/v1/decision-log?caseId=RC-2026-000777&from=2026-12-01&to=2026-12-31 with page 1 and the page-size bound in force
    Then the page holds both entries in decidedAt order with the total count of the case
    When the same read is sent with from=2026-12-04 and to=2026-12-31
    Then the page holds no entry and the total is 0
    Given case "RC-2026-000778" is outside the caller's scope
    When the case owner sends GET /api/recovery/decision/v1/decision-log?caseId=RC-2026-000778
    Then the response is 404 with MSG-P4-003 and no entry of that case is returned
  Scenario: AC12 The entry carries codes, references and the reason and no customer value (new, D-RCV-60)
    Given the rwb-comms contract mock returns the record of the refusal of AC1 with the inputs reference "inputs/2026-12-03/7f3a", and the message body, the phone number, the LINE identifier and the contact value behind it
    When the ledger consumes and appends that record
    Then the entry holds the decision code "X6", the final call "contact refused", the rule id "R-UNI-04", the rule version "UNI-2026.11", the channel "SMS", the reason code "X6 Lost contact", the case reference "RC-2026-000777", the requesting role "RW-CASEOWN" and the inputs reference "inputs/2026-12-03/7f3a"
    Then the entry, its event payload and its audit line hold no message body, no phone number, no LINE identifier, no contact value, no template body and no party identifier
    Then the message body, the contact value and the template body stay in rwb_comms, rwb_source_data and the ACE notification path
  Scenario: AC13 A record without its required fields, personal data or a rule package is refused (new, D-RCV-60)
    Given the rwb-comms contract mock returns a refusal record without its final call
    When the ledger consumes that record
    Then the record is refused with a message ID Not specified in the source documents (NEWAC-RWB-P7-E2022-APP-AC13) naming the missing field, nothing is appended and no entry is written from an assumed value
    Given the rwb-comms contract mock returns a record that carries a message body, a phone number and a LINE identifier
    When the ledger consumes that record
    Then no entry, event payload, audit line or log holds any of them
    Given a rule package is offered to the record path
    When the record path receives it
    Then no rule is evaluated and no workflow, activity or Schedule is registered on the path
  Scenario: AC14 A read without valid credentials is answered 401 (new, D-RCV-60)
    Given the caller sends no valid credentials
    When the caller sends GET /api/recovery/decision/v1/decision-log/{entryId} or GET /api/recovery/decision/v1/decision-log?caseId=RC-2026-000777
    Then each response is 401 and no entry is returned
```

The fourteen criteria are new and `acs` is empty for this story. Every value inside them is a legacy value of RWB-E2-022 or of the P7 baseline, and no new business value is introduced. The payload field set of the record, the request and answer shape of the two reads, the final call of a passed check, the reason-code list, the rule version label of R-LIT-03, the parameter names and the per-service login name have no source and are carried in GAP-1274 and GAP-1275 with ASM-2252 to ASM-2255. The `-ITG` copies of the test cases belong to RWB-ITG-E2022-ITG.

### 8. Business rules
| ID | Rule | Source |
|---|---|---|
| BR1 | Every refusal of the contact check writes exactly one decision entry, and every send that passed the check writes exactly one: a refusal and a send each leave one entry and no more | Legacy RWB-E2-022 AC3, AC10, BR1, BR7; FSD P7 v3 A2.2; REQ-OCC-005 |
| BR2 | The entry of a refusal carries decision code "X6" and final call "contact refused" | Legacy RWB-E2-022 AC3; BR-P7-002; DP-07 |
| BR3 | Every entry is hash chained — a `chain_seq`, a `prev_hash` equal to the previous entry's `entry_hash` (64 zeros for the first) and an `entry_hash` equal to the SHA-256 of the entry's canonical form — and the ingest of the shared topic is continuous Kafka inside the completeness target of slide 28, with JOB-14 at 02:00 and the daily seal the baseline's | REQ-DRI-003; FSD P7 v3 AC-ALT-P7-001-01; Architecture v5 slides 28 and 44 |
| BR4 | The log is append only: an entry is never changed and never deleted, and a correction is a new entry naming the one it corrects in `corrects_entry_id` | REQ-DRI-002; FSD P7 v3 AC-P7-001-01 and A2.1 |
| BR5 | The entry names the case reference, the channel, the rule id and rule version, the reason code, the requesting role and the inputs reference; it never carries the message body, the phone number, the LINE identifier, a contact value, a template body or a party identifier | Legacy RWB-E2-022 section 17; DF-ACE-078; CTL-11; §R7.2 s17 |
| BR6 | A refusal is recorded whole or not at all: a refused append leaves no entry, a second append for the same refusal is refused, and one entry exists under a repeated record because the inbox dedupe and the idempotency key hold and the repeat is counted | Legacy RWB-E2-022 BR7, BR9; FSD P7 v3 AC-EXC-P7-002-03; R-UNI-39, R-UNI-40 |
| BR7 | The decision code, the final call, the reason code and the channel are data rows read at the version in force; none of them is a literal in code | BR-P7-002; TSD P7 v2 T3.2; DP-07; GAP-1274 with ASM-2253 |
| BR8 | The story records and exposes; it sends no message, runs no contact check, merges no template, writes no outbox row, maps no delivery result, and changes no case, deviation, contact point or interaction | Architecture v5 slides 14, 41 and 44; DP-01; DP-18 |
| BR9 | The two reads declare the Decision log right R with the scope applied, are one hop from the gateway-bff composite route and read no table of another service; a role without the right is refused with MSG-P4-002 and a case outside the scope with MSG-P4-003 | TSD P7 v2 T-A.1, T6.1 and T6.2; REQ-ILG-010; DP-11; DP-19 |
| BR10 | A record that lacks its decision code, its final call, its rule id, its rule version, its channel, its case reference or its requesting role is refused with MSG-P7-003 and appends nothing; no entry is written from an assumed value | FSD P7 v3 AC-EXC-P7-002-01 and AC-EXC-P7-002-05 read on this slice; REQ-OCC-005 |
| BR11 | No personal data in the entry, the inputs reference, the event, the audit line, the tests or the logs; the contact point is a token and this service never holds a contact value | Architecture v5 slide 11; legacy RWB-E2-022 section 17; REQ-DRI-001 |
| BR12 | The entry, its chain position, its inbox row and its idempotency row commit in one transaction; a failed append leaves nothing and the fact is redelivered, and a refusal that cannot be recorded does not proceed | Principle 5; R-UNI-39; FSD P7 v3 A2.5; DP-03 |
| BR13 | The rule evaluation stays embedded in the owning service (DP-04) and this service records the rule id and version it is given; the rule packages stay in the registry of this service and no rule is evaluated and no workflow, activity or Schedule is registered on this path | Architecture v5 slides 27 and 44; Template and Rules §R5.5 DP-04, DP-10 |

### 9. State transitions
None for a case, a message, a deviation or a contact point. The states below are the states of an entry of this story, and the entry has no state column of its own: it is appended and then immutable.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | `DecisionRecorded` arrives with decision code "X6" and final call "contact refused" | The code is in LOV-DECISION, the final call is in the list, the rule id and version, the channel, the case and the requesting role are present, and the chain head is known | Appended at the next `chain_seq`, with its `prev_hash`, its `entry_hash`, its inbox row and its idempotency row in one transaction |
| Absent | `DecisionRecorded` arrives with a code or a final call outside its list, or with a value missing, or the store or the chain is unavailable | The record fails the check of BR10, or the append cannot commit | Absent: refused with MSG-P7-003, no chain position used, the fact redelivered, the refusal not completed and an incident raised under R-UNI-39 |
| Appended | The same record arrives again with the same idempotency key | The inbox or the idempotency key holds the entry | Unchanged: the first entry's ID is returned and the repeat is counted |
| Appended | A duplicate append for the same refusal arrives | The first entry of that refusal stands | Unchanged: the second append is refused with MSG-GEN-004 |
| Appended | A delivery result arrives for the reference of the send | A delivery result is not a decision of this service | Unchanged: no entry is appended and no chain position is used |
| Appended | A correction is taken, or an UPDATE or a DELETE is attempted | The correction names the entry it corrects; any caller, including the schema owner, may not change an entry | Appended: a new entry with `corrects_entry_id`; otherwise unchanged, the statement refused by the append-only rule |
| Appended | The daily chain check and the daily seal run | JOB-14 at 02:00 and the seal of the baseline | Sealed: the entry is unchanged and the chain is verified |

The message keeps its own lifecycle and delivery status in `rwb-comms`, the deviation keeps its state in `rwb-deviation`, the consent keeps its state in `rwb-source-data` and the case keeps its state in `rwb-case`; this story changes none of them (BR8).

### 10. Authority
The rights below are the Decision log rights this story applies; TSD P7 v2 T6.1 declares R on the decision log for every role and T6.2 declares the service identities. DP-08 is not in the pattern set of this legacy key, so the declaration sits at gateway-bff on the composite route and this story keeps a local guard that refuses closed when the answer is missing (GAP-1274; ASM-2255).

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Sends the message that produces the record on a case in scope (Case record C) and reads the entries of that case (Decision log R) |
| RW-CONDUCT, Conduct and QA officer | Reads blocked contacts and their entries, one entry and the entries of a case in a date range (Decision log R) |
| RW-COMPLAIN and RW-TEAMMGR | Read the entries of a disputed case and of team cases, including the contact stop from `X1` (Decision log R) |
| RW-AUDIT, internal audit; RW-COMPLY, Compliance and PDPA officer | Read the ledger by case and by date range and one entry with its rule version and its chain fields, and never a contact value, which the entry never carries (Decision log R, scope ALL for audit) |
| SY-DECLOG, decision record writer | Writes the record inside the refusal or the send transaction at the producer and appends it to the ledger here; the append is a service identity's and not a person's. A role outside the matrix, or a case out of the caller's scope, is refused with MSG-P4-002, or 404 with MSG-P4-003 |
| The `rwb-decision` service identity | Consumes the fact, reads its own `rwb_decision` rows, and appends the entry, its inbox row and its idempotency row (DP-02) |
| `rwb-comms` | Owns the contact check, the send, the template check, the outbox, the retry limit of 5 with R-UNI-34, the exception queue, the dispatch, the delivery status and the failed count; this story holds no authority over any of them |
| `rwb-source-data`, `rwb-case`, `rwb-deviation`, `rwb-integration`, `rwb-access` | Own the interaction ledger and the consent, the case and its legal hold, the deviation and its contact stop, the NSS and LINE interface configuration, and the session, role and scope; this story writes none of them, and no approval level from the delegation of authority applies, because a contact decision is not an approval |

The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1274; ASM-2255); the story refers to "the rwb-decision login (DP-02)" and never to the shared legacy login.

### 11. Data
| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001, DF-DEC-002, DF-DEC-003 | `decision_log_entry` | id, case_id (the case reference `RC-2026-000777`), decision_code ("X6", a value of LOV-DECISION) | Write |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id (R-UNI-04, R-UNI-10, R-UNI-20 or R-LIT-03) and rule_version ("UNI-2026.11" for a universal rule) | Write |
| DF-DEC-006, DF-DEC-007, DF-DEC-009 to DF-DEC-011, DF-DEC-013 | `decision_log_entry` | model_version, agent_version, recommendation, approver_user_id, approval_level, override_reason | Not written: no model and no agent takes part in a contact decision, and it proposes nothing, is not approved and is not an override |
| DF-DEC-008 | `decision_log_entry` | inputs_ref (the inputs reference of the record, with the freshness of each input) | Write |
| DF-DEC-012 | `decision_log_entry` | final_call ("contact refused" on a refusal) | Write |
| DF-DEC-014 | `decision_log_entry` | actions (the channel, the reason code and the requesting role) | Write; the container is TSD P7 v2 T3.1 and its content for this record is Not specified in the source documents (GAP-1274; ASM-2252) |
| DF-DEC-015 | `decision_log_entry` | outcome | Not written: the send and its delivery status are `rwb-comms`'s |
| DF-DEC-016 to DF-DEC-018, DF-DEC-028, DF-DEC-029 | `decision_log_entry` | decided_at, prev_hash, entry_hash, chain_seq, corrects_entry_id | Write (corrects_entry_id on a correction only) |
| DF-DEC-030, DF-DEC-031 | `decision_log_entry` | actor_user_id (the service identity of the append) and idempotency_key (the key of the record, e.g. "c0ffee00-0001") | Write |
| DF-CAS-001, DF-CAS-020, DF-CAS-038, DF-CAS-043 | `recovery_case` (P3), `deviation` (S8) | id, legal_hold, deviation_code, contact_stop | Read as a fact of the record, never a table |
| DF-REF-046, DF-REF-047, DF-REF-066 | `template` (P6) | template_code, template_version, channel | Read as a fact of the refusal; the catalog is never read here and no template value is written |
| DF-ACE-075, DF-ACE-077, DF-ACE-078, DF-EXT-015, DF-EXT-017, DF-EXT-018 | contact point behind the P1 contract, `contact_point_ext` (P1) | contact_type, person_key, contact_value, consent_given, verified_at, failed_count | The contact value is never read and never written, and no contact value enters this service; the consent facts are read as facts of the refusal, never a table and never written |
| DF-INT-002 to DF-INT-006, DF-INT-012, DF-INT-028, DF-INT-029 | `interaction` (P1) | case_id, channel, conduct_check, delivery_status, external_ref | Never read and never written: the interaction is `rwb-source-data`'s and the delivery status is `rwb-comms`'s |
| (reference lists), (inbox, idempotency) | reference data (P3); `processed_event`, `idempotency_key` | LOV-DECISION, the final-call list, the reason-code list, LOV-CHANNEL; event_id, consumer, processed_at, the record's key and the first entry ID | The lists through the reference-data contract of DP-07, never a table; the inbox and idempotency rows written |

No row of `recovery_case`, `deviation`, `template`, `contact_point_ext` or `interaction` is copied into `rwb_decision`: the case, the deviation, the consent and the template arrive as facts of the record and the contact value never arrives at all (DP-01, DP-18). The phone number, the LINE identifier, the message body and the party `P-0077` are named in this document as legacy values only and are written in no entry of this story (BR5, BR11). Field IDs are those of the Logical Data Model and Data Dictionary v9; the container of the channel, the reason code and the requesting role inside `actions` is the reading of ASM-2252 and is Not specified in the source documents (GAP-1274; ASM-2252). The trigger `tr_declog_append_only` is a database object of the decision-log store baseline (GAP-1274), not a field or entity of the Logical Data Model or the Data Classification; it is named here as an object only.

### 12. Contract
#### 12.1 REST operations provided
Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. Both paths are the ones TSD P7 v2 T-A.1 carries (API-P7-006 and API-P7-007) and the Ownership Map gives to P7. The request and response field set of a contact entry is Not specified in the source documents (GAP-1274; ASM-2252).

| Method | Path | API ID | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006 | Query: `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page`, `size`; a case with a date range is `caseId` with `from` and `to` | 200 `DecisionLogPage`: `items`, `page`, `size`, `total` | Decision log R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007 | None | 200 `DecisionLogEntry`: `entryId`, `chainSeq`, `caseId`, `decisionCode`, `finalCall`, `ruleId`, `ruleVersion`, `inputsRef`, the channel, the reason code, the requesting role, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId`, `actorUserId` | Decision log R, scope applied | Not applicable, read only |

Errors: 401 no session (messageId Not specified in the source documents (DOR-RWB-P7-E2022-APP-8)); 403 the role lacks the Decision log right (MSG-P4-002); 404 the entry or the case is absent or outside the scope (MSG-P4-003); 422 a query value is outside its list (messageId Not specified in the source documents (DOR-RWB-P7-E2022-APP-8)); 503 the ledger is unavailable (messageId Not specified in the source documents (CG-ALL-7261)) or the authorise answer did not arrive inside the 2 s budget (messageId Not specified in the source documents (CG-ALL-7261)). Every error is an RFC 9457 problem response with `messageId` set. `GET /cases/{caseId}/recommendation` (API-P7-001) and the approval operations API-P7-002 to API-P7-005 and API-P7-008 are P7 operations of the decision center and belong to the other P7 stories of this service; this story declares none of them.

#### 12.2 REST operations consumed
| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access (Architecture v5 slide 14) | The cached role, scope and Decision log right R decision behind the two reads; consumed, faked, one hop with a 2 s timeout and a breaker (DP-11), and in no C row of this story (GAP-1274; ASM-2255) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION with "X6", the final-call list with "contact refused", the reason-code list and LOV-CHANNEL with `SMS` and `LINE`, at the version in force (DP-07); faked |

The five fakes of this slice stand behind those rows and behind the record under test: the **rwb-comms dispatch contract fake** (RWB-P6-E2022-CON) poses the five refusals and the send, the **decision-record library fake** (RWB-PLT-E1027-CON) supplies the append, the chain and the append-only refusal, the **rwb-access fake** answers the authorise call, the **rwb-case reference-data fake** supplies the four lists, and the **central ledger fake** supplies the ledger reference, the completeness reading, the replay of the same fact and the chain head. The record itself arrives on `rwb.decision-record.v1` and not over REST.

#### 12.3 Events published
None. This story publishes no event of its own: the record of a contact decision is a fact of `rwb-comms` on `rwb.decision-record.v1` and the entries are read through the operations of 12.1. `rwb.decision.DecisionRecorded.v1` is published by the owning service of each decision and `rwb-decision` is its consumer, as the event catalogue names it (Architecture v5 slide 42, event 08). The `ApprovalRequested`, `ApprovalDecided` and `RulePackageInForce` events of `rwb.decision.events.v1` belong to the approval and rule-registry stories of this service and are not touched here; no new event is added to that topic and no new topic is created.

#### 12.4 Events consumed
| Event | Topic | Owner | Handler |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 ledger and its shared topic; published by `rwb-comms` for the contact decisions of the SMS and LINE loop | `ContactRecordListener`: inbox dedupe by event ID and by the record's idempotency key, then `ContactRecordAppendService` for the decision code, the final call, the rule id and version, the channel, the reason code, the case reference, the requesting role and the inputs reference |

The fact carries IDs, codes, versions and a reference only; no message body, no phone number, no LINE identifier and no customer value travels on the topic (BR5, BR11). Which fields of the fact this service requires is Not specified in the source documents (GAP-1274; ASM-2252); the reading this story applies is that of ASM-2252. Each consumed fact has its retry topic and its `.dlt` topic on the platform convention (DP-09).

#### 12.5 Workflows and activities
None. The append is a transactional write on the consumer path and not a workflow step; the handler is a Kafka consumer with the inbox of DP-09; the contact check and its evaluation (DP-04) run inside the activity of `rwb-comms` and are neither started nor signalled here. This story registers no workflow and no activity on the `rwb-decision` queue and adds none to the workflow kit.

#### 12.6 Schedules
None, and this story creates no Schedule of its own. The legacy JOB-13 decision-log copy at 01:00 is retired: the ingest of `rwb.decision-record.v1` here is continuous Kafka, as Architecture v5 slide 44 states. The daily chain check JOB-14 at 02:00 and the daily seal of the ledger to write-once storage are the decision-log baseline's and cover these entries like any other. No cron entry, no job name and no Temporal Schedule is registered by this story.

#### 12.7 Tables owned
| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The contact entry, its decision code, final call, rule id and version, channel, reason code, requesting role, inputs reference and chain position; append only |
| `approval` | P7 (`rwb_decision`) | Not read and not written: a contact decision is not an approval |
| `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` | P7 (`rwb_decision`) | The registry stays here, but nothing of it is read on this path: the evaluation is embedded in the owning service (DP-04) |
| decision record (local library), `outbox_event`, `processed_event`, `idempotency_key` | P7 rows in the producer's schema through the decision-record path; PLT library created in `rwb_decision` | The local write of DP-03 inside the refusal or the send transaction with its hash chain, and the inbox and idempotency rows of an append (DP-09) |

Not owned and never read: `interaction` and `contact_point_ext` (P1), `recovery_case` and the reference lists (P3), `deviation` (S8), `template` and `merge_field` (P6), `interface_config` (P2), `role`, `permission`, `masking_rule` and `delegation_limit` (P4). No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes
| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-comms dispatch contract fake | RWB-P6-E2022-CON | The five refusals with their records: the contact stop from `X6` lost contact with MSG-P6-001 naming "X6 Lost contact", the contact stop from `X1` with contact stop on with MSG-P6-001 naming "X1 Dispute or complaint", no consent with MSG-P6-002 naming "SMS", the legal hold with MSG-P3-004, the withdrawn `SMS-REMIND` with MSG-P6-003; the send of channel `SMS` accepted with reference "NSS-7781", conduct check `PASSED` and delivery status `DELIVERED`; the send of channel `LINE` with `LINE-REMIND` and delivery status `READ`; the 503 with MSG-P7-003 of a refusal whose record was not written |
| rwb-case reference-data fake | RWB-P3-E1043-CON | LOV-DECISION with "X6", the final-call list with "contact refused", the reason-code list and LOV-CHANNEL with "SMS" and "LINE", at the version in force; an unreadable answer beyond 2 s |
| rwb-access fake | The P4 authorise contract of Architecture v5 slide 14 | The allow answer for `RW-CASEOWN`, `RW-CONDUCT`, `RW-COMPLAIN`, `RW-TEAMMGR` and `RW-AUDIT` with the Decision log right R and the case in scope; MSG-P4-002 for a caller without the right; case `RC-2026-000778` outside the scope for MSG-P4-003 |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the idempotency key "c0ffee00-0001", and a forced failure for AC7 |
| central ledger fake | The ledger side of `rwb.decision-record.v1` | The ledger reference of the entry, the completeness reading of the ingest, the replay of the same fact and the duplicate append of AC9, and the chain head AC7 asserts against |

Each fake is replaced by the real service as its own story lands, without a change to the scenarios.

#### 12.9 Call-type summary
| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 2 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the authorise answer and the `rwb-case` reference-data read consumed, one hop and 2 s with a breaker per downstream |
| Kafka | Published 0, consumed 1 | `rwb.decision-record.v1` consumed with its retry and `.dlt` topics; no event published and no new topic |
| Temporal | None | No workflow, no activity and no Schedule; the evaluation is `rwb-comms`'s activity and the chain check is the baseline's |
| File | None | No file input and no file output; the daily seal to write-once storage is the baseline's, and no document, message or snapshot passes through this story |

### 13. Solution plan
**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `log/contact`, Java package `th.co.scb.ace.workbench.recovery.decision.contact`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | The monolith base path | `/api/recovery/decision/v1` | none |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Which pattern has an instance here: DP-03 is the record itself — the append through the decision-record path, the `prev_hash` and `entry_hash` chain, the append-only rule and the shared topic, with its H RWB-PLT-E1027-CON. DP-01 is the boundary — the entry lives in `rwb_decision` and the interaction, the contact point, the case, the deviation and the template are never read as tables. DP-07 is the four lists read with the version in force; DP-09 is the inbox dedupe and the idempotency row of an append; DP-11 is the one hop with a 2 s timeout and a breaker on the authorise call and the reference-data read; DP-19 is the gateway-bff route of the two reads. DP-05, DP-10 and DP-18 have an instance only as an absence: no ACE view and no ACE table is read and the phone number and the LINE identifier never enter; the legacy JOB-13 copy becomes continuous Kafka with no Schedule (12.6); the interaction ledger is `rwb-source-data`'s and this story holds no ledger entry. The platform H dependencies of the DP table — H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON and H RWB-PLT-N001-CON — and the C dependencies of the published contracts of other services — C RWB-P3-E1043-CON and the authorise contract of P4 — are not in the metadata rows of this story, which name None and RWB-P6-E2022-CON; they are the dependencies the DP table adds and are recorded in GAP-1274 and ASM-2255. None blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and published contracts of `rwb-case` and `rwb-access`, built against their fakes.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ContactRecordListener | Kafka consumer with the inbox | Reads `DecisionRecorded` on `rwb.decision-record.v1`, deduplicates by event ID and by the record's idempotency key, keeps the "X6" contact facts and hands them to the appender |
| ContactRecordAppendService | Service | Checks the decision code, the final call, the rule id and version, the channel, the case reference and the requesting role, and writes the entry, its chain position, its inbox row and its idempotency row in one transaction (BR2, BR10, BR12) |
| ChainHasher | Service | The canonical form of an entry and its SHA-256, the first `prev_hash` of 64 zeros and the `prev_hash` of every later entry (BR3) |
| DecisionLogQueryController, DecisionLogQueryService, DecisionLogRepository | Controller, service, repository | The two operations of 12.1 with the declared right, the scope and the paging; the row shape of a contact entry; `decision_log_entry` insert only with its search indexes and idempotency key |
| ReferenceListClient | Client | LOV-DECISION, the final-call list, the reason-code list and LOV-CHANNEL through DP-07 with the version in force |
| AuthoriseClient | Client | The cached authorise answer of `rwb-access` behind the two reads, one hop with a 2 s timeout and a breaker (DP-11) |

**Database, configuration and reference data**

- Writes `decision_log_entry`, its inbox and idempotency rows, all in schema `rwb_decision`; reads no other schema (DP-01). The table, its columns of TSD P7 v2 T3.1, the trigger `tr_declog_append_only`, the missing grant and the unique key on the idempotency key belong to the decision-log store baseline and are not rebuilt here (GAP-1274). One migration step in the per-service Flyway sequence (DP-15, through RWB-PLT-E1044-CON): `V2022_1__decision_log_contact_index.sql` adds `ix_declog_contact_case ON decision_log_entry (case_id, decision_code, decided_at)`, indexed on the field decided_at in descending order, for the case-and-date search; the index name is Not specified in the source documents (GAP-1274; ASM-2252).
- LOV-DECISION with "X6", the final-call list with "contact refused", the reason-code list and LOV-CHANNEL with `SMS` and `LINE` are reference data read through DP-07 with the version in force (BR7). The rule version labels are the ones the owning service returns; "UNI-2026.11" is the legacy value of the P7 baseline for a universal rule and the label of R-LIT-03 is Not specified in the source documents (GAP-1274; ASM-2254). The page-size bound and the 5-minute completeness target are parameters of their owners whose names are Not specified in the source documents (GAP-1274; ASM-2255), and no feature switch of this story's own is named by a source; the send switch is `rwb.comms.sms-line` of RWB-P6-E2022-APP.

**Build steps**

1. `DecisionLogRepository` and the index step; test the search by case and date range and the single read, and that an INSERT outside a transaction is refused (AC11). Then `ChainHasher` and the canonical form: `chain_seq`, `prev_hash` from the previous entry, the first `prev_hash` of 64 zeros and `entry_hash` as the SHA-256 of the canonical form (AC1, AC8).
2. `ContactRecordListener` with the inbox and the dedupe by event ID and idempotency key, and `ContactRecordAppendService` with the checks of BR10 and the fail-closed transaction; test the replay of the same fact (AC9) and the forced failure of AC7 with the chain position the refused write does not use.
3. The append-only rule with the trigger and the grant, the four statements of AC8 refused and the audit line written. Then `ReferenceListClient` with the version in force, and the refusal rather than an assumed code, final call, reason code or channel (BR7, X9).
4. `DecisionLogQueryController` and `AuthoriseClient` against their fakes; tests for AC10, AC11, MSG-P4-002 and MSG-P4-003 (TC-E2-022-13), then the contract-fake run of the whole slice from Day 1 and the boundary test: no write outside `rwb_decision` (the other schemas are those of section 12.7), and no message body, phone number, LINE identifier, contact value or template body in any entry, event payload or log line (AC5, AC12).

**Done when.** The tests of section 16 pass, the chain of a SIT day verifies from the first entry with no break, each of the five refusals leaves one entry naming its rule and version, a send leaves one entry beside it, a refusal whose record cannot be written leaves none and does not consume a chain position, a repeated record leaves one entry, both reads answer inside the 2 s budget of the frame, and no message, case, deviation or contact point was changed by this story.

### 14. Validation and messages
| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | A contact record cannot be appended, or the record lacks a value the entry requires | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The record path, on the append; the send answers 503 and nothing leaves |
| MSG-GEN-004 | A second append arrives for the same refusal | Someone else changed this record. Reload it to see their change. | This story, on the duplicate append of AC9 |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of the read |
| MSG-P4-003 | The case or the entry is outside the caller's scope | This case is not in your scope. | This story, through the authorise answer of the read |
| MSG-GEN-006 | The authorise answer or a reference list does not arrive inside the 2 s budget | {system} is not available. Try again in a few minutes. | This story, on the read path and on the append path |
| MSG-P6-001 | A contact stop applies | Contact with this customer is stopped for {reason}. | `rwb-comms` on the refusal; this story asserts it and never rewrites it |
| MSG-P6-002 | No consent for the channel | The customer has not consented to {channel}. Use another channel. | `rwb-comms` on the refusal; this story asserts it and never rewrites it |
| MSG-P6-003 | The template is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. | `rwb-comms` on the refusal; this story asserts it and never rewrites it |
| MSG-P3-004 | A legal hold is on the case | This case is on hold for {deviation}. The prescription date is still {date}. | `rwb-case` through the refusal of `rwb-comms`; this story asserts it and never rewrites it |

MSG-P6-001, MSG-P6-002, MSG-P6-003, MSG-P3-004 and MSG-P7-003 are copied unchanged from RWB-E2-022 section 14, and MSG-P4-002, MSG-P4-003 and MSG-GEN-006 from the P7 baseline. The message id set of this slice beyond these nine has no source and is carried in GAP-1274 with ASM-2255. The {reason} of MSG-P6-001 is the reason code as the data holds it ("X6 Lost contact", "X1 Dispute or complaint").

Delivery shape: every error is an RFC 9457 problem response with `messageId` set to the ID above, `detail` carrying the text with its placeholders filled, and `instance` naming the request. The status mapping is the legacy one: 403 with MSG-P4-002, 404 with MSG-P4-003, 409 with MSG-GEN-004, 422 with MSG-GEN-001 of the send, and 503 with MSG-P7-003 on the record path.

### 15. Screens and states
No screen is built in this story. The two reads are consumed by SCR-38 Decision log query, which searches the log by case, rule, approver and date with export, and by the auditor's view of the ledger; both are reached through the gateway-bff composite route of DP-19 and are another story's. SCR-03 Case record and SCR-04 Case timeline stay `rwb-comms`'s, and this story feeds neither of them.

| Where | State | What the reader sees |
|---|---|---|
| SCR-38 Decision log query (P7) | List | The "X6" entries of the case in decidedAt order, each with its final call, its rule id and version, its channel, its reason code and its requesting role |
| The entry read | One entry | The same row with its inputs reference, its `decidedAt`, its `prevHash` and its `entryHash`, and a correction beside the entry it corrects |
| The read | 403, or 404 | MSG-P4-002 for a caller without the right, MSG-P4-003 for a case outside the scope; no row is returned |
| SCR-03 Case record (rwb-comms, not built here) | Loading | As Screen Specifications v1 SCR-03 gives it (CG-ALL-7266) |
| SCR-03 Case record (rwb-comms, not built here) | Empty, error, no access | Not specified in the source documents (CG-ALL-7266) |
| SCR-04 Case timeline (rwb-comms, not built here) | Loading | As Screen Specifications v1 SCR-04 gives it (CG-ALL-7267) |
| SCR-04 Case timeline (rwb-comms, not built here) | Empty, error, no access | Not specified in the source documents (CG-ALL-7267) |
| SCR-38 Decision log query (P7) | Loading | As Screen Specifications v1 SCR-38 gives it (CG-ALL-7268) |
| SCR-38 Decision log query (P7) | Empty, error | Not specified in the source documents (CG-ALL-7268) |

No screen shows a phone number or a LINE identifier: the record carries neither. A panel or screen id for showing a contact entry beside the message on SCR-04, and the field list of SCR-38, are Not specified in the source documents (GAP-1274; ASM-2252); the field list and the composite route specification belong to RWB-PLT-N001-CON and to the story that owns SCR-38.

### 16. Test cases
| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-022-01 | AC6, BR1; legacy Covers "AC1, BR1, BR4, BR8" | Contract | P-0077 MOBILE consent GIVEN; NSS stub reference NSS-7781; the record of the send on rwb.decision-record.v1 |
| TC-E2-022-02 | AC6, BR1; legacy Covers "AC2, BR4" | Contract | P-0077 LINE consent GIVEN; LINE OA stub delivered and read; the record of the LINE send |
| TC-E2-022-03 | AC1, BR2, BR3; legacy Covers "AC3, BR3" | Component | Open X6; record with decision code "X6" and final call "contact refused" |
| TC-E2-022-04 | AC2, BR2; legacy Covers "AC4, BR2" | Component | Open X1 with contact stop; channel LINE |
| TC-E2-022-05 | AC3, BR7; legacy Covers "AC5, BR4" | Component | MOBILE consent WITHDRAWN; rule R-UNI-10 |
| TC-E2-022-06 | AC5, BR7; legacy Covers "AC6, BR8" | Component | SMS-REMIND TH v1 Withdrawn; rule R-LIT-03 |
| TC-E2-022-07 | AC6, AC9; legacy Covers "AC7, BR6" | Contract | Notification path stub unavailable for 6 attempts; no record reaches the topic for a send that stayed queued, and the retry limit with R-UNI-34 is rwb-comms's (NFR-026: three retries per item, then the exception queue) |
| TC-E2-022-08 | AC6, BR1; legacy Covers "AC8" | Unit | NSS result FAILED, failed count 0; the delivery result appends nothing and uses no chain position |
| TC-E2-022-09 | AC9, BR6; legacy Covers "AC9, BR9" | Component | Same Idempotency-Key "c0ffee00-0001" twice |
| TC-E2-022-10 | AC7, BR12; legacy Covers "AC10, BR7" | NFR | Open X6; decision log stubbed unavailable; 503 with MSG-P7-003, nothing sent, incident under R-UNI-39 |
| TC-E2-022-11 | AC4, BR2; legacy Covers "AC11, BR5" | Component | Legal hold true; rule R-UNI-20 |
| TC-E2-022-12 | AC1, AC11; legacy Covers "AC12" | Component | No channel; the send is refused with 422 and MSG-GEN-001 by rwb-comms and no entry is appended |
| TC-E2-022-13 | AC10, AC11, BR9; legacy Covers "Access" | Component | RW-PHONECOL reads the decision log; refused with MSG-P4-002 |
| TC-E2-022-14 | AC7, BR12; legacy Covers "Principle 5" | NFR | Decision log write forced to fail on 10 refusals; none recorded as sent |
| TC-E2-022-15 | AC5, AC12, BR9, BR11; not in legacy RWB-E2-022 | Component | A write to a table of section 12.7 outside `rwb_decision`, and a message body, phone number or LINE identifier offered to an entry; each refused and nothing written |
| TC-E2-022-16 | BR10; not in legacy RWB-E2-022 | Component | Record of a refusal without its final call; a message ID Not specified in the source documents (NEWAC-RWB-P7-E2022-APP-AC13) naming the missing field; nothing written |
| TC-E2-022-17 | BR13; not in legacy RWB-E2-022 | Component | Rule package offered to the record path; no rule evaluated and no workflow, activity or Schedule registered on the path |
| TC-E2-022-18 | AC13, BR10, BR11, BR13; not in legacy RWB-E2-022 | Component | Record without its final call; record carrying a message body, phone number or LINE identifier; rule package offered to the record path; each refused or not appended, nothing written |
| TC-E2-022-19 | AC14, BR9; not in legacy RWB-E2-022 | Component | No valid credentials on GET of one entry and on the list; 401 and no entry returned |

The fourteen legacy test cases of RWB-E2-022 are kept in their legacy order and each is answered here on the record side: the entry, its rule id and version, its chain, its two reads and its refusals. The send, the conduct check, the template status, the retry limit of 5 with R-UNI-34, the exception queue, the delivery status `FAILED` and the message history are the contract fakes' and their own services'. The legacy level System maps to Contract or Component as the row shows, Access to Component and Resilience to NFR. The `-ITG` copies of these cases end in `-ITG` and belong to RWB-ITG-E2022-ITG. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails
- No business value in code: the decision code, the final-call list, the reason-code list, the channel list, the page-size bound, the completeness target and the message ids are reference or parameter rows, and the rule ids and versions are facts of the owning service; nothing of them is a constant here.
- No personal data in the entry, the inputs reference, the event, the audit line, the tests or the logs: the case reference, the channel, the reason code, the rule id and version, the requesting role, the hashes and the dates only. The message body, the phone number, the LINE identifier and the contact value stay in `rwb_comms`, `rwb_source_data` and the ACE notification path (BR5, BR11).
- No cross-schema read and no cross-service write: the interaction and the consent are P1's, the case is P3's, the deviation is S8's, the template is P6's, the interface configuration is P2's and the role and scope are P4's; each is reached through its contract and none is copied (DP-01, DP-18). ACE data only through the owner's contract or the owner's `v_ace_*` views, and this story reads no ACE table and no ACE view, because the contact point never enters it (DP-05).
- One appender and no mover: this story changes no message, case, deviation, contact point or interaction, so a decision record can never send a message or clear a stop (BR8).
- No entry without its record and no record without its decision: the entry, its chain position, its inbox row and its idempotency row commit in one transaction, and a refusal whose record cannot be written is not completed, with incident under R-UNI-39 (BR12).
- Append only and hash chained: no UPDATE and no DELETE on `decision_log_entry`, a correction is a new entry with `corrects_entry_id`, and the chain is verifiable from `chain_seq` 1; the inbox dedupe, the idempotency key and the refusal of a duplicate append make a second entry impossible (BR3, BR4, BR6).
- One base and one topic: `/api/recovery/decision/v1` and `rwb.decision-record.v1` with `rwb-decision` in namespace `rwb-recovery`; no monolith base and no other service's base or topic is declared here as this service's own.
- One hop and 2 s with a breaker per downstream on the authorise call and the reference-data read; an unreadable list refuses the append rather than writing an assumed value (DP-11).
- The rule evaluation stays embedded in the owning service and this story loads no rule model and calls no Drools runtime on any path (DP-04, BR13).

### 18. Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-004 | Messages are sent by SMS and LINE through the bank's channel platforms, with the result recorded on the case | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | R-UNI-33, R-UNI-34, R-UNI-40 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-07, TC-E2-022-08, TC-E2-022-12 |
| REQ-OCC-005 | Every outbound contact carries a conduct check result, and a contact that fails the check is held | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04, FEAT-OCC-05 | 06 to 10 Recovery case processes | R-UNI-04, R-UNI-05, R-UNI-20, R-DEV-16, R-UNI-39 | TC-E2-022-03, TC-E2-022-04, TC-E2-022-10, TC-E2-022-11, TC-E2-022-14 |
| REQ-OCC-006 | A customer who withdraws consent for a channel stops receiving on that channel, and statutory notices continue | Business Requirements Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 06 to 10 Recovery case processes | R-UNI-10 | TC-E2-022-05 |
| REQ-ILG-010 | Letters, messages and calls dispatched by the Workbench write their result to the ledger, including proof of delivery where it returns | Business Requirements Epic 2, section 4 | FEAT-ILG-07 | 06 to 10 Recovery case processes | R-UNI-34 | TC-E2-022-01, TC-E2-022-02, TC-E2-022-08, TC-E2-022-13 |
| REQ-DRI-006 | No component calls a system of record directly; data leaves through paths ACE already has | Business Requirements Program, section 5.6; Epic 2, sections 3.6 and 4 | FEAT-OCC-03, FEAT-OCC-04 | 13 Manage documents and correspondence | No direct call to NSS or LINE OA; only the ACE notification path | TC-E2-022-01, TC-E2-022-02, TC-E2-022-07, TC-E2-022-15 |

| Legacy reference | Where it is kept |
|---|---|
| The contact stop from a lost contact and its decision entry "X6" with final call "contact refused" (legacy AC3, X1), the contact stop from a dispute or complaint (legacy AC4, X2), no consent with `WITHDRAWN` (legacy AC5, X3), the legal hold (legacy AC11, X9) and the withdrawn template (legacy AC6, X4) | Sections 1, 3, 4, 7 (AC1 to AC5), 8 (BR1, BR2, BR7), 9, 14 |
| The decision log write that fails on a refusal, MSG-P7-003 and rule R-UNI-39 (legacy AC10, X8) | Sections 5 (X3, X10), 7 (AC7), 8 (BR12), 14 |
| The retry limit of 5, rule R-UNI-34, the exception queue, the delivery status `FAILED` and the message history, which stay with rwb-comms | Sections 1, 12.4, 16, 19 |
| Templates `SMS-REMIND` and `LINE-REMIND` in `TH` at version 1, channels `SMS` and `LINE`, case `RC-2026-000777`, owner `CO-0201`, party `P-0077`, reference "NSS-7781", Idempotency-Key "c0ffee00-0001" | Sections 3, 7, 11, 16 |
| Rule ids R-UNI-04, R-UNI-05, R-UNI-10, R-UNI-20, R-LIT-03, R-DEV-16 and the version label "UNI-2026.11" | Sections 4, 8, 13, 16 |
| Messages MSG-P6-001, MSG-P6-002, MSG-P6-003, MSG-P3-004, MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-GEN-004 and MSG-GEN-006 | Section 14, exception paths |
| Legacy key RWB-E2-022, story RWB-P7-E2022-APP, contract RWB-P6-E2022-CON, test cases TC-E2-022-01 to TC-E2-022-14, patterns DP01, DP03, DP05, DP07, DP09, DP10, DP11, DP13, DP18, DP19 | Metadata, sections 1, 3, 12, 13, 16 |

The record side of REQ-DRI-001, REQ-DRI-002, REQ-DRI-003, REQ-DRI-005 and REQ-DRI-012 is met by the append, the chain, the refusal of an unrecorded action and the two reads; those requirements are carried in full by the other P7 stories of this service, and the rest of the ledger, the approvals and the rule registry belong to them too.

### 19. Out of scope
- The NSS and LINE OA dispatch, the conduct check itself, the template check, the merge, the outbox, the retry limit of 5 with rule R-UNI-34, the exception queue, the delivery status on the interaction and the message history: `rwb-comms` (P6) in RWB-P6-E2022-APP, RWB-P6-E2022-CON and RWB-P6-E2022-OPS.
- AC1, AC2, AC4, AC7, AC8, AC9, AC11 and AC12 of the legacy key as journeys, and the cross-service harness with its evidence: RWB-ITG-E2022-ITG.
- The interaction ledger, the delivery status and the message history on the case timeline, the consent, the contact point, its verified flag and its failed count, and the customer record: rwb-source-data (P1) under DP-18, RWB-P1-E2022-APP and RWB-P1-E1066-CON.
- The case, its legal hold flag, the case list and the reference data; the deviation and the contact stop: rwb-case (P3) with RWB-P3-E1035-CON and RWB-P3-E1043-CON, and rwb-deviation (S8) with its `DeviationRaised` and `DeviationCleared` events.
- The NSS and LINE interface configuration and the ACE notification path, and the session, the role, the scope and the Decision log right behind the two reads: rwb-integration (P2) with the ACE common module (INT-17, INT-18), and rwb-access (P4) with RWB-P4-E2022-APP and RWB-P4-E1037-CON.
- The rule package registry, the rule authoring, the four-eyes approval and the RulePackageInForce publication: the rule-registry stories of this service; this story neither evaluates nor publishes a rule.
- The general ingest of every other decision code into the ledger, the append-only table itself, the daily chain check JOB-14 at 02:00 and the daily seal, and the retired data-lake copy with JOB-13 and lake retention: the decision-log baseline of this service (DP-17).
- SCR-38 Decision log query as a built screen, the SCR-04 panel and the composite route, the `-ITG` copies of the test cases and the cross-service harness, and the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability: the screen stories and RWB-PLT-N001-CON, RWB-ITG-E2022-ITG, and an OPS story of this legacy key.
