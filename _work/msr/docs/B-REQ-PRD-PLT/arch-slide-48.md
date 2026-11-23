
A8 · Volumes are modest; peaks come from the daily batch and document intake

We do not split for throughput; we split so each capability can change, fail and scale on its own

3,110
new cases a month

~21 req/s
414 concurrent staff at peak

48
concurrent partner users (320 total)

64-74k
documents a month; 2.8 TB by 2031

283-318k
rule evaluations a month

55-62k
decision-log entries a month

| Route work a month | Volume |
|---|---|
| Registered letters | 1,909 |
| Lawsuits filed | 667 |
| Repossessions | 720 |
| Debt-sale accounts | ~315 |
| Property sales | 29 |


Service targets (NFR v3)
Screen response < 2 s (p95)
Rule evaluation < 300 ms
AI agent: 60 s, then rule result
99.9% in business hours
RPO/RTO: not yet set

What actually needs to scale
The 05:00-07:00 chain: case creation, payment matching, allocation, rebalance
OCR and document intake: bursts of uploads; 500 pages an hour
Notice generation at 16:00 and court-date timers; AI agent runs
The screens (API tier) are light: 2 small pods per service are enough

Split for ownership and isolation, scale only the hot paths

48

Notes: All figures from Volume and Scale Forecast v3 and NFR Spec v3. Open cases: 23,570 today, 26,479 by end 2027, 47,389 by 2031. New cases ~3,110 a month. 414 concurrent internal users is ~21 requests a second at peak; 320 partner users with 48 concurrent.

Where load concentrates: the overnight/morning chain (case creation and allocation by 07:00), OCR (500 pages an hour target), notice generation (WIN batch 16:00), rule evaluation (283-318k a month).

Implication: a single well-built service could carry this load. The case for splitting is ownership, release independence, failure isolation and regulatory isolation (AI, partner DMZ, audit), not raw throughput. Scaling is by worker pools (KEDA) on the few hot paths.

NFR gap: RPO/RTO are not set in NFR Spec v3; proposed tiers.

