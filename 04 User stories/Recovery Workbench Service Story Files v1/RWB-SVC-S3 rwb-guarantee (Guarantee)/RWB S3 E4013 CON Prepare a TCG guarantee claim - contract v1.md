# RWB-S3-E4013-CON Prepare a TCG guarantee claim - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-013 for rwb-guarantee (S3). The preparation side of the guarantee-claim resource is published on Day 1 on base `/api/recovery/guarantee/v1` (DP-13): the create operation, the two schemas the preparation needs, the `guarantee_claim` DDL template with the standard columns, the error set, the versioning rule and the fakes. The four legacy acceptance criteria stay with RWB-S3-E4013-APP and every criterion here is new. The resource is reached by the browser through the gateway-bff composite route for SCR-17 (DP-19). The update that records the filing is published by RWB-S3-E4014-CON on the same base, so the document is split by operation and recorded as one conflict (GAP-2709; ASM-4500); TSD S3 T-A.1 declares no read operation, so v1 publishes no GET (GAP-2709; ASM-4501). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **service contract owner**, I want **the published contract of the preparation side of the guarantee-claim resource of rwb-guarantee (S3) — the base `/api/recovery/guarantee/v1`, `POST /cases/{caseId}/guarantee-claims` with the entity names `GuaranteeClaimRequest` and `GuaranteeClaim` of TSD S3 T-A.2, the elements named in camelCase after DF-TRT-015 to DF-TRT-022, the `guarantee_claim` DDL template with the T3.0 standard columns, the error set 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body, the `Idempotency-Key` rule, the versioning rule and the fakes** instead of the monolith's in-process controller and the one `recovery.guarantee_claim` table of the shared schema, so that **RWB-S3-E4013-APP and every later story of the service build against one frozen shape from Day 1, with no wait on any other team**.

This story owns the contract of one resource and nothing else:

- the OpenAPI 3.1 document of the guarantee-claim resource, its server base and its create operation, with the problem schema and the security;
- the two object schemas the preparation needs — `GuaranteeClaimRequest` for the create body and `GuaranteeClaim` for the answer — with the element naming rule, the required set and the enumeration rule;
- the `guarantee_claim` DDL template with the eight fields of TSD S3 T3.1 and the seven standard columns of T3.0, one template each environment applies in this service's own schema, with no cross-schema key;
- the error set of the create, the `Idempotency-Key` rule, the compatibility rule and the pinning rule;
- the fake set generated from the document, and the drift test that every consuming build runs.

It does not own: the handlers, the workflow branch, the checklist assembly and the claim write, which are RWB-S3-E4013-APP; the update that records the filing and its `GuaranteeClaimUpdate` schema, which are RWB-S3-E4014-CON, and the approval and submission behind it, which are RWB-S3-E4014-APP; the tracking to payment, which is RWB-S3-E4015-APP; the subrogation position, which is RWB-S3-E4016-APP; the guarantor notices, which are RWB-S3-E4017-APP; the case status and the case signal, which are rwb-case's; the central ledger and the `GUA` rule rows, which are P7's; the roles and rights data, which are rwb-access's; the composite route, which is the platform edge story's; the scheme documents, which are rwb-document's.

### 2. Business rationale

The monolith exposed the claim through one controller in the shared process on the legacy base, and the claim row lived in the one `recovery` schema beside 91 other tables (TSD S3 T2, T3.1). Three facts follow from the target and make a contract necessary before any code. First, the schema is now `rwb_guarantee` with its own login and no cross-schema access, so the table shape has to be a template every environment applies rather than one shared migration (DP-01, DP-02, DP-15). Second, the base is now `/api/recovery/guarantee/v1`, so the claim paths no longer collide with the case, the payment and the treatment services and every caller has one place to read them (DP-13). Third, five stories of this service and the reporting and integration builds read a claim, so the elements, the required set and the error set have to be frozen before the first of them starts.

TSD S3 already fixes most of it, and this story publishes what the source states rather than inventing: T-A.1 names the two paths, their rights and the first epic; T-A.2 names the request, the update and the response entities `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` with the error statuses and the `Idempotency-Key` header on the create; T3.1 names the eight fields of `guarantee_claim` with their physical types, their required flag and their list; T3.0 names the standard record columns; T3.2 names the members of LOV-CLAIM-STATUS and LOV-CLAIM-TYPE.

