# RWB-S3-E4020-CON File an insurance claim on a collateral event - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the contract slice split from RWB-E4-020 for rwb-guarantee (S3). The guarantee-claim resource is republished on base `/api/recovery/guarantee/v1` (DP-13) with the collateral-event branch of its two operations, the three schemas with the collateral and appraisal elements, the `guarantee_claim` DDL template, the error set, the versioning rule and the fakes; the two legacy acceptance criteria stay with RWB-S3-E4020-APP and every criterion here is new. The resource is reached through the gateway-bff composite route for SCR-17 (DP-19). No source gives the collateral event, the collateral key or the appraisal a field identifier (GAP-2737; ASM-4549), gives the claim a deadline or amount source for this claim type (GAP-2737; ASM-4543) or gives the 409 of an already filed claim a business text (GAP-2737). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S3-E4020-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S3-E4020-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-020 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

### 1. Story

As a **service contract owner**, I want **the published contract of the collateral-event branch of the guarantee-claim resource of rwb-guarantee (S3) — the base `/api/recovery/guarantee/v1`, `POST /cases/{caseId}/guarantee-claims` and `PATCH /guarantee-claims/{claimId}` with the entities `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` of TSD S3 T-A.2, the eight `guarantee_claim` fields named in camelCase after DF-TRT-015 to DF-TRT-022, the collateral and appraisal elements the branch needs, the `guarantee_claim` DDL template with the T3.0 standard columns, the error set 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body, the `Idempotency-Key` rule, the versioning rule and the fakes** instead of the monolith's in-process controller and its one `recovery.guarantee_claim` table of the shared schema, so that **RWB-S3-E4020-APP and every later story of the service build against one frozen shape from Day 1, with no wait on any other team**.

This story owns the contract of one branch of one resource and nothing else:

- the OpenAPI 3.1 document of the guarantee-claim resource for the collateral-insurance branch: the base, the two operations, the three object schemas, the problem schema, the security and the error set;
- the collateral and appraisal elements the branch publishes: the collateral key, the collateral type and value, the appraisal number, the appraised value and the appraisal date, as optional elements of the create and of the answer;
- the `guarantee_claim` DDL template with the eight fields of TSD S3 T3.1 and the seven standard columns of T3.0, one template each environment applies in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-TRT and DF-ACE identifiers), the required set and the enumeration rule that names a list code and no member;
- the `Idempotency-Key` rule on the POST, the compatibility rule and the pinning rule;
- the fake set generated from the document, and the drift test that every consuming build runs.

It does not own: the handlers, the workflow branch, the collateral read, the filing write and the case report, which are RWB-S3-E4020-APP; the TCG claim preparation and submission, which are FEAT-GUA-01 and FEAT-GUA-02 (RWB-E4-013 and RWB-E4-014); the tracking to payment, which is FEAT-GUA-03; the subrogation position, which is FEAT-GUA-04; the case status and the case signal, which are rwb-case's; the appraisal order and the SVAF exchange, which are rwb-valuation's; the X7 deviation, which is rwb-deviation's; the central ledger and the `GUA` rule rows, which are P7's; the roles and rights data, which are rwb-access's; the composite route, which is the platform edge story's; any insurer interface, which no source publishes.

### 2. Business rationale

The monolith exposed the claim through one controller in the shared process on the legacy base, and the claim row lived in the one `recovery` schema beside 91 other tables (TSD S3 T2, T3.1). Four facts follow from the target and make a contract necessary before any code. First, the schema is now `rwb_guarantee` with its own login and no cross-schema access, so the table shape has to be a template every environment applies rather than one shared migration (DP-01, DP-02, DP-15). Second, the base is now `/api/recovery/guarantee/v1`, so the claim paths no longer collide with the case, the payment and the treatment services (DP-13). Third, the collateral-insurance claim of FEAT-GUA-08 needs elements the eight row fields do not carry — the collateral it is filed on, the appraisal it is filed against — so the branch's element set has to be frozen before the story that reads and writes it starts. Fourth, five stories of this service and the reporting build read a claim, so the error set and the required set have to be one shape.

TSD S3 already fixes most of it, and this story publishes what the source states rather than inventing: T-A.1 names the two paths, their rights and the first epic; T-A.2 names the request, the update and the response entities with the error statuses and the `Idempotency-Key` header on the create; T3.1 names the eight fields of `guarantee_claim` with their physical types, their required flag and their list; T3.0 names the standard record columns; T3.2 names the members of LOV-CLAIM-STATUS and LOV-CLAIM-TYPE, `COLLATERAL_INSURANCE` among them. The legacy story contributes the collateral, collateral-detail and valuation rows of its Data table, which are the elements the branch adds.

