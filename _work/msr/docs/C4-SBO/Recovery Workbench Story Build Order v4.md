SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench story build order

E2E Recovery Workbench. SCB Collections and Recovery. Henka Group, 22 November 2026. v4. Version 3 of this document is dated 16 November 2026.

Version 4 keeps the 115 items of version 3 in their five windows, with every key, title, module, E or S flag, waits-on, item number and date unchanged, and adds the two things the realignment needs: the parallel lane of every story and its Ready to start position. Each item is shown as the microservice stories that carry it, with the service of the Ownership Map v1 and the suggested owner of the work type in Template and Rules §R5.3.

No approval of this version is recorded, so it is issued as Draft: Not specified in the source documents (CG-C4-SBO-1; ASM-C4-SBO-1).

## How this version is read

- Lane. A parallel lane is a connected group of non-contract stories joined by a build dependency (H). A contract story has no build dependency and sits in the contract group CG-W<wave>. A lane is at most four stories deep: the longest chain of build dependencies inside a lane is four stories, and a deeper chain is cut so that the later story builds against the earlier story's contract (Template and Rules §R5.7 rules 1 to 5).
- Ready to start. Day 1 means the story has contract dependencies only, and a contract dependency never blocks because the application builds against the published contract and its fake. After <story> names the story in the same lane that it waits for (Template and Rules §R5.7 rule 8, §R5.4).
- Owner. The service of a story is the Ownership Map v1. The team type is the suggested owner of the work type in Template and Rules §R5.3, and it is a suggestion only: any team may pick up any story (U3; DL46).
- Legacy key. The key of version 3 is kept beside its new stories, so an item can still be found and ordered the old way. The waits-on column of version 3 is kept word for word; it names legacy keys, and the realigned waits of each story are its Ready to start and its lane (CG-C4-SBO-9; ASM-C4-SBO-9).

The order the 115 items are built in, from Recovery Workbench Build Sequence Epic 1 and Epic 2 v6.xlsx. The story numbers are a catalog, not an order: RWB-E1-001 depends on RWB-E1-043 and RWB-E1-044, which are built before it. Pull the next item whose dependencies are done. E is an enabler, S is a user story. Waits on names the items that must finish first, by their number within the same family. RWB-ACE-001 is the ACE team's delivery and is not pulled by either squad; it gates RWB-E1-069.

D-RCV-36. This version applies decision D-RCV-36. Temporal runs the case lifecycle from Epic 3, with case data in the ACE database, and Drools evaluates rules from versioned rule packages. RWB-E1-029, RWB-TE-005 and RWB-E1-048 are retired; their work moved to RWB-E1-073 and RWB-E2-041. The new configuration stories are RWB-E1-070 to RWB-E1-073 and RWB-E2-037 to RWB-E2-043.

Why configuration comes first. The Epic 1 configuration stories RWB-E1-070 to RWB-E1-073 build the Temporal platform, the worker, the Drools runtime and the rule authoring path before RWB-E1-018, RWB-E1-020 and RWB-E1-021, because those engines call RuleEvaluator and write the package version to the decision log. The Epic 2 stories do the same before the engines: RWB-E2-042 loads the RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH packages before RWB-E2-002, RWB-E2-004, RWB-E2-007, RWB-E2-008 and RWB-E2-027, and RWB-E2-043 sets the integration pattern before Epic 3.

D-RCV-60. This version also applies decision D-RCV-60: Architecture v5, 19 services inside ACE, Kafka with outbox and inbox, a reusable Temporal layer, embedded Drools with the rule registry in rwb-decision, the edge of gateway-bff and the partner gateway, and no data lake. Every one of the 115 items is split into the stories that carry it (Template and Rules §R5 and §R6), and each story carries its own lane and its own Ready to start, so an item is no longer one unit of work: it is the stories listed against it, and the contract story of the item is pulled before the application stories that use it. A build dependency points only inside the service or to a platform contract story; a dependency on another service is a contract dependency and never blocks the build; an integration dependency sits only on an integration story; external and team-type work is tracked and does not block. Two items carry no story: RWB-E1-014, the decision log copy to the data lake, because there is no data lake (DP-17), and RWB-TE-007, the Quartz scheduler, whose work is RWB-PLT-E1071-CON on Temporal Schedules (DP-10).

## Window 1, 2 to 13 November 2026 (tentative)

15 items, releasing in Epic 1 (tentative).

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

The same 15 items in the same order, as the 60 microservice stories that carry them. Inside an item the contract story comes first, then the application, database, infrastructure, DevOps and integration stories.

| # | Key | New story | Work type | Service | Suggested owner | Parallel lane | Ready to start |
|---|---|---|---|---|---|---|---|
| 1 | RWB-E1-044 | RWB-PLT-E1044-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 1 | RWB-E1-044 | RWB-PLT-E1044-APP | App development | PLT platform | TechX | L-PLT-TPL-G | Day 1 |
| 1 | RWB-E1-044 | RWB-PLT-E1044-APP-2 | App development | PLT platform | TechX | L-PLT-TPL-F | Day 1 |
| 1 | RWB-E1-044 | RWB-PLT-E1044-OPS | DevOps | PLT platform | DevOps team | L-PLT-TPL-H | Day 1 |
| 2 | RWB-TE-001 | RWB-PLT-TE001-APP | App development | PLT platform | TechX | L-PLT-TPL-J | Day 1 |
| 2 | RWB-TE-001 | RWB-PLT-TE001-APP-2 | App development | PLT platform | TechX | L-PLT-TPL-I | Day 1 |
| 3 | RWB-E1-042 | RWB-P3-E1042-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 3 | RWB-E1-042 | RWB-PLT-E1042-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 3 | RWB-E1-042 | RWB-P3-E1042-APP | App development | P3 rwb-case | TechX | L-P3-N | Day 1 |
| 3 | RWB-E1-042 | RWB-PLT-E1042-APP | App development | PLT platform | TechX | L-PLT-LIB-F | Day 1 |
| 3 | RWB-E1-042 | RWB-PLT-E1042-OPS | DevOps | PLT platform | DevOps team | L-PLT-LIB-E | Day 1 |
| 4 | RWB-TE-002 | RWB-PLT-TE002-APP | App development | PLT platform | TechX | L-PLT-TPL-L | Day 1 |
| 4 | RWB-TE-002 | RWB-PLT-TE002-OPS | DevOps | PLT platform | DevOps team | L-PLT-TPL-K | Day 1 |
| 5 | RWB-TE-003 | RWB-PLT-TE003-APP | App development | PLT platform | TechX | L-PLT-TPL-N | Day 1 |
| 5 | RWB-TE-003 | RWB-PLT-TE003-APP-2 | App development | PLT platform | TechX | L-PLT-TPL-M | Day 1 |
| 6 | RWB-TE-011 | RWB-PLT-TE011-APP | App development | PLT platform | TechX | L-PLT-TPL-Q | Day 1 |
| 7 | RWB-TE-012 | RWB-PLT-TE012-APP | App development | PLT platform | TechX | L-PLT-TPL-R | Day 1 |
| 8 | RWB-E1-043 | RWB-P3-E1043-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 8 | RWB-E1-043 | RWB-PLT-E1043-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 8 | RWB-E1-043 | RWB-P3-E1043-APP | App development | P3 rwb-case | TechX | L-P3-O | Day 1 |
| 8 | RWB-E1-043 | RWB-PLT-E1043-APP | App development | PLT platform | TechX | L-PLT-LIB-G | Day 1 |
| 9 | RWB-E1-001 | RWB-P1-E1001-APP | App development | P1 rwb-source-data | TechX | L-P1-A | Day 1 |
| 9 | RWB-E1-001 | RWB-P4-E1001-APP | App development | P4 rwb-access | TechX | L-P4-K | Day 1 |
| 9 | RWB-E1-001 | RWB-P7-E1001-APP | App development | P7 rwb-decision | TechX | L-P7-A | Day 1 |
| 9 | RWB-E1-001 | RWB-P8-E1001-APP | App development | P8 rwb-payment | TechX | L-P8-B | Day 1 |
| 9 | RWB-E1-001 | RWB-ITG-E1001-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 10 | RWB-E1-069 | RWB-P1-E1069-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1001-APP, RWB-P1-ACE001-DB |
| 10 | RWB-E1-069 | RWB-P4-E1069-APP | App development | P4 rwb-access | TechX | L-P4-AC | Day 1 |
| 10 | RWB-E1-069 | RWB-P1-E1069-DB | ACE DB | P1 rwb-source-data | ACE team | L-P1-R | Day 1 |
| 10 | RWB-E1-069 | RWB-ITG-E1069-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 11 | RWB-E1-007 | RWB-P2-E1007-CON | Contract | P2 rwb-integration | TechX | CG-W1 | Day 1 |
| 11 | RWB-E1-007 | RWB-P2-E1007-APP | App development | P2 rwb-integration | TechX | L-P2-A | Day 1 |
| 11 | RWB-E1-007 | RWB-P3-E1007-APP | App development | P3 rwb-case | TechX | L-P3-C | Day 1 |
| 11 | RWB-E1-007 | RWB-P4-E1007-APP | App development | P4 rwb-access | TechX | L-P4-L | Day 1 |
| 11 | RWB-E1-007 | RWB-P5-E1007-APP | App development | P5 rwb-document | TechX | L-P5-B | Day 1 |
| 11 | RWB-E1-007 | RWB-P6-E1007-APP | App development | P6 rwb-comms | TechX | L-P6-B | Day 1 |
| 11 | RWB-E1-007 | RWB-P2-E1007-INF | Infrastructure | P2 rwb-integration | SCB IT infrastructure | L-P2-C | Day 1 |
| 11 | RWB-E1-007 | RWB-P2-E1007-OPS | DevOps | P2 rwb-integration | DevOps team | L-P2-B | Day 1 |
| 11 | RWB-E1-007 | RWB-ITG-E1007-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 12 | RWB-E1-008 | RWB-P7-E1008-CON | Contract | P7 rwb-decision | TechX | CG-W1 | Day 1 |
| 12 | RWB-E1-008 | RWB-P4-E1008-APP | App development | P4 rwb-access | TechX | L-P4-M | Day 1 |
| 12 | RWB-E1-008 | RWB-P7-E1008-APP | App development | P7 rwb-decision | TechX | L-P7-B | Day 1 |
| 12 | RWB-E1-008 | RWB-P7-E1008-DB | ACE DB | P7 rwb-decision | ACE team | L-P7-D | Day 1 |
| 12 | RWB-E1-008 | RWB-P7-E1008-OPS | DevOps | P7 rwb-decision | DevOps team | L-P7-C | Day 1 |
| 12 | RWB-E1-008 | RWB-ITG-E1008-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 13 | RWB-E1-064 | RWB-P1-E1064-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 13 | RWB-E1-064 | RWB-P1-E1064-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| 13 | RWB-E1-064 | RWB-P4-E1064-APP | App development | P4 rwb-access | TechX | L-P4-AA | Day 1 |
| 13 | RWB-E1-064 | RWB-P1-E1064-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-N | Day 1 |
| 13 | RWB-E1-064 | RWB-ITG-E1064-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 14 | RWB-E1-065 | RWB-P1-E1065-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 14 | RWB-E1-065 | RWB-P1-E1065-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| 14 | RWB-E1-065 | RWB-P3-E1065-APP | App development | P3 rwb-case | TechX | L-P3-T | Day 1 |
| 14 | RWB-E1-065 | RWB-P4-E1065-APP | App development | P4 rwb-access | TechX | L-P4-AB | Day 1 |
| 14 | RWB-E1-065 | RWB-P5-E1065-APP | App development | P5 rwb-document | TechX | L-P5-T | Day 1 |
| 14 | RWB-E1-065 | RWB-S8-E1065-APP | App development | S8 rwb-deviation | TechX | L-S8-E | Day 1 |
| 14 | RWB-E1-065 | RWB-P1-E1065-DB | ACE DB | P1 rwb-source-data | ACE team | L-P1-O | Day 1 |
| 14 | RWB-E1-065 | RWB-ITG-E1065-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 15 | RWB-TE-004 | RWB-PLT-TE004-APP | App development | PLT platform | TechX | L-PLT-TPL-O | Day 1 |
| 15 | RWB-TE-004 | RWB-ITG-TE004-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |

## Window 2, 16 to 27 November 2026 (tentative)

57 items, releasing in Epic 1 (tentative).

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

The same 57 items in the same order, as the 235 microservice stories that carry them. Inside an item the contract story comes first, then the application, database, infrastructure, DevOps and integration stories.

| # | Key | New story | Work type | Service | Suggested owner | Parallel lane | Ready to start |
|---|---|---|---|---|---|---|---|
| 16 | RWB-E1-047 | RWB-PLT-E1047-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 16 | RWB-E1-047 | RWB-PLT-E1047-APP | App development | PLT platform | TechX | L-PLT-LIB-H | Day 1 |
| 16 | RWB-E1-047 | RWB-ITG-E1047-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 17 | RWB-E1-017 | RWB-P1-E1017-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 17 | RWB-E1-017 | RWB-P1-E1017-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1001-APP, RWB-P1-E1064-APP |
| 17 | RWB-E1-017 | RWB-P5-E1017-APP | App development | P5 rwb-document | TechX | L-P5-D | Day 1 |
| 17 | RWB-E1-017 | RWB-P7-E1017-APP | App development | P7 rwb-decision | TechX | L-P7-E | Day 1 |
| 17 | RWB-E1-017 | RWB-P1-E1017-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-K | Day 1 |
| 17 | RWB-E1-017 | RWB-ITG-E1017-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 18 | RWB-E1-056 | RWB-PLT-E1056-OPS | DevOps | PLT platform | DevOps team | L-PLT-OBS-B | Day 1 |
| 20 | RWB-E1-027 | RWB-P7-E1027-CON | Contract | P7 rwb-decision | TechX | CG-W1 | Day 1 |
| 20 | RWB-E1-027 | RWB-PLT-E1027-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 20 | RWB-E1-027 | RWB-P7-E1027-APP | App development | P7 rwb-decision | TechX | L-P7-B | After RWB-P7-E1008-APP |
| 20 | RWB-E1-027 | RWB-PLT-E1027-APP | App development | PLT platform | TechX | L-PLT-LIB-C | Day 1 |
| 20 | RWB-E1-027 | RWB-ITG-E1027-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 22 | RWB-E1-038 | RWB-P4-E1038-APP | App development | P4 rwb-access | TechX | L-P4-J | Day 1 |
| 23 | RWB-TE-006 | RWB-PLT-TE006-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 23 | RWB-TE-006 | RWB-PLT-TE006-APP | App development | PLT platform | TechX | L-PLT-LIB-J | Day 1 |
| 23 | RWB-TE-006 | RWB-ITG-TE006-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 24 | RWB-TE-008 | RWB-PLT-TE008-APP | App development | PLT platform | TechX | L-PLT-TPL-P | Day 1 |
| 24 | RWB-TE-008 | RWB-ITG-TE008-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 25 | RWB-E1-019 | RWB-P3-E1019-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 25 | RWB-E1-019 | RWB-P3-E1019-APP | App development | P3 rwb-case | TechX | L-P3-F | Day 1 |
| 25 | RWB-E1-019 | RWB-P4-E1019-APP | App development | P4 rwb-access | TechX | L-P4-P | Day 1 |
| 25 | RWB-E1-019 | RWB-P6-E1019-APP | App development | P6 rwb-comms | TechX | L-P6-D | Day 1 |
| 25 | RWB-E1-019 | RWB-P3-E1019-DB | ACE DB | P3 rwb-case | ACE team | L-P3-H | Day 1 |
| 25 | RWB-E1-019 | RWB-ITG-E1019-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 26 | RWB-E1-022 | RWB-P4-E1022-CON | Contract | P4 rwb-access | TechX | CG-W1 | Day 1 |
| 26 | RWB-E1-022 | RWB-P4-E1022-APP | App development | P4 rwb-access | TechX | L-P4-A | Day 1 |
| 26 | RWB-E1-022 | RWB-P4-E1022-DB | ACE DB | P4 rwb-access | ACE team | L-P4-S | Day 1 |
| 26 | RWB-E1-022 | RWB-ITG-E1022-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 27 | RWB-E1-037 | RWB-P4-E1037-CON | Contract | P4 rwb-access | TechX | CG-W1 | Day 1 |
| 27 | RWB-E1-037 | RWB-PLT-E1037-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 27 | RWB-E1-037 | RWB-P4-E1037-APP | App development | P4 rwb-access | TechX | L-P4-A | After RWB-P4-E1022-APP |
| 27 | RWB-E1-037 | RWB-PLT-E1037-APP | App development | PLT platform | TechX | L-PLT-LIB-D | Day 1 |
| 27 | RWB-E1-037 | RWB-ITG-E1037-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 28 | RWB-E1-039 | RWB-P4-E1039-CON | Contract | P4 rwb-access | TechX | CG-W1 | Day 1 |
| 28 | RWB-E1-039 | RWB-P4-E1039-APP | App development | P4 rwb-access | TechX | L-P4-A | After RWB-P4-E1022-APP |
| 28 | RWB-E1-039 | RWB-P5-E1039-APP | App development | P5 rwb-document | TechX | L-P5-J | Day 1 |
| 28 | RWB-E1-039 | RWB-P7-E1039-APP | App development | P7 rwb-decision | TechX | L-P7-L | Day 1 |
| 28 | RWB-E1-039 | RWB-P4-E1039-DB | ACE DB | P4 rwb-access | ACE team | L-P4-W | Day 1 |
| 28 | RWB-E1-039 | RWB-P4-E1039-OPS | DevOps | P4 rwb-access | DevOps team | L-P4-V | Day 1 |
| 28 | RWB-E1-039 | RWB-ITG-E1039-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 29 | RWB-E1-016 | RWB-P1-E1016-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 29 | RWB-E1-016 | RWB-P1-E1016-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1001-APP, RWB-P1-E1064-APP, RWB-P1-E1069-APP |
| 29 | RWB-E1-016 | RWB-P4-E1016-APP | App development | P4 rwb-access | TechX | L-P4-N | Day 1 |
| 29 | RWB-E1-016 | RWB-P5-E1016-APP | App development | P5 rwb-document | TechX | L-P5-C | Day 1 |
| 29 | RWB-E1-016 | RWB-P1-E1016-DB | ACE DB | P1 rwb-source-data | ACE team | L-P1-J | Day 1 |
| 29 | RWB-E1-016 | RWB-ITG-E1016-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 30 | RWB-E1-025 | RWB-P5-E1025-APP | App development | P5 rwb-document | TechX | L-P5-G | Day 1 |
| 30 | RWB-E1-025 | RWB-ITG-E1025-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 31 | RWB-E1-045 | RWB-P3-E1045-APP | App development | P3 rwb-case | TechX | L-P3-F | Day 1 |
| 32 | RWB-E1-046 | RWB-P6-E1046-CON | Contract | P6 rwb-comms | TechX | CG-W1 | Day 1 |
| 32 | RWB-E1-046 | RWB-P5-E1046-APP | App development | P5 rwb-document | TechX | L-P5-K | Day 1 |
| 32 | RWB-E1-046 | RWB-P6-E1046-APP | App development | P6 rwb-comms | TechX | L-P6-A | Day 1 |
| 32 | RWB-E1-046 | RWB-P7-E1046-APP | App development | P7 rwb-decision | TechX | L-P7-M | Day 1 |
| 32 | RWB-E1-046 | RWB-ITG-E1046-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 33 | RWB-E1-058 | RWB-P10-E1058-CON | Contract | P10 rwb-agent | TechX | CG-W1 | Day 1 |
| 33 | RWB-E1-058 | RWB-P10-E1058-APP | App development | P10 rwb-agent | TechX | L-P10-A | Day 1 |
| 33 | RWB-E1-058 | RWB-P10-E1058-INF | Infrastructure | P10 rwb-agent | SCB IT infrastructure | L-P10-B | Day 1 |
| 33 | RWB-E1-058 | RWB-P10-E1058-OPS | DevOps | P10 rwb-agent | DevOps team | L-P10-C | Day 1 |
| 33 | RWB-E1-058 | RWB-ITG-E1058-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 34 | RWB-E1-070 | RWB-PLT-E1070-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 34 | RWB-E1-070 | RWB-PLT-E1070-APP | App development | PLT platform | TechX | L-PLT-WF-D | Day 1 |
| 34 | RWB-E1-070 | RWB-ITG-E1070-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 35 | RWB-E1-071 | RWB-PLT-E1071-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 35 | RWB-E1-071 | RWB-PLT-E1071-APP | App development | PLT platform | TechX | L-PLT-WF-E | Day 1 |
| 36 | RWB-E1-072 | RWB-PLT-E1072-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 36 | RWB-E1-072 | RWB-PLT-E1072-APP | App development | PLT platform | TechX | L-PLT-LIB-I | Day 1 |
| 37 | RWB-E1-073 | RWB-P3-E1073-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 37 | RWB-E1-073 | RWB-P2-E1073-APP | App development | P2 rwb-integration | TechX | L-P2-D | Day 1 |
| 37 | RWB-E1-073 | RWB-P3-E1073-APP | App development | P3 rwb-case | TechX | L-P3-F | Day 1 |
| 37 | RWB-E1-073 | RWB-P6-E1073-APP | App development | P6 rwb-comms | TechX | L-P6-J | Day 1 |
| 37 | RWB-E1-073 | RWB-P7-E1073-APP | App development | P7 rwb-decision | TechX | L-P7-P | Day 1 |
| 37 | RWB-E1-073 | RWB-P3-E1073-INF | Infrastructure | P3 rwb-case | SCB IT infrastructure | L-P3-W | Day 1 |
| 37 | RWB-E1-073 | RWB-ITG-E1073-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 38 | RWB-E1-018 | RWB-P3-E1018-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 38 | RWB-E1-018 | RWB-P1-E1018-APP | App development | P1 rwb-source-data | TechX | L-P1-L | Day 1 |
| 38 | RWB-E1-018 | RWB-P3-E1018-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1073-APP |
| 38 | RWB-E1-018 | RWB-P4-E1018-APP | App development | P4 rwb-access | TechX | L-P4-O | Day 1 |
| 38 | RWB-E1-018 | RWB-P5-E1018-APP | App development | P5 rwb-document | TechX | L-P5-E | Day 1 |
| 38 | RWB-E1-018 | RWB-P7-E1018-APP | App development | P7 rwb-decision | TechX | L-P7-F | Day 1 |
| 38 | RWB-E1-018 | RWB-P3-E1018-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-G | Day 1 |
| 38 | RWB-E1-018 | RWB-ITG-E1018-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 39 | RWB-TE-013 | RWB-P10-TE013-CON | Contract | P10 rwb-agent | TechX | CG-W1 | Day 1 |
| 39 | RWB-TE-013 | RWB-P10-TE013-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP |
| 39 | RWB-TE-013 | RWB-P7-TE013-APP | App development | P7 rwb-decision | TechX | L-P7-AR | Day 1 |
| 39 | RWB-TE-013 | RWB-P10-TE013-OPS | DevOps | P10 rwb-agent | DevOps team | L-P10-M | Day 1 |
| 39 | RWB-TE-013 | RWB-ITG-TE013-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 40 | RWB-E1-013 | RWB-P9-E1013-CON | Contract | P9 rwb-reporting | TechX | CG-W1 | Day 1 |
| 40 | RWB-E1-013 | RWB-P1-E1013-APP | App development | P1 rwb-source-data | TechX | L-P1-H | Day 1 |
| 40 | RWB-E1-013 | RWB-P3-E1013-APP | App development | P3 rwb-case | TechX | L-P3-E | Day 1 |
| 40 | RWB-E1-013 | RWB-P9-E1013-APP | App development | P9 rwb-reporting | TechX | L-P9-A | Day 1 |
| 40 | RWB-E1-013 | RWB-P9-E1013-OPS | DevOps | P9 rwb-reporting | DevOps team | L-P9-B | Day 1 |
| 40 | RWB-E1-013 | RWB-ITG-E1013-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 41 | RWB-E1-020 | RWB-P3-E1020-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 41 | RWB-E1-020 | RWB-P3-E1020-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1018-APP, RWB-P3-E1019-APP, RWB-P3-E1073-APP |
| 41 | RWB-E1-020 | RWB-P4-E1020-APP | App development | P4 rwb-access | TechX | L-P4-Q | Day 1 |
| 41 | RWB-E1-020 | RWB-P7-E1020-APP | App development | P7 rwb-decision | TechX | L-P7-G | Day 1 |
| 41 | RWB-E1-020 | RWB-S8-E1020-APP | App development | S8 rwb-deviation | TechX | L-S8-A | Day 1 |
| 41 | RWB-E1-020 | RWB-P3-E1020-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-I | Day 1 |
| 41 | RWB-E1-020 | RWB-ITG-E1020-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 42 | RWB-E1-024 | RWB-P5-E1024-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1025-APP |
| 42 | RWB-E1-024 | RWB-ITG-E1024-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 43 | RWB-E1-062 | RWB-P10-E1062-CON | Contract | P10 rwb-agent | TechX | CG-W1 | Day 1 |
| 43 | RWB-E1-062 | RWB-P10-E1062-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| 43 | RWB-E1-062 | RWB-P4-E1062-APP | App development | P4 rwb-access | TechX | L-P4-Y | Day 1 |
| 43 | RWB-E1-062 | RWB-P5-E1062-APP | App development | P5 rwb-document | TechX | L-P5-S | Day 1 |
| 43 | RWB-E1-062 | RWB-S8-E1062-APP | App development | S8 rwb-deviation | TechX | L-S8-D | Day 1 |
| 43 | RWB-E1-062 | RWB-ITG-E1062-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 44 | RWB-E1-066 | RWB-P1-E1066-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 44 | RWB-E1-066 | RWB-P1-E1066-APP | App development | P1 rwb-source-data | TechX | L-P1-P | Day 1 |
| 44 | RWB-E1-066 | RWB-P3-E1066-APP | App development | P3 rwb-case | TechX | L-P3-U | Day 1 |
| 44 | RWB-E1-066 | RWB-P1-E1066-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-Q | Day 1 |
| 44 | RWB-E1-066 | RWB-ITG-E1066-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 45 | RWB-E1-002 | RWB-P1-E1002-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 45 | RWB-E1-002 | RWB-P1-E1002-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| 45 | RWB-E1-002 | RWB-P3-E1002-APP | App development | P3 rwb-case | TechX | L-P3-B | Day 1 |
| 45 | RWB-E1-002 | RWB-P1-E1002-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-F | Day 1 |
| 45 | RWB-E1-002 | RWB-ITG-E1002-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 46 | RWB-E1-023 | RWB-P3-E1023-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 46 | RWB-E1-023 | RWB-P3-E1023-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1018-APP |
| 46 | RWB-E1-023 | RWB-P4-E1023-APP | App development | P4 rwb-access | TechX | L-P4-T | Day 1 |
| 46 | RWB-E1-023 | RWB-S8-E1023-APP | App development | S8 rwb-deviation | TechX | L-S8-C | Day 1 |
| 46 | RWB-E1-023 | RWB-ITG-E1023-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 47 | RWB-E1-028 | RWB-P3-E1028-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 47 | RWB-E1-028 | RWB-P3-E1028-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1045-APP, RWB-P3-E1020-APP |
| 47 | RWB-E1-028 | RWB-P4-E1028-APP | App development | P4 rwb-access | TechX | L-P4-U | Day 1 |
| 47 | RWB-E1-028 | RWB-P7-E1028-APP | App development | P7 rwb-decision | TechX | L-P7-I | Day 1 |
| 47 | RWB-E1-028 | RWB-P3-E1028-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-K | Day 1 |
| 47 | RWB-E1-028 | RWB-ITG-E1028-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 48 | RWB-E1-031 | RWB-P3-E1031-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 48 | RWB-E1-031 | RWB-P3-E1031-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1020-APP |
| 48 | RWB-E1-031 | RWB-ITG-E1031-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 49 | RWB-E1-049 | RWB-P5-E1049-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 49 | RWB-E1-049 | RWB-P5-E1049-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1024-APP |
| 49 | RWB-E1-049 | RWB-P6-E1049-APP | App development | P6 rwb-comms | TechX | L-P6-F | Day 1 |
| 49 | RWB-E1-049 | RWB-P5-E1049-INF | Infrastructure | P5 rwb-document | SCB IT infrastructure | L-P5-M | Day 1 |
| 49 | RWB-E1-049 | RWB-P5-E1049-OPS | DevOps | P5 rwb-document | DevOps team | L-P5-L | Day 1 |
| 49 | RWB-E1-049 | RWB-ITG-E1049-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 50 | RWB-E1-067 | RWB-P1-E1067-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 50 | RWB-E1-067 | RWB-P1-E1067-APP | App development | P1 rwb-source-data | TechX | L-P1-P | After RWB-P1-E1066-APP |
| 50 | RWB-E1-067 | RWB-P3-E1067-APP | App development | P3 rwb-case | TechX | L-P3-V | Day 1 |
| 50 | RWB-E1-067 | RWB-P5-E1067-APP | App development | P5 rwb-document | TechX | L-P5-U | Day 1 |
| 50 | RWB-E1-067 | RWB-ITG-E1067-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 51 | RWB-E1-068 | RWB-P1-E1068-APP | App development | P1 rwb-source-data | TechX | L-P1-P | After RWB-P1-E1066-APP |
| 52 | RWB-E1-021 | RWB-P3-E1021-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 52 | RWB-E1-021 | RWB-P3-E1021-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1020-APP, RWB-P3-E1073-APP |
| 52 | RWB-E1-021 | RWB-P4-E1021-APP | App development | P4 rwb-access | TechX | L-P4-R | Day 1 |
| 52 | RWB-E1-021 | RWB-P5-E1021-APP | App development | P5 rwb-document | TechX | L-P5-F | Day 1 |
| 52 | RWB-E1-021 | RWB-P7-E1021-APP | App development | P7 rwb-decision | TechX | L-P7-H | Day 1 |
| 52 | RWB-E1-021 | RWB-S8-E1021-APP | App development | S8 rwb-deviation | TechX | L-S8-B | Day 1 |
| 52 | RWB-E1-021 | RWB-P3-E1021-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-J | Day 1 |
| 52 | RWB-E1-021 | RWB-ITG-E1021-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 53 | RWB-E1-030 | RWB-P3-E1030-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 53 | RWB-E1-030 | RWB-P3-E1030-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1020-APP |
| 53 | RWB-E1-030 | RWB-P7-E1030-APP | App development | P7 rwb-decision | TechX | L-P7-J | Day 1 |
| 53 | RWB-E1-030 | RWB-P3-E1030-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-L | Day 1 |
| 53 | RWB-E1-030 | RWB-ITG-E1030-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 54 | RWB-E1-041 | RWB-P5-E1041-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 54 | RWB-E1-041 | RWB-P5-E1041-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| 55 | RWB-E1-050 | RWB-P5-E1050-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 55 | RWB-E1-050 | RWB-P3-E1050-APP | App development | P3 rwb-case | TechX | L-P3-P | Day 1 |
| 55 | RWB-E1-050 | RWB-P5-E1050-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| 55 | RWB-E1-050 | RWB-P5-E1050-OPS | DevOps | P5 rwb-document | DevOps team | L-P5-N | Day 1 |
| 55 | RWB-E1-050 | RWB-ITG-E1050-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 56 | RWB-E1-015 | RWB-P1-E1015-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 56 | RWB-E1-015 | RWB-P1-E1015-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1001-APP, RWB-P1-E1069-APP |
| 56 | RWB-E1-015 | RWB-P1-E1015-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-I | Day 1 |
| 56 | RWB-E1-015 | RWB-ITG-E1015-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 57 | RWB-E1-011 | RWB-P1-E1011-CON | Contract | P1 rwb-source-data | TechX | CG-W1 | Day 1 |
| 57 | RWB-E1-011 | RWB-P1-E1011-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1015-APP, RWB-P1-E1069-APP |
| 57 | RWB-E1-011 | RWB-P3-E1011-APP | App development | P3 rwb-case | TechX | L-P3-D | Day 1 |
| 57 | RWB-E1-011 | RWB-P6-E1011-APP | App development | P6 rwb-comms | TechX | L-P6-C | Day 1 |
| 57 | RWB-E1-011 | RWB-S5-E1011-APP | App development | S5 rwb-asset | TechX | L-S5-A | Day 1 |
| 57 | RWB-E1-011 | RWB-P1-E1011-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-G | Day 1 |
| 57 | RWB-E1-011 | RWB-ITG-E1011-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 58 | RWB-E1-026 | RWB-P5-E1026-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1025-APP, RWB-P5-E1024-APP |
| 58 | RWB-E1-026 | RWB-ITG-E1026-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 59 | RWB-E1-035 | RWB-P3-E1035-CON | Contract | P3 rwb-case | TechX | CG-W1 | Day 1 |
| 59 | RWB-E1-035 | RWB-P3-E1035-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1023-APP |
| 60 | RWB-E1-053 | RWB-P5-E1053-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 60 | RWB-E1-053 | RWB-P5-E1053-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1049-APP, RWB-P5-E1025-APP |
| 61 | RWB-E1-057 | RWB-P5-E1057-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 61 | RWB-E1-057 | RWB-P5-E1057-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1049-APP |
| 61 | RWB-E1-057 | RWB-S9-E1057-APP | App development | S9 rwb-partner | TechX | L-S9-C | Day 1 |
| 61 | RWB-E1-057 | RWB-P5-E1057-INF | Infrastructure | P5 rwb-document | SCB IT infrastructure | L-P5-R | Day 1 |
| 61 | RWB-E1-057 | RWB-P5-E1057-OPS | DevOps | P5 rwb-document | DevOps team | L-P5-Q | Day 1 |
| 61 | RWB-E1-057 | RWB-ITG-E1057-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 62 | RWB-E1-059 | RWB-P10-E1059-CON | Contract | P10 rwb-agent | TechX | CG-W1 | Day 1 |
| 62 | RWB-E1-059 | RWB-P10-E1059-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| 62 | RWB-E1-059 | RWB-ITG-E1059-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 63 | RWB-E1-032 | RWB-P5-E1032-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 63 | RWB-E1-032 | RWB-P3-E1032-APP | App development | P3 rwb-case | TechX | L-P3-M | Day 1 |
| 63 | RWB-E1-032 | RWB-P5-E1032-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1024-APP |
| 63 | RWB-E1-032 | RWB-P6-E1032-APP | App development | P6 rwb-comms | TechX | L-P6-E | Day 1 |
| 63 | RWB-E1-032 | RWB-P7-E1032-APP | App development | P7 rwb-decision | TechX | L-P7-K | Day 1 |
| 63 | RWB-E1-032 | RWB-S9-E1032-APP | App development | S9 rwb-partner | TechX | L-S9-B | Day 1 |
| 63 | RWB-E1-032 | RWB-P5-E1032-INF | Infrastructure | P5 rwb-document | SCB IT infrastructure | L-P5-I | Day 1 |
| 63 | RWB-E1-032 | RWB-P5-E1032-OPS | DevOps | P5 rwb-document | DevOps team | L-P5-H | Day 1 |
| 63 | RWB-E1-032 | RWB-ITG-E1032-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 64 | RWB-E1-033 | RWB-P5-E1033-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1024-APP, RWB-P5-E1049-APP |
| 65 | RWB-E1-034 | RWB-P6-E1034-APP | App development | P6 rwb-comms | TechX | L-P6-A | After RWB-P6-E1046-APP |
| 65 | RWB-E1-034 | RWB-ITG-E1034-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 66 | RWB-E1-040 | RWB-P5-E1040-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1024-APP, RWB-P5-E1025-APP, RWB-P5-E1026-APP |
| 67 | RWB-E1-052 | RWB-P6-E1052-CON | Contract | P6 rwb-comms | TechX | CG-W1 | Day 1 |
| 67 | RWB-E1-052 | RWB-P3-E1052-APP | App development | P3 rwb-case | TechX | L-P3-Q | Day 1 |
| 67 | RWB-E1-052 | RWB-P5-E1052-APP | App development | P5 rwb-document | TechX | L-P5-O | Day 1 |
| 67 | RWB-E1-052 | RWB-P6-E1052-APP | App development | P6 rwb-comms | TechX | L-P6-A | After RWB-P6-E1046-APP |
| 67 | RWB-E1-052 | RWB-P7-E1052-APP | App development | P7 rwb-decision | TechX | L-P7-N | Day 1 |
| 67 | RWB-E1-052 | RWB-ITG-E1052-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 68 | RWB-E1-060 | RWB-P10-E1060-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP |
| 68 | RWB-E1-060 | RWB-ITG-E1060-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 69 | RWB-E1-061 | RWB-P10-E1061-CON | Contract | P10 rwb-agent | TechX | CG-W1 | Day 1 |
| 69 | RWB-E1-061 | RWB-P10-E1061-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1059-APP |
| 70 | RWB-E1-054 | RWB-P5-E1054-CON | Contract | P5 rwb-document | TechX | CG-W1 | Day 1 |
| 70 | RWB-E1-054 | RWB-P3-E1054-APP | App development | P3 rwb-case | TechX | L-P3-R | Day 1 |
| 70 | RWB-E1-054 | RWB-P4-E1054-APP | App development | P4 rwb-access | TechX | L-P4-X | Day 1 |
| 70 | RWB-E1-054 | RWB-P5-E1054-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1049-APP, RWB-P5-E1032-APP |
| 70 | RWB-E1-054 | RWB-P7-E1054-APP | App development | P7 rwb-decision | TechX | L-P7-O | Day 1 |
| 70 | RWB-E1-054 | RWB-ITG-E1054-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 71 | RWB-E1-063 | RWB-P10-E1063-CON | Contract | P10 rwb-agent | TechX | CG-W1 | Day 1 |
| 71 | RWB-E1-063 | RWB-P10-E1063-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP |
| 71 | RWB-E1-063 | RWB-P4-E1063-APP | App development | P4 rwb-access | TechX | L-P4-Z | Day 1 |
| 71 | RWB-E1-063 | RWB-P6-E1063-APP | App development | P6 rwb-comms | TechX | L-P6-I | Day 1 |
| 71 | RWB-E1-063 | RWB-P10-E1063-OPS | DevOps | P10 rwb-agent | DevOps team | L-P10-D | Day 1 |
| 71 | RWB-E1-063 | RWB-ITG-E1063-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |
| 72 | RWB-E1-055 | RWB-P6-E1055-CON | Contract | P6 rwb-comms | TechX | CG-W1 | Day 1 |
| 72 | RWB-E1-055 | RWB-P1-E1055-APP | App development | P1 rwb-source-data | TechX | L-P1-M | Day 1 |
| 72 | RWB-E1-055 | RWB-P3-E1055-APP | App development | P3 rwb-case | TechX | L-P3-S | Day 1 |
| 72 | RWB-E1-055 | RWB-P5-E1055-APP | App development | P5 rwb-document | TechX | L-P5-P | Day 1 |
| 72 | RWB-E1-055 | RWB-P6-E1055-APP | App development | P6 rwb-comms | TechX | L-P6-A | After RWB-P6-E1052-APP |
| 72 | RWB-E1-055 | RWB-P6-E1055-INF | Infrastructure | P6 rwb-comms | SCB IT infrastructure | L-P6-H | Day 1 |
| 72 | RWB-E1-055 | RWB-P6-E1055-OPS | DevOps | P6 rwb-comms | DevOps team | L-P6-G | Day 1 |
| 72 | RWB-E1-055 | RWB-ITG-E1055-ITG | Integration | ITG integration | TechX | L-ITG-W1 | Day 1 |

