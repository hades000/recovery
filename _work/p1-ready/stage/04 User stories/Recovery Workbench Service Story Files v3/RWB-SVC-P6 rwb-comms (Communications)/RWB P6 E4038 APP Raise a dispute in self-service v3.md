# RWB-P6-E4038-APP Raise a dispute in self-service

**Version 3 changes.**

- Aligned the dispute customer read and fake to getCustomer (RD-P1-060).

**Version and date.** v3, 27 November 2026.

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4038-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-038 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P6-E4038-APP-16); the squad sizes it at refinement |
| Contract version | /v1 path only; the version is Not specified in the source documents (DOR-RWB-P6-E4038-APP-23) |
| Fake library version | Not specified in the source documents (DOR-RWB-P6-E4038-APP-22) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-V |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4038-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | rwb-source-data.yaml 5.1.0 getCustomer (RWB-P1-E1069-APP) |
| Readiness decisions | RD-P1-060 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-038 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E4038-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026. Aligned the dispute customer read and fake to getCustomer (RD-P1-060).

### 1. Story

As a **customer (borrower) on LINE OA or HOME.SCB**, I want **to raise a dispute against the notice that was sent to me, so that rwb-comms records the dispute against that notice, writes the decision record before the change takes effect, asks the deviation owner to raise X1 and puts the contact stop on the outbound contact of the notice while the deviation is open**, so that **no further notice or message leaves on a disputed case until the deviation owner clears it, and every step of the way carries a dated decision record**.

The legacy story names the customer (borrower) as the actor and the FSD P6 repeats it as the primary actor of FEAT-COM-04, with the Complaint officer as the also-user (FSD P6 A2.17.3.3). The rights matrix of TSD P6 T6.1 has no customer row at all: it lists staff and partner principals, and the internal principal who holds the Documents and Litigation rights of this module is the Complaint officer (RW-COMPLAIN, Documents CRU and Litigation R) (GAP-1114; ASM-2062). This story therefore records the dispute for the customer who raises it on the bank's channel and answers the internal readers who hold the rights of the capability area, and it declares the customer principal once, in the contract baseline.

The X1 deviation, its code, its owner, its clock and the pause of the case are not this service's facts: R-UNI-04 gives them to the deviation owner and to the case, the deviation table is S8's and the case and its timers are P3's (Ownership Map). This story asks the deviation owner to raise X1, records the reference it answers, and applies the contact stop to its own notices; it builds no deviation row and no case row.

### 2. Business rationale

A dispute raised today reaches the bank by phone or at a branch, is written on a form and re-keyed, and the contact stop is applied by asking an owner to hold the letters (FSD P6 A2.17.1). Nothing on the letter path knows that a dispute is open, so a demand can go out while the complaint is being read. FEAT-COM-04 puts the action on the customer's own channel and makes the stop a fact of the case rather than a promise in a conversation (FSD P6 A2.17; Epics 3 to 8 Specification v3, feature row FEAT-COM-04, epic E4, module P6). The FSD measures the feature with "notices with proof of delivery, 100 percent", measured from the decision log and the Workbench records and reviewed monthly (FSD P6 A2.17.1).

In the target the action is not one monolith write. rwb-comms owns the notice, the template, the merge fields and the proof of delivery (Architecture v5 slides 17 and 41); rwb-deviation owns X1 to X7, the pause, the handling and the return (slide 41); rwb-case owns the case, its state and its clocks; rwb-decision owns the central ledger; rwb-source-data owns the ACE customer, contact and consent facts; rwb-access and gateway-bff authorise and compose the customer channel (Architecture v5 slides 13, 17 and 20). Architecture v5 slide 17 fixes exactly what this service takes in and sends out: in, the events `DeviationRaised` and `DeviationCleared` "for the contact stop", with `TreatmentApproved`, `PaymentMissed` and `CaseStateChanged`; out, the schema `rwb_comms` with notices, templates, merge fields and proof of delivery, and the topic `rwb.comms.events.v1` with `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`.

This story is the rwb-comms slice of legacy RWB-E4-038. It owns both legacy criteria, AC1 (the dispute is raised, X1 opens, the contact stop applies and the result is written to the decision log with the rule version) and AC2 (a decision record that cannot be written changes nothing and shows MSG-P7-003), because both are satisfied inside this service once the deviation is taken from the owner's contract and the customer facts from the data contract. The rest of the legacy story body belongs to other features and is carried as one conflict rather than copied: the screen is SCR-33 Template approval, the permission table names Litigation C and Litigation R, and the endpoint block names the two notice administration operations `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` (GAP-1115; ASM-2063).

The decoupling is the one the target fixes. The dispute is a row of this service and no deviation row, no case row and no ACE table is declared here (DP-01 in force as a prohibition); the customer, contact and consent facts are read on rwb-source-data's contract and never on a `v_ace_*` view of this service (DP-05); the decision record goes through the local library and the shared topic before the change (DP-03); the base is `/api/recovery/comms/v1` (DP-13); and the customer channel and the internal notice screens reach the answer through the gateway-bff composite route (DP-19).

Four points are gaps and assumptions rather than quiet decisions. No source names a dispute operation, a request, an answer or a table of rwb-comms, and the FSD field catalogue of the feature lists notice fields only, so the two operations, the shapes and the new `notice_dispute` table are fixed by RWB-P6-E4038-CON with their field detail marked (GAP-1112; ASM-2060). No source publishes an operation of rwb-deviation that opens X1 for a customer dispute, and TSD P6 T5.2 does not list S8 among the modules this module calls, so the call is consumed and faked and adds no contract dependency (GAP-1113; ASM-2061). The customer principal of a self-service action is missing from the rights matrix (GAP-1114; ASM-2062). And the dispute reason codes, the decision code, the rule id and the refusal texts are given by no source (GAP-1117; ASM-2065). The requirement the feature serves is REQ-OCC-011 ("customer self-service for an offer, a signature, a payment and a dispute is available on the bank's digital channels"), which the traceability table of TSD P6 T8 maps to FEAT-COM-01 instead of FEAT-COM-04 (GAP-1115; ASM-2063).

### 3. Preconditions

