SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Cutover and go-live plan

| Item | Detail |
|---|---|
| Document | Recovery Workbench cutover and go-live plan |
| Version | 4 |
| Date | 22 November 2026 |
| Supersedes | Version 3, 15 November 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |
| Applies to | The 19 Recovery services inside ACE, cut over one wave at a time, with gateway-bff, Kafka, Temporal and the ACE batch |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft |
| Change | 4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |

Version 4 keeps sections 1 to 9 of version 3, with every ID, number, team code and date in them, and changes the one thing the realignment needs: the cutover is run per wave, because the Workbench is 19 services inside ACE (ADR-013) that arrive with their epics (Architecture v5 slide 38), not one deployable. The per-wave content is added in sections 10 to 12 and in the rows marked as changed. No other position of version 3 changes.

No approval of this version is recorded, so it is issued as Draft: Not specified in the source documents (CG-B-DELIVDOC-46-10; ASM-B-DELIVDOC-46-10).

# 1. How releases go live

Each wave goes live in the change window agreed with SCB IT (DL34). The first release, 30 November 2026 (tentative), is the Wave 1 cutover and also starts the case list.

Services arrive with their waves (Architecture v5 slide 38). Wave 0 is not a release: it puts the platform in place once, with the service template and the Helm chart, the contract libraries, the workflow kit, the 19 schemas and logins, the Kafka topics and ACLs, and Temporal 1.30 or later. Wave 1 carries nine services: P1 rwb-source-data, P2 rwb-integration, P3 rwb-case, P4 rwb-access, P5 rwb-document, P6 rwb-comms, P7 rwb-decision, P9 rwb-reporting and P10 rwb-agent. Wave 2 carries four: P8 rwb-payment, S2 rwb-treatment, S5 rwb-asset and S8 rwb-deviation. Wave 3 carries four: S1 rwb-valuation, S3 rwb-guarantee, S4 rwb-litigation and S6 rwb-debtsale. Wave 4 carries two: S7 rwb-writeoff and S9 rwb-partner. A service is created when its epic starts, so nothing is built twice.

The Workbench runs no load: ACE ingests every source and rwb-source-data (P1) reads the 30 SELECT-only recovery.v_ace_* views (D-RCV-35, ADR-010). No other service reads the views; every other service reads ACE data through the rwb-source-data contract, one hop from gateway-bff. Each service of a wave goes live as its own api and worker deployment, in its own schema rwb_<name> with its own login, on its own topic rwb.<name>.events.v1 and its own task queue rwb-<name> in namespace rwb-recovery, behind its own feature flags. The release is ready when the ACE batch is ready, so the checks in section 6 are wave gates.

If the change is significant under FPG 19/2560 clause 5.5, BOT approval is needed before the Wave 1 cutover, up to 30 business days; the submission date is not stated in the source documents (CG-B-DELIVDOC-46-6; ASM-B-DELIVDOC-46-6).

# 2. Sequence for each release

| When | Step | Who |
|---|---|---|
| Friday before | Go decision on the SIT and UAT exits of the wave; flags for unfinished work confirmed off | Release owner with the product owner and application owner |
| Release day minus 2 | The contract versions of every service in the wave published with their fakes; the wave's schemas, logins, topics, ACLs and task queues checked in production | Solution architect with the platform team and the ACE DBA |
| Release day minus 1 | Reference data, rules and templates for the release loaded with their valid from date | Reference data administrator |
| Release day | Deploy the tag of each service in the wave to production in the change window, one service at a time, each behind its flags | ACE team with the DevOps team |
| Release day | Smoke test: sign-in per role, case list, one decision, one notice, one document, and from Wave 2 one payment | QA engineers with business testers |
| Release day, after the smoke test | Flags on for each service of the wave in the order of section 10.4; a service whose smoke test fails keeps its flag off and stays at its previous build | Release owner |
| Next morning | ACE batch for the business date checked in v_ace_batch_status, then the case list reconciled to the ACE account view | Data steward |
| First week | Floor support for the teams that receive real users | Business analysts, business lead |
| Four weeks after | Benefit check (G6) | Product owner |

# 3. Rehearsal

Each wave is rehearsed in UAT: the deploy of each service in the wave, the reference data load, the smoke test and the rollback of a single service. Wave 1 is rehearsed twice. A later wave is rehearsed against the services it starts and the earlier waves it calls, using their published contracts and fakes.

# 4. Rollback

- Switch the feature flags of the failing service off, service by service. The rest of the wave stays live.

- If a flag does not cover the fault, redeploy the previous tag of that service only. The other services of the wave keep their tags.

- Keep in-flight cases on the build that recorded them: Worker Versioning pins each worker to its build, and a case continues on its pinned version until it continues-as-new.

