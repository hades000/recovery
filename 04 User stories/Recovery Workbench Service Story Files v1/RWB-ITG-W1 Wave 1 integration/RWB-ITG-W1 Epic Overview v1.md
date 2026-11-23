# RWB-ITG-W1 Wave 1 integration - Epic Overview v1

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Wave 1. Stories: 52. Ownership is suggested only; any team may pick up any story.

## Suggested owners

| Team type | Stories |
|---|---|
| QA team (suggested; any team may pick up this story) | 2 |
| TechX (suggested; any team may pick up this story) | 50 |

## Day-1 stories

- RWB-ITG-E1001-ITG Recovery tables for the 14 data products
- RWB-ITG-E1002-ITG Case list v1 with case ID, owner and queue
- RWB-ITG-E1007-ITG Integration adapters for outbound files
- RWB-ITG-E1008-ITG Decision log store v1, append only and hash chained
- RWB-ITG-E1011-ITG Reconciliation and data quality report
- RWB-ITG-E1013-ITG Baseline measures
- RWB-ITG-E1015-ITG Freshness stamp per data product
- RWB-ITG-E1016-ITG Access control per data product and catalog entries
- RWB-ITG-E1017-ITG Retention and archive rule for the data store
- RWB-ITG-E1018-ITG Case ID issuance and case record v1
- RWB-ITG-E1019-ITG Roles, teams and queues as data
- RWB-ITG-E1020-ITG Allocation and assignment engine v1
- RWB-ITG-E1021-ITG Transfer rules and engine v1
- RWB-ITG-E1022-ITG Sign-on with SSO, MFA and the first roles
- RWB-ITG-E1023-ITG Case record view v1, read only
- RWB-ITG-E1024-ITG Document store and index
- RWB-ITG-E1025-ITG Document types and fields agreed
- RWB-ITG-E1026-ITG Attach and search screen
- RWB-ITG-E1027-ITG Decision log writer v1
- RWB-ITG-E1028-ITG Service levels, timers, escalation and prescription dates
- RWB-ITG-E1030-ITG Daily rebalancing and queue measures
- RWB-ITG-E1031-ITG Queue and owner on the case list with filters
- RWB-ITG-E1032-ITG Automatic attach from the OCR intake
- RWB-ITG-E1034-ITG Letter template management
- RWB-ITG-E1037-ITG Role to permission matrix as data and PDPA field masking by role
- RWB-ITG-E1039-ITG Access log into the decision log and break-glass admin
- RWB-ITG-E1046-ITG Template and merge field catalog as data
- RWB-ITG-E1047-ITG Feature flags for module release with a removal date
- RWB-ITG-E1049-ITG OCR pipeline on the Workbench document hub
- RWB-ITG-E1050-ITG Document classification
- RWB-ITG-E1052-ITG Notice generation v1
- RWB-ITG-E1054-ITG Review queue for low-confidence documents
- RWB-ITG-E1055-ITG Proof of delivery capture design with WIN
- RWB-ITG-E1057-ITG Intake from branches, mailroom, partner SFTP and email
- RWB-ITG-E1058-ITG Agent platform set-up [E1a]
- RWB-ITG-E1059-ITG Case intake agent in shadow [E1b]
- RWB-ITG-E1060-ITG Extraction evaluation [E1c]
- RWB-ITG-E1062-ITG Deviation screening agent in shadow [E2b]
- RWB-ITG-E1063-ITG Agent monitoring dashboard v1 [E2c]
- RWB-ITG-E1064-ITG Data dictionary for the 14 data products
- RWB-ITG-E1065-ITG Sandbox database with synthetic recovery data
- RWB-ITG-E1066-ITG Interaction ledger store and writer
- RWB-ITG-E1067-ITG Every Workbench action into the interaction ledger
- RWB-ITG-E1069-ITG Read-only ACE source views, grants and boundary rule
- RWB-ITG-E1070-ITG Temporal platform on the ACE AKS clusters
- RWB-ITG-E1073-ITG Rule authoring, validation, test scenarios, approval and rollback in Drools
- RWB-ITG-TE004-ITG Masked data in SIT and UAT
- RWB-ITG-TE006-ITG Outbox and retry for outbound work
- RWB-ITG-TE008-ITG Decision log hash chain check
- RWB-ITG-TE013-ITG Agent runtime client with fallback
- RWB-ITG-W1J01-ITG Contract-test harness and synthetic test data
- RWB-ITG-W1J02-ITG Wave 1 v5 journey end to end

## Lanes

| Lane | Stories | Ready to start |
|---|---|---|
| L-ITG-W1 | RWB-ITG-E1001-ITG, RWB-ITG-E1002-ITG, RWB-ITG-E1007-ITG, RWB-ITG-E1008-ITG, RWB-ITG-E1011-ITG, RWB-ITG-E1013-ITG, RWB-ITG-E1015-ITG, RWB-ITG-E1016-ITG, RWB-ITG-E1017-ITG, RWB-ITG-E1018-ITG, RWB-ITG-E1019-ITG, RWB-ITG-E1020-ITG, RWB-ITG-E1021-ITG, RWB-ITG-E1022-ITG, RWB-ITG-E1023-ITG, RWB-ITG-E1024-ITG, RWB-ITG-E1025-ITG, RWB-ITG-E1026-ITG, RWB-ITG-E1027-ITG, RWB-ITG-E1028-ITG, RWB-ITG-E1030-ITG, RWB-ITG-E1031-ITG, RWB-ITG-E1032-ITG, RWB-ITG-E1034-ITG, RWB-ITG-E1037-ITG, RWB-ITG-E1039-ITG, RWB-ITG-E1046-ITG, RWB-ITG-E1047-ITG, RWB-ITG-E1049-ITG, RWB-ITG-E1050-ITG, RWB-ITG-E1052-ITG, RWB-ITG-E1054-ITG, RWB-ITG-E1055-ITG, RWB-ITG-E1057-ITG, RWB-ITG-E1058-ITG, RWB-ITG-E1059-ITG, RWB-ITG-E1060-ITG, RWB-ITG-E1062-ITG, RWB-ITG-E1063-ITG, RWB-ITG-E1064-ITG, RWB-ITG-E1065-ITG, RWB-ITG-E1066-ITG, RWB-ITG-E1067-ITG, RWB-ITG-E1069-ITG, RWB-ITG-E1070-ITG, RWB-ITG-E1073-ITG, RWB-ITG-TE004-ITG, RWB-ITG-TE006-ITG, RWB-ITG-TE008-ITG, RWB-ITG-TE013-ITG, RWB-ITG-W1J01-ITG, RWB-ITG-W1J02-ITG | Day 1 |
