# RWB-P7-E2028-APP Case intake agent live at L1 [E3a]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2028-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP07, DP09, DP10, DP13, DP15, DP19 |
| Parallel lane | L-P7-AI |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2028-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-005, FR-P7-006, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-028 for rwb-decision, the decision record of the agent-output verdict. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-E2028-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **every accept, correction or rejection of the L1 intake summary written as one append-only, hash-chained decision record of code D6 that names the agent and the prompt version in force and the reason I gave, readable afterwards in the central decision ledger**, so that **the bank can show which model and which prompt produced the recommendation I followed or overruled, how often the summary was right, and that no verdict exists without its record**.

Inside `rwb-decision` this is the decision-record slice of the legacy story RWB-E2-028:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- One deliverable and nothing else: the D6 decision record of an agent-output verdict. It takes the facts of one verdict on the intake summary, validates the code and the reason, appends one `decision_log_entry` in `rwb_decision` with the hash link of the record before it, writes the outbox row of the shared topic in the same transaction, answers with the record reference, and serves the ledger back on the two decision-log reads under the Decision log right and the case scope.
- The record is written through the decision-record path of DP-03 and never through another service's table. The record, its chain link and its outbox row commit together or not at all (R-UNI-39), and the row is never updated or deleted (REQ-DRI-002).
- The agent runtime is not here. The policy, the prompt, the agent run, the stored summary and the gap flags, the guardrails, the masked model call, the mode (SHADOW or L1), the masked panel and its six states stay in `rwb-agent` (P10, RWB-P10-E2028-APP and RWB-P10-E2028-CON), together with the acceptance and correction measure and its job. The case status, the case record and the scope decision stay in `rwb-case` (P3). The role, the scope, the masking policy and the authorise answer stay in `rwb-access` (P4). This story changes no case status, sets no task and no field of a case from the summary, and holds no copy of a case rule.
- The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-1294; ASM-2298); this story uses the phrase "the `rwb-decision` login (DP-02)" and never the shared monolith login.
- The legacy behaviour carried into the decision service is unchanged: the same one decision log entry per accept, correction or rejection, with the same decision code D6, the same agent version "INTAKE@P2/PR3", the same recommendation reference, the same final call and the same reason; the same refusal of a correction or a rejection that carries no reason; the same refusal of the whole action when the record cannot be written.

### 2. Business rationale

A case owner reads accounts, documents, appraisals and contact points before the first action on a new case, and after the shadow results and the approved L1 proposal the intake summary is shown to that owner. What makes the feature auditable is not the summary but the verdict on it: each accept, correction or rejection is a decision of code D6 taken by a person on the output of a model, and REQ-DRI-001 requires that record to hold the case, the decision, the agent and prompt versions, an inputs snapshot, the recommendation, the approver, the final call and the reason. Without that record the bank cannot say which model version and which prompt version a case owner followed, cannot measure how often the summary was right per segment, and cannot answer an audit or a regulatory request (NFR-033, NFR-036).

Under Architecture v5 the ledger is `rwb-decision`'s (slides 14, 41 and 20): every service writes its own decision record locally and publishes `DecisionRecorded` on `rwb.decision-record.v1`, and `rwb-decision` holds the central ledger. The realignment changes the mechanism, not the business rule:

1. The `DecisionLogWriter` of the monolith becomes the local decision-record library and the shared topic of DP-03, written in the same transaction as the change it records and hash-linked to the record before it.
2. The decision code, the verdict list and the reason codes that decided a branch in code become reference data read with the version in force (DP-07), so a code value or a new reason is a row and not a release.
3. The events of the module become CloudEvents on the owner's topics with an outbox on this service and an inbox on every consumer (DP-09), so a redelivery never writes a second record and a repeat never consumes a second chain sequence.
4. The scheduled and triggered work stays with the service that owns it through the workflow kit (DP-10): the metrics run is the reporting service's and the chain check is the decision-log store's, so this story registers no workflow and no Schedule.
5. Every path is on the owner's base `/api/recovery/decision/v1` (DP-13), each service migrates its own schema through its own Flyway sequence (DP-15), and the ledger reads are reached through the gateway-bff composite route the screens use (DP-19).

This story carries REQ-DRI-001 for the agent-verdict half and the decision-record half of REQ-ACA-005: the record holds identifiers, versions, a code, a final call and a reason, and no name, e-mail address, mobile number, national identity number or account number, because the summary itself and its masking tokens stay in `rwb-agent`.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P10-E2028-CON | The published agent contract: the run read this story consumes for the agent code, the agent and prompt version, the model version, the mode, the status and the data date, and the feedback operation of `rwb-agent` whose transaction this append is the first step of. The request and answer shape of the append, of the run read and of the ledger reads is Not specified in the source documents (GAP-1294; ASM-2298), and the fact set this story assumes is that of ASM-2302 |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the hash link, the chain sequence and the outbox row in one transaction |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION with the code D6 and the verdict list ACCEPTED, CORRECTED and REJECTED, with the version in force |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one `DecisionRecorded` fact per record, relayed once, and the inbox objects of the schema |
| RWB-PLT-E1071-CON | The workflow kit in namespace `rwb-recovery` (DP-10), held as a baseline only; this story starts no workflow and registers no Schedule |
| RWB-PLT-E1044-CON | The per-service Flyway sequence and migration conventions (DP-15) |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which the two ledger reads are reached; this story adds no route |
| The authorise answer of `rwb-access` and the case read of `rwb-case` | The Decision log right and the scope of the reader, and the owner, team, region and product group the scope filter is applied to; both are consumed on their published contracts or their fakes, are not rows of the metadata, and are carried in GAP-1295 |

Business preconditions carried from RWB-E2-028:

- Policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is approved by RW-RISK and in force from 2027-01-25 (legacy sections 3 and 7).
- The run of the case carries the agent version "INTAKE@P2/PR3" and the item of the verdict is the intake summary, item key "SUMMARY" (legacy sections 4 and 8).
- The case owner holds RW-CASEOWN with Case record CRU and the case is in that owner's scope (legacy section 3); the scope decision itself is `rwb-access`'s and `rwb-case`'s and this story only applies the answer.
- The decision code of the verdict is D6, a value of LOV-DECISION read with the version in force; the legacy story records it as an assumed code and the list is the source (legacy section 8 BR3).
- A correction or a rejection carries a reason of at most 1,000 characters (legacy section 12, AgentFeedbackRequest).
- The two roles that matter on the read are RW-CASEOWN and RW-RISK: the case owner reads the record of a case in scope and the risk and model risk officer reads the record of the summary they approved the use of (legacy sections 7 and 10).
- No build dependency. Day 1.

