# RWB-S8-E2029-APP Deviation screening agent evaluation and L1 on one segment [E3b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E2029-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 2 |
| Business epic | EP03 |
| Release | 31 January 2027 (tentative) |
| Legacy key | RWB-E2-029 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-S8-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E2029-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (FR-S8-001, FR-S8-002, FR-S8-003, FR-S8-004, FR-S8-018, FR-S8-019, FR-S8-020, FR-S8-021, FR-S8-022, FR-S8-023, FR-S8-024, FR-S8-025, FR-S8-026, FR-S8-027, FR-S8-028, FR-S8-045, FR-S8-046, FR-S8-047, FR-S8-050, FR-S8-051, FR-S8-052, FR-S8-053, FR-S8-056) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-029 for rwb-deviation, carrying the one write the confirmation of a screening proposal causes in this service — the raise of the deviation with `raised_by` "SCREENING_AGENT" under R-DEV-01, its decision record and its event — together with the three guards the legacy story states (one open code per case, Case record right U, the version in force at mode L1). Applied: the plan's H row is None and the platform libraries of DP-03, DP-06, DP-07 and DP-09 and the edge route of DP-19 arrive with the service template; the legacy section 12 Java interface becomes the REST contract of DP-11 and the request is extended with the return point, the agent version and the segment pair the record and the gate need (GAP-3100; ASM-5298); and legacy AC1 to AC10 stay with RWB-P10-E2029-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **case owner (RW-CASEOWN)**, I want **rwb-deviation to take the deviation that the screening agent proposed and I confirmed as a deviation raise on the one segment where the agent is live at L1 — recording the decision first, allowing one open code per case and refusing every request outside that segment —** so that **the flag shows on the case and in every queue from the moment I confirm it, and the agent's feedback can name the record this service wrote**.

This story is the rwb-deviation part of legacy RWB-E2-029. In the legacy story the owner confirms or rejects each proposal on SCR-03, and on a confirmation "the system calls the S8 deviation service, which raises the deviation with raised_by SCREENING_AGENT and applies R-DEV-01" (legacy section 4 step 6), then stores feedback ACCEPTED "linked to the decision log entry S8 wrote" (step 7). Its section 12 publishes the interface this service exposes: `DeviationService.raise(caseId, deviationCode, reason, documentIds, raisedBy, agentRunId)`, returning the deviation id and the decision log entry id. Its AC7 and AC8 count deviations on the case, its AC9 fails the record, and its X8 refuses a role without Case record U.

Inside `rwb-deviation` this is the confirmed-proposal raise:

- Service `rwb-deviation`, schema `rwb_deviation`, REST base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with event names `rwb.deviation.<Event>.v1`, Temporal task queue `rwb-deviation` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.deviation` (context pack, service row).
- `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` is the legacy published interface turned into a contract with a fake (DP-11, DP-13): one hop, 2 s, `Idempotency-Key`, called under the case owner's identity by the confirmation step of the agent.
- The gate: the agent version a raise names must be the version in force for policy "SCREENING", status `LOADED`, mode `L1` for the segment pair the run carried (legacy BR1, AC1, AC3), read on the contract of RWB-P10-E2029-CON.
- The transaction: the `deviation` row, the local decision record, its `rwb.decision-record.v1` entry and the `rwb.deviation.DeviationRaised.v1` outbox row are written in one transaction and nothing of them survives alone (DP-03, DP-09).
- One open deviation per case and code: a partial unique index, so two confirmations of the same proposal leave one deviation and one event (legacy BR5, AC7, AC8).
- The raise hands the pause of R-DEV-01 to `DeviationWorkflow` on the service's queue: the stage timer pauses, the prescription timer keeps running, and the case status "On hold" is rwb-case's reaction to the event, never a write from here.

Not owned here: the agent run, the policy and its evaluation, the panel, the feedback row and the rejection path (RWB-P10-E2029-APP, which owns legacy AC1 to AC10), the interface itself (RWB-P10-E2029-CON), the officer's own raise and the timer display (RWB-S8-E2015-APP), the route rules and the handling flows (Epic 7 of this service), and the end-to-end proof (the ITG story of the key).

### 2. Business rationale

A proposal is worth nothing until the case carries the flag: the deviation pauses the stage clock, stops contact and routes the case to the person who owns the code, and the queue of the named handler only sees it once a `deviation` row exists. The legacy story measures the agent on 500 shadow cases and then lets the owner confirm a proposal on one segment; this slice is what happens at that click, and three target facts shape it.

1. **The raise is one write, and it is this service's.** `deviation` is S8's single table in `rwb_deviation` (context pack ownership rows; TSD S8 T3.1), and the Ownership Map gives the service this operation. A confirmation travels one hop into it and nowhere else: the agent writes no deviation, rwb-case writes no deviation, and no service reads the table (DP-01, DP-11).
2. **The record comes before the case moves.** CTL-07, R-UNI-39 and legacy BR4 make the decision log the precondition of the change, and legacy AC9 is the case where the record fails with "nothing stored". In the target the record, the row and the two outbox entries are one transaction, so a failed record leaves no deviation, no contact stop, no clock and no event (DP-03, DP-09).
3. **One deviation, one open code, one segment.** The owner may click twice, two sessions may confirm the same proposal, and the agent may run again on the same case: legacy AC7 and AC8 fix the outcomes as one deviation for the code and a refusal for the second request. And mode L1 is a policy fact for one segment only, so a raise that does not match it leaves the case untouched (legacy BR1, AC3).

The slice therefore supports REQ-DVH-006 (the row, the event and the route are what make the flag visible on the case and in every queue) and REQ-DVH-001 (the raise accepts exactly the codes of LOV-DEVIATION, from the case data, call notes and documents the run read). It changes no rule of the DEV route set, no policy of the agent and no state of the case.

### 3. Preconditions

- The `rwb_deviation` baseline is in place: `deviation` exists with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, loaded by the DB story of this service, and the outbox, inbox and idempotency tables of the platform event library exist in the schema.
- The service runs as its own login on `rwb_deviation` (DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case` or `rwb_agent` is refused by the database and fails the boundary test.
- RWB-P10-E2029-CON is published: the contract of this legacy key fixes the raise request and its answer, the policy read (agent "SCREENING", the version in force, its status, its segment pair and its autonomy mode) and the identity rule (the raise is made under the confirming person's identity, never the agent's). The operation name and field names of the policy read are Not specified in the source documents (GAP-3100; ASM-5299), and the story builds against its fake.
- The decision-record library and the `rwb.decision-record.v1` topic of DP-03 are on the service template, and the outbox and inbox library of DP-09 is on the template, with retry and `.dlt` conventions for `rwb.deviation.events.v1`.
- The reference-data contract of rwb-case is on the template (DP-07), with LOV-DEVIATION (X1 to X7) and LOV-RAISED-BY (SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT) at the version in force (TSD S8 T3.2).
- The parameters contract and client library of rwb-case are on the template (DP-06); this slice reads no business parameter of its own, because every value that shapes the raise is a policy row of rwb-agent read on its contract.
- The authorisation decision of rwb-access is consumed as the cached permission of the service (DP-08 arrives with the baseline and is not added to the H row): the raise needs Case record right U, applied to the scope of the caller (TSD S8 T-A.1).
- The policy "SCREENING" version "P2" is loaded in rwb-agent with status `LOADED`, segment MORTGAGE and BKK, the prompt "PR2" and the evaluation run of the 500-case shadow run, and RW-RISK has approved it — all of it rwb-agent's work in RWB-P10-E2029-APP; this slice only reads the version in force.
- `DeviationWorkflow` is deployable on queue `rwb-deviation`, and its pause step (the stage timer paused, the prescription timer untouched) is the service's existing behaviour of the raise path.

