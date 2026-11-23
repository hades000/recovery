# A6-flows - Ownership Map part: flows

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Agent: aisdlc-msr-worker
Date: 22 November 2026
WP: A6-flows (fanout: 0)

## Files written

1. `_work/msr/plan/ownership_part_flows.json`
2. `_work/msr/gaps/A6-flows.jsonl`
3. `_work/msr/assumptions/A6-flows.jsonl`
4. `_work/msr/editlog/A6-flows.md`

## What was done

1. Read the skeleton sections `events` (30 items), `jobs` (22 items) and `workflows` (15 items) from `_work/msr/plan/ownership_skeleton.json`; 67 items in total.
2. Applied R-PREC from the implementation plan Appendix R R3: Arch v5 catalogue slides 13-20 and 41-44 first, then the Temporal and Drools Detailed Design, then the narrative slides, Decision Log, ADRs, Technical Specifications, Functional Specifications and the Physical Schema. The FSD v6 and TSD v5 module files were not in `_work/msr/extract/`; the read-only originals in folders 03 and 05 were used for spot checks instead, and nothing outside the read-only list was written.
3. Events: took the producer and topic from the Arch v5 event catalogue (slides 42-43) and the owning service from the service contracts (slides 14-20). Checked every event against the Event and Messaging Design v4 owning module. EV-18 is retired and is a durable timer, so it maps to PLT; EV-08 is published by every service but its type, topic and ledger belong to P7.
4. Jobs: none left on Quartz. Each job has a replacement in the WP format where the v5 job map allows it: a Temporal Schedule name in the owning service, an event-started workflow, or an explicit no-Schedule entry for the retired or continuous jobs. JOB-01 and JOB-09 are retired under D-RCV-35 and are owned by P1 for the ACE view contract; JOB-05 is retired in favour of durable timers; JOB-11 is the service-template outbox relay; JOB-13 is continuous Kafka ingest; JOB-15 is Airflow-triggered.
5. Workflows: all 15 map to the workflow owner named in the service contracts and the Temporal design (CaseWorkflow to P3, stage workflows to S1-S8, ApprovalWorkflow to P7, DocumentIntakeWorkflow to P5, NoticeDispatchWorkflow to P6, InstructionWorkflow to S9, AgentRunWorkflow to P10, PlatformSmokeWorkflow to PLT).
6. Rulings: 9 items have two sources disagreeing (EV-08, EV-18, EV-21, EV-26, JOB-05, JOB-10, JOB-13, JOB-15, JOB-16). Each one has a Conflict gap row (severity P2) and an assumption row. Three further assumptions cover mappings where the source owner is not a service code (JOB-01 and JOB-09 owner ACE team; JOB-11 owner every service), without a Conflict gap.
7. No value was invented: every owner cites a source file and slide or sheet, and every non-source mapping is an ASM row.
8. Checked that every skeleton item appears exactly once: 30 events, 22 jobs and 15 workflows, no duplicates and no extras. Checked that every ASM cited in the part file exists in the assumptions file, and that every ruling has a gap row and an assumption row.

## Conflicts recorded

- EV-08: producer `all 19` in the v5 event catalogue versus owning module Decision center and log in Event and Messaging Design v4; owner P7.
- EV-18: producer `durable timer` (retired) in the v5 catalogue versus owning module Case and workflow in Event and Messaging Design v4; owner PLT.
- EV-21: producer rwb-partner in the v5 catalogue versus `Consumed` from the partner portal in Event and Messaging Design v4; owner S9.
- EV-26: producer rwb-source-data in the v5 catalogue versus `Consumed` from ACE ingestion in Event and Messaging Design v4; owner P1.
- JOB-05: v5 retires the timer check in favour of durable timers, while D-RCV-36 T2 and ADR-011 keep Quartz and the TimerScheduler port in Epics 1 and 2; owner PLT.
- JOB-10: v5 gives two owners (`rwb-comms + integration`); one owner recorded, P6.
- JOB-13: v5 makes decision-log ingest continuous on Kafka and DP-17 removes the data lake, while Batch and Scheduling Design v4 keeps a nightly data-lake copy; owner P7.
- JOB-15: v5 slide 44 says Airflow trigger with no data lake, while the narrative slides describe a 01:30 Temporal Schedule and Batch and Scheduling Design v4 writes to the data lake; owner P9.
- JOB-16: v5 and the Temporal design make the scan a Temporal Schedule, while Batch and Scheduling Design v4 starts it on the ACE batch record and T2 keeps Quartz; owner S7.

## Verification

- JSON and JSONL parse with PowerShell ConvertFrom-Json: 0 errors.
- Skeleton coverage: events 30/30, jobs 22/22, workflows 15/15; duplicates 0, missing 0, extra 0.
- Owners restricted to the 20 allowed codes: 0 violations.
- Job replacement present for 22/22 jobs.
- 9 rulings, each with 1 Conflict gap and 1 assumption; 12 assumption rows in total; 9 gap rows in total.
- The check harness reads the one-line `Write only` entry as a single path, so `--wp` found no content files to scan. The four files were therefore also checked directly: 0 person names against the folder-21 deny-list, 0 email addresses, 0 issue-tracker words, and 0 unresolved ASM citations.
- `python -I "22 Microservice Realignment/checks/run_all.py" --wp A6-flows --quick` was run after this log was written; the result is in the report file named below. C02, C03, C05, C12, C13 and C18 all PASS with 0 findings.
- Report written by the check script to `22 Microservice Realignment/checks/reports/wp-A6-flows-<timestamp>.md`.