One resource and two contract stories is the split the plan forces, because each legacy key gets its own CON story and both keys name the same two operations. The reading taken here is that the resource is published once and split by operation: this story freezes the base, the element naming rule, the required set, the DDL template, the versioning rule and the fakes, and RWB-S3-E4014-CON publishes the update that records the filing against the same base and pins what is frozen here (GAP-2709; ASM-4500). The alternative — two documents on one base — is the failure the registry is there to catch.

What the source does not state is recorded, not filled. TSD S3 T-A.1 lists two operations and no read, so v1 publishes no GET and the screen's claim content is what the create and the update answers return alongside the case read (GAP-2709; ASM-4501). The scheme checklist has no field of its own on `guarantee_claim`, so the checklist is an activity output and is not a published element (GAP-2709). The retention and archive rule of a claim row is stated nowhere, so the template declares none (GAP-2709).

The fake is the Day-1 unblocker. RWB-S3-E4013-APP, the four sibling application stories and any reporting or integration build can create and read a claim before a single table exists in an environment, and the drift test turns a private variant of the shape into a build failure rather than a defect found in SIT.

### 3. Preconditions

- TSD S3 T-A.1 fixes the endpoint inventory: API-S3-001 `POST` on `/cases/{caseId}/guarantee-claims` with right C and the `Idempotency-Key` header, and API-S3-002 `PATCH` on `/guarantee-claims/{claimId}` with right U and idempotency not applicable; the base becomes `/api/recovery/guarantee/v1` by DP-13 and this story publishes the first of the two.
- TSD S3 T-A.2 fixes the entity names `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` and the error statuses 401, 403, 404, 409, 422 and 503; the update schema belongs to RWB-S3-E4014-CON and is named here only.
- TSD S3 T3.1 fixes DF-TRT-015 to DF-TRT-022 with their physical types, their required flags and their lists, and T3.0 fixes the seven standard record columns.
- TSD S3 T3.2 fixes the list codes LOV-CLAIM-STATUS and LOV-CLAIM-TYPE; their members are values in force and are not restated in the document (BR-S3-001).
- TSD S3 T6.1 fixes the capability area "Treatment and offer" and the rights of each role; the document declares the right of the operation and holds no role list.
- The problem envelope is the platform one, RFC 9457 `application/problem+json` with the platform extension members; the platform API style guide fixes its member names, so this document reuses them and does not redeclare them.
- RWB-PLT-E1027-CON publishes the decision-record contract; this document names it as the writer behind the decision of a preparation and declares no record element of its own (DP-03).
- RWB-PLT-E1044-CON publishes the per-service Flyway conventions, so the DDL is a template applied by this service's own sequence and not one shared migration (DP-15).
- No source gives a claim read operation, a checklist field or a retention rule; all three are outside this contract and are recorded once (GAP-2709; ASM-4501).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), it sits in contract group CG-W3 and it is published at status Draft (realignment v1; ASM-4498).

### 4. Flow

