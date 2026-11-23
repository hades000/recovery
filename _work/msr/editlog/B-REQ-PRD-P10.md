# Edit log B-REQ-PRD-P10

Work package: B-REQ-PRD-P10 - PRD P10 rwb-agent v1 (PRD Builder)
Tool and model: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60 microservice realignment
Date: 22 November 2026
Agent: aisdlc-prd-builder. fanout: 0, so no subagent was used.

## Files written

- 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md
- _work/msr/docs/B-REQ-PRD-P10/source-baseline.md
- _work/msr/gaps/B-REQ-PRD-P10.jsonl
- _work/msr/assumptions/B-REQ-PRD-P10.jsonl
- _work/msr/editlog/B-REQ-PRD-P10.md

No existing file was edited. The sources in folders 03, 17, 18, 21 and 22 are read-only in this work package, and no source was modified. The master traceability matrix is assembler-owned and was not written; the rows this PRD contributes are in its Appendix A.

## What was produced

| Item | Count |
|---|---|
| Capabilities CAP-P10-nnn | 11 |
| Functional requirements FR-P10-nnn | 26 |
| Non-functional requirements NFR-P10-nnn | 17 |
| Acceptance criteria AC-P10-nnn | 17 |
| Open questions Q-P10-nn | 8 |
| Business requirements traced (BRD IDs) | 16 |
| Business requirements with no functional requirement | 0 |

## Source set read

| Source | Version | Use |
|---|---|---|
| BRD Program | v5, 22 November 2026 | Sections 5.3, 5.4, 5.5, 5.15, 5.7, 6.2 to 6.9, 6.12, 8, 10.2, 10.3, 11, 12 |
| BRD Epic 1 | v5 | Section 3.9 P10 agent runtime, RWB-E1-058 to RWB-E1-063 |
| BRD Epic 2 | v3 | Section 3.10, RWB-E2-031 and RWB-E2-032, and its gap GAP-1462 |
| BRD Epics 3 to 8 | v1 | Sections 8.1 (BR-015), 8.6 (BR-072, BR-081, BR-084), RULE-029, RULE-031, KPI-012, Q-014, Q-017, Q-026 |
| FSD P10 Agent runtime | v3, 15 November 2026 | A1.2 feature overview, A2.1 to A2.16, Requirements served, Screens, Appendix B |
| Architecture v5 Text Extract | v1 | Slides 4, 9, 16, 29, 33, 34, 35, 38, 41, 42, 43, 44 |
| Temporal and Drools Design Text Extract | v1 | Slides 27 and 28, R-UNI-32 and the 60 second rule |
| Story Template and Rules | v1 | R1, R3, R4, R5.6, R8.1, R8.2, R9 |
| Ownership Map and ownership.json | v1 | Eight P10 tables, twelve P10 API rows, EV-28, AgentRunWorkflow |
| split_plan.json | current | "stats" and "legacy" for the P10 keys only |
| ids.json | current | D-RCV-60, ADR-013 to ADR-023, DL44 to DL49 |

## Realignment changes carried into the PRD

1. The module becomes the service rwb-agent with schema `rwb_agent`, its own login, REST base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, task queue `rwb-agent` and Java package `th.co.scb.ace.workbench.recovery.agent`.
2. One published event, `rwb.agent.AgentRunCompleted.v1` (EV-28), with identifiers, codes and counts only.
3. One workflow, `AgentRunWorkflow` on queue `rwb-agent`: 60 seconds, then the rule result.
4. The data lake write and the Power BI data set behind the agent dashboard are removed by ADR-018, and the dashboard is served from the service's own daily measures and from the rwb-reporting read model.
5. `agent_run_daily` is read as a projection over the run record because the Logical Data Model v8 lists eight agent entities and not nine.
6. Every case fact is read through the rwb-source-data tool contract and every extracted field through the rwb-document tool contract; no grant on the recovery schema and no grant on another service schema.
7. JOB-15 stays the reporting extract of rwb-reporting; the service runs its own daily aggregation and hands the measures to the read model.
8. The tool gateway is read-only for wave 1 and wave 2, and a write tool is carried as an open question rather than a requirement.
9. Autonomy is a versioned policy row with the values OFF, SHADOW and L1, a four-eyes approval, a drift watch with a stated threshold and minimum feedback, and a step up or down on a named evaluation run.
10. Release slicing follows the wave map: MVP in wave 1, the L1 work, the feedback loop, the TDR suggestion and the autonomy row in wave 2, reuse in wave 3, champion and challenger with the committee in wave 4. Every date is copied from BRD Program v5 section 8 and marked tentative.
11. Status is Draft and the approval table is empty, because no BRD in the set carries a status or an approval record.

## Gaps and assumptions

| Register | Rows written | Candidate ID range |
|---|---|---|
| Gaps | 18 | GAP-1516 to GAP-1532 |
| Assumptions | 24 | ASM-2637 to ASM-2660 |

Gap mix by type: Conflict 5 (CG-1, CG-3, CG-4, CG-5, CG-18), Ambiguous 3 (CG-13, CG-15, CG-16), Missing 10 (CG-2, CG-6, CG-7, CG-8, CG-9, CG-10, CG-11, CG-12, CG-14, CG-17). Severity: P1 2 (CG-1, CG-3), P2 10, P3 6. Assumption confidence: High 14, Medium 10.

The five conflicts that change a requirement are the data lake and Power BI dashboard (CG-1), the direct ACE read (CG-3), JOB-15 (CG-4), the admin path names (CG-5) and the screening mode (CG-18). Each carries the Architecture v5 or Ownership Map ruling under R-PREC rule 1 and a matching assumption.

## Checks

Command: `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P10 --quick`

Result: all six quick checks PASS (C02, C03, C05, C12, C13, C18). Report written under `22 Microservice Realignment/checks/reports/`.

The same harness was also run on the five work-package files for the checks outside the quick set that apply to a requirements document: C01 baseline integrity PASS, C14 header lines PASS, C16 service names and API bases PASS, C17 gap and assumption rows and every citation PASS, C20 tool line PASS. C19 reports missing planned outputs of other work packages whose stories are not written yet, and its findings name no file of this work package.

No failure was left open. Nothing was written outside the "Write only" list of the work package.
