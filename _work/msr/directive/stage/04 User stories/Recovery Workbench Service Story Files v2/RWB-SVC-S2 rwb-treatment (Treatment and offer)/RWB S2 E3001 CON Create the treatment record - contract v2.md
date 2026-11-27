# RWB-S2-E3001-CON Create the treatment record - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E3-001 for rwb-treatment (S2). The treatment resource is published on Day 1 on base `/api/recovery/treatment/v1` (DP-13), with the two operations and the `treatment` DDL template it needs; the four legacy acceptance criteria stay with RWB-S2-E3001-APP, and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S2-E3001-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (12 resolved, 17 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S2-E3001-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-treatment |
| Contract version | 1 (major version 1, base /api/recovery/treatment/v1) |
| Service epic | RWB-SVC-S2 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-001 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S2-E3001-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S2 rwb-treatment v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **service contract owner**, I want **the published contract of the treatment resource of rwb-treatment (S2) — the base `/api/recovery/treatment/v1`, `POST /cases/{caseId}/treatments` and `GET /treatments/{treatmentId}` with the entity names `TreatmentRequest` and `Treatment` of TSD S2 T-A.2, the elements named in camelCase after DF-TRT-001 to DF-TRT-033, the `treatment` DDL template with the T3.0 standard columns, the error set 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body, the `Idempotency-Key` rule, the versioning rule and the fakes** instead of the monolith's in-process controller and the one `recovery.treatment` table of the shared schema, so that **RWB-S2-E3001-APP and every later story of the service build against one frozen shape from Day 1, with no wait on any other team**.

This story owns the contract of one resource and nothing else:

- the OpenAPI 3.1 document of the treatment resource: the base, the two operations, the two object schemas, the problem schema, the security and the error set;
- the `treatment` DDL template with the columns and types of TSD S2 T3.1 and the standard columns of T3.0, one template each environment applies in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-TRT field identifiers), the required set and the enumeration rule that names a list code and no member;
- the `Idempotency-Key` rule on the POST, the compatibility rule and the pinning rule;
- the fake set generated from the document, and the drift test that every consuming build runs;
- reference data: the list codes named in AC2 are taken from the reference-data contract (DP-06, DP-07), and this contract names no parameter.

It does not own: the handlers, the workflow, the stage outcome reporting and the row write, which are RWB-S2-E3001-APP; the settlement offer and its operation, which is RWB-S2-E3002-CON; the approval envelope and the draft-terms change, which are RWB-S2-E3003-CON; the TDR plan body and its timers, which are RWB-S2-E3004-CON; the case status and the case signal, which are rwb-case's; the central ledger, which is P7's; the roles and rights data, which are rwb-access's; the composite route, which is the platform edge story's.

### 2. Business rationale

The monolith exposed the treatment through one controller in the shared process on the base `/api/recovery/v1`, and the treatment row lived in the one `recovery` schema next to 91 other tables. Three facts follow from the target and make a contract necessary before any code. First, the schema is now `rwb_treatment` with its own login and no cross-schema access, so the table shape has to be a template every environment applies rather than one shared migration (DP-01, DP-15; Architecture v5 slides 39 and 41). Second, the base is now `/api/recovery/treatment/v1`, so the paths of the treatment no longer collide with the case, the payment and the guarantee services and every caller has one place to read them (DP-13). Third, five stories of this service and several other services read a treatment, so the element names, the required set and the error set have to be frozen before the first one of them starts.

TSD S2 already fixes most of it, and this story publishes what the source states rather than inventing: T-A.1 names the four paths and their rights, T-A.2 names the request and response entities `TreatmentRequest`, `TreatmentUpdate` and `Treatment` with the error statuses and the `Idempotency-Key` header, T3.1 names the 25 fields of `treatment` with their physical types, their required flag and their list, and T3.0 names the standard record columns. What the source does not state is the field list of the contracts, settlement and deed-in-lieu agreements and plan timers that Architecture v5 slide 41 also places in `rwb_treatment`; those tables get their own shape with the sibling stories that own them, and the boundary is recorded once (GAP-1869; ASM-3065).

The contract also fixes what stays out. The offer operation of Architecture v5 slide 18 is not declared here: it is RWB-S2-E3002-CON. The approval envelope of `POST /treatments/{treatmentId}/submit` is RWB-S2-E3003-CON. The plan body of the TDR treatment is RWB-S2-E3004-CON. No case status appears in any element, because the case status is rwb-case's and reaches this service on the case signal (ASM-3062). And the decision record is not a treatment element: it is written in the same transaction through the RWB-PLT-E1027-CON library, and the only sign of it on the resource is the `decisionLogId` element of the row (DP-03).

