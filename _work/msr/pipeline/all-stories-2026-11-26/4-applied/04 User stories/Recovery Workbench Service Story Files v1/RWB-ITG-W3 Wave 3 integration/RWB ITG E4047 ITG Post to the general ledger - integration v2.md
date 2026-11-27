# RWB-ITG-E4047-ITG Post to the general ledger

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E4047-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-047 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P8-E4047-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-047 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-ITG-E4047-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want one repeatable cross-service harness that **posts the accounting entries for a seeded settlement, a seeded asset sale and a seeded write-off to the general ledger through rwb-payment's posting step and rwb-integration's outbound interface, records the posting reference against the proceeds, and asserts the decision record that carries the rule version, against the owning services' published contracts and their fakes**, so that **the ledger is proven to receive every entry from the Workbench through the outbound interface and never through a direct write, a settlement, a sale or a write-off is proven to leave a posting reference behind, and no posting is proven to move without its decision record**.

### 2. Business rationale

A settlement that clears but never reaches the general ledger leaves the account open in the books after the customer has paid, and a write-off that is approved but never posted leaves the provision standing against a debt the bank has already given up on. Both outcomes depend on the same chain: the payment rows read from `v_ace_payment`, the proceeds match that rwb-payment drives as the `postProceeds` saga step, the posting item that leaves through rwb-integration's outbound interface to the general ledger, the posting reference the ledger returns, and the decision record that rwb-decision holds with its rule version. The chain crosses four services and three call types, and a defect at any hop shows up as an unposted settlement, an unreconciled sale or a write-off that no committee can trace to the books.

This story owns the harness that proves the chain as the legacy key describes it. It carries AC1 of RWB-E4-047 into evidence: the accounting entries for settlements, sales and write-offs reach the ledger, and the result is written to the decision log with the rule version. It proves the settlement route on R-SET-14 and its final installment on R-SET-18, the asset sale route on R-DIS-54, the debt sale posting run on R-DS-31 and the write-off posting and its reference on R-WO-21, with the rejection and re-posting path of R-DS-32, R-DS-33, R-WO-22 and R-WO-23 held as the exception the run must not pass over. It serves REQ-S2-008, REQ-S6-008, REQ-S7-005 and REQ-DRI-001, and it carries FEAT-PAY-07 into evidence.

The harness is decoupled the same way the services are. It never reads another service's table (DP-01): the payment rows come from rwb-source-data, which owns the ACE view contract, the proceeds, payments, posting item and delivery come from rwb-payment and rwb-integration, and the decision record comes from rwb-decision. It calls each owner's base `/api/recovery/<short>/v1` and never a monolith base, and it calls through the gateway-bff composite route where a screen would (DP-19). Every call is one hop with a 2 s budget. The ACE payment row is read through rwb-source-data's products contract and not through a view of the harness's own (DP-05), and the decision record is read from rwb-decision and its shared topic (DP-03).

### 3. Preconditions

- The published contracts of rwb-payment, rwb-integration, rwb-source-data, rwb-case, rwb-decision, rwb-access, rwb-debtsale and rwb-writeoff are in the contract registry, and a WireMock stub set is generated from each one and its version pinned.
- The contract fakes of section 12.8 are published and reachable before the first run, including the payment and file event stubs.
- A settlement on a seeded case, an asset sale on a second seeded case and a write-off on a third are seeded through the owning services' published operations only. The seeding set, the harness environment specification and the fixture contents are not specified in the source documents (GAP-0433; ASM-0609).
- The seeded account carries the payment rows the run reads from `v_ace_payment`, and the data product code that serves them is not specified in the source documents (GAP-0433; ASM-0609).
- The general ledger is modelled by an outbound item on the interface config in rwb-integration and, where the configured interface is a file, by an outbound fixture. The interface identifier, the transport, the posting file layout and the test endpoint are not specified in the source documents (GAP-0433; ASM-0609).
- The field that carries the posting reference the ledger returns is not specified in the source documents (GAP-0433; ASM-0609).
- The entry set that each route posts to the ledger is not specified in the source documents (GAP-0433; ASM-0609).
- The rule package in force carries R-SET-14, R-SET-18, R-DIS-54, R-DS-31, R-WO-21, R-WO-22 and R-WO-23, and the version of each is readable on the decision record that cites it.
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the write-off and posting right and for a caller without it.
- No build dependency and no contract dependency. Day 1, with the fakes in place from the first run, and the rwb-payment fake replaced by the real service when RWB-P8-E4047-APP lands. rwb-debtsale is a wave 3 service; rwb-writeoff is wave 4, so the write-off route runs on its fake in wave 3 and is rerun when S7 lands, and neither is an I story of this key.

