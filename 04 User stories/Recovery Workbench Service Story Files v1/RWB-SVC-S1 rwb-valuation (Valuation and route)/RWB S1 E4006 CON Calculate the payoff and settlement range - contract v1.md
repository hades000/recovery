# RWB-S1-E4006-CON Calculate the payoff and settlement range - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S1-E4006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-valuation |
| Service epic | RWB-SVC-S1 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S1 rwb-valuation v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: the contract slice of RWB-E4-006, the baseline that the payoff and range calculation of rwb-valuation builds against on Day 1. The baseline fixes the calculation elements of `POST /cases/{caseId}/route` (API-S1-001) on `/api/recovery/valuation/v1` (DP-13) — the payoff, `payoff_as_at`, `settlement_range_low`, `settlement_range_high`, `floor_price`, the rule id and version and the calculation state — the five consumed rows of rwb-source-data, rwb-decision, rwb-case and rwb-access (DP-05), the decision-record element and the library that carries it (DP-03), the elements of `RouteDecisionWorkflow` and its two activities, the rights, the error envelope and the fakes; it publishes no event, because the ownership rows give S1 none. No source publishes the operation names of the consumed rows or the element name of the payoff amount (GAP-2616 and -6; ASM-4318 and -6), gives S1 a table for the payoff, the range or the floor (GAP-2615; ASM-4317) or fixes the freshness limit and the floor method (GAP-2618; ASM-4320). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead of rwb-valuation**, I want **the published contract baseline of the payoff and range calculation of rwb-valuation — its calculation elements in the route answer, its consumed rows, its decision-record element, its workflow elements, its rights, its error envelope and its fakes — fixed and tagged before the build starts**, so that **the application story, the wave 3 harness and the four owners it consumes can build and test on Day 1 against one versioned surface instead of guessing the shape of a neighbour's answer**.

This is the contract slice of legacy RWB-E4-006. It owns:

- the document that fixes the calculation elements of `POST /cases/{caseId}/route` (API-S1-001) on base `/api/recovery/valuation/v1`: `RouteRequest` in, `Approval` out, the payoff, `payoff_as_at`, `settlement_range_low`, `settlement_range_high`, `floor_price`, the rule id, the rule version and the calculation state as declared elements, the `Idempotency-Key` header, the rights and the error set (DP-13);
- the five consumed rows: the account and balance read and the freshness read of rwb-source-data, the rule-set-in-force and decision-log read of rwb-decision, the case and account-set read of rwb-case, and the authorise operation of rwb-access, each with its owner, its use and a placeholder where the name is not published (DP-05);
- the decision-record element, the library that carries it and the shared topic it reaches (DP-03);
- the elements of `RouteDecisionWorkflow` and its two activities on task queue `rwb-valuation`;
- the calculation elements of SCR-13 Route decision, one hop through the gateway-bff composite route (DP-19);
- the fakes and their documented answers;
- the naming and boundary rule of the baseline: one base, one topic, one queue, one login, no foreign schema, no monolith base, no balance copy.

It does not own: the calculation itself, its freshness gate, its exception handling and the screen behaviour, which are RWB-S1-E4006-APP; the recommendation and its reasons, which are FEAT-VAL-07; the approval and the case move, which are the route-decision submission slice of RWB-E4-005 and rwb-case (P3); the ACE balances and their batch date, which are rwb-source-data's (P1); the rule set, the range bounds, the floor and the central ledger, which are rwb-decision's (P7); the roles and scopes, which are rwb-access's (P4); the treatment record and the offer, which are rwb-treatment's (S2); the composite route and the screen field list, which are RWB-PLT-N001-CON; and the deployment, which is the operations story of this legacy key.

### 2. Business rationale

A contract baseline is what lets several teams start together. Legacy RWB-E4-006 asks for a payoff worked out from balances the Workbench does not own and a range the bank governs, recorded with its rule version before the route is chosen. That means the step reads two contracts and writes one record in a third, and without a tagged baseline each of those shapes would be discovered at the first integration instead of at the review.

The three rules the baseline applies:

