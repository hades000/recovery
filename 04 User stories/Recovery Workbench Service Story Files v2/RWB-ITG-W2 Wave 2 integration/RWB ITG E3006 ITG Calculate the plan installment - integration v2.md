# RWB-ITG-E3006-ITG Calculate the plan installment

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E3006-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP07, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E3006-ITG-16); the squad sizes it at refinement |
| Contract version | /v1 on each owner's base path `/api/recovery/<short>/v1` |
| Contract fake library version | Not specified in the source documents (DOR-RWB-ITG-E3006-ITG-22) |
| Depends on (build) | RWB-S2-E3006-APP |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | RWB-S2-E3006-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-006 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E3006-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 18 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As an **integration and QA harness**, I want **one repeatable cross-service proof that, when the route is approved, the payoff is taken from ALS, the range the officer may move within is set from reference data and the case reaches PAYOFF_AND_RANGE_SET with one decision record naming the rule and its version, against the owning services' published contracts and their fakes**, so that **the officer negotiates on the figure the bank's own system of record holds and inside the guardrail the rule set allows, and a payoff, a range and a case state cannot drift apart unseen**.

The treatment is owned by rwb-treatment, the case state by rwb-case, the ALS facts by ACE and read through rwb-source-data, the reference rows by rwb-case, and the record by rwb-decision. The harness provides no operation, table, workflow, schedule or screen. It proves the behaviour the owning services publish, and RWB-S2-E3006-APP owns the real behaviour and builds it.

### 2. Business rationale

The range the officer may move within is the guardrail that keeps a settlement negotiation inside the rule set: REQ-S2-004 says settlement terms are negotiated inside a rule-set range and anything outside it needs approval, and a range nobody set from reference data is no guardrail at all. The payoff behind that range comes from ALS and is never re-keyed, so the figure the officer reads is the figure the core system holds. Without one cross-service proof, a payoff figure, a range and a case state can each be right on their own and still disagree: the officer negotiates on a stale number, or on a range that came from a lookup table somebody edited, and the case has already moved as if both were settled.

The monolith computed all three in its P3 module against the single recovery schema, in one transaction, where a range that did not match its reference row could not hide behind a case that had moved. In v5 they arrive through four owners and one shared record: rwb-treatment holds the settlement treatment and drives the step, rwb-case holds the case status and the reference data the range is set from, rwb-source-data owns the contract over the ACE views that carry the ALS payoff facts, and rwb-decision holds the record with the rule and its version. A defect at any hop now looks exactly like a successful step, until the offer built on that range is approved and booked.

This story owns the harness that proves the composition as the legacy key describes it. It carries AC2 of RWB-E3-006, the R-SET-01 criterion, into evidence: a case in state ROUTE_APPROVED_SETTLEMENT, the route approved, the payoff calculated from ALS, the range set from reference data, and the case at PAYOFF_AND_RANGE_SET. It serves REQ-S2-004 and REQ-RDF-002, and it carries the record rules REQ-DRI-001 and REQ-DRI-005 into evidence, with FEAT-TRT-06.

The harness is decoupled the same way the services are. It never reads another service's table (DP-07): the treatment and its state come from rwb-treatment, the case status from rwb-case, the ALS facts from rwb-source-data, the range rows from rwb-case's reference-data contract and the record from rwb-decision. It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13), and it calls through the gateway-bff composite route where a screen would (DP-19). Every call is one hop with a 2 s budget. The ACE payoff facts are read through rwb-source-data's products contract and never through a view of the harness's own (DP-05), and the record is read from rwb-decision and the shared `rwb.decision-record.v1` topic (DP-03).

### 3. Preconditions

- The published contracts of rwb-treatment, rwb-case, rwb-source-data, rwb-decision and rwb-access are in the contract registry, and a WireMock stub set is generated from each one and its version pinned.
- A case sits at ROUTE_APPROVED_SETTLEMENT with its settlement treatment, seeded through the owning services' published operations only. The seeding set, the SIT environment specification and the evidence format are not specified in the source documents (GAP-0423; ASM-0598).
- The ALS facts for the case's account are available through the P1 rwb-source-data products contract, current to the ACE batch the environment is on.
- The reference rows that carry the range exist for the case's band, and the harness reads them through the rwb-case reference-data contract and never from a table.
- The rule package in force carries R-SET-01, and its version is readable on the decision record that cites it.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for a role that holds Treatment and offer C and for a caller outside it.
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run, and the rwb-treatment fake replaced by the real service when RWB-S2-E3006-APP lands.

