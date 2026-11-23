# Edit log B-REQ-PRD-P1 — PRD P1 rwb-source-data v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-P1
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md`
- `_work/msr/docs/B-REQ-PRD-P1/ownership/Recovery Workbench Microservice Ownership Map v1.md`
- `_work/msr/docs/B-REQ-PRD-P1/write_registers.py`
- `_work/msr/gaps/B-REQ-PRD-P1.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P1.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P1.md`

The Ownership Map was converted to text with `python -I "22 Microservice Realignment/compat/convert_sources.py"` into the scratch folder so every table, operation, event, job and workflow owner in the PRD is taken from the map rather than reasoned. The register writer is scratch tooling; it writes the two jsonl files once so no id is rewritten.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md` is version 1 of the family: the folder `03 Requirements and specifications/PRD/` did not exist before this run, so there is no earlier version to supersede (ASM-2635). The first two lines are the header of Template and Rules §R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD v2 (28 October 2026) and v3 (15 November 2026) change notes and every source ID character for character.

Thirteen sections are written in the order the agent contract sets: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the eight confirmed v5 constraints); personas and roles; current-versus-target user journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty. An appendix lists the source sections used.

Volume: 14 capabilities (CAP-P1-001 to CAP-P1-014), 32 functional requirements (FR-P1-001 to FR-P1-032), 27 non-functional requirements (NFR-P1-001 to NFR-P1-027), 24 acceptance criteria in GIVEN/WHEN/THEN form (AC-P1-001 to AC-P1-024), 13 personas (ROL-P1-01 to ROL-P1-13), 5 journeys (JRN-P1-01 to JRN-P1-05) and 15 open questions (OQ-P1-01 to OQ-P1-15).

Requirement mapping: every FR row carries the FSD requirement it serves (REQ-RDF-001 to REQ-RDF-014), and §11.2 gives the BR to capability to FR/NFR to AC chain per requirement. BR coverage is 12 of 12 live P1 program requirements. REQ-RDF-005 and REQ-RDF-006 have no FR by design: D-RCV-35 (U5) removed them from system scope and their later home is the Cutover plan. The requirement substance, the FSD feature IDs (FEAT-RDF-xx), the FSD acceptance criteria IDs (AC-P1-xxx), the open question IDs (OQ-P1-xx), the data product codes (DP01 to DP14), the reconciliation checks (REC-01, REC-02, REC-05), JOB-04, EV-26, EV-27 and the message IDs are preserved; no number was recomputed.

Owners: every owner in §9 and §11.3 is a role or a service code from the Ownership Map; no person is named. Service facts follow §R4 for P1: schema `rwb_source_data`, REST base `/api/recovery/source-data/v1`, topic `rwb.source-data.events.v1`, task queue `rwb-source-data`, Java package `th.co.scb.ace.workbench.recovery.sourcedata`, epic `RWB-SVC-P1`, wave 1. Release dates are copied unchanged and marked "(tentative)". No solution design is added beyond the v5 constraints: no class, table definition or endpoint is designed here, and the operations, activities and events named are only those the architecture and the map already fix.

Rulings that change the FSD output, each carried as a gap and an assumption row: the data lake and the dashboard connection are gone, so the report, the measure extract and the decision-log copy lose their destination (CG-1); retention moves to the document service (CG-2); masking rules move to the access service (CG-3); the case list screen and its operation stay with the case service (CG-4); the measure job moves to reporting (CG-5); the data-ready and data-late events are produced here (CG-6).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-P1.jsonl` — 17 rows, GAP-1499 to GAP-1515, with the keys of §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 6 Conflict, 6 Missing, 4 Ambiguous plus 1 Missing on governance. Severity: 1 P1 (the open ACE dependency that gates the Section B views and freshness), 10 P2, 6 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-P1.jsonl` — 20 rows, ASM-2617 to ASM-2636, with the keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption, as the source-precedence rule requires; 3 rows carry no gap (tentative dates, first version of the family, wave placement).
- Counts: CG = 17, ASM = 20. Numbering is left to step D1; the ids above are the candidate ids of this work package and every citation in the PRD resolves to a row.

## Deliberate omissions

- The traceability matrix in `requirement/Traceability_Matrix.md` was not updated: the file is outside this work package's write list, and rule 1 forbids writing outside it. The chain is therefore carried inside the PRD in §11.2, so no trace is lost.
- No master, BRD, FSD or story file was edited. The only source read that was converted is the Ownership Map, and the conversion writes into the scratch folder.
- No issue tracker, wiki, repository or web call was made; no git command was run.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P1 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- The three checks that apply to a non-story document were run directly on the PRD: C14 (the §R8.1 header lines in the first six lines) PASS, C16 (no unknown service name in a topic, REST base or queue, and no old monolith API base) PASS, C17 (all 26 cited CG/ASM ids have a register row) PASS, C20 (tool line present, no wrong tool attribution) PASS. C15 was checked too: no release date differs from the BRD release plan and every date is marked tentative.
- C19 still reports planned outputs of other work packages that have not run yet; none of its findings names a B-REQ-PRD-P1 output, and the PRD's own planned output is present.
