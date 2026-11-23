# RWB-P6-E4035-APP View the offer on LINE and web

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4035-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-035 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-S |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4035-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-035 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **customer (borrower)**, I want **the offer the bank has made shown to me on the channel I already use — LINE or the HOME.SCB web portal — rendered from the approved notice template of that channel and its merge fields, with my view recorded as the proof of delivery of that notice and refused when a contact stop is in force or when I have not consented to that channel**, so that **I can read the offer where I am without a call or a branch visit, and the bank can prove the notice reached me instead of chasing a callback by phone**.

The legacy story names the customer (borrower) as the actor. The module specification agrees and adds the case owner as an also-user (FSD P6 A2.14.3.3): the customer reads the offer and the case owner reads the same proof of delivery. The two channels are not screens of this workbench: LINE is reached through LINE OA and the web through HOME.SCB (FSD P6 A2.14.2 integration points), so this story serves the two operations behind those channels and the edge route that reaches them, and it builds no channel screen of its own. The offer, the customer, the contact point and the consent are not this service's facts, and this story builds none of them.

### 2. Business rationale

The module's own statement of the problem is that letters and notices are prepared by hand and that proof of delivery is chased by phone (FSD P6 A2.14.1), and its measure is "notices with proof of delivery, 100 percent, measured from the decision log and Workbench records, reviewed monthly". A customer who opens the offer in LINE or in the web portal and whose view is written against the notice is the cheapest form of that proof: the notice is the same approved template the letter path uses, and the view is a dated fact on the notice instead of a phone call. Architecture v5 gives P6 the notice, the templates, the merge fields and the proof of delivery (slide 17, slide 41), so the proof of a digital delivery belongs here and the offer itself does not.

This story is the rwb-comms app slice of legacy RWB-E4-035 (FSD P6 A2.14, FEAT-COM-01 View the offer on LINE and web, prerequisite FEAT-OCC-04 Dispatch a LINE message through LINE OA). It owns both legacy criteria, AC1 (the customer sees the offer on the channel they use, and the result is written to the decision log with the rule version) and AC2 (nothing changes and MSG-P7-003 when the decision log cannot be written), because both are satisfied inside this service once the offer, the contact point and the consent are taken from the owners' contracts. It serves REQ-OCC-011, the requirement the traceability table of TSD P6 T8 maps to FEAT-COM-01 and marks "written one epic ahead" with no story and no test.

The decoupling is the one the target fixes. The offer and its facts are rwb-treatment's and the customer, the contact point and the consent are rwb-source-data's, so both are read one hop on their contracts and faked, and no ACE view is read here (DP-01, DP-05). Neither service names a contract story in this story's Contract dependencies, so neither is declared as a C row: both are consumed and faked (GAP-1131; ASM-2079). The decision record goes through the local library and the shared topic (DP-03), the base is `/api/recovery/comms/v1` (DP-13), and the channel screens reach the answers through the gateway-bff composite route (DP-19).

### 3. Preconditions

- RWB-P6-E4035-CON is published: the two channel operations under `/api/recovery/comms/v1`, the `NoticeChannelView` and `NoticeView` elements, the capability area and right of each operation, the error set, the `NoticeDelivered` element, the four consumed events, the fakes and the drift test, so this story builds against a fixed contract on Day 1.
- The `notice` row exists in `rwb_comms` with `case_id`, `document_id`, `notice_type`, `template_id` and its state; the baseline is the one RWB-P6-E1052-APP creates and RWB-P6-E1052-CON publishes (TSD P6 T3.1, DF-LEG-015 to DF-LEG-018, DF-LEG-031).
- A template version exists for the notice and is approved for the channel the customer uses: `approved_by_legal` true, an `approved_at`, a valid-from date and a `channel` value of LOV-CHANNEL (TSD P6 T3.1, DF-REF-051, DF-REF-064, DF-REF-065, DF-REF-066). A template that is withdrawn or not approved for the channel is refused with MSG-P6-003.
- The merge-field catalogue answers the merge codes of the template with their source entity and field, their required flag and their personal-data flag (TSD P6 T3.1, DF-REF-252 to DF-REF-260), so the answer is rendered from data and no merge code is written in code.
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract (DP-03), so the decision record is written before the change and relayed by the platform outbox relay.
- The offer of the case is answered on the rwb-treatment contract with the facts the answer renders, one hop with a 2 s budget. No S2 contract story is named in this story's Contract dependencies, so the read is consumed and faked (GAP-1131; ASM-2079). Which fields of the treatment read carry the offered amount, the settlement amount and the validity date is Not specified in the source documents (GAP-1131; ASM-2079).
- The customer, the verified contact point of the channel and its consent state are answered on the rwb-source-data contract, read one hop with a 2 s budget, because the 30 `recovery.v_ace_*` views are read only by rwb-source-data (DP-05; Architecture v5 slide 8). This service reads no `v_ace_*` view of its own, holds no grant on an ACE schema and stores no contact point. No P1 contract story is named, so the read is consumed and faked (GAP-1131; ASM-2079). The data product code that carries the contact point and its consent is Not specified in the source documents (GAP-1131; ASM-2079).
- The two channel values are `LINE` and `PORTAL` of LOV-CHANNEL (TSD P6 T3.2); "web" in the feature name is HOME.SCB, the bank's web portal, and no source gives a separate `WEB` value, so the web channel is `PORTAL` (GAP-1134; ASM-2082).
- The screen path is the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), so no channel screen of this story calls the service directly.
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are the contract baseline of this key and two platform CON stories, and the C, I and X rows are empty (Template and Rules §R5.7, §R5.4).

