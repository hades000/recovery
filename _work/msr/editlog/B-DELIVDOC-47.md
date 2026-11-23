# Edit log - WP B-DELIVDOC-47 (Recovery Workbench Run Operating Model next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `11 Delivery and operations/Recovery Workbench Run Operating Model v3.pptx`
- `_work/msr/docs/B-DELIVDOC-47/build_v3.py`
- `_work/msr/docs/B-DELIVDOC-47/tune.py`
- `_work/msr/docs/B-DELIVDOC-47/write_jsonl.py`
- `_work/msr/docs/B-DELIVDOC-47/set_props.py`
- `_work/msr/docs/B-DELIVDOC-47/verify/Recovery Workbench Run Operating Model v3.md`
- `_work/msr/docs/B-DELIVDOC-47/verify2/Recovery Workbench Run Operating Model v3.md`
- `_work/msr/docs/B-DELIVDOC-47/verify3/Recovery Workbench Run Operating Model v3.md`
- `_work/msr/docs/B-DELIVDOC-47/render/Recovery Workbench Run Operating Model v3.pdf`
- `_work/msr/docs/B-DELIVDOC-47/render/slide01.png` to `_work/msr/docs/B-DELIVDOC-47/render/slide19.png`
- `_work/msr/docs/B-DELIVDOC-47/render/check08.png`
- `_work/msr/gaps/B-DELIVDOC-47.jsonl`
- `_work/msr/assumptions/B-DELIVDOC-47.jsonl`
- `_work/msr/editlog/B-DELIVDOC-47.md`

Scratch only (`_work/msr/docs/B-DELIVDOC-47/`): the build script, the font-tuning script, the register
writer, the two text extractions of the finished deck and the PDF and PNG renders used to check the
layout. The converted source text was written by the conversion tool to the extract folder the WP names,
`_work/msr/extract/B-DELIVDOC-47/`.

## What was done

The source `11 Delivery and operations/Recovery Workbench Run Operating Model v2.pptx` was never edited.
It was converted to text for reading and copied to version 3 with `compat/office_write.py copy`, and the
new content was added to the copy.

