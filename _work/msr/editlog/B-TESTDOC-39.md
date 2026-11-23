# Edit log - WP B-TESTDOC-39 (Recovery Workbench Test Strategy next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `09 Testing and quality/Recovery Workbench Test Strategy v3.docx`

- `_work/msr/docs/B-TESTDOC-39/Recovery Workbench Test Strategy v3.md`

- `_work/msr/docs/B-TESTDOC-39/template-fixed.docx`

- `_work/msr/docs/B-TESTDOC-39/verify/Recovery Workbench Test Strategy v3.md`

- `_work/msr/docs/B-TESTDOC-39/fix_template.py`

- `_work/msr/docs/B-TESTDOC-39/set_props.py`

- `_work/msr/docs/B-TESTDOC-39/verify_docx.py`

- `_work/msr/docs/B-TESTDOC-39/scan_names.py`

- `_work/msr/docs/B-TESTDOC-39/compare.py`

- `_work/msr/docs/B-TESTDOC-39/check_extra.py`

- `_work/msr/docs/B-TESTDOC-39/inspect.py`

- `_work/msr/docs/B-TESTDOC-39/inspect2.py`

- `_work/msr/docs/B-TESTDOC-39/styles.py`

- `_work/msr/docs/B-TESTDOC-39/props.py`

- `_work/msr/docs/B-TESTDOC-39/plan_peek.py`

- `_work/msr/docs/B-TESTDOC-39/plan_peek2.py`

- `_work/msr/docs/B-TESTDOC-39/plan_peek3.py`

- `_work/msr/docs/B-TESTDOC-39/plan_peek4.py`

- `_work/msr/docs/B-TESTDOC-39/own_peek.py`

- `_work/msr/docs/B-TESTDOC-39/services_peek.py`

- `_work/msr/gaps/B-TESTDOC-39.jsonl`

- `_work/msr/assumptions/B-TESTDOC-39.jsonl`

- `_work/msr/editlog/B-TESTDOC-39.md`

Scratch only (`_work/msr/docs/B-TESTDOC-39/`): the full text of the new version, the repaired
template copy, the property writer, the three verification scripts and the small readers used to
count the Ownership Map and the plan. The converted source text was written by the conversion
tool to the extract folder the WP names, `_work/msr/extract/B-TESTDOC-39/`.

## What was done

