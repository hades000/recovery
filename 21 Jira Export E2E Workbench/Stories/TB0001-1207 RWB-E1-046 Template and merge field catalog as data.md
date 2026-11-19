# TB0001-1207 [RWB-E1-046] Template and merge field catalog as data

| Field | Value |
|---|---|
| Jira | [TB0001-1207](https://scbjira.atlassian.net/browse/TB0001-1207) |
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
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:43.768+0700 |
| Updated | 2026-11-17T10:07:54.563+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a litigation officer (RW-LITOFF), I want letter and document templates and their merge fields held as versioned data with the Legal approval record on each version, so that a template change is a data release approved by Legal and never a code release.

## Acceptance criteria

```gherkin
Feature: Template and merge field catalog as data

  Background:
    Given the merge field catalog version "MF-2026.11" is in force with merge codes "CASE_NO", "CUSTOMER_NAME", "POSTAL_ADDRESS", "TOTAL_OUTSTANDING" and "NOTICE_DATE"
    Given template "DEMAND-MTG" in language "TH" has version 1 Approved by user "LEG-0001" on 2026-10-01

  Scenario: AC1 Template versioned
    Given a load file for template "DEMAND-MTG" language "TH" approved by user "LEG-0001" on 2026-11-10 with valid from 2026-11-10
    When it is loaded on 2026-11-10
    Then the system creates version 2 of "DEMAND-MTG" with state "Approved", approver "LEG-0001" and approval date 2026-11-10
    Then TemplateCatalog returns version 2 as current for "DEMAND-MTG", "TH" on 2026-11-10
    Then version 1 stays readable with its own approver and approval date

  Scenario: AC2 Unapproved template blocked
    Given template "RECALL-HP" in language "TH" has only version 1 in state "Draft"
    When the letter engine asks TemplateCatalog for the current version of "RECALL-HP", "TH"
    Then the catalog refuses with TemplateNotApprovedException
    Then the refusal carries MSG-P6-005 naming "RECALL-HP" version 1

  Scenario: AC3 Merge fields checked
    Given a load file for template "GUARANTOR-SSME" whose body uses the merge code "GUARANTOR_EMAIL"
    Given "GUARANTOR_EMAIL" is not in the catalog
    When it is loaded
    Then the system refuses the load in full with MSG-P6-006 naming "GUARANTOR_EMAIL"
    Then the system creates no version of "GUARANTOR-SSME"

  Scenario: AC4 Catalog row with an unknown field ID is refused
    Given a catalog load file of 12 rows where row 7 names a BR Field ID "XX-CAS-999" that is not in the data dictionary
    When it is loaded
    Then the system refuses the load in full with MSG-P1-002 naming the check "field ID not in the data dictionary"
    Then catalog version "MF-2026.11" stays in force

  Scenario: AC5 Template row with a missing required field is refused
    Given a template load file whose row has no body reference
    When it is loaded
    Then the system refuses the load in full with MSG-GEN-001 naming "body_ref"

  Scenario: AC6 Repeated load creates no new version
    Given the load file of AC1 has been loaded once and version 2 exists
    When the same file with the same file hash is loaded again
    Then the system refuses the load with MSG-P1-002 naming the check "repeat of load"
    Then "DEMAND-MTG" still has 2 versions

  Scenario: AC7 Withdrawn current version leaves no current version
    Given version 2 of "DEMAND-MTG" "TH" was Approved and current and is now in state "Withdrawn"
    When the letter engine asks TemplateCatalog for the current version of "DEMAND-MTG", "TH" on 2026-11-20
    Then TemplateCatalog returns no current version and throws TemplateWithdrawnException
    Then the refusal carries MSG-P6-003 naming "DEMAND-MTG"

  Scenario: AC8 Future valid from date keeps the earlier version current
    Given version 3 of "DEMAND-MTG" "TH" is Approved with valid from 2026-12-01
    When TemplateCatalog is asked on 2026-11-30 and on 2026-12-01
    Then it returns version 2 on 2026-11-30
    Then it returns version 3 on 2026-12-01
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
