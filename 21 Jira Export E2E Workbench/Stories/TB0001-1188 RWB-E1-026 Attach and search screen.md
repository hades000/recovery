# TB0001-1188 [RWB-E1-026] Attach and search screen

| Field | Value |
|---|---|
| Jira | [TB0001-1188](https://scbjira.atlassian.net/browse/TB0001-1188) |
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
| Created | 2026-11-05T12:37:26.427+0700 |
| Updated | 2026-11-18T17:23:01.005+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a case owner (RW-CASEOWN), I want to upload, see and search the documents of a case from the case record view, so that the case file is complete and I find a document by type and date without leaving the case.

## Acceptance criteria

```gherkin
Feature: Attach and search screen

  Background:
    Given document type table version "DOCTYPE-2026.11" is in force
    Given user "TEST-CO-01" holds RW-CASEOWN and owns case "RW-2026-000123"

  Scenario: AC1 Upload
    Given "TEST-CO-01" is on the Documents tab of case "RW-2026-000123"
    When "TEST-CO-01" uploads "court-notice-0007.pdf" of 2 MB with type "COURT_NOTICE"
    Then the response is 201 with source "UPLOAD" and doc_version 1
    Then the document shows at the top of the case document list within 5 seconds of submit
    Then GET /cases/{caseId}/documents with type "COURT_NOTICE" returns it

  Scenario: AC2 Search
    Given case "RW-2026-000123" holds 50 documents of which 12 are "COURT_NOTICE"
    Given 4 of the court notices were stored between 1 October 2026 and 31 October 2026
    When "TEST-CO-01" searches type "COURT_NOTICE" from 1 October 2026 to 31 October 2026
    Then exactly the 4 court notices stored in October show, newest first
    Then the result count reads 4

  Scenario: AC3 Checklist placeholder
    Given case "RW-2026-000123" holds 12 court notices and 1 appraisal report and no other agreed type
    When the Documents tab opens
    Then the checklist placeholder lists the six agreed types
    Then COURT_NOTICE shows present with 12, APPRAISAL_REPORT shows present with 1
    Then DEMAND_LETTER, TITLE_DEED, SETTLEMENT_AGREEMENT and GUARANTOR_NOTICE show not present

  Scenario: AC4 Upload without a type
    Given "TEST-CO-01" picks "scan-0009.pdf" and no document type
    When "TEST-CO-01" submits the upload
    Then the response is 422 with MSG-GEN-001 naming "Document type"
    Then the system stores no document

  Scenario: AC5 Upload that fails the malware scan
    Given a test file "eicar-0001.pdf" holding the EICAR test signature
    When "TEST-CO-01" uploads it with type "COURT_NOTICE"
    Then the response is 422 with MSG-P5-016
    Then the file is in the quarantine container and no document row exists

  Scenario: AC6 File type not allowed
    Given a file "minutes-0002.xlsx" with spreadsheet content
    When "TEST-CO-01" uploads it with type "SETTLEMENT_AGREEMENT"
    Then the response is 415 with MSG-P5-001 shown in the upload dialog
    Then the system stores no document

  Scenario: AC7 The same file uploaded again
    Given "court-notice-0007.pdf" is stored on case "RW-2026-000123" as "COURT_NOTICE"
    When "TEST-CO-01" uploads the same file with the same type
    Then the response is 200 with the existing document ID and MSG-P5-024
    Then the case still holds one copy of that court notice

  Scenario: AC8 Double submit
    Given "TEST-CO-01" submits "appraisal-0003.pdf" with Idempotency-Key "TEST-KEY-0001"
    When the same request with Idempotency-Key "TEST-KEY-0001" arrives a second time within 1 second
    Then both responses carry the same document ID
    Then one document row and one decision log entry exist for it

  Scenario: AC9 Date range in the wrong order
    Given "TEST-CO-01" is on the Documents tab
    When "TEST-CO-01" searches from 31 October 2026 to 1 October 2026
    Then the search is not run and MSG-GEN-003 shows next to the date fields

  Scenario: AC10 No document matches
    Given case "RW-2026-000123" holds no "TITLE_DEED"
    When "TEST-CO-01" searches type "TITLE_DEED"
    Then the list shows the empty state "No documents match this search." with the action "Clear the search"

  Scenario: AC11 Case outside the scope
    Given user "TEST-CO-02" holds RW-CASEOWN with scope OWN and does not own case "RW-2026-000123"
    When "TEST-CO-02" opens the Documents tab of that case
    Then GET /cases/{caseId}/documents returns 403 with MSG-P4-003
    Then the system shows no document name
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
