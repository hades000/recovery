# RWB-ITG-E6008-ITG Derecognize and post to the general ledger

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register)

- Freshness answer named by its published fields: `status` `LOADED` or `STALE`, `businessDate`, `loadedAt`.

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-E6008-ITG-16) |
| Depends on (build) | None |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-E6008-ITG-21) |
| Integration dependencies | RWB-S6-E6008-APP (build not done yet; stub until then) |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-005, RD-P1-041 |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-008 as the wave 4 integration proof of the derecognition and the general ledger posting steps of DebtSaleWorkflow, driven from the award and observed across rwb-debtsale, rwb-integration and the ACE read-back; the build of those steps is RWB-S6-E6008-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-E6008-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 13 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer**, I want **the sold accounts to leave the book and the result to reach ALS and the general ledger through a posting that carries a recorded reference and a decision record the central ledger confirms before the point of no return, proved end to end against the real services from the award onwards**, so that **debt sales run on approved lots and masked data, and a rejected or late posting is re-posted rather than lost**.

This story builds the harness and the evidence, and nothing else. The derecognition, the general ledger posting and the decision record are built by S6 in RWB-S6-E6008-APP and its CON story; the posting leaves through P2 rwb-integration's ACE integration path, which is P2's own product. The harness starts the journey at the award operation, observes every hop through the owners' published contracts, and writes a run report per lot. It builds no production endpoint, no table, no workflow, no activity, no schedule and no screen, and it writes no code in any service.

### 2. Business rationale

A lot can be awarded, the buyer can pay, and the bank can still carry the accounts on its book. That is the failure this story is written against. The award moves a lot of accounts to a buyer; the derecognition removes those accounts from the book, the posting books the sale in the general ledger, and the provision input reaches Finance. If the posting leaves no reference, the money side cannot be reconciled to a ledger entry, and the sale is a settlement nobody can find in the books. If the accounts stay in `v_ace_account` with their old status, the next ACE batch puts the sold balances back into arrears reporting and the case list, and every measure computed over them is wrong. If the posting is rejected and the rejection sits in a queue, the lot stays between two states for longer than the two working days R-DS-32 allows.

The point of no return is the transfer and the derecognition (Temporal design slide 22: "Transfer and derecognition are the pivot"). The saga may undo everything before it; after it, the steps are retried until they succeed, and strict mode makes the transfer wait until the central ledger in rwb-decision confirms the decision record. That is why this story asserts the confirmation before the posting reference is recorded, and why it asserts the re-post path as carefully as the happy path: after the pivot there is no compensation, only the retry and the exception task.

