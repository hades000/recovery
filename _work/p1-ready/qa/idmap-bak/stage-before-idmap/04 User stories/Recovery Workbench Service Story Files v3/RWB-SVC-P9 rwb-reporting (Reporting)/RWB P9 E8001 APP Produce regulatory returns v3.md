# RWB-P9-E8001-APP Produce regulatory returns

**Version 3 changes.**

- RD-P1-004: Align the Error and Message Standard v6 wording.

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E8001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P9-E |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P9-E8001-APP-16) |
| Depends on (build) | RWB-P9-E8001-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Contract version | Not specified in the source documents (DOR-RWB-P9-E8001-APP-23) |
| Readiness decisions | RD-P1-004 |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 10 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Version | Date | Change | Tool |
|---|---|---|---|
| v1 | 22 November 2026 | D-RCV-60 realignment of RWB-E8-001 into rwb-reporting, app slice | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| v2 | 26 November 2026 | D-RCV-60: fixes from the rulings workbook (X20 RWB-P9-E8001-APP) | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1. Story

As a **compliance and PDPA officer**, I want **the rwb-reporting returns run that freezes the measure snapshots of a business date and records the return with the rule version in force**, so that **every regulatory measure is read from the decision log instead of being counted by hand, and no return is published from a stale data product, an unversioned definition or an unrecorded decision**.

The service owns the measure definitions, the frozen snapshots and the publish row. The decision facts and the rule version are written through the local decision-record library and read back through the rwb-decision contract; the run is the service's own daily reporting job. Nothing of another service is read as a table.

### 2. Business rationale

Measures are counted by hand from spreadsheets at month end (FSD P9 A1.3), so the regulator sees a number nobody can trace to a decision. TSD P9 NFR-065 requires the business measures per decision to be produced from the decision log and not from a separate count, and the legacy story already says the measures come from the decision log. This story makes the return a frozen, versioned artefact: the measure rows carry the definition version and the frozen flag, the publish row carries the published or held status, and one decision record carries the rule version in force.

In the microservice layout rwb-reporting is the only owner of the measure tables, and the read model is built from events rather than from a copy of another service's data (DP-17, ADR-018): the legacy data lake and Power BI copy (INT-19) is removed by Architecture v5, so the return is read from `rwb_reporting.measure_snapshot` through one REST base (DP-13) and reached through the gateway-bff composite route (DP-19). The decision record leaves through the local library on `rwb.decision-record.v1` (DP-03), which is what makes AC1 traceable to its rule version.

The lake removal is a real conflict between sources rather than a quiet change: the FSD A2.7.2 integration points and TSD P9 T5.1 still name Power BI and the data lake, and the pattern set of this key does not carry DP-17. The conflict is recorded once, with the assumed replacement.

### 3. Preconditions

- The contract baseline RWB-P9-E8001-CON is published with the returns read of appendix API-P9-001 and the decision element, and its three fakes answer the accepted and the refused case.
- A definition of each returned measure is in force for the business date, with its `definition_version` (for example MD-2026.11 in the FSD example) and its data product from LOV-DATA-PRODUCT.
- The data products the return reads carry the business date; a product whose ACE batch has not arrived is stale and holds the run (VR-P9-007-1).
- The publish row of the business date is not HELD, and the case counts behind it were reconciled by the reconciliation capability of this service.
- The rule version in force is available to the local decision-record library (DP-03) and the decision facts of the day are readable through the rwb-decision contract.
- The caller holds Reporting R (RW-COMPLY, RW-BIANAL, RW-DATASTEW, RW-AUDIT and the other roles of TSD P9 T6.1), or the run uses the service identity; scope is applied to the read.
- The two platform contracts are available: RWB-PLT-E1027-CON (decision record) and RWB-PLT-N001-CON (gateway-bff composite route).
- Values that no source fixes: the step name of the run inside JOB-15, the layout of the return, the wording of MSG-P9-002 and MSG-P9-003 and the decision code are Not specified in the source documents (GAP-2582; ASM-4261).

### 4. Flow