- **the owner publishes, the consumer adapts.** Every consumed row names its owner, its use and its 2 s budget, and every row whose name is not published carries the placeholder and its gap (GAP-2616; ASM-4318).
- **one hop, one budget.** Each consumed row is a single hop with a 2 s timeout and a breaker; a balance is never read from a table of this service and never chained through a second service (DP-05, ADR-020).
- **additive only.** A new optional element is a minor version; a removal, a rename, a type change or a new required element is a major version and a new document (s9).

The business outcome the baseline protects is the one FEAT-VAL-06 and REQ-S1-004 of FSD S1 state: the payoff and the range are calculated by rule from current balances, with the floor applied. The baseline states no outcome and no business value of its own, and no criterion here asserts a particular payoff amount.

### 3. Preconditions

- The Ownership Map rows for S1 are in force: `POST /assets/{assetId}/valuations`, `POST /assets/{assetKey}/valuations` and `POST /cases/{caseId}/route`; no table, no event, no job, and one workflow, `RouteDecisionWorkflow`. The two valuation paths belong to the appraisal-intake baseline and are not declared here.
- The service naming is fixed: schema `rwb_valuation`, one login of its own, base `/api/recovery/valuation/v1`, topic `rwb.valuation.events.v1` with `.retry` and `.dlt`, task queue `rwb-valuation` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.valuation`.
- TSD S1 is the shape of record for the service: T-A.1 gives API-S1-001 with right Treatment and offer U; T-A.2 gives `RouteRequest` in, `Approval` out, errors 401, 403, 404, 409, 422 and 503 and the `Idempotency-Key`; T6.1 gives the capability area and its rights.
- The platform CON stories are published: RWB-PLT-E1027-CON for the decision record (DP-03) and RWB-PLT-N001-CON for the composite route (DP-19). A CON story has no build dependency (R5.7 rule 1), so both sit in the preconditions and not in the H row.
- The range bounds, the floor and the freshness limit are values of the settlement route set in force and are referenced with their identifier and version; no source publishes their numeric values and none is declared here (GAP-2618; ASM-4320).
- No approval is needed to publish a Draft baseline; the document is baselined by its own review and the build waits only for its tag (ASM-4323).

### 4. Flow

1. The author drafts the baseline from the Ownership Map rows of the context pack, TSD S1 T-A.1, T-A.2 and T6.1, the FSD S1 A2.6 rules and the DP table.
2. Every provided element is declared with its method, path, type, nullability, source, rights and error set.
3. Every consumed row is declared with its owner, its use, its budget and a placeholder where the name is not published.
4. The decision-record element is declared with the library of DP-03, the shared topic and the transaction it joins.
5. The workflow and its two activities are declared with their input, their signals and their outcome elements.
6. The closed lists are referenced with their identifier and their version and are never enumerated in code; the range bounds, the floor and the freshness limit are referenced with their rule id.
7. The fakes are declared with their documented answers, one per consumed row and one for the composite route.
8. The compatibility check runs on the draft against the previous tag: a breaking change fails it.
9. The document goes to review as Draft; the reviewers are the owners of the five consumed rows and the tech lead of the service.
10. On the review's close the document is tagged; the application story and the wave 3 harness start against the tag and the fakes, and the code never moves ahead of the document.

### 5. Exception paths

| ID | Trigger | What happens | Covered by |
|---|---|---|---|
| X1 | A consumer asks for a shape the sources do not publish | The element or row carries the placeholder and its gap; no name, value or path is invented | C3, C4 |
| X2 | A change removes, renames, retypes or newly requires an element | The compatibility check fails and the document needs a new major version | C1 |
| X3 | A declared element or operation reaches another service's data, base or table | The review refuses the baseline and the boundary test fails the build | C7 |
| X4 | A consumed row has no fake, or its fake has no documented answer | The baseline is not tagged and the application story cannot start | C6 |
| X5 | The rights of an operation are not a row of the access matrix | The operation is not declared and the error set stays incomplete | C5 |
| X6 | An owner changes its documented answer after the tag | The owner publishes a version, this document follows in a minor or major version, and the fake is updated | X2, s9 |
| X7 | Two documents claim the same base, topic, queue or element name | The owner named in the Ownership Map keeps it and the other document changes | C7 |

X1 to X3 are the paths of an incomplete source, X4 to X6 the paths of a baseline moving under a build, and X7 the naming boundary.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no build, no live service and no approval; starts on Day 1 and is finished before the application story's first line |
| Negotiable | The wording, the section order and the fake data are this story's choice; the operation, the request, the answer, the rights and the error set are fixed by TSD S1 |
| Valuable | Four teams build at once against one tagged surface, and the first integration finds behaviour, not shape |
| Estimable | One document, one provided operation with eight declared elements, five consumed rows, one decision-record element, one workflow with two activities, one screen subject and eight fakes |
| Small | Finished inside a week; the review is the only gate |
| Testable | Every criterion is a document check that runs in the contract test suite, plus the compatibility check on the published schema |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the payoff and range calculation

  Scenario: C1 The baseline validates and only additive changes pass (new, D-RCV-60)
    Given the published schema, the element list and the closed lists of the baseline
    When a change removes, renames, retypes or newly requires an element
    Then the compatibility check fails and the change needs a new major version
    And a change that adds an optional element passes as a minor version

  Scenario: C2 The calculation elements of the route answer are published as declared (new, D-RCV-60)
    Given the element table of the baseline
    When POST /cases/{caseId}/route on /api/recovery/valuation/v1 is read
    Then it names RouteRequest in, Approval out, the Idempotency-Key header and the scope rule of T-A.2
    And the answer declares the payoff, payoff_as_at, settlement_range_low, settlement_range_high, floor_price, the rule id, the rule version and the calculation state, each with its type, its nullability and its source

  Scenario: C3 The five consumed rows carry their owners, their budgets and their placeholders (new, D-RCV-60)
    Given the consumed operation table of the baseline
    When the rows of rwb-source-data, rwb-decision, rwb-case and rwb-access are read
    Then each row names its owner, its use, one hop and a 2 s budget
    And where the operation name is not published the row carries the placeholder and the gap identifier and no path

  Scenario: C4 The consumed rows are declared as reads and no balance or rule table is declared (new, D-RCV-60)
    Given the consumed table and the table-ownership table of the baseline
    When the balance, the freshness and the rule-set rows are read
    Then each is declared as a consumed read of its owner and never as a table of this service
    And no v_ace_* copy, no foreign schema, no payoff table and no foreign key is declared

  Scenario: C5 The rights and the error envelope are declared for the operation (new, D-RCV-60)
    Given the operation the baseline provides
    When the rights and the error set are read
    Then it names the capability area Treatment and offer and the right U of the access matrix
    And the error set names 400, 401, 403 with MSG-P4-002, 404, 409, 422 with MSG-GEN-001 and 503 in one problem envelope

  Scenario: C6 The decision-record element, the workflow elements and the fakes are declared (new, D-RCV-60)
    Given the baseline document
    When the decision-record element, the workflow table and the fake table are read
    Then the element names RWB-PLT-E1027-CON as its library, the shared topic and the transaction it joins
    And RouteDecisionWorkflow and its two activities name their input, their signals and their task queue
    And every consumed row has a fake with a documented answer, including the stopped decision-record stub

  Scenario: C7 The naming, the publication and the boundary of the baseline hold (new, D-RCV-60)
    Given the base, the topic, the queue, the schema and the outbox of the baseline
    When the document is checked against the naming rule, the ownership rows and the event list
    Then one base, one topic, one queue and one login are declared and no monolith base and no foreign topic appear
    And no event is published, because the ownership rows give S1 none, and no Schedule is declared
```

