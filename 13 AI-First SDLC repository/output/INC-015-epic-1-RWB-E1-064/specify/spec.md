# Technical Specification — RWB-E1-064 Data dictionary for the 14 data products

| Field | Value |
|---|---|
| Story | RWB-E1-064 — Data dictionary for the 14 data products |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-015-epic-1-RWB-E1-064` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (REQ-RDF-001, REQ-RDF-011); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 064 Data dictionary for the 14 data products v1.md` |
| Upstream IDs | REQ-RDF-001, REQ-RDF-011; US-RWB-E1-064; R-UNI-38; CTL-08; DL12; DL41 (count only) |
| Status | `SUCCESS` |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen. The dictionary and contracts are read and changed through endpoints; story §15. |
| Logic In Scope | `YES` — dictionary attributes, field versioning, contract per source, confirmation, publish rule, new version on change. |
| API In Scope | `YES` — five endpoints: `GET /admin/data-dictionary/fields`, `PATCH /admin/data-dictionary/fields/{fieldCode}`, `GET /admin/data-contracts`, `PATCH /admin/data-contracts/{contractId}`, `POST /admin/data-contracts/{contractId}/publish` (API-P1-012..016). |
| API Impact Type | `NEW_API_REQUIRED` — new endpoints; contract deltas noted below. |
| Impacted Existing Nodes | `sys_fields` (extended), `sys_field_version` (new), `data_contract` (new), `data_product` (read, created by RWB-E1-001); reference data service (RWB-E1-043). |
| New Nodes Required | `YES` — `DataDictionaryController`, `DataDictionaryService`, `DataContractService`, `DataDictionaryLoader`, `DataDictionaryQuery`, `SysFieldRepository`, `SysFieldVersionRepository`, `DataContractRepository`, `DataProductRepository`. |
| Inherited Existing Behavior | `sys_objects`/`sys_fields` seed (RWB-E1-001); reference load/approve (RWB-E1-043); LOV-ROLE and LOV-REFRESH. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every field carries type, source system, source field, refresh, owner and behaviour when late. | SPEC-RWB-E1-064-002, 003, 014 | DIRECT | The loader validates the six attributes; `data_type`/`physical_type` come from E1-001. | COVERED |
| BR2 | Each data product has one system of record and one owner role. | SPEC-RWB-E1-064-012 | DIRECT | Reads `data_product`; no duplicate table in this story. | COVERED |
| BR3 | A contract is published only after the system owner's confirmation. | SPEC-RWB-E1-064-005, 006, 007 | DIRECT | `confirmed_by_role`, `confirmed_on`, `confirmation_document_ref`; publish refuses without them. | COVERED |
| BR4 | A field change creates a new version with date and reason; earlier versions stay readable. | SPEC-RWB-E1-064-004, 009 | DIRECT | `sys_field_version`; unique `(field_id, field_version)`. | COVERED |
| BR5 | A dictionary load with an exception is refused whole. | SPEC-RWB-E1-064-002, 011 | DIRECT | `validate` writes nothing; `apply` one transaction. | COVERED |
| BR6 | A change to a published contract's field opens a new DRAFT version; the published version stays in force. | SPEC-RWB-E1-064-008 | DIRECT | New `data_contract` row with version+1, status DRAFT; old row PUBLISHED. | COVERED |
| AC1 | DF-ACC-014 shows type, physical type, source, refresh, owner and late behaviour; all fields in force are complete. | SPEC-RWB-E1-064-003, 014 | DIRECT | `GET /admin/data-dictionary/fields`; count is the dictionary in force (DL41). | COVERED |
| AC2 | A confirmed DC-ALS publishes as v1 and its 32 fields show Confirmed. | SPEC-RWB-E1-064-006, 007, 016 | DIRECT | Confirmation recorded; publish sets status and field mapping status. | COVERED |
| AC3 | A field change to DPD_DAYS creates v2 with reason; v1 stays readable. | SPEC-RWB-E1-064-004 | DIRECT | `If-Match` version; new `sys_field_version` row. | COVERED |
| AC4 | Publish without confirmation returns 409 and stays DRAFT. | SPEC-RWB-E1-064-007 | DIRECT | MSG-P1-021. | COVERED |
| AC5 | A change with an empty reason returns 422 and leaves the field at v1. | SPEC-RWB-E1-064-004, 010 | DIRECT | MSG-GEN-001. | COVERED |
| AC6 | A load with a missing refresh cycle is refused whole. | SPEC-RWB-E1-064-002, 011 | DIRECT | MSG-P1-002 with the check text. | COVERED |
| AC7 | Two changes from version 1: first saves v2, second returns 409. | SPEC-RWB-E1-064-009 | DIRECT | Optimistic lock; MSG-GEN-004. | COVERED |
| AC8 | A change to a published contract's field creates a DRAFT v2; v1 stays PUBLISHED. | SPEC-RWB-E1-064-008 | DIRECT | Contract versioning. | COVERED |
| X1 | Publish without confirmation. | SPEC-RWB-E1-064-007 | DIRECT | 409 MSG-P1-021. | COVERED |
| X2 | Field change without a reason. | SPEC-RWB-E1-064-004 | DIRECT | 422 MSG-GEN-001. | COVERED |
| X3 | Dictionary load with a missing attribute. | SPEC-RWB-E1-064-002 | DIRECT | Refuse whole; MSG-P1-002. | COVERED |
| X4 | Two stewards change the same field from the same version. | SPEC-RWB-E1-064-009 | DIRECT | Second gets 409 MSG-GEN-004. | COVERED |
| X5 | A field of a published contract changes. | SPEC-RWB-E1-064-008 | DIRECT | New DRAFT contract version. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **every field in the 14 data products typed, sourced and owned, with a data contract per source system that its owner confirms**, so that **a data contract can be agreed with the system that owns it**.

