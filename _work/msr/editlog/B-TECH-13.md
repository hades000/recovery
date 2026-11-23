# Edit log - WP B-TECH-13 (Recovery Workbench Document Management Design next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Document Management Design v2.docx` (converted text in
`_work/msr/extract/B-TECH-13`, all eight sections, five tables and the three open decisions DL19, DL26 and DL27);
`22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (R1, R3, R5, R8, R9);
`_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`
(the 12 P5 tables, the 17 P5 operations, EV-16, EV-17, EV-28, JOB-12, JOB-17, DocumentIntakeWorkflow);
`22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 13, 14, 16, 20, 41, 42, 43, 44);
`22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`;
`_work/msr/plan/split_plan.json` (`stats` and `legacy` only) and `_work/msr/plan/ids.json`.
Nothing read was edited. The v2 document was opened read-only and used as the render template; it is byte-for-byte
unchanged on disk (sha256 matches `_work/msr/plan/baseline.json`).

## Files written

- 05 Technical architecture/Recovery Workbench Document Management Design v3.docx
- _work/msr/docs/B-TECH-13/Recovery Workbench Document Management Design v3.md
- _work/msr/docs/B-TECH-13/template-fixed.docx
- _work/msr/docs/B-TECH-13/build.py
- _work/msr/docs/B-TECH-13/verify.py
- _work/msr/docs/B-TECH-13/check_log.py
- _work/msr/gaps/B-TECH-13.jsonl
- _work/msr/assumptions/B-TECH-13.jsonl
- _work/msr/editlog/B-TECH-13.md

Everything except the version 3 document and this log sits in the scratch folder `_work/msr/docs/B-TECH-13/` (rule 5):
the full text of the new version, the repaired scratch template, the build script and the verification script. The
converted source text is in the run extract folder `_work/msr/extract/B-TECH-13`.

## 1. How the next version was produced

The source was never edited. The next version is 3, being the highest `v<n>` of the family in the folder plus 1
(Template and Rules R8.2), and the full text was written to
`_work/msr/docs/B-TECH-13/Recovery Workbench Document Management Design v3.md` and rendered onto a scratch copy of the
v2 document with `compat/office_write.py` `md-docx --template` (through `build.py`), so the new version keeps the v2
styles, section properties, page setup and footer.

**Template repair, in the scratch copy only.** The family stores its heading style names as `Heading 1`, which
`python-docx` looks up as `heading 1`, and it has no `List Bullet` style, so `md-docx` fails on the family and the
bullet fallback appends a second, prefixed copy of every bullet. `build.py` repairs only the scratch copy: conventional
style names, and a `List Bullet` style on `List Paragraph` with the bullet numbering the v2 lists use. The v2 file is
not touched.

**Document properties.** The v2 file carries a person name in `author` and `last_modified_by`. The new file is set to
`Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Document Management Design v3`,
revision 3 and modified 22 November 2026 (rule 4).

**Header, change log and status.** Paragraphs 1 and 2 of the new file are the header of Template and Rules R8.1. The
metadata table carries the change row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
DeepSeek v4.1 Flash`, a `Source version` row `1, as the source metadata table writes it, dated 28 October 2026` and the
status row `Draft. No approval is recorded for this version (ASM-3347)`; a change-log table follows the
metadata table with the same row.

**One version conflict.** The source metadata table reads `Version | 1` and `Date | 28 October 2026`, while the file
name reads v2. The file name is taken as the family version, so this document is version 3, and both source readings
stay visible in the `Source version` row (GAP-2077; ASM-3337; ASM-3348).

## 2. Fidelity to version 2

`verify.py` compares every substantive line of the v2 text with the round-trip extract of the v3 file, table rows
cell by cell:

| Item | Result |
|---|---|
| Substantive lines of version 2 | 68 |
| Kept character for character | 41 |
| Kept, with a realignment clause appended to the same sentence or cell | 24 |
| Intended changes | 3 |
| Lines of version 2 lost and not listed as changed | 0 |
| Sections | 1 to 8 in the order of the source, then 9 (seven subsections) and 10 added |
| Tables | 15 (6 of the source, 9 new) |
| Header lines 1 and 2 | Present, as the first two paragraphs |
| Change-log row with D-RCV-60 and the tool line | Present |

The three intended changes are the source date line `SCB Collections and Recovery. Henka Group, 28 October 2026`
(replaced by the R8.1 header, its date kept in the `Source version` row), the `Version` row (1 to 3) and the `Date` row
(28 October 2026 to 22 November 2026).

Every other heading, table row, ID, number and message code of the source is kept: the nine rows of section 1, the
seven intake sources, the six document types with all their fields and retention classes, the four custody events, the
four search and access rules, the four retention rules, DT06, NFR-076, DL03, DL19, DL26, DL27 and MSG-P5-002,
MSG-P5-003 and MSG-P5-004. The 24 extended lines keep their source sentence word for word and append the
per-service statement that the realignment needs, with its CG and ASM citation. The source carries no release date and
none is added; the forward date of 28 October 2026 is read as tentative under U7 and DL48 (ASM-3348).

## 3. What version 3 changes, and why

The change set is the realignment only. Section 10 of the document holds the change table with the section, the source
statement, the version 3 statement and the decision. In summary:

1. **One service for the hub.** The document hub is the service rwb-document (P5) with schema and login `rwb_document`,
   REST base `/api/recovery/document/v1`, topic `rwb.document.events.v1` with its retry and `.dlt` topics, task queue
   `rwb-document`, namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.document` (ADR-013,
   ADR-014; DP-02, DP-13, DP-14).