The harness is decoupled the way the services are. Every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). ACE data is read only through rwb-source-data's data-product contract (DP-05) with its freshness stamp, never from another service's schema and never by a direct view read (DP-01). The decision record is written by S6 through the local decision-record library on `rwb.decision-record.v1` (DP-03) and read back through rwb-decision's contract; where a screen would compose these calls the path is the gateway-bff composite route (DP-19). It carries REQ-S6-007 and REQ-S6-008 and the state rules R-DS-30 to R-DS-34 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S6 rwb-debtsale (the lot read and the award), P2 rwb-integration (outbound items, the resend and the file run), P1 rwb-source-data (DP01, DP09 and freshness), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP09 Debt sale, each with one system of record, so a sold account and its lot have one named owner before a status is resolved (FSD P1 v3, A2.2).
- P2's ACE integration path for the general ledger posting is configured in SIT, with an outbound item type for the posting and a file run that records its answer.
- RWB-S6-E6008-APP owns the derecognition, the posting and the decision record; until it lands, the posting fixture of §12.8 stands in for its effect and the story is reported as a stub pass.
- The lot award and its criteria are RWB-S6-E6005-*; the fixture holds an already awarded lot, so this story never asserts a price, a reserve or a cap.
- The harness environment and base hosts, the posting reference shape and its rejection codes, the retry and back-off settings, the evidence format and retention, the pass or fail gate, and the synthetic lot and account keys: Not specified in the source documents (GAP-0454; ASM-0646).
- The synthetic lot, its two accounts, the case and the business date are held in the fixture as data, not written in code.
- The signed epic design of the service epic RWB-ITG-W4 is recorded: Not specified in the source documents (DOR-RWB-ITG-E6008-ITG-14).
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-S6-E6008-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the fixture: lot `LOT-SYN-2027-0001` with lot_no `LOT-SYN-2027-0001`, cut_off_date 2027-03-31 and the winning buyer's panel entry, holding two accounts `ACC-SYN-000801` and `ACC-SYN-000802` on case `RW-2027-000801`. On Day 1 the stub of §12.8 returns the same records.
2. Harness: awards the lot through `POST /api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award` with one Idempotency-Key, which starts DebtSaleWorkflow on the task queue `rwb-debtsale`. The award's own criteria are out of scope; the fixture lot already passes them.
3. Harness: reads the lot through `GET /api/recovery/debtsale/v1/debt-sale-lots/{lotId}` and asserts the lot_no, the cut_off_date, the winner and the lot status after the transfer (DF-SAL-030).
4. Harness: reads `GET /api/recovery/integration/v1/admin/outbound-items` for the lot's posting item, and asserts one outbound item, its file run, the file name of the run and a delivered answer.
5. Harness: asserts the posting reference is recorded on the lot, and that the amount and the account count it carries match the lot read and the DP09 rows.
6. Harness: reads `GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` and asserts both sold accounts carry their derecognised status, then reads DP09 records for the same case and asserts the two `debt_sale_account` rows with their outstanding and selling price.
7. Harness: reads `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` and asserts `status` `LOADED`, the `businessDate` and `loadedAt` behind that read, so a stale product is never reported as a clean derecognition.
8. Harness: counts one `rwb.debtsale.LotAwarded.v1` and one `rwb.debtsale.AccountsTransferred.v1` on `rwb.debtsale.events.v1`, and asserts the consumer effect through `GET /api/recovery/case/v1/cases/{caseId}`; then replays both events and asserts the case and the lot are unchanged, because the inbox holds one processed row per consumer.
9. Harness: reads `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` and asserts one entry for the derecognition and one for the posting, each with its rule id and rule version, and that `rwb.decision.DecisionRecorded.v1` was published on `rwb.decision-record.v1` and confirmed by the central ledger before the posting reference was recorded.
10. Harness: holds the ledger answer back, asserts the posting step does not complete and no posting reference is recorded; then releases an ALS or general ledger rejection, asserts the case moves to POSTING_REJECTED_DS with an exception task, resends the same outbound item through `POST /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend` and asserts one outbound item, one posting reference and one ledger entry after the correction.
11. Harness: closes the claim window under R-DS-34 and asserts the lot closes with its realized recovery by lot and by buyer.
12. Harness: calls `GET /api/recovery/access/v1/me/session` as a synthetic RW-OFF caller, then reads the lot through `GET /api/recovery/debtsale/v1/debt-sale-lots/{lotId}` and asserts 403 with MSG-P4-002 and no state change.
13. Harness: writes one run report per lot, keyed by story and lot_no, naming the contract version of each hop, whether the hop was a stub or the owner, the posting reference, the outbound item id, the ledger entry and the criteria verdicts.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-008-01-ITG (ITG AC1) | AC1 |
| X2 | The outbound item exists but no file run carries a delivered answer | The run fails on AC4 and the report names the item id, the file run and its answer; a queued item is never reported as posted | None | TC-E6-008-01-ITG (ITG AC4) | AC4 |
| X3 | The posting leaves and no reference is recorded on the lot | The run fails on AC4 and the report names the lot, the item id and the file run, so an unreferenced posting is a failure | None | TC-E6-008-01-ITG (ITG AC4) | AC4 |
| X4 | The ACE batch still shows a sold account with its old status | The run fails on AC4 and the report names the account_key, the status read and the freshness stamp | None | TC-E6-008-01-ITG (ITG AC4) | AC4 |
| X5 | The central ledger has not confirmed the decision record and the posting completes anyway | The run fails on AC5 and the report names the case, the state and the missing confirmation; strict mode is never assumed | MSG-P7-003 | TC-E6-008-06-ITG (ITG AC5) | AC5 |
| X6 | ALS or the general ledger rejects the posting and no exception task is raised | The run fails on AC5 and the report names the rejection code, the case state and the task; a rejected posting without a task is a lost posting | None | TC-E6-008-04-ITG (ITG AC5) | AC5 |
| X7 | The correction produces a second outbound item, a second posting reference or a second ledger entry | The run fails on AC5 and the report names the two items or entries | None | TC-E6-008-04-ITG (ITG AC5) | AC5 |
| X8 | A caller without the Debt sale right is allowed to read the lot | The run fails on AC6 and the report names the caller role, the operation and the answer; a 200 is a failure even when no data changed | MSG-P4-002 (expected, and missing) | TC-E6-008-05-ITG (ITG AC6) | AC6 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-S6-E6008-APP, and its fixture answers until it lands |
| Negotiable | The fixture layout, the posting reference shape, the retry settings, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The sold accounts are proved to leave the book, the posting is proved to carry a reference a ledger entry can be matched to, and the re-post is proved to happen once |
| Estimable | One runner, one stub set, one posting fixture, one outbound-item probe, one ACE read-back, one event observer and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion runs against the stubs and again against RWB-S6-E6008-APP as it lands |