### 4. Flow

1. `rwb-agent` (P10): the case owner accepts, corrects or rejects the stored L1 summary of a case, and `rwb-agent` opens one feedback transaction for the run, the item "SUMMARY" and the verdict with its optional reason.
2. `rwb-agent` (P10): as the first step of that transaction it calls the append of this service with the case reference, the run reference, the item key, the verdict, the reason and its idempotency key, and it holds the answer until the append returns.
3. `rwb-decision` `VerdictRecordController`: validates the shape of the request, the idempotency key and the presence of a reason for a correction or a rejection; a missing reason is 422 with MSG-P7-005 and nothing is written (X1).
4. `rwb-decision` `VerdictValidationService`: reads the decision code D6 and the verdict list through the reference-data contract of DP-07 with the version in force, and refuses a code or a final call that is not a value of its list with 422 and MSG-P7-009 naming the field (X6).
5. `rwb-decision` `AgentFactClient`: reads the run through the P10 run read, one hop with a 2 s timeout and a breaker, and takes the agent code, the agent and prompt version, the model version, the mode, the status and the data date from the owner of the run instead of trusting the caller (ASM-2302); the run reference is the inputs reference of the record.
6. `rwb-decision` `ChainWriter`: takes the last `entry_hash` and `chain_seq` of the ledger under the append lock, computes the entry hash over the canonical form of the new record, and builds the row with `prev_hash` equal to that last hash and `chain_seq` equal to the next number.
7. `rwb-decision` `DecisionRecordAppendService`, one `RecordAndApply` transaction in `rwb_decision`: the `decision_log_entry` row is inserted with decision code D6, the agent and prompt version, the model version, the inputs reference, the recommendation of the run reference and the gap references, the final call, the reason as the override reason, the approver user reference and the decided time; the outbox row for `DecisionRecorded` on `rwb.decision-record.v1` is written; and the transaction commits. A failure of the library or of the insert rolls everything back and answers 503 with MSG-P7-003 (X2), and no chain sequence number is consumed.
8. `rwb-decision` `VerdictRecordController`: answers 201 with the record reference, the chain sequence, the entry hash and the decided time. `rwb-agent` stores that reference as the decision reference of its feedback row and commits its own transaction.
9. `rwb-decision` `DecisionRecordOutbox`: the relay of the platform publishes `rwb.decision-record.DecisionRecorded.v1` from the outbox in CloudEvents 1.0 with the record ID as its key; `rwb-decision` itself and `rwb-reporting` consume it (Architecture v5 slide 42, event 08).
10. A reader with the Decision log right R and the case in scope reads the ledger with `GET /api/recovery/decision/v1/decision-log?caseId=…` and one record with `GET /api/recovery/decision/v1/decision-log/{entryId}`, and sees the decision code D6, the agent version "INTAKE@P2/PR3", the final call, the reason, the approver, the decided time and the two hashes; the guard of the read is `rwb-access`'s and the scope filter is applied to the case read (X4, X5).
11. Nothing in this story changes the case, the run, the summary or the panel: the case keeps its status, `rwb-agent` keeps the feedback row and the measure, and the record is the only thing this service adds.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The owner corrects or rejects without a reason | Refused with 422 before anything is read or written; no record, no outbox row and no chain sequence consumed | MSG-P7-005 | AC4 |
| X2 | The record cannot be written: the library fails, the insert fails or the connection is lost | The whole transaction rolls back; no record and no outbox row; the chain stands at its last entry; `rwb-agent` stores no feedback because its transaction never commits; the incident is raised under R-UNI-39 | MSG-P7-003 | AC5, TC-E2-028-11 |
| X3 | The same verdict arrives twice for the same run and item, or two requests arrive at once | The idempotency key and the unique index give one record; the second call returns the first record with its own ID and the chain gains no second link; the 409 of the panel is the feedback operation's and is not produced here | MSG-GEN-004 (produced by `rwb-agent`) | AC6 |
| X4 | The reader holds no Decision log right, or the request reaches the service without the declared right | 403 with MSG-P4-002 and nothing returned | MSG-P4-002 | AC7, TC-E2-028-10 |
| X5 | The case of the record is outside the reader's scope | 404 with MSG-P4-003 and nothing returned | MSG-P4-003 | AC7 |
| X6 | The decision code or the final call is not a value of its list, or the record carries no agent version | 422 with MSG-P7-009 naming the offending field; nothing is written | MSG-P7-009 | AC1, AC3 |
| X7 | The append is called with no open transaction | The library refuses the call with its illegal-transaction condition and nothing is written (FSD P7 A2.2.4.3 AC-EXC-P7-002-04) | None to a user | AC1 |
| X8 | The case has no L1 output, because the run timed out or the segment is still in SHADOW | No verdict arrives, so no record is written and nothing is refused; the ledger holds no D6 record for the case | None to a user | AC8 |
| X9 | Two appends compute the same chain sequence | The unique key of the sequence refuses the second row and the append is retried on the new head of the chain; no gap and no duplicate is written | None to a user | AC3 |

A record is never updated and never deleted: a wrong record is corrected by a new record that names the one it corrects in `corrects_entry_id`, so the ledger stays append only (REQ-DRI-002). The record, its chain link and its outbox row are always written together, so a record cannot exist without its event and an event cannot name a record that was not stored.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the agent contract of RWB-P10-E2028-CON, the decision-record library and the reference-data contract of its DP table, and the fakes; no agent runtime, no case behaviour and no authorise rule is rebuilt here |
| Negotiable | The code values, the verdict list, the reason codes and the message texts are reference data or the message standard; the story fixes only the one-record-per-verdict rule, the chain and the fail-closed behaviour |
| Valuable | Every verdict on the intake summary has one record that names the agent and prompt versions, so the acceptance measure and the audit answer stand on a stored fact |
| Estimable | One controller, one append service, one validation service, one chain writer, two reads, one migration |
| Small | Fits one sprint with its tests; it is the decision-record slice of the legacy key |
| Testable | Each of the eight criteria in section 7 runs as an automated test against the contract fakes and the decision-record library, with a fixed clock and a seeded chain |

### 7. Acceptance criteria