1. JOB-15, the daily reporting run of the service, starts at 01:30 for the business date and reaches the returns step, which runs inside JOB-15 (the step name is Not specified in the source documents (GAP-2582; ASM-4261)).
2. System: resolves the measures of the return from `measure_definition` — the definition in force on the business date, highest `definition_version` valid from that date, for every data product of LOV-DATA-PRODUCT the return reads.
3. System: checks that each data product carries the business date; a stale product stops the run with MSG-P1-001 and nothing is frozen.
4. System: reads the decision facts of the business date through the rwb-decision contract — decision code, rule id, rule version, model version — and sums them per measure and dimension.
5. System: writes the snapshot rows into `measure_snapshot` with `measure_code`, `definition_version`, `business_date`, `product_group`, `dimension_code`, `dimension_value`, `value`, `case_count` and `is_baseline`.
6. System: publishes one decision record through the local library and the outbox to `rwb.decision-record.v1`: FEAT-RPT-07 as the decision reference, the rule version in force, the business date and the definition version (the decision code is Not specified in the source documents (GAP-2582; ASM-4265)).
7. System: on an accepted record, sets `frozen` true and `published_at` on the rows and writes the `measure_publish` row with status PUBLISHED; on a held day it writes status HELD with `held_reason` and publishes nothing.
8. System: the returns reader reads the frozen set through GET /reports/measures (API-P9-001) under the base, and the gateway-bff composite route serves the screens of section 15.
9. System: a run that fails at steps 3, 4 or 6 leaves no frozen row and no PUBLISHED publish row for that business date; the next run retries the date.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A data product of the return is stale for the business date | The run stops; no snapshot row is frozen; the run record names the product and its date | MSG-P1-001 | AC1 |
| X2 | A measure of the return has no definition in force | No value is written for that measure; the run record names it and the rest of the return proceeds | MSG-P9-003 | AC1 |
| X3 | The decision record cannot be written | Nothing is frozen and nothing is published; the date stays open and an incident is raised | MSG-P7-003 | AC2 |
| X4 | The decision-log read of rwb-decision does not answer | The run stops; no snapshot row is frozen for the date; the next run retries | MSG-GEN-006 | AC1; AC7 |
| X5 | The caller lacks Reporting R | 403 with the refusal; nothing is read | MSG-P4-002 | AC3; TC-E8-001-06 |
| X6 | The publish row of the date is HELD | The return is not published for that date and the held reason is returned | None | AC1 |
| X7 | A late correction to a published date | A new snapshot for the corrected date and a correcting decision record; the frozen rows of the earlier publish are never rewritten | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P9-E8001-CON and its fakes, with the two platform contracts as build dependencies; the rwb-decision read is a contract client with a fake and adds no build block |
| Negotiable | The measures, their formulas, units and data products are data of the data steward; the return layout, the step name and the decision code are settled with the reporting owner |
| Valuable | Turns a hand-counted month-end return into a frozen set that carries its definition version and its rule version, and removes the lake copy |
| Estimable | One service, one job step, one read, one decision element, three tables and seven exception paths |
| Small | Fits one sprint with the contract fakes |
| Testable | Every criterion is a component or contract test over synthetic cases and recorded contract payloads |

### 7. Acceptance criteria

```gherkin
Feature: Produce regulatory returns

  Background:
    Given the base of rwb-reporting is /api/recovery/reporting/v1 and its schema is rwb_reporting
    Given the definition of measure "CASES_BY_ROUTE" in force on the business date is "MD-2026.11"
    Given the rwb-decision contract mock returns the decision facts of the business date

  Scenario: AC1 Produce regulatory returns (legacy RWB-E8-001 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-decision contract mock returns the decision record accepted with the rule version in force
    When its trigger arrives
    Then builds the regulatory extracts from the data products and the decision log
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-001 AC2)
    Given the decision log cannot be written
    Given the rwb-decision contract mock returns a refused decision write
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The caller lacks Reporting R is refused (new, D-RCV-60)
    Given the caller does not hold Reporting R
    When the caller reads the return
    Then the system answers 403, nothing is read and the user sees MSG-P4-002

  Scenario: AC4 A snapshot row carries no personal data (new, D-RCV-60)
    Given a measure snapshot row is frozen for the business date
    When the row, its event or its log line is written
    Then it carries codes, dates, amounts and counts only

  Scenario: AC5 The return rules hold on a run (new, D-RCV-60)
    Given a run builds the return for the business date
    When the run reads, freezes and publishes the return
    Then the measures come from measure_definition, a stale product holds the return with MSG-P1-001, the record is written before any row is frozen, and a frozen row is never rewritten

  Scenario: AC6 A provided operation answers only the codes its contract allows (new, D-RCV-60)
    Given the contract of GET /reports/measures allows the codes 401, 403 and 404
    When a caller reads the return without a valid session, without Reporting R or on a refused read
    Then the system answers 401, 403 or 404 as the contract gives, and no other code

  Scenario: AC7 A consumed call that fails or does not answer stops the run (new, D-RCV-60)
    Given the rwb-decision contract mock does not answer the decision-log read
    When the run reads the decision facts of the business date
    Then the run stops, no snapshot row is frozen for the date and the user sees MSG-GEN-006
```