The fake is the Day-1 unblocker. RWB-S2-E3001-APP, the four sibling application stories and any reporting or integration build can create and read a treatment before a single table exists in an environment, and the drift test turns a private variant of the shape into a build failure rather than a defect found in SIT.

### 3. Preconditions

- TSD S2 T-A.1 fixes the endpoint inventory: API-S2-001 `POST monolith-base/cases/{caseId}/treatments` with right C and the `Idempotency-Key` header, and API-S2-002 `GET monolith-base/treatments/{treatmentId}` with right R; the base is renamed to `/api/recovery/treatment/v1` by DP-13.
- TSD S2 T-A.2 fixes the entity names `TreatmentRequest`, `TreatmentUpdate` and `Treatment`, and the error statuses of the two operations this story declares.
- TSD S2 T3.1 fixes the fields DF-TRT-001 to DF-TRT-033 with their physical types, their required flags and their lists, and T3.0 fixes the seven standard record columns.
- TSD S2 T3.2 fixes the list codes LOV-TREATMENT, LOV-PROPOSER, LOV-TRT-OUTCOME, LOV-APPROVAL-LEVEL, LOV-CREDIT-RESULT and LOV-TRT-SIGNATURE; their members are values in force and are not restated in the document (BR-S2-001).
- TSD S2 T6.1 fixes the capability area "Treatment and offer" and the rights of each role; the document declares the right of each operation and holds no role list.
- The problem envelope is the platform one, RFC 9457 `application/problem+json` with the platform extension members; the platform API style guide fixes its member names, so this document reuses them and does not redeclare them.
- RWB-PLT-E1027-CON publishes the decision-record contract; this document names it as the writer behind `decisionLogId` and declares no record element of its own (DP-03).
- RWB-PLT-E1044-CON publishes the per-service Flyway conventions, so the DDL is a template applied by this service's own sequence and not one shared migration (DP-15).
- No source gives a field list for the contracts, settlement and deed-in-lieu agreements and plan timers of Architecture v5 slide 41, and none states how the stage reports its outcome to the case; both are outside this contract and are recorded once (GAP-1869; ASM-3065).
- No build dependency and no approval stop: a CON story is Day 1 by rule (§R5.7), it sits in contract group CG-W2 and it is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the base and the two operations of section 12.1, taken character for character from TSD S2 T-A.1 with the DP-13 base.
2. The author fixes the element naming rule: every element of `TreatmentRequest` and `Treatment` is the DF-TRT field name in camelCase, and `caseId` is taken from the path on the POST and is not repeated in the request body.
3. The author fixes the required set from the required column of TSD S2 T3.1, so `id`, `caseId`, `treatmentType`, `proposedBy`, `proposedAt` and `installmentsPaid` are required and every other element is optional.
4. The author fixes the enumeration rule: an enumerated element names its list code and no member, because the members are values in force (BR-S2-001).
5. The author writes the `treatment` DDL template: the columns, the physical types, the required set, the primary key, the indexes, the standard columns and the rule that no key crosses a schema.
6. The author writes the error set of each operation with the problem envelope and the four message identifiers the platform catalogue already holds, and the `Idempotency-Key` rule of the POST.
7. The author writes the versioning and pinning section: a compatible change keeps major version 1, a breaking change raises major version 2 under a new base segment, and v1 is never edited in place.
8. The lint and schema steps run: the document linted against the platform style, every example validated against its schema, the personal-data scan run on the examples, and the template applied twice in two throwaway schemas.
9. The fake set is generated from the document: the two success answers, one refused answer per error status, the repeated-key answer and the unavailable answer, all from the same example set.
10. The drift test is generated and wired into the build of RWB-S2-E3001-APP and of the four sibling application stories.
11. The document and the fakes are published at v1, and the pinned version of this contract and of each consuming story is recorded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A path outside `/api/recovery/treatment/v1`, or a third operation, is added to the document | The lint fails the build; the base and the two operations are fixed | None | AC1 |
| X2 | An element is named after anything other than a DF-TRT field, or a required element is published optional | The schema validation fails the build | None | AC2 |
| X3 | The template is applied in another service's schema, or a foreign key crosses a schema | The boundary test fails the build; the template creates the table in the applying schema only | None | AC3 |
| X4 | An error body is not a problem document, or a status outside the declared set is returned | The envelope validation fails the build | None | AC4 |
| X5 | A published element is removed, renamed, made required or given a new error status under version 1 | The change raises major version 2 under a new base segment; v1 is never edited in place | None | AC5 |
| X6 | A consuming build ships without the drift test, or ships a private variant of an element | The registry refuses the change and the drift test fails the build | None | AC6 |
| X7 | A value the consumers need is fixed by no source — the field list of the agreement tables, the cause of the 409, the outcome report of the stage | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-1869; ASM-3065) | AC7; Sections 12 and 13 |