### 4. Flow

1. Harness: seeds the case, its settlement treatment and the account it belongs to through the owning services' published operations only, and reads each back. The seeding set and its environment are not specified in the source documents (GAP-0423; ASM-0598).
2. Harness: reads the case state through `GET /api/recovery/case/v1/cases/{caseId}` and asserts ROUTE_APPROVED_SETTLEMENT before the step.
3. Harness: reads the treatment through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and asserts it is the settlement treatment of that case, so the step is driven by the owner's record and not by a fixture.
4. Harness: places or observes the route approval. A case seeded at ROUTE_APPROVED_SETTLEMENT already carries the ROUTE_APPROVED fact, so the run observes it rather than raising it; the route decision itself is S1 rwb-valuation's and is out of this story, and the rule's condition (decision.approved and route = R2, R-SET-01) is read from the rule package in force.
5. Harness: asserts the payoff facts through `GET /api/recovery/source-data/v1/data-products/{productCode}/records`, read from the ACE views that carry the ALS balances, and that they are the figures the case is now set from (DP-05). The data product code that carries them is not named for this story in the source documents (GAP-0423; ASM-0598).
6. Harness: asserts the range rows through `GET /api/recovery/case/v1/admin/lists/{listCode}` on P3 rwb-case's reference-data contract, and that the range the case holds resolves to those rows and not to a value in code (DP-07). The list code that carries the range is not named for this story in the source documents (GAP-0423; ASM-0598).
7. Harness: asserts the case at PAYOFF_AND_RANGE_SET through `GET /api/recovery/case/v1/cases/{caseId}` and `rwb.case.CaseStateChanged.v1` for the move on `rwb.case.events.v1`.
8. Harness: asserts exactly one decision record for the move through `GET /api/recovery/decision/v1/decision-log`, naming R-SET-01 and its rule version, and asserts `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` for that record (DP-03).
9. Harness: asserts the earlier fact where the treatment was approved before the run, `rwb.treatment.TreatmentApproved.v1` on `rwb.treatment.events.v1`, once for the path and with no personal data on it.
10. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a caller without the Treatment and offer C right.
11. Harness: asserts that each call sat on the owner's base as a single hop with a 2 s budget and a breaker per downstream, and that no call was retried into a second state change.
12. Harness: writes one evidence report per business date, keyed by story and business date, with the criterion and its assertions, and gates the wave on the result. The evidence format and its retention are not specified in the source documents (GAP-0423; ASM-0598).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC2 |
| X2 | The payoff facts are not reflected from the ACE views inside the run window | The run fails and the report names the data product, the account and the business date | None | AC2 |
| X3 | No reference rows exist for the case's band, or the case's range does not resolve to a row | The run fails on AC2 and the report names the list code, the band and the rows it found | None | AC2; BR2 |
| X4 | The case does not reach PAYOFF_AND_RANGE_SET | The run fails on AC2 and the report names the two states it saw | None | AC2 |
| X5 | Zero decision records or two exist for the move, or the record carries no rule version | The run fails on AC2 and the report names the records it found | None | AC2; BR4 |
| X6 | The record cannot be written for the move | Nothing changes: the case state, the treatment and the range stay as they were, and the owning service returns MSG-P7-003 | MSG-P7-003 | AC2; BR5 |
| X7 | A role without the Treatment and offer C right attempts the step | The call is refused with MSG-P4-002 and the refusal is recorded | MSG-P4-002 | AC2 |
| X8 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC2 |

