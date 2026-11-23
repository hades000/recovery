# RWB-S5-E3027-CON Recommend the disposal route - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3027-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-027 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the disposal-route recommendation of rwb-asset, split from RWB-E3-027. It fixes the `RouteRecommendation` element and its route vocabulary, the expected return per route and its unit, the additive `route_recommendation` property of the two asset reads on `/api/recovery/asset/v1` (DP-13), the consumed rwb-source-data asset and score rows, the rwb-case state and move rows, the rwb-decision package read, the decision-record element of DP-03, the fakes and the absence tests. No source gives an operation, an event or a representation for a recommendation, so the element names and the return unit are design choices of this baseline and are carried as a gap and an assumption (GAP-2874, GAP-2875; ASM-4770, ASM-4771). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the disposal-route recommendation of rwb-asset — the `RouteRecommendation` element with its five route words, its expected return per route and its reasons, the additive property on the two asset reads, the consumed rwb-source-data, rwb-case and rwb-decision rows, the decision-record element, the tables and the fakes**, so that **the app story, the pricing story and the wave 2 harness build against one fixed, testable contract on Day 1 and a route word, a return unit, a consumed field or an answer shape can never drift between rwb-asset, rwb-source-data and rwb-case without a failing build**.

This is the contract slice of legacy RWB-E3-027. It owns:

- the `RouteRecommendation` element: the recommended route, the ranked routes, the expected return on each with its unit, the reasons and the rule ID with its version;
- the five route words of the legacy criterion — auction, broker, RAMC, buy-back and rental — and their mapping to the closed lists of the service;
- the additive `route_recommendation` property of the two reads that RWB-S5-E3019-CON baselined, so no operation is added and no consumer breaks;
- the consumed rows of rwb-source-data (the asset fact and the COLLINS economics), rwb-case (the case state and the case-move answer) and rwb-decision (the DISPOSAL package);
- the decision-record element of DP-03 that the recommendation is written into, and the rule for a failed write;
- the fakes, the drift test, the naming baseline and the absence tests.

It does not own: the behaviour of the step, which is RWB-S5-E3027-APP; the approval of the route, which is the next story of this service; the pricing, listing and auction shapes, which are RWB-S5-E3028-APP and the auction stories; the case of record and its route states, which are rwb-case's (P3); the ACE asset and COLLINS score facts, which are rwb-source-data's (P1); and the rule rows, which are rwb-decision's (P7).

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and every cross-service fact the recommendation needs has to be a published shape before the app story starts: the ACE asset fact, the COLLINS economics, the case state and the case move. The legacy recommendation read the ACE views (`v_ace_npa_asset` in its data table, `v_ace_score` in the FSD) and wrote the case stage and the decision log in one schema; the target has three owners for those four facts, so each becomes a contract.

The baseline also fixes the naming that the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset`. It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_decision` (Architecture v5 slides 29, 37 and 45), so DP-05 is declared as a prohibition and both ACE facts are consumed on the owner's contracts only.

