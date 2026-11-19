# RWB-E1-056 Run books and monitoring for every Epic 1 job

| Field | Value |
|---|---|
| Jira | TB0001-1217, component E2E Workbench, status To Do, parent TB0001-1162, labels DEV-Reviewed, QA-Reviewed, R-Spec |
| Jira comments read | 3 (N. Anuroje 17 Nov; R. Kasemphin 17 Nov; C. Gingpuwaluck 17 Nov): about 50 points |
| Story text used | Story Files v7, `RWB E1 056 Run books and monitoring for every Epic 1 job v1.md` (15 Nov; same text in Epic 1 v9) |
| Build order | Build Sequence v6 order 18, Window 2 (16 to 27 Nov), depends on RWB-E1-007 only |
| Prepared | 18 November 2026 |

Status key: **ANSWERED** = a document in the set decides it. **PROPOSED** = the documents imply the answer; the owner should ratify it. **OPEN** = no document decides it; options and a recommendation are given. Gap IDs (G-...) are in `Document Gaps.md`.

## Summary

| Status | Items |
|---|---|
| ANSWERED | Q02, Q04, Q07, Q08, Q10 (SLA), Q16, Q17 (list), Q20, Q23, Q33 |
| PROPOSED | Q01, Q03, Q06, Q09, Q11, Q12, Q13, Q14, Q17 (message), Q18, Q19, Q21, Q22, Q24 to Q32, Q34, Q36, Q37 |
| OPEN | Q05, Q10 (RTO), Q15, Q35 |

The most important finding: **the build order in Build Sequence v6 contradicts the story's own preconditions** (Q01).

## A. Concerns (dependencies)

### Q01 Dependencies used but not listed, and the build order (PROPOSED, gap G-056-01)

| Dependency | Story use | Build Sequence v6 | Finding |
|---|---|---|---|
| RWB-TE-007 Quartz and job run log | Section 3; flow step 5; `GET /admin/jobs` | TE-007 is order 21 and **depends on this story** (order 18) | The story needs the job run log, which is built after it. Circular in practice |
| RWB-E1-015 stale marker, EV-27 | Section 3 (precondition) | order 56 | Needed by AC8 and BR7; built 38 places later |
| RWB-E1-069 views, CHK-01 | Section 3 | order 10 | Fine |
| RWB-E1-001 `job_catalog` | V0004 seed | order 9 (E1-007, order 11, depends on it) | Fine, add to Depends on |
| RWB-E1-043 dictionary load | AC9 fix | order 8 | Fine, add to Depends on |
| RWB-TE-001 forbidden-name list | BR6 | early | Fine, add to Depends on |
| RWB-E1-070, RWB-E2-037 Temporal run books | Section 13 step 6 | order 34; Epic 2 | They write their own run books; no conflict |

**Proposed:** build TE-007 (scheduler and job run log) before this story and limit its dependency on E1-056 to the run books; the AC8 and AC9 parts that need E1-015 are tested with the stub batch row and re-run when E1-015 lands. Decision: Delivery lead and Tech lead.

### Q02 Job bodies come from other stories (ANSWERED)

Section 3 already says the jobs are "built or stubbed". A stub is a Quartz job that writes the `rwb.job.run` start and end event and nothing else; the owning story replaces its body. AC1 and AC3 ("ran at least once in SIT") pass with stubs.

### Q03 New Quartz jobs are not in the 16 catalog rows (PROPOSED, gap G-X-01)

Batch and Scheduling Design v4 has 22 jobs. Added under D-RCV-36: **JOB-20** RulePackageEffectiveDateJob (RWB-E1-073, daily 00:01, owner center of excellence analyst), **JOB-21** StuckWorkflowScanner (RWB-E2-037, every 5 minutes, platform administrator), **JOB-22** SmokeScheduleJob (RWB-E1-071, daily 06:00, platform administrator). RWB-E1-047 adds a weekly flag report job that is not in the table at all. `RunbookCompletenessTest` would fail on any of them that is in the recovery module without a row and a run book.

