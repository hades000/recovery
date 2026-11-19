# TB0001-1198 [RWB-E1-037] Role to permission matrix as data and PDPA field masking by role

| Field | Value |
|---|---|
| Jira | [TB0001-1198](https://scbjira.atlassian.net/browse/TB0001-1198) |
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
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:36.676+0700 |
| Updated | 2026-11-18T17:22:58.939+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 2 |
| Comments | 1 |

## Description

As a product owner, I want the mapping of roles to capability areas, the scope of each role and the masking of each personal data field held as versioned tables that every screen and API applies, so that a change of rights is a data load with an approver, a person sees only the cases in their scope, and personal data shows unmasked only to roles that need it.

## Acceptance criteria

```gherkin
Feature: Role to permission matrix as data and PDPA field masking by role

  Background:
    Given the environment is SIT
    Given permission matrix version "PM-2026.11" is in force
    Given RW-LEGAL holds "-" in Queue and allocation in "PM-2026.11"
    Given masking version "MASK-SIT-01" is in force, in which only RW-CASEOWN sees contact_point.value_token unmasked

  Scenario: AC1 Matrix as data
    Given test user "U-2101" holding RW-REFADM loads matrix file "PM-2026.12" with table "permission" and validFrom "2026-12-01"
    Given the file gives RW-LEGAL the letter "R" in Queue and allocation and is otherwise equal to "PM-2026.11"
    Given test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    When test user "U-2103" holding RW-LEGAL signs in on 1 December 2026 and calls GET /queues
    Then the call returns status 200, where under "PM-2026.11" it returned 403, with no deployment
    Then one decision log entry exists with final call "APPROVED", the load ID, version "PM-2026.12", 756 rows and approver "U-2102"

  Scenario: AC2 Masking
    Given test user "U-2104" holds only RW-PHONECOL
    When the user opens case "RW-2026-000123" in the case record view
    Then the borrower's identity number shows as "XXXXXXXXX1234" and the phone number as "XXXXXX5678"
    Then the system makes no request to the ACE PII service for clear values
    Then the system writes the view to the access event stream with the case ID and the fields shown masked

  Scenario: AC3 Denied action
    Given test user "U-2105" holds only RW-CASEOWN, whose Queue and allocation letter is "R"
    When the user calls POST /cases/{caseId}/transfer for case "RW-2026-000123"
    Then the system refuses the call with status 403 and message MSG-P4-002 before the handler runs
    Then the case owner and queue are unchanged
    Then the system writes one refusal event with area "QUEUE_AND_ALLOCATION" and right "U"

  Scenario: AC4 A case outside the scope is not returned
    Given test user "U-2105" holds RW-CASEOWN with default scope "OWN" and owns 12 cases
    Given case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    When the user calls GET /cases
    Then 12 cases return and the total is 12
    Then GET /cases/{caseId} for "RW-2026-000456" returns status 404 with message MSG-P4-003

  Scenario: AC5 A matrix file with an error is refused in full
    Given matrix file "PM-2026.13" lists RW-CASEOWN twice for Case record and gives RW-AUDIT the letters "RX" in Reporting
    When test user "U-2101" loads it
    Then the system refuses the load with message MSG-P1-002 naming the duplicate row and the invalid letters
    Then the system stores no row of "PM-2026.13" and "PM-2026.11" stays in force

  Scenario: AC6 The loader cannot approve, and only the table's approver role may
    Given load "PM-2026.12" was loaded by test user "U-2101"
    When "U-2101" calls approve on that load
    Then the system refuses the call with message MSG-P7-002 and the load stays "Loaded"
    Then when test user "U-2106" holding RW-COE calls approve on that load
    Then the system refuses the call with status 403 and message MSG-P4-002

  Scenario: AC7 An approval that cannot be recorded does not take effect
    Given the decision log store is unavailable
    When test user "U-2102" holding RW-SECADM approves load "PM-2026.12"
    Then the call returns status 503 with message MSG-P7-003
    Then the load stays "Loaded" and "PM-2026.11" stays in force

  Scenario: AC8 A leaver loses access at the next request
    Given test user "U-2107" holds RW-TEAMMGR and has an open session since 08:00
    Given the access administrator removes "U-2107" from group "RWB-SIT-RW-TEAMMGR" at 10:00
    When the user calls GET /cases at 10:06, after the 5 minute membership refresh
    Then the system refuses the call with status 401 and message MSG-P4-001
    Then the system ends the session and a new sign-in is refused

  Scenario: AC9 A personal field with no masking rule is masked
    Given no masking rule in "MASK-SIT-01" covers party.date_of_birth for any role
    When test user "U-2105" holding RW-CASEOWN opens case "RW-2026-000123"
    Then the date of birth shows masked as "XXXX-XX-XX"

  Scenario: AC10 Two approvals of the same load at once
    Given load "PM-2026.12" is "Loaded"
    When two approve calls for it arrive at the same time from "U-2102" and test user "U-2108" holding RW-SECADM
    Then one call approves and one decision log entry is written
    Then the other call returns status 409 with message MSG-GEN-004 and writes nothing
```

## Comments (1)

### Comment 1: Nitchayaphan Kanpirompachira, 2026-11-17T18:26:53.038+0700, edited 2026-11-18T16:47:37.789+0700

Comment ID 1795594

After reviewing the card, I have the following questions that need clarification:

# *Maximum File Size Limit for Reference Data Upload*

The endpoint {{POST /admin/reference-loads}} handles file uploads for reference data (e.g., {{permission}} and {{masking_rule}} tables), and currently specifies {{HTTP 422 (MSG-GEN-001)}} for empty files.

*Questions:*

* What is the defined maximum allowed file size (e.g., 10MB, 20MB) for files uploaded via {{POST /admin/reference-loads}}?
* If an uploaded file exceeds the maximum limit, what is the expected HTTP response status and error message code? (e.g., {{HTTP 413 Payload Too Large}} or {{HTTP 422 Unprocessable Entity}} with a specific message code?)



# *Sample Reference Load File for* {{permission}} Table

The endpoint {{POST /admin/reference-loads}} is specified to handle reference data loads for the {{permission}} table.

*Could you provide:* A sample file (e.g., CSV or JSON format with column headers/schema and sample rows) used to load data into the {{permission}} table via {{POST /admin/reference-loads}}?



# *Permission Action Format and Ordering*

In the permission data load, permissions are indicated by action letters (e.g., {{C}}, {{R}}, {{U}}, {{D}}, {{A}}).

*Questions:* How should development handle missing actions or placeholder characters (e.g., {{CRUD-}} or {{C-R--}})? Should the backend parse any arbitrary combination of allowed characters, or is there an expected fixed-length/positional mask format?



# *Sample Reference Load File for* {{masking_rule}} Table

Similar to permissions, the {{masking_rule}} reference data is expected to be loaded via {{POST /admin/reference-loads}}.

*Could you provide:* A sample file (headers, fields, and example rows) used for loading the {{masking_rule}} table?



# *Session Duration and Timeout (DL38)*

Regarding session management referenced under Decision Log DL38:

*Question:* Could you confirm the exact session duration and timeout rules before a user is required to initiate a new session? is it 15 minutes ?

** What is the defined timeout limit (e.g., idle inactivity timeout vs. absolute session lifetime)?
** What specific trigger/condition marks the session as expired requiring a new session to be created?


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
