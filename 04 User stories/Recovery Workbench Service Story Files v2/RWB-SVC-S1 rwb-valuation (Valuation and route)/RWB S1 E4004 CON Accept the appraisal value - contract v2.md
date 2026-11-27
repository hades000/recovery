# RWB-S1-E4004-CON Accept the appraisal value - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4004-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement; not sized in this story; INVEST Small: fits within two weeks |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (path `/api/recovery/valuation/v1`, DP-13) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-004, the baseline the acceptance step of rwb-valuation builds against on Day 1. The baseline declares the acceptance element set of the route operation `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` (DP-13), its band and its case-move answer, the five consumed rows of rwb-source-data, rwb-case, rwb-decision and rwb-access (DP-05), the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. The element list of `RouteRequest` and `Approval` is not published and no source states how the acceptance and the band enter them (GAP-2606; ASM-4307); the acceptance fields carry two candidate shapes and no owner publishes their type or nullability (GAP-2607; ASM-4308); the band policy's row and boundaries are not published (GAP-2605; ASM-4306). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S1-E4004-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 12 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the appraisal-acceptance slice of rwb-valuation, being its acceptance element set on the route operation, its five consumed rows, its decision-record element, its workflow elements, its rights, its error envelope and its fakes, fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the four owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-004. It owns:

- the document that fixes `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1` for the acceptance: `RouteRequest` in, `Approval` out, the `Idempotency-Key`, the rights and the error set (DP-13);
- the acceptance element set: the valuation key, the accepted value, the appraisal date, the acceptance marker and the band in the answer, each with its type, its nullability and its source where a source gives one (GAP-2606; ASM-4307);
- the five consumed rows: the appraisal, outlier-flag and acceptance data product of rwb-source-data, the case state and the case-move answer of rwb-case, the rule-in-force and ledger read of rwb-decision, and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published (DP-05); the valuation fields are read only through the rwb-source-data contract, and no ACE view is read by this service (GAP-1677);
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two acceptance activities on task queue `rwb-valuation`;
- the subject of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19); its empty, loading, error and no-access states are owned by RWB-S1-E4004-APP, and the error set of the route operation (AC5) is the answer they read, with 403 and MSG-P4-002 for no access;
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base.

It does not own: the acceptance behaviour, the band fixing, the decision records, the case-move answer and the screens' behaviour, which are RWB-S1-E4004-APP; the two valuation operations `POST /assets/{assetId}/valuations` and `POST /assets/{assetKey}/valuations`, which are the appraisal-intake baseline RWB-S1-E4002-CON; the ACE appraisal, collateral and acceptance facts, which are rwb-source-data's (P1); the case of record and its valuation states, which are rwb-case's (P3); the rule rows, the band policy and the central ledger, which are rwb-decision's (P7) and rwb-access's (P4); the roles and scopes behind the right, which are rwb-access's (P4); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets the teams start together. Legacy RWB-E4-004 asks the case owner to accept a value that fixes the band the route decision runs on, and to have the result recorded with its rule version, so the step reads facts from three other services, answers a case move to a fourth and writes one record in a fifth. Without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2604; ASM-4305).
- **one hop, one budget.** Each consumed row is a single hop with a 2 s timeout and a breaker; the appraisal is never read from a table and never chained through a second service (DP-05, ADR-020).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (s9).

