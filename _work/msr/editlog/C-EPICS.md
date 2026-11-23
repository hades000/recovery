# Edit log C-EPICS — Recovery Workbench Service Epics v1

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: C-EPICS (31 epics: scope, wave, suggested owner, lanes, Day-1 stories)
Fanout: 0 (single agent, no subagents)

## Files written (4)

- `04 User stories/Recovery Workbench Service Epics v1.md` — new v1 (the source set has no earlier Service Epics file; the numbers come from the Service Story Catalog v1).
- `_work/msr/gaps/C-EPICS.jsonl` — 3 candidate gap rows (GAP-3198, GAP-3199, GAP-3200).
- `_work/msr/assumptions/C-EPICS.jsonl` — 3 assumption rows (ASM-5600, ASM-5601, ASM-5602).
- `_work/msr/editlog/C-EPICS.md` — this file.

Scratch (not a deliverable): `_work/msr/docs/C-EPICS/make_service_epics.py` (reader and writer for the file above) and `_work/msr/extract/C-EPICS/Recovery Workbench Service Story Catalog v1.md` (converted text of the source workbook, written by `compat/convert_sources.py`).

## What the file carries

- Two header lines of Template and Rules §R8.1 on lines 1–2, then the title, the tool line and the decision.
- A change-log table whose v1 row is "v1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash".
- All 31 epics, kept in the R5.1 order (7 platform, 19 service, 5 integration): one summary table row and one block per epic.
- Per epic: scope, service, epic wave, Arch v5 service wave, suggested owner (the full fixed phrase of §R5.3), owner basis, owner mix, stories, lanes, Day-1 stories, business-epic tags, releases and PRD; for a service epic also schema, REST base, topic, task queue, owned workflows, the Ownership Map counts of tables, REST operations and events, and the IN and OUT contract lines of Arch v5 slides 14–20; for a platform or integration epic the key stories and the rule references.
- Sections 6–9: Day-1 work by team type, epics per wave, lanes and contract groups, totals reconciled with `split_plan.json` stats.
- Sections 10–12: the three open items, the DOC-EPICS-01 to DOC-EPICS-06 traceability rows, and out of scope.

## Numbers copied unchanged from the source

- 31 epics: 19 service, 7 platform, 5 integration. Stories 1034, Day-1 stories 939, epic-lane memberships 547, distinct lanes 510, legacy stories 358 — equal to the Epics sheet and to `split_plan.json` stats (slices 1034, day1 939, lanes 510, legacy 358).
- Every release date is copied character for character and marked (tentative); no date was raised as a gap. New stories that carry no legacy date stay "None (new story)", the wording the story files use.

## Candidate registers

- Gaps: `_work/msr/gaps/C-EPICS.jsonl` — 3 rows. GAP-3198 (no epic-level scope or owner column), GAP-3199 (epic wave rule undefined where stories span waves; "NF" wording in §R5.6), GAP-3200 (547 epic-lane memberships against 510 distinct lanes). All three are P3 documentation rows.
- Assumptions: `_work/msr/assumptions/C-EPICS.jsonl` — 3 rows, one per gap, each cited from §10 of the file. All High confidence.
- Counts: CG rows 3, ASM rows 3.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp C-EPICS --quick` → C02, C03, C05, C12, C13, C18 all PASS.
- C14 (header), C15 (release dates), C16 (service names), C17 (gap and assumption citations), C19 (planned output present with the D-RCV-60 row) and C20 (tool line) were run directly on the same artefacts: all PASS.
- No person name, no email address and no issue-tracker reference appears in any file. No legacy master file was changed; the source workbook and the Ownership Map were read only.

## Notes for the assembler

- The epic wave is the earliest wave among the epic's stories (recorded as ASM-5601). Seven service epics therefore start before their service's Arch v5 wave; the per-service conflict stays with the story work packages, which raise one row per service and business epic (§R5.6).
- The epic owner is a soft suggestion (U3) and is the §R5.3 phrase most of the epic's stories carry (ASM-5600). RWB-ITG-NFR is the only epic owned by QA team, because its two stories are the performance and browser harnesses.
- Nothing in the source catalog, the Ownership Map or the Arch v5 extract had to be re-estimated: every value in the file is copied, or derived by one stated rule.