### 4. Flow

1. The customer opens the offer in LINE OA or in HOME.SCB; the edge calls `GET /api/recovery/comms/v1/notices/{noticeId}/channel-view?channel={channel}` through the gateway-bff composite route, with `channel` one of LOV-CHANNEL and no other parameter.
2. The service reads the notice from `rwb_comms`: a notice that is absent or outside the caller's scope answers 404 and nothing else is read.
3. The service checks the template of the notice: it must be approved for that channel and not withdrawn (DF-REF-051, DF-REF-064, DF-REF-066); otherwise the answer is 409 with MSG-P6-003 and the offer is not shown.
4. The service reads the contact point of the channel and its consent state on the rwb-source-data contract, one hop with a 2 s budget. A contact stop in force refuses the view with 409 and MSG-P6-001 (VR-P6-014-1); a channel without consent refuses it with 409 and MSG-P6-002 (VR-P6-014-2). Both checks are re-run at step 8, because a stop can be raised between the read and the record.
5. The service reads the offer of the case on the rwb-treatment contract, one hop with a 2 s budget. No offer in force, an offer whose validity has passed, or an answer the owner does not return is refused with 409 or 503 respectively, and nothing is shown.
6. The service resolves the merge codes of the template against the facts it holds and the facts the owners returned, and answers 200 with the `NoticeChannelView`: the notice and case references, the notice type, the template code, version and language, the channel, the offer reference and its validity date, and the merge values the channel renders. The merge values are carried in the answer and never written to `rwb_comms`.
7. The customer's view is posted by the channel: `POST /api/recovery/comms/v1/notices/{noticeId}/views` with an Idempotency-Key and the view: `channel` and `viewed_at`.
8. The service re-runs the two checks of step 4 against the contact point as it stands at that moment and refuses with 409 and MSG-P6-001 or MSG-P6-002, so a view is never recorded on a stop or on an unconsented channel.
9. The service writes the decision record through the local decision-record library before any change, with the decision code and the rule id of the view, the notice, the case, the channel and the viewed-at (DP-03).
10. The decision record written, the service writes one `notice_view` row, sets `delivery_status` to `DELIVERED` and `callback_date` to the date the proof came back, which for a digital view is the view date, and answers 201 with the `NoticeView`.
11. In the same transaction the service writes `rwb.comms.NoticeDelivered.v1` to the outbox when the notice was not already `DELIVERED`, and the outbox relay of the platform publishes it; a view on a notice already `DELIVERED` records the view and publishes no second event.
12. A repeat of the POST with the same Idempotency-Key returns the first answer with status 201 and records no second view and no second event.
13. A role without the right of the operation answers 403 with MSG-P4-002, and a decision record that cannot be written stops the flow at step 9: the notice and the view are unchanged, the answer is 503 with MSG-P7-003 and an incident is raised under R-UNI-39.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A contact stop is in force for the customer | The view is refused with 409; no view row, no notice change, no event | MSG-P6-001 | AC1 |
| X2 | The customer has not consented to the channel | The view is refused with 409; nothing changes | MSG-P6-002 | AC1 |
| X3 | The template of the notice is withdrawn or not approved for the channel | The offer is not shown and the view is refused with 409; nothing changes | MSG-P6-003 | AC1 |
| X4 | The case has no offer in force, or the offer validity has passed | Refused with 409; no record and no view | Not specified in the source documents (GAP-1131; ASM-2079) | AC1 |
| X5 | The rwb-source-data or the rwb-treatment contract times out or answers 5xx | The view is refused with 503 and nothing is recorded (fail closed) | Not specified in the source documents (GAP-1131; ASM-2079) | AC1 |
| X6 | The decision log cannot be written | Nothing changes, no view is recorded, the answer is 503 and an incident is raised | MSG-P7-003 | AC2 |
| X7 | A role without the right of the operation | Refused with 403; nothing changes | MSG-P4-002 | TC-E4-035-03 |
| X8 | The notice is outside the caller's scope | Refused with 404; nothing changes | None | TC-E4-035-03 |
| X9 | The POST is repeated with the same Idempotency-Key | The first answer is returned with status 201; no second view and no second event | None | AC1 |
| X10 | The case is under legal hold | The view is refused under R-UNI-20 and nothing changes | Not specified in the source documents (GAP-1131; ASM-2079) | AC1 |

MSG-P6-001, MSG-P6-002 and MSG-P6-003 are copied unchanged from the validation table of the legacy story and are the three refusal messages the module gives this feature (FSD P6 A2.14.3.1). X1, X2 and X3 are therefore the only refusals of section 5 whose text the sources give; the texts of X4, X5 and X10 and the exact status of X10 are not given by the legacy story, FSD P6 A2.14 or TSD P6, so they carry the placeholder of section 14. X10 rests on R-UNI-20 ("a legal hold stops every outbound action and every automated decision"); showing the offer and recording the delivery are outbound actions.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4035-CON, the decision-record library and the edge route. The offer, the contact point, the consent and the case state are contract fakes and a consumed event from the first run |
| Negotiable | The channel list, the decision code, the rule id and the refusal texts are reference data and message-list rows; the story fixes the order of the checks and the place of the decision record |
| Valuable | Every offer shown on a channel carries a decision record and a dated proof of delivery on its notice, and a stop, an unconsented channel or a withdrawn template shows nothing |
| Estimable | Two endpoints, one new table, one library write, two owner adapters, one consumed event projection and the parameter set; four legacy test cases plus the contract tests of the baseline |
| Small | Fits one sprint as the app slice of the legacy key; the contract baseline, the offer, the contact repository and the channel screens are other stories' |
| Testable | Each criterion of section 7 runs as one automated test against the contract fakes; the whole path is proven without a second service being live |

