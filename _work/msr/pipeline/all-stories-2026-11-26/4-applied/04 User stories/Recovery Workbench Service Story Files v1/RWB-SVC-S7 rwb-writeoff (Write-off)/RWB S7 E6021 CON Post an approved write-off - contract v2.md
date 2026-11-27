# RWB-S7-E6021-CON Post an approved write-off - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S7-E6021-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-writeoff |
| Service epic | RWB-SVC-S7 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | CG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S7 rwb-writeoff v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract baseline of the posting feature of rwb-writeoff, split from RWB-E6-021 (FEAT-WOF-09). It fixes the `write_off` element and its DF-FIN fields, the WRITEOFF state vocabulary including the POSTING values, the consumed rwb-source-data account, asset and ledger rows, the consumed rwb-case state and move answers, the consumed rwb-decision package row, the prepared-posting-pack element that the ALS and general-ledger crossing consumes, the decision-record element of DP-03, the rights, the fakes and the absence tests, on the base `/api/recovery/writeoff/v1` (DP-13) behind the gateway-bff composite route (DP-19). It provides no REST operation: the two operations of this legacy key are RWB-S7-E6013-APP's and RWB-S7-E6018-APP's, the plan's C and X rows are empty while the step consumes rwb-source-data, rwb-case and rwb-decision, and the ALS and general-ledger interface is published in no source (GAP-3034; ASM-5067, ASM-5070, ASM-5071). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-S7-E6021-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the posting feature of rwb-writeoff — the `write_off` element with its DF-FIN fields and the WRITEOFF state vocabulary including the POSTING values, the consumed rwb-source-data account, asset and ledger rows, the consumed rwb-case state and move answers, the consumed rwb-decision package row, the prepared-posting-pack element, the decision-record element, the rights, the tables and the fakes**, so that **the app story, the SCR-27 fragment, the wave 4 harness and the posting track build against one fixed, testable contract on Day 1, and a field, a state value, a consumed shape or a pack element can never drift between rwb-writeoff, rwb-source-data, rwb-case and rwb-decision without a failing build**.

The baseline is deliberately narrow: it declares one element of this service, one composition element for the posting track and the boundaries the feature crosses. It declares no operation, no event and no Schedule of its own, and it declares nothing of the ALS and general-ledger interface.

### 2. Business rationale

Contract-first REST with one hop and a 2 s timeout is the decoupling decision (DP-11, ADR-020). The legacy posting of RWB-E6-021 crossed four boundaries at once — ACE account and asset data, the case state, the rule package and the general ledger — inside one process and one schema. The target splits them: rwb-source-data owns the `recovery.v_ace_*` views and the interaction ledger, rwb-case owns the case and its route states, rwb-decision owns the rule package and the ledger, and rwb-writeoff owns the write-off row. Each boundary is now a contract another team builds against, so each has to be fixed before the app story starts: the `write_off` fields, the WRITEOFF state values the pack and the posting use, the source-data reads, the case state read and move answer, the package row, and the pack the posting is made from.

The baseline also fixes the naming the checks require: schema `rwb_writeoff`, login `rwb_writeoff`, base `/api/recovery/writeoff/v1`, topic `rwb.writeoff.events.v1` with its retry and `.dlt` topics, task queue `rwb-writeoff` in namespace `rwb-recovery` and Java package `th.co.scb.ace.workbench.recovery.writeoff` (Template and Rules v1 §R4; context pack service row). It records that rwb-writeoff holds no grant on `rwb_case`, `rwb_source_data` or `rwb_decision` and no `v_ace_*` grant, so those are consumed on their owners' contracts only (DP-01, DP-05).

Four points are carried as gaps and assumptions rather than decided quietly: the plan's C and X rows are empty while the step consumes three services and most consumed operation names are unpublished (GAP-3034), the feature provides no operation because the key's two operations belong to other stories (ASM-5071), the state values of the legacy criteria are read as the WRITEOFF state on `write_off.state` while the case route state is answered to rwb-case (ASM-5037), and the ALS and general-ledger interface that FEAT-WOF-09 names has no published definition in any source (ASM-5070).

The wave and the date are the plan's and the legacy epic's: this key is EP06, wave 4, release 30 April 2027, and rwb-writeoff is created in wave 4, so the two agree and the date is copied unchanged and marked tentative (ASM-5035).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the base, the topic, the queue and the event names follow the platform rule rather than a local choice.
- The platform error envelope, the pagination and filter convention and the `Idempotency-Key` rule are the platform baseline (Architecture v5 slide 11); where this document narrows them it does so explicitly.
- The ownership of the objects is taken from the context pack and the Ownership Map only: `write_off` is S7's, `recovery_case` is P3's, `account_ext`, `interaction` and the `v_ace_*` views are P1's, `rule_row` and `decision_log_entry` are P7's, `document` is P5's, `notice` is P6's. This document never declares another service's table or operation as its own.
- The rwb-source-data, rwb-case and rwb-decision rows are published with their fakes, so each consumed row names a real owner document; they are not in this story's dependency rows, which are None, and the absence is recorded (GAP-3034; ASM-5067).
- The WO rule package and its row R-WO-05 are governed in rwb-decision (P7); this baseline names the row and declares none of it.
- The `write_off` table and its columns arrive with the DB story of this service; this baseline declares shapes and creates no table, no column and no migration.
- The pack element and the pack document reference are RWB-S7-E6015-APP's; this baseline declares how the posting track composes the prepared pack and builds no second pack (ASM-5068).
- The two operations of this legacy key, API-S7-001 and API-S7-002, are outside this baseline and belong to RWB-S7-E6013-APP and to RWB-S7-E6018-APP to -E6020-APP (ASM-5071).
- No build dependency: this story is Day 1 by rule (Template and Rules v1 §R5.7).

