# RWB-ITG-E4002-ITG Receive the appraisal value from SVAF

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E4002-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement (DOR-RWB-ITG-E4002-ITG-16) |
| Depends on (build) | RWB-S1-E4002-APP (not done; AC1 runs on the WireMock stub until it is live) |
| Contract dependencies | None |
| Integration dependencies | RWB-S1-E4002-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-002 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E4002-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want one repeatable cross-service harness that runs the appraisal step of the D6 route decision from the ACE ingestion of the SVAF result to the case owner's acceptance and the decision record that names the rule and its version, against rwb-valuation's published contract and the fakes of the services it reads, so that the value a route is chosen on is proven to be ACE's own appraisal read through the owning contract, the Workbench's acceptance of it is proven to be the Workbench's own record, and the route moves only when the record is written.

### 2. Business rationale

The route decision is only as good as the value behind it. The Workbench loads no SVAF file and holds no copy of the appraisal: ACE ingests the SVAF feed, and the Workbench reads the appraisal number, value, type and date from `v_ace_valuation` for the asset business key, then keeps its own judgement about that appraisal, the acceptance, the stale flag and the age, in `valuation_ext` against the `valuation_key` (REQ-RDF-004; D-RCV-35 U1 and U4; DP-05). Two owners therefore stand behind one number, ACE for the value and the Workbench for its acceptance of it, and a defect in the seam between them shows up as a route priced on a stale or absent appraisal.

The step crosses four services and two call types. rwb-valuation owns the route decision and its `RouteDecisionWorkflow`; rwb-source-data owns the ACE view contract and the extension tables, `valuation_ext` among them; rwb-case holds the case state at the moment of the assessment; rwb-decision holds the central ledger that the record reaches within 5 minutes; and rwb-access answers the role and scope question, including the refusal. The harness proves that chain as the legacy key describes it, and it carries AC1 of RWB-E4-002 into evidence: appraisal `AP-0001` for asset `AST-0001` at appraisal date 2026-11-02 with appraised value 4250000, read for the asset key, accepted against the valuation key, and logged with the rule version.

The harness is decoupled the same way the services are. It owns no schema and never reads another service's table (DP-01): the appraisal and the acceptance fields come from rwb-source-data's products contract, the route assessment from rwb-valuation, the case state from rwb-case and the record from rwb-decision. It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base (DP-13), it calls the gateway-bff composite route where a screen would (DP-19), and it reads and asserts the decision record through the local decision-record library's topic and the central ledger (DP-03). Every call is one hop with a 2 s budget.

### 3. Preconditions

- The published contracts of rwb-valuation, rwb-source-data, rwb-case, rwb-decision and rwb-access are in the contract registry, and a WireMock stub set is generated from each one and its version pinned.
- A case, its asset and its collateral link are seeded through the owning services' published operations only. Not specified in the source documents (GAP-0430; ASM-0606): the wave 3 harness pack, its environment and its seeding set.
- ACE has ingested the SVAF appraisal `AP-0001` for asset `AST-0001` at appraisal date 2026-11-02, and `v_ace_valuation` holds appraised value 4250000 for that asset key, as the legacy key states them.
- Not specified in the source documents (GAP-0430; ASM-0606): the data product code that carries `v_ace_valuation` and `valuation_ext`, and the internal operation and field details through which the route assessment records the acceptance; who writes the fields is open between P1 and S1 (`ownership.json` ruling ASM-0081; FSD P1 OQ-P1-05).
- No S1 rule package is in force in Phase 1 (Temporal and Drools Design Text Extract v1 slide 17 states "No S1 package yet (Phase 2)"), so the harness asserts the rule ID and version that the owning service records and fails the run when either is absent.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the case owner's role and for a caller outside the case scope.
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run, and the rwb-valuation fake replaced by the real service when RWB-S1-E4002-APP lands.

### 4. Flow

