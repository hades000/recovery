# RWB-P7-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2029-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not set; the squad sizes it at refinement |
| Patterns applied | DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-P7-AJ |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2029-CON; rwb-document contract for the document read; call-note field of the rwb-source-data contract |
| Contract fake library version | Not specified in the source documents (DOR-RWB-P7-E2029-APP-22) |
| Contract version built against | Not specified in the source documents (DOR-RWB-P7-E2029-APP-23) |
| Integration dependencies | None |
| SIT harness, SCREEN-S2 fixture pack, Enterprise AI test profile, evidence format and wave 2 release gate | Not specified in the source documents (GAP-0411); agree at the wave 2 entry check and hold as data files with this story |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-DVH-001, REQ-DVH-006) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-029 for rwb-decision, the dated L1 promotion record of the deviation screening agent on one segment and the decision record of each rejected proposal. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P7-E2029-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 25 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **risk and model risk officer (RW-RISK)**, I want **the promotion of the deviation screening agent to L1 on Mortgage cases in Bangkok to be a dated approval that this service records as one append-only, hash-chained decision record naming the evaluation run, the per-code scores, the conditions, the approver and the effective date, and every rejected proposal of that agent to be recorded the same way with the case owner's reason**, so that **the bank can show on any date which version of the screening policy was in force for which segment, on which evaluation it was promoted, and why a proposal was not followed**.

Inside `rwb-decision` this is the promotion-decision and rejection-record slice of the legacy story RWB-E2-029:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- One deliverable and nothing else: the decision. It gates a promotion to L1 on the stated conditions, holds the promotion as one `approval` row routed to the RW-RISK authority, appends one `decision_log_entry` when that approval is given, and appends one `decision_log_entry` for a rejected agent proposal. The scores, the run and the policy row stay with their owner.
- The record is written through the decision-record path of DP-03 and never through another service's table. The record, its chain link, the approval status and its outbox row commit together or not at all (R-UNI-39), and the row is never updated or deleted.
- The agent runtime is not here. The policy, the prompt, the run, the stored proposals, the mode (SHADOW or L1), the confidence marker, the panel "Proposed deviations" and its states, the feedback row and the evaluation sample stay in `rwb-agent` (P10, RWB-P10-E2029-APP and RWB-P10-E2029-CON). The deviation raise and R-DEV-01 stay in `rwb-deviation` (S8). The case status and the case record stay in `rwb-case` (P3). The role, the scope and the authorise answer stay in `rwb-access` (P4). This story raises no deviation, moves no case and stores no feedback.
- The legacy behaviour carried into the decision service is unchanged: the same one decision log entry per rejected proposal, with the proposed code as the decision, the agent version "SCREENING@P2/PR2", the reason, and final call "REJECTED"; the same refusal of a rejection with no reason; the same refusal of the whole action when the record cannot be written; the same refusal of a promotion whose scores miss a stated condition.

### 2. Business rationale

A promotion to L1 is the moment a model stops shadowing and starts proposing to a person, and it is a decision of the bank, not a deployment. The legacy story measures precision and recall per code, then lets RW-COE load an L1 proposal that RW-RISK approves. What makes that auditable is not the score table but the date and the terms: which version, which segment, which evaluation, which conditions, who approved and from when. NFR-033 requires every decision to be reproducible with the model, agent and prompt versions in force, and NFR-034 requires the version applied and the approver on every action; without this record the bank cannot answer why a Mortgage case in Bangkok was screened at L1 on a given day while a hire purchase case was not.

Under Architecture v5 the record and the approval are `rwb-decision`'s (slides 4, 13 and 41): every service writes its own decision record and publishes `DecisionRecorded`, and the approval routing and the central ledger sit here. The realignment changes the mechanism, not the business rule:

1. The `DecisionLogWriter` of the monolith becomes the local decision-record library and the shared topic of DP-03, written in the same transaction as the approval it records and hash-linked to the record before it.
2. The confidence floor, the promotion conditions and the effective-date discipline that were code branches become parameter and reference-data values read with the version in force (DP-06, DP-07), so a threshold or a segment scope is a row and not a release.
3. The agent facts — the evaluation scores, the run, the agent and prompt version, the data date — arrive on the P10 contract with a mock, one hop and a 2 s timeout (DP-11), and the ACE input freshness on the `rwb-source-data` contract or a `v_ace_*` view (DP-05); no `agent_*` row and no ACE table is read here.
4. The two published facts go out as CloudEvents with an outbox on this service (DP-09), so a redelivery never writes a second record and a repeat never consumes a second chain sequence.
5. Every path is on `/api/recovery/decision/v1` (DP-13) and every read is reached through the gateway-bff composite route the screens use (DP-19).

