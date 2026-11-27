# RWB-ITG-E4045-ITG Calculate fees and charges

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E4045-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-045 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Size | Not sized in the story; the squad sizes it at refinement |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-ITG-E4045-ITG-14) |
| Contract story | Not specified in the source documents (DOR-RWB-ITG-E4045-ITG-21) |
| Fake library version | Not specified in the source documents (DOR-RWB-ITG-E4045-ITG-22) |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E4045-ITG-23) |
| Depends on (build) | None (RWB-P8-E4045-APP is an integration dependency only; the Day-1 run uses the rwb-payment stub in section 12.8) |
| Contract dependencies | None |
| Integration dependencies | RWB-P8-E4045-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-045 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E4045-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 13 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want **one repeatable cross-service harness that takes a seeded case with a payment on its account and a partner on its contracted fee terms, drives the fee step through rwb-payment, and proves that partner fees, court fees and charges are worked out from the fee tables held as data and written to the decision record with the rule version, against the owning services' published contracts and their fakes**, so that **every fee raised on a payment or a booking is shown to come from data a business person may change and to be on record before it is raised, and no fee reaches a partner, a court or the ledger on a value that lives in code**.

### 2. Business rationale

A fee worked out from a number in code cannot be defended when the contracted schedule moves, and it cannot be changed without a release. A court fee or a legal expense raised without its approval is spend beyond the delegation of authority, which the bank has to unwind. A partner fee paid without a recorded result is money it cannot recover. All three sit on one chain: the payment and its fee step in P8 rwb-payment, which owns payment and proceeds matching, fees and bookings in `rwb_payment`; the partner and its contracted fee terms in S9 rwb-partner, which owns the panel, partner users, instructions, results, fees and scorecards in `rwb_partner`; the payment row in `v_ace_payment`, which is ACE's and is read through P1 rwb-source-data's data product; the approver inside the D7.4 limit, whose DoA table is P4 rwb-access's; and the record that cites the rule and its version, which is written with the change in one transaction and reaches the ledger through `rwb.decision-record.v1` (REQ-DRI-001; R-UNI-39). Where the payment on the account is the settlement payment, the posting that raises it is R-SET-14's, and it belongs to the treatment and payment stories and not to this one.

This story owns the harness that proves that chain as the legacy key describes it, carrying AC1 of RWB-E4-045 into evidence. The fee tables are data, so the run asserts the outcome against the terms the owners publish and not against a figure written here. The three states the same loop touches are the owner's: PAYMENT_MATCHED when the payment matches (R-WO-37), PROCEEDS_APPLIED when the proceeds and the vendor fee are applied (R-DIS-54), and FEE_APPROVED when a court fee passes its approval (R-LIT-42). It serves REQ-S9-004, REQ-CHO-009 and REQ-DRI-001, and it carries FEAT-PAY-05 into evidence, with REQ-S9-004 read against the contracted schedule and against recorded results (R-DIS-11; R-WO-37).

The harness is decoupled the same way the services are. It owns no schema and reads no other service's table (DP-01): the fee step, the matched proceeds and the fees on the case come from rwb-payment, the partner and its contracted fee terms from rwb-partner, the payment row from rwb-source-data's product, the record from rwb-decision and the authority from rwb-access. It reads `v_ace_payment` through rwb-source-data's contract and never through a view of its own (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). It calls each owner's base `/api/recovery/<short>/v1`, one hop per call with a 2 s timeout and a circuit breaker per downstream, and it calls the gateway-bff composite route where a screen would (DP-19).

### 3. Preconditions

