# RWB-P7-E2032-APP TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-P7-AK |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2032-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-032 for rwb-decision, the decision record of a TDR offer suggestion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E2032-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the TDR offer suggestion that rwb-agent obtains through the model gateway recorded as one append-only, hash-chained decision record of code D5 that names the model version in force, the inputs it was given and the suggested terms, and readable afterwards in the decision ledger**, so that **the treatment record holds what was suggested next to what was offered, and the bank can show which model version suggested it and that no suggestion exists without its record**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-032:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- One deliverable and nothing else: the D5 decision record of one offer suggestion. It takes the facts of one suggestion, validates the code and the final call against their lists, appends one `decision_log_entry` in `rwb_decision` with the hash link of the record before it, writes the outbox row of the shared topic in the same transaction, answers with the record reference, and serves the record back on the two decision-log reads under the Decision log right and the case scope.
- The record is written through the decision-record path of DP-03 and never through another service's table. The record, its chain link and its outbox row commit together or not at all (R-UNI-39), and the row is never updated and never deleted (REQ-DRI-002).
- The agent runtime is not here. The model gateway, the `TDR_OFFER` policy and its review date, the masked inputs, the output schema "tdr-offer-v1", the 60 second timeout, the mode (OFF or L1), the agent run, the suggestion returned to the treatment, the feature flag `rwb.agent.tdr-suggestion` and the suggestion area of SCR-14 stay in `rwb-agent` (P10, RWB-P10-E2032-APP and RWB-P10-E2032-CON). The treatment record, its type and its offer fields stay in `rwb-treatment` (S2). The role, the scope, the masking policy and the authorise answer stay in `rwb-access` (P4).
- The legacy decision-log mapping is carried unchanged: case ID, decision code "D5", the model version, `agent_version` null, the masked inputs snapshot as the inputs reference, the suggestion as the recommendation, final call "SUGGESTION_RECORDED", and the actions {"treatmentId", "agentRunId"}.
- The legacy behaviour carried into the decision service is unchanged: a suggestion is returned only after its record is written (BR3, R-UNI-39, CTL-06), one record per treatment under the key "TDR_OFFER:<treatmentId>" (BR5, R-UNI-40), and no suggestion and no record when the model is out of service, times out or fails its check (BR2, BR4).
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-2403; ASM-3997); this story uses the phrase "the `rwb-decision` login (DP-02)" and never the shared monolith login.

### 2. Business rationale

The restructuring officer builds each restructure offer by hand from the balance, the arrears and the payment history. When the TDR team's offer-suggestion model is in service, its suggestion must appear on the treatment record and must be recorded with the model version (REQ-DRI-001), so that the treatment record holds what was suggested next to what was offered (REQ-CHO-006). The suggestion is advice and the officer decides the offer in every case, but the audit answer depends on the record and not on the panel: without it the bank cannot say which model version produced the suggestion the officer saw, cannot reproduce it (NFR-033), and cannot answer an audit or regulatory request (NFR-036).

Under Architecture v5 the ledger is `rwb-decision`'s (slides 14, 20 and 41): every service writes its own decision record locally and publishes `DecisionRecorded` on `rwb.decision-record.v1`, and `rwb-decision` holds the central ledger. The realignment changes the mechanism, not the business rule: the `DecisionLogWriter` of the monolith becomes the local decision-record library and the shared topic of DP-03, hash-linked to the record before it; the decision code and the final call become reference data read with the version in force (DP-07); the record event becomes a CloudEvent with an outbox and an inbox (DP-09); the in-process call becomes a REST contract with a mock, one hop and a 2 s timeout (DP-11), so `rwb-agent` can build against this service before it is live. The body of the suggestion — the account read through the ACE views and the policy parameters — stays with its owners (DP-05, DP-06).

This story carries REQ-DRI-001 for the model-version half and the record half of REQ-CHO-006: identifiers, versions, a code, a final call and the suggested terms, and no name, e-mail address, mobile number, national identity number or account number.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P10-E2032-CON | The published agent contract: the run read this story consumes for the model code, the model version, the status, the fallback, the guardrail result, the suggestion terms, the treatment and case reference and the masked inputs snapshot, and the append operation of `rwb-agent` whose transaction this append is the first step of. The request and answer shape of the append is Not specified in the source documents (GAP-2403; ASM-3997), and the fact set this story assumes is that of ASM-3999 |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the hash link, the chain sequence and the outbox row in one transaction |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION with the code D5 and the final-call list with SUGGESTION_RECORDED, with the version in force |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameters client library and the `rwb-case` parameters contract (DP-06), held as a baseline only: the `TDR_OFFER` policy values stay in `rwb-agent` and this story reads none of them |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one `DecisionRecorded` fact per record, relayed once |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which the ledger reads are reached; this story adds no route |
| The authorise answer of `rwb-access` and the case read of `rwb-case` | The Decision log right R and the scope of the reader, and the owner, team, region and product group the scope filter is applied to; both are consumed on their published contracts or their fakes, are not rows of the metadata, and are carried in GAP-2404 |

Business preconditions carried from RWB-E2-032 (legacy sections 3 and 4):

- Policy "TDR_OFFER" version "P1" has mode "OFF" and review date 2027-02-28 until the TDR team deploys the model; version "P2" with mode "L1", the model code, model version "TDR-OFFER-1.0", output schema "tdr-offer-v1" and timeout 60 seconds is loaded by RW-COE and approved by RW-RISK (legacy section 3).
- Restructure treatment "T-1001" is open on case "RW-2026-001001", and the account has principal outstanding 1,250,000.00 baht and 120 days past due (legacy section 7 Background).
- The officer holds RW-RESTRUCT and reads the record of a case in scope (legacy section 10); the scope decision itself is `rwb-access`'s and `rwb-case`'s and this story only applies the answer.
- A suggestion is one suggestion per treatment, key "TDR_OFFER:<treatmentId>" (legacy BR5).
- No build dependency. Day 1.

### 4. Flow

1. `rwb-treatment` (S2): the restructuring officer opens a restructure treatment on case "RW-2026-001001" and asks `rwb-agent` for a suggestion.
2. `rwb-agent` (P10): reads the `TDR_OFFER` policy in force; when the mode is OFF it returns no suggestion, makes no call and sends nothing to this service (AC2).
3. `rwb-agent` (P10): otherwise assembles the masked inputs, calls the TDR model through the model gateway with the policy timeout, checks the answer against "tdr-offer-v1", and keeps the suggestion and the run.
4. `rwb-agent` (P10): as the first step of its suggestion transaction it calls the append of this service with the case reference, the run reference, the treatment reference, the model code, the model version, the input set reference, the suggested terms, the decided time and its idempotency key, and holds the answer.
5. `rwb-decision` `SuggestionRecordController`: validates the shape of the request, the idempotency key and the presence of the case, the run, the model version and the treatment; a missing required fact is 422 with MSG-P7-009 naming the field and nothing is written (X1).
6. `rwb-decision` `SuggestionValidationService`: reads the decision code D5 and the final-call value SUGGESTION_RECORDED through the reference-data contract of DP-07 with the version in force, and refuses a value that is not of its list with 422 and MSG-P7-009 (X1).
7. `rwb-decision` `AgentFactClient`: reads the run through the P10 run read, one hop with a 2 s timeout and a breaker, and takes the model code, the model version, the status, the fallback, the guardrail result and the suggested terms from the owner of the run instead of trusting the caller (ASM-3999); the run reference and the input set reference form the inputs reference of the record.
8. `rwb-decision` `ChainWriter`: takes the last `entry_hash` and `chain_seq` of the ledger under the append lock, computes the entry hash over the canonical form of the new record, and builds the row with `prev_hash` equal to that last hash and `chain_seq` equal to the next number.
9. `rwb-decision` `SuggestionRecordAppendService`, one `RecordAndApply` transaction in `rwb_decision`: the `decision_log_entry` row is inserted with decision code D5, the model version, `agent_version` null, the inputs reference, the suggestion as the recommendation, final call SUGGESTION_RECORDED and the actions {"treatmentId", "agentRunId"}; the outbox row for `DecisionRecorded` on `rwb.decision-record.v1` is written; and the transaction commits. A failure rolls everything back and answers 503 with MSG-P7-003 (X2), and no chain sequence number is consumed.
10. `rwb-decision` `SuggestionRecordController`: answers 201 with the record reference, the chain sequence, the entry hash and the decided time. `rwb-agent` stores that reference as the decision link of its run and commits its own transaction; only then does the suggestion reach the treatment.
11. `rwb-decision` `DecisionRecordOutbox`: the relay of the platform publishes `rwb.decision-record.DecisionRecorded.v1` from the outbox in CloudEvents 1.0 with the record ID as its key; `rwb-decision` itself and `rwb-reporting` consume it (Architecture v5 slide 42, event 08).
12. A reader with the Decision log right R and the case in scope reads the ledger with `GET /api/recovery/decision/v1/decision-log?caseId=…` and one record with `GET /api/recovery/decision/v1/decision-log/{entryId}`, and sees the decision code D5, the model version "TDR-OFFER-1.0", the suggested terms, the final call, the decided time and the two hashes (AC3, AC9, X7, X8).
13. Nothing in this story changes the treatment, the offer, the run or the panel: the officer edits the offer fields as before, and the suggestion is never copied into them (BR7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The append carries a decision code or a final call that is not a value of its list, or no model version | Refused with 422 before anything is written, naming the field; no record, no outbox row and no chain sequence consumed | MSG-P7-009 | AC1 |
| X2 | The record cannot be written: the library fails, the insert fails or the connection is lost | The whole transaction rolls back; no record and no outbox row; the chain stands at its last entry; `rwb-agent` stores no decision link and returns no suggestion, so its transaction never commits; the incident is raised under R-UNI-39 | MSG-P7-003 | AC6, TC-E2-032-10 |
| X3 | The same treatment asks again, or two appends arrive at once | The idempotency key and the unique index give one record; the second call returns the first record with its own ID and the chain gains no second link; the 409 of the panel is `rwb-agent`'s and is not produced here | MSG-GEN-004 (produced by `rwb-agent`) | AC7 |
| X4 | The model is not in service (policy mode OFF) | `rwb-agent` returns no suggestion and sends no append, so no record is written and nothing is refused | MSG-P10-007 (produced by `rwb-agent`) | AC2 |
| X5 | The model does not answer within 60 seconds, or the answer fails the output schema | `rwb-agent` keeps the run TIMED_OUT or GUARDRAIL_FAILED and sends no append, so no record is written | MSG-P10-007 (produced by `rwb-agent`) | AC4, AC5 |
| X6 | The treatment type is not RESTRUCTURE | `rwb-agent` makes no call and no suggestion, so no append arrives and no record is written | None to a user | AC8 |
| X7 | The reader holds no Decision log right, or the request reaches the service without the declared right | 403 with MSG-P4-002 and nothing returned | MSG-P4-002 | AC9, TC-E2-032-09 |
| X8 | The case of the record is outside the reader's scope | 404 with MSG-P4-003 and nothing returned | MSG-P4-003 | AC3 |

A record is never updated and never deleted: a wrong record is corrected by a new record that names the one it corrects in `corrects_entry_id`, so the ledger stays append only (REQ-DRI-002). The record, its chain link and its outbox row are always written together, so a record cannot exist without its event and an event cannot name a record that was not stored.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the agent contract of RWB-P10-E2032-CON, the decision-record library and the reference-data contract of its DP table, and their fakes; no agent runtime, no model gateway, no treatment behaviour and no authorise rule is rebuilt here |
| Negotiable | The code values, the final-call list and the message texts are reference data or the message standard; the story fixes only the one-record-per-suggestion rule, the chain and the fail-closed behaviour |
| Valuable | Every recorded suggestion names the model version it came from, so the treatment record, the audit answer and the model review stand on a stored fact |
| Estimable | One controller, one append service, one validation service, one chain writer, two reads, one migration |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the nine criteria in section 7 runs as an automated test against the contract fakes and the decision-record library, with a fixed clock and a seeded chain |

### 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion model through the model gateway [E3e] — the rwb-decision decision record of an offer suggestion

  Background:
    Given the environment is SIT
    Given restructure treatment "T-1001" is open on case "RW-2026-001001"
    Given the account has principal outstanding 1,250,000.00 baht and 120 days past due

  Scenario: AC1 A recorded suggestion writes one D5 entry (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of treatment "T-1001" with model code "TDR_OFFER", model version "TDR-OFFER-1.0", status "COMPLETED", fallback false, the suggested terms of 84 installments of 18,900.00 baht and the masked inputs snapshot of the run
    Given the rwb-case contract mock returns case "RW-2026-001001" with product group "MORTGAGE"
    When rwb-agent sends the suggestion record for treatment "T-1001" and this service appends it
    Then one decision record exists for case "RW-2026-001001" with decision code "D5", model version "TDR-OFFER-1.0", no agent version, the masked inputs snapshot as its inputs reference, the suggested terms as its recommendation, final call "SUGGESTION_RECORDED" and actions carrying "treatmentId" and "agentRunId"
    Then the answer carries the record reference and the chain sequence that rwb-agent stores as the decision link of its run
    Then the record, its chain link and its outbox row for the decision record event are written in one transaction
    Then the record carries no name, no e-mail address, no mobile number, no national identity number and no account number

  Scenario: AC2 Mode OFF writes nothing and refuses nothing (new, D-RCV-60)
    Given the rwb-agent contract mock returns no suggestion for treatment "T-1001", because policy "TDR_OFFER" version "P1" has mode "OFF" and review date 2027-02-28
    When rwb-agent sends no suggestion record for the treatment and the ledger is read for case "RW-2026-001001"
    Then no decision record with decision code "D5" exists for the case and no chain sequence is consumed
    Then MSG-P10-007 on SCR-14 is rwb-agent's and this story produces no message

  Scenario: AC3 The record is readable with its model version and its inputs (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of treatment "T-1001" with model version "TDR-OFFER-1.0" and the suggested terms of 84 installments of 18,900.00 baht, and that suggestion was recorded
    Given the rwb-access contract mock returns the allow answer on the Decision log right R to the reader who holds RW-RESTRUCT
    When the reader sends GET /api/recovery/decision/v1/decision-log/{entryId} for the record and then GET /api/recovery/decision/v1/decision-log for case "RW-2026-001001"
    Then the single read carries decision code "D5", model version "TDR-OFFER-1.0", final call "SUGGESTION_RECORDED", the inputs reference, the suggested terms, the decided time, the previous hash and the entry hash
    Then the page holds the same record, so the model version and the terms can be read beside the offer on the treatment record

  Scenario: AC4 The model does not answer and no record is written (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of treatment "T-1001" with status "TIMED_OUT" and fallback true, the model stub having been silent for 61 seconds
    When the treatment is asked for a suggestion and the ledger is read for case "RW-2026-001001"
    Then no decision record with decision code "D5" exists for the case and no chain sequence is consumed
    Then the treatment continues and MSG-P10-007 is rwb-agent's own message (R-UNI-32)

  Scenario: AC5 An answer that fails the schema writes no record (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of treatment "T-1001" with status "GUARDRAIL_FAILED", check "SCHEMA" and no suggestion, the model having returned installments -12
    When the ledger is read for case "RW-2026-001001"
    Then no decision record with decision code "D5" exists for the case and nothing is appended

  Scenario: AC6 The decision cannot be recorded and no suggestion is returned (new, D-RCV-60)
    Given the rwb-agent contract mock holds an open suggestion for treatment "T-1001"
    Given the decision-record library refuses the append and raises its unavailable condition
    When rwb-agent sends the suggestion record for that run
    Then the answer is 503 with MSG-P7-003
    Then no decision record and no outbox row exists for the run and the chain stands at its last entry
    Then rwb-agent keeps the run without a decision link and returns no suggestion to the treatment
    Then an incident is raised under R-UNI-39 to the platform administration role

  Scenario: AC7 The same treatment asks twice and gains one record (new, D-RCV-60)
    Given a decision record with decision code "D5" and the idempotency key "TDR_OFFER:T-1001" was recorded for treatment "T-1001"
    Given rwb-agent holds a recorded answer for the treatment and makes no second model call
    When rwb-agent sends the same suggestion again with that idempotency key
    Then one decision record exists for treatment "T-1001"
    Then the answer returns the first record with the same record reference and the chain gains no second link
    Then the refusal with 409 and MSG-GEN-004 is rwb-agent's and is not produced here

  Scenario: AC8 Not a restructure writes no record (new, D-RCV-60)
    Given treatment "T-1002" has type "SETTLEMENT"
    When the treatment is asked for a suggestion and the ledger is read for treatment "T-1002"
    Then rwb-agent makes no model call and sends no append
    Then no decision record with decision code "D5" exists for treatment "T-1002"

  Scenario: AC9 The record is guarded by the Decision log right (new, D-RCV-60)
    Given a decision record with decision code "D5" was recorded for treatment "T-1001"
    Given the rwb-access contract mock returns the refusal on the Decision log right R to the caller, who holds the Treatment and offer right only
    When the caller sends GET /api/recovery/decision/v1/decision-log/{entryId} for that record
    Then the answer is 403 with MSG-P4-002 and nothing is returned
```

These nine criteria are new for the `rwb-decision` slice of RWB-E2-032 and are the decision-record criteria of the key; every value in them is a legacy value of RWB-E2-032 sections 3, 4, 7, 8, 12 and 14 — treatment `T-1001` on case `RW-2026-001001`, the principal of 1,250,000.00 baht at 120 days past due, policy `TDR_OFFER` version P1 mode OFF with review date 2027-02-28, model code `TDR_OFFER` and model version `TDR-OFFER-1.0`, the 84 installments of 18,900.00 baht, the 60 second timeout and the 61 second stub, the answer with installments -12, decision D5, the final call `SUGGESTION_RECORDED`, the key `TDR_OFFER:<treatmentId>`, treatment `T-1002` of type SETTLEMENT, the roles RW-RESTRUCT and RW-RISK and the messages MSG-P7-003, MSG-P4-002, MSG-P10-007 and MSG-GEN-004 — and no new business value is introduced. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key either gives the suggestion on the panel, calls the model gateway, or asserts the agent run, and all three belong to `rwb-agent` (P10). The wording of MSG-P7-003, MSG-P10-007 and MSG-P4-002 is the legacy wording and section 14 repeats it unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A suggestion is returned to the treatment only after its decision record is written, and the append is the first step of the agent run's transaction; when the record cannot be written, no suggestion is returned | Legacy BR3; Principle 5; R-UNI-39; CTL-06; REQ-DRI-001 |
| BR2 | The record carries the decision code D5, a value of LOV-DECISION read with the version in force; the code is data and never a constant of the code | Legacy section 12 (decision_code "D5"); TSD P7 v2 T3.1 (DF-DEC-003); DP-07; ASM-3998 |
| BR3 | The record names the model version of the suggestion, taken from the run and not from the caller, with `agent_version` null because the suggestion is a model output and not an agent output of a prompt | Legacy section 12 (model_version, agent_version null); TSD P7 v2 T3.1 (DF-DEC-006, DF-DEC-007); NFR-033; ASM-3999 |
| BR4 | The inputs reference is the masked inputs snapshot of the run, so the suggestion can be reproduced from the record without the account data entering this service | Legacy section 12 (inputs_ref = masked inputs snapshot); TSD P7 v2 T3.1 (DF-DEC-008); NFR-033; DP-05 |
| BR5 | The recommendation is the suggested terms, and the actions are the treatment reference and the agent run reference; the suggestion is never copied into the offer fields or the treatment status | Legacy section 12 (recommendation, actions); Legacy BR7; TSD P7 v2 T3.1 (DF-DEC-009, DF-DEC-014) |
| BR6 | The final call is SUGGESTION_RECORDED, a value of its list read as reference data; the list is data and never a constant of the code | Legacy section 12; DP-07; ASM-3998 |
| BR7 | One record per treatment: the idempotency key "TDR_OFFER:<treatmentId>" held by a unique key of the ledger makes a second record impossible, and a repeated append returns the first record | Legacy BR5; R-UNI-40; TSD P7 v2 T3.1 (DF-DEC-031); DP-09 |
| BR8 | Mode OFF, a timeout or a failed check gives no suggestion and therefore no record; a treatment that is not RESTRUCTURE is never suggested | Legacy BR2, BR4, BR6; R-UNI-32 |
| BR9 | The record is append only and hash chained: an entry hash over its canonical form, a previous hash equal to the entry hash before it, a sequence number that is never reused, and no update and no delete; a wrong record is corrected by a new record that names the one it corrects | REQ-DRI-002; REQ-DRI-003; TSD P7 v2 T3.1 (DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029) |
| BR10 | The record, its chain link and its outbox row commit in one transaction, and the failure rolls the caller's suggestion transaction back as well | REQ-DRI-005; R-UNI-39; DP-03; MSG-P7-003 |
| BR11 | The ledger is read under the Decision log right R and the caller's scope; the right is `rwb-access`'s to answer and the scope filter is applied to the case read of `rwb-case`; this service holds no role, no scope and no masking rule of its own | TSD P7 v2 T6.1 and T6.2; legacy section 10; the authorise dependency is carried in GAP-2404 |
| BR12 | No personal data in the record, the event, the trail or the logs: case, run and treatment references, a decision code, a version, a final call, the suggested terms, a user reference and dates only | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43; legacy section 17 |
| BR13 | The model, its version, the output schema, the review date and the timeout are policy values of `rwb-agent` and reference data; this story reads none of them and hard-codes none of them | Legacy BR1 and BR2; Template and Rules §R3 default rulings (parameters to P3); DP-06 |

### 9. State transitions

The states below are the states of a decision record of this story. The treatment, the offer, the agent run and the panel are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | An append arrives for a recorded suggestion, with a code and a final call of their lists and a run that answers | The library writes the record, the outbox row and the chain link in one transaction | Appended, with a chain sequence, a previous hash and an entry hash |
| Absent | An append arrives with a code or a final call that is not a value of its list, or without a model version | The validation refuses the request | Absent: 422 with MSG-P7-009 naming the field |
| Absent | The library or the insert fails | The transaction rolls back | Absent: 503 with MSG-P7-003, the chain at its last entry, the caller's run left without a decision link |
| Absent | The same treatment was already recorded | The idempotency key and the unique key hold | Appended: unchanged, the first record returned |
| Appended | A wrong record must be corrected | A person decides the correction | Appended: a new record with `corrects_entry_id` naming the wrong one; the wrong one stays |
| Appended | Any update or delete is attempted | Through the service role or the schema owner | Appended: refused, and the attempt is written to the ACE audit log |

The final call has one value on this path; a later call value is a new reference row and a new record, never an update. The treatment stays where `rwb-treatment` has it and the run and the panel stay as `rwb-agent` has them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, the restructuring officer | Reads the record of a case in scope (Decision log R) and builds the offer from it; the suggestion is advice and the officer decides (legacy section 10, BR7) |
| RW-CASEOWN, the case owner | Reads the record of a case in scope (Decision log R) |
| RW-RISK, RW-COE and RW-AUDIT | Read the ledger under the Decision log right R, as TSD P7 v2 T6.1 fixes it; they take no suggestion and load no policy here |
| SY-AGENT and SY-DECLOG | Append the record on behalf of a suggestion, one hop, under the service identity; they hold no user right and write nothing else |
| The `rwb-decision` service identity | Writes its own `rwb_decision` rows, the outbox row and the chain link, and reads the run through the P10 contract (`rwb-decision` login, DP-02) |
| The decision-record library identity | Writes the record, the hash link and the outbox row in one transaction and publishes on `rwb.decision-record.v1` (DP-03) |
| `rwb-agent` (P10) | Owns the policy, the model gateway, the masked inputs, the output schema, the run, the suggestion returned to the treatment, the flag, the panel and the admin reads; this story holds none of them |
| `rwb-treatment` (S2) and `rwb-access` (P4) | Own the treatment and the offer fields, and the rights, the scope and the masking; this story applies their answers and changes neither |

The authorisation decision is `rwb-access`'s and is consumed as the authorise answer the read declares; the refusal shape stays 403 with MSG-P4-002 and 404 with MSG-P4-003. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-2403; ASM-3997).

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, the value D5 of LOV-DECISION |
| DF-DEC-004 | `decision_log_entry` | rule_id | Not written: a model suggestion is not a rule answer |
| DF-DEC-005 | `decision_log_entry` | rule_version | Not written, for the same reason |
| DF-DEC-006 | `decision_log_entry` | model_version | Write, "TDR-OFFER-1.0" from the run |
| DF-DEC-007 | `decision_log_entry` | agent_version | Write null: the suggestion is a model output and not a prompt output (legacy section 12) |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the masked inputs snapshot reference of the run |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the suggested terms of the run |
| DF-DEC-010, DF-DEC-011 | `decision_log_entry` | approver_user_id, approval_level | Not written: the officer approves the offer on the treatment record and not this suggestion |
| DF-DEC-012 | `decision_log_entry` | final_call | Write, SUGGESTION_RECORDED |
| DF-DEC-013 | `decision_log_entry` | override_reason | Not written on this path |
| DF-DEC-014 | `decision_log_entry` | actions | Write, {"treatmentId", "agentRunId"} |
| DF-DEC-015 | `decision_log_entry` | outcome | Not written by this story |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017, DF-DEC-018 | `decision_log_entry` | prev_hash, entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on a record that corrects an earlier one |
| DF-DEC-030 | `decision_log_entry` | actor_user_id | Write, the service identity |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write, "TDR_OFFER:<treatmentId>" |
| DF-DEC-001 to DF-DEC-031 | decision record | all fields | Read through the two ledger operations |
| DF-AGT-004, DF-AGT-005, DF-AGT-006, DF-AGT-012, DF-AGT-016 | `agent_policy` | model_code, model_version, output_schema_ref, timeout_seconds, review_date | Not read here: the policy stays in `rwb-agent` (legacy section 11, DP-06) |
| DF-AGT-036, DF-AGT-037, DF-AGT-040, DF-AGT-041, DF-AGT-042, DF-AGT-046, DF-AGT-047, DF-AGT-048, DF-AGT-049, DF-AGT-058 | `agent_run` | id, agent_code, model_version, case_id, subject_id, status, fallback, guardrail_result, output, decision_log_id | Read through the P10 run read; the field set of that read is Not specified in the source documents (GAP-2403; ASM-3999) |
| DF-ACC-009, DF-ACE-018, DF-ACE-020, DF-ACE-025, DF-ACE-045, DF-ACE-046 | `v_ace_account`, `v_ace_payment` | principal outstanding, total balance, days past due, interest rate and the payments of 12 months | Not read here: the masked inputs are assembled by `rwb-agent` from the owner of the ACE data (DP-05) |
| DF-CAS-001, DF-CAS-003, DF-CAS-009, DF-CAS-011, DF-CAS-012 | `recovery_case` | id, product_group, owner_user_id, team_code, region_code | Read through the P3 case read, for the scope filter only |
| (inbox) | library table in `rwb_decision` | event_id, consumer, processed_at | Not written: this story consumes no event |
| (outbox) | library table in `rwb_decision` | the `DecisionRecorded` row | Write |

No row of `agent_policy` or `agent_run` is copied into `rwb_decision`: the run facts arrive on the P10 contract and `rwb-agent` stores this story's record reference in its own column. No row of `treatment`, `recovery_case`, `task` or `timer` is written, and no role, scope or masking row is read from `rwb_access`. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two reads are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1; the append on the same collection is the write path DP-03 needs and is Not specified in the source documents (GAP-2403; ASM-3997). The request and answer field set of the three operations is Not specified in the source documents (GAP-2403; ASM-3997).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/decision-log` | Append one decision record for one recorded suggestion: validate, chain and write, then answer 201 with the record; a repeated key answers 200 with the first record | Service identity only, SY-AGENT and SY-DECLOG (TSD P7 v2 T6.1, right C); one hop from `rwb-agent` with a 2 s timeout | Idempotency-Key header, "TDR_OFFER:<treatmentId>", kept on the ledger row |
| GET | `/decision-log` | API-P7-006: search the ledger by case, decision, rule, approver and date, one page at a time | Decision log, right R, scope applied through the authorise answer and the case read of P3 | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one record with its inputs, its model version, its final call and its two hashes | Decision log, right R, scope applied | Not applicable, read only |

The append request this story assumes carries `caseId`, `runId`, `treatmentId`, `modelCode`, `modelVersion`, `inputsRef`, `suggestion`, `idempotencyKey` and `decidedAt`; the status, the fallback, the guardrail result and the suggested terms are read from the run as well, and the caller's copy is never trusted over the run. The DecisionRecord answer carries `id`, `caseId`, `decisionCode`, `modelVersion`, `agentVersion`, `inputsRef`, `recommendation`, `finalCall`, `actions`, `decidedAt`, `chainSeq`, `prevHash` and `entryHash`. Both sets are the placeholder until the contract baseline is agreed (GAP-2403; ASM-3997).

Errors: 401 no session; 403 the role holds no Decision log right (MSG-P4-002); 404 the record or the case is absent or out of scope (MSG-P4-003); 409 the append repeats a key with a different body (MSG-GEN-004); 422 a code, a final call or a required version is not a value it must have (MSG-P7-009); 503 the record was not written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/agent-runs/{runId}` | P10 rwb-agent, on RWB-P10-E2032-CON | The run facts the record names: model code, model version, status, fallback, guardrail result, suggested terms, treatment and case reference and the inputs snapshot reference; faked, one hop with a 2 s timeout and a breaker |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The owner, team, region and product group the scope filter of the ledger read is applied to; faked, one hop |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The cached decision of the Decision log right R and the scope of the reader behind the two reads; faked |

The three operations are the P10, P3 and P4 rows of the Ownership Map and of Architecture v5 slides 14, 16 and 41. Their request and answer shape is Not specified in the source documents (GAP-2403; ASM-3997). The reference-data contract of DP-07 is consumed through its client library for LOV-DECISION and the final-call list; its operation path is not given by any source this story may read and is carried in GAP-2403. DP-08, which would add the guard library and the authorise contract as named dependencies, is not among the patterns of this key, so the authorise answer is consumed against its published contract or its fake and the dependency is carried in GAP-2404, as ASM-4002 reads it.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7, published by this service | entryId | record ID, case ID, decision code D5, model version "TDR-OFFER-1.0", inputs reference, final call SUGGESTION_RECORDED, decided at, chain sequence, entry hash |

The event is written to the outbox in the same transaction as the record and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform (DP-09); the shared topic carries its own name, so the event of the catalogue is published there and not on the service topic. `rwb-decision` itself and `rwb-reporting` consume it, as event 08 of Architecture v5 slide 42 names them. No event carries a name, an e-mail address, a mobile number, an account number or the account data behind the suggestion.

#### 12.4 Events consumed

None. This story consumes no event: the suggestion arrives on the append request and the run facts on the run read. The inbox objects of DP-09 are created in the schema by the service baseline and this story writes none.

#### 12.5 Workflows and activities

None of this story's own. The append is one synchronous service operation inside the caller's unit of work, not a workflow, and the ledger read is a query. `rwb-decision` holds `ApprovalWorkflow` of the workflow kit and its Schedules for other slices of the service; this story starts no workflow, signals none, and registers no activity and no Schedule on the `rwb-decision` queue. The chain check JOB-14 at 02:00 is the decision-log store's and the rule promotion JOB-13 is the rule registry's.

#### 12.6 Schedules

None. The rule promotion JOB-13 and the chain check JOB-14 belong to other slices of this service and run on their own Temporal Schedules; this story adds neither and polls nothing.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The record of the suggestion: the code, the model version, the inputs reference, the recommendation, the final call, the actions, the hashes and the chain sequence; written once and read |
| outbox library table | PLT library, created in `rwb_decision` | The `DecisionRecorded` row (DP-09) |
| `idempotency_key` | PLT library, created in `rwb_decision` | The stored answer of a repeated append (DP-09) |

Not owned and never read by this story: `agent_policy`, `agent_run` and the ACE views (P10 and P1), `treatment` (S2), `recovery_case` (P3), `delegation_limit`, `role`, `permission` and `masking_rule` (P4). The run arrives on its contract, the case on its read and the authorise answer on its own; no foreign key crosses a schema and no row of another service is copied (DP-01). The `approval`, `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` tables are this service's but another story's, and this story writes none of them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-agent contract fake | RWB-P10-E2032-CON | The run of treatment `T-1001` with model code "TDR_OFFER", model version "TDR-OFFER-1.0", status "COMPLETED", the suggested terms of 84 installments of 18,900.00 baht and the inputs snapshot reference; the run of `T-1001` with status "TIMED_OUT" and fallback true; the run with status "GUARDRAIL_FAILED" and check "SCHEMA"; no suggestion for `T-1001` under policy P1 mode OFF; treatment `T-1002` of type "SETTLEMENT"; the request journal for the idempotency key and the ordering assertions |
| rwb-case fake | The P3 case read | Case `RW-2026-001001` with product group "MORTGAGE", owner, team and region; the case-and-scope answer of the reference-data contract for LOV-DECISION and the final-call list (DP-07) |
| rwb-access fake | The P4 authorise call | The allow answer on the Decision log right R for the RW-RESTRUCT reader and the refusal for the caller who holds the Treatment and offer right only (MSG-P4-002) |
| decision-record fake | RWB-PLT-E1027-CON | The append of the local record, the chain sequence allocation and the hash link; the chain verifier over a seeded ledger; a forced failure and an unavailable condition for AC6 and TC-E2-032-10 |

Each fake is replaced by the real service as its contract lands, without a change to the criteria. The decision-record fake stands only for the tests of the chain and of the failure, because the library is the service's own DP-03 baseline.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 3 | `POST /decision-log`, `GET /decision-log` and `GET /decision-log/{entryId}` provided; the run read, the case read and the authorise call consumed, one hop each with the 2 s timeout |
| Kafka | Published 1 event type, consumed 0 | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; nothing consumed |
| Temporal | None | No workflow, no activity and no Schedule registered; JOB-13 and JOB-14 stay with their owners |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger/offersuggestion`, Java package `th.co.scb.ace.workbench.recovery.decision.offersuggestion`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/decision/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the core of the slice: the legacy `DecisionLogWriter` becomes the local decision-record library of this service, which writes the record, the hash link and the outbox row in one transaction and publishes on the shared topic. DP-07 is where the decision code D5 and the final-call list live: both are read through the reference-data contract of `rwb-case` with the version in force and neither is a constant here. DP-11 is the one hop from `rwb-agent` to the append and the one hop back on the run read, each with a 2 s timeout and a breaker. DP-09 is the outbox and the CloudEvents envelope of the one published fact; the inbox objects are part of the service baseline. DP-01 keeps the record in `rwb_decision` alone; DP-13 puts the three operations on `/api/recovery/decision/v1`; DP-19 is the composite route through which the two ledger reads are reached, and this story adds no route and serves no screen of its own.

DP-05 and DP-06 are carried and not used. The account, the arrears and the twelve months of payments are assembled by `rwb-agent` from the owner of the ACE data and reach this story only as the inputs snapshot reference, and the `TDR_OFFER` policy stays a parameter row of `rwb-agent`; the two rows stay in the DP table because the legacy key needs them at its primary slice.

The platform H dependencies of the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-N001-CON) and the two C dependencies that DP-06 and DP-07 bring with them (C RWB-P3-E1042-CON, C RWB-P3-E1043-CON) are not in the metadata rows, which name None and RWB-P10-E2032-CON; they are recorded in GAP-2404 and ASM-4001. None of them blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and published contracts of another service. DP-20, which would name an agent contract of its own, is not among the patterns of the key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuggestionRecordController | Controller | `POST /decision-log` with the shape and idempotency validation, the 201 and 200 answers, and the problem mapping for 401, 409, 422 and 503 |
| SuggestionValidationService | Service | Reads LOV-DECISION and the final-call list with the version in force, and refuses a code, a final call or a missing version with MSG-P7-009 |
| AgentFactClient | Adapter | The run read of RWB-P10-E2032-CON, one hop with a 2 s timeout and a breaker; takes the model version, the status and the suggested terms from the owner of the run |
| ChainWriter | Service | Reads the head of the chain under the append lock, computes the entry hash over the canonical form and builds the previous hash and the sequence number |
| SuggestionRecordAppendService | Service | One `RecordAndApply` transaction: the record, the chain link and the outbox row, or nothing; maps the failure to 503 with MSG-P7-003 |
| DecisionRecordRepository | Repository | `decision_log_entry` in `rwb_decision`, with the unique key of the chain sequence and of the idempotency key |
| DecisionRecordQueryService | Service | The ledger page and the single record, with the scope filter applied to the case read |
| AccessCheckClient, CaseScopeClient | Client | The authorise answer of the Decision log right and the P3 case read behind the two reads |
| DecisionRecordOutbox | Library use | The outbox row of `DecisionRecorded` in the same transaction as the record (DP-09) |

**Database and migrations**

- Writes `decision_log_entry` and the outbox and idempotency objects of the library, all in schema `rwb_decision`; reads no other schema.
- The `decision_log_entry` baseline, its append-only trigger and its grants belong to the decision-log store slice of this service (legacy RWB-E1-008) and are not rebuilt here.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2032_1__decision_offer_suggestion.sql` adds the unique key `ux_declog_idem ON decision_log_entry (idempotency_key) WHERE idempotency_key IS NOT NULL`, the index `ix_declog_case_decided ON decision_log_entry (case_id, decided_at DESC)` for the ledger read of one case, and the check that a D5 record carries a model version. The chain-sequence unique key is the decision-log store's.
- No row is updated and no row is deleted by this story; the update path of the store does not exist and the delete path does not exist.

**Configuration and reference data**

- LOV-DECISION with the code D5 and the final-call list with SUGGESTION_RECORDED are read through the reference-data contract of DP-07 with the version in force; neither is a constant in code (ASM-3998).
- The `TDR_OFFER` policy rows P1 (mode OFF, review date 2027-02-28) and P2 (mode L1, model version "TDR-OFFER-1.0", output schema "tdr-offer-v1", timeout 60 seconds) are rows of `rwb-agent` and are not read or written here (DP-06, ASM-4003).
- The feature flag `rwb.agent.tdr-suggestion` stays with RWB-P10-E2032-APP and never gates the append; a suggestion that reached the gateway always writes its record (ASM-4000).
- The `rwb-decision` login of DP-02, the flyway user and the outbox relay identity are environment configuration and not values of this story.

**Build steps**

1. The migration `V2032_1__decision_offer_suggestion.sql`; test that a repeated idempotency key and a D5 record without a model version are refused (BR3, BR7).
2. `ChainWriter` with the head read, the canonical form and the entry hash; test the seeded chain and the first record with the previous hash of 64 zeros (AC1).
3. `SuggestionValidationService` with the two lists of DP-07; tests for AC1 and X1.
4. `SuggestionRecordAppendService` and the fail-closed transaction; tests for AC1 and AC6 and TC-E2-032-10.
5. `AgentFactClient` over the run read with the timeout and the breaker, and the contract-fake run of the whole fact before `rwb-agent` is live (AC1, AC4, AC5).
6. `SuggestionRecordController` and `DecisionRecordQueryService` with the authorise answer, the scope filter and the page; tests for AC3, AC9 and TC-E2-032-09.
7. The idempotency path: a repeated append returns the first record and the chain gains no link; tests for AC7.
8. The absence tests: mode OFF, a timeout, a failed check and a settlement treatment leave no D5 record (AC2, AC4, AC5, AC8).
9. The privacy test: the record, the event payload and the log entries carry no name, e-mail address, mobile number, national identity number or account number (AC1).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P10-E2032-CON stay green, and a SIT day shows one D5 record per recorded suggestion with the model version "TDR-OFFER-1.0" and the key "TDR_OFFER:T-1001", a chain that verifies from its first entry, one `DecisionRecorded` event per record, no record and no suggestion when the record cannot be written, one record for a repeated request, no record when the model is off, slow or out of schema, and no personal data in any record, event or log.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append transaction |
| MSG-P7-009 | The decision code, the final call or a required version is not a value it must have | Not specified in the source documents (GAP-2403; ASM-3997) | This story, on the validation; the FSD names only the identifier and the field |
| MSG-P4-002 | The caller holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer |
| MSG-P4-003 | The record or the case is outside the reader's scope | This case is not in your scope. | This story, through the authorise answer and the case read |
| MSG-P10-007 | No suggestion: model not in service, timeout or failed check | No offer suggestion is available for this treatment. The TDR model is not in service. | `rwb-agent`, on the panel and on the treatment; this story produces no message |
| MSG-GEN-004 | The same suggestion arrives again for the treatment | Someone else changed this record. Reload it to see their change. | `rwb-agent`, on its request; this story returns the first record |

MSG-P7-003, MSG-P10-007 and MSG-P4-002 are copied unchanged from the legacy story RWB-E2-032 section 14; MSG-GEN-004 and MSG-P4-003 are the platform messages the agent operation and the authorise contract carry; MSG-P7-009 is named by FSD P7 v3 A2.2.4.3 and its text is not written out in any source this story may read, so the placeholder stands. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The suggestion area of SCR-14 Treatment record — the terms with the model code and version, or MSG-P10-007, while the officer edits the offer fields — belongs to RWB-P10-E2032-APP, and this story neither renders nor hides it. The record is read through the two operations of section 12.1 and shown by SCR-38 Decision log query, which is the decision-log query slice of this service and not this story; the composite route of DP-19 is used and not extended.

| Where | State | What the reader sees |
|---|---|---|
| `POST /decision-log` | 201 Appended | The record reference, the chain sequence, the entry hash and the decided time |
| `POST /decision-log` | 200 Already recorded | The first record of the same treatment, with its own reference; nothing new is written |
| `POST /decision-log` | 422 A value out of its list, or a missing version | MSG-P7-009, naming the field, and nothing written |
| `POST /decision-log` | 503 Record not written | MSG-P7-003 and nothing written; the caller's run is left without a decision link |
| `GET /decision-log` | One page | The records of a case in scope with code D5, model version, final call and decided time |
| `GET /decision-log/{entryId}` | One record | Code D5, model version "TDR-OFFER-1.0", the suggested terms, final call, decided time, previous hash and entry hash |
| `GET /decision-log`, `GET /decision-log/{entryId}` | 403 or 404 | MSG-P4-002 for a role without the right, MSG-P4-003 for a case out of scope |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-032-01 | AC1, BR1, BR2, BR3 | Contract | Treatment `T-1001` on case `RW-2026-001001`, run with model version "TDR-OFFER-1.0" and 84 installments of 18,900.00 baht; one D5 record with SUGGESTION_RECORDED |
| TC-E2-032-02 | AC2, BR8 | Component | Policy `TDR_OFFER` P1 mode OFF, review date 2027-02-28; no run, no record and no chain sequence consumed |
| TC-E2-032-03 | AC3, BR4, BR5 | Component | A recorded suggestion on `T-1001`; the read carries the model version, the inputs reference and the suggested terms |
| TC-E2-032-04 | AC4, BR8 | Component | Model stub silent for 61 seconds, run TIMED_OUT with fallback true; no record |
| TC-E2-032-05 | AC5, BR8 | Component | Answer with installments -12, run GUARDRAIL_FAILED with check SCHEMA; no record |
| TC-E2-032-06 | AC6, BR1, BR10 | Component | The decision-record write fails after the model answers; 503 MSG-P7-003, no record and no decision link on the run |
| TC-E2-032-07 | AC7, BR7 | Component | A second request for `T-1001` with the key `TDR_OFFER:T-1001`; one record and the first record returned |
| TC-E2-032-08 | AC8, BR8 | Component | Treatment `T-1002` of type SETTLEMENT; no call and no record |
| TC-E2-032-09 | AC9, BR11 | Component | A caller holding the Treatment and offer right only reads the ledger; 403 with MSG-P4-002 |
| TC-E2-032-10 | AC6, BR1, BR10 | NFR | The decision-record write forced to fail after the model answers; no record, no suggestion returned and MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because this slice carries the record of every suggestion of the key; the tests whose reading lives in `rwb-agent`, `rwb-treatment` or `rwb-access` assert this story's record through the contract fake for the rest. The `-ITG` copies of the same cases are RWB-ITG-W2-ITG and are not written here.

### 17. Guardrails

- No business value in code: the decision code, the final-call list, the model code, the model version, the schema limits, the timeout and the review date are reference-data or parameter rows; nothing of them is a constant here.
- No personal data in the record, the event payload, the trail, the tests or the model request: case, run and treatment references, a decision code, a version, a final call, the suggested terms and dates only; the masked inputs stay behind their reference.
- No read of another service's tables (DP-01): the run arrives on its contract, the case on its read and the authorise answer on its own; no `agent_run`, `agent_policy`, `treatment`, `recovery_case`, `delegation_limit`, `role` or `permission` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all; the account, the arrears and the payments reach it only as the inputs snapshot reference of the run (DP-05).
- One recorder and no mover: this story changes no treatment, no offer field, no case status, no run and no panel state, and the suggestion is never copied into the offer (BR5).
- No record without its event and no event without its record: the record, the chain link and the outbox row commit in one transaction, and a failure changes nothing and leaves the caller's run without a decision link (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist, the sequence number is never reused, and a wrong record is corrected by a new record naming the one it corrects (REQ-DRI-002).
- One record per treatment: the idempotency key and the unique key make a second record impossible, and a repeated call returns the first record.
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb-decision` in namespace `rwb-recovery`, with the shared topic `rwb.decision-record.v1` for the record event; no story in this key declares another service's base or topic as its own (DP-13).
- One hop and 2 s on every call, with a breaker per downstream; a missing answer never produces a record from a guessed version.
- The record path is never gated by a feature flag and never skipped for speed: a suggestion without its record is a defect, not a degraded mode.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | Business Requirements Epic 2, section 3.10; Business Requirements Program, sections 5.3 and 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39, CTL-06 | TC-E2-032-01, TC-E2-032-03, TC-E2-032-06, TC-E2-032-09, TC-E2-032-10 |
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | Business Requirements Epic 2, section 3.10; Business Requirements Program, sections 5.3 and 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-32, R-UNI-40 | TC-E2-032-01, TC-E2-032-02, TC-E2-032-04, TC-E2-032-05, TC-E2-032-07, TC-E2-032-08 |

| Legacy reference | Where it is kept |
|---|---|
| One decision log entry per recorded suggestion, with decision D5, the model version, the inputs reference, the recommendation, the final call and the actions | Sections 1, 2, 4, 7 (AC1, AC3), 8 (BR2 to BR6) |
| MSG-P7-003, R-UNI-39 and the block when the record cannot be written | Sections 5 (X2), 7 (AC6), 8 (BR1, BR10), 14 |
| Mode OFF, the timeout, the schema failure and the type check | Sections 5 (X4, X5, X6), 7 (AC2, AC4, AC5, AC8), 8 (BR8), 14 |
| One suggestion per treatment, key "TDR_OFFER:<treatmentId>" | Sections 5 (X3), 7 (AC7), 8 (BR7) |
| MSG-P4-002 and the roles RW-RESTRUCT and RW-RISK | Sections 5 (X7), 7 (AC9), 10, 14 |
| Treatment `T-1001`, case `RW-2026-001001`, the 1,250,000.00 baht at 120 days past due, policy P1 mode OFF with review date 2027-02-28, model version "TDR-OFFER-1.0" | Background and scenarios of section 7; section 3 |
| Legacy key RWB-E2-032, story RWB-P7-E2032-APP, contract RWB-P10-E2032-CON | Metadata, sections 3 and 12 |
| Test cases TC-E2-032-01 to TC-E2-032-10 | Section 16 |
| Decoupling patterns DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P10-E2032-APP and RWB-P10-E2032-CON the policy and its review date, the model gateway and the masked inputs, the output schema and the timeout, the agent run, the suggestion returned to the treatment, the feature flag, the panel and the admin reads; the treatment record and its offer fields are `rwb-treatment`'s (S2); RWB-ITG-W2-ITG the cross-service harness and the `-ITG` copies of the test cases.

### 19. Out of scope

- The agent policy and its review date, the masked input assembly, the model gateway call, the output schema "tdr-offer-v1", the 60 second timeout, the mode, the agent run, the suggestion returned to the treatment, the feature flag `rwb.agent.tdr-suggestion`, the admin reads and the suggestion area of SCR-14: RWB-P10-E2032-APP, with the contract, the event schemas and the fakes in RWB-P10-E2032-CON.
- Building or training the TDR model: the TDR team, outside the Workbench (legacy section 19).
- The treatment record, its type, its offer fields and the offer the officer builds: `rwb-treatment` (S2) and the treatment stories.
- The role model, the scope, the masking policy and the authorise answer: `rwb-access` (P4); this story consumes the answer and holds no rule of it.
- The decision-log store of this service — the append-only trigger, the grants, the chain verifier and the daily chain check JOB-14 at 02:00: the decision-log store slice (legacy RWB-E1-008) and the service baseline.
- The approval routing, the `ApprovalWorkflow`, the rule package registry, the rule promotion JOB-13 and the decision center screens SCR-10, SCR-11 and SCR-38: the other slices of `rwb-decision`.
- The affordability and plan calculation of the offer (ACE restructure calculator, R-RES-06) and the settlement and restructure agent that proposes plan terms: ACE and the agent catalog, not this story.
- The integration harness and the `-ITG` copies of the test cases: RWB-ITG-W2-ITG.
- The ACE DB story, the infrastructure story and the deployment story of this legacy key: their own DB, INF and OPS stories; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability are the OPS story's.

The release 31 December 2026 is copied unchanged from the legacy story and stays tentative; no date is changed by this story.
