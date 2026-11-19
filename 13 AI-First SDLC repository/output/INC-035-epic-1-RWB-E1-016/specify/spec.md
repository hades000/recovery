# Technical Specification — RWB-E1-016 Access control per data product and catalog entries

| Field | Value |
|---|---|
| Story | RWB-E1-016 — Access control per data product and catalog entries |
| Epic / module | E1 / P1 Recovery data engine |
| RUN_ID | `INC-035-epic-1-RWB-E1-016` |
| Source requirement | `requirement/RecoveryWorkbench_Requirements.md` (FR-RWB-001; REQ-RDF-010, REQ-RDF-011); per-story file `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB E1 016 Access control per data product and catalog entries v1.md`; FSD P1 A2.15, A2.16; TSD P1 T3.1, T5.2, T6 |
| Upstream IDs | BRD section: Business Requirements Epic 1, 3.1 and 4; FR-RWB-001; REQ-RDF-010, REQ-RDF-011; FEAT-RDF-15, FEAT-RDF-16; US-RWB-E1-016; CTL-08, CTL-09, CTL-11; DL26; REQ-ACA-006 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | Product Owner (TBC); Compliance Reviewer (see `compliance-validation.md`) |

## Change Scope Declaration

| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — the story adds no screen, component, route, label or state. The case record view SCR-03 displays product data through the endpoint but its presentation is owned by RWB-E1-023/RWB-E1-035. |
| Logic In Scope | `YES` — capability check, access-row check, scope check, masking, PII access logging and whole-load validation. |
| API In Scope | `YES` — two endpoints are first delivered in this story: `GET /data-products/{productCode}/records` and `GET /admin/data-products`. |
| API Impact Type | `NEW_API_REQUIRED` |
| Impacted Existing Nodes | `data_product`, `sys_objects`, `sys_fields`, `retention_rule` (read); `party`, `contact_point`, `loan_account`, `collateral` and other P1 product tables (read); `data_product_access` (new). |
| New Nodes Required | `YES` — `DataProductController`, `DataProductAccessService`, `DataProductRecordService`, `DataProductCatalogService`, `DataProductAccessRepository`, `DataProductAccess`, `DataProductAccessLoader`. |
| Inherited Existing Behavior | Tables and metadata (RWB-E1-001); P4 role/permission matrix and masking interface (RWB-E1-037); data product rows (RWB-E1-064); ACE PII access logging; ACE capability check. |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `YES` |

## Requirement-to-SPEC Logic Coverage

| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | A role reads a data product only through a `data_product_access` row in force for that role and product. | SPEC-RWB-E1-016-002 | DIRECT | Repository query filters `valid_from <= today` and `valid_to` null or >= today. | COVERED |
| BR2 | A personal field is masked unless the masking rules let the role see it. | SPEC-RWB-E1-016-004 | DIRECT | `sys_fields.is_personal` drives the `MaskingPolicy` call. | COVERED |
| BR3 | With no masking rule loaded, every personal field stays masked. | SPEC-RWB-E1-016-004 | DIRECT | Empty policy result defaults to `MASKED`; fail-closed. | COVERED |
| BR4 | Every read of personal data is written to the PII access log; a read that cannot be logged is refused. | SPEC-RWB-E1-016-005 | DIRECT | Log write before response; 503 on failure. | COVERED |
| BR5 | A record outside the caller's scope is refused. | SPEC-RWB-E1-016-003 | DIRECT | `CaseScopeQuery.linksInScope`; 404 MSG-P4-003. | COVERED |
| BR6 | An access load with an exception is refused in full; the previous version stays in force. | SPEC-RWB-E1-016-007 | DIRECT | Whole-load validation before any insert; transactional apply. | COVERED |
| BR7 | Each data product has one catalog entry with owner, system of record, refresh cycle, retention and fields with PDPA tags. | SPEC-RWB-E1-016-006 | DIRECT | Catalog built from `data_product`, `sys_objects`, `sys_fields`, `retention_rule`. | COVERED |
| AC1 | RW-AUDIT reads DP02; mobile shows `******5678`; national ID returns `MASKED`; one PII log entry is written. | SPEC-RWB-E1-016-001, 004, 005 | DIRECT | Access row, masking and log in one read path. | COVERED |
| AC2 | 14 catalog entries, each with owner role, source, refresh, expected-by, retention class and field list; DP02 has 20 fields, 9 personal. | SPEC-RWB-E1-016-006 | DIRECT | Catalog response composed per product; field count from `sys_fields`. | COVERED |
| AC3 | RW-PHONECOL has no access row for DP06: 403 MSG-P4-002; refusal logged. | SPEC-RWB-E1-016-002, 005, 011 | DIRECT | Access-row denial path writes the refusal log. | COVERED |
| AC4 | An access load naming role `RW-UNKNOWN` is refused whole with MSG-P1-002; `DPA-2026.11` stays in force. | SPEC-RWB-E1-016-007 | DIRECT | Role code checked against the role table; no partial write. | COVERED |
| AC5 | RW-CASEOWN not owning the case: 404 MSG-P4-003; no row read. | SPEC-RWB-E1-016-003, 011 | DIRECT | Scope check precedes the product read. | COVERED |
| AC6 | No masking rule loaded: first name, last name, cif, date of birth and contact value masked. | SPEC-RWB-E1-016-004 | DIRECT | Default mask for every `is_personal` field. | COVERED |
| AC7 | PII access log rejects writes: 503 MSG-GEN-006; no personal field returned. | SPEC-RWB-E1-016-005, 011 | DIRECT | Log failure aborts before serialisation. | COVERED |
| AC8 | Access row valid from 2026-12-15, today 2026-12-14: 403 MSG-P4-002. | SPEC-RWB-E1-016-002 | DIRECT | `valid_from` boundary compared with the business date. | COVERED |
| X1 | No access row for the user's roles and the product. | SPEC-RWB-E1-016-002, 011 | DIRECT | 403 MSG-P4-002; refusal logged. | COVERED |
| X2 | Access load names a role code not in the roles table. | SPEC-RWB-E1-016-007 | DIRECT | Load refused whole; previous version stays. | COVERED |
| X3 | Case outside the caller's scope. | SPEC-RWB-E1-016-003 | DIRECT | 404 MSG-P4-003; no row read. | COVERED |
| X4 | No masking rule for a personal field. | SPEC-RWB-E1-016-004 | DIRECT | Field masked for every role. | COVERED |
| X5 | PII access log cannot be written. | SPEC-RWB-E1-016-005 | DIRECT | 503 MSG-GEN-006; no personal data returned. | COVERED |
| X6 | Access row valid-from date is after today. | SPEC-RWB-E1-016-002 | DIRECT | Row not in force; 403 MSG-P4-002. | COVERED |
| ST1 | An approved access version takes effect on its `valid_from` date. | SPEC-RWB-E1-016-008 | DIRECT | Loader writes rows with the version and valid-from date; no update of prior rows. | COVERED |

## User story intent interpretation

As a **data steward and data product owner (RW-DATASTEW)**, I want **read access to each data product granted by role, PDPA fields tagged, every read logged, and a catalog entry per product with owner, system of record, freshness and fields**, so that **personal data is read only by the roles that need it and every product is findable**.

The story delivers the read side of the data product store. It does not build a screen: it delivers two
APIs and the access data that other screens and services call. The case record view will consume the
record endpoint; auditors and analysts consume the catalog endpoint. Access and masking are data rows,
so a change of who sees what is a reference load, not a deployment.

## Entry trigger and preconditions

| Item | Value |
|---|---|
| Trigger | A user opens a data product view (`GET /data-products/{productCode}/records`) or the catalog (`GET /admin/data-products`); a reference load applies an approved access version. |
| Preconditions | RWB-E1-001 tables and `sys_objects`/`sys_fields` with `is_personal`; RWB-E1-037 role/permission matrix and `MaskingPolicy`; RWB-E1-064 `data_product` DP01–DP14; `DPA-2026.11` loaded and approved; ACE PII access logging available. |
| Input | Path `productCode`; query `caseId` (required), `page`, `size`; session roles and scope; access rows in force; `sys_fields` personal tags; masking rules. |
| Output | `DataProductRecordPage` with masked field map and freshness stamp; `DataProductCatalogEntry[]`; PII access log entries (allow and deny). |
| Feature flag | `rwb.dataengine.product-access`. Off: both endpoints return 404 and the case record view falls back to its prior path. |