This story carries REQ-DVH-001 on the detection-terms side — the segment, the floor and the conditions that bound what the agent may propose — and REQ-DVH-006 on the record side: a confirmed or rejected flag is a matter of record with the version that produced it.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P10-E2029-CON | The published agent contract: the evaluation read (per-code precision and recall, sample size, sample and version), the run read (agent version, mode, status, data date) and the feedback transaction whose first step the rejection record is. The request and answer shapes are Not specified in the source documents (GAP-2402; ASM-3989) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the append, the hash link, the chain sequence and the outbox row in one transaction |
| RWB-PLT-E1042-CON, RWB-P3-E1042-CON | The parameter client library and the `rwb-case` parameters contract (DP-06): the confidence floor 0.80, the promotion conditions and the effective-date discipline, with the version in force |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` reference-data contract (DP-07): LOV-DECISION, LOV-APPROVAL-STATUS, LOV-APPROVAL-LEVEL, LOV-CAPABILITY and LOV-PRODUCT, with the version in force |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents (DP-09): one fact per record and one per approval request, relayed once |
| RWB-PLT-N001-CON | The gateway-bff composite route (DP-19) through which the approval and ledger reads are reached; this story adds no route |
| The authorise answer of `rwb-access` and the case read of `rwb-case` | The Decision log right and the scope of the reader; consumed on their published contracts or their fakes and carried in GAP-2402 (ASM-3995) |

Business preconditions carried from RWB-E2-029:

- SCREENING runs in shadow and scores per code on sample "SCREEN-S2" version 1, the business analysts' review of 500 shadow cases (legacy sections 3 and 7).
- Policy "SCREENING" version "P2" with prompt "PR2" is loaded for segment MORTGAGE and BKK, with the fallback and the measures, and RW-RISK approves it (legacy sections 3, 4 and 7).
- The L1 proposal states the condition "recall at least 0.75 for every code" and the confidence floor 0.80 (legacy AC10, BR6).
- The segment is a pair of values, product group MORTGAGE and region BKK; every other segment stays SHADOW (legacy BR1, AC3).
- The case owner holds RW-CASEOWN with Case record U and the case is in scope; the owner's verdict itself is `rwb-agent`'s (legacy sections 3 and 10).
- No build dependency. Day 1.

### 4. Flow

1. `rwb-agent` (P10): RW-COE runs the evaluation of "SCREENING" on sample "SCREEN-S2" version 1, and the precision and recall per code X1 to X7 with sample size 500 are stored there; this service reads them on the P10 contract and copies no score.
2. `rwb-agent` (P10): RW-COE loads the L1 proposal for policy "SCREENING" version "P2", prompt "PR2", segment MORTGAGE and BKK, effective 2027-01-26, with the conditions, the floor and the fallback, and calls this service's approval operation one hop with a 2 s timeout and a breaker.
3. `rwb-decision` `PromotionGate`: reads the conditions and the floor through DP-06 with the version in force, reads the evaluation run through the P10 contract, and refuses a proposal whose scores miss a stated condition with 422 and MSG-P10-001 naming the code, its value and the threshold (X1); nothing is created.
4. `rwb-decision` `ApprovalService`: writes one `approval` row with status "WAITING", source type "AGENT_POLICY", the policy version as its source reference, the capability area of rules and parameters, the product group MORTGAGE, the segment, the condition set and the RW-COE preparer, and builds the approval level from the delegation of authority read as reference data with its version (DP-07).
5. `rwb-decision` `ApprovalEvent`: the outbox row of `ApprovalRequested` is written in the same transaction, and the relay publishes it on `rwb.decision.events.v1`.
6. RW-RISK reads the item with `GET /api/recovery/decision/v1/approvals/{approvalId}` and approves it with `POST …/approve`. A user may not approve what that user prepared: refused with MSG-P7-002 and the item stays "WAITING" (X2). An approval above the level is held, not approved (X3).
7. `rwb-decision` `DecisionRecordAppendService`, one `RecordAndApply` transaction in `rwb_decision`: `decision_log_entry` is inserted with the promotion decision code, the evaluation run as its inputs reference, the recommendation as the condition set with the scores, the approver and the level, final call "APPROVED", decided time and the chain link; the `approval` row moves to "APPROVED" with that record as its `decision_log_id`; the outbox row for `DecisionRecorded` is written; the transaction commits. A failure rolls everything back and answers 503 with MSG-P7-003 (X4).
8. `rwb-decision` `DecisionRecordOutbox`: the relay publishes `rwb.decision.DecisionRecorded.v1` with the record ID as its key; `rwb-decision` and `rwb-reporting` consume it.
9. A case owner rejects a proposed code on the panel of `rwb-agent`; `rwb-agent` sends the verdict "REJECTED" for item key "X6" with the reason, and its feedback transaction waits on this service.
10. `rwb-decision` `ProposalRecordService`: validates the presence of the reason (422 with MSG-P7-005, X5), reads the run through the P10 contract for agent version "SCREENING@P2/PR2" and the data date, reads the case freshness on the `rwb-source-data` contract (DP-05); this service reads no ACE view or table, and appends one record with decision code "X6", final call "REJECTED", the reason as the override reason, the run as inputs and recommendation reference, and its chain link; the answer carries the record reference that `rwb-agent` stores as its feedback's decision reference.
11. Readers with the Decision log right R and the case in scope read the ledger with `GET /api/recovery/decision/v1/decision-log` and one record with `GET …/decision-log/{entryId}`, and see the decision, the agent version, the final call, the reason, the approver, the decided time and the two hashes; a role without the right is refused with 403 and MSG-P4-002, and a case outside the reader's scope with 404 (X6, X7).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A promotion is proposed and a code's score misses a stated condition (legacy AC10) | 422 before any row is written; nothing is created and the version in force is unchanged | MSG-P10-001 | AC2, TC-E2-029-10 |
| X2 | The user who prepared the promotion also approves it | Refused; the item stays "WAITING" and no record is written | MSG-P7-002 | AC4 |
| X3 | The approval needs a level above the caller's limit | The item is held at the level the delegation table names, not approved; no record and no refusal of the item | MSG-P7-001 | AC4 |
| X4 | The record cannot be written: the library fails, the insert fails or the connection is lost | The whole transaction rolls back; no record, no outbox row, the approval stays "WAITING" and the chain stands at its last entry; the incident is raised under R-UNI-39 | MSG-P7-003 | AC7, TC-E2-029-09, TC-E2-029-12 |
| X5 | A rejection arrives with an empty reason (legacy AC5) | 422 before anything is read or written; no record, no outbox row and no chain sequence consumed | MSG-P7-005 | AC6, TC-E2-029-05 |
| X6 | The reader holds no Decision log right, or the request reaches the service without the declared right | 403 and nothing returned | MSG-P4-002 | AC9, TC-E2-029-11 |
| X7 | The case of the record is outside the reader's scope | 404 and nothing returned | The authorise contract's out-of-scope message | AC9 |
| X8 | Two approvals of the same item arrive at once (legacy AC8) | The status guard and the unique key give one approval and one record; the second call is refused | MSG-GEN-004 | AC8, TC-E2-029-08 |
| X9 | A rejection arrives for a code that is already open on the case | No proposal is sent for that code, so no record is written and nothing is refused; the panel filter is `rwb-agent`'s | None to a user | AC5, TC-E2-029-07 |

A record is never updated and never deleted: a wrong record is corrected by a new record that names the one it corrects in `corrects_entry_id`, so the ledger stays append only. The record, its chain link, the approval status and its outbox row are always written together, so an approval cannot move without its record and a record cannot exist without its event.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P10-E2029-CON, the decision-record library and the parameter and reference-data contracts of its DP table, and their fakes; no agent runtime, no deviation flow and no case behaviour is rebuilt here |
| Negotiable | The floor, the conditions, the segment values, the approval level and the message texts are parameters, reference data or the message standard; the story fixes only one record per approval and per rejection, the chain and the fail-closed behaviour |
| Valuable | A promotion to L1 and a refusal to follow the agent are both dated, evidenced and attributable, which is what an auditor asks first |
| Estimable | One gate, one approval service, one append service, one chain writer, two reads, one migration |
| Small | Fits one sprint with its tests; it is the decision slice of the legacy key |
| Testable | Each of the nine criteria in section 7 runs as an automated test against the contract fakes and the decision-record library, with a fixed clock and a seeded chain |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent evaluation and L1 on one segment [E3b] — the rwb-decision promotion and rejection record

  Background:
    Given the environment is SIT
    Given the rwb-case parameters mock returns parameter "SCREENING_PROMOTION_CONDITIONS" with condition "recall at least 0.75 for every code" and the confidence floor 0.80 in force
    Given the rwb-agent contract mock returns evaluation run "EVAL-SCREEN-S2-01" on sample "SCREEN-S2" version 1 with sample size 500 and precision and recall per flag X1 to X7
    Given policy "SCREENING" version "P2" with prompt "PR2" has mode "L1" for segment MORTGAGE and BKK and mode "SHADOW" for every other segment

  Scenario: AC1 A promotion that meets its conditions is held as one dated approval (new, D-RCV-60)
    Given the evaluation of "SCREEN-S2" version 1 holds for X1 41 true positives, 4 false positives and 5 false negatives, so precision 0.9111 and recall 0.8913, and every code X1 to X7 meets "recall at least 0.75"
    When RW-COE loads the L1 proposal for policy "SCREENING" version "P2", segment MORTGAGE and BKK, effective 2027-01-26, and RW-RISK approves it
    Then one approval exists with source type "AGENT_POLICY", the policy version as its source reference, status "APPROVED" and its decision log reference set
    Then one decision record exists naming the evaluation run, sample size 500, the scores, the condition set, the confidence floor 0.80, segment MORTGAGE and BKK, prompt "PR2", the effective date 2027-01-26, the approver and the approval level
    Then the record's final call is "APPROVED" and it carries its chain sequence, its previous hash and its entry hash
    Then no score row and no policy row of rwb-agent is copied into rwb_decision

  Scenario: AC2 A promotion whose scores miss a condition is refused (new, D-RCV-60)
    Given the rwb-agent contract mock returns X4 recall 0.6000 in the evaluation of "SCREEN-S2" version 1
    When RW-COE loads an L1 proposal with condition "recall at least 0.75 for every code"
    Then the load is refused with 422 and MSG-P10-001 naming "X4 recall 0.6000 below 0.75"
    Then no approval and no decision record exists for the proposal and the version in force is unchanged

  Scenario: AC3 The record answers which version was in force on a date (new, D-RCV-60)
    Given the approval of "SCREENING" "P2" for segment MORTGAGE and BKK is effective 2027-01-26
    And the approval of "SCREENING" "P3" for the same segment is effective 2027-02-01
    When the ledger is read for policy "SCREENING" and segment MORTGAGE and BKK with the effective date on or before 2027-01-30 and again with the effective date on or before 2027-02-02
    Then the first read answers "P2" and the second answers "P3"
    Then neither read changes a row, and each answer names the evaluation run and the approver of the version it answers

  Scenario: AC4 The preparer cannot approve and a level above the limit is held (new, D-RCV-60)
    Given the approval item of "SCREENING" "P2" for segment MORTGAGE and BKK is "WAITING" and was prepared by RW-COE
    When the same user calls approve, and then a user whose limit is below the level the delegation table names calls approve
    Then the first call is refused with MSG-P7-002 and the item stays "WAITING"
    Then the second call is held with MSG-P7-001 at the level the delegation table names and no record is written
    Then the delegation limit and its version are read as reference data and never held as a constant

  Scenario: AC5 A rejected proposal is one record with the owner's reason (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000801" with agent "SCREENING", version "SCREENING@P2/PR2", mode "L1", proposing X6 on data as of 2027-01-25
    When rwb-agent sends the verdict "REJECTED" for item "X6" with reason "Customer answered on 2027-01-25"
    Then one decision record exists with decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED" and the reason as its override reason
    Then its inputs reference names the run and the data date 2027-01-25
    Then this story raises no deviation and stores no feedback row, and the answer carries the record reference rwb-agent stores

  Scenario: AC6 A rejection with no reason writes nothing (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000801" proposing X6
    When rwb-agent sends the verdict "REJECTED" for item "X6" with an empty reason
    Then the answer is 422 with MSG-P7-005
    Then no decision record and no outbox row is written and the chain sequence number is not consumed

  Scenario: AC7 The record cannot be written and nothing else moves (new, D-RCV-60)
    Given the rwb-agent contract mock returns the run of case "RW-2027-000801" proposing X6
    Given the decision-record library refuses the append and raises its unavailable condition
    When rwb-agent sends the verdict "REJECTED" for item "X6" with a reason
    Then the answer is 503 with MSG-P7-003
    Then no decision record and no outbox row exists for the run and the chain stands at its last entry
    Then rwb-agent stores no feedback for the run, because its transaction never commits
    Then an incident is raised under R-UNI-39 to the platform administration role

  Scenario: AC8 Two approvals of one item at once give one record (new, D-RCV-60)
    Given the approval item of "SCREENING" "P2" is "WAITING" and two sessions of RW-RISK hold it
    When both sessions approve it at the same time
    Then one approval is "APPROVED" and one decision record exists for it
    Then the second request is refused with 409 and MSG-GEN-004 and the chain gains no second link

  Scenario: AC9 The record is readable and the read is guarded (new, D-RCV-60)
    Given a decision record exists for case "RW-2027-000801" with decision "X6" and final call "REJECTED"
    Given the rwb-access contract mock returns the allow answer on the Decision log right R to the case owner and the refusal to role RW-PHONECOL, which holds Case record R only
    Given the rwb-case contract mock returns case "RW-2027-000802" in team "HP-NE" outside the reader's scope
    When the case owner sends GET /api/recovery/decision/v1/decision-log for case "RW-2027-000801" and GET …/decision-log/{entryId}, and role RW-PHONECOL sends the same page read, and the owner reads case "RW-2027-000802"
    Then the page and the single read carry decision "X6", agent version "SCREENING@P2/PR2", final call "REJECTED", the decided time, the previous hash and the entry hash
    Then role RW-PHONECOL is refused with 403 and MSG-P4-002 and the out-of-scope case is refused with 404

  Scenario: AC10 The inputs reference names the ACE input and its date from the contract (new, D-RCV-60)
    Given the rwb-source-data contract fake returns the appraisal date 2027-01-25 for the case "RW-2027-000801"
    When rwb-agent sends the verdict "REJECTED" for item "X6" with reason "Customer answered on 2027-01-25"
    Then the inputs reference of the record names the ACE input and the data date 2027-01-25
    Then this service reads no ACE view or table to build the record

  Scenario: AC11 The record is append only and hash chained (new, D-RCV-60)
    Given one decision record exists for case "RW-2027-000801" with decision "X6" and final call "REJECTED"
    When a second record is appended for the same case and a caller sends an update or a delete of the first record
    Then the second record's previous hash equals the entry hash of the first and its chain sequence number is the next one
    Then the update and the delete leave the first record unchanged, and a wrong record is corrected only by a new record that names the one it corrects

  Scenario: AC12 The record holds no personal data (new, D-RCV-60)
    Given one decision record exists for case "RW-2027-000801" with decision "X6" and final call "REJECTED"
    When the record, its outbox event, its trail and its logs are read
    Then each carries case and run identifiers, codes, versions, the reason, user references and dates only

  Scenario: AC13 A record changes no case value (new, D-RCV-60)
    Given the case "RW-2027-000801" holds its current status, tasks, timers and deviations
    When the rejection of "X6" is recorded
    Then no case status, no task, no timer and no deviation is set or changed for case "RW-2027-000801" by this story
    Then the pause of R-DEV-01 is not set here and stays with rwb-deviation on a confirmation

  Scenario: AC14 The rules with no criterion hold on the record path (new, D-RCV-60)
    Given one decision record exists for case "RW-2027-000801" with decision "X6" and final call "REJECTED"
    When the approval of "SCREENING" "P2" for segment MORTGAGE and BKK is read with its approver and level, the inputs reference of the record is read, and the record is read with its outbox event and trail
    Then the approver is not the preparer and the approval level and its delegation version are on the record
    Then the inputs reference names the ACE input and its date from the rwb-source-data contract only
    Then the record, its event and its trail carry no personal data and no case status, task, timer or deviation is set or changed

  Scenario: AC15 A call without a valid credential is answered 401 (new, D-RCV-60)
    Given no valid credential is presented
    When the caller sends POST /decision-log, POST /approvals/{approvalId}/approve, GET /approvals and GET /decision-log
    Then each call is answered 401 and no approval, decision record or outbox row is written

  Scenario: AC16 A replay of a write with the same idempotency key gives the first record (new, D-RCV-60)
    Given a rejection of "X6" for case "RW-2027-000801" was recorded with an idempotency key
    When the same write is sent again with the same idempotency key
    Then the answer is Not specified in the source documents (NEWAC-RWB-P7-E2029-APP-AC13) and nothing new is written
```

