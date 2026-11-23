# Edit log B-REQ-PRD-S2 — PRD S2 rwb-treatment v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-S2
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md`
- `_work/msr/docs/B-REQ-PRD-S2/todo.md`
- `_work/msr/docs/B-REQ-PRD-S2/write_registers.py`
- `_work/msr/docs/B-REQ-PRD-S2/verify.py`
- `_work/msr/docs/B-REQ-PRD-S2/run_extra_checks.py`
- `_work/msr/gaps/B-REQ-PRD-S2.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S2.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S2.md`

No file outside the work package's write list was touched. No source document was edited: the FSD S2, the two BRDs, the Architecture v5 extract, the Temporal and Drools extract and the Ownership Map were read only, and the Ownership Map was read through the run's own converted JSON (`_work/msr/plan/ownership.json`) rather than converted again. The register writer is scratch tooling that writes the two jsonl files once, so no id is rewritten. The verify and extra-check scripts are scratch only and write nothing.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md` is version 1 of the family: the folder `03 Requirements and specifications/PRD/` held P1 to P10 and S1 and no S2 file before this run, so there is no earlier version to supersede (ASM-2870). The first two lines are the header of Template and Rules §R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD v3 (15 November 2026) change note character for character, marks FSD v1 and v2 as not specified, and lists every source ID the PRD preserves.

Thirteen sections are written in the order the agent contract sets, followed by Appendix A: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the eleven confirmed v5 constraints); personas and roles; current-versus-target journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty.

Volume: 19 capabilities (CAP-S2-001 to CAP-S2-019), 42 functional requirements (FR-S2-001 to FR-S2-042), 32 non-functional requirements (NFR-S2-001 to NFR-S2-032), 24 acceptance criteria in GIVEN/WHEN/THEN form (AC-S2-001 to AC-S2-024), 14 personas (ROL-S2-01 to ROL-S2-14), 6 journeys (JRN-S2-01 to JRN-S2-06) and 16 open questions (OQ-S2-01 to OQ-S2-16).

Requirement mapping: every FR row carries the FSD requirement it serves (REQ-S2-001 to REQ-S2-010), the Epic 2 requirement behind it where the BRD names this service (RWB-E2-004 to RWB-E2-032) and the release slice it lands in. Section 11.2 gives the BR to capability to FR/NFR to AC chain per requirement. BR coverage is 10 of 10 program requirements of this module and 11 of 11 Epic 2 requirements that name this service, with no gap. The requirement substance, the FSD feature IDs (FEAT-TRT-01 to FEAT-TRT-18), the validation rule IDs (VR-S2-001-1 to VR-S2-018-1), the business rule IDs (BR-S2-001 to BR-S2-018), the routing rule IDs (R-RES, R-SET, R-DIL), the acceptance criteria IDs (AC-S2-001-01 to AC-S2-018-01 and their exception rows), the message IDs (MSG-S2-001, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), the list IDs (LOV-TREATMENT, LOV-PROPOSER) and the screen IDs (SCR-14, SCR-15, SCR-16) are preserved; no number was recomputed and no value was recomputed.

Owners: every owner in sections 9, 11.3 and 12 is a role or a service code from the Ownership Map or the BRD; no person is named. Service facts follow §R4 for S2: schema `rwb_treatment`, REST base `/api/recovery/treatment/v1`, topic `rwb.treatment.events.v1`, task queue `rwb-treatment`, Java package `th.co.scb.ace.workbench.recovery.treatment`, epic `RWB-SVC-S2`, wave 2. Release dates are copied unchanged and marked "(tentative)": E2 31 December 2026, E3 31 January 2027. No solution design is added beyond the v5 constraints: no class, table definition or endpoint is designed here, and the operations, activities, events and the Nexus operation named are only those the architecture, the design and the map already fix.

Release slicing: wave 2 carries the published contract, the treatment record and the data date it is read with; wave 3 carries the settlement, the TDR plan, the offer with its validity, the signature and booking, the broken plan, the deed in lieu with its readiness, inspection and transfer, the document set and the collateral release; wave 4 carries the buy-back rental (Should) and the TDR offer suggestion (Could). The split follows the sources rather than inventing one: the service is wave 2 and EP02, the FSD says "E2 foundations; E3", and every requirement of the module is an E3 requirement, which is carried as GAP-1709 and ASM-2862.

Rulings that change the FSD output, each carried as a gap and an assumption row: every source fact is read through the rwb-source-data contract and no ACE view is read (GAP-1696); the write back to the collections system leaves through rwb-integration (GAP-1697); the service's own table set is named as four entity groups because the map lists one (GAP-1698); the offer command is carried as the map's path with slide 18's path read as the same command (GAP-1699); every clock is a durable timer, not Quartz (GAP-1701); booking, matching and posting stay with rwb-payment (GAP-1703); documents and signatures go through rwb-document and rwb-comms (GAP-1704); the CCMS release, the title check and the asset take-on leave through rwb-integration and rwb-asset (GAP-1705); acceptance criteria are written from the FSD's own steps because its criteria are placeholders (GAP-1708).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-S2.jsonl` — 21 rows, GAP-1696 to GAP-1716, with the keys of §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 11 Missing, 5 Ambiguous, 4 Conflict, 1 Outdated. Severity: 1 P1 (the read path, which gates every requirement of the service), 13 P2, 7 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-S2.jsonl` — 26 rows, ASM-2849 to ASM-2874, with the keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption, as the source-precedence rule requires; 5 rows carry no gap (first version of the family, tentative dates, wave placement, roles only, the two requirement ID sets).
- Counts: CG = 21, ASM = 26. Numbering is left to step D1; the ids above are the candidate ids of this work package, and every citation in the PRD resolves to a row in one of the two files or in the A6 registers that the Ownership Map ruling ids point at.

## Deliberate omissions

- The traceability matrix in `requirement/Traceability_Matrix.md` was not updated: the file is outside this work package's write list, and rule 1 forbids writing outside it. The chain is therefore carried inside the PRD in section 11.2, so no trace is lost.
- No master, BRD, FSD or story file was edited, and no new version of the FSD was produced: this work package produces a PRD, not a source document.
- No issue tracker, wiki, repository or web call was made; no git command was run.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S2 --quick` — C02, C03, C05, C12, C13 and C18 all PASS.
- The document checks that apply to a non-story PRD were run directly on this work package's files: C14 (the §R8.1 header lines inside the first six lines) PASS, C15 (no release date changed, every release date marked tentative) PASS, C16 (no unknown service name in a topic, REST base or queue, and no old monolith API base) PASS, C17 (every cited CG and ASM id has a register row, including the ASM-A6 ids the Ownership Map rulings use) PASS, C20 (tool line present, no wrong tool attribution) PASS.
- C19 still reports planned outputs of other work packages that have not run yet; none of its findings names a B-REQ-PRD-S2 output, and this work package's own planned outputs (the PRD and this edit log) are present.
- The work package's own verifier (`_work/msr/docs/B-REQ-PRD-S2/verify.py`, scratch) reports 0 failures on the id sets (19 capabilities, 42 functional requirements, 32 non-functional requirements, 24 acceptance criteria, 14 personas, 6 journeys, 16 open questions), on the FR table (every row carries a capability, a REQ-S2 source, a priority and a release), on the capability coverage (every capability has at least one functional requirement), and on the tentative marks of the two release dates.
