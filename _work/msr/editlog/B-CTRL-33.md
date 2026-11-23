# Edit log - WP B-CTRL-33 (Recovery Workbench Records Retention and Archiving next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `10 Policy, controls and compliance/Recovery Workbench Records Retention and Archiving v2.docx`, converted
with `compat/convert_sources.py` to `_work/msr/extract/B-CTRL-33` (all four sections, three tables, 16 retention rows);
`22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (R1, R3, R5, R8, R9);
`_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`
(Services, Tables, Endpoints and the retention ruling); `22 Microservice Realignment/Recovery Workbench Architecture v5
Text Extract v1.md` (slides 11, 16, 20, 37, 41, 44); `22 Microservice Realignment/Recovery Workbench Temporal and Drools
Design Text Extract v1.md`; `_work/msr/plan/split_plan.json` (stats and legacy only) and `_work/msr/plan/ids.json`.
Read for target values only: Physical Schema v6 (recovery_case.legal_hold, retention_rule, retention_action, document),
Logical Data Model v8 (data product per table, LOV-RETENTION), FSD P5 Document hub v3 (A2.17, JOB-17, RET-2026.11),
Event and Messaging Design v4 (no retention event), Decision Log v10 (DL26, DL27). Nothing read was edited.

## Files written

- 10 Policy, controls and compliance/Recovery Workbench Records Retention and Archiving v3.docx
- _work/msr/gaps/B-CTRL-33.jsonl
- _work/msr/assumptions/B-CTRL-33.jsonl
- _work/msr/editlog/B-CTRL-33.md

Scratch files under `_work/msr/docs/B-CTRL-33/` (build and verification only, not outputs of the run): the full text of
version 3, the repaired template copy, the build script and the verification script. The converted source text sits in
`_work/msr/extract/B-CTRL-33`, and the round-trip extract of the new file in the scratch `roundtrip3` folder.

## 1. How the next version was produced

The source was never edited. The full text of version 3 was written to
`_work/msr/docs/B-CTRL-33/Recovery Workbench Records Retention and Archiving v3.md` and rendered onto a scratch copy of
the v2 document with `compat/office_write.py md-docx --template`, so the new version keeps the v2 section properties,
page setup, footer and styles.

**Template repair, in the scratch copy only.** This family stores the built-in heading style names as `Heading 1`, which
`python-docx` looks up as `heading 1`, and it has no `List Bullet` style. `build.py` repairs the copy (canonical style
names, and a `List Bullet` style based on `List Paragraph` with the `numId 2` list the v2 bullets use) and then
renders. The v2 file is byte-for-byte unchanged.

**Table look.** `md-docx` creates plain tables. `build.py` gives each table the look of the source: 9638 twips wide,
fixed layout, thin single borders, a shaded `DCD3EB` header row in bold `4E297F` at 9 pt, repeated header, and column
widths proportional to the longest cell of each column, normalised to the text width so a six-column table fits the page.

**Document properties.** The v2 file carries a person name in `author` and `last_modified_by`. The new file is set to
`Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Records Retention and Archiving
v3`, revision 3, modified 22 November 2026 (rule 4).

**Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules R8.1. The metadata
table carries the change row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek
v4.1 Flash`, a `Source version` row `1, 28 October 2026`, a `Delivery model` row and the `Status` row `Draft. No approval
is recorded for this version (ASM-0270)`.

**One version conflict.** The source metadata table reads `Version | 1` and `Date | 28 October 2026`, while the file
name reads v2. The file name is taken as the family version, so this document is version 3, and both source readings stay
in the document (GAP-0177; ASM-0261).

## 2. Fidelity to version 2

| Item | Result |
|---|---|
| Unique non-empty lines of version 2 | 45 |
| Lines of version 2 present verbatim in version 3 | All, except the metadata `Version` and `Date` rows and the decision-log archive cell, which are the intended changes |
| Lines of version 2 not found and not listed as changed | 0 |
| Sections | 1 to 4 in the order of the source, then 1.1, 2.1, 3.1, 4.1, 5, 6 and 7 added |
| Tables | 10 (3 of the source, 7 new) |
| Header lines 1 and 2 | Present, as the first two paragraphs |
| Change-log row with D-RCV-60 and the tool line | Present |
| Unresolved CG/ASM citations | 0 of 24 |

