# Edit log - WP B-TESTDOC-40 (Recovery Workbench Non Functional Test Plan next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work pack: B-TESTDOC-40. Fanout: 0 (no subagent).

## Files written

- `09 Testing and quality/Recovery Workbench Non Functional Test Plan v3.docx`
- `_work/msr/docs/B-TESTDOC-40/Recovery Workbench Non Functional Test Plan v3.md`
- `_work/msr/docs/B-TESTDOC-40/template_v3.docx`
- `_work/msr/docs/B-TESTDOC-40/fix_template.py`
- `_work/msr/docs/B-TESTDOC-40/renumber.py`
- `_work/msr/docs/B-TESTDOC-40/clean_md.py`
- `_work/msr/docs/B-TESTDOC-40/format_tables.py`
- `_work/msr/docs/B-TESTDOC-40/format_title.py`
- `_work/msr/docs/B-TESTDOC-40/format_widths.py`
- `_work/msr/docs/B-TESTDOC-40/set_properties.py`
- `_work/msr/docs/B-TESTDOC-40/verify.py`
- `_work/msr/docs/B-TESTDOC-40/check_editlog_parse.py`
- `_work/msr/docs/B-TESTDOC-40/roundtrip/Recovery Workbench Non Functional Test Plan v3.md`
- `_work/msr/gaps/B-TESTDOC-40.jsonl`
- `_work/msr/assumptions/B-TESTDOC-40.jsonl`
- `_work/msr/editlog/B-TESTDOC-40.md`

Nothing else was written. The source `09 Testing and quality/Recovery Workbench Non Functional Test Plan v2.docx`
was read only and is byte-for-byte unchanged on disk (sha256 checked against `_work/msr/plan/baseline.json`).
Its text for reading came from the sanctioned conversion command into `_work/msr/extract/B-TESTDOC-40/`.

