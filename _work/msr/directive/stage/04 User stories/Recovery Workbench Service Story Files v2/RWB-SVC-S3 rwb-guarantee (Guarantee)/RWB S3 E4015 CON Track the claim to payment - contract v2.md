# RWB-S3-E4015-CON Track the claim to payment - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S3-E4015-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-guarantee |
| Service epic | RWB-SVC-S3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-015 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement (DOR-RWB-S3-E4015-CON-16) |
| Contract version | v1, base `/api/recovery/guarantee/v1` |
| Open decisions | DL10 open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 confirmed |
| Reference data | Lists LOV-CLAIM-STATUS and LOV-CLAIM-TYPE; parameters: Not specified in the source documents (DOR-RWB-S3-E4015-CON-20); reference-data contract DP-06 and DP-07 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S3 rwb-guarantee v1.md (no FR mapped; no REQ identifier given by any source: Not specified in the source documents (GAP-2718); the PRD link to a REQ identifier is a PRD change to be made at C1) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-015 for rwb-guarantee (S3). The guarantee-claim resource is published on Day 1 on base `/api/recovery/guarantee/v1` (DP-13) with the two operations of TSD S3 T-A.1, the three entity names of T-A.2, the `guarantee_claim` DDL template of T3.1 with the standard columns of T3.0, the error set, the `Idempotency-Key` rule, the versioning rule and the fakes; the payment facts it names are consumed, never owned (DP-05), and the record element is the library's (DP-03). The four legacy acceptance criteria stay with RWB-S3-E4015-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S3-E4015-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 12 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **service contract owner**, I want **the published contract of the guarantee-claim resource of rwb-guarantee (S3) — the base `/api/recovery/guarantee/v1`, `POST /cases/{caseId}/guarantee-claims` with `GuaranteeClaimRequest` and `GuaranteeClaim`, `PATCH /guarantee-claims/{claimId}` with `GuaranteeClaimUpdate`, the elements named in camelCase after DF-TRT-015 to DF-TRT-022, the `guarantee_claim` DDL template with the seven standard columns, the error set 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body, the `Idempotency-Key` rule on the create, the partial-update rule of the patch, the versioning rule and the fakes** instead of the monolith's in-process controller and the one `recovery.guarantee_claim` table of the shared schema, so that **RWB-S3-E4015-APP and every later story of this service build against one frozen shape from Day 1, with no wait on any other team**.

This story owns the contract of one resource and nothing else:

- the OpenAPI 3.1 document of the guarantee-claim resource: the base, the two operations, the three object schemas, the problem schema, the security and the error set;
- the `guarantee_claim` DDL template with the columns and types of TSD S3 T3.1 and the standard columns of T3.0, one template each environment applies in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-TRT field identifiers), the required set, the enumeration rule that names a list code and no member, and the partial-update rule of the patch;
- the `Idempotency-Key` rule on the create, the compatibility rule and the pinning rule;
- the fake set generated from the document, and the drift test that every consuming build runs.

It does not own: the handlers, the workflow, the stage outcome, the breach raise and the row write, which are RWB-S3-E4015-APP; the preparation side of the same resource, which is RWB-S3-E4013-CON, and the submission side, which is RWB-S3-E4014-CON, both of them declaring the same base, the same entity names and the same DDL template as this story; the subrogation columns and the subrogation story's shape, which are RWB-S3-E4016-CON and RWB-S3-E4016-APP; the case, its stage state and its `timer` row, which are rwb-case's; the central ledger, which is P7's; the payment facts, which are rwb-source-data's; the roles and rights data, which are rwb-access's; the composite route, which is the platform edge story's; the claim deadline, the preparation window and the warning window per scheme, which are versioned reference data read at run time, and no value of them is restated in this story.

### 2. Business rationale

The monolith exposed the guarantee claim through one controller in the shared process on the base `/api/recovery/v1`, and the claim row lived in the one `recovery` schema next to 91 other tables. Three facts follow from the target and make a contract necessary before any code. First, the schema is now `rwb_guarantee` with its own login and no cross-schema access, so the table shape has to be a template every environment applies rather than one shared migration (DP-01, DP-15; Architecture v5 slides 39 and 41). Second, the base is now `/api/recovery/guarantee/v1`, so the claim no longer collides with the case, the treatment and the payment paths and every caller has one place to read them (DP-13). Third, eight stories of this service and several readers outside it touch a claim, so the element names, the required set, the error set and the partial-update rule have to be frozen before the first of them starts.

TSD S3 already fixes most of it, and this story publishes what the source states rather than inventing: T-A.1 names API-S3-001 and API-S3-002 with their rights and the `Idempotency-Key` header on the create only; T-A.2 names `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` with the error statuses; T3.1 names the eight fields of `guarantee_claim` as DF-TRT-015 to DF-TRT-022 with their physical types, required flags and lists; T3.0 names the seven standard record columns. What the source does not state is the element list of the two request schemas beyond the table's fields, the cause behind the 409, and the shape of the lost-claim reason and lost amount the two deadline rows record; those are the boundary recorded once (GAP-2719; ASM-4517).

