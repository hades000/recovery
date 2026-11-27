# RWB-P6-E4040-APP Record a custody movement of a document

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E4040-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 3 |
| Business epic | EP04 |
| Release | 28 February 2027 (tentative) |
| Legacy key | RWB-E4-040 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P6-X |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P6-E4040-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E4-040 for rwb-comms. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E4040-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **legal counsel (RW-LEGAL)**, I want **the movement of a physical original out of the bank and back recorded against the notice it serves, checked against the state of the notice, written to the decision record before the change, made against the document store of the document hub one hop away, and readable on the contract of rwb-comms with the movement that the hub holds**, so that **an original is never lost without a trace, and no movement is recorded that a legal hold or an unapproved state should have stopped**.

The legacy story names the legal counsel as the actor. The module specification lists the primary actor of FEAT-COM-06 as "None; runs unattended" and the legal counsel as an also-user (FSD P6 A2.19.3.3): the officer starts the movement and the checks of section 4 run unattended inside the service. The physical document and its custody rows are not this service's, and this story builds none of them.

### 2. Business rationale

An original that leaves the vault, the branch or the court and comes back is the evidence a litigation file rests on, and the legacy monolith kept that record in the same schema as the notice, so a missing original could only be found by reading a table nobody owned. Architecture v5 gives the document hub to P5 (slide 41: metadata, custody, OCR text and fields, signatures and retention) and gives P6 the notice, the templates, the merge fields and the proof of delivery (slide 17), so the target splits one legacy screen into two owners: rwb-document holds the physical document and every movement of it in `document_custody` (Ownership Map), and rwb-comms holds the notice that the original serves and the reference of the movement recorded against it. The legacy key is FSD P6 A2.19 / FEAT-COM-06, its prerequisite is FEAT-DCM-19 (the document hub as the system of record), and its integration point is the Workbench document hub.

This story is the rwb-comms app slice of legacy RWB-E4-040. It owns both legacy criteria, AC1 (record a custody movement) and AC2 (not recorded when the decision log cannot be written), because both are satisfied inside this service once the movement is taken from the owner's contract. The decoupling is the one the target fixes: the notice and its movement reference are `rwb_comms` rows and no custody table is declared here (DP-01); the decision record goes through the local library and the shared topic (DP-03); the base is `/api/recovery/comms/v1` (DP-13); and the screens reach the answer through the gateway-bff composite route (DP-19). It gives the FSD P6 measure "notices with proof of delivery, 100 percent" its service-side evidence for the originals path, and it serves no requirement of the P6 requirement list, because FEAT-COM-06 has none: the requirement, the operation and the field set are the gaps of section 18.

### 3. Preconditions

- RWB-P6-E4040-CON is published: the two custody operations under `/api/recovery/comms/v1`, the seven-field movement, the decision-record element, the one consumed event, the two fakes and the empty rows, so this story builds against a fixed contract on Day 1.
- The `notice` row exists in `rwb_comms` with `case_id`, `document_id` and the state of the notice: the baseline is the one RWB-P6-E1046-APP and RWB-P6-E1052-APP create, and the notice of an original always carries the `document_id` of that original (TSD P6 T3.1, DF-LEG-017).
- The decision-record library and the shared topic `rwb.decision-record.v1` are live with the RWB-PLT-E1027-CON contract (DP-03), so the decision record is written before the change and relayed by the platform outbox relay.
- The document hub answers the custody write and the document read of its own contract, and its answers are available as fakes from the first run. The operation is `POST /documents/{documentId}/custody` of the Ownership Map, owned by P5 rwb-document (TSD P5 T2 appendix T-A.1, API-P5-007); no P5 contract story is named in this story's Contract dependencies and no P5 CON story covers the operation yet (GAP-1156; ASM-2103).
- The document and its custody rows are P5's: `document`, `document_custody`, `document_field`, `document_type`, `document_checklist_item`, `case_document_check`, `document_hub_parameter`, `document_intake`, `document_text`, `signature_request`, `retention_rule` and `retention_action` are all in `rwb_document` (Ownership Map; Architecture v5 slides 16 and 41). This service reads no table of another service and no `v_ace_*` view, and it holds no grant on `rwb_document`.
- The notice states that allow a movement are read as a parameter (`rwb.comms.custody.eligible-states`), and whether a movement is allowed on a closed case or on a case under legal hold is Not specified in the source documents (GAP-1160; ASM-2107).
- The screen path is the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), so no screen of this story calls the service directly.
- No build dependency outside rwb-comms and the platform contracts: the H rows of the metadata table are the contract baseline of this key and two platform CON stories, and the C row is empty (Template and Rules §R5.7, §R5.4).

