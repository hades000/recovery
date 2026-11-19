# Increment Card — INC-035-epic-1-RWB-E1-016

**RWB-E1-016 — Access control per data product and catalog entries**

## Identification

| Field | Value |
|---|---|
| Increment ID | `INC-035` |
| Title | Access control per data product and catalog entries |
| Programme / product | Recovery Workbench (recovery module of ACE) |
| Jira epic / key | `E1` / `RWB-E1-016` |
| RUN_ID | `INC-035-epic-1-RWB-E1-016` |
| Parent epic card | `epics/EPIC-001-foundation-1.md` |
| Module | P1 Recovery data engine |
| Story type | User story |
| Priority | Must |
| Window | Window 2 |
| Critical path | Yes |
| Depends on | RWB-E1-037, RWB-E1-001, RWB-E1-064 |
| Status | In delivery |

## Project type

**Path:** Greenfield development of the Workbench module with brownfield ACE integration constraints. The full 13-question classification is in `epics/EPIC-001-foundation-1.md` and applies to this story.

**Story type:** User story. **Module:** P1 Recovery data engine. **Build group:** P1b.

## Scope

**Story:** As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, PDPA fields tagged, every read logged, and a catalog entry per product with owner, system of record, freshness and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

**Main flow:**
1. User: opens a data product view, which calls GET /data-products/{productCode}/records?caseId=.
2. DataProductAccessService: checks the capability right Case record R through the ACE access check.
3. DataProductAccessService: checks data_product_access for a row in force for one of the user's roles and the product.
4. DataProductAccessService: calls the P3 case scope interface for the case's accounts and parties in the user's scope.
5. DataProductRecordService: reads the product rows for those accounts or parties from P1 tables.
6. DataProductRecordService: for each field tagged is_personal in sys_fields, applies the P4 masking interface for the user's roles.

**Out of scope:**
- The role to permission matrix and the masking rule mechanism (RWB-E1-037).
- The access log search and break-glass (RWB-E1-039).
- Masking rule values per role and field (DL26, Compliance).
- The personal data screen SCR-47 (Epic 8).
- Data product definitions and the field dictionary (RWB-E1-064).

**Business outcome and value hypothesis:** Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Access per data product, held as data rows, limits each role to the products its work needs; PDPA tags on each field drive masking; and every read goes to the PII access log. The catalog gives one entry per product so a developer, an analyst or an auditor finds the owner, the source, the freshness rule, the retention and the personal fields without asking. Serves REQ-RDF-010 and REQ-RDF-011.

**Constraints and guardrails:**
- No business value in code: access by role and masking by role are data rows; the code holds no role or product list.
- No personal data in logs, tests or prompts: the PII access log carries field names, not values; test parties are synthetic.
- No read of another module's tables: case scope comes from CaseScopeQuery, masking from MaskingPolicy, roles from the session.
- A read that cannot be logged returns no personal data.

## Reused approved artefacts

| Artefact | Version / link |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 016 Access control per data product and catalog entries v1.md` |
| Requirement IDs | REQ-RDF-010, REQ-RDF-011 |
| BRD section | Business Requirements Epic 1, section 3.1 (story) and section 4 (REQ-RDF-010, REQ-RDF-011) |
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
| RW-DATASTEW, data steward | Prepares the access rows for their products; reads the catalog (Platform administration R) |
| RW-REFADM, reference data administrator | Submits the access load through POST /admin/reference-loads (Reference data C) |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules (DL26); reads the catalog |
| RW-SECADM, security administrator | Owns the role to permission matrix; reads the access log |
| RW-COE, RW-AUDIT, RW-PLATADM | Read the catalog (Platform administration R) |
| Roles with Case record R and an access row, for example RW-CASEOWN, RW-AUDIT | Read a data product for a case in scope |
| SY-DATALOAD, data load | Applies an approved access version to data_product_access |

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
| Quality and release | API Tester | Applicable | Required by the spec's API scope. |
| Quality and release | Functional Automation Test | Not used | UI is not in scope. |
| Quality and release | Azure Deploy pipeline | Not used | ACE uses its own pipeline. |

## Risk, rollback and stop signals

- **Rollback route:** feature flag off or redeploy the previous tag; see `epics/EPIC-001-foundation-1.md`.
- **Feature flag:** `rwb.dataengine.product-access`.
- **Critical path:** Yes; **depends on:** RWB-E1-037, RWB-E1-001, RWB-E1-064.
- **Stop signals:** see the epic card; story guardrails are:
  - No business value in code: access by role and masking by role are data rows; the code holds no role or product list.
  - No personal data in logs, tests or prompts: the PII access log carries field names, not values; test parties are synthetic.
  - No read of another module's tables: case scope comes from CaseScopeQuery, masking from MaskingPolicy, roles from the session.
  - A read that cannot be logged returns no personal data.

## Evidence links

| Evidence | Location |
|---|---|
| Story file | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 016 Access control per data product and catalog entries v1.md` |
| Specification | `output/INC-035-epic-1-RWB-E1-016/specify/spec.md` |
| Compliance validation | `output/INC-035-epic-1-RWB-E1-016/specify/compliance-validation.md` |
| Agent run log | `output/INC-035-epic-1-RWB-E1-016/specify/agent-run-log.md` |
| Plan and tasks | `output/INC-035-epic-1-RWB-E1-016/plan/` (TBC) |
| Implementation evidence | `output/INC-035-epic-1-RWB-E1-016/implement/` (TBC) |
| API / functional test reports | `output/INC-035-epic-1-RWB-E1-016/api-tests/`, `functional-tests/` (TBC) |
| Review findings | `output/INC-035-epic-1-RWB-E1-016/review/` (TBC) |
| Traceability | `requirement/Traceability_Matrix.md` |

## Card status

| Field | Value |
|---|---|
| Status | In delivery |
| Specification | SUCCESS — spec matches the current story ACs |
| Compliance review | PASS — gate-002 re-run 2026-11-06 (see `output/INC-035-epic-1-RWB-E1-016/specify/compliance-validation.md`) |
| Acceptance criteria | 8 ACs in the current story (AC1, AC2, AC3, AC4, AC5, AC6, AC7, AC8) |
| AC numbering | None — AC numbering is contiguous |
| Story source | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 016 Access control per data product and catalog entries v1.md` |
| Output run | `output/INC-035-epic-1-RWB-E1-016/specify/` |
| Card history | Backfilled on 2026-11-04; split from the epic card now at `epics/EPIC-001-foundation-1.md`. Future increments create the story card before the Technical Specifier starts. |