The contract also fixes what stays out. The payment facts of `v_ace_payment` are not declared: they are read on the rwb-source-data contract and never from a view of this service (DP-05). The stage state is not a claim element and no case status appears in any schema, because the case is rwb-case's and reaches the service on the signal (ASM-4512). The decision record is not a claim element: it is written in the same transaction through the RWB-PLT-E1027-CON library, and the only sign of it on the resource is the `decisionLogId` element of the row (DP-03). The subrogation position is RWB-S3-E4016-CON's and declares no column here.

The fake is the Day-1 unblocker. RWB-S3-E4015-APP, the seven sibling stories of this service and any reporting or integration build can create, patch and read a claim before a single table exists in an environment, and the drift test turns a private variant of the shape into a build failure rather than a defect found in SIT.

### 3. Preconditions

- TSD S3 T-A.1 fixes the endpoint inventory: API-S3-001 `POST /cases/{caseId}/guarantee-claims` with right C and the `Idempotency-Key` header, and API-S3-002 `PATCH /guarantee-claims/{claimId}` with right U and no idempotency header; both are published on base `/api/recovery/guarantee/v1`, the legacy base being renamed by DP-13.
- TSD S3 T-A.2 fixes the entity names `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate`, the purpose of each operation and the error statuses 401, 403, 404, 409, 422 and 503 on both operations.
- TSD S3 T3.1 fixes the fields DF-TRT-015 to DF-TRT-022 with their physical types, their required flags and their lists, T3.0 fixes the seven standard record columns, and T3.3 fixes the one relationship, `guarantee_claim` many to one `recovery_case` on `case_id`.
- TSD S3 T3.2 fixes the list codes LOV-CLAIM-STATUS and LOV-CLAIM-TYPE; their members are values in force and are not restated as defaults in the document (BR-S3-003).
- TSD S3 T6.1 fixes the capability area Treatment and offer and the rights of each role, with RW-GUARANT at CRU and RW-CASEOWN, RW-RESTRUCT and RW-SPECIAL at CRU; the document declares the right of each operation and holds no role list.
- The problem envelope is the platform one, RFC 9457 `application/problem+json` with the platform extension members; the platform API style guide fixes its member names, so this document reuses them and does not redeclare them.
- RWB-PLT-E1027-CON publishes the decision-record contract; this document names it as the writer behind `decisionLogId` and declares no record element of its own (DP-03).
- RWB-PLT-E1044-CON publishes the per-service Flyway conventions, so the DDL is a template applied by this service's own sequence and not one shared migration (DP-15).
- No source enumerates the elements of `GuaranteeClaimRequest` and `GuaranteeClaimUpdate` beyond the table's fields, states the cause behind the 409, or gives a field identifier for the lost-claim reason and lost amount; those are outside this contract and are recorded once (GAP-2719; ASM-4517).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7 rule 1), it sits in contract group CG-W3 and it is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the base and the two operations of section 12.1, taken character for character from TSD S3 T-A.1 with the DP-13 base.
2. The author fixes the element naming rule: every element of `GuaranteeClaimRequest`, `GuaranteeClaim` and `GuaranteeClaimUpdate` is a DF-TRT field name in camelCase, and `caseId` is taken from the path on the create and is not repeated in the request body.
3. The author fixes the required set from the required column of TSD S3 T3.1: `claimType`, `claimDeadline` and `claimedAmount` are required on the create with `status`, and the patch carries only the elements a claim result changes.
4. The author fixes the enumeration rule: `claimType` and `status` name their list code and no member, because the members are values in force (BR-S3-003).
5. The author writes the `guarantee_claim` DDL template: the columns, the physical types, the required set, the primary key, the index on `case_id`, the standard columns and the rule that no key crosses a schema.
6. The author writes the error set of each operation with the problem envelope and the message identifiers the platform catalogue and TSD S3 already hold, the 409 of a claim whose state refuses the patch, and the `Idempotency-Key` rule of the create.
7. The author writes the versioning and pinning section: a compatible change keeps major version 1, a breaking change raises major version 2 under a new base segment, and v1 is never edited in place.
8. The lint and schema steps run: the document linted against the platform style, every example validated against its schema, the personal-data scan run on the examples, and the template applied twice in two throwaway schemas.
9. The fake set is generated from the document: the create answer, the patch answer, one refused answer per error status, the repeated-key answer and the unavailable answer, all from the same example set.
10. The drift test is generated and wired into the build of RWB-S3-E4015-APP and of the seven sibling application stories.
11. The document and the fakes are published at v1, and the pinned version of this contract and of each consuming story is recorded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A path outside `/api/recovery/guarantee/v1`, a third operation, or a GET on the claim is added to the document | The lint fails the build; the base and the two operations are fixed | None | AC1 |
| X2 | An element is named after anything other than a DF-TRT field, a required element is published optional, or a list member is written as a default | The schema validation fails the build | None | AC2 |
| X3 | The template is applied in another service's schema, or a foreign key crosses a schema | The boundary test fails the build; the template creates the table in the applying schema only | None | AC3 |
| X4 | An error body is not a problem document, or a status outside the declared set is returned | The envelope validation fails the build | None | AC4 |
| X5 | The patch is published as a full replace, or it carries an element the claim row does not hold | The schema validation fails the build; the patch is a partial update with its own required set | None | AC5 |
| X6 | A published element is removed, renamed, made required or given a new error status under version 1 | The change raises major version 2 under a new base segment; v1 is never edited in place | None | AC6 |
| X7 | A consuming build ships without the drift test, or ships a private variant of an element | The registry refuses the change and the drift test fails the build | None | AC6 |
| X8 | A value the consumers need is fixed by no source — the element list of the two request schemas, the cause of the 409, the lost-claim reason and amount | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2719; ASM-4517) | AC7 |

