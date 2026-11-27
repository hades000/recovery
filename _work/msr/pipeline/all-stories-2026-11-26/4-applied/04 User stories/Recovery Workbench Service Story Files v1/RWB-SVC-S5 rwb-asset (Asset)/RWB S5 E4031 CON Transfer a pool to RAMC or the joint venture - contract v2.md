# RWB-S5-E4031-CON Transfer a pool to RAMC or the joint venture - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S5-E4031-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-asset |
| Service epic | RWB-SVC-S5 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-031 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S5 rwb-asset v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of the RAMC and joint venture transfer step of rwb-asset, split from RWB-E4-031. It fixes the two asset reads on `/api/recovery/asset/v1` that answer SCR-21 and PRT-06 (DP-13), the `AssetSale` and `Listing` elements with their closed lists, the transfer and instruction elements, the four consumed rows (rwb-case state and case-move answer, rwb-decision approval, rwb-source-data asset and sale facts), the decision-record element of DP-03, the fakes, the rights, the error envelope and the absence tests. No source gives the pool reference, the transfer-price element or its template version, the approval reference, the instruction element names, the acceptance and refusal codes or the case-move operation name (GAP-2954; ASM-4852); no source names an operation of this step and the legacy endpoints name other steps' operations (GAP-2955; ASM-4851); the consumed rows have no published operation names (GAP-2959; ASM-4852); `asset` is read as S5 (GAP-2957; ASM-4854); the plan carries no requirement id (GAP-2956; ASM-4855); the sources are in review and no approval exists (GAP-2958; ASM-4802). The baseline declares no event, no Schedule and no table, operation or topic of another owner (DP-05, DP-14). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S5-E4031-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the RAMC and joint venture transfer step of rwb-asset - the two asset reads, the sale and listing elements with their closed lists, the instruction element, the four consumed rows, the decision-record element, the rights, the error envelope and the fakes - baselined and tagged before the build starts**, so that **the application story, the two screens, the partner service and the wave 3 harness build and test on Day 1 against one fixed, versioned surface instead of guessing the shape of a neighbour's answer, and a field, a list value, an approval reference or a case move can never drift between rwb-asset, rwb-case, rwb-decision, rwb-partner and rwb-source-data without a failing build**.

This is the contract slice of legacy RWB-E4-031. It owns:

- the document that fixes the two reads of the asset and its transfer on base `/api/recovery/asset/v1`, with their parameters, their answer, their rights and their idempotency (DP-13);
- the `AssetSale` and `Listing` elements with the columns of DF-SAL-001 to DF-SAL-019 and the closed lists `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING` and `LOV-SEGMENT`;
- the transfer element: the pool, the transfer price with its template version, the fee and the taxes, the approval reference and the instruction reference, each with the placeholder where no name is published;
- the instruction element of the partner call and its answer (DP-11 call type of the matrix, actually a Temporal child call);
- the four consumed rows — the rwb-case state read and case-move answer, the rwb-decision approval, the rwb-source-data data product — each with its owner, its use and the placeholder where the name is not published (DP-05);
- the decision-record element of DP-03 and the library dependency that carries it;
- the capability area, the rights and the error envelope of the operations it declares;
- the fakes and their documented answers, so every consumed answer has a stub on Day 1;
- the naming and the boundary: one base, one topic, one queue, one login, no foreign schema, no monolith base, no Schedule and no event of this step.

It does not own: the behaviour behind the reads, the rule evaluation, the record write, the `asset_sale` rows, the instruction call and the case-move answer, which are RWB-S5-E4031-APP; the committee approval, its workflow and its answer, which are rwb-decision's (P7); the partner instruction, its portal and its codes, which are rwb-partner's (S9); the case of record and its route states, which are rwb-case's (P3); the party and NPA asset and sale facts, which are rwb-source-data's (P1); the governed template the price comes from, which is rwb-comms's (P6); the posting and the money, which are rwb-payment's (P8); and the screen field list and the composite route, which are RWB-PLT-N001-CON (DP-19).

### 2. Business rationale

A contract baseline is what lets six teams build at once. The transfer of the legacy key crossed an officer screen, a committee approval, a partner portal and a case state in one process. In the target it crosses five boundaries, each owned by another service, so each has to be fixed before the application story starts: the asset, listing and sale elements of `rwb-asset`; the vocabulary of the lists; the case state and the case-move answer; the approval child workflow and its answer; the partner instruction element; and the decision record.

