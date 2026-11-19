<!-- source: 05 Technical architecture/Recovery Workbench Observability and Monitoring Design v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Observability and Monitoring Design v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Observability and monitoring design

SCB Collections and Recovery. Henka Group, 16 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench observability and monitoring design |
| Version | 3 |
| Date | 16 November 2026 |
| Change | v3, 16 November 2026, D-RCV-36: Temporal server and worker metrics, a workflow dashboard, three workflow alerts with run books, and Drools rule package metrics (E2-037) |
| Prepared by | Henka Group |
| Structure | arc42 crosscutting concepts |

# 1. What is measured

| Area | Measures | Source |
|---|---|---|
| Service | Request rate, errors, latency at the 50th and 95th percentile per endpoint | Traces and metrics in Log Analytics |
| Loads | Start, end, rows, checks passed and failed, business date | Job monitor |
| Jobs | Runs, duration, missed runs | Quartz job table |
| Outbox | Items waiting, oldest item, retries, exception queue size | Outbox table |
| Decision log | Entries a day, write failures, chain check result | Decision log |
| Agents | Calls, latency, fallbacks, guardrail failures, cost | Agent runs |
| Cases | Open cases, cases in exception queues, breached service levels | Workbench |
| Data | Stale data products, reconciliation breaks | Data quality console |
| Temporal | Workflow failed count, workflow task timeouts, schedule-to-start latency, activity failures and worker poll failures | Temporal server and worker metrics in Prometheus |
| Rules | KieBase compile count, evaluation count and latency, cache hit ratio, NoPackageInForce count | Drools runtime metrics in Prometheus |

# 2. Alerts

| Alert | Raised when | Goes to | Within |
|---|---|---|---|
| Load failed | A check refuses a load | Data steward, platform administrator | 15 minutes |
| Load late | The load has not arrived by 07:00 | Data steward | 15 minutes |
| Decision log write failed | Any failure | Platform administrator; incident | Immediately |
| Hash chain break | Daily check fails | Compliance, internal audit | Same day |
| Exception queue growing | More than 50 items or older than one day | Platform administrator | 1 hour |
| Error rate | 5xx above 1 percent for 5 minutes | Platform administrator, tech leads | 5 minutes |
| Latency | 95th percentile above 2 seconds for 15 minutes | Platform administrator | 15 minutes |
| Agent fallbacks | Above 10 percent of calls in an hour | Risk and model risk officer | 1 hour |
| Reconciliation break | Any account at 90 days past due without a case | Data steward | Next morning |
| Failed workflow | A workflow execution is failed (MSG-P3-037) | Platform administrator | 5 minutes |
| Stuck workflow | A workflow has no progress for temporal.stuck.hours (=24) | Platform administrator | 1 hour |
| Schedule-to-start latency | Above its threshold for 15 minutes | Platform administrator | 15 minutes |
| Rule package compile failed | A rule package load fails the compile check (MSG-P3-027 with check compile) | Center of excellence analyst, platform administrator | 15 minutes |

Alert thresholds are reference data and change by load. Each alert names one owner; the owner's backup receives it when the owner is absent.

# 3. Dashboards

| Dashboard | For | Shows |
|---|---|---|
| Service health | Platform administrator, ACE team | Availability, errors, latency, saturation |
| Data health | Data steward | Loads, freshness, breaks, exceptions |
| Work health | Team managers | Queues, caps, breached service levels, exception queues |
| Agent health | Risk and model risk officer | Calls, fallbacks, acceptance, cost |
| Workflow health (Grafana) | Platform administrator, RW-PLATADM, RW-COE | Temporal workflows by type and status; failed, stuck, schedule-to-start latency, activity failures and worker poll failures; KieBase compile count, evaluation count and latency, cache hit ratio and NoPackageInForce count. No personal data. |

The workflow health dashboard is a Grafana dashboard fed by Prometheus. It shows counts and durations by workflow type and status, never a case identifier, account number, name or national ID. The same panels carry the Drools signals, so a rule package that fails to compile is visible next to the workflow that depends on it.

# 4. Run books

Every job, load and alert has a run book: what it does, how to check it, how to rerun it and who to call. Run books are written with the story that builds the job (RWB-E1-056).

Each of the four new alerts has a run book: failed workflow, stuck workflow, schedule-to-start latency and rule package compile failure. A run book names the check, the query or link, the action, the escalation and the owner, and it is written with the story that builds the signal (RWB-E2-037).

The Temporal server and worker run books are owned by RWB-E1-070 and RWB-E2-037. The rule package run book (compile failure at load and no package in force) is owned by RWB-E1-073.

A workflow run book starts from the Temporal Web UI behind Entra ID, reads the history summary and the worker build ID, and never decodes a payload outside a break-glass session (RWB-E2-038).