X1 to X7 are the lint, schema, boundary, envelope, partial-update, versioning and drift failures of a contract build; X8 is the boundary this key records, because the source fixes the table's fields and the entities' names and nothing more of the schema.

### 6. INVEST check

| Test | Result |
|---|---|
| Negotiable | The element order, the example values, the index list and the fake technology are open until v1 is frozen; the base, the two operations, the entity names, the required set, the error set and the versioning rule are fixed |
| Independent | Publishes a document, a DDL template and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Valuable | Unblocks RWB-S3-E4015-APP and the seven sibling stories on Day 1 and keeps one claim shape for eight stories and every later reader |
| Estimable | One OpenAPI document, three schemas, one DDL template, one error set, one versioning rule and one fake set |
| Small | One sprint for the document, the template, the fakes and the drift test |
| Testable | Each criterion of section 7 is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: guarantee-claim resource contract

  Background:
    Given the guarantee-claim resource contract document is published with major version 1
    Given the service has one schema, rwb_guarantee, and one login of its own
    Given the contract declares the two operations of TSD S3 T-A.1 and nothing more

  Scenario: AC1 The document publishes the base and the two operations, and nothing else (new, D-RCV-60)
    Given the OpenAPI document of the guarantee-claim resource
    When it is linted against the platform contract style rules
    Then it declares the server base /api/recovery/guarantee/v1 and no path on the monolith base
    Then it declares POST /cases/{caseId}/guarantee-claims with the request body GuaranteeClaimRequest and the response GuaranteeClaim
    Then it declares PATCH /guarantee-claims/{claimId} with the request body GuaranteeClaimUpdate and the response GuaranteeClaim
    Then it declares no other path: no GET, no delete and no operation of a sibling resource is in the document
    Then each operation declares the capability area "Treatment and offer" with right C on the POST and right U on the PATCH, the bearer security scheme and the scope rule
    Then a path outside the base, or a third operation, fails the lint

  Scenario: AC2 GuaranteeClaim carries the DF-TRT elements, the required set and no list member (new, D-RCV-60)
    Given the schema section of the document and its worked example
    When both request schemas and the response schema are validated and the example is checked against them
    Then GuaranteeClaimRequest, GuaranteeClaimUpdate and GuaranteeClaim are the three object schemas of this resource, with the platform problem schema reused and not redeclared
    Then every element of the three schemas is a DF-TRT field name in camelCase, from DF-TRT-015 to DF-TRT-022
    Then id, caseId, claimType, claimDeadline, claimedAmount and status are required on the response, and claimType, claimDeadline and claimedAmount are required on the create
    Then caseId is taken from the path on the create and is not repeated in GuaranteeClaimRequest
    Then claimType and status name their list code and no member value
    Then no subrogation element, no case status element, no ACE payment element and no stage state element is declared
    Then the validation fails on an unknown element, on a missing required element and on a status element added to the body

  Scenario: AC3 The guarantee_claim DDL template creates the table with the standard columns and no cross-schema key (new, D-RCV-60)
    Given the DDL template of the contract
    When it is applied twice, in two throwaway schemas, through the service's own Flyway sequence
    Then it creates guarantee_claim in the applying schema only, with the primary key on id and each column type as TSD S3 T3.1 states it
    Then claim_type is varchar(25), claim_deadline and filed_at are date, claimed_amount and paid_amount are numeric(18,2), status is varchar(12) and case_id is uuid
    Then it carries the standard columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then case_id and decision_log_id are cross references with an index each and no foreign key, and no other schema is named
    Then the required elements of AC2 are NOT NULL and the optional ones are nullable
    Then the two list columns keep the widths of the TSD and no check constraint repeats a list member
    Then a hand-written table that drifts from the template fails the drift test

  Scenario: AC4 The error set, the problem envelope and the Idempotency-Key are fixed (new, D-RCV-60)
    Given the error section of the document
    When one refused answer per status is validated against it
    Then the POST and the PATCH both declare 401, 403, 404, 409, 422 and 503
    Then every error body is application/problem+json with type, title, status, detail, instance and the messageId extension
    Then 403 carries MSG-P4-002, 404 carries the not-in-scope answer, 409 carries the refusal of a claim whose status does not admit the patch, 422 carries MSG-GEN-001 with the field name and 503 carries the platform unavailability answer
    Then the POST declares Idempotency-Key as a required header and the PATCH declares it not applicable
    Then an error body that is not a problem document, a POST without the header and a success body that is a problem document all fail the validation

  Scenario: AC5 The patch is a partial update with its own required set and its own conflict (new, D-RCV-60)
    Given the patch section of the document and its example
    When a patch body is validated against GuaranteeClaimUpdate
    Then the patch carries only filedAt, paidAmount and status, and no identity or creation element
    Then an element absent from the body leaves the row unchanged and is not cleared
    Then filedAt and paidAmount are accepted only where status admits them, and a body that sets paidAmount on a claim in PREPARING fails the validation
    Then the patch declares no Idempotency-Key, declares no other path and answers the same GuaranteeClaim as the create
    Then a patch published as a full replace fails the validation

  Scenario: AC6 Versioning separates a compatible change from a new major version, and the fake and drift test catch every difference (new, D-RCV-60)
    Given the versioning section of the document and the fake set generated from it
    When a change is proposed to a published element, and the contract test runs the fake, the template application and the drift test
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a removed element, a new required element, a renamed element, a new error status or a path change raises major version 2 under a new base segment
    Then v1 is never edited in place and stays readable after v2 is published
    Then the fake answers a create with 201 and a patch with 200, each with a GuaranteeClaim, a refused answer per status, and the first answer for a repeated Idempotency-Key
    Then the template application proves the table twice in two schemas, and the drift test fails on any difference between the fake, the template and sections 12 and 13

  Scenario: AC8 Each business rule BR1 to BR11 is traced to a criterion or a guardrail that proves it (new, D-RCV-60)
    Given the business rules of section 8 and the guardrails of section 17
    When each rule is matched to the criterion, guardrail or boundary test named for it
    Then BR1 and BR9 are proved by AC1, BR2, BR3, BR4 and BR11 by AC2, BR5 by AC3, BR6 and BR7 by AC4, BR8 by AC5, and BR7 and BR10 by AC6
    Then BR11 is also proved by the no-case-status guardrail of section 17, and BR10 by the guardrail on published versions
    Then a rule with no proving criterion or guardrail fails the traceability check

  Scenario: AC7 A value the consumers need that no source fixes is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value fixed by no source: the element list of the two request schemas, the cause of the 409, or the lost-claim reason and amount
    When the document is published with that value recorded as the working read of the assumption
    Then the value carries Not specified in the source documents (GAP-2719; ASM-4517) and no element, status or message is invented for it
    Then the gap stays open in the story until GAP-2719 is closed, and the 409 and the lost-claim fields are not published as final