- The published contracts of rwb-payment, rwb-partner, rwb-source-data, rwb-case, rwb-decision and rwb-access are in the contract registry, and a stub set is generated from each published OpenAPI or AsyncAPI document with its version pinned.
- A case, a payment on its account and a partner on its contracted fee terms are seeded through the owning services' published operations only. The seeding set, the harness environment specification and the fixture contents are not specified in the source documents (GAP-0431; ASM-0607).
- The fee tables, the court fee and charge schedules and the partner's contracted fee terms are read from their owners only, and the harness holds no copy of any of them. Who owns and stores the fee tables and the two schedules, and their table and field names, are not specified in the source documents (GAP-0431; ASM-0607).
- The operation and field names in rwb-payment that carry the calculated fee amounts, and which field or child record of `partner` carries the contracted fee terms, are not specified in the source documents (GAP-0431; ASM-0607).
- The data product code that serves the `v_ace_payment` row through the source-data products operation is not specified in the source documents (GAP-0431; ASM-0607).
- The rule package in force carries R-LIT-41, R-LIT-42, R-DIS-11, R-DIS-54 and R-WO-37, and the version of each rule is readable on the decision record that cites it.
- An approver inside the D7.4 limit exists on the DoA data that rwb-access holds, and the approval it gives is the one the record cites before a court fee or a legal expense is raised (R-LIT-41; R-LIT-42).
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the roles that hold the case record R and for a caller whose role does not include the right.
- No build dependency and no contract dependency. Day 1, with the fakes of section 12.8 in place from the first run, and the rwb-payment fake replaced by the real service when RWB-P8-E4045-APP lands.

### 4. Flow

1. Harness: seeds the case, the payment on its account and the partner on its contracted fee terms through the owning services' published operations only; the seeding set and its environment are not specified in the source documents (GAP-0431; ASM-0607).
2. Harness: reads the partner and its contracted fee terms through `GET /api/recovery/partner/v1/partners` and pins the terms the run is keyed by, so that every fee assertion is made against the owner's data and not against a figure in the script (REQ-S9-004).
3. Harness: reads the payment row from `v_ace_payment` through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` and asserts `payment_code`, the amount, the account and the payment date the run was seeded with (DP-05, REQ-CHO-009). The product code is not specified in the source documents (GAP-0431; ASM-0607).
4. Harness: drives the fee step with `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match`, so the fees are worked out by the service that owns them and not by the harness. In production the same step is the `matchPayments` activity on queue rwb-payment (JOB-07), which updates `rwb_payment` and writes `rwb.payment.ProceedsMatched.v1` to its outbox in one transaction.
5. Harness: reads the matched proceeds and the fee amounts recorded against them through `GET /api/recovery/payment/v1/proceeds`, and the payments and the fees on the case through `GET /api/recovery/payment/v1/cases/{caseId}/payments`, which Architecture v5 slide 17 gives to rwb-payment. The field names that carry the fee amounts are not specified in the source documents (GAP-0431; ASM-0607).
6. Harness: asserts the partner fee against the contracted schedule read in step 2 and against the recorded result it is paid on, so the fee follows the schedule and the result and is not a percentage in the script (REQ-S9-004; R-DIS-11; R-WO-37).
7. Harness: asserts, for a court fee or a legal expense, that it was checked against its schedule and routed for approval inside the D7.4 limit before it was raised, and that the decision record names R-LIT-41 and R-LIT-42 with their versions (R-LIT-41; R-LIT-42).
8. Harness: asserts that where proceeds are applied, the vendor fee is matched on them, and that the proceeds and the fee read back from step 5 agree (R-DIS-54).
9. Harness: asserts that no fee amount is hard-coded: the same step is run for a second seeded partner on a different contracted schedule, and the fee must follow that partner's terms with no change to the harness. Who owns and stores the schedules is not specified in the source documents (GAP-0431; ASM-0607).
10. Harness: subscribes to `rwb.payment.events.v1` and asserts `rwb.payment.ProceedsMatched.v1` for the case, once for the run, with no personal data on it, and asserts `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for the record, reaching the ledger within 5 minutes (DP-03).
11. Harness: reads `GET /api/recovery/decision/v1/decision-log` and asserts exactly one record for the fee step, carrying the rule ID and the rule version the owner recorded, and the fee amounts it was based on (REQ-DRI-001).
12. Harness: repeats the run with the decision record forced to fail and asserts that nothing moves: no fee amount, no proceeds match, no approval and no case change, and the message the owner returns. This is the negative path of AC2, whose criterion belongs to RWB-P8-E4045-APP.
13. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a role that does not include the right.
14. Harness: publishes one evidence report per story and business date, naming the criterion, the assertions, the contract versions and whether each hop was a stub or the owner. The evidence format and its retention are not specified in the source documents (GAP-0431; ASM-0607).

