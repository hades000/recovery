# RWB-ITG-E5002-ITG Record proof of delivery on a notice

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E5002-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W3 |
| Wave | 3 |
| Business epic | EP05 |
| Release | 31 March 2027 (tentative) |
| Legacy key | RWB-E5-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-ITG-W3 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-S4-E5002-APP, RWB-P6-E5002-APP, RWB-P3-E5002-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E5-002 for the wave 3 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a member of the integration and QA team, I want **one repeatable cross-service harness that takes a seeded case in route state NOTICE_DISPATCHED with a notice the post has returned, records the proof of delivery through the notice's own contract, and proves the whole served-notice chain — the proof on the notice in rwb-comms, the delivery fact handed to rwb-litigation on the published contract, the case route move and the notice-period start in rwb-case, with the decision record written before either changes — against the owning services' published contracts and their fakes**, so that **no notice period is ever shown to start from anything other than the day the customer received the notice, a notice nobody could serve is shown as unserved instead of a clock that never runs, and the officer stops chasing the post room for a date that three services can prove between them**.

### 2. Business rationale

A statutory notice only starts its clock when it was served, and a period counted from the print date can be challenged in court. That single sentence is the whole reason legacy RWB-E5-002 exists, and it is also why the step cannot stay in one service. The legacy story wrote the delivery confirmation onto the case and started the notice-period timer from it (R-LIT-07), marked the notice unserved and did not start the period when the proof window expired (R-LIT-08), and refused the whole action when the decision log could not be written (R-UNI-39; REQ-DRI-005). One legacy step, three target owners: the delivery fact is a fact of the notice and belongs to rwb-comms, which owns the notice, the template, the merge fields and the proof of delivery (Architecture v5 slide 41 and slide 17; `notice`, `template`, `merge_field` in `ownership.json`); the evaluation of the delivery rules and the legal action belong to rwb-litigation, which owns legal actions, hearings, judgments and enforcement in `rwb_litigation`; and the case of record, its route state, its timer and its task belong to rwb-case, which owns case, CMMN state, queues, tasks, allocation and timers in `rwb_case`. No source describes the delivered chain as one operation, and no source names the contract that carries the delivery fact from the notice to the litigation evaluation (GAP-0437; ASM-0624).

That split is what this story is for. A chain across three owners can be correct service by service and still be wrong end to end: a notice Delivered with a case that never moved, a case in the notice period with a timer that started on the sent date, an unserved notice whose case kept a running clock, or a proof recorded twice that moved the case twice. Each of those failures is invisible to the unit tests of the three slices and is exactly what the wave entry check has to see. So the harness drives the real path — the proof write on the notice that `RWB-P6-E5002-APP` builds, the hand-off on the S4 contract `RWB-S4-E5002-CON` that `RWB-S4-E5002-APP` publishes, the case move and the durable timer that `RWB-P3-E5002-APP` applies — and asserts the holders' own answers at every hop. It computes no date, no duration, no state and no rule outcome itself.

This story owns no legacy criterion. The four criteria AC1 to AC4 of RWB-E5-002 are owned by `RWB-S4-E5002-APP`, which keeps the case transitions and the legacy lines word for word; the notice half is `RWB-P6-E5002-APP` and the case half is `RWB-P3-E5002-APP`. By way of reference only, AC2 of the legacy key reads: given a case in state NOTICE_DISPATCHED, when proof of delivery is received, then attach the proof and start the notice period from the delivered date, and the case moves to WITH_CUSTOMER_NOTICE_PERIOD; that criterion is the S4 slice's and is not restated here as a scenario. The criteria of this story are new under D-RCV-60 and test only the cross-service deliverable in the title: the chain, the unserved branch, the record written before the change, the single hop and single hand-off, the refusal, and the screen read.

The harness is decoupled the same way the services are. It owns no schema and reads no other service's table (DP-01): the notice and its serving facts come from rwb-comms, the legal action and the litigation answer from rwb-litigation, the case route state and the notice-period timer from rwb-case, the record from rwb-decision and the authority from rwb-access. It reads no ACE view and no ACE table (DP-05): the proof this run records is the one the officer supplies through the notice's own operation, and the automatic `v_ace_pod` read that fills the notice from the WIN file is the dispatch loop of the Epic 2 stories and not this run's input. The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). It calls each owner's base `/api/recovery/<short>/v1`, one hop per call with a 2 s timeout and a circuit breaker per downstream, never the old monolith base (DP-13), and it calls the gateway-bff composite route where a screen would (DP-19).

It serves REQ-OCC-003 ("letters are dispatched for print and post, and proof of delivery returns to the case"), REQ-S4-001 ("demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed"), REQ-CWC-010 and REQ-CWC-016 on the case move and its rule version, and REQ-DRI-001 and REQ-DRI-005 on the record that must exist before the effect. It carries the control CTL-15 into evidence — a notice period starts only from the delivery date on the proof of delivery, never from the print date — and it holds the FSD P6 measure "notices with proof of delivery, 100 percent" on the notice side of the chain.

### 3. Preconditions

