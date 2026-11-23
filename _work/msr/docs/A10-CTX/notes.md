SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# A10-CTX scratch notes

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
WP: A10-CTX (fanout: 0; no subagents used)

## Sources read

| Source | Use |
|---|---|
| `22 Microservice Realignment/aisdlc/.github/contexts/` (9 files) | Existing context package: project, domain, backend, frontend, testing, two standards files, README, manifest |
| `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (51 slides) | Services, contracts, call types, events, jobs, data, edge, security, delivery, compliance |
| `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (32 slides) | Workflow model, rule governance, scenarios S1-S9, open design points |
| `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` | §R1, §R3, §R5, §R8, §R9 |
| `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` | Services, Tables, FK cuts, Endpoints, Events, Workflows, Jobs, Parameters, Rulings |
| `_work/msr/plan/ownership.json` | 93 tables, 156 endpoints, 30 events, 22 jobs, 15 workflows, 71 rulings |
| `_work/msr/plan/split_plan.json` | `stats` and `legacy` only |
| `_work/msr/plan/ids.json` | D-RCV-60, ADR-013..023, DL44..49 |

## Output counts

- Context file: `realignment-v5-context.md`, 18 sections, 19-service catalogue, 30 events, 22 jobs,
  15 workflows, 93 tables with owners, 20 decoupling patterns, 11 ADRs, 6 Decision Log rows.
- Candidate gap rows: 22 (`CG-A10-CTX-1` .. `CG-A10-CTX-22`).
- Candidate assumption rows: 24 (`ASM-A10-CTX-1` .. `ASM-A10-CTX-24`); 22 pair with a gap, 2 stand
  alone (`ASM-A10-CTX-23` Arch v5 treated as the target, `ASM-A10-CTX-24` manifest index update).

## Notes

- The five canonical context files all exist and are substantive; none is missing or empty, so there
  is no `MISSING_CONTEXT_HANDOFF`. They are v2 and stale against D-RCV-60, recorded as
  `CG-A10-CTX-19`.
- No number was allocated for gaps or assumptions; step D1 does the numbering.
- `make_rows.py` in this folder generates the two jsonl files; it is scratch, not an output.
