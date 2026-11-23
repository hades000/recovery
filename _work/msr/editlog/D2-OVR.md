# Edit log - WP D2-OVR (Recovery Workbench Project Overview next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `12 Project communication/Recovery Workbench Project Overview v5.pptx`
- `_work/msr/docs/D2-OVR/slides.md`
- `_work/msr/docs/D2-OVR/prepare.py`
- `_work/msr/docs/D2-OVR/layout.py`
- `_work/msr/docs/D2-OVR/title_size.py`
- `_work/msr/docs/D2-OVR/verify/Recovery Workbench Project Overview v5.md`
- `_work/msr/gaps/D2-OVR.jsonl`
- `_work/msr/assumptions/D2-OVR.jsonl`
- `_work/msr/editlog/D2-OVR.md`

Scratch only (`_work/msr/docs/D2-OVR/`): the text of the five appended slides, the property and
release-date writer, the layout script that fits the new slides to the deck grid and puts the
document-control slide first, the title-size fix, and the re-extract used for verification. The
converted source text was written by the conversion tool to `_work/msr/extract/D2-OVR/`, the folder
the WP names.

## What was done

The source `12 Project communication/Recovery Workbench Project Overview v4.pptx` was never edited.
It was converted to text for reading, copied to `... v5.pptx` with `compat/office_write.py copy`,
and the new version was built on the copy only.

1. **Every slide, ID, number and date of the source kept.** The source has 10 slides. Version 5 has
   15: the 10 source slides in their order, plus a document-control slide first and four
   realignment slides last. A line-for-line comparison of the re-extracted v5 text against the v4
   text finds slides 2 to 11 identical to source slides 1 to 10, with one difference only: the
   eight release dates on the plan slide. Every number (42 applications, 21/23/26 days, 1,486 days,
   73 L3 processes with 38/17/7/9/2 and 52/23/10/12/3 percent, 66.3% to 73%, 50 to 13, 1,095 days),
   every ID (DL01, DL02, DL06, DL12, DL16, DL17, DL18, DL22, DL23, DL32, DL33, E1 to E8) and every
   date of the source (28 October 2026, 30 Nov 2026 to 30 Jun 2027, and the needed-by dates 28 Oct,
   30 Oct, 7 Nov, 6 Nov, 13 Nov, 30 Nov) is copied unchanged.
2. **Release dates marked tentative.** The eight Release cells of the plan slide read
   `30 Nov 2026 (tentative)` to `30 Jun 2027 (tentative)`. No date was moved, and no date is raised
   as a gap (U7, DL48). The 28 October 2026 date of the source title slide is not a release date and
   is unchanged.
3. **Header and change log.** Slide 1 is the document-control slide. Its first line, which is the
   slide title, is `SCB Collections and Recovery. Henka Group, 22 November 2026.` and its first body
   line is `(C) Siam Commercial Bank and Henka Pte Ltd`: the two header lines of Template and Rules
   §R8.1. The slide then carries the version, the tool line, the supersession of version 4, the
   change-log row `v5, 22 November 2026, D-RCV-60 microservice realignment,
   T3 Code / OpenCode / DeepSeek v4.1 Flash`, and the Draft status with its assumption row.
4. **Realignment summary (the only content change).** Slide 12 states D-RCV-60 and Architecture v5:
   Recovery stays part of ACE, recovery-core is split into 19 services (P1 to P10, S1 to S9), and
   each service owns its schema `rwb_<name>`, REST base `/api/recovery/<name>/v1`, topic
   `rwb.<name>.events.v1` and task queue `rwb-<name>` in namespace `rwb-recovery`, with one
   reusable Temporal layer and embedded Drools governed from rwb-decision. It also states what does
   not change: the six-stage journey, the eight routes, the five decision steps, the CMMN 1.1 case
   model, rules as versioned data and one decision log entry per decision.
5. **Ownership Map for every owner.** Slide 13 lists the 19 services by Arch v5 wave with the
   service name as it stands in the Services sheet of `Ownership Map v1` (P1 rwb-source-data to
   S9 rwb-partner) and says that the owner of each row is that service. Slide 14 uses the map, not
   the source deck, for every owner it names: case list and parameters and reference data P3
   rwb-case, document hub P5 rwb-document, partner portal S9 rwb-partner, decision log and rules
   P7 rwb-decision, DoA table P4 rwb-access, AI preparation P10 rwb-agent. No person is named and
   no team is named as an owner, because R5.3 keeps the owner a suggestion only.
6. **Realignment decisions.** Slide 15 points to Architecture v5 slides 13 to 20 and 41 to 44, to
   D-RCV-60 and DL44 to DL49, to ADR-013 to ADR-023, to the service, platform and integration epics
   of R5.1, and to the run material of folder 22 and the registers of folder 23. The IDs come from
   `_work/msr/plan/ids.json`; nothing outside that allocation is used.
7. **Reading the source slides with the change.** Version 4 says "one service, one repository and
   one front end" (source slides 2 and 7) and that sentence is kept word for word, as the WP
   requires. Slide 14 states how it is read under the realignment and cites the conflict row; the
   conflict is recorded in full as CG-D2-OVR-1.
8. **Document properties repaired.** The source copy carries a person name in the author and
   last-modified-by properties. Version 5 sets author `SCB Collections and Recovery`,
   last-modified-by the tool line of this run, title `Recovery Workbench Project Overview v5`, the
   §R8.1 subject, revision 5, and 22 November 2026 as created and modified. A scan of every part of
   the new pptx finds no person name, no e-mail address and no issue-tracker reference.
9. **Layout.** The five new slides are set on the deck grid: title at 24 pt bold in the deck purple
   (18 pt on the document-control slide, whose title is the header line), a thin rule under the
   title, body at 14 pt, and a page number in the source position. The ten source slides are
   untouched, including their pictures, tables, connectors and page numbers.
10. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp D2-OVR --quick`
    passes C02, C03, C05, C12, C13 and C18. C14 (header), C17 (every CG and ASM citation has a row),
    C20 (tool line) and a repeat of C12 and C13 were run against the same file set and also pass.

## Registers

- Gap rows: 4 (`CG-D2-OVR-1` to `CG-D2-OVR-4`): Conflict 1 (documentation, the one-service
  wording), Ambiguous 1 (documentation, service wave to release), Missing 2 (experience 1,
  governance 1). Severity: P3 for all four. No gap row raises a date.
- Assumption rows: 4 (`ASM-D2-OVR-1` to `ASM-D2-OVR-4`), confidence High 1, Medium 3, Low 0.
- Every missing value in the deck is the R9 placeholder with its CG and ASM pair. The 19 service
  names, schemas, REST bases, topics, queues and waves, the decision and ADR IDs, the epic codes and
  the dates are copied from the sources character for character; no value is invented.

## Not done, by rule

- No approval was sought and none is recorded; the deck is issued as Draft.
- No master file was written, no register was numbered, and no source file was edited.
- No issue tracker, Confluence, repository, Figma or web call was made, and no commit was created.