No story carries item 19 RWB-E1-014, the decision-log copy to the data lake, because there is no data lake in D-RCV-60 (DP-17), and no story carries item 21 RWB-TE-007, the Quartz scheduler, whose work is RWB-PLT-E1071-CON on Temporal Schedules (DP-10). The item keeps its number and its place in the order of version 3, and a dependency that pointed at RWB-TE-007 now points at RWB-PLT-E1071-CON (Template and Rules §R6).

## Window 3, 30 November to 11 December 2026 (tentative)

21 items, releasing in Epic 2 (tentative).

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

The same 21 items in the same order, as the 100 microservice stories that carry them. Inside an item the contract story comes first, then the application, database, infrastructure, DevOps and integration stories.

| # | Key | New story | Work type | Service | Suggested owner | Parallel lane | Ready to start |
|---|---|---|---|---|---|---|---|
| 73 | RWB-E2-037 | RWB-PLT-E2037-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 73 | RWB-E2-037 | RWB-PLT-E2037-APP | App development | PLT platform | TechX | L-PLT-WF-F | Day 1 |
| 74 | RWB-E2-038 | RWB-PLT-E2038-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 74 | RWB-E2-038 | RWB-PLT-E2038-APP | App development | PLT platform | TechX | L-PLT-WF-G | Day 1 |
| 74 | RWB-E2-038 | RWB-ITG-E2038-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 75 | RWB-E2-039 | RWB-PLT-E2039-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 75 | RWB-E2-039 | RWB-PLT-E2039-APP | App development | PLT platform | TechX | L-PLT-WF-H | Day 1 |
| 76 | RWB-E2-040 | RWB-PLT-E2040-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| 76 | RWB-E2-040 | RWB-PLT-E2040-APP | App development | PLT platform | TechX | L-PLT-WF-I | Day 1 |
| 77 | RWB-E2-041 | RWB-P3-E2041-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 77 | RWB-E2-041 | RWB-P3-E2041-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1073-APP |
| 77 | RWB-E2-041 | RWB-P4-E2041-APP | App development | P4 rwb-access | TechX | L-P4-AX | Day 1 |
| 77 | RWB-E2-041 | RWB-P7-E2041-APP | App development | P7 rwb-decision | TechX | L-P7-AN | Day 1 |
| 77 | RWB-E2-041 | RWB-ITG-E2041-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 78 | RWB-E2-042 | RWB-P3-E2042-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 78 | RWB-E2-042 | RWB-P3-E2042-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1073-APP |
| 78 | RWB-E2-042 | RWB-P4-E2042-APP | App development | P4 rwb-access | TechX | L-P4-AY | Day 1 |
| 78 | RWB-E2-042 | RWB-P6-E2042-APP | App development | P6 rwb-comms | TechX | L-P6-R | Day 1 |
| 78 | RWB-E2-042 | RWB-P7-E2042-APP | App development | P7 rwb-decision | TechX | L-P7-AO | Day 1 |
| 78 | RWB-E2-042 | RWB-P3-E2042-INF | Infrastructure | P3 rwb-case | SCB IT infrastructure | L-P3-AP | Day 1 |
| 78 | RWB-E2-042 | RWB-P3-E2042-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-AO | Day 1 |
| 78 | RWB-E2-042 | RWB-ITG-E2042-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 79 | RWB-TE-010 | RWB-ITG-TE010-ITG | Integration | ITG integration | QA team | L-ITG-NFR | Day 1 |
| 80 | RWB-E2-003 | RWB-P2-E2003-APP | App development | P2 rwb-integration | TechX | L-P2-A | After RWB-P2-E1007-APP |
| 80 | RWB-E2-003 | RWB-P4-E2003-APP | App development | P4 rwb-access | TechX | L-P4-AE | Day 1 |
| 80 | RWB-E2-003 | RWB-ITG-E2003-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 81 | RWB-TE-009 | RWB-ITG-TE009-ITG | Integration | ITG integration | QA team | L-ITG-NFR | Day 1 |
| 82 | RWB-E2-005 | RWB-P7-E2005-CON | Contract | P7 rwb-decision | TechX | CG-W2 | Day 1 |
| 82 | RWB-E2-005 | RWB-P7-E2005-APP | App development | P7 rwb-decision | TechX | L-P7-B | After RWB-P7-E1008-APP |
| 82 | RWB-E2-005 | RWB-ITG-E2005-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 83 | RWB-E2-004 | RWB-P3-E2004-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 83 | RWB-E2-004 | RWB-P3-E2004-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1018-APP, RWB-P3-E1045-APP, RWB-P3-E2042-APP |
| 83 | RWB-E2-004 | RWB-P4-E2004-APP | App development | P4 rwb-access | TechX | L-P4-AF | Day 1 |
| 83 | RWB-E2-004 | RWB-P7-E2004-APP | App development | P7 rwb-decision | TechX | L-P7-S | Day 1 |
| 83 | RWB-E2-004 | RWB-S2-E2004-APP | App development | S2 rwb-treatment | TechX | L-S2-A | Day 1 |
| 83 | RWB-E2-004 | RWB-P3-E2004-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-Z | Day 1 |
| 83 | RWB-E2-004 | RWB-ITG-E2004-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 84 | RWB-E2-011 | RWB-P3-E2011-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 84 | RWB-E2-011 | RWB-P3-E2011-APP | App development | P3 rwb-case | TechX | L-P3-F | After RWB-P3-E1020-APP |
| 85 | RWB-E2-013 | RWB-P7-E2013-CON | Contract | P7 rwb-decision | TechX | CG-W2 | Day 1 |
| 85 | RWB-E2-013 | RWB-P3-E2013-APP | App development | P3 rwb-case | TechX | L-P3-AF | Day 1 |
| 85 | RWB-E2-013 | RWB-P4-E2013-APP | App development | P4 rwb-access | TechX | L-P4-AI | Day 1 |
| 85 | RWB-E2-013 | RWB-P6-E2013-APP | App development | P6 rwb-comms | TechX | L-P6-K | Day 1 |
| 85 | RWB-E2-013 | RWB-P7-E2013-APP | App development | P7 rwb-decision | TechX | L-P7-X | Day 1 |
| 85 | RWB-E2-013 | RWB-P7-E2013-OPS | DevOps | P7 rwb-decision | DevOps team | L-P7-Y | Day 1 |
| 85 | RWB-E2-013 | RWB-ITG-E2013-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 86 | RWB-E2-012 | RWB-P3-E2012-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 86 | RWB-E2-012 | RWB-P3-E2012-APP | App development | P3 rwb-case | TechX | L-P3-AD | Day 1 |
| 86 | RWB-E2-012 | RWB-P7-E2012-APP | App development | P7 rwb-decision | TechX | L-P7-W | Day 1 |
| 86 | RWB-E2-012 | RWB-S8-E2012-APP | App development | S8 rwb-deviation | TechX | L-S8-G | Day 1 |
| 86 | RWB-E2-012 | RWB-P3-E2012-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-AE | Day 1 |
| 86 | RWB-E2-012 | RWB-ITG-E2012-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 87 | RWB-E2-033 | RWB-P2-E2033-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 87 | RWB-E2-033 | RWB-P2-E2033-APP | App development | P2 rwb-integration | TechX | L-P2-H | Day 1 |
| 87 | RWB-E2-033 | RWB-P3-E2033-APP | App development | P3 rwb-case | TechX | L-P3-AK | Day 1 |
| 87 | RWB-E2-033 | RWB-P4-E2033-APP | App development | P4 rwb-access | TechX | L-P4-AT | Day 1 |
| 87 | RWB-E2-033 | RWB-S8-E2033-APP | App development | S8 rwb-deviation | TechX | L-S8-J | Day 1 |
| 87 | RWB-E2-033 | RWB-ITG-E2033-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 88 | RWB-E2-015 | RWB-P3-E2015-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 88 | RWB-E2-015 | RWB-P3-E2015-APP | App development | P3 rwb-case | TechX | L-P3-AD | Day 1 |
| 88 | RWB-E2-015 | RWB-P4-E2015-APP | App development | P4 rwb-access | TechX | L-P4-AK | Day 1 |
| 88 | RWB-E2-015 | RWB-S8-E2015-APP | App development | S8 rwb-deviation | TechX | L-S8-H | Day 1 |
| 88 | RWB-E2-015 | RWB-P3-E2015-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-AH | Day 1 |
| 88 | RWB-E2-015 | RWB-ITG-E2015-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 89 | RWB-E2-001 | RWB-P2-E2001-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 89 | RWB-E2-001 | RWB-P1-E2001-APP | App development | P1 rwb-source-data | TechX | L-P1-S | Day 1 |
| 89 | RWB-E2-001 | RWB-P2-E2001-APP | App development | P2 rwb-integration | TechX | L-P2-A | After RWB-P2-E1007-APP |
| 89 | RWB-E2-001 | RWB-P3-E2001-APP | App development | P3 rwb-case | TechX | L-P3-X | Day 1 |
| 89 | RWB-E2-001 | RWB-P7-E2001-APP | App development | P7 rwb-decision | TechX | L-P7-Q | Day 1 |
| 89 | RWB-E2-001 | RWB-P2-E2001-OPS | DevOps | P2 rwb-integration | DevOps team | L-P2-E | Day 1 |
| 89 | RWB-E2-001 | RWB-ITG-E2001-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 90 | RWB-E2-014 | RWB-P7-E2014-CON | Contract | P7 rwb-decision | TechX | CG-W2 | Day 1 |
| 90 | RWB-E2-014 | RWB-P3-E2014-APP | App development | P3 rwb-case | TechX | L-P3-AG | Day 1 |
| 90 | RWB-E2-014 | RWB-P4-E2014-APP | App development | P4 rwb-access | TechX | L-P4-AJ | Day 1 |
| 90 | RWB-E2-014 | RWB-P6-E2014-APP | App development | P6 rwb-comms | TechX | L-P6-L | Day 1 |
| 90 | RWB-E2-014 | RWB-P7-E2014-APP | App development | P7 rwb-decision | TechX | L-P7-X | After RWB-P7-E2013-APP |
| 90 | RWB-E2-014 | RWB-P7-E2014-OPS | DevOps | P7 rwb-decision | DevOps team | L-P7-Z | Day 1 |
| 90 | RWB-E2-014 | RWB-ITG-E2014-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 91 | RWB-E2-022 | RWB-P6-E2022-CON | Contract | P6 rwb-comms | TechX | CG-W2 | Day 1 |
| 91 | RWB-E2-022 | RWB-P1-E2022-APP | App development | P1 rwb-source-data | TechX | L-P1-X | Day 1 |
| 91 | RWB-E2-022 | RWB-P4-E2022-APP | App development | P4 rwb-access | TechX | L-P4-AO | Day 1 |
| 91 | RWB-E2-022 | RWB-P6-E2022-APP | App development | P6 rwb-comms | TechX | L-P6-A | After RWB-P6-E1052-APP |
| 91 | RWB-E2-022 | RWB-P7-E2022-APP | App development | P7 rwb-decision | TechX | L-P7-AD | Day 1 |
| 91 | RWB-E2-022 | RWB-P6-E2022-OPS | DevOps | P6 rwb-comms | DevOps team | L-P6-P | Day 1 |
| 91 | RWB-E2-022 | RWB-ITG-E2022-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 92 | RWB-E2-002 | RWB-P2-E2002-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 92 | RWB-E2-002 | RWB-P2-E2002-APP | App development | P2 rwb-integration | TechX | L-P2-A | After RWB-P2-E2001-APP |
| 92 | RWB-E2-002 | RWB-P3-E2002-APP | App development | P3 rwb-case | TechX | L-P3-Y | Day 1 |
| 92 | RWB-E2-002 | RWB-P4-E2002-APP | App development | P4 rwb-access | TechX | L-P4-AD | Day 1 |
| 92 | RWB-E2-002 | RWB-P7-E2002-APP | App development | P7 rwb-decision | TechX | L-P7-R | Day 1 |
| 92 | RWB-E2-002 | RWB-P2-E2002-OPS | DevOps | P2 rwb-integration | DevOps team | L-P2-F | Day 1 |
| 92 | RWB-E2-002 | RWB-ITG-E2002-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 93 | RWB-E2-021 | RWB-P6-E2021-CON | Contract | P6 rwb-comms | TechX | CG-W2 | Day 1 |
| 93 | RWB-E2-021 | RWB-P1-E2021-APP | App development | P1 rwb-source-data | TechX | L-P1-W | Day 1 |
| 93 | RWB-E2-021 | RWB-P3-E2021-APP | App development | P3 rwb-case | TechX | L-P3-AI | Day 1 |
| 93 | RWB-E2-021 | RWB-P4-E2021-APP | App development | P4 rwb-access | TechX | L-P4-AN | Day 1 |
| 93 | RWB-E2-021 | RWB-P6-E2021-APP | App development | P6 rwb-comms | TechX | L-P6-A | After RWB-P6-E1052-APP, RWB-P6-E1055-APP |
| 93 | RWB-E2-021 | RWB-P7-E2021-APP | App development | P7 rwb-decision | TechX | L-P7-AC | Day 1 |
| 93 | RWB-E2-021 | RWB-P6-E2021-OPS | DevOps | P6 rwb-comms | DevOps team | L-P6-O | Day 1 |
| 93 | RWB-E2-021 | RWB-ITG-E2021-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |

## Window 4, 14 to 25 December 2026 (tentative)

19 items, releasing in Epic 2 (tentative).

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

The same 19 items in the same order, as the 121 microservice stories that carry them. Inside an item the contract story comes first, then the application, database, infrastructure, DevOps and integration stories.

| # | Key | New story | Work type | Service | Suggested owner | Parallel lane | Ready to start |
|---|---|---|---|---|---|---|---|
| 94 | RWB-E2-019 | RWB-P4-E2019-CON | Contract | P4 rwb-access | TechX | CG-W2 | Day 1 |
| 94 | RWB-E2-019 | RWB-P4-E2019-APP | App development | P4 rwb-access | TechX | L-P4-A | After RWB-P4-E1022-APP, RWB-P4-E1039-APP |
| 94 | RWB-E2-019 | RWB-P7-E2019-APP | App development | P7 rwb-decision | TechX | L-P7-AB | Day 1 |
| 94 | RWB-E2-019 | RWB-S9-E2019-APP | App development | S9 rwb-partner | TechX | L-S9-D | Day 1 |
| 94 | RWB-E2-019 | RWB-P4-E2019-INF | Infrastructure | P4 rwb-access | SCB IT infrastructure | L-P4-AM | Day 1 |
| 94 | RWB-E2-019 | RWB-ITG-E2019-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 95 | RWB-E2-036 | RWB-P2-E2036-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 95 | RWB-E2-036 | RWB-P2-E2036-APP | App development | P2 rwb-integration | TechX | L-P2-K | Day 1 |
| 95 | RWB-E2-036 | RWB-P3-E2036-APP | App development | P3 rwb-case | TechX | L-P3-AN | Day 1 |
| 95 | RWB-E2-036 | RWB-P4-E2036-APP | App development | P4 rwb-access | TechX | L-P4-AW | Day 1 |
| 95 | RWB-E2-036 | RWB-P7-E2036-APP | App development | P7 rwb-decision | TechX | L-P7-AM | Day 1 |
| 95 | RWB-E2-036 | RWB-S8-E2036-APP | App development | S8 rwb-deviation | TechX | L-S8-K | Day 1 |
| 95 | RWB-E2-036 | RWB-ITG-E2036-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 96 | RWB-E2-006 | RWB-P2-E2006-APP | App development | P2 rwb-integration | TechX | L-P2-A | After RWB-P2-E1007-APP |
| 96 | RWB-E2-006 | RWB-P3-E2006-APP | App development | P3 rwb-case | TechX | L-P3-AA | Day 1 |
| 96 | RWB-E2-006 | RWB-P7-E2006-APP | App development | P7 rwb-decision | TechX | L-P7-T | Day 1 |
| 96 | RWB-E2-006 | RWB-S2-E2006-APP | App development | S2 rwb-treatment | TechX | L-S2-B | Day 1 |
| 96 | RWB-E2-006 | RWB-ITG-E2006-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 97 | RWB-E2-007 | RWB-P2-E2007-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 97 | RWB-E2-007 | RWB-P1-E2007-APP | App development | P1 rwb-source-data | TechX | L-P1-T | Day 1 |
| 97 | RWB-E2-007 | RWB-P2-E2007-APP | App development | P2 rwb-integration | TechX | L-P2-A | After RWB-P2-E1007-APP |
| 97 | RWB-E2-007 | RWB-P3-E2007-APP | App development | P3 rwb-case | TechX | L-P3-AB | Day 1 |
| 97 | RWB-E2-007 | RWB-P4-E2007-APP | App development | P4 rwb-access | TechX | L-P4-AG | Day 1 |
| 97 | RWB-E2-007 | RWB-P7-E2007-APP | App development | P7 rwb-decision | TechX | L-P7-U | Day 1 |
| 97 | RWB-E2-007 | RWB-S2-E2007-APP | App development | S2 rwb-treatment | TechX | L-S2-C | Day 1 |
| 97 | RWB-E2-007 | RWB-P2-E2007-OPS | DevOps | P2 rwb-integration | DevOps team | L-P2-G | Day 1 |
| 97 | RWB-E2-007 | RWB-ITG-E2007-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 98 | RWB-E2-008 | RWB-P8-E2008-CON | Contract | P8 rwb-payment | TechX | CG-W2 | Day 1 |
| 98 | RWB-E2-008 | RWB-P1-E2008-APP | App development | P1 rwb-source-data | TechX | L-P1-U | Day 1 |
| 98 | RWB-E2-008 | RWB-P4-E2008-APP | App development | P4 rwb-access | TechX | L-P4-AH | Day 1 |
| 98 | RWB-E2-008 | RWB-P7-E2008-APP | App development | P7 rwb-decision | TechX | L-P7-V | Day 1 |
| 98 | RWB-E2-008 | RWB-P8-E2008-APP | App development | P8 rwb-payment | TechX | L-P8-C | Day 1 |
| 98 | RWB-E2-008 | RWB-S2-E2008-APP | App development | S2 rwb-treatment | TechX | L-S2-D | Day 1 |
| 98 | RWB-E2-008 | RWB-P8-E2008-OPS | DevOps | P8 rwb-payment | DevOps team | L-P8-D | Day 1 |
| 98 | RWB-E2-008 | RWB-ITG-E2008-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 99 | RWB-E2-032 | RWB-P10-E2032-CON | Contract | P10 rwb-agent | TechX | CG-W2 | Day 1 |
| 99 | RWB-E2-032 | RWB-P10-E2032-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP |
| 99 | RWB-E2-032 | RWB-P7-E2032-APP | App development | P7 rwb-decision | TechX | L-P7-AK | Day 1 |
| 99 | RWB-E2-032 | RWB-S2-E2032-APP | App development | S2 rwb-treatment | TechX | L-S2-K | Day 1 |
| 99 | RWB-E2-032 | RWB-P10-E2032-INF | Infrastructure | P10 rwb-agent | SCB IT infrastructure | L-P10-G | Day 1 |
| 99 | RWB-E2-032 | RWB-ITG-E2032-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 100 | RWB-E2-010 | RWB-P1-E2010-CON | Contract | P1 rwb-source-data | TechX | CG-W2 | Day 1 |
| 100 | RWB-E2-010 | RWB-P1-E2010-APP | App development | P1 rwb-source-data | TechX | L-P1-A | After RWB-P1-E1069-APP, RWB-P1-E1015-APP |
| 100 | RWB-E2-010 | RWB-S2-E2010-APP | App development | S2 rwb-treatment | TechX | L-S2-E | Day 1 |
| 100 | RWB-E2-010 | RWB-S3-E2010-APP | App development | S3 rwb-guarantee | TechX | L-S3-A | Day 1 |
| 100 | RWB-E2-010 | RWB-P1-E2010-OPS | DevOps | P1 rwb-source-data | DevOps team | L-P1-V | Day 1 |
| 100 | RWB-E2-010 | RWB-ITG-E2010-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 101 | RWB-E2-027 | RWB-P8-E2027-CON | Contract | P8 rwb-payment | TechX | CG-W2 | Day 1 |
| 101 | RWB-E2-027 | RWB-P4-E2027-APP | App development | P4 rwb-access | TechX | L-P4-AR | Day 1 |
| 101 | RWB-E2-027 | RWB-P7-E2027-APP | App development | P7 rwb-decision | TechX | L-P7-AH | Day 1 |
| 101 | RWB-E2-027 | RWB-P8-E2027-APP | App development | P8 rwb-payment | TechX | L-P8-C | After RWB-P8-E2008-APP |
| 101 | RWB-E2-027 | RWB-S2-E2027-APP | App development | S2 rwb-treatment | TechX | L-S2-J | Day 1 |
| 101 | RWB-E2-027 | RWB-P8-E2027-OPS | DevOps | P8 rwb-payment | DevOps team | L-P8-E | Day 1 |
| 101 | RWB-E2-027 | RWB-ITG-E2027-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 102 | RWB-E2-035 | RWB-P2-E2035-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 102 | RWB-E2-035 | RWB-P2-E2035-APP | App development | P2 rwb-integration | TechX | L-P2-H | After RWB-P2-E2033-APP |
| 102 | RWB-E2-035 | RWB-P3-E2035-APP | App development | P3 rwb-case | TechX | L-P3-AM | Day 1 |
| 102 | RWB-E2-035 | RWB-P4-E2035-APP | App development | P4 rwb-access | TechX | L-P4-AV | Day 1 |
| 102 | RWB-E2-035 | RWB-P7-E2035-APP | App development | P7 rwb-decision | TechX | L-P7-AL | Day 1 |
| 102 | RWB-E2-035 | RWB-P2-E2035-OPS | DevOps | P2 rwb-integration | DevOps team | L-P2-J | Day 1 |
| 102 | RWB-E2-035 | RWB-ITG-E2035-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 103 | RWB-E2-016 | RWB-P3-E2016-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 103 | RWB-E2-016 | RWB-P3-E2016-APP | App development | P3 rwb-case | TechX | L-P3-AD | After RWB-P3-E2015-APP, RWB-P3-E2012-APP |
| 103 | RWB-E2-016 | RWB-P5-E2016-APP | App development | P5 rwb-document | TechX | L-P5-V | Day 1 |
| 103 | RWB-E2-016 | RWB-ITG-E2016-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 104 | RWB-E2-024 | RWB-P5-E2024-CON | Contract | P5 rwb-document | TechX | CG-W2 | Day 1 |
| 104 | RWB-E2-024 | RWB-P3-E2024-APP | App development | P3 rwb-case | TechX | L-P3-AJ | Day 1 |
| 104 | RWB-E2-024 | RWB-P4-E2024-APP | App development | P4 rwb-access | TechX | L-P4-AP | Day 1 |
| 104 | RWB-E2-024 | RWB-P5-E2024-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1032-APP, RWB-P5-E1024-APP |
| 104 | RWB-E2-024 | RWB-P7-E2024-APP | App development | P7 rwb-decision | TechX | L-P7-AE | Day 1 |
| 104 | RWB-E2-024 | RWB-ITG-E2024-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 105 | RWB-E2-026 | RWB-P5-E2026-CON | Contract | P5 rwb-document | TechX | CG-W2 | Day 1 |
| 105 | RWB-E2-026 | RWB-P4-E2026-APP | App development | P4 rwb-access | TechX | L-P4-AQ | Day 1 |
| 105 | RWB-E2-026 | RWB-P5-E2026-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E1024-APP |
| 105 | RWB-E2-026 | RWB-P6-E2026-APP | App development | P6 rwb-comms | TechX | L-P6-Q | Day 1 |
| 105 | RWB-E2-026 | RWB-P7-E2026-APP | App development | P7 rwb-decision | TechX | L-P7-AG | Day 1 |
| 105 | RWB-E2-026 | RWB-S2-E2026-APP | App development | S2 rwb-treatment | TechX | L-S2-I | Day 1 |
| 105 | RWB-E2-026 | RWB-ITG-E2026-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 106 | RWB-E2-009 | RWB-P9-E2009-CON | Contract | P9 rwb-reporting | TechX | CG-W2 | Day 1 |
| 106 | RWB-E2-009 | RWB-P3-E2009-APP | App development | P3 rwb-case | TechX | L-P3-AC | Day 1 |
| 106 | RWB-E2-009 | RWB-P9-E2009-APP | App development | P9 rwb-reporting | TechX | L-P9-A | After RWB-P9-E1013-APP |
| 106 | RWB-E2-009 | RWB-S8-E2009-APP | App development | S8 rwb-deviation | TechX | L-S8-F | Day 1 |
| 106 | RWB-E2-009 | RWB-P9-E2009-OPS | DevOps | P9 rwb-reporting | DevOps team | L-P9-C | Day 1 |
| 106 | RWB-E2-009 | RWB-ITG-E2009-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 107 | RWB-E2-017 | RWB-P5-E2017-CON | Contract | P5 rwb-document | TechX | CG-W2 | Day 1 |
| 107 | RWB-E2-017 | RWB-P4-E2017-APP | App development | P4 rwb-access | TechX | L-P4-AL | Day 1 |
| 107 | RWB-E2-017 | RWB-P5-E2017-APP | App development | P5 rwb-document | TechX | L-P5-G | After RWB-P5-E2026-APP |
| 107 | RWB-E2-017 | RWB-P6-E2017-APP | App development | P6 rwb-comms | TechX | L-P6-M | Day 1 |
| 107 | RWB-E2-017 | RWB-P7-E2017-APP | App development | P7 rwb-decision | TechX | L-P7-AA | Day 1 |
| 107 | RWB-E2-017 | RWB-S2-E2017-APP | App development | S2 rwb-treatment | TechX | L-S2-F | Day 1 |
| 107 | RWB-E2-017 | RWB-ITG-E2017-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 108 | RWB-E2-025 | RWB-P5-E2025-CON | Contract | P5 rwb-document | TechX | CG-W2 | Day 1 |
| 108 | RWB-E2-025 | RWB-P5-E2025-APP | App development | P5 rwb-document | TechX | L-P5-Y | Day 1 |
| 108 | RWB-E2-025 | RWB-P7-E2025-APP | App development | P7 rwb-decision | TechX | L-P7-AF | Day 1 |
| 108 | RWB-E2-025 | RWB-S2-E2025-APP | App development | S2 rwb-treatment | TechX | L-S2-H | Day 1 |
| 108 | RWB-E2-025 | RWB-S4-E2025-APP | App development | S4 rwb-litigation | TechX | L-S4-A | Day 1 |
| 108 | RWB-E2-025 | RWB-P5-E2025-OPS | DevOps | P5 rwb-document | DevOps team | L-P5-X | Day 1 |
| 108 | RWB-E2-025 | RWB-ITG-E2025-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 109 | RWB-E2-031 | RWB-P10-E2031-CON | Contract | P10 rwb-agent | TechX | CG-W2 | Day 1 |
| 109 | RWB-E2-031 | RWB-P10-E2031-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1063-APP |
| 109 | RWB-E2-031 | RWB-P4-E2031-APP | App development | P4 rwb-access | TechX | L-P4-AS | Day 1 |
| 109 | RWB-E2-031 | RWB-P10-E2031-OPS | DevOps | P10 rwb-agent | DevOps team | L-P10-F | Day 1 |
| 109 | RWB-E2-031 | RWB-ITG-E2031-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 110 | RWB-E2-034 | RWB-P2-E2034-CON | Contract | P2 rwb-integration | TechX | CG-W2 | Day 1 |
| 110 | RWB-E2-034 | RWB-P1-E2034-APP | App development | P1 rwb-source-data | TechX | L-P1-Y | Day 1 |
| 110 | RWB-E2-034 | RWB-P2-E2034-APP | App development | P2 rwb-integration | TechX | L-P2-A | After RWB-P2-E1007-APP |
| 110 | RWB-E2-034 | RWB-P3-E2034-APP | App development | P3 rwb-case | TechX | L-P3-AL | Day 1 |
| 110 | RWB-E2-034 | RWB-P4-E2034-APP | App development | P4 rwb-access | TechX | L-P4-AU | Day 1 |
| 110 | RWB-E2-034 | RWB-S9-E2034-APP | App development | S9 rwb-partner | TechX | L-S9-E | Day 1 |
| 110 | RWB-E2-034 | RWB-P2-E2034-OPS | DevOps | P2 rwb-integration | DevOps team | L-P2-I | Day 1 |
| 110 | RWB-E2-034 | RWB-ITG-E2034-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 111 | RWB-E2-018 | RWB-P5-E2018-APP | App development | P5 rwb-document | TechX | L-P5-W | Day 1 |
| 111 | RWB-E2-018 | RWB-P6-E2018-APP | App development | P6 rwb-comms | TechX | L-P6-A | After RWB-P6-E2022-APP |
| 111 | RWB-E2-018 | RWB-S2-E2018-APP | App development | S2 rwb-treatment | TechX | L-S2-G | Day 1 |
| 111 | RWB-E2-018 | RWB-P6-E2018-OPS | DevOps | P6 rwb-comms | DevOps team | L-P6-N | Day 1 |
| 111 | RWB-E2-018 | RWB-ITG-E2018-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 112 | RWB-E2-043 | RWB-P3-E2043-CON | Contract | P3 rwb-case | TechX | CG-W2 | Day 1 |
| 112 | RWB-E2-043 | RWB-P3-E2043-APP | App development | P3 rwb-case | TechX | L-P3-AR | Day 1 |
| 112 | RWB-E2-043 | RWB-P7-E2043-APP | App development | P7 rwb-decision | TechX | L-P7-AP | Day 1 |
| 112 | RWB-E2-043 | RWB-P3-E2043-OPS | DevOps | P3 rwb-case | DevOps team | L-P3-AQ | Day 1 |
| 112 | RWB-E2-043 | RWB-ITG-E2043-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |

## Epic 3, 28 December 2026 to 22 January 2027 (tentative)

3 items, releasing in Epic 3 (tentative).

| # | Key | Title | Module | E or S | Waits on |
|---|---|---|---|---|---|
| 113 | RWB-E2-028 | Case intake agent live at L1 [E3a] | P10 | S | E1-061, E1-035, E1-027, E2-031 |
| 114 | RWB-E2-030 | Legal document agent in shadow on Epic 1 data [E3c] | P10 | S | E1-058, E2-025, E1-061 |
| 115 | RWB-E2-029 | Deviation screening agent evaluation and L1 on one segment [E3b] | P10 | S | E1-062, E2-015, E1-061, E2-028 |

The same 3 items in the same order, as the 14 microservice stories that carry them. Inside an item the contract story comes first, then the application, database, infrastructure, DevOps and integration stories.

| # | Key | New story | Work type | Service | Suggested owner | Parallel lane | Ready to start |
|---|---|---|---|---|---|---|---|
| 113 | RWB-E2-028 | RWB-P10-E2028-CON | Contract | P10 rwb-agent | TechX | CG-W2 | Day 1 |
| 113 | RWB-E2-028 | RWB-P10-E2028-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E2031-APP |
| 113 | RWB-E2-028 | RWB-P7-E2028-APP | App development | P7 rwb-decision | TechX | L-P7-AI | Day 1 |
| 113 | RWB-E2-028 | RWB-P10-E2028-OPS | DevOps | P10 rwb-agent | DevOps team | L-P10-E | Day 1 |
| 113 | RWB-E2-028 | RWB-ITG-E2028-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 114 | RWB-E2-030 | RWB-P10-E2030-CON | Contract | P10 rwb-agent | TechX | CG-W2 | Day 1 |
| 114 | RWB-E2-030 | RWB-P10-E2030-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1058-APP |
| 114 | RWB-E2-030 | RWB-P5-E2030-APP | App development | P5 rwb-document | TechX | L-P5-Z | Day 1 |
| 114 | RWB-E2-030 | RWB-ITG-E2030-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |
| 115 | RWB-E2-029 | RWB-P10-E2029-CON | Contract | P10 rwb-agent | TechX | CG-W2 | Day 1 |
| 115 | RWB-E2-029 | RWB-P10-E2029-APP | App development | P10 rwb-agent | TechX | L-P10-A | After RWB-P10-E1062-APP |
| 115 | RWB-E2-029 | RWB-P7-E2029-APP | App development | P7 rwb-decision | TechX | L-P7-AJ | Day 1 |
| 115 | RWB-E2-029 | RWB-S8-E2029-APP | App development | S8 rwb-deviation | TechX | L-S8-I | Day 1 |
| 115 | RWB-E2-029 | RWB-ITG-E2029-ITG | Integration | ITG integration | TechX | L-ITG-W2 | Day 1 |