**Proposed final count for the Epic 1 release: 19 rows** = the 16 now + JOB-20 + JOB-22 + the flag report job (new ID, next free JOB-23). JOB-21 is seeded by RWB-E2-037 with `first_release` E2. The Temporal server and worker run books stay with RWB-E1-070 and RWB-E2-037. Decision: Tech lead. Update Batch Design v5 with the new ID.

Careful: the story's AC4 uses "JOB-20" as an example of a **new** job with a bad run book; JOB-20 is now a real job. Use a fake ID such as "JOB-99". Test Cases v7 uses "JOB-12", which is also a real job.

### Q04 Related documents are out of sync (ANSWERED, confirmed, gap G-056-02)

Test Cases v7: TC-E1-056-01, -03, -04 say 13 rows, TC-02 says 16; TC-05 uses JOB-03 (the story: JOB-04); TC-06 uses 2026-11-27 (the story: 2026-12-01); TC-04 uses JOB-12 (the story: JOB-20). FSD P7 AC-P7-014 still says "list of Epic 1 jobs" with 13 jobs and JOB-01. The story is module P2 Integration; the FSD files the ACs under P7. Rebuild the test cases and the FSD from the story after the Q03 decision.

### Q05 Infrastructure outside the squad (OPEN for the owner, gap G-056-04)

Observability and Monitoring Design v3 puts traces and metrics in Log Analytics. No document says who provisions the workspace, the workbook "Recovery jobs", the alert rules, or RW-PLATADM access to the workbook in DEV, SIT and UAT. Owner: ACE team with Azure operations. This is a precondition to name before build, not a design question.

## B. Business clarifications

### Q06 Who is the operations team in PROD? (PROPOSED)

Run Operating Model v2 (section 1): Tier 2 application support, which "handles defects, failed jobs, exception queues", is the **platform administrator, the reference data administrator and the data steward**; Tier 3 engineering is the TechX recovery squads and the ACE team; platform support (Azure, Entra ID) is SCB IT. So "operations" in the run books means RW-PLATADM. Who holds RW-PLATADM in PROD is not named; DL39 (option A) gives real users to administration roles at Epic 1, and the role owner appoints them (Admin and Access Model v5). Run book language is not decided (G-056-05): **proposed** English for run books and Thai plus English for alert text through the message table (DL10).

### Q07 Job owners without rerun rights: what do they do when alerted? (ANSWERED, partly)

Team manager (JOB-03, JOB-06), credit administration (JOB-07, JOB-08) and compliance (JOB-14, JOB-17) are alerted and cannot rerun (section 10). Run Operating Model v2 sends failed jobs to Tier 2, the platform administrator. So the escalation section of those run books says: **notify RW-PLATADM to rerun, and state the business decision the owner makes** (accept the late list, tell the collectors). The decision text per job is for the job's own story.

### Q08 Who owns JOB-05 (Timer check)? (ANSWERED)

Batch Design v4: **Platform administrator**. BR3 omits JOB-05; add it. Batch v4 owners for the rest match BR3: JOB-02, 04, 13 data steward; JOB-03, 06 team managers; JOB-07, 08 credit administration; JOB-10, 11, 12 platform administrator; JOB-14, 17 compliance; JOB-15 reporting and BI analyst.

### Q09 Cut-off for the morning allocation when the ACE batch is late (PROPOSED)

Batch Design v4 section 5: JOB-03 allocation "by 07:00"; the chain starts when the ACE batch record arrives; if a source is late, the data products show their last complete business date and AceDataLate goes to the data steward; there is no day-of run on previous-day data. E1-015 BR8 adds that the case list holds and the previous list stays published. So: **keep waiting, do not run on old data.** The cut-off time itself is disputed (07:00, 07:15, 08:00): see Q07 in the RWB-E1-015 file.

### Q10 Restart SLA and RTO (ANSWERED for the SLA, OPEN for the RTO)

Run Operating Model v2 section 2: severity 2 respond in 1 hour, restore in 1 working day; severity 1 respond 15 minutes, restore 4 hours. Batch Design v4 section 6: a failed job alerts its owner within 15 minutes. Whether "case list ready by 08:00" is an escalation trigger is not documented. RTO (NFR-023) is open, DL11.

