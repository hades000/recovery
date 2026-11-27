# RWB-S6-E6008-CON Derecognize and post to the general ledger - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S6-E6008-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-debtsale |
| Service epic | RWB-SVC-S6 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S6 rwb-debtsale v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the derecognition and posting slice of rwb-debtsale, split from RWB-E6-008. It fixes the derecognition, posting-item and posting-result elements and the activity answers they appear in (DP-13), the state and item vocabulary, the four consumed rows for the account facts, the case state and move, the package in force and the rwb-integration posting interface (DP-05), the decision-record element of DP-03, the rights, the error envelope, the fakes and the absence tests. TSD S6 appendix T-A publishes no derecognition or posting operation, and no column of the two tables carries a posting result, so the baseline declares no provided operation and no answer property and records both absences. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S6-E6008-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the derecognition and posting step of rwb-debtsale — the derecognition, posting-item and posting-result elements and the activity answers they appear in, the state and item vocabulary, the four consumed rows for rwb-source-data, rwb-case, rwb-decision and rwb-integration, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, the settlement and put-back stories and the wave 4 harness build against one fixed, testable contract on Day 1 and an item type, a result code, a state name or an answer shape can never drift between rwb-debtsale, rwb-source-data, rwb-case, rwb-decision and rwb-integration without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy derecognition of RWB-E6-008 crossed four boundaries at once: a case state, an account balance held in ACE, a decision log and a posting to ALS and the general ledger. The target splits them: rwb-case owns the case and its route states, rwb-source-data owns the account and balance facts, rwb-decision owns the package in force and its ledger, rwb-integration owns the interface to ALS, the general ledger and the Finance provision feed, and rwb-debtsale owns the lot, the decision and the item it sends. Each boundary is a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_debtsale`, base `/api/recovery/debtsale/v1`, topic `rwb.debtsale.events.v1` with its retry and `.dlt` topics, task queue `rwb-debtsale` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.debtsale`.