1. Harness: seeds the case, its asset `AST-0001` and the collateral link through the owning services' published operations only. Not specified in the source documents (GAP-0430; ASM-0606): the seeding set and its environment.
2. Harness: consumes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` and asserts that the ACE batch carrying the SVAF appraisal is ready for the business date, with no personal data on the event.
3. Harness: reads the appraisal through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` and asserts appraisal number `AP-0001`, appraisal type, appraised value 4250000 and appraisal date 2026-11-02 for the asset key, and the acceptance fields `accepted`, `stale_flag` and `age_days` in `valuation_ext` against the `valuation_key` (DP-05). Not specified in the source documents (GAP-0430; ASM-0606): the product code.
4. Harness: triggers the route assessment with `POST /api/recovery/valuation/v1/cases/{caseId}/route`, which is the owner's step in which the appraisal is read and accepted, and never sets an appraisal or an acceptance value itself.
5. Harness: reads the case state at the route decision through `GET /api/recovery/case/v1/cases/{caseId}`, and asserts the state the owner reached with the assessment.
6. Harness: reads the acceptance back through the same products operation and asserts `accepted`, `stale_flag` and `age_days` for the `valuation_key`, including that an appraisal older than the 12-month policy limit reads stale (REQ-S1-001). Who writes `accepted`, `accepted_at` and `accepted_by` in `valuation_ext` is open between P1 and S1 (`ownership.json` ruling ASM-0081; FSD P1 OQ-P1-05), so the harness asserts the fields through the P1 data product and the S1 route assessment and never writes them.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log` for the case and asserts exactly one record for the assessment, naming the rule ID and its rule version, and asserts the freshness of the data the decision used (REQ-RDF-009).
8. Harness: subscribes to `rwb.decision-record.v1` and asserts `rwb.decision.DecisionRecorded.v1` for the case within 5 minutes, carrying IDs and business facts only.
9. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a caller outside the case scope.
10. Harness: publishes one evidence report keyed by story and business date, with the criterion and its assertions, and gates the wave on the result. Not specified in the source documents (GAP-0430; ASM-0606): the evidence format and its retention.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | No `AceDataReady` event arrives for the business date, or the appraisal is not visible for the asset key | The run fails and the report names the business date, the asset key and the product code used | None | AC1 |
| X3 | The appraisal number, value, type or date read for the asset key is not the one ACE ingested | The run fails on AC1 and the report names both sets of values | None | AC1 |
| X4 | The route assessment is accepted but the acceptance fields are not set in `valuation_ext` against the `valuation_key` | The run fails on AC1 and the report names the valuation key and the fields it read | None | AC1 |
| X5 | `age_days` reads inside the 12-month policy limit while the appraisal date is older than it, or the stale flag contradicts the age | The run fails on AC1 and the report names the appraisal date, the age and the flag | None | AC1 |
| X6 | More or fewer than one decision record exists for the assessment, or its rule ID or rule version is missing | The run fails on AC1 and the report names the records it found, and states that no S1 package is in force in Phase 1 | None | AC1 |
| X7 | `DecisionRecorded` does not reach the shared topic inside the 5-minute window | The run fails on AC1 and the report names the case and the elapsed time | None | AC1 |
| X8 | The case does not reach the state the owner sets for the assessment | The run fails on AC1 and the report names the case and both states | None | AC1 |
| X9 | A caller outside the case scope is authorised | The run fails on the access check and the report names the operation | None | AC1 |
| X10 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. No S1 package is in force in Phase 1, so the harness asserts the data, the state and the decision record and not a rule outcome; the business messages this journey can produce are in section 14 and belong to the owning services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-S1-E4002-APP |
| Negotiable | The data product code, the acceptance write, the multi-appraisal choice and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The appraisal the route is priced on, and the Workbench's acceptance of it, are proven end to end before the wave opens |
| Estimable | One harness runner, one stub set, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-S1-E4002-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Receive the appraisal value from SVAF

  Background:
    Given the contract fakes of section 12.8 are published and their versions pinned
    And the case and the asset are seeded through the owning contracts

  Scenario: AC1 Receive the appraisal value from SVAF (legacy RWB-E4-002 AC1)
    Given ACE has ingested the SVAF appraisal "AP-0001" for asset "AST-0001" at appraisal date 2026-11-02 and the rwb-source-data contract returns appraised value 4250000 for the asset key
    When the case owner assesses the route
    Then the Workbench reads the appraisal number, value, type and date for the asset_key through the rwb-source-data contract (DP-01, DP-05)
    Then it sets accepted, stale_flag and age_days in valuation_ext against the valuation_key
    Then the system writes the result to the decision log with the rule version

  Scenario: AC3 No value is accepted by the harness or by a system step (new, D-RCV-60)
    Given the appraisal for the asset is older than the 12-month policy limit
    When the case owner assesses the route without accepting the value
    Then stale_flag is set in valuation_ext against the valuation_key
    Then accepted is not set by the harness or by a system step
    Then the stale appraisal raises the order of the next story without a person asking for it

  Scenario: AC4 A consumed call fails or does not answer (new, D-RCV-60)
    Given the rwb-valuation call fails or does not answer
    When the case owner assesses the route
    Then no value is accepted and no decision is recorded

  Scenario: AC5 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the valuation model does not allow for the valuation_key
    When the case owner requests the status change
    Then the change is refused and no decision is recorded
```

