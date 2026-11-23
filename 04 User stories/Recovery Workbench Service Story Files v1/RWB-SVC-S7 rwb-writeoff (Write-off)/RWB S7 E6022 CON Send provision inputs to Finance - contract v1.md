# RWB-S7-E6022-CON Send provision inputs to Finance - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6022-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-022 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the Finance feed slice of rwb-writeoff, split from RWB-E6-022. It fixes the provision-input, tax-file and feed-result elements and the activity answers they appear in (DP-13), the state and item vocabulary, the four consumed rows for the case state and move, the rule package in force, the tax criteria reference data and the Finance provision feed, the decision-record element of DP-03, the rights, the error envelope, the fakes and the absence tests. TSD S7 appendix T-A publishes two operations, the scan and the committee decision, and neither is a feed operation; no column of `write_off` carries a feed status, so the baseline declares no provided operation and no answer property and records both absences. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the Finance feed step of rwb-writeoff — the provision-input, tax-file and feed-result elements and the activity answers they appear in, the state and item vocabulary, the four consumed rows for rwb-case, rwb-decision and the Finance provision feed, the decision-record element, the rights, the error envelope and the fakes**, so that **the app story, the posting and reconciliation stories of this service and the wave 4 harness build against one fixed, testable contract on Day 1 and a feed element, a status, a state name or an answer shape can never drift between rwb-writeoff, rwb-case, rwb-decision and Finance without a failing build**.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy Finance feed of RWB-E6-022 crossed four boundaries at once: the posted population held in the recovery schema, a case state, a decision log and a file to Finance. The target splits them: rwb-case owns the case and its route states and publishes the reference data, rwb-decision owns the rule package and its ledger, this service owns the write-off and the decision, and Finance owns the feed. Each boundary is a contract another team builds against, so each has to be fixed before the app story starts.

The baseline also fixes the naming the checks require: schema `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff`.

Four points are carried as gaps and assumptions rather than decided quietly. TSD S7 appendix T-A publishes no feed operation and the two endpoint rows of the legacy story are the scan and the committee decision (GAP-3036; ASM-5079). No column of `write_off` carries the feed status, the feed reference, the acceptance code or the tax file reference, so the elements are activity and record elements and appear in no REST answer (GAP-3036; ASM-5080). The transport, layout, acceptance codes and retry schedule of the Finance provision feed are named by no source in the read set, and Architecture v5 slide 13 gives rwb-writeoff no call to rwb-integration and no file cell (GAP-3036; ASM-5076). And the tax criteria version is reference data behind DP-07, which the key's pattern set does not carry (GAP-3036; ASM-5075).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the `Idempotency-Key` rule and the problem-document convention are the platform baseline; where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the Ownership Map only: `write_off` is S7's, `recovery_case` and `timer` are P3's, `decision_log_entry` and `rule_row` are P7's, `role` and `permission` are P4's, `document` is P5's, and every `v_ace_*` view is P1's. This document never declares another service's table, operation or interface as its own.
- The rwb-case state read and move answer and its reference-data answer, the rwb-decision package read and the Finance provision feed are published with their fakes, so each consumed row names a real owner document; they are not in this story's contract-dependency row, which is None, and the absence is recorded (GAP-3036; ASM-5073).
- The WO rule set and its rows for R-WO-25 to R-WO-28 are governed in rwb-decision (P7); this baseline names them and declares none of them.
- `write_off` arrives with the DB story of this service, with the columns of DF-FIN-010 to DF-FIN-020; this baseline declares shapes and creates no table, no column and no migration.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). No approved baseline exists for the key — FSD S7 v3 and TSD S7 v2 stand at "In review" — so the baseline is published in Draft (realignment v1) and the release 30 April 2027 is copied unchanged and marked tentative (ASM-5081).
- The metadata wave is EP06's wave 4 and the service's Arch v5 wave is also 4, so no wave conflict arises and the baseline is a Day-1 artefact because it carries no build dependency (ASM-5082).

### 4. Flow