The business outcome the baseline protects is the one FEAT-VAL-04 of FSD S1 states: the case owner accepts the value and the band the route decision runs on is fixed. The baseline states no outcome and no business value of its own, and no criterion here asserts that a value is accepted or that a band is fixed.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`. The map carries two valuation paths and no source says which is current; neither is declared here, because the intake is RWB-S1-E4002-CON.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights. T-A.2 publishes no field table for either type (GAP-2606; ASM-4307).
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions of this baseline and not in its H row.
- The acceptance fields have two candidate shapes: `accepted`, `accepted_at`, `accepted_by`, `stale_flag` and `age_days` on `recovery.valuation_ext` (DF-EXT-036 to DF-EXT-049) and `accepted`, `stale_flag`, `age_days` on a NEW `valuation` table (DF-COL-018 to DF-COL-027, DF-COL-043, DF-COL-044), while the ownership rows give S1 no table (GAP-2607; ASM-4308).
- The band policy is administered by the product head under FEAT-ADM-04; no source names its row, its identifiers, its boundaries or the answer it travels on (GAP-2605; ASM-4306).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag.

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2 and T6.1, FSD S1 A2.4 rules and field catalog, and the DP table.
2. Every provided operation is declared with its method, path, request, documented answer, rights, idempotency and error set; the acceptance is declared as an element set of the one operation the legacy Endpoints table names.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The acceptance element set is declared with the type and the nullability a source gives, marked optional where no source gives one, and never made required by this baseline.
5. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
6. The workflow and its two acceptance activities are declared with their input, their signals and their outcome elements.
7. The schema, the open lists and the closed lists are published; a closed list is referenced with its identifier and its version and is never enumerated in code.
8. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
9. The compatibility check runs on the draft against the previous tag of this service's baseline family: a breaking change fails it.
10. The document goes to review as Draft; the reviewers are the owners of the four consumed services and the tech lead of the service.
11. On the review's close the document is tagged; the application story and the wave 3 harness start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for an element or a shape the sources do not publish | The row carries the placeholder and its gap and is marked optional; no type and no element is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2, s9 |
| X7 | Two documents claim the same base, topic, queue or path | The owner named in the Ownership Map keeps it and the other document changes | C7 |
| X8 | A source publishes a second shape of an acceptance element | The element is declared once, with the higher-precedence shape, and the other is recorded as a gap | C3, C4 |

X1, X2 and X8 are the paths of an incomplete or conflicting source, X4 to X6 the paths of a baseline moving under a build, and X3 and X7 the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the path, the request, the answer, the rights and the error set are fixed by TSD S1 |
| Valuable | The application story, the harness and four owners build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation with an acceptance element set, five consumed rows, one decision-record element, one workflow with two activities, one subject of SCR-13 and eight fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the appraisal-acceptance slice

  Scenario: AC1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: AC2 The route operation and its acceptance element set are published as declared (new, D-RCV-60)
    Given the operation table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header and the scope rule of T-A.2
    And the acceptance elements carry their type, their nullability, their source and a placeholder where no source publishes one

  Scenario: AC3 The five consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, rwb-case, rwb-decision and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: AC4 The consumed rows are declared as reads and answers, and no foreign table is declared (new, D-RCV-60)
    Given the consumed table and the table-ownership table of the baseline
    When the appraisal, the acceptance, the case-state and the case-move rows are read
    Then each is declared as a consumed read or answer of its owner and never as a table of this service
    And no v_ace_* object, no foreign schema and no foreign foreign key is declared

  Scenario: AC5 The rights and the error envelope are declared per operation (new, D-RCV-60)
    Given the operations the baseline provides
    When the rights and the error set of each operation are read
    Then each names the capability area Treatment and offer and the right of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: AC6 The decision-record element, the workflow elements and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the workflow table and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library, the shared topic and the transaction it joins
    And RouteDecisionWorkflow and its two acceptance activities name their input, their signals and their task queue
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub

  Scenario: AC7 The naming, the publication and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the naming rule, the ownership rows and the event list
    Then one base, one topic, one queue and one login are declared and no monolith base and no foreign topic appear
    And no event is published, because the ownership rows give S1 none, and no Schedule is declared

  Scenario: AC8 Each business rule of section 8 is checked against the draft it governs (new, D-RCV-60)
    Given the business rules BR1 to BR10 of section 8
    When each rule is checked against the draft that it governs
    Then every rule holds, and a rule that is an architecture constraint is checked by a guardrail or boundary test

  Scenario: AC9 The retry and the timeout of each activity of the route workflow are declared (new, D-RCV-60)
    Given the two activities of RouteDecisionWorkflow in the baseline
    When an activity is retried or times out
    Then its retry policy and its timeout are read from the baseline, and where none is published they carry Not specified in the source documents (NEWAC-RWB-S1-E4004-CON-AC4)

  Scenario: AC10 A status change the model does not allow is refused (new, D-RCV-60)
    Given the closed lists and the status model of the baseline
    When a status change the model does not allow is requested
    Then the request is refused with the error set named in AC5 and no change is written
```

