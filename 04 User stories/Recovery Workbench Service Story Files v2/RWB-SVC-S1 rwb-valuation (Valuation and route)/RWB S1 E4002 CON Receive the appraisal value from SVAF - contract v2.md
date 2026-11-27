# RWB-S1-E4002-CON Receive the appraisal value from SVAF - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-E4-002 for rwb-valuation (S1). The route resource is published on Day 1 on base `/api/recovery/valuation/v1` (DP-13) with the one operation the receipt is reached through, the `RouteRequest` and `Approval` schemas of TSD S1 T-A.2, the `valuation_ext` DDL template and the fakes; the legacy acceptance criteria stay with RWB-S1-E4002-APP and every criterion here is new. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4002-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (18 resolved, 8 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S1-E4002-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-S1-E4002-CON-16) |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Contract version | v1, fixed at the base path /api/recovery/valuation/v1; the OpenAPI info version is Not specified in the source documents (DOR-RWB-S1-E4002-CON-23) |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| Open decisions | DL10 open; assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863 confirmed by the directive; GAP-0430 and GAP-0436 are agreed at the wave 3 entry check, and this contract builds against the fakes until then |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **service contract owner**, I want **the published contract of the route resource of rwb-valuation (S1) — the base `/api/recovery/valuation/v1`, `POST /cases/{caseId}/route` with the entity names `RouteRequest` and `Approval` of TSD S1 T-A.2, its elements named in camelCase after the DF-ACE appraisal fields and the DF-EXT valuation-extension fields it returns, the `valuation_ext` DDL template with the T3.0 standard columns, the error set 401, 403, 404, 409, 422 and 503 with the RFC 9457 problem body, the `Idempotency-Key` rule, the versioning rule and the fakes** instead of the monolith's in-process controller and its one `recovery` schema, so that **RWB-S1-E4002-APP and the eleven sibling application stories of the service build against one frozen shape from Day 1, with no wait on ACE, on rwb-source-data or on any other team**.

This story owns the contract of one resource and one table template, and nothing else:

- the OpenAPI 3.1 document of the route resource: the base, the one operation, the two object schemas, the problem schema reused from the platform, the security and the error set;
- the `valuation_ext` DDL template with the columns of the legacy data row and the standard columns of TSD S1 T3.0, one template each environment applies in this service's own schema, with no cross-schema key;
- the element naming rule (camelCase after the DF-ACE and DF-EXT field identifiers), the required set, the enumeration rule that names a list code and no member, and the rule that the appraisal facts are returned and never stored;
- the `Idempotency-Key` rule on the POST, the compatibility rule and the pinning rule;
- the fake set generated from the document, and the drift test every consuming build runs.

It does not own: the handler, the view read, the freshness gate and the row write, which are RWB-S1-E4002-APP; the appraisal order (FEAT-VAL-01) and the outlier flag (FEAT-VAL-03) with their own operations; the acceptance of the value (FEAT-VAL-04); the COLLINS return, the payoff and the recommendation; the two asset valuation operations of the S1 ownership rows, which are the sibling contracts'; the `recovery.v_ace_*` views, which rwb-source-data owns; the case, which is rwb-case's; the central ledger and the rule packages, which are P7's; the roles and rights data, which are rwb-access's; the composite route, which is the platform edge story's.

### 2. Business rationale

The monolith exposed the route assessment through one controller in the shared process, on a shared base, with the appraisal rows, the case rows and the decision-log rows all in the one `recovery` schema. Three facts follow from the target and make a contract necessary before any code. First, the schema is now `rwb_valuation` with its own login and no cross-schema access, so the Workbench-owned table has to be a template every environment applies rather than one shared migration (DP-01; Architecture v5 slides 39 and 41). Second, the base is now `/api/recovery/valuation/v1`, so a route call no longer collides with the case, the payment or the asset services (DP-13). Third, twelve application stories of this service and the browser through gateway-bff read the route response, so the element names, the required set and the error set have to be frozen before the first of them starts.

TSD S1 already fixes most of it, and this story publishes what the source states rather than inventing: T-A.1 names the path, its right and its first epic, T-A.2 names the purpose, the request `RouteRequest`, the response `Approval`, the error statuses and the `Idempotency-Key` header, T3.1 names the valuation fields with their physical types and lists, and T3.0 names the seven standard record columns. The appraisal itself is ACE's: it is read through `recovery.v_ace_valuation` and is not a table of this schema, so the contract returns those facts and never declares a table for them (DP-05; D-RCV-35; ADR-010).

The contract also fixes what stays out. The appraisal order, the outlier flag and the acceptance are separate operations and separate contracts. The two asset valuation operations the S1 ownership rows carry are not declared here either: they belong to the sibling valuation keys (ASM-4294). No case status and no case element appears in any schema, because the case is rwb-case's and reaches this service as a path identifier (DP-01). The decision record is not a route element: it is written in the same transaction through the RWB-PLT-E1027-CON library (DP-03).