### 4. Flow

1. Harness: seeds the settlement case, the asset sale case and the write-off case through the owning services' published operations only; the seeding set and its environment are not specified in the source documents (GAP-0433; ASM-0609).
2. Harness: reads the payment rows of the seeded account through `GET /api/recovery/source-data/v1/data-products/{productCode}/records` and asserts the payment code, the payment date and the payment amount the settlement and the sale need (DP-05); the data product code for `v_ace_payment` is not specified in the source documents (GAP-0433; ASM-0609).
3. Harness: reads the payments the case holds through `GET /api/recovery/payment/v1/cases/{caseId}/payments`, proving the payment side of the match is the owner's and not the harness's.
4. Harness: drives the posting for the settlement proceeds with `POST /api/recovery/payment/v1/proceeds/{proceedsId}/match` and reads the proceeds and the posting reference recorded against them back with `GET /api/recovery/payment/v1/proceeds`. In production the same fact arrives as `rwb.payment.ProceedsMatched.v1` on the `postProceeds` saga step, and the harness asserts that event too.
5. Harness: asserts the general ledger posting item as an outbound item on the general ledger interface config through `GET /api/recovery/integration/v1/admin/outbound-items`, naming the case and the proceeds, and its delivery through `GET /api/recovery/integration/v1/admin/outbox/deliveries`.
6. Harness: subscribes to `rwb.integration.events.v1` and asserts `rwb.integration.FileDelivered.v1` for the posting item, or `rwb.integration.FileFailed.v1` where the owner recorded a failure the run must not pass over.
7. Harness: reads `GET /api/recovery/decision/v1/decision-log` for each case and asserts exactly one record for each posting, naming R-SET-14, R-SET-18, R-DIS-54, R-DS-31 or R-WO-21 and its rule version, and asserts `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` for it, reaching the ledger inside the 5-minute window the design names.
8. Harness: runs the final installment path of the same settlement loop: a treatment at PAYMENT_PART_RECEIVED whose cumulative receipt equals the settlement amount, matched and posted the same way, with the case at PAYMENT_CLEARED (R-SET-18).
9. Harness: runs the asset sale path: the sale proceeds are applied to the case and the loan account, the vendor fee is matched, the case reaches PROCEEDS_APPLIED and the posting item is on the ledger interface (R-DIS-54).
10. Harness: runs the debt sale path: it awards the seeded lot through `POST /api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award`, after derecognition the general ledger posting run posts to the ledger, the provision input is sent to Finance, and the case reaches GL_POSTED (R-DS-31). The Finance provision feed input is not specified in the source documents (GAP-0433; ASM-0609).
11. Harness: runs the write-off path: it records the committee decision through `POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision`, the approved write-off posts to the core system and the ledger, the posting reference is recorded when both return it, and the case reaches POSTED (R-WO-21). The write-off path runs on the S7 fake until rwb-writeoff lands in wave 4.
12. Harness: runs the rejection path: the ledger rejects the posting, the posting is held, an exception task is raised and the case reaches POSTING_REJECTED (R-DS-32, R-WO-22); the corrected cause is re-posted and the case returns to POSTING_PENDING or GL_POSTED (R-DS-33, R-WO-23).
13. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a caller without the write-off and posting right.
14. Harness: publishes the per-run evidence report keyed by story and business date, with the criterion and its assertions, and gates the wave on the result. The evidence format and its retention are not specified in the source documents (GAP-0433; ASM-0609).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC1 |
| X2 | The proceeds match returns no proceed, or the posting reference is missing from it | The run fails and the report names the proceeds and the operation; the run is not marked passed | None | AC1 |
| X3 | No outbound item is created for the case and the proceeds on the general ledger interface config | The run fails on AC1 and the report names the interface config and the proceeds | None | AC1 |
| X4 | The outbound item stays undelivered, or `rwb.integration.FileFailed.v1` arrives | The run fails and the report names the outbound item and the failure the owner recorded | None | AC1 |
| X5 | The payment rows read through the rwb-source-data product do not match the seeded payments | The run fails and the report names the payment code and the product version | None | AC1 |
| X6 | More or fewer than one decision record exists for a posting, or its rule version is missing | The run fails and the report names the records it found | None | AC1 |
| X7 | The decision record does not reach the ledger inside the 5-minute window | The run fails and the report names the record and the elapsed time | None | AC1 |
| X8 | The final installment path does not reach PAYMENT_CLEARED, or the settlement amount is not the matched total | The run fails on the R-SET-18 path and the report names the treatment and the two amounts | None | AC1 |
| X9 | The sale proceeds are not applied to the case and the loan account, or the vendor fee is unmatched | The run fails on the R-DIS-54 path and the report names the proceeds and the case | None | AC1 |
| X10 | The debt sale posting run does not reach GL_POSTED, or no provision input is sent to Finance | The run fails on the R-DS-31 path and the report names the lot and the posting run | None | AC1 |
| X11 | The write-off posts but no posting reference is recorded, or only one of the core system and the ledger returns it | The run fails on the R-WO-21 path and the report names the write-off and both responses | None | AC1 |
| X12 | A rejection does not hold the posting or raise the exception task, or the corrected cause is not re-posted | The run fails on the R-DS-32, R-WO-22, R-DS-33 and R-WO-23 paths and the report names the rejection and the retry count | None | AC1 |
| X13 | A caller without the write-off and posting right is authorised | The run fails on the access check and the report names the operation | MSG-P4-002 | AC1 |
| X14 | A real service is reachable but its contract version differs from the registry | The run fails before any assertion and the report names the service and both versions | None | AC1 |