## Lanes and Day 1 in this version

This version gives every story its lane and its Day-1 position. The 115 items are carried by 530 stories: 460 are Day 1 and 70 wait for a story in their own lane, in 282 lanes. The 92 contract stories of these items carry no build dependency and sit in the contract groups CG-W0 to CG-W4, one per wave; a contract story is always Day 1, and its fake lets the application story start beside it (Template and Rules §R5.7 rules 1, 2 and 8).

| Team type | Day-1 stories of the 115 items | Work types |
|---|---|---|
| TechX | 392 | Contract, App development, Integration |
| ACE team | 7 | ACE DB |
| SCB IT infrastructure | 10 | Infrastructure |
| DevOps team | 49 | DevOps |
| QA team | 2 | Integration harness and non-functional stories |
| All | 460 | All six work types |

The board limit of a team type, and the number of stories a team type may hold at once, is Not specified in the source documents (CG-C4-SBO-6; ASM-C4-SBO-6). The board limit per squad of version 3 is kept unchanged.

The whole story set of this run, which carries the later epics and the new platform and harness stories beside the 115 items, has 1034 stories in 510 lanes, of which 939 are Day 1. Its position by wave:

| Wave | Stories | Lanes used | Contract group | Day 1 | Waits for a story in its lane |
|---|---|---|---|---|---|
| Wave 0 | 65 | 49 | CG-W0 | 65 | 0 |
| Wave 1 | 266 | 127 | CG-W1 | 225 | 41 |
| Wave 2 | 293 | 167 | CG-W2 | 264 | 29 |
| Wave 3 | 159 | 81 | CG-W3 | 159 | 0 |
| Wave 4 | 251 | 100 | CG-W4 | 226 | 25 |
| All | 1034 | 510 | CG-W0 to CG-W4 | 939 | 95 |