1. **Header and change log.** The first two text lines of slide 1 are the header of Template and Rules
   §R8.1, and the footer of slide 1 carries the change-log row
   `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
   Slide 19 is a change-log table with the same row and with version 2 recorded as the source row, and
   slide 7 opens the deck's arguments with the same row plus the Draft status. No date is raised as a gap.
2. **Every slide, ID, number and date of the source kept.** Slides 2 to 6 (who runs the Workbench, the
   four service levels, hours and shifts, escalation, and the DL02 decision) are copied and were checked
   line for line against the source extraction: identical. The dates 28 October 2026, the times 08:00,
   20:00, 05:00, 07:00 and 09:00, the respond and restore times of 15 minutes, 4 hours, 1 hour and 1
   working day, DL02, and the role names of the source are all kept. The source states no release date,
   so the deck states that the release dates are unchanged and tentative (U7; DL48) on slides 7 and 18
   instead of inventing one.
3. **Run book per service, the only change the realignment needs.** Slides 8 to 17 add: the service
   shape and the waves (slide 8), the eight run-book steps that every service follows (slide 9), one row
   per service for P1 to P5, P6 to P10, S1 to S5 and S6 to S9 with its schema, task queue, topic, the
   workflows and Schedules it runs and what to look at first (slides 10 to 13), the run book of the
   shared platform (slide 14), the owners (slide 15), the hours and rota (slide 16), the escalation
   (slide 17), the new decisions (slide 18) and the change log (slide 19). Every value on those slides is
   taken from the Architecture v5 text extract (slides 12 to 20, 34 and 44), the Temporal and Drools
   design text extract, the Ownership Map v1 Services sheet and Template and Rules R4, R5.3, R5.4, R5.6,
   R5.7 and R8.4. Nothing is invented: the service shorthands, schemas, REST bases, topics, task queues
   and waves are copied character for character from the Ownership Map.
4. **Ownership Map for every owner.** Slide 15 names the map owners: the service code for services,
   tables, endpoints, events, workflows and jobs; P3 rwb-case for parameters and reference data and the
   case list API; P7 rwb-decision for the rule package registry; P1 rwb-source-data for the interaction
   ledger; the platform library for feature flags and for the outbox, inbox and idempotency tables, with
   the admin paths served by P2 rwb-integration. Slides 10 to 13 carry the service code as the owner of
   every row, and the service owner for the run remains the open value.
5. **New decisions use the IDs of `_work/msr/plan/ids.json`.** Slide 18 carries D-RCV-60 and DL44 to DL49
   with the positions of Template and Rules §R8.4; no ID outside that file is used, and the one decision
   of the source, DL02, is kept unchanged on slide 6 and is not renumbered.
6. **Format and layout.** The deck was built with `python-pptx` on the copy: the design shapes of slide 2
   (title, rule line, page number) were cloned onto each new slide so the deck looks like one document,
   and each table keeps the source's table style, header fill, purple header text and grey row rules.
   Row heights are estimated from the text so that no table is cramped and none runs past the page. Every
   new slide was rendered to PDF and PNG with LibreOffice and read back; slide 1, 7, 8, 9, 10, 11, 12,
   13, 14, 15, 16, 17 and 19 were checked by eye for overlap, truncation and legibility.
7. **No person name, no e-mail, no issue tracker.** The deck was scanned after the build: every character
   is ASCII, there is no person name, no e-mail address and no issue-tracker reference, and the tool line
   is the one allowed for this run. The bullet glyph of the draft became a bold lead-in phrase instead of
   a character, so the deck carries no non-ASCII character at all. The document properties of the copy
   carried the name of a person from the source file; `set_props.py` replaces the author and last-modified
   by with the organisation and the tool line, sets the title to version 3, the subject to D-RCV-60, the
   revision to 3, the modified date to 22 November 2026 and the change-log row as the description. A byte
   scan of all parts of the new file then found no person name, no e-mail address and no other tool name.
8. **Verification.** The finished deck was extracted twice with `compat/convert_sources.py`. Slide 1
   starts with the §R8.1 header lines; slides 2 to 6 match the source extraction line for line; the file
   has 19 slides and 303 lines of extracted text; the CG and ASM citations in the deck all resolve to a
   register row.

## Registers

- Gap rows: 7 (`GAP-0309` to `GAP-0315`). Types: Missing 7. Areas: governance 4,
  infrastructure 1, documentation 2. Severity: P2 3, P3 4. No gap row raises a date.
- Assumption rows: 7 (`ASM-0401` to `ASM-0407`). Confidence: High 2, Medium 5,
  Low 0. Each gap row names its assumption and each assumption names its gap.
- Every missing value in the deck is the R9 placeholder with its CG and ASM pair: the run-time service
  owner (CG/ASM-1) on slides 10 to 13 and 15, the tier roles per service (CG/ASM-2) on slide 15, the
  alert thresholds and dashboard (CG/ASM-3) on slide 9, the per-service rota (CG/ASM-4) on slides 14 and
  16, the change history and tool line of the source (CG/ASM-5) on slides 7 and 19, the missing run book
  of the source (CG/ASM-6) on slide 8, and the approval and status (CG/ASM-7) on slide 7.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DELIVDOC-47 --quick` was run and
passed: C02, C03 and C05 (story-file checks; this WP writes no story file), C12 (no person name, no
e-mail), C13 (no issue-tracker reference) and C18 (no write outside the WP list, no legacy file changed).
C14, C15, C17 and C20 were also run against the same file set and pass: the header lines, the tentative
release statement, every CG and ASM citation having a row, and the tool line.

## Not done, by rule

- No approval was sought and none is recorded; the deck is issued as Draft.
- No master file was written, no register was numbered, and no other document was edited.
- No issue tracker, Confluence, repository or web call was made, and no commit was created.