AC1 and AC2 are the criteria of RWB-E8-001 and this story owns both; they are copied verbatim and each gains one inserted Given so the cross-service part is asserted against the contract mock, with every legacy value kept. The frozen set, the publish row and the read of section 12 are the evidence that AC1 produced a return and not a screen.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | No value a business person may change is written in code; it is read from reference data with its version: the measure definitions of measure_definition (section 12.7) | BR-P9-007; reference-data contract: Not specified in the source documents (DOR-RWB-P9-E8001-APP-20) | AC1; TC-E8-001-01 |
| BR2 | A data product stale after a late or failed ACE batch holds the return for that business date | VR-P9-007-1; MSG-P1-001 | AC1 (X1); TC-E8-001-01 |
| BR3 | Business measures per decision are produced from the decision log, not from a separate count; the return is built from the reporting read model and the decision record and read through GET /reports/measures, with no data lake copy | TSD P9 NFR-065 | AC1; TC-E8-001-01 |
| BR4 | The return is recorded with the rule version in force before any snapshot row is frozen; a failed record blocks the return and raises an incident | Legacy AC1 and AC2; R-UNI-39 | AC1; AC2; TC-E8-001-01; TC-E8-001-02 |
| BR5 | A row of a published business date is frozen and is never rewritten; a correction is a new snapshot for the corrected date plus a correcting record | DF-RPT-051; R-UNI-24 (ASM-4268) | AC2 (X7); TC-E8-001-02 |
| BR6 | The measure list of the return is data: the definitions in force for the business date, by data product and definition version | DF-RPT-031 to DF-RPT-040 | AC1; TC-E8-001-01 |
| BR7 | The service reads and writes only `rwb_reporting`; decision facts come through the rwb-decision contract and case counts already reconciled by this service; the fate of document_field and rule_row: Not specified in the source documents (GAP-2582) | DP-01; Ownership Map | AC1; TC-E8-001-01 |
| BR8 | No personal data enters a snapshot row, an event, a workflow input or a log: codes, dates, amounts and counts only | DP-09; guardrail 2 | AC4; TC-E8-001-07 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| (none) | JOB-15 reaches the returns step | The definitions are in force and no product is stale | Snapshot rows written, not frozen |
| Not frozen | Decision record accepted | The rule version is recorded | Frozen and PUBLISHED |
| Not frozen | Decision record refused or the read fails | Nothing is frozen | Held for the date, retried by the next run |
| Frozen and PUBLISHED | Correction of the date | A correcting record is written | A new snapshot set for the corrected date; the frozen rows stay |

The publish status values are PUBLISHED and HELD of LOV-MEASURE-PUBLISH; the `frozen` and `is_baseline` flags are the snapshot's own columns. No case state moves in this story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, compliance and PDPA officer | Reads the return in scope (Reporting R); the role the legacy story names |
| RW-BIANAL, reporting and BI analyst | Reads the return and the frozen set (Reporting R, CRUD on the measure set) |
| RW-DATASTEW, data steward and data product owner | Owns the measure definitions and their versions (Reporting CRU); not changed by this story |
| RW-AUDIT, internal audit | Reads the frozen set and the decision record of a date (Reporting R) |
| Service identity of rwb-reporting | Runs the step and writes the decision record (no person) |
| Platform team | Owns the decision-record library and the incident raised by R-UNI-39 |

### 11. Data