The fake is the Day-1 unblocker. RWB-S1-E4002-APP and the sibling stories can assess a route and read a valuation before a single table exists in an environment, and the drift test turns a private variant of the shape into a build failure rather than a defect found in SIT.

### 3. Preconditions

- TSD S1 T-A.1 fixes the endpoint inventory: API-S1-001, the route assessment on the case path with right U and the `Idempotency-Key` header; the monolith base is renamed to `/api/recovery/valuation/v1` by DP-13.
- TSD S1 T-A.2 fixes the purpose, the request entity `RouteRequest`, the response entity `Approval`, the error statuses and the idempotency rule of the operation this story declares.
- TSD S1 T3.1 fixes the valuation fields with their physical types, required flags and lists, and T3.0 fixes the seven standard record columns; the legacy data row fixes the `valuation_ext` field identifiers DF-EXT-036 to DF-EXT-049.
- TSD S1 T3.2 fixes the list codes LOV-APPRAISAL and LOV-ROUTE; their members are values in force and are not restated in the document (BR-S1-002).
- TSD S1 T6.1 fixes the capability area Treatment and offer and the rights of each role; the document declares the right of the operation and holds no role list.
- The problem envelope is the platform one, RFC 9457 `application/problem+json` with the platform extension members; the style guide fixes its member names and this document reuses them.
- RWB-PLT-E1027-CON publishes the decision-record contract; this document names it as the writer behind the record reference and declares no record element of its own (DP-03).
- The contract artefact coordinates, the publication channel, the retention of a `valuation_ext` row and the nesting of the appraisal elements inside the answer are stated by no source read for this key (GAP-2595; ASM-4295).
- FSD S1 and TSD S1 carry status "In review", and no approval is needed to publish a Draft baseline (ASM-4296).
- No build dependency and no approval stop: a CON story is Day 1 by rule, sits in contract group CG-W3 and is published at status Draft (realignment v1).

### 4. Flow

1. The contract author fixes the base and the one operation of section 12.1, taken character for character from TSD S1 T-A.1 with the DP-13 base.
2. The author fixes the element naming rule: every element of `RouteRequest` and `Approval` is a DF field name in camelCase, the appraisal elements after DF-ACE-187 to DF-ACE-195 and the Workbench flags after DF-EXT-036 to DF-EXT-049.
3. The author fixes the required set: the required column of the TSD for the elements it gives, and the fields the legacy story names as required for the extension row.
4. The author fixes the enumeration rule: an enumerated element names its list code and no member, because the members are values in force (BR-S1-002).
5. The author writes the `valuation_ext` DDL template: the columns, their types, the primary key, the unique key on `valuation_key`, the standard columns and the rule that no key crosses a schema.
6. The author writes the read rule of the resource: the appraisal facts are returned from the view and are never declared as a table, a column or a cache of this schema (BR1).
7. The author writes the error set of the operation with the problem envelope and the message identifiers the platform catalogue already holds, and the `Idempotency-Key` rule.
8. The author writes the versioning and pinning section: a compatible change keeps major version 1, a breaking change raises major version 2 under a new base segment, and v1 is never edited in place.
9. The lint and schema steps run: the document linted against the platform style, every example validated against its schema, the personal-data scan run on the examples, and the template applied twice in two throwaway schemas.
10. The fake set is generated from the document: the success answer, one refused answer per error status, the repeated-key answer and the unavailable answer, all from one example set.
11. The drift test is generated and wired into the build of RWB-S1-E4002-APP and of the sibling stories that read the resource.
12. The document and the fakes are published at v1, and the pinned version of this contract and of each consuming story is recorded.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A path outside `/api/recovery/valuation/v1`, or a second operation, is added to the document | The lint fails the build; the base and the one operation are fixed | None | AC1 |
| X2 | An element is named after anything other than a DF field, or a required element is published optional | The schema validation fails the build | None | AC2 |
| X3 | The template is applied in another service's schema, or a foreign key crosses a schema | The boundary test fails the build; the template creates the table in the applying schema only | None | AC3 |
| X4 | An error body is not a problem document, or a status outside the declared set is returned | The envelope validation fails the build | None | AC4 |
| X5 | A published element is removed, renamed, made required or given a new error status under version 1 | The change raises major version 2 under a new base segment; v1 is never edited in place | None | AC5 |
| X6 | A consuming build ships without the drift test, or ships a private variant of an element | The registry refuses the change and the drift test fails the build | None | AC6 |
| X7 | A value the consumers need is fixed by no source — the nesting of the appraisal elements, the cause of the 409, the retention rule | The value is published as the working read of the assumption and the gap stays open | Not specified in the source documents (GAP-2595; ASM-4295) | AC7 |