### 7. Acceptance criteria

```gherkin
Feature: View the offer on LINE and web — the rwb-comms slice

  Background:
    Given notice "N-0401" of case "RC-2026-000401" is "Sent" with template "OFFER-LINE" version 3 approved for channel "LINE"
    Given the offer "TRT-2026-000401" of case "RC-2026-000401" is in force until "2026-12-12"

  Scenario: AC1 View the offer on LINE and web (legacy RWB-E4-035 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-source-data contract mock returns the verified "LINE" contact point of case "RC-2026-000401" with consent "GIVEN" and no contact stop, and the rwb-treatment contract mock returns the offer "TRT-2026-000401" of that case in force
    When the user acts on the screen
    Then lets the customer see the offer the bank has made, on the channel they use
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-035 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the two criteria of RWB-E4-035 copied line for line, with the origin tag on each scenario line. One line is added inside AC1 for the part of the criterion that names a fact of another owner, and it is the only added line: the offer is S2's and the contact point and its consent are P1's, so the criterion can only run against the two contract fakes, and every value of the criterion is kept. No business value is added. The Background names the data the criterion assumes and no contract answer; the two criteria run against the fakes of 12.8 and answer on the contract of 12.1.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The offer is shown on the channel the customer uses; the channels of this story are `LINE` and `PORTAL` of LOV-CHANNEL, and the web channel of HOME.SCB is `PORTAL` because no source gives a `WEB` value | FSD P6 A2.14.1 and A2.14.2 (integration points LINE OA, HOME.SCB); TSD P6 T3.2 |
| BR2 | A contact stop stops every contact attempt and every outbound action: the offer is not shown and no view is recorded | VR-P6-014-1 (MSG-P6-001); R-RES-19; R-LIT-05 |
| BR3 | A message to a channel without consent is refused; the offer is not shown and no view is recorded | VR-P6-014-2 (MSG-P6-002); R-RES-09 ("send it on a consented channel") |
| BR4 | No value a business person may change is written in code: the channel list, the decision code, the rule id and the refusal texts are data and reference data read with the version in force | BR-P6-014; Template and Rules §R7.2 s17 |
| BR5 | The view is the proof of delivery of the notice: it sets `delivery_status` to `DELIVERED` and `callback_date` to the view date, the date the proof came back | FSD P6 A2.14.1 (metric "notices with proof of delivery"); TSD P6 T3.1 (DF-LEG-021, DF-LEG-022) |
| BR6 | The decision record is written before the change, through the local decision-record library and the shared topic; a view whose record cannot be written does not proceed | R-UNI-39; DP-03; legacy AC2 |
| BR7 | A legal hold on the case stops the offer being shown and the view being recorded | R-UNI-20 |
| BR8 | The offer is shown only from a template version approved by Legal for that channel and valid on the day; a withdrawn or unapproved template shows nothing | FSD P6 (MSG-P6-003); TSD P6 T3.1 (DF-REF-051, DF-REF-064, DF-REF-065, DF-REF-066) |
| BR9 | The offer facts and the customer, contact point and consent facts are read one hop on their owners' contracts and never from a table of theirs; this service reads no `v_ace_*` view | DP-01; DP-05; Architecture v5 slide 8 |
| BR10 | At most one `NoticeDelivered` per notice: the first delivery, WIN or digital, publishes it, and a later view records the view and publishes nothing | Architecture v5 slide 42 (event 15); RWB-P6-E1055-CON (no second delivered) |
| BR11 | One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery` | DP-13; DP-14; Template and Rules §R4 |
| BR12 | A repeated POST with the same Idempotency-Key returns the first answer and records no second view | Architecture v5 slide 11; DP-09 |
| BR13 | The answer renders the merge values of the template from the facts of their owners; no merge value, no contact point and no name is written to `rwb_comms` | Template and Rules §R7.2 s17; TSD P6 T3.1 (DF-REF-258 personal_data) |
| BR14 | The case state and the legal hold are rwb-case's facts and arrive on the consumed event; this service holds no case row | Architecture v5 slide 41 (P3 owns the case); DP-01 |

The events of the catalogue this story listens to are only 05 `CaseStateChanged`, 06 `DeviationRaised`, 07 `DeviationCleared` and 10 `TreatmentApproved`, and the only event it publishes is 15 `NoticeDelivered` (12.3, 12.4). Event 08 `DecisionRecorded` is not a business event of this story: it is the local decision-record library's row on the shared topic (DP-03). No source states which event a digital view raises, so the publication of 15 on a view is this story's decision and is recorded as a gap (GAP-1132; ASM-2080).

### 9. State transitions

The notice lifecycle is declared by RWB-P6-E1055-CON and built by the notice stories; this story moves one transition of it and adds one row beside it:

| From | Event | Condition | To |
|---|---|---|---|
| Sent | A view is recorded on the channel | No contact stop, consent given, template approved for the channel, offer in force, decision record written | Delivered: `delivery_status` `DELIVERED`, `callback_date` the view date, one `notice_view` row, one `NoticeDelivered` |
| Sent | A view is refused on the contact stop or on consent | VR-P6-014-1 or VR-P6-014-2 applies | Sent, unchanged; no view row and no event |
| Sent | A view is refused on the template or on the offer | The template is withdrawn or not approved for the channel, or no offer is in force | Sent, unchanged; no view row and no event |
| Sent | The decision record cannot be written | The library fails | Sent, unchanged; MSG-P7-003 and an incident under R-UNI-39 |
| Delivered | A second view is recorded on the channel | The notice is already `DELIVERED` | Delivered, unchanged; one more `notice_view` row and no second event |
| Delivered | Any view attempt | The case is under legal hold | Delivered, unchanged; the refusal of X10 |

The `notice_view` row has no state of its own: a view is a fact, written once per view and never updated. The offer's own state, its validity and its expiry are rwb-treatment's (R-RES-09 gives the offer a 14-day validity), and the case state and the hold are rwb-case's, so the two are consumed as facts and never written here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Customer (borrower) | The primary actor of FSD P6 A2.14.3.3: opens the offer on LINE or on HOME.SCB and posts the view. TSD P6 T6.1 holds no customer row, so the customer's own identity is authorised at the edge and not by a letter of the matrix (GAP-1134; ASM-2082) |
| RW-LITOFF, litigation officer | Litigation CRUA in TSD P6 T6.1: records a view on the notices of the litigation files and reads the channel view (rights C and R) |
| RW-ENFORCE, enforcement owner | Litigation CRU in TSD P6 T6.1: records a view taken for enforcement and reads it (rights C and R) |
| RW-CASEOWN, case owner | Litigation R in TSD P6 T6.1: reads the channel view of the cases owned, the also-user of FSD P6 A2.14.3.3 |
| RW-TEAMMGR, team manager | Litigation R in TSD P6 T6.1: reads the channel views of the team's cases |
| RW-COMPLAIN, complaint officer | Litigation R in TSD P6 T6.1: reads the channel view of a case under a complaint |
| RW-LEGAL, legal counsel | Litigation RA in TSD P6 T6.1: reads the channel view and approves the template the channel renders |
| RW-AUDIT, internal audit | Litigation R in TSD P6 T6.1: reads the views and their decision records |
| RW-COMPLY, compliance and PDPA officer | Litigation R in TSD P6 T6.1: reads the views of a notice under a compliance request |
| rwb-comms service identity | Reads its own `notice`, `template` and `merge_field` rows, writes the view row, the two notice columns and the outbox row, and calls the two owner contracts and the decision-record library (DP-02) |
| Decision-record library identity | Writes the local decision record of the view and relays it on `rwb.decision-record.v1` (DP-03) |

The legacy permission check names Litigation C for RW-LITOFF and RW-ENFORCE and Litigation R for a long role list, and the matrix of TSD P6 T6.1 is the only source of the letters above. The two operations inherit the capability area and the right of the notice resource they extend — Litigation C for the write, the right of API-P6-001, and Litigation R for the read, the right of API-P6-002 — because no source declares an offer-view right (GAP-1134; ASM-2082). The authorise contract of rwb-access is not in this story's pattern set: the right is declared on the operation and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (`rwb_comms`, P6) | id | Read |
| DF-LEG-016 | notice (`rwb_comms`, P6) | case_id | Read |
| DF-LEG-017 | notice (`rwb_comms`, P6) | document_id | Read, as the reference of the generated offer letter |
| DF-LEG-018 | notice (`rwb_comms`, P6) | notice_type | Read |
| DF-LEG-021 | notice (`rwb_comms`, P6) | callback_date | Write on a view, with the view date |
| DF-LEG-022 | notice (`rwb_comms`, P6) | delivery_status | Write on a view, to `DELIVERED` |
| DF-LEG-031 | notice (`rwb_comms`, P6) | template_id | Read |
| Standard column | notice (`rwb_comms`, P6) | state, version, updated_at, updated_by | Read, and version and updated_at written with the view |
| DF-REF-045 to DF-REF-051, DF-REF-063 to DF-REF-066 | template (`rwb_comms`, P6) | template_code, template_version, language, body_ref, approved_by_legal, approved_at, valid_from, channel | Read |
| DF-REF-252 to DF-REF-260 | merge_field (`rwb_comms`, P6) | merge_code, source_entity, source_field, field_id, is_required, personal_data, catalog_version, valid_from | Read |
| Not specified in the source documents (GAP-1133; ASM-2081) | notice_view (`rwb_comms`, P6) | id, notice_id, case_id, channel, viewed_at and the reference of the channel session | Written on a view, then read |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer, through the rwb-source-data contract | the customer, the verified contact point of the channel and its consent state | Read through the contract, never a table and never a view of this service |
| DF-TRT-001 to DF-TRT-014 | treatment, through the rwb-treatment contract | the offer of the case, its type, its proposed-at and its validity | Read through the contract, never a table |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, rule version, case, notice, channel, decided at, hash chain | Write |
| DF-REF-001 to DF-REF-015 | rule_row, through the rwb-decision contract | rule_id, rule_version | Read through the contract, never a table |
| Standard column | outbox_event, processed_event, idempotency_key (library objects in `rwb_comms`) | the outbox row of the delivery event, the inbox dedupe of the four consumed events, the POST key | Write |

The offer, its validity and its plan are S2's rows in `rwb_treatment`; the customer, the contact point and the consent are P1's, and `account_ext`, `party_ext` and `contact_point_ext` are P1's extension rows (Ownership Map). This service reads none of them, holds no grant on those schemas and declares no foreign key across a boundary: `notice.case_id` and `notice.document_id` are identifiers, not keys of another service.

