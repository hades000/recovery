<!-- source: 05 Technical architecture/Recovery Workbench Observability and Monitoring Design v2.docx -->
<!-- converted: 2026-11-04 from DOCX -->

> **Source:** `05 Technical architecture/Recovery Workbench Observability and Monitoring Design v2.docx`  
> **Converted from:** DOCX

Recovery Workbench

Observability and monitoring design

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench observability and monitoring design |
| Version | 1 |
| Date | 28 October 2026 |
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

Alert thresholds are reference data and change by load. Each alert names one owner; the owner's backup receives it when the owner is absent.

# 3. Dashboards

| Dashboard | For | Shows |
|---|---|---|
| Service health | Platform administrator, ACE team | Availability, errors, latency, saturation |
| Data health | Data steward | Loads, freshness, breaks, exceptions |
| Work health | Team managers | Queues, caps, breached service levels, exception queues |
| Agent health | Risk and model risk officer | Calls, fallbacks, acceptance, cost |

# 4. Run books

Every job, load and alert has a run book: what it does, how to check it, how to rerun it and who to call. Run books are written with the story that builds the job (RWB-E1-056).
