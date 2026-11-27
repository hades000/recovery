# RWB-P6-E4039-APP Maintain the contact repository

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4039-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-039 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP13, DP19 |
| Parallel lane | L-P6-W |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4039-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-039 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E4039-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **compliance and PDPA officer (RW-COMPLY)**, I want **the verified contact points of a party read with their consent state per channel from the owner's contract, one contact point's consent and verification state maintained for one channel, and the change written to the decision record before it leaves this service**, so that **every notice and message leaves on a channel the customer has consented to, a withdrawn consent removes exactly that channel and leaves the statutory notices standing (R-UNI-10), and no contact change is ever made unrecorded**.

The legacy story names the compliance and PDPA officer as the actor, and the module specification of FEAT-COM-05 names the same role as primary with the case owner as also-user (FSD P6 A2.18.3.3). The legacy story's own endpoint table and screen table do not serve this feature: it lists the notice operations `POST /cases/{caseId}/notices` and `GET /notices/{noticeId}` and the template screen SCR-33 Template approval, and neither a notice operation nor a template screen maintains a consent state. Those two elements belong to other stories of this service, and the contact repository has no operation and no screen in any source (GAP-1120; ASM-2068).

### 2. Business rationale

Consent is the condition on which a recovery contact is lawful, and the legacy monolith kept the contact value, its consent state and its verification in the same `recovery` schema as the notice, so a withdrawn consent and a stopped contact could only be checked by reading tables the communications module neither owned nor governed. Architecture v5 gives ACE's customer, contact and account data to rwb-source-data (slide 41: the ACE view contract and the four extension tables; slide 17: P1 reads the `v_ace_*` views and writes `rwb_source_data`), and gives rwb-comms the notice, the templates, the merge fields and the proof of delivery. The Ownership Map carries `contact_point_ext` and `party_ext` under P1 `rwb_source_data`, and the FSD sentence that describes this feature — "Contact values are read from `v_ace_contact`; consent, verification and failed count are held in `recovery.contact_point_ext`, keyed by the composite contact key" (FSD P6 A2.18.2) — names rows that this service does not own in the target (GAP-1118; ASM-2066).

So the rework is a re-homing of the rows and not a change of the feature owner. FEAT-COM-05 stays with P6 (FSD P6 A2.18, prerequisite FEAT-RDF-04), the contact value, the consent state, the verification and the failed count arrive on the rwb-source-data contract (DP-05), and rwb-comms keeps the decision record of every change and the contact-stop facts it consumes from the deviation events. This story is the repository's app slice, and it declares no contact table and no `v_ace_*` query of its own: DP-01 is in force here as a prohibition, and DP-05 is its route (Template and Rules §R5.5).

The story owns both legacy criteria, AC1 (maintain the repository) and AC2 (not recorded when the decision log cannot be written), because both are satisfied inside this service once the contact rows are taken from the owner. It gives the FSD P6 measure "notices with proof of delivery, 100 percent, measured on the decision log and the Workbench records, reviewed monthly" its service-side evidence for the consent half, and it carries the requirements that name a consent state per channel and a verified contact point (REQ-OCC-006, REQ-OCC-010, NFR-044). The decoupling is the one the target fixes: the consent and verification state is P1's and arrives one hop from its contract (DP-05); the decision record goes through the local library and the shared topic (DP-03); the base is `/api/recovery/comms/v1` (DP-13); and the screen reaches the answer through the gateway-bff composite route (DP-19).

### 3. Preconditions

- RWB-P6-E4039-CON is published: the two contact operations under `/api/recovery/comms/v1`, the `ContactPoint` element set with its placeholders, the decision-record element, the two consumed rows, the two consumed events, the fakes and the drift test, so this story builds against a fixed contract on Day 1.
- The contact points, the consent state, the verification date and the failed count are P1 rwb-source-data's rows: `v_ace_contact` (DF-ACE-075 to DF-ACE-083), `v_ace_customer` (DF-ACE-055 to DF-ACE-074), `contact_point_ext` (DF-EXT-013 to DF-EXT-026) and `party_ext` are in `rwb_source_data` per the Ownership Map, and this service reads none of them and holds no grant on that schema (GAP-1118; ASM-2066).
- The rwb-source-data contract answers the contact read and the consent write of one contact point and its answers are available as fakes from the first run. No source names a published operation of that contract for either of them (GAP-1119; ASM-2067).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract (DP-03), so the record is written before the change and relayed by the platform outbox relay.
- The two deviation events of the contact stop are consumed inside this service with the inbox dedupe, so the stop a case is under is known when the repository is read (Architecture v5 slide 17: "events DeviationRaised / Cleared (contact stop)").
- The consent states, the verification rule and the failed-count threshold are data and reference data read with the version in force; none of the three value sets is given by any source read here (GAP-1121; ASM-2069).
- The channel vocabulary is LOV-CHANNEL of TSD P6 T3.2 (`MOBILE, HOME_PHONE, WORK_PHONE, LINE, EMAIL, POSTAL_ADDRESS, CALL, VISIT, SMS, LETTER, PORTAL, BRANCH`); this service passes the code through and the owner validates it on its own list.
- The screen path is the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), so no screen of this story calls the service directly.
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are the contract baseline of this key and two platform CON stories, and the C, I and X rows are empty (Template and Rules §R5.4, §R5.7).