### Q11 Mid-day rerun of JOB-02 or JOB-03 (PROPOSED)

A completed run is never repeated (AC7, BR5); a failed run restarts from its failed step, and the job body is idempotent for its business date (Batch v4 section 6: "No job processes the same business date twice"). So a rerun cannot re-allocate work the collectors have already started. State this in the JOB-02 and JOB-03 run books.

### Q12 ACE restates data after a job completed (PROPOSED, decision OPEN)

AC7 refuses every rerun. A controlled force-rerun with approval is in no document. **Proposed:** not in Epic 1; the incident goes to Tier 3 and ACE; a force-rerun path is a candidate for the Epic 8 administration stories (FEAT-ADM-12).

### Q13 WAITING has no timeout; what is SKIPPED? (PROPOSED)

Batch v4: the chain starts when the record arrives and JOB-02 "runs on the next complete ACE batch" with no cases from a stale business date. So WAITING has no timeout. **Proposed:** SKIPPED is the state of a business date that a later complete business date has overtaken; the next date is processed, the missed date is not back-filled. Add the definition and an AC (Q27).

### Q14 Alert thresholds and expected duration (PROPOSED)

1.5 times the expected duration is the DL11 assumption; JOB-02 at 45 minutes implies 30 expected. No document lists an expected duration per job (Batch Design v4 xlsx has none). Keep `expected_minutes` and `alert_after_minutes` as data (BR8) and ask each job's story to provide its expected duration.

### Q15 Alert channels and out-of-hours (OPEN)

Observability v3 gives owner roles and response times only (for example 15 minutes) and no channel. E1-056 section 4 uses e-mail from a Log Analytics alert rule. Teams, SMS, on-call paging and out-of-hours cover are in no document, and many jobs run between 05:00 and 06:30. Owner: SCB IT operations and the platform administrator. Needed before UAT.

### Q16 Which sources show "last complete ACE business date per source"? (ANSWERED)

Every distinct source in the E1-015 product-to-source map: ALS, SCBPDM, EFS, CCMS, SVAF, LIT, WIN, COLLINS (the Epic 1 sources), plus AMIS, RPS and GL once they are live (Integration Inventory v3: AMIS and RPS first release E3, GL E6). Show only live sources in Epic 1.

## C. AC details

### Q17 AC1 forbidden names and the X2 message (list: ANSWERED, a gap; message: PROPOSED)

**The list.** The module map in the local workbench repo (`18 E2E Recovery Workbench/backend/src/test/resources/architecture/recovery-modules.yaml`, RWB-TE-001, D-RCV-37) holds `modules` (19 names), `external` (common, collection) and `clientLibraries` (the call libraries that only the adapter package may use). It holds **no list of forbidden run book words**. The words the story relies on (inbound load job, file arrival, load rerun, data quality exception console, a table in schema `public`) exist only in the story text (G-056-08). **Proposed:** add a `forbiddenRunbookTerms` section to the YAML through a TE-001 change, matched as case-insensitive text (not whole-word), and read it in `RunbookCompletenessTest`.

**The message.** X1 uses MSG-P2-005 but X2 shows a raw build log text. **Proposed:** give X2 its own ID, `MSG-P2-028`, and assert it in AC1. (Message numbers are assigned across all four files in `Document Gaps.md`, G-X-06.)

Also: Error and Message Standard v4 says MSG-P2-005 concerns "the six sections"; the story has eight. Fix the standard (G-056-06).

### Q18 AC2 root cause: JOB-02 fails when `v_ace_account` has no row at 90 DPD (PROPOSED)

The data fault is ACE's. Batch v4 says JOB-02 makes "no cases from a stale business date" and a rerun fails again until ACE fixes the data. The restart steps should say: do not rerun; confirm in `v_ace_batch_status`; raise a data incident to ACE (Tier 3). Whether one bad account should stop the whole job or be raised as an exception row is a design question for the case creation story (RWB-E1-018). Decision: Tech lead.

### Q19 AC2 the 06:20 end time, and "no developer action" (PROPOSED)

Replace the clock time with a measurable condition: "ends COMPLETED within the job's `expected_minutes` times 1.5 on the test clock". Measure "no developer action" as: the ACE audit entries for the rerun show RW-PLATADM as the only actor.

