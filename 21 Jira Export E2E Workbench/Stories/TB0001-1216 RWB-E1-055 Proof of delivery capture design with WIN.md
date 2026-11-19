# TB0001-1216 [RWB-E1-055] Proof of delivery capture design with WIN

| Field | Value |
|---|---|
| Jira | [TB0001-1216](https://scbjira.atlassian.net/browse/TB0001-1216) |
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
| Created | 2026-11-05T12:37:51.011+0700 |
| Updated | 2026-11-17T10:08:35.005+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a litigation officer (RW-LITOFF), I want generated notices sent to WIN for print and registered mail, with the dispatch and the proof of delivery written back on the notice, so that the case shows what was sent and when it arrived.

## Acceptance criteria

```gherkin
Feature: Proof of delivery capture design with WIN

  Background:
    Given the dispatch-eligible notice states are "GENERATED"
    Given notice "N-0001" for case "RC-2026-000123" is in state "Generated" with notice type "DEMAND" and primary account contract "CT-77001"

  Scenario: AC1 Dispatched
    Given JOB-10 runs at 16:00 on 2026-11-25
    When WIN acknowledges the file with sent date 26112026, barcode "RR123456789TH" and sent type "NPL" for contract "CT-77001"
    Then notice "N-0001" has state "Sent", sent date 2026-11-26 and barcode "RR123456789TH"
    Then the interaction ledger has an outbound "LETTER" entry for case "RC-2026-000123" on 2026-11-26
    Then the system writes noticeDispatched to the outbox with notice "N-0001", barcode "RR123456789TH" and sent date 2026-11-26
    Then the case record shows MSG-P6-004 "DEMAND was sent for registered mail on 26 November 2026."

  Scenario: AC2 Proof of delivery
    Given notice "N-0001" is "Sent" with barcode "RR123456789TH"
    When the INT-15 file of 2026-11-30 holds barcode "RR123456789TH" with call-back date 28112026
    Then notice "N-0001" has state "Delivered", delivery status "DELIVERED" and callback date 2026-11-28
    Then the system writes noticeDelivered to the outbox with delivered date 2026-11-28
    Then case "RC-2026-000123" has a running "NOTICE_PERIOD" timer started on 2026-11-28

  Scenario: AC3 Interface contract agreed with WIN
    Given the sample INT-15 file "WIN-POD-SAMPLE-v1" of 25 records supplied by the WIN owner
    When it is loaded in SIT
    Then it passes checks DQ-085 to DQ-091 with 0 records refused
    Then the job monitor records layout version "WIN-POD-SAMPLE-v1" against INT-15

  Scenario: AC4 File not acknowledged
    Given the WIN file of 2026-11-25 holding "N-0001" is not acknowledged
    When JOB-10 runs on 2026-11-26, 2026-11-27 and 2026-11-28 and none is acknowledged
    Then the system sends "N-0001" in each of the three files and stays "Generated"
    Then after the third failure a task is raised to the litigation officer team with MSG-GEN-006 naming "WIN"

  Scenario: AC5 Proof of delivery file fails a check
    Given an INT-15 file whose trailer says 40 records and whose body holds 39
    When JOB-09 loads it
    Then the system refuses the file in full with MSG-P1-002 naming check "control total"
    Then no notice changes state

  Scenario: AC6 Unknown reference held
    Given an INT-15 file of 30 records where 1 record has barcode "RR000000000TH" and contract "CT-99999" matching no notice
    When JOB-09 loads it
    Then 29 records update their notices
    Then the system holds 1 record on the exception list with check "References"

  Scenario: AC7 Same file loaded twice
    Given the INT-15 file for business date 2026-11-30 has loaded
    When the same file is loaded again
    Then the system refuses it with MSG-P1-002 naming check "business date"

  Scenario: AC8 Repeated dispatch run
    Given JOB-10 has written notice "N-0001" in the file of 2026-11-25
    When JOB-10 is rerun on 2026-11-25 from the job monitor
    Then the second file does not hold "N-0001"

  Scenario: AC9 Barcode missing after three days
    Given notice "N-0002" was in the file of 2026-11-25 and no barcode has returned
    When the daily reconciliation REC-05 runs on 2026-11-28
    Then the system lists "N-0002" as a break for the platform administrator on SCR-45

  Scenario: AC10 Repeated delivery record
    Given notice "N-0001" is "Delivered" with callback date 2026-11-28
    When the INT-15 file of 2026-12-07 repeats barcode "RR123456789TH" with call-back date 28112026
    Then the notice is unchanged
    Then the system writes no second NoticeDelivered
    Then the system counts the repeat under rule R-UNI-40

  Scenario: AC11 Proof of delivery file late
    Given the INT-15 file due on 2026-11-30 has not arrived
    When a litigation officer opens case "RC-2026-000123" on 2026-12-01
    Then the notice section shows MSG-P1-001 naming "DP07 Legal" and 2026-11-23
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