| BR Field ID | Entity | Field | Read or write | Where |
|---|---|---|---|---|
| DF-RPT-031 to DF-RPT-040 | measure_definition | all fields | Read | own schema `rwb_reporting` |
| DF-RPT-041 to DF-RPT-052 | measure_snapshot | all fields, `frozen` and `published_at` written | Read and write | own schema `rwb_reporting` |
| DF-RPT-053 to DF-RPT-058 | measure_publish | all fields | Read and write | own schema `rwb_reporting` |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision code, rule id, rule version, model version, decided at | Read through the rwb-decision contract | P7 contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | the returns record with its rule version | Write through the decision-record library | shared `rwb.decision-record.v1` |

The legacy Data section also names `document_field` and `rule_row`; documents are rwb-document's and rule rows are rwb-decision's, and this story reads neither (GAP-2582; ASM-4269). The return layout and the field types beyond the TSD P9 T3.1 definitions are Not specified (GAP-2582; ASM-4263).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1`.

| Method | Path | Purpose | Auth | Errors |
|---|---|---|---|---|
| GET | `/reports/measures` | Read the frozen measure set of a period by measure, product and route (API-P9-001) | Reporting R, scope applied | 401 MSG-P4-001; 403 MSG-P4-002; 503 MSG-GEN-006 |

Query parameters are `measure`, `product`, `route`, `from` and `to`; the answer is Measure[] (TSD P9 T-A.2). The return itself is read through this one operation, because the Ownership Map gives rwb-reporting one provided operation (GAP-2582; ASM-4270). The right is enforced on the platform authorisation path, and DP-08 is not in the pattern set of this key (GAP-2582; ASM-4267).

#### 12.2 REST operations consumed

| Operation | Owner | Contract | Purpose | Timeout |
|---|---|---|---|---|
| GET the decision-log read of `/api/recovery/decision/v1` | rwb-decision (P7) | RWB-P7-E2005-CON, faked here | The decision facts and the rule version recorded per decision of the business date | 2 s |

One hop, on the owner's published contract, never a table. The plan declares no C row for this read, so it is declared and faked (GAP-2582; ASM-4272). No other operation is consumed: the case counts behind a publish come from this service's own reconciliation.

#### 12.3 Events published

None. The Ownership Map gives rwb-reporting no event of its own; the returns record leaves on the shared `rwb.decision-record.v1` through the local library and the outbox (DP-03), and the rule version is never copied into `rwb_reporting` (GAP-2582; ASM-4264).

#### 12.4 Events consumed

| Event or fact | Topic | Owner | Use |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (event 05) | `rwb.case.events.v1` | P3 rwb-case | The case state behind the count measures |
| The notice and contact facts of the day | `rwb.comms.events.v1` | P6 rwb-comms | The contact and notice measures |
| The treatment outcome facts | `rwb.treatment.events.v1` | S2 rwb-treatment | The settlement and restructuring measures |
| The debt-sale lot facts | `rwb.debtsale.events.v1` | S6 rwb-debtsale | The sale measures |
| The write-off and recovery facts | `rwb.writeoff.events.v1` | S7 rwb-writeoff | The write-off and recovery measures |
| The payment facts | `rwb.payment.events.v1` | P8 rwb-payment | The cash and recovery measures |

The event names beyond `rwb.case.CaseStateChanged.v1` are pinned by the Kafka Topic and Event Catalog and are Not specified in the sources read for this WP (GAP-2582; ASM-4273). Dedupe is by the CloudEvents id through the inbox.

#### 12.5 Workflows and activities

None. The Ownership Map gives rwb-reporting no domain workflow; the returns step is part of the daily reporting run and its workflow identity is the job's own (GAP-2582; ASM-4261). No child workflow, no Nexus call and no case workflow is started.

#### 12.6 Schedules

| Job | Queue | When | Step |
|---|---|---|---|
| JOB-15, the daily reporting run | `rwb-reporting` | Daily at 01:30 | The returns step of section 4; no separate Schedule and no Quartz row |

The registration detail and the cron of the Schedule are the platform's and are Not specified in the sources read for this WP (GAP-2582; ASM-4276).

#### 12.7 Tables owned

| Table | Schema | Owner service | Contracted use |
|---|---|---|---|
| measure_definition | rwb_reporting | rwb-reporting | The definition in force by measure, data product, unit and definition version |
| measure_snapshot | rwb_reporting | rwb-reporting | The frozen value per measure, business date, product group and dimension |
| measure_publish | rwb_reporting | rwb-reporting | The PUBLISHED or HELD status of a business date with the two counts and the held reason |

`decision_log_entry` is P7 rwb-decision's, `recovery_case` is P3 rwb-case's and `document` is P5 rwb-document's; this service names them only as consumed answers (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision WireMock | The decision facts of a date, an empty day, a refused write and an answer beyond the budget (path and answer fixed with the P7 owner; GAP-2582; ASM-4272) | AC1, AC2, X3, X4 |
| decision-record library stub | An accepted record with the rule version and a stopped chain | AC1, AC2 |
| event harness for the six consumed topics | One synthetic business date of facts, a repeat delivery with the same CloudEvents id and a stale product | AC1, X1 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | The returns read provided; the decision-log read of P7 consumed, one hop with a 2 s timeout |
| Kafka | None published, 6 topics consumed | The read model of the day; the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | The job's own run | JOB-15 on `rwb-reporting`; no domain workflow |
| File | None | No file is read or written; the lake copy is removed (GAP-2584; ASM-4262) |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting.returns`.

