# Edit log B-REQ-PRD-S7 - PRD S7 rwb-writeoff v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-S7
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md`
- `_work/msr/docs/B-REQ-PRD-S7/ownership/Recovery Workbench Microservice Ownership Map v1.md`
- `_work/msr/docs/B-REQ-PRD-S7/write_registers.py`
- `_work/msr/docs/B-REQ-PRD-S7/verify.py`
- `_work/msr/gaps/B-REQ-PRD-S7.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S7.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S7.md`

The remaining files in the scratch folder `_work/msr/docs/B-REQ-PRD-S7/` are read extracts cut from the sources already converted under `_work/msr/extract/` and from the two BRD files in folder 03: `arch_*.txt` and `temporal_*.txt` (Architecture v5 and the Temporal and Drools design), `prog_*.txt` and `brd_*.txt` and `e38_*.txt` (Program v5 and Epics 3 to 8 v1), `rwo_rules.txt` (Business Rules and Routing Logic v4), `ldm_wo.txt` and `schema_wo.txt` (Logical Data Model v8 and Physical Schema v6), `owner_*.txt` (Ownership Map), `dl_hits.txt` (Decision Log v10) and `def_hits_Recovery_Wor.txt` (a search for DEF-05 that found nothing outside the FSD's change note). The Ownership Map was converted to text with `python -I "22 Microservice Realignment/compat/convert_sources.py"` into the scratch folder, so every operation, event, workflow, table and job owner in the PRD is taken from the map rather than reasoned. `write_registers.py` writes the two jsonl registers once so that no id is rewritten; `verify.py` checks the id sets, the citations, the section order, the header, the change-log row, the service facts, the BR and FSD-requirement columns of every FR row and the tentativeness of every release date, against the written PRD, and is scratch only.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md` is version 1 of the family: the folder `03 Requirements and specifications/PRD/` holds P1 to P10 and S1 and no S7 file before this run, so there is no earlier version to supersede. The first two lines are the header of Template and Rules section R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD v3 (15 November 2026) change note character for character, marks FSD v1 and v2 as not specified, and lists every source ID the PRD preserves.

Thirteen sections are written in the order the agent contract sets, followed by Appendix A: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the twelve confirmed v5 constraints); personas and roles; current-versus-target journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty.

Volume: 17 capabilities (CAP-S7-001 to CAP-S7-017), 41 functional requirements (FR-S7-001 to FR-S7-041), 36 non-functional requirements (NFR-S7-001 to NFR-S7-036), 26 acceptance criteria in GIVEN/WHEN/THEN form (AC-S7-001 to AC-S7-026), 16 personas (ROL-S7-01 to ROL-S7-16), 6 journeys (JRN-S7-01 to JRN-S7-06) and 17 open questions (OQ-S7-01 to OQ-S7-17).

Requirement mapping: every FR row carries the FSD requirement it serves (REQ-S7-001 to REQ-S7-008), the BRD requirement behind it (BR-051 to BR-059) and, where one applies, the routing rule of Business Rules and Routing Logic v4 that carries the transition (R-WO-01 to R-WO-51); section 11.2 gives the BR to capability to FR/NFR to AC chain per requirement, including BR-058 and RULE-019 to RULE-022. BR coverage is 8 of 8 program requirements, 9 of 9 BRD requirements of E6 that name this service, and all four rules; there is no gap. The requirement substance, the FSD feature IDs (FEAT-WOF-01 to FEAT-WOF-16), the FSD acceptance criteria IDs (AC-S7-001-01 to AC-S7-016-01 with their exception and background rows), the validation and business rule IDs (VR-S7-001-1 to VR-S7-016-1, BR-S7-001 to BR-S7-016), the message IDs (MSG-S7-001, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), the list IDs (LOV-STAGE, LOV-TREATMENT, LOV-ROUTE-SET, LOV-CAPABILITY), the case states named by the routing rules, the field IDs of the Logical Data Model (DF-FIN-010 to DF-FIN-020, DF-ACE-261 to DF-ACE-269) and the screen ID (SCR-27) are preserved; no number was recomputed and no value was recomputed.

