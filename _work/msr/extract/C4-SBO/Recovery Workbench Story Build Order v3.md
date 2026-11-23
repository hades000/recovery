Recovery Workbench story build order

E2E Recovery Workbench. SCB Collections and Recovery. Henka Group, 16 November 2026. v3.

The order the 115 items are built in, from Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx. The story numbers are a catalog, not an order: RWB-E1-001 depends on RWB-E1-043 and RWB-E1-044, which are built before it. Pull the next item whose dependencies are done. E is an enabler, S is a user story. Waits on names the items that must finish first, by their number within the same family. RWB-ACE-001 is the ACE team's delivery and is not pulled by either squad; it gates RWB-E1-069.

D-RCV-36. This version applies decision D-RCV-36. Temporal runs the case lifecycle from Epic 3, with case data in the ACE database, and Drools evaluates rules from versioned rule packages. RWB-E1-029, RWB-TE-005 and RWB-E1-048 are retired; their work moved to RWB-E1-073 and RWB-E2-041. The new configuration stories are RWB-E1-070 to RWB-E1-073 and RWB-E2-037 to RWB-E2-043.

Why configuration comes first. The Epic 1 configuration stories RWB-E1-070 to RWB-E1-073 build the Temporal platform, the worker, the Drools runtime and the rule authoring path before RWB-E1-018, RWB-E1-020 and RWB-E1-021, because those engines call RuleEvaluator and write the package version to the decision log. The Epic 2 stories do the same before the engines: RWB-E2-042 loads the RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH packages before RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008 and RWB-E2-027, and RWB-E2-043 sets the integration pattern before Epic 3.

Window 1, 2 to 13 November 2026

15 items, releasing in Epic 1.

| # | Key | Title | Module | E or S | Waits on |
|---|---|---|---|---|---|
| 1 | RWB-E1-044 | Database migrations versioned with parameterized schema names | P3 | E | None |
| 2 | RWB-TE-001 | Recovery module folder and boundary test | P2 | E | None |
| 3 | RWB-E1-042 | Central configuration service and parameter catalog | P3 | E | E1-044 |
| 4 | RWB-TE-002 | Code owners for the recovery module | P2 | E | TE-001 |
| 5 | RWB-TE-003 | Types and contract tests from the API specification | P2 | E | TE-001 |
| 6 | RWB-TE-011 | PDPA lint for code, tests and logs | P2 | E | TE-001 |
| 7 | RWB-TE-012 | Document storage containers | P5 | E | TE-001 |
| 8 | RWB-E1-043 | Reference data service with versioned tables | P3 | E | E1-042, E1-044 |
| 9 | RWB-E1-001 | Recovery tables for the 14 data products | P1 | S | E1-044, E1-043 |
| 10 | RWB-E1-069 | Read-only ACE source views, grants and boundary rule | P1 | S | E1-001, ACE-001 |
| 11 | RWB-E1-007 | Integration adapters for outbound files | P2 | S | E1-001, E1-069 |
| 12 | RWB-E1-008 | Decision log store v1, append only and hash chained | P7 | S | E1-001 |
| 13 | RWB-E1-064 | Data dictionary for the 14 data products | P1 | E | E1-001, E1-043, E1-069 |
| 14 | RWB-E1-065 | Sandbox database with synthetic recovery data | P1 | E | E1-001, E1-069 |
| 15 | RWB-TE-004 | Masked data in SIT and UAT | P1 | E | E1-065 |


Window 2, 16 to 27 November 2026

57 items, releasing in Epic 1.