`acs` is empty for this story: no legacy criterion is owned verbatim here. Every legacy criterion of RWB-E2-029 either reads or drives the agent panel, the run and the feedback row — AC1's evaluation and stored scores, AC2's panel and confirm path, AC3's shadow answer, AC6's low-confidence marker, AC7's filter and AC8's feedback refusal — and those belong to `rwb-agent` (P10). The sixteen criteria above are new for the `rwb-decision` slice and test only the promotion decision and the rejection record; their values are the legacy values of RWB-E2-029 sections 3, 4, 7 and 8 — sample "SCREEN-S2" version 1 with 500 cases, X1 with 41 true positives, 4 false positives and 5 false negatives giving precision 0.9111 and recall 0.8913, the condition "recall at least 0.75 for every code", X4 recall 0.6000, the confidence floor 0.80, policy "SCREENING" version "P2" with prompt "PR2", segment MORTGAGE and region BKK, agent version "SCREENING@P2/PR2", cases `RW-2027-000801` and `RW-2027-000802`, the reason "Customer answered on 2027-01-25", and roles RW-COE, RW-RISK and RW-CASEOWN — and no new business value is introduced.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One decision record per approval of a promotion and one per rejected proposal, and no approval and no rejection exists without its record | REQ-DRI-001; R-UNI-39; legacy BR4 |
| BR2 | A promotion to L1 is refused when any code named by the stated condition misses it, and the refusal names the code, its score and the threshold | Legacy BR7 and AC10; CTL-08; MSG-P10-001 |
| BR3 | The promotion names its segment as a pair of values, product group and region; every case outside the pair stays SHADOW and this service makes no exception | Legacy BR1 and AC3; `agent_policy.segment_product_group`, `segment_region_code` |
| BR4 | The condition set, the confidence floor 0.80, the segment values and the approval level are parameter or reference-data values read with the version in force; none is a constant of the code | Legacy BR1, BR6, BR7; DP-06; DP-07; FSD P7 A2.1.3.1 BR-P7-001 |
| BR5 | A promotion is approved by a user other than its preparer, and the level applied is the one the delegation of authority names at the moment of the decision, with its version on the record | FSD P7 A2.4.3.1 VR-P7-004-1 and VR-P7-004-2; legacy section 10; NFR-034; MSG-P7-001; MSG-P7-002 |
| BR6 | A rejection needs a reason, which is written as the override reason of the record before the feedback of `rwb-agent` is stored; an empty reason is refused | Legacy BR4 and AC5; CTL-07; MSG-P7-005 |
| BR7 | The decision of a rejection is the proposed code X1 to X7 and the final call is REJECTED; the code is a value of LOV-DECISION read with the version in force (ASM-3991) | Legacy AC4 and section 14; TSD P7 v2 T3.1 (DF-DEC-003); DP-07 |
| BR8 | The record names the agent and prompt version of the run and the data date, taken from the owner of the run and never from the caller, so a decision taken on stale data is visible | TSD P7 v2 T3.1 (DF-DEC-007, DF-DEC-008); NFR-033; legacy AC1 |
| BR9 | The inputs reference of a record names the ACE input and its date, read on the `rwb-source-data` contract only; no ACE view or table is read | DP-05; legacy section 11 DF-ACE-193 |
| BR10 | The record is append only and hash chained: an entry hash over its canonical form, a previous hash equal to the entry hash before it, a sequence number never reused, and no update and no delete; a wrong record is corrected by a new record that names the one it corrects | REQ-DRI-002; TSD P7 v2 T3.1 (DF-DEC-017, DF-DEC-018, DF-DEC-028, DF-DEC-029) |
| BR11 | The record, its chain link, the approval status and its outbox row commit in one transaction, and no approval proceeds when the record cannot be written | REQ-DRI-005; R-UNI-39; DP-03; MSG-P7-003 |
| BR12 | One approval per item and one record per approval: the status guard and the unique key make a second approval impossible, and the second call is refused with 409 | R-UNI-40; DP-09; legacy AC8 |
| BR13 | The approval and the ledger are read under the Decision log right A or R and the caller's scope; the right is `rwb-access`'s to answer and the scope filter is applied to the case read of `rwb-case` | TSD P7 v2 T6.1 and T6.2; FSD P7 T-A.1; legacy section 10 and X8 |
| BR14 | No personal data in the record, the events, the trail or the logs: case and run identifiers, codes, versions, a condition set, scores, a reason, user references and dates only | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43; REQ-ACA-005 |
| BR15 | No case value changes because of a record: no case status, no task, no timer and no deviation is set here; the pause of R-DEV-01 is `rwb-deviation`'s on a confirmation | Legacy section 9 and section 17; R-DEV-01 |

