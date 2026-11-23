# Edit log — WP B-TECH-11 (Recovery Workbench Availability Performance and Recovery Design next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Availability Performance and Recovery Design v2.docx`
(converted to text, all 6 sections and 5 tables), `22 Microservice Realignment/Recovery Workbench Microservice Story
Template and Rules v1.md` (§R1, §R3, §R4, §R5, §R7.2, §R8, §R9), `_work/msr/plan/ownership.json` and
`22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Read me, Services, Jobs, Rulings),
`22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 5, 10, 11, 22, 33, 34, 35,
37, 41, 48), `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (L1, L2,
slides 26, 27, 28), `_work/msr/plan/split_plan.json` (`stats` and `legacy` only) and `_work/msr/plan/ids.json`.
Nothing read was edited; the v2 document was opened read-only and used as the template, never written.

## Files written

- 05 Technical architecture/Recovery Workbench Availability Performance and Recovery Design v3.docx
- _work/msr/gaps/B-TECH-11.jsonl
- _work/msr/assumptions/B-TECH-11.jsonl
- _work/msr/editlog/B-TECH-11.md

Scratch, under `_work/msr/docs/B-TECH-11/`: the full text `Recovery Workbench Availability Performance and Recovery
Design v3.md`, `build.py`, `verify.py`, `probe_styles.py`, `template-fixed.docx` and the round-trip extract in
`roundtrip/`. The converted source text sits in `_work/msr/extract/B-TECH-11`.

## 1. How the next version was produced

- The source was never edited. Its full text is written to `_work/msr/docs/B-TECH-11/` and rendered onto a scratch copy
  of the v2 document with `compat/office_write.py`, so the new version keeps the v2 styles, section properties, page
  setup and footer.
- **Template repair, in the scratch copy only.** This family stores the heading style names as `Heading 1`, which
  `python-docx` looks up as `heading 1`, and it has no `List Bullet` style. Without the repair `md-docx` fails on the
  headings and the bullet fallback appends a second, prefixed copy of every bullet. `build.py` repairs the copy
  (conventional style names, and a `List Bullet` style on `List Paragraph` with the numbering the family uses, numId 2)
  and then renders. The v2 file is unchanged on disk; `roundtrip/` is the extract of the new file used for verification.
- **Document properties.** The v2 file carries a person name in `author` and `last_modified_by`. `build.py` sets the new
  file to `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title, revision 3 and modified 22 November 2026
  (rule 4).