### 4. Flow

1. A legal counsel or a compliance and PDPA officer sends `POST /api/recovery/comms/v1/notices/{noticeId}/custody-movements` with an Idempotency-Key and the movement: `document_id`, `moved_at`, `from_location`, `to_location` and `held_by`.
2. The service reads the notice from `rwb_comms` and checks its state against the parameter `rwb.comms.custody.eligible-states`; a notice outside the parameter is refused with 409 and the movement is not attempted.
3. The service checks that the notice carries a `document_id`; a notice without one is refused with 422 and MSG-GEN-001 naming the document reference, because a movement without a document is not a movement.
4. The service confirms the document on the owner's contract, one hop with a 2 s budget: the document exists, its case is the case of the notice, and it is not disposed of. A document the owner does not return is refused with 404 and changes nothing.
5. The service writes the decision record through the local decision-record library before any change, with the decision code and the rule id of the movement, the notice, the document, the movement date, the from and to locations and the holder (DP-03).
6. The decision record written, the service calls the custody operation of the document hub, one hop with a 2 s budget, with the same five fields; the owner records the row in `document_custody` and answers the custody record with its identifier.
7. The service stores the identifier of the movement on the notice as its movement reference, in the same transaction as the decision record, and answers 201 with the movement as the contract fixes it; the outbox relay of the platform publishes `rwb.decision-record.DecisionRecorded.v1` (EV-08).
8. A reader with the Documents read right sends `GET /api/recovery/comms/v1/notices/{noticeId}/custody-movements`; the service answers 200 with the notice reference and the movements the owner's contract returns for the document of that notice, newest first, and reads no table of the document hub for them.
9. A repeat of the POST with the same Idempotency-Key returns the first answer with status 201 and records no second movement.
10. A notice outside the caller's scope answers 404 on both operations, and a role without the Documents right answers 403 with MSG-P4-002, neither of them changing anything.
11. A decision record that cannot be written stops the flow at step 5: the notice is unchanged, no movement is sent to the document hub, the answer is 503 with MSG-P7-003 and an incident is raised under R-UNI-39.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The notice is not in an eligible state | Refused with 409; no decision record and no movement | Not specified in the source documents (GAP-1157; ASM-2104) | AC1 |
| X2 | The notice carries no document reference | Refused with 422 | MSG-GEN-001 | AC1 |
| X3 | The document hub does not return the document of the notice | Refused with 404; nothing changes | Not specified in the source documents (GAP-1157; ASM-2104) | AC1 |
| X4 | The decision log cannot be written | Nothing changes, no movement is sent, the answer is 503 and an incident is raised | MSG-P7-003 | AC2 |
| X5 | The custody operation of the document hub times out or answers 5xx | Nothing changes and the movement is not recorded anywhere; the answer is 503 | Not specified in the source documents (GAP-1157; ASM-2104) | AC2 |
| X6 | The case is under legal hold | The movement is refused under R-UNI-20 and nothing changes | Not specified in the source documents (GAP-1160; ASM-2107) | AC1 |
| X7 | A role without the Documents right | Refused with 403; nothing changes | MSG-P4-002 | TC-E4-040-03 |
| X8 | The notice is outside the caller's scope | Refused with 404; nothing changes | None | TC-E4-040-03 |
| X9 | The POST is repeated with the same Idempotency-Key | The first answer is returned with status 201 and no second movement is recorded | None | AC1 |

X1, X3, X5 and X6 are refusals this service raises itself, and their message texts and the exact status of X6 are not given by the legacy story, the FSD P6 A2.19 or the TSD P6, so they carry the placeholder of section 14. X6 rests on R-UNI-20 ("a legal hold stops every outbound action and automated decision"); the document hub holds the document and its custody, and this service only refuses to start a movement it cannot justify.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P6-E4040-CON, the decision-record library and the edge route. The document hub, its custody operation and the case state are contract fakes from the first run |
| Negotiable | The eligible notice states, the location list and the holder vocabulary are parameters and reference data; the story fixes the order of the checks and the place of the decision record |
| Valuable | Every original that moves carries a decision record, a movement reference on the notice and a readable history, and a held or unapproved case records nothing |
| Estimable | Two endpoints, one service, one owner adapter, one library write and the parameter; four legacy test cases plus the contract tests of the baseline |
| Small | Fits one sprint as the app slice of the legacy key, with no table of its own beyond the notice reference |
| Testable | Each criterion of section 7 runs as one automated test against the contract fakes; the whole path is proven without a second service being live |

### 7. Acceptance criteria

```gherkin
Feature: Record a custody movement of a document — the rwb-comms slice

  Background:
    Given the eligible notice states are "APPROVED" and "SENT"
    Given notice "N-0101" for case "RC-2026-000321" is "Approved" with document "D-0101"
    Given case "RC-2026-000321" has no legal hold

  Scenario: AC1 Record a custody movement of a document (legacy RWB-E4-040 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-document contract mock returns document "D-0101" of case "RC-2026-000321" and the custody movement "CM-0101" for it
    When its trigger arrives
    Then tracks a physical document leaving and returning, so the original is never lost
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E4-040 AC2)
    Given the decision log cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the two criteria of RWB-E4-040 copied line for line, with the origin tag on each scenario line and one `Given the rwb-document contract mock returns …` line added inside AC1 for the part of the criterion that names a fact of another owner: the document and the movement are P5's, so the criterion can only run against the document hub's contract fake. Every legacy line and every legacy value is kept, and no business value is added. The two criteria run against the two fakes of 12.8 and answer on the contract of 12.1.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The physical document and every movement of it are rwb-document's rows; this service declares no custody table and reads none (DP-01) | Architecture v5 slide 41; Ownership Map (`document`, `document_custody` owned by P5); DP-01 |
| BR2 | A movement is recorded through the custody operation of the rwb-document contract, one hop with a 2 s budget; a timeout or an error records nothing and never answers as recorded (DP-11) | ADR-020; Ownership Map (API-P5-007); DP-11 |
| BR3 | The decision record is written before the change, through the local decision-record library and the shared topic; a movement whose record cannot be written does not proceed (DP-03) | R-UNI-39; DP-03; legacy AC2 |
| BR4 | A movement is accepted only when the notice is in an eligible state and carries the `document_id` of the original; the eligible states are parameters, not code | FSD P6 A2.19.3.1 (BR-P6-019); TSD P6 T3.1 (DF-LEG-017) |
| BR5 | A legal hold on the case stops the movement | R-UNI-20 |
| BR6 | No value a business person may change is written in code: the eligible states, the location list and the holder vocabulary are read as data and parameters with the version in force | FSD P6 A2.19.3.1 (BR-P6-019) |
| BR7 | The location values are the LOV-CUSTODY list the document hub holds, and their validation is the owner's on its own operation; this service checks presence and never keeps the value set in code | TSD P5 T3.1 and T3.2; Template and Rules §R7.2 s17 |
| BR8 | `held_by` carries an organisational role, a team or a location, never a person and never a personal identifier | Template and Rules §R7.2 s17; TSD P6 T6.2 (masking) |
| BR9 | The read answers from the owner's contract and from the notice reference; no table of the document hub and no `v_ace_*` view is named in a query of this service (DP-01) | Architecture v5 slides 16 and 41; DP-01 |
| BR10 | A repeated POST with the same Idempotency-Key returns the first answer and records no second movement (DP-09) | Architecture v5 slide 11; DP-09 |
| BR11 | One base and one topic: `/api/recovery/comms/v1` and `rwb.comms.events.v1`; this story declares no other service's path or topic as its own (DP-13, DP-14) | DP-13; DP-14; Template and Rules §R4 |
| BR12 | A custody movement raises no business event of this service: the catalogue has none for custody, and the only event of the check is `DecisionRecorded` on the shared `rwb.decision-record.v1` (DP-03) | Architecture v5 slide 42 (event 08); DP-03 |
| BR13 | A missing answer of an owner never records a movement or returns one as recorded (fail closed) | ADR-020; DP-11 |
| BR14 | The case state and the closure of a case are rwb-case's, and the hold is read from its facts; this service holds no case row and no timer | Architecture v5 slide 41; Ownership Map (`recovery_case`, `timer` owned by P3) |

### 9. State transitions

A custody movement moves no notice of this service. The notice state of section 5 of the baseline stays as it is, and the movement is a fact recorded against the notice and against the document of the document hub:

| From | Event | Condition | To |
|---|---|---|---|
| The notice state (unchanged) | A movement is accepted | The notice is in an eligible state, carries the document, and the legal hold check passes | The notice state is unchanged; a movement row exists in the document hub's `document_custody` (P5) and the notice holds its reference |
| The notice state (unchanged) | A movement is refused on state or document | The state is outside the parameter or the `document_id` is empty | No movement, no decision record, no change |
| The notice state (unchanged) | A movement is refused on a legal hold | R-UNI-20 applies to the case | No movement, no decision record, no change |
| The notice state (unchanged) | The decision record cannot be written | The library fails | No movement, no change, MSG-P7-003, incident under R-UNI-39 |

The rows of `document_custody` and their state are P5's: the document, its custody and its `retention_rule` and `retention_action` rows are the document hub's facts (Ownership Map; Architecture v5 slides 16 and 41), and the movement reference on the notice is the only state this story writes. Whether a closed case or a case under legal hold permits a movement, and which notice states are eligible, is Not specified in the source documents (GAP-1160; ASM-2107); the eligible states therefore arrive as a parameter and the closure question is answered by the consumed case fact of 12.4.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LEGAL, legal counsel | Documents CRUA in the matrix of TSD P6 T6.1: records a movement and reads the movements of a notice (rights C and R) |
| RW-LITOFF, litigation officer | Documents CRUA in TSD P6 T6.1: records and reads the movements of the notices of the litigation files (rights C and R) |
| RW-ENFORCE, enforcement owner | Documents CRU in TSD P6 T6.1: records a movement of an original taken for enforcement and reads it (rights C and R) |
| RW-CASEOWN, case owner | Documents CRU in TSD P6 T6.1: records a movement on the cases owned and reads them |
| RW-COMPLY, compliance and PDPA officer | Documents RU in TSD P6 T6.1: records a movement of an original held for a compliance request and reads the movements |
| RW-TEAMMGR, team manager | Documents R in TSD P6 T6.1: reads the movements of the team's notices |
| RW-AUDIT, internal audit | Documents R in TSD P6 T6.1: reads the movements and their decision records |
| RW-CONDUCT, conduct and QA officer | Documents R in TSD P6 T6.1: reads the movements of a notice under review |
| RW-PLATADM, platform administrator | Documents R in TSD P6 T6.1: reads the movements and operates the feature switch; no administrative write of a movement |
| rwb-comms service identity | Reads its own `notice` row, writes the movement reference and the outbox row, and calls the document hub and the decision-record library (DP-02) |
| Decision-record library identity | Writes the local decision record of the movement and relays it on `rwb.decision-record.v1` (DP-03) |

The matrix of TSD P6 T6.1 is the only source of the letters above. The legacy story names the Litigation right for the notice endpoints it copied; this story serves new custody operations, so their capability area and right are declared in RWB-P6-E4040-CON as Documents C and R with scope applied, and the legacy Litigation rights of the notice operations are unchanged and built by RWB-P6-E1052-APP (GAP-1157; ASM-2104). The authorise contract of rwb-access is not in this story's pattern set: the right is declared on the operation and enforced at gateway-bff, which asks rwb-access, so no P4 dependency is declared.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice (`rwb_comms`, P6) | id | Read |
| DF-LEG-016 | notice (`rwb_comms`, P6) | case_id | Read |
| DF-LEG-017 | notice (`rwb_comms`, P6) | document_id | Read |
| DF-LEG-018 | notice (`rwb_comms`, P6) | notice_type | Read |
| Standard column | notice (`rwb_comms`, P6) | state | Read |
| Not specified in the source documents (GAP-1158; ASM-2105) | notice (`rwb_comms`, P6) | the reference of the latest recorded movement | Write when the owner answers the movement, then read |
| DF-DOC-001 to DF-DOC-011 | document, through the rwb-document contract | id, case_id, document_type, storage_ref | Read through the contract, never a table |
| DF-DOC-018 to DF-DOC-024 | document_custody, through the rwb-document contract | id, document_id, moved_at, from_location, to_location, held_by and the seventh field | Write through the contract, never a table |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, rule version, case, notice, document, decided at, hash chain | Write |
| DF-REF-001 to DF-REF-015 | rule_row, through the rwb-decision contract | rule_id, rule_version | Read through the contract, never a table |
| DF-REF-045 to DF-REF-051 | template (`rwb_comms`, P6) | id, template_code, template_version, language | Read, for the notice reference only |
| Standard column | outbox_event, processed_event, idempotency_key (library objects in `rwb_comms`) | the outbox row of the decision record, the inbox dedupe, the POST key | Write |

The physical document, its movement and its due-back fact are the document hub's: `document`, `document_custody`, `document_text`, `document_field`, `document_type`, `document_checklist_item`, `document_hub_parameter`, `document_intake`, `signature_request`, `retention_rule` and `retention_action` are P5's rows in `rwb_document` (Ownership Map). This service reads none of them, holds no grant on that schema and declares no foreign key across the boundary. The seventh movement field, the type and the required flag of each movement field on this service's own answer, and the name of the notice-side reference column are Not specified in the source documents (GAP-1158; ASM-2105); RWB-P6-E4040-CON fixes the seven names and the column name, and the owner's definition of the table stays the owner's.

The migration of this story is one per-service Flyway step in `rwb_comms` (DP-15, RWB-PLT-E1044-CON is not in this story's build list, so the step follows the baseline sequence of RWB-P6-E1046-APP): it adds the notice-side movement reference column, nullable, with no default and no backfill. The index `ix_notice_case_id` on `notice (case_id)` serves the read of the movements of a case, and the movement rows themselves are indexed by their owner. No column of this service carries a name, an address, an identity number, an account number or a contact point: `held_by` is an organisational role, a team or a location. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-comms (P6); base `/api/recovery/comms/v1`. The shapes are those fixed in RWB-P6-E4040-CON; this story implements them and adds no path. Neither operation is in the endpoint inventory of the TSD (GAP-1157; ASM-2104).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/notices/{noticeId}/custody-movements` | Record one movement of the original of a notice and return it, 201 with the Movement | Documents, right C, scope applied | Idempotency-Key header, kept 24 hours |
| GET | `/notices/{noticeId}/custody-movements` | List the movements of the original of a notice, newest first, 200 with the Movement list | Documents, right R, scope applied | Not applicable |

