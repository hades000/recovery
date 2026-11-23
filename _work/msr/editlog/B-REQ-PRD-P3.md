# Edit log — WP B-REQ-PRD-P3 (PRD P3 rwb-case v1)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment
Date: 22 November 2026
Agent: aisdlc-prd-builder. Fanout: 0 (no subagent used; the work package allows none).

## Files written

- `03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md`
- `_work/msr/docs/B-REQ-PRD-P3/make_rows.py`
- `_work/msr/gaps/B-REQ-PRD-P3.jsonl`
- `_work/msr/assumptions/B-REQ-PRD-P3.jsonl`
- `_work/msr/editlog/B-REQ-PRD-P3.md`

Nothing outside the "Write only" list was created, edited or deleted. No existing file was modified. The PRD folder `03 Requirements and specifications/PRD/` did not exist and was created by writing the first file into it.

## Output summary

| Item | Value |
|---|---|
| PRD version | 1 (first version of the family) |
| Status | Draft; approval table empty (ASM-2680) |
| Header | Template and Rules §R8.1, first two lines |
| Change-log row | 1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Sections | 13 (document control, overview, personas, journeys, capabilities, FR, NFR, data, integration, release slicing, acceptance criteria, open questions, approval) |
| CAP rows | 24 (CAP-P3-001 to CAP-P3-024) |
| FR rows | 41 (FR-P3-001 to FR-P3-041) |
| NFR rows | 35 (NFR-P3-001 to NFR-P3-035) |
| AC rows | 37 (AC-P3-001 to AC-P3-037) |
| Open questions | 21 (OQ-P3-001 to OQ-P3-021; 9 carried from DL06, DL10, DL11, DL16, DL22, DL23, DL26, DL43 and Q-012 of the Epics 3 to 8 BRD) |
| Release slices | Wave 1 / EP01 (30 November 2026, tentative); wave 2 / EP02 and EP03 (31 December 2026 and 31 January 2027, tentative); wave 3 / EP04 and EP05 (28 February 2027 and 31 March 2027, tentative); wave 4 / EP06, EP07 and EP08 (30 April 2027, 31 May 2027 and 30 June 2027, tentative) |
| Candidate gap rows | 15 (GAP-1549 to GAP-1563) |
| Candidate assumption rows | 17 (ASM-2680 to ASM-2696) |
| BR coverage gaps | 1 unscheduled (REQ-WKM-010 has no story); 2 delivered across two services (REQ-CHO-009 with rwb-payment, REQ-S7-008 with rwb-writeoff) |

## Counts of candidate rows

| Register | Rows | Numbered by step D1 |
|---|---|---|
| `_work/msr/gaps/B-REQ-PRD-P3.jsonl` | 15 | GAP-nnnn |
| `_work/msr/assumptions/B-REQ-PRD-P3.jsonl` | 17 | ASM-nnnn |

Every cited `CG-B-REQ-PRD-P3-n` and `ASM-B-REQ-PRD-P3-n` in the PRD resolves to a row in these two files; every row is cited at least once.

## Sources read (read-only)

| Source | Used for |
|---|---|
| BRD Program v5, Epic 1 v5, Epic 2 v3, Epics 3 to 8 v1 (in 03 Requirements and specifications; the converted text of the previous versions sits under `_work/msr/extract`) | The REQ rows of module 5.3 and 5.2 assigned to this service, the delivery model, the wave and release table, the requirement to service trace, the program NFRs, the open decisions, the Epics 3 to 8 closure rule and the Q-012 retention question |
| FSD P3 Case and workflow v4 (v6 folder copy) | The 52 FEAT features, BR-P3-001 to BR-P3-052, the AC-P3 criteria, the roles, the screens, the glossary |
| Architecture v5 Text Extract v1 | Service boundary, wave, schema, topic, task queue, event catalogue, job map, the ACE read path ruling |
| Temporal and Drools Design Text Extract v1 | The case workflow model, the case router, the four-step rule pattern, Continue-As-New |
| Microservice Story Template and Rules v1 | §R1, §R3, §R5, §R8, §R9 |
| `_work/msr/plan/ownership.json` and the Ownership Map v1 | The 15 P3 tables, 22 P3 interface paths, 7 P3 events, 3 P3 jobs, the case workflow, the ownership rulings |
| `_work/msr/plan/split_plan.json` (stats and legacy/slices) | The 84 P3 slices, their waves, releases and requirements |
| `_work/msr/plan/ids.json` | D-RCV-60 and the ADR and decision-log IDs |

No external system was called. No issue tracker, no wiki, no git commit.

## Decisions and deviations

1. **Traceability matrix not written.** The agent contract asks for rows to be appended to `requirement/Traceability_Matrix.md`. The work package's "Write only" list does not include that file, and root rule 1 allows only the listed files, so the matrix was not touched. The BR to CAP to FR/NFR to AC trace is instead complete inside the PRD (§5.1, §5.3, §6, §7, §11) and can be appended by the assembler in Stage C.
2. **FR to FSD mapping.** The work package asks for FR-P3-nnn mapped to the FSD requirement IDs. The FSD P3 carries no REQ identifier, so each FR cites the BRD REQ ID as the requirement key and the FSD FEAT, BR-P3 and AC-P3 codes as the functional detail (GAP-1552; ASM-2682).
3. **Service scope.** The PRD is scoped to rwb-case. Requirements owned by P1, P4, P5, P6, P7, P9, P10 and the stage services appear only as dependencies (ASM-2683).
4. **No design beyond confirmed v5 constraints.** The document states the service boundary, schema, contract base, topic, task queue and the case workflow model because Architecture v5 confirms them. It states no class, table, endpoint or message schema of its own.
5. **No person names.** Roles only, throughout, including the owner columns and the open questions.
6. **Re-based on the latest BRD versions.** The BRD Builder work packages produced Program v5, Epic 1 v5, Epic 2 v3 and Epics 3 to 8 v1 in the same run, so this PRD cites those versions and takes the delivery model, the wave windows and the requirement to service trace from them. The P3 requirement text is unchanged between Program v4 and v5, so no FR changed because of the re-base; three rows changed their treatment: REQ-WKM-010 is assigned to this service for EP07 with no story (GAP-1553), REQ-CHO-009 is assigned to this service while the matching runs in rwb-payment (GAP-1563, now carried as FR-P3-041 for the case-facing half) and REQ-S7-008 gives the closure rule to rwb-writeoff (GAP-1554, with the case state change kept here as FR-P3-038).
7. **Two requirement halves.** Where a requirement is delivered across two services, this PRD states its half and names the other. The pairing is recorded in §5.3 and in the open questions.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P3 --quick` — C02, C03, C05, C12, C13, C18 all PASS.

Also run on the written files: C14 (header) PASS, C17 (gap and assumption schema plus citation resolution) PASS, C20 (tool line, no foreign tool attribution) PASS.

Result: PASS, no failures, no retries needed.

## Handover

Next step: Product Owner and FDA approve the PRD, then the context update, then the backlog draft for this service (Template and Rules §R8.5; root AGENTS.md rule 14 does not apply because there is no fanout).
