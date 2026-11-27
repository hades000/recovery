# RWB-ITG-E3017-ITG Release the collateral after settlement

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E3017-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S2-E3017-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E3-017 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E3017-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **one repeatable cross-service journey harness that runs a settlement from clearance confirmed to the release instruction to CCMS, the case state COLLATERAL_RELEASE_REQUESTED, the single decision record that carries the rule version and the later CCMS confirmation, against the owning services' published contracts and their fakes**, so that **the release of the security is proven to leave the Workbench through rwb-integration and to be recorded before the case moves, and a settlement does not stall after the customer's money has cleared**.

### 2. Business rationale

A settlement that has cleared but never reaches CCMS leaves the customer's title held after the debt is paid, and a release instruction sent without its decision record is a state the bank cannot defend at audit. Both outcomes depend on one chain: the securities read from `v_ace_collateral` and `v_ace_collateral_detail`, the clearance fact that closes the settlement in rwb-treatment, the release instruction that leaves through rwb-integration's outbound interface to CCMS, the case state that rwb-case moves, and the decision record that rwb-decision holds with its rule version. That chain crosses five services and three call types, so a defect at any hop shows up as a title held after settlement or a case that moves with nothing behind it.

This story owns the harness that proves the chain as the legacy key describes it. It carries AC3 of RWB-E3-017, the R-SET-20 criterion, into evidence: clearance confirmed in state PAYMENT_CLEARED, the securities read from `v_ace_collateral`, the release requested, and the case at COLLATERAL_RELEASE_REQUESTED. The same loop is asserted on its two later facts, which the owning services drive and the harness observes: the R-SET-21 confirmation from CCMS returning the title and closing the treatment and the case, and the R-RES-33 close when the final installment has been paid, which ends PLAN_RUNNING at PLAN_COMPLETED. It serves REQ-S2-008, REQ-DRI-007, REQ-RDF-004, REQ-CHO-008 and REQ-DRI-001, and it carries FEAT-TRT-17 and its FEAT-CHO-08 dependency into evidence.

The harness is decoupled the same way the services are. It never reads another service's table (DP-01): the treatment and its state come from rwb-treatment, the outbound item and its delivery from rwb-integration, the case state from rwb-case, the decision record from rwb-decision and the securities from rwb-source-data, which owns the ACE view contract. It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13), and it calls through the gateway-bff composite route where a screen would (DP-19). Every call is one hop with a 2 s budget. The ACE collateral and account rows are read through rwb-source-data's products contract and not through a view of the harness's own (DP-05), and the decision record is read from rwb-decision and its shared topic (DP-03).

### 3. Preconditions

- The published contracts of rwb-treatment, rwb-integration, rwb-source-data, rwb-case, rwb-decision and rwb-access are in the contract registry, and a WireMock stub set is generated from each one and its version pinned.
- A journey case, its settlement treatment and its account are seeded through the owning services' published operations only. The seeding set, the harness environment specification and the fixture contents are not specified in the source documents (GAP-0426; ASM-0602).
- The case is at PAYMENT_CLEARED, the settlement treatment is approved and open, account `A-0001` carries a zero balance, and `v_ace_collateral` holds two active securities for it, all as the legacy key states them.
- CCMS is modelled by the outbound item on the interface config in rwb-integration and, where the configured interface is a file, by an outbound fixture. The interface code, the transport, the message or file layout and the test endpoint are not specified in the source documents (GAP-0426; ASM-0602).
- The rule package in force carries R-SET-20, R-SET-21, R-SET-22 and R-RES-33, and the version of each is readable on the decision record that cites it.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the case owner's role and for a caller outside the case scope.
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run, and the rwb-treatment fake replaced by the real service when RWB-S2-E3017-APP lands.

### 4. Flow