## Field-level behaviour matrix

| Entity | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `data_product_access` | `product_code` | Reference load | System writes on approved load | Must be DP01–DP14 |
| `data_product_access` | `role_code` | Reference load | System writes on approved load | Must exist in the role table |
| `data_product_access` | `can_read` | Reference load | System writes | Boolean; false row grants nothing |
| `data_product_access` | `access_version` | Load header | System writes | One version per load; unique with product and role |
| `data_product_access` | `valid_from` / `valid_to` | Load header / row | System writes | `valid_from` required; `valid_to` optional; no overlap for one product and role |
| `party` | `first_name`, `last_name`, `cif_no`, `id_no_token`, `date_of_birth` | P1 tables | Read only | Masked when `sys_fields.is_personal` and no rule allows |
| `contact_point` | `value_token` | P1 tables | Read only | Masked; channel and consent status are not personal |
| `sys_fields` | `is_personal` | Data dictionary | Read only in this story | Drives masking; no field list in code |
| `data_product` | `owner_role`, `system_of_record`, `refresh_cycle`, `expected_by` | Reference data | Read only | One row per product |

## Status-transition matrix

| Record | From | Event | To | Side effects |
|---|---|---|---|---|
| `data_product_access` | Version in force | Approved load reaches `valid_from` | New version in force | New rows inserted; prior rows remain for history; reads use the row in force on the business date |
| Read request | — | Capability right missing | Refused | 403 MSG-P4-002; nothing read |
| Read request | — | Access row missing or not in force | Refused | 403 MSG-P4-002; refusal logged |
| Read request | — | Case out of scope | Refused | 404 MSG-P4-003; nothing read |
| Read request | — | PII log write fails | Refused | 503 MSG-GEN-006; no personal field returned |

No case status changes. This story changes the version in force of `data_product_access` only.

## Exceptional-case behaviour

| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | No access row for the user's roles and product | 403; no row read; refusal written to the access log | MSG-P4-002 |
| X2 | Access load names an unknown role | Load refused whole; `DPA-2026.11` stays in force | MSG-P1-002 |
| X3 | Case outside the caller's scope | 404; no row read; refusal logged | MSG-P4-003 |
| X4 | No masking rule for a personal field | Field masked for every role | None |
| X5 | PII access log cannot be written | Read refused with 503; no personal field returned | MSG-GEN-006 |
| X6 | Access row not yet in force | Row ignored; read refused until `valid_from` | MSG-P4-002 |

## API change assessment

| Item | Value |
|---|---|
| API Impact Type | `NEW_API_REQUIRED` |
| New endpoints | `GET /api/recovery/v1/data-products/{productCode}/records` (API-P1-010); `GET /api/recovery/v1/admin/data-products` (API-P1-011). |
| Contract delta | `DataProductRecordPage` (items, freshness, page, size, total) and `DataProductCatalogEntry[]` (productCode, productName, definition, ownerRole, systemOfRecord, refreshCycle, expectedBy, retentionClass, fields with entity, fieldName, fieldId, dataType, isPersonal). |
| Backward compatibility | New endpoints; no existing contract changes. The P4 reference-load endpoints are reused unchanged. |
| Authorization | Records: Case record R plus an access row in force. Catalog: Platform administration R. |
| Error behaviour | 400 missing `caseId` MSG-GEN-001; 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003; 503 MSG-GEN-006. |
| Versioning | First release E1; no version bump. Contract tests from the API specification (RWB-TE-003). |

## Unit Test Applicability

| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; SCR-03 presentation is owned by RWB-E1-023/RWB-E1-035. | Existing frontend tests remain green; no new frontend test required. |
| Backend | YES | REQUIRED | 80% lines, statements, branches and functions on changed code | REQ-RDF-010, REQ-RDF-011; SPEC-RWB-E1-016-001..015 | New controller, two services, catalog builder, loader and repository. | Positive, negative, boundary and error-path tests: access row present/absent/not yet valid; role present/absent; masking rule present/absent; scope in/out; log write failure; unknown role in a load; 14-entry catalog; DP02 field counts. |

