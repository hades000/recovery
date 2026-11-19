# Increment Card — INC-009-epic-1-RWB-E1-001

**RWB-E1-001 — Recovery tables for the 14 data products**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-009` |
| Title | Recovery tables for the 14 data products |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-001` |
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 9 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-044, RWB-E1-043 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **the 92 recovery tables for the 14 data products created in the ACE database, with a data dictionary that covers those tables and the 30 read-only ACE views, and one system of record and one owner per data product**, so that **every Workbench record has one home and every data product has one accountable owner and one read path**.

**Business outcome:** The Workbench holds no copy of source data. ACE ingests ALS, SCBPDM, EFS, COLLINS, CCMS, SVAF, AMIS, RPS, LIT, WIN, GL, NLEADS, EasyApp and Entra ID, and the Workbench reads what it needs through the 30 `recovery.v_ace_*` views (D-RCV-35 U1 and U4, ADR-010). This story creates the 88 Workbench tables, the four extension tables that hold a Workbench decision about an ACE record, the metadata registry that holds the data dictionary as data, and the catalog of the 14 data products DP01 to DP14. Each data product then has exactly one system of record, written "ACE (ingested from X)" for source data, "Recovery Workbench" for Workbench records, or one sentence naming both where the product holds both, and one named owner, as REQ-RDF-001 requires. The measure it serves is "the ACE batch is complete when the Workbench reads it on 99 percent of days", because the dictionary and the catalog are what every later read and every freshness stamp are resolved against.

**Main flow:**
1. Pipeline: runs migration `V0001__rwb_e1_001_recovery_schema.sql` in DEV with `recoverySchema = recovery`.
2. Migration: creates the 92 tables (the 88 Workbench tables and the four extension tables), their indexes, the append-only triggers on `decision_log_entry` and `interaction`, and the catalog table `data_product`, in one transaction.
3. Migration: inserts the 14 `data_product` rows, then the 122 `sys_objects` rows and the 1,366 `sys_fields` rows (section 13), and creates the view `v_data_dictionary`.
4. Migration: adds `fk_sys_objects_data_product`; `sys_objects.data_product` is nullable, so the 24 operational objects of OPS, AGT and RPT carry no product.
5. Pipeline: runs the dictionary conformance test, which compares every column of the 92 tables in the recovery schema with `sys_fields` (1,062 fields).
6. Pipeline: repeats steps 1 to 5 in SIT.

**Acceptance criteria:**
- AC1: Schema deployed
- AC2: Dictionary published
- AC3: One system of record
- AC4: Failed migration leaves no partial schema
- AC5: Column without a dictionary entry fails the build
- AC6: Repeated migration has no effect
- AC7: Catalog row with two systems of record is refused
- AC8: Catalog with a missing product is refused
- AC9: Value outside its list
- AC10: Same catalog file loaded again
- AC11: Source named on its own is refused

