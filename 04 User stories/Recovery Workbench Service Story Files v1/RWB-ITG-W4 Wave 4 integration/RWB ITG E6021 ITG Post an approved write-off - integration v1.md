# RWB-ITG-E6021-ITG Post an approved write-off

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E6021-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-021 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S7-E6021-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E6-021 for the wave 4 integration epic. This is the wave-4 proof that an approved write-off posts through rwb-integration's ACE integration path to ALS with a recorded posting reference and to the general ledger, that the posting reference comes back through the ACE views as DP13 Money and closure, that `WriteOffApproved` reaches its consumers once, and that a rejected posting re-posts on the same outbound item without a second posting. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **Credit Administration officer (RW-CREDITAD)**, I want **the approved write-off proven end to end on the real services: leaving rwb-writeoff as one outbound item on rwb-integration's ACE integration path with a recorded posting reference, the posting read back from `v_ace_write_off` through DP13 Money and closure, `WriteOffApproved` published once and consumed once by rwb-case and once by rwb-payment, the approved population equal to the posted population, and the point of no return held until the central ledger confirms the decision record**, so that **an approved write-off leaves the book once, on the date the ledger returns, with its provision released, and no case is ever reported as posted on a partial answer**.

This story builds the harness and the evidence, and nothing else. The posting itself is S7's: state `POSTING_PENDING`, `POSTED` and `POSTING_REJECTED`, the posting reference, the provision release and the population reconciliation are built in RWB-S7-E6021-APP and its contract story RWB-S7-E6021-CON. The ACE integration path, the outbound item and its file run belong to P2 rwb-integration; the write-off's posting facts come back from ACE through P1 rwb-source-data as DP13; the decision record comes from P7 rwb-decision, the case state from P3 rwb-case and the right from P4 rwb-access. The harness writes no code in any service, owns no schema, and asserts what the services answer.

### 2. Business rationale

An approved write-off that does not reach the core system and the general ledger leaves the bank carrying a loss it has already decided to take: the committee has approved, the pack is closed, and the account still sits on the book with its provision, its ageing and its recovery route. The reverse failure is worse. A posting that goes out twice, or a case marked posted while the ledger has returned nothing, breaks the tie between the approved population and the posted population, and REQ-S7-005 asks for exactly that tie: approved write-offs post, the provision is released and completeness is published. The monthly cut-off means the window is narrow; a posting that fails on the last working day has two working days (R-WO-22) before the exception loop opens.

The failure this story exists for is the one no single service can see. S7 can prove that its own state moved to `POSTED`; only the pair of services proves that the outbound item on the ACE integration path carries one posting and not two, only the ACE views prove that the general ledger holds the posting under the same write-off, only the consumers' inboxes prove that `WriteOffApproved` had its effect once, and only the two populations side by side prove that the committee's approval was posted in full. Posting is the point of no return in the design, and the design makes it wait for the central ledger to confirm the decision record in strict mode; a harness that stubbed the ledger would never see that gate at all.

The harness is decoupled the way the services are. The write-off is called on its own base `/api/recovery/writeoff/v1`, the outbound items on `/api/recovery/integration/v1/admin`, ACE data only through P1's DP13 data-product contract (DP-05) and never from a view or another service's schema, the decision record through P7's log read (DP-03, ADR-022), the case through P3 and the right through P4; every call is one hop with a 2 s budget (DP-13, ADR-020), the event is the outbox-and-inbox pair with CloudEvents on `rwb.writeoff.events.v1` (ADR-015), and where a screen exists the path is the gateway-bff composite route (DP-19). It carries REQ-S7-005, NFR-026 and NFR-033 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S7 rwb-writeoff (the committee decision), P2 rwb-integration (outbound items and resend), P1 rwb-source-data (DP13 records and freshness), P7 rwb-decision (the decision log), P3 rwb-case (the case) and P4 rwb-access (the session) are in the contract registry, and a contract fake is generated from each one with its version pinned.
- rwb-writeoff runs `WriteOffWorkflow` on task queue `rwb-writeoff` with its posting, provision-release and reconciliation steps, and holds the JOB-16 write-off scan Schedule on the 3rd working day (Arch v5 slides 20 and 44; Temporal design slide 23); this story observes both and changes neither.
- The topic `rwb.writeoff.events.v1` exists with its retry and `.dlt` topics, and the consumers' inbox tables are in place: rwb-case, rwb-payment and rwb-reporting (Arch v5 slide 43, event 24).
- The data product DP13 Money and closure is published by rwb-source-data with `v_ace_write_off` as its source and a freshness stamp, so the posting can be read back from ACE (Integrations sheet INT-16 GL).
- The committee decision for the synthetic write-off is recorded with the rule version in force, and rwb-decision holds the matching entry so the posting step has a decision record to confirm (ADR-022).
- The ALS and the general ledger answer fixture of §12.8 stands in for the real answer on Day 1, and the real answer replaces it when S7 is in SIT.
- The synthetic case, write-off, account key and cut-off month are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the contract fakes in place from the first run; the one wait is RWB-S7-E6021-APP, which replaces its fake and never blocks the lane (Template and Rules §R5.4, §R5.7).
- Harness environment, base hosts, the shape of the ALS and GL posting answer, its rejection codes, the retry settings, the evidence format and the pass or fail gate: Not specified in the source documents (GAP-0456; ASM-0648)

