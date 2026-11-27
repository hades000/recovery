# RWB-ITG-E6028-ITG Sell a post charge-off population

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6028-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-028 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | RWB-S7-E6028-APP, RWB-P7-E6028-APP (not built yet; the harness starts on the contract fakes) |
| Contract dependencies | None |
| Contract version | 5.0.0 (Recovery Workbench API Specification v5, info.version of rwb-writeoff, rwb-decision, rwb-case, rwb-debtsale, rwb-source-data and rwb-access) |
| Integration dependencies | RWB-S7-E6028-APP, RWB-P7-E6028-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-028 as the wave 4 integration proof that a post charge-off population is opened for sale with the approval the limit requires, that a pack above the write-off committee limit escalates to the credit approval committee through rwb-decision's approval, that a sale selection hands the population to the debt sale route with every case at SOLD_POST_CHARGEOFF, and that the decision record is written once with its rule version; the build of the sale is RWB-S7-E6028-APP and RWB-P7-E6028-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E6028-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (17 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **debt sale officer**, I want **the sale of a charged-off population proved end to end on the real services: the approval the limit requires read from rwb-decision's approval and recorded by rwb-writeoff, the population handed to the debt sale route as one lot with no case left behind at PLACEMENT_DECIDED, and one decision record per case with its rule version**, so that **no charged-off account is sold without the approval its amount needs and no case is reported as sold on a partial answer**.

This story builds the harness and the evidence, and nothing else. The sale decision, the states and the rule evaluation are RWB-S7-E6028-APP and RWB-P7-E6028-APP; the lot is S6 rwb-debtsale's debt sale route, reached on its own published lot operation, and the case with its timers is P3 rwb-case's. The decision record is P7 rwb-decision's library and ledger, written locally by the service that takes the action and confirmed centrally. The harness calls the published operations of S7, S6, P7, P3, P1 and P4, reads the case, the lot, DP09 Debt sale and the decision log, counts the events and writes one run report per population. The harness provides no endpoint, table, workflow, activity, schedule or screen, and it writes no code in any service.

### 2. Business rationale

A charged-off population is sold without the approval its amount needs, or a case is reported SOLD_POST_CHARGEOFF that no lot holds. Both failures are silent inside one service. The first is a limit that was never applied: R-WO-12 says that when the amount sits above the write-off committee limit the pack goes to the credit approval committee chaired by the product head with Risk, and the case moves to ESCALATED_TO_CREDIT_COMMITTEE — a population that skips that step is sold on an authority the committee never held. The second is a state that ran ahead of the route: R-WO-32 says that when the placement is a sale, the charged-off population is handed to the debt sale route and the case moves to SOLD_POST_CHARGEOFF, so a case at SOLD_POST_CHARGEOFF with no account in a lot is a case the bank cannot account for and a population the buyer cannot reconcile. R-WO-13 and R-WO-15 close the first gap from the other side: the final call, the approver and the limit applied are recorded, so the authority behind each sold account is readable after the fact. R-WO-29 sets the starting point — the post charge-off rule decides the treatment once the finance feed is accepted and leaves the case at PLACEMENT_DECIDED, which is the state the sale selects from. REQ-S7-006 asks for post charge-off treatment set by rule, including placement with an agency, and REQ-S6-001 asks that accounts eligible for sale are selected by rule against the policy cap; this harness proves the handover between the two requirements rather than restating either.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); there is no in-process call and no second hop on a caller's behalf. The write-off decision is S7's, the approval item and its level are P7's, the lot and its accounts are S6's, the case and its timers are P3's, the ACE-side product is P1's and the right is P4's. No table of another service is read (DP-01), ACE data is read only through P1's DP09 data-product contract (DP-05), and the decision record goes through the local library on `rwb.decision-record.v1` (DP-03, ADR-022). Where a screen would compose the approval, the case and the lot, the path is the gateway-bff composite route (DP-19); this run calls each owner's own operation at the service boundary and never a composite route of its own.

One limit is stated plainly because it shapes the run. The Ownership Map publishes no write-off read and no write-off sale operation. The population is therefore identified through the case read, the decision log and DP09 Debt sale read through rwb-source-data, and the handover is driven by the debt sale route's own published lot operation, not by an operation the harness invents. Where a state lives only on the write-off record it is asserted in RWB-S7-E6028-APP against S7's own reads, and this story asserts the boundary.

### 3. Preconditions

