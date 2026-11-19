# Increment index

Two epic-level records live in `epics/`. The 78 story-level records in this folder match the Epic 1 output run IDs one-to-one.

## Epics

| Epic | Card | Tailoring | Release | Status |
|---|---|---|---|---|
| `EPIC-001` Foundation 1 | `epics/EPIC-001-foundation-1.md` | `epics/EPIC-001-tailoring.md` | 30 Nov 2026 | In delivery |
| `EPIC-002` Foundation 2 | `epics/EPIC-002-foundation-2.md` | `epics/EPIC-002-tailoring.md` | 31 Dec 2026 | Mobilised |

## Story increments

| INC | Story | Title | Module | Type | Priority | Spec | ACs | AC notes | Card | Run |
|---|---|---|---|---|---|---|---|---|---|---|
| 001 | `RWB-E1-044` | Database migrations versioned with parameterized schema names | P3 Case and workflow | Enabler | Must | SUCCESS | 0 | - | `INC-001-epic-1-RWB-E1-044.md` | `output/INC-001-epic-1-RWB-E1-044/specify/` |
| 002 | `RWB-TE-001` | Recovery module folder and boundary test | P2 Integration | Enabler | Must | SUCCESS | 0 | - | `INC-002-epic-1-RWB-TE-001.md` | `output/INC-002-epic-1-RWB-TE-001/specify/` |
| 003 | `RWB-E1-042` | Central configuration service and parameter catalog | P3 Case and workflow | Enabler | Must | SUCCESS | 9 | AC2-AC3 removed | `INC-003-epic-1-RWB-E1-042.md` | `output/INC-003-epic-1-RWB-E1-042/specify/` |
| 004 | `RWB-TE-002` | Code owners for the recovery module | P2 Integration | Enabler | Must | SUCCESS | 0 | - | `INC-004-epic-1-RWB-TE-002.md` | `output/INC-004-epic-1-RWB-TE-002/specify/` |
| 005 | `RWB-TE-003` | Types and contract tests from the API specification | P2 Integration | Enabler | Must | SUCCESS | 0 | - | `INC-005-epic-1-RWB-TE-003.md` | `output/INC-005-epic-1-RWB-TE-003/specify/` |
| 006 | `RWB-TE-005` | Rule table test harness | P3 Case and workflow | Enabler | Must | SUCCESS | 7 | - | `INC-006-epic-1-RWB-TE-005.md` | `output/INC-006-epic-1-RWB-TE-005/specify/` |
| 007 | `RWB-TE-011` | PDPA lint for code, tests and logs | P2 Integration | Enabler | Must | SUCCESS | 0 | - | `INC-007-epic-1-RWB-TE-011.md` | `output/INC-007-epic-1-RWB-TE-011/specify/` |
| 008 | `RWB-TE-012` | Document storage containers | P5 Document hub | Enabler | Must | SUCCESS | 12 | - | `INC-008-epic-1-RWB-TE-012.md` | `output/INC-008-epic-1-RWB-TE-012/specify/` |
| 009 | `RWB-E1-043` | Reference data service with versioned tables | P3 Case and workflow | Enabler | Must | SUCCESS | 10 | - | `INC-009-epic-1-RWB-E1-043.md` | `output/INC-009-epic-1-RWB-E1-043/specify/` |
| 010 | `RWB-E1-001` | Recovery tables for the 14 data products | P1 Recovery data engine | User story | Must | SUCCESS | 7 | AC4-AC6 removed | `INC-010-epic-1-RWB-E1-001.md` | `output/INC-010-epic-1-RWB-E1-001/specify/` |
| 011 | `RWB-E1-003` | ALS daily extract load | P1 Recovery data engine | User story | Must | SUCCESS | 14 | - | `INC-011-epic-1-RWB-E1-003.md` | `output/INC-011-epic-1-RWB-E1-003/specify/` |
| 012 | `RWB-E1-005` | Excel and SharePoint inventory | P1 Recovery data engine | User story | Must | SUCCESS | 8 | - | `INC-012-epic-1-RWB-E1-005.md` | `output/INC-012-epic-1-RWB-E1-005/specify/` |
| 013 | `RWB-E1-007` | Integration adapters for file loads and outbound files | P2 Integration | User story | Must | SUCCESS | 8 | AC1 removed | `INC-013-epic-1-RWB-E1-007.md` | `output/INC-013-epic-1-RWB-E1-007/specify/` |
| 014 | `RWB-E1-008` | Decision log store v1, append only and hash chained | P7 Decision center and log | User story | Must | SUCCESS | 8 | - | `INC-014-epic-1-RWB-E1-008.md` | `output/INC-014-epic-1-RWB-E1-008/specify/` |
| 015 | `RWB-E1-064` | Data dictionary for the 14 data products | P1 Recovery data engine | Enabler | Must | SUCCESS | 8 | - | `INC-015-epic-1-RWB-E1-064.md` | `output/INC-015-epic-1-RWB-E1-064/specify/` |
| 016 | `RWB-E1-065` | Sandbox database with synthetic recovery data | P1 Recovery data engine | Enabler | Must | SUCCESS | 0 | - | `INC-016-epic-1-RWB-E1-065.md` | `output/INC-016-epic-1-RWB-E1-065/specify/` |
| 017 | `RWB-E1-051` | Legacy feed jobs on ADF and Control-M | P2 Integration | User story | Must | SUCCESS | 4 | AC2-AC3 removed | `INC-017-epic-1-RWB-E1-051.md` | `output/INC-017-epic-1-RWB-E1-051/specify/` |
| 018 | `RWB-TE-004` | Masked data in SIT and UAT | P1 Recovery data engine | Enabler | Must | SUCCESS | 0 | - | `INC-018-epic-1-RWB-TE-004.md` | `output/INC-018-epic-1-RWB-TE-004/specify/` |
| 019 | `RWB-E1-029` | Rule load, validation and rollback | P3 Case and workflow | User story | Must | SUCCESS | 12 | - | `INC-019-epic-1-RWB-E1-029.md` | `output/INC-019-epic-1-RWB-E1-029/specify/` |
| 020 | `RWB-E1-047` | Feature flags for module release with a removal date | P2 Integration | User story | Should | SUCCESS | 9 | - | `INC-020-epic-1-RWB-E1-047.md` | `output/INC-020-epic-1-RWB-E1-047/specify/` |
| 021 | `RWB-E1-010` | Excel and SharePoint loads | P1 Recovery data engine | User story | Must | SUCCESS | 13 | - | `INC-021-epic-1-RWB-E1-010.md` | `output/INC-021-epic-1-RWB-E1-010/specify/` |
| 022 | `RWB-E1-017` | Retention and archive rule for the data store | P1 Recovery data engine | User story | Should | SUCCESS | 9 | - | `INC-022-epic-1-RWB-E1-017.md` | `output/INC-022-epic-1-RWB-E1-017/specify/` |
| 023 | `RWB-E1-056` | Run books and monitoring for every Epic 1 job | P2 Integration | Enabler | Must | SUCCESS | 5 | AC1, AC4 removed | `INC-023-epic-1-RWB-E1-056.md` | `output/INC-023-epic-1-RWB-E1-056/specify/` |
| 024 | `RWB-E1-014` | Decision log copy to the data lake | P1 Recovery data engine | User story | Should | SUCCESS | 8 | - | `INC-024-epic-1-RWB-E1-014.md` | `output/INC-024-epic-1-RWB-E1-014/specify/` |
| 025 | `RWB-E1-027` | Decision log writer v1 | P7 Decision center and log | User story | Must | SUCCESS | 7 | - | `INC-025-epic-1-RWB-E1-027.md` | `output/INC-025-epic-1-RWB-E1-027/specify/` |
| 026 | `RWB-TE-007` | Scheduled jobs on Quartz | P3 Case and workflow | Enabler | Must | SUCCESS | 9 | - | `INC-026-epic-1-RWB-TE-007.md` | `output/INC-026-epic-1-RWB-TE-007/specify/` |
| 027 | `RWB-E1-038` | Delegation of authority table as reference data | P4 Access and administration | User story | Must | SUCCESS | 9 | - | `INC-027-epic-1-RWB-E1-038.md` | `output/INC-027-epic-1-RWB-E1-038/specify/` |
| 028 | `RWB-TE-006` | Outbox and retry for outbound work | P2 Integration | Enabler | Must | SUCCESS | 11 | - | `INC-028-epic-1-RWB-TE-006.md` | `output/INC-028-epic-1-RWB-TE-006/specify/` |
| 029 | `RWB-TE-008` | Decision log hash chain check | P7 Decision center and log | Enabler | Must | SUCCESS | 8 | - | `INC-029-epic-1-RWB-TE-008.md` | `output/INC-029-epic-1-RWB-TE-008/specify/` |
| 030 | `RWB-E1-019` | Roles, teams and queues as data | P3 Case and workflow | User story | Must | SUCCESS | 12 | - | `INC-030-epic-1-RWB-E1-019.md` | `output/INC-030-epic-1-RWB-E1-019/specify/` |
| 031 | `RWB-E1-022` | Sign-on with SSO, MFA and the first roles | P4 Access and administration | User story | Must | SUCCESS | 9 | - | `INC-031-epic-1-RWB-E1-022.md` | `output/INC-031-epic-1-RWB-E1-022/specify/` |
| 032 | `RWB-E1-012` | Retire local copies | P1 Recovery data engine | User story | Must | SUCCESS | 10 | - | `INC-032-epic-1-RWB-E1-012.md` | `output/INC-032-epic-1-RWB-E1-012/specify/` |
| 033 | `RWB-E1-037` | Role to permission matrix as data and PDPA field masking by role | P4 Access and administration | User story | Must | SUCCESS | 10 | - | `INC-033-epic-1-RWB-E1-037.md` | `output/INC-033-epic-1-RWB-E1-037/specify/` |
| 034 | `RWB-E1-039` | Access log into the decision log and break-glass admin | P4 Access and administration, with P7 Decision center and log | User story | Must | SUCCESS | 10 | - | `INC-034-epic-1-RWB-E1-039.md` | `output/INC-034-epic-1-RWB-E1-039/specify/` |
| 035 | `RWB-E1-016` | Access control per data product and catalog entries | P1 Recovery data engine | User story | Must | SUCCESS | 8 | - | `INC-035-epic-1-RWB-E1-016.md` | `output/INC-035-epic-1-RWB-E1-016/specify/` |
| 036 | `RWB-E1-025` | Document types and fields agreed | P5 Document hub | User story | Must | SUCCESS | 7 | - | `INC-036-epic-1-RWB-E1-025.md` | `output/INC-036-epic-1-RWB-E1-025/specify/` |
| 037 | `RWB-E1-045` | Multi-product parameters for Mortgage, HP and SSME | P3 Case and workflow | Enabler | Must | SUCCESS | 8 | - | `INC-037-epic-1-RWB-E1-045.md` | `output/INC-037-epic-1-RWB-E1-045/specify/` |
| 038 | `RWB-E1-046` | Template and merge field catalog as data | P6 Communications | User story | Must | SUCCESS | 8 | - | `INC-038-epic-1-RWB-E1-046.md` | `output/INC-038-epic-1-RWB-E1-046/specify/` |
| 039 | `RWB-E1-058` | Agent platform set-up [E1a] | P10 Agent runtime | User story | Must | SUCCESS | 15 | - | `INC-039-epic-1-RWB-E1-058.md` | `output/INC-039-epic-1-RWB-E1-058/specify/` |
| 040 | `RWB-E1-018` | Case ID issuance and case record v1 | P3 Case and workflow | User story | Must | SUCCESS | 12 | - | `INC-040-epic-1-RWB-E1-018.md` | `output/INC-040-epic-1-RWB-E1-018/specify/` |
| 041 | `RWB-TE-013` | Agent runtime client with fallback | P10 Agent runtime | Enabler | Must | SUCCESS | 8 | - | `INC-041-epic-1-RWB-TE-013.md` | `output/INC-041-epic-1-RWB-TE-013/specify/` |
| 042 | `RWB-E1-013` | Baseline measures | P9 Reporting | User story | Must | SUCCESS | 8 | - | `INC-042-epic-1-RWB-E1-013.md` | `output/INC-042-epic-1-RWB-E1-013/specify/` |
| 043 | `RWB-E1-020` | Allocation and assignment engine v1 | P3 Case and workflow | User story | Must | SUCCESS | 13 | - | `INC-043-epic-1-RWB-E1-020.md` | `output/INC-043-epic-1-RWB-E1-020/specify/` |
| 044 | `RWB-E1-024` | Document store and index | P5 Document hub | User story | Must | SUCCESS | 12 | - | `INC-044-epic-1-RWB-E1-024.md` | `output/INC-044-epic-1-RWB-E1-024/specify/` |
| 045 | `RWB-E1-062` | Deviation screening agent in shadow [E2b] | P10 Agent runtime | User story | Must | SUCCESS | 9 | - | `INC-045-epic-1-RWB-E1-062.md` | `output/INC-045-epic-1-RWB-E1-062/specify/` |
| 046 | `RWB-E1-066` | Interaction ledger store and writer | P1 Recovery data engine | User story | Must | SUCCESS | 8 | - | `INC-046-epic-1-RWB-E1-066.md` | `output/INC-046-epic-1-RWB-E1-066/specify/` |
| 047 | `RWB-E1-002` | Case list v1 with case ID, owner and queue | P1 Recovery data engine | User story | Must | SUCCESS | 10 | - | `INC-047-epic-1-RWB-E1-002.md` | `output/INC-047-epic-1-RWB-E1-002/specify/` |
| 048 | `RWB-E1-023` | Case record view v1, read only | P3 Case and workflow | User story | Must | SUCCESS | 10 | - | `INC-048-epic-1-RWB-E1-023.md` | `output/INC-048-epic-1-RWB-E1-023/specify/` |
| 049 | `RWB-E1-028` | Service levels, timers, escalation and prescription dates | P3 Case and workflow | User story | Must | SUCCESS | 11 | - | `INC-049-epic-1-RWB-E1-028.md` | `output/INC-049-epic-1-RWB-E1-028/specify/` |
| 050 | `RWB-E1-031` | Queue and owner on the case list with filters | P3 Case and workflow | User story | Must | SUCCESS | 8 | - | `INC-050-epic-1-RWB-E1-031.md` | `output/INC-050-epic-1-RWB-E1-031/specify/` |
| 051 | `RWB-E1-049` | OCR pipeline on the Workbench document hub | P5 Document hub | User story | Must | SUCCESS | 9 | - | `INC-051-epic-1-RWB-E1-049.md` | `output/INC-051-epic-1-RWB-E1-049/specify/` |
| 052 | `RWB-E1-067` | Every Workbench action into the interaction ledger | P1 Recovery data engine | User story | Must | SUCCESS | 8 | - | `INC-052-epic-1-RWB-E1-067.md` | `output/INC-052-epic-1-RWB-E1-067/specify/` |
| 053 | `RWB-E1-068` | Interaction ledger read interface | P1 Recovery data engine | User story | Must | SUCCESS | 8 | - | `INC-053-epic-1-RWB-E1-068.md` | `output/INC-053-epic-1-RWB-E1-068/specify/` |
| 054 | `RWB-E1-006` | Data quality rules v1 | P1 Recovery data engine | User story | Must | SUCCESS | 9 | - | `INC-054-epic-1-RWB-E1-006.md` | `output/INC-054-epic-1-RWB-E1-006/specify/` |
| 055 | `RWB-E1-021` | Transfer rules and engine v1 | P3 Case and workflow | User story | Must | SUCCESS | 14 | - | `INC-055-epic-1-RWB-E1-021.md` | `output/INC-055-epic-1-RWB-E1-021/specify/` |
| 056 | `RWB-E1-030` | Daily rebalancing and queue measures | P3 Case and workflow | User story | Must | SUCCESS | 10 | - | `INC-056-epic-1-RWB-E1-030.md` | `output/INC-056-epic-1-RWB-E1-030/specify/` |
| 057 | `RWB-E1-041` | Retention classes and virus scan on intake | P5 Document hub | User story | Must | SUCCESS | 10 | - | `INC-057-epic-1-RWB-E1-041.md` | `output/INC-057-epic-1-RWB-E1-041/specify/` |
| 058 | `RWB-E1-050` | Document classification | P5 Document hub | User story | Must | SUCCESS | 10 | - | `INC-058-epic-1-RWB-E1-050.md` | `output/INC-058-epic-1-RWB-E1-050/specify/` |
| 059 | `RWB-E1-011` | Reconciliation and data quality report | P1 Recovery data engine | User story | Must | SUCCESS | 6 | - | `INC-059-epic-1-RWB-E1-011.md` | `output/INC-059-epic-1-RWB-E1-011/specify/` |
| 060 | `RWB-E1-015` | Freshness stamp per data product | P1 Recovery data engine | User story | Must | SUCCESS | 8 | - | `INC-060-epic-1-RWB-E1-015.md` | `output/INC-060-epic-1-RWB-E1-015/specify/` |
| 061 | `RWB-E1-026` | Attach and search screen | P5 Document hub | User story | Must | SUCCESS | 11 | - | `INC-061-epic-1-RWB-E1-026.md` | `output/INC-061-epic-1-RWB-E1-026/specify/` |
| 062 | `RWB-E1-035` | Case record view v1.1 with documents and history timeline | P3 Case and workflow | User story | Should | SUCCESS | 7 | - | `INC-062-epic-1-RWB-E1-035.md` | `output/INC-062-epic-1-RWB-E1-035/specify/` |
| 063 | `RWB-E1-053` | Field extraction for the six types into the index | P5 Document hub | User story | Must | SUCCESS | 13 | - | `INC-063-epic-1-RWB-E1-053.md` | `output/INC-063-epic-1-RWB-E1-053/specify/` |
| 064 | `RWB-E1-057` | Intake from branches, mailroom, partner SFTP and email | P5 Document hub | User story | Must | SUCCESS | 16 | - | `INC-064-epic-1-RWB-E1-057.md` | `output/INC-064-epic-1-RWB-E1-057/specify/` |
| 065 | `RWB-E1-059` | Case intake agent in shadow [E1b] | P10 Agent runtime | User story | Must | SUCCESS | 8 | - | `INC-065-epic-1-RWB-E1-059.md` | `output/INC-065-epic-1-RWB-E1-059/specify/` |
| 066 | `RWB-E1-004` | EFS extract load | P1 Recovery data engine | User story | Must | SUCCESS | 10 | - | `INC-066-epic-1-RWB-E1-004.md` | `output/INC-066-epic-1-RWB-E1-004/specify/` |
| 067 | `RWB-E1-009` | CCMS and SVAF loads | P1 Recovery data engine | User story | Must | SUCCESS | 11 | - | `INC-067-epic-1-RWB-E1-009.md` | `output/INC-067-epic-1-RWB-E1-009/specify/` |
| 068 | `RWB-E1-032` | Automatic attach from the OCR intake | P5 Document hub | User story | Must | SUCCESS | 15 | - | `INC-068-epic-1-RWB-E1-032.md` | `output/INC-068-epic-1-RWB-E1-032/specify/` |
| 069 | `RWB-E1-033` | Search across cases | P5 Document hub | User story | Should | SUCCESS | 10 | - | `INC-069-epic-1-RWB-E1-033.md` | `output/INC-069-epic-1-RWB-E1-033/specify/` |
| 070 | `RWB-E1-034` | Letter template management | P6 Communications | User story | Should | SUCCESS | 10 | - | `INC-070-epic-1-RWB-E1-034.md` | `output/INC-070-epic-1-RWB-E1-034/specify/` |
| 071 | `RWB-E1-040` | Document checklist per case type as reference data | P5 Document hub | User story | Should | SUCCESS | 9 | - | `INC-071-epic-1-RWB-E1-040.md` | `output/INC-071-epic-1-RWB-E1-040/specify/` |
| 072 | `RWB-E1-048` | Rule change audit report | P3 Case and workflow | Enabler | Should | SUCCESS | 9 | - | `INC-072-epic-1-RWB-E1-048.md` | `output/INC-072-epic-1-RWB-E1-048/specify/` |
| 073 | `RWB-E1-052` | Notice generation v1 | P6 Communications | User story | Must | SUCCESS | 8 | - | `INC-073-epic-1-RWB-E1-052.md` | `output/INC-073-epic-1-RWB-E1-052/specify/` |
| 074 | `RWB-E1-060` | Extraction evaluation [E1c] | P10 Agent runtime | Spike | Must | SUCCESS | 8 | - | `INC-074-epic-1-RWB-E1-060.md` | `output/INC-074-epic-1-RWB-E1-060/specify/` |
| 075 | `RWB-E1-061` | Intake agent evaluation and L1 proposal [E2a] | P10 Agent runtime | User story | Must | SUCCESS | 7 | - | `INC-075-epic-1-RWB-E1-061.md` | `output/INC-075-epic-1-RWB-E1-061/specify/` |
| 076 | `RWB-E1-054` | Review queue for low-confidence documents | P5 Document hub | User story | Must | SUCCESS | 17 | - | `INC-076-epic-1-RWB-E1-054.md` | `output/INC-076-epic-1-RWB-E1-054/specify/` |
| 077 | `RWB-E1-063` | Agent monitoring dashboard v1 [E2c] | P10 Agent runtime | User story | Should | SUCCESS | 7 | - | `INC-077-epic-1-RWB-E1-063.md` | `output/INC-077-epic-1-RWB-E1-063/specify/` |
| 078 | `RWB-E1-055` | Proof of delivery capture design with WIN | P6 Communications | User story | Should | SUCCESS | 11 | - | `INC-078-epic-1-RWB-E1-055.md` | `output/INC-078-epic-1-RWB-E1-055/specify/` |

