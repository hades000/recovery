# RWB-S5-E4034-CON Sell through a broker - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the broker-route step of rwb-asset, split from RWB-E4-034. It fixes the two asset reads and the listing create on `/api/recovery/asset/v1` (DP-13), the `Listing` element with its fee and terms properties and its closed lists, the round element where the route needs it, the consumed rwb-partner instruction element and its answer, the consumed rwb-case state and move rows, the rwb-comms template row, the rwb-payment auto-debit row and the rwb-decision package row, the rights and the error envelope, the decision-record element of DP-03, the fakes and the absence tests. The listing path is declared in the business-key form the later API versions carry; the broker instruction, the case-move answer, the template price read and the auto-debit request have no published operation shape and the fee and terms have no column set; the module event list gives the service one published event where the catalogue gives two; the rule package reaches four services and not this one; and the baseline is used while it sits in Draft with no approval record (GAP-2967 to GAP-2971; ASM-4870 to ASM-4879). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E4034-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 19 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S5-E4034-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-034 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Contract version | v1 (path version of /api/recovery/asset/v1) |
| Size | Not specified in the source documents (DOR-RWB-S5-E4034-CON-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **tech lead**, I want **the published contract baseline of the broker route of rwb-asset — the two asset reads and the listing create on `/api/recovery/asset/v1`, the `Listing` element with its fee and terms properties and its closed lists, the round element, the consumed rwb-partner, rwb-case, rwb-comms, rwb-payment and rwb-decision rows, the rights, the error envelope, the decision-record element and the fakes**, so that **the app story, the two screens and the wave 3 harness build against one fixed, testable contract on Day 1 and a listing property, a list value, an instruction property or an answer shape can never drift between rwb-asset, rwb-case, rwb-partner, rwb-comms, rwb-payment and rwb-decision without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020), and the typed Temporal interface on the owner's queue is the same decision for the broker call (Architecture v5 slide 24). The legacy route of RWB-E4-034 crossed five boundaries in one transaction: an officer screen, the case state, a partner instruction, a template price and an auto-debit. The target splits them: rwb-case owns the case and its route states, rwb-partner owns the broker and its instruction, rwb-comms owns the template and its price, rwb-payment owns the auto-debit and the money, rwb-decision owns the approval and the package, and rwb-asset owns the listing, the route outcome and the step.