The baseline also fixes the naming the checks require: schema `rwb_asset`, base `/api/recovery/asset/v1`, topic `rwb.asset.events.v1` with its retry and `.dlt` topics, task queue `rwb-asset` in namespace `rwb-recovery` and package `th.co.scb.ace.workbench.recovery.asset`. It records that rwb-asset holds no `v_ace_*` grant and no grant on `rwb_case`, `rwb_decision` or `rwb_partner`, so DP-05 is declared as a prohibition and the asset facts are consumed on the owner's contract only.

Two points are carried as gaps and assumptions rather than decided quietly. No source gives the pool reference, the transfer price element, its template version, the approval reference, the instruction element names or the acceptance and refusal codes, so the baseline declares them with a placeholder and never as a business value (GAP-2954; ASM-4852). The consumed rows have no published operation names and the legacy endpoints name the operations of other steps, so the baseline declares no provided operation for the transfer and carries the placeholder on every consumed row (GAP-2955, GAP-2959; ASM-4851, ASM-4852).

**What the baseline does not do.** It states no business outcome and fixes no business value: the transfer price, the fee, the tax treatment, the approval limit and the timer are values of their owners, read at their version.

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline; where this document narrows them it does so explicitly.
- Ownership is taken from the Ownership Map only: `listing` and `asset_sale` are S5's, `recovery_case`, `assignment` and `task` are P3's, `approval`, `decision_log_entry` and `rule_row` are P7's, `partner` and `partner_instruction` are S9's, `template` is P6's, `proceeds` is P8's, `document` is P5's, and every `v_ace_*` view is P1's. `asset` is absent from the map and is read as S5 from Architecture v5 slides 19 and 41 and TSD S5 T3.1 (GAP-2957; ASM-4854).
- The rwb-case rows, the rwb-decision approval and the rwb-source-data product are published by their owners with fakes, so each consumed row names a real owner document; their operation names are Not specified in the source documents (GAP-2959; ASM-4852), and they are not in this story's contract-dependency row, which is None.
- The DISPOSAL rule package and its row R-DIS-59 are governed in rwb-decision; this baseline names the row and declares none of it.
- The `asset`, `listing` and `asset_sale` tables and their columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- No approval is needed to publish a Draft baseline, and the missing approval of the realigned stories is recorded (GAP-2958; ASM-4802); the baseline is tagged when its contract tests pass and the consumers sign it off (§9).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-asset for this step: the two reads with their request and answer elements, the filters, the rights and the error responses.
2. Fix the `AssetSale` and `Listing` elements and the transfer part of the asset answer: the pool, the transfer price with its template version, the fee and the taxes, the approval reference and the instruction reference, each against the list it is declared against.
3. Fix the closed vocabulary: `LOV-SALE-CHANNEL` (with the `RAMC` value of the pool), `LOV-LISTING`, `LOV-HOLDING` and `LOV-SEGMENT`, and record that the transfer state and the transfer channel have no value in the sources.
4. Fix the instruction element and its answer, with the Temporal child-call type of the matrix.
5. Fix the four consumed rows: the rwb-case state read, the case-move answer, the rwb-decision approval and the rwb-source-data product, each with its owner, its use and the placeholder where the name is not published.
6. Record the decision-record element of DP-03, written before the transfer rows change.
7. Record the naming baseline and the boundary: one base, one topic, one queue, one login, no foreign schema, no monolith base, no Schedule and no event.
8. Publish the contract tables of section 12 and the fakes of 12.8.
9. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shapes, the rights, the envelope, and the absence of a `v_ace_*` read, of a `recovery_case` write and of an event.
10. Tag the baseline and hand it to RWB-S5-E4031-APP, the two screens, rwb-partner and the wave 3 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response or request body fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC5 |
| X2 | A field is renamed or removed within major version 1, or a required element is added | The contract test fails; the change needs a new major version | None | AC1 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list or an operation name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the owner document | None | AC3, AC4 |
| X5 | A value outside a closed list appears in the document, an example or a fake | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares another service's operation as provided, a `v_ace_*` view, a `recovery_case` row or an approval answer | The review fails the baseline; the boundary test fails the build | None | AC7 |
| X7 | The document declares an event, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | The rights of an operation are not the ones TSD S5 T-A.1 and T6.1 declare | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner documents of rwb-case, rwb-decision, rwb-partner and rwb-source-data only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the reads, the lists, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S5-E4031-APP, the two screens, rwb-partner and the wave 3 harness on Day 1 |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the RAMC and joint venture transfer step of rwb-asset

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of listing and asset_sale is S5, of recovery_case and task is P3, of approval is P7, of partner is S9, of template is P6 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The document validates and the two reads keep the additive rule (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-asset is published with this change
    When it is validated against the OpenAPI 3.1 schema and compared with the previous major version
    Then it validates with no error
    Then it declares GET /assets with an AssetPage answer of status 200 and GET /assets/{assetId} with an Asset answer of status 200, both under the base /api/recovery/asset/v1 and owned by rwb-asset
    Then the list declares the filters type, status, region, page and size, and the single read declares the path parameter assetId
    Then no property is removed or renamed, no type changes and no new required property appears within major version 1
    Then a removal, a rename, a type change or a new required property is refused as a minor change and requires a new major version

  Scenario: AC2 The sale, listing and transfer elements and their closed lists are fixed (new, D-RCV-60)
    Given the asset, listing and transfer sections of the baseline
    When they are compared with TSD S5 T3.1 and T3.2 and with the closed lists of the service
    Then AssetSale declares the eleven columns of DF-SAL-009 to DF-SAL-019 and Listing the eight columns of DF-SAL-001 to DF-SAL-008 with their required flags and types
    Then the transfer element declares the pool reference, the transfer price with the template version it was read at, the transfer fee, the two taxes, the approval reference and the instruction reference
    Then every amount is declared as a value of a reference or of a template row and never as an example constant
    Then sale_channel is declared against LOV-SALE-CHANNEL with DUTCH_AUCTION, BROKER, DIRECT, LED_AUCTION and RAMC, listing status against LOV-LISTING with DRAFT, LIVE, UNDER_OFFER, SOLD and WITHDRAWN, holding status against LOV-HOLDING with HELD, LISTED, UNDER_OFFER, SOLD, TRANSFERRED and RENTED, and the segment against LOV-SEGMENT with RETAIL, SSME and CORPORATE
    Then no value is added to any list by this document
    Then the transfer state value and the transfer channel value are Not specified in the source documents (GAP-2954; ASM-4852) and the element carries the placeholder
    Then no personal data property is declared: the partner is a party key and no name, address, contact value or identity number appears

  Scenario: AC3 The instruction element and its answer are declared with their placeholders (new, D-RCV-60)
    Given the instruction section of the baseline
    When it is compared with Architecture v5 slide 19 and the connection matrix
    Then the instruction is declared as a Temporal child call to rwb-partner on task queue rwb-partner, with the case reference, the pool reference, the partner, the transfer price with its template version and the approval reference
    Then its answer declares the instruction reference and the acceptance or refusal state
    Then the element names, the acceptance code and the refusal code are Not specified in the source documents (GAP-2954; ASM-4852) and each row carries the placeholder
    Then the document declares no partner path as provided and no partner, partner_instruction or fee property of its own, and the boundary test fails a build that adds one
    Then no commitment code or fee value is invented: both stay the owner's reference data

  Scenario: AC4 The rwb-case, rwb-decision and rwb-source-data rows are declared with their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with rwb-case as the owner of recovery_case, with rwb-decision as the owner of approval and with rwb-source-data as the owner of the ACE views
    Then the case state read is declared with the case reference and the route state, and the case-move answer with the move RAMC_TRANSFER_PENDING carrying the rule ID, its version, the pool and the instruction reference
    Then the approval is declared as consumed from P7 rwb-decision as the kit's approval child workflow, with the case, the route, the transfer price it is asked about and the answered or refused answer
    Then the asset and sale facts are declared as consumed from P1 rwb-source-data on the data-product contract, with the asset reference, type, segment, book value and the freshness stamp
    Then the operation names of the four rows are Not specified in the source documents (GAP-2959; ASM-4852) and each row carries the placeholder
    Then the document declares no recovery_case property, no case row write, no approval answer and no v_ace_* path as its own

  Scenario: AC5 The rights and the error envelope are fixed (new, D-RCV-60)
    Given the access and error sections of the baseline
    When they are compared with TSD S5 T-A.1, T6.1 and the platform envelope
    Then both reads declare Asset and disposal right R with the scope applied, and no operation of this baseline declares a right C, U or A
    Then RW-SALEOFF holds CRUA, RW-NPAMGR and RW-ENFORCE hold CRU, RW-PRODHEAD, RW-HEADNPA and RW-HEADASL hold RA, PT-RAMC holds RU and every other role of TSD S5 T6.1 holds R
    Then each read answers 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503 with one envelope and one message ID per condition
    Then neither read declares an Idempotency-Key, because neither changes anything
    Then a role outside the matrix is refused at the edge and the refusal is the same envelope

  Scenario: AC6 The decision-record element and the seven fakes answer the document (new, D-RCV-60)
    Given the decision section and the fakes of the baseline
    When each is compared with the library schema and with the operation or the element it serves
    Then one decision record is declared per rule outcome with the case reference, the pool reference, the rule ID, the package version in force, the inputs reference, the outcome, the case move and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before the transfer rows change, and a failed write leaves them unchanged with MSG-P7-003
    Then the rwb-case fake answers the states ROUTE_APPROVED_RAMC and ROUTE_APPROVED of case "RC-2026-000512", an accepted move and a refused move
    Then the rwb-partner fake answers the instruction of pool "POOL-2026-000512" accepted with its reference "INS-2026-000512", a refusal with its code and no answer beyond the retry policy
    Then the rwb-decision fake answers the approval answered and refused and the package with R-DIS-59, the rwb-source-data fake answers the asset and sale facts with a fresh and a stale stamp, and the decision-record stub answers a healthy chain and a stopped chain
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming and the boundary are fixed and nothing is published (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_asset, the login is rwb_asset, the topic is rwb.asset.events.v1, the queue is rwb-asset and the package is th.co.scb.ace.workbench.recovery.asset
    Then the tables named as owned are asset_sale, listing and asset, and the library objects decision_record and idempotency_key, and recovery_case, task, approval, decision_log_entry, rule_row, partner, partner_instruction, template, proceeds and document and every v_ace_* view are named as other owners' and consumed only through their contracts
    Then the document declares no event published by this step, no event consumed, no second topic, no consumer group and no Schedule, and the absence test fails a build that adds one
    Then no operation of this service issues the transfer, because no source names one (GAP-2955; ASM-4851)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S5-E4031-APP, they fix no business value, and they copy no criterion of the legacy story, whose three criteria stay with the application story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The `asset_sale`, `listing` and `asset` shapes are rwb-asset's, and the contract declares their fields, lists and required flags on those elements only | Architecture v5 slide 41; Ownership Map; TSD S5 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before the transfer rows change, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S5 T2; legacy AC1 and AC3 |
| BR3 | The ACE asset and sale facts stay with rwb-source-data: the contract declares them as a consumed row and declares no `v_ace_*` path, property or grant | DP-05; Architecture v5 slides 29, 37 and 45; GAP-2959 |
| BR4 | The case move is answered and not written: the contract declares the state read and the answer, and no `recovery_case` property and no case row write | Ownership Map (`recovery_case` owner P3); GAP-2959 |
| BR5 | The instruction stays with rwb-partner: the contract declares it as a consumed child call and declares no partner path as provided, no partner row and no fee value | Architecture v5 slide 19; Ownership Map (`partner`, `partner_instruction` owner S9); GAP-2954 |
| BR6 | The approval stays with rwb-decision and the limit with rwb-access: the contract declares the approval child workflow as consumed and no approval answer or limit of its own | Ownership Map (`approval` owner P7); GAP-2959 |
| BR7 | Nothing is published by this step: no event, no second topic and no outbox element; `AssetTakenOn` and `AssetSold` are the service's only events | Architecture v5 slide 19 and slide 43 |
| BR8 | The vocabulary is closed: the four lists are published as enumerated values and no value is added by this document | TSD S5 T3.2; FSD S5 A2.22.3.1 BR-S5-022 |
| BR9 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR10 | No personal data in a schema, an example or a fake: identifiers, party keys, codes, amounts, dates and a rule version only | Architecture v5 slide 42 notes; Template and Rules v1 §R7.2 (s17) |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or operation as its own | DP-13, DP-14; Template and Rules §R4 |
| BR12 | The transfer price, the fee, the taxes and the timer are values of a template version or of a rule row in force, never a schema default, an example or an enumeration member of the code | R-DIS-59; TSD S5 T3.1; legacy Guardrails |

### 9. State transitions

The lifecycle of this document, not of an asset and not of a case:

| From | Event | To |
|---|---|---|
| Drafted | The OpenAPI document validates in the pipeline | In review |
| In review | Every consumer signs off and the drift test passes | Tagged |
| Tagged | A breaking change is required | A new major version is drafted |
| Tagged | The owner retires a field | The field is deprecated for one minor version before removal |

The case states `ROUTE_APPROVED_RAMC` and `RAMC_TRANSFER_PENDING` are declared as the vocabulary of the case read and the case-move answer and are owned by rwb-case (BR4). R-DIS-60 and the state `ASSET_TRANSFERRED` are named as the step after this one and are declared by no one here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-asset | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the reading of `asset` as S5 |
| Consuming teams (the app story, the two screens, rwb-partner, rwb-case, rwb-decision, rwb-source-data and the wave 3 harness) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme is named "the rwb-asset login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| AssetSale element | The columns of DF-SAL-009 to DF-SAL-019: `id`, `asset_id`, `listing_id`, `contract_date`, `sale_date`, `sale_price`, `transfer_fee`, `specific_business_tax`, `corporate_income_tax`, `gain_loss` and `incentive_amount` |
| Listing element | The columns of DF-SAL-001 to DF-SAL-008: `id`, `asset_id`, `sale_channel`, `start_price`, `floor_price`, `round_no`, `listed_at` and `status` |
| Transfer element | The pool reference, the transfer price with its template version, the fee, the two taxes, the approval reference and the instruction reference; the pool reference and the price element are Not specified in the source documents (GAP-2954; ASM-4852) |
| Lists | `LOV-SALE-CHANNEL`, `LOV-LISTING`, `LOV-HOLDING` and `LOV-SEGMENT`, published as enumerations and read as reference data at their version |
| Instruction element | The case reference, the pool reference, the partner, the transfer price with its template version and the approval reference; answer with the instruction reference and its acceptance or refusal; element and code names Not specified in the source documents (GAP-2954; ASM-4852) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the transfer rows change (DP-03) |
| ACE fact | The asset and sale facts of P1, read only through the owner's data product and never written, copied or joined here |
| Not declared here | `recovery_case`, `assignment` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `partner` and `partner_instruction` (S9), `template` (P6), `proceeds` (P8), `document` (P5) and every `v_ace_*` view (P1) |
| Consumed fields with no source | The operation names of the rwb-case read and move, the element names of the approval answer, the operation name of the rwb-source-data read and the acceptance and refusal codes of the instruction: Not specified in the source documents (GAP-2959; ASM-4852) |

The field-level types, lengths and required flags of the added references are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR9. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-asset (S5); base `/api/recovery/asset/v1` (DP-13). The two reads are the answers PRT-06 Transfer confirmation and SCR-21 Asset list consume through the gateway-bff composite route (DP-19).

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| GET | `/assets` | AssetPage out, filtered by type, status and region, paginated by page and size, each row carrying the sale channel and the transfer reference of the pool (API-S5-001) | Asset and disposal, right R, scope applied | Not declared |
| GET | `/assets/{assetId}` | Asset of status 200 out, with its title, condition, valuations, costs and its `asset_sale` references (API-S5-002) | Asset and disposal, right R, scope applied | Not declared |
| None | None for the transfer instruction | No operation of rwb-asset issues the transfer: Architecture v5 slide 19 names the partner activity and the Ownership Map gives `POST /cases/{caseId}/instructions` to S9, so the instruction is carried on the consumed side and in 12.5 (GAP-2955; ASM-4851) | None | None |

The two reads answer 400, 401, 403 with MSG-P4-002, 404, 422 with MSG-GEN-001 and 503, each with the error envelope and one message ID of section 14. The operation IDs are those of TSD S5 T-A.1 and the paths are those of the target base, not the monolith form. API-S5-003 `POST /assets/{assetId}/valuations` is rwb-valuation's under the Ownership Map ruling ASM-0043, and API-S5-004 and API-S5-005 belong to the pricing and auction stories of this service; none of the three is declared here.

#### 12.2 REST operations consumed

| Method | Path | Owner | Call type and use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | REST; the case state `ROUTE_APPROVED_RAMC`, the case reference, the account link and the route outcome with the transfer price and its template version; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-2959; ASM-4852)) | rwb-case (P3) | P3 rwb-case | REST or the stage outcome the parent applies; the move `RAMC_TRANSFER_PENDING` with the rule ID, its version, the pool and the instruction reference; faked |
| The approval answer (element names Not specified in the source documents (GAP-2959; ASM-4852)) | rwb-decision (P7) | P7 rwb-decision | Temporal child workflow `ApprovalWorkflow`; the approval reference, the approved route and the transfer price it approved; no REST approval operation is declared; faked |
| The asset and sale facts of the pool (operation name Not specified in the source documents (GAP-2959; ASM-4852)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | REST; the asset reference, type, segment, book value and the freshness stamp, read only; faked |

Every REST row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020), and the child call uses the platform activity retry policy. The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-2959 (ASM-4852).