### 4. Flow

1. A compliance and PDPA officer or a case owner opens the contact repository of a party and sends `GET /api/recovery/comms/v1/parties/{partyId}/contact-points`, with the case reference of the case in whose context the screen was opened.
2. The service checks the role, the Documents read right and the scope; a role without the right answers 403 with MSG-P4-002, and a party outside the caller's scope answers 404, neither of them reading anything.
3. The service calls the contact read of the rwb-source-data contract, one hop with a 2 s budget, and receives the contact points of the party with the consent state, the consent date, the verification date and the failed count of each channel (DP-05).
4. The service marks each contact point of the case the caller named with the contact stop in force from the local projection of the two deviation events, and answers 200 with the `ContactPoint` list as the contract fixes it.
5. A compliance and PDPA officer selects one contact point and one channel and sends `PUT /api/recovery/comms/v1/contact-points/{contactKey}` with `If-Match` holding the version the read returned, the channel code and the consent and verification values.
6. The service validates the request against the reference data in force: the channel is one of LOV-CHANNEL, the consent state is one of the consent codes, and a verification carries a source and a date. A missing or unknown value answers 422 with MSG-GEN-001 and changes nothing.
7. A version that no longer matches the contact point answers 409 and changes nothing; the caller re-reads and decides again.
8. The service writes the decision record through the local decision-record library before anything leaves the service: decision code, rule id, rule version, party reference, contact key, channel, the consent state written, the failed count and the decided-at (DP-03).
9. The record written, the service sends the consent and verification write of that contact point to the rwb-source-data contract, one hop with a 2 s budget. The owner records the change and answers the stored state with its new version.
10. The service answers 200 with the stored `ContactPoint` and the new version; the outbox relay publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08). A repeat of the PUT with the same `If-Match` returns the first answer and records no second change.
11. A decision record that cannot be written stops the flow at step 8: the owner is not called, the contact point is unchanged, the answer is 503 with MSG-P7-003 and an incident is raised under R-UNI-39.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The party is absent, or outside the caller's scope | 404; nothing is read and nothing changes | None | TC-E4-039-03 |
| X2 | The role lacks the Documents right | 403; nothing is read and nothing changes | MSG-P4-002 | TC-E4-039-03 |
| X3 | The owner does not return the party's contact points | 404; the answer carries no contact point | Not specified in the source documents (GAP-1119; ASM-2067) | AC1 |
| X4 | A required field is missing, or the channel is not in LOV-CHANNEL | 422; nothing is sent to the owner | MSG-GEN-001 | AC1 |
| X5 | The `If-Match` version is stale | 409; nothing is sent to the owner and no record is written | Not specified in the source documents (GAP-1121; ASM-2069) | TC-E4-039-01 |
| X6 | The consent and verification write of the owner times out or answers 5xx | Nothing changes and the record of the attempt stays in the local chain; the answer is 503 | Not specified in the source documents (GAP-1119; ASM-2067) | AC2 |
| X7 | The decision record cannot be written | The owner is not called, nothing changes, the answer is 503 and an incident is raised | MSG-P7-003 | AC2 |
| X8 | A consent state or a channel code is not in the reference data in force | 422; the owner is not called | MSG-GEN-001 | TC-E4-039-04 |
| X9 | The PUT is repeated with the same `If-Match` | The first answer is returned with status 200 and no second change is recorded | None | TC-E4-039-01 |

X3, X5 and X6 are refusals this service raises itself, and their message texts are not given by the legacy story, the FSD P6 A2.18 or the TSD P6, so they carry the placeholder of section 14. X5 rests on the version element of RWB-P6-E4039-CON; the owner's version of the contact point is its own, and this service only refuses a change it cannot justify. X6 leaves the decision record of the attempt in the local chain, because R-UNI-39 admits no unlogged action, and the owner's row is unchanged.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4039-CON, the decision-record library and the edge route. The contact rows, the consent state and the contact stop are contract fakes from the first run |
| Negotiable | The consent state set, the verification rule and the failed-count threshold are data and reference data; the story fixes the order of the checks and the place of the decision record |
| Valuable | Every consent change carries a decision record and a channel answer that a dispatch story can trust, and a withdrawn channel never removes a statutory notice |
| Estimable | Two operations, one service, one owner adapter, one projection of two consumed events, one library write and the reference data; four legacy test cases plus the contract tests of the baseline |
| Small | Fits one sprint as the app slice of the legacy key, with one small projection table and no contact table of its own |
| Testable | Each criterion of section 7 runs as one automated test against the contract fakes; the whole path is proven without a second service being live |

### 7. Acceptance criteria

