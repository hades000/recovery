# RWB-ITG-DM004-ITG Migrate treatment and offers

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM004-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-DM004-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-004 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-DM004-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated treatment and offer records resolves to its ACE view row and lists every orphan for the data steward and the ACE team, against the owning services' published contracts and their fakes**, so that **a restructure, settlement or deed already promised to a customer continues without a break at cutover**.

This is a harness story: it builds no production endpoint, table, workflow, schedule or screen, and it changes no business state. The legacy extract, the read of the plan from `v_ace_plan` and the cutover itself are legacy AC1 and AC3 of RWB-DM-004, and they belong to RWB-P1-DM004-APP. S2 owns the cutover load of its own Flyway sequence into `rwb_treatment` (DP-15), and S2 owns every state the harness reads. What this story adds is the repeatable proof that a migrated record still finds its case, its approval level and the plan it refers to, and that every key with no ACE row is listed with a reason and an owner role.

### 2. Business rationale

An agreed but unbooked treatment carries a promise: a settlement at a discount, a restructure, a deed in lieu. At cutover that promise survives only if the migrated record still finds its case, its approval level and the plan it refers to. A treatment that loses its case is a case a customer cannot continue; a treatment that loses its approval level is an agreement the bank cannot show it was allowed to make; a treatment whose `plan_ref` names a plan the ACE view does not hold is a balance that may be booked twice or not at all. The risk is not that the migration is wrong in bulk; it is that one break nobody lists becomes one customer promise lost, and nobody can say afterwards which record it was.

The harness is decoupled the way the services are. ACE data such as the account, the customer and the plan is read only through the operations of rwb-source-data, which is the only reader of the `recovery.v_ace_*` views (DP-05, D-RCV-35, ADR-010). The treatment keeps its own schema `rwb_treatment` and its own Flyway sequence (DP-15), so the cutover load is S2's and not a shared recovery schema. The SCR-45 data quality view of the same breaks is read through the gateway-bff composite route where a screen would compose it (DP-19). Zero tolerance is the rule the harness proves: every business key resolves (REQ-RDF-007) and every break is listed with its reason (REQ-RDF-008). That is DL25, and it is what turns a cutover report into evidence the data steward and the ACE team can act on.

### 3. Preconditions

- The published contract of S2 rwb-treatment, `GET /treatments/{treatmentId}`, is in the contract registry, and a stub is generated from it, so a migrated treatment can be read on Day 1.
- The published contract of P1 rwb-source-data is in the registry: the rerun of JOB-04, the records of DP01, DP02 and DP04 by case, and the freshness of DP04, each with a stub.
- The published contract of P3 rwb-case, `GET /cases/{caseId}`, is in the registry, so the case and its `account_key` and `person_key` are read from their owner and not from a table.
- The published contract of P4 rwb-access, `POST /authorise`, is in the registry, so the Platform administration right is checked and the refusal path is reachable.
- The data product catalog holds DP01 Account and arrears, DP02 Customer and party and DP04 Treatment and offers, with ACE as the system of record for the plan data and ON_CHANGE as the refresh of DP04 (FSD P1 v3, A2.2.2).
- S2's own Flyway sequence (DP-15) has carried the migrated treatment records into `rwb_treatment` for the business date under test; RWB-P1-DM004-APP has run the reconciliation, or its stub returns the same result.
- The harness environment and its base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields behind the SCR-45 composite route, the reconciliation extract format and its retention, the pass or fail gate and the data seeding set: Not specified in the source documents (GAP-0444; ASM-0636).
- No build dependency. Day 1, with the fakes in place from the first run, and the fake for RWB-P1-DM004-APP replaced by the real hop when that story lands.

### 4. Flow