### 4. Flow

1. Draft the OpenAPI 3.1 document of rwb-writeoff for this feature and record that it declares no operation for it, with the two operations of the key named as other stories'.
2. Fix the `write_off` element: the properties of DF-FIN-010 to DF-FIN-020 with their types, lengths, required flags and the state each value is declared against.
3. Fix the WRITEOFF state vocabulary of TSD S7 T4, including `PACK_PREPARED`, `POSTING_PENDING`, `POSTED`, `POSTING_REJECTED`, `WRITEOFF_EXCEPTION` and `PROVISION_RELEASED`, and mark the values the table does not print with the placeholder.
4. Fix the consumed rwb-source-data rows: the account and asset read and the interaction-ledger read, with the placeholder on the names the sources do not publish.
5. Fix the consumed rwb-case rows: the state read and the case-move answer, with the placeholder on the move name.
6. Fix the consumed rwb-decision row: the WO package version in force with R-WO-05.
7. Record the prepared-posting-pack element — the five pack facts and the record reference the posting track consumes — and the decision-record element of DP-03, written before the `write_off` row changes.
8. Record that the ALS and general-ledger interface is declared nowhere: no field, no file layout, no reference shape and no error set, and the integration story owns it.
9. Publish the contract tables of section 12, the rights and the fakes of 12.8.
10. Add the contract tests: schema validation, the additive rule, the vocabulary, the element shapes, the error set, the rights, the drift between a fake and the document, the absence of an operation, of an event, of a Schedule and of a foreign table; then tag the baseline and hand it to RWB-S7-E6021-APP, the SCR-27 fragment and the wave 4 harness.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A body fails schema validation or an element carries a value outside the state vocabulary | The build fails on the schema and vocabulary lint; a deployed service answers 400 or 500 with the error envelope | MSG-GEN-001 | AC1, AC2, AC6 |
| X2 | A field is renamed or removed within major version 1, or a state value changes | The contract test fails; the change needs a new major version | None | AC2 |
| X3 | A contract fake drifts from the document | The drift test fails the build and the merge is blocked | None | AC5 |
| X4 | A consumed row has a field list or a name the sources do not give | The row carries the placeholder, the gap and the assumption, and the fake is derived from the published document | None | AC3, AC4 |
| X5 | The document declares an operation, an event, a Schedule, another service's object or an ALS or general-ledger element as its own | The absence test and the boundary test fail the build | None | AC1, AC6, AC7 |
| X6 | The rights of the read and of the consumed acts are not the ones TSD S7 T6.1 and T-A.1 declare | The access test fails the build | MSG-P4-002 | AC6 |
| X7 | The prepared pack is declared with a field the pack story does not publish, or with a second pack builder | The review fails the baseline; the pack element carries the placeholder and names RWB-S7-E6015-APP | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the context pack and the published owner contracts of rwb-source-data, rwb-case and rwb-decision only |
| Negotiable | The element names beyond the ones the sources give, the example values and the fake fixtures are settled in the baseline review; the fields, the state values, the base, the topic and the queue are fixed by the target architecture |
| Valuable | Unblocks RWB-S7-E6021-APP, the SCR-27 fragment, the wave 4 harness and the posting track on Day 1, and the rwb-source-data, rwb-case and rwb-decision teams on the same day |
| Estimable | One OpenAPI document, nine contract tables, seven fakes and seven new contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Contract baseline of the posting feature of rwb-writeoff

  Background:
    Given the service naming rule of the platform library is in force
    Given the ownership of write_off is S7, of recovery_case is P3, of account_ext, interaction and the v_ace_* views is P1 and of rule_row and decision_log_entry is P7
    Given every consumed contract is the published contract of its owner and is answered by its fake

  Scenario: AC1 The baseline provides no operation for the pack-prepared step and records the key's two operations as other stories' (new, D-RCV-60)
    Given the OpenAPI 3.1 document of rwb-writeoff is published with this change
    When it is validated against the OpenAPI 3.1 schema
    Then it validates with no error
    Then it declares no operation whose behaviour is the pack-prepared step of the posting track
    Then it records POST /write-off-scans (API-S7-001) as RWB-S7-E6013-APP's and POST /write-offs/{writeOffId}/committee-decision (API-S7-002) as RWB-S7-E6018-APP's with the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP (ASM-5071)
    Then the stage read behind SCR-27 carries the placeholder, with an error set of 400, 401, 403 with MSG-P4-002, 404 and 503 and one message ID per condition
    Then the absence test fails a build that declares a pack-prepared operation, a second base or a second topic

  Scenario: AC2 The write_off element and the WRITEOFF state vocabulary are declared (new, D-RCV-60)
    Given the write-off section of the baseline
    When it is compared with TSD S7 T3.0, T3.1 and T4 and with the API Specification's WriteOff element
    Then the write_off element declares the properties of DF-FIN-010 to DF-FIN-020: id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product and recovered_after
    Then id, case_id, amount, tax_criteria_met and recovered_after are required and the other six are optional, responsibility_center, cost_center and gl_product are strings of at most 10 characters, amount and recovered_after are numeric(18,2) and the two dates are dates
    Then state is declared as the standard record column of TSD S7 T3.0 with the WRITEOFF values SCAN_DUE, SCAN_HELD, POPULATION_PROPOSED, PACK_PREPARED, PACK_INCOMPLETE, WITH_COMMITTEE, CASE_REMOVED_BY_TEAM, ESCALATED_TO_CREDIT_COMMITTEE, APPROVED, RETURNED_TO_PURSUE, DEFERRED, POSTING_PENDING, POSTED, POSTING_REJECTED, WRITEOFF_EXCEPTION, PROVISION_RELEASED, RETENTION_RUNNING and CASE_CLOSED, and the values of the 27-state machine that T4 does not print carry the placeholder (GAP-3034; ASM-5037)
    Then the element records that posted_date is written once ALS and the general ledger answer, and is written by no operation of this feature (ASM-5070)

  Scenario: AC3 The consumed rwb-source-data rows are declared (new, D-RCV-60)
    Given the consumed rows and the source-data boundary of the baseline
    When they are compared with rwb-source-data as the owner of account_ext, the interaction ledger and the recovery.v_ace_* views
    Then the account and asset read is declared as consumed from P1 rwb-source-data with the account reference, the balance, the provision carried and the asset facts of the case, and its operation name is Not specified in the source documents (GAP-3034; ASM-5067)
    Then the route-history read is declared as consumed from P1 on the interaction ledger of DF-INT-001 to DF-INT-013, its name is Not specified in the source documents, and the ledger is recorded as P1's under the default ruling (DP-18)
    Then the document records that v_ace_account (DF-ACE-001 to DF-ACE-042) and v_ace_npa_asset (DF-ACE-208 to DF-ACE-219) are P1's views, that only rwb-source-data holds SELECT on them, and that this service holds no v_ace_* grant (DP-01, DP-05)
    Then the document declares no ACE table property and no v_ace_* path, and each consumed row is one hop with a 2 s budget and a breaker (DP-11, ADR-020)

  Scenario: AC4 The consumed rwb-case state and move rows and the rwb-decision package row are declared (new, D-RCV-60)
    Given the consumed rows of the case boundary and the rule package
    When they are compared with rwb-case as the owner of recovery_case and with rwb-decision as the owner of rule_row
    Then the case state read is declared as consumed from P3 rwb-case on the GET /cases/{caseId} family, with the case reference and the state of the write-off stage
    Then the case-move answer is declared as consumed from P3 with the move PACK_PREPARED carrying the rule ID and its version, its operation name is Not specified in the source documents, and the connection matrix row S7 is recorded as having no REST edge to P3 (ASM-5037)
    Then the WO rule package version in force is declared as consumed from P7 rwb-decision with the row R-WO-05 and the reference data the pack reads, reached as an activity on that owner's queue, and its operation name is Not specified in the source documents (GAP-3034; ASM-5067)
    Then the document declares no recovery_case property, no rule_row property and no ledger entry of its own, and records that DP-04 is not in this key's pattern set

  Scenario: AC5 The prepared-posting-pack element and the fakes answer the document (new, D-RCV-60)
    Given the pack section and the fakes of the baseline
    When each is compared with the pack element of RWB-S7-E6015-APP and with the element it serves
    Then the prepared-posting-pack element declares the case reference, the write-off reference, the balance, the provision carried, the route history, the legal state, the asset state, the residual and the decision-record reference
    Then the element is declared as composed from the pack and the source-data answers at the package version in force, and it records that the pack builder, the document index and the agent run are RWB-S7-E6015-APP's and the rwb-agent's (ASM-5068)
    Then the element declares no ALS field, no general-ledger field, no posting reference and no file layout, and records that the crossing is RWB-ITG-E6021-ITG's (ASM-5070)
    Then the rwb-source-data fake answers the balance, the provision carried, the asset facts and the route history, a stale product and a missing fact; the rwb-case fake answers the two states and an accepted and a refused move; the rwb-decision fake answers the package with R-WO-05
    Then the drift test compares every fake with the document and fails the build on any difference

  Scenario: AC6 The rights, the roles, the scope and the decision record are fixed (new, D-RCV-60)
    Given the access and decision sections of the baseline
    When they are compared with TSD S7 T6.1, T-A.1, the legacy permission rows and the library schema
    Then the read declares Write-off and posting right R with the scope applied, RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, and RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA
    Then the document records the legacy A holders RW-CREDITAD, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE and the legacy C holders RW-WRITEOFF and RW-CREDITAD, and declares no A right on an operation of this story (ASM-5071)
    Then one decision record is declared per rule outcome with the case reference, the write-off reference, the rule ID, the package version in force, the inputs reference, the five pack facts, the outcome and the decided-at time, written through the library on the shared rwb.decision-record.v1 before the write_off row changes, with a failed write leaving the row unchanged with MSG-P7-003 (DP-03; ASM-5040)
    Then the document records that write_off.decision_log_id carries the local record and that the P7 ledger entry identifier is not stored here (ASM-5040)
    Then a role without the right is refused with MSG-P4-002 and the access test fails a build whose rights differ

  Scenario: AC7 The naming baseline and the boundary are fixed and nothing is published or scheduled (new, D-RCV-60)
    Given the naming and data sections of the baseline
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present and names its owner from the context pack and the Ownership Map, with None where the element is empty
    Then the schema is rwb_writeoff, the login is rwb_writeoff, the base is /api/recovery/writeoff/v1, the topic is rwb.writeoff.events.v1, the queue is rwb-writeoff and the Java package is th.co.scb.ace.workbench.recovery.writeoff
    Then the tables named as owned are write_off and the library objects decision_record, idempotency_key and outbox_event, and recovery_case, account_ext, interaction, rule_row, decision_log_entry, document, notice and every v_ace_* view are named as other owners' and are consumed only through their contracts
    Then the document declares no published event and no consumed event, and names WriteOffApproved (EV-24) as RWB-S7-E6018-APP's (ASM-5069)
    Then the document declares no Schedule, no Quartz row and no shared job table, and names JOB-16 as RWB-S7-E6013-APP's and the posting and close windows as RWB-ITG-E6021-ITG's and the package's (ASM-5070)
    Then the document records that the plan's C and X rows are empty although the step consumes three services, and that the S7 module files were read from the extract folder (GAP-3034; ASM-5067)
