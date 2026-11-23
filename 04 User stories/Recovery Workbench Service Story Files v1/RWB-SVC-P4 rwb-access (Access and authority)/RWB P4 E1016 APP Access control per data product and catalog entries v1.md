# RWB-P4-E1016-APP Access control per data product and catalog entries

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P4-E1016-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-access |
| Service epic | RWB-SVC-P4 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-016 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP02, DP05, DP07, DP08, DP11, DP19 |
| Parallel lane | L-P4-N |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P4 rwb-access v1.md (FR-P4-016, FR-P4-018, FR-P4-023, FR-P4-024, FR-P4-025, FR-P4-026, FR-P4-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-016 for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **security administrator (RW-SECADM), a compliance and PDPA officer (RW-COMPLY) and every caller of the authorise contract**, I want **the Recovery roles, their permission rows and the masking policy held as data in `rwb_access` and served as three answers — the role catalogue with its permissions, default scope, role class, masking exceptions and matrix version, the masking policy with a marker per field ID at the masking version in force, and the data-product half of the authorise answer with allowed or refused, the matrix version, the masking version and a marker per field**, so that **no screen, no service and no agent keeps its own copy of the permission matrix or of the masking rules, and a data-product read is allowed, refused and masked from one place that changes with a version and without a deployment**.

Inside `rwb-access` this is the policy and catalogue half of the legacy story RWB-E1-016:

- Service `rwb-access`, schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Three deliverables, and nothing else: the role catalogue read `GET /api/recovery/access/v1/admin/roles` (API-P4-007), the masking policy read `GET /api/recovery/access/v1/masking-policies`, and the data-product half of `POST /api/recovery/access/v1/authorise`, which takes the capability area, the right, a product code, a case reference and a field list, and answers allowed or refused with the matrix version, the masking version and a marker per field ID.
- The P4 catalogue entries of the legacy story are the `role`, `permission` and `masking_rule` rows of this service: each role with its permission rows, each role's default scope and role class, the `unmasked` exceptions of the masking policy and the two version labels in force. There is no other catalogue of this service.
- The other half of the legacy key is not built here: the `data_product`, `data_product_access`, `data_product_load`, `sys_objects` and `sys_fields` rows, the 14 catalog entries, the 30 `recovery.v_ace_*` views and their grants are P1's (RWB-P1-E1016-APP, RWB-P1-E1016-CON and RWB-P1-E1016-DB); the retention class of a catalog entry is P5's (RWB-P5-E1016-APP); the end-to-end proof of the composed entry is RWB-ITG-E1016-ITG. This story reads none of those rows, defines none of them and calls none of the views.
- No event is published by this slice. DP-09 is not a pattern of this story, so the policy-change event of the service (`rwb.access.AccessPolicyChanged.v1`) is the load story's and not this one's, and the access entry of a data-product read is the access-log story's (RWB-P4-E1039-APP).

### 2. Business rationale

Audit findings record staff sending debtor data outside the bank and users holding access they did not need (CTL-11, CTL-09). Legacy RWB-E1-016 answers both within one engine: access to a data product is the role's access row plus the database grant on the view, personal fields are masked by role, and one catalog entry per product names its owner, its source, its freshness and its personal fields. The legacy story also reads the role to permission matrix and the masking rules through the ACE access check and `FieldMasker`, so the matrix, the scope and the masking policy are already the policy inputs of every data-product answer it gives.

In the target those inputs are a service of their own. Architecture v5 slide 41 gives P4 `rwb-access` the Recovery roles as data, the scope and the masking policy; slide 14 puts `POST /authorise`, `GET /me/permissions`, `GET /doa-limits` and `/masking-policies` on its inbound surface. The role catalogue is API-P4-007 of TSD P4 appendix T-A, the read that the administration screens and the auditors need, and the data-product answer becomes the part of `POST /authorise` that carries a product code. The rows behind all three are the ones TSD P4 T3.1 already defines: `role` (DF-REF-034 to DF-REF-039), `permission` with its `matrix_version` (DF-REF-040 to DF-REF-044) and `masking_rule` with its `masking_version` (DF-REF-198 to DF-REF-204). This story therefore re-specifies no data product, no access row and no view: it serves the policy side of the legacy answer, and it keys the masking rows on field IDs the P1 dictionary publishes.

The remainder of the legacy key is a split, not a copy. The data products, the access rows and the 14 catalog entries are P1's data engine; the retention class is P5's; the composed entry a data steward reads is proved by RWB-ITG-E1016-ITG. What is left in P4 is exactly what the legacy story uses as a policy store: the roles, the matrix and the masking rows, plus the two catalogue reads and the data-product answer that name them.

The story meets REQ-RDF-010 by making the personal fields of a data-product read maskable by role from one place, REQ-RDF-011 by resolving the owner role and the masking exceptions that a catalog entry names, and REQ-ACA-006 by returning the field IDs and the markers that the access entry of a data-product read carries. It supports controls CTL-09 and CTL-11 and the measure that rule and limit changes need no code release: a new matrix or masking version takes effect on its valid-from date with no deployment.

No source names the request and answer fields of these three operations, and no source says whether the role catalogue carries masking exceptions at all: that field set, the marker vocabulary and the meaning of the masking-exceptions part are Not specified in the source documents (GAP-0983; ASM-1722). The story fixes them as stated below and in section 12, keeps every business value a data row, and changes no value that a source does name.

### 3. Preconditions

- RWB-P4-E1037-APP delivered the `rwb_access` baseline: the tables `role` (DF-REF-034 to DF-REF-039), `permission` (DF-REF-040 to DF-REF-044), `masking_rule` (DF-REF-198 to DF-REF-204) and `role_conflict` (DF-REF-205 to DF-REF-211) exist in the service's schema with their dictionary rows, and the guard library of DP-08 is published.
- RWB-P4-E1037-CON published the authorise contract this story answers behind: the request that carries a capability area, a right, a case reference and a field list, the answer that carries a decision code and a marker per field, and the contract fakes. This story adds the product code and the two version labels to that answer and no new path.
- The matrix version `PM-2026.11` is in force in `permission`, with the roles and letters of the FSD and TSD examples: for example RW-SECADM holds `CRUDA` in Platform administration, RW-AUDIT holds `R` in Platform administration, RW-COMPLY holds `R` in Rules and parameters, `RU` in Reference data and `R` in Platform administration, RW-CASEOWN holds `R` in Queue and allocation and `-` in Platform administration, and RW-LEGAL holds `CRUA` in Documents. The letters and the version label are data rows; the values named here are the ones the source examples carry.
- The masking version `MASK-SIT-01` is in force in `masking_rule`. The label is the one the FSD uses for the SIT environment, and the runtime label is set by the pack owner at load time; no source fixes a production label.
- The reference-data contract of `rwb-case` and its client library are live (DP-07), for LOV-CAPABILITY (the 14 capability areas), LOV-ROLE-CLASS (`BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR`), LOV-SCOPE (`OWN`, `TEAM`, `REGION`, `ALL`) and LOV-ROLE. No capability area, role class or scope value is written in code.
- The field catalogue exists in P1's dictionary: `sys_objects` and `sys_fields` hold the field IDs this policy keys on, for example `DF-ACE-059` (`date_of_birth`), `DF-ACE-073` (`id_no_masked`), `DF-ACE-074` (`id_no_last4`) and `DF-ACE-078` (`contact_value`). This story reads neither table and copies no dictionary row; the field ID is a value in this service's own policy rows.
- The owner of `data_product_access` presents the access resolution of a data-product read with the authorise request: the access version, the product code, the caller's role codes and the valid-from date that were resolved for that read. rwb-access neither reads that table nor holds a copy of it, and the field set of this input is Not specified in the source documents (GAP-0983; ASM-1724).
- The login is the rwb-access login (DP-02: one login per service). No credential is named in this story, and no grant is created here.
- The 30 `recovery.v_ace_*` views and their grants belong to RWB-P1-E1016-DB and RWB-P1-E1016-APP; this story creates, alters and grants nothing on them and asserts only that its own class names none of them.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. RW-SECADM, holding `CRUDA` in Platform administration (TSD P4 T6.1), calls `GET /api/recovery/access/v1/admin/roles`.
2. The controller resolves the caller's roles from the session and the Platform administration letter from `permission` at the matrix version in force. No `R` letter, or no role at all, is refused before any role is read (MSG-P4-002 and MSG-P4-001).
3. `RoleCatalogueService` reads `role` and `permission` in schema `rwb_access` and answers one entry per role with `roleCode`, `roleName`, `roleClass`, `defaultScope`, the role's permission rows (`capabilityArea`, `letters`), its masking exceptions and the `matrixVersion` in force.
4. The masking exceptions of a role are resolved from `masking_rule` at the masking version in force: the field IDs whose row for that role says `unmasked` true, and nothing else. Whether the catalogue carries this part at all is Not specified in the source documents (GAP-0983; ASM-1723).
5. RW-COMPLY or RW-SECADM calls `GET /api/recovery/access/v1/masking-policies` with a role and a field list. `MaskingPolicyService` answers one marker per field ID (`masked` or `clear`) and the `maskingVersion` in force. It returns no value, no rendering and no last four digits: the value is rwb-source-data's to return and the rendering is the screen owner's.
6. A caller — the records path of `rwb-source-data`, the gateway-bff composite route, or any service identity under the guard library — calls `POST /api/recovery/access/v1/authorise` with the capability area, the right, the product code, the case reference, the field IDs and the access resolution of the read (DP-08, DP-11).
7. `AuthoriseService` unions the letters of the caller's roles in the requested capability area. No role, or no letter for the area and the right, is refused with 403 and MSG-P4-002 before any field is answered (BR5).
8. `ScopeService` tests the case reference against the caller's default scope with the case attributes that arrive in the request. A case outside the scope is answered 404 with MSG-P4-003 and no field marker (BR6). No case table is read: the case is rwb-case's and its attributes arrive in the request.
9. `DataProductAnswerService` applies the data-product condition: the access resolution presented with the request must carry a row in force for one of the caller's roles and the product code, with a valid-from date not after the case's business date. An absent row, or a row not yet in force, answers refused and no field is answered clear (BR8, X4, X5).
10. `MaskingAnswerService` resolves the marker per field ID at the masking version in force: `clear` only where a row for a role the caller holds, that field ID and that version says `unmasked` true, and `masked` otherwise, including where no row exists (BR3, BR7).
11. The answer names `allowed` (or the decision code of the guard contract), the `matrixVersion`, the `maskingVersion` and one marker per field ID. It carries no value, no masked rendering and no last four digits (BR7, BR12).
12. Every read of this story runs against `role`, `permission` and `masking_rule` in schema `rwb_access` only. No `recovery.v_ace_*` view and no `public` table is named by any class of the package, and the build rule fails one that does (BR10, AC7).
13. This slice writes no access entry, publishes no event and consumes no event. The access entry of a data-product read is written by RWB-P4-E1039-APP through the decision-record library (DP-03), which is not a pattern of this story, and the policy-change event belongs to the load story.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The caller holds no Workbench role | 401 before any role, product or field is read | MSG-P4-001 | AC1 |
| X2 | The caller's roles hold no Platform administration `R` letter on `GET /admin/roles` | 403 and no role row is returned | MSG-P4-002 | AC1, AC2 |
| X3 | The caller's roles hold no letter for the requested capability area and right | 403 and no field is answered clear or refused-by-masking | MSG-P4-002 | AC2 |
| X4 | The access resolution presented with the request carries no row for the caller's roles and the product code | The answer is refused and no field is answered clear | None: the answer carries `allowed` false | AC6 |
| X5 | The access row exists with a valid-from date after the case's business date | The row is not in force, so the answer is refused until that date | None: the answer carries `allowed` false | AC6 |
| X6 | The case reference is outside the caller's default scope | 404 and no field marker is returned | MSG-P4-003 | AC8 |
| X7 | A requested field ID has no `masking_rule` row at the masking version in force | The field is answered `masked`; other fields are unaffected | None: the answer carries `masked` | AC3, AC4 |
| X8 | The product code, the capability area or the field ID is unknown to the reference lists | 422 naming the field; nothing is answered | MSG-GEN-001 | AC3 |
| X9 | A class of the package names `recovery.v_ace_*` or a `public` table, or the schema holds a foreign key to another service | The build or the migration fails and names the class or the constraint; nothing merges | Build log or SQLSTATE 42501 | AC7 |
| X10 | A masking row names a field ID at a version that is not in force | The row is ignored for the answer; the version in force decides | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_access` baseline and the RWB-P4-E1037-CON fake; the data products, the access rows, the dictionary and the views belong to the P1 stories and are not prerequisites of this build |
| Negotiable | Role codes, capability areas, letters, scope values, field IDs, masking rows and both version labels are data rows and reference data; the story fixes only the answer shape and the rules |
| Valuable | One service answers what a role may do, which field is masked for it and whether a data-product read is allowed, and a version change needs no deployment |
| Estimable | Three reads of the service's own tables, one catalogue query, one marker resolver, one data-product condition, one privilege test |
| Small | Fits one sprint with its tests, as a secondary slice of the legacy key; it creates no table and no migration |
| Testable | Every criterion in section 7 is one automated test with synthetic rows; no ACE data and no production data is needed |

### 7. Acceptance criteria

```gherkin
Feature: The role catalogue, the masking policy and the data-product authorise answer of rwb-access

  Background:
    Given the environment is SIT
    Given matrix version "PM-2026.11" is in force in "permission"
    Given masking version "MASK-SIT-01" is in force in "masking_rule"
    Given case "RW-2026-000102" has its business date 2026-11-20 and belongs to the default scope "ALL" of the caller unless the scenario says otherwise
    Given the field IDs of the policy are "DF-ACE-059", "DF-ACE-073", "DF-ACE-074" and "DF-ACE-078"

  Scenario: AC1 The role catalogue returns each role with its permissions, scope and version (new, D-RCV-60)
    Given the caller holds "RW-SECADM", whose Platform administration letters are "CRUDA" in "PM-2026.11"
    When the caller calls GET /api/recovery/access/v1/admin/roles
    Then the answer is 200 and holds one entry per role row in "rwb_access"
    And the entry for "RW-LEGAL" carries roleClass "BANK_USER", defaultScope "ALL" and its permission rows, including the letters "CRUA" in the capability area "DOCUMENTS"
    And the entry for "RW-CASEOWN" carries defaultScope "OWN" and the letters "R" in the capability area "QUEUE_AND_ALLOCATION"
    And every entry names matrixVersion "PM-2026.11"
    And the answer carries the masking exceptions of each role and names the masking version "MASK-SIT-01"

  Scenario: AC2 A permission row grants the area and no row refuses (new, D-RCV-60)
    Given the caller holds "RW-CASEOWN", whose "QUEUE_AND_ALLOCATION" letters are "R" in "PM-2026.11"
    When the caller asks POST /api/recovery/access/v1/authorise for area "QUEUE_AND_ALLOCATION", right "U", productCode "DP02" and caseId "RW-2026-000102"
    Then the answer is refused with status 403 and message MSG-P4-002
    And the answer names area "QUEUE_AND_ALLOCATION" and right "U"
    When the same caller asks for area "QUEUE_AND_ALLOCATION" and right "R"
    Then the answer carries allowed true
    When a caller holding only "RW-PHONECOL" calls GET /api/recovery/access/v1/admin/roles
    Then the call is refused with status 403 and message MSG-P4-002, because its Platform administration letters are "-"
    And no role row, no permission row and no masking exception is returned

  Scenario: AC3 The data-product answer names the mask marker per field (new, D-RCV-60)
    Given the caller holds "RW-AUDIT" with scope "ALL" and the case record letters "R"
    Given no "masking_rule" row at "MASK-SIT-01" gives "RW-AUDIT" an unmasked field
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", productCode "DP02" and caseId "RW-2026-000102" with field IDs "DF-ACE-059", "DF-ACE-073", "DF-ACE-074" and "DF-ACE-078"
    Then the answer carries allowed true, matrixVersion "PM-2026.11" and maskingVersion "MASK-SIT-01"
    And each field ID carries the marker "masked"
    And no field carries a value, a masked rendering or the last four digits of an identity number
    When the request names a field ID that no reference list holds
    Then the call is refused with status 422 and message MSG-GEN-001 naming the field

  Scenario: AC4 The masking version in force is named by the masking policy read (new, D-RCV-60)
    Given the "masking_rule" rows at "MASK-SIT-01" hold unmasked "true" for role "RW-COMPLY" and field "DF-ACE-074"
    And no row at that version covers field "DF-ACE-059" for any role
    When a caller holding "RW-COMPLY" calls GET /api/recovery/access/v1/masking-policies with role "RW-COMPLY" and field IDs "DF-ACE-059", "DF-ACE-073" and "DF-ACE-074"
    Then the answer names maskingVersion "MASK-SIT-01" and one marker per field ID
    And "DF-ACE-074" is "clear" and "DF-ACE-059" and "DF-ACE-073" are "masked"
    And the answer carries no value, no masked rendering and no identity number
    When a caller holding only "RW-CASEOWN" asks for the same field IDs
    Then "DF-ACE-074" is "masked" under the same version and no other row changes

  Scenario: AC5 A version change takes effect without a deployment (new, D-RCV-60)
    Given matrix version "PM-2026.12" is loaded with 756 rows and gives "RW-LEGAL" the letter "R" in "QUEUE_AND_ALLOCATION", and is otherwise equal to "PM-2026.11"
    Given its valid-from date is 2026-12-01 and it is approved
    When a caller holding "RW-LEGAL" asks POST /api/recovery/access/v1/authorise for area "QUEUE_AND_ALLOCATION", right "R" and productCode "DP02" on 1 December 2026
    Then the answer carries allowed true and names matrixVersion "PM-2026.12"
    And the same request on 30 November 2026 was refused with status 403 and MSG-P4-002 under "PM-2026.11"
    And GET /api/recovery/access/v1/admin/roles names matrixVersion "PM-2026.12"
    And no deployment, no restart and no code change takes place
    And the rows of "PM-2026.11" stay readable with their valid-to date

  Scenario: AC6 An access row absent or not yet in force is refused (new, D-RCV-60)
    Given access version "DPA-2026.11" holds no row for role "RW-PHONECOL" and product "DP06"
    When a caller holding "RW-PHONECOL" asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", productCode "DP06" and caseId "RW-2026-000102"
    Then the answer carries allowed false and no field is answered clear
    Given access version "DPA-2026.12" gives "RW-PHONECOL" read on "DP06" from 2026-12-15 and today is 2026-12-14
    When the same caller asks for the same read with the access resolution of "DPA-2026.12"
    Then the answer carries allowed false, because the row is not yet in force
    And no access row is read from "data_product_access", which is P1's table
    And when the same read is presented on 2026-12-15 the answer carries allowed true, with the masking markers of the fields asked

  Scenario: AC7 No ACE view read, no public read and no foreign key (new, D-RCV-60)
    Given the rwb-access login and the 30 "recovery.v_ace_*" views of schema "recovery"
    When a class of `th.co.scb.ace.workbench.recovery.access.catalogue` names "recovery.v_ace_customer"
    Then the build fails and names the class and the object
    When a session as the rwb-access login selects from "recovery.v_ace_customer"
    Then the statement fails with SQLSTATE 42501
    When a session as the rwb-access login selects from "public.customer"
    Then the statement fails with SQLSTATE 42501
    When the migration of "rwb_access" is inspected
    Then no foreign key of "role", "permission" or "masking_rule" references a table outside schema "rwb_access"
    And every read of this story names only "role", "permission" and "masking_rule" in "rwb_access"
    And the 30 views, their definitions and their grants are P1's and are not created, altered or granted here

  Scenario: AC8 A case outside the caller's scope answers 404 (new, D-RCV-60)
    Given the caller holds "RW-CASEOWN" with default scope "OWN" and owns case "RW-2026-000102"
    And case "RW-2026-000456" belongs to team "MTG-NE" and another owner
    When the caller asks POST /api/recovery/access/v1/authorise for area "CASE_RECORD", right "R", productCode "DP02" and caseId "RW-2026-000456"
    Then the call is refused with status 404 and message MSG-P4-003
    And no allowed flag, no matrix version, no masking version and no field marker is returned
    When the same caller asks for case "RW-2026-000102"
    Then the answer is 200 with the markers of the fields asked
```

The eight criteria are new and test only this deliverable: the role catalogue, the masking policy read and the data-product half of the authorise answer. The legacy criteria of RWB-E1-016 are owned elsewhere: AC1, AC3 to AC11 by RWB-P1-E1016-APP (the access rows, the masking of a record read, the scope test on the records path, the PII log, the view grants and the catalog entries), AC2 by RWB-ITG-E1016-ITG on the composed entry, and the retention class of an entry by RWB-P5-E1016-APP. No legacy criterion text is copied into this story.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The role list, the permission rows and the masking rows are data with a version: a new role, a new letter or a new masking exception is a row, and no role code, capability area, letter, scope value or field ID is written in Java | FSD P4 A2.3 and A2.4; BR-P4-003, BR-P4-004, BR-P4-030; TSD P4 T3.1 |
| BR2 | The role catalogue answers each role with its permission rows per capability area, its role class, its default scope, its masking exceptions and the matrix version in force; the P4 catalogue entries of the legacy story are these rows and nothing else | FSD P4 A2.3 and A2.30; TSD P4 T3.1 (`role`, `permission`); Arch v5 slide 41 |
| BR3 | A field is `clear` only where a `masking_rule` row for a role the caller holds, that field ID and the masking version in force says `unmasked` true; the union of the caller's roles applies and every other case is `masked` | FSD P4 A2.5; TSD P4 T3.1 (`masking_rule`); NFR-039 |
| BR4 | `GET /admin/roles` needs the Platform administration `R` letter; a caller without it is refused before any role is read, and the refusal names the area and the right | API-P4-007; TSD P4 T6.1; FSD P4 AC-ALT-P4-001-01 |
| BR5 | Default deny: no role, no permission row for the area, or no letter for the right answers refused, never allowed. A missing row never opens an area | FSD P4 VR-P4-004-1 and VR-P4-005-1; MSG-P4-001, MSG-P4-002; CTL-09 |
| BR6 | A case outside the caller's scope is answered 404 and returns no field marker; the case attributes arrive in the request and no case table is read | CTL-09; FSD P4 AC-EXC-P4-004-01; MSG-P4-003 |
| BR7 | The data-product answer carries allowed or refused, the matrix version, the masking version and a marker per field ID; it never carries a value, a masked rendering or the last four digits of a field | FSD P4 A2.5; NFR-039; NFR-040 |
| BR8 | The data-product answer is allowed only where the access resolution presented with the request carries a row in force for one of the caller's roles and the product code; an absent row or a row not yet in force answers refused. The row itself is P1's `data_product_access` and is never read here | Legacy RWB-E1-016 BR1 and AC8; FSD P4 A2.30; Ownership Map (`data_product_access` P1) |
| BR9 | An access or matrix load with an exception is refused whole and the version in force stays in force; a version is never edited in place, and a change is a new version with a later valid-from date | Legacy RWB-E1-016 BR6; FSD P4 AC-EXC-P4-004-02; TSD P4 T3.2 (LOV-VERSION-STATUS) |
| BR10 | rwb-access reads no ACE table, no `recovery.v_ace_*` view and no other service's schema, and holds no foreign key across a schema; a class that names a view or a `public` table fails the build | Arch v5 slides 8, 9 and 41; DP-01; DP-05; legacy RWB-E1-016 BR8 |
| BR11 | A field ID is a key into this service's own policy; the dictionary (`sys_objects`, `sys_fields`) and the field metadata are P1's, are read through its contract and are never copied into `rwb_access` | Ownership Map (`sys_objects`, `sys_fields` P1); TSD P4 T3.1 (`masking_rule.field_id`) |
| BR12 | A masking version or a matrix version takes effect by its valid-from date, with no deployment and no code change; the previous rows stay readable with their valid-to date | REQ-ACA-002; REQ-ACA-003; FSD P4 AC-P4-004-01; TSD P4 T3.2 |
| BR13 | This slice writes no access entry and publishes no event: the entry of a data-product read is the access-log story's through the decision-record library, and the policy-change event is the load story's | Arch v5 slide 14 (P4 events: AccessPolicyChanged, DoaLimitChanged); DP-03 and DP-09 not applied here |
| BR14 | The reference lists (LOV-CAPABILITY, LOV-ROLE-CLASS, LOV-SCOPE, LOV-ROLE) are read with the version in force; `lov_value` is reference data of P3 under the ownership ruling and is not a table of this service | TSD P4 T3.2; DP-07; ownership ruling ASM-0071 |
| BR15 | The reference-loads and list endpoints of the administration surface (`/admin/reference-loads*`, `/admin/lists/{listCode}`) are P3's; this story neither serves nor changes them | Ownership ruling ASM-0041; API-P4-004 to API-P4-006 |

### 9. State transitions

This service holds no case, task or approval state. The states it answers are the outcome of a permission test, a scope test, a data-product test and a masking test, and the lifecycle of a matrix version and a masking version, which the load path and the pack owner write.

| From | Event | Condition | To |
|---|---|---|---|
| Version in force | A request for a capability area and a right | A permission row of one of the caller's roles carries the letter | Area answered as granted |
| Version in force | A request for a capability area and a right | No permission row carries the letter, or the caller holds no role | Area answered as refused; 403 and MSG-P4-002 |
| Version in force | A data-product request | The access resolution presented carries a row in force | Data-product condition satisfied; the masking markers decide the field answer |
| Version in force | A data-product request | The row is absent or its valid-from date is after the case's business date | Data-product condition refused; no field answered clear |
| Version in force | A field list | A covering row says `unmasked` true for a role the caller holds | Field answered `clear` |
| Version in force | A field list | No covering row, or `unmasked` false | Field answered `masked` |
| A matrix or masking version in force | A new version is loaded, approved and dated | The valid-from date is reached, with no deployment | The new version answers every read from that date; the older rows stay readable for their own dates |
| A load refused whole | The load path reports a check failure | Any row of the load fails a check | The previous version stays in force and no row of the refused load is stored |

The version lifecycle of a matrix version and of a masking version is TSD P4 T3.2 (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED); this story reads the version in force and writes no row of it. The load and approval themselves are the load path's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-SECADM, security administrator | Calls `GET /admin/roles` (Platform administration `CRUDA`, TSD P4 T6.1); owns the matrix rows through the load path, not here |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY, RW-PLATADM | Call `GET /admin/roles` (Platform administration `R`); read the catalogue and the versions in force |
| RW-COMPLY, Compliance and PDPA officer | Calls `GET /masking-policies` and reads which field IDs the masking version opens for a role; owns the pack content through the load path, not here |
| Every business role with the right in the area, for example RW-CASEOWN in Queue and allocation and RW-AUDIT in Case record | Receives the allowed or refused answer and the marker of a field it is entitled to ask about; may not change a row, a version or an exception |
| Service identities of the other services and of the gateway-bff composite route | Call `POST /authorise` under the guard library of DP-08 with their own cached permission read |
| `rwb-access` itself | Reads `role`, `permission` and `masking_rule` in its own schema and writes no row of them in this story |
| RW-REFADM, reference data administrator, and the load path | Prepare and approve matrix and masking versions; they use the reference-loads surface, which is P3's under ASM-0041 |
| ACE view owner and ACE DBA | Not this story: the views, the field dictionary and the grants stay with RWB-P1-E1016-APP, RWB-P1-E1016-DB and RWB-ACE-001 |
| No approval level from the delegation of authority applies | The story takes no business decision; the DoA answer is RWB-P4-E2013-APP's |

The refusal shape is 403 with an RFC 9457 problem response, `messageId` set to MSG-P4-002, and the area and right named in the detail. The database login is the per-service login of the baseline (DP-02), and this story names no credential.

### 11. Data

| BR Field ID | Table in `rwb_access` | Field | Read or write |
|---|---|---|---|
| DF-REF-034 | `role` | id | Read |
| DF-REF-035 | `role` | role_code | Read |
| DF-REF-036 | `role` | role_name | Read |
| DF-REF-037 | `role` | role_class | Read |
| DF-REF-038 | `role` | default_scope | Read |
| DF-REF-039 | `role` | entra_group | Read; no Entra group is written by this story |
| DF-REF-040 | `permission` | id | Read |
| DF-REF-041 | `permission` | role_id | Read |
| DF-REF-042 | `permission` | capability_area | Read |
| DF-REF-043 | `permission` | letters | Read |
| DF-REF-044 | `permission` | matrix_version | Read |
| DF-REF-198 | `masking_rule` | id | Read |
| DF-REF-199 | `masking_rule` | role_code | Read |
| DF-REF-200 | `masking_rule` | field_id | Read |
| DF-REF-201 | `masking_rule` | unmasked | Read |
| DF-REF-202 | `masking_rule` | masking_version | Read |
| DF-REF-203 | `masking_rule` | valid_from | Read |
| DF-REF-204 | `masking_rule` | valid_to | Read |
| DF-REF-205 to DF-REF-211 | `role_conflict` | role_code, conflicts_with, conflict_version | Not read by this story; the sign-in conflict check is the session story's |
| DF-REF-159 to DF-REF-184 | `reference_version`, `reference_row` of `rwb-case` | LOV-CAPABILITY, LOV-ROLE-CLASS, LOV-SCOPE and LOV-ROLE with their versions in force | Read through the reference-data contract (DP-07); no row is copied |
| DF-ACE-059, DF-ACE-073, DF-ACE-074, DF-ACE-078 | `v_ace_customer` (named as field IDs only, never read) | `date_of_birth`, `id_no_masked`, `id_no_last4`, `contact_value` | Not read and not written; the field IDs are keys of this service's policy rows, used here as the test data of the marker |
| DF-REF-071 to DF-REF-086 and DF-REF-088 to DF-REF-105 | `data_product`, `data_product_access`, `sys_objects`, `sys_fields` | the 14 catalog entries and the field dictionary | Not read and not written: P1's, reached through its contract only (BR11) |

This story writes no row of any table: it is a read slice of the service's own policy. No row of `data_product`, `data_product_access`, `data_product_load`, `sys_objects`, `sys_fields`, `retention_rule` or `delegation_limit` is read, written or defined here, and no `recovery.v_ace_*` view is read. The field ID is a value in `masking_rule`, with no foreign key across a schema. Field IDs are those in the Logical Data Model and Data Dictionary v8; `lov_value` and the reference tables are P3's under the ownership ruling and arrive through DP-07.

### 12. Contract

#### 12.1 REST operations provided

All three sit on base `/api/recovery/access/v1` of DP-13. This slice adds no other path, no other query parameter and no other response field.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/admin/roles` | The role catalogue: each role with its permission rows, default scope, role class, masking exceptions and the matrix version in force | Platform administration `R`, scope applied; API-P4-007 | Not applicable, read only |
| GET | `/masking-policies` | The masking policy in force for a role and a field list: one mask marker per field ID and the masking version | Any authenticated caller with a Workbench role; own roles only | Not applicable, read only |
| POST | `/authorise` | The data-product half of the authorise answer: allowed or refused for an area, a right, a product code, a case and a field list, with the matrix version, the masking version and a marker per field ID | Any authenticated caller with a Workbench role, or a service identity | Idempotent by identity, area, right, product code, case reference and field list within the cache window |

Request and answer shapes, as this story fixes them:

- `/admin/roles`: request has no parameter beyond the session. Answer: `roleCode`, `roleName`, `roleClass`, `defaultScope`, `permissions` (a list of `capabilityArea` and `letters`), `maskingExceptions` (a list of `fieldId`), `matrixVersion`, `maskingVersion`.
- `/masking-policies`: query `role` and `fieldIds`. Answer: `maskingVersion` and a list of `fieldId` and `marker`, where the marker is `masked` or `clear`.
- `/authorise`: request has the capability area, the right, `productCode`, `caseId`, `fieldIds` and the access resolution of the read (access version, role codes, valid-from date). Answer: `allowed`, `matrixVersion`, `maskingVersion` and a list of `fieldId` and `marker`.

The request and answer field names above, the marker vocabulary and the `maskingExceptions` part are Not specified in the source documents (GAP-0983; ASM-1722). The access resolution the request carries is the resolution of `data_product_access`, which is P1's table, and its field set is Not specified in the source documents (GAP-0983; ASM-1724).

Errors: 401 no Workbench role (MSG-P4-001); 403 no Platform administration `R` on the catalogue, or no letter for the area and right on the authorise answer (MSG-P4-002); 404 case absent or outside the caller's scope (MSG-P4-003); 422 a required or unknown query field (MSG-GEN-001); 503 the reference lists are unavailable.

`POST /authorise` and `/masking-policies` are named on the inbound surface of `rwb-access` in Architecture v5 slide 14; `/admin/roles` is API-P4-007 of TSD P4 appendix T-A. The session read `/me/session`, the permissions read `/me/permissions`, the delegation lookup `/doa-limits`, the access-log search and the reference-loads surface are other stories' (RWB-P4-E1022-APP, RWB-P4-E2013-APP, RWB-P4-E1039-APP and the P3 reference-loads contract under ASM-0041); this story adds none of them.

#### 12.2 REST operations consumed

None. At run time rwb-access calls no service: the caller's identity arrives in the session, the case attributes for the scope test and the access resolution of the read arrive in the request, and the reference lists reach it through the cached client library of `rwb-case` (DP-07). The one-hop and 2 s budget of DP-11 apply to the inbound call, and to the screen path that reads the catalogue through the gateway-bff composite route.

#### 12.3 Events published

None. DP-09 is not a pattern of this story, so this slice holds no outbox row, adds no topic and publishes no event. `rwb.access.AccessPolicyChanged.v1` is the load story's: a matrix version, a permission row or a masking version is loaded, approved and rolled back by the load path, and that is where the change is announced. The access entry of a data-product read is the access-log story's, written through the decision-record library of DP-03, which this story does not apply.

#### 12.4 Events consumed

None. The matrix version and the masking version in force are read from `rwb_access` on each call; no topic is consumed here, and rwb-access is a reference-data owner with no inbound event on Architecture v5 slide 14.

#### 12.5 Workflows and activities

None. All three answers are synchronous REST answers in the caller's thread. The six-monthly access review list (JOB-18) is a Schedule of this service and belongs to RWB-P4-AD008-APP (Architecture v5 slide 44); this story starts no workflow and registers no activity on the `rwb-access` queue.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job sits in this story.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `role` | P4 (`rwb_access`) | Read only: the role catalogue entry and the caller's roles |
| `permission` | P4 (`rwb_access`) | Read only: the letters of a capability area and the matrix version |
| `masking_rule` | P4 (`rwb_access`) | Read only: the `unmasked` exceptions and the masking version |
| `role_conflict` | P4 (`rwb_access`) | Not read here; the conflict check belongs to the session story |
| `delegation_limit` | P4 (`rwb_access`) | Not read here; the DoA lookup is RWB-P4-E2013-APP's |

No table, no view and no foreign key of another schema is used (DP-01). `data_product`, `data_product_access`, `data_product_load`, `sys_objects` and `sys_fields` are P1's and are not read; `retention_rule` is P5's; `lov_value` and the reference tables are P3's and arrive through DP-07 (ASM-0071); `rule_package*` is P7's; `queue` and `queue_member` are P3's. This story uses no outbox, inbox or idempotency object, because DP-09 is not applied.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| RWB-P4-E1037-CON fake | The authorise contract | A granted area, a refused area, a case out of scope and a field with no masking row, each with its answer shape |
| matrix fixture | The `role` and `permission` rows | Matrix version `PM-2026.11` with the roles and letters of the source examples, and `PM-2026.12` for AC5 |
| masking fixture | The `masking_rule` rows | Masking version `MASK-SIT-01` with one unmasked row for RW-COMPLY and `DF-ACE-074`, and no row for `DF-ACE-059` |
| reference-data fake | RWB-P3-E1043-CON (DP-07) | LOV-CAPABILITY, LOV-ROLE-CLASS, LOV-SCOPE and LOV-ROLE with their versions |
| access-resolution fixture | The request value of a data-product read | Access versions `DPA-2026.11` and `DPA-2026.12`, product codes `DP02` and `DP06`, and the two valid-from dates of AC6; a request value, not a service contract |

The request and answer field names of the three operations are stubbed from the fixture this story fixes, and their list is Not specified in the source documents (GAP-0983; ASM-1722).

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 3 (`GET /admin/roles`, `GET /masking-policies` and the data-product part of `POST /authorise`); consumed 0 | Base `/api/recovery/access/v1` |
| Kafka | Published 0; consumed 0 | DP-09 is not applied; the policy-change event is the load story's |
| Temporal | 0 workflows, 0 activities | JOB-18 is RWB-P4-AD008-APP's |
| File | None | No file input or output; matrix and masking versions arrive by load, not in this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.access.catalogue`, module `catalogue`, in the service root `th.co.scb.ace.workbench.recovery.access`. The read-only repositories stay in the same module as the answers they serve.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-02 | `recovery_svc` login | One login per service | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The legacy markers this slice replaces are the in-process read of the role to permission matrix and of the masking rules inside the data engine (DP-11: one REST contract with a mock, one hop and a 2 s timeout), the `RecoveryAccessGuard` capability check on the data-product read (DP-08: this service's own authorise contract) and the single recovery schema read of `role`, `permission` and `masking_rule` (DP-01: this service's `rwb_access`). DP-05 applies as a prohibition for this service: it holds no ACE view and reads none, and the field IDs of its policy are keys, not data. DP-07 arrives through the cached client library, and DP-19 is the route behind SCR-43 and SCR-47, which this story does not build.

This is a secondary slice and it adds no H dependency of its own. The metadata rows "Depends on (build)", "Contract dependencies", "Integration dependencies" and "External dependencies" stay exactly as this Work Package fixes them: the libraries, the per-service Flyway baseline, the guard library and the gateway route are already build dependencies of the P4 service's own stories, in particular RWB-P4-E1037-CON and RWB-P4-E1037-APP, and this story builds against the published contract and its fake. No H dependency, no C dependency and no X dependency is created here.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `RoleCatalogueController` | Controller | `GET /admin/roles`: the Platform administration `R` check, query validation and the error mapping to RFC 9457 problem responses |
| `RoleCatalogueService` | Service | One entry per role with its permission rows, role class, default scope, masking exceptions and the matrix version in force |
| `MaskingPolicyController` | Controller | `GET /masking-policies`: the role and field-list validation and the answer shape |
| `MaskingPolicyService` | Service | The mask marker per field ID at the masking version in force and the version label |
| `AuthoriseDataProductPart` | Service | The data-product condition of the authorise answer: the access resolution presented, the matrix version and the markers |
| `PermissionReader` | Service | The `role` and `permission` rows of the caller and of the requested area, in the matrix version in force |
| `MaskingReader` | Service | The `masking_rule` rows by `role_code`, `field_id` and `masking_version`; no row means `masked` |
| `ScopeService` | Service | The default-scope test of the case reference with the attributes that arrive in the request |
| `CatalogueRepository` | Repository | Read-only queries over `role`, `permission` and `masking_rule` in schema `rwb_access`; no write method |
| `ReferenceLists` | Service | LOV-CAPABILITY, LOV-ROLE-CLASS, LOV-SCOPE and LOV-ROLE through the reference-data contract of DP-07; no Java enum of areas, classes or scopes |

**Database and migrations**

- This story creates no table and owns no Flyway version of its own. `role`, `permission`, `masking_rule` and `role_conflict` are created, indexed and loaded by RWB-P4-E1037-APP and the load path in the per-service sequence of DP-15, and this story reads them through its repository.
- No write statement exists in the repository: it exposes no save, update or delete, so a catalogue read, a masking read and an authorise answer can never change a policy row.
- If the SIT query plan needs an index that the creating story does not hold, the index is added to that story's migration, not to a new one here. The read predicates are the version columns (`matrix_version`, `masking_version`), `role_code`, `capability_area` and `field_id`.
- No `v_ace_*` object and no `public` object is created, altered or granted: the views, their definitions and their grants belong to RWB-P1-E1016-APP and RWB-P1-E1016-DB.

**Configuration and reference data**

- The matrix version in force and the masking version in force are read from the two version columns; the SIT versions are `PM-2026.11` and `MASK-SIT-01`, the labels the source examples carry. No production label is fixed by this story.
- LOV-CAPABILITY (14 areas), LOV-ROLE-CLASS (`BANK_USER`, `PARTNER_USER`, `NON_HUMAN_ACTOR`), LOV-SCOPE (`OWN`, `TEAM`, `REGION`, `ALL`) and LOV-ROLE are read through the reference-data contract of DP-07 with the version in force; no area, class, scope or role code is a constant in code.
- The role, permission and masking rows themselves are data of this service, prepared by the matrix owner and the pack owner and approved on the load path; this story neither prepares nor approves a version.
- The login is the rwb-access login (DP-02). No credential is named and no grant is created in this story.

**Build steps**

1. `CatalogueRepository` with the read-only queries over `role`, `permission` and `masking_rule`, and a test that the repository has no write method.
2. `RoleCatalogueService` and `GET /admin/roles`, with the Platform administration `R` check ordered before any role read; tests for AC1 and the refusal half of AC2.
3. `PermissionReader` and the union of the letters of a capability area, with the default-deny path of a missing row and a missing role; tests for AC2.
4. `MaskingPolicyService` and `GET /masking-policies`, with the `unmasked` true rule and the no-row default; tests for AC4.
5. `AuthoriseDataProductPart` behind the existing authorise path: the product code, the access resolution presented, the absent row and the not-yet-in-force row; tests for AC3 and AC6.
6. `ScopeService` with the default scope and the 404 of a case outside it; tests for AC8.
7. The version tests on a fixed clock: `PM-2026.12` in force from 2026-12-01 answers with no deployment and the older rows stay readable; tests for AC5.
8. The service's own login test: no privilege on any of the 30 views and none in `public`, and no foreign key across a schema; tests for AC7. The proof across all 19 logins is RWB-ITG-E1069-ITG's and is not repeated here.
9. A contract-fake run of the three answers, so the story builds before the load path and the records path are live.

**Feature switch.** None of its own. The service-level flag of RWB-P4-E1037-CON governs the baseline, and a matrix or masking version is released and rolled back as data by the load path, never by a flag; this story always answers the version in force.

**Done when.** The tests in section 16 pass; `GET /admin/roles` returns every role with its permission rows, default scope, role class, masking exceptions and the matrix version in force; `GET /masking-policies` returns a marker per field ID and the masking version; the authorise answer names allowed or refused, both versions and a marker per field for a data-product read; a matrix version dated 2026-12-01 answers with no deployment; a case outside the scope answers 404; and the build is green on the read of the service's own tables and the login holds no privilege on any `recovery.v_ace_*` view and none in `public`.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P4-001 | The token holds no Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. | This story, on all three operations |
| MSG-P4-002 | No Platform administration `R` on the catalogue, or no letter for the requested area and right | You cannot {action} here. Your role does not include it. | This story, on the catalogue and on the authorise answer |
| MSG-P4-003 | The case reference is outside the caller's scope | This case is not in your scope. | This story, on the authorise answer |
| MSG-GEN-001 | A required query field is empty, or a product code, capability area or field ID is not in its list | Enter {field}. | This story, on all three operations |
| Build log | A class of the package names a `v_ace_*` view or a `public` table | The boundary rule fails and names the class and the object | The service's build |

No new message ID is created by this story. For MSG-P4-002 the {action} names the action the caller tried — for example "read roles" or "read a data product" — and never a case fact or a field value. The 403 of an absent letter is the only refusal that carries a `messageId` other than MSG-P4-001; a refused data-product answer and a masked field are answer values, not messages. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built by this story. The answers it serves are the ones SCR-43 Roles and access (roles, permissions, scope and the group mapping) and SCR-47 Personal data (masking rules and versions) display; both are E8 screens and both are served, before E8, by the gateway-bff composite route of DP-19 with a read of this service and a read of the field values from rwb-source-data, one hop each. The catalogue and the masking policy are also read directly as APIs by the auditors and by the other services' guards.

| Screen | State | Where it is |
|---|---|---|
| SCR-43 Roles and access | Loading, list, empty; refusal state with MSG-P4-002 | E8; the route reads `GET /admin/roles` |
| SCR-47 Personal data | Loading, list, empty; the masking version in force | E8; the route reads `GET /masking-policies` |

The screen fields and the field-level rendering of the composite route are Not specified in the source documents (GAP-0983; ASM-1722). This story returns a marker and a version and never a rendering: the masked rendering of a field belongs to the screen owner, and the value belongs to rwb-source-data.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-016-01 | AC3, BR3, BR7 | End to end | RW-AUDIT with scope ALL; case RW-2026-000102; product DP02; field IDs `DF-ACE-059`, `DF-ACE-073`, `DF-ACE-074` and `DF-ACE-078`; masking version MASK-SIT-01; the masked records read and the PII log are P1's |
| TC-E1-016-02 | AC1, BR2 | End to end | The DP01 catalog entry and its views are P1's; the owner role and the masking exceptions of the entry are resolved here from the role catalogue under PM-2026.11 |
| TC-E1-016-03 | AC6, BR8 | Component | RW-PHONECOL; product DP06; no access row in DPA-2026.11 |
| TC-E1-016-04 | AC5, BR9 | Contract | Matrix version PM-2026.12 loaded with 756 rows and approved for 2026-12-01; the refused load of the same fixture carries the check failure and leaves PM-2026.11 in force |
| TC-E1-016-05 | AC8, BR6 | Component | RW-CASEOWN with scope OWN; case RW-2026-000456 on team MTG-NE |
| TC-E1-016-06 | AC3, AC4, BR3 | Component | RW-COMPLY; no masking row for `DF-ACE-059`; one unmasked row for `DF-ACE-074` |
| TC-E1-016-07 | BR7 | Contract | PII access log stub rejecting writes; the entry itself is the access-log story's and this answer carries only markers and versions |
| TC-E1-016-08 | AC6, BR8 | Component | Access version DPA-2026.12 gives RW-PHONECOL read on DP06 from 2026-12-15; test clock 2026-12-14 |
| TC-E1-016-09 | AC2, BR4, BR5 | Component | RW-TRIBE and RW-PHONECOL call `GET /admin/roles`; refused with MSG-P4-002; the catalog call of the legacy case is P1's |
| TC-E1-016-10 | AC7, BR10 | Component | The rwb-access login; SELECT on `recovery.v_ace_customer` and on `public.customer`, both refused with SQLSTATE 42501; the 30 view names and their grants are P1's |
| TC-E1-016-11 | BR2 | End to end | 30 views, 122 objects and 1,366 fields: the catalog content is P1's; this story contributes the role rows and the masking exceptions it resolves |
| TC-E1-016-12 | BR2 | End to end | Catalog load setting `v_ace_customer` to Workbench: the refusal is P1's; this story contributes the role catalogue entry the load does not touch |

Every legacy test case of this key is listed above with the slice of the behaviour this story answers. TC-E1-016-01 answers the authorised data-product read through RWB-P1-E1016-APP, and here the markers and both versions of the answer; TC-E1-016-02 answers the DP01 catalog entry through RWB-P1-E1016-APP and RWB-ITG-E1016-ITG, and here the owner role and the masking exceptions resolved from the catalogue; TC-E1-016-03, TC-E1-016-06 and TC-E1-016-08 answer the access row, the masking rule and the not-yet-in-force row at the P4 answer; TC-E1-016-04 answers the load refusal on the load path (P3's reference-loads surface under ASM-0041) and the version change here; TC-E1-016-05 answers the scope test; TC-E1-016-07 answers the PII log path through P1's records read; TC-E1-016-09 answers the refusal shape of a role without the right, which is this service's answer, while the catalog call it names is P1's; TC-E1-016-10 answers the grant model through RWB-P1-E1016-DB, and here the two facts about this service's own login; and TC-E1-016-11 and TC-E1-016-12 answer the catalog content and its load through P1. The `-ITG` copies belong to RWB-ITG-E1016-ITG. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the legacy test case ID.

### 17. Guardrails

- No business value in code: the roles, capability areas, letters, scope values, role classes, field IDs, masking rows and both version labels are data rows read with the version in force. No role code, area, letter, scope value or field-ID list appears in Java, and the reference lists arrive through DP-07.
- No personal data in answers, logs, workflow inputs, tests or prompts: an answer carries a marker, a version and field IDs only; the test field IDs are named, never rendered, and every test row is synthetic.
- The clear identity number never leaves ACE: the customer view returns `id_no_masked` (`DF-ACE-073`) and `id_no_last4` (`DF-ACE-074`), this service never reads them and no masking row of this policy opens them.
- ACE data only through the owner's contract or `v_ace_*` views — and this service reads neither: a class that names a view fails the build, and the pointer to a value is rwb-source-data's contract.
- No cross-schema read and no cross-schema key: `rwb_access` holds no foreign key into another schema and no copy of a case, product, catalog or ACE row (DP-01). The dictionary, the access rows and the views stay with P1.
- A missing role, a missing permission row, a missing access row and a missing masking row all resolve to refused or `masked`, never to allowed and never to `clear`.
- No event and no access entry is produced here: the entry of a data-product read is the access-log story's through the decision-record library, and the policy-change event is the load story's.
- An applied version is never edited; a change is a new matrix or masking version with a later valid-from date, and the load path is the only writer.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access to each data product is controlled per role through the read-only views, and personal data is masked by role in line with PDPA — here, the masking policy and the per-field marker of a data-product read | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ACA-05 | All recovery processes | CTL-09, CTL-11; BR-P4-005; NFR-039; NFR-040; BR3, BR7, BR8 | TC-E1-016-01, TC-E1-016-03, TC-E1-016-06, TC-E1-016-08 |
| REQ-RDF-011 | Every data product has a catalog entry stating its definition, owner, system of record, refresh cycle and retention — here, the owner role, the role class, the default scope and the masking exceptions the entry names | Business Requirements Epic 1, sections 3.1 and 4 | FEAT-ACA-03; FEAT-ACA-04 | All recovery processes | BR-P4-003; BR-P4-004; BR-P4-030; BR1, BR2 | TC-E1-016-02, TC-E1-016-09, TC-E1-016-11, TC-E1-016-12 |
| REQ-ACA-006 | Every read of the case store, the document store and the data lake copy is written to the access log — here, the answer returns the field IDs and the markers that the access entry of a data-product read names; the entry itself is RWB-P4-E1039-APP's | Business Requirements Epic 1, section 4 | FEAT-ACA-07; FEAT-ACA-08 | All recovery processes | BR13; DP-03 (not applied here) | TC-E1-016-01, TC-E1-016-07 |

The supporting features of this slice are FEAT-ACA-03 (roles as data), FEAT-ACA-04 (the role to permission matrix as data) and FEAT-ACA-05 (mask PDPA fields by role), which the FSD P4 module pairs with RWB-E1-037; this slice answers them for the catalogue, the masking policy and the data-product answer and changes neither the matrix load design nor the access-log design. The legacy story is RWB-E1-016, disposition Split (rework); its other slices are RWB-P1-E1016-APP, RWB-P1-E1016-CON, RWB-P1-E1016-DB, RWB-P5-E1016-APP and RWB-ITG-E1016-ITG.

### 19. Out of scope

- The `data_product`, `data_product_access`, `data_product_load`, `sys_objects` and `sys_fields` rows, the 14 catalog entries, the 30 `recovery.v_ace_*` views and their grants: RWB-P1-E1016-APP, RWB-P1-E1016-CON and RWB-P1-E1016-DB. They are neither read nor defined here.
- The composed catalog entry a data steward reads, and the end-to-end proof across the owners: RWB-ITG-E1016-ITG. The retention class of an entry: RWB-P5-E1016-APP.
- The read of a data-product record and the masked rendering of its personal fields: rwb-source-data (RWB-P1-E1016-APP) and gateway-bff (DP-19).
- The matrix and masking versions as loads: the reference-loads surface is P3's (`/admin/reference-loads*`, `/admin/lists/{listCode}`; ASM-0041) and the approval path is RWB-P4-AD010-APP; the masking pack content and its roster are the pack owner's under DL26.
- The session and permissions reads (`/me/session`, `/me/permissions`) and the role conflict check: RWB-P4-E1022-APP and RWB-P4-E1037-APP.
- The delegation of authority lookup and the approver-authority answer: RWB-P4-E2013-APP. The rules and parameters administration: P7 rwb-decision (`rule_package*`, ASM-0069).
- The access-log search, the access entry of a read and break-glass: RWB-P4-E1039-APP and RWB-P4-AD007-APP.
- The six-monthly access review list (JOB-18): RWB-P4-AD008-APP. The E8 administration screens SCR-43 and SCR-47: their E8 stories, with the route served by gateway-bff.
- The `rwb_access` schema baseline, the login, the topic and queue provisioning, the dashboards and the runbook of this service.