What the source does not state is recorded, not filled. The collateral and appraisal elements have no field identifier and no published shape, so v1 publishes them as optional elements whose names follow the legacy column names and whose identifiers wait for the data model (GAP-2737; ASM-4549). The claim deadline and the claimed amount are required fields of the row and no source states where a collateral-insurance claim takes them, so the document declares them required, as T3.1 does, and fixes no basis (GAP-2737; ASM-4543). The 409 cause of a claim already filed has a status here and no business text (GAP-2737).

The fake is the Day-1 unblocker. RWB-S3-E4020-APP and the four sibling stories can create, read and update a claim — a collateral-insurance claim among them — before a single table exists in an environment, and the drift test turns a private variant of the shape into a build failure rather than a defect found in SIT.

### 3. Preconditions

- TSD S3 T-A.1 fixes the endpoint inventory: API-S3-001 `POST` on `/cases/{caseId}/guarantee-claims` with right C and the `Idempotency-Key` header, and API-S3-002 `PATCH` on `/guarantee-claims/{claimId}` with right U and idempotency not applicable; the base becomes `/api/recovery/guarantee/v1` by DP-13.
- TSD S3 T-A.2 fixes the entity names `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` and the error statuses 401, 403, 404, 409, 422 and 503 of both operations.
- TSD S3 T3.1 fixes DF-TRT-015 to DF-TRT-022 with their physical types, their required flags and their lists, and T3.0 fixes the seven standard record columns.
- TSD S3 T3.2 fixes the list codes LOV-CLAIM-STATUS and LOV-CLAIM-TYPE, whose members include `COLLATERAL_INSURANCE`; the members are values in force and are not restated in the document (BR-S3-008).
- TSD S3 T6.1 fixes the capability area "Treatment and offer" and the rights of each role; the document declares the right of each operation and holds no role list.
- The problem envelope is the platform one, RFC 9457 `application/problem+json` with the platform extension members; the platform API style guide fixes its member names, so this document reuses them and does not redeclare them.
- RWB-PLT-E1027-CON publishes the decision-record contract; this document names it as the writer behind the decision of a filing and declares no record element of its own (DP-03).
- RWB-PLT-E1044-CON publishes the per-service Flyway conventions, so the DDL is a template applied by this service's own sequence and not one shared migration (DP-15).
- No source gives the collateral event, the collateral key or the appraisal a field identifier, the claim a deadline basis, or the 409 a business text; all three are recorded once (GAP-2737; ASM-4543; ASM-4549).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), it sits in contract group CG-W3 and it is published at status Draft (realignment v1) (ASM-4548).

### 4. Flow

1. The contract author fixes the base and the two operations of section 12.1, taken character for character from TSD S3 T-A.1 with the DP-13 base.
2. The author fixes the element naming rule: every element of the three schemas is a DF-TRT field name, or a collateral or appraisal name from the legacy Data table of the key, in camelCase; `caseId` is taken from the path on the POST and is not repeated in the request body.
3. The author fixes the required set from the required column of TSD S3 T3.1, so `id`, `caseId`, `claimType`, `claimDeadline`, `claimedAmount` and `status` are required and `filedAt` and `paidAmount` are optional; the collateral and appraisal elements are optional and carry no default.
4. The author fixes the enumeration rule: an enumerated element names its list code and no member, because the members are values in force (BR-S3-008).
5. The author writes the `guarantee_claim` DDL template: the columns, the physical types, the required set, the primary key, the indexes, the standard columns and the rule that no key crosses a schema.
6. The author writes the error set of each operation with the problem envelope and the message identifiers the platform catalogue already holds, the `Idempotency-Key` rule of the POST and the 409 cause of a claim already filed.
7. The author writes the versioning and pinning section: a compatible change keeps major version 1, a breaking change raises major version 2 under a new base segment, and v1 is never edited in place.
8. The lint and schema steps run: the document linted against the platform style, every example validated against its schema, the personal-data scan run on the examples, and the template applied twice in two throwaway schemas.
9. The fake set is generated from the document: the collateral-insurance create, the filing, the read answer, one refused answer per error status, the repeated-key answer and the unavailable answer, all from one example set.
10. The drift test is generated and wired into the build of RWB-S3-E4020-APP and of the four sibling application stories.
11. The document and the fakes are published at v1, and the pinned version of this contract and of each consuming story is recorded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A path outside `/api/recovery/guarantee/v1`, or a third operation such as a collateral-event callback or an insurer submit, is added to the document | The lint fails the build; the base and the two operations are fixed (DP-13) | None | AC1 |
| X2 | An element is named after anything other than a DF-TRT, a collateral or an appraisal name, or a required element is published optional | The schema validation fails the build | None | AC2 |
| X3 | The template is applied in another service's schema, or a foreign key crosses a schema | The boundary test fails the build; the template creates the table in the applying schema only | None | AC3 |
| X4 | An error body is not a problem document, or a status outside the declared set is returned | The envelope validation fails the build | None | AC4 |
| X5 | A published element is removed, renamed, made required or given a new error status under version 1 | The change raises major version 2 under a new base segment; v1 is never edited in place | None | AC5 |
| X6 | A consuming build ships without the drift test, or ships a private variant of an element | The registry refuses the change and the drift test fails the build | None | AC6 |
| X7 | A value the consumers need is fixed by no source — the field identifiers of the collateral elements, the deadline basis and the 409 text | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2737; ASM-4549) | Sections 12 and 13 |

