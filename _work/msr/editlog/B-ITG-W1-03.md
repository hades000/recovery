# Edit log B-ITG-W1-03 — RWB-ITG-W1 Wave 1 integration

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-03 (legacy RWB-E1-019, RWB-E1-020, RWB-E1-021, RWB-E1-022, RWB-E1-023)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message; two were re-dispatched after a network reset and a rate limit and wrote only their own files.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1019 ITG Roles, teams and queues as data - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1020 ITG Allocation and assignment engine v1 - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1021 ITG Transfer rules and engine v1 - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1022 ITG Sign-on with SSO, MFA and the first roles - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1023 ITG Case record view v1, read only - integration v1.md`

482, 526, 542, 481 and 511 lines. Every story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in order, the 19 `### n.` section headings of §R7.2 in order, the nine contract sub-tables 12.1–12.9, the §16 Level column, one origin tag on every `Scenario:` line and the D-RCV-60 change-log row with the tool line. The service facts follow §R4: the integration service is rwb-integration (P2), each story is an integration suite and provides no API, no event and no table; the P2 reserved names (`/api/recovery/integration/v1`, `rwb.integration.events.v1`, `rwb-integration`, `rwb_integration`) are recorded and unused in every 12.1.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1019-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1020-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1021-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1022-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1023-ITG.json`

Each fragment carries the 28 keys of the WP in the WP order: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. H, C and X are empty on every story; I carries the WP list unchanged (4, 4, 5, 3 and 7 entries); `tcs` keeps the legacy ids in the WP order without the `-ITG` suffix; `acs` carries the owned legacy criteria or the new D-RCV-60 criteria, with `text_first_line` identical to the Scenario line in the story.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-03.jsonl` — 5 rows: GAP-0344, GAP-0345, GAP-0346, GAP-0347, GAP-0348.
- `_work/msr/assumptions/B-ITG-W1-03.jsonl` — 5 rows: ASM-0438, ASM-0439, ASM-0440, ASM-0441, ASM-0442.

One combined gap row and one assumption row per legacy key, as the WP allows. The per-key rows were returned by the subagents and merged by the lead in one write, so there is no duplicate id and no concurrent write to a register. Every CG and ASM id cited in the five stories and five fragments resolves to a row in these two files.

## Coverage by legacy key

- RWB-E1-019: no legacy AC is owned by this slice. Ten new ACs tagged `(new, D-RCV-60)` prove the cross-service queue reference data: one approved load in force for the queue read (P3), the role read (P4) and the notice (P6); the one-call rollback; the role that is not in force refuses the load; capacity and allocation agree at the cap; queue membership becomes the P4 scope; the future valid-from version; the idempotent reload; the P4 guard on Reference data C; the same reference-approval pattern as the delegation table (P4-E1038); and the queue code read on the notice without a copy. 13 legacy TCs carried as `-ITG`.
- RWB-E1-020: legacy AC10 (`AC10 The run waits for case creation`) copied word for word with `(legacy RWB-E1-020 AC10)`, plus 10 new ACs on the cross-service allocation: JOB-03 as a DailyCaseRun step by 07:00; the two packages fetched from rwb-decision with a verified checksum; one ledger record per allocation within five minutes; CaseAllocated and CaseAllocationFailed in the envelope; the deviation queue; no version in force; the rerun; the overflow and exception reconciliation; the refused rerun; the failed record that stops one case only. 15 legacy TCs carried as `-ITG`.
- RWB-E1-021: no legacy AC is owned by this slice. Ten new ACs on the transfer: the eight triggers as events of their owners; the case router signal and the inbox dedupe; the TRANSFER package fetched and evaluated in the case activity; one ledger record per transfer; one CaseTransferred event; the legal hold that stops an automated transfer; the manual transfer contract and its reason list; the overflow queue; no rule matched; no version in force. 16 legacy TCs carried as `-ITG`.
- RWB-E1-022: legacy AC1 (`AC1 SSO sign-in`) and AC3 (`AC3 Not in group`) copied word for word with their origin tags, plus 8 new ACs on the edge and the boundary: the short-lived user JWT at every owner; the group-to-role mapping as one data row; the scope from the P3 membership; the service identity refused like a person; the refusal event to the audit path with no personal data; the matrix version and the open session; the cached authorise answer; the session only at the edge and the MFA gate at the edge. 10 legacy TCs carried as `-ITG`.
- RWB-E1-023: legacy AC4 (`AC4 Stale ACE batch`), AC11 (`AC11 No copy of the account on the case`) and AC12 (`AC12 An account link with no ACE row`) copied word for word with their origin tags, plus 8 new ACs on the composed screen: the parallel owner calls; the freshness from P1; the one AC-READ record across P3 and P4; the masking rule of P4; the merged contact history from the P1 ledger (DP-18); the deviation and hold flags of S8; the document-hub section message; the refusal at the first owner call. 13 legacy TCs carried as `-ITG`.

The legacy criteria bodies were compared line by line with §7 of the five legacy stories: every owned criterion is identical apart from the appended origin tag.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-03 --quick` → C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- The same WP file list was run directly through C14, C15, C16, C17, C20: all PASS. C19 lists this WP's editlog before it was written and planned outputs of other WPs that have not run; no other B-ITG-W1-03 output is missing.
- Additional direct checks on the five stories: 20 metadata rows in order; 19 headings in order; every Scenario line tagged; the nine `12.x` sub-headings in order; all legacy TCs present as `-ITG` copies with the Level column; the §13 DP table with every pattern of the WP; only the WP gap and assumption ids cited; no `/api/recovery/v1/` outside an as-built section; no person name, no e-mail, no issue-tracker reference and no wrong tool attribution. The five fragments parse with the 28 keys in order.

## Notes for the assembler

- The ITG slices carry I dependencies only; H, C and X are empty by the WP. The §13 DP table shows the §R5.5 dependency text for reference and states in words that an ITG story adds no build dependency and blocks no build of its own.
- RWB-E1-020: JOB-03 is a DailyCaseRun step in rwb-case, while the job catalogue read and the rerun are x-module P1 in the ownership map (GAP-0345). The suite reads the run through the P1 catalogue and asserts the step through the workflow; the monitor surface of a workflow step is the recorded gap.
- RWB-E1-021: the route-decided trigger (TRF-002) is the legacy rule event carried in CaseStateChanged; Arch v5 announces the route from rwb-valuation (S1, wave 3) as RouteDecided. The wave 1 run asserts the case side only and does not fake S1 (GAP-0346).
- RWB-E1-022: the authorise operation is the published rwb-access contract of Arch v5 slide 14 (`POST /authorise`) on the P4 base of DP-13; it has no row of its own in the ownership map. The user-JWT claim set and the place of the MFA gate are the recorded gap (GAP-0347).
- RWB-E1-023: the case-scoped deviation read follows `GET /deviations` of Arch v5 slide 15 on the S8 base of slide 41, because the ownership map carries only POST and PATCH for the resource; S8 is a wave 2 service in Arch v5 but is listed as an integration dependency of this wave 1 story by the WP. Both are recorded in GAP-0348. The interaction read is P1's under ASM-0038.
- RWB-E1-019: the notice of rwb-comms carries the queue and team code read from the P3 contract; the field names of that notice response and of the P4 session team scope are the recorded gap (GAP-0344).
- No legacy master file was changed, and no issue-tracker, Confluence, GitLab, Figma or web call was made.
