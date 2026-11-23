# Edit log B-REQ-PRD-P2 - PRD P2 rwb-integration v1

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-REQ-PRD-P2 (PRD Builder), fanout 0

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md`
- `_work/msr/docs/B-REQ-PRD-P2/source-notes.md`
- `_work/msr/gaps/B-REQ-PRD-P2.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P2.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P2.md`

## What the document contains

The PRD is version 1 of the family: no predecessor PRD exists in `03 Requirements and specifications/PRD`, so the section set follows the PRD Builder contract and nothing is copied from an earlier PRD. The first two lines are the header of Template and Rules section R8.1, the change-log row of section 1.3 names D-RCV-60 and the tool line, status is Draft, the release dates are copied from BRD Program v4 section 8 and marked `(tentative)`, and the approval table is empty.

Sections: 1 document control, change log and ID conventions; 2 product overview and relationship to ACE (new, reused, confirmed v5 constraints, exclusions); 3 personas and roles; 4 user journeys (WIN file, debt buyer tape, reporting delivery, duplicate and held morning, EFS hand-over); 5 capabilities; 6 functional requirements; 7 non-functional requirements; 8 data requirements; 9 integration points; 10 release slicing by wave; 11 acceptance criteria and validation evidence; 12 open questions; 13 approval; Appendix A traceability summary.

Counts: 8 capabilities (CAP-P2-001 to CAP-P2-008), 22 functional requirements (FR-P2-001 to FR-P2-022), 13 non-functional requirements (NFR-P2-001 to NFR-P2-013), 14 acceptance criteria (AC-P2-001 to AC-P2-014), 7 open questions (Q-P2-01 to Q-P2-07).

## Realignment changes carried into the PRD

- The module becomes the service rwb-integration: schema `rwb_integration`, own login, REST base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, task queue `rwb-integration`, Java package `th.co.scb.ace.workbench.recovery.integration`.
- The two events `FileDelivered` and `FileFailed` are the service's published events; the shared decision record is published by the platform library.
- The data lake extracts INT-19 and INT-20 leave the product baseline (CG 1; ASM 3).
- The outbound file reads ACE only through the rwb-source-data contract; the service holds no grant on the recovery schema (CG 2; ASM 4).
- Job ownership follows the Ownership Map; the service registers no Temporal Schedule (CG 3; ASM 5).
- The INT-25 tape is built from the request manifest of rwb-debtsale, not from its table (CG 6; ASM 8).
- The removed inbound functions keep their IDs in the exclusion table and carry no FR and no AC (CG 9; ASM 11).
- The EFS hand-over intake is the wave-2 capability traced to REQ-DRI-013 (ASM 18).

## Coverage

- BR to FR coverage: REQ-DRI-006 (6 FR), REQ-DRI-007 (12 FR), REQ-DRI-008 (4 FR), REQ-DRI-013 (1 FR). All four P2 business requirements are covered; no BR of the P2 section is without a functional requirement. FR-P2-022 traces to two BRs, so the distinct count is 22.
- BR to NFR coverage: 21 BRD non-functional requirements are traced from the 13 NFR-P2 rows; the interface-level targets that no source states are held open under DL11 (CG 11; ASM 12).
- Every FR maps to a capability and every AC maps to at least one FR or NFR (section 11.1).
- The master `requirement/Traceability_Matrix.md` is assembler-owned and was not written; the rows this work package contributes are in Appendix A of the PRD.

## Gap and assumption rows

- Gap rows written to `_work/msr/gaps/B-REQ-PRD-P2.jsonl`: 15, ids GAP-1534 to GAP-1548 (types: 5 Conflict, 5 Missing, 4 Ambiguous, 1 Outdated; severities: 3 P1, 5 P2, 7 P3).
- Assumption rows written to `_work/msr/assumptions/B-REQ-PRD-P2.jsonl`: 19, ids ASM-2661 to ASM-2679.
- Only step D1 numbers the rows as GAP-nnnn and ASM-nnnn; the rows carry the candidate ids of this work package.
- Every CG and ASM id cited in the PRD exists in one of the two jsonl files.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P2 --quick` was run after the files were written. Last report: `22 Microservice Realignment/checks/reports/wp-B-REQ-PRD-P2-20261122-191916.md` and `.json`. Result: all six quick checks pass with no findings (C02, C03, C05, C12, C13, C18). The wider checks C12, C13, C14, C17 and C20 were also run against the five files of this work package and pass. C19 reports missing outputs of other work packages queued in `_work/msr/wp` (B-P1-04, B-P1-08, B-P3-02, B-P3-06, B-P3-08, B-P3-10, B-P4-02, B-P4-04, B-P4-06, B-P4-07, B-P4-11, B-P4-15, B-P5-02, B-P5-05, B-P5-07, B-P6-02, B-P6-03, B-P6-06, B-P7-04 to B-P7-09, B-P8-01); none of those paths belongs to this work package and they are left to their own runs.

## Notes and limits

- No source file was edited; the PRD is a new file and the PRD folder is new.
- No value was invented: every value that no source states carries the section R9 placeholder with its CG and ASM citation.
- The document carries no person name and no contact address; roles only.
- Nothing outside the write-only list of the work package was written.
