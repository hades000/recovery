## Sheet: Read me

| SCB Collections and Recovery. Henka Group, 22 November 2026. |
|---|
| (C) Siam Commercial Bank and Henka Pte Ltd |
| Recovery Workbench Risks Assumptions Issues and Dependencies v5 (D-RCV-60 microservice realignment). |
| Sheets: Risks, Assumptions, Issues, Dependencies. Every row of v4 is kept with its ID, number and date; the realignment only adds rows and points the owners at the Ownership Map v1. |
| Change log |
| v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |
| Realignment notes |
| 1. The nine realignment risks R1 to R9 are added to the Risks sheet as R-19 to R-27, so that no ID of the source version changes. Mapping: R1 to R-19, R2 to R-20, R3 to R-21, R4 to R-22, R5 to R-23, R6 to R-24, R7 to R-25, R8 to R-26, R9 to R-27. |
| 2. Owners are roles, never names. Where the Recovery Workbench Microservice Ownership Map v1 assigns the item to one of the 19 services, the service code and name are added in brackets after the role (P1 rwb-source-data to P10 rwb-agent, S1 rwb-valuation to S9 rwb-partner, PLT for the platform). |
| 3. Positions that the realignment adds beyond the ten of the Assumptions sheet are held in the Assumptions Register v1 (folder 23). The Assumptions sheet carries the pointer row A-11; where a row of this workbook relies on a register position, the register row is named. |
| 4. Dates are copied unchanged from v4. No release date appears in this workbook; a release date added later is marked (tentative). |
| 5. The 19 services, their schemas, topics, queues, owners of tables and endpoints, and the default rulings are those of the Architecture v5 Text Extract v1 and the Ownership Map v1. |
| Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. |

## Sheet: Risks

