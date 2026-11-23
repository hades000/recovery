# Edit log - WP B-TESTDOC-42 (Recovery Workbench Definition of Ready and Done next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work pack: B-TESTDOC-42. Fanout: 0 (one worker, no subagents).

Sources read: `09 Testing and quality/Recovery Workbench Definition of Ready and Done v3.docx`, converted with
`compat/convert_sources.py` to `_work/msr/extract/B-TESTDOC-42` (5 sections, 10 tables, 20 ready items, 20 done
items); `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3,
§R5, §R8, §R9); `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice
Ownership Map v1.xlsx` (sheets Read me, Services, Tables, Endpoints, Events, Workflows and activities, Jobs,
Parameters, Rulings); `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides
11, 29, 41, 46); `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`
(contract jars, replay gate E2-040, RecordAndApply, JOB-14 chain check); `_work/msr/plan/split_plan.json` (stats and
legacy only) and `_work/msr/plan/ids.json`. Nothing read was edited.

## Files written

- 09 Testing and quality/Recovery Workbench Definition of Ready and Done v4.docx
- _work/msr/docs/B-TESTDOC-42/Recovery Workbench Definition of Ready and Done v4.md
- _work/msr/docs/B-TESTDOC-42/build.py
- _work/msr/docs/B-TESTDOC-42/template-fixed.docx
- _work/msr/docs/B-TESTDOC-42/write_rows.py
- _work/msr/docs/B-TESTDOC-42/verify.py
- _work/msr/docs/B-TESTDOC-42/probe_checks.py
- _work/msr/gaps/B-TESTDOC-42.jsonl
- _work/msr/assumptions/B-TESTDOC-42.jsonl
- _work/msr/editlog/B-TESTDOC-42.md

Scratch only under `_work/msr/docs/B-TESTDOC-42/`: the full text of v4 as Markdown, the template copy, the build
script, the register-row script and the two verification scripts. The converted source text sits in
`_work/msr/extract/B-TESTDOC-42`, and the round-trip extract of the new file in
`_work/msr/docs/B-TESTDOC-42/roundtrip`. The v3 document was never edited: its SHA-256 still matches
`_work/msr/plan/baseline.json` (check C01 PASS).

## 1. How the next version was produced

The source was never opened for writing. Its full text was written to
`_work/msr/docs/B-TESTDOC-42/Recovery Workbench Definition of Ready and Done v4.md` and rendered with
`compat/office_write.py md-docx` onto a repaired **copy** of the v3 document as the style template, so the new
version keeps the v3 section properties, page setup, footer and styles.

The WP's direct command was tried first and failed, as it has for this document family: the family stores the
built-in heading style names as `Heading 1`, which `python-docx` looks up as `heading 1`, and it has no
`List Bullet` style, so `md-docx --template` stops with `KeyError: no style with name 'Heading 1'`. `build.py`
repairs the scratch copy only (canonical style names, and a `List Bullet` style based on `List Paragraph` with the
`numId 2` list the family uses) and then renders. The v3 file itself is byte-for-byte unchanged.

**Look.** `build.py` gives every table the look of the source: 9638 twips wide, fixed layout, thin single borders,
a `DCD3EB` header row in bold `4E297F` at 9 pt, an `EEEAF6` body at 9 pt in `1F1F1F`, repeated header row, and
column widths proportional to the longest cell of each column. The two title lines take the source sizes, 26 pt and
17 pt. Paragraphs removed by `md-docx` are the v3 body only; the section properties and the footer come from the
template copy.