| # | Key | Title | Module | E or S | Waits on |
|---|---|---|---|---|---|
| 16 | RWB-E1-047 | Feature flags for module release with a removal date | P2 | S | E1-001 |
| 17 | RWB-E1-017 | Retention and archive rule for the data store | P1 | S | E1-001, E1-043, TE-012, E1-064 |
| 18 | RWB-E1-056 | Run books and monitoring for every Epic 1 job | P2 | E | E1-007 |
| 19 | RWB-E1-014 | Decision log copy to the data lake | P1 | S | E1-056, E1-017 |
| 20 | RWB-E1-027 | Decision log writer v1 | P7 | S | E1-008, E1-056 |
| 21 | RWB-TE-007 | Scheduled jobs on Quartz | P3 | E | E1-044, E1-056 |
| 22 | RWB-E1-038 | Delegation of authority table as reference data | P4 | S | E1-043, E1-027 |
| 23 | RWB-TE-006 | Outbox and retry for outbound work | P2 | E | E1-044, E1-027, E1-007 |
| 24 | RWB-TE-008 | Decision log hash chain check | P7 | E | E1-008, TE-007 |
| 25 | RWB-E1-019 | Roles, teams and queues as data | P3 | S | E1-038, E1-043 |
| 26 | RWB-E1-022 | Sign-on with SSO, MFA and the first roles | P4 | S | E1-001, E1-019 |
| 27 | RWB-E1-037 | Role to permission matrix as data and PDPA field masking by role | P4 | S | E1-022, E1-043, E1-027 |
| 28 | RWB-E1-039 | Access log into the decision log and break-glass admin | P4,P7 | S | E1-008, E1-022, E1-027 |
| 29 | RWB-E1-016 | Access control per data product and catalog entries | P1 | S | E1-037, E1-001, E1-064, E1-069 |
| 30 | RWB-E1-025 | Document types and fields agreed | P5 | S | E1-069 |
| 31 | RWB-E1-045 | Multi-product parameters for Mortgage, HP and SSME | P3 | E | E1-042, E1-043 |
| 32 | RWB-E1-046 | Template and merge field catalog as data | P6 | S | E1-001, E1-069 |
| 33 | RWB-E1-058 | Agent platform set-up [E1a] | P10 | S | E1-001, E1-037 |
| 34 | RWB-E1-070 | Temporal platform on the ACE AKS clusters | P3 | E | E1-044, E1-056, E1-022 |
| 35 | RWB-E1-071 | Temporal worker and SDK in the recovery module | P3 | E | E1-070, E1-042, E1-047, TE-001 |
| 36 | RWB-E1-072 | Drools runtime and rule package store | P3 | E | E1-044, E1-043, E1-027 |
| 37 | RWB-E1-073 | Rule authoring, validation, test scenarios, approval and rollback in Drools | P3 | S | E1-072, E1-042 |
| 38 | RWB-E1-018 | Case ID issuance and case record v1 | P3 | S | E1-016, E1-027, E1-042, E1-069, E1-072, E1-073 |
| 39 | RWB-TE-013 | Agent runtime client with fallback | P10 | E | TE-007, E1-058, E1-027 |
| 40 | RWB-E1-013 | Baseline measures | P9 | S | E1-043, E1-018 |
| 41 | RWB-E1-020 | Allocation and assignment engine v1 | P3 | S | E1-018, E1-019, E1-027, E1-056, E1-072, E1-073 |
| 42 | RWB-E1-024 | Document store and index | P5 | S | E1-027, E1-018, E1-025, TE-012, E1-001 |
| 43 | RWB-E1-062 | Deviation screening agent in shadow [E2b] | P10 | S | E1-058, TE-013 |
| 44 | RWB-E1-066 | Interaction ledger store and writer | P1 | S | E1-018, E1-027 |
| 45 | RWB-E1-002 | Case list v1 with case ID, owner and queue | P1 | S | E1-018, E1-069, E1-007, E1-020 |
| 46 | RWB-E1-023 | Case record view v1, read only | P3 | S | E1-018, E1-024, E1-037, E1-039 |
| 47 | RWB-E1-028 | Service levels, timers, escalation and prescription dates | P3 | S | E1-045, E1-020, E1-027, E1-043 |
| 48 | RWB-E1-031 | Queue and owner on the case list with filters | P3 | S | E1-020, E1-039 |
| 49 | RWB-E1-049 | OCR pipeline on the Workbench document hub | P5 | S | TE-012, E1-024, E1-045 |
| 50 | RWB-E1-067 | Every Workbench action into the interaction ledger | P1 | S | E1-066 |
| 51 | RWB-E1-068 | Interaction ledger read interface | P1 | S | E1-066 |
| 52 | RWB-E1-021 | Transfer rules and engine v1 | P3 | S | E1-028, E1-020, E1-027, E1-072, E1-073 |
| 53 | RWB-E1-030 | Daily rebalancing and queue measures | P3 | S | E1-020, E1-027, E1-028 |
| 54 | RWB-E1-041 | Retention classes and virus scan on intake | P5 | S | E1-024, E1-049 |
| 55 | RWB-E1-050 | Document classification | P5 | S | E1-049, E1-025 |
| 56 | RWB-E1-015 | Freshness stamp per data product | P1 | S | E1-001, E1-069, E1-027 |
| 57 | RWB-E1-011 | Reconciliation and data quality report | P1 | S | E1-002, E1-015, E1-069 |
| 58 | RWB-E1-026 | Attach and search screen | P5 | S | E1-025, E1-024, E1-041, E1-045, E1-030 |
| 59 | RWB-E1-035 | Case record view v1.1 with documents and history timeline | P3 | S | E1-021, E1-023, E1-027 |
| 60 | RWB-E1-053 | Field extraction for the six types into the index | P5 | S | E1-049, E1-050, E1-025 |
| 61 | RWB-E1-057 | Intake from branches, mailroom, partner SFTP and email | P5 | S | E1-049, TE-012, E1-041 |
| 62 | RWB-E1-059 | Case intake agent in shadow [E1b] | P10 | S | E1-030, E1-058, TE-013 |
| 63 | RWB-E1-032 | Automatic attach from the OCR intake | P5 | S | E1-024, E1-050, E1-053 |
| 64 | RWB-E1-033 | Search across cases | P5 | S | E1-024, E1-053, E1-049 |
| 65 | RWB-E1-034 | Letter template management | P6 | S | E1-046, E1-015 |
| 66 | RWB-E1-040 | Document checklist per case type as reference data | P5 | S | E1-024, E1-043, E1-025, E1-026 |
| 67 | RWB-E1-052 | Notice generation v1 | P6 | S | E1-015, E1-027, E1-046, E1-069 |
| 68 | RWB-E1-060 | Extraction evaluation [E1c] | P10 | S | E1-053, E1-058 |
| 69 | RWB-E1-061 | Intake agent evaluation and L1 proposal [E2a] | P10 | S | E1-059 |
| 70 | RWB-E1-054 | Review queue for low-confidence documents | P5 | S | E1-049, E1-035, E1-050, E1-053, E1-032 |
| 71 | RWB-E1-063 | Agent monitoring dashboard v1 [E2c] | P10 | S | E1-061, E1-007, E1-014, E1-058 |
| 72 | RWB-E1-055 | Proof of delivery capture design with WIN | P6 | S | E1-052, E1-054, E1-028, E1-066 |


