# Recovery Workbench: Service Volume and Temporal Sizing (Summary)

Draft · 24 November 2026 · D-RCV-60 · Full detail and workings: *Recovery Workbench Service Volume, Calls and Temporal Sizing v1*

## The short answer

Recovery's load is **small**. About 21 screen requests a second at peak, about 26k events a day, and under 10 Temporal actions a second in business hours. We split into 19 services for ownership and isolation, not for throughput (Architecture v5 slide 48). So:

- **2 small API pods per service** is enough. No service needs to autoscale its API.
- **Scale only five worker pools:** case, payment, document, comms and agent.
- **Size Temporal for bursts and for long-running workflows**, not for average throughput.

Figures marked **(est)** are our estimates where no source gives a number. Section 5 says how each was worked out.

## 1. Headline numbers (2027)

| What | Volume | Source |
|---|---|---|
| Open cases | ~23,600 at go-live → 27,100 in 2027 → 47,400 by 2031 | NFR-001, Volume Forecast v4 |
| New cases | ~3,000 a month (5,200 by 2031) | Volume Forecast v4 |
| Users at peak | ~414 concurrent (366 staff, 48 partners) | Volume Forecast v4 |
| Screen requests | ~21 a second at peak | Volume Forecast v4 |
| Documents | ~72k a month; 2.8 TB by 2031 | Volume Forecast v4 |
| Kafka events | ~563k a month, ~26k a business day (est) | Arch v5: "tens of thousands a day" |
| Temporal workflows started | ~261k a month (est) | |
| Temporal workflows open at once | ~120k, up to ~290k if every restructured account is monitored (est) | |

## 2. How services talk to each other

| Call type | Used for | Why |
|---|---|---|
| **REST** (sync) | Screens: browser → gateway-bff → one owner service | A person is waiting (< 2 s). One hop only, so a slow service cannot slow a chain of others |
| **Kafka event** (async) | Facts that happened, e.g. CaseCreated, PaymentMissed | Many services can listen, events arrive in order per case, and history can be replayed |
| **Temporal** (activity or child workflow) | Asking another service to do a step, e.g. approve, send a letter, post proceeds; long processes | Survives restarts, retries on its own, and holds timers for months or years |
| **Nexus** | rwb-treatment → ACE restructure calculator | Crosses into ACE's own namespace safely |
| **SQL view** | Only rwb-source-data reads ACE | One read grant for the whole Workbench |
| **File** | WIN letters, debt-buyer files, posting files | Outside parties take files |

## 3. Per service (2027)

| Service | Main volume a month | Peak requests a second | Events a month | Temporal starts a month (open at once) | Scales? |
|---|---|---|---|---|---|
| P1 source-data | 28,119 accounts a day; 25 ACE view reads a second (74 in a burst) | 12 | ~30 | ~45 | No |
| P2 integration | ~70 files | < 0.1 | ~70 | Activities only | No |
| P3 case | 2,980 new cases; 27,100 open | 6.4 | ~64k | 3,000 (27,100 open) | **Yes, 05:00–07:00** |
| P4 access | Permission checks (cached) | ~1 | < 50 | — | No |
| P5 document | 71,800 documents | 2.2 | ~117k | 71,800 | **Yes, OCR bursts** |
| P6 comms | ~81k notices (est) | 0.9 | ~165k (est) | 81,300 (est) | **Yes, 16:00** |
| P7 decision | 63k ledger entries; ~11.6k approvals (est) | 1.5 | ~86k | 11,600 (est) | Small |
| P8 payment | 13k–187k receipts (est) | 0.7 | ~25k (est) | Activities only | **Yes, 05:00–07:00** |
| P9 reporting | 1 publish a day | 0.9 (est) | ~22 | ~30 | No |
| P10 agent | ~76k agent runs | 0.2 | ~76k | 76,300 | **Yes, bursts** |
| S1 valuation | 2,980 route decisions | 0.5 | ~3k | 2,980 | No |
| S2 treatment | ~4,000 treatments | 1.5 | ~8k | 4,000 (~48k open; ~222k if every restructured account is monitored) | No |
| S3 guarantee | ~360 claims (est) | 0.2 | ~720 | 360 | No |
| S4 litigation | 667 lawsuits | 1.1 | ~1.7k | 667 (~24k open, run for years) | No |
| S5 asset | ~750 assets | 0.7 | ~1.5k | 750 (~6k open) | No |
| S6 debtsale | ~315 accounts; ~1 lot (est) | 0.2 | ~2 | ~1 | No |
| S7 writeoff | 894 write-offs | 0.2 | ~900 | 894 | No |
| S8 deviation | 2,980 screenings; ~300 raised (est) | 0.4 | ~600 | 2,980 | No |
| S9 partner | ~4,500 instructions (est); 48 partners online | 2.8 | ~13.6k | 4,520 (~10k open) | No |

