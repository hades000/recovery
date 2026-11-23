# Edit log B-ITG-W1-04 - RWB-ITG-W1 Wave 1 integration

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-04 (legacy RWB-E1-024, RWB-E1-025, RWB-E1-026, RWB-E1-027, RWB-E1-028)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, in one dispatch. The E1025 subagent failed once on a connection error before writing anything and was re-dispatched alone; it then completed.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1024 ITG Document store and index - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1025 ITG Document types and fields agreed - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1026 ITG Attach and search screen - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1027 ITG Decision log writer v1 - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1028 ITG Service levels, timers, escalation and prescription dates - integration v1.md`

Every story carries the two header lines of Template and Rules section R8.1, the 20 metadata rows of section R7.1 in order, the 19 `### n.` section headings of section R7.2 in order, the nine contract sub-tables 12.1-12.9, the section 16 Level column, the origin tag on every Scenario line and the D-RCV-60 change-log row with the tool line. The service facts follow section R4: the integration service is rwb-integration (P2); each suite is a test harness and provides no API, no event and no table; the reserved P2 names are recorded as unused.

Because `acs` is empty on all five story lines, none of these ITG slices re-owns a legacy acceptance criterion. Each writes new criteria tagged `(new, D-RCV-60)` that test only the cross-service deliverable in its title, and each states in sections 2 and 18 that the legacy criteria stay with the sibling APP story (RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP, RWB-P7-E1027-APP, RWB-P3-E1028-APP and RWB-P4-E1028-APP). The legacy TC IDs are carried unchanged as `-ITG` copies in the WP order.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1024-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1025-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1026-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1027-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1028-ITG.json`

Each fragment has the 28 WP keys in the fixed order: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. H, C and X are empty on every ITG story; I carries the WP list exactly; tcs are the legacy IDs in the WP order; acs carries the new D-RCV-60 criteria with their exact Scenario first lines. The E1028 fragment lists the four case events as consumed and names the two deviation events in the story only, because they are wave 2 and not sent at wave 1.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-04.jsonl` - 5 rows (GAP-0349, GAP-0350, GAP-0351, GAP-0352, GAP-0353).
- `_work/msr/assumptions/B-ITG-W1-04.jsonl` - 5 rows (ASM-0443, ASM-0444, ASM-0445, ASM-0446, ASM-0447).

One combined gap row and one assumption row per legacy key. Each subagent wrote its two rows to a per-key part file (`_work/msr/gaps/B-ITG-W1-04-<key>.part.jsonl` and the matching assumptions part), and the parent merged the five parts into the two WP registers once, in legacy order, then removed the part files. No concurrent write to a shared register and no duplicate id.

## Coverage

- RWB-E1-024: nine new criteria (store against a real case across P5/P3/P1, write-once on a real WORM container, version history, duplicate, parameter-driven limits, decision record in the same transaction, missing case refused, copy pending, access refusal); 14 legacy TCs as `-ITG` copies; the P5/P3/P1 split and the shared decision-record topic are the recorded gap and assumption.
- RWB-E1-025: nine new criteria (store and type reader share one version, fields resolve to the P1 dictionary, type not in force refused, load with no source field refused, sign-off and invalid-value refusals, repeated version, future-version boundary, load-right refusal); 8 legacy TCs as `-ITG` copies; the P4-to-P3 reference-load move and the unpublished P5 load path are the recorded gap and assumption.
- RWB-E1-026: ten new criteria (composite list and upload, type-and-date search, checklist counts, missing type, malware refusal, duplicate, idempotency, date validation and empty state, scope refusal, parameter-driven size limit); 13 legacy TCs as `-ITG` copies; the gateway-bff composite path, its aggregation shape and the scan trigger are the recorded gap and assumption.
- RWB-E1-027: ten new criteria (four Epic 1 records, schema refusal, rule version refusal, failed write stops the action, idempotent repeat, no transaction, unknown decision code, ledger within five minutes, no data-lake copy, ledger-right refusal); 9 legacy TCs as `-ITG` copies; the PLT writer plus P7 ledger split, the P3 parameter and LOV ownership and the retired lake copy are the recorded gap and assumption.
- RWB-E1-028: twelve new criteria (durable timer start, warning and escalation, prescription date, missing service level, missing legal period, contract-date fallback, catch-up after a worker outage, single breach, decision-log failure at expiry, stage-clock-only pause, access refusal, durable timers replace JOB-05); 14 legacy TCs as `-ITG` copies; the JOB-05/TimerDue retirement, the P3 projection, the P1 account-date path and the wave 2 deviation events are the recorded gap and assumption.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-04 --quick` - C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- The five stories and five fragments were also checked directly for the 20 metadata rows in order, the 19 headings, the tagged Scenario lines, tables 12.1-12.9, the Level column and the WP TC order, parseable fragment JSON and the exact 28-key order, one placeholder pair per story with all CG/ASM citations resolving to the merged registers, no person name, no email address, no issue-tracker reference, no `/api/recovery/v1/` outside a preserved copy, and no wrong tool attribution.
- C06 PASS (I dependencies only, and only on ITG stories), C15 PASS (release unchanged and tentative), C16 PASS (service names in every topic and REST base), C17 PASS (register keys and citation resolution) and C20 PASS (tool line) were run on this WP's files.
- C19 was run on the full queue: it reports 200 planned outputs of other WPs that have not run yet (for example B-ITG-W1-03 and B-PLT-LIB-01) and zero B-ITG-W1-04 findings.
- C10 (legacy AC ownership) is a stage C/D check that waits for the sibling component fragments; it reports RWB-E1-024 AC10 to AC12 and RWB-E1-026 AC11 as not yet owned by any fragment, which are the criteria of RWB-P5-E1024-APP and RWB-P5-E1026-APP, not of these ITG slices.

## Notes for the assembler

- The five ITG slices carry I dependencies only; H, C and X are empty by the WP. Each section 13 DP table shows the section R5.5 dependency text for reference and states that the ITG story adds no build dependency.
- The new ACs are cross-service criteria only. The legacy ACs are not copied into these stories, so a later check that maps legacy AC ownership must read the sibling APP stories, not these files.
- RWB-E1-024 and RWB-E1-025 use the P3 parameter and reference-data contracts (DP-06, DP-07) and the P1 contracts without listing P3 or P1 as new stories: the WP I list is copied unchanged and the recorded assumption explains the route.
- RWB-E1-027 lists PLT and P7 only; the four Epic 1 records are produced by the wave 1 callers through the real library, and the suite drives the library through its conformance caller, so no P3/P5 contract is declared as an integration dependency.
- RWB-E1-028 retires JOB-05 and `TimerDue`, reads the timer through the P3 projection and the workflow history, and records the P1 account-date path and the wave 2 deviation events in the gap and assumption.
- No legacy master file was changed, and no issue-tracker, Confluence, GitLab or Figma call was made. No production data was used.