```

These eight criteria are new and test only the contract deliverable. **The four legacy acceptance criteria of RWB-E4-015 stay with RWB-S3-E4015-APP** and are not repeated here, and every identifier, path, entity name, field identifier, width and status is taken from TSD S3 T-A.1, T-A.2 and T3.1, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The guarantee-claim resource is published on one base, `/api/recovery/guarantee/v1`, with exactly two operations: the create and the patch | TSD S3 T-A.1; DP-13 |
| BR2 | The three schemas are `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim`, and every element is a DF-TRT field name in camelCase | TSD S3 T-A.2, T3.1 |
| BR3 | The required set is the required column of TSD S3 T3.1, and `caseId` comes from the path on the create | TSD S3 T3.1 |
| BR4 | An enumerated element names its list code and no member, because the members are values in force with their version | TSD S3 T3.2; BR-S3-003 |
| BR5 | The `guarantee_claim` DDL template carries the fields of T3.1 with their physical types and the standard columns of T3.0, and creates the table in the applying schema only with no cross-schema key | DP-01; DP-15; TSD S3 T3.0, T3.1, T3.3 |
| BR6 | The error set is fixed per operation, and every error body is an RFC 9457 problem document that names its `messageId` | TSD S3 T-A.2; platform API style |
| BR7 | The create is idempotent by the `Idempotency-Key` header: a repeated key returns the first answer and creates no second claim; the patch declares none, because it sets absolute values and a repeat leaves the same row | TSD S3 T-A.2; DOR-RWB-S3-E4015-CON-8 |
| BR8 | The patch is a partial update of `filed_at`, `paid_amount` and `status`, and it never replaces the row: an absent element leaves its column unchanged | TSD S3 T-A.2; GAP-2719; ASM-4517 |
| BR9 | The create needs Treatment and offer C and the patch needs Treatment and offer U; the right is declared in the document and answered by the platform guard, and no check is declared in code | TSD S3 T6.1 |
| BR10 | A published element is never edited in place: a compatible change keeps major version 1 and a breaking change raises major version 2 under a new base segment | Template and Rules §R7.2; §R5.4 class C |
| BR11 | The document declares no case status, no stage state, no decision-record element, no ACE payment element and no subrogation element: the case is rwb-case's, the record is the library's, the payment is rwb-source-data's and the subrogation position is RWB-S3-E4016-CON's | ASM-4512; DP-03; DP-05; GAP-2719 |

**Where each rule lives in the target.** BR1 to BR4 are the paths, the schemas and the required set of the document and its lint. BR5 is the DDL template and its boundary test. BR6 is the error section and the platform problem schema it reuses. BR7 is the header rule of the create and the fake's repeated-key answer. BR8 is the patch section and its example. BR9 is the `security` section of each operation, with the guard being a service-template capability that adds no dependency. BR10 is the versioning section. BR11 is the boundary of this key: the case state, the record, the payment and the subrogation position are not claim elements.

**Criterion coverage.** BR1 and BR9 are AC1; BR2, BR3, BR4 and BR11 are AC2; BR5 is AC3; BR6 and BR7 are AC4; BR8 is AC5; BR7 and BR10 are also AC6.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are touched and neither is invented here.

| Object | State | Meaning in the contract |
|---|---|---|
| GuaranteeClaim (`status`) | PREPARING, FILED, DEFECT, PAID, REJECTED | The five members of LOV-CLAIM-STATUS in force; the document names the code and no member, and the example shows one value |
| GuaranteeClaim (`state`) | Draft or the applying value | The standard column of T3.0, declared varchar(40) with no check constraint, so a new state is a data change and not a contract change |
| Contract | v1 | The published version every consuming story pins |
| Contract | v2 | Raised by a breaking change under a new base segment; v1 stays readable and is never edited |

The 17 stage states of the GUARANTEE machine of TSD S3 T4 are the case's and appear nowhere in this document: the stage reports them to the parent `CaseWorkflow` and they are not claim elements (ASM-4512). The claim's own lifecycle — prepared, filed, paid or lost — is RWB-S3-E4015-APP's and its sibling stories'.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the DDL template and the fakes |
| The service owner of rwb-guarantee | Approves a breaking change and freezes a version |
| The eight application stories of this service | Consume the contract, pin the version and raise a change request rather than a private variant |
| The rwb-case owner (P3) | Confirms that no case status, no stage state and no case table is declared here, and that the stage outcome reaches the case on the signal |
| The rwb-source-data owner (P1) | Confirms that no `v_ace_*` view and no payment element is published here, and that the payment fact is consumed on its contract |
| The rwb-decision owner (P7) | Confirms the rule ID and the rule version as the values a claim carries, and that no decision code list is published here |
| The rwb-access owner (P4) | Confirms the capability area and the two rights the operations declare, and that the rwb-access authorise check of DP-08 answers them at the platform guard |
| The platform API owner | Owns the problem envelope, the style guide and the registry this document validates against |
| RW-GUARANT, RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL and the other roles of TSD S3 T6.1 | Read and patch the claim through the two operations and hold the rights the document declares; they hold no authoring right here |
| No delegation of authority level applies | A resource contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, the template, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only, and the guarantor appears as no element at all.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes paths, element names, types, a required set, an error set and list codes; no customer, account or case value appears |
| Shapes published | `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` with the DF-TRT-015 to DF-TRT-022 elements, the problem schema reused from the platform, and the `guarantee_claim` DDL template |
| Personal data | None. The claim carries no party, no name, no address, no contact value and no identity number; `createdBy` is a user identifier |
| Tables published | `guarantee_claim` only, as a DDL template applied in `rwb_guarantee`; the library objects `decision_record` and `idempotency_key` are applied in the same schema under RWB-PLT-E1027-CON and are named, not declared |
| Field identifiers | DF-TRT-015 to DF-TRT-022 as TSD S3 T3.1 lists them; the list codes LOV-CLAIM-STATUS and LOV-CLAIM-TYPE |
| Retention | The retention and archive rule of a claim row is Not specified in the source documents (GAP-2719; ASM-4517) |

The document is the one place where a business value could leak, so it fixes that a list is named by its code and never by its members, that no stage state is a claim element, and that the examples carry synthetic identifiers of the same kind as the legacy `SYN` values.

**BR Field ID.** The six rows above carry no BR Field ID: Not specified in the source documents (DOR-RWB-S3-E4015-CON-7). The check that `decision_record` is a field or entity of LDM v9 or Data Classification v5 is Cross-document.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-guarantee (S3); base `/api/recovery/guarantee/v1` (DP-13). This story publishes both operations of the resource.

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/guarantee-claims` | `GuaranteeClaimRequest`; `caseId` from the path | 201 with `GuaranteeClaim` | Treatment and offer C, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |
| PATCH | `/guarantee-claims/{claimId}` | `GuaranteeClaimUpdate` | 200 with `GuaranteeClaim` | Treatment and offer U, scope applied | Not applicable | 401, 403, 404, 409, 422, 503 |

