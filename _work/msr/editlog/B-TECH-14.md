# Edit log - WP B-TECH-14 (Recovery Workbench Notification and Correspondence Design next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Notification and Correspondence Design v2.docx`
(converted text, all six sections and five tables), `22 Microservice Realignment/Recovery Workbench Microservice Story
Template and Rules v1.md` (R1, R3, R5, R8, R9), `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery
Workbench Microservice Ownership Map v1.xlsx` (Services, Tables, Endpoints, Events, Workflows, Jobs, Rulings),
`22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 9, 13, 14, 17, 20, 30, 31,
41, 42, 44, 47, 48), `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`
(slides 7, 8, 13 and the kit templates), `_work/msr/plan/split_plan.json` (stats and legacy only) and
`_work/msr/plan/ids.json`. The module specifications were also read for the target values: TSD P6 Communications v2,
FSD P6 Communications v3, Interface Specifications v4 (INT-14, INT-15, INT-17, INT-18, INT-34), Physical Schema v6
(notice, template, merge_field), Decision Log v10 (DL10, DL28) and Business Rules and Routing Logic v4 (R-LIT-03 to
R-LIT-08, R-UNI-10). Nothing read was edited; the v2 document was opened read-only and used as a template, never written.

## Files written

- 05 Technical architecture/Recovery Workbench Notification and Correspondence Design v3.docx
- _work/msr/gaps/B-TECH-14.jsonl
- _work/msr/assumptions/B-TECH-14.jsonl
- _work/msr/editlog/B-TECH-14.md

Scratch files under `_work/msr/docs/B-TECH-14/` (build and verification only, not outputs of the run): the full text
`Recovery Workbench Notification and Correspondence Design v3.md`, `template-fixed.docx`, `build.py`, `verify.py` and
`rows.py`. The converted source text sits in the run extract folder, `_work/msr/extract/B-TECH-14`.

## 1. How the next version was produced

The source was never edited. The full text of version 3 was written to
`_work/msr/docs/B-TECH-14/Recovery Workbench Notification and Correspondence Design v3.md` and rendered onto a scratch
copy of the v2 document with `compat/office_write.py md-docx --template`, so the new version keeps the v2 styles,
section properties, page setup and footer.

**Template repair, in the scratch copy only.** This document family stores the heading style names as `Heading 1`,
which `python-docx` looks up as `heading 1`, and it has no `List Bullet` style; `md-docx` fails on the family and the
bullet fallback appends a second, prefixed copy of every bullet. `build.py` repairs the copy (conventional style names,
and a `List Bullet` style on `List Paragraph` with the numbering `numId 3` that the v2 lists in sections 2 and 4 use)
and then renders. The v2 file is byte-for-byte unchanged.

**Document properties.** The v2 file carries a person name in `author` and `last_modified_by`. `build.py` sets the new
file to `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Notification and
Correspondence Design v3`, revision 3 and modified 22 November 2026 (rule 4).

**Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules R8.1. The metadata
table carries the change row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`, a `Source version` row `1, 28 October 2026`, a `Service` row naming P6 rwb-comms and the `Status` row `Draft. No
approval is recorded for this version (ASM-3352)`.

**One version conflict.** The source metadata table reads `Version | 1` and `Date | 28 October 2026`, while the file name
reads v2. The file name is taken as the family version, so this document is version 3, and both source readings stay in
the document (GAP-2087; ASM-3353).

## 2. Fidelity to version 2

`verify.py` compares every non-empty line of the v2 text with the round-trip extract of the v3 file, cell by cell for
tables:

| Item | Result |
|---|---|
| Unique non-empty lines of version 2 | 107 |
| Lines of version 2 present verbatim in version 3 | All, except the three lines listed as intended changes |
| Lines of version 2 not found and not listed as changed | 0 |
| Sections | 1 to 6 in the order of the source, then 7, 8 and 9 added |
| Tables | 15 (5 of the source, 10 new) |
| Header lines 1 and 2 | Present, as the first two lines |
| Change-log row with D-RCV-60 and the tool line | Present |
| Unresolved CG/ASM citations | 0 of 27 |

