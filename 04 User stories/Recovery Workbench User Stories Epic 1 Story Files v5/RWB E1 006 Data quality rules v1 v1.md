# RWB-E1-006 Data quality rules v1

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-E1-006 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | FEAT-RDF-10 Run data quality rules on every load |
| Requirement IDs | REQ-RDF-008 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-002, RWB-E1-003, RWB-E1-043 |
| Status | Ready for build |

## 1. Story

As a **data steward and data product owner (RW-DATASTEW)**, I want **ten data quality rules (missing owner, duplicate account, days past due mismatch, stale balance, missing collateral link and five more) run on every load, with a reason code on every failed row**, so that **the case list can be trusted**.

## 2. Business rationale

Today a wrong owner, an account on two cases or a balance that does not add up is found only when a case owner works the case. This story runs ten row-level rules, held as versioned data rows, after every load and after the daily case list build, and writes each failed row with its rule code to the exception list that the data steward and Power BI read. It meets REQ-RDF-008 and serves the data quality measures completeness 99.9 percent, validity 99.5 percent and uniqueness 100 percent.

## 3. Preconditions

- RWB-E1-003 is done: loads write load_run and dq_exception and raise an internal completion call for each data product.
- RWB-E1-002 is done: case_list_row is built by the case list step of JOB-04.
- RWB-E1-043 is done: the reference data service loads a table through the handler the owning module provides.
- The rule version "DQR-2026.11" with the ten rules in section 13 is loaded and approved by the data steward.
- Parameter `case.entry.dpd` 90 (DL16) is loaded.
- The rules run as service identity SY-DATALOAD.

## 4. Flow

1. System: a load completes for a data product (for example INT-01 for DP01), or the case list step of JOB-04 completes for DP03.
2. System: reads the dq_rule rows in force for that data product on the business date.
3. System: builds the SQL for each rule from its rule type template and its parameters, using only table and column names that sys_fields holds for P1-owned tables.
4. System: runs each rule and collects the failing records.
5. System: writes one dq_exception row per failing record with the rule code as check and reason code, the rule version, the record key and the business date.
6. System: sets CLEARED on any OPEN exception of the same rule and record that no longer fails.
7. System: writes the count per rule to the load_run check results.
8. System: the JOB-04 publish step writes the open and new exceptions for the business date to the data lake extract for Power BI.
9. Data steward: reads the exceptions through GET /admin/data-quality/exceptions or the Power BI data quality report.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A rule version names a field not in the data dictionary | The rule load is refused in full | MSG-P1-005 | AC4 |
| X2 | A rule row names a rule type or a table outside the allowed set | The rule load is refused in full | MSG-P1-007 | AC5 |
| X3 | One rule fails at run time (for example a statement timeout) | That rule is ERROR on the load_run; the other rules run; the data steward is alerted | MSG-P1-015 | AC6 |
| X4 | The rules run again for the same load | No second exception row for the same rule, record and load | None | AC7 |
| X5 | A rule's valid to date has passed or its valid from date is in the future | The rule does not run | None | AC8 |
| X6 | A record that failed before now passes | Its open exception is set CLEARED with the date | None | AC9 |
| X7 | A role without Platform administration R lists exceptions | 403 | MSG-P4-002 | TC-E1-006-10 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs on the outputs of the load stories and the case list; no case is changed |
| Negotiable | The rules, their parameters and their versions are data; the story fixes the rule types and the run points |
| Valuable | Every failed row is visible with a reason before a case owner meets it |
| Estimable | Seven rule type templates, one runner, one handler, one read endpoint |
| Small | Can be finished in two weeks or less with its tests |
| Testable | Each criterion below is one automated test on synthetic data |

## 7. Acceptance criteria