### Q20 AC2 chain after a rerun (ANSWERED)

Flow step 10 and BR4: the system starts the dependent jobs in the order of the daily timeline; the administrator does not rerun each by hand.

### Q21 AC3 AGT-01 is a continuous service (PROPOSED)

Last run, duration and status mean nothing for a service. **Proposed:** AGT-01 reports a heartbeat (last heartbeat time and status) and has no rerun through the endpoint; its row keeps the heartbeat in the same columns with the schedule text "continuous". Owner: Center of excellence with the agent runtime story (RWB-TE-013).

### Q22 AC3 data consistency between the workbook and the endpoint (PROPOSED)

No tolerance is documented. **Proposed:** the AC compares them after a fixed wait for Log Analytics ingestion (assumed 5 minutes, DL11) and says "within 5 minutes".

### Q23 `{jobId}` is the failed execution ID (ANSWERED, gap G-X-05)

API v4 (`/admin/jobs/{jobId}/rerun`) names the path parameter `jobId`, the story says it is the failed execution ID and the interface method is `rerun(long failedExecutionId)`. Rename the parameter `executionId` in API v5 and say "rerun the failed execution of JOB-04" in AC5 and AC7.

### Q24 AC6 recipients and MSG-P2-004 (PROPOSED)

The recipient is the owner role in `job_catalog` (BR3), not "the data steward group": change AC6. The message: Standard v4 lists MSG-P2-004 for failure **and** for running past a threshold, but its text says "{job} failed at {time}", which is wrong for a running job; Story Defects v4 has it open twice. **Proposed:** a second message `MSG-P2-029` "{job} has run for {minutes} minutes, past its alert threshold of {threshold}. Follow run book {runbook}." and narrow MSG-P2-004 to failure.

### Q25 Repeated alerts (PROPOSED)

JOB-05 runs every 5 minutes. **Proposed:** one alert per run per condition, with the key job ID, business date and condition (failed or over threshold), so a job that stays over its threshold alerts once. Add to flow step 7.

### Q26 No AC for a FAILED job alert (PROPOSED)

Add:

```gherkin
  Scenario: AC10 Failed job alerts its owner
    Given JOB-07 fails at 05:50 on business date 2026-12-01
    When the alert rule runs
    Then the owner role "RW-CREDITAD" and RW-PLATADM receive message MSG-P2-004 within 15 minutes
    Then the alert is sent once for this run
```

### Q27 SKIPPED and "resolved" alert (PROPOSED)

Add an AC that a business date overtaken by a later complete date is recorded SKIPPED (Q13). For a "resolved" alert: **proposed yes**, one short message when the batch completes and the job starts, so the data steward sees the end of the incident; it needs its own message ID. Owner: Data steward.

### Q28 AC7 and MSG-GEN-004 (PROPOSED)

"Someone else changed this record" does not describe a rerun of a completed job. **Proposed:** `MSG-P2-030` "{job} has already completed for {date}." (Message numbers: see G-X-06.)

### Q29 AC8: what JOB-04 reads (PROPOSED, gap G-015-06)

Batch v4: JOB-04 is "Daily reconciliation"; JOB-02 is case creation. AC8 says "the case list step of JOB-04" and AC7 asserts both `case_list_row` and `reconciliation_result` for JOB-04. The documents never name the job that writes `case_list_row`. Settle it once with RWB-E1-015 (their Q17). Whether JOB-04 reads EFS (DP05): E1-015 AC9 says yes (the gate names DP05 and EFS). AC8 wording: "marks DP05 Contact and promises as STALE".

### Q30 The feature flag `rwb.integration.job-monitoring` (PROPOSED)

Precedent in the set: `rwb.p3.temporal` "Off: no worker, and the admin smoke endpoint returns 404" (TSD P3 v3). **Proposed:** off means the three admin endpoints return 404 and the workbook panel is hidden; `rwb.job.run` events and the alert rules stay on; the pipeline checks (`RunbookCompletenessTest`, CHK-01) never depend on a runtime flag.

### Q31 Data section lists "DF-OPS-224 to 232, all 9 fields" (PROPOSED)

