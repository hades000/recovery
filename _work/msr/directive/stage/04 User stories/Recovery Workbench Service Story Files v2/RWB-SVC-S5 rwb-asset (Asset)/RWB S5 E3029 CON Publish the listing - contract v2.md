# RWB-S5-E3029-CON Publish the listing - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E3029-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E3-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S5-E3029-CON-16) |
| Contract version | API Specification v5, path /api/recovery/asset/v1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | rwb-integration (P2): consumed rows for the channel publication and the pause, with placeholders, until its owner contract is added: Not specified in the source documents (GAP-2886) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the listing publication of rwb-asset, split from RWB-E3-029. It fixes the publish operation and the asset read on `/api/recovery/asset/v1` (DP-13), the `Listing` element and its two closed lists, the channel set with the floor withheld, the consumed rwb-source-data, rwb-document, rwb-deviation, rwb-case and rwb-integration rows, the decision-record element of DP-03, the fakes and the absence tests. The listing row is absent from the legacy Data table, the channel set has no list value for HOME.SCB or the EASY app and no adapter owner, and the plan's C row is empty (GAP-2885, GAP-2886, GAP-2887; ASM-4781, ASM-4782, ASM-4783, ASM-4784). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S5-E3029-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (11 resolved, 18 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the listing publication of rwb-asset — the publish operation and the asset read on `/api/recovery/asset/v1`, the `Listing` element with its two closed lists and its channel set, the consumed rwb-source-data, rwb-document, rwb-deviation, rwb-case and rwb-integration rows, the decision-record element, the tables and the fakes**, so that **the app story, the two screens and the wave 2 harness build against one fixed, testable contract on Day 1 and a listing field, a channel value, a price, a schedule or an answer shape can never drift between rwb-asset, rwb-integration and rwb-case without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy publication of RWB-E3-029 crossed four boundaries at once: an officer screen, the ACE asset fact, the document evidence and three external channels. The target splits them: rwb-source-data owns the ACE asset fact and the title status, rwb-document owns the evidence, rwb-deviation owns the deviation codes, rwb-case owns the case and its route states, rwb-integration owns the channel adapters, and rwb-asset owns the listing record. Each boundary is now a contract that another team builds against, so each has to be fixed before the app story starts: the `listing` fields of the publication, the values of `LOV-SALE-CHANNEL` and `LOV-LISTING`, the channel set of the criterion, the publication payload with the floor withheld, the evidence and deviation facts, the case state and move of rwb-case and the record of the decision.

The baseline also fixes the naming that the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.asset` (Architecture v5 slide 19 notes). It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case` or `rwb_deviation`, so DP-05 is declared as a prohibition and every outside fact is consumed on the owner's contract only.