- RWB-P6-E4038-CON is published: the two dispute operations under `/api/recovery/comms/v1`, the `DisputeRequest` and `Dispute` schemas, the new `notice_dispute` row of `rwb_comms`, the `hold_reason` carrier of the contact stop, the `Idempotency-Key` rule, the error set, the decision-record element, the two consumed deviation events, the two fakes and the empty rows, so this story builds against a fixed contract on Day 1.
- The `notice` row exists in `rwb_comms` with `case_id` (DF-LEG-016), `party_id` (DF-LEG-030), `notice_type` (DF-LEG-018), `delivery_status` (DF-LEG-022) and `hold_reason` (DF-LEG-032): the baseline is the one RWB-P6-E1052-APP and RWB-P6-E2021-APP create, and the dispute is recorded against a notice that was sent (TSD P6 T3.1).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract (DP-03), so the decision record is written before the change and relayed by the platform outbox relay.
- The deviation owner answers the X1 raise and the state read of its own contract, and its answers are available as fakes from the first run. The operation is the deviation create of the Ownership Map row `POST /cases/{caseId}/deviations`, owned by S8 rwb-deviation; no S8 contract story is named in this story's Contract dependencies, so the row is declared as consumed and faked and no contract dependency is added (GAP-1113; ASM-2061).
- The customer, contact and consent facts arrive on rwb-source-data's contract (DP-05): the party of the notice, the contact points the stop applies to and the consent state of the channel. This service reads no `v_ace_*` view and holds no grant on `rwb_source_data` or on the ACE views (Architecture v5 slides 13 and 20).
- The deviation table, the case and its clocks are other owners': `deviation` is S8's in `rwb_deviation` and `recovery_case`, `task`, `timer`, `queue` and `assignment` are P3's in `rwb_case` (Ownership Map; Architecture v5 slide 41). No deviation row, no case row and no foreign key across the boundary is declared here.
- The screen path is the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), so neither the customer channel nor an internal notice screen calls the service directly.
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are the contract baseline of this key and two platform CON stories, and the C, I and X rows are empty (Template and Rules §R5.7, §R5.4).

### 4. Flow

1. A customer on LINE OA or HOME.SCB raises a dispute on a notice through the gateway-bff composite route, which passes `POST /api/recovery/comms/v1/notices/{noticeId}/disputes` with an Idempotency-Key, the channel and the reason code.
2. The service reads the notice from `rwb_comms` and checks that it belongs to the caller's case scope; a notice outside the scope answers 404 and changes nothing.
3. The service refuses a notice that is not a sent notice of the case with 409 and records nothing, because a dispute is raised against the notice the customer holds.
4. The service resolves the party of the notice and its contact and consent facts on the rwb-source-data contract, one hop with a 2 s budget (DP-05); a party the data contract does not return stops the flow with 404 and changes nothing.
5. The service writes the decision record through the local decision-record library before any change, with the decision code and the rule id and version in force, the case, the notice, the channel and the reason code (DP-03).
6. The decision record written, the service asks the deviation owner to raise X1 on the rwb-deviation contract, one hop with a 2 s budget, naming the case, the notice, the dispute and the channel; the owner raises the deviation, pauses the case clock and answers its deviation reference.
7. The service stores the dispute as a row of `notice_dispute` in `rwb_comms` with the owner's deviation reference, in the same transaction as the decision record and the notice hold of the next step.
8. The service sets `notice.hold_reason` (DF-LEG-032) to the contact stop of the answered deviation, so every dispatch and every message of that notice is held from that moment (R-LIT-05, R-UNI-04).
9. The service answers 201 with the dispute as the contract fixes it, the deviation reference included; the outbox relay publishes `rwb.decision.DecisionRecorded.v1` (EV-08).
10. When the deviation owner later publishes `rwb.deviation.DeviationCleared.v1` (EV-07), the inbox of this service applies the lift: the dispute row records the lift from the event and `notice.hold_reason` is cleared, so the outbound contact of the notice resumes on the permitted channels (R-UNI-44). No operation of this story needs to be called for that.
11. A repeat of the POST with the same Idempotency-Key returns the first answer with status 201 and raises no second deviation. A reader with the Documents right sends `GET /api/recovery/comms/v1/notices/{noticeId}/disputes` and receives 200 with the disputes of the notice, newest first.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The notice is outside the caller's scope or does not exist | Refused with 404; nothing changes | None | AC3 (TC-E4-038-21) |
| X2 | The notice is not a sent notice of the case | Refused with 409; no decision record, no deviation, no hold | Not specified in the source documents (GAP-1117; ASM-2065) | AC1 |
| X3 | A required field is missing, or the channel or the reason code is not in its list | Refused with 422; nothing changes | MSG-GEN-001 | AC1 |
| X4 | The data contract does not return the party of the notice | Refused with 404; no decision record and no deviation | Not specified in the source documents (GAP-1117; ASM-2065) | AC1 |
| X5 | The decision record cannot be written | Nothing changes, no deviation is raised, the answer is 503 and an incident is raised | MSG-P7-003 | AC2 |
| X6 | The deviation owner does not answer, or answers 5xx | The decision record stands, the dispute row is written in the received state with no owner reference, the notice is held and a retry and an alert follow; the answer is 202 and never a 201 with a deviation reference | Not specified in the source documents (GAP-1113; ASM-2061) | AC1 |
| X7 | The deviation event arrives twice | The second event is ignored and the idempotency hit is recorded | None | AC1 |
| X8 | A role without the Documents right | Refused with 403; nothing changes | MSG-P4-002 | AC4 (TC-E4-038-22) |
| X9 | The POST is repeated with the same Idempotency-Key | The first answer is returned with status 201 and no second deviation is raised | None | AC1 |

X2, X4 and X6 are refusals and partial outcomes this service produces itself, and their message texts and the exact status of X2 and X4 are given by no source, so they carry the placeholder of section 14. X6 is the fail-safe of the design rather than a rollback: the decision record is already written and the customer's dispute is kept, the stop is applied on the notice, and the missing deviation is reconciled by a retry that names the same dispute so the owner raises X1 once (R-UNI-04 gives the stop to the deviation; this service does not release a stop it did not raise).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4038-CON, the decision-record library and the edge route. The deviation owner, the customer data contract and the two deviation events are fakes from the first run |
| Negotiable | The reason codes, the channel list, the decision code and the refusal texts are reference data, parameters and the message list; the story fixes the order of the checks and the place of the decision record |
| Valuable | A customer stops contact on the same day the dispute is raised, every held notice carries the reason, and the bank can show a dated, reproducible record of the request and of what it did |
| Estimable | Two endpoints, one new table, one owner adapter for the deviation, one for the customer data, one library write, two consumed events and the projection; four legacy test cases plus the contract tests of the baseline |
| Small | Fits one sprint as the app slice of the legacy key: one table, one projection column and no workflow |
| Testable | Each criterion of section 7 runs as one automated test against the contract fakes; the whole path is proven without a second service being live |