The report text is for the wave entry check and is not part of the message standard. The rule set carries no message ID for R-SET-14, R-SET-18, R-DIS-54, R-DS-31, R-WO-21, R-WO-22 or R-WO-23, so the harness asserts state, data and the decision record and not a message; the business messages this journey can produce are in section 14 and belong to the owning services.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only wait is one I story, RWB-P8-E4047-APP |
| Negotiable | The general ledger interface fixture, the entry set mapping, the seeding set and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The posting of settlements, sales and write-offs to the ledger, and its record, are proven end to end before the wave opens |
| Estimable | One harness runner, one stub set, one interface fixture, one event probe, one report |
| Small | Fits in one sprint with its tests |
| Testable | The criterion runs against its fakes and again against the real owner as RWB-P8-E4047-APP lands |

### 7. Acceptance criteria

```gherkin
Feature: Post to the general ledger

  Background:
    Given a seeded settlement, a seeded asset sale and a seeded write-off are in place for the run
    Given the seeded account carries the payment rows the run reads from "v_ace_payment"
    Given the rule package in force carries R-SET-14, R-SET-18, R-DIS-54, R-DS-31, R-WO-21, R-WO-22 and R-WO-23
    Given the contract fakes of section 12.8 are published and their versions are pinned

  Scenario: AC1 Post to the general ledger (legacy RWB-E4-047 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then posts the accounting entries for settlements, sales and write-offs to the ledger
    Then the system writes the result to the decision log with the rule version
```

AC2 of the legacy key ("Not recorded") is owned by RWB-P8-E4047-APP and is not restated here; the harness asserts its outcome as the decision-record failure path of AC1 rather than as a second criterion.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A settlement payment is matched and posted when it equals the settlement amount, and the final installment is matched and posted the same way | R-SET-14; R-SET-18 |
| BR2 | Asset proceeds are applied to the case and the loan account, and the vendor fee is matched | R-DIS-54 |
| BR3 | After derecognition in a debt sale, the general ledger posting run posts to the ledger and sends the provision input to Finance | R-DS-31 |
| BR4 | An approved write-off posts to the core system and the ledger, and the posting reference is recorded when both return it | R-WO-21 |
| BR5 | A rejection holds the posting and raises an exception task, and a corrected cause is re-posted | R-DS-32; R-DS-33; R-WO-22; R-WO-23 |
| BR6 | The Workbench writes nothing to the ledger directly: the entries leave through the outbound interface, and every item is logged, retried and placed in an exception queue after the retry limit | REQ-DRI-006; REQ-DRI-007 |
| BR7 | The decision record carries the rule and its version and is written with the change in one transaction, and no posting proceeds without it | REQ-DRI-001; REQ-DRI-005; R-UNI-39 |