Service facts follow section R4 for S7 and the Ownership Map Services sheet: schema `rwb_writeoff`, REST base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1`, task queue `rwb-writeoff`, Java package `th.co.scb.ace.workbench.recovery.writeoff`, epic `RWB-SVC-S7`, wave 4. Owners: every owner in section 9 and section 11.3 is a role or a service code from the Ownership Map or the BRD; no person is named. Release dates are copied unchanged and marked "(tentative)": E6 30 April 2027, with wave 4 also carrying EP07 at 31 May 2027 and EP08 at 30 June 2027. No solution design is added beyond the v5 constraints: no class, no column definition beyond the field set the model already holds, and no endpoint is designed here, and the operations, activities and events named are only those the architecture, the design and the map already fix.

Rulings that change the FSD output, each carried as a gap and an assumption row: the service reads the GL outcome, the balances and the batch status through the rwb-source-data contract and reads no ACE view (CG-1); the posting runs as a step on rwb-payment's queue with the outcome read back through P1, so this service records the posting reference and never calls ALS or the general ledger (CG-2); the four entity groups are named as entities because the map lists one table (CG-3); the collection operations slide 20 names are published even though the register holds only two operations (CG-4); the Finance feed leaves through P2 (CG-5); the pack document is P5's (CG-6); the agency is reached through S9 in the same wave (CG-7); a charged-off population is handed to S6 (CG-8); the case state stays with rwb-case (CG-9); the scan is a Temporal Schedule that also tests the ALS batch (CG-10, ruled and carried from ASM-0066); the posting waits for the ledger acknowledgement under strict mode (CG-16); the pack agent runs with a template fallback (CG-20); a post charge-off payment is matched by P8 and reaches this service as ProceedsMatched (CG-21); completeness is published from rwb-reporting because the data lake is removed (CG-22).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-S7.jsonl` - 24 rows, GAP-1792 to GAP-1815, with the keys of section R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 13 Missing, 8 Conflict, 3 Ambiguous. Severity: 2 P1 (the read path and the posting owner, which gate every requirement of the service), 17 P2, 5 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-S7.jsonl` - 26 rows, ASM-2968 to ASM-2993, with the keys of section R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption, as the source-precedence rule requires; 2 rows carry no gap (dates unchanged and tentative; roles only, no names).
- Counts: CG = 24, ASM = 26. Numbering is left to step D1; the ids above are the candidate ids of this work package, and every citation in the PRD resolves to a row in one of the two files or to a row of the A6 and BRD registers that the Ownership Map and the epic BRD rulings already hold (ASM-0066, ASM-013, ASM-014, and the CG-B-REQ-BRD-E38 ids the epic open questions carry).

## Deliberate omissions

- The traceability matrix under `_work/msr/` and the AISDLC `requirement/Traceability_Matrix.md` were not written: both sit outside this work package's write list, and rule 1 forbids writing outside it. The chain BR to CAP to FR/NFR to AC is therefore carried inside the PRD in section 11.2, so no trace is lost.
- No master, BRD, FSD, TSD, story or data-model file was edited. The only source converted in this run is the Ownership Map, and the conversion writes into the scratch folder.
- No issue tracker, wiki, repository or web call was made; no git command was run.
- No value was invented where a source has none: the tax criteria and the two tracks (Q-006), the exception owner and its time limit (Q-007), the write-off cap (RISK-004), the committee levels and limits (DL18/Q-001), the retention periods and masking rules (DL26/Q-012), the first-time-right baseline (Q-023) and DEF-05 are all carried as open questions with a named owner role.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S7 --quick` - C02, C03, C05, C12, C13, C18 all PASS.
- The document checks that apply to a non-story PRD were run on the whole stage-B output set: C14 (the R8.1 header lines inside the first six lines) PASS, C15 (no release date changed, every release date marked tentative) PASS, C16 (no unknown service name in a topic, REST base or queue) PASS with 6 findings in other work packages' story files and none in this work package, C17 (every cited CG and ASM id has a register row) PASS with 190 findings in other work packages' story files and none here, C20 (tool line present, no wrong tool attribution) PASS. The stage-B C02, C04, C16 and C17 failures name only story files of work packages outside B-REQ-PRD-S7.
- The scratch verifier `verify.py` reports 0 failures on: header lines, change-log row, all citations, the 17/41/36/26 id sets being contiguous, every FR and AC being a table row, every FR naming a capability of section 5, a BR of BR-051 to BR-059 and an FSD requirement of REQ-S7-001 to REQ-S7-008, all nine BRs having at least one FR, the thirteen section headings in order, the four service facts, the absence of the old monolith API base, and the absence of any issue-tracker reference.
