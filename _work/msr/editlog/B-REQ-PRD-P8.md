# Edit log B-REQ-PRD-P8 - PRD P8 rwb-payment v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-P8
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md`
- `_work/msr/docs/B-REQ-PRD-P8/write_registers.py`
- `_work/msr/gaps/B-REQ-PRD-P8.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P8.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P8.md`

The register writer is scratch tooling: it writes the two jsonl files once, so no id is rewritten by hand and every citation in the PRD resolves to one row.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md` is version 1 of the family: the folder held PRD P1, P2, P3, P4, P5, P7 and P9 and no P8 document, so there is no earlier P8 version to supersede (ASM-2780). The first two lines are the header of Template and Rules section R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, `fsd`, `tsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD P8 v3 change note (15 November 2026) and the TSD P8 v2 record (28 October 2026) with every source identifier character for character.

Thirteen sections are written in the order the agent contract sets: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the nine confirmed v5 constraints); personas and roles; current-versus-target user journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty. Appendix A lists the source sections used.

Volume: 12 capabilities (CAP-P8-001 to CAP-P8-012), 32 functional requirements (FR-P8-001 to FR-P8-032), 20 non-functional requirements (NFR-P8-001 to NFR-P8-020), 24 acceptance criteria in GIVEN/WHEN/THEN form (AC-P8-001 to AC-P8-024), 14 roles (ROL-P8-01 to ROL-P8-14), 6 journeys (JRN-P8-01 to JRN-P8-06) and 12 open questions (OQ-P8-01 to OQ-P8-12).

Requirement mapping: FSD P8 v3 issues no requirement ID of its own - its "Requirements served" table and the TSD T8 traceability table are empty (GAP-1624; ASM-2760) - so every FR carries the FSD feature (FEAT-PAY-01 to FEAT-PAY-11) and the FSD acceptance criterion it re-expresses, plus the BRD requirement it serves. Section 11.2 gives the BR to capability to FR/NFR to AC chain and section 11.3 the BR to epic and release trace. Twenty-four requirement statements are cited (18 program requirements, the five numbered business requirements of the Epics 3 to 8 BRD and one universal rule) and each is served by at least one FR or NFR; three nearby BRs are named as deliberately not served here, with the owning service. The program BRD has no requirement section for P8 (GAP-1498; ASM-2783), so the requirements are read from sections 5.3, 5.11 and 5.12 to 5.16 as its section 11 note describes, with section 5.11 added because enforcement proceeds rest on REQ-S4-010 (GAP-1641).

Owners: every owner in section 9 and section 11.4 is a role, a role code or a service code taken from the Microservice Ownership Map. Service facts follow section R4 for P8: schema `rwb_payment`, REST base `/api/recovery/payment/v1`, topic `rwb.payment.events.v1`, task queue `rwb-payment`, Java package `th.co.scb.ace.workbench.recovery.payment`, epic `RWB-SVC-P8`, wave 2. Release dates are copied unchanged from the program release plan (30 November 2026, 31 December 2026, 31 January 2027, 28 February 2027, 30 April 2027) and each is marked "(tentative)". No solution design is added beyond the v5 constraints: no class, table definition or endpoint is designed, and the operations, activities, events and tables named are only those the architecture, the API Specification and the map already fix.

Release slicing: wave 2 (Epic 2, 31 December 2026 tentative) carries matching, the missed payment, the matching values and the unmatched list - the two legacy stories that name this service, RWB-E2-008 and RWB-E2-027 - plus booking confirmation, which the Epics 3 to 8 BRD places in E3 (GAP-1629; ASM-2765). Wave 3 (Epic 4, 28 February 2027 tentative) carries settlement, sale and enforcement proceeds, fees, posting, the deed in lieu rental and the daily reconciliation. Wave 4 (Epic 6, 30 April 2027 tentative) carries provision inputs and post charge-off recovery. Later increments list the reversal, the same-day trigger, the ledger return and the fee tables, each with the question that unlocks it.

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-P8.jsonl` - 20 rows, GAP-1624 to GAP-1643, with the keys of section R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 5 Conflict, 2 Ambiguous, 12 Missing, 1 Outdated. Severity: 14 P2, 6 P3, no P1.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-P8.jsonl` - 25 rows, ASM-2760 to ASM-2784, with the keys of section R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption; 5 rows carry no gap (first version of the family, tentative dates, roles only, the reading of the program BRD sections, the FSD v1 and v2 history).
- Counts: CG = 20, ASM = 25. Numbering is left to step D1; the ids above are the candidate ids of this work package and every CG and ASM citation in the PRD resolves to a row (checked).

## Rulings that change the FSD output

Each is carried as a gap row and an assumption row: the empty FSD requirement tables (CG-1), the nine placeholder acceptance criteria (CG-2), the two operation names that differ between the architecture slide and the API Specification (CG-3), the data quality exception list that has no home (CG-4), the retired matching value table (CG-5), the Epic 3 against Epic 4 booking date (CG-6), the posting file with no layout (CG-7), the direct system-of-record interfaces that v5 removes (CG-8), the unbuilt payment reversal (CG-9), the undefined fee tables (CG-10), the uuid against business-key payment link (CG-11), the ledger side of the daily reconciliation (CG-12), the unspecified application order (CG-13), the two messages without wording (CG-14), the measure without a baseline (CG-15), the unnamed workflows (CG-16), the same-day trigger the data path cannot meet (CG-17), the missing section 5.11 in the BRD note (CG-18), the missing approval (CG-19) and the missing receipt volume (CG-20).

## New decisions

No new decision ID was needed: the only decision this document records is D-RCV-60, taken from `_work/msr/plan/ids.json`, and no ADR, DL or D-RCV identifier outside that file's existing allocations is used or claimed. The gaps and assumptions are candidate ids of this work package only; step D1 numbers them.

## Deliberate omissions- The traceability matrix in `requirement/Traceability_Matrix.md` was not updated: the file is outside this work package's write list, and rule 1 forbids writing outside it. The BR to CAP to FR/NFR to AC chain is therefore carried inside the PRD in section 11.2, so no trace is lost.
- No master, BRD, FSD, TSD or story file was edited or converted. The source documents were read from the converted text already in `_work/msr/extract/`, so this work package ran no converter and wrote nothing outside its own paths.
- No issue tracker, wiki, repository or web call was made; no git command was run.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P8 --quick` - C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS. Six of six pass, no finding.
- The checks that apply to a non-story document were run on the PRD and the registers as well: C12 (no person name, no email address) PASS, C13 (no issue-tracker reference) PASS, C14 (the section R8.1 header lines in the first six lines) PASS, C16 (no unknown service name in a topic, REST base or queue, and no old monolith API base) PASS, C17 (every cited CG and ASM id has a register row, and every register row carries its required keys) PASS, C20 (tool line present in the edit log, no wrong tool attribution) PASS.
- C19 (planned outputs of the work packages) still reports work packages whose outputs have not been written yet, because the run is in progress across wave-B packages. No C19 finding names a B-REQ-PRD-P8 output, and both planned outputs of this work package (the PRD and this edit log) exist.
- Self-audit of the document: 12 capabilities, 32 functional requirements and 24 acceptance criteria; every FR is served by at least one BR and covered by at least one AC, and every CAP and every AC reference resolves. Nine of the twenty non-functional requirements have no AC of their own; each is covered by an evidence row in section 11.4 (availability, recovery, chain, encryption and pipeline, identity, rollback, language, tenancy and retention), which is how a non-functional target is proven.

