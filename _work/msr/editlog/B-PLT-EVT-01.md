# Edit log B-PLT-EVT-01 — RWB-PLT-EVT Kafka event platform

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Date: 22 November 2026
Work package: B-PLT-EVT-01 (legacy N002, N008, N012)
Fanout: 3 subagents (aisdlc-msr-worker), one per legacy key, dispatched in one message under fanout 5.

## Story files written (3)

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EVT Kafka event platform/RWB PLT N002 INF Kafka topics, retry and dead-letter topics and ACLs - infrastructure v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EVT Kafka event platform/RWB PLT N008 INF Schema registry with BACKWARD compatibility - infrastructure v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-EVT Kafka event platform/RWB PLT N012 INF Blob, Key Vault and MFT SFTP standard resources - infrastructure v1.md`

## Fragments written (3)

- `_work/msr/fragments/RWB-PLT-N002-INF.json`
- `_work/msr/fragments/RWB-PLT-N008-INF.json`
- `_work/msr/fragments/RWB-PLT-N012-INF.json`

## Candidate registers

- `_work/msr/gaps/B-PLT-EVT-01.jsonl` — 3 rows (GAP-1398, GAP-1397, GAP-1399).
- `_work/msr/assumptions/B-PLT-EVT-01.jsonl` — 3 rows (ASM-2434, ASM-2433, ASM-2435).
- One combined gap row and one assumption row per story, as the WP directs. Appended once each, append-only, no rewrite.

## What each story carries

- Every story is new (`preserved=false`, `delta=false`): the two header lines of Template and Rules §R8.1, the 20 metadata rows of §R7.1 in order, the 19 section headings of §R7.2 in order, the nine contract sub-tables 12.1–12.9 (None where empty), the §R7.2 s16 Level column, and the D-RCV-60 change-log row.
- Metadata values copied from the WP JSON: work type INF, owner SCB IT infrastructure, service platform, epic RWB-PLT-EVT, wave 0, business epic NEW, release "None (new story)", disposition New, build status Not started, patterns None, lanes L-PLT-EVT-A/B/C, ready Day 1, H/C/I/X all None, PRD reference "Pending (C1)", status "Draft (realignment v1)".
- ACs: six per story, all tagged `(new, D-RCV-60)`, testing only the deliverable in the title (topic set, retry and dead-letter and ACLs; schema registry and BACKWARD compatibility; Blob, Key Vault and MFT/SFTP). No legacy AC exists for N002, N008 or N012, so no AC is copied and no business value is introduced.
- TCs: six per story, `TC-PLT-N002-INF-01`…`06`, `TC-PLT-N008-INF-01`…`06`, `TC-PLT-N012-INF-01`…`06`, one per AC, with the Level column (Component, Integration, Contract, NFR).
- Naming: only the 19 service shorts and the shared topic `rwb.decision-record.v1` are used; the stories invent no "platform" short, REST base or task queue. No monolith base and no legacy topic name is provisioned.
- Section 12 is None on 12.1–12.8 for N002 and 12.1–12.8 for N012, with the call-type summary in 12.9; N008 records the registry API as a platform API and not a Recovery business contract.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-EVT-01 --quick` → C02, C03, C05, C12, C13, C18 all PASS.
- The `--wp` file list truncates a path at " ("; the parent also ran C15, C16, C17 and C20 directly on the six artefacts and three story files: all PASS.
- No person name, no email address and no issue-tracker reference appears in any file; no legacy master file was changed.

## Notes for the assembler

- The three gaps are genuinely open platform values, not story defects: retry and dead-letter topic names, ACL principals and quotas (N002); registry product, hosting and subject naming (N008); container, key and endpoint names plus rotation and retention periods (N012). Each is answered by one recorded assumption so the stories can be estimated and built.
- N002 provisions 100 topics: 20 event topics (19 service topics plus the shared decision-record topic), 60 retry topics and 20 dead-letter topics.
- N008 registers the event types of the event catalogue including the rows marked + (RouteDecided, AssetSold, JudgmentRecorded, AuctionResult, TreatmentClosed, GuaranteeClaim*, AccountsTransferred, AccessPolicyChanged, DoaLimitChanged, FileDelivered, FileFailed, ReportPublished).
- The story set has no preserved or delta slice, so the "As built (monolith)" rule of Template and Rules §R6 is not used in this WP.
