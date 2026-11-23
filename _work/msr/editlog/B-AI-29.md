# Edit log — WP B-AI-29 (Recovery Workbench AI and Agent Architecture next version)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026. Fanout: 0 (one worker, no subagents).

Sources read: `08 AI and agents/Recovery Workbench AI and Agent Architecture v2.pptx` (all 11 slides, every
shape and table), its converted text in the run extract folder for this work package,
`22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (§R1, §R3, §R5, §R8,
§R9), `_work/msr/plan/ownership.json` and `22 Microservice Realignment/Recovery Workbench Microservice Ownership
Map v1.xlsx` (Read me, Services, Workflows and activities, Events, Parameters; Tables and Endpoints for the P10
rows), `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 2, 7, 8, 13 to
20, 35, 36, 38, 39, 41 and 43), `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text
Extract v1.md` (slides 12, 13 and 14), `_work/msr/plan/split_plan.json` ("stats" and "legacy" only; this document
is a deck family, not a story family, so no legacy key maps to it) and `_work/msr/plan/ids.json`.
Nothing read was edited; the v2 deck was opened read-only and copied, and the copy is the only deck that changed.

## Files written

- 08 AI and agents/Recovery Workbench AI and Agent Architecture v3.pptx
- _work/msr/gaps/B-AI-29.jsonl
- _work/msr/assumptions/B-AI-29.jsonl
- _work/msr/editlog/B-AI-29.md

Scratch files under `_work/msr/docs/B-AI-29/` (build and verification only, not outputs of the run):

- _work/msr/docs/B-AI-29/build.py
- _work/msr/docs/B-AI-29/gen_registers.py
- _work/msr/docs/B-AI-29/verify.py
- _work/msr/docs/B-AI-29/v2-slide-text.txt
- _work/msr/docs/B-AI-29/v3-slide-text.txt
- _work/msr/docs/B-AI-29/render/Recovery Workbench AI and Agent Architecture v3.pdf

The converted source text of this work package sits in the run extract folder, `_work/msr/extract/B-AI-29`, and was
made with `compat/convert_sources.py`; the source deck itself was never opened for writing.

## 1. How the next version was produced

The source deck was never edited. `compat/office_write.py copy` made
`Recovery Workbench AI and Agent Architecture v3.pptx` from the v2 deck, and `build.py` then changed only the copy:

1. **Ten new slides, one of them the read-me.** Each new slide is built from the deck's own shapes: the 24 pt bold
   Aptos title in 4E297F, the hairline rule and the page-number box are copied from source slide 6, the note text box
   from source slide 7, and every table uses the deck's own table style `{5940675A-B579-460E-94D1-54222C63F5DA}`
   with the header fill DCD3EB, the 4E297F headings, the white body and the C8C8C8 hairline under each row. Table
   heights are measured before they are written (characters per line by column width and font size) and the largest
   font that fits the 4.55 M EMU table area is chosen: 11 pt on the change table, 11 pt on the ten-step workflow,
   12 pt on the other seven tables. No table reaches the note, and no note reaches the page number.
2. **The read-me slide placed second.** The title slide of version 2 stays slide 1, so the deck still opens on its
   cover of 28 October 2026, and the read-me slide carries the two header lines of Template and Rules §R8.1 as its
   first two lines. Source slides 2 to 11 therefore sit at positions 3 to 12.
3. **Page numbers follow the position.** Only the number in the page-number box of the ten numbered source slides
   changed (2 to 11 became 3 to 12); the new slides are numbered 13 to 21, so no number repeats or skips.
4. **Document properties.** The v2 file carries a person name in `author`. The new file is set to `Henka Group` and
   `T3 Code / OpenCode / DeepSeek v4.1 Flash`, title `Recovery Workbench AI and Agent Architecture v3`, revision 3
   and modified 22 November 2026 (rule 4).

**Header, change log and status.** The read-me slide opens with
`SCB Collections and Recovery. Henka Group, 22 November 2026.` and `(C) Siam Commercial Bank and Henka Pte Ltd`, then
the change-log row `3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
Flash`, the row it follows (`2, 28 October 2026, the issued deck`), what changes, what is added, the owner rule, the
dates rule, the decisions used, the placeholder rule and the status `Draft. No approval is recorded for this version
(ASM-0122)`.

## 2. Fidelity to version 2

`verify.py` extracts every shape and every table cell of both decks and compares them:

| Item | Result |
|---|---|
| Non-empty lines of version 2, page numbers excluded | 370 |
| Lines of version 2 present verbatim in version 3 | 370 of 370 |
| Lines of version 2 missing and not listed as changed | 0 |
| Slides | 21: the 11 of version 2 in their order, the read-me slide at 2, the 9 new slides at 13 to 21 |
| Change to a source slide | the page number only (2 to 11 became 3 to 12) |
| Tables | 18 (9 of the source, 9 new) |
| Header lines 1 and 2 of §R8.1 | Present, as the first two lines of the read-me slide |
| Change-log row with D-RCV-60 and the tool line | Present |
| Unresolved CG/ASM citations | 0 of 28 |

Every table, ID, number and date of version 2 is kept character for character: the 25 sub-decisions on slides 3 and
4 with their modes, run-by, autonomy bands and first epics; the eighteen sub-decision rows and the three automated
steps (X1-X7, X6, P8, P5); the six components, the six steps and the six component rows of slide 5; the twelve agents
with their live and shadow epics on slide 6; the ten models with their model inventory IDs on slide 7; the eight
guardrails on slide 8; the five autonomy levels on slide 9; the six who govern on slide 10; and the three open
decisions DL33, DL11 and DL26 on slide 11. The title slide keeps `Henka Group, 28 October 2026`. Version 2 carries no
release date and none is added; the document date is kept as issued and read as tentative under U7 and DL48
(ASM-0124).

