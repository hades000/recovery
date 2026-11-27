# RWB-P7-E2006-APP Credit approval pack for NLEADS

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P7-E2006-APP |
| Readiness decisions | RD-P1-004 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-P7-E2006-APP-16) |
| Patterns applied | DP01, DP03, DP05, DP07, DP11, DP15, DP19 |
| Parallel lane | L-P7-T |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E2006-CON (not yet created; contract version: Not specified in the source documents (DOR-RWB-P7-E2006-APP-23)) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (no FR mapped to REQ-CHO-008, REQ-CHO-006, REQ-RDF-009) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 22 November 2026: the rwb-decision slice of RWB-E2-006 is issued as its own story, holding the level the delegation of authority requires for a credit decision read in one hop at the moment of the result and the D5 credit result sealed as one hash-chained decision log entry that carries the NLEADS reference, the result, the level applied and the version. The pack assembly, the two treatment endpoints and the four result columns stay with rwb-integration and rwb-treatment, and the route move with rwb-case. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 31 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT) recording on a plan what NLEADS decided, and an internal auditor (RW-AUDIT) reading it afterwards**, I want **the level the delegation of authority requires for the credit decision read in one hop from the service that owns that table on the date of the result, that level compared with the level NLEADS returned, and the credit result sealed as one append-only, hash-chained decision log entry carrying decision code D5, the final call, both levels, the delegation version, the NLEADS reference and the result date**, so that **a credit result on a plan can be explained from one record the same day, and no result is recorded at a level the delegation of authority does not allow**.

This is the `rwb-decision` slice of legacy RWB-E2-006 and it owns no legacy criterion: `acs` is empty, and the criteria of section 7 are new and test only what this service delivers. What sits here:

- The level: read at the moment of the result, for decision code D5, item 2.1.1, the product group, the amount and the result date, in one REST hop with a 2 s budget and a fake (DP-07, DP-11). No level, limit or version is held in code and no delegation row is copied here (DP-01, FSD P7 A2.24: "Reads the limits from the versioned table at the moment of the decision, and records the version used"). The table is not one of the six P7 owns, and the sources disagree on its home (GAP-2478; ASM-4112).
- The record: one `decision_log_entry` per credit result, decision code D5, final call "approved" or "rejected", the level applied and the level required, the delegation version, the NLEADS reference and the result date in the actions payload, the inputs reference, the actor, the decided time and the chain position. Written through the local decision-record library and announced as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` (DP-03, ADR-022).
- The check: the level NLEADS returned is at or above the level the delegation requires, compared against the value the owning contract returns and not against a rank in code; below it, the result is refused and nothing changes.
- The reads: `GET /approvals/{approvalId}` for the pack screen and the two decision-log reads for the auditor, on base `/api/recovery/decision/v1` (DP-13), in schema `rwb_decision`, with the topic `rwb.decision.events.v1` and the queue `rwb-decision`.
- The values of the legacy case are copied unchanged: case RW-2026-000610 and case RW-2026-000620 in route state PLAN_RUNNING, treatment TRT-SYN-0610 of type RESTRUCTURE with offer amount 2,400,000.00 baht, haircut 0.00 baht and 84 installments valid until 2026-12-29, product group MORTGAGE, plan status APPROVED, required level L6 under item 2.1.1, recorded level L5, references NL-SYN-000610, NL-SYN-000611, NL-SYN-000612 and NL-SYN-000613, result date 2026-12-17, and the delegation files DOA-2026.11 and DOA-2027.01 (legacy sections 4, 7 and 14).

### 2. Business rationale

Legacy RWB-E2-006 promised that a plan which goes to credit is decided in NLEADS, that the outcome lands on the case, and that the decision log holds a D5 entry with the final call and the NLEADS reference before anything moves. Two of those promises are this service's: the level that says who could have decided, and the record that proves what was decided and when.

Both fail quietly once the monolith is cut. The delegation of authority is versioned reference data of another service, loaded by file, approved by a second officer and in force from a date (FSD P7 A2.24; Temporal and Drools slide 6: "Delegation limits are held as versioned reference data (delegation_limit) and follow the same approve-and-date discipline"). A service that carries a level in code, or reads the table itself, routes a 2,400,000.00 baht MORTGAGE restructure to the wrong authority the moment DOA-2027.01 replaces DOA-2026.11, and nothing fails. The decision log is no longer one writer in one process either: each service writes locally and the ledger is sealed from `rwb.decision-record.v1`, so a result can reach the treatment with no entry and the case still looks decided.

This story puts both guarantees back: the level is read at the moment of the result, with the version used written on the entry, and the entry is written before the approval status changes, so a result that cannot be recorded does not proceed (Principle 5, R-UNI-39, CTL-06).

It is one of five slices of the legacy key: the pack and the two treatment endpoints are rwb-integration's (RWB-P2-E2006-APP), the four result columns and the treatment state are rwb-treatment's (RWB-S2-E2006-APP), the route state move and the queue are rwb-case's (RWB-P3-E2006-APP), and the routing and escalation are this service's other slice (RWB-P7-E2013-APP). NLEADS has no interface and is never called from here (INT-26, legacy BR4). The story serves REQ-CHO-008 and REQ-CHO-006 on the record side and REQ-RDF-009 through the inputs reference, and supports CTL-04, CTL-06 and NFR-033.

### 3. Preconditions

- The `rwb_decision` baseline is in place: schema and login (DP-02), `decision_log_entry` with `chain_seq`, `prev_hash`, `entry_hash`, `corrects_entry_id` and `idempotency_key`, `approval`, the outbox and the inbox, the base and the topic (RWB-P7-E1008-APP; RWB-P7-E1027-APP and RWB-PLT-E1027-CON for the record library).
- The D5 approval of the case exists in `approval` in status WAITING, routed by RWB-P7-E2013-APP, carrying case RW-2026-000610, treatment TRT-SYN-0610, decision code D5, capability area TREATMENT_AND_OFFER, product group MORTGAGE and amount 2,400,000.00 baht, with the delegation row and the version that routing stamped. This story reads that row and writes its status and its `decision_log_id`; it creates no route and no queue entry.
- The delegation read of rwb-access (P4) is published with its fake: the level, the row id and the version in force for a decision code, a regulation item, a product group, an amount and a date. The path, the request and the answer shape are Not specified in the source documents (GAP-2479; ASM-4113).
- The rows of item 2.1.1 for MORTGAGE, and file DOA-2026.11 in force from 2026-11-30, are loaded and approved in the owning service (DL18; FSD P7 A2.24 AC-P7-024-01).
- LOV-APPROVAL-LEVEL (L1 to L6) and LOV-APPROVAL-STATUS (WAITING, HELD_NO_LIMIT, APPROVED, REFUSED, RETURNED) are present in the reference lists, and the final-call set is the one the record library validates (RWB-PLT-E1027-CON).
- The caller holds the Decision log right A with case RW-2026-000610 in scope. The legacy story asked for the Treatment and offer right U instead; the difference is recorded in GAP-2481 and ASM-4115.
- No human approval gate is met for this story set: the status is Draft and an assumption records it (ASM-4119).

### 4. Flow

1. The officer submits the plan in NLEADS from the pack assembled by rwb-integration, records the result on the treatment, and the treatment service calls the recording operation of this service with the NLEADS reference, the result, the level NLEADS returned, the result date and, for a refusal, the reason.
2. `CreditDecisionController` validates the body and the `If-Match` version, resolves the D5 approval of the treatment (GAP-2482; ASM-4116) and calls `DelegationLevelClient`.
3. The client reads the required level for decision D5, item 2.1.1, product group MORTGAGE, amount 2,400,000.00 baht and the result date, in one hop with a 2 s timeout.
4. `CreditDecisionService` compares the level NLEADS returned with the level required. Below it the answer is 409 with MSG-P2-018 and nothing is written; with no row covering the request, 409 with MSG-P7-010 and an incident to the RW-RISK queue; with the read unavailable, 503 with MSG-GEN-006.
5. The service writes one `decision_log_entry` through the decision-record library, in the same transaction as the approval status change and before it.
6. The approval moves to APPROVED or REFUSED with its `decision_log_id`, the level returned and the version used, under the `If-Match` version check.
7. The library puts `rwb.decision.DecisionRecorded.v1` in the outbox; the relay publishes it on `rwb.decision-record.v1` and on `rwb.decision.events.v1` (GAP-2483; ASM-4117).
8. A failed entry write rolls the transaction back: 503 with MSG-P7-003, an incident, and neither the approval nor the case moves; the offer release, the refusal reason on the route and the return of the case stay with R-RES-11, R-RES-12 and R-RES-14 in rwb-case and rwb-treatment.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A checklist document is not on the case | The pack marks the item missing; this service is not called | MSG-P2-009 | AC11; RWB-P2-E2006-APP |
| X2 | A balance in the pack is older than its age limit | The pack shows the input age; the entry carries the inputs reference beside it | MSG-P7-006 | RWB-P2-E2006-APP; AC1 |
| X3 | Reference empty, or a refusal without a reason | Refused; nothing changes | MSG-GEN-001 | AC5 |
| X4 | Result date after today | Refused | MSG-GEN-002 | AC5 |
| X5 | The NLEADS approval level is below the level the delegation requires | Refused; the approval stays WAITING and no entry is written | MSG-P2-018 | AC6 |
| X6 | A result is already recorded on the approval | Refused; no second entry | MSG-P2-010 | AC7 |
| X7 | The case is not in AWAITING_CREDIT_APPROVAL, or the treatment is not a restructure | Refused by the owning service; this service is not called | MSG-P3-005 | AC12; AC13; RWB-P3-E2006-APP |
| X8 | The approval changed between the read and the write | Refused | MSG-GEN-004 | AC10 |
| X9 | The decision log write fails | Nothing changes; an incident is raised | MSG-P7-003 | AC8 |
| X10 | A role without the Decision log right A | Refused; nothing changes | MSG-P4-002 | AC4, AC9 |
| X11 | No row of the delegation of authority covers the request | Refused; nothing changes; an incident to the RW-RISK queue | MSG-P7-010 | AC1 |
| X12 | The delegation read is unavailable | Refused; nothing changes | MSG-GEN-006 | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the `approval` row of RWB-P7-E2013-APP and the record library of RWB-P7-E1027-APP, and the published delegation read |
| Negotiable | The level, the item, the versions and the input age limit are rows and contract answers, never code |
| Valuable | Puts the authority and the proof of a credit decision on one record, and stops a result at the wrong level |
| Estimable | Five operations, two tables of one schema, one client, one fake and one migration step |
| Small | Within two weeks with its tests |
| Testable | Each criterion of section 7 is one automated test, and each legacy test case of section 16 is one script |

### 7. Acceptance criteria

```gherkin
Feature: Credit approval pack for NLEADS, the rwb-decision slice

  Background:
    Given case "RW-2026-000610" is in route state "AWAITING_CREDIT_APPROVAL"
    Given treatment "TRT-SYN-0610" of type "RESTRUCTURE" has offer amount 2,400,000.00 baht, haircut 0.00 baht and 84 installments
    Given the ACE plan status of the case is "APPROVED"
    Given the plan needs approval at level "L6" or higher under item 2.1.1
    Given the D5 approval of treatment "TRT-SYN-0610" is "WAITING" with amount 2,400,000.00 baht and product group "MORTGAGE"

  Scenario: AC1 The required level is read in one hop on the result date and stamped on the entry (new, D-RCV-60)
    Given the rwb-access contract mock returns level "L6", the row id of item 2.1.1 at L6 and version "DOA-2026.11" for decision "D5", item "2.1.1", product group "MORTGAGE", amount 2,400,000.00 baht on 2026-12-17
    When the caller records reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date "2026-12-17"
    Then the delegation read is one REST hop and answers inside 2 s
    Then one decision log entry exists with decision code "D5", final call "approved", approval level "L5", the row id of item 2.1.1 at L6 and version "DOA-2026.11" in its actions, the inputs reference, the actor, the decided time and its chain_seq, prev_hash and entry_hash
    Then the service reads no delegation row, no case, no treatment and no balance as a table of another schema
    When no row of the delegation of authority covers the request
    Then the response is 409 with message MSG-P7-010 and an incident is raised to the RW-RISK queue
    Then no entry is written and the approval stays "WAITING"

  Scenario: AC2 The version in force on the result date is the version written on the entry (new, D-RCV-60)
    Given version "DOA-2027.01" is in force from 2027-01-01 and moves the same amounts to level "L5"
    And an earlier D5 result for the same amounts was recorded on 2026-12-17 with version "DOA-2026.11" on its entry
    When a D5 result is recorded on 2027-01-02 with approval level "L5"
    Then the delegation read returns level "L5" and version "DOA-2027.01"
    Then the new entry carries level "L5" and version "DOA-2027.01" in its actions
    Then the earlier entry still carries "DOA-2026.11" and the approval routed on 2026-12-15 keeps the version routing stamped on it

  Scenario: AC3 The pack shows the required level through the approval read (new, D-RCV-60)
    Given the approval was routed at level "L6" with version "DOA-2026.11" and amount 2,400,000.00 baht
    When the pack screen asks for the approval through the gateway-bff composite route
    Then the answer carries decision code "D5", product group "MORTGAGE", amount 2,400,000.00 baht, level "L6", version "DOA-2026.11", status "WAITING" and the decision log id
    Then the answer carries no account, balance, collateral value, appraisal, document or refusal reason
    Then a caller whose scope excludes case "RW-2026-000610" receives 404 with MSG-P4-003

  Scenario: AC4 An approved NLEADS result is recorded as one D5 entry before the approval moves (new, D-RCV-60)
    Given the caller holds the Decision log right "A" with case "RW-2026-000610" in scope
    When the caller records reference "NL-SYN-000610", result "APPROVED", approval level "L5" and result date "2026-12-17"
    Then the approval status is "APPROVED" and it holds the decision log id of the entry
    Then the entry's actions carry reference "NL-SYN-000610" and result date "2026-12-17"
    Then rwb.decision.DecisionRecorded.v1 for case "RW-2026-000610" is in the outbox with no account number, balance, address or refusal reason in its payload
    Then the entry was committed before the approval status changed

  Scenario: AC5 A refused NLEADS result is recorded with its reason, and invalid input is refused (new, D-RCV-60)
    When the caller records reference "NL-SYN-000611", result "REFUSED" and reason "Income does not cover 84 installments"
    Then the approval status is "REFUSED" and it holds the reason
    Then one entry exists with decision code "D5", final call "rejected" and override_reason "Income does not cover 84 installments"
    When the caller records result "REFUSED" with reference "NL-SYN-000612" and an empty reason
    Then the response is 422 with message MSG-GEN-001 for field "reason"
    When the caller records a result date "2026-12-31" on "2026-12-17"
    Then the response is 422 with message MSG-GEN-002
    Then the approval does not change and no second entry is written

  Scenario: AC6 A level below the level required is refused and nothing is written (new, D-RCV-60)
    Given the rwb-access contract mock returns level "L5" as the level required for this approval
    When the caller records reference "NL-SYN-000612", result "APPROVED" and approval level "L6"
    Then the response is 409 with message MSG-P2-018 with level "L6" and required level "L5"
    Then the approval stays "WAITING", and no entry and no outbox row is written

  Scenario: AC7 A second result or a repeated request writes no second entry (new, D-RCV-60)
    Given the approval holds result "APPROVED" with reference "NL-SYN-000610" recorded on "2026-12-17" and one entry
    When the caller records a result again
    Then the response is 409 with message MSG-P2-010
    When the same request is replayed with the same Idempotency-Key
    Then the first entry is returned and no second entry is written

  Scenario: AC8 A result that cannot be recorded does not happen (new, D-RCV-60)
    Given the decision log store is unavailable
    When the caller records reference "NL-SYN-000613", result "APPROVED" and approval level "L5"
    Then the response is 503 with message MSG-P7-003
    Then the approval stays "WAITING", no entry exists and no event is in the outbox
    Then an incident is raised to the platform administrator queue

  Scenario: AC9 The credit result is read back by audit within the scope (new, D-RCV-60)
    Given the D5 entry of treatment "TRT-SYN-0610" exists with its chain position
    When RW-AUDIT reads the decision log for case "RW-2026-000610" and decision "D5"
    Then the page carries that one entry with final call "approved", the level applied "L5", the level required "L6", version "DOA-2026.11" and reference "NL-SYN-000610"
    And the entry read by its own id carries the same chain_seq, prev_hash and entry_hash
    Then a caller whose scope excludes the case receives 404 with MSG-P4-003

  Scenario: AC10 Two callers record a result at once (new, D-RCV-60)
    Given two callers read the D5 approval of treatment "TRT-SYN-0610" at version "3"
    When both record a result with If-Match "3"
    Then the service saves one result and one entry
    Then the service refuses the other with 409 and message MSG-GEN-004

  Scenario: AC11 A missing checklist document is marked missing by the pack and this service is not called (new, D-RCV-60)
    Given checklist document "INCOME_PROOF" is not on case "RW-2026-000610"
    When the pack is requested for treatment "TRT-SYN-0610"
    Then the pack marks the item missing with message MSG-P2-009
    Then this service is not called and no entry is written

  Scenario: AC12 A case outside AWAITING_CREDIT_APPROVAL is refused by its owning service and this service is not called (new, D-RCV-60)
    Given the route state of case "RW-2026-000610" is "PLAN_RUNNING"
    When the caller records reference "NL-SYN-000614", result "APPROVED" and approval level "L5"
    Then the owning service refuses with message MSG-P3-005
    Then this service is not called and no entry is written

  Scenario: AC13 A treatment that is not a restructure is refused by its owning service and this service is not called (new, D-RCV-60)
    Given the treatment "TRT-SYN-0610" is not a restructure
    When the caller records reference "NL-SYN-000614", result "APPROVED" and approval level "L5"
    Then the owning service refuses with message MSG-P3-005
    Then this service is not called and no entry is written

  Scenario: AC14 No code of this story calls NLEADS (new, D-RCV-60)
    Then the code of this story has no call to NLEADS and no outbound interface to NLEADS

  Scenario: AC15 A call without a valid credential or without the right is refused with 401 or 403 (new, D-RCV-60)
    When a caller calls a recording or read operation with no valid credential
    Then the response is 401
    When a caller without the Decision log right calls a recording or read operation
    Then the response is 403

  Scenario: AC16 A timed-out recording activity is retried without a second entry, and a timeout before commit writes nothing (new, D-RCV-60)
    Given the record-result activity for treatment "TRT-SYN-0610" timed out before it committed
    When the activity is retried with the same Idempotency-Key
    Then one entry exists after the retry and the approval holds its decision log id
    When the record-result activity times out before it commits
    Then no entry and no outbox row are written and the approval stays "WAITING"
