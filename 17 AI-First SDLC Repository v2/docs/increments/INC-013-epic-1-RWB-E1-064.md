# Increment Card — INC-013-epic-1-RWB-E1-064

**RWB-E1-064 — Data dictionary for the 14 data products**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-013` |
| Title | Data dictionary for the 14 data products |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-064` |
| RUN_ID | `INC-013-epic-1-RWB-E1-064` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | Enabler |
| Priority | Must |
| Build order | 13 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-001, RWB-E1-043, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Ready for specify |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** Enabler. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **all 122 objects and 1,366 fields of the 14 data products typed, sourced and owned, including the 30 ACE views and the four extension tables, with a data contract for the ACE read path that the ACE team confirms**, so that **every read has one published definition and a change to an ACE column reaches the dictionary through one governed load**.

**Business outcome:** The dictionary is the only place that says what a field is, where it comes from and who owns it. It now covers 122 objects and 1,366 fields: the 92 Workbench tables hold 1,062 fields, 49 of them on the four extension tables, and the 30 `recovery.v_ace_*` views hold 304 fields, 177 in Section A and 127 in Section B. The Workbench loads no source data (D-RCV-35 U1), so every source is either ACE, whose columns are recorded as `public.table.column` on the view fields where the view reads one column, or the Workbench itself.

**Main flow:**
1. Data steward: prepares the governance load for all 1,366 fields with owner role, refresh cycle, late behavior and interface, and checks the source system and source field of each view field against the view definition.
2. Reference data administrator: loads the file through POST /admin/reference-loads with table `sys_fields` and valid from 2026-11-30.
3. DataDictionaryLoader: refuses the whole load if any field is unknown, if a view field's source system is not "ACE", if a Workbench field's source system is not "Workbench", if a view field's source field is not a column of that view and is not one of the 7 derived fields, or if any of the required attributes is empty; otherwise writes the attributes and version 1 of each field to `sys_field_version`.
4. Data steward: records the ACE team lead's confirmation of contract DC-ACE, which lists the 304 ACE fields and the read interfaces V0002 and V0003, with the confirming role, the date and the stored document reference.
5. Data steward: publishes DC-ACE with POST /admin/data-contracts/{contractId}/publish; the service refuses a contract without a confirmation.
6. DataContractService: sets the contract PUBLISHED. The published version stays in force until a later version is confirmed and published.

**Acceptance criteria:**
- AC1: Every field is defined
- AC2: Every ACE view has dictionary rows
- AC3: The arrears field comes from the ACE delay days
- AC4: A new ACE column is a dictionary change through RWB-E1-043
- AC5: A change keeps its history
- AC6: The ACE read path is agreed before it is published
- AC7: Two changes to the same field at once
- AC8: A change to a field in a published contract

**Out of scope:**
- The tables, the seed and the dictionary view: RWB-E1-001.
- The 30 ACE views, their grants and the view conformance test: RWB-E1-069.
- The catalog endpoint, access by product and PDPA masking: RWB-E1-016.
- Freshness stamps per data product: RWB-E1-015.
- Retention per product and table: RWB-E1-017.
- The reference data screen SCR-40: Epic 8.
- Contracts for stage 2 data products: RWB-E2-010.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-064-data-dictionary-for-the-14-data-products-v1.md` |
| Requirement IDs | REQ-RDF-001, REQ-RDF-011 |
| BRD section | Business Requirements Epic 1, section 3.1 (story), section 4 (REQ-RDF-001, REQ-RDF-011) and section 5 (data dictionary sources and owners) |
| Decision | D-RCV-35 (U1, U4); ADR-010; DL43 |
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
| RW-DATASTEW, data steward and data product owner | Changes field definitions, records the confirmation, publishes the contract (Reference data U) |
| RW-REFADM, reference data administrator | Submits the dictionary load (Reference data C) |
| RW-COE, center of excellence analyst | Reads and changes field definitions (Reference data CRUD) |
| ACE team lead | Confirms the ACE read contract; owns the ACE columns it names (RWB-ACE-001) |
| RW-TRIBE, RW-AUDIT and other roles with Reference data R | Read the dictionary and the contracts |
| SY-DATALOAD, data load | Applies an approved dictionary load |

## Contract extract

**Endpoints** | Method and path | Request | Response | Errors | Authorization | Idempotency | |---|---|---|---|---|---| | GET /admin/data-dictionary/fields | Query: product, entity, field, sourceSystem, page, size | DataDictionaryFieldPage: items of DataDictionaryField (fieldId, entity, fieldName, dataType, physicalType, mandatory, listCode, sourceSystem, sourceField, refreshCycle, ownerRole, lateBehavior, interfaceId, isPersonal, version, versionDate) and the object and field counts | 401 (MSG-P4-001); 403 (MSG-P4-002); 503 (MSG-GEN-006) | Reference data, R | Not applicable | | PATCH /admin/data-dictionary/fields/{fieldCode} | Header If-Match: version; body DataDictionaryFieldChange (changed attributes, reason) | DataDictionaryField | 403; 404 unknown field (MSG-P4-003); 409 stale version (MSG-GEN-004); 422 reason empty (MSG-GEN-001); 428 no If-Match (MSG-GEN-004) | Reference data, U |…

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

- No business value in code: owners, cycles, late behavior and contract content are data rows. - No personal data in logs, tests or prompts: the dictionary holds definitions, not values; the confirmation names a role, not a person. - No read of another module's tables: other modules use DataDictionaryQuery. The only public schema names in the story are the ACE column names recorded in the dictionary, which no recovery class reads directly. - A published contract is never edited in place; a change makes a new version. - No DDL: V0001 owns the five tables; this story never adds or alters a column.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-064-data-dictionary-for-the-14-data-products-v1.md` |
| Specification | `output/INC-013-epic-1-RWB-E1-064/specify/spec.md` |
| Compliance validation | `output/INC-013-epic-1-RWB-E1-064/specify/compliance-validation.md` |
| Agent run log | `output/INC-013-epic-1-RWB-E1-064/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-013-epic-1-RWB-E1-064/plan/` |
| Implementation evidence | `output/INC-013-epic-1-RWB-E1-064/implement/` |
| API / functional test reports | `output/INC-013-epic-1-RWB-E1-064/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-013-epic-1-RWB-E1-064/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Ready for specify |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 8 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-064-data-dictionary-for-the-14-data-products-v1.md` |
| Output run | `output/INC-013-epic-1-RWB-E1-064/` |