## 3. What version 3 adds (slides 13 to 21)

1. **The change table (13).** Seven rows, each a statement of the source deck with its version 3 reading, the owner
   and the decision behind it: the six parts of slide 5 become one service; the model endpoint becomes INT-23; the
   60-second rule becomes the AgentRunWorkflow timer; the decision log becomes the local record plus the shared topic;
   the twelve agents are started by the service that owns the stage decision; the model output is read through P1;
   autonomy and governance are unchanged.
2. **The rwb-agent contract (14).** Nine rows: service, REST base, REST consumed, outside call, events consumed,
   published events, Temporal, tables owned and what the service does not own, transcribed from the Architecture v5
   service contract on slide 16, the Ownership Map v1 and Rules R4.
3. **The six parts of slide 5, placed (15).** Orchestrator, tool gateway, guardrail checker, prompt and policy
   store, evaluation harness and model endpoint, each with what it is inside the service, its call type and its owner
   (ASM-0126, ASM-0128, ASM-0134).
4. **AgentRunWorkflow step by step (16).** Ten steps from the event that starts a run to the ledger, with the call
   type of each: the child workflow, the policy read, the tool reads, the model call, the guardrail check, the 60 s
   timer, the run row and the local decision record, AgentRunCompleted, and P7 collecting the record.
5. **The 60-second rule (17).** Six situations — a timeout, a schema failure, an action outside the list, a low
   confidence, an endpoint that does not answer, and the unnamed rule for ten agents — each with what happens, where
   it is recorded and who owns it (GAP-0074, GAP-0076).
6. **The twelve agents and their callers (18).** One row per agent of source slide 6 with the service and workflow
   that start the run and the live epic as issued; three rows come from a service contract, nine follow the stage
   owner (GAP-0071; ASM-0130).
7. **The guardrails, and where each is enforced (19).** The eight rows of source slide 8 with the mechanism that
   enforces them in version 3 and the owner: the tool gateway, allowed actions, schema check, confidence floor,
   fallback, personal data, versions and the decision log.
8. **Autonomy and governance (20).** The five levels of source slide 9 and their measures, unchanged, with who acts,
   where the level is held and what is measured; the note keeps the committee and Model Risk approval and records
   the level as configuration (ASM-0133, ASM-0137).
9. **What stays open (21).** The ten points this version cannot close, each with its CG and ASM row and an owner
   role, and a note that DL33, DL11 and DL26 stay open on source slide 11.

## 4. Owners

Every owner is a service code of the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json` (P1 to P10,
S1 to S9), a platform epic (RWB-PLT-*), or a party outside the 19 services (ACE Common, Enterprise AI, COLLINS)
(ASM-0125). No owner is taken from a story master, and no owner is a team type or a person. The agent runtime is
P10 `rwb-agent` throughout, with schema `rwb_agent`, REST base `/api/recovery/agent/v1`, topic
`rwb.agent.events.v1` and queue `rwb-agent`, as Rules §R4 and the Ownership Map give them. Governance is not given
a service code: the six who govern on source slide 10 are bank functions outside the 19 services
(ASM-0133).

## 5. Registers

- Gap rows written: **10** candidate rows, `GAP-0069` to `GAP-0078`, in `_work/msr/gaps/B-AI-29.jsonl`:
  3 Conflict, 3 Missing and 4 Ambiguous; 5 of severity P2 and 5 of P3; needed by wave 0 (1 row), wave 1 (8 rows)
  and wave 2 (1 row).
- Assumption rows written: **18** candidate rows, `ASM-0121` to `ASM-0138`, in
  `_work/msr/assumptions/B-AI-29.jsonl`: 8 High and 10 Medium.
- Nine of the eighteen assumptions answer a gap (ASM-7 to ASM-10, ASM-12, ASM-13, ASM-15, ASM-16 and ASM-18), and
  each of the ten gaps names its assumption; ASM-7 answers both CG-6 and CG-8. Nine carry no gap: the reading rule
  for the kept slides, the Draft status, the slide order, the unchanged dates, the owner rule, the components of
  slide 5, the decision record, the evaluation sets and the autonomy level as configuration.
- Every citation in the deck resolves to a row: 28 distinct CG/ASM citations (all 10 gaps and all 18 assumptions),
  0 unresolved.
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## 6. Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-AI-29 --quick`

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

`verify.py` reports PASS on its nine rules: 21 slides in the order of version 2, 370 of 370 source lines present, the
two header lines first on the read-me slide, the D-RCV-60 change-log row and the Draft status, page numbers equal to
the position, 28 of 28 citations resolved, no pipe text left on a new slide, every shape inside the slide with no
table over the note, and the document properties on the organisation and the tool. C01, C14, C17 and C20 were also
run and pass: no file of the source baseline changed on disk, the header lines are present, every register row has
its required keys and no citation is orphaned, and no edit log of the run is missing the tool line. A PDF render of
all 21 slides confirms the new tables fit inside the table area, with no row clipped and no overlap with the note or
the page number.

## 7. Status and boundaries

The deck is issued in **Draft**: no approval is recorded for this run (ASM-0122). No later lifecycle stage was
started. No issue tracker, wiki, repository, design tool or web call was made, and no commit was created. The v2 deck
and the other documents of folder 08 were not touched, and no story master was changed.