```gherkin
Feature: Case intake agent live at L1 [E3a] — the rwb-decision decision record of the agent-output verdict

  Background:
    Given the environment is SIT
    Given policy "INTAKE" version "P2" with mode "L1" and prompt "PR3" is in force from 2027-01-25 and approved by RW-RISK
    Given case owner "owner.user07" holds RW-CASEOWN and owns case "RW-2027-000501"

  Scenario: AC1 An accepted summary writes one D6 record (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000501" with agent "INTAKE", version "INTAKE@P2/PR3", autonomy mode "L1", status "ANSWERED" and the gap flags MISSING_DOCUMENT and NO_VALID_APPRAISAL
    Given the rwb-case contract mock returns case "RW-2027-000501" owned by "owner.user07" with product group "MORTGAGE"
    When rwb-agent sends the verdict "ACCEPTED" for item "SUMMARY" of that run and this service appends the record
    Then one decision record exists for case "RW-2027-000501" with decision code "D6", agent version "INTAKE@P2/PR3", the run as its inputs and recommendation reference, final call "ACCEPTED" and no override reason
    Then the answer carries the record reference and the chain sequence that rwb-agent stores as the decision reference of its feedback
    Then the record, its chain link and its outbox row for the decision record event are written in one transaction
    Then the record carries no name, no e-mail address, no mobile number, no national identity number and no account number

  Scenario: AC2 A correction carries its coded reason and the data date (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000503" with agent "INTAKE", version "INTAKE@P2/PR3", autonomy mode "L1", status "ANSWERED" and data as of 2027-01-26 against business date 2027-01-28
    Given case owner "owner.user07" holds RW-CASEOWN and owns case "RW-2027-000503"
    When rwb-agent sends the verdict "CORRECTED" with a coded reason for item "SUMMARY" of that run
    Then one decision record exists with decision code "D6", final call "CORRECTED" and the coded reason as its override reason
    Then its inputs reference carries the run and the data date 2027-01-26
    Then its entry hash is the hash of its canonical form and its previous hash is the entry hash of the record before it
    Then the warning MSG-P1-001 stays the panel's and this story produces no message from that date

  Scenario: AC3 A rejection is the third final call and each verdict makes exactly one record (new, D-RCV-60)
    Given the rwb-agent contract mock returns three runs of case "RW-2027-000501" with agent "INTAKE" and version "INTAKE@P2/PR3", the first accepted, the second corrected with a coded reason and the third rejected with a coded reason
    When the three verdicts are sent for item "SUMMARY", one per run
    Then three decision records exist for the case, one per run and item
    Then their final calls are exactly "ACCEPTED", "CORRECTED" and "REJECTED"
    Then the chain sequence numbers are assigned in the order the records were appended and no number is reused
    Then no record carries a rule ID or a rule version, because the verdict of an agent output is not a rule answer

  Scenario: AC4 A correction or a rejection without a reason writes nothing (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000501" with status "ANSWERED"
    When rwb-agent sends the verdict "CORRECTED" with an empty reason, and then the verdict "REJECTED" with an empty reason
    Then each answer is 422 with MSG-P7-005
    Then no decision record and no outbox row is written for the run and the chain sequence number is not consumed

  Scenario: AC5 The record cannot be written and nothing else moves (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000501" with status "ANSWERED"
    Given the decision-record library refuses the append and raises its unavailable condition
    When rwb-agent sends the verdict "ACCEPTED" for that run
    Then the answer is 503 with MSG-P7-003
    Then no decision record and no outbox row exists for the run and the chain stands at its last entry
    Then rwb-agent stores no feedback for the run, because its transaction never commits
    Then an incident is raised under R-UNI-39 to the platform administration role

  Scenario: AC6 A repeated verdict gives one record and never a second chain link (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000501" with status "ANSWERED" and the verdict "ACCEPTED" was already recorded for item "SUMMARY"
    When rwb-agent sends the same verdict again with the same idempotency key for the same run and item
    Then one decision record exists for the run and item "SUMMARY"
    Then the answer returns the first record with the same record reference and the chain gains no second link
    Then the refusal with 409 and MSG-GEN-004 is the feedback operation's and is not produced here

  Scenario: AC7 The record is readable and the read is guarded (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000501" and the verdict "ACCEPTED" was recorded for it
    Given the rwb-access contract mock returns the allow answer on the Decision log right R to "owner.user07" and the refusal to role RW-PHONECOL, which holds Case record R only
    Given the rwb-case contract mock returns case "RW-2027-000601" in team "HP-NE" outside the scope of "owner.user07"
    When "owner.user07" sends GET /api/recovery/decision/v1/decision-log for case "RW-2027-000501" and then GET /api/recovery/decision/v1/decision-log/{entryId} for that record
    Then the page holds the record with decision code "D6", agent version "INTAKE@P2/PR3" and final call "ACCEPTED"
    Then the single read carries decision code "D6", agent version "INTAKE@P2/PR3", final call "ACCEPTED", the decided time, the previous hash and the entry hash
    Then role RW-PHONECOL is refused with 403 and MSG-P4-002 and a read for case "RW-2027-000601" is refused with 404 and MSG-P4-003

  Scenario: AC8 A case with no L1 verdict leaves no record (new, D-RCV-60)
    Given the rwb-agent contract mock returns no L1 output for unsecured case "RW-2027-000701", whose INTAKE policy is mode "SHADOW"
    Given the rwb-agent contract mock returns the run of case "RW-2027-000502" with status "TIMED_OUT" and fallback true
    When the ledger is read for the two cases
    Then neither case holds a decision record with decision code "D6"
    Then no verdict is sent for either case and no chain sequence number is consumed
```

