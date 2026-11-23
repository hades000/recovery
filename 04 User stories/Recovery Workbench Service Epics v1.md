SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench Service Epics v1

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Source (read-only): `04 User stories/Recovery Workbench Service Story Catalog v1.xlsx` (Epics and Stories sheets), `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx` (Services and Workflows and activities sheets), `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 14-20) and `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` §R1, §R3, §R5, §R8 and §R9.

## Change log

| Version | Date | Decision | Tool | Change |
|---|---|---|---|---|
| v1 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash | First issue of the Service Epics file: the 31 epics with scope, wave, suggested owner, lanes and Day-1 stories, taken from the Service Story Catalog v1 and the Microservice Ownership Map v1. |

## 1. What this file is

One block and one summary row for each of the 31 epics of the realignment: 19 service epics, 7 platform epics and 5 integration epics (`RWB-SVC-P1`…`RWB-SVC-S9`, `RWB-PLT-TPL`…`RWB-PLT-OBS`, `RWB-ITG-W1`…`RWB-ITG-NFR`; Template and Rules §R5.1 and user decision U1). Every story also carries its business epic (EP01–EP08) as a tag, so the service view and the business view of the same backlog stay in step.

The numbers are the Service Story Catalog v1 numbers: stories, lanes and Day-1 stories per epic, and the wave. This file adds the two values the catalog stores nowhere at epic level — the scope of the epic and its suggested owner — using the epic ID pattern of §R5.2, the Microservice Ownership Map v1 and the fixed owner phrases of Template and Rules §R5.3. No story is changed here: the story files are the record, and this file is the overview.

No conflict on the R-PREC list (§R3) had to be resolved in this file. The three values that had to be derived are stated in §10 with their gap and assumption rows (Template and Rules §R9).

The Epics sheet of the catalog is reproduced here in full, with the scope and the suggested owner added. The Stories, Legacy map, Dependencies and Contracts sheets stay in the catalog: they are the source of the story files and of the Day-1 Work Allocation v1.

**How to read it.**

- **Scope.** `PLT` is a platform epic, `ITG` an integration epic, `P1`–`P10` a platform service and `S1`–`S9` a route service (naming pattern of §R5.2).
- **Epic wave.** The wave at which the epic starts: the earliest wave carried by its stories. A story keeps its W-MAP wave when that is earlier than its service's Arch v5 wave (§R5.6), so for a service epic the Arch v5 service wave from the Ownership Map is shown next to the epic wave where the two differ.
- **Suggested owner.** A suggestion only; any team may pick up any story (U3). The owner of an epic is the §R5.3 owner phrase that most of its stories carry (so the harness and NFR stories of `RWB-ITG-NFR` make QA team the owner of that epic), and the full fixed phrase is written in each block. The summary table uses the short team name.
- **Lanes.** A lane is a connected group of non-CON stories linked by H dependencies; its depth is at most 4 (§R5.7 rule 5). A contract story is always Day 1 and sits in contract group `CG-W<wave>`, so a contract group is shared by every epic of its wave.
- **Day-1 stories.** The count of stories whose Ready to start is "Day 1": contract stories, and stories whose only build dependencies are contract stories (§R5.7 rules 1 and 8).
- **Releases.** Every date is copied unchanged and marked (tentative). A story that carries no legacy date is counted as "None (new story)", the wording the story files use.

## 2. The 31 epics

| Epic | Scope | Name | Epic wave | Arch v5 wave | Suggested owner | Stories | Lanes | Day-1 stories |
|---|---|---|---|---|---|---|---|---|
| RWB-PLT-TPL | PLT | Service template and repositories | 0 | 0 (platform) | TechX | 19 | 19 | 19 |
| RWB-PLT-LIB | PLT | Shared libraries | 0 | 0 (platform) | TechX | 18 | 11 | 18 |
| RWB-PLT-WF | PLT | Temporal workflow platform | 0 | 0 (platform) | TechX | 16 | 10 | 16 |
| RWB-PLT-DB | PLT | ACE DB schemas and logins | 0 | 0 (platform) | ACE team | 2 | 2 | 2 |
| RWB-PLT-EVT | PLT | Kafka event platform | 0 | 0 (platform) | SCB IT infrastructure | 3 | 3 | 3 |
| RWB-PLT-EDGE | PLT | Edge and gateway | 0 | 0 (platform) | SCB IT infrastructure | 5 | 5 | 5 |
| RWB-PLT-OBS | PLT | Observability | 0 | 0 (platform) | DevOps team | 2 | 2 | 2 |
| RWB-SVC-P1 | P1 | rwb-source-data (Source data) | 1 | 1 | TechX | 62 | 28 | 37 |
| RWB-SVC-P2 | P2 | rwb-integration (Integration) | 1 | 1 | TechX | 27 | 14 | 20 |
| RWB-SVC-P3 | P3 | rwb-case (Case and workflow) | 1 | 1 | TechX | 84 | 50 | 71 |
| RWB-SVC-P4 | P4 | rwb-access (Access and authority) | 1 | 1 | TechX | 111 | 68 | 99 |
| RWB-SVC-P5 | P5 | rwb-document (Document) | 1 | 1 | TechX | 52 | 29 | 38 |
| RWB-SVC-P6 | P6 | rwb-comms (Communications) | 1 | 1 | TechX | 48 | 31 | 41 |
| RWB-SVC-P7 | P7 | rwb-decision (Decision and rules) | 1 | 1 | TechX | 52 | 46 | 49 |
| RWB-SVC-P8 | P8 | rwb-payment (Payment) | 1 | 2 | TechX | 21 | 16 | 20 |
| RWB-SVC-P9 | P9 | rwb-reporting (Reporting) | 1 | 1 | TechX | 12 | 9 | 11 |
| RWB-SVC-P10 | P10 | rwb-agent (Agent) | 1 | 1 | TechX | 40 | 16 | 28 |
| RWB-SVC-S1 | S1 | rwb-valuation (Valuation and route) | 3 | 3 | TechX | 24 | 13 | 24 |
| RWB-SVC-S2 | S2 | rwb-treatment (Treatment and offer) | 2 | 2 | TechX | 47 | 30 | 47 |
| RWB-SVC-S3 | S3 | rwb-guarantee (Guarantee) | 2 | 3 | TechX | 17 | 10 | 17 |
| RWB-SVC-S4 | S4 | rwb-litigation (Litigation) | 2 | 3 | TechX | 45 | 24 | 45 |
| RWB-SVC-S5 | S5 | rwb-asset (Asset) | 1 | 2 | TechX | 51 | 28 | 51 |
| RWB-SVC-S6 | S6 | rwb-debtsale (Debt sale) | 3 | 3 | TechX | 30 | 18 | 30 |
| RWB-SVC-S7 | S7 | rwb-writeoff (Write-off) | 4 | 4 | TechX | 32 | 17 | 32 |
| RWB-SVC-S8 | S8 | rwb-deviation (Deviation) | 1 | 2 | TechX | 31 | 22 | 31 |
| RWB-SVC-S9 | S9 | rwb-partner (Partner) | 1 | 4 | TechX | 36 | 21 | 36 |
| RWB-ITG-W1 | ITG | Wave 1 integration | 1 | — | TechX | 52 | 1 | 52 |
| RWB-ITG-W2 | ITG | Wave 2 integration | 2 | — | TechX | 43 | 1 | 43 |
| RWB-ITG-W3 | ITG | Wave 3 integration | 3 | — | TechX | 9 | 1 | 9 |
| RWB-ITG-W4 | ITG | Wave 4 integration | 4 | — | TechX | 41 | 1 | 41 |
| RWB-ITG-NFR | ITG | Non-functional integration | 1 | — | QA team | 2 | 1 | 2 |

Totals: 31 epics · 1034 stories · 939 Day-1 stories · 547 epic-lane memberships (510 distinct lane IDs; a contract group is counted once per epic, see §8).

## 3. Platform epics (7, wave 0)

The platform epics carry the work every service needs before its own code starts: the service template, the shared libraries, the Temporal layer, the ACE schemas and logins, the Kafka and event platform, the edge and the observability baseline (§R5.1, §R4). They are wave 0: a platform contract story H dependency is what lets a service lane start on Day 1 (§R5.7 rules 1–3).

### RWB-PLT-TPL — Service template and repositories

| Item | Value |
|---|---|
| Epic | RWB-PLT-TPL |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 12 of 19 stories carry this suggestion; work-type mix: Contract 1 · App development 11 · DevOps 7 (§R5.3) |
| Owner mix of the stories | TechX 12 · DevOps team 7 |
| Stories | 19 |
| Lanes | 19 (contract groups: CG-W0) |
| Day-1 stories | 19 |
| Business-epic tags | EP01, EP01-TE, NEW, NF |
| Releases | 30 November 2026 (tentative) — 14 · None (new story) — 5 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-E1044-CON` Database migrations versioned with parameterized schema names (DP-15) |
| Rule references | §R5.1 (service template and repositories); §R4 (schema, login, REST base, topic and epic naming per service); DP-15 (per-service Flyway sequence, H `RWB-PLT-E1044-CON`) |