The report text is for the wave entry check and is not part of the message standard. The rule set carries no message ID for R-SET-01, so the harness asserts state, data and the decision record and not a message; the business messages this journey can produce are in section 14 and belong to the owning services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-S2-E3006-APP |
| Negotiable | The data product code, the list code, the seeding set and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The payoff from ALS, the range from reference data and the move to PAYOFF_AND_RANGE_SET are proven end to end, with their record, before the wave opens |
| Estimable | One harness runner, one stub set, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-S2-E3006-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Calculate the plan installment

  Scenario: AC2 Rule R-SET-01 (legacy RWB-E3-006 AC2)
    Given a case in state ROUTE_APPROVED_SETTLEMENT
    When route approved
    Then calculate the payoff from ALS and set the range from reference data
    Then the case moves to PAYOFF_AND_RANGE_SET

  Scenario: AC4 The range the officer may move within is present from reference data (new, D-RCV-60)
    Given a case in state PAYOFF_AND_RANGE_SET
    When the range is read
    Then the range from reference data is present for the case

  Scenario: AC5 A consumed event delivered twice moves the case once (new, D-RCV-60)
    Given a case in state ROUTE_APPROVED_SETTLEMENT
    When the route approved event is delivered twice
    Then the case moves to PAYOFF_AND_RANGE_SET once

  Scenario: AC6 A consumed call that fails leaves the case unchanged (new, D-RCV-60)
    Given a case in state ROUTE_APPROVED_SETTLEMENT
    When the call to an owner's contract fails
    Then the case stays at ROUTE_APPROVED_SETTLEMENT and no decision record is written

  Scenario: AC7 A status change the model does not allow is refused (new, D-RCV-60)
    Given a case in state ROUTE_APPROVED_SETTLEMENT
    When a status change the model does not allow is requested
    Then the change is refused, the case stays in its current state and no decision record is written
