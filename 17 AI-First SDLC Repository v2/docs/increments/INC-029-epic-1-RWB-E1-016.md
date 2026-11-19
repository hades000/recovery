# Increment Card — INC-029-epic-1-RWB-E1-016

**RWB-E1-016 — Access control per data product and catalog entries**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-029` |
| Title | Access control per data product and catalog entries |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `EPIC-001` / `RWB-E1-016` |
| RUN_ID | `INC-029-epic-1-RWB-E1-016` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Build order | 29 of 72 (Build Sequence v6, 16 November 2026) |
| Depends on | RWB-E1-037, RWB-E1-001, RWB-E1-064, RWB-E1-069 |
| Blocks | See the build sequence |
| Status | Backlog — not started |

## Project type

**Path:** Greenfield Workbench module on the brownfield ACE service. The 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, source data reached only through the ACE view grant, personal fields masked by role from `v_ace_customer` and `v_ace_contact`, every read logged, and a catalog entry per product that names its owner, system of record, freshness, views and tables and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

**Business outcome:** Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Under D-RCV-35 there is no load and no tokenization: source data is reached only through the `recovery.v_ace_*` views, so access to a data product is the role's access row plus the database grant on the view, and the identity number is masked inside `v_ace_customer` itself. Access rows held as data limit each role to the products its work needs; masking rules decide which role sees a personal field in clear; and every read of personal data goes to the PII access log. The catalog gives one entry per product so a developer, an analyst or an auditor finds the owner, the source, the freshness rule, the retention, the views behind it and the personal fields without asking. Serves REQ-RDF-010 and REQ-RDF-011.

**Main flow:**
1. User: opens a data product view, which calls GET /data-products/{productCode}/records?caseId=.
2. DataProductAccessService: checks the capability right Case record R through the ACE access check.
3. DataProductAccessService: checks data_product_access for a row in force for one of the user's roles and the product.
4. DataProductAccessService: calls the P3 case scope interface for the case's account keys and person keys in the user's scope.
5. DataProductRecordService: reads the product rows. A Workbench table is read in the recovery schema; a source product is read from its `recovery.v_ace_*` view by `account_key`, `person_key`, `asset_key`, `payment_code` or `contact_key`. The read runs as recovery_svc, which has SELECT on the view and nothing on `public`.
6. DataProductRecordService: for each field tagged is_personal in sys_fields, applies `FieldMasker` for the user's roles. The identity number is already masked in the view; the phone, email and address are full in the view because notices and calls need them.

**Acceptance criteria:**
- AC1: Role access
- AC2: Catalog entry
- AC3: Access denied
- AC4: An access load with an unknown role is refused
- AC5: A case outside the user's scope
- AC6: No masking rule loaded keeps every personal field masked
- AC7: The PII access log is unavailable
- AC8: An access row not yet in force
- AC9: The view grant is the source data access
- AC10: Thirty view rows in the catalog
- AC11: A view marked as Workbench is refused

**Out of scope:**
- The role to permission matrix and the masking rule mechanism (RWB-E1-037).
- The access log search and break-glass (RWB-E1-039).
- Masking rule values per role and field (DL26, Compliance).
- The personal data screen SCR-47 (Epic 8).
- Data product definitions and the field dictionary (RWB-E1-064).
- The view definitions, their ownership and the grants (RWB-E1-069).

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-016-access-control-per-data-product-and-catalog-entries-v1.md` |
| Requirement IDs | REQ-RDF-010, REQ-RDF-011 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-010, REQ-RDF-011) |
| Decision | D-RCV-35 (U4); ADR-010 |
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
| RW-DATASTEW, data steward | Prepares the access rows for their products; reads the catalog (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the access load through POST /admin/reference-loads (Reference data C) |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules (DL26); reads the catalog |
| RW-SECADM, security administrator | Owns the role to permission matrix; reads the access log |
| RW-COE, RW-AUDIT, RW-PLATADM | Read the catalog (Platform administration R) |
| Roles with Case record R and an access row, for example RW-CASEOWN, RW-AUDIT | Read a data product for a case in scope |
| recovery_svc, recovery service identity | Applies an approved access version to data_product_access; reads the views with SELECT only |

## Contract extract

**Endpoints** | Item | GET /data-products/{productCode}/records | GET /admin/data-products | |---|---|---| | Request | Path: productCode (DP01 to DP14); query: caseId (required), page, size | Query: product (optional) | | Response | DataProductRecordPage: items (record id, entity, fields map with masked values), freshness (FreshnessStamp from RWB-E1-015), page, size, total | DataProductCatalogEntry[]: productCode, productName, definition, ownerRole, systemOfRecord, refreshCycle, expectedBy, retentionClass, fields (entity, fieldName, fieldId, dataType, isPersonal), reconciliations (rec_code), access (roleCode, canRead, accessVersion, validFrom) | | Errors | 400 missing caseId (MSG-GEN-001); 401 (MSG-P4-001); 403 no capability right or no access row (MSG-P4-002); 404 case not found or out of scope (MSG-P4-003); 503 PII log or store down (MSG-GEN-006) | 401; 403; 503 | | Authorization | Ca…

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

- No business value in code: access by role and masking by role are data rows; the code holds no role or product list. - No personal data in logs, tests or prompts: the PII access log carries field names, not values; test customers are synthetic. - No read of another module's tables: case scope comes from CaseScopeQuery, masking from FieldMasker, roles from the session. - ACE data only through `recovery.v_ace_*` views; a direct `public.*` read is a defect and fails at the database. - A read that cannot be logged returns no personal data. - No token, detokenization call or clear identity number exists in any response.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-016-access-control-per-data-product-and-catalog-entries-v1.md` |
| Specification | `output/INC-029-epic-1-RWB-E1-016/specify/spec.md` |
| Compliance validation | `output/INC-029-epic-1-RWB-E1-016/specify/compliance-validation.md` |
| Agent run log | `output/INC-029-epic-1-RWB-E1-016/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-029-epic-1-RWB-E1-016/plan/` |
| Implementation evidence | `output/INC-029-epic-1-RWB-E1-016/implement/` |
| API / functional test reports | `output/INC-029-epic-1-RWB-E1-016/api-tests/`, `functional-tests/` |
| Review findings | `output/INC-029-epic-1-RWB-E1-016/review/` |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | Backlog — not started |
| Specification | NOT RUN — new v2 baseline |
| Compliance review | Not run |
| Acceptance criteria | 11 acceptance criteria |
| Test cases in story | 0 |
| Preserved implementation |  |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-016-access-control-per-data-product-and-catalog-entries-v1.md` |
| Output run | `output/INC-029-epic-1-RWB-E1-016/` |

