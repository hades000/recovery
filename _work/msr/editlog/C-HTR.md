# Edit log C-HTR

Work package: WP C-HTR, How To Read The Acceptance Criteria next version.
Decision: D-RCV-60. Agent: aisdlc-msr-worker. Fanout: 0, so no subagent was started.
Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench How To Read The Acceptance Criteria v2.docx`
- `_work/msr/docs/C-HTR/Recovery Workbench How To Read The Acceptance Criteria v2.md`
- `_work/msr/docs/C-HTR/build.py`
- `_work/msr/docs/C-HTR/set_props.py`
- `_work/msr/docs/C-HTR/write_rows.py`
- `_work/msr/docs/C-HTR/source_structure.txt`
- `_work/msr/docs/C-HTR/verify/Recovery Workbench How To Read The Acceptance Criteria v2.md`
- `_work/msr/gaps/C-HTR.jsonl`
- `_work/msr/assumptions/C-HTR.jsonl`
- `_work/msr/editlog/C-HTR.md`

Scratch only, listed for completeness: `_work/msr/docs/C-HTR/_arch.txt` and `_work/msr/docs/C-HTR/_temporal.txt` are the notes taken from the two text extracts while checking the service statements, and `_work/msr/extract/C-HTR/` holds the converted source. The source v1 document was never edited.

## What the new version does

The two header lines of Template and Rules §R8.1 are the first two paragraphs of the docx, followed by the title, a metadata table, the change-log row `2, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`, and the source's own title line.

| Item | Change |
|---|---|
| Intro | The two source paragraphs (English and Thai) are kept word for word; one paragraph is added to say what this version adds |
| How the set is sliced | New. One story per service and work type, what a slice is, the counts of this version, the four parts of the story key plus the -2 delta, the six work types with their fixed suggested-owner phrases, the five slices of RWB-E1-001, and the six preserved Epic 1 stories |
| A scenario has three parts | Kept word for word with its Thai paragraph and its Given/When/Then table |
| Every line states its own role | Kept word for word with its Thai paragraph |
| The result says who acts | Kept word for word with its Thai paragraph |
| A worked example | Kept word for word with its Thai paragraph and its six-row table; one paragraph added naming RWB-ITG-E1001-ITG as the story that carries AC7 now |
| The origin tag at the end of every scenario | New. The two tags, `(legacy RWB-E1-001 AC7)` and `(new, D-RCV-60)`, and what each one tells a reader |
| The AC number inside the tag | New. Inherited numbers keep their legacy value and can leave gaps; new numbers continue after the last legacy number; the AC2, AC7, AC12 and AC15 lines of RWB-ITG-E1001-ITG are the example |
| Reading the slices of one legacy story | New. The reading order of a slice set, and the five slices of RWB-E1-001 with the legacy and new scenarios each one carries |
| The sentence patterns that repeat | Kept word for word with its 23-row table |
| The codes you will see | Kept word for word with its 13-row table |
| Where to read more | The three source paragraphs and their Thai text are kept word for word; two paragraphs are added, one pointing at the Service Story Catalog v1, the Story Build Order v3, the Day-1 Work Allocation v1 and the Dependency Map v4, and one stating the Thai gap |

Checked mechanically on the rendered file: all 58 Thai lines of the source are present in the new docx text, and every non-empty line of the source appears in the read-back conversion. No release date appears in the source or in this version, so no date needed the (tentative) mark; the date 22 November 2026 is the version date. No person name is left anywhere in the package (the source carried one in its document properties, which are replaced). No new ADR or DL ID was needed.

## Gap and assumption rows

| Register | Rows | IDs |
|---|---|---|
| Gaps (CG) | 5 | GAP-3201 (source has no version, date or status, Missing, P3), GAP-3202 (the guide predates slices, Outdated, P3), GAP-3203 (no Thai wording for the new sections, Missing, P3), GAP-3204 (work types and key pattern absent, Missing, P3), GAP-3205 (hub and glossary state after the realignment, Ambiguous, P3) |
| Assumptions (ASM) | 6 | ASM-5603 to ASM-5608 |

Counts: 5 CG rows, 6 ASM rows. Highest severity: P3. The placeholder `Not specified in the source documents (GAP-3201; ASM-5603)` appears in the Supersedes row and in change-log row 1; `(GAP-3203; ASM-5605)` appears in the closing paragraph of Where to read more.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C-HTR --quick` - see the report in `22 Microservice Realignment/checks/reports/`. Result: all six quick checks PASS.

## Failures

None.
