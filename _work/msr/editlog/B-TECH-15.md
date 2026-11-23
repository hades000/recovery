# Edit log — WP B-TECH-15 (Recovery Workbench Information Flow next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `05 Technical architecture/Recovery Workbench Information Flow v5.pptx` (all 11 slides, every
shape and table), its converted text in the run extract folder for this work package,
`22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5, §R8,
§R9), `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership
Map v1.xlsx` (Read me, Services, Tables, Endpoints, Events, Workflows and activities, Jobs, Parameters, Rulings),
`22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 2 to 44, in particular
the connection matrix on 13, the 19 service contracts on 14 to 20, the event catalogues on 42 and 43 and the job map
on 44), `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (slides 13 to
16), `_work/msr/plan/split_plan.json` ("stats" and "legacy" only, 358 legacy keys) and `_work/msr/plan/ids.json`.
The physical schema extract was also read for the 30 view names. Nothing read was edited; the v5 deck was opened
read-only, copied, and the copy is the only deck that changed.

## Files written

- 05 Technical architecture/Recovery Workbench Information Flow v6.pptx
- _work/msr/gaps/B-TECH-15.jsonl
- _work/msr/assumptions/B-TECH-15.jsonl
- _work/msr/editlog/B-TECH-15.md

Scratch files under `_work/msr/docs/B-TECH-15/` (build and verification only, not outputs of the run):

- _work/msr/docs/B-TECH-15/build.py
- _work/msr/docs/B-TECH-15/verify.py
- _work/msr/docs/B-TECH-15/slides.md
- _work/msr/docs/B-TECH-15/source-v5-pptx-text.txt
- _work/msr/docs/B-TECH-15/v6-slide-text.txt

The converted source text of this work package sits in the run extract folder, `_work/msr/extract/B-TECH-15`.

## 1. How the next version was produced

The source deck was never edited. `compat/office_write.py copy` made
`Recovery Workbench Information Flow v6.pptx` from the v5 deck, and `build.py` then changed only the copy:

1. **Eleven new slides, 13 to 22, ten of them with a table.** Each one is built from the deck's own shapes: the
   title text box, the hairline
   rule, the page-number box and the note text box are copied from source slide 4, so the new slides keep the 24 pt
   bold Aptos title in 4E297F at the geometry of the source title, the same rule, the same note style, and the same
   table look (header fill DCD3EB with 4E297F bold headings, body fill FFFFFF, the C8C8C8 hairline under each row,
   the same cell margins). Table rows are measured before they are written (characters per line by column width and
   font size) and the largest font that fits the 4.60 M EMU table area is chosen, 12 pt on the short tables, 11 pt on
   the nine service rows, 10 pt on the ten service rows, 9.5 pt on the 13-row change table. No table reaches the note.
2. **The read-me slide placed second.** The title slide of version 5 stays slide 1, so the deck still opens on its
   cover of 15 November 2026, and the read-me slide carries the two header lines of Template and Rules §R8.1 as its
   first two lines. Source slides 2 to 11 therefore sit at positions 3 to 12.
3. **Page numbers follow the position.** Only the number in the page-number box of the ten numbered source slides
   changed (2 to 11 became 3 to 12); the new slides are numbered 13 to 22, so no number repeats or skips.
4. **Document properties.** The v5 file carries a person name in `author` and `last_modified_by`. The new file is set
   to `Henka Group` and `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench Information Flow v6`,
   revision 6 and modified 22 November 2026 (rule 4).

**Header, change log and status.** The read-me slide opens with
`SCB Collections and Recovery. Henka Group, 22 November 2026.` and `(C) Siam Commercial Bank and Henka Pte Ltd`, then
the change-log row `6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`, the row it follows (`5, 15 November 2026, the issued deck`), what changes, what is added, the owner and wave
rule, the dates rule, the decisions used, the placeholder rule and the status `Draft. No approval is recorded for this
version (ASM-3370)`.

## 2. Fidelity to version 5

`verify.py` extracts every shape and every table cell of both decks and compares them slide by slide:

| Item | Result |
|---|---|
| Non-empty lines of version 5, page numbers excluded | 331 (319 distinct) |
| Lines of version 5 present verbatim in version 6 | 331 of 331 |
| Lines of version 5 missing and not listed as changed | 0 |
| Slides | 22: the 11 of version 5 in their order, the read-me slide at 2, the 11 new slides at 13 to 22 |
| Change to a source slide | the page number only (2 to 11 became 3 to 12) |
| Tables | 19 (9 of the source, 10 new) |
| Header lines 1 and 2 of §R8.1 | Present, as the first two lines of the read-me slide |
| Change-log row with D-RCV-60 and the tool line | Present |
| Unresolved CG/ASM citations | 0 of 25 |

Every table, ID, number, date and word of version 5 is kept character for character: the two inbound boxes with their
source systems, the six daily rows I01 to I06 with their views and data products, the ten weekly, monthly and entered
rows I07 to I16, the eight outbound rows O01 to O08, the six decisions D5 to D9 with their freshness, the seven
fallback rows, the seven checks, the five same-day rows, and the eight rows of gaps and assumptions with DL06, DL25,
DL29, DL30, DL43, D-RCV-35 and the date "21 November" as issued. The title slide keeps `Henka Group, 15 November
2026`. Version 5 carries no release date and none is added; the two document dates are kept as issued and read as
tentative under U7 and DL48 (ASM-3381).

## 3. What version 6 adds (slides 13 to 22)

1. **The change table (13).** Twelve rows, each a flow of the source deck with the version 6 owner and the decision
   that carries it: P1 alone reads the 30 views (ADR-010, DP-05); 19 schemas and logins (ADR-014); the one module
   becomes P3, P7, P5 and S9 (ADR-013); Kafka gains the 19 business topics and the shared ledger topic (ADR-015,
   DP-09); O04 moves to P9 and O05 stays open (ADR-018, DP-17); O02 is split between P6 and P2 (DP-16); O03, I13,
   O06, I14, I15, I16 and O08 are placed; P3 owns caseId (ADR-011, DP-12).
2. **The ten platform services (14).** One row per service, P1 to P10, with its topic, its wave, the information it
   takes in and the information it sends out, transcribed from the Architecture v5 service contracts on slides 14 to
   20 and the Ownership Map (ASM-3384).
3. **The nine stage services (15).** The same shape for S1 to S9, including the workflows each one owns and the
   parent-child link to the CaseWorkflow.
4. **The events, in two slides (16, 17).** The 19 events the source slides actually use, with producer, consumers
   and topic, copied from the Architecture v5 catalogues on slides 42 and 43: AceDataReady, AceDataLate, CaseCreated,
   CaseStateChanged, DeviationRaised and Cleared, DocumentStored, DocumentFieldsExtracted, PartnerResultSubmitted,
   RulePackageInForce, TreatmentApproved, TreatmentBooked, PaymentMissed, ProceedsMatched, NoticeGenerated,
   NoticeDispatched, NoticeDelivered, WriteOffApproved and DecisionRecorded.
5. **One payment end to end (18).** Nine steps from ACE ingestion to the central ledger: P1 reads the payment and
   publishes AceDataReady, P3 starts DailyCaseRun, P8 finds no payment and publishes PaymentMissed, the case router
   signals the CaseWorkflow, S2 evaluates R-RES-27 and starts the 30-day cure period, RecordAndApply writes record,
   state and outbox in one transaction, and P7 collects DecisionRecorded within five minutes (Architecture v5 slide
   22; Temporal and Drools design slide 14).
6. **Five call types (19).** REST, Kafka event, Temporal, File and SQL view, with what travels, who owns the path and
   the limit of each (Architecture v5 slides 11 and 12).
7. **The shared platform (20).** gateway-bff with Redis, Kafka, Temporal, Airflow, Blob with WORM, the 30 views and
   ACE Common, each with its owner and where this deck uses it.
8. **The owner of each fallback (21).** The seven rows of source slide 8 with the service that acts, what it sends
   and what the user sees.
9. **What stays open (22).** The nine points this version cannot close, each with its CG and ASM row and an owner
   role, plus a note that DL06, DL30 and DL43 stay open on source slide 12.

## 4. Owners

Every owner is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`, a platform
epic (RWB-PLT-*), or a party outside the 19 services (ACE Common, WIN, NSS, LINE OA, partners, debt buyers)
(ASM-3382). No owner is taken from a story master, and no owner is a team type or a person. One flow has no
row to point at: gateway-bff, the Redis session and the App Gateway route, which the Map does not carry. They are
given to the platform edge epic RWB-PLT-EDGE and to RWB-PLT-N001-CON (DP-19) and raised as GAP-2099
(ASM-3372). The wave of every flow is the wave of its owning service in Rules §R4 (ASM-3383).