### 7. Acceptance criteria

```gherkin
Feature: Derecognize and post to the general ledger - wave 4 integration harness

  Background:
    Given the synthetic lot "LOT-SYN-2027-0001" holds accounts "ACC-SYN-000801" and "ACC-SYN-000802" on case "RW-2027-000801"
    Given the lot is awarded and its accounts are transferred to the winning buyer
    Given the ACE batch for business date "2027-03-31" is loaded and DP01 and DP09 answer for the case

  Scenario: AC1 Derecognize and post to the general ledger (legacy RWB-E6-008 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then removes the sold accounts from the book as this service's decision, and P8 builds and sends the posting to ALS and the ledger with no direct interface from this service
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-DS-31 (legacy RWB-E6-008 AC2)
    Given a case in state DERECOGNISED
    When gl posting run
    Then post to the general ledger and send the provision input to Finance
    Then the case moves to GL_POSTED

  Scenario: AC3 Rule R-DS-33 (legacy RWB-E6-008 AC3)
    Given a case in state POSTING_REJECTED_DS
    When posting corrected
    Then re-post to ALS and the general ledger
    Then the case moves to GL_POSTED

  Scenario: AC4 The posting reference is recorded and the accounts leave the book (new, D-RCV-60)
    Given the lot "LOT-SYN-2027-0001" is awarded and its accounts are transferred
    When the derecognition run and the general ledger posting run complete
    Then rwb-integration holds one outbound item for the lot with its file run and a delivered answer
    And the posting reference is recorded on the lot and matches the amount and the account count of the DP09 rows
    And the ACE batch shows "ACC-SYN-000801" and "ACC-SYN-000802" with their derecognised status through DP01 of the rwb-source-data contract fake with its freshness stamp
    And "rwb.debtsale.LotAwarded.v1" is published once on "rwb.debtsale.events.v1" and consumed once by rwb-case and once by rwb-payment
    And "rwb.debtsale.AccountsTransferred.v1" is published once on the same topic and consumed once by rwb-case and once by rwb-reporting
    And a replay of either event leaves the case and the lot unchanged, because the inbox holds one processed row per consumer
    And the decision record for the derecognition and the posting is published as "rwb.decision.DecisionRecorded.v1" and confirmed by the central ledger in rwb-decision
    And the lot closes under R-DS-34 when the claim window closes

  Scenario: AC5 The posting waits for the ledger and a rejection is never lost (new, D-RCV-60)
    Given a case in state DERECOGNISED whose posting run GL_POSTING_RUN has started and the central ledger has not confirmed the decision record
    When the general ledger posting run is attempted
    Then the posting step does not complete and no posting reference is recorded
    When ALS or the general ledger rejects the posting
    Then the case moves to POSTING_REJECTED_DS with an exception task raised
    When the outbound item is resent through POST /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend and the cause is cleared
    Then one outbound item, one posting reference and one ledger entry exist for the lot
    And the case moves to GL_POSTED once and only once

  Scenario: AC6 A caller without the right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Debt sale R
    When the caller reads the lot through GET /api/recovery/debtsale/v1/debt-sale-lots/{lotId}
    Then the answer is 403 with "MSG-P4-002"
    And no state changes

  Scenario: AC7 The harness asserts BR1 to BR8 and changes none of them (new, D-RCV-60)
    Given the lot "LOT-SYN-2027-0001" is awarded and its accounts are transferred
    When the harness runs the derecognition and the posting checks
    Then each rule BR1 to BR8 is asserted against the state the run observes
    And the harness changes no rule and writes no rule state

  Scenario: AC8 A consumed call that fails or does not answer holds the posting and records no posting reference (new, D-RCV-60)
    Given a case in state DERECOGNISED whose posting run GL_POSTING_RUN has started
    When a consumed call of section 12.2 fails or does not answer
    Then the posting step does not complete and no posting reference is recorded
    And the case does not move to GL_POSTED
```

