# RWB-S5-E3026-CON Re-appraise a held asset on cycle - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3026-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-026 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the re-appraisal cycle step of rwb-asset, split from RWB-E3-026. It fixes the two asset reads on `/api/recovery/asset/v1` with their appraisal and re-appraisal properties (DP-13), the consumed rwb-source-data appraisal row, the rwb-valuation order row of API-S5-003, the rwb-case state read and move answer, the decision-record element of DP-03, the JOB-19 Schedule parameters, the fakes and the absence tests. The plan carries no DP-09, DP-10 or C row for this key although the step is driven by a Schedule, places an order and consumes three owners' contracts, and the target path of the valuation order is not published (GAP-2869, GAP-2870; ASM-4757 to ASM-4761, ASM-4764, ASM-4765). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the re-appraisal cycle of rwb-asset — the two asset reads with their appraisal properties, the consumed rwb-source-data appraisal row, the rwb-valuation order row, the rwb-case state and move rows, the decision-record element, the JOB-19 Schedule parameters and the fakes**, so that **the app story, the two screens and the wave 2 harness build against one fixed, testable contract on Day 1 and an appraisal field, a route value, an order property or a move shape can never drift between rwb-asset, rwb-source-data, rwb-case and rwb-valuation without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy re-appraisal of RWB-E3-026 crossed three boundaries at once: an officer screen, the ACE appraisal fact and the case state. The target splits them: rwb-source-data owns the ACE valuation fact, rwb-valuation owns the appraisal and the SVAF exchange, rwb-case owns the case and its route states, and rwb-asset owns the cycle, the decision and the two reads. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the appraisal properties of the reads, the route values `ASSET_HELD`, `NO_BID_AT_FLOOR`, `REAPPRAISAL_ORDERED` and `RELISTED`, the order element, the fact the rwb-source-data contract answers, the case state and move, and the record of the decision.

The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset`. It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case`, `rwb_valuation` or `rwb_decision`, so DP-05 is declared as a prohibition and the appraisal fact is consumed on the owner's contract only.