The wave 3 entry check, with the integration and QA leads, settles the harness environment, the seeded identifiers, the fixed business date, the data product codes, the unnamed operations, the evidence format and the gate thresholds for this story (GAP-0436). No value is set in this story until that check.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The partner read from rwb-partner carries no contracted fee terms for the run's business date | The run fails on AC1 and the report names the partner and the terms it found | None | AC1 |
| X3 | The payment row read from `v_ace_payment` does not carry the `payment_code` the case was seeded with | The run fails on AC1 and the report names the payment row and the code it found | None | AC1 |
| X4 | The fee step returns or records a fee amount that does not follow the schedule read from the owner | The run fails on AC1 and the report names the schedule term, the expected amount and the amount recorded | None | AC1 |
| X5 | A court fee or a legal expense is raised with no approval inside the D7.4 limit | The run fails on AC1 and the report names the fee and the approval it looked for | None | AC1 |
| X6 | The proceeds are applied but no vendor fee is matched on them | The run fails on the R-DIS-54 assertion and the report names the proceeds | None | AC1 |
| X7 | The fee amount does not follow the second partner's contracted schedule, or it stays fixed when the terms differ | The run fails on the data-not-code assertion and the report names both partners and both schedules | None | AC1 |
| X8 | More than one record exists for the fee step, or its rule ID or rule version is missing | The run fails on AC1 and the report names the records it found | None | AC1 |
| X9 | The record does not reach `rwb.decision-record.v1` inside 5 minutes | The run fails on AC1 and the report names the record and its arrival time | None | AC1 |
| X10 | The decision record is forced to fail but a fee amount, a proceeds match or an approval still moves | The run fails on the negative path and the report names what moved | MSG-P7-003 | AC2 path, BR7 |
| X11 | A role that does not include the right is authorised, or a caller outside the case scope passes | The run fails on the access check and the report names the operation | MSG-P4-002 | AC3, AC4 |
| X12 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. R-LIT-41, R-LIT-42, R-DIS-11, R-DIS-54 and R-WO-37 carry no message ID in the rule set, so the harness asserts the state, the data, the proceeds and the decision record, and names a message ID only where an owning service returns one of the three in section 14.