Each boundary is a contract another team builds against, so each is fixed before the app story starts: the `Listing` fields, the values of `LOV-SALE-CHANNEL`, `LOV-LISTING` and `LOV-HOLDING`, the listing create and its answer, the read shapes, the instruction element and its answer, the case state and move, the template row, the auto-debit row, the rights and the record of the decision. The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset`, and records that rwb-asset holds no `v_ace_*` grant and no grant on another `rwb_*` schema, so DP-05 is declared as a prohibition and every foreign fact is consumed on its owner's contract only.

Four points are carried as gaps rather than decided quietly: the broker fee and terms have no rule row, no column set and no value, and the four consumed shapes are unpublished (GAP-2967), the legacy feature's title and its criteria disagree on which route it builds (GAP-2968), the listing path form and the legacy Data, Endpoints and Screen rows name another owner's tables and superseded paths (GAP-2969), and the event list and the rule-package delivery disagree with the catalogue (GAP-1942, GAP-1944).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- Ownership is taken from the Ownership Map and the context pack only: `listing` and `asset_sale` are S5's, `recovery_case` and `task` are P3's, `proceeds` is P8's, `document` is P5's, `template` and `notice` are P6's, `decision_log_entry`, `rule_row` and `approval` are P7's, `partner_instruction` and `partner` are S9's, and every `v_ace_*` view is P1's. `asset` has no Ownership Map row although Architecture v5 slides 19 and 41 and TSD S5 T3.1 give it to S5 (GAP-2969; ASM-4872).
- The rwb-case state and move rows, the rwb-partner instruction element, the rwb-comms template row, the rwb-payment auto-debit row and the rwb-decision package and approval rows are published with their fakes, so each consumed row names a real owner document; they are not in this story's contract-dependency row, which is None (GAP-2967, GAP-1944; ASM-4870, ASM-4874).
- The `listing`, `asset_sale` and `asset` tables arrive with the DB story of this service, including the additive broker fee and terms columns it adds under DP-15; this baseline declares shapes and creates no table, no column and no migration (GAP-2967; ASM-4879).
- The DISPOSAL package and its rows for R-DIS-24, R-DIS-25 and R-DIS-26 are governed in rwb-decision (P7); this baseline names them and declares none of them (GAP-1944; ASM-4874).
- The lifecycle of this document is the one in §9; no approval is recorded in this run, so the baseline is used in Draft under D-RCV-60 (GAP-2971; ASM-4876).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads and the listing create with their request and answer elements, the filters, the rights, the `Idempotency-Key` rule and the error responses.
2. Fix the `Listing` element: the columns of DF-SAL-001 to DF-SAL-008, the additive fee and terms properties, their types, their required flags and the list each is declared against.
3. Fix the round element of API-S5-005 where the route needs a round, and state that its behaviour is the auction stories'.
4. Fix the consumed rows: the rwb-partner instruction element and its answer, the rwb-case state read and move answer, the rwb-comms template row, the rwb-payment auto-debit row and the rwb-decision package row, marking every field the sources do not give with the placeholder.
5. Record the decision-record element of DP-03, written before the listing row changes.
6. Record the closed vocabulary of the lists, the rights of the two TSD S5 T-A.1 rows and the rule that no value is a constant of the code.
7. Publish the tables of §12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a `v_ace_*` read and of a foreign row write, the drift between a fake and the document, and the absence of a published event and of a Schedule.
9. Tag the baseline and hand it to RWB-S5-E4034-APP, the two screens and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A request or response body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A value outside `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING` or `LOV-ASSET-TYPE` appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation or table as provided, a `v_ace_*` view, a `recovery_case`, `partner_instruction` or `template` row | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | The document declares a published event, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights or the error answers of an operation are not the ones TSD S5 T-A.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-case, rwb-partner, rwb-comms, rwb-payment and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E4034-APP, the two screens and the wave 3 harness on Day 1, and the five owner teams on the same day |
| Estimable | One OpenAPI document, one AsyncAPI fragment, one consumed instruction element, nine contract tables, seven fakes and four new contract tests |
| Small | One sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the broker route of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case and task is P3, of proceeds is P8, of template and notice is P6, of decision_log_entry, rule_row and approval is P7, of partner_instruction and partner is S9, and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The document validates and the additive rule holds on every element (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then no operation, path parameter, required property or list value of major version 1 is renamed or removed, and a change that needs one is declared as a new major version
    Then each element the baseline adds is optional or additive, so a consumer of major version 1 keeps validating against the new document

  Scenario: AC2 The listing and round elements are fixed with their fee and terms properties and their closed lists (new, D-RCV-60)
    Given the listing section of the baseline
    When it is compared with TSD S5 T3.1, T3.2 and appendix T-A.1
    Then the Listing element declares the properties of DF-SAL-001 to DF-SAL-008: id, asset_code, sale_channel, start_price, floor_price, round_no, listed_at and status
    Then sale_channel is declared against LOV-SALE-CHANNEL with the values DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION and RAMC, and status against LOV-LISTING with the values DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN
    Then id, asset_code, sale_channel, start_price, floor_price, round_no and status are required and listed_at is optional
    Then the fee and terms properties are declared on the listing or the sale element as optional additive properties, and their names, types and required flags are Not specified in the source documents (GAP-2967; ASM-4870)
    Then the create operation POST /assets/{assetKey}/listings declares ListingRequest in and Approval out with the answers 400, 401, 403, 404, 409, 422 and 503, a required Idempotency-Key and the right C of Asset and disposal
    Then the round operation POST /listings/{listingId}/rounds declares AuctionRoundRequest in and AssetSale out with the right U, a required Idempotency-Key and the answers TSD S5 T-A.1 gives it, and its behaviour is declared as the auction stories'
    Then no property is added for the case route state, the partner, the template price or the auto-debit, and those facts are referenced as identifiers of their owners

  Scenario: AC3 The consumed rwb-partner instruction element and its answer are declared (new, D-RCV-60)
    Given the consumed and workflow sections of the baseline
    When they are compared with Architecture v5 slides 19 and 24, the Ownership Map and TSD S5 T-A.1
    Then the instruction is declared as the activity Partner.issueInstruction on task queue rwb-partner in namespace rwb-recovery, produced and executed by S9 rwb-partner, not as a REST operation of rwb-asset
    Then its request element carries the instruction type, the partner reference, the asset reference, the listing reference and the fee and term references, and its answer element carries the instruction reference and the issued-at time
    Then the property names, types and required flags of both elements are Not specified in the source documents (GAP-2967; ASM-4870) and the rows carry the placeholder
    Then the document declares no partner_instruction property, no partner row write and no grant on rwb_partner, and the boundary test fails a build that adds one
    Then the call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC4 The rwb-case, rwb-comms template, rwb-payment auto-debit and rwb-decision package rows are declared with their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the Ownership Map and the owner contracts
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and a move carrying the rule ID and its version
    Then the template read is declared as consumed from P6 rwb-comms with the template code, its language, its version and the price the buy-back terms are agreed at
    Then the auto-debit request is declared as consumed from P8 rwb-payment with the case reference, the rental terms reference and the mandate reference
    Then the package in force is declared as consumed from P7 rwb-decision with the package code and its version, and the approval answer as the ApprovalWorkflow element of the same owner
    Then every operation name, request shape and answer shape of these rows that no source publishes is Not specified in the source documents (GAP-2967, GAP-1944; ASM-4870, ASM-4874) and the row carries the placeholder
    Then the document declares no recovery_case, template, proceeds or posting property and no write of a foreign row

  Scenario: AC5 The rights and the error envelope are fixed for every operation (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S5 T-A.1 and T6.1
    Then both reads declare Asset and disposal right R with the scope applied, the listing create declares right C and the round operation right U
    Then RW-SALEOFF holds CRUA, RW-NPAMGR and RW-ENFORCE hold CRU, and every other role of TSD S5 T6.1 holds the right the matrix gives it
    Then the rights of the two Ownership Map rows are carried onto the paths the baseline declares, and the difference between the two path forms is recorded (GAP-2969; ASM-4872)
    Then every operation declares the same error envelope with 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503, and one message ID per condition
    Then every POST declares the Idempotency-Key and describes its stored answer, and no GET declares the header

  Scenario: AC6 The decision-record element and the fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the listing or route reference, the rule ID, the package version in force, the approval reference, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the listing row changes, and a failed write leaves the listing unchanged with MSG-P7-003
    Then the rwb-case fake answers the state read and the accepted and refused move, and the rwb-partner fake answers the instruction and its answer
    Then the rwb-comms fake answers the template at its version and a version not in force, the rwb-payment fake answers the auto-debit, the rwb-decision fake answers the package in force and the approval answer, and the record stub answers a healthy chain and a stopped chain
    Then the gateway-bff fake answers the merged SCR-21 and SCR-23 read, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming and the boundary are fixed and no event is published by this step (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the base is /api/recovery/asset/v1, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are listing, asset_sale, asset and the library objects decision_record and idempotency_key, and recovery_case, task, proceeds, document, template, notice, decision_log_entry, rule_row, approval, partner_instruction, partner and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the step declares no published event, no consumed event, no second topic and no Schedule, records that AssetTakenOn belongs to the take-on story and AssetSold to the sale story, and states that the module event list gives the service one event while the catalogue gives two (GAP-1942; ASM-4873)
    Then the document declares no operation of another service as provided, and the absence and boundary tests fail a build that adds one
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E4034-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word. No fee, term, price, state value or route condition is stated here as a business rule: the parameters of R-DIS-24, R-DIS-25 and R-DIS-26 stay with the package and the app story (GAP-2967, GAP-2968; ASM-4870, ASM-4871).

AC8. Given the contract is published, when each rule BR1 to BR14 of section 8 is checked, then the declared elements meet the rule and each rule has a test case in section 16.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The listing is rwb-asset's, and the contract declares its fields, lists, required flags and two POST operations on the `Listing` element and the listing paths only | Architecture v5 slide 41; TSD S5 T3.1, T3.2 and appendix T-A.1 |
| BR2 | The decision record is declared as an element written before the listing row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy AC1 and AC4 |
| BR3 | The ACE sale and asset facts stay with rwb-source-data: rwb-asset reads them only through the rwb-source-data contract, the contract declares no `v_ace_*` path and no `v_ace_*` property, and describes no ACE table read of rwb-asset | DP-05; ASM-4872; GAP-1750 |
| BR4 | The case move is answered and not written: the contract declares the state read and the answer, and no `recovery_case` property and no case row write | Ownership Map (`recovery_case` owner P3); ASM-4877 |
| BR5 | The broker instruction is rwb-partner's: the contract declares it as the `Partner.issueInstruction` activity of S9, and no `partner_instruction` property, partner row or grant on `rwb_partner` | Architecture v5 slides 19 and 24; Ownership Map (`partner_instruction`, `partner` owner S9) |
| BR6 | The template and its price are rwb-comms' and the auto-debit and the money are rwb-payment's: both are declared as consumed and faked, never as provided | Ownership Map (`template` owner P6, `proceeds` owner P8); GAP-2967 |
| BR7 | The package in force and the approval answer are rwb-decision's: the contract declares the package version and the approval reference as consumed elements and no rule row and no approval row | Ownership Map (`approval`, `rule_row` owner P7); GAP-1944 |
| BR8 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; TSD S5 T-A.2 |
| BR9 | The vocabulary is closed: `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING` and `LOV-ASSET-TYPE` are published as enumerated values and no list value is a constant of the code; the lists are read through the reference-data contract of DP-06 and DP-07, and the parameters read are Not specified in the source documents (DOR-RWB-S5-E4034-CON-20) | TSD S5 T3.2; FSD S5 BR-S5-025 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Template and Rules v1 §R7.2 (s17) |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes |
| BR13 | The document lists only operations owned by rwb-asset; a consumed operation or activity is described as consumed and faked, never as provided | Ownership Map; DP-11; Architecture v5 slide 24 |
| BR14 | No event is declared as published or consumed by this step; `AssetTakenOn` and `AssetSold` are named as other stories' and the module list that omits `AssetSold` is recorded | Architecture v5 slides 19 OUT and 43; TSD S5 T5.3; GAP-1942 |

### 9. State transitions

The lifecycle of this document, not of a listing:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The reads, the listing and round elements, the instruction element, the five consumed rows, the rights, the error envelope and the seven fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 3 harness and the five owner teams accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new filter, an optional listing property or a new optional consumed field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes, or a path parameter changes its meaning | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC3, AC4 and AC7 fail: a `v_ace_*` view, a foreign row, a published event, a consumed event, a second topic or a Schedule | In review |
| Draft, In review, Baselined | No approval is recorded for the baseline | The run continues under D-RCV-60 with the baseline in Draft (GAP-2971; ASM-4876) | Draft, used under an assumption |

The listing-status machine the document describes is the app story's: `LOV-LISTING` is DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN, and this baseline fixes the vocabulary and the value the create writes and moves no listing. The legacy SCR-23 states do not map one to one onto those values, and the mapping is recorded (ASM-4878). The case route states the consumed rows name are rwb-case's and are fixed by its own contract.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document, the AsyncAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, the path form and the correction of the Ownership Map rows the baseline consumes, including the missing `asset` row |
| Consuming teams (the app story, the two screens, the wave 3 harness and the owners of rwb-case, rwb-partner, rwb-comms, rwb-payment and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library and the Temporal client and codec the instruction reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake, including the instruction element |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

Each REST operation of this baseline is guarded by the rwb-access authorise check under DP-08; the role codes that check tests are Not specified in the source documents (DOR-RWB-S5-E4034-CON-6).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Listing element | The columns of DF-SAL-001 to DF-SAL-008: `id`, `asset_code`, `sale_channel`, `start_price`, `floor_price`, `round_no`, `listed_at` and `status` | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Fee and terms properties | The fee, its basis and currency, the instruction term and the terms reference, declared additively and optionally on the listing or the sale element; their names, types and required flags are Not specified in the source documents (GAP-2967; ASM-4870). The fee and terms are read as route data with their version; the DB story of this service adds the additive fee and terms columns under DP-15, and no business value is written here (GAP-1937; GAP-2967) | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Required flags | `id`, `asset_code`, `sale_channel`, `start_price`, `floor_price`, `round_no` and `status` required; `listed_at` and the fee and terms optional | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Lists | `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING` and `LOV-ASSET-TYPE`, published as enumerations and read as reference data at their version | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Round element | `AuctionRoundRequest` in and `AssetSale` out for API-S5-005, declared as the auction stories' behaviour | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Instruction element | The instruction type, the partner reference, the asset and listing references and the fee and term references in, and the instruction reference and the issued-at time out, with the placeholder for every field no source names (GAP-2967; ASM-4870). Declared as the Partner.issueInstruction activity of S9 with an additive request and answer element and a placeholder property list (GAP-1937; GAP-2967) | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the listing row changes (DP-03) | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Consumed owner rows | The rwb-case state and move, the rwb-comms template and price, the rwb-payment auto-debit and the rwb-decision package version and approval answer, each declared as consumed and faked (GAP-1944; ASM-4874). The operation names and shapes of the case-move answer, the template read, the auto-debit request and the package read are placeholders, as no source states them (GAP-1937; GAP-2967). The DISPOSAL package is fetched at its version in force at the start of the step, held for the evaluation, and its package code and version are written to the decision record (GAP-1944) | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| ACE sale fact | DF-ACE-220 to DF-ACE-230 of `v_ace_npa_sale` in P1, read only through the owner's contract and never written, copied or joined here | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |
| Not declared here | `recovery_case` and `task` (P3), `document` (P5), `template` and `notice` (P6), `proceeds` (P8), `decision_log_entry`, `rule_row` and `approval` (P7), `partner_instruction` and `partner` (S9) | Not specified in the source documents (DOR-RWB-S5-E4034-CON-7) |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2, the path form of AC5 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story (ASM-4879).

The disposal rules are read as versioned data rows with the package version recorded on every decision. The rule texts the FSD states are the requirement; the package code, the remaining rules and the state list are left to the rule package in rwb-decision (GAP-1761; GAP-1944).

The broker route is R-DIS-26, to BROKER_INSTRUCTED. The broker-route rules named in the register are R-DIS-24, R-DIS-25, R-DIS-26, R-DIS-64 and R-DIS-65; their rule text is carried in Business Rules and Routing Logic v4 and is not repeated here. R-DIS-24 and R-DIS-25 are the legacy criteria kept on this story; the rental build is RWB-S5-E4033-APP's on the same step, and the rule owner confirms the step boundary of the three routes (GAP-1938; GAP-2968).

The listing path is the business-key form that API Specification v3 and v4 carry, and API-S5-005 stays on the listing identifier. The Ownership Map rows for GET /assets/{assetId} and POST /assets/{assetId}/listings and the TSD S5 endpoint inventory are corrected as documentation acts, not as a second contract (GAP-1941).

The legacy screen states SCR-23 are carried as the business conditions of the approval and the listing status of LOV-LISTING. The legacy data and endpoint rows are read as corrected: no v_ace_* read, no case, rule, template or partner table, and the business-key asset paths (GAP-1940).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetKey}` | Asset of status 200 out, with title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |
| POST | `/assets/{assetKey}/listings` | `ListingRequest` in, `Approval` out of status 201 or 202, with a required `Idempotency-Key` (API-S5-004) | Asset and disposal, right C, scope applied | `Idempotency-Key` declared |
| POST | `/listings/{listingId}/rounds` | `AuctionRoundRequest` in, `AssetSale` out, with a required `Idempotency-Key` (API-S5-005) | Asset and disposal, right U, scope applied | `Idempotency-Key` declared |