The story turns the dictionary into versioned data and groups the mapped fields into one contract per source system. A contract is a written agreement: it is published only after the system owner's confirmation is recorded. A change never edits a published contract in place.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | RW-REFADM loads dictionary attributes through `POST /admin/reference-loads` with `table = sys_fields`; RW-DATASTEW confirms, records contract confirmations, publishes and changes fields. |
| Preconditions | RWB-E1-001 done (`sys_objects`, `sys_fields`, `data_product`); RWB-E1-043 done; RW-DATASTEW holds Reference data RU; RW-REFADM holds Reference data CRUD; the source mapping lists 108 mapped fields across INT-01..INT-16. |
| Input | Dictionary attribute file; contract confirmation details; field change with reason. |
| Output | `sys_fields` attributes, `sys_field_version` rows, `data_contract` rows; API responses. |
| Feature flag | `rwb.dataengine.data-dictionary`. Off: endpoints and loader unavailable. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `sys_fields` | `owner_role` | Attribute load | Reference data U | Must be in LOV-ROLE. |
| `sys_fields` | `refresh_cycle` | Attribute load | Reference data U | DAILY, WEEKLY, MONTHLY, ON_CHANGE; free text up to 30. |
| `sys_fields` | `late_behavior` | Attribute load | Reference data U | Required; text up to 200. |
| `sys_fields` | `interface_id` | Attribute load | Reference data U | Required for mapped fields; INT-xx. |
| `sys_fields` | `source_system`, `source_field` | Attribute load | Reference data U | Required for every mapped field. |
| `sys_field_version` | `field_version` | System | System | Starts at 1; increments per change; unique with `field_id`. |
| `sys_field_version` | `definition` | System snapshot | System | JSON of the changed attributes. |
| `sys_field_version` | `change_reason` | Change request | Reference data U | Required; text up to 400. |
| `data_contract` | `contract_code` | Source system | System | Unique per version; e.g. `DC-ALS`. |
| `data_contract` | `source_system` | Source system | System | One contract per source system. |
| `data_contract` | `interface_id` | Derived from fields | System | Primary interface; the API list is derived from `sys_fields`. |
| `data_contract` | `contract_version` | System | System | Starts at 1; increments. |
| `data_contract` | `status` | System | System | DRAFT, PUBLISHED, SUPERSEDED. |
| `data_contract` | `confirmed_by_role`, `confirmed_on`, `confirmation_document_ref` | Confirmation | Reference data U | Required before publish. |