| Component | Type | Microservice responsibility |
|---|---|---|
| RegulatoryReturnController | Controller | The 12.1 read, the permission check and the error mapping |
| ReturnRunStep | Service | Steps 1 to 8 of section 4 in one unit of work per business date; idempotent on the date |
| MeasureDefinitionResolver | Service | The definition in force per measure from `measure_definition`; refuses a measure with none (X2) |
| StaleProductGuard | Service | The business-date check of every data product the return reads (X1) |
| DecisionFactClient | Client | The decision-log read of RWB-P7-E2005-CON, with a circuit breaker and a 2 s timeout |
| SnapshotWriter | Repository | The snapshot rows and the frozen flag; never rewrites a frozen row (BR5) |
| PublishGuard | Service | The `measure_publish` row: PUBLISHED, or HELD with the held reason (X6) |
| DecisionRecordPublisher | Publisher | The local decision-record library and the outbox to `rwb.decision-record.v1` (DP-03) |

**Database.** Per-service Flyway in `rwb_reporting` (DP-15) with the three tables of TSD P9 T3.1 and the standard record columns, the unique keys on (measure_code, definition_version) and on `measure_publish.business_date`, and an index on (business_date, measure_code, dimension_code). No migration touches another schema.

**Configuration and reference data.** The measures, formulas, units, data products and dimensions are data rows of this service (BR1, BR6). The single parameter of the run is the hold-on-stale switch, `REPORTING_RETURNS_HOLD_ON_STALE`, default true; its name is assumed and not fixed by a source (GAP-2582; ASM-4263).

**Build steps.**
1. Flyway baseline of `rwb_reporting` with the three tables; unique-key tests.
2. MeasureDefinitionResolver and StaleProductGuard against synthetic definitions and a stale product.
3. DecisionFactClient against the rwb-decision fake, with the empty day and the timeout case.
4. SnapshotWriter and the freeze rule of BR5.
5. DecisionRecordPublisher and PublishGuard: accepted, refused and held.
6. ReturnRunStep: order of steps, idempotence on the business date, the seven exception paths.
7. RegulatoryReturnController with the 12.1 error mapping and the scope filter.

**Feature flag.** `rwb.reporting.regulatory-returns`; off, the step is skipped and the read answers 404.

**Done when** the tests of section 16 pass, a synthetic business date produces a frozen set with its definition version and its rule version, and no table of another schema is read or written.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product of the return is stale for the business date | {product} is from {date}. Today's load has not arrived. |
| MSG-P7-003 | The returns decision could not be recorded | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller lacks Reporting R | You cannot {action} here. Your role does not include it. |
| MSG-P9-003 | A measure of the return has no definition in force | Not specified in the source documents (GAP-2582; ASM-4266) |
| MSG-P9-002 | The counts behind the publish do not match | Not specified in the source documents (GAP-2582; ASM-4266) |
| MSG-GEN-006 | A downstream of the run is unavailable | {system} is not available. Try again in a few minutes. |
| MSG-P4-001 | Not specified in the source documents (DOR-RWB-P9-E8001-APP-9) | Not specified in the source documents (DOR-RWB-P9-E8001-APP-9) |