```

### 8. Business rules

| ID | Rule | Source | Where it lands here |
|---|---|---|---|
| BR1 | A restructure outside the approved range or with a deviation goes to credit approval | R-RES-10 | The approval exists before this story is called; the case state is rwb-case's |
| BR2 | Credit approval releases the offer to the customer with a 14-day validity | R-RES-11 | Outside this slice: rwb-treatment and rwb-case after the event of 12.3 |
| BR3 | A credit refusal records the reason, then returns the case to the route decision for the case owner | R-RES-12, R-RES-14 | The reason is held on the approval and on the entry here; the route move is rwb-case's |
| BR4 | NLEADS has no interface; the officer submits and records the result | INT-26; DL12 | No call to NLEADS from any code of this story (AC14) |
| BR5 | The approval level must be at or above the level the delegation of authority sets for the decision, product and amount | doa.txt item 2.1.1; CTL-04; DL18; FSD P7 A2.24 | Compared against the value the owning contract returns on the result date (AC1, AC6); L1 is the highest authority, so L6's THB 100m limit is why THB 120m moves to L5 |
| BR6 | The pack documents are those of the NLEADS pack checklist | Document types reference table; DL19 | The checklist and its document links are rwb-integration's and rwb-document's |
| BR7 | An input past its age limit is shown with its age | MSG-P7-006; REQ-RDF-009 | The pack shows the age; the entry carries the inputs reference it was taken from |
| BR8 | A decision that cannot be written to the decision log does not proceed | Principle 5; R-UNI-39; CTL-06 | AC8: the transaction rolls back and nothing moves |
| BR9 | A restructure covers every account of the customer in the case | CTL-26 | Outside this slice: the account set is the pack's, and no balance is read here |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WAITING | Credit result approved | final call approved and the level at or above the level required | APPROVED |
| WAITING | Credit result refused | final call rejected with a reason | REFUSED |
| WAITING | Level below the level required | any | WAITING, 409 MSG-P2-018 |
| WAITING | No delegation row covers the request | any | WAITING, 409 MSG-P7-010, incident to the RW-RISK queue |
| WAITING | The delegation read is unavailable | any | WAITING, 503 MSG-GEN-006 |
| WAITING | Decision log write fails | any | WAITING, 503 MSG-P7-003, incident |
| APPROVED or REFUSED | Any further result | any | unchanged, 409 MSG-P2-010 |

The legacy route-state table is unchanged and moves in `rwb-case`, not here: AWAITING_CREDIT_APPROVAL to OFFER_WITH_CUSTOMER on CREDIT_APPROVED by R-RES-11, to DECLINED_BY_CREDIT on CREDIT_DECLINED by R-RES-12, and to BACK_TO_ROUTE_DECISION on DECLINE_RECORDED by R-RES-14 (legacy section 9; RWB-P3-E2006-APP). The treatment state moves from SUBMITTED to APPROVED or REFUSED in `rwb-treatment` (RWB-S2-E2006-APP). HELD_NO_LIMIT and RETURNED are statuses of the routing slice and are not set here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT, restructuring officer | Records the NLEADS result on a case in scope (legacy: Treatment and offer, CRUA; here Decision log, A) |
| RW-CASEOWN, case owner | Records the result on cases in scope (legacy: Treatment and offer, CRU; here Decision log, A) |
| RW-CREDCOMM, RW-PRODHEAD | Read the pack, the approval and the entry (Decision log, R); they approve in NLEADS, not here |
| RW-AUDIT, RW-COMPLY, RW-CONDUCT | Read the entry and its chain position (Decision log, R) |
| SY-DECLOG, decision log writer | Writes the entry through the record library (Decision log, C) |
| SY-CASEWF, SY-RULES | Read the entry and move the case on the event (Decision log, C) |
| Approval levels L1 to L6 | As in doa.txt item 2.1.1, recorded from NLEADS on the entry and never as a right |

The right declared on the recording operations is the Decision log right A of TSD P7 API-P7-003 and API-P7-005, while the legacy story requires the Treatment and offer right U; the difference is a gap and an assumption (GAP-2481; ASM-4115), and no role gains or loses a right in this story.



### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | decision_log_entry | id | Write |
| DF-DEC-002 | decision_log_entry | case_id | Write, from the approval |
| DF-DEC-003 | decision_log_entry | decision_code | Write, D5 |
| DF-DEC-008 | decision_log_entry | inputs_ref | Write, the inputs snapshot the decision rests on (GAP-2480) |
| DF-DEC-011 | decision_log_entry | approval_level | Write, the level NLEADS returned |
| DF-DEC-012 | decision_log_entry | final_call | Write, approved or rejected |
| DF-DEC-013 | decision_log_entry | override_reason | Write, the refusal reason |
| DF-DEC-014 | decision_log_entry | actions | Write, the required level, the row id, the version, the NLEADS reference and the result date (GAP-2480) |
| DF-DEC-016 | decision_log_entry | decided_at | Write, the result date and time |
| DF-DEC-017 | decision_log_entry | prev_hash | Write, by the record library |
| DF-DEC-018 | decision_log_entry | entry_hash | Write, by the record library |
| DF-DEC-028 | decision_log_entry | chain_seq | Write, by the record library |
| DF-DEC-030 | decision_log_entry | actor_user_id | Write, the caller |
| DF-DEC-031 | decision_log_entry | idempotency_key | Write, from the Idempotency-Key header |
| DF-DEC-035 | approval | regulation_item | Read, item 2.1.1 |
| DF-DEC-038 | approval | approval_level | Read at routing; write the level NLEADS returned |
| DF-DEC-039 | approval | delegation_limit_id | Read, stamped by routing |
| DF-DEC-040 | approval | limit_version | Read, stamped by routing |
| DF-DEC-041 | approval | product_group | Read |
| DF-DEC-042 | approval | amount | Read |
| DF-DEC-046 | approval | status | Write |
| DF-DEC-053 | approval | decision_log_id | Write |

Not owned and never read as a table: `delegation_limit` and `role` (P4, through its contract), `recovery_case` and `treatment` (P3 and S2, through their contracts), `document` (P5), `v_ace_*` (read only by rwb-source-data, DP-05). The four legacy treatment columns `nleads_ref`, `credit_result`, `credit_result_reason` and `credit_result_at` (DF-TRT-023 to DF-TRT-026; `credit_result_at` is Not specified in the source documents (CG-ALL-7077)) belong to the treatment owner and are not written here.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The paths are the ones TSD P7 v2 T-A.1 carries and the Ownership Map gives to P7. Not provided here, and belonging to other P7 stories: `GET /approvals` and `POST /approvals/{approvalId}/return` (RWB-P7-E2013-APP), the 12 rule-governance operations of RWB-P7-E1073-APP, and `GET /cases/{caseId}/recommendation`, whose single owner among the P7 stories is not stated in the sources read (GAP-2484; ASM-4118).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/approve` | API-P7-003: record an approved NLEADS result at the level returned; 200 with the DecisionLogEntry | Decision log, right A, scope applied | `Idempotency-Key` header; one result per approval |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/refuse` | API-P7-005: record a refused NLEADS result with its reason; 200 with the DecisionLogEntry | Decision log, right A, scope applied | `Idempotency-Key` header; one result per approval |
| GET | `/api/recovery/decision/v1/approvals/{approvalId}` | API-P7-008: one approval with its decision code, product group, amount, level, version, status and decision log id for the pack screen; 200 with the ApprovalDetail | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log` | API-P7-006: entries searched by `caseId`, `decision`, `ruleId`, `approver`, `from`, `to`, `page` and `size`; 200 with the DecisionLogPage | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | API-P7-007: one entry with its decision code, final call, levels, version, reference and chain fields; 200 with the DecisionLogEntry | Decision log, right R, scope applied | Not applicable, read only |