### 4. Flow

1. The case owner confirms X1 in the panel "Proposed deviations" (RWB-P10-E2029-APP). The confirmation step posts `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` under the owner's identity, with `deviationCode` "X1", `raisedBy` "SCREENING_AGENT", the agent run id, the agent version "SCREENING@P2/PR2", the reason, the document ids, the return point and the segment pair the run carried, and an `Idempotency-Key` (legacy section 4 steps 6 and 7; DP-11, DP-13).
2. `DeviationGuard` authorises the call from the cached decision of rwb-access (Case record right U, scope applied) and refuses with 403 and MSG-P4-002 before a row is read or written (legacy X8, TC-E2-029-11).
3. `RaiseValidator` checks the required fields and the two lists at the version in force: `deviation_code` in LOV-DEVIATION and `raised_by` in LOV-RAISED-BY (DP-07), and refuses with 422 and MSG-GEN-001 naming the field that is absent.
4. `PolicyVersionGate` reads policy "SCREENING" at its version in force on the contract of RWB-P10-E2029-CON and compares it with the request: same agent version, status `LOADED`, and autonomy mode `L1` for the segment pair the run carried. Where any of the three differs the request is refused with 409 and no message to a user: no row, no record, no contact stop, no clock and no event (legacy BR1, AC3).
5. `OpenCodeGuard` asks the service's own table whether the case already carries an open deviation of that code, and relies on the partial unique index for the case where two requests pass the check together (legacy BR5, AC7, AC8).
6. `DeviationRaiseService` runs `RecordAndApply` in one transaction: the local decision record with the final call `ACCEPTED`, the agent version and the reason; the `deviation` row with `raised_by` "SCREENING_AGENT", `raised_at` the business date and time, `paused_state` the return point sent, `contact_stop` true for X1 to X3, `handler_user_id` empty until the route step and `state` `DEV_FLAGGED`; the `rwb.decision-record.v1` outbox row; and the `rwb.deviation.DeviationRaised.v1` outbox row (DP-03, DP-09).
7. The answer returns 201 with the `deviationId`, the `decisionLogEntryId`, the state `DEV_FLAGGED` and the code, so the agent's own feedback row can name the record (legacy AC2, section 4 step 7); this service writes no feedback row.
8. `DeviationWorkflow` is started or continued on queue `rwb-deviation` for the case, with the deviation id: it pauses the stage timer at the return point while the prescription clock keeps running, and its route step assigns the named owner under R-DEV-02 to R-DEV-06 (legacy R-DEV-01; Temporal design slide 8).
9. The relay publishes `rwb.deviation.DeviationRaised.v1`; rwb-case moves the case to "On hold" and rwb-comms holds outbound contact where the stop applies. Neither is a call from this service.
10. A replay with the same `Idempotency-Key` answers the first result and writes nothing: the same `deviationId`, the same `decisionLogEntryId`, one event.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The calling identity holds no Case record right U for the case | Refused with 403 before any row is read or written; no record and no event | MSG-P4-002 | AC5, TC-E2-029-11 |
| X2 | `deviationCode` or `raisedBy` is absent, or either is not a value of its list at the version in force | Refused with 422; nothing is written | MSG-GEN-001 | AC1, section 14 |
| X3 | The named agent version is not the version in force, its status is not `LOADED`, or its mode is not `L1` for the segment pair carried | Refused with 409 and no message to a user; no row, no record, no contact stop, no clock, no event | None | AC2 |
| X4 | The case already carries an open deviation of the code, or a second confirmation passes the check at the same moment | The request is refused with 409; one deviation and one event remain | MSG-GEN-004 | AC3 |
| X5 | The decision record or its outbox row cannot be written | The transaction rolls back: 503, no deviation row, no event and no clock; an incident is raised under R-UNI-39 | MSG-P7-003 | AC4, TC-E2-029-12 |
| X6 | The policy read of RWB-P10-E2029-CON does not answer inside 2 s, so the version in force is unknown | Refused with 503 and the name of the system; the gate never falls back to raising | MSG-GEN-006 | Section 14 |
| X7 | The same request is replayed with the same `Idempotency-Key` | The first answer is returned; no second row, record or event | None | AC6 |
| X8 | A component, a statement or a test reaches a `recovery_case` row, a `rwb_agent` or `rwb_decision` table, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | Section 17, BR8 |