- Roll a rule package back with one call: the version in force keeps running and the refused or rolled-back version is recorded (states ROLLED_BACK and REFUSED).

- Reload the previous reference data versions if they changed.

- Decisions taken under the new release stay in the decision log: the record written in the service's own schema in the same transaction as the change, then collected into the central ledger of rwb-decision; corrections are new entries.

- No ACE data is rolled back with the Workbench: the views read the ACE batch for the business date, and a wrong batch is corrected in ACE.

# 5. Who decides to go

The release owner in the ACE team decides with the product owner and the application owner, wave by wave. A severity 1 or 2 defect open without a flag stops the wave. A service that fails its own gate is held at its previous build while the rest of the wave proceeds, because each service has its own flags, image and schema; the hold is recorded in the release checklist with the date and time of the next attempt.

# 6. ACE batch readiness check

The check runs on the release day of every wave before the smoke test, and again on the first morning after the release. A failed check holds the part of the release that reads ACE; the Workbench features that read no ACE data go ahead behind their flags. Only rwb-source-data reads the views, so one check covers every service of the wave.

| Check | Passes when | Who confirms |
|---|---|---|
| ACE additions | RWB-ACE-001 is applied in PROD and the 14 tables and 12 columns are present | ACE team lead |
| Batch complete | ace_batch_run holds a COMPLETED row for each recovery source and the business date, and v_ace_batch_status returns it | ACE ingestion owner |
| Grant in place | The view-owner role selects the 21 listed ACE tables and no other; the rwb_source_data login reads the 30 recovery.v_ace_* views only and writes no ACE table | ACE DBA with SCB IT security |
| Views resolve | 16 Section A and 14 Section B views compile, and the conformance test resolves the 80 appendix fields | Data steward |
| Case list runs | JOB-02 starts on AceDataReady for the ALS business date and creates no case from an incomplete batch (DailyCaseRun in rwb-case) | QA lead with the data steward |
| Service gates | Each service of the wave answers its readiness probe from its own deployment, and its topic and task queue are reachable | DevOps team with the owning squad |
| Fallback agreed | If a check fails, the case list holds, the data screens stay behind their flags, and the ACE team names the recovery date | Release owner with the product owner |

# 7. First release specifics

| Item | Plan |
|---|---|
| Case list | Built from the ACE account view on the first COMPLETED ALS batch for the business date; reconciled to v_ace_account before it is shown, by rwb-case |
| ACE views | 16 Section A views live on the day; the 14 Section B views and the 12 new ACE columns need RWB-ACE-001 (DL43, due 21 November), read through rwb-source-data only |
| Spreadsheets | Retired team by team under the procedure in section 8; each team keeps a read-only archive |
| Access | Administration roles only; business roles from Epic 2 (DL39), served by rwb-access |
| Documents | Store and OCR live; bulk intake of open-case documents starts, served by rwb-document |
| Services | The nine Wave 1 services go live in the order of section 10.4: P1, P2, P3, P4, P5, P6, P7, P9 and P10 |
| Decisions and rules | Approvals and the central ledger run in rwb-decision; the rule packages of the release are in force from their valid from date |
| Notices | Notices and letters run in rwb-comms; the WIN daily file follows the routes that need it |
| Agent | rwb-agent runs with the rule fallback; no agent answer is used without its recorded rule version |

# 8. Tracker retirement

The 20 Excel and SharePoint trackers, 14 marked LOAD and 6 marked RETIRE in the inventory, are retired in the Wave 1 release, team by team. Six teams own them: TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. None is loaded into the Workbench. RWB-E1-005, RWB-E1-010 and RWB-E1-012 are removed under D-RCV-35, so the Workbench provides no inventory, no load and no retirement screen: the procedure below is run by the teams and recorded in one report.

| Step | What happens | Who |
|---|---|---|
| 1 | The team manager works from the case list for two working days after the last tracker file of the team is signed off | Team manager |
| 2 | The team manager makes each tracker read-only or moves it to the read-only archive, and records the archive location | Team manager |
| 3 | The team manager confirms the retirement of each tracker, with the archive location and the date | Team manager |
| 4 | The data steward records the fields of each tracker that no data product carries, for the later epic that picks them up | Data steward |
| 5 | The Tribe lead reads the six-team report: trackers, retired, outstanding and the confirming manager for each team | Tribe lead |
| 6 | The report is filed with the release checklist on 26 November 2026; a team with an outstanding tracker is named with its tracker codes | Tribe lead with the business lead |

# 9. Open decisions