Read for this work pack: the converted text of the v2 plan (all 46 lines, the 3 tables and the 4 sections);
`22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (R1, R3, R4, R5,
R7 and R8.1, R8.3, R9); `_work/msr/plan/ownership.json` (tables, api, events, jobs, workflows and the
rulings) and `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Read me,
Services, Jobs, Workflows and activities); `22 Microservice Realignment/Recovery Workbench Architecture v5 Text
Extract v1.md` (slides 2, 3, 4, 10, 11, 12, 13, 14 to 20, 33, 34, 38, 41 to 44, 48 and 49);
`22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (the 19-service
shape, the workflow kit, Continue-As-New, the rule package lifecycle, the failure scenes);
`_work/msr/plan/split_plan.json` ("stats" and "legacy" only); `_work/msr/plan/ids.json`; and
`_work/msr/extract/Recovery Workbench Non Functional Specification v3.md` for the NFR IDs and targets.

## How the next version was produced

1. **Read me order.** The v3 file opens with the two header lines of Template and Rules R8.1, the product
   title, the document name, the document control table and the change log. The change-log row reads
   `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`,
   and the same string is repeated as a line of its own.
2. **Markdown first.** The whole text was written to `_work/msr/docs/B-TESTDOC-40/... v3.md` and the .docx was
   built from it with `compat/office_write.py md-docx --template`, so the source file was never edited.
3. **A scratch template.** The source stores its built-in styles under display names, which python-docx cannot
   resolve, so `fix_template.py` copied the source to `template_v3.docx` and lower-cased only the style names
   (`title`, `heading 1` to `heading 6`, `list paragraph`). Page setup, footer, theme and fonts come from the
   source.
4. **Tables.** The source template defines no table style, so `format_tables.py` added single-line grey borders,
   a repeating header row and 8.5 pt cell text to the 15 tables of the new file; `format_widths.py` gave each
   table a fixed proportional column width (6.69 inches, the usable A4 width); and `format_title.py` restored
   the 26 pt title and the 17 pt subtitle of the source title block.
5. **Properties.** The source carries a person name in `author` and `last_modified_by`. `set_properties.py` set
   both to the organisation and the tool line, the title to "... v3", the subject to D-RCV-60, the revision to 3
   and the modified date to 22 November 2026. A scan of every part of the package finds no person name.

## What the version keeps

- The title, the subtitle and the 4 sections 1 to 4, in the same order and with the same headings.
- The 8 tests of section 1 with their How, Pass mark and When cells, cell for cell: Load (410 simulated users at
  three requests a minute for one hour; 95th percentile under 2 seconds; error rate under 0.5 percent), Stress
  (twice the busiest hour; no data loss; recovers within 10 minutes), Volume (end-2027 size; case history under
  2 seconds), Batch window (COLLINS load and the morning chain; allocation complete by 07:00), Resilience (kill a
  service instance, fail the database over, stop the agent platform; no lost actions; agent steps fall back to
  rules), Restore (within the ACE recovery objectives, DL11), Security (no finding above the bank threshold;
  penetration before the partner portal opens) and Accessibility (no level A or AA failure; each screen).
- The environment paragraph, the who-runs table (5 rows) and the open-target sentence on DL11.
- Every ID, number and date of the source, including the ones of the NFR specification it points to. The date
  28 October 2026 is kept and the source's title-block line is quoted in the Supersedes row, because the R8.1
  header takes the first two lines of the new document.

## What the version changes, and why

1. **Per-service non-functional tests (new section 6, 82 rows).** Five test slots per service, from the 19
   services of the Ownership Map v1: 6.1 response time and load (19 rows, NFT-<code>-01), 6.2 rules and agents
   (6 rows, NFT-<code>-02, for the six services that evaluate a route, treatment, debt-sale, write-off or
   screening decision or call an agent), 6.3 events, workflows and schedules (19 rows, NFT-<code>-03), 6.4 data,
   isolation and restore (19 rows, NFT-<code>-04) and 6.5 security, masking and audit (19 rows,
   NFT-<code>-05).
2. **Journey tests (new section 7, 12 rows).** The six steps of the recovery journey on Architecture v5 slide 3,
   the eight routes and the always-on deviation and decision pieces, each row naming the services, the workflow
   and the NFR IDs it proves.
3. **Platform tests (new section 8, 8 rows).** gateway-bff and the edge, Kafka, Temporal, the 19 schemas and
   logins, observability, the template and pipeline, availability, and backup and restore of the shared stores.
4. **Load and gates (new section 9).** The wave of each service is its Ownership Map wave (P1 to P7, P9 and P10
   in wave 1; P8, S2, S5 and S8 in wave 2; S1, S3, S4 and S6 in wave 3; S7 and S9 in wave 4), with the source
   gates (E1, E2, E5, E8, each release, each screen) written against it.
5. **Traceability (new section 10).** The 8 non-functional legacy keys NF-01 to NF-08, their disposition
   Moved (no impact), their new platform story RWB-PLT-NF01-OPS to RWB-PLT-NF08-INF and the test that proves
   each; then the NFR IDs each group of tests proves.
6. **Registers (new section 11).** The 8 gap rows and their paired assumptions, with the D1 numbering note.
7. **Kept and changed (new section 12).** A short statement of what is word for word and what the realignment
   added.

## Owners

Every owner is a service code of the Microservice Ownership Map v1 (P1 rwb-source-data, P2 rwb-integration,
P3 rwb-case, P4 rwb-access, P5 rwb-document, P6 rwb-comms, P7 rwb-decision, P8 rwb-payment, P9 rwb-reporting,
P10 rwb-agent, S1 rwb-valuation, S2 rwb-treatment, S3 rwb-guarantee, S4 rwb-litigation, S5 rwb-asset,
S6 rwb-debtsale, S7 rwb-writeoff, S8 rwb-deviation, S9 rwb-partner) or a platform epic of Template and Rules
R5.1 (RWB-PLT-TPL, RWB-PLT-LIB, RWB-PLT-WF, RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-EDGE, RWB-PLT-OBS). The team
type is written as a role only (QA team, QA engineers, SCB IT, SCB IT security, ACE team, DevOps team,
database administrator role, solution architect, delivery lead, business lead, IT lead with Operational Risk,
document owner). No person is named and no team is made the owner of a service test.

## Decisions cited

D-RCV-60, with ADR-013, ADR-014, ADR-015, ADR-016, ADR-017, ADR-018, ADR-019, ADR-020, ADR-021, ADR-022,
ADR-023, DL44, DL45, DL46, DL47, DL48 and DL49 available in `_work/msr/plan/ids.json` for the architecture
statements; this document itself cites U1, U3, U7, U8, R3, R4, R5.1, R5.3, R5.6, R7 s17, R8.1, R9, D-RCV-60,
DL11, DL27, ADR-010 and the DP-01, DP-02 and DP-15 patterns. No new ADR or DL ID is allocated here.

## Registers

- Gap rows written: **8** candidate rows, `GAP-2124` to `GAP-2131`, in
  `_work/msr/gaps/B-TESTDOC-40.jsonl` (5 Missing, 1 Conflict, 1 Ambiguous, 1 Outdated; 1 P1 for the open
  restore target, 3 P2, 4 P3).
- Assumption rows written: **15** candidate rows, `ASM-3409` to `ASM-3423`, in
  `_work/msr/assumptions/B-TESTDOC-40.jsonl` (10 High, 5 Medium).
- Every gap row names its paired assumption, every assumption rests on its gap where it has one, and every
  citation in the document resolves to a row in one of the two files.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as root rule 7 and Template and Rules R9 require.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TESTDOC-40 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

C02, C03 and C05 are the story-file checks, and this work pack writes no story file. C12 finds no person name
and no email address in the files of this WP. C13 finds no issue-tracker reference. C18 finds no write outside
the "Write only" list and no change to a story master.

`python -I "_work/msr/docs/B-TESTDOC-40/verify.py"` reports PASS on 24 assertions: header lines 1 and 2 present;
the change-log row present and identical; the 9-row section 1 table cell for cell equal to v2; the 5-row
who-runs table kept with 6 rows appended; every source paragraph of 40 characters or more kept verbatim; 19
services carrying tests with 4 or 5 each and 82 in total; 12 journey and 8 platform tests; no issue-tracker
reference; no email address; the four document properties set to the organisation and the tool; no person name
anywhere in the .docx package; 8 gap and 15 assumption rows, all citations resolved and all pairs intact; and
the v2 file byte-for-byte unchanged.

## Status and boundaries

The plan is issued in **Draft**: no approval is recorded for this run (ASM-3409). No later lifecycle
stage was started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was
created. No other document of the family was touched and the v2 plan was read only.

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash
