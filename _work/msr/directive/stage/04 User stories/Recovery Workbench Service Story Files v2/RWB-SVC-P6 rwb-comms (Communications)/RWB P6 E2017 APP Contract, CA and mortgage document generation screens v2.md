# RWB-P6-E2017-APP Contract, CA and mortgage document generation screens

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2017-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-017 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Set by the squad at refinement |
| Patterns applied | DP01, DP03, DP07, DP11, DP13, DP19 |
| Parallel lane | L-P6-M |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P5-E2017-CON, RWB-P6-E2017-CON (contract story not yet issued) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-001, FR-P6-002, FR-P6-003, FR-P6-004, FR-P6-005, FR-P6-012, FR-P6-014, FR-P6-032, FR-P6-033, FR-P6-034) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the rwb-comms slice of legacy RWB-E2-017 is split out. It keeps the template catalog with its versions and Legal approval, the merge field catalog with its locked attribute and the signature basis behind the two screens, on base `/api/recovery/comms/v1`, and it wires the screens through gateway-bff; the documents, the file, the write-once copy, the send transaction and the ledger entries stay with their owners. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P6-E2017-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 20 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the document set of a deed in lieu treatment, and the merge fields of each document, to come from the template catalog with the version Legal approved and the fields the catalog marks locked**, so that **the screens show the set and the values in force and no officer re-keys a contract, a credit approval or a mortgage document from a Word file**.

rwb-comms owns `template` and `merge_field`, so it serves the four answers the screens cannot take elsewhere: the set of a treatment type and product group with the version in force (SCR-14); the Legal approval of that version and the withdrawal that ends it; the merge fields of a version with their required, personal-data and locked attributes (SCR-30); and the signature basis, `E_SIGNATURE_ALLOWED` or `WET_INK_REQUIRED`, that decides the path the send panel offers.

The rest of the key belongs elsewhere: the documents, the regenerate, the write-once copy and the send transaction are `RWB-P5-E2017-APP` and `RWB-P5-E2017-CON`; the records are `RWB-P7-E2017-APP`; the treatment is `RWB-S2-E2017-APP`; the rights are `RWB-P4-E2017-APP`; the signature requests are `RWB-P6-E2018-APP` (API-P6-009, API-P6-010); the harness is `RWB-ITG-E2017-ITG`. The legacy AC1 to AC13 are owned by `RWB-P5-E2017-APP`; this story owns none of them and its criteria are new.

### 2. Business rationale

The legacy screens read three facts from the module's own schema: which template version is current, that Legal approved it, and which merge fields a user may correct. In the target those facts are rwb-comms data (`template`, `merge_field` in `rwb_comms`), the documents and their states are rwb-document's, and the ledger is rwb-decision's. Splitting the key on that line is what makes the catalog reusable by a letter, a notice and a generated contract alike, and it is what stops rwb-document copying a template row to render one.

The split is also where the legacy risks land. Its preconditions call the set, the Legal approval and the locked attribute "reference data" and mark them assumed; its BR1, BR3 and BR8 make the set, the overridable fields and the signature path data of Legal. If the catalog answers a version Legal has not approved, or answers a locked amount as editable, the officer signs a document no approval covers. This story therefore serves each fact as one read that carries the version in force, the approval flag and the valid-from date, and refuses closed where no approved version exists.

REQ-DCM-012 asks for generation from approved templates with no re-keying, REQ-OCC-002 for templates versioned with the Legal approval against the version, and REQ-OCC-009 for the signature path to follow the Legal rule. This story serves all three on the catalog side. Where a source fixes no value it carries the placeholder `Not specified in the source documents (GAP-2392; ASM-3968)`.

### 3. Preconditions

- `RWB-P5-E2017-CON` is published: the OpenAPI 3.1 document of `rwb-document` with the set read `GET /api/recovery/document/v1/cases/{caseId}/generated-documents`, the review read `GET /api/recovery/document/v1/documents/{documentId}/merge-values`, the `Document` and `MergeValuePage` shapes, the three states and the fakes. It is the only Contract dependency and the build runs against its fakes from Day 1.
- The catalog rows exist in `rwb_comms`: `template` (DF-REF-045 to DF-REF-069) and `merge_field` (DF-REF-252 to DF-REF-260) of TSD P6 v2 T3.1, maintained by `RWB-P6-E1046-APP` and its baseline. This story reads them and writes none.
- API-P6-003 and API-P6-005 of TSD P6 v2 T-A.1 are in force, Documents R each. The documented answer of API-P6-005 is the binary body only, so the JSON catalog answer is this story's design (GAP-2392; ASM-3968).
- The set of a treatment type and product group is reference data: "DEED_IN_LIEU uses DIL-CONTRACT, DIL-CA and DIL-MORTGAGE; RESTRUCTURE uses RES-AGREEMENT (assumed)", and CONTRACT, CREDIT_APPROVAL and MORTGAGE_DOCUMENT are legal types of the document type table (assumed). The rows are rwb-case reference data under the default ruling, reached through `RWB-P3-E1043-CON` (DP-07); their shape is Not specified in the source documents (GAP-2392; ASM-3971).
- The legacy values are unchanged: case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK", treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4, and the set "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal.
- The two screens are reached through gateway-bff composite routes (DP-19). The route and its permission are `RWB-PLT-N001-CON`, not in this story's Depends on (build) list, so the panels are developed against the route contract (GAP-2392; ASM-3972).
- The authorise answer is a REST read of rwb-access and a fake; the guard is the platform's and DP-08 is not in this story's pattern set (GAP-2392; ASM-3973).
- The release date 31 December 2026 is the legacy one and stays tentative, and the story is Draft (realignment v1) because no approval of the realigned story is recorded (ASM-3974).

### 4. Flow

1. The officer opens SCR-14 for "TRT-0401" through the gateway-bff composite route (DP-19); gateway-bff checks the session and the coarse permission, and this story repeats the right check on its own operations.
2. The panel asks the set: `GET /api/recovery/comms/v1/admin/templates?treatmentType=DEED_IN_LIEU&productGroup=MORTGAGE&state=APPROVED` (API-P6-003, DP-13).
3. TemplateSetService reads the set rows of the treatment type and product group through the rwb-case reference-data contract (DP-07): each document type with its template code and its place in the set.
4. TemplateCatalogReader reads `template` in `rwb_comms` (DP-01) for each code: the version in force (the approved version with the latest valid-from date on or before today), its language, `approved_by_legal`, `approved_at`, `valid_from`, `signature_basis` and `merge_codes`. A code with no approved version refuses the whole set (AC3).
5. The answer is one `TemplateSetPage` with three items for the legacy set, each with its document type, code, version, Legal approval and signature basis.
6. On SCR-30 the panel reads the merged values of a draft from rwb-document and the catalog of the version that draft was made from from this story: `GET /api/recovery/comms/v1/admin/templates/{templateId}/content` with `Accept: application/json` (API-P6-005).
7. MergeFieldJoin joins the two by merge code: the value and its formatted form from rwb-document, the label, the required and personal-data flags and the locked attribute from `merge_field`. A locked field is read only and the correction form offers only the unlocked ones.
8. The correction itself, its record and the write-once copy are the owners': rwb-document changes the document, rwb-decision writes the record through its library, and this story writes and keeps neither (DP-03).
9. On Send for signature the panel posts to `POST /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` (API-P6-009, `RWB-P6-E2018-APP`) with the `Idempotency-Key` header, after SendPreflight has compared the versions of the set with the versions in force (AC6).
10. Every answer is a read of `rwb_comms` and of consumed contracts: one hop, 2 s, a breaker per target, one retry with jitter on a GET (DP-11). Nothing is cached and nothing enters the outbox.
11. Screen states of SCR-14 and SCR-30: the empty, loading (SCR-14), error and no-access states are Not specified in the source documents (DOR-RWB-P6-E2017-APP-10); the loading state of SCR-30 follows Screen Specifications v1, section SCR-30.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A code of the set has no version approved by Legal | The set is refused whole; the panel disables Generate | MSG-P5-010 naming the code and the version | AC3 |
| X2 | The version of a code is withdrawn and no later one is approved | Refused closed; the place in the set is not filled from another code | MSG-P6-003 naming the code | AC3 |
| X3 | The version in force moved after the drafts were made | The pre-flight refuses the send; the officer regenerates | MSG-P5-013 naming the document and "template version 3" | AC2, AC6 |
| X4 | A merged value arrives for a merge code the catalog does not hold | Shown with its value and no label, and offered for no correction | MSG-P5-014 | AC4 |
| X5 | The field is locked by the catalog | Read only; a direct correction is refused by its owner | MSG-P5-014 naming "Transfer price" | AC4 |
| X6 | The authorise answer refuses the right | Refused before any template row is read | MSG-P4-002 | AC8 |
| X7 | The template id is unknown, or the template is outside the scope | 404; no content is answered | MSG-P4-003 | AC8 |
| X8 | The set rows do not arrive inside 2 s, or they are stale | Refused closed; no default set and no remembered rows | MSG-GEN-006 | AC1, AC7 |
| X9 | The template body cannot be read for the JSON answer | 503; the panel shows the values without the catalog and offers no correction | MSG-GEN-006 | AC4 |
| X10 | A template row appears in `rwb_document`, or a document row in `rwb_comms` | The schema inspection test fails the build | None | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against `RWB-P5-E2017-CON` and its fakes, the catalog rows and the rwb-case reference contract; no in-lane predecessor |
| Negotiable | The field shape of the JSON content answer and the filter names of the set read are settled with the screen team and the engine owner |
| Valuable | The screens show the Legal-approved version and the locked fields, and nobody re-keys a document |
| Estimable | Two reads, four readers, one join, one pre-flight, no table and no migration |
| Small | Fits one sprint as the catalog slice of a key split across five services |
| Testable | Each criterion runs against the P3 reference fake, the P5 document fakes, the P4 authorise fake and a catalog fixture |

### 7. Acceptance criteria

```gherkin
Feature: The template catalog and merge field catalog behind the generation screens

  Background:
    Given case "RW-2026-000401" with product group "MORTGAGE" in team "FCR-BKK"
    Given treatment "TRT-0401" of type "DEED_IN_LIEU" approved at D6.4
    Given the set for "DEED_IN_LIEU" is "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1, all approved by Legal
    Given a restructuring officer with role RW-RESTRUCT and scope team "FCR-BKK"
    Given the rwb-case contract mock returns the set rows of "DEED_IN_LIEU" for "MORTGAGE" with the document types "CONTRACT", "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT"

  Scenario: AC1 The set read answers the version in force of each document type (new, D-RCV-60)
    Given the officer opens SCR-14 for "TRT-0401" and the panel asks for the set
    When GET /admin/templates is called with treatmentType "DEED_IN_LIEU", productGroup "MORTGAGE" and state "APPROVED"
    Then the answer is one TemplateSetPage with three items
    Then the item for "CONTRACT" carries "DIL-CONTRACT", template version 2, approvedByLegal true and validFrom 2026-12-10
    Then the items for "CREDIT_APPROVAL" and "MORTGAGE_DOCUMENT" carry "DIL-CA" version 1 and "DIL-MORTGAGE" version 1
    Then each item carries its document type from the reference rows and its signature basis
    Then no code, version or valid-from date in the answer comes from a constant in code

  Scenario: AC2 The version in force follows the Legal approval date (new, D-RCV-60)
    Given "DIL-CONTRACT" version 2 is approved and valid from 2026-12-10
    Given "DIL-CONTRACT" version 3 is approved by Legal and valid from 2026-12-15
    When the set is read on 2026-12-14
    Then the item for "CONTRACT" carries version 2
    When the set is read on 2026-12-15
    Then the item for "CONTRACT" carries version 3
    Then version 2 stays readable by its template id and its content read still answers version 2
    Then a version or a valid-from date sent in the request is ignored

  Scenario: AC3 A version without the Legal approval, or a withdrawn version, refuses the set (new, D-RCV-60)
    Given "DIL-CA" has only version 1 and its approvedByLegal is false
    When the set for "DEED_IN_LIEU" and "MORTGAGE" is read
    Then the response is 422 with MSG-P5-010 naming "DIL-CA" and version 1
    Then no item of the set is answered and Generate documents is disabled
    Given "DIL-MORTGAGE" version 1 is withdrawn and no later version is approved
    When the set is read again
    Then the response is 422 with MSG-P6-003 naming "DIL-MORTGAGE"
    Then the place of "MORTGAGE_DOCUMENT" is not filled from another code and no default version is used

  Scenario: AC4 The merge field catalog answers the locked attribute of each value (new, D-RCV-60)
    Given the content read of "DIL-CONTRACT" version 2 is called with Accept application/json
    When the catalog of that version is answered
    Then the answer carries templateId, "DIL-CONTRACT", templateVersion 2, approvedByLegal true and the signature basis
    Then each field carries mergeCode, fieldId, sourceEntity, sourceField, isRequired, personalData and locked
    Then transfer_price is answered with locked true and contract_date with locked false
    Then the values of "DOC-0411" at doc_version 1 are joined to the catalog by merge code, and a locked value offered for correction is refused with 422 MSG-P5-014 naming "Transfer price"
    Then the binary answer of API-P6-005 for the generation engine is unchanged

  Scenario: AC5 The signature basis is data, not a rule in code (new, D-RCV-60)
    Given template "DIL-CONTRACT-MTG" of product group "MORTGAGE" has signature_basis "WET_INK_REQUIRED"
    When its set and content reads are answered
    Then both carry signatureBasis "WET_INK_REQUIRED" from the template row
    When a version approved by Legal sets signature_basis "E_SIGNATURE_ALLOWED" with valid from 2027-01-01
    Then the read of 2027-01-01 carries "E_SIGNATURE_ALLOWED" and no release and no restart was made in rwb-comms
    Then no signature basis value is written in code and the values are those of LOV-SIGNATURE-BASIS

  Scenario: AC6 The send panel passes the set to API-P6-009 after a version pre-flight (new, D-RCV-60)
    Given the three drafts of "TRT-0401" were made from "DIL-CONTRACT" version 2, "DIL-CA" version 1 and "DIL-MORTGAGE" version 1
    When the officer chooses Send for signature with Idempotency-Key "S-0401"
    Then the pre-flight passes and the panel posts to POST /treatments/{treatmentId}/signature-requests with the header unchanged
    Then the answer of API-P6-009 is returned unchanged and this story stores no request row
    When the same send with Idempotency-Key "S-0401" is chosen again
    Then the first answer is returned and no second request is asked of the owner
    When "DIL-CONTRACT" version 3 became current after the drafts were made and Send is chosen
    Then the pre-flight refuses with 422 MSG-P5-013 naming the contract and "template version 3" and no send is posted

  Scenario: AC7 No document, signature or ledger row is held in rwb_comms (new, D-RCV-60)
    Given the schema "rwb_comms" is deployed from its own Flyway sequence
    When the schema is inspected for the objects of this story
    Then the only objects it reads are "template" and "merge_field"
    Then no table, view or synonym of a document, a document_field, a signature_request or a decision_log_entry exists in "rwb_comms"
    Then the login of rwb-comms holds no grant on "rwb_document", "rwb_case", "rwb_access" or "rwb_decision"
    Then this story adds no migration and writes no record to "rwb.decision-record.v1"

  Scenario: AC8 The right and the scope are checked on both reads (new, D-RCV-60)
    Given RW-TEAMMGR holds Documents R and RW-BIANAL holds no Documents right
    When RW-TEAMMGR reads the set and the content
    Then both answers are 200 and every field is read only
    When RW-BIANAL reads the set
    Then the response is 403 with MSG-P4-002
    When a caller asks for an unknown template id, or a template outside its scope
    Then the response is 404 with MSG-P4-003
    Then the authorise answer is read once per call, one hop, and no right is computed in rwb-comms

  Scenario: AC9 Every rule BR1 to BR10 of section 8 is proven by a test case of section 16 (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When the test cases of section 16 are listed
    Then each rule carries at least one test case ID that appears in section 16
    Then a rule that is an architecture constraint is proven by TC-P6-E2017-APP-02 or by a boundary test

  Scenario: AC10 A consumed read that fails or does not answer within 2 s is retried once and then refused (new, D-RCV-60)
    Given the rwb-case contract mock does not answer within 2 s on the set read
    When the set is read
    Then one retry with jitter is made on the GET and no further retry is made
    Then when the retry also fails the answer carries the owner's message unchanged and no item of the set is answered
```

The eight criteria are new and test only the catalog side of the screens. The legacy AC1 to AC13 stay with `RWB-P5-E2017-APP`; the legacy values are reused unchanged where a criterion needs them, so "RW-2026-000401", "TRT-0401", "DOC-0411", "DIL-CONTRACT" version 2, a locked transfer_price, "WET_INK_REQUIRED" and "template version 3" are the source values.

### 8. Business rules

| ID | Rule | Source | Test cases |
|---|---|---|---|
| BR1 | The set of templates for a treatment comes from reference data by treatment type and product group, never from code | legacy BR1; RWB-E1-046; DL28 (open; assumptions ASM-1861, ASM-1925, ASM-2093, ASM-2727) | TC-E2-017-01 |
| BR2 | A version is in force from its valid-from date once Legal approved it, and earlier versions stay readable | FSD P6 AC-ALT-P6-007-01; `template.valid_from` | TC-E2-017-13 |
| BR3 | A set is answered only when every code holds an approved version; a withdrawn code with no later approval refuses the whole set | FSD P6 AC-EXC-P6-007-02 and -03; legacy BR2 | TC-E2-017-04 |
| BR4 | Only a field the catalog marks unlocked may be corrected, and only with a reason | legacy BR3; merge field catalog | TC-E2-017-05, TC-E2-017-06 |
| BR5 | The label, the required flag and the personal-data flag are catalog data, and no value is offered as correctable without them | `merge_field`; legacy BR3 | TC-P6-E2017-APP-01 |
| BR6 | The signature basis is data of Legal, `E_SIGNATURE_ALLOWED` or `WET_INK_REQUIRED`, never a rule in code | legacy BR8; `template.signature_basis`; LOV-SIGNATURE-BASIS | TC-P6-E2017-APP-01 |
| BR7 | A set is sent only from the version in force; the pre-flight compares and the owner checks again | legacy BR6; FSD P6 AC-EXC-P6-007-16 | TC-E2-017-07 |
| BR8 | rwb-comms holds no document, signature or ledger row, reads none from another schema and keeps no catalog copy | DP-01; Ownership Map rows of P6 | TC-P6-E2017-APP-02 |
| BR9 | One base, one hop and 2 s on every consumed read, with a breaker and one retry with jitter on a GET | DP-11, DP-13, ADR-020 | TC-E2-017-12 |
| BR10 | Every refusal uses its owner's message unchanged and no refusal is reworded here | legacy section 14 | TC-E2-017-14 |

### 9. State transitions

None. This story changes no case state, no document state and no request state: those belong to rwb-case, rwb-document and the request story. The only state it reads is the template version.

| Version state | Event | Condition | What this story answers |
|---|---|---|---|
| DRAFT | Uploaded by the catalog story | Not yet approved | Not offered |
| APPROVED | Legal approval recorded with a valid-from date (API-P6-006) | Date reached | Offered as the version in force, `approvedByLegal` true |
| APPROVED | A later version becomes valid | Newer valid-from date | The newer one is offered; the older stays readable by id |
| WITHDRAWN | Withdrawal recorded with a reason (API-P6-007) | No later approved version | Refused closed with MSG-P6-003 |

The approval and the withdrawal are the catalog story's operations (`RWB-P6-E1046-APP`); this story reads their outcome only.

### 10. Authority

The rights are the Documents rights of TSD P6 v2 T6.1, declared by each operation and answered by the rwb-access authorise contract through the platform guard, one hop and 2 s. DP-08 is not in this story's pattern set, so no guard work is added.

| Who | Documents (T6.1) | What this story allows |
|---|---|---|
| RW-RESTRUCT, restructuring officer (FCR) | CRU | Reads the set and the catalog, corrects an unlocked value, chooses Send |
| RW-CASEOWN, case owner | CRU | The same, in the cases of its queue |
| RW-LEGAL, legal counsel | CRUA | Reads both; owns the approvals that make a version current |
| RW-TEAMMGR, team manager | R | Reads both read only |
| RW-CREDCOMM, credit approval committee member | R | Reads both read only |
| RW-PLATADM, platform administrator | R | Reads both read only |
| RW-BIANAL, reporting and BI analyst | - | Refused both reads with MSG-P4-002 |
| SY-CASEWF, case workflow module | R | Service identity: reads the set for a scripted step, no person involved |

No role approves a template version here: the A right is exercised on API-P6-006 by `RWB-P6-E1046-APP`, and a caller without it is refused there with MSG-P4-002. Scope filters every query, so a template outside the caller's team scope answers 404.

### 11. Data

| BR Field ID | Entity | Field | Owner | Read or write |
|---|---|---|---|---|
| DF-REF-045, DF-REF-046, DF-REF-047 | template | id, template_code, template_version | P6 (rwb_comms) | Read in the service's own schema |
| DF-REF-048, DF-REF-049 | template | language, product_group | P6 (rwb_comms) | Read; LOV-LANG and LOV-PRODUCT |
| DF-REF-051, DF-REF-063, DF-REF-064 | template | approved_by_legal, approved_by, approved_at | P6 (rwb_comms) | Read; the Legal approval of the version |
| DF-REF-065, DF-REF-068, DF-REF-069 | template | valid_from, signature_basis, merge_codes | P6 (rwb_comms) | Read; the version in force, the path, the codes used |
| DF-REF-050 | template | body_ref | P6 (rwb_comms) | Not parsed: the body is answered as binary to the engine |
| DF-REF-252, DF-REF-253, DF-REF-256 | merge_field | id, merge_code, field_id | P6 (rwb_comms) | Read; the join key with the merged value |
| DF-REF-254, DF-REF-255 | merge_field | source_entity, source_field | P6 (rwb_comms) | Read; the provenance of a value |
| DF-REF-257, DF-REF-258 | merge_field | is_required, personal_data | P6 (rwb_comms) | Read; the required and masking flags |
| DF-REF-259, DF-REF-260 | merge_field | catalog_version, valid_from | P6 (rwb_comms) | Read; the catalog version the field belongs to |
| The locked attribute of a merge field | merge_field | not named in TSD P6 T3.1 | P6 (rwb_comms) | Read with the placeholder Not specified in the source documents (GAP-2392; ASM-3969) |
| DF-DOC-001, DF-DOC-004, DF-DOC-032, DF-DOC-033 and the state | document | id, document_type, template_id, treatment_id, state | P5 (rwb_document) | Read through the P5 contract only |
| DF-REF-028, DF-REF-029 and the set rows | lov_value and reference rows | lov_code, value_code, the set of a treatment type | P3 (rwb_case) | Read through the P3 reference-data contract (DP-07) |
| DF-REF-035 | role | role_code | P4 (rwb_access) | Read through the authorise answer, never by SQL |

No row of `template` or `merge_field` is written here, and no row of `document`, `document_field`, `signature_request` or `decision_log_entry` is read or written. Field IDs are those of the Logical Data Model and Data Dictionary; the notice and dispatch rows are not used.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`.

| Method | Path | API ID | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/admin/templates` | API-P6-003, its query widened with `treatmentType` and `productGroup` as an additive change within major version 1 (GAP-2392; ASM-3970) | Query `treatmentType`, `productGroup`, `state`, `page`, `size` | 200 `TemplateSetPage`: items each with templateId, documentType, templateCode, templateVersion, language, productGroup, channel, approvedByLegal, approvedAt, validFrom, state, signatureBasis, mergeCodes; plus page, size, total | Documents R, scope applied | GET, no key |
| GET | `/admin/templates/{templateId}/content` | API-P6-005, answered as `TemplateContent` when `Accept` is `application/json` and as the binary body otherwise (GAP-2392; ASM-3968) | Path `templateId`; header `Accept` | 200 `TemplateContent`: templateId, templateCode, templateVersion, language, productGroup, approvedByLegal, validFrom, state, signatureBasis, mergeCodes, fields each with mergeCode, fieldId, sourceEntity, sourceField, isRequired, personalData, locked | Documents R, scope applied | GET, no key |

Errors of both: 401 MSG-P4-001; 403 MSG-P4-002; 404 MSG-P4-003 for an unknown id or a template outside the scope; 422 MSG-P5-010 for a version without the Legal approval and MSG-P6-003 for a withdrawn code; 503 MSG-GEN-006 naming the system that did not answer. No operation here writes, so no `Idempotency-Key` is declared and no POST or PATCH is added to the base.

#### 12.2 REST operations consumed

| Call | Owner | Use in this story |
|---|---|---|
| `GET /api/recovery/case/v1/admin/lists/{listCode}` and the set rows under `RWB-P3-E1043-CON` (DP-07) | P3 rwb-case | LOV-PRODUCT, LOV-SIGNATURE-BASIS and the rows that map a treatment type and product group to document types and template codes; shape Not specified in the source documents (GAP-2392; ASM-3971); faked |
| `GET /api/recovery/document/v1/cases/{caseId}/generated-documents` | P5 rwb-document | The documents of the treatment with their type, template code, version and state, so the panel knows which drafts to show beside the set; faked from `RWB-P5-E2017-CON` |
| `GET /api/recovery/document/v1/documents/{documentId}/merge-values` | P5 rwb-document | The merged value and its formatted form per merge code, joined to the catalog of the version the draft was made from; faked |
| `POST /api/recovery/access/v1/authorise` | P4 rwb-access | The right and the scope of the caller, read once per call through the platform guard; faked; DP-08 is not in this pattern set (ASM-3973) |
| `POST` and `GET /api/recovery/comms/v1/treatments/{treatmentId}/signature-requests` | rwb-comms, same service, owned by `RWB-P6-E2018-APP` (API-P6-009, API-P6-010) | The send the panel posts to and the request state it shows; this story asks the answer and stores nothing |

Every row is one hop with a 2 s timeout and a breaker, and a GET is retried once with jitter (DP-11, ADR-020). The boundary is fixed: the template and its catalog are this service's; the document, its versions and its states are P5's; the treatment and its approval are S2's; the ledger is P7's; the set rows and the lists are P3's; the rights are P4's.

#### 12.3 Events published

None. The story reads a catalog and changes no state, so nothing enters the outbox and nothing is added to `rwb.comms.events.v1`, whose events remain `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered` under the DP-14 naming (TSD P6 T5.3). DP-09 is not in the pattern set and no template or approval event is invented.

#### 12.4 Events consumed

None. A change of a version, of its Legal approval or of a merge field reaches the screens on the next read, so no consumer, inbox group or retry topic is registered. DP-03 is applied as a boundary and not as a write: the record of a correction and of a send is written by the producing service into its ledger through the local decision-record library on `rwb.decision-record.v1`, and this story writes none and keeps no copy; the reference the screen shows is the opaque value of the P5 answer.

#### 12.5 Workflows and activities

None. Both operations are synchronous reads with a 2 s budget; no workflow, activity or child workflow is started on task queue `rwb-comms`. The service's `NoticeDispatchWorkflow` is not used and the send path of API-P6-009 belongs to `RWB-P6-E2018-APP`.

#### 12.6 Schedules

None. There is no sweep, no nightly refresh and no cache warm-up: the version in force is computed at read time from `valid_from`, and a stored copy would be a second place for a version to be wrong. No Temporal Schedule is registered.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| template | P6 (rwb_comms) | Read for the version in force, the Legal approval, the valid-from date, the signature basis and the merge codes; written by `RWB-P6-E1046-APP` only |
| merge_field | P6 (rwb_comms) | Read for the merge code, the field id, the required flag and the personal-data flag as stored in the catalog (this story sets the personal-data flag of no field) and the locked attribute; written by `RWB-P6-E1046-APP` only |
| No document, document_field, signature_request or decision_log_entry object | Not owned, never created | AC7: no cross-schema object and no local copy |
| The locked attribute of a merge field | P6 (rwb_comms) | Not named in TSD P6 T3.1; carried as the placeholder Not specified in the source documents (GAP-2392; ASM-3969) |

No migration is added and no statement here names a table in another schema (DP-01, DP-15). The service login is the rwb-comms login and holds no privilege on `rwb_document`, `rwb_case`, `rwb_access` or `rwb_decision` (DP-02).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-comms catalog fixture | `template` rows for "DIL-CONTRACT" versions 2 and 3, "DIL-CA" version 1 with `approved_by_legal` false, withdrawn "DIL-MORTGAGE" version 1 and "DIL-CONTRACT-MTG" with "WET_INK_REQUIRED"; `merge_field` rows with transfer_price locked and contract_date unlocked | AC1 to AC5, AC7 |
| rwb-case reference-data WireMock | The set rows of "DEED_IN_LIEU" for "MORTGAGE" with the three document types, LOV-PRODUCT, LOV-SIGNATURE-BASIS and LOV-SIGN-METHOD, and a delayed answer | AC1, AC3, AC5 |
| rwb-document contract fake: `RWB-P5-E2017-CON` document WireMock (library version Not specified in the source documents (DOR-RWB-P6-E2017-APP-22)) | The set read of "TRT-0401" with three drafts and the merge values of "DOC-0411" at doc_version 1, contract_date "2026-12-10" and transfer_price 1250000.00 | AC4, AC6 |
| rwb-access authorise WireMock | RW-RESTRUCT with Documents CRU, RW-TEAMMGR with R, RW-BIANAL with none, and a delayed answer | AC8 |
| API-P6-009 stub | "ACCEPTED" with one request, a repeat answered with the first result, and "UNAVAILABLE" | AC6 |
| Decision-record stub | A producing service writing one record; this story is asserted to write none | AC7 |

The fixture stands where `RWB-P6-E1046-APP` lands its rows, and the JSON answer is replaced by the published operation when the catalog baseline is revised (GAP-2392; ASM-3968).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The two template reads provided; the P3 lists and set rows, the two P5 document reads, the P4 authorise answer and the in-service API-P6-009 and API-P6-010 consumed; one hop, 2 s, breaker |
| Kafka | None | No produce and no consume; the service topic keeps the three notice events of the DP-14 naming |
| Temporal | None | No workflow, activity or Schedule here |
| File | None | Nothing is read from or written to a file; the binary body is answered to the engine and not parsed |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `catalog`, package `th.co.scb.ace.workbench.recovery.comms.catalog`. Base `/api/recovery/comms/v1`, schema `rwb_comms`; topic and task queue are not used here.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; `template` and `merge_field` read there and nowhere else | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and `rwb.decision-record.v1`; applied as a boundary — the record is the producer's and this story writes and keeps none | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case for the set rows and the lists behind the codes | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route behind SCR-14 and SCR-30 | H RWB-PLT-N001-CON |

The dependencies the DP table attaches to DP-03, DP-07 and DP-19 are not in this story's four dependency columns, which the plan fixed at None, `RWB-P5-E2017-CON`, None and None; the build goes against the platform release train and the published P3 and P5 documents (GAP-2392; ASM-3972).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TemplateSetController | Controller | `GET /admin/templates`, query and paging validation, the problem mapping for 401, 403, 404, 422 and 503 |
| TemplateContentController | Controller | `GET /admin/templates/{templateId}/content` and the `Accept` choice between the JSON catalog and the binary body |
| TemplateSetService | Service | The set of a treatment type and product group and its refusal-closed rule |
| TemplateVersionResolver | Service | The version in force per code from `valid_from`, `approved_by_legal` and the state, with the older version still readable |
| MergeFieldJoin | Service | The join of the P5 value with the catalog row by merge code, and the read-only rule of a locked field |
| SignatureBasisReader | Service | The `signature_basis` of the version and the list values it may take |
| ReferenceCatalogClient | Client | The P3 set rows and lists, one hop, 2 s, breaker |
| DocumentCatalogClient | Client | The two P5 reads, faked from `RWB-P5-E2017-CON` |
| SendPreflight | Service | The comparison of the versions of the set with the versions in force, and the relay of API-P6-009 |

**Database and migrations.** Reads `template` and `merge_field` in `rwb_comms`; creates no table, view, index or grant and adds no migration. The locked attribute is read from the catalog row once `RWB-P6-E1046-APP` adds it, until then from the fixture (ASM-3969).

**Configuration and reference data.** The set rows through DP-07, whose shape is Not specified in the source documents (ASM-3971); LOV-PRODUCT, LOV-SIGNATURE-BASIS, LOV-LANG and LOV-SIGN-METHOD as data with their version; the read budget of one hop, 2 s, one retry with jitter and a breaker per target; and the feature switch `rwb.comms.template-catalog`, off answering 503 for both reads and never serving a default version.

**Build steps**

1. TemplateSetController and TemplateSetService over the shape of 12.1, with the right check first; test AC8.
2. TemplateVersionResolver with the valid-from and approval rules and the older version kept readable; test AC1 and AC2.
3. The refusal-closed rules of the whole set; test AC3.
4. TemplateContentController with the `Accept` choice, then MergeFieldJoin against the P5 fake; test AC4.
5. SignatureBasisReader and its list values; test AC5.
6. SendPreflight and the relay of API-P6-009 with the key unchanged and the first answer returned; test AC6.
7. The no-copy proof and the gateway-bff route of the two panels against the fakes; test AC7.

**Done when.** The tests of section 16 pass, the schema inspection shows only `template` and `merge_field` behind the two reads, and a SIT week shows a new "DIL-CONTRACT" version becoming current on its valid-from date with the old one still readable and no release of rwb-comms.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-001 | No session, or no Recovery Workbench role | You have no Recovery Workbench role. Ask your team manager to request one. |
| MSG-P4-002 | The role lacks Documents R | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The template id is unknown, or the template is outside the scope | Not specified in the source documents (GAP-2392; ASM-3975) |
| MSG-P5-010 | A version of a code of the set has no Legal approval | Not specified in the source documents (GAP-2392; ASM-3975) |
| MSG-P6-003 | A code of the set is withdrawn and no later version is approved | Not specified in the source documents (GAP-2392; ASM-3975) |
| MSG-P5-013 | Send with a document on a version no longer in force | {document} cannot be sent yet: {reason}. |
| MSG-P5-014 | A locked merge field is offered for correction | {field} comes from the approved treatment and cannot be changed here. |
| MSG-P5-002 | A change to a document already sent | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-006 | A consumed read did not answer in time, or the template body cannot be read | {system} is not available. Your request is queued and will be retried. |
| MSG-P7-003 | The ledger write of the owner fails on a correction or a send | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

Every text is copied unchanged from legacy RWB-E2-017 section 14 or the FSD message set; the five IDs whose text is not in the sources read carry the placeholder and no invented wording. Thai text follows decision DL10 (open; assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863).

### 15. Screens and states

Both screens are reached through gateway-bff composite routes (DP-19); this story builds the two catalog reads and one pre-flight behind them and no panel of its own.

| Screen | State | What the user does |
|---|---|---|
| SCR-14 Treatment record | Approved | Sees the set with the version and Legal approval of each document type and the signature basis the send will take; chooses Generate documents and Send for signature |
| SCR-14 Treatment record | Draft, submitted | Generate documents is disabled with MSG-P5-011, answered by the treatment owner through the route |
| SCR-14 Treatment record | Set refused | Shows MSG-P5-010 or MSG-P6-003 for the code without an approved version and offers no Generate |
| SCR-14 Treatment record | Empty | Not specified in the source documents (CG-ALL-6508) |
| SCR-14 Treatment record | Loading | Not specified in the source documents (CG-ALL-6508) |
| SCR-14 Treatment record | Error | Not specified in the source documents (CG-ALL-6508) |
| SCR-14 Treatment record | No access | Not specified in the source documents (CG-ALL-6508) |
| SCR-30 Case documents | List | Opens a draft: PDF and values from rwb-document, labels and locked flags from this story, and a form only on the unlocked fields |
| SCR-30 Case documents | Read only (common state) | A sent document, or any document for RW-TEAMMGR, shows without edit controls |
| SCR-30 Case documents | Empty | Not specified in the source documents (CG-ALL-6509) |
| SCR-30 Case documents | Loading | As Screen Specifications v1, section SCR-30 (CG-ALL-6509) |
| SCR-30 Case documents | Error | Not specified in the source documents (CG-ALL-6509) |
| SCR-30 Case documents | No access | Not specified in the source documents (CG-ALL-6509) |

No screen shows a template body, a person or a record: the panels show codes, versions, dates, flags and the list names behind them.
Generation, review and signature go through the RWB-P5-E2017-CON and RWB-P6-E2017-CON contracts (the latter not yet issued); the treatment holds the document reference only, and schema rwb_treatment keeps no document content (GAP-1704).
Placement (GAP-2698): the actions and their records stay with RWB-P5-E2017-APP; the treatment gate and the treatment leg of the screen stay with rwb-treatment; one screen is served through gateway-bff; rwb-treatment writes no decision record of this key.
The treatment-side panel section is an optional additive property of the declared treatment read; its names, the action vocabulary and the set read from RWB-P5-E2017-CON (2 s budget) stay provisional until the contracts are frozen (GAP-2697).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-017-14 | AC8 | Component | RW-TEAMMGR user (Documents R) calls both reads; a role without Documents is refused with MSG-P4-002 |
| TC-E2-017-01 | AC1, AC4 | End to end | Synthetic mortgage DIL treatment, three approved templates |
| TC-E2-017-02 | AC4 | End to end | Contract date moved by two days |
| TC-E2-017-03 | AC6 | End to end | Three reviewed drafts; API-P6-009 stub returns ACCEPTED |
| TC-E2-017-04 | AC3 | End to end | Treatment with no decision_log_id; the set refused for the code without the Legal approval |
| TC-E2-017-05 | AC4 | End to end | Empty reason |
| TC-E2-017-06 | AC4 | End to end | Locked transfer price |
| TC-E2-017-07 | AC6 | End to end | One draft not reviewed; the pre-flight refuses the send |
| TC-E2-017-08 | AC6 | End to end | Document in state SENT |
| TC-E2-017-09 | AC7 | End to end | Decision log stub refusing writes on a correction; this story writes no record |
| TC-E2-017-10 | AC6 | End to end | Same send key twice |
| TC-E2-017-11 | AC6 | End to end | Two sessions on one draft |
| TC-E2-017-12 | AC6 | End to end | API-P6-009 stub returns UNAVAILABLE, then ACCEPTED |
| TC-E2-017-13 | AC2 | End to end | Template version 3 made current after the drafts |
| TC-E2-017-15 | AC7 | NFR | Ledger write forced to fail on the send; nothing sent, the catalog unchanged, MSG-P7-003, incident raised |
| TC-P6-E2017-APP-01 | AC1, AC5 | Contract | The `TemplateSetPage` and `TemplateContent` schemas against the document, with the three legacy codes and both signature basis values |
| TC-P6-E2017-APP-02 | AC7 | Component | Schema inspection of `rwb_comms` for a document, document_field, signature_request or decision_log_entry object, and the grant check of the login |
| TC-P6-E2017-APP-03 | AC1, AC5 | Component | Read of the `template` and `merge_field` tables of section 12.7 at the boundary: a merge field with no locked value, and a template with no later approval |
| TC-P6-E2017-APP-04 | AC9 | Component | Each rule BR1 to BR10 of section 8 listed with its test case IDs; the architecture-constraint rules checked against TC-P6-E2017-APP-02 |
| TC-P6-E2017-APP-05 | AC10 | NFR | rwb-case contract mock that does not answer within 2 s on the set read; one retry, then the owner's refusal |

