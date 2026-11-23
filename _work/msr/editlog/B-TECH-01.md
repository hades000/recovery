# Edit log - WP B-TECH-01 (ACE Architecture Decision v-next)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `05 Technical architecture/Recovery Workbench ACE Architecture Decision v4.docx`

- `_work/msr/docs/B-TECH-01/Recovery Workbench ACE Architecture Decision v4.md`

- `_work/msr/docs/B-TECH-01/template-fixed.docx`

- `_work/msr/docs/B-TECH-01/fix_template.py`

- `_work/msr/docs/B-TECH-01/set_props.py`

- `_work/msr/docs/B-TECH-01/verify/Recovery Workbench ACE Architecture Decision v4.md`

- `_work/msr/docs/B-TECH-01/verify2/Recovery Workbench ACE Architecture Decision v4.md`

- `_work/msr/gaps/B-TECH-01.jsonl`

- `_work/msr/assumptions/B-TECH-01.jsonl`

- `_work/msr/editlog/B-TECH-01.md`

Scratch only (`_work/msr/docs/B-TECH-01/`): the full rendered text of the new version, the repaired
template copy, the two small scripts, and the two round-trip extracts used to verify the docx.

## What was done

The source `05 Technical architecture/Recovery Workbench ACE Architecture Decision v3.docx` was never
edited. It was converted to text for reading, and the new version was written in full as Markdown, then
rendered with `compat/office_write.py md-docx` onto a copy of the v3 template.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules R8.1. The metadata table
   keeps the v3 rows (Document, Version, Date, Prepared by, Structure) and adds Supersedes (version 3,
   15 November 2026), Decision (D-RCV-60), Status (Draft) and the change-log row
   `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
   Section 10 holds that row again in a change-log table with the list of what changed.
2. **Every section, ID, number and date kept.** Sections 1 to 9 keep their titles and order, with 3.1 to 3.4
   and the new 1.1, 5.1 and 5.2. Every ID of v3 is still present (DT02, DT07 to DT11, DL03 to DL07, DL37,
   DL43, D-RCV-35, RWB-ACE-001, ADR-010), and every figure (90 days, 366 of 448 routing rules, 448 rules in
   10 route sets, 22 Tier 1 tables and 16 views, 14 Tier 2 tables and 12 columns and 14 views, 4 extension
   tables, 88 Workbench tables, 92 tables, 122 objects, 1,366 fields, 108 tables, 1,256 fields, 30 views,
   80 fields), and every date (29, 30 and 31 October 2026, 6 and 21 November 2026, October 2026,
   15 November 2026, 2 November). No release date appears in this document, so no `(tentative)` mark was
   needed.
3. **The decision changes to 19 services inside ACE.** Section 1 states 19 services, one per business
   module, with one schema, login, repository and pipeline each, gateway-bff composing the screens, and
   Temporal running the case as a parent CaseWorkflow with a child workflow per stage. Section 2 records
   that ADR-013 supersedes ADR-002, the single-service decision, and keeps every reason for staying inside
   ACE. New section 1.1 lists ADR-013 to ADR-023 with the sections each one changes, using the IDs of
   `_work/msr/plan/ids.json`, and names DL44 to DL49.
4. **Workflow section realigned.** 3.1 keeps its four options and six criteria; the option 3 column and the
   verdict row are rewritten for rows plus durable timers and a stage per child workflow. 3.2 and 3.4 are
   restated for a shared Temporal layer, Schedules in the owning service instead of Quartz, outbox and
   inbox on Kafka, embedded Drools per service and a local decision record with a central ledger. The CMMN
   model, the row-based case state and the 366-of-448 argument are unchanged. The restatement is
   recorded as GAP-1981 and ASM-3202.
5. **Structure and data sections.** Section 4 replaces the modular-monolith option with 19 services by
   module from one template, and keeps the written exception for the `recovery.v_ace_*` views and adds the
   Temporal Nexus call to the ACE restructure calculator. Section 5 keeps every tier and figure and adds
   5.1, the 19 schemas with their owner code, wave and content from the Ownership Map and the Architecture
   v5 service catalogue, and 5.2, per-service Flyway and the four extension tables in `rwb_source_data`.
6. **Consequences and open points.** Section 7 keeps the six rows of v3 and adds Rules, Reporting and
   Observability, each carrying its ADR. Section 8 keeps all seven open points, their proposed answers and
   every due date; the six rows that named an individual now carry the R9 placeholder with the
   organisation the row already stated kept after it. Section 9 keeps the five roles and their v3 statuses
   word for word, with a note that version 4 has no approval round.
7. **Template repairs and document properties.** The docx family stores `w:name/@w:val` as
   `Heading 1`, which `python-docx` looks up as `heading 1`, so `md-docx --template` failed with
   `KeyError: no style with name 'Heading 1'` on every document of this family. The family also has no
   `List Bullet` style, so `add_paragraph(text, style="List Bullet")` appended the paragraph and then
   raised, and the fallback appended a second, prefixed copy of every bullet. `fix_template.py` copies
   the v3 file to the scratch folder, writes the conventional Word value `heading 1`, and adds a
   `List Bullet` style based on `List Paragraph` with the bullet numbering (numId 3) the v3 document
   uses for its own lists. The rendered document keeps the v3 styles, section properties and page setup,
   and Word still shows the styles as Heading 1 and List Bullet. The source file was not touched. The
   template also carried a person name in the author and last-modified-by properties; `set_props.py`
   replaces both with the organisation and the tool, sets the v4 title, and dates the document
   22 November 2026 (rule 4). The docx was extracted again after the property write and matches the
   rendered Markdown line for line: 167 non-blank lines, 12 tables, 15 bullets, no duplicated bullet.
8. **Verification.** The docx was extracted again with `compat/convert_sources.py` and compared to the
   rendered Markdown: header lines, metadata table, all nine sections, 1.1, 3.1 to 3.4, 5.1 and 5.2,
   section 10, and every table row are present.
9. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-01 --quick` was run
   until it passed: C02, C03, C05 (story-file checks, no story file in this WP), C12 (no person name, no
   email address), C13 (no issue-tracker reference) and C18 (no write outside the WP list, no legacy file
   changed).

## Registers

- Gap rows: 6 (`GAP-1978` to `GAP-1983`), all P3: governance 2, workflow 1, delivery 2, data 1.
- Assumption rows: 6 (`ASM-3199` to `ASM-3204`), confidence High 1, Medium 4, Low 1.
- No gap row raises a date, and no value is invented: every missing value is the R9 placeholder.

## Not done, by rule

- No approval was sought and none is recorded; the document is Draft.
- No master file was written, no register was numbered, and no other document was edited.