### RWB-PLT-LIB — Shared libraries

| Item | Value |
|---|---|
| Epic | RWB-PLT-LIB |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 17 of 18 stories carry this suggestion; work-type mix: Contract 8 · App development 9 · DevOps 1 (§R5.3) |
| Owner mix of the stories | TechX 17 · DevOps team 1 |
| Stories | 18 |
| Lanes | 11 (contract groups: CG-W0) |
| Day-1 stories | 18 |
| Business-epic tags | EP01, EP01-TE, NEW, NF |
| Releases | 30 November 2026 (tentative) — 15 · None (new story) — 3 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-E1027-CON` Decision log writer v1 (DP-03) · `RWB-PLT-E1072-CON` Drools runtime and rule package store (DP-04) · `RWB-PLT-E1042-CON` Central configuration service and parameter catalog (DP-06) · `RWB-PLT-E1043-CON` Reference data service with versioned tables (DP-07) · `RWB-PLT-E1037-CON` Role to permission matrix as data and PDPA field masking by role (DP-08) · `RWB-PLT-TE006-CON` Outbox and retry for outbound work (DP-09) · `RWB-PLT-E1047-CON` Feature flags for module release with a removal date (DP-14) · `RWB-PLT-N009-CON` RFC 9457 problem and Idempotency-Key helpers - interface and fake |
| Rule references | §R5.1 (shared libraries); DP-03 (decision record), DP-04 (embedded Drools), DP-06 (parameters), DP-07 (reference data), DP-08 (authorise guard), DP-09 (outbox and inbox), DP-14 (topic naming library) |

### RWB-PLT-WF — Temporal workflow platform

| Item | Value |
|---|---|
| Epic | RWB-PLT-WF |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 14 of 16 stories carry this suggestion; work-type mix: Contract 7 · App development 7 · Infrastructure 2 (§R5.3) |
| Owner mix of the stories | TechX 14 · SCB IT infrastructure 2 |
| Stories | 16 |
| Lanes | 10 (contract groups: CG-W0) |
| Day-1 stories | 16 |
| Business-epic tags | EP01, EP02, NEW, NF |
| Releases | 30 November 2026 (tentative) — 4 · 31 December 2026 (tentative) — 8 · None (new story) — 4 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-E1071-CON` Temporal worker and SDK in the recovery module (DP-10) · `RWB-PLT-N010-CON` Workflow kit templates - interface and fake |
| Rule references | §R5.1 (Temporal workflow platform); §R4 (Temporal namespace `rwb-recovery`, task queue `rwb-<short>`); DP-10 (Quartz replacement, H `RWB-PLT-E1071-CON`); DP-12 (parent and child workflows) |

### RWB-PLT-DB — ACE DB schemas and logins

| Item | Value |
|---|---|
| Epic | RWB-PLT-DB |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | ACE team (suggested; any team may pick up this story) |
| Owner basis | ACE team 2 of 2 stories carry this suggestion; work-type mix: ACE DB 2 (§R5.3) |
| Owner mix of the stories | ACE team 2 |
| Stories | 2 |
| Lanes | 2 (no contract group) |
| Day-1 stories | 2 |
| Business-epic tags | NEW, NF |
| Releases | None (new story) — 2 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-NF06-DB` Create the 19 rwb_* schemas and logins · `RWB-PLT-N011-DB` PgBouncer pools, migrator role and grant check |
| Rule references | §R5.1 (ACE DB schemas and logins); §R4 (schema `rwb_<short with _>`, login per service); DP-01, DP-02 (own schema, own login); DP-15 (migration ownership) |

### RWB-PLT-EVT — Kafka event platform

| Item | Value |
|---|---|
| Epic | RWB-PLT-EVT |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Owner basis | SCB IT infrastructure 3 of 3 stories carry this suggestion; work-type mix: Infrastructure 3 (§R5.3) |
| Owner mix of the stories | SCB IT infrastructure 3 |
| Stories | 3 |
| Lanes | 3 (no contract group) |
| Day-1 stories | 3 |
| Business-epic tags | NEW |
| Releases | None (new story) — 3 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-N002-INF` Kafka topics, retry and dead-letter topics and ACLs · `RWB-PLT-N008-INF` Schema registry with BACKWARD compatibility · `RWB-PLT-N012-INF` Blob, Key Vault and MFT/SFTP standard resources |
| Rule references | §R5.1 (Kafka event platform); §R4 (topic `rwb.<short>.events.v1` with retry and `.dlt`, shared topic `rwb.decision-record.v1`); DP-09 (outbox and inbox, CloudEvents) |

### RWB-PLT-EDGE — Edge and gateway

