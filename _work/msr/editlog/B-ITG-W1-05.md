# Edit log B-ITG-W1-05

WP B-ITG-W1-05, realignment decision D-RCV-60, 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Run: RWB-ITG-W1 wave 1 integration; five legacy keys RWB-E1-030, RWB-E1-031, RWB-E1-032, RWB-E1-034 and RWB-E1-037, one ITG story each, fanout 5 (one subagent per legacy key, all in one message, each writing only its own story and fragment).

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1030 ITG Daily rebalancing and queue measures - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1031 ITG Queue and owner on the case list with filters - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1032 ITG Automatic attach from the OCR intake - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1034 ITG Letter template management - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1037 ITG Role to permission matrix as data and PDPA field masking by role - integration v1.md
- _work/msr/fragments/RWB-ITG-E1030-ITG.json
- _work/msr/fragments/RWB-ITG-E1031-ITG.json
- _work/msr/fragments/RWB-ITG-E1032-ITG.json
- _work/msr/fragments/RWB-ITG-E1034-ITG.json
- _work/msr/fragments/RWB-ITG-E1037-ITG.json
- _work/msr/gaps/B-ITG-W1-05.jsonl
- _work/msr/assumptions/B-ITG-W1-05.jsonl
- _work/msr/editlog/B-ITG-W1-05.md

## Counts

| Item | Count |
|---|---|
| Story files | 5 |
| Fragments | 5 |
| Gap rows (CG) | 5 (one combined row per story, suffix -1 on each of E1030, E1031, E1032, E1034 and E1037) |
| Assumption rows (ASM) | 18 (3 for E1030, 3 for E1031, 4 for E1032, 4 for E1034, 4 for E1037) |
| Acceptance criteria | E1030 11, E1031 10, E1032 17, E1034 12, E1037 15; every one tagged `(new, D-RCV-60)` |
| Test cases | E1030 12, E1031 10 (one new `TC-ITG-E1031-ITG-10`), E1032 17, E1034 12 (one new `TC-ITG-E1034-ITG-12`), E1037 15; every legacy TC kept with the `-ITG` suffix |

Every story has the 20 metadata rows of Template and Rules §R7.1 in order, the 19 `### n.` sections of §R7.2, section 12.1 to 12.9 with "None" where empty, the Level column in §16, the DP table of §R5.5 for every pattern in its metadata row, the two header lines and the D-RCV-60 change-log row with the tool line above.

## Method and deviations

- Each of the five subagents read the template, the model story RWB-ITG-E1039-ITG, its own legacy story, the Arch v5 extract slides 13-20 and 41-44, the Temporal and Drools extract and the relevant Ownership Map rows, and wrote only its own story file and fragment.
- The WP executor wrote the two registers from the briefs so that one writer owns each jsonl and no row is lost to a concurrent append; the ids cited in the stories and fragments are exactly the rows in the registers.
- One adjustment after review: the E1034 story cited four gap ids while the WP allows one combined gap row per story; the three extra citations were normalised to `GAP-0357`, and the four assumptions stay distinct.
- No pre-existing file was edited, no legacy master was changed (C01 passes), and no external system was called.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-05 --quick` — C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.

Targeted run of the remaining checks over the files of this WP — C01 PASS, C14 PASS, C15 PASS, C16 PASS, C17 PASS, C20 PASS. C11 reports WARN only for legacy keys outside this WP whose stories are not written yet (for example E1-022 and E1-024); no warning names E1-030, E1-031, E1-032, E1-034 or E1-037, so every legacy test case of these five keys is kept.

## Open points

The five combined gap rows and the 18 assumption rows are in `_work/msr/gaps/B-ITG-W1-05.jsonl` and `_work/msr/assumptions/B-ITG-W1-05.jsonl`; step D1 numbers them as GAP-nnnn and ASM-nnnn. The main readings are the Schedule and rerun facade for JOB-06, the projection of the queue measures into rwb-reporting without a lake, the export access entry and masking source, the event-started intake and the resolve operation, the moved template operations and their freshness stamp, and the matrix load owner with the platform library boundary.
