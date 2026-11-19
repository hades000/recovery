# TB0001-1168 [RWB-E1-006] Data quality rules v1

| Field | Value |
|---|---|
| Jira | [TB0001-1168](https://scbjira.atlassian.net/browse/TB0001-1168) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | - |
| Created | 2026-11-05T12:37:09.180+0700 |
| Updated | 2026-11-17T21:49:42.491+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want ten data quality rules (missing owner, duplicate account, days past due mismatch, stale balance, missing collateral link and five more) run on every load, with a reason code on every failed row, so that the case list can be trusted.

## Acceptance criteria

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

## Comments (0)

(none)

## Other Jira fields

| Field | ID | Value |
|---|---|---|
| App Owner | customfield_10188 | - |
| App Owner (migrated 3) | customfield_11031 | - |
| Approver2 | customfield_11586 | Nuttakorn Leeviravanich |
| AR: Atlassian-TemplateO | customfield_11656 | emaile,role |
| AR: Atlassian_Template | customfield_11654 | \|\|Full Name \|\| Email \|\| Role \|\| Company \|\| \|{Full Name}\|{Email}\|{Role}\|{Company}\| \|\|\|\| |
| BI Status | customfield_10169 | To be Confirmed |
| Build % | customfield_12531 | 0% |
| Bulk Backlog Detail Uploaded | customfield_11628 | No |
| CCB Status | customfield_10228 | New |
| Created Date | customfield_10249 | 2026-11-05 |
| Customer Impact | customfield_10246 | No |
| CX Status | customfield_10217 | To be Confirmed |
| Defect Re-Opened? | customfield_10619 | No |
| Defect Re-Opened? (Checkbox) | customfield_10174 | No |
| Demand type | customfield_10244 | Project |
| Demand types(Migrated on 29 Mar 2024) | customfield_11926 | Incident |
| Deploy Status | customfield_10170 | Initial |
| DGO Approval | customfield_10113 | Pending |
| DPO Approval | customfield_10122 | Pending |
| Epic Type | customfield_10275 | Project |
| Epic Type OLD | customfield_10052 | Project |
| Execution Method | customfield_10240 | Manual |
| Grooming Status | customfield_10212 | Not Started |
| Grooming Status (migrated) | customfield_10649 | Not Started |
| Has been Approved | customfield_10232 | No |
| Independent Story | customfield_10101 | No |
| Is Required Downtime | customfield_10245 | N |
| Is Required Downtime | customfield_11847 | N |
| Issue Priority | customfield_10102 | Medium |
| IT Risk Approval | customfield_10133 | Pending |
| Logs / Description | customfield_11491 | Log: xxxx URL: xxxx |
| Penetration Test Status | customfield_10183 | Not Started |
| Penetration Test Status (migrated) | customfield_10654 | Not Started |
| Priority | customfield_10610 | Medium |
| QbD Status OLD | customfield_10050 | Not Required |
| Regulatory Related | customfield_10260 | No |
| Regulatory Status | customfield_10201 | No Issues |
| Regulatory Status (migrated) | customfield_10647 | No Issues |
| Release Confirmation | customfield_10637 | Not Confirmed Internal |
| Release Confirmation (API) | customfield_10200 | Not Confirmed Internal |
| Requirement Status | customfield_10207 | Not Completed |
| Root Cause | customfield_12535 | Unknown |
| SAT Process | customfield_10274 | PENDING |
| SAT Status(Migrated) | customfield_12360 | Not Start |
| SD Required | customfield_10257 | no |
| Segment | customfield_10193 | Retail |
| Severity | customfield_10168 | 3 - Medium |
| Severity (migrated) | customfield_10597 | 3 - Medium |
| SIT retest failure tracking | customfield_15014 | 0.0 |
| SIT Shakedown Status | customfield_10189 | Not Started |
| Solution Remark (Nonstd) | customfield_10216 | To be Confirmed |
| Solution Status | customfield_10640 | To be Confirmed |
| Squad Estimation Status | customfield_10229 | Estimation In Progress |
| Target Fix Date Adjustment Flag | customfield_15017 | No |
| Test Cases Review | customfield_10150 | In-progress |
| Testing environment | customfield_15163 | Non-Aging |
| Toggle Flag | customfield_11588 | No Toggle Flag |
| Training Material Status | customfield_10176 | Not Started |
| UAT Estimation Status | customfield_10234 | Estimation In Progress |
| UAT Execution By | customfield_13554 | UAT Team |
| UAT Execution By | customfield_10237 | Squad Team |
| UAT Owner | customfield_10184 | KANRUTHAI ASAVAROONGPAISAL |
| UAT retest failure tracking | customfield_15015 | 0.0 |
| UAT Shakedown Status | customfield_10194 | Not Started |