| Item | Value |
|---|---|
| Epic | RWB-PLT-EDGE |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | SCB IT infrastructure (suggested; any team may pick up this story) |
| Owner basis | SCB IT infrastructure 3 of 5 stories carry this suggestion; work-type mix: Contract 1 · App development 1 · Infrastructure 3 (§R5.3) |
| Owner mix of the stories | TechX 2 · SCB IT infrastructure 3 |
| Stories | 5 |
| Lanes | 5 (contract groups: CG-W0) |
| Day-1 stories | 5 |
| Business-epic tags | NEW, NF |
| Releases | None (new story) — 5 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-N001-CON` gateway-bff route contract (DP-19) · `RWB-PLT-N001-APP` gateway-bff routes and composite screens · `RWB-PLT-N006-INF` Redis session store for gateway-bff · `RWB-PLT-N007-INF` Partner gateway in the DMZ (FAPI 2.0) |
| Rule references | §R5.1 (edge and gateway); §R4 (gateway-bff with the Redis session store, partner gateway in the DMZ); DP-13 (REST base), DP-19 (composite route, H `RWB-PLT-N001-CON`) |

### RWB-PLT-OBS — Observability

| Item | Value |
|---|---|
| Epic | RWB-PLT-OBS |
| Scope | PLT |
| Service | platform |
| Epic wave | 0 |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Owner basis | DevOps team 2 of 2 stories carry this suggestion; work-type mix: DevOps 2 (§R5.3) |
| Owner mix of the stories | DevOps team 2 |
| Stories | 2 |
| Lanes | 2 (no contract group) |
| Day-1 stories | 2 |
| Business-epic tags | EP01, NEW |
| Releases | 30 November 2026 (tentative) — 1 · None (new story) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-PLT-N005-OPS` Platform dashboards and alerts baseline · `RWB-PLT-E1056-OPS` Run books and monitoring for every Epic 1 Workbench job |
| Rule references | §R5.1 (observability); ADR-023 (observability per service), allocated in §R8.4 |

## 4. Service epics (19)

One epic per service, in service code order (§R4, U1). Each epic owns its schema, its login, its REST base, its topic and its Temporal task queue, and it may read another service's data only through that service's contract or through its own `v_ace_*` views (DP-01, DP-02, DP-05, §R7.2 s17).

The table, operation and event counts of a block are the counts of the Ownership Map (its machine form `_work/msr/plan/ownership.json`). Where a count is 0 the map assigns none to that service; the named lists and the rulings behind them are in the map and its Rulings sheet.

### RWB-SVC-P1 — rwb-source-data (Source data)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P1 |
| Scope | P1 |
| Service | `rwb-source-data` (Source data) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 49 of 62 stories carry this suggestion; work-type mix: Contract 11 · App development 38 · ACE DB 4 · DevOps 9 (§R5.3) |
| Owner mix of the stories | TechX 49 · ACE team 4 · DevOps team 9 |
| Stories | 62 |
| Lanes | 28 (contract groups: CG-W1, CG-W2, CG-W4) |
| Day-1 stories | 37 |
| Business-epic tags | EP01, EP02, EP08 |
| Releases | 30 November 2026 (tentative) — 41 · 31 December 2026 (tentative) — 16 · 30 June 2027 (tentative) — 5 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md` |
| Schema | `rwb_source_data` |
| REST base | `/api/recovery/source-data/v1` |
| Topic | `rwb.source-data.events.v1` |
| Temporal task queue | `rwb-source-data` |
| Workflows owned | None in the Ownership Map |
| Tables in the Ownership Map | 18 |
| REST operations in the Ownership Map | 18 |
| Events published in the Ownership Map | 2 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /customers/{id}, /accounts/{id}; GET /collateral/{id}, /payments?accountId=; GET /freshness (business date); POST /business-days/{date}/ready (Airflow) ; events (none: Airflow call; fallback polls ACE batch record) ; Temporal Act: listEligibleAccounts, snapshot(page); Workflow: AceIngestCheck, reconciliation
- Out: schema rwb_source_data (ACE view contract, extension tables, freshness, reconciliation) ; topic rwb.source-data.events.v1: AceDataReady, AceDataLate (05:30) ; SQL ACE DB views: SELECT recovery.v_ace_* (30 views)

### RWB-SVC-P2 — rwb-integration (Integration)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P2 |
| Scope | P2 |
| Service | `rwb-integration` (Integration) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 20 of 27 stories carry this suggestion; work-type mix: Contract 8 · App development 12 · Infrastructure 1 · DevOps 6 (§R5.3) |
| Owner mix of the stories | TechX 20 · SCB IT infrastructure 1 · DevOps team 6 |
| Stories | 27 |
| Lanes | 14 (contract groups: CG-W1, CG-W2) |
| Day-1 stories | 20 |
| Business-epic tags | EP01, EP02, EP04 |
| Releases | 30 November 2026 (tentative) — 5 · 31 December 2026 (tentative) — 21 · 28 February 2027 (tentative) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P2 rwb-integration v1.md` |
| Schema | `rwb_integration` |
| REST base | `/api/recovery/integration/v1` |
| Topic | `rwb.integration.events.v1` |
| Temporal task queue | `rwb-integration` |
| Workflows owned | None in the Ownership Map |
| Tables in the Ownership Map | 3 |
| REST operations in the Ownership Map | 11 |
| Events published in the Ownership Map | 0 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /interface-runs (operations); POST /interface-runs/{id}/retry ; events (none: called as a task) ; Temporal Act: deliverFile(manifest), receiveFile; Airflow window: WIN file 16:00, buyer files per lot
- Out: schema rwb_integration (interface config, file runs, outbound items, ACE integration paths) ; topic rwb.integration.events.v1: FileDelivered, FileFailed ; REST Document: fetch file by ID (SAS link) ; FILE WIN (registered mail): daily outbound file (INT-14) · Debt buyers: per lot, encrypted (INT-25)

### RWB-SVC-P3 — rwb-case (Case and workflow)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P3 |
| Scope | P3 |
| Service | `rwb-case` (Case and workflow) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 71 of 84 stories carry this suggestion; work-type mix: Contract 20 · App development 51 · ACE DB 1 · Infrastructure 2 · DevOps 10 (§R5.3) |
| Owner mix of the stories | TechX 71 · ACE team 1 · SCB IT infrastructure 2 · DevOps team 10 |
| Stories | 84 |
| Lanes | 50 (contract groups: CG-W1, CG-W2) |
| Day-1 stories | 71 |
| Business-epic tags | EP01, EP02, EP03, EP05, EP06, EP08 |
| Releases | 30 November 2026 (tentative) — 44 · 31 December 2026 (tentative) — 35 · 31 January 2027 (tentative) — 1 · 31 March 2027 (tentative) — 1 · 30 April 2027 (tentative) — 2 · 30 June 2027 (tentative) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P3 rwb-case v1.md` |
| Schema | `rwb_case` |
| REST base | `/api/recovery/case/v1` |
| Topic | `rwb.case.events.v1` |
| Temporal task queue | `rwb-case` |
| Workflows owned | CaseWorkflow |
| Tables in the Ownership Map | 15 |
| REST operations in the Ownership Map | 22 |
| Events published in the Ownership Map | 7 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /cases/{id}, /cases?queue=; POST /cases/{id}/actions; GET /tasks · POST /tasks/{id}/complete; GET /case-summary/{id} (for ACE shared case view) ; events RouteDecided; DeviationRaised / Cleared; PaymentMissed, TreatmentBooked, ProceedsMatched; LotAwarded, AssetTakenOn, WriteOffApproved; AceDataReady, RulePackageInForce ; Temporal CaseWorkflow (parent, one per case); DailyCaseRun (Schedule + AceDataReady); Act: allocate, transfer, rebalance
- Out: schema rwb_case (case, CMMN state, queues, tasks, allocation, timers) ; topic rwb.case.events.v1: CaseCreated, CaseAllocated, CaseAllocationFailed, CaseTransferred, CaseStateChanged, TimerBreached ; TMP Source data: listEligibleAccounts(businessDate) · Valuation: child: RouteDecisionWorkflow · Treatment: child: stage workflows · Litigation, Asset, Debt sale, Write-off, Guarantee: child · Deviation: child: DeviationWorkflow ; REST Access: authorise (cached)

### RWB-SVC-P4 — rwb-access (Access and authority)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P4 |
| Scope | P4 |
| Service | `rwb-access` (Access and authority) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 106 of 111 stories carry this suggestion; work-type mix: Contract 34 · App development 72 · ACE DB 3 · Infrastructure 1 · DevOps 1 (§R5.3) |
| Owner mix of the stories | TechX 106 · ACE team 3 · SCB IT infrastructure 1 · DevOps team 1 |
| Stories | 111 |
| Lanes | 68 (contract groups: CG-W1, CG-W2, CG-W4) |
| Day-1 stories | 99 |
| Business-epic tags | EP01, EP02, EP08 |
| Releases | 30 November 2026 (tentative) — 26 · 31 December 2026 (tentative) — 24 · 30 June 2027 (tentative) — 61 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md` |
| Schema | `rwb_access` |
| REST base | `/api/recovery/access/v1` |
| Topic | `rwb.access.events.v1` |
| Temporal task queue | `rwb-access` |
| Workflows owned | None in the Ownership Map |
| Tables in the Ownership Map | 5 |
| REST operations in the Ownership Map | 4 |
| Events published in the Ownership Map | 0 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST POST /authorise (role, scope, DoA); GET /me/permissions; GET /doa-limits · /masking-policies ; events (none: reference data owner) ; Temporal Schedule: access review list (six-monthly)
- Out: schema rwb_access (Recovery roles as data, scope, masking policy, DoA table, access log) ; topic rwb.access.events.v1: AccessPolicyChanged, DoaLimitChanged ; REST ACE Common: sign-in, group-to-role (Entra)

