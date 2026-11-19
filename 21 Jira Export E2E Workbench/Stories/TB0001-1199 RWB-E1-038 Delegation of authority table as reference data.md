# TB0001-1199 [RWB-E1-038] Delegation of authority table as reference data

| Field | Value |
|---|---|
| Jira | [TB0001-1199](https://scbjira.atlassian.net/browse/TB0001-1199) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:37.480+0700 |
| Updated | 2026-11-18T17:28:11.827+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a Risk and model risk officer (RW-RISK), I want the delegation of authority (which approval level may approve which decision, by product, principal amount and second condition) held as a versioned table that the approval router reads, so that approval limits change by an approved data load and every approval can be checked against the limit that applied on its date.

## Acceptance criteria

```gherkin
Feature: Delegation of authority table as reference data

  Background:
    Given the environment is SIT
    Given test user "U-3101" holds RW-REFADM and test user "U-3102" holds RW-RISK

  Scenario: AC1 Table loaded
    Given the delegation of authority file "DOA-2026.11" built from Regulation กกค.540031 as amended by กกค.690070, with 95 limits
    When "U-3101" loads it with table "delegation_limit" and validFrom "2026-11-30" and "U-3102" approves it
    Then the system stores 218 rows : 109 decision and limit rows for MORTGAGE and 109 for SSME
    Then every row has a decision code, an approval level and a product, and no two rows repeat the same decision, regulation item, product, level and limits
    Then the system stores item 2.1.1 at level L4 as two rows: principal 300,000,000.00 with loss up to 45.00 percent and maximum loss 150,000,000.00, and principal 50,000,000.00 with no loss limit

  Scenario: AC2 Lookup
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D6.4, item 2.1.1, product MORTGAGE, principal 2,400,000.00, loss 20.00 percent and loss amount 480,000.00 on 15 December 2026
    Then the lookup returns level L6, the row ID of item 2.1.1 at L6 and version "DOA-2026.11"

  Scenario: AC3 Change
    Given "DOA-2026.11" is in force
    Given file "DOA-2027.01" adds a row for item 2.1.5 at level L5 with principal up to 10,000,000.00, validFrom "2027-01-01"
    When "U-3101" loads it and "U-3102" approves it
    Then the rows of "DOA-2026.11" stay readable with valid_to "2026-12-31"
    Then a lookup for D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 2 January 2027 returns L5 and version "DOA-2027.01"
    Then one decision log entry records the approval of "DOA-2027.01" with its valid from date

  Scenario: AC4 A file with an error is refused in full
    Given file "DOA-2026.12" gives item 2.1.1 at L5 a principal limit of 400,000,000.00, above the 300,000,000.00 of L4
    Given it gives one row the decision code "D6.9"
    When "U-3101" loads it
    Then the system refuses the load with message MSG-P1-002 naming the falling limit and the unknown decision code
    Then the system stores no row of "DOA-2026.12" and "DOA-2026.11" stays in force

  Scenario: AC5 The loader cannot approve and only Risk may
    Given load "DOA-2027.01" was loaded by "U-3101"
    When "U-3101" calls approve on it
    Then the system refuses the call with message MSG-P7-002
    Then when test user "U-3103" holding RW-PRODHEAD calls approve on it
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC6 An approval that cannot be recorded does not take effect
    Given the decision log store is unavailable
    When "U-3102" approves load "DOA-2027.01"
    Then the call returns status 503 with message MSG-P7-003 and the load stays "Loaded"

  Scenario: AC7 No limit covers the request
    Given "DOA-2026.11" holds no row for product HIRE_PURCHASE
    When the router asks who may approve decision D6.4, item 2.1.1, for HIRE_PURCHASE, principal 900,000.00
    Then the lookup returns "NOT_COVERED"
    Then the system raises an incident to the RW-RISK queue with message MSG-P7-010 naming D6.4 and HIRE_PURCHASE

  Scenario: AC8 The version valid on the decision date is used
    Given "DOA-2026.11" is valid to 31 December 2026 and "DOA-2027.01" from 1 January 2027
    When the router looks up D6.6, item 2.1.5, MORTGAGE, principal 8,000,000.00 dated 31 December 2026 and again dated 1 January 2027
    Then the first lookup returns L4 and "DOA-2026.11"
    Then the second returns L5 and "DOA-2027.01"

  Scenario: AC9 A write-off for a related party goes to the Board
    Given "DOA-2026.11" is in force
    When the router asks who may approve decision D9.2, item 2.1.10, criteria met, product SSME, principal 300,000.00, with related party flag true
    Then the lookup returns level L1 with reason "RELATED_PARTY"
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
