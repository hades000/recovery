# Edit log B-REQ-PRD-P6 — PRD P6 rwb-comms v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-P6
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md`
- `_work/msr/docs/B-REQ-PRD-P6/Recovery Workbench Microservice Ownership Map v1.md`
- `_work/msr/docs/B-REQ-PRD-P6/write_registers.py`
- `_work/msr/docs/B-REQ-PRD-P6/check_prd.py`
- `_work/msr/gaps/B-REQ-PRD-P6.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P6.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P6.md`

The Ownership Map was converted to text with `python -I "22 Microservice Realignment/compat/convert_sources.py"` into the scratch folder, so every table, operation, event, job and workflow owner in the PRD is taken from the map rather than reasoned. The register writer and the consistency checker are scratch tooling; the writer writes the two jsonl files once, so no id is rewritten.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md` is version 1 of the family: the folder held no earlier PRD for this service, so there is no earlier version to supersede (ASM-2744). The first two lines are the header of Template and Rules §R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD v2 (28 October 2026) and v3 (15 November 2026) change notes and every source ID character for character.

Thirteen sections are written in the order the agent contract sets: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves and where, and the eight confirmed v5 constraints); personas and roles; current-versus-target user journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty. An appendix lists the source sections used.

Volume: 13 capabilities (CAP-P6-001 to CAP-P6-013), 38 functional requirements (FR-P6-001 to FR-P6-038), 24 non-functional requirements (NFR-P6-001 to NFR-P6-024), 34 acceptance criteria in GIVEN/WHEN/THEN form (AC-P6-001 to AC-P6-034), 10 personas (ROL-P6-01 to ROL-P6-10), 5 journeys (JRN-P6-01 to JRN-P6-05) and 10 open questions (OQ-P6-01 to OQ-P6-10).

Requirement mapping: every FR row carries the FSD requirement it serves (REQ-OCC-001 to REQ-OCC-011) and the FSD feature and section it comes from (FEAT-OCC-01 to -13, FEAT-COM-01 to -08), and §11.2 gives the BR to capability to FR/NFR to AC chain per requirement. BR coverage is 11 of the 11 P6 program requirements. Two of them are covered as this service's contribution rather than as ownership of the whole behaviour: REQ-OCC-007 and REQ-OCC-008 describe the case record view and the case timeline, which are rwb-case's (GAP-1598; ASM-2730). The requirement substance, the FSD feature IDs, the acceptance criteria IDs, the API IDs (API-P6-001 to API-P6-011), the interface IDs (INT-14, INT-17, INT-18), JOB-10, the event IDs (EV-13, EV-14, EV-15), the lists of values, the rule references and the message IDs are preserved; no number was recomputed.

Owners: every owner in §9 and §11.3 is a role or a service code from the Ownership Map; no person is named. Service facts follow §R4 for P6: schema `rwb_comms`, REST base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1`, task queue `rwb-comms`, Java package `th.co.scb.ace.workbench.recovery.comms`, epic `RWB-SVC-P6`, wave 1. Release dates are copied unchanged and marked "(tentative)". No solution design is added beyond the v5 constraints: no class, table definition or endpoint is designed here, and the operations, activities, events and tables named are only those the architecture and the map already fix.

Rulings that change the FSD output, each carried as a gap and an assumption row: the template and merge-field catalog is this service's against the DL28 answer (CG-1); the signature request is stored by the document hub while the flow stays here (CG-2); the proof of delivery is applied here and read through the source-data contract (CG-3); the case record view and the timeline belong to rwb-case (CG-4); a sent message is a ledger entry, not a fourth table (CG-5); seven features leave the module (CG-13).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-P6.jsonl` — 17 rows, GAP-1595 to GAP-1611, with the keys of §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 6 Conflict, 7 Missing, 3 Ambiguous, 1 Outdated. Severity: 2 P1 (the WIN file layout and the open ACE dependency that gates proof of delivery), 10 P2, 5 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-P6.jsonl` — 19 rows, ASM-2727 to ASM-2745, with the keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption; 2 rows carry no gap (the first version of the family, and the tentative dates).
- Counts: CG = 17, ASM = 19. Numbering is left to step D1; the ids above are the candidate ids of this work package and every citation in the PRD resolves to a row.

## Deliberate omissions

- The traceability matrix in `requirement/Traceability_Matrix.md` was not updated: the file is outside this work package's write list, and rule 1 forbids writing outside it. The chain is therefore carried inside the PRD in §11.2, so no trace is lost.
- No master, BRD, FSD, TSD or story file was edited. The only source read that was converted is the Ownership Map, and the conversion writes into the scratch folder.
- No issue tracker, wiki, repository or web call was made; no git command was run.
- The FSD carries no open question of its own for this module, so no OQ-P6 id is carried forward; the ten questions raised are product-level and each names the gap and assumption that stand in for an answer.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P6 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- The checks that apply to a non-story document were run directly on the PRD: C14 (the §R8.1 header lines in the first six lines) PASS, C16 (no unknown service name in a topic, REST base or queue, and no old monolith API base) PASS, C17 (all 36 cited CG/ASM ids have a register row, and every row is cited) PASS, C20 (tool line present, no wrong tool attribution) PASS, C12 (no person name and no email address) PASS, C13 (no issue-tracker reference) PASS.
- Internal consistency, run with `_work/msr/docs/B-REQ-PRD-P6/check_prd.py`: no number missing from the CAP, FR, NFR or AC sequence; every FR and NFR is referenced by at least one acceptance criterion; every FR and NFR row carries at least one BR.
- C15 was checked by hand: every release date is the BRD release plan date for its wave and each is marked "(tentative)".