AC2 of the legacy key is recorded as "Not recorded" and is owned by RWB-S1-E4002-APP; it is not restated here.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The appraisal number, value, type and date are ACE's and are read from `v_ace_valuation` for the asset key; the Workbench holds no copy of the appraisal, reads it SELECT-only and loads no SVAF file | REQ-RDF-004; D-RCV-35 U1 and U4; DP-05 |
| BR2 | The acceptance, the stale flag and the age are the Workbench's own and are held in `valuation_ext` against the `valuation_key`, in table rwb_valuation.valuation_ext, which this service creates and owns | REQ-RDF-004; legacy RWB-E4-002 |
| BR3 | An appraisal older than the 12-month policy limit is flagged stale on the extension record and raises the order of the next story, without a person asking for it | REQ-S1-001; Temporal and Drools Design Text Extract v1 slide 17 |
| BR4 | Every decision records the freshness of the data it used | REQ-RDF-009 |
| BR5 | The decision record carries the rule and its version and is written with the change in one transaction | REQ-DRI-001; R-UNI-39 |
| BR6 | No action proceeds if its record cannot be written | REQ-DRI-005; R-UNI-39 |
| BR7 | The case owner accepts the value; no value is accepted by the harness or by a system step | legacy RWB-E4-002 AC1; Temporal and Drools Design Text Extract v1 slide 17, step 3 |

No S1 package is in force in Phase 1 (Temporal and Drools Design Text Extract v1 slide 17 states "No S1 package yet (Phase 2)"), so the harness asserts the rule ID and version that the owning service records and fails the run when either is absent.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| VALUATION_ORDERED | Report attached and value extracted | the value is read from `v_ace_valuation` for the asset key | VALUATION_RECEIVED (R-DIL-09) |
| VALUATION_RECEIVED | Value presented for acceptance | the case owner accepts the value | VALUATION_ACCEPTED (R-DIL-09) |
| VALUATION_RECEIVED | Access refused recorded | the valuer records an access refusal and an external estimate is used | VALUATION_ACCEPTED (R-DIL-10) |
| AWAITING_VALUER | Panel service level breached | Not specified in the source documents (CG-ALL-866) past the panel service level | AWAITING_VALUER, escalated and re-allocated (R-DIL-11) |

