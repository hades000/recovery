# RWB-ITG-E2010-ITG Stage 2 data products: contracts, plans and treatments
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2010-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-010 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2004-APP, RWB-P1-E2010-APP, RWB-S2-E2010-APP, RWB-S3-E2010-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-010 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the integration and QA team**, I want **a repeatable cross-service journey harness for the stage 2 data products DP04 (treatments, plans, contracts and guarantee claims) across rwb-source-data, rwb-case, rwb-treatment and rwb-guarantee**, so that **the DP04 build, the read join and the access gate are proven end to end, with evidence, before the wave 2 release is accepted**.

This story builds the harness and the evidence only. It builds no production endpoint, no screen, no table, no migration, no workflow and no schedule; it serves no operation, it owns no table and it starts no workflow of its own. The real behaviour is owned by the four I stories RWB-P3-E2004-APP (the case, account link and scope reads of rwb-case), RWB-P1-E2010-APP (the DP04 stage 2 build, the snapshot tables, the freshness stamp, the count check, the references break and the DP04 read in rwb-source-data), RWB-S2-E2010-APP (the treatment record and the treatment contract of rwb-treatment) and RWB-S3-E2010-APP (the guarantee claim contract of rwb-guarantee), and those four stories block the ITG run.

### 2. Business rationale

The legacy RWB-E2-010 journey crosses more than one service and more than one kind of data. rwb-treatment owns the treatment record, rwb-guarantee owns the guarantee claim, rwb-case owns the case and its account links, rwb-source-data owns the ACE view contract, the DP04 snapshot tables, the freshness stamp, the catalog entry and the access rows, and rwb-access answers the role check. The legacy story carried the build, the read and the access gate in one module against one recovery schema; the split puts the build in RWB-P1-E2010-APP, the treatment contract in RWB-S2-E2010-APP, the claim contract in RWB-S3-E2010-APP and the case and account links in RWB-P3-E2004-APP, and leaves this story the proof that the four parts agree on one business date.

What the harness proves, in one repeatable run per business date:

- JOB-02 stage 2 runs only after DP01 is stamped for the business date from a COMPLETE ALS batch, and the step state is Complete or Failed on the run.
- 40 active treatments and 5 TCG claims reach dp_treatment and dp_guarantee_claim for business date 2026-12-14, each row linked to its case.
- The contract number and contract date are read from v_ace_account and the plan terms from v_ace_plan at request time and are never copied into a Workbench table, so the read join is exercised on every call rather than on a snapshot.
- The DP04 freshness stamp is written for the day only when the count check agrees, and the catalog entry names Workbench for treatment and claim and the two ACE views for the contract and plan facts.
- A guarantee claim that names a case that does not exist is held on the break list with check References and is not written to dp_guarantee_claim.
- A role with no DP04 access row is refused with MSG-P4-002 and the refusal is logged, while the data steward read still answers.
- A repeat run for the same business date leaves the row count and the stamp unchanged, and the end-of-day boundary is 00:00:00 of the next day.

It meets REQ-RDF-014 (the stage 2 data products exist before the first treatment goes live) and REQ-RDF-010 (access to each data product is controlled per role, with personal data masked) at the integration level, and it leaves every business rule, every message and every screen behaviour where the owning stories put them.

### 3. Preconditions