X1, X4 and X5 are the legacy paths carried onto the slice (legacy X8, X4 and X5 of the proposal, and legacy AC9); X2, X3, X6 and X7 are the paths the contract, the policy gate and the idempotency key add. The agent's own paths — a code outside X1 to X7 in the proposal, a low-confidence marker, a rejection without a reason, a failed policy load — are RWB-P10-E2029-APP's and are not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Writes only `rwb_deviation` and builds on Day 1 against the RWB-P10-E2029-CON fake, the reference-data and decision-record fakes and the platform libraries of the template; it waits for no in-lane story |
| Negotiable | The request field order, the operation name and the shape of the answer are this story's; the codes, the actor values, the segment pair and the policy are rows |
| Valuable | A confirmed proposal becomes the case's deviation, with one deviation per code, one record and one event, and the agent's feedback names the record this service wrote |
| Estimable | One operation, three guards, one transaction, one index and one workflow hand-off |
| Small | Fits one sprint as a secondary slice of the legacy key, beside RWB-P10-E2029-APP and the contract RWB-P10-E2029-CON |
| Testable | Every criterion runs on synthetic cases, synthetic policies and one forced record failure through the contract fakes, plus the access, gate, duplicate and replay cases |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent evaluation and L1 on one segment [E3b] — the confirmed-proposal raise in rwb-deviation

  Background:
    Given the rwb-agent contract mock returns policy "SCREENING" version "P2" with prompt "PR2", status "LOADED", mode "L1" for segment MORTGAGE and BKK and mode "SHADOW" for every other segment
    Given the rwb-case reference-data contract mock returns LOV-DEVIATION with X1 to X7 and LOV-RAISED-BY with SCREENING_AGENT, RULE, OFFICER and CUSTOMER_CONTACT
    Given the rwb-access decision mock grants Case record right U to the case owner "owner.user07" for the case of the request

  Scenario: AC1 A confirmed proposal becomes the case's deviation (new, D-RCV-60)
    Given the owner confirms X1 on Mortgage case "RW-2027-000801" in region BKK with the return point "WITH_FCR_OFFICER"
    When the confirmation posts deviationCode "X1", raisedBy "SCREENING_AGENT", agent version "SCREENING@P2/PR2", the agent run id, the reason and the run's segment pair
    Then one deviation exists with code "X1", raised_by "SCREENING_AGENT", state "DEV_FLAGGED", the return point sent and contact_stop true
    Then one decision record holds the final call "ACCEPTED", the agent version and the reason, written in the same transaction as the deviation row
    Then the answer is 201 with the deviationId and the decisionLogEntryId of that record
    Then one rwb.deviation.DeviationRaised.v1 outbox row names the deviation and carries no reason text and no personal data
    Then this service writes no agent_feedback row

  Scenario: AC2 Nothing is raised outside the L1 segment (new, D-RCV-60)
    Given hire purchase case "RW-2027-000802" in region BKK and the segment pair the run carried for it
    When the confirmation posts the raise for that case under policy "SCREENING" version "P2"
    Then the request is refused with status 409 and no message to a user
    Then no deviation row, no decision record and no contact stop exist for the case
    Then no rwb.deviation.DeviationRaised.v1 outbox row exists and no clock moved
    Then the same request with the segment pair MORTGAGE and BKK and mode "L1" is accepted
    Then a raise that names an agent version other than the version in force is refused with 409 in the same way

  Scenario: AC3 One open deviation for one code on one case (new, D-RCV-60)
    Given deviation "X1" is open on case "RW-2027-000801"
    When a confirmation posts deviationCode "X1" for case "RW-2027-000801"
    Then the request is refused with status 409 and MSG-GEN-004
    Then one deviation "X1" exists on the case and one event has been written for it
    Given two sessions of "owner.user07" confirm X1 on case "RW-2027-000804" at the same time
    When both requests arrive
    Then one deviation "X1" exists and the second request is refused with 409 and MSG-GEN-004
    Then exactly one rwb.deviation.DeviationRaised.v1 outbox row names the deviation

  Scenario: AC4 The record is written first and nothing survives without it (new, D-RCV-60)
    Given the decision record of the raise cannot be written
    When the confirmation posts deviationCode "X6" for case "RW-2027-000801"
    Then the request is refused with status 503 and MSG-P7-003
    Then no deviation row exists for the request, no decision record exists and no rwb.deviation.DeviationRaised.v1 outbox row exists
    Then no contact stop is set and no clock moved
    Then an incident is raised under R-UNI-39

  Scenario: AC5 The agent's own identity raises nothing (new, D-RCV-60)
    Given the rwb-access decision mock returns no Case record right U for the identity "SY-AGENT", which holds Case record right R only
    When that identity posts a confirmation for case "RW-2027-000801"
    Then the call is refused with status 403 and MSG-P4-002
    Then no deviation row and no decision record exist
    Then the same request under the owner's identity with Case record right U is accepted

  Scenario: AC6 A replay answers the first result (new, D-RCV-60)
    Given the confirmation of AC1 answered with a deviationId and a decisionLogEntryId
    When the same request is replayed with the same Idempotency-Key
    Then the answer carries the same deviationId and the same decisionLogEntryId with 200
    Then one deviation exists and one event has been written
    Then no second decision record and no second outbox row is written