- The published contracts of rwb-comms, rwb-litigation, rwb-case, rwb-decision and rwb-access are in the contract registry, and a stub set is generated from each published OpenAPI or AsyncAPI document with its version pinned.
- `RWB-S4-E5002-CON` is published: the proof-record operation on `/api/recovery/litigation/v1`, its request and answer (the notice reference, the case reference, the delivery status, the delivered or callback date, the rule ID and the package version of the S4 evaluation), its error envelope and its fake. The operation's own name is Not specified in the source documents (GAP-0437; ASM-0624); the harness never calls it, and it reads its effect on the case and the record instead.
- The notice proof write that rwb-comms serves on `POST /api/recovery/comms/v1/notices/{noticeId}/proof-of-delivery` is published by `RWB-P6-E5002-APP`. The path is that story's design and is named by no source (GAP-0437; ASM-0624).
- A case in route state `NOTICE_DISPATCHED` and a notice in state Sent for it, with its `sent_date` (DF-LEG-019) and `barcode` (DF-LEG-020), are seeded through the owning services' published operations only. The dispatch that puts the notice in Sent is `RWB-P6-E2021-APP` and is proven by `RWB-ITG-E2021-ITG`; this harness starts after it. The seeding set, the harness environment and the fixture contents are Not specified in the source documents (GAP-0437; ASM-0627).
- The litigation rule package in force on the business date carries R-LIT-07, R-LIT-08, R-LIT-09 and their timer specifications, and the version of each rule is readable on the record that cites it. The package code is not named by any source read (GAP-0437; ASM-0628).
- The notice-period duration is in force as a versioned reference row of rwb-case, and the proof window is the one R-LIT-08 carries. Neither the row code nor its value is named by any source read (GAP-0437; ASM-0626).
- The LOV-DELIVERY values and the mapping of a value onto the notice state are in force at their version, and the harness reads the notice state the owner returns rather than applying a mapping of its own (GAP-0437; ASM-0625).
- An authorisation path exists through `POST /api/recovery/access/v1/authorise` for the roles that hold the Litigation right of the notice, and for a role that holds none.
- No build dependency and no contract dependency. Day 1, with the fakes of section 12.8 in place from the first run, and each fake replaced by the real service as its I story lands: `RWB-P6-E5002-APP`, `RWB-S4-E5002-APP` and `RWB-P3-E5002-APP`.

### 4. Flow

1. Harness: seeds a case in route state `NOTICE_DISPATCHED` and a notice of that case in state Sent with its `sent_date` and `barcode`, through the owning services' published operations only; the seeding set and its environment are Not specified in the source documents (GAP-0437; ASM-0627).
2. Harness: reads the notice through `GET /api/recovery/comms/v1/notices/{noticeId}` and pins what the run is keyed by: the notice reference, the case reference, the notice state Sent, the `sent_date`, the `barcode` and an empty `delivery_status` and `callback_date` (DP-13).
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts route state `NOTICE_DISPATCHED`, and reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts that no notice-period timer is running yet, so the "before" of the chain is on record.
4. Harness: records the returned proof with `POST /api/recovery/comms/v1/notices/{noticeId}/proof-of-delivery`, carrying the delivery status `DELIVERED` and the callback date, so the fact is recorded by the service that owns the notice and not by the harness. The path is the P6 slice's design and is named by no source (GAP-0437; ASM-0624).
5. Harness: reads the notice again and asserts the owner's answer: state Delivered, delivery status `DELIVERED`, the callback date it sent, and the `barcode` and `sent_date` unchanged. The mapping that turns the delivery status into the notice state is the owner's reference data, not an assertion the harness makes up (ASM-0625).
6. Harness: asserts the hand-off happened, without calling it: rwb-comms sends one call to the proof-record operation of `RWB-S4-E5002-CON` per recorded proof, and the harness sees its consequence in rwb-litigation's answer and in rwb-case's state, which is the only place a consequence is provable from outside. The operation name is Not specified in the source documents (GAP-0437; ASM-0624).
7. Harness: reads the litigation side through `GET /api/recovery/litigation/v1/legal-actions/{legalActionId}` and asserts the legal action of the notice and the pack state the notice belongs to, so a case move that no litigation answer supports fails the run.
8. Harness: reads the case again and asserts the route move the target fixes: `NOTICE_DISPATCHED` to `WITH_CUSTOMER_NOTICE_PERIOD` by R-LIT-07, with the rule ID and the package version in force on the case row (`rule_version`, DF-CAS-021).
9. Harness: reads `GET /api/recovery/case/v1/cases/{caseId}/timers` and asserts one notice-period timer, `timer_type` of the notice period (DF-WRK-030) with `started_at` (DF-WRK-031) equal to the delivered date it sent and `expires_at` (DF-WRK-032) equal to the end the owner publishes from the reference row in force, which the harness reads and never computes (CTL-15; ASM-0626).
10. Harness: reads `GET /api/recovery/decision/v1/decision-log` and asserts exactly one record for the delivery move, naming R-LIT-07 and the package version in force with the delivered date it was based on, and asserts that the record exists for the move rather than being written after it (REQ-DRI-001; R-UNI-39).
11. Harness: repeats the run on the unserved branch, with a delivery status of `UNDELIVERABLE` or with the proof window expired and no proof at all, and asserts the notice Unserved, the case `NOTICE_UNSERVED` by R-LIT-08 or R-LIT-09, and no notice-period timer (R-LIT-08; R-LIT-09).
12. Harness: repeats the served run with the decision record forced to fail and asserts that nothing moves: the notice keeps state Sent with no `delivery_status` and no `callback_date`, the case stays `NOTICE_DISPATCHED`, no timer row appears, and the caller sees MSG-P7-003. This is the negative path of a criterion owned by `RWB-S4-E5002-APP` and by `RWB-P6-E5002-APP`, and it is exercised here as the chain's own guard (REQ-DRI-005; R-UNI-39).
13. Harness: records the same proof twice, with the same delivery status and callback date and with the same Idempotency-Key, and asserts one notice write, one hand-off, one case move, one timer and one record, with the repeat counted under R-UNI-40.
14. Harness: authorises each call through `POST /api/recovery/access/v1/authorise` and records the refusal path for a role that does not include the Litigation right of the notice, with MSG-P4-002 and nothing changed.
15. Harness: reads the screen path through the gateway-bff composite route and asserts that SCR-18 Notice approval and SCR-19 Litigation workspace show the notice facts of this chain, the case state and the notice-period end, merged from the three owners, with no owner service called directly by the browser (DP-19).
16. Harness: publishes one evidence report per story and business date, naming the criterion, the assertions, the contract versions, the reference-data versions and whether each hop was a stub or the owner. The evidence format and its retention are Not specified in the source documents (GAP-0437; ASM-0627).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fake answers a shape the published contract does not allow | The run fails at that hop; the report names the service, the operation and the contract version | None | AC7 |
| X2 | The notice read back after the proof write is not in the state the owner's mapping gives for the delivery status | The run fails on AC1 and the report names the status, the state returned and the mapping version it read | None | AC1 |
| X3 | The notice is Delivered but the case stays in `NOTICE_DISPATCHED`, or the case moves with no notice Delivered behind it | The run fails on AC1 and the report names the notice, the case and both states | None | AC1 |
| X4 | A notice-period timer is running with `started_at` other than the delivered date, or it starts before the notice is Delivered | The run fails on the CTL-15 assertion and the report names the sent date, the delivered date and `started_at` | None | AC1 |
| X5 | The unserved branch leaves a notice-period timer running, or the case in any state other than `NOTICE_UNSERVED` | The run fails on AC2 and the report names the case state, the timer rows it found and the answer that produced them | None | AC2 |
| X6 | No record exists for the delivery move, or its rule ID or package version is missing | The run fails on AC3 and the report names the records it found and the versions they cite | None | AC3 |
| X7 | The decision record is forced to fail but the notice, the case, the timer or the litigation answer still moves | The run fails on AC3 and the report names what moved | MSG-P7-003 | AC3 |
| X8 | More than one hand-off leaves rwb-comms for one recorded proof, or one hand-off produces two case moves | The run fails on AC4 and the report names the calls and the moves it counted | None | AC4 |
| X9 | The same proof recorded twice writes a second notice change, a second hand-off, a second timer or a second record | The run fails on AC4 and the report names what the repeat produced | None | AC4 |
| X10 | A role without the Litigation right records the proof or reads the case, and the call is served | The run fails on the access check and the report names the operation and the role | MSG-P4-002 | AC5 |
| X11 | The composite route answers a screen from one owner only, or the browser path reaches an owner service directly | The run fails on AC6 and the report names the route, the owners it merged and the ones it did not | None | AC6 |
| X12 | A real service is reachable but its contract version differs from the registry, or a reference row is at a different version than the run pinned | The run fails before any assertion and the report names the service and both versions | None | AC7 |

