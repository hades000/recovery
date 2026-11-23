# WP A6-api — Ownership Map part: api
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-msr-worker. fanout: 0
Read only:
- _work/msr/plan/ownership_skeleton.json (section "api")
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md (catalogue slides 14-20 and 41-44 win over narrative slides)
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- _work/msr/extract/ (FSD v6 and TSD v5 module files, Event and Messaging, Batch and Scheduling, Physical Schema)
- The R-PREC precedence and default rulings in 2026-11-22-recovery-microservice-realignment-implementation-plan.md Appendix R §R3
Write only: _work/msr/plan/ownership_part_api.json ; _work/msr/gaps/A6-api.jsonl ; _work/msr/assumptions/A6-api.jsonl ; _work/msr/editlog/A6-api.md
Do: for EVERY item in the skeleton section, choose exactly one owner from P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, S1, S2, S3, S4, S5, S6, S7, S8, S9, PLT. Use R-PREC order. The "hint" counts are which legacy module stories mention the table (a hint, not a rule).
Output JSON: {"api": [{"id": "<table | METHOD path | EV-nn | JOB-nn | Workflow>", "owner": "<code>", "basis": "<source file + slide/section>", "ruling": "<text or empty>", "asm": "<ASM-A6-api-n or empty>"}]}
Every ruling (two sources disagree) also gets a gap row (type Conflict, severity P2) and an assumption row.
Jobs: also give "replacement": "Temporal Schedule <name> in <service>" or "event-started workflow" (v5 slide 44); Quartz is retired.
Finish: every skeleton item appears once in your output. Write the edit log with tool line T3 Code / OpenCode / DeepSeek v4.1 Flash.