The two operations and their purpose, request and response entities, access rights, idempotency and error statuses are those of TSD S3 T-A.1 and T-A.2 for API-S3-001 and API-S3-002, with the base renamed by DP-13. RWB-S3-E4013-CON and RWB-S3-E4014-CON declare the same base, the same three entity names and the same `guarantee_claim` DDL template for the preparation and the submission of a claim; this story owns the result elements `filedAt`, `paidAmount` and `status`, the partial-update rule of the patch and the 409 of a claim whose status refuses it, so one shape serves the whole service. No GET, no delete and no operation of the subrogation resource is declared (sections 8, 19).

#### 12.2 REST operations consumed

None — a contract document calls no service. The case state reaches the consuming story on the case signal, the payment fact and the rule package on their owners' contracts, and the rights and lists through the platform client libraries. Every one of them is a fact of the consuming story, and this contract adds no dependency of its own.

#### 12.3 Events published

None. The document declares no event type, and the Ownership Map gives S3 no event; the service topic `rwb.guarantee.events.v1` with event names `rwb.guarantee.<Event>.v1` is named in section 19 as a boundary and no type is declared here (DP-14). The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this contract (DP-03).

#### 12.4 Events consumed

None. The package, the lists and the payment fact are read by RWB-S3-E4015-APP on their contracts and never by a document; this contract names neither a topic nor a subscription.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity. `GuaranteeClaimWorkflow` is the application story's, on task queue `rwb-guarantee` in namespace `rwb-recovery`, and it calls the two operations and the server-side service method behind them; the document describes the resource only.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared, and the claim deadline is a durable timer of the workflow and not a schedule of either kind.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `guarantee_claim` | `rwb_guarantee` | S3 | The DDL template of section 13: DF-TRT-015 to DF-TRT-022, the seven standard columns, the primary key on `id`, the indexes on `case_id` and `decision_log_id` and no cross-schema key (DP-01, DP-15) |
| `decision_record` | `rwb_guarantee` | PLT library object applied in this schema | Named only: the shape is RWB-PLT-E1027-CON's and the row is written in the caller's transaction (DP-03) |
| `idempotency_key` | `rwb_guarantee` | PLT library object applied in this schema | Named only: the row of the create's `Idempotency-Key` rule (BR7) |

