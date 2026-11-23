# Edit log B-REQ-PRD-S1 — PRD S1 rwb-valuation v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-S1
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md`
- `_work/msr/docs/B-REQ-PRD-S1/ownership/Recovery Workbench Microservice Ownership Map v1.md`
- `_work/msr/docs/B-REQ-PRD-S1/write_registers.py`
- `_work/msr/docs/B-REQ-PRD-S1/verify.py`
- `_work/msr/gaps/B-REQ-PRD-S1.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S1.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S1.md`

The Ownership Map was converted to text with `python -I "22 Microservice Realignment/compat/convert_sources.py"` into the scratch folder, so every operation, event, workflow, table and job owner in the PRD is taken from the map rather than reasoned. The register writer is scratch tooling: it writes the two jsonl files once so no id is rewritten. The verify script checks the id sets, the citations and the counts against the written PRD and is scratch only.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md` is version 1 of the family: the folder `03 Requirements and specifications/PRD/` held P1 to P4 and no S1 file before this run, so there is no earlier version to supersede (ASM-2844). The first two lines are the header of Template and Rules §R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD v3 (15 November 2026) change note character for character, marks FSD v1 and v2 as not specified, and lists every source ID the PRD preserves.

Thirteen sections are written in the order the agent contract sets, followed by Appendix A: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the ten confirmed v5 constraints); personas and roles; current-versus-target journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty.

Volume: 13 capabilities (CAP-S1-001 to CAP-S1-013), 28 functional requirements (FR-S1-001 to FR-S1-028), 29 non-functional requirements (NFR-S1-001 to NFR-S1-029), 20 acceptance criteria in GIVEN/WHEN/THEN form (AC-S1-001 to AC-S1-020), 12 personas (ROL-S1-01 to ROL-S1-12), 5 journeys (JRN-S1-01 to JRN-S1-05) and 15 open questions (OQ-S1-01 to OQ-S1-15).

Requirement mapping: every FR row carries the FSD requirement it serves (REQ-S1-001 to REQ-S1-008) and the BRD requirement behind it (BR-016 to BR-021), and §11.2 gives the BR to capability to FR/NFR to AC chain per requirement. BR coverage is 8 of 8 program requirements and 6 of 6 BRD requirements of E4 that name this service, with no gap. The requirement substance, the FSD feature IDs (FEAT-VAL-01 to FEAT-VAL-12), the FSD acceptance criteria IDs (AC-S1-001-01 to AC-S1-012-01 and their exception rows), the validation and business rule IDs (VR-S1-001-1 to VR-S1-012-1, BR-S1-001 to BR-S1-012), the message IDs (MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), the list ID (LOV-APPRAISAL) and the screen ID (SCR-13) are preserved; no number was recomputed and no value was recomputed.

Owners: every owner in §9 and §11.3 is a role or a service code from the Ownership Map or the BRD; no person is named. Service facts follow §R4 for S1: schema `rwb_valuation`, REST base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1`, task queue `rwb-valuation`, Java package `th.co.scb.ace.workbench.recovery.valuation`, epic `RWB-SVC-S1`, wave 3. Release dates are copied unchanged and marked "(tentative)": E3 31 January 2027, E4 28 February 2027, E8 30 June 2027. No solution design is added beyond the v5 constraints: no class, table definition or endpoint is designed here, and the operations, activities and events named are only those the architecture, the design and the map already fix.

Rulings that change the FSD output, each carried as a gap and an assumption row: the service reads collateral, appraisal, balance and score facts through the rwb-source-data contract and reads no ACE view (CG-1); the appraisal acceptance stays in P1's `valuation_ext` and is reached by contract (CG-2); the service's own table set is named as three entity groups because the map lists none (CG-3); the valuation order leaves through rwb-integration (CG-7); the route timers are durable workflow timers, not Quartz (CG-8); the route command path and the asset valuation paths are carried as open with a named owner (CG-5, CG-6); E3 consumes a published contract and fake one release before the service exists (CG-13).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-S1.jsonl` — 19 rows, GAP-1677 to GAP-1695, with the keys of §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 10 Missing, 5 Conflict, 3 Ambiguous, 1 Outdated. Severity: 1 P1 (the read path, which gates every requirement of the service), 12 P2, 6 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-S1.jsonl` — 24 rows, ASM-2825 to ASM-2848, with the keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption, as the source-precedence rule requires; 5 rows carry no gap (first version of the family, tentative dates, wave placement, roles only, the two requirement ID sets).
- Counts: CG = 19, ASM = 24. Numbering is left to step D1; the ids above are the candidate ids of this work package, and every citation in the PRD resolves to a row in one of the two files or in the A6 registers that the Ownership Map ruling ids point at.

## Deliberate omissions

- The traceability matrix in `requirement/Traceability_Matrix.md` was not updated: the file is outside this work package's write list, and rule 1 forbids writing outside it. The chain is therefore carried inside the PRD in §11.2, so no trace is lost.
- No master, BRD, FSD or story file was edited. The only source that was converted is the Ownership Map, and the conversion writes into the scratch folder.
- No issue tracker, wiki, repository or web call was made; no git command was run.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S1 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- The document checks that apply to a non-story PRD were run directly on this work package's files: C14 (the §R8.1 header lines inside the first six lines) PASS, C15 (no release date changed, every release date marked tentative) PASS, C16 (no unknown service name in a topic, REST base or queue, and no old monolith API base) PASS, C17 (every cited CG and ASM id has a register row, including the ASM-A6 ids the Ownership Map rulings use) PASS, C20 (tool line present, no wrong tool attribution) PASS.
- C19 still reports planned outputs of other work packages that have not run yet; none of its findings names a B-REQ-PRD-S1 output, and this work package's own planned outputs (the PRD and this edit log) are present.
