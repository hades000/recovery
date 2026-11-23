# Edit log - WP B-TECH-12 (Recovery Workbench Audit and Logging Design next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Audit and Logging Design v2.docx` (converted text, all six
sections and four tables), `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md`
(R1, R3, R5, R8, R9), `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice
Ownership Map v1.xlsx` (tables, endpoints, events, jobs, rulings), `22 Microservice Realignment/Recovery Workbench
Architecture v5 Text Extract v1.md` (slides 13, 14, 20, 26, 28, 29, 30, 35, 37, 42, 44, 49), `22 Microservice
Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (decision record, strict mode, ADR-009
change), `_work/msr/plan/split_plan.json` (stats and legacy only) and `_work/msr/plan/ids.json`. Nothing read was edited;
the v2 document was opened read-only and used as a template, never written.

## Files written

- 05 Technical architecture/Recovery Workbench Audit and Logging Design v3.docx
- _work/msr/gaps/B-TECH-12.jsonl
- _work/msr/assumptions/B-TECH-12.jsonl
- _work/msr/editlog/B-TECH-12.md

Scratch files under `_work/msr/docs/B-TECH-12/` (build and verification only, not outputs of the run): the full text
`Recovery Workbench Audit and Logging Design v3.md`, `template-fixed.docx`, `build.py`, `verify.py`, `rows.py` and the
round-trip extract under `roundtrip/`. The converted source text sits in the run extract folder,
`_work/msr/extract/B-TECH-12`.

## 1. How the next version was produced

The source was never edited. The full text of version 3 was written to
`_work/msr/docs/B-TECH-12/Recovery Workbench Audit and Logging Design v3.md` and rendered onto a scratch copy of the v2
document with `compat/office_write.py md-docx --template`, so the new version keeps the v2 styles, section properties,
page setup and footer.

**Template repair, in the scratch copy only.** This document family stores the heading style names as `Heading 1`, which
`python-docx` looks up as `heading 1`, and it has no `List Bullet` style; `md-docx` fails on the family and the bullet
fallback appends a second, prefixed copy of every bullet. `build.py` repairs the copy (conventional style names, and a
`List Bullet` style on `List Paragraph` with the numbering `numId 3` that the v2 lists in sections 4 and 6 use) and then
renders. The v2 file is byte-for-byte unchanged.

**Document properties.** The v2 file carries a person name in `author` and `last_modified_by`. `build.py` sets the new
file to `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Audit and Logging Design
v3`, revision 3 and modified 22 November 2026 (rule 4).

**Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules R8.1. The metadata
table carries the change row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`, a `Source version` row `1, 28 October 2026` and the status row `Draft. No approval is recorded for this version
(ASM-3320)`.

**One version conflict.** The source metadata table reads `Version | 1` and `Date | 28 October 2026`, while the file name
reads v2. The file name is taken as the family version, so this document is version 3, and both source readings stay in
the document (GAP-2067; ASM-3321).

## 2. Fidelity to version 2

`verify.py` compares every non-empty line of the v2 text with the round-trip extract of the v3 file, cell by cell for
tables:

| Item | Result |
|---|---|
| Lines of version 2 present verbatim in version 3 | All, except the seven lines listed as intended changes |
| Lines of version 2 not found and not listed as changed | 0 |
| Sections | 1 to 6 in the order of the source, then 7, 8 and 9 added |
| Tables | 10 (4 of the source, 6 new) |
| Header lines 1 and 2 | Present, as the first two lines |
| Change-log row with D-RCV-60 and the tool line | Present |

The seven intended changes are the source date line (replaced by the R8.1 header and the `Source version` row), the
`Version` and `Date` rows of the metadata table (now 3 and 22 November 2026), and one `Where` cell each of the decision
log, interaction ledger, access log and application logs rows. Every other heading, table row, ID and number of the
source is kept character for character: R-UNI-24, DL26, D1 to D9, all eleven entry fields, all five tracing bullets, all
four integrity bullets, all four retention rows and the three "never logged" bullets. The source carries no release date
and none is added; the forward date of 28 October 2026 is read as tentative under U7 and DL48 (ASM-3333).

## 3. What version 3 changes, and why

The change set is the realignment only: the local decision record plus the central ledger. Section 9 of the document
holds the change table with the section, the v2 value, the v3 value and the decision. In summary:

1. **Local record plus central ledger.** The single decision log becomes a local decision record in the schema of the
   service that takes the decision, written in one transaction with the state change and the outbox row (R-UNI-39), and a
   central ledger in rwb-decision (P7) collected from EV-08 on topic `rwb.decision-record.v1` (ADR-022, ADR-009 amended;
   Architecture v5 slides 20 and 28). Section 2.1 maps the eleven source fields to the target field names of the Temporal
   and Drools design.
