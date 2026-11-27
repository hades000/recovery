# RWB-P6-E2014-APP Approval screen for D7.1 demand and recall notices

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E2014-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-014 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Parallel lane | L-P6-L |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E2014-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (FR-P6-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-014 for rwb-comms; the notice side of the D7.1 approval screen — the notice answer the screen reads, the template version and state it must show, and the approve, regenerate and hold moves the decision makes — reworked onto `rwb_comms`, the decision-record library and the gateway-bff composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E2014-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **litigation officer (RW-LITOFF)**, I want **the demand or recall notice held in rwb-comms to be readable with the template code, version and state that produced it, and to move to Approved, to a new version from another approved variant, or to Held, only when the D7.1 approval screen of rwb-decision says so**, so that **the 16:00 dispatch run takes only a notice a person approved, a withdrawn template can never be approved, and no notice ever moves without a record of the move**.

### 2. Business rationale

A demand fee notice sent to a customer incomplete is a Bank of Thailand finding, and a wrong amount or address on a notice can void the notice period and delay litigation. The legacy story kept the notice, its template version, the case, the ACE facts and the approval in one monolith transaction, so the screen could read all of them and the notice could be approved in the same call. In the target that transaction does not exist: rwb-decision owns the approval and the central decision ledger in `rwb_decision`, rwb-comms owns the notice, its template version and the template state in `rwb_comms`, rwb-case owns the case and its routing, rwb-source-data owns the ACE balance and contact facts, and gateway-bff composes the screen one hop per owner (Architecture v5 slides 14, 17, 20 and 41; TSD P6 v2 T1 and T5.2; P6 context pack).

This story is the rwb-comms slice of legacy RWB-E2-014. It owns the notice side of the decision and nothing else: the notice answer the SCR-18 Notice approval panel shows (notice, case, document, notice type, state, and the template code, version and state), the four operations on the notice that the decision drives — the read, the approve, the regenerate from another approved variant and the hold — and the record of each move. The approval screen itself, the routing, the preparer rule, the input-age check and the decision entry are RWB-P7-E2014-APP's, which owns the ten legacy criteria; this story carries no legacy criterion of its own and its criteria in section 7 are new, testing only the four operations and the two state rules.

The decoupling is the one the target fixes: the notice and the template are `rwb_comms` rows (DP-01); the notice move is recorded through the local decision-record library and relayed on `rwb.decision-record.v1` (DP-03); the balance and the postal address that the panel shows are rwb-source-data's facts, read at the route and never from a `v_ace_*` view of this service (DP-05); the feature switch, the notice type list, the override reasons and the template state values are parameters and reference data read with the version in force (DP-06, DP-07); the record leaves through the outbox with the CloudEvents envelope (DP-09); the 16:00 run that consumes the approved state is RWB-P6-E2021-APP's Temporal Schedule and not a Quartz row of this story (DP-10); the three former in-process `NoticeApi` calls become REST operations with a mock, one hop and a 2 s budget (DP-11); the base is `/api/recovery/comms/v1` (DP-13); and the panel reaches the answer through the gateway-bff composite route (DP-19). It serves REQ-APD-002 (the approver sees the recommendation, the reasons and the inputs on one screen) and REQ-APD-006 (demand and recall notices are approved through approval routing), and supports CTL-05 (the preparer cannot decide) and CTL-14 (only an approved notice is dispatched) from the notice side. The measure is the FSD P6 one: notices with an approval entry before dispatch, target 100 percent.

### 3. Preconditions

- RWB-P6-E1052-APP is done: the notice is generated from the current Approved template with `notice_type`, `template_id`, `party_id` and `document_id` set and state Generated, and `rwb.comms.NoticeGenerated.v1` (EV-13) is published on `rwb.comms.events.v1`.
- RWB-P6-E1046-APP is done: `template` and `merge_field` hold the versions, the Legal approval (`approved_by_legal`, `approved_by`, `approved_at`, `valid_from`) and the withdrawal, so the state of a template version is a row of this service and not a value of another.
- The `rwb_comms` baseline is in place and the per-service Flyway sequence runs in `rwb_comms` (DP-15); the library objects `outbox_event`, `processed_event` and `idempotency_key` exist (DP-09).
- RWB-P7-E2014-CON is published and is the contract this story builds against on Day 1: the composite route of SCR-11 with the SCR-18 panel, the notice summary shape it consumes, the three decision operations and their answers, the `Idempotency-Key`, and the fakes. The screen contract is a C row and never blocks the build (Template and Rules §R5.7).
- The local decision-record library and the shared topic `rwb.decision-record.v1` are live (DP-03), and the outbox relay of the platform carries the record of every notice move (DP-09).
- The parameters contract of rwb-case is live (RWB-P3-E1042-CON, DP-06) for the switch `rwb.decision.notice-approval` as the legacy story names it, and the reference-data contract is live (RWB-P3-E1043-CON, DP-07) for LOV-NOTICE, LOV-OVERRIDE-REASON, LOV-PRODUCT and the template state values DRAFT, APPROVED and WITHDRAWN of TSD P6 T-A.2.
- The templates DEMAND-MTG, DEMAND-MTG-B (a second Approved variant of the demand notice for Mortgage) and RECALL-MTG are Approved in language TH, with the Legal approval that RWB-P6-E1046-APP records.
- Notice "N-0201" for case "RW-2026-000123" exists in state Generated from template "DEMAND-MTG" "TH" version 2 under rule "R-LIT-03" version "LIT-2026.12", prepared by "U-9211", and its approval "A-0201" is WAITING for role RW-LITOFF in rwb-decision.
- Test users in SIT hold RW-LITOFF; one holds RW-LEGAL; one holds RW-CASEOWN. The SIT fixtures are synthetic and carry no name, no address and no account number.
- No build dependency: this story has no H row. The platform contracts the patterns name (DP-03, DP-06, DP-07, DP-09, DP-19) are held by the notice contract baseline RWB-P6-E1052-CON and reached through the published libraries, and the plan records none as a build row for this slice (GAP-2389; ASM-3965).

### 4. Flow

1. A litigation officer opens SCR-10 Approval queue and selects the D7.1 item; the queue and the screen are composed by the gateway-bff composite route of RWB-PLT-N001-CON on the contract RWB-P7-E2014-CON (DP-19).
2. The route calls this story's read: `GET /api/recovery/comms/v1/notices/{noticeId}` with the `noticeId` of the approval's `source_ref`. The answer carries the notice `id`, `caseId`, `documentId`, `noticeType`, `state`, and the `templateCode`, `templateVersion` and `templateState` of the template version that produced it.
3. The panel shows the notice as the document reference the answer carries, together with the notice type, the template code and version, the template state and the case; the notice body and the addressee are not part of the answer and are served by rwb-document and rwb-source-data at the route.
4. rwb-decision runs its checks — the caller holds Litigation right A, the caller is not the preparer, the reason rules, the input-age limits — and on a decision calls one of the three operations of this story with an `Idempotency-Key`. The approval answer and the `decisionLogEntryId` it passes are, with the notice ID, the whole input of this service (DP-11).
5. On approve: `POST /notices/{noticeId}/approve` with the decision entry reference moves the notice Generated to Approved, stores the reference and the approval time, and the notice becomes eligible for the 16:00 dispatch run of RWB-P6-E2021-APP (JOB-10). The answer is the notice in state Approved, 200.
6. On a change of variant: `POST /notices/{noticeId}/regenerate` with `templateCode` of the chosen variant produces the new notice version from that Approved variant of the same notice type and product group and writes it on the same notice; the approval then approves that version, and only the changed notice reaches the dispatch run. That the new version stays on the same notice row is a ruling of this story (GAP-2386; ASM-3962).
7. On a refusal: `POST /notices/{noticeId}/hold` with reason `REFUSED_BY_APPROVER` and the decision entry reference moves the notice Generated to Held with `hold_reason` set, and the notice is excluded from the dispatch run. A withdrawn template is held the same way with reason `TEMPLATE_WITHDRAWN` under R-LIT-04, and an approve of such a notice is refused before any move.
8. Each move writes one local decision record through the library in the same transaction as the notice row: decision code D7.1, the rule in force (R-LIT-03 on approve, R-LIT-04 on a withdrawn template), the notice and case IDs, the template code and version, the approver and the reference of the approval entry, decided at. The library relays it on `rwb.decision-record.v1` through the outbox (DP-03, DP-09); that the move writes its own record next to the entry of the approval is a ruling of this story (GAP-2390; ASM-3966).
9. A move whose record cannot be written does not happen: the notice row is unchanged, the answer is 503 with MSG-P7-003, and an incident is raised under R-UNI-39.
10. A repeat of any of the three calls with the same `Idempotency-Key` returns the first answer and moves nothing a second time; a call against a notice that is no longer in state Generated answers 409 with MSG-GEN-004.
11. The dispatch Schedule of RWB-P6-E2021-APP selects the notices in state Approved for the business date and runs the conduct check; this story reads nothing of that run and is not called by it.
12. Renewed approval is not offered: an approved notice that is later withdrawn is held by the dispatch story, never re-approved here.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The live template version of the notice is WITHDRAWN | The approve is refused with 409 and the notice stays Generated; the hold with TEMPLATE_WITHDRAWN moves it to Held under R-LIT-04 | MSG-P6-003 | AC3 |
| X2 | The chosen variant is not Approved, or is of another notice type or product group | The regenerate is refused with 422 and no new notice version is produced | MSG-GEN-001 | AC4 |
| X3 | The notice is not in state Generated (already Approved or Held) | The call is refused with 409 and the state is unchanged | MSG-GEN-004 | AC7 |
| X4 | The caller does not hold the Litigation right of the operation | Refused with 403; nothing changes | MSG-P4-002 | AC8 |
| X5 | The notice is absent or outside the caller's scope | Refused with 404; nothing changes | MSG-P4-003 | AC8 |
| X6 | The local decision record cannot be written | The notice row is unchanged, the answer is 503 and an incident is raised | MSG-P7-003 | AC6 |
| X7 | A repeat with the same `Idempotency-Key` | The first answer is returned; no second move and no second record | None | AC2, AC5 |
| X8 | `templateCode` missing on regenerate, or `reasonCode` missing on hold | Refused with 422 naming the field | MSG-GEN-001 | AC4, AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | One service, four operations and one record path; builds against the published notice contract RWB-P6-E1052-CON, the P7 screen contract RWB-P7-E2014-CON and the platform libraries; nothing waits on another team |
| Negotiable | The feature switch, the notice type list, the override reasons and the template state values are data rows; the story fixes only the order of the checks and the state path |
| Valuable | The notice a person approved is the only notice dispatched, and a withdrawn template cannot be approved |
| Estimable | Four operations, two state rules, one migration column, one record path |
| Small | Fits one sprint with its tests, as the secondary slice of a legacy key that RWB-P7-E2014-APP leads |
| Testable | Each criterion in section 7 runs as one automated test against the contract fakes and the `rwb_comms` fixtures, and the twelve legacy cases of section 16 keep their IDs and their data |

### 7. Acceptance criteria

```gherkin
Feature: Approval screen for D7.1 demand and recall notices — the rwb-comms slice

  Background:
    Given the environment is SIT
    Given demand notice "N-0201" for case "RW-2026-000123" is "Generated", generated at 08:10 on 14 December 2026 from template "DEMAND-MTG" "TH" version 2, under rule "R-LIT-03" version "LIT-2026.12", prepared by "U-9211"
    Given its template "DEMAND-MTG" version 2 is "APPROVED" and template "DEMAND-MTG-B" is "APPROVED" for product group "MORTGAGE"
    Given its approval "A-0201" is WAITING for role RW-LITOFF in rwb-decision
    Given the decision entry "E-0201" is the entry of "A-0201"
    Given test user "U-9212" holds RW-LITOFF on Litigation right A and did not prepare the notice

  Scenario: AC1 The notice answer the panel reads (new, D-RCV-60)
    When "U-9212" opens "A-0201" and the route reads notice "N-0201"
    Then the answer is status 200 and carries notice "N-0201", case "RW-2026-000123", its document reference, notice type "DEMAND", state "Generated", template code "DEMAND-MTG", template version 2 and template state "APPROVED"
    Then the answer carries no name, no address and no account number
    Then the answer is returned inside the 2 s budget of the route

  Scenario: AC2 Approve moves the notice and is recorded (new, D-RCV-60)
    Given the local decision record of notice "N-0201" can be written
    When "U-9212" approves and rwb-decision calls the approve operation for "N-0201" with decision entry "E-0201" and an Idempotency-Key
    Then the answer is status 200 and notice "N-0201" is in state "Approved" with the decision entry reference "E-0201"
    Then notice "N-0201" is eligible for the 16:00 dispatch run of the business date
    Then one local decision record exists with decision code "D7.1", rule "R-LIT-03", notice "N-0201", case "RW-2026-000123", template "DEMAND-MTG" version 2, approver "U-9212" and decided at, and one record is in the outbox
    When the same approve call arrives again with the same Idempotency-Key
    Then the answer is the first answer and no second record and no second state move is written

  Scenario: AC3 A withdrawn template is never approved (new, D-RCV-60)
    Given template "DEMAND-MTG" version 2 is withdrawn at 09:30 on 14 December 2026
    When rwb-decision calls the approve operation for "N-0201" at 10:00
    Then the answer is status 409 with MSG-P6-003
    Then notice "N-0201" stays "Generated" and no decision record is written
    When rwb-decision calls the hold operation for "N-0201" with reason "TEMPLATE_WITHDRAWN" and decision entry "E-0201"
    Then the answer is status 200 and notice "N-0201" is in state "Held" with hold reason "TEMPLATE_WITHDRAWN"
    Then one local decision record exists with rule "R-LIT-04" for notice "N-0201"

  Scenario: AC4 A change regenerates from the chosen approved variant (new, D-RCV-60)
    Given the local decision record of notice "N-0201" can be written
    When rwb-decision calls the regenerate operation for "N-0201" with template code "DEMAND-MTG-B" and an Idempotency-Key
    Then the answer is status 200 and notice "N-0201" carries template code "DEMAND-MTG-B", a new document reference and notice type "DEMAND"
    Then notice "N-0201" is still in state "Generated" and only the changed version can be approved
    When the regenerate is called with template code "RECALL-MTG" for product group "MORTGAGE"
    Then the answer is status 422 with MSG-GEN-001 naming "templateCode" and no new notice version is produced
    When the regenerate is called with no template code
    Then the answer is status 422 with MSG-GEN-001 naming "templateCode"

  Scenario: AC5 A refusal holds the notice (new, D-RCV-60)
    Given the local decision record of notice "N-0201" can be written
    When rwb-decision calls the hold operation for "N-0201" with reason "REFUSED_BY_APPROVER" and decision entry "E-0201"
    Then the answer is status 200 and notice "N-0201" is in state "Held" with hold reason "REFUSED_BY_APPROVER"
    Then notice "N-0201" is not eligible for the 16:00 dispatch run
    Then one local decision record exists with final call of the approval and the reason code, and one record is in the outbox
    When the hold is called with no reason code
    Then the answer is status 422 with MSG-GEN-001 naming "reasonCode"
    When the same hold call arrives again with the same Idempotency-Key
    Then the answer is the first answer and no second record is written

  Scenario: AC6 A move that cannot be recorded does not happen (new, D-RCV-60)
    Given the local decision record library refuses the write for notice "N-0201"
    When rwb-decision calls the approve operation for "N-0201" with decision entry "E-0201"
    Then the answer is status 503 with MSG-P7-003
    Then notice "N-0201" stays "Generated" with no decision entry reference
    Then an incident is raised under rule R-UNI-39 and nothing is in the dispatch run

  Scenario: AC7 A notice moves once (new, D-RCV-60)
    Given notice "N-0201" is in state "Approved"
    When rwb-decision calls the approve operation for "N-0201" with decision entry "E-0201"
    Then the answer is status 409 with MSG-GEN-004
    Then the state and the decision entry reference of "N-0201" are unchanged and no second record is written
    When rwb-decision calls the hold operation for the same notice with reason "REFUSED_BY_APPROVER"
    Then the answer is status 409 with MSG-GEN-004 and the notice stays "Approved"

  Scenario: AC8 The right and the scope of the four operations (new, D-RCV-60)
    Given test user "U-9212" holds RW-CASEOWN and case "RW-2026-000123" is outside its scope
    When "U-9212" calls the read of notice "N-0201"
    Then the answer is status 404 with MSG-P4-003 and nothing is returned
    Given test user "U-9212" holds RW-CASEOWN and case "RW-2026-000123" is inside its scope
    When "U-9212" calls the approve operation for "N-0201"
    Then the answer is status 403 with MSG-P4-002
    Then notice "N-0201" stays "Generated" and no record is written
```

The eight criteria are new under D-RCV-60 and test only the four operations of this story and its two state rules. No legacy criterion is copied here: the ten criteria of RWB-E2-014 belong to RWB-P7-E2014-APP, which owns the approval screen, and this story answers the notice half of each of them behind that contract's fake. The values the criteria use are copied unchanged from RWB-E2-014 and the P6 extracts — the notice "N-0201", case "RW-2026-000123", template "DEMAND-MTG" version 2, variant "DEMAND-MTG-B", rule "R-LIT-03" version "LIT-2026.12", preparer "U-9211", approver "U-9212", the 09:30 withdrawal, the 10:00 decision, the 16:00 run, the reason codes `REFUSED_BY_APPROVER`, `TEMPLATE_WITHDRAWN` and `TEMPLATE_VARIANT`, and the messages MSG-P6-003, MSG-GEN-001, MSG-GEN-004, MSG-P4-002, MSG-P4-003 and MSG-P7-003 — and no business value is invented. The paths are relative to the base of this service, `/api/recovery/comms/v1` (DP-13).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Only a notice in state Approved is eligible for dispatch, and the notice reaches Approved only through the D7.1 approval | REQ-APD-006; CTL-14; legacy BR1 |
| BR2 | The notice answer carries the template code, the template version and the state of that version, so the approver sees what the notice was built from | REQ-APD-002; legacy BR2 |
| BR3 | The service does not decide who approves: the preparer rule, the right and the reason rules are checked by rwb-decision, and this service refuses a move only on its own notice state and template state | CTL-05; legacy BR3; DP-11 |
| BR4 | A notice whose template version is WITHDRAWN is never approved; it is held under R-LIT-04 | R-LIT-03; R-LIT-04; legacy BR5 |
| BR5 | A change of variant regenerates from an Approved variant of the same notice type and the same product group, and only that version is approved | R-UNI-14; CTL-07; LOV-OVERRIDE-REASON |
| BR6 | The notice state moves Generated to Approved, or Generated to Held with a reason code; no other transition is accepted and a second move is refused | legacy section 9; TSD P6 T3.0 |
| BR7 | A move that cannot be written to the decision record does not happen, and the notice stays Generated | Principle 5; R-UNI-39; legacy BR8 |
| BR8 | Every move is one transaction over the notice row, the local decision record and the outbox row, and each move is idempotent on the `Idempotency-Key` | ADR-015; DP-03; DP-09 |
| BR9 | The notice, its template reference and its hold reason are `rwb_comms` rows; the approval, the entry and the case are reached on their owners' contracts and never by a table read (DP-01, DP-11) | Architecture v5 slides 17 and 41; DP-01 |
| BR10 | The notice carries no name, no address and no account number; the panel's masked address and total balance are rwb-source-data facts read at the route (DP-05, DP-19) | Template and Rules §R7.2 s17; ADR-010 |
| BR11 | The feature switch, the notice types, the product groups, the override reasons and the template state values are parameters and reference data read with the version in force; no such value is written in code | TSD P6 T3.2; FSD P6 A2.1 BR-P6-001; DP-06, DP-07 |
| BR12 | The move is recorded in the local decision record with the rule in force — R-LIT-03 on an approval, R-LIT-04 on a withdrawn template — and relayed on the shared topic, so the central ledger and the reporting read model follow without a call made for them | DP-03; DP-09; legacy section 12 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Generated | Approve operation with a decision entry reference | The live template version is APPROVED | Approved |
| Generated | Hold operation with reason `REFUSED_BY_APPROVER` | A reason code is given | Held |
| Generated | Hold operation with reason `TEMPLATE_WITHDRAWN` | The live template version is WITHDRAWN (R-LIT-04) | Held |
| Generated | Regenerate operation with a template code | The variant is APPROVED, of the same notice type and product group | Generated, carrying the new template and a new document reference |
| Approved | Approve or hold operation | None: the notice has left Generated | Refused with 409, state unchanged |
| Held | Approve or hold or regenerate operation | None: the notice has left Generated | Refused with 409, state unchanged |

The template state that gates the first row is `template.state` and moves DRAFT to APPROVED on the approve operation of the template catalogue and APPROVED to WITHDRAWN on its withdraw operation, both of RWB-P6-E1046-APP; this story reads it and never writes it. Sent, Delivered and Unserved are the dispatch states of RWB-P6-E2021-APP and are not reached here: this story hands over an Approved notice and reads nothing of the run. A held notice stays held until its template is approved again and the notice is regenerated and approved anew, which is a new decision and not a re-approval of the old row.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-LITOFF, litigation officer | Litigation CRUA in TSD P6 T6.1: reads the notice answer (right R) and, through the approval of rwb-decision, causes the approve, regenerate and hold moves (right A) |
| RW-LEGAL, legal counsel | Litigation RA in TSD P6 T6.1: reads the notice and holds the template approval that the approve gates on; its own approvals are checked by rwb-decision and not here |
| RW-HEADLIT, Head of Litigation | Litigation RA in TSD P6 T6.1: the escalated approval of rwb-decision reaches the same three moves |
| rwb-decision service identity | Calls the three decision operations with the approver's decision entry reference, one hop, under the right declared in 12.1 |
| rwb-comms service identity | Reads its own `notice` and `template` rows, writes the state, the `hold_reason` and the decision entry reference, and writes the outbox rows (DP-02) |
| Decision-record library identity | Writes the local decision record of every move and relays it on `rwb.decision-record.v1` (DP-03) |
| Platform route owner | Owns the composite route, the field list, the mask flags and the budget; this story answers the route |

The three decision operations are not declared in the appendix T-A of TSD P6, so their declared right is an assumption of this story (GAP-2388; ASM-3964); the matrix of TSD P6 T6.1 gives the Litigation rights of each role and is the only source used for the rows above. Authorisation is enforced at gateway-bff through the rwb-access contract, which is not in this key's pattern set, so no DP-08 row is claimed.

### 11. Data

| BR Field ID | Entity in `rwb_comms` | Field | Read or write |
|---|---|---|---|
| DF-LEG-015 | notice | id | Read (the key of every operation) |
| DF-LEG-016 | notice | case_id | Read in the answer |
| DF-LEG-017 | notice | document_id | Read in the answer; written on regenerate |
| DF-LEG-018 | notice | notice_type | Read in the answer; the check of the variant |
| DF-LEG-030 | notice | party_id | Read only, never in an event |
| DF-LEG-031 | notice | template_id | Read in the answer; written on regenerate |
| DF-LEG-032 | notice | hold_reason | Write on a hold |
| Standard column | notice | state | Write on every move, read in the answer |
| Standard column | notice | version, updated_at, updated_by | Write, for the optimistic lock of the move |
| No field ID | notice | decision_log_entry_id (added by this story) | Write on approve and hold (GAP-2385; ASM-3961) |
| DF-REF-045, DF-REF-046, DF-REF-047 | template | id, template_code, template_version | Read in the answer |
| DF-REF-049 | template | product_group | Read for the same-product rule of a change |
| DF-REF-051, DF-REF-065 | template | approved_by_legal, valid_from | Read, with `state`, for the approve gate |
| Standard column | template | state | Read: DRAFT, APPROVED or WITHDRAWN |
| DF-DEC-001 to DF-DEC-018 | decision record (local, through the library) | decision code, rule, notice, case, approver, decided at, hash chain | Write |

This story creates no table: `notice` and `template` are the baseline of RWB-P6-E1052-APP and RWB-P6-E1046-APP, and the only schema change is the nullable `decision_log_entry_id uuid` on `notice` with a unique index, in the per-service Flyway step `V2014_1__notice_decision_reference.sql` in `rwb_comms` (DP-15). The reference is nullable because a notice can be held by the dispatch story without an approval entry, and it is not the record itself: the record is the library's, in `rwb_comms`, and is mirrored to the central ledger on the shared topic. The status of the approval, its terms and its own `decision_log_id` are `rwb_decision` rows and are not read or written here. No column of this service holds a name, an address, an identity number or an account number; the masked address of the panel is produced at the route from the rwb-source-data answer. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

Owner rwb-comms (P6); base `/api/recovery/comms/v1` (DP-13). Topic `rwb.comms.events.v1`, queue `rwb-comms`, schema `rwb_comms`. The shapes below are those fixed in RWB-P7-E2014-CON, which this story builds against, and in RWB-P6-E1052-CON, the notice contract baseline of this service.

#### 12.1 REST operations provided

| ID | Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|---|
| API-P6-002 | GET | `/notices/{noticeId}` | Read a notice with its template code, version and state for the approval panel | Litigation, right R, scope applied | Not applicable |
| — | POST | `/notices/{noticeId}/approve` | Move the notice Generated to Approved with the decision entry reference; answers the notice | Litigation, right A, scope applied | `Idempotency-Key` required |
| — | POST | `/notices/{noticeId}/regenerate` | Produce the notice version from another Approved variant of the same notice type and product group; answers the notice | Litigation, right A, scope applied | `Idempotency-Key` required |
| — | POST | `/notices/{noticeId}/hold` | Move the notice Generated to Held with a reason code and the decision entry reference; answers the notice | Litigation, right A, scope applied | `Idempotency-Key` required |

The three decision operations are the `NoticeApi.approve`, `NoticeApi.regenerate` and `NoticeApi.hold` of RWB-E2-014, which the legacy publishes only as Java methods and which neither the Ownership Map nor appendix T-A of TSD P6 lists as REST rows (GAP-2384; ASM-3960). Their declared right is an assumption in the same way (GAP-2388; ASM-3964). Requests: approve and hold carry `decisionLogEntryId` and, on hold, `reasonCode`; regenerate carries `templateCode`. Errors: 401 no session; 403 the role lacks the declared right (MSG-P4-002); 404 the notice is absent or out of scope (MSG-P4-003); 409 the template version is withdrawn (MSG-P6-003), or the notice is no longer in state Generated (MSG-GEN-004); 422 a missing or barred `templateCode` or `reasonCode` (MSG-GEN-001); 503 the record was not written (MSG-P7-003). The property list of the notice answer is not given by T-A.2 and is baselined in RWB-P7-E2014-CON from TSD P6 T3.1 plus the template facts (GAP-2387; ASM-3963).

#### 12.2 REST operations consumed

| Method and path | Owner | Use in this story |
|---|---|---|
| The approval answer and the decision entry reference of RWB-P7-E2014-CON | P7 rwb-decision | The `decisionLogEntryId` and the approver of every move; this story never reads the approval table and never decides who approves (DP-11) |
| The parameters read of `rwb.decision.notice-approval`, on RWB-P3-E1042-CON | P3 rwb-case | The feature switch of the three operations, read with the version in force (DP-06, BR11) |
| The reference-data read of LOV-NOTICE, LOV-PRODUCT, LOV-OVERRIDE-REASON and the template state values, on RWB-P3-E1043-CON | P3 rwb-case | The same-notice-type and same-product check of a change, the reason codes and the three template states (DP-07, BR11) |

Every row is one hop with a 2 s timeout and a breaker per downstream (DP-11, ADR-020). No row reads a table and no row reads a `v_ace_*` view: only rwb-source-data reads the ACE views (ADR-010).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | decision code D7.1, rule (R-LIT-03 or R-LIT-04) and its version, notice ID, case ID, template code and version, notice state from and to, reason code where one applies, approver, decided at, reference of the approval entry |

It is written to the outbox in the same transaction as the notice row and relayed with the CloudEvents 1.0 envelope by the outbox relay of the platform (DP-03, DP-09). This story publishes no event of its own topic: the three events of `rwb.comms.events.v1` are `NoticeGenerated` (EV-13), published by RWB-P6-E1052-APP when the notice is produced, and `NoticeDispatched` (EV-14) and `NoticeDelivered` (EV-15), published by RWB-P6-E2021-APP. The movement of a notice between Generated, Approved and Held is not one of the three and reaches its consumers through the decision record, which is what the legacy contract of RWB-E2-014 declares ("consumes EV-13 NoticeGenerated; publishes EV-08 DecisionRecorded").

#### 12.4 Events consumed

None. EV-13 `rwb.comms.NoticeGenerated.v1` is published by the generation story of this same service, and the listener that consumes it to route D7.1 to the litigation officer is RWB-P7-E2013-APP; this story starts when the approval exists and is called on the decision. The two other subscriptions of the service (the deviation events and the case state event) belong to RWB-P6-E2021-APP.

#### 12.5 Workflows and activities

None. The four operations are synchronous calls of one hop and 2 s; no workflow is started and no activity is added. `NoticeDispatchWorkflow` and the 16:00 Schedule of JOB-10 are RWB-P6-E2021-APP's, and this story only makes a notice eligible for that run by moving it to Approved (DP-10 as a boundary, not as work of this slice).

#### 12.6 Schedules

None. No Quartz row and no Schedule is added. The 16:00 dispatch run that consumes the Approved state is the Schedule of RWB-P6-E2021-APP on task queue `rwb-comms` in the namespace `rwb-recovery` (DP-10).

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| notice | P6 (rwb_comms) | The notice row: `state`, `hold_reason`, `template_id`, `document_id` and the added `decision_log_entry_id` are written here |
| template | P6 (rwb_comms) | The template version, its product group, its Legal approval and its `state`; read only here, written by RWB-P6-E1046-APP |
| decision record (local) | P6 rows in `rwb_comms`, written through the P7 library | The record of every notice move (DP-03) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The decision record, the stored `Idempotency-Key` answer of the three operations (DP-09) |

Not owned and never read: `approval` and `decision_log_entry` (P7 rwb-decision), `document` (P5 rwb-document), `recovery_case` (P3 rwb-case), `parameter_catalog` and `reference_row` (P3 rwb-case), `outbound_item` and `interface_config` (P2 rwb-integration). `merge_field` is P6's and is not touched by this story. No foreign key crosses a service boundary (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Documented answers used by this story |
|---|---|---|
| rwb-decision approval fake (RWB-P7-E2014-CON) | The approval answer and the `decisionLogEntryId` of the move | Approval `A-0201` for notice `N-0201` with entry `E-0201` and approver `U-9212`; the refused approval of AC5; a delayed answer beyond 2 s |
| rwb-comms notice and template fake (RWB-P6-E1052-CON) | The notice rows read by the four operations | Notice `N-0201` Generated from `DEMAND-MTG` TH version 2; `DEMAND-MTG-B` and `RECALL-MTG` Approved for MORTGAGE; `DEMAND-MTG` version 2 WITHDRAWN from 09:30 on 14 December 2026 for AC3 |
| Decision-record library fake | The local record and the shared topic | A healthy chain and outbox; a refusing library for AC6 |
| Parameters and reference-data fake | The switch and the lists | `rwb.decision.notice-approval` on and off; LOV-NOTICE, LOV-PRODUCT, LOV-OVERRIDE-REASON and the three template states |

The fakes are derived from the published contracts of RWB-P7-E2014-CON and RWB-P6-E1052-CON, and the drift test of each contract story fails a build in which a fake and the document disagree.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 4 provided, 3 consumed | The notice read and the three decision operations provided; the approval answer, the parameters read and the reference-data read consumed; one hop, 2 s |
| Kafka | 1 published, 0 consumed | `DecisionRecorded` on `rwb.decision-record.v1` through the library; nothing of `rwb.comms.events.v1` |
| Temporal | None | No workflow, activity or Schedule; the dispatch run is RWB-P6-E2021-APP's |
| File | None | No file is read or written; the notice body is a document reference owned by rwb-document |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `notices`, Java package `th.co.scb.ace.workbench.recovery.comms.notices`; the operations are an extension of the notice controller of RWB-P6-E1052-APP and add no new module.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/comms/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-05 applies as a prohibition: this service reads no `v_ace_*` view and no ACE row, and the total balance and the postal address that the panel shows are rwb-source-data facts read at the route, so the notice answer carries identifiers and codes only. DP-10 applies as a boundary: the JOB-10 run is RWB-P6-E2021-APP's Temporal Schedule, and this story adds no job. No pattern is claimed for DP-02 (the per-service login is the DB story's), DP-04 (no rule package is evaluated here; the rule in force is read as an identifier of the approval), DP-08 (the authorise call is the platform route's), DP-12 (no case workflow is composed), DP-14 (no topic is renamed by this story), DP-15 (the migration is the baseline's plus one column), DP-16, DP-17 (the data lake is removed and nothing here reads it), DP-18 (no ledger entry is written by a notice move) or DP-20. The H rows the table names are met through the notice contract baseline RWB-P6-E1052-CON and the published libraries, and the plan carries none of them as a build row of this slice (GAP-2389; ASM-3965).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| NoticeController | Controller | `GET /notices/{noticeId}` and the three POST operations, with validation, the `Idempotency-Key` and the problem mapping of 12.1 |
| NoticeReadService | Service | Builds the notice answer with the template code, version and state, and applies the scope and the mask flags of the route |
| NoticeDecisionService | Service | Orders the checks — state Generated, template state, variant eligibility — and performs the move with its record in one transaction |
| VariantSelector | Service | Resolves the chosen template code to an Approved variant of the same notice type and product group, so a change never crosses a notice type |
| DecisionRecorder | Service | Writes the local decision record and the outbox row through the library; a failure fails the move |
| TemplateStateReader | Adapter | Reads `template.state`, the Legal approval and `valid_from` of the version that produced the notice, in `rwb_comms` |
| NoticeClient (for rwb-decision) | Adapter | The contract the approval screen consumes: the read and the three decision operations, one hop, 2 s |