1. The contract author fixes the base and the create operation of section 12.1, taken character for character from TSD S3 T-A.1 with the DP-13 base, and records that the update of the same resource is RWB-S3-E4014-CON's (ASM-4500).
2. The author fixes the element naming rule: every element of the two schemas is a DF-TRT field name in camelCase, and `caseId` is taken from the path on the create and is not repeated in the request body.
3. The author fixes the required set from the required column of TSD S3 T3.1, so `claimType`, `claimDeadline`, `claimedAmount` and `status` are required on the answer and on the create body, and `filedAt` and `paidAmount` are optional and null at preparation.
4. The author fixes the enumeration rule: an enumerated element names its list code and no member, because the members are values in force (BR-S3-001).
5. The author writes the `guarantee_claim` DDL template: the columns, the physical types, the required set, the primary key, the index on `case_id`, the standard columns and the rule that no key crosses a schema.
6. The author writes the error set of the create with the problem envelope and the message identifiers the platform catalogue already holds, the `Idempotency-Key` rule and the 409 cause of a claim already open for the case.
7. The author writes the versioning and pinning section: a compatible change keeps major version 1, a breaking change raises major version 2 under a new base segment, v1 is never edited in place, and the update of RWB-S3-E4014-CON pins this version.
8. The lint and schema steps run: the document linted against the platform style, every example validated against its schema, the personal-data scan run on the examples, and the template applied twice in two throwaway schemas.
9. The fake set is generated from the document: the create answer, the create refusals, the repeated-key answer and the unavailable answer, all from one example set.
10. The drift test is generated and wired into the build of RWB-S3-E4013-APP, of the four sibling application stories and of RWB-S3-E4014-CON.
11. The document and the fakes are published at v1, and the pinned version of this contract and of each consuming story is recorded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A path outside `/api/recovery/guarantee/v1`, a read operation, or a second create is added to the document | The lint fails the build; the base and the create are fixed, and the update is RWB-S3-E4014-CON's (ASM-4500) | None | AC1 |
| X2 | An element is named after anything other than a DF-TRT field, or a required element is published optional | The schema validation fails the build | None | AC2 |
| X3 | The template is applied in another service's schema, or a foreign key crosses a schema | The boundary test fails the build; the template creates the table in the applying schema only | None | AC3 |
| X4 | An error body is not a problem document, or a status outside the declared set is returned | The envelope validation fails the build | None | AC4 |
| X5 | A published element is removed, renamed, made required or given a new error status under version 1 | The change raises major version 2 under a new base segment; v1 is never edited in place | None | AC5 |
| X6 | Two documents are published on one base, or a second CON story redefines a frozen element | The registry refuses the change and the drift test fails both builds (ASM-4500) | None | AC5, AC6 |
| X7 | A value the consumers need is fixed by no source — a read operation, a checklist field, a retention rule | The value is not published; the gap stays open and the consuming story works around it | Not specified in the source documents (GAP-2709; ASM-4501) | Sections 12 and 13 |

