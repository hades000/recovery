# TB0001-1189 [RWB-E1-027] Decision log writer v1

| Field | Value |
|---|---|
| Jira | [TB0001-1189](https://scbjira.atlassian.net/browse/TB0001-1189) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | Chitchaya Muanchonchana |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | - |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Pre-analyze |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:27.155+0700 |
| Updated | 2026-11-18T17:27:46.591+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As the case workflow module (SY-CASEWF), I want one writer that validates and records case created, owner assigned, case transferred and document attached, with the rule ID and version used, in the same transaction as the action, so that the first decision records exist in Epic 1 and no action proceeds without its record.

## Acceptance criteria

```gherkin
Feature: Decision log writer v1

  Background:
    Given the environment is DEV with synthetic data
    Given allocation table version "ALLOC-2026.11" and transfer rule version "TRF-2026.11" are in force

  Scenario: AC1 Record per event
    Given case "RW-2026-000123" is created by JOB-02 and given owner "U-7101" by row "ALLOC-MTG-BKK-01" of "ALLOC-2026.11" in JOB-03
    When the two events are written
    Then two entries exist for the case with final calls "CASE_CREATED" and "OWNER_ASSIGNED"
    Then the second entry carries rule ID "ALLOC-MTG-BKK-01", rule version "ALLOC-2026.11", actor "SY-CASEWF" and an inputs reference
    Then both entries pass the schema check and two DecisionRecorded events are in the outbox

  Scenario: AC2 Schema enforced
    Given a record for case "RW-2026-000123" with final call "CASE_TRANSFERRED" and no rule version, model version or agent version
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "versions"
    Then the writer logs the error with the case ID and the missing field
    Then the system rolls the transfer in the same transaction back

  Scenario: AC3 A rule ID with no rule version is refused
    Given a record with rule ID "R-UNI-14" and an empty rule version
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "ruleVersion"

  Scenario: AC4 A failed write stops the action
    Given the decision log store is unavailable
    When JOB-03 gives case "RW-2026-000124" to owner "U-7102"
    Then the write raises DecisionLogUnavailableException
    Then the case owner stays empty and the case status stays "New"
    Then the system raises an incident to the platform administrator queue

  Scenario: AC5 A repeated event gives one entry
    Given event "EV-7f3a-0001" for document "DOC-2026-0009981" attached to case "RW-2026-000123" was written
    When the same event with idempotency key "EV-7f3a-0001" arrives again
    Then one entry exists for the event
    Then the writer returns the first entry's ID and adds 1 to the repeat count for R-UNI-40

  Scenario: AC6 A write outside a transaction is refused
    Given a caller without an open transaction
    When it calls the writer
    Then the system refuses the call with IllegalTransactionStateException and nothing is written

  Scenario: AC7 An unknown decision code is refused
    Given a record with decision code "D99"
    When it is written
    Then the system refuses it with message MSG-P7-009 naming "decisionCode"
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
