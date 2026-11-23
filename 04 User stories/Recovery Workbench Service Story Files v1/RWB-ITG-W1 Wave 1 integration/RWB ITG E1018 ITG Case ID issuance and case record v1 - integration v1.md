# RWB-ITG-E1018-ITG Case ID issuance and case record v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1018-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-018 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP03, DP04, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1001-APP, RWB-P1-E1016-APP, RWB-P1-E1069-APP, RWB-P3-E1018-APP, RWB-P5-E1018-APP, RWB-P1-E1018-APP, RWB-P4-E1018-APP, RWB-P7-E1018-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-020) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-018 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer**, I want **the end-to-end proof of the RWB-E1-018 case creation and case record across rwb-source-data (P1), rwb-case (P3), rwb-access (P4), rwb-document (P5) and rwb-decision (P7)**, so that **the batch gate, the case-created event, the missing-view-row path and the package-in-force refusal are proved on real services before wave 1 exits**.

### 2. Business rationale

RWB-E1-018 creates one recovery case per customer and product at 90 days past due, and every later team, letter and document refers to that case number. The component copy of the behaviour already exists: RWB-P3-E1018-APP owns the legacy criteria AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC10, AC11, AC12 and AC14 in rwb-case, against the published contracts of the services it needs. This integration story owns the four criteria that a single service cannot prove: AC1 (the case is created at the threshold and the creation is announced), AC9 (nothing is created before the ALS batch for the business date is complete), AC13 (a business key with no view row is listed and never invented) and AC15 (no EXCLUSION package in force holds creation for the whole date).

The batch gate is a fact about rwb-source-data, not about rwb-case: the readiness signal, the freshness stamp and the AceDataReady event are produced by the source-data owner, and rwb-case only reacts to them. The case-created fact is a cross-service fact in the same way: the case row commits in rwb-case, the event leaves on the owner's topic and the decision is recorded in the central ledger of rwb-decision, and an assertion on any one of those three alone would pass while the other two were wrong. A missing view row is found by the source-data data quality check, while the link that must not be invented lives in rwb-case. None of the four can be proved inside one service.

The target delta is named in GAP-0343 and ASM-0437. The legacy AC1 publishes the in-process `caseCreated` and the legacy section 12 writes the decision log inside P3; in the target the creation publishes `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` (CloudEvents, key caseId) and the decision is recorded in rwb-decision through the shared topic `rwb.decision-record.v1` (DP-03), asserted through the P7 contract. REC-05, the check that every key resolves to its ACE view row, is a data-quality exception owned by rwb-source-data, so the harness reads its output rather than a P3 table. No service contract is faked in this story: the eight integration dependencies are the real services on their published contracts, and a fake would defeat the purpose of the run.

### 3. Preconditions