```gherkin
Feature: Data quality rules v1

  Background:
    Given the rule version "DQR-2026.11" with rules DQ01 to DQ10 is in force from 2026-11-20
    Given the business date is 2026-11-30

  Scenario: AC1 Rules run daily
    Given the case list for 2026-11-30 holds three accounts "ACC0000301", "ACC0000302" and "ACC0000303", each linked to two open cases
    When the case list step of JOB-04 completes and the rules for DP03 run
    Then the system writes three dq_exception rows with check code and reason code "DQ02", rule version "DQR-2026.11" and raised_on 2026-11-30
    Then GET /admin/data-quality/exceptions with product "DP03" and from 2026-11-30 returns the three rows
    Then the load_run check results show "DQ02" = 3

  Scenario: AC2 Report in Power BI
    Given the rules for 2026-11-30 wrote 3 DQ02, 14 DQ05 and 2 DQ06 exceptions
    When the JOB-04 publish step writes the data quality extract for 2026-11-30
    Then the extract holds 19 rows with rule code, rule name, data product, business date and record key
    Then the Power BI data quality report shows failures by rule, by data product and by day for 2026-11-30

  Scenario: AC3 Rule as data
    Given the reference data administrator loads rule version "DQR-2026.12" adding rule DQ11 of type RANGE on loan_account.interest_rate with maximum 30.0000, valid from 2026-12-01
    Given the data steward approves the version
    When the INT-01 load for 2026-12-01 completes
    Then DQ11 runs with no deployment and writes 2 exceptions for the 2 accounts with interest rate 32.5000
    Then DQ01 to DQ10 run unchanged

  Scenario: AC4 Rule naming an unknown field
    Given a rule version in which DQ12 names loan_account.balance_total
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-005 "loan_account.balance_total is not in the data dictionary."
    Then the rule version in force stays "DQR-2026.11"

  Scenario: AC5 Rule on a table outside P1
    Given a rule version in which DQ12 is of type NOT_NULL on recovery_case.owner_user_id
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P1-007 "Row 12: target_entity must be one of loan_account, account_payment, party, contact_point, collateral, account_collateral, collections_history, case_list_row."

  Scenario: AC6 One rule fails at run time
    Given the statement for DQ05 times out after the 60 second limit
    When the rules for DP03 run
    Then the system shows DQ05 as ERROR on the load_run and the other rules for DP03 write their exceptions
    Then the data steward group receives MSG-P1-015 "Rule DQ05 did not run for 2026-11-30: statement timeout. The other rules ran."

  Scenario: AC7 Rules run twice for one load
    Given the rules for the INT-01 load of 2026-11-30 have written 2 DQ06 exceptions
    When the rules run again for the same load
    Then dq_exception still holds 2 DQ06 rows for that load

  Scenario: AC8 Rule outside its valid dates
    Given DQ07 has valid to 2026-11-30
    When the INT-01 load for 2026-11-30 completes
    Then DQ07 does not run and the load_run check results do not list DQ07

  Scenario: AC9 Exception cleared when the record passes
    Given an OPEN DQ01 exception for case account "ACC0000777" raised on 2026-11-27
    Given the case of "ACC0000777" now has an owner
    When the rules for DP03 run for 2026-11-30
    Then the system sets the exception CLEARED with cleared_on 2026-11-30
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Data quality rules run on every load and every failed row carries a reason code | REQ-RDF-008; FEAT-RDF-10 |
| BR2 | Each rule is a versioned data row with valid from, valid to, approver and test case; a change needs no code release | Principle 1; DT02; CTL-08 |
| BR3 | A rule version takes effect on its valid from date | R-UNI-38 |
| BR4 | A rule version with an exception is refused in full | Reference data change process, step 3 |
| BR5 | Rules read only P1-owned tables and columns that the data dictionary holds | ADR-002; sys_fields |
| BR6 | Row rule codes DQ01 to DQ10 are separate from the load checks DQ-001 to DQ-098, which refuse or hold a whole load | Data quality and reconciliation rules, load checks |
| BR7 | DQ03 uses the entry threshold of 90 days past due | Parameter case.entry.dpd (DL16) |
| BR8 | A duplicate case found by DQ02 is merged by P3 under its own rule | R-UNI-17 |

## 9. State transitions

None. This story does not change a case status. It changes the status of dq_exception rows (OPEN to CLEARED) and adds rule results to the load_run check results.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DATALOAD, data load from COLLINS | Runs the rules; writes dq_exception and the load_run results |
| RW-REFADM, reference data administrator | Loads a rule version (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Approves a rule version as its owner; reads exceptions (Platform administration R) |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read exceptions (Platform administration R) |
| RW-BIANAL, reporting and BI analyst | Builds the Power BI data quality report (Reporting CRUD) |

Separation of duty: the reference data administrator who loads a version cannot approve it.

## 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACC-002 | loan_account | account_no | Read |
| DF-ACC-009 | loan_account | principal_outstanding | Read (DQ06, DQ07) |
| DF-ACC-010 | loan_account | interest_outstanding | Read (DQ06) |
| DF-ACC-011 | loan_account | fees_outstanding | Read (DQ06) |
| DF-ACC-012 | loan_account | total_balance | Read (DQ06) |
| DF-ACC-008 | loan_account | interest_rate | Read (DQ11 in AC3) |
| DF-ACC-014 | loan_account | days_past_due | Read (DQ08) |
| DF-ACC-016 | loan_account | classification | Read (DQ08) |
| DF-ACC-017 | loan_account | last_payment_date | Read (DQ10) |
| DF-ACC-021 | loan_account | data_as_of | Read (DQ04) |
| DF-ACC-023 | account_payment | account_id | Read (DQ10) |
| DF-ACC-025 | account_payment | payment_date | Read (DQ10) |
| DF-PTY-001 | party | id | Read (DQ09) |
| DF-PTY-014 | contact_point | party_id | Read (DQ09) |
| DF-COL-015 | account_collateral | account_id | Read (DQ05) |
| DF-RPT-003 | case_list_row | case_id | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-RPT-005 | case_list_row | account_id | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-RPT-006 | case_list_row | account_no | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-RPT-007 | case_list_row | product_group | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-RPT-009 | case_list_row | status | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-RPT-010 | case_list_row | owner_user_id | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-RPT-015 | case_list_row | days_past_due | Read (DQ01, DQ02, DQ03, DQ05) |
| DF-OPS-052 | dq_rule | id | Write (through the handler); read |
| DF-OPS-053 | dq_rule | rule_code | Write (through the handler); read |
| DF-OPS-054 | dq_rule | rule_version | Write (through the handler); read |
| DF-OPS-055 | dq_rule | rule_name | Write (through the handler); read |
| DF-OPS-056 | dq_rule | product_code | Write (through the handler); read |
| DF-OPS-057 | dq_rule | target_entity | Write (through the handler); read |
| DF-OPS-058 | dq_rule | rule_type | Write (through the handler); read |
| DF-OPS-059 | dq_rule | rule_params | Write (through the handler); read |
| DF-OPS-060 | dq_rule | valid_from | Write (through the handler); read |
| DF-OPS-061 | dq_rule | valid_to | Write (through the handler); read |
| DF-OPS-062 | dq_rule | approved_by | Write (through the handler); read |
| DF-OPS-063 | dq_rule | test_case_id | Write (through the handler); read |
| DF-OPS-041 | dq_exception | id | Write |
| DF-OPS-042 | dq_exception | load_run_id | Write |
| DF-OPS-043 | dq_exception | product_code | Write |
| DF-OPS-044 | dq_exception | check_code | Write |
| DF-OPS-050 | dq_exception | rule_version | Write |
| DF-OPS-045 | dq_exception | record_key | Write |
| DF-OPS-046 | dq_exception | reason_code | Write |
| DF-OPS-048 | dq_exception | raised_on | Write |
| DF-OPS-049 | dq_exception | status | Write |
| DF-OPS-051 | dq_exception | cleared_on | Write |
| DF-OPS-034 | load_run | check_results | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

**Rule run**

| Item | Value |
|---|---|
| Trigger | The completion of each load step in JOB-01 and JOB-09 (internal call `DataQualityRuleRunner.runFor(productCode, loadRunId)`); the case list step of JOB-04 for DP03 |
| Job name | JOB-01 COLLINS load check and intake; JOB-09 File loads; JOB-04 Daily reconciliation |
| Input | dq_rule rows in force; the P1 tables named by the rules |
| Output | dq_exception; load_run check results; the data quality extract in the JOB-04 publish step |
| Events published | None |
| Idempotency key | load_run_id, check_code and record_key (unique) |
| Restart | Rules run again in full on rerun of the load; existing rows are not duplicated |

**GET /admin/data-quality/exceptions** (API-P1-003)

| Item | Value |
|---|---|
| Request | Query `product` (data product code, for example DP03), `from`, `to` (raised_on dates) |
| Response 200 | `DataQualityException[]`: id, product, check (rule or check code), record (record key), raisedOn |
| 401, 403, 503 | MSG-P4-001; MSG-P4-002; database unavailable |
| Authorization | Platform administration R, scope All |
| Idempotency | Read only |

**Rule load.** `POST /admin/reference-loads` (P4, Reference data C) with `table = dq_rule`; P1 implements `ReferenceTableHandler` (signature in RWB-E1-001) as `DqRuleHandler`. Refusals return 422 with MSG-P1-005 or MSG-P1-007.

## 13. Solution plan

**Package.** Folder `recovery/dataengine/quality`, Java package `recovery.dataengine.quality`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DqRule | Entity | Maps dq_rule |
| DqRuleRepository | Repository | Reads the rules in force by product and date |
| DqRuleHandler | Published interface implementation | ReferenceTableHandler for `dq_rule`: validates entity, field, rule type and parameters against sys_fields and the allowed set |
| RuleTypeTemplates | Service | One SQL template per rule type: NOT_NULL, UNIQUE_ACROSS, RANGE, SUM_EQUALS, EXISTS_LINK, MAX_AGE_DAYS, FIELD_BEFORE |
| DataQualityRuleRunner | Service | Runs the rules of one product for one load with a 60 second limit per rule; writes and clears exceptions |
| DqExceptionRepository | Repository (from RWB-E1-003) | Insert with ON CONFLICT DO NOTHING; clear by rule and record |
| DataQualityExtractWriter | Service | Writes the day's exceptions to the lake extract in the JOB-04 publish step |
| RecoveryDataEngineController | Controller | GET /admin/data-quality/exceptions |

**Database.** Migration `V1_006__dq_rule.sql` creates dq_rule (rule_code varchar(8), rule_version varchar(20), rule_name varchar(120), product_code varchar(4), target_entity varchar(60), rule_type varchar(15), rule_params jsonb, valid_from date, valid_to date, approved_by uuid, test_case_id varchar(20), standard columns, unique (rule_code, rule_version)); adds rule_version varchar(20) and cleared_on date to dq_exception and `uk_dq_exception UNIQUE (load_run_id, check_code, record_key)`.

**Configuration and reference data.** Rule version "DQR-2026.11", loaded by the reference data administrator and approved by the data steward:

| Rule | Name | Product | Table | Type and parameters |
|---|---|---|---|---|
| DQ01 | Missing owner | DP03 | case_list_row | NOT_NULL owner_user_id where status is not NEW |
| DQ02 | Duplicate account | DP03 | case_list_row | UNIQUE_ACROSS account_id over case_id |
| DQ03 | Days past due mismatch | DP03 | case_list_row | RANGE days_past_due minimum case.entry.dpd |
| DQ04 | Stale balance | DP01 | loan_account | MAX_AGE_DAYS data_as_of 0 days behind the load business date, for accounts on the case list |
| DQ05 | Missing collateral link | DP03 | case_list_row | EXISTS_LINK account_collateral.account_id where product_group in MORTGAGE, HIRE_PURCHASE |
| DQ06 | Balance parts do not add up | DP01 | loan_account | SUM_EQUALS total_balance = principal_outstanding + interest_outstanding + fees_outstanding, tolerance 0.00 |
| DQ07 | Negative principal | DP01 | loan_account | RANGE principal_outstanding minimum 0.00 |
| DQ08 | Missing classification | DP01 | loan_account | NOT_NULL classification where days_past_due at or above case.entry.dpd |
| DQ09 | Party without a contact point | DP02 | party | EXISTS_LINK contact_point.party_id |
| DQ10 | Payment after the last payment date | DP01 | account_payment | FIELD_BEFORE payment_date not after loan_account.last_payment_date |

**Build steps**

1. Write migration V1_006, DqRule and DqRuleRepository; test the in-force query by date.
2. Write RuleTypeTemplates with bound parameters and identifiers taken only from sys_fields; unit test each template with a pass and a fail fixture.
3. Write DqRuleHandler with the checks for X1 and X2; connect it to the reference data service.
4. Write DataQualityRuleRunner with the per-rule limit, the ERROR result and the clear step.
5. Call the runner from the completion of each load step and from the case list step.
6. Write DataQualityExtractWriter and add it to the JOB-04 publish step.
7. Write the controller method with the capability check.

**Feature flag.** `rwb.p1.dq-rules`. Off: no rule runs; loads complete as before.

**Done when.** The tests in section 16 pass, and the ten rules of "DQR-2026.11" each have a passing and a failing test case named in test_case_id.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-005 | Rule names a field not in the dictionary | {entity}.{field} is not in the data dictionary. |
| MSG-P1-007 | Rule type or table outside the allowed set | Row {row}: {field} must be one of {values}. |
| MSG-P1-015 | A rule fails at run time | Rule {rule} did not run for {date}: {reason}. The other rules ran. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

## 15. Screens and states

No Workbench screen in this story. The data steward reads the exceptions through the endpoint and the Power BI data quality report. SCR-45 Data quality shows load check results and breaks, with the states Loading and Breaks, from E2.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-006-01 | AC1, BR1, BR8 | System | Case list with three accounts each on two open cases |
| TC-E1-006-02 | AC2 | System | 3 DQ02, 14 DQ05 and 2 DQ06 exceptions for 2026-11-30 |
| TC-E1-006-03 | AC3, BR2, BR3 | System | Rule version DQR-2026.12 with DQ11; 2 accounts at 32.5000 |
| TC-E1-006-04 | AC4, BR4, BR5 | System | Rule DQ12 on loan_account.balance_total |
| TC-E1-006-05 | AC5, BR5 | System | Rule DQ12 on recovery_case.owner_user_id |
| TC-E1-006-06 | AC6 | System | DQ05 statement forced past 60 seconds |
| TC-E1-006-07 | AC7 | System | Rules run twice on one INT-01 load |
| TC-E1-006-08 | AC8, BR3 | System | DQ07 with valid to 2026-11-30 |
| TC-E1-006-09 | AC9 | System | Open DQ01 exception for ACC0000777 |
| TC-E1-006-10 | Access | Access | RW-CASEOWN calls GET /admin/data-quality/exceptions; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: rules, thresholds and product lists are rule rows and parameters; only the seven rule type templates are code.
- No personal data in logs, tests or prompts. record_key holds account keys or record IDs, never names or contact values.
- No read of another module's tables. Rules on case data read case_list_row, which P1 builds from the P3 published interface.
- No rule text is executed as SQL: identifiers come from sys_fields and values are bound parameters.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-008 | Data quality rules on every load; every failed row has a reason code | Epic 1, 3.1; Program, 5.1 | FEAT-RDF-10 | All recovery processes | R-UNI-17; R-UNI-38; CTL-08 | TC-E1-006-01 to TC-E1-006-10 |

## 19. Out of scope

- Working a data quality break to closure with an owner and a date (FEAT-RPT-09, Epic 2).
- The Data quality screen SCR-45 (Epic 2).
- The daily reconciliation to ALS (RWB-E1-011).
- Merging duplicate cases (R-UNI-17, P3).
- Rules on tables owned by other modules, which those modules run in their own stories.