No table of another service is declared, read or keyed: `recovery_case`, `timer` and `task` are P3's, `rule_row`, `decision_log_entry` and the approval items P7's, the payment rows P8's and the ACE views P1's. The subrogation columns Architecture v5 slide 41 places with the guarantee route are RWB-S3-E4016-CON's and declare no column here.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Guarantee-claim resource fake | The two operations of 12.1 | A 201 create with a `GuaranteeClaim` in PREPARING; a 200 patch of the same claim; a 403, a 404, a 409, a 422 and a 503 answer |
| Repeated-key fake | The `Idempotency-Key` rule of the create | The first answer returned again for the same key, with no second claim |
| Patch fake | The partial-update rule of the patch | An answer that changes only the elements the body carries, and a refusal of a body that sets `paidAmount` on a claim in PREPARING |
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
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the guarantee-claim resource, the three schemas with the published types in `th.co.scb.ace.workbench.recovery.guarantee.api`, the `guarantee_claim` DDL template as a resource, and the fake set with the drift test. The implementation behind it is RWB-S3-E4015-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2719; ASM-4517).

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity | `id`, `caseId`, `decisionLogId` | `id` and `caseId` on the response; `caseId` from the path on the create |
| Claim | `claimType`, `claimDeadline`, `claimedAmount` | all three on the create and on the response |
| Result | `filedAt`, `paidAmount`, `status` | `status` on the create and on the response; `filedAt` and `paidAmount` optional and patched only |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-TRT field names in camelCase; the mapping is one to one and is checked by the drift test. `GuaranteeClaimUpdate` carries the result group only. The lost-claim reason and lost amount that the two deadline rows of the application story record have no field identifier in TSD S3 T3.1, so no element is published for them and the boundary is recorded once (GAP-2719; ASM-4517).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the writer behind `decisionLogId` and declares no record element | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The payment fact is consumed on rwb-source-data's contract; the document declares no `v_ace_*` path and no `v_ace_*` property | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/guarantee/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is `decisionLogId`. DP-05 is the prohibition the resource inherits, since the legacy data table reads `v_ace_payment` and the target reads it on the owner's contract. DP-19 is the route SCR-17 uses and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template as the schema and migration rules and add no dependency. The embedded Drools runtime, the access guard and the workflow kit are the service template's wave-0 capabilities, so nothing this contract refers to adds a build dependency of its own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `GuaranteeClaimOpenApi` | Document | The base, the two operations, the three schemas, the security, the error set and the versioning section (BR1 to BR4, BR6, BR10) |
| `ClaimSchemas` | Published schema | `GuaranteeClaimRequest`, `GuaranteeClaimUpdate` and `GuaranteeClaim` with the DF-TRT elements and the required set (BR2, BR3) |
| `ClaimDdlTemplate` | Resource | The `guarantee_claim` DDL: columns, types, keys, indexes and standard columns (BR5) |
| `ProblemEnvelope` | Reused schema | The platform RFC 9457 problem document with the `messageId` extension (BR6) |
| `IdempotencyRule` | Document | The `Idempotency-Key` header of the create, the repeated-key answer and its counting (BR7) |
| `PatchRule` | Document | The partial-update rule, the element set of the patch and its 409 (BR8) |
| `Fake set and fixtures` | Test asset | The create, patch, refused, conflict, unavailable and repeated-key answers every consuming build uses (AC6) |
| `DriftTest` | Test asset | The comparison of a consuming build against sections 12 and 13 (BR10, AC6) |