These eight criteria are new for the `rwb-decision` slice of RWB-E2-028 and are the decision-record criteria of the key; the values are the legacy values of RWB-E2-028 sections 3, 4 and 7 — case `RW-2027-000501`, policy "INTAKE" version "P2" mode L1 approved by RW-RISK from 2027-01-25, agent version `INTAKE@P2/PR3`, decision D6, the final calls ACCEPTED, CORRECTED and REJECTED, roles RW-CASEOWN and RW-RISK, cases `RW-2027-000502`, `RW-2027-000503`, `RW-2027-000601` and `RW-2027-000701`, data as of 2027-01-26 against business date 2027-01-28 — and no new business value is introduced. `acs` is empty for this story: no legacy criterion is owned verbatim here, because every legacy criterion of the key either reads the stored output or gives the verdict on the panel, and both belong to `rwb-agent` (P10). The wording of MSG-P7-005, MSG-P7-003, MSG-GEN-004, MSG-P4-002, MSG-P4-003 and MSG-P1-001 is the legacy wording and section 14 repeats it unchanged.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every accept, correction or rejection of the L1 intake summary writes exactly one decision record, and no verdict exists without its record | REQ-DRI-001; REQ-DRI-005; R-UNI-39; legacy BR3 |
| BR2 | The record carries the decision code D6, a value of LOV-DECISION read with the version in force; the code is data and never a constant of the code | Legacy BR3 (assumed code); TSD P7 v2 T3.1 (DF-DEC-003); FSD P7 v3 A2.14.3.2; DP-07 |
| BR3 | The record names the agent and the prompt version of the run, taken from the run and not from the caller, so a reader can tell which model and which prompt produced the recommendation that was followed or overruled | REQ-DRI-001; TSD P7 v2 T3.1 (DF-DEC-007); NFR-033; ASM-2302 |
| BR4 | The final call is the verdict: ACCEPTED, CORRECTED or REJECTED, one of the values of the verdict list read as reference data; the verdict list is data and never a constant of the code | Legacy sections 8 and 17; DP-07; ASM-2299 |
| BR5 | A correction or a rejection carries a reason of at most 1,000 characters, written as the override reason of the record; an acceptance carries none; a correction or a rejection without a reason is refused | Legacy BR4 and section 12; CTL-07; MSG-P7-005 |
| BR6 | The inputs reference of the record is the run reference with the data date of the run, so a verdict given on data older than the business date is visible in the ledger; the stale warning on the panel is `rwb-agent`'s | TSD P7 v2 T3.1 (DF-DEC-008); FSD P7 v3 A2.14.3.2; legacy AC9 |
| BR7 | The recommendation of the record is the run reference and the gap flags of the summary, and never the summary text: the text and its masking tokens stay in `rwb-agent` | Legacy section 12 (recommendation {"runId","gaps"}); CTL-11 |
| BR8 | The record is append only and hash chained: an entry hash over its canonical form, a previous hash equal to the entry hash before it, a sequence number that is never reused, and no update and no delete; a wrong record is corrected by a new record that names the one it corrects | REQ-DRI-002; REQ-DRI-003; TSD P7 v2 T3.1 (DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029) |
| BR9 | The record, its chain link and its outbox row commit in one transaction, and no action proceeds when the record cannot be written; the failure rolls the caller's feedback back as well | REQ-DRI-005; R-UNI-39; DP-03; MSG-P7-003 |
| BR10 | One record per run and item: the idempotency key of the run and the item key, held by the unique key of the ledger, makes a second record for the same verdict impossible, and a repeated call returns the first record | R-UNI-40; DP-09; ASM-2301 |
| BR11 | The ledger is read under the Decision log right R and the caller's scope; the right is `rwb-access`'s to answer and the scope filter is applied to the case read of `rwb-case`; this service holds no role, no scope and no masking rule of its own | TSD P7 v2 T6.1 and T6.2; legacy section 10; the authorise dependency is carried in GAP-1295 |
| BR12 | No personal data in the record, the event, the trail or the logs: case and run identifiers, a decision code, a version, a final call, a reason code, a user reference and dates only | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43; REQ-ACA-005 |
| BR13 | No case value changes because of the record: no case status, no task, no timer and no field is set from the summary or from the verdict, and the case stays where `rwb-case` has it | Legacy section 9 and section 17; Architecture v5 slide 41 |
| BR14 | The ledger read returns no row of a case outside the caller's scope, and a request without the declared right is refused before any row is read | TSD P7 v2 T6.2; legacy AC7 and legacy X5, X8 |
| BR15 | The record is the local record of this service and the central ledger at once: it is written in `rwb_decision`, sealed by the ledger of this service, and published on `rwb.decision-record.v1` for the consumers of the catalogue only | Architecture v5 slides 14, 20 and 42; DP-03; DP-09 |

### 9. State transitions

The states below are the states of a decision record of this story. The case, the agent run, the summary and the panel are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | An append arrives for a verdict with a reason where one is needed, a code and a final call of their lists, and a run that answers | The library writes the record, the outbox row and the chain link in one transaction | Appended, with a chain sequence, a previous hash and an entry hash |
| Absent | An append arrives with no reason for a correction or a rejection | The validation refuses the request | Absent: 422 with MSG-P7-005 and no sequence consumed |
| Absent | An append arrives with a code or a final call that is not a value of its list | The validation refuses the request | Absent: 422 with MSG-P7-009 naming the field |
| Absent | The library or the insert fails | The transaction rolls back | Absent: 503 with MSG-P7-003, the chain at its last entry, the caller's feedback rolled back |
| Absent | The same run and item were already recorded | The idempotency key and the unique key hold | Appended: unchanged, the first record returned |
| Appended | A later append arrives | The chain head has moved | Appended: the new record names the previous hash of the head |
| Appended | A wrong record must be corrected | A person decides the correction | Appended: a new record with `corrects_entry_id` naming the wrong one; the wrong one stays |
| Appended | Any update or delete is attempted | Through the service role or the schema owner | Appended: refused, and the attempt is written to the ACE audit log |

The final call moves between the three values of the verdict list only through a new record, never through an update. The case stays where `rwb-case` has it, and the run and the panel stay as `rwb-agent` has them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, the case owner | Gives the verdict on the summary of a case in scope through the feedback operation of `rwb-agent`, and reads the record of that case in the ledger (Decision log R, Case record U for the verdict) |
| RW-RISK, the risk and model risk officer | Reads the record of the summary whose use they approved, with the code, the agent and prompt version and the final call |
| RW-TEAMMGR, RW-COE and RW-AUDIT | Read the ledger under the Decision log right R, as TSD P7 v2 T6.1 fixes it; they take no verdict |
| SY-AGENT and SY-DECLOG | Append the record on behalf of the verdict, one hop, under the service identity; they hold no user right and write nothing else |
| The `rwb-decision` service identity | Writes its own `rwb_decision` rows, the outbox row and the chain link, and reads the run through the P10 contract (`rwb-decision` login, DP-02) |
| The decision-record library identity | Writes the record, the hash link and the outbox row in one transaction and publishes on `rwb.decision-record.v1` (DP-03) |
| `rwb-agent` (P10) | Owns the run, the summary, the gap flags, the mode, the guardrails, the panel, the feedback row and the acceptance measure; this story holds none of them |
| `rwb-case` (P3) and `rwb-access` (P4) | Own the case status, the case record, the scope and the rights; this story applies their answers and changes neither |

The authorisation decision is `rwb-access`'s and is consumed as the authorise answer the read declares; the refusal shape stays 403 with MSG-P4-002 and 404 with MSG-P4-003. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-1294; ASM-2298); the story refers to "the `rwb-decision` login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, the value D6 of LOV-DECISION |
| DF-DEC-004 | `decision_log_entry` | rule_id | Not written: the verdict of an agent output is not a rule answer |
| DF-DEC-005 | `decision_log_entry` | rule_version | Not written, for the same reason |
| DF-DEC-006 | `decision_log_entry` | model_version | Write, taken from the run when the run names it |
| DF-DEC-007 | `decision_log_entry` | agent_version | Write, "INTAKE@P2/PR3" from the run |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the run reference with the data date |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the run reference and the gap references |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Write, the owner reference who gave the verdict |
| DF-DEC-011 | `decision_log_entry` | approval_level | Not written: an agent-output verdict carries no delegation level |
| DF-DEC-012 | `decision_log_entry` | final_call | Write, ACCEPTED, CORRECTED or REJECTED |
| DF-DEC-013 | `decision_log_entry` | override_reason | Write on a correction or a rejection |
| DF-DEC-014, DF-DEC-015 | `decision_log_entry` | actions, outcome | Not written by this story; the outcome of the verdict is `rwb-agent`'s |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write |
| DF-DEC-017, DF-DEC-018 | `decision_log_entry` | prev_hash, entry_hash | Write |
| DF-DEC-028 | `decision_log_entry` | chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on a record that corrects an earlier one |
| DF-DEC-030 | `decision_log_entry` | actor_user_id | Write, the service identity or the owner reference |
| DF-DEC-031 | `decision_log_entry` | idempotency_key | Write, the run and the item key |
| DF-DEC-001 to DF-DEC-031 | decision record | all fields | Read through the two ledger operations |
| DF-CAS-001, DF-CAS-003, DF-CAS-009, DF-CAS-011, DF-CAS-012 | `recovery_case` | id, product_group, owner_user_id, team_code, region_code | Read through the P3 case read, for the scope filter only |
| DF-AGT-036, DF-AGT-037, DF-AGT-038, DF-AGT-043, DF-AGT-046, DF-AGT-050, DF-AGT-055 | `agent_run` | id, agent_code, agent_version, autonomy_mode, status, confidence, data_as_of | Read through the P10 run read |
| DF-AGT-039, DF-AGT-040 | `agent_run` | model version and prompt version, where the run names them | Read through the P10 run read; the field set of that read is Not specified in the source documents (GAP-1294; ASM-2302) |
| (inbox) | library table in `rwb_decision` | event_id, consumer, processed_at | Not written: this story consumes no event |
| (outbox) | library table in `rwb_decision` | the `DecisionRecorded` row | Write |

No row of `agent_run`, `agent_feedback`, `agent_policy` or `agent_prompt` is copied into `rwb_decision`: the run facts arrive on the P10 contract and the feedback row is `rwb-agent`'s, which stores this story's record reference in its own column. No row of `recovery_case`, `task`, `timer` or `queue` is written, and no role, scope or masking row is read from `rwb_access`. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two reads are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1; the append on the same collection is the write path DP-03 needs and is Not specified in the source documents (GAP-1294; ASM-2298). The request and answer field set of the three operations is Not specified in the source documents (GAP-1294; ASM-2298).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/decision-log` | Append one decision record for one verdict of an agent output: validate, chain and write, then answer 201 with the record; a repeated key answers 200 with the first record | Service identity only, SY-AGENT and SY-DECLOG (TSD P7 v2 T6.1, right C); one hop from `rwb-agent` with a 2 s timeout | Idempotency-Key header, the run reference and the item key, kept on the ledger row |
| GET | `/decision-log` | API-P7-006: search the ledger by case, decision, rule, approver and date, one page at a time | Decision log, right R, scope applied through the authorise answer and the case read of P3 | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one record with its inputs, its versions, its final call, its reason and its two hashes | Decision log, right R, scope applied | Not applicable, read only |

The append request this story assumes carries `caseId`, `runId`, `itemKey` ("SUMMARY"), `verdict`, `reason`, `idempotencyKey` and `decidedAt`; the agent code, the agent and prompt version, the model version and the data date are read from the run and not from the request. The DecisionRecord answer carries `id`, `caseId`, `decisionCode`, `agentVersion`, `modelVersion`, `inputsRef`, `recommendation`, `finalCall`, `overrideReason`, `approverUserId`, `decidedAt`, `chainSeq`, `prevHash` and `entryHash`. Both sets are the placeholder until the contract baseline is agreed (GAP-1294; ASM-2298).

Errors: 401 no session; 403 the role holds no Decision log right (MSG-P4-002); 404 the record or the case is absent or out of scope (MSG-P4-003); 409 the append repeats a key with a different body (MSG-GEN-004); 422 a reason is missing (MSG-P7-005) or a code, a final call or a version is not a value of its list (MSG-P7-009); 503 the record was not written (MSG-P7-003). Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/agent-runs/{runId}` | P10 rwb-agent, on RWB-P10-E2028-CON | The run facts the record names: agent code, agent and prompt version, model version, autonomy mode, status, confidence and data as of; faked, one hop with a 2 s timeout and a breaker |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The owner, team, region and product group the scope filter of the ledger read is applied to; faked, one hop |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The cached decision of the Decision log right R and the scope of the reader behind the two reads; faked |

The three operations are the P10, P3 and P4 rows of the Ownership Map and of Architecture v5 slides 14, 16 and 41. Their request and answer shape is Not specified in the source documents (GAP-1294; ASM-2298). The two reads declare the Decision log right R on the operation, take the right and the scope from the authorise answer and apply the scope filter to the case read, as ASM-2303 reads it. DP-08, which would add the guard library and the authorise contract as named dependencies, is not among the patterns of this key, so the authorise answer is consumed against its published contract or its fake and the dependency is carried in GAP-1295.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7, published by this service | entryId | record ID, case ID, decision code D6, agent version, model version, inputs reference, final call, decided at, chain sequence, entry hash |

The event is written to the outbox in the same transaction as the record and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform (DP-09); the shared topic carries its own name, so the event of the catalogue is published there and not on the service topic. `rwb-decision` itself and `rwb-reporting` consume it, as event 08 of Architecture v5 slide 42 names them. No event carries a name, an e-mail address, a mobile number, an account number or the summary text.

#### 12.4 Events consumed

None. This story consumes no event: the verdict arrives on the append request and the run facts on the run read. The inbox objects of DP-09 are created in the schema by the service baseline and this story writes none.

#### 12.5 Workflows and activities

None of this story's own. The append is one synchronous service operation inside the caller's unit of work, not a workflow, and the ledger read is a query. `rwb-decision` holds `ApprovalWorkflow` of the workflow kit and its Schedules for other slices of the service; this story starts no workflow, signals none, and registers no activity and no Schedule on the `rwb-decision` queue. The chain check JOB-14 at 02:00 is the decision-log store's and the metrics run JOB-15 is `rwb-reporting`'s (Architecture v5 slide 44).

#### 12.6 Schedules