### RWB-SVC-P5 — rwb-document (Document)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P5 |
| Scope | P5 |
| Service | `rwb-document` (Document) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 44 of 52 stories carry this suggestion; work-type mix: Contract 12 · App development 32 · Infrastructure 3 · DevOps 5 (§R5.3) |
| Owner mix of the stories | TechX 44 · SCB IT infrastructure 3 · DevOps team 5 |
| Stories | 52 |
| Lanes | 29 (contract groups: CG-W1, CG-W2, CG-W4) |
| Day-1 stories | 38 |
| Business-epic tags | EP01, EP02, EP03, EP08 |
| Releases | 30 November 2026 (tentative) — 38 · 31 December 2026 (tentative) — 11 · 31 January 2027 (tentative) — 1 · 30 June 2027 (tentative) — 2 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P5 rwb-document v1.md` |
| Schema | `rwb_document` |
| REST base | `/api/recovery/document/v1` |
| Topic | `rwb.document.events.v1` |
| Temporal task queue | `rwb-document` |
| Workflows owned | DocumentIntakeWorkflow |
| Tables in the Ownership Map | 12 |
| REST operations in the Ownership Map | 17 |
| Events published in the Ownership Map | 2 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST POST /documents (returns upload link); GET /documents/{id}, /cases/{id}/documents; POST /documents/generate ; events AgentRunCompleted (classification) ; Temporal DocumentIntakeWorkflow: OCR, classify, extract; Act: generate, seal · Schedule: retention
- Out: schema rwb_document (metadata, custody, OCR text and fields, signatures, retention) ; topic rwb.document.events.v1: DocumentStored, DocumentFieldsExtracted ; TMP Agent: child: classify / extract run ; FILE Azure Blob (WORM): files, 2.8 TB by 2031

### RWB-SVC-P6 — rwb-comms (Communications)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P6 |
| Scope | P6 |
| Service | `rwb-comms` (Communications) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 43 of 48 stories carry this suggestion; work-type mix: Contract 14 · App development 29 · Infrastructure 1 · DevOps 4 (§R5.3) |
| Owner mix of the stories | TechX 43 · SCB IT infrastructure 1 · DevOps team 4 |
| Stories | 48 |
| Lanes | 31 (contract groups: CG-W1, CG-W2, CG-W3, CG-W4) |
| Day-1 stories | 41 |
| Business-epic tags | EP01, EP02, EP04, EP05, EP08 |
| Releases | 30 November 2026 (tentative) — 16 · 31 December 2026 (tentative) — 13 · 28 February 2027 (tentative) — 16 · 31 March 2027 (tentative) — 1 · 30 June 2027 (tentative) — 2 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md` |
| Schema | `rwb_comms` |
| REST base | `/api/recovery/comms/v1` |
| Topic | `rwb.comms.events.v1` |
| Temporal task queue | `rwb-comms` |
| Workflows owned | NoticeDispatchWorkflow |
| Tables in the Ownership Map | 3 |
| REST operations in the Ownership Map | 11 |
| Events published in the Ownership Map | 3 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST POST /notices (request); GET /cases/{id}/notices ; events DeviationRaised / Cleared (contact stop); TreatmentApproved, PaymentMissed; CaseStateChanged ; Temporal NoticeDispatchWorkflow (kit template)
- Out: schema rwb_comms (notices, templates, merge fields, proof of delivery) ; topic rwb.comms.events.v1: NoticeGenerated, NoticeDispatched, NoticeDelivered ; TMP Document: generate letter · Decision: child: approval · Integration: deliverFile (WIN letters) ; REST ACE Common: notification path (SMS, LINE)

### RWB-SVC-P7 — rwb-decision (Decision and rules)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P7 |
| Scope | P7 |
| Service | `rwb-decision` (Decision and rules) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 48 of 52 stories carry this suggestion; work-type mix: Contract 5 · App development 43 · ACE DB 1 · DevOps 3 (§R5.3) |
| Owner mix of the stories | TechX 48 · ACE team 1 · DevOps team 3 |
| Stories | 52 |
| Lanes | 46 (contract groups: CG-W1, CG-W2) |
| Day-1 stories | 49 |
| Business-epic tags | EP01, EP01-TE, EP02, EP03, EP06 |
| Releases | 30 November 2026 (tentative) — 20 · 31 December 2026 (tentative) — 29 · 31 January 2027 (tentative) — 2 · 30 April 2027 (tentative) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md` |
| Schema | `rwb_decision` |
| REST base | `/api/recovery/decision/v1` |
| Topic | `rwb.decision.events.v1` |
| Temporal task queue | `rwb-decision` |
| Workflows owned | ApprovalWorkflow |
| Tables in the Ownership Map | 6 |
| REST operations in the Ownership Map | 19 |
| Events published in the Ownership Map | 3 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /decisions?caseId=; POST /approvals/{id}/decide; POST /rule-models · GET /rule-models/{n}/{v} ; events DecisionRecorded (from all 19); NoticeGenerated (approval); AgentRunCompleted ; Temporal ApprovalWorkflow (kit template); Schedules: rule promote 00:01, chain check 02:00
- Out: schema rwb_decision (approvals, central decision ledger, DMN model registry) ; topic rwb.decision.events.v1: ApprovalRequested, ApprovalDecided, RulePackageInForce ; REST Access: DoA limits ; FILE Immutable storage: daily ledger seal (WORM)

### RWB-SVC-P8 — rwb-payment (Payment)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P8 |
| Scope | P8 |
| Service | `rwb-payment` (Payment) |
| Epic wave | 1 |
| Arch v5 service wave | 2 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 19 of 21 stories carry this suggestion; work-type mix: Contract 6 · App development 13 · DevOps 2 (§R5.3) |
| Owner mix of the stories | TechX 19 · DevOps team 2 |
| Stories | 21 |
| Lanes | 16 (contract groups: CG-W2, CG-W3) |
| Day-1 stories | 20 |
| Business-epic tags | EP01, EP02, EP04, EP06, EP08 |
| Releases | 30 November 2026 (tentative) — 1 · 31 December 2026 (tentative) — 7 · 28 February 2027 (tentative) — 12 · 30 April 2027 (tentative) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P8 rwb-payment v1.md` |
| Schema | `rwb_payment` |
| REST base | `/api/recovery/payment/v1` |
| Topic | `rwb.payment.events.v1` |
| Temporal task queue | `rwb-payment` |
| Workflows owned | None in the Ownership Map |
| Tables in the Ownership Map | 1 |
| REST operations in the Ownership Map | 2 |
| Events published in the Ownership Map | 3 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /cases/{id}/payments; POST /proceeds/{id}/allocate (manual) ; events AceDataReady; TreatmentApproved, LotAwarded; AssetSold, WriteOffApproved ; Temporal Act: matchPayments, confirmBookings; Act: postProceeds (saga step)
- Out: schema rwb_payment (payment and proceeds matching, fees, bookings, posting files) ; topic rwb.payment.events.v1: TreatmentBooked, PaymentMissed, ProceedsMatched ; TMP Source data: payments for business date · Integration: deliverFile (posting file)