## 4. Temporal sizing

| Setting | Proposal | Why |
|---|---|---|
| Throughput | 100 actions a second sustained, 200 in a burst | Normal load is 7–10 a second. 10x headroom covers bursts and 2031 growth |
| History shards | **512** | Cannot be changed after the cluster is built, so set it once with room to grow |
| Server pods | 2 each of frontend, history (3 in PROD), matching and internal-worker | For availability, not load |
| Database | PostgreSQL, 100 GB | Expected 20–32 GB in 2027 and ~45 GB in 2031. Writes are frequent, so plan the disk for write speed |
| Namespace rate limit | ~400 requests a second | The cluster is shared with ACE, so a Recovery fault must not slow ACE |
| Retention | 30 days, then archive to Blob | Already decided (RWB-PLT-NF08) |
| Long workflows | Continue-As-New at each stage end and at least every 28 days | Already decided. Keeps each history small |
| Workers | Case 2–6, document 2–8, payment 1–4, comms 1–4, agent 1–6, decision 1–3, all others 1–2 | Scale on queue backlog (KEDA). Agent runs are limited by the AI endpoint quota |
| Bulk timers | Spread restructure due-date timers over 2–4 hours | ~87k timers could fire on one date and collide with the 05:00–07:00 chain |

## 5. Our estimates where the sources give no number

| Service | Estimate | How we got it |
|---|---|---|
| Comms: SMS/LINE | ~54k a month | 2 messages per open case (a reminder before the due date, a notice after a miss). If ACE Common records them instead, comms drops to ~27k notices |
| Payment: receipts | 13k a month (base) to 187k (high) | Base: 40% of open-case accounts pay each month. High: also one instalment for each of the 173,807 restructured accounts. **We size for high** |
| Decision: approvals | ~11.6k a month | One approval for each material action whose contract asks for one |
| Guarantee: claims | ~360 a month | Half of new SSME cases claim a TCG guarantee, plus 5% of Mortgage and HP cases claim insurance |
| Partner: instructions | ~4,500 a month | Lawsuits + repossessions + auction listings + valuations + 30% of new cases placed with agencies |
| Debt sale: lots | ~12 a year | 3,783 accounts a year at about 300 accounts a lot |
| Reporting: reads | ~0.9 a second | 5% of staff screen requests |

## 6. To confirm

| What | Who (role) | When |
|---|---|---|
| Temporal shards, database, rate limit, pod sizes | ACE platform team | **Before the cluster is built** |
| Kafka quota at ~563k events a month | ACE platform team | Wave 1 |
| Connection limits per service login | ACE DBA | Wave 1 |
| SMS/LINE volume, and who records it | Communications owner with the ACE Common team | Wave 1 |
| Approval counts | Risk with the decision center owner | Wave 1 |
| Receipt volume | Payments owner | Wave 2 |
| Guarantee claims | Guarantee owner | Wave 3 |
| Partner instructions | Partner and agency manager | Wave 4 |
| Agent concurrency quota | Enterprise AI endpoint owner | Wave 1 |

*Note: Architecture v5 says "3,110 new cases a month". That figure is new accounts; it works out to ~3,000 cases.*