X1 to X6 are the lint, schema, boundary, envelope, versioning and duplicate-base failures of a contract build; X7 is the boundary this key records, because the source fixes the two operations and the eight fields and nothing more.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a DDL template and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The element order, the example values, the index list and the fake technology are open until v1 is frozen; the base, the create, the element names, the required set, the error set and the versioning rule are fixed |
| Valuable | Unblocks RWB-S3-E4013-APP and the four sibling stories on Day 1 and keeps one claim shape for every later reader |
| Estimable | One OpenAPI document, two schemas, one DDL template, one error set, one versioning rule and one fake set |
| Small | One sprint for the document, the template, the fakes and the drift test |
| Testable | Each criterion of section 7 is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: guarantee-claim resource contract, preparation side

  Background:
    Given the guarantee-claim resource contract document is published with major version 1
    Given the service has one schema, rwb_guarantee, and one login of its own
    Given the contract declares the create of TSD S3 T-A.1 and names the update as RWB-S3-E4014-CON's

  Scenario: AC1 The document publishes the base and the create, and nothing else (new, D-RCV-60)
    Given the OpenAPI document of the guarantee-claim resource
    When it is linted against the platform contract style rules
    Then it declares the server base /api/recovery/guarantee/v1 and no path on the legacy base
    Then it declares POST /cases/{caseId}/guarantee-claims with the request body GuaranteeClaimRequest and the response GuaranteeClaim
    Then it declares no other path: no read, no submit, no TCG channel callback and no delete, and the update that records the filing is named as RWB-S3-E4014-CON's on the same base
    Then the operation declares the capability area "Treatment and offer" with right C, the bearer security scheme and the scope rule
    Then a path outside the base, a third operation on this document, or a changed base fails the lint

  Scenario: AC2 The two schemas carry the DF-TRT elements, the required set and no list member (new, D-RCV-60)
    Given the schema section of the document and its worked example
    When both schemas are validated and the example is checked against them
    Then GuaranteeClaimRequest and GuaranteeClaim are the two object schemas of this resource, with the platform problem schema reused and not redeclared
    Then every element of both schemas is a DF-TRT field name in camelCase, from DF-TRT-015 to DF-TRT-022
    Then claimType, claimDeadline, claimedAmount and status are required and filedAt and paidAmount are optional
    Then caseId is taken from the path on the create and is not repeated in GuaranteeClaimRequest
    Then claimType and status name their list code LOV-CLAIM-TYPE and LOV-CLAIM-STATUS and no member value
    Then no checklist element, no document element, no case status element and no decision-record element is declared
    Then the validation fails on an unknown element, on a missing required element and on a list member written into a schema

  Scenario: AC3 The guarantee_claim DDL template creates the table with the standard columns and no cross-schema key (new, D-RCV-60)
    Given the DDL template of the contract
    When it is applied twice, in two throwaway schemas, through the service's own Flyway sequence
    Then it creates guarantee_claim in the applying schema only, with the primary key on id and each column type as TSD S3 T3.1 states it
    Then it carries the standard columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then case_id is a cross reference with an index and no foreign key, and no other schema is named
    Then claim_type and status keep their list widths and no check constraint repeats a list member
    Then the required elements of AC2 are NOT NULL and the optional ones are nullable
    Then it declares no retention rule, because no source states one
    Then a hand-written table that drifts from the template fails the drift test

  Scenario: AC4 The error set, the problem envelope and the Idempotency-Key are fixed for the create (new, D-RCV-60)
    Given the error section of the document
    When one refused answer per status is validated against it
    Then the create declares 401, 403, 404, 409, 422 and 503
    Then every error body is application/problem+json with type, title, status, detail, instance and the messageId extension
    Then 403 carries MSG-P4-002, 404 carries the unknown case, 409 carries the conflict of a claim already open for the case, 422 carries MSG-GEN-001 with the field name and 503 carries the platform unavailability body
    Then the create declares Idempotency-Key as a required header
    Then an error body that is not a problem document, a create without the header and a success body that is a problem document all fail the validation

  Scenario: AC5 Versioning, one base and one publisher separate a compatible change from a new major version (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element or to the base
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a removed element, a new required element, a renamed element, a new error status or a path change raises major version 2 under a new base segment
    Then v1 is never edited in place and stays readable after v2 is published
    Then the resource has one document per major version on one base, and the update published by RWB-S3-E4014-CON pins the version frozen here
    Then each consuming story pins the published version and a private variant fails its drift test

  Scenario: AC6 The fake answers the document and the drift test catches every difference (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the claim fake, the problem fakes, the template application and the drift test
    Then the claim fake answers a create with 201 and a GuaranteeClaim whose status is PREPARING, and no other operation
    Then it answers a refused create with 403 and 422, an unknown case with 404, a claim already open with 409 and an unavailable service with 503
    Then it returns the first answer for a repeated Idempotency-Key and never a second claim
    Then the template application proves the table twice in two schemas
    Then the drift test fails on any difference between the fake, the template and sections 12 and 13 of the document, and on a second document published on the same base
```

These six criteria are new and test only the contract deliverable. **The four legacy acceptance criteria of RWB-E4-013 stay with RWB-S3-E4013-APP** and are not repeated here, and every identifier, path, entity name, field identifier and status is taken from TSD S3 T-A.1, T-A.2, T3.1 and T3.2, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The guarantee-claim resource is published on one base, `/api/recovery/guarantee/v1`; this story publishes the create and names the update as RWB-S3-E4014-CON's | TSD S3 T-A.1; DP-13; ASM-4500 |
| BR2 | The two schemas of this story are `GuaranteeClaimRequest` and `GuaranteeClaim`, and every element is a DF-TRT field name in camelCase | TSD S3 T-A.2, T3.1 |
| BR3 | The required set is the required column of TSD S3 T3.1: `claimType`, `claimDeadline`, `claimedAmount` and `status`; `filedAt` and `paidAmount` are optional and null at preparation; `caseId` comes from the path on the create | TSD S3 T3.1 |
| BR4 | An enumerated element names its list code and no member, because the members are values in force with their version | TSD S3 T3.2; BR-S3-001 |
| BR5 | The `guarantee_claim` DDL template carries the eight fields of T3.1 with their physical types and the standard columns of T3.0, and creates the table in the applying schema only with no cross-schema key | DP-01; DP-15; TSD S3 T3.0, T3.1 |
| BR6 | The error set is fixed for the create, and every error body is an RFC 9457 problem document that names its `messageId` | TSD S3 T-A.2; platform API style |
| BR7 | The create is idempotent by the `Idempotency-Key` header: a repeated key returns the first answer and creates no second claim | TSD S3 T-A.2; legacy RWB-E4-013 endpoint table |
| BR8 | The create needs Treatment and offer C; the right is declared in the document and checked by the platform guard, and no check is declared in code | TSD S3 T6.1 |
| BR9 | A published element is never edited in place: a compatible change keeps major version 1 and a breaking change raises major version 2 under a new base segment; one resource has one document per major version on one base | Template and Rules §R7.2; §R5.4 class C; ASM-4500 |
| BR10 | The document declares no case status, no decision-record element and no decision code: the status is rwb-case's, the record is the library's and the code is the rule ID and version in force | DP-01; DP-03; ASM-4496 |
| BR11 | The document declares no read operation, no checklist element, no document element and no retention rule, because TSD S3 T-A.1 lists two operations only and no source gives the claim row a checklist field, a document field or a retention rule | GAP-2709; ASM-4501 |
| BR12 | The 409 of the create means the case already has an open claim; its status, its cause and its `messageId` slot are fixed and its business text is not in any source | GAP-2709 |

**Where each rule lives in the target.** BR1 to BR4 are the paths, the schemas and the required set of the document and its lint. BR5 is the DDL template and its boundary test. BR6 is the error section and the platform problem schema it reuses. BR7 is the header rule of the create and the fake's repeated-key answer. BR8 is the `security` section of the operation; the guard is the platform library's and the contract adds no dependency for it. BR9 is the versioning section and the reason the update pins this version rather than redeclaring an element. BR10 and BR11 are the boundaries of this key: the case status and the decision code are not contract values, and the read, the checklist, the document and the retention rule are not published. BR12 is the conflict of the create.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are touched and neither is fixed here.

| Object | State | Meaning in the contract |
|---|---|---|
| GuaranteeClaim | PREPARING | The state a created claim carries in the fake and in the example; the state RWB-S3-E4013-APP writes |
| GuaranteeClaim | FILED, DEFECT, PAID, REJECTED | Named by LOV-CLAIM-STATUS; the document carries them as members of the list in force and fixes none of them |
| GuaranteeClaim | NOT_ELIGIBLE | The hold of R-GUA-02 is a case outcome reported by the stage, not a member of the claim list; the document declares no such element |
| Contract | v1 | The published version every consuming story pins, including the update of RWB-S3-E4014-CON |
| Contract | v2 | Raised by a breaking change under a new base segment; v1 stays readable and is never edited |

The claim journey itself is RWB-S3-E4013-APP's and the sibling stories', and the seventeen rule states of TSD S3 T4 are case statuses of rwb-case that appear nowhere in this document (GAP-2709; ASM-4496). The `state` column is declared as varchar(40) with no check constraint, so a new row state is a data change and not a contract change.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the DDL template and the fakes |
| The service owner of rwb-guarantee | Approves a breaking change and freezes a version |
| The five application stories of this service | Consume the contract, pin the version and raise a change request rather than a private variant |
| RWB-S3-E4014-CON | Publishes the update of the same resource and pins the base, the element naming rule, the required set and the version frozen here |
| The rwb-case owner (P3) | Confirms that no case status and no case table is declared here, and that the stage outcome reaches the case on the signal |
| The rwb-decision owner (P7) | Confirms the rule ID and the rule version as the values a preparation carries, and that no decision code list is published here |
| The rwb-access owner (P4) | Confirms the capability area and the right the create declares |
| The platform API owner | Owns the problem envelope, the style guide and the registry this document validates against |
| RW-GUARANT, RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL and the other roles of TSD S3 T6.1 | Read and create the claim through the operations and hold the rights the document declares; they hold no authoring right here |
| No delegation of authority level applies | A resource contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, the template, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes paths, element names, types, a required set, an error set and list codes; no customer, account or case value appears |
| Shapes published | `GuaranteeClaimRequest` and `GuaranteeClaim` with the DF-TRT-015 to DF-TRT-022 elements, the problem schema reused from the platform, and the `guarantee_claim` DDL template |
| Personal data | None. `id` and `caseId` are identifiers, never a name; no account number, national identifier or document content appears |
| Tables published | `guarantee_claim` only, as a DDL template applied in `rwb_guarantee`; the library object `decision_record` is applied in the same schema under RWB-PLT-E1027-CON and is named, not declared |
| Field identifiers | DF-TRT-015 to DF-TRT-022 as TSD S3 T3.1 lists them, and the standard columns of T3.0 which carry no field identifier; the list codes LOV-CLAIM-STATUS and LOV-CLAIM-TYPE |
| Checklist and documents | Not published: the scheme checklist is an activity output of RWB-S3-E4013-APP and the documents are rwb-document's; no element, table or reference appears here (GAP-2709) |
| Retention | The retention and archive rule of a claim row is Not specified in the source documents (GAP-2709) |

The document is the one place where a business value could leak, so it fixes that a list is named by its code and never by its members, that a case status is not a claim element, and that the examples carry synthetic identifiers of the same kind as the legacy `SYN` values.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This story publishes the create; the update is published by RWB-S3-E4014-CON on the same base (ASM-4500).

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest`; `caseId` from the path | 201 with `GuaranteeClaim` | Treatment and offer C, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |

The operation, its purpose, its request and response entities, its right, its idempotency and its error statuses are those of TSD S3 T-A.1 and T-A.2 for API-S3-001, with the base renamed by DP-13. API-S3-002 is published by RWB-S3-E4014-CON and is named, not declared. No read operation is declared, because TSD S3 T-A.1 lists two operations only (GAP-2709; ASM-4501).

#### 12.2 REST operations consumed

None — a contract document calls no service. The case status reaches the service on the case signal the parent `CaseWorkflow` forwards, and the rule package on `RulePackageInForce`; the rights and the lists arrive through the platform client libraries. Every one of them is a fact of the consuming story, and this contract adds no dependency of its own.

#### 12.3 Events published

None. The service topic is `rwb.guarantee.events.v1` with event names `rwb.guarantee.<Event>.v1` (DP-14), and the ownership rows give S3 no event type, so no event of a preparation is declared here. The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this contract (DP-03).

#### 12.4 Events consumed

None. The package event is consumed by RWB-S3-E4013-APP and never by a document; the contract names no subscription.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity. `GuaranteeClaimWorkflow` is the application story's, on task queue `rwb-guarantee` in namespace `rwb-recovery`, and it calls the create and the server-side service method behind it; the document describes the resource only (Temporal and Drools Design slide 13).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared, and the ownership rows give S3 no job; the claim deadline and the preparation window belong to the application story and to rwb-case.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 | The DDL template of section 13: DF-TRT-015 to DF-TRT-022, the seven standard columns, the primary key on `id`, the index on `case_id` and no cross-schema key (DP-01, DP-15) |
| `decision_record` | `rwb_guarantee` | PLT library object applied in this schema | Named only: the shape is RWB-PLT-E1027-CON's and the row is written in the caller's transaction (DP-03) |

No table of another service is declared, read or keyed, and no checklist, document, case or channel table appears in the template.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Claim resource fake | The create of 12.1 | A 201 create with a `GuaranteeClaim` in state PREPARING; a 403 and a 422 refusal; a 404 for an unknown case; a 409 for a case that already has an open claim; a 503 unavailability |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second claim |
| Template application | The `guarantee_claim` DDL template | The table created twice in two throwaway schemas, with the standard columns, the keys and no cross-schema reference |
| Problem fakes | The problem envelope | One `application/problem+json` body per error status, each with its `messageId` |
| Registry and drift fake | The compatibility and single-publisher rule | One accepted and one refused body in BACKWARD mode, and a drift failure for a private variant of an element or for a second document on the same base |

Every fake answers from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming build rather than as a surprise in SIT.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation on `/api/recovery/guarantee/v1` | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches it through gateway-bff (DP-19) |
| Kafka | 0 | 0 | The service topic is named and no event type is declared here |
| Temporal | 0 | 0 | The contract declares no workflow and no activity |
| File | 0 | 0 | No file crosses the contract; the scheme documents are rwb-document's |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the guarantee-claim resource, the two schemas with the published types in `th.co.scb.ace.workbench.recovery.guarantee.api`, the `guarantee_claim` DDL template as a resource, and the fake set with the drift test. The implementation behind it is RWB-S3-E4013-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2709).

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity | `id`, `caseId` | `id` on the answer; `caseId` from the path |
| Claim | `claimType`, `claimDeadline`, `claimedAmount` | all three |
| Filing and payment | `filedAt`, `paidAmount` | none; null at preparation |
| Lifecycle | `status` | yes |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-TRT field names in camelCase; the mapping is one to one and is checked by the drift test. `GuaranteeClaimRequest` carries the create body without `id`, `filedAt`, `paidAmount` and `status`; `GuaranteeClaim` carries all eight fields. `GuaranteeClaimUpdate` is RWB-S3-E4014-CON's and appears here only as a name (ASM-4500).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the writer and declares no record element | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/guarantee/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the claim carries only its own eight fields. DP-19 is the route SCR-17 uses and is the platform edge story's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GuaranteeClaimOpenApi | Document | The base, the create, the schemas, the security, the error set and the versioning section (BR1 to BR4, BR6, BR9) |
| GuaranteeClaimSchema | Published schema | The two schemas with the DF-TRT elements and the required set (BR2, BR3) |
| GuaranteeClaimDdlTemplate | Resource | The `guarantee_claim` DDL: columns, types, keys, indexes and standard columns (BR5) |
| ProblemEnvelope | Reused schema | The platform RFC 9457 problem document with the `messageId` extension (BR6) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and the 409 cause (BR7, BR12) |
| Fake set and fixtures | Test asset | The create, the refusals, the conflict, the unavailable and the repeated-key answers used by every consuming build (AC6) |
| DriftTest | Test asset | The comparison of a consuming build against sections 12 and 13 (BR9, AC6) |

**Database.** The template creates `guarantee_claim` in `rwb_guarantee` only, with the physical types of TSD S3 T3.1 and the standard columns of T3.0. `case_id` is a cross reference with an index and no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15).

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR4). The capability area and the right are declared per operation and their role lists are rwb-access data (BR8). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the create; lint the path and the right, and refuse a third operation and a legacy-base path (AC1).
2. Write the two schemas with the element mapping, the required set, the enumeration rule and the example; validate the example (AC2).
3. Write the DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key (AC3).
4. Write the error section with the problem envelope and the message identifiers, the `Idempotency-Key` rule and the 409 cause (AC4).
5. Write the versioning and pinning section with one compatible and one breaking example, and record that the update pins this version (AC5).
6. Generate the fake set and the drift test, and wire the drift test into the build of RWB-S3-E4013-APP, of the four sibling stories and of RWB-S3-E4014-CON (AC6).
7. Publish v1 and record the pinned version of this contract and of each consuming story (AC5).

