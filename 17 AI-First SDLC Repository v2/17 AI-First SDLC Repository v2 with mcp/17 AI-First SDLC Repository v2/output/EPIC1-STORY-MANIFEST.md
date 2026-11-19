# Epic 1 story manifest

| INC | Story | Title | Module | Type | Priority | Status |
|---|---|---|---|---|---|---|
| 001 | `RWB-E1-044` | Database migrations versioned with parameterized schema names | P3 Case and workflow | Enabler | Must | Planned — plan carried from the 10 Nov 2026 run; schema basis reverted to `recovery` by D-RCV-35; re-plan before build |
| 002 | `RWB-TE-001` | Recovery module folder and boundary test | P2 Integration | Enabler | Must | Implemented — module boundary built; spec and plan rebaselined 16 Nov 2026 |
| 003 | `RWB-E1-042` | Central configuration service and parameter catalog | P3 Case and workflow | Enabler | Must | Implemented — migration applied and tested; spec and plan rebaselined 16 Nov 2026 |
| 004 | `RWB-TE-002` | Code owners for the recovery module | P2 Integration | Enabler | Must | Ready for specify |
| 005 | `RWB-TE-003` | Types and contract tests from the API specification | P2 Integration | Enabler | Must | Ready for specify |
| 006 | `RWB-TE-011` | PDPA lint for code, tests and logs | P2 Integration | Enabler | Must | Ready for specify |
| 007 | `RWB-TE-012` | Document storage containers | P5 Document hub | Enabler | Must | Ready for specify |
| 008 | `RWB-E1-043` | Reference data service with versioned tables | P3 Case and workflow | Enabler | Must | Planned — plan carried from the 10 Nov 2026 run; re-baseline for D-RCV-35 |
| 009 | `RWB-E1-001` | Recovery tables for the 14 data products | P1 Recovery data engine | User story | Must | Ready for specify |
| 010 | `RWB-E1-069` | Read-only ACE source views, grants and boundary rule | P1 Recovery data engine | User story | Must | Ready for specify |
| 011 | `RWB-E1-007` | Integration adapters for outbound files | P2 Integration | User story | Must | Ready for specify |
| 012 | `RWB-E1-008` | Decision log store v1, append only and hash chained | P7 Decision center and log | User story | Must | Ready for specify |
| 013 | `RWB-E1-064` | Data dictionary for the 14 data products | P1 Recovery data engine | Enabler | Must | Ready for specify |
| 014 | `RWB-E1-065` | Sandbox database with synthetic recovery data | P1 Recovery data engine | Enabler | Must | Ready for specify |
| 015 | `RWB-TE-004` | Masked data in SIT and UAT | P1 Recovery data engine | Enabler | Must | Ready for specify |
| 016 | `RWB-E1-047` | Feature flags for module release with a removal date | P2 Integration | User story | Should | Backlog — not started |
| 017 | `RWB-E1-017` | Retention and archive rule for the data store | P1 Recovery data engine | User story | Should | Backlog — not started |
| 018 | `RWB-E1-056` | Run books and monitoring for every Epic 1 Workbench job | P2 Integration | Enabler | Must | Backlog — not started |
| 019 | `RWB-E1-014` | Decision log copy to the data lake | P1 Recovery data engine | User story | Should | Backlog — not started |
| 020 | `RWB-E1-027` | Decision log writer v1 | P7 Decision center and log | User story | Must | Backlog — not started |
| 021 | `RWB-TE-007` | Scheduled jobs on Quartz | P3 Case and workflow | Enabler | Must | Backlog — not started |
| 022 | `RWB-E1-038` | Delegation of authority table as reference data | P4 Access and administration | User story | Must | Backlog — not started |
| 023 | `RWB-TE-006` | Outbox and retry for outbound work | P2 Integration | Enabler | Must | Backlog — not started |
| 024 | `RWB-TE-008` | Decision log hash chain check | P7 Decision center and log | Enabler | Must | Backlog — not started |
| 025 | `RWB-E1-019` | Roles, teams and queues as data | P3 Case and workflow | User story | Must | Backlog — not started |
| 026 | `RWB-E1-022` | Sign-on with SSO, MFA and the first roles | P4 Access and administration | User story | Must | Backlog — not started |
| 027 | `RWB-E1-037` | Role to permission matrix as data and PDPA field masking by role | P4 Access and administration | User story | Must | Backlog — not started |
| 028 | `RWB-E1-039` | Access log into the decision log and break-glass admin | P4 Access and administration, with P7 Decision center and log | User story | Must | Backlog — not started |
| 029 | `RWB-E1-016` | Access control per data product and catalog entries | P1 Recovery data engine | User story | Must | Backlog — not started |
| 030 | `RWB-E1-025` | Document types and fields agreed | P5 Document hub | User story | Must | Backlog — not started |
| 031 | `RWB-E1-045` | Multi-product parameters for Mortgage, HP and SSME | P3 Case and workflow | Enabler | Must | Backlog — not started |
| 032 | `RWB-E1-046` | Template and merge field catalog as data | P6 Communications | User story | Must | Backlog — not started |
| 033 | `RWB-E1-058` | Agent platform set-up [E1a] | P10 Agent runtime | User story | Must | Backlog — not started |
| 034 | `RWB-E1-070` | Temporal platform on the ACE AKS clusters | P3 Case and workflow | Enabler | Must | Backlog — not started |
| 035 | `RWB-E1-071` | Temporal worker and SDK in the recovery module | P3 Case and workflow | Enabler | Must | Backlog — not started |
| 036 | `RWB-E1-072` | Drools runtime and rule package store | P3 Case and workflow | Enabler | Must | Backlog — not started |
| 037 | `RWB-E1-073` | Rule authoring, validation, test scenarios, approval and rollback in Drools | P3 Case and workflow | User story | Must | Backlog — not started |
| 038 | `RWB-E1-018` | Case ID issuance and case record v1 | P3 Case and workflow | User story | Must | Backlog — not started |
| 039 | `RWB-TE-013` | Agent runtime client with fallback | P10 Agent runtime | Enabler | Must | Backlog — not started |
| 040 | `RWB-E1-013` | Baseline measures | P9 Reporting | User story | Must | Backlog — not started |
| 041 | `RWB-E1-020` | Allocation and assignment engine v1 | P3 Case and workflow | User story | Must | Backlog — not started |
| 042 | `RWB-E1-024` | Document store and index | P5 Document hub | User story | Must | Backlog — not started |
| 043 | `RWB-E1-062` | Deviation screening agent in shadow [E2b] | P10 Agent runtime | User story | Must | Backlog — not started |
| 044 | `RWB-E1-066` | Interaction ledger store and writer | P1 Recovery data engine | User story | Must | Backlog — not started |
| 045 | `RWB-E1-002` | Case list v1 with case ID, owner and queue | P1 Recovery data engine | User story | Must | Backlog — not started |
| 046 | `RWB-E1-023` | Case record view v1, read only | P3 Case and workflow | User story | Must | Backlog — not started |
| 047 | `RWB-E1-028` | Service levels, timers, escalation and prescription dates | P3 Case and workflow | User story | Must | Backlog — not started |
| 048 | `RWB-E1-031` | Queue and owner on the case list with filters | P3 Case and workflow | User story | Must | Backlog — not started |
| 049 | `RWB-E1-049` | OCR pipeline on the Workbench document hub | P5 Document hub | User story | Must | Backlog — not started |
| 050 | `RWB-E1-067` | Every Workbench action into the interaction ledger | P1 Recovery data engine | User story | Must | Backlog — not started |
| 051 | `RWB-E1-068` | Interaction ledger read interface | P1 Recovery data engine | User story | Must | Backlog — not started |
| 052 | `RWB-E1-021` | Transfer rules and engine v1 | P3 Case and workflow | User story | Must | Backlog — not started |
| 053 | `RWB-E1-030` | Daily rebalancing and queue measures | P3 Case and workflow | User story | Must | Backlog — not started |
| 054 | `RWB-E1-041` | Retention classes and virus scan on intake | P5 Document hub | User story | Must | Backlog — not started |
| 055 | `RWB-E1-050` | Document classification | P5 Document hub | User story | Must | Backlog — not started |
| 056 | `RWB-E1-015` | Freshness stamp per data product | P1 Recovery data engine | User story | Must | Backlog — not started |
| 057 | `RWB-E1-011` | Reconciliation and data quality report | P1 Recovery data engine | User story | Must | Backlog — not started |
| 058 | `RWB-E1-026` | Attach and search screen | P5 Document hub | User story | Must | Backlog — not started |
| 059 | `RWB-E1-035` | Case record view v1.1 with documents and history timeline | P3 Case and workflow | User story | Should | Backlog — not started |
| 060 | `RWB-E1-053` | Field extraction for the six types into the index | P5 Document hub | User story | Must | Backlog — not started |
| 061 | `RWB-E1-057` | Intake from branches, mailroom, partner SFTP and email | P5 Document hub | User story | Must | Backlog — not started |
| 062 | `RWB-E1-059` | Case intake agent in shadow [E1b] | P10 Agent runtime | User story | Must | Backlog — not started |
| 063 | `RWB-E1-032` | Automatic attach from the OCR intake | P5 Document hub | User story | Must | Backlog — not started |
| 064 | `RWB-E1-033` | Search across cases | P5 Document hub | User story | Should | Backlog — not started |
| 065 | `RWB-E1-034` | Letter template management | P6 Communications | User story | Should | Backlog — not started |
| 066 | `RWB-E1-040` | Document checklist per case type as reference data | P5 Document hub | User story | Should | Backlog — not started |
| 067 | `RWB-E1-052` | Notice generation v1 | P6 Communications | User story | Must | Backlog — not started |
| 068 | `RWB-E1-060` | Extraction evaluation [E1c] | P10 Agent runtime | Spike | Must | Backlog — not started |
| 069 | `RWB-E1-061` | Intake agent evaluation and L1 proposal [E2a] | P10 Agent runtime | User story | Must | Backlog — not started |
| 070 | `RWB-E1-054` | Review queue for low-confidence documents | P5 Document hub | User story | Must | Backlog — not started |
| 071 | `RWB-E1-063` | Agent monitoring dashboard v1 [E2c] | P10 Agent runtime | User story | Should | Backlog — not started |
| 072 | `RWB-E1-055` | Proof of delivery capture design with WIN | P6 Communications | User story | Should | Backlog — not started |