Every service has at least one contract story, and every team type has Day-1 work (Template and Rules §R5.7 rules 6 and 7). A lane is named after the service that owns it and a letter, for example L-P3-F for rwb-case; a lane of the platform epics is L-PLT-<epic>-<letter> and a lane of the integration epics is L-ITG-W<n>, with L-ITG-NFR for the non-functional stories. The longest chain of build dependencies inside any lane of the set is four stories.

## Day-1 work that is new in this version

These stories carry no item of version 3 and they are all Day 1. N001 to N012 are the platform stories of wave 0, and W1J01 to W4J01 are the integration harness and journey stories, one pair per wave. They are what makes sure every team type has Day-1 work: the infrastructure stories for SCB IT infrastructure, the DevOps stories for the DevOps team, the ACE DB story for the ACE team, and W1J01 with the harness stories for QA (Template and Rules §R5.7 rule 6). They sit before the five windows of this document, because wave 0 is not a release (CG-C4-SBO-8; ASM-C4-SBO-8).

| Legacy key | New story | Work type | Service | Suggested owner | Parallel lane | Ready to start |
|---|---|---|---|---|---|---|
| N001 | RWB-PLT-N001-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| N001 | RWB-PLT-N001-APP | App development | PLT platform | TechX | L-PLT-EDGE-A | Day 1 |
| N002 | RWB-PLT-N002-INF | Infrastructure | PLT platform | SCB IT infrastructure | L-PLT-EVT-A | Day 1 |
| N003 | RWB-PLT-N003-INF | Infrastructure | PLT platform | SCB IT infrastructure | L-PLT-WF-A | Day 1 |
| N004 | RWB-PLT-N004-OPS | DevOps | PLT platform | DevOps team | L-PLT-TPL-A | Day 1 |
| N005 | RWB-PLT-N005-OPS | DevOps | PLT platform | DevOps team | L-PLT-OBS-A | Day 1 |
| N006 | RWB-PLT-N006-INF | Infrastructure | PLT platform | SCB IT infrastructure | L-PLT-EDGE-B | Day 1 |
| N007 | RWB-PLT-N007-INF | Infrastructure | PLT platform | SCB IT infrastructure | L-PLT-EDGE-C | Day 1 |
| N008 | RWB-PLT-N008-INF | Infrastructure | PLT platform | SCB IT infrastructure | L-PLT-EVT-B | Day 1 |
| N009 | RWB-PLT-N009-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| N009 | RWB-PLT-N009-APP | App development | PLT platform | TechX | L-PLT-LIB-A | Day 1 |
| N010 | RWB-PLT-N010-CON | Contract | PLT platform | TechX | CG-W0 | Day 1 |
| N010 | RWB-PLT-N010-APP | App development | PLT platform | TechX | L-PLT-WF-B | Day 1 |
| N011 | RWB-PLT-N011-DB | ACE DB | PLT platform | ACE team | L-PLT-DB-A | Day 1 |
| N012 | RWB-PLT-N012-INF | Infrastructure | PLT platform | SCB IT infrastructure | L-PLT-EVT-C | Day 1 |
| W1J01 | RWB-ITG-W1J01-ITG | Integration | ITG integration | QA team | L-ITG-W1 | Day 1 |
| W1J02 | RWB-ITG-W1J02-ITG | Integration | ITG integration | QA team | L-ITG-W1 | Day 1 |
| W2J01 | RWB-ITG-W2J01-ITG | Integration | ITG integration | QA team | L-ITG-W2 | Day 1 |
| W3J01 | RWB-ITG-W3J01-ITG | Integration | ITG integration | QA team | L-ITG-W3 | Day 1 |
| W4J01 | RWB-ITG-W4J01-ITG | Integration | ITG integration | QA team | L-ITG-W4 | Day 1 |