X1 to X6 are the lint, schema, boundary, envelope, versioning and drift failures of a contract build; X7 is the boundary this key records, because the source fixes the path, the two entity names and the valuation fields, and not the nesting, the conflict cause or the retention.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes a document, a DDL template and a fake set; builds against nothing, reads no business data and starts on Day 1 |
| Negotiable | The element order, the example values, the index list and the fake technology are open until v1 is frozen; the base, the operation, the entity names, the error set and the versioning rule are fixed |
| Valuable | Unblocks RWB-S1-E4002-APP and the sibling stories on Day 1 and keeps one route shape and one valuation-extension table for the whole service |
| Estimable | One OpenAPI document, one schema pair, one DDL template, one error set, one versioning rule and one fake set |
| Small | One sprint for the document, the template, the fakes and the drift test |
| Testable | Each criterion of section 7 is one lint, schema or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: route resource contract

  Background:
    Given the route resource contract document is published with major version 1
    Given the service has one schema, rwb_valuation, and one login of its own
    Given the contract declares the one operation of TSD S1 T-A.1 and nothing more

  Scenario: AC1 The document publishes the base and the one operation, and nothing else (new, D-RCV-60)
    Given the OpenAPI document of the route resource
    When it is linted against the platform contract style rules
    Then it declares the server base /api/recovery/valuation/v1 and no path on the monolith base
    Then it declares POST /cases/{caseId}/route with the request body RouteRequest and the response Approval
    Then it declares no other path: the appraisal order, the outlier flag, the acceptance and the two asset valuation operations are not in the document
    Then the operation declares the capability area Treatment and offer with right U, the bearer security scheme and the scope rule
    Then a path outside the base, or a second operation, fails the lint

  Scenario: AC2 The schemas carry the DF elements, the required set and no list member (new, D-RCV-60)
    Given the schema section of the document and its worked example
    When both schemas are validated and the example is checked against them
    Then RouteRequest and Approval are the two object schemas of this resource, with the platform problem schema reused and not redeclared
    Then every element of both schemas is a DF field name in camelCase: the appraisal elements after DF-ACE-187 to DF-ACE-195 and the Workbench flags after DF-EXT-036 to DF-EXT-049
    Then caseId is taken from the path on the POST and is not repeated in RouteRequest
    Then appraisalType names LOV-APPRAISAL and the route code names LOV-ROUTE, and no member value is published
    Then no appraisal table, no appraisal column, no case status and no decision-record element is declared
    Then the validation fails on an unknown element, on a missing required element and on a status element added to the body

  Scenario: AC3 The valuation_ext DDL template creates the table with the standard columns and no cross-schema key (new, D-RCV-60)
    Given the DDL template of the contract
    When it is applied twice, in two throwaway schemas, through the service's own Flyway sequence
    Then it creates valuation_ext in the applying schema only, with the primary key on id and a unique key on valuation_key
    Then it carries the fields the legacy data row names from DF-EXT-036 to DF-EXT-049, with stale_flag and age_days as the TSD types them
    Then it carries the standard columns is_active, state, version, created_at, created_by, updated_at and updated_by
    Then no column holds an appraisal fact read from v_ace_valuation, and no foreign key points into a view or another schema
    Then a hand-written table that drifts from the template fails the drift test

  Scenario: AC4 The error set, the problem envelope and the Idempotency-Key are fixed (new, D-RCV-60)
    Given the error section of the document
    When one refused answer per status is validated against it
    Then the POST declares 401, 403, 404, 409, 422 and 503
    Then every error body is application/problem+json with type, title, status, detail, instance and the messageId extension
    Then 403 carries MSG-P4-002, 422 carries MSG-GEN-001 with the field name and 503 carries MSG-GEN-006
    Then the stale data product of VR-S1-002-1 is carried as MSG-P1-001 with the product and the date placeholders
    Then the POST declares Idempotency-Key as a required header
    Then an error body that is not a problem document and a POST without the header both fail the validation

  Scenario: AC5 Versioning separates a compatible change from a new major version, and the consumer pins (new, D-RCV-60)
    Given the versioning section of the document
    When a change is proposed to a published element
    Then an added optional element keeps major version 1 and is accepted by the registry in BACKWARD mode
    Then a removed element, a new required element, a renamed element, a new error status or a path change raises major version 2 under a new base segment
    Then v1 is never edited in place and stays readable after v2 is published
    Then each consuming story pins the published version and a private variant fails its drift test
    Then the document records the version pinned by RWB-S1-E4002-APP

  Scenario: AC6 The fake answers the document and the drift test catches every difference (new, D-RCV-60)
    Given the fake set generated from the document
    When the contract test runs the route fake, the problem fakes, the template application and the drift test
    Then the route fake answers a POST with 200 and an Approval carrying the appraisal facts of the fixture and the Workbench flags
    Then it answers a refused call with 403 and 422, an unknown case with 404, a conflict with 409 and an unavailable service with 503
    Then it returns the first answer for a repeated Idempotency-Key and never a second result
    Then the template application proves the table twice in two schemas
    Then the drift test fails on any difference between the fake, the template and sections 12 and 13 of the document

  Scenario: AC7 A value fixed by no source is published as the working read and the gap stays open (new, D-RCV-60)
    Given a consumer needs a value that no source fixes: the nesting of the appraisal elements, the cause of the 409 or the retention rule
    When the document is validated and reviewed
    Then the value is published as the working read of ASM-4295 and not as a fixed value
    Then the gap GAP-2595 stays open and its placeholder reads Not specified in the source documents (GAP-2595; ASM-4295)
    Then no nesting, conflict cause or retention rule is invented in the document
