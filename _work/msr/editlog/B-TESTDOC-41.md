# Edit log — WP B-TESTDOC-41 (Recovery Workbench Test Data Plan, next version)

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Sources read

| Source | Used for |
|---|---|
| `09 Testing and quality/Recovery Workbench Test Data Plan v3.docx` | The whole of version 3, read through the converted text `_work/msr/extract/B-TESTDOC-41/Recovery Workbench Test Data Plan v3.md`; every section, row, ID, number and date |
| `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` | R1, R3, R5 (R5.4 dependency classes, R5.5 DP table, R5.7 Day-1 rules), R8 (R8.1 header, R8.2 versioning), R9 (placeholder and jsonl keys) |
| `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` | Sheets Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Rulings — the owner of every element used in sections 2.1, 3.1, 5 and 6 |
| `_work/msr/plan/ownership.json` | The same owners in machine form: 93 tables, 156 endpoints, 30 events, 15 workflows, 22 jobs |
| `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` | Slides 11, 13, 20, 29, 41, 42, 43, 44 and 46 — call types and contract artefacts, schema and login per service, the 19 service contracts, the event and job catalogues, the testing answer |
| `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` | The rule evaluation step in an activity, the rule package test minimum (rules.testcases.min=50), replay and determinism |
| `_work/msr/plan/split_plan.json` | `stats` and `legacy` only, for the wave and story context |
| `_work/msr/plan/ids.json` | The allocated decision, ADR and DL IDs (D-RCV-60, ADR-014, ADR-020, ADR-021, DL44) |

No source file was edited. No issue tracker, wiki, repository, figure library or web call was made.

## Files written

- `09 Testing and quality/Recovery Workbench Test Data Plan v4.docx`
- `_work/msr/docs/B-TESTDOC-41/Recovery Workbench Test Data Plan v4.md`
- `_work/msr/docs/B-TESTDOC-41/template-fixed.docx`
- `_work/msr/docs/B-TESTDOC-41/verify/Recovery Workbench Test Data Plan v4.md`
- `_work/msr/gaps/B-TESTDOC-41.jsonl`
- `_work/msr/assumptions/B-TESTDOC-41.jsonl`
- `_work/msr/editlog/B-TESTDOC-41.md`

Scratch only (`_work/msr/docs/B-TESTDOC-41/`): the full rendered text of the new version, the repaired template copy, the verification extract and eight small helper scripts (`gen_rows.py`, `fix_template.py`, `set_props.py`, `verify_docx.py`, `check_cites.py`, `check_props.py`, `run_extra_checks.py` and the probes). The source was converted for reading into `_work/msr/extract/B-TESTDOC-41/` with `compat/convert_sources.py`, as the WP allows.

## What was done

The source `09 Testing and quality/Recovery Workbench Test Data Plan v3.docx` was never edited. It was converted to text for reading; the new version was written in full as Markdown, then rendered with `compat/office_write.py md-docx` onto a repaired copy of the version 3 template.