| Risks |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 27 risks: 26 open and 1 closed by D-RCV-35, with impact, likelihood, action, owner and review date. Nine realignment risks R1 to R9 are added by D-RCV-60 as R-19 to R-27 (see the Read me sheet); owners point to the Ownership Map v1. v5, 22 November 2026. |  |  |  |  |  |  |  |
| ID | Risk | Impact | Likelihood | Action | Owner | Review by | Status |
| R-01 | Data arrives a day late for decisions that need today's position | High | Medium | Closed by D-RCV-35 on 15 November 2026: the Workbench runs no load, so its position is the ACE business date and every screen shows the freshness stamp; ACE batch lateness is carried by R-13 | Solution architect (P1 rwb-source-data) | 2026-11-30 00:00:00 | Closed |
| R-02 | Collateral, appraisals and assets arrive weekly or monthly | Medium | High | Age limits on decision inputs; the ACE feed cadence and the age of each data product are published in the catalog (DL12 option A is superseded by D-RCV-35) | Data lead (P1 rwb-source-data) | 2026-11-20 00:00:00 | Open |
| R-03 | One squad's change holds the other's release | Medium | Medium | Feature flags, code owners and the module boundary test (DL04, DL37) | Tech leads (PLT) | 2026-11-06 00:00:00 | Open |
| R-04 | Embedded Drools is new to ACE | Medium | Medium | Drools evaluator in the recovery module, tested package by package; R-16 covers the RW-COE author training and RWB-E1-073 carries the package load checks | Solution architect (P7 rwb-decision) | 2026-11-27 00:00:00 | Open |
| R-05 | Volume grows faster than forecast | Medium | Low | Sized at 15 percent inflow growth; reviewed each quarter (DL15) | Data lead (P1 rwb-source-data) | 2027-03-31 00:00:00 | Open |
| R-06 | Partner access from outside the bank takes one to three months | High | High | Change raised in November; law firms first needed at Epic 5 (DL03) | Product owner (S9 rwb-partner) | 2026-11-30 00:00:00 | Open |
| R-07 | Epic 3 has no confirmed builder for TDR and DIL | High | Medium | Decision DL14 by 6 Nov; the plan holds Epic 3 scope until then | IT lead (S2 rwb-treatment) | 2026-11-06 00:00:00 | Open |
| R-08 | Deployment slots limit parallel testing | Medium | High | One DEV and one SIT slot shared until DL35 is met | ACE team (PLT) | 2026-11-06 00:00:00 | Open |
| R-09 | Songkran and Chakri Day fall in the Epic 6 test weeks | Medium | High | Release window confirmed under DL34; testers booked early | Program manager | 2027-03-01 00:00:00 | Open |
| R-10 | Business testers not available during the build | High | Medium | Testers named under DL09; scripts prepared with the analysts | Business lead | 2026-11-06 00:00:00 | Open |
| R-11 | Thai wording not ready for Epic 2 screens and letters | Medium | Medium | English release with Thai labels loaded as reference data when supplied (DL10) | Business lead (P6 rwb-comms) | 2026-11-20 00:00:00 | Open |
| R-12 | Agent model endpoint not approved | Medium | Medium | Agents run in shadow; rules decide (DL33) | CTO with Enterprise AI (P10 rwb-agent) | 2026-11-06 00:00:00 | Open |
| R-13 | RWB-ACE-001 lands late, or the ACE team does not accept the 14 tables, 12 columns, the batch record and the grant | High | Medium | DL43 estimated and accepted by 21 November; the 16 Section A views go first so the case record can start; a Tier 1-only fallback for the case list is costed | ACE team lead; program manager (P1 rwb-source-data) | 2026-11-21 00:00:00 | Open |
| R-14 | Temporal operational skills and on-call load for SCB IT: cluster upgrades, backup and certificates | High | Medium | Name SCB IT as the operator with an on-call rota; the RWB-E1-070 run book covers upgrade, backup, certificate and namespace recovery; drill each in SIT before the Epic 3 build window; RWB-E2-037 and RWB-E2-039 add the alerts and the failover test | SCB IT platform lead (PLT) | 2026-11-27 00:00:00 | Open |
| R-15 | Epic 1 date pressure: the four new configuration stories RWB-E1-070 to RWB-E1-073 must land before the engines | High | High | Start the Temporal and Drools configuration in window 2; pull RWB-E1-070 to RWB-E1-073 before RWB-E1-018, RWB-E1-020 and RWB-E1-021; review burn-down at the weekly sponsor review; keep the engine stories behind their flags if a configuration story slips | Program manager (PLT) | 2026-11-16 00:00:00 | Open |
| R-16 | Drools XLS authoring training for RW-COE | Medium | High | Run the authoring workshop and template guide in RWB-E1-073; coach two package loads before the first live approval; RW-RISK reviews the first three packages; the scenario suite must reach rules.testcases.min before approval | RW-COE lead (P7 rwb-decision) | 2026-11-27 00:00:00 | Open |
| R-17 | The cancelled INC-006 and INC-019 work and its lost build output | Medium | High | Close INC-006 and INC-019 as cancelled under D-RCV-36; keep the branch and build output as reference only; RWB-E1-073 rebuilds the scenario runner, the load checks and the approval path; no reuse without review | Delivery lead | 2026-11-20 00:00:00 | Open |
| R-18 | SCB IT has not approved the Temporal server and Java SDK versions or the Drools KIE library versions | High | Medium | Submit the version list in window 1; pin only approved versions; record the approved versions in Environment and Deployment Design v4; DEP-36 tracks the approval and the build does not start the platform stories until it closes | SCB IT architecture (PLT) | 2026-11-16 00:00:00 | Open |
| R-19 | 19 services instead of one deployable: delivery, on-call and release load spread over 19 services plus the platform | High | High | Build the platform once in Wave 0: service template, one Helm chart, golden pipeline, contract libraries, workflow kit, 19 schemas and logins, Kafka topics and ACLs; services arrive with the epic that needs them (9 in wave 1, then 4, 4 and 2); observability per service; the platform team runs Kafka and Temporal. Carried as realignment risk R1. | Delivery lead (PLT) | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-20 | Kafka is not ready on the ACE platform, so events stay in the outbox and each service misses the facts it consumes | High | Medium | Outbox and inbox library with CloudEvents on topics rwb.<short>.events.v1, with retry and .dlt topics; events wait in the outbox until the broker returns; Azure Event Hubs Kafka endpoint as the fallback; topics, ACLs and quotas agreed with the ACE platform team before the wave 1 go-live. Carried as realignment risk R2. | PLT (event platform); P2 rwb-integration | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-21 | 19 schemas and 19 logins in the ACE database: connection budget, grants and cross-schema leaks | High | Medium | One login per service with its own PgBouncer pool and connection cap; grant on the own schema only; no cross-schema join, view or foreign key; the boundary test fails a build on any cross-schema reference; Flyway per service in its own schema; the RWB-ACE-001 grant feeds the recovery.v_ace_* views to rwb-source-data only. Carried as realignment risk R3. | PLT (ACE DB schemas and logins); ACE team | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-22 | The shared Temporal layer is not yet owned or operated at the version the design needs: Nexus and Worker Versioning below 1.30+ | High | Medium | Upgrade in Wave 0 before the first service goes live, under DEP-36 and R-18; the workflow kit is versioned and workers are pinned with Worker Versioning; the replay gate replays recorded histories against every new build; the run book covers upgrade, backup, certificate and namespace recovery. Carried as realignment risk R4. | PLT (workflow platform); SCB IT platform lead | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-23 | Rule conversion from XLS decision tables to DMN 1.6 table by table on an embedded Drools runtime, with governance central in one service | Medium | High | Convert table by table on the same Drools runtime; KIE libraries only, no KIE Server, Business Central or KJAR; package load checks and at least 50 scenarios before approval; the rule package registry and the four-eyes approval stay in rwb-decision, each service runs its own evaluated copy; R-04, R-16 and R-18 stay open. Carried as realignment risk R5. | P7 rwb-decision | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-24 | Contract-first calls across 19 services: REST is one hop with a 2 s timeout, so a new cross-service hop is a design change and not a build fix | Medium | Medium | Every consumer builds against the published contract and its fake, so no build waits on another team; REST stays one hop with a 2 s timeout, circuit breakers and bulkheads; real cross-service behaviour is tested on integration stories only; a service holds another service's ID and asks through its contract, never through its schema. Carried as realignment risk R6. | Architecture (PLT contract libraries) | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-25 | The ledger model is not accepted by Audit: a local decision record plus the central ledger in rwb-decision, instead of one synchronous central log | High | Medium | Strict mode for irreversible steps; a walkthrough with Risk and Internal Audit before the wave 1 go-live; the local decision-record library publishes on the shared topic rwb.decision-record.v1 and the central ledger stays in rwb-decision; rollback to the central log is one configuration change per service. Carried as realignment risk R7. | P7 rwb-decision; Risk and Internal Audit | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-26 | The programme finishes within 8 months while wave 1 carries nine services, the platform and the ACE changes together | High | High | Platform and contract stories first, as Day 1 work for every team type; a service is built when its epic starts, so nothing is built twice; the Epic 1 change is a set of delta stories against the preserved built stories; burn-down at the weekly sponsor review; dates unchanged and tentative (DL48). Carried as realignment risk R8. | Program manager (PLT) | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |
| R-27 | No data lake: reports come from a read model built from events in rwb-reporting, so a story that still expects lake data blocks | Medium | High | INT-19 and INT-20 are removed and the data lake copy is dropped; rwb-reporting builds its measures and snapshots from the events of the owning services, not from ACE tables; a story that still needs lake data raises a gap in the Change Register instead of a lake dependency. Carried as realignment risk R9. | P9 rwb-reporting | Not specified in the source documents (CG-B-DELIVDOC-48-1; ASM-B-DELIVDOC-48-1) | Open |

