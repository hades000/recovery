<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!Read me first v2.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v7.zip!Read me first v2.md`  
> **Converted from:** Markdown (extracted)

# Read me first

SCB Collections and Recovery. Henka Group, 16 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

This folder holds 72 story files for Epic 1, one per story, plus this read-me. Hand a coding agent one story file together with:

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
| RWB E1 001 Recovery tables for the 14 data products v1.md | RWB-E1-001 Recovery tables for the 14 data products |
| RWB E1 002 Case list v1 with case ID owner and queue v1.md | RWB-E1-002 Case list v1 with case ID, owner and queue |
| RWB E1 007 Integration adapters for file loads and outbound files v1.md | RWB-E1-007 Integration adapters for outbound files |
| RWB E1 008 Decision log store v1 append only and hash chained v1.md | RWB-E1-008 Decision log store v1, append only and hash chained |
| RWB E1 011 Reconciliation and data quality report v1.md | RWB-E1-011 Reconciliation and data quality report |
| RWB E1 013 Baseline measures v1.md | RWB-E1-013 Baseline measures |
| RWB E1 014 Decision log copy to the data lake v1.md | RWB-E1-014 Decision log copy to the data lake |
| RWB E1 015 Freshness stamp per data product v1.md | RWB-E1-015 Freshness stamp per data product |
| RWB E1 016 Access control per data product and catalog entries v1.md | RWB-E1-016 Access control per data product and catalog entries |
| RWB E1 017 Retention and archive rule for the data store v1.md | RWB-E1-017 Retention and archive rule for the data store |
| RWB E1 018 Case ID issuance and case record v1 v2.md | RWB-E1-018 Case ID issuance and case record v1 |
| RWB E1 019 Roles teams and queues as data v1.md | RWB-E1-019 Roles, teams and queues as data |
| RWB E1 020 Allocation and assignment engine v1 v2.md | RWB-E1-020 Allocation and assignment engine v1 |
| RWB E1 021 Transfer rules and engine v1 v2.md | RWB-E1-021 Transfer rules and engine v1 |
| RWB E1 022 Sign on with SSO MFA and the first roles v1.md | RWB-E1-022 Sign-on with SSO, MFA and the first roles |
| RWB E1 023 Case record view v1 read only v1.md | RWB-E1-023 Case record view v1, read only |
| RWB E1 024 Document store and index v1.md | RWB-E1-024 Document store and index |
| RWB E1 025 Document types and fields agreed v1.md | RWB-E1-025 Document types and fields agreed |
| RWB E1 026 Attach and search screen v1.md | RWB-E1-026 Attach and search screen |
| RWB E1 027 Decision log writer v1 v1.md | RWB-E1-027 Decision log writer v1 |
| RWB E1 028 Service levels timers escalation and prescription dates v2.md | RWB-E1-028 Service levels, timers, escalation and prescription dates |
| RWB E1 030 Daily rebalancing and queue measures v1.md | RWB-E1-030 Daily rebalancing and queue measures |
| RWB E1 031 Queue and owner on the case list with filters v1.md | RWB-E1-031 Queue and owner on the case list with filters |
| RWB E1 032 Automatic attach from the OCR intake v1.md | RWB-E1-032 Automatic attach from the OCR intake |
| RWB E1 033 Search across cases v1.md | RWB-E1-033 Search across cases |
| RWB E1 034 Letter template management v1.md | RWB-E1-034 Letter template management |
| RWB E1 035 Case record view v1 1 with documents and history timeline v1.md | RWB-E1-035 Case record view v1.1 with documents and history timeline |
| RWB E1 037 Role to permission matrix as data and PDPA field masking by role v1.md | RWB-E1-037 Role to permission matrix as data and PDPA field masking by role |
| RWB E1 038 Delegation of authority table as reference data v1.md | RWB-E1-038 Delegation of authority table as reference data |
| RWB E1 039 Access log into the decision log and break glass admin v1.md | RWB-E1-039 Access log into the decision log and break-glass admin |
| RWB E1 040 Document checklist per case type as reference data v1.md | RWB-E1-040 Document checklist per case type as reference data |
| RWB E1 041 Retention classes and virus scan on intake v1.md | RWB-E1-041 Retention classes and virus scan on intake |
| RWB E1 042 Central configuration service and parameter catalog v1.md | RWB-E1-042 Central configuration service and parameter catalog |
| RWB E1 043 Reference data service with versioned tables v2.md | RWB-E1-043 Reference data service with versioned tables |
| RWB E1 044 Database migrations versioned with parameterized schema names v1.md | RWB-E1-044 Database migrations versioned with parameterized schema names |
| RWB E1 045 Multi product parameters for Mortgage HP and SSME v1.md | RWB-E1-045 Multi-product parameters for Mortgage, HP and SSME |
| RWB E1 046 Template and merge field catalog as data v1.md | RWB-E1-046 Template and merge field catalog as data |
| RWB E1 047 Feature flags for module release with a removal date v1.md | RWB-E1-047 Feature flags for module release with a removal date |
| RWB E1 049 OCR pipeline on the Workbench document hub v1.md | RWB-E1-049 OCR pipeline on the Workbench document hub |
| RWB E1 050 Document classification v1.md | RWB-E1-050 Document classification |
| RWB E1 052 Notice generation v1 v1.md | RWB-E1-052 Notice generation v1 |
| RWB E1 053 Field extraction for the six types into the index v1.md | RWB-E1-053 Field extraction for the six types into the index |
| RWB E1 054 Review queue for low confidence documents v1.md | RWB-E1-054 Review queue for low-confidence documents |
| RWB E1 055 Proof of delivery capture design with WIN v1.md | RWB-E1-055 Proof of delivery capture design with WIN |
| RWB E1 056 Run books and monitoring for every Epic 1 job v1.md | RWB-E1-056 Run books and monitoring for every Epic 1 Workbench job |
| RWB E1 057 Intake from branches mailroom partner SFTP and email v1.md | RWB-E1-057 Intake from branches, mailroom, partner SFTP and email |
| RWB E1 058 Agent platform set up E1a v1.md | RWB-E1-058 Agent platform set-up [E1a] |
| RWB E1 059 Case intake agent in shadow E1b v1.md | RWB-E1-059 Case intake agent in shadow [E1b] |
| RWB E1 060 Extraction evaluation E1c v1.md | RWB-E1-060 Extraction evaluation [E1c] |
| RWB E1 061 Intake agent evaluation and L1 proposal E2a v1.md | RWB-E1-061 Intake agent evaluation and L1 proposal [E2a] |
| RWB E1 062 Deviation screening agent in shadow E2b v1.md | RWB-E1-062 Deviation screening agent in shadow [E2b] |
| RWB E1 063 Agent monitoring dashboard v1 E2c v1.md | RWB-E1-063 Agent monitoring dashboard v1 [E2c] |
| RWB E1 064 Data dictionary for the 14 data products v1.md | RWB-E1-064 Data dictionary for the 14 data products |
| RWB E1 065 Sandbox database with synthetic recovery data v1.md | RWB-E1-065 Sandbox database with synthetic recovery data |
| RWB E1 066 Interaction ledger store and writer v1.md | RWB-E1-066 Interaction ledger store and writer |
| RWB E1 067 Every Workbench action into the interaction ledger v1.md | RWB-E1-067 Every Workbench action into the interaction ledger |
| RWB E1 068 Interaction ledger read interface v1.md | RWB-E1-068 Interaction ledger read interface |
| RWB E1 069 Read only ACE source views, grants and boundary rule v1.md | RWB-E1-069 Read-only ACE source views, grants and boundary rule |
| RWB E1 070 Temporal platform on the ACE AKS clusters v1.md | RWB-E1-070 Temporal platform on the ACE AKS clusters |
| RWB E1 071 Temporal worker and SDK in the recovery module v1.md | RWB-E1-071 Temporal worker and SDK in the recovery module |
| RWB E1 072 Drools runtime and rule package store v1.md | RWB-E1-072 Drools runtime and rule package store |
| RWB E1 073 Rule authoring validation test scenarios approval and rollback in Drools v1.md | RWB-E1-073 Rule authoring, validation, test scenarios, approval and rollback in Drools |
| RWB TE 001 Recovery module folder and boundary test v1.md | RWB-TE-001 Recovery module folder and boundary test |
| RWB TE 002 Code owners for the recovery module v1.md | RWB-TE-002 Code owners for the recovery module |
| RWB TE 003 Types and contract tests from the API specification v1.md | RWB-TE-003 Types and contract tests from the API specification |
| RWB TE 004 Masked data in SIT and UAT v1.md | RWB-TE-004 Masked data in SIT and UAT |
| RWB TE 006 Outbox and retry for outbound work v1.md | RWB-TE-006 Outbox and retry for outbound work |
| RWB TE 007 Scheduled jobs on Quartz v2.md | RWB-TE-007 Scheduled jobs on Quartz |
| RWB TE 008 Decision log hash chain check v1.md | RWB-TE-008 Decision log hash chain check |
| RWB TE 011 PDPA lint for code tests and logs v1.md | RWB-TE-011 PDPA lint for code, tests and logs |
| RWB TE 012 Document storage containers v1.md | RWB-TE-012 Document storage containers |
| RWB TE 013 Agent runtime client with fallback v1.md | RWB-TE-013 Agent runtime client with fallback |
