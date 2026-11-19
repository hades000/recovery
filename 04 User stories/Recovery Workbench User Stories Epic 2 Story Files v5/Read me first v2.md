# Read me first

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

This folder holds 43 story files for Epic 2, one per story, plus this read-me. Hand a coding agent one story file together with:

| File | Why |
|---|---|
| The functional and technical specification of the story's module | Behavior, components, tables and endpoints of the module |
| Recovery Workbench Logical Data Model and Data Dictionary v8 | Every field and its BR Field ID |
| Recovery Workbench Physical Schema v6 | The tables and columns |
| Recovery Workbench API Specification v4 | Paths, request and response schemas, errors |
| Recovery Workbench Business Rules and Routing Logic | Rule IDs the story cites |
| Recovery Workbench Error and Message Standard v4 | Message IDs and Thai text |
| Recovery Workbench Engineering Practices v5 | Package structure, tests, flags and merge rules |

Build in the order of the Build Sequence. Section 13 of each story is the solution plan; section 16 lists the tests that must pass.

This version applies decision D-RCV-36, ADR-011 and ADR-012: case workflows run on Temporal from Epic 3 with case data kept in the ACE database, rules are evaluated by embedded Drools from versioned rule packages, RWB-E1-029 and RWB-TE-005 are retired into RWB-E1-073 and RWB-E1-048 is retired into RWB-E2-041. Stories rewritten for this version carry v2 in the file name; new stories carry v1.

| File | Story |
|---|---|
| RWB E2 001 EFS hand over with full history from the COLLINS load v1.md | RWB-E2-001 EFS hand-over with full history |
| RWB E2 002 ACE plan status on the case v2.md | RWB-E2-002 ACE plan status on the case |
| RWB E2 003 Customer s other products on the case v1.md | RWB-E2-003 Customer's other products on the case |
| RWB E2 004 Treatment entity and plan timers data model v2.md | RWB-E2-004 Treatment entity and plan timers data model |
| RWB E2 005 Decision log query API for audit v1.md | RWB-E2-005 Decision log query API for audit |
| RWB E2 006 Credit approval pack for NLEADS v1.md | RWB-E2-006 Credit approval pack for NLEADS |
| RWB E2 007 Booking confirmation from the ALS load v2.md | RWB-E2-007 Booking confirmation from the ALS load |
| RWB E2 008 Payment matching with the missed payment event v2.md | RWB-E2-008 Payment matching with the missed payment event |
| RWB E2 009 Steering dashboard v1 data set v1.md | RWB-E2-009 Steering dashboard v1 data set |
| RWB E2 010 Stage 2 data products contracts plans and treatments v1.md | RWB-E2-010 Stage 2 data products: contracts, plans and treatments |
| RWB E2 011 Queue view screens my queue team queues filters and ageing v1.md | RWB-E2-011 Queue view screens: my queue, team queues, filters and ageing |
| RWB E2 012 Manual transfer and reassignment screen with reason v2.md | RWB-E2-012 Manual transfer and reassignment screen with reason |
| RWB E2 013 Approval routing with the delegation of authority table v1.md | RWB-E2-013 Approval routing with the delegation of authority table |
| RWB E2 014 Approval screen for D7 1 demand and recall notices v1.md | RWB-E2-014 Approval screen for D7.1 demand and recall notices |
| RWB E2 015 Timers escalation and the deviation flag on the case record view v1.md | RWB-E2-015 Timers, escalation and the deviation flag on the case record view |
| RWB E2 016 Full case record view with the history timeline v1.md | RWB-E2-016 Full case record view with the history timeline |
| RWB E2 017 Contract CA and mortgage document generation screens v1.md | RWB-E2-017 Contract, CA and mortgage document generation screens |
| RWB E2 018 E signature flow for customers and the bank v1.md | RWB-E2-018 E-signature flow for customers and the bank |
| RWB E2 019 Partner identities through the external gateway v1.md | RWB-E2-019 Partner identities through the external gateway |
| RWB E2 021 Letter dispatch loop with proof of delivery from WIN v1.md | RWB-E2-021 Letter dispatch loop with proof of delivery from WIN |
| RWB E2 022 SMS and LINE dispatch through NSS and LINE OA v1.md | RWB-E2-022 SMS and LINE dispatch through NSS and LINE OA |
| RWB E2 024 Field app photos and bills into the document hub v1.md | RWB-E2-024 Field app photos and bills into the document hub |
| RWB E2 025 Extraction for the stage 2 and 3 document types v1.md | RWB-E2-025 Extraction for the stage 2 and 3 document types |
| RWB E2 026 Document generation engine for contract CA and mortgage templates v1.md | RWB-E2-026 Document generation engine for contract, CA and mortgage templates |
| RWB E2 027 Payment matching rules with the data team v2.md | RWB-E2-027 Payment matching rules with the data team |
| RWB E2 031 Agent monitoring dashboard v2 E3d v1.md | RWB-E2-031 Agent monitoring dashboard v2 [E3d] |
| RWB E2 032 TDR offer suggestion model through the model gateway E3e v1.md | RWB-E2-032 TDR offer-suggestion model through the model gateway [E3e] |
| RWB E2 033 Case and queue list with status owner and ageing v1.md | RWB-E2-033 Case and queue list with status, owner and ageing |
| RWB E2 034 Interaction ledger on the case and from every channel v1.md | RWB-E2-034 Interaction ledger on the case and from every channel |
| RWB E2 035 Next action on the case v2.md | RWB-E2-035 Next action on the case |
| RWB E2 036 Queue write interface for models and agents v1.md | RWB-E2-036 Queue write interface for models and agents |
| RWB E2 037 Temporal observability and run books v1.md | RWB-E2-037 Temporal observability and run books |
| RWB E2 038 Temporal security codec server and admin audit v1.md | RWB-E2-038 Temporal security, codec server and admin audit |
| RWB E2 039 Temporal resilience backup failover upgrade and archive v1.md | RWB-E2-039 Temporal resilience: backup, failover, upgrade and archive |
| RWB E2 040 Workflow versioning and replay test gate v1.md | RWB-E2-040 Workflow versioning and replay test gate |
| RWB E2 041 Rule change governance and audit report v1.md | RWB-E2-041 Rule change governance and audit report |
| RWB E2 042 Epic 2 rule packages in Drools v1.md | RWB-E2-042 Epic 2 rule packages in Drools |
| RWB E2 043 Temporal and Drools integration pattern and reference case workflow v1.md | RWB-E2-043 Temporal and Drools integration pattern and reference case workflow |
| RWB E2 028 Case intake agent live at L1 E3a v1.md | RWB-E2-028 Case intake agent live at L1 [E3a] |
| RWB E2 029 Deviation screening agent evaluation and L1 on one segment E3b v1.md | RWB-E2-029 Deviation screening agent evaluation and L1 on one segment [E3b] |
| RWB E2 030 Legal document agent in shadow on Epic 1 data E3c v1.md | RWB-E2-030 Legal document agent in shadow on Epic 1 data [E3c] |
| RWB TE 009 Performance test harness v1.md | RWB-TE-009 Performance test harness |
| RWB TE 010 Browser and accessibility tests v1.md | RWB-TE-010 Browser and accessibility tests |