The harness shows no screen. The SCR-28 states are listed in the state table in section 15, where the empty, error and no-access states are Not specified in the source documents (CG-ALL-882) (DOR-RWB-ITG-E4045-ITG-10).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-P8-E4045-APP |
| Negotiable | The seeding set, the schedule fixture, the report shape and the composite route are configuration agreed at the wave entry check, not business values in code |
| Valuable | The fee amounts, their schedule basis and their record are proven end to end before wave 3 opens |
| Estimable | One harness runner, one stub set, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-P8-E4045-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Calculate fees and charges

  Background:
    Given the seeded case carries a payment on its account and a partner on its contracted fee terms
    And the contract fakes of section 12.8 are published with their versions pinned

  Scenario: AC1 Calculate fees and charges (legacy RWB-E4-045 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then works out partner fees, court fees and charges from the fee tables held as data
    Then the system writes the result to the decision log with the rule version

  Scenario: AC3 Access check (covers exception X11) (new, D-RCV-60)
    Given a caller whose role does not include the right
    When the fee step is authorised through POST /api/recovery/access/v1/authorise
    Then the call is refused with MSG-P4-002 and the report names the operation

  Scenario: AC4 Caller outside the case scope is refused (new, D-RCV-60)
    Given a caller outside the case scope
    When the fee step is authorised through POST /api/recovery/access/v1/authorise
    Then the call is refused with MSG-P4-002 and the report names the operation

  Scenario: AC5 A vendor fee is matched when proceeds are applied (new, D-RCV-60)
    Given a case with a vendor fee recorded
    When proceeds are applied
    Then the vendor fee is matched on the proceeds

  Scenario: AC6 A consumed event delivered again is applied once (new, D-RCV-60)
    Given an event the fee step has already consumed
    When the same event is delivered again
    Then the fee step applies it once and the second delivery changes nothing

  Scenario: AC7 A consumed call that fails or does not answer records no fee action (new, D-RCV-60)
    Given the fee step has made a call to a consumed contract
    When the call fails or does not answer
    Then the fee step records no fee action for that call

  Scenario: AC8 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change the model does not allow
    When the fee step requests the change
    Then the change is refused and nothing is written
```

AC2 of the legacy key ("Not recorded") is owned by RWB-P8-E4045-APP and is not restated here; the harness exercises it only as the negative path of the same loop, in step 12 of section 4 and in TC-E4-045-02-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Partner fees, court fees and charges are worked out from the fee tables held as data, never from a value in code | Legacy RWB-E4-045 AC1; REQ-S9-004 |
| BR2 | A partner fee follows the contracted schedule and is paid against recorded results | REQ-S9-004; R-DIS-11; R-WO-37 |
| BR3 | A court fee or legal expense is checked against its schedule and routed for approval inside the D7.4 limit before it is raised | R-LIT-41; R-LIT-42 |
| BR4 | Payments are matched to the plan, the settlement or the fee they belong to by the ACE `payment_code`, and anything unmatched goes to the exception list | REQ-CHO-009 |
| BR5 | A vendor fee is matched when proceeds are applied | R-DIS-54; AC5 |
| BR6 | The fee amounts and the rule version are written to the decision record with the change in one transaction | REQ-DRI-001; R-UNI-39 |
| BR7 | No fee action proceeds if its record cannot be written | REQ-DRI-005; R-UNI-39 |

The fee tables' owner and storage are not named by any source read, and the harness reads the fee terms through the owning contracts and holds no copy.

Reference data: the harness reads the fee tables and the court fee and charge schedules as reference data through the owning contracts (DP-06, DP-07). The parameter names and keys are not specified in the source documents (DOR-RWB-ITG-E4045-ITG-20).

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PLACED_WITH_AGENCY | PAYMENT_RECEIVED_AFTER_CHARGEOFF | the payment matches the case and the placement | PAYMENT_MATCHED (R-WO-37) |
| ASSET_SOLD | PROCEEDS_POSTED | any | PROCEEDS_APPLIED (R-DIS-54), with the vendor fee matched on the proceeds |
| LEGAL_SPEND_APPROVAL | FEE_APPROVED | inside the D7.4 limit, or the committee approves above it | IN_HEARING (R-LIT-42), with the fee raised and posted against the case |

These are the owner's states: rwb-payment raises PAYMENT_MATCHED and PROCEEDS_APPLIED in its own schema, and the approval inside the D7.4 limit is rwb-access's and rwb-decision's. The harness changes none of them itself. It seeds through the owning services' published operations, drives the fee step through the rwb-payment contract, and then asserts the state the owner reached, naming the owner and the operation behind each move in the report. A state the harness set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL and the roles that hold Treatment and offer C | Drive the fee step for their case and read the fees, the proceeds and the record through the owning contracts |
| RW-CASEOWN, RW-TEAMMGR, RW-PHONECOL, RW-FIELDCOL, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD and the further roles that hold the case record R | Read the same run evidence, including the partner's fee terms, the payment row and the decision record |
| QA lead | Owns the harness configuration, the seeding set, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-payment, rwb-partner, rwb-source-data, rwb-decision and rwb-access make every change the harness asserts |
| No approval level from the delegation of authority applies to the harness | The harness takes no business decision; the approval inside the D7.4 limit belongs to the fee story and to the approver |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | id, case_no, product_group, primary_person_key, status, stage_code | Read, through the rwb-case contract |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount | Read, through the rwb-source-data data product (DP-05); no direct view read |
| DF-PRT-001 to DF-PRT-007 | partner | id, partner_code, partner_name, partner_type, panel_status, contract_end | Read, through the rwb-partner contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | id, case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | id, rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. Which field or child record of `partner` carries the contracted fee terms, and which `decision_log_entry` and `rule_row` fields carry the calculated fee amounts, are not specified in the source documents (GAP-0431; ASM-0607). The harness owns no table and writes no row directly: every read and every seed goes through the API of the owning service (DP-01, DP-05), and the payment row is ACE's, so the Workbench holds no payment copy (legacy RWB-E4-045; D-RCV-35 U1 and U4).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/payment/v1/proceeds/{proceedsId}/match` | P8 rwb-payment | Drive the fee step as part of the payment and proceeds match (AC1) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The matched proceeds and the fee amounts recorded against them (AC1) |
| GET | `/api/recovery/payment/v1/cases/{caseId}/payments` | P8 rwb-payment | The payments and the fees on the case; Architecture v5 slide 17 gives this path to rwb-payment (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state and identity the fee is recorded against (AC1) |
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | The partner record and its contracted fee terms (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The payment row from `v_ace_payment` (AC1, DP-05) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record with the rule ID and the rule version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope, including the refusal path (AC1) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream. Where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). The `{productCode}` that carries the `v_ace_payment` row, the operation and field names that carry the calculated fee amounts in rwb-payment, and the field that carries the contracted fee terms in rwb-partner are not specified in the source documents (GAP-0431; ASM-0607). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the fee step through the rwb-payment contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | P8 rwb-payment | The fact that the fee step follows, once for the run (AC1) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through its own local decision-record library | The record written with the fee change reaches the ledger within 5 minutes (AC1, DP-03) |

Both carry IDs and business facts only, keyed by caseId and proceedsId, and the harness asserts that no personal data is present.

#### 12.5 Workflows and activities

None added. The harness exercises the `matchPayments` and `postProceeds` activities on queue rwb-payment, which carry the fee step and the proceeds posting, and the treatment and settlement path that raises them, and it asserts their effects through the services' contracts and the owner's topic. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The fee step is triggered by the payment and the proceeds match and not by a Schedule, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the fees, the proceeds and the payments are rwb-payment's, the partner and its fee terms are rwb-partner's, the record and the rule rows are rwb-decision's, the role, scope and DoA data are rwb-access's, and the payment row is ACE's, read through rwb-source-data's contract (DP-05).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-payment | `POST /proceeds/{proceedsId}/match`, `GET /proceeds`, `GET /cases/{caseId}/payments`, `rwb.payment.events.v1` | Day-1 run of AC1 and of the negative path before RWB-P8-E4045-APP is live |
| Stub for rwb-partner | `GET /partners` | Day-1 assertion of the partner and its contracted fee terms |
| Stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertion and Given of the `v_ace_payment` row; no test-data line reads the view directly |
| Stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertion of the case state and identity the fee is recorded against |
| Stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record for the fee step with its rule version |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| ProceedsMatched event stub | `rwb.payment.ProceedsMatched.v1` | The fact that the fee step follows, where the environment does not run the payment match |

Each fake is generated from the published OpenAPI or AsyncAPI document of its service, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The fee tables and the court fee and charge schedules, the fee operation and its field names in rwb-payment, the data product code, the harness environment, the seeding set and the evidence format are not specified in the source documents (GAP-0431; ASM-0607).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s timeout and a circuit breaker per downstream, composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.payment.ProceedsMatched.v1` and `rwb.decision.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | Exercised only: the `matchPayments` and `postProceeds` activities on queue rwb-payment and the treatment and settlement path that raises them; none added |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependency is the one I story, RWB-P8-E4045-APP: until it is live the run uses the rwb-payment stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour. The legacy key states no endpoint and says the work runs inside the recovery module, so the fee step is the owner's activity and not something the harness computes. The harness owns no schema (DP-01) and reads the fees, the proceeds, the partner, the record and the payment row from their owners only. The payment row is read through rwb-source-data's data product, which owns the ACE view contract, and not through a view of the harness's own (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). The composed reads a screen would make are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| FeeCalculationRunner | Job | Runs the owned criterion and the negative path in order for a business date and holds the run lock |
| StubSet | Fake | The six service stubs and the ProceedsMatched event stub of section 12.8, each generated from the published contract with the version pinned |
| FeeScheduleProbe | Service | Reads the partner's contracted fee terms and the court fee and charge schedules from their owners, and asserts the fee amounts against them rather than against a figure in the script |
| ProceedsProbe | Service | Reads the matched proceeds, the fees on the case and the payment row, and asserts them for the case and the payment |
| EventProbe | Service | Consumes `rwb.payment.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the report keyed by story and business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, with one case carrying a payment on its account and one partner on its contracted fee terms, and one case whose proceeds are applied for the vendor fee path. The environment, the seeding set, the fee tables and the schedules behind it, and the evidence retention are not specified in the source documents (GAP-0431; ASM-0607). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the six service stubs and the ProceedsMatched event stub from the published contracts, pin each version in the report and fail the run on a version mismatch (X1, X12).
2. Build the FeeScheduleProbe to read the partner's contracted fee terms and the court fee and charge schedules from their owners, and to fail where the owner publishes none for the business date (X2).
3. Build the ProceedsProbe to read the payment row through the rwb-source-data contract fake (section 12.8) and the fees from rwb-payment (X3).
4. Build the FeeCalculationRunner for AC1: drive the fee step, read the matched proceeds and the fees on the case, assert the partner fee against the schedule and the recorded result, and assert the court fee against its schedule and its approval (X4, X5).
5. Add the vendor fee assertion on the R-DIS-54 path: apply the proceeds and assert the vendor fee matched on them (X6).
6. Add the data-not-code assertion: change the schedule held by the owner for the business date and assert the fee follows it, with no change to the harness (X7).
7. Assert one record for the fee step through the rwb-decision contract, naming the rule ID and version and the fee amounts it was based on, and fail where either is absent (X8).
8. Add the EventProbe for `rwb.payment.ProceedsMatched.v1` and `rwb.decision.DecisionRecorded.v1`, and assert the key, the 5-minute arrival and the absence of personal data (X9).
9. Add the negative path: force the decision record to fail, assert that nothing moves and record the message the owner returns (X10).
10. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a role that does not include the right (X11).
11. Add the EvidenceReport and the gate, then swap the rwb-payment stub for the real service when RWB-P8-E4045-APP lands and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it; the flag key is not specified in the source documents (GAP-0431; ASM-0607).

**Done when.** The tests of section 16 pass; the criterion passes against the fakes on Day 1 and again against rwb-payment when RWB-P8-E4045-APP lands; and the wave entry check holds a report keyed by story and business date with the contract, schedule and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the fee step cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-LIT-41, R-LIT-42, R-DIS-11, R-DIS-54 and R-WO-37 carry no message ID in the rule set, so the harness asserts the state, the data and the decision record, and names a message ID only where an owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-28 Proceeds matching is the screen the legacy key names for this behaviour:

| State | What the user sees and does |
|---|---|
| Loading | The payment match and the fee step are running for the business date |
| matched | The payment, the proceeds and the fee are aligned to the case and to the partner's schedule |
| unmatched | The payment, a fee or a vendor fee does not align to the case, and an officer has to resolve it on the exception list |
| Empty | Not specified in the source documents (CG-ALL-882) |
| Error | Not specified in the source documents (CG-ALL-882) |
| No access | Not specified in the source documents (CG-ALL-882) |

The harness renders no screen. It reads these states through the rwb-payment, rwb-partner, rwb-source-data and rwb-decision contracts, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0431; ASM-0607).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-045-01-ITG | AC1, BR1, BR2, BR3, BR4, BR6 | Integration | Seeded case with a payment and a partner on a contracted fee schedule |
| TC-E4-045-02-ITG | BR7 (negative path only; AC2 run by RWB-P8-E4045-APP) | Integration | Decision log forced to fail; MSG-P7-003 |
| TC-E4-045-03-ITG | AC3 (X11), Access | Component | A role without the right; MSG-P4-002 |
| TC-E4-045-04-ITG | Principle 5 | NFR | Forced decision-log write failure; nothing moves |
| TC-E4-045-05-ITG | AC4 (X11, case scope), Access | Component | A caller outside the case scope; MSG-P4-002 |
| TC-E4-045-06-ITG | AC5, BR5 | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC4) | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC4) |
| TC-E4-045-07-ITG | AC6 | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC5) | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC5) |
| TC-E4-045-08-ITG | AC7 | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC6) | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC6) |
| TC-E4-045-09-ITG | AC8 | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC7) | Not specified in the source documents (NEWAC-RWB-ITG-E4045-ITG-AC7) |

These are the ITG copies of TC-E4-045-01 to TC-E4-045-04 and carry the legacy data unchanged, with the component and NFR copies keeping the legacy levels. TC-E4-045-05-ITG to TC-E4-045-09-ITG are new and have no legacy copy. The full legacy tests, with their Given, When and Then, are in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under those IDs.

### 17. Guardrails

- No business value in code: the fee tables, the court fee and charge schedules, the partner's contracted fee terms, the rule versions, the seeding set and the result mappings are data, and the harness holds no copy of any of them.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the payment row is ACE's, read through rwb-source-data's data product (DP-05).
- The Workbench holds no payment copy and writes no fee row outside the owning service; the fee amounts are the owner's and are read back through its contract (legacy RWB-E4-045; D-RCV-35 U1 and U4).
- One hop and a 2 s timeout per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a fee, a proceeds match, an approval or a decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results | Business Requirements Program v5, section 5.16 | FEAT-PAY-05 | D6.4 settlement; D7.4 legal spend | R-DIS-11, R-WO-37 | TC-E4-045-01-ITG |
| REQ-CHO-009 | Payments received, read from ACE through `v_ace_payment`, are matched to the plan, the settlement or the fee they belong to by the ACE `payment_code`, and anything unmatched goes to an exception list | Business Requirements Program v5, section 5.3 | FEAT-PAY-05 | D6.4 settlement | R-DIS-54 | TC-E4-045-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Business Requirements Program v5, section 5.7 | FEAT-PAY-05 | D6.4 settlement; D7.4 legal spend | R-LIT-41, R-LIT-42, R-DIS-54 | TC-E4-045-01-ITG, TC-E4-045-02-ITG, TC-E4-045-04-ITG |

### 19. Out of scope

- AC2 of the legacy key, the refusal when the decision log cannot be written, which is owned by RWB-P8-E4045-APP; this story exercises it only as a negative path.
- The production payment endpoint and the fee step inside rwb-payment, which are RWB-P8-E4045-APP: the fee calculation, the proceed and fee records and the posting file.
- The fee tables themselves and the court fee and charge schedules, their owner, their storage, their table and field names and the business values they hold.
- The contract baselines of rwb-payment, rwb-partner, rwb-source-data, rwb-decision and rwb-access, which are their CON stories and are consumed here through the published documents and their fakes.
- The platform configuration: the decision-record library, the gateway-bff composite route, the feature-flag library and the observability set.
- The partner portal and the partner gateway: the panel, the partner users and how a partner submits a result, which belong to rwb-partner.
- The approval itself inside the D7.4 limit and the DoA table behind it, which belong to the fee story, to rwb-access and to rwb-decision.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.