### 9. State transitions

The states below are the states of an approval item and of a record of this service. The case, the run, the proposals and the panel are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A promotion is proposed with a condition set and an effective date | Every named code meets its condition | WAITING, with one `ApprovalRequested` in the outbox |
| Absent | A promotion is proposed and a code misses its condition | The gate refuses the request | Absent: 422 with MSG-P10-001 and nothing written |
| WAITING | The preparer calls approve | Preparer and approver are the same user | WAITING: MSG-P7-002, no record |
| WAITING | An approver below the required level calls approve | The level is above the caller's limit | HELD_NO_LIMIT with MSG-P7-001, no record |
| WAITING | An approver within the level calls approve | The record, the chain link and the outbox row commit | APPROVED, with one record and a chain sequence |
| WAITING | The record cannot be written | The transaction rolls back | WAITING: 503 with MSG-P7-003 and the chain at its last entry |
| WAITING | A second approval arrives for the same item | The status guard and the unique key hold | APPROVED once: the second call is 409 with MSG-GEN-004 |
| WAITING | The approver returns or refuses the item | A reason is given | RETURNED or REFUSED, with one record and its reason |
| APPROVED, RETURNED, REFUSED | Any later change | Through a new record only | Unchanged: the item is never edited in place |
| Absent | A rejection arrives for a proposed code with a reason | The run answers and the reason is present | Appended, with its chain sequence, previous hash and entry hash |
| Absent | A rejection arrives with an empty reason | The validation refuses the request | Absent: 422 with MSG-P7-005 and no sequence consumed |
| Absent | A rejection arrives for a code already open on the case | No proposal was sent, so no rejection arrives | Absent: nothing written and nothing refused |

The final call moves only through a new record, never through an update. The approval status moves through the four values of LOV-APPROVAL-STATUS and no other.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, the center of excellence analyst | Runs the evaluation in `rwb-agent` and loads the L1 proposal; prepares the approval item (Rules and parameters C) |
| RW-RISK, the risk and model risk officer | Approves, returns or refuses the promotion within the level the delegation of authority names (Rules and parameters A), and reads the record of the version it approved the use of |
| RW-CASEOWN, the case owner | Gives the verdict on a proposal through `rwb-agent`, and reads the record of a case in scope in the ledger (Decision log R) |
| RW-CONDUCT, the conduct and QA officer | Reads the scores and the records of the promotions (Rules and parameters R) |
| SY-AGENT | Calls the approval and the append on behalf of `rwb-agent`, one hop, under the service identity; holds no user right and writes nothing else |
| SY-DECLOG and the decision-record library identity | Write the record, the hash link and the outbox row in one transaction and publish on `rwb.decision-record.v1` (DP-03) |
| The `rwb-decision` service identity | Writes its own `rwb_decision` rows and reads the evaluation and the run on the P10 contract (`rwb-decision` login, DP-02) |
| `rwb-agent` (P10) | Owns the policy, the prompt, the run, the proposals, the mode, the panel, the feedback row and the evaluation sample; this story holds none of them |
| `rwb-deviation` (S8) | Owns the raise of a deviation and the pause of R-DEV-01; this story neither raises nor pauses |

The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-2402; ASM-3993); the story refers to "the `rwb-decision` login (DP-02)". The authorisation decision is `rwb-access`'s and is consumed as the authorise answer each read declares.

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write on a rejection record; empty on a promotion record (see the note below) |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, a value of LOV-DECISION: the code X1 to X7 on a rejection, the promotion decision code on a promotion (ASM-3990) |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Write when the promotion came from a rule-parameter row; otherwise empty |
| DF-DEC-006 | `decision_log_entry` | model_version | Write where the run names it |
| DF-DEC-007 | `decision_log_entry` | agent_version | Write, "SCREENING@P2/PR2" from the run |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the evaluation run reference on a promotion and the run reference with the data date on a rejection |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the condition set with the per-code scores and the floor on a promotion; the run reference on a rejection |
| DF-DEC-010 | `decision_log_entry` | approver_user_id | Write, the approver of a promotion or the owner who rejected |
| DF-DEC-011 | `decision_log_entry` | approval_level | Write on a promotion; empty on a rejection |
| DF-DEC-012 | `decision_log_entry` | final_call | Write, APPROVED, RETURNED, REFUSED or REJECTED |
| DF-DEC-013 | `decision_log_entry` | override_reason | Write on a refusal, a return and a rejection |
| DF-DEC-014, DF-DEC-015 | `decision_log_entry` | actions, outcome | Write the action taken; the outcome on the case stays `rwb-agent`'s and `rwb-deviation`'s |
| DF-DEC-016 | `decision_log_entry` | decided_at | Write, the moment of the decision, and on a promotion its effective date in the recommendation |
| DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on a record that corrects an earlier one |
| DF-DEC-030, DF-DEC-031 | `decision_log_entry` | actor_user_id, idempotency_key | Write |
| DF-DEC-032 to DF-DEC-053 | `approval` | all fields | Write the item: source type "AGENT_POLICY", the policy version as its source reference, the capability area, the product group, the level, the preparer, the status, the due time, the escalation level and the decision log reference |
| DF-CAS-001, DF-CAS-003, DF-CAS-012 | `recovery_case` | id, product_group, region_code | Read through the P3 case read, for the scope filter and the segment check |
| DF-AGT-089, DF-AGT-090, DF-AGT-095, DF-AGT-096 | `agent_evaluation` | label_key, sample_size, precision_value, recall_value | Read through the P10 evaluation read; never copied |
| DF-AGT-036, DF-AGT-038, DF-AGT-043, DF-AGT-046, DF-AGT-050, DF-AGT-059, DF-AGT-060 | `agent_run` | id, agent_version, autonomy_mode, status, confidence, segment fields | Read through the P10 run read |
| DF-ACE-193 | rwb-source-data contract | appraisal_date | Read for the data date of the inputs reference (DP-05), never copied |
| (outbox) | library table in `rwb_decision` | the `DecisionRecorded` and `ApprovalRequested` rows | Write |