**Database and migrations**

- Writes `notice` (`state`, `hold_reason`, `template_id`, `document_id`, `decision_log_entry_id`), the local decision record and the library objects, all in `rwb_comms`; reads no other schema.
- One migration: `V2014_1__notice_decision_reference.sql` adds the nullable `decision_log_entry_id uuid` with a unique index and the reason-code check on `hold_reason`; no column carries a name, an address or an account number.
- No row of `template` or `merge_field` is written here, and no row of `approval` or `decision_log_entry` is read.

**Configuration and reference data**

- `rwb.decision.notice-approval`, the legacy switch name kept unchanged, read as a parameter through RWB-P3-E1042-CON (DP-06); off refuses the three operations closed with 503 MSG-P7-003 and leaves the notices as they are. The namespace of the switch for the comms half is not settled (GAP-2391; ASM-3967).
- LOV-NOTICE, LOV-PRODUCT and LOV-OVERRIDE-REASON read through RWB-P3-E1043-CON (DP-07); the template state values DRAFT, APPROVED and WITHDRAWN as TSD P6 T-A.2 uses them; the hold reason vocabulary is fixed by this story because no source holds it as a list (GAP-2391; ASM-3967).

**Build steps**

1. NoticeReadService and the answer mapping with the template facts; test AC1 against the fixture of `N-0201`.
2. NoticeDecisionService and the state gate: Generated only, 409 on any other state; tests for AC7.
3. The approve path with the decision entry reference, the record and the idempotent replay; tests for AC2 and AC5.
4. The template gate: WITHDRAWN refuses with MSG-P6-003 and the hold with TEMPLATE_WITHDRAWN follows; test for AC3.
5. VariantSelector and the regenerate path with the same-type and same-product check, 422 on a barred or missing code; test for AC4.
6. DecisionRecorder and the fail-closed path; test AC6 and TC-E2-014-12.
7. The scope and right refusals at the operation, with the route's field list and mask flags; test AC8.
8. The SIT run with rwb-decision: approve, and confirm the approved notice in the 16:00 run of RWB-P6-E2021-APP, and that no held notice is in it.

