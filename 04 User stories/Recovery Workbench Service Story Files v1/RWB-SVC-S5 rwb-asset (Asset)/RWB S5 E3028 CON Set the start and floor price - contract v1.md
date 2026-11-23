# RWB-S5-E3028-CON Set the start and floor price - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3028-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-028 |
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

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the pricing step of rwb-asset, split from RWB-E3-028. It fixes the three asset operations of the step on `/api/recovery/asset/v1` that answer SCR-21 and SCR-23 and carry the listing create (DP-13), the listing and price element with its start price, floor price, channel, round and status, the closed lists that element is declared against, the six consumed rows (rwb-case state and case-move answer, rwb-agent proposal, rwb-source-data asset and COLLINS fact, rwb-valuation appraisal, rwb-decision approval), the decision-record element of DP-03, the fakes, the rights, the error envelope and the absence tests. No source gives the consumed rows a published operation name, a channel or status value for this step, the step schedule by asset class or the price-model reference (GAP-2881; ASM-4777). The approval answer, the proposal element and the appraisal element are not published either, and the fakes that answer them are derived with a placeholder (GAP-2877; GAP-2878; GAP-2880; ASM-4773; ASM-4774; ASM-4776). The baseline declares no event and no Schedule of its own, and it declares no table, operation or topic of another owner (DP-05, DP-14). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the pricing step of rwb-asset - the listing create in its two path forms and the two asset reads on `/api/recovery/asset/v1`, the listing and price element and its closed lists, the six consumed rows of rwb-case, rwb-agent, rwb-source-data, rwb-valuation and rwb-decision, the decision-record element, the rights, the error envelope and the fakes - baselined and tagged before the build starts**, so that **the application story, the two screens, the pricing agent, the valuation service and the wave 2 harness build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer, and a price field, a list value, an approval reference, a proposal or a case-move answer can never drift between rwb-asset, rwb-case, rwb-agent, rwb-source-data, rwb-valuation and rwb-decision without a failing build**.

This is the contract slice of legacy RWB-E3-028. It owns:

- the document that fixes the listing create and the two reads of the asset and its listing on base `/api/recovery/asset/v1`, with their parameters, their documented answer, their rights and their idempotency (DP-13);
- the listing and price element and its closed lists: the asset reference, the channel, `start_price`, `floor_price`, the round, the listed-at time, the status and the approval reference, declared against `LOV-LISTING`, `LOV-SALE-CHANNEL`, `LOV-ASSET-TYPE` and `LOV-HOLDING`;
- the six consumed rows: the rwb-case state read and case-move answer, the rwb-agent pricing proposal, the rwb-source-data asset and COLLINS fact, the rwb-valuation appraisal read and the rwb-decision approval, each with its owner, its use and the placeholder where no operation name is published (DP-05);
- the decision-record element of DP-03 and the local library dependency that carries it;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so that every consumed answer has a stub on Day 1;
- the naming and the boundary: one base, one topic, one queue, one login, no foreign schema, no monolith base, no Schedule and no event declared as this step's own.

It does not own: the pricing behaviour, the rule evaluation, the approval request, the listing writes and the case moves, which are RWB-S5-E3028-APP; the pricing agent, its model and its proposal, which are rwb-agent's (P10); the appraisal and its value, which are rwb-valuation's (S1); the ACE asset and COLLINS facts, which are rwb-source-data's (P1); the approval, its limit and its answer, which are rwb-decision's (P7) and rwb-access's (P4); the case of record and its route states, which are rwb-case's (P3); the publication of the listing and the auction rounds, which are the later stories of this service; and the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets six teams build at once. The pricing step of the legacy key crossed an officer screen, a pricing model, an appraisal, an approval of the floor and a case state in one process. In the target it crosses six boundaries, each owned by another service, so each has to be fixed before the application story starts: the listing and price element, the vocabulary of the lists the prices are declared against, the case state and the case-move answer, the proposal of the agent, the asset and appraisal facts, and the approval of the floor with the decision record.