2. **Owners from the Ownership Map.** Every store has one owner: `decision_log_entry` in `rwb_decision` (P7);
   `interaction` and `efs_ledger_outcome` in `rwb_source_data` (P1, plan default ruling and DP-18); the access log in
   `rwb_access` (P4, with `GET /admin/access-log`); retention tables in rwb-document (P5); the rule and model versions in
   rwb-decision (P7); ACE Common and the SOC log outside the 19 services. The new section 7 is that table.
3. **Data lake removed.** The nightly copy of the decision log to the data lake is removed (ADR-018, DP-17). JOB-13 is
   the continuous ingest in rwb-decision, JOB-14 is the daily chain check and the ledger is anchored daily to write-once
   storage (Architecture v5 slides 14, 28 and 44). RWB-E1-014 stays retired.
4. **Integrity per service.** The four rules of the source are kept and placed: the one transaction, strict mode at the
   four points of no return (debt transfer, write-off posting, auction sale and title transfer), the daily seal, and the
   gap alert inside the five-minute completeness target (Architecture v5 slides 26 and 28).
5. **Tracing across 19 services.** The five tracing bullets are kept; W3C Trace Context covers the services, the events
   and the workflows, and the audit search is answered by P7 on `GET /decision-log` (Architecture v5 slides 35 and 49;
   ADR-023).
6. **Privacy.** The three "never logged" rules are kept and extended to Kafka events and workflow history, which carry
   references and not personal data; the approver is an identifier, masked in exports (GAP-2073;
   ASM-3330).
7. **Decisions.** Section 8 lists D-RCV-60, ADR-009 as amended, ADR-013 to ADR-016, ADR-018, ADR-022 and ADR-023, and
   the decision-log rows DL44 to DL49, all decided on 22 November 2026 (ids.json; Rules v1 R8.4).

## 4. Owners

Every owner in the document is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`,
or PLT for the platform observability (ASM-3331). No owner is taken from the story masters, and no owner is a team
type or a person. Where the source names a party that the map does not own (ACE Common, the SOC log), the document names
the party outside the 19 services and the ACE Common contract INT-34.

## 5. Registers

- Gap rows written: **10** candidate rows, `GAP-2067` to `GAP-2076`, in `_work/msr/gaps/B-TECH-12.jsonl`
  (5 Ambiguous, 2 Conflict, 2 Missing, 1 Outdated; 4 of severity P2 and 6 of P3).
- Assumption rows written: **17** candidate rows, `ASM-3320` to `ASM-3336`, in
  `_work/msr/assumptions/B-TECH-12.jsonl` (9 High, 8 Medium).
- Every gap row names its assumption, every assumption that rests on a gap names it, and every citation in the document
  resolves to a row: the document cites CG-1 to CG-10 and ASM-1 to ASM-14, ASM-16 and ASM-17. ASM-15 is the document
  property assumption and is not cited in the body; it is applied to the .docx properties.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-12 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify.py` reports PASS: header lines 1 and 2 present, the D-RCV-60 change-log row present, 0 unexplained missing lines
of version 2, sections 1 to 9 in order, 10 tables, 0 unresolved CG/ASM citations, no replacement character and no
bullet-fallback text, and the document properties set to the organisation and the tool. C12 finds no person name and no
email address in the files of this WP; C13 finds no issue-tracker reference; C18 finds no write outside the "Write only"
list and no change to a story master. The v2 document is unchanged on disk.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-3320). No later lifecycle stage was
started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. No other
document of the family was touched.

## 8. Re-verification on the closing pass

The WP was re-checked on the closing pass of the same dispatch. No file under "Write only" was rewritten: the version 3
document, both register files and this log already held the run's output, and rewriting them would have edited a file
that exists (rule 1). The pass confirmed the state instead:

| Check | Result |
|---|---|
| `run_all.py --wp B-TECH-12 --quick` | C02 PASS 0, C03 PASS 0, C05 PASS 0, C12 PASS 0, C13 PASS 0, C18 PASS 0 |
| `verify.py` | PASS: 51 source lines, 0 not present; properties Henka Group / T3 Code / OpenCode / DeepSeek v4.1 Flash, revision 3; 58 paragraphs, 10 tables; 26 of 27 register rows cited |
| Header lines 1 and 2 of the .docx | `SCB Collections and Recovery. Henka Group, 22 November 2026.` and `(C) Siam Commercial Bank and Henka Pte Ltd`, as the first two paragraphs |
| Change-log row | `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` |
| Register counts | 10 gap rows (5 Ambiguous, 2 Conflict, 2 Missing, 1 Outdated; 4 P2, 6 P3) and 17 assumption rows (9 High, 8 Medium); key sets match R9 |
| Dates | 28 October 2026 kept; no release date added; a date later read as a release is tentative (U7; DL48) |
| Source files | v2 .docx unchanged on disk (last write 3 November 2026); no person name, email address or tracker reference in any file of this WP |