None. The metrics run JOB-15 at 01:30 is the reporting extract of `rwb-reporting` and runs on its own trigger; the chain check JOB-14 at 02:00 belongs to the decision-log store slice of this service; this story adds neither and polls nothing.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The record of the verdict: the code, the versions, the inputs reference, the recommendation, the final call, the reason, the hashes and the chain sequence; written once and read |
| outbox library table | PLT library, created in `rwb_decision` | The `DecisionRecorded` row (DP-09) |
| `idempotency_key` | PLT library, created in `rwb_decision` | The stored answer of a repeated append (DP-09) |

Not owned and never read by this story: `agent_run`, `agent_policy`, `agent_prompt`, `agent_feedback` and `agent_evaluation` (P10), `recovery_case` (P3), `delegation_limit`, `role`, `permission` and `masking_rule` (P4). The run arrives on its contract, the case on its read, and the authorise answer on its own; no foreign key crosses a schema and no row of another service is copied (DP-01). The `approval` and `rule_package` tables are this service's but another story's, and this story writes neither.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-agent contract fake | RWB-P10-E2028-CON | The run of case `RW-2027-000501` with agent "INTAKE", version "INTAKE@P2/PR3", mode "L1", status "ANSWERED" and the two gap flags; three runs of the same case for the three verdicts; the run of `RW-2027-000503` with data as of 2027-01-26; the run of `RW-2027-000502` with status "TIMED_OUT" and fallback true; no L1 output for `RW-2027-000701`; the request journal for the idempotency key and the ordering assertions |
| rwb-case fake | The P3 case read | Case `RW-2027-000501` owned by `owner.user07` with product group "MORTGAGE", team and region; case `RW-2027-000601` in team "HP-NE" outside the scope; case `RW-2027-000503` |
| rwb-access fake | The P4 authorise call | The allow answer on the Decision log right R for `owner.user07`, the refusal on the right for role RW-PHONECOL (MSG-P4-002) and the refusal of the out-of-scope case (MSG-P4-003) |
| decision-record fake | RWB-PLT-E1027-CON | The append of the local record, the chain sequence allocation and the hash link; the chain verifier over a seeded ledger; a forced failure and an unavailable condition for AC5 and TC-E2-028-11 |

Each fake is replaced by the real service as its contract lands, without a change to the criteria. The decision-record fake stands only for the tests of the chain and of the failure, because the library is the service's own DP-03 baseline.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3, consumed 3 | `POST /decision-log`, `GET /decision-log` and `GET /decision-log/{entryId}` provided; the run read, the case read and the authorise call consumed, one hop each with the 2 s timeout |
| Kafka | Published 1 event type, consumed 0 | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; nothing consumed |
| Temporal | None | No workflow, no activity and no Schedule registered; JOB-14 and JOB-15 stay with their owners |
| File | None | No file input and no file output; the daily ledger seal is another slice's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger/agentverdict`, Java package `th.co.scb.ace.workbench.recovery.decision.agentverdict`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the core of the slice: the legacy `DecisionLogWriter` of the monolith becomes the local decision-record library of this service, which writes the record, the hash link and the outbox row in one transaction and publishes on the shared topic, so every verdict of an agent output has one record in the ledger that this service owns. DP-07 is where the decision code and the verdict list live: LOV-DECISION and the verdict list are read through the reference-data contract of `rwb-case` with the version in force, and neither is a constant here. DP-09 is the outbox and the CloudEvents envelope of the one published fact; the inbox objects are part of the service baseline and this story consumes no event. DP-10 is carried and not used: the metrics run JOB-15 at 01:30 belongs to `rwb-reporting` and the chain check JOB-14 at 02:00 to the decision-log store slice, so the Schedule stays with the service that owns it and this story registers no workflow and no Schedule. DP-13 puts the three operations on `/api/recovery/decision/v1`; DP-15 puts the migration in the per-service Flyway sequence of `rwb_decision`; DP-19 is the composite route through which the two ledger reads are reached by the decision-log query screen of the service, and this story adds no route and serves no screen of its own.

The platform H dependencies of the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-E1071-CON, H RWB-PLT-E1044-CON, H RWB-PLT-N001-CON) and the C dependency that DP-07 brings with it (C RWB-P3-E1043-CON) are not in the metadata rows of this story, which name None and RWB-P10-E2028-CON; they are the dependencies the DP table adds and they are recorded in GAP-1295 and ASM-2304. The same row carries the two consumed operations that no pattern names: the P3 case read and the P4 authorise call. None of them blocks the build beyond Day 1: they are platform contracts of waves 0 and 1 and published contracts of other services. The agent contract arrives as the C dependency RWB-P10-E2028-CON, and DP-20, which would name an agent contract of its own, is not among the patterns of the key.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| VerdictRecordController | Controller | `POST /decision-log` with the shape and idempotency validation, the 201 and 200 answers, and the problem mapping for 401, 409, 422 and 503 |
| DecisionRecordController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the guard, the scope, the page and the problem mapping for 401, 403, 404 and 503 |
| VerdictValidationService | Service | Reads LOV-DECISION and the verdict list with the version in force, and refuses a code or a final call that is not a value of its list with MSG-P7-009 |
| AgentFactClient | Adapter | The run read of RWB-P10-E2028-CON, one hop with a 2 s timeout and a breaker; takes the agent and prompt version from the owner of the run |
| ChainWriter | Service | Reads the head of the chain under the append lock, computes the entry hash over the canonical form and builds the previous hash and the sequence number |
| DecisionRecordAppendService | Service | One `RecordAndApply` transaction: the record, the chain link and the outbox row, or nothing; maps the failure to 503 with MSG-P7-003 |
| DecisionRecordRepository | Repository | `decision_log_entry` in `rwb_decision`, with the unique key of the chain sequence and of the idempotency key |
| DecisionRecordQueryService | Service | The ledger page and the single record, with the scope filter applied to the case read |
| AccessCheckClient | Client | The authorise answer behind the two reads, with the cached decision of the right |
| CaseScopeClient | Client | The P3 case read that gives the owner, team, region and product group of the scope filter |
| DecisionRecordOutbox | Library use | The outbox row of `DecisionRecorded` in the same transaction as the record (DP-09) |

**Database and migrations**