- **Header, change log and status.** Lines 1 and 2 of the new file are the header of Template and Rules §R8.1. The
  metadata table carries the change row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode /
  DeepSeek v4.1 Flash`, the source version row (2 as the file name, 1 as the version in the source table, 28 October
  2026) and the status row `Draft. No approval is recorded for this version (ASM-3318)`.

## 2. Fidelity to version 2

`verify.py` compares every non-empty line of the v2 text with the round-trip extract of the v3 file.

| Item | Result |
|---|---|
| Lines of version 2 present verbatim in version 3 | 51 of 56 |
| Lines of version 2 changed on purpose, each with its reason in `verify.py` | 5 |
| Lines of version 2 not found and not listed as changed | 0 |
| Sections | 1 to 6, in order, with the same titles |
| Tables | 15 (5 of the source, 10 new) |
| Header lines 1 and 2 | Present, as the first two paragraphs |
| Change-log row with D-RCV-60 and the tool line | Present |
| Bullets rendered twice by the fallback | 0 |

The five changed lines are the source date line, the two metadata rows (Version and Date), and the two scaling bullets
that the realignment cannot keep: bullet 1 ("the recovery module adds no separate service") and bullet 2 (report reads
from the data lake). Every other line of the source, including all seven load rows, all eight service levels with their
statuses, all three backup rows, all five degraded-mode rows and all four test bullets, is copied word for word. Every
number (99.9, 99.5, 2 seconds, 300 milliseconds, 60 seconds, 07:00, 23,600, 26,500, 1,234, 410, 21, 5.8 million,
2.8 TB, 36 GB), every ID (DL11, DL27, NFR-071, RWB-TE-009) and every date of the source is kept.

## 3. What version 3 changes, and why

The change set is the realignment only, and the closing table of the document, `Realignment changes in version 3
(D-RCV-60)`, lists the twelve changes with the section, the v2 value, the v3 value and the decision.

1. **Per-service targets.** Section 1 keeps its eight levels and gains the owner of each from the Ownership Map; the new
   section 1.2 applies the two availability targets to all 19 services, in 19 rows with the owning epic (`RWB-SVC-P1` to
   `RWB-SVC-S9`) and the Arch v5 wave (ADR-013, DL45, DL46).
2. **Performance per call type.** The new section 1.3 turns the three response levels of the source into the seven call
   types of the target architecture, with the numbers the sources already set: 2 second REST timeout and one hop, retry
   topics at 1 minute, 10 minutes and 1 hour then the dead-letter topic, activity retry 1 second with back-off 2 and 10
   attempts, the 5 second statement timeout on the views, 300 ms on the rule and 60 seconds on the agent (ADR-015,
   ADR-016, ADR-020).
3. **RPO and RTO are a gap.** The two rows stay exactly as written (`The ACE value`, `Open, DL11`) and the new section
   1.4 states that no value exists for any store: the placeholder of Rules §R9 is used for the ACE database, the
   Temporal persistence database and the Kafka topics, with no tier and no number of minutes invented (GAP-2058).
4. **Load.** The seven rows stay; the new section 2.1 puts the load on the services that carry it, in the words of
   Arch v5 slide 33, and adds the 2031 horizon (about 47,389 open cases) that the source stops short of (GAP-2060).
5. **Scaling.** The two obsolete bullets become the 19-service shape (API deployment of 2 pods, worker deployment scaled
   by KEDA on the task-queue backlog or consumer lag) and the rwb-reporting read model in place of the data lake
   (ADR-013, ADR-016, ADR-018, DP-17). The other three bullets stay word for word and one paragraph names the owner of
   each object they mention (P7, P5, P1).
6. **Backup.** The three rows stay; section 4.1 adds an owner per store and the two stores the target architecture adds
   (Temporal persistence, Kafka topics), and section 4.2 describes what a restore of one service looks like (outbox
   replay, inbox dedupe, history replay, stuck-workflow scan JOB-21).
7. **Degraded modes.** The five rows stay; section 5.1 covers one of the 19 services down with the litigation example of
   Arch v5 slide 34, and section 5.2 gives the eight failures inside one service that the Temporal and Drools design
   details, each with an owner (ADR-023).
8. **Tests.** The four bullets stay and gain the story of each: RWB-ITG-TE009-ITG for the load test (the split of
   RWB-TE-009), RWB-PLT-NF06-DB with the ACE DBA for the failover, P5 rwb-document with RWB-PLT-DB for the restore, and
   the replay gate, contract and boundary tests for every service (section 6.1).
9. **Decisions.** DL11 stays as the only decision reference of the source; DL44 to DL49 and ADR-013 to ADR-023 are cited
   where the realignment needs them, all from `_work/msr/plan/ids.json`.

## 4. Owners

Every owner in the document is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`,
or a platform epic of Rules §R5.1 (RWB-PLT-DB, RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-EDGE, RWB-PLT-OBS). No owner is a team
type and no owner is a person; the team-type phrases of Rules §R5.3 are not used. Two components the source needs have no
row in the map (gateway-bff and the partner gateway) and both are named with the platform epic that owns the edge, with a
gap row for the missing map row (GAP-2063).

## 5. Registers

- Gap rows written: **10** candidate rows, `GAP-2057` to `GAP-2066`, in `_work/msr/gaps/B-TECH-11.jsonl`
  (1 Conflict of document control, 1 Conflict of capacity figures, 2 Outdated, 4 Missing, 1 Ambiguous, plus the missing
  RPO and RTO row; 3 of severity P2 and 7 of P3).
- Assumption rows written: **14** candidate rows, `ASM-3306` to `ASM-3319`, in
  `_work/msr/assumptions/B-TECH-11.jsonl` (10 High, 4 Medium).
- Every gap row names its assumption; every assumption names its gap where it has one. The document cites all 10 gap rows
  and all 14 assumption rows, and `verify.py` confirms that every citation resolves to a row.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-11 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify.py` reports PASS: header lines 1 and 2 present, the D-RCV-60 change-log row present, 0 unexplained missing lines
of version 2, sections 1 to 6 in order, 12 subsections, 15 tables, 24 resolved citations, 0 gap rows uncited, and no
bullet rendered twice. C12 finds no person name and no email address in the files of this WP, C13 finds no issue-tracker
reference, and C18 finds no write outside the "Write only" list and no change to a story master. The v2 document is
unchanged on disk.

## 7. Status and boundaries

The document is issued in **Draft**: no approval is recorded for this run (ASM-3318). No later lifecycle stage
was started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. No other
document of the family was touched.