```gherkin
Feature: Maintain the contact repository — the rwb-comms slice

  Background:
    Given the consent states, the verification rule and the failed-count threshold are data read with the version in force
    Given party "PT-0101" has contact points on the rwb-source-data contract
    Given the contact stop in force is read from the two deviation events of this service

  Scenario: AC1 Maintain the contact repository (legacy RWB-E4-039 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-source-data contract mock returns the verified contact points of the party with their consent state per channel
    When the user acts on the screen
    Then keeps the verified contact points for every customer, with consent state per channel
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-039 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the two criteria of RWB-E4-039 copied line for line, with the origin tag on each scenario line and one `Given the rwb-source-data contract mock returns …` line added inside AC1 for the part of the criterion that names a fact of another owner: the contact points, their verified state and their consent state per channel are P1's rows, so the criterion can only run against that contract's fake. Every legacy line and every legacy value is kept, and no business value is added. The two criteria run against the fakes of 12.8 and answer on the contract of 12.1.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contact point, the consent state, the verification and the failed count are rwb-source-data's rows; this service declares no contact table, no consent column and no `v_ace_*` query, and holds no grant on `rwb_source_data` (DP-01) | Architecture v5 slides 17 and 41; Ownership Map (`contact_point_ext`, `party_ext` owned by P1); DP-01; DP-05 |
| BR2 | The contact rows are read and written through the rwb-source-data contract, one hop with a 2 s budget; a timeout or an error records nothing and never answers as recorded (DP-11 as the call shape of DP-05) | ADR-020; Architecture v5 slide 41 (P1 ACE view contract); DP-05 |
| BR3 | The decision record is written before the change, through the local decision-record library and the shared topic; a change whose record cannot be written does not proceed | R-UNI-39; DP-03; legacy AC2 |
| BR4 | A consent state per channel is held for every party, and a withdrawn consent removes that channel from the contact plan while the statutory notices continue | R-UNI-10; FSD P6 A2.18.1; REQ-OCC-006; NFR-044 |
| BR5 | A contact attempt while a contact stop is in force is refused with MSG-P6-001 and a message to a channel without consent with MSG-P6-002; both checks sit on the send path of the dispatch stories, and this service supplies the consent state and the stop they read | FSD P6 A2.18.3.1 (VR-P6-018-1, VR-P6-018-2); R-UNI-04; R-LIT-05; R-UNI-44 |
| BR6 | No value a business person may change is written in code: the consent states, the verification rule, the failed-count threshold and the channel vocabulary are data or reference data read with the version in force | FSD P6 A2.18.3.1 (BR-P6-018) |
| BR7 | A consent change never deletes a contact point and never changes a contact value: the value is ACE's, the consent is the party's state, and this service writes the state only | FSD P6 A2.18.2; Ownership Map (P1 owns `contact_point_ext` and the `v_ace_contact` rows) |
| BR8 | A new verified contact point clears a lost-contact deviation, as the requirement states; the clearing is the deviation owner's act and this service only makes the verified state visible | REQ-OCC-010; Architecture v5 slide 42 (event 07) |
| BR9 | A contact stop never removes a consent record and never adds one: the stop removes the channel from the contact plan (R-LIT-05) and the consent record is the party's own act | R-UNI-10; R-LIT-05 |
| BR10 | An element of this story carries an identifier, a code and a date only: no contact value, no masked contact value, no name and no identity number is written to `rwb_comms`, logged, published or sent to the owner | Template and Rules §R7.2 s17; TSD P6 T6.2 (masking) |
| BR11 | A stale version is refused, and the caller re-reads before deciding again; concurrent writes never overwrite a newer consent state | RWB-P6-E4039-CON 12.1; FSD P6 A2.18.3.1 |
| BR12 | One base and one topic: `/api/recovery/comms/v1` and `rwb.comms.events.v1`; this story declares no other service's path or topic as its own (DP-13) | DP-13; Template and Rules §R4 |
| BR13 | A consent change raises no business event of this service: the catalogue has none for a contact, and the only event of the change is `DecisionRecorded` on the shared `rwb.decision-record.v1` (DP-03) | Architecture v5 slide 42 (event 08); DP-03 |
| BR14 | The party, the case and the deviation are other services' facts: the party and the case come with the request and through the case references the events carry, and this service holds no case row and no party row | Architecture v5 slide 41; Ownership Map (`recovery_case`, `case_party` owned by P3) |

### 9. State transitions

The state this story moves is the consent and verification state of one contact point and one channel, held by P1 and written through its contract. The contact value, the channel and the contact point itself are unchanged:

| From | Event | Condition | To |
|---|---|---|---|
| The consent state of a channel (a code of the reference data) | A consent record is written | The channel is in LOV-CHANNEL, the version matches and the decision record is written | The new consent state, its date and the version of the owner's row; the record holds the change |
| A consent state | The consent is withdrawn | The party withdraws consent for that channel (R-UNI-10) | That channel leaves the contact plan; the statutory notices continue; the record holds the change |
| A verification state | A verification is recorded | A source and a date are given for the channel | The verified state and its date; the failed count is set as the owner stored it |
| A consent state | The change is refused on the version | `If-Match` no longer matches the owner's version | No change; 409; no owner call |
| A consent state | The decision record cannot be written | The library fails | No change; 503 with MSG-P7-003; incident under R-UNI-39 |
| A consent state | The owner does not answer | The contact write times out or answers 5xx | No change at the owner; the attempt stays in the local chain; 503 |

The contact stop is not this story's state: it is raised and lifted by the deviation and case rules (R-UNI-04 raises X1 and applies the stop, R-LIT-05 holds the notice, R-UNI-44 resumes contact on the permitted channels), and this service only projects the two deviation events to mark a channel in its answer.

| Projected stop state | Event | Condition | Effect on this story's answer |
|---|---|---|---|
| No stop | `DeviationCleared` or no event | The case has no stop in force | Every contact point is answered with its own consent state and no stop mark |
| Stop in force | `DeviationRaised` | The event names a case and a reason code | Every contact point of that case is marked as stopped, and the reason code is answered as the event carried it |
| Stop lifted | `DeviationCleared` | The stop of that case is lifted | The mark is removed; the consent states are answered unchanged |

Whether a consent change may be recorded while a stop is in force is not given by any source, so the story applies R-UNI-10 and R-LIT-05 as written: the stop removes the channel from the plan and the consent record is the party's own act (BR9). The projection's shape is Not specified in the source documents (GAP-1123; ASM-2071).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COMPLY, compliance and PDPA officer | Documents RU in TSD P6 T6.1: reads the repository and maintains the consent and verification state of a channel (rights R and U); the primary actor of FEAT-COM-05 |
| RW-CASEOWN, case owner | Documents CRU in TSD P6 T6.1: reads the repository of the parties of the cases owned and records the consent the party gave (rights R and U); the also-user of FEAT-COM-05 |
| RW-CONDUCT, conduct and QA officer | Documents R in TSD P6 T6.1: reads the repository and the stop mark of a case under review |
| RW-LEGAL, legal counsel | Documents CRUA in TSD P6 T6.1: reads the consent state of a party served with a notice |
| RW-TEAMMGR, team manager | Documents R in TSD P6 T6.1: reads the repository of the team's parties |
| RW-AUDIT, internal audit | Documents R in TSD P6 T6.1: reads the repository and the decision records of the consent changes |
| RW-DATASTEW, data steward and data product owner | Documents R in TSD P6 T6.1: reads the repository and the ACE data product freshness behind it |
| RW-PLATADM, platform administrator | Documents R in TSD P6 T6.1: reads the repository and operates the feature switch; no administrative write of a consent state |
| rwb-comms service identity | Reads its own `contact_stop` projection, writes the decision record and the outbox row, and calls the rwb-source-data contract and the decision-record library (DP-02) |
| Decision-record library identity | Writes the local decision record of the change and relays it on `rwb.decision-record.v1` (DP-03) |
| rwb-source-data service identity | Owns `contact_point_ext` and the ACE contact rows and is the only writer of the consent and verification state; this service never writes them (DP-01) |

The matrix of TSD P6 T6.1 is the only source of the letters above. The legacy story declares the Litigation rights C and R for the two notice operations it copied, and the primary role of this feature holds Litigation R only and never Litigation C, so the legacy right cannot serve the contact repository: the capability area and the right of the two contact operations are declared in RWB-P6-E4039-CON as Documents R and U with scope applied, and the legacy Litigation rights of the notice operations are unchanged and built by RWB-P6-E1052-APP (GAP-1122; ASM-2070). The authorise contract of rwb-access is not in this story's pattern set: the right is declared on the operation and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-075 to DF-ACE-083 | v_ace_contact, through the rwb-source-data contract | contact_key, contact_type, person_key, contact_value, contact_value_masked and the other fields of the row | Read through the contract, never a view and never a table |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext, through the rwb-source-data contract | contact_key, contact_type, consent_given, consent_at, verified_at, failed_count and the eight fields the legacy table does not name | Read and write through the contract, never a table |
| DF-ACE-055 to DF-ACE-074 | v_ace_customer, through the rwb-source-data contract | person_key and cif_no, for the party reference only | Read through the contract, never a view |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, rule version, model version, party reference, contact key, channel, the state written, decided at, hash chain | Write |
| DF-REF-001 to DF-REF-015 | rule_row, through the rwb-decision contract | rule_id, rule_version | Read through the contract, never a table |
| Not specified in the source documents (GAP-1123; ASM-2071) | the composite contact key of `contact_point_ext` | the definition and the physical form of the key | Read, for the path and the answer |
| Not specified in the source documents (GAP-1121; ASM-2069) | consent and verification, through the rwb-source-data contract | the consent state value set, the verification rule and the failed-count threshold | Read as reference data, never as a literal |
| Standard column | contact_stop (`rwb_comms`, P6) | case_ref, stop_flag, reason_code, last_event_id, received_at | Write when a deviation event arrives, then read |
| Standard column | processed_event, outbox_event (library objects in `rwb_comms`) | the inbox dedupe of the two deviation events, the outbox row of the decision record | Write |

The contact value, the masked contact value, the consent state, the verification and the failed count are P1's: `contact_point_ext`, `party_ext`, `account_ext`, `valuation_ext`, `interaction`, the `v_ace_customer` and `v_ace_contact` rows and the thirty `v_ace_*` views are in `rwb_source_data` or in ACE (Ownership Map; Architecture v5 slides 15 and 41). This service reads none of them, holds no grant on that schema, declares no foreign key across the boundary and stages no copy of a contact value (GAP-1118; ASM-2066). The composite contact key, the eight fields of `contact_point_ext` that the legacy table leaves unnamed and the physical type of the consent and verification elements are Not specified in the source documents (GAP-1123; ASM-2071); RWB-P6-E4039-CON fixes the names and the placeholders, and the owner's definition of its own table stays the owner's.

The migration of this story is one per-service Flyway step in `rwb_comms` (DP-15; RWB-PLT-E1044-CON is not in this story's build list, so the step follows the baseline sequence of RWB-P6-E1046-APP): it creates `contact_stop` with the case reference, the stop flag, the reason code, the identifier of the last event applied and the received time, nullable where the source is silent, with no default and no backfill, and the index `ix_contact_stop_case_ref` on `contact_stop (case_ref)` serves the read. No contact table, no consent column, no contact-value column and no `v_ace_*` view is created or named by the migration. No column of this service carries a name, an address, an identity number, an account number or a contact point. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E4039-CON; this story implements them and adds no path. Neither operation is in the endpoint inventory of the TSD (GAP-1120; ASM-2068).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/parties/{partyId}/contact-points` | Read the contact points of a party with the consent and verification state of each channel, and the stop mark of the case the caller names, 200 with the ContactPoint list | Documents, right R, scope applied | Not applicable |
| PUT | `/contact-points/{contactKey}` | Maintain the consent and verification state of one contact point and one channel, 200 with the stored ContactPoint and its new version | Documents, right U, scope applied | `If-Match` with the version of the contact point; a repeat with the same version returns the first answer |