2. **One schema.** The three source tables and nine more sit in `rwb_document` and are owned by P5; no other service
   reads them and there is no cross-schema join, view or foreign key (DP-01; ADR-014).
3. **Intake is a workflow.** "The intake job" becomes `DocumentIntakeWorkflow` on queue `rwb-document`, started every
   15 minutes by JOB-12 with KEDA workers (ADR-016; DP-10; Arch v5 slides 16 and 44).
4. **The agent is a service.** Classification and extraction are child workflows on queue `rwb-agent` (P10), answered
   by `AgentRunCompleted` (EV-28) on `rwb.agent.events.v1` (DP-20).
5. **The store is named.** "Blob storage" is Azure Blob (WORM), claim-check with the file ID in the case, the workflow
   and the events, planned at 2.8 TB by 2031 (Arch v5 slide 16; GAP-2085).
6. **The case and the authority are contracts.** The case match reads the case contract of rwb-case (P3) over REST,
   one hop with a 2 s timeout and a fake; the capability area and case scope are checked through the authorise contract
   of rwb-access (P4) with the guard library (DP-11, DP-08; GAP-2078).
7. **Records management is split.** `retention_rule` and `retention_action` stay in `rwb_document`; the legal hold is
   recorded by rwb-case (P3) through `POST /cases/{caseId}/legal-hold` and is read by rwb-document before any expiry is
   proposed (GAP-2079; ASM-3339).
8. **New section 9.** The service view: identity, the 17 provided operations, the one consumed operation, the two
   published and one consumed event, the workflow, the two activities and the schedule, the 12 owned tables and the
   call-type summary.
9. **New section 10.** The change table, so that a reader sees what moved and under which decision.
10. **Decisions.** DL44 to DL49 are added to the open-decision list of section 8 as decided on 22 November 2026;
    DL19, DL26 and DL27 stay open and are copied word for word (Rules v1 R8.4; `ids.json`).

## 4. Owners

Every owner in the document is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`:
P5 rwb-document for the 12 tables, the 17 operations, EV-16, EV-17, JOB-12, JOB-17 and `DocumentIntakeWorkflow`;
P3 rwb-case for the case contract, the legal hold and the task; P4 rwb-access for the masking rows, the access log and
the authorise contract; P10 rwb-agent for the agent runs and EV-28; S2 rwb-treatment for the settlement e-signature;
S9 rwb-partner for the partner upload. The platform dependencies are named with their story keys
(H RWB-PLT-E1037-CON, C RWB-P4-E1037-CON). No owner is a team type or a person, and no owner is taken from a story
master (ASM-3349).

## 5. Registers

- Gap rows written: **10** candidate rows, `GAP-2077` to `GAP-2086`, in `_work/msr/gaps/B-TECH-13.jsonl`
  (4 Ambiguous, 2 Conflict, 2 Missing, 2 Outdated; 2 of severity P2 and 8 of P3). Every row carries the R9 key set.
- Assumption rows written: **15** candidate rows, `ASM-3337` to `ASM-3351`, in
  `_work/msr/assumptions/B-TECH-13.jsonl` (9 High, 6 Medium). Every row carries the R9 key set.
- Every gap row names its assumption, every assumption that rests on a gap names it, and every CG and ASM citation in
  the document resolves to a row: the document cites CG-1 to CG-10 and ASM-1 to ASM-15.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-13 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

Run as well, outside the quick set, on the files of this WP: C17 PASS (0 findings: every CG and ASM citation resolves
to a jsonl row, both registers carry the R9 key set), C20 PASS (tool line present, no wrong tool attribution),
C13 PASS, C14 PASS (header lines present).

`verify.py` reports PASS: header lines 1 and 2 are the first two paragraphs, the D-RCV-60 change-log row is present,
0 source lines are lost, sections 1 to 8 keep the source order with 9 and 10 added, 15 tables, no template artefact,
no email address, no issue-tracker reference, and the document properties set to the organisation and the tool (49
paragraphs, 15 tables).

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-3347). No later lifecycle stage
was started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. No other
document of the family was touched, and the v2 document is unchanged on disk.