- Writes `decision_log_entry` and the outbox and idempotency objects of the library, all in schema `rwb_decision`; reads no other schema.
- The `decision_log_entry` baseline, its append-only trigger and its grants belong to the decision-log store slice of this service (legacy RWB-E1-008) and are not rebuilt here.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2028_1__decision_agent_verdict.sql` adds the unique key `ux_declog_chain_seq ON decision_log_entry (chain_seq)`, the unique key `ux_declog_idem ON decision_log_entry (idempotency_key) WHERE idempotency_key IS NOT NULL`, the index `ix_declog_case_decided ON decision_log_entry (case_id, decided_at DESC)` for the ledger read of one case, and the foreign key of `corrects_entry_id` to `decision_log_entry (id)`.
- No row is updated and no row is deleted by this story; the update path of the store does not exist and the delete path does not exist.

**Configuration and reference data**

- LOV-DECISION and the verdict list ACCEPTED, CORRECTED and REJECTED are read through the reference-data contract of DP-07 with the version in force; the code D6 and the three final calls are values of those lists and never constants in code (ASM-2299).
- The reason codes of a correction and of a rejection are reference data; the list and its values are Not specified in the source documents (GAP-1294; ASM-2300), so the story validates the presence and the length of the reason and not a set of codes it does not have.
- The reason length, 1,000 characters, is the column length of `override_reason` and of the legacy request (DF-DEC-013).
- The feature switch of the legacy capability, `rwb.agent.intake-l1`, stays with RWB-P10-E2028-APP and is not read here: a record that could be switched off would break R-UNI-39, so the append is never gated by a flag (ASM-2305).
- The `rwb-decision` login of DP-02, the flyway user and the outbox relay identity are environment configuration and not values of this story.

**Build steps**

1. The migration `V2028_1__decision_agent_verdict.sql` with the two unique keys, the index and the foreign key; test that a repeated chain sequence and a repeated idempotency key are refused by the constraints (BR8, BR10, X9).
2. `ChainWriter` with the head read, the canonical form and the entry hash; test the seeded chain of 100 records and the first record with the previous hash of 64 zeros (AC1, AC3).
3. `VerdictValidationService` with the two lists of DP-07 and the reason rule; tests for AC4, X1 and X6.
4. `DecisionRecordAppendService` and the fail-closed transaction; tests for AC1, AC5 and TC-E2-028-11.
5. `AgentFactClient` over the run read with the timeout and the breaker, and the contract-fake run of the whole fact before `rwb-agent` is live (AC1, AC2).
6. `DecisionRecordController` and `DecisionRecordQueryService` with the authorise answer, the scope filter and the page; tests for AC7 and TC-E2-028-10.
7. The idempotency path: a repeated append returns the first record and the chain gains no link; tests for AC6.
8. The privacy test: the record, the event payload and the log entries carry no name, e-mail address, mobile number, national identity number or account number (AC1, AC2).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P10-E2028-CON stay green, and a SIT day shows one D6 record per verdict of the intake summary with the agent version "INTAKE@P2/PR3", a chain that verifies from its first entry, one `DecisionRecorded` event per record, no record and no feedback row when the record cannot be written, one record for a repeated verdict, and no personal data in any record, event or log.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-005 | A correction or a rejection carries no reason | Enter the reason you are not following the recommendation. | This story, on the append |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append transaction |
| MSG-P7-009 | The decision code, the final call or a required version is not a value it must have | Not specified in the source documents (GAP-1294; ASM-2298) | This story, on the validation; the FSD names only the identifier and the field |
| MSG-GEN-004 | The same verdict arrives again for the run and item, or the record changed | Someone else changed this record. Reload it to see their change. | `rwb-agent`, on the feedback; this story returns the first record |
| MSG-P4-002 | The reader holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer |
| MSG-P4-003 | The record or the case is outside the reader's scope | This case is not in your scope. | This story, through the authorise answer and the case read |
| MSG-P1-001 | The summary was built on data older than the business date | {product} is from {date}. Today's load has not arrived. | `rwb-agent`, on the panel; this story records the data date and produces no message |

MSG-P7-005, MSG-P7-003 and MSG-P1-001 are copied unchanged from the legacy story RWB-E2-028 section 14; MSG-GEN-004, MSG-P4-002 and MSG-P4-003 are the platform messages the feedback operation and the authorise contract carry; MSG-P7-009 is named by FSD P7 v3 A2.2.4.3 and its text is not written out in any source this story may read, so the placeholder stands. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The panel "Agent summary" on SCR-03 Case record and its six states — loading, empty, unavailable, stale, ready and recorded — belong to RWB-P10-E2028-APP, and this story neither renders nor hides them. The record is read through the two operations of section 12.1 and shown by SCR-38 Decision log query, which is the decision-log query slice of this service and not this story; the composite route of DP-19 is used and not extended.

| Where | State | What the reader sees |
|---|---|---|
| `POST /decision-log` | 201 Appended | The record reference, the chain sequence, the entry hash and the decided time |
| `POST /decision-log` | 200 Already recorded | The first record of the same run and item, with its own reference; nothing new is written |
| `POST /decision-log` | 422 No reason, or a value out of its list | MSG-P7-005 or MSG-P7-009, naming the field, and nothing written |
| `POST /decision-log` | 503 Record not written | MSG-P7-003 and nothing written; the caller's feedback is rolled back |
| `GET /decision-log` | One page | The records of a case in scope with code D6, agent version, final call and decided time |
| `GET /decision-log/{entryId}` | One record | Code D6, agent version "INTAKE@P2/PR3", final call, reason, approver, decided time, previous hash and entry hash |
| `GET /decision-log`, `GET /decision-log/{entryId}` | 403 or 404 | MSG-P4-002 for a role without the right, MSG-P4-003 for a case out of scope |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-028-10 | AC7, BR11, BR14 | Component | RW-PHONECOL, which holds Case record R only, reads the ledger and is refused with MSG-P4-002; case `RW-2027-000601` out of scope is 404 with MSG-P4-003 |
| TC-E2-028-01 | AC1, BR1, BR2, BR3, BR6 | Component | Case `RW-2027-000501` with an ANSWERED run, agent version "INTAKE@P2/PR3" and the two gap flags |
| TC-E2-028-02 | AC3, BR3, BR10 | Contract | January 2027, MORTGAGE/BKK: 300 feedback rows, 240 accepted, 45 corrected and 15 rejected, each with one D6 record |
| TC-E2-028-03 | AC8, BR13 | Component | Case `RW-2027-000502` with a TIMED_OUT run and fallback true; no record |
| TC-E2-028-04 | AC4, BR5 | Component | A correction with an empty reason and a rejection with an empty reason; 422 MSG-P7-005 and nothing written |
| TC-E2-028-05 | AC1, AC5, BR9 | Component | The decision-record library fails on an acceptance; no record, no outbox row and no feedback row |
| TC-E2-028-06 | AC6, BR10 | Component | A second verdict for the same run and item; one record and the first record returned |
| TC-E2-028-07 | AC7, BR11 | Contract | Case `RW-2027-000601` in team `HP-NE`; the read is 404 with MSG-P4-003 |
| TC-E2-028-08 | AC8, BR13 | Component | Unsecured case `RW-2027-000701` with segment UNSECURED in SHADOW; no record |
| TC-E2-028-09 | AC2, BR6 | Contract | Case `RW-2027-000503`, data as of 2027-01-26 and business date 2027-01-28; the data date on the inputs reference |
| TC-E2-028-11 | AC5, BR9 | NFR | The decision-record write forced to fail on a verdict; no record, no outbox row, no feedback row and the chain at its last entry |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because this slice carries the record of every verdict of the key; the tests whose reading lives in `rwb-agent`, `rwb-case` or `rwb-access` assert this story's record through the contract fake for the rest. The `-ITG` copies of the same cases are RWB-ITG-E2028-ITG and are not written here.

### 17. Guardrails

- No business value in code: the decision code, the verdict list, the reason codes, the message texts and the data date are reference-data rows, message-standard rows or facts of the run; nothing of them is a constant here.
- No personal data in the record, the event payload, the trail, the tests or the prompts: case and run identifiers, a decision code, a version, a final call, a reason, a user reference and dates only; the summary text and its masking tokens never enter this service.
- No read of another service's tables (DP-01): the run arrives on its contract, the case on its read and the authorise answer on its own; no `agent_run`, `agent_feedback`, `recovery_case`, `delegation_limit`, `role` or `permission` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all.
- One recorder and no mover: this story changes no case status, no task, no timer, no run and no summary, so a record can never move a case.
- No record without its event and no event without its record: the record, the chain link and the outbox row commit in one transaction, and a failure changes nothing and leaves the caller's feedback unwritten (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist, the sequence number is never reused, and a wrong record is corrected by a new record naming the one it corrects (REQ-DRI-002).
- One record per run and item: the idempotency key and the unique key make a second record impossible, and a repeated call returns the first record.
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb-decision` in namespace `rwb-recovery`, with the shared topic `rwb.decision-record.v1` for the record event; no story in this key declares another service's base or topic as its own (DP-13).
- One hop and 2 s on every call, with a breaker per downstream; a missing answer never produces a record from a guessed version or a guessed code.
- The record path is never gated by a feature flag and never skipped for speed: a verdict without its record is a defect, not a degraded mode.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the agent and prompt versions | Business Requirements Program, sections 5.7 and 5.4 | FEAT-DRI-02, FEAT-DRI-03, FEAT-DRI-04; legacy FEAT-AGT-07 | 06 Take over and own the case | R-UNI-32, R-UNI-39, CTL-06 | TC-E2-028-01, TC-E2-028-02, TC-E2-028-03, TC-E2-028-04, TC-E2-028-05, TC-E2-028-06, TC-E2-028-09, TC-E2-028-11 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Program, sections 5.7 and 5.4 | FEAT-DRI-02; legacy FEAT-AGT-07 | 06 Take over and own the case | CTL-11 | TC-E2-028-01, TC-E2-028-07, TC-E2-028-08, TC-E2-028-10 |