1. Draft the OpenAPI 3.1 fragment of rwb-writeoff for this step: the provision-input, tax-file and feed-result elements with the rights and the error responses, and no operation of its own (GAP-3036; ASM-5079).
2. Fix the elements: the write-off and case references, the amount, the tax criteria flag, the tax criteria version, the committee and posting dates, the responsibility centre, the cost centre, the GL product, the amount recovered after charge-off, the feed reference, the acceptance code, the tax file reference and the case move.
3. Fix the consumed rows: the rwb-case state read and move answer, the rwb-case reference-data read of the tax criteria version, the rwb-decision package read and the Finance provision feed, marking the fields the sources do not give with the placeholder.
4. Record the decision-record element of DP-03, written before anything leaves.
5. Record the closed vocabulary of the states and the item types, and the rule that no value is a constant of the code.
6. Record that a record, a feed item and a fake carry references, codes, amounts, dates, a boolean and a version only, and no person name, identity number, address or contact value.
7. Publish the contract tables of section 12 and the fakes of 12.8.
8. Add the contract tests: schema validation, the additive rule, the vocabulary, the shapes, the `Idempotency-Key` rule, the error envelope, the absence of a provided operation and of an answer property, the absent `recovery_case` and `v_ace_*` properties, the drift between a fake and the document, and the absence of published and consumed events of this step.
9. Tag the baseline and hand it to RWB-S7-E6022-APP, the posting and reconciliation stories of this service and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response body, a request body or an element fails schema validation | The build fails on the schema lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC7 |
| X2 | A field is renamed or removed within major version 1, or an item type changes | The contract test fails; the change needs a new major version | None | AC1, AC4 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC6 |
| X4 | A consumed row has a field list the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | A state, an item type or a value outside the declared vocabulary appears in the document or an example | The vocabulary test fails the build | None | AC2 |
| X6 | The document declares a provided operation, an answer property, or a write of another owner's row | The review fails the baseline; the boundary test fails the build | None | AC1, AC7 |
| X7 | The document declares a published or a consumed event for this step, a second topic or a Schedule | The absence test fails the build | None | AC7 |
| X8 | A person field — a name, an identity number, an address or a contact value — appears in any element, example or fake | The schema test and the review fail the baseline | None | AC2, AC6 |
| X9 | The rights of a surface are not the ones TSD S7 T6.1 declares | The access test fails the build | MSG-P4-002 | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the Ownership Map and the published owner contracts of rwb-case, rwb-decision and Finance only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the element set, the vocabulary, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S7-E6022-APP, the posting and reconciliation stories and the wave 4 harness on Day 1, and gives the Finance interface owner the one feed shape it must answer |
| Estimable | One OpenAPI fragment, nine contract tables, seven fakes and four new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the Finance feed step of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case and timer is P3, of decision_log_entry and rule_row is P7, of document is P5 and of every v_ace_* view is P1
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The provision-input, tax-file and feed-result elements are declared and no operation is claimed (new, D-RCV-60)
    Given the OpenAPI 3.1 fragment of rwb-writeoff for this step is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares the ProvisionInput element with the write-off reference, the case reference, the amount, the tax criteria flag, the tax criteria version, the committee date, the posting date, the responsibility centre, the cost centre, the GL product, the amount recovered after charge-off and the inputs as-of date, the TaxFile element with the business date, the tax criteria version, the account set and the tax criteria flag per account, and the FinanceFeedResult element with the record id, the feed reference, the acceptance code, the tax file reference, the case move and the retry count
    Then the elements are declared as the input and output of the prepareFinanceFeed and sendFinanceFeed activities on rwb-writeoff and as the decision-record payload, and it records that no published REST answer carries them because no column of write_off does (GAP-3036; ASM-5080)
    Then it declares no provided operation and records that TSD S7 T-A publishes only API-S7-001 POST /write-off-scans and API-S7-002 POST /write-offs/{writeOffId}/committee-decision, which belong to the scan and the committee stories (GAP-3036; ASM-5079)
    Then the answers 400, 401, 403, 404, 409, 422 and 503 are declared with one envelope and one message ID per condition

  Scenario: AC2 The state and item-type vocabulary is closed (new, D-RCV-60)
    Given the vocabulary section of the baseline
    When it is compared with TSD S7 T3.2, T4 and the rule rows R-WO-25 to R-WO-29
    Then the states named are PROVISION_RELEASED, FINANCE_FEED_SENT and FINANCE_FEED_REJECTED of the WRITEOFF machine, POSTED is named as R-WO-25's and PLACEMENT_DECIDED as R-WO-29's, and neither is declared here
    Then the feed item type is declared against a closed list with the values PROVISION_INPUTS and TAX_FILE, and no third value, and the names are baseline names because no source enumerates them (GAP-3036; ASM-5076)
    Then the tax criteria flag is declared as a boolean, the tax criteria version as a reference-data value read with its effective date, and TSD S7 T3.2 declares no list of values, so the baseline declares no list enumeration and records the absence (GAP-3036; ASM-5075)
    Then no state, no item type and no value is a constant of the code, and the vocabulary test fails the build on any value outside these sets
    Then no property carries a person name, an identity number, an address or a contact value, and the schema test fails any element, example or fake that adds one

  Scenario: AC3 The four consumed rows are declared with their owners and their placeholders (new, D-RCV-60)
    Given the consumed rows of the baseline
    When they are compared with the owner documents and the connection-matrix row of S7
    Then the case state read and the case-move answer are declared as consumed from P3 rwb-case, with the case reference, the route state, the write-off link and the moves FINANCE_FEED_SENT and FINANCE_FEED_REJECTED carrying the rule ID and its version
    Then the reference-data read is declared as consumed from P3 rwb-case under the default ruling for parameters and reference data, with the tax criteria version, its effective date and its criteria (GAP-3036; ASM-5075)
    Then the package read is declared as consumed from P7 rwb-decision, with the version in force and the rows R-WO-25 to R-WO-28 named and not declared
    Then the feed is declared as consumed from the Finance provision feed with the two item types, the manifest fields and the feed reference and acceptance code back, and its transport, address, layout, codes and retry schedule are Not specified in the source documents (GAP-3036; ASM-5076)
    Then the operation names of the case read, the case-move answer and the reference-data read are Not specified in the source documents (GAP-3036; ASM-5073) and the rows carry the placeholder
    Then the document declares no recovery_case, rule_row, document or v_ace_* property, and no grant on another schema

  Scenario: AC4 The feed item and its result set are fixed and the feed values stay data (new, D-RCV-60)
    Given the item section of the baseline
    When it is compared with R-WO-26 to R-WO-28 and with the Finance provision feed
    Then the manifest carries the feed reference, the business date, the provision input set, the tax file, the record reference and the Idempotency-Key, written on the singular key defined at the end of this list
    Then one feed is declared per business date and population, a rejected file is declared as held under R-WO-27 with its two-working-day timer, and a re-send is declared under R-WO-28 with the tax criteria version and the tax file reference recorded
    Then the transport, the address, the file layouts, the acceptance and rejection codes and the retry limit are declared as rows of the Finance feed configuration, read per run and named by no source in the read set (GAP-3036; ASM-5076)
    Then the document declares no file layout, no tax form and no direct Finance endpoint of its own, and records that Architecture v5 slide 13 gives rwb-writeoff no call to rwb-integration and no file cell (GAP-3036; ASM-5076)
    Then a repeated request with the same Idempotency-Key describes no second feed and answers the feed that exists

  Scenario: AC5 The decision-record element, the rights and the error envelope are fixed (new, D-RCV-60)
    Given the decision section and the access section of the baseline
    When they are compared with the library schema, TSD S7 T6.1 and the platform error envelope
    Then one record is declared per run and per case outcome with the case reference, the write-off reference, the rule ID, the package version in force, the tax criteria version, the inputs as-of date, the feed reference, the acceptance code, the tax file reference, the outcome, the reason and the decided-at time
    Then the record is written through the library on the shared rwb.decision-record.v1 before anything leaves, and a failed write leaves no feed and answers no move, with MSG-P7-003
    Then the capability area Write-off and posting and its rights are declared as consumed from P4 rwb-access, with RW-CREDITAD CRUA, RW-WRITEOFF CRU, RW-PRODHEAD RA, RW-WOCOMM RA, RW-FINANCE RA, the remaining staff roles R and SY-DATALOAD U as TSD S7 T6.1 gives them
    Then a refused caller answers 403 with MSG-P4-002, and the feed and the re-send run under the service identity because the feature's primary use is 'None; runs unattended' and the Finance and CFO delegate is its also-user (GAP-3036; ASM-5079)
    Then the document declares no decision_log_entry column and no rule_row column as its own

  Scenario: AC6 The fakes answer the document and the drift test holds (new, D-RCV-60)
    Given the fakes of the baseline
    When each is compared with the operation or the element it serves
    Then the rwb-case fake answers a case at PROVISION_RELEASED, an accepted move and a refused move for each of FINANCE_FEED_SENT and FINANCE_FEED_REJECTED, a case at POSTED and a case that has left the population
    Then the reference-data fake answers the tax criteria version in force with its effective date and a state with no version in force, the rwb-decision fake answers the WO rule set at its version with R-WO-25 to R-WO-28, and the rwb-access fake answers the capability area with and without the right
    Then the Finance feed fake answers one feed accepted with its reference and acceptance code, one file rejected with its code, one re-send accepted with the tax file reference and no answer beyond 2 s
    Then the decision-record stub answers a healthy chain and a stopped chain, and the composite route fake answers the merged SCR-27 write-off proposal screen for write-off WO-2026-000042
    Then every fake carries references, codes, amounts, dates, a boolean and a version only, with no person name, identity number, address or contact value, and the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC7 The naming baseline and the boundary are fixed and this step publishes and consumes no event (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the Ownership Map, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the topic is rwb.writeoff.events.v1, the queue is rwb-writeoff and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then 12.1 is None and records that no operation is provided and that API-S7-001 and API-S7-002 belong to the scan and the committee stories
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, timer, role, permission, document, decision_log_entry, rule_row and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event for this step, and records that WriteOffApproved (EV-24) is the approval story's and AceDataReady (EV-26) is the scan's
    Then the document declares no Schedule and records that the month-end close of R-WO-26 is a durable timer of WriteOffWorkflow (GAP-3036; ASM-5078)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6022-APP and they copy no criterion of the legacy story, whose AC1, AC2 and AC3 stay with the app story word for word.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off and its population are rwb-writeoff's, and the contract declares their fields as read by this step only | Architecture v5 slide 4; TSD S7 T3.1 |
| BR2 | The decision record is declared as an element written before anything leaves, through the local library on the shared topic; a failed write leaves no feed and answers no move | DP-03; TSD S7 T2; legacy AC3 |
| BR3 | The case state and the case move stay with rwb-case: the contract declares the read and the two moves, and declares no `recovery_case` property and no case row write | Ownership Map (recovery_case owner P3); ASM-5073 |
| BR4 | The tax criteria version is reference data read with its version, declared as one consumed row, never a schema default and never a constant | R-WO-03; FSD S7 A2.10.3.1; ASM-5075 |
| BR5 | The feed leaves only through the Finance provision feed: the contract declares one feed read with two item types and the result back, and no direct Finance endpoint, no second channel and no local file layout | R-WO-26 (Systems column); ASM-5076 |
| BR6 | This baseline declares no provided operation: the step runs unattended behind the workflow and no answer of the service carries a feed field | TSD S7 T-A.1; GAP-3036; ASM-5079 |
| BR7 | A POST of a feed declares the `Idempotency-Key`; one feed per business date and population, and one re-send per cleared rejection; a GET declares none | Architecture v5 slide 11; TSD S7 T-A.2; R-UNI-40 |
| BR8 | The vocabulary is closed: the three states and the two item types are published as enumerated values, TSD S7 T3.2 declares no list of values, and no value is a constant of the code | TSD S7 T3.2, T4; FSD S7 BR-S7-010; GAP-3036 |
| BR9 | No personal data in a schema, an example or a fake: a record and a feed item carry references, codes, amounts, dates, a boolean and a version only | Template and Rules v1 §R7.2 (s17); FSD S7 A1.4 |
| BR10 | One REST base, one topic, one queue and one login per service; the document never declares another service's base, topic or queue as its own | DP-13; Template and Rules §R4 |
| BR11 | A schema change is additive within major version 1; a breaking change, including a change of an item type or of a state name, is a new major version | Architecture v5 slide 42 notes (BACKWARD compatibility) |
| BR12 | The feed identifier, transport, layout, acceptance codes and retry limit are Finance's configuration rows, named here and declared nowhere here | GAP-3036; ASM-5076 |
| BR13 | The feed status, the feed reference, the acceptance code and the tax file reference have no column in TSD S7 T3.1, so the record and the case state carry them and this baseline adds no column and no migration | GAP-3036; ASM-5080 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The elements, the vocabulary, the consumed rows and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the posting and reconciliation stories, the wave 4 harness and the rwb-case, rwb-decision and Finance owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property is added within major version 1, for example an optional result field | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, an item type or a state name changes, or a provided operation is added | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence tests of AC1 and AC7 fail: a provided operation, an answer property, a `recovery_case` or `v_ace_*` property, an event or a Schedule | In review |

The route state machine the document describes is the app story's: a case whose provision is released is fed to Finance, held on a rejected file, or re-sent once the file is accepted. This baseline fixes the vocabulary of those states and moves no case.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI fragment and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the Ownership Map rows the baseline consumes, including the absent feed operation and the absent feed column |
| Consuming teams (the app story, the posting and reconciliation stories, the wave 4 harness and the owners of rwb-case, rwb-decision, rwb-access and the Finance provision feed) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Finance interface owner | Owns the feed identifier, its transport, its layouts, its acceptance codes and its retry limit the items obey |
| Data steward | Confirms that no personal data field is declared in an element, an answer or a fake |

The per-service login behind the security scheme of the document is named "the rwb_writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Provision input element | The write-off reference, the case reference, the amount, the tax criteria flag, the tax criteria version, the committee date, the posting date, the responsibility centre, the cost centre, the GL product, the amount recovered after charge-off and the inputs as-of date |
| Tax file element | The business date, the tax criteria version, the account set with the tax criteria flag per account, and the file reference |
| Finance feed result element | The record id, the feed reference, the acceptance code, the tax file reference, the case move and the retry count |
| Write-off shapes | The columns DF-FIN-010 to DF-FIN-020 as the step reads them; the absent feed columns are recorded (GAP-3036; ASM-5080) |
| Case facts | The case reference, the route state and the write-off link of P3 rwb-case, read only through the owner's contract (DF-CAS-001 to DF-CAS-023) |
| States and item types | `PROVISION_RELEASED`, `FINANCE_FEED_SENT`, `FINANCE_FEED_REJECTED`; the item types `PROVISION_INPUTS` and `TAX_FILE`, as baseline names |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before anything leaves (DP-03) |
| Not declared here | `recovery_case` and `timer` (P3), `role` and `permission` (P4), `document` (P5), `decision_log_entry` and `rule_row` (P7), and every `v_ace_*` view (P1) |
| Consumed fields with no source | The three operation names, the feed identifier, its transport, address, layouts, acceptance codes and retry limit: Not specified in the source documents (GAP-3036; ASM-5073, ASM-5076) |

The field-level types, lengths and required flags of the elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the additive rule of BR11. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None of its own. TSD S7 appendix T-A publishes two operations for the module: API-S7-001 `POST /write-off-scans` (right C) and API-S7-002 `POST /write-offs/{writeOffId}/committee-decision` (right A), and neither of them is a Finance feed operation. The two endpoint rows of the legacy story are those two operations; they are the scan's and the committee decision's, and the feed outcome is read from the case state of rwb-case and from the record of this service behind the composite route. This baseline therefore declares no operation as provided, records the two sibling rows by name, and fixes only the elements and the activity answers of the step. The absence is recorded as GAP-3036 with ASM-5079.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference, its route state and its write-off link; faked |
| The case-move answer (operation name Not specified in the source documents (GAP-3036; ASM-5073)) | rwb-case (P3) | P3 rwb-case | The moves `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED` with the rule ID and its version; faked |
| The reference-data read (operation name Not specified in the source documents (GAP-3036; ASM-5075)) | `/api/recovery/case/v1` | P3 rwb-case | The tax criteria version in force, its effective date and its criteria; faked |
| The rule package in force (read) | `/api/recovery/decision/v1` | P7 rwb-decision | The WO rule set at its version with R-WO-25 to R-WO-28; faked |
| The Finance provision feed (interface values Not specified in the source documents (GAP-3036; ASM-5076)) | Finance provision feed, outside the 19 services | Finance | The provision input set and the tax file in; the feed reference and the acceptance code out; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four reads and the feed call are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3036 with ASM-5073.

#### 12.3 Events published

None. Architecture v5 and the event catalogue give rwb-writeoff the topic `rwb.writeoff.events.v1` and one event, `WriteOffApproved` (EV-24, payload `writeOffId`, `caseId`, `amount`, consumer "Posting"), which belongs to the committee approval story (RWB-S7-E6018-APP). No finance-feed or provision event exists, so the baseline declares no event of its own, no outbox row and no producer, and the absence test of AC7 fails a build that adds one (ASM-5077).

#### 12.4 Events consumed

None. The connection matrix gives rwb-writeoff listeners on rwb-payment's and rwb-source-data's events, which belong to the post charge-off payment story and the scan (`AceDataReady`, EV-26, whose consumers include the write-off scan JOB-16), and no event of the module carries a feed or a provision answer. This baseline therefore declares no consumer group, no subscription, no inbox of its own and no Kafka call from this step, and the absence test of AC7 fails a build that adds one (ASM-5077).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case, the child of `CaseWorkflow` on rwb-case (P3), which continues-as-new across the committee, posting, Finance feed and post charge-off window | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the two steps; its signals and its outcome for the parent are declared, not built |
| `prepareFinanceFeed` | Activity, the R-WO-26 step | `rwb-writeoff` | In: the business date, the population, the case state, the tax criteria version and the package in force. Out: the provision input set, the tax file, the rule ID with its version, the record id and the `FINANCE_FEED_SENT` move |
| `sendFinanceFeed` | Activity, the R-WO-27 and R-WO-28 step | `rwb-writeoff` | In: the two items and the manifest. Out: the feed reference, the acceptance code, the tax file reference, the record id and the `FINANCE_FEED_SENT` or `FINANCE_FEED_REJECTED` move |

No child workflow for the case and none for the money exists in this service. The activity names are target design choices and the trigger is the provision release of R-WO-25 and the month-end close of R-WO-26. No activity is registered by this story, and the scan, the committee, the posting, the reconciliation and the post charge-off steps belong to the sibling stories of this service.

#### 12.6 Schedules

None. R-WO-26 carries "month-end close" in its timer column and the service's one job row is the scan's (JOB-16), so the wait is a durable timer inside `WriteOffWorkflow`. This baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table (GAP-3036; ASM-5078).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off, its population and its GL-facing columns; read by this step, which changes no column (GAP-3036; ASM-5080) |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of each rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the business date, the population and each feed |
| outbox_event | PLT library, created in `rwb_writeoff` | The library object the service's sibling stories relay their events through; this step declares no row |

`recovery_case` and `timer` (P3), `role` and `permission` (P4), `document` (P5), `decision_log_entry` and `rule_row` (P7) and every `v_ace_*` view (P1) are not owned by this baseline; it names them only as answers, rule versions or another story's table, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case state and move fake | A case at `PROVISION_RELEASED` and one at `POSTED`; an accepted move and a refused move for each of `FINANCE_FEED_SENT` and `FINANCE_FEED_REJECTED` | AC3, AC6 |
| Reference-data fake of rwb-case | The tax criteria version in force with its effective date; a state with no version in force | AC3, AC6 |
| rwb-decision rule-package fake | The WO rule set at its version in force with R-WO-25 to R-WO-28 | AC3, AC6 |
| Finance provision feed fake | One feed accepted with its reference and acceptance code, one file rejected with its code, one re-send accepted with the tax file reference, one manifest refused and no answer beyond 2 s | AC4, AC6 |
| rwb-access authorise fake | The capability area "Write-off and posting" with its rights for the TSD S7 T6.1 roles; a caller without the right | AC5, AC6 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain and a stopped chain | AC5, AC6 |
| gateway-bff composite route fake | The merged SCR-27 answer for write-off WO-2026-000042, carrying the case state once | AC1, AC6 |

The fakes are test-only and are replaced by the real services and the real Finance interface in SIT. The three operation names and the feed values are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3036; ASM-5073, ASM-5076).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-case state read and move answer, the rwb-case reference-data read and the rwb-decision package read; one hop, 2 s; plus the Finance feed call |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval story's and `AceDataReady` (EV-26) is the scan's |
| Temporal | 1 workflow and 2 activities declared, 0 registered | `WriteOffWorkflow`, `prepareFinanceFeed` and `sendFinanceFeed` on `rwb-writeoff`; no Schedule |
| File | 1 declared | The provision input set and the tax file are file items of the Finance feed; this baseline fixes a manifest, not a layout |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no write-off, no case and no rule package. What it publishes is one OpenAPI 3.1 fragment, nine contract tables, seven fakes and four new contract tests.