The request body of the two recording operations carries `nleadsRef`, `result` (APPROVED or REFUSED), `approvalLevel` (L1 to L6), `resultDate`, `reason` (required when REFUSED, 1 to 1,000 characters) and the header `If-Match`. The DecisionLogEntry body carries `entryId`, `chainSeq`, `caseId`, `decisionCode`, `finalCall`, `approvalLevel`, `inputsRef`, `decidedAt`, `prevHash`, `entryHash`, `correctsEntryId` and `actorUserId`, and for a D5 entry the required level, the delegation row id, the version, the NLEADS reference and the result date. The field-level shape of the actions payload and the 1 to 30 letters, digits and dashes of the NLEADS reference are Not specified in the source documents (GAP-2480; ASM-4114). Errors: 401 with Not specified in the source documents (CG-ALL-7083); 403 with MSG-P4-002; 404 with MSG-P4-003; 409 with MSG-P2-010, MSG-P2-018, MSG-P7-010 or MSG-GEN-004; 422 with MSG-GEN-001 or MSG-GEN-002; 503 with MSG-P7-003 or MSG-GEN-006. Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Purpose | Owner | Operation | Notes |
|---|---|---|---|
| The level required for a decision on a date | rwb-access (P4) | `GET /api/recovery/access/v1/doa-limits` | Answers the level, the delegation row id and the version in force for a decision code, a regulation item, a product group, an amount and a date. The resource name, the query parameters and the body are Not specified in the source documents (GAP-2479; ASM-4113) |