X1 to X6 are the lint, schema, boundary, envelope, versioning and drift failures of a contract build; X7 is the boundary this key records, because the source fixes the two operations and the eight row fields and names the collateral only in the legacy Data table.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a DDL template and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The element order, the example values, the index list and the fake technology are open until v1 is frozen; the base, the two operations, the element names, the required set, the error set and the versioning rule are fixed |
| Valuable | Unblocks RWB-S3-E4020-APP and four sibling stories on Day 1 and keeps one claim shape, with the collateral branch inside it, for every later reader |
| Estimable | One OpenAPI document, three schemas, one DDL template, one error set, one versioning rule and one fake set |
| Small | One sprint for the document, the template, the fakes and the drift test |
| Testable | Each criterion of section 7 is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: collateral-event branch of the guarantee-claim resource contract

  Background:
    Given the guarantee-claim resource contract document is published with major version 1
    Given the service has one schema, rwb_guarantee, and one login of its own
    Given the contract declares the two operations of TSD S3 T-A.1 and nothing more

  Scenario: AC1 The document publishes the base, the two operations and the collateral-insurance branch, and nothing else (new, D-RCV-60)
    Given the OpenAPI document of the guarantee-claim resource
    When it is linted against the platform contract style rules
    Then it declares the server base /api/recovery/guarantee/v1 and no path on the legacy base
    Then it declares POST /cases/{caseId}/guarantee-claims with the request body GuaranteeClaimRequest and the response GuaranteeClaim
    Then it declares PATCH /guarantee-claims/{claimId} with the request body GuaranteeClaimUpdate and the response GuaranteeClaim
    Then it declares no other path: no collateral-event callback, no insurer submit, no delete and no read operation of a sibling resource
    Then each operation declares the capability area "Treatment and offer" with right C on the POST and right U on the PATCH, the bearer security scheme and the scope rule
    Then a path outside the base, or a third operation, fails the lint

  Scenario: AC2 The three schemas carry the DF-TRT elements, the collateral and appraisal elements, the required set and no list member (new, D-RCV-60)
    Given the schema section of the document and its worked example
    When both schemas are validated and the example is checked against them
    Then GuaranteeClaimRequest, GuaranteeClaimUpdate and GuaranteeClaim are the three object schemas of this resource, with the platform problem schema reused and not redeclared
    Then every claim element of the three schemas is a DF-TRT field name in camelCase, from DF-TRT-015 to DF-TRT-022
    Then the collateral and appraisal elements are optional and are the collateral key, the collateral type, the collateral value, the appraisal number, the appraised value and the appraisal date
    Then id, caseId, claimType, claimDeadline, claimedAmount and status are required and filedAt and paidAmount are optional
    Then caseId is taken from the path on the POST and is not repeated in GuaranteeClaimRequest
    Then claimType and status name their list code LOV-CLAIM-TYPE and LOV-CLAIM-STATUS and no member value
    Then no deviation element, no case status element, no document element and no insurer element is declared
    Then the validation fails on an unknown element, on a missing required element and on a list member written into a schema

  Scenario: AC3 The guarantee_claim DDL template creates the table with the standard columns and no cross-schema key (new, D-RCV-60)
    Given the DDL template of the contract
    When it is applied twice, in two throwaway schemas, through the service's own Flyway sequence
    Then it creates guarantee_claim in the applying schema only, with the primary key on id and each column type as TSD S3 T3.1 states it
    Then it carries the standard columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then case_id is a cross reference with an index and no foreign key, and no other schema is named
    Then claim_type and status keep their list widths and no check constraint repeats a list member
    Then the required elements of AC2 are NOT NULL, the optional ones are nullable, and no column is created for a collateral or appraisal element
    Then a hand-written table that drifts from the template fails the drift test

  Scenario: AC4 The error set, the problem envelope, the Idempotency-Key and the 409 cause are fixed (new, D-RCV-60)
    Given the error section of the document
    When one refused answer per status is validated against it
    Then both operations declare 401, 403, 404, 409, 422 and 503
    Then every error body is application/problem+json with type, title, status, detail, instance and the messageId extension
    Then 403 carries MSG-P4-002, 404 carries the unknown claim or case, 409 carries the conflict of a claim already in FILED, 422 carries MSG-GEN-001 with the field name and 503 carries MSG-GEN-006
    Then the POST declares Idempotency-Key as a required header and the PATCH declares it not applicable
    Then an error body that is not a problem document, a POST without the header and a success body that is a problem document all fail the validation

  Scenario: AC5 Versioning separates a compatible change from a new major version, and the consumer pins (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a removed element, a new required element, a renamed element, a new error status or a path change raises major version 2 under a new base segment
    Then v1 is never edited in place and stays readable after v2 is published
    Then each consuming story pins the published version and a private variant fails its drift test
    Then the document records the version pinned by RWB-S3-E4020-APP

  Scenario: AC6 The fake answers the document and the drift test catches every difference (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the claim fake, the collateral answer, the problem fakes, the template application and the drift test
    Then the claim fake answers a collateral-insurance create with 201 and a GuaranteeClaim whose status is PREPARING, a filing with 200 and the same claim in FILED, and no other operation
    Then the answer carries the collateral key, the appraised value and the appraisal date it was given, and carries none of them when the create omitted them
    Then it answers a refused create with 403 and 422, an unknown claim with 404, an already filed claim with 409 and an unavailable service with 503
    Then it returns the first answer for a repeated Idempotency-Key and never a second claim
    Then the template application proves the table twice in two schemas
    Then the drift test fails on any difference between the fake, the template and sections 12 and 13 of the document
```

These six criteria are new and test only the contract deliverable. **The two legacy acceptance criteria of RWB-E4-020 stay with RWB-S3-E4020-APP** and are not repeated here, and every identifier, path, entity name, field identifier and status is taken from TSD S3 T-A.1, T-A.2, T3.1 and T3.2, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The guarantee-claim resource is published on one base, `/api/recovery/guarantee/v1`, with exactly two operations: the create and the update | TSD S3 T-A.1; DP-13 |
| BR2 | The three schemas are `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim`, every claim element is a DF-TRT field name in camelCase, and every collateral element is a legacy collateral or appraisal name in camelCase | TSD S3 T-A.2, T3.1; legacy RWB-E4-020 Data table |
| BR3 | The required set is the required column of TSD S3 T3.1: `id`, `caseId`, `claimType`, `claimDeadline`, `claimedAmount` and `status`; `filedAt`, `paidAmount` and the collateral elements are optional; `caseId` comes from the path on the POST | TSD S3 T3.1 |
| BR4 | An enumerated element names its list code and no member, because the members are values in force with their version | TSD S3 T3.2; BR-S3-008 |
| BR5 | The `guarantee_claim` DDL template carries the eight fields of T3.1 with their physical types and the standard columns of T3.0, and creates the table in the applying schema only with no cross-schema key | DP-01; DP-15; TSD S3 T3.0, T3.1 |
| BR6 | The error set is fixed per operation, and every error body is an RFC 9457 problem document that names its `messageId` | TSD S3 T-A.2; platform API style |
| BR7 | The create is idempotent by the `Idempotency-Key` header: a repeated key returns the first answer and creates no second claim | TSD S3 T-A.2; legacy RWB-E4-020 endpoint table |
| BR8 | The create needs Treatment and offer C and the update needs Treatment and offer U; the right is declared in the document and checked by the platform guard, and no check is declared in code | TSD S3 T6.1 |
| BR9 | A published element is never edited in place: a compatible change keeps major version 1 and a breaking change raises major version 2 under a new base segment | Template and Rules §R7.2; §R5.4 class C |
| BR10 | The document declares no case status, no deviation element and no decision-record element: the status is rwb-case's, X7 is rwb-deviation's and the record is the library's | DP-01; DP-03; ASM-4547 |
| BR11 | The document declares no insurer operation, no SVAF operation and no appraisal order, because no source publishes an interface for any of them and INT-29 is TCG only | TSD S3 T5.1; GAP-2737 |
| BR12 | The collateral and appraisal elements are published optional with no field identifier and no default, and the claim deadline and claimed amount are required with no basis fixed, because no source states either | GAP-2737; ASM-4543; ASM-4549 |
| BR13 | The 409 of the update means the claim is already in `FILED`; its status, its cause and its `messageId` slot are fixed and its business text is not in any source | GAP-2737 |

**Where each rule lives in the target.** BR1 to BR4 are the paths, the schemas and the required set of the document and its lint. BR5 is the DDL template and its boundary test. BR6 is the error section and the platform problem schema it reuses. BR7 is the header rule of the POST and the fake's repeated-key answer. BR8 is the `security` section of each operation; the guard is the platform library's and the contract adds no dependency for it. BR9 is the versioning section. BR10, BR11, BR12 and BR13 are the four boundaries of this key: the case status, the deviation and the record are not contract values; no insurer, SVAF or appraisal operation is published; the collateral elements are optional placeholders until the data model names them; and the 409 is a status with a cause and no text.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are touched and neither is fixed here.

| Object | State | Meaning in the contract |
|---|---|---|
| GuaranteeClaim | PREPARING | The state a created collateral-insurance claim carries in the fake and in the example |
| GuaranteeClaim | FILED | The state the update returns after the filing; the state RWB-S3-E4020-APP writes |
| GuaranteeClaim | DEFECT, PAID, REJECTED | Named by LOV-CLAIM-STATUS; the document carries them as members of the list in force and fixes none of them |
| Contract | v1 | The published version every consuming story pins |
| Contract | v2 | Raised by a breaking change under a new base segment; v1 stays readable and is never edited |

The claim journey is RWB-S3-E4020-APP's and the sibling stories', the X7 states of R-DEV-01 to R-DEV-22 are rwb-deviation's, and the case states of R-LIT-79 are rwb-case's; none of them appears in this document (BR10; ASM-4547). The `state` column is declared as varchar(40) with no check constraint, so a new row state is a data change and not a contract change.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the DDL template and the fakes |
| The service owner of rwb-guarantee | Approves a breaking change and freezes a version |
| The five application stories of this service | Consume the contract, pin the version and raise a change request rather than a private variant |
| The rwb-source-data owner (P1) | Confirms that no collateral, appraisal or account element is published as a copy of a `v_ace_*` field and that the read stays on the owner's contract |
| The rwb-case owner (P3) | Confirms that no case status and no case table is declared here, and that the stage outcome reaches the case on the signal |
| The rwb-valuation owner (S1) | Confirms that no appraisal operation is declared here and that the re-appraisal is ordered from the case |
| The rwb-decision owner (P7) | Confirms the rule ID and the rule version as the values a filing carries, and that no decision code list is published here |
| The rwb-access owner (P4) | Confirms the capability area and the rights the two operations declare |
| The platform API owner | Owns the problem envelope, the style guide and the registry this document validates against |
| RW-CASEOWN, RW-GUARANT, RW-RESTRUCT, RW-SPECIAL and the other roles of TSD S3 T6.1 | Read and update the claim through the two operations and hold the rights the document declares; they hold no authoring right here |
| An insurer and SVAF | Receive the officer's filing and the appraisal outside the Workbench; they hold no right and appear in no schema |

No personal name, no email address and no credential appears in the document, the template, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes paths, element names, types, a required set, an error set and list codes; no customer, account, collateral or case value appears |
| Shapes published | `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` with the DF-TRT-015 to DF-TRT-022 elements and the optional collateral and appraisal elements, the problem schema reused from the platform, and the `guarantee_claim` DDL template |
| Personal data | None. `id` and `caseId` are identifiers, never a name; no account number, national identifier, owner name or document content appears, and the collateral is published by key and value only |
| Tables published | `guarantee_claim` only, as a DDL template applied in `rwb_guarantee`; the library object `decision_record` is applied in the same schema under RWB-PLT-E1027-CON and is named, not declared |
| Field identifiers | DF-TRT-015 to DF-TRT-022 as TSD S3 T3.1 lists them, the standard columns of T3.0 which carry no field identifier, and the list codes LOV-CLAIM-STATUS and LOV-CLAIM-TYPE. The collateral, collateral-detail and valuation fields of the legacy Data table have no field identifier in this service and are published as elements (GAP-2737; ASM-4549) |
| Retention | The retention and archive rule of a claim row is Not specified in the source documents (GAP-2737; ASM-4543) |

The document is the one place where a business value could leak, so it fixes that a list is named by its code and never by its members, that a case status and a deviation code are not claim elements, and that the examples carry synthetic identifiers of the same kind as the legacy `SYN` values.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This story publishes both operations with the collateral-event branch inside them.

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest`; `caseId` from the path; the collateral and appraisal elements optional | 201 with `GuaranteeClaim` | Treatment and offer C, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` | 200 with `GuaranteeClaim` | Treatment and offer U, scope applied | Not applicable | 401, 403, 404, 409, 422, 503 |

The two operations and their purpose, request and response entities, access rights, idempotency and error statuses are those of TSD S3 T-A.1 and T-A.2 for API-S3-001 and API-S3-002, with the base renamed by DP-13. No third operation is declared: the filing itself is the update, and no collateral-event callback, insurer submit or appraisal order exists, because no source publishes one (GAP-2737; BR11).

#### 12.2 REST operations consumed

None — a contract document calls no service. The collateral and appraisal facts reach the consuming story through rwb-source-data's contract, the case status reaches it on the case signal that Architecture v5 slide 13 shows as a Temporal edge, and the rights and the lists arrive through the platform client libraries. Every one of them is a fact of the consuming story, and this contract adds no dependency of its own.

#### 12.3 Events published

None. The service topic is `rwb.guarantee.events.v1` with event names `rwb.guarantee.<Event>.v1` (DP-14), and the ownership rows give S3 no event type, so no event of a collateral-insurance claim is declared here. The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this contract (DP-03).

#### 12.4 Events consumed

None. The rule-package event is consumed by RWB-S3-E4020-APP and never by a document; the collateral event reaches the story on the case signal and never on a topic; the contract names no subscription.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity. `GuaranteeClaimWorkflow` is the application story's, on task queue `rwb-guarantee` in namespace `rwb-recovery`, and it calls the two operations and the server-side service method behind them; the document describes the resource only (Temporal and Drools Design slide 13).

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared, and the ownership rows give S3 no job; the claim clock and the 10 working days of R-LIT-79 belong to the sibling stories and to rwb-case.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 | The DDL template of section 13: DF-TRT-015 to DF-TRT-022, the seven standard columns, the primary key on `id`, the index on `case_id` and no cross-schema key (DP-01, DP-15) |
| `decision_record` | `rwb_guarantee` | PLT library object applied in this schema | Named only: the shape is RWB-PLT-E1027-CON's and the row is written in the caller's transaction (DP-03) |

No table of another service is declared, read or keyed, and no `v_ace_*` view, deviation table, document table or case table appears in the template.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Claim resource fake | The two operations of 12.1 | A 201 collateral-insurance create with a `GuaranteeClaim` in state PREPARING; a 200 filing of the same claim in FILED; a 403 and a 422 refusal; a 404 for an unknown ID; a 409 for a claim already filed; a 503 unavailability |
| Collateral answer fake | The optional collateral and appraisal elements | A create with all six elements, a create with none of them, and an answer that returns exactly the elements it was given |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second claim |
| Template application | The `guarantee_claim` DDL template | The table created twice in two throwaway schemas, with the standard columns, the keys and no cross-schema reference |
| Problem fakes | The problem envelope | One `application/problem+json` body per error status, each with its `messageId` |
| Registry and drift fake | The compatibility rule | One accepted and one refused body in BACKWARD mode, and a drift failure for a private variant of an element |

Every fake answers from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming build rather than as a surprise in SIT.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/guarantee/v1` | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches them through gateway-bff (DP-19) |
| Kafka | 0 | 0 | The service topic is named and no event type is declared here |
| Temporal | 0 | 0 | The contract declares no workflow and no activity |
| File | 0 | 0 | No file crosses the contract; no insurer and no SVAF channel exists |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the guarantee-claim resource with the collateral-event branch, the three schemas with the published types in `th.co.scb.ace.workbench.recovery.guarantee.api`, the `guarantee_claim` DDL template as a resource, and the fake set with the drift test. The implementation behind it is RWB-S3-E4020-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2737; ASM-4549).

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity | `id`, `caseId` | both |
| Claim | `claimType`, `claimDeadline`, `claimedAmount` | all three |
| Collateral | `collateralNo`, `collateralType`, `collateralValue` | none; optional, no default |
| Appraisal | `appraisalNo`, `appraisedValue`, `appraisalDate` | none; optional, no default |
| Filing and payment | `filedAt`, `paidAmount` | none |
| Lifecycle | `status` | yes |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The claim element names are the DF-TRT field names in camelCase and the collateral names follow the legacy columns `collateral_no`, `collateral_type`, `collateral_value`, `appraisal_no`, `appraised_value` and `appraisal_date` of the Data table of the key; the mapping is one to one and is checked by the drift test. `GuaranteeClaimRequest` carries the create body without `id`, `filedAt`, `paidAmount` and `status`; `GuaranteeClaimUpdate` carries the filing, that is `status` and `filedAt`, and no other element, because the source gives the row no other field for a filing (GAP-2737; ASM-4543).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the writer and declares no record element | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The service's own ACE views or the owner's contract; the resource declares no ACE field as its own | referred to; the consuming story carries the read |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/guarantee/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the claim carries only its own fields. DP-05 is the read the application story performs through rwb-source-data; the resource publishes the collateral key and value as claim elements and copies no view field as its own (ASM-4545). DP-19 is the route SCR-17 uses and is the platform edge story's.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| GuaranteeClaimOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR4, BR6, BR9) |
| GuaranteeClaimSchema | Published schema | The three schemas with the DF-TRT elements, the collateral elements and the required set (BR2, BR3) |
| GuaranteeClaimDdlTemplate | Resource | The `guarantee_claim` DDL: columns, types, keys, indexes and standard columns (BR5) |
| ProblemEnvelope | Reused schema | The platform RFC 9457 problem document with the `messageId` extension (BR6) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and the 409 cause (BR7, BR13) |
| Fake set and fixtures | Test asset | The create, filing, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC6) |
| DriftTest | Test asset | The comparison of a consuming build against sections 12 and 13 (BR9, AC6) |

