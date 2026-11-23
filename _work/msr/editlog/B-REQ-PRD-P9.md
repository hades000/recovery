# Edit log B-REQ-PRD-P9 — PRD P9 rwb-reporting v1 (PRD Builder)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 (microservice realignment)
Date: 22 November 2026
Work package: B-REQ-PRD-P9
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md`
- `_work/msr/docs/B-REQ-PRD-P9/write_registers.py`
- `_work/msr/gaps/B-REQ-PRD-P9.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P9.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P9.md`

The register writer is scratch tooling placed under the work package's scratch folder; it writes the two jsonl files once, so no identifier is rewritten afterwards. No source file was edited: the PRD is a new file in a folder that held P1 and P2 only, and every input was read from the versions named in the work package.

## The PRD

`03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md` is version 1 of the P9 family (ASM-2806). The first two lines are the header of Template and Rules §R8.1, followed by the front matter (`title`, `description`, `status: Draft`, `brd`, plus `fsd`, `service`, `epic`, `wave`, `decision`). Section 1 carries the change-log row "1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash", a document-control table that keeps every source ID character for character, and an inherited-history table that keeps the FSD v3 change note, its empty v2 note as a placeholder, and the ID continuity statement.

Thirteen sections follow the agent contract: document control and change log; product overview and relationship to ACE (what is new, what is reused, what leaves, and the eight confirmed v5 constraints); personas and roles; current-versus-target user journeys; capabilities; functional requirements; non-functional requirements; data requirements; integration points; release slicing by wave; acceptance criteria and validation evidence; open questions; approval table left empty. Two appendices hold the ID conventions and the sources used.

Volume: 14 capabilities (CAP-P9-001 to CAP-P9-014), 32 functional requirements (FR-P9-001 to FR-P9-032), 24 non-functional requirements (NFR-P9-001 to NFR-P9-024), 24 acceptance criteria in GIVEN/WHEN/THEN form (AC-P9-001 to AC-P9-024), 11 personas (ROL-P9-01 to ROL-P9-11), 6 journeys (JRN-P9-01 to JRN-P9-06) and 14 open questions (OQ-P9-01 to OQ-P9-14).

Service facts follow §R4 for P9: schema `rwb_reporting`, REST base `/api/recovery/reporting/v1`, resources `GET /dashboards/{id}`, `GET /reports/{id}` and `POST /reports/{id}/run` from Architecture v5 slide 15 and slide 41, topic `rwb.reporting.events.v1` with `ReportPublished`, task queue `rwb-reporting` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.reporting`, service epic `RWB-SVC-P9`, wave 1. Every owner in §9 and §11.3 is a role or a service code from the Ownership Map; no person is named. Release slices carry the section 8 dates unchanged and marked "(tentative)": 30 November 2026 (wave 1), 31 December 2026 (wave 2), 30 April 2027 and 30 June 2027 (wave 4).

Requirement mapping: every FR row carries the FSD feature and acceptance criterion it comes from, because FSD P9 has no requirement IDs (GAP-1645); §11.2 gives the BR to capability to FR/NFR to AC chain. No solution design is added beyond the v5 constraints: no class, no table definition and no endpoint is designed here, and the operations, activities, events and schedules named are only those the architecture and the Ownership Map already fix.

## Realignment rulings applied

Each ruling below is a gap row and a paired assumption row.

1. The data lake and the Power BI connection are removed, so the FSD's integration points, the INT-19 extract and every lake acceptance criterion are read as the reporting read model and a delivered file (GAP-1646, -19; ASM-2788).
2. RWB-E1-014 and REQ-DRI-009 are retired, so the operational reporting is counted from the decision record and the lake copy's checks move to the extract (GAP-1650; ASM-2792).
3. The reconciliation result and the break rows are P1's; the break view and its closure are here (GAP-1651; ASM-2793).
4. The queue measure is P3's; the business-date publication and the reconciliation to the case list are here (GAP-1652; ASM-2794).
5. JOB-15 keeps 01:30 and gains the run operation as its other entry, so the two mechanisms in v5 cannot double-publish (GAP-1647; ASM-2789).
6. The report identifier is read as the measure report for the measure read, and the conflict stays open as OQ-P9-04 (GAP-1648; ASM-2790).
7. The six approved definitions plus the measures named in the alternate flows are published, and the count of seven is carried as OQ-P9-03 (GAP-1649; ASM-2791).
8. Classification, staging and re-ageing are built here under BR-083 pending the owner being confirmed (GAP-1653; ASM-2795).
9. The agent measures are counted from the decision record, because the consumer matrix gives this service no dependency on rwb-agent (GAP-1663; ASM-2801).

## Candidate registers

- Gaps: `_work/msr/gaps/B-REQ-PRD-P9.jsonl` — 20 rows, GAP-1644 to GAP-1663, with the keys of §R9 (id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp). Types: 8 Conflict, 5 Ambiguous, 7 Missing. Severity: 2 P1 (the removed data lake and the retired decision-log copy, both of which the wave-1 and wave-2 acceptance criteria are written against), 11 P2, 7 P3.
- Assumptions: `_work/msr/assumptions/B-REQ-PRD-P9.jsonl` — 22 rows, ASM-2785 to ASM-2806, with the keys of §R9 (id, text, why, read, gap, applied_in, confidence, confirm, impact, wp). Every gap has a paired assumption; 3 rows carry no gap (roles only, access and masking with P4, first version of the family).
- Counts: CG = 20, ASM = 22. Numbering is left to step D1; the identifiers above are the candidate identifiers of this work package and every citation in the PRD resolves to a row.

## BR coverage

5 of the 5 live P9 requirement keys are covered by at least one functional requirement: RWB-E1-013, RWB-E2-009, BR-061, BR-082 and BR-083. The three supporting program keys (REQ-WKM-009, REQ-WKM-006, REQ-CWC-015) are covered as reads and publications. No BR is left without a requirement. The program BRD carries no P9 requirement section at all (GAP-1644), so coverage is stated against the keys that name reporting duties. Two keys are covered by design with no FR of their own: RWB-E1-014 and REQ-DRI-009 are retired with the data lake, and RWB-E1-011 and RWB-E1-030 belong to P1 and P3 with the report surface here.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P9 --quick` — C02, C03, C05, C12, C13 and C18 all PASS. C14 (header lines), C17 (every CG and ASM citation resolves to a jsonl row with its required keys) and C20 (tool line) also PASS when run over this work package's files. C19 reports missing story-stage outputs of other work packages only; nothing in this work package is listed.

## Deliberate omissions

- No value, date, count, identifier or message is invented. Where a source has no value the placeholder of §R9 is written and a gap row and an assumption row exist.
- No person is named, and no issue tracker, wiki, repository or web source was read or written.
- The traceability matrix under the AI-SDLC requirement folder is outside this work package's write list, so the BR to CAP to FR/NFR to AC chain is written in the PRD at §11.2 and not appended there (root rule 1).