The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset` (Architecture v5 slide 19 notes). It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case`, `rwb_decision` or `rwb_valuation`, so DP-05 is declared as a prohibition and the appraisal, the asset fact and the COLLINS economics are consumed on their owners' contracts only.

Two points are carried as gaps and assumptions rather than decided quietly. No source gives the consumed rows a published operation name, and the proposal, the appraisal and the approval elements are not published, so the baseline declares them as consumed with a placeholder and never as its own (GAP-2877; GAP-2878; GAP-2880; ASM-4773; ASM-4774; ASM-4776). The channel and status values of this step and the step schedule by asset class have no list in TSD S5 T3.2, so the element carries the placeholder and adds no enumeration member (GAP-2881; ASM-4777).

**What the baseline does not do.** It states no business outcome and fixes no business value: the percentage and the limit of the floor check, the step schedule, the proposal and the approval are values of their owners, read at their version, and no criterion here asserts a result the application story owns.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case`, `assignment` and `task` are P3's, `approval`, `decision_log_entry` and `rule_row` are P7's, `deviation` is S8's, `template` and `notice` are P6's, `proceeds` is P8's, `document` is P5's, the appraisal and valuation facts are S1's, and every `v_ace_*` view is P1's. This document never declares another service's table, operation or topic as its own.
- The rwb-case state and move rows, the rwb-agent proposal, the rwb-source-data fact, the rwb-valuation appraisal and the rwb-decision approval are published by their owners with fakes, so each consumed row names a real owner document; their operation names are Not specified in the source documents (GAP-2876; GAP-2877; GAP-2878; GAP-2880; ASM-4772; ASM-4773; ASM-4774; ASM-4776), and they are not in this story's contract-dependency row, which is None.
- The DISPOSAL rule package and its rows R-DIS-28, R-DIS-29 and R-DIS-17 are governed in rwb-decision (P7); this baseline names them and declares none of them, and the step schedule by asset class is a value of the package (GAP-2881; ASM-4777).
- The `listing` and `asset` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No approval is needed to publish a Draft baseline; the baseline is tagged when its contract tests pass and the consumers sign it off (§9).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the listing create in its two path forms and the two reads, with their request and answer elements, the filters, the rights, the `Idempotency-Key` rule and the error responses.
2. Fix the `Asset` element and the listing part of it: the asset reference, the channel, `start_price`, `floor_price`, the round, the listed-at time, the status and the approval reference, with the list each of them is declared against.
3. Fix the closed vocabulary of the lists the element uses: `LOV-LISTING`, `LOV-SALE-CHANNEL`, `LOV-ASSET-TYPE` and `LOV-HOLDING`, and record that this step's own channel and status values have no value in the sources.
4. Fix the six consumed rows: the rwb-case state read and case-move answer, the rwb-agent proposal, the rwb-source-data asset and COLLINS fact, the rwb-valuation appraisal and the rwb-decision approval, each with its owner, its use and the placeholder where the name is not published.
5. Record the decision-record element of DP-03, written before the listing row changes.
6. Record the naming baseline and the boundary: one base, one topic, one queue, one login, no foreign schema, no monolith base, no Schedule and no event of this step.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shapes, the `Idempotency-Key` rule, the rights, the error envelope, the absence of a `v_ace_*` read, of a `recovery_case` write and of an event.
9. Tag the baseline and hand it to RWB-S5-E3028-APP, the two screens, the pricing agent and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1, or a required element is added | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published owner document | None | AC3, AC4 |
| X5 | A value outside `LOV-LISTING`, `LOV-SALE-CHANNEL`, `LOV-ASSET-TYPE` or `LOV-HOLDING` appears in the document, in an example or in a fake | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row, a proposal, an appraisal value or an approval answer | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | The document declares an event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |
| X9 | The floor check has no percentage or limit value in the sources | The element declares the price check by its rule ID only and carries the placeholder; no percentage and no limit is written | None | AC4 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner documents of rwb-case, rwb-agent, rwb-source-data, rwb-valuation and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E3028-APP, the two screens, the pricing agent and the wave 2 harness on Day 1, and the rwb-case, rwb-agent, rwb-source-data, rwb-valuation and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the pricing step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing is S5, of recovery_case and task is P3, of approval and rule_row is P7, of the appraisal is S1 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The document validates and the listing create keeps the additive rule (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema and compared with the previous major version
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then it declares POST /assets/{assetId}/listings and POST /assets/{assetKey}/listings with a ListingRequest in and an Approval out, the right C, the errors 401, 403, 404, 409, 422 and 503, and the Idempotency-Key header
    Then no property is removed or renamed, no type changes and no new required property appears within major version 1
    Then a removal, a rename, a type change or a new required property is refused as a minor change and requires a new major version

  Scenario: AC2 The listing and price element and its closed lists are fixed (new, D-RCV-60)
    Given the asset and listing sections of the baseline
    When they are compared with TSD S5 T3.1 and T3.2 and with the closed lists of the service
    Then the listing element declares the asset reference, the channel, start_price, floor_price, the round, the listed-at time, the status and the approval reference
    Then both prices are declared as numbers with their scale, required, and never as an example constant, a default or a computed value
    Then sale_channel is declared against LOV-SALE-CHANNEL with the values DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION and RAMC, and listing status against LOV-LISTING with the values DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN
    Then asset_type is declared against LOV-ASSET-TYPE and holding_status against LOV-HOLDING, and no value is added to any list by this document
    Then this step's own channel and status values are Not specified in the source documents (GAP-2881; ASM-4777) and the element carries the placeholder
    Then the step schedule by asset class is declared as a value of the rule package in force and not as an enumeration or a constant of the document
    Then no personal data property is declared: the element carries references, amounts, codes and dates only

  Scenario: AC3 The rwb-agent proposal and the rwb-source-data and rwb-valuation facts are declared as consumed (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with R-DIS-28, R-DIS-17 and the owners of the facts
    Then the pricing proposal is declared as consumed from P10 rwb-agent with the asset, the appraisal reference and the COLLINS economics reference in, and the opening price, the floor as the reserve, the model reference and its version out
    Then the asset and COLLINS fact is declared as consumed from P1 rwb-source-data with the asset key, the asset class, the transfer-in type, the book value, the COLLINS economics reference and the freshness stamp
    Then the appraisal is declared as consumed from S1 rwb-valuation with the appraised value, its date, the model version and the outliers flag, and no appraisal property is declared as this service's own
    Then their operation names and call types are Not specified in the source documents (GAP-2877; GAP-2878; ASM-4773; ASM-4774) and each row carries the placeholder
    Then the document declares no v_ace_* path, no v_ace_* property, no model and no computed price

  Scenario: AC4 The rwb-case and rwb-decision rows and the floor check are declared with their placeholders (new, D-RCV-60)
    Given the consumed rows and the validation section of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with rwb-decision as the owner of approval and rule_row
    Then the case state read is declared with the case reference and the route state, and the case-move answer with the moves PRICE_PROPOSED, FLOOR_APPROVED and ASSET_HELD carrying the rule ID and its version
    Then the approval is declared as consumed from P7 rwb-decision as the kit's approval child workflow, with the case, the asset, the floor and the officer's proposal in, and the answered or refused answer with the approval reference out
    Then the floor check VR-S5-011-1 is declared by its rule ID with MSG-S5-001 and its two placeholders, and the percentage and the limit are Not specified in the source documents (GAP-2879; ASM-4775)
    Then the operation names of the case-move answer and of the approval are Not specified in the source documents (GAP-2876; GAP-2880; ASM-4772; ASM-4776) and each row carries the placeholder
    Then the document declares no recovery_case property, no case row write, no approval answer and no rule row of its own

  Scenario: AC5 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S5 T-A.1, T6.1 and the platform envelope
    Then the two reads declare Asset and disposal right R with the scope applied, and the two listing paths declare right C with the scope applied and the Idempotency-Key rule
    Then RW-SALEOFF holds CRUA, RW-ENFORCE and RW-NPAMGR hold CRU, the service identities SY-CASEWF, SY-RULES, SY-DATALOAD and SY-AGENT hold R, C or U as the matrix gives them, and RW-HEADNPA holds RA
    Then the reads answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, and the listing create answers 400, 401, 403, 404, 409, 422 and 503, each with one envelope and one message ID per condition
    Then a role outside the matrix is refused at the edge and the refusal is the same envelope
    Then no operation of this baseline declares a right U or A; the right U of the auction rounds belongs to the later story of this service

  Scenario: AC6 The decision-record element and the seven fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version in force, the model version, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the listing row changes, and a failed write leaves it unchanged with MSG-P7-003
    Then the rwb-case fake answers the states ROUTE_APPROVED_AUCTION, PRICE_PROPOSED, FLOOR_APPROVED, REAPPRAISAL_RECEIVED and ASSET_HELD of case "RC-2026-000512", an accepted move and a refused move
    Then the rwb-agent fake answers the proposed opening price and the floor as the reserve with the model reference, and the rwb-valuation fake answers an accepted value and a rejected value
    Then the rwb-source-data fake answers the asset and COLLINS fact with its freshness stamp, and the rwb-decision fake answers the approval answered and refused
    Then the decision-record stub answers a healthy chain and a stopped chain, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming and the boundary are fixed and nothing is published (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are listing and asset, and the library objects decision_record and idempotency_key, and recovery_case, task, approval, rule_row, appraisal, template, proceeds, document, decision_log_entry and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no event consumed, no second topic, no consumer group and no Schedule, and the absence test fails a build that adds one
    Then the two listing paths are declared as one operation in two forms and neither is declared as another service's
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3028-APP, they fix no business value, and they copy no criterion of the legacy story, whose four criteria stay with the application story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The listing and its two prices are rwb-asset's, and the contract declares their fields, their lists and their required flags on the listing element only | Architecture v5 slide 41; Ownership Map (`listing` owner S5); TSD S5 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the listing row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy RWB-E3-028 AC1 and AC4 |
| BR3 | The proposal stays with rwb-agent and the appraisal with rwb-valuation: the contract declares both as consumed and declares no model, no computed price and no appraisal property | R-DIS-28 ("Pricing agent proposes"); R-DIS-17 ("Update the appraised value"); GAP-2877; GAP-2878 |
| BR4 | The approval stays with rwb-decision and the limit with rwb-access: the contract declares the approval child workflow as consumed and declares no approval answer, no percentage, no limit and no authority row | Temporal and Drools Design slides 12 and 13; Ownership Map (`approval` owner P7); GAP-2879; GAP-2880 |
| BR5 | The case move is answered and not written: the contract declares the state read and the answer, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); GAP-2876 |
| BR6 | The ACE facts stay with rwb-source-data: the contract declares the asset and COLLINS fact as consumed and declares no `v_ace_*` path and no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45 |
| BR7 | Nothing is published by this step: the contract declares no event of its own, no second topic and no outbox row, and names `AssetTakenOn` and `AssetSold` as the service's only events | Architecture v5 slide 19 OUT and slide 43 |
| BR8 | The vocabulary is closed: `LOV-LISTING`, `LOV-SALE-CHANNEL`, `LOV-ASSET-TYPE` and `LOV-HOLDING` are published as enumerated values, and no value is added by this document | TSD S5 T3.2; FSD S5 A2.11.3.1 BR-S5-011; GAP-2881 |
| BR9 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR10 | The floor check is declared by its rule ID and its message only: no percentage and no limit is a constant, a schema default or an enumeration member | VR-S5-011-1; FSD S5 A2.11.3.1; GAP-2879 |
| BR11 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule and model version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR12 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |

### 9. State transitions

The lifecycle of this document, not of an asset and not of a case:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The three operations, the listing and price element, the lists, the six consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the pricing agent, the wave 2 harness and the owners of rwb-case, rwb-agent, rwb-source-data, rwb-valuation, rwb-decision and rwb-access accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional filter or a new optional listing reference | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, or a new required property appears | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC7 fail: a `v_ace_*` view, a `recovery_case` property, a proposal, an appraisal value, an approval answer, an event, a second topic or a Schedule | In review |
| Baselined | A consumed owner publishes a changed answer | The consumed row is re-derived from the owner's document and in review again | In review |

The listing status, the route state and the approval state that the document describes are the application story's and their owners': `LOV-LISTING` is DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN, the route states are rwb-case's, and this baseline fixes the vocabulary and moves nothing.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the ownership rows the baseline consumes |
| Consuming teams (the app story, the two screens, the pricing agent, the wave 2 harness and the owners of rwb-case, rwb-source-data, rwb-valuation, rwb-decision and rwb-access) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the approval child workflow, the decision-record library and the event envelope this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, and that the prices and the model are references |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Asset element | The columns of DF-COL-028 to DF-COL-042, as declared by the asset reads of the service |
| Listing element | The columns of DF-SAL-001 to DF-SAL-008: `id`, `asset_id`, `sale_channel`, `start_price`, `floor_price`, `round_no`, `listed_at` and `status` |
| References of the element | The asset reference, the approval reference, the model reference with its version and the case reference |
| Lists | `LOV-LISTING`, `LOV-SALE-CHANNEL`, `LOV-ASSET-TYPE` and `LOV-HOLDING`, published as enumerations and read as reference data at their version |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the listing row changes (DP-03) |
| Rule rows | DF-REF-001 to DF-REF-015 of P7, named by their rule ID and read as the package version in force, never declared here |
| ACE asset, score and valuation fact | DF-ACE-187 to DF-ACE-195, DF-ACE-208 to DF-ACE-219 and DF-ACE-270 to DF-ACE-279 of P1, read only through the owner's contract and never written, copied or joined here |
| Not declared here | recovery_case, assignment and task (P3), approval and rule_row (P7), appraisal (S1), deviation (S8), template and notice (P6), proceeds (P8), document (P5) |
| Consumed fields with no source | The channel and status values of this step, the step schedule by asset class, the percentage and the limit of the floor check, the model reference, and the operation names of the case move, the proposal, the appraisal and the approval: Not specified in the source documents (GAP-2877, GAP-2878, GAP-2879, GAP-2880, GAP-2881; ASM-4773, ASM-4774, ASM-4775, ASM-4776, ASM-4777) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2, the three operations of AC1 and the additive rule. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and its listing (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |
| POST | `/assets/{assetId}/listings` | ListingRequest in, Approval out (API-S5-004); 409 when the case or the listing is not in the state the rule expects | Asset and disposal, right C, scope applied | `Idempotency-Key` header |
| POST | `/assets/{assetKey}/listings` | The business-key form of API-S5-004, in the Ownership Map row; the same ListingRequest and Approval | Asset and disposal, right C, scope applied | `Idempotency-Key` header |

The four operations answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, and the two listing paths also answer 409, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S5 T-A.1 and the paths are those of the target base, not the monolith form. The two listing paths are one operation in two forms: the Ownership Map carries the business-key form and TSD S5 T-A.1 carries the `{assetId}` form, and the API v2 asset paths are superseded in v3 by the business-key path under the Ownership Map ruling ASM-0052. A separate listing read is not declared, because the listing is answered inside the `Asset` element of `/assets/{assetId}` (GAP-2881; ASM-4777). API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's under ASM-0043 and API-S5-005 `POST /listings/{listingId}/rounds` belongs to the auction rounds story of this service; neither is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The route state and the case reference the element and the answer carry; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2876; ASM-4772)) | rwb-case (P3) | P3 rwb-case | The moves `PRICE_PROPOSED`, `FLOOR_APPROVED` and `ASSET_HELD` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The pricing proposal (operation name and call type Not specified in the source documents (GAP-2877; ASM-4773)) | rwb-agent (P10) | P10 rwb-agent | The opening price and the floor as the reserve with the model reference and its version; faked |
| The asset and COLLINS fact (operation name Not specified in the source documents (GAP-2877; ASM-4773)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The asset key, asset class, transfer-in type, book value, COLLINS economics reference and freshness stamp; faked |
| The appraisal read (operation name Not specified in the source documents (GAP-2878; ASM-4774)) | `/api/recovery/valuation/v1` | S1 rwb-valuation | The appraised value, its date, the model version and the outliers flag; faked |
| The approval child workflow of the kit (element names Not specified in the source documents (GAP-2880; ASM-4776)) | rwb-decision (P7), its own task queue | P7 rwb-decision | The approval of the floor with the answered or refused answer and the approval reference; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020); the approval is a Temporal child workflow and not a chained REST call, so it keeps the one-hop rule. The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2876, GAP-2877, GAP-2878 and GAP-2880 with their assumptions.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives rwb-asset exactly two events, `AssetTakenOn` and `AssetSold`; the take-on is RWB-S5-E3019-APP's and the sale and its `AssetSold` are the sale and auction stories', and the pricing step changes no state another service subscribes to. This baseline therefore declares no outbox row, no second topic and no Schedule, and the absence test of AC7 fails a build that adds one.

#### 12.4 Events consumed

None, and the flow needs none. The step is signalled by the parent after the route approval, the proposal and the appraisal are reads, and the approval comes back as the child workflow's answer. The four events the service does consume, `JudgmentRecorded`, `AuctionResult`, `ProceedsMatched` and `PartnerResultSubmitted`, belong to the take-on, sale and proceeds steps (Architecture v5 slides 19 and 43). `DeviationRaised` and `DeviationCleared` are consumed by rwb-case, rwb-comms and rwb-treatment, not by rwb-asset (Architecture v5 slide 42 rows 06 and 07). This baseline declares no consumer group, no subscription and no inbox of its own.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | The stage that hosts the pricing step; its signals and its outcome for the parent are declared, not built |
| `setStartAndFloorPrice` | Activity, the pricing step | `rwb-asset` | The case and the asset in; the rule ID with its package version, the listing reference, the approval reference and the case move out |
| `ApprovalWorkflow` (the kit's approval child) | Child workflow, owned by rwb-decision | rwb-decision's queue | Consumed, declared as the owner's and never as this service's |

No child workflow for the case and none for the money exists in this service. The activity names are a target design choice and the trigger is read as the stage signal after the auction route approval, because FEAT-AST-11 is a User feature and the FSD declares no background event for it (FSD S5 A2.11.4.4). No activity is registered by this story.

#### 12.6 Schedules

None. The step runs from the stage signal, the officer's request and the approval answer; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to the re-appraisal story of this service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| listing | S5 (`rwb_asset`) | The listing of the asset with its channel, its two prices, its round, its listed-at time, its status and its approval reference; the table the `Asset` answer reads and the listing create writes |
| asset | S5 (`rwb_asset`) | Read by the element: the asset reference, the asset class, the book value and the holding status. The row is absent from the Ownership Map table list and its owner is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2884; ASM-4780) |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated listing create and the answer it holds |

`recovery_case`, `assignment` and `task` (P3), `approval`, `decision_log_entry` and `rule_row` (P7), `appraisal` and `valuation` (S1), `deviation` (S8), `template` and `notice` (P6), `proceeds` (P8), `document` (P5) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or another owner's rows, and no foreign key leaves the schema (DP-01). No `outbox_event` row is declared, because nothing is published.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The states `ROUTE_APPROVED_AUCTION`, `PRICE_PROPOSED`, `FLOOR_APPROVED`, `REAPPRAISAL_RECEIVED` and `ASSET_HELD` of case `RC-2026-000512`; an accepted move and a refused move | AC4, AC6 |
| rwb-agent pricing fake | The proposed opening price and the floor as the reserve with the model reference and its version; no answer beyond 2 s | AC3, AC6 |
| rwb-source-data asset fake | The asset key, asset class, transfer-in type, book value, COLLINS economics reference and freshness stamp | AC3, AC6 |
| rwb-valuation appraisal fake | The appraised value accepted with `outlier_flag = N`, and a value rejected with `officer_accepted = N` | AC3, AC6 |
| rwb-decision approval fake | The approval of the floor answered with its reference; the approval refused; an approval not answered inside the budget | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000512`, with the asset, its listing and its prices read once | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT. The answers of the rwb-agent proposal, the rwb-source-data fact, the rwb-valuation appraisal and the rwb-decision approval are derived from the published owner documents and carry the placeholder until their owners confirm them (GAP-2877, GAP-2878, GAP-2880; ASM-4773, ASM-4774, ASM-4776). The drift test of AC6 compares each fake with the document, so a fake that drifts from its owner's published answer fails the build.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 5 consumed | The two reads and the listing create in its two path forms on `/api/recovery/asset/v1`; the rwb-case state read, the rwb-case case-move answer, the rwb-agent proposal, the rwb-source-data fact and the rwb-valuation appraisal; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The step publishes nothing and subscribes to nothing; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 activity and 1 child workflow declared, 0 registered | `AssetDisposalWorkflow` and `setStartAndFloorPrice` on `rwb-asset`; the approval child workflow on rwb-decision's queue; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no listing, no case, no proposal and no approval. What it publishes is one OpenAPI 3.1 document, nine contract tables and seven fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset` element with the listing part, the `AssetPage` element, the `ListingRequest` and `Approval` elements, the vocabulary of the four lists as published enumerations, the contract README rows for the six consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema, because rwb-asset holds none (Architecture v5 slides 29, 37 and 45; GAP-2877). DP-13 moves the base of the operations and nothing else. DP-19 is behind SCR-21 and SCR-23, whose screen model is the edge contract's. DP-09 is not in the pattern set of this key, which is consistent with a step that publishes nothing and consumes nothing.

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. The six consumed rows are C dependencies in fact and not in the metadata row (GAP-2876, GAP-2877, GAP-2878, GAP-2880; ASM-4772, ASM-4773, ASM-4774, ASM-4776).

**Build steps**

1. Write the three operations of AC1, both listing path forms included, and validate the additive rule in the pipeline.
2. Write the listing element of AC2 and its four lists, with the placeholder where a value has no source, and the no-personal-data schema test.
3. Record the rwb-agent, rwb-source-data and rwb-valuation rows of AC3 with their owners, their paths and their placeholders.
4. Record the rwb-case and rwb-decision rows and the floor check of AC4 with their placeholders.
5. Record the rights and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the seven fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the contract tests of section 16 pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens, the pricing agent, the wave 2 harness and the five consuming owners have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | The floor sits below the percentage of fair market value the approver's level may sign; the element declares the rule ID and both placeholders, and no path of this baseline raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this baseline raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the listing row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. MSG-S5-002 is carried because it is in the message set of the feature, and no path of this baseline raises it.

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states and SCR-23 Listing and price in its draft, below-limit, approved and published states, all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its listing and its prices, rwb-case for the case and its route state, rwb-decision for the approval of the floor and rwb-agent for the proposal; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The below-limit, refused, not-recorded and approved states the application story shows read the messages of section 14 on the same route, and the published state is written by the publication story of this service.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-028-01 | AC1, AC2, AC5 | Contract | The asset `AST-2026-000512` of case `RC-2026-000512`; the contract half answers the listing create, the listing element, the four lists and the rights of the operations |
| TC-E3-028-02 | AC3, AC6 | Contract | The proposal of rwb-agent and the appraisal of rwb-valuation; the contract half answers the two consumed elements, their placeholders and the drift test of their fakes |
| TC-E3-028-03 | AC3, AC4 | Contract | The asset, COLLINS and freshness facts of rwb-source-data; the contract half answers the element, its references and the case and approval rows with their placeholders |
| TC-E3-028-04 | AC4, AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element written before the change |
| TC-E3-028-05 | AC5, AC7 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers the 403 with MSG-P4-002, the 400 of the envelope and the absence tests of the boundary |
| TC-E3-028-06 | AC1, AC6 | Contract | A forced vocabulary violation and a drifted fake; the contract half answers the failing vocabulary and drift tests and the additive rule |
| TC-S5-E3028-CON-01 | AC1 | Contract | The document validates against OpenAPI 3.1; the three operations in four paths, the base, the filters, the `Idempotency-Key` rule and the seven error answers are present |
| TC-S5-E3028-CON-02 | AC2 | Contract | The listing element validates with its two prices, its references and its status; the four closed lists are published and no list value is added; the channel and status placeholders are present |
| TC-S5-E3028-CON-03 | AC3, AC4 | Contract | The six consumed rows and their placeholders; the proposal, the asset fact, the appraisal, the case and the approval rows name their owner and their path and declare nothing of another service's |
| TC-S5-E3028-CON-04 | AC6, AC7 | Contract | The seven fakes match the document and a drifted fake fails the build; no event, no second topic, no Schedule, no `v_ace_*` property and no `recovery_case` property |

The six legacy cases are the legacy cases of RWB-E3-028 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3028-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S5-E3028-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the percentage and the limit of the floor check, the step schedule, the proposal, the model reference, the channels, the listing statuses and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule and model version only; every example is synthetic.
- ACE data only through the owner's contract or the service's own `v_ace_*` views: the document declares no `v_ace_*` path and no `v_ace_*` property, and rwb-asset holds no such grant (BR6).
- The case stays with rwb-case, the approval with rwb-decision, the proposal with rwb-agent and the appraisal with rwb-valuation: the document declares no `recovery_case` property, no approval answer, no model and no appraisal value, and no case row write (BR3, BR4, BR5).
- The money stays with rwb-payment: the document declares no posting, no balance and no proceeds property.
- One base, one topic, one queue and one login per service; a document that names another service's base, topic or operation as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row, a shared job table or a monolith base.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the approval child workflow and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-004 | A start price and a floor price are proposed for every asset, and the floor is approved by the named role; the contract fixes the element, the two prices, the approval reference and the records on which the pricing step is built (FSD S5 requirements served; Epics 3 to 8 Specification v3 FEAT-AST-11). The split plan carries no requirement id for this slice, and the absence is recorded (GAP-2882; ASM-4778) | The listing element, the two prices, the approval reference, the decision-record element and the six consumed rows | TC-E3-028-01, TC-E3-028-04, TC-S5-E3028-CON-02, TC-S5-E3028-CON-03 |
| ADR-014 | Schema and login per service | The base and the login the document names | TC-S5-E3028-CON-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed REST rows with their budget and breaker, and the approval child workflow | TC-S5-E3028-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the change | TC-E3-028-04, TC-S5-E3028-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-028, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S5-E3028-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S5-E3028-CON-01 to -04 |
| Feature and screens | FEAT-AST-11, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-28, R-DIS-29 and R-DIS-17, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the three operations, the evaluation of R-DIS-28, R-DIS-29 and R-DIS-17, the approval request, the listing writes and the case moves: RWB-S5-E3028-APP.
- The pricing agent, its model, its version and the reserve basis: rwb-agent (P10) (GAP-2877; GAP-2883).
- The appraisal, its value, its date and the outliers check: rwb-valuation (S1) and SVAF (GAP-2878).
- The asset, COLLINS and NPA facts and the freshness of the data product: rwb-source-data (P1).
- The approval, its limit and its answer, and the delegated-authority rows: rwb-decision (P7) and rwb-access (P4) (GAP-2879; GAP-2880).
- The case of record, its route states, `assignment`, `task`, `timer` and the parent `CaseWorkflow`: rwb-case (P3) (GAP-2876).
- The publication of the listing and its schedule (R-DIS-33 to R-DIS-35): RWB-S5-E3029-APP.
- The descending price schedule, the vendor allocation and the auction rounds (R-DIS-30 to R-DIS-32, R-DIS-36 to R-DIS-39): the wave 2 auction stories of this service, API-S5-005.
- The sale, the bid acceptances and the `AssetSold` publication (R-DIS-40 to R-DIS-52): the sale stories of this service.
- The authoring, testing and approval of the DISPOSAL package and its step schedule: rwb-decision (P7).
- The document, its custody and its retention, and the evidence of the listing as documents: rwb-document (P5).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