### 7. Acceptance criteria

```gherkin
Feature: Raise a dispute in self-service — the rwb-comms slice

  Background:
    Given notice "N-0101" of case "RC-2026-000321" has been dispatched with delivery status "PENDING"
    Given no contact stop is in force on case "RC-2026-000321"

  Scenario: AC1 Raise a dispute in self-service (legacy RWB-E4-038 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-deviation contract mock returns the deviation "DV-0101" raised for notice "N-0101" with its owner reference
    When the user acts on the screen
    Then lets the customer raise a dispute, which opens X1 and applies the contact stop
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-038 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 A notice outside the caller's scope or not found is refused with 404 (new, D-RCV-60)
    Given the caller is outside the scope of notice "N-0101" or the notice does not exist
    When the customer raises a dispute on notice "N-0101"
    Then the system refuses with 404 and nothing changes

  Scenario: AC4 A role without the Documents right is refused with 403 (new, D-RCV-60)
    Given the caller has a role without the Documents right
    When the caller sends the dispute POST for notice "N-0101"
    Then the system refuses with 403, the user sees MSG-P4-002 and nothing changes

  Scenario: AC5 Each rule of section 8 with no criterion is checked by its test case of section 16 (new, D-RCV-60)
    Given the rule of section 8 is in force
    When its test case of section 16 runs
    Then the rule holds

  Scenario: AC6 A caller without valid credentials is refused with 401, and the 403 and 404 answers stay as AC3 and AC4 (new, D-RCV-60)
    Given the caller presents no valid credentials
    When the caller sends the dispute POST for notice "N-0101"
    Then the system refuses with 401 and nothing changes

  Scenario: AC7 A replay of a write with the same Idempotency-Key returns the first answer (new, D-RCV-60)
    Given the dispute POST for notice "N-0101" was accepted with an Idempotency-Key
    When the same POST is repeated with the same Idempotency-Key
    Then the first answer is returned with status 201 and no second deviation is raised

  Scenario: AC8 A failed or unanswered call to the deviation owner records no fully raised dispute (new, D-RCV-60)
    Given the rwb-deviation contract mock fails or does not answer for notice "N-0101"
    When the customer raises a dispute on notice "N-0101"
    Then the dispute is written in the received state with no deviation reference, the notice is held and the answer is Not specified in the source documents (NEWAC-RWB-P6-E4038-APP-AC8)

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a dispute in the state "received"
    When a status change the state model does not allow is requested
    Then the system refuses it and nothing changes
```

AC1 and AC2 are the two criteria of RWB-E4-038 copied line for line, with the origin tag on each scenario line and one `Given the rwb-deviation contract mock returns …` line added inside AC1 for the part of the criterion that names a fact of another owner: X1 and its reference are rwb-deviation's, so the criterion can only run against that owner's contract fake. Every legacy line and every legacy value is kept and no business value is added. The two criteria run against the fakes of 12.8 and answer on the contract of 12.1.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A dispute raises X1 through the deviation owner's contract and never by writing a deviation row of this service; the deviation, its code, its owner and the pause of the case are S8's and P3's facts (DP-01, DP-11) | R-UNI-04; Architecture v5 slide 41; Ownership Map (`deviation` owned by S8, `recovery_case` by P3) |
| BR2 | The contact stop applies to the outbound contact of the notice: while the deviation is open, `notice.hold_reason` is set and every dispatch and message of that notice is held | Architecture v5 slide 17 ("events DeviationRaised / Cleared (contact stop)"); TSD P6 T3.1 (DF-LEG-032); R-LIT-05 |
| BR3 | The decision record is written before the change, through the local decision-record library and the shared topic; a dispute whose record cannot be written does not proceed | R-UNI-39; DP-03; legacy AC2 |
| BR4 | The stop is lifted on `DeviationCleared` and the outbound contact resumes on the permitted channels only; this service lifts a stop only when the deviation owner clears it | R-UNI-44; Architecture v5 slide 17 |
| BR5 | A dispute is recorded against a notice of the case that was sent to the customer; a notice that is not a sent notice of the case carries no dispute | FSD P6 A2.17.1 and A2.17.2; TSD P6 T3.1 (DF-LEG-019, DF-LEG-022) |
| BR6 | The customer, contact and consent facts are read on rwb-source-data's contract, one hop with a 2 s budget; this service reads no `v_ace_*` view and no table of another schema (DP-05) | Architecture v5 slides 13 and 20; DP-05; TSD P5 T3.1 not applied here |
| BR7 | No value a business person may change is written in code: the reason codes, the channel list, the decision code, the rule id and the rule version are data or reference data read with the version in force | FSD P6 A2.17.3.1 (BR-P6-017); Template and Rules §R7.2 s17 |
| BR8 | A contact attempted while a stop is in force is refused with MSG-P6-001, and a contact on a channel without consent with MSG-P6-002; the contact and dispatch path raises them, this story only supplies the stop and the consent state it reads | FSD P6 A2.17.3.1 (VR-P6-017-1, VR-P6-017-2) |
| BR9 | A legal hold on the case stops every outbound action; a dispute never lifts it and the stop it applies is additional to it | R-UNI-20 |
| BR10 | A repeated POST with the same Idempotency-Key returns the first answer and raises no second deviation | Architecture v5 slide 11; DP-09 |
| BR11 | A deviation event that arrives twice is ignored and the idempotency hit is recorded | R-UNI-40; DP-09 |
| BR12 | One base and one topic: `/api/recovery/comms/v1` and `rwb.comms.events.v1`; this story declares no other service's path or topic as its own, and the shared decision topic is the library's | DP-13; DP-14; Template and Rules §R4 |
| BR13 | Raising a dispute raises no event of this service: the catalogue has none for a dispute, and the only event of the check is `DecisionRecorded` on the shared `rwb.decision-record.v1`; the stop and its lift are rwb-deviation's events | Architecture v5 slide 42 (events 06, 07 and 08); DP-03 |
| BR14 | A missing answer of an owner never records a dispute as fully raised and never answers with a deviation reference it does not hold (fail closed on the reference, fail safe on the dispute) | ADR-020; DP-11; ASM-2061 |

