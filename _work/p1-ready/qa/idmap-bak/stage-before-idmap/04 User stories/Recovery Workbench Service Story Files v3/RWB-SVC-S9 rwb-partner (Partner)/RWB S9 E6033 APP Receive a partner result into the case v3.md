# RWB-S9-E6033-APP Receive a partner result into the case

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: legacy RWB-E6-033 is split for the partner service. The end-to-end proof that a result reaches the case the same day (AC1) is RWB-ITG-E6033-ITG; the published contract is RWB-S9-E6033-CON. This story delivers the rwb-partner app slice: the result intake on `/api/recovery/partner/v1`, the instruction closed with its result code, the `PartnerResultSubmitted` fact for the case owner, the local decision record and the refusal path of legacy AC2. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (24 resolved, 14 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-S9-E6033-APP |
| Readiness decisions | RD-P1-004, RD-P1-007, RD-P1-064 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-partner |
| Service epic | RWB-SVC-S9 |
| Wave | 4 |
| Business epic | EP06 |
| Release | 30 April 2027 (tentative) |
| Legacy key | RWB-E6-033 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Open decisions | DL10 closed by the directive on confirmed assumptions ASM-2250, ASM-2357, ASM-2377, ASM-2863 |
| Parallel lane | L-S9-J |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-S9-E6033-APP-16) |
| Epic design sign-off | Not specified in the source documents (DOR-RWB-S9-E6033-APP-14) |
| Contract version | Not specified in the source documents (DOR-RWB-S9-E6033-APP-23); base path `/api/recovery/partner/v1` |
| Depends on (build) | RWB-S9-E6033-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S9 rwb-partner v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Version 3 changes**

- D-RCV-60 P1 developer readiness (RD-P1 register). Aligned the quoted English to Error and Message Standard v6. Added the partner-owned REST ledger append, its key and the matching EV-21 header. RD-P1-064.


### 1. Story

As a **case owner (RW-CASEOWN)**, I want **a contact, promise or cash result that a partner submits through the partner portal recorded on the instruction and published for the case the same day, and refused whole with MSG-P7-003 when its decision record cannot be written**, so that **partners are placed, paid and measured by rule and no case carries a partner result without the record that proves it**.

This is the app slice of legacy RWB-E6-033 (FEAT-PRM-05). It owns **AC2** word for word and adds four criteria that test only the rwb-partner build. **AC1** and TC-E6-033-01 are owned by `RWB-ITG-E6033-ITG`, which proves the arrival on the case; TC-E6-033-03 (Access) is owned by `RWB-S9-E6033-CON`.

It builds the intake `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results` (API-S9-005) and the read `GET /api/recovery/partner/v1/partner/instructions` (API-S9-003) on the service base (DP-13); the closure of `partner_instruction` in `rwb_partner` (`status` `DONE`, `result_code` set); the `PartnerResultSubmitted` fact (EV-21) on `rwb.partner.events.v1`, written to the outbox in the same transaction, keyed on the case ID; the local decision record through RWB-PLT-E1027-CON (DP-03) and the refusal of AC2; and the two screens through the gateway-bff composite route, read only (DP-19). The case row, the ledger, the documents and the panel are other owners' (section 19).

### 2. Business rationale

Partners are instructed and paid by email and spreadsheet, and allocation is not based on performance (FSD S9 A1.3). A result arrives as an attachment, is keyed in days later, and the fee and the scorecard are computed on what somebody remembered to type. **REQ-S9-004** (fees paid against recorded results) and **REQ-S9-008** (data exchanged through the portal, not email) name the target; FEAT-PRM-05 is the feature that turns a portal submission into a recorded result.

Architecture v5 moves the fact once, and that move is the story. The partner reaches the partner gateway (FAPI 2.0) that fronts S9 (slide 8), so the submission is a REST operation on the service base; the case lives in another service, so the result travels as a fact on `rwb.partner.events.v1` and never as a write into a case table. The one thing that must not travel is a change without its record: the instruction row, the local record and the outbox row are one `rwb_partner` transaction, and if the record cannot be written nothing happens and the partner sees MSG-P7-003 (DP-03; principle 5; BR-S9-005).

AC2 is therefore not a detail. A stored result with no record would let a fee be checked against a result no one can prove and would break the audit chain rwb-decision seals centrally. No business value is invented: the states, the instruction types, the data elements and the messages are those of TSD S9 T3.2, FSD S9 A2.5 and the legacy story.

### 3. Preconditions

