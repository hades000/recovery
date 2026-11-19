# TB0001-1190 [RWB-E1-028] Service levels, timers, escalation and prescription dates

| Field | Value |
|---|---|
| Jira | [TB0001-1190](https://scbjira.atlassian.net/browse/TB0001-1190) |
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
| Created | 2026-11-05T12:37:27.873+0700 |
| Updated | 2026-11-17T21:35:34.479+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want a service level per queue and status, a timer on every case, a warning to the owner and a breach raised to the named escalation point by rule, and a prescription date set from the legal periods, so that no case waits past its limit unseen and no legal claim expires unnoticed.

## Acceptance criteria

```gherkin
Feature: Service levels, timers, escalation and prescription dates

  Background:
    Given the SERVICE_LEVEL row for "HIRE_PURCHASE" and "ASSIGNED" is 5 working days with warning percent 80 and escalation role RW-TEAMMGR
    Given the LEGAL_PERIOD row for "HIRE_PURCHASE" is 2 years from the last payment date
    Given 2026-12-05 to 2026-12-07 are not working days in the HOLIDAY table

  Scenario: AC1 Timer starts
    Given hire purchase case RW-2026-000401 is placed in queue "LIT-BKK-OFF" with status "ASSIGNED" at 2026-12-01 09:00
    When the case arrives
    Then a SERVICE_LEVEL timer is RUNNING with expires_at 2026-12-09 09:00 and warn_at 2026-12-08 09:00
    Then GET /cases/{caseId}/timers returns the timer with its due date

  Scenario: AC2 Warning and escalation
    Given the SERVICE_LEVEL timer of case RW-2026-000401 passes warn_at and later expires_at
    When the timer check runs after each point
    Then owner U-31 receives MSG-P3-003 at the warning point
    Then the system raises at expiry the breach to RW-TEAMMGR of team "LIT-BKK" with TimerBreached and escalation level 1
    Then the case keeps queue "LIT-BKK-OFF" and owner U-31
    Then both the warning and the breach have a decision log entry, the breach with rule R-UNI-30

  Scenario: AC3 Prescription date
    Given a new hire purchase case RW-2026-000402 with one account whose last payment date is 2026-03-15
    When the case is created
    Then the prescription date is 2028-03-15
    Then a PRESCRIPTION timer expires on 2028-03-15 with warn_at 2027-09-17
    Then GET /cases/{caseId} shows prescription date 2028-03-15

  Scenario: AC4 No service level for the queue and status
    Given no SERVICE_LEVEL version is in force on 2026-12-01
    When case RW-2026-000403 is placed in queue "NPA-BKK-CO" with status "ASSIGNED" on 2026-12-01
    Then no SERVICE_LEVEL timer starts
    Then the system lists the case on the exception queue with MSG-P3-026 for "service level" and "HIRE_PURCHASE ASSIGNED"

  Scenario: AC5 No legal period for the product
    Given the LEGAL_PERIOD table has no row for "SSME"
    When SSME case RW-2026-000404 is created
    Then the prescription date is empty
    Then the system lists the case on the exception queue with MSG-P3-026 for "legal period" and "SSME"

  Scenario: AC6 No payment ever made
    Given a hire purchase case RW-2026-000405 with an account that has no last payment date and contract date 2025-06-30
    When the case is created
    Then the prescription date is 2027-06-30

  Scenario: AC7 Missed timer check runs
    Given JOB-05 did not run from 10:00 to 10:40 and three timers passed expires_at in that time
    When JOB-05 runs at 10:45
    Then the system raises three breaches , one for each timer

  Scenario: AC8 A breach is raised once
    Given the SERVICE_LEVEL timer of case RW-2026-000406 is EXPIRED with escalation level 1
    When JOB-05 runs again
    Then the system publishes no second TimerBreached for the timer
    Then escalation level stays 1

  Scenario: AC9 Decision log unavailable at a breach
    Given the decision log store is unavailable
    When the SERVICE_LEVEL timer of case RW-2026-000407 passes expires_at
    Then the timer stays RUNNING with escalation level 0
    Then the job record carries MSG-P7-003 for the timer
    Then the system raises the breach by the first run after the store is back

  Scenario: AC10 A deviation pauses the stage clock and not the prescription clock
    Given case RW-2026-000408 has a RUNNING SERVICE_LEVEL timer and a PRESCRIPTION timer
    When DeviationRaised arrives on 2026-12-02 and DeviationCleared on 2026-12-04
    Then the SERVICE_LEVEL timer was PAUSED from 2026-12-02 to 2026-12-04 and its expires_at moved by 2 working days
    Then the PRESCRIPTION timer stayed RUNNING with the same expires_at
    Then the case record shows MSG-P3-004 with the prescription date while the deviation was open

  Scenario: AC11 The warning point on a 5-day service level
    Given a SERVICE_LEVEL timer of 5 working days started on Monday 2026-12-14 at 08:00
    When the timer check runs on Friday 2026-12-18 at 08:05
    Then the system sends the warning MSG-P3-003 once in that run, with end date Monday 2026-12-21
    Then no warning was sent by the run on Friday 2026-12-18 at 07:55
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