### 9. State transitions

A dispute changes no notice delivery state of its own. It sets and clears the contact stop on the notice, and its own row follows the deviation owner's events:

| From | Event | Condition | To |
|---|---|---|---|
| No dispute on the notice | A dispute is accepted | The notice is a sent notice of the case, the party is resolved and the decision record is written | A `notice_dispute` row exists with the owner's deviation reference and `notice.hold_reason` is set |
| A dispute with the stop in force | `DeviationRaised` arrives for the same case and notice | The inbox has not seen the event key | The row records the raised deviation and the stop stays in force |
| A dispute with the stop in force | `DeviationCleared` arrives | The event names the deviation of the row | The row records the lift and `notice.hold_reason` is cleared, so the outbound contact resumes (R-UNI-44) |
| A dispute with the stop in force | The deviation owner does not answer the raise | The call times out or answers 5xx | The row stands in the received state with no owner reference, the notice is held, a retry and an alert follow (X6) |
| No dispute on the notice | A dispute is refused on scope, notice state, field or party | The check of section 4 fails | No dispute, no decision record, no deviation, no change |
| No dispute on the notice | The decision record cannot be written | The library fails | No dispute, no deviation, no hold, MSG-P7-003, incident under R-UNI-39 |

The state vocabulary of a `notice_dispute` row is Not specified in the source documents (GAP-1112; ASM-2060): the FSD field catalogue of the feature lists notice fields only and no source names a dispute state list. RWB-P6-E4038-CON fixes the values once, as reference data, and this story reads them with the version in force. The notice delivery states (`DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING`, LOV-DELIVERY of TSD P6 T3.2) are never changed by a dispute, and `hold_reason` (DF-LEG-032) is the only notice column this story writes.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Customer (borrower), on LINE OA or HOME.SCB | The primary actor of FEAT-COM-04 in FSD P6 A2.17.3.3: raises the dispute on the notice of their own case. The rights matrix has no customer row, so the principal, its token and the case scope it carries are the edge's and the gap of section 18 (GAP-1114; ASM-2062) |
| RW-COMPLAIN, complaint officer | Documents CRU in TSD P6 T6.1: records a dispute of a case of the complaint queue and reads the disputes of its notices (rights C and R) |
| RW-FRAUD, fraud investigator | Documents CRU in TSD P6 T6.1: records and reads a dispute of a case under a fraud flag (rights C and R) |
| RW-CASEOWN, case owner | Documents CRU in TSD P6 T6.1: records a dispute taken by phone and reads the disputes of the cases owned |
| RW-TEAMMGR, team manager | Documents R in TSD P6 T6.1: reads the disputes of the team's notices |
| RW-LITOFF, litigation officer | Documents CRU in TSD P6 T6.1: records a dispute on a notice under litigation and reads it |
| RW-ENFORCE, enforcement owner | Documents CRU in TSD P6 T6.1: records a dispute raised at enforcement and reads it |
| RW-LEGAL, legal counsel | Documents CRUA in TSD P6 T6.1: reads the disputes of the notices of a legal file (rights R and A on the notice resource) |
| RW-CONDUCT, conduct and QA officer | Documents R in TSD P6 T6.1: reads the disputes and the stops they raised, and is the role the routing logic gives the notice hold (R-LIT-05) and the lift (R-UNI-44) |
| RW-COMPLY, compliance and PDPA officer | Documents RU in TSD P6 T6.1: records a dispute received as a PDPA or compliance request and reads the disputes |
| RW-AUDIT, internal audit | Documents R in TSD P6 T6.1: reads the disputes and their decision records |
| RW-PLATADM, platform administrator | Documents R in TSD P6 T6.1: reads the disputes and operates the feature switch; no administrative write of a dispute |
| rwb-comms service identity | Reads its own `notice` row, writes the `notice_dispute` row and the hold, writes the outbox row, and calls the deviation owner, the data contract and the decision-record library (DP-02) |
| Decision-record library identity | Writes the local decision record of the dispute and relays it on `rwb.decision-record.v1` (DP-03) |
| rwb-deviation service identity | Raises X1 for the dispute, owns its clock and the pause of the case, and publishes `DeviationRaised` and `DeviationCleared` |

The letters above are the Documents column of TSD P6 T6.1 and nothing else. The right of the two dispute operations is declared in RWB-P6-E4038-CON as Documents C and R with the scope applied; the authorise contract of rwb-access is not in this story's pattern set, because the right is declared on the operation and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (`rwb_comms`, P6) | id | Read |
| DF-LEG-016 | notice (`rwb_comms`, P6) | case_id | Read |
| DF-LEG-018 | notice (`rwb_comms`, P6) | notice_type | Read |
| DF-LEG-019 | notice (`rwb_comms`, P6) | sent_date | Read |
| DF-LEG-022 | notice (`rwb_comms`, P6) | delivery_status | Read |
| DF-LEG-030 | notice (`rwb_comms`, P6) | party_id | Read |
| DF-LEG-032 | notice (`rwb_comms`, P6) | hold_reason: the contact stop of the answered deviation | Write on the raise, cleared on the lift |
| Standard column | notice (`rwb_comms`, P6) | state, version, updated_at, updated_by | Write on the hold and the lift |
| Not specified in the source documents (GAP-1112; ASM-2060) | notice_dispute (`rwb_comms`, P6, new table) | dispute id, notice id, case id, channel, reason code, raised at, state, the owner's deviation reference | Write on the raise; read on the list; the state and the lift written from the deviation events |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer, on the rwb-source-data contract | person_key, cif_no, customer_status and the contact and consent facts of the party | Read through the contract, never a table and never a view of this service |
| DF-CAS-036 to DF-CAS-045 | deviation, on the rwb-deviation contract | id, case_id, deviation_code, raised_at, raised_by, paused_state and 4 more | Write through the contract (the X1 raise) and read its reference, never a table |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, rule version, case, notice, dispute, channel, reason code, decided at, hash chain | Write |
| DF-REF-001 to DF-REF-015 | rule_row, through the rwb-decision contract | rule_id, rule_version | Read through the contract, never a table |
| DF-REF-045 to DF-REF-051 | template (`rwb_comms`, P6) | id, template_code, template_version, language | Read, for the notice reference only |
| Standard column | outbox_event, processed_event, idempotency_key (library objects in `rwb_comms`) | the outbox row of the decision record and of the dispute, the inbox dedupe of the two deviation events, the POST key | Write |

