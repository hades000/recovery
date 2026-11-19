# TB0001-1172 [RWB-E1-010] Excel and SharePoint loads

| Field | Value |
|---|---|
| Jira | [TB0001-1172](https://scbjira.atlassian.net/browse/TB0001-1172) |
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
| Created | 2026-11-05T12:37:12.684+0700 |
| Updated | 2026-11-18T17:18:12.957+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a data steward and data product owner (RW-DATASTEW), I want every inventoried tracker with a load decision loaded into its data product, with the row counts reconciled and the team manager's sign-off, so that the teams' own lists are held in the Workbench data store.

## Acceptance criteria

```gherkin
Feature: Excel and SharePoint loads

  Background:
    Given tracker "LIT-07 Litigation case tracker" of team LIT has decision LOAD, target data product DP07 and status LISTED
    Given its field list holds 18 fields, of which "Customer name" and "Mobile" are tagged personal

  Scenario: AC1 File loaded
    Given the file "LIT-07 Litigation tracker 2026-11-20.xlsx" with 1,240 rows, each with an account number found in loan_account
    When the data steward calls POST /admin/trackers/{trackerId}/loads with the file
    Then the response is 202 with a Job of type "TRACKER" and status RUNNING
    Then tracker_row holds 1,240 rows for LIT-07 with target data product DP07 and source file name "LIT-07 Litigation tracker 2026-11-20.xlsx"
    Then the tracker shows 1,240 file rows, 1,240 loaded, 0 rejected and status LOADED

  Scenario: AC2 Reconciled
    Given the LIT-07 load shows 1,240 file rows, 1,240 loaded and 0 rejected
    When the team manager of team LIT calls POST /admin/trackers/{trackerId}/sign-off with confirmed row count 1,240
    Then the tracker status is SIGNED_OFF with the team manager's user ID and the sign-off time

  Scenario: AC3 Rejected rows
    Given the LIT-07 file has 1,240 rows, of which 17 have no account number
    When the load runs
    Then the system writes 1,223 rows to tracker_row
    Then the system writes 17 dq_exception rows with check code "TRK-01" and record keys "LIT-07 row 14" to "LIT-07 row 1,205"
    Then the data steward and the LIT team manager receive MSG-P1-008 "1,223 rows loaded from LIT-07 Litigation tracker 2026-11-20.xlsx. 17 rows rejected; the reject list is on the load."
    Then GET /admin/data-quality/exceptions with product "DP07" returns the 17 rejected rows

  Scenario: AC4 Personal fields are dropped
    Given the LIT-07 file of 1,240 rows
    When the load runs
    Then no tracker_row holds a value for "Customer name" or "Mobile"
    Then each tracker_row holds the 16 other fields
    Then the load_run check results show "DROPPED_PERSONAL_FIELDS" = 2

  Scenario: AC5 Account number not found
    Given 5 rows of the LIT-07 file carry account numbers not in loan_account
    When the load runs
    Then the system rejects the 5 rows with check code "TRK-02"
    Then the system writes 1,235 rows

  Scenario: AC6 Counts do not match at sign-off
    Given the LIT-07 load shows 1,240 file rows, 1,223 loaded and 17 rejected
    When the team manager of team LIT signs off with confirmed row count 1,251
    Then the system refuses the sign-off with MSG-P1-009 "The counts do not match: 1,251 rows confirmed, 1,240 rows in the file, 1,223 loaded, 17 rejected. Sign-off is not allowed."
    Then the tracker status stays LOADED

  Scenario: AC7 The person who loaded cannot sign off
    Given a user who holds RW-DATASTEW and RW-TEAMMGR for team LIT loaded the LIT-07 file
    When the same user signs off
    Then the system refuses the sign-off with MSG-P7-002 "You prepared this decision, so you cannot approve it."

  Scenario: AC8 Team manager of another team
    Given the LIT-07 load is LOADED
    When the team manager of team NPA signs off LIT-07
    Then the system refuses the sign-off with 403 and MSG-P4-002

  Scenario: AC9 Tracker without a load decision
    Given tracker "TDR-03 Restructure follow-up list" has decision KEEP and status KEPT
    When the data steward uploads a file for TDR-03
    Then the system refuses the upload with MSG-P1-010 "TDR-03 cannot be loaded: its decision is KEEP and its status is KEPT."
    Then the system stores no file

  Scenario: AC10 Same file uploaded again
    Given "LIT-07 Litigation tracker 2026-11-20.xlsx" was loaded on 2026-11-20
    When the data steward uploads the same file again
    Then the response is 409 with MSG-P1-011
    Then tracker_row is unchanged

  Scenario: AC11 New file before sign-off
    Given the LIT-07 load of 2026-11-20 is LOADED with 1,223 rows and not signed off
    When the data steward uploads "LIT-07 Litigation tracker 2026-11-23.xlsx" with 1,262 rows, all matched
    Then tracker_row holds 1,262 rows for LIT-07, all from the 2026-11-23 file
    Then the load_run of 2026-11-20 has status SUPERSEDED

  Scenario: AC12 File type not allowed
    Given a file "LIT-07 tracker.pdf"
    When the data steward uploads it for LIT-07
    Then the response is 415 with MSG-P1-018 "Use an .xlsx or .csv file of at most 20 MB for a tracker load."

  Scenario: AC13 Header does not match the field list
    Given the LIT-07 file has no column "Court name", which is in the field list
    When the load runs
    Then the system refuses the load at structure with MSG-P1-002 "The LIT-07 load for 2026-11-20 was refused: structure. The previous load is still in use."
    Then no tracker_row for that file is written
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