1. **Header and change log.** Lines 1 and 2 are the header of Template and Rules R8.1, character for character. The title block keeps its two title lines and adds the version line `Version 4, 22 November 2026. The version 3 text is dated 15 November 2026.` The metadata table keeps every version 3 row (Document, Version, Date, Prepared by, Structure) and adds Decision, Supersedes, Status, Tool and the change-log row `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Section 7 is the change log.
2. **Every section, ID, number and date kept.** Sections 1 to 6 keep their titles and order and are not renumbered. The version 3 numbers are kept character for character: 22 Tier 1 and 14 Tier 2 ACE tables, 92 recovery tables, 4 extension tables, 30 views (16 Section A, 14 Section B), 122 dictionary objects, 1,366 dictionary fields (304 on the views, 49 on the extension tables), 20 removed tables, 2,812 cases (1,226 Mortgage, 1,296 Hire purchase, 290 SSME) plus 10 per exception shape, 184,500 account rows, 28,140 at 90 days past due or more, 21 entry exclusions, 37 case accounts below the threshold, 180 documents, 49 extension columns, seed 20261128, MASK-SIT-01, DF-ACE-073, DF-ACE-074, DF-ACE-078, DF-ACE-079, the date 15 November 2026 and the references RWB-E1-037, RWB-E1-065, RWB-TE-004, RWB-TE-011. The Ownership Map adds the numbers the version 3 text did not have: 19 schemas and logins, 93 tables with 18 per P1 down to 0 for S1, 156 REST operations, 30 events, 15 workflows and 22 jobs.
3. **Synthetic data per schema.** Section 1 restates the seeding model over the 19 schemas `rwb_<service>` and the single reader of the 30 views. Section 2 gains three object groups (19 service schemas, the 6 platform library objects with 4 in every schema, 20 contract fakes) and a new section 2.1 with one row per service: the schema, the table count and names from the Ownership Map, and the synthetic rows that schema holds. Section 6 gains eight count rows for the same facts. The four environment rows of section 1 and all eleven test rows of section 3 keep their names and their data, with the owning service and the fake added.
4. **Contract mocks.** New section 3.1 gives one row per provider (19 services plus gateway-bff): the artefacts it publishes (OpenAPI 3.1 with the REST operation count, AsyncAPI 3.0 with the EV IDs, the activity contract jar or workflow), what the fake serves, and the data it returns. Seven rules follow: generated from the artefact, stateless, 2 s timeout with RFC 9457 errors, CloudEvents on the provider topic with duplicate replay, the activity jar with the Temporal test server and replayed histories, never used where the class is I, and no personal data.
5. **Owners from the Ownership Map.** Section 5 keeps the six version 3 items and their wording and adds a column naming the service and the sheet of the map that records each owner; two rows are added (contract fakes, job and schedule data). Every owner in sections 2.1, 3 and 3.1 is the code of the map.
6. **Masking realigned.** Section 4 keeps its nine points, moves the masking rules to `masking_rule` in rwb_access (P4), states that rwb-source-data (P1) is the only login that reads the views, and adds a point that no personal data crosses a service boundary: events and workflow inputs carry IDs and business facts, and Temporal payloads are encrypted by the codec.
7. **Two source values change, and both are recorded.** The internal Version row (3) becomes 4 under R8.2, and the decision row becomes D-RCV-60 with ADR-014, ADR-020, ADR-021 and DL44; the version 3 decision references are kept in the Supersedes row. Assumptions ASM-3432 and ASM-3433 record the two. The document states no release date, so no date carries a `(tentative)` mark.
8. **Template repair and document properties.** The docx family stores `w:name/@w:val` of the heading styles as `Heading 1`, which `python-docx` looks up as `heading 1`, and it has no `List Bullet` style, so `md-docx --template` would fail on both. `fix_template.py` copies version 3 to the scratch folder, writes the conventional heading names and adds a `List Bullet` style based on `List Paragraph` with the bullet numbering (numId 2) the version 3 bullets use. `set_props.py` replaces the person name in the author and last-modified-by properties with the organisation and the tool, sets the version 4 title and dates the document 22 November 2026 (rule 4). The source file was not touched.
9. **Verification.** The new docx was extracted again with `compat/convert_sources.py` and compared with the rendered Markdown: 9 tables, 111 table rows, 9 headings (7 at Heading 1, 2 at Heading 2), 16 bullets, every paragraph line present, the two header lines first. Document properties carry no person name.

## Rows

- Candidate gaps: 9 rows, `GAP-2132` to `GAP-2140`. Numbered GAP-nnnn in step D1.
- Candidate assumptions: 11 rows, `ASM-3424` to `ASM-3434`. Numbered ASM-nnnn in step D1.
- Every gap has one assumption. Two assumptions (ASM-9, ASM-10) carry no gap: they record the version and decision change and the absence of a release date.
- Confidence: High 7, Medium 4. Severity: P2 5, P3 4.
- Placeholders in the document: one value, the product that hosts the contract fakes (CG-3 / ASM-3), written as `Not specified in the source documents`. The other eight rows are cited where the realignment settles a fact that the sources leave open: the table counts (CG-1), the valuation schema (CG-2), the key set of the fakes (CG-4), the mask owner (CG-5), the per-schema seed (CG-6), the unnumbered events (CG-7), the smoke data set (CG-8) and the platform library placement (CG-9).

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TESTDOC-41 --quick`: C02, C03, C05, C12, C13 and C18 PASS with zero findings. The report is under `22 Microservice Realignment/checks/reports/wp-B-TESTDOC-41-*.md`.
- C14, C15, C16, C17 and C20 over the same file set: PASS with zero findings.
- `check_cites.py`: 20 jsonl rows, 20 citations in the new text, no citation without a row and no row uncited.
- `verify_docx.py`: 9 tables, 111 table rows (equal to the Markdown), 9 headings in order, 16 bullets, 0 missing paragraph lines.

## Failures

None.