Errors: 401 no session; 403 the role lacks the Documents right (MSG-P4-002); 404 the notice is absent or out of scope, or the document hub does not return the document; 409 the notice is not in an eligible state; 422 a field fails validation (MSG-GEN-001); 503 the decision was not recorded (MSG-P7-003) or the document hub did not answer. The Movement body of the POST answer carries `id`, `noticeId`, `documentId`, `movedAt`, `fromLocation`, `toLocation` and `heldBy`, and the seventh field of the owner's table with the placeholder (GAP-1158; ASM-2105).

Request: CustodyMovementRequest with `document_id` required and equal to the `document_id` of the notice, `moved_at` required, `from_location` and `to_location` required, `held_by` required; no field is a name and none is free text of a person.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| POST | `/documents/{documentId}/custody` of the rwb-document contract (API-P5-007) | P5 rwb-document | Records the movement of the original and answers its custody record; faked. No P5 contract story is named in this story's Contract dependencies (GAP-1156; ASM-2103) |
| GET | the document read of the rwb-document contract | P5 rwb-document | Confirms the document exists, that its case is the case of the notice and that it is not disposed of; faked; same gap |

Every row is one hop with a 2 s timeout, a GET retried once with jitter and a breaker per downstream. No row reads a table, no row reads a `v_ace_*` view, and no row is declared as provided by this service (DP-01; Ownership Map).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision record reference, decision code, rule id, rule version, notice id, document id, moved at, from location, to location, decided at |