No row of `agent_policy`, `agent_run`, `agent_evaluation` or `agent_feedback` is copied into `rwb_decision`, and no `recovery_case`, `deviation` or `assignment` row is written. `approval.case_id` is required by the TSD for the case approvals of this service, and a policy promotion has no case; the case-less promotion row and the columns that carry its segment are Not specified in the source documents (GAP-2402; ASM-3992), so the segment and the condition set are held in the source reference and the terms of the row. Field IDs are those in the Logical Data Model and Data Dictionary v9.

### 12. Contract

Until the values of GAP-2193, GAP-2194 and GAP-2402 are published, the story uses the placeholders and assumed shapes of the sources and builds no code value for them.

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The six approval and ledger operations are API-P7-002 to API-P7-008 of TSD P7 v2 T-A.1, minus the recommendation read. The append on the decision-log collection is the write path DP-03 and DP-11 need and is Not specified in the source documents (GAP-2402; ASM-3989); the request and answer field sets of all eight operations are the same placeholder.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/decision-log` | Append one record for one promotion, refusal, return or rejection: validate, chain and write, then answer 201; a repeated key answers 200 with the first record | Service identity, SY-AGENT and SY-DECLOG (TSD P7 v2 T6.1, right C); one hop from `rwb-agent` with a 2 s timeout | Idempotency-Key header, kept on the record |
| GET | `/decision-log` | API-P7-006: search the ledger by case, decision, rule, approver and date, one page at a time | Decision log, right R, scope applied | Not applicable |
| GET | `/decision-log/{entryId}` | API-P7-007: read one record with its inputs, versions, final call, reason and two hashes | Decision log, right R, scope applied | Not applicable |
| GET | `/approvals` | API-P7-002: list the items waiting for the caller's level | Decision log, right A, scope applied | Not applicable |
| GET | `/approvals/{approvalId}` | API-P7-008: read one item with its routing, limit and age | Decision log, right A, scope applied | Not applicable |
| POST | `/approvals/{approvalId}/approve` | API-P7-003: approve within the caller's limit and answer with the record | Decision log, right A, scope applied | Idempotency-Key header |
| POST | `/approvals/{approvalId}/return` | API-P7-004: return the item to its preparer with a reason | Decision log, right A, scope applied | Idempotency-Key header |
| POST | `/approvals/{approvalId}/refuse` | API-P7-005: refuse the item with a reason and answer with the record | Decision log, right A, scope applied | Idempotency-Key header |

The append request this story assumes carries `caseId` (empty on a promotion), `sourceType`, `sourceRef`, `itemKey` (the proposed code or the policy version), `decisionCode`, `finalCall`, `reason`, `effectiveDate`, `recommendation`, `idempotencyKey` and `decidedAt`; the agent version and the data date are read from the run and not from the request. Errors: 401 no session (Not specified in the source documents (CG-ALL-7355)); 403 the role holds no right (MSG-P4-002); 404 the record, the item or the case is absent or out of scope (Not specified in the source documents (CG-ALL-7355)); 409 the item already moved or the key repeats a different body (MSG-GEN-004); 422 a reason is missing (MSG-P7-005), a promotion misses a condition (MSG-P10-001) or a value is not of its list (MSG-P7-009); 503 the record was not written (MSG-P7-003). Every error that has a message ID is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-evaluations/{evaluationRunId}` | P10 rwb-agent, on RWB-P10-E2029-CON | The per-code precision and recall, the sample and its size, and the condition check of the promotion gate; faked, one hop, 2 s |
| GET | `/api/recovery/agent/v1/agent-runs/{runId}` | P10 rwb-agent, on RWB-P10-E2029-CON | The agent and prompt version, the mode, the status and the data date of a rejection record; faked |
| GET | `/api/recovery/case/v1/parameters/{parameterCode}` | P3 rwb-case (DP-06) | The promotion conditions, the confidence floor 0.80 and the effective-date discipline, with the version in force; faked |
| GET | `/api/recovery/case/v1/reference-data/{listCode}` | P3 rwb-case (DP-07) | LOV-DECISION, LOV-APPROVAL-STATUS, LOV-APPROVAL-LEVEL, LOV-CAPABILITY and LOV-PRODUCT, with the version in force; faked |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The owner, team, region and product group of the scope filter and of the segment check; faked |
| GET | `/api/recovery/source-data/v1/...` | P1 rwb-source-data, or this service's `v_ace_valuation` view (DP-05) | The appraisal date of the ACE input named in the inputs reference; the operation is Not specified in the source documents (GAP-2402; ASM-3989) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The cached decision of the Decision log right A or R and the writer's scope; faked |

The P10 operations are named by RWB-P10-E2029-CON and by legacy section 12; the P3 operations are the parameter and reference-data contracts of the DP table of this key; the P1 and P4 operations are the DP-05 and DP-08 markers of the ownership rows. DP-08 is not among the patterns of this key, so the authorise answer is consumed against its published contract or its fake and the dependency is carried in GAP-2402 (ASM-3995). Every call is one hop with a 2 s timeout and a breaker per downstream.

#### 12.3 Events published

| Event | Topic | Owner | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7, published by this service | entryId | record ID, case ID where there is one, decision code, agent version, evaluation run or inputs reference, final call, decided at, chain sequence, entry hash |
| `rwb.decision.ApprovalRequested.v1` (EV-09) | `rwb.decision.events.v1` | P7, published by this service | approvalId | Not specified in the source documents (CG-ALL-7357) |

Both events are written to the outbox in the same transaction as the row they announce and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform (DP-09); the record event uses the shared topic `rwb.decision-record.v1` and the approval event the service topic. The third event the Ownership Map gives this service, EV-30, is not published by this story and its name and payload are Not specified in the source documents this story may read (GAP-2402; ASM-3994). No event carries a name, an e-mail address, a mobile number, an account number or a proposal text.

#### 12.4 Events consumed

None. The verdict and the promotion arrive on the append and approval requests, and the evaluation and the run on the P10 reads. The inbox objects of DP-09 are created in the schema by the service baseline and this story writes none.

#### 12.5 Workflows and activities

None of this story's own. The approval is one synchronous operation inside the writer's unit of work and the ledger read is a query. `ApprovalWorkflow` and the workflow kit belong to other slices of `rwb-decision`; this story starts no workflow, signals none and registers no activity and no Schedule on the `rwb-decision` queue.

#### 12.6 Schedules