**Deliverables.** The additive fragment `openapi/rwb-writeoff-v1.yaml` for the three elements, the vocabulary of the three states and the two item types as published enumerations, the contract README rows for the five consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction rule the record element describes: the record and the feed outcome commit together or not at all. DP-13 fixes the base and this baseline adds no operation to it. DP-19 is behind SCR-27, whose screen model is the edge contract's. The two H rows of the table are the ones the metadata carries, and the five consumed rows are class C in fact while the plan's C row is None (GAP-3036; ASM-5073). DP-07 and DP-16 are absent from the key's pattern set although the tax criteria version is reference data and the feed is external; both are recorded (ASM-5075, ASM-5076).

**Build steps**

1. Write the three elements and the no-provided-operation record of AC1, and validate the additive rule in the pipeline.
2. Write the vocabulary of AC2 and the two item types as published enumerations with the no-constant rule and the no-list record.
3. Record the four consumed rows of AC3 with their owners, their budget and their placeholders.
4. Record the feed item, its result set and the configuration values of AC4.
5. Record the decision-record element, the rights and the error envelope of AC5.
6. Publish the seven fakes of AC6 and the drift test.
7. Record the naming baseline, the boundary, the absence of events and of a Schedule of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI fragment validates in the pipeline, the four contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the posting and reconciliation stories and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set; it names the tax criteria hold, which gates the tax file (BR4) | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a manifest is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the surface declares | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before anything leaves | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| None | The Finance feed rejects a file; the row is Finance's | Not specified in the source documents (GAP-3036; ASM-5076) |

