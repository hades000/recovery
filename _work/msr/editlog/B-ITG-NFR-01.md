# Edit log B-ITG-NFR-01 — RWB-ITG-NFR (non-functional integration)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-NFR-01 (legacy RWB-TE-009, RWB-TE-010)
Fanout: 2 subagents (aisdlc-msr-worker), one per legacy key, in one dispatch.

## Story files written (2)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-NFR Non-functional integration/RWB ITG TE009 ITG Performance test harness - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-NFR Non-functional integration/RWB ITG TE010 ITG Browser and accessibility tests - integration v1.md`

Each story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in order, the 19 section headings of §R7.2 in order, the nine sub-tables 12.1–12.9, the §R7.2 s16 Level column, the origin tag on every Scenario line and the D-RCV-60 change-log row. The service facts follow §R4 for P2 rwb-integration: schema `rwb_integration`, REST base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, event names `rwb.integration.<Event>.v1`, task queue `rwb-integration`, Java package `th.co.scb.ace.workbench.recovery.integration`.

## Fragments written (2)

- `_work/msr/fragments/RWB-ITG-TE009-ITG.json`
- `_work/msr/fragments/RWB-ITG-TE010-ITG.json`

Each fragment has the 28 keys of the WP: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file.

## Candidate registers

- `_work/msr/gaps/B-ITG-NFR-01.jsonl` — 2 rows (GAP-0330, GAP-0331; one combined gap row per legacy key).
- `_work/msr/assumptions/B-ITG-NFR-01.jsonl` — 4 rows (ASM-0422, ASM-0423, ASM-0424, ASM-0425; two defaults per legacy key).

The register rows were written once by the parent with a per-key id, so the two parallel subagents could cite them without a concurrent write to the same jsonl file. Counts: CG = 2, ASM = 4.

## Coverage

- RWB-TE-009 has no legacy ACs and no legacy TCs (§7 and §16 of the legacy story say "None"), so its ITG story carries six new ACs (AC1–AC6) and six new TCs (TC-ITG-TE009-ITG-01 to -06), all tagged `(new, D-RCV-60)` and testing only the harness deliverable. Every business value is copied from the legacy story: 410 virtual users at 3 requests a minute, 10-minute ramp, 60-minute steady period, 95th percentile under 2,000 ms, error rate under 1 percent, at least 23,600 open cases, one run at a time with the lock released within 90 minutes.
- RWB-TE-010 has no legacy ACs and no legacy TCs, so its ITG story carries eight new ACs (AC1–AC8) and eight new TCs (TC-ITG-TE010-ITG-01 to -08). The values are copied from the legacy story: WCAG 2.1 A and AA, current and previous major versions of Microsoft Edge and Google Chrome (four browser configurations), Thai and English, the six screens SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09, MSG-P4-002 for a role without the right, and one retry with a flaky list.
- Patterns applied from the plan: RWB-ITG-TE009-ITG DP01, DP07, DP10, DP13, DP19, DP20; RWB-ITG-TE010-ITG DP07, DP19. The §13 pattern table reproduces the §R5.5 rows; the H, C, I and X lists stay empty as the plan sets them, because both stories are pipeline stages that run against deployed SIT services and published contracts. P2 rwb-integration provides no REST operation in either story, so 12.1, 12.3 to 12.8 are `None` and 12.2 lists the consumed operations with owners from the Ownership Map only.
- The monolith base never appears outside a legacy marker in the pattern table; every consumed operation uses `/api/recovery/<short>/v1` on the owner's service (DP-13) through gateway-bff (DP-19).
- No person name, no email address and no issue-tracker reference appears in any file; no legacy master file was changed.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-NFR-01 --quick` — C02, C03, C05, C12, C13, C18 all PASS.
- Additional checks run directly on the six WP artefacts: C15 (release 31 December 2026 tentative), C16 (service names), C17 (every cited CG/ASM id has a register row) all PASS.
- C19 still reports planned outputs of WPs not yet run; no B-ITG-NFR-01 output is missing.