**Database.** The template creates `guarantee_claim` in `rwb_guarantee` only, with the physical types of TSD S3 T3.1 and the standard columns of T3.0. `case_id` and `decision_log_id` are cross references with an index each and no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). No timer, task, case or payment table is created here.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR4). The capability area and the rights are declared per operation and their role lists are rwb-access data (BR9). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the two operations; lint the paths and the rights (AC1).
2. Write the three schemas with the element mapping, the required set, the enumeration rule and the examples; validate the examples (AC2).
3. Write the DDL template and apply it twice in two throwaway schemas; assert the columns, the widths, the keys and the absence of a cross-schema key (AC3).
4. Write the error section with the problem envelope, the message identifiers and the `Idempotency-Key` rule (AC4).
5. Write the patch section with its element set, its conditional rule and its 409 (AC5).
6. Write the versioning and pinning section with one compatible and one breaking example, then generate the fake set and the drift test and wire it into the build of RWB-S3-E4015-APP and of the seven sibling stories (AC6).
7. Publish v1 and record the pinned version of this contract and of each consuming story (AC6).

**Feature flag.** `rwb.guarantee.claim-contract-v1`.

**Done when.** The document lints, the three schemas validate, the template applies twice, the fake answers every status including the conflict, the patch and the repeated key, the drift test is green on the build of this story and of RWB-S3-E4015-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not hold the right of the operation | You cannot {action} here. Your role does not include it. | 403, problem body with `messageId` MSG-P4-002 |
| MSG-GEN-001 | A required field of the request is missing or invalid | Enter {field}. | 422, problem body with `messageId` MSG-GEN-001 and `field` |
| MSG-P7-003 | The decision record cannot be written before the claim changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. | 503, problem body with `messageId` MSG-P7-003 |
| MSG-P1-001 | The payment product the consuming story reads is stale after a late or failed ACE batch | {product} is from {date}. Today's load has not arrived. | Not an answer of this resource: it is shown by the consuming story |