The four named message IDs are contract elements and the text is the legacy and FSD wording, copied unchanged; no message is reworded and no new one is invented. The rejection row is carried because a rejected feed is read from Finance's own row, which no source in the read set gives.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its scan, proposed, in-committee and approved readings plus the feed readings, all read only, through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off and its feed outcome and rwb-case for the case and its route state; this baseline fixes the elements and the case state the screen reads, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The refused, not-recorded, rejected and held readings the app story shows use the messages of section 14 on the same route. The legacy screen table gives no screen for the feed, so this baseline adds no screen and no field list of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-022-01 | AC1, AC2 | Contract | Write-offs WO-2026-000042 and WO-2026-000043; the contract half answers the three elements, the no-provided-operation record and the state and item vocabulary |
| TC-E6-022-02 | AC3, AC5 | Contract | The case fake at `PROVISION_RELEASED`; the contract half answers the rwb-case row, the reference-data row, its placeholders and the `FINANCE_FEED_SENT` move shape |
| TC-E6-022-03 | AC4 | Contract | A feed accepted and a file rejected with its code; the contract half answers the manifest, the result set and the held and re-sent shapes |
| TC-E6-022-04 | AC5, AC6 | Contract | RW-CREDITAD holds CRUA and RW-FINANCE holds RA; the contract half answers the rights of the capability area |
| TC-E6-022-05 | AC5, AC6 | Contract | The record stub stopped; the contract half answers the MSG-P7-003 path, the decision-record element, the fakes and the drift test |
| TC-S7-E6022-CON-01 | AC1 | Contract | The fragment validates; the three elements, the seven error answers and the no-provided-operation and no-answer-property records are present |
| TC-S7-E6022-CON-02 | AC2 | Contract | The three states and the two item types validate as closed enumerations, and the no-list record is present |
| TC-S7-E6022-CON-03 | AC3, AC4 | Contract | The four consumed rows, their placeholders, the manifest and the result set; the no-`recovery_case`, no-`v_ace_*` and no-`document` boundary |
| TC-S7-E6022-CON-04 | AC5, AC6, AC7 | Contract | The rights, the seven fakes and the drift test; the absence of a published or consumed event, of a second topic and of a Schedule |