The row is written to the outbox in the same transaction as the movement reference and relayed with the CloudEvents 1.0 envelope by the platform outbox relay (DP-03, DP-09); the local decision-record library of this service publishes it and this story declares no event of its own. No custody event exists in the catalogue of Architecture v5 slide 42 and none is declared here (BR12).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | Takes note that a case closes or moves, so a movement on a closed case is refused; deduped through the inbox. The shape of the local projection that answers it is Not specified in the source documents (GAP-1160; ASM-2107) |

The event is not a decision input on its own: the state of the notice and the answers of the document hub are read at the moment the movement is recorded, and the event only keeps the local picture of closure current between calls. It carries IDs, codes and dates only and no personal data.

#### 12.5 Workflows and activities

None. The movement is one synchronous operation of the request thread with one library write and one adapter call; there is no workflow, no activity, no durable timer and no child workflow. Nothing in this story is started by a Schedule and nothing is queued for a later run.

#### 12.6 Schedules

None. No job of the catalogue is created, changed or read: JOB-10 (WIN notices) and JOB-11 (outbox relay) belong to other stories and to the platform, and JOB-17 (retention) is rwb-document's (Architecture v5 slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| notice | P6 (rwb_comms) | The notice of the original, its `document_id`, its state and the reference of the latest recorded movement; written here for the reference only |
| template | P6 (rwb_comms) | Read for the notice reference; written by RWB-P6-E1046-APP and the template stories |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The decision entry of a recorded movement (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox row of the decision record, the inbox dedupe of the consumed event and the POST key |

Not owned and never read: `document`, `document_custody`, `document_text`, `document_intake`, `document_field`, `document_type`, `document_checklist_item`, `document_hub_parameter`, `signature_request`, `retention_rule`, `retention_action` and `case_document_check` (P5 rwb-document, in `rwb_document`); `recovery_case`, `task`, `timer`, `queue` and `assignment` (P3 rwb-case); `decision_log_entry`, `rule_row` and the rule package tables (P7 rwb-decision); `interaction` (P1 rwb-source-data); `outbound_item` and `interface_config` (P2 rwb-integration). No custody table is declared in `rwb_comms` (DP-01), and `merge_field` is not read by this story.

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-document custody fake | The document read and the custody write of the P5 contract | Document `D-0101` of case `RC-2026-000321` present and clean; the custody write answering movement `CM-0101`; a document the owner does not return; a disposed document; a delayed answer beyond 2 s; a custody write failing with 5xx |
| rwb-case state fake | The consumed `CaseStateChanged` row | Case `RC-2026-000321` open; the same case closed; a legal hold true; a duplicated event for the inbox dedupe |
| decision-record library stub | The local library and the shared topic | A healthy chain and outbox; a stopped chain for AC2 and TC-E4-040-04 |

The fakes are derived from the published contracts of RWB-P6-E4040-CON, and the drift test of that story fails a build in which a fake and the document disagree. The custody fake carries the placeholder of the P5 side until the P5 contract names the seventh field (GAP-1158; ASM-2105).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 2 consumed | The movement record and the movement list provided; the document read and the custody write of the document hub consumed; one hop, 2 s |
| Kafka | 1 declared as published by the library, 1 consumed | `DecisionRecorded` through the library on the shared topic; `CaseStateChanged` consumed; no custody event either way |
| Temporal | None | The operation is synchronous; no workflow, activity or Schedule |
| File | None | No file is read or written by this story |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `custody`, Java package `th.co.scb.ace.workbench.recovery.comms.custody`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01 is in force as a prohibition and is not a pattern of this key's list: the legacy key's data table names `document` and `document_custody` as module P6 rows, and the target gives both to P5 rwb-document, so this service declares no such table and no row of it is read here (GAP-1156; ASM-2103). DP-09 is used only through the library's outbox, which DP-03 brings with RWB-PLT-E1027-CON, so no separate platform row is added to the metadata table.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CustodyMovementController | Controller | The two operations with validation, the Idempotency-Key and the problem mapping for 401, 403, 404, 409, 422 and 503 |
| CustodyMovementService | Service | Reads the notice, applies the eligible-state check, confirms the document, orders the decision record before the change, stores the reference and answers |
| DocumentCustodyClient | Adapter | The document read and the custody write of the rwb-document contract, one hop, 2 s, with a breaker |
| DecisionRecordClient | Adapter | The local decision-record write before the change and its outbox row, through the library |
| NoticeStateGuard | Service | The eligible-state parameter, the presence of `document_id` and the refusal paths of section 5 |
| MovementReferenceWriter | Service | Writes the movement reference on the notice in the same transaction as the decision record |

**Database and migrations**

- Reads and writes `notice` and the local decision record, all in schema `rwb_comms` (DP-01); reads no other schema.
- Migration in this story: `V4040_1__notice_custody_ref.sql` adds the notice-side movement reference column of section 11, nullable, and the index `ix_notice_case_id` where the baseline does not hold it yet. No custody table, no custody column and no foreign key to `rwb_document` is created.
- No row of `template` or `merge_field` is written here.

**Configuration and reference data**

- `rwb.comms.custody.eligible-states`, as data; its value is set at the baseline review and never in code.
- The location list is LOV-CUSTODY of the document hub, validated by the owner; the holder vocabulary is data and never a name.
- The 2 s budget and one retry of the GET are the platform settings of ADR-020.
- The feature switch `rwb.comms.custody-movements`, read as a parameter: off refuses both operations with 404 and records nothing.

**Build steps**

1. CustodyMovementController and CustodyMovementService over the two operations, the Idempotency-Key and the problem mapping; tests for the repeat and the two scope refusals.
2. NoticeStateGuard with the eligible-state parameter and the `document_id` presence; tests for X1 and X2.
3. DocumentCustodyClient with the document read, the custody write, the timeout and the failure branches behind the fake; tests for X3 and X5.
4. DecisionRecordClient and the fail-closed path: a failed write leaves the notice unchanged and answers MSG-P7-003 with the incident of R-UNI-39; test for AC2 and TC-E4-040-04.
5. MovementReferenceWriter and the transaction that holds the reference and the decision record together; test for AC1.
6. The read of the movements with the owner's answer, paging and the newest-first order; test for AC1 on the read side.
7. The feature switch, the parameter rows and the contract-fake run of the whole path before the document hub is live.

**Feature switch.** `rwb.comms.custody-movements`, read as a parameter; off refuses both operations and records nothing.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P6-E4040-CON stay green, every accepted movement has one decision record and one movement reference on its notice, a refused movement has neither, and no schema of this service names `document`, `document_custody` or any `retention_*` table.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Documents right | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is missing, including the document reference of the notice | Enter {field}. |
| Not specified in the source documents (GAP-1157; ASM-2104) | The notice is not in an eligible state, the document hub does not return the document, or the hub does not answer in time | The refusal answers 409, 404 or 503 with the platform error envelope; the message ID and its text are left to the owner of the message list |

MSG-P7-003, MSG-P4-002 and MSG-GEN-001 are copied unchanged from the validation table of the legacy story. The other three messages of that table (MSG-P6-003, MSG-P6-004 and MSG-P6-001) belong to the dispatch of a notice and to its template and are not raised by this story: RWB-P6-E2021-APP and the template stories raise them. The refusal messages of section 5 stand as placeholders until the message list is published, and no message text is invented here.

### 15. Screens and states

The legacy key names SCR-33 Template approval, and that screen shows a template and its approval states (Draft, approved, withdrawn); it cannot show a movement of a physical original, and this story therefore supplies no screen of its own. The movement is a fact of the document hub and is shown on SCR-32 Document custody, which is a screen of the P5 document hub (FSD P5) and is served through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19) from the answers of RWB-P6-E4040-CON and of the hub. The route, the screen field list and the masking of the holder field belong to RWB-PLT-N001-CON and to the stories that own each screen.