### RWB-SVC-P9 — rwb-reporting (Reporting)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P9 |
| Scope | P9 |
| Service | `rwb-reporting` (Reporting) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 10 of 12 stories carry this suggestion; work-type mix: Contract 5 · App development 5 · DevOps 2 (§R5.3) |
| Owner mix of the stories | TechX 10 · DevOps team 2 |
| Stories | 12 |
| Lanes | 9 (contract groups: CG-W1, CG-W2, CG-W4) |
| Day-1 stories | 11 |
| Business-epic tags | EP01, EP02, EP06, EP08 |
| Releases | 30 November 2026 (tentative) — 3 · 31 December 2026 (tentative) — 3 · 30 April 2027 (tentative) — 2 · 30 June 2027 (tentative) — 4 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md` |
| Schema | `rwb_reporting` |
| REST base | `/api/recovery/reporting/v1` |
| Topic | `rwb.reporting.events.v1` |
| Temporal task queue | `rwb-reporting` |
| Workflows owned | None in the Ownership Map |
| Tables in the Ownership Map | 3 |
| REST operations in the Ownership Map | 1 |
| Events published in the Ownership Map | 0 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /dashboards/{id}; GET /reports/{id} · POST /reports/{id}/run (Airflow) ; events All business events (projections); DecisionRecorded ; Temporal Schedule: measures 01:30; Act: buildRegulatoryExtract
- Out: schema rwb_reporting (measures, snapshots, steering dashboard, regulatory reports) ; topic rwb.reporting.events.v1: ReportPublished ; TMP Source data: snapshot(page) for measures · Integration: deliverFile (regulatory extract)

### RWB-SVC-P10 — rwb-agent (Agent)

| Item | Value |
|---|---|
| Epic | RWB-SVC-P10 |
| Scope | P10 |
| Service | `rwb-agent` (Agent) |
| Epic wave | 1 |
| Arch v5 service wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 33 of 40 stories carry this suggestion; work-type mix: Contract 15 · App development 18 · Infrastructure 2 · DevOps 5 (§R5.3) |
| Owner mix of the stories | TechX 33 · SCB IT infrastructure 2 · DevOps team 5 |
| Stories | 40 |
| Lanes | 16 (contract groups: CG-W1, CG-W2, CG-W4) |
| Day-1 stories | 28 |
| Business-epic tags | EP01, EP01-TE, EP02, EP03, EP08 |
| Releases | 30 November 2026 (tentative) — 17 · 31 December 2026 (tentative) — 6 · 31 January 2027 (tentative) — 10 · 30 June 2027 (tentative) — 7 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md` |
| Schema | `rwb_agent` |
| REST base | `/api/recovery/agent/v1` |
| Topic | `rwb.agent.events.v1` |
| Temporal task queue | `rwb-agent` |
| Workflows owned | AgentRunWorkflow |
| Tables in the Ownership Map | 8 |
| REST operations in the Ownership Map | 11 |
| Events published in the Ownership Map | 1 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /agent-runs/{id}; GET/POST /agent-policies (admin) ; events DocumentStored (intake); CaseCreated (screening) ; Temporal AgentRunWorkflow: 60 s, then rule result; Tool gateway: read-only calls for the agent
- Out: schema rwb_agent (agent policies, prompts, runs, guardrails, evaluations) ; topic rwb.agent.events.v1: AgentRunCompleted ; REST Source data: tool: read case facts · Document: tool: read extracted fields · Enterprise AI endpoint: HTTPS private endpoint

### RWB-SVC-S1 — rwb-valuation (Valuation and route)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S1 |
| Scope | S1 |
| Service | `rwb-valuation` (Valuation and route) |
| Epic wave | 3 |
| Arch v5 service wave | 3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 24 of 24 stories carry this suggestion; work-type mix: Contract 12 · App development 12 (§R5.3) |
| Owner mix of the stories | TechX 24 |
| Stories | 24 |
| Lanes | 13 (contract groups: CG-W3) |
| Day-1 stories | 24 |
| Business-epic tags | EP04 |
| Releases | 28 February 2027 (tentative) — 24 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md` |
| Schema | `rwb_valuation` |
| REST base | `/api/recovery/valuation/v1` |
| Topic | `rwb.valuation.events.v1` |
| Temporal task queue | `rwb-valuation` |
| Workflows owned | RouteDecisionWorkflow |
| Tables in the Ownership Map | 0 |
| REST operations in the Ownership Map | 3 |
| Events published in the Ownership Map | 0 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET /cases/{id}/valuation; POST /cases/{id}/route-proposals ; events RulePackageInForce ; Temporal RouteDecisionWorkflow (child of case)
- Out: schema rwb_valuation (valuations, D6 route decision, route agent output) ; topic rwb.valuation.events.v1: RouteDecided ; TMP Agent: child: route agent · Decision: child: approval ; REST Source data: collateral, appraisals

### RWB-SVC-S2 — rwb-treatment (Treatment and offer)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S2 |
| Scope | S2 |
| Service | `rwb-treatment` (Treatment and offer) |
| Epic wave | 2 |
| Arch v5 service wave | 2 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 47 of 47 stories carry this suggestion; work-type mix: Contract 18 · App development 29 (§R5.3) |
| Owner mix of the stories | TechX 47 |
| Stories | 47 |
| Lanes | 30 (contract groups: CG-W2) |
| Day-1 stories | 47 |
| Business-epic tags | EP02, EP03 |
| Releases | 31 December 2026 (tentative) — 11 · 31 January 2027 (tentative) — 36 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md` |
| Schema | `rwb_treatment` |
| REST base | `/api/recovery/treatment/v1` |
| Topic | `rwb.treatment.events.v1` |
| Temporal task queue | `rwb-treatment` |
| Workflows owned | TreatmentWorkflow |
| Tables in the Ownership Map | 1 |
| REST operations in the Ownership Map | 4 |
| Events published in the Ownership Map | 1 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /treatments; POST /treatments/{id}/offer ; events TreatmentBooked, PaymentMissed; DeviationRaised ; Temporal TreatmentWorkflow · settlement and DIL sagas
- Out: schema rwb_treatment (treatments, contracts, settlement and deed-in-lieu agreements, plan timers) ; topic rwb.treatment.events.v1: TreatmentApproved, TreatmentClosed ; TMP Decision: child: approval · Document: contract, e-sign · Payment: postProceeds ; NEXUS ACE Common: restructure calculator (Nexus)

