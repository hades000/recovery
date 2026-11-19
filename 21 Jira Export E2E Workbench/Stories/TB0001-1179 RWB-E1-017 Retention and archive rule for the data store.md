# TB0001-1179 [RWB-E1-017] Retention and archive rule for the data store

| Field | Value |
|---|---|
| Jira | [TB0001-1179](https://scbjira.atlassian.net/browse/TB0001-1179) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Decision, R-Dependency, R-Environment, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:18.695+0700 |
| Updated | 2026-11-18T16:57:26.513+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 4 |
| Comments | 3 |

## Description

As a Compliance and PDPA officer (RW-COMPLY), I want a retention rule per data product and table, held as reference data, applied by a job that archives rows past their rule and logs the action, so that the store holds what the policy allows and nothing older.

## Acceptance criteria

```gherkin
Feature: Retention and archive rule for the data store

  Background:
    Given retention rule version "RET-2026.11" holds product "DP05", table "interaction", age basis "occurred_at", 24 months
    Given the run date is Sunday 2026-12-06

  Scenario: AC1 Retention rule applied
    Given 1,250 interaction rows with occurred_at before 2024-12-06 and 4,800 rows from 2024-12-06 onward
    When JOB-17 runs
    Then 1,250 rows move to the archive container under "retention/2026-12-06/interaction/"
    Then the 1,250 rows are no longer in the live interaction table
    Then the job run logs count 1,250 for DP05 interaction under rule version "RET-2026.11"

  Scenario: AC2 Rule changed as data
    Given retention rule version "RET-2027.01" changes DP05 interaction to 36 months, approved and valid from 2027-01-01
    Given interaction rows with occurred_at on 2024-01-15 and on 2023-12-20
    When JOB-17 runs on Sunday 2027-01-03
    Then the row from 2024-01-15 stays in the live table
    Then the row from 2023-12-20 moves to the archive container
    Then the job run logs rule version "RET-2027.01"

  Scenario: AC3 Legal hold
    Given case "RW-2024-000311" is marked legal hold and has 40 interaction rows older than 24 months
    When JOB-17 runs
    Then the system keeps its 40 rows in the live table
    Then the hold report lists case "RW-2024-000311" with 40 rows kept
    Then the summary alert to Compliance reads MSG-P1-020 with 1 case on legal hold kept

  Scenario: AC4 A rule with months outside the allowed range
    Given a retention load version "RET-2026.12" with a row for DP05 interaction at 0 months
    When the load is validated
    Then the system refuses the load in full with MSG-GEN-002 for field "retention_months" between 1 and 600
    Then version "RET-2026.11" stays in force

  Scenario: AC5 The archive write fails
    Given the archive container refuses writes
    When JOB-17 runs
    Then the system deletes no interaction row
    Then the job run ends "FAILED" with MSG-GEN-006 for system "Archive container"

  Scenario: AC6 A repeat run in the same month
    Given JOB-17 archived 1,250 rows on 2026-12-06
    When JOB-17 is rerun on 2026-12-06
    Then the system archives 0 rows
    Then the archive container still holds one set of the 1,250 rows

  Scenario: AC7 A row exactly at its retention age
    Given an interaction row with occurred_at 2024-12-06T00:00+07:00
    When JOB-17 runs on 2026-12-06
    Then the row stays in the live table

  Scenario: AC8 A rule for the decision log is refused
    Given a retention load version "RET-2026.12" with a row for product "DP12", table "decision_log_entry"
    When the load is validated
    Then the system refuses the load in full with MSG-P1-002 and check "decision_log_entry is not archived by the retention job"

  Scenario: AC9 A rerun while the job is running
    Given JOB-17 is running
    When a platform administrator posts a rerun of JOB-17
    Then the system refuses the rerun with status 409 and MSG-P2-006
```

## Comments (3)

### Comment 1: THAMMASAK JUKCHAN, 2026-11-17T16:00:11.893+0700

Comment ID 1795036

*Dev review — RWB-E1-017 Retention and archive rule for the data store*
Source: v14 set (User Stories Epic 1 v7, Build Notes v4, Physical Schema v4, Build Order v1, Decision Log v8)

{quote}*⚠️ Top blockers — need answer before build*

# *No archive container.* TE-012 creates only rwb-intake, rwb-docs, rwb-docs-legal, rwb-quarantine — no write-once archive container. Which container name, who creates it? _(PO-88)_
# *retention_rule DDL ≠ Schema v4.* §13 says "created in this story", but schema v4 already has the table with different columns and unique key. Which is source of truth?
# *LAKE_COPY row refused.* Loader refuses any rule on {{decision_log_entry}} (AC8/BR5), but RWB-E1-014 needs DP12 / decision_log_entry / LAKE_COPY → it can never load. _(PO-86)_{quote}

*Questions*

# *Archive container (AC1, AC5)* — name, owner (TE-012 template?), write-once/immutable policy, and SY-DATALOAD write access per environment? _(PO-88)_
# *retention_rule DDL (§11, §13)* — story: {{product_code varchar(4)}}, unique (product_code, table_name, record_class, rule_version). Schema v4: {{varchar(25)}}, unique (table_name, record_class, rule_version), plus {{end_action DEFAULT 'ARCHIVE'}} and {{reference_version_id}} not in the story; §11 skips DF-REF-122. Should our migration create or only alter the table? _(PO-76 / PO-29)_
# *Table owner* — RWB-E1-041 §11 also says it creates {{retention_rule}} (its §13 uses {{retention_class}}). One table + one JOB-17 with two steps, owned by E1-017? _(PO-108)_
# *Decision log exemption (AC8, BR5)* — can the loader refuse {{decision_log_entry}} only for live-store record classes and allow {{LAKE_COPY}}? _(PO-86)_
# *CaseHoldQuery (AC3)* — which story builds P3 {{CaseHoldQuery.casesOnLegalHold()}} / {{caseNumbers()}}? No Epic 1 story sets {{legal_hold}}. How do we seed RW-2024-000311 for the test? _(PO-87)_
# *Rerun (AC6, AC9)* — §12 allows rerun only for a *failed* JOB-17, but AC6 reruns a successful run. Allowed (idempotent per run date + rule version)? Will a second manifest on the same write-once path be rejected? 409 while running = MSG-P2-006? (E1-003 uses MSG-P1-011 on the same endpoint.) _(PO-85)_
# *Retention values (AC1)* — DP05 interaction 24 months from {{occurred_at}} is assumed. Compliance to confirm per data product. _(DL26 / PO-27 — overdue since 13 Nov)_
# *Ledger purge* — audit/environment docs say ledger is insert-only; this story's migration lets DELETE pass {{refuse_change()}} when {{recovery.retention_purge='on'}}. Is purging interaction rows approved? Who owns {{refuse_change()}} — E1-066 (#46) owns the interaction append-only rule. _(CTX-BE-CONFLICT-005)_
# *Build order* — "Done when" needs E1-056 run book (#23); Quartz/rerun from TE-007 (#26). Both after this story (#22). Add E1-056 to Depends on and move after #23, or build against stubs?
# *Story fix* — §16 has TC-E1-017-10 but §18 traces only TC-01..09. Please add TC-10 to §18.

*We can start now:* RetentionRuleLoader validation, "strictly older" row selector, ArchiveWriter with manifest + SHA-256 read-back — tested on Azurite with stub {{CaseHoldQuery}} while the above is open.

### Comment 2: Nate Trakarntanasuk, 2026-11-17T16:07:25.930+0700

Comment ID 1795060

*Dependency and scope questions for grooming*

{quote}# {{CaseHoldQuery}} (the P3 interface this story's legal-hold exclusion depends on — {{casesOnLegalHold()}} / {{caseNumbers()}}) has no owning story anywhere in the current backlog that I can find. Which card is expected to deliver it, and is it even planned yet?
# Similarly, *the job endpoints this story reuses for reading the run and for a manual rerun* have a fully specified contract at the architecture level, but no story currently claims to build the underlying implementation — every story that uses them (this one included) treats them as already existing. Which card actually delivers these first?
# *Job numbering*: this story's monthly retention job is JOB-17. A separate, unrelated story (document retention/virus-scan intake) also names its own job JOB-17 (*RWB-E1-041*), for a completely different purpose. These look like two independently-specified jobs that collided on the same number — can we confirm which one should actually be JOB-17 and whether the other needs renumbering?
# *Shared-table behavior change*: this story changes {{interaction}}'s delete-refusal trigger from unconditional to conditional (gated by a runtime flag). Has this been checked against any other module/story that might assume deletes on {{interaction}} are always refused?{quote}

### Comment 3: NAMTIP WONGSOMBOON, 2026-11-18T11:53:18.181+0700, edited 2026-11-18T12:09:27.299+0700

Comment ID 1796334

Ref: Grooming Session – Room 2 with Henka , {{2026-11-18}}
Quartz is not used in the E2E Workbench project. Apache Airflow is used instead.
AC9 A rerun while the job is running → The test results will be recorded as Unit Test results.


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