The five legacy cases are those of RWB-E6-022 in their legacy order, carried as the contract half: their Covers column names the criteria of this story that fix the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6022-APP. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The four cases `TC-S7-E6022-CON-01` to `-04` are new. The full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID; no `-ITG` copy is written here, because the plan splits this key to no integration story.

### 17. Guardrails

- No business value in the contract: the feed layout, the tax file layout, the acceptance and rejection codes, the retry limit, the month-end close, the states, the item types and the tax criteria version stay data, reference data or enumeration members of a published schema, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: references, codes, amounts, dates, a boolean and a version only; every example is synthetic.
- The case stays with rwb-case and the ACE facts with rwb-source-data: the document declares no `recovery_case` property, no `v_ace_*` property and no case row write (BR3).
- Nothing leaves except through the Finance provision feed: the document declares no direct Finance endpoint, no second channel and no local file layout of its own (BR5).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No operation of a sibling is claimed: API-S7-001 and API-S7-002 are named as the surfaces the scan and the committee stories own, never as provided here (GAP-3036).
- No retired element is reintroduced: the absence tests fail a build that declares a published or consumed event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (FSD S7 Requirements served, E6); the split plan carries no requirement id for this slice (GAP-3036) | The three elements, the four consumed rows and the feed item | TC-E6-022-01, TC-E6-022-02, TC-S7-E6022-CON-01 |
| ADR-014 | Schema and login per service | The `rwb_writeoff` login and the owned tables of 12.7 | TC-S7-E6022-CON-03 |
| ADR-015 | Kafka with outbox, inbox and CloudEvents | The recorded absence of an event of this step and the library object the siblings use | TC-S7-E6022-CON-04 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The five consumed rows with their budget and breaker | TC-E6-022-02, TC-S7-E6022-CON-03 |
| ADR-022 | Local decision record plus central ledger | The decision-record element written before anything leaves | TC-S7-E6022-CON-04 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-022, disposition Split (rework); feature FEAT-WOF-10; module S7 Write-off and recovery |
| Legacy criteria | AC1, AC2 and AC3 owned word for word by RWB-S7-E6022-APP; this baseline copies none of them |
| Test cases | The five legacy cases as the contract half, and the four new contract cases TC-S7-E6022-CON-01 to -04 |
| Feature and screens | FEAT-WOF-10 Send provision inputs to Finance; SCR-27 Write-off proposal |
| Rules | R-WO-25, R-WO-26, R-WO-27 and R-WO-28, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (outbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the elements, the evaluation of R-WO-26 to R-WO-28, the record, the feed items and the case moves: RWB-S7-E6022-APP.
- The scan operations API-S7-001 and the committee decision API-S7-002 and their shapes: RWB-S7-E6013-CON and RWB-S7-E6018-CON (GAP-3036).
- The posting of the write-off and the provision release of R-WO-25: RWB-S7-E6021-APP; the reconciliation of the approved and posted populations: RWB-S7-E6023-APP.
- The write-off exception loop of R-WO-24, R-WO-41 and R-WO-43 to R-WO-46: RWB-S7-E6024-APP.
- The post charge-off treatment of R-WO-29 and later, the closing of the case and the retention period: the post charge-off stories of this service.
- The write-off and its GL-facing columns beyond the shapes this step reads: the DB story of rwb-writeoff (DF-FIN-010 to DF-FIN-020).
- The case of record, its route states and the parent `CaseWorkflow`: rwb-case (P3), whose state, move and reference-data answers this baseline declares as consumed and faked.
- The capability area, the rights and the scope rows: rwb-access (P4).
- The authoring, testing, approval and versioning of the WO rule set and of R-WO-25 to R-WO-28: rwb-decision (P7).
- The Finance provision feed — its identifier, transport, address, layouts, acceptance codes, retry limit and exception queue: Finance.
- The documents of the case and the storage of the tax file: rwb-document (P5).
- The composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