The customer, the contact points, the consent state and the identity of the borrower are rwb-source-data's facts, and the deviation is rwb-deviation's: `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` are P1's in `rwb_source_data` (Ownership Map; Architecture v5 slide 41) and `deviation` is S8's in `rwb_deviation`. This service reads none of them as a table, holds no grant on either schema and declares no foreign key across the boundary. The field names, the types and the required flags of the `notice_dispute` row and of the dispute element are Not specified in the source documents (GAP-1112; ASM-2060); RWB-P6-E4038-CON fixes them once and the owner's definition of the deviation table stays the owner's.

The migration of this story is one per-service Flyway step in `rwb_comms` (DP-15; RWB-PLT-E1044-CON is not in this story's build list, so the step follows the baseline sequence of RWB-P6-E1052-APP): `V<nnnn>__notice_dispute.sql` creates `notice_dispute`, its standard columns of TSD P6 T3.0, `state` and `version` included, and the index on `(notice_id, case_id)`. `notice.hold_reason` (DF-LEG-032) already exists in the baseline of TSD P6 T3.1 and is not created here. No column of this service carries a name, an address, an identity number, an account number or a contact point; the channel is a code of LOV-CHANNEL and the reason code is a reference-data code. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E4038-CON; this story implements them and adds no path. Neither operation is in the endpoint inventory of TSD P6 T-A.1, which holds API-P6-001 to API-P6-011 and none for a dispute (GAP-1112; ASM-2060).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/notices/{noticeId}/disputes` | Record one dispute against a notice and return it, 201 with the Dispute, or 202 when the deviation owner has not answered | Documents, right C, scope applied | Idempotency-Key header, kept 24 hours |
| GET | `/notices/{noticeId}/disputes` | List the disputes of a notice, newest first, 200 with the Dispute list | Documents, right R, scope applied | Not applicable |

Errors: 401 no session (message ID Not specified in the source documents (DOR-RWB-P6-E4038-APP-8)); 403 the role lacks the Documents right (MSG-P4-002); 404 the notice is absent or out of scope, or the data contract does not return the party (message ID Not specified in the source documents (DOR-RWB-P6-E4038-APP-8)); 409 the notice is not a sent notice of the case, or a dispute is already open against it (message ID Not specified in the source documents (DOR-RWB-P6-E4038-APP-8)); 422 a field fails validation (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003). The Dispute body of the answer carries `id`, `noticeId`, `caseId`, `channel`, `reasonCode`, `raisedAt`, `state` and the owner's deviation reference, whose element names and physical types are fixed by the contract baseline with the placeholder where no source names them (GAP-1112; ASM-2060).

Request: `DisputeRequest` with `channel` required and taken from LOV-CHANNEL, `reasonCode` required and taken from the reason-code list in force, and no field that carries a name, an address, an identity number or free text of a person. The Dispute body and the Request hold no field that Data Classification and Personal Data Inventory v5 classes as personal data. The personal data that the service reads or writes inside rwb_comms is notice.person_key (DF-LEG-030) and notice.hold_reason (DF-LEG-032), the second written in step 8 of section 4; neither is returned in the answer.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | the deviation create of the rwb-deviation contract (Ownership Map row `POST /cases/{caseId}/deviations`) | S8 rwb-deviation | Raises X1 for the case and the notice and answers the deviation with its identifier and state; faked. No S8 contract story is named in this story's Contract dependencies (GAP-1113; ASM-2061) |
| GET | the customer read of the rwb-source-data contract (Ownership Map row `GET /customers/{personKey}`) | P1 rwb-source-data | Resolves the party of the notice, its contact points and the consent state of the channel the stop applies to; faked from rwb-source-data.yaml 5.1.0 (RD-P1-060) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). No row reads a table, no row reads a `v_ace_*` view of this service, and no row is declared as provided by this service (DP-01; Ownership Map).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision record reference, decision code, rule id, rule version, case id, notice id, dispute id, the deviation reference, channel, reason code, decided at |

The row is written to the outbox in the same transaction as the `notice_dispute` row and the notice hold and relayed with the CloudEvents 1.0 envelope by the platform outbox relay (DP-03, DP-09). The local decision-record library of this service publishes it and this story declares no event of its own: the catalogue of Architecture v5 slide 42 has no dispute event, and the three events of this service (EV-13 `NoticeGenerated`, EV-14 `NoticeDispatched`, EV-15 `NoticeDelivered`) belong to the generation and dispatch stories.

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | Takes the stop that the deviation owner raised: the `notice_dispute` row of the case and notice records the deviation and `notice.hold_reason` is set, so the outbound contact of the notice is held; deduped through the inbox. The shape of the local projection that answers it is Not specified in the source documents (GAP-1116; ASM-2064) |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | Applies the lift: the row records that the deviation was cleared and `notice.hold_reason` is cleared, so the outbound contact of the notice resumes on the permitted channels (R-UNI-44); deduped through the inbox; same gap |

Architecture v5 slide 17 gives these two events to this service with the words "contact stop", and R-LIT-05 and R-UNI-44 are the routing rules behind them. They are not a decision input on their own: the dispute is recorded from the call of section 4 and the events only keep the local picture of the stop current between calls. Each carries IDs, codes and dates only and no personal data. `TreatmentApproved` (EV-10) and `PaymentMissed` (EV-12) are the other rows of slide 17 and belong to the payment and treatment stories of this service; neither is used here.

#### 12.5 Workflows and activities

None. The dispute is one synchronous operation of the request thread with one library write and two adapter calls; there is no workflow, no activity and no durable timer. The pause of the case clock and the deviation's own handling run in rwb-deviation's `DeviationWorkflow` on its own task queue (Architecture v5 slide 28), which this story calls through the contract and never starts.

#### 12.6 Schedules