```

These seven criteria are new for the contract baseline and test the artefact only. They restate no business outcome owned by RWB-S7-E6021-APP and they copy no criterion of the legacy story, whose AC2 and AC4 stay with the app story word for word and whose AC1 and AC3 stay with RWB-ITG-E6021-ITG.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-off row and its state are rwb-writeoff's, and the contract declares their fields and state values on the `write_off` element only | Context pack ownership row `write_off`; TSD S7 T3.0 and T3.1; DP-01 |
| BR2 | The decision record is declared as an element written before the row changes, through the local library on the shared topic; a failed write changes nothing | DP-03; TSD S7 T2; legacy RWB-E6-021 AC2 and AC4 |
| BR3 | The ACE account, asset and ledger facts stay with rwb-source-data: the contract declares the reads as consumed and declares no ACE property and no `v_ace_*` path | DP-05, DP-01, DP-02; context pack naming rules; ASM-5067, ASM-5072 |
| BR4 | The case and its route states stay with rwb-case: the contract declares the state read and the move answer as consumed and declares no `recovery_case` property | Context pack ownership rows; ASM-5037 |
| BR5 | The rule package and the ledger stay with rwb-decision: the contract names R-WO-05 and declares no rule row and no ledger entry | Business Rules and Routing Logic v4; ASM-5067, ASM-5040 |
| BR6 | The prepared pack is composed, not built: the element names R-WO-05's five facts and the record reference, and records the pack builder as RWB-S7-E6015-APP's and the agent run as rwb-agent's | FSD S7 A2.3 and A2.9 (the same R-WO-05 row); ASM-5068 |
| BR7 | The ALS and general-ledger interface is declared nowhere: no field, no file layout, no reference shape and no error set, and the crossing and the provision release are the integration story's | TSD S7 T5.1 (None); connection matrix row S7; ASM-5070 |
| BR8 | No event and no Schedule belongs to this feature: `WriteOffApproved` (EV-24) is the approval story's and JOB-16 is the scan story's | Event and Messaging Design v5 EV-24; Batch and Scheduling Design v5 JOB-16; ASM-5069 |
| BR9 | The state vocabulary is closed: the WRITEOFF values are published as an enumeration of `state` and no state value is a constant of the code | TSD S7 T3.0 and T4; ASM-5037 |
| BR10 | No personal data in a schema, an example or a fake: identifiers, an amount, a code and a rule version only | Template and Rules v1 §R7.2 (s17); context pack naming rule on PII |
| BR11 | One REST base, one topic, one queue and one login per service; the document never declares another service's base or topic as its own | DP-13; Template and Rules v1 §R4 |
| BR12 | A schema change is additive within major version 1; a breaking change is a new major version | Architecture v5 slide 11 notes (BACKWARD compatibility) |
| BR13 | The document declares only operations owned by rwb-writeoff, and this feature owns none; a consumed element is described as consumed and faked, never as provided | Ownership rows; DP-11; ASM-5071 |

### 9. State transitions

The lifecycle of this document, not of a write-off:

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The element, the state vocabulary, the consumed rows, the pack element, the rights and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the SCR-27 fragment, the wave 4 harness and the rwb-source-data, rwb-case and rwb-decision owners accept the document and the fakes | Baselined |
| Baselined | Additive change | A property or a state value is added within major version 1 | Baselined |
| Baselined | Breaking change | A property is removed, renamed or retyped, or a state value changes | New major version drafted |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | A forbidden element appears | The absence and boundary tests of AC1 and AC7 fail: an operation, an event, a Schedule, an ALS element or a foreign table | In review |

The WRITEOFF machine the document describes is the app story's and the integration story's: `POPULATION_PROPOSED`, `PACK_PREPARED`, `POSTING_PENDING`, `POSTED`, `POSTING_REJECTED`, `WRITEOFF_EXCEPTION` and `PROVISION_RELEASED` are the values this feature reads and writes, and the case route state that rwb-case holds is answered, not declared here. This baseline fixes the vocabulary and moves no write-off and no case (ASM-5037).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-writeoff | Owns the OpenAPI document and the contract tables; tags the baseline |
| Solution architect | Approves a breaking change, a new major version, and the correction of the consumed rows |
| Consuming teams (the app story, the SCR-27 fragment, the wave 4 harness, the posting track and the owners of rwb-source-data, rwb-case and rwb-decision) | Review and sign off the parts they consume |
| Platform library owner | Owns the error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library this document reuses |
| Data steward | Confirms that no personal data field is declared in an answer, an element or a fake |

The per-service login behind the security scheme of the document is named "the rwb-writeoff login (DP-02)" and is not part of this baseline.

### 11. Data

The contract baseline declares shapes, not business values.

| Item | Content |
|---|---|
| Write-off element | The columns of DF-FIN-010 to DF-FIN-020: `id`, `case_id`, `decision_log_id`, `amount`, `tax_criteria_met`, `committee_date`, `posted_date`, `responsibility_center`, `cost_center`, `gl_product`, `recovered_after` |
| Required flags | `id`, `case_id`, `amount`, `tax_criteria_met` and `recovered_after` required; the other six optional, as the API Specification's `WriteOff` element declares them |
| State | `state` of TSD S7 T3.0 against the WRITEOFF vocabulary of T4, published as an enumeration and read as reference data |
| Record reference | `decision_log_id` holds the identifier the local decision-record library returns, and the P7 ledger entry id is not stored here (ASM-5040) |
| Prepared pack | The case reference, the write-off reference, the balance, the provision carried, the route history, the legal state, the asset state, the residual and the record reference; composed from the pack of RWB-S7-E6015-APP and the source-data answers (ASM-5068) |
| Decision record | DF-DEC-001 to DF-DEC-018 through the local library, written before the row changes (DP-03) |
| Consumed shapes | The source-data account, asset and ledger rows of P1, the case state and move rows of P3, and the package row of P7, each declared as consumed and faked |
| Not declared here | `recovery_case` (P3), `account_ext`, `interaction` and the `v_ace_*` views (P1), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6), the ALS and general-ledger interface, and the two operations API-S7-001 and API-S7-002 (other stories of this service) |
| Consumed fields with no source | The operation names of the source-data reads, of the case move and of the package read, the values of the WRITEOFF table that T4 does not print, and the posting and close windows: Not specified in the source documents (GAP-3034; ASM-5067, ASM-5037, ASM-5070) |

The field-level formats of the added elements are settled in the baseline review; this story fixes the element names, the vocabulary of AC2 and the optionality rule of BR12. **No new table, no new column and no migration** is declared by this story.

### 12. Contract

#### 12.1 REST operations provided

None. Owner rwb-writeoff (S7); base `/api/recovery/writeoff/v1` (DP-13). This feature provides no operation and this baseline declares none for it. The two operations of this legacy key are other stories' of the same service: `POST /write-off-scans` (API-S7-001, right C) is RWB-S7-E6013-APP's, and `POST /write-offs/{writeOffId}/committee-decision` (API-S7-002, right A) carries the approve outcome at RWB-S7-E6018-APP and the reject and defer outcomes at RWB-S7-E6019-APP and RWB-S7-E6020-APP. The stage read behind SCR-27 is Not specified in the source documents and carries the placeholder (GAP-3034; ASM-5071). A build that declares a pack-prepared operation here fails the absence test of AC1.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in the baseline |
|---|---|---|---|
| `GET /cases/{caseId}` family (read) | `/api/recovery/case/v1` | P3 rwb-case | The case reference and the state of the write-off stage; faked. The matrix row S7 has no REST edge to P3, so the facts also arrive in the stage input from the parent `CaseWorkflow` (ASM-5037) |
| The account and asset read (operation name Not specified in the source documents (GAP-3034; ASM-5067)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The account reference, the balance, the provision carried and the asset facts of the case; faked |
| The route-history read of the interaction ledger (operation name Not specified in the source documents (GAP-3034; ASM-5067)) | `/api/recovery/source-data/v1` | P1 rwb-source-data | The route history of the case from DF-INT-001 to DF-INT-013; the ledger is P1's under the default ruling (DP-18); faked |
| The read of the WO rule package version in force (operation name Not specified in the source documents (GAP-3034; ASM-5067)) | `/api/recovery/decision/v1` | P7 rwb-decision | The package version and the row R-WO-05 with the reference data the pack reads; reached as an activity on that owner's queue, as the connection matrix row S7 gives it; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). The four rows are contract dependencies of class C that the plan's C row does not carry, and the absence is recorded as GAP-3034 with ASM-5067.

#### 12.3 Events published

None. The service owns `WriteOffApproved` (EV-24) on topic `rwb.writeoff.events.v1` with payload `writeOffId`, `caseId` and `amount`, and it is the committee's approval, which RWB-S7-E6018-APP publishes. This baseline therefore declares no producer, no envelope and no outbox row of its own, and the absence test of AC7 fails a build that adds one (ASM-5069).

#### 12.4 Events consumed

None. No source gives rwb-writeoff a consumed event for this feature: the pack arrives inside the same service and the account, asset and case facts arrive on their owners' contracts. This baseline declares no consumer group, no subscription and no inbox of its own, and the absence test of AC7 fails a build that adds one (ASM-5069).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow, one execution per case per stage, the stage child of `CaseWorkflow` | `rwb-writeoff` in namespace `rwb-recovery` | The stage that hosts the pack-prepared branch; its input, its signals and its outcome for the parent are declared, not built |
| The pack-prepared branch of `WriteOffWorkflow` | Workflow branch | `rwb-writeoff` | The step from the pack to `PACK_PREPARED`: R-WO-05, the record, the row and the stage outcome |
| `prepareWriteOffPackForPosting` | Activity, the one step | `rwb-writeoff` | The case, the write-off, the source-data answer and the package answer in; the rule ID with its version, the state, the record reference and the case move out |
| `EvaluateRules` and `RecordAndApply` on `rwb-decision` | Consumed activity contract, L4 | `rwb-decision` | The package version in force and the record of the outcome on the owner's queue; this document declares the shapes and registers nothing |

No child workflow of this service exists in this feature and the committee's act is not run here: it is the `ApprovalWorkflow` of the kit on the P7 queue, started by RWB-S7-E6018-APP. The activity name is a target design choice and the trigger is read as the arrival of the pack for a write-off in `POPULATION_PROPOSED`, because the FSD declares the scan as the module's only background event (FSD S7 A2.9.4.4). No activity is registered by this story.

#### 12.6 Schedules

None. The branch runs from the pack; this baseline declares no Temporal Schedule, no Quartz row, no shared job table and no batch table. JOB-16, the monthly write-off scan on the third working day on the ACE batch-complete record for ALS, is RWB-S7-E6013-APP's. The month-end close window and the posting window of R-WO-20 are timer values of the package and of the posting track, which is RWB-ITG-E6021-ITG's; their calendar and cadence are Not specified in the source documents and carry the placeholder (GAP-3034; ASM-5070).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| write_off | S7 (`rwb_writeoff`) | The write-off of the balance on a case, its DF-FIN fields, its `state` and its record reference; the table the element answers from |
| decision_record | PLT library, created in `rwb_writeoff` | The local hash-linked decision record of the rule outcome (DP-03) |
| idempotency_key | PLT library, created in `rwb_writeoff` | The key of the repeated pack and the outcome it holds |
| outbox_event | PLT library, created in `rwb_writeoff` | Created in this schema by the library for the stories that publish; no row of it belongs to this feature |

`recovery_case` (P3), `account_ext`, `interaction` and the thirty `recovery.v_ace_*` views (P1), `rule_row` and `decision_log_entry` (P7), `document` (P5), `notice` (P6) and the posting and proceeds tables of P8 and S9 are not owned by this baseline; it names them only as answers or rule versions of their owners, and no foreign key leaves the schema (DP-01).

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-source-data account and asset fake | The balance and the provision carried of `RC-2027-000721`, the asset facts, a stale product with its date, a missing fact and no answer beyond 2 s | AC3, AC5 |
| rwb-source-data ledger fake | The route history of the case, and a case with no route history | AC3, AC5 |
| rwb-case state and move fake | The states `POPULATION_PROPOSED` and `PACK_PREPARED` of case `RC-2027-000721`; an accepted and a refused `PACK_PREPARED` move; no answer beyond 2 s | AC4, AC5 |
| rwb-decision rule-package fake | The WO package at its version in force with R-WO-05 and its reference data | AC4, AC5 |
| Local decision-record library stub (`RWB-PLT-E1027-CON`) | A healthy chain, and a stopped chain | AC6 |
| rwb-writeoff write-off and pack fake | The write-off `WO-2027-000321` of case `RC-2027-000721` with its amount, its tax criteria flag, its state, its record reference and its prepared pack | AC2, AC5 |
| gateway-bff composite route fake | The merged SCR-27 answer for the write-off, with the write-off facts of this service read once | AC1 |

The fakes are test-only and are replaced by the real services in SIT. The unpublished operation names and the posting windows are derived from the published documents and carry the placeholder until their owners confirm them (GAP-3034; ASM-5067, ASM-5070).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 4 consumed | The rwb-case state read, the rwb-source-data account-and-asset read and ledger read, and the rwb-decision package read; one hop, 2 s |
| Kafka | 0 published, 0 consumed | `WriteOffApproved` (EV-24) is the approval story's; the decision record is the library's on `rwb.decision-record.v1` and is not an event of this service |
| Temporal | 1 workflow, 1 branch and 1 activity declared, 0 registered, 1 consumed | `WriteOffWorkflow` and its pack-prepared branch on `rwb-writeoff` with its activity, and the consumed package and record activities on `rwb-decision`; no Schedule and no child workflow |
| File | None | No file is read, built or delivered here; the pack documents are rwb-document's (P5) and the ALS and general-ledger crossing is the integration story's (ASM-5070) |

### 13. Solution plan

**The CON declares shapes and moves nothing.** It writes no code, no migration and no table, and it changes no write-off, no case, no source-data row and no rule package. What it publishes is one OpenAPI 3.1 document, nine contract tables, the rights of the read and seven fakes.

**Deliverables.** The additive document `openapi/rwb-writeoff-v1.yaml`, the `write_off` element and the state enumeration, the prepared-posting-pack schema, the contract README rows for the four consumed rows and their placeholders, and the seven WireMock mapping sets.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | the monolith API base | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the element the baseline declares before the row changes, on the shared `rwb.decision-record.v1`. DP-05 is the largest change of the feature: the legacy read of `v_ace_account`, `v_ace_npa_asset` and `interaction` becomes three consumed rows of rwb-source-data, and the service's own-ACE-view option of the pattern is closed because this service holds no `recovery.v_ace_*` grant. DP-13 moves the base of the key's two operations and adds none, because this feature owns no operation. DP-19 is behind SCR-27, whose screen model is the edge contract's, and this baseline fixes the write-off answer only. No other pattern is claimed: the case, the source data and the package are consumed contracts and the ALS crossing is the harness's, so DP-04, DP-09, DP-10, DP-16 and DP-20 stay off this table and their absence is recorded in the registers (GAP-3034; ASM-5067, ASM-5069, ASM-5070).

**Build steps**

1. Record the absence of a pack-prepared operation and the two operations as other stories', with the absent-operation test of AC1.
2. Write the `write_off` element, its required flags, its lengths and its state enumeration of AC2, with the unprinted state values and the `posted_date` note.
3. Record the rwb-source-data rows of AC3 with their owner, their budget, the ledger ruling and the placeholder.
4. Record the rwb-case and rwb-decision rows of AC4 with their owners and the placeholder.
5. Write the prepared-posting-pack schema of AC5, its composition rule and its absent ALS element, and publish the seven fakes with the drift test.
6. Record the rights, the roles, the scope and the decision-record element of AC6, with the legacy A and C holder disposition.
7. Record the naming baseline and the boundary of AC7, then tag the baseline and collect the consumer sign-off.

**Done when.** The OpenAPI document validates in the pipeline, the seven contract tests pass, the fakes answer every consumed path and the drift test is green, and the app story, the SCR-27 fragment, the posting track and the wave 4 harness have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-S7-001 | Carried from the legacy message set of this key. It names the tax criteria version, which is the scan's gate, so no path of this feature raises it | The scan is on hold until Finance publishes the tax criteria. |
| MSG-GEN-001 | A required field of a body is absent or invalid, or a body fails schema validation | Enter {field}. |
| MSG-P4-002 | The role lacks the Write-off and posting right the read declares, and a role without the right of a consumed act tries it | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record cannot be written before the write-off row changes | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A pack fact is stale after a late or failed ACE batch (VR-S7-009-1) | {product} is from {date}. Today's ACE batch has not arrived. |

The first four message IDs are those of the legacy message set of this key and MSG-P1-001 is the message of VR-S7-009-1 in FSD S7 A2.9.3.1; the text is the legacy and FSD wording, copied unchanged, and no message is reworded or added. MSG-S7-001 is carried because it is in the message set of this feature, and the check itself belongs to the scan story of this service.

### 15. Screens and states

The contract serves SCR-27 Write-off proposal in its scan, proposed, in-committee, approved and pack-prepared states, through the gateway-bff composite route (DP-19). The route calls rwb-writeoff for the write-off, its stage state and the five pack facts, rwb-case for the case and its route state, and rwb-decision for the decision records; this baseline fixes the rwb-writeoff answer only, and the composite route specification and the screen field list belong to RWB-PLT-N001-CON. The stage read behind the list is a placeholder, because no source publishes it (ASM-5071). The refused, not-recorded and stale states of the app story read the messages of section 14 on the same route, and the posted, rejected and provision-released states belong to the posting track and its integration story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-021-01 | AC1, AC2 | Contract | The posting of write-off `WO-2027-000321`; the contract half answers the element, its state and the absent pack-prepared operation |
| TC-E6-021-02 | AC2, AC3 | Contract | The five pack facts with the limit-free pack reference data; the contract half answers the source-data rows, the state value and the `PACK_PREPARED` move shape |
| TC-E6-021-03 | AC2, AC4 | Contract | A posting that has to wait for a rejection to clear; the contract half answers the POSTING state values, the row and the move shapes |
| TC-E6-021-04 | AC5, AC6 | Contract | The decision-record stub stopped; the contract half answers the MSG-P7-003 path and the record element |
| TC-E6-021-05 | AC6 | Contract | A role without the Write-off and posting right; the contract half answers the 403 with MSG-P4-002 and the rights of the read |
| TC-E6-021-06 | AC5, AC7 | Contract | A forced record failure and a forbidden element; the contract half answers the record path, the pack schema and the absence tests |
| TC-S7-E6021-CON-01 | AC1 | Contract | The document validates; no pack-prepared operation, no second base and no second topic are declared, and the two operations of the key are named as other stories' |
| TC-S7-E6021-CON-02 | AC2 | Contract | The `write_off` element validates with its eleven properties, its five required flags and the WRITEOFF state enumeration |
| TC-S7-E6021-CON-03 | AC3 | Contract | The source-data account, asset and ledger rows and their placeholders; the no-`v_ace_*` and no-ACE-table boundary |
| TC-S7-E6021-CON-04 | AC4 | Contract | The case state and move rows and the package row with their placeholders; no `recovery_case` and no `rule_row` property |
| TC-S7-E6021-CON-05 | AC5 | Contract | The prepared-posting-pack schema with its nine members, its composition rule and its absent ALS element; the seven fakes match the document and a drifted fake fails the build |
| TC-S7-E6021-CON-06 | AC6 | Contract | RW-WRITEOFF holds CRU, RW-CREDITAD holds CRUA, RW-PRODHEAD, RW-WOCOMM and RW-FINANCE hold RA, and the legacy A and C holders are recorded; the decision-record element matches the library schema |
| TC-S7-E6021-CON-07 | AC7 | Contract | The naming baseline; the absence test for an event, a second topic, a Schedule and a Quartz row, and the boundary test for a `v_ace_*` path and a foreign table property |

The six legacy cases are the legacy cases of RWB-E6-021 in their legacy order, carried as the contract half: their Covers column names the criterion of this story that fixes the surface each one exercises, their Data keeps the legacy intent, and the business outcome of each is proved by RWB-S7-E6021-APP for AC2 and AC4 and by RWB-ITG-E6021-ITG for AC1 and AC3. Legacy level `System` maps to `Contract` here because the artefact under test is the contract, and the access and forced-failure cases map to `Contract` for the same reason. The seven cases `TC-S7-E6021-CON-01` to `-07` are new. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID; no `-ITG` copy is written here, and the cross-service journey of the key belongs to the wave 4 harness.

### 17. Guardrails

- No business value in the contract: the posting and close windows, the retry limit, the pack reference data, the state values and the rule row stay package values, reference data or an enumeration, never a schema default or a constant of the code.
- No personal data in a schema, an example or a fake: identifiers, an amount, a code and a rule version only; every example is synthetic.
- The ACE facts stay with rwb-source-data, the case with rwb-case and the package and the ledger with rwb-decision: the document declares no `account_ext`, `interaction`, `v_ace_*`, `recovery_case`, `rule_row` or ledger property and no row write of any of them (BR3, BR4, BR5).
- The prepared pack is composed, not built: the document declares no pack builder, no document index and no agent run of its own and names RWB-S7-E6015-APP and rwb-agent (BR6).
- The ALS and general-ledger interface stays undeclared here: no field, no file layout, no posting reference and no error set (BR7, ASM-5070).
- This feature owns no operation: the document declares none for it and records the two operations of the key as other stories' (BR13, ASM-5071).
- One base, one topic, one queue and one login per service; a document that names another service's base or topic as its own fails the review (DP-13).
- No retired element is reintroduced: the absence tests fail a build that declares an event, a second topic, a Schedule, a Quartz row or a shared job table.
- The error envelope, the `Idempotency-Key` rule, the naming rule and the decision-record library come from the platform; this story narrows them but never redefines them.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-S7-002 | The committee pack is prepared from case and provision data with no manual assembly (Must, E6); the contract fixes the pack facts, the source-data rows and the record on which the pack is built | The prepared-posting-pack schema, the source-data rows and the element | TC-E6-021-02, TC-S7-E6021-CON-03, TC-S7-E6021-CON-05 |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published (Must, E6); the contract fixes the row, the POSTING vocabulary and the prepared pack that the crossing consumes, and declares no ALS element (GAP-3034; ASM-5070) | The `write_off` element, the state enumeration and the pack schema | TC-E6-021-01, TC-E6-021-03, TC-S7-E6021-CON-02 |
| ADR-014 | Schema and login per service | `rwb_writeoff` and its own login | TC-S7-E6021-CON-07 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The four consumed rows with their budget and breaker | TC-S7-E6021-CON-03, TC-S7-E6021-CON-04 |
| ADR-022 | Local decision record plus central ledger | The decision-record element and the ledger entry of P7 | TC-S7-E6021-CON-06 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E6-021, disposition Split (rework) |
| Legacy criteria | AC2 and AC4 of the legacy story, owned word for word by RWB-S7-E6021-APP, and AC1 and AC3, owned by RWB-ITG-E6021-ITG; this baseline copies none of them |
| Test cases | The six legacy cases as the contract half, and the seven new contract cases TC-S7-E6021-CON-01 to -07 |
| Feature and screens | FEAT-WOF-09 Post an approved write-off, SCR-27 Write-off proposal |
| Rules | R-WO-05, named from the Business Rules and Routing Logic v4 and governed in rwb-decision |
| Decoupling patterns | DP03, DP05, DP13, DP19 |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-022 (local decision record with the central ledger) |

### 19. Out of scope

- The behaviour behind the elements, the evaluation of R-WO-05, the decision record, the state, the record reference and the case-move answer: RWB-S7-E6021-APP.
- The ALS and general-ledger posting, the posting reference, the rejection and the re-post under R-WO-20 to R-WO-23 and R-WO-44, the provision release under R-WO-25 and the completeness publication: RWB-ITG-E6021-ITG (ASM-5070).
- The assembly of the pack, its document index and its agent run: RWB-S7-E6015-APP (ASM-5068).
- The monthly eligibility scan, the tax criteria and JOB-16, and API-S7-001: RWB-S7-E6013-APP and RWB-S7-E6014-APP.
- The removal of a case by the team under R-WO-07: RWB-S7-E6016-APP; the committee decision act, API-S7-002, and the approve, reject and defer outcomes: RWB-S7-E6018-APP, RWB-S7-E6019-APP and RWB-S7-E6020-APP (ASM-5071).
- The case of record and its route states: rwb-case (P3), whose answers this baseline declares as consumed and faked (ASM-5037).
- The account, asset and ledger facts and the `recovery.v_ace_*` views: rwb-source-data (P1) (GAP-3034; ASM-5067, ASM-5072).
- The WO rule package, its version and the ledger: rwb-decision (P7) (ASM-5067, ASM-5040).
- The pack documents and their custody: rwb-document (P5); the notices to customers: rwb-comms (P6); the payment posting of a recovery after charge-off: rwb-payment (P8).
- The gateway-bff composite route and the screen field list of SCR-27: RWB-PLT-N001-CON and the edge stories.
- The provisioning feed to Finance, the reconciliation of the approved and posted populations and the exception loop: RWB-E6-022 to RWB-E6-024 (FEAT-WOF-10 to -12).
- The deployment of this capability, its flag, its dashboards, its alerts and its runbook: the operations story of this legacy key.