The seven criteria are new to this run and are tagged as such. They test the contract deliverable only: the schema, the elements, the lists, the consumed rows, the rights, the envelope, the decision-record element, the workflow, the fakes and the boundary. No criterion states a business outcome of the application story, and none asserts a payoff amount, a range value or a floor value.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One owner per operation, row, element and table: the baseline declares the route operation that the Ownership Map gives S1 and names every other row with its owner | Ownership Map rows of S1; TSD S1 T-A.1 |
| BR2 | A consumed row with no published operation name carries the placeholder and its gap and never an invented path, an invented parameter or an invented transport | Template and Rules v1 §R9; GAP-2616 |
| BR3 | The baseline is additive: a new optional element is a minor version, and a removal, a rename, a type change or a new required element is a major version | ADR-020; s9 |
| BR4 | Every consumed row is one hop with a 2 s timeout, a breaker and no chain; a balance arrives on the rwb-source-data data product or on this service's own SELECT-only view and is never copied | DP-05; ADR-020; D-RCV-35 U1 |
| BR5 | The range bounds, the floor and the freshness limit are referenced by rule id and version and are never declared as a literal, a default or a fixture value | BR-S1-006; R-SET-01, R-SET-03, R-SET-05 |
| BR6 | No event is published by this baseline: the ownership rows give S1 no event, and the decision record reaches the ledger on the shared topic through the library of DP-03 | DP-03; context pack S1 ownership rows |
| BR7 | The decision record is written through RWB-PLT-E1027-CON in the caller's transaction before the answer is composed, and its element is declared once for the service | DP-03 |
| BR8 | The baseline declares no payoff, range or floor table: the ownership rows give S1 no table and TSD S1 T3.1 declares only `valuation` and `score` | GAP-2615; ASM-4317 |
| BR9 | No personal data in any element, fake, example or log of the baseline | Template and Rules v1 §R7.2 (s17) |
| BR10 | The baseline never declares another service's table, operation or topic as its own, and a check fails the build where one names it | DP-01, DP-13, DP-14 |

