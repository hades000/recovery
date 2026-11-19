# RWB-E1-056 Run books and monitoring for every Epic 1 job: Jira comments

Fetched from Jira on 18 November 2026 (project TB0001, ticket [TB0001-1217](https://scbjira.atlassian.net/browse/TB0001-1217)). Text is copied as written, with Jira's list markup turned into Markdown lists. Nothing has been changed or answered here.

## Ticket

| Field | Value |
|---|---|
| Key | TB0001-1217 |
| Status | To Do |
| Assignee | Chanissara Mahakittikun |
| Reporter | Krissada Rongrat |
| Parent epic | TB0001-1162 |
| Labels | DEV-Reviewed, QA-Reviewed, R-Spec |
| Created | 5 Nov 2026 12:37 |
| Last updated | 18 Nov 2026 17:05 (no comment was added after 17 Nov 12:14, so this was a field change) |
| Comments | 3 (Jira reports total = 3) |

## Replies

**There are no replies on this ticket.** Jira has no threaded replies on comments. A reply would show up as a further comment, and the ticket has only three, all posted as separate top-level comments. How they relate:

| Comment | Relation |
|---|---|
| 2 (Ratchadaphorn) | Addressed to the assignee (Chanissara) with a cc to a second person. It does not respond to comment 1. |
| 3 (Chanapai) | Opens with "These points add to the questions already on this card", so it adds to comment 2. It is not a reply to a specific question. |
| 1 (Natapatchara) | Stand-alone. Edited by its author on 17 Nov 09:17, after posting. |

Nobody on the story owner side has answered any of the three yet.

## Timeline

| # | Posted | Author | Comment ID | Topic |
|---|---|---|---|---|
| 1 | 17 Nov 2026 01:39 (edited 09:17) | Natapatchara Anuroje | 1793629 | 3 content gaps, dependencies, provisioning |
| 2 | 17 Nov 2026 11:21 | Ratchadaphorn Kasemphin | 1794173 | 5 dependency concerns, 11 business questions, 20 AC detail questions |
| 3 | 17 Nov 2026 12:14 | Chanapai Gingpuwaluck | 1794346 | 3 additions (monitoring tool, catalog loading, language) |

---

## Comment 1: Natapatchara Anuroje

Posted 17 Nov 2026 01:39, edited 17 Nov 2026 09:17. Comment ID 1793629.

Read through the story content itself looking for gaps that would need a client answer.

1. **How does a held job actually resume?** AC8 says when the EFS batch completes at 08:40, "the daily gate returns COMPLETE and JOB-04 starts for 2026-12-01" the same day. But nothing says *how*. Is this event-driven (something listens for the batch-complete event and kicks JOB-04 off immediately), or does JOB-04 only get re-evaluated at its next normal Quartz trigger? If it's the latter, a job scheduled once daily wouldn't actually resume same-day at 08:40 as the AC implies.
2. **Scope of RunbookCompletenessTest's Quartz scan.** Does it scan every `JobDetail` registered in the whole ACE service (which also runs the collection and common modules' own jobs), or only jobs inside the recovery module? If it's service-wide, every other squad's scheduled job would also need an 8-section run book in this story's exact format. That is a cross-squad impact not mentioned anywhere in this story or its Out of Scope section.
3. **CHK-01's nature is inconsistent.** The Background/job_catalog treats it as a scheduled catalog row like the other 15 (with `schedule_text`, `alert_after_minutes`, etc.), but AC9 describes it purely as a pipeline/build-time gate ("the merge is blocked"). If it's build-time only, which catalog fields genuinely apply to it? Does it even have a Quartz schedule and an alert threshold, or just a run book?

Separately, on dependencies (not a content gap, just worth tracking): this story needs RWB-E1-007, RWB-E1-015 and RWB-E1-069, none of which has a current spec. RWB-E1-007 specifically is still Block/R-Decision/R-Requirement/R-Spec with about 20 open items that could affect which jobs end up in this story's catalog. And on provisioning: the `RWB-<env>-RW-PLATADM` Entra ID group this story's role checks rely on doesn't exist yet either. It is created by RWB-E1-022 (Sign-on with SSO/MFA/first roles), also Backlog.

---

## Comment 2: Ratchadaphorn Kasemphin

Posted 17 Nov 2026 11:21. Comment ID 1794173. Addressed to Chanissara Mahakittikun (assignee), with a cc to a second Jira user (account id 634e23a1a04e906250c53a5f; Jira does not show the name).

### Concerns (Dependencies)

1. **Dependencies the story uses but does not list in "Depends on"**
   - **RWB-TE-007** (Quartz and the job run log): Flow step 5 and `GET /admin/jobs` read the last run from the P1 job run log.
   - **RWB-E1-001** (V0001 creates `job_catalog`): the V0004 seed cannot run without it.
   - **RWB-E1-043** (dictionary load): the CHK-01 run book gives it as the fix (AC9).
   - **RWB-TE-001**: owns the forbidden-name list in `recovery-modules.yaml`.
   - **RWB-E1-070 and RWB-E2-037**: own the Temporal server and worker run books, per the Change Register.
2. **Job bodies come from other stories.** JOB-02 to JOB-17 and AGT-01 are each built in their own story. Any job not built yet needs a stub, or AC1 and AC3 ("ran at least once in SIT") cannot pass.
3. **New Quartz jobs from the Temporal and Drools adoption are not in the 16 catalog rows.**
   - Examples: `RulePackageEffectiveDateJob` (RWB-E1-073, runs at 00:01), `PlatformSmokeWorkflow` and `StuckWorkflowScanner`.
   - If `RunbookCompletenessTest` checks every Quartz JobDetail in the recovery module, these jobs will fail the build unless they are added to the catalog.
4. **Related documents are out of sync with the story.**
   - FSD P7 v3 (AC-P7-014) and Test Cases v7 still use **13 jobs** and JOB-01, and use JOB-12 in AC4. The story uses 16 rows and JOB-20.
   - TC-E1-056-05 uses JOB-03; the story uses JOB-04.
   - The dates in TC-06 do not match the story.
   - The story's module is P2 Integration, but the FSD places the ACs under P7.
5. **ACE and Azure infrastructure outside the squad:** the Log Analytics workspace, the alert rule setup, and RW-PLATADM access to the workbook.

### Clarification needed

#### A. Business perspective

1. **Who is the "operations team" in Production?** SCB IT Ops (L1/L2), the ACE platform team?
   - Who holds RW-PLATADM in PROD?
   - Should run books be in Thai, English or both?
2. **What should job owners without rerun rights do when alerted?** Team manager (JOB-03, JOB-06), Credit administration (JOB-07, JOB-08) and Compliance (JOB-14, JOB-17) receive alerts but cannot rerun. The escalation path needs to say who they notify and what they decide.
3. **Who owns JOB-05 (Timer check)?** BR3 does not name a role.
4. **What is the cut-off for the morning allocation?** If an ACE batch is late, how long do we wait? After the cut-off, do we run on the previous day's data with a stale marker, or keep waiting?
5. **What is the restart SLA or RTO?** For example, the case list must be ready by 08:00 for collectors. Is that time also the escalation trigger?
6. **What happens on a mid-day rerun?** If JOB-02 or JOB-03 is rerun during business hours, does it re-allocate over work collectors have already started?
7. **What if ACE restates data after a job has COMPLETED?** AC7 refuses every rerun. Does the business need a controlled force-rerun path with approval?
8. **WAITING has no timeout.** If the ACE batch never arrives that day, does the next day skip that date (SKIPPED) or catch up?
9. **Alert thresholds:** please confirm the DL11 assumption (1.5 × expected duration; JOB-02 = 45 minutes) and the expected duration of each job.
10. **Alert channels:** email only, or also Teams, SMS or on-call paging? Are out-of-hours alerts needed? Many jobs run between 05:00 and 06:30.
11. **Which sources must show the "last complete ACE business date per source"?** ALS, EFS and which others? Please give the full list.

#### B. AC details

1. **AC1 / BR1, catalog scope:** should `RulePackageEffectiveDateJob` and the other Temporal-adoption Quartz jobs be added to the 16 rows? What is the final count?
2. **AC1 / X2, forbidden names:**
   - What words or patterns does the forbidden-name list in `recovery-modules.yaml` (RWB-TE-001) contain? Is the check an exact match or a pattern?
   - In section 5 Exception paths, X2 gives a raw build log text instead of a MSG ID. X1, which is also a pipeline error, uses MSG-P2-005. Should X2 get its own MSG ID, and should AC1 assert the error message?
3. **AC2, root cause of the failure:** JOB-02 fails because `v_ace_account` has no row for an account at 90 DPD. If ACE has not fixed the data, a rerun will fail again. The restart steps must say what to do with that account: skip it, raise an exception, or wait for an ACE fix.
4. **AC2, restart from the failed step:**
   - What are JOB-02's steps or checkpoints?
   - The asserted end time of 06:20 cannot be tested deterministically. Replace it with a condition that can be measured.
5. **AC2, "the run records no developer action":** how is this measured? For example: the audit shows only RW-PLATADM as the actor.
6. **AC2, chain after a rerun:** does "JOB-03 runs after JOB-02" mean the system triggers downstream jobs automatically, or must the admin rerun each one by hand?
7. **AC3, AGT-01:** AGT-01 is a continuously running service.
   - What do last run, duration and status mean for it? Should it use a heartbeat instead?
   - Can AGT-01 be rerun through the endpoint?
8. **AC3, data consistency:** within what latency must the workbook and `GET /admin/jobs` show the "same" data, given the Log Analytics ingestion delay?
9. **AC5 / AC7 / Contract, `{jobId}`:** the `{jobId}` path parameter is the failed execution ID, not the job ID (JOB-04). The AC says "rerun for JOB-04". These need to be aligned.
10. **AC6, alert recipients:** the AC hard-codes the "data steward group". It should say "the owner role in `job_catalog`".
11. **AC6 / MSG-P2-004, message text:** the text says "{job} failed at…". That is wrong for a job still running past its threshold, so it needs its own message.
12. **AC6, repeat alerts:** do alerts repeat while the job stays over its threshold? JOB-05 runs every 5 minutes, so it needs dedup to avoid an alert flood.
13. **No AC for the FAILED alert:** Flow step 7 alerts on FAILED, but no AC covers it.
14. **AC7, MSG-GEN-004:** "Someone else changed this record…" does not fit the rerun of a completed job. A dedicated message is needed.
15. **AC8, what JOB-04 does:**
    - The AC says "the case list step of JOB-04", but JOB-04 is reconciliation; the case list is JOB-02.
    - Does JOB-04 actually read EFS (DP05 Contact and Promises)?
    - AC7 asserts both `case_list_row` and `reconciliation_result` for JOB-04. Please confirm JOB-04's scope.
16. **AC8, wording:** "marks DP05 Contact and promises 'STALE'" needs clearer wording.
17. **AC8, "resolved" alert:** should a "resolved" alert be sent once the batch completes?
18. **SKIPPED state:** section 9 lists it, but no AC says when it occurs.
19. **Feature flag `rwb.integration.job-monitoring`:** what stops working when it is OFF: events, alerts, endpoints, the pipeline test?
20. **Data section:** it says "DF-OPS-224 to 232, all 9 fields" but does not list `job_id` or each of the remaining fields.

---

## Comment 3: Chanapai Gingpuwaluck

Posted 17 Nov 2026 12:14. Comment ID 1794346.

These points add to the questions already on this card.

1. **Monitoring tool.** The story and the alert set-up use Log Analytics, but the TechX target uses CELK (feedback #77). Please decide before the workbook and alert rules are built.
2. **How the job catalog is loaded.** `job_catalog` is seeded by migration V0004, while BR8 calls it data.
   - Question: should it be loaded through the reference data service instead? Then a new job or a changed owner needs no migration. This also removes the conflict with "one migration per story".
3. **Job owners in Thai and English.** The weekly report and the alerts go to business owners. Please confirm the language of alert text as well as of run books, because MSG-P2-004 has no Thai text in the story.

Who answers: Ops, Solution architect, ACE team.

---

## Question count

| Comment | Author | Questions | Other items |
|---|---|---|---|
| 1 | Natapatchara Anuroje | 3 | 1 dependency note, 1 provisioning note |
| 2 | Ratchadaphorn Kasemphin | 11 business + 20 AC detail = 31 | 5 dependency concerns (the 4th covers four document mismatches) |
| 3 | Chanapai Gingpuwaluck | 3 | none |
| | **Total** | **37** | |

These are the questions answered in `19 Jira Open Questions/RWB-E1-056 Open questions and answers.md`.