1. Harness: holds the synthetic fixture of case `RW-2026-000604`, its migrated treatment `TRT-0604` (type SETTLEMENT, offer amount 2400000, approval level L6, outcome PENDING, `plan_ref` PLAN-SYN-0604 with status RUNNING), the keys `ACC-SYN-000604` and `PERS-SYN-000604`, and the orphan `plan_ref` PLAN-SYN-0777 for business date 2026-12-31, and serves it through the stub set. Nothing is seeded into a schema by hand.
2. Harness: triggers JOB-04 for business date 2026-12-31 with `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` and one Idempotency-Key, and keeps the run identifier the answer returns.
3. Harness: reads the treatment with `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and asserts its type, its offer amount 2400000, its approval level L6, its outcome PENDING and its own state, which the reconciliation does not move.
4. Harness: reads the case with `GET /api/recovery/case/v1/cases/{caseId}` and takes `account_key` ACC-SYN-000604 and `person_key` PERS-SYN-000604 from the case rather than from the treatment.
5. Harness: resolves the keys through `GET .../data-products/DP01/records?caseId={caseId}`, `GET .../data-products/DP02/records?caseId={caseId}` and `GET .../data-products/DP04/records?caseId={caseId}`, reads `GET .../data-products/freshness?product=DP04` before the rerun, and records for each key whether it resolved or is an orphan.
6. Harness: reads the reconciliation extract of the run and the SCR-45 answer through the gateway-bff composite route, asserts the two agree, and asserts the break list holds one row for the orphan `plan_ref` PLAN-SYN-0777 with key type PLAN, reason NO_ACE_ROW and owner role RW-DATASTEW, while the treatment stays readable at its own state and no plan is booked.
7. Harness: reruns JOB-04 for the same business date with the same fixture and one Idempotency-Key, and compares the break list and the counts of treatments, their approvals and their plan links with the first run.
8. Harness: calls `POST /api/recovery/access/v1/authorise` for a synthetic RW-OFF caller without the Platform administration right, and asserts 403 with MSG-P4-002, no run started and no break row written.
9. Harness: writes one report per business date, keyed by story and business date, with the four criteria, the contract versions, whether each hop was a stub or the owner, and the counts it compared, and gates the wave on the result.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1, AC2 |
| X2 | The cutover extract fixture lacks a required key, such as the case, the account key, the person key or the plan_ref | The run fails before any assertion and the report names the missing key and the fixture row | MSG-GEN-001 | AC1 |
| X3 | A key with no ACE view row is not listed on the break list | The run fails on AC1 or AC2 whatever the treatment state, and the report names the key, its type and the view it was checked against | None | AC1, AC2 |
| X4 | A rerun of JOB-04 lists the same break twice, or the counts of treatments, approvals and plan links differ | The run fails on AC3 and the report shows both runs side by side | None | AC3 |
| X5 | JOB-04 is refused because the freshness of DP04 is late | The run fails on AC3 and names the product, the business date and the last complete ACE business date; a late product is reported as a late product and not as a pass | MSG-P1-001 | AC3 |
| X6 | The SCR-45 answer and the reconciliation extract disagree on the break list or the counts | The run fails and the report names both sources and the difference | MSG-P1-012 | AC1, AC2 |
| X7 | A caller without the Platform administration right starts a run anyway | The run fails on AC4 and the report names the operation and the role | MSG-P4-002 | AC4 |

The report text is for the wave entry check and is not part of the message standard. The business messages the reconciliation produces are in section 14 and are asserted as data on the break list, the case and the data product freshness.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is the single I story, RWB-P1-DM004-APP |
| Negotiable | The fixture contents, the break-list fields and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | Referential completeness of the migrated treatment and offer records is proven, with every orphan listed and owned, before the wave opens |
| Estimable | One harness runner, one stub set, one cutover extract fixture, one key resolver, one break-list assertion, one report |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion runs against its fake and again against the real hop as RWB-P1-DM004-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate treatment and offers - wave 4 cutover reconciliation harness

  Background:
    Given treatment "TRT-0604" of type "SETTLEMENT" on case "RW-2026-000604" with offer amount "2400000", approval level "L6" and outcome "PENDING"
    Given the ACE plan view holds plan_ref "PLAN-SYN-0604" with plan_status "RUNNING"
    Given the case links account_key "ACC-SYN-000604" and person_key "PERS-SYN-000604"
    Given JOB-04 has run for business date "2026-12-31"

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-004 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC2 A plan key with no view row is listed and no plan is booked (new, D-RCV-60)
    Given migrated treatment "TRT-0604" refers to plan_ref "PLAN-SYN-0777"
    And the ACE plan view holds no row for plan_ref "PLAN-SYN-0777"
    When the harness reads the reconciliation result for business date "2026-12-31"
    Then the break list holds one row for treatment "TRT-0604" with key type "PLAN" and key value "PLAN-SYN-0777"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the treatment stays readable at its own state through the rwb-treatment contract
    And no plan is booked by the reconciliation

  Scenario: AC3 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-12-31" has run once
    When JOB-04 is rerun for the same business date
    Then the break list holds exactly one row for plan_ref "PLAN-SYN-0777"
    And the counts of treatments, their approvals and their plan links equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC4 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When the harness calls the reconciliation run for business date "2026-12-31"
    Then the answer is 403 with "MSG-P4-002"
    And no reconciliation run starts and no break row is written
```