| State of the notice | What the reader sees of the movements |
|---|---|
| Any state with a movement recorded | The movements of the document of the notice, newest first, with the date, the from and to locations and the holder, and the reference the notice holds |
| Any state with no movement recorded | An empty list, and the notice shows that no movement is recorded |
| A movement refused | Nothing is added to the list, and the refusal message of section 14 is shown |

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E4-040-01 | AC1, BR1, BR2, BR3, BR4 | End to end | Notice `N-0101` of case `RC-2026-000321` in `APPROVED` with document `D-0101`; the document hub fake answers document `D-0101` and movement `CM-0101`; the movement is recorded and the notice holds `CM-0101` |
| TC-E4-040-02 | AC2, BR3 | End to end | Decision log stubbed unavailable; nothing changes and MSG-P7-003 is shown |
| TC-E4-040-03 | Access | Component | A role without the Documents right sends the POST and the GET; refused with 403 and MSG-P4-002; a notice outside the scope answers 404 |
| TC-E4-040-04 | Principle 5 | NFR | The decision log write is forced to fail on 10 movements; no movement is sent to the document hub, no reference is written and an incident is raised under R-UNI-39 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID. The four cases keep their legacy IDs, their legacy order, their legacy covers and their legacy data. The legacy table carries no level column, so `AC1` and `AC2` map to End to end, `Access` to Component and `Principle 5` to NFR, as the levels of the target table require. The journey that leaves the contract fakes and touches the real document hub is not owned by a separate integration story of this key; the tests above run against the fakes of 12.8.

