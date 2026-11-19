# TB0001-1180 [RWB-E1-018] Case ID issuance and case record v1

| Field | Value |
|---|---|
| Jira | [TB0001-1180](https://scbjira.atlassian.net/browse/TB0001-1180) |
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
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:19.472+0700 |
| Updated | 2026-11-17T21:34:38.026+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a product owner, I want every account at 90 days past due or more that is not excluded placed on one recovery case per customer and product, with a case ID in the form RW-YYYY-NNNNNN issued at creation and never reused, a status and its linked accounts, created by rule from the daily load, so that every team, letter and document refers to one case ID.

## Acceptance criteria

```gherkin
Feature: Case ID issuance and case record v1

  Background:
    Given parameter "case.entry.dpd" is 90
    Given the exclusion rows version "EXCL-2026.11" are in force
    Given the business date is 2026-12-01
    Given the COLLINS load for 2026-12-01 has passed its checks

  Scenario: AC1 Case created at 90 days past due
    Given account A-5001 of customer P-0101, product group "HIRE_PURCHASE", reaches 90 days past due in the load with no exclusion
    Given the last case number issued in 2026 is RW-2026-000122
    When the entry rule runs
    Then case RW-2026-000123 exists with status "NEW", no stage code and entry date 2026-12-01
    Then the system links account A-5001 as the primary account and P-0101 as "BORROWER"
    Then the system publishes caseCreated with case number RW-2026-000123

  Scenario: AC2 Exclusion applied
    Given account A-5002 at 92 days past due with tdr_flag = true
    When the entry rule runs
    Then the system creates no case for A-5002
    Then an exclusion record holds account A-5002, reason "ACTIVE_PLAN", the exclusion rule ID and version "EXCL-2026.11"

  Scenario: AC3 One case per customer and product
    Given customer P-0102 has two hire purchase accounts A-5003 and A-5004, both at 95 days past due
    When the entry rule runs
    Then one case exists for P-0102 and "HIRE_PURCHASE" with both accounts linked
    Then total outstanding at entry is the sum of the two balances, THB 412,350.00

  Scenario: AC4 ID never reused
    Given case RW-2026-000123 was closed on 2026-12-15
    When a new case is created on 2026-12-16
    Then it receives RW-2026-000124
    Then case RW-2026-000123 is still returned by a search on its case number

  Scenario: AC5 State model as data
    Given the list LOV-CASE-STATUS gains the value "WAITING_COURT" through a list load with valid from 2027-01-01
    When a case moves to "WAITING_COURT" on 2027-01-02
    Then the case service accepts the value without a code change
    Then the decision log entry for the move carries the list version in force

  Scenario: AC6 Exclusion rules as data
    Given the exclusion rows include reason "OPEN_DISPUTE"
    When account A-5005 at 90 days past due with an open dispute arrives
    Then the system creates no case
    Then the exclusion record for A-5005 holds reason "OPEN_DISPUTE"

  Scenario: AC7 The entry threshold boundary
    Given account A-5006 at 89 days past due and account A-5007 at 90 days past due, both with no exclusion
    When the entry rule runs
    Then the system creates a case for A-5007
    Then the system creates no case for A-5006

  Scenario: AC8 A repeated run creates nothing new
    Given JOB-02 has created case RW-2026-000125 for account A-5008 on 2026-12-01
    When JOB-02 runs again for 2026-12-01
    Then account A-5008 has one case link
    Then the system issues no case number in the second run

  Scenario: AC9 No cases from a refused load
    Given the COLLINS load for 2026-12-02 was refused at the control total check
    When the morning schedule runs
    Then JOB-02 does not start for 2026-12-02
    Then the job monitor shows MSG-P1-001 for the account data product
    Then JOB-02 runs for 2026-12-02 after the next load passes

  Scenario: AC10 The decision log write fails
    Given the decision log store is unavailable
    When the entry rule runs for account A-5009
    Then no case exists for A-5009
    Then the job record lists A-5009 as failed with MSG-P7-003
    Then the system takes A-5009 again in the next run

  Scenario: AC11 The yearly number range is used up
    Given the last case number issued in 2026 is RW-2026-999999
    When account A-5010 qualifies for a new case on 2026-12-30
    Then the system creates no case for A-5010
    Then the job record carries MSG-P3-025 with year 2026
    Then the system raises an incident to the platform administrator

  Scenario: AC12 Two products give two cases
    Given customer P-0103 has mortgage account A-5011 and hire purchase account A-5012, both at 91 days past due
    When the entry rule runs
    Then two cases exist for P-0103, one with product group "MORTGAGE" and one with "HIRE_PURCHASE"
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