None. The three jobs the ownership rows give this service — JOB-13, JOB-14 and JOB-20 — belong to other slices: the lake copy JOB-13 is removed with the lake (DP-17), the chain check JOB-14 is the decision-log store's, and JOB-20 is another slice's. This story adds no Schedule and polls nothing.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The record of a promotion, a return, a refusal and a rejection: the code, the versions, the inputs, the recommendation, the final call, the reason, the hashes and the chain sequence; written once and read |
| `approval` | P7 (`rwb_decision`) | The promotion item: source type and reference, capability area, product group, level, preparer, status, due time and decision log reference |
| outbox and idempotency library tables | PLT library, created in `rwb_decision` | The `DecisionRecorded` and `ApprovalRequested` rows and the stored answer of a repeated call (DP-09) |

Not owned and never read by this story: `agent_policy`, `agent_prompt`, `agent_run`, `agent_evaluation` and `agent_feedback` (P10), `recovery_case`, `deviation` and `assignment` (P3 and S8), `delegation_limit`, `role`, `permission` and `masking_rule` (P4). No foreign key crosses a schema and no row of another service is copied (DP-01). `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are this service's but another story's, and this story writes none of them.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-agent contract fake | RWB-P10-E2029-CON | Evaluation run "EVAL-SCREEN-S2-01" on "SCREEN-S2" version 1, 500 cases, X1 41/4/5 and every code above 0.75; the same run with X4 recall 0.6000; the runs of cases `RW-2027-000801` and `RW-2027-000802` with version "SCREENING@P2/PR2", mode "L1" and "SHADOW" and data as of 2027-01-25; a forced failure of the feedback transaction for AC7 |
| rwb-case fake | The case, parameter and reference-data reads of P3 | Case `RW-2027-000801` in MORTGAGE and BKK, case `RW-2027-000802` in HIRE_PURCHASE and BKK and outside the reader's scope; parameter "SCREENING_PROMOTION_CONDITIONS" with the condition and the floor 0.80; the five lists with their versions |
| rwb-access fake | The P4 authorise call | The allow answer on the Decision log rights A and R for the approver and the case owner, and the refusal for role RW-PHONECOL (MSG-P4-002) |
| rwb-source-data fake | The P1 freshness read of DP-05 | The appraisal date that the inputs reference of a rejection names |
| decision-record fake | RWB-PLT-E1027-CON | The append, the chain sequence allocation and the hash link; the chain verifier over a seeded ledger; a forced failure and an unavailable condition for AC7 and TC-E2-029-12 |

Each fake is replaced by the real service as its contract lands, without a change to the criteria.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 8, consumed 7 | The approval and ledger operations provided; the evaluation and run reads, the parameter and reference-data reads, the case read, the freshness read and the authorise call consumed, one hop each with the 2 s timeout |
| Kafka | Published 2 event types, consumed 0 | `rwb.decision.DecisionRecorded.v1` on the shared topic and `rwb.decision.ApprovalRequested.v1` on the service topic; nothing consumed |
| Temporal | None | No workflow, no activity and no Schedule registered; `ApprovalWorkflow` stays with its own slice |
| File | None | No file input and no file output |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `promotion/screening`, Java package `th.co.scb.ace.workbench.recovery.decision.promotion`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the core: the legacy `DecisionLogWriter` becomes the local decision-record library, which writes the record, the chain link, the approval status and the outbox row in one transaction. DP-06 and DP-07 carry every business value of the key — the condition set, the floor 0.80, the segment pair, the codes, the statuses and the approval level — with their versions, so a threshold or a limit is a row and not a release. DP-11 is the one hop to `rwb-agent` for the evaluation and the run, against the published contract and its fake. DP-05 gives the freshness of the ACE input without a read of an ACE table. DP-09 is the outbox and the CloudEvents envelope of the two published facts. DP-13 puts the eight operations on `/api/recovery/decision/v1` and DP-19 is the composite route through which the approval and ledger reads are reached; this story adds no route and serves no screen of its own.

The platform H dependencies of the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-N001-CON) and the two C dependencies that DP-06 and DP-07 bring (C RWB-P3-E1042-CON, C RWB-P3-E1043-CON) are not in the metadata rows of this story, which name None and RWB-P10-E2029-CON; they are the dependencies the DP table adds and they are recorded in GAP-2402 and ASM-3995. None of them blocks the build beyond Day 1: they are platform contracts of wave 0 and published contracts of another service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PromotionRecordController | Controller | The append on `POST /decision-log` with the shape and idempotency validation, and the 201 and 200 answers |
| ApprovalController | Controller | `GET /approvals`, `GET /approvals/{approvalId}`, `POST …/approve`, `…/return`, `…/refuse` with the guard and the problem mapping |
| DecisionRecordController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the guard, the scope and the page |
| PromotionGate | Service | Reads the condition set and the floor of DP-06 and the evaluation of the P10 contract, and refuses a promotion that misses a condition with MSG-P10-001 |
| ApprovalService | Service | Writes the item with its level, its preparer, its status and its source reference; moves it through LOV-APPROVAL-STATUS; refuses a self-approval with MSG-P7-002 and holds a level above the limit with MSG-P7-001 |
| ProposalRecordService | Service | Validates the reason of a rejection, reads the run for the agent version and the data date, and builds the record |
| ChainWriter | Service | Reads the head of the chain under the append lock, computes the entry hash over the canonical form and builds the previous hash and the sequence number |
| DecisionRecordAppendService | Service | One `RecordAndApply` transaction: the record, the chain link, the approval status and the outbox row, or nothing; maps a failure to 503 with MSG-P7-003 |
| DecisionRecordQueryService | Service | The ledger page and the single record with the scope filter applied to the case read |
| AgentContractClient | Adapter | The evaluation and run reads of RWB-P10-E2029-CON, one hop with a 2 s timeout and a breaker |
| ParameterClient, ReferenceDataClient | Client | The DP-06 and DP-07 reads with the version in force |
| AccessCheckClient, CaseScopeClient | Client | The authorise answer behind every read and the P3 case read of the scope filter |

**Database and migrations**

- Writes `decision_log_entry`, `approval` and the outbox and idempotency objects of the library, all in schema `rwb_decision`; reads no other schema.
- The `decision_log_entry` baseline, its append-only trigger and its grants belong to the decision-log store slice of this service (legacy RWB-E1-008), and the `approval` baseline to the approval routing slice; this story widens neither.
- Migration in this story, in the per-service Flyway sequence: adds the unique key of `decision_log_entry (chain_seq)`, the unique key of the idempotency key, the index of the ledger read by case and decided time, the unique key that holds one record per approval on `approval (source_type, source_ref, status)` where the status is APPROVED, and the foreign key of `approval.decision_log_id` to `decision_log_entry (id)`.
- No row is updated except the status and the decision log reference of `approval`; no record row is ever updated or deleted.

**Configuration and reference data**

- The condition set "recall at least 0.75 for every code" and the confidence floor 0.80 are parameter values read through DP-06 with the version in force; the segment pair MORTGAGE and BKK, the codes X1 to X7 and the statuses are reference-data values through DP-07.
- The approval level and its limit come from the delegation of authority read with its version at the moment of the decision, and the version used is written on the record (BR5).
- The promotion decision code is a value of LOV-DECISION and its value is Not specified in the source documents (GAP-2402; ASM-3990); the story validates against the list and never hard-codes the code.
- The feature switch of the legacy capability, `rwb.agent.screening-l1`, stays with RWB-P10-E2029-APP and is not read here: a record that could be switched off would break R-UNI-39 (ASM-3996).
- The `rwb-decision` login of DP-02, the Flyway user and the outbox relay identity are environment configuration and not values of this story.

**Build steps**

1. The migration with the two unique keys of the ledger and the one record per approval; test that a repeated chain sequence, a repeated idempotency key and a second approval are refused by the constraints (BR10, BR12, X8).
2. `PromotionGate` with the DP-06 conditions and the P10 evaluation read, and the refusal naming code, value and threshold; tests for AC2 and TC-E2-029-10.
3. `ApprovalService` with the item, the level, the preparer and the status machine; tests for AC1, AC4 and TC-E2-029-01.
4. `ChainWriter` with the head read, the canonical form and the entry hash; test the seeded chain and the first record with the previous hash of 64 zeros (AC1, AC5).
5. `ProposalRecordService` and `DecisionRecordAppendService` with the reason rule and the fail-closed transaction; tests for AC5, AC6, AC7, TC-E2-029-04, TC-E2-029-05, TC-E2-029-09 and TC-E2-029-12.
6. The parallel approval path and its 409; tests for AC8 and TC-E2-029-08.
7. `DecisionRecordController` and `DecisionRecordQueryService` with the authorise answer, the scope filter and the page; tests for AC9 and TC-E2-029-11.
8. The freshness read of DP-05 and the data date on the inputs reference; test for AC5.
9. The privacy test: no record, event payload or log carries a name, an e-mail address, a mobile number, a national identity number or an account number (AC1, AC5).

**Done when.** The tests in section 16 pass, the contract tests of RWB-P10-E2029-CON stay green, and a SIT day shows one dated promotion record for MORTGAGE and BKK with its evaluation run and condition set, a promotion refused when a code misses a condition, one record per rejected proposal with the reason and the agent version "SCREENING@P2/PR2", a chain that verifies from its first entry, one event per record and per approval request, no record and no feedback row when the record cannot be written, and no personal data in any record, event or log.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-005 | A rejection carries no reason | Enter the reason you are not following the recommendation. | This story, on the append |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append transaction |
| MSG-P10-001 | A promotion misses a stated condition | The {kind} file for {agent} was refused: {check}. The version in force is unchanged. | This story, on the gate; the message id is the agent's and the check is the condition set |
| MSG-P7-002 | The preparer approves what the preparer prepared | You prepared this decision, so you cannot approve it. | This story, on the approval |
| MSG-P7-001 | The approval needs a level above the caller's limit | This needs approval at level {level}. It has been sent to {approver}. | This story, on the approval; the level and the approver are reference-data values |
| MSG-P7-009 | A code, a final call or a required version is not a value it must have | Not specified in the source documents (GAP-2402; ASM-3990) | This story, on the validation; the FSD names only the identifier and the field |
| MSG-GEN-004 | The item already moved, or a second approval arrives | Someone else changed this record. Reload it to see their change. | This story, on the approval |
| MSG-P4-002 | The reader holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer |
| MSG-S8-001 | A deviation is raised after a confirmation | {deviation} was raised. The case is with {handler}. | `rwb-deviation`, on the confirmation; this story produces no message |

MSG-P7-005, MSG-P7-003, MSG-P10-001, MSG-GEN-004, MSG-P4-002 and MSG-S8-001 are copied unchanged from the legacy story RWB-E2-029 section 14. MSG-P7-002, MSG-P7-001 and MSG-P7-009 are the messages of FSD P7 v3 A2.1, A2.4 and A2.2, whose identifiers and texts this story copies as they stand; the text of MSG-P7-009 is not written out in any source this story may read, so the placeholder stands. Thai text for each message follows decision DL10, which stays open; its assumptions are ASM-2250, ASM-2357, ASM-2377 and ASM-2863.

### 15. Screens and states

No screen is built in this story. The panel "Proposed deviations" on SCR-03 Case record and its four states — empty, ready, low confidence and recorded — belong to RWB-P10-E2029-APP, and this story neither renders nor hides them. The item and the records are read through the operations of section 12.1 and shown by the approval queue and the decision-log query screens of this service's other slices; the composite route of DP-19 is used and not extended.

| Where | State | What the reader sees |
|---|---|---|
| `POST /decision-log` | 201 Appended | The record reference, the chain sequence, the entry hash and the decided time |
| `POST /decision-log` | 200 Already recorded | The first record of the same item with its own reference; nothing new is written |
| `POST /decision-log` | 422 No reason, or a value out of its list | MSG-P7-005 or MSG-P7-009, naming the field, and nothing written |
| `POST /decision-log` | 503 Record not written | MSG-P7-003 and nothing written; the caller's feedback is rolled back |
| `POST /approvals/{approvalId}/approve` | 200 Approved | The record reference, the level applied and the effective date |
| `POST /approvals/{approvalId}/approve` | Refused or held | MSG-P7-002 for a self-approval, MSG-P7-001 for a level above the limit, MSG-GEN-004 for a second approval |
| `GET /approvals`, `GET /approvals/{approvalId}` | One page, one item | The policy version, the segment, the condition set, the level and the age of the item |
| `GET /decision-log`, `GET /decision-log/{entryId}` | One page, one record | The decision, the agent version "SCREENING@P2/PR2", the final call, the reason, the approver, the decided time and the two hashes |
| `GET /decision-log` | 403 or 404 | MSG-P4-002 for a role without the right; nothing returned for a case out of scope |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

The states of SCR-03 for this story are empty, loading, error and no access; all four are Not specified in the source documents (CG-ALL-7363).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-029-11 | AC9, BR13 | Component | RW-PHONECOL, which holds Case record R only, reads the ledger and is refused with MSG-P4-002; a case outside the scope answers 404 |
| TC-E2-029-01 | AC1, AC2, BR2, BR4 | Contract | "SCREEN-S2" version 1 with 500 cases; X1 counts 41, 4 and 5; every code above 0.75 and one run with X4 at 0.6000 |
| TC-E2-029-02 | AC2, BR1, BR3, BR4, BR8 | Contract | Mortgage case `RW-2027-000801` in BKK, complaint note 2027-01-26, promotion effective 2027-01-26 |
| TC-E2-029-03 | AC3, BR3 | Component | Hire purchase case `RW-2027-000802` in BKK; the segment answer is SHADOW and no promotion record names it |
| TC-E2-029-04 | AC4, BR6, BR7 | Component | Reject X6 with the reason "Customer answered on 2027-01-25"; one record with the reason |
| TC-E2-029-05 | AC5, BR6 | Component | Reject X6 with an empty reason; 422 MSG-P7-005 and nothing written |
| TC-E2-029-06 | AC6, BR4 | Component | X2 with confidence 0.72; the floor 0.80 is a parameter value named on the record and no score is copied |
| TC-E2-029-07 | AC7, X9 | Component | X1 already open on the case; no proposal is sent, so no record is written |
| TC-E2-029-08 | AC8, BR12 | Component | Two approvals of one item at once; one APPROVED, one record, the second refused with 409 and MSG-GEN-004 |
| TC-E2-029-09 | AC9, BR11 | Component | The decision-record library fails on a rejection; no record, no outbox row and no feedback row |
| TC-E2-029-10 | AC10, BR2 | Contract | X4 recall 0.6000 against the condition 0.75; 422 MSG-P10-001 naming the code, the value and the threshold |
| TC-E2-029-12 | AC7, BR11 | NFR | The record write forced to fail on a rejection; nothing stored, the chain at its last entry and MSG-P7-003 |
| TC-E2-029-13 | AC4 | Component | Not specified in the source documents (DOR-RWB-P7-E2029-APP-12) |
| TC-E2-029-14 | §12.7 tables (ASM-3438) | Component | Boundary values of the tables of section 12.7; Not specified in the source documents (DOR-RWB-P7-E2029-APP-12) |
| TC-E2-029-15 | AC4, BR5 | Component | Item of "SCREENING" "P2" for MORTGAGE and BKK is WAITING and prepared by RW-COE; the preparer approves and is refused with MSG-P7-002; a user below the delegation level approves and is held with MSG-P7-001 and no record |
| TC-E2-029-16 | AC10, BR9 | Contract | Rejection of X6 on case `RW-2027-000801` with appraisal date 2027-01-25 on the rwb-source-data fake; the inputs reference names that date |
| TC-E2-029-17 | AC11, BR10 | Component | Second record appended after the first for case `RW-2027-000801`; the chain link holds and the update and delete attempts leave the first record unchanged |
| TC-E2-029-18 | AC12, BR14 | Component | Rejection of X6 on case `RW-2027-000801`; the record, event, trail and logs carry no personal data |
| TC-E2-029-19 | AC13, BR15 | Component | Rejection of X6 on case `RW-2027-000801`; no case status, task, timer or deviation is set or changed |
| TC-E2-029-20 | AC14, BR5, BR9, BR10, BR14, BR15 | Component | Rejection of X6 on case `RW-2027-000801`; the approval of "SCREENING" "P2" read with its record, inputs reference, event and trail |
| TC-E2-029-21 | AC15 | Component | Each provided operation called with no valid credential; 401 on each and nothing written |
| TC-E2-029-22 | AC16 | Component | Rejection of X6 on case `RW-2027-000801` recorded, then the same write sent again with the same idempotency key; answer Not specified in the source documents (NEWAC-RWB-P7-E2029-APP-AC13) and nothing new written |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The legacy level System maps to Component or Contract as the row shows, Access to Component and Resilience to NFR. The whole legacy set is kept because this slice carries the record of every promotion and every rejection of the key; the tests whose reading lives in `rwb-agent`, `rwb-deviation`, `rwb-case` or `rwb-access` assert this story's record through the contract fake for the rest. The `-ITG` copies of the same cases belong to the integration story of this key and are not written here.

Volume: this module states no deviation, screening or queue volume. No source gives the deviations open at go-live, the screening runs per night, the deviation queue size or the rule evaluations per screening. The platform figures are the only ones available: 23,600 open cases at go-live and 3,110 new a month (NFR-001), about 370 staff online of 914 (NFR-002) and 300 milliseconds per rule evaluation (NFR-011). The agent evaluation samples are 200 and 500 cases. The real deviation rate is measured in the shadow run before the wave 2 volume test is sized (GAP-1833).

### 17. Guardrails

- No business value in code: the condition set, the confidence floor, the segment pair, the codes, the statuses, the approval level and the message texts are parameter, reference-data or message-standard rows; nothing of them is a constant here.
- No personal data in the record, the event payload, the trail, the tests or the prompts: case and run identifiers, codes, versions, scores, a condition set, a reason, user references and dates only.
- No read of another service's tables (DP-01): the evaluation and the run arrive on the P10 contract, the case, the parameters and the lists on the P3 contracts, and the right on the authorise answer; no `agent_*`, `recovery_case`, `deviation` or `delegation_limit` row is copied into `rwb_decision`.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads one appraisal date on the `rwb-source-data` contract or its own `v_ace_valuation` view and no ACE table (DP-05).
- One recorder and no mover: this story raises no deviation, pauses no clock, changes no case status and stores no feedback, so a record can never move a case.
- No record without its event and no event without its record: the record, the chain link, the approval status and the outbox row commit in one transaction, and a failure changes nothing and leaves the writer's feedback unwritten (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist on a record, the sequence number is never reused, and a wrong record is corrected by a new record naming the one it corrects.
- A person decides a promotion: the agent may propose, and no path lets the agent, a job or a retry approve a promotion, move an item to APPROVED or write a rejection on its own behalf.
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` and `rwb-decision` in namespace `rwb-recovery`, with the shared topic `rwb.decision-record.v1` for the record event.
- One hop and 2 s on every call, with a breaker per downstream; a missing answer never produces a record from a guessed version, code or score.
- The record path is never gated by a feature flag and never skipped for speed: an approval or a rejection without its record is a defect, not a degraded mode.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-AGT-08, FEAT-DVH-07 | 11 Handle customer care and deviations | R-UNI-39 | TC-E2-029-01, TC-E2-029-02, TC-E2-029-04, TC-E2-029-05, TC-E2-029-06, TC-E2-029-09, TC-E2-029-10, TC-E2-029-12 |
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue | Business Requirements Program, section 5.15 | FEAT-DVH-07 | 11 Handle customer care and deviations | R-DEV-01 | TC-E2-029-02, TC-E2-029-08, TC-E2-029-11 |