### 4. Flow

1. Harness: runs preflight. It reads the six contracts, pins each version in the run report, loads the ALS and GL answer fixture and the synthetic population, and stops the run before any assertion if a contract is missing or a pinned version has moved.
2. Harness: opens the run for cut-off month 2027-04 on the synthetic case `RW-2027-000721` and its write-off `WO-SYN-000721`, with the approved population of the month read from the fixture as a count and an amount.
3. Harness: takes the approval that starts the posting — `POST /api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` as a RW-CREDITAD session holding Write-off and posting A, on the decision the committee has already recorded (R-WO-20 opens the window, R-WO-21 posts).
4. Harness: reads `GET /api/recovery/integration/v1/admin/outbound-items` and asserts exactly one outbound item for the write-off, on the ACE integration path, with its file run and its interface configuration.
5. Harness: lets the ALS and the general ledger answer the item. On a reference the write-off moves `POSTING_PENDING` to `POSTED` and the posting reference is recorded once (R-WO-21); on a rejection it moves to `POSTING_REJECTED` and holds (R-WO-22).
6. Harness: calls `POST /api/recovery/integration/v1/admin/outbound-items/{itemId}/resend` twice for the same item with one Idempotency-Key per call, then reads the outbound items again and asserts one item, one file run and one posting — the resend is a delivery retry and never a second write-off.
7. Harness: reads the posting back from ACE through `GET /api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` and asserts the write-off, its account key, its amount, `posted_date`, `responsibility_center`, `cost_center` and `gl_product` on `v_ace_write_off` (DF-ACE-261 to DF-ACE-269), with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP13` for the business date and the load time.
8. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}` for the write-off stage on the case and `GET /api/recovery/decision/v1/decision-log?caseId={caseId}` for the posting entry, its rule version and its hash, and asserts that the posting entry exists once and names the same posting reference.
9. Harness: watches the topic `rwb.writeoff.events.v1` and asserts that `rwb.writeoff.WriteOffApproved.v1` is published once for the write-off, that rwb-case consumes it once and rwb-payment consumes it once, each recorded in its own inbox table, and that a redelivery adds no second effect.
10. Harness: reconciles the approved population with the posted population for the cut-off month (R-WO-42, R-WO-43): the approved count and amount equal the posted count and amount, `POPULATION_RECONCILED` holds and the retention timer starts; when they differ the case is on `WRITEOFF_EXCEPTION` with the difference named and no case is reported as posted.
11. Harness: repeats the posting step with the central ledger held back, and then with the local decision record and the ledger both unavailable, and asserts that the point of no return does not pass and that nothing is posted (AC5).
12. Harness: calls the committee decision as a synthetic RW-OFF caller with no Write-off and posting A, and asserts 403 with MSG-P4-002 and no decision entry for the write-off (AC6).
13. Harness: writes one run report per cut-off month, keyed by story and month, naming the contract version of each hop, whether the hop was a contract fake or the owner, the outbound item, the event and inbox counts, the two populations and the six criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A contract fake answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-E6-021-01-ITG (ITG AC1) |
| X2 | The ALS or the general ledger answers a rejection | The write-off holds on `POSTING_REJECTED`, the rejection is raised against the item, and no posting reference is recorded | None | TC-E6-021-03-ITG (ITG AC2) |
| X3 | A resend is called twice for the same outbound item | The run fails on AC3 if a second outbound item, a second file run or a second posting exists; a delivery retry is not reported as a new posting | None | TC-E6-021-03-ITG (ITG AC2) |
| X4 | The same `WriteOffApproved` is delivered twice to a consumer | The run fails on AC3 unless the consumer's inbox ignores the second delivery and the effect stays one per consumer | None | TC-E6-021-01-ITG (ITG AC3) |
| X5 | The approved count or amount differs from the posted count or amount | The case moves to `WRITEOFF_EXCEPTION` with the difference named (R-WO-43), and the run fails if any case of the month is reported as posted | None | TC-E6-021-01-ITG (ITG AC4) |
| X6 | The central ledger has not confirmed the decision record, or the local record cannot be written | The posting step does not reach `POSTED`, no posting reference is recorded, and on the forced failure the answer carries MSG-P7-003 with nothing posted | MSG-P7-003 | TC-E6-021-04-ITG, TC-E6-021-06-ITG (ITG AC5) |
| X7 | A caller without Write-off and posting A takes the committee decision | The answer is 403 with MSG-P4-002, and the decision log holds no entry for the write-off | MSG-P4-002 | TC-E6-021-05-ITG (ITG AC6) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and their fakes from Day 1; the only wait is RWB-S7-E6021-APP, and its fake answers until it lands |
| Negotiable | The fixture layout, the answer fixture, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | Proves across services that the approved population was posted once, reached its consumers once, and is tied to the ledger before the point of no return is called |
| Estimable | One runner, one fake set, one answer fixture, one outbound-item assertion, one event probe and one report |
| Small | Fits in one sprint with its six tests |
| Testable | Each criterion is asserted on an observable: an outbound item, a file run, a returned reference, a case stage, an event, an inbox row, two populations and a response code |

