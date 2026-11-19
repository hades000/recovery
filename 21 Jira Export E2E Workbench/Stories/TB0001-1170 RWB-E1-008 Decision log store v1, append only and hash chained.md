# TB0001-1170 [RWB-E1-008] Decision log store v1, append only and hash chained

| Field | Value |
|---|---|
| Jira | [TB0001-1170](https://scbjira.atlassian.net/browse/TB0001-1170) |
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
| Created | 2026-11-05T12:37:11.077+0700 |
| Updated | 2026-11-18T17:27:37.740+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 1 |
| Comments | 0 |

## Description

As a center of excellence analyst (RW-COE), I want an append-only decision log store holding the seven field groups of every decision, with each entry hashed to the one before it, so that every decision from Epic 1 is recorded once, cannot be changed or deleted, and any change to a stored entry is found by recomputing the chain.

## Acceptance criteria

```gherkin
Feature: Decision log store v1, append only and hash chained

  Background:
    Given the environment is DEV with synthetic data
    Given the decision log store is empty

  Scenario: AC1 Append only
    Given an entry with chain_seq 1 and final call "OWNER_ASSIGNED" is stored for case "RW-2026-000123"
    When an UPDATE setting final_call to "CASE_TRANSFERRED" and a DELETE of the entry are attempted through the ACE service's database role and again through the schema owner role
    Then the system refuses all four statements : by the missing grant for the service role, and with "decision_log_entry is append only" from tr_declog_append_only for the schema owner
    Then the entry is unchanged
    Then the system writes the refused attempts to the ACE audit log with the table, the operation and the entry ID

  Scenario: AC2 Hash chain
    Given 100 entries are appended
    When the chain verifier runs from chain_seq 1 to 100
    Then every entry_hash equals the SHA-256 of the entry's canonical form
    Then every prev_hash equals the entry_hash of the entry before it, and the first prev_hash is 64 zeros
    Then the result holds count 100, last chain_seq 100 and that entry's entry_hash

  Scenario: AC3 Seven field groups
    Given an entry is appended for decision "D6" on case "RW-2026-000123" with rule "R-UNI-14", rule version "UNI-2026.11", inputs reference "inputs/2026-12-03/7f3a", recommendation, approver "U-6101", approval level "L6", final call "APPROVED", actions and outcome
    When it is read with GET /decision-log/{entryId}
    Then the response holds inputsRef, ruleId and ruleVersion, recommendation, approverUserId and approvalLevel, finalCall, actions and outcome
    Then decidedAt, prevHash and entryHash are present

  Scenario: AC4 Hash chain verified daily
    Given the store holds 10,000 entries
    Given the actions of the entry with chain_seq 7,412 were changed in the DEV database with the trigger disabled
    When the chain verifier runs from chain_seq 1 to 10,000
    Then the result names chain_seq 7,412 and its entry ID as the first break
    Then the system raises an incident and MSG-P7-008 is sent to the Compliance group within 15 minutes of the run start

  Scenario: AC5 Two appends at the same moment form one chain
    Given entries up to chain_seq 50 are stored
    When two writers append one entry each in parallel transactions
    Then the entries get chain_seq 51 and 52
    Then the prev_hash of 52 equals the entry_hash of 51, and the prev_hash of 51 equals the entry_hash of 50

  Scenario: AC6 A correction is a new entry
    Given entry "E-1" records owner "U-6102" by mistake
    When a correction entry is appended with corrects_entry_id "E-1" and the right owner "U-6103"
    Then entry "E-1" is unchanged
    Then GET /decision-log for case "RW-2026-000123" returns both entries in chain order with the correction naming "E-1"

  Scenario: AC7 A failed append leaves nothing behind
    Given the database connection for the store is closed in the test double
    When a writer appends an entry inside a transaction that also changes the case owner
    Then the system raises decisionLogUnavailableException
    Then the system stores no entry , the case owner is unchanged and chain_seq is not used

  Scenario: AC8 Reading an entry needs the Decision log right
    Given test user "U-6104" holds only RW-PHONECOL, whose Decision log letter is "-"
    When the user calls GET /decision-log/{entryId}
    Then the system refuses the call with status 403 and message MSG-P4-002
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