**Database.** The template creates `guarantee_claim` in `rwb_guarantee` only, with the physical types of TSD S3 T3.1 and the standard columns of T3.0. `case_id` is a cross reference with an index and no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15).

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR4). The capability area and the rights are declared per operation and their role lists are rwb-access data (BR8). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared. The collateral and appraisal element names are placeholder names until the data owner allocates field identifiers (BR12).

**Build steps**

1. Write the document with the base and the two operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the collateral elements, the required set, the enumeration rule and the example; validate the example (AC2).
3. Write the DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key (AC3).
4. Write the error section with the problem envelope and the message identifiers, the `Idempotency-Key` rule and the 409 cause (AC4).
5. Write the versioning and pinning section with one compatible and one breaking example (AC5).
6. Generate the fake set and the drift test, and wire the drift test into the build of RWB-S3-E4020-APP and of the four sibling stories (AC6).
7. Publish v1 and record the pinned version of this contract and of each consuming story (AC5).

**Feature flag.** `rwb.guarantee.claim-resource-contract`, the same flag as the sibling contract stories of this service.

**Done when.** The document lints, the three schemas validate, the template applies twice, the fake answers every status including the conflict and the repeated key, the collateral elements round-trip or are absent, the drift test is green on the build of this story and of RWB-S3-E4020-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not hold the right of the operation | You cannot {action} here. Your role does not include it. | 403, problem body with `messageId` MSG-P4-002 |
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. | 422, problem body with `messageId` MSG-GEN-001 and `field` |
| MSG-P7-003 | The filing cannot be recorded and the action is not taken | The action was not taken because the decision could not be recorded. Try again in a few minutes. | Problem body of the update with `messageId` MSG-P7-003; the source fixes its text and no status beside it |
| MSG-GEN-006 | The service is unavailable | {system} is not available. Your request is queued and will be retried. | 503, problem body with `messageId` MSG-GEN-006 |