None. No job of the catalogue is created, changed or read: JOB-10 (WIN notices, 16:00, rwb-comms with rwb-integration) belongs to the dispatch story and the file window of the bank's scheduler (Architecture v5 slide 44), and JOB-11 (outbox relay) is the platform's.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice of the dispute, its case, its party, its delivery state and `hold_reason` (DF-LEG-032), which carries the contact stop; written here for the hold and the lift |
| notice_dispute | P6 (rwb_comms, new) | The dispute row of section 11: written on the raise, read on the list, updated from the two deviation events |
| template | P6 (rwb_comms) | Read for the notice reference; written by the template stories |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of a recorded dispute (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox row of the decision record, the inbox dedupe of the two deviation events and the POST key |

Not owned and never read: `deviation` and the deviation handling rows (S8 rwb-deviation, in `rwb_deviation`); `recovery_case`, `task`, `timer`, `queue`, `assignment` and `case_account` (P3 rwb-case); `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` (P1 rwb-source-data); `decision_log_entry`, `rule_row` and the rule package tables (P7 rwb-decision); `outbound_item` and `interface_config` (P2 rwb-integration); `document`, `document_custody` and the retention rows (P5 rwb-document). No deviation table and no case table is declared in `rwb_comms` (DP-01), and no query of this service names a `v_ace_*` view (DP-05).

#### 12.8 Contract fakes

The rwb-source-data fake uses the 5.1.0 getCustomer shape for the notice personKey, with masked personal fields and available contact metadata. This story has no unmasking grant (RD-P1-060).

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-deviation fake | The deviation create and the deviation read of the S8 contract | Deviation `DV-0101` raised for case `RC-2026-000321` with its owner, its state and the pause; a duplicate raise answering the first deviation; a delayed answer beyond 2 s; a raise failing with 5xx; a deviation already cleared |
| rwb-source-data fake | The customer read of the P1 contract | Party `P-0101` of case `RC-2026-000321` with its contact points and the consent state of channel `LINE`; a party the owner does not return; a channel without consent; a delayed answer beyond 2 s |
| deviation-event fake | The two consumed rows of 12.4 | `DeviationRaised` and `DeviationCleared` for the case and notice; a duplicated event for the inbox; a cleared event for a deviation the row does not hold |
| decision-record library stub | The local library and the shared topic | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-038-04 |
| Dispute fake and drift test | The two operations of 12.1 against the published document | The 201, the 202 of X6, the 200 list, the repeated Idempotency-Key and every refusal of 12.1; a drifted fake fails the build |

The fakes are derived from the published contracts of RWB-P6-E4038-CON, and the drift test of that story fails a build in which a fake and the document disagree. The deviation fake and the deviation-event fake carry the placeholder of the S8 side until the S8 contract names the operation and the element (GAP-1113; ASM-2061).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The dispute record and the dispute list provided; the deviation create and the customer read consumed; one hop, 2 s each |
| Kafka | 1 declared as published by the library, 2 consumed | `DecisionRecorded` through the library on the shared topic; `DeviationRaised` and `DeviationCleared` consumed with the inbox dedupe; no dispute event either way |
| Temporal | None | The operation is synchronous; the deviation's own workflow is S8's and is not started here |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `dispute`, Java package `th.co.scb.ace.workbench.recovery.comms.dispute`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | the monolith base `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is in this key's list because the legacy data table reads `v_ace_customer` (DF-ACE-055 to DF-ACE-074) for the party of the notice: in the target that read is rwb-source-data's contract and adds no dependency row, and this service names no `v_ace_*` view. DP-01 is in force as a prohibition and is not a pattern of this key: the legacy data table names `deviation` and `decision_log_entry` as rows of the module, and the target gives the first to S8 rwb-deviation and the second to the shared library of P7, so no such table is declared here (GAP-1113; ASM-2061).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DisputeController | Controller | The two operations with validation, the Idempotency-Key and the problem mapping for 401, 403, 404, 409, 422, 202 and 503 |
| DisputeIntakeService | Service | Reads the notice, applies the sent-notice check, orders the decision record before the change, asks the deviation owner, writes the row and the hold, answers |
| DeviationClient | Adapter | The deviation create and the deviation read of the S8 contract, one hop, 2 s, with a breaker |
| SourceDataClient | Adapter | The customer read of the P1 contract (DP-05), one hop, 2 s, with a breaker |
| DecisionRecordClient | Adapter | The local decision-record write before the change and its outbox row, through the library |
| ContactStopProjection | Service | Sets and clears `notice.hold_reason` from the raise and the two deviation events, and answers the dispatch path with the stop |
| DeviationEventConsumer | Consumer | The inbox of `DeviationRaised` and `DeviationCleared`, with the dedupe of R-UNI-40 |

**Database and migrations**

- Reads and writes `notice`, `notice_dispute` and the local decision record, all in schema `rwb_comms` (DP-01); reads no other schema.
- Migration in this story: `V<nnnn>__notice_dispute.sql` creates the new table of section 11 and the index `(notice_id, case_id)`. No deviation table, no deviation column and no foreign key to another service's schema is created.
- `notice.hold_reason` (DF-LEG-032) exists in the baseline and is written, not created.

**Configuration and reference data**

- `rwb.comms.dispute.reason-codes`: the reason-code list, read as reference data with the version in force; its value is set at the baseline review and never in code.
- The channel list is LOV-CHANNEL of TSD P6 T3.2; the notice types are LOV-NOTICE; the delivery states are LOV-DELIVERY.
- The decision code and the rule id of a dispute, and the refusal texts of X2 and X4, are the reference data and the message list of section 14 and are not written here.
- The 2 s budget and one retry of the GET are the platform settings of ADR-020.
- The feature switch `rwb.comms.self-service-dispute`, read as a parameter: off refuses both operations with 404 and records nothing.
- Reference data (the reason-code list, LOV-CHANNEL, LOV-NOTICE and LOV-DELIVERY) is read through the reference-data contract of DP-06 and DP-07, whose name is Not specified in the source documents (DOR-RWB-P6-E4038-APP-20).

**Build steps**

1. DisputeController and DisputeIntakeService over the two operations, the Idempotency-Key and the problem mapping; tests for the repeat and the two scope refusals.
2. The sent-notice check and the field validation of X2 and X3; tests for both.
3. SourceDataClient with the party, contact and consent read behind the fake (DP-05); tests for X4 and for the channel without consent.
4. DecisionRecordClient and the fail-closed path: a failed write leaves the notice and the table untouched and answers MSG-P7-003 with the incident of R-UNI-39; test for AC2 and TC-E4-038-04.
5. DeviationClient and the X6 branch: a timeout leaves the row in the received state with no reference, keeps the hold and answers 202 with a retry; test for AC1 on the fail-safe side.
6. The transaction that holds the `notice_dispute` row, the notice hold and the decision record together; test for AC1.
7. ContactStopProjection and DeviationEventConsumer over the two events, with the dedupe and the lift of R-UNI-44; tests for X7 and the lift.
8. The read of the disputes with paging and the newest-first order, the feature switch and the contract-fake run of the whole path before any other service is live.

**Feature switch.** `rwb.comms.self-service-dispute`, read as a parameter; off refuses both operations and records nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4038-CON stay green, every accepted dispute has one decision record and one deviation reference, a refused dispute has neither, the stop is set on the raise and cleared on the lift, and no schema of this service names `deviation`, `recovery_case` or a `v_ace_*` view.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is missing or a value is outside its list | Enter {field}. |
| MSG-P6-001 | A contact is attempted on the case while the contact stop is in force; the contact and dispatch path raises it, this story sets the stop it reads | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | A message is attempted on a channel whose consent state this story reads as absent; the contact path raises it | The customer has not consented to {channel}. Use another channel. |
| Not specified in the source documents (GAP-1117; ASM-2065) | The notice is not a sent notice of the case, the party is not returned, or the deviation owner does not answer | The refusal answers 404, 409 or 502-shaped 202 with the platform error envelope; the message IDs and their texts are left to the owner of the message list |

MSG-P7-003, MSG-P4-002, MSG-GEN-001, MSG-P6-001 and MSG-P6-002 are copied unchanged from the validation table of the legacy story and from the rules VR-P6-017-1 and VR-P6-017-2 of FSD P6 A2.17.3.1. MSG-P6-003 ("the {template} template has been withdrawn") belongs to the template and dispatch stories and is not raised here; RWB-P6-E2021-APP and the template stories raise it. The refusal messages of section 5 stand as placeholders until the message list is published, and no text is invented.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template and its approval states, so it cannot show a dispute (GAP-1115; ASM-2063). The customer raises the dispute from the notice screen of the self-service channel; the screen identifier of that surface is Not specified in the source documents (GAP-1114; ASM-2062), and the route, the field list and the masking of the party are RWB-PLT-N001-CON's through the gateway-bff composite route (DP-19). The internal reader sees the disputes of a notice on the notice screen of RWB-P6-E1052-APP, which calls this contract once for the list and once for the notice reference and merges the answers.

| State of the notice | What the reader sees of the disputes |
|---|---|
| A sent notice with no dispute | An empty list, and the notice shows no contact stop |
| A sent notice with a dispute and the stop in force | One or more disputes, newest first, with the channel, the reason code, the raised date, the state and the deviation reference, and the notice shows the stop and its reason |
| A sent notice whose deviation was cleared | The same list with the lift recorded, and the notice shows no stop |
| A dispute refused | Nothing is added to the list, and the refusal message of section 14 is shown |
| A dispute accepted while the deviation owner did not answer | The dispute in the received state with no deviation reference, the stop in force, and the pending reconciliation shown to the internal reader |
| Empty state (no dispute to show) | The empty list of the first row of this table |
| Loading state | Not specified in the source documents (CG-ALL-6711) |
| Error state | Not specified in the source documents (CG-ALL-6711) |
| No access state | Not specified in the source documents (CG-ALL-6711) |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-038-01 | AC1, BR1, BR2, BR3, BR5 | End to end | Notice `N-0101` of case `RC-2026-000321` dispatched with delivery status `PENDING`; the deviation fake answers `DV-0101` and the data fake answers party `P-0101`; the dispute is recorded, the decision record written, `hold_reason` set and `DV-0101` stored |
| TC-E4-038-02 | AC2, BR3 | End to end | Decision log stubbed unavailable; nothing changes, no deviation is raised and MSG-P7-003 is shown |
| TC-E4-038-03 | Access | Component | A role without the Documents right sends the POST and the GET; refused with 403 and MSG-P4-002; a notice outside the scope answers 404 |
| TC-E4-038-21 | AC3, Scope | Component | AC3: a notice outside the caller's scope or not found is refused with 404 and nothing changes |
| TC-E4-038-22 | AC4, Access | Component | AC4: a role without the Documents right sends the dispute POST; refused with 403 and MSG-P4-002 |
| TC-E4-038-23 | Rule | Component | BR4: DeviationCleared lifts the stop on the permitted channels only, and only when the deviation owner clears it |
| TC-E4-038-07 | Rule | Component | BR6: customer, contact and consent facts are read on the rwb-source-data contract within 2 s; no v_ace_* view is read |
| TC-E4-038-08 | Rule | Component | BR7: no business value is hard-coded; reason codes, channel list, decision code, rule id and rule version are read as data |
| TC-E4-038-09 | Rule | Component | BR8: a contact during a stop is refused with MSG-P6-001 and a contact on a channel without consent with MSG-P6-002 |
| TC-E4-038-10 | Rule | Component | BR9: a dispute never lifts a legal hold on the case; the dispute stop is additional to it |
| TC-E4-038-11 | Rule | Component | BR10: a repeated POST with the same Idempotency-Key returns the first answer and raises no second deviation |
| TC-E4-038-12 | Rule | Component | BR11: a deviation event that arrives twice is ignored and the idempotency hit is recorded |
| TC-E4-038-13 | Rule | Component | BR12: only /api/recovery/comms/v1 and rwb.comms.events.v1 are declared; no other path or topic is declared as own |
| TC-E4-038-14 | Rule | Component | BR13: raising a dispute emits no event of this service; the only event of the check is DecisionRecorded |
| TC-E4-038-15 | Rule | Component | BR14: a missing owner answer never records a dispute as fully raised nor answers with a deviation reference it does not hold |
| TC-E4-038-16 | AC5, BR4, BR6 to BR14 | Component | The test cases TC-E4-038-23 and TC-E4-038-07 to TC-E4-038-15 are the test of these rules |
| TC-E4-038-17 | AC6, Access | Component | Notice `N-0101` of case `RC-2026-000321`; caller without valid credentials sends the dispute POST; refused with 401 and nothing changes |
| TC-E4-038-18 | AC7, BR10 | Component | Dispute POST for notice `N-0101` accepted with an Idempotency-Key, then repeated with the same key; the first answer 201 is returned and no second deviation is raised |
| TC-E4-038-19 | AC8, BR14, X6 | Component | Deviation fake for `N-0101` fails or does not answer; the dispute is in the received state with no deviation reference, the notice is held and the answer is Not specified in the source documents (NEWAC-RWB-P6-E4038-APP-AC8) |
| TC-E4-038-20 | AC9 | Component | Dispute in state "received"; a status change the state model does not allow is requested; refused and nothing changes; the refusal message is Not specified in the source documents (GAP-1117) |
| TC-E4-038-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 disputes; no deviation is raised, no dispute row and no hold are written, and an incident is raised under R-UNI-39 |
| TC-E4-038-05 | 12.1 operations and the events of section 12 | Contract | Not specified in the source documents (DOR-RWB-P6-E4038-APP-12); the contract half is in RWB-P6-E4038-CON |
| TC-E4-038-06 | Section 12.7 tables | Component | Not specified in the source documents (DOR-RWB-P6-E4038-APP-12); boundary values of the tables of 12.7 (ASM-3438) |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The four cases keep their legacy IDs, their legacy order, their legacy covers and their legacy data. The legacy table carries no level column, so `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR, as the levels of the target table require. The journey that leaves the contract fakes and touches the real deviation service and the real data contract is not owned by a separate integration story of this key; the tests above run against the fakes of 12.8, and the contract half of the same cases is RWB-P6-E4038-CON's.

### 17. Guardrails

- No business value in code: the reason codes, the channel list, the decision code, the rule id and the rule version are data or reference data read with the version in force.
- No personal data in events, logs, prompts or tests: notice IDs, case IDs, party IDs, dispute IDs, deviation IDs, codes and dates only. No name, address, identity number, account number or contact point is written to `rwb_comms`, to `notice_dispute` or to the decision record.
- No read of another service's tables and no `v_ace_*` read of this service: the deviation is S8's and the customer, contact and consent facts are P1's, and both arrive only on the owner's contract (DP-01, DP-05).
- No deviation table and no case table is declared here: a migration of this service that creates `deviation`, `recovery_case` or a cross-schema key fails the review (DP-01).
- The decision record is written before the change, and a dispute that cannot be recorded does not proceed: the notice is unchanged, no deviation is raised and an incident is raised (R-UNI-39).
- A stop this service did not raise is never released by this service: the lift is applied from `DeviationCleared` of the owner and from nothing else (R-UNI-44, BR4).
- Every outbound event is written to the outbox in the same transaction as the dispute row and the hold, and carries IDs and facts only (DP-03, DP-09).
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story of this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never answers with a deviation reference it does not hold (ADR-020, DP-11).
- Every example is synthetic; no production payload, no production file and no production identifier is copied into a test or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-038 |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-038 ACn) |
| Legacy test cases | TC-E4-038-01 to TC-E4-038-04, all four in the legacy order |
| Legacy feature | FEAT-COM-04 Raise a dispute in self-service (FSD P6 A2.17; Epics 3 to 8 Specification v3, E4 P6), prerequisite FEAT-DVH-05 of the S8 deviation service |
| Feature | FEAT-COM-04 Raise a dispute in self-service |
| L3 process | Not specified in the source documents (DOR-RWB-P6-E4038-APP-2) |
| Legacy data rows | deviation DF-CAS-036 to DF-CAS-045; v_ace_customer DF-ACE-055 to DF-ACE-074; notice DF-LEG-015 to DF-LEG-023 and DF-LEG-030 to DF-LEG-034; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015; template DF-REF-045 to DF-REF-051 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 and DP-15 in force as rules) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-04, R-UNI-20, R-UNI-39, R-UNI-40, R-UNI-44, R-LIT-05, R-RES-19 and R-SET-12 (the same stop event in the restructure and settlement stages), BR-P6-017, VR-P6-017-1 and VR-P6-017-2 of FSD P6 A2.17.3.1 |
| Requirements | REQ-OCC-011, customer self-service for an offer, a signature, a payment and a dispute on the bank's digital channels (FSD P6 requirements served, E4, Should); TSD P6 T8 maps REQ-OCC-011 to FEAT-COM-01, which the feature table of the FSD and of Epics 3 to 8 does not support (GAP-1115; ASM-2063) |
| Contract and tests | RWB-P6-E4038-CON, TC-P6-E4038-CON-01 to TC-P6-E4038-CON-06, and the fakes of 12.8 |