These are the owner's states, held in rwb-valuation and in the extension record of rwb-source-data. S1 has no rule package in Phase 1, so the valuation state names come from the deed-in-lieu valuation sub-flow (R-DIL-07 to R-DIL-11), which the S1 step mirrors; the harness asserts what rwb-valuation records and names that source in the report. The harness changes none of these states itself: it triggers the assessment through the rwb-valuation contract, reads the state back through the rwb-case contract, and reports the owner and the operation behind each transition. A state the harness set by hand would prove nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT, and roles with Treatment and offer U | Assess the route and accept the value through the rwb-valuation contract, which is the case owner's step in the run |
| RW-CASEOWN, RW-TEAMMGR and roles with Treatment and offer R | Read the same journey evidence, including the case state and the decision record |
| QA lead | Owns the harness configuration, the seeding set, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-valuation, rwb-source-data, rwb-case, rwb-decision and rwb-access read, accept and record; the harness asserts and never writes |
| No approval level from the delegation of authority applies | The harness takes no business decision; the acceptance belongs to the case owner and the route approval belongs to the valuation story |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-187 to DF-ACE-195 | v_ace_valuation | valuation_key, asset_key, appraisal_no, appraisal_type, appraised_value, appraisal_date | Read, through the rwb-source-data products contract (DP-05) |
| DF-ACE-091 to DF-ACE-098 | v_ace_collateral | collateral_no, asset_key, account_key, collateral_value, collateral_type, register_date | Read, through the rwb-source-data products contract (DP-05) |
| DF-EXT-036 to DF-EXT-049 | valuation_ext | valuation_key, accepted, accepted_at, accepted_by, stale_flag, age_days | Read, through the rwb-source-data products contract (DP-05); the writer of the acceptance fields is open between P1 and S1 (`ownership.json` ruling ASM-0081; FSD P1 OQ-P1-05) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | case_id, decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The harness owns no table and writes no row: it reads and writes through the API of the owning service only (DP-01, DP-05), and every table above stays with its owner.

Reference data is read under DP-06 and DP-07; the reference parameters are Not specified in the source documents (DOR-RWB-ITG-E4002-ITG-20).

The R-DIL-11 timer condition behind the panel service level row in section 9 is written `order_age > panel service level`. The term `order_age` is not a field or entity of the Logical Data Model and Data Dictionary v9; its data model field name is Not specified in the source documents (DOR-RWB-ITG-E4002-ITG-7).

### 12. Contract

Contract version fixed: this story builds against version 5.0.0 of the contracts of rwb-valuation, rwb-source-data, rwb-case, rwb-decision and rwb-access in Recovery Workbench API Specification v5.

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/valuation/v1/cases/{caseId}/route` | S1 rwb-valuation | The route assessment in which the appraisal is read and accepted (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The appraisal number, value, type and date from `v_ace_valuation`, and the acceptance fields in `valuation_ext` (AC1, DP-05) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state at the route decision (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record with the rule ID and version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope, including the refusal path (AC1) |

Not specified in the source documents (GAP-0430; ASM-0606): the data product code that carries `v_ace_valuation` and `valuation_ext`, and the internal operation and field details through which the route assessment records the acceptance (the writer is open between P1 and S1). Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-13); where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the assessment through the rwb-valuation contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The ACE batch that carries the SVAF appraisal is ready (AC1) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through the local decision-record library | The record reaches the ledger within 5 minutes (AC1, DP-03) |

`rwb.source-data.AceDataReady.v1` carries the business date and no personal data; `rwb.decision.DecisionRecorded.v1` is keyed by caseId. The harness asserts that neither carries personal data.

#### 12.5 Workflows and activities

None added. The harness exercises the existing `RouteDecisionWorkflow` on task queue `rwb-valuation` and the `CaseWorkflow` on task queue `rwb-case`, and asserts their effects through the services' contracts and the owners' topics. It creates, changes and owns no workflow, activity or Schedule.

#### 12.6 Schedules

None added. The assessment is triggered by a person and by the case reaching the route decision, and this story sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the appraisal is ACE's, read through rwb-source-data's contract, the extension record is rwb-source-data's, the assessment is rwb-valuation's, the case is rwb-case's and the record is rwb-decision's.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-valuation | `POST /cases/{caseId}/route`, `rwb.valuation.events.v1` | Day-1 runs of AC1 before RWB-S1-E4002-APP is live |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the appraisal, the acceptance fields and `valuation_ext` |
| WireMock stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertion of the case state at the route decision |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record with its rule ID and version |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| AceDataReady event stub | `rwb.source-data.AceDataReady.v1` | The batch-ready fact where the environment does not run the ACE ingest |

Given and test-data lines in sections 7 and 16 are written against these fakes, not against `v_ace_valuation` or any other ACE view or extension table.

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. Not specified in the source documents (GAP-0430; ASM-0606): the product code, the internal acceptance write, the choice between more than one appraisal for an asset, the gateway-bff composite route for SCR-13, the harness pack, the seeding set and the evidence format. The harness environment, seeded identifiers, business date, product codes, unnamed operations, evidence format and gate thresholds are carried to the wave 3 entry check (GAP-0436).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 5 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.source-data.AceDataReady.v1` and `rwb.decision.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | None added; `RouteDecisionWorkflow` on `rwb-valuation` and `CaseWorkflow` on `rwb-case` exercised only |
| File | None. The harness handles no file; the SVAF feed is ACE's ingest and not this story's |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependency is the one I story, RWB-S1-E4002-APP: until it is live the run uses the rwb-valuation stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour. The harness owns no schema (DP-01), reads the appraisal and the acceptance fields from rwb-source-data's products contract (DP-05), and never touches the ACE views itself. The decision record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). Every call sits on the owner's per-service base with a single hop (DP-13), and the composed reads a screen would make for SCR-13 are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| AppraisalRunner | Job | Runs the owned criterion for a business date in order and holds the run lock |
| StubSet | Fake | The five WireMock stubs and the `AceDataReady` event stub, each generated from the published contract with the version pinned |
| EventProbe | Service | Consumes `rwb.source-data.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, with one case at the route decision whose asset `AST-0001` carries the appraisal `AP-0001` at appraisal date 2026-11-02 and appraised value 4250000, and a second case whose appraisal date is older than the 12-month policy limit so that the stale path is exercised. Not specified in the source documents (GAP-0430; ASM-0606): the environment, the seeding set, the product code and the evidence retention. Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the five stubs and the `AceDataReady` event stub from the published contracts, pin each contract version in the run report and fail the run on a version mismatch (X1, X10).
2. Build the AppraisalRunner for AC1: assert `AceDataReady`, read the appraisal for the asset key, trigger the route assessment, read the case state and the acceptance fields, read one record with its rule ID and version, and assert `DecisionRecorded` inside 5 minutes (X2, X3, X4, X7, X8).
3. Add the stale path: an appraisal date older than the 12-month policy limit, the stale flag set and `age_days` consistent with the date (X5).
4. Add the rule-version assertion and the report text for the Phase 1 position, that no S1 package is in force and the rule ID and version of the owning service are what the run checks (X6).
5. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller outside the case scope (X9).
6. Add the EvidenceReport and the gate, then swap the rwb-valuation stub for the real service when RWB-S1-E4002-APP lands and rerun the criterion.

