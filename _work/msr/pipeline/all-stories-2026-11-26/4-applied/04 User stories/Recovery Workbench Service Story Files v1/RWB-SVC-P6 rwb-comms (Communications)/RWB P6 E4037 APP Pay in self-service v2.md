# RWB-P6-E4037-APP Pay in self-service

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4037-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-U |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4037-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-037 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E4037-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **customer (borrower)**, I want **to pay against the plan or the settlement from the same self-service screen, with the intent taken against the notice that screen showed me, the contact stop and the channel consent checked before it is taken, the payment reference of the payment owner written on that notice and the decision record written with the rule version**, so that **every self-service payment is checkable in the decision log, and no intent is taken from a customer whose contact is stopped or whose channel carries no consent**.

The legacy story names the customer (borrower) as the actor, and the module specification gives FEAT-COM-03 the customer as its only primary role, with HOME.SCB and payments as its integration points (FSD P6 A2.16.2 and A2.16.3.3). The money is not this service's: Architecture v5 gives payment and proceeds matching, fees, bookings and posting files to P8 rwb-payment (slide 41), and gives rwb-comms the notice, the templates, the merge fields and the proof of delivery (slide 17). This story is therefore the rwb-comms slice of the legacy key — the self-service surface takes the customer's intent against the notice, checks it, records it and writes the decision record — and the matching, the posting and the money rows stay with P8.

### 2. Business rationale

Letters and notices are prepared by hand and the proof of delivery is chased by phone (FSD P6 A2.16.1), and the customer who receives a demand notice or accepts a plan has no way to pay against it from the same screen without a call or a branch visit. The legacy story states the outcome in one line — the customer pays against the plan or the settlement from the same screen, and the result is written to the decision log with the rule version (RWB-E4-037) — and its own Endpoints block carries only the two notice operations of the module, so the legacy build had no operation of its own for the act (GAP-1125; ASM-2073).

In the target the act splits along the module boundary. The notice of the case, its template, its proof of delivery and the self-service surface stay with rwb-comms; the plan and the settlement stay with S2 rwb-treatment; the payment instruction, its amount, its matching and its posting are P8 rwb-payment's, whose events this service listens to (Architecture v5 slides 17, 41 and 42; event rows 05, 10 and 12). The decoupling is the one the target fixes: the base is `/api/recovery/comms/v1` (DP-13), the decision record goes through the local library and the shared topic (DP-03), the contact and consent facts are read through rwb-source-data's contract and not through a view of this service (DP-05), and the screen reaches the answer through the gateway-bff composite route (DP-19).

This story is the app slice of RWB-E4-037 and owns both legacy criteria: AC1 (pay in self-service, recorded with the rule version) and AC2 (nothing changes when the decision log cannot be written). It serves the module measure "notices with proof of delivery, 100 percent" (FSD P6 A2.16.1) by giving the payment its evidenced reference on the notice, and it serves the prerequisite chain the legacy metadata names: FEAT-COM-03 depends on FEAT-COM-01 (RWB-E4-037; FSD P6 A2.16.2), the offer view of RWB-P6-E4035-APP.

### 3. Preconditions

- RWB-P6-E4037-CON is published: the two self-service payment-intent operations under `/api/recovery/comms/v1`, the PaymentIntent element set, the `payment_intent` row, the decision-record element, the consumed rows, the fakes and the declared absence of a money table, so this story builds against a fixed contract on Day 1.
- The notice of the case exists in `rwb_comms` with `case_id`, `notice_type`, `sent_date`, `barcode`, `delivery_status` and its state: the baseline is the one RWB-P6-E1052-APP and RWB-P6-E1046-APP create (TSD P6 T3.1, DF-LEG-015 to DF-LEG-023 and DF-LEG-034).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract (DP-03), so the decision record is written before the change and relayed by the platform outbox relay.
- The payment owner answers the registration of a payment intent against a plan or a settlement, and its answers are available as a fake from the first run. No operation path and no contract story of P8 is named for this key, so the row is consumed and faked with an empty Contract dependencies row (GAP-1124; ASM-2072).
- The rwb-source-data contract answers the verified contact points, the consent state per channel and the contact stop, and its answers are available as a fake from the first run (DP-05). `contact_point_ext` and the contact-stop fact are not P6 rows in the Ownership Map, so the row is consumed and faked and no C row is declared (GAP-1124; ASM-2072).
- The tables of this service are `notice`, `template`, `merge_field` and the `payment_intent` row of this key in `rwb_comms` (Ownership Map, P6). No payment, posting, plan, treatment or contact table is declared here and no other schema is read.
- The lists of the module are reference data read with the version in force: LOV-CHANNEL, LOV-NOTICE, LOV-DELIVERY and LOV-SENT-TYPE (TSD P6 T3.2); the eligible notice states of a self-service payment, the target vocabulary and the value set of the owner's state are Not specified in the source documents (GAP-1127; ASM-2075).
- The screen path is the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), so no screen of this story calls the service directly.
- No build dependency outside rwb-comms and the platform contracts: the three H rows of the metadata table are the contract baseline of this key and two platform CON stories, and the C, I and X rows are empty (Template and Rules §R5.4, §R5.7).

### 4. Flow

1. A customer, signed in through ACE Common and routed by gateway-bff to their own case, opens the notice on the self-service screen and sends `POST /api/recovery/comms/v1/notices/{noticeId}/payment-intents` with an Idempotency-Key and the request: the `target` (the plan or the settlement) and the `channel` the customer chose.
2. The service authorises the object, not only the action: the case of the notice must be inside the caller's scope, and a notice of a case outside it answers 404 without naming it.
3. The service reads the notice from `rwb_comms` and checks that it is in a state that accepts a self-service payment; the eligible states are a parameter, not code, and a notice outside it answers 409.
4. The service runs the conduct check of A2.16 before anything else happens: it reads the consent state per channel and the contact stop from the rwb-source-data contract, one hop with a 2 s budget (DP-05). A contact stop answers 409 with MSG-P6-001 naming the reason, and a channel without consent answers 409 with MSG-P6-002 naming the channel; neither takes an intent.
5. The service validates the request: `target` and `channel` are required and `channel` is a value of LOV-CHANNEL; a missing or unknown value answers 422 with MSG-GEN-001 naming the field.
6. The service writes the decision record through the local decision-record library before the change, with the decision code, the rule id and the rule version in force, the case, the notice, the target, the channel and the decided-at (DP-03).
7. The decision record written, the service registers the intent with rwb-payment, one hop with a 2 s budget, carrying the case, the notice, the target and the channel. The owner answers the payment reference and the state of the instruction, and reports whether there is anything to pay against; this service never computes an amount and never posts money.
8. The service stores the intent as one `payment_intent` row of `rwb_comms` with the owner's reference, in the same transaction as the decision record, and answers 201 with the PaymentIntent as the contract fixes it; the outbox relay of the platform publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08).
9. A customer reads `GET /api/recovery/comms/v1/notices/{noticeId}/payment-intents` and the service answers 200 with the intents of that notice, newest first, reading only `rwb_comms`.
10. The owner's events keep the picture current: a missed payment arrives on the consumed payment event and a plan or settlement approval on the consumed treatment event, and the state a reader sees is the owner's; a closed case arrives on the consumed case event.
11. A repeat of the POST with the same Idempotency-Key returns the first answer with status 201 and writes no second intent; a role without the right answers 403 with MSG-P4-002.
12. A decision record that cannot be written stops the flow at step 6: the notice and the intent rows are unchanged, no call is made to rwb-payment, the answer is 503 with MSG-P7-003 and an incident is raised under R-UNI-39.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The notice is outside the caller's scope | Refused with 404; nothing changes | None | TC-E4-037-03 |
| X2 | The notice is not in an eligible state for a self-service payment | Refused with 409; no decision record and no intent | Not specified in the source documents (GAP-1127; ASM-2075) | AC1 |
| X3 | A contact stop is in force on the case | Refused with 409; nothing is taken and no call is made to rwb-payment | MSG-P6-001 | AC1 |
| X4 | The channel carries no consent | Refused with 409; nothing is taken | MSG-P6-002 | AC1 |
| X5 | `target` or `channel` is missing, or the channel is not a value of LOV-CHANNEL | Refused with 422 | MSG-GEN-001 | AC1 |
| X6 | The decision log cannot be written | Nothing changes, no call is made to rwb-payment, the answer is 503 and an incident is raised | MSG-P7-003 | AC2 |
| X7 | rwb-payment times out or answers 5xx | Nothing is written and the answer is 503; no intent is returned as taken | Not specified in the source documents (GAP-1124; ASM-2072) | AC2 |
| X8 | rwb-source-data does not answer the consent read | The check fails closed: nothing is taken and the answer is 503 | Not specified in the source documents (GAP-1124; ASM-2072) | AC1 |
| X9 | rwb-payment reports that there is nothing to pay against for the target | Refused with 409; nothing is taken and no decision record is left behind | Not specified in the source documents (GAP-1127; ASM-2075) | AC1 |
| X10 | A role without the right of the operation | Refused with 403; nothing changes | MSG-P4-002 | TC-E4-037-03 |
| X11 | The POST is repeated with the same Idempotency-Key | The first answer is returned with status 201 and no second intent is written | None | AC1 |

X2, X7, X8 and X9 are refusals and failures this service raises itself, and the legacy story, the FSD P6 A2.16 and the TSD P6 name no message for them, so they carry the placeholder of section 14. X3, X4, X5, X6 and X10 are the messages the legacy validation table already gives for this key and the FSD A2.16.3.1 repeats (VR-P6-016-1, VR-P6-016-2), and they are copied unchanged.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4037-CON, the decision-record library and the edge route. The payment owner, the contact read and the case state are contract fakes from the first run |
| Negotiable | The eligible states of a notice, the target vocabulary and the confirmation channels are parameters and reference data; the story fixes the order of the checks and the place of the decision record |
| Valuable | The customer pays from the screen that showed the notice, and every intent carries a decision record and an owner reference; a stopped or non-consenting customer takes nothing |
| Estimable | Two operations, one service, two owner adapters, one library write, one parameter set and one new row; four legacy test cases plus the contract tests of the baseline |
| Small | Fits one sprint as the app slice of the legacy key, with no money row and no column of another owner |
| Testable | Each criterion of section 7 runs as one automated test against the contract fakes; the whole path is proven without a live payment service |

### 7. Acceptance criteria

```gherkin
Feature: Pay in self-service — the rwb-comms slice

  Background:
    Given the parameter "rwb.comms.payment-intent.eligible-notice-states" is in force
    Given notice "N-0101" of case "RC-2026-000321" is "APPROVED"
    Given LOV-CHANNEL is the channel list in force

  Scenario: AC1 Pay in self-service (legacy RWB-E4-037 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-payment contract mock returns payment intent "PI-0101" accepted against the plan of case "RC-2026-000321"
    When the user acts on the screen
    Then lets the customer pay against the plan or the settlement from the same screen
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-037 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the two criteria of RWB-E4-037 copied line for line, with the origin tag on each scenario line and one `Given the rwb-payment contract mock returns …` line added inside AC1 for the part of the criterion that names a fact of another owner: the plan and the money are P8's and S2's, so the criterion can only run against the payment owner's contract fake. Every legacy line and every legacy value is kept, and no business value is added — the intent reference and the case identifier of the fake are synthetic, as everywhere in this story set. The two criteria run against the fakes of 12.8 and answer on the contract of 12.1.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The payment intent, its amount, its matching and its posting are rwb-payment's, and the plan and the settlement are S2 rwb-treatment's; this service declares no money row, computes no amount and reads no schema of another service (DP-01) | Architecture v5 slides 17 and 41; Ownership Map (`proceeds` owned by P8, `treatment` owned by S2) |
| BR2 | The intent is registered through the rwb-payment contract, one hop with a 2 s budget; a timeout or an error takes nothing and never answers as taken (DP-11) | ADR-020; DP-11 |
| BR3 | The decision record is written before the change, through the local decision-record library and the shared topic; an intent whose record cannot be written does not proceed | R-UNI-39; DP-03; legacy AC2 |
| BR4 | The conduct check of A2.16 runs before the intent is taken: a contact stop refuses the request with MSG-P6-001 and a channel without consent refuses it with MSG-P6-002 | FSD P6 A2.16.3.1 (VR-P6-016-1, VR-P6-016-2); legacy validation table |
| BR5 | The consent state per channel and the contact stop are read from the rwb-source-data contract, one hop; this service holds no contact row and no `v_ace_*` grant of its own | DP-05; Ownership Map (`contact_point_ext` owned by P1) |
| BR6 | The notice of the case must exist and be in a state that accepts a self-service payment; the eligible states are a parameter read with its version, not code | FSD P6 A2.16.3.1 (BR-P6-016); TSD P6 T3.1 (notice state) |
| BR7 | The intent answers the plan or the settlement that the customer's arrangement carries, on a consented channel, and the target is read as reference data rather than fixed in code | R-RES-09; R-SET-04; FSD P6 A2.16.3.1 (BR-P6-016) |
| BR8 | No value a business person may change is written in code: the eligible states, the targets, the channels and the message texts are data, reference data or parameters | FSD P6 A2.16.3.1 (BR-P6-016) |
| BR9 | One base and one topic: `/api/recovery/comms/v1` and `rwb.comms.events.v1`; this story declares no other service's path or topic as its own (DP-13, DP-14) | DP-13; DP-14; Template and Rules §R4 |
| BR10 | The act publishes no event of this service: EV-13, EV-14 and EV-15 are the notice events of the dispatch stories and the payment events (EV-11, EV-12, EV-25) are rwb-payment's; the only row of the check is the library's `DecisionRecorded` on the shared topic (DP-03) | Architecture v5 slide 42 (events 08, 11 to 15); DP-03 |
| BR11 | The paid, missed or expired state of a reference arrives on the consumed payment event and from the owner's answer, and is never computed by this service | Architecture v5 slide 42 (event 12); event row of 12.4 |
| BR12 | A closed case takes no new intent; the closure is taken from the consumed case event and this service holds no case row | Architecture v5 slide 42 (event 05); Ownership Map (`recovery_case` owned by P3) |
| BR13 | A repeated POST with the same Idempotency-Key returns the first answer and writes no second intent (DP-09) | Architecture v5 slide 11; DP-09 |
| BR14 | A missing answer of an owner never takes an intent and never returns one as taken (fail closed); the retry and exception-queue handling of a downstream failure stays with the integration owner | ADR-020; DP-11; R-UNI-33; R-UNI-34 |
| BR15 | A legal hold stops every outbound action and every automated decision; this act sends nothing outbound and makes no automated decision, so the hold does not refuse it, and the dispatch stories keep their own hold check | R-UNI-20 |

### 9. State transitions

A self-service payment moves no notice state and no case state. It writes one row of this service and leaves the notice as it is:

| From | Event | Condition | To |
|---|---|---|---|
| The notice state (unchanged) | An intent is taken | The notice is eligible, the conduct check passes and the owner answers a reference | The notice state is unchanged; one `payment_intent` row exists and one decision record names the rule version |
| The notice state (unchanged) | An intent is refused on state, contact stop, consent or validation | X2, X3, X4 or X5 applies | No row, no decision record, no change |
| The notice state (unchanged) | The decision record cannot be written | The library fails | No row, no change, MSG-P7-003, incident under R-UNI-39 |
| The notice state (unchanged) | The owner does not answer or answers 5xx | X7 applies | No row, no change, 503 with the placeholder of section 14 |
| An intent row (state of the owner) | The owner reports the payment missed, or the payment arrives | The consumed payment event or the owner's read answers | The row stays; the state a reader sees is the owner's |
| An intent row (state of the owner) | The case closes | The consumed case event arrives | No new intent on that notice; the rows stay readable |

The value set of the owner's state is Not specified in the source documents (GAP-1127; ASM-2075); this service stores the state code the owner returns and never invents one. The plan, the settlement and their own state machines are S2 rwb-treatment's, and the case state and its closure are P3 rwb-case's: neither is moved here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Customer (borrower) | The only primary role of FEAT-COM-03 (FSD P6 A2.16.3.3): takes an intent against the plan or the settlement of their own notice and reads the intents of it |
| rwb-comms service identity | Reads its own `notice` row, writes the `payment_intent` row and the outbox row, and calls rwb-payment, rwb-source-data and the decision-record library (DP-02) |
| Decision-record library identity | Writes the local decision record of an intent and relays it on `rwb.decision-record.v1` (DP-03) |
| rwb-payment service identity | Owns the payment instruction, the amount due, the matching and the posting; this service calls it and never writes its rows (DP-01) |
| rwb-source-data service identity | Owns the contact points, the consent state per channel and the contact stop as an answer of its contract (DP-05) |
| rwb-case service identity | Owns the case state and its closure; this service consumes the case event and writes no case row (DP-01) |

The capability area and the right of the two operations are declared in RWB-P6-E4037-CON, because the role matrix of TSD P6 T6.1 lists staff roles only and names no right for a customer-facing self-service operation (GAP-1128; ASM-2076). Every operation authorises the object as well as the action: the case of the notice must be inside the caller's scope, which is the scope filter TSD P6 T6.2 applies to every query. The legacy story copied the Litigation rights of the two notice operations; those operations are built by RWB-P6-E1052-APP and their rights are unchanged by this story.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (`rwb_comms`, P6) | id | Read |
| DF-LEG-016 | notice (`rwb_comms`, P6) | case_id | Read |
| DF-LEG-017 | notice (`rwb_comms`, P6) | document_id | Read, for the notice reference only |
| DF-LEG-018 | notice (`rwb_comms`, P6) | notice_type | Read |
| DF-LEG-019 to DF-LEG-023 | notice (`rwb_comms`, P6) | sent_date, barcode, callback_date, delivery_status, sent_type | Read |
| DF-LEG-031 | notice (`rwb_comms`, P6) | template_id | Read, so the notice of the intent is the notice that was sent |
| Standard column | notice (`rwb_comms`, P6) | state | Read, for the eligible-state check |
| Not specified in the source documents (GAP-1126; ASM-2074) | payment_intent (`rwb_comms`, P6, new row of this key) | intent id, case_id, notice_id, target, channel, the owner's payment reference, the owner's state, requested_at | Write, then read |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, rule version, case, notice, target, channel, decided at, hash chain | Write |
| DF-REF-001 to DF-REF-015 | rule_row, through the rwb-decision contract | rule_id, rule_version | Read through the contract, never a table |
| DF-REF-045 to DF-REF-051 | template (`rwb_comms`, P6) | id, template_code, template_version, language | Read only where the notice carries a template; no template is written here |
| Not specified in the source documents (GAP-1126; ASM-2074) | payment instruction, through the rwb-payment contract | payment reference, amount, currency, state | Read the answer, never stored beyond the reference |
| Not specified in the source documents (GAP-1124; ASM-2072) | contact point, consent and contact stop, through the rwb-source-data contract | channel, consent state, stop reason | Read through the contract, never a table |
| Standard column | outbox_event, processed_event, idempotency_key (library objects in `rwb_comms`) | the outbox row of the decision record, the inbox dedupe, the POST key | Write |

The plan, the settlement, the treatment and the money rows are S2 rwb-treatment's and P8 rwb-payment's, and the contact points of ACE are read only through the source-data contract (DP-05; Ownership Map). This service declares no payment table, no amount column and no foreign key across a service boundary. The element names, types, widths, required flags and DF field ids of the `payment_intent` row are fixed by RWB-P6-E4037-CON and carry the placeholder of section 14 where no source names them (GAP-1126; ASM-2074).

The migration of this story is one per-service Flyway step in `rwb_comms` (ADR-021): it creates the `payment_intent` row of the baseline with its two indexes, `ix_payment_intent_notice_id` and `ix_payment_intent_case_id`, and adds no column to `notice`. No column of this service carries a name, an address, an identity number, an account number, a card number or a contact point. Field IDs are those of the Logical Data Model and Data Dictionary, and the row has none yet, which is the gap of section 18.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E4037-CON; this story implements them and adds no path. Neither operation is in the endpoint inventory of the TSD P6 (GAP-1125; ASM-2073).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/notices/{noticeId}/payment-intents` | Take the customer's intent to pay against the plan or the settlement of the case of the notice, 201 with the PaymentIntent | Case record, right C, scope applied | Idempotency-Key header, kept 24 hours |
| GET | `/notices/{noticeId}/payment-intents` | List the intents of the notice, newest first, 200 with the PaymentIntent list | Case record, right R, scope applied | Not applicable |

Errors: 401 no session; 403 the caller lacks the right (MSG-P4-002); 404 the notice is absent or the case is outside the scope; 409 the notice is not eligible, a contact stop is in force, the channel carries no consent or the owner reports nothing to pay against (MSG-P6-001, MSG-P6-002); 422 a field fails validation (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003) or an owner did not answer.

Request: `PaymentIntentRequest` with `target` required and a value of the target reference data, and `channel` required and a value of LOV-CHANNEL; `noticeId` comes from the path. Answer: `PaymentIntent` with `intentId`, `noticeId`, `caseId`, `target`, `channel`, `paymentReference`, `ownerState` and `requestedAt`, the last three marked in the baseline with the placeholder where the sources are silent (GAP-1126; ASM-2074).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | the operation of the rwb-payment contract that registers a payment intent against a plan or a settlement; its path and field set are Not specified in the source documents (GAP-1124; ASM-2072) | P8 rwb-payment | Registers the intent and answers the payment reference, the state and whether there is anything to pay against; faked |
| GET | the contact, consent and contact-stop read of the rwb-source-data contract; its path is Not specified in the source documents (GAP-1124; ASM-2072) | P1 rwb-source-data | Answers the consent state per channel and the contact stop of the case; faked |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). No row reads a table of another service and no row reads a `v_ace_*` view directly: the views belong to rwb-source-data under DP-05.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision record reference, decision code, rule id, rule version, case, notice, target, channel, payment reference, decided at |

The row is written to the outbox in the same transaction as the `payment_intent` row and relayed with the CloudEvents 1.0 envelope by the platform outbox relay (DP-03, DP-09); the local decision-record library of this service writes it and the type is P7's. This story publishes no event of its own: EV-13, EV-14 and EV-15 are the notice events of the dispatch stories, and the payment events are rwb-payment's (BR10).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | Refuses a new intent on a closed case and keeps the local picture of closure current; deduped through the inbox |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | Keeps the target of the customer's arrangement current, so an intent names a plan or a settlement that was approved; deduped through the inbox |
| `rwb.payment.PaymentMissed.v1` (EV-12) | `rwb.payment.events.v1` | P8 rwb-payment | Keeps the missed state of a registered reference as the owner states it; deduped through the inbox. The event that carries a completed payment is Not specified in the source documents (GAP-1129; ASM-2077), so the paid state is read from the owner's answer and never assumed |

None of the three is a decision input on its own: the checks of section 4 are made at the moment the intent is requested, and the events only keep the local picture current between calls. All three carry IDs, codes and dates only and no personal data.

#### 12.5 Workflows and activities

None. An intent is one synchronous operation of the request thread with one library write and two owner calls; there is no workflow, no activity, no durable timer and no child workflow. `NoticeDispatchWorkflow` on task queue `rwb-comms` is the dispatch stories' and a payment is not a dispatch.

#### 12.6 Schedules

None. No job of the catalogue is created, changed or read: JOB-10 (outbound notices at 16:00) belongs to the dispatch stories and to rwb-integration, and JOB-07 and JOB-08 (payment matching and booking confirmation) are rwb-payment's (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| payment_intent | P6 (rwb_comms) | The new row of this key: the intent, its target and channel, the owner's reference and state; written here |
| notice | P6 (rwb_comms) | The notice the intent answers, its case, its template and its state; read here, written by the notice stories |
| template | P6 (rwb_comms) | Read for the notice reference only; written by RWB-P6-E1046-APP and the template stories |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of an intent (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox row of the decision record, the inbox dedupe of the consumed events and the POST key |

Not owned and never read: the payment instruction, the proceeds and the posting rows of P8 rwb-payment (`payment`, `proceeds` in `rwb_payment`); `treatment`, the plan and the settlement rows of S2 rwb-treatment; `contact_point_ext`, `party_ext` and the interaction rows of P1 rwb-source-data; `recovery_case`, `task`, `timer` and `queue` of P3 rwb-case; `decision_log_entry`, `rule_row` and the rule package tables of P7 rwb-decision; `deviation` of S8 rwb-deviation. No money table is declared in `rwb_comms` (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-payment intent fake | The registration operation of the P8 contract | Payment reference `PI-0101` with the state of the instruction and a target to pay against; a target with nothing to pay against; a 5xx; an answer delayed beyond 2 s |
| rwb-source-data contact fake | The consent and contact-stop read of the P1 contract | Consent `GIVEN` for channel `SMS` on party `P-0077`; consent `WITHDRAWN`; a contact stop with a reason; a delayed answer |
| rwb-case state fake | The consumed `CaseStateChanged` row | Case `RC-2026-000321` open; the same case closed; a duplicated event for the inbox dedupe |
| rwb-treatment event fake | The consumed `TreatmentApproved` row | A plan approved for the case; a settlement approved; a duplicated event |
| rwb-payment event fake | The consumed `PaymentMissed` row | A missed payment on reference `PI-0101`; a duplicated event |
| decision-record library stub | The local library and the shared topic | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-037-04 |

The fakes are derived from the published contracts of RWB-P6-E4037-CON, and the drift test of that story fails a build in which a fake and the document disagree. The payment fake carries the placeholder of the P8 operation until the P8 contract names it (GAP-1124; ASM-2072).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The intent take and the intent list provided; the payment registration of P8 and the consent and contact-stop read of P1 consumed; one hop, 2 s |
| Kafka | 1 declared as written by the library, 3 consumed | `DecisionRecorded` through the library on the shared topic; `CaseStateChanged`, `TreatmentApproved` and `PaymentMissed` consumed; no event of this service's own |
| Temporal | None | The operation is synchronous; no workflow, activity or Schedule |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `paymentintent`, Java package `th.co.scb.ace.workbench.recovery.comms.paymentintent`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is applied through the consent and contact-stop read of 12.2 and adds no dependency, because this service holds no ACE view of its own and reads the facts on the source-data contract. DP-09 is used only through the library's outbox, which DP-03 brings with RWB-PLT-E1027-CON, so no separate platform row is added to the metadata table. DP-01 and DP-15 stand behind the boundary and the migration as rules and add no dependency.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PaymentIntentController | Controller | The two operations with validation, the Idempotency-Key and the problem mapping of 12.1 |
| PaymentIntentService | Service | Reads the notice, applies the eligible-state check, orders the conduct check, the decision record, the owner call and the row write |
| ConductCheckClient | Adapter | The consent and contact-stop read of the rwb-source-data contract, one hop, 2 s, with a breaker |
| PaymentIntentClient | Adapter | The registration of the intent with rwb-payment, one hop, 2 s, with a breaker; it never computes an amount |
| PaymentIntentWriter | Service | Writes the `payment_intent` row in the same transaction as the decision record |
| DecisionRecordClient | Adapter | The local decision-record write before the change and its outbox row |
| IntentStateProjection | Listener | Keeps the owner's state and the closure of the case current from the three consumed events, through the inbox |

**Database and migrations**

- Reads and writes `notice`, `payment_intent` and the local decision record, all in schema `rwb_comms` (DP-01); reads no other schema.
- Migration in this story: `V4037_1__payment_intent.sql` creates the `payment_intent` row of section 11 in `rwb_comms` with its two indexes. No payment table, no amount column and no foreign key to `rwb_payment` or `rwb_treatment` is created.

**Configuration and reference data**

- `rwb.comms.payment-intent.eligible-notice-states` and `rwb.comms.payment-intent.targets`, as data; their values are set at the baseline review and never in code (GAP-1127; ASM-2075).
- The channels are LOV-CHANNEL of the module, read as reference data with the version in force.
- The 2 s budget and the single retry of a GET are the platform settings of ADR-020.
- The feature switch `rwb.comms.payment-intents`, read as a parameter: off refuses both operations with 404 and takes nothing.

**Build steps**

1. PaymentIntentController and PaymentIntentService over the two operations, the Idempotency-Key and the problem mapping; tests for the repeat and the two scope refusals.
2. The notice read and the eligible-state parameter; tests for X2.
3. ConductCheckClient with the consent, stop and failure branches behind the fake; tests for X3, X4 and X8.
4. DecisionRecordClient and the fail-closed path: a failed write leaves the tables unchanged, calls no owner and answers MSG-P7-003 with the incident of R-UNI-39; test for AC2 and TC-E4-037-04.
5. PaymentIntentClient and PaymentIntentWriter in one transaction, including the nothing-to-pay-against branch; tests for AC1 and X9.
6. IntentStateProjection over the three consumed events, with the inbox dedupe and the closed-case refusal; tests for BR11 and BR12.
7. The list operation, the newest-first order, the feature switch and the contract-fake run of the whole path before the payment owner is live.

**Feature switch.** `rwb.comms.payment-intents`, read as a parameter; off refuses both operations and takes nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4037-CON stay green, every taken intent has one decision record and one owner reference, a refused or failed intent has neither, and no schema of this service names a payment, proceeds, plan or contact table.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop is in force on the case | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | The channel carries no consent | The customer has not consented to {channel}. Use another channel. |
| MSG-GEN-001 | A required field is missing or the channel is not a value of LOV-CHANNEL | Enter {field}. |
| MSG-P4-002 | The caller lacks the right of the operation | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Not specified in the source documents (GAP-1129; ASM-2077) | The notice is not eligible, the owner reports nothing to pay against, rwb-payment does not answer or answers 5xx, or rwb-source-data does not answer | The refusal answers 409 or 503 with the platform error envelope; the message ID and its text are left to the owner of the message list |

The five message IDs are copied unchanged from the validation table of the legacy story, and VR-P6-016-1 and VR-P6-016-2 of the FSD P6 A2.16.3.1 name the first two of them. The sixth message of that legacy table, MSG-P6-003 (template withdrawn), is not raised here: it belongs to the notice, the dispatch and the template stories. No message text is invented.

### 15. Screens and states

The legacy story names SCR-33 Template approval, which shows a template and its approval states and cannot show a payment. The self-service screen is the customer's own screen on HOME.SCB and the web, the first integration point FSD P6 A2.16.2 names, and it is the screen that showed the notice; it is served through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), which calls this service once for the intents of the notice and rwb-payment once for the amount due and the state, and merges the two answers. No screen of this story calls a service directly.

| State of the notice or the intent | What the customer sees |
|---|---|
| Notice shown, no intent | The amount due of the plan or the settlement from the payment owner, and the two targets |
| Intent taken | The reference, its date and the state the owner reports, next to the notice it answers |
| Refusal on contact stop, consent or state | The message of section 14 and no intent |
| Notice of a case outside the caller's scope | Nothing: the answer is 404 and no screen data is returned |

The route, the merge order, the field list of the screen and the masking at the edge belong to RWB-PLT-N001-CON and to the stories that own each part of the screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-037-01 | AC1, BR2, BR3, BR4, BR5, BR6, BR7 | End to end | Case `RC-2026-000321`, notice `N-0101` in `APPROVED`, party `P-0077` with consent `GIVEN` for `SMS` and no stop; the payment fake answers `PI-0101`; the intent is taken, one `payment_intent` row exists and one decision record names the rule version |
| TC-E4-037-02 | AC2, BR3 | End to end | Decision log stubbed unavailable; nothing changes, no call reaches rwb-payment and MSG-P7-003 is shown |
| TC-E4-037-03 | Access | Component | A caller for a notice whose case is outside the scope answers 404; a role without the right answers 403 with MSG-P4-002; nothing changes in either run |
| TC-E4-037-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 intents; no call reaches rwb-payment, no row is written and an incident is raised under R-UNI-39 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The four cases keep their legacy IDs, their legacy order, their legacy covers and their legacy data. The legacy table carries no level column, so `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR, as the levels of the target table require. The journey that leaves the contract fakes and touches the real payment owner is not owned by a separate integration story of this key; the tests above run against the fakes of 12.8.

### 17. Guardrails

- No business value in code: the eligible notice states, the targets, the channels and the message texts are data, reference data or parameters read with the version in force.
- No personal data in events, logs, prompts or tests: case IDs, notice IDs, intent references, codes, amounts and dates only. No name, address, identity number, account number, card number or contact point is written to `rwb_comms`, put in an event or logged.
- No read of another service's tables and no `v_ace_*` read of this service: the contact and consent facts arrive on the source-data contract and the money arrives on the payment contract (DP-01, DP-05).
- No payment table, no proceeds row, no amount column and no posting row in `rwb_comms`: a migration that creates one fails the review, and the amount is always the owner's answer.
- The decision record is written before the change, and an intent that cannot be recorded does not proceed: the tables are unchanged, no owner is called and an incident is raised (R-UNI-39).
- Every outbound event is written to the outbox in the same transaction as the `payment_intent` row and carries IDs and facts only (DP-03, DP-09).
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story of this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never takes an intent and never returns one as taken (ADR-020, DP-11).
- Every example is synthetic; no production payload, no production amount and no production identifier is copied into a test or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-037 |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-037 ACn) |
| Legacy test cases | TC-E4-037-01 to TC-E4-037-04, all four in the legacy order |
| Legacy feature | FEAT-COM-03 Pay in self-service (FSD P6 A2.16), prerequisite FEAT-COM-01 View the offer on LINE and web |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-023; template DF-REF-045 to DF-REF-051; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015; treatment DF-TRT-001 to DF-TRT-014 and v_ace_customer DF-ACE-055 to DF-ACE-074, both read by their owners only |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 and DP-15 in force as rules) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-RES-09, R-SET-04, R-UNI-20, R-UNI-33, R-UNI-34, R-UNI-39, BR-P6-016, VR-P6-016-1 and VR-P6-016-2 |
| Requirements | Not mapped: the P6 requirement list of the FSD holds no requirement for FEAT-COM-03, and the endpoint inventory holds no self-service payment operation (GAP-1125; ASM-2073) |
| Contract and tests | RWB-P6-E4037-CON and TC-P6-E4037-CON-01 to TC-P6-E4037-CON-06 |

The supporting facts of the legacy key — the payment instruction and the money (P8 rwb-payment), the plan and the settlement (S2 rwb-treatment), the contact and consent facts (P1 rwb-source-data) and the decision log entry (P7, DP-03) — are answered here for the rwb-comms slice and by their owners for their own slices, and this story changes none of their designs.

### 19. Out of scope

- The payment instruction, its amount, its matching, its posting, the receipt and the ledger entries: P8 rwb-payment and the stories of its epic. This story consumes the registration and builds none of it.
- The plan, the settlement and the treatment: S2 rwb-treatment. This story asks the payment owner for nothing of them and carries no plan row.
- The contact repository, the consent state per channel and the contact stop as rows: rwb-source-data on its contract, with the repository screen in RWB-P6-E4039-APP. This story reads the answer and stores none of it.
- The offer screen and the acceptance of an offer: RWB-P6-E4035-APP and RWB-P6-E4036-APP, the FEAT-COM-01 and FEAT-COM-02 slices of this module.
- The dispute in self-service and the contact stop it applies: RWB-P6-E4038-APP and S8 rwb-deviation.
- The contract baseline, its two operations, its element set, its fakes and its tests: RWB-P6-E4037-CON.
- The notice, the template, the dispatch and the proof of delivery: RWB-P6-E1052-APP, RWB-P6-E1046-APP, RWB-P6-E2021-APP, RWB-P6-E2022-APP and their contract stories.
- The right, the scope, the customer sign-in and the masking at the edge: the RWB-P4 stories, RWB-PLT-N001-CON and ACE Common; this story declares the right and applies the scope.
- The decision code and the rule id of a self-service payment, the target vocabulary, the state value set of the instruction and the event that reports a completed payment: their owners. This story carries them as placeholders and does not invent them.