### 9. State transitions

The object of this section is the document, not a case: the lifecycle of the contract baseline.

| From | Event | Condition | To |
|---|---|---|---|
| None | The draft is complete | Every element, row, fake and error is declared | Draft |
| Draft | The review is opened | The owners of the five consumed rows are named as reviewers | In review |
| In review | The review closes with no open comment | The compatibility check passes | Baselined, tagged for the application story and the harness |
| In review | A comment needs a shape change | The change is applied to the draft | Draft |
| Baselined | An additive change is approved | A new optional element only, and the check passes | Baselined, new minor version |
| Baselined | A breaking change is approved | A removal, a rename, a type change or a new required element | Draft of a new major version, and the consumers are notified |
| Baselined | An owner changes its answer | X6 | Draft of a new minor or major version, and the fake is updated |

| Step | Event | Condition | To |
|---|---|---|---|
| Being authored | A consumed row has no published name | X1 | The row carries the placeholder and the gap, and the draft continues |
| In review | An element or a row reaches a foreign schema, base or topic | X3, X7 | The baseline is refused |
| Ready to tag | A consumed row has no fake | X4 | Not tagged, and the review reopens |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-valuation | Authors the baseline, resolves the calculation elements, the workflow elements and the decision-record element, and signs the tag |
| Owner of rwb-source-data (P1) | Reviews the account, balance and freshness rows, and publishes the operation names when they exist |
| Owner of rwb-decision (P7) | Reviews the rule-set row and the decision-record element with the platform library |
| Owner of rwb-case (P3) | Reviews the case and account-set row and the case element of the answer |
| Owner of rwb-access (P4) | Reviews the authorise row and the capability area and right of the declaration |
| Platform library owner (RWB-PLT-E1027, RWB-PLT-N001) | Publishes the decision-record element and the composite route the baseline references |
| Reviewer of the access matrix | Confirms the capability area and the right of the declared operation |
| Any team | Reads the baseline and its fakes from Day 1; no team may change a declared shape outside the lifecycle of s9 |

No person is named anywhere in this document; the roles above are the roles of the run.

### 11. Data

| Element | Owner | Declared in this baseline | Read or write |
|---|---|---|---|
| The account elements of `v_ace_account` (DF-ACE-001 to DF-ACE-042) | P1 (`rwb_source_data`) | account_key, account_code, account_status, contract_no, product_category_efs, total_balance and the field count of the legacy data row; referenced as the data product and not redefined | Consumed |
| The three balance elements (DF-ACE-020, DF-ACE-022, DF-ACE-024) | P1 (`rwb_source_data`) | total_balance, past_due_amount, collections_fee, with their types and nullability | Consumed |
| The freshness elements of `v_ace_batch_status` | P1 (`rwb_source_data`) | the product and its date, as the `payoff_as_at` stamp | Consumed |
| The rule elements of `rule_row` (DF-REF-001 to DF-REF-015) | P7 (`rwb_decision`) | the rule id, the rule version, the route set and the range and floor values the set names; referenced with their types | Consumed |
| The case elements of the route operation | P3 (`rwb_case`) | the case reference, its state and its account set; referenced, not redefined | Consumed |
| The decision-record elements (DF-DEC-001 to DF-DEC-018) | PLT library, created in `rwb_valuation` | the rule id, the rule version, the facts reference, the outcome and the decided-at time | Written through the library |