Legacy AC4 (the decision log cannot be written) belongs to RWB-S6-E6008-APP, and this story asserts the same failure at the point of no return through AC5.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The sold accounts are derecognised on the account before the posting is attempted | R-DS-30 | AC1, AC4; TC-E6-008-01-ITG |
| BR2 | The posting books the sale in the general ledger and sends the provision input to Finance, and the case moves to GL_POSTED | R-DS-31 | AC2; TC-E6-008-02-ITG |
| BR3 | When ALS or the general ledger rejects the posting, the posting is held and an exception task is raised inside two working days | R-DS-32 | AC5; TC-E6-008-04-ITG |
| BR4 | When the rejection cause is cleared the posting is re-posted once, and the case moves to GL_POSTED | R-DS-33 | AC3, AC5; TC-E6-008-03-ITG, TC-E6-008-04-ITG |
| BR5 | The lot closes when no put-back claim arrives inside the claim window, with realized recovery recorded by lot and by buyer | R-DS-34 | AC4; TC-E6-008-01-ITG |
| BR6 | The transfer and the derecognition are the point of no return, and the transfer waits for the central ledger to confirm the decision record | Temporal and Drools design slide 22; slide 25 strict-mode note | AC5; TC-E6-008-06-ITG |
| BR7 | An awarded account stops every other open action on its case the same day, and the transfer, the derecognition and the posting follow the award without re-keying | REQ-S6-007; REQ-S6-008 | AC4; TC-E6-008-01-ITG |
| BR8 | ACE data is read only through rwb-source-data's data-product contract with its freshness stamp, and never from a view or another service's schema | D-RCV-35; DP-01, DP-05 | AC4; TC-E6-008-01-ITG |

The harness asserts these rules and changes none of them; the rules themselves are evaluated in RWB-S6-E6008-APP. AC7 and TC-E6-008-07-ITG assert all of BR1 to BR8 together.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| DATA_TRANSFERRED | DERECOGNITION_RUN | the sold accounts are derecognised | DERECOGNISED |
| DERECOGNISED | GL_POSTING_RUN | the posting leaves through rwb-integration and the ledger accepts it | GL_POSTED |
| DERECOGNISED | POSTING_REJECTED | ALS or the general ledger rejects the posting | POSTING_REJECTED_DS |
| POSTING_REJECTED_DS | POSTING_CORRECTED | the rejection cause is cleared and the item is resent once | GL_POSTED |
| GL_POSTED | CLAIM_WINDOW_CLOSED | no put-back claim inside the claim window | LOT_CLOSED |