The fifteen legacy IDs, their order and their Data are kept. Levels follow the set mapping: legacy System is End to end, legacy Access is Component, legacy Resilience is NFR; the five new cases are Contract, Component and NFR. Covers points at this story's new criteria, because the legacy cases were written against the screens, the regenerate and the send that `RWB-P5-E2017-APP` now owns: here the same data proves the catalog side. The full test with its Given, When and Then is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. The Covers column above keeps this story's own criteria, and the legacy criteria numbers are not copied.

### 17. Guardrails

- No business value in code: the set, the document types, the lists, the signature basis and the locked attribute are data of their owners (DP-01, DP-07).
- No personal data in events, workflow inputs, logs, tests or prompts: the catalog carries codes, versions, dates and flags, and `personal_data` travels as a boolean, never as a value.
- ACE data only through the owner's contract or the owner's `v_ace_*` views; this story reads no ACE table and no ACE view.
- No cross-schema read and no cross-service write: `template` and `merge_field` in `rwb_comms`, the documents through `RWB-P5-E2017-CON`, the set rows through DP-07 (DP-01).
- No local copy and no catalog cache: the version in force is computed at read time, and the inspection test of AC7 fails the build if a document, signature or ledger object appears in `rwb_comms`.
- One base, one hop and 2 s on every consumed read, with a breaker and one retry with jitter on a GET; a slow answer refuses both reads closed (DP-11, DP-13, ADR-020).
- A version is offered only when Legal approved it and its valid-from date has arrived; a code without one refuses the whole set and no default is served.
- The right is asked, never computed, and a refusal is MSG-P4-002 in every service.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-012 | Contracts, credit applications and mortgage documents generated from approved templates with no re-keying | Program, section 5.5; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | R-DIL-14, R-DIL-16, R-DIL-18 | TC-E2-017-01, TC-E2-017-03, TC-E2-017-04, TC-E2-017-07, TC-E2-017-13, TC-P6-E2017-APP-01 |
| REQ-OCC-002 | Templates versioned with the Legal approval recorded against the version | Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 13 Manage documents and correspondence | R-LIT-03 | TC-E2-017-01, TC-E2-017-04, TC-E2-017-13, TC-P6-E2017-APP-01 |
| REQ-OCC-009 | The signature path follows the product and the Legal rule | Program, section 5.6; Epic 2, section 3.5 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu | R-DIL-18, R-RES-16 | TC-E2-017-03, TC-E2-017-12, TC-P6-E2017-APP-01 |
| RWB-E2-017 | The legacy key this story is the catalog slice of; its AC1 to AC13 are owned by RWB-P5-E2017-APP | Legacy section 7 | FEAT-OCC-07 | 7.3 Negotiate settlement or deed in lieu; 13 Manage documents and correspondence | BR1 to BR10 of section 8 | All twenty cases of section 16 |
| DP set | DP01, DP03, DP07, DP11, DP13, DP19 | Template and Rules section R5.5 | - | - | - | TC-E2-017-01, TC-E2-017-02, TC-E2-017-13, TC-E2-017-14 |
| ADR-013 | 19 services inside ACE, each with its own schema and login | Architecture v5 slides 20 and 41 | - | - | - | TC-P6-E2017-APP-02 |
| ADR-014 | One schema and one login per service in ACE PostgreSQL | Architecture v5 slide 41 | - | - | - | TC-P6-E2017-APP-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | Template and Rules section R5.5, DP-11 | - | - | - | TC-E2-017-14, TC-E2-017-12 |

CTL-12 and CTL-14 apply to the write-once copy and to the completeness of a set at send, and both are exercised by `RWB-P5-E2017-APP`; this story carries the version check that feeds CTL-14 and no control of its own.

### 19. Out of scope

- The draft store, the regenerate, the write-once copy, the send transaction and the four document operations: `RWB-P5-E2017-APP` and `RWB-P5-E2017-CON`.
- The generation engine, its template selection and its merge rules: `RWB-P5-E2026-APP` and `RWB-P5-E2026-CON`.
- The record of a correction and of a send, and the ledger read: `RWB-P7-E2017-APP`.
- The treatment, its approval at D6.4 and its `decision_log_id`: `RWB-S2-E2017-APP`.
- The rights, the scope and the permission matrix: `RWB-P4-E2017-APP` and `RWB-P4-E1037-CON`.
- The signature requests, their send, their result and the signed copy: `RWB-P6-E2018-APP` (API-P6-009 to API-P6-011).
- The upload, the approval and the withdrawal of a template version: `RWB-P6-E1046-APP` and `RWB-P6-E1046-CON`.
- The composite routes of SCR-14, SCR-30 and the case screens: `RWB-PLT-N001-CON`.
- The end-to-end proof across the five services: `RWB-ITG-E2017-ITG`.