The baseline declares no table of its own, because the Ownership Map gives S1 none and TSD S1 T3.1 declares only `valuation` and `score`, neither of which is a payoff, range or floor row (GAP-2615; ASM-4317). It declares no column, no index and no migration, and it enumerates no business value: the range bounds, the floor, the freshness limit and the lists are referenced with their identifier and their version. **No personal data** appears in any element, fake or example, and every fixture identifier is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-valuation (S1); base `/api/recovery/valuation/v1` (DP-13). This is the operation the legacy story names in its Endpoints table, and the only one this baseline declares.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/cases/{caseId}/route` | `RouteRequest` in and `Approval` out (API-S1-001); the answer declares the payoff, `payoff_as_at`, `settlement_range_low`, `settlement_range_high`, `floor_price`, the rule id, the rule version and the calculation state | Treatment and offer, right U, scope applied | `Idempotency-Key` header; the stored answer is returned on a repeat |
| None | A calculation or range operation of its own | No source publishes a second operation for the calculation, so no path is declared and the calculation rides the route answer | Not applicable | Not applicable |

The element name of the payoff amount itself is Not specified in the source documents (GAP-2620; ASM-4322); the other seven element names are the names the routing workbook uses (Business Rules and Routing Logic v4, R-SET-02, R-SET-04 and R-SET-05). The two valuation operations of the map are S1's and are the appraisal-intake slice, not this baseline's.

The error envelope of the declared operation: 400 for a malformed request, 401 for an unauthenticated call, 403 with MSG-P4-002 for a role without the right, 404 for an unknown or out-of-scope case, 409 on a second submission under a new key, 422 with MSG-GEN-001 for an invalid element, and 503 when the decision library or a consumed contract does not answer, in one problem document with a code, a message ID and a correlation reference.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| The account and balance data-product read (operation name Not specified in the source documents (GAP-2616; ASM-4318)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | `total_balance`, `past_due_amount` and `collections_fee` of each account of the case at the ACE batch date; faked |
| The freshness read (operation name Not specified in the source documents (GAP-2616; ASM-4318)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The account product and its batch date for the `payoff_as_at` stamp and the freshness gate; faked |
| The rule-set-in-force and decision-log read (operation name Not specified in the source documents (GAP-2616; ASM-4318)) | `/api/recovery/decision/v1` | P7 rwb-decision | The settlement route set at its version, with the range bounds, the floor and the rule id, and the record the ledger holds; faked |
| `GET /cases/{caseId}` family | `/api/recovery/case/v1` | P3 rwb-case | The case, its state and its account set; faked |
| `POST /authorise` | `/api/recovery/access/v1` | P4 rwb-access | The capability area, the right and the scope of the caller; faked |

Each row is one hop, 2 s, a retry once for a GET and a breaker per downstream (ADR-020). Where a name is not published the row carries the placeholder and no path, so the consumer adapts at the tag instead of inventing a surface (BR2). The plan gives this slice no C dependency, so every row is built against its fake.

#### 12.3 Events published

None. The ownership rows give rwb-valuation no event: the topic `rwb.valuation.events.v1` exists with its `.retry` and `.dlt` under the naming rule, but this baseline declares no event, no event name and no outbox row on it. The only publication of this step is the decision record, which the library of DP-03 sends to `rwb.decision-record.v1`, and that is the library's publication and not an event of this service.

#### 12.4 Events consumed

None declared. FSD S1 A2.6.2 names the trigger set as "a completed ACE batch, an event or a timer" and no source publishes an event name for any of them; the ownership rows give S1 no job and no event, so the baseline declares no subscription and the trigger is carried by the application story (GAP-2619; ASM-4321). The freshness of the account data product is read as an element of the rwb-source-data row and not as a subscription.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `RouteDecisionWorkflow` | Workflow, one execution per case per assessment, continues-as-new | `rwb-valuation` in namespace `rwb-recovery` | Input: the case, the account set and the rule set in force; signals: the freshness answer of the account product and the rule version |
| `calculatePayoffAndRange` | Activity | `rwb-valuation` | The account set and the business date in; the payoff, `payoff_as_at`, the range bounds, the floor, the rule id and version and the decision record out, in one transaction |
| `readAccountBalances` | Activity | `rwb-valuation` | The account keys in; the three balances and the product date out; no write |

`RouteDecisionWorkflow` is the one workflow the ownership rows give S1. This baseline fixes its input, its two signals and the two activities the calculation adds; the remaining activities of the route decision are the sibling stories'. The activity names are a design choice of the application story, and the baseline carries them so that the workflow history is stable.

#### 12.6 Schedules

None. The ownership rows give S1 no job, and this baseline declares no Temporal Schedule and no legacy Quartz job. A batch-completion trigger would be a Schedule of this service and no source names one (GAP-2619; ASM-4321).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| None | S1 declares no payoff, range or floor table | The ownership rows give S1 no table and TSD S1 T3.1 declares only `valuation` and `score` (GAP-2615; ASM-4317) |
| decision_record | PLT library, created in `rwb_valuation` | The local decision record of DP-03, declared through RWB-PLT-E1027-CON |
| idempotency_key | PLT library, created in `rwb_valuation` | The key of the repeated command and the answer it holds |

The baseline declares no column, no index and no migration, and it declares no table of another owner: `v_ace_account` and `v_ace_batch_status` (P1), `rule_row`, `decision_log_entry` and `approval` (P7), `treatment` (S2) and `recovery_case` and `timer` (P3) are named by their owners and never declared here. If the S1 table owner later confirms a calculation table, the DB story of this service creates it in its own Flyway sequence and this baseline declares its elements in a minor version.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and balance fake | Account `A-0001` of case `RC-2026-000401` with total balance 1240000, past due amount 86000 and collections fee 4500 at ACE batch date 2026-12-14; an account with no row; no answer beyond 2 s | C3, C4, C6 |
| rwb-source-data freshness fake | The account product at the business date, and the same product from an earlier date | C3, C6 |
| rwb-decision rule-set and log fake | The settlement route set in force with its rule id and version, its range bounds and its floor; a set with no floor; the record the ledger holds | C3, C6 |
| rwb-case account-set fake | Case `RC-2026-000401` with account `A-0001`; a case in another state | C3, C6 |
| rwb-access authorise fake | The capability area Treatment and offer, right U accepted and refused | C5 |
| Decision-record stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | C6 |
| gateway-bff composite route fake | The merged SCR-13 answer for case `RC-2026-000401`, with the payoff, the range and the floor elements read once | C2, C6 |

Each fake answers only what its owner documents, and a fake that answers more than its document fails the review. The rows whose names are not published are stubbed from the documents and carry the placeholder until their owners confirm them (GAP-2616; ASM-4318).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 5 consumed | `POST /cases/{caseId}/route` on `/api/recovery/valuation/v1`; the rwb-source-data account and freshness rows, the rwb-decision rule-set row, the rwb-case row and the rwb-access row; one hop, 2 s |
| Kafka | 0 published, 0 consumed | No event of this service and no declared subscription; the decision record reaches `rwb.decision-record.v1` through the library of DP-03 |
| Temporal | 1 workflow and 2 activities | `RouteDecisionWorkflow`, `calculatePayoffAndRange` and `readAccountBalances` on `rwb-valuation`; no Schedule |
| File | None declared | The step reads contracts only; the fresh-payoff request of R-SET-03 and the interfaces behind it are rwb-integration's |

### 13. Solution plan

**Document.** `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-S1 rwb-valuation (Valuation and route)/RWB S1 E4006 CON Calculate the payoff and settlement range - contract v1.md`, with the schema and the examples in the service contract folder of RWB-S1-E4006.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Sections and owners of the review.** The document is written in nine parts: the provided operation and its eight calculation elements, the five consumed rows, the empty publication, the workflow and its activities, the tables, the fakes, the call-type summary, the data elements and the lifecycle. Each part is reviewed by the owner of the rows it names, and the tag waits for every reviewer.

**Compatibility check.** The schema is published as JSON Schema with `additionalProperties: false` on the closed objects, and the check runs on three inputs: the previous tag, the new draft and a corpus of recorded answers from the fakes. A removal, a rename, a type change or a new required element fails the check and forces a new major version (C1, BR3).

**Fakes.** One per consumed row plus the composite route, each built from the document and not from the real service, so that a fake can be published before its owner's build finishes (C6).

**Done when.** The seven criteria pass, the five reviewer roles have closed their comments, the compatibility check passes on the tag, the eight fakes are published with their documented answers, and RWB-S1-E4006-APP and the wave 3 harness can start against the tag with no open shape question.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A role without the Treatment and offer right calls the declared operation | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required element of `RouteRequest` is absent or invalid, or a declared calculation element has no value | Enter {field}. |
| MSG-P7-003 | The decision record cannot be written, as the decision-record element declares it | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The ACE account data product behind the balance row is stale | {product} is from {date}. Today's ACE batch has not arrived. |
| Document rule | A change fails the compatibility check | A breaking change needs a new major version. |
| Document rule | A consumed row or an element has no published name | Not specified in the source documents (GAP-2616; ASM-4318). |

The four message IDs are those of the legacy story, of FSD S1 A2.6.3.1 and of the platform set, copied unchanged. The two document rules are checks of this story and are not service messages.

### 15. Screens and states

The baseline serves SCR-13 Route decision through the gateway-bff composite route (DP-19). What this story fixes is the calculation part of the element list of the route answer and the states the screen can show from it.

| Screen | States | What the route reads on this service |
|---|---|---|
| SCR-13 Route decision | Loading; recommendation; overridden; submitted | The payoff and its as-at date, the two range bounds, the floor, the rule version and the calculation state: calculated, blocked on a stale product, or an unmatched exception naming the missing value |

No screen is built here, no component is delivered and no state machine is declared: the screen section of a contract story lists the elements the screens read and the states their answers can carry. The route itself, its merge order and its field list are RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-006-01 | C1, C2: the payoff, the range and the floor elements of the answer, with their types and sources | Contract | The published schema and the recorded answer of case `RC-2026-000401` with the AC1 amounts |
| TC-E4-006-02 | C4, C6: the decision-record element and the stopped chain | Contract | The decision-record element, a healthy stub and a stopped stub |
| TC-E4-006-03 | C5: the right and the error envelope of the declared operation | Contract | One request per right, including a role without it; one request per error code, 400, 401, 403, 404, 409, 422 and 503 |
| TC-E4-006-04 | C3, C7: the five consumed rows, the boundary and the empty publication | Contract | The five rows with and without a published name; the base, the topic, the queue and the schema; an outbox declaration that must stay empty |
| TC-S1-E4006-CON-01 | C3: the placeholder and the gap of an unpublished operation name | Contract | The five consumed rows, each with and without a published name |
| TC-S1-E4006-CON-02 | C6: the fakes, the workflow elements and the decision-record element | Contract | The eight fakes and one fake that answers more than its document |
| TC-S1-E4006-CON-03 | C1, C7: the compatibility check and the naming boundary | Contract | The previous tag, an additive draft, a breaking draft, and a draft that names a foreign schema, a monolith base, a foreign topic or a Schedule |

The four legacy case IDs are the legacy test cases of RWB-E4-006 in their legacy order, mapped onto this contract deliverable: the calculation and its elements (01), the failure of the decision log (02), the access path (03) and the principle-5 record failure (04). The three `TC-S1-E4006-CON-` cases are new and test the parts of the baseline no legacy case touches. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID; the `-ITG` copies belong to the wave 3 harness.

### 17. Guardrails

- No business value in the baseline: the range bounds, the floor, the freshness limit and the closed lists are referenced with their identifier, list or version, never enumerated as a constant or a default.
- No personal data in any element, fake, example or log: identifiers, codes, amounts, dates and a rule version only, and every fixture is synthetic.
- ACE data only through the owner's contract or the service's own view: the baseline declares no `v_ace_*` copy and no ACE table, and the balances appear only as the rwb-source-data data product (DP-05).
- The case stays with rwb-case, the rule set and the ledger with rwb-decision, and the treatment record with rwb-treatment: none is declared as this service's own.
- One base, one topic, one queue and one login per service; no document, module or test names another service's base or topic as its own (DP-13, DP-14).
- No retired element is reintroduced: no monolith base `/api/recovery/v1`, no account copy table, no shared job table, no Quartz row, no Schedule, no foreign schema and no event published by this baseline.
- Additive only: a breaking change needs a new major version and a re-tag, and the code never moves ahead of the document (BR3).

### 18. Traceability

| Source | Reference | Used in |
|---|---|---|
| Legacy story | RWB-E4-006, disposition Split (rework); AC1 and AC2 are owned by RWB-S1-E4006-APP; this story carries no legacy criterion and fixes the surface both touch | 1, 11, 12, 16 |
| Feature | FEAT-VAL-06 Calculate the payoff and settlement range, module S1, epic E4, depends on FEAT-DRI-07 | 1, 2, 3 |
| FSD S1 v3 | A2.6.1 intent and metric; A2.6.2 steps and integration points ALS and GL and the Rules component; A2.6.3.1 VR-S1-006-1 and BR-S1-006; A2.6.3.3 roles; A2.6.4.1 AC-S1-006-01; REQ-S1-004; SCR-13 | 2, 3, 8, 12, 14, 15 |
| TSD S1 v2 | T2 components; T3.0 standard columns; T3.1 `valuation` and `score`; T5.2 cross-module interfaces; T6.1 rights; T-A.1 and T-A.2 API-S1-001 | 3, 10, 11, 12, 16 |
| Epics 3 to 8 Specification v3 | E4 S1 FEAT-VAL-06 row; FEAT-VAL-07 and FEAT-TRT-02 depend on it | 1, 3 |
| Routing logic v4 | R-SET-01, R-SET-02, R-SET-03, R-SET-04, R-SET-05 and R-SET-25 (D6.4); the element names of the range, the floor and the as-at date | 2, 8, 11, 12 |
| Logical data model and Physical Schema | DF-ACE-001 to DF-ACE-042; DF-ACE-020, DF-ACE-022 and DF-ACE-024; DF-REF-001 to DF-REF-015; DF-DEC-001 to DF-DEC-018 | 11 |
| Patterns | DP-03, DP-05, DP-13, DP-19 (Template and Rules v1 §R5.5) | 13 |
| Gaps and assumptions | GAP-2615, -2, -4 and -6; ASM-4317, -2, -4, -6 and -7 | 1, 3, 11, 12, 13, 14 |
| Decisions | ADR-010, ADR-013, ADR-014, ADR-020, ADR-022; D-RCV-35 U1; D-RCV-60 | all |

### 19. Out of scope

- The calculation itself, its freshness gate, its exception paths and the screen behaviour: RWB-S1-E4006-APP.
- The route recommendation, its reasons and the alternatives: FEAT-VAL-07 and its story.
- The approval of the route, the override reason and the case move: the route-decision submission slice of RWB-E4-005 and rwb-case (P3).
- The offer built inside the range and the treatment record: rwb-treatment (S2).
- The ACE balances, their batch date and the freshness of the data product: rwb-source-data (P1).
- The range bounds, the floor, the rule package, its approval and the central ledger: rwb-decision (P7).
- The fresh-payoff request to EAPI: rwb-integration (P2).
- The roles, scopes and masking behind the right: rwb-access (P4) and the guard of the service template.
- The composite route, the merge order and the field list of SCR-13: RWB-PLT-N001-CON and the edge stories.
- The decision-record library's own schema and migration: RWB-PLT-E1027-CON.
- The cross-service journey of the legacy key and its evidence: the wave 3 harness.
- The deployment, the flag, the dashboards, the alerts and the runbook of this capability: the operations story of this legacy key.