The mapping of each route to its general ledger entry set is not named by any source read; it is held by the owning service as data and is asserted by the harness only through the posting item and its delivery.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| PAYMENT_RECEIVED | PAYMENT_MATCHED | amount_received = settlement_amount | PAYMENT_CLEARED (R-SET-14) |
| PAYMENT_PART_RECEIVED | FINAL_INSTALLMENT_RECEIVED | cumulative_received = settlement_amount | PAYMENT_CLEARED (R-SET-18) |
| PROCEEDS_POSTED | PROCEEDS_APPLIED | proceeds applied and vendor fee matched | PROCEEDS_APPLIED (R-DIS-54) |
| DERECOGNISED | GL_POSTING_RUN | any | GL_POSTED (R-DS-31) |
| POSTING_PENDING | ALS_POSTING_CONFIRMED | the core system and the ledger both return a reference | POSTED (R-WO-21) |
| POSTING_PENDING or DERECOGNISED | POSTING_REJECTED | the core system or the ledger rejects the posting | POSTING_REJECTED (R-DS-32, R-WO-22) |

These are the owners' states. rwb-payment moves the payment, proceeds and posting states, rwb-writeoff moves the write-off posting states, rwb-debtsale moves the debt sale posting state, and rwb-case reads the result. The harness changes none of them itself: it seeds through the owners' published operations, drives the match through the rwb-payment contract, and then asserts the states the owners reached. A state the harness set by hand would prove nothing, so the report names the owner and the operation that made each move.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD, RW-WRITEOFF, SY-DATALOAD and roles with Write-off and posting U | Drive the proceeds match and read the proceeds, the payments, the posting reference and the outbound item through the owning contracts |
| RW-CASEOWN, RW-TEAMMGR and roles with Case record R | Read the same journey evidence, including the case state and the decision record |
| QA lead | Owns the harness configuration, the general ledger interface fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-payment, rwb-integration, rwb-source-data, rwb-decision and rwb-access make every state change the harness asserts |
| No approval level from the delegation of authority applies | The harness takes no business decision; the write-off approval and the debt sale award belong to their own stories |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | status (PAYMENT_CLEARED, PROCEEDS_APPLIED, POSTED, POSTING_REJECTED, GL_POSTED) | Read, through the rwb-case contract |
| DF-ACE-043 to DF-ACE-054 | v_ace_payment | payment_code, account_key, payment_date, payment_amount, payment_channel, capital_amount | Read, through the rwb-source-data products contract (DP-05) |
| DF-OPS-168 to DF-OPS-177 | outbound_item | interface_id, idempotency_key, status, the posting reference | Read, through the rwb-integration admin operation |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | decision_code, rule_id, rule_version, model_version | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row | rule_id, rule_version, route_set, from_state, event_code | Read, through the rwb-decision rule contract |