### 17. Guardrails

- No business value in code: the eligible notice states, the location list and the holder vocabulary are data rows and parameters read with the version in force.
- No personal data in events, logs, prompts or tests: notice IDs, case IDs, document IDs, movement IDs, codes and dates only. `held_by` is an organisational role, a team or a location, and no name, address, identity number or account number is written to `rwb_comms` or sent to the document hub.
- No read of another service's tables and no `v_ace_*` read of this service: the document, its custody and its retention rows are P5's and arrive only on the owner's contract (DP-01).
- No custody table is declared here: a migration of this service that creates `document_custody`, `document` or a `retention_*` table fails the review (DP-01).
- The decision record is written before the change, and a movement that cannot be recorded does not proceed: the notice is unchanged, no call is made to the document hub and an incident is raised (R-UNI-39).
- Every outbound event is written to the outbox in the same transaction as the movement reference and carries IDs and facts only (DP-03, DP-09).
- One base, one topic and one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in namespace `rwb-recovery`; no story of this key declares another service's base or topic as its own (DP-13, DP-14).
- One hop and 2 s on every call; a timeout never records a movement and never returns one as recorded (ADR-020, DP-11).
- Every example is synthetic; no production payload, no production file and no production identifier is copied into a test or a fake.

### 18. Traceability