- The four I stories are published and deployed in the SIT environment, or their published contracts and the §12.8 fakes stand in for them: RWB-P3-E2004-APP (case, account links and scope reads), RWB-P1-E2010-APP (DP04 stage 2 build, snapshot tables, freshness, catalog, breaks and the DP04 read), RWB-S2-E2010-APP (treatment record and treatment contract) and RWB-S3-E2010-APP (guarantee claim contract).
- Business date 2026-12-14 and the ACE batch for ALS for it is COMPLETE at 06:20, with DP01 stamped for the day.
- The treatment module holds 40 active treatments, 12 of them restructure plans with installments published in v_ace_plan, and 9 of the 12 plans carry a credit approval recorded on the case by the restructuring officer.
- 5 TCG guarantee claim records exist for 5 existing cases, with claimed amounts from 180,000.00 to 1,250,000.00 baht.
- data_product_access version "DPA-2026.12" gives DP04 read to RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT, and gives no DP04 access row to RW-PHONECOL.
- gateway-bff is deployed with the composite route of DP-19 available for the DP04 read.
- The harness environment, its seeding of the 40 treatments, the 12 plans and the 5 claims, its evidence format and retention, and its pass or fail gate: Not specified in the source documents (GAP-0392; ASM-0567).
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date 2026-12-14 and the versions of the four contracts it is about to exercise.
2. Harness: seeds the 40 active treatments through the rwb-treatment contract — of which 12 are restructure plans with installments published in v_ace_plan and 9 carry a credit approval recorded on the case — the 5 TCG guarantee claims through the rwb-guarantee contract, the case links and primary account key of case RW-2026-000512 through the rwb-case contract, and the ACE facts through the rwb-source-data contract or its fake: the contract number and contract date on v_ace_account and the plan terms on v_ace_plan. It reads each seed back and asserts the seeded state.
3. Harness: observes the stage 2 step of JOB-02 for 2026-12-14, started by the AceDataReady event of the day, and records the step state, its start and end, and the business date it built.
4. Harness: asserts 40 dp_treatment rows for 2026-12-14 and 5 dp_guarantee_claim rows, each linked to its case, and asserts that no row was written for the claim of unknown case UUID 00000000-0000-0000-0000-000000000997.
5. Harness: reads DP04 for case RW-2026-000512 through the gateway-bff composite route and asserts the contract number and contract date of its primary account from v_ace_account and the plan terms from v_ace_plan at request time, with no contract or plan value held on a snapshot row.
6. Harness: asserts the DP04 freshness stamp for 2026-12-14 with status LOADED, and the catalog entry that names Workbench for treatment and guarantee claim and v_ace_account and v_ace_plan for the contract and plan facts.
7. Harness: asserts the count check — 40 built rows against 41 from the owning module — holds the stamp, keeps 2026-12-13 as the latest published day and lists a break with MSG-P1-002 naming 40 and 41, and that no snapshot for 2026-12-14 is published.
8. Harness: asserts the references break for the unknown case, then the access refusal of user u-phone-02 holding RW-PHONECOL with MSG-P4-002 and the logged refusal, alongside a data steward read that still answers.
9. Harness: repeats the step for 2026-12-14 and asserts 40 rows with no duplicate and an unchanged stamp, then asserts the end-of-day boundary with treatment TRT-SYN-0601 changed at 2026-12-14T23:59:59+07:00 and TRT-SYN-0602 changed at 2026-12-15T00:00:00+07:00.
10. Harness: forces the treatment contract to fail, asserts MSG-GEN-006 and MSG-P1-001 and that the 2026-12-13 rows and the previous published day stand, then returns the fake to its healthy answer.
11. Harness: writes one run report per business date, keyed by story and business date, and evaluates the pass or fail gate; the report format, its retention and the gate: Not specified in the source documents (GAP-0392; ASM-0567).

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A role without a DP04 access row reads the product: user u-phone-02 holding RW-PHONECOL | 403 on the DP04 read; the refusal is logged with user u-phone-02 and product DP04; the data steward read still answers | MSG-P4-002 | TC-E2-010-03-ITG |
| X2 | A guarantee claim names case UUID 00000000-0000-0000-0000-000000000997, which does not exist | No row in dp_guarantee_claim for that claim; the break list holds it with product DP04 and check References; the other 5 claims are written | None | TC-E2-010-04-ITG |
| X3 | TreatmentQuery, and the treatment contract, is unavailable | The step ends FAILED with MSG-GEN-006 for system Treatment; dp_treatment keeps the 2026-12-13 rows; DP04 is stale at 08:00 with MSG-P1-001 and the date 2026-12-13 | MSG-GEN-006, MSG-P1-001 | TC-E2-010-05-ITG |
| X4 | The step runs again for the same business date 2026-12-14 | Still 40 rows for 2026-12-14 and no duplicate; the freshness stamp is unchanged | None | TC-E2-010-06-ITG |
| X5 | The active treatment count differs: 41 from the owning module against 40 built rows | No stamp for 2026-12-14; a break with check "Active treatment count 40 against 41" is listed for the data steward; 2026-12-13 stays the latest published day | MSG-P1-002 | TC-E2-010-07-ITG |
| X6 | A treatment changed at the end of business date 2026-12-14 | TRT-SYN-0601 changed at 2026-12-14T23:59:59+07:00 is in the 2026-12-14 build; TRT-SYN-0602 changed at 2026-12-15T00:00:00+07:00 is not | None | TC-E2-010-08-ITG |
| X7 | The count matches but no DP04 freshness stamp is written for the day | The run fails the freshness assertion, the report names the missing stamp for 2026-12-14, and the previous published day is unchanged | None | TC-E2-010-01-ITG |
| X8 | The seed cannot be loaded through the owning contracts or the fakes | The run refuses to start and names the missing seed item; no scenario is reported as passed | None | All |
| X9 | Another run holds the harness environment lock | The run refuses to start and names the lock holder; nothing is seeded and no evidence is produced | None | All |
| X10 | The evidence report cannot be written or attached | The run is marked failed with the local evidence kept for rerun and the gate stays closed | None | All |
| X11 | A role without the platform administration right, RW-TRIBE, reads the data quality list | 403 with MSG-P4-002 and the refusal logged; the data steward read of the same list is allowed | MSG-P4-002 | TC-E2-010-09-ITG |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on its own once the four I stories are deployed; until then it runs against the §12.8 fakes, and it builds no service feature |
| Negotiable | The harness pack, the seed pack and the evidence format are agreed with QA; no business value is fixed by the harness |
| Valuable | The DP04 build, the read join to the two ACE views and the access gate are proven once across four services, with the counts and the stamp on the evidence |
| Estimable | One harness project, one journey specification, one fake pack for five services and one run report |
| Small | Fits in one iteration with the owning stories' contract tests |
| Testable | Each scenario of §7 is one automated journey on synthetic data with a machine-checkable result |

