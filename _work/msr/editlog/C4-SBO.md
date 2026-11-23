# Edit log - WP C4-SBO (Recovery Workbench Story Build Order next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `11 Delivery and operations/Recovery Workbench Story Build Order v4.docx`
- `_work/msr/docs/C4-SBO/Recovery Workbench Story Build Order v4.md`
- `_work/msr/docs/C4-SBO/items.json`
- `_work/msr/docs/C4-SBO/paras.json`
- `_work/msr/docs/C4-SBO/gen.py`
- `_work/msr/docs/C4-SBO/post.py`
- `_work/msr/docs/C4-SBO/verify.py`
- `_work/msr/docs/C4-SBO/gapwrite.py`
- `_work/msr/gaps/C4-SBO.jsonl`
- `_work/msr/assumptions/C4-SBO.jsonl`
- `_work/msr/editlog/C4-SBO.md`

Scratch only (`_work/msr/docs/C4-SBO/`): the full text of the new version, the 115 items read out of
the five tables of version 3 (`items.json`), the paragraph dump of version 3 (`paras.json`), the
generator of the Markdown, the post-processor that sets the table widths and the document properties,
the verification script and its re-extract in `verify/`, and the register writer. The converted source
text was written by the conversion tool to the extract folder the WP names,
`_work/msr/extract/C4-SBO/`.

## What was done

The source `11 Delivery and operations/Recovery Workbench Story Build Order v3.docx` was never edited.
It was converted to text for reading, and the new version was written in full as Markdown and rendered
with `compat/office_write.py md-docx` onto the version 3 file as the template.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules §R8.1. The change-log
   table carries the row `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
   DeepSeek v4.1 Flash`, and the version 3 row records that the source carries no change log, with its
   gap and assumption pair.
2. **Every section, ID, number and date of version 3 kept.** The five windows, the 115 items, every
   key, title, module, E or S flag, waits-on, item number and window date are copied word for word, and
   the opening paragraph, the D-RCV-36 paragraph, the configuration paragraph and the two How-to-use
   paragraphs are kept as they stand. Each window heading and release line is marked `(tentative)`;
   no date is moved and no date is raised as a gap.
3. **Lanes and Ready to start, the two things the realignment needs.** Each item is shown as the
   microservice stories that carry it, one row per story, with the service, the suggested owner of the
   work type, the parallel lane and the Ready to start of that story, read from the story set of the run
   (`_work/msr/fragments`). The item order of version 3 is unchanged; inside an item the order is
   contract, application, database, infrastructure, DevOps, integration (Template and Rules §R5.7). The
   530 story rows carry 460 Day 1 and 70 waiting stories in 282 lanes, of which 92 are contract stories.
4. **Ownership Map for every owner.** The Service column of every story is the service of the Ownership
   Map v1 (P1 to P10, S1 to S9, PLT, ITG) and the Suggested owner column is the team type of the work
   type in Template and Rules §R5.3 (TechX, ACE team, SCB IT infrastructure, DevOps team, QA team), with
   the soft-owner phrase stated in the reading note (U3; DL46).
5. **Retired items.** RWB-E1-014 and RWB-TE-007 keep their number and their place in the order of
   version 3 and carry no story: no data lake (DP-17) and Temporal Schedules in place of Quartz (DP-10),
   with a dependency on RWB-TE-007 repointed to RWB-PLT-E1071-CON (R6). The note sits under the window 2
   realignment table and the count of 57 items is unchanged.
6. **Day-1 summary and the new stories.** A lane and Day-1 section gives the position of the 530 stories
   of the 115 items by team type, and the position of the whole story set of the run (1034 stories, 939
   Day 1, 510 lanes) by wave. A second table lists the platform stories N001 to N012 and the harness and
   journey stories W1J01 to W4J01, which carry no item of version 3, are all Day 1, and sit before
   window 1 because wave 0 is not a release.
7. **Critical path.** The two How-to-use paragraphs are kept word for word, and two paragraphs are
   added: the five team types in place of the two squads, and the same chain in the lane terms of this
   version (L-P1-A, L-P1-R, L-P3-F, L-PLT-WF-D, L-PLT-WF-E, L-PLT-LIB-I, L-P3-W, L-P3-K, L-P3-L,
   L-P10-A, L-P10-F, L-P10-E), with the note that RWB-E1-072 reaches RWB-E1-018 through
   RWB-PLT-E1072-CON and its fake.
8. **Table shape and document properties.** Fourteen tables: the five item tables of version 3
   unchanged, the five realignment tables at eight columns, the team-type and wave summary, the new-story
   table and the change log. Column widths are set and the first row of every table repeats as a header
   row. The core properties carry the organisation and the tool line in place of the person name of the
   template, the v4 title, the D-RCV-60 subject and revision 4, dated 22 November 2026. A byte scan of
   every part of the file finds no person name.
9. **Verification.** The docx was extracted again with `compat/convert_sources.py` and compared with the
   Markdown it was rendered from: 750 lines each, 0 missing and 0 extra, 14 tables with 16, 61, 58, 236,
   22, 101, 20, 122, 4, 15, 7, 7, 21 and 3 rows, and 12 headings. No line carries a person name, an
   e-mail address, the issue tracker or its product name.
10. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp C4-SBO --quick` was run
    and passed: C02, C03 and C05 (story-file checks, no story file in this WP), C12 (no person name, no
    e-mail), C13 (no issue-tracker reference) and C18 (no write outside the WP list, no legacy file
    changed). C14 (header lines), C17 (every CG and ASM citation has a row) and C20 (tool line) were run
    against the same 14 files and also pass.

## Registers

- Gap rows: 9 (`GAP-3237` to `GAP-3245`): Missing 4 (governance 2, documentation 1, planning and
  waves 1), Conflict 1 (governance), Ambiguous 3 (story split, release planning, dependency
  classification), Outdated 1 (documentation). Severity: P3 9. No gap row raises a date.
- Assumption rows: 9 (`ASM-5657` to `ASM-5665`), confidence High 6, Medium 3, Low 0.
- Every missing value in the document is the R9 placeholder with its CG and ASM pair; no lane, no Ready
  to start, no owner, no release date and no story key is invented.

## Not done, by rule

- No approval was sought and none is recorded; the document is issued as Draft.
- No master file was written, no register was numbered, and no other document was edited.
- No issue tracker, Confluence, repository or web call was made, and no commit was created.