| Trace item | Value |
|---|---|
| Legacy key | RWB-E4-040, disposition Split (rework) |
| Legacy criteria owned here | AC1 and AC2, each tagged (legacy RWB-E4-040 ACn) |
| Legacy test cases | TC-E4-040-01 to TC-E4-040-04, all four in the legacy order |
| Legacy feature | FEAT-COM-06 Record a custody movement of a document (FSD P6 A2.19), prerequisite FEAT-DCM-19 of the P5 document hub |
| Decoupling patterns | DP03, DP13, DP19 (DP-01 in force as a prohibition) |
| Architecture decisions | ADR-013 (19 services inside ACE), ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway and migration ownership), ADR-022 (local decision record plus central ledger) |
| Rules | R-UNI-20, R-UNI-39 |
| Requirements | Not mapped: the P6 requirement list of the FSD "Requirements served" table holds no requirement for FEAT-COM-06, and the endpoint inventory holds no custody operation (GAP-1157; ASM-2104) |
| Contract and tests | RWB-P6-E4040-CON and TC-P6-E4040-CON-01 to TC-P6-E4040-CON-06 |

The supporting facts of the legacy key — the document and its custody (FEAT-DCM-19 of P5), the decision log entry (P7, DP-03) and the screen SCR-33 the legacy story names — are answered here for the rwb-comms slice and by their owners for their own slices, and this story changes none of their designs.

### 19. Out of scope

- The physical document, the custody rows and the custody operation themselves: P5 rwb-document (`document`, `document_custody` in `rwb_document`, API-P5-007 and the P5 stories that build the hub). This story consumes the operation and builds none of it.
- The retention classes and periods, `retention_rule`, `retention_action` and JOB-17: P5 rwb-document, with RWB-P6-E4042-APP and RWB-P6-E4042-CON on the notice side. This story reads no retention row.
- The answer to a legal or audit document request: RWB-P6-E4041-APP and RWB-P6-E4041-CON.
- The contract baseline, its two operations, its movement field set, its fakes and its tests: RWB-P6-E4040-CON.
- The legal hold, the closure of a case and the case state: P3 rwb-case. This story consumes the case fact and reads no case row.
- The right, the scope and the masking of the holder field at the edge: RWB-P4 stories and RWB-PLT-N001-CON; this story declares the right and applies the scope.
- The screens of the document hub and of the notice: FSD P5 SCR-32 and the screens RWB-PLT-N001-CON serves. The legacy screen SCR-33 Template approval belongs to the template stories and does not show a movement.
- The notice generation, the template catalogue, the dispatch and the proof of delivery: RWB-P6-E1052-APP, RWB-P6-E1046-APP, RWB-P6-E2021-APP, RWB-P6-E5002-APP and their contract stories.
- The decision code, the rule id and the message texts of a custody movement: the owner of the decision types and the message list. This story carries them as placeholders and does not invent them.