The three intended changes are the source date line (replaced by the R8.1 header and the `Source version` row) and the
`Version` and `Date` rows of the metadata table (now 3 and 22 November 2026). Every other heading, table row, ID and
number of the source is kept character for character: the five kinds of notice and their channels and proofs, the seven
production bullets, R-LIT-03, R-LIT-04, R-LIT-05, R-LIT-07, R-LIT-08 and R-UNI-10, the five template rows, DL10 and
DL28 with their fallback answers, and the three volume rows including "About 1,900 a month". The source carries no
release date and none is added; the forward date of 28 October 2026 is kept and read as tentative under U7 and DL48
(ASM-3366).

## 3. What version 3 changes, and why

The change set is the realignment only: the service that owns notices, templates and proofs of delivery. Section 9 of
the document holds the change table with the section, the v2 value, the v3 value and the decision. In summary:

1. **One owner for notices.** Everything the source calls "the Workbench" for a notice is P6 rwb-comms: notices,
   templates, merge fields and the proof of delivery in `rwb_comms`, with REST base `/api/recovery/comms/v1`, topic
   `rwb.comms.events.v1` and queue `rwb-comms` (Architecture v5 slides 17 and 41; Ownership Map v1; ADR-013, ADR-014).
2. **Seven steps, five services.** The seven production bullets are mapped step by step in 2.1: the notice request and
   the workflow in P6, the letter in P5 rwb-document, the approval in P7 rwb-decision, the file in P2 rwb-integration and
   the proof of delivery read by P1 rwb-source-data. Each crossing is a contract or an event (DP-11, DP-16, DP-18).
3. **Templates and merge fields.** `rwb_comms.template` and `rwb_comms.merge_field`, with the P6 admin endpoints and the
   Legal approval on the version. The DL28 answer of 13 November 2026 gives the templates to the document module; the
   conflict is raised and Architecture v5 is followed (GAP-2089; ASM-3356).
4. **Contact rules placed.** The consent and the contact point are P1 `contact_point_ext` read through the P1 contract;
   the contact stop arrives as EV-06 and EV-07 from S8 rwb-deviation; contact times are reference data of P3 rwb-case;
   the interaction ledger is P1's (DP-07, DP-18; GAP-2091, GAP-2092, GAP-2097).
5. **Events.** EV-13 NoticeGenerated, EV-14 NoticeDispatched and EV-15 NoticeDelivered are published on
   `rwb.comms.events.v1`; EV-05, EV-06, EV-07, EV-10 and EV-12 are consumed (Architecture v5 slide 42; ADR-015).
6. **Workflow and job.** NoticeDispatchWorkflow and JOB-10 at 16:00 are kit templates of the platform, not Quartz jobs
   (Architecture v5 slide 44; ADR-016).
7. **Decisions.** Section 8 lists D-RCV-60, ADR-013 to ADR-016 and ADR-018 to ADR-023, and the decision-log rows DL44 to
   DL49, all decided on 22 November 2026 (`ids.json`; Rules v1 R8.4).

## 4. Owners