- `RWB-S9-E6033-CON` is published: the two operations, the multipart result shape, the event envelope and the fakes. This story builds against them on Day 1; a CON dependency never blocks (§R5.4, §R5.7).
- `RWB-PLT-E1027-CON` (local decision-record library) and `RWB-PLT-N001-CON` (gateway-bff composite route) are published.
- `rwb_partner` and its login exist, and the service's own Flyway sequence is at the version that carries the library tables; this story adds its write key and its index on that sequence and never edits an applied migration.
- `partner_instruction` exists with the columns of TSD S9 T3.1 (DF-PRT-008 to DF-PRT-016) and the standard columns of T3.0; `partner` (DF-PRT-001 to DF-PRT-007) and `partner_user` (DF-REF-212 to DF-REF-217) carry the firm of the partner user.
- An instruction of type `COLLECT` sits with a firm in status `ACCEPTED`, issued by FEAT-PRM-03 and due on `due_at`; the result closes it.
- The partner user reaches the service through the partner gateway, holds Partner portal U, and the instruction belongs to the user's own firm (NFR-050; TSD S9 T6.1).
- LOV-INSTR-STATUS, LOV-INSTRUCTION and LOV-PANEL are versioned reference rows read at their version; the read is provided by the service template and the panel story, so it adds no row to this build list (ASM-5390).
- The decision code of the intake and the version in force are read as values at their version; which rule and version the record names is Not specified in the source documents (GAP-3114; ASM-5388).
- MSG-GEN-001, MSG-P4-002, MSG-P7-003 and MSG-P1-001 are unchanged from FSD S9 and the legacy story; no published message catalogue defines their entry format (GAP-3114; ASM-5388).
- No approval stop: FSD S9 is "In review", the story is Draft (realignment v1) (ASM-5389).

### 4. Flow