The operations answer 400, 401, 403 with MSG-P4-002, 404, 409 for the state conflict TSD S5 T-A.1 gives the two POSTs, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of §14. The operation IDs are those of TSD S5 appendix T-A.1 and the paths are those of the target base, not the monolith form. The path parameter is the ACE asset business key that the later API versions carry, while the Ownership Map, TSD S5 T-A.1 and the legacy story carry the asset-id form; the difference is recorded and the business-key form is declared (GAP-2969; ASM-4872). `POST /assets/{assetId}/valuations` (API-S5-003) is rwb-valuation's and is not declared here. The round operation is declared because a listing opened by the broker route may run rounds under the channels that use them; its behaviour is the auction stories' and this baseline fixes its shape only.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state and the case reference the listing and the route carry; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2967; ASM-4870)) | `/api/recovery/case/v1` | P3 rwb-case | The move with the rule ID and its version; on the workflow boundary it is the stage outcome the parent applies; faked |
| The template read (operation name Not specified in the source documents (GAP-2967; ASM-4870)) | `/api/recovery/comms/v1` | P6 rwb-comms | The template code, its language, its version and the price; faked |
| The auto-debit request (operation name Not specified in the source documents (GAP-2967; ASM-4870)) | `/api/recovery/payment/v1` | P8 rwb-payment | The auto-debit set for the case against the rental terms; faked |
| The package in force (operation name Not specified in the source documents (GAP-1944; ASM-4874)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DISPOSAL package with its code and its version in force; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The case-move answer and the rwb-partner instruction are also elements on the Temporal boundary: the move is the stage outcome, and the instruction is the activity of 12.5.

#### 12.3 Events published

None. This step publishes no event, so the baseline declares no event element, no producer role and no outbox row for it. `AssetTakenOn` on `rwb.asset.events.v1` is the take-on story's and `AssetSold` is the sale story's (Architecture v5 slides 19 OUT and 43). TSD S5 T5.3 gives the module `AssetTakenOn` as its only published event and omits `AssetSold`, which the catalogue carries, and the baseline records the difference rather than declaring a second event (GAP-1942; ASM-4873).

#### 12.4 Events consumed

None. The step is started by the stage trigger the parent forwards and by the approval answer of the `ApprovalWorkflow` child, and the partner result arrives as the answer of the activity it calls, so no Kafka subscription belongs to it. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is the route approval; `PartnerResultSubmitted` on `rwb.partner.events.v1` is consumed by the tracking and sale stories of this service, not by this step. This baseline declares no consumer group, no subscription and no inbox, and the absence test of AC7 fails a build that adds one.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | The stage that hosts the route step; its inputs, signals and outcome for the parent are declared, not built; the workflow ID form and the start and duplicate-start rule are Not specified in the source documents (CG-ALL-10313) |
| `openBrokerRoute` | Activity, the one route step | `rwb-asset` | The case, the approved route and the asset in; the rule ID with its package version, the listing reference, the instruction reference and the case move out, with the record, the listing row and the holding change in one transaction |
| `Partner.issueInstruction` | Activity, S9's, called by this step | `rwb-partner` in namespace `rwb-recovery` | The instruction type, the partner reference, the asset and listing references and the fee and term references in, and the instruction reference and the issued-at time out; the property list is Not specified in the source documents (GAP-2967; ASM-4870) |
| `ApprovalWorkflow` | Child workflow of the workflow kit, P7's | `rwb-decision` in namespace `rwb-recovery` | The approval answer with its approval reference, declared as consumed and faked |

The names `AssetDisposalWorkflow`, `Partner.issueInstruction` and `ApprovalWorkflow` are the ones Architecture v5 slides 19 and 24 and the Temporal and Drools Design give; the name `openBrokerRoute` is a target design choice that no source fixes (ASM-4879). No workflow is registered by this story and no activity is built by it.

#### 12.6 Schedules

None. The step runs from the stage trigger and the approval answer; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to RWB-S5-E3026-APP, and the R-DIS-26 instruction timer is a timer of rwb-partner's instruction and of the workflow's own wait.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| listing | S5 (`rwb_asset`) | The offer of the asset, its channel, prices, round, listed date and status, plus the additive fee and terms properties; the table the listing element answers from |
| asset_sale | S5 (`rwb_asset`) | The sale row and the broker fee and terms the route agreed on its additive columns; the sale row itself is the sale story's |
| asset | S5 (`rwb_asset`) | The held asset and its holding status, read by the two asset reads |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated approval and the answer it holds |

`recovery_case` and `task` (P3), `proceeds` (P8), `document` (P5), `template` and `notice` (P6), `decision_log_entry`, `rule_row` and `approval` (P7), `partner_instruction` and `partner` (S9) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as consumed answers, rule versions or another story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The state read of case `RC-2026-000534` in `ROUTE_WITH_APPROVER` and in the states the moves produce; an accepted move and a refused move | AC4, AC5, AC6 |
| rwb-partner instruction fake | The instruction accepted with its reference and issued-at time; an instruction refused because the partner is not on the panel; no answer beyond 2 s; an unreadable answer | AC3, AC6 |
| rwb-comms template fake | The buy-back template at its version with its language and price; a version not in force | AC4, AC6 |
| rwb-payment auto-debit fake | The auto-debit set for case `RC-2026-000534` with its mandate reference; no answer beyond 2 s | AC4, AC6 |
| rwb-decision package and approval fake | The DISPOSAL package with its code and version in force, and the `ApprovalWorkflow` answer approved, refused and returned | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000534` | AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names and shapes of the case-move answer, the template read, the auto-debit request and the package read, and the property list of the instruction, are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2967, GAP-1944; ASM-4870, ASM-4874).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 5 consumed | The two reads and the two POSTs on `/api/recovery/asset/v1`; the case state read and move answer, the template read, the auto-debit request and the package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | This step owns no event; the record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 2 activities declared (one of them S9's) and 1 child workflow consumed | `AssetDisposalWorkflow`, `openBrokerRoute`, `Partner.issueInstruction` on `rwb-partner` and the `ApprovalWorkflow` answer; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no listing, no case, no instruction, no template, no debit and no package. What it publishes is one OpenAPI 3.1 document, one AsyncAPI fragment, one instruction element, nine contract tables and seven fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `Asset`, `AssetPage`, `ListingRequest`, `Listing` and `Approval` elements and the round elements of API-S5-005, the vocabulary of the four lists as published enumerations, the consumed-row README with its placeholders, the instruction element declared as the S9 activity, and the seven WireMock and Temporal activity mapping sets.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on another owner's schema, because rwb-asset holds none (ASM-4872). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-23, whose screen model is the edge contract's. DP-04 is not in the pattern set of this key, so the package is declared as a consumed row rather than as an embedded-package feed, and the absence is recorded (GAP-1944; ASM-4874).

**Dependencies the tables add and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list already carries, and it leaves out the package feed of DP-04 that the evaluated rules need. The five consumed rows and the instruction element are C dependencies in fact and not in the metadata row (GAP-2967, GAP-1944; ASM-4870, ASM-4874).

**Build steps**

1. Write the two reads and the two POSTs with the declared path form and validate the additive rule of AC1 in the pipeline.
2. Write the `Listing` element, its required flags, its two lists and the placeholder of the fee and terms properties of AC2, and the round element of API-S5-005.
3. Write the instruction element and its answer of AC3 as the S9 activity, with the placeholder property list and the no-grant boundary.
4. Record the rwb-case, rwb-comms, rwb-payment and rwb-decision rows of AC4 with their owners, budgets and placeholders.
5. Record the rights and the error envelope of AC5, including the path-form note.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the seven fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the contract tests of §16 pass, the fakes answer every consumed path and the drift test is green, the absence tests of AC3, AC4 and AC7 are green, and the app story, the two screens and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key; it names the floor and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set; it names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the listing row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five IDs are contract elements and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added. The refusal and the not-recorded messages of FSD S5 A2.25.4.3 are these same two IDs, and no separate FSD message is declared.

### 15. Screens and states

The contract serves SCR-21 Asset list in its loading and list states, with its empty, error and no access states Not specified in the source documents (CG-ALL-10317), and SCR-23 Listing and price in its draft, below-limit, approved and published states, with its empty, loading, error and no access states Not specified in the source documents (CG-ALL-10318), all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the asset, its holding status and its listing, rwb-case for the case and its route state, rwb-valuation for the valuation the floor is set against and rwb-partner for the instruction reference; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON.

The refusal, not-recorded and field-invalid states the app story shows read the messages of §14 on the same route. The legacy screen states are business conditions rather than `LOV-LISTING` values, so the vocabulary is fixed in AC2 and the mapping is recorded (ASM-4878). The legacy Data, Endpoints and Screen states rows are read as corrected: no `v_ace_*` read and no case, rule, template or partner row; the asset paths in the business-key form with the internal uuid kept internal; and the SCR-23 states as business conditions of the approval and the floor check over `LOV-LISTING`.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-034-01 | AC1, AC2 | Contract | The listing of asset `AST-2026-000534` for case `RC-2026-000534`; the contract half answers the two reads, the two POSTs, the `Listing` element and its lists |
| TC-E4-034-02 | AC2, AC4 | Contract | Case `RC-2026-000534` at `ROUTE_WITH_APPROVER` with the buy-back route; the contract half answers the template row, its placeholder and the approval answer shape |
| TC-E4-034-03 | AC2, AC4 | Contract | Case `RC-2026-000534` with the rental route; the contract half answers the auto-debit row, its placeholder and the rental terms properties |
| TC-E4-034-04 | AC6 | Contract | The record stub stopped and a malformed request; the contract half answers the MSG-P7-003 path and the 400 of the envelope |
| TC-E4-034-05 | AC5 | Contract | A role without the Asset and disposal right; the contract half answers the 403 with MSG-P4-002 and the rights of the four operations |
| TC-E4-034-06 | AC5, AC6 | Contract | RW-SALEOFF holds CRUA and RW-NPAMGR holds CRU; the contract half answers the rights, the idempotency rule and the absence tests |
| TC-S5-E4034-CON-01 | AC1 | Contract | The document validates; no operation, required property or list value of major version 1 is removed or renamed and every added element is additive |
| TC-S5-E4034-CON-02 | AC2, AC5 | Contract | The `Listing` element validates with its eight properties, its seven required flags, its two lists and the placeholder fee and terms; the round element validates and the path form is the declared one |
| TC-S5-E4034-CON-03 | AC3, AC7 | Contract | The instruction element validates as the S9 activity with its placeholder property list; the absence tests for a published event, a consumed event, a second topic, a Schedule and a foreign schema |
| TC-S5-E4034-CON-04 | AC4, AC6 | Contract | The five consumed rows and their placeholders; the seven fakes match the document and a drifted fake fails the build; the no-`v_ace_*` and no-foreign-row boundary |
| TC-S5-E4034-CON-05 | AC4 | Contract | The tables of section 12.7 with their owners; the boundary of the five owned tables with no foreign key to another owner's table (DP-01) |
| TC-S5-E4034-CON-06 | AC8 | Contract | The fourteen rules BR1 to BR14 each checked against the declared elements; a rule without a declared element fails the build |

The six legacy cases are the legacy cases of RWB-E4-034 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, and the business outcome of each is proved by RWB-S5-E4034-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The six new cases are `TC-S5-E4034-CON-01` to `-06`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the fee, its basis and currency, the instruction term, the template price, the start and floor prices, the lists and the rule rows stay route data, template data, reference data or the package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic, and the instruction element carries no person name, contact value or identity number.
- ACE data only through the owner's contract or `v_ace_*` views: the document declares no `v_ace_*` path, no `v_ace_*` property and no ACE table read of rwb-asset (BR3).
- The case stays with rwb-case, the broker with rwb-partner, the template with rwb-comms and the money with rwb-payment: the document declares no `recovery_case`, `partner_instruction`, `template`, `proceeds` or posting property and no foreign row write (BR4, BR5, BR6).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation or activity is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event, a consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule, the decision-record library, the Temporal client and the payload codec come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-010 | A transfer to the asset management company, a buy-back and a rental each follow a recorded approval, and BR-030 of the Epics 3 to 8 BRD adds the broker sale; the contract fixes the listing, the instruction and the consumed rows the recorded route is built on (Business Requirements Program v5; FSD S5 requirements served); the split plan carries no requirement id for this slice (GAP-2970; ASM-4875) | The `Listing` element, the listing create, the instruction element and the five consumed rows | TC-E4-034-01, TC-E4-034-02, TC-S5-E4034-CON-01, TC-S5-E4034-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout, and the typed Temporal interface on the owner's queue | The five consumed rows and the `Partner.issueInstruction` element with their budget and breaker | TC-S5-E4034-CON-03, TC-S5-E4034-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element of 12.7 and AC6 | TC-E4-034-04, TC-S5-E4034-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-034, disposition Split (rework) |
| Legacy criteria | AC1 to AC4, owned word for word by RWB-S5-E4034-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new cases TC-S5-E4034-CON-01 to -04 |
| Feature and screens | FEAT-AST-25, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-24, R-DIS-25 and R-DIS-26, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-020, ADR-022 |

### 19. Out of scope

- The behaviour behind the reads and the listing create, the evaluation of R-DIS-24, R-DIS-25 and R-DIS-26, the record, the listing row, the holding change, the instruction and the case-move answer: RWB-S5-E4034-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked (BR4).
- The broker, its panel, its users, its instruction and result rows and the partner gateway: rwb-partner (S9) (BR5).
- The template, its text, its merge fields and its price: rwb-comms (P6) (BR6).
- The auto-debit, the rent charge, the fee posting and the proceeds: rwb-payment (P8), with the rental terms themselves built by RWB-S5-E4033-APP.
- The approval path and the package: rwb-decision (P7), whose approval and rule rows this baseline declares as consumed and faked (BR7).
- The ACE NPA sale and asset facts and the freshness of the data product: rwb-source-data (P1).
- The sale, the proceeds application and the `AssetSold` event: the sale and proceeds stories of this service (GAP-1942).
- The publishing of the listing, the floor approval and the price ladder: FEAT-AST-11 and FEAT-AST-12's stories and the behaviour of API-S5-005's rounds, whose shape alone is declared here.
- The valuations of the asset: rwb-valuation (S1) under API-S5-003.
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