1. Harness: seeds the journey case, its settlement treatment at PAYMENT_CLEARED and its account `A-0001` through the owning services' published operations only; the seeding set and its environment are not specified in the source documents (GAP-0426; ASM-0602).
2. Harness: reads the securities through `GET /api/recovery/source-data/v1/data-products/DP06/records` and asserts two active securities for `A-0001`, the title detail read with them, and the zero balance read from `v_ace_account` through the same products contract (DP-05).
3. Harness: places the clearance confirmation on the settlement treatment with `PATCH /api/recovery/treatment/v1/treatments/{treatmentId}` and reads it back with `GET /api/recovery/treatment/v1/treatments/{treatmentId}`, proving the treatment close and the release instruction are the owner's and not the harness's. In production the same fact arrives as `rwb.payment.ProceedsMatched.v1` (EV-25) from rwb-payment, which CaseWorkflow forwards to the TreatmentWorkflow child on the rwb-treatment queue; the harness asserts that event too when the environment runs the payment match (JOB-07).
4. Harness: asserts the release instruction as an outbound item on the CCMS interface config through `GET /api/recovery/integration/v1/admin/outbound-items`, naming the case and the treatment, and its delivery through `GET /api/recovery/integration/v1/admin/outbox/deliveries`.
5. Harness: subscribes to `rwb.treatment.events.v1` and asserts `rwb.treatment.TreatmentClosed.v1` for the case, once for the path, and no personal data on it. Where the settlement treatment was approved before the run, it asserts `rwb.treatment.TreatmentApproved.v1` (EV-10) as the earlier fact on the same topic.
6. Harness: asserts the case state at COLLATERAL_RELEASE_REQUESTED through `GET /api/recovery/case/v1/cases/{caseId}`, and that the treatment reads closed at the same moment.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log` for the case and asserts exactly one record for the transition, naming R-SET-20 and its rule version, and asserts `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` for it.
8. Harness: asserts the R-SET-21 fact driven by the owning service: CCMS confirms the release, the title is returned, the treatment closes and the case reaches CASE_CLOSED_SETTLED, with one record naming R-SET-21 and its version. The confirmation input and its fixture are not specified in the source documents (GAP-0426; ASM-0602).
9. Harness: runs the second path of the same loop on a plan treatment at PLAN_RUNNING with `installments_paid` equal to `installments_due`, and asserts the R-RES-33 outcome as the owner's: the treatment closes, the collateral is released and the case reaches PLAN_COMPLETED, with one record naming R-RES-33 and its version.
10. Harness: asserts that where the configured CCMS interface is a file, `rwb.integration.FileDelivered.v1` carries the delivery and `rwb.integration.FileFailed.v1` carries a failure the run must not pass over.
11. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a caller outside the case scope.
12. Harness: publishes the per-run evidence report keyed by story and business date, with the criterion and its assertions, and gates the wave on the result. The evidence format and its retention are not specified in the source documents (GAP-0426; ASM-0602).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC3 |
| X2 | The clearance confirmation is not reflected on the treatment inside the run window | The run fails and the report names the treatment and the operation; the run is not marked passed | None | AC3 |
| X3 | No outbound item is created for the case and the treatment on the CCMS interface config | The run fails on AC3 and the report names the interface config and the treatment | None | AC3 |
| X4 | The outbound item stays undelivered, or `rwb.integration.FileFailed.v1` arrives | The run fails and the report names the outbound item and the failure the owner recorded | None | AC3 |
| X5 | The case does not reach COLLATERAL_RELEASE_REQUESTED | The run fails on AC3 and the report names the two states | None | AC3 |
| X6 | More or fewer than one decision record exists for the transition, or its rule version is missing | The run fails on AC3 and the report names the records it found | None | AC3 |
| X7 | The securities read from `v_ace_collateral` are not the two the case holds, or `in_active` is not false after the release recording | The run fails on AC3 and the report names the collateral number and the flag | None | AC3 |
| X8 | CCMS confirms the release but the treatment does not close, or the case does not reach CASE_CLOSED_SETTLED | The run fails on the R-SET-21 path and the report names the treatment and the case state | None | AC3 |
| X9 | The final installment path does not reach PLAN_COMPLETED, or the treatment or collateral stays open | The run fails on the R-RES-33 path and the report names the treatment and the case state | None | AC3 |
| X10 | A caller outside the case scope is authorised | The run fails on the access check and the report names the operation | None | AC3 |
| X11 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC3 |

The report text is for the wave entry check and is not part of the message standard. The rule set carries no message ID for R-SET-20, R-SET-21, R-SET-22 or R-RES-33, so the harness asserts state, data and the decision record and not a message; the business messages this journey can produce are in section 14 and belong to the owning services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-S2-E3017-APP |
| Negotiable | The CCMS interface fixture, the seeding set and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The release of the security after settlement, and its record, are proven end to end before the wave opens |
| Estimable | One harness runner, one stub set, one interface fixture, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-S2-E3017-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Release the collateral after settlement

  Background:
    Given account "A-0001" carries a zero balance and "v_ace_collateral" holds two active securities for it
    Given the rule package in force carries R-SET-20 and R-SET-21

  Scenario: AC3 Rule R-SET-20 (legacy RWB-E3-017 AC3)
    Given a case in state PAYMENT_CLEARED
    When clearance confirmed
    Then close the account in ALS and request the release of the securities read from v_ace_collateral
    Then the case moves to COLLATERAL_RELEASE_REQUESTED
```

