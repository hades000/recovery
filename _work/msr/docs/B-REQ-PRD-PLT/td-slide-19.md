
S3 · Guarantees and guarantors

File TCG or insurer claims before the deadline and pursue guarantors

Starts when  a guarantee is found at takeover; the claim deadline timer starts (R-GUA-01)

1

Claim deadline timer

R-GUA-01

2

Agent assembles claim

R-GUA-04

3

Officer approves, 3 wd

R-GUA-07

4

Submit to TCG

R-GUA-12

5

Query, part pay or reject

R-GUA-14/17/20

6

Paid: record subrogation

R-GUA-22/23

7

Residual back to D6

R-GUA-25

Runs in
rwb-guarantee
GuaranteeClaimWorkflow

System step

Timer

Signal / event

Drools decision

Person

External system

AI agent

Drools decides

Guarantee route set, 32 rules (package Phase 2)
Deadline missed = claim lost (R-GUA-05)
Disputed guarantee raises X1 (R-GUA-30)

Who approves

Release guarantor: L4 ≤ THB 30m, L3 ≤ 200m
Release TCG guarantee: PARC

Clocks

Claim deadline; warning → Head of Litigation
Guarantor notice runs in parallel (R-GUA-06)

Point of no return / undo

A missed claim deadline cannot be undone

S3 lives or dies on one date; a durable Temporal timer makes sure the deadline is never missed.

19

Notes: Source: FSD S3 Guarantees and guarantors v3; Routing Logic v4 (R-GUA, 32 rules). Today claims are late because deadlines are not tracked. Warning window escalates to the Head of Litigation (R-GUA-11). D6.6 guarantor notice in parallel (R-GUA-06, EV-13/14/15). Release a guarantor (2.1.5); release a TCG guarantee (2.4).