X1 to X6 are the lint, schema, boundary, envelope, versioning and drift failures of a contract build; X7 is the boundary this key records, because the source fixes the field list of the treatment and of nothing else in the schema.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a DDL template and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The element order, the example values, the index list and the fake technology are open until v1 is frozen; the base, the two operations, the element names, the required set, the error set and the versioning rule are fixed |
| Valuable | Unblocks RWB-S2-E3001-APP and the four sibling stories on Day 1 and keeps one treatment shape for five stories and every later reader |
| Estimable | One OpenAPI document, one schema pair, one DDL template, one error set, one versioning rule and one fake set |
| Small | One sprint for the document, the template, the fakes and the drift test |
| Testable | Each criterion of section 7 is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: treatment resource contract

  Background:
    Given the treatment resource contract document is published with major version 1
    Given the service has one schema, rwb_treatment, and one login of its own
    Given the contract declares the two operations of TSD S2 T-A.2 and nothing more

  Scenario: AC1 The document publishes the base and the two operations, and nothing else (new, D-RCV-60)
    Given the OpenAPI document of the treatment resource
    When it is linted against the platform contract style rules
    Then it declares the server base /api/recovery/treatment/v1 and no path on the old base /api/recovery/v1
    Then it declares POST /cases/{caseId}/treatments with the request body TreatmentRequest and the response Treatment
    Then it declares GET /treatments/{treatmentId} with no request body and the response Treatment
    Then it declares no other path: the offer operation, the draft-terms change, the submit and the approval envelope are not in the document
    Then each operation declares the capability area "Treatment and offer" with right C on the POST and right R on the GET, the bearer security scheme and the scope rule
    Then a path outside the base, or a third operation, fails the lint

  Scenario: AC2 Treatment carries the DF-TRT elements, the required set and no list member (new, D-RCV-60)
    Given the schema section of the document and its worked example
    When both schemas are validated and the example is checked against them
    Then TreatmentRequest and Treatment are the two object schemas of this resource, with the platform problem schema reused and not redeclared
    Then every element of both schemas is a DF-TRT field name in camelCase, from DF-TRT-001 to DF-TRT-033
    Then id, caseId, treatmentType, proposedBy, proposedAt and installmentsPaid are required and every other element is optional
    Then caseId is taken from the path on the POST and is not repeated in TreatmentRequest
    Then treatmentType, proposedBy, outcome, approvalLevel, creditResult and signatureStatus name their list code and no member value
    Then no guarantee-claim element, no contract, agreement or plan-timer element and no case status element is declared
    Then the validation fails on an unknown element, on a missing required element and on a status element added to the body

  Scenario: AC3 The treatment DDL template creates the table with the standard columns and no cross-schema key (new, D-RCV-60)
    Given the DDL template of the contract
    When it is applied twice, in two throwaway schemas, through the service's own Flyway sequence
    Then it creates treatment in the applying schema only, with the primary key on id and each column type as TSD S2 T3.1 states it
    Then it carries the standard columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then case_id and decision_log_id are cross references with an index each and no foreign key, and no other schema is named
    Then the required elements of AC2 are NOT NULL and the optional ones are nullable
    Then the list columns keep the widths of the TSD and no check constraint repeats a list member
    Then a hand-written table that drifts from the template fails the drift test

  Scenario: AC4 The error set, the problem envelope and the Idempotency-Key are fixed (new, D-RCV-60)
    Given the error section of the document
    When one refused answer per status is validated against it
    Then the POST declares 401, 403, 404, 409, 422 and 503 and the GET declares 401, 403, 404 and 503
    Then every error body is application/problem+json with type, title, status, detail, instance and the messageId extension
    Then 403 carries MSG-P4-002, 404 carries MSG-P4-003, 409 carries the conflict of an open treatment of the same type for the case, 422 carries MSG-P7-009 with the field name and 503 carries MSG-GEN-006
    Then the POST declares Idempotency-Key as a required header and the GET declares it not applicable
    Then an error body that is not a problem document, a POST without the header and a success body that is a problem document all fail the validation

  Scenario: AC5 Versioning separates a compatible change from a new major version, and the consumer pins (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a removed element, a new required element, a renamed element, a new error status or a path change raises major version 2 under a new base segment
    Then v1 is never edited in place and stays readable after v2 is published
    Then each consuming story pins the published version and a private variant fails its drift test
    Then the document records the version pinned by RWB-S2-E3001-APP

  Scenario: AC6 The fake answers the document and the drift test catches every difference (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the treatment fake, the problem fakes, the template application and the drift test
    Then the treatment fake answers a create with 201 and a Treatment whose state is Draft, and a read with 200 and the same Treatment
    Then it answers a refused create with 403 and 422, a missing treatment with 404, a conflict with 409 and an unavailable service with 503
    Then it returns the first answer for a repeated Idempotency-Key and never a second treatment
    Then the template application proves the table twice in two schemas
    Then the drift test fails on any difference between the fake, the template and sections 12 and 13 of the document

  Scenario: AC7 A value fixed by no source is published as the working read and the gap stays open (new, D-RCV-60)
    Given a value the consumers need is fixed by no source
    When the contract is published
    Then the value is published as the working read of the assumption
    Then the gap stays open and the message names GAP-1869 and ASM-3065
```

These six criteria are new and test only the contract deliverable. **The four legacy acceptance criteria of RWB-E3-001 stay with RWB-S2-E3001-APP** and are not repeated here, and every identifier, path, entity name, field identifier and status is taken from TSD S2 T-A.1, T-A.2 and T3.1, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The treatment resource is published on one base, `/api/recovery/treatment/v1`, with exactly two operations: the create and the read | TSD S2 T-A.1; DP-13 |
| BR2 | The two schemas are `TreatmentRequest` and `Treatment`, and every element is a DF-TRT field name in camelCase | TSD S2 T-A.2, T3.1 |
| BR3 | The required set is the required column of TSD S2 T3.1: `id`, `caseId`, `treatmentType`, `proposedBy`, `proposedAt` and `installmentsPaid`; `caseId` comes from the path on the POST | TSD S2 T3.1 |
| BR4 | An enumerated element names its list code and no member, because the members are values in force with their version | TSD S2 T3.2; BR-S2-001 |
| BR5 | The `treatment` DDL template carries the fields of T3.1 with their physical types and the standard columns of T3.0, and creates the table in the applying schema only with no cross-schema key | DP-01; DP-15; TSD S2 T3.0, T3.1 |
| BR6 | The error set is fixed per operation, and every error body is an RFC 9457 problem document that names its `messageId` | TSD S2 T-A.2; platform API style |
| BR7 | The create is idempotent by the `Idempotency-Key` header: a repeated key returns the first answer and creates no second treatment | TSD S2 T-A.2; legacy RWB-E3-001 AC1 |
| BR8 | The create needs Treatment and offer C and the read needs Treatment and offer R; the right is declared in the document and checked by the platform guard against the rwb-access authorise check, and no check is declared in code | TSD S2 T6.1; DP-08 |
| BR9 | A published element is never edited in place: a compatible change keeps major version 1 and a breaking change raises major version 2 under a new base segment | Template and Rules §R7.2; §R5.4 class C |
| BR10 | The document declares no case status, no decision-record element and no decision code: the status is rwb-case's, the record is the library's and the code is the rule ID and version in force | ASM-3062; DP-03; GAP-1869; ASM-3065 |
| BR11 | The document declares no field of the contracts, settlement and deed-in-lieu agreements and plan timers, because the source gives them no field list; their shape is published with the sibling stories that own them | GAP-1869; ASM-3065 |
| BR12 | The treatment read carries an optional readiness section with checkType, encumbranceStatus, registrationStatus, titleSetStatus, checkedAt, ruleId, ruleVersion, holdUntil, collateralNo and assetKey, served inside the answer of `GET /treatments/{treatmentId}` at the same major version; the encumbrance and title statuses are values of the ACE read and never a column of the treatment table | ASM-B2-S2-008-1; ASM-B2-S2-008-2; ASM-B2-S2-008-3; GAP-2674; GAP-2675 |
| BR13 | The title-set task is an element of the stage outcome that reaches rwb-case, carrying R-SET-22 with its version, the 5 working-day clock and the reason code; it is not a treatment element, and the view ranges DF-ACE-091 to DF-ACE-098, DF-ACE-196 to DF-ACE-207 and DF-ACE-208 to DF-ACE-219 are read only | TSD S2 v2 T4 SETTLEMENT; FSD S2 A2.13.3.1; GAP-2674; GAP-2675 |

**Where each rule lives in the target.** BR1 to BR4 are the paths, the schemas and the required set of the document and its lint. BR5 is the DDL template and its boundary test. BR6 is the error section and the platform problem schema it reuses. BR7 is the header rule of the POST and the fake's repeated-key answer. BR8 is the `security` section of each operation; the guard is the platform library's and the contract adds no dependency for it. BR9 is the versioning section. BR10 and BR11 are the two boundaries of this key: the case status and the decision code are not contract values, and the tables the source names without a field list are not published here.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are touched and neither is fixed here.

| Object | State | Meaning in the contract |
|---|---|---|
| Treatment | Draft | The state a created treatment carries in the fake and in the example; the other states of the row are the values in force the screen shows |
| Treatment | submitted, approved, booked, broken | Named by the legacy SCR-14 state list; the document carries them as values of `state` from the list in force and fixes none of them |
| Contract | v1 | The published version every consuming story pins |
| Contract | v2 | Raised by a breaking change under a new base segment; v1 stays readable and is never edited |

The treatment lifecycle itself is RWB-S2-E3001-APP's and the sibling stories'; the transition table of a case is rwb-case's and appears nowhere in this document. The `state` column is declared as varchar(40) with no check constraint, so a new row state is a data change and not a contract change.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the DDL template and the fakes |
| The service owner of rwb-treatment | Approves a breaking change and freezes a version |
| The five application stories of this service | Consume the contract, pin the version and raise a change request rather than a private variant |
| The rwb-case owner (P3) | Confirms that no case status and no case table is declared here, and that the stage outcome reaches the case on the signal |
| The rwb-decision owner (P7) | Confirms the rule ID and the rule version as the values a treatment carries, and that no decision code list is published here |
| The rwb-access owner (P4) | Confirms the capability area and the rights the two operations declare |
| The platform API owner | Owns the problem envelope, the style guide and the registry this document validates against |
| RW-RESTRUCT, RW-CASEOWN, RW-SPECIAL, RW-GUARANT and the other roles of TSD S2 T6.1 | Read the treatment through the two operations and hold the rights the document declares; they hold no authoring right here |
| No delegation of authority level applies | A resource contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in the document, the template, an example or a fake. Where a caller must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value |
|---|---|
| Business data published | None. The document publishes paths, element names, types, a required set, an error set and list codes; no customer, account or case value appears. BR ID: BR11 |
| Shapes published | `TreatmentRequest` and `Treatment` with the DF-TRT-001 to DF-TRT-033 elements, the problem schema reused from the platform, and the `treatment` DDL template. BR ID: BR2, BR3, BR5 |
| Personal data | None. `proposedBy` and `createdBy` are references or user identifiers, never a name; no account number, national identifier or document content appears. BR ID: BR4 |
| Tables published | `treatment` only, as a DDL template applied in `rwb_treatment`; the library object `decision_record` is applied in the same schema under RWB-PLT-E1027-CON and is named, not declared. The dated copy `dp_treatment` is P1's, built from this service's events and read only for reporting; this service never reads it as the source of a treatment (ASM-A6-tables-14). BR ID: BR5, BR10 |
| Field identifiers | DF-TRT-001 to DF-TRT-033 as TSD S2 T3.1 lists them; the list codes LOV-TREATMENT, LOV-PROPOSER, LOV-TRT-OUTCOME, LOV-APPROVAL-LEVEL, LOV-CREDIT-RESULT and LOV-TRT-SIGNATURE. BR ID: BR2, BR3, BR4 |
| Retention | The retention and archive rule of a treatment row is Not specified in the source documents (GAP-1869; ASM-3065). BR ID: BR11 |

The document is the one place where a business value could leak, so it fixes that a list is named by its code and never by its members, that a case status is not a treatment element, and that the examples carry synthetic identifiers of the same kind as the legacy `SYN` values.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-treatment (S2); base `/api/recovery/treatment/v1` (DP-13). This story publishes both operations.

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/treatments` | `TreatmentRequest`; `caseId` from the path | 201 with `Treatment` | Treatment and offer C, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |
| GET | `/treatments/{treatmentId}` | None | 200 with `Treatment` | Treatment and offer R, scope applied | Not applicable | 401, 403, 404, 503 |

The two operations and their purpose, request and response entities, access rights, idempotency and error statuses are those of TSD S2 T-A.1 and T-A.2 for API-S2-001 and API-S2-002, with the base renamed by DP-13. The offer operation, the draft-terms change and the submit-for-approval operation are not declared here; they belong to RWB-S2-E3002-CON, RWB-S2-E3003-CON and RWB-S2-E3004-CON (section 19).

#### 12.2 REST operations consumed

None — a contract document calls no service. The case status reaches the service on the case signal and the rule package on `RulePackageInForce`; the rights and the lists arrive through the platform client libraries. Every one of them is a fact of the consuming story, and this contract adds no dependency of its own.

#### 12.3 Events published

None. The service topic is `rwb.treatment.events.v1` with event names `rwb.treatment.<Event>.v1` (DP-14), and the two event types `TreatmentApproved` and `TreatmentClosed` are named in section 19 as the sibling stories' and are not declared here. The `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this contract (DP-03).

#### 12.4 Events consumed

None. The package event and the case signal are consumed by RWB-S2-E3001-APP and never by a document; the contract names neither as a subscription.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity. `TreatmentWorkflow` is the application story's, on task queue `rwb-treatment` in namespace `rwb-recovery`, and it calls the two operations and the server-side service method behind them; the document describes the resource only.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared, and the plan timers of the restructure route belong to the sibling plan story.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `treatment` | `rwb_treatment` | S2 | The DDL template of section 13: DF-TRT-001 to DF-TRT-033, the seven standard columns, the primary key on `id`, the indexes on `case_id` and `decision_log_id` and no cross-schema key (DP-01, DP-15) |
| `decision_record` | `rwb_treatment` | PLT library object applied in this schema | Named only: the shape is RWB-PLT-E1027-CON's and the row is written in the caller's transaction (DP-03) |

Architecture v5 slide 41 also names contracts, settlement and deed-in-lieu agreements and plan timers in `rwb_treatment`; the source gives them no field list, so this contract declares no column of theirs and their shape is published with RWB-S2-E3002-CON and RWB-S2-E3004-CON (GAP-1869; ASM-3065). No table of another service is declared, read or keyed.

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Treatment resource fake | The two operations of 12.1 | A 201 create with a `Treatment` in state Draft; a 200 read of the same treatment; a 403 and a 422 refusal; a 404 for an unknown ID; a 409 conflict; a 503 unavailability |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second treatment |
| Template application | The `treatment` DDL template | The table created twice in two throwaway schemas, with the standard columns, the keys and no cross-schema reference |
| Problem fakes | The problem envelope | One `application/problem+json` body per error status, each with its `messageId` |
| Registry and drift fake | The compatibility rule | One accepted and one refused body in BACKWARD mode, and a drift failure for a private variant of an element |

Every fake answers from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming build rather than as a surprise in SIT.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 2 operations on `/api/recovery/treatment/v1` | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches them through gateway-bff (DP-19) |
| Kafka | 0 | 0 | The service topic is named and no event type is declared here |
| Temporal | 0 | 0 | The contract declares no workflow and no activity |
| File | 0 | 0 | No file crosses the contract |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the treatment resource, the `TreatmentRequest` and `Treatment` schemas with the published types in `th.co.scb.ace.workbench.recovery.treatment.api`, the `treatment` DDL template as a resource, and the fake set with the drift test. The implementation behind it is RWB-S2-E3001-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-1869; ASM-3065).

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity | `id`, `caseId`, `decisionLogId` | `id` and `caseId` yes; `decisionLogId` no |
| Type and proposer | `treatmentType`, `proposedBy`, `proposedAt` | all three |
| Terms | `offerAmount`, `haircutAmount`, `installments`, `validUntil`, `interestRate`, `installmentAmount`, `installmentShortfall`, `firstDueDate` | none |
| Approval and credit | `approvalLevel`, `nleadsRef`, `creditResult`, `creditResultReason`, `creditResultAt` | none |
| Booking and plan | `bookedAt`, `bookingDifference`, `signatureStatus`, `installmentsPaid` | `installmentsPaid` yes; the rest no |
| Outcome | `outcome`, `outcomeAt` | none |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF-TRT field names in camelCase; the mapping is one to one and is checked by the drift test. `TreatmentUpdate` of TSD T-A.2 is not published here, because the draft-terms change belongs to RWB-S2-E3003-CON.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the writer behind `decisionLogId` and declares no record element | referred to; the consuming story carries the dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the base of this resource is `/api/recovery/treatment/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-03 is named and not declared: the record is the library's and the only trace on the resource is `decisionLogId`. DP-19 is the route the two screens use and is the platform edge story's. DP-01 and DP-15 stand behind the DDL template as the schema and migration rules and add no dependency. The embedded Drools runtime and the rule packages, the access guard, the outbox and inbox library and the workflow kit are the service template's wave-0 capabilities, so nothing this contract refers to adds a build dependency of its own (ASM-3063, ASM-3064).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| TreatmentOpenApi | Document | The base, the two operations, the schemas, the security, the error set and the versioning section (BR1 to BR4, BR6, BR9) |
| TreatmentSchema | Published schema | `TreatmentRequest` and `Treatment` with the DF-TRT elements and the required set (BR2, BR3) |
| TreatmentDdlTemplate | Resource | The `treatment` DDL: columns, types, keys, indexes and standard columns (BR5) |
| ProblemEnvelope | Reused schema | The platform RFC 9457 problem document with the `messageId` extension (BR6) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR7) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers used by every consuming build (AC6) |
| DriftTest | Test asset | The comparison of a consuming build against sections 12 and 13 (BR9, AC6) |

**Database.** The template creates `treatment` in `rwb_treatment` only, with the physical types of TSD S2 T3.1 and the standard columns of T3.0. `case_id` and `decision_log_id` are cross references with an index each and no foreign key, and no other schema is named in the template. The template is applied by the service's own Flyway sequence and never edits an applied migration (DP-15). The agreements and plan timers are not created here.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR4). The capability area and the rights are declared per operation and their role lists are rwb-access data (BR8). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the two operations; lint the paths and the rights (AC1).
2. Write the two schemas with the element mapping, the required set, the enumeration rule and the example; validate the example (AC2).
3. Write the DDL template and apply it twice in two throwaway schemas; assert the columns, the keys, the widths and the absence of a cross-schema key (AC3).
4. Write the error section with the problem envelope and the four message identifiers, and the `Idempotency-Key` rule (AC4).
5. Write the versioning and pinning section with one compatible and one breaking example (AC5).
6. Generate the fake set and the drift test, and wire the drift test into the build of RWB-S2-E3001-APP and of the four sibling stories (AC6).
7. Publish v1 and record the pinned version of this contract and of each consuming story (AC5).

**Feature flag.** `rwb.treatment.create-record-contract`.

**Done when.** The document lints, the two schemas validate, the template applies twice, the fake answers every status including the conflict and the repeated key, the drift test is green on the build of this story and of RWB-S2-E3001-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P4-002 | The caller's role does not hold the right of the operation | You cannot {action} here. Your role does not include it. | 403, problem body with `messageId` MSG-P4-002 |
| MSG-P4-003 | The case or the treatment is outside the caller's scope, or does not exist | This case is not in your scope. | 404, problem body with `messageId` MSG-P4-003 |
| MSG-P7-009 | A treatment field is refused | The decision record was refused: {field} is missing or not valid. | 422, problem body with `messageId` MSG-P7-009 and `field` |
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. | 422, problem body with `messageId` MSG-GEN-001 and `field` |
| MSG-GEN-006 | The service is unavailable | {system} is not available. Your request is queued and will be retried. | 503, problem body with `messageId` MSG-GEN-006 |

The four texts are the legacy and platform texts carried unchanged, and this contract adds no message identifier of its own. The 401 carries the platform authentication problem and no business message. The 409's message text is not stated in any source read for this key and is Not specified in the source documents (GAP-1869; ASM-3065); the contract fixes only its status, its cause and its `messageId` slot. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: it publishes a resource. SCR-14 Treatment record (Draft; submitted; approved; booked; broken; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8465)) and SCR-15 Settlement offer (Draft; below floor; approved; sent; accepted; empty, loading, error and no access: Not specified in the source documents (CG-ALL-8466)) are reached through the gateway-bff composite route, which calls this resource and the case read in one hop each (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this contract fixes only the elements the read returns.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S2-E3001-CON-01 | AC1 | Contract | The document linted: the base, the two operations, the rights, the bearer scheme, and a third operation and an old-base path refused |
| TC-S2-E3001-CON-02 | AC2 | Contract | The two schemas validated against the DF-TRT elements, the required set, the list codes and the example; an unknown element, a missing required element and a status element refused |
| TC-S2-E3001-CON-03 | AC3 | Component | The template applied in two throwaway schemas; the standard columns, the types, the keys, the widths and the absence of a cross-schema key asserted; a drifted hand-written table refused |
| TC-S2-E3001-CON-04 | AC4 | Contract | One problem body per status on each operation, the four message identifiers, the `Idempotency-Key` header required on the POST and refused absent |
| TC-S2-E3001-CON-05 | AC5, AC6 | Component | A compatible change and a breaking change against the registry fake; the fake answering the success, refusal, conflict, unavailable and repeated-key answers; the drift test on a consuming build |
| TC-S2-E3001-CON-06 | AC3 | Component | Boundary: the tables of section 12.7 applied in rwb_treatment only; the seven standard columns and no table of another service asserted (ASM-3438) |
| TC-S2-E3001-CON-07 | AC7 | Contract | A value fixed by no source published as the working read; the gap message with GAP-1869 and ASM-3065 asserted |

The legacy test set TC-E3-001-01 to TC-E3-001-06 is carried by RWB-S2-E3001-APP and by the wave 2 integration harness, and these five are the contract's own tests; no legacy id is renumbered here.

### 17. Guardrails

- No business value in the contract: the list members, the row states, the rights and the message texts are values in force, and the document names their codes only (BR4).
- No personal data in a schema, an example, a fake or a log: `proposedBy` and `createdBy` are references, the case is an identifier, and the personal-data scan fails the build otherwise.
- No cross-schema reference in the template and no foreign key across services: `case_id` and `decision_log_id` are cross references, and the boundary test fails the build.
- No case status, no case table and no case column in any schema of this resource (ASM-3062; DP-01).
- No decision-record element and no decision code list: the record is the library's, `decisionLogId` is its only trace, and the code is the rule ID and version in force (DP-03).
- No path outside the base and no operation of a sibling: the offer, the draft-terms change, the submit and the approval envelope are named as out of scope and never declared.
- A published version is never edited in place: a breaking change raises major version 2 under a new base segment with a migration note (BR9).
- The agreements, the settlement and deed-in-lieu agreements and the plan timers are not published, because no source gives them a field list.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-001 | A restructure proposed in the collections system reaches the restructuring officer with the case, and the case does not leave the Workbench | Business Requirements Program v5, section 5.9 | FEAT-TRT-01 | 07 Route, settle and claim | BR1 to BR11; DP-13 | TC-S2-E3001-CON-01 to TC-S2-E3001-CON-05 |
| Legacy test set RWB-E3-001 | TC-E3-001-01, TC-E3-001-02, TC-E3-001-03, TC-E3-001-04, TC-E3-001-05, TC-E3-001-06 | Business Requirements Program v5, section 5.9 | FEAT-TRT-01 | 07 Route, settle and claim | R-RES-01, R-RES-10 | Executed by RWB-S2-E3001-APP and the wave 2 harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S2-E3001-APP | App development | H consumer: implements the two operations, the row and the stage against this contract and its fake |
| RWB-S2-E3002-APP, RWB-S2-E3002-CON | App development, Contract | Sibling: the settlement offer, its range and its own operation; this contract declares none of it |
| RWB-S2-E3003-APP, RWB-S2-E3003-CON | App development, Contract | Sibling: the approval below the floor, the approval envelope and the draft-terms change |
| RWB-S2-E3004-APP, RWB-S2-E3004-CON | App development, Contract | Sibling: the TDR plan body, the plan timers and the closing event |
| RWB-S2-E3005-APP | App development | Sibling: the ACE affordability pre-assessment on a treatment |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library behind `decisionLogId`; this contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route the two screens use |
| RWB-PLT-E1044-CON | Contract | Referred to: the per-service Flyway sequence that applies the DDL template |
| RWB-P3-E2004-CON, P3 rwb-case | Contract, App development | Referred to: the case of record, the case signal and the status this resource never carries |
| P7 rwb-decision | App development | Referred to: the rule packages and the rule versions a treatment records |
| RWB-ITG-W2 | Integration | The end-to-end proof of the resource against the live owners, held by the wave 2 harness |

### 19. Out of scope

- The implementation behind the contract — the handlers, the repository, the workflow, the activities and the row write: RWB-S2-E3001-APP.
- The offer operation and the settlement range: RWB-S2-E3002-CON and RWB-S2-E3002-APP.
- The approval envelope, the draft-terms change (`TreatmentUpdate`, PATCH) and the submit-for-approval operation: RWB-S2-E3003-CON and RWB-S2-E3003-APP.
- The TDR plan body, its installments and its plan timers: RWB-S2-E3004-CON and RWB-S2-E3004-APP.
- The ACE affordability pre-assessment and the restructure calculator: RWB-S2-E3005-APP.
- The case status, the case signal and the case table, and the stage outcome report to the case: rwb-case (P3), with the report shape recorded once (GAP-1869; ASM-3065).
- The central decision ledger and the rule packages: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data themselves: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-14 and SCR-15: the platform edge story and the screen owners (DP-19).
- The contracts, settlement and deed-in-lieu agreements and plan timers that Architecture v5 slide 41 places in `rwb_treatment` without a field list (GAP-1869; ASM-3065).
- The deployment of this build: the chart values, the schema and login, the topic and the flag.
- The real cross-service proof of the resource against the live owners: the wave 2 integration harness.