Errors: 401 no session; 403 the role lacks the Documents right (MSG-P4-002); 404 the party is absent or out of scope, or the owner does not return it; 409 the `If-Match` version is stale; 422 a field fails validation or the channel or the consent state is not in the reference data in force (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003) or the owner did not answer. The `ContactPoint` answer carries `contactKey`, `partyId`, `contactType` (a LOV-CHANNEL code), `consentState`, `consentAt`, `verifiedAt`, `failedCount`, `blockedByStop`, `stopReasonCode` and `version`; the consent value set, the composite key and the physical types are the placeholders of section 11 (GAP-1121; ASM-2069; GAP-1123; ASM-2071).

Request: `ContactPointRequest` carries `contactType` (the channel, required), `consentState` (required), `consentAt` and `verifiedAt` (required with a verification), `failedCount` (optional, written by the owner's counting) and `version` (required in `If-Match`); no field carries a contact value, a name or an identity number.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | the contact-point read of the rwb-source-data contract (P1 rwb-source-data); the published path is Not specified in the source documents (GAP-1119; ASM-2067) | P1 rwb-source-data | Supplies the contact points of a party from the ACE contact rows and the consent, verification and failed count from `contact_point_ext`; faked |
| PUT | the consent and verification write of a contact point on the rwb-source-data contract; no operation of that contract is named for it in any source (GAP-1119; ASM-2067) | P1 rwb-source-data | Records the consent state, the consent date, the verification date and the failed count of one contact point and one channel, and answers the stored state with its version; faked |
| GET | the rule read of the rwb-decision contract (P7 rwb-decision) | P7 rwb-decision | Supplies the rule id and the rule version the decision record carries; faked. The rule of a consent change is Not specified in the source documents (GAP-1121; ASM-2069) |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. No row reads a table, no row reads a `v_ace_*` view, and no row is declared as provided by this service (DP-01; DP-05; Ownership Map). No C dependency row is declared, because the plan names no P1 or P7 contract story for this key (Template and Rules §R5.4).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision record reference, decision code, rule id, rule version, party reference, contact key, contact type, the consent state written, the decided-at |

The row is written to the outbox in the same transaction as the owner's answer and relayed with the CloudEvents 1.0 envelope by the platform outbox relay (DP-03); the local decision-record library of this service publishes it and this story declares no event of its own. A consent change raises no event on `rwb.comms.events.v1`: the three catalogue events of this service (EV-13, EV-14 and EV-15, which TSD P6 T5.3 names `NoticeGenerated`, `NoticeDispatched` and `NoticeDelivered`) are the notice and dispatch stories', and the catalogue of Architecture v5 slide 42 holds no contact event (BR13).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` | S8 rwb-deviation | Marks the case reference the event carries as under a contact stop in the local `contact_stop` projection, with the reason code, deduped through the inbox |
| `rwb.deviation.DeviationCleared.v1` (EV-07) | `rwb.deviation.events.v1` | S8 rwb-deviation | Lifts the stop of that case reference, so the read answer carries no stop mark, deduped through the inbox |

The two rows are the "events DeviationRaised / Cleared (contact stop)" of Architecture v5 slide 17 and are the only way the contact stop reaches this service. They carry IDs, codes and dates only and no personal data. They are not a decision input of a consent change on their own: the consent state is the party's and is written to the owner, and the stop only marks a channel in the answer. The shape of the local projection that answers them is Not specified in the source documents (GAP-1123; ASM-2071).

#### 12.5 Workflows and activities

None. The read and the maintenance are two synchronous operations of the request thread with one library write and one adapter call; there is no workflow, no activity, no durable timer and no child workflow. Nothing in this story is started by a Schedule and nothing is queued for a later run.

#### 12.6 Schedules

None. No job of the catalogue is created, changed or read: JOB-10 (WIN notices) and JOB-11 (outbox relay) belong to other stories and to the platform, and the ACE freshness check is P1's (Architecture v5 slide 41).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| contact_stop | P6 (rwb_comms) | The stop flag, the reason code and the last event applied, per case reference, derived from EV-06 and EV-07; no contact value, no consent state and no party row |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of a consent change (DP-03) |
| processed_event, outbox_event | PLT library, created in `rwb_comms` | The inbox dedupe of the two deviation events and the outbox row of the decision record |
| notice, template, merge_field | P6 (rwb_comms) | Owned by this service and not read or written by this story: the notice, template and merge-field stories own them |

Not owned and never read: `contact_point_ext`, `party_ext`, `account_ext`, `valuation_ext` and `interaction` (P1 rwb-source-data, in `rwb_source_data`), and the thirty `v_ace_*` views of the ACE view contract, among them `v_ace_customer` and `v_ace_contact`; `recovery_case`, `case_party`, `task`, `timer` and `queue` (P3 rwb-case); `decision_log_entry`, `rule_row`, `approval` and the rule package rows (P7 rwb-decision); `deviation` (S8 rwb-deviation); `lov_value`, `reference_row`, `reference_version` and `parameter_value` (P3 rwb-case); `document` and `document_custody` (P5 rwb-document); `outbound_item` and `interface_config` (P2 rwb-integration). No contact table, no consent table and no consent column is declared in `rwb_comms` (DP-01; GAP-1118; ASM-2066).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-source-data contact fake | The contact read and the consent write of the P1 contract | Party `PT-0101` with contact points on three channels, one of them withdrawn and one unverified; a party with no contact point; a party the owner does not return; a consent write answering the stored state and a new version; a write failing with 5xx; an answer delayed beyond 2 s |
| rwb-source-data version fake | The version element of the two operations | The version the read returned; a version the owner moved on before the write, for the 409 of X5 |
| rwb-deviation stop fake | The two consumed rows of 12.4 | No stop; a stop in force from X1 with its reason code; a stop lifted; a duplicated event for the inbox dedupe |
| rwb-decision rule fake | The rule read of 12.2 | A rule id and a rule version in force; an absent rule version |
| decision-record library stub | The local library and the shared topic | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-039-04 |

The fakes are derived from the published contracts of RWB-P6-E4039-CON, and the drift test of that story fails a build in which a fake and the document disagree. The contact fake carries the placeholders of the P1 side — the composite key, the consent value set, the verification rule and the failed-count threshold — until the P1 contract names them (GAP-1119; ASM-2067; GAP-1121; ASM-2069).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 3 consumed | The contact read and the consent write provided; the contact read, the consent write and the rule read consumed; one hop, 2 s each |
| Kafka | 1 declared as published by the library, 2 consumed | `DecisionRecorded` through the library on the shared topic; `DeviationRaised` and `DeviationCleared` consumed; no contact event either way |
| Temporal | None | The two operations are synchronous; no workflow, activity or Schedule |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `contact`, Java package `th.co.scb.ace.workbench.recovery.comms.contact`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this service takes the contract, and declares no view of its own | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is in force as a prohibition and is not a pattern of this key's list: the legacy feature holds `v_ace_contact`, `v_ace_customer` and `contact_point_ext` as its own data and the FSD describes the consent state as a `recovery.contact_point_ext` row, while the Ownership Map gives all four extension tables, `contact_point_ext` among them, and the ACE view contract to P1 rwb-source-data. This service therefore declares no contact table, no consent column and no `v_ace_*` query, and reads none (GAP-1118; ASM-2066). DP-09 is used only through the library's outbox, which DP-03 brings with RWB-PLT-E1027-CON, so no separate platform row is added to the metadata table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ContactPointController | Controller | The two operations with validation, the `If-Match` version and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| ContactPointService | Service | Reads the party, marks the stop, orders the decision record before the change, calls the owner and answers |
| ConsentRule | Service | The consent state set, the channel check against LOV-CHANNEL, the verification rule and the failed-count threshold, read as reference data with the version in force |
| SourceDataContactClient | Adapter | The contact read and the consent write of the rwb-source-data contract, one hop, 2 s, with a breaker |
| DeviationStopListener | Consumer | The two deviation events, the inbox dedupe and the write of the `contact_stop` projection |
| ContactStopReader | Service | The stop mark and the reason code of a case reference, for the read answer |
| DecisionRecordClient | Adapter | The local decision-record write before the change and its outbox row, through the library |
| FeatureSwitch | Configuration | `rwb.comms.contact-repository`, read as a parameter |

**Database and migrations**

- Reads and writes `contact_stop` and the local decision record, all in schema `rwb_comms` (DP-01); reads no other schema.
- Migration in this story: `V4039_1__contact_stop.sql` creates the projection of section 11 with the index `ix_contact_stop_case_ref`. No contact table, no consent column, no contact-value column and no foreign key to `rwb_source_data`, `rwb_case` or `rwb_deviation` is created.
- No row of `notice`, `template` or `merge_field` is read or written here.

**Configuration and reference data**

- `rwb.comms.contact.consent-states`, as data; its value set is Not specified in the source documents (GAP-1121; ASM-2069) and is set at the baseline review, never in code.
- `rwb.comms.contact.verification-rule` and `rwb.comms.contact.failed-count-threshold`, as data; both are Not specified in the source documents (GAP-1121; ASM-2069).
- The channel vocabulary is LOV-CHANNEL of TSD P6 T3.2, validated by the owner on its own list; this service checks presence and passes the code through.
- The 2 s budget and one retry of the GET are the platform settings of ADR-020.
- The feature switch `rwb.comms.contact-repository`, read as a parameter: off refuses both operations with 404 and records nothing.

**Build steps**

1. ContactPointController and ContactPointService over the two operations, the `If-Match` version and the problem mapping; tests for X1, X2 and X5.
2. SourceDataContactClient with the contact read, the consent write, the timeout and the failure branches behind the fake; tests for X3 and X6.
3. ConsentRule with the consent state set, the LOV-CHANNEL check, the verification rule and the failed-count threshold as reference data; tests for X4 and X8.
4. DecisionRecordClient and the fail-closed path: a failed write leaves the owner's row unchanged and answers MSG-P7-003 with the incident of R-UNI-39; test for AC2 and TC-E4-039-04.
5. DeviationStopListener and ContactStopReader over the two events, the inbox and the projection, with the stop mark in the read answer; tests for the duplicated event and the lifted stop.
6. The read answer with paging, the newest-first order and the stop mark, and the PUT answer with the owner's new version; test for AC1 on both sides.
7. The migration of `contact_stop`, the index and the absence test that fails a build which declares a contact table, a consent column or a `v_ace_*` query.
8. The feature switch, the parameter rows and the contract-fake run of the whole path before the rwb-source-data contract is live.

**Feature switch.** `rwb.comms.contact-repository`, read as a parameter; off refuses both operations and records nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4039-CON stay green, every accepted consent change has one decision record and one owner answer, a refused change has neither, and no schema of this service names `contact_point_ext`, `v_ace_contact`, a consent column or any contact value.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is missing, the channel is not in LOV-CHANNEL, or the consent state is not in the reference data in force | Enter {field}. |
| Not specified in the source documents (GAP-1121; ASM-2069) | The `If-Match` version is stale | The refusal answers 409 with the platform error envelope; the message ID and its text are left to the owner of the message list |
| Not specified in the source documents (GAP-1119; ASM-2067) | The owner does not return the party's contact points, or does not answer in time | The refusal answers 404 or 503 with the platform error envelope; the message ID and its text are left to the owner of the message list |

MSG-P7-003, MSG-P4-002 and MSG-GEN-001 are copied unchanged from the validation table of the legacy story. The other three messages of that table (MSG-P6-003, MSG-P6-002 and MSG-P6-001) belong to the template and to the send path of a notice and are not raised by this story: MSG-P6-003 is the template's, and MSG-P6-001 and MSG-P6-002 are the two checks VR-P6-018-1 and VR-P6-018-2 applied by the dispatch stories (RWB-P6-E2022-APP and RWB-P6-E5002-APP). The refusal messages of section 5 stand as placeholders until the message list is published, and no message text is invented here.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template and its approval states (Draft, approved, withdrawn); it cannot show a consent state, and no source of this module names a contact repository screen (FSD P6 screen list; GAP-1120; ASM-2068). The repository is therefore a surface the edge story serves: the compliance and PDPA officer opens the contact points of a party from the case in context, and the gateway-bff composite route of RWB-PLT-N001-CON (DP-19) calls this service once for the contact points and once for the consent write and merges the answers with the case it already holds. The route, the screen field list and the masking of a contact value in the screen belong to RWB-PLT-N001-CON and to the stories that own each screen; this service answers codes and dates only and never a contact value.

| State of the repository | What the reader sees |
|---|---|
| A party with consented channels | One row per channel with its consent state, its consent date, the verified state and the date, and the failed count as the owner holds it |
| A party with a withdrawn channel | The channel with its withdrawn state and no verified mark; the other channels unchanged; the statutory notices of the case continue (R-UNI-10) |
| A case under a contact stop | Every contact point of that case marked with the stop and the reason code the event carried; the consent records unchanged |
| A change refused | Nothing is added to the list, and the refusal message of section 14 is shown |
| A party with no contact point | An empty list, and the screen shows that the owner returned no contact point |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-039-01 | AC1 | End to end | Party `PT-0101` of case `RC-2026-000321` with three contact points on the rwb-source-data fake; one channel's consent written; the decision record written and the owner's new version answered |
| TC-E4-039-02 | AC2 | End to end | Decision log stubbed unavailable; the owner is not called, nothing changes and MSG-P7-003 is shown |
| TC-E4-039-03 | Access | Component | A role without the Documents right sends the GET and the PUT; refused with 403 and MSG-P4-002; a party outside the scope answers 404 |
| TC-E4-039-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 consent changes; no write is sent to the owner, no consent state changes and an incident is raised under R-UNI-39 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The four cases keep their legacy IDs, their legacy order, their legacy covers and their legacy data. The legacy table carries no level column, so `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR, as the levels of the target table require. The journey that leaves the contract fakes and touches the real rwb-source-data contract is not owned by a separate integration story of this key; the tests above run against the fakes of 12.8.

### 17. Guardrails

- No business value in code: the consent states, the verification rule, the failed-count threshold and the channel vocabulary are data rows and reference data read with the version in force (BR6).
- No personal data in events, logs, prompts or tests: party references, case references, contact keys, channel codes, consent codes and dates only. A contact value, a masked contact value, a name, an address and an identity number are never written to `rwb_comms`, never logged and never sent to the owner (BR10).
- No read of another service's tables and no `v_ace_*` read by this service: the contact point, the consent state, the verification and the failed count are P1's and arrive only on the owner's contract (DP-01, DP-05).
- No contact table is declared here: a migration of this service that creates a contact table, a consent column, a contact-value column or a query on `rwb_source_data` fails the review (DP-01).
- The decision record is written before the change, and a change that cannot be recorded does not proceed: the owner's row is unchanged, no call is made to the owner and an incident is raised (R-UNI-39).
- A consent change never deletes a contact point, never changes a contact value and never removes a statutory notice (BR4, BR7).
- Every outbound event is written to the outbox in the same transaction as the owner's answer and carries IDs and facts only (DP-03, DP-09).
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story of this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never records a consent change and never returns one as recorded (ADR-020).
- Every example is synthetic; no production payload, no production contact value, no production file and no production identifier is copied into a test or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-039 |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-039 ACn) |
| Legacy test cases | TC-E4-039-01 to TC-E4-039-04, all four in the legacy order |
| Legacy feature | FEAT-COM-05 Maintain the contact repository (FSD P6 A2.18), prerequisite FEAT-RDF-04 |
| Legacy data rows | v_ace_customer DF-ACE-055 to DF-ACE-074; v_ace_contact DF-ACE-075 to DF-ACE-083; contact_point_ext DF-EXT-013 to DF-EXT-026; notice DF-LEG-015 to DF-LEG-023; decision_log_entry DF-DEC-001 to DF-DEC-018; rule_row DF-REF-001 to DF-REF-015; template DF-REF-045 to DF-REF-051 |
| Decoupling patterns | DP03, DP05, DP13, DP19 (DP-01 in force as a prohibition) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-04, R-UNI-10, R-UNI-20, R-UNI-39, R-UNI-44, R-LIT-05; VR-P6-018-1, VR-P6-018-2 and BR-P6-018 of FSD P6 A2.18.3.1 |
| Requirements | REQ-OCC-006 (a withdrawn consent stops that channel and statutory notices continue), REQ-OCC-010 (a verified contact point clears a lost-contact deviation), NFR-044 (consent state per channel held and applied); the endpoint inventory holds no contact operation (GAP-1120; ASM-2068) |
| Contract and tests | RWB-P6-E4039-CON and TC-P6-E4039-CON-01 to TC-P6-E4039-CON-06 |