## Detailed design

### Components

| Component | Type | Responsibility |
|---|---|---|
| `DataProductController` | Controller | Both GET endpoints; validation; problem responses. |
| `DataProductAccessService` | Service | Capability check, access-row check, scope call, PII log write. |
| `DataProductRecordService` | Service | Reads product rows for the case accounts/parties; masks personal fields. |
| `DataProductCatalogService` | Service | Builds catalog entries from `data_product`, `sys_objects`, `sys_fields`, `retention_rule`. |
| `DataProductAccessRepository` | Repository | Reads and writes `data_product_access` only. |
| `DataProductAccess` | Entity | One row per product, role and version. |
| `DataProductAccessLoader` | Published interface | Applies an approved access version. |

Package `recovery.dataengine.access`. Other modules are reached only through `CaseScopeQuery` (P3),
`MaskingPolicy` (P4) and the ACE access check. No role or permission table is read.

### Data and migration

- New table `data_product_access`: `id` uuid, `product_code` varchar(25), `role_code` varchar(20),
  `can_read` boolean, `access_version` varchar(20), `valid_from` date, `valid_to` date, standard
  columns; unique (`product_code`, `role_code`, `access_version`); index (`role_code`, `product_code`,
  `valid_from`).
- Reads: `sys_objects`, `sys_fields`, `data_product`, `retention_rule`, `party`, `contact_point`,
  `loan_account`, `collateral` and the other P1 product tables.
- Writes: `data_product_access` only.
- Migration is forward-only; no existing table is altered.

### Access check order

1. ACE capability check: Case record R for the records endpoint, Platform administration R for the catalog.
2. Session role codes resolved; `data_product_access` row in force for the product and any role with
   `can_read = true`.
3. `CaseScopeQuery.linksInScope(caseId, user)`; `CaseNotInScopeException` maps to 404.
4. Product rows read for the returned account and party IDs.
5. Personal fields masked through `MaskingPolicy`; empty result means `MASKED`.
6. PII access log written with user, product, case, field names and time — never values.
7. Response returned with the product freshness stamp (RWB-E1-015).

**Transaction.** The access load applies one version in one transaction; reads are read-only and do not
hold a transaction across the PII log write and the response. No event is published by this story.

### Catalog composition

One entry per `data_product` row: definition, owner role, system of record, refresh cycle,
expected-by, retention class from `retention_rule`, and the field list from `sys_fields` with
`field_id`, `data_type` and `is_personal`. No field list or product list is held in code.

### Access load validation

`DataProductAccessLoader.apply` validates the whole version before writing: known product code,
known role code, `can_read` present, `valid_from` present, no overlapping row for the same product and
role. Any failure refuses the whole load with MSG-P1-002; the prior version remains in force. The load
is one transaction.

### Security and authority

| Actor | Right | Scope |
|---|---|---|
| RW-DATASTEW | Platform administration R (catalog) | All |
| RW-REFADM | Reference data C (access load) | All |
| RW-COMPLY | Owns masking rules; catalog R | All |
| RW-SECADM | Owns role matrix; access-log read | All |
| RW-COE, RW-AUDIT, RW-PLATADM | Catalog R | All |
| RW-CASEOWN, RW-AUDIT and other case roles | Case record R plus access row | Own / role scope |
| SY-DATALOAD | Applies approved access version | All |

Every endpoint uses Spring Security method security naming the capability area and right. Denials and
out-of-scope reads are written to the PII access log with no field values.

### Observability and operations

- Metrics: reads allowed, reads denied (no row / out of scope / log failure), catalog reads, load
  refusals.
- Alerts: PII access log unavailable; access load refused.
- Audit: PII access log entry per read and per denial; access version in force is queryable.
- Run book entry under RWB-E1-056 for the access load.

### Performance

- Catalog: one query per metadata table, assembled in memory; 14 products and their fields.
- Records: paged read on the product table; page size bounded by the API contract.
- No caching of access decisions across requests; a version change takes effect on the next request.