Window 3, 30 November to 11 December 2026

21 items, releasing in Epic 2.

| # | Key | Title | Module | E or S | Waits on |
|---|---|---|---|---|---|
| 73 | RWB-E2-037 | Temporal observability and run books | P2 | E | E1-070, E1-071, E1-056 |
| 74 | RWB-E2-038 | Temporal security, codec server and admin audit | P4 | E | E1-070, E1-071, E1-039 |
| 75 | RWB-E2-039 | Temporal resilience, backup, failover, upgrade and archive | P2 | E | E1-070, E2-037 |
| 76 | RWB-E2-040 | Workflow versioning and replay test gate | P2 | E | E1-071 |
| 77 | RWB-E2-041 | Rule change governance and audit report | P3 | S | E1-073, E1-037 |
| 78 | RWB-E2-042 | Epic 2 rule packages in Drools | P3 | S | E1-073 |
| 79 | RWB-TE-010 | Browser and accessibility tests | P2 | E | TE-003 |
| 80 | RWB-E2-003 | Customer's other products on the case | P2 | S | E1-069, E1-007 |
| 81 | RWB-TE-009 | Performance test harness | P2 | E | TE-004 |
| 82 | RWB-E2-005 | Decision log query API for audit | P7 | S | E1-008, E1-039, E2-041 |
| 83 | RWB-E2-004 | Treatment entity and plan timers data model | P3,P1 | S | E1-018, E1-028, E1-045, E1-072, E2-042 |
| 84 | RWB-E2-011 | Queue view screens: my queue, team queues, filters and ageing | P3 | S | E1-020, E1-031 |
| 85 | RWB-E2-013 | Approval routing with the delegation of authority table | P7 | S | E1-038, E1-028, E1-027, E1-037 |
| 86 | RWB-E2-012 | Manual transfer and reassignment screen with reason | P3 | S | E1-021, E2-011, E1-072 |
| 87 | RWB-E2-033 | Case and queue list with status, owner and ageing | P2 | S | E1-018, E1-031, E2-011 |
| 88 | RWB-E2-015 | Timers, escalation and the deviation flag on the case record view | P3 | S | E1-028, E1-035 |
| 89 | RWB-E2-001 | EFS hand-over with full history | P2 | S | E1-069, E1-015, E1-007 |
| 90 | RWB-E2-014 | Approval screen for D7.1 demand and recall notices | P7,P6 | S | E2-013, E1-052 |
| 91 | RWB-E2-022 | SMS and LINE dispatch through NSS and LINE OA | P6 | S | E1-052, E1-066 |
| 92 | RWB-E2-002 | ACE plan status on the case | P2 | S | E2-001, E1-072, E2-042 |
| 93 | RWB-E2-021 | Letter dispatch loop with proof of delivery from WIN | P6 | S | E1-052, E1-055, E2-014 |