## How to use it

Take the next item in order whose dependencies are done. Work in progress per squad stays within the board limit. An item on the critical path is taken before any other item. An item that will miss its release stays behind its flag and moves to the next release. The two squads agree the split at the daily board; the product owner settles a disagreement the same day.

The critical path starts outside the squads. RWB-ACE-001, the ACE team's 14 tables, 12 columns and read grant, is due on 21 November under DL43 and gates RWB-E1-069, the 30 read-only views. RWB-E1-069 gates RWB-E1-018 and RWB-E1-002, the case record and the case list. RWB-E1-072 and RWB-E1-073 gate RWB-E1-018, so the four configuration stories RWB-E1-070 to RWB-E1-073 sit on the chain. From RWB-E1-020 the chain runs RWB-E1-028, RWB-E1-030, RWB-E1-059, RWB-E1-061 and RWB-E1-063, then RWB-E2-031, RWB-E2-028 and RWB-E2-029: 17 items end to end. A day lost on RWB-ACE-001, on RWB-E1-069 or on the Temporal and Drools configuration moves the 30 November release.

In this version the two squads are the five team types: TechX, ACE team, SCB IT infrastructure, DevOps team and QA team. The daily board agrees the item order as before, and the product owner settles a disagreement the same day; no source states how a team type is assigned to an item before the board meets (CG-C4-SBO-3; ASM-C4-SBO-3).

An item is pulled by its stories, in the order contract, application, database, infrastructure, DevOps and integration. A Day-1 story may be pulled at once by any team type. A story that is not Day 1 is pulled when the story named in its Ready to start is done, and it never waits for a story of another service: a contract dependency is answered by the published contract and its fake, an integration dependency sits only on an integration story, and external or team-type work is tracked and does not block the build (Template and Rules §R5.4 and §R5.7).

The critical path in the lane terms of this version: RWB-ACE-001 is lane L-P1-A as RWB-P1-ACE001-DB; RWB-E1-069 is lane L-P1-R; RWB-E1-018 is lane L-P3-F; the four configuration stories RWB-E1-070 to RWB-E1-073 are lanes L-PLT-WF-D, L-PLT-WF-E, L-PLT-LIB-I and L-P3-W; RWB-E1-020 and RWB-E1-028 are lanes L-P3-F and L-P3-K; RWB-E1-030 is lane L-P3-L; RWB-E1-059, RWB-E1-061 and RWB-E1-063 are lane L-P10-A; RWB-E2-031 is lane L-P10-F and RWB-E2-028 is lane L-P10-E, with RWB-E2-029 in L-S8-I beside them. RWB-E1-072 is the platform contract RWB-PLT-E1072-CON, so the Drools runtime reaches RWB-E1-018 through that contract and its fake and the chain is not blocked by the platform epic.

Every release date in this document is unchanged and tentative (U7; DL48). Version 3 names no release date for an item: it names the epic a window releases in, and this version keeps that statement as it stands, marked tentative (CG-C4-SBO-7; ASM-C4-SBO-7). The window dates above are the dates of version 3 and are not moved by the realignment.

## Assumptions and gaps

Open points of this document, each carried as a gap row and an assumption row:

- The approval and the status of version 4 (CG-C4-SBO-1; ASM-C4-SBO-1).
- The change log of version 3, which the source does not carry (CG-C4-SBO-2; ASM-C4-SBO-2).
- The two squads of version 3 against the five team types of this version (CG-C4-SBO-3; ASM-C4-SBO-3).
- One module per item against the several services each split story belongs to (CG-C4-SBO-4; ASM-C4-SBO-4).
- The two items that version 3 still lists and D-RCV-60 retires, RWB-E1-014 and RWB-TE-007 (CG-C4-SBO-5; ASM-C4-SBO-5).
- The board limit of a team type (CG-C4-SBO-6; ASM-C4-SBO-6).
- The release date of an item, which version 3 gives only as the epic it releases in (CG-C4-SBO-7; ASM-C4-SBO-7).
- The platform and harness stories N001 to N012 and W1J01 to W4J01, which sit in no window of version 3 (CG-C4-SBO-8; ASM-C4-SBO-8).
- The waits-on column of version 3, which names legacy keys and not the stories that now carry them (CG-C4-SBO-9; ASM-C4-SBO-9).

## Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 3 | 16 November 2026 | Source version. It carries no change-log row of its own; the realignment records that as a gap and an assumption (CG-C4-SBO-2; ASM-C4-SBO-2). | Not specified in the source documents (CG-C4-SBO-2; ASM-C4-SBO-2) |
| 4 | 22 November 2026 | D-RCV-60 microservice realignment: the 115 items kept in their five windows with every key, title, module, E or S flag, waits-on, item number and date, and each item split into its microservice stories with the service of the Ownership Map v1, the suggested owner of the work type, the parallel lane and the Ready to start of every story; the two retired items carry no story; the Day-1 summary and the new platform and harness stories added. | T3 Code / OpenCode / DeepSeek v4.1 Flash |