AC1, AC2 and AC4 are owned by the app story of this legacy key, RWB-S2-E3017-APP, and are not restated here. AC3 is the cross-service criterion this ITG copy owns: the harness asserts it through the owners' contracts, and it asserts the two later facts of the same loop, the R-SET-21 confirmation and the R-RES-33 final-installment close, as observed facts in section 4 and section 16 rather than as new criteria.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | At PAYMENT_CLEARED with funds cleared, the Workbench closes the account in ALS and requests the release of the collateral, and the case moves to COLLATERAL_RELEASE_REQUESTED | R-SET-20; FEAT-TRT-17 |
| BR2 | At COLLATERAL_RELEASE_REQUESTED with CCMS confirming the release, the Workbench returns the title, closes the treatment and closes the case | R-SET-21 |
| BR3 | Where the title documents are not found, the case stays at COLLATERAL_RELEASE_REQUESTED and a task re-creates the title set before the release, inside 5 working days | R-SET-22 |
| BR4 | At PLAN_RUNNING with the final installment paid, the Workbench closes the treatment, releases the collateral and closes the case | R-RES-33 |
| BR5 | The securities are read from `v_ace_collateral` and its title detail; the Workbench records its own request and confirmation and writes no collateral row | Legacy RWB-E3-017; D-RCV-35 U1 and U4; REQ-RDF-004 |
| BR6 | The release leaves through the outbound interface to CCMS, and every outbound item is logged, retried on a defined schedule and placed in an exception queue after the retry limit | REQ-DRI-007 |
| BR7 | The decision record carries the rule and its version, and it is written with the state change in one transaction | REQ-DRI-001; R-UNI-39 |
| BR8 | No action proceeds if its decision record cannot be written | REQ-DRI-005; R-UNI-39 |
| BR9 | The booking and the settled balance are confirmed from the ACE account data for the next business date | REQ-CHO-008; FEAT-CHO-08 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PAYMENT_CLEARED | CLEARANCE_CONFIRMED | funds cleared | COLLATERAL_RELEASE_REQUESTED (R-SET-20) |
| COLLATERAL_RELEASE_REQUESTED | COLLATERAL_RELEASED | CCMS confirms the release | CASE_CLOSED_SETTLED (R-SET-21) |
| COLLATERAL_RELEASE_REQUESTED | TITLE_DOCUMENTS_MISSING | title documents not found | COLLATERAL_RELEASE_REQUESTED, with a task to re-create the title set (R-SET-22) |
| PLAN_RUNNING | FINAL_INSTALLMENT_PAID | installments_paid = installments_due | PLAN_COMPLETED (R-RES-33) |

The treatment and the case are the owners' state: rwb-treatment closes the treatment, and P3 moves the case status on the events the loop raises. The treatment close is published as `rwb.treatment.TreatmentClosed.v1` and the case move is read back through the rwb-case contract.

