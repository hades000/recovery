# RWB-ITG-E4001-ITG Order an appraisal when the last one is stale

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E4001-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E4001-ITG-16); the squad sizes the story at refinement |
| Depends on (build) | RWB-S1-E4001-APP (not done yet; see Integration dependencies) |
| Contract dependencies | Valuation and payoff contract with its fake, published ahead of wave 3; the only E3 dependency this service creates. Contract story: Not specified in the source documents (DOR-RWB-ITG-E4001-ITG-21) |
| Reference data | 12-month appraisal age limit parameter: Not specified in the source documents (DOR-RWB-ITG-E4001-ITG-20). Reference-data contract: DP-06, DP-07 |
| Open values | Not specified in the source documents (GAP-0436, GAP-0429, GAP-1683, GAP-2587). Harness values, SVAF interface, data product code, staleness parameter and operation names are agreed at the wave 3 entry check with the integration and QA leads |
| Contract version | Not specified in the source documents (DOR-RWB-ITG-E4001-ITG-23) |
| Integration dependencies | RWB-S1-E4001-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-001 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E4001-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 15 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want **one repeatable cross-service harness that drives the route assessment on a case whose appraisal is older than the limit, proves that the order to SVAF leaves the Workbench through rwb-integration with no person involved, and proves that the decision record carrying the rule version is written with it, against the owning services' published contracts and their fakes**, so that **the unattended re-appraisal path is shown to work end to end before the wave opens, and a stale appraisal can never leave a case at the route decision with no order raised and nothing recorded**.

### 2. Business rationale

A route chosen on an appraisal that is older than the policy limit values the security on a stale number, and an order raised without its decision record is a state the bank cannot defend at audit. The same case can also be ordered twice when the age check is applied in two places and neither sees the other. The rule exists to remove that: an appraisal older than 12 months raises a valuation order to SVAF with no person asking (Temporal and Drools Design slide 17, "Appraisal stale after 12 months"; REQ-S1-001).

Proving the rule is not the work of one service. The appraisal number, value, type and date are ACE's and reach the case through rwb-source-data's data product over `v_ace_valuation`, with the Workbench's acceptance held in `valuation_ext` (REQ-RDF-004; D-RCV-35 U1 and U4). The age check and the order are S1 rwb-valuation's, in RouteDecisionWorkflow on the rwb-valuation queue. The order leaves as an outbound item of rwb-integration, logged, retried and placed in an exception queue after the retry limit (REQ-DRI-007). The record that cites the rule and its version is written with the state change in one transaction and reaches the ledger through `rwb.decision-record.v1` (REQ-DRI-001; R-UNI-39). The case state while the appraisal is outstanding is rwb-case's. That chain crosses six services and three call types, so a defect at any hop appears as an order never sent, an order sent twice, or a decision with no record behind it.

This story owns the harness that proves the chain as the legacy key describes it, carrying AC1 of RWB-E4-001 into evidence. It serves REQ-S1-001, REQ-RDF-004, REQ-DRI-007 and REQ-DRI-001, and it carries FEAT-VAL-01 into evidence. AC2 of the same legacy key, the refusal when the decision log cannot be written, is owned by the app story RWB-S1-E4001-APP and is exercised here only as the negative path of the loop.

The harness is decoupled the same way the services are. It owns no schema and reads no other service's table (DP-01): the appraisal and its acceptance come from rwb-source-data's data product (DP-05), the order and its delivery from rwb-integration, the case state from rwb-case, the record from rwb-decision. It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13), one hop per call with a 2 s budget and a circuit breaker per downstream, and it calls the gateway-bff composite route where a screen would (DP-19). The record is read from rwb-decision's contract and the shared topic rather than from a local log table (DP-03).

### 3. Preconditions