```

These seven criteria are new and test only the contract deliverable. **The legacy acceptance criteria of RWB-E4-002 stay with RWB-S1-E4002-APP** and are not repeated here, and every identifier, path, entity name, field identifier and status is taken from TSD S1 T-A.1, T-A.2, T3.1 and T3.2 and the legacy data row, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The route resource is published on one base, `/api/recovery/valuation/v1`, with exactly one operation: the route assessment and its answer | TSD S1 T-A.1; DP-13 |
| BR2 | The two schemas are `RouteRequest` and `Approval`, and every element is a DF field name in camelCase; the appraisal elements sit as one flat group inside `Approval` (working read, GAP-2595) | TSD S1 T-A.2, T3.1; legacy RWB-E4-002 data |
| BR3 | `caseId` comes from the path on the POST and is not repeated in the body; the required set is the required column of the TSD for each element it gives | TSD S1 T-A.2 |
| BR4 | An enumerated element names its list code and no member: appraisalType names LOV-APPRAISAL and the route code names LOV-ROUTE | TSD S1 T3.2; BR-S1-002 |
| BR5 | The appraisal facts are returned from `recovery.v_ace_valuation` and are never declared as a table, a column or a cache of `rwb_valuation` | FSD S1 A2.2; DP-05; D-RCV-35; ADR-010 |
| BR6 | The `valuation_ext` DDL template carries the fields DF-EXT-036 to DF-EXT-049 with the standard columns of T3.0, a unique key on `valuation_key`, and creates the table in the applying schema only | DP-01; TSD S1 T3.0, T3.1 |
| BR7 | The error set is fixed per operation, and every error body is an RFC 9457 problem document that names its `messageId`; the freshness message MSG-P1-001 is part of the declared set | TSD S1 T-A.2; FSD S1 A2.2.3.1 |
| BR8 | The operation needs right U in Treatment and offer; the right is declared in the document and checked by the platform guard, and no check is declared in code | TSD S1 T6.1 |
| BR9 | The POST is idempotent by the `Idempotency-Key` header: a repeated key returns the first answer and writes no second result | TSD S1 T-A.2 |
| BR10 | A published element is never edited in place: a compatible change keeps major version 1 and a breaking change raises major version 2 under a new base segment | Template and Rules §R7.2; §R5.4 class C |
| BR11 | The document declares no case status, no case table and no decision-record element: the case is rwb-case's and the record is the library's, and the only trace on the resource is the record reference | DP-01; DP-03; GAP-2595; ASM-4295 |

**Where each rule lives in the target.** BR1 and BR2 are the paths and the schemas of the document and its lint. BR3 and BR4 are the required set and the enumeration rule. BR5 is the read rule of AC2 and the absence of any appraisal column in the template. BR6 is the DDL template and its boundary test. BR7 is the error section and the platform problem schema it reuses. BR8 is the `security` section; the guard is the platform library's and the contract adds no dependency for it. BR9 is the header rule and the fake's repeated-key answer. BR10 is the versioning section. BR11 is the boundary between the resource and the case of record.

**Covered by.** BR1 AC1; BR2 AC2; BR3 AC2; BR4 AC2; BR5 AC2 and AC3; BR6 AC3; BR7 AC4; BR8 AC1; BR9 AC4 and AC6; BR10 AC5; BR11 AC2.

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are touched and neither is fixed here.

| Object | State | Meaning in the contract |
|---|---|---|
| `valuation_ext` row | receipt state | The row a receipt writes: `stale_flag` and `age_days` set, `accepted` at its receipt value, `accepted_at` and `accepted_by` absent |
| `valuation_ext` row | accepted | The state FEAT-VAL-04 writes; the document carries `accepted`, `accepted_at` and `accepted_by` as elements and fixes no value |
| Contract | v1 | The published version every consuming story pins |
| Contract | v2 | Raised by a breaking change under a new base segment; v1 stays readable and is never edited |

The row lifecycle itself is RWB-S1-E4002-APP's and the sibling stories'; the transition table of a case is rwb-case's and appears nowhere in this document. The `state` column is declared as varchar(40) with no check constraint, so a new row state is a data change and not a contract change.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the document, the DDL template and the fakes |
| The service owner of rwb-valuation | Approves a breaking change and freezes a version |
| The twelve application stories of this service | Consume the contract, pin the version and raise a change request rather than a private variant |
| The rwb-source-data owner (P1) | Confirms which view the appraisal facts come from and that the resource declares no copy of them |
| The rwb-case owner (P3) | Confirms that no case status and no case table is declared here and that the case arrives as the path identifier |
| The rwb-decision owner (P7) | Confirms the rule ID and the rule version as the values a decision record carries, and that no decision code list is published here |
| The rwb-access owner (P4) | Confirms the capability area and the right the operation declares |
| The rwb-access authorise check (DP-08) | Checks right U in Treatment and offer on each call; its operation name is Not specified in the source documents (DOR-RWB-S1-E4002-CON-6) |
| The platform API owner | Owns the problem envelope, the style guide and the registry this document validates against |
| RW-CASEOWN, RW-RESTRUCT, RW-SPECIAL, RW-GUARANT and the other roles of TSD S1 T6.1 | Call the operation and hold the rights the document declares; they hold no authoring right here |
| No delegation of authority level applies | A resource contract is a technical artefact, not a route decision |

No personal name, no email address and no credential appears in the document, the template, an example or a fake. The valuer is a partner reference, never a name.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The document publishes paths, element names, types, a required set, an error set and list codes; no customer, account, asset or appraisal value appears beyond the synthetic example | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Shapes published | `RouteRequest` and `Approval` with the appraisal elements of DF-ACE-187 to DF-ACE-195 and the Workbench flags of DF-EXT-036 to DF-EXT-049, the problem schema reused from the platform, and the `valuation_ext` DDL template | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Personal data | None. The request and the answer carry identifiers, codes, dates and amounts; no account number, national identifier, name or document content appears | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Tables published | `valuation_ext` only, as a DDL template applied in `rwb_valuation`; the library object `decision_record` is applied in the same schema under RWB-PLT-E1027-CON and is named, not declared | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Views referred to | `recovery.v_ace_valuation`, `recovery.v_ace_collateral` and `recovery.v_ace_batch_status`, owned by rwb-source-data, read only and never published as tables (DP-05). The criteria and test data read no view; the fake fixture stands in for the appraisal facts. The receipt runs inside POST /cases/{caseId}/route with no schedule and no event | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Field identifiers | DF-EXT-036 to DF-EXT-049 for the table, DF-ACE-187 to DF-ACE-195 for the appraisal facts returned; the list codes LOV-APPRAISAL and LOV-ROUTE | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Retention | The retention and archive rule of a `valuation_ext` row is Not specified in the source documents (GAP-2595; ASM-4295) | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |
| Reference data | LOV-APPRAISAL and LOV-ROUTE are read by list code only, under the reference-data contract DP-06 and DP-07; this contract reads no parameter, and the parameter key is Not specified in the source documents (DOR-RWB-S1-E4002-CON-20) | Not specified in the source documents (DOR-RWB-S1-E4002-CON-7) |

The document is the one place where a business value could leak, so it fixes that a list is named by its code and never by its members, that a case status is not a route element, and that the examples carry synthetic identifiers only.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This story publishes the one operation.

| Method | Path | Request | Response | Access | Idempotency | Errors |
|---|---|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest`; `caseId` from the path | 200 with `Approval`, carrying the appraisal facts read and the Workbench flags | Treatment and offer U, scope applied | `Idempotency-Key` header required | 401, 403, 404, 409, 422, 503 |