```

The six criteria are new and test only this slice: the raise a confirmed proposal causes in `rwb-deviation`, its record and event, and the four guards around it. The legacy criteria AC1 to AC10 of RWB-E2-029 are owned word for word by RWB-P10-E2029-APP (the evaluation, the L1 panel, the other segments on the agent side, the rejection with and without a reason, the low-confidence marker, the code already open on the panel, the two confirmations on the panel, the rejected-record case and the condition on the scores), and no legacy criterion text is copied here. Five legacy values are reused because the sources publish them: the call `PR2`, the policy "P2" with status `LOADED` and segment MORTGAGE and BKK (legacy AC1), the agent version "SCREENING@P2/PR2" (legacy AC4), the return point "WITH_FCR_OFFICER" (FSD S8 AC-ALT-S8-002-01) and the cases `RW-2027-000801`, `-802` and `-804` (legacy AC2, AC3, AC8). Two points are recorded rather than smoothed over: the request is wider than the legacy Java signature, because the record needs the agent version and the gate needs the segment pair (GAP-3100; ASM-5298), and the case status "On hold" is asserted nowhere here because it is rwb-case's reaction to the event (ASM-5304).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A confirmation causes one write in this service and no other: the `deviation` row of the case, written in `rwb_deviation` only, with no read and no key of another service's table | DP-01, DP-11; context pack ownership rows; TSD S8 T3.1, T3.3 |
| BR2 | The decision record is written before the case moves and in the same transaction as the row and the event; where the record fails, nothing is stored, 503 is answered and an incident is raised | Legacy BR4, AC9, X6; CTL-07; R-UNI-39; DP-03 |
| BR3 | One open deviation per case and code: a code already open is refused, and of two simultaneous confirmations only one leaves a deviation and an event | Legacy BR5, AC7, AC8, X4; `deviation.deviation_code` |
| BR4 | The agent raises nothing itself: the raise is made under the confirming person's identity with Case record right U, and an identity holding the agent's read right only is refused | Legacy BR2, AC2, X8; legacy section 10; TSD S8 T6.1 (SY-AGENT: Case record R) |
| BR5 | A raise is accepted only where the agent version it names is the version in force for policy "SCREENING", its status is `LOADED` and its mode is `L1` for the segment pair the run carried; every other segment is refused and the case is untouched | Legacy BR1, AC1, AC3; agent_policy.autonomy_mode, segment_product_group and segment_region_code are rwb-agent's rows |
| BR6 | `deviation_code` and `raised_by` are values of LOV-DEVIATION and LOV-RAISED-BY at the version in force; no code, actor value, segment or floor is a constant, a default or a branch of the module | FSD S8 BR-S8-001, BR-S8-002; TSD S8 T3.1, T3.2; DP-07 |
| BR7 | The event carries references, codes, a boolean and dates: no reason text, no document content, no person name, no contact value and no handler identity | Template and Rules §R7.2 (s17); TSD S8 T6.2 |
| BR8 | No foreign key leaves `rwb_deviation`, no statement reaches another `rwb_*` schema and no `v_ace_*` view is read by this slice; `case_id` and the run id are references | DP-01, DP-05; ADR-014 |

BR1 and BR8 are executed by the same boundary test: a statement on `rwb_case`, `rwb_agent` or a `v_ace_*` view fails the build, and a foreign key across schemas fails the migration check. BR2 is executed by `RecordAndApply`, which writes the record, the row and both outbox entries in one transaction: the forced-failure test of AC4 asserts that none of the four survives. BR3 is executed by the partial unique index and by the guard in front of it, so the guard is a courtesy for the message and the index is the truth of legacy AC8. BR4 is executed by the guard of the operation with the caller's own identity: no shared agent identity exists, and the service never takes the right from a header or a claim the caller controls. BR5 is executed by `PolicyVersionGate` on the contract read, never on a cached copy of the policy in `rwb_deviation`.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_STATE | DEVIATION_FLAGGED | A person confirms a proposal of the screening agent; the version in force is `LOADED` at mode `L1` for the segment; the code is not open | DEV_FLAGGED (R-DEV-01) |
| DEV_FLAGGED | OWNER_ASSIGNED | The route step of `DeviationWorkflow` applies R-DEV-02 to R-DEV-06 for the code | DEV_WITH_OWNER |
| DEV_FLAGGED, DEV_WITH_OWNER | — | A raise is refused: the segment, the version, the code or the record | No change: no row, no event, no clock |
| — | A proposal is rejected rather than confirmed | No call reaches this service | No change on the case |

The table is the head of the DEV state machine of TSD S8 T4: this story enters it at R-DEV-01 and stops at `DEV_FLAGGED`, and the states after the route step are the handling flows of the Epic 7 stories. The case status "On hold" is not a transition of this service — it is rwb-case's reaction to `rwb.deviation.DeviationRaised.v1` (legacy AC2; ASM-5304), and the pause of the stage timer with the prescription clock left running is the workflow step this raise starts (Temporal design slide 8).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-CASEOWN, case owner | Case record CRU (TSD S8 T6.1): confirms a proposal and, on that confirmation, the raise is accepted under the owner's own identity |
| SY-AGENT, agent platform | Case record R only: runs the agent and proposes; holds no right to raise, so its own identity is refused by the operation (AC5) |
| rwb-deviation service identity (the service login, DP-02) | Writes the `deviation` row, the decision record and the outbox rows of `rwb_deviation`; reads the two policy and reference contracts; holds no grant on another schema |
| RW-PHONECOL, phone collector, and every role with Case record R only | Reads the case and the deviation; its confirmation request is refused with MSG-P4-002 (legacy TC-E2-029-11) |
| RW-COE, center of excellence analyst, and RW-RISK, risk and model risk officer | Own the evaluation and the approval of the L1 proposal in rwb-agent (`Rules and parameters` C and A); this slice reads the result of their approval and grants them nothing of its own |
| RW-FRAUD, RW-SPECIAL, RW-COMPLAIN, RW-LEGAL, RW-TEAMMGR | The roles a code routes to after this raise: they see the deviation in their queue and hold the rights the matrix gives them; this story assigns nothing beyond the route step |
| RW-AUDIT, RW-COMPLY, RW-PLATADM | Read the deviation, the decision record or the platform state of the service as the matrix gives it; no write of their own |

The rights are the rows of TSD S8 T6.1 and the declared right of the operation in TSD S8 T-A.1 (Case record, right U, scope applied). DP-08 is not in this story's pattern set: the authorisation decision is rwb-access's and is consumed as the cached permission the service template already carries, so the check is stated here and not built here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Write, the deviation reference of the answer |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Write from the path, and read by the open-code guard |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Write, and read by the open-code guard |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Write, the business date and time of the raise |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Write, "SCREENING_AGENT" from LOV-RAISED-BY |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Write, the return point the confirmation sent |
| DF-CAS-042 | deviation (S8, `rwb_deviation`) | handler_user_id | Written empty by this story and set by the route step |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Write, true for X1 to X3 (FEAT-DVH-05) |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Empty at the raise; written by the clear step |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (P7, through the DP-03 library) | all fields | Write one entry in the same transaction: final call `ACCEPTED`, agent version, reason, correlation id |
| DF-AGT-036 | agent_run (P10) | id | Carried on the request as a reference and recorded; never read as a table |
| DF-AGT-038 | agent_run (P10) | agent_version | Carried on the request ("SCREENING@P2/PR2") and written on the record |
| DF-AGT-009, DF-AGT-010 | agent_policy (P10) | segment_product_group, segment_region_code | Read on the contract as the segment pair of the version in force, compared with the pair the request carries |
| DF-AGT-008 | agent_policy (P10) | autonomy_mode | Read on the contract in the gate; never copied into `rwb_deviation` |
| DF-REF-002 to DF-REF-010 | rule_row (P7, in the package) | rule_id, owner_role | Not read here: the route step of the workflow owns them |
| DF-CAS-005, DF-CAS-012 | recovery_case (P3) | status, region_code | Not read and not written: the case row is rwb-case's, and "On hold" is its reaction to the event |
| DF-ACE-193 | v_ace_valuation (P1) | appraisal_date | Not read here: the appraisal date is the X7 input of the agent, not of the raise (DP-05; GAP-3100; ASM-5301) |
| DF-AGT-098 to DF-AGT-102 | agent_feedback (P10) | agent_run_id, item_key, verdict, reason, decision_log_id | Not written here: the feedback row is rwb-agent's and names the `decisionLogEntryId` this service returns |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary. **One table written (`deviation`), no new column** and one migration step for the partial unique index that makes legacy AC8 true for an open code (ASM-5302). The decision record is the library's table in `rwb_deviation`, and the outbox, inbox and idempotency tables are the platform's in the same schema.

No personal data. The row and the event carry identifiers, codes, a boolean, dates and a version; the reason is free text and stays in the decision record, and it is masked on the screens of the panel. No name, address, contact value or identity number enters the row, the event, a log, a trace or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13); the legacy published interface becomes this contract with a fake (DP-11).

| Method | Path | Request | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| POST | `/cases/{caseId}/deviations` | `DeviationRequest` | `Deviation` with `decisionLogEntryId` | Case record right U, scope applied | `Idempotency-Key` header required |

`DeviationRequest` carries `deviationCode` (a value of LOV-DEVIATION), `raisedBy` (a value of LOV-RAISED-BY), `reason`, `documentIds`, `agentRunId`, `agentVersion`, `pausedState`, `segmentProductGroup` and `segmentRegionCode`. The answer carries `deviationId`, `caseId`, `deviationCode`, `state` (`DEV_FLAGGED`), `raisedAt`, `raisedBy`, `pausedState`, `contactStop` and `decisionLogEntryId`, which are the TSD S8 T3.1 columns of `deviation` plus the record id the legacy return publishes. Errors: 401 no Workbench identity; 403 Case record right U absent (MSG-P4-002) or case outside the scope; 409 the gate of BR5 (no user message) or a code already open (MSG-GEN-004); 422 a missing or unknown field (MSG-GEN-001); 503 the record cannot be written (MSG-P7-003) or the policy does not answer (MSG-GEN-006). A replay with the same `Idempotency-Key` answers 200 with the first result.

The request is wider than the legacy Java signature, which carries `caseId`, `deviationCode`, `reason`, `documentIds`, `raisedBy` and `agentRunId` only: `agentVersion` is added so the record can name the version in force (legacy AC4 writes "SCREENING@P2/PR2"), `pausedState` so the required column DF-CAS-041 is the return point the person saw, and the segment pair so the gate of BR5 can compare it with the policy row. The addition is recorded as a gap and an assumption (GAP-3100; ASM-5298). The second operation of the Ownership Map, `PATCH /deviations/{deviationId}`, is the clear step of the handling stories and is untouched here.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The agent policy read of RWB-P10-E2029-CON (operation name Not specified in the source documents (GAP-3100; ASM-5299)) | `/api/recovery/agent/v1` | P10 rwb-agent | The version in force for policy "SCREENING": its status, its mode and its segment pair, for the gate of BR5; faked, one hop, 2 s |
| The reference-data read (operation name Not specified in the source documents (GAP-3100; ASM-5299)) | `/api/recovery/case/v1` | P3 rwb-case | LOV-DEVIATION and LOV-RAISED-BY at the version in force; faked, cached |

Both rows are one hop with a 2 s timeout and a breaker per downstream (ADR-020). The second is a class C dependency in fact that the plan does not hold, because this story's C row is `RWB-P10-E2029-CON` and its H row is None; the reference-data contract arrives with the platform library of DP-07 (GAP-3100; ASM-5300). The parameters contract of DP-06 is on the template and this slice reads no value of it, and no other service is called: the case row, the documents and the agent run are not read here.

#### 12.3 Events published

| Event | Topic | Envelope | Payload |
|---|---|---|---|
| `rwb.deviation.DeviationRaised.v1` (EV-06) | `rwb.deviation.events.v1` with retry and `.dlt` | CloudEvents, outbox, relay; the event id is the outbox key | `deviationId`, `caseId`, `deviationCode`, `raisedBy`, `raisedAt`, `pausedState`, `contactStop`, `decisionLogEntryId`, `agentRunId` |
| The decision-record entry of DP-03 | `rwb.decision-record.v1` (shared, P7) | CloudEvents through the same outbox, one entry per decision | The record id, the decision, the final call `ACCEPTED`, the agent version, the correlation id |

The payloads carry references, codes, a boolean, dates and a version and no reason text, no document content and no person data (BR7): the reason is free text and stays in the decision record. The two rows are written in the same transaction as the deviation row, so a raise that fails leaves neither of them (BR2). The event family is the service's one family for the raise; the envelope type name of the decision-record entry is the library's and is Not specified in the source documents (GAP-3100; ASM-5303).

#### 12.4 Events consumed

None. The raise arrives on the request, in the caller's thread: this slice subscribes to no topic, holds no consumer group and writes no inbox row, and the case router in rwb-case is the consumer of the event this story publishes. The inbox table of DP-09 is present in `rwb_deviation` for the consumers other stories of this service add.

#### 12.5 Workflows and activities

| Workflow | Queue | What this story does with it |
|---|---|---|
| `DeviationWorkflow` | `rwb-deviation`, namespace `rwb-recovery` | Started or continued by the raise with the case and the deviation id (workflow id `deviation-{caseId}`) |

The workflow applies R-DEV-01 after the commit: it pauses the stage timer at the return point while the prescription timer keeps running, then its route step assigns the named owner under R-DEV-02 to R-DEV-06 and takes the deviation to `DEV_WITH_OWNER`, then waits for the next signal. Its four steps are the platform pattern of Temporal design slide 13 (receive, evaluate, record and apply, wait); this slice adds the start and nothing of the rules, and the activities it relies on are the service's existing ones. The case workflow `CaseWorkflow` on queue `rwb-case` is rwb-case's and receives the same fact through the case router, never as a call from here.

#### 12.6 Schedules

None. The raise is request-driven and the service owns no job in the ownership rows (Jobs 0). The escalation timer of R-DEV-20 and every deviation service level are workflow timers of the handling stories, not a Temporal Schedule of this slice.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | Written: one row per confirmed proposal; read by the open-code guard |
| decision_record | PLT library, created in `rwb_deviation` | Written: one local record per raise, with its final call and agent version |
| outbox_event | PLT library, created in `rwb_deviation` | Written: one row for `rwb.deviation.events.v1` and one for `rwb.decision-record.v1` |
| processed_event | PLT library, created in `rwb_deviation` | Present for the consumers of other stories; this slice writes none of its rows |
| idempotency_key | PLT library, created in `rwb_deviation` | Written: the `Idempotency-Key` of the request and its first answer |

The migration of this story is one step in the per-service Flyway sequence of `rwb_deviation`: the partial unique index on `deviation (case_id, deviation_code)` where `cleared_at` is null. Not owned and never read as a table: `recovery_case` (P3), the `v_ace_*` views and the interaction ledger (P1), `document` (P5), `agent_policy`, the agent run and `agent_feedback` (P10 `rwb_agent`), `rule_row` and the decision rows of the central ledger (P7).

#### 12.8 Contract fakes

| Fake | Documents | Used by |
|---|---|---|
| RWB-P10-E2029-CON agent fake | Policy "SCREENING" version "P2" with status `LOADED`, prompt "PR2", mode `L1` for MORTGAGE and BKK and `SHADOW` elsewhere; a version not in force; a status other than `LOADED`; no answer beyond 2 s | AC1, AC2, X3, X6 |
| rwb-case reference-data fake | LOV-DEVIATION with X1 to X7 and LOV-RAISED-BY at the version in force; a code and an actor value that have left the version | AC1, X2 |
| rwb-access decision fake | A granted Case record right U for the owner, a refused decision for an identity with R only, and a scope that excludes one case | AC5, X1 |
| rwb-decision decision-record fake | The library's record and the `rwb.decision-record.v1` entry; a forced failure of the write | AC1, AC4 |
| gateway-bff composite route fake | The deviation of the case as SCR-03 and SCR-08 see it after the raise | AC1, AC3 |

The fakes are test-only and are replaced by the real services in SIT. No fake carries personal data: every case, reason and document id in the fixtures is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 2 consumed | `POST /cases/{caseId}/deviations` on `/api/recovery/deviation/v1`; the agent policy and the reference data, each one hop with 2 s and a breaker |
| Kafka | 2 published, 0 consumed | `rwb.deviation.DeviationRaised.v1` (EV-06) on `rwb.deviation.events.v1`; the decision-record entry on `rwb.decision-record.v1` |
| Temporal | 1 workflow, 0 schedules | `DeviationWorkflow` on queue `rwb-deviation`: the pause and the route of R-DEV-01 |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `deviation-raise`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationController` | REST | The operation of 12.1, the problem mapping of section 14 and the idempotency key |
| `DeviationGuard` | Guard | Case record right U and the scope, from the cached decision of rwb-access |
| `RaiseValidator` | Service | The required fields and the two lists at the version in force (DP-07) |
| `PolicyVersionGate` | Service | Compares the named agent version, its status and its mode for the segment pair with the policy in force on the contract of RWB-P10-E2029-CON |
| `OpenCodeGuard` | Repository | The open code of the case in `deviation`, and the translation of the unique-index violation into 409 and MSG-GEN-004 |
| `DeviationRaiseService` | Service | `RecordAndApply`: the record, the row, the decision-record entry and the event in one transaction (DP-03, DP-09) |
| `DecisionRecordWriter` | Client of the library | The local record and the `rwb.decision-record.v1` outbox row, with the correlation id of the answer |
| `DeviationWorkflowStarter` | Client | Starts or continues `DeviationWorkflow` on `rwb-deviation` after the commit |
| `AgentPolicyClient` | Client | The policy read of RWB-P10-E2029-CON, one hop, 2 s, breaker, cached for the request |
| `ReferenceDataClient` | Client | LOV-DEVIATION and LOV-RAISED-BY at the version in force, cached |