#### 12.3 Events published

None. The topic `rwb.asset.events.v1` carries `AssetTakenOn` and `AssetSold` and neither is the RAMC or joint venture transfer. This baseline declares no outbox element, no event and no third catalogue row for the step, and the absence test of AC7 fails a build that adds one (BR7; ASM-4851).

#### 12.4 Events consumed

None. Architecture v5 slide 19 gives rwb-asset `JudgmentRecorded`, `AuctionResult` and `ProceedsMatched`, none of which is the approval, the transfer price or the case state, and `PartnerResultSubmitted` belongs to the step that closes the transfer under R-DIS-60. `TRANSFER_INSTRUCTED` reaches the step through the case router's subscription in rwb-case and the parent's signal, so this baseline declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `AssetDisposalWorkflow` | Workflow, one execution per case per stage, the child of `CaseWorkflow`, continues-as-new | `rwb-asset` in namespace `rwb-recovery` | The stage that hosts the transfer step; its input, signals and outcome for the parent are declared, not built |
| `transferToRamc` | Activity, the one transfer step | `rwb-asset` | The case, the pool and the route outcome in; the rule ID with its package version, the transfer rows, the instruction reference and the case move out |
| `issueInstruction` | Activity of rwb-partner (S9), consumed and called as a Temporal child call; the name is the one Architecture v5 slide 19 gives | `rwb-partner` | In: the case reference, the pool reference, the partner, the transfer price with its template version and the approval reference. Out: the instruction reference and the acceptance or refusal. Element and code names Not specified in the source documents (GAP-2954; ASM-4852) |
| `ApprovalWorkflow` | Workflow of rwb-decision (P7), started by the route step under R-DIS-23, declared here as the source of the approval answer | `rwb-decision` | The approval reference, the approved route and the transfer price it approved; no REST approval operation is declared (GAP-2959; ASM-4852) |