The supporting facts of the legacy key — the X1 deviation and its pause (FEAT-DVH-05 of S8), the case and its clocks (P3), the customer and consent data (P1) and the central ledger entry (P7, DP-03) — are answered here for the rwb-comms slice and by their owners for their own slices, and this story changes none of their designs. The two operations and the `notice_dispute` row are this run's own decision and are marked as such (GAP-1112; ASM-2060).

### 19. Out of scope

- The X1 deviation, its code, its owner, its clock and the pause and return of the case: S8 rwb-deviation (`deviation` in `rwb_deviation`, FEAT-DVH-05, `DeviationWorkflow`). This story calls the operation and consumes the two events and builds none of it.
- The case, its state, its timers and its scope: P3 rwb-case. This story reads the case scope the edge passes and reads no case row.
- The customer, the contact points and the consent state: P1 rwb-source-data through DP-05, and the ACE views it alone reads.
- The contract baseline, its two operations, its element set, its new table, its fakes and its tests: RWB-P6-E4038-CON.
- The decision-record library, its chain and its outbox: RWB-PLT-E1027-CON and the RWB-PLT-LIB stories; this story writes through them.
- The dispatch of a notice, JOB-10, the WIN file and `NoticeDispatchWorkflow`: RWB-P6-E2021-APP and RWB-P6-E2021-CON. The stop this story sets is read there; the hold of a dispatch is not built here.
- The notice generation, the template catalogue and the proof of delivery: RWB-P6-E1052-APP, RWB-P6-E1046-APP and RWB-P6-E5002-APP.
- The gateway-bff composite route, the customer sign-in, the screen field list and the masking at the edge: RWB-PLT-N001-CON, RWB-P4 stories and the bank's channel applications.
- The reason codes, the decision code, the rule id, the refusal texts and the state vocabulary of a dispute: the owners of the reference data, the parameters and the message list.
