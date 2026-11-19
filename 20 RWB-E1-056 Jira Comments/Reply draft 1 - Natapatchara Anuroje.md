# Reply draft 1: to Natapatchara Anuroje (comment 1793629)

Status: DRAFT. Not posted to Jira. Written for the TB0001-1217 thread; the text below the line is what would be posted.

Source: `19 Jira Open Questions/RWB-E1-056 Open questions and answers.md` (Q32, Q33, Q34, Q01) and `RWB-E1-007 Open questions and answers.md`.

---

[~accountid:63dea460614cb4ba53009c69] thank you, these are useful. Replies to each point, based on the document set of 15 Nov (Story Files v7, Batch and Scheduling Design v4, Decision Log v10).

*1. How does a held job resume? Answered.*
It is event driven. RWB-E1-015 flow step 11 says a later COMPLETED batch sets the data product to LOADED and starts the daily jobs through EV-26. Batch and Scheduling Design v4 says the same: the chain starts when the ACE batch record arrives, not at the next Quartz trigger. So JOB-04 does start at 08:40 on the same day. One detail is still open: how often the listener checks the ACE batch status view. RWB-E1-015 proposes 5 minutes. We will add the wording "started by event EV-26, not by the Quartz trigger" to AC8.

*2. Scope of the RunbookCompletenessTest scan. Proposed, needs the tech lead to confirm.*
Recovery module only. The module map `recovery-modules.yaml` has the root package `th.co.scb.ace.demo.recovery` and lists the collection and common modules as `external`. We propose that the story says the scan covers classes under the recovery root package and ignores the `external` modules, so no other squad needs run books in this format. The Out of Scope section should say so.

*3. CHK-01 is a catalog row but also a build gate. Proposed.*
`job_catalog` allows `expected_minutes` and `alert_after_minutes` to be null. We propose that the CHK-01 row has the schedule text "Pipeline, every build", a null alert threshold (no runtime alert) and a run book. Fields that do not apply stay null.

*Dependencies.*
- RWB-E1-007: the 20 open items on this ticket were mostly about the inbound file checks. Decision D-RCV-35 (15 Nov) made RWB-E1-007 outbound-only, so most of them no longer apply; the E1-007 Jira description is out of date. The catalog count is not affected by E1-007. The jobs that do affect it are the ones added under D-RCV-36 (JOB-20, JOB-21, JOB-22) and the weekly feature-flag report from RWB-E1-047. We propose a catalog of 19 rows for the Epic 1 release; the tech lead decides.
- RWB-E1-015 and RWB-E1-069 do have story files in v7. The real problem is the build order: Build Sequence v6 puts RWB-E1-015 at order 56, after this story at order 18, and puts RWB-TE-007 (the job run log this story reads) at order 21. We propose building TE-007 first and testing the stale-marker parts of AC8 with a stub batch row until E1-015 lands.
- RW-PLATADM and RWB-E1-022: the Entra ID group is not available until that story delivers it. We propose adding RWB-E1-022 to Depends on. I have not checked how the role checks are handled in the meantime.

Still open for the owners: the tool for monitoring (Log Analytics or CELK), who provisions the workspace and alert rules, and the PROD holders of RW-PLATADM. These are on the other comments.