| Legacy reference | Where it is kept |
|---|---|
| The evaluation of "SCREEN-S2" version 1, 500 cases, per-code precision and recall, X1 at 0.9111 and 0.8913 | Sections 3, 4, 7 (AC1, AC2), 8 (BR2, BR4) |
| The L1 promotion on segment MORTGAGE and BKK, its conditions and its effective date | Sections 1, 2, 4, 7 (AC1, AC3), 8 (BR1, BR3, BR4), 13 |
| MSG-P7-005 and the reason on a rejection | Sections 5 (X5), 7 (AC6), 8 (BR6), 14 |
| MSG-P7-003, R-UNI-39 and the block when the record cannot be written | Sections 5 (X4), 7 (AC7), 8 (BR11), 14 |
| MSG-GEN-004 and one record per item | Sections 5 (X8), 7 (AC8), 8 (BR12), 14 |
| MSG-P4-002, MSG-S8-001, RW-CASEOWN and RW-RISK | Sections 5 (X6), 7 (AC9), 10, 14 |
| The condition set, the confidence floor 0.80 and MSG-P10-001 | Sections 5 (X1), 7 (AC2), 8 (BR2, BR4), 14 |
| The legacy cases RW-2027-000801 and RW-2027-000802, policy SCREENING P2 with prompt PR2, agent version SCREENING@P2/PR2 | Background and scenarios of section 7; section 3 |
| Legacy key RWB-E2-029, story RWB-P7-E2029-APP, contract RWB-P10-E2029-CON | Metadata, sections 3 and 12 |
| Test cases TC-E2-029-01 to TC-E2-029-12 | Section 16 |
| Decoupling patterns DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 | Metadata, section 13 |