## 5. Registers

- Gap rows written: **9** candidate rows, `GAP-2099` to `GAP-2107`, in `_work/msr/gaps/B-TECH-15.jsonl`:
  3 Conflict, 3 Ambiguous, 2 Outdated, 1 Missing; 4 of severity P2 and 5 of P3; needed by wave 0 (1 row), wave 1
  (7 rows) and wave 3 (1 row).
- Assumption rows written: **16** candidate rows, `ASM-3369` to `ASM-3384`, in
  `_work/msr/assumptions/B-TECH-15.jsonl`: 9 High and 7 Medium.
- Nine of the sixteen assumptions answer a gap one for one (ASM-4 to ASM-12) and each of the nine gaps names its
  assumption. Seven carry no gap: the reading rule for the kept slides, the Draft status, the slide order and page
  numbers, the unchanged dates, the owner rule, the wave rule and the transcription rule.
- Every citation in the deck resolves to a row: 25 distinct CG/ASM citations (all 9 gaps and all 16 assumptions),
  0 unresolved.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-15 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify.py` reports PASS on its ten rules: slide count and order (22 slides, the 11 of version 5 in place), 331 of 331
source lines present, the header lines first on the read-me slide, the D-RCV-60 change-log row and the Draft status,
page numbers equal to the position, every shape inside the slide, no table over the note, no note over the table,
25 of 25 citations resolved, no pipe text left on a new slide, and the document properties on the organisation and the
tool. C01 was also run and passes: no file of the source baseline, the v5 deck included, changed on disk. Render checks
through a PDF conversion confirm the new slides fit, with no clipped row and no overlap with the page number.

## 7. Status and boundaries

The deck is issued in **Draft**: no approval is recorded for this run (ASM-3370). No later lifecycle stage was
started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. The v5 deck,
the v4 deck and the other document of this family were not touched, and no story master was changed.
