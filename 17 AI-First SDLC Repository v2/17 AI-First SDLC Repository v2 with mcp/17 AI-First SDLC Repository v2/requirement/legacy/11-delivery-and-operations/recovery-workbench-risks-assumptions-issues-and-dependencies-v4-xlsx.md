<!-- source: 11 Delivery and operations/Recovery Workbench Risks Assumptions Issues and Dependencies v4.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Risks Assumptions Issues and Dependencies v4.xlsx`  
> **Converted from:** XLSX

## Risks

| Risks |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|
| 18 risks: 17 open and 1 closed by D-RCV-35, with impact, likelihood, action, owner and review date. v4, 16 November 2026. |  |  |  |  |  |  |  |
| ID | Risk | Impact | Likelihood | Action | Owner | Review by | Status |
| R-01 | Data arrives a day late for decisions that need today's position | High | Medium | Closed by D-RCV-35 on 15 November 2026: the Workbench runs no load, so its position is the ACE business date and every screen shows the freshness stamp; ACE batch lateness is carried by R-13 | Solution architect | 46356 | Closed |
| R-02 | Collateral, appraisals and assets arrive weekly or monthly | Medium | High | Age limits on decision inputs; the ACE feed cadence and the age of each data product are published in the catalog (DL12 option A is superseded by D-RCV-35) | Data lead | 46346 | Open |
| R-03 | One squad's change holds the other's release | Medium | Medium | Feature flags, code owners and the module boundary test (DL04, DL37) | Tech leads | 46332 | Open |
| R-04 | Embedded Drools is new to ACE | Medium | Medium | Drools evaluator in the recovery module, tested package by package; R-16 covers the RW-COE author training and RWB-E1-073 carries the package load checks | Solution architect | 46353 | Open |
| R-05 | Volume grows faster than forecast | Medium | Low | Sized at 15 percent inflow growth; reviewed each quarter (DL15) | Data lead | 46477 | Open |
| R-06 | Partner access from outside the bank takes one to three months | High | High | Change raised in November; law firms first needed at Epic 5 (DL03) | Product owner | 46356 | Open |
| R-07 | Epic 3 has no confirmed builder for TDR and DIL | High | Medium | Decision DL14 by 6 Nov; the plan holds Epic 3 scope until then | IT lead | 46332 | Open |
| R-08 | Deployment slots limit parallel testing | Medium | High | One DEV and one SIT slot shared until DL35 is met | ACE team | 46332 | Open |
| R-09 | Songkran and Chakri Day fall in the Epic 6 test weeks | Medium | High | Release window confirmed under DL34; testers booked early | Program manager | 46447 | Open |
| R-10 | Business testers not available during the build | High | Medium | Testers named under DL09; scripts prepared with the analysts | Business lead | 46332 | Open |
| R-11 | Thai wording not ready for Epic 2 screens and letters | Medium | Medium | English release with Thai labels loaded as reference data when supplied (DL10) | Business lead | 46346 | Open |
| R-12 | Agent model endpoint not approved | Medium | Medium | Agents run in shadow; rules decide (DL33) | CTO with Enterprise AI | 46332 | Open |
| R-13 | RWB-ACE-001 lands late, or the ACE team does not accept the 14 tables, 12 columns, the batch record and the grant | High | Medium | DL43 estimated and accepted by 21 November; the 16 Section A views go first so the case record can start; a Tier 1-only fallback for the case list is costed | ACE team lead; program manager | 46347 | Open |
| R-14 | Temporal operational skills and on-call load for SCB IT: cluster upgrades, backup and certificates | High | Medium | Name SCB IT as the operator with an on-call rota; the RWB-E1-070 run book covers upgrade, backup, certificate and namespace recovery; drill each in SIT before the Epic 3 build window; RWB-E2-037 and RWB-E2-039 add the alerts and the failover test | SCB IT platform lead | 46353 | Open |
| R-15 | Epic 1 date pressure: the four new configuration stories RWB-E1-070 to RWB-E1-073 must land before the engines | High | High | Start the Temporal and Drools configuration in window 2; pull RWB-E1-070 to RWB-E1-073 before RWB-E1-018, RWB-E1-020 and RWB-E1-021; review burn-down at the weekly sponsor review; keep the engine stories behind their flags if a configuration story slips | Program manager | 46342 | Open |
| R-16 | Drools XLS authoring training for RW-COE | Medium | High | Run the authoring workshop and template guide in RWB-E1-073; coach two package loads before the first live approval; RW-RISK reviews the first three packages; the scenario suite must reach rules.testcases.min before approval | RW-COE lead | 46353 | Open |
| R-17 | The cancelled INC-006 and INC-019 work and its lost build output | Medium | High | Close INC-006 and INC-019 as cancelled under D-RCV-36; keep the branch and build output as reference only; RWB-E1-073 rebuilds the scenario runner, the load checks and the approval path; no reuse without review | Delivery lead | 46346 | Open |
| R-18 | SCB IT has not approved the Temporal server and Java SDK versions or the Drools KIE library versions | High | Medium | Submit the version list in window 1; pin only approved versions; record the approved versions in Environment and Deployment Design v4; DEP-36 tracks the approval and the build does not start the platform stories until it closes | SCB IT architecture | 46342 | Open |

## Assumptions

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

## Issues

| Issues |  |  |  |  |  |
|---|---|---|---|---|---|
| Problems happening now. |  |  |  |  |  |
| ID | Issue | Owner | Needed by | Action | Status |
| I-01 | Two deployment slots planned in DEV are not yet available | ACE team | 46332 | Squads share one slot; tests queued | Open |
| I-02 | Decision owners past their date on DL01 and DL02 | Product owner | 46325 | Escalated to the sponsor review | Open |
| I-03 | CCMS and SVAF layouts not confirmed by the ACE team before RWB-ACE-001 | ACE team | 46347 | ACE team confirms both layouts inside RWB-ACE-001; the Workbench builds no adapter and holds no copy | Open |

## Dependencies

| Dependencies |  |  |  |  |  |  |
|---|---|---|---|---|---|---|
| 36 dependencies from the dependency map, including DEP-36 for the Temporal and Drools version approval. v4, 16 November 2026. |  |  |  |  |  |  |
| ID | On | What is needed | Epic | Needed by | Owner | Decision |
| DEP-01 | ACE team | Recovery module folder, package and boundary test in the ACE repository | E1 | 46328 | ACE team | DL05 |
| DEP-02 | ACE team | Code owners file and merge rules for the recovery module | E1 | 46328 | ACE team | DL04, DL37 |
| DEP-03 | ACE team | Deployment slots: one DEV and one SIT for the recovery squads | E1 | 46332 | ACE team | DL35 |
| DEP-04 | ACE team | Common module services: sign-in, access check, audit and PII logging, the shared case view | E1 | 46335 | ACE team | None |
| DEP-05 | ACE team | Monthly release window and the release owner | E1 | 46339 | SCB IT | DL34 |
| DEP-06 | ACE team | Restructure calculator and plan status from the common module | E2 | 46357 | ACE team with the collection squad | DL14, DL30 |
| DEP-07 | Collection squad | EFS hand-over data and contact history in the COLLINS load | E2 | 46356 | Collection squad with data engineering | DL29 |
| DEP-08 | Collection squad | Shared Epic 2 items: notice path, customer contact stop, shared tasks | E2 | 46356 | IT lead with the product owner | DL30 |
| DEP-09 | Collection squad | TDR and DIL split between the collection squad, the Enterprise AI team and TechX | E3 | 46371 | IT lead | DL14 |
| DEP-10 | Architecture team | Partner access from outside the bank through the external gateway | E5 | 46419 | Architecture team | DL03 |
| DEP-11 | Architecture team | Model endpoint the agents call, inside the SCB tenant | E1 | 46332 | CTO with Enterprise AI | DL33 |
| DEP-12 | Architecture team | Non-functional targets for availability, recovery point and recovery time | E1 | 46339 | Solution architect with Risk | DL11 |
| DEP-13 | Architecture team | Legacy systems kept, changed or retired | E2 | 46346 | IT lead | DL12 |
| DEP-14 | Data engineering | COLLINS load of account, payment, customer and score data into the ACE database for recovery accounts | E1 | 46335 | Data engineering | DL06, DL20 |
| DEP-15 | Data engineering | File layouts and test files for CCMS, SVAF, AMIS, RPS, WIN and GL | E1 | 46339 | Data engineering with the system owners | DL12 |
| DEP-16 | Data engineering | Masked test data in SIT and UAT from the PII service | E1 | 46339 | Data engineering | DL26 |
| DEP-17 | Data engineering | Reconciliation tolerance per data product | E1 | 46339 | Data lead | DL25 |
| DEP-18 | SCB IT security | Entra ID groups for the Workbench roles in each environment | E1 | 46335 | SCB IT security | DL40 |
| DEP-19 | SCB IT security | Access timers: session, inactivity and break-glass | E2 | 46346 | SCB IT security | DL38 |
| DEP-20 | Enterprise AI team | Agent platform: orchestrator, tool gateway, prompt store and evaluation | E1 | 46342 | Enterprise AI team | DL33 |
| DEP-21 | Enterprise AI team | Route return models by route for the route decision | E4 | 46412 | Enterprise AI team with Model Risk | None |
| DEP-22 | Autonomous Ops team | OCR and extraction for the first document types | E1 | 46342 | Autonomous Ops team | DL19 |
| DEP-23 | Business | Delegation of authority: holders, limits and substitutes | E2 | 46356 | Risk with the product heads | DL18 |
| DEP-24 | Business | Service levels per case state and caseload caps | E2 | 46339 | Business lead; product owner | DL22, DL23 |
| DEP-25 | Business | Letter templates approved by Legal in Thai and English | E2 | 46339 | Legal counsel | DL28 |
| DEP-26 | Business | Business testers named for each release | E1 | 46332 | Business lead | DL09 |
| DEP-27 | Business | Thai labels and message wording | E2 | 46331 | Business lead with Legal and Compliance | DL10 |
| DEP-28 | Partners | Panel law firms onboarded to the partner portal with user accounts | E5 | 46447 | Partner and agency manager | DL03 |
| DEP-29 | Partners | Valuers, auction vendors and RAMC onboarded to the partner portal | E4 | 46419 | Partner and agency manager; Head of Asset Liquidity | DL03 |
| DEP-30 | Partners | Debt buyers' data room access and confidentiality agreements | E5 | 46447 | Head of Asset Liquidity | DL03 |
| DEP-31 | Partners | Collection agencies onboarded with placement and outcome capture | E6 | 46478 | Partner and agency manager | DL03 |
| DEP-32 | Business | TCG claim rules and the guarantee quota | E4 | 46412 | Guarantee officer | None |
| DEP-33 | Business | Write-off tax criteria version from Finance | E6 | 46468 | Finance and CFO delegate | None |
| DEP-34 | ACE team | RWB-ACE-001: 14 tables, 12 columns, one batch record per source and business date and the SELECT grant that the 30 recovery.v_ace_* views read | E1 | 46347 | ACE team lead | DL43 |
| DEP-35 | ACE team | DL43: the ACE team's estimate and acceptance of RWB-ACE-001, with the 14 ingestion jobs and the migration window in the 30 November release named | E1 | 46347 | Sponsor with the ACE team lead | DL43 |
| DEP-36 | SCB IT | SCB IT approves the Temporal server and Java SDK versions and the Drools KIE library versions before the build window | E1 | 46342 | SCB IT architecture | D-RCV-36 |