The other slices of the key answer the rest: RWB-P10-E2029-APP and RWB-P10-E2029-CON the policy, the prompt, the run, the stored proposals, the mode, the confidence marker, the panel, the feedback row and the evaluation sample; the S8 story of RWB-E2-015 the deviation raise and the pause of R-DEV-01; RWB-P3-E1035-APP the case record and the case status; the integration story of this key the cross-service harness and the `-ITG` copies of the test cases.

### 19. Out of scope

- The agent policy, the prompt and its version, the agent run, the stored proposals and their sources, the guardrails, the masked model call, the autonomy mode and its change, the panel "Proposed deviations" and its states, the feedback row and the evaluation sample and its scoring: RWB-P10-E2029-APP, with the contract, the event schemas and the fakes in RWB-P10-E2029-CON.
- The raise of a deviation, `raised_by` "SCREENING_AGENT", R-DEV-01, the stage clock, the case status "On hold" and the deviation queue: `rwb-deviation` (S8) and the story of RWB-E2-015.
- The case record, the case status, the case scope and the stale warning on the panel: `rwb-case` (P3); the scope answer and the masking are `rwb-access`'s (P4).
- The decision-log store of this service — the append-only trigger, the grants, the chain verifier and the daily chain check JOB-14 — and the approval routing with its `ApprovalWorkflow` and its screens: other slices of `rwb-decision`.
- The rule package registry, the Drools packages, the dry run, the rule authoring and the rollback: the rule-authoring slice of this service.
- The acceptance and correction measure by segment and its extract: JOB-15 of `rwb-reporting` and the measure of RWB-P10-E2029-APP.
- The lake copy of the ledger: removed with the data lake (DP-17).
- The integration harness and the `-ITG` copies of the test cases: the integration story of this key.
- The ACE DB story, the infrastructure story and the deployment story of this legacy key: their own DB, INF and OPS stories; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability are the OPS story's.

The names of the level holders and substitutes and the parameter values of the delegation of authority are data of their owners, and no date is changed by this story: the release 31 January 2027 is copied unchanged and stays tentative.
