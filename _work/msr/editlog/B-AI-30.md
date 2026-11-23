# Edit log - WP B-AI-30 (Recovery Workbench Model Integration Design, next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `08 AI and agents/Recovery Workbench Model Integration Design v3.docx`

- `_work/msr/docs/B-AI-30/Recovery Workbench Model Integration Design v3.md`

- `_work/msr/docs/B-AI-30/template-fixed.docx`

- `_work/msr/docs/B-AI-30/fix_template.py`

- `_work/msr/docs/B-AI-30/set_props.py`

- `_work/msr/docs/B-AI-30/strip_backticks.py`

- `_work/msr/docs/B-AI-30/verify/Recovery Workbench Model Integration Design v3.md`

- `_work/msr/gaps/B-AI-30.jsonl`

- `_work/msr/assumptions/B-AI-30.jsonl`

- `_work/msr/editlog/B-AI-30.md`

Scratch only (`_work/msr/docs/B-AI-30/`): the full rendered text of the new version, the repaired template copy, three small helper scripts, and the round-trip extract used to verify the docx. The source was also converted to text for reading into `_work/msr/extract/B-AI-30/` with `compat/convert_sources.py`, as the WP allows under "Read only".

## What was done

The source `08 AI and agents/Recovery Workbench Model Integration Design v2.docx` was never edited. It was converted to text for reading, and the new version was written in full as Markdown, then rendered with `compat/office_write.py md-docx` onto a copy of the v2 template.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules R8.1. The title block keeps the two title lines, the metadata table keeps the v2 rows (Document, Version, Date, Prepared by, Structure) and adds Decision, Supersedes, Status, Tool and the change-log row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Section 6 holds a change-log table with the same row and the list of what changed.
2. **Every section, ID, number and date kept.** Sections 1 to 5 keep their titles and order and are not renumbered. Every model inventory ID is copied character for character (CRR_RET_353, 376, 334, 203, 313, 323, 349, 350, 340, 346, 345, 366, 356, 355, 285, 351, 372, 373, 380, 392, 393, 371, 370), and INT-08, DL33, DP11, D5.1, D5.2 and the 28 October 2026 date are kept. The document carries no release date, so no `(tentative)` mark was needed.
3. **Model calls only from rwb-agent activities.** Section 1 names rwb-agent (P10) as the agent platform of DL33 and states that the only caller of the model endpoint is an activity on the rwb-agent task queue; section 4 restates the four v2 points against INT-23, AgentRunWorkflow, the 60-second rule fallback (R-UNI-32, DL11), the tool gateway and the run records.
4. **Owners from the Ownership Map.** The score and the `v_ace_score` view are rwb-source-data (P1); the model ID and version on a decision sit in the owning service's decision record and the central ledger of rwb-decision (P7); the prompt, policy and run records are rwb-agent (P10); the approvals are P7; the agent tables are P10. The three monitoring roles of v2 stay word for word and gain the data owner of each measure.
5. **Two source values change, and both are recorded.** The internal Version row (1) becomes 3 under R8.2, and the v2 title-block date line becomes the version 3 line that still carries 28 October 2026; both are GAP-0079. Everything else of the source wording is kept verbatim: 46 of the 48 non-blank lines of the v2 extract appear unchanged in the new text.
6. **Template repair and document properties.** The docx family stores `w:name/@w:val` as `Heading 1`, which `python-docx` looks up as `heading 1`, and it has no `List Bullet` style, so `md-docx --template` fails on both. `fix_template.py` copies the v2 file to the scratch folder, writes the conventional Word heading names and adds a `List Bullet` style based on `List Paragraph` with the bullet numbering (numId 2) the v2 document uses. `set_props.py` replaces the person name in the author and last-modified-by properties with the organisation and the tool, sets the v3 title and dates the document 22 November 2026 (rule 4). The source file was not touched.
7. **Verification.** The new docx was extracted again with `compat/convert_sources.py` and compared line by line with the rendered Markdown: identical apart from the extract's own table separator row. 8 tables, 23 bullets (no duplicated bullet), the 6 section headings at Heading 1, and the two header lines are present.
8. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-AI-30 --quick` was run until it passed: C02, C03, C05 (story-file checks, no story file in this WP), C12 (no person name, no email address), C13 (no issue-tracker reference) and C18 (no write outside the WP list, no legacy file changed).

## Registers

- Gap rows: 7, `GAP-0079` to `GAP-0085`, all P3: Governance 1, AI and agents 4, Data 1, Integration 1.
- Assumption rows: 9, `ASM-0139` to `ASM-0147`: confidence High 5, Medium 4.
- Every placeholder in the document cites a gap row and an assumption row that exist; no value is invented and no date is raised as a gap.

## Not done, by rule

- No approval was sought and none is recorded; the document is Draft.
- No master file was written, no register was numbered, no other document was edited, and no issue tracker or external system was called.
