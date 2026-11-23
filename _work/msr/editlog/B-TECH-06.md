# Edit log - WP B-TECH-06 (Workflow Engine Design next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Agent: aisdlc-msr-worker. fanout: 0, so no subagent was used.

## Files written

- 05 Technical architecture/Recovery Workbench Workflow Engine Design v4.docx
- _work/msr/docs/B-TECH-06/Recovery Workbench Workflow Engine Design v4.md
- _work/msr/docs/B-TECH-06/template-fixed.docx
- _work/msr/docs/B-TECH-06/fix_template.py
- _work/msr/docs/B-TECH-06/set_props.py
- _work/msr/docs/B-TECH-06/verify.py
- _work/msr/gaps/B-TECH-06.jsonl
- _work/msr/assumptions/B-TECH-06.jsonl
- _work/msr/editlog/B-TECH-06.md

The source `05 Technical architecture/Recovery Workbench Workflow Engine Design v3.docx` was never edited.
The converted source text is `_work/msr/extract/B-TECH-06/Recovery Workbench Workflow Engine Design v3.md`,
produced with `compat/convert_sources.py`.

## What was done

The next version is v4, the highest `v<n>` of the family plus one (R8.2). The full text was written to
`_work/msr/docs/B-TECH-06/Recovery Workbench Workflow Engine Design v4.md` and rendered with
`compat/office_write.py md-docx ... --template <source .docx>`, so the styles, the page setup and the footer
`(C) Siam Commercial Bank and Henka Pte Ltd` come from the source and the body is the new text.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules R8.1. The metadata table keeps
   every row of v3 (Document, Version, Date, Change, Prepared by, Structure) and adds Supersedes, a second
   Change row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`,
   a Decision row and a Status row. The v3 Change row (D-RCV-36, 16 November 2026) is copied word for word.
   Status is Draft because no approval is recorded (ASM-3248).
2. **Every section kept.** 1 to 9 in the same order with the same titles. Three new subsections carry the
   realignment: 3.1 the parent and its children, 5.1 Schedules, 5.2 the workflow kit. No section, table row or
   bullet of v3 was dropped: `verify.py` reports that every section heading, every identifier (JOB-nn, E1-070,
   E2-043, ADR-011, MSG-P3-036, R-UNI-33, DL22, EV-nn, REQ-DRI-005, SY-*, temporal.*, drools.*), every number
   (10 stages, 30 milestones, 150 tasks, 53 event listeners, 448 sentries, 93 tables, 51,200 events, 50 MB,
   1 second, 2, 10, 30 days, 24 hours, 7233) and every date of v3 is present in v4. The only table row label of
   v3 that changes text is `Epics 1-2 work`, whose row now says that Quartz is retired.
3. **Workflow kit (first change).** Section 1 gains a Workflow kit row; section 5.2 gives the eight kit templates
   of Architecture v5 slide 23 (Approval, Notify, Document intake, Agent run with rule fallback, Human task with
   SLA, Saga runner, Scheduled job, Partner instruction), what each does and which stage workflow uses it. The
   kit is owned by the platform team and delivered with RWB-PLT-E1071, the contract DP-10 names (GAP-2023;
   ASM-3252).
4. **Child workflow per stage (second change).** DP-12 and Architecture v5 slide 25 replace the one-long-workflow
   model: section 1 restates the Workflow per case row, section 2 maps Stage to a child workflow on the owner's
   queue, section 3 adds the case router step (signalWithStart) and the forwarding to the running child, and
   section 3.1 lists the parent and its nine children with the owner and task queue of each from the Microservice
   Ownership Map v1 (P3 rwb-case, S1 rwb-valuation, S2 rwb-treatment, S3 rwb-guarantee, S4 rwb-litigation,
   S5 rwb-asset, S6 rwb-debtsale, S7 rwb-writeoff, S8 rwb-deviation, P7 rwb-decision for ApprovalWorkflow).
   Section 6 adds the Continue-As-New rule and parent close policy ABANDON.
5. **Schedules (third change).** Quartz is retired (TE-007, JOB-05). Section 1 restates the Epics 1-2 work row,
   section 4 gives every timer as a durable timer of the owning service and keeps the TimerScheduler port and its
   four methods, and section 5.1 carries the whole job map of Architecture v5 slide 44: all 20 jobs with When,
   Owner and the mechanism in v4, of which nine are Temporal Schedules (JOB-06, 14, 16, 17, 18, 19, 20, 21, 22).
   Each job owner is the owner in the Ownership Map v1 (Jobs).
6. **Owners.** Every owner in the document comes from the Microservice Ownership Map v1 and
   `_work/msr/plan/ownership.json`: services and task queues (Services sheet), the ten workflows
   (Workflows and activities sheet), the 20 jobs of 5.1 (Jobs sheet) and the parameters and reference data of
   section 5 (Parameters sheet, RWB-P3-E1042-CON and RWB-P3-E1043-CON). No person is named anywhere; only roles
   (RW-PLATADM, RW-AUDIT, RW-SECADM) and team types.
7. **Release dates.** The two dates of the delivery table are kept unchanged and marked `(tentative)` (U7). No
   date was raised as a gap.
8. **Decisions used.** D-RCV-60 with the IDs of `_work/msr/plan/ids.json`: ADR-014, ADR-016, ADR-017 and ADR-022,
   DL44, plus ADR-011 as cited by the source. DP-01, DP-02, DP-05, DP-06, DP-07, DP-10 and DP-12 of R5.5.
   No new ADR or DL ID was allocated by this work package.
9. **Never invented.** Where a source is silent the document carries the R9 placeholder and the pair of rows:
   the child workflow ID (GAP-2021), the Schedule attributes (GAP-2022), the kit version
   (GAP-2023), the timer-row rule (GAP-2016), the stage-clock pause (GAP-2024),
   Continue-As-New with a signal in flight (GAP-2020) and the child failure path (GAP-2019).

## Counts

| Item | Value |
|---|---|
| Candidate gap rows | 9 (GAP-2016 to GAP-2024) |
| Candidate assumption rows | 12 (ASM-3248 to ASM-3259) |
| Sections kept | 9 of 9 |
| Subsections added | 3 (3.1, 5.1, 5.2) |
| Kit templates listed | 8 |
| Child workflows listed | 9 (parent plus 8 stage children and ApprovalWorkflow) |
| Jobs in the schedule table | 20 (9 Temporal Schedules, 1 retired, 10 event-started or Airflow-driven) |
| Release dates marked tentative | 7 of 7 |

Gap types: Ambiguous 1, Missing 7, Conflict 1. Severity: P2 5, P3 4.
Assumption confidence: High 3, Medium 9.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-06 --quick`: PASS (C02, C03, C05, C12,
C13, C18). `verify.py` reports PASS on the R8.1 header, the change-log row, every section, every identifier,
every number and every date of the source, the tentative release dates, the seven realignment values and the
resolution of every CG and ASM citation to a jsonl row. A source-to-next-version table diff reports 0 lost table
row labels.

## Not done, by rule

- No approval was sought and none is recorded; the document is Draft.
- No master file, no register number and no other document was edited; no issue tracker, no git commit.
- The Decision Log, the Change Register and the Batch and Scheduling Design v5 are other work packages and were
  read only where this document cites them.