Window 4, 14 to 25 December 2026

19 items, releasing in Epic 2.

| # | Key | Title | Module | E or S | Waits on |
|---|---|---|---|---|---|
| 94 | RWB-E2-019 | Partner identities through the external gateway | P4 | S | E1-022, E1-037, E1-039 |
| 95 | RWB-E2-036 | Queue write interface for models and agents | P2 | E | E1-019, E1-020, E1-027 |
| 96 | RWB-E2-006 | Credit approval pack for NLEADS | P2 | S | E2-004, E1-007 |
| 97 | RWB-E2-007 | Booking confirmation from the ALS load | P2,P8 | S | E2-004, E1-007, E1-072, E2-042 |
| 98 | RWB-E2-008 | Payment matching with the missed payment event | P8 | S | E2-004, E1-069, E1-072, E2-042 |
| 99 | RWB-E2-032 | TDR offer-suggestion model through the model gateway [E3e] | P10 | S | E1-058, E2-004, E1-027 |
| 100 | RWB-E2-010 | Stage 2 data products: contracts, plans and treatments | P1 | S | E2-004, E1-016, E1-015 |
| 101 | RWB-E2-027 | Payment matching rules with the data team | P8 | S | E2-008, E2-042 |
| 102 | RWB-E2-035 | Next action on the case | P2 | S | E1-018, E1-031, E2-033, E1-072, E2-042 |
| 103 | RWB-E2-016 | Full case record view with the history timeline | P3,P7 | S | E1-035, E2-015, E2-012 |
| 104 | RWB-E2-024 | Field app photos and bills into the document hub | P5 | S | E1-057, E1-032, E1-053, E1-024, E1-041 |
| 105 | RWB-E2-026 | Document generation engine for contract, CA and mortgage templates | P5 | S | E1-046, E1-034, E1-024, E1-027 |
| 106 | RWB-E2-009 | Steering dashboard v1 data set | P9 | S | E1-013, E1-063 |
| 107 | RWB-E2-017 | Contract, CA and mortgage document generation screens | P5 | S | E2-026, E1-034, E1-054, TE-012 |
| 108 | RWB-E2-025 | Extraction for the stage 2 and 3 document types | P5 | S | E1-053, E1-050, E1-054 |
| 109 | RWB-E2-031 | Agent monitoring dashboard v2 [E3d] | P10 | S | E1-063, E2-005 |
| 110 | RWB-E2-034 | Interaction ledger on the case and from every channel | P2 | S | E1-027, E2-016, E1-069, E1-007, E1-066, E1-067, TE-006 |
| 111 | RWB-E2-018 | E-signature flow for customers and the bank | P6 | S | E2-017, E2-022 |
| 112 | RWB-E2-043 | Temporal and Drools integration pattern and reference case workflow | P3 | E | E1-071, E1-072, TE-006 |


Epic 3, 28 December 2026 to 22 January 2027

3 items, releasing in Epic 3.

| # | Key | Title | Module | E or S | Waits on |
|---|---|---|---|---|---|
| 113 | RWB-E2-028 | Case intake agent live at L1 [E3a] | P10 | S | E1-061, E1-035, E1-027, E2-031 |
| 114 | RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | P10 | S | E1-058, E2-025, E1-061 |
| 115 | RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | P10 | S | E1-062, E2-015, E1-061, E2-028 |


How to use it

Take the next item in order whose dependencies are done. Work in progress per squad stays within the board limit. An item on the critical path is taken before any other item. An item that will miss its release stays behind its flag and moves to the next release. The two squads agree the split at the daily board; the product owner settles a disagreement the same day.

The critical path starts outside the squads. RWB-ACE-001, the ACE team's 14 tables, 12 columns and read grant, is due on 21 November under DL43 and gates RWB-E1-069, the 30 read-only views. RWB-E1-069 gates RWB-E1-018 and RWB-E1-002, the case record and the case list. RWB-E1-072 and RWB-E1-073 gate RWB-E1-018, so the four configuration stories RWB-E1-070 to RWB-E1-073 sit on the chain. From RWB-E1-020 the chain runs RWB-E1-028, RWB-E1-030, RWB-E1-059, RWB-E1-061 and RWB-E1-063, then RWB-E2-031, RWB-E2-028 and RWB-E2-029: 17 items end to end. A day lost on RWB-ACE-001, on RWB-E1-069 or on the Temporal and Drools configuration moves the 30 November release.