| Decision | What is needed |
|---|---|
| DL12 | Which legacy systems are kept |
| DL34 | The release window |
| DL43 | Whether the ACE team accepts RWB-ACE-001 and its 21 November date |
| BOT approval (FPG 19/2560 clause 5.5) | Whether the change is significant, and the submission date; needed before the Wave 1 cutover |
| Wave 2, 3 and 4 release dates | Not specified in the source documents (CG-B-DELIVDOC-46-2; ASM-B-DELIVDOC-46-2) |
| Wave to release mapping | Not specified in the source documents (CG-B-DELIVDOC-46-3; ASM-B-DELIVDOC-46-3) |

# 10. Cutover by wave

## 10.1 Wave roster

| Wave | Release | Services | Roles at the cutover | Gate |
|---|---|---|---|---|
| Wave 0 | Not a release; the platform is in place before Wave 1 | Service template and Helm chart, contract libraries, workflow kit, 19 schemas and logins, Kafka topics and ACLs, Temporal 1.30+ | Platform team with the ACE DBA and the ACE platform team | No data gate; the platform items of section 1 must be in place |
| Wave 1 | 30 November 2026 (tentative) | P1 rwb-source-data, P2 rwb-integration, P3 rwb-case, P4 rwb-access, P5 rwb-document, P6 rwb-comms, P7 rwb-decision, P9 rwb-reporting, P10 rwb-agent (9) | Release owner with the ACE team; owning squads; ACE DBA; data steward; QA lead | Section 6 check plus the per-service gates of 10.3 |
| Wave 2 | Not specified in the source documents (CG-B-DELIVDOC-46-2; ASM-B-DELIVDOC-46-2) | P8 rwb-payment, S2 rwb-treatment, S5 rwb-asset, S8 rwb-deviation (4) | Release owner with the ACE team; owning squads; QA lead | Section 6 check plus the per-service gates of 10.3 |
| Wave 3 | Not specified in the source documents (CG-B-DELIVDOC-46-2; ASM-B-DELIVDOC-46-2) | S1 rwb-valuation, S3 rwb-guarantee, S4 rwb-litigation, S6 rwb-debtsale (4) | Release owner with the ACE team; owning squads; QA lead | Section 6 check plus the per-service gates of 10.3 |
| Wave 4 | Not specified in the source documents (CG-B-DELIVDOC-46-2; ASM-B-DELIVDOC-46-2) | S7 rwb-writeoff, S9 rwb-partner (2) | Release owner with the ACE team; owning squads; partner gateway owner | Section 6 check plus the per-service gates of 10.3 |

## 10.2 Cutover steps, every wave

1. Wave gate: the DL34 window is confirmed, the BOT approval is recorded if it is required, the SIT and UAT exits are signed, and every unfinished item has its flag off.

2. Platform pre-check: the schemas and logins of the wave exist on the ACE PostgreSQL server, its topics and ACLs exist on the bank Kafka platform, its task queues exist in namespace rwb-recovery, and each login has its PgBouncer pool and connection cap.

3. Contract pre-check: every service of the wave has its OpenAPI, AsyncAPI and activity-jar contract published with its fake, and every service it calls is live at a published version (one hop, 2 s timeout, circuit breaker per downstream).

4. Data pre-check: the ACE batch readiness check of section 6, run by the ACE team lead, the ACE ingestion owner, the ACE DBA and the data steward.

5. Deploy: the tag of each service of the wave, one service at a time, api then worker. A service that fails its readiness probe stops the sequence; it is fixed or held, and the earlier services of the wave keep their flags off.

6. Flags on: in the order of section 10.4, one service at a time, with its smoke test after each.

7. Smoke test per service: sign-in per role, the service's own screen or contract, one decision recorded, and its event seen on its topic by its consumers.

8. First morning: the ACE batch for the business date, the case list reconciliation, the daily ledger seal and the chain check (JOB-14 at 02:00).

9. Record: the release checklist names each service, its tag, its flag states, its gate results and anything held.

## 10.3 Per-service gates

| Gate | Passes when | Who confirms |
|---|---|---|
| Readiness | The readiness and metrics endpoints answer from the service's own api and worker deployment | DevOps team |
| Contract | Contract tests pass against the published contract and its fake | QA team |
| Boundary | The boundary test passes: no cross-schema reference anywhere in the service, and only rwb_source_data reads the recovery.v_ace_* views | ACE DB team |
| Topic | The service publishes on rwb.<name>.events.v1 with CloudEvents 1.0 and its outbox relay, and its retry topics and .dlt topic exist | Platform team |
| Queue | The worker polls its own task queue rwb-<name> only, and the codec server decrypts its payloads | Platform team |
| Flags | Every flag of the service is named and is off before the deploy | DevOps team |
| Rollback | The previous tag and the previous rule package version are recorded, and the flag switch is rehearsed | Release owner |

