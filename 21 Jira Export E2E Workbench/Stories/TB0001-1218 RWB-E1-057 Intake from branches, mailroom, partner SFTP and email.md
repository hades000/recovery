# TB0001-1218 [RWB-E1-057] Intake from branches, mailroom, partner SFTP and email

| Field | Value |
|---|---|
| Jira | [TB0001-1218](https://scbjira.atlassian.net/browse/TB0001-1218) |
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
| Created | 2026-11-05T12:37:52.640+0700 |
| Updated | 2026-11-18T17:23:00.376+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a case owner, I want scans from branch scanners and the mailroom, partner files by SFTP and attachments from the recovery mailboxes to enter the same OCR intake with the source recorded, so that every document path ends in the document hub.

## Acceptance criteria

```gherkin
Feature: Intake from branches, mailroom, partner SFTP and email

  Background:
    Given JOB-12 Document intake runs every 15 minutes from 08:00 to 18:00 Asia/Bangkok on working days
    Given INTAKE_ALLOWED_TYPES is PDF, JPG and PNG and INTAKE_MAX_FILE_MB is 25
    Given partner "LF-007" is a law firm with panel_status "ACTIVE"

  Scenario: AC1 Branch scan
    Given file "scan-0001.pdf" of 1.2 MB in the scanner folder of branch "BR-0123", created by the scanner at 2026-11-30 09:12
    When the intake job runs at 09:15
    Then one document_intake row has source "SCAN", channel_code "BR-0123", captured_at 2026-11-30 09:12 and an empty scan_result
    Then the file is in the intake container at the row's intake_ref
    Then the file is no longer in the scanner folder and is in its processed folder

  Scenario: AC2 Partner SFTP
    Given file "LF-007-notice-0001.pdf" in the SFTP inbound subfolder "LF-007"
    When the job runs
    Then one document_intake row has source "PARTNER", channel_code "LF-007" and partner_id of partner "LF-007"

  Scenario: AC3 Mailbox
    Given an email to recovery mailbox "MBX-RECOVERY-01" with one PDF attachment "reply-0001.pdf"
    When the job runs
    Then one document_intake row has source "EMAIL", channel_code "MBX-RECOVERY-01" and the sender address recorded
    Then the system masks the sender address in every response and absent from the job record and the logs
    Then the email is in the archive folder of "MBX-RECOVERY-01"

  Scenario: AC4 Mailroom scan
    Given file "mailroom-0001.pdf" in the mailroom folder
    When the job runs
    Then one document_intake row has source "SCAN" and channel_code "MAILROOM"

  Scenario: AC5 A file type not allowed is refused
    Given file "letter-0002.docx" in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system writes no document_intake row for it
    Then the file is in the rejected folder of branch "BR-0123"
    Then the job record shows 1 refused on "BR-0123" with MSG-P5-007 and reason MSG-P5-001

  Scenario: AC6 A file above the size limit is refused
    Given file "scan-0003.pdf" of 25.1 MB and file "scan-0004.pdf" of 25.0 MB in the scanner folder of branch "BR-0123"
    When the job runs
    Then the system refuses "scan-0003.pdf" with reason MSG-P5-017 and moved to the rejected folder
    Then "scan-0004.pdf" has a document_intake row

  Scenario: AC7 An unknown or suspended partner is refused
    Given file "notice-0005.pdf" in the SFTP subfolder "LF-099", which is no partner_code
    Given file "notice-0006.pdf" in the SFTP subfolder "LF-008", a partner with panel_status "SUSPENDED"
    When the job runs
    Then the system writes no document_intake row for either file
    Then the job record shows MSG-P5-007 with reasons "PARTNER_UNKNOWN" and "PARTNER_NOT_ACTIVE"

  Scenario: AC8 A duplicate file is not taken in twice
    Given file "scan-0001.pdf" with hash "H1" from branch "BR-0123" was taken in on 30 November
    When the same file arrives again from branch "BR-0123" on 2 December
    Then the system writes no second document_intake row
    Then the system moves the file to the processed folder and counted as a duplicate

  Scenario: AC9 An empty run
    Given no new file or email on any channel
    When the job runs
    Then the job record shows intakeStep complete with 0 items on each channel

  Scenario: AC10 The intake container does not accept writes
    Given the intake container refuses writes
    When the job runs with file "scan-0007.pdf" in the folder of branch "BR-0123"
    Then the system writes no document_intake row
    Then "scan-0007.pdf" stays in the scanner folder
    Then on the next run with the container available the file is taken in

  Scenario: AC11 Two failed runs raise an alert
    Given the run at 10:00 failed because the SFTP inbound folder could not be read
    When the run at 10:15 fails for the same reason
    Then the platform administrator receives MSG-P5-008 naming "PARTNER_SFTP"
    Then the run at 10:30 tries again

  Scenario: AC12 The job runs once across two instances
    Given two service instances are running
    When the 09:15 run is due
    Then the system records one run for 09:15
    Then each file has one document_intake row

  Scenario: AC13 An email with no usable attachment
    Given an email to "MBX-RECOVERY-01" with no attachment
    Given an email with only a 6 KB signature image
    When the job runs
    Then the system writes no document_intake row for either email
    Then both emails are in the archive folder

  Scenario: AC14 A file seen again after a failed move
    Given file "scan-0008.pdf" was taken in at 11:00 and the move to the processed folder failed
    When the run at 11:15 sees "scan-0008.pdf" again
    Then the system writes no second document_intake row
    Then the system moves the file to the processed folder

  Scenario: AC15 Outside business hours
    Given the time is 18:15 on a working day
    When the scheduler checks JOB-12
    Then no run starts until 08:00 the next working day

  Scenario: AC16 An item taken in is scanned before OCR
    Given file "scan-0009.pdf" was taken in by intakeStep with an empty scan_result
    When ocrStep runs in the same job before scanStep has set scan_result
    Then ocrStep does not read "scan-0009.pdf"
    Then after scanStep sets scan_result "CLEAN" ocrStep reads it
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