No child workflow for the case and none for the money exists in this service, and no activity is registered by this story. The step activity name is a target design choice and the trigger is read as the case event `TRANSFER_INSTRUCTED` forwarded by the parent, because the FSD declares no background event for the feature (FSD S5 A2.22.4.4).

#### 12.6 Schedules

None. The step runs from the case event and from the signals the parent forwards; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. The R-DIS-59 timer cell "per agreement" is a governed timer specification of the rule row and is named in section 8 of the app story, not declared as a Schedule here (GAP-2954; ASM-4856).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| asset_sale | S5 (`rwb_asset`) | The transfer record of the pool, its fields, its lists and its required flags; one of the two tables the reads answer from |
| listing | S5 (`rwb_asset`) | The listing the pool is offered through, its sale channel and its status vocabulary |
| asset | S5 (`rwb_asset`) | The assets of the pool, their type, segment and book value, as the reads answer them, on the same reading as the take-on baseline (GAP-2957; ASM-4854) |
| decision_record | PLT library, created in `rwb_asset` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_asset` | The key of the repeated event and the answer it holds |

`recovery_case`, `assignment` and `timer` (P3), `decision_log_entry`, `rule_row` and `approval` (P7), `partner` and `partner_instruction` (S9), `template` (P6), `proceeds` (P8), `document` (P5) and every `v_ace_*` view (P1) are not owned here; the baseline names them only as answers, rule versions or another service's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | The states `ROUTE_APPROVED_RAMC` and `ROUTE_APPROVED` of case `RC-2026-000512` with the pool reference and the transfer price with its template version; an accepted move and a refused move | AC4, AC6 |
| rwb-partner instruction fake | An instruction of pool `POOL-2026-000512` accepted with its reference `INS-2026-000512`; a refusal with its code; no answer beyond the retry policy; an unreadable answer | AC3, AC6 |
| rwb-decision approval fake | The committee approval of the RAMC route for case `RC-2026-000512` with its approval reference and the transfer price it approved; an answer with an unstated element name | AC4, AC6 |
| rwb-decision rule-package fake | The DISPOSAL package at its version in force with R-DIS-59 and the timer specification of its row | AC6 |
| rwb-source-data data-product fake | The asset and sale facts of the pool with the freshness stamp, a stale product and no answer beyond 2 s | AC4, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC6 |
| gateway-bff composite route fake | The merged PRT-06 and SCR-21 answer for case `RC-2026-000512` | AC5, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The operation names of the rwb-case rows and of the rwb-source-data read, the element names of the approval answer and the codes of the instruction are derived from the published documents and carry the placeholder until their owners confirm them (GAP-2959; ASM-4852).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The two asset reads on `/api/recovery/asset/v1`; the rwb-case state read, the case-move answer and the rwb-source-data product read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this step; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow and 1 activity declared, 1 partner child call and 1 approval child workflow consumed, 0 registered | `AssetDisposalWorkflow` and `transferToRamc` on `rwb-asset`, `issueInstruction` on `rwb-partner` and the `ApprovalWorkflow` answer on `rwb-decision`; no Schedule |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no asset, no listing, no case and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables and seven fakes.

**Deliverables.** The additive document `openapi/rwb-asset-v1.yaml`, the `AssetSale`, `Listing` and `AssetPage` elements, the transfer element and the instruction element in the contract README, the vocabulary of the four lists as published enumerations, the contract README rows for the consumed rows and their placeholders, and the seven WireMock and activity-stub mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is declared as a prohibition here: the document declares no `v_ace_*` path, no `v_ace_*` property and no grant on another owner's schema, because rwb-asset holds none. DP-13 moves the base and nothing else. DP-19 is behind PRT-06 and SCR-21, whose screen models are the edge contract's. DP-09 is not in the pattern set of this key and is not needed, because the step publishes no event.

**Dependencies the table adds and the plan does not hold.** The pattern table adds the two H rows, `RWB-PLT-E1027-CON` for DP-03 and `RWB-PLT-N001-CON` for DP-19, which the plan's build list for this key carries, and the four consumed rows are C dependencies in fact and not in the metadata row (GAP-2959; ASM-4852).

**Build steps**

1. Write the two reads and validate the additive rule of AC1 in the pipeline.
2. Write the `AssetSale`, `Listing` and transfer elements, their required flags, the four lists and the references of AC2 with the placeholder where a name or a type is unstated.
3. Write the instruction element and its answer of AC3 with the placeholder and the partner-path prohibition test.
4. Record the consumed rwb-case, rwb-decision and rwb-source-data rows of AC4 with their owners, their call types, their budgets and their placeholders.
5. Record the rights and the error envelope of AC5.
6. Record the decision-record element of AC6 and validate it against the library schema.
7. Publish the seven fakes of AC6 and the drift test.
8. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The document validates in the pipeline, the contract tests of section 16 pass, the fakes answer every consumed path and the drift test is green, and the app story, the two screens, rwb-partner and the wave 3 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S5-001 | Carried from the legacy message set of this key. It names the floor percentage and the approval limit, which are the pricing story's, so no path of this step raises it | The floor is {pct} of fair market value, below the {limit} this level may approve. |
| MSG-S5-002 | Carried from the legacy message set of this key. It names the age of an appraisal, which is the re-appraisal story's, so no path of this step raises it | The appraisal is from {date}, more than a year ago. Order a new one before pricing. |
| MSG-GEN-001 | A required field of a request is absent or invalid, or a body fails schema validation (X1, VR-S5-022-1) | Enter {field}. |
| MSG-P4-002 | The role lacks the Asset and disposal right the operation declares (X8) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the transfer rows change | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The five message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is added. The refusal code and the refusal message of the partner instruction are S9's and are declared as a consumed element with the placeholder, not as a message of this service (GAP-2954; ASM-4852).

### 15. Screens and states

The contract serves PRT-06 Transfer confirmation in its pending and confirmed states and SCR-21 Asset list in its loading and list states, all through the gateway-bff composite route (DP-19). The route calls rwb-asset for the pool, its transfer record and its prices, rwb-case for the case and its route state, rwb-decision for the approval reference and rwb-partner for the instruction state; this baseline fixes the rwb-asset answers only, and the composite route specification and the screen field lists belong to RWB-PLT-N001-CON. PRT-06's confirmation surface is the partner portal's and is served with rwb-partner; no source names the service that owns its field list (GAP-2954; ASM-4852). The refusal, not-recorded and absent-price states the app story shows read the messages of section 14 on the same route.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-031-01 | AC2 | Contract | Case `RC-2026-000512` with pool `POOL-2026-000512` of two assets; the contract half answers the sale, listing and transfer elements, their required flags and their lists |
| TC-E4-031-02 | AC3, AC4 | Contract | The instruction element and its answer, the rwb-case move shape and the approval answer, with every placeholder carried |
| TC-E4-031-03 | AC1, AC6 | Contract | The document validates and the record element and the seven fakes answer it; a drifted fake fails the build |
| TC-E4-031-04 | AC5 | Contract | A role without the Asset and disposal right and a malformed request; the contract half answers 403 with MSG-P4-002 and 400 of the envelope |
| TC-E4-031-05 | AC1, AC6 | Contract | A stopped decision-record chain and a stale data product; the contract half answers the MSG-P7-003 path and the freshness rule |
| TC-S5-E4031-CON-01 | AC1 | Contract | The document validates; every added property is optional or a new path, and a renaming or a retyping fails the build |
| TC-S5-E4031-CON-02 | AC2 | Contract | The two elements validate with their nineteen properties, their required flags, the four closed lists and the declared references |
| TC-S5-E4031-CON-03 | AC3, AC4 | Contract | The instruction element, its answer and the four consumed rows validate against their owner documents and carry the placeholders where no name is published |
| TC-S5-E4031-CON-04 | AC5, AC7 | Contract | The rights and the error envelope of the two reads; the absence tests for a provided partner path, a foreign base, a `v_ace_*` property, a published event and a Schedule |

The five legacy cases are the legacy cases of RWB-E4-031 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S5-E4031-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four `TC-S5-E4031-CON-01` to `-04` cases are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the contract: the transfer price and the fee, the tax treatment, the timer specification, the four lists and the rule rows stay data, reference data, a governed template version or the rule package, never a schema default, an example or an enumeration member of the code.
- No personal data in a schema, an example or a fake: identifiers, codes, amounts, dates and a rule version only; every example is synthetic.
- ACE data only through the owner's contract: the document declares no `v_ace_*` path, no ACE table read and no ACE property of its own, and the pool's facts arrive on the rwb-source-data product (BR3).
- The case stays with rwb-case, the approval and the rule rows with rwb-decision, and the instruction with rwb-partner: the document declares no `recovery_case` property, no approval property, no partner path as provided and no partner row write (BR4, BR5, BR6).
- The money stays with rwb-payment: the document declares no posting, no balance and no proceeds property.
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own, or the monolith base, fails the review (DP-13, DP-14).
- The document lists only operations owned by rwb-asset; a consumed operation, activity or child workflow is described as consumed and faked, never as provided (DP-01, DP-11).
- No retired element is reintroduced and no event is declared: the absence tests fail a build that declares a published event, a consumed event of this step, a second topic, a Schedule, a Quartz row or a shared job table (BR7).

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| Not specified in the source documents (GAP-2956; ASM-4855) | The plan carries no requirement id for this slice and TSD S5 T8 names no requirement row for FEAT-AST-22; the contract fixes the fields, the instruction element and the consumed rows on which the legacy requirement RWB-E4-031 is built | The sale, listing and transfer elements, the instruction element and the four consumed rows | TC-E4-031-01, TC-E4-031-02, TC-S5-E4031-CON-01, TC-S5-E4031-CON-02 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The three consumed REST rows with their budget and breaker | TC-S5-E4031-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before the change | TC-E4-031-03, TC-S5-E4031-CON-03 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-031, disposition Split (rework) |
| Legacy criteria | AC1 to AC3 of the legacy story, owned word for word by RWB-S5-E4031-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S5-E4031-CON-01 to -04 |
| Feature and screens | FEAT-AST-22, PRT-06 Transfer confirmation and SCR-21 Asset list |
| Rules | R-DIS-59, governed in rwb-decision; R-DIS-23 and R-DIS-60 are the rows before and after this step and are declared by no one here |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the two reads, the evaluation of R-DIS-59, the decision record, the `asset_sale` rows, the partner instruction and the case-move answer: RWB-S5-E4031-APP.
- The committee approval, the `ApprovalWorkflow` child, the `approval` table and the four-eyes rule: rwb-decision (P7) (GAP-2959).
- The partner panel, the instruction, its portal, its result, its fee, its acceptance codes and the partner REST path: rwb-partner (S9) (GAP-2954).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3).
- The ACE asset and sale facts and the freshness of the data product: rwb-source-data (P1).
- The governed template the transfer price is produced from and the Calculation Service: rwb-comms (P6).
- R-DIS-60 and the posting of the transfer, the proceeds and any balance: the step that completes the transfer and rwb-payment (P8).
- The valuations of the asset: rwb-valuation (S1) under API-S5-003 and ASM-0043 (GAP-2955).
- The listing, the floor price and the auction rounds as operations: the pricing and auction stories of this service, API-S5-004 and API-S5-005.
- The authoring, testing, approval and versioning of the DISPOSAL package, of the R-DIS-59 row and of its timer specification: rwb-decision (P7).
- The gateway-bff composite route and the field lists of PRT-06 and SCR-21: RWB-PLT-N001-CON and the edge stories.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness, which copies none of these criteria.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