- The published contracts of rwb-valuation, rwb-source-data, rwb-integration, rwb-case, rwb-decision and rwb-access are in the contract registry, and a stub set is generated from each published OpenAPI or AsyncAPI document with its version pinned.
- A case is seeded through the owning services' published operations only, with one asset whose appraisal in `v_ace_valuation` is older than the 12-month limit, and the case is at the route decision (Temporal and Drools Design slide 17).
- The acceptance of that appraisal and the stale flag are read from `valuation_ext` through rwb-source-data's data product, not from a copy of the harness's own (REQ-RDF-004; DP-05).
- The SVAF order is modelled by the interface config on rwb-integration and, where the configured interface is a file, by an outbound fixture. The interface ID, the transport, the order-file layout and the test endpoint are not specified in the source documents (GAP-0429; ASM-0605).
- The data product code that carries `v_ace_valuation` and `valuation_ext` records, the parameter name that holds the 12-month limit and the harness environment specification are not specified in the source documents (GAP-0429; ASM-0605).
- The S1 route package is Phase 2 (Temporal and Drools Design slide 17, "No S1 package yet (Phase 2)"), so no S1 rule ID is in force and none is asserted by the harness; the harness asserts the rule ID and version that the owning service records.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for a role that holds the right and for a role that does not.
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run and the rwb-valuation fake replaced by the real service when RWB-S1-E4001-APP lands.

### 4. Flow

1. Harness: seeds the case and its asset through the owning services' published operations only, with one appraisal older than the 12-month limit; the seeding set and the environment are not specified in the source documents (GAP-0429; ASM-0605).
2. Harness: reads the appraisal row through `GET /api/recovery/source-data/v1/data-products/{productCode}/records`, asserting the appraisal number, value, type and date, and the acceptance and stale flag held in `valuation_ext` (DP-05). The product code is not specified in the source documents (GAP-0429; ASM-0605).
3. Harness: triggers the route assessment with `POST /api/recovery/valuation/v1/cases/{caseId}/route` on the rwb-valuation base, which starts RouteDecisionWorkflow on queue rwb-valuation; the request carries no person's identity, because the rule runs unattended.
4. Harness: asserts the order as an interface run through `GET /api/recovery/integration/v1/interface-runs`, naming the case and the appraisal it replaces, and asserts that exactly one order exists for the case.
5. Harness: asserts the case state while the appraisal is outstanding through `GET /api/recovery/case/v1/cases/{caseId}`, and that the state is the owner's and not the harness's.
6. Harness: reads `GET /api/recovery/decision/v1/decision-log` and asserts one record for the order, carrying the rule ID and the rule version the owner recorded, and asserts nothing else moved on the case in the same step.
7. Harness: subscribes to `rwb.integration.events.v1` and asserts `rwb.integration.FileDelivered.v1` where the configured SVAF interface is a file, and `rwb.integration.FileFailed.v1` where the order fails, which fails the run (REQ-DRI-007).
8. Harness: subscribes to `rwb.decision-record.v1` and asserts that the record reaches the ledger within 5 minutes, keyed by the case, with no personal data on it (DP-03).
9. Harness: repeats the same route assessment on the same case with the same Idempotency-Key and asserts that exactly one order exists for it, because every POST carries an Idempotency-Key and a repeat of the same command creates no second effect (Architecture v5 slide 11).
10. Harness: repeats the run with the decision log forced to fail and asserts that nothing moves: no order, no case state change, and the message the owner returns. This is the negative path of AC2, whose criterion belongs to RWB-S1-E4001-APP.
11. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a role that does not hold the right.
12. Harness: publishes one evidence report per story and business date, naming the criterion, the assertions, the contract versions and whether each hop was a stub or the owner. The evidence format is not specified in the source documents (GAP-0429; ASM-0605).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The appraisal row read from the data product does not carry the age the seed placed there | The run fails and the report names the appraisal number, the date and the flag | None | AC1 |
| X3 | The route assessment returns no order for a stale appraisal | The run fails on AC1 and the report names the case and the appraisal | None | AC1 |
| X4 | More than one order exists for one assessment and one Idempotency-Key, or the repeat of the same command creates a second order | The run fails on AC1 and the report names the interface runs it found | None | AC1 |
| X5 | The decision record is missing, or its rule ID or rule version is absent | The run fails on AC1 and the report names the records it found | None | AC1 |
| X6 | `rwb.integration.FileFailed.v1` arrives for the order | The run fails and the report names the interface run and the failure the owner recorded | None | AC1 |
| X7 | The record does not reach `rwb.decision-record.v1` inside 5 minutes | The run fails on AC1 and the report names the record and its arrival time | None | AC1 |
| X8 | The decision log is forced to fail but the order or the case state still moves | The run fails on the negative path and the report names what moved | MSG-P7-003 | AC2 path, BR5 |
| X9 | A role that does not hold the right is authorised | The run fails on the access check and the report names the operation | MSG-P4-002 | AC3 |
| X10 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. Each message here is served from its owning service's catalogue; this service adds no message of its own, and the Thai and English wording is put through the message standard before wave 3 release. No S1 rule ID is in force for this feature, so the harness asserts the state, the data, the interface run and the record the owner writes, and names a message ID only where an owning service returns one. The order to SVAF is raised through rwb-integration, which owns the SVAF interface and its retries; the decision record carries the order date, the rule version and the limit applied.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-S1-E4001-APP |
| Negotiable | The SVAF order fixture, the data product code, the limit's parameter name and the report shape are configuration agreed at the wave entry check, not business values in code |
| Valuable | The unattended re-appraisal order and its record are proven end to end before wave 3 opens |
| Estimable | One harness runner, one stub set, one interface fixture, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-S1-E4001-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Order an appraisal when the last one is stale

  Background:
    Given the appraisal of the seeded asset is older than the 12-month limit
    And the case is at the route decision
    And the contract fakes of section 12.8 are published with their versions pinned

  Scenario: AC1 Order an appraisal when the last one is stale (legacy RWB-E4-001 AC1)
    Given the data and the rule version this feature needs are in place
    When RouteDecisionWorkflow runs the appraisal-age check as the decision starts, is reopened or an appraisal arrives
    Then checks the appraisal age against the limit and raises the order to SVAF with no person involved
    Then the system writes the result to the decision log with the rule version

  Scenario: AC3 A role without the right is refused access (new, D-RCV-60)
    Given a role that does not hold the right to order the appraisal
    When it is authorised for the order
    Then the access check fails and MSG-P4-002 is returned, and the report names the operation

  Scenario: AC4 A consumed call that fails or does not answer fails the run (new, D-RCV-60)
    Given a consumed call to a fake or a real service fails or does not answer
    When the run reaches that call
    Then the run fails at that hop and the report names the service and the operation

  Scenario: AC5 A status change the model does not allow is refused (new, D-RCV-60)
    Given the case or the order is at a status from which the model does not allow the change
    When the change is requested
    Then the change is refused and the state does not move