### 7. Acceptance criteria

```gherkin
Feature: Post an approved write-off - wave 4 posting harness

  Background:
    Given the environment is SIT with synthetic data
    Given the case "RW-2027-000721" carries the write-off "WO-SYN-000721" for cut-off month "2027-04"
    Given the ALS and the general ledger answer fixture returns a posting reference for the write-off
    Given the committee decision for the write-off is recorded with the rule version in force

  Scenario: AC1 Post an approved write-off (legacy RWB-E6-021 AC1)
    Given the data and the rule version this feature needs are in place
    When its trigger arrives
    Then posts the write-off to ALS and the general ledger and releases the provision
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Rule R-WO-23 (legacy RWB-E6-021 AC3)
    Given a case in state POSTING_REJECTED
    When rejection cleared
    Then re-post to ALS and the general ledger
    Then the case moves to POSTING_PENDING

  Scenario: AC3 The posting reference returns and the event reaches its consumers once (new, D-RCV-60)
    Given the write-off "WO-SYN-000721" is in POSTING_PENDING with one outbound item on rwb-integration
    When the ALS and the general ledger return the posting reference for the write-off
    Then the case carries the write-off stage POSTED and posted_date is set to the date in the answer
    And the posting reference is recorded once against the write-off
    And rwb-integration holds exactly one outbound item for the write-off with its file run
    When POST "/api/recovery/integration/v1/admin/outbound-items/{itemId}/resend" is called twice for the same item
    Then no second outbound item and no second posting exist
    And rwb.writeoff.WriteOffApproved.v1 is published once on rwb.writeoff.events.v1
    And rwb-case consumes it once and rwb-payment consumes it once, each through its inbox
    And the ACE batch shows the posting back through DP13 with its freshness stamp

  Scenario: AC4 The approved population equals the posted population (new, D-RCV-60)
    Given the committee approved the population of cut-off month "2027-04"
    When the posting of the population is complete
    Then the approved count and amount of the month equal the posted count and amount
    And POPULATION_RECONCILED holds and the retention timer starts
    When one write-off of the month is not posted and the two populations differ
    Then the case moves to WRITEOFF_EXCEPTION with the difference named
    And no case is reported as posted on a partial answer
    And the correction path re-posts on the same outbound item or refers the pack back to the committee

  Scenario: AC5 The posting waits for the ledger and a failed decision record stops it (new, D-RCV-60)
    Given the central ledger has not confirmed the decision record of the posting step
    When the point of no return is reached
    Then the posting step does not reach POSTED and no posting reference is recorded
    When the local decision record and the ledger are both unavailable
    Then nothing is posted and the answer carries "MSG-P7-003"

  Scenario: AC6 A caller without the right is refused (new, D-RCV-60)
    Given a synthetic caller with role "RW-OFF" and no Write-off and posting A
    When the caller calls POST "/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision"
    Then the answer is 403 with "MSG-P4-002"
    And no decision is recorded for the write-off
```

Legacy AC2 (R-WO-05, the pack) and AC4 (the decision log cannot be written) belong to RWB-S7-E6021-APP, and the six criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | ALS and the general ledger return a reference, the posting reference is recorded and the write-off moves `POSTING_PENDING` to `POSTED`; without a reference it does not move | R-WO-21; DF-FIN-016 |
| BR2 | A rejection holds the posting on `POSTING_REJECTED` and raises it; once the cause is cleared and the retry limit is not reached, the write-off re-posts and returns to `POSTING_PENDING` | R-WO-23; R-WO-22 |
| BR3 | The approved population and the posted population are compared every month: equal counts and amounts publish completeness and start the retention timer, and a difference raises the exception with the difference named | R-WO-42; R-WO-43 |
| BR4 | The exception is corrected by one of three routes — re-post, return to scan, or refer the pack back to the committee — and a re-post never writes a second posting | R-WO-44; R-WO-46; Temporal design slide 23 |
| BR5 | Posting is the point of no return, and the posting step waits for the central ledger to confirm the decision record in strict mode; a posting without its decision record does not pass | Temporal design slide 23; ADR-022 |
| BR6 | The write-off posts once and leaves once: one outbound item per write-off on the ACE integration path, and a delivery resend is a retry, not a second posting | Arch v5 slides 16 and 41; ADR-015 |
| BR7 | `WriteOffApproved` is published once per approved write-off and has its effect once per consumer, through the consumer's inbox | Arch v5 slide 43, event 24; ADR-015 |
| BR8 | An interface failure after the retry limit moves the item to the exception queue with a task for a named owner | NFR-026 |
| BR9 | Every decision behind the posting is reproducible from the log, including the rule version | NFR-033; DF-DEC-004, DF-DEC-005 |
| BR10 | The posting facts — `posted_date`, `responsibility_center`, `cost_center` and `gl_product` — are read back from the general ledger through the ACE view, and the Workbench never asserts a posting the ledger does not hold | DF-FIN-016 to DF-FIN-019; DF-ACE-264 to DF-ACE-267; DP-05 |
| BR11 | ACE data is read only through rwb-source-data's data-product contract, never from a view or another service's schema | DP-05; DP-01; ADR-020 |
| BR12 | Every call is one hop on the owner's base with a 2 s budget, and no service calls another service on the caller's behalf | DP-13; ADR-020 |

The harness asserts these rules and changes none of them.

### 9. State transitions

| From | Event | Condition | To | Owner |
|---|---|---|---|---|
| `APPROVED` | `POSTING_TASK_CREATED` | the posting window is open and no unmatched payment is in flight | `POSTING_PENDING` | S7 rwb-writeoff (R-WO-20) |
| `POSTING_PENDING` | `ALS_POSTING_CONFIRMED` | ALS and the general ledger return a reference | `POSTED` | S7 rwb-writeoff (R-WO-21) |
| `POSTING_PENDING` | `ALS_POSTING_REJECTED` | result = rejected | `POSTING_REJECTED` | S7 rwb-writeoff (R-WO-22) |
| `POSTING_REJECTED` | `REJECTION_CLEARED` | retry count below the limit and the cause is cleared | `POSTING_PENDING` | S7 rwb-writeoff (R-WO-23) |
| `POSTED` | `POPULATION_RECONCILED` | approved count and amount equal posted count and amount | `RETENTION_RUNNING` | S7 rwb-writeoff (R-WO-42) |
| `POSTED` | `POPULATION_NOT_RECONCILED` | the approved and posted populations differ | `WRITEOFF_EXCEPTION` | S7 rwb-writeoff (R-WO-43) |
| `WRITEOFF_EXCEPTION` | `CORRECTION_REPOST` | the owner decides to re-post | `POSTING_PENDING` | S7 rwb-writeoff (R-WO-44) |
| `WRITEOFF_EXCEPTION` | `CORRECTION_REFER_TO_COMMITTEE` | the owner refers the case back | `WITH_COMMITTEE` | S7 rwb-writeoff (R-WO-46) |