**Done when.** The tests in section 16 pass, the contract tests of RWB-P7-E2014-CON and RWB-P6-E1052-CON stay green, and a SIT week shows every demand and recall notice moved only through the three operations, every move with its decision record, no approved notice with a withdrawn template, and no notice in the dispatch run without an approval entry.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P6-003 | The template version of the notice is withdrawn | The {template} template has been withdrawn. The notice is on hold until Legal approves a new version. |
| MSG-GEN-004 | The notice is no longer in state Generated | Someone else changed this record. Reload it to see their change. |
| MSG-GEN-001 | A required field is missing or barred | Enter {field}. |
| MSG-P4-002 | The role lacks the declared right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The notice is outside the caller's scope | This case is not in your scope. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

MSG-P6-003, MSG-GEN-004, MSG-GEN-001 and MSG-P7-003 are copied unchanged from RWB-E2-014 section 14; MSG-P4-002 and MSG-P4-003 are the platform catalog's. Thai text for each message follows DL10.

### 15. Screens and states

The SCR-18 Notice approval panel inside SCR-11 is served through the gateway-bff composite route (DP-19, RWB-PLT-N001-CON); the panel names, the field list, the mask flags and the timeout budget are fixed in RWB-P7-E2014-CON. This story supplies the notice half of the panel answer and sets these states:

| Screen | State | What the user sees |
|---|---|---|
| SCR-18 Notice approval | Generated | The notice, its template code and version and the template state while the decision is open; approve, change of variant and reject are offered by the route, not by this service |
| SCR-18 Notice approval | Approved | The notice moved on the approval and waiting for the 16:00 dispatch run |
| SCR-18 Notice approval | Held | The notice held with its reason code, and MSG-P6-003 when the reason is a withdrawn template |
| SCR-18 Notice approval | Withdrawn template | MSG-P6-003 and no approve offered, because the approve is refused by this service as well as by the route |

The notice preview is the document reference the answer carries, served by rwb-document at the route; the notice body, the addressee and the account number are never in the answer, and the masked address of the panel is a rwb-source-data value read at the route. The route's own loading, temporarily unavailable and session-expired states are the platform route's and are declared in RWB-P7-E2014-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-014-01 | AC2, BR1, BR8 | Contract | Synthetic demand notice N-0201 from DEMAND-MTG version 2; legacy AC1 is owned by RWB-P7-E2014-APP, and the notice half runs here |
| TC-E2-014-02 | AC4, BR5 | Contract | Variant DEMAND-MTG-B with reason TEMPLATE_VARIANT |
| TC-E2-014-03 | AC5, BR6 | Contract | Refusal with a reason; hold reason REFUSED_BY_APPROVER |
| TC-E2-014-04 | AC7, BR3 | Contract | Preparer who also holds RW-LEGAL; the refusal is rwb-decision's and no call reaches this service |
| TC-E2-014-05 | AC1, BR2 | Contract | Total balance from a load 3 days old; the age check is rwb-decision's and the answer is unchanged |
| TC-E2-014-06 | AC3, BR4 | Contract | Template DEMAND-MTG version 2 withdrawn after generation |
| TC-E2-014-07 | AC5, BR6 | Contract | Refusal with an empty reason; the hold call never leaves rwb-decision |
| TC-E2-014-08 | AC4, BR5 | Contract | Variant change with no reason code; the regenerate call never leaves rwb-decision |
| TC-E2-014-09 | AC7 | Contract | Two litigation officers deciding one item; the second approve call answers 409 |
| TC-E2-014-10 | AC1 | Component | Notice answer content check: template code, version and state, and no personal data |
| TC-E2-014-11 | AC8 | Component | A role without the right is refused with MSG-P4-002, and a notice out of scope with MSG-P4-003 |
| TC-E2-014-12 | AC6 | NFR | The decision record write forced to fail during an approval; the notice stays Generated |