| Legacy reference | Where it is kept |
|---|---|
| One decision log entry per verdict, with decision D6, the agent version, the recommendation reference, the final call and the reason | Sections 1, 2, 4, 7 (AC1, AC3), 8 (BR1 to BR7) |
| MSG-P7-005 and the reason on a correction or a rejection | Sections 5 (X1), 7 (AC4), 8 (BR5), 14 |
| MSG-P7-003, R-UNI-39 and the block when the record cannot be written | Sections 5 (X2), 7 (AC5), 8 (BR9), 14 |
| MSG-GEN-004 and the one-feedback-per-run rule | Sections 5 (X3), 7 (AC6), 8 (BR10), 14 |
| MSG-P4-002, MSG-P4-003, RW-CASEOWN and RW-RISK | Sections 5 (X4, X5), 7 (AC7), 10, 14 |
| MSG-P1-001 and the data date of a verdict | Sections 7 (AC2), 8 (BR6), 14 |
| The legacy cases RW-2027-000501, 000502, 000503, 000601 and 000701, and policy INTAKE P2 mode L1 from 2027-01-25 | Background and scenarios of section 7; section 3 |
| Legacy key RWB-E2-028, story RWB-P7-E2028-APP, contract RWB-P10-E2028-CON | Metadata, sections 3 and 12 |
| Test cases TC-E2-028-01 to TC-E2-028-11 | Section 16 |
| Decoupling patterns DP03, DP07, DP09, DP10, DP13, DP15, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P10-E2028-APP and RWB-P10-E2028-CON the policy, the prompt, the run, the stored summary and gap flags, the guardrails, the mode, the panel, the feedback row and the acceptance measure; RWB-P3-E1035-APP the case record, the case status and `CaseCreated`; RWB-ITG-E2028-ITG the cross-service harness and the `-ITG` copies of the test cases.

### 19. Out of scope

- The agent policy, the prompt and its version, the agent run, the stored summary and the gap flags, the guardrails, the masked model call, the autonomy mode and its change, the panel "Agent summary" and its six states, the feedback row, the metrics job JOB-15 and SCR-46 Agent monitor: RWB-P10-E2028-APP, with the contract, the event schemas and the fakes in RWB-P10-E2028-CON.
- The case record, the case status, the case list, the stale warning on the panel and the case scope decision: RWB-P3-E1035-APP and `rwb-case`; the panel states are `rwb-agent`'s and the scope answer is `rwb-access`'s.
- The role model, the scope, the masking policy and the authorise answer: `rwb-access` (P4); this story consumes the answer and holds no rule of it.
- The decision-log store of this service — the append-only trigger, the grants, the chain verifier and the daily chain check JOB-14 at 02:00: the decision-log store slice (legacy RWB-E1-008) and the service baseline.
- The approval routing, the `ApprovalWorkflow`, the decision center screens SCR-10, SCR-11 and SCR-38 and the rule package registry: the other slices of `rwb-decision`.
- The acceptance and correction measure by segment and its extract: JOB-15 of `rwb-reporting` and the measure of RWB-P10-E2028-APP.
- The daily ledger seal to immutable storage and the lake copy: the seal is another slice's and the lake is removed (DP-17).
- The integration harness and the `-ITG` copies of the test cases: RWB-ITG-E2028-ITG.
- The ACE DB story, the infrastructure story and the deployment story of this legacy key: their own DB, INF and OPS stories; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability are the OPS story's.

The names of the level holders and substitutes and the parameter values of the DoA are data of their owners, and no date is changed by this story: the release 31 January 2027 is copied unchanged and stays tentative.