```

AC2 of the legacy key ("Not recorded") is owned by RWB-S1-E4001-APP and is not restated here; the harness exercises it only as the negative path of the same loop, in step 10 of section 4 and in TC-E4-001-02-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An appraisal older than the policy limit of 12 months triggers a valuation order with no person asking for it | REQ-S1-001; Temporal and Drools Design slide 17 |
| BR2 | The Workbench holds no appraisal copy: the appraisal number, value, type and date are ACE's and are read through `v_ace_valuation`; the acceptance is read from `valuation_ext` through the rwb-source-data data product, and the age and the stale flag are computed per assessment and recorded in the decision record with the limit version, with no column of this service written | REQ-RDF-004; D-RCV-35 U1 and U4; DP-05 |
| BR3 | Every order is an outbound item through rwb-integration, logged, retried on a defined schedule and placed in an exception queue after the retry limit | REQ-DRI-007 |
| BR4 | The decision record carries the rule and its version, and it is written with the state change in one transaction | REQ-DRI-001; R-UNI-39 |
| BR5 | No action proceeds if its decision record cannot be written | REQ-DRI-005; R-UNI-39 |
| BR6 | A POST carries an Idempotency-Key, and a repeat of the same command creates no second order | Architecture v5 slide 11 |
| BR7 | No person is in the loop for the order: nothing in the path waits for a person's action | Legacy RWB-E4-001 AC1 |

The S1 route package is Phase 2 (Temporal and Drools Design slide 17, "No S1 package yet (Phase 2)"), so no S1 rule ID is asserted here; the harness asserts the rule ID and version the owning service records and fails the run when either is absent.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Route decision | ROUTE_ASSESSMENT_TRIGGERED | `stale_flag` = Y, appraisal older than 12 months | VALUATION_ORDERED, with the order raised |
| VALUATION_ORDERED | FAST_LANE_SELECTED | lead_rank in the top 10% | AWAITING_VALUER (R-DIL-07) |
| AWAITING_VALUER | VALUATION_RECEIVED | report attached and value extracted | VALUATION_RECEIVED (R-DIL-09) |
| VALUATION_RECEIVED | VALUE_ACCEPTED | the case owner accepts the value | VALUATION_ACCEPTED (R-DIL-09) |
| AWAITING_VALUER | VALUER_SLA_BREACHED | order_age past the panel service level | AWAITING_VALUER, escalated and the order re-allocated (R-DIL-11) |

The state names and the transitions are the owner's, taken from R-DIL-07 to R-DIL-11 and from the route decision of D6. rwb-valuation holds VALUATION_ORDERED, AWAITING_VALUER, VALUATION_RECEIVED and VALUATION_ACCEPTED, and the appraisal is received in the Workbench only after ACE has ingested the SVAF result. The harness changes none of these states itself: it triggers the assessment through the rwb-valuation contract and then asserts what the owner reached, naming the owner and the operation behind each move in the report.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT, roles with Treatment and offer U | Trigger the route assessment and read the order, the case state and the decision record through the owners' contracts |
| RW-CASEOWN, RW-TEAMMGR, roles with Treatment and offer R | Read the same journey evidence |
| QA lead | Owns the harness configuration, the SVAF order fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-valuation, rwb-integration, rwb-source-data, rwb-case, rwb-decision and rwb-access make every change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the order is raised by the rule, not by a person |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date | Read, through the rwb-source-data data product (DP-05) |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | valuation_key, accepted, accepted_at, accepted_by, stale_flag, age_days | Read, through the rwb-source-data data product (DP-05) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract |
| DF-CAS-001 to DF-CAS-023 | recovery_case | status, and the case identity the order is keyed by | Read, through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The harness owns no table and writes no row directly: every read and every seed goes through the API of the owning service (DP-01, DP-05), and the appraisal itself is ACE's, so the Workbench records only its acceptance and its order.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/valuation/v1/cases/{caseId}/route` | S1 rwb-valuation | Trigger the route assessment that checks the appraisal age and raises the order (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The appraisal row from `v_ace_valuation` and the acceptance fields in `valuation_ext` (AC1, DP-05) |
| GET | `/api/recovery/integration/v1/interface-runs` | P2 rwb-integration | The SVAF order as an interface run (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state while the appraisal is outstanding (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record with the rule ID and version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope check, including the refusal path |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream (DP-13). Where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). The `{productCode}` that carries `v_ace_valuation` and `valuation_ext` records is not specified in the source documents (GAP-0429; ASM-0605). No operation is invented in this story. The six consumed rows are built against their documents and fakes, and their operation names stay a placeholder until the owners publish them before the wave 3 tag (GAP-2590). The business-key path POST /assets/{assetKey}/valuations is the current valuation path and the id-keyed POST /assets/{assetId}/valuations is superseded; the service owner confirms this at the tag, and the order itself is read as the SVAF interface run (GAP-2588).

#### 12.3 Events published

None. The harness publishes no Kafka event; it triggers the route assessment through the rwb-valuation contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The SVAF order delivered, where the configured interface is a file (AC1) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | A failed order, which fails the run (AC1) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through its own local decision-record library | The record reaches the ledger within 5 minutes (AC1, DP-03) |

All three carry IDs and business facts only, keyed by caseId, and the harness asserts that no personal data is present.

#### 12.5 Workflows and activities

None added. The harness exercises RouteDecisionWorkflow on queue rwb-valuation, which checks the appraisal age and raises the order, and CaseWorkflow on queue rwb-case, which holds the case while the appraisal is outstanding, and asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story. The appraisal-age check runs as a step of RouteDecisionWorkflow when the decision starts, when it is reopened and when an appraisal arrives, and no Temporal Schedule is added until the job map gives this service one (GAP-1686).

#### 12.6 Schedules

None added. The trigger is the route assessment and not a Schedule, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the appraisal is ACE's, read through rwb-source-data's contract (DP-05), the order belongs to rwb-integration, the case to rwb-case and the record to rwb-decision.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-valuation | `POST /cases/{caseId}/route` | Day-1 run of AC1 and of the second-assessment path before RWB-S1-E4001-APP is live |
| Stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the appraisal and its acceptance |
| Stub for rwb-integration | `GET /interface-runs`, `rwb.integration.events.v1` | Day-1 assertions on the SVAF order, its delivery and its failure |
| Stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertions on the case state while the appraisal is outstanding |
| Stub for rwb-decision | `GET /decision-log` | Day-1 assertion of the record with the rule ID and version |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |

Each fake is generated from the published OpenAPI or AsyncAPI document of its service, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The SVAF order fixture, the data product code, the parameter name for the limit and the evidence format are not specified in the source documents (GAP-0429; ASM-0605).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 6 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s timeout and a circuit breaker per downstream (DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` and `rwb.decision.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | Exercised only: RouteDecisionWorkflow on queue rwb-valuation and CaseWorkflow on queue rwb-case; none added |
| File | Only where the configured SVAF interface is a file, modelled by the outbound fixture |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependency is the one I story, RWB-S1-E4001-APP: until it is live the run uses the rwb-valuation stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| StaleAppraisalRunner | Job | Runs the owned criterion and the second-assessment path in order for a business date and holds the run lock |
| StubSet | Fake | The six stubs of section 12.8, each generated from the published contract with the version pinned |
| SvafOrderFixture | Fixture | The interface run on the configured SVAF interface and its delivery or failure, keyed by case and appraisal |
| EventProbe | Service | Consumes `rwb.integration.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the report keyed by story and business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, with one case at the route decision, one asset and one appraisal older than 12 months, and the acceptance and stale flag set through the owner's published operations. The environment, the seeding set, the data product code, the parameter name for the limit and the evidence retention are not specified in the source documents (GAP-0429; ASM-0605). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the six stubs from the published contracts, pin each version in the report and fail the run on a version mismatch (X1, X10).
2. Build the SvafOrderFixture and prove one interface run from creation to delivery for a business date (X6).
3. Build the StaleAppraisalRunner for AC1: read the appraisal and its acceptance through the data product, trigger the route assessment, assert the order as an interface run and the case state while it is outstanding (X2, X3).
4. Assert one record for the order through the rwb-decision contract, naming the rule ID and version, and fail where either is absent (X5).
5. Add the EventProbe for `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` and `rwb.decision.DecisionRecorded.v1`, and assert the key, the 5-minute arrival and the absence of personal data (X6, X7).
6. Add the second-assessment path and assert that no second order is raised for the same case (X4).
7. Add the negative path: force the decision log to fail, assert that nothing moves and record the message the owner returns (X8).
8. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a role that does not hold the right (X9).
9. Add the EvidenceReport and the gate, then swap the rwb-valuation stub for the real service when RWB-S1-E4001-APP lands and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it; the flag key is not specified in the source documents (GAP-0429; ASM-0605).

**Done when.** The tests of section 16 pass; the criterion passes against the fakes on Day 1 and again against rwb-valuation when RWB-S1-E4001-APP lands; and the wave entry check holds a report keyed by story and business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the order cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

No S1 rule ID is in force for this feature, so the harness asserts the state, the data, the interface run and the record, and names a message ID only where an owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-13 Route decision shows the states this journey sets:

| State | What the user sees and does |
|---|---|
| Loading | The route assessment is running; the appraisal age is being checked |
| Recommendation | The route is recommended on the expected return; a stale appraisal has raised the order and the case waits on the value |
| Overridden | The case owner has replaced the recommendation with reasons |
| Submitted | The route is submitted for its approval |
| Empty | Not specified in the source documents (CG-ALL-864) |
| Error | MSG-GEN-004 when the record was changed by someone else: Someone else changed this record. Reload it to see their change. MSG-P7-003 when the decision cannot be recorded |
| No access | MSG-P4-002 for an action outside the role's permission: You cannot {action} here. Your role does not include it. |

The harness renders no screen. It asserts the data behind SCR-13 through the owners' contracts and asserts the SVAF order as an interface run, so a passed run means the screen has the right data behind it. The gateway-bff composite route for SCR-13, and the harness evidence detail and its retention, are not specified in the source documents (GAP-0429; ASM-0605).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-001-01-ITG | AC1, BR1, BR2, BR3, BR4, BR6, BR7 | Integration | Case with an appraisal older than 12 months; SVAF order as an interface run |
| TC-E4-001-02-ITG | BR5 (negative path only); AC2 run by RWB-S1-E4001-APP | Integration | Decision log forced to fail; MSG-P7-003 |
| TC-E4-001-03-ITG | AC3, X9 | Component | A role without the right; MSG-P4-002 |
| TC-E4-001-04-ITG | Principle 5 | NFR | Forced decision-log write failure; nothing moves |
| TC-E4-001-05-ITG | AC4 | Integration | A consumed call that fails or does not answer; the report names the service and the operation |
| TC-E4-001-06-ITG | AC5 | Component | Case or order at a status the model does not allow; the state does not move |

The four ITG copies carry the legacy cases TC-E4-001-01 to TC-E4-001-04 unchanged. The full legacy tests are in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under those IDs.

### 17. Guardrails

- No business value in code: the 12-month limit's parameter name, the interface fixture, the seeding set and the result mappings are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the appraisal is ACE's, read through rwb-source-data's data product (DP-05).
- The Workbench holds no appraisal copy and writes no appraisal row; it records its acceptance in `valuation_ext` through the owner (REQ-RDF-004; D-RCV-35 U1 and U4).
- One hop and a 2 s timeout per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a case, appraisal, order or decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S1-001 | An appraisal older than the policy limit triggers a new valuation order without a person asking for it | Business Requirements Program v5, section 5.8 | FEAT-VAL-01 | D6 route decision (S1 valuation) | None in force (S1 package Phase 2) | TC-E4-001-01-ITG |
| REQ-RDF-004 | Appraisal values are available on the case through `v_ace_valuation`, and the Workbench's acceptance is held in `valuation_ext` | Business Requirements Program v5, section 5.1 | FEAT-VAL-01 | D6 route decision (S1 valuation) | R-DIL-07 to R-DIL-11 where relevant | TC-E4-001-01-ITG |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule and place failures in an exception queue | Business Requirements Program v5, section 5.2 | FEAT-VAL-01 | D6 route decision (S1 valuation) | None in force (S1 package Phase 2) | TC-E4-001-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-VAL-01 | D6 route decision (S1 valuation) | None in force (S1 package Phase 2) | TC-E4-001-01-ITG, TC-E4-001-02-ITG, TC-E4-001-04-ITG |

### 19. Out of scope

- AC2 of the legacy key, the refusal when the decision log cannot be written, which is owned by RWB-S1-E4001-APP; this story exercises it only as a negative path.
- The production valuation endpoints, RouteDecisionWorkflow on the rwb-valuation queue, the (absent) S1 Schedule and the `rwb_valuation` table, which are the S1 service stories of this legacy key.
- The contract baselines of the six services, which are their CON stories and are consumed here through the published documents and their fakes.
- The platform configuration: the decision-record library, the gateway-bff composite route, the feature-flag library and the observability set.
- The SVAF interface itself: its ID, transport, order-file layout, result codes and test endpoint, none of which a source read gives.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.