The path, the purpose, the request and response entities, the right and the error statuses are those of TSD S1 T-A.1 and T-A.2, with the base renamed by DP-13. The appraisal order, the outlier flag, the acceptance, the recommendation and the approval inside the limit are not declared here; each is a sibling contract of this service. The two asset valuation operations the S1 ownership rows carry are the sibling contracts' too (ASM-4294).

#### 12.2 REST operations consumed

None — a contract document calls no service. The appraisal arrives through the view, the case through the path, the rule package through the workflow's own package read, and the rights and lists through the platform client libraries. Every one of them is a fact of the consuming story, and this contract adds no dependency of its own.

#### 12.3 Events published

None. The service topic is `rwb.valuation.events.v1` with event names `rwb.valuation.<Event>.v1` (DP-14) and the ownership rows give S1 no event; the `DecisionRecorded` event of the library is written in the caller's transaction under RWB-PLT-E1027-CON and is not a type of this contract (DP-03).

#### 12.4 Events consumed

None. The freshness of the valuation product is a read of `v_ace_batch_status`, not a subscription; the package event is consumed by the application story and never by a document.

#### 12.5 Workflows and activities

None — the contract defines no workflow and no activity. `RouteDecisionWorkflow` is the service's one workflow in the ownership rows, belongs to the route-decision story of the service, and calls the operation this document describes; the document fixes the resource and not the workflow.

#### 12.6 Schedules

None. No Temporal Schedule and no Quartz job is declared.

#### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `valuation_ext` | `rwb_valuation` | S1 | The DDL template of section 13: DF-EXT-036 to DF-EXT-049, the seven standard columns, the primary key on `id`, the unique key on `valuation_key` and no cross-schema key (DP-01) |
| `decision_record` | `rwb_valuation` | PLT library object applied in this schema | Named only: the shape is RWB-PLT-E1027-CON's and the row is written in the caller's transaction (DP-03) |