- RWB-P1-E1001-APP is done: the recovery tables for the data products, the ACE view contract and the freshness of the ALS data product are in place in rwb_source_data.
- RWB-P1-E1016-APP is done: the ACE source query and its boundary are published, so the account, customer and relation facts are read by the owner and exposed through the P1 contract.
- RWB-P1-E1069-APP is done: the data products, their freshness and the readiness call for a business date are published.
- RWB-P3-E1018-APP is done: case creation exists in rwb-case, with the gate on the readiness signal, the one-case-per-customer-and-product rule, the number issuance and the case read operations.
- RWB-P5-E1018-APP is done: the case document links are created and read through the rwb-document contract.
- RWB-P1-E1018-APP is done: the intake and the reconciliation that produce the missing-key list for the data steward are published.
- RWB-P4-E1018-APP is done: the Case record right and its refusal are enforced by rwb-access.
- RWB-P7-E1018-APP is done: the rule-package version list, the rollback and the central decision ledger are published, and the ENTRY and EXCLUSION packages are loaded and approved.
- The published contracts of P1, P3, P4, P5 and P7 are versioned in the registry, and the harness consumes only those contracts.
- The harness RWB-ITG-W1J01-ITG is available with its synthetic ALS batch and its synthetic case set.
- The SIT environment is available with the Temporal namespace `rwb-recovery`, the topics of the wave-1 services with their retry and `.dlt` topics, the schema registry and the rule packages of the run.
- No production data is read, copied or connected to; every account, customer, person, account key and case number used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: seeds the ACE batch rows for the business date and the synthetic accounts, customers and relations of the RWB-ITG-W1J01-ITG set through the harness; no service schema is opened and no production row is used.
2. Harness: publishes the readiness signal for the business date by calling `POST /api/recovery/source-data/v1/business-days/{date}/ready`, in the same way the Airflow readiness stub does.
3. Harness: consumes `rwb.source-data.AceDataReady.v1` on `rwb.source-data.events.v1` and confirms that the DailyCaseRun workflow started on queue `rwb-case` for that business date.
4. Harness: reads `GET /api/recovery/source-data/v1/data-products/freshness` and confirms that the ALS data product for the business date is fresh before any case is asserted.
5. Harness: reads `GET /api/recovery/case/v1/cases` with the case-number search, then `GET /api/recovery/case/v1/cases/{caseId}` and `GET /api/recovery/case/v1/cases/{caseId}/accounts`; it asserts status "NEW", no stage code, the entry date, the primary person key and the account link with `is_primary` true.
6. Harness: consumes `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` and asserts the CloudEvents envelope, the key caseId, case number RW-2026-000123, product group, accounts and business date, and that no personal data field is present.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log` for the case and asserts one record with decision code "D6", final call "CASE_CREATED", the ENTRY rule ID, the package version "ENTRY-2026.11" and the ALS business date; it also consumes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` for the same creation.
8. Harness, AC9: seeds a second business date 2026-12-02 whose batch row is at status "RUNNING", runs the cut-off check, asserts that no case exists for that date and that the job monitor shows MSG-P1-001, then publishes readiness for 2026-12-02 and asserts that the cases appear.
9. Harness, AC13: takes the synthetic row of account A-5013 and person P-0105 out of the source set through the P1 data set, runs the next intake, asserts that no case and no party link is created, that the existing links of case RW-2026-000126 are unchanged, and that the reconciliation output lists both keys for the data steward.
10. Harness, AC15: reads `GET /api/recovery/decision/v1/admin/rule-packages/EXCLUSION/versions`, rolls the EXCLUSION package back with `POST /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback`, publishes readiness for a new date, asserts that no case is created and that the job record carries MSG-P3-027 with package code "EXCLUSION", then promotes "EXCL-2026.11" again, asserts that creation resumes, and cleans up the synthetic set.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The ALS batch for the business date is still RUNNING at the cut-off | DailyCaseRun does not start for that date, no case is created and the job monitor shows the waiting line for the data product and the date | MSG-P1-001 | AC9 |
| X2 | No EXCLUSION package version is in force on the business date | Creation is held for the whole date, no case exists and the job record names the package-in-force check with the package code | MSG-P3-027 | AC15 |
| X3 | A business key on a case link or in the intake has no row in the source view | No case and no party link is created from the missing row, the existing link is unchanged, and the reconciliation output lists the key | None | AC13 |
| X4 | AceDataReady is delivered twice for the same business date | The consumer inbox ignores the second delivery, the run creates no second case or link, and every account shows one case link | None | AC1, TC-E1-018-08-ITG |
| X5 | The yearly case number range is used up | No case is created for the account, the job record carries the range line with the year and an incident goes to the platform administrator | MSG-P3-025 | TC-E1-018-11-ITG, owned by RWB-P3-E1018-APP |
| X6 | The decision of the creation cannot be recorded | No case exists for the account, the run reports the account as failed and the account is taken again in the next run | MSG-P7-003 | TC-E1-018-10-ITG, owned by RWB-P3-E1018-APP |
| X7 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X8 | The W1J01 synthetic set, or the ACE batch fixture in it, is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC9 |
| X9 | No earlier EXCLUSION version can be rolled back to, or the rollback is refused | The rollback step fails and the run stops; the version in force is reported and creation is not asserted | MSG-P3-027 | AC15 |
| X10 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | Section 17 |

X1 to X3 and X9 are the legacy exception paths carried onto the real services; X4 to X8 are the cross-service failures that only appear when the run leaves one service; X10 is the guardrail of section 17 in testable form.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the eight integration dependencies and the published contracts of P1, P3, P4, P5 and P7, not their source code, and it owns no schema and no table |
| Negotiable | The fixture composition, the poll interval, the cut-off time and the report layout are configuration; the gate behaviour, the message IDs, the case number and the package versions are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: the batch gate, one case per customer and product, one CaseCreated event per creation, one decision record in the central ledger, the missing-view-row path and the package-in-force refusal |
| Estimable | One suite module, one fixture builder, four contract probes, one gate control, one rollback step and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, a workflow result, a ledger record or a data-quality list |