**Feature switch.** The legacy key names no feature switch for this behaviour. The journey runs behind the platform feature-flag library as the wave releases it. Not specified in the source documents (GAP-0430; ASM-0606): the flag key for this harness.

**Done when.** The tests of section 16 pass for AC1; the criterion passes against the fakes on Day 1 and again against rwb-valuation when RWB-S1-E4002-APP lands; and the wave entry check holds a run report keyed by story and business date with the contract versions and the product code used named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the assessment cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-DIL-09, R-DIL-10 and R-DIL-11 carry no message ID in the rule set, and no S1 package is in force in Phase 1, so the harness asserts the data, the state and the decision record and names a message ID only where the owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-13 Route decision shows the states this step sets:

| State | What the user sees and does |
|---|---|
| Loading | The appraisal is being read for the asset key; no value is presented yet |
| recommendation | The value is shown with its type and date and the route recommendation built on it |
| overridden | The case owner has chosen differently from the recommendation and given a reason |
| submitted | The assessment is submitted; the acceptance and the record exist |
| Empty | Not specified in the source documents (CG-ALL-873) |
| Error | Not specified in the source documents (CG-ALL-873) |
| No access | You cannot {action} here. Your role does not include it. (MSG-P4-002) |

SCR-13 Route decision shows Loading, recommendation, overridden and submitted, as the legacy key states them. Not specified in the source documents (GAP-0430; ASM-0606): the gateway-bff composite route that serves SCR-13.

The harness renders no screen. It reads these states through the rwb-valuation, rwb-source-data, rwb-case and rwb-decision contracts, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the evidence report. Not specified in the source documents (GAP-0430; ASM-0606): its format and retention.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-002-01-ITG | AC1, BR1, BR2, BR4, BR5 | Integration | SVAF appraisal AP-0001 for asset AST-0001, appraisal date 2026-11-02, appraised value 4250000 |
| TC-E4-002-02-ITG | BR6 (run by RWB-S1-E4002-APP) | Integration | Decision log forced to fail; MSG-P7-003 |
| TC-E4-002-03-ITG | Access | Component | A role without the right; MSG-P4-002 |
| TC-E4-002-04-ITG | Principle 5 | NFR | Forced decision-log write failure; nothing moves |
| TC-E4-002-05-ITG | AC3, BR3, BR7 | Integration | Appraisal older than the 12-month policy limit (date Not specified in the source documents (DOR-RWB-ITG-E4002-ITG-4)); no acceptance by the case owner |
| TC-E4-002-06-ITG | AC4 | Integration | Consumed rwb-valuation call fails or does not answer; Not specified in the source documents (NEWAC-RWB-ITG-E4002-ITG-AC4) |
| TC-E4-002-07-ITG | AC5 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E4002-ITG-AC5) |

These are the ITG copies of TC-E4-002-01 to TC-E4-002-04; the full legacy tests, with their Given, When and Then, are in `Recovery Workbench Test Cases v8.xlsx` under those IDs. TC-E4-002-02-ITG is kept as the copy of AC2 and is exercised through the owning app story, because AC2 belongs to RWB-S1-E4002-APP.

### 17. Guardrails

- No business value in code: the appraisal type, the 12-month policy limit, the seeding set, the product code and the evidence shape are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the ACE appraisal is read through rwb-source-data's product (DP-05).
- The Workbench holds no copy of the appraisal and loads no SVAF file; the value is ACE's and the acceptance is the Workbench's, held in `valuation_ext` (legacy RWB-E4-002; D-RCV-35 U1 and U4).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets an appraisal, an acceptance or a case state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-004 | Collateral records and appraisal values are read through `v_ace_collateral`, `v_ace_collateral_detail` and `v_ace_valuation`, and the Workbench's acceptance of an appraisal is held in `valuation_ext` | Business Requirements Program v5, section 5.1 | FEAT-VAL-02 | D6 route decision (S1 valuation) | R-DIL-09, R-DIL-10 | TC-E4-002-01-ITG |
| REQ-RDF-009 | Every data product carries a freshness stamp, and every decision records the freshness of the data it used | Business Requirements Program v5, section 5.1 | FEAT-VAL-02 | D6 route decision (S1 valuation) | None in force (S1 package Phase 2) | TC-E4-002-01-ITG |
| REQ-S1-001 | An appraisal older than the policy limit triggers a new valuation order without a person asking for it | Business Requirements Program v5, section 5.8 | FEAT-VAL-02 | D6 route decision (S1 valuation) | R-DIL-09, R-DIL-11 | TC-E4-002-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding the case, the decision, the rule and its version | Business Requirements Program v5, section 5.7 | FEAT-VAL-02 | D6 route decision (S1 valuation) | None in force (S1 package Phase 2) | TC-E4-002-01-ITG, TC-E4-002-04-ITG |

### 19. Out of scope

- AC2 of the legacy key, which is owned by RWB-S1-E4002-APP and is exercised through that app story.
- The rwb-valuation behaviour itself: the route decision, the recommendation, the approval and the workflow are the service story RWB-S1-E4002-APP.
- The production valuation endpoints, the `RouteDecisionWorkflow` and the `CaseWorkflow` themselves, and the `rwb_valuation`, `rwb_source_data`, `rwb_case` and `rwb_decision` tables, none of which this story changes.
- The contract baselines of the five consumed services, which are their own CON stories and are only pinned and asserted here.
- The platform configuration: the gateway-bff composite route, the feature-flag library, the decision-record library and the Temporal namespace, which are platform work and not this story's.
- The SVAF feed itself, its file layout, its delivery schedule and the ACE ingest that receives it, which belong to ACE and to rwb-source-data.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The product code, the acceptance write, the multi-appraisal choice, the harness pack, the seeding set and the evidence format: carried as a gap and an assumption, not decided here.