The nine are the `job_catalog` columns in Physical Schema v6: `id`, `job_id`, `job_name`, `owner_role`, `schedule_text`, `runbook_path`, `expected_minutes`, `alert_after_minutes`, `first_release`. The story lists DF-OPS-226 to 232 by field and the other two by range only. List all nine, including `job_id`.

### Q32 CHK-01 is in the catalog but is a build-time gate (PROPOSED)

N. Anuroje: the row has a schedule and a threshold, the AC says it blocks a merge. `job_catalog` allows `expected_minutes` and `alert_after_minutes` to be null. **Proposed:** CHK-01's row has schedule text "Pipeline, every build", a null `alert_after_minutes` (no runtime alert) and a run book. Fields that do not apply are null, not invented.

### Q33 How does a held job resume? (ANSWERED)

N. Anuroje asked whether this is event driven. **Yes.** E1-015 flow step 11: a later COMPLETED batch sets the product LOADED and "starts the daily jobs through EV-26"; Batch v4: "the chain starts when the record arrives". It does not wait for a Quartz trigger. The one open detail is the listener's poll interval (E1-015 reads the view; E1-015 Q09 proposes 5 minutes).

### Q34 Scope of `RunbookCompletenessTest`: whole service or recovery module only? (PROPOSED)

N. Anuroje: if it scans every `JobDetail` in the ACE service, other squads' jobs would need eight-section run books. **Proposed: recovery module only.** The forbidden-name and module rules already come from the recovery module map (`recovery-modules.yaml`, root package `th.co.scb.ace.demo.recovery`; the common and collection modules are listed as `external`). Say in the story that the scan covers classes under the recovery root package and ignores the `external` modules. Owner: Tech lead.

## D. Follow-up (C. Gingpuwaluck)

### Q35 Monitoring tool: Log Analytics or CELK (OPEN, gap G-056-07)

The story and Observability v3 use Log Analytics. **CELK appears nowhere in the document set** (searched all converted text); the "feedback #77" is not in the set. If TechX targets CELK, it is a change to Observability v3, the workbook and the alert rules. Decision before the workbook is built: Solution architect with Ops and the ACE team.

### Q36 `job_catalog` seeded by migration V0004 or loaded as reference data (PROPOSED)

BR8 says owners and thresholds are data, but V0004 is a migration. E1-043 serves 12 reference tables (PRODUCT, REGION, EXPOSURE_BAND, ROLE, TEAM, QUEUE, SERVICE_LEVEL, DOCUMENT_TYPE, TEMPLATE, DELEGATION_LIMIT, LEGAL_PERIOD, PRODUCT_PARAMETER) and `job_catalog` is not one. **Proposed:** keep V0004 as the first, idempotent seed (`ON CONFLICT DO NOTHING`), and add `JOB_CATALOG` to LOV-REF-TABLE so that later changes are reference data loads and need no migration. This also removes the clash with "one migration per story".

### Q37 Alert and run book language (see Q06) (PROPOSED)

MSG-P2-004 has Thai text in Error and Message Standard v4; the story does not show it. Alerts use the message table (English and Thai, DL10); run books in English.

## Changes to make to the story

1. Header: Depends on adds TE-007, E1-001, E1-043, TE-001, E1-015 (Q01); resolve the order conflict.
2. Catalog: add JOB-20, JOB-22 and the flag report job; AC4 uses a fake ID (Q03).
3. BR3: add JOB-05 (Q08). Section 11: list all nine fields (Q31).
4. AC1: assert a message ID for X2 (Q17). AC2: measurable condition (Q19). AC3: AGT-01 heartbeat, consistency window (Q21, Q22).
5. AC5, AC7: failed execution wording (Q23). AC6: owner role from the catalog (Q24).
6. New ACs: FAILED alert (Q26), SKIPPED (Q27), flag off (Q30).
7. Messages: split MSG-P2-004, add the over-threshold message and the completed-job message (Q24, Q28).
8. Scope of the scan stated (Q34); CHK-01 row (Q32).
9. Regenerate Test Cases v7 and the FSD P7 ACs from the story (Q04).
