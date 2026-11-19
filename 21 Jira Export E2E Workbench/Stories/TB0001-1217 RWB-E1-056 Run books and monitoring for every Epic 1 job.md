# TB0001-1217 [RWB-E1-056] Run books and monitoring for every Epic 1 job

| Field | Value |
|---|---|
| Jira | [TB0001-1217](https://scbjira.atlassian.net/browse/TB0001-1217) |
| Type | Story |
| Status | To Do |
| Resolution | - |
| Parent | TB0001-1162 |
| Epic link | TB0001-1162 |
| Assignee | CHANISSARA MAHAKITTIKUN |
| Reporter | KRISSADA RONGRAT |
| Priority | Medium |
| Labels | DEV-Reviewed, QA-Reviewed, R-Spec |
| Components | E2E Workbench |
| Fix versions | - |
| Affects versions | - |
| Sprint | Design - Grooming |
| Team | RWB_SQ1 |
| Created | 2026-11-05T12:37:51.821+0700 |
| Updated | 2026-11-18T20:18:53.368+0700 |
| Due date | - |
| Resolved | - |
| Original estimate | - |
| Remaining estimate | - |
| Time spent | - |
| Votes | 0 |
| Watchers | 5 |
| Comments | 3 |

## Description

As a platform administrator (RW-PLATADM), I want a run book for every scheduled job (purpose, schedule, owner, failure signs, restart steps, escalation) and monitoring of each job's last run, status and duration, so that the operations team can restart any Epic 1 job without the developer.

## Acceptance criteria

```gherkin
Feature: Run books and monitoring for every Epic 1 job

  Background:
    Given job_catalog holds 13 rows with first release "E1"

  Scenario: AC1 Run book present
    Given the list of Epic 1 jobs and services in job_catalog
    When RunbookCompletenessTest runs in the pipeline
    Then each of the 13 jobs has a file in docs/operations/runbooks
    Then each file has the sections purpose, schedule, owner, failure signs, restart steps and escalation

  Scenario: AC2 Restart by run book
    Given JOB-01 failed at 05:20 on business date 2026-11-26 while it loaded the EFS data for "INT-07"
    When a platform administrator follows the restart steps and calls POST /admin/jobs/{jobId}/rerun at 06:05
    Then JOB-01 restarts from its failed step and ends with status "COMPLETED" at 06:25
    Then JOB-02 runs after JOB-01 and the case list shows cases with data as of 2026-11-26
    Then the system records no developer action in the run

  Scenario: AC3 Monitoring in place
    Given every job in job_catalog ran at least once in SIT
    When the platform administrator opens the workbook "Recovery jobs"
    Then each of the 13 jobs shows its last run time, status and duration
    Then GET /admin/jobs returns the same last run, status, startedAt and endedAt for each job

  Scenario: AC4 Missing run book blocks the build
    Given a developer adds a Quartz job "JOB-12" with a run book that has no "Escalation" section
    When the pipeline runs
    Then the build fails with message MSG-P2-005 naming job "JOB-12" and section "Escalation"

  Scenario: AC5 Rerun while running refused
    Given JOB-03 started at 06:40 and is running
    When a platform administrator calls POST /admin/jobs/{jobId}/rerun for JOB-03 at 06:45
    Then the response is 409 with message MSG-P2-006
    Then JOB-03 continues its run

  Scenario: AC6 Job running past its threshold
    Given JOB-02 has an alert threshold of 45 minutes (assumed; DL11)
    When JOB-02 has run for 46 minutes on business date 2026-11-27
    Then the data steward group and the platform administrator group receive message MSG-P2-004
    Then the system does not stop JOB-02

  Scenario: AC7 Rerun of a completed job changes nothing
    Given JOB-01 completed for business date 2026-11-28
    When a platform administrator reruns it for the same date
    Then each interface run for that date is written as "DUPLICATE"
    Then the system loads no account record a second time
```

## Comments (3)

### Comment 1: NATAPATCHARA ANUROJE, 2026-11-17T01:39:05.583+0700, edited 2026-11-17T09:17:47.496+0700

Comment ID 1793629

Read through the story content itself  looking for gaps that would need a client answer

* *How does a held job actually resume?* AC8 says when the EFS batch completes at 08:40, "the daily gate returns COMPLETE and JOB-04 starts for 2026-12-01" the same day. But nothing says *how* — is this event-driven (something listens for the batch-complete event and kicks JOB-04 off immediately), or does JOB-04 only get re-evaluated at its next normal Quartz trigger? If it's the latter, a job scheduled once daily wouldn't actually resume same-day at 08:40 as the AC implies.
* *Scope of RunbookCompletenessTest's Quartz scan* — does it scan every {{JobDetail}} registered in the whole ACE service (which also runs the collection and common modules' own jobs), or only jobs inside the recovery module? If it's service-wide, every other squad's scheduled job would also need an 8-section run book in this story's exact format — that's a cross-squad impact not mentioned anywhere in this story or its Out of Scope section.
* *CHK-01's nature is inconsistent* — the Background/job_catalog treats it as a scheduled catalog row like the other 15 (with {{schedule_text}}, {{alert_after_minutes}}, etc.), but AC9 describes it purely as a pipeline/build-time gate ("the merge is blocked"). If it's build-time only, which catalog fields genuinely apply to it — does it even have a Quartz schedule and an alert threshold, or just a run book?