### 7. Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1, proven across the wave 1 services

  Background:
    Given parameter "case.entry.dpd" is 90
    Given package ENTRY version "ENTRY-2026.11" is in force
    Given package EXCLUSION version "EXCL-2026.11" is in force
    Given the business date is 2026-12-01
    Given v_ace_batch_status holds the ALS batch for 2026-12-01 with status "COMPLETED" and is_complete true
    Given all involved services are deployed in SIT with published contracts
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded

  Scenario: AC1 Case created at 90 days past due (legacy RWB-E1-018 AC1)
    Given v_ace_account holds account A-5001 with product_category "HIRE_PURCHASE", days_past_due 90 and data_as_of 2026-12-01, with no exclusion
    Given v_ace_ca_relation holds person_key P-0101 on account A-5001 as "BORROWER" and v_ace_customer holds P-0101
    Given the last case number issued in 2026 is RW-2026-000122
    When AceDataReady is raised for ALS and 2026-12-01 and JOB-02 runs
    Then case RW-2026-000123 exists with status "NEW", no stage code, entry date 2026-12-01 and primary_person_key P-0101
    Then case_account holds account_key A-5001 on that case with is_primary true
    Then case_party holds person_key P-0101 as "BORROWER"
    Then the system publishes caseCreated with case number RW-2026-000123

  Scenario: AC9 No cases before the ALS batch is complete (legacy RWB-E1-018 AC9)
    Given v_ace_batch_status shows the ALS batch for 2026-12-02 with status "RUNNING" at the 09:00 cut-off
    When the morning check runs
    Then JOB-02 does not start for 2026-12-02
    Then the job monitor shows MSG-P1-001 for "DP01 Account and arrears" with date 2026-12-01
    Then JOB-02 starts for 2026-12-02 when AceDataReady is raised for ALS and 2026-12-02

  Scenario: AC13 A key with no view row is listed, never invented (legacy RWB-E1-018 AC13)
    Given case RW-2026-000126 links account_key A-5013 and person_key P-0105
    Given v_ace_account has no row for A-5013 on 2026-12-01 and v_ace_customer has no row for P-0105
    When JOB-02 runs for 2026-12-01 and the intake reads the case links
    Then the system creates no case and no party link from a missing view row
    Then case RW-2026-000126 keeps its existing links unchanged
    Then REC-05 lists account_key A-5013 and person_key P-0105 for the data steward and the ACE team
    Then both keys are read again on the next complete ALS batch

  Scenario: AC15 No EXCLUSION package in force holds creation (legacy RWB-E1-018 AC15)
    Given no EXCLUSION version is in force on 2026-12-01
    When AceDataReady is raised for ALS and 2026-12-01 and JOB-02 runs
    Then the system creates no case for 2026-12-01
    Then the job record carries MSG-P3-027 for the package in force check with package code "EXCLUSION"
    Then the accounts are taken again when an EXCLUSION version is in force
```

**Target reading.** The source views are read only by rwb-source-data and are asserted here through the P1 contract and its freshness stamp; the suite opens no view and no service schema. The case-created event is the Kafka event `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` in the CloudEvents envelope, key caseId, not the in-process `caseCreated` of the legacy criterion. The decision record of a creation is asserted through the P7 contract on `rwb.decision-record.v1` and the P7 decision-log read; the EXCLUSION rollback of AC15 is the P7 admin path, which is the one-call rollback of the rule design. No service table is read and no value is invented (GAP-0343; ASM-0437).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An account enters recovery when `days_past_due` in `v_ace_account` for the ACE business date is at or above the entry threshold and package ENTRY returns ENTER | Parameter case.entry.dpd = 90; package ENTRY; DL16; DF-ACE-018 |
| BR2 | One case per borrower `person_key` and product group, with every qualifying account linked by `account_key` | DL17; REQ-CWC-003 |
| BR3 | An account matching an EXCLUSION rule gets no case; the reason, rule ID and package version are recorded in `case_entry_exclusion` | Package EXCLUSION; REQ-CWC-004 |
| BR4 | The case number is RW, the entry year and a six-digit number from a yearly sequence; it is issued once and never reused | recovery_case.case_no (DF-CAS-002); uk_recovery_case |
| BR5 | A new case has status NEW and no owner until allocation | casemodel.txt Case status "New" |
| BR6 | Status values are read from the list, not from code | LOV-CASE-STATUS; Principle 1 |
| BR7 | No case is created before the ALS batch for the business date is COMPLETED in `v_ace_batch_status`. A late or failed batch raises AceDataLate (EV-27), and the case is created on the next complete batch | CTL-02; JOB-02 "No cases from an incomplete day"; RWB-E1-015 |
| BR8 | Every case creation writes its decision log entry, with the ENTRY rule ID and package version, in the same transaction; a failed write rolls the creation back | Principle 5; R-UNI-39; REQ-CWC-016 |
| BR9 | Exposure band is set from the total outstanding at entry using the band table in force | recovery_case.exposure_band (DF-CAS-015); LOV-EXPOSURE |
| BR10 | A case created on bad data is canceled by rule, never deleted | R-UNI-16 (Epic 2 handling) |
| BR11 | The case links to ACE by business key (`primary_person_key`, `account_key`, `person_key`) with no foreign key. A key with no view row is listed by REC-05 and never invented from a partial record | D-RCV-35 U4; ADR-010; REC-05 |
| BR12 | The primary account is the linked account with the highest `total_balance` on the business date; a tie breaks on the lowest `account_key` | case_account.is_primary (DF-CAS-027); Data Tier Map section 5 |
| BR13 | Entry and exclusion decisions come only from `RuleEvaluator` on packages ENTRY and EXCLUSION. A version not in force holds creation with MSG-P3-027 and is never a default decision | R-UNI-41; D-RCV-36 T3, T5 |
| BR14 | One case per customer and product across the real services: the case is created once in rwb-case, the account link is created once per `account_key`, and a repeated readiness signal for the same business date adds no case and no link | DP-09; REQ-CWC-003; Arch v5 slide 42 (inbox dedupe, key caseId) |
| BR15 | Event first, never a table copy: the creation commits in rwb-case with its outbox row and leaves as `rwb.case.CaseCreated.v1` on `rwb.case.events.v1`; the decision leaves as `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; the suite reads no copy of either | ADR-015; DP-03; DP-09 |
| BR16 | No cross-service table read: the suite and every service read another service's data through its contract only, and the source views stay behind rwb-source-data | DP-01; DP-05; ADR-020 |
| BR17 | One hop and two seconds: every REST call of the run goes to the owning service, behind gateway-bff where a screen is involved, with the 2 s client budget and no service-to-service chain | ADR-020; DP-11; DP-19 |
| BR18 | No personal data in events, logs, workflow history or fixtures: the run carries account keys, person keys, case numbers, rule IDs, package versions and business dates only | Guardrail of RWB-E1-018; Arch v5 slide 42 notes |