Every retention period, every reason, the 16 record rows, the three stage rows and the seven bullet rules of the source
are kept character for character. The source carries no release date, so none is added and nothing is marked tentative;
the source date of 28 October 2026 is kept and read as tentative (ASM-0272; DL48).

## 3. What version 3 changes, and why

The change set is the realignment only: retention stated per schema, and every owner read from the Ownership Map.

1. **A schema column.** Section 1 keeps its five columns and adds a sixth, `Owning schema and service`. A record the
   source lists under two data products is named against both schemas, for example account in `rwb_source_data` (P1) and
   money in `rwb_payment` (P8) (GAP-0185; ASM-0269).
2. **Retention by schema.** Section 1.1 reads the same periods one schema at a time, 19 rows, one per service of
   Architecture v5, with the wave of each service (ADR-013, ADR-014; DP-01). No period is invented: three schemas that
   hold only tables with no data-product row carry the placeholder (GAP-0180; ASM-0264).
3. **The decision log.** The 10-year period and the reason stay; the archive rule becomes the central decision ledger of
   `rwb_decision`, because the data lake is removed (GAP-0178; ASM-0262; ADR-018, ADR-022).
4. **Destruction.** The four steps and the monthly cadence stay. JOB-17 becomes a Temporal Schedule in `rwb-document`,
   reads `retention_rule`, and acts through the owner of each schema, because no service may write another service's
   tables and no expiry operation or event exists (GAP-0182; ASM-0266; ADR-016, DP-01).
5. **Legal hold.** The three hold rules stay; the hold is `recovery_case.legal_hold` with `status_before_hold` in
   `rwb_case`, and a hold on a party or a document is read from the case, since neither has a field of its own
   (GAP-0181; ASM-0265).
6. **Scores and access log.** Scores (DP11) is read from `v_ace_score`, with no Workbench table, and the access log is
   `rwb-access`; both keep their source period and both are recorded as gaps (GAP-0179, GAP-0183).
7. **Decisions.** Section 6 lists D-RCV-60, ADR-013 to ADR-023 as they apply here, and DL26 to DL49, with the IDs of
   `ids.json` and Template and Rules R8.4.

## 4. Owners

Every owner is a service code and a schema of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`, or a
party outside the 19 services (ACE Common, the SOC, OpenTelemetry, Azure Blob) (ASM-0273). Retention itself is
P5 `rwb-document` under the Ownership Map ruling, which is why `retention_rule` and `retention_action` are named in
`rwb_document` only. No owner is a team type and no person is named.

## 5. Registers

- Gap rows written: **9** candidate rows, `GAP-0177` to `GAP-0185`, in `_work/msr/gaps/B-CTRL-33.jsonl`:
  1 Conflict, 2 Outdated and 6 Missing; 5 of severity P2 and 4 of P3; needed by wave 0 (1 row), wave 1 (7 rows) and
  wave 2 (1 row).
- Assumption rows written: **15** candidate rows, `ASM-0261` to `ASM-0275`, in
  `_work/msr/assumptions/B-CTRL-33.jsonl`: 8 High and 7 Medium.
- Nine of the fifteen assumptions answer a gap one for one (ASM-1 to ASM-9), and each gap names its assumption. Six
  carry no gap (ASM-10 to ASM-15): the draft status, the added sections, the dates, the owners being service codes, the
  logs, and the policy document not being a story.
- Every citation in the document resolves to a row: 24 distinct CG/ASM citations, 0 unresolved.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-CTRL-33 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

The verification script reports PASS: header lines 1 and 2 as the first two paragraphs, the D-RCV-60 change-log row
present, 0 unexplained missing lines of version 2, headings 1 to 7 in order, 10 tables, all 19 schema rows in section
1.1, 0 unresolved CG/ASM citations, no replacement character, and the document properties set to the organisation and the
tool. C12 finds no person name and no email address; C13 finds no issue-tracker reference; C18 finds no write outside the
"Write only" list and no change to a story master. The v2 document is unchanged on disk.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-0270). No later lifecycle stage
was started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. No other
document of the folder was touched.