The migration of this story is one per-service Flyway step in `rwb_comms` (DP-15; RWB-PLT-E1044-CON is not in this story's build list, so the step follows the baseline sequence of RWB-P6-E1046-APP): `V4035_1__notice_view.sql` creates `notice_view` with its five elements and an index on `(notice_id, viewed_at)`, all nullable-safe and with no default and no backfill. No column of the table carries a name, an address, an identity number, an account number or a contact point: the channel is a LOV code and the session reference is an opaque identifier, so the merge values are rendered at request time and stored nowhere. The table name, the column names and the field IDs are this story's design and are Not specified in the source documents (GAP-1133; ASM-2081).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E4035-CON; this story implements them and adds no path. Neither operation is in the endpoint inventory of the TSD (GAP-1130; ASM-2078).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/notices/{noticeId}/channel-view?channel={channel}` | Answer the offer of the notice rendered for one channel from the approved template and its merge fields, 200 with the `NoticeChannelView` | Litigation R, scope applied | Not applicable |
| POST | `/notices/{noticeId}/views` | Record one customer view of the offer as the proof of delivery of the notice, 201 with the `NoticeView` | Litigation C, scope applied | Idempotency-Key header required, answer kept 24 hours |

Errors: 401 no session; 403 the caller lacks the right (MSG-P4-002); 404 the notice is absent or out of scope; 409 a contact stop (MSG-P6-001), no consent (MSG-P6-002), a withdrawn or unapproved template (MSG-P6-003), no offer in force, or a legal hold; 422 a field fails validation (MSG-GEN-001), including a `channel` outside LOV-CHANNEL; 503 the decision was not recorded (MSG-P7-003) or an owner did not answer. The `NoticeChannelView` carries the notice and case references, the notice type, the template code, version and language, the channel, the offer reference and validity date, and the merge values; the `NoticeView` carries the view reference, the notice and case references, the channel, the viewed-at and the delivery status. The view reference, the viewed-at type and the members the sources do not name carry the placeholder (GAP-1133; ASM-2081).

Request: `POST` body `NoticeViewRequest` with `channel` required and one of LOV-CHANNEL, and `viewed_at` required; no field is a name, an address, an identity number or a contact point, and the body carries no merge value.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/data-products/{productCode}/records` of the rwb-source-data contract | P1 rwb-source-data | Answers the customer, the verified contact point of the channel and its consent state (DP-05). Faked; no P1 contract story is named in this story's Contract dependencies (GAP-1131; ASM-2079), and the product code is Not specified in the source documents (GAP-1131; ASM-2079) |
| GET | `/treatments/{treatmentId}` of the rwb-treatment contract | S2 rwb-treatment | Answers the offer of the case, its type and its validity, so the channel view shows an offer in force; faked; same gap |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream (ADR-020). No row reads a table, no row reads a `v_ace_*` view, and no row is declared as provided by this service (DP-01, DP-05).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs, codes and dates only) |
|---|---|---|---|---|
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` (retry and `.dlt`) | P6 rwb-comms | caseId | notice id, case id, delivered date, callback date, delivery status and the channel of the delivery |

The row is written to the outbox in the same transaction as the view row and the two notice columns, and relayed with the CloudEvents 1.0 envelope by the platform outbox relay (DP-09; the library arrives with DP-03). The element reuses the shape RWB-P6-E1055-CON declares for the WIN path — notice id, case id, delivered date, callback date and delivery status, keyed by caseId — and adds `channel` additively within major version 1. The publication on a digital view is justified by the measure "notices with proof of delivery, 100 percent" of FSD P6 A2.14.1, which counts delivered notices, and by catalogue row 15 of Architecture v5 slide 42, whose owner is P6 and whose consumers are rwb-litigation, rwb-guarantee and rwb-case — the three parties that need the delivery date, rwb-case to start its notice period. No source states which event a digital view raises, so the trigger is this story's decision and is recorded as a gap (GAP-1132; ASM-2080); the first delivery only publishes it, by BR10.

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | Keeps the local picture of the case state and a legal hold current, so a view on a held case is refused under R-UNI-20; deduped through the inbox |
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | Raises the local contact-stop flag when a stop is raised by X1 or X2, so a view is refused between two calls to the rwb-source-data contract (VR-P6-014-1; R-RES-19; R-LIT-05) |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | Clears the local contact-stop flag when the stop is lifted |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | S2 rwb-treatment | Keeps the local picture of an approved offer for the case, so a case with no approved offer is refused and a case with one is not read on every view |

The four rows are consumed inside this service with the inbox dedupe, and none of them is a decision input on its own: the contact point, the consent, the offer and the case state are read at the moment of the request and the event only keeps the local picture current between calls. No event carries a name, an address, an identity number or a contact point. The shape of the local projection that answers each row is Not specified in the source documents (GAP-1131; ASM-2079).

#### 12.5 Workflows and activities

None. The channel view is one synchronous read with two adapter calls, and the view record is one synchronous write with one library write and one outbox row; there is no workflow, no activity, no child workflow and no durable timer. `NoticeDispatchWorkflow` on task queue `rwb-comms` in namespace `rwb-recovery` is the dispatch stories' and is not started or signalled here.

#### 12.6 Schedules

None. No Temporal Schedule, no cron and no catch-up window is created, changed or read: JOB-10 (WIN notices, 16:00) is the letter dispatch of RWB-P6-E2021-APP with rwb-integration, and no job row of the catalogue belongs to an offer view (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice of the offer, its `template_id`, its state, and the two delivery columns a view writes |
| notice_view | P6 (rwb_comms) | One row per customer view: the notice, the case, the channel, the viewed-at and the session reference; created by this story |
| template | P6 (rwb_comms) | Read for the code, version, language, body, approval, validity and channel; written by the template stories |
| merge_field | P6 (rwb_comms) | Read for the merge codes, their source entity and field, their required and personal-data flags; written by the catalogue story |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of a recorded view (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox row of the delivery event, the inbox dedupe of the four consumed events and the POST key |

Not owned and never read: `treatment`, `treatment_plan` and the treatment timers (S2 rwb-treatment); `account_ext`, `party_ext`, `contact_point_ext`, `interaction` and the data-product rows (P1 rwb-source-data); `recovery_case`, `task`, `timer` and `queue` (P3 rwb-case); `deviation` (S8 rwb-deviation); `decision_log_entry`, `rule_row` and the rule package tables (P7 rwb-decision); `document`, `document_text` and the document rows (P5 rwb-document); `outbound_item` and `interface_config` (P2 rwb-integration). No `v_ace_*` view is named in a query of this service (DP-01, DP-05), and no table of another owner is created or altered by this story's migration.

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-source-data contact fake | The customer, contact point and consent read of 12.2 | Case `RC-2026-000401` with a verified `LINE` contact point and consent `GIVEN`; the same case with consent `NOT_GIVEN`; the same case with a contact stop in force; a contact point that is not verified; a delayed answer beyond 2 s |
| rwb-treatment offer fake | The offer read of 12.2 | Offer `TRT-2026-000401` in force until `2026-12-12`; a case with no offer; an offer whose validity has passed; a delayed answer beyond 2 s |
| rwb-case state fake | The `CaseStateChanged` row of 12.4 | Case `RC-2026-000401` open; the same case closed; a legal hold true; a duplicated event for the inbox |
| rwb-deviation event fake | The two deviation rows of 12.4 | A stop raised for the case; the same stop cleared; a duplicated event for the inbox |
| decision-record library stub | The local library and the shared topic | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-035-04 |
| Delivery event fake | The published row of 12.3 | A first delivery writing one outbox row; a second view on an already `DELIVERED` notice writing none |

The fakes are derived from the published contracts of RWB-P6-E4035-CON, and the drift test of that story fails a build in which a fake and the document disagree. The contact and offer fakes carry the placeholder of the P1 and S2 side until those owners publish the two contract elements (GAP-1131; ASM-2079).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The channel view and the view record provided; the contact point and consent read and the offer read consumed; one hop, 2 s |
| Kafka | 1 published, 4 consumed | `NoticeDelivered` on `rwb.comms.events.v1`; `CaseStateChanged`, `DeviationRaised`, `DeviationCleared` and `TreatmentApproved` consumed; `DecisionRecorded` written by the local library on the shared topic |
| Temporal | None | Both operations are synchronous; no workflow, activity or Schedule |
| File | None | No file is read or written by this story; the channel screens are the edge's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `offerview`, Java package `th.co.scb.ace.workbench.recovery.comms.offerview`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 is the pattern this key needs most: the legacy story reads `v_ace_customer` for the customer and the contact point, and in the target no service but rwb-source-data reads an ACE view (Architecture v5 slide 8), so the read is a data-product read on P1's contract and no `v_ace_*` name appears in a query of this service. DP-01 is in force as a prohibition and is not a pattern of this key's list, and it adds no dependency. DP-09 arrives with the library that DP-03 brings, so no separate platform row is added. DP-14 is applied as a rule of the naming and not as a dependency, because the topic name is the platform's.

**Components**

| Component | Type | Responsible for |
|---|---|---|
| ChannelViewController | Controller | The two operations with validation, the `Idempotency-Key`, the scope check and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| ChannelViewService | Service | Reads the notice and the template, orders the consent, stop and offer checks, resolves the merge fields and assembles the `NoticeChannelView` |
| NoticeViewRecorder | Service | Re-runs the checks, writes the decision record, the `notice_view` row, the two notice columns and the outbox row in one transaction |
| ContactConsentClient | Adapter | The customer, contact point and consent read of the rwb-source-data contract, one hop, 2 s, with a breaker |
| OfferClient | Adapter | The offer read of the rwb-treatment contract, one hop, 2 s, with a breaker |
| DeliveryRuleGuard | Service | VR-P6-014-1, VR-P6-014-2, the template approval for the channel, the offer in force and the legal hold, with the refusals of section 5 |
| MergeRenderer | Service | Resolves the merge codes of the template from the merge_field catalogue against the facts of their owners; stores nothing |
| DecisionRecordClient | Adapter | The local decision-record write before the change and its outbox row, through the library |
| DeliveryEventPublisher | Service | Writes `NoticeDelivered` once per notice, in the same transaction as the view |

**Database and migrations**

- Reads and writes `notice`, `notice_view`, `template`, `merge_field` and the local decision record, all in schema `rwb_comms` (DP-01); reads no other schema.
- Migration in this story: `V4035_1__notice_view.sql` creates the `notice_view` table of section 11 and the index `ix_notice_view_notice` on `(notice_id, viewed_at)`. No table of another owner is created, altered or keyed.
- No row of `template` or `merge_field` is written here.

**Configuration and reference data**

- `rwb.comms.offerview.channels`, read as data: the channel values a view accepts, a subset of LOV-CHANNEL (`LINE`, `PORTAL`). Its value is set at the baseline review and never in code.
- The decision code and the rule id of a view are reference data read with the version in force; they are Not specified in the source documents (GAP-1131; ASM-2079).
- The 2 s budget and the one retry of a GET are the platform settings of ADR-020.
- The feature switch `rwb.comms.offer-channel-view`, read as a parameter: off refuses both operations with 404 and records nothing.

**Build steps**

1. ChannelViewController and ChannelViewService over the read, with the scope check, the parameter and the problem mapping; test for the 404 of X8 and the 403 of X7.
2. DeliveryRuleGuard with VR-P6-014-1, VR-P6-014-2, the template approval for the channel and the legal hold; tests for X1, X2, X3 and X10.
3. ContactConsentClient with the contact, consent and stop branches behind the fake, and the fail-closed path of X5; test for X5.
4. OfferClient with the offer in force, no offer and expired offer branches behind the fake; test for X4.
5. MergeRenderer over the merge_field catalogue with the required and personal-data flags; test that no merge value is written to `rwb_comms`.
6. NoticeViewRecorder with the decision record before the change, the view row, the two notice columns and the outbox row in one transaction; tests for AC1 and for the repeat key of X9.
7. DecisionRecordClient and the fail-closed path: a failed write leaves the notice unchanged and answers MSG-P7-003 with the incident of R-UNI-39; test for AC2 and TC-E4-035-04.
8. DeliveryEventPublisher with the once-per-notice rule of BR10 and the four consumed rows with their inbox dedupe; test for the second view and for a duplicated event.
9. The feature switch, the parameter rows and the contract-fake run of the whole path before rwb-source-data and rwb-treatment are live.

**Feature switch.** `rwb.comms.offer-channel-view`, read as a parameter; off refuses both operations and records nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4035-CON stay green, every recorded view carries one decision record, one `notice_view` row and at most one `NoticeDelivered`, every refused view carries none of the three, and no schema of this service names a treatment table, an ACE view or a deviation row.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-001 | A contact stop is in force for the customer (VR-P6-014-1, X1) | Contact with this customer is stopped for {reason}. |
| MSG-P6-002 | The customer has not consented to the channel (VR-P6-014-2, X2) | The customer has not consented to {channel}. Use another channel. |
| MSG-P6-003 | The template of the notice is withdrawn or not approved for the channel (X3) | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-P7-003 | The decision log write failed (X6, legacy AC2) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller's role lacks the right of the operation (X7) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is missing or `channel` is outside LOV-CHANNEL | Enter {field}. |
| Not specified in the source documents (GAP-1131; ASM-2079) | No offer is in force, the offer validity has passed, an owner does not answer, or the case is under legal hold (X4, X5, X10) | The refusal answers 409 or 503 with the platform error envelope; the message ID and its text are left to the owner of the message list |

The six messages of the legacy table are copied unchanged, and all six are raised by this story: MSG-P6-003 by the channel and template check, MSG-P6-002 and MSG-P6-001 by the two checks of section 5, and MSG-GEN-001, MSG-P4-002 and MSG-P7-003 by validation, access and the decision record. The refusals of X4, X5 and X10 stand as placeholders until the message list is published, and no message text is invented here.

### 15. Screens and states

The legacy story names SCR-33 Template approval, and that screen shows a template and its approval states (Draft, approved, withdrawn); it cannot show an offer to a customer. FSD P6 A2.14.3.3 names the customer (borrower) as the primary actor and the case owner as an also-user, but the module's screen list gives this feature no screen identifier, so the screen field list, the layout and the masking belong to the edge and are Not specified in the source documents (GAP-1135; ASM-2083). The two channels are external: LINE through LINE OA and the web through HOME.SCB (FSD P6 A2.14.2), both reached through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), which calls the channel view and, once the customer has opened it, the view record.

| State of the offer and the notice | What the customer sees |
|---|---|
| The notice is `Sent`, the template is approved for the channel and the offer is in force | The offer rendered on the channel: the offer facts, the validity date and the merge values of the template |
| A contact stop is in force, or the channel has no consent | No offer, and the refusal of section 14 in the channel's own presentation |
| The template is withdrawn or not approved for the channel, or no offer is in force | No offer, and the refusal of section 14 |
| The notice is `Delivered` and the customer opens it again | The offer as it stands, and the view is recorded as a second view without a second event |
| The case is under legal hold | No offer, and the refusal of X10 |

The case owner's view of the same facts is the notice screen of RWB-P6-E5002-APP, which reads the notice with its `callback_date` and `delivery_status`; this story supplies the two columns that screen shows and no screen of its own.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-035-01 | AC1 | End to end | Notice `N-0401` of case `RC-2026-000401` in `Sent` with template `OFFER-LINE` version 3 approved for `LINE`; the contact fake returns a verified `LINE` contact point with consent `GIVEN` and no stop; the offer fake returns offer `TRT-2026-000401` in force; the view is recorded, the notice is `DELIVERED` with the view date as its callback date, one `NoticeDelivered` is written and the decision log holds the rule version |
| TC-E4-035-02 | AC2 | End to end | Decision log stubbed unavailable; nothing changes, no view row and no event, and MSG-P7-003 is shown |
| TC-E4-035-03 | Access | Component | A role without Litigation R sends the GET and a role without Litigation C sends the POST; both are refused with 403 and MSG-P4-002, and a notice outside the scope answers 404 |
| TC-E4-035-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 views; no view row is written, the notice is unchanged, no event enters the outbox and an incident is raised under R-UNI-39 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. The four cases keep their legacy IDs, their legacy order, their legacy covers and their legacy data. The legacy table carries no level column, so `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR, as the levels of the target table require. The journey that leaves the contract fakes and touches the real rwb-source-data and rwb-treatment contracts is not owned by a separate integration story of this key; the tests above run against the fakes of 12.8.

