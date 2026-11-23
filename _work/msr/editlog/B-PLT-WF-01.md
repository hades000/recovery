# Edit log B-PLT-WF-01 — RWB-PLT-WF Temporal workflow platform

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-PLT-WF-01 (legacy N010, RWB-E1-070, RWB-E1-071, RWB-E2-037, RWB-E2-038)
Fanout: 5 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message under fanout 5.

## Story files written (10)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT N010 APP Workflow kit templates and codec server v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT N010 CON Workflow kit templates - interface and fake - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E1070 APP Temporal platform on the ACE AKS clusters v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E1070 CON Temporal platform on the ACE AKS clusters - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E1071 APP Temporal worker and SDK in the recovery module v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E1071 CON Temporal worker and SDK in the recovery module - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2037 APP Temporal observability and run books v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2037 CON Temporal observability and run books - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 APP Temporal security, codec server and admin audit v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 CON Temporal security, codec server and admin audit - contract v1.md`

## Fragments written (10)

- `_work/msr/fragments/RWB-PLT-N010-APP.json`
- `_work/msr/fragments/RWB-PLT-N010-CON.json`
- `_work/msr/fragments/RWB-PLT-E1070-APP.json`
- `_work/msr/fragments/RWB-PLT-E1070-CON.json`
- `_work/msr/fragments/RWB-PLT-E1071-APP.json`
- `_work/msr/fragments/RWB-PLT-E1071-CON.json`
- `_work/msr/fragments/RWB-PLT-E2037-APP.json`
- `_work/msr/fragments/RWB-PLT-E2037-CON.json`
- `_work/msr/fragments/RWB-PLT-E2038-APP.json`
- `_work/msr/fragments/RWB-PLT-E2038-CON.json`

## Candidate registers

- `_work/msr/gaps/B-PLT-WF-01.jsonl` — 11 rows: GAP-1439, -N010-2, -E1070-1, -E1070-2, -E1071-1, -E1071-2, -E2037-1, -E2037-2, -E2037-3, -E2038-1, -E2038-2.
- `_work/msr/assumptions/B-PLT-WF-01.jsonl` — 11 rows with the matching ASM ids.
- One combined gap row and one assumption row per story (10 stories), plus one extra conflict row and its assumption for the E2037 scan cadence: 11 rows each, append-only, written once per subagent and never rewritten.

## What each story carries

- Every story: the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in order, the 19 section headings of §R7.2 in order, the nine contract sub-tables 12.1–12.9 (None where empty), the §R7.2 s16 Level column and the D-RCV-60 change-log row with the tool line.
- Metadata copied from the WP JSON: work type APP/CON, owner "TechX (suggested; any team may pick up this story)", service platform, epic RWB-PLT-WF, wave 0, business epic NEW/EP01/EP02, release "None (new story)" or "30 November 2026 (tentative)"/"31 December 2026 (tentative)", disposition New/Split (rework), build status Not started, patterns exactly as listed (None for N010), lanes L-PLT-WF-B/D/E/F/G and CG-W0, ready Day 1, H/C/I/X exactly as the WP, PRD reference "Pending (C1)", status "Draft (realignment v1)".
- Legacy ACs owned: 29 in total (E1070 AC1–AC7, E1071 AC1–AC7, E2037 AC1–AC8, E2038 AC1–AC7), each copied with every value kept and tagged "(legacy RWB-… ACn)". New ACs: 37, all tagged "(new, D-RCV-60)", testing only the deliverable in the story title.
- Legacy TCs kept: 34 with their IDs and the new Level column (System mapped to Integration or Component, Operational to Component or NFR, Access to Component). New TCs: 37 (TC-PLT-N010-APP-01…07, TC-PLT-N010-CON-01…06 and the CON series of the four legacy keys).
- §12 is realigned to the target: the codec server speaks the Temporal codec server protocol on the platform internal ingress (no `/api/recovery` base); the smoke operation is the PLT-owned `POST /admin/workflows/smoke` from the Ownership Map; the access log is the P4 base `/api/recovery/access/v1/admin/access-log`; the catalogue read is the P2 base `/api/recovery/integration/v1/admin/scheduled-jobs`; the parameters and reference reads are the P3 bases.
- Platform identity rule applied: RWB-PLT-WF is shared platform, not one of the 19 services, so no `rwb_*` schema, no `rwb.<short>.events.v1` topic, no `/api/recovery/<short>/v1` base and no service short is invented; the Temporal namespace `rwb-recovery` is used as specified and the platform task queue `rwb-platform` is carried as the working read of the assumption (Ownership Map JOB-22).
- Realignment deltas recorded in the stories: E1070 AC2 expresses the monolith schema and login as `rwb_case` and the P3 rwb-case login (DP-01, DP-02); E1071 AC1/AC3/AC5 replace the Quartz smoke job with the JOB-22 Schedule and the monolith base with `POST /admin/workflows/smoke` (DP-10, DP-13); E2037 runs the scanner as JOB-21 every 5 minutes instead of the legacy Quartz 15 minutes (Arch v5 slide 44) with the conflict recorded; E2038 runs the 02:00 reconciliation as a Temporal Schedule.
- N010 (new) applies no DP row: the metadata reads None and §13 states why (no legacy marker), following the RWB-PLT-N002-INF precedent.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-WF-01 --quick` → C02, C03, C05, C12, C13, C18 all PASS (0 findings).
- Targeted runs over the 23 Write-only artefacts: C01, C06, C07, C15, C16, C17, C20 PASS. C09/C10/C11 carry findings only for other legacy keys of other WPs that are still in flight; no finding names RWB-E1-070, RWB-E1-071, RWB-E2-037, RWB-E2-038 or N010.
- No person name, no email address, no issue-tracker reference and no "Claude" attribution appears in any file; no legacy master file was changed; no file outside the Write-only list was written.

## Notes for the assembler

- The 10 platform-identity gaps are one issue per story, not a story defect: §R4 has 19 service rows and no platform row, so the platform login, task queue and admin base have to be fixed in the Wave 0 Service Catalog. Each is answered by one recorded assumption so the stories can be estimated and built.
- The E2037 cadence conflict is a genuine source disagreement: the legacy story uses a Quartz scanner every 15 minutes, while Arch v5 slide 44 and the Ownership Map JOB-21 say every 5 minutes. The story uses 5 minutes and records the legacy value as superseded (GAP-1446).
- The E1070 run book path stays `docs/operations/runbooks/RWB-E1-070.md` word for word; if the RWB-PLT-E1056-OPS catalogue publishes a different run book name, that is a follow-up correction, not a gap of this WP.
- Fragment `tcs` carries the story's own test case IDs (legacy IDs for the APP stories, new CON IDs for the CON stories); legacy TCs are not duplicated onto the CON stories, which own no legacy AC.
- `workflows` in the N010 fragments carries the eight L3 template names (Approval, Notify, Document intake, Agent run with rule fallback, Human task with SLA timers, Saga runner, Scheduled job, Partner instruction); §12.5 maps each to its `Kit…Workflow` type name.