The ACE views are named and not published: no appraisal table, column or cache is declared in `rwb_valuation`, and no table of another service is declared, read or keyed (DP-05). The Ownership Map lists no table for S1, so the table is published here on the assumption that the map's S1 table row is incomplete (GAP-2594; ASM-4291).

#### 12.8 Contract fakes

| Fake | Serves | Answers |
|---|---|---|
| Route resource fake | The operation of 12.1 | A 200 answer carrying the appraisal facts of the fixture and the flags; a 403 and a 422 refusal; a 404 for an unknown case; a 409 conflict; a 503 unavailability |
| rwb-source-data contract fake | The appraisal reads in the Given and test-data lines | The appraisal facts of the fixture as the rwb-source-data contract returns them, with a freshness answer; no ACE view is read or set up |
| Repeated-key fake | The `Idempotency-Key` rule | The first answer returned again for the same key, with no second result |
| Template application | The `valuation_ext` DDL template | The table created twice in two throwaway schemas, with the unique key, the standard columns and no cross-schema reference |
| Problem fakes | The problem envelope | One `application/problem+json` body per error status, each with its `messageId` |
| Registry and drift fake | The compatibility rule | One accepted and one refused body in BACKWARD mode, and a drift failure for a private variant of an element |

Every fake answers from the same example set as the document, so a change to the contract shows up as a contract-test failure in a consuming build rather than as a surprise in SIT.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 1 operation on `/api/recovery/valuation/v1` | 0 | OpenAPI 3.1, RFC 9457 problem bodies; the browser reaches it through gateway-bff (DP-19) |
| Kafka | 0 | 0 | The service topic is named and no event type is declared here |
| Temporal | 0 | 0 | The contract declares no workflow and no activity |
| File | 0 | 0 | No file crosses the contract; ACE ingests the SVAF feed |
| SQL view | 0 | 0 | The views are referred to as the source of the returned facts and are not declared |

### 13. Solution plan

**Package.** Contract artefact of the service: the OpenAPI 3.1 document of the route resource, the `RouteRequest` and `Approval` schemas with the published types in `th.co.scb.ace.workbench.recovery.valuation.api`, the `valuation_ext` DDL template as a resource, and the fake set with the drift test. The implementation behind it is RWB-S1-E4002-APP. The artefact coordinates and the publication channel are Not specified in the source documents (GAP-2595; ASM-4295).

**Element surface**

| Element group | Elements | Required |
|---|---|---|
| Identity | `caseId`, the record reference | `caseId` from the path; the rest no |
| Appraisal facts, returned and never stored | `valuationKey`, `assetKey`, `appraisalNo`, `forcedSaleValue`, `appraisedValue`, `appraisalDate` and the appraisal type, after DF-ACE-187 to DF-ACE-195 | the appraisal number, the type and the date yes; the forced sale value no |
| Workbench decision | `accepted`, `acceptedAt`, `acceptedBy`, `staleFlag`, `ageDays`, `valuerPartnerId`, after DF-EXT-036 to DF-EXT-049 | `staleFlag` and `ageDays` yes; the acceptance trio no on a receipt |
| Route decision | the route code from LOV-ROUTE and the override reason, after TSD S1 T-A.2 | the route code yes; the override reason only on an override |
| Standard | `state`, `version`, `createdAt`, `createdBy`, `updatedAt`, `updatedBy`, `isActive` | none in the body; they are columns of the template |