## Status-transition matrix

| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| None | Field loaded | Six attributes valid | Version 1 | `sys_fields` updated; `sys_field_version` v1. |
| Version N | Field change | Reason present; `If-Match` current | Version N+1 | New `sys_field_version`; old version readable. |
| None | Contract created | Source system has mapped fields | DRAFT v1 | `data_contract` row. |
| DRAFT | Confirmation recorded | Role, date, document present | DRAFT (confirmed) | Confirmation fields set. |
| DRAFT (confirmed) | Publish | Confirmation present | PUBLISHED | Field mapping status Confirmed. |
| PUBLISHED | Field of the contract changes | Any mapped field changes | PUBLISHED + DRAFT v2 | New DRAFT row; v1 stays in force. |
| PUBLISHED | New version published | v2 confirmed and published | v1 SUPERSEDED, v2 PUBLISHED | Old version valid-to set. |

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Publish without confirmation | 409; contract stays DRAFT. | MSG-P1-021 |
| X2 | Field change without a reason | 422; no version written. | MSG-GEN-001 |
| X3 | Dictionary load with a missing attribute | Refuse whole; previous dictionary stays. | MSG-P1-002 |
| X4 | Two changes from the same version | First saves; second 409. | MSG-GEN-004 |
| X5 | Field of a published contract changes | New DRAFT contract version; published stays. | None |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | API-P1-012..016: dictionary field search, field change, contract list, contract confirmation, contract publish. |
| Contract delta | (1) `DataContractConfirmation.confirmationDocumentId` is `uuid`; the data model stores `confirmation_document_ref varchar(400)` and AC2 uses `DOC-SYN-0640`. Use a string `confirmationDocumentRef`; update the schema. (2) `DataContract.interfaceIds` is an array; `data_contract.interface_id` is a scalar. The service derives the list from the contract's fields; no schema change. |
| Backward compatibility | New endpoints; no existing consumer. |
| Authorization | Reference data R for reads; Reference data U for changes, confirmation and publish. |
| Error behaviour | 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 409 MSG-GEN-004 / MSG-P1-021; 422 MSG-GEN-001; 503 MSG-GEN-006. |
| Versioning | Additive; update API Specification v2 before implementation (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | Story §15 states no screen; all reads and changes use endpoints. | Existing frontend tests remain green; no new frontend test. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-001, REQ-RDF-011; SPEC-RWB-E1-064-001..016 | New loader, services, repositories, controller and contract versioning. | Positive, negative, boundary and error-path tests: six attributes; missing attribute; versioning; reason required; optimistic lock; confirmation; publish rule; new DRAFT on published change; 403. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DataDictionaryController` | Controller | Five endpoints; capability checks; Problem mapping. |
| `DataDictionaryService` | Service | Field reads, versioned changes with reason, optimistic lock. |
| `DataContractService` | Service | Contract per source system; confirmation; publish rule; new version on change. |
| `DataDictionaryLoader` | Published interface | Whole-load validation and apply. |
| `DataDictionaryQuery` | Published interface | Field and product definitions for other packages and modules. |
| `SysFieldRepository`, `SysFieldVersionRepository`, `DataContractRepository`, `DataProductRepository` | Repository | Read and write the tables. |
| `SysField`, `SysFieldVersion`, `DataContract`, `DataProduct` | Entity | One per table. |

### Data and migration

- Adds `owner_role varchar(20)`, `refresh_cycle varchar(30)`, `late_behavior varchar(200)`, `interface_id varchar(10)` to `sys_fields`.
- Creates `sys_field_version` (id, field_id, field_version, definition jsonb, change_reason, changed_at, changed_by; unique `(field_id, field_version)`).
- Creates `data_contract` (id, contract_code, source_system, interface_id, contract_version, status, confirmed_by_role, confirmed_on, confirmation_document_ref, published_at, published_by, standard columns; unique `(contract_code, contract_version)`).
- Does **not** create `data_product`; it is created and seeded by RWB-E1-001. This story reads it.
- Seeds version 1 of every field in the dictionary in force. Under DL41 option A that is 413 fields; under option B, 1,256. The loader and tests read the count at run time.

### Rules

1. The load must carry six attributes per field: `source_system`, `source_field`, `refresh_cycle`, `owner_role`, `late_behavior`, `interface_id`. `data_type` and `physical_type` are read from the E1-001 seed.
2. Any missing attribute refuses the whole load with MSG-P1-002 and the first failing check.
3. A field change requires a reason, the current `If-Match` version and a new `sys_field_version` row.
4. A contract is one per source system. Its fields are the `sys_fields` rows with that `source_system`; its interfaces are the distinct `interface_id` values of those fields.
5. Publish requires `confirmed_by_role`, `confirmed_on` and `confirmation_document_ref`; otherwise 409 MSG-P1-021.
6. A change to a field of a PUBLISHED contract creates a new DRAFT contract version; the published version stays in force until the new one is published.

### Transaction and events

- Dictionary load: one transaction; a failure rolls back all attributes and versions.
- Field change: one transaction for the `sys_fields` update and the `sys_field_version` insert.
- Contract publish: one transaction for the contract status and the field mapping status.
- No event is published; the `ReferenceLoad` and the contract row are the record.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-DATASTEW | Reference data U — change fields, record confirmations, publish | All |
| RW-REFADM | Reference data C — submit the dictionary load | All |
| RW-COE | Reference data CRUD — read and change fields | All |
| RW-TRIBE, RW-AUDIT and other R roles | Reference data R | All |
| SY-DATALOAD | Apply an approved dictionary load | All |
| Any other role | None | 403 MSG-P4-002 |

The dictionary holds definitions, not values; the confirmation names a role, not a person.

### Observability and operations

- `GET /admin/data-dictionary/fields` and `GET /admin/data-contracts` are the read surfaces.
- `ReferenceLoad` records the dictionary load; `data_contract` records the version and publish.
- No job or alert; a contract without confirmation is visible as DRAFT.

### Performance

- The dictionary is 413–1,256 fields; paged reads with `page`/`size`.
- Contract building is a grouped query by `source_system`; no per-field call.
- Field changes are single-row writes with an index on `(field_id, field_version)`.

### Feature flag and rollback

- `rwb.dataengine.data-dictionary`. Off: endpoints and loader unavailable.
- Rollback: a published contract is superseded by the previous version; a field version is never deleted. The migration is forward-only.

### No UI change

No screen. SCR-40 Reference data arrives in E8; developers and analysts use the endpoints.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-064-01 | AC1, BR1, BR2 | System | Seeded dictionary; DF-ACC-014 | Type NUMBER, integer, ALS source, DELAY_DAYS, Daily end of day, RW-DATASTEW, keep previous/mark stale |
| TC-E1-064-02 | AC2, BR3 | System | DC-ALS, 32 fields, confirmation 2026-11-12, DOC-SYN-0640 | PUBLISHED v1; 32 fields Confirmed |
| TC-E1-064-03 | AC3, BR4 | System | Change DF-ACC-014 source field to DPD_DAYS with reason | v2 dated 2026-11-18; v1 readable |
| TC-E1-064-04 | AC4, BR3 | System | DC-EFS no confirmation | 409 MSG-P1-021; stays DRAFT |
| TC-E1-064-05 | AC5, BR4 | System | Change DF-ACC-015 with empty reason | 422 MSG-GEN-001; stays v1 |
| TC-E1-064-06 | AC6, BR5 | System | DF-COL-005 no refresh cycle | Refused whole; MSG-P1-002 |
| TC-E1-064-07 | AC7 | System | Two changes to DF-ACC-016 from v1 | First v2; second 409 MSG-GEN-004 |
| TC-E1-064-08 | AC8, BR6 | System | Published DC-ALS; DF-ACC-014 changes | DRAFT v2; v1 stays PUBLISHED |
| TC-E1-064-09 | X4 | Security | RW-TRIBE PATCH field | 403 MSG-P4-002 |
| TC-E1-064-10 | BR1 | Unit | Each of the six attributes missing | Load refused; first failing check named |

## Guardrails

- Owners, cycles, late behaviour and contract content are data rows.
- No personal data in logs, tests or prompts; the dictionary holds definitions, not values.
- No read of another module's tables; other modules use `DataDictionaryQuery`.
- A published contract is never edited in place; a change makes a new version.

## Out of scope

- Catalog endpoint, access by product and PDPA masking (RWB-E1-016).
- Freshness (RWB-E1-015), retention (RWB-E1-017), SCR-40 (Epic 8).
- Contracts for stage 2 data products (RWB-E2-010).

## Traceability

| Requirement ID | Requirement (short) | Rules | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, one system of record and one owner | CTL-08; DL12; DL41 | TC-E1-064-01, 02, 04, 06 |
| REQ-RDF-011 | Catalog entry per product with definition, owner, source and refresh | R-UNI-38 | TC-E1-064-03, 05, 07, 08 |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1, AC1; SPEC-002, 014 | Flow step 1 names four load attributes; BR1/AC1 require six. | Which attributes the loader validates. | The six loaded attributes are source system, source field, refresh cycle, owner role, late behaviour and interface. Data type and physical type come from the E1-001 seed. | `RESOLVED` | SPEC-002, 014 |
| CLAR-002 | AC1; SPEC-003 | The story asserts 1,256 fields and 108 entities; DL41 is open and recommends 41/413. | Test fixture and completeness assertion. | DL41's recommendation says E1-064 takes the count in force; the loader and tests read the count, not a fixed 1,256. No behaviour change. | `RESOLVED` | SPEC-003 |
| CLAR-003 | BR3, AC2; SPEC-006 | API uses `confirmationDocumentId` (uuid); the data model uses `confirmation_document_ref varchar(400)`; AC2 uses `DOC-SYN-0640`. | Confirmation contract. | Use a string `confirmationDocumentRef`; update the API schema. | `RESOLVED` | SPEC-006 |
| CLAR-004 | SPEC-001, 012 | Story §13 creates and seeds `data_product`; E1-001 already creates it. | Duplicate table and seed. | E1-064 must not recreate `data_product`; it reads the E1-001 table. | `RESOLVED` | SPEC-001, 012 |
| CLAR-005 | SPEC-005, 013 | `data_contract.interface_id` is a scalar; the API returns `interfaceIds` as a list. | Contract response. | Store the primary interface; derive the list from the contract's fields. No schema change. | `RESOLVED` | SPEC-005, 013 |
| CLAR-006 | SPEC-004 | Flow step 8 uses `{fieldId}`, section 12 uses `{fieldCode}`. | Path parameter. | Both are the BR Field ID (`DF-ACC-014`); use `{fieldCode}` per API-P1-013. | `RESOLVED` | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all 6 items are answered from the story, TSD, physical schema or API
contract. CLAR-002 depends on DL41 for the test count only; the logic is not blocked.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this backend story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New dictionary versioning and data-contract capability; five new endpoints; no UI.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new dictionary, contract versioning and five endpoints]
REQUIREMENT_COVERAGE_SUMMARY: All 6 business rules, 8 acceptance criteria and 5 exception paths are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 6] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
