# Edit log B-REQ-PRD-S6 — PRD S6 rwb-debtsale v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-S6
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md`
- `_work/msr/docs/B-REQ-PRD-S6/ownership/Recovery Workbench Microservice Ownership Map v1.md`
- `_work/msr/docs/B-REQ-PRD-S6/write_registers.py`
- `_work/msr/docs/B-REQ-PRD-S6/verify.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_ownership.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_split.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_split2.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_docs.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_allowed.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_counts.py`
- `_work/msr/docs/B-REQ-PRD-S6/probe_checks.py`
- `_work/msr/gaps/B-REQ-PRD-S6.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-S6.jsonl`
- `_work/msr/editlog/B-REQ-PRD-S6.md`

The Ownership Map was converted to text with `python -I "22 Microservice Realignment/compat/convert_sources.py" "22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx" "_work/msr/docs/B-REQ-PRD-S6/ownership"`, so every operation, event, workflow and table owner in the PRD is taken from the map rather than reasoned. The probe scripts read `_work/msr/plan/ownership.json` and `_work/msr/plan/split_plan.json` (the "stats" and "legacy" keys only) and are scratch. The register writer writes the two jsonl files once so no id is rewritten. The verify script checks the id sets, the citations, the table shapes, the header and the forbidden strings against the written PRD.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md` is version 1 of the family: the folder `03 Requirements and specifications/PRD/` held P1 to P10 and S1 and no S6 file before this run, so there is no earlier version to supersede (ASM-2967). The first two lines are the header of Template and Rules §R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash" and an inherited-history table that keeps the FSD v3 (15 November 2026) change note character for character, marks FSD v1 and v2 as not specified, and lists every source ID the PRD preserves.

Thirteen sections are written in the order the agent contract sets, followed by Appendix A: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the twelve confirmed v5 constraints); personas and roles; current-versus-target journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty.

Volume: 17 capabilities (CAP-S6-001 to CAP-S6-017), 33 functional requirements (FR-S6-001 to FR-S6-033), 31 non-functional requirements (NFR-S6-001 to NFR-S6-031), 22 acceptance criteria in GIVEN/WHEN/THEN form (AC-S6-001 to AC-S6-022), 13 personas (ROL-S6-01 to ROL-S6-13), 5 journeys (JRN-S6-01 to JRN-S6-05) and 16 open questions (OQ-S6-01 to OQ-S6-16).

Requirement mapping: every FR row carries the FSD requirement or feature it serves (REQ-S6-001 to REQ-S6-009, FEAT-DBS-08, FEAT-DBS-16), the BRD requirement behind it (BR-044 to BR-050) and the routing rules it applies (R-DS-01 to R-DS-41), and §11.2 gives the BR to capability to FR/NFR to AC chain per requirement. BR coverage is 9 of 9 program requirements and 7 of 7 BRD requirements of E5 and E6 that name this service, with no gap; BR-046 and BR-050 have no program requirement of their own and trace to their FSD features and to RULE-015. The requirement substance, the FSD feature IDs (FEAT-DBS-01 to FEAT-DBS-16), the FSD acceptance criteria IDs (AC-S6-001-01 to AC-S6-016-01 and their exception rows), the validation and business rule IDs (VR-S6-001-1 to VR-S6-016-1, BR-S6-001 to BR-S6-016), the routing rule IDs (R-DS-01 to R-DS-41), the message IDs (MSG-S6-001, MSG-P1-001, MSG-P4-002, MSG-P7-003, MSG-GEN-001), the list IDs (LOV-SEGMENT, LOV-BUYER-CLASS, LOV-LOT-STATUS, LOV-PUTBACK), the field IDs (DF-SAL-020 to DF-SAL-037), the screen IDs (SCR-25, SCR-26) and the partner screen ID (PRT-05) are preserved; no number was recomputed and no value was recomputed.