**Out of scope:**
- The 30 read-only ACE views, their grants and the view conformance test (RWB-E1-069).
- Freshness stamp per data product from the ACE batch record (RWB-E1-015).
- Access control per data product, PDPA masking and the catalog entry screen (RWB-E1-016).
- Retention and archive rules (RWB-E1-017).
- Stage 2 data products for contracts, plans and treatments (REQ-RDF-014, Epic 2).
- The dictionary endpoint, field versions and data contracts with each system owner (RWB-E1-064).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| Requirement IDs | REQ-RDF-001 |
| BRD section | Business Requirements Epic 1, section 3.1; Business Requirements Program, section 5.1 |
| Decision | D-RCV-35 (U1 to U5); ADR-010; DL43 open |
| Epic card | `epics/EPIC-001-foundation-1.md` |
| Lifecycle tailoring | `epics/EPIC-001-tailoring.md` |
| Module FSD / PRD | `docs/prds/` |
| Module TSD | `requirement/legacy/05-technical-architecture/` |
| API specification | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v4.yaml` |
| Physical schema | `requirement/legacy/06-data/recovery-workbench-physical-schema-v6.sql` |
| Engineering practices | `AGENTS.md` |

## Lifecycle tailoring

Shared record: `epics/EPIC-001-tailoring.md`. The phase classification is epic-level; this card records the story-specific agents and evidence.

## Story authority

| Who | What they may do in this story |
|---|---|
| Pipeline service identity (ACE pipeline) | Runs the migration and the conformance test in DEV and SIT |
| RW-REFADM, reference data administrator | Loads the catalog file (Reference data C) |
| RW-DATASTEW, data steward and data product owner | Confirms the catalog version as its owner (Reference data U); cannot load it (no Reference data C) |
| Developers and the data steward in DEV and SIT | Query v_data_dictionary with read access to the recovery schema |
| Any role without Reference data C | Refused with MSG-P4-002 on the catalog load |

No approval level from the delegation of authority applies.

## Contract extract

**Dictionary view** `v_data_dictionary` (read model created by the migration; RWB-E1-064 builds the dictionary endpoint on it) | Column | From | |---|---| | entity, data_product, entity_system_of_record | sys_objects | | field, field_id, data_type, physical_type, is_mandatory, lov_code, references_object, source_system, source_field, is_personal, late_behavior, interface_id, description | sys_fields | | product_system_of_record, refresh_cycle, owner_role, owner_user_id | data_product | The view joins sys_fields to sys_objects on object_name and left joins data_product on product_code where the product is active, and returns active rows only. It reads no ACE table. **Reference load handler** (published interface of P4 that P1 implements, from RWB-E1-043) ```java public interface ReferenceTableHandler { String tableCode(); // returns "data_product" ValidationReport validate(ReferenceLoadF…

## Owners and approvals

| Gate | Accountable role | Name | Decision / date |
|---|---|---|---|
| Requirements approval | Product Owner | Chitchaya Muanchonchana | Source story set v7/v6, 16 Nov 2026 |
| Context readiness | Forward Deployed Engineer | Jesniphat Pukkham | CONTEXT-20261116 |
| Plan approval | Forward Deployed Architect | Jesniphat Pukkham | Per-story plan gate |
| Pull request approval | Forward Deployed Engineer | Recovery tech lead | Per MR |

## Agents selected

| Lifecycle group | Agent | Applicable / Optional / Not used | Reason |
|---|---|---|---|
| Requirements and discovery | Context Builder / Updater | Applicable | Context package CONTEXT-20261116. |
| Design, backlog and spec | Technical Specifier | Applicable | Produces the implementation-ready spec. |
| Plan and build | Implementation Planner | Applicable | Produces `plan.md` and `tasks.md`. |
| Plan and build | Implementation Builder | Applicable | Builds the approved plan in ACE. |
| Quality and release | Compliance Reviewer | Applicable | Spec, plan and code gates. |
| Quality and release | API Tester | Per API scope | Driven by the spec. |
| Quality and release | Functional Automation Test | Per UI scope | Driven by the spec. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Stop signals:** any guardrail in story §17; a migration that is not `V<seq>__<story>_<name>.sql`; a direct read of an ACE table outside `recovery.v_ace_*`.

**Guardrails:**

- No business value in code: product names, definitions, systems of record, owners and refresh cycles come from the catalog load. - No personal data in logs, tests or prompts. Owner user IDs in DEV and SIT are synthetic test users. - ACE data only through `recovery.v_ace_*` views. This story creates no view over a public table and reads no public table. - The migration changes no data outside the recovery schema, creates no constraint into schema public and never drops a table in PROD. - The dictionary reads only sys_objects, sys_fields and data_product in the recovery schema.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| Specification | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` |
| Compliance validation | `output/INC-009-epic-1-RWB-E1-001/specify/compliance-validation.md` |
| Agent run log | `output/INC-009-epic-1-RWB-E1-001/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-009-epic-1-RWB-E1-001/plan/` |
| Implementation evidence | `output/INC-009-epic-1-RWB-E1-001/implement/` |
| API / functional test reports | `output/INC-009-epic-1-RWB-E1-001/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-009-epic-1-RWB-E1-001/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` |
| Output run | `output/INC-009-epic-1-RWB-E1-001/` |