### RWB-SVC-S3 — rwb-guarantee (Guarantee)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S3 |
| Scope | S3 |
| Service | `rwb-guarantee` (Guarantee) |
| Epic wave | 2 |
| Arch v5 service wave | 3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 17 of 17 stories carry this suggestion; work-type mix: Contract 8 · App development 9 (§R5.3) |
| Owner mix of the stories | TechX 17 |
| Stories | 17 |
| Lanes | 10 (contract groups: CG-W3) |
| Day-1 stories | 17 |
| Business-epic tags | EP02, EP04 |
| Releases | 31 December 2026 (tentative) — 1 · 28 February 2027 (tentative) — 16 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md` |
| Schema | `rwb_guarantee` |
| REST base | `/api/recovery/guarantee/v1` |
| Topic | `rwb.guarantee.events.v1` |
| Temporal task queue | `rwb-guarantee` |
| Workflows owned | GuaranteeClaimWorkflow |
| Tables in the Ownership Map | 1 |
| REST operations in the Ownership Map | 2 |
| Events published in the Ownership Map | 0 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /guarantee-claims ; events NoticeDelivered; ProceedsMatched ; Temporal GuaranteeClaimWorkflow
- Out: schema rwb_guarantee (TCG and insurance claims, guarantor notices and pursuit) ; topic rwb.guarantee.events.v1: GuaranteeClaimFiled, GuaranteeClaimSettled ; TMP Comms: child: guarantor notice · Decision: child: approval

### RWB-SVC-S4 — rwb-litigation (Litigation)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S4 |
| Scope | S4 |
| Service | `rwb-litigation` (Litigation) |
| Epic wave | 2 |
| Arch v5 service wave | 3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 45 of 45 stories carry this suggestion; work-type mix: Contract 22 · App development 23 (§R5.3) |
| Owner mix of the stories | TechX 45 |
| Stories | 45 |
| Lanes | 24 (contract groups: CG-W3) |
| Day-1 stories | 45 |
| Business-epic tags | EP02, EP05 |
| Releases | 31 December 2026 (tentative) — 1 · 31 March 2027 (tentative) — 44 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S4 rwb-litigation v1.md` |
| Schema | `rwb_litigation` |
| REST base | `/api/recovery/litigation/v1` |
| Topic | `rwb.litigation.events.v1` |
| Temporal task queue | `rwb-litigation` |
| Workflows owned | LitigationWorkflow |
| Tables in the Ownership Map | 2 |
| REST operations in the Ownership Map | 5 |
| Events published in the Ownership Map | 0 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /legal-actions; GET/POST /hearings ; events NoticeDelivered; PartnerResultSubmitted ; Temporal LitigationWorkflow (years; continues-as-new)
- Out: schema rwb_litigation (legal actions, hearings, judgments, enforcement, LED auction ladder) ; topic rwb.litigation.events.v1: LawsuitFiled, JudgmentRecorded, AuctionResult ; TMP Partner: issueInstruction (law firm) · Comms: child: demand notice · Decision: child: approval

### RWB-SVC-S5 — rwb-asset (Asset)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S5 |
| Scope | S5 |
| Service | `rwb-asset` (Asset) |
| Epic wave | 1 |
| Arch v5 service wave | 2 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 51 of 51 stories carry this suggestion; work-type mix: Contract 25 · App development 26 (§R5.3) |
| Owner mix of the stories | TechX 51 |
| Stories | 51 |
| Lanes | 28 (contract groups: CG-W2, CG-W3) |
| Day-1 stories | 51 |
| Business-epic tags | EP01, EP03, EP04 |
| Releases | 30 November 2026 (tentative) — 1 · 31 January 2027 (tentative) — 22 · 28 February 2027 (tentative) — 28 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md` |
| Schema | `rwb_asset` |
| REST base | `/api/recovery/asset/v1` |
| Topic | `rwb.asset.events.v1` |
| Temporal task queue | `rwb-asset` |
| Workflows owned | AssetDisposalWorkflow |
| Tables in the Ownership Map | 2 |
| REST operations in the Ownership Map | 6 |
| Events published in the Ownership Map | 1 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /assets, /listings; POST /auction-rounds ; events JudgmentRecorded, AuctionResult; ProceedsMatched ; Temporal AssetDisposalWorkflow; Schedule: re-appraisal monthly
- Out: schema rwb_asset (assets taken on, holding, floor price, listings, auction rounds) ; topic rwb.asset.events.v1: AssetTakenOn, AssetSold ; TMP Partner: issueInstruction (auction vendor) · Decision: child: approval · Payment: postProceeds

### RWB-SVC-S6 — rwb-debtsale (Debt sale)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S6 |
| Scope | S6 |
| Service | `rwb-debtsale` (Debt sale) |
| Epic wave | 3 |
| Arch v5 service wave | 3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 30 of 30 stories carry this suggestion; work-type mix: Contract 14 · App development 16 (§R5.3) |
| Owner mix of the stories | TechX 30 |
| Stories | 30 |
| Lanes | 18 (contract groups: CG-W3, CG-W4) |
| Day-1 stories | 30 |
| Business-epic tags | EP05, EP06 |
| Releases | 31 March 2027 (tentative) — 7 · 30 April 2027 (tentative) — 23 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md` |
| Schema | `rwb_debtsale` |
| REST base | `/api/recovery/debtsale/v1` |
| Topic | `rwb.debtsale.events.v1` |
| Temporal task queue | `rwb-debtsale` |
| Workflows owned | DebtSaleWorkflow |
| Tables in the Ownership Map | 2 |
| REST operations in the Ownership Map | 5 |
| Events published in the Ownership Map | 1 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /lots; POST /lots/{id}/bids · /award ; events ProceedsMatched ; Temporal DebtSaleWorkflow (saga, pivot = transfer)
- Out: schema rwb_debtsale (lots, data room, buyer terms, bids, award, transfer) ; topic rwb.debtsale.events.v1: LotAwarded, AccountsTransferred ; TMP Document: data room pack · Decision: child: approval · Integration: deliverFile (buyer file) · Payment: postProceeds