The harness changes no state. Every change in the table is made by S7 rwb-writeoff inside `WriteOffWorkflow`, and the harness reads the result through the case contract, the DP13 records and the decision log. A state the harness had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts. `CORRECTION_RETURN_TO_SCAN` (R-WO-45) is S7's own path and is not exercised here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CREDITAD Credit Administration officer | Takes the committee decision that starts the posting (Write-off and posting A); reads the posting result and the populations |
| RW-WOCOMM Write-off committee member | Holds Write-off and posting A; the decision the harness posts was taken by the committee, not by this story |
| RW-FINANCE Finance | Holds Write-off and posting A; reads the posting and the provision release |
| RW-WRITEOFF Write-off team member | Holds Write-off and posting C; runs the scan (JOB-16) and reads the populations; not the caller of the posting |
| RW-OFF Case officer | The synthetic caller of AC6; holds no Write-off and posting A and is refused |
| RW-TRIBE, RW-PLATADM | Read the run report and the evidence; the platform administrator holds the environment |
| QA lead | Owns the harness configuration, the fixtures, the answer fixture, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the fake set and the swap from a fake to the real service |
| The owning services' identities | S7 posts and releases, P2 holds the outbound item and its file run, P1 serves DP13, P7 holds the ledger, P3 holds the case, P4 answers the right; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access and the committee decision is recorded by the caller |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-FIN-010 to DF-FIN-020 | `write_off` (rwb_writeoff) | id, case_id, decision_log_id, amount, tax_criteria_met, committee_date, posted_date, responsibility_center, cost_center, gl_product, recovered_after | Read as the posting result through the case, DP13 and the decision log; written by S7 |
| DF-FIN-015 | `write_off` | committee_date | Read (the approval the posting derives from) |
| DF-FIN-016 | `write_off` | posted_date | Read (set from the ledger's answer; also on `v_ace_write_off`) |
| DF-FIN-017 | `write_off` | responsibility_center | Read (compared with the ledger's answer) |
| DF-FIN-018 | `write_off` | cost_center | Read (compared with the ledger's answer) |
| DF-FIN-019 | `write_off` | gl_product | Read (compared with the ledger's answer) |
| DF-FIN-020 | `write_off` | recovered_after | Read (zero at posting; changed only after charge-off) |
| DF-ACE-261 to DF-ACE-269 | `v_ace_write_off` | write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system, data_as_of | Read through the P1 DP13 contract only |
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | case_no, status, stage_code, owner_user_id, rule_version and 18 more | Read through the rwb-case contract |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` | id, case_id, decision_code, rule_id, rule_version, final_call, actions, outcome, decided_at, entry_hash and 8 more | Read through the rwb-decision decision-log contract |
| DF-REF-001 to DF-REF-015 | `rule_row` | rule_id, rule_version, route_set, from_state, event_code, to_state and 9 more | Asserted from the decision entry (DF-DEC-004, DF-DEC-005); the rule catalogue is P7's and is not read directly here |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The write-off table is S7's, the case is P3's, the ledger is P7's and the rule catalogue is P7's; the ACE side of the posting is `v_ace_write_off`, reachable only as DP13 Money and closure through rwb-source-data (DP-05, INT-16 GL). The harness owns no table and writes no row; the write-off record's own fields are asserted where the contracted reads carry them, and the rest is proven in RWB-S7-E6021-APP against its own reads.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/writeoff/v1/write-offs/{writeOffId}/committee-decision` | S7 rwb-writeoff | The approval that starts the posting (AC1, AC5, AC6) |
| GET | `/api/recovery/integration/v1/admin/outbound-items` | P2 rwb-integration | The one outbound item for the write-off and its file run (AC1, AC3) |
| POST | `/api/recovery/integration/v1/admin/outbound-items/{itemId}/resend` | P2 rwb-integration | The delivery retry that must not write a second posting (AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP13/records?caseId={caseId}` | P1 rwb-source-data | The posting read back from `v_ace_write_off` (AC1, AC3, AC4) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP13` | P1 rwb-source-data | The business date and the load time of DP13 (AC3) |
| GET | `/api/recovery/decision/v1/decision-log?caseId={caseId}` | P7 rwb-decision | The posting entry, its rule version and its hash (AC1, AC5, AC6) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The write-off stage on the case and its timers (AC3, AC4) |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | The caller's role and rights for the committee decision (AC6) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-13, ADR-020). No operation is invented in this story: each path is the owner's published operation, and the Ownership Map publishes no read of a write-off record, so the harness identifies the posting through the case, DP13 and the decision log. Where a screen would compose them, the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event. `WriteOffApproved` is produced by rwb-writeoff's outbox and is asserted in 12.4; the harness writes its report to the wave record.

#### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.writeoff.WriteOffApproved.v1` | `rwb.writeoff.events.v1` | Produced by S7 rwb-writeoff; consumed by P3 rwb-case, P8 rwb-payment and P9 rwb-reporting | CloudEvents 1.0 binary mode, key caseId, exactly one event per approved write-off; inbox dedupe in each consumer's `processed_event`; retry then `.dlt` |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by every service, rwb-writeoff included; consumed by P7 rwb-decision and P9 rwb-reporting | Exactly one event per local append; the entry's hash and rule version are what the posting step waits for under BR5 |

The two events are asserted on the topic, not read from a table: the harness counts them per write-off and per consumer, and a redelivery is a pass only when the inbox absorbs it.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `WriteOffWorkflow` | Workflow | `rwb-writeoff` | The posting step (step 4, R-WO-21, EV-24), the provision release and feed step (step 5, R-WO-25/26) and the population reconciliation (R-WO-42/43) |

`WriteOffWorkflow` and its steps are S7's, registered by its worker in RWB-S7-E6021-APP; this story observes their effect and starts none of them by hand. The provision release and the Finance feed belong to RWB-E6-022 and are observed only as far as the posting's own state depends on them.

#### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| JOB-16 write-off scan in rwb-writeoff | Monthly, 3rd working day, overlap policy SKIP with a catch-up window | Registered by the rwb-writeoff release; read by the harness and never changed or triggered by it in this story | JOB-16 Write-off scan |

JOB-16 is a Temporal Schedule in rwb-writeoff (Arch v5 slide 44; Temporal design slide 23), not a shared Quartz row; the scan itself is RWB-E6-013's and this story neither runs it nor asserts its population.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). The write-off is S7's, the outbound item and its file run are P2's, DP13 is P1's, the ledger is P7's and the case is P3's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Fake for rwb-writeoff | The committee decision of §12.2 | Records the decision for write-off `WO-SYN-000721` once per Idempotency-Key, returns the write-off identifier, and refuses a caller without Write-off and posting A with 403 and MSG-P4-002 |
| Fake for rwb-integration | `GET /admin/outbound-items`, `POST /admin/outbound-items/{itemId}/resend` | One outbound item for the write-off with one file run and its interface configuration; the resend answers accepted and writes no second item |
| Fake for rwb-source-data | DP13 records and the DP13 freshness read | The write-off's posting back from `v_ace_write_off`: write_off_key, account_key, amount, posted_date, responsibility_center, cost_center, gl_product, source_system and data_as_of, with the business date and the load time |
| Fake for rwb-decision | `GET /decision-log?caseId={caseId}` | The posting entry with its rule ID, rule version, final call, actions and entry hash; an empty log for a write-off whose decision was refused |
| Fake for rwb-case | `GET /cases/{caseId}` | Case `RW-2027-000721` with its write-off stage and its timers, `POPULATION_RECONCILED` and `WRITEOFF_EXCEPTION` included |
| Fake for rwb-access | `GET /me/session` | A RW-CREDITAD session holding Write-off and posting A, and a RW-OFF session holding neither |
| ALS and GL answer fixture | The answer of the core system and the general ledger to a posting item | A posting reference with its posting date and the GL keys, a rejection with its reason, a late answer, and no answer at all |

Each fake is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The shape of the ALS and GL posting answer, its reference format, its rejection codes and the retry settings are Not specified in the source documents (GAP-0456; ASM-0648)

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-13, ADR-020) |
| Kafka | None published; 2 event types consumed — `rwb.writeoff.WriteOffApproved.v1` on `rwb.writeoff.events.v1` and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` — with inbox dedupe at rwb-case, rwb-payment and rwb-decision |
| Temporal | None added; `WriteOffWorkflow` on `rwb-writeoff` and the JOB-16 write-off scan Schedule are observed |
| File | The outbound file run of the posting item on the ACE integration path (INT-16 GL), and the ALS and GL answer fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery-w4/write-off-posting`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON from DP-03 and RWB-PLT-N001-CON from DP-19) are platform stories delivered by the platform wave and are not repeated in the metadata H field of this story, which stays empty. The one blocking dependency is the I story RWB-S7-E6021-APP, which replaces its fake; until it is live the run uses the fake, and a fake pass is reported as a fake pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the six owned criteria in order for a cut-off month and holds the run lock |
| FakeSet | Fake | The six contract fakes and the ALS and GL answer fixture of §12.8, each generated from the published contract with its version pinned |
| PostingDriver | Service | Takes the committee decision as a RW-CREDITAD holder and reads the one outbound item and its file run |
| ReferenceProbe | Service | Applies the ALS and GL answer, asserts the recorded posting reference and the case stage, and calls the resend twice |
| PostingReadBack | Service | Reads DP13 records and freshness and compares the posting's write-off, account key, amount, posted_date and GL keys with the answer |
| PopulationCheck | Service | Compares the approved count and amount of the month with the posted count and amount, and names each difference |
| LedgerGate | Service | Holds the central ledger confirmation back, and forces the local decision-record failure, and asserts what the point of no return does |
| EventProbe | Service | Consumes `rwb.writeoff.events.v1` and the consumers' inboxes and asserts one event and one effect per consumer |
| AccessProbe | Service | Calls the committee decision as RW-OFF and asserts 403 with MSG-P4-002 and no decision entry |
| EvidenceReport | Service | Writes one report per cut-off month keyed by story, and holds the pass or fail gate |

**Environment and synthetic data.** SIT, against the contract fakes from Day 1 and the real services as RWB-S7-E6021-APP lands, on the synthetic case `RW-2027-000721`, the write-off `WO-SYN-000721`, its synthetic account key, cut-off month 2027-04 and the population of the month read from the fixture as a count and an amount. In SIT the answer comes from the ALS and the general ledger through the ACE integration path and is read back through DP13. The harness environment, the base hosts, the answer shape, the retry settings, the evidence format and the gate are Not specified in the source documents (GAP-0456; ASM-0648)

**Build steps**

1. Generate the six contract fakes and load the ALS and GL answer fixture; pin every contract version in the run report and fail the run on a mismatch (X1).
2. Build the PostingDriver for AC1: take the committee decision as RW-CREDITAD, read the outbound items, and assert one item for the write-off with its file run and its interface configuration.
3. Add the ReferenceProbe for AC1 and AC3: apply the answer, assert the recorded posting reference, the `POSTED` stage and `posted_date` from the answer, then call the resend twice and assert no second item, no second file run and no second posting (X3).
4. Add the PostingReadBack for AC3: read DP13 records and freshness, and compare the write-off, its account key, its amount, `posted_date`, `responsibility_center`, `cost_center` and `gl_product` with the answer and the decision entry (AC1).
5. Add the EventProbe for AC3: assert one `WriteOffApproved` on `rwb.writeoff.events.v1`, one effect in rwb-case and one in rwb-payment, and that a redelivery adds none (X4).
6. Add PopulationCheck for AC4: equal counts and amounts give `POPULATION_RECONCILED` and the retention timer; a difference gives `WRITEOFF_EXCEPTION` with the difference named, no case reported as posted, and the correction path re-posting on the same item (X5).
7. Add the LedgerGate for AC5 (the ledger held back, then the forced decision-record failure with MSG-P7-003), the re-post path of AC2 from `POSTING_REJECTED` (X2), and the access path of AC6, then the EvidenceReport and the gate, swapping a fake for the real owner as RWB-S7-E6021-APP lands (X6, X7).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The six tests of section 16 pass against the fakes and again against the real services when RWB-S7-E6021-APP lands, the approved population of the cut-off month equals the posted population read back through DP13, exactly one `WriteOffApproved` exists per approved write-off with one inbox effect per consumer, and the wave entry check holds a run report keyed by story and cut-off month.

### 14. Validation and messages

| ID | Type | Message | Where the run asserts it |
|---|---|---|---|
| MSG-S7-001 | Error | The scan is on hold until Finance publishes the tax criteria. | The scan is on hold, so the posting does not start for the month and the harness fails the run before any posting assertion |
| MSG-GEN-001 | Error | Enter {field}. | The committee decision called without the decision field answers with the field named in place of {field} |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. | The RW-OFF caller on the committee decision, with the action named in place of {action} |
| MSG-P7-003 | Error | The action was not taken because the decision could not be recorded. Try again in a few minutes. | The forced decision-record failure of AC5, with nothing posted |

The four texts are copied unchanged from RWB-E6-021; the story adds no message text. The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

This story builds no screen. The states are read through rwb-case and the write-off record: the write-off stage as the case read returns it, and the posting facts as they come back from the general ledger through DP13. The Ownership Map publishes no read of a write-off record, so where a state lives only on that record it is asserted in RWB-S7-E6021-APP against its own reads, and the harness identifies the posting through the case, DP13 and the decision log.

| State | What the harness asserts |
|---|---|
| `POSTING_PENDING` | The item exists on the ACE integration path with its file run, and no posting reference is recorded yet |
| `POSTED` | The reference is recorded once, `posted_date` is the date in the answer, and DP13 shows the posting |
| `POSTING_REJECTED` | The rejection is raised against the item, no reference is recorded, and the re-post returns the write-off to `POSTING_PENDING` |
| `WRITEOFF_EXCEPTION` | The difference between the approved and posted populations is named, and no case of the month is reported as posted |
| `POPULATION_RECONCILED` | The approved count and amount equal the posted count and amount, and the retention timer starts |

SCR-27 Write-off proposal is RWB-S7-E6021-APP's screen and is out of scope here; what the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0456; ASM-0648)

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-021-01-ITG | AC1 (legacy); ITG AC1, ITG AC3 | End to end | One approved write-off for a cut-off month, the posting step live |
| TC-E6-021-02-ITG | AC2 (legacy); ITG AC2 | Integration | A case in POSTING_REJECTED with the cause cleared |
| TC-E6-021-03-ITG | AC3 (legacy); ITG AC2 | Integration | An ALS rejection and one re-post on the same outbound item |
| TC-E6-021-04-ITG | ITG AC5 (legacy AC4 is RWB-S7-E6021-APP's) | Integration | The ledger held back, then a forced decision-record failure |
| TC-E6-021-05-ITG | Access; ITG AC6 | Component | RW-OFF caller without Write-off and posting A |
| TC-E6-021-06-ITG | Principle 5; ITG AC5 | Integration | A forced decision-record failure stops the posting with MSG-P7-003 |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic case, write-off, account key and cut-off month, the populations, the answer fixture, the retry settings and the report layout are data.
- No personal data in logs, fixtures, events or the report: every key is synthetic, and `WriteOffApproved` and `DecisionRecorded` carry IDs, references and codes, never a customer fact.
- ACE data only through the P1 contract: the posting is read back as DP13 Money and closure, never from `v_ace_write_off` directly and never from another service's schema (DP-01, DP-05).
- One hop and a 2 s budget per call, with a breaker per downstream, so the harness fails where a screen would (DP-13, ADR-020).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a fake or the owner.
- The harness never runs against UAT or production, never triggers the JOB-16 scan in a live environment, and never writes a row by hand.
- A failing criterion is fixed in the service that owns it or raised as a gap; it is never waived in the script.
- No business decision is taken here: the committee decision is recorded by the caller, the posting is S7's, and the harness only asserts what the services answer.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-E6-021 Post an approved write-off | Recovery Workbench User Stories Epics 3 to 8 v3, lines 10192 to 10288 | Sections 1, 3, 11, 14 and 19 of this file |
| Legacy AC1 and AC3, verbatim | The same, lines 10211 to 10215 and 10223 to 10227 | Section 7, AC1 and AC2, marked (legacy RWB-E6-021 AC1) and (legacy RWB-E6-021 AC3) |
| Legacy AC2 and AC4, and the six legacy test cases TC-E6-021-01 to TC-E6-021-06 | The same, lines 10217 to 10232 and 10275 to 10284 | AC2 and AC4 stay with RWB-S7-E6021-APP (section 19); the six cases are copied as -ITG in section 16 |
| R-WO-21, R-WO-23, R-WO-42, R-WO-43, R-WO-44, R-WO-46 | Business Rules and Routing Logic v4, lines 352, 354, 373, 374, 375 and 377 | Section 8, BR1 to BR4; section 9 |
| JOB-16 Write-off scan, monthly on the 3rd working day | Arch v5 slides 20 and 44; Temporal design slide 23 | Section 12.6 |
| Event 24 `WriteOffApproved` on `rwb.writeoff.events.v1`, consumed by rwb-case, rwb-payment and rwb-reporting | Arch v5 slide 43 | Section 12.4; AC3 |
| Point of no return, posting waits for the central ledger in strict mode | Temporal design slide 23 | Section 8, BR5; AC5 |
| REQ-S7-005, approved write-offs post, the provision is released and completeness is published | Business Requirements Program v4, line 396 | Sections 2 and 8 |
| INT-16 GL, write-off postings into ACE read through `v_ace_write_off` | Epics 3 to 8 Specification v3, Integrations sheet, line 233 | Sections 11, 12.8 and 12.9 |
| NFR-026, three retries then the exception queue with a task | Business Requirements Program v4, line 496 | Section 8, BR8 |
| NFR-033, every decision reproducible from the log | Business Requirements Program v4, line 520 | Section 8, BR9 |
| DF-FIN-010 to DF-FIN-020, DF-ACE-261 to DF-ACE-269, DF-CAS-001 to DF-CAS-023, DF-DEC-001 to DF-DEC-018, DF-REF-001 to DF-REF-015 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP-03, DP-05, DP-13 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application; metadata |
| ADR-015, ADR-020 and ADR-022 | Architecture Decision Records, ADR-015 (Kafka with outbox and inbox), ADR-020 (one hop and 2 s) and ADR-022 (local record plus central ledger) | Sections 8, 12 and 13 |
| RWB-S7-E6021-APP and RWB-S7-E6021-CON | The split plan of this wave | Section 19; the build of the posting and the two legacy criteria stay there |

### 19. Out of scope

- RWB-S7-E6021-CON and RWB-S7-E6021-APP: the write-off contract, the posting, the provision release, the population reconciliation, and legacy AC2 (R-WO-05, the pack) and AC4 (the decision log cannot be written).
- The committee decision itself and its approval levels: RWB-E6-018 to RWB-E6-020.
- The committee pack: RWB-E6-015.
- The monthly scan and the tax criteria: RWB-E6-013 and RWB-E6-014.
- The provision inputs and the tax file to Finance: RWB-E6-022.
- The approved-versus-posted reconciliation as a product: RWB-E6-023.
- The write-off exception loop: RWB-E6-024.
- SCR-27 Write-off proposal.
- The ALS and the general ledger adapters as products, and the ACE ingestion that loads `gl_write_off`.
- Platform deployment, the topic and queue provisioning, the Schedule registration and the environment itself.