The source `09 Testing and quality/Recovery Workbench Test Strategy v2.docx` was never edited. It was
never opened for writing: it was copied to the scratch folder as the render template, converted to
text for reading, and the new version was written in full as Markdown and then rendered with
`compat/office_write.py md-docx` onto the repaired copy of the v2 template.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules §R8.1. The metadata
   table keeps every v2 row (Document, Version, Date, Prepared by, Structure) and adds Supersedes
   (Version 2, 28 October 2026), Decision (D-RCV-60), Status (Draft) and the change-log row
   `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.
   Section 12 is a change-log table that carries that row again with the list of what changed.
2. **Every section, number and date of the source kept.** Sections 1 to 7 keep their titles, order and
   content, with the nine test levels, three environments, three gates, the test data paragraph, the
   five "who tests what" rows, the traceability paragraph and the defects paragraph. The figures of the
   source are unchanged: 80 percent line coverage, severity 1, 2 and 3, the SIT week and the UAT week.
   The date 28 October 2026 is kept in the Supersedes row and in change-log row 1. The source states no
   release date, so no `(tentative)` mark was needed; section 3 records that programme release dates are
   unchanged and tentative (R1 U7; DL48).
3. **Contract tests.** New section 8 gives one contract under test per call type with the owner from the
   Ownership Map: OpenAPI 3.1 for REST with RFC 9457 problems, Idempotency-Key, the 2 second timeout and
   one retry on GET only; AsyncAPI 3.0 with the JSON Schema registry in BACKWARD compatibility, the
   CloudEvents envelope, retry topics at 1, 10 and 60 minutes and the dead-letter topic; the Temporal
   contract jar; the file manifest; the 30 `recovery.v_ace_*` views. All of it is taken from Architecture
   v5 slide 11.
4. **Component tests with mocks.** New section 9 defines the level and gives a table of what is real
   (own schema, own topic, workflow kit, embedded Drools) against what is a fake (every other schema,
   every outside producer and consumer, another service's activity, the rule registry) and what each
   pairing proves. It carries the R-UNI-39 one-transaction rule, the `NoPackageInForce` non-retryable
   rule with the JOB-21 scan, the 60 second agent fallback (R-UNI-32), the determinism rules, the replay
   gate E2-040 and the boundary test from Architecture v5 and the Temporal and Drools design.
5. **Integration test group per wave.** New section 10 gives one group per integration epic
   (RWB-ITG-W1 to RWB-ITG-W4) with the services under test from the wave map, the journey story of each
   wave, what the journey proves from the A2 and A3 event catalogues, and the exit. Section 3 adds the
   four wave gates ahead of SIT, UAT and Release, and section 10 keeps the daily smoke workflow JOB-22.
6. **Ownership Map used for every owner.** Section 11 is a test scope table of all 20 owner codes with
   the tables, REST operations, events, workflows and jobs the map assigns, counted from
   `_work/msr/plan/ownership.json` and checked against the sheets of the Ownership Map v1. Sections 5, 8
   and 9 read the test owner and the fake owner from the contract owner. The map gives S1 rwb-valuation no
   table row, which is recorded as GAP-2123.
7. **Epic 1 preservation.** Section 6 states that the six preserved Epic 1 stories keep their as-built
   section 16 test cases word for word and the microservice tests sit on the delta and CON stories
   (R6; DL47; U2).
8. **Template repair and document properties.** The family stores `w:name/@w:val` as `Heading 1`, which
   `python-docx` looks up as `heading 1`, so `md-docx --template` fails with
   `KeyError: no style with name 'Heading 1'`; the family also has no `List Bullet` style. The scratch
   `fix_template.py` repairs the copy only, and the source is untouched. The family also carries a person
   name in the author and last-modified-by properties; `set_props.py` replaces both with the organisation
   and the tool, sets the v3 title, subject, category, comment and revision 3, and dates the document
   22 November 2026 (AGENTS.md rule 4). A byte scan of all 16 parts of the new docx finds no person name
   and no e-mail address.
9. **Verification.** The docx was extracted again with `compat/convert_sources.py`; the rendered Markdown
   and the extracted text match line for line (127 normalised lines each, 0 missing, 0 extra), with 10
   tables and 14 headings: the two title lines, sections 1 to 12 and the metadata table.
10. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TESTDOC-39 --quick` was
    run and passed: C02, C03, C05 (story-file checks, no story file in this WP), C12 (no person name, no
    e-mail), C13 (no issue-tracker reference) and C18 (no write outside the WP list, no legacy file
    changed). C14 (header lines), C17 (every CG and ASM citation has a row) and C20 (tool line) were run
    against the same file set and also pass.

## Registers

- Gap rows: 8 (`GAP-2116` to `GAP-2123`): Conflict 2 (documentation, data),
  Missing 4 (governance, test approach, environments, test design), Outdated 1 (test approach),
  Ambiguous 1 (test approach). Severity: P2 1 (the rwb_valuation table assignment), P3 7. No gap row
  raises a date.
- Assumption rows: 8 (`ASM-3401` to `ASM-3408`), confidence High 2, Medium 6, Low 0.
- Every missing value in the document is the R9 placeholder with its CG and ASM pair; no business value,
  owner, count or date is invented - the counts of section 11 are the rows of the Ownership Map v1.

## Not done, by rule

- No approval was sought and none is recorded; the document is issued as Draft.
- No master file was written, no register was numbered, and no other document was edited.
- No issue tracker, Confluence, repository or web call was made, and no commit was created.