### RWB-SVC-S7 — rwb-writeoff (Write-off)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S7 |
| Scope | S7 |
| Service | `rwb-writeoff` (Write-off) |
| Epic wave | 4 |
| Arch v5 service wave | 4 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 32 of 32 stories carry this suggestion; work-type mix: Contract 16 · App development 16 (§R5.3) |
| Owner mix of the stories | TechX 32 |
| Stories | 32 |
| Lanes | 17 (contract groups: CG-W4) |
| Day-1 stories | 32 |
| Business-epic tags | EP06 |
| Releases | 30 April 2027 (tentative) — 32 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md` |
| Schema | `rwb_writeoff` |
| REST base | `/api/recovery/writeoff/v1` |
| Topic | `rwb.writeoff.events.v1` |
| Temporal task queue | `rwb-writeoff` |
| Workflows owned | WriteOffWorkflow |
| Tables in the Ownership Map | 1 |
| REST operations in the Ownership Map | 2 |
| Events published in the Ownership Map | 1 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /write-offs; POST /write-offs/{id}/submit ; events AceDataReady (GL write-off); ProceedsMatched ; Temporal WriteOffWorkflow; Schedule: scan, 3rd working day
- Out: schema rwb_writeoff (eligibility, committee, posting, recovery after charge-off) ; topic rwb.writeoff.events.v1: WriteOffApproved ; TMP Decision: child: committee approval · Payment: postProceeds ; REST Source data: GL outcome

### RWB-SVC-S8 — rwb-deviation (Deviation)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S8 |
| Scope | S8 |
| Service | `rwb-deviation` (Deviation) |
| Epic wave | 1 |
| Arch v5 service wave | 2 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 31 of 31 stories carry this suggestion; work-type mix: Contract 10 · App development 21 (§R5.3) |
| Owner mix of the stories | TechX 31 |
| Stories | 31 |
| Lanes | 22 (contract groups: CG-W4) |
| Day-1 stories | 31 |
| Business-epic tags | EP01, EP02, EP03, EP07 |
| Releases | 30 November 2026 (tentative) — 5 · 31 December 2026 (tentative) — 5 · 31 January 2027 (tentative) — 1 · 31 May 2027 (tentative) — 20 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md` |
| Schema | `rwb_deviation` |
| REST base | `/api/recovery/deviation/v1` |
| Topic | `rwb.deviation.events.v1` |
| Temporal task queue | `rwb-deviation` |
| Workflows owned | DeviationWorkflow |
| Tables in the Ownership Map | 1 |
| REST operations in the Ownership Map | 2 |
| Events published in the Ownership Map | 2 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST GET/POST /deviations; POST /deviations/{id}/clear ; events CaseCreated (screening); AceDataReady (deceased, bankrupt flags); AgentRunCompleted ; Temporal DeviationWorkflow (child of case)
- Out: schema rwb_deviation (X1-X7 screening, pause, handling, return) ; topic rwb.deviation.events.v1: DeviationRaised, DeviationCleared ; TMP Agent: child: screening agent run ; REST Source data: party flags

### RWB-SVC-S9 — rwb-partner (Partner)

| Item | Value |
|---|---|
| Epic | RWB-SVC-S9 |
| Scope | S9 |
| Service | `rwb-partner` (Partner) |
| Epic wave | 1 |
| Arch v5 service wave | 4 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 36 of 36 stories carry this suggestion; work-type mix: Contract 16 · App development 20 (§R5.3) |
| Owner mix of the stories | TechX 36 |
| Stories | 36 |
| Lanes | 21 (contract groups: CG-W4) |
| Day-1 stories | 36 |
| Business-epic tags | EP01, EP02, EP06, EP07, EP08 |
| Releases | 30 November 2026 (tentative) — 2 · 31 December 2026 (tentative) — 2 · 28 February 2027 (tentative) — 2 · 30 April 2027 (tentative) — 14 · 31 May 2027 (tentative) — 16 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md` |
| Schema | `rwb_partner` |
| REST base | `/api/recovery/partner/v1` |
| Topic | `rwb.partner.events.v1` |
| Temporal task queue | `rwb-partner` |
| Workflows owned | InstructionWorkflow |
| Tables in the Ownership Map | 3 |
| REST operations in the Ownership Map | 6 |
| Events published in the Ownership Map | 2 |
| Rule references | §R4 (naming per service); DP table of §R5.5 |

**Contract in Arch v5 (slides 14-20).**

- In: REST Staff: GET/POST /partners, /instructions; Partner portal: /partner/v1/* (FAPI 2.0) ; events (work arrives as Temporal tasks) ; Temporal InstructionWorkflow: SLA timers; Act: issueInstruction, recordResult
- Out: schema rwb_partner (panel, partner users, instructions, results, fees, scorecards) ; topic rwb.partner.events.v1: InstructionIssued, PartnerResultSubmitted ; REST Document: partner uploads (link) · Partners (law firms, agencies, buyers): via partner gateway, MFA

## 5. Integration epics (5)

One integration epic per wave plus the non-functional epic (§R5.1). Integration stories are the only stories allowed to carry I dependencies (real cross-service behaviour, §R5.4 and §R5.7 rule 4), and the contract-test harness `RWB-ITG-W1J01-ITG` is what makes QA Day-1 work in wave 1 (§R5.7 rule 6).

### RWB-ITG-W1 — Wave 1 integration

| Item | Value |
|---|---|
| Epic | RWB-ITG-W1 |
| Scope | ITG |
| Service | integration |
| Epic wave | 1 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 50 of 52 stories carry this suggestion; work-type mix: Integration 52 (§R5.3) |
| Owner mix of the stories | TechX 50 · QA team 2 |
| Stories | 52 |
| Lanes | 1 (no contract group) |
| Day-1 stories | 52 |
| Business-epic tags | EP01, EP01-TE, NEW |
| Releases | 30 November 2026 (tentative) — 50 · None (new story) — 2 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-ITG-W1J01-ITG` Contract-test harness and synthetic test data (§R5.7 rule 6) · `RWB-ITG-W1J02-ITG` Wave 1 v5 journey end to end |
| Rule references | §R5.1 (one integration epic per wave); §R5.5 DP-11 and DP-16 (REST one hop, 2 s timeout; rwb-integration contract); §R5.7 rule 6 (the harness makes QA Day-1 work) |

### RWB-ITG-W2 — Wave 2 integration

| Item | Value |
|---|---|
| Epic | RWB-ITG-W2 |
| Scope | ITG |
| Service | integration |
| Epic wave | 2 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 42 of 43 stories carry this suggestion; work-type mix: Integration 43 (§R5.3) |
| Owner mix of the stories | TechX 42 · QA team 1 |
| Stories | 43 |
| Lanes | 1 (no contract group) |
| Day-1 stories | 43 |
| Business-epic tags | EP02, EP03, NEW |
| Releases | 31 December 2026 (tentative) — 34 · 31 January 2027 (tentative) — 8 · None (new story) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-ITG-W2J01-ITG` Wave 2 journey end to end |
| Rule references | §R5.1 (one integration epic per wave); §R5.4 class I (real cross-service behaviour, ITG stories only); §R5.7 rule 4 |

### RWB-ITG-W3 — Wave 3 integration

| Item | Value |
|---|---|
| Epic | RWB-ITG-W3 |
| Scope | ITG |
| Service | integration |
| Epic wave | 3 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 8 of 9 stories carry this suggestion; work-type mix: Integration 9 (§R5.3) |
| Owner mix of the stories | TechX 8 · QA team 1 |
| Stories | 9 |
| Lanes | 1 (no contract group) |
| Day-1 stories | 9 |
| Business-epic tags | EP04, EP05, NEW |
| Releases | 28 February 2027 (tentative) — 6 · 31 March 2027 (tentative) — 2 · None (new story) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-ITG-W3J01-ITG` Wave 3 journey end to end |
| Rule references | §R5.1 (one integration epic per wave); §R5.4 class I (real cross-service behaviour, ITG stories only); §R5.7 rule 4 |

### RWB-ITG-W4 — Wave 4 integration