## 10.4 Order of cutover inside a wave

The order below is the D-RCV-60 proposal. It follows the connection matrix of Architecture v5 slide 13: a service starts after the services it calls are live or publish a fake, and a service that every other service caches from goes first.

| Wave | Order | Why |
|---|---|---|
| Wave 1 | P4 rwb-access, P1 rwb-source-data, P3 rwb-case, P7 rwb-decision, P5 rwb-document, P6 rwb-comms, P9 rwb-reporting, P2 rwb-integration, P10 rwb-agent | Every service caches permissions from rwb-access; rwb-source-data publishes AceDataReady; rwb-case and rwb-decision carry the case list and the ledger; the shared capabilities follow; the readers come last |
| Wave 2 | S8 rwb-deviation, P8 rwb-payment, S2 rwb-treatment, S5 rwb-asset | The deviation screen is always on; payment and treatment must be live before the routes that post money and book a treatment; asset follows them |
| Wave 3 | S1 rwb-valuation, S3 rwb-guarantee, S4 rwb-litigation, S6 rwb-debtsale | The route decision comes before the routes it proposes; guarantee and litigation reach payment, comms, partner and document, and debt sale reaches payment, document and integration |
| Wave 4 | S7 rwb-writeoff, S9 rwb-partner | Write-off depends on payment and source data; the partner service opens the partner gateway and the buyer files last |

## 10.5 What can hold a wave

| Event | What holds it | Who decides |
|---|---|---|
| ACE batch late | rwb-source-data publishes AceDataLate at 05:30; the case list holds and the features that read no ACE data go ahead behind their flags | Release owner with the data steward |
| A service fails its gate | That service stays at its previous build with its flag off; the rest of the wave proceeds | Release owner |
| BOT approval not given | Wave 1 does not start; the platform work of Wave 0 continues | Programme governance |
| A rule package is refused at load | The version in force keeps running and the wave proceeds on the last good package | Reference data administrator with rwb-decision |
| The ledger does not confirm | The strict-mode steps wait for the acknowledgement: debt transfer, write-off, auction sale and title transfer; the other steps continue | Release owner with the product owner |

# 11. Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 3 | 15 November 2026 | Source version: cutover for one deployable; the source carries no change log and no tool line (CG-B-DELIVDOC-46-11; ASM-B-DELIVDOC-46-11) | Not stated in the source documents |
| 4 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

# 12. Assumptions and gaps

| ID | Position taken or item open |
|---|---|
| CG-B-DELIVDOC-46-1; ASM-B-DELIVDOC-46-1 | The file is version 3 while its metadata table says Version 2; version 3 is read as the current source and version 4 is issued from it, with the Version 2 row kept unchanged in the superseded file |
| CG-B-DELIVDOC-46-2; ASM-B-DELIVDOC-46-2 | Only the first release, 30 November 2026, is named; the Wave 2, 3 and 4 dates are open and carry the placeholder of section 9 |
| CG-B-DELIVDOC-46-3; ASM-B-DELIVDOC-46-3 | One wave goes live per release and a release carries only its own services; the earlier waves stay live |
| CG-B-DELIVDOC-46-4; ASM-B-DELIVDOC-46-4 | The first-release capabilities are delivered by the nine Wave 1 services named in section 7 and section 10.1 |
| CG-B-DELIVDOC-46-5; ASM-B-DELIVDOC-46-5 | The rollback is per service, with its flags, its previous tag, Worker Versioning for in-flight cases and a one-call rule package rollback |
| CG-B-DELIVDOC-46-6; ASM-B-DELIVDOC-46-6 | BOT approval under FPG 19/2560 clause 5.5 is treated as required before the Wave 1 cutover, with the date open |
| CG-B-DELIVDOC-46-7; ASM-B-DELIVDOC-46-7 | The sentence that the release reads the 30 views is read as rwb-source-data reading them for the Workbench, and the rwb_source_data login replaces the recovery role of the source |
| CG-B-DELIVDOC-46-8; ASM-B-DELIVDOC-46-8 | The wave is deployed into the existing ACE AKS cluster and namespace rwb-recovery, one api and one worker per service, with no new capacity plan assumed |
| CG-B-DELIVDOC-46-9; ASM-B-DELIVDOC-46-9 | The tracker retirement stays a team procedure run by the six team managers against the Wave 1 case list; no service is named as the tracker owner |
| CG-B-DELIVDOC-46-10; ASM-B-DELIVDOC-46-10 | Version 4 is issued as Draft with no recorded approval |
| CG-B-DELIVDOC-46-11; ASM-B-DELIVDOC-46-11 | The change log starts at version 3 as the source row, and the version 3 date of 15 November 2026 is kept |