Three points are carried as gaps and assumptions rather than decided quietly: the `listing` row, the channel set, the price schedule and the pause marker have no legacy Data row and no list value (GAP-2885), the channel adapter of HOME.SCB, the EASY app and the auction portal has no owner contract in the plan and DP-16 is not in the pattern set (GAP-2886), and the module FSD and TSD extracts named by the work package are absent from the run's extract set, so the module facts are read from the data model, the physical schema, the feature specification and the rule set (GAP-2887).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case` and `timer` are P3's, `deviation` is S8's, `document` is P5's, `proceeds` is P8's, `notice` is P6's, `decision_log_entry` and `rule_row` are P7's. This document never declares another service's table or operation as its own.
- The consumed rows of rwb-source-data, rwb-document, rwb-deviation, rwb-case and rwb-integration are named with their owner, their budget and a placeholder where the source gives no operation name; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-2885, GAP-2886; ASM-4781, ASM-4782).
- The DISPOSAL rule package and its rule rows for R-DIS-33 and R-DIS-67 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- The `listing` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the publish operation and the asset read, with their request and answer elements, the filters, the rights and the error responses.
2. Fix the `Listing` element: the columns of DF-SAL-001 to DF-SAL-008, their types, their required flags and the list each of them is declared against.
3. Fix the channel set: the three channels the criterion names, the value each channel carries, the publication payload with the floor withheld and the pause command.
4. Fix the consumed rows: the source-data asset fact, the document set, the deviation codes, the case state read and the case-move answer, and the channel publication, marking the fields and operations the sources do not give with the placeholder.
5. Record the decision-record element of DP-03, written before the listing rows change.
6. Record the closed vocabulary of the two lists, the naming baseline and the rule that no value is a constant of the code.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the withheld floor, the absence of a `v_ace_*` read and of a `recovery_case` write, the drift between a fake and the document, and the absence of a published and of a consumed event.
9. Tag the baseline and hand it to RWB-S5-E3029-APP, the two screens and the wave 2 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body or a request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1 | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC4 |
| X5 | A value outside `LOV-SALE-CHANNEL` or `LOV-LISTING` appears in the document or in an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document carries a floor price in a channel payload, a `v_ace_*` path, a `recovery_case` property or another owner's operation | The review fails the baseline; the boundary and withheld-floor tests fail the build | None | AC3, AC7 |
| X7 | The document declares a published event, a consumed event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones the legacy permission table declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-source-data, rwb-document, rwb-deviation, rwb-case and rwb-integration only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the operations, the lists, the base, the topic, the queue and the channel set are fixed |
| Valuable | Unblocks RWB-S5-E3029-APP, the two screens and the wave 2 harness on Day 1, and the rwb-integration, rwb-document, rwb-deviation and rwb-case teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, nine fakes and five new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the listing publication of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case and timer is P3, of deviation is S8, of document is P5 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The publish operation and the asset read are declared on the asset base with their shapes and their errors (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares POST /assets/{assetId}/listings with the listing set of status 201 out and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then POST declares the request element of the publication and the header Idempotency-Key, and the repeat of a key returns the stored answer
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition
    Then every other property of the two operations is copied from the baseline of the asset reads and is not redefined here

  Scenario: AC2 The Listing element and its two closed lists are fixed (new, D-RCV-60)
    Given the listing section of the baseline
    When it is compared with the data model, the physical schema and the legacy criteria
    Then the Listing element declares the properties of DF-SAL-001 to DF-SAL-008: id, asset_key, sale_channel, start_price, floor_price, round_no, listed_at and status
    Then sale_channel is declared against LOV-SALE-CHANNEL with the values DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION and RAMC, and status against LOV-LISTING with the values DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN
    Then asset_key, sale_channel, start_price, floor_price and status are required and id, round_no and listed_at are answers of the service
    Then the element is answered once per published channel, and the price schedule is declared as a property of the publication request and of no table column
    Then no property is added for a photograph, an inspection report, a title status, a deviation code or a pause state, and those facts are referenced as the owners' facts

  Scenario: AC3 The three channels are declared and the floor is withheld (new, D-RCV-60)
    Given the channel section of the baseline
    When it is compared with the legacy criterion AC2 and the rule R-DIS-33
    Then the publication declares HOME.SCB, the EASY app and the auction portal as the three channels of one action, each with its own answer entry
    Then the publication payload carries the asset reference, the channel, the start price and the price schedule, and declares no floor price property and no floor value in any example
    Then the declared answer of each channel is accepted or refused, and a refused channel leaves the other two standing
    Then the mapping of HOME.SCB and the EASY app to a LOV-SALE-CHANNEL value is Not specified in the source documents (GAP-2885; ASM-4781) and is declared as a parameter of the publication
    Then the pause of R-DIS-67 is declared as a command of the same integration contract, with the listing references of the asset

  Scenario: AC4 The consumed owners' rows are declared and their facts stay with them (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the owner contracts and Architecture v5 slides 29, 37 and 45
    Then the asset fact and the title status are declared as consumed from P1 rwb-source-data, with the asset reference, asset key, asset type, segment, book value, title status and the freshness stamp
    Then the photograph count and the inspection report are declared as consumed from P5 rwb-document, and the open deviation codes as consumed from S8 rwb-deviation
    Then the operation name of each of the three rows is Not specified in the source documents (GAP-2885; ASM-4781) and each row carries the placeholder
    Then the document declares no v_ace_* path, no document property, no deviation property and no grant on any rwb_* schema of another owner, and the boundary test fails a build that adds one
    Then every call is one hop with a 2 s budget, a breaker and no retry of its own (DP-11, ADR-020)

  Scenario: AC5 The case rows, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the consumed rows and the access sections of the baseline
    When they are compared with rwb-case as the owner of recovery_case and with the legacy permission table
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the move LISTING_LIVE or DISPOSAL_PAUSED_DEVIATION carrying the rule ID and its version
    Then the operation name of the case-move answer is Not specified in the source documents (GAP-2885; ASM-4781) and the row carries the placeholder
    Then the document declares no recovery_case property, no route-state column and no write of a case row from rwb-asset
    Then POST declares Asset and disposal right C, held by RW-ENFORCE, RW-SALEOFF, RW-NPAMGR and SY-DATALOAD, and GET declares right R with the scope applied
    Then a repeated request with the same Idempotency-Key describes no second effect and stores its answer, and GET declares no header

  Scenario: AC6 The decision-record element and the nine fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the asset reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the listing rows change, and a failed write leaves the listing unchanged with MSG-P7-003
    Then the rwb-source-data fake answers the asset fact of "AST-2026-000512" with title status "clear" and with the title not clear, the rwb-document fake answers three photographs and the inspection report and its absences, and the rwb-deviation fake answers deviation "X4" open and no deviation
    Then the rwb-case fake answers the states FLOOR_APPROVED, LISTING_LIVE and DISPOSAL_PAUSED_DEVIATION, an accepted move and a refused move, and the rwb-integration fake answers each channel accepted or refused
    Then the rwb-decision fake answers the DISPOSAL package at its version with R-DIS-33 and R-DIS-67, and the decision-record stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and no event is published or consumed (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the Java package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are listing and the library objects decision_record and idempotency_key, and asset, asset_sale, recovery_case, timer, deviation, document, notice, proceeds, decision_log_entry, rule_row and every v_ace_* view are named as other owners'
    Then the document declares no published event, no consumed event, no second topic and no Schedule, and the absence test fails a build that adds one
    Then the document records that listing is absent from the legacy Data table of RWB-E3-029 and that its eight fields are read from the data model and the physical schema (GAP-2885; ASM-4781)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E3029-APP and they copy no criterion of the legacy story, whose four criteria stay with the app story word for word.

Scenario: AC8 Every rule BR1 to BR14 of section 8 is covered by a criterion, a test, or a guardrail or boundary test in section 16 (new, D-RCV-60)

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The listing record is rwb-asset's, and the contract declares its fields, its two lists and its required flags on the `Listing` element only; DF-SAL-001 to DF-SAL-008 are the record, and the channel mapping and the pause marker are reference data at their version | Architecture v5 slide 41; data model DF-SAL-001 to DF-SAL-008; physical schema `listing`; GAP-2885 |
| BR2 | The decision record is declared as an element written before the listing rows change, through the local library on the shared topic; a failed write changes nothing | DP-03; legacy RWB-E3-029 AC1 and AC4 |
| BR3 | The ACE asset fact and the title status stay with rwb-source-data: the contract declares the data-product read as consumed, declares no `v_ace_*` property and describes no ACE table read of rwb-asset | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2885 |
| BR4 | The case move is answered and not written: the contract declares the state read and the answer, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); GAP-2885 |
| BR5 | The three channels are declared once: HOME.SCB, the EASY app and the auction portal, published from one action, each with its own answer | Legacy RWB-E3-029 AC2; REQ-S5-005 |
| BR6 | The floor is never declared in a channel payload: the publication carries the start price and the schedule only, and a build or an example that carries the floor fails the withheld-floor test | Legacy RWB-E3-029 AC2, "with the floor not published" |
| BR7 | A POST declares the `Idempotency-Key` and stores its answer; a GET declares none | Architecture v5 slide 11; DP-11 |
| BR8 | The vocabulary is closed: `LOV-SALE-CHANNEL` and `LOV-LISTING` are published as enumerated values, and the channel mapping the lists do not give carries the placeholder | data model LOV rows; GAP-2885; ASM-4781 |
| BR9 | The evidence and the deviation are other owners' facts: the contract declares them as consumed rows and declares no property for a photograph, an inspection report, a title status or a deviation code | Ownership Map (document P5, deviation S8); GAP-2885 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR13 | The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided | Ownership Map; DP-11 |
| BR14 | The rule rows of R-DIS-33 and R-DIS-67 and the reference data of the evidence conditions and deviation codes are governed in rwb-decision and named here, never declared here | Business Rules and Routing Logic v4 |

### 9. State transitions

The lifecycle of this document, not of a listing:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the element, the two lists, the channels, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the two screens, the wave 2 harness and the rwb-source-data, rwb-document, rwb-deviation, rwb-case and rwb-integration owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example a new optional listing field or a channel parameter | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, a list value changes or a channel is added to the declared set | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence and withheld-floor tests of AC3 and AC7 fail: a floor in a payload, a `v_ace_*` view, a `recovery_case` property, a published event, a second topic or a Schedule | In review |

The listing-status machine that the document describes is the app story's: `LOV-LISTING` is DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN, and this baseline fixes the vocabulary and the publication value `LIVE` and moves no asset.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the absent `listing` row and the missing channel values |
| Consuming teams (the app story, the two screens, the wave 2 harness and the owners of rwb-source-data, rwb-document, rwb-deviation, rwb-case, rwb-integration and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-asset login (DP-02)" and is not part of this baseline.

The rwb-access authorise check (DP-08) guards every operation. Its operation path is Not specified in the source documents (DOR-RWB-S5-E3029-CON-6). The empty, error and no-access states of SCR-21 and the empty, loading, error and no-access states of SCR-23 are Not specified in the source documents (DOR-RWB-S5-E3029-CON-10).

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Listing element | The columns of DF-SAL-001 to DF-SAL-008: `id`, `asset_key`, `sale_channel`, `start_price`, `floor_price`, `round_no`, `listed_at` and `status` | BR1 |
| Required flags | `asset_key`, `sale_channel`, `start_price`, `floor_price` and `status` required; `id`, `round_no` and `listed_at` answered by the service | BR1 |
| Lists | `LOV-SALE-CHANNEL` (DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION, RAMC) and `LOV-LISTING` (DRAFT, LIVE, UNDER_OFFER, SOLD, WITHDRAWN), published as enumerations and read as reference data at their version. Parameters: Not specified in the source documents (DOR-RWB-S5-E3029-CON-20); reference-data contract DP-06 and DP-07 | BR8 |
| Channels | HOME.SCB, the EASY app and the auction portal, declared from the legacy criterion; the mapping of the first two to a list value is Not specified in the source documents (GAP-2885; ASM-4781) | BR5 |
| Publication payload | The asset reference, the channel, the start price, the price schedule and the listing period; no floor price (BR6) | BR6 |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the listing rows change (DP-03) | BR2 |
| ACE asset fact | DF-ACE-208 to DF-ACE-219 of `v_ace_npa_asset` in P1, read only through the owner's data product and never written, copied or joined here | BR3 |
| Deviation fact | DF-CAS-036 to DF-CAS-045 of `deviation` in S8, read only through the owner's contract | BR9 |
| Not declared here | `asset` and `asset_sale` (S5, other stories'), `recovery_case` and `timer` (P3), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7) | BR4 |
| Consumed rows with no source | The operation names of the five consumed owners' rows: Not specified in the source documents (GAP-2885, GAP-2886; ASM-4781, ASM-4782) | BR13 |

The field-level types, lengths and required flags of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/assets/{assetId}/listings` | A publish request in; the listing set out with one entry per channel, its prices, its schedule and its state, status 201 (API-S5-004) | Asset and disposal, right C, scope applied | `Idempotency-Key` required; the stored answer is returned on a repeat |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and listing references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |

The two operations answer 400, 401, 403 with MSG-P4-002, 404, 409 where the case is not in the expected state, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of the module API list and the paths are those of the target base, not the monolith form. API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's, and API-S5-005 `POST /listings/{listingId}/rounds` belongs to the descending-schedule story; neither is declared by this baseline.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The read of DP06 Collateral and assets (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The ACE asset fact and the title status of the case, with the freshness stamp; faked |
| The document-set read (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/document/v1` | P5 rwb-document | The photograph count and the presence of the inspection report of R-DIS-33; faked |
| The deviation read (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | `/api/recovery/deviation/v1` | S8 rwb-deviation | The open deviation codes (X1, X4, X5) of R-DIS-67; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case state, the case reference and the account link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2885; ASM-4781)) | rwb-case (P3) | P3 rwb-case | The move `LISTING_LIVE` or `DISPOSAL_PAUSED_DEVIATION` with the rule ID and its version; on the workflow boundary it is the stage outcome the parent `CaseWorkflow` applies; faked |
| The channel publication and pause (operation names Not specified in the source documents (GAP-2886; ASM-4782)) | `/api/recovery/integration/v1` | P2 rwb-integration | The publication of the start price and the schedule to HOME.SCB, the EASY app and the auction portal with the floor withheld, and the pause of R-DIS-67; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The six rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2885 and GAP-2886 with ASM-4781 and ASM-4782.

#### 12.3 Events published

None. Architecture v5 slide 19 OUT gives the topic `rwb.asset.events.v1` with `AssetTakenOn` and `AssetSold`, and neither belongs to this step: the take-on is RWB-S5-E3019-APP and the sale is the sale story of this service. The listing-live and the pause reach rwb-case on the case-move answer, so this baseline declares no published event, no outbox row and no AsyncAPI fragment of its own, and the absence test of AC7 fails a build that adds one.

#### 12.4 Events consumed

None. Architecture v5 slide 19 IN gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, and none of them is the listing evidence or the deviation; the evidence and the deviation are read on their owners' contracts and the case signal arrives on the parent `CaseWorkflow`. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` | The stage that hosts the publication and the pause; its signals and its outcome for the parent are declared, not built |
| `publishListing` | Activity, the publication step | `rwb-asset` | The case, the asset fact and the evidence in; the rule ID with its package version, the listing references per channel, the channel answers and the case move out |
| `pauseListing` | Activity, the pause command of R-DIS-67 | `rwb-asset` | The case, the deviation codes and the listing references in; the pause answer per channel, the pause marker and the case move out |

No child workflow for the case and none for the money exists in this service. The two activity names are target design choices and no source fixes them; no activity is registered by this story.

Workflow ID form and start rule of `AssetDisposalWorkflow`: Not specified in the source documents (CG-ALL-9941).

#### 12.6 Schedules

None. The publication runs from the evidence fact and the pause from the deviation fact; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table, and no Job of Architecture v5 slide 44 is owned or moved here. JOB-19 Re-appraisal monthly is the service's single Schedule and belongs to the re-appraisal story. The price schedule is a payload of the publication, not a Schedule of the service.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| listing | S5 (`rwb_asset`) | The published listing, one row per channel, its fields, its two lists and its status; the table the two reads answer from |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated fact and the channel answer it holds |

`asset` and `asset_sale` (S5, other stories'), `recovery_case` and `timer` (P3), `deviation` (S8), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or a later story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data data-product fake | The asset fact of `AST-2026-000512` for case `RC-2026-000512` with book value, segment `NPA` and title status `clear`; the same asset with the title not clear; a stale product; no answer beyond 2 s | AC4, AC6 |
| rwb-document document-set fake | Three photographs and the inspection report of case `RC-2026-000512`; no photograph; the report absent; no answer beyond 2 s | AC4, AC6 |
| rwb-deviation fake | Deviation `X4` open for case `RC-2026-000512`; a deviation `X2`; no deviation open; no answer beyond 2 s | AC4, AC6 |
| rwb-case state and move fake | The states `FLOOR_APPROVED`, `LISTING_LIVE` and `DISPOSAL_PAUSED_DEVIATION`; an accepted move and a refused move | AC5, AC6 |
| rwb-integration channel fake | HOME.SCB, the EASY app and the auction portal each accepting a publication; one channel refusing; a pause accepted; no answer beyond 2 s | AC3, AC6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-33 and R-DIS-67 | AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged SCR-21 and SCR-23 answer for case `RC-2026-000512` | AC1 |
| Ownership and vocabulary stub | The `listing` field list with its two LOVs, and the channel mapping with its placeholder | AC2, AC3 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the five consumed owners' rows are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2885, GAP-2886; ASM-4781, ASM-4782).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 6 consumed | The publish operation and the asset read on `/api/recovery/asset/v1`; the source-data, document, deviation, case-state, case-move and channel rows; one hop, 2 s |
| Kafka | 0 published, 0 consumed | The service topic carries `AssetTakenOn` and `AssetSold`, neither of which is this step's |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `AssetDisposalWorkflow`, `publishListing` and `pauseListing` on `rwb-asset`; no Schedule |
| File | None | No file is read, built or delivered here; the channel publication is a REST call |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no listing, no price, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and nine fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml` with the publish operation, the `Asset` and `ListingSet` elements and the `Listing` element, the vocabulary of the two lists as published enumerations, the channel set and the withheld-floor rule, the contract README rows for the consumed rows and their placeholders, and the nine WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on any other owner's schema, because rwb-asset holds none (Architecture v5 slides 29, 37 and 45; GAP-2885; ASM-4781). DP-13 moves the base and nothing else. DP-19 is behind SCR-21 and SCR-23, whose screen model is the edge contract's. DP-16, the integration adapter, is not in the pattern set of this key, which is why the channel publication is declared as a consumed contract of rwb-integration rather than as an adapter of this service (GAP-2886; ASM-4782).

**Dependencies the table adds and the plan does not hold.** The pattern table adds two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key already carries. The six consumed rows are C dependencies in fact and not in the metadata row (GAP-2885, GAP-2886; ASM-4781, ASM-4782).

**Build steps**

1. Write the two operations and validate the additive rule of AC1 in the pipeline.
2. Write the `Listing` element, its required flags and its two lists of AC2 with the placeholder where the channel mapping is unstated.
3. Write the channel set, the publication payload and the withheld-floor test of AC3, and the pause command.
4. Record the consumed rwb-source-data, rwb-document and rwb-deviation rows of AC4 with their owners, budgets and placeholders.
5. Record the rwb-case rows, the rights and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the nine fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the contract tests pass, the fakes answer every consumed path and the drift test is green, the withheld-floor and absence tests are green, and the app story, the two screens and the wave 2 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the listing rows change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy wording, copied unchanged; no message is reworded and no new one is added.

### 15. Screens and states

The contract serves SCR-23 Listing and price in its Draft, below-limit, approved and published states (empty, loading, error and no access: Not specified in the source documents (CG-ALL-9946)) and SCR-21 Asset list in its loading and list states (empty, error and no access: Not specified in the source documents (CG-ALL-9945)), all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the listing, its prices, its channel, its status and its schedule, rwb-case for the case and its route state, rwb-source-data for the asset fact and rwb-valuation for the valuation references; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refusal, not-recorded, channel-not-published and paused states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E3-029-01 | AC1, AC2 | Contract | The publication of asset `AST-2026-000512`; the contract half answers the publish operation, the `Listing` element and its two lists |
| TC-E3-029-02 | AC2, AC3 | Contract | Case `RC-2026-000512` at `FLOOR_APPROVED`; the contract half answers the three channels, the entry per channel and the absent floor in every payload and example |
| TC-E3-029-03 | AC3, AC5 | Contract | Case `RC-2026-000512` at `LISTING_LIVE` with deviation `X4`; the contract half answers the pause command and the `DISPOSAL_PAUSED_DEVIATION` move shape |
| TC-E3-029-04 | AC5, AC6 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers the 403 with MSG-P4-002 and the 400 of the envelope |
| TC-E3-029-05 | AC5 | Contract | RW-SALEOFF, RW-ENFORCE, RW-NPAMGR and SY-DATALOAD hold C; the contract half answers the rights of the two operations |
| TC-E3-029-06 | AC6, AC7 | Contract | The decision-record stub stopped and a drifted fake; the contract half answers the MSG-P7-003 path and the absence tests |
| TC-S5-E3029-CON-01 | AC1 | Contract | The document validates; the two operations, the base, the `Idempotency-Key` rule and the seven error answers are present |
| TC-S5-E3029-CON-02 | AC2 | Contract | The `Listing` element validates with its eight properties, its five required flags and the two closed lists |
| TC-S5-E3029-CON-03 | AC3 | Contract | The three channels and the entry per channel; the withheld-floor test fails a payload or an example that carries the floor |
| TC-S5-E3029-CON-04 | AC4, AC5, AC6, AC7 | Contract | The six consumed rows and their placeholders; the nine fakes match the document and a drifted fake fails the build; the no-`v_ace_*`, no-`recovery_case` and no-event boundary |
| TC-S5-E3029-CON-05 | BR1, BR2, BR3, BR4 | Contract | The boundary of the §12.7 tables: `listing`, `decision_record` and `idempotency_key` only; the not-owned names and every `v_ace_*` view absent; no foreign key leaves the schema; the decision record written before the listing rows |
| TC-S5-E3029-CON-06 | BR5, BR6, BR7, BR8, BR9, BR10, BR11, BR12, BR13, BR14 | Contract | The three channels and no floor in any payload; the `Idempotency-Key` on each POST and none on a GET; the closed lists; no personal data field; one base, topic, queue and login; an additive schema change; operations of rwb-asset only; no rule row declared |
| TC-S5-E3029-CON-07 | AC8 | Contract | Not specified in the source documents (NEWAC-RWB-S5-E3029-CON-AC8) |

The six legacy cases are the legacy cases of RWB-E3-029 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E3029-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S5-E3029-CON-01` to `-04` are new. The full test, with its Given, When and Then, is in the Recovery Workbench Test Cases workbook, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 2 harness.

### 17. Guardrails

- No business value in the contract: the evidence conditions, the deviation codes, the price steps, the lists and the rule rows stay data, reference data or the rule package, never a schema default or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- The ACE asset fact, the evidence and the deviation stay with their owners: the document declares no `v_ace_*` path, no `recovery_case` property, no document or deviation property and no row write of another owner (BR3, BR4, BR9).
- The floor is never declared in a channel payload, and the withheld-floor test fails a build or an example that carries it (BR6).
- The money stays with rwb-payment: the document declares no posting, no balance and no proceeds property.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced: the absence tests fail a build that declares a published event, a consumed event, a second topic, a Schedule, a Quartz row or a shared job table.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S5-005 | Listings are published to the bank's channel and the auction portal from one action; the contract fixes the element, the channel set and the consumed rows on which the publication is built (Business Requirements Program v5); the split plan carries no requirement id for this slice (GAP-2885; ASM-4781) | The `Listing` element, the channel set, the withheld-floor rule and the six consumed rows | TC-E3-029-01, TC-E3-029-02, TC-S5-E3029-CON-01, TC-S5-E3029-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The six consumed rows with their budget and breaker | TC-S5-E3029-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the change | TC-E3-029-06, TC-S5-E3029-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E3-029, disposition Split (rework) |
| Legacy criteria | AC1 to AC4 of the legacy story, owned word for word by RWB-S5-E3029-APP; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S5-E3029-CON-01 to -04 |
| Feature and screens | FEAT-AST-12, SCR-21 Asset list and SCR-23 Listing and price |
| Rules | R-DIS-33 and R-DIS-67, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the publish operation and the read, the evaluation of R-DIS-33 and R-DIS-67, the decision record, the `listing` rows, the channel publication, the pause and the case-move answer: RWB-S5-E3029-APP.
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The ACE NPA asset fact, the title status and the freshness of the data product: rwb-source-data (P1).
- The photograph set, the inspection report and their retention: rwb-document (P5).
- The deviation, its codes and its owner: rwb-deviation (S8).
- The channel adapters of HOME.SCB, the EASY app and the auction portal: rwb-integration (P2) (GAP-2886).
- The start price, the floor and their approval: FEAT-AST-11 and the pricing story of this service.
- The descending price schedule, the rounds and the re-listing: FEAT-AST-13, FEAT-AST-15 and FEAT-AST-17 and their stories, API-S5-005.
- The authoring, testing, approval and versioning of the DISPOSAL package and of the rule rows of R-DIS-33 and R-DIS-67: rwb-decision (P7).
- The gateway-bff composite route and the screen field list of SCR-21 and SCR-23: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 2 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
