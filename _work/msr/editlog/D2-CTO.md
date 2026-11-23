# D2-CTO edit log

WP: D2-CTO — Recovery Workbench Executive Presentation CTO, next version.
Decision: D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Fanout: 0 (no subagents).

## Files written

- `12 Project communication/Recovery Workbench Executive Presentation CTO v4.pptx`
- `_work/msr/docs/D2-CTO/slides.md`
- `_work/msr/docs/D2-CTO/build_deck.py`
- `_work/msr/docs/D2-CTO/extract_logo.py`
- `_work/msr/docs/D2-CTO/cover_logo.png`
- `_work/msr/docs/D2-CTO/dump_slides.py`
- `_work/msr/docs/D2-CTO/peek.py`
- `_work/msr/docs/D2-CTO/check_kept.py`
- `_work/msr/docs/D2-CTO/verify/Recovery Workbench Executive Presentation CTO v4.md`
- `_work/msr/gaps/D2-CTO.jsonl`
- `_work/msr/assumptions/D2-CTO.jsonl`
- `_work/msr/editlog/D2-CTO.md`

## What was done

1. Read the version 3 deck (7 slides) through the compat converter; read the Template and Rules (R1, R3, R5, R8, R9), the Architecture v5 extract (slides 13 to 20, 41 to 45), the Temporal and Drools extract, the Ownership Map v1 (Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Rulings), the ownership plan and split plan stats and legacy, and the ID plan.
2. Copied the source to v4 with `compat/office_write.py copy`; the source file was not touched.
3. Wrote the new realignment section (12 slides) as `_work/msr/docs/D2-CTO/slides.md`: header and change log, what this version changes, wave-band diagram, the ten platform services, the nine stage services, the wave plan, Day-1 work with counters, ownership, gaps and assumptions, where to read more, and a divider before the kept version 3 slides.
4. Rendered the section into the copy in the deck's own style (24 pt purple title, rule line, footer number, table style of the version 3 slides, brand cover) and moved it in front of the kept slides: 12 new + 7 kept = 19 slides.
5. Verified by re-converting the written deck and checking every slide: 19 slides, the two header lines are the first two text lines, every version 3 statement, ID, count and date is unchanged, and no shape crosses the slide edge.

## Notes and deviations

- `compat/office_write.py pptx-append` writes markdown table rows as literal pipe text into a body placeholder. This deck is table- and diagram-led (WP D2-CTO: services, waves, Day-1, gaps), so the same `slides.md` is rendered by `_work/msr/docs/D2-CTO/build_deck.py`, which reads that markdown and writes real tables, wave-band shapes and counter cards in the version 3 visual style. The prescribed `copy` step is used unchanged; no source file is edited.
- The kept version 3 slides carry their original words. Only the footer page number follows the new position (13 to 19); recorded as ASM-D2-CTO-8.
- Release dates: none was invented. The wave slide carries the placeholder of R9 with CG-D2-CTO-1 and ASM-D2-CTO-3.
- No person named; owners are the service codes of the Ownership Map plus the suggested owner per work type (R1 U3, DL46).
- No issue tracker, no external call, no commit.

## Counts

- Gap candidate rows: 4 (CG-D2-CTO-1 to CG-D2-CTO-4).
- Assumption candidate rows: 8 (ASM-D2-CTO-1 to ASM-D2-CTO-8).
- New slides: 12. Kept slides: 7. Total: 19.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp D2-CTO --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- Kept-slide check (`_work/msr/docs/D2-CTO/check_kept.py`): the text of the 7 kept version 3 slides is identical to the source, footer numbers aside.
- Deck check: 19 slides, the two R8.1 header lines are the first two text lines of slide 1, the v4 change-log row appears on slides 1 and 2 verbatim, and no shape crosses the slide edge.