The report text is for the wave entry check and is not part of the message standard. R-LIT-07, R-LIT-08, R-LIT-09, R-UNI-39, R-UNI-40 and CTL-15 carry no message ID in the rule set, so the harness asserts the notice state, the case state, the timer, the record and the notices on the topics, and names a message ID only where an owning service returns one of those in section 14.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; the only waits are the three I stories, `RWB-P6-E5002-APP`, `RWB-S4-E5002-APP` and `RWB-P3-E5002-APP`, and each is replaced as it lands |
| Negotiable | The seeding set, the fixtures, the reference-data versions and the report shape are configuration agreed at the wave entry check, not business values in code |
| Valuable | The served-notice chain, the unserved branch and the record-before-effect rule are proven across three owners before wave 3 opens |
| Estimable | One harness runner, one stub set, three probes, one event probe, one report |
| Small | Fits one sprint with its tests |
| Testable | Each criterion runs against the fakes and again against the real owners, and a stub pass is reported as a stub pass |

### 7. Acceptance criteria

```gherkin
Feature: Record proof of delivery on a notice, across rwb-comms, rwb-litigation and rwb-case

  Background:
    Given case "RC-2026-000321" is in route state "NOTICE_DISPATCHED"
    Given notice "N-0101" of that case is in state "Sent" with barcode "RR223344556TH" and sent date 2026-12-15
    Given the LOV-DELIVERY values and the mapping of a delivery status to the notice state are in force at their version
    Given the litigation rule package in force carries R-LIT-07, R-LIT-08 and R-LIT-09
    Given every consumed contract is the published contract of its owner, with its version pinned, and is answered by its fake

  Scenario: AC1 A recorded proof serves the notice and starts the notice period on the delivered date (new, D-RCV-60)
    Given the rwb-comms contract mock accepts the proof for notice "N-0101" and the rwb-litigation contract mock accepts the delivery answer with rule "R-LIT-07"
    Given the rwb-case contract mock answers route state "NOTICE_DISPATCHED" before the run and no notice-period timer
    When "LIT-0101" records the proof of delivery for notice "N-0101" with delivery status "DELIVERED" and callback date 2026-12-18
    Then notice "N-0101" reads state "Delivered" with delivery status "DELIVERED" and callback date 2026-12-18
    Then the case reads route state "WITH_CUSTOMER_NOTICE_PERIOD" with rule "R-LIT-07" and the package version in force
    Then one notice-period timer reads started_at 2026-12-18 and expires_at is the end the owner publishes from the reference row in force
    Then one decision record names R-LIT-07, the package version in force and the delivered date

  Scenario: AC2 A notice that could not be served leaves no notice period running (new, D-RCV-60)
    Given the rwb-litigation contract mock answers the delivery answer with rule "R-LIT-08" where the proof window expired, and "R-LIT-09" where the result is undeliverable
    When "LIT-0101" records the proof for notice "N-0101" with delivery status "UNDELIVERABLE" and callback date 2026-12-21
    Then notice "N-0101" reads state "Unserved" with delivery status "UNDELIVERABLE"
    Then the case reads route state "NOTICE_UNSERVED" with its rule and the package version in force
    Then no notice-period timer is created and none is started
    When the proof window expires with no proof recorded for a second notice of the same case
    Then the notice reads "Unserved", the case reads "NOTICE_UNSERVED" by R-LIT-08, and still no notice-period timer is created

  Scenario: AC3 The record is written before the chain moves, and nothing moves when it fails (new, D-RCV-60)
    Given the local decision-record library answers and the reference rows are in force at their version
    When the proof for notice "N-0101" is recorded with delivery status "DELIVERED" and callback date 2026-12-18
    Then exactly one decision record names the delivery outcome, R-LIT-07, the package version and the notice and case references
    Given the local decision-record library is unavailable
    When the same proof is recorded
    Then notice "N-0101" keeps state "Sent" with no delivery status and no callback date
    Then the case keeps route state "NOTICE_DISPATCHED" and no notice-period timer exists
    Then the caller reads MSG-P7-003 and no second record is written

  Scenario: AC4 One hop and one hand-off per proof, and a repeated proof changes nothing (new, D-RCV-60)
    Given notice "N-0101" is "Delivered" with callback date 2026-12-18 and the case is "WITH_CUSTOMER_NOTICE_PERIOD"
    When the same proof is recorded again with the same delivery status and the same callback date
    Then the notice is unchanged and no second hand-off leaves rwb-comms
    Then the case keeps its route state, its single timer and its single record
    Then the repeat is counted under R-UNI-40
    When a second proof is recorded for the same notice with a different callback date
    Then the run records the answer the owner gives and asserts that the notice carries one state, the case one route move, one timer and one record, whichever answer that is
    Then the report names that answer, so a conflicting proof is closed by the notice owner and not by the harness

  Scenario: AC5 A role without the Litigation right is refused and the chain does not move (new, D-RCV-60)
    Given "U-5002" holds RW-PHONECOL, which carries no Litigation right
    Given the rwb-access contract mock returns no Litigation right for that role
    When "U-5002" records the proof for notice "N-0101"
    Then the call is refused with status 403 and MSG-P4-002
    Then notice "N-0101" keeps state "Sent", the case keeps "NOTICE_DISPATCHED" and no record is written
    When "U-5002" reads the case of the same notice
    Then the read is refused with status 403 and MSG-P4-002

  Scenario: AC6 The chain shows on the two screens through one composite route (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-18 Notice approval and SCR-19 Litigation workspace for case "RC-2026-000321"
    Given notice "N-0101" is "Delivered" and the case is "WITH_CUSTOMER_NOTICE_PERIOD" with its notice-period end
    When "LIT-0101" opens SCR-18 and SCR-19
    Then SCR-18 shows the notice state "delivered", the delivery status "DELIVERED", the callback date 2026-12-18 and the barcode "RR223344556TH"
    Then SCR-19 shows the same notice facts, the case state and the notice-period end from GET /cases/{caseId}/timers
    Then the browser calls one composite route and no owner service directly

  Scenario: AC7 The harness holds no value of its own and a drifted contract fails the run (new, D-RCV-60)
    Given a second seeded case whose notice-period reference row is at another version and whose delivered date is another day
    When the served run is repeated with no change to the harness
    Then the notice state, the case state, the timer end and the record follow the owners and the versions they publish
    Given a real service answers at a contract version other than the one pinned at the start of the run
    When the run starts
    Then it fails before its first assertion and the report names the service, the pinned version and the version it found
    Then no assertion is reported as passed
```

The seven criteria are new under D-RCV-60 and test only the cross-service deliverable of this story. AC1 to AC4 of RWB-E5-002 are owned by `RWB-S4-E5002-APP` and are quoted nowhere here as a scenario; the notice half is `RWB-P6-E5002-APP`'s and the case half is `RWB-P3-E5002-APP`'s. The three documents of this key use the same labels for different criteria, so a criterion is always quoted with its story ID (GAP-0437; ASM-0623).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A recorded proof of delivery with a served result of delivered starts the notice period from the delivered date and moves the case to the notice period, and the proof is attached to the notice it serves | R-LIT-07; legacy RWB-E5-002 AC2 |
| BR2 | A proof window that expires with no proof marks the notice unserved and starts no notice period; a result of refused, returned or undeliverable takes the same end | R-LIT-08, R-LIT-09; legacy RWB-E5-002 AC3 |
| BR3 | The notice, its template, its merge fields and its proof of delivery are rwb-comms's; the legal action and the delivery-rule evaluation are rwb-litigation's; the case state, the timer, the task and the case record are rwb-case's | Architecture v5 slide 41 and slide 17; `ownership.json` (notice, template and merge_field own P6; legal_action and hearing own S4; recovery_case, timer and task own P3) |
| BR4 | No notice period starts except from the delivery date on the proof of delivery, and never from the print or sent date | CTL-15; R-LIT-07 |
| BR5 | The decision is recorded before the effect, with the rule ID and the version in force; no action proceeds if its record cannot be written | R-UNI-39; REQ-DRI-001; REQ-DRI-005; legacy RWB-E5-002 AC4 |
| BR6 | The same proof, event or request twice produces one effect and the repeat is counted | R-UNI-40; legacy TC-E5-002-01 |
| BR7 | The case moves between states and queues by the transfer rules on the rule outcome, and every move is logged with the rule ID and the rule version that caused it | REQ-CWC-010; REQ-CWC-016 |
| BR8 | The harness asserts the owners' answers and computes no date, duration, state or rule outcome of its own; every value it compares comes from an owner's contract or a versioned reference row | DP-01; DP-05; Template and Rules v1 section R7.2 (s17) |

R-LIT-07 and R-LIT-08 are the two rows of the litigation rule table that carry this behaviour; R-LIT-09 is the same end by a failed delivery. The notice-period duration and the proof window are data, not constants: the harness reads them and never writes them.

### 9. State transitions

Three owners move three different things in this chain, and the table names each one with its owner. The notice moves on its own lifecycle in rwb-comms; the case route state moves on the litigation evaluation and is applied by rwb-case; the timer is the case's.

| From | Event | Condition | To | Owner |
|---|---|---|---|---|
| Sent | A proof is recorded with delivery status `DELIVERED` | The notice carries a `sent_date` and a callback date | Delivered, with `callback_date` (DF-LEG-021) and `delivery_status` (DF-LEG-022) written once | P6 rwb-comms |
| Sent | A proof is recorded with `REFUSED` or `UNDELIVERABLE`, or the proof window expires with no proof | The notice carries a `sent_date` | Unserved, with the delivery status the proof carries | P6 rwb-comms |
| NOTICE_DISPATCHED | PROOF_OF_DELIVERY_RECEIVED | R-LIT-07, served result delivered, on the delivered date | WITH_CUSTOMER_NOTICE_PERIOD | S4 rwb-litigation evaluates, P3 rwb-case applies |
| NOTICE_DISPATCHED | PROOF_WINDOW_EXPIRED | R-LIT-08, no proof returned inside the proof window | NOTICE_UNSERVED | S4 rwb-litigation evaluates, P3 rwb-case applies |
| NOTICE_DISPATCHED | DELIVERY_FAILED | R-LIT-09, served result refused, returned or undeliverable | NOTICE_UNSERVED | S4 rwb-litigation evaluates, P3 rwb-case applies |
| WITH_CUSTOMER_NOTICE_PERIOD | NOTICE_PERIOD_EXPIRED | R-LIT-15, no cure and no dispute at the period end; the timer story of this legacy family, not this one | PACK_ASSEMBLY | P3 rwb-case |
| any other case state | A delivery answer arrives | The case is not in `NOTICE_DISPATCHED` | unchanged, and the arrival is recorded as an exception | S4 rwb-litigation, P3 rwb-case |

The notice-period timer is created on the delivered branch only: `timer_type` of the notice period (DF-WRK-030) with `started_at` (DF-WRK-031) equal to the delivered date and `expires_at` (DF-WRK-032) equal to that date plus the duration of the reference row in force, held as a durable timer inside CaseWorkflow with the timer row as the projection the screens read.

The harness moves none of these. It seeds through the owning services' published operations, drives the proof through the notice's own write, and then asserts the state each owner reached, naming the owner and the operation behind each move in the report. A state the harness set by hand would prove nothing, and a field it computed would hide exactly the defect the chain exists to catch (GAP-0437; ASM-0623).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation C and Litigation A on the legacy permission block of RWB-E5-002: records the proof, reads the notice, the case and the record in scope |
| RW-ENFORCE, enforcement owner | Litigation C: records the proof and reads the same facts in scope |
| RW-LEGAL, RW-PRODHEAD, RW-HEADLIT | Litigation A: read only |
| RW-CASEOWN, RW-TEAMMGR | Read the case state, the notice facts and the timer through their own rights |
| RW-PHONECOL, phone collector | Holds no Litigation right: refused on the proof write and on the case read with MSG-P4-002 |
| QA lead | Owns the harness configuration, the seeding set, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a fake to the real service |
| The owning services' identities | rwb-comms, rwb-litigation, rwb-case, rwb-decision and rwb-access make every change the harness asserts; the harness makes none |
| No delegation-of-authority level applies to the harness | The harness takes no business decision; the delivery outcome is the litigation evaluation's and the case move is the case service's |

The rights are the rows of the legacy permission block and nothing wider. A refusal keeps MSG-P4-002 and changes nothing.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 to DF-LEG-023 | notice (P6, `rwb_comms`) | id, case_id, document_id, notice_type, sent_date (DF-LEG-019), barcode (DF-LEG-020), callback_date (DF-LEG-021), delivery_status (DF-LEG-022), sent_type | Read after the proof write, through the rwb-comms contract; written by the owner, never by the harness |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | id, case_no, product_group, primary_person_key, status, stage_code and the rest, with route_state (DF-CAS-007) and rule_version (DF-CAS-021) | Read, through the rwb-case contract |
| DF-WRK-027 to DF-WRK-036 | timer (P3, `rwb_case`) | id, case_id, task_id, timer_type (DF-WRK-030), started_at (DF-WRK-031), expires_at (DF-WRK-032), warn_at, paused, status (DF-WRK-035), escalation_level | Read, through `GET /cases/{caseId}/timers` |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7, `rwb_decision`) | id, case_id, decision_code, rule_id (DF-DEC-004), rule_version, model_version and the rest | Read, through the rwb-decision contract |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | id, rule_id, rule_version, route_set, from_state, event_code and the rest | Read, by rule ID and package version through the rwb-decision registry |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer (P1 rwb-source-data) | person_key, cif_no, first_name, last_name, date_of_birth, customer_status and the rest | Not read: the harness reads no ACE view and no ACE table, and the customer attributes a rule needs travel inside the S4 answer (DP-05) |
| DF-PRT-001 to DF-PRT-007 | partner (S9, `rwb_partner`) | id, partner_code, partner_name, partner_type, panel_status, contract_end | Not read: the law firm instruction of the litigation stage is `RWB-S4-E5002-APP`'s and no partner fact is asserted by this chain |

Field IDs are those of the Logical Data Model and Data Dictionary v8 and of the legacy key. Two of the facts the chain asserts have no field ID in any source read: the notice lifecycle state that the SCR-18 list calls delivered and unserved, which is a standard column of the TSD P6 design and not one of the nine `notice` fields, and the notice reference, delivered date and outcome that rwb-case adds to the case row in `RWB-P3-E5002-APP`. Both are carried as Not specified in the source documents (GAP-0437; ASM-0623).

The harness owns no table and writes no row directly: every read and every seed goes through the API of the owning service (DP-01, DP-05), and it holds no copy of a notice, a case, a timer or a record. It stores nothing between runs except its evidence report.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/comms/v1/notices/{noticeId}` | P6 rwb-comms | The notice and its serving facts before and after the proof write: state, `notice_type`, `sent_date`, `barcode`, `callback_date` and `delivery_status` (AC1, AC2) |
| POST | `/api/recovery/comms/v1/notices/{noticeId}/proof-of-delivery` | P6 rwb-comms | Records the returned proof and drives the chain; the path is `RWB-P6-E5002-APP`'s design and is named by no source (AC1, AC2, AC4) |
| GET | `/api/recovery/litigation/v1/legal-actions/{legalActionId}` | S4 rwb-litigation | The legal action of the notice and the pack state, so a case move without a litigation answer fails the run (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case route state, `rule_version` and the case identity the notice belongs to (AC1, AC2, AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timers` | P3 rwb-case | The notice-period timer and its `started_at` and `expires_at` (AC1, AC2) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | The record of the delivery move with its rule ID and package version (AC3) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Litigation right and the scope, including the refusal path (AC5) |
| GET | the gateway-bff composite route of SCR-18 and SCR-19 | PLT gateway-bff, RWB-PLT-N001-CON | The merged screen answer of the three owners, read once (AC6) |

Every owner operation is one hop on its base `/api/recovery/<short>/v1`, with a 2 s timeout and a circuit breaker per downstream, and never on the old monolith base (DP-13). The harness does not call the proof-record operation of `RWB-S4-E5002-CON`: that call is rwb-comms's, its own name is Not specified in the source documents (GAP-0437; ASM-0624), and the harness asserts its effect on the case and the record instead of repeating it. Architecture v5 slide 17 also names `GET /cases/{id}/notices` for rwb-comms; the published map does not carry it, so this run reads the one notice it seeded. No operation is invented beyond the one the P6 slice designs and the composite route the platform owns.

#### 12.3 Events published

None. The harness publishes no Kafka event; it drives the proof through the notice's contract and consumes the owners' events.

#### 12.4 Events consumed

| Event | Topic | Producer | Use |
|---|---|---|---|
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | P6 rwb-comms | Carries the delivery fact for the notice where the run consumes it, keyed by caseId with IDs and facts only and no personal data (AC1) |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | The case move with fromState, toState, the event code and the rule ID, read as the case's own announcement of the move the run asserts (AC1, AC2) |
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | every service, through its own local decision-record library | The record written with the change reaches the ledger, so a move with no record is a failed run (AC3, DP-03) |

All three carry IDs and business facts only, keyed by caseId, and the harness asserts that no personal data is present on any of them.

#### 12.5 Workflows and activities

None added. The harness exercises the durable notice-period timer inside CaseWorkflow on task queue `rwb-case`, and the step `RWB-P3-E5002-APP` adds behind it, and it exercises LitigationWorkflow on task queue `rwb-litigation` as the stage that produces the delivery answer; both are the owners' and neither is created, changed or owned here. The harness triggers them through the published operations only and asserts their effects through the services' contracts and topics.

#### 12.6 Schedules

None added. Nothing in this chain runs on a schedule: the proof arrives when the returned post is recorded, and the notice-period clock is a durable timer inside the case workflow and not a Schedule or a polling job. The 16:00 file window that dispatches the letter is JOB-10 and belongs to `RWB-P6-E2021-APP`, not here.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01): `notice` is rwb-comms's, `legal_action` and `hearing` are rwb-litigation's, `recovery_case`, `timer` and `task` are rwb-case's, `decision_log_entry` and `rule_row` are rwb-decision's, the roles and scope data are rwb-access's, and the notice-period duration is a reference row of rwb-case.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| Stub for rwb-comms | `GET /notices/{noticeId}`, `POST /notices/{noticeId}/proof-of-delivery`, `rwb.comms.events.v1` | Day-1 run of AC1, AC2 and AC4 before `RWB-P6-E5002-APP` is live |
| Stub for rwb-litigation | `GET /legal-actions/{legalActionId}`, and the proof-record answer of `RWB-S4-E5002-CON` as rwb-comms sees it | Day-1 assertion of the litigation side of the chain and of the refusal where the case is not in the expected state |
| Stub for rwb-case | `GET /cases/{caseId}`, `GET /cases/{caseId}/timers`, `rwb.case.events.v1` | Day-1 assertion of the route move, the rule version and the notice-period timer |
| Stub for rwb-decision | `GET /decision-log` | Day-1 assertion of one record for the move with its rule ID and package version |
| Stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path |
| gateway-bff composite route fake | The DP-19 route of SCR-18 and SCR-19 | Day-1 assertion of the merged screen answer (AC6) |
| Event stubs | `rwb.comms.NoticeDelivered.v1`, `rwb.case.CaseStateChanged.v1`, `rwb.decision-record.DecisionRecorded.v1` | The facts the run asserts where the environment does not run the owners' producers |

Each fake is generated from the published OpenAPI or AsyncAPI document of its owner, and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The two operation names no source gives, the reference rows behind the notice-period duration and the delivery-status mapping, the seeding set, the environment and the evidence format are Not specified in the source documents (GAP-0437; ASM-0624, ASM-0625, ASM-0626, ASM-0627).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 owner operations and one composite route consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s timeout and a circuit breaker per downstream, and the screen read through gateway-bff (DP-13, DP-19) |
| Kafka | None published; `rwb.comms.NoticeDelivered.v1`, `rwb.case.CaseStateChanged.v1` and `rwb.decision-record.DecisionRecorded.v1` consumed (DP-03) |
| Temporal | Exercised only: the durable notice-period timer and the step inside CaseWorkflow on queue `rwb-case`, and LitigationWorkflow on queue `rwb-litigation`; none added |
| File | None |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1027-CON and RWB-PLT-N001-CON) are delivered by the platform wave and are not repeated in the metadata H row of this story, which stays None. The three I stories are the only blocking dependencies: `RWB-P6-E5002-APP` for the notice and its proof write, `RWB-S4-E5002-APP` for the delivery evaluation and the contract behind it, and `RWB-P3-E5002-APP` for the case move and the timer. Until each is live the run uses that owner's stub, and a stub pass is reported as a stub pass.

The decoupling is also the story's reading of the legacy step, and it is the split the plan fixes. The legacy key wrote the delivery confirmation onto the case and started the timer in process; in the target the notice fact is P6's, the rule evaluation and the case move are S4's, and the timer and its task are P3's, so the harness proves the chain across the three and computes nothing itself (GAP-0437; ASM-0623). It owns no schema (DP-01) and reads the notice, the case, the timer, the record and the authority from their owners only. It reads no ACE view: the proof is the officer's fact recorded through the notice's own operation, and the automatic `v_ace_pod` loop is the Epic 2 dispatch stories (DP-05). The record is read from rwb-decision's contract and the shared `rwb.decision-record.v1` topic rather than from a local log table (DP-03). It calls the owners on their own bases and never the monolith base (DP-13), and the composed reads a screen would make are exercised through the gateway-bff composite route (DP-19).

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeProofChainRunner | Job | Runs the served branch, the unserved branch and the negative path in order for a business date and holds the run lock |
| StubSet | Fake | The five owner stubs, the composite-route fake and the three event stubs of section 12.8, each generated from the published contract with the version pinned |
| NoticeProbe | Service | Records the proof and reads the notice back, asserting the state, the delivery status and the callback date against the mapping and the values the owner publishes |
| CaseAndTimerProbe | Service | Reads the case route state, the rule version and the notice-period timer, and asserts `started_at` against the delivered date and `expires_at` against the end the owner publishes (CTL-15) |
| LitigationProbe | Service | Reads the legal action and the pack state of the notice, so a case move without a litigation answer fails the run |
| DecisionRecordProbe | Service | Reads one record for the move through the rwb-decision contract and asserts its rule ID, package version and delivered date, and the failed-write path |
| EventProbe | Service | Consumes `rwb.comms.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1` and asserts the facts for the case, their keys and the absence of personal data |
| EvidenceReport | Service | Writes the report keyed by story and business date and holds the pass or fail gate |

**Environment and test data.** SIT, against the fakes from Day 1 and the real services as they land, with one case in `NOTICE_DISPATCHED` carrying a notice in Sent with its barcode and sent date, one notice whose proof comes back undeliverable, and one notice whose proof window expires with no proof. The environment, the seeding set, the reference-data versions behind it and the evidence retention are Not specified in the source documents (GAP-0437; ASM-0627). Seeding uses only the owning services' published operations, never a schema write.

**Build steps**

1. Generate the five owner stubs, the composite-route fake and the three event stubs from the published contracts, pin each version in the report and fail the run on a version mismatch (X1, X12).
2. Build the NoticeProbe around the notice read and the proof write, and assert the state the owner returns from the delivery status it was given (X2).
3. Build the CaseAndTimerProbe for the route move, the rule version and the notice-period timer, and assert the notice and the case agree (X3).
4. Add the CTL-15 assertion: `started_at` equals the delivered date, and `expires_at` equals the end the owner publishes from the reference row in force, with no date computed in the harness (X4).
5. Build the unserved branch: an undeliverable proof and an expired proof window, with no timer created and the case in `NOTICE_UNSERVED` (X5).
6. Build the DecisionRecordProbe: one record for the move, naming R-LIT-07 and the package version in force, read before the assertions that depend on it (X6).
7. Add the negative path: force the decision record to fail, assert that the notice, the case, the timer and the litigation answer do not move, and record MSG-P7-003 (X7).
8. Add the hand-off counter: one hand-off per recorded proof and one case move per hand-off, asserted from the litigation answer and the case state (X8).
9. Add the repeat: the same proof twice and the same Idempotency-Key twice, with one write, one hand-off, one move, one timer and one record, and the repeat counted under R-UNI-40 (X9).
10. Add the access path through `POST /api/recovery/access/v1/authorise`, including the refusal for a role that does not include the right (X10).
11. Add the composite-route read of SCR-18 and SCR-19 through the edge fake, and fail a screen answer that merges fewer than the three owners or reads an owner directly (X11).
12. Add the EvidenceReport and the gate, then swap each stub for the real service as its I story lands and rerun the criteria.

**Feature switch.** The legacy key names no feature switch for this behaviour. The harness runs behind the platform feature-flag library as the wave releases it, and the P6 slice's own flag on the proof write is respected by the run; the flag keys are Not specified in the source documents (GAP-0437; ASM-0627).

**Done when.** The tests of section 16 pass; the criteria pass against the fakes on Day 1 and again against each owner as its I story lands; no run reports a notice period that started from anything other than the delivered date; and the wave entry check holds a report keyed by story and business date with the contract, reference-data and fixture versions named.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record for the delivery move cannot be written (X7, AC3) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role does not include the Litigation right of the notice, or the case is outside their scope (X10, AC5) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required value is missing from the proof request, carried from the legacy message set (AC1) | Enter {field}. |
| MSG-S4-001 | Carried from the legacy message set of this key: the pack is missing an item. The pack belongs to `RWB-S4-E5002-APP` and no path of this story raises it | The pack is missing {item}. Add it before filing. |
| MSG-S4-002 | Carried from the legacy message set of this key: the claim on the case is close to expiry. It is S4's fact and S4's text, and no path of this story raises it | The claim on this case expires on {date}. File before then. |

The five texts are the legacy wording of RWB-E5-002 section 14, copied unchanged; no message is reworded and no new message is added. R-LIT-07, R-LIT-08, R-LIT-09, R-UNI-39, R-UNI-40 and CTL-15 carry no message ID in the rule set, so the harness asserts the notice state, the case state, the timer, the record and the events, and names a message ID only where an owner returns one of the five above. The harness produces none of these messages itself.

### 15. Screens and states

No screen is built in this story. Two existing surfaces show the chain, read through the gateway-bff composite route (DP-19):

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-18 Notice approval | Sent | The notice with its sent date and barcode, and the proof form of `RWB-P6-E5002-APP` |
| SCR-18 Notice approval | Delivered | The notice state "delivered", the delivery status `DELIVERED` and the callback date, read only |
| SCR-18 Notice approval | Unserved | The notice state "unserved" with the delivery status of the proof, and the case state beside it |
| SCR-18 Notice approval | Not recorded | The decision record could not be written, MSG-P7-003, and nothing changed |
| SCR-18 Notice approval | Refused | A role without the Litigation right reads MSG-P4-002 and nothing changes |
| SCR-19 Litigation workspace | Pack and notice period | The same notice facts, the case state and the notice-period end, next to the pack state rwb-litigation serves |
| SCR-19 Litigation workspace | Unserved | The case state `NOTICE_UNSERVED` with the reason the litigation answer gave, and no notice-period end |

The harness renders no screen. It reads these states through the composite route, so a passed run means the two screens have the right data behind them, merged from the three owners in one route. The route path, the screen-model field list and the merge order belong to `RWB-PLT-N001-CON` and the edge stories, not here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E5-002-01-ITG | AC1, AC4, BR1, BR4, BR6, AC1 (owned by RWB-S4-E5002-APP) | Integration | Case "RC-2026-000321" in "NOTICE_DISPATCHED"; notice "N-0101" Sent with barcode "RR223344556TH" and sent date 2026-12-15; a proof with "DELIVERED" and callback date 2026-12-18; the same proof recorded twice |
| TC-E5-002-02-ITG | AC1, AC3, BR1, BR4, BR5, AC2 (owned by RWB-S4-E5002-APP) | Integration | A notice in "NOTICE_DISPATCHED" and proof of delivery received for it with delivered_at 2026-12-18; the notice-period duration read as a versioned reference row; R-LIT-07 in force |
| TC-E5-002-03-ITG | AC2, BR2, R-LIT-08, R-LIT-09, AC3 (owned by RWB-S4-E5002-APP) | Integration | The proof window expired with no proof returned; a proof with "UNDELIVERABLE"; the notice left "Unserved", the case in "NOTICE_UNSERVED", and no notice-period timer |
| TC-E5-002-04-ITG | AC3, BR5, AC4 (owned by RWB-S4-E5002-APP) | Integration | The decision record forced to fail; nothing moves; MSG-P7-003 |
| TC-E5-002-05-ITG | AC5, BR8 | Component | A role without the right, refused with MSG-P4-002 |
| TC-E5-002-06-ITG | AC3, AC7, BR5 | NFR | A forced decision log write failure stops the action with MSG-P7-003, and a drifted contract fails the run before its first assertion |

