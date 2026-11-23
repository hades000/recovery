# Edit log B-ITG-W1-02 — RWB-ITG-W1 Wave 1 integration

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-ITG-W1-02 (legacy RWB-E1-013, RWB-E1-015, RWB-E1-016, RWB-E1-017, RWB-E1-018)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, in one dispatch.

## Story files written (5)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1013 ITG Baseline measures - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1015 ITG Freshness stamp per data product - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1016 ITG Access control per data product and catalog entries - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1017 ITG Retention and archive rule for the data store - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1018 ITG Case ID issuance and case record v1 - integration v1.md`

Every story carries the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in order, the 19 `### n.` section headings of §R7.2 in order, the nine contract sub-tables 12.1–12.9, the §16 Level column, the origin tag on every Scenario line and the D-RCV-60 change-log row. The service facts follow §R4: the integration service is rwb-integration (P2), the suite is a test harness and provides no API, no event and no table; the P2 reserved names are recorded but unused.

## Fragments written (5)

- `_work/msr/fragments/RWB-ITG-E1013-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1015-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1016-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1017-ITG.json`
- `_work/msr/fragments/RWB-ITG-E1018-ITG.json`

Each fragment has the 28 keys of the WP: id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file. H, C and X are empty on every ITG story; I carries the WP list; the tcs are the legacy IDs in the WP order; `acs` carries the owned legacy ACs or, for E1017, the ten new D-RCV-60 ACs.

## Candidate registers

- `_work/msr/gaps/B-ITG-W1-02.jsonl` — 5 rows (GAP-0339, GAP-0340, GAP-0341, GAP-0342, GAP-0343).
- `_work/msr/assumptions/B-ITG-W1-02.jsonl` — 5 rows (ASM-0433, ASM-0434, ASM-0435, ASM-0436, ASM-0437).

One combined gap row and one assumption row per legacy key, as the WP allows. Rows were written per key to temporary part files and merged once, so no duplicate id and no concurrent write to the register.

## Coverage

- RWB-E1-013: AC2 and AC6 copied verbatim with `(legacy RWB-E1-013 ACn)`; 9 legacy TCs carried as `-ITG` copies; the data-lake removal (DP-17) and the P9 measure-definition load path are the recorded gap and assumption.
- RWB-E1-015: AC1, AC2, AC4, AC5, AC6, AC7, AC9, AC10 and AC11 copied verbatim; 12 legacy TCs carried as `-ITG` copies; the P8 wave 2 job pair and the removed lake copy of the case list are the recorded gap and assumption.
- RWB-E1-016: AC2 copied verbatim; 12 legacy TCs carried as `-ITG` copies; the catalog composition across rwb-source-data, rwb-access and rwb-document is the recorded gap and assumption.
- RWB-E1-017: no legacy AC is owned by this slice; ten new ACs tagged `(new, D-RCV-60)` test only the retention/archive integration (run ownership, archive and delete, legal hold, decision-log exclusion, failure, repeat run, out-of-range rule, boundary, concurrent rerun, right refusal); 10 legacy TCs carried as `-ITG` copies; the P5 retention ownership and the P1 interaction path are the recorded gap and assumption.
- RWB-E1-018: AC1, AC9, AC13 and AC15 copied verbatim; 16 legacy TCs carried as `-ITG` copies; the Kafka CaseCreated event and the P7 decision record replace the local event and log, and the ACE batch fixture is the recorded gap and assumption.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-02 --quick` → C02, C03, C05, C12, C13, C18 all PASS.
- The five story files were additionally checked directly: 20 metadata rows in order, 19 headings, every legacy AC body identical to the legacy §7 apart from the appended origin tag, one placeholder pair per story, all CG/ASM citations resolve to the merged registers, no person name and no email address, no issue-tracker reference, no wrong tool attribution.
- C15 (release unchanged and marked tentative), C16 (service names in topics and REST bases), C17 (candidate register keys and citation resolution) and C20 (tool line) pass on the five stories and five fragments.
- C19 still lists planned outputs of other WPs that have not run yet; no B-ITG-W1-02 output is missing.

## Notes for the assembler

- The ITG slices carry I dependencies only; H, C and X are empty by the WP. The DP table in §13 shows the §R5.5 dependency text for reference and states that the ITG story adds no build dependency.
- The legacy story RWB-E1-013 §12 owns a measure-definition load path that the Ownership Map does not publish for P9; the E1013 assumption points to RWB-P9-E1013-APP for it.
- RWB-E1-015 AC1 and AC6 name JOB-07 and JOB-08, which belong to rwb-payment (P8, wave 2); the wave 1 suite asserts JOB-02 and JOB-04 and the P8 pair is deferred to RWB-ITG-W2.
- RWB-E1-017 has no owned legacy AC; the new ACs use the rule in force and synthetic rows rather than numeric business values, and the ten legacy TCs are mapped to them one to one.
- No legacy master file was changed, and no issue-tracker, Confluence, GitLab or Figma call was made.
