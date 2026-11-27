# RWB-P6-E4036-APP Accept an offer in self-service

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4036-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-036 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-T |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4036-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-036 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E4036-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **customer (borrower)**, I want **to accept the offer the bank has made, from the digital channel I already use, without a call or a branch visit, and to have my acceptance recorded against the notice the bank sent me and on my case with the rule version in force**, so that **my answer to the offer is a recorded fact that the case and the decision ledger can rest on, and a refusal reaches me with its reason instead of a tap that does nothing**.

The legacy story names the customer as the actor and one screen, SCR-33 Template approval, and its criterion asks for the acceptance to be recorded on the case (RWB-E4-036 AC1). The module specification names the customer (borrower) as the primary actor, the restructuring officer (FCR) as an also-user, and the integration points LINE OA and HOME.SCB (FSD P6 A2.15.3.3 and A2.15.2).

**The slice.** rwb-comms owns the notice it sent, its template and its channel, and it owns the customer's response on that notice. It owns neither the offer, nor the case and its stage, nor the party and its consent. This story is the intake of the tap: one idempotent operation that takes the customer's response against a notice it sent, checks the notice and the consumed facts it needs, writes one decision through the local decision-record library with the rule of the response and the rule version in force, and hands the acceptance on so that the case records it. It writes no case row, no treatment row and no consent row.

### 2. Business rationale

An offer reaches the customer and the answer is the routing event: `CUSTOMER_SIGNED` when the offer is accepted and signed (R-RES-16) and `CUSTOMER_DECLINED` when it is declined (R-RES-17), after a validity of 14 days (R-RES-09, R-RES-11) and under the offer clock that a contact stop holds (R-RES-19, R-RES-18). Today the answer comes by telephone or at a branch, because letters and notices are prepared by hand and proof of delivery is chased by phone (FSD P6 A2.15.1), and the case records neither the channel nor the rule version of the answer. FEAT-COM-02 closes that gap on the channel the customer already uses, and its metric is "notices with proof of delivery, 100 percent, measured on the decision log and the Workbench records, monthly" (FSD P6 A2.15.1).

The target splits the capability along its owners: the offer and its route set are rwb-treatment's (`treatment`, DF-TRT-001 to DF-TRT-014); the case and its stage are rwb-case's (`recovery_case`, DF-CAS-001 to DF-CAS-023); the party, its contact point and its consent are rwb-source-data's, reached through its contract and never through `v_ace_customer` (DP-05); the decision ledger is rwb-decision's, written through the local library (DP-03); the notice and its template are rwb-comms's (`notice`, `template`, DF-LEG-015 to DF-LEG-034 and DF-REF-045 to DF-REF-069). What is left for this service is the act itself: take the response on the notice, apply the two conduct rules that guard every contact of the module (VR-P6-015-1, VR-P6-015-2), record the response under the rule version in force, and serve it to the officer and to the case.

The legacy story is a thin entry: module P6, FEAT-COM-02, depends FEAT-COM-01, priority Must, one screen, two criteria and four test cases, and a permission check that copies Litigation C and Litigation R from the module template, which is not the right of a customer-facing answer (GAP-1108; ASM-2056). The decoupling is the pattern set of the key: the notice rows and the response stay in `rwb_comms` (DP-01 as a prohibition, no dependency); the response is a decision through the local library (DP-03); the party and its consent arrive on the rwb-source-data contract (DP-05); the base is `/api/recovery/comms/v1` (DP-13); the answer reaches the case record through the gateway-bff composite route (DP-19). DP-09 and DP-10 are deliberately absent: this capability raises no event of its own and starts no workflow.

### 3. Preconditions

- RWB-P6-E4036-CON is published: the two response operations under `/api/recovery/comms/v1`, the `ResponseRequest` and `Response` schemas, the `notice_response` row of section 11, the decision element, the consumed rows, the fakes and the drift test, so this story builds against a fixed contract on Day 1.
- The `rwb_comms` baseline exists from RWB-P6-E1052-APP and RWB-P6-AD017-APP: `notice` with `id`, `case_id`, `notice_type`, `sent_date`, `party_id` and `template_id` (DF-LEG-015, -016, -018, -019, -030, -031), and the per-service Flyway sequence that this story adds one migration to.
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with RWB-PLT-E1027-CON (DP-03), so the response decision is written before the change and relayed by the outbox relay.
- The gateway-bff composite route is live with RWB-PLT-N001-CON (DP-19): the self-service channel and the case record panel both reach this service through it, and no screen calls the service directly.
- The three consumed facts are available as fakes from the first run: the offer of the case on the rwb-treatment contract (`GET /treatments/{treatmentId}`, S2 rwb-treatment, Ownership Map), the acceptance record of the case on the rwb-case contract, and the party's contact point with its consent state on the rwb-source-data contract (DP-05). The plan names no contract story for any of the three on this key, so all three are consumed and faked and their operation paths are Not specified in the source documents (GAP-1109; ASM-2057).
- The notice of the offer is the notice the customer answers: the story accepts a response only on a notice of the case the caller reaches, and the identity of "the notice that carried the offer" is not named by any source (GAP-1109; ASM-2057).
- The conduct rules are the two of the module: VR-P6-015-1 (contact while a contact stop is in force, MSG-P6-001) and VR-P6-015-2 (a channel without consent, MSG-P6-002), and BR-P6-015 keeps every changeable value out of code.
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are this key's contract baseline and two platform CON stories, and the C row is empty (Template and Rules §R5.7, §R5.4), so the story is Day 1.