Legacy AC1 and AC3 belong to RWB-P1-DM004-APP, and the four criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated record resolves to its view row, and an orphan is a break, not a warning | REQ-RDF-007; DL25 |
| BR2 | Every break is listed with its key, its reason and its owner, visible to the data steward and, where the row is missing in ACE, to the ACE team | REQ-RDF-008; BR-P1-011-3 |
| BR3 | Zero tolerance: referential completeness is 100 percent, and the target is not relaxed for a cutover date | DL25; FSD P1 v3 quality measure |
| BR4 | ACE data is read only through the views owned by rwb-source-data, and no service reads the views or another service's tables | D-RCV-35; ADR-010; DP-05 |
| BR5 | No plan record is copied and no plan is booked by the migration; the plan is read from ACE | Legacy RWB-DM-004 AC1, owned by RWB-P1-DM004-APP |
| BR6 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | Legacy RWB-DM-004 guardrails |
| BR7 | Each service owns its own Flyway sequence and its own cutover load | DP-15; ADR-021 |

### 9. State transitions

The harness changes no state and writes no row. The treatment it reads stays at PENDING with approval level L6 and offer amount 2400000, and the plan it refers to stays RUNNING in the ACE plan view as read through rwb-source-data: no plan record is copied, no plan is booked and no reconciliation result is written by the harness.

An orphan key changes nothing either. Treatment TRT-0604 stays readable at its own state through the rwb-treatment contract while `plan_ref` PLAN-SYN-0777 has no view row, and the only thing that moves is the break list: the orphan is listed with its reason NO_ACE_ROW and its owner role RW-DATASTEW. When the ACE view later holds a row for that `plan_ref`, the next reconciliation no longer lists it, and again no treatment state moves.

Every state change in this journey belongs to S2 rwb-treatment, to P3 rwb-case or to P1 rwb-source-data: the harness triggers JOB-04 and reads, and it asserts the states the owners reached. A state the harness set by hand would prove nothing, so the report names the owner and the operation behind each assertion. The cutover load that puts the migrated record into `rwb_treatment` is S2's own Flyway sequence (DP-15), run by S2's own cutover step and not by this story; RWB-P1-DM004-APP owns the reconciliation that this story exercises.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Owns the break list and the referential completeness measure; reads the reconciliation, the treatment and the case through the owners' contracts |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Hold the Platform administration right (R) in the legacy permission check of this key, and may read the break list for their scope and rerun the reconciliation for a business date |
| RW-AUDIT, RW-COMPLY | Read the run report and the break list as evidence; they take no reconciliation decision |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from the fake to the real hop of RWB-P1-DM004-APP |
| The owning services' identities | rwb-source-data owns JOB-04, the data product reads and the freshness; rwb-treatment owns the treatment and its state; rwb-case owns the case and its keys; rwb-access owns the right |
| No approval level from the delegation of authority applies | The harness takes no business decision; it reads, reruns and asserts, and the cutover sign-off is RWB-P1-DM004-APP |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | recovery_case | All 55 fields of the case, read through the rwb-case contract | Read |
| DF-TRT-001 to DF-TRT-033 | treatment | All 33 fields of the treatment, read through the rwb-treatment contract | Read |
| DF-ACE-160 to DF-ACE-177 | v_ace_plan | All 18 fields of the ACE plan view, read through the rwb-source-data contract and never from the view | Read |
| Standard column | recovery_case, treatment | source and migrated_at | Read |