The harness changes no state itself. It seeds through the owning services' published operations, places the clearance fact on the treatment through the owner's contract, and then asserts the states the owners reached: PAYMENT_CLEARED to COLLATERAL_RELEASE_REQUESTED, COLLATERAL_RELEASE_REQUESTED to CASE_CLOSED_SETTLED, and PLAN_RUNNING to PLAN_COMPLETED. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT, case owner and restructuring roles with Treatment and offer C | Place the clearance fact on the treatment and read the treatment, its close and the release instruction through the rwb-treatment contract |
| RW-CASEOWN, RW-TEAMMGR and roles with Treatment and offer R | Read the same journey evidence, including the case state and the decision record |
| QA lead | Owns the harness configuration, the CCMS interface fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-treatment, rwb-integration, rwb-source-data, rwb-case, rwb-decision, rwb-access and rwb-payment make every state change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the settlement approval belongs to the treatment story |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | status (PAYMENT_CLEARED, COLLATERAL_RELEASE_REQUESTED, PLAN_COMPLETED, CASE_CLOSED_SETTLED) | Read, through the rwb-case contract |
| DF-TRT-001 to DF-TRT-014 | treatment | id, case_id, decision_log_id, treatment_type, plan installment counters, state | Read and write, through the rwb-treatment contract |
| DF-ACE-001 to DF-ACE-042 | v_ace_account | account_code, total_balance | Read, through the rwb-source-data products contract |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date, and the active flag `in_active` | Read, through the rwb-source-data products contract (DP06) |
| DF-ACE-196 to DF-ACE-207 | v_ace_collateral_detail | asset_key, title_doc_no, plot_no, area_text, province, lien_rank | Read, through the rwb-source-data products contract (DP06) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-OPS-169 to DF-OPS-175 | outbound_item | interface_id, idempotency_key, status | Read, through the rwb-integration admin operation |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The harness owns no table and writes no row directly: it reads and writes through the API of the owning service only (DP-01, DP-05), and the Workbench writes no collateral row, because ACE holds the release state (legacy RWB-E3-017; D-RCV-35 U1 and U4).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| PATCH | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Place the clearance confirmation on the settlement treatment (AC3) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Read the treatment, its close and its release state (AC3) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The release instruction as an outbound item on the CCMS interface config (AC3) |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | The delivery of that outbound item (AC3) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The two active securities and the title detail from DP06 Collateral and assets, and the zero balance (AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state at COLLATERAL_RELEASE_REQUESTED and CASE_CLOSED_SETTLED (AC3) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The single record for each transition, with R-SET-20, R-SET-21 or R-RES-33 and its version (AC3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and authority check for each call, including the refusal path (AC3) |

The zero balance is read from `v_ace_account` through the same products operation; the data product code that carries the account row is not named for this story in the source documents (GAP-0426; ASM-0602). Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-13); where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the clearance fact through the rwb-treatment contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | The settlement treatment was approved before the run (AC3) |
| `rwb.treatment.TreatmentClosed.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The treatment closed once for each path (AC3) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through the local decision-record library | The record written with the state change (AC3) |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The release instruction delivered, where the configured CCMS interface is a file (AC3) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The release instruction failed, where the configured CCMS interface is a file (AC3) |
| `rwb.payment.ProceedsMatched.v1` (EV-25) | `rwb.payment.events.v1` | P8 rwb-payment | The clearance fact in production, forwarded to the TreatmentWorkflow child by CaseWorkflow; asserted where the environment runs the payment match (AC3) |

All six carry IDs and business facts only, keyed by caseId and treatmentId, and the harness asserts that no personal data is present (DP-03, DP-09).

#### 12.5 Workflows and activities

None added. The harness exercises the existing TreatmentWorkflow settlement saga in rwb-treatment, which closes the treatment and raises the release instruction, and the CaseWorkflow in rwb-case, which forwards the clearance fact to the stage child and moves the case status, and asserts their effects through the services' contracts and the owner's topic. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. R-SET-20, R-SET-21, R-SET-22 and R-RES-33 are triggered by facts and not by a Schedule, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the treatment is rwb-treatment's, the interface config and outbound items are rwb-integration's, and the securities are ACE's, read through rwb-source-data's contract (DP-05).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-treatment | `PATCH /treatments/{treatmentId}`, `GET /treatments/{treatmentId}`, `rwb.treatment.events.v1` | Day-1 runs of AC3 and of the R-SET-21 and R-RES-33 paths before RWB-S2-E3017-APP is live |
| WireMock stub for rwb-integration | `GET /admin/outbound-items`, `GET /admin/outbox/deliveries`, `rwb.integration.events.v1` | Day-1 assertions on the release instruction and its delivery |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the two securities, the title detail and the zero balance |
| WireMock stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertions on COLLATERAL_RELEASE_REQUESTED, PLAN_COMPLETED and CASE_CLOSED_SETTLED |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record per transition with its rule version |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| Payment event stub | `rwb.payment.ProceedsMatched.v1` | The clearance fact where the environment does not run the payment match |
| CCMS outbound fixture | The outbound item on the configured CCMS interface | The release instruction and its confirmation, where the interface is a file |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The CCMS interface code and transport, the fixture contents and result codes, the data seeding set, the harness environment and the evidence format and retention are not specified in the source documents (GAP-0426; ASM-0602).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.treatment.TreatmentApproved.v1`, `rwb.treatment.TreatmentClosed.v1`, `rwb.decision-record.DecisionRecorded.v1`, `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` and `rwb.payment.ProceedsMatched.v1` consumed (DP-03, DP-09) |
| Temporal | None added; the TreatmentWorkflow settlement saga and the CaseWorkflow stage routing exercised |
| File | The CCMS outbound interface as a fixture, where the configured interface is a file |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays None. The blocking dependency is the one I story, RWB-S2-E3017-APP: until it is live the run uses the rwb-treatment stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour. The harness owns no schema (DP-01) and reads the treatment, the case, the outbound item, the securities and the decision record from their owners only. The decision record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). The two securities and their title detail are read through rwb-source-data's DP06 product, which owns the ACE view contract, and not through a view of the harness's own (DP-05). Every call sits on the owner's per-service base with a single hop (DP-13), and the composed reads a screen would make are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the owned criterion and its two later facts in order for a business date and holds the run lock |
| StubSet | Fake | The six WireMock stubs and the payment event stub, each generated from the published contract with the version pinned |
| CcmsInterfaceFixture | Fixture | The outbound item on the configured CCMS interface and its confirmation, keyed by case and treatment |
| EventProbe | Service | Consumes `rwb.treatment.events.v1`, `rwb.integration.events.v1`, `rwb.payment.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, on account `A-0001` with a zero balance and two active securities, one case at PAYMENT_CLEARED with its approved settlement treatment, and one case at PLAN_RUNNING with its plan installments due. The environment, the seeding set, the CCMS interface fixture and the evidence retention are not specified in the source documents (GAP-0426; ASM-0602). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the six stubs and the payment event stub from the published contracts, pin each contract version in the run report and fail the run on a version mismatch (X1, X11).
2. Build the CcmsInterfaceFixture and prove one outbound item from creation to delivery for a business date (X4).
3. Build the JourneyRunner for AC3: read the two securities and the zero balance, place the clearance fact on the treatment, assert the treatment close, the outbound item and the delivery, the case at COLLATERAL_RELEASE_REQUESTED and one record naming R-SET-20 with its version (X2, X3, X5, X6, X7).
4. Add the EventProbe for `rwb.treatment.TreatmentClosed.v1`, `rwb.treatment.TreatmentApproved.v1` and `rwb.decision-record.DecisionRecorded.v1` and assert the key and the absence of personal data.
5. Add the R-SET-21 path: the CCMS confirmation, the title returned, the treatment closed and the case at CASE_CLOSED_SETTLED, with one record naming R-SET-21 (X8).
6. Add the R-RES-33 path: a plan treatment at PLAN_RUNNING with `installments_paid` equal to `installments_due`, the treatment closed, the collateral released and the case at PLAN_COMPLETED, with one record naming R-RES-33 (X9).
7. Add the file events `rwb.integration.FileDelivered.v1` and `rwb.integration.FileFailed.v1` for the configured CCMS interface and assert that a failure fails the run (X4).
8. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller outside the case scope (X10).
9. Add the EvidenceReport and the gate, then swap the rwb-treatment stub for the real service when RWB-S2-E3017-APP lands and rerun the criterion and its two later facts.

**Feature switch.** The legacy key names no feature switch for this behaviour. The journey runs behind the platform feature-flag library as the wave releases it; the flag key for this harness is not specified in the source documents (GAP-0426; ASM-0602).

**Done when.** The tests of section 16 pass for AC3 and for the two later facts of the loop; the criterion passes against the fakes on Day 1 and again against rwb-treatment when RWB-S2-E3017-APP lands; and the wave entry check holds a run report keyed by story and business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the transition cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-SET-20, R-SET-21, R-SET-22 and R-RES-33 carry no message ID in the rule set, so the harness asserts the state, the data and the decision record and names the message ID only where the owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-14 Treatment record (built in RWB-S2-E3017-APP) and SCR-15 Settlement offer show the states this journey sets:

| State | What the user sees and does |
|---|---|
| Draft | The settlement treatment is being prepared; no release fact exists |
| Submitted | The settlement is with its approver; no release fact exists |
| Approved | The settlement treatment is approved and waits for clearance |
| Booked | The clearance is confirmed, the account is closed in ALS and the release instruction has left, or the title has been returned and the treatment is closed |
| Broken | A title document is missing and a task re-creates the title set before the release (R-SET-22) |

The case states COLLATERAL_RELEASE_REQUESTED, PLAN_COMPLETED and CASE_CLOSED_SETTLED are read through the rwb-case contract and shown on the case record view, whose screen ID is not named for this feature in the source documents (GAP-0426; ASM-0602). SCR-14 shows Draft, submitted, approved, booked and broken; SCR-15 shows Draft, below floor, approved, sent and accepted.

The harness renders no screen. It reads these states through the rwb-treatment, rwb-case, rwb-integration and rwb-source-data contracts, so a passed run means the screens have the right data behind them. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0426; ASM-0602).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-017-01-ITG | AC1 | Integration | Account `A-0001`; two active securities; release instruction to CCMS |
| TC-E3-017-02-ITG | AC2, BR4 | Integration | PLAN_RUNNING; installments_paid = installments_due |
| TC-E3-017-03-ITG | AC3, BR1, BR2, BR5, BR6 | Integration | PAYMENT_CLEARED; clearance confirmed; account `A-0001` with a zero balance and two active securities; `in_active` false after the recording |
| TC-E3-017-04-ITG | AC4, BR8 | Integration | Decision log stubbed unavailable; MSG-P7-003 |
| TC-E3-017-05-ITG | Access | Component | A role without the right; refused with MSG-P4-002 |
| TC-E3-017-06-ITG | Principle 5 | NFR | Decision log write forced to fail; no treatment, collateral or case state changes |

The integration cases above are the ITG copies of the legacy cases TC-E3-017-01 to TC-E3-017-06 and carry the legacy data unchanged; the component and NFR copies keep the legacy levels. TC-E3-017-03-ITG is the copy that covers AC3, the criterion this story owns, and it carries the R-SET-21 and R-RES-33 assertions of section 4 as the same loop. The full test, with its Given, When and Then, is in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under the legacy test case IDs TC-E3-017-01 to TC-E3-017-06.

### 17. Guardrails

- No business value in code: the rule versions, the CCMS interface fixture, the seeding set, the eligible states and the result code mappings are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the securities are ACE's, read through rwb-source-data's DP06 product (DP-05).
- The Workbench writes no collateral row; the release state is ACE's, and the Workbench records its own request and confirmation (legacy RWB-E3-017; D-RCV-35 U1 and U4).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a treatment, case, collateral or decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program v5, section 5.9 | FEAT-TRT-17 | D6.4 Settlement | R-SET-20, R-SET-21, R-RES-33 | TC-E3-017-01-ITG, TC-E3-017-02-ITG, TC-E3-017-03-ITG |
| REQ-DRI-007 | The integration adapters log every outbound file, retry on a defined schedule and place failures in an exception queue | Business Requirements Program v5, section 5.2 | FEAT-TRT-17 | D6.4 Settlement | R-SET-20, R-SET-21 | TC-E3-017-01-ITG, TC-E3-017-03-ITG |
| REQ-RDF-004 | Collateral records and appraisal values are read through `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_valuation` | Business Requirements Program v5, section 5.1 | FEAT-TRT-17 | D6.4 Settlement | R-SET-20 | TC-E3-017-03-ITG |
| REQ-CHO-008 | Booked terms are recorded on the case and the booking is confirmed from the next business date's ACE account data | Business Requirements Program v5, section 5.3 | FEAT-TRT-17; FEAT-CHO-08 | D6.4 Settlement | R-RES-33 | TC-E3-017-02-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-TRT-17 | D6.4 Settlement | R-SET-20, R-SET-21, R-RES-33 | TC-E3-017-03-ITG, TC-E3-017-06-ITG |

### 19. Out of scope

- AC1, AC2 and AC4 of the legacy key, which are owned by RWB-S2-E3017-APP.
- The rwb-treatment behaviour itself: the settlement offer, its approval, the plan timers and the treatment record are the service story RWB-S2-E3017-APP.
- The rwb-integration interface build, the outbound item lifecycle and the retry and exception queue, which are the P2 stories of the same interface.
- The CCMS interface code, transport, message or file layout and test endpoint, none of which a source read gives.
- The other release triggers of the same rules: the asset-proceeds close (R-UNI-48, S5 asset disposal) and the deed-in-lieu transfer release (R-DIL-27, S2), each of which has its own journey.
- Any production screen, endpoint, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.