Four points are carried as gaps and assumptions rather than decided quietly. The plan's C row for this slice is None while the step needs four consumed contracts and one interface call (GAP-3007; ASM-4960). TSD S6 appendix T-A publishes no derecognition or posting operation and the two endpoint rows of the legacy story belong to the lot builder and the data room (GAP-3007; ASM-4964). No column of `debt_sale_lot` or `debt_sale_account` carries the posting result, the item reference or the rejection reason, so the elements are activity and record elements and appear in no REST answer (GAP-3007; ASM-4965). And the ledger item's identifier, layout and result codes are rwb-integration's data and are named by no source in the read set (GAP-3007; ASM-4963).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the `Idempotency-Key` rule and the problem-document convention are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `debt_sale_lot` and `debt_sale_account` are S6's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, `role` and `permission` are P4's, `document` is P5's, `notice` is P6's, `proceeds` is P8's, and the interface rows and the outbound item are P2's. This document never declares another service's table, operation or interface as its own.
- The rwb-source-data account read, the rwb-case state read and move answer, the rwb-decision package read and the rwb-integration outbound interface are published with their fakes, so each consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3007; ASM-4960).
- The DEBTSALE package and its rows for R-DS-29 to R-DS-33 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `debt_sale_lot` and `debt_sale_account` arrive with the DB story of this service, with the columns of DF-SAL-020 to DF-SAL-037; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). No approved baseline exists for the key — FSD S6 v3 and TSD S6 v2 stand at "In review" — so the baseline is published in Draft (realignment v1) and the release 30 April 2027 is copied unchanged and marked tentative (ASM-4967).
- The metadata wave is EP06's wave 4 while the service itself is created in wave 3 (Template and Rules §R5.6); the baseline is still a Day-1 artefact because it carries no build dependency (ASM-4968).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-debtsale for this step: the derecognition, posting-item and posting-result elements with the rights and the error responses, and no operation of its own (GAP-3007; ASM-4964).
2. Fix the elements: the lot and account references, the balance removed, the rule ID with its version, the item type, the business date, the amount, the value date, the item reference, the result code, the rejection code and the exception task reference.
3. Fix the consumed rows: the rwb-source-data account and balance read with its as-of date, the rwb-case state read and move answer, the rwb-decision package read and the rwb-integration posting item, marking the fields the sources do not give with the placeholder.
4. Record the decision-record element of DP-03, written before anything leaves.
5. Record the closed vocabulary of the states, the item types and the lists, and the rule that no value is a constant of the code.
6. Record that a record, an item manifest and a fake carry references, codes, amounts, dates and a rule version only, and no person name, identity number, address or contact value.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a provided operation and of an answer property, the absent `recovery_case`, `v_ace_*` and `interface_config` properties, the drift between a fake and the document, and the absence of published and consumed events of this step.
9. Tag the baseline and hand it to RWB-S6-E6008-APP, the settlement and put-back stories and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body, a request body or an element fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC7 |
| X2 | A field is renamed or removed within major version 1, or an item type changes | The contract test fails; the change needs a new major version | None | AC1, AC4 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A state, an item type or a list value outside the declared vocabulary appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a provided operation, an answer property, or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC1, AC7 |
| X7 | The document declares a published or a consumed event for this step, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | A person field — a name, an identity number, an address or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC6 |
| X9 | The rights of a surface are not the ones TSD S6 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-source-data, rwb-case, rwb-decision and rwb-integration only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the vocabulary, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S6-E6008-APP, the settlement and put-back stories and the wave 4 harness on Day 1, and gives the rwb-integration team the one item shape it must answer |
| Estimable | One OpenAPI fragment, nine contract tables, six fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the derecognition and posting step of rwb-debtsale

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of debt_sale_lot and debt_sale_account is S6, of recovery_case is P3, of decision_log_entry and rule_row is P7 and of the interface rows and the outbound item is P2
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The derecognition, posting-item and posting-result elements are declared and no operation is claimed (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-debtsale for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the AccountDerecognition element with the lot reference, the account reference, the balance removed, the rule ID with its version and the decided-at time, the PostingItem element with the interface reference, the business date, the item type, the amount, the value date, the item reference, the result code, the rejection code and the idempotency key, and the PostingResult element with the record id, the item set, the result, the case move and the exception task reference
    Then the elements are declared as the input and output of the derecogniseAccounts and postToLedger activities on rwb-debtsale and as the decision-record payload, and it records that no published REST answer carries them because no column of the two tables does (GAP-3007; ASM-4965)
    Then it declares no provided operation and records that TSD S6 T-A publishes none for this step, and that the two endpoint rows of the legacy story are API-S6-001 and API-S6-002 and belong to the lot builder and the data room (GAP-3007; ASM-4964)
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition

  Scenario: AC2 The state, item-type and list vocabulary is closed (new, D-RCV-60)
    Given the vocabulary section of the baseline
    When it is compared with TSD S6 T3.2, T4 and the rule rows R-DS-29 to R-DS-34
    Then the states named are DATA_TRANSFERRED, DERECOGNISED, GL_POSTED and POSTING_REJECTED_DS of the DEBTSALE machine, and LOT_CLOSED is named as R-DS-34's and not declared here
    Then the item type is declared against a closed list with the values ALS_BALANCE_REMOVAL, GL_ENTRY and PROVISION_INPUT, and no fourth value
    Then the lot status is declared against LOV-LOT-STATUS with the values BUILDING, OFFERED, AWARDED, TRANSFERRED and CLOSED, segment against LOV-SEGMENT with RETAIL, SSME and CORPORATE, buyer_class against LOV-BUYER-CLASS with AMC and NON_AMC, and put_back_status against LOV-PUTBACK with NONE, CLAIMED, ACCEPTED and REJECTED
    Then no state, no item type and no list value is a constant of the code, and the vocabulary test fails the build on any value outside these sets
    Then no property carries a person name, an identity number, an address or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The four consumed rows are declared with their owners and their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the owner documents and the connection matrix row of S6
    Then the account and balance read is declared as consumed from P1 rwb-source-data, with the account reference, the account code, the account status, the contract number, the total balance, the outstanding and the as-of date
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state and the moves DERECOGNISED, GL_POSTED and POSTING_REJECTED_DS carrying the rule ID and its version
    Then the package read is declared as consumed from P7 rwb-decision, with the version in force and the rows R-DS-29 to R-DS-33 named and not declared
    Then the posting item is declared as consumed from P2 rwb-integration as an activity on queue rwb-integration, with the three item types, the manifest fields and the item reference and result code back (GAP-3007; ASM-4960, ASM-4963)
    Then the operation names of the four rows are Not specified in the source documents (GAP-3007; ASM-4960) and the rows carry the placeholder
    Then the document declares no account, balance, recovery_case, rule_row, interface_config or outbound_item property, and no grant on another schema

  Scenario: AC4 The posting item and its result set are fixed and the interface values stay data (new, D-RCV-60)
    Given the item section of the baseline
    When it is compared with R-DS-30 to R-DS-33 and with the interface of rwb-integration
    Then the manifest carries the interface reference, the business date, the lot reference, the case set, the account set, the amount, the value date, the posting facts block and the Idempotency-Key
    Then one item set is declared per lot and business date, and a rejected item is declared as held under R-DS-32 and replaced only by the corrected item of R-DS-33
    Then the item identifier, the transport, the file layout, the result codes and the retry schedule are declared as rows of rwb-integration's interface configuration, read per item and named by no source in the read set (GAP-3007; ASM-4963)
    Then the document declares no file layout, no chart of accounts and no entry set of its own, and no direct ALS or general ledger endpoint
    Then a repeated request with the same Idempotency-Key describes no second item and answers the item that exists

  Scenario: AC5 The decision-record element, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the decision section and the access section of the baseline
    When they are compared with the library schema, TSD S6 T6.1 and the platform error envelope
    Then one record is declared per rule outcome with the case reference, the lot reference, the account set, the rule ID, the package version in force, the inputs reference with the as-of date, the item references, the result codes, the outcome, the reason and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything leaves, and a failed write leaves no item and answers no move, with MSG-P7-003
    Then the capability area Debt sale and its rights are declared as consumed from P4 rwb-access, with RW-DEBTSALE CRUA, RW-PRODHEAD RA, RW-HEADASL RA, RW-CREDITAD R and the SY-* identities R as TSD S6 T6.1 gives them
    Then a refused caller answers 403 with MSG-P4-002, and the posting and re-post run under the service identity because RW-CREDITAD holds R only (GAP-3007; ASM-4964)
    Then the document declares no decision_log_entry column and no rule_row column as its own

  Scenario: AC6 The fakes answer the document and the drift test holds (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-source-data fake answers the accounts of lot LOT-2026-000042 with their balance as-of 2026-12-31, a stale product with its date and no answer beyond 2 s
    Then the rwb-case fake answers the states DATA_TRANSFERRED and DERECOGNISED, an accepted move and a refused move for each of the three move names, the rwb-decision fake answers the DEBTSALE package at its version, and the rwb-access fake answers the capability area with and without the right
    Then the rwb-integration fake answers one accepted ALS item, one accepted general ledger item, one item rejected by ALS, one item rejected by the general ledger, one refused manifest and no answer beyond 2 s
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-26 award screen for the lot
    Then every fake carries references, codes, amounts, dates and a rule version only, with no person name, identity number, address or contact value, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and this step publishes and consumes no event (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_debtsale, the login is rwb_debtsale, the topic is rwb.debtsale.events.v1, the queue is rwb-debtsale and the Java package is th.co.scb.ace.workbench.recovery.debtsale
    Then 12.1 is None and records that no operation is provided and that API-S6-001 and API-S6-002 belong to the lot builder and the data room
    Then the tables named as owned are debt_sale_lot, debt_sale_account and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, role, permission, document, notice, proceeds, decision_log_entry, rule_row, interface_config, outbound_item and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event for this step, and it records that LotAwarded (EV-23) is the award story's, AccountsTransferred is the transfer story's and ProceedsMatched (EV-25) is the remittance story's
    Then the document declares no Schedule and records that the month-end close of R-DS-31 is a durable timer of DebtSaleWorkflow (GAP-3007; ASM-4966)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S6-E6008-APP and they copy no criterion of the legacy story, whose AC4 stays with the app story word for word and whose AC1 to AC3 are RWB-ITG-E6008-ITG's.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The lot and its population are rwb-debtsale's, and the contract declares their fields and lists as read by this step only | Architecture v5 slide 4; TSD S6 T3.1 and T3.2 |
| BR2 | The decision record is declared as an element written before anything leaves, through the local library on the shared topic; a failed write sends no item and answers no move | DP-03; TSD S6 T2; legacy AC4 |
| BR3 | The account and balance facts stay with rwb-source-data: the contract declares the read as consumed and declares no account, balance or `v_ace_*` property | DP-05; TSD S6 A2.12.2; ASM-4961 |
| BR4 | The case move is answered and not written: the contract declares the state read and the three moves, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); ASM-4961 |
| BR5 | The posting leaves only through rwb-integration: the contract declares one interface read, three item types and the result back, and no direct ALS or general ledger endpoint | R-DS-30 to R-DS-33 (Systems column); ASM-4963 |
| BR6 | This baseline declares no provided operation: the step runs unattended behind the workflow and no answer of the service carries a posting field | TSD S6 T-A.1; GAP-3007; ASM-4964 |
| BR7 | A POST of an item declares the `Idempotency-Key`; one item set per lot and business date; a GET declares none | Architecture v5 slide 11; TSD S6 T-A.2; R-UNI-40 |
| BR8 | The vocabulary is closed: the four states, the three item types and `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS` and `LOV-PUTBACK` are published as enumerated values and no value is a constant of the code | TSD S6 T3.2, T4; FSD S6 BR-S6-012 |
| BR9 | No personal data in a schema, an example or a fake: a record and an item carry references, codes, amounts, dates and a rule version only | Template and Rules v1 §R7.2 (s17); FSD S6 A2.3 |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or queue as its own | DP-13; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change, including a change of an item type or of a state name, is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR12 | The interface identifier, the transport, the layout, the result codes and the retry schedule are rwb-integration's configuration rows, named here and declared nowhere here | GAP-3007; ASM-4963 |
| BR13 | The posting result and its references have no column in TSD S6 T3.1, so the record and the case state carry them and this baseline adds no column and no migration | GAP-3007; ASM-4965 |

### 9. State transitions

The lifecycle of this document, not of a lot:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The elements, the vocabulary, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the settlement and put-back stories, the wave 4 harness and the rwb-source-data, rwb-case, rwb-decision and rwb-integration owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional result field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, an item type or a state name changes, or a provided operation is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1 and AC7 fail: a provided operation, an answer property, a `recovery_case` or `v_ace_*` property, an event or a Schedule | In review |

The route state machine the document describes is the app story's: a transferred case is derecognised, posted, or held at `POSTING_REJECTED_DS` and re-posted. This baseline fixes the vocabulary of those states and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-debtsale | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the absent derecognition operation and the absent posting column |
| Consuming teams (the app story, the settlement and put-back stories, the wave 4 harness and the owners of rwb-source-data, rwb-case, rwb-decision and rwb-integration) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| rwb-integration (P2) | Owns the interface identifier, the transport, the layout, the result codes and the retry schedule the items obey |
| Data steward | Confirms that no personal data field is declared in an element, an answer or a fake |

The per-service login behind the security scheme of the document is named "the rwb_debtsale login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Derecognition element | The lot reference, the account reference, the balance removed, the rule ID with its version and the decided-at time |
| Posting item element | The interface reference, the business date, the item type, the amount, the value date, the posting facts block, the idempotency key, the item reference and the result and rejection codes |
| Posting result element | The record id, the item set with its references and result codes, the result, the case move and the exception task reference |
| Account facts | The account reference, the account code, the account status, the contract number, the total balance, the outstanding and the as-of date, of P1 rwb-source-data, read only through the owner's contract (DF-ACE-001 to DF-ACE-042) |
| Lot and account shapes | The lot columns DF-SAL-020 to DF-SAL-030 and the account columns DF-SAL-031 to DF-SAL-037, as the step reads them; the missing posting columns are recorded (GAP-3007; ASM-4965) |
| States and lists | `DATA_TRANSFERRED`, `DERECOGNISED`, `GL_POSTED`, `POSTING_REJECTED_DS`; the item types `ALS_BALANCE_REMOVAL`, `GL_ENTRY`, `PROVISION_INPUT`; `LOV-LOT-STATUS`, `LOV-SEGMENT`, `LOV-BUYER-CLASS`, `LOV-PUTBACK` |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything leaves (DP-03) |
| Not declared here | `recovery_case` and `timer` (P3), `role` and `permission` (P4), `document` (P5), `notice` (P6), `proceeds` (P8), `decision_log_entry` and `rule_row` (P7), `interface_config` and `outbound_item` (P2), and every `v_ace_*` view (P1) |
| Consumed fields with no source | The four operation names, the interface identifier, the transport, the layout, the result codes and the retry schedule: Not specified in the source documents (GAP-3007; ASM-4960, ASM-4963) |

The field-level types, lengths and required flags of the elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the additive rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S6 appendix T-A publishes five operations for the module: API-S6-001 `POST /debt-sale-lots` (C), API-S6-002 `GET /debt-sale-lots/{lotId}` (R), API-S6-003 `POST /debt-sale-lots/{lotId}/award` (A), API-S6-004 `GET /partner/data-room/{lotId}` (Partner portal R) and API-S6-005 `POST /partner/data-room/{lotId}/bids` (Partner portal C), and none of them is a derecognition or a posting operation. The two endpoint rows of the legacy story are API-S6-001 and API-S6-002; they are the lot builder's and the data room's, and the posting state is read from the case state of rwb-case on the award screen. This baseline therefore declares no operation as provided, records the two sibling rows by name, and fixes only the elements and the activity answers of the step. The absence is recorded as GAP-3007 with ASM-4964.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| The account and balance read (operation name Not specified in the source documents (GAP-3007; ASM-4960)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The account reference, its code, its status, the contract number, the total balance, the outstanding and the as-of date; faked |
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its route state and its lot link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3007; ASM-4960)) | rwb-case (P3) | P3 rwb-case | The moves `DERECOGNISED`, `GL_POSTED` and `POSTING_REJECTED_DS` with the rule ID and its version; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEBTSALE package at its version with R-DS-29 to R-DS-33; faked |
| The posting item (activity name Not specified in the source documents (GAP-3007; ASM-4963)) | activity on queue `rwb-integration`, Temporal namespace `rwb-recovery` | P2 rwb-integration | The manifest of AC4 in; the item reference and the result code out; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four reads and the item call are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3007 with ASM-4960.

#### 12.3 Events published

None. Architecture v5 and the event catalogue give rwb-debtsale the topic `rwb.debtsale.events.v1` with `LotAwarded` (EV-23, payload `lotId`, `buyerId`, `price`) and with `AccountsTransferred` beside it in the service's event set. Both are sibling stories': EV-23 is the award's (RWB-S6-E6005-APP) and `AccountsTransferred` is the transfer's (RWB-S6-E6007-APP). No posting-result or derecognition event exists, so the baseline declares no event of its own, no outbox row and no producer, and the absence test of AC7 fails a build that adds one (ASM-4962).

#### 12.4 Events consumed

None. The connection matrix gives rwb-debtsale `ProceedsMatched` (EV-25) from rwb-payment, which belongs to the remittance story (RWB-S6-E6011-APP), and no event of the module carries a derecognition or a posting answer. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one (ASM-4962).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `DebtSaleWorkflow` | Workflow, one execution per lot, the child of `CaseWorkflow` on rwb-case (P3), a saga whose pivot is the transfer and which continues-as-new across the posting and the put-back window | `rwb-debtsale` in namespace `rwb-recovery` | The stage that hosts the two steps; its signals and its outcome for the parent are declared, not built |
| `derecogniseAccounts` | Activity, the R-DS-30 step | `rwb-debtsale` | In: the lot, its accounts, the balance and the package in force. Out: the rule ID with its version, the record id and the `DERECOGNISED` move |
| `postToLedger` | Activity, the R-DS-31 to R-DS-33 step | `rwb-debtsale` | In: the account set, the amounts, the business date and the items. Out: the item references, the result codes, the record id and the `GL_POSTED` or `POSTING_REJECTED_DS` move |
| The outbound item call | Activity provided by rwb-integration, called as a task | `rwb-integration` | In: the manifest of AC4. Out: the item reference and the result code |

No child workflow for the case and none for the money exists in this service. The activity names are target design choices and the trigger is the transfer of the lot and the month-end close of R-DS-31. No activity is registered by this story, and the award, settlement, transfer, put-back and lot-closure steps belong to the sibling stories of this service.

#### 12.6 Schedules

None. R-DS-31 carries "month-end close" in its timer column and the service owns no job row, so the wait is a durable timer inside `DebtSaleWorkflow`. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table (GAP-3007; ASM-4966).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| debt_sale_lot | S6 (`rwb_debtsale`) | The lot, its status and its accounts; read by this step, which changes no column |
| debt_sale_account | S6 (`rwb_debtsale`) | The accounts of the lot and their balance; read by this step, which changes no column (GAP-3007; ASM-4965) |
| decision_record | PLT library, created in `rwb_debtsale` | The local hash-linked decision record of each rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_debtsale` | The key of the lot, the business date and each item |
| outbox_event | PLT library, created in `rwb_debtsale` | The library object the service's sibling stories relay their events through; this step declares no row |

`recovery_case` and `timer` (P3), `role` and `permission` (P4), `decision_log_entry` and `rule_row` (P7), `document` (P5), `notice` (P6), `proceeds` (P8), `interface_config` and `outbound_item` (P2) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or another story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and balance fake | The accounts of lot `LOT-2026-000042` with their status, contract, total balance and outstanding, as-of `2026-12-31`; a stale product with its date; no answer beyond 2 s | AC3, AC6 |
| rwb-case state and move fake | Cases at `DATA_TRANSFERRED` and `DERECOGNISED` of lot `LOT-2026-000042`; an accepted move and a refused move for each of the three move names | AC3, AC6 |
| rwb-decision rule-package fake | The DEBTSALE package at its version in force with R-DS-29 to R-DS-33 | AC3, AC6 |
| rwb-integration outbound-interface fake | One ALS item accepted with a reference, one general ledger item accepted, one item rejected by ALS, one rejected by the general ledger, one manifest refused, no answer beyond 2 s | AC4, AC6 |
| rwb-access authorise fake | The capability area "Debt sale" with its rights for the TSD S6 T6.1 roles; a caller without the right | AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-26 answer for lot `LOT-2026-000042`, carrying the case state once | AC1, AC6 |

The fakes are test-only and are replaced by the real services in SIT. The four operation names and the interface values are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3007; ASM-4960, ASM-4963).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 3 consumed | The rwb-source-data account read, the rwb-case state read and the case-move answer, the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `LotAwarded` and `AccountsTransferred` are sibling stories' and `ProceedsMatched` is the remittance story's |
| Temporal | 1 workflow and 2 activities declared, plus 1 activity of rwb-integration, 0 registered | `DebtSaleWorkflow`, `derecogniseAccounts` and `postToLedger` on `rwb-debtsale`; the outbound item on `rwb-integration`; no Schedule |
| File | None declared | The ALS and ledger interface is a file run of rwb-integration's interface row; this baseline fixes a manifest, not a layout |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no lot, no case, no account and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, seven fakes and four new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-debtsale-v1.yaml` for the three elements, the vocabulary of the four states, the three item types and the four lists as published enumerations, the contract README rows for the five consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the record element describes: the record and the item commit together or not at all. DP-05 is applied as the owner's contract, and the document declares no `v_ace_*` property. DP-13 fixes the base and this baseline adds no operation to it. DP-19 is behind SCR-26, whose screen model is the edge contract's. The two H rows of the table are the ones the metadata carries, and the five consumed rows are class C in fact while the plan's C row is None (GAP-3007; ASM-4960).

**Build steps**

1. Write the three elements and the no-provided-operation record of AC1, and validate the additive rule in the pipeline.
2. Write the vocabulary of AC2 and the four lists as published enumerations with the no-constant rule.
3. Record the four consumed rows of AC3 with their owners, their budget and their placeholders.
4. Record the posting item, its result set and the interface values of AC4.
5. Record the decision-record element, the rights and the error envelope of AC5.
6. Publish the seven fakes of AC6 and the drift test.
7. Record the naming baseline, the boundary, the absence of events and of a Schedule of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the four contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the settlement and put-back stories and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S6-001 | Carried from the legacy message set of this key. It names an open deviation on an account, which is the eligibility story's, so no path of this step raises it | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | A required field of a manifest is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Debt sale right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything leaves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | The account or balance product of the lot is stale after a late or failed batch (VR-S6-012-1); the check is the owner's | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P2-001 | ALS or the general ledger rejects an item; the row is rwb-integration's | Not specified in the source documents (GAP-3007; ASM-4963) |

The five named message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is invented. MSG-P2-001 is carried because a rejected posting is read from rwb-integration's exception queue, and its text is that service's row.

### 15. Screens and states

The contract serves SCR-26 Award in its transferred, derecognised, posted and rejected readings, all read only, through the gateway-bff composite route (DP-19). The route calls rwb-debtsale for the lot and its accounts, rwb-case for the case and its route state and rwb-source-data for the balance and its as-of date; this baseline fixes the elements and the case state the screen reads, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refused, not-recorded, rejected and stale readings the app story shows use the messages of section 14 on the same route. SCR-25 Lot builder and PRT-05 Data room are other stories' and read nothing from this step.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-008-01 | AC1, AC2 | Contract | Lot `LOT-2026-000042` with 12 accounts; the contract half answers the three elements, the no-provided-operation record and the state and item vocabulary |
| TC-E6-008-02 | AC3, AC5 | Contract | The account and balance fake as-of `2026-12-31`; the contract half answers the rwb-source-data row, its placeholder and the `DERECOGNISED` move shape |
| TC-E6-008-03 | AC4 | Contract | An ALS item accepted and a general ledger item rejected; the contract half answers the manifest, the result set and the held and re-posted shapes |
| TC-E6-008-04 | AC5, AC6 | Contract | The record stub stopped; the contract half answers the MSG-P7-003 path and the decision-record element |
| TC-E6-008-05 | AC5 | Contract | RW-CREDITAD holds R and RW-DEBTSALE holds CRUA; the contract half answers the rights of the capability area |
| TC-E6-008-06 | AC6, AC7 | Contract | A malformed manifest and an absent account answer; the contract half answers the error envelope, the absence tests and the no-personal-data test |
| TC-S6-E6008-CON-01 | AC1 | Contract | The fragment validates; the three elements, the seven error answers and the no-provided-operation and no-answer-property records are present |
| TC-S6-E6008-CON-02 | AC2 | Contract | The four states, the three item types and the four lists validate as closed enumerations |
| TC-S6-E6008-CON-03 | AC3, AC4 | Contract | The four consumed rows, their placeholders, the manifest and the result set; the no-`recovery_case`, no-`v_ace_*` and no-`interface_config` boundary |
| TC-S6-E6008-CON-04 | AC5, AC6, AC7 | Contract | The rights, the seven fakes and the drift test; the absence of a published or consumed event, of a second topic and of a Schedule |

The six legacy cases are those of RWB-E6-008 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S6-E6008-APP or by RWB-ITG-E6008-ITG. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S6-E6008-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID; the `-ITG` copies belong to the wave 4 harness and none is written here.

### 17. Guardrails

- No business value in the contract: the entry set, the chart of accounts, the provision layout, the result codes, the posting window, the states, the item types and the lists stay data, reference data or enumeration members of a published schema, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: references, codes, amounts, dates and a rule version only; every example is synthetic.
- The account and balance facts stay with rwb-source-data and the case with rwb-case: the document declares no `v_ace_*` property, no `recovery_case` property and no case row write (BR3, BR4).
- Nothing leaves except through rwb-integration: the document declares no direct ALS endpoint, no direct general ledger endpoint and no provision file layout of its own (BR5).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S6-001 and API-S6-002 are named as the surfaces the lot builder and the data room own, never as provided here (GAP-3007).
- No retired element is reintroduced: the absence tests fail a build that declares a published or consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying (FSD S6 Requirements served, E6); the split plan carries no requirement id for this slice (GAP-3007) | The three elements, the four consumed rows and the posting item | TC-E6-008-01, TC-E6-008-02, TC-E6-008-03, TC-S6-E6008-CON-01 |
| ADR-014 | Schema and login per service | The `rwb_debtsale` login and the owned tables of 12.7 | TC-S6-E6008-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The recorded absence of an event of this step and the library object the siblings use | TC-S6-E6008-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-S6-E6008-CON-03, TC-S6-E6008-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before anything leaves | TC-S6-E6008-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-008, disposition Split (rework); feature FEAT-DBS-12 |
| Legacy criteria | AC4 owned word for word by RWB-S6-E6008-APP; AC1 to AC3 owned by RWB-ITG-E6008-ITG; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the four new contract cases TC-S6-E6008-CON-01 to -04 |
| Feature and screens | FEAT-DBS-12 Derecognize and post to the general ledger; SCR-26 Award |
| Rules | R-DS-29, R-DS-30, R-DS-31, R-DS-32 and R-DS-33, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the elements, the evaluation of R-DS-30 to R-DS-33, the record, the items and the three case moves: RWB-S6-E6008-APP.
- The cross-service journey of AC1 to AC3 and its `-ITG` copies: RWB-ITG-E6008-ITG.
- The lot operations API-S6-001 and API-S6-002 and their shapes: the lot builder and the data room stories of this service (GAP-3007).
- The award operation API-S6-003, its `DecisionLogEntry` answer and `LotAwarded`: RWB-S6-E6005-APP.
- The transfer of R-DS-29 and `AccountsTransferred`: RWB-S6-E6007-APP.
- The put-back claim, the reversal and the lot closure of R-DS-34 to R-DS-39: RWB-S6-E6009-APP; the closing of the case: RWB-S6-E6010-APP.
- The account, balance and ALS facts and the freshness of the data product: rwb-source-data (P1).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state and move answer this baseline declares as consumed and faked.
- The capability area, the rights and the scope rows: rwb-access (P4).
- The authoring, testing, approval and versioning of the DEBTSALE package and of R-DS-29 to R-DS-33: rwb-decision (P7).
- The interface identifier, transport, layout, result codes, retry schedule and exception queue of the items: rwb-integration (P2).
- The accounting rules, the chart of accounts and the entry set of ALS and of the general ledger: the ledger and Finance.
- The composite route and the screen field list of SCR-26: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