### 9. State transitions

The legacy case states of RWB-E1-018:

| From | Event | Condition | To |
|---|---|---|---|
| None | AceDataReady (EV-26), package ENTRY returns ENTER | `days_past_due` at or above 90 in `v_ace_account` for the completed ALS business date, package EXCLUSION returns no match, no open case for the borrower and product group | New |
| New | Allocation rule matched | Handled by RWB-E1-020 | Assigned |

The states the run observes across the services:

| Item | States |
|---|---|
| Batch gate | Waiting (the batch is not complete and MSG-P1-001 is shown), Ready (the readiness signal is received and the data product is fresh), Held (no EXCLUSION version is in force and MSG-P3-027 is shown) |
| DailyCaseRun | Not started, started by AceDataReady, waiting at the gate, completed with the run counts, held for the whole business date |
| Case | NEW at creation with no stage code; Assigned belongs to RWB-E1-020 and is out of scope |
| Rule package version | LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED |
| Suite run | Not started, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the clock and gate control, the rollback step and the evidence report |
| Service owner of rwb-source-data | Owns the readiness call, the freshness read, the AceDataReady event and the reconciliation that lists a missing key |
| Service owner of rwb-case | Owns case creation, the DailyCaseRun workflow, the case read operations and the publication of `rwb.case.CaseCreated.v1` |
| Service owner of rwb-access | Owns the Case record right and its refusal on the case reads |
| Service owner of rwb-document | Owns the case document links that the run reads back after a creation |
| Service owner of rwb-decision | Owns the version list, the rollback, the central ledger and the RulePackageInForce event |
| Data steward | Receives the missing-key list of REC-05 and decides the data correction |
| Platform administrator | Receives the incident when the yearly number range is used up and when the gate is held for a whole date |
| Every case role holding Case record R | Reads the case and its accounts inside its scope; no write in this story |
| No role | Reads a service schema directly, or takes production data into the run |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Read through the P3 contract; written by rwb-case |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Read through the P3 contract; written by rwb-case |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Read through the P3 contract; written by rwb-case |
| DF-CAS-056 to DF-CAS-061 | case_entry_exclusion | all fields, including rule_id and rule_version | Read through the P3 contract; asserted for the sibling criteria |
| DF-ACE-001 | v_ace_account | account_key | Synthetic value only, seeded through the P1 data set |
| DF-ACE-002 | v_ace_account | account_code | Synthetic value only, seeded through the P1 data set |
| DF-ACE-010 | v_ace_account | product_category | Synthetic value only, seeded through the P1 data set |
| DF-ACE-012 | v_ace_account | branch_code | Synthetic value only, seeded through the P1 data set |
| DF-ACE-018 | v_ace_account | days_past_due | Synthetic value only, seeded through the P1 data set |
| DF-ACE-020 | v_ace_account | total_balance | Synthetic value only, seeded through the P1 data set |
| DF-ACE-031 | v_ace_account | tdr_flag | Synthetic value only, seeded through the P1 data set |
| DF-ACE-036 | v_ace_account | data_as_of | Synthetic value only, seeded through the P1 data set |
| DF-ACE-056 | v_ace_customer | person_key | Synthetic value only, seeded through the P1 data set |
| DF-ACE-061 | v_ace_customer | deceased_flag | Synthetic value only, seeded through the P1 data set |
| DF-ACE-084 | v_ace_ca_relation | person_key | Synthetic value only, seeded through the P1 data set |
| DF-ACE-085 | v_ace_ca_relation | account_key | Synthetic value only, seeded through the P1 data set |
| DF-ACE-086 | v_ace_ca_relation | relation_type | Synthetic value only, seeded through the P1 data set |
| DF-ACE-178 | v_ace_batch_status | source_system | Synthetic batch row, seeded through the P1 data set |
| DF-ACE-179 | v_ace_batch_status | business_date | Synthetic batch row, seeded through the P1 data set |
| DF-ACE-182 | v_ace_batch_status | status | Synthetic batch row, seeded through the P1 data set |
| DF-ACE-186 | v_ace_batch_status | is_complete | Synthetic batch row, seeded through the P1 data set |
| DF-EXT-001 | party_ext | person_key | Read through the P1 contract; seeded synthetically |
| DF-EXT-003 | party_ext | deceased_override | Read through the P1 contract; seeded synthetically |
| DF-EXT-004 | party_ext | bankruptcy | Read through the P1 contract; seeded synthetically |
| DF-EXT-005 | party_ext | fraud_flag | Read through the P1 contract; seeded synthetically |
| DF-EXT-027 | account_ext | account_key | Read through the P1 contract; seeded synthetically |
| DF-EXT-028 | account_ext | dispute_open | Read through the P1 contract; seeded synthetically |
| DF-REF-002 | rule_row | rule_id | Read through the P7 package contract |
| DF-REF-003 | rule_row | rule_version (the package version label) | Read through the P7 package contract |
| DF-REF-007 | rule_row | condition_expr | Not read by the suite |
| DF-REF-052 | rule_row | rule_table | Not read by the suite |
| DF-REF-296 to DF-REF-298 | rule_row | package_version_id, drools_rule_name, outputs | Read through the P7 package contract |
| DF-REF-028 | lov_value | lov_code | Read through the P3 reference-data contract |
| DF-REF-029 | lov_value | value_code | Read through the P3 reference-data contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 contract; written by rwb-decision |