### Feature flag and rollback

`rwb.dataengine.product-access`. Off: both endpoints return 404; the prior case-record read path is
used. Rollback: turn the flag off; the new table remains and is harmless.

## Test scenarios

| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-E1-016-01 | AC1, BR1, BR2, BR4 | System | RW-AUDIT; case RW-2026-000102; synthetic party | Mobile `******5678`; national ID `MASKED`; one PII log entry |
| TC-E1-016-02 | AC2, BR7 | System | 14 products; DP02 20 fields, 9 personal | 14 entries; all catalog attributes present; DP02 counts match |
| TC-E1-016-03 | AC3, BR1 | System | RW-PHONECOL; DP06 | 403 MSG-P4-002; denial logged |
| TC-E1-016-04 | AC4, BR6 | System | Load with `RW-UNKNOWN` | Whole load refused MSG-P1-002; `DPA-2026.11` in force |
| TC-E1-016-05 | AC5, BR5 | System | RW-CASEOWN; case not owned | 404 MSG-P4-003; no row read |
| TC-E1-016-06 | AC6, BR3 | System | RW-COMPLY; no masking rules | All listed personal fields masked |
| TC-E1-016-07 | AC7, BR4 | System | PII log stub rejecting writes | 503 MSG-GEN-006; no personal field returned |
| TC-E1-016-08 | AC8, BR1 | System | Row valid from 2026-12-15; clock 2026-12-14 | 403 MSG-P4-002 |
| TC-E1-016-09 | X2 | System | Load with overlapping rows | Whole load refused; no partial write |
| TC-E1-016-10 | Access | Security | RW-TRIBE calls the catalog | 403 MSG-P4-002 |
| TC-E1-016-11 | BR2, BR3 | Unit | Masking policy present/absent; personal/non-personal field | Policy applied; absent rule masks; non-personal untouched |

## Clarification Log

| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1; SPEC-002 | Which access version is in force at go-live? | The version is data; the read must use the row in force. | `DPA-2026.11`, loaded and approved per story §3. | RESOLVED | SPEC-002 |
| CLAR-002 | BR3; SPEC-004 | What happens when Compliance has not loaded masking rules? | Determines default masking. | DL26: every personal field is masked until a rule is loaded. | RESOLVED | SPEC-004 |
| CLAR-003 | BR6; SPEC-007 | Is the access load whole-file or row-by-row? | Determines partial-write behaviour. | Whole-load refusal; the previous version stays in force (story AC4, BR6). | RESOLVED | SPEC-007 |
| CLAR-004 | BR4; SPEC-005 | Must the PII log write complete before the response? | Determines whether an unlogged read can return data. | Yes; a read that cannot be logged is refused with 503 (story BR4, AC7). | RESOLVED | SPEC-005 |
| CLAR-005 | API; SPEC-009 | Are the two endpoints new or reused? | Determines the API impact type. | New in this story; API-P1-010 and API-P1-011, first release E1. | RESOLVED | SPEC-009 |
| CLAR-006 | UI; SPEC-013 | Does the story change SCR-03? | Determines UI scope and design evidence. | No; SCR-03 presentation is owned by RWB-E1-023/RWB-E1-035. The story supplies the API only. | RESOLVED | SPEC-013 |
| CLAR-007 | BR2; SPEC-004 | Which fields are personal? | Determines masking coverage. | `sys_fields.is_personal` is authoritative; no list in code (story §11, BR2). | RESOLVED | SPEC-004 |

`CLARIFICATION_STATUS: RESOLVED` — all 7 items are answered from the story, the FSD/TSD or DL26. No
item changes the business outcome.

## Status reporting

```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this API-only story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New backend access-control and catalog capability; two new read endpoints; no screen change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: YES] [API_IMPACT: NEW_API_REQUIRED] [REASON: new data-product read and catalog endpoints with PDPA masking]
REQUIREMENT_COVERAGE_SUMMARY: All 7 business rules, 8 acceptance criteria, 6 exception paths, 1 data state transition and 4 read outcomes are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