| Item | Value |
|---|---|
| Epic | RWB-ITG-W4 |
| Scope | ITG |
| Service | integration |
| Epic wave | 4 |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Owner basis | TechX 40 of 41 stories carry this suggestion; work-type mix: Integration 41 (§R5.3) |
| Owner mix of the stories | TechX 40 · QA team 1 |
| Stories | 41 |
| Lanes | 1 (no contract group) |
| Day-1 stories | 41 |
| Business-epic tags | EP06, EP07, EP08, NEW |
| Releases | 30 November 2026 (tentative) — 4 · 31 December 2026 (tentative) — 7 · 28 February 2027 (tentative) — 1 · 30 April 2027 (tentative) — 10 · 31 May 2027 (tentative) — 13 · 30 June 2027 (tentative) — 5 · None (new story) — 1 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-ITG-W4J01-ITG` Wave 4 journey end to end |
| Rule references | §R5.1 (one integration epic per wave); §R5.4 class I (real cross-service behaviour, ITG stories only); §R5.7 rule 4 |

### RWB-ITG-NFR — Non-functional integration

| Item | Value |
|---|---|
| Epic | RWB-ITG-NFR |
| Scope | ITG |
| Service | integration |
| Epic wave | 1 |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Owner basis | QA team 2 of 2 stories carry this suggestion; work-type mix: Integration 2 (§R5.3) |
| Owner mix of the stories | QA team 2 |
| Stories | 2 |
| Lanes | 1 (no contract group) |
| Day-1 stories | 2 |
| Business-epic tags | EP01-TE |
| Releases | 31 December 2026 (tentative) — 2 |
| PRD | `03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md` |
| Key stories | `RWB-ITG-TE009-ITG` Performance test harness · `RWB-ITG-TE010-ITG` Browser and accessibility tests |
| Rule references | §R5.3 (harness and NFR stories: QA team); §R5.1 (non-functional integration epic); §R5.6 (W-MAP wave of the EP01-TE stories) |

## 6. Day-1 work by team type

Every team type has Day-1 work (§R5.7 rule 6). Counted from the Stories sheet of the catalog:

| Team type | §R5.3 work types | Day-1 stories | Epics with Day-1 work |
|---|---|---|---|
| TechX | CON, APP, ITG | 846 | 27 |
| ACE team | DB | 11 | 5 |
| SCB IT infrastructure | INF | 18 | 9 |
| DevOps team | OPS | 57 | 13 |
| QA team | ITG (harness and NFR) | 7 | 5 |

Total Day-1 stories: 939.

## 7. Epics per wave

| Wave | Platform epics | Service epics | Integration epics | Stories |
|---|---|---|---|---|
| 0 | 7 | 0 | 0 | 65 |
| 1 | 0 | 13 | 2 | 681 |
| 2 | 0 | 3 | 1 | 152 |
| 3 | 0 | 2 | 1 | 63 |
| 4 | 0 | 1 | 1 | 73 |

A service epic sits in the wave of its earliest story, so seven service epics start before their service's Arch v5 wave: `RWB-SVC-S3` (epic wave 2, Arch v5 wave 3), `RWB-SVC-S4` (2 / 3), `RWB-SVC-S5` (1 / 2), `RWB-SVC-S6` (3 / 4), `RWB-SVC-S8` (1 / 2), `RWB-SVC-S9` (1 / 4) and `RWB-SVC-P8` (1 / 2). The other twelve service epics start in their service's own wave (`RWB-SVC-S1` 3, `RWB-SVC-S2` 2, `RWB-SVC-S7` 4, and `RWB-SVC-P1`–`RWB-SVC-P7`, `RWB-SVC-P9` and `RWB-SVC-P10` at 1). The story-level conflict is raised once per service and business epic by the story work packages (§R5.6).

## 8. Lanes and contract groups

| Contract group | Wave | Stories in the group | Epics that use it |
|---|---|---|---|
| CG-W0 | 0 | 17 | 4 |
| CG-W1 | 1 | 44 | 9 |
| CG-W2 | 2 | 64 | 12 |
| CG-W3 | 3 | 71 | 7 |
| CG-W4 | 4 | 92 | 10 |

A contract group is one lane shared by every epic of its wave, so the per-epic lane counts in §2 add to 547 while the programme has 510 distinct lanes. The other lanes are per-epic work lanes `L-<scope>-<n>` and the integration lanes `L-ITG-W<n>`.

## 9. Totals and reconciliation

| Measure | Value | Source |
|---|---|---|
| Epics | 31 (19 service, 7 platform, 5 integration) | Catalog Epics sheet; §R5.1 |
| Stories | 1034 | Catalog Epics sheet; `split_plan.json` stats slices |
| Day-1 stories | 939 | Catalog Epics sheet; `split_plan.json` stats day1 |
| Legacy stories mapped | 358 | `split_plan.json` stats legacy |
| Distinct lanes | 510 | `split_plan.json` stats lanes |
| Epic-lane memberships | 547 | Catalog Epics sheet (a shared contract group is counted per epic) |
| Release dates | unchanged, every one marked (tentative) | Catalog Stories sheet |

## 10. Open items

Three documentation values are not carried by the source catalog and are resolved as recorded: they do not change a story, a lane or a date.

| ID | What is open | Resolution used here | Severity |
|---|---|---|---|
| GAP-3198 | The catalog has no epic-level scope or owner column. | Scope from the epic ID pattern (§R5.2); owner from the Ownership Map and the work-type owner table (§R5.3). Assumption ASM-5600. | P3 |
| GAP-3199 | The catalog Epics sheet gives a wave but no rule for it, and §R5.6 also puts "NF" work at wave 0. | Epic wave = earliest wave among its stories; the Arch v5 service wave is shown beside it. Assumption ASM-5601. | P3 |
| GAP-3200 | Per-epic lane counts add to 547, the distinct lane count is 510. | A shared contract group `CG-W<n>` is counted in every epic that uses it; both numbers are shown. Assumption ASM-5602. | P3 |

## 11. Traceability

| DOC ID | Part of this file | Source | Decision |
|---|---|---|---|
| DOC-EPICS-01 | §1 and §2, the 31 epics and their scope | Catalog Epics sheet; §R5.1, §R5.2, U1 | D-RCV-60 |
| DOC-EPICS-02 | §2 and §3–§5, wave per epic | Catalog Stories sheet waves; §R5.6 | D-RCV-60 |
| DOC-EPICS-03 | §2 and §3–§5, suggested owner per epic | Ownership Map Services sheet; §R5.3, U3 | D-RCV-60 |
| DOC-EPICS-04 | §4, the service runtime facts (schema, REST base, topic, queue, workflows, tables, operations, events) | Ownership Map Services and Workflows and activities sheets; `ownership.json` | D-RCV-60 |
| DOC-EPICS-05 | §4, the IN and OUT contract lines | Arch v5 Text Extract v1 slides 14-20 | D-RCV-60 |
| DOC-EPICS-06 | §6–§9, Day-1 work, waves, lanes and totals | Catalog Stories and Epics sheets; `split_plan.json` stats; §R5.7 | D-RCV-60 |

## 12. Out of scope

- The story content itself: each story file carries its own 20 metadata rows and 19 sections, and its acceptance criteria.
- The Day-1 Work Allocation v1 (capacity per lane) and the epic overview per epic folder, which are separate files of the Service Story Catalog v1 set (§R8.7).
- The build order, dependency map and RTM, which are their own next versions (§R8.7).
- Anything outside the Recovery Workbench: no data lake (DP-17), no tracker update (U6).
