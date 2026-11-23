# Edit log B-PLT-WF-02 — RWB-PLT-WF Temporal workflow platform (legacy RWB-E2-039, RWB-E2-040, N003, NF-08)

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-PLT-WF-02 (legacy RWB-E2-039, RWB-E2-040, N003, NF-08)
Fanout: 5 subagents (aisdlc-msr-worker) dispatched in one message under fanout 5 — E2039-APP, E2039-CON, E2040-APP, E2040-CON, and one subagent for the two infrastructure stories N003 and NF-08.

## Story files written (6)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2039 APP Temporal resilience  backup, failover, upgrade and archive v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2039 CON Temporal resilience  backup, failover, upgrade and archive - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2040 APP Workflow versioning and replay test gate v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2040 CON Workflow versioning and replay test gate - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT N003 INF Temporal namespace rwb-recovery and codec key - infrastructure v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT NF08 INF Temporal platform baseline - infrastructure v1.md`

## Fragments written (6)

- `_work/msr/fragments/RWB-PLT-E2039-APP.json`
- `_work/msr/fragments/RWB-PLT-E2039-CON.json`
- `_work/msr/fragments/RWB-PLT-E2040-APP.json`
- `_work/msr/fragments/RWB-PLT-E2040-CON.json`
- `_work/msr/fragments/RWB-PLT-N003-INF.json`
- `_work/msr/fragments/RWB-PLT-NF08-INF.json`

## Candidate registers

- `_work/msr/gaps/B-PLT-WF-02.jsonl` — 6 rows, one combined gap row per story: GAP-1447, GAP-1448, GAP-1449, GAP-1450, GAP-1451, GAP-1452.
- `_work/msr/assumptions/B-PLT-WF-02.jsonl` — 6 rows with the matching ASM ids, one default per story.
- Every row is type Missing, severity P1, needed_by_wave 0, confidence Medium: the shared Temporal platform has no row in Template and Rules §R4, so the platform login and admin base, the task queue, the backup/restore owner, the archive immutability period and manifest retention, the replay container retention, the pinned server and SDK release, the namespace quotas, rate limits and certificate set, and the baseline compatibility matrix and conformance cadence are named by no read source. Each story writes the §R9 placeholder where the value is still open and continues in Draft.
- The six subagent staging files in `_work/msr/logs/` are the audit trail of the rows merged above; only the merged registers carry the ids that the stories cite.

## What each story carries

- Every story: the two §R8.1 header lines, the 20 metadata rows of §R7.1 in order, the 19 section headings of §R7.2 in order, `#### 12.1`–`#### 12.9` with "None" where empty, the §R7.2 s16 Level column, the D-RCV-60 change-log row and the tool line.
- Metadata copied from the WP JSON: work type APP/CON/INF, the fixed owner phrase for TechX and for SCB IT infrastructure, service platform, epic RWB-PLT-WF, wave 0, business epic EP02 / NEW / NF, release `31 December 2026 (tentative)` or `None (new story)`, legacy disposition Split (rework) / New / Moved (no impact), build status Not started, patterns exactly as listed (DP01–DP19 sets for the four E2 stories, None for N003 and NF-08), lanes L-PLT-WF-H, CG-W0, L-PLT-WF-I, CG-W0, L-PLT-WF-A, L-PLT-WF-C, ready Day 1, H/C/I/X exactly as the WP, PRD reference `Pending (C1)`, status `Draft (realignment v1)`.
- Legacy work: RWB-E2-039 AC1–AC9 copied with every value (case-RW-2026-000201 to -000102, 09:40/09:42/09:55/10:00, 12 workflows, smoke at 14:06, 5 workflows, 30 days, 7 days, 02:00, dt=2026-10-23, national ID 1101700203456, key version 2, three retries) and its 11 TCs; RWB-E2-040 AC1–AC8 copied with every value (40 histories, 200 histories, 01:00/09:00, build IDs 9f3c2a1-418 and 7b1d4e0-419, event ID 4 ActivityTaskScheduled, Workflow.getVersion("smoke-step-2", Workflow.DEFAULT_VERSION, 2), 60 seconds, 10 minutes, 12 and 2 running workflows, 36 hours, 1101700203456, gate 10, MSG-P3-038) and its 10 TCs.
- 43 acceptance criteria in total: 17 legacy (9 + 8) and 26 new (E2039-CON 8, E2040-CON 8, N003 6, NF08 7), all new ones tagged `(new, D-RCV-60)` and testing only the deliverable in the title. 50 test cases in total: 21 legacy ids kept (11 + 10), 29 new (8 + 8 + 6 + 7).
- The CON stories own no legacy AC by the WP, so they carry no legacy TC; the legacy ids stay with the APP stories, and no legacy TC is duplicated.
- Realignment deltas recorded: the Quartz archive job becomes the `HistoryArchiveJob` Temporal Schedule at 02:00 on task queue `rwb-platform` (DP-10; RWB-TE-007 retired) and the Quartz nightly export becomes the 01:00 `HistoryExportJob` Schedule; the platform is shared platform, so no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base is invented (§R4 has no platform row); the decision entry is written through DecisionLogApi of RWB-PLT-E1027-CON; parameters and reference data come through the platform contracts and their C rows; Worker Versioning and Temporal 1.30+ carry the replay gate; the archive is write-once in Blob with a manifest row and a checksum.
- NF-08 is written as the versioned baseline standard of the shared Temporal layer (version baseline, topology, determinism rule, Continue-As-New, Worker Versioning and the replay gate, codec, retention and archive, metrics/UI/codec-server baseline, ACE availability and recovery objectives, compatibility matrix, conformance check and evidence) and stays disjoint from RWB-PLT-E1070 (cluster install), RWB-PLT-N003 (namespace and codec key), RWB-PLT-N010 (kit), RWB-PLT-E2037 (observability) and RWB-PLT-E2038 (codec server).
- N003 is written as the namespace `rwb-recovery` record plus the AES-GCM codec key in Key Vault, the entitlements, the four search attributes and the namespace evidence pack, and names the cluster, mTLS, UI and codec-server runtime as RWB-PLT-E1070's.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-WF-02 --quick` → C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, 0 findings, exit 0, rerun after the registers were merged.
- Targeted runs over the 15 Write-only artefacts: C06 PASS, C07 PASS, C15 PASS, C16 PASS, C17 PASS, C20 PASS, C09 PASS. C10 and C11 carry findings only for other legacy keys of other work packages that are still in flight; no finding names RWB-E2-039, RWB-E2-040, N003 or NF-08.
- No person name, no email address, no issue-tracker reference and no other tool attribution appears in any file; no legacy master file was changed; no file outside the Write-only list was written.

## Notes for the assembler

- One gap and one assumption per story, not one per value: the platform-identity question is a single Wave 0 Service Catalog fix that all six stories inherit, so each story raises it once and answers it with one recorded default.
- The platform task queue name `rwb-platform` is written inside backticks everywhere (C16 treats a bare "queue rwb-<name>" as a service name, and "platform" is not one of the 19 service shorts). Three legacy Given lines therefore carry the backticks around the queue name; no value in any criterion changed, and the E2-039 AC3 line is the one where the mark-up is required for the check.
- The E2039 CON story carries eight contract TCs and no legacy TC; the eleven legacy ids are cited only by RWB-PLT-E2039-APP, which is the story that owns the nine legacy criteria.
- N003 and NF-08 have no legacy story in any read source (the WP source is null), so both were filled from the architecture, the Temporal design and the program BRD under §R7.3, and every value that no source states is left as the §R9 placeholder answered by the recorded assumption.
