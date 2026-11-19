# TB0001-1202 [RWB-E1-041] Retention classes and virus scan on intake

| Field | Value |
|---|---|
| Jira | [TB0001-1202](https://scbjira.atlassian.net/browse/TB0001-1202) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | QA-Reviewed |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:39.737+0700 |
| Updated | 2026-11-18T17:22:59.907+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 2 |
| Comments | 2 |

## Description

As a compliance and PDPA officer (RW-COMPLY), I want every uploaded or scanned file checked for malware before it is stored, and a retention class per document type that the store applies and a monthly job acts on, so that the store holds only safe files and keeps each document for the time the policy sets, never removing one silently or while a legal hold is in place.

## Acceptance criteria

```gherkin
Feature: Retention classes and virus scan on intake

  Background:
    Given retention class table version "RET-2026.11" is in force
    Given class "LEGAL10Y" has period 120 months and end action "REVIEW"
    Given class "GENERAL05Y" has period 60 months and end action "ARCHIVE"

  Scenario: AC1 Malware blocked
    Given a test file "eicar-0002.pdf" with the EICAR signature as an intake item from a branch scanner
    When JOB-12 runs the scan step
    Then the item has scan_result "INFECTED" and the file is in the quarantine container
    Then no document row exists for the file and the OCR step does not read it
    Then the system writes the audit event "MALWARE_BLOCKED" with the intake ID and the source, and the platform administrator is alerted

  Scenario: AC2 Retention class
    Given a demand letter of type "DEMAND_LETTER" with class "LEGAL10Y" in the type table
    When the document is stored on case "RW-2026-000123"
    Then the document row carries retention class "LEGAL10Y" and write_once true
    Then the file is in the write-once container

  Scenario: AC3 Expiry with end action archive
    Given an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000123" with no legal hold
    When JOB-17 runs on 6 December 2026
    Then the document has state "ARCHIVED" and its blob is in the archive tier
    Then one decision log entry "DOCRET" names the document, class "GENERAL05Y", version "RET-2026.11" and expiry date 1 November 2026

  Scenario: AC4 Expiry with end action review
    Given a court notice of class "LEGAL10Y" stored on 1 November 2016 on case "RW-2026-000456"
    When JOB-17 runs on 6 December 2026
    Then the system lists the court notice in "retention/review/2026-12-06.csv" with its class and expiry date
    Then the document and its blob are unchanged

  Scenario: AC5 Legal hold overrides the class
    Given an appraisal report of class "GENERAL05Y" stored on 1 November 2021 on case "RW-2026-000789" with legal_hold true
    When JOB-17 runs on 6 December 2026
    Then the system does not archiv the document and not listed
    Then the job record counts it as held

  Scenario: AC6 Scanning service unavailable
    Given the scanning service stub returns no answer
    When JOB-12 runs twice with 3 unscanned intake items
    Then the 3 items have no scan_result and the OCR step reads none of them
    Then the system alerts the platform administrator after the second run
    Then an upload during the outage returns 503 with MSG-P5-022 and no document row or blob is written

  Scenario: AC7 Class not in the retention table
    Given a document with retention class "OLD03Y" that is not in version "RET-2026.11"
    When JOB-17 runs
    Then the system lists the document as exception "RETENTION_CLASS_MISSING" in the review list
    Then the document is unchanged

  Scenario: AC8 Second run in the same month
    Given JOB-17 ran on 6 December 2026 and archived 4 documents and listed 9
    When JOB-17 is rerun on 7 December 2026
    Then the system archives no document again, no second "DOCRET" entry is written and the review list still holds 9 rows

  Scenario: AC9 Invalid retention class load
    Given a load file for table "RETENTION_CLASS" with class "TEMP01M" at period 0 months and end action "DELETE"
    When the reference data administrator loads it
    Then the system refuses the load in full with MSG-P3-027 naming both errors
    Then version "RET-2026.11" stays in force

  Scenario: AC10 Expiry on the run date
    Given an appraisal report of class "GENERAL05Y" stored on 6 December 2021
    When JOB-17 runs on 6 December 2026
    Then the system archives the document , because its expiry date equals the run date
```

## Comments (2)

### Comment 1: Nate Trakarntanasuk, 2026-11-18T16:10:55.420+0700

Comment ID 1797149

h3. Clarification needed: JOB-17 is specified twice, as two unrelated jobs

Both RWB-E1-017 and RWB-E1-041 independently define a monthly Quartz job named "JOB-17" ({{RetentionJob}} in each spec), but they are *not* the same job:

* RWB-E1-017's JOB-17 archives rows in data-store tables ({{interaction}}, etc.) via the {{retention_rule}} table — module P1.
* RWB-E1-041's JOB-17 archives/lists *document blobs* via a separate {{retention_class}}/{{retention_action}} table — module P5.

Each spec lists its own {{RetentionJob}} under "New Nodes Required," not as an extension of an existing one, and neither spec references the other. This isn't a case of one story laying the groundwork and the other adding to it later — they're two independently-designed jobs that happened to pick the same number.

If both are implemented as currently specified, the job catalog, run book, alerts, and {{GET /admin/jobs?type=JOB-17}} would all have two unrelated jobs reporting under the same identifier, regardless of which one is built first.

Can we confirm: these are intended to be two separate jobs, and one of them needs a different job number (e.g. JOB-18) before either goes to implementation? If so, which one keeps "JOB-17"?

### Comment 2: Nate Trakarntanasuk, 2026-11-18T16:14:20.434+0700

Comment ID 1797158

h3. Clarification needed: who builds {{CaseDirectory}}?

This story's legal-hold exclusion (BR4) depends on {{CaseDirectory}} (P3), but no story in the backlog claims to build it. It's actually a wider gap — at least 8 other stories (RWB-E1-024, 026, 032, 033, 040, 049, 054) depend on the same interface, none of which builds it either. Recommend raising this once at the epic level rather than per-card, but flagging here since this story is one of its consumers.

Which card actually delivers {{CaseDirectory}}?


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
