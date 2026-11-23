<!-- source: 11 Delivery and operations/Recovery Workbench Dependency Map v4.xlsx -->
<!-- converted: 2026-11-16 from XLSX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Dependency Map v4.xlsx`  
> **Converted from:** XLSX

## Dependencies

| Dependencies outside the recovery squads |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|
| 36 dependencies on the ACE team, the collection squad, the architecture team, data engineering, SCB IT security, the AI teams, the business and the partners. DEP-34 and DEP-35 carry the ACE delivery and DL43, added on 15 November 2026. DEP-36 adds the Temporal and Drools version approval, added on 16 November 2026. v4, 16 November 2026. |  |  |  |  |  |  |  |  |
| ID | On | What is needed | For epic | Needed by | Owner | Decision | If late | Status |
| DEP-01 | ACE team | Recovery module folder, package and boundary test in the ACE repository | E1 | 46328 | ACE team | DL05 | The squads cannot merge into ACE | Open |
| DEP-02 | ACE team | Code owners file and merge rules for the recovery module | E1 | 46328 | ACE team | DL04, DL37 | Reviews stall and changes cross module folders | Open |
| DEP-03 | ACE team | Deployment slots: one DEV and one SIT for the recovery squads | E1 | 46332 | ACE team | DL35 | Squads queue for one slot and SIT runs late | Open |
| DEP-04 | ACE team | Common module services: sign-in, access check, audit and PII logging, the shared case view | E1 | 46335 | ACE team | None | Every screen and service waits for the access check | Open |
| DEP-05 | ACE team | Monthly release window and the release owner | E1 | 46339 | SCB IT | DL34 | The first release date moves | Open |
| DEP-06 | ACE team | Restructure calculator and plan status from the common module | E2 | 46357 | ACE team with the collection squad | DL14, DL30 | The treatment record shows no live plan | Open |
| DEP-07 | Collection squad | EFS hand-over data and contact history in the COLLINS load | E2 | 46356 | Collection squad with data engineering | DL29 | Cases start with no collections history | Open |
| DEP-08 | Collection squad | Shared Epic 2 items: notice path, customer contact stop, shared tasks | E2 | 46356 | IT lead with the product owner | DL30 | Both squads build the same item | Open |
| DEP-09 | Collection squad | TDR and DIL split between the collection squad, the Enterprise AI team and TechX | E3 | 46371 | IT lead | DL14 | Epic 3 has no confirmed builder | Open |
| DEP-10 | Architecture team | Partner access from outside the bank through the external gateway | E5 | 46419 | Architecture team | DL03 | Law firms cannot use the partner portal at Epic 5 | Open |
| DEP-11 | Architecture team | Model endpoint the agents call, inside the SCB tenant | E1 | 46332 | CTO with Enterprise AI | DL33 | The agent runtime cannot run in shadow | Open |
| DEP-12 | Architecture team | Non-functional targets for availability, recovery point and recovery time | E1 | 46339 | Solution architect with Risk | DL11 | Sizing and tests run against proposed values | Open |
| DEP-13 | Architecture team | Legacy systems kept, changed or retired | E2 | 46346 | IT lead | DL12 | Interfaces are built for systems that may be retired | Open |
| DEP-14 | Data engineering | ACE ingestion of account, payment, customer and score data complete for the business date, read through v_ace_account, v_ace_payment, v_ace_customer and v_ace_score; no Workbench load and no staging table | E1 | 46335 | Data engineering | DL06, DL20 | No case can be opened from the ACE account view for the business date | Open |
| DEP-15 | Data engineering | File layouts and test files for CCMS, SVAF, AMIS, RPS, WIN and GL | E1 | 46339 | Data engineering with the system owners | DL12 | File loads are built against assumed layouts | Open |
| DEP-16 | Data engineering | Masked test data in SIT and UAT from the PII service | E1 | 46339 | Data engineering | DL26 | SIT and UAT run on synthetic data only | Open |
| DEP-17 | Data engineering | Reconciliation tolerance per data product | E1 | 46339 | Data lead | DL25 | Loads are checked without agreed tolerances | Open |
| DEP-18 | SCB IT security | Entra ID groups for the Workbench roles in each environment | E1 | 46335 | SCB IT security | DL40 | No one can sign in to SIT or UAT | Open |
| DEP-19 | SCB IT security | Access timers: session, inactivity and break-glass | E2 | 46346 | SCB IT security | DL38 | Session rules use the ACE defaults | Open |
| DEP-20 | Enterprise AI team | Agent platform: orchestrator, tool gateway, prompt store and evaluation | E1 | 46342 | Enterprise AI team | DL33 | Agents stay off; the rule result is used | Open |
| DEP-21 | Enterprise AI team | Route return models by route for the route decision | E4 | 46412 | Enterprise AI team with Model Risk | None | The route decision runs on rules only | Open |
| DEP-22 | Autonomous Ops team | OCR and extraction for the first document types | E1 | 46342 | Autonomous Ops team | DL19 | Documents are stored without extracted fields | Open |
| DEP-23 | Business | Delegation of authority: holders, limits and substitutes | E2 | 46356 | Risk with the product heads | DL18 | Approval routing uses provisional limits | Open |
| DEP-24 | Business | Service levels per case state and caseload caps | E2 | 46339 | Business lead; product owner | DL22, DL23 | Timers and caps load as placeholders | Open |
| DEP-25 | Business | Letter templates approved by Legal in Thai and English | E2 | 46339 | Legal counsel | DL28 | Notices cannot be generated | Open |
| DEP-26 | Business | Business testers named for each release | E1 | 46332 | Business lead | DL09 | UAT has no testers | Open |
| DEP-27 | Business | Thai labels and message wording | E2 | 46331 | Business lead with Legal and Compliance | DL10 | Screens release with English labels only | Open |
| DEP-28 | Partners | Panel law firms onboarded to the partner portal with user accounts | E5 | 46447 | Partner and agency manager | DL03 | Instructions go by email for another month | Open |
| DEP-29 | Partners | Valuers, auction vendors and RAMC onboarded to the partner portal | E4 | 46419 | Partner and agency manager; Head of Asset Liquidity | DL03 | Results are keyed by bank staff | Open |
| DEP-30 | Partners | Debt buyers' data room access and confidentiality agreements | E5 | 46447 | Head of Asset Liquidity | DL03 | Lot data goes by file transfer | Open |
| DEP-31 | Partners | Collection agencies onboarded with placement and outcome capture | E6 | 46478 | Partner and agency manager | DL03 | Agency placements stay on spreadsheets | Open |
| DEP-32 | Business | TCG claim rules and the guarantee quota | E4 | 46412 | Guarantee officer | None | Claims are tracked by hand | Open |
| DEP-33 | Business | Write-off tax criteria version from Finance | E6 | 46468 | Finance and CFO delegate | None | The write-off scan holds (R-WO-03) | Open |
| DEP-34 | ACE team | RWB-ACE-001: 14 tables, 12 columns, one batch record per source and business date and the SELECT grant that the 30 recovery.v_ace_* views read | E1 | 46347 | ACE team lead | DL43 | RWB-E1-069 has only the 16 Section A views; the case list, the case record and the 12 ACE columns are missing, so the 30 November release moves | Open |
| DEP-35 | ACE team | DL43: the ACE team's estimate and acceptance of RWB-ACE-001, with the 14 ingestion jobs and the migration window in the 30 November release named | E1 | 46347 | Sponsor with the ACE team lead | DL43 | The ACE additions have no committed date; the plan holds the 21 November assumption and moves if it slips | Open |
| DEP-36 | SCB IT | SCB IT approves the Temporal server and Java SDK versions and the Drools KIE library versions before the build window | E1 | 46342 | SCB IT architecture | D-RCV-36 | The build pins no Temporal or Drools version and RWB-E1-070, RWB-E1-072 and RWB-E2-042 cannot start | Open |

## Story dependencies

| Story dependencies |  |  |
|---|---|---|
| 325 story-level dependencies, rebuilt from the Dependencies sheets of Recovery Workbench User Stories Epic 1 v9, Epic 2 v7 and Technical Enabler Stories v7 on 16 November 2026. Each row is one dependency; the story on the right is finished first. Rows that named RWB-E1-029, RWB-TE-005 or RWB-E1-048 are replaced by RWB-E1-073 or RWB-E2-041. v4. |  |  |
| Story | Title | Depends on |
| RWB-E1-001 | Recovery tables for the 14 data products | RWB-E1-043 |
| RWB-E1-001 | Recovery tables for the 14 data products | RWB-E1-044 |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | RWB-E1-007 |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | RWB-E1-015 |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | RWB-E1-018 |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | RWB-E1-020 |
| RWB-E1-002 | Case list v1 with case ID, owner and queue | RWB-E1-069 |
| RWB-E1-007 | Integration adapters for outbound files | RWB-E1-001 |
| RWB-E1-007 | Integration adapters for outbound files | RWB-E1-015 |
| RWB-E1-007 | Integration adapters for outbound files | RWB-E1-069 |
| RWB-E1-008 | Decision log store v1, append only and hash chained | RWB-E1-001 |
| RWB-E1-011 | Reconciliation and data quality report | RWB-E1-002 |
| RWB-E1-011 | Reconciliation and data quality report | RWB-E1-015 |
| RWB-E1-011 | Reconciliation and data quality report | RWB-E1-069 |
| RWB-E1-013 | Baseline measures | RWB-E1-018 |
| RWB-E1-013 | Baseline measures | RWB-E1-043 |
| RWB-E1-014 | Decision log copy to the data lake | RWB-E1-017 |
| RWB-E1-014 | Decision log copy to the data lake | RWB-E1-056 |
| RWB-E1-015 | Freshness stamp per data product | RWB-E1-001 |
| RWB-E1-015 | Freshness stamp per data product | RWB-E1-027 |
| RWB-E1-015 | Freshness stamp per data product | RWB-E1-069 |
| RWB-E1-016 | Access control per data product and catalog entries | RWB-E1-001 |
| RWB-E1-016 | Access control per data product and catalog entries | RWB-E1-037 |
| RWB-E1-016 | Access control per data product and catalog entries | RWB-E1-064 |
| RWB-E1-016 | Access control per data product and catalog entries | RWB-E1-069 |
| RWB-E1-017 | Retention and archive rule for the data store | RWB-E1-001 |
| RWB-E1-017 | Retention and archive rule for the data store | RWB-E1-043 |
| RWB-E1-017 | Retention and archive rule for the data store | RWB-E1-064 |
| RWB-E1-017 | Retention and archive rule for the data store | RWB-TE-012 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-001 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-016 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-027 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-042 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-069 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-072 |
| RWB-E1-018 | Case ID issuance and case record v1 | RWB-E1-073 |
| RWB-E1-019 | Roles, teams and queues as data | RWB-E1-038 |
| RWB-E1-019 | Roles, teams and queues as data | RWB-E1-043 |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-E1-018 |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-E1-019 |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-E1-027 |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-E1-056 |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-E1-072 |
| RWB-E1-020 | Allocation and assignment engine v1 | RWB-E1-073 |
| RWB-E1-021 | Transfer rules and engine v1 | RWB-E1-020 |
| RWB-E1-021 | Transfer rules and engine v1 | RWB-E1-027 |
| RWB-E1-021 | Transfer rules and engine v1 | RWB-E1-028 |
| RWB-E1-021 | Transfer rules and engine v1 | RWB-E1-072 |
| RWB-E1-021 | Transfer rules and engine v1 | RWB-E1-073 |
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | RWB-E1-001 |
| RWB-E1-022 | Sign-on with SSO, MFA and the first roles | RWB-E1-019 |
| RWB-E1-023 | Case record view v1, read only | RWB-E1-018 |
| RWB-E1-023 | Case record view v1, read only | RWB-E1-024 |
| RWB-E1-023 | Case record view v1, read only | RWB-E1-037 |
| RWB-E1-023 | Case record view v1, read only | RWB-E1-039 |
| RWB-E1-023 | Case record view v1, read only | RWB-E1-068 |
| RWB-E1-023 | Case record view v1, read only | RWB-E1-069 |
| RWB-E1-024 | Document store and index | RWB-E1-001 |
| RWB-E1-024 | Document store and index | RWB-E1-018 |
| RWB-E1-024 | Document store and index | RWB-E1-025 |
| RWB-E1-024 | Document store and index | RWB-E1-027 |
| RWB-E1-024 | Document store and index | RWB-TE-012 |
| RWB-E1-025 | Document types and fields agreed | RWB-E1-069 |
| RWB-E1-026 | Attach and search screen | RWB-E1-024 |
| RWB-E1-026 | Attach and search screen | RWB-E1-025 |
| RWB-E1-026 | Attach and search screen | RWB-E1-030 |
| RWB-E1-026 | Attach and search screen | RWB-E1-041 |
| RWB-E1-026 | Attach and search screen | RWB-E1-045 |
| RWB-E1-027 | Decision log writer v1 | RWB-E1-008 |
| RWB-E1-027 | Decision log writer v1 | RWB-E1-056 |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | RWB-E1-020 |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | RWB-E1-027 |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | RWB-E1-043 |
| RWB-E1-028 | Service levels, timers, escalation and prescription dates | RWB-E1-045 |
| RWB-E1-030 | Daily rebalancing and queue measures | RWB-E1-020 |
| RWB-E1-030 | Daily rebalancing and queue measures | RWB-E1-027 |
| RWB-E1-030 | Daily rebalancing and queue measures | RWB-E1-028 |
| RWB-E1-031 | Queue and owner on the case list with filters | RWB-E1-020 |
| RWB-E1-031 | Queue and owner on the case list with filters | RWB-E1-039 |
| RWB-E1-032 | Automatic attach from the OCR intake | RWB-E1-024 |
| RWB-E1-032 | Automatic attach from the OCR intake | RWB-E1-050 |
| RWB-E1-032 | Automatic attach from the OCR intake | RWB-E1-053 |
| RWB-E1-033 | Search across cases | RWB-E1-024 |
| RWB-E1-033 | Search across cases | RWB-E1-049 |
| RWB-E1-033 | Search across cases | RWB-E1-053 |
| RWB-E1-034 | Letter template management | RWB-E1-015 |
| RWB-E1-034 | Letter template management | RWB-E1-046 |
| RWB-E1-035 | Case record view v1.1 with documents and history timeline | RWB-E1-021 |
| RWB-E1-035 | Case record view v1.1 with documents and history timeline | RWB-E1-023 |
| RWB-E1-035 | Case record view v1.1 with documents and history timeline | RWB-E1-027 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | RWB-E1-022 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | RWB-E1-027 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | RWB-E1-043 |
| RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | RWB-E1-069 |
| RWB-E1-038 | Delegation of authority table as reference data | RWB-E1-027 |
| RWB-E1-038 | Delegation of authority table as reference data | RWB-E1-043 |
| RWB-E1-039 | Access log into the decision log and break-glass admin | RWB-E1-008 |
| RWB-E1-039 | Access log into the decision log and break-glass admin | RWB-E1-022 |
| RWB-E1-039 | Access log into the decision log and break-glass admin | RWB-E1-027 |
| RWB-E1-040 | Document checklist per case type as reference data | RWB-E1-024 |
| RWB-E1-040 | Document checklist per case type as reference data | RWB-E1-025 |
| RWB-E1-040 | Document checklist per case type as reference data | RWB-E1-026 |
| RWB-E1-040 | Document checklist per case type as reference data | RWB-E1-043 |
| RWB-E1-041 | Retention classes and virus scan on intake | RWB-E1-024 |
| RWB-E1-041 | Retention classes and virus scan on intake | RWB-E1-049 |
| RWB-E1-042 | Central configuration service and parameter catalog | RWB-E1-044 |
| RWB-E1-043 | Reference data service with versioned tables | RWB-E1-042 |
| RWB-E1-043 | Reference data service with versioned tables | RWB-E1-044 |
| RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | RWB-E1-042 |
| RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | RWB-E1-043 |
| RWB-E1-046 | Template and merge field catalog as data | RWB-E1-001 |
| RWB-E1-046 | Template and merge field catalog as data | RWB-E1-069 |
| RWB-E1-047 | Feature flags for module release with a removal date | RWB-E1-001 |
| RWB-E1-049 | OCR pipeline on the Workbench document hub | RWB-E1-024 |
| RWB-E1-049 | OCR pipeline on the Workbench document hub | RWB-E1-045 |
| RWB-E1-049 | OCR pipeline on the Workbench document hub | RWB-TE-012 |
| RWB-E1-050 | Document classification | RWB-E1-025 |
| RWB-E1-050 | Document classification | RWB-E1-049 |
| RWB-E1-052 | Notice generation v1 | RWB-E1-015 |
| RWB-E1-052 | Notice generation v1 | RWB-E1-018 |
| RWB-E1-052 | Notice generation v1 | RWB-E1-027 |
| RWB-E1-052 | Notice generation v1 | RWB-E1-046 |
| RWB-E1-052 | Notice generation v1 | RWB-E1-069 |
| RWB-E1-053 | Field extraction for the six types into the index | RWB-E1-025 |
| RWB-E1-053 | Field extraction for the six types into the index | RWB-E1-049 |
| RWB-E1-053 | Field extraction for the six types into the index | RWB-E1-050 |
| RWB-E1-054 | Review queue for low-confidence documents | RWB-E1-032 |
| RWB-E1-054 | Review queue for low-confidence documents | RWB-E1-035 |
| RWB-E1-054 | Review queue for low-confidence documents | RWB-E1-049 |
| RWB-E1-054 | Review queue for low-confidence documents | RWB-E1-050 |
| RWB-E1-054 | Review queue for low-confidence documents | RWB-E1-053 |
| RWB-E1-055 | Proof of delivery capture design with WIN | RWB-E1-028 |
| RWB-E1-055 | Proof of delivery capture design with WIN | RWB-E1-052 |
| RWB-E1-055 | Proof of delivery capture design with WIN | RWB-E1-054 |
| RWB-E1-055 | Proof of delivery capture design with WIN | RWB-E1-066 |
| RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | RWB-E1-007 |
| RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | RWB-E1-015 |
| RWB-E1-056 | Run books and monitoring for every Epic 1 Workbench job | RWB-E1-069 |
| RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | RWB-E1-041 |
| RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | RWB-E1-049 |
| RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | RWB-TE-012 |
| RWB-E1-058 | Agent platform set-up [E1a] | RWB-E1-001 |
| RWB-E1-058 | Agent platform set-up [E1a] | RWB-E1-037 |
| RWB-E1-058 | Agent platform set-up [E1a] | RWB-E1-069 |
| RWB-E1-059 | Case intake agent in shadow [E1b] | RWB-E1-030 |
| RWB-E1-059 | Case intake agent in shadow [E1b] | RWB-E1-058 |
| RWB-E1-059 | Case intake agent in shadow [E1b] | RWB-TE-013 |
| RWB-E1-060 | Extraction evaluation [E1c] | RWB-E1-053 |
| RWB-E1-060 | Extraction evaluation [E1c] | RWB-E1-058 |
| RWB-E1-061 | Intake agent evaluation and L1 proposal [E2a] | RWB-E1-059 |
| RWB-E1-062 | Deviation screening agent in shadow [E2b] | RWB-E1-058 |
| RWB-E1-062 | Deviation screening agent in shadow [E2b] | RWB-TE-013 |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | RWB-E1-007 |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | RWB-E1-014 |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | RWB-E1-058 |
| RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | RWB-E1-061 |
| RWB-E1-064 | Data dictionary for the 14 data products | RWB-E1-001 |
| RWB-E1-064 | Data dictionary for the 14 data products | RWB-E1-043 |
| RWB-E1-064 | Data dictionary for the 14 data products | RWB-E1-069 |
| RWB-E1-065 | Sandbox database with synthetic recovery data | RWB-E1-001 |
| RWB-E1-065 | Sandbox database with synthetic recovery data | RWB-E1-069 |
| RWB-E1-066 | Interaction ledger store and writer | RWB-E1-018 |
| RWB-E1-066 | Interaction ledger store and writer | RWB-E1-027 |
| RWB-E1-067 | Every Workbench action into the interaction ledger | RWB-E1-066 |
| RWB-E1-068 | Interaction ledger read interface | RWB-E1-066 |
| RWB-E1-069 | Read-only ACE source views, grants and boundary rule | RWB-ACE-001 |
| RWB-E1-069 | Read-only ACE source views, grants and boundary rule | RWB-E1-001 |
| RWB-E1-070 | Temporal platform on the ACE AKS clusters | RWB-E1-022 |
| RWB-E1-070 | Temporal platform on the ACE AKS clusters | RWB-E1-044 |
| RWB-E1-070 | Temporal platform on the ACE AKS clusters | RWB-E1-056 |
| RWB-E1-071 | Temporal worker and SDK in the recovery module | RWB-E1-042 |
| RWB-E1-071 | Temporal worker and SDK in the recovery module | RWB-E1-047 |
| RWB-E1-071 | Temporal worker and SDK in the recovery module | RWB-E1-070 |
| RWB-E1-071 | Temporal worker and SDK in the recovery module | RWB-TE-001 |
| RWB-E1-072 | Drools runtime and rule package store | RWB-E1-027 |
| RWB-E1-072 | Drools runtime and rule package store | RWB-E1-043 |
| RWB-E1-072 | Drools runtime and rule package store | RWB-E1-044 |
| RWB-E1-073 | Rule authoring, validation, test scenarios, approval and rollback in Drools | RWB-E1-042 |
| RWB-E1-073 | Rule authoring, validation, test scenarios, approval and rollback in Drools | RWB-E1-072 |
| RWB-E2-001 | EFS hand-over with full history | RWB-E1-007 |
| RWB-E2-001 | EFS hand-over with full history | RWB-E1-015 |
| RWB-E2-001 | EFS hand-over with full history | RWB-E1-069 |
| RWB-E2-002 | ACE plan status on the case | RWB-E1-072 |
| RWB-E2-002 | ACE plan status on the case | RWB-E2-001 |
| RWB-E2-002 | ACE plan status on the case | RWB-E2-042 |
| RWB-E2-003 | Customer's other products on the case | RWB-E1-007 |
| RWB-E2-003 | Customer's other products on the case | RWB-E1-069 |
| RWB-E2-004 | Treatment entity and plan timers data model | RWB-E1-018 |
| RWB-E2-004 | Treatment entity and plan timers data model | RWB-E1-028 |
| RWB-E2-004 | Treatment entity and plan timers data model | RWB-E1-045 |
| RWB-E2-004 | Treatment entity and plan timers data model | RWB-E1-072 |
| RWB-E2-004 | Treatment entity and plan timers data model | RWB-E2-042 |
| RWB-E2-005 | Decision log query API for audit | RWB-E1-008 |
| RWB-E2-005 | Decision log query API for audit | RWB-E1-039 |
| RWB-E2-005 | Decision log query API for audit | RWB-E2-041 |
| RWB-E2-006 | Credit approval pack for NLEADS | RWB-E1-007 |
| RWB-E2-006 | Credit approval pack for NLEADS | RWB-E2-004 |
| RWB-E2-007 | Booking confirmation from the ALS load | RWB-E1-007 |
| RWB-E2-007 | Booking confirmation from the ALS load | RWB-E1-069 |
| RWB-E2-007 | Booking confirmation from the ALS load | RWB-E1-072 |
| RWB-E2-007 | Booking confirmation from the ALS load | RWB-E2-004 |
| RWB-E2-007 | Booking confirmation from the ALS load | RWB-E2-042 |
| RWB-E2-008 | Payment matching with the missed payment event | RWB-E1-069 |
| RWB-E2-008 | Payment matching with the missed payment event | RWB-E1-072 |
| RWB-E2-008 | Payment matching with the missed payment event | RWB-E2-004 |
| RWB-E2-008 | Payment matching with the missed payment event | RWB-E2-042 |
| RWB-E2-009 | Steering dashboard v1 data set | RWB-E1-013 |
| RWB-E2-009 | Steering dashboard v1 data set | RWB-E1-063 |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | RWB-E1-015 |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | RWB-E1-016 |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | RWB-E1-069 |
| RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | RWB-E2-004 |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | RWB-E1-020 |
| RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | RWB-E1-031 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | RWB-E1-021 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | RWB-E1-072 |
| RWB-E2-012 | Manual transfer and reassignment screen with reason | RWB-E2-011 |
| RWB-E2-013 | Approval routing with the delegation of authority table | RWB-E1-027 |
| RWB-E2-013 | Approval routing with the delegation of authority table | RWB-E1-028 |
| RWB-E2-013 | Approval routing with the delegation of authority table | RWB-E1-037 |
| RWB-E2-013 | Approval routing with the delegation of authority table | RWB-E1-038 |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | RWB-E1-052 |
| RWB-E2-014 | Approval screen for D7.1 demand and recall notices | RWB-E2-013 |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | RWB-E1-028 |
| RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | RWB-E1-035 |
| RWB-E2-016 | Full case record view with the history timeline | RWB-E1-035 |
| RWB-E2-016 | Full case record view with the history timeline | RWB-E2-012 |
| RWB-E2-016 | Full case record view with the history timeline | RWB-E2-015 |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | RWB-E1-034 |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | RWB-E1-054 |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | RWB-E2-026 |
| RWB-E2-017 | Contract, CA and mortgage document generation screens | RWB-TE-012 |
| RWB-E2-018 | E-signature flow for customers and the bank | RWB-E2-017 |
| RWB-E2-018 | E-signature flow for customers and the bank | RWB-E2-022 |
| RWB-E2-019 | Partner identities through the external gateway | RWB-E1-022 |
| RWB-E2-019 | Partner identities through the external gateway | RWB-E1-037 |
| RWB-E2-019 | Partner identities through the external gateway | RWB-E1-039 |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | RWB-E1-052 |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | RWB-E1-055 |
| RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | RWB-E2-014 |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | RWB-E1-052 |
| RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | RWB-E1-066 |
| RWB-E2-024 | Field app photos and bills into the document hub | RWB-E1-024 |
| RWB-E2-024 | Field app photos and bills into the document hub | RWB-E1-032 |
| RWB-E2-024 | Field app photos and bills into the document hub | RWB-E1-041 |
| RWB-E2-024 | Field app photos and bills into the document hub | RWB-E1-053 |
| RWB-E2-024 | Field app photos and bills into the document hub | RWB-E1-057 |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | RWB-E1-050 |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | RWB-E1-053 |
| RWB-E2-025 | Extraction for the stage 2 and 3 document types | RWB-E1-054 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | RWB-E1-024 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | RWB-E1-027 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | RWB-E1-034 |
| RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | RWB-E1-046 |
| RWB-E2-027 | Payment matching rules with the data team | RWB-E2-008 |
| RWB-E2-027 | Payment matching rules with the data team | RWB-E2-042 |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | RWB-E1-027 |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | RWB-E1-035 |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | RWB-E1-061 |
| RWB-E2-028 | Case intake agent live at L1 [E3a] | RWB-E2-031 |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | RWB-E1-061 |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | RWB-E1-062 |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | RWB-E2-015 |
| RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | RWB-E2-028 |
| RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | RWB-E1-058 |
| RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | RWB-E1-061 |
| RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | RWB-E2-025 |
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | RWB-E1-063 |
| RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | RWB-E2-005 |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | RWB-E1-027 |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | RWB-E1-058 |
| RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | RWB-E2-004 |
| RWB-E2-033 | Case and queue list with status, owner and ageing | RWB-E1-018 |
| RWB-E2-033 | Case and queue list with status, owner and ageing | RWB-E1-031 |
| RWB-E2-033 | Case and queue list with status, owner and ageing | RWB-E2-011 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-E1-007 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-E1-027 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-E1-066 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-E1-067 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-E1-069 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-E2-016 |
| RWB-E2-034 | Interaction ledger on the case and from every channel | RWB-TE-006 |
| RWB-E2-035 | Next action on the case | RWB-E1-018 |
| RWB-E2-035 | Next action on the case | RWB-E1-031 |
| RWB-E2-035 | Next action on the case | RWB-E1-072 |
| RWB-E2-035 | Next action on the case | RWB-E2-033 |
| RWB-E2-035 | Next action on the case | RWB-E2-042 |
| RWB-E2-036 | Queue write interface for models and agents | RWB-E1-019 |
| RWB-E2-036 | Queue write interface for models and agents | RWB-E1-020 |
| RWB-E2-036 | Queue write interface for models and agents | RWB-E1-027 |
| RWB-E2-037 | Temporal observability and run books | RWB-E1-056 |
| RWB-E2-037 | Temporal observability and run books | RWB-E1-070 |
| RWB-E2-037 | Temporal observability and run books | RWB-E1-071 |
| RWB-E2-038 | Temporal security, codec server and admin audit | RWB-E1-039 |
| RWB-E2-038 | Temporal security, codec server and admin audit | RWB-E1-070 |
| RWB-E2-038 | Temporal security, codec server and admin audit | RWB-E1-071 |
| RWB-E2-039 | Temporal resilience: backup, failover, upgrade and archive | RWB-E1-070 |
| RWB-E2-039 | Temporal resilience: backup, failover, upgrade and archive | RWB-E2-037 |
| RWB-E2-040 | Workflow versioning and replay test gate | RWB-E1-071 |
| RWB-E2-041 | Rule change governance and audit report | RWB-E1-037 |
| RWB-E2-041 | Rule change governance and audit report | RWB-E1-073 |
| RWB-E2-042 | Epic 2 rule packages in Drools | RWB-E1-073 |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | RWB-E1-071 |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | RWB-E1-072 |
| RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | RWB-TE-006 |
| RWB-TE-002 | Code owners for the recovery module | RWB-TE-001 |
| RWB-TE-003 | Types and contract tests from the API specification | RWB-TE-001 |
| RWB-TE-004 | Masked data in SIT and UAT | RWB-E1-037 |
| RWB-TE-004 | Masked data in SIT and UAT | RWB-E1-065 |
| RWB-TE-004 | Masked data in SIT and UAT | RWB-E1-069 |
| RWB-TE-006 | Outbox and retry for outbound work | RWB-E1-007 |
| RWB-TE-006 | Outbox and retry for outbound work | RWB-E1-027 |
| RWB-TE-006 | Outbox and retry for outbound work | RWB-E1-044 |
| RWB-TE-007 | Scheduled jobs on Quartz | RWB-E1-028 |
| RWB-TE-007 | Scheduled jobs on Quartz | RWB-E1-044 |
| RWB-TE-007 | Scheduled jobs on Quartz | RWB-E1-056 |
| RWB-TE-008 | Decision log hash chain check | RWB-E1-008 |
| RWB-TE-008 | Decision log hash chain check | RWB-TE-007 |
| RWB-TE-009 | Performance test harness | RWB-TE-004 |
| RWB-TE-010 | Browser and accessibility tests | RWB-TE-003 |
| RWB-TE-011 | PDPA lint for code, tests and logs | RWB-TE-001 |
| RWB-TE-012 | Document storage containers | RWB-TE-001 |
| RWB-TE-013 | Agent runtime client with fallback | RWB-E1-027 |
| RWB-TE-013 | Agent runtime client with fallback | RWB-E1-058 |
| RWB-TE-013 | Agent runtime client with fallback | RWB-TE-007 |

## By team and epic

| Dependencies by team and epic |  |  |  |  |  |  |  |  |  |
|---|---|---|---|---|---|---|---|---|---|
| Count of dependencies each team must meet before each epic. v4, 16 November 2026. |  |  |  |  |  |  |  |  |  |
| On | E1 | E2 | E3 | E4 | E5 | E6 | E7 | E8 | Total |
| ACE team | 7 | 1 |  |  |  |  |  |  | 8 |
| Architecture team | 2 | 1 |  |  | 1 |  |  |  | 4 |
| Autonomous Ops team | 1 |  |  |  |  |  |  |  | 1 |
| Business | 1 | 4 |  | 1 |  | 1 |  |  | 7 |
| Collection squad |  | 2 | 1 |  |  |  |  |  | 3 |
| Data engineering | 4 |  |  |  |  |  |  |  | 4 |
| Enterprise AI team | 1 |  |  | 1 |  |  |  |  | 2 |
| Partners |  |  |  | 1 | 2 | 1 |  |  | 4 |
| SCB IT security | 2 | 1 |  |  |  |  |  |  | 3 |
| Total | 18 | 9 | 1 | 3 | 3 | 2 | 0 | 0 | 36 |

## How they are tracked

| How dependencies are tracked |  |
|---|---|
| Applies to every row. |  |
| Step | What happens |
| 1 | Each dependency has one owner outside the squads and a date |
| 2 | The program manager reviews open dependencies every week with each owner |
| 3 | A dependency late by more than five working days goes to the sponsor review with its effect on the release |
| 4 | A dependency tied to a decision closes when the decision is taken in the decision log |
| 5 | Where a dependency is late, the squads build on the stated assumption behind a flag |