The twelve cases keep their legacy IDs, order and data; the legacy level System maps to Contract, Access to Component and Resilience to NFR, because the end-to-end journey of each is owned by RWB-P7-E2014-APP and by the SIT run of section 13. No `-ITG` copy exists for this key in this story: the cross-service behaviour is proved inside the same SIT run through rwb-decision, and an ITG copy of a case, if one is added, takes the suffix `-ITG` on the ITG story and not here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the switch, the notice types, the product groups, the override reasons, the template state values and the reason codes are parameters and reference data read with the version in force (DP-06, DP-07).
- No personal data in events, logs, tests or prompts: notice IDs, case IDs, document references, template codes and versions, reason codes and dates only. The notice body and the addressee stay in rwb-document and rwb-source-data, and the SIT fixtures are synthetic.
- No read of another service's tables and no `v_ace_*` read of this service: the approval, the case and the ACE facts arrive on their owners' contracts or at the route (DP-01, DP-05, DP-11).
- The notice row and its decision record commit in one transaction, so a move that cannot be recorded changes nothing (BR7, BR8).
- Any move is idempotent on the `Idempotency-Key`, and no notice moves twice (BR8).
- One base, one topic, one queue: `/api/recovery/comms/v1`, `rwb.comms.events.v1` and `rwb-comms` in the namespace `rwb-recovery` (DP-13, DP-14).
- One hop and 2 s on every call, and a timeout never approves, regenerates or holds a notice (DP-11).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-APD-002 | Recommendation, reasons, inputs and limit on one screen | Business Requirements Epic 2, section 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR2, BR10 | TC-E2-014-05, TC-E2-014-10 |
| REQ-APD-006 | Demand and recall notices approved through approval routing | Business Requirements Epic 2, section 3.7 | FEAT-APD-08 | 8.1 Prepare pre-litigation | BR1, BR3, BR4, BR5, BR6, BR7, BR8 | TC-E2-014-01 to TC-E2-014-04, TC-E2-014-06 to TC-E2-014-09, TC-E2-014-11, TC-E2-014-12 |