**Feature flag.** `rwb.guarantee.claim-resource-contract`.

**Done when.** The document lints, the two schemas validate, the template applies twice, the fake answers every status including the conflict and the repeated key, the drift test is green on the build of this story, of RWB-S3-E4013-APP and of RWB-S3-E4014-CON, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not hold the right of the operation | You cannot {action} here. Your role does not include it. | 403, problem body with `messageId` MSG-P4-002 |
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. | 422, problem body with `messageId` MSG-GEN-001 and `field` |
| MSG-P7-003 | The preparation cannot be recorded and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | Problem body of the create with `messageId` MSG-P7-003; the source fixes its text and no status beside it |

The texts are the legacy and platform texts carried unchanged, and this contract adds no message identifier of its own. The 401 carries the platform authentication problem and no business message; the 404 names the unknown case; the 409 of a case that already has an open claim is fixed by its status, its cause and its `messageId` slot, and its business text is not stated in any source read for this key (GAP-2709). The 503 carries the platform unavailability body; no module message names it for this key. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: it publishes a resource. SCR-17 Guarantee claim (Not due; due; submitted; paid; refused) is reached through the gateway-bff composite route, which calls this resource and the case read in one hop each (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this contract fixes only the elements the create returns. Because TSD S3 T-A.1 declares no read operation, the `Not due` and `due` states are composed from the create answer and the case read, and the open question is recorded once (GAP-2709; ASM-4501).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S3-E4013-CON-01 | AC1 | Contract | The document linted: the base, the create, the right, the bearer scheme, and a third operation, a read path and a legacy-base path refused |
| TC-S3-E4013-CON-02 | AC2 | Contract | The two schemas validated against the DF-TRT elements, the required set, the list codes and the example; an unknown element, a missing required element and a list member refused |
| TC-S3-E4013-CON-03 | AC3 | Component | The template applied in two throwaway schemas; the standard columns, the types, the keys, the widths and the absence of a cross-schema key asserted; a drifted hand-written table refused |
| TC-S3-E4013-CON-04 | AC4 | Contract | One problem body per status on the create, the message identifiers, the 409 cause, the `Idempotency-Key` header required and refused absent |
| TC-S3-E4013-CON-05 | AC5, AC6 | Component | A compatible and a breaking change against the registry fake; a second document on the same base refused; the fake answering the create, refusal, conflict, unavailable and repeated-key answers; the drift test on a consuming build |

The legacy test set TC-E4-013-01 to TC-E4-013-06 is carried by RWB-S3-E4013-APP and by the wave 3 integration harness, and these five are the contract's own tests; no legacy id is renumbered here.

### 17. Guardrails

- No business value in the contract: the list members, the row states, the rights and the message texts are values in force, and the document names their codes only (BR4).
- No personal data in a schema, an example, a fake or a log: `id` and `caseId` are identifiers, and the personal-data scan fails the build otherwise.
- No cross-schema reference in the template and no foreign key across services: `case_id` is a cross reference, and the boundary test fails the build.
- No case status, no case table and no case column in any schema of this resource (BR10; DP-01).
- No decision-record element and no decision code list: the record is the library's and the code is the rule ID and version in force (DP-03).
- No checklist element, no document element and no retention rule, because no source gives them (BR11; GAP-2709).
- No read operation and no path outside the base: a GET, a submit path and a channel callback are named as out of scope and never declared.
- One resource, one document per major version on one base: a second document on the same base fails the registry and the drift test (BR9; ASM-4500).
- A published version is never edited in place: a breaking change raises major version 2 under a new base segment with a migration note (BR9).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S3-001 | A guarantee claim is prepared from case data and submitted inside the guarantor's deadline | Business Requirements Program v4, section 5.10 | FEAT-GUA-01 | 07 Route, settle and claim | BR1 to BR12; DP-13 | TC-S3-E4013-CON-01 to TC-S3-E4013-CON-05 |
| REQ-S3-002 | Claim status, payment and any shortfall are recorded on the case | Business Requirements Program v4, section 5.10 | FEAT-GUA-01 | 07 Route, settle and claim | BR2; BR5 | TC-S3-E4013-CON-02, TC-S3-E4013-CON-03 |
| Legacy test set RWB-E4-013 | TC-E4-013-01, TC-E4-013-02, TC-E4-013-03, TC-E4-013-04, TC-E4-013-05, TC-E4-013-06 | Business Requirements Program v4, section 5.10 | FEAT-GUA-01 | 07 Route, settle and claim | R-GUA-01; R-GUA-04 | Executed by RWB-S3-E4013-APP and the wave 3 harness; not owned here |

TSD S3 T8 maps the module's requirements to FEAT-GUA-01 as the "written one epic ahead" placeholder; the feature code FEAT-GUA-01 of FSD S3 A2.1 is carried alongside until the C1 PRD settles the mapping.

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4013-APP | App development | H consumer: implements the create, the checklist, the claim write and the stage against this contract and its fake |
| RWB-S3-E4014-CON | Contract | Co-publisher on the same base: publishes the update that records the filing and pins the version frozen here (ASM-4500) |
| RWB-S3-E4014-APP, RWB-S3-E4015-APP, RWB-S3-E4016-APP, RWB-S3-E4017-APP | App development | Siblings: they read the same resource and declare no path of their own |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library the preparation writes through |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route the SCR-17 screen uses |
| RWB-PLT-E1044-CON | Contract | Referred to: the per-service Flyway sequence that applies the DDL template |
| P3 rwb-case | Service | Referred to: the case of record, the case signal and the status this resource never carries |
| P5 rwb-document | Service | Referred to: the scheme documents, which the resource does not carry |
| P7 rwb-decision | Service | Referred to: the `GUA` rule rows and the rule versions a preparation records |
| RWB-ITG-W3 | Integration | The end-to-end proof of the resource against the live owners, held by the wave 3 harness |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the workflow branch, the checklist activity and the claim write: RWB-S3-E4013-APP.
- The update that records the filing, its `GuaranteeClaimUpdate` schema and its 409 cause: RWB-S3-E4014-CON; the approval and submission behind it: RWB-S3-E4014-APP.
- The tracking of the claim to payment and the lost claim: RWB-S3-E4015-APP.
- The subrogation position and the closing of the guarantee: RWB-S3-E4016-APP.
- The guarantor and co-borrower notices: RWB-S3-E4017-APP.
- The case status, the case signal and the case table: rwb-case (P3).
- The central decision ledger, the `GUA` rule rows and their approval: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data themselves: rwb-access (P4).
- The scheme checklist and the guarantee documents: RWB-S3-E4013-APP and rwb-document (P5); no element or table is published for them.
- A read operation on the resource, until a source names one: GAP-2709 and ASM-4501.
- A retention and archive rule for a claim row: not stated in any source (GAP-2709).
- The gateway-bff composite route, the screen field list and the layout of SCR-17: the platform edge story and the screen owner (DP-19).
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof of the resource against the live owners: the wave 3 integration harness.