## Sheet: Assumptions

| Assumptions |  |  |  |
|---|---|---|---|
| Positions the build uses until the bank decides. |  |  |  |
| ID | Assumption | Decision | Status |
| A-01 | Entry at 90 days past due | DL16 | Open |
| A-02 | One case per customer per product | DL17 | Open |
| A-03 | Application owner administration of access | DL01 | Open |
| A-04 | Customer facts from ACE, which ingests them from SCBPDM and the core bank, read through v_ace_customer | DL20 | Open |
| A-05 | Provisional delegation limits from the approval authority regulation | DL18 | Open |
| A-06 | Service level and caseload values loaded as placeholders | DL22, DL23 | Open |
| A-07 | Current bank letter templates as version 1 | DL28 | Open |
| A-08 | Inventory counts and 15 percent growth for sizing | DL15 | Open |
| A-09 | TechX squad shape: tech lead, three back end, one front end, one QA | DL36 | Open |
| A-10 | Monthly release in the last week of each month | DL34 | Open |
| A-11 | Positions the realignment adds are held in the Assumptions Register v1 (folder 23); where a row of this workbook relies on a register position, the register row is named in the Action column | D-RCV-60 | Open |

## Sheet: Issues

| Issues |  |  |  |  |  |
|---|---|---|---|---|---|
| Problems happening now. |  |  |  |  |  |
| ID | Issue | Owner | Needed by | Action | Status |
| I-01 | Two deployment slots planned in DEV are not yet available | ACE team | 2026-11-06 00:00:00 | Squads share one slot; tests queued | Open |
| I-02 | Decision owners past their date on DL01 and DL02 | Product owner | 2026-10-30 00:00:00 | Escalated to the sponsor review | Open |
| I-03 | CCMS and SVAF layouts not confirmed by the ACE team before RWB-ACE-001 | ACE team | 2026-11-21 00:00:00 | ACE team confirms both layouts inside RWB-ACE-001; the Workbench builds no adapter and holds no copy | Open |