The seven criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the lists, the consumed rows, the rights, the envelope, the decision-record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts that a value is accepted, that a band is fixed or that a rule fires.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row and element with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row or an element with no published shape carries the placeholder and its gap, is marked optional, and never receives an invented path, parameter, type or transport | Template and Rules v1 §R9; GAP-2604 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; ACE facts arrive on the rwb-source-data data product and never on a view of this service | DP-05; ADR-020 |
| BR5 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows |
| BR6 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before any answer, and its element is declared once for the service | DP-03 |
| BR7 | No business value is declared in the baseline: the appraisal types, the route codes and the band policy are referenced with their identifier, their list or their version | TSD S1 T3.2; FSD S1 A2.4.3.1 BR-S1-004 |
| BR8 | No personal data in any element, fake, example or log of the baseline; the accepting user is declared as an identifier and not as a name | Template and Rules v1 §R7.2 (s17) |
| BR9 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |
| BR10 | Where two sources give an acceptance element two shapes, the higher-precedence source is declared, the other is recorded as a gap, and the element stays optional until its owner confirms it | Template and Rules v1 §R3; GAP-2607 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every operation, row, element, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the four consumed services are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A row or an element has no published shape | X1, X8 | It carries the placeholder and the gap, and the draft continues |
| In review | A row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the shape of the service's own operation and acceptance elements where no owner speaks, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the appraisal, outlier-flag and acceptance rows, and publishes the operation names when they exist |
| Owner of rwb-case (P3) | Reviews the case-state row and the case-move answer of the route operation |
| Owner of rwb-decision (P7) | Reviews the rule-in-force row and the decision-record element with the platform library |
| Owner of rwb-access (P4) | Reviews the authorise row, the capability area and rights of each declared operation, and the band policy of FEAT-ADM-04 |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of every declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write | BR Field ID |
|---|---|---|---|---|
| The appraisal elements of `v_ace_valuation` (DF-ACE-187 to DF-ACE-195) | P1 (`rwb_source_data`) | The valuation key, the asset key, the appraisal number, type, appraised value, forced sale value and appraisal date; referenced as the data product and not redefined | Consumed | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The acceptance elements of `valuation_ext` (DF-EXT-036 to DF-EXT-049) | P1 data product | `accepted`, `accepted_at`, `accepted_by`, `stale_flag`, `age_days`; declared optional, with the type a source gives and a placeholder where none is given (GAP-2607; ASM-4308) | Consumed and never written by this service; the acceptance has no durable home in the sources (GAP-2603), this service never writes schema rwb_source_data, and OQ-P1-05 (who writes `stale_flag` and `age_days`) stays open (ASM-A6-tables-15) | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The acceptance elements of `valuation` (DF-COL-018 to DF-COL-027, DF-COL-043, DF-COL-044) | S1 declares no table, TSD S1 T3.1 declares one | `accepted`, `stale_flag`, `age_days`; the second shape of the same three facts, recorded and not declared as a table here | Consumed as a reference | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The outlier flag of FEAT-VAL-03 | P1 data product | Field id and owner row Not specified in the source documents (GAP-2604; ASM-4305); declared as an element of the data product answer | Consumed | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The band and its policy version | P4 (`rwb_access`), administered under FEAT-ADM-04 | The band fixed by an accepted value; the identifiers, the boundaries and the row that carries it are Not specified in the source documents (GAP-2605; ASM-4306) | Consumed as data and recorded | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The case elements and the move answer | P3 (`rwb_case`) | The case reference, its valuation state and the answer that applies the move; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | The rule id, the rule version and the route set in force; referenced, not redefined | Consumed | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | The rule id, the rule version, the inputs reference, the outcome and the decided-at time | Written through the library | Not specified in the source documents (DOR-RWB-S1-E4004-CON-7) |