```

AC1 and AC3 are owned by the app story of this legacy key, RWB-S2-E3006-APP, and are not restated here. AC2 is the cross-service criterion this ITG copy owns: the harness asserts it through the owners' contracts, and it carries no business value of its own.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | At ROUTE_APPROVED_SETTLEMENT with the route approved, the Workbench calculates the payoff from ALS, sets the range from reference data and the case moves to PAYOFF_AND_RANGE_SET | R-SET-01; FEAT-TRT-06 |
| BR2 | The range the officer may move within comes from reference data and never from a value in code, and a case outside it needs approval | R-SET-01; REQ-S2-004 |
| BR3 | The payoff is read from ALS and is never re-keyed into a Workbench copy | REQ-RDF-002; legacy RWB-E3-006 AC2 |
| BR4 | The decision record carries the rule and its version, and it is written with the state change | REQ-DRI-001 |
| BR5 | No move proceeds if its decision record cannot be written | REQ-DRI-005 |
| BR6 | The treatment is the owner's: the harness places no treatment row, and the settlement treatment and its terms stay with rwb-treatment | Legacy RWB-E3-006; DP-01 |
| BR7 | An offer outside the range needs approval; the offer rules that carry it, R-SET-04 and R-SET-05, belong to RWB-S2-E3006-APP and the harness asserts only that the range exists | REQ-S2-004; legacy RWB-E3-006 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ROUTE_APPROVED_SETTLEMENT | ROUTE_APPROVED | decision.approved and route = R2 | PAYOFF_AND_RANGE_SET (R-SET-01) |

The treatment and the case are the owners' state: rwb-treatment holds the settlement treatment and drives the step, and P3 moves the case status on the fact the step raises. The treatment approval is published as `rwb.treatment.TreatmentApproved.v1`, the case move as `rwb.case.CaseStateChanged.v1`, and the record as `rwb.decision.DecisionRecorded.v1`.

The harness changes no state itself. It seeds through the owning services' published operations, observes the route approval the seeded case already carries, and then asserts the state the owner reached: ROUTE_APPROVED_SETTLEMENT to PAYOFF_AND_RANGE_SET. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT and the roles with Treatment and offer C (RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT) | Read the case, the treatment, the ALS payoff facts, the range and the record, and place the step where the run must; the harness calls under the same right and fails where it is refused |
| The roles with Treatment and offer R (RW-CASEOWN, RW-TEAMMGR, RW-RESTRUCT, RW-SPECIAL, RW-COMPLAIN, RW-FRAUD, RW-LITOFF, RW-LEGAL and 12 more) | Read the same journey evidence, including the case state, the range and the decision record |
| QA lead | Owns the harness configuration, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-treatment, rwb-case, rwb-source-data, rwb-decision and rwb-access make every state change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the settlement approval and any offer outside the range belong to the treatment story |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | status (ROUTE_APPROVED_SETTLEMENT, PAYOFF_AND_RANGE_SET) | Read, through the rwb-case contract |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_code, total_balance and the balance fields the payoff is taken from | Read, through the rwb-source-data products contract |
| DF-ACE-270 to DF-ACE-279 | v_ace_score | score_key, account_key, model_code, model_version, score_value, estimate_value and 4 more | Read, through the rwb-source-data products contract, only where the payoff or the range uses a score |
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, decision_log_id, treatment_type, state | Read and write, through the rwb-treatment contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code and 9 more | Read, through the rwb-decision or rwb-case contract, never from a table |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The harness owns no table and writes no row directly: it reads and writes through the API of the owning service only (DP-05, DP-07), and the payoff stays ALS's, because ACE holds it and the Workbench holds no copy (legacy RWB-E3-006; REQ-RDF-002).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/treatment/v1/cases/{caseId}/treatments` | S2 rwb-treatment | Seed the settlement treatment, only where the run must (AC2) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Read the settlement treatment and its state (AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case at ROUTE_APPROVED_SETTLEMENT and at PAYOFF_AND_RANGE_SET (AC2) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The reference rows the range is set from (DP-07, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The ALS payoff facts the case is set from (DP-05, AC2) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | One record for the move, naming R-SET-01 and its version (AC2) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and authority check for each call, including the refusal path (AC2) |

The data product code that carries the ALS payoff facts and the list code that carries the range are not named for this story in the source documents (GAP-0423; ASM-0598). Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-13); where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the step through the owning services' contracts and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The settlement treatment was approved before the run (AC2) |
| `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | The case reached PAYOFF_AND_RANGE_SET (AC2) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through the local decision-record library | The record written with the state change, naming R-SET-01 and its version (AC2) |

All three carry IDs and business facts only, keyed by caseId and treatmentId, and the harness asserts that no personal data is present (DP-03).

#### 12.5 Workflows and activities

None added. The harness exercises the existing TreatmentWorkflow in rwb-treatment, which holds the settlement treatment across the step, and the CaseWorkflow in rwb-case, which moves the case status on the fact the step raises, and asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. R-SET-01 is triggered by a fact and not by a Schedule, and this story sets no cron, overlap policy, catch-up window or Schedule of its own.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-07): the treatment is rwb-treatment's, the case status and the reference rows are rwb-case's, the ALS payoff facts are ACE's, read through rwb-source-data's contract (DP-05), and the record is rwb-decision's.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-treatment | `POST /cases/{caseId}/treatments`, `GET /treatments/{treatmentId}`, `rwb.treatment.events.v1` | Day-1 run of AC2 before RWB-S2-E3006-APP is live |
| WireMock stub for rwb-case | `GET /cases/{caseId}`, `GET /admin/lists/{listCode}`, `rwb.case.events.v1` | Day-1 assertions on ROUTE_APPROVED_SETTLEMENT, PAYOFF_AND_RANGE_SET and the reference rows |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertion of the ALS payoff facts |
| WireMock stub for rwb-decision | `GET /decision-log`, `rwb.decision-record.v1` | Day-1 assertion of one record for the move with its rule version |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The exact response values of each stub, the seeding set, the SIT environment and the evidence format and retention are not specified in the source documents (GAP-0423; ASM-0598).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.treatment.TreatmentApproved.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | None added; the TreatmentWorkflow and the CaseWorkflow exercised |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays None. The blocking dependency is the one I story, RWB-S2-E3006-APP: until it is live the run uses the rwb-treatment stub, and a stub pass is reported as a stub pass.

The microservice move is the story's own reading of the legacy behaviour. The treatment and the payoff calculation that the monolith's P3 module did in one transaction against the single recovery schema become S2 rwb-treatment's own behaviour, driven by its own workflow and recorded by its own code. The ALS facts come through P1 rwb-source-data's contract and never from a local copy or a view of the harness's own (DP-05), and the range comes from P3 rwb-case's reference-data contract and never from a value in code (DP-07). Every call sits on the owner's per-service base with one hop (DP-13), the record goes through the local decision-record library and the shared topic (DP-03), and the composed read a screen would make goes through the gateway-bff composite route (DP-19). Per-service schemas mean the Workbench holds no payoff copy: the ALS balances stay ACE's, and the harness sees them only as the owner returns them.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the owned criterion for a business date and holds the run lock |
| StubSet | Fake | The five WireMock stubs, each generated from the published contract with the version pinned |
| EventProbe | Service | Consumes `rwb.treatment.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, on a case at ROUTE_APPROVED_SETTLEMENT with its settlement treatment, the ALS payoff facts for its account and the reference rows that carry its range. The environment, the seeding set and the evidence retention are not specified in the source documents (GAP-0423; ASM-0598). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the five stubs from the published contracts, pin each contract version in the run report and fail the run on a version mismatch (X1, X8).
2. Build the JourneyRunner for AC2: read the case at ROUTE_APPROVED_SETTLEMENT, read the settlement treatment, observe the route approval, and read the ALS payoff facts and the range rows through their owners (X2, X3).
3. Assert the case at PAYOFF_AND_RANGE_SET, that the range the case holds resolves to the reference rows it was set from, and that no value came from the script (X3, X4).
4. Add the EventProbe for `rwb.case.CaseStateChanged.v1`, `rwb.treatment.TreatmentApproved.v1` and `rwb.decision.DecisionRecorded.v1` and assert the key and the absence of personal data.
5. Assert exactly one decision record for the move, naming R-SET-01 and its rule version, and fail where zero or two exist or the version is missing (X5).
6. Add the record failure path: with the decision log write forced to fail, the case state, the treatment and the range stay untouched and the owner returns MSG-P7-003 (X6).
7. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller without the Treatment and offer C right (X7).
8. Add the EvidenceReport and the gate, then swap the rwb-treatment stub for the real service when RWB-S2-E3006-APP lands and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The journey runs behind the platform feature-flag library as the wave releases it; the flag key for this harness is not specified in the source documents (GAP-0423; ASM-0598).

**Done when.** The tests of section 16 pass for AC2; the criterion passes against the fakes on Day 1 and again against rwb-treatment when RWB-S2-E3006-APP lands; and the wave entry check holds a run report keyed by story and business date with the contract versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S2-002 | The payoff the case holds is older than the freshness limit | The payoff is from {date}. A new figure has been requested. |
| MSG-P7-003 | The decision record for the move cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-SET-01 carries no message ID in the rule set, so the harness asserts the state, the data and the decision record and names a message ID only where the owning service returns one of the four above. The payoff freshness warning is R-SET-03's and belongs to the owning service; the harness produces none of these messages itself.

### 15. Screens and states

SCR-15 Settlement offer and SCR-14 Treatment record (both built in RWB-S2-E3006-APP) show the states this journey sets and the values it fixes:

| State | What the user sees and does |
|---|---|
| ROUTE_APPROVED_SETTLEMENT | The route is approved and the case waits for the payoff and the range; the offer cannot be built yet |
| PAYOFF_AND_RANGE_SET | The payoff is held from ALS and the range from reference data, and the officer builds an offer inside the range on SCR-15 |
| Draft | The settlement treatment is being prepared on SCR-14 |
| Approved | The settlement treatment is approved and the offer is released on SCR-15 |
| Empty, loading, error and no access on SCR-14 | Not specified in the source documents (CG-ALL-817) |
| Empty, loading, error and no access on SCR-15 | Not specified in the source documents (CG-ALL-818) |

SCR-14 shows Draft, submitted, approved, booked and broken; SCR-15 shows Draft, below floor, approved, sent and accepted. The case states ROUTE_APPROVED_SETTLEMENT and PAYOFF_AND_RANGE_SET are read through the rwb-case contract and shown on the case record view, whose screen ID is not named for this feature in the source documents (GAP-0423; ASM-0598).

The harness renders no screen. It reads these states and values through the rwb-treatment, rwb-case, rwb-source-data and rwb-decision contracts, so a passed run means the screens have the right data behind them. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0423; ASM-0598).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-006-01-ITG | Legacy AC1 of RWB-E3-006, the criterion RWB-S2-E3006-APP owns, asserted here as the composed result: the model installment and the range the officer may move within, with the record and its rule version (BR1, BR2, BR3, BR4) | Integration; run by RWB-S2-E3006-APP | A case at ROUTE_APPROVED_SETTLEMENT; the reference rows that carry the range; the ALS payoff facts |
| TC-E3-006-02-ITG | Legacy AC2 of RWB-E3-006, the criterion this story owns: rule R-SET-01 — the payoff calculated from ALS, the range set from reference data and the case at PAYOFF_AND_RANGE_SET with one record naming R-SET-01 and its version (BR1, BR2, BR3, BR4) | Integration | ROUTE_APPROVED_SETTLEMENT; route approved with route = R2; the ALS payoff facts; the reference rows; one record naming R-SET-01 |
| TC-E3-006-03-ITG | Legacy AC3 of RWB-E3-006, asserted through the owner: the record cannot be written, nothing changes and MSG-P7-003 is returned (BR5) | Integration; run by RWB-S2-E3006-APP | Decision record stubbed unavailable; MSG-P7-003 |
| TC-E3-006-04-ITG | Legacy Access case of RWB-E3-006: a role without the Treatment and offer C right is refused with MSG-P4-002 | Integration | A role without the right; refused with MSG-P4-002 |
| TC-E3-006-05-ITG | Legacy Principle 5 case of RWB-E3-006: no business value in code, no personal data in events or logs, no read of another service's tables (BR2, BR6) | Component | Events and reports scanned for personal data; every read through an owner's contract |
| TC-E3-006-06-ITG | AC4 (BR7, new): the range the officer may move within is present for the case from reference data; the harness asserts only that the range exists. Test design: Not specified in the source documents (NEWAC-RWB-ITG-E3006-ITG-AC4) | Integration | A case at PAYOFF_AND_RANGE_SET; the reference rows that carry the range |
| TC-E3-006-07-ITG | AC5 (new): a consumed event delivered twice moves the case once. Test design: Not specified in the source documents (NEWAC-RWB-ITG-E3006-ITG-AC5) | Integration | ROUTE_APPROVED_SETTLEMENT; route approved event delivered twice |
| TC-E3-006-08-ITG | AC6 (new): a consumed call that fails leaves the case at ROUTE_APPROVED_SETTLEMENT with no decision record written. Test design: Not specified in the source documents (NEWAC-RWB-ITG-E3006-ITG-AC6) | Integration | ROUTE_APPROVED_SETTLEMENT; the owner's contract call stubbed to fail |
| TC-E3-006-09-ITG | AC7 (new): a status change the model does not allow is refused; the case stays in its current state with no decision record written. Test design: Not specified in the source documents (NEWAC-RWB-ITG-E3006-ITG-AC7) | Integration | ROUTE_APPROVED_SETTLEMENT; a status change the model does not allow requested |