These are the ITG copies of TC-E5-002-01 to TC-E5-002-06, kept in the order of the legacy list and carrying the legacy data unchanged, with the access copy at Component level and the forced-failure and drift copy at NFR level as the legacy levels map. The full legacy tests, with their Given, When and Then, are in `Recovery Workbench Test Cases v7.xlsx`, tab Story test cases, under those IDs.

### 17. Guardrails

- No business value in code: the notice-period duration, the proof window, the delivery-status to notice-state mapping, the rule rows and the package version are data with a version, and the harness holds no copy of any of them.
- No personal data in logs, fixtures, reports, tests or prompts: the chain carries case and notice references, dates, a barcode, list values and rule IDs, never a name, an address or an account number, and the harness asserts the absence of personal data on the three events.
- No read of another service's tables: every read and every seed goes through the owning contract (DP-01), and no ACE view and no ACE table is read by the harness (DP-05).
- The harness computes nothing of its own: the notice state, the case state, the timer end and the record are the owners' answers, and a value the harness derived would be reported as a harness defect, not as a service pass.
- One hop and a 2 s timeout per call, with a circuit breaker per downstream and no call chain, so the harness fails where a screen would (DP-13, DP-19).
- A stub pass is never reported as a real-service pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, never sets a notice state, a case state, a timer or a record by hand, and writes nothing but its evidence report.
- A failing assertion is fixed in the service that owns it or reported as a gap and an assumption; it is never waived in the script.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-003 | Letters are dispatched for print and post, and proof of delivery returns to the case; this chain carries the return onto the notice and to the case's owner | Business Requirements Program v4, section 5.6 | FEAT-LIT-02 | 13 Manage documents and correspondence | R-LIT-07, R-LIT-08, CTL-15 | TC-E5-002-01-ITG, TC-E5-002-02-ITG, TC-E5-002-03-ITG |
| REQ-S4-001 | Demand and recall notices are generated by rule, approved, dispatched, and their notice periods are timed | Business Requirements Program v4, section 5.11 | FEAT-LIT-02, FEAT-LIT-03 | D7 litigation; notice period | R-LIT-07, R-LIT-08, R-LIT-09 | TC-E5-002-01-ITG, TC-E5-002-02-ITG, TC-E5-002-03-ITG |
| REQ-CWC-010 | Cases move between queues and roles by transfer rules on stage change, route decision, timer expiry and the other named triggers | Business Requirements Program v4, section 5.3 | FEAT-LIT-02 | D7 litigation | R-LIT-07, R-LIT-08 | TC-E5-002-01-ITG, TC-E5-002-03-ITG |
| REQ-CWC-016 | Every allocation, assignment, transfer and timer event is logged with the rule ID and the rule version that caused it | Business Requirements Program v4, section 5.3 | FEAT-LIT-02 | D7 litigation | R-UNI-39 | TC-E5-002-01-ITG, TC-E5-002-02-ITG |
| REQ-DRI-001 | Every decision writes one record holding case and decision, the rule, model, agent and prompt versions, an inputs snapshot, the recommendation, the approval, the actions taken and the outcome | Business Requirements Program v4, section 5.7 | FEAT-LIT-02 | D7 litigation | R-LIT-07, R-UNI-39 | TC-E5-002-01-ITG, TC-E5-002-02-ITG |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program v4, section 5.7 | FEAT-LIT-02 | D7 litigation | R-UNI-39 | TC-E5-002-04-ITG, TC-E5-002-06-ITG |

The legacy story master of the Epics 3 to 8 set carries no requirement ID for RWB-E5-002: it gives the feature FEAT-LIT-02, the module, the data, the endpoints, the screens, the rights, the messages and the test cases, and no REQ identifier. The trace above therefore runs to the Program BRD requirements that this chain serves, with FEAT-LIT-02 and the rules R-LIT-07, R-LIT-08 and R-LIT-09 as the whole legacy trace, until the EP05 PRD adds the requirement ID (GAP-0437; ASM-0629).

### 19. Out of scope

- The notice, its template, the merge fields, the proof of delivery on the notice row and the notice lifecycle state: rwb-comms (P6), `RWB-P6-E5002-APP`.
- The delivery-rule evaluation, the legal action, the pack, the proof-window expiry and the queue transfer of an unserved notice: rwb-litigation (S4), `RWB-S4-E5002-APP`; the proof-record operation and its shape: `RWB-S4-E5002-CON`.
- The case route move, the notice-period timer and its task, the case-side decision record and the case columns behind them: rwb-case (P3), `RWB-P3-E5002-APP`.
- The automatic WIN proof-of-delivery loop that reads `v_ace_pod`, the INT-15 file, the notice Sent state and `NoticeDelivered`: `RWB-P6-E2021-APP`, `RWB-P1-E2021-APP` and `RWB-ITG-E2021-ITG`; this run starts from a notice already Sent.
- The four legacy criteria AC1 to AC4 of RWB-E5-002 as the S4 slice words them: `RWB-S4-E5002-APP`.
- The notice generation, the notice request, the approval path and the template catalog: the further P6 and S4 stories of this legacy family.
- The contract baselines of rwb-comms, rwb-litigation, rwb-case, rwb-decision and rwb-access, which are their CON stories and are consumed here through the published documents and their fakes.
- The platform configuration: the decision-record library, the gateway-bff composite route, the feature-flag library and the observability set, which the platform wave delivers.
- The roles, the scope and the masking data themselves, and the full screen model of SCR-18 and SCR-19.
- Any production screen, event, workflow, Schedule or table: this story builds a test harness and its evidence only.
- The fixture contents, the harness environment, the reference-row codes, the evidence format and its retention, and the feature-flag keys: carried as a gap and assumptions, not decided here.