The baseline declares no table of its own, because the Ownership Map gives S1 none while TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2607; ASM-4308). It declares no column, no index and no migration, and it enumerates no business value: every list, code and band is referenced with its identifier and its version. **No personal data** appears in any element, fake or example: the accepting user is an identifier, and every fixture identifier is synthetic. The reference data and parameters are read under DP-06 and DP-07: the closed lists are referenced by identifier and version, the band policy by its identifier and version, and no parameter key or reference-data contract field is named here (Not specified in the source documents (DOR-RWB-S1-E4004-CON-20)). A consumed operation with no published name carries the placeholder and its gap (GAP-2604); its client and fake are built from the documented use, and a published name replaces the placeholder in a minor version (BR2). The acceptance element set is declared as optional elements of the one operation API-S1-001 and not as a second operation; any separate acceptance write is added later by its owner in a minor version with its rights and error set (GAP-2606). Until the owner names the field or table that holds the accepted value, accepted_at and the accepting user (GAP-2603), the acceptance is the decision record and the case move answer.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out, carrying the acceptance of a valuation key with its value and the band in the answer, plus an override reason where the answer departs from the recommendation (API-S1-001) | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |


The acceptance element set of `RouteRequest` is declared as the valuation key, the accepted value and the appraisal date, and of `Approval` as the band, the accepted value and the acceptance marker; each is optional in the baseline, because TSD S1 T-A.2 publishes the two type names and no field table and no source states how the acceptance enters them (GAP-2606; ASM-4307). The two valuation operations of the map belong to the appraisal-intake slice of RWB-S1-E4002-CON and are not declared here.