Owners: every owner in §9 and §11.3 is a role or a service code from the Ownership Map or the BRD; no person is named. Service facts follow §R4 for S6: schema `rwb_debtsale`, REST base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1`, task queue `rwb-debtsale`, Java package `th.co.scb.ace.workbench.recovery.debtsale`, epic `RWB-SVC-S6`, wave 3. Release dates are copied unchanged and marked "(tentative)": EP05 31 March 2027, EP06 30 April 2027, wave 3 releases 28 February 2027 and 31 March 2027. No solution design is added beyond the v5 constraints: no class, table definition or endpoint is designed here, and the operations, activities, events and tables named are only those the architecture, the design, the Ownership Map and the physical schema already fix.

Release slicing by wave: EP05 (wave 3) carries the population, the lot and its price, the masked tape, the data room and the cap enforcement in five slices; EP06 (wave 4) carries the buyer qualification and barring, the bids, the award with the agreement and the notices, the settlement, transfer and posting, the put-back and case closure, and the sale ledger in seven slices. The service wave and the E6 wave do not conflict, because the conflict rule applies only where a business epic wave is earlier than the service wave (ASM-2966).

Rulings that change the FSD output, each carried as a gap and an assumption row: the service reads the balance, the COLLINS economics and the freshness through the rwb-source-data contract and reads no ACE view, and the slide 13 matrix gives it no such cell (GAP-1770); five of the six records the architecture gives this service have no table (GAP-1771); the foreign key to `partner` does not survive the split (GAP-1772); the buyer operations go through the partner gateway (GAP-1774); the customer notices go through P6 and not to WIN (GAP-1775); the buyer's KYC and licence facts have no source (GAP-1776); the posting is P8's and the derecognition is this service's decision (GAP-1779); the sale is a saga per lot as well as a stage workflow per case (GAP-1780); the monthly cycle needs a schedule that no source gives it (GAP-1781); masking is this service's act under the P4 policy and not a separate PII service (GAP-1783); `borrower_code` and `account_key` are personal data in use despite the data model flag (GAP-1786).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-S6.jsonl` — 22 rows, GAP-1770 to GAP-1791, with the keys of §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 13 Missing, 6 Conflict, 3 Ambiguous. Severity: 1 P1 (the read path, which gates every requirement of the service), 14 P2, 7 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-S6.jsonl` — 26 rows, ASM-2942 to ASM-2967, with the keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every one of the 22 gaps has a paired assumption, as the source-precedence rule requires; 4 rows carry no gap (the first version of the family with an empty approval table, tentative dates, wave placement, and the two requirement ID sets).
- Counts: CG = 22, ASM = 26. Numbering is left to step D1; the ids above are the candidate ids of this work package, and every one of the 48 CG and ASM citations in the PRD resolves to a row in one of the two files.

## Deliberate omissions

- The traceability matrix in `requirement/Traceability_Matrix.md` was not updated: the file is outside this work package's write list, and rule 1 forbids writing outside it. The chain is therefore carried inside the PRD in §11.2, so no trace is lost.
- No master, BRD, FSD or story file was edited. The only source that was converted is the Ownership Map, and the conversion writes into the scratch folder.
- No issue tracker, wiki, repository or web call was made; no git command was run.
- No person is named anywhere. The Decision Log v10 columns that carry a person's name were read for the decision text only and are not quoted.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-S6 --quick` — C02, C03, C05, C12, C13, C18 all PASS (0 findings each).
- The document checks that apply to a non-story PRD were run directly on this work package's files: C14 (the §R8.1 header lines inside the first six lines) PASS, C15 (no release date changed, every release date marked tentative) PASS, C16 (no unknown service name in a topic, REST base or queue, and no old monolith API base) PASS, C17 (every cited CG and ASM id has a register row) PASS, C20 (tool line present, no wrong tool attribution) PASS.
- The scratch verify script reports: 48 distinct CG and ASM citations, 0 unresolved; CAP 17, FR 33, NFR 31 and AC 22 complete and contiguous; every FR present in the §11.2 trace summary; no malformed table row in sections 5, 6, 7 or 11.1; no forbidden string.
- C19 still reports planned outputs of other work packages that have not run yet; none of its findings names a B-REQ-PRD-S6 output, and this work package's own planned output (the PRD) and this edit log are present.