**Document properties.** The v3 file carries a person name in `author` and `last_modified_by`; the new file is set
to `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title
`Recovery Workbench Definition of Ready and Done v4`, revision 4, created 28 October 2026, modified 22 November
2026. No person name remains in the file.

**Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules §R8.1. The
metadata table carries the source rows unchanged and adds `Family version of this copy | 4`, `Decision | D-RCV-60
microservice realignment` and `Status | Draft. No approval is recorded for this version (ASM-3444)`. The
change-log row reads `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`.

**One version conflict.** The v3 metadata table reads `Version | 2` and `Date | 28 October 2026` while the file
name reads v3. The file name is taken as the family version, so this copy is version 4; both source readings stay in
the table as written (GAP-2141; ASM-3435).

## 2. Fidelity to v3

| Item | Result |
|---|---|
| Sections | 1, 1.1, 2, 2.1, 2.2, 2.3, 3, 3.1, 3.2, 3.3, 3.4, 3.5, 4, 5, 5.1, 6 - the five source sections in order, with 1.1, 2.3, 3.5, 5.1 and 6 added |
| Ready and done items of the source | All 20 of section 2 and all 20 of section 3, with their numbers and labels |
| Source table rows changed on purpose | 10 of 69 rows: the Ready and Done gate rows, ready item 8, done items 1, 5, 9, 12 and 18, and the two section 5 rows |
| Source table rows otherwise verbatim | 59 |
| Source paragraphs present verbatim | All except the repeated date line of the cover, which the R8.1 header lines replace |
| Tables | 16 (10 of the source, 6 new) |
| Header lines 1 and 2 | Present, as the first two paragraphs |
| Change-log row with D-RCV-60 and the tool line | Present |
| Unresolved CG/ASM citations | 0 of 21 |

No number, ID or date of the source is changed: the 20 + 20 item numbers, the seven gate rows, the nine pipeline
gates, the five section 4 rows, DL09, DL10, DL37, R-UNI-39, E2-040 and the date 28 October 2026 are all as written.
The document states no release date, so none is marked tentative and none is raised as a gap (ASM-3445).

## 3. What v4 changes, and why

The change set is the realignment only: **Ready is the published contract; Done is the contract and boundary tests
green**, and every owner comes from the Ownership Map.

1. **Gate table.** The Ready row and the Done row now name the new sections 2.3 and 3.5 as part of their condition
   (GAP-2143, GAP-2144).
2. **Table 1.1, owners.** The 19 services of Architecture v5 with wave, schema and REST base from the Ownership Map
   v1 sheet Services, and the suggested owner team of R5.3. This is the owner reference the rest of the document
   uses (GAP-2142; ASM-3436).
3. **Ready, item 8 and section 2.3.** The contract is published before code as an OpenAPI 3.1 document, an
   AsyncAPI 3.0 document and an activity jar in the Service Contract Catalog v1, with a fake of the same version;
   the story states the version it builds against; ownership of every table, endpoint, event, workflow and job is
   named from the map; Ready to start follows R5.7 (Architecture v5 slide 11; R5.4; DP-11).
4. **Ready, items 17, 19, 20.** A class C dependency never blocks because the consumer builds against the contract
   and its fake; test data is one data set per schema; parameters and reference data come through
   RWB-P3-E1042-CON and RWB-P3-E1043-CON (DP-06, DP-07).
5. **Done, items 1, 2, 5, 9, 12.** The code is merged in the service's own repository; the contract tests and the
   boundary test are named among the nine gates; the exception path is a failed decision record write where the
   record, the state change and the outbox row are one transaction (R-UNI-39); the decision record is written in the
   owning schema and sealed in the central ledger with the JOB-14 chain check; the story touches one service and one
   schema, with a green boundary test (Architecture v5 slide 29; DP-01, DP-03).
6. **Done, item 18.** The tracker row keeps the pull request and merged commit requirement, names no tracker record
   and points at the separate impact and follow-up file (U6; GAP-2147).
7. **Done, section 3.5.** Items 21 to 27: contract tests green, boundary test green, event compatibility, replay
   test, decision record test, version published, fake retired (Architecture v5 slides 11, 29 and 46; E2-040).
8. **Sections 4 and 5.** Four rows for a contract or a boundary failure, and two definitions with their owners for
   contract publication and the boundary test (GAP-2149).
9. **Section 6.** Eight change rows, each with its where, the v3 state, the v4 state and the basis.

## 4. Owners

Every owner is read from the Ownership Map v1 and the Template and Rules: the 19 services and their schemas and
REST bases (sheet Services), the two contracts of the Parameters row (RWB-P3-E1042-CON, RWB-P3-E1043-CON), and the
suggested owner team per work type (R5.3: TechX, ACE team, SCB IT infrastructure, DevOps team, QA team, each with
the fixed phrase "suggested; any team may pick up this story"). No owner is a person and no person is named.

## 5. Registers

- Gap rows written: **10** candidate rows, `GAP-2141` to `GAP-2150`, in
  `_work/msr/gaps/B-TESTDOC-42.jsonl`: 7 Missing, 1 Conflict, 1 Ambiguous, 1 Outdated; 3 of severity P2 and 7 of
  P3; needed by wave 0 (3 rows) and wave 1 (7 rows).
- Assumption rows written: **15** candidate rows, `ASM-3435` to `ASM-3449`, in
  `_work/msr/assumptions/B-TESTDOC-42.jsonl`: 11 High and 4 Medium confidence.
- Ten assumptions answer a gap one for one (ASM-1 to ASM-9 and ASM-14), and each of the ten gaps names its
  assumption. Five carry no gap (ASM-10 to ASM-13 and ASM-15): the draft status, the dates, the numbering of the
  added items, the kept decision-log identifiers, and the added change section.
- Every citation in the document resolves to a row: 21 distinct CG/ASM citations, 0 unresolved. Numbering to
  GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TESTDOC-42 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

Also run directly on this WP's own files: C01 PASS (the v3 source and the story masters are unchanged), C14 PASS
(header lines first), C17 PASS (every gap and assumption row has its required keys and all 21 citations resolve),
C20 PASS (tool line). C19 reports only the outputs of other work packs that have not run yet; both B-TESTDOC-42
expected outputs exist.

`verify.py` reports PASS on: header lines 1 and 2 as the first two paragraphs, the D-RCV-60 change-log row, section
headings 1 to 6 in order with 1.1, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5 and 5.1, 16 tables, the 19 service codes
of table 1.1, all 20 + 20 source item numbers kept, 21 citations, no issue-tracker name, no email address, no person
name, no replacement character, and document properties set to the organisation and the tool. The round-trip
extract of the new file was read back and matches the Markdown.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded in this run (ASM-3444). No later lifecycle
stage was started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created.
No other document of folder 09 was touched.