The texts are the legacy and platform texts carried unchanged, and this contract adds no message identifier of its own. The 401 carries the platform authentication problem and no business message; the 404 names the unknown case or claim. The 409 of an already filed claim is fixed by its status, its cause and its `messageId` slot, and its business text is not stated in any source read for this key (GAP-2737). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: it publishes a resource. SCR-17 Guarantee claim (Not due; due; submitted; paid; refused) is reached through the gateway-bff composite route, which calls this resource and the case read in one hop each (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this contract fixes only the elements the read returns, the collateral and appraisal elements among them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S3-E4020-CON-01 | AC1 | Contract | The document linted: the base, the two operations, the rights, the bearer scheme, and a third operation, a collateral-event callback and a legacy-base path refused |
| TC-S3-E4020-CON-02 | AC2 | Contract | The three schemas validated against the DF-TRT elements, the six collateral elements, the required set, the list codes and the example; an unknown element, a missing required element and a list member refused |
| TC-S3-E4020-CON-03 | AC3 | Component | The template applied in two throwaway schemas; the standard columns, the types, the keys, the widths, the absence of a cross-schema key and no collateral column asserted; a drifted hand-written table refused |
| TC-S3-E4020-CON-04 | AC4 | Contract | One problem body per status on each operation, the message identifiers, the 409 cause, the `Idempotency-Key` header required on the POST and refused absent |
| TC-S3-E4020-CON-05 | AC5, AC6 | Component | A compatible and a breaking change against the registry fake; the fake answering the create, filing, refusal, conflict, unavailable and repeated-key answers; the collateral round-trip and its absence; the drift test on a consuming build |

The legacy test set TC-E4-020-01 to TC-E4-020-04 is carried by RWB-S3-E4020-APP and by the wave 3 integration harness, and these five are the contract's own tests; no legacy id is renumbered here.

### 17. Guardrails

- No business value in the contract: the list members, the row states, the rights and the message texts are values in force, and the document names their codes only (BR4).
- No personal data in a schema, an example, a fake or a log: the identifiers and the collateral key are not personal data, and the personal-data scan fails the build otherwise.
- No cross-schema reference in the template and no foreign key across services: `case_id` is a cross reference, and the boundary test fails the build.
- No case status, no case table and no case column in any schema of this resource (BR10; DP-01).
- No deviation element and no decision-record element: X7 is rwb-deviation's and the record is the library's (DP-03).
- No insurer, SVAF or appraisal operation, because no source publishes one (BR11; GAP-2737).
- No path outside the base and no operation of a sibling: a collateral-event callback, an insurer submit and the sibling resources are named as out of scope and never declared.
- A published version is never edited in place: a breaking change raises major version 2 under a new base segment with a migration note (BR9).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-020, disposition Split (rework); its two criteria stay with RWB-S3-E4020-APP; its endpoint table, its Data table and its screen row are used here for the branch elements | 1, 2, 11, 12 |
| Feature | FEAT-GUA-08 File an insurance claim on a collateral event, module S3, epic E4, kind user, systems Workbench and SVAF, depends on FEAT-VAL-01 | 1, 2 |
| FSD S3 v3 | A2.8.3.1 VR-S3-008-1 and BR-S3-008; A2.8.3.2 field catalog; A2.8.3.3 roles; SCR-17; REQ-S3-002 and REQ-S3-007 | 2, 8, 11, 15 |
| TSD S3 v2 | T-A.1 and T-A.2 for API-S3-001 and API-S3-002; T3.0 standard columns; T3.1 `guarantee_claim`; T3.2 the two list codes and the member `COLLATERAL_INSURANCE`; T3.3 relationships; T5.1 INT-29; T5.3 no event; T6.1 rights | 3, 8, 9, 11, 12, 13 |
| Requirements | REQ-S3-002 and REQ-S3-007 of Business Requirements Program v5, section 5.10 | 2, 18 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4020-APP | App development | H consumer: implements the two operations, the collateral read, the filing write and the case report against this contract and its fake |
| RWB-S3-E4013-APP, RWB-S3-E4014-APP | App development | Siblings: preparation and submission of the TCG claim; they read the same resource and declare no path of their own |
| RWB-S3-E4015-APP, RWB-S3-E4016-APP | App development | Siblings: the tracking to payment and the subrogation position; they read the same resource |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library the filing writes through |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route the SCR-17 screen uses |
| RWB-PLT-E1044-CON | Contract | Referred to: the per-service Flyway sequence that applies the DDL template |
| P1 rwb-source-data | Service | Referred to: the collateral and appraisal read the consuming story performs; this document publishes no copy of a view field |
| P3 rwb-case, S1 rwb-valuation, S8 rwb-deviation | Services | Referred to: the case status, the appraisal order and the X7 deviation this resource never carries |
| RWB-ITG-W3 | Integration | The end-to-end proof of the resource against the live owners, held by the wave 3 harness |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the workflow branch, the activities and the filing write: RWB-S3-E4020-APP.
- The X7 deviation, its pause, its states and its return: rwb-deviation and FEAT-DVF-07.
- The appraisal order, the SVAF exchange and the accepted value: rwb-valuation and FEAT-VAL-01 to FEAT-VAL-04.
- The case status, the case signal and the case table: rwb-case (P3).
- The central decision ledger, the `GUA` rule rows and their approval: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-17: the platform edge story and the screen owner (DP-19).
- An insurer operation, an SVAF operation and an appraisal order as published elements, until a source names an interface (GAP-2737; BR11).
- The field identifiers of the collateral and appraisal elements, until the data owner allocates them (GAP-2737; ASM-4549).
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof of the resource against the live owners: the wave 3 integration harness.