The four texts are the legacy and FSD texts carried unchanged except MSG-P1-001, whose English text is the message text of Recovery Workbench Error and Message Standard v4 (MSG-P1-001), and this contract adds no message identifier of its own. The 401 carries the platform authentication problem and no business message. The 404 text, the 409 text and the 503 text for an unavailable downstream are not stated in any source read for this key and are Not specified in the source documents (GAP-2719; ASM-4517); the contract fixes their status, their cause and their `messageId` slot. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: it publishes a resource. SCR-17 Guarantee claim (Not due; due; submitted; paid; refused; empty, loading, error and no access states: Not specified in the source documents (CG-ALL-8872)) is reached through the gateway-bff composite route, which calls this resource and the case read in one hop each (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this contract fixes only the elements the two operations carry.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-015-01 | AC1, AC2 | Contract | The document, its base and its two operations; the three schemas, the DF-TRT elements, the required set and the example |
| TC-E4-015-02 | AC2, AC5 | Contract | A patch body of filedAt, paidAmount and status against GuaranteeClaimUpdate; a partial body and a body that sets paidAmount on PREPARING |
| TC-E4-015-03 | AC2, AC5 | Contract | The claim `status` values of LOV-CLAIM-STATUS and `claimType` of LOV-CLAIM-TYPE, with a member written as a default refused |
| TC-E4-015-04 | AC4, AC6 | Contract | One problem body per status on each operation, the repeated-key answer and the drift test of a private variant |
| TC-E4-015-05 | AC4, AC5 | Contract | A role without Treatment and offer U or C, a body with a missing field and a claim whose status refuses the patch |
| TC-E4-015-06 | AC6 | Contract | The template applied twice, the BACKWARD-mode acceptance and refusal, and the pinned version of RWB-S3-E4015-APP |
| TC-S3-E4015-CON-01 | AC1 | Contract | The document linted: the base, the two operations, the rights, the bearer scheme, and a third operation and an old-base path refused |
| TC-S3-E4015-CON-02 | AC2 | Contract | The three schemas validated against the DF-TRT elements, the required set, the list codes and the examples |
| TC-S3-E4015-CON-03 | AC3 | Component | The template applied in two throwaway schemas; the standard columns, the types, the widths, the keys and the absence of a cross-schema key asserted |
| TC-S3-E4015-CON-04 | AC5, AC6 | Component | The patch partial-update rule, the conflict cause, the fakes and the drift test on a consuming build |
| TC-S3-E4015-CON-07 | AC8 | Contract | Each rule BR1 to BR11 of section 8 matched to the criterion or the section 17 guardrail that proves it, and an unproved rule refused |
| TC-S3-E4015-CON-05 | AC3 | Component | The boundary of the three tables of section 12.7 only: no table of another service declared, read or keyed, and the library objects named, not declared |
| TC-S3-E4015-CON-06 | AC7 | Component | A value fixed by no source is published as the working read, carries Not specified in the source documents (GAP-2719; ASM-4517), and the gap stays open |

The six legacy cases are the legacy cases of RWB-E4-015 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S3-E4015-APP. Where the legacy test names a rule, the contract half answers the element and the status the rule's target state implies, and the rule itself is evaluated by the application story. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S3-E4015-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the list members, the row states, the rights and the message texts are values in force, and the document names their codes only (BR4).
- No personal data in a schema, an example, a fake or a log: the claim carries no party, the case is an identifier, `createdBy` is a user identifier, and the personal-data scan fails the build otherwise.
- No cross-schema reference in the template and no foreign key across services: `case_id` and `decision_log_id` are cross references, and the boundary test fails the build.
- No case status, no stage state, no case table and no `timer` column in any schema of this resource (ASM-4512; DP-01).
- No ACE payment element, no `v_ace_*` path and no `v_ace_*` property: the payment fact is rwb-source-data's and is consumed on its contract (DP-05).
- No decision-record element and no decision code list: the record is the library's, `decisionLogId` is its only trace, and the code is the rule ID and version in force (DP-03).
- No subrogation element: the subrogation position is RWB-S3-E4016-CON's and declares nothing here.
- No path outside the base and no operation of a sibling: no GET, no delete and no third operation is declared.
- A published version is never edited in place: a breaking change raises major version 2 under a new base segment with a migration note (BR10).

### 18. Traceability

| Requirement ID | Requirement (short) | Feature | Rules | Test cases |
|---|---|---|---|---|
| No REQ-S3 identifier is given for this key by any source read: TSD S3 T8 maps REQ-S3-001 to REQ-S3-007 to FEAT-GUA-01, and the Epics 3 to 8 specification carries feature IDs only (GAP-2718; ASM-4516) | Claim status, payment and any shortfall are recorded on the case, inside the guarantor's deadline (FSD S3 A2.3, REQ-S3-002) | FEAT-GUA-03 | BR1 to BR11; DP-13 | TC-E4-015-01 to TC-E4-015-06, TC-S3-E4015-CON-01 to -04 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S3-E4015-APP | App development | H consumer: implements the two operations, the workflow, the row and the breach against this contract and its fake |
| RWB-S3-E4013-APP, RWB-S3-E4014-APP | App development | Sibling: the preparation and the submission of the claim, which create and patch the same row |
| RWB-S3-E4016-CON, RWB-S3-E4016-APP | Contract, App development | Sibling: the subrogation position, which declares its own elements and adds none here |
| RWB-S3-E4017-APP, RWB-S3-E4018-APP, RWB-S3-E4019-APP, RWB-S3-E4020-APP | App development | Siblings: the notices, the negotiation, the closing and the insurance claim, which consume the same resource |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library behind `decisionLogId`; this contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route SCR-17 uses |
| RWB-PLT-E1044-CON | Contract | Referred to: the per-service Flyway sequence that applies the DDL template |
| P3 rwb-case, P7 rwb-decision, P1 rwb-source-data | App development | Referred to: the case and its stage state, the package and the rules, and the payment facts the claim never carries |
| RWB-ITG-W3 | Integration | The end-to-end proof of the resource against the live owners, held by the wave 3 harness |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the workflow, the activities, the breach and the row write: RWB-S3-E4015-APP.
- The preparation of the claim, the scheme checklist and R-GUA-04: RWB-S3-E4013-APP and RWB-S3-E4013-CON.
- The submission to the TCG portal and its reference: RWB-S3-E4014-APP and RWB-S3-E4014-CON.
- The subrogation position and R-GUA-22 to R-GUA-25: RWB-S3-E4016-CON and RWB-S3-E4016-APP.
- The guarantor and co-borrower notices: RWB-S3-E4017-APP and RWB-S3-E4017-CON.
- The negotiation with a guarantor: RWB-S3-E4018-APP and RWB-S3-E4018-CON.
- The closing of the guarantee and the insurance claim on a collateral event: RWB-S3-E4019-APP and RWB-S3-E4020-APP with their contracts.
- The case, its stage state, its `timer` and `task` rows and the stage outcome answer: rwb-case (P3); no case element is published here (ASM-4512).
- The payment facts of ACE and every `v_ace_*` view: rwb-source-data (P1) (DP-05).
- The central ledger, the rule packages and the decision codes: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-17: the platform edge story (DP-19).
- The element list of the two request schemas beyond the table's fields, the cause of the 409 and the fields of the lost-claim reason and amount (GAP-2719; ASM-4517).
- Any event type of `rwb.guarantee.events.v1`: the Ownership Map gives S3 no event, and this contract declares none (DP-14).
- The deployment of this build: the chart values, the schema and login, the queue, the flag and the publication pipeline.
- The real cross-service proof of the resource against the live owners: the wave 3 integration harness.