### 17. Guardrails

- No business value in code: the channel list, the decision code, the rule id and the refusal texts are data and reference data read with the version in force.
- No personal data in events, logs, prompts or tests: notice IDs, case IDs, offer IDs, view IDs, channel codes and dates only. No name, address, identity number, account number or contact point is written to `rwb_comms`, to the outbox or to a log, and the merge values are rendered at request time and stored nowhere.
- No read of another service's tables and no `v_ace_*` read of this service: the offer is S2's and the customer, contact point and consent are P1's, and both arrive only on the owners' contracts (DP-01, DP-05).
- No table of another owner is created or altered: a migration of this service that creates a treatment, case, deviation or ACE table fails the review.
- The decision record is written before the change, and a view that cannot be recorded does not proceed: the notice is unchanged, no view row and no event are written, and an incident is raised (R-UNI-39).
- A contact stop and a missing consent are refusals and never warnings: the offer is not shown and no view is recorded (VR-P6-014-1, VR-P6-014-2).
- Every outbound event is written to the outbox in the same transaction as the view and carries IDs, codes and dates only; at most one `NoticeDelivered` per notice (BR10).
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story of this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never shows an offer and never records a view (ADR-020).
- Every example is synthetic; no production payload, no production file and no production identifier is copied into a test or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-035 |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-035 ACn) |
| Legacy test cases | TC-E4-035-01 to TC-E4-035-04, all four in the legacy order |
| Legacy feature | FEAT-COM-01 View the offer on LINE and web (FSD P6 A2.14), prerequisite FEAT-OCC-04 Dispatch a LINE message through LINE OA |
| Legacy endpoints copied | The notice operations of the module, `POST /cases/{caseId}/notices` (API-P6-001, Litigation C) and `GET /notices/{noticeId}` (API-P6-002, Litigation R), which belong to RWB-P6-E1052-APP and RWB-P6-E5002-APP; this story provides neither and inherits their area and right |
| Legacy data rows | notice DF-LEG-015 to DF-LEG-023 and DF-LEG-030 to DF-LEG-034; template DF-REF-045 to DF-REF-051 and DF-REF-063 to DF-REF-069; merge_field DF-REF-252 to DF-REF-260; v_ace_customer DF-ACE-055 to DF-ACE-074; treatment DF-TRT-001 to DF-TRT-014; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 in force as a prohibition) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | VR-P6-014-1, VR-P6-014-2, BR-P6-014, R-UNI-20, R-UNI-39, R-RES-09, R-RES-19, R-LIT-05 |
| Requirements | REQ-OCC-011, the requirement TSD P6 T8 maps to FEAT-COM-01 and marks "written one epic ahead"; none of the other P6 requirements names this feature |
| Contract and tests | RWB-P6-E4035-CON and TC-P6-E4035-CON-01 to TC-P6-E4035-CON-06 |