**Database and migrations.** One step in the per-service Flyway sequence of `rwb_deviation`: `V2029_1__deviation_raise_index.sql`, the partial unique index on `deviation (case_id, deviation_code)` where `cleared_at` is null, which makes the one-open-code rule of BR3 true under two simultaneous requests. No table and no column is added, the decision-record table comes from the DP-03 library, and no migration of this service touches another schema. The index name is a design choice no source document fixes (ASM-5302).

**Configuration and reference data.**

- The codes, the actor values and the segment pair are rows of LOV-DEVIATION, LOV-RAISED-BY and the policy of rwb-agent at their version in force; none is a constant of the module (DP-07, BR6).
- Policy "SCREENING", its version "P2", its status, its mode and its segment pair are rwb-agent's data and are read on its contract; this service keeps no copy of them (DP-11).
- The confidence floor 0.80, the prompt "PR2" and the evaluation run are rwb-agent's and are not read here: the raise carries no confidence.
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020, and `rwb.deviation.screening-raise` is a flag of the platform library: off means the gate refuses every raise naming "SCREENING_AGENT" with 409 while the officer's own raise is unchanged.

**Build steps**

1. The migration step and the index on a loaded and an empty `rwb_deviation` (BR3, AC3).
2. `RaiseValidator` over the reference-data fake, with a code and an actor value that have left the version in force; unit tests for X2.
3. `PolicyVersionGate` over the agent fake, in the four states (in force at L1, not in force, not `LOADED`, `SHADOW` for the pair) and with no answer; tests for AC2, X3 and X6.
4. `DeviationGuard` with the granted and refused decisions, the scope and the agent's read-only identity; tests for AC5 and X1.
5. `RecordAndApply` with the record, the row, the two outbox rows and the forced record failure; tests for AC1, AC4 and X5.
6. `OpenCodeGuard` and the index under two simultaneous requests; tests for AC3.
7. The idempotency path and its replay; test for AC6.
8. `DeviationWorkflowStarter` and the pause at the return point on the workflow fake, plus the property test that the reason and a synthetic personal value appear in no event and no log (BR7).
9. The contract-fake run of RWB-P10-E2029-CON so the slice proves every criterion before the agent is live at L1 in DEV.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

This is a secondary slice: the metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P10-E2029-CON` exactly as the Work Package fixes them, so the four platform contracts that DP-03, DP-06, DP-07 and DP-09 name and the edge route of DP-19 arrive with the service template and are not written into the H row (GAP-3100; ASM-5300).

- **DP-11** is the core of the story: the legacy in-process `DeviationService.raise` becomes a REST operation with a mock, one hop and a 2 s timeout, so the confirmation of a person in rwb-agent reaches this service through its published contract and not through a shared library. **DP-13** gives it the service base, and **DP-19** is the route a screen reads the same deviation through after the raise.
- **DP-03** is the record before the change: the local library writes the record with the final call, the agent version and the correlation id, and puts it on the shared topic in the same transaction — which is what makes legacy AC2's "linked to the decision log entry S8 wrote" a single fact and legacy AC9's failure a clean rollback.
- **DP-09** is the row, the record and the event in one outbox: one fact, one owner, one transaction. The inbox is present and this slice consumes nothing.
- **DP-07** is the two lists at the version in force, which is what keeps the codes and actor values out of the code; **DP-06** is on the template and no business parameter is read by this slice, because the values that shape the raise are policy rows of rwb-agent (BR6).
- **DP-05** is a boundary and not a read: the appraisal date of X7 (DF-ACE-193) is the agent's input, this service holds no `v_ace_*` grant, and ACE data reaches the Workbench only through rwb-source-data or the service's own views where another story needs it.

**Done when.** The tests of section 16 pass, a confirmation of X1 on `RW-2027-000801` leaves one deviation with `raised_by` "SCREENING_AGENT", one record and one event with the identifiers returned, a raise outside the L1 segment leaves nothing, two simultaneous confirmations leave one deviation and one event, a forced record failure leaves nothing and answers 503 with MSG-P7-003, the agent's own identity is refused with MSG-P4-002, the index applies cleanly on an empty `rwb_deviation`, and no statement outside the schema exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's identity holds no Case record right U (X1, AC5) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required field is absent or is not a value of its list (X2) | Enter {field}. |
| MSG-GEN-004 | The case already carries an open deviation of the code (X4, AC3) | Someone else changed this record. Reload it to see their change. |
| MSG-P7-003 | The decision record cannot be written (X5, AC4) | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-GEN-006 | The policy read does not answer inside the budget (X6) | {system} is not available. Your request is queued and will be retried. |
| MSG-S8-001 | After the raise, on the case record and in the queue (AC1) | {deviation} was raised. The case is with {handler}. |
| None | A raise outside the L1 segment, a replay and the index race (X3, X7, half of X4) | No message: no user is in the loop for the gate, and the panel shows the proposal as not raised |

The six IDs and their text are those of the legacy and FSD message sets, copied unchanged. For MSG-P4-002, {action} names the action the caller tried — "raise this deviation" — and never a case fact. For MSG-GEN-006, {system} is "Agent policy" on the gate path. For MSG-S8-001, {handler} is the role the route step assigned and the message is shown by the screens of section 15, not returned by the raise. Errors are RFC 9457 problem responses with `messageId`, `detail` with the placeholders filled and `instance` naming the request; the HTTP mapping is 403 for MSG-P4-002, 409 for the gate and MSG-GEN-004, 422 for MSG-GEN-001, and 503 for MSG-P7-003 and MSG-GEN-006. MSG-P7-005 and MSG-P10-001 (the reason of a rejection and a refused policy load) are RWB-P10-E2029-APP's and are not restated here.

### 15. Screens and states

No screen is built by this story: the confirmation happens in the panel "Proposed deviations" of SCR-03, which is rwb-agent's (RWB-P10-E2029-APP), and the raise is its call. What this story feeds is the after-state of the flag:

| Screen | State after a raise | Owner of the screen |
|---|---|---|
| SCR-03 Case record | The on-hold banner of the deviation with MSG-S8-001 naming the code and the handler role; the panel keeps the verdict `ACCEPTED` with its date | gateway-bff composite route (DP-19); panel in rwb-agent |
| SCR-08 Deviation queue | The deviation listed for the named handler with its code, raised date, contact stop and return point | This service, through the composite route |
| SCR-46 Agent monitor | SCREENING shown live for MORTGAGE and BKK and shadow elsewhere; no state of it is written here | rwb-agent |

A raise that is refused leaves the panel as it was: the proposal stays confirmable where the refusal is a race (MSG-GEN-004), and it is not raised at all where the gate refused. SCR-06 Raise deviation is the officer's own raise and is RWB-S8-E2015-APP's.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-029-11 | AC5: the raise needs Case record right U on the confirming person's identity; the agent's read-only identity and a phone collector's identity are refused | Component | RW-PHONECOL confirms X1; refused with 403 and MSG-P4-002; the owner's identity is accepted |
| TC-E2-029-01 | No criterion here: the evaluation of 500 shadow cases and its scores are RWB-P10-E2029-APP's, and this service raises nothing for an evaluation | Component | SCREEN-S2 version 1, 500 cases; X1 counts 41, 4, 5; precision 0.9111 and recall 0.8913 |
| TC-E2-029-02 | AC1 and AC2: one deviation X1 with `raised_by` "SCREENING_AGENT" under R-DEV-01, one record, one event and the two identifiers returned. The panel and the feedback row are RWB-P10-E2029-APP's | Component | Mortgage case RW-2027-000801 in BKK, complaint note 2027-01-26, policy P2 `LOADED` at L1 for MORTGAGE and BKK |
| TC-E2-029-03 | AC2: a raise whose segment pair is not the L1 pair of the version in force is refused and leaves the case untouched | Component | Hire purchase case RW-2027-000802 in BKK; mode `SHADOW` for that pair |
| TC-E2-029-04 | No criterion here: a rejection raises nothing and never reaches this service; its record is rwb-agent's | Component | Reject X6 with a reason |
| TC-E2-029-05 | No criterion here: the required reason of a rejection is enforced by rwb-agent | Component | Reject X6 with an empty reason |
| TC-E2-029-06 | No criterion here: the floor and the "Low confidence" marker are the agent's, and a raise carries no confidence value | Component | X2 with confidence 0.72 |
| TC-E2-029-07 | AC3: a code already open on the case is refused, so the raise of a second X1 leaves one deviation | Component | X1 already open on case RW-2027-000801 |
| TC-E2-029-08 | AC3 and AC6: two parallel confirmations of X1 leave one deviation, one event and one record; the second is 409 with MSG-GEN-004 | Component | Two sessions of owner.user07 confirm X1 on RW-2027-000804 at the same time |
| TC-E2-029-09 | AC4: the record fails first, so no deviation row, no record, no event, 503 and MSG-P7-003 | Component | Decision record write forced to fail on a raise of X6 |
| TC-E2-029-10 | No criterion here: the L1 proposal and its conditions are loaded in rwb-agent; this service reads only the mode in force | Component | X4 recall 0.6000, condition 0.75 |
| TC-E2-029-12 | AC4 under forced and repeated failure: nothing stored, MSG-P7-003, incident raised under R-UNI-39 | NFR | Record write forced to fail twice; the row, the record and both outbox rows absent |

The twelve legacy cases of RWB-E2-029 are listed in the order the Work Package gives them, with the Level column added, and each names the slice of behaviour this story answers: the raise and its record for TC-E2-029-02, the segment gate for TC-E2-029-03, the duplicate rule for TC-E2-029-07 and TC-E2-029-08, the failed record for TC-E2-029-09 and TC-E2-029-12, and the authority for TC-E2-029-11; the remaining cases are the agent's and are listed with no criterion here. The legacy table publishes no level, so one is assigned per case: legacy "System" maps to Component for a single-service half, "Access" to Component, and "Resilience" to NFR (GAP-3100; ASM-5305). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written here: the same values across rwb-agent, rwb-case, rwb-deviation and rwb-access are the ITG story of this legacy key.

### 17. Guardrails

- No business value in code: the codes, the actor values, the segment pair, the policy version, its status and its mode are rows read at the version in force. A build check fails on a code, an actor value or a segment literal in the source.
- No personal data in a row, an event, a workflow input or a log: identifiers, codes, a boolean, dates and a version only. The reason is free text in the decision record, and a property test asserts that it and a synthetic personal value never reach the event, a log line or a span attribute.
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant, the raise reads no ACE product, and the appraisal date of X7 is the agent's input (DP-05).
- No cross-schema read and no cross-schema key: `rwb_deviation` holds the row, `case_id` and the run id are references, and a statement on `rwb_case`, `rwb_agent` or `rwb_decision` fails the boundary test (DP-01).
- The record is never after the change: the record, the row and both outbox rows are one transaction, and a build that writes the row first fails the acceptance test (BR2, DP-03).
- One event owner per fact: the raise publishes `rwb.deviation.DeviationRaised.v1` and the decision record only, and rwb-case and rwb-comms react to the event instead of being called (DP-09).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- The agent runtime is never embedded and never called back: this service reads the policy on the contract of RWB-P10-E2029-CON and writes no run, no feedback and no policy row.
- Any migration is a step in the per-service Flyway sequence of `rwb_deviation`, versioned and repeatable, and touches no other schema.
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base, no data-lake export and no cross-module Java interface.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases |
|---|---|---|---|
| REQ-DVH-006 | A deviation flag is visible on the case and in every queue (Business Requirements Program, section 5.15; FEAT-DVH-07) | The raise writes the row, the record and `rwb.deviation.DeviationRaised.v1` in one transaction, so rwb-case sets "On hold" and the queue of the named handler lists the code | TC-E2-029-02, TC-E2-029-07, TC-E2-029-08 |
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags (FEAT-AGT-08, FEAT-DVH-07) | The raise accepts exactly the codes of LOV-DEVIATION with `raised_by` "SCREENING_AGENT", and the confirmation carries the document ids the proposal was based on | TC-E2-029-02, TC-E2-029-03, TC-E2-029-09, TC-E2-029-12 |
| D-RCV-60 DP-01 | The row is this service's, and no other service's table is read | `deviation` in `rwb_deviation`, the boundary test | TC-E2-029-02, TC-E2-029-07 |
| D-RCV-60 DP-03 | The decision is recorded locally and on the shared topic before the case moves | `DecisionRecordWriter` and `RecordAndApply` | TC-E2-029-02, TC-E2-029-09, TC-E2-029-12 |
| D-RCV-60 DP-11 | The legacy in-process interface becomes a REST contract with a mock | `POST /api/recovery/deviation/v1/cases/{caseId}/deviations` and the agent fake | TC-E2-029-02, TC-E2-029-11 |
| D-RCV-60 DP-13 | The operation is served on the base of the service | The path of 12.1 | TC-E2-029-02 |
| D-RCV-60 DP-19 | The screens read the same deviation through the edge | The composite route of section 15 | TC-E2-029-02 |

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E2-029 — the confirmation that raises through S8 (section 4 steps 6 and 7; section 12 published interface; BR1 to BR5; AC2, AC3, AC7, AC8, AC9; X8) | Sections 1, 4, 7, 8, 9, 11, 12 and 16 |
| Legacy values reused — policy "SCREENING" "P2" `LOADED` at L1 for MORTGAGE and BKK, prompt "PR2", agent version "SCREENING@P2/PR2", return point "WITH_FCR_OFFICER", cases RW-2027-000801 to RW-2027-000804, date 2027-01-26 | Background, sections 3 to 16 |
| MSG-P4-002, MSG-GEN-001, MSG-GEN-004, MSG-P7-003, MSG-GEN-006, MSG-S8-001 | Section 14, exception paths |
| TC-E2-029-01 to TC-E2-029-12 | Section 16 |
| Legacy criteria AC1 to AC10 | Owned by RWB-P10-E2029-APP; not restated here (section 7) |

### 19. Out of scope

- The agent runtime, policy "SCREENING" and its versions, prompt "PR2", the sample "SCREEN-S2", the evaluation and its scores, the confidence floor, the panel "Proposed deviations", the "Low confidence" marker, the feedback row and the rejection path: RWB-P10-E2029-APP and the contract RWB-P10-E2029-CON.
- The interface itself, its operation name, its field names and the policy read of the contract: RWB-P10-E2029-CON.
- The officer's own raise of a deviation, the timers of the case and their escalation: RWB-S8-E2015-APP.
- The routing rules R-DEV-02 to R-DEV-06 as rules, the handling of X1 to X7, the contact stop lifecycle and the clearing of a deviation with `PATCH /deviations/{deviationId}`: the Epic 7 stories of this service.
- L1 on further segments, a later policy version and the promotion of another agent: rwb-agent's later work, with no story here.
- The case status "On hold", the contact hold and the prescription clock as case facts: rwb-case and rwb-comms react to the event; this slice writes none of them.
- The `rwb_deviation` schema baseline, the platform migration role, the `rwb.deviation.events.v1` topics and consumer groups, the observability and the runbook of this service.
- The end-to-end proof of these values across rwb-agent, rwb-case, rwb-deviation and rwb-access: the ITG story of this legacy key.