Field IDs are those of RWB-E1-018 and are copied unchanged. The suite owns no field and no table: every row of this table is seeded synthetically by the harness RWB-ITG-W1J01-ITG or read through an owner's contract, and no production value is used.

The exact fixture composition - the row count of the synthetic ACE batch rows, the exact synthetic case set and the keys of the removed view row - is Not specified in the source documents (GAP-0343; ASM-0437). The fixture is the W1J01 data set, it is synthetic, and its keys are the ones the criteria name.

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are not used, and no `rwb_integration` table is written.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Readiness trigger for the business date, as the Airflow stub calls it; starts the gate | 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | ALS gate: the freshness stamp of the data product for the business date | 2 s |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Case-number search for the creation and for the unchanged closed case | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case record: status, stage code, entry date, primary person key | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | Case accounts: `account_key`, `is_primary`, `linked_from`, `linked_to` | 2 s |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Decision record of the creation: decision code, final call, rule ID, package version | 2 s |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | Package in force: the EXCLUSION versions and the one in force | 2 s |
| POST | `/api/recovery/decision/v1/admin/rule-package-versions/{versionId}/rollback` | P7 rwb-decision | AC15: the one-call rollback that removes the EXCLUSION version from force, and the promote back | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service, and the readiness and freshness operations are the only P1 writes it triggers.

#### 12.3 Events published