Every owner in the document is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`,
or a party outside the 19 services (ACE Common, WIN, NSS, LINE OA) (ASM-3367). No owner is taken from the story
masters, and no owner is a team type or a person. The partner instruction and the internal alert are the two kinds the
source lists that rwb-comms does not own; they are given to S9 rwb-partner and P3 rwb-case and raised as a gap
(GAP-2095; ASM-3362).

## 5. Registers

- Gap rows written: **12** candidate rows, `GAP-2087` to `GAP-2098`, in `_work/msr/gaps/B-TECH-14.jsonl`:
  6 Conflict, 3 Missing, 2 Ambiguous, 1 Outdated; 6 of severity P2 and 6 of P3; needed by wave 0 (1 row), wave 1
  (5 rows), wave 2 (5 rows) and wave 3 (1 row).
- Assumption rows written: **17** candidate rows, `ASM-3352` to `ASM-3368`, in
  `_work/msr/assumptions/B-TECH-14.jsonl`: 8 High and 9 Medium.
- Twelve of the seventeen assumptions answer a gap one for one (ASM-2, ASM-4 to ASM-14), and each of the twelve gaps
  names its assumption. Five assumptions carry no gap (ASM-1, ASM-3, ASM-15, ASM-16, ASM-17): the draft status, the
  added sections, the unchanged dates, the owners being service codes, and the order of the ledger write and the send.
- Every citation in the document resolves to a row: 27 distinct CG/ASM citations, 0 unresolved.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-14 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify.py` reports PASS: header lines 1 and 2 present, the D-RCV-60 change-log row present, 0 unexplained missing lines
of version 2, sections 1 to 9 in order, 15 tables, 0 unresolved CG/ASM citations, no replacement character, and the
document properties set to the organisation and the tool. C12 finds no person name and no email address in the files of
this WP; C13 finds no issue-tracker reference; C14 finds no missing header in the markdown text; C18 finds no write
outside the "Write only" list and no change to a story master. The v2 document is unchanged on disk.

Two observations outside this WP's files, recorded and not acted on, because fixing them would be a write outside the
"Write only" list:

- C17 (not part of the quick set) stops on `_work/msr/gaps/B-P8-01.jsonl`, which starts with a UTF-8 byte-order mark, so
  the whole register cannot be parsed by that check. The two files of this WP carry no byte-order mark and pass the row
  and required-key rules when read on their own.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-3352). No later lifecycle stage was
started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. No other
document of the family was touched, and the v2 document was not edited.

## 8. Verification pass and the one content correction

The next version was then audited against the plan files a second time, and one content defect was corrected in the
document this WP owns. It is recorded here because section 7.2 of the document changed:

- **What was wrong.** Section 7.2 says it lists the P6 stories that build this design, but three of them were missing:
  `RWB-P6-E1034-APP` (letter template management, 30 November 2026), `RWB-P6-E2014-APP` (approval screen for D7.1
  demand and recall notices, 31 December 2026) and `RWB-P6-E5002-APP` (record proof of delivery on a notice,
  31 March 2027). All three carry sections 2.1, 3 and 7 of this design. The closing sentence of 7.2 also read that
  `RWB-P6-E4039` carries EP02, while `split_plan.json` gives it wave 3 and EP04.
- **What was done.** The three rows were added with the plan's own work type, title and release (each marked
  "(tentative)"), and the closing sentence now states the wave and the business epic of every story mentioned, per
  `split_plan.json` and Rules v1 R5.6: wave 1 and EP01 for E1034, E1046, E1052 and E1055; wave 2 and EP02 for E2014,
  E2021 and E2022; wave 3 and EP04 and EP05 for E4039 and E5002; wave 4 and EP08 for AD017.
- **No new gap or assumption.** Every value of the three rows is read from `_work/msr/plan/split_plan.json`; nothing is
  invented, so the registers stay at 12 gap rows and 17 assumption rows, and the 27 CG/ASM citations of the document
  are unchanged.

The deliverable and the registers were then re-verified: `build.py` re-rendered the file from the markdown onto the
repaired scratch copy of v2, `verify.py` reported PASS (107 source lines, 0 unexplained missing lines, 27 citations with
0 unresolved, 15 tables, 9 sections in order, organisation and tool in the document properties), the markdown-to-docx
completeness check reported 0 missing lines with the R8.1 header as paragraphs 1 and 2 and the D-RCV-60 change-log row
present, and `run_all.py --quick` reported C02, C03, C05, C12, C13 and C18 all PASS with 0 findings. The v2 document is
still unchanged on disk.