MSG-P1-001 comes from VR-P9-007-1, MSG-P7-003 and MSG-P4-002 from the legacy story, and MSG-GEN-006 from the message standard; the texts are copied unchanged. Thai text follows decision DL10 (still open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

No screen in this story, as the legacy story says. The frozen set is read by SCR-37 Steering dashboard and by the reporting screens of the module through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19). States of SCR-37: loaded, the answer shows the frozen rows of the latest PUBLISHED date, and a HELD date shows the earlier published date with its held reason. Empty, error and no access: Not specified in the source documents (CG-ALL-7896). Loading: Not specified in the source documents (CG-ALL-7896).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-001-01 | AC1 | Component | Synthetic business date with definitions in force, six topics of facts and a rwb-decision fake that accepts the record |
| TC-E8-001-02 | AC2 | Component | The decision-record library forced to refuse; no frozen row and no PUBLISHED row for the date |
| TC-E8-001-03 | Access | Contract | RW-TEAMMGR calls the read with Reporting R and RW-AUDIT reads in scope; a role without the right is refused with MSG-P4-002 |
| TC-E8-001-04 | Principle 5 | NFR | The decision record is forced to fail on ten business dates; nothing is frozen, nothing is published and an incident is raised |
| TC-E8-001-05 | Boundary of section 12.7 tables | Component | Boundary business dates with one row in each table of section 12.7 (measure_definition, measure_snapshot, measure_publish) |
| TC-E8-001-06 | AC3 | Contract | The caller holds no Reporting R; the read is refused with MSG-P4-002 and nothing is read |
| TC-E8-001-07 | AC4 | Component | A frozen snapshot row and its event, workflow input and log line; only codes, dates, amounts and counts are present |
| TC-E8-001-08 | AC5 (BR1 to BR7) | Component | A synthetic run with a definition in force, a stale product and a decision record; the rules of BR1 to BR7 hold |
| TC-E8-001-09 | AC6 | Contract | A stub of GET /reports/measures answers 401, 403 and 404 in turn; a code outside the contract is refused |
| TC-E8-001-10 | AC7 | Component | The rwb-decision fake forced to fail on the decision-log read; no frozen row and no PUBLISHED row for the date |

The four legacy cases keep their IDs, their order and their intent; the contract cases are in RWB-P9-E8001-CON section 16. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: measures, formulas, units, data products, dimensions and the definition version are data rows of this service.
- No personal data in a snapshot, an event, a workflow input or a log: codes, dates, amounts and counts only.
- ACE data only through the owner's contract: this service reads no `v_ace_*` view and no ACE table, and the decision facts arrive through the rwb-decision contract.
- No table of rwb_decision, rwb_case or rwb_document is read or written; no cross-schema query and no shared login.
- A frozen row is never rewritten (BR5); a correction is a new date plus a correcting record.
- No retired element returns: no data lake copy, no INT-19 extract and no Quartz entry (GAP-2584; ASM-4262).

### 18. Traceability

| Item | Value |
|---|---|
| Requirement and feature | FEAT-RPT-07 Produce regulatory returns, Epic 8, module P9 (FSD P9 A2.7) |
| Feature | FEAT-RPT-07 Produce regulatory returns |
| L3 process | Not specified in the source documents (DOR-RWB-P9-E8001-APP-2) |
| Business rules | BR-P9-007; VR-P9-007-1; NFR-065; R-UNI-39; R-UNI-24 |
| Legacy criteria | AC-P9-007-01 and the two exception flows AC-EXC-P9-007-01 and AC-EXC-P9-007-02 |
| Legacy and disposition | RWB-E8-001, Split (rework); app slice owns AC1 and AC2 |
| Test cases | TC-E8-001-01 to TC-E8-001-04 |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-018, ADR-019, ADR-020, ADR-021, ADR-022 |

### 19. Out of scope

- The contract baseline, its document, its fakes and its contract tests (RWB-P9-E8001-CON).
- The measure definitions and their approval, with their administration screens and the definition version lifecycle.
- The baseline measure set, the steering dashboard data set and the benefit tracking of the same service; this story reads their tables and does not change them.
- The reconciliation of the case counts behind a publish and its data quality break handling (FEAT-RPT-05, FEAT-RPT-09).
- The delivery of an extract to a regulator, and any file, data lake or Power BI path (INT-19 and INT-20 removed; GAP-2584).
- The classification, staging and re-ageing capability of the same epic (FEAT-RPT-10, RWB-E8-002).