The element names are the DF field names in camelCase; the mapping is one to one and is checked by the drift test. The nesting of the appraisal group inside `Approval` is Not specified in the source documents (GAP-2595; ASM-4295) and is fixed at v1 as one group, with the elements flat.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the document names the writer behind the record reference | referred to; the consuming story carries the dependency |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | The appraisal facts come from `v_ace_valuation`; the document declares no copy of them | none |
| DP-13 | the monolith API base | `/api/recovery/valuation/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route; the resource is reached through it and the contract declares no composite route | referred to; the consuming story carries the dependency |

DP-13 is the pattern this story publishes. DP-05 is why the `Approval` schema carries the appraisal facts and the template carries no column for them. DP-03 is named and not declared. DP-19 is the route SCR-13 uses and is the platform edge story's. DP-01 stands behind the DDL template as the schema rule and adds no dependency; the guard, the reference data and the workflow kit are the service template's wave-0 capabilities.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RouteOpenApi | Document | The base, the one operation, the schemas, the security, the error set and the versioning section (BR1 to BR4, BR7, BR10) |
| RouteSchema | Published schema | `RouteRequest` and `Approval` with the DF elements and the required set (BR2, BR3) |
| ValuationExtDdlTemplate | Resource | The `valuation_ext` DDL: columns, types, keys and standard columns (BR6) |
| ProblemEnvelope | Reused schema | The platform RFC 9457 problem document with the `messageId` extension (BR7) |
| IdempotencyRule | Document | The `Idempotency-Key` header, the repeated-key answer and its counting (BR9) |
| Fake set and fixtures | Test asset | The success, refusal, conflict, unavailable and repeated-key answers every consuming build uses (AC6) |
| DriftTest | Test asset | The comparison of a consuming build against sections 12 and 13 (BR10, AC6) |

**Database.** The template creates `valuation_ext` in `rwb_valuation` only, with the primary key on `id`, a unique key on `valuation_key`, an index on `asset_key`, `stale_flag` and `age_days` as the TSD types them, and the standard columns of T3.0. No column holds an appraisal fact and no foreign key points into a view or another schema (DP-01, DP-05). The template is applied by the service's own Flyway sequence and never edits an applied migration.

**Configuration and reference data.** The list codes are named and their members are read as values in force with their version (BR4). The capability area and the right are declared per operation and their role lists are rwb-access data (BR8). The problem envelope, its member names and its `messageId` extension are the platform style guide's and are reused, not redeclared.

**Build steps**

1. Write the document with the base and the one operation; lint the path and the right (AC1).
2. Write the two schemas with the element mapping, the required set, the enumeration rule and the example; validate the example (AC2).
3. Write the DDL template and apply it twice in two throwaway schemas; assert the columns, the unique key, the widths and the absence of a cross-schema key (AC3).
4. Write the error section with the problem envelope and the message identifiers, and the `Idempotency-Key` rule (AC4).
5. Write the versioning and pinning section with one compatible and one breaking example (AC5).
6. Generate the fake set and the drift test, and wire the drift test into the build of RWB-S1-E4002-APP and of the sibling stories (AC6).
7. Publish v1 and record the pinned version of this contract and of each consuming story (AC5).

**Feature flag.** `rwb.valuation.route-contract`.

**Done when.** The document lints, the two schemas validate, the template applies twice, the fake answers every status including the conflict and the repeated key, the drift test is green on the build of this story and of RWB-S1-E4002-APP, and v1 is published with the pinned versions recorded.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-GEN-001 | A required field of the request is missing | Enter {field}. | 422, problem body with `messageId` MSG-GEN-001 and `field` |
| MSG-P1-001 | The valuation product is stale for the business date | {product} is from {date}. Today's load has not arrived. | 422 or 503 as the consuming story's freshness gate answers, with `messageId` MSG-P1-001 and the product and the date |
| MSG-P4-002 | The caller's role does not hold right U in Treatment and offer | You cannot {action} here. Your role does not include it. | 403, problem body with `messageId` MSG-P4-002 |
| MSG-GEN-006 | The service or the ACE view is unavailable | {system} is not available. Your request is queued and will be retried. | 503, problem body with `messageId` MSG-GEN-006 |

The texts are the legacy, FSD and platform texts carried unchanged, and this contract adds no message identifier of its own. The 401 carries the platform authentication problem and no business message. The 404 and the 409 texts are not stated in any source read for this key: the contract fixes their statuses, their causes and their `messageId` slots, and the wording is Not specified in the source documents (GAP-2595; ASM-4295). Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story, and the contract declares none: it publishes a resource. SCR-13 Route decision (loading; recommendation; overridden; submitted; empty, error and no access: Not specified in the source documents (CG-ALL-7965)) is reached through the gateway-bff composite route, which calls this resource and the case read in one hop each (DP-19). The screen field list and the composite route specification belong to the platform edge story and the screen owners; this contract fixes only the elements the operation returns.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-S1-E4002-CON-01 | AC1 | Contract | The document linted: the base, the one operation, the right, the bearer scheme, and a second operation and a monolith-base path refused |
| TC-S1-E4002-CON-02 | AC2 | Contract | The two schemas validated against the DF elements, the required set, the list codes and the example; an unknown element, a missing required element and a status element refused |
| TC-S1-E4002-CON-03 | AC3 | Component | The template applied in two throwaway schemas; the columns, the unique key, the standard columns and the absence of a cross-schema key asserted; a drifted hand-written table refused |
| TC-S1-E4002-CON-04 | AC4 | Contract | One problem body per status, the four message identifiers, the `Idempotency-Key` header required and refused absent |
| TC-S1-E4002-CON-05 | AC5, AC6 | Component | A compatible and a breaking change against the registry fake; the fake answering the success, refusal, conflict, unavailable and repeated-key answers; the drift test on a consuming build |
| TC-S1-E4002-CON-06 | 12.7 tables | Component | The `valuation_ext` template and the tables of 12.7 checked for the primary key on `id`, the unique key on `valuation_key` and no cross-schema key; a duplicate `valuation_key` refused |
| TC-S1-E4002-CON-07 | AC7 | Contract | A consumer need that no source fixes (the nesting, the 409 cause or the retention rule) reviewed; the value published as the working read of ASM-4295, GAP-2595 left open, nothing invented |

The legacy test set TC-E4-002-01 to TC-E4-002-04 is carried by RWB-S1-E4002-APP and by the wave 3 integration harness, and these five are the contract's own tests; no legacy id is renumbered here.

### 17. Guardrails

- No business value in the contract: the list members, the row states, the limits and the message texts are values in force, and the document names their codes only (BR4).
- No personal data in a schema, an example, a fake or a log: the case and the asset are identifiers, the valuer is a partner reference, and the personal-data scan fails the build otherwise.
- No appraisal fact in the table: `valuation_ext` carries the Workbench decision and the flags only, and the drift test fails on a column that repeats `appraised_value`, `appraisal_no` or `appraisal_date` (DP-05).
- No cross-schema reference in the template and no foreign key into a view: the boundary test fails the build.
- No case status, no case table and no case column in any schema of this resource (DP-01).
- No decision-record element and no decision code list: the record is the library's, the reference is its only trace, and the code is the rule ID and version in force (DP-03).
- No path outside the base and no operation of a sibling: the order, the outlier flag, the acceptance and the two asset valuation operations are named as out of scope and never declared.
- A published version is never edited in place: a breaking change raises major version 2 under a new base segment with a migration note (BR10).
- The appraisal view is referred to and never published, and the contract never grants a read of it.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| None stated for FEAT-VAL-02 (GAP-2594; ASM-4295) | The FSD's requirement table carries no row for the receipt; the contract publishes the route resource the receipt is reached through | Business Requirements Program v5, section 5; FSD S1 Requirements served | FEAT-VAL-02 | D6 Route decision | VR-S1-002-1, BR-S1-002; BR1 to BR11 | TC-S1-E4002-CON-01 to TC-S1-E4002-CON-05 |
| Legacy test set RWB-E4-002 | TC-E4-002-01, TC-E4-002-02, TC-E4-002-03, TC-E4-002-04 | Business Requirements Program v5, section 5 | FEAT-VAL-02 | D6 Route decision | VR-S1-002-1 | Executed by RWB-S1-E4002-APP and the wave 3 harness; not owned here |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-S1-E4002-APP | App development | H consumer: implements the operation, the view read and the row against this contract and its fake |
| RWB-S1-E4001-APP, RWB-S1-E4003-APP, RWB-S1-E4004-APP | App development | Sibling: the appraisal order, the outlier flag and the acceptance, each against its own contract |
| RWB-S1-E4005-APP, RWB-S1-E4006-APP, RWB-S1-E4007-APP, RWB-S1-E4008-APP | App development | Sibling: the COLLINS return, the payoff and range, the recommendation and the approval inside the limit, on the value this resource returns |
| RWB-S1-E4009-APP, RWB-S1-E4010-APP, RWB-S1-E4011-APP, RWB-S1-E4012-APP | App development | Sibling: the committee, the hold, the reconsideration and the route flow start |
| RWB-PLT-E1027-CON | Contract | Referred to: the local decision-record library behind the record reference; this contract adds no build dependency of its own |
| RWB-PLT-N001-CON | Contract | Referred to: the gateway-bff composite route SCR-13 uses |
| P1 rwb-source-data | App development | Referred to: the ACE views the values come from, and the grant the consuming story needs |
| P3 rwb-case | App development | Referred to: the case of record and the case read the composite route composes |
| RWB-ITG-W3 | Integration | The end-to-end proof of the resource against the live views and the live case, held by the wave 3 harness |

### 19. Out of scope

- The implementation behind the contract — the handler, the view read, the freshness gate, the flag and age computation and the row write: RWB-S1-E4002-APP.
- The appraisal order and its SVAF order path: FEAT-VAL-01 and its own contract.
- The outlier flag against market and the last value: FEAT-VAL-03 and its own contract.
- The acceptance of the value and the band it fixes: FEAT-VAL-04 and its own contract.
- The COLLINS return, the payoff and settlement range, the recommendation, the approval inside the limit, the committee, the hold, the reconsideration and the route flow start: FEAT-VAL-05 to FEAT-VAL-12.
- The two asset valuation operations of the S1 ownership rows, which belong to the sibling valuation keys (ASM-4294).
- The `recovery.v_ace_*` views, the ACE ingestion of the SVAF feed and the SELECT grant: ACE and rwb-source-data (P1).
- The case, its status and the case read: rwb-case (P3).
- The central decision ledger and the rule packages: rwb-decision (P7); the local record contract: RWB-PLT-E1027-CON.
- The roles, the rights and the scope data: rwb-access (P4).
- The gateway-bff composite route, the screen field list and the layout of SCR-13: the platform edge story and the screen owners (DP-19).
- The nesting of the appraisal elements, the retention of a row, the wording of the 404 and 409 and the publication coordinates: recorded once (GAP-2595; ASM-4295).
- The real cross-service proof of the resource against the live views and the live case: the wave 3 integration harness.
- The deployment of this build: chart values, the schema and login, the view grants and the flag.