None. The suite publishes no business event; it observes the events of the owning services, listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.source-data.AceDataReady.v1` | `rwb.source-data.events.v1` | P1 rwb-source-data | The readiness event for the business date starts DailyCaseRun on queue `rwb-case`; CloudEvents envelope, key caseId or business date, no personal data field |
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | Exactly one event per creation, case number RW-2026-000123, product group, accounts and business date; the assertion of AC1 on the platform |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | The decision of the creation reaches the central ledger; decision code D6, final call CASE_CREATED, the ENTRY rule ID and package version |
| `rwb.decision.RulePackageInForce.v1` | `rwb.decision.events.v1` | P7 rwb-decision | A package promoted by the 00:01 schedule is announced; used to place the rollback and the promote back of AC15 |

The envelope is CloudEvents 1.0, and a consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published schema; the event and ledger assertions replace the in-process `caseCreated` and the local decision log of the legacy criterion (GAP-0343; ASM-0437).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| DailyCaseRun | Workflow | `rwb-case` | Started by AceDataReady for the business date; gate check, creation, the run counts; output read as the result of the run (JOB-02) |
| CaseWorkflow | Workflow | `rwb-case` | One per case from entry to closure, started with the case ID; the suite asserts that the creation started it |
| EvaluateRules | Activity | `rwb-case` | Input package code, facts and business date; output package code, package version, rule ID and outputs (DP-04) |
| RecordAndApply | Activity | `rwb-case` | Writes the decision record, the state and the outbox rows in one transaction, and fails as one unit |
| AceIngestCheck | Workflow | `rwb-source-data` | Readiness and freshness check for the business date, before the gate opens |
| reconciliation | Workflow | `rwb-source-data` | JOB-04 reconciliation, event-started; the source of the missing-key list that AC13 reads |

Arch v5 slide 15 draws AceIngestCheck and the reconciliation as workflows of rwb-source-data, and the ownership map replaces JOB-04 with an event-started workflow there. The suite observes their runs through the P1 job API and the owner's contract; it starts no workflow of its own (GAP-0343; ASM-0437).

#### 12.6 Schedules

| Schedule or start | Cadence | Registration | Legacy reference |
|---|---|---|---|
| JOB-02 case creation | Event-started: AceDataReady for the business date starts DailyCaseRun | Registered by the rwb-case release | JOB-02 Case creation |
| JOB-04 reconciliation | Event-started workflow on queue `rwb-source-data`, started by AceDataReady | Registered by the rwb-source-data release | JOB-04 Reconciliation |
| JOB-20 rule promote | Temporal Schedule at 00:01, overlap policy SKIP, catch-up window; publishes RulePackageInForce | Registered by the rwb-decision release | JOB-20 Rule promote |

The suite triggers the 00:01 schedule once through the Temporal client with the same input the cadence uses, and it starts no schedule of its own.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). Every fact it asserts is read through a contract of section 12.2, 12.4 or 12.5.

#### 12.8 Contract fakes

None for a service contract. The only stubs are external to the nineteen services:

| Stub | Purpose |
|---|---|
| ACE batch and synthetic account, customer and relation fixture (RWB-ITG-W1J01-ITG) | Stands in for the ACE ingestion that the bank's Airflow owns, outside the nineteen services |
| Airflow readiness stub | Calls the P1 readiness operation for the business date, in the way the Airflow DAG will |
| Mock Entra sign-in | Gives the run its synthetic test identities, as the platform demo sign-in does |

No published service contract is faked, and a run that needs a fake for P1, P3, P4, P5 or P7 fails the preflight.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 8 | The readiness trigger, the freshness read, three case reads, the decision-log read, the version list and the rollback; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 4 event types | `rwb.source-data.AceDataReady.v1`, `rwb.case.CaseCreated.v1`, `rwb.decision-record.DecisionRecorded.v1`, `rwb.decision.RulePackageInForce.v1`; CloudEvents 1.0, key caseId |
| Temporal | None | 2 workflows in rwb-case, 2 in rwb-source-data, 4 activities | DailyCaseRun and CaseWorkflow in rwb-case; EvaluateRules and RecordAndApply activities in rwb-case; AceIngestCheck and reconciliation workflows in rwb-source-data; the JOB-02, JOB-04 and JOB-20 starts of 12.6 are observed |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a fixture builder for the ACE batch and the synthetic case set, a readiness and clock control for the gate, a set of contract probes, a rule-rollback step and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published contracts, run order, report and exit code |
| BatchFixtureDriver | Test harness | Seeds the synthetic ACE batch rows and the synthetic account, customer and relation rows of the W1J01 set, and calls the P1 readiness operation for the business date |
| GateControl | Test harness | Places the batch row at COMPLETED or RUNNING for a date, moves the business date, and proves that a held date creates nothing |
| EventProbe | Test harness | Consumes the four events of 12.4 and asserts the envelope, the key, the event count per creation and the absence of a personal data field |
| CaseProbe | Test harness | Calls the case-number search and the two case reads and asserts status NEW, no stage code, entry date, primary person key and the account links |
| DecisionProbe | Test harness | Reads the P7 decision log and asserts the decision code, the final call, the ENTRY rule ID and the package version of the creation |
| PackageRollbackStep | Test harness | Reads the EXCLUSION version list, rolls the version back, asserts the held date and MSG-P3-027, then promotes "EXCL-2026.11" back |
| MissingKeyStep | Test harness | Takes the synthetic row of A-5013 and P-0105 out of the source set, runs the intake and reads the reconciliation output |
| ReportWriter | Test harness | One row per test case, with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table and no schema object.

**Configuration and reference data**

- The SIT endpoints of P1, P3, P4, P5 and P7, the topic names, the queue names, the namespace `rwb-recovery` and the schema-registry address, all as configuration.
- The synthetic account, customer, person and case keys of the W1J01 set, the business dates 2026-12-01 and 2026-12-02, and the last case number RW-2026-000122.
- The threshold, the package codes ENTRY and EXCLUSION and the versions "ENTRY-2026.11" and "EXCL-2026.11", read through the P3 and P7 contracts and never written in the suite code.
- The list values, including LOV-CASE-STATUS and LOV-EXPOSURE, read through the P3 reference-data contract (DP-07).
- The 2 s client budget, the poll interval and the cut-off time of the run.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies of the table stay with the service, platform and operations stories that own them; this story carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). The I list names the eight services whose behaviour the run exercises.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| ALS batch rows | The synthetic batch rows for 2026-12-01 at COMPLETED and for 2026-12-02 at RUNNING, seeded through the W1J01 set | AC1, AC9 |
| Synthetic case set | The accounts, customers and relations of the run, including A-5001 with P-0101 at 90 days past due and the case links of RW-2026-000126 | AC1, AC13 |
| Number state | The last case number issued in 2026 set to RW-2026-000122 | AC1 |
| Package state | The EXCLUSION version in force, and the earlier version that the rollback returns to | AC15 |
| Missing-key fixture | The source row of A-5013 and P-0105 removed for the date, with the case link left in place | AC13 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the topics, the queue and the schedule, with the contract preflight that fails on any drift.
2. Build BatchFixtureDriver and the W1J01 fixtures for the batch rows and the synthetic case set; assert that the readiness operation opens the gate and that no case exists before it.
3. Build EventProbe for the four events, with the envelope, the key and the no-personal-data assertions, and the inbox-dedupe case of a repeated AceDataReady.
4. Build CaseProbe for the case-number search and the two case reads; assert the case, the account link and the party link of AC1 through the P3 contract.
5. Build DecisionProbe for the P7 decision log and the DecisionRecorded event; assert the decision code, the final call, the rule ID and the package version of the creation.
6. Build GateControl and the AC9 path: a RUNNING batch, the cut-off check, MSG-P1-001, then the readiness signal and the cases of the next date.
7. Build MissingKeyStep for AC13 and PackageRollbackStep for AC15, including the promote back and the assertion that creation resumes.
8. Build ReportWriter, the cleanup of the synthetic set and the evidence report; run the whole suite twice to prove that a repeated run adds no case and no link.

**Done when.** The sixteen test cases of section 16 pass on the real services in SIT, the four criteria this story owns (AC1, AC9, AC13, AC15) are signed off against the contracts, exactly one `rwb.case.CaseCreated.v1` and one decision record exist per creation, no service table was read, the synthetic set is cleaned up, and the evidence report names every criterion with its observable.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | JOB-02 waiting for a COMPLETED ALS batch | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P3-027 | No ENTRY or EXCLUSION version is in force on the business date | The rule version was refused at the {check} check: {detail}. |
| MSG-P7-003 | Decision log write failed for an account | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P3-025 | Yearly case number range used up | Case numbers for {year} are used up. New cases are on hold until the range is extended. |
| MSG-P4-002 | Read without Case record R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Case outside the reader's scope | This case is not in your scope. |

The six texts are copied unchanged from RWB-E1-018 and this story adds no message ID. For MSG-P3-027 the {check} value is "package in force" and the {detail} names the package code only.

### 15. Screens and states

SCR-02 Case list (Loading; empty; list; filtered) shows each new case with its case number, product, status NEW and entry date, read through the gateway-bff composite route (DP-19). SCR-03 Case record (Loading; read only) shows the case and its linked accounts by `account_key`. The run asserts the same facts through the case read operations and checks that the two screens show the case number, the product, the status NEW, the entry date and the linked accounts. The full read-only case record view is RWB-E1-023 and is out of scope.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-018-02-ITG | AC2, BR3 | Integration | `v_ace_account` A-5002 with `tdr_flag` true; package EXCLUSION "EXCL-2026.11"; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-01-ITG | AC1, BR1, BR2, BR4, BR5, BR11, BR12, BR13 | Integration | `v_ace_account` A-5001 at 90 days past due, borrower P-0101, last number RW-2026-000122; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-03-ITG | AC3, BR2, BR12 | Integration | Borrower P-0102 with two HP accounts of 300,000.00 and 112,350.00; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-04-ITG | AC4, BR4 | Integration | Closed case RW-2026-000123; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-05-ITG | AC5, BR6 | Integration | New status value WAITING_COURT in LOV-CASE-STATUS; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-06-ITG | AC6, BR3 | Integration | A-5005 with `dispute_open` true in account_ext; EXCLUSION rule "EXCL-006"; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-07-ITG | AC7, BR1 | Integration | Accounts at 89 and 90 days past due in `v_ace_account`; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-08-ITG | AC8 | Integration | JOB-02 run twice for 2026-12-01; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-09-ITG | AC9, BR7 | Integration | ALS batch for 2026-12-02 at status RUNNING; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-10-ITG | AC10, BR8 | Integration | Decision log store unavailable for one account; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-11-ITG | AC11, BR4 | Integration | Sequence at 999999; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-12-ITG | AC12, BR2 | Integration | Borrower P-0103 with a mortgage and an HP account; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-13-ITG | AC14, BR11 | Integration | RW-REFADM reads GET /cases/{caseId} and is refused with MSG-P4-002; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-14-ITG | Principle 5 | NFR | Decision log write forced to fail for the whole run; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-15-ITG | AC13, BR11 | Integration | Case links A-5013 and P-0105 with no view row for 2026-12-01; end-to-end: real services on the wave 1 contracts |
| TC-E1-018-16-ITG | AC15, BR13 | Integration | No EXCLUSION version in force on 2026-12-01; end-to-end: real services on the wave 1 contracts |

TC-E1-018-01-ITG, TC-E1-018-09-ITG, TC-E1-018-15-ITG and TC-E1-018-16-ITG are the copies this story signs off, one for AC1, AC9, AC13 and AC15. The other twelve are regression evidence for the component copy RWB-P3-E1018-APP, which owns their criteria, and they are run here on the real services so that a change in one service cannot pass unnoticed. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, and the legacy Resilience level becomes NFR.

### 17. Guardrails

- Synthetic data only: the harness RWB-ITG-W1J01-ITG loads every account, customer, person, case number and batch row, and no production data is read, copied or connected to.
- No personal data in events, logs, workflow history, fixtures or the report: account keys, person keys, case numbers, rule IDs, package versions and business dates only.
- No cross-service table read: every fact is read through a contract, the source views stay behind rwb-source-data, and the suite ships with no client for a service schema (DP-01, DP-05).
- No business value in the test code: the threshold 90, the exclusion reasons, the exposure bands and the status list are the parameter, the packages and the lists in force, read through the P3 and P7 contracts.
- CloudEvents 1.0 with IDs and facts only on every asserted event, one event per creation, and the consumer inbox as the only dedupe.
- One hop and a 2 s budget on every REST call, with no service called through another service (ADR-020).
- No production access and no production namespace: the run is pinned to SIT and refuses to start against any other environment.
- Clean-up in the same run: the synthetic set, the business dates, the rolled-back package version and the started workflows are removed or promoted back, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-001 | One case for every non-excluded account at 90 days past due | `POST /api/recovery/source-data/v1/business-days/{date}/ready`, `GET /api/recovery/source-data/v1/data-products/freshness`, AceDataReady, the three case reads | TC-E1-018-01-ITG, TC-E1-018-07-ITG, TC-E1-018-09-ITG |
| REQ-CWC-002 | Case ID RW-YYYY-NNNNNN, never reused | `GET /api/recovery/case/v1/cases` with the case-number search, `GET /api/recovery/case/v1/cases/{caseId}` | TC-E1-018-01-ITG, TC-E1-018-04-ITG, TC-E1-018-11-ITG |
| REQ-CWC-003 | One case per customer and product | `GET /api/recovery/case/v1/cases/{caseId}/accounts`, `rwb.case.CaseCreated.v1` | TC-E1-018-03-ITG, TC-E1-018-08-ITG, TC-E1-018-12-ITG |
| REQ-CWC-004 | Exclusion rules as data | `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`, the rollback, MSG-P3-027 | TC-E1-018-02-ITG, TC-E1-018-06-ITG, TC-E1-018-16-ITG |
| REQ-CWC-005 | State model with one state at a time | `GET /api/recovery/case/v1/cases/{caseId}` status and stage code | TC-E1-018-05-ITG |
| REQ-CWC-016 | Every workflow event logged with rule ID and version | `rwb.decision-record.DecisionRecorded.v1`, `GET /api/recovery/decision/v1/decision-log` | TC-E1-018-10-ITG, TC-E1-018-14-ITG |
| REQ-CHO-004 | One agreed hand-over point in days past due for every rule and report | The readiness and freshness reads, the entry threshold of the P3 parameter contract, `rwb.case.CaseCreated.v1` | TC-E1-018-01-ITG |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The four events of 12.4, the consumer inbox dedupe, schema-registry versioning | TC-E1-018-01-ITG, TC-E1-018-08-ITG, TC-E1-018-15-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The eight REST operations of 12.2 and the preflight contract test | TC-E1-018-09-ITG, TC-E1-018-13-ITG |
| ADR-021 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; it asserts through contracts only | Every test case, at the preflight |
| DP-03 | Decision record library and the shared topic | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, the P7 decision-log read | TC-E1-018-10-ITG, TC-E1-018-14-ITG |
| DP-04 | Embedded Drools kit and rule packages from rwb-decision | The ENTRY and EXCLUSION versions, the version list, the rollback | TC-E1-018-02-ITG, TC-E1-018-16-ITG |
| DP-06 | Parameters contract of rwb-case | The entry threshold read through the P3 parameter contract, not a value in code | TC-E1-018-01-ITG, TC-E1-018-07-ITG |
| DP-07 | Reference-data contract of rwb-case | LOV-CASE-STATUS and LOV-EXPOSURE read through the P3 contract | TC-E1-018-05-ITG |
| DP-14 | Topic naming of the owner | `rwb.case.events.v1`, `rwb.source-data.events.v1`, `rwb.decision.events.v1` | TC-E1-018-01-ITG, TC-E1-018-09-ITG |
| RWB-E1-018 (legacy story) | Case ID issuance and case record v1: AC1, AC9, AC13, AC15 | The eight REST operations, the four events, the two workflows and the four activities of section 12 | The four signed-off copies of section 16 |
| RWB-P3-E1018-APP (component copy) | Case creation and case record in rwb-case, owning AC2 to AC8, AC10 to AC12 and AC14 | The case create path, the case read operations, the number issuer and the exclusion record | The twelve regression copies of section 16 |

### 19. Out of scope

- The eight application builds this run depends on: RWB-P1-E1001-APP, RWB-P1-E1016-APP, RWB-P1-E1069-APP, RWB-P3-E1018-APP, RWB-P5-E1018-APP, RWB-P1-E1018-APP, RWB-P4-E1018-APP and RWB-P7-E1018-APP.
- The contract, database, operations and infrastructure stories of the legacy key.
- The criteria this story does not own: AC2, AC3, AC4, AC5, AC6, AC7, AC8, AC10, AC11, AC12 and AC14, which belong to RWB-P3-E1018-APP.
- The allocation and transfer engine (RWB-E1-020 and RWB-E1-021).
- The build of the harness RWB-ITG-W1J01-ITG itself.
- The non-functional epic RWB-ITG-NFR.
- The data lake: it is removed from the target architecture (DP-17) and no copy of a case or a decision goes to it.