Separately, on dependencies (not a content gap, just worth tracking): this story needs RWB-E1-007, RWB-E1-015 and RWB-E1-069, none of which has a current spec; RWB-E1-007 specifically is still Block/R-Decision/R-Requirement/R-Spec with ~20 open items that could affect which jobs end up in this story's catalog. And on provisioning: the {{RWB-<env>-RW-PLATADM}} Entra ID group this story's role checks rely on doesn't exist yet either — it's created by RWB-E1-022 (Sign-on with SSO/MFA/first roles), also Backlog.

### Comment 2: Ratchadaphorn Kasemphin, 2026-11-17T11:21:22.058+0700

Comment ID 1794173

 @CHANISSARA MAHAKITTIKUN  
cc. @Chitchaya Muanchonchana 
Concerns (Dependencies)

# *Dependencies the story uses but does not list in "Depends on"*
#* *RWB-TE-007* (Quartz and the job run log): Flow step 5 and {{GET /admin/jobs}} read the last run from the P1 job run log.
#* *RWB-E1-001* (V0001 creates {{job_catalog}}): the V0004 seed cannot run without it.
#* *RWB-E1-043* (dictionary load): the CHK-01 run book gives it as the fix (AC9).
#* *RWB-TE-001*: owns the forbidden-name list in {{recovery-modules.yaml}}.
#* *RWB-E1-070 and RWB-E2-037*: own the Temporal server and worker run books, per the Change Register.
# *Job bodies come from other stories.* JOB-02 to JOB-17 and AGT-01 are each built in their own story. Any job not built yet needs a stub, or AC1 and AC3 ("ran at least once in SIT") cannot pass.
# *New Quartz jobs from the Temporal and Drools adoption are not in the 16 catalog rows.*
#* Examples: {{RulePackageEffectiveDateJob}} (RWB-E1-073, runs at 00:01), {{PlatformSmokeWorkflow}} and {{StuckWorkflowScanner}}.
#* If {{RunbookCompletenessTest}} checks every Quartz JobDetail in the recovery module, these jobs will fail the build unless they are added to the catalog.
# *Related documents are out of sync with the story.*
#* FSD P7 v3 (AC-P7-014) and Test Cases v7 still use *13 jobs* and JOB-01, and use JOB-12 in AC4. The story uses 16 rows and JOB-20.
#* TC-E1-056-05 uses JOB-03; the story uses JOB-04.
#* The dates in TC-06 do not match the story.
#* The story's module is P2 Integration, but the FSD places the ACs under P7.
# *ACE and Azure infrastructure outside the squad:* the Log Analytics workspace, the alert rule setup, and RW-PLATADM access to the workbook.

----

h2. Clarification needed

h3. A. Business perspective

# *Who is the "operations team" in Production?* SCB IT Ops (L1/L2), the ACE platform team?
#* Who holds RW-PLATADM in PROD?
#* Should run books be in Thai, English or both?
# *What should job owners without rerun rights do when alerted?* Team manager (JOB-03, JOB-06), Credit administration (JOB-07, JOB-08) and Compliance (JOB-14, JOB-17) receive alerts but cannot rerun. The escalation path needs to say who they notify and what they decide.
# *Who owns JOB-05 (Timer check)?* BR3 does not name a role.
# *What is the cut-off for the morning allocation?* If an ACE batch is late, how long do we wait? After the cut-off, do we run on the previous day's data with a stale marker, or keep waiting?
# *What is the restart SLA or RTO?* For example, the case list must be ready by 08:00 for collectors. Is that time also the escalation trigger?
# *What happens on a mid-day rerun?* If JOB-02 or JOB-03 is rerun during business hours, does it re-allocate over work collectors have already started?
# *What if ACE restates data after a job has COMPLETED?* AC7 refuses every rerun. Does the business need a controlled force-rerun path with approval?
# *WAITING has no timeout.* If the ACE batch never arrives that day, does the next day skip that date (SKIPPED) or catch up?
# *Alert thresholds:* please confirm the DL11 assumption (1.5 × expected duration; JOB-02 = 45 minutes) and the expected duration of each job.
# *Alert channels:* email only, or also Teams, SMS or on-call paging? Are out-of-hours alerts needed? Many jobs run between 05:00 and 06:30.
# *Which sources must show the "last complete ACE business date per source"?* ALS, EFS and which others? Please give the full list.

