# TB0001-1185 [RWB-E1-023] Case record view v1, read only

| Field | Value |
|---|---|
| Jira | [TB0001-1185](https://scbjira.atlassian.net/browse/TB0001-1185) |
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
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:24.026+0700 |
| Updated | 2026-11-18T17:23:00.781+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a case owner (RW-CASEOWN), I want one read-only screen per case with the case ID, accounts, arrears, owner, queue, stage, status, contact history and documents, read from the data products with the business date of each, so that I stop searching files and systems to understand a case.

## Acceptance criteria

```gherkin
Feature: Case record view v1, read only

  Background:
    Given case owner U-81 owns case RW-2026-000701, a hire purchase case with 2 accounts
    Given the latest business date is 2026-12-02

  Scenario: AC1 Loads fast
    Given case RW-2026-000701 has 50 documents and 120 contact history entries
    When U-81 opens the case record view
    Then the header, accounts, parties, contact history and the first page of documents show in under 2 seconds at the 95th percentile over 50 openings

  Scenario: AC2 Data from products
    Given the account data product for 2026-12-02 holds days past due 97 and total balance THB 206,175.00 for account A-7001
    When the view opens
    Then the Accounts section shows 97 days past due and THB 206,175.00 for A-7001
    Then the section shows business date 2026-12-02
    Then the header shows queue "TDR-BKK-CO", owner U-81, status "IN_PROGRESS" and entry date 2026-11-30

  Scenario: AC3 Customer facts from the load
    Given the customer profile for the borrower arrived in the COLLINS load of 2026-12-02
    When the view opens
    Then the Parties section shows the borrower with role "BORROWER", segment "RETAIL" and business date 2026-12-02
    Then the contact history shows the EFS entries with channel, direction, result and time

  Scenario: AC4 Stale data product
    Given the COLLINS load for 2026-12-03 was refused and the account data product is from 2026-12-02
    When U-81 opens the view on 2026-12-03
    Then the Accounts section shows business date 2026-12-02
    Then the stale banner shows MSG-P1-001 for the account data product with date 2026-12-02

  Scenario: AC5 Case outside the scope
    Given case RW-2026-000702 belongs to team "LIT-BKK" and U-81 has scope Own
    When U-81 opens case RW-2026-000702
    Then the response is 404 with MSG-P4-003
    Then no case data shows

  Scenario: AC6 Document hub unavailable
    Given the document hub does not answer within 3 seconds
    When U-81 opens the view
    Then the Documents section shows MSG-P3-023 for "Documents"
    Then the header, accounts, parties and contact history show

  Scenario: AC7 Personal data access log unavailable
    Given the personal data access log cannot be written
    When U-81 opens the view
    Then the borrower's name and customer number show masked
    Then the Parties section shows MSG-P3-023 for "Personal details"

  Scenario: AC8 Masking by role
    Given phone collector U-82 may not see the customer number unmasked
    Given the case is in U-82's scope
    When U-82 opens the view
    Then the customer number shows masked as "xxxxxx4821"
    Then the access log holds the read with user U-82 and the masked result

  Scenario: AC9 Case on hold
    Given case RW-2026-000701 has status "ON_HOLD" for deviation X1 with prescription date 2028-03-15
    When U-81 opens the view
    Then the on hold banner shows MSG-P3-004 with "X1" and 2028-03-15

  Scenario: AC10 No documents and no contact history
    Given case RW-2026-000703 has no documents and no contact history
    When its owner opens the view
    Then the Documents and Contact history sections each show MSG-P3-024
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
