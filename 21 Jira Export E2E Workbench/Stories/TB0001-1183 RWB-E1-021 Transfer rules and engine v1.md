# TB0001-1183 [RWB-E1-021] Transfer rules and engine v1

| Field | Value |
|---|---|
| Jira | [TB0001-1183](https://scbjira.atlassian.net/browse/TB0001-1183) |
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
| Created | 2026-11-05T12:37:22.422+0700 |
| Updated | 2026-11-17T21:34:56.046+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a team manager (RW-TEAMMGR), I want cases moved between queues and roles by the transfer rule table on stage change, route decided, timer expired, deviation raised or cleared, approval needed, document received, payment missed, or a manual request with a reason, so that hand-offs between teams run without email.

## Acceptance criteria

```gherkin
Feature: Transfer rules and engine v1

  Background:
    Given the transfer rows version "TRF-2026.11" are in force
    Given queue "LIT-BKK-OFF" belongs to team "LIT-BKK" and role RW-LITOFF with method "LOWEST_LOAD" and cap 150

  Scenario: AC1 Rule-driven transfer
    Given case RW-2026-000301 is "IN_PROGRESS" in queue "TDR-BKK-CO" with owner U-21
    Given transfer row "TRF-007" moves a case to queue "LIT-BKK-OFF" when ROUTE_APPROVED carries route "R4"
    When the route decision approves route "R4" for the case
    Then the case is in queue "LIT-BKK-OFF" with owner U-31, the member with the lowest load
    Then the assignment of U-21 has an end time and a new assignment has reason "TRANSFER" and rule ID "TRF-007"
    Then the decision log entry carries rule ID "TRF-007" and rule version "TRF-2026.11"

  Scenario: AC2 Manual transfer
    Given a team manager of team "TDR-BKK"
    When they call the transfer endpoint for case RW-2026-000302 with reason code "MANUAL", transfer reason "R03" and target owner U-22
    Then the case owner is U-22
    Then the assignment and the decision log entry carry transfer reason "R03"

  Scenario: AC3 One queue only
    Given case RW-2026-000303 is in queue "TDR-BKK-CO" with record version 7
    When a rule transfer to "LIT-BKK-OFF" and a manual transfer to "DIL-BKK-CO" arrive in the same second
    Then the case ends in exactly one queue
    Then the system refuses the second transfer with MSG-GEN-004
    Then a decision log entry records the second transfer with final call "TRANSFER_REJECTED"

  Scenario Outline: AC4 Eight triggers
    Given transfer row "<row>" moves a case to queue "<queue>" on trigger "<event>"
    Given case RW-2026-000304 meets the row's condition
    When "<event>" arrives for the case
    Then the case is in queue "<queue>"
    Then the decision log entry carries rule ID "<row>"

    Examples:
      | row     | event              | queue        |
      | TRF-001 | CaseStateChanged   | NPA-BKK-CO   |
      | TRF-002 | ROUTE_APPROVED     | LIT-BKK-OFF  |
      | TRF-003 | TimerDue           | LIT-BKK-OFF  |
      | TRF-004 | DeviationRaised    | DEV-HANDLER  |
      | TRF-005 | DeviationCleared   | TDR-BKK-CO   |
      | TRF-006 | ApprovalRequested  | TDR-BKK-APR  |
      | TRF-008 | DocumentStored     | DIL-BKK-CO   |
      | TRF-009 | PaymentMissed      | TDR-BKK-CO   |

  Scenario: AC5 Admin API
    Given a team manager with Queue and allocation U and a litigation officer with Case record U
    When the team manager reassigns case RW-2026-000305 to U-23 with transfer reason "R04"
    When the litigation officer places a legal hold with reason "Court order" and reference "ORD-2026-0412", then lifts it
    Then the case owner is U-23
    Then the case went to "ON_HOLD" and back to "IN_PROGRESS"
    Then each of the three calls has a decision log entry with its reason

  Scenario: AC6 Manual transfer without a reason
    When a team manager calls the transfer endpoint for case RW-2026-000306 with no transfer reason
    Then the system refuses the call with 422 and MSG-P3-001
    Then the case keeps its queue and owner

  Scenario: AC7 Target owner at the cap
    Given U-24 holds 150 open cases in queue "TDR-BKK-CO"
    When a team manager transfers case RW-2026-000307 to U-24 with transfer reason "R01"
    Then the system refuses the call with 422 and MSG-P3-002 naming U-24

  Scenario: AC8 Closed case
    Given case RW-2026-000308 has status "CLOSED"
    When a team manager transfers it to queue "TDR-BKK-CO"
    Then the system refuses the call with 409 and MSG-P3-005

  Scenario: AC9 Decision log unavailable
    Given the decision log store is unavailable
    When a team manager transfers case RW-2026-000309 with transfer reason "R03"
    Then the system refuses the call with 503 and MSG-P7-003
    Then the case keeps its queue and owner

  Scenario: AC10 Legal hold stops automated transfers
    Given case RW-2026-000310 has legal_hold = true
    When TimerDue arrives and matches row "TRF-003"
    Then the case keeps its queue and owner
    Then the system records the skip on the job log with rule R-UNI-20

  Scenario: AC11 A repeated event
    Given PaymentMissed with event ID "EVT-88120" moved case RW-2026-000311 to "TDR-BKK-CO"
    When PaymentMissed with event ID "EVT-88120" arrives again
    Then the case has one transfer for the event
    Then the system counts the repeat as an idempotency hit

  Scenario: AC12 No owner below the cap in the target queue
    Given every member of "LIT-BKK-OFF" holds 150 open cases
    When row "TRF-007" fires for case RW-2026-000312
    Then the case is in the overflow queue "LIT-BKK-OVF" with no owner
    Then the system tells the team manager of "LIT-BKK" with MSG-P3-011 and count 1

  Scenario: AC13 Hold on a case already on hold
    Given case RW-2026-000313 has status "ON_HOLD" with a legal hold
    When a litigation officer places a legal hold again
    Then the system refuses the call with 409 and MSG-P3-005

  Scenario: AC14 No row matches
    Given no transfer row matches DocumentStored for case RW-2026-000314
    When DocumentStored arrives for the case
    Then the case keeps its queue and owner
    Then the system writes no decision log entry
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