| Trace item | Value |
|---|---|
| Legacy key | RWB-E2-014, disposition Split (rework) |
| Legacy criteria owned here | None: AC1 to AC10 are RWB-P7-E2014-APP's, and this story answers their notice half behind the contract RWB-P7-E2014-CON |
| Criteria of this story | AC1 to AC8, each tagged (new, D-RCV-60) |
| Test cases | TC-E2-014-01 to TC-E2-014-12, all twelve in the legacy order |
| Decoupling patterns | DP01, DP03, DP05, DP06, DP07, DP09, DP10, DP11, DP13, DP19 |
| Architecture decisions | ADR-014 (schema and login per service), ADR-015 (Kafka with outbox, inbox and CloudEvents), ADR-020 (contract-first REST, one hop, 2 s timeout), ADR-021 (per-service Flyway), ADR-022 (local decision record plus central ledger) |
| Rules | R-LIT-03, R-LIT-04, R-UNI-14, R-UNI-39 |

The three supporting features of the legacy key — FEAT-APD-08 (approve demand and recall notices), FEAT-APD-04 (the rejection reason) and the template catalogue of FEAT-OCC-01 — are answered for the rwb-comms slice here and by rwb-decision for the approval slice, and this story changes neither design.

### 19. Out of scope

- The approval screen, its panels, the routing, the preparer rule, the input-age check, the reason rules and the decision entry: RWB-P7-E2014-APP, RWB-P7-E2013-APP and RWB-P7-E2014-CON.
- The composite route, its field list and its mask flags: RWB-PLT-N001-CON, with the screen contract of RWB-P7-E2014-CON.
- Notice generation from the template and the merge of the case facts: RWB-P6-E1052-APP and RWB-P6-E1052-CON.
- The template catalogue, the Legal approval and the withdrawal of a version: RWB-P6-E1046-APP and RWB-P6-E1046-CON. This story reads the state and never writes it.
- Dispatch to WIN, proof of delivery, the notice period and the hold reasons of the run: RWB-P6-E2021-APP.
- The `approval` and `decision_log_entry` rows and the central ledger: rwb-decision (P7, DP-03).
- The case facts, the case number and the case-owner task of a refusal: rwb-case (P3), read at the route.
- The total balance and the postal address that the panel shows: rwb-source-data (P1, DP-05), read at the route.
- Guarantor notices and statutory sale notices (Epic 5) and the approvals that carry an amount limit (Epic 3).
- The deployment, the alerts and the runbook of this legacy key: RWB-P7-E2014-OPS; the contract documents and the fakes: RWB-P7-E2014-CON and RWB-P6-E1052-CON.
