# Increment Card — INC-010-epic-1-RWB-E1-001

**RWB-E1-001 — Recovery tables for the 14 data products**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-010` |
| Title | Recovery tables for the 14 data products |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-001` |
| RUN_ID | `INC-010-epic-1-RWB-E1-001` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 1 |
| Critical path | Yes |
| Depends on | RWB-E1-044, RWB-E1-043 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1a.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **the recovery tables for the 14 data products created in the ACE database, with a data dictionary and one system of record and one owner per data product**, so that **every later load has one target table and one accountable owner**.

**Main flow:**
1. Pipeline: runs migration `V0001__rwb_e1_001_recovery_schema.sql` in DEV with `recoverySchema = recovery`.
2. Migration: creates the 43 tables, the 68 foreign keys, the 76 indexes and the append-only triggers on decision_log_entry and interaction, and the new table data_product, in one transaction.
3. Migration: inserts the 108 sys_objects rows, the 1,256 sys_fields rows and the 14 data_product seed rows (section 13), and creates the view `v_data_dictionary`.
4. Pipeline: runs the dictionary conformance test, which compares every column in the recovery schema with sys_fields.
5. Pipeline: repeats steps 1 to 4 in SIT.
6. Reference data administrator: loads the data product catalog file with table code `data_product` through `POST /admin/reference-loads`, naming the owner user ID of each product for the environment.

**Out of scope:**
- Freshness stamp per data product (RWB-E1-015).
- Access control per data product, PDPA masking and the catalog entry screen (RWB-E1-016).
- Retention and archive rules (RWB-E1-017).
- Stage 2 data products for contracts, plans and treatments (REQ-RDF-014, Epic 2).
- The dictionary endpoint, field versions and data contracts with each system owner (RWB-E1-064).

**Business outcome and value hypothesis:** Recovery data is held today in the core bank, EFS, LIT, CCMS, SVAF, AMIS and team spreadsheets, with no single checked copy. This story creates the 43 recovery tables from the physical schema, the metadata registry that holds the data dictionary as data, and the catalog of the 14 data products DP01 to DP14. Each data product then has exactly one system of record and one named owner, as REQ-RDF-001 requires. The measure it serves is "loads on time and complete on 99 percent of days" (FSD P1 A2.1), because no load can start until its target table and owner exist.

**Constraints and guardrails:**
- No business value in code: product names, systems of record, owners and refresh cycles come from the catalog load.
- No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users.
- No read of another module's tables. The dictionary reads only sys_objects, sys_fields and data_product.
- The migration changes no data outside the recovery schema and never drops a table in PROD.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 001 Recovery tables for the 14 data products v1.md` |
| Requirement IDs | REQ-RDF-001 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| Logical data model and data dictionary | `requirement/legacy/06-data/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Business rules and routing logic | `requirement/legacy/02-business-architecture-and-process/` |
| Error and message standard | `requirement/legacy/07-screens-and-experience/` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Role | Rights in this story |
|---|---|
| Pipeline service identity (ACE pipeline) | Runs the migration and the conformance test in DEV and SIT |
| RW-REFADM, reference data administrator | Loads the catalog file (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Confirms the catalog version as its owner (Reference data U); cannot load it (no Reference data C) |
| Developers and the data steward in DEV and SIT | Query v_data_dictionary with read access to the recovery schema |
| Any role without Reference data C | Refused with MSG-P4-002 on the catalog load |

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Intake approval | Product Owner | TBC | |
| Context readiness | Forward Deployed Engineer | TBC | |
| Requirements approval (BRD / PRD) | Product Owner, FDA | TBC | |
| Design and architecture approval | Forward Deployed Architect | TBC | |
| Backlog and specification approval | Product Owner | TBC | |
| Plan approval | Forward Deployed Architect | TBC | |
| Task approval | Forward Deployed Engineer | TBC | |
| Pull request approval (code review) | Forward Deployed Engineer | TBC | |
| Quality and security gate | FDA, Quality Engineer, Security | TBC | |
| Release readiness | Forward Deployed Engineer | TBC | |
| Deployment approval | Product Owner / PM | TBC | |
| Operate and learn review | Ops / System Manager | TBC | |

`TBC` is not an approval (`GAP-006`). The story is in delivery at the specification stage; the human gates remain open until named.

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder | Not used | The context package exists; reuse `.github/contexts/` and `EPIC-001`. |
| Requirements and discovery | BRD Builder | Not used | The BRD is approved; reuse it. |
| Requirements and discovery | PRD Builder | Not used | The FSD/PRD is approved; reuse it. |
| Design, backlog and spec | Jira Backlog Manager | Optional | The local story file is the backlog; Jira import is TBC. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in the ACE repository. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Not used | API is not in scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.p1.data-catalog`. The flag covers the catalog handler; the migration is not behind a flag.
- **Critical path:** Yes; **depends on:** RWB-E1-044, RWB-E1-043.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: product names, systems of record, owners and refresh cycles come from the catalog load.
  - No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users.
  - No read of another module's tables. The dictionary reads only sys_objects, sys_fields and data_product.
  - The migration changes no data outside the recovery schema and never drops a table in PROD.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 001 Recovery tables for the 14 data products v1.md` |
| Specification | `output/INC-010-epic-1-RWB-E1-001/specify/spec.md` |
| Compliance validation | `output/INC-010-epic-1-RWB-E1-001/specify/compliance-validation.md` |
| Agent run log | `output/INC-010-epic-1-RWB-E1-001/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-010-epic-1-RWB-E1-001/plan/` (TBC) |
| Implementation evidence | `output/INC-010-epic-1-RWB-E1-001/implement/` (TBC) |
| API / functional test reports | `output/INC-010-epic-1-RWB-E1-001/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-010-epic-1-RWB-E1-001/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — regated 2026-11-06: clarifications resolved by the D-RCV rulings; gate-002 compliance PASS |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-010-epic-1-RWB-E1-001/specify/compliance-validation.md`) |
| Acceptance criteria | 6 ACs in the current story (AC2, AC3, AC7, AC8, AC9, AC10); old AC1 removed by the 4 November 2026 cleanup |
| AC numbering | Intentional gaps: AC4, AC5, AC6 (removed by the 4 November 2026 cleanup) |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 001 Recovery tables for the 14 data products v1.md` |
| Output run | `output/INC-010-epic-1-RWB-E1-001/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