The supporting facts of the legacy key — the contact value and its consent state (P1 rwb-source-data, DP-05), the decision log entry (P7, DP-03), the contact stop (S8 rwb-deviation and P3 rwb-case) and the screen SCR-33 the legacy story names — are answered here for the rwb-comms slice and by their owners for their own slices, and this story changes none of their designs.

### 19. Out of scope

- The contact points, the contact values, the consent state, the verification and the failed count themselves: P1 rwb-source-data (`v_ace_contact`, `v_ace_customer`, `contact_point_ext`, `party_ext` in `rwb_source_data`, and the ACE view contract). This story consumes the two operations and builds none of them.
- The consent and contact-stop rules of a send: VR-P6-018-1 and VR-P6-018-2 are applied by the dispatch stories (RWB-P6-E2021-APP, RWB-P6-E2022-APP and RWB-P6-E5002-APP), which read this repository's answer.
- The deviation, its codes, its owners and its lifecycle: S8 rwb-deviation (R-UNI-04, R-LIT-05, R-UNI-44). This story projects two events and reads no deviation row.
- The party, the case, the case-to-party link and the case state: P3 rwb-case (`recovery_case`, `case_party`). This story holds no case row and no party row.
- The consent state set, the verification rule, the failed-count threshold and the channel list as curations: their owners and the reference data. This story carries them as data and reference-data reads and does not invent a value.
- The contract baseline, its two operations, its element set, its fakes and its tests: RWB-P6-E4039-CON.
- The right, the scope and the masking of a contact value at the edge: RWB-P4 stories and RWB-PLT-N001-CON; this story declares the right and applies the scope.
- The notice, the template, the merge field, the dispatch and the proof of delivery: RWB-P6-E1052-APP, RWB-P6-E1046-APP, RWB-P6-E2021-APP, RWB-P6-E5002-APP and their contract stories. The legacy screen SCR-33 Template approval belongs to the template stories.
- The decision code, the rule id and the message texts of a consent change: the owner of the decision types and the message list. This story carries them as placeholders and does not invent them.