### 7. Acceptance criteria

These four criteria are new for the ITG harness. The legacy RWB-E2-010 AC1 to AC8 are owned by the app stories of the split, RWB-P1-E2010-APP first, and are cited here only through their `-ITG` test cases.

```gherkin
Feature: Stage 2 data products: contracts, plans and treatments - wave 2 integration harness

  Background:
    Given business date 2026-12-14 and the ACE batch for ALS for it is COMPLETE at 06:20, with DP01 stamped for the day
    Given the treatment module holds 40 active treatments, 12 of them restructure plans with installments published in v_ace_plan, and 9 of the 12 plans carry a credit approval recorded on the case
    Given 5 TCG guarantee claim records exist for 5 existing cases
    Given data_product_access version "DPA-2026.12" gives DP04 read to RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE and RW-AUDIT and no DP04 access row to RW-PHONECOL

  Scenario: AC1 The composite DP04 read through gateway-bff (new, D-RCV-60)
    Given the harness seeds the 40 treatments and the 5 claims through the rwb-treatment and rwb-guarantee contracts and the case links of case "RW-2026-000512" through rwb-case
    When the harness reads DP04 for "RW-2026-000512" through the gateway-bff composite route for 2026-12-14
    Then the answer carries the contract number and contract date of the primary account of "RW-2026-000512" from v_ace_account and the plan terms from v_ace_plan, read at request time
    And dp_treatment holds 40 rows for 2026-12-14 and dp_guarantee_claim holds 5 rows, each linked to its case
    And the DP04 freshness status is "LOADED" for 2026-12-14
    And the catalog entry names system of record "Workbench" for treatment and guarantee claim and names v_ace_account and v_ace_plan for the contract and plan facts
    And no service reads another service's schema and no snapshot row holds a contract or a plan value
    And the run report holds one trace spanning the gateway and each owning service

  Scenario: AC2 The count check holds the publish (new, D-RCV-60)
    Given the stage 2 step of JOB-02 starts for 2026-12-14 from the AceDataReady event of the day
    When the step has loaded the 40 treatments and the 5 claims and the count check reads 41 active treatments from the owning module against 40 built rows
    Then DP04 is not stamped for 2026-12-14
    And 2026-12-13 stays the latest published day
    And the data quality break list holds the break with MSG-P1-002 naming 40 and 41
    And no snapshot for 2026-12-14 is published

  Scenario: AC3 The references break and the access refusal (new, D-RCV-60)
    Given a TCG claim names case UUID "00000000-0000-0000-0000-000000000997", which does not exist
    And user "u-phone-02" holds RW-PHONECOL, which has no DP04 access row
    When the stage 2 step runs for 2026-12-14 and the user calls the DP04 read for "RW-2026-000512"
    Then the claim is held on the break list with product "DP04" and check "References" and is not written to dp_guarantee_claim
    And the read is refused with status 403 and MSG-P4-002
    And the refusal is logged with user "u-phone-02" and product "DP04"
    And the data steward read of the same product still answers

  Scenario: AC4 A repeat run and the end-of-day boundary (new, D-RCV-60)
    Given the stage 2 step completed for 2026-12-14 with 40 treatment rows
    And treatment "TRT-SYN-0601" changed at 2026-12-14T23:59:59+07:00 and treatment "TRT-SYN-0602" changed at 2026-12-15T00:00:00+07:00
    When the step runs again for 2026-12-14
    Then dp_treatment still holds 40 rows for 2026-12-14 with no duplicate
    And "TRT-SYN-0601" is in the 2026-12-14 build and "TRT-SYN-0602" is not
    And the DP04 freshness stamp for 2026-12-14 is unchanged
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | DP04 holds treatments and guarantee claims from the Workbench, and contract and plan facts read from v_ace_account and v_ace_plan, with one system of record and one owner for each part | REQ-RDF-014; data_product DP04; sys_objects |
| BR2 | No Workbench table copies a contract, a plan or an account; the views are read at request time | D-RCV-35 U1; tier map section 9 |
| BR3 | Every snapshot row links to an existing case, or it is held on the break list and retried with the next build | DQ load check "References" |
| BR4 | The product is stamped for the day only when the active count matches the owning module, with zero tolerance | DL25; RWB-E1-011 hold rule (FEAT-RDF-13) |
| BR5 | A role reads DP04 only through an access row in force | data_product_access; REQ-RDF-010 |
| BR6 | Credit approval for a restructure is recorded on the case by the officer; there is no interface to NLEADS | INT-26; DL12 |
| BR7 | Plan installments come from the ACE plan published calculation | DF-ACE-174 source ACE; INT-34 |

The seven rules are copied unchanged from RWB-E2-010 and the split changes none of them. The harness asserts them across the service boundaries and re-implements none of them: the count, the access rows, the expected-by time and the tolerance are data held by rwb-source-data and rwb-access, and the harness holds no copy.

### 9. State transitions

None for the case. This story changes no case status. It observes the DP04 freshness status and the state of the stage 2 step of the JOB-02 run:

| Observed | After a build that matches | After a build that is refused or fails |
|---|---|---|
| DP04 freshness status | LOADED for 2026-12-14 | STALE, with 2026-12-13 as the latest published day |
| Stage 2 product step of JOB-02 | Complete | Failed |

The harness adds a run state of its own only: Not started, Seeding, Running, Passed, Failed, with the latest run for a build deciding the gate. A failed run leaves every row in rwb-source-data exactly as it was before the run.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Owns DP04; reads the catalog entry and the breaks; supplies the control read of AC3 |
| RW-CASEOWN, case owner | Reads DP04 for cases in scope; the harness drives this read for case RW-2026-000512 |
| RW-RESTRUCT, restructuring officer | Reads DP04 for the restructure plans in scope, including the plan terms of v_ace_plan |
| RW-GUARANT, guarantee officer | Reads DP04 for the guarantee claims of the cases in scope |
| RW-CREDITAD, Credit Administration officer | Reads DP04 for the cases in scope, including the 9 plans with a credit approval |
| RW-COE, center of excellence analyst | Reads DP04 for all cases |
| RW-AUDIT, audit | Reads DP04 for all cases |
| RW-PHONECOL | Holds no DP04 access row; refused with MSG-P4-002, and the refusal is asserted |
| The integration and QA team | Runs the harness, keeps the fake pack, the seed pack and the evidence, and reads the reports |

No approval level from the delegation of authority applies: the journey reads data products and takes no business decision. Authorisation is answered by rwb-access through the authorise operation of §12.2.

### 11. Data

The harness owns no table. It seeds and reads the fields below through the owning services' contracts and asserts them; the field IDs are those of the Logical Data Model and Data Dictionary.

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read through the S2 treatment contract |
| DF-TRT-002 | treatment | case_id | Read through the S2 treatment contract |
| DF-TRT-003 | treatment | decision_log_id | Read through the S2 treatment contract |
| DF-TRT-004 | treatment | treatment_type | Read through the S2 treatment contract |
| DF-TRT-005 | treatment | proposed_by | Read through the S2 treatment contract |
| DF-TRT-006 | treatment | proposed_at | Read through the S2 treatment contract |
| DF-TRT-007 | treatment | offer_amount | Read through the S2 treatment contract |
| DF-TRT-008 | treatment | haircut_amount | Read through the S2 treatment contract |
| DF-TRT-009 | treatment | installments | Read through the S2 treatment contract |
| DF-TRT-010 | treatment | valid_until | Read through the S2 treatment contract |
| DF-TRT-011 | treatment | approval_level | Read through the S2 treatment contract |
| DF-TRT-012 | treatment | booked_at | Read through the S2 treatment contract |
| DF-TRT-013 | treatment | outcome | Read through the S2 treatment contract |
| DF-TRT-014 | treatment | outcome_at | Read through the S2 treatment contract |
| DF-TRT-015 | guarantee_claim | id | Read through the S3 guarantee claim contract |
| DF-TRT-016 | guarantee_claim | case_id | Read through the S3 guarantee claim contract |
| DF-TRT-017 | guarantee_claim | claim_type | Read through the S3 guarantee claim contract |
| DF-TRT-018 | guarantee_claim | claim_deadline | Read through the S3 guarantee claim contract |
| DF-TRT-019 | guarantee_claim | claimed_amount | Read through the S3 guarantee claim contract |
| DF-TRT-020 | guarantee_claim | filed_at | Read through the S3 guarantee claim contract |
| DF-TRT-021 | guarantee_claim | paid_amount | Read through the S3 guarantee claim contract |
| DF-TRT-022 | guarantee_claim | status | Read through the S3 guarantee claim contract |
| DF-ACE-001 | v_ace_account | account_key | Read through the P1 DP04 read; seeded through the P1 contract |
| DF-ACE-006 | v_ace_account | contract_no | Read through the P1 DP04 read |
| DF-ACE-007 | v_ace_account | contract_date | Read through the P1 DP04 read |
| DF-ACE-160 | v_ace_plan | plan_ref | Read through the P1 DP04 read |
| DF-ACE-174 | v_ace_plan | installments | Read through the P1 DP04 read |
| DF-ACE-175 | v_ace_plan | recommended_installment | Read through the P1 DP04 read |
| DF-ACE-168 | v_ace_plan | booked_at | Read through the P1 DP04 read |
| DF-TRT-034 to DF-TRT-051 | dp_treatment | all fields | Read through the P1 DP04 read; written by RWB-P1-E2010-APP, never by the harness |
| DF-TRT-052 to DF-TRT-061 | dp_guarantee_claim | all fields | Read through the P1 DP04 read; written by RWB-P1-E2010-APP, never by the harness |
| DF-OPS-001 to DF-OPS-009 | data_product_load | all fields | Read through the P1 freshness and catalog operations; written by RWB-P1-E2010-APP, never by the harness |

The treatment and guarantee_claim fields are read through the rwb-treatment and rwb-guarantee contracts, not from their tables. v_ace_account and v_ace_plan are read only through the rwb-source-data contract; the harness reads no ACE view directly (DP-05). Test data is synthetic: no production case, account, treatment or claim is used, and no personal data is written to a run report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

One hop per call, no chaining; the 2 s timeout and the circuit breaker per downstream of DP-11 apply to every row.

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/source-data/v1/data-products/DP04/records` | P1 rwb-source-data | The DP04 read for a case, with the snapshot rows joined to v_ace_account and v_ace_plan at request time (AC1, AC3); `?caseId=` |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The DP04 freshness stamp of the business date, LOADED or STALE, and the latest published day (AC2, AC4) |
| GET | `/api/recovery/source-data/v1/admin/data-products` | P1 rwb-source-data | The DP04 catalog entry and its systems of record (AC1) |
| GET | `/api/recovery/source-data/v1/admin/data-quality/exceptions` | P1 rwb-source-data | The References break and the count break of the business date (AC2, AC3, X11) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Reruns the stage 2 step of JOB-02 for the business date (AC4, X4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case and its primary account key for case RW-2026-000512 (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | The account links of the case that the DP04 read resolves in v_ace_account (AC1) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | The treatment record seeded for the 40 rows and for TRT-SYN-0601 and TRT-SYN-0602 (AC1, AC4) |
| POST | `/api/recovery/guarantee/v1/cases/{caseId}/guarantee-claims` | S3 rwb-guarantee | Seeds the 5 TCG claims and the claim for unknown case UUID 00000000-0000-0000-0000-000000000997 (AC2, AC3); the contract may answer with no claims until RWB-S3-E2010-APP lands |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The DP04 read decision for u-phone-02 holding RW-PHONECOL, for RW-TRIBE and for the data steward (AC3, X11) |

The composite DP04 route through gateway-bff is DP-19, owned by the platform edge story RWB-PLT-N001-CON. Its path and merge order: Not specified in the source documents (GAP-0392; ASM-0567).

#### 12.3 Events published

None. The harness publishes no Kafka event of its own; the AceDataReady event of the day is published by rwb-source-data and only replayed through its test profile.

#### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The event of 2026-12-14 is published after the ALS batch is COMPLETE at 06:20 and is what starts the stage 2 step of JOB-02 (AC2) |
| `rwb.treatment.TreatmentApproved.v1` | `rwb.treatment.events.v1` | S2 rwb-treatment | The approval of a restructure plan reaches the topic inside the run window, so the 9 plans with a credit approval are the ones dp_treatment carries (AC1) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (ledger); every service publishes its own record | The record of the treatment approval reaches the shared topic and names the case and the treatment, alongside the treatment read of §12.2 (AC1) |

Consumers dedupe through their own inbox table; the harness consumes with its own group and never asserts a producer's outbox row.

#### 12.5 Workflows and activities

JOB-02 Case creation, stage 2 product step, is exercised and not built: an event-started step started by `AceDataReady` for the business date, running on queue `rwb-case` as part of DailyCaseRun or on the P1 stage-2 worker, per the owning story RWB-P1-E2010-APP. The harness records the workflow ID, the business date and the state of the step, and asserts the snapshot rows, the breaks and the stamp afterwards.

No workflow is built, no activity is added and no schedule is created by this story.

#### 12.6 Schedules

None. The harness run is started by the test pipeline, not by a Temporal Schedule and not by Airflow; the daily step it observes is started by the event of §12.4.

#### 12.7 Tables owned

None. The harness owns no table in any schema (DP-01); it seeds and reads through the operations of §12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Stubbed answers |
|---|---|---|
| rwb-source-data | data-products/DP04/records, data-products/freshness, admin/data-products, admin/data-quality/exceptions, admin/jobs/{jobId}/rerun | DP04 for RW-2026-000512 with the contract number and contract date of its primary account and the plan terms, 40 dp_treatment rows for 2026-12-14 and 5 guarantee claims; freshness LOADED for 2026-12-14, STALE with 2026-12-13 after a failed step, and no stamp for the AC2 hold; the catalog entry with Workbench for treatment and claim; the References break for UUID 00000000-0000-0000-0000-000000000997 and the count break naming 40 and 41 with MSG-P1-002; 403 with MSG-P4-002 for RW-PHONECOL and for RW-TRIBE on the admin list; 503 with MSG-GEN-006 for the forced treatment failure; 409 with MSG-P2-006 for a rerun while the step runs |
| rwb-case | cases/{caseId}, cases/{caseId}/accounts | RW-2026-000512 with its primary account key and its account links; the 5 cases of the guarantee claims; no case for UUID 00000000-0000-0000-0000-000000000997 |
| rwb-treatment | treatments/{treatmentId} | The 40 active treatments, of which 12 are restructure plans and 9 carry a credit approval; TRT-SYN-0601 changed at 2026-12-14T23:59:59+07:00 and TRT-SYN-0602 at 2026-12-15T00:00:00+07:00; a forced error for the AC5 case |
| rwb-guarantee | cases/{caseId}/guarantee-claims | The 5 TCG claims of existing cases and the claim for the unknown case UUID; an empty list for every case until RWB-S3-E2010-APP lands |
| rwb-access | authorise | Allow the DP04 read for RW-CASEOWN, RW-RESTRUCT, RW-GUARANT, RW-CREDITAD, RW-COE, RW-AUDIT and RW-DATASTEW; refuse RW-PHONECOL and RW-TRIBE with MSG-P4-002 |

The fakes are replaced by the real service as each I story lands, contract by contract. The harness environment, its repository, its seeding of the 40 treatments, the 12 plans and the 5 claims, its evidence format and retention, and its pass or fail gate: Not specified in the source documents (GAP-0392; ASM-0567).

#### 12.9 Call-type summary

| Call type | Used | Detail |
|---|---|---|
| REST | Yes | Ten consumed operations of §12.2 through gateway-bff and the owning services; one hop, 2 s timeout, breaker per downstream |
| Kafka | Yes | Consumes `rwb.source-data.AceDataReady.v1`, `rwb.treatment.TreatmentApproved.v1` and `rwb.decision-record.DecisionRecorded.v1`; publishes nothing |
| Temporal | Observed only | Starts no workflow and adds no activity; it observes the stage 2 step of JOB-02 through the P1 operations and records its state |
| File | No | Reads and writes no file itself; the run report is written by the pipeline reporter of §13 |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies named by this table are delivered by the platform wave and are not repeated in the metadata H list; the harness has no build dependency of its own. The blocking dependencies of this story are the four I stories RWB-P3-E2004-APP, RWB-P1-E2010-APP, RWB-S2-E2010-APP and RWB-S3-E2010-APP, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Test harness | Runs the eleven flow steps for the business date, keyed by story and business date, takes the environment lock, and stops at the first failed assertion with the trace |
| CompositeRouteClient | Harness adapter | Calls the gateway-bff composite DP04 route and the ten consumed operations of §12.2, one hop each with the 2 s budget |
| FakePack | WireMock project | Serves rwb-source-data, rwb-case, rwb-treatment, rwb-guarantee and rwb-access from the published contract documents of §12.8 |
| Stage2Fixture | Data | The seeded 40 active treatments with 12 restructure plans and 9 credit approvals, the 5 TCG claims, the case links of RW-2026-000512, the ACE contract and plan facts, TRT-SYN-0601 and TRT-SYN-0602, and the claim of the unknown case UUID |
| JoinAssertion | Assertion | Fails the run when the DP04 answer does not carry the contract number and contract date from v_ace_account and the plan terms from v_ace_plan at request time, or when a snapshot row carries a contract or a plan value |
| CountAssertion | Assertion | Compares 40 built rows against the owning module count, and fails the run when the stamp is written on a difference or when a break with MSG-P1-002 is missing |
| AccessAssertion | Assertion | Fails the run when RW-PHONECOL or RW-TRIBE is not refused with MSG-P4-002, when the refusal is not logged, or when the data steward read does not answer |
| RunReportWriter | Reporter | Writes one run report with the trace, the per-assertion result and the gate outcome; format and retention Not specified in the source documents (GAP-0392; ASM-0567) |

**Environment and test data**

- Environment: SIT, one namespace, the four owning services deployed from their wave 2 builds or replaced by the §12.8 fakes. Harness repository, environment, seeding mechanism and evidence format: Not specified in the source documents (GAP-0392; ASM-0567).
- Data: business date 2026-12-14 with the ALS batch COMPLETE at 06:20, 40 active treatments, 12 restructure plans with installments in v_ace_plan, 9 credit approvals, 5 TCG claims, case RW-2026-000512, user u-phone-02 holding RW-PHONECOL, TRT-SYN-0601, TRT-SYN-0602, case UUID 00000000-0000-0000-0000-000000000997, data_product_access version DPA-2026.12 and the prior published day 2026-12-13. No production record is copied.
- Reset: each run starts from the seeded state for 2026-12-14, so a repeated run is deterministic and the same report is produced.

**Build steps**

1. Build JourneyRunner and CompositeRouteClient against the published contract documents of rwb-source-data, rwb-case, rwb-treatment, rwb-guarantee and rwb-access.
2. Publish FakePack for the five services from the same documents, and prove the harness runs green from Day 1 on the fakes.
3. Write Stage2Fixture with the 40 treatments, the 12 plans, the 9 approvals, the 5 claims and the case links, and test that a bad seed stops the run (X8).
4. Add the DP04 read assertion of AC1 through gateway-bff, with JoinAssertion, the catalog systems of record and the one-trace check.
5. Add the stage 2 observation and the count check of AC2 with CountAssertion, including the held stamp and the break naming 40 and 41.
6. Add the references break and the access set of AC3 with AccessAssertion, including the logged refusal and the data steward control read.
7. Add the repeat run and the end-of-day boundary of AC4, then the forced treatment failure with MSG-GEN-006 and MSG-P1-001, and the lock and evidence failures of X9 and X10.
8. Replace each fake with the real service as its I story lands, publish the run report per business date, and evaluate the pass or fail gate: Not specified in the source documents (GAP-0392; ASM-0567).

**Feature switch:** the harness has no production feature flag and runs in the test environment only. The production switch it exercises is `rwb.dataengine.stage2-products` from the legacy solution plan: with it off the stage 2 step does not run, DP04 keeps the previous published day, and the harness asserts that state as the AC2 and AC5 baseline; with it on the step runs and the scenarios of §7 apply.

**Done when:** the journey runs green against the four deployed I stories in SIT, the run report for 2026-12-14 holds every assertion of §7 and §16 with its trace, the DP04 catalog entry shows in the admin data product read with Workbench and the two ACE views as systems of record, and the pass or fail gate agreed with QA is met for one full business date.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | Role without a DP04 access row | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | DP04 stale after a failed step | {product} is from {date}. Today's load has not arrived. |
| MSG-P1-002 | Count check break held the publish | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-GEN-006 | TreatmentQuery or GuaranteeClaimQuery unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P2-006 | Rerun while JOB-02 is running | {job} is already running. Wait for it to finish before you rerun it. |

The harness asserts the message ID and the substituted values; it does not own the message text. For MSG-P1-001 the {product} value is DP04 and {date} is 2026-12-13; for MSG-P1-002 the {source} value is DP04, {date} is 2026-12-14 and {check} is "Active treatment count 40 against 41"; for MSG-GEN-006 the {system} value is Treatment. Thai text for each message follows decision DL10.

### 15. Screens and states

| Screen | State | What the harness asserts |
|---|---|---|
| SCR-45 Data quality | Loading | The break list answers for the data steward, so the Loading state of the list is reached through the admin data quality operation |
| SCR-45 Data quality | Breaks | The list shows the DP04 References break for UUID 00000000-0000-0000-0000-000000000997 and the count break naming 40 and 41 for 2026-12-14 |
| SCR-03 Case record | DP04 read | The composite route returns the treatments, the guarantee claims, the contract number and contract date from v_ace_account and the plan terms from v_ace_plan for case RW-2026-000512 |
| SCR-03 Case record | Refused | The answer for user u-phone-02 carries 403 with MSG-P4-002, and the refusal is logged |

The settlement, TDR and DIL screens that consume DP04 come in Epic 3 and are out of scope. The harness opens no screen and renders no page; it asserts the operations behind those screens, and screen-level behaviour remains with the owning app stories. The harness environment and its evidence detail: Not specified in the source documents (GAP-0392; ASM-0567).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-010-01-ITG | AC1, BR1, BR2, BR6, BR7 | Integration | 40 synthetic treatments, 12 plans, 9 approvals |
| TC-E2-010-02-ITG | AC2, BR1 | Integration | 5 TCG claims for existing cases |
| TC-E2-010-03-ITG | AC3, BR5 | Integration | RW-PHONECOL reads DP04 |
| TC-E2-010-04-ITG | AC4, BR3 | Integration | TCG claim for an unknown case ID |
| TC-E2-010-05-ITG | AC5 | Integration | TreatmentQuery stub returning errors |
| TC-E2-010-06-ITG | AC6 | Integration | Step run twice for 2026-12-14 |
| TC-E2-010-07-ITG | AC7, BR4 | Integration | countActive() 41 against 40 rows |
| TC-E2-010-08-ITG | AC8 | Integration | Changes at 23:59:59 and 00:00:00 |
| TC-E2-010-09-ITG | Access | Component | RW-TRIBE calls GET /admin/data-quality/exceptions; refused with MSG-P4-002 |

The full legacy test, with its Given, When and Then, is in the legacy test case workbook, tab Story test cases, under the same legacy test case ID. The Covers column names the legacy AC of RWB-E2-010 that the `-ITG` copy is derived from; the Level column maps the legacy System level to Integration and the legacy Access level to Component.

### 17. Guardrails

- No business value in code: the access rows, the expected-by time, the tolerance and the counts are data held by rwb-source-data and rwb-access; the harness reads them and holds no copy.
- No personal data in logs, tests, traces or reports: the treatments, claims and cases are synthetic, and the report holds identifiers, codes, counts and timestamps only.
- No copy of ACE data: the contract number and contract date are read from v_ace_account and the plan terms from v_ace_plan at request time, and the JoinAssertion fails the run when a snapshot row carries a contract or a plan value.
- Treatments and claims go through their contracts: the harness reads rwb-treatment and rwb-guarantee and never their tables, and case links go through rwb-case.
- No call to NLEADS or the Thai Credit Guarantee Corporation: the credit approval arrives as a record on the case and the claim as a record of rwb-guarantee.
- No read of another service's schema and no direct ACE read: every read is an operation of §12.2, and the run fails on any cross-schema reference in the trace.
- One hop only: the harness fails a run when the trace shows a call chain deeper than the gateway and one owner.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration, and the harness never runs against UAT or production.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-014 | Stage 2 data products for contracts, plans and treatments exist before the first treatment goes live | Business Requirements Epic 2, sections 3.1 and 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-E2-010-01-ITG to TC-E2-010-08-ITG |
| REQ-RDF-010 | Access to each data product is controlled per role, and personal data is masked by role in line with PDPA | Business Requirements Epic 1, section 4 | FEAT-CHO-09 | 07 Route, settle and claim | DL25; DL12 | TC-E2-010-03-ITG, TC-E2-010-09-ITG |

The two requirements are exercised at the integration level by the harness; this story adds no requirement ID of its own, and the business rules and the screen behaviour stay with the owning stories.

### 19. Out of scope

- The four owning I stories RWB-P3-E2004-APP, RWB-P1-E2010-APP, RWB-S2-E2010-APP and RWB-S3-E2010-APP, and every screen, endpoint, table, migration, rule and workflow they build.
- Production code in any service: the harness is test and evidence only, and it owns no table.
- The contract baselines of rwb-source-data, rwb-case, rwb-treatment, rwb-guarantee and rwb-access, which their CON stories own.
- Platform deployment, the gateway-bff composite route implementation (RWB-PLT-N001-CON) and the platform configuration of Kafka, Temporal and the observability stack.
- The settlement, TDR and DIL screens of Epic 3 that read DP04.
- Guarantee claim filing and the claim deadline timers (S3, Epic 4).
- The other legacy journeys of RWB-E2-006, RWB-E2-007, RWB-E2-008, RWB-E2-009, RWB-E2-012 and the rest, which their own ITG stories cover.
