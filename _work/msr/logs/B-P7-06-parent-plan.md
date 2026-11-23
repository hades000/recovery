# B-P7-06 parent plan (scratch)

- [x] Read Template and Rules v1, ownership.json, plan, checks
- [x] Read the five legacy Epic 1 stories
- [x] Read TSD P7, FSD P7 (A2.1-A2.9), Drools design slides 15-16, Arch v5 rwb-decision rows
- [ ] Fan out 5 subagents, one legacy key each
- [ ] Merge gaps/assumptions rows into _work/msr/gaps/B-P7-06.jsonl and _work/msr/assumptions/B-P7-06.jsonl
- [ ] Run checks/run_all.py --wp B-P7-06 --quick and fix
- [ ] Write _work/msr/editlog/B-P7-06.md

Slice definition per key (rwb-decision's part only):
- E1018: case-creation decision record D6 / CASE_CREATED, ENTRY-2026.11 rule version, ledger ingest of rwb.decision-record.v1, read by case, chain, idempotency, rule model in force + checksum + EV-30.
- E1020: allocation and assignment records (OWNER_ASSIGNED, RULE_GAP), ALLOC-2026.11 ALLOC-014 and ASSIGN-2026.11 ASSIGN-007, one entry per case and business date, rule models in force.
- E1021: transfer records (CASE_TRANSFERRED, TRANSFER_REJECTED), TRF-2026.11 TRF-007 and the eight triggers, manual transfer with caller and reason R03, rule model in force.
- E1028: deadline records (warning, breach R-UNI-30 escalation level 1, prescription date with the LEGAL_PERIOD version in force), reproducibility, nightly chain check JOB-14.
- E1030: rebalance move records (CASE_TRANSFERRED / OWNER_ASSIGNED with reason REBALANCE), ledger count against the run record, DP-17 no data lake copy, read by decision code and date.