## Sheet: Dependencies

| Dependencies |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 36 dependencies from the dependency map, including DEP-36 for the Temporal and Drools version approval. Owners point to the Ownership Map v1 (D-RCV-60). v5, 22 November 2026. |  |  |  |  |  |  |
| ID | On | What is needed | Epic | Needed by | Owner | Decision |
| DEP-01 | ACE team | Recovery module folder, package and boundary test in the ACE repository | E1 | 2026-11-02 00:00:00 | ACE team (PLT) | DL05 |
| DEP-02 | ACE team | Code owners file and merge rules for the recovery module | E1 | 2026-11-02 00:00:00 | ACE team (PLT) | DL04, DL37 |
| DEP-03 | ACE team | Deployment slots: one DEV and one SIT for the recovery squads | E1 | 2026-11-06 00:00:00 | ACE team (PLT) | DL35 |
| DEP-04 | ACE team | Common module services: sign-in, access check, audit and PII logging, the shared case view | E1 | 2026-11-09 00:00:00 | ACE team (PLT) | None |
| DEP-05 | ACE team | Monthly release window and the release owner | E1 | 2026-11-13 00:00:00 | SCB IT | DL34 |
| DEP-06 | ACE team | Restructure calculator and plan status from the common module | E2 | 2026-12-01 00:00:00 | ACE team with the collection squad | DL14, DL30 |
| DEP-07 | Collection squad | EFS hand-over data and contact history in the COLLINS load | E2 | 2026-11-30 00:00:00 | Collection squad with data engineering | DL29 |
| DEP-08 | Collection squad | Shared Epic 2 items: notice path, customer contact stop, shared tasks | E2 | 2026-11-30 00:00:00 | IT lead with the product owner | DL30 |
| DEP-09 | Collection squad | TDR and DIL split between the collection squad, the Enterprise AI team and TechX | E3 | 2026-12-15 00:00:00 | IT lead | DL14 |
| DEP-10 | Architecture team | Partner access from outside the bank through the external gateway | E5 | 2027-02-01 00:00:00 | Architecture team (S9 rwb-partner) | DL03 |
| DEP-11 | Architecture team | Model endpoint the agents call, inside the SCB tenant | E1 | 2026-11-06 00:00:00 | CTO with Enterprise AI (P10 rwb-agent) | DL33 |
| DEP-12 | Architecture team | Non-functional targets for availability, recovery point and recovery time | E1 | 2026-11-13 00:00:00 | Solution architect with Risk (PLT) | DL11 |
| DEP-13 | Architecture team | Legacy systems kept, changed or retired | E2 | 2026-11-20 00:00:00 | IT lead | DL12 |
| DEP-14 | Data engineering | COLLINS load of account, payment, customer and score data into the ACE database for recovery accounts | E1 | 2026-11-09 00:00:00 | Data engineering | DL06, DL20 |
| DEP-15 | Data engineering | File layouts and test files for CCMS, SVAF, AMIS, RPS, WIN and GL | E1 | 2026-11-13 00:00:00 | Data engineering with the system owners | DL12 |
| DEP-16 | Data engineering | Masked test data in SIT and UAT from the PII service | E1 | 2026-11-13 00:00:00 | Data engineering | DL26 |
| DEP-17 | Data engineering | Reconciliation tolerance per data product | E1 | 2026-11-13 00:00:00 | Data lead (P1 rwb-source-data) | DL25 |
| DEP-18 | SCB IT security | Entra ID groups for the Workbench roles in each environment | E1 | 2026-11-09 00:00:00 | SCB IT security | DL40 |
| DEP-19 | SCB IT security | Access timers: session, inactivity and break-glass | E2 | 2026-11-20 00:00:00 | SCB IT security | DL38 |
| DEP-20 | Enterprise AI team | Agent platform: orchestrator, tool gateway, prompt store and evaluation | E1 | 2026-11-16 00:00:00 | Enterprise AI team (P10 rwb-agent) | DL33 |
| DEP-21 | Enterprise AI team | Route return models by route for the route decision | E4 | 2027-01-25 00:00:00 | Enterprise AI team with Model Risk (P10 rwb-agent) | None |
| DEP-22 | Autonomous Ops team | OCR and extraction for the first document types | E1 | 2026-11-16 00:00:00 | Autonomous Ops team (P5 rwb-document) | DL19 |
| DEP-23 | Business | Delegation of authority: holders, limits and substitutes | E2 | 2026-11-30 00:00:00 | Risk with the product heads | DL18 |
| DEP-24 | Business | Service levels per case state and caseload caps | E2 | 2026-11-13 00:00:00 | Business lead; product owner | DL22, DL23 |
| DEP-25 | Business | Letter templates approved by Legal in Thai and English | E2 | 2026-11-13 00:00:00 | Legal counsel (P6 rwb-comms) | DL28 |
| DEP-26 | Business | Business testers named for each release | E1 | 2026-11-06 00:00:00 | Business lead | DL09 |
| DEP-27 | Business | Thai labels and message wording | E2 | 2026-11-05 00:00:00 | Business lead with Legal and Compliance | DL10 |
| DEP-28 | Partners | Panel law firms onboarded to the partner portal with user accounts | E5 | 2027-03-01 00:00:00 | Partner and agency manager (S9 rwb-partner) | DL03 |
| DEP-29 | Partners | Valuers, auction vendors and RAMC onboarded to the partner portal | E4 | 2027-02-01 00:00:00 | Partner and agency manager (S9 rwb-partner); Head of Asset Liquidity | DL03 |
| DEP-30 | Partners | Debt buyers' data room access and confidentiality agreements | E5 | 2027-03-01 00:00:00 | Head of Asset Liquidity (S6 rwb-debtsale) | DL03 |
| DEP-31 | Partners | Collection agencies onboarded with placement and outcome capture | E6 | 2027-04-01 00:00:00 | Partner and agency manager (S9 rwb-partner) | DL03 |
| DEP-32 | Business | TCG claim rules and the guarantee quota | E4 | 2027-01-25 00:00:00 | Guarantee officer (S3 rwb-guarantee) | None |
| DEP-33 | Business | Write-off tax criteria version from Finance | E6 | 2027-03-22 00:00:00 | Finance and CFO delegate (S7 rwb-writeoff) | None |
| DEP-34 | ACE team | RWB-ACE-001: 14 tables, 12 columns, one batch record per source and business date and the SELECT grant that the 30 recovery.v_ace_* views read | E1 | 2026-11-21 00:00:00 | ACE team lead (P1 rwb-source-data) | DL43 |
| DEP-35 | ACE team | DL43: the ACE team's estimate and acceptance of RWB-ACE-001, with the 14 ingestion jobs and the migration window in the 30 November release named | E1 | 2026-11-21 00:00:00 | Sponsor with the ACE team lead (P1 rwb-source-data) | DL43 |
| DEP-36 | SCB IT | SCB IT approves the Temporal server and Java SDK versions and the Drools KIE library versions before the build window | E1 | 2026-11-16 00:00:00 | SCB IT architecture (PLT) | D-RCV-36 |