### 4. Flow

1. The customer, signed in on LINE OA or HOME.SCB, opens the offer and answers it. The channel calls `POST /api/recovery/comms/v1/notices/{noticeId}/responses` through the gateway-bff composite route with the `responseCode`, the `channel` and the `respondedAt`, and an `Idempotency-Key`.
2. The service checks the caller's right and the scope of the notice, reads the `notice` row of `rwb_comms`, and refuses with 404 when the notice is absent or outside the caller's scope; nothing is read from another schema.
3. The service checks that the notice is in a state that accepts a response, from the parameter `rwb.comms.response.eligible-states`; a notice outside it is refused with 409 and changes nothing.
4. In parallel, one hop each on the owners' contracts: the rwb-treatment read returns the offer of the case with its route set and its validity, the rwb-source-data read returns the party's contact point on that channel with its consent state and its verified flag, and the rwb-case read returns the stage of the case.
5. The conduct check runs the two rules of the module. An open contact stop on the case refuses with 409 and MSG-P6-001 naming the reason (VR-P6-015-1, R-RES-19). No verified contact point with consent for that channel refuses with 409 and MSG-P6-002 naming the channel (VR-P6-015-2). A refusal writes no decision and no response row.
6. The eligibility check runs: the response is taken only when the offer is still with the customer and inside its validity of 14 days (R-RES-09, R-RES-11, R-RES-18); outside it the answer is 409 and nothing is written. A legal hold on the case refuses the outbound answer and the acceptance under R-UNI-20.
7. On a pass, one decision is written through the local decision-record library before any change, with the case, the notice, the party, the response code, the channel, the responded at, the rule id (`R-RES-16` for an acceptance, `R-RES-17` for a decline) and the rule version in force (DP-03).
8. The decision written, the service stores one `notice_response` row of `rwb_comms` in the same transaction as the outbox row, and hands the acceptance on: one call on the rwb-case contract so that the case records the acceptance, one hop with a 2 s budget.
9. The answer is 201 with the `Response`: its identifier, the notice, the case, the response code, the channel, the responded at and the decision record reference. The library's outbox row publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08).
10. A repeat of the POST with the same `Idempotency-Key` returns the first answer with status 201 and records no second response and no second decision.
11. The officer, or the case record panel, reads the answers of a notice with `GET /api/recovery/comms/v1/notices/{noticeId}/responses`: 200 with the notice reference and the responses of that notice, newest first, and the notice with no response returns an empty list and says so.
12. A response whose decision record cannot be written stops the flow at step 7: no `notice_response` row, no hand-on call, the answer is 503 with MSG-P7-003 and an incident is raised under R-UNI-39.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The notice is absent or outside the caller's scope | Refused with 404; nothing is read or written | None | AC1 |
| X2 | The notice is not in a state that accepts a response | Refused with 409; no decision and no response row | Not specified in the source documents (GAP-1106; ASM-2054) | AC1 |
| X3 | An open contact stop on the case | Refused with 409; nothing changes and the offer clock stays with the deviation owner | MSG-P6-001 | AC1 |
| X4 | No verified contact point with consent on the channel | Refused with 409; nothing changes | MSG-P6-002 | AC1 |
| X5 | The offer is no longer with the customer, or its 14-day validity has passed | Refused with 409; nothing is written | Not specified in the source documents (GAP-1111; ASM-2059) | AC1 |
| X6 | A legal hold on the case | Refused under R-UNI-20; nothing changes | Not specified in the source documents (GAP-1111; ASM-2059) | AC1 |
| X7 | A required element is missing | Refused with 422 naming the element | MSG-GEN-001 | AC1 |
| X8 | The decision record cannot be written | Nothing changes, no response row, no hand-on call, the answer is 503 and an incident is raised | MSG-P7-003 | AC2 |
| X9 | A consumed answer is late or in error | The answer is refused closed; no decision is assumed and nothing is written | Not specified in the source documents (GAP-1109; ASM-2057) | AC1 |
| X10 | The rwb-case hand-on call times out or answers 5xx | The response row and the decision stand, the hand-on is retried and the case records the acceptance on the retry; the answer is 503 | Not specified in the source documents (GAP-1109; ASM-2057) | AC1 |
| X11 | The POST is repeated with the same `Idempotency-Key` | The first answer is returned with status 201 and no second response is recorded | None | AC1 |
| X12 | A second distinct response for the same notice | Refused; the first response stands | Not specified in the source documents (GAP-1111; ASM-2059) | AC1 |
| X13 | The role lacks the right of the operation | Refused with 403; nothing changes | MSG-P4-002 | TC-E4-036-03 |

X2, X5, X6 and X12 are refusals this service raises itself, and their message texts and the exact status of X12 are not given by the legacy story, the FSD P6 A2.15 or the TSD P6, so they carry the placeholder of section 14. X3 and X4 carry the two messages the module owns, MSG-P6-001 and MSG-P6-002, unchanged from the legacy validation table. X10 is the only path in which the decision and the response exist while the case has not yet recorded the acceptance: the record is never rolled back, because the acceptance happened, and the hand-on is retried until the owner answers.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4036-CON, the decision-record library and the edge route; the offer of rwb-treatment, the case of rwb-case and the contact point of rwb-source-data are contract fakes from the first run |
| Negotiable | The eligible notice states, the response codes, the decision code and the refusal texts are parameters or reference data; the story fixes the order of the checks, the place of the decision record and one response per notice |
| Valuable | Every acceptance and every decline is one decision with its rule version and one response row on the notice, and the case records the acceptance from it |
| Estimable | Two operations, one conduct check, one eligibility check, one decision path, three adapter calls and one versioned Flyway step |
| Small | Fits one sprint as the app slice of a thin legacy key, with one new table, one migration and no event of its own |
| Testable | Each criterion of section 7 runs against the fakes of 12.8; the whole path is proven without a second service being live |

### 7. Acceptance criteria

```gherkin
Feature: Accept an offer in self-service — the rwb-comms slice

  Background:
    Given the eligible notice states are "SENT" and "DELIVERED"
    Given notice "N-0101" of case "RC-2026-000321" for party "P-0101" is "SENT" on channel "LINE"

  Scenario: AC1 Accept an offer in self-service (legacy RWB-E4-036 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-case contract mock returns case "RC-2026-000321" with the acceptance recorded on it
    When the user acts on the screen
    Then lets the customer accept without a call or a branch visit, which records the acceptance on the case
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-036 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the two criteria of RWB-E4-036 copied line for line, with the origin tag on each scenario line and one `Given the rwb-case contract mock returns …` line added inside AC1 for the part of the criterion that names a fact of another owner: the acceptance is recorded on the case, which is rwb-case's fact, so the criterion can only run against the case contract fake. Every legacy line and every legacy value is kept and no business value is added; the case identifier is the synthetic one the fakes of 12.8 use. The two criteria run against the fakes of 12.8 and answer on the two operations of 12.1.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The customer's answer is the routing event `CUSTOMER_SIGNED` for an acceptance and `CUSTOMER_DECLINED` for a decline; this service records the fact, the case moves under rwb-case's rule | R-RES-16, R-RES-17 |
| BR2 | An offer is answered only while it is with the customer and inside its validity of 14 days; this service holds no offer, no clock and no validity date and reads them on the rwb-treatment contract | R-RES-09, R-RES-11, R-RES-18 |
| BR3 | No contact and no answer while a contact stop is in force, and the offer clock stays with the deviation owner | VR-P6-015-1, MSG-P6-001, R-RES-19 |
| BR4 | A channel is used only with a verified contact point whose consent for it is given; a withdrawn consent removes the channel and keeps the statutory notices | VR-P6-015-2, MSG-P6-002 |
| BR5 | A legal hold on the case stops every outbound action and every automated decision | R-UNI-20 |
| BR6 | The response is one decision, written before any change through the local decision-record library with its rule and the rule version in force; a write that fails blocks the step and raises an incident | DP-03; R-UNI-39; legacy AC2 |
| BR7 | An acceptance in self-service is not a signature: where Legal requires wet ink, the recorded fact is the acceptance of the offer and the signature is the paper path of the module | R-RES-16; TSD P6 T3.2 LOV-SIGNATURE-BASIS `WET_INK_REQUIRED` |
| BR8 | The notice and its template are `rwb_comms` rows; the offer, the case and the party with its consent are read on their owners' contracts, never as tables and never through `v_ace_customer` | DP-01, DP-05, Ownership Map |
| BR9 | The base is `/api/recovery/comms/v1` and the answer reaches the case record through the gateway-bff composite route | DP-13, DP-19 |
| BR10 | One notice carries one response: a repeat with the same `Idempotency-Key` returns the first answer, and a second distinct response is refused | Template and Rules §R7.2 s17; GAP-1111 |
| BR11 | No value a business person may change is written in code: the eligible notice states, the response codes, the decision code and the rule ids are data or reference data read with the version in force | FSD P6 A2.15 BR-P6-015 |
| BR12 | This act raises no business event of this service: the catalogue has no acceptance event, and the only row is the library's `DecisionRecorded` on the shared topic | Architecture v5 slide 42 (event 08); DP-03 |
| BR13 | The response row is the only state this story writes; the case stage, the treatment and the consent are never written here | Architecture v5 slide 41; Ownership Map (`recovery_case` P3, `treatment` S2, `contact_point_ext` P1) |
| BR14 | No personal data leaves the service: a response carries identifiers, a channel code, a response code, a rule id, a rule version and timestamps, and no name, address, identity number, account number or contact value | Template and Rules §R7.2 s17; TSD P6 T6.2 (masking) |

### 9. State transitions

The response of a notice is the only state this story writes. The notice state of the baseline keeps its own machine and the case stage is rwb-case's:

| From | Event | Condition | To |
|---|---|---|---|
| No response | The customer answers the notice | Every check passes and the decision is written | Recorded: one `notice_response` row with its response code, and one decision record |
| No response | The customer answers the notice | An open contact stop on the case | Refused: MSG-P6-001, no row, no decision |
| No response | The customer answers the notice | No verified contact point with consent on the channel | Refused: MSG-P6-002, no row, no decision |
| No response | The customer answers the notice | The notice is outside the eligible states, the offer has left the customer or its validity has passed | Refused: 409 and the placeholder of section 14 (GAP-1106; ASM-2054) |
| No response | The customer answers the notice | The case is under legal hold | Refused under R-UNI-20 (GAP-1111; ASM-2059) |
| No response | The customer answers the notice | The decision record cannot be written | Unchanged: 503, MSG-P7-003 and an incident (R-UNI-39) |
| Recorded | The same `Idempotency-Key` arrives again | The stored answer is inside its 24 hours | Recorded, unchanged: the first answer is returned |
| Recorded | A second distinct response arrives for the notice | Any | Refused: the first response stands (GAP-1111; ASM-2059) |
| Recorded | The hand-on call to rwb-case fails | The owner does not answer in the budget | Recorded: the row and the decision stand and the hand-on is retried |

The states of the notice (`SENT`, `DELIVERED`, `REFUSED`, `UNDELIVERABLE`, `PENDING` on LOV-DELIVERY, TSD P6 T3.2) are the notice's own and are never moved by a response, and the stage of the case does not move here: the case moves under rwb-case's rule from the acceptance it records.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Customer (borrower) | Primary actor of FSD P6 A2.15.3.3: answers the offer on LINE OA or HOME.SCB and sees the refusal reason |
| RW-RESTRUCT, restructuring officer (FCR) | Documents CRU in TSD P6 T6.1: reads the responses of the notices of the case |
| RW-CASEOWN, case owner | Documents CRU in TSD P6 T6.1: reads the responses of the cases owned |
| RW-TEAMMGR, team manager | Documents R in TSD P6 T6.1: reads the responses of the team's notices |
| RW-CONDUCT, conduct and QA officer | Documents R in TSD P6 T6.1: reads a response and its conduct outcome for a conduct review |
| RW-AUDIT, internal audit | Documents R in TSD P6 T6.1: reads the responses and their decision records |
| RW-PLATADM, platform administrator | Documents R in TSD P6 T6.1: reads the responses and operates the feature switch; no administrative write of a response |
| The self-service channel (LINE OA, HOME.SCB) | Calls the two operations through the gateway-bff composite route with the customer's session; it holds no right of its own |
| rwb-comms service identity | Reads its own `notice` row, writes `notice_response` and the outbox row, and calls the three consumed rows and the decision-record library (DP-02) |
| Decision-record library identity | Writes the response decision and relays it on `rwb.decision-record.v1` (DP-03) |

The matrix of TSD P6 T6.1 is the only source of the staff letters above. The legacy permission check names Litigation C and Litigation R, which is the module template's copy for the two notice operations and not the right of a customer-facing answer; the capability area and the right of the two response operations are declared in RWB-P6-E4036-CON as Litigation C and Litigation R with scope applied, and are Not specified in the source documents (GAP-1108; ASM-2056). The authorise contract of rwb-access is not in this story's pattern set: the right is declared on the operation and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (`rwb_comms`, P6) | id | Read |
| DF-LEG-016 | notice (`rwb_comms`, P6) | case_id | Read |
| DF-LEG-018 | notice (`rwb_comms`, P6) | notice_type | Read, to name the notice the customer answered |
| DF-LEG-019 | notice (`rwb_comms`, P6) | sent_date | Read |
| DF-LEG-030 | notice (`rwb_comms`, P6) | party_id | Read, to ask rwb-source-data for the contact point of the party |
| DF-LEG-031 | notice (`rwb_comms`, P6) | template_id | Read |
| DF-LEG-022 | notice (`rwb_comms`, P6) | delivery_status | Read, as the proof-of-delivery state of the notice |
| Standard column | notice (`rwb_comms`, P6) | state | Read, for the eligible-state parameter |
| Not specified in the source documents (GAP-1107; ASM-2055) | notice_response (new table in `rwb_comms`, P6) | id, notice_id, case_id | Write, then read |
| Not specified in the source documents (GAP-1107; ASM-2055) | notice_response (new table in `rwb_comms`, P6) | response_code, channel, responded_at | Write, then read |
| Not specified in the source documents (GAP-1107; ASM-2055) | notice_response (new table in `rwb_comms`, P6) | decision_record_id, state, version, is_active, created_at, created_by, updated_at, updated_by | Write, then read |
| DF-REF-045 to DF-REF-051, DF-REF-066 | template (`rwb_comms`, P6) | template_code, template_version, language, channel | Read, for the notice reference only |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, rule version, case, notice, party, response code, channel, decided at, hash chain | Write |
| DF-TRT-001 to DF-TRT-014 | treatment, through the rwb-treatment contract | id, case_id, treatment_type and the route set of the offer | Read through the contract, never a table |
| DF-CAS-001 to DF-CAS-023 | recovery_case, through the rwb-case contract | id, stage_code, status | Read through the contract, never a table |
| DF-ACE-055 to DF-ACE-074 | the customer and its contact point, through the rwb-source-data contract | the contact point of the party on the channel, its consent state and its verified flag | Read through the contract, never a view and never `v_ace_customer` |

The response is this service's own row: no source names it, because TSD P6 T3.1 holds `notice`, `template`, `merge_field` and `signature_request` and no response table, and the legacy data table names only the six entities of its owner modules. Its field names, its physical types and its required flags are fixed by RWB-P6-E4036-CON and carry the placeholder where no source names them (GAP-1107; ASM-2055). The offer, the case and the party are never stored here: they arrive on their owners' contracts, and no foreign key crosses a service boundary (DP-01, DP-05).

The migration of this story is one per-service Flyway step in `rwb_comms` (DP-15): it creates `notice_response` and the index `ix_notice_response_notice_id` on `notice_response (notice_id)`, which serves the read of section 12.1, and it adds no column to `notice`. No column of this service carries a name, an address, an identity number, an account number or a contact value: `channel` is a LOV-CHANNEL code (TSD P6 T3.2) and the contact value itself stays behind the rwb-source-data contract. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E4036-CON; this story implements them and adds no path. Neither operation is in the endpoint inventory of the TSD, which stops at API-P6-011 (GAP-1106; ASM-2054).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/notices/{noticeId}/responses` | Record the customer's response to a notice and return it, 201 with the `Response` | Litigation, right C, scope applied | `Idempotency-Key` header, answer kept 24 hours |
| GET | `/notices/{noticeId}/responses` | List the responses of a notice, newest first, 200 with the `Response` list | Litigation, right R, scope applied | Not applicable |

Errors: 401 no session; 403 the role lacks the right (MSG-P4-002); 404 the notice is absent or out of scope; 409 a contact stop (MSG-P6-001), no consent on the channel (MSG-P6-002), the notice outside the eligible states, the offer no longer with the customer, a legal hold, or the notice already answered; 422 a missing or invalid element (MSG-GEN-001); 503 the decision could not be recorded (MSG-P7-003) or a consumed answer did not arrive. The `Response` body carries `id`, `noticeId`, `caseId`, `responseCode`, `channel`, `respondedAt` and `decisionRecordId`.

Request: `ResponseRequest` with `responseCode` required, `channel` required as a LOV-CHANNEL code, and `respondedAt` required; `noticeId` comes from the path. No element is a name, a contact value or free text of a person.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/treatments/{treatmentId}` of the rwb-treatment contract | S2 rwb-treatment | The offer of the case with its route set and its validity, for the eligibility check of BR2; faked; no C row (GAP-1109; ASM-2057) |
| POST | the acceptance record of the case, on the rwb-case contract, path Not specified in the source documents (GAP-1109; ASM-2057) | P3 rwb-case | Hands the acceptance on so that the case records it, as AC1 requires; faked; no C row |
| GET | the contact point of a party on a channel with its consent and verified flag, on the rwb-source-data contract, path Not specified in the source documents (GAP-1109; ASM-2057) | P1 rwb-source-data | The consent check of BR4, through the contract and never through `v_ace_customer`; faked; no C row |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. No row reads a table, no row reads a `v_ace_*` view, and no row is declared as provided by this service (DP-01, DP-05).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision record reference, decision code, rule id, rule version, case id, notice id, party id, response code, channel, responded at, decided at |

The row is written to the outbox in the same transaction as the `notice_response` row and relayed with the CloudEvents 1.0 envelope by the platform outbox relay (DP-03, DP-09 through the library); the local decision-record library publishes it and this story declares no event of its own. The catalogue row 08 is the only published row this story touches: the three notice events of this service (EV-13 `NoticeGenerated`, EV-14 `NoticeDispatched`, EV-15 `NoticeDelivered`) belong to the generation and dispatch stories and are never raised by a response (BR12).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | Takes note that the offer of the case is approved and released, so a response can be taken; deduped through the inbox (GAP-1109; ASM-2057) |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | Takes note that the case moved, closed or went under a legal hold, so a response is refused under R-UNI-20; deduped through the inbox (GAP-1109; ASM-2057) |

Neither event is a decision input on its own: the offer, the stage and the consent are read at the moment the response is recorded, and the events only keep the local picture current between calls. Both carry IDs, codes and dates only and no personal data. The shape of the local projection that answers them is fixed by RWB-P6-E4036-CON.

#### 12.5 Workflows and activities

None. The response is one synchronous operation of the request thread with one library write and three adapter calls; there is no workflow, no activity, no durable timer and no child workflow. `NoticeDispatchWorkflow` on task queue `rwb-comms` belongs to the dispatch stories of this service and is not used here.

#### 12.6 Schedules

None. No job of the catalogue is created, changed or read: JOB-10 (WIN notices, 16:00) is the dispatch run of RWB-P6-E2021-APP and RWB-P6-E2022-APP (Architecture v5 slide 44), and this capability registers no Schedule and reads no job table.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | Read for the notice the customer answered, its case, its party, its template and its state; written by RWB-P6-E1052-APP and the dispatch stories |
| notice_response | P6 (rwb_comms) | The response of the customer to a notice, created by this story; the only state this story writes |
| template | P6 (rwb_comms) | Read for the notice reference only; written by RWB-P6-E1046-APP and RWB-P6-AD017-APP |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The response decisions of this story (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox row of the decision record, the inbox dedupe of the two consumed events and the POST key |

Not owned and never read: `treatment` (S2 rwb-treatment); `recovery_case`, `task`, `timer`, `queue` and `assignment` (P3 rwb-case); `contact_point_ext`, `party_ext`, `account_ext` and `interaction` (P1 rwb-source-data); `decision_log_entry`, `rule_row` and the rule package tables (P7 rwb-decision); `document` and `signature_request` (P5 rwb-document); `deviation` (S8 rwb-deviation); `outbound_item` and `interface_config` (P2 rwb-integration). No `v_ace_*` view is read by this service (DP-05), `merge_field` is not read by this story, and no foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-treatment offer fake | The offer read and the consumed `TreatmentApproved` row | Offer of case `RC-2026-000321` with its route set, inside and outside its validity; an approved offer; an offer not yet approved; a delayed answer beyond 2 s |
| rwb-case fake | The acceptance record and the consumed `CaseStateChanged` row | Case `RC-2026-000321` open and in an offer stage; the acceptance recorded and answering its reference; a closed case; a legal hold true; a duplicated event for the inbox dedupe; a hand-on call failing with 5xx |
| rwb-source-data fake | The contact point and consent read | A verified `LINE` contact point for `P-0101` with consent given; consent withdrawn; no contact point on the channel; a delayed answer |
| decision-record library stub | The local library and the shared topic | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-036-02 |
| Self-service channel stub | The caller of the two operations | A LINE OA answer for `N-0101`; a HOME.SCB answer; a repeat with the same `Idempotency-Key`; a second distinct answer for the same notice |

The fakes are derived from the published contract of RWB-P6-E4036-CON, and the drift test of that story fails a build in which a fake and the document disagree. The treatment, case and source-data fakes carry the placeholder of their owner's side until those contracts name the paths this story consumes (GAP-1109; ASM-2057).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The response record and the response list provided; the offer read of rwb-treatment, the acceptance record of rwb-case and the contact point read of rwb-source-data consumed; one hop each, 2 s |
| Kafka | 1 published by the library, 2 consumed | `DecisionRecorded` through the library on the shared topic; `TreatmentApproved` and `CaseStateChanged` consumed; no event of this service either way |
| Temporal | None | One synchronous operation; no workflow, activity or Schedule |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `response`, Java package `th.co.scb.ace.workbench.recovery.comms.response`. Base `/api/recovery/comms/v1`, topic `rwb.comms.events.v1`, task queue `rwb-comms` in namespace `rwb-recovery`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is in force as a prohibition and is not a pattern of this key's list: the legacy data table names `recovery_case`, `treatment` and `v_ace_customer`, and the target gives the case to P3, the treatment to S2 and the party to P1, so this service declares none of their tables and reads none of them. DP-09 is used only through the library's outbox, which DP-03 brings with RWB-PLT-E1027-CON, so no separate platform row is added to the metadata table. DP-10 is not applied: the response is one synchronous step.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeResponseController | Controller | The two operations with validation, the `Idempotency-Key` and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| NoticeResponseService | Service | The ordered step of section 4: notice, conduct check, eligibility check, decision, row, hand-on, answer |
| ConductCheck | Service | The two rules of VR-P6-015-1 and VR-P6-015-2 over the consumed answers; fails closed |
| ResponseEligibility | Service | The eligible-state parameter, the offer validity from the treatment read and the legal hold from the case fact |
| TreatmentClient, CaseClient, SourceDataClient | Adapter | One hop each on the owner's contract, breaker, 2 s, no default answer |
| ResponseDecisionWriter | Service | The local decision record of BR6 written before the change, through the library |
| NoticeResponseWriter | Service | The `notice_response` row and the outbox row in one transaction, then the hand-on call |
| NoticeResponseRead | Service | The response list of a notice, newest first, with paging |

**Database and migrations**

- Reads `notice` and `template`, writes `notice_response` and the local decision record, all in schema `rwb_comms` (DP-01); reads no other schema and no `v_ace_*` view.
- Migration in this story: `V4036_1__notice_response.sql` creates `notice_response` of section 11 and the index `ix_notice_response_notice_id`, and adds no column to `notice`. No treatment, case, party or customer column is created and no foreign key to another schema is declared.

**Configuration and reference data**

- `rwb.comms.response.eligible-states`, as data; its value is set at the baseline review and never in code.
- The response codes and the decision code are reference data read with the version in force, and the rule ids `R-RES-16` and `R-RES-17` are named as reference data, never as a constant of a member list (BR11; GAP-1110; ASM-2058).
- The channel codes are LOV-CHANNEL of TSD P6 T3.2; the mapping of the channel of HOME.SCB to a LOV-CHANNEL code is Not specified in the source documents (GAP-1111; ASM-2059).
- The 2 s budget and one retry of the GET are the platform settings of ADR-020.
- The feature switch `rwb.comms.notice-response`, read as a parameter: off refuses both operations with 404 and records nothing.

**Build steps**

1. NoticeResponseController and the notice binding, with the 404, the 422 and the problem mapping; tests for X1 and X7.
2. ConductCheck over the two fakes with the contact stop and the consent: X3 and X4 with MSG-P6-001 and MSG-P6-002.
3. ResponseEligibility with the eligible-state parameter, the offer validity and the legal hold; tests for X2, X5 and X6.
4. ResponseDecisionWriter and the fail-closed path: a failed write leaves the notice unchanged and answers MSG-P7-003 with the incident of R-UNI-39; tests for AC2 and TC-E4-036-04.
5. NoticeResponseWriter and the transaction that holds the row and the outbox row together, then the hand-on call of BR1 with its retry; test for AC1 and for X10.
6. NoticeResponseRead with the newest-first order and the empty answer; test for the read side of AC1.
7. Idempotence: the repeat with the same key and the second distinct response; tests for X11 and X12.
8. The feature switch, the parameter rows and the contract-fake run of the whole path before the three owners are live, with the drift test of RWB-P6-E4036-CON in the pipeline.

**Feature switch.** `rwb.comms.notice-response`, read as a parameter; off refuses both operations with 404 and records nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4036-CON stay green, every accepted response has one decision record and one `notice_response` row and a case that recorded the acceptance, every refused response has neither, and no schema of this service names `treatment`, `recovery_case`, `contact_point_ext` or `v_ace_customer`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | An open contact stop is in force on the case | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | No verified contact point with consent on the channel | The customer has not consented to {channel}. Use another channel. |
| MSG-GEN-001 | A required element is missing or invalid | Enter {field}. |
| MSG-P4-002 | The role lacks the right of the operation | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| Not specified in the source documents (GAP-1106; ASM-2054) | The notice is outside the eligible states, or it is already answered | The refusal answers 409 with the platform error envelope; the message ID and its text are left to the owner of the message list |
| Not specified in the source documents (GAP-1111; ASM-2059) | The offer has left the customer, the offer expired, or the case is under a legal hold | The refusal answers 409 with the platform envelope; the message ID and its text are not given by any source |

MSG-P6-001, MSG-P6-002, MSG-GEN-001, MSG-P4-002 and MSG-P7-003 are copied unchanged from the validation table of the legacy story. MSG-P6-003 of that table (a withdrawn template) belongs to the dispatch of a notice and is raised by RWB-P6-E2021-APP, not here. The refusal messages of section 5 stand as placeholders until the message list is published, and no message text is invented here.

### 15. Screens and states

The legacy key names SCR-33 Template approval, which is the template screen of the module and shows a template with its Draft, approved and withdrawn states (FSD P6 Screens); it cannot show a self-service answer, and the P6 screen list of the FSD holds no screen for a response. The customer's surface is the channel itself, LINE OA and HOME.SCB (FSD P6 A2.15.2 integration points), and this story serves the two operations the channel calls and the panel the officer reads. No screen identifier for the response panel is given by any source (GAP-1111; ASM-2059).

The officer reads the responses on the case record panel through the gateway-bff composite route (DP-19), in these states:

| State | What the reader sees |
|---|---|
| Recorded | The notice type and its sent date, the response code, the channel, the responded at, the rule id and the rule version of the response |
| No response | The notices of the case with no response, and the stage of the case as its owner returns it |
| Refused | The message the customer saw, MSG-P6-001 or MSG-P6-002, with no response beside the notice |
| Not recorded | MSG-P7-003 where the decision could not be written, and the incident of R-UNI-39 |

The route, the panel field list and the masking belong to RWB-PLT-N001-CON and to the story that owns the case record view; this story serves the two operations and no screen of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-036-01 | AC1 | End to end | Notice `N-0101` of case `RC-2026-000321` for party `P-0101` in an eligible state; the fakes answer an approved offer inside its validity, a verified `LINE` contact point with consent given and no contact stop and no legal hold; the response is recorded, the decision carries `R-RES-16` with its rule version and the case records the acceptance. Legacy test: Accept an offer in self-service |
| TC-E4-036-02 | AC2 | End to end | The decision chain is forced to fail; nothing is recorded, no response row is written, MSG-P7-003 is shown and the incident of R-UNI-39 is raised. Legacy test: Not recorded |
| TC-E4-036-03 | Access | Component | A role without the right sends the POST and the GET and is refused with 403 and MSG-P4-002; a notice outside the scope answers 404. Legacy test: A role without the right is refused with MSG-P4-002 |
| TC-E4-036-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 responses; no response row is written, no hand-on call is made and an incident is raised under R-UNI-39. Legacy test: A forced decision log write failure stops the action with MSG-P7-003 |

The four cases keep their legacy identifiers, their legacy order, their legacy coverage and their legacy intent. The legacy table carries no level column, so `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR, as the levels of the target table require. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The journey that leaves the contract fakes and touches the real treatment, case and source-data services is not owned by a separate integration story of this key; the tests above run against the fakes of 12.8.

### 17. Guardrails

- No business value in code: the eligible notice states, the response codes, the decision code, the rule ids and the channel codes are data or reference data read with the version in force.
- No personal data in events, workflow inputs, logs, tests or prompts: notice IDs, case IDs, party IDs, a channel code, a response code, a rule id, a rule version and timestamps only. No name, address, identity number, account number or contact value is written to `rwb_comms` or sent to another service.
- No read of another service's tables and no `v_ace_*` read of this service: the offer, the case and the party with its consent arrive only on their owners' contracts (DP-01, DP-05).
- The decision record is written before the change, and a response that cannot be recorded does not proceed: no `notice_response` row, no hand-on call, an incident raised (R-UNI-39).
- One notice carries one response, the POST is idempotent by `Idempotency-Key` and a second distinct response is refused.
- A legal hold stops the answer, and a missing answer of an owner never counts as a pass (fail closed).
- No event of this service is invented: the only published row is the library's `DecisionRecorded` on `rwb.decision-record.v1` (DP-03).
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story of this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; no response is recorded or returned as recorded on a timeout (ADR-020).
- Every example is synthetic; no production payload, no production file and no production identifier is copied into a test or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-036 |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-036 ACn) |
| Legacy test cases | TC-E4-036-01 to TC-E4-036-04, all four in the legacy order |
| Legacy feature | FEAT-COM-02 Accept an offer in self-service (FSD P6 A2.15), prerequisite FEAT-COM-01 of the same module |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-023 and DF-LEG-030 to DF-LEG-034; template DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069; treatment DF-TRT-001 to DF-TRT-014; recovery_case DF-CAS-001 to DF-CAS-023; the customer DF-ACE-055 to DF-ACE-074; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015 |
| Legacy rules | VR-P6-015-1, VR-P6-015-2, BR-P6-015 |
| Rules | R-RES-09, R-RES-11, R-RES-16, R-RES-17, R-RES-18, R-RES-19, R-UNI-20, R-UNI-39 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 in force as a prohibition) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-019 (edge: gateway-bff and partner gateway), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Requirements | REQ-OCC-011 (customer self-service for an offer, a signature, a payment and a dispute on the bank's digital channels, Should, E4), which this story serves for the offer; the E1 and E2 requirements of the module are named in section 19 |
| Contract and tests | RWB-P6-E4036-CON and TC-P6-E4036-CON-01 to TC-P6-E4036-CON-06 |

The supporting facts of the legacy key — the offer and its route set (rwb-treatment), the case stage and the acceptance on the case (rwb-case), the party and its consent (rwb-source-data), the decision ledger (P7, DP-03) and the template screen SCR-33 (the template stories) — are answered here for the rwb-comms slice and by their owners for their own slices, and this story changes none of their designs.

### 19. Out of scope

- The offer, its amount, its route set and its validity date, and the treatment the acceptance acts on: S2 rwb-treatment (`treatment`, DF-TRT-001 to DF-TRT-014 and `POST /treatments/{treatmentId}/submit`). This story reads the offer and writes none of it.
- The case, its stage, its status and the acceptance recorded on it: P3 rwb-case (`recovery_case`, DF-CAS-001 to DF-CAS-023). This story hands the acceptance on and writes no case row.
- The contact point, the consent state, the verified flag and the channel removal: P1 rwb-source-data, reached through its contract and never through `v_ace_customer` (DP-05).
- The contact stop, the deviation codes and their clearing: S8 rwb-deviation. This story reads the contact stop as a consumed fact and shows the reason of MSG-P6-001.
- The e-signature and the paper signature where Legal requires wet ink: RWB-P6-E2018-APP and the document hub (P5 `signature_request`).
- The offer view on LINE OA and HOME.SCB: FEAT-COM-01 and the channel's own screen.
- The generation and dispatch of the notice and its proof of delivery: RWB-P6-E1052-APP, RWB-P6-E2021-APP, RWB-P6-E2022-APP and RWB-P6-E5002-APP.
- The template and merge-field administration and the screen SCR-33: RWB-P6-E1046-APP and RWB-P6-AD017-APP.
- The central decision ledger, its schema and its hash chain: P7 rwb-decision. This story writes the local record through the library (DP-03).
- The contract baseline, its two operations, its element set, its row definition, its fakes and its tests: RWB-P6-E4036-CON.
- The right, the scope and the masking at the edge, and the case record panel: RWB-P4 stories and RWB-PLT-N001-CON.
- The decision code, the response-code list and the refusal texts: the owners of the reference data and of the message list. This story carries them as placeholders and does not invent them.