Field IDs are those in the Logical Data Model and Data Dictionary, taken from the legacy key. The `proceeds` and `payment` tables are rwb-payment's and are read through its contract; the harness owns no table and writes no row directly (DP-01, DP-05). The Workbench writes nothing to the ledger, which is outside the Workbench and reached only through the outbound interface.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/payment/v1/proceeds/{proceedsId}/match` | P8 rwb-payment | Drive the posting for the settlement or the sale proceeds (AC1) |
| GET | `/api/recovery/payment/v1/proceeds` | P8 rwb-payment | The proceeds and the posting reference recorded against them (AC1) |
| GET | `/api/recovery/payment/v1/cases/{caseId}/payments` | P8 rwb-payment | The payments on the case (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The general ledger posting item and its interface config (AC1) |
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | The delivery of that item (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The payment row from `v_ace_payment` (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case state after each posting (AC1) |
| POST | `/api/recovery/debtsale/v1/debt-sale-lots/{lotId}/award` | S6 rwb-debtsale | Award the seeded lot that raises the derecognition and the posting run (AC1) |
| POST | `/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` | S7 rwb-writeoff | Record the committee decision that raises the write-off posting; the S7 fake until wave 4 (AC1) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record with the rule ID and version (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role and scope, including the refusal path (AC1) |

The data product code that carries the `v_ace_payment` row is not specified in the source documents (GAP-0433; ASM-0609). Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream; where a screen would compose them, the harness calls the gateway-bff composite route (DP-19). No operation is invented in this story.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the posting through the rwb-payment contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.payment.ProceedsMatched.v1` | `rwb.payment.events.v1` | P8 rwb-payment | The fact that raises the posting (AC1) |
| `rwb.integration.FileDelivered.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The posting delivered to the general ledger (AC1) |
| `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The posting failed, which the run must not pass over (AC1) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | every service, through the local decision-record library | The record reaching the ledger within 5 minutes (AC1) |

All four carry IDs and business facts only, keyed by caseId, and the harness asserts that no personal data is present (DP-03, DP-09).

#### 12.5 Workflows and activities

None added. The harness exercises the `postProceeds` saga step and the `confirmBookings` activity on queue rwb-payment, which drive the posting for the settlement and the sale, and the `deliverFile` activity on queue rwb-integration, which delivers the posting item to the general ledger. The write-off posting is rwb-writeoff's and is exercised through its own contract. It asserts their effects through the services' contracts and the owners' topics. No workflow, activity or Schedule is created, changed or owned by this story.

#### 12.6 Schedules

None added. R-SET-14, R-SET-18, R-DIS-54, R-DS-31, R-WO-21, R-WO-22 and R-WO-23 are triggered by facts and by the posting run, and this story sets no cron, overlap policy or catch-up window. The month-end close window the debt sale posting waits for is not specified in the source documents (GAP-0433; ASM-0609).

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the proceeds, payments and posting item are rwb-payment's, the interface config, outbound items and deliveries are rwb-integration's, and the payment row is ACE's, read through rwb-source-data's contract (DP-05).

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-payment | `POST /proceeds/{proceedsId}/match`, `GET /proceeds`, `GET /cases/{caseId}/payments`, `rwb.payment.events.v1` | Day-1 runs of AC1 for the settlement, the final installment, the sale and the write-off before RWB-P8-E4047-APP is live |
| WireMock stub for rwb-integration | `GET /admin/outbound-items`, `GET /admin/outbox/deliveries`, `rwb.integration.events.v1` | Day-1 assertions on the posting item, its interface config and its delivery |
| WireMock stub for rwb-source-data | `GET /data-products/{productCode}/records` | Day-1 assertions on the `v_ace_payment` rows |
| WireMock stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertions on the case state after each posting |
| WireMock stub for rwb-debtsale | `POST /debt-sale-lots/{lotId}/award` | Day-1 assertion of the lot award that raises the derecognition and the posting run |
| WireMock stub for rwb-writeoff | `POST /write-offs/{writeOffId}/committee-decision` | Day-1 assertion of the write-off posting until rwb-writeoff lands in wave 4 |
| WireMock stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record per posting with its rule version |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and refusal path |
| Payment event stub | `rwb.payment.ProceedsMatched.v1` | The posting fact where the environment does not run the match |
| File event stubs | `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` | The delivered and failed posting where the environment does not run the deliverFile activity |
| General ledger outbound fixture | The outbound item on the configured general ledger interface | The posting and its reference, where the interface is a file |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The general ledger interface identifier and transport, the posting file layout and its result codes, the entry set per route, the posting reference field, the data product code for `v_ace_payment`, the seeding set, the harness environment and the evidence format and retention are not specified in the source documents (GAP-0433; ASM-0609).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 11 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget, composed through gateway-bff where a screen would (DP-19) |
| Kafka | None published; `rwb.payment.ProceedsMatched.v1`, `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` and `rwb.decision-record.DecisionRecorded.v1` consumed (DP-03, DP-09) |
| Temporal | None added; the `postProceeds` saga step and the `confirmBookings` activity on queue rwb-payment and the `deliverFile` activity on queue rwb-integration exercised |
| File | The general ledger interface as an outbound fixture, where the configured interface is a file |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The blocking dependency is the one I story, RWB-P8-E4047-APP: until it is live the run uses the rwb-payment stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy behaviour. The harness owns no schema (DP-01) and reads the proceeds, the payments, the posting item, the delivery and the decision record from their owners only. The decision record is read from rwb-decision's contract and the shared topic `rwb.decision-record.v1` rather than from a local log table (DP-03). The `v_ace_payment` row is read through rwb-source-data's product, which owns the ACE view contract, and not through a view of the harness's own (DP-05). Every call sits on the owner's per-service base with a single hop, and the composed reads a screen would make are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| PostingJourneyRunner | Job | Runs the owned criterion and its four posting routes in order for a business date and holds the run lock |
| StubSet | Fake | The eight WireMock stubs and the payment and file event stubs, each generated from the published contract with the version pinned |
| LedgerInterfaceFixture | Fixture | The outbound item on the configured general ledger interface and the reference it returns, keyed by case and proceeds |
| EventProbe | Service | Consumes `rwb.payment.events.v1`, `rwb.integration.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, on one seeded settlement case, one seeded asset sale case and one seeded write-off case, each with its account and its `v_ace_payment` rows. The environment, the seeding set, the general ledger interface fixture and the evidence retention are not specified in the source documents (GAP-0433; ASM-0609). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the eight stubs and the payment and file event stubs from the published contracts, pin each contract version in the run report and fail the run on a version mismatch (X1, X14).
2. Build the LedgerInterfaceFixture and prove one posting item from creation to delivery for a business date (X3, X4).
3. Build the PostingJourneyRunner for the settlement route on R-SET-14: read the payment row and the case payments, drive the match, assert the proceeds and the posting reference, the outbound item and its delivery, the case at PAYMENT_CLEARED and one record naming R-SET-14 with its version (X2, X5, X6, X7).
4. Add the final installment route on R-SET-18 from PAYMENT_PART_RECEIVED with `cumulative_received` equal to the settlement amount (X8).
5. Add the asset sale route on R-DIS-54: the proceeds applied to the case and the loan account, the vendor fee matched and the case at PROCEEDS_APPLIED (X9).
6. Add the debt sale route on R-DS-31: the posting run, the provision input to Finance and the case at GL_POSTED (X10).
7. Add the write-off route on R-WO-21: the posting to the core system and the ledger, the posting reference recorded when both return it, and the case at POSTED (X11).
8. Add the rejection route on R-DS-32 and R-WO-22 with the exception task, and the re-posting on R-DS-33 and R-WO-23 with the retry limit (X12).
9. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a caller without the write-off and posting right (X13).
10. Add the EvidenceReport and the gate, then swap the rwb-payment stub for the real service when RWB-P8-E4047-APP lands and rerun the criterion and its four routes.

**Feature switch.** The legacy key names no feature switch for this behaviour. The journey runs behind the platform feature-flag library as the wave releases it; the flag key for this harness is not specified in the source documents (GAP-0433; ASM-0609).

**Done when.** The tests of section 16 pass for AC1 and for its four posting routes; the criterion passes against the fakes on Day 1 and again against rwb-payment when RWB-P8-E4047-APP lands; and the wave entry check holds a run report keyed by story and business date with the contract and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the posting cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the write-off and posting right, or the case is outside their scope | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the request | Enter {field}. |

R-SET-14, R-SET-18, R-DIS-54, R-DS-31, R-WO-21, R-WO-22 and R-WO-23 carry no message ID in the rule set, so the harness asserts the state, the data, the posting reference and the decision record and names the message ID only where the owning service returns one of the three above. The harness produces none of these messages itself.

### 15. Screens and states

SCR-28 Proceeds matching shows the states this journey sets:

| State | What the user sees and does |
|---|---|
| Loading | The proceeds list is being read; no match is recorded |
| matched | The proceeds are matched to the case and the posting reference is recorded against them |
| unmatched | The proceeds are not matched; no posting exists for them |

SCR-28 Proceeds matching carries the states Loading, matched and unmatched in the legacy key. The case states PAYMENT_CLEARED, PROCEEDS_APPLIED, POSTED, POSTING_REJECTED and GL_POSTED are read through the rwb-case contract and shown on the case record view, whose screen ID is not named for this feature in the source documents (GAP-0433; ASM-0609).

The harness renders no screen. It reads these states through the rwb-payment, rwb-integration, rwb-case and rwb-source-data contracts, so a passed run means the screen has the right data behind it. What the wave entry check looks at instead is the evidence report, whose format and retention are not specified in the source documents (GAP-0433; ASM-0609).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-047-01-ITG | AC1, BR1, BR2, BR6, BR7 | Integration | Seeded settlement, sale proceeds and write-off posting |
| TC-E4-047-02-ITG | AC2 (owned by RWB-P8-E4047-APP), BR7 | Integration | Decision log forced to fail; MSG-P7-003 |
| TC-E4-047-03-ITG | Access | Component | A role without the right; MSG-P4-002 |
| TC-E4-047-04-ITG | Principle 5 | NFR | Forced decision-log write failure; nothing moves |

The four cases above are the ITG copies of TC-E4-047-01 to TC-E4-047-04 and carry their data unchanged. TC-E4-047-01-ITG is the copy that covers AC1, the criterion this story owns, and it carries the four posting routes of section 4 as the same loop; TC-E4-047-02-ITG covers AC2, which belongs to RWB-P8-E4047-APP and is asserted here only as the decision-record failure path. The full legacy tests, with their Given, When and Then, are in `Recovery Workbench Test Cases v8.xlsx`, tab Story test cases, under the legacy test case IDs TC-E4-047-01 to TC-E4-047-04.

### 17. Guardrails

- No business value in code: the rule versions, the general ledger interface fixture, the entry set mapping, the seeding set, the eligible states and the result code mappings are data.
- No personal data in logs, fixtures, reports, tests or prompts: the events carry IDs and business facts only, and the harness asserts the absence of personal data.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and the payment row is ACE's, read through rwb-source-data's product (DP-05).
- The Workbench writes nothing to the ledger: every entry leaves through the outbound interface, and every item is logged, retried and placed in an exception queue after the retry limit (REQ-DRI-006; REQ-DRI-007).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would.
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never sets a payment, proceeds, posting, case or decision state by hand.
- A failing assertion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S2-008 | Booked terms, settled accounts and released collateral are posted to their systems of record without re-keying | Business Requirements Program v5, section 5.9 | FEAT-PAY-07 | D6.4 Settlement | R-SET-14, R-SET-18 | TC-E4-047-01-ITG |
| REQ-S6-008 | Data transfer, derecognition and the general ledger posting follow the award without re-keying | Business Requirements Program v5, section 5.13 | FEAT-PAY-07 | D8.4 Debt sale | R-DS-31 | TC-E4-047-01-ITG |
| REQ-S7-005 | Approved write-offs post to the core system and the general ledger, the provision is released, and completeness is published | Business Requirements Program v5, section 5.14 | FEAT-PAY-07 | D9 Write-off | R-WO-21 | TC-E4-047-01-ITG |
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Business Requirements Program v5, section 5.7 | FEAT-PAY-07 | D6.4 Settlement; D8.4 Debt sale; D9 Write-off | R-SET-14, R-DIS-54, R-DS-31, R-WO-21 | TC-E4-047-01-ITG, TC-E4-047-02-ITG, TC-E4-047-04-ITG |

### 19. Out of scope

- AC2 of the legacy key, which is owned by RWB-P8-E4047-APP and is asserted here only through the decision-record failure path.
- The rwb-payment behaviour itself: the proceeds match, the posting step, the booking confirmation and the payment state are the service story RWB-P8-E4047-APP.
- The general ledger interface build itself: the interface config, the posting file layout, the transport and the retry and exception queue are the P2 stories of the same interface.
- The production payment endpoint and posting step, which are the owners' code and not part of a harness.
- The contract baselines of rwb-payment, rwb-integration, rwb-source-data, rwb-decision and rwb-access, which other stories publish and this one only consumes.
- The platform configuration: the Kafka topics, the Temporal namespace and queues, and the feature-flag library, which the platform wave delivers.
- The month-end close window the debt sale posting waits for, which is Finance's calendar and not this story's.
- The ledger's own accounting rules: the entry set each route posts, the accounting treatment and the reconciliation to the books belong to the ledger and to the owning service.
- Any production screen, endpoint, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the evidence format and its retention, and the feature flag key: carried as a gap and an assumption, not decided here.
