# TB0001-1176 [RWB-E1-014] Decision log copy to the data lake

| Field | Value |
|---|---|
| Jira | [TB0001-1176](https://scbjira.atlassian.net/browse/TB0001-1176) |
| Type | Story |
| Status | In Design - Solution |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | Block, DEV-Reviewed, QA-Reviewed, R-Dependency, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ2 |
| Created | 2026-11-05T12:37:16.299+0700 |
| Updated | 2026-11-18T16:58:19.813+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 3 |
| Comments | 2 |

## Description

As a center of excellence analyst (RW-COE), I want the decision log copied to the data lake each night, with a retention rule applied to the copy, so that reporting reads the log without touching the live log and nothing in the copy is kept longer than its rule.

## Acceptance criteria

```gherkin
Feature: Decision log copy to the data lake

Background:
Given the live decision log holds 12,480 entries with last entry hash "a3f1...09c2"
Given the watermark shows 12,100 entries copied with last hash "77be...41d0"
Given the retention rule for DP12 record class LAKE_COPY is 24 months, rule version "RET-2026.11"

Scenario: AC1 Daily copy
Given 380 entries were written on business date 2026-11-30
When JOB-13 runs at 01:00 on 2026-12-01
Then the partition "business_date=2026-11-30" holds 380 rows
Then the manifest shows cumulative count 12,480 and last hash "a3f1...09c2"
Then the data lake copy has the same row count and the same last hash as the live log
Then the watermark moves to 12,480 and "a3f1...09c2"

Scenario: AC2 Retention rule
Given lake partitions for business dates 2024-11-29 and 2024-11-30 exist
When the retention step of JOB-13 runs on 2026-12-01
Then the partition "business_date=2024-11-29" and "business_date=2024-11-30" moves to the archive tier
Then the job run records 2 partition archived under rule version "RET-2026.11"

Scenario: AC3 A copy that does not match is not published
Given the lake write for 2026-11-30 stops after 379 of 380 rows
When the reconciliation step compares the copy with the live log
Then the system does not mark the partition complete
Then the watermark stays at 12,100 and "77be...41d0"
Then the job run shows check "REC-08" failed with MSG-P1-019

Scenario: AC4 A repeat run for the same date writes no duplicates
Given JOB-13 completed for 2026-11-30 with 380 rows
When JOB-13 is rerun for 2026-11-30
Then the partition "business_date=2026-11-30" still holds 380 rows
Then the cumulative count stays 12,480

Scenario: AC5 The decision log interface is unavailable
Given DecisionLogExport returns an error for every call
When JOB-13 runs for 2026-11-30
Then the job run ends with status "FAILED" and MSG-GEN-006 for system "Decision log"
Then the watermark and the previous partitions are unchanged

Scenario: AC6 A day with no new decisions
Given no entry was written after "77be...41d0"
When JOB-13 runs for 2026-11-30
Then the partition holds 0 rows and the manifest shows cumulative count 12,100
Then check "REC-08" passes

Scenario: AC7 Two runs at the same time
Given JOB-13 is running for 2026-11-30
When a platform administrator posts a rerun of JOB-13
Then the system refuses the rerun with status 409 and MSG-P2-006
Then one run continues

Scenario: AC8 A partition exactly at its retention age is kept
Given a lake partition for business date 2024-12-01
When the retention step runs on 2026-12-01
Then the partition "business_date=2024-12-01" stays in the copy
```

## Comments (2)

### Comment 1: RACHATAPON PONGANANTAYOTIN, 2026-11-17T16:03:16.624+0700, edited 2026-11-17T16:27:31.609+0700

Comment ID 1795047

Dev question from spec review

# *ACE business date stamp (Build Notes v6, Boundary):* "it now stamps the ACE business date it copies alongside the Workbench sequence." Which field needs to be added in Parquet or the manifest, what should it be named, and where does its value come from given that the story reads solely via {{DecisionLogExport}}?
# *Partition state and archive tier:* The story defines states {{Written}}, {{Complete}}, and {{Archived}} (Section 9, State transitions) but does not specify where they are stored (table, marker file, or manifest), nor how Power BI knows to skip incomplete partitions. Also, does "archive tier" refer to storage access tiers or a separate container (RWB-E1-017 uses a write-once archive container from RWB-TE-012)?
# *Rerun for a date already successfully copied (AC4):* RWB-E1-056 specifies that {{POST /admin/jobs/{jobId}/rerun}} accepts the jobId of a failed execution and returns 409 {{MSG-GEN-004}} if the run is already complete. If a completed date is rerun per AC4, through what channel is it done? Furthermore, once the watermark advances to 12,480, where does a rerun find the "same chain range" (from the manifest first hash or elsewhere)? The story does not specify.
# *LakeRetentionService*: Do we need any implementation for the LAKE_COPY retention, or just load the rule configuration into table and RWB-E1-017 will handle retention ?

### Comment 2: Nate Trakarntanasuk, 2026-11-17T16:18:00.602+0700

Comment ID 1795095

*QA Dependency and scope questions for grooming*

# {{DecisionLogExport}} (the P7 read interface this story depends on — {{head()}} / {{entriesAfter()}} — to read the live decision log without a direct table read) has no owning story in the current backlog that I can find. I checked both decision-log stories (RWB-E1-008, which builds the log store and chain verifier, and RWB-E1-027, which builds the write-side {{DecisionLogWriter}}) — neither lists {{DecisionLogExport}} as something they build. Which card delivers this read interface?
# This story also reuses the job-monitor endpoints for reading the run result and for a manual rerun. Same question as raised on RWB-E1-017: the contract is specified at the architecture level, but no story currently claims to build the implementation — which card delivers it?


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
