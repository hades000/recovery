# Edit log C4-BSEQ — Build Sequence next version

Decision: D-RCV-60 microservice realignment.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Agent: aisdlc-msr-worker. Fanout: 0 (no subagent used).

## Source read

Read only, never modified:

Read: 11 Delivery and operations/Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx (copied to the next version)
Read: 04 User stories/Recovery Workbench Service Story Catalog v1.xlsx (1034 stories with lane, ready, release and owner)
Read: 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (§R1, §R3, §R5, §R6, §R8, §R9)
Read: 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx, with _work/msr/plan/ownership.json
Read: 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (slides 13 to 20, 41 to 44)
Read: 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
Read: _work/msr/plan/split_plan.json ("stats" and "legacy" only) and _work/msr/plan/ids.json
Read: the converted text written to _work/msr/extract/C4-BSEQ/ with compat/convert_sources.py

## Files written

- 11 Delivery and operations/Recovery Workbench Build Sequence Epic 1 and Epic 2 v7.xlsx
- _work/msr/gaps/C4-BSEQ.jsonl
- _work/msr/assumptions/C4-BSEQ.jsonl
- _work/msr/editlog/C4-BSEQ.md
- _work/msr/docs/C4-BSEQ/build.py
- _work/msr/docs/C4-BSEQ/registers.py
- _work/msr/docs/C4-BSEQ/prep.py
- _work/msr/docs/C4-BSEQ/agg.py
- _work/msr/docs/C4-BSEQ/analyze.py
- _work/msr/docs/C4-BSEQ/mapping.json
- _work/msr/docs/C4-BSEQ/src_v6_dump.txt

## What changed (v6 to v7)

- Copy of v6, then extended. Every sheet of v6 is kept: Sequence, By window, Critical path, By module, Pull rules.
- All 115 items, their keys, titles, modules, types, priorities, dependencies, windows, dates, releases and critical-path flags are kept character for character; Order (v6) is on every row.
- New columns on Sequence: Contract story (v7), Delivery stories (v7), Service(s) (v7), Lane(s) (v7), Owner(s) (v7), Ready to start (v7), plus Order (v7). 115 items map to 530 stories: 441 by a service and 89 integration stories. Owner(s) (v7) takes the owner of each new story as recorded in the catalog, so a harness or NFR story shows QA team and the rest show the team type of their work type.
- New sheet "Day 1 first": 65 platform stories (wave 0) and the contract groups CG-W1 (44) and CG-W2 (64), 173 stories in pull order before Window 1.
- New sheet "By service and lane": 18 service or platform or integration rows (the services that carry part of the 115 items) with window counts, contract stories, lanes and Day-1 stories, plus the 17 lanes that hold more than one story.
- New sheet "Owners (v7)": the work-type owner phrases of §R5.3, the Ownership Map default rulings and the 19-service map.
- New sheets "Read me" (first sheet, two lines of §R8.1 header and the change-log row) and "Change log".
- By window: three new columns (stories after the split, contract stories, items with no contract story of their own). Source rows and counts unchanged.
- Critical path: three new columns (story, service, lane). The 17 steps, their windows and their gating notes unchanged.
- Pull rules: rules 1 to 6 unchanged; rules 7 to 12 added for the realignment (Day-1 block, contract-first build, H and I rules, service waves, tentative dates).
- Release dates copied unchanged and marked (tentative); the Release column keeps the v6 edition labels E1, E2 and E3; no date was raised as a gap.
- Retired items RWB-E1-014 and RWB-TE-007 keep their rows, marked "No new story" and "Not pulled" (§R6).

## Gaps and assumptions

- Gaps: 5 candidate rows in _work/msr/gaps/C4-BSEQ.jsonl (GAP-3227 to GAP-3231), for D1 to number.
- Assumptions: 12 candidate rows in _work/msr/assumptions/C4-BSEQ.jsonl (ASM-5635 to ASM-5646), for D1 to number.
- The placeholder cited in the workbook is GAP-3227 with ASM-5640 (release date missing for the 23 new wave-0 platform stories).

## Checks

- python -I "22 Microservice Realignment/checks/run_all.py" --wp C4-BSEQ --quick : PASS on C02, C03, C05, C12, C13 and C18.
- The source workbook and every other read-only file were not modified.

## Notes

- No subagent was used: the work package sets fanout 0.
- No external system was called; no issue tracker entry was created or updated.
- No names of people appear in any output; owners are roles and team types only.