Two points are carried as gaps and assumptions rather than decided quietly: no source names an operation, an event or a representation for a recommendation, so the element and its property are additive design names (GAP-2874; ASM-4770), and no source fixes the unit of the expected return or the mapping of the five route words to a closed list, because `LOV-SALE-CHANNEL` carries `DUTCH_AUCTION`, `BROKER`, `DIRECT`, `LED_AUCTION` and `RAMC` and no buy-back or rental value while the machine carries `ROUTE_APPROVED_BUYBACK` and `RENTAL_ACTIVE` states (GAP-2875; ASM-4771).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- RWB-S5-E3019-CON is published and tagged: the two asset reads, the `Asset` element and its four closed lists are the parent surface of this baseline, and this document extends them additively without redefining them.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case` is P3's, `decision_log_entry` and `rule_row` are P7's, the ACE facts and the 30 `recovery.v_ace_*` views are P1's. This document never declares another service's table or operation as its own, and it records that `asset` has no Ownership Map row while Architecture v5 slides 19 and 41 and TSD S5 T3.1 give it to S5 (GAP-2872; ASM-4768).
- The rwb-source-data data-product contracts of DP06 Collateral and assets and of the COLLINS score fact, the rwb-case state and move rows and the rwb-decision package read are published with their fakes, so the consumed rows name a real owner document; none of them is in this story's contract-dependency row, which is None (GAP-2872; ASM-4768).
- The DISPOSAL rule package and the rule rows for R-DIS-08, R-DIS-14 and R-DIS-19 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `asset`, `listing` and `asset_sale` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 change of rwb-asset: the additive `route_recommendation` property on the `Asset` answer of `GET /assets/{assetId}` and on each entry of the `AssetPage` answer of `GET /assets`, with no new operation and no new base.
2. Fix the `RouteRecommendation` element: the recommended route, the ranked list of routes with the expected return and the reasons on each, the rule ID, the package version and the decided-at time.
3. Fix the route vocabulary: the five words of the legacy criterion against `LOV-SALE-CHANNEL` and the DISPOSAL route states, with the placeholder where a word has no list value.
4. Fix the return unit: an amount with its currency, its currency code and the model version of the economics it came from, and the prohibition on a percentage, a threshold or a target written as a schema default.
5. Fix the consumed rows: the rwb-source-data asset and score products with their freshness stamps, the rwb-case state read and move answer, and the rwb-decision package read, marking the fields the sources do not give with the placeholder.
6. Record the decision-record element of DP-03: one record per rule outcome, written before anything changes, and the failed-write answer with MSG-P7-003.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the return unit, the placeholder discipline, the error envelope, the absence of a `v_ace_*` read and of a `recovery_case` write, the absence of a new operation, an event and a Schedule, and the drift between a fake and the document.
9. Tag the baseline and hand it to RWB-S5-E3027-APP, the pricing story and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2 |
| X2 | A property is renamed or removed within major version 1 | The additive test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-SALE-CHANNEL`, `LOV-HOLDING` or `LOV-ASSET-TYPE` appears in the document or in an example | The vocabulary test fails the build | None | AC1 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view or a `recovery_case` row | The review fails the baseline; the boundary test fails the build | None | AC3, AC4 |
| X7 | The document declares a new operation, a consumed event, a second topic or a Schedule for the recommendation | The absence test fails the build | None | AC6 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the E3019 contract baseline, the Ownership Map and the published owner contracts of rwb-source-data, rwb-case and rwb-decision only |
| Negotiable | The element names, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the target architecture and the parent baseline |
| Valuable | Unblocks RWB-S5-E3027-APP, the pricing story and the wave 2 harness on Day 1 |
| Estimable | One OpenAPI change, one element with three sub-shapes, nine contract tables, five fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the disposal-route recommendation of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case is P3, of decision_log_entry and rule_row is P7 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The recommendation element and its route vocabulary are fixed on the two reads (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then RouteRecommendation is declared as an additive property route_recommendation of the Asset answer and of each AssetPage entry, and no operation, path, base or status code is added
    Then the element declares recommended_route, ranked_routes, reasons, rule_id, rule_version and decided_at, and only recommended_route, ranked_routes, rule_id and rule_version are required
    Then each ranked route declares the route word, the expected return, its currency and the reasons of that route
    Then the route word is declared against the five words of the legacy criterion and their list mapping: auction, broker, RAMC, buy-back and rental, with the placeholder where a word has no value of LOV-SALE-CHANNEL
    Then an example carrying a word outside the five fails the vocabulary test, and the absence test fails a build that adds an operation for the recommendation

  Scenario: AC2 The expected return and the reasons are fixed with their unit and their version (new, D-RCV-60)
    Given the return section of the element
    When it is compared with the data model and the rule action of R-DIS-19
    Then the expected return is declared as an amount with its currency code, and no percentage, threshold, target or price is a default of the schema
    Then each return carries the model version of the economics it came from, and the element carries the package version in force
    Then the reasons are declared as an ordered list of coded reasons with no personal data and no free text that names a person
    Then the unit and the list of codes are Not specified in the source documents (GAP-2875; ASM-4771) and carry the placeholder

  Scenario: AC3 The consumed rwb-source-data rows are declared and the ACE facts stay there (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the rwb-source-data data-product contracts and Architecture v5 slides 29, 37 and 45
    Then the read of DP06 Collateral and assets is declared as consumed from P1, with the asset reference, asset type, book value, holding status, transfer-in type and the freshness stamp
    Then the read of the COLLINS score product that the legacy v_ace_score row gives is declared as consumed from P1, with the score key, model code, model version, score value and estimate value, and its operation name is Not specified in the source documents (GAP-2872; ASM-4768)
    Then the document declares no v_ace_* path, no v_ace_* property and no grant on any rwb_* schema of another owner, and the boundary test fails a build that adds one
    Then each call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-case rows and the rights are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with TSD S5 T-A.1 and T6.1
    Then the case state read is declared as consumed from P3 with the case reference, the route state, the appraisal currency and the title status, and its operation name is Not specified in the source documents (GAP-2872; ASM-4768)
    Then the case-move answer is declared as consumed from P3 with the move ROUTE_RECOMMENDED or ASSET_HELD, the rule ID and the version, and the document declares no recovery_case property and no write of a case row from rwb-asset
    Then both reads declare Asset and disposal right R with the scope applied, RW-SALEOFF holds CRUA, RW-NPAMGR and RW-ENFORCE hold CRU and every other role of TSD S5 T6.1 holds R
    Then a role without the right is answered 403 with MSG-P4-002, and no read declares an Idempotency-Key

  Scenario: AC5 The decision-record element and the rule-package read are fixed (new, D-RCV-60)
    Given the decision section of the baseline
    When it is compared with the library schema of RWB-PLT-E1027-CON and with the rule package of rwb-decision
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version in force, the inputs reference, the outcome, the recommended route with its returns, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything changes, and a failed write leaves the service unchanged with MSG-P7-003
    Then the package read that returns the DISPOSAL version in force is declared as consumed from P7 with its operation name Not specified in the source documents (GAP-2872; ASM-4768)
    Then neither the record nor the package read carries a personal data property, and a schema test fails any that is added

  Scenario: AC6 The fakes, the naming baseline and the absence tests are fixed (new, D-RCV-60)
    Given the fakes of the baseline and the naming baseline
    When each fake is compared with the element it serves
    Then the rwb-source-data asset fake, the rwb-source-data score fake, the rwb-case state fake, the rwb-case move fake, the rwb-decision package fake, the decision-record stub and the gateway-bff composite route fake each answer the document, and a drifted fake fails the build
    Then the document names the schema rwb_asset, the base /api/recovery/asset/v1, the topic rwb.asset.events.v1 with its retry and .dlt topics, the task queue rwb-asset in namespace rwb-recovery and the package th.co.scb.ace.workbench.recovery.asset
    Then the document publishes no event and consumes no event, and declares no Schedule: the recommendation is not an event and no source names one
    Then a build that adds an operation, a property outside the additive rule, an event, a topic or a Schedule fails the absence test
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The recommendation is exposed only as an additive property of the two reads that RWB-S5-E3019-CON baselined; no operation, base or status code is added | TSD S5 T-A.1 and T-A.2; Architecture v5 slide 11; FSD S5 A2.10.3.3 |
| BR2 | The element carries the rule ID and the package version in force, so a recommendation can never be read without the version that produced it | DP-03; FSD S5 BR-S5-010; legacy RWB-E3-027 AC1 |
| BR3 | The ACE asset fact and the COLLINS economics are consumed on the rwb-source-data contracts only; no `v_ace_*` path, property or grant is declared | DP-05; Architecture v5 slides 29, 37 and 45; FSD S5 A2.10.2 |
| BR4 | The case state is read and the case move is answered; `recovery_case` and its route states are never a property of this document | Ownership Map (recovery_case owner P3); GAP-2872 |
| BR5 | The route word is a closed value of the five words of the legacy criterion, and its mapping to `LOV-SALE-CHANNEL` is reference data, not a schema enumeration of the code | TSD S5 T3.2; GAP-2875; ASM-4771 |
| BR6 | The expected return is an amount with its currency and its model version; no percentage, threshold or target is a default or an example of the schema | BR-S5-010; R-DIS-19; GAP-2875 |
| BR7 | The contract carries identifiers, codes, amounts, dates and versions only; no personal data property, example or fake | Template and Rules v1 §R7.2 (s17); Architecture v5 slide 42 notes |
| BR8 | A consumed row whose operation name no source gives carries the placeholder and its gap; the fake is derived from the published document and never from the guess | Template and Rules v1 §R9; GAP-2872 |

### 9. State transitions

The document does not own the case machine; it fixes the closed values the schema may carry, which are the route states of the DISPOSAL machine of TSD S5 T4 that the recommendation reads and answers.

| Schema value | Where it appears | Meaning in the document |
|---|---|---|
| `ASSET_HELD`, `EVICTION_REQUIRED`, `TITLE_BLOCKED`, `ROUTE_RECOMMENDED` | The case state of the consumed rwb-case read and the move of its answer | The four states of the three rules; the document declares them as enumerated strings and owns none |
| `auction`, `broker`, `RAMC`, `buy-back`, `rental` | `recommended_route` and each ranked route | The five words of the legacy criterion; the mapping to `LOV-SALE-CHANNEL` is reference data (BR5) |
| `HELD` | The holding status of the consumed asset fact | Read only, unchanged by the recommendation |

| Element state | Event | Condition | To |
|---|---|---|---|
| Absent | The app story writes a recommendation | The record is committed | Present, with its ranked returns and its version |
| Present | A later step of the same case writes a new recommendation | The new package version is in force | Replaced, with the new version; the earlier record stays in the chain |
| Present | The record write fails | X1 of the app story | Unchanged, and the caller sees MSG-P7-003 |

The element is a projection of the decision record of the same case; it is not a stored row of its own, and the document declares no table for it (BR1, BR2).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| rwb-asset service owner (suggested TechX) | Owns the document, tags the baseline and answers the consumer sign-off |
| P3 rwb-case owner | Confirms the state read and the move answer rows and their fakes |
| P1 rwb-source-data owner | Confirms the asset and score product rows, their freshness stamps and their operation names |
| P7 rwb-decision owner | Confirms the package read and the rule and version element |
| Platform contract owner (`RWB-PLT-E1047-CON`, `RWB-PLT-E1027-CON`) | Confirms the naming baseline and the record schema the element is written into |
| RW-SALEOFF, RW-NPAMGR, RW-ENFORCE | The roles that read the recommendation; their rights are the TSD S5 T6.1 rows of AC4 |
| Every other role of TSD S5 T6.1 | Asset and disposal R: reads the element in scope, and the partner roles read it through the partner gateway |

The rights are the rows of TSD S5 T6.1 and nothing wider. The FSD says the feature runs unattended with the sale officer as also-user (FSD S5 A2.10.3.3), so the document declares right R on the two reads and no operation for the recommendation.

### 11. Data

| Element | Property | Type | Required | Unit or list | Source |
|---|---|---|---|---|---|
| RouteRecommendation | recommended_route | string | Yes | The five route words (BR5) | Legacy RWB-E3-027 AC1; GAP-2875 |
| RouteRecommendation | ranked_routes | array of RankedRoute | Yes | One entry per route | Legacy RWB-E3-027 AC1 |
| RouteRecommendation | reasons | array of string | No | Coded reasons, no personal data | R-DIS-19 ("with reasons") |
| RouteRecommendation | rule_id | string | Yes | `R-DIS-08`, `R-DIS-14`, `R-DIS-19` | Business Rules and Routing Logic v4 |
| RouteRecommendation | rule_version / package_version | string | Yes | The version in force | FSD S5 BR-S5-010; DP-03 |
| RouteRecommendation | decided_at | date-time | No | ISO 8601 | TSD S5 T3.0 (record columns) |
| RankedRoute | route | string | Yes | The five route words | Legacy RWB-E3-027 AC1 |
| RankedRoute | expected_return | object: amount, currency | Yes | Amount with its currency code | Legacy RWB-E3-027 AC1; unit Not specified in the source documents (GAP-2875; ASM-4771) |
| RankedRoute | model_version | string | No | The version of the economics it came from | FSD S5 A2.10.2 (`v_ace_score`); DF-ACE-270 to DF-ACE-279 |
| RankedRoute | reasons | array of string | No | Coded reasons of that route | R-DIS-19 |
| Consumed | the rwb-source-data asset properties | object | Yes | Asset reference, asset type, book value, holding status, transfer-in type, freshness stamp | TSD S5 T3.1 (DF-COL-028 to DF-COL-042); operation name Not specified (GAP-2872) |
| Consumed | the rwb-source-data score properties | object | Yes | Score key, model code, model version, score value, estimate value, freshness stamp | DF-ACE-270 to DF-ACE-279; operation name Not specified (GAP-2872) |
| Consumed | the rwb-case state and move properties | object | Yes | Case reference, route state, appraisal currency, title status; move, rule ID, version | DF-CAS-001 to DF-CAS-023; operation name Not specified (GAP-2872) |
| Not declared | any `v_ace_*` property, `recovery_case` row, `timer`, `decision_log_entry` or `rule_row` | — | — | — | DP-01, DP-05; BR3, BR4 |

The element properties are the design names of this baseline, because no source gives a representation for a recommendation (GAP-2874; ASM-4770). The field IDs of the consumed rows are those of the TSD S5 T3.1 and the Logical Data Model and Data Dictionary v8. **No table and no column** is declared: the element is a projection of the decision record, and `listing` and `asset_sale` are the pricing and sale stories' shapes.

**No personal data.** Every property is an identifier, a code, an amount with its currency, a date or a version. No name, address, contact value or identity number is declared, and every example and fake is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). The two operations are those of RWB-S5-E3019-CON; this baseline adds one property and no operation.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, each entry extended with `route_recommendation` (API-S5-001) | Asset and disposal, right R, scope applied | Not applicable |
| GET | `/assets/{assetId}` | Asset of status 200 out, extended with `route_recommendation` (API-S5-002) | Asset and disposal, right R, scope applied | Not applicable |

The errors stay those of the parent baseline: 401, 403 with MSG-P4-002, 404 for an unknown or out-of-scope asset, 422 with MSG-GEN-001 and 503 when the decision library or a consumed contract does not answer. The additive rule is the one that protects the consumers of the E3019 baseline: a property may be added to a response and only a new major version may rename or remove one (X2).

#### 12.2 REST operations consumed

| Operation | Base | Owner | Use |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset fact: asset reference, asset type, book value, holding status, transfer-in type and the freshness stamp; faked |
| The read of the COLLINS score product (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The economics: score key, model code, model version, score value, estimate value and the freshness stamp; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The route state, the appraisal currency and the title status; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | rwb-case (P3) | P3 rwb-case | The answer that carries `ROUTE_RECOMMENDED` or `ASSET_HELD` with the rule and its version; faked |
| The rule-package read (operation name Not specified in the source documents (GAP-2872; ASM-4768)) | rwb-decision (P7) | P7 rwb-decision | The DISPOSAL package at the version in force with R-DIS-08, R-DIS-14 and R-DIS-19; faked |

Each row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). None of the five rows is in this story's contract-dependency list, which is None, although all five are class C in fact; the absence is recorded as GAP-2872 with ASM-4768.

#### 12.3 Events published

None. The service's events are `AssetTakenOn` (EV-22) and `AssetSold`; neither is the recommendation, which is a projection of the decision record and a case move. This baseline declares no event name, no payload and no consumer, and the absence test fails a build that adds one (GAP-2874; ASM-4770).

#### 12.4 Events consumed

None. Architecture v5 slide 13 puts an E in the row of S5 under S4, but no source names the litigation event and no source names an event for the release or ready-to-sell facts, so this baseline declares no consumer group and no inbox row, and records the absence (GAP-2871; ASM-4766).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow referenced by the element | `rwb-asset` in namespace `rwb-recovery` | The stage child of `CaseWorkflow` that writes the recommendation of this baseline |
| `recommendDisposalRoute`, `releaseAssetToHold` | Activities referenced by the element | `rwb-asset` | The steps that produce the element and the case move; their inputs and outputs are the consumed rows and the element of section 11 |

The document fixes the element shapes the activities exchange and not their orchestration; the activity names are a design choice of the app story and are fixed by no source document.

#### 12.6 Schedules

None. JOB-19 Re-appraisal monthly is the service's only Schedule and belongs to RWB-S5-E3026-APP; the two-working-day target of R-DIS-19 is a timer of the workflow and is not a Schedule of this baseline.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| decision_record | PLT library, created in `rwb_asset` | The record the element is projected from (DP-03); this baseline declares its element shape, not its schema |
| idempotency_key | PLT library, created in `rwb_asset` | Referenced by the repeated signal rule of the app story |
| listing / asset_sale | S5 (`rwb_asset`) | Referenced only: the pricing and sale shapes, written by RWB-S5-E3028-APP and the auction stories |

Not declared and never read as a table: `recovery_case` (P3), `v_ace_npa_asset`, `v_ace_score` and `collateral` (P1), `decision_log_entry` and `rule_row` (P7). No foreign key leaves the schema (DP-01, DP-05).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data asset fake | The asset fact of `AST-2026-000511` for case `RC-2026-000511` at `HELD`; the same asset with the title still blocked; a stale product with its date; no answer beyond 2 s | AC1, AC3 |
| rwb-source-data score fake | The COLLINS economics with its model version and estimate; a stale score product; no answer beyond 2 s | AC2, AC3 |
| rwb-case state fake | The case at `ASSET_HELD`, at `EVICTION_REQUIRED` with the occupancy vacant and at `TITLE_BLOCKED` with the title clear; a case in none of the three | AC4 |
| rwb-case move fake | The moves `ROUTE_RECOMMENDED` and `ASSET_HELD` accepted; a move refused because the case is not in the state the rule expects | AC4 |
| rwb-decision package fake | The DISPOSAL package at its version in force with R-DIS-08, R-DIS-14 and R-DIS-19; a package one version behind | AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-22 answer with `route_recommendation` read once from this service | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the consumed rows are stubbed from the published documents and carry the placeholder until their owners confirm them (GAP-2872; ASM-4768), and the element property names carry their own gap (GAP-2874; ASM-4770).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 5 consumed | The two asset reads with the additive property on `/api/recovery/asset/v1`; the two rwb-source-data products, the rwb-case state read, the case-move answer and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The recommendation is not an event and no source names an event for it |
| Temporal | 1 workflow, 2 activities referenced | `AssetDisposalWorkflow` on `rwb-asset`; no Schedule |
| File | None | No file is described, read or delivered |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.asset`, module `route`, package `th.co.scb.ace.workbench.recovery.asset.route`; the document lives with the service's OpenAPI file and its AsyncAPI fragment is empty.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition in the document: no `v_ace_*` path, property or grant is declared, and the two ACE facts are the ones the rwb-source-data contracts answer. DP-03 fixes the element the recommendation is projected from. DP-13 and DP-19 fix the base and the route by which the element reaches the screens; the composite route itself is RWB-PLT-N001-CON.

**Build steps**

1. Extend the OpenAPI document of the service with the additive property and validate the additive rule (AC1).
2. Write the `RouteRecommendation` and `RankedRoute` elements with their required flags and the four closed lists (AC1, AC2).
3. Write the return unit, the model version and the coded reasons, with the placeholder where no source gives a unit (AC2).
4. Record the two rwb-source-data rows with their owners, budgets, freshness stamps and placeholders (AC3).
5. Record the rwb-case rows, the rights and the error envelope (AC4).
6. Record the decision-record element and the package read, and validate them against the library schema (AC5).
7. Publish the seven fakes and the drift test (AC6).
8. Record the naming baseline and the absence tests, then tag the baseline and collect the consumer sign-off (AC6).

**Done when.** The OpenAPI document validates in the pipeline, the five contract tests pass, every consumed row is answered by its fake, the drift test is green, and the app story, the pricing story and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this baseline raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this baseline raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field is absent or invalid, or a body fails schema validation (X1) | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares (X8) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the recommendation (AC5) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | An ACE data product of the case is stale; the check is the owner's and this service holds no batch status read (VR-S5-010-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The six message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-001 and MSG-S5-002 are carried because they are in the message set of the feature, and no path of this baseline raises them.

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states and SCR-22 Asset record in its held, listed and sold states, all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its recommendation, rwb-case for the case and its route state, rwb-source-data for the ACE asset fact and rwb-valuation for the valuation references; this baseline fixes the rwb-asset answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The held state of SCR-22 shows `route_recommendation` with the recommended route, the ranked returns and the reasons; the list state of SCR-21 shows the recommended route only. The refusal, not-recorded and stale-data states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-027-01 | AC1, AC2 | Contract | The asset fact and the COLLINS economics of `AST-2026-000511`; the contract half answers the element, the five route words and the ranked returns with their unit |
| TC-E3-027-02 | AC1, AC4 | Contract | Case `RC-2026-000511` at `EVICTION_REQUIRED` with the occupancy vacant; the contract half answers the release and the `ASSET_HELD` move shape |
| TC-E3-027-03 | AC1, AC4 | Contract | Case `RC-2026-000511` at `TITLE_BLOCKED` with the title clear; the contract half answers the release and the `ASSET_HELD` move shape |
| TC-E3-027-04 | AC5 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E3-027-05 | AC4 | Contract | RW-SALEOFF holds CRUA and RW-NPAMGR holds CRU; the contract half answers the rights of the two reads |
| TC-E3-027-06 | AC5, AC6 | Contract | The decision-record stub stopped and a stale data product; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S5-E3027-CON-01 | AC1 | Contract | The document validates; the property is additive on both answers and no operation, path, base or status code is added |
| TC-S5-E3027-CON-02 | AC1, AC2 | Contract | The element validates with its required flags, the five route words and the return unit; a value outside the five fails the vocabulary test |
| TC-S5-E3027-CON-03 | AC3 | Contract | The two rwb-source-data rows and their placeholders; the no-`v_ace_*` boundary and the 2 s budget |
| TC-S5-E3027-CON-04 | AC4, AC5 | Contract | The rwb-case rows, the rights and the error envelope; the decision-record element and the package read |
| TC-S5-E3027-CON-05 | AC6 | Contract | The seven fakes match the document and a drifted fake fails the build; the absence of an operation, an event, a topic and a Schedule |

The six legacy cases are the legacy cases of RWB-E3-027 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3027-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract. The five cases `TC-S5-E3027-CON-01` to `-05` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the wave 2 harness carries the `-ITG` copies.

### 17. Guardrails

- No business value in the contract: the five route words, the return unit, the two-working-day target, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts with their currency, dates and versions only; every example is synthetic.
- ACE data only through the owner's contract: no `v_ace_*` path, property or grant is declared, and a build that adds one fails the boundary test (DP-05).
- The case and the decision log stay with their owners: no `recovery_case` property and no `decision_log_entry` row is declared; the record is the local library element (DP-03).
- One base, one topic, one queue and one login per service; the document renames nothing that RWB-S5-E3019-CON baselined and adds no second base (DP-13, DP-14).
- No invented surface: no operation, event, topic or Schedule is declared for the recommendation, and every element name that no source gives carries its gap and its assumption (BR8).
- The additive rule is tested, not trusted: a rename or a removal within major version 1 fails the build (X2).

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| FEAT-AST-10 | Recommend the disposal route: proposes auction, broker, RAMC, buy-back or rental with the expected return on each, runs unattended (Epics 3 to 8 Specification v3; FSD S5 A2.10) | The element, its route vocabulary and the consumed rows | TC-S5-E3027-CON-01, TC-S5-E3027-CON-02 |
| REQ-S5-004 | A start price and a floor price are proposed for every asset (the pricing step that consumes this baseline; the story master carries no requirement id for this key, GAP-2873; ASM-4769) | The recommended route and its return on the two reads | TC-S5-E3027-CON-01 |
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval | The ranked RAMC, buy-back and rental routes | TC-S5-E3027-CON-02 |
| ADR-013 | 19 services inside ACE | rwb-asset as the owner of the contract | TC-S5-E3027-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget | TC-S5-E3027-CON-03 |
| ADR-022 | Local decision record plus central ledger | The element projected from the local record | TC-S5-E3027-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-027, disposition Split (rework) |
| Legacy criteria | None owned by this slice; AC1 to AC4 are RWB-S5-E3027-APP's, and their contract half is carried by TC-E3-027-01 to TC-E3-027-06 |
| Test cases | TC-E3-027-01 to TC-E3-027-06, TC-S5-E3027-CON-01 to TC-S5-E3027-CON-05 |
| Feature and screens | FEAT-AST-10, SCR-21 Asset list and SCR-22 Asset record |
| Rules | R-DIS-08, R-DIS-14 and R-DIS-19, named from the Business Rules and Routing Logic v4 |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour of the step, the ranking at run time and the case moves: RWB-S5-E3027-APP.
- The approval of the recommendation and the route submission: the next story of this service (R-DIS-20, R-DIS-27).
- The opening price, the floor and the `listing` shape: RWB-S5-E3028-APP.
- The auction rounds, the sealed bids and the `asset_sale` shape: the auction stories of this service.
- The case machine and the route states as rows: rwb-case (P3), whose state and move rows this baseline consumes and fakes (GAP-2872).
- The ACE asset, collateral and COLLINS score facts and the freshness of each data product: rwb-source-data (P1) (GAP-2872; ASM-4768).
- The agent-assisted advice named in R-DIS-19: rwb-agent (P10) and DP-20, which this key's pattern set does not carry (GAP-2872; ASM-4768).