GL_POSTING_RUN and POSTING_CORRECTED are the R-DS-31 and R-DS-33 event codes; the case states are DERECOGNISED, GL_POSTED and POSTING_REJECTED_DS, and the lot status after each step is read through DF-SAL-030 (building, offered, awarded, transferred, closed). The harness changes no state. Every change in the table is made by the owner: S6 rwb-debtsale holds the lot and drives DebtSaleWorkflow, rwb-integration carries the posting and its answer, rwb-decision holds the central ledger, and P3 rwb-case holds the case state. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, Credit Administration | Owns the posting and the correction; holds Debt sale R; is the role the journey is written for |
| RW-DEBTSALE, debt sale officer | Awards the lot and closes it under R-DS-34; holds Debt sale C and R |
| RW-SALEOFF, RW-FINANCE | Read the same posting evidence; RW-FINANCE receives the provision input of R-DS-31 |
| RW-OFF, RW-TRIBE, RW-PLATADM | Read only where their rights allow; RW-OFF is the refused caller of AC6 |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | S6 runs DebtSaleWorkflow and writes the decision record, P2 carries the outbound item and the file run, P1 answers the data products, P7 holds the ledger, P3 holds the case and P4 answers the session; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the DoA is P4's |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-SAL-020 to DF-SAL-030 | debt_sale_lot | lot_no, cut_off_date, buyer_partner_id, status | Read through the rwb-debtsale contract |
| DF-SAL-031 to DF-SAL-035 | debt_sale_account | account_key, borrower_code, outstanding | Read through the rwb-debtsale contract and DP09 |
| DF-CAS-001 to DF-CAS-023 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract |
| DF-ACE-001 to DF-ACE-042 | v_ace_account (field IDs only; not read as a view) | account_key, account_code, account_status, total_balance | Read through DP01 of the rwb-source-data contract |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version | Read through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, from_state, event_code | Read through the rwb-decision contract |
| DF-INT-001 to DF-INT-013 | interaction | occurred_at, channel, direction | Read, where the run records the journey on the case timeline |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The lot and its accounts are S6's, the case is P3's, the decision log and the rule rows are P7's, and the ACE side is DP01 and DP09 of P1's contract; the harness reads them only through those contracts and never from a schema. The harness owns no table and writes no row. Lists and parameters the run reads go through the reference-data contract DP-06 and DP-07; their keys are Not specified in the source documents (DOR-RWB-ITG-E6008-ITG-20). The DP09 rows it reads are `debt_sale_lot` DF-SAL-020 to DF-SAL-030 and `debt_sale_account` DF-SAL-031 to DF-SAL-035, and the ACE side is `v_ace_account` DF-ACE-001 to DF-ACE-042 read through DP01.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award` | S6 rwb-debtsale | Starts the saga; the trigger of every criterion, with one Idempotency-Key (AC1, AC4) |
| GET | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}` | S6 rwb-debtsale | Lot number, cut-off date, winner, lot status and the recorded posting reference (AC4, AC6) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The lot's posting item, its file run and the delivered answer (AC4, AC5) |
| POST | `/api/recovery/integration/v1/admin/outbound-items/{itemId}/resend` | P2 rwb-integration | The re-post after a cleared rejection (AC5) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The sold accounts and their status, as the v_ace_account fields rwb-source-data returns (AC4) |
| GET | `/api/recovery/source-data/v1/data-products/DP09/records?caseId={caseId}` | P1 rwb-source-data | The lot and account rows, their outstanding and selling price (AC4, AC5) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time behind the ACE read (AC4) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The decision record of the derecognition and the posting, with the rule version (AC1, AC4, AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after the posting, the rejection and the correction (AC2, AC3, AC4, AC5) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's roles and rights before a read (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19). The award's own criteria, its reserve and the 54% cap are RWB-S6-E6005-* and are not asserted here.

Contract version built against: 5.0.0, the `info.version` of rwb-debtsale.yaml, rwb-integration.yaml, rwb-source-data.yaml, rwb-decision.yaml, rwb-case.yaml and rwb-access.yaml in 05 Technical architecture/Recovery Workbench API Specification v5.

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Producer | Use in the run |
|---|---|---|---|
| `rwb.debtsale.AccountsTransferred.v1` | `rwb.debtsale.events.v1` | S6 rwb-debtsale | Counts one publication after the transfer and, with the replay, proves one processed row per consumer (AC4) |
| `rwb.decision.DecisionRecorded.v1` | `rwb.decision-record.v1` | S6 rwb-debtsale through the local decision-record library (DP-03) | Proves the record of the derecognition and the posting was published and confirmed by the central ledger before the posting reference was recorded (AC4, AC5) |

The harness subscribes to both topics under one consumer group of its own, counts publications and replays each event once. The consumer effect it reads is the case through the rwb-case operation of §12.2; the inbox row counts of rwb-payment and rwb-reporting come from the consumer evidence in the run fixture, because neither consumer exposes an operation in this story. `rwb.debtsale.LotAwarded.v1` on the same topic is produced by the award and is observed by count only, since rwb-case and rwb-payment are its consumers.

#### 12.5 Workflows and activities

None added. The harness exercises DebtSaleWorkflow, S6's saga on the task queue `rwb-debtsale` in the `rwb-recovery` namespace, and observes the activities it runs after the transfer: the transfer of the accounts, the derecognition, the general ledger posting and the proceeds step, each on its owning service's queue as the saga runs them. They are stated here as observed and not built here; no workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. The sale cycle is monthly and DebtSaleWorkflow is started by the award, so the harness starts the journey with the award operation and sets no cron, overlap policy or catch-up window.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); debt_sale_lot and debt_sale_account are S6's, recovery_case is P3's, decision_log_entry and rule_row are P7's, outbound_item is P2's, and the ACE side belongs to the views behind P1's contract.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-debtsale | `POST /debt-sale-lots/{lotId}/award`, `GET /debt-sale-lots/{lotId}` | Accepts the award once per Idempotency-Key, then returns lot `LOT-SYN-2027-0001` with cut_off_date 2027-03-31, status transferred, then closed, and the posting reference once it is recorded |
| Stub for rwb-integration | `GET /admin/outbound-items`, `POST /admin/outbound-items/{itemId}/resend` | One outbound item for the lot with its file run, the delivered answer, the ledger entry id, and a resend that keeps the same itemId |
| Stub for rwb-source-data | DP01 records, DP09 records, freshness | Both accounts in v_ace_account with their derecognised status, the two debt_sale_account rows, and `status` `LOADED`, `businessDate` 2027-03-31 with `loadedAt` |
| Stub for rwb-decision | `GET /decision-log?caseId={caseId}` | One entry for the derecognition and one for the posting, each with its rule id and rule version, and the ledger confirmation |
| Stub for rwb-case | `GET /cases/{caseId}` | Case `RW-2027-000801` with its state after the posting, the rejection and the correction |
| Stub for rwb-access | `GET /me/session` | Allows RW-CREDITAD with Debt sale R; refuses RW-OFF with 403 and MSG-P4-002 |
| Posting fixture (ACE side) | The ALS and general ledger result of the job | The delivered answer of the outbound item, the ledger entry, one ALS rejection with its code and a cleared correction, at the point where the real adapters would answer |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The contract fake library version recorded as published for these stubs is Not specified in the source documents (DOR-RWB-ITG-E6008-ITG-22). The harness environment and base hosts, the stub answer for the ALS and general ledger posting reference with its shape, its reference format and its rejection codes, the retry and back-off settings, the evidence format and retention, the pass or fail gate, and the synthetic lot and account keys are Not specified in the source documents (GAP-0454; ASM-0646).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 10 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published; two consumed, `rwb.debtsale.AccountsTransferred.v1` and `rwb.decision.DecisionRecorded.v1`, counted and replayed once |
| Temporal | None added; DebtSaleWorkflow on `rwb-debtsale` exercised from the award, with its transfer, derecognition, posting and proceeds activities |
| File | The outbound item's file run, read through the rwb-integration contract, and the posting fixture of the ACE side |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H dependency DP-03 adds, RWB-PLT-E1027-CON, is a platform story delivered by the platform wave and is not repeated in the metadata H field of this story, which stays empty; the same holds for RWB-PLT-N001-CON. The one blocking dependency is the I story RWB-S6-E6008-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for a lot and holds the run lock |
| AwardDriver | Service | Calls the award once per lot with one Idempotency-Key and reads the lot before and after each step |
| PostingProbe | Service | Reads the outbound item, its file run and the delivered answer, asserts the recorded posting reference, and resends the same item after a cleared rejection |
| AceReadBack | Service | Reads DP01 and DP09 with the freshness stamp, and names every account that still shows its old status |
| EventObserver | Service | Subscribes to `rwb.debtsale.events.v1` and `rwb.decision-record.v1`, counts publications and replays each event once |
| LedgerConfirm | Service | Reads the decision log and asserts the ledger confirmation arrived before the posting reference was recorded |
| StubSet | Fake | The six stubs and the posting fixture of §12.8, generated from the published contracts with the version pinned |
| EvidenceReport | Service | Writes one report per lot keyed by story and lot_no, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as RWB-S6-E6008-APP lands, on the synthetic lot `LOT-SYN-2027-0001`, accounts `ACC-SYN-000801` and `ACC-SYN-000802`, case `RW-2027-000801` and business date 2027-03-31. The harness seeds nothing by hand and never writes a schema row. The environment and base hosts, the stub answer for the posting reference with its shape, its reference format and its rejection codes, the retry and back-off settings, the evidence format and retention, the pass or fail gate, and the synthetic lot and account keys are Not specified in the source documents (GAP-0454; ASM-0646).