The supporting facts of the legacy key — the customer and the contact point (P1 rwb-source-data, DP-05), the offer (S2 rwb-treatment), the case state and the legal hold (P3 rwb-case), the decision log entry (P7, DP-03) and the template approval (P6 template stories) — are answered here for the rwb-comms slice and by their owners for their own slices, and this story changes none of their designs.

### 19. Out of scope

- The offer, its plan, its validity and its approval: S2 rwb-treatment. This story reads the offer on its contract and writes none of it.
- The customer, the contact point of a channel and the consent state, and the contact repository itself: P1 rwb-source-data and the contact-repository story of this key, RWB-P6-E4039-APP. This story reads the contact point on the contract and holds no contact row.
- The contact stop, the deviation that raises it and the offer clock it holds: S8 rwb-deviation and R-RES-19, R-LIT-05. This story consumes the two deviation events and refuses on them.
- The case state, its closure and the legal hold: P3 rwb-case. This story consumes the case event and reads no case row.
- The template and merge-field catalogue, the approval of a template version and its withdrawal: RWB-P6-E1046-APP, RWB-P6-AD017-APP and RWB-P6-E1034-APP. This story reads them and writes no template row.
- The notice generation, the notice operations of the module and the returned WIN proof: RWB-P6-E1052-APP, RWB-P6-E1052-CON, RWB-P6-E5002-APP and RWB-P6-E2021-APP. The view record is not the proof-of-delivery operation of a returned letter.
- Dispatch of the notice, JOB-10, the WIN file, `NoticeDispatchWorkflow` and the first `NoticeDispatched` and `NoticeGenerated` rows: RWB-P6-E2021-APP, RWB-P6-E1055-APP and RWB-P6-E2022-APP.
- The channel screens on LINE OA and HOME.SCB, the composite route and the masking at the edge: RWB-PLT-N001-CON and the channel owners. This story supplies the two operations and no screen.
- The contract baseline, its two operations, its element set, its fakes and its tests: RWB-P6-E4035-CON.
- The decision code, the rule id and the message texts of a view, and the data product code of the contact point: the owners of the decision types, the message list and the data products. This story carries them as placeholders and does not invent them.
