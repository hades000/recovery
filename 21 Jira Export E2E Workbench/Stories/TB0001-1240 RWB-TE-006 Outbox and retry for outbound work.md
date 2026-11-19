# TB0001-1240 [RWB-TE-006] Outbox and retry for outbound work

| Field | Value |
|---|---|
| Jira | [TB0001-1240](https://scbjira.atlassian.net/browse/TB0001-1240) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1234 |
| Epic link | TB0001-1234 |
| Assignee | - |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | - |
| Team | RWB_SQ1 |
| Created | 2026-11-05T16:11:14.224+0700 |
| Updated | 2026-11-17T21:35:53.473+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a squad member (RW-TRIBE), I want every application event and every outbound work request written to an outbox in the same transaction as the change, and delivered to each consumer in order with retry, so that no outbound action is lost when a system or a consumer is down, and nothing is sent for a change that did not commit.

## Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work

  Background:
    Given consumer "win-dispatch" takes work request WIN_DISPATCH, holds the case step and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged, do not hold the case step and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 Sent after commit
    Given a notice approved
    When the transaction commits at 14 December 2026 10:00:00
    Then the outbox holds one WIN_DISPATCH request for case "RW-2026-000601" with one delivery for "win-dispatch"
    Then the header holds the event ID, idempotency key "WIN_DISPATCH:NT-SYN-0601", schema version 1, occurred time and actor
    Then the payload holds notice and case references only, with no name, address or identifier
    Then at the 10:01 run the sender delivers it and "win-dispatch" passes the notice to OutboundFiles.enqueue for the day's WIN file
    Then the delivery has status DELIVERED

  Scenario: AC2 Retry limit
    Given a target down for longer than the retry limit
    When "win-dispatch" fails at 10:01, 10:02, 10:07 and 10:22
    Then the system makes no fifth attempt
    Then the item moves to the exception queue: the "win-dispatch" delivery has status EXCEPTION and attempt count 4
    Then the system raises task RESOLVE_OUTBOX_DELIVERY on case "RW-2026-000601" for role RW-PLATADM
    Then event RETRY_LIMIT_REACHED moves the case to EXCEPTION_QUEUE by R-UNI-36 with one decision log entry

  Scenario: AC3 Nothing is sent for a change that did not commit
    Given the notice approval fails after OutboxWriter.publish and the transaction rolls back
    When the sender runs
    Then no event and no delivery exist for "NT-SYN-0601"

  Scenario: AC4 A retry that succeeds
    Given "win-dispatch" fails at 10:01 and the case moves to RETRY_QUEUE by R-UNI-33
    When the attempt at 10:02 succeeds
    Then the system delivers the delivery status with attempt count 2
    Then event RETRY_SUCCEEDED returns the case to the state it paused in by R-UNI-35

  Scenario: AC5 The same event is written once
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the outbox holds one event with that key
    Then the second transaction receives DuplicateOutboxKeyException and changes nothing

  Scenario: AC6 Two sender instances
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then the system makes each delivery once
    Then the delivery log holds 200 calls

  Scenario: AC7 Order per case and consumer
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the sender runs
    Then the system does not deliver sequence 12 to "ledger" until sequence 11 is DELIVERED

  Scenario: AC8 Consumers are independent
    Given event CaseAllocated for case "RW-2026-000601"
    When "ledger" fails and "reporting-feed" succeeds at 10:01
    Then the system delivers the "reporting-feed" delivery and the "ledger" delivery is RETRYING with next attempt 10:02
    Then the case route state does not change, because "ledger" does not hold the case step

  Scenario: AC9 Sending an exception delivery again
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator sends it again
    Then the response is 200 with message MSG-GEN-005
    Then the delivery status is PENDING with attempt count 0 and due at the next run
    When the platform administrator sends delivery "OBD-SYN-0002" with status DELIVERED again
    Then the response is 409 with message MSG-P2-022

  Scenario: AC10 An event with no case
    Given an event with no case whose only consumer fails 4 times
    When the retries are used
    Then the delivery status is EXCEPTION
    Then the system sends an alert to the platform administrator within 15 minutes
    Then no task and no case event are raised

  Scenario: AC11 Retry settings come from configuration
    Given the retry delays are changed in the configuration service to 2, 10 and 30 minutes at 09:00
    When "ledger" fails at 10:01
    Then the next attempt is due at 10:03
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
