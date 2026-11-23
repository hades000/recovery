# Edit log B-ITG-W4-01 — RWB-ITG-W4: legacy RWB-AD-014, RWB-AD-015, RWB-AD-018, RWB-AD-019, RWB-AD-022

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date 22 November 2026.
Agent: aisdlc-msr-worker. fanout: 5, so five task subagents were used, one per legacy key, each writing only that key's story and fragment; the parent merged the gap and assumption rows.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG AD014 ITG Configure queues - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG AD015 ITG Configure service levels and timers - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG AD018 ITG Interface and job monitor - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG AD019 ITG Data quality and reconciliation console - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG AD022 ITG Partner firms and partner users - integration v1.md`
- `_work/msr/fragments/RWB-ITG-AD014-ITG.json`
- `_work/msr/fragments/RWB-ITG-AD015-ITG.json`
- `_work/msr/fragments/RWB-ITG-AD018-ITG.json`
- `_work/msr/fragments/RWB-ITG-AD019-ITG.json`
- `_work/msr/fragments/RWB-ITG-AD022-ITG.json`
- `_work/msr/gaps/B-ITG-W4-01.jsonl`
- `_work/msr/assumptions/B-ITG-W4-01.jsonl`
- `_work/msr/editlog/B-ITG-W4-01.md`

No existing file was edited; every file above was created by this WP. The five legacy keys stay untouched and no master file was written.

## What was produced

- Five ITG story files, one per legacy key, each with the 20 metadata rows of Template and Rules §R7.1 in order, the 19 sections of §R7.2 in order, the `SCB Collections and Recovery. Henka Group, 22 November 2026.` header, a D-RCV-60 change-log row naming the tool line, and §12.1 to §12.9.
- `RWB-ITG-AD014-ITG` Configure queues: 6 new acceptance criteria, `TC-AD-014-01-ITG` to `TC-AD-014-04-ITG`, patterns DP03, DP05, DP06, DP07, DP13 and DP19; the queue version, its approval and the allocation effect are proved across rwb-case, rwb-access and rwb-decision.
- `RWB-ITG-AD015-ITG` Configure service levels and timers: 6 new acceptance criteria, `TC-AD-015-01-ITG` to `TC-AD-015-04-ITG`, the same six patterns; the approved service-level version, the running timer that keeps its due date, the refusal and the decision record are proved across rwb-case, rwb-access and rwb-decision, and the timer lifecycle stays with RWB-ITG-E1028-ITG.
- `RWB-ITG-AD018-ITG` Interface and job monitor: legacy AC3 copied verbatim with its `(legacy RWB-AD-018 AC3)` tag plus 5 new criteria, `TC-AD-018-01-ITG` to `TC-AD-018-04-ITG`, patterns DP05, DP13 and DP19; the job and freshness composition, the single rerun, the WAITING and STALE pair and the no-rerun guardrail are proved against rwb-source-data.
- `RWB-ITG-AD019-ITG` Data quality and reconciliation console: legacy AC1 and AC2 copied verbatim with their tags plus 4 new criteria, `TC-AD-019-01-ITG` to `TC-AD-019-04-ITG`, patterns DP05, DP10 and DP19; the composition from rwb-source-data and rwb-case, the annotation, the access refusal and the Schedule refresh are proved. Legacy AC3 stays with the P1 and P3 slices and is not claimed here.
- `RWB-ITG-AD022-ITG` Partner firms and partner users: legacy AC1 copied verbatim with its tag plus 5 new criteria, `TC-AD-022-01-ITG` to `TC-AD-022-03-ITG`, patterns DP05, DP13 and DP19; firm scope, the partner-user resolution and the absence of a partner user in rwb-access are proved through rwb-partner, rwb-access and the partner gateway.
- Each story owns no production code, no table, no event publication, no workflow and no Schedule: it is a harness in `itg/recovery` that drives the owners' published operations, observes their published reads and writes one run report.
- Each story keeps the legacy test cases as `-ITG` copies with the Level column, and each has exception paths, business rules, state-transition, authority, data, contract, solution-plan, message, screen, test, guardrail, traceability and out-of-scope sections.

## Gaps and assumptions

- Gap rows: 5, one combined row per story — `GAP-0438`, `GAP-0439`, `GAP-0440`, `GAP-0441` and `GAP-0442`. All are type Missing and severity P2, needed by wave 4.
- Assumption rows: 5, one per story — `ASM-0630`, `ASM-0631`, `ASM-0632`, `ASM-0633` and `ASM-0634`. All are confidence Medium.
- Every placeholder in the five stories cites its own gap id and assumption id, the two ids exist as rows, and no other candidate id is used. The contractual patterns also cite the Ownership Map rulings `ASM-0069`, `ASM-0072`, `ASM-0075` and `ASM-0078`, which already exist.
- The defaults recorded are: run in SIT with stubs generated from the published contracts from Day 1; read and write only through the owners' published operations; hold every queue, service level, job, business date, data product, firm, partner user and instruction as fixture data; report a stub pass as a stub pass; never read a service schema or an ACE view.
- No release date was raised as a gap and no date was changed: 30 June 2027 and 28 February 2027 are copied unchanged and marked `(tentative)`.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-01 --quick` — C02, C03, C05, C12, C13 and C18 all PASS, 0 findings. The further WP-scoped checks C06, C07, C08, C09, C11, C14, C15, C16, C17 and C20 were also run over this WP's files and PASS; C11 returns the stage-wide warnings for legacy keys whose slices are not yet written. C01 passes. The stage-wide C04, C10 and C19 report missing outputs of other WPs that have not run yet and are outside this WP's Write only list.

## Notes and open points

- RWB-AD-014 and RWB-AD-015 own no legacy acceptance criterion in the split plan, so their ITG stories are built from new criteria that test only the cross-service deliverable; the legacy values (queue fields and the overflow rule, 10 working days with a warning at 8 for LIT_PACK) are used unchanged.
- RWB-AD-018 keeps legacy AC3 and RWB-AD-019 and RWB-AD-022 keep AC1 (and AC2 for AD019) word for word; their other criteria stay with the primary slices and are named in section 19.
- RWB-AD-022 carries business epic EP08 with the legacy release date 28 February 2027; the date is copied unchanged and marked tentative and is not raised as a conflict, as §R1 U7 and rule 10 require.
- rwb-integration (P2) is not called by any of the five stories: the job monitor reads the outbound actions through the P1 job read, and the partner portal is S9's. No P2 operation is invented.
- The interface and job monitor, the data quality console, the queue and service-level configuration and the partner portal all cross at least one service boundary and each is proved in one run report keyed by story and case or configuration key.
