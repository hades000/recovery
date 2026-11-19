# TB0001-1215 [RWB-E1-054] Review queue for low-confidence documents

| Field | Value |
|---|---|
| Jira | [TB0001-1215](https://scbjira.atlassian.net/browse/TB0001-1215) |
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
| Created | 2026-11-05T12:37:50.261+0700 |
| Updated | 2026-11-18T17:23:00.133+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a litigation officer, I want a queue of documents with low classification or extraction confidence, each correctable in one screen, with the correction fed back to the labeled set, so that no document is attached wrongly and the models improve.

## Acceptance criteria

```gherkin
Feature: Review queue for low-confidence documents

  Background:
    Given DOCTYPE-2026.11 is in force and the classify_threshold of every type is 0.8000
    Given REVIEW_TEAM_UNATTACHED is "LIT-BKK" for this test
    Given a litigation officer with role RW-LITOFF in team "LIT-BKK" with team scope

  Scenario: AC1 Queued
    Given intake item "IN-0101" on which classification returned "COURT_NOTICE" 0.6200 and "DEMAND_LETTER" 0.2100
    Given its review_reason is "LOW_CONFIDENCE"
    When the officer opens SCR-31
    Then the system lists "IN-0101" with reason "LOW_CONFIDENCE" and the candidates "COURT_NOTICE 0.62" and "DEMAND_LETTER 0.21"

  Scenario: AC2 Corrected
    Given intake item "IN-0101" in the review queue with hearing_date "2026-12-15" in state "REVIEW"
    When the officer sets type "COURT_NOTICE", corrects hearing_date to "2026-12-16", confirms the other fields, chooses case "RW-2026-000201" and chooses Attach
    Then the system stores a document on "RW-2026-000201" with type "COURT_NOTICE" and hearing_date field_value "2026-12-16", extracted_value "2026-12-15", state "CORRECTED" and confirmed_by the officer's user ID
    Then the document review_status is "CORRECTED" and "IN-0101" has review_outcome "ATTACHED"
    Then the store writes one DOCATT decision log entry
    Then LabeledSetReader returns "IN-0101" with predicted type, confirmed type, extracted value and corrected value

  Scenario: AC3 A stored document with a field to check
    Given document "DOC-0103" on case "RW-2026-000202" has black_case_no "Por 2001/2569" in state "REVIEW" and review_status "PENDING"
    When the officer chooses Confirm on black_case_no and completes the review
    Then black_case_no has state "CONFIRMED" and confirmed_by the officer's user ID
    Then the document review_status is "CONFIRMED"

  Scenario: AC4 An empty correction is refused
    Given document "DOC-0103" has court_name in state "REVIEW"
    When the officer chooses Correct on court_name with an empty value
    Then the response is 422 with MSG-GEN-001 naming "Court name"
    Then court_name is unchanged

  Scenario: AC5 A type not in the list is refused
    Given intake item "IN-0104" in the review queue
    When the officer sets the type to "PAYSLIP"
    Then the response is 422 with MSG-P5-006 naming "PAYSLIP"

  Scenario: AC6 A date outside the allowed range is refused
    Given REVIEW_DATE_MIN is 2000-01-01 and REVIEW_DATE_MAX is 2100-12-31
    When the officer corrects hearing_date on "IN-0101" to "2569-12-16"
    Then the response is 422 with MSG-GEN-002 naming "Hearing date", "2000-01-01" and "2100-12-31"

  Scenario: AC7 Attach with a field still in review is refused
    Given intake item "IN-0105" has two fields in state "REVIEW" and the officer has confirmed one
    When the officer chooses Attach
    Then the response is 422 with MSG-GEN-001 naming the field still in review
    Then the system stores no document

  Scenario: AC8 A closed case is refused
    Given intake item "IN-0106" with review_reason "CASE_CLOSED" and candidate case "RW-2026-000150" with status "Closed"
    When the officer chooses case "RW-2026-000150" and chooses Attach
    Then the response is 422 with MSG-P5-005 naming "RW-2026-000150"
    Then the system stores no document

  Scenario: AC9 Two officers on the same item
    Given two officers opened intake item "IN-0107" at version 3
    Given the first officer attached it, so the item is at version 4
    When the second officer chooses Attach with version 3
    Then the response is 409 with MSG-GEN-004
    Then one document exists for "IN-0107"

  Scenario: AC10 A type change re-runs extraction for the new type
    Given intake item "IN-0108" was classified "DEMAND_LETTER" with five extracted fields
    When the officer sets the type to "GUARANTOR_NOTICE"
    Then extraction runs for "GUARANTOR_NOTICE" and the item shows its four fields, each in state "REVIEW"
    Then the DEMAND_LETTER fields are no longer offered

  Scenario: AC11 The file is already on the chosen case
    Given document "DOC-0109" on case "RW-2026-000203" holds a file with hash "H109"
    Given intake item "IN-0109" holds the same file
    When the officer attaches "IN-0109" to "RW-2026-000203"
    Then the system stores no second document and "IN-0109" is linked to "DOC-0109"
    Then the screen shows MSG-P5-024 naming "DOC-0109"

  Scenario: AC12 Discard an unreadable item
    Given intake item "IN-0110" with review_reason "UNREADABLE_FILE"
    When the officer chooses Discard with reason "Blank page from the branch scanner"
    Then "IN-0110" has review_outcome "DISCARDED" with the reason, the officer's user ID and the time
    Then it leaves the queue and no document is stored

  Scenario: AC13 Discard without a reason is refused
    Given intake item "IN-0112" with review_reason "RESCAN"
    When the officer chooses Discard with an empty reason
    Then the response is 422 with MSG-GEN-001 naming "Reason"
    Then "IN-0112" stays in the queue

  Scenario: AC14 The queue lists items in scope, oldest first
    Given 3 review items for team "LIT-BKK" received on 2 November, 4 November and 3 November
    Given 2 review items of team "HP-NE"
    When the officer opens SCR-31
    Then 3 items show, in the order 2 November, 3 November, 4 November
    Then no item of team "HP-NE" shows

  Scenario: AC15 An empty queue
    Given no review item for team "LIT-BKK"
    When the officer opens SCR-31
    Then the screen shows the empty state "No documents are waiting for review."

  Scenario: AC16 A document outside the officer's scope
    Given document "DOC-0111" belongs to a case of team "HP-NE"
    When the officer calls GET /api/recovery/v1/documents/DOC-0111
    Then the response is 404 with MSG-P4-003

  Scenario: AC17 The same confirmation sent twice
    Given the officer confirmed black_case_no on "DOC-0103"
    When the same PATCH with confirmed true and the same value arrives again
    Then the response is 200 with the saved field
    Then confirmed_by and updated_at are unchanged
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