One hop, 2 s timeout, no retry on the caller path and a circuit breaker that refuses a stale answer rather than guessing. The read replaces the legacy `String DelegationQuery.requiredLevel(String decisionCode, String productGroup, BigDecimal amount)` of the in-process interface; the date argument is new and is the result date, because the level in force on the day of the decision is what BR5 and FSD P7 A2.24 require. P7 makes this one REST call and no other, which is its only cell in the matrix of Architecture v5 slide 13, and the home of the table itself is the disagreement GAP-2478 records.

#### 12.3 Events published

| Event | Topic | When | Payload |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` (shared, the ledger of ADR-022) | One per D5 entry, from the outbox in the same transaction | `entryid`, `caseid`, `decisioncode` D5, `approver` |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | As above, for the rwb-reporting read model, which the matrix of slide 13 gives an event subscription to P7 | The same payload. The event name on the service topic is Not specified in the source documents (GAP-2483; ASM-4117) |

CloudEvents envelope, keyed by case id, retry and `.dlt` topics per R4. No account number, no balance, no name, no address and no refusal reason travel on either topic; the reference, the codes, the levels and the dates are carried with the entry id, and the refusal reason is read from the entry by a caller with the right.

#### 12.4 Events consumed

| Item | Value | Service |
|---|---|---|
| Events consumed | None. This story consumes no event: the result arrives on the recording operations of 12.1, and the approval is created by the routing slice. P7's two inbound event cells in the matrix of slide 13, from rwb-comms and rwb-agent, belong to the notice and agent stories | rwb-decision |

#### 12.5 Workflows and activities

| Item | Value |
|---|---|
| Workflows and activities | None registered here. The `ApprovalWorkflow` of `rwb-decision` belongs to RWB-P7-E2013-APP on queue `rwb-decision`; its reminder and escalation steps call the same approval reads and no activity of this story. The recording path is a REST transaction with the record library, not a workflow step |

#### 12.6 Schedules

| Item | Value |
|---|---|
| Schedules | None. The three jobs of this service, JOB-13, JOB-14 and JOB-20, belong to the ledger chain check, the queue measures and the rule promotion and are other stories' Schedules on queue `rwb-decision` (DP-10) |

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7, schema `rwb_decision` | The D5 credit entry: case, decision code, levels, version, reference, result date, inputs reference, actor, decided time and the chain position; append only, no UPDATE and no DELETE grant |
| `approval` | P7, schema `rwb_decision` | Read the D5 row; write its status, the level NLEADS returned and `decision_log_id`; one result per row |
| `outbox_event`, `idempotency_key`, `processed_event` | PLT library, created in `rwb_decision` | The `DecisionRecorded` fact of 12.3 and the repeat protection of AC7 |

One Flyway step in `rwb_decision` (DP-15) adds the unique constraint on `(source_type, source_ref)` for decision code D5 and the index on `(case_id, decision_code, decided_at)`; it creates no table, alters no column and touches no other schema. No foreign key crosses a schema (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-access delegation fake | The published contract of P4 behind 12.2 | `D5`, item `2.1.1`, `MORTGAGE`, 2,400,000.00 baht on 2026-12-17 → level `L6`, the row id of item 2.1.1 at L6, version `DOA-2026.11`; the same amounts on 2027-01-02 → level `L5`, version `DOA-2027.01`; the same amounts on 2027-01-02 with required level `L5` for AC6; `NOT_COVERED` with MSG-P7-010 for a product with no row; a timeout for the unavailable read |
| decision-record library fake | RWB-PLT-E1027-CON | The append, the next `chain_seq`, the `prev_hash`, the `entry_hash` over the canonical form, the append-only refusal, the idempotency answer of AC7 and a forced `DecisionLogUnavailableException` for AC8 |
| rwb-access scope fake | The edge declaration of DP-19 | The allow answer with the Decision log right `A` and case `RW-2026-000610` in scope; the refusal of MSG-P4-002 for a role without the right, and the scope `MTG-BKK` against case `RW-2026-000620` of another team for MSG-P4-003 |

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 5, consumed 1 | The two recording operations and the three reads provided; the delegation read of rwb-access consumed in one hop with a 2 s timeout (DP-11) |
| Kafka | Published 1 event on 2 topics, consumed 0 | `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and on `rwb.decision.events.v1`, through the outbox of the record library |
| Temporal | None | No workflow, no activity and no Schedule; `ApprovalWorkflow` is the routing slice's |
| File | None | No file input and no file output; the pack, the documents and the NLEADS reference arrive as values on the request |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `credit`, Java package `th.co.scb.ace.workbench.recovery.decision.credit`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_decision`; no delegation, case, treatment or ACE table is read | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The balance, the days past due and the data date come from rwb-source-data through rwb-integration's pack; this service stores the inputs reference only | none |
| DP-07 | Reference data, LOV | The delegation rows are read through the contract of the service that owns them; the capability area, the product group and the approval levels are LOVs of the service | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the record and its seal on the shared topic; DP-01 and DP-07 are the boundary, since no delegation row is copied and no rank is written in code; DP-05 is an instance only as an absence, because the balances the pack shows are read by rwb-integration through rwb-source-data and this service never touches a `v_ace_*` view; DP-11 is the one hop with the 2 s budget; DP-15 is the single migration step; DP-19 is the composite route through which SCR-14 shows the level. The four platform contracts the DP table adds are not in the metadata build row, which stays None and Day 1 (GAP-2484; ASM-4118).

| Component | Type | Responsibility |
|---|---|---|
| `CreditDecisionController` | Controller | The two recording operations and the three reads; validation; problem responses; `If-Match` |
| `CreditDecisionService` | Service | The level check, the entry write before the status change, the approval update, the outbox fact |
| `DelegationLevelClient` | REST client | One hop to the delegation read of rwb-access, 2 s timeout, circuit breaker, no cached level |
| `CreditEntryReader` | Service | The two decision-log reads with the scope filter and the chain fields |
| `ApprovalRepository` | Repository | `approval` and `decision_log_entry` in `rwb_decision` only |

**Build steps.** (1) The migration step and the constraint of 12.7. (2) `DelegationLevelClient` against the fake of 12.8, with the timeout and the `NOT_COVERED` path. (3) `CreditDecisionService` with the level check, the entry through the record library and the rollback of AC8. (4) The two recording operations with the right, the scope, the version and the idempotency key. (5) The three reads and the payload guard of AC4 and AC9. (6) The outbox relay for the two topics.

**Feature flag.** None: the path is behind the existing Decision log right, and the routing slice's flag governs whether an approval is created at all.

**Done when.** The tests of section 16 pass, the entry of a synthetic credit result is read back from `rwb.decision-record.v1` by a second consumer with no customer field in it, and an auditor reads the same result through the decision log with its chain position intact.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-018 | NLEADS approval level below the required level | The NLEADS approval is at level {level}. This plan needs level {required} or higher. |
| MSG-P2-010 | Result already recorded | The NLEADS result for this treatment was recorded on {date}. |
| MSG-GEN-001 | Reference or refusal reason empty | Enter {field}. |
| MSG-GEN-002 | Result date after today | {field} must be between {min} and {max}. |
| MSG-GEN-004 | Approval changed by someone else | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P7-010 | No delegation row covers the decision | No approval limit covers {decision} for {product}. The item is held and Risk has been told. |
| MSG-GEN-006 | The delegation read is unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P4-002 | A role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The approval or the entry is out of scope | This case is not in your scope. |
| MSG-P2-009 | A checklist document is not on the case | Not specified in the source documents (DOR-RWB-P7-E2006-APP-9) |
| MSG-P3-005 | The case is not in AWAITING_CREDIT_APPROVAL, or the treatment is not a restructure | Not specified in the source documents (DOR-RWB-P7-E2006-APP-9) |
| MSG-P7-006 | A balance in the pack is older than its age limit | Not specified in the source documents (DOR-RWB-P7-E2006-APP-9) |

MSG-P2-018, MSG-P2-010, MSG-GEN-001, MSG-GEN-002, MSG-GEN-004, MSG-P7-003 and MSG-P4-002 are copied from legacy section 14 character for character; MSG-P7-010 and MSG-GEN-006 are named by FSD P7 A2.24 AC-EXC-P7-024-04 and by legacy section 12, and their texts are taken from Error and Message Standard v4 §4.

### 15. Screens and states

SCR-14 Treatment record, composed by gateway-bff (DP-19). The credit pack panel shows the level, the version and the status from `GET /approvals/{approvalId}`; the result form shows the NLEADS reference, the result, the level, the result date and the reason. On a refusal the reason is required and shown on the panel; on a level below the requirement the form shows MSG-P2-018 with both levels and does not submit. The panel moves WAITING → APPROVED → the entry link, or WAITING → REFUSED → the reason. The empty, loading, error and no access states are Not specified in the source documents (CG-ALL-7092). The pack sections, the documents and the input ages are rwb-integration's and are shown beside this panel, and the route move after the result is not a screen state of this service.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-006-01 | AC1, AC3; legacy AC1, BR6, BR9 | Component | Synthetic case with 2 accounts, 1 collateral and 5 checklist documents |
| TC-E2-006-02 | AC4; legacy AC2, BR2 | Component | Result APPROVED at level L5 |
| TC-E2-006-03 | AC5; legacy AC3, BR3 | Component | Result REFUSED with a reason |
| TC-E2-006-04 | AC3, document part: RWB-P2-E2006-APP; legacy AC4, BR6 | Component | No INCOME_PROOF document |
| TC-E2-006-05 | AC1, input age part: RWB-P2-E2006-APP; legacy AC5, BR7 | Component | Account load of 2026-12-12 |
| TC-E2-006-06 | AC5; legacy AC6 | Component | Empty reason; result date in the future |
| TC-E2-006-07 | AC6; legacy AC7, BR5 | Component | Level L6 for a plan that needs L5 |
| TC-E2-006-08 | AC7; legacy AC8 | Component | Result recorded twice |
| TC-E2-006-09 | AC6, case-state part: RWB-P3-E2006-APP; legacy AC9, BR1 | Component | Case in PLAN_RUNNING |
| TC-E2-006-10 | AC10; legacy AC10 | Component | Two results with If-Match version 3 |
| TC-E2-006-11 | AC8; legacy AC11, BR8 | NFR | Decision log store stopped during a result |
| TC-E2-006-12 | AC4, AC9, authority; legacy Access | Component | RW-PHONECOL calls a recording operation; refused with MSG-P4-002 |
| TC-E2-006-13 | AC8; legacy Principle 5 | NFR | Decision log write forced to fail; approval and entry unchanged; MSG-P7-003 |
| TC-E2-006-14 | §12 operations, events and activities | Contract | Recording and read operations against the fakes of 12.8 |
| TC-E2-006-15 | §12.7 tables; ASM-3438 | Boundary | Writes attempted to each table of 12.7 and to a table of another schema |
| TC-E2-006-16 | AC11; RWB-P2-E2006-APP | Component | Checklist document INCOME_PROOF not on the case |
| TC-E2-006-17 | AC12, case-state part: RWB-P3-E2006-APP | Component | Case in PLAN_RUNNING |
| TC-E2-006-18 | AC13 | Component | Treatment not a restructure; owning service refuses with MSG-P3-005; no call to this service |
| TC-E2-006-19 | AC14; BR4 | Boundary | Code of this story scanned for any call to NLEADS |
| TC-E2-006-20 | AC15; §12 operations | Contract | Call with no credential and call without the Decision log right against the recording and read operations |
| TC-E2-006-21 | AC16 | NFR | Record-result activity timed out before commit and retried with the same Idempotency-Key |

TC-E2-006-01 and TC-E2-006-02 are also carried at contract level for the two topics, and AC1, AC2, AC3 and AC9 run as contract tests against the fakes of 12.8. The cross-service copies of these test cases end in `-ITG` and belong to RWB-ITG-E2006-ITG.

### 17. Guardrails

- No business value in code: the levels, the regulation item, the versions and the final-call set are rows, LOVs or answers of the owning contract.
- No personal data in events, workflow inputs or logs: no name, account number, balance, address or refusal reason on `rwb.decision-record.v1` or `rwb.decision.events.v1`, and the reason is not written to application logs.
- ACE data only through the owner's contract or `v_ace_*` views, and this service reads neither.
- No read of another service's table, and no foreign key across a schema.
- The entry is written before the approval status changes, and the entry is append only.
- No call to NLEADS from any code, test or prompt.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-008 | Plan submitted for credit approval recorded on the case | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-RES-10, R-RES-11, R-RES-12, R-RES-14, R-UNI-39 | TC-E2-006-02, TC-E2-006-03, TC-E2-006-06 to TC-E2-006-11, TC-E2-006-13 |
| REQ-CHO-006 | Treatment holds type, terms, approval and outcome | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-006-01, TC-E2-006-04, TC-E2-006-05 |
| REQ-RDF-009 | A decision input carries its age and is refreshed before it is used | Program 5.3; Epic 2 3.2 | FEAT-CHO-07 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-006-01, TC-E2-006-05 |

### 19. Out of scope

- The pack: its assembly, the checklist, the input ages, the documents, `GET /treatments/{treatmentId}/credit-pack` and `POST /treatments/{treatmentId}/credit-result` are RWB-P2-E2006-APP on `rwb-integration`.
- The four treatment columns, the treatment state, the reason and the offer release are RWB-S2-E2006-APP on `rwb-treatment`.
- The route state moves, the case queue and R-RES-11, R-RES-12 and R-RES-14 are RWB-P3-E2006-APP on `rwb-case`.
- The routing, the approval queue, the escalation and `POST /approvals/{approvalId}/return` are RWB-P7-E2013-APP; the demand and recall approval screen is RWB-P7-E2014-APP.
- The load, the approval and the dating of the delegation files DOA-2026.11 and DOA-2027.01 are the authority service's, with the routing slice reading them (legacy RWB-E1-038).
- Booking the plan in NLEADS and ALS and its confirmation: RWB-E2-007 and Epic 3 (R-RES-21, R-RES-22); NLEADS itself is never called (INT-26).
- Approval inside the Workbench for decisions within the delegation: RWB-E2-013.
- The cross-service proof of the whole legacy key: RWB-ITG-E2006-ITG.