## Status notes

- **78** story cards, one per Epic 1 build-sequence story.
- **0** specs are stale against the current story ACs. The 14 affected specs were cleaned on 5 November 2026; no removed acceptance criterion is mapped anywhere in `output/`.
- **0** specs are blocked. The six previously blocked specs (`RWB-E1-001`, `RWB-E1-014`, `RWB-E1-018`, `RWB-E1-013`, `RWB-E1-032`, `RWB-E1-061`) were regated on 6 November 2026 after the D-RCV-28 to D-RCV-33 rulings; their gate-002 compliance validations are `PASS`.
- **7** stories have zero business ACs: `RWB-E1-044`, `RWB-TE-001`, `RWB-TE-002`, `RWB-TE-003`, `RWB-TE-011`, `RWB-E1-065`, `RWB-TE-004`.
- **5** stories have intentional AC-numbering gaps from the 4 November 2026 cleanup: `RWB-E1-042`, `RWB-E1-001`, `RWB-E1-007`, `RWB-E1-051`, `RWB-E1-056`. `RWB-E1-021` AC4 is a Scenario Outline and is present.
- Named approvers remain `TBC` (`GAP-006`); acting approvers are recorded per specification gate on 6 November 2026 and must be replaced by names before the increment approval signs. The mandatory-control checklist in `epics/EPIC-001-tailoring.md` is still unchecked.