**Build steps**

1. Generate the six stubs and the posting fixture from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the AwardDriver and prove the award is accepted once per Idempotency-Key and the lot read moves from awarded to transferred (AC1).
3. Add AC2 and AC3 against a case in DERECOGNISED and a case in POSTING_REJECTED_DS, asserting the posting, the provision input to Finance and the move to GL_POSTED from both.
4. Build the PostingProbe for AC4: one outbound item, its file run, the delivered answer and the recorded posting reference matched to the DP09 amount and account count (X2, X3).
5. Add the AceReadBack for AC4: both accounts with their derecognised status in v_ace_account through DP01 with the freshness stamp, so a stale product fails the run (X4).
6. Add the EventObserver for AC4: one LotAwarded and one AccountsTransferred publication, the case effect once, and a replay that changes nothing because the inbox holds one row per consumer.
7. Add the LedgerConfirm for AC5: hold the ledger answer back, assert no posting reference is recorded, then release the rejection and assert POSTING_REJECTED_DS with its exception task (X5, X6).
8. Add the resend path for AC5 and assert one outbound item, one posting reference and one ledger entry after the correction (X7).
9. Add the R-DS-34 lot close assertion, the access path for AC6 through the session read and the lot read, then the EvidenceReport and the gate, and swap a stub for the real owner as RWB-S6-E6008-APP lands (X8).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-S6-E6008-APP when it lands, and the wave entry check holds a run report keyed by story and lot_no.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-S6-001 | Error | {account} has an open deviation and cannot be sold. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-S6-001 is asserted with the account_key of the sold account when the deviation screening refuses a sale, MSG-GEN-001 with the missing field when a read is made short of a required parameter, MSG-P4-002 with the refused action on the lot read, and MSG-P7-003 when the decision record cannot be written and nothing changes.