h3. B. AC details

# *AC1 / BR1, catalog scope:* should {{RulePackageEffectiveDateJob}} and the other Temporal-adoption Quartz jobs be added to the 16 rows? What is the final count?
# *AC1 / X2, forbidden names:*
#* What words or patterns does the forbidden-name list in {{recovery-modules.yaml}} (RWB-TE-001) contain? Is the check an exact match or a pattern?
#* In section 5 Exception paths, X2 gives a raw build log text instead of a MSG ID. X1, which is also a pipeline error, uses MSG-P2-005. Should X2 get its own MSG ID, and should AC1 assert the error message?
# *AC2, root cause of the failure:* JOB-02 fails because {{v_ace_account}} has no row for an account at 90 DPD. If ACE has not fixed the data, a rerun will fail again. The restart steps must say what to do with that account: skip it, raise an exception, or wait for an ACE fix.
# *AC2, restart from the failed step:*
#* What are JOB-02's steps or checkpoints?
#* The asserted end time of 06:20 cannot be tested deterministically. Replace it with a condition that can be measured.
# *AC2, "the run records no developer action":* how is this measured? For example: the audit shows only RW-PLATADM as the actor.
# *AC2, chain after a rerun:* does "JOB-03 runs after JOB-02" mean the system triggers downstream jobs automatically, or must the admin rerun each one by hand?
# *AC3, AGT-01:* AGT-01 is a continuously running service.
#* What do last run, duration and status mean for it? Should it use a heartbeat instead?
#* Can AGT-01 be rerun through the endpoint?
# *AC3, data consistency:* within what latency must the workbook and {{GET /admin/jobs}} show the "same" data, given the Log Analytics ingestion delay?
# *AC5 / AC7 / Contract,* {{{jobId}}}: the {{{jobId}}} path parameter is the failed execution ID, not the job ID (JOB-04). The AC says "rerun for JOB-04". These need to be aligned.
# *AC6, alert recipients:* the AC hard-codes the "data steward group". It should say "the owner role in {{job_catalog}}".
# *AC6 / MSG-P2-004, message text:* the text says "{job} failed at…". That is wrong for a job still running past its threshold, so it needs its own message.
# *AC6, repeat alerts:* do alerts repeat while the job stays over its threshold? JOB-05 runs every 5 minutes, so it needs dedup to avoid an alert flood.
# *No AC for the FAILED alert:* Flow step 7 alerts on FAILED, but no AC covers it.
# *AC7, MSG-GEN-004:* "Someone else changed this record…" does not fit the rerun of a completed job. A dedicated message is needed.
# *AC8, what JOB-04 does:*
#* The AC says "the case list step of JOB-04", but JOB-04 is reconciliation; the case list is JOB-02.
#* Does JOB-04 actually read EFS (DP05 Contact and Promises)?
#* AC7 asserts both {{case_list_row}} and {{reconciliation_result}} for JOB-04. Please confirm JOB-04's scope.
# *AC8, wording:* "marks DP05 Contact and promises 'STALE'" needs clearer wording.
# *AC8, "resolved" alert:* should a "resolved" alert be sent once the batch completes?
# *SKIPPED state:* section 9 lists it, but no AC says when it occurs.
# *Feature flag* {{rwb.integration.job-monitoring}}: what stops working when it is OFF: events, alerts, endpoints, the pipeline test?
# *Data section:* it says "DF-OPS-224 to 232, all 9 fields" but does not list {{job_id}} or each of the remaining fields.

### Comment 3: Chanapai Gingpuwaluck, 2026-11-17T12:14:41.238+0700

Comment ID 1794346

These points add to the questions already on this card.

# *Monitoring tool.* The story and the alert set-up use Log Analytics, but the TechX target uses CELK (feedback #77). Please decide before the workbook and alert rules are built.
# *How the job catalog is loaded.* {{job_catalog}} is seeded by migration V0004, while BR8 calls it data.
#* Question: should it be loaded through the reference data service instead? Then a new job or a changed owner needs no migration. This also removes the conflict with "one migration per story".
# *Job owners in Thai and English.* The weekly report and the alerts go to business owners. Please confirm the language of alert text as well as of run books, because MSG-P2-004 has no Thai text in the story.

Who answers: Ops, Solution architect, ACE team.


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
