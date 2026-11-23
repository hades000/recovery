# Edit log B-REQ-PRD-P7

| Item | Value |
|---|---|
| Work package | B-REQ-PRD-P7 — PRD P7 rwb-decision v1 (PRD Builder) |
| Agent | aisdlc-prd-builder |
| Decision | D-RCV-60 |
| Date | 22 November 2026 |
| Tool | T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Fanout | 0 |

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md`
- `_work/msr/gaps/B-REQ-PRD-P7.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P7.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P7.md`
- `_work/msr/docs/B-REQ-PRD-P7/notes.md`
- `_work/msr/docs/B-REQ-PRD-P7/write_rows.py`

No source document was edited. The PRD is a new v1: no P7 PRD existed in `03 Requirements and specifications/PRD/` (only P1 and P4), so the next version of the family is v1.

## What the new version contains

- Header lines of Template and Rules §R8.1, front matter with `status: Draft`, `brd` and `fsd`, and the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash".
- Sections 1 to 13 plus Appendix A, as the WP requires: document control and change log; product overview and relationship to ACE (new, reused, moved, removed); personas and roles; current and target journeys; capabilities (CAP-P7-001 to CAP-P7-018, each with BR IDs and MoSCoW); functional requirements (FR-P7-001 to FR-P7-036, each with its FSD REQ ID); non-functional requirements (NFR-P7-001 to NFR-P7-022); data requirements with classification; integration points and their questions; release slicing by wave (0, 1, 2, 3, 4) with release dates marked (tentative); acceptance criteria (AC-P7-001 to AC-P7-022) with source evidence and a BR → CAP → FR/NFR → AC trace summary; open questions (OQ-P7-01 to OQ-P7-12) with the assumptions they rest on; and an empty approval table with the next step.
- Realignment only: the interaction ledger moves to rwb-source-data; the data-lake copy is removed; the notice pipeline, template catalog and proof of delivery move to rwb-comms; rule governance stays here while evaluation moves to the owning service; the DoA table is read from rwb-access; the strict mode, WORM seal and 5-minute completeness target come from Architecture v5. No design beyond the confirmed v5 constraints; every owner is the Ownership Map's.

## Registers

| Register | File | Rows |
|---|---|---|
| Candidate gaps | `_work/msr/gaps/B-REQ-PRD-P7.jsonl` | 12 (GAP-1612 to GAP-1623) |
| Candidate assumptions | `_work/msr/assumptions/B-REQ-PRD-P7.jsonl` | 14 (ASM-2746 to ASM-2759) |

Gap rows written: 12. Assumption rows written: 14. Row IDs are candidate IDs in the WP form; step D1 renumbers them as GAP-nnnn and ASM-nnnn.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P7 --quick` — C02, C03, C05, C12, C13 and C18 all PASS.

## Notes for the assembler

- The BR → CAP → FR/NFR → AC rows are in section 11.2 of the PRD. This WP may not write `requirement/Traceability_Matrix.md`, so the rows are left there for the assembler.
- No issue tracker, wiki, source-control service, design tool or web call was made, no git command was run, and no later lifecycle stage was started.
- BR coverage: 19 of 34 P7 program requirements are served here; 1 is removed with the data lake (REQ-DRI-009) and 14 move to rwb-source-data (REQ-ILG-001 to REQ-ILG-014). No live requirement is without a functional requirement.