### 15. Screens and states

The legacy story has no screen of its own for this journey, and neither does this harness: it observes the owners' operations and writes a report. The states are read through those operations, not rendered.

| State | Read through | What the run asserts |
|---|---|---|
| DERECOGNISED | rwb-debtsale lot read and rwb-case case read | The sold accounts are derecognised and the posting has not yet been accepted |
| GL_POSTING_RUN | the outbound item and its file run | The posting has left and the answer has not arrived, and no posting reference is recorded yet |
| GL_POSTED | rwb-case case read and DP01 | The posting is accepted, the reference is recorded and the accounts carry their derecognised status |
| POSTING_REJECTED_DS | rwb-case case read | The rejection is held with its exception task and the two-working-day clock of R-DS-32 runs |
| POSTING_CORRECTED | the outbound item and its file run | One resend of the same item, one posting reference and one ledger entry |
| LOT_CLOSED | rwb-debtsale lot read, DF-SAL-030 | The lot closes under R-DS-34 with realized recovery by lot and by buyer |

The harness renders no screen. SCR-25 Lot builder and SCR-26 Award are RWB-S6-E6005's and RWB-S6-E6009's and neither builds nor reads them here. SCR-25 states empty, loading, error and no access: Not specified in the source documents (CG-ALL-1076). SCR-26 states empty, loading, error and no access: Not specified in the source documents (CG-ALL-1077). What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0454; ASM-0646).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-008-01-ITG | AC1 (legacy); ITG AC1, ITG AC4 | End to end | One awarded lot with two accounts, the transfer and the posting steps live |
| TC-E6-008-02-ITG | AC2 (legacy); ITG AC2 | Integration | A case in DERECOGNISED with a GL posting run |
| TC-E6-008-03-ITG | AC3 (legacy); ITG AC3 | Integration | A case in POSTING_REJECTED_DS with the cause cleared |
| TC-E6-008-04-ITG | ITG AC5 (legacy AC4 is RWB-S6-E6008-APP's) | Integration | The ledger is held back, then an ALS rejection and a re-post |
| TC-E6-008-05-ITG | Access; ITG AC6 | Component | RW-OFF caller without Debt sale R |
| TC-E6-008-06-ITG | Principle 5; ITG AC5 | Integration | A forced decision-record failure at the point of no return |
| TC-E6-008-07-ITG | ITG AC7; BR1 to BR8 | Component | Not specified in the source documents (NEWAC-RWB-ITG-E6008-ITG-AC7) |
| TC-E6-008-08-ITG | ITG AC8 | Integration | Not specified in the source documents (NEWAC-RWB-ITG-E6008-ITG-AC8) |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic lot, its accounts, the business date, the posting reference, the rejection codes, the retry settings and the report layout are data.
- No personal data in logs, events or reports: every key is synthetic, and the events carry IDs and facts only.
- ACE data only through the P1 contract: DP01 and DP09 with their freshness stamp, never a direct view read and never another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11, DP-13).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand or sets a state it then asserts.
- A failing criterion is fixed in the owning service or raised as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-008 Derecognize and post to the general ledger | Recovery Workbench User Stories Epics 3 to 8 v3, lines 9020 to 9116 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1, AC2 and AC3, verbatim | The same, lines 9039 to 9055 | Section 7, AC1 to AC3, marked (legacy RWB-E6-008 AC1) to (legacy RWB-E6-008 AC3) |
| Legacy AC4, Not recorded, and its test case TC-E6-008-04 | The same, lines 9057 to 9061 and 9110 | AC5 asserts the same failure here; the legacy AC stays with RWB-S6-E6008-APP (section 19) |
| Legacy test cases TC-E6-008-01 to TC-E6-008-06 | The same, lines 9107 to 9112 | Copied as -ITG in section 16 |
| FEAT-DBS-12 Derecognize and post to the general ledger | Epics 3 to 8 Specification v3, line 103 | Sections 1 and 2 |
| REQ-S6-007 and REQ-S6-008 | Business Requirements Program v4, lines 383 and 384 | Section 8, BR7 |
| R-DS-30 to R-DS-34 | Business Rules and Routing Logic v4, lines 320 to 324 | Sections 8 and 9 |
| INT-03 Core bank (ALS) and INT-16 GL | Epics 3 to 8 Specification v3, lines 230 and 233 | Sections 2, 12.8 and 13 |
| DF-SAL-020 to DF-SAL-030, DF-SAL-031 to DF-SAL-035, DF-CAS-001 to DF-CAS-023, DF-ACE-001 to DF-ACE-042, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015, DF-INT-001 to DF-INT-013 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DP-03, DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records v4 | Sections 12.4, 12.2 and 8: outbox and inbox on Kafka, contract-first REST with one hop and 2 s, local decision record plus central ledger |
| DebtSaleWorkflow and the pivot | Architecture v5 slides 19 and 41; Temporal and Drools design slides 22 and 25 | Sections 2, 8, 12.5 and 13 |

### 19. Out of scope

- RWB-S6-E6008-CON and RWB-S6-E6008-APP: the build of the derecognition, the general ledger posting, the provision input and the decision record.
- The lot award and its price test (RWB-S6-E6005-*), and SCR-25 Lot builder and SCR-26 Award (RWB-S6-E6005, RWB-S6-E6009).
- The buyer put-back claim (RWB-E6-009), the sale agreement (RWB-E6-006) and the case close (RWB-E6-010).
- The CONTRACTS and the screens of S6, and the S6 CON, APP and DB stories.
- The general ledger and ALS adapters as products: the outbound item, its file run and the ACE integration path are P2's own stories, and this story only reads them through the contract.
- The 30 ACE views and ACE ingestion (RWB-ACE-001); DP01 and DP09 are read through P1's contract only.
- Platform deployment and configuration, and the platform H dependencies named in section 13.