1. The partner user submits a contact, promise or cash result with its documents on `POST /api/recovery/partner/v1/partner/instructions/{instructionId}/results`, behind the partner gateway.
2. The guard library resolves the identity and the right; a role without Partner portal U is refused before any read (MSG-P4-002).
3. The service reads `partner_instruction`, `partner` and `partner_user` in `rwb_partner` and checks that the instruction belongs to the firm of the partner user.
4. It checks the status: a result is accepted only from `SENT`, `ACCEPTED` or `IN_PROGRESS`; `DONE`, `DECLINED` and `RECALLED` answer 409 and change nothing (X1).
5. It validates the submission — result present, document references of the documented type, body within the documented bound — and refuses with MSG-GEN-001 and the field (X2).
6. It resolves the decision code and the version in force on the submitted date and assembles the record.
7. In one `rwb_partner` transaction: `status` becomes `DONE`, `result_code` takes the reported value, the audit columns are set, the record is written through `DecisionRecordWriter.record`, and the outbox row is written (DP-03).
8. If the record write refuses, nothing at all is written and the answer is MSG-P7-003 (AC2, X3).
9. The service signals `InstructionWorkflow` with `resultSubmitted`; the workflow closes the stage and reports the outcome to the parent `CaseWorkflow` of rwb-case, which moves the case.
10. The relay publishes `rwb.partner.PartnerResultSubmitted.v1` on `rwb.partner.events.v1` keyed on the case ID, with the case ID as `ce_subject` and the payload `instructionId`, `result` and `documents` (GAP-3115); rwb-case applies the result and writes its own record (that journey is AC1 and is the ITG story's).
After the local result commits, rwb-partner appends the result through POST /api/recovery/source-data/v1/cases/{caseId}/interactions under its workload identity with eventCode PARTNER_RESULT, actorType PARTNER, actorRef the partner code, channel PORTAL and business key EV-21-<caseNo>-<yyyyMMdd>-<actionId>. Send a UUID Idempotency-Key and reuse it on an identical retry. The same business key is carried in ce_idempotencykey of PartnerResultSubmitted. The event serves its existing consumers. P1’s Kafka intake does not append this event (RD-P1-064 rule 9; ASM-5391).
11. The same `Idempotency-Key` returns the first answer and writes no second change and no second event (AC5).
12. SCR-34 and SCR-35 read the instruction and its result through the composite route, one hop each; the browser calls no owner service and no screen writes (DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The instruction is `DONE`, `DECLINED` or `RECALLED`, or belongs to another firm | 409 or 404; nothing written; the refusal is logged | Not specified in the source documents (GAP-3114; ASM-5388) | AC4 |
| X2 | A required element is missing or the body exceeds the documented bound | The whole submission is refused; no row and no event | MSG-GEN-001 | AC3 |
| X3 | The local decision record cannot be written | Nothing is written: no status, no result code, no event | MSG-P7-003 | AC2 |
| X4 | The same `Idempotency-Key` is submitted twice | The first answer returns, the repeat is counted, one change and one event exist | None | AC5 |
| X5 | A list or parameter read misses the 2 s budget, or its breaker is open | Nothing written; one retry with jitter | MSG-GEN-006 | AC8 |
| X6 | A data product is stale for the business date | The submission is refused and the staleness named | MSG-P1-001 | AC9 |
| X7 | A component or test reaches a case, rule, ledger or document table | The grant refuses and the boundary test fails the build | None (pipeline log) | AC10 |

X1 to X4 are this slice's paths; X5 to X7 are inherited platform rules. The legacy exception paths are AC2 here and the access case of the contract.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Starts on Day 1 with three CON H rows and no C row; the case consumer and the screen are fakes |
| Negotiable | Activity and consumer-group names, the multipart bound and the write key are this story's choice; the states, types, elements and messages are fixed |
| Valuable | A portal result becomes a recorded, provable result the same day, or nothing happens |
| Estimable | One operation, one read, one workflow signal, one migration, one library adapter, one screen fragment |
| Small | Fits two weeks with its tests, as the app slice of one legacy key |
| Testable | Each of the five criteria of section 7 is one automated test |

### 7. Acceptance criteria

```gherkin
Feature: Receive a partner result into the case — the rwb-partner intake

  Background:
    Given partner instruction of type "COLLECT" on a case in the partner user's firm, in status "ACCEPTED"
    Given the partner user holds Partner portal U and the instruction belongs to the user's own firm
    Given the lists LOV-INSTR-STATUS and LOV-INSTRUCTION are in force at their version

  Scenario: AC2 Not recorded (legacy RWB-E6-033 AC2)
    Given the decision record cannot be written
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003

  Scenario: AC3 The result is recorded on the instruction and published (new, D-RCV-60)
    Given the partner user submits a promise result with its documents on the instruction
    When the intake validates the submission and writes the transaction
    Then partner_instruction holds status "DONE" and result_code holds the value the partner reported
    Then exactly one local decision record is written in the same transaction, naming the decision code of the intake and the version in force
    Then exactly one PartnerResultSubmitted event is written to the outbox in that transaction, keyed on the case ID
    Then the event carries the instruction ID, the result and the document references, and no personal data
    Then rwb-partner appends one PARTNER_RESULT through the rwb-source-data REST contract and writes no case, interaction or document table directly

  Scenario: AC4 An instruction that is not open refuses the submission (new, D-RCV-60)
    Given the instruction is in status "DONE", "DECLINED" or "RECALLED"
    When the partner user submits a result on it
    Then the answer is 409 and no instruction column changes
    Then no decision record and no event is written
    Then an instruction of another firm answers 404 and the same nothing-changes rule holds

  Scenario: AC5 A repeated submission writes one result (new, D-RCV-60)
    Given the submission of AC3 is complete
    When the partner user submits the same result again with the same Idempotency-Key
    Then the first answer is returned and the repeat is counted
    Then partner_instruction still holds the same status and the same result code
    Then rwb.partner.events.v1 still holds one event for the instruction

  Scenario: AC6 The instruction and its result read on SCR-34 and SCR-35 (new, D-RCV-60)
    Given the gateway-bff composite route serves SCR-34 Partner list and SCR-35 Placement and allocation
    Given the instruction holds status "DONE" with its result
    When a partner user or a case owner holding Partner portal R opens SCR-35 for the case
    Then SCR-35 shows the instruction, its due date, its status and its result, read only
    Then SCR-34 lists the instructions of the firm with their status
    Then the browser calls no owner service directly and no screen writes anything

  Scenario: AC7 SCR-34 and SCR-35 show empty, loading, error and no-access states (new, D-RCV-60)
    Given the firm holds no partner instruction
    When a partner user opens SCR-34
    Then the SCR-34 empty state is Not specified in the source documents (CG-ALL-11870)
    Given a read for SCR-35 is in flight
    Then SCR-35 shows a loading state and no instruction
    Given the read for SCR-35 fails
    Then the SCR-35 error state is Not specified in the source documents (CG-ALL-11871)
    Given the user holds no Partner portal R
    When the user opens SCR-35
    Then the SCR-35 no-access state is Not specified in the source documents (CG-ALL-11871)

  Scenario: AC8 A list or parameter read that misses its budget changes nothing (new, D-RCV-60)
    Given a list or parameter read for the submission misses the 2 s budget or its breaker is open
    When the partner user submits a promise result
    Then the read retries once with jitter and nothing is written
    Then the user sees MSG-GEN-006

  Scenario: AC9 A stale data product refuses the submission (new, D-RCV-60)
    Given a data product is stale for the business date of the submission
    When the partner user submits a promise result
    Then the submission is refused, the user sees MSG-P1-001 naming the product and the date, and nothing is written

  Scenario: AC10 A component that reaches a table it does not own is refused (new, D-RCV-60)
    Given a component or test holds the rwb-partner grant
    When it reads or writes a case, rule, ledger or document table
    Then the grant refuses and the boundary test fails the build

  Scenario: AC11 A request without a valid credential or without Partner portal U is refused (new, D-RCV-60)
    Given a request to the rwb-partner operation carries no valid credential
    When the request is sent
    Then the answer is 401 and nothing is written
    Given the request carries a valid credential of a user without Partner portal U
    When the request is sent
    Then the answer is 403 and nothing is written

  Scenario: AC12 A retried or timed-out recordPartnerResult activity writes once (new, D-RCV-60)
    Given the recordPartnerResult activity is retried or times out
    When the workflow replays the activity
    Then the recorded outcome is reused and nothing is written twice
```

AC2 is legacy, word for word. AC3 to AC6 are new under D-RCV-60 and test only the rwb-partner deliverable. AC1 and TC-E6-033-01 belong to `RWB-ITG-E6033-ITG`; TC-E6-033-03 belongs to the contract. No legacy value is restated beyond the story's own lists, states and messages.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A submitted result closes the instruction: `status` becomes `DONE`, `result_code` holds the reported result, nothing else of the row changes | legacy RWB-E6-033; TSD S9 T3.1 |
| BR2 | A result is accepted only from `SENT`, `ACCEPTED` or `IN_PROGRESS`; `DONE`, `DECLINED` and `RECALLED` are terminal for the intake | TSD S9 T3.2; legacy AC2 |
| BR3 | Every intake writes one local decision record in the same transaction; a failed write changes nothing and answers MSG-P7-003 | FSD S9 BR-S9-005; principle 5; DP-03 |
| BR4 | The result reaches the case only as a fact on `rwb.partner.events.v1` keyed on the case ID, written to the outbox in the transaction | DP-01; Architecture v5 slides 12 and 42 |
| BR5 | The instruction belongs to the firm of the partner user; a foreign instruction answers 404 and discloses nothing | NFR-050; TSD S9 T6.1 |
| BR6 | A list or parameter read that fails inside the budget changes nothing and retries once with jitter | TSD S9 T7; ADR-020 |
| BR7 | A stale data product refuses the submission with MSG-P1-001, naming the product and the date | FSD S9 VR-S9-005-1 |
| BR8 | No value a business person may change is written in code: states, types, decision code and version are read at their version | FSD S9 BR-S9-005; principle 1 |
| BR9 | The same `Idempotency-Key` gives one change, one record and one event; the repeat is counted | TSD S9 T-A.2, API-S9-005; R-UNI-40 |
| BR10 | A result carries identifiers, codes, document references and dates only; no personal data reaches the row, the record, the event or the log | legacy guardrail; Architecture v5 slide 22 |

BR1 and BR2 are the state check and the one write of section 9; BR3 is `recordPartnerResult` and the rollback of X3; BR4 is the outbox element of 12.3; BR5 is the firm scope of step 3; BR6 and BR7 are the refusals of X5 and X6; BR8 is the read of the lists and of the version in force; BR9 is the idempotency element of the contract; BR10 is the payload rule of 12.3. The parameters read are Not specified in the source documents (DOR-RWB-S9-E6033-APP-20); the reference-data contract is DP-06 and DP-07.

### 9. State transitions

The case status is rwb-case's and is not moved here. The rows below are the instruction states of LOV-INSTR-STATUS.

| From | Event | Condition | To |
|---|---|---|---|
| `SENT` | Partner accepts | The accept operation of the same service | `ACCEPTED` |
| `SENT`, `ACCEPTED`, `IN_PROGRESS` | Result submitted | Submission valid and record written | `DONE`, `result_code` set |
| `DONE`, `DECLINED`, `RECALLED` | Result submitted | The instruction is closed | No change; 409 (X1) |
| Any open state | Result submitted, record fails | The record cannot be written | No change; MSG-P7-003 (X3) |
| Any open state | Partner declines | The accept operation | `DECLINED`; no result is taken |
| Any open state | Work recalled | The recall rule of the panel story | `RECALLED`; the intake is closed |

`DONE` and `result_code` are set in one statement, so no instruction is done without a result and none carries a result without being done. Acceptance, decline and recall belong to the panel and allocation stories; the contract declares their operations.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Partner portal users of the instructed firm: PT-AGENCY, PT-LAWFIRM, PT-VALUER, PT-AUCTION, PT-BUYER, PT-RAMC (RU) | Submit a result on their own firm's instruction; read their own instructions |
| RW-AGENCYMG, partner and agency manager (CRUDA) | Read the instruction and its result; submit on behalf of a firm through the portal |
| RW-CASEOWN, case owner (R) | Read the instruction and result on the case; writes nothing on the portal |
| RW-LITOFF, RW-ENFORCE, RW-SALEOFF, RW-NPAMGR, RW-DEBTSALE, RW-GUARANT (CRU) | Read and submit inside their capability area, as the legacy permission rows name them |
| RW-HEADLIT, RW-HEADNPA, RW-HEADASL (RA) | Read the instruction and the result; approve nothing here |
| RW-AUDIT, RW-COE (R) | Read the instruction, the result and the record it was taken under |
| SY-PARTNER, service identity (login `rwb_partner`) | Writes `partner_instruction`, the record and the outbox row in its own schema; no grant elsewhere |
| Role without Partner portal U | Refused with MSG-P4-002 before any read |

No delegation of authority level applies: recording a result decides nothing about the customer. Every operation of this story is guarded by the rwb-access authorise check before any read; the guard library resolves the identity and the right (flow step 2). No personal name, email address or credential appears in the story, a test or a log.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-PRT-008, DF-PRT-009, DF-PRT-010 | partner_instruction (S9, `rwb_partner`) | id, case_id, partner_id | Read, to resolve the instruction, its case and its firm |
| DF-PRT-011, DF-PRT-012, DF-PRT-013 | partner_instruction (S9) | instruction_type, instructed_at, due_at | Read, LOV-INSTRUCTION and the clock |
| DF-PRT-014 | partner_instruction (S9) | status | Write `DONE`; read for the state check |
| DF-PRT-015 | partner_instruction (S9) | result_code | Write, the reported result |
| DF-PRT-016 | partner_instruction (S9) | fee_amount | Not written: the fee is the work of FEAT-PRM-07 |
| DF-PRT-001, DF-PRT-002, DF-PRT-004, DF-PRT-005 | partner (S9, `rwb_partner`) | id, partner_code, partner_type, panel_status | Read, the firm and its panel status |
| DF-REF-212 to DF-REF-217 | partner_user (S9, `rwb_partner`) | identity_ref, partner_id, role_code, valid_from, valid_to | Read, the firm and role binding |
| DF-DEC-001 to DF-DEC-018 | decision_record (local, `rwb_partner`) | all fields, through `DecisionRecordWriter.record` | Write, in the same transaction (DP-03) |
| DF-CAS-001 to DF-CAS-023 | recovery_case (P3, `rwb_case`) | the case and its status | Not read and not written: the case ID travels as the event key |
| DF-INT-001 to DF-INT-013 | interaction (P1, rwb_source_data) | The result ledger entry | Appended via the P1 REST operation by rwb-partner (RD-P1-064; ASM-5391) |
| DF-REF-001 to DF-REF-015 | rule_row (P7, `rwb_decision`) | rule_id, rule_version | Not read as a table: the record names the code and the version in force as a value, taken from the parameters contract of rwb-case at its version (GAP-3114; ASM-5388) |
| Standard columns | partner_instruction (S9) | version, created_at, created_by, updated_at, updated_by | Write the audit columns as TSD S9 T3.0 defines them |
| processed_event, outbox_event, idempotency_key | PLT library, created in `rwb_partner` | the outbox row and the write key | Write through the library, in the transaction (DP-03) |

`partner_instruction` is the only business table written, and only `status`, `result_code` and the audit columns of it. No foreign key leaves `rwb_partner`: `case_id` is an identifier and the legacy `fk_partner_instruction_case_id` is dropped with the split. The Flyway version adds the write key that makes one result per instruction, plus the index the portal read uses, and no business column. No personal data is written. The partner result is rwb-partner's own row and event; DP06 to DP08 are P1's read-only data products built from the S9 events (GAP-2103). P1 owns the interaction row and the timeline read; the EV-20 and EV-21 payload element names and the seam with RWB-P2-E2034-CON are agreed at that contract's review (GAP-3149).

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-partner (S9); base `/api/recovery/partner/v1` (DP-13). The operations are those TSD S9 T-A.1 lists for this legacy key; `RWB-S9-E6033-CON` publishes their shape.

| Method | Path | Documented shape | Access | Idempotency |
|---|---|---|---|---|
| POST | `/partner/instructions/{instructionId}/results` (API-S9-005) | Multipart: result, files; `PartnerInstruction` out; errors 401, 403, 404, 409, 415, 422, 503 | Partner portal U, scope applied, guard library | `Idempotency-Key` header |
| GET | `/partner/instructions` (API-S9-003) | Query: status, page, size; `InstructionPage` out; errors 401, 403, 503 | Partner portal R, scope applied | Not applicable |

Both are reached only through the partner gateway (FAPI 2.0), and by staff only through the composite route (DP-19). Errors are RFC 9457 problem bodies; the 409 text is Not specified in the source documents (GAP-3114; ASM-5388).

#### 12.2 REST operations consumed

After the local result commits, rwb-partner appends the result through POST /api/recovery/source-data/v1/cases/{caseId}/interactions under its workload identity with eventCode PARTNER_RESULT, actorType PARTNER, actorRef the partner code, channel PORTAL and business key EV-21-<caseNo>-<yyyyMMdd>-<actionId>. Send a UUID Idempotency-Key and reuse it on an identical retry. The same business key is carried in ce_idempotencykey of PartnerResultSubmitted. The event serves its existing consumers. P1’s Kafka intake does not append this event (RD-P1-064 rule 9; ASM-5391).

None. The intake resolves everything from its own `rwb_partner` rows and publishes the result as a fact, so it calls no service on the path and spends no 2 s budget (DP-01). The lists and the version in force arrive through the client library of the service template (ASM-5390).

#### 12.3 Events published

| Event | Topic | Key | Payload carries | Purpose |
|---|---|---|---|---|
| `rwb.partner.PartnerResultSubmitted.v1` (EV-21) | `rwb.partner.events.v1` | `caseId` | instruction ID, the result (result code), the document references, the submitted time | Announces the result to rwb-case, which applies it, and to rwb-reporting; written to the outbox in the transaction |

| Envelope element | Value |
|---|---|
| Mode | CloudEvents 1.0, binary |
| ce_type | `rwb.partner.PartnerResultSubmitted.v1` |
| ce_source | rwb-partner |
| ce_subject and key | The case ID of the instruction |
| ce_id and traceparent | The event identifier and the W3C trace context of the call |
| ce_idempotencykey | EV-21-<caseNo>-<yyyyMMdd>-<actionId>, also the REST append business key |
| Payload | Identifiers, a result code and document references only; no personal data, no free text, no document content |

EV-21 is a consumed portal event in the monolith; in the target the portal ingress is the REST operation above and the same fact is published on the service topic, with the case ID added as key and subject (ASM-5389). The payload beyond instruction ID, result and documents is Not specified in the source documents (GAP-3115; ASM-5389). The retry and `.dlt` topics are the service template's and add no row here.

#### 12.4 Events consumed

None. A result arrives by the REST operation, not on a topic.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `InstructionWorkflow` | Workflow, one execution per instruction; the one workflow the S9 ownership row carries | `rwb-partner` | Signal `resultSubmitted` with the instruction ID and the result reference; closes the stage and reports to the parent `CaseWorkflow` of rwb-case |
| `recordPartnerResult` (name is this story's design choice) | Activity | `rwb-partner` | One `rwb_partner` transaction: the instruction columns, the record, the outbox row |

The REST call answers the partner synchronously, so the transaction runs in the request path through the same activity class, and the signal only closes the stage. The activity and signal names are fixed by no source (GAP-3114; ASM-5388); a replay reuses the recorded outcome and writes nothing twice. The workflow ID form and start rule are Not specified in the source documents (CG-ALL-11865; DOR-RWB-S9-E6033-APP-8).

#### 12.6 Schedules

None. The intake is started by a submission and the instruction clock is a durable timer of `InstructionWorkflow`, not a Schedule. The outbox relay is a library component in every service, not a Schedule of this one.

#### 12.7 Tables owned

| Table | Schema | Owner | This story |
|---|---|---|---|
| `partner_instruction` | `rwb_partner` | S9 | Writes `status`, `result_code` and the audit columns; the table arrives with the panel story and this story adds the write key and index |
| `partner` | `rwb_partner` | S9 | Read only, the firm and its panel status |
| `partner_user` | `rwb_partner` | S9 | Read only, the firm and role scope |
| `decision_record` | `rwb_partner` | PLT library applied here | Written through `DecisionRecordWriter.record`; the central `decision_log_entry` is P7's (DP-03) |
| `processed_event`, `outbox_event`, `idempotency_key` | `rwb_partner` | PLT library applied here | The outbox row and the write key |

Not owned and never read as a table: `recovery_case`, `task`, `timer` (P3), `decision_log_entry`, `rule_row`, `rule_package` (P7), `interaction` (P1) and the document tables (P5). No foreign key leaves the schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| `RWB-S9-E6033-CON` intake fake | Accepted submission with the instruction `DONE`; 409 for a closed instruction; 404 for a foreign firm; 422 for a missing element; a repeated key with the first answer | AC3, AC4, AC5 |
| `RWB-PLT-E1027-CON` writer fake | An accepted record with chain sequence and entry hash, and a refusal with MSG-P7-003 | AC2, AC3, AC5 |
| `PartnerResultSubmitted` fixture | One event per result keyed on the case ID, and the same submission twice under one key | AC3, AC5 |
| Composite route fake (`RWB-PLT-N001-CON`) | The merged SCR-34 and SCR-35 answer for the firm | AC6 |

The fakes are test-only and are replaced by the real services in SIT; a drift is a build failure of the story that owns the fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 0 consumed | The intake and the list on `/api/recovery/partner/v1`, behind the partner gateway for partners and the composite route for staff |
| Kafka | 1 published, 0 consumed | `rwb.partner.PartnerResultSubmitted.v1` keyed on the case ID; the record library's `DecisionRecorded` on `rwb.decision-record.v1` (DP-03) |
| Temporal | 1 workflow, 1 activity | `InstructionWorkflow` on `rwb-partner` with `recordPartnerResult`; no Schedule |
| File | Documents in the multipart body | Storage, OCR and retention are rwb-document's and are not built here |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.partner`, module `result`; front end `src/modules/recovery/partner/InstructionResult.tsx`, the fragment SCR-35 embeds, read only.

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/partner/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-03 is the transaction the story is built on: the record is a local row written with the change or not at all. DP-13 moves both operations to the service base, so the legacy partner resource `/partner/instructions/{instructionId}/results` on the monolith's one base becomes `/api/recovery/partner/v1/partner/instructions/{instructionId}/results`. DP-19 reaches SCR-34 and SCR-35 through the composite route, read only. The own-schema rule, the per-service Flyway sequence, the outbox and the list reads follow from the service template and the platform stories and add no row to this build list (ASM-5390, ASM-5392).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `PartnerResultController` | REST controller | The two operations, the multipart parse, the RFC 9457 mapping (BR1, BR2, BR9) |
| `PartnerResultService` | Service | Firm scope, state check, validation, version in force, record assembly (BR2, BR5, BR8) |
| `InstructionRepository` | Repository | Reads and writes `partner_instruction`, `partner`, `partner_user` in `rwb_partner` only |
| `DecisionRecordAdapter` | Library adapter | Calls `DecisionRecordWriter.record` with the decision code and the version (DP-03, BR3) |
| `ResultOutboxWriter` | Library adapter | Writes the outbox row in the transaction (BR4) |
| `InstructionWorkflow` (result branch) | Workflow | Receives `resultSubmitted`, closes the stage, reports to the parent |
| `recordPartnerResult` | Activity | The one transaction of step 7 and its rollback |
| `ResultGuard` | Service | Refuses a closed instruction, a foreign firm and a repeated key |
| `Migrations` | Migration | The write key and the index on the service's own sequence |

**Build steps.** (1) The Flyway version with the write key and index, against the TSD types. (2) The two operations behind the contract fake; test AC3 and AC6. (3) The firm scope and the state check; test AC4 and X1. (4) The record adapter and the rollback; test AC2 and X3. (5) The outbox row and the event fixture; test AC3 and AC5. (6) The workflow signal and the stage report against the case stub. (7) The boundary, stale-data and no-PII tests; test BR7, BR10 and X7. **Done when** the tests of section 16 pass, one submission closes its instruction once, one event per submission reaches the topic keyed on the case ID, a refused record leaves no trace, and both screens show the result through the composite route in SIT.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required element of the submission is empty (X2) | Enter {field}. |
| MSG-P4-002 | The identity has no right on the intake or the list (12.1) | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The record cannot be written and the result is not recorded (AC2, X3) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P1-001 | A data product is stale for the business date (X6) | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-006 | A list or parameter read misses the budget (X5) | {system} is not available. Try again in a few minutes. |
| None (GAP-3114) | The instruction is closed or belongs to another firm (X1) | RFC 9457 problem with a status and a detail; no message ID |

The four IDs and their texts are copied unchanged; this story adds no message. Status mapping: 403 MSG-P4-002, 404 and 409 for a closed or foreign instruction, 415 for a wrong body type, 422 for a refused element (415 and 422 are RFC 9457 problems with no message ID), 503 MSG-GEN-006. Thai text follows DL10.

### 15. Screens and states

| Screen | State | What the user sees or does |
|---|---|---|
| SCR-35 Placement and allocation | Loading | The composite route placeholder while the instruction read answers |
| SCR-35 Placement and allocation | Instruction open | The instruction, its type, its due date and status; the partner user submits a result |
| SCR-35 Placement and allocation | Result received | Status `DONE` and the reported result, read only |
| SCR-35 Placement and allocation | Submission refused | MSG-P7-003 or the 409 refusal, with nothing changed |
| SCR-35 Placement and allocation | Empty | Not specified in the source documents (CG-ALL-11871) |
| SCR-35 Placement and allocation | Error | Not specified in the source documents (CG-ALL-11871) |
| SCR-35 Placement and allocation | No access | Not specified in the source documents (CG-ALL-11871) |
| SCR-34 Partner list | Loading | The placeholder while the list answers |
| SCR-34 Partner list | List | The instructions of the firm with status and due date, read only |
| SCR-34 Partner list | Refused | A role without Partner portal R reads MSG-P4-002 and nothing changes |
| SCR-34 Partner list | Empty | Not specified in the source documents (CG-ALL-11870) |
| SCR-34 Partner list | Error | Not specified in the source documents (CG-ALL-11870) |
| SCR-34 Partner list | No access | Not specified in the source documents (CG-ALL-11870) |

Both screens are the legacy story's own and are served by the composite route, which composes the case read of rwb-case with the instruction read of this service, one hop each (DP-19). The route specification and the layout belong to the platform edge story; this story fixes the service side of the answer only.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E6-033-02 | AC2, BR3 | Component | The record mock refusing with MSG-P7-003; the instruction before and after |
| TC-E6-033-04 | AC2, BR3 | Component | A forced failure of the record write mid-transaction; no status, no event |
| TC-S9-E6033-APP-01 | AC3, BR1, BR4, BR10 | End to end | A promise result with two document references on an `ACCEPTED` `COLLECT` instruction; row, record and outbox asserted |
| TC-S9-E6033-APP-02 | AC4, BR2, BR5 | Component | An instruction in `DONE`, one in `RECALLED`, one of another firm |
| TC-S9-E6033-APP-03 | AC5, BR9 | Component | The same submission twice under one key, then a second key on the closed instruction |
| TC-S9-E6033-APP-04 | AC6, BR5 | Component | The composite-route fake merging SCR-34 and SCR-35 for one firm |
| TC-S9-E6033-APP-05 | AC7 | Component | The firm with no instruction, a read in flight, a failed read, and a user without Partner portal R; SCR-34 and SCR-35 asserted for each state |
| TC-S9-E6033-APP-06 | §12.3, §12.5 | Contract | The REST operation, the `resultSubmitted` signal and `recordPartnerResult` checked against the operations, events and activities of §12 |
| TC-S9-E6033-APP-07 | §12.7, AC10 | Component | A read and a write on each table not owned, and a foreign-key attempt; the boundary test fails the build |
| TC-S9-E6033-APP-08 | AC8, BR6 | Component | A list read forced past 2 s, then an open breaker; nothing written; one retry with jitter |
| TC-S9-E6033-APP-09 | AC9, BR7 | Component | A data product stale for the business date of the submission; MSG-P1-001 and no write |
| TC-S9-E6033-APP-10 | AC11 | Not specified in the source documents (NEWAC-RWB-S9-E6033-APP-AC11) | Not specified in the source documents (NEWAC-RWB-S9-E6033-APP-AC11) |
| TC-S9-E6033-APP-11 | AC12 | Component | recordPartnerResult retried and timed out after the transaction; the replay asserted to write nothing twice |

TC-E6-033-02 and TC-E6-033-04 keep their legacy identifiers because their scenarios are the record refusal this slice owns; the legacy Level "System" maps to Component here, because the case is stubbed and the assertion is inside the service. TC-E6-033-01 is executed by `RWB-ITG-E6033-ITG` and TC-E6-033-03 by `RWB-S9-E6033-CON`. The full test is in Recovery Workbench Test Cases, tab Story test cases, and the integration copies end in `-ITG`.

### 17. Guardrails

- No business value in code: states, types, panel states, the decision code and the version are read at their version; a build check fails on a list member in source or configuration (BR8).
- No personal data in the row, the record, the event, logs or spans: identifiers, codes and dates only; a document reference is a document ID, never a body (BR10).
- No read of another service's tables and no cross-schema join: `recovery_case` (P3), `decision_log_entry` and `rule_row` (P7), `interaction` (P1) and the document tables (P5) are reached only through their owners.
- The record is written in the same transaction as the change, and a failed write rolls the submission back with MSG-P7-003 (AC2, X3).
- One result per instruction and one event per key: the write key and the `Idempotency-Key` carry the rule (BR9, AC5).
- No ACE view and no ACE grant in this service.
- An applied migration is never edited: the write key and index are a new version.
- The portal is reached only through the partner gateway with multi-factor authentication, and a scope filter applies to every query (NFR-050).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-S9-004 | Fees are calculated from the contracted schedule and paid against recorded results — this story records the result the fee is checked against | Program, 5.16 | FEAT-PRM-05 | 12 Manage partners | BR-S9-005, BR1, BR3 | TC-E6-033-02, TC-S9-E6033-APP-01, TC-S9-E6033-APP-03 |
| REQ-S9-008 | Partners exchange data through the portal and the external gateway, not by email — this story takes the result on the portal operation | Program, 5.16 | FEAT-PRM-05 | 12 Manage partners | BR-S9-005, BR5, BR9 | TC-S9-E6033-APP-01, TC-S9-E6033-APP-02, TC-S9-E6033-APP-04 |

Both rows are the S9 rows of the Program section 5.16; FEAT-PRM-05 is the legacy feature and this story answers its system half. The legacy story carries no requirement identifiers, so none is invented.

| Story or item | Relation to this story |
|---|---|
| RWB-S9-E6033-CON | H: both operations, the multipart shape, the event envelope and the fakes; owns TC-E6-033-03 |
| RWB-ITG-E6033-ITG | Owns AC1 and TC-E6-033-01: the same-day arrival on the case across rwb-partner, rwb-case and the ledger |
| RWB-PLT-E1027-CON, RWB-PLT-N001-CON | H: the local decision-record library and the composite route |
| rwb-case (P3) | Consumes the event, applies the result, moves the status and raises its task |
| rwb-decision (P7) | Seals the local record in the central ledger; the rule rows are not read here |
| rwb-source-data (P1) | Owns the interaction ledger a contact result reaches (DP-18) |
| rwb-document (P5) | Stores the result documents; the files are handed over, not stored here |
| Other S9 stories | The panel, allocation, override, fee and scorecard; this story writes their instruction's result only |

### 19. Out of scope

- The contract — the OpenAPI, the event envelope, the vocabularies and the fakes: `RWB-S9-E6033-CON`.
- The end-to-end proof of the same-day arrival and the ledger entry that proves it: `RWB-ITG-E6033-ITG`.
- The application of the result to the case, the case status, the stage and the task: rwb-case (P3).
- The ledger entry, the chain check and the decision-log read: rwb-decision (P7).
- The interaction ledger row of a contact result: rwb-source-data (P1).
- The storage, OCR, retention and retrieval of the result documents: rwb-document (P5).
- The panel, fee schedule, allocation, override, fee match and scorecard: the other S9 stories of FEAT-PRM-01 to FEAT-PRM-15.
- The acceptance and decline (API-S9-004), the issuance (API-S9-002) and the invoice (API-S9-006): the panel and allocation stories.
- The partner gateway route and the SCR-34/SCR-35 field list and layout: the platform edge story and the screen owners.
- The physical schema files, the grants and the deployment of this build.