The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid or unmatched element, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The appraisal, outlier-flag and acceptance data-product read (operation name Not specified in the source documents (GAP-2604; ASM-4305)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraisal of the asset, its value, its date and its type, the outlier flag, the acceptance state of `valuation_ext` and the freshness stamp; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case state and its asset link, which the step checks before an acceptance is recorded; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2604; ASM-4305)) | `/api/recovery/case/v1` | P3 rwb-case | The move from `VALUATION_ACCEPTED` on `VALUE_ACCEPTED`, applied by the case of record; faked |
| The rule-in-force and decision-log read (operation name Not specified in the source documents (GAP-2604; ASM-4305)) | `/api/recovery/decision/v1` | P7 rwb-decision | The rule id and the version in force, the band policy element where it is carried there, and the record the ledger holds; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The band policy is administered under FEAT-ADM-04 and no source says which answer it travels on, so the baseline references it as an element of the rule-in-force answer and asserts no boundary (GAP-2605; ASM-4306). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it (ASM-4309). The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. The acceptance is started by the case owner's command on the route operation; FSD S1 A2.4.4.4 declares no background event for the feature and the ownership rows give S1 no event and no job, so the baseline declares no subscription and no consumer group (ASM-4309). The freshness of the ACE data product is read as an element of the rwb-source-data row and not as a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` | Input: the case, the asset key, the valuation key, the route set and the rule package in force; signals: the freshness answer and the case-move answer |
| `acceptAppraisalValue` | Activity | `rwb-valuation` | The valuation key, the asset key, the submitted value, the appraisal date and the band policy in force in; the band, the acceptance marker and the step outcome out |
| `recordAcceptance` | Activity | `rwb-valuation` | The decision record, the idempotency row and the case-move answer out, in one transaction |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. Its workflow ID form is Not specified in the source documents (CG-ALL-8020); the catalog starts it as a child of CaseWorkflow when the case reaches route decision D6 or is reopened (ROUTE_D6_REOPEN), and its duplicate-start policy is Not specified in the source documents (CG-ALL-8020). This baseline fixes its input, its two signals and the two activities the acceptance adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. The acceptance is command-driven and no source names a Schedule for it or for a re-review of an unaccepted value (GAP-2605; ASM-4306).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no table | The Ownership Map gives S1 no table, while TSD S1 T3.1 declares `valuation` as a NEW Workbench table and the FSD holds the acceptance in `recovery.valuation_ext` (GAP-2607; ASM-4308) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `recovery_case`, `assignment`, `task` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), every `v_ace_*` view (P1) and `valuation_ext` as an ACE-schema object are named by their owner and never declared here. If the S1 data owner confirms `valuation`, the DB story of this service creates it in its own Flyway sequence and this baseline declares its elements in a minor version.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | Appraisal `APR-2026-000404` of asset `AST-2026-000404` with its value and its type, the acceptance fields of `valuation_ext`, the outlier flag and a fresh stamp; the same asset with an open flag, with an existing acceptance and with a stale product; no answer beyond 2 s | C3, C4, C6 |
| rwb-case case-state fake | Case `RC-2026-000404` at `VALUATION_ACCEPTED`; a case in another state | C3, C6 |
| rwb-case move-answer fake | The move from `VALUATION_ACCEPTED` on `VALUE_ACCEPTED` accepted with its reference, and refused with its reason | C3, C6 |
| rwb-decision rule and log fake | The rule id and the band policy at their version in force for the business date; the record the ledger holds, once and twice | C3, C6 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000404`, with the appraisal, the band and the route elements read once | C2, C6 |
| Placeholder fake for an unpublished row | The documented use of the row and no field the source does not name, so the consumer can tell a published from an unpublished shape | C3 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2604; ASM-4305).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data data-product row, the rwb-case state and move rows, the rwb-decision row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `acceptAppraisalValue` and `recordAcceptance` on `rwb-valuation`; no Schedule |
| File | None declared | The appraisal arrives through ACE ingestion and the rwb-source-data data product, and this service writes no file (DP-05) |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4004 CON Accept the appraisal value - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4004.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operation with its acceptance elements, the five consumed rows, the publication, the workflow and its activities, the tables, the fakes, the call-type summary, the data elements and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3). The acceptance elements are declared optional, so the first tag does not break a consumer that does not carry them.

**Fakes.** One per consumed row plus the composite route and the placeholder, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The seven criteria pass, the five reviewer roles have closed their comments, the compatibility check passes on the tag, the eight fakes are published with their documented answers, and RWB-S1-E4004-APP and the wave 3 harness can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE data product behind the appraisal row is stale | {product} is from {date}. Today's load has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row or an element has no published shape | Not specified in the source documents (GAP-2604; ASM-4305). |

The four message IDs are those of the legacy message set of the key, of FSD S1 A2.4.3.1 and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the element list of the acceptance part of the route answer and the states the screen can show from this service's answer.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Empty: Not specified in the source documents (CG-ALL-8025); Loading; recommendation; overridden; submitted; Error: Not specified in the source documents (CG-ALL-8025); No access: Not specified in the source documents (CG-ALL-8025) | The value, its appraisal date, its outlier state, the band the acceptance fixes, the acceptance marker and the decision record with its rule version, and the override reason of the submission |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-004-01 | AC1, AC2: the schema, the acceptance elements and the closed lists of the route answer | Contract | The published schema and the recorded answers of case `RC-2026-000404` |
| TC-E4-004-02 | AC4, AC6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-004-03 | AC5: the rights and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-004-04 | AC3, AC7: the five consumed rows, the boundary and the empty publication | Contract | The five consumed rows with and without a published name; the base, the topic, the queue and the schema; an outbox declaration that must stay empty |
| TC-S1-E4004-CON-01 | AC3: the placeholder and the gap of an unpublished operation name | Contract | The five consumed rows, each with and without a published name |
| TC-S1-E4004-CON-02 | AC6: the fakes, the workflow elements and the decision-record element | Contract | The eight fakes and one fake that answers more than its document |
| TC-S1-E4004-CON-03 | AC7: the naming and boundary rule | Contract | A draft that names a foreign schema, a monolith base, a foreign topic or a Schedule |
| TC-S1-E4004-CON-04 | AC1, AC2: the compatibility check and the optional acceptance elements | Contract | The previous tag, an additive draft and a breaking draft |
| TC-S1-E4004-CON-05 | AC4: the boundary of the tables of section 12.7, no table of another owner declared | Contract | The tables of section 12.7 with the foreign tables of P3, P7 and P1 and the valuation_ext object |
| TC-S1-E4004-CON-06 | AC8, BR1 to BR10: each business rule of section 8 | Contract | One check per rule, each against the draft that the rule governs |
| TC-S1-E4004-CON-07 | AC9: the retry and the timeout of each activity of RouteDecisionWorkflow | Contract | Each activity run once, retried and timed out |
| TC-S1-E4004-CON-08 | AC10: the refused status change | Contract | A status change the model allows and a status change it does not allow |

The four legacy case IDs are the legacy test cases of RWB-E4-004 in their legacy order, mapped onto this contract deliverable: the acceptance and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The four `TC-S1-E4004-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the appraisal types of `LOV-APPRAISAL`, the route codes of `LOV-ROUTE` and the band policy are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic; the accepting user is an identifier.
- ACE data only through the owner's contract: the baseline declares no `v_ace_*` element and no ACE table, and the appraisal and the acceptance appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case and the rules with rwb-decision: no `recovery_case` element and no `rule_row` element is declared as this service's own.
- The band policy is referenced and not declared: a baseline that fixes a band, a boundary or a floor fails the review (BR7).
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-004, disposition Split (rework); AC1 and AC2 are owned by RWB-S1-E4004-APP; this story carries no legacy criterion and fixes the surface that story and the harness touch | 1, 11, 12, 16 |
| Feature | FEAT-VAL-04 Accept the appraisal value, module S1, epic E4, depends on FEAT-VAL-03; the band policy is FEAT-ADM-04 | 1, 2, 3 |
| FSD S1 v3 | A1.4 preconditions; A2.4.2 steps and integration points; A2.4.3.1 VR-S1-004-1 and BR-S1-004; A2.4.3.2 field catalog; A2.4.3.3 roles; A2.4.4.4 no background event; REQ-S1-002, REQ-S1-003 and REQ-S1-008; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T3.2 `LOV-APPRAISAL` and `LOV-ROUTE`; T3.3 relationships; T5.1 to T5.3; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| Logical data model | DF-ACE-187 to DF-ACE-195, DF-EXT-036 to DF-EXT-049, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-COL-018 to DF-COL-027 and DF-COL-043 to DF-COL-044 | 11 |
| Routing logic | R-UNI-38, R-UNI-39 and R-UNI-40; R-DIL-09 and R-DIL-12 and the valuation states of the D6.4 route set; no S1 route rule is in force, because the S1 package is Phase 2 | 8, 14 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2604, -3, -4 and -5; ASM-4305 to -6; the application gap GAP-2603 is cited where the acceptance store is read | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-013, ADR-014, ADR-015, ADR-020, ADR-022; D-RCV-60 | all |

### 19. Out of scope

- The acceptance behaviour, the band fixing, the decision records, the case-move answer and the screen behaviour: RWB-S1-E4004-APP.
- The two valuation operations and the appraisal intake: RWB-S1-E4002-CON and the appraisal stories of this service.
- The outlier flag of FEAT-VAL-03 and its clearance: the sibling appraisal stories of this service.
- The ACE appraisal, collateral and acceptance facts and the freshness of the data product: rwb-source-data (P1); the store of `valuation_ext` and of any `valuation` table: the data owner of this service (GAP-2607).
- The band policy, its identifiers and its boundaries, and the administration of bands, floors and ranges per product: rwb-access and the product head under FEAT-ADM-04 (GAP-2605).
- The case of record, its valuation states and the parent `CaseWorkflow`: rwb-case (P3).
- The rule rows, the package version, its approval and the central ledger: rwb-decision (P7).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