- The published contracts of S7 rwb-writeoff (the committee decision), P7 rwb-decision (the approval read, the approval decision and the decision log), P3 rwb-case (the case and its timers), S6 rwb-debtsale (the lot creation and the lot read), P1 rwb-source-data (DP09 records with the product's freshness stamp) and P4 rwb-access (the session) are in the contract registry, and a contract fake is generated from each one with its version pinned.
- RWB-S7-E6028-APP and RWB-P7-E6028-APP own the sale decision, the case states and the rule evaluation, including the limit test and the post charge-off placement decision; this story observes them and changes neither.
- The S6 fake stands in for the debt sale route until S6's own lot stories land; the lot it answers is a contract fake and is reported as one, never as a real lot.
- The rule package in force holds R-WO-12, R-WO-13, R-WO-15, R-WO-29, R-WO-31 and R-WO-32 with their rule version, so the decision entry the run reads names a rule that is still the one in force.
- rwb-writeoff runs `WriteOffWorkflow` on task queue `rwb-writeoff` with its committee, posting and post charge-off steps, and holds the JOB-16 write-off scan Schedule on the 3rd working day (Arch v5 slides 20 and 44; Temporal design slide 23); this story reads both and starts neither.
- The approval item and its level are P7's and are read through P7's approval contract; the harness asserts the level the approval carries and reads no delegation table of any service (DP-01).
- The synthetic population, the three cases `RW-2027-000728` to `RW-2027-000730`, their write-offs `WO-SYN-000728` to `WO-SYN-000730`, the cut-off month 2027-04, the business date 2027-04-30, the two inside-limit amounts, the one above-limit amount and the write-off committee limit itself are `Not specified in the source documents (GAP-0458; ASM-0650)`, and are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the contract fakes in place from the first run; the two waits are RWB-S7-E6028-APP and RWB-P7-E6028-APP, which replace their fakes and never block the lane (Template and Rules §R5.4, §R5.7).

### 4. Flow

1. Harness: runs preflight. It reads the six contracts, pins each version in the run report, loads the population fixture and the P7 approval fixture, and stops the run before any assertion if a contract is missing or a pinned version has moved (X1).
2. Harness: loads the fixture: the population of three synthetic cases `RW-2027-000728` to `RW-2027-000730`, their write-offs `WO-SYN-000728` to `WO-SYN-000730`, cut-off month 2027-04, business date 2027-04-30, two amounts inside the write-off committee limit and one above it, and the limit itself as a fixture value.
3. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` for each case and names its status, stage and `rule_version` as the baseline, asserts every case is at PLACEMENT_DECIDED, and asserts that no lot exists for the population and that no case has left PLACEMENT_DECIDED (AC1, AC2).
4. Harness: takes the committee decision on the above-limit write-off with `POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` as a RW-CREDITAD session holding Write-off and posting A, reads `GET /api/recovery/decision/v1/approvals`, and asserts one approval item for the credit approval committee chaired by the product head with Risk, carrying the limit applied and the amount (R-WO-12). The case reads ESCALATED_TO_CREDIT_COMMITTEE (AC2).
5. Harness: approves the item with `POST /api/recovery/decision/v1/approvals/{approvalId}/approve` as a RW-PRODHEAD session, and asserts the answer is an approval, that the decision log holds the final call, the approver and the limit applied (R-WO-13, R-WO-15), that the case now reads APPROVED, and that exactly one decision entry was appended for the action (AC2, AC4).
6. Harness: takes the committee decision on the two inside-limit write-offs and asserts each routes to the write-off committee under R-WO-11 and is approved under R-WO-15, so the whole population of three is approved before the sale is opened (AC2).
7. Harness: opens the sale of the approved population with `POST /api/recovery/debtsale/v1/debt-sale-lots` under one Idempotency-Key for cut-off month 2027-04, and reads `GET /api/recovery/debtsale/v1/debt-sale-lots/{lotId}`: one lot holds the three accounts of the population, with its lot number, cut-off date, status and the accounts it carries (AC1, AC3).
8. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` for each case and asserts SOLD_POST_CHARGEOFF on all three (R-WO-32), that no case is left at PLACEMENT_DECIDED, and that the state change is stamped inside business date 2027-04-30 (AC1, AC3).
9. Harness: replays the same lot creation with the same Idempotency-Key, reads the lot again and asserts one lot, the same three accounts and no second account row; a second lot or a second account fails the run (X4, AC3).
10. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP09/records?caseId={caseId}` for each case and asserts the account is in the lot the debt sale route built, with the product's freshness stamp carrying the business date (AC1).
11. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` for each case and asserts one entry per action, each with its rule id and rule version and each naming the same lot and the same write-off; then watches `rwb.decision-record.v1` and `rwb.case.events.v1` and asserts one `DecisionRecorded` per action and one `CaseStateChanged` per state change (AC4).
12. Harness: resets the fixture to the pre-approval snapshot, forces the decision-record hop to fail, opens the sale again under a new Idempotency-Key, and asserts the answer carries MSG-P7-003 with no lot, no account row, no state change and no decision entry (AC5).
13. Harness: calls the committee decision as a synthetic RW-OFF caller with no Write-off and posting A and asserts 403 with MSG-P4-002 and no decision entry for the write-off (AC6); then writes one run report per population and cut-off month, keyed by story and month, naming the contract version of each hop, whether the hop was a fake or the owner, the approval item with the limit applied, the lot and its accounts, the three case states, the decision entries with their rule versions, both event counts and the six criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A contract fake or a real owner answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-028-01-ITG (AC1) | AC1 |
| X2 | A case of the population reads SOLD_POST_CHARGEOFF before its write-off is approved | The run fails on AC2 and the report names the case, its write-off, the approval item and the state read, because a sale before the approval is the failure R-WO-12 exists for | None | TC-E6-028-02-ITG (AC2) | AC2 |
| X3 | The approval item carries no limit applied, or the case approves without one | The run fails on AC2 and the report names the approval item, the amount, the limit the fixture holds and what the decision entry recorded (R-WO-13, R-WO-15) | None | TC-E6-028-02-ITG (AC2) | AC2 |
| X4 | The replay of the lot creation produces a second lot or a second account row | The run fails on AC3 and the report names both lots, both Idempotency-Keys and the account rows each created | None | TC-E6-028-03-ITG (AC3) | AC3 |
| X5 | The decision record is written twice for one action, written without its rule version, or not confirmed centrally | The run fails on AC4 and the report names the entries, their rule versions and the missing confirmation on `rwb.decision-record.v1` | None | TC-E6-028-06-ITG (AC4) | AC4 |
| X6 | The decision record is forced to fail on the sale selection | The answer carries MSG-P7-003, no lot exists, no case moved to SOLD_POST_CHARGEOFF and the decision log holds no entry for the action; a 200 or a created lot fails the run | MSG-P7-003 | TC-E6-028-04-ITG (AC5) | AC5 |
| X7 | A caller without Write-off and posting A takes the committee decision | The answer is 403 with MSG-P4-002, no decision entry exists and no case changed state | MSG-P4-002 | TC-E6-028-05-ITG (AC6) | AC6 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and their fakes from Day 1; the only waits are RWB-S7-E6028-APP and RWB-P7-E6028-APP, and their fakes answer until they land |
| Negotiable | The fixture layout, the three synthetic cases, the amounts and the limit, the business date, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | Proves across services that no account is sold without the approval its amount needs, that the sale hands the population over once, and that no case is reported sold on a partial answer |
| Estimable | One runner, one fixture, one committee driver, one approval probe, one sale driver, one lot probe, one product read-back, one decision probe, one event probe, one access probe and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion is asserted on an observable: an approval item with its limit, a case state, a lot with its accounts, a DP09 record, a decision entry with its rule version, an event count and a response code |

### 7. Acceptance criteria

```gherkin
Feature: Sell a post charge-off population - wave 4 sale harness

  Background:
    Given the environment is SIT with synthetic data
    Given the population of cut-off month "2027-04" holds the cases "RW-2027-000728" to "RW-2027-000730" with the write-offs "WO-SYN-000728" to "WO-SYN-000730"
    Given two of the three amounts sit inside the write-off committee limit and one sits above it
    Given every case of the population is at PLACEMENT_DECIDED on business date "2027-04-30"
    Given the rule package in force holds R-WO-12, R-WO-13, R-WO-15, R-WO-29, R-WO-31 and R-WO-32

  Scenario: AC1 The approved population reaches the sale route with one decision record per case (new, D-RCV-60)
    Given the three write-offs of the population are approved inside their delegation
    When POST "/api/recovery/debtsale/v1/debt-sale-lots" is called once for the population with one Idempotency-Key
    Then GET "/api/recovery/debtsale/v1/debt-sale-lots/{lotId}" holds the three accounts of the population
    And GET "/api/recovery/case/v1/cases/{caseId}" answers SOLD_POST_CHARGEOFF for every case of the population under R-WO-32
    And GET "/api/recovery/decision/v1/decision-log?caseId={caseId}" holds one entry per action with its rule id and rule version
    And no case of the population is left at PLACEMENT_DECIDED

  Scenario: AC2 A pack above the write-off committee limit escalates to the credit approval committee (new, D-RCV-60)
    Given the write-off "WO-SYN-000730" sits above the write-off committee limit
    When POST "/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision" records the decision on that write-off
    Then GET "/api/recovery/decision/v1/approvals" answers one approval item for the credit approval committee chaired by the product head with Risk under R-WO-12
    And the case answers ESCALATED_TO_CREDIT_COMMITTEE
    When POST "/api/recovery/decision/v1/approvals/{approvalId}/approve" approves the item with the limit applied
    Then the case answers APPROVED and the decision record read holds the final call, the approver and the limit applied under R-WO-13 and R-WO-15
    And no lot exists for the population

  Scenario: AC3 A sale selection hands the population to the debt sale route once (new, D-RCV-60)
    Given the approved population of "2027-04" is held at PLACEMENT_DECIDED
    When POST "/api/recovery/debtsale/v1/debt-sale-lots" is called with one Idempotency-Key
    Then one lot holds the three accounts of the population with the cut-off date of the month
    And every case of the population reads SOLD_POST_CHARGEOFF
    When the same call is replayed with the same Idempotency-Key
    Then one lot exists and no second account row is added
    And GET "/api/recovery/source-data/v1/data-products/DP09/records?caseId={caseId}" shows each account in the lot the route built

  Scenario: AC4 The decision record is written once per action with its rule version (new, D-RCV-60)
    Given the committee decisions, the approval and the sale selection of the run are complete
    When GET "/api/recovery/decision/v1/decision-log?caseId={caseId}" is read for each case
    Then one entry exists per action with its rule_id and its rule_version
    And rwb.decision.DecisionRecorded.v1 is published once per action on rwb.decision-record.v1
    And rwb.case.CaseStateChanged.v1 is published once per state change on rwb.case.events.v1
    And a re-read of the log adds no second entry

  Scenario: AC5 A forced decision-record failure stops the sale with nothing handed over (new, D-RCV-60)
    Given the local decision record cannot be written on the sale selection
    When POST "/api/recovery/debtsale/v1/debt-sale-lots" is called for the approved population
    Then the answer carries "MSG-P7-003"
    And no lot is created and no case moves to SOLD_POST_CHARGEOFF
    And the decision record read holds no entry for the sale selection

  Scenario: AC6 A caller without Write-off and posting A is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Write-off and posting A
    When the caller calls POST "/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision"
    Then the answer is 403 with "MSG-P4-002"
    And no decision is recorded for the write-off and no case changes state

  Scenario: AC7 A pack inside the write-off committee limit is routed to the write-off committee (new, D-RCV-60)
    Given the write-off "WO-SYN-000728" sits inside the write-off committee limit
    Then GET "/api/recovery/decision/v1/decision-log?caseId={caseId}" holds the routing to the write-off committee under R-WO-11
    And the meeting of the write-off committee is scheduled for "WO-SYN-000728"
    And GET "/api/recovery/decision/v1/approvals" holds no approval item for "WO-SYN-000728"

  Scenario: AC8 A placement held for want of agency capacity stays at PLACEMENT_DECIDED and is not sold (new, D-RCV-60)
    Given one case of the population is held for want of agency capacity
    Then GET "/api/recovery/case/v1/cases/{caseId}" answers PLACEMENT_DECIDED for that case
    And that case is in no lot of GET "/api/recovery/debtsale/v1/debt-sale-lots/{lotId}"
    And that case is never reported SOLD_POST_CHARGEOFF

  Scenario: AC9 Every call answers within its 2 s budget on the owner's base path (new, D-RCV-60)
    Given each call of AC1 to AC8 is made once by the harness
    Then each answer arrives within 2 s
    And each call is one hop on the owner's base path "/api/recovery/<short>/v1" with no call made on another service's behalf

  Scenario: AC10 A retried or timed-out activity does not repeat the sale or the decision record (new, D-RCV-60)
    Given the sale selection of the approved population has been called with one Idempotency-Key
    When the activity of DebtSaleWorkflow that writes the lot times out and is retried
    Then one lot exists and no second account row is added
    And each decision record of the run is written once, with its rule id and rule version

  Scenario: AC11 A consumed call that fails or does not answer leaves no lot and no case moved (new, D-RCV-60)
    Given a consumed call of the sale selection fails or does not answer
    When POST "/api/recovery/debtsale/v1/debt-sale-lots" is called for the approved population
    Then no lot is created and the error code and message of the answer are Not specified in the source documents (NEWAC-RWB-ITG-E6028-ITG-AC9)
    And no case of the population moves to SOLD_POST_CHARGEOFF
    And the decision record read holds no entry for the sale selection
```

Legacy AC1 to AC4 stay with RWB-S7-E6028-APP as its build criteria: the sale decision, the escalation state, the sale-selected state and the decision-log write are S7's own behaviour, asserted there against S7's own reads. Legacy AC4, the not-recorded path, is asserted here too, but across the boundary in AC5: what this run proves is that a failed record leaves no lot, no account row and no case state behind on the debt sale side. Every criterion in this section is new work of this harness and none of them is a copy.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A pack whose amount sits inside the write-off committee limit is routed to the write-off committee and the meeting is scheduled; the limit test is the rule's, not the harness's | R-WO-11 |
| BR2 | A pack whose amount sits above the write-off committee limit is routed to the credit approval committee chaired by the product head with Risk, and the case moves to ESCALATED_TO_CREDIT_COMMITTEE | R-WO-12 |
| BR3 | An approval records the final call, the approver and the limit applied, and releases the case; the record is what makes the authority behind a sold account readable afterwards | R-WO-13; R-WO-15 |
| BR4 | The post charge-off treatment is decided by rule once the finance feed is accepted: the write-off posts, the feed is sent and the placement decision leaves the case at PLACEMENT_DECIDED, which is the only state the sale selects from | R-WO-20; R-WO-29 |
| BR5 | A placement held for want of agency capacity stays at PLACEMENT_DECIDED and escalates on its timer; a case still at PLACEMENT_DECIDED is not sold and is never reported sold | R-WO-31 |
| BR6 | A sale selection hands the charged-off population to the debt sale route and moves the case to SOLD_POST_CHARGEOFF; the handover is one lot for the population and one account row per case | R-WO-32 |
| BR7 | Post charge-off treatment is set by rule, and the sale population is selected by rule against the policy cap; the two rules meet at the handover this run proves | REQ-S7-006; REQ-S6-001 |
| BR8 | Every action writes its decision record once, with its rule id and rule version, through the local decision-record library on `rwb.decision-record.v1`, and the record is confirmed centrally; an action whose record cannot be written does not happen | DP-03; ADR-022 |
| BR9 | No service reads another service's tables, and ACE data is read only through rwb-source-data's data-product contract; DP09 is the product that carries the sold account | DP-01; DP-05 |
| BR10 | Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget, and no service calls another on the caller's behalf | DP-11; DP-13 |

Coverage of these rules in section 7: BR1 AC7; BR2 and BR3 AC2; BR4 and BR5 AC8; BR6 and BR7 AC1 and AC3; BR8 AC4 and AC5; BR9 AC3; BR10 AC9.

The harness asserts these rules and changes none of them.

### 9. State transitions

| From | Event | Condition | To | Owner |
|---|---|---|---|---|
| `PACK_PREPARED` | `PACK_ROUTED` | amount inside the write-off committee limit | `WITH_COMMITTEE` | S7 rwb-writeoff (R-WO-11) |
| `PACK_PREPARED` | `LIMIT_EXCEEDED` | amount above the write-off committee limit | `ESCALATED_TO_CREDIT_COMMITTEE` | S7 rwb-writeoff (R-WO-12) |
| `ESCALATED_TO_CREDIT_COMMITTEE` | `CREDIT_COMMITTEE_APPROVED` | approved inside the delegation with Risk | `APPROVED` | S7 rwb-writeoff (R-WO-13) |
| `WITH_COMMITTEE` | `COMMITTEE_APPROVED` | approved inside the delegation | `APPROVED` | S7 rwb-writeoff (R-WO-15) |
| `FINANCE_FEED_SENT` | `POST_CHARGEOFF_RULE_RUN` | finance_feed_status = accepted | `PLACEMENT_DECIDED` | S7 rwb-writeoff (R-WO-29) |
| `PLACEMENT_DECIDED` | `NO_AGENCY_CAPACITY` | no agency on the panel has capacity | `PLACEMENT_DECIDED` | S7 rwb-writeoff (R-WO-31) |
| `PLACEMENT_DECIDED` | `SALE_SELECTED` | placement_type = sale | `SOLD_POST_CHARGEOFF` | S7 rwb-writeoff (R-WO-32) |

The harness changes no state. Every change in the table is made by S7 rwb-writeoff, and the harness reads the result through P3 rwb-case, whose case read carries the status, the stage and the rule version the state was entered under. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts. The lot and its accounts are S6's and are read on S6's published lot operation; `PLACEMENT_RECALLED` (R-WO-34) and the agency placement (R-WO-30) are S7's own paths and are not exercised here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD Credit Administration officer | Takes the committee decision that starts the approval (Write-off and posting A); reads the approval item and the case state |
| RW-WOCOMM Write-off committee member | Holds Write-off and posting A; is the committee the inside-limit packs route to under R-WO-11 |
| RW-PRODHEAD Product head | Chairs the credit approval committee with Risk and approves the above-limit item through P7's approval operation; the limit applied is carried on the approval and recorded in the decision log |
| RW-DEBTSALE Debt sale officer | Holds the sale role: opens the sale of the approved population on the debt sale route and reads the lot |
| RW-SALEOFF Sale officer | Reads the lot and the population; holds no committee right |
| RW-OFF Case officer | The synthetic caller of AC6; holds no Write-off and posting A and is refused |
| RW-TRIBE, RW-PLATADM | Read the run report and the evidence; the platform administrator holds the environment |
| QA lead | Owns the harness configuration, the population fixture, the approval fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the fake set and the swap from a fake to the real service |
| The owning services' identities | S7 takes the decision and publishes its outcome (which service moves the case state is an open question with the P3 owner, GAP-1800), P7 holds the approval item and the ledger, S6 builds the lot and its accounts, P3 holds the case and its timers, P1 serves DP09, P4 answers the right; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision and grants no right: the committee decision is recorded by the caller, the approval item and its level are P7's, and the harness only asserts what the services answer |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 to DF-FIN-020 | `write_off` (rwb_writeoff) | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product, recovered_after | Read as the decision and the state through the case, the decision log and the lot; written by S7 |
| DF-FIN-011 | `write_off` | case_id | Read (the link between the write-off and the case the run reads) |
| DF-FIN-013 | `write_off` | amount | Read (the value the limit test is applied to; compared with the approval item) |
| DF-FIN-015 | `write_off` | committee_date | Read (the approval the sale derives from) |
| DF-SAL-020 to DF-SAL-030 | `debt_sale_lot` (rwb_debtsale) | id, lot_no, cut_off_date, segment, reserve_price, buyer_partner_id, buyer_class, signing_date, approval_authority, payment_terms, status | Read through the S6 lot read; written by S6 |
| DF-SAL-022 | `debt_sale_lot` | cut_off_date | Read (asserted as 2027-04, the cut-off month of the population) |
| DF-SAL-028 | `debt_sale_lot` | approval_authority | Read (the authority the lot carries, where the lot read returns it) |
| DF-SAL-030 | `debt_sale_lot` | status | Read (the lot's own status at creation and after the replay) |
| DF-SAL-031 to DF-SAL-037 | `debt_sale_account` (rwb_debtsale) | id, lot_id, account_key, borrower_code, outstanding, selling_price, put_back_status | Read through the S6 lot read; written by S6 |
| DF-SAL-033 | `debt_sale_account` | account_key | Read (each account of the population matched to a case) |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` (rwb_case) | case_no, status, stage_code, route_state, owner_user_id, rule_version and 17 more | Read through the rwb-case contract |
| DF-CAS-006, DF-CAS-007 | `recovery_case` | stage_code, route_state | Read (the value the harness asserts for PLACEMENT_DECIDED, ESCALATED_TO_CREDIT_COMMITTEE, APPROVED and SOLD_POST_CHARGEOFF) |
| DF-CAS-021 | `recovery_case` | rule_version | Read (the rule version the state was entered under, compared with the decision entry) |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (rwb_decision) | id, case_id, decision_code, rule_id, rule_version, final_call, approver_user_id, approval_level, actions, entry_hash and 8 more | Read through the rwb-decision decision-log contract |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Read (one entry per action, with the rule that fired and its version) |
| DF-DEC-010, DF-DEC-011 | `decision_log_entry` | approver_user_id, approval_level | Read (the approver and the level applied, on the approval entry) |
| DF-DEC-012 | `decision_log_entry` | final_call | Read (the option decided, on the approval entry) |
| DF-REF-001 to DF-REF-015 | `rule_row` (rwb_decision) | id, rule_id, rule_version, route_set, from_state, event_code and 9 more | Asserted from the decision entry (DF-DEC-004, DF-DEC-005); the rule catalogue is P7's and is not read directly here |

Field IDs are those in the Logical Data Model and Data Dictionary v9. Reference data: the write-off committee limit is read as a parameter on the approval item, and the rule catalogue is read through the decision entry; both come through the reference-data contracts DP-06 and DP-07. The write-off table is S7's, the one table the Ownership Map holds (its four entity groups are eligibility, committee decision, posting and recovery after charge-off, with key fields Not specified in the source documents (GAP-1794)), the lot and its accounts are S6's, the case is P3's, the ledger and the rule catalogue are P7's. The harness owns no table and writes no row: it asserts the write-off facts where the contracted reads carry them, the lot and its accounts on S6's lot read, and the decision record on P7's log read and on `rwb.decision-record.v1`.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use and the ACs it serves |
|---|---|---|---|
| POST | `/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` | S7 rwb-writeoff | Records the committee decision that starts the approval, inside the limit and above it (AC2, AC6) |
| GET | `/api/recovery/decision/v1/approvals` | P7 rwb-decision | The one approval item for the credit approval committee with the limit applied (AC2) |
| POST | `/api/recovery/decision/v1/approvals/{approvalId}/approve` | P7 rwb-decision | Approves the item and appends the final call, the approver and the limit applied (AC2, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The baseline and the state: PLACEMENT_DECIDED, ESCALATED_TO_CREDIT_COMMITTEE, APPROVED, SOLD_POST_CHARGEOFF (AC1, AC2, AC3, AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The placement timer that holds a case at PLACEMENT_DECIDED under R-WO-31 (AC2, AC3) |
| POST | `/api/recovery/debtsale/v1/debt-sale-lots` | S6 rwb-debtsale | Opens the sale of the approved population as one lot, with one Idempotency-Key (AC1, AC3, AC5) |
| GET | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}` | S6 rwb-debtsale | The lot and the accounts it holds, after the creation and after the replay (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP09/records?caseId={caseId}` | P1 rwb-source-data | DP09 Debt sale read back through the data-product contract, with the product's freshness stamp (AC1) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | One entry per action with its rule id, its rule version and the lot it names (AC1, AC4, AC5, AC6) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's role and rights for the committee decision (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-13, ADR-020). The ten paths are the owners' published operations and none is invented here. The Ownership Map publishes no read of a write-off record and no write-off sale operation, so the population is identified through the case read, DP09 and the decision log, and the handover is driven by the debt sale route's own published lot operation: the harness never calls a write-off sale path, because there is none to call. Where a screen would compose the approval item, the case and the lot, the path would be the gateway-bff composite route (DP-19); this run calls each owner's own operation instead.

#### 12.3 Events published

None. The harness publishes no Kafka event. `DecisionRecorded` is produced by each service's outbox and `CaseStateChanged` by rwb-case's, and both are asserted in 12.4; the harness writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by every service, rwb-writeoff and rwb-debtsale included; consumed by P7 rwb-decision and P9 rwb-reporting | CloudEvents 1.0 binary mode, key caseId, exactly one event per local append; the entry's rule version is what makes the action reproducible |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | Produced by P3 rwb-case; consumed by P6 rwb-comms and P9 rwb-reporting | Exactly one event per state change; the harness counts one per case transition of the run and asserts a redelivery adds no effect |

The two events are asserted on the topic, not read from a table: the harness counts them per case and per action, and a redelivery is a pass only when the consumer's inbox absorbs it. `LotAwarded` (Arch v5 slide 43, row 23) is S6's award step and is not in this story, which stops at the lot and its accounts.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow | `rwb-writeoff` | The committee step, the posting step and the post charge-off placement decision (R-WO-12/13/15, R-WO-20 to R-WO-32) |
| `ApprovalWorkflow` | Workflow | `rwb-decision` | The approval item, its level and its final call (R-WO-13, R-WO-15) |
| `DebtSaleWorkflow` | Workflow (saga, pivot = transfer) | `rwb-debtsale` | The lot, its accounts and the step the sale selection starts (Arch v5 line 1399) |

The three workflows are observed only. Each is registered by its own service's worker and its steps are that service's; this story starts none of them by hand and asserts their effect through the case read, the approval read, the lot read and the decision log. The hand-over from the write-off route to the debt sale route (R-WO-32, BR6) has no S7 cell and no S6 cell in the connection matrix: the population, the route and the approval are recorded here as product behaviour, and the call type and direction are an open question with the S6 owner before the wave 4 system test. The platform contracts RWB-PLT-E1027-CON and RWB-PLT-N001-CON and the consumed contracts of P3 and P4 are carried in the Dependency Map as non-blocking contracts (GAP-1312); the metadata rows stay as the plan gives them.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| JOB-16 write-off scan in rwb-writeoff | Monthly, 3rd working day, overlap policy SKIP with a catch-up window | Registered by the rwb-writeoff release; read by the harness and never changed or triggered by it in this story | JOB-16 Write-off scan |

JOB-16 is a Temporal Schedule in rwb-writeoff (Arch v5 slide 44; Temporal design slide 23), not a shared Quartz row; the scan and its population are RWB-E6-013's and this story neither runs them nor asserts them.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). The write-off is S7's, the approval, the decision log and the rule rows are P7's, the lot and its accounts are S6's, the case is P3's and DP09 is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Fake for rwb-writeoff | The committee decision of §12.2 | Records the decision for each synthetic write-off once per Idempotency-Key, answers ESCALATED_TO_CREDIT_COMMITTEE above the limit and WITH_COMMITTEE inside it, and refuses a caller without Write-off and posting A with 403 and MSG-P4-002 |
| Fake for rwb-decision | `GET /approvals`, `POST /approvals/{approvalId}/approve`, `GET /decision-log`, and the `DecisionRecorded` event | One approval item for the credit approval committee carrying the limit applied, an approval that appends one entry with its rule id, rule version, approver and level, and an empty log for a refused or failed action |
| Fake for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers` | The three cases with their status, stage, rule version and placement timer, and the SOLD_POST_CHARGEOFF, APPROVED, ESCALATED_TO_CREDIT_COMMITTEE and PLACEMENT_DECIDED states |
| Fake for rwb-debtsale | `POST /debt-sale-lots`, `GET /debt-sale-lots/{lotId}` | One lot for the population with its lot number, cut-off date and status, three account rows for the three cases, and an idempotent answer to a replay that adds no second lot and no second row |
| Fake for rwb-source-data | DP09 records and the freshness stamp of the product | The DP09 record per case with the lot and account the route built, and the product's business date and load time |
| Fake for rwb-access | `GET /me/session` | A RW-CREDITAD session holding Write-off and posting A, a RW-PRODHEAD session holding the approval right, a RW-DEBTSALE session holding the sale right, and a RW-OFF session holding none |
| Population fixture independent of ALS and the general ledger | The synthetic population and the amounts of the cut-off month | The three cases and their write-offs, the two inside-limit amounts, the one above-limit amount and the write-off committee limit as data, with a fault switch on the decision-record hop for AC5 |

Each fake is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment, the base hosts, the fixture layout, the amounts and the limit, the business date, the evidence format and retention, and the pass or fail gate are `Not specified in the source documents (GAP-0458; ASM-0650)`.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13, ADR-020) |
| Kafka | None published; 2 event types consumed — `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and `rwb.case.CaseStateChanged.v1` on `rwb.case.events.v1` — with inbox dedupe at rwb-decision and at the reporting consumer |
| Temporal | None added; `WriteOffWorkflow` on `rwb-writeoff`, `ApprovalWorkflow` on `rwb-decision` and `DebtSaleWorkflow` on `rwb-debtsale` are observed |
| File | None. The population, the approval and the lot answers are fixtures and contract fakes, not files |

### 13. Solution plan

**Package.** Folder `itg/recovery-w4/post-chargeoff-sale`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON from DP-03 and RWB-PLT-N001-CON from DP-19) are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays empty. The blocking dependencies are the two I stories, RWB-S7-E6028-APP and RWB-P7-E6028-APP, which replace their fakes; until they are live the run uses the fakes, and a fake pass is reported as a fake pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for a population and a cut-off month, and holds the run lock |
| PopulationFixture | Fixture | The three synthetic cases and their write-offs, the two inside-limit and one above-limit amounts, the write-off committee limit, the cut-off month and the business date, plus the fault switch of AC5 |
| CommitteeDriver | Service | Takes the committee decision on the above-limit write-off and on the two inside-limit write-offs, and reads the resulting approval item |
| ApprovalProbe | Service | Approves the item through P7 and asserts the final call, the approver, the limit applied and the one decision entry |
| SaleDriver | Service | Opens the sale as one lot under one Idempotency-Key and replays the same call |
| LotProbe | Service | Reads the lot and its accounts after the creation and after the replay, and fails on a second lot or a second account |
| ProductReadBack | Service | Reads DP09 through P1 for each case and asserts the account is in the lot the route built |
| DecisionProbe | Service | Reads the decision log per case and asserts one entry per action with its rule id, its rule version and the lot it names |
| EventProbe | Service | Counts `DecisionRecorded` on `rwb.decision-record.v1` and `CaseStateChanged` on `rwb.case.events.v1`, and asserts a redelivery adds no effect |
| AccessProbe | Service | Calls the committee decision as RW-OFF and asserts 403 with MSG-P4-002 and no decision entry |
| EvidenceReport | Service | Writes one report per population and cut-off month keyed by story, and holds the pass or fail gate |

**Environment and synthetic data.** SIT, against the contract fakes from Day 1 and the real services as RWB-S7-E6028-APP and RWB-P7-E6028-APP land, on the synthetic cases `RW-2027-000728` to `RW-2027-000730`, their write-offs `WO-SYN-000728` to `WO-SYN-000730`, cut-off month 2027-04 and business date 2027-04-30, with two amounts inside the write-off committee limit and one above it. The S6 hop stays a contract fake and is reported as a fake hop until the S6 lot stories land, and the whole run is independent of ALS and the general ledger. The harness environment, the base hosts, the amounts and the limit, the evidence format and the gate are `Not specified in the source documents (GAP-0458; ASM-0650)`.

**Build steps**

1. Generate the six contract fakes, load the population fixture and the approval fixture, pin every contract version in the run report and fail the run on a mismatch (X1, AC1).
2. Build the CommitteeDriver for AC2: take the decision on the above-limit write-off, read the approval item and assert the credit approval committee chaired by the product head with Risk, with the limit applied and the case at ESCALATED_TO_CREDIT_COMMITTEE (X2).
3. Add the ApprovalProbe for AC2 and AC4: approve through P7, assert the final call, the approver, the limit applied, the APPROVED state and one decision entry (X3).
4. Add the inside-limit path of AC2: the two inside-limit write-offs route to the write-off committee under R-WO-11 and are approved under R-WO-15, and the baseline of step 3 confirms no lot and no case left at PLACEMENT_DECIDED before the sale.
5. Add the SaleDriver and the LotProbe for AC1 and AC3: open the lot with one Idempotency-Key, assert the three accounts, replay, and assert one lot and no second account row (X4).
6. Add the case read for AC3: every case of the population reads SOLD_POST_CHARGEOFF inside business date 2027-04-30 and none is left at PLACEMENT_DECIDED; a case at SOLD_POST_CHARGEOFF that the lot does not hold fails the run.
7. Add the ProductReadBack for AC1: read DP09 per case through P1's contract and assert the account is in the lot the route built.
8. Add the DecisionProbe and the EventProbe for AC4: one entry per action with its rule id and rule version, one `DecisionRecorded` per action and one `CaseStateChanged` per state change, and no second entry on a re-read (X5).
9. Add the forced failure of AC5 with MSG-P7-003 and nothing handed over (X6), the AccessProbe of AC6 (X7), then the EvidenceReport and the gate, swapping a fake for the real owner as each I story lands.

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The six tests of section 16 pass against the fakes and again against the real services when RWB-S7-E6028-APP and RWB-P7-E6028-APP land, the above-limit write-off carries the approval item of the credit approval committee with the limit applied, one lot holds all three accounts read back through DP09, every case of the population reads SOLD_POST_CHARGEOFF with none left at PLACEMENT_DECIDED, and the wave entry check holds a run report keyed by story and cut-off month.

### 14. Validation and messages

| ID | Type | Message | Where the run asserts it |
|---|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. | The scan is on hold, so no population reaches PLACEMENT_DECIDED and the harness fails the run before any sale assertion |
| MSG-GEN-001 | Error | Enter {field}. | The committee decision called without its decision field answers with the field named in place of {field} |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | The RW-OFF caller on the committee decision, with the action named in place of {action} |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The forced decision-record failure of AC5, with nothing handed over |

The four texts are copied unchanged from RWB-E6-028; the story adds no message text. The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

This story builds no screen. SCR-27 Write-off proposal is the legacy screen of RWB-E6-028 and is not built here; it belongs to S7 and its states are read through the case contract and the decision log, not from a screen.

| State | What the run asserts | Through which read |
|---|---|---|
| `PLACEMENT_DECIDED` | The baseline of every case before the sale, with the placement timer running; no case is left here after the sale | `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/timers` |
| `ESCALATED_TO_CREDIT_COMMITTEE` | The above-limit case carries the escalation and one approval item for the credit approval committee with the limit applied (R-WO-12) | The case read and `GET /api/recovery/decision/v1/approvals` |
| `APPROVED` | The final call, the approver and the limit applied are recorded and the case is approved (R-WO-13, R-WO-15) | The case read and `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` |
| `SOLD_POST_CHARGEOFF` | Every case of the population is sold, each account is in the lot, and the decision entry names the same lot (R-WO-32) | The case read, `GET /api/recovery/debtsale/v1/debt-sale-lots/{lotId}` and DP09 |
| A refused or failed action | No lot, no account row, no state change and no decision entry; the answer carries MSG-P4-002 or MSG-P7-003 | The case read, the lot read and the decision log, read before and after the call |
| Empty | Screen state of SCR-27, not asserted by this run: a plain sentence saying there is nothing to show, and the action to take if one applies | None; Screen Inventory and Navigation v2, common states |
| Loading | Screen state of SCR-27, not asserted by this run: skeleton rows while data arrives, with no spinner over the whole page | None; Screen Inventory and Navigation v2, common states |
| Error | Screen state of SCR-27, not asserted by this run: the message from the error and message standard next to the field or at the top | None; Screen Inventory and Navigation v2, common states |
| No access | Screen state of SCR-27, not asserted by this run: Write-off and posting access is checked on every request, and an action outside the role's permission shows MSG-P4-002 | None; Screen Specifications v1, SCR-27 |

What the wave entry check looks at instead of a screen is the run report, whose environment, layout and retention are `Not specified in the source documents (GAP-0458; ASM-0650)` until agreed at the wave 4 entry check and held as configuration. The write-off read and the write-off sale operation do not exist: the population is asserted through the case read, the decision-log read and DP09, and the handover is driven by S6's published lot operation.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-028-01-ITG | ITG AC1, ITG AC3 | End to end | The whole journey on the population of three synthetic cases, from the approvals to the lot and the three sold cases |
| TC-E6-028-02-ITG | ITG AC2 | Integration | The above-limit write-off `WO-SYN-000730`, the credit approval committee item and the limit applied |
| TC-E6-028-03-ITG | ITG AC3 | Integration | One lot creation and one replay with the same Idempotency-Key over the three accounts |
| TC-E6-028-04-ITG | ITG AC5 | Integration | The not-recorded path forced on the sale selection, with MSG-P7-003 |
| TC-E6-028-05-ITG | ITG AC6 | Component | A RW-OFF caller holding no Write-off and posting A |
| TC-E6-028-06-ITG | ITG AC4 | Integration | The decision record with its rule version, the central confirmation and the one entry per action |
| TC-E6-028-07-ITG | ITG AC7 | Integration | One pack inside the write-off committee limit, `WO-SYN-000728`, routed to the write-off committee |
| TC-E6-028-08-ITG | ITG AC8 | Integration | One case held for want of agency capacity at PLACEMENT_DECIDED, outside any lot |
| TC-E6-028-09-ITG | ITG AC9 | Component | Each call of AC1 to AC8, timed against the 2 s budget on the owner's base path |
| TC-E6-028-10-ITG | §12 operations, events and activities | Contract | Each operation, event and activity of §12 against the published contract of its owning service |
| TC-E6-028-11-ITG | ITG AC10 | Integration | A sale selection with one Idempotency-Key, its writing activity timed out and retried, over the three accounts |
| TC-E6-028-12-ITG | ITG AC11 | Integration | A consumed call of the sale selection forced to fail, and one forced not to answer, with no lot created |

TC-E6-028-01-ITG copies the legacy TC-E6-028-01 (AC1, the population sold), TC-E6-028-02-ITG copies TC-E6-028-02 (AC2, rule R-WO-12), TC-E6-028-03-ITG copies TC-E6-028-03 (AC3, rule R-WO-32), TC-E6-028-04-ITG copies TC-E6-028-04 (AC4, not recorded), TC-E6-028-05-ITG copies TC-E6-028-05 (access, MSG-P4-002) and TC-E6-028-06-ITG copies TC-E6-028-06 (the forced decision log write failure, MSG-P7-003). Legacy AC1 to AC4 stay with RWB-S7-E6028-APP, so each copy here asserts the same rule across the service boundary rather than inside S7; the full legacy tests, with their Given, When and Then, are in Recovery Workbench Test Cases v8.xlsx under the same legacy test case IDs.

### 17. Guardrails

- No business value in code: the three cases and their write-offs, the amounts, the write-off committee limit, the cut-off month, the business date, the fixture layout and the report shape are data.
- No personal data in logs, fixtures, events or the report: every key is synthetic, and `DecisionRecorded` and `CaseStateChanged` carry IDs, codes and states, never a customer fact.
- ACE data only through the P1 contract: DP09 Debt sale is read as a data product with its freshness stamp, never from a view and never from another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a breaker per downstream, so the harness fails where a screen would (DP-13, ADR-020).
- No invented operation: every path in section 12.2 is the owner's published operation, and the harness calls no write-off read and no write-off sale path because the Ownership Map publishes none.
- A fake pass is never reported as a real pass: the report names the contract version and whether the hop was a fake or the owner, and the S6 hop stays a fake hop until the S6 lot stories land.
- The harness never runs against UAT or production, never triggers the JOB-16 scan in a live environment, and never writes a row by hand.
- A failing criterion is fixed in the service that owns it or raised as a gap; it is never waived in the script, and no business decision is taken here.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-028 Sell a post charge-off population | Recovery Workbench User Stories Epics 3 to 8 v3, lines 10846 to 10939 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1 to AC4 | The same, lines 10862 to 10887 | Section 7, note: AC1 to AC4 stay with RWB-S7-E6028-APP; AC4 is asserted here across the boundary in AC5 |
| Legacy endpoints, the committee decision and the write-off scan | The same, lines 10897 to 10902 | Section 12.2 (the committee decision) and section 19 (the scan) |
| Legacy screen SCR-27 Write-off proposal and its states | The same, lines 10904 to 10908 | Section 15 |
| Legacy permission checks, Write-off and posting A and C | The same, lines 10910 to 10915 | Section 10; AC6 |
| Legacy messages MSG-S7-001, MSG-GEN-001, MSG-P4-002, MSG-P7-003 | The same, lines 10917 to 10924 | Section 14, copied word for word |
| Legacy test cases TC-E6-028-01 to TC-E6-028-06 | The same, lines 10926 to 10935 | Section 16, copied as -ITG |
| FEAT-WOF-16 Sell a post charge-off population | Epics 3 to 8 Specification v3, line 123 | Sections 2 and 8 |
| FEAT-DBS-09 Award the lot and test the price, the feature the legacy story depends on | The same, line 100 | Sections 2 and 8 |
| REQ-S7-006, post charge-off treatment set by rule | Business Requirements Program v4, line 397 | Sections 2 and 8, BR7 |
| REQ-S6-001, the sale population selected by rule against the policy cap | The same, line 377 | Sections 2 and 8, BR7 |
| R-WO-11, R-WO-12, R-WO-13, R-WO-15, R-WO-20, R-WO-29, R-WO-31 and R-WO-32 | Business Rules and Routing Logic v4, lines 342, 343, 344, 346, 351, 360, 362 and 363 | Section 8, BR1 to BR6; section 9 |
| S6 service row, S7 service row, and events 23 `LotAwarded` and 24 `WriteOffApproved` | Arch v5 slides 41 and 43, lines 2896 to 2899 and 2949 to 2950 | Sections 12.4, 12.5 and 12.9 |
| S6 lot contract and the debt sale saga, `GET/POST /lots`, `POST /lots/{id}/award`, `DebtSaleWorkflow` pivot = transfer | Arch v5, lines 1397 to 1403 | Sections 12.2, 12.5 and 13 |
| Edge rules, the partner gateway and one hop with a 2 s timeout | Arch v5, lines 1458 and 1460 | Sections 2, 12.2 and 17 |
| Point of no return and strict mode at the pivot | Temporal design, lines 1555, 1815 to 1819 and 1829 | Section 8, BR8; AC5 |
| Partner clocks and placement terms, R-WO-30 to R-WO-35 | Temporal design slide 25, lines 1663 to 1755 | Section 19; the agency placement is not exercised here |
| DF-FIN-010 to DF-FIN-020, DF-SAL-020 to DF-SAL-030, DF-SAL-031 to DF-SAL-037, DF-CAS-001 to DF-CAS-023, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application; metadata |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records, ADR-015 (Kafka with outbox and inbox), ADR-020 (one hop and 2 s) and ADR-022 (local record plus central ledger) | Sections 8, 12 and 13 |
| GAP-0458 and ASM-0650 | This WP's candidate rows, merged into the Gap Register and the Assumptions Register | Sections 3, 12.2, 12.8, 13 and 15 |
| RWB-S7-E6028-APP, RWB-P7-E6028-APP and RWB-S7-E6028-CON | The split plan of this wave | Section 19; the build of the sale decision and the states stays there |

### 19. Out of scope

- RWB-S7-E6028-CON, RWB-S7-E6028-APP and RWB-P7-E6028-APP: the write-off contract, the sale decision, the case states, the rule evaluation, the limit test and the decision record inside the services.
- The S6 debt sale build and its own stories: lots, the data room, the buyers, the qualification, the bids, the award, the data transfer, the derecognition and the general ledger posting (FEAT-DBS-02, FEAT-DBS-05, FEAT-DBS-09).
- The write-off scan and the tax criteria: RWB-E6-013 and RWB-E6-014.
- The committee pack: RWB-E6-015.
- The monthly scan population and its removal path (R-WO-06 to R-WO-10).
- The posting of the write-off and the provision release: RWB-E6-021 and RWB-E6-022.
- The agency placement, its capacity test and its recall (R-WO-30, R-WO-31, R-WO-34).
- SCR-27 Write-off proposal.
- The ALS and the general ledger adapters as products, and the ACE ingestion behind DP09.
- The platform H stories RWB-PLT-E1027-CON and RWB-PLT-N001-CON.
- Platform deployment, the topic and queue provisioning, the Schedule registration and the environment itself.
- Any production change.