The five cases above are the ITG copies of the legacy cases TC-E3-006-01 to TC-E3-006-05 and carry the legacy data unchanged; the component copy keeps the legacy level. TC-E3-006-02-ITG is the copy that covers AC2, the criterion this story owns; TC-E3-006-01-ITG and TC-E3-006-03-ITG observe the criteria RWB-S2-E3006-APP owns through the owners' contracts. The full test, with its Given, When and Then, is in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under the legacy test case IDs TC-E3-006-01 to TC-E3-006-05.

### 17. Guardrails

- No business value in code: the rule versions, the data product and list codes, the seeding set, the eligible states and the range itself are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-07), and the ALS payoff facts are ACE's, read through rwb-source-data's products contract (DP-05).
- The Workbench holds no payoff copy (legacy RWB-E3-006; REQ-RDF-002), so the harness fails a run that finds a re-keyed figure behind a state it asserts.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a treatment, case, range or decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-004 | Settlement terms are negotiated inside a rule-set range, and anything outside the range needs approval | Business Requirements Program v5, section 5.9 | FEAT-TRT-06 | D6, treatment and settlement | R-SET-01 | TC-E3-006-01-ITG, TC-E3-006-02-ITG |
| REQ-RDF-002 | Account balance, arrears, payments and classification are read from ACE through the views, current to the latest completed ACE batch | Business Requirements Program v5, section 5.1 | FEAT-TRT-06 | D6, treatment and settlement | R-SET-01 | TC-E3-006-02-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-TRT-06 | D6, treatment and settlement | R-SET-01 | TC-E3-006-02-ITG, TC-E3-006-03-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program v5, section 5.7 | FEAT-TRT-06 | D6, treatment and settlement | R-SET-01 | TC-E3-006-03-ITG |

### 19. Out of scope

- AC1 and AC3 of the legacy key, and the whole rwb-treatment behaviour, which are owned by RWB-S2-E3006-APP.
- The rwb-treatment contract baseline, which is RWB-S2-E3006-CON.
- The ACE data product build behind the ALS payoff facts, which are the P1 stories.
- The affordability pre-assessment that precedes this step, which is RWB-E3-005.
- The offer, the validity timer and the booking that follow this step, which are RWB-E3-007 to RWB-E3-010.
- Any production screen, endpoint, event, workflow, schedule or table: this story builds a test harness and its evidence only.