Field IDs are those in the Logical Data Model and Data Dictionary, and the three ranges are the ones the legacy story names. The harness reads three data products and no table: DP01 Account and arrears carries the account key, DP02 Customer and party carries the person key, and DP04 Treatment and offers carries the plan the treatment refers to, with the plan data sourced from ACE and the treatment records from the Workbench (FSD P1 v3, A2.2.2). The harness owns no table and writes no row: every read goes through the API of the owning service (DP-05, DP-01). The seeding set and the harness environment: Not specified in the source documents (GAP-0444; ASM-0636).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Rerun JOB-04 for the business date under test with one Idempotency-Key (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The account row for account_key ACC-SYN-000604 (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | The customer row for person_key PERS-SYN-000604 (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/DP04/records?caseId={caseId}` | P1 rwb-source-data | The plan row present for PLAN-SYN-0604 and absent for PLAN-SYN-0777 (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP04` | P1 rwb-source-data | The freshness of DP04 before the rerun (AC3) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The migrated treatment, its type, its offer amount, its approval level, its outcome and its own state (AC1, AC2, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its `account_key` and its `person_key` (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration right for each call, and the refusal path for RW-OFF (AC4) |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream, and no call chain is made (Architecture v5 slide 11; DP-05). No operation is invented in this story and no operation is a monolith path.

Where a screen would compose the breaks, the harness calls the gateway-bff composite route behind SCR-45 Data quality instead of stitching the two sources itself, so the run proves the same answer the data steward sees (DP-19). Its path and its merge order across the reconciliation extract and the data product freshness are Not specified in the source documents (GAP-0444; ASM-0636).

#### 12.3 Events published

None. The harness publishes no Kafka event; it consumes nothing from a topic and writes its report to the wave record.

#### 12.4 Events consumed

None. The harness does not consume an event: JOB-04 is started by AceDataReady in production and is rerun for a business date through the owner's operation, which is the path a repeated reconciliation needs.

#### 12.5 Workflows and activities

None added. The harness exercises the existing JOB-04 Reconciliation run of rwb-source-data, its REC-05 business key step, and asserts the effect through the owner's contract and the break list (DP-05). No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. JOB-04 is event-triggered by AceDataReady and is rerun for the business date under test through the owner's operation; no cron, overlap policy or catch-up window is set by this story.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); it reads the treatment, the case and the data products through their owners' contracts.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-source-data | Rerun of JOB-04, DP01, DP02 and DP04 records by case, and DP04 freshness | Day-1 run of AC1, AC2 and AC3 before RWB-P1-DM004-APP is live |
| Stub for rwb-treatment | `GET /treatments/{treatmentId}` | Day-1 read of treatment TRT-0604 at PENDING with its type, amount, level and outcome |
| Stub for rwb-case | `GET /cases/{caseId}` | Day-1 read of the case and its `account_key` and `person_key` |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path of AC4 |
| Cutover extract fixture | The synthetic cutover extract of RWB-P1-DM004-APP | The migrated records for case RW-2026-000604 and business date 2026-12-31, with the clean plan_ref PLAN-SYN-0604 and the orphan PLAN-SYN-0777 |
| Reconciliation extract fixture | The extract the REC-05 step writes | The break rows and the counts a rerun is compared against |
| SCR-45 composite route stub | The gateway-bff composite route behind SCR-45 Data quality | The answer the console would show for the same business date |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The fixture field layouts, the break-list fields, the composite route path and merge order, the harness environment, the data seeding set and the evidence format and retention: Not specified in the source documents (GAP-0444; ASM-0636).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (Architecture v5 slide 11; DP-05), composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published and none consumed; JOB-04 is exercised through its owner's rerun operation |
| Temporal | None added; JOB-04 Reconciliation exercised, event-triggered by AceDataReady in production |
| File | The cutover extract fixture and the reconciliation extract fixture, both as fixtures |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The single blocking dependency is the I story RWB-P1-DM004-APP: it owns the extract, the read of the plan from `v_ace_plan` and the reconciliation; the cutover load is S2's own Flyway sequence. Until it is live the run uses its stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The stubs generated from the published contracts of rwb-source-data, rwb-treatment, rwb-case and rwb-access, with each contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic cutover extract for case RW-2026-000604, treatment TRT-0604, the keys ACC-SYN-000604 and PERS-SYN-000604, the clean plan_ref PLAN-SYN-0604 and the orphan PLAN-SYN-0777 |
| PlanKeyResolver | Service | Resolves the case, account, person and plan keys through the DP01, DP02 and DP04 records and the DP04 freshness, and separates a resolved key from an orphan |
| BreakListAssertion | Service | Reads the reconciliation extract and the SCR-45 composite answer and asserts one row, its key type, its reason and its owner role |
| EvidenceReport | Service | Writes one report per business date, names the contract and fixture versions, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real hop of RWB-P1-DM004-APP as soon as it lands, on case `RW-2026-000604` and treatment `TRT-0604` of type SETTLEMENT with offer amount 2400000, approval level L6 and outcome PENDING, the account key ACC-SYN-000604, the person key PERS-SYN-000604, the plan PLAN-SYN-0604 at status RUNNING, the orphan plan PLAN-SYN-0777 and business date 2026-12-31. The amount and the L6 level are the worked example values of the Temporal and Drools design, not values invented here. The environment, the base hosts, the seeding set and the evidence retention: Not specified in the source documents (GAP-0444; ASM-0636). The fixture is served by the stubs and never written into a schema.

**Build steps**

1. Generate the stub set from the published contracts and pin each contract version in the run report; fail the run on a version mismatch (X1).
2. Build the CutoverExtractFixture and prove the treatment, the case and the three data product reads resolve for business date 2026-12-31 (X2).
3. Build the JourneyRunner for the trigger and the reads: rerun JOB-04 with one Idempotency-Key, read the treatment at PENDING, read the case with its account and person keys, and read the DP04 freshness.
4. Add the PlanKeyResolver: DP01, DP02 and DP04 by case, with the resolved keys and the orphan separated, and assert every key on the clean record resolves (AC1).
5. Add AC2: the orphan PLAN-SYN-0777 with no view row, one break row with key type PLAN, reason NO_ACE_ROW and owner role RW-DATASTEW, the treatment still readable at PENDING, and no plan booked (X3).
6. Add AC3: rerun for the same business date, assert one break row for the orphan, equal counts of treatments, approvals and plan links, and one report entry per business date (X4, X5).
7. Add AC4 and the gate: `POST /authorise` for RW-OFF without the Platform administration right, 403 with MSG-P4-002 and no break row written (X7), plus the SCR-45 disagreement path (X6), then the EvidenceReport and the swap of the stub for RWB-P1-DM004-APP when it lands.

**Feature switch.** None. The harness is a test scope and runs only against the environment under test; no flag guards it and no production flag is read or set.

**Done when.** The tests of section 16 pass for the four owned criteria; AC1 and the three new criteria pass against the stub set on Day 1 and again, unchanged, against RWB-P1-DM004-APP when it lands; and the wave entry check holds a run report keyed by story and business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The DP04 freshness is late, so JOB-04 cannot reconcile the treatment records | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-012 | The reconciliation extract and the SCR-45 answer disagree on the breaks or the counts | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | A required key is missing from the fixture or from a read | Enter {field}. |
| MSG-P4-002 | A caller without the Platform administration right asks for a reconciliation run | You cannot {action} here. Your role does not include it. |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a run failure points at a service and a message and not only at a business date.

### 15. Screens and states

SCR-45 Data quality, the screen the legacy story names, shows the breaks this harness reads, in the two states the legacy story names:

| State | What the data steward sees | What the harness asserts through the composite route |
|---|---|---|
| Loading | The console is reading the reconciliation of the business date; no break list yet | No break assertion is made while the state is Loading, and the run waits for the answer or fails with X1 |
| Breaks | The break list with each key, its type, its reason and its owner role, and the referential completeness of the business date | One row for plan_ref PLAN-SYN-0777 with key type PLAN, reason NO_ACE_ROW and owner role RW-DATASTEW, agreeing with the reconciliation extract (AC1, AC2) |

The harness renders no screen. It reads these states through the gateway-bff composite route (DP-19) and through the rwb-source-data and rwb-treatment contracts, so a passed run means the console has the right data behind it. The screen behaviour itself stays with the owning APP stories, and the console itself is RWB-AD-019. What the wave entry check looks at instead is the run report, whose format and retention: Not specified in the source documents (GAP-0444; ASM-0636).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-004-01-ITG | AC1 (legacy); ITG AC1 | Integration | Synthetic case RW-2026-000604 and treatment TRT-0604 with DP01, DP02 and DP04 rows present |
| TC-DM-004-02-ITG | AC2 (legacy); ITG AC1, ITG AC2 | Integration | One plan_ref PLAN-SYN-0777 with no view row |
| TC-DM-004-03-ITG | AC3 (legacy, owned by RWB-P1-DM004-APP); ITG AC3 | Integration | Two JOB-04 runs for business date 2026-12-31 |
| TC-DM-004-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |

The integration cases above are the ITG copies of the legacy cases of the same number and carry the legacy data unchanged; the component copy keeps the legacy level. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the offer amount, the approval level, the treatment type, the plan status, the break reasons and the owner role mapping are data in the fixture, not code.
- No personal data in logs, fixtures, reports, tests or prompts: the synthetic keys are not personal data, and the report names IDs, keys, codes and dates only.
- No cross-schema read and no read of another service's tables: every read goes through the owning contract (DP-01), and ACE data only through rwb-source-data (DP-05, D-RCV-35, ADR-010).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (Architecture v5 slide 11).
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a treatment, a case, a plan, a break row or a reconciliation result by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-004 Migrate treatment and offers | Recovery Workbench Data Migration Stories v4, section RWB-DM-004 | Split; this story owns the wave 4 cutover reconciliation harness, RWB-P1-DM004-APP owns the extract and the cutover |
| Legacy AC2 Reconcile the business keys, verbatim: "Given the migrated records When the REC-05 step runs Then every business key on a migrated record resolves to its view row, account_key and person_key included And each orphan is listed for the data steward and the ACE team" | Recovery Workbench Data Migration Stories v4, RWB-DM-004 AC2 | Section 7, AC1, with ITG AC2 to ITG AC4 around it |
| Legacy test cases TC-DM-004-01 to TC-DM-004-04 | Recovery Workbench Data Migration Stories v4, RWB-DM-004 | Section 16, as TC-DM-004-01-ITG to TC-DM-004-04-ITG |
| DF-CAS-001 to DF-CAS-055, DF-TRT-001 to DF-TRT-033 and DF-ACE-160 to DF-ACE-177 | Recovery Workbench Data Migration Stories v4, RWB-DM-004 data; Logical Data Model and Data Dictionary | Section 11 |
| DL25, zero tolerance on the reconciliation | Decision Log; REQ-RDF-007 and REQ-RDF-008 | Sections 2, 8 (BR1, BR3) and 12 |
| D-RCV-35 and ADR-010, ACE data only through the views owned by rwb-source-data | Decision Log; ADR-010 | Sections 2, 8 (BR4) and 12.2 |
| RWB-E1-011 Reconciliation and data quality report | Business Requirements Epic 1, RWB-E1-011 with REQ-RDF-007 and REQ-RDF-008 | Sections 5, 12 and 15 |
| DP-05, DP-15 and DP-19 | Template and Rules v1, section R5.5 | Sections 12 and 13 |

### 19. Out of scope

- RWB-P1-DM004-APP: the extract of the legacy treatment and approval records, the read of the plan from `v_ace_plan` and the cutover itself belong there, and so do legacy AC1 and AC3.
- S2's own cutover load, its Flyway sequence and the treatment records it writes (DP-15).
- S2 production code and its CON, APP and DB stories.
- The SCR-45 Data quality console, which is RWB-AD-019, and its screen behaviour, which stays with the owning APP stories.
- The cutover plan, the ten clean days and the data steward sign-off.
- ACE ingestion and the `recovery.v_ace_*` views, which are RWB-ACE-001.
- Platform configuration such as Kafka, Temporal and the gateway-bff routes.
- The other data migration keys and their harnesses.
- Any production endpoint, table, event, workflow, Schedule or screen: this story builds a test harness and its evidence only, and the behaviour it proves is built by RWB-P1-DM004-APP and S2.