Four points are carried as gaps and assumptions rather than decided quietly: the four consumed rows have no C row in the plan (GAP-2869), the target path of the valuation order and the operation names of the rwb-source-data read and of the move answer are unpublished (GAP-2870), DP-10 is absent although JOB-19 is the service's single job (ASM-4759), and the module model holds no re-appraisal record, so the cycle is the Schedule and the workflow's state (ASM-4761).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case` is P3's, `valuation` is S1's, `decision_log_entry` and `rule_row` are P7's, and every `v_ace_*` view is P1's. This document never declares another service's table or operation as its own.
- The rwb-source-data appraisal contract, the rwb-valuation operation API-S5-003 and the rwb-case state and move rows are published with their fakes, so each consumed row names a real owner document; none is in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2869; ASM-4757, ASM-4758, ASM-4760).
- The Temporal workflow kit and its Schedule capability (`RWB-PLT-E1071-CON`) are available, because JOB-19 is declared as a Schedule and not as a Quartz row; the plan's pattern set does not carry DP-10 (ASM-4759).
- The DISPOSAL rule package and its rule rows for R-DIS-15, R-DIS-44 and R-DIS-06 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `asset` and `listing` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration (ASM-4761).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). It stays in Draft until the verification loop collects its sign-offs (ASM-4764).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads with their request and answer elements, the filters, the rights and the error responses.
2. Fix the appraisal and re-appraisal properties of the `Asset` element: the appraisal reference, its type, its value and its date, the one-year flag, the holding status and the re-appraisal state, with the placeholder where the model gives no column.
3. Fix the consumed rows: the rwb-source-data appraisal read with its freshness stamp, the rwb-valuation order of API-S5-003 with its `Idempotency-Key`, and the rwb-case state read and move answer, marking the fields the sources do not give with the placeholder.
4. Record the decision-record element of DP-03, written before the order is placed.
5. Fix the closed vocabulary of the lists and of the route values, the naming baseline and the rule that no value is a constant of the code.
6. Fix the JOB-19 Schedule parameters: the cadence, the reference time with its placeholder, the due-asset selection and the pause rule.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case`, `rwb_valuation` or `rwb_decision` write, the drift between a fake and the document, and the absence of a published event.
9. Tag the baseline and hand it to RWB-S5-E3026-APP, the two screens and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC4 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC2, AC3, AC4 |
| X5 | A value outside `LOV-HOLDING`, the DISPOSAL route states or the order reason codes appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a `valuation` row or a `rule_row` | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | The document declares a published or consumed event, a second topic or a second Schedule | The absence test fails the build | None | AC6 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-source-data, rwb-valuation and rwb-case only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3026-APP, the two screens and the wave 2 harness on Day 1, and the rwb-source-data, rwb-valuation and rwb-case teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, nine contract tables, seven fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the re-appraisal cycle of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case is P3, of valuation is S1, of decision_log_entry and rule_row is P7 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The two asset reads are declared with the appraisal and re-appraisal properties (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the Asset element declares the appraisal reference, the appraisal type, the appraised value, the appraisal date, the one-year flag, the holding status and the re-appraisal state, and each is marked required or optional
    Then the list declares the filters type, status and region with page and size, and the single read declares the path parameter assetId
    Then the answers 400, 401, 403, 404, 422 and 503 are declared with one envelope and one message ID per condition, and neither read declares an Idempotency-Key
    Then every other property of the two operations is copied from the asset baseline and is not redefined here

  Scenario: AC2 The re-appraisal vocabulary and the route values are fixed (new, D-RCV-60)
    Given the schema section of the baseline
    When it is compared with TSD S5 T3.2 and T4
    Then holding_status is declared against LOV-HOLDING with the values HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED
    Then the route values ASSET_HELD, NO_BID_AT_FLOOR, REAPPRAISAL_ORDERED and RELISTED are declared as the case route states this step reads and answers, and as values of the case owner and not of this service
    Then the re-appraisal reason codes are declared as an enumeration read from reference data, with the values the package in force gives and no value written in the document
    Then the 12-month interval, the one-year flag, the re-list limit and the 10-working-day target are declared as inputs read with their version and never as schema defaults
    Then no property is added for an appraisal value, an order reference or a cycle date, because those are rwb-valuation's and the workflow's

  Scenario: AC3 The consumed rwb-source-data row and the rwb-valuation order row are declared (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-source-data data-product contract, TSD S5 T-A.1 and the ruling ASM-0043
    Then the appraisal and NPA asset read is declared as consumed from P1 rwb-source-data, with the appraisal reference, type, value and date, the one-year flag, the asset reference, asset key and book value, and the freshness stamp
    Then its operation and data-product names are Not specified in the source documents (GAP-2869; ASM-4757) and the row carries the placeholder
    Then the valuation order of API-S5-003 is declared as consumed from S1 rwb-valuation with the asset reference, the appraisal reference, the reason code, the rule version and an Idempotency-Key, and its target path is Not specified in the source documents (GAP-2870; ASM-4758)
    Then the document declares no valuation value, no appraised price, no SVAF path and no property of the valuation table, and the boundary test fails a build that adds one
    Then both calls are one hop with a 2 s budget and a breaker (DP-11, ADR-020)

  Scenario: AC4 The rwb-case rows, the rights, the error envelope and the repeat rule are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with TSD S5 T-A.1 and T6.1
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the moves REAPPRAISAL_ORDERED and RELISTED carrying the rule ID and its version
    Then the operation name of the case-move answer is Not specified in the source documents (GAP-2869; ASM-4760) and the row carries the placeholder
    Then the document declares no recovery_case property, no case route-state column and no write of a case row from rwb-asset
    Then both reads declare Asset and disposal right R with the scope applied, and a role without it is answered 403 with MSG-P4-002
    Then a repeated order with the same Idempotency-Key describes no second effect, and no read declares the header

  Scenario: AC5 The decision-record element and the seven fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the appraisal reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the order is placed, and a failed write leaves everything unchanged with MSG-P7-003
    Then the rwb-source-data fake answers the appraisal older than 12 months with the flag not applied, the fact inside 12 months, the flag applied, a stale product and no answer beyond 2 s
    Then the rwb-valuation fake answers an accepted order with its reference, a refused order and no answer beyond 2 s
    Then the rwb-case fake answers the states ASSET_HELD and NO_BID_AT_FLOOR, the accepted moves REAPPRAISAL_ORDERED and RELISTED and a refused move, and the rwb-decision fake answers the DISPOSAL package at its version
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The JOB-19 Schedule parameters are fixed and no event is declared (new, D-RCV-60)
    Given the scheduling and event sections of the baseline
    When they are compared with the S5 ownership rows and Architecture v5 slide 19
    Then JOB-19 Re-appraisal monthly is declared as the one Schedule of rwb-asset on queue rwb-asset, monthly, with its reference time and day marked Not specified in the source documents (GAP-2869; ASM-4759)
    Then the due-asset selection and the pause rule are declared as parameters of the Schedule and not as code
    Then no Quartz row, no shared job table, no batch table and no second Schedule is declared
    Then the document declares no published event and no consumed event, and names AssetTakenOn as the service's own event of the take-on story and not as an element of this step
    Then the absence test fails a build that adds a producer, a consumer group, a second topic or a Schedule

  Scenario: AC7 The naming baseline and the boundary are fixed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are asset, listing, decision_record and idempotency_key, and recovery_case, valuation, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no consumed or published event and no second topic, and the absence test fails a build that adds one
    Then the document records that the module model holds no re-appraisal table and no appraisal-date, one-year-flag or re-list-count column, so the cycle is the Schedule and the workflow's state (GAP-2870; ASM-4761)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3026-APP and they copy no criterion of the legacy story, whose criteria AC1, AC2 and AC4 stay with the app story word for word and whose AC3 stays with the wave 2 harness.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The two reads, the appraisal properties and the re-appraisal state are declared on this service's own base and element only | Architecture v5 slide 41; TSD S5 T3.1 and T3.2; DP-13 |
| BR2 | The decision record is declared as an element written before the order is placed, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E3-026 AC1 and AC4 |
| BR3 | The appraisal fact stays with rwb-source-data: the contract declares the read as consumed, declares no `v_ace_*` property and describes no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; ASM-4757 |
| BR4 | The valuation and the order stay with rwb-valuation: API-S5-003 is consumed, never provided, and no valuation value, price or SVAF element is declared here | TSD S5 T-A.1 and T-A.2; Ownership Map ruling ASM-0043; ASM-4758 |
| BR5 | The case move is answered and not written: the contract declares the state read and the answer, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); ASM-4760 |
| BR6 | The vocabulary is closed: `LOV-HOLDING`, the four route states and the reason codes are published as enumerated values and no value is a constant of the code | TSD S5 T3.2 and T4; FSD S5 BR-S5-009 |
| BR7 | JOB-19 is declared as one Temporal Schedule with named parameters, and no Quartz row, shared job table or batch table is declared | DP-10; S5 ownership rows (JOB-19); Architecture v5 slide 44; ASM-4759 |
| BR8 | No event is published or consumed by this step: the topic of the service carries `AssetTakenOn` and `AssetSold`, which belong to other stories | Architecture v5 slide 19 OUT and slide 43; GAP-2869 |
| BR9 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR12 | The rule rows of R-DIS-15, R-DIS-44 and R-DIS-06 and the values of the interval, the flag and the limit are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4; ASM-4763 |

### 9. State transitions

The lifecycle of this document, not of an asset:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two reads, the appraisal properties, the consumed rows, the Schedule parameters and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 2 harness and the rwb-source-data, rwb-valuation and rwb-case owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional appraisal property or a filter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a route or reason value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3, AC6 and AC7 fail: a `v_ace_*` view, a `recovery_case` property, a valuation property, an event or a second Schedule | In review |

The route machine the document describes is the DISPOSAL machine of TSD S5 T4 and belongs to rwb-case: this baseline fixes the vocabulary it reads and answers — `ASSET_HELD`, `NO_BID_AT_FLOOR`, `REAPPRAISAL_ORDERED` and `RELISTED` — and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document, the AsyncAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the corrections of the Ownership Map rows the baseline consumes, and the ruling ASM-0043 on the valuation order |
| Consuming teams (the app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-valuation, rwb-case, rwb-decision, rwb-access and rwb-payment) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the workflow kit with its Schedule capability this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element additions | The appraisal reference, the appraisal type, the appraised value, the appraisal date, the one-year flag, the holding status and the re-appraisal state, on the element of DF-COL-028 to DF-COL-042 |
| Route vocabulary | `ASSET_HELD`, `NO_BID_AT_FLOOR`, `REAPPRAISAL_ORDERED` and `RELISTED`, declared as the case owner's values (TSD S5 T4) |
| Lists | `LOV-HOLDING`, the route values and the re-appraisal reason codes, published as enumerations and read as reference data at their version |
| Rule inputs | The 12-month interval, the one-year flag, the re-list limit and the 10-working-day target, declared as versioned inputs and never as defaults |
| Order element | The asset reference, the appraisal reference, the reason code, the rule version and the `Idempotency-Key`; no valuation value, no price and no SVAF element |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the order is placed (DP-03) |
| ACE appraisal fact | DF-ACE-187 to DF-ACE-195 of `v_ace_valuation` and DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` in P1, read only through the owner's contract and never written, copied or joined here |
| Not declared here | `recovery_case` (P3), `valuation` (S1), `decision_log_entry` and `rule_row` (P7), `asset_sale` (S5, the sale stories'), `document` (P5), `proceeds` (P8) |
| Consumed fields with no source | The operation and data-product names of the rwb-source-data read, the target path of the valuation order and the operation name of the case-move answer: Not specified in the source documents (GAP-2869, GAP-2870; ASM-4757, ASM-4758, ASM-4760) |

The field-level types, lengths and required flags of the added properties are settled in the baseline review; this story fixes the property names, the vocabulary of AC2 and the optionality rule of BR11. **No new table, no new column and no migration** is declared by this story (ASM-4761).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its appraisal references, its appraisal age and its re-appraisal state (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S5 T-A.1 and the paths are those of the target base, not the monolith form. API-S5-003 is consumed from rwb-valuation under ASM-0043, and API-S5-004 and API-S5-005 belong to the pricing and auction stories of this service; none of the three is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The appraisal and NPA asset read (operation and data-product names Not specified in the source documents (GAP-2869; ASM-4757)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The appraisal reference, type, value and date, the one-year flag, the asset reference, asset key and book value, and the freshness stamp; faked |
| `POST` of the valuation order (API-S5-003; target path Not specified in the source documents (GAP-2870; ASM-4758)) | rwb-valuation (S1) | S1 rwb-valuation | The re-appraisal order: asset reference, appraisal reference, reason code, rule version, `Idempotency-Key`; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2869; ASM-4760)) | rwb-case (P3) | P3 rwb-case | `REAPPRAISAL_ORDERED` or `RELISTED` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent applies; faked |

Every row is one hop with a 2 s timeout, a breaker per downstream, and a GET retried once with jitter (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2869 with ASM-4757, ASM-4758 and ASM-4760.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset the topic `rwb.asset.events.v1` with `AssetTakenOn` and `AssetSold`, and both belong to the take-on and the sale stories; the S5 ownership row lists the single event EV-22, which is `AssetTakenOn`. This baseline therefore declares no producer, no outbox row and no event element for this step, and the absence test of AC6 fails a build that adds one.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is the re-appraisal cycle or the case state: the trigger is the JOB-19 Schedule and the workflow's own round result. This baseline declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | The stage that hosts the cycle step; its input, its signals and its outcome for the parent are declared, not built |
| `orderReappraisal` | Activity, the one cycle step | `rwb-asset` | The case, the asset and the appraisal fact in; the rule ID with its package version, the order reference and the case move out |

No child workflow for the case and none for the valuation exists in this service. The activity name is a target design choice and is fixed by no source document; the trigger is read as the Schedule fire and the round result, because the FSD declares no background event for the feature (FSD S5 A2.9.4.4). No activity is registered by this story.

#### 12.6 Schedules

| Schedule | Declared parameters | Owner |
|---|---|---|
| JOB-19 Re-appraisal monthly | Cadence monthly; the reference time and day are Not specified in the source documents (GAP-2869; ASM-4759); the due-asset selection by appraisal age and holding status; the pause rule of the feature flag; the start of `orderReappraisal` on queue `rwb-asset` | rwb-asset (S5) through the workflow kit of DP-10 |

JOB-19 is the single job of the S5 ownership rows and replaces its legacy Quartz row. `RWB-PLT-E1071-CON` is named here and is not in this story's build row, because the plan carries no DP-10 row for this key. No other Schedule, no Quartz row, no shared job table and no batch table is declared by this baseline.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset | S5 (`rwb_asset`) | The asset, its case, its holding status and the appraisal references the reads answer |
| listing | S5 (`rwb_asset`) | The round and its result, the fact of the no-bid path |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated order and the answer it holds |

`recovery_case` (P3), `valuation` (S1), `decision_log_entry` and `rule_row` (P7), `asset_sale` (S5, later stories'), `document` (P5), `proceeds` (P8) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data appraisal fake | The appraisal of asset `AST-2026-000511` older than 12 months with the one-year flag not applied; the same fact inside 12 months; the flag applied; a stale product with its date; no answer beyond 2 s; an unreadable answer | AC1, AC3, AC5 |
| rwb-valuation order fake | An accepted order with its order reference; a refused order; no answer beyond 2 s | AC3, AC5 |
| rwb-case state and move fake | The states `ASSET_HELD` and `NO_BID_AT_FLOOR` of case `RC-2026-000511`; the accepted moves `REAPPRAISAL_ORDERED` and `RELISTED`; a refused move | AC4, AC5 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-15, R-DIS-44 and R-DIS-06 | AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| Temporal Schedule stub (`RWB-PLT-E1071-CON`) | A Schedule that fires the step for the due assets, a paused Schedule and a Schedule whose run fails | AC6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for asset `AST-2026-000511` | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The names of the rwb-source-data read, of the valuation order and of the case-move answer are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2869, GAP-2870).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 4 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-source-data fact read, the rwb-valuation order, the rwb-case state read and the case-move answer; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event element; `AssetTakenOn` and `AssetSold` are other stories' and the decision record is the library's on `rwb.decision-record.v1` |
| Temporal | 1 workflow and 1 activity declared, 0 registered, 1 Schedule | `AssetDisposalWorkflow`, `orderReappraisal` and JOB-19 on `rwb-asset` |
| File | None | No file is read, built or delivered here; the SVAF exchange is rwb-valuation's |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no case, no valuation and no rule package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment, nine contract tables, seven fakes and five new contract tests.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml` with the appraisal properties of the `Asset` element, the `ReappraisalOrderRequest` element of the consumed row, the route and reason vocabularies as published enumerations, the AsyncAPI fragment with the absence of an event of this step, the JOB-19 parameter block, the contract README rows for the consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on another owner's schema (ASM-4757). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-23, whose screen model is the edge contract's. DP-10 is not in the pattern set of this key, which is why the Schedule and its library are declared as an absent row rather than added to the H list (ASM-4759).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries, and it leaves out the four consumed rows and the Schedule library. The four consumed rows are C dependencies in fact and not in the metadata row (GAP-2869, GAP-2870).

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Declare the appraisal and re-appraisal properties of AC1 and the vocabulary of AC2 with the placeholder where a type or a value is unstated.
3. Record the consumed rwb-source-data row of AC3 with its owner, its budget, its freshness stamp and its placeholder.
4. Record the rwb-valuation order row of AC3 with its `Idempotency-Key`, its reason vocabulary and its path placeholder.
5. Record the rwb-case rows, the rights, the error envelope and the repeat rule of AC4.
6. Record the decision-record element of AC5 and validate it against the library schema, then publish the seven fakes and the drift test.
7. Record the JOB-19 parameters and the absence of an event of AC6.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-002 | The appraisal of the asset is older than a year; the document declares it as the warning the reads can carry (VR-S5-009-1) | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the order is placed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states and SCR-23 Listing and price in its draft, below-limit, approved and published states, all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status, its appraisal age and its re-appraisal state, rwb-case for the case and its route state, rwb-source-data for the appraisal fact and rwb-valuation for the valuation references; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The warning, refusal and not-recorded states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-026-01 | AC1, AC2 | Contract | The appraisal of asset `AST-2026-000511` older than 12 months; the contract half answers the two reads, the appraisal properties and the vocabulary |
| TC-E3-026-02 | AC2, AC4 | Contract | Case `RC-2026-000511` at `NO_BID_AT_FLOOR`; the contract half answers the route values and the `RELISTED` move shape |
| TC-E3-026-03 | AC3, AC5 | Contract | The `ASSET_HELD` case with the cycle due; the contract half answers the rwb-source-data row, the rwb-valuation order, their placeholders and the decision record |
| TC-E3-026-04 | AC1, AC4 | Contract | A malformed request and a role without the Asset and disposal right; the contract half answers the 400 of the envelope and the 403 with MSG-P4-002 |
| TC-E3-026-05 | AC4 | Contract | RW-SALEOFF holds CRUA and RW-NPAMGR holds CRU; the contract half answers the rights of the two reads |
| TC-E3-026-06 | AC5, AC6, AC7 | Contract | The decision-record stub stopped, a paused Schedule and a stale appraisal; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S5-E3026-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the filters and the six error answers are present |
| TC-S5-E3026-CON-02 | AC2 | Contract | The appraisal properties and the four route values validate, and the reason enum carries no value of the document |
| TC-S5-E3026-CON-03 | AC3, AC6 | Contract | The four consumed rows and their placeholders; the JOB-19 parameters; the absence test for a published event, a consumed event, a second topic and a second Schedule |
| TC-S5-E3026-CON-04 | AC5, AC7 | Contract | The seven fakes match the document and a drifted fake fails the build; the no-`v_ace_*`, no-`recovery_case` and no-`valuation` boundary |

The six legacy cases are the legacy cases of RWB-E3-026 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3026-APP or, for AC3, by the wave 2 harness. Legacy level `System` maps to `Contract` here because the artefact under test is the contract. The four cases `TC-S5-E3026-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the 12-month interval, the one-year flag, the re-list limit, the 10-working-day target, the lists, the route values and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- The appraisal fact stays with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` path, no `recovery_case` property, no case row write and no ACE table read (BR3, BR5).
- The valuation stays with rwb-valuation: no valuation value, no appraised price, no SVAF element and no valuation row is declared here, and API-S5-003 is consumed only (BR4).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares an event of this step, a second topic, a second Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the workflow kit come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-003 | Holding age drives re-appraisal and the provision step by rule (FSD S5 requirements served, Must, E3); the contract fixes the properties, the vocabularies and the consumed rows on which the cycle is built; the split plan carries no requirement id for this slice (GAP-2869; ASM-4763) | The appraisal properties, the route vocabulary, the order row and the Schedule parameters | TC-E3-026-01, TC-E3-026-03, TC-S5-E3026-CON-01, TC-S5-E3026-CON-02 |
| ADR-016 | Reusable Temporal layer; Schedules replace Quartz | The JOB-19 Schedule parameters | TC-S5-E3026-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S5-E3026-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element | TC-S5-E3026-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-026, disposition Split (rework) |
| Legacy criteria | AC1, AC2 and AC4 of the legacy story, owned word for word by RWB-S5-E3026-APP; AC3 by RWB-ITG-E3026-ITG; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S5-E3026-CON-01 to -04 |
| Feature and screens | FEAT-AST-09, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-44, R-DIS-15 and R-DIS-06, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Job | JOB-19 Re-appraisal monthly |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-016 (Schedules replace Quartz), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two reads, the evaluation of R-DIS-15 and R-DIS-44, the decision record, the order and the case-move answer: RWB-S5-E3026-APP.
- AC3 and its end-to-end evidence across rwb-source-data, rwb-valuation and rwb-case: RWB-ITG-E3026-ITG.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The valuation itself: the valuer, the SVAF exchange, the appraisal value, R-DIS-16 to R-DIS-18 and API-S5-003 as a provided operation belong to rwb-valuation (S1) (ASM-4758).
- The ACE valuation and NPA asset facts and the freshness of the data product: rwb-source-data (P1) (ASM-4757).
- The authoring, testing, approval and versioning of the DISPOSAL package and of R-DIS-15, R-DIS-44 and R-DIS-06: rwb-decision (P7).
- The listing, the price ladder, the auction rounds and the sale: the pricing and auction stories of this service, API-S5-004 and API-S5-005.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its Schedule pause, its dashboards, its alerts and its runbook: the operations story of this legacy key.
