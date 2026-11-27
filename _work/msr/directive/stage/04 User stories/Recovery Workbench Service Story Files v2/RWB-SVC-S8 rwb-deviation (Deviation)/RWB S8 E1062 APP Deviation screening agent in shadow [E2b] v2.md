# RWB-S8-E1062-APP Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-S8-E1062-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-deviation |
| Service epic | RWB-SVC-S8 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-062 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20 |
| Parallel lane | L-S8-D |
| Ready to start | Day 1 |
| Size | Set by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-E1062-CON |
| Contract version | Not specified in the source documents (DOR-RWB-S8-E1062-APP-23) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD S8 rwb-deviation v1.md (FR-S8-001, FR-S8-002, FR-S8-003, FR-S8-004, FR-S8-009, FR-S8-010, FR-S8-011, FR-S8-021, FR-S8-022, FR-S8-023, FR-S8-024, FR-S8-025, FR-S8-026, FR-S8-027, FR-S8-028, FR-S8-041, FR-S8-044, FR-S8-045, FR-S8-046, FR-S8-047, FR-S8-049, FR-S8-050, FR-S8-051, FR-S8-052, FR-S8-053, FR-S8-056) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-062 for rwb-deviation, carrying the deviation estate the shadow screening run reads (the open codes of the case and the owner role each code would route to) and the gate that keeps a screening raise out of the service while the policy in force is SHADOW. Applied: the plan's H row is None and the platform libraries of DP-04, DP-06, DP-07, DP-09, DP-15 and DP-19 arrive with the baseline; the Ownership Map gives S8 two write operations and no read, so the read is declared here with a gap (GAP-3085; ASM-5252); and legacy AC1 to AC9 stay with RWB-P10-E1062-APP. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-S8-E1062-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (19 resolved, 28 cross-document, 6 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **rwb-deviation to serve the screening agent the open deviations of a case and the owner role each code in force would route to, and to refuse any raise that names the screening agent while the policy in force is SHADOW**, so that **the shadow run reads the deviation estate of the case from its owner and changes nothing in force — no deviation record, no contact stop, no clock**.

This story is the rwb-deviation part of legacy RWB-E1-062. The legacy story has the agent read "the case, the interaction ledger, the documents and their fields" and store proposals in shadow (legacy sections 2 and 4), and its Data table reads `deviation.deviation_code` "so a code already open is not proposed again" and `recovery_case.deviation_open` (DF-CAS-038, DF-CAS-019). Two of those facts are this service's: the open deviations of the case, and the routing truth of each code.

Inside `rwb-deviation` this is the screening-input capability of the deviation service:

- Service `rwb-deviation`, schema `rwb_deviation`, REST base `/api/recovery/deviation/v1`, topic `rwb.deviation.events.v1` with event names `rwb.deviation.<Event>.v1`, Temporal task queue `rwb-deviation` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.deviation` (context pack, service row).
- `GET /deviations` with the case as query answers the deviation estate of one case in one hop: the open deviations with their code, state, raised date, contact stop, paused state and outcome, and beside them the owner role that each code of LOV-DEVIATION routes to at the package version in force (DP-13, DP-04, DP-07).
- The answer is built from `deviation` in `rwb_deviation` only; no `recovery_case` row, no `v_ace_*` view and no another service's table is read (DP-01).
- `ScreeningRaiseGate` refuses a raise that names `raised_by` "SCREENING_AGENT" while the autonomy mode of policy "SCREENING" in force is "SHADOW", read on the rwb-agent contract of RWB-P10-E1062-CON (DP-20); a refused raise writes no row, publishes no event and moves no clock.
- No event is published by this slice: in shadow nothing is raised, so `rwb.deviation.DeviationRaised.v1` (EV-06) stays with the raise story (DP-09 as a prohibition).

What this story does not own: the agent runtime, the policy "SCREENING" and its versions, the prompt "PR1", the output schema "screening-v1", the guardrail checks, the per-proposal owner resolution, the evaluation on sample "SCREEN-S1" and the run states, which are rwb-agent's in RWB-P10-E1062-APP against the contract RWB-P10-E1062-CON, and which own legacy AC1 to AC9; the documents and extracted fields the agent reads, which are rwb-document's in RWB-P5-E1062-APP; the masking policy itself, which is rwb-access's in RWB-P4-E1062-APP; the raise, pause, routing, contact stop and clear of a deviation, which are the Epic 2 stories of this service; and the end-to-end proof across the five services, which is RWB-ITG-E1062-ITG.

### 2. Business rationale

A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The screening agent reads the case, the ledger and the documents at entry and again when a document arrives, and proposes deviations with reasons (legacy section 2); in Epic 1 the proposals are stored only, scored against the business analysts' review and shown to nobody. The measurement is only worth something if a proposal is measured against the deviation estate the case actually carries, and if nothing in that estate moves while the agent is in shadow.

Three target facts shape this slice.

1. **The deviation estate is this service's.** `deviation` is S8's single table in `rwb_deviation` (context pack ownership rows; TSD S8 T3.1), so an open code, its state, its contact stop and its paused state are answered here and nowhere else. The agent cannot read another service's table (DP-01), and under DP-18 the ledger it also reads is rwb-source-data's, not this service's answer.
2. **The owner role of a code is data, and its owner is the service that routes it.** R-DEV-02 to R-DEV-06 are rows of the DEV route set, 22 rules over 9 states in TSD S8 T4, and they are what assigns each deviation to the complaint officer, the specialist, the fraud investigator or Legal (FSD S8 A2.4). Serving the projection here means the agent's proposal names the role the case would really route to, which is REQ-DVH-003, and the value is read with the package version and never typed in code (DP-04, DP-07).
3. **Shadow means nothing in force moves.** Legacy BR1 and AC1 fix it: no deviation record, `deviation_open` false on every case, no contact stop, no user-facing proposal. In the target the agent cannot write here at all (no operation of this service is a write the agent may call), and the gate of this story refuses a screening raise on the service side as well, so a change in the agent cannot leak into a deviation row, a contact stop or a clock (R-DEV-01 is never fired from a shadow run).

The slice therefore supports REQ-DVH-001 (the codes of the estate the detection is measured on), REQ-DVH-003 (each code routes to its named owner, an unmapped code to the team manager) and REQ-DVH-007 (a complaint is matched to the contact before it — the ledger window is rwb-source-data's and this answer carries no interaction). It changes no rule of the DEV route set and no policy of the agent.

### 3. Preconditions

- The `rwb_deviation` baseline is in place: `deviation` exists with the columns of DF-CAS-036 to DF-CAS-045 and the standard record columns of TSD S8 T3.0, loaded by the DB story of this service, and the outbox, inbox and idempotency tables of the platform event library exist in the schema.
- The service runs as its own login on `rwb_deviation` (DP-02) and holds no grant on another `rwb_*` schema and no `v_ace_*` grant, so a statement on `recovery_case` or `rwb_case` is refused by the database and fails the boundary test.
- RWB-P10-E1062-CON is published: the rwb-agent contract of this legacy key, which fixes the policy read (agent "SCREENING", its version in force, its autonomy mode, the confidence floor and the prompt) and the run key "SCREENING:<caseId>:<eventId>" the agent uses. The operation name and the field names of the policy read are Not specified in the source documents (GAP-3085; ASM-5253), and the story builds against its fake.
- The DEV route set is in force in the rwb-decision registry with R-DEV-02 to R-DEV-06 among its 22 rules, reachable on the registry read with its package version; its operation name is Not specified in the source documents (GAP-3085; ASM-5254).
- The embedded Drools kit of RWB-PLT-E1072-CON is on the service template, so the projection is evaluated in the service and not in the caller (DP-04).
- The parameters contract and client library of rwb-case are on the service template (DP-06), and the maximum number of deviations one answer carries is a parameter value; its value is Not specified in the source documents (GAP-3085; ASM-5256).
- The reference-data contract of rwb-case is on the service template (DP-07), with LOV-DEVIATION (X1 to X7) and LOV-RAISED-BY (SCREENING_AGENT, RULE, OFFICER, CUSTOMER_CONTACT) at the version in force (TSD S8 T3.2).
- The authorisation decision of rwb-access is consumed as the cached permission of the service (DP-08, which arrives with the baseline and is not added to the H row): the read needs Case record right R and the two write operations need right U (TSD S8 T-A.1, T-A.2).
- No approval is needed to build against a Draft contract baseline; the contract is tagged by RWB-P10-E1062-CON when its tests pass.

### 4. Flow

1. The screening run of RWB-P10-E1062-APP assembles its inputs and asks this service for the deviation estate of the case: `GET /api/recovery/deviation/v1/deviations?caseId=<caseId>` with the identity SY-AGENT, one hop, inside a 2 s budget (legacy section 4 step 3; DP-13).
2. `DeviationGuard` authorises the call from the cached decision of rwb-access (Case record right R, scope applied) and refuses with 403 and MSG-P4-002 before a row is read (legacy X7, TC-E1-062-10).
3. `OpenDeviationReader` reads the `deviation` rows of the case in `rwb_deviation` whose `cleared_at` is null and whose `state` is not a cleared state, with the code, state, raised date and actor, contact stop, paused state and outcome (DF-CAS-036 to DF-CAS-045).
4. `DeviationOwnerProjection` takes the codes of LOV-DEVIATION at the version in force from the reference-data contract (DP-07), fetches the DEV package at its version in force on the registry read (DP-04), evaluates R-DEV-02 to R-DEV-06 in the embedded kit for each code, and pairs each code with the owner role the rule assigns; a code with no owner row is paired with "RW-TEAMMGR" and the marker "unmapped" (legacy BR3, AC4).
5. `ScreeningInputAssembler` builds the answer: the open deviations of the case and the owner projection of the codes in force, with no person name, no contact value, no handler identity and no free-text note (legacy section 11; BR2).
6. The answer is returned inside the 2 s budget, one hop, with no call to another service on the read path beyond the reference-data and package reads of steps 4, and the read is repeated on the same inputs with the same answer (a read is idempotent and writes nothing).
7. On the write path, `ScreeningRaiseGate` checks each raise request that names `raised_by` "SCREENING_AGENT": it reads the autonomy mode of policy "SCREENING" at its version in force on the rwb-agent contract (DP-20). Where the mode is "SHADOW" the request is refused with 409 and no message to a user, nothing is written, no outbox row is created, no contact stop is set and no clock moves (legacy BR1; AC1).
8. Where the mode is not "SHADOW" the gate lets the request through to the raise path of the Epic 2 story of this service, and this story changes nothing of that path (legacy section 19; RWB-E2-029).
9. A read of a case that this service holds no deviation for answers an empty list with 200: the case is rwb-case's row and this service does not confirm its existence, so no 404 is invented for a case it does not own (ASM-5252).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The calling identity holds no Case record right R | Refused with 403 before any row is read; nothing is returned | MSG-P4-002 | AC5, TC-E1-062-10 |
| X2 | The `caseId` query is absent or is not a case reference | 422 and no read; nothing is written | MSG-GEN-001 | AC6, TC-E1-062-15 |
| X3 | The reference-data or the package read does not answer inside the budget, or the registry has no package version in force | 503 with the platform envelope and the name of the system; no partial answer is built | MSG-GEN-006 | AC7, TC-E1-062-16 |
| X4 | A code of the version in force has no owner row in R-DEV-02 to R-DEV-06 | The projection names "RW-TEAMMGR" and the marker "unmapped" for that code; the rest of the answer stands | None | AC3 |
| X5 | A raise request names `raised_by` "SCREENING_AGENT" while the policy in force is "SHADOW" | Refused with 409; no `deviation` row, no `deviation_open` change, no contact stop, no clock and no outbox row | None to a user | AC4 |
| X6 | The rwb-agent policy read does not answer, so the mode in force is unknown | The raise is refused with 503 and the reason names the agent contract; the shadow side never falls back to "raise" | MSG-GEN-006 | AC8, TC-E1-062-17 |
| X7 | A component, a statement or a test reaches a `recovery_case` row, a `rwb_case` table, a `v_ace_*` view or another service's schema | The grant refuses the statement and the boundary test fails the build; nothing is released | None (pipeline log) | AC9, AC13, TC-E1-062-18, TC-E1-062-19; Section 17, BR1, BR6 |

X1 and X5 to X7 are the legacy exception paths carried onto the slice (the role case X7 of the legacy story is TC-E1-062-10, the shadow case is BR1); X2 to X4 are the paths the two owner reads and the projection add. The agent's own paths — a code outside X1 to X7, a low-confidence proposal, a repeated event on the run side and a timeout — are RWB-P10-E1062-APP's and are not restated here.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Answers from `rwb_deviation` only and builds on Day 1 against the RWB-P10-E1062-CON fake, the registry and reference-data fakes and the platform libraries of the baseline; it waits for no in-lane story |
| Negotiable | The view name, the answer's field order, the parameter values of the limit and the wording of the projection are this story's; the codes, the owner roles, the states and the lists are rows |
| Valuable | The shadow run is measured against the real deviation estate of each case, a proposal names the role the case would route to, and no shadow run can create a deviation, a stop or a clock |
| Estimable | One module, one read operation, one projection, one gate, one view and one Flyway step |
| Small | Fits one sprint as a secondary slice of the legacy key, beside RWB-P10-E1062-APP and RWB-P5-E1062-APP |
| Testable | Every criterion runs on synthetic deviations and synthetic packages through the contract fakes, plus the access, refusal and boundary cases |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent in shadow [E2b] — the rwb-deviation estate and the shadow gate

  Background:
    Given the rwb-agent contract mock returns policy "SCREENING" at its version in force with mode "SHADOW", confidence floor 0.80 and prompt "PR1"
    Given the rwb-decision rule-package mock returns the DEV route set at its version in force with R-DEV-02 to R-DEV-06
    Given the rwb-case reference-data contract mock returns LOV-DEVIATION with X1 to X7 and LOV-RAISED-BY at the version in force

  Scenario: AC1 The open deviations of the case are served to the agent (new, D-RCV-60)
    Given case "RW-2026-000403" holds open deviation "X1" raised on 2026-12-10 with contact stop true and paused state "WITH_FCR_OFFICER"
    When "SY-AGENT" calls GET /api/recovery/deviation/v1/deviations with case "RW-2026-000403"
    Then the answer holds deviation "X1" with its id, its case id, code "X1", state, raised date, contact stop and paused state
    Then the answer holds no person name, no contact value, no handler identity and no free-text note
    Then a case with no open deviation answers an empty list

  Scenario: AC2 Every open code of the case is in the one answer (new, D-RCV-60)
    Given case "RW-2026-000502" holds open deviation "X3" raised on 2026-12-10 and open deviation "X6" raised on 2026-12-11
    When "SY-AGENT" calls GET /api/recovery/deviation/v1/deviations with case "RW-2026-000502"
    Then the answer holds both codes "X3" and "X6", so a code already open is not proposed again
    Then the codes are read from LOV-DEVIATION at the version in force in one answer and not one call per code

  Scenario: AC3 The owner role of each code comes from the DEV rule rows (new, D-RCV-60)
    Given the rule-package mock gives R-DEV-04 the owner role "RW-FRAUD" for code "X4" and holds no owner row for code "X7"
    When the read answers for case "RW-2026-000402"
    Then the projection names owner role "RW-FRAUD" from R-DEV-04 for code "X4"
    Then the code with no owner row in R-DEV-02 to R-DEV-06 is projected with owner role "RW-TEAMMGR" and the marker "unmapped"
    Then no code, no owner role and no marker is written in the Java source or in the module configuration

  Scenario: AC4 In shadow mode the service raises nothing (new, D-RCV-60)
    Given the rwb-agent contract mock returns mode "SHADOW" for policy "SCREENING" at its version in force
    When a raise request names raised_by "SCREENING_AGENT" for case "RW-2026-000404" with code "X2"
    Then the request is refused with status 409 and no message to a user
    Then no deviation row exists, deviation_open stays false on the case, no contact stop is set and no clock moves
    Then no rwb.deviation.DeviationRaised.v1 event and no outbox row is written
    Then the same request under a mode other than "SHADOW" is not refused by this gate

  Scenario: AC5 A caller without the Case record right is refused (new, D-RCV-60)
    Given the rwb-access contract mock returns no Case record right R for the calling identity
    When that identity calls GET /api/recovery/deviation/v1/deviations with case "RW-2026-000403"
    Then the call is refused with status 403 and message MSG-P4-002
    Then no deviation and no owner role is returned
    Then the service reads no table outside rwb_deviation and holds no v_ace_* grant

  Scenario: AC6 A read without a case reference is refused before any read (new, D-RCV-60)
    When "SY-AGENT" calls GET /api/recovery/deviation/v1/deviations with no caseId
    Then the call is refused with status 422 and message MSG-GEN-001
    Then no row is read and nothing is written

  Scenario: AC7 A read that misses the budget or has no package version in force returns no partial answer (new, D-RCV-60)
    Given the reference-data mock does not answer inside the budget, or the rule-package mock has no version in force
    When "SY-AGENT" calls GET /api/recovery/deviation/v1/deviations with case "RW-2026-000403"
    Then the call is refused with status 503 and message MSG-GEN-006 naming the system
    Then no partial answer is built

  Scenario: AC8 An unknown agent policy is never read as raise (new, D-RCV-60)
    Given the rwb-agent contract mock does not answer for policy "SCREENING"
    When a raise request names raised_by "SCREENING_AGENT" for case "RW-2026-000404" with code "X2"
    Then the raise is refused with status 503 and message MSG-GEN-006, and the reason names the agent contract
    Then no deviation row, no event and no outbox row is written

  Scenario: AC9 A statement outside rwb_deviation fails the build (new, D-RCV-60)
    Given the build holds a statement on a recovery_case row, a rwb_case table, a v_ace_* view or another service's schema
    When the boundary build check runs
    Then the grant refuses the statement and the build fails
    Then nothing is released

  Scenario: AC13 The database refuses a statement outside rwb_deviation at run time (new, D-RCV-60)
    Given the service runs as its own login on rwb_deviation and holds no grant on recovery_case, rwb_case, v_ace_* or another service's schema
    When the login issues a statement on a recovery_case row, on a rwb_case table or on a v_ace_* view
    Then the database refuses the statement
    Then the refusal fails the boundary test and nothing is released

  Scenario: AC14 The read rules of section 8 hold on the answer, the build and the log (new, D-RCV-60)
    Given a synthetic personal value is placed in handler_user_id and in a free-text column of a deviation row
    When "SY-AGENT" reads the deviation of that case twice on the same rows and the same package version
    Then the serialised answer, the log and the span attributes hold no such value (BR1, BR2)
    Then the two answers are the same and no row is written (BR8)
    Then the agent holds no call to the write operations of the service (BR8)
    Then the build check finds no code, owner role or rule constant in the source (BR5)
    Then no ledger table, no Drools event, no outbox write and no outbound call to rwb-source-data is in the build (BR6, BR7)
    Then a raise naming "SCREENING_AGENT" is refused while the mode in force is "SHADOW" (BR4)

  Scenario: AC15 A call without a valid credential is refused with 401 on every provided operation (new, D-RCV-60)
    Given the calling identity carries no valid credential
    When the identity calls any operation of rwb-deviation, for example GET /api/recovery/deviation/v1/deviations with case "RW-2026-000403"
    Then the call is refused with status 401
    Then no deviation and no owner role is returned
```

The twelve criteria are new and test only this slice: the deviation estate the screening run reads and the gate that keeps a screening raise out of the service in shadow. The legacy criteria AC1 to AC9 of RWB-E1-062 are owned word for word by RWB-P10-E1062-APP (the shadow flags, the comparison, the document trigger, the owner role, the preceding contact, the review marker, the repeated event, the code outside the list and the timeout), and no legacy criterion text is copied here. Two legacy values are reused because the sources publish them: the owner role "RW-FRAUD" from R-DEV-04 for X4 and the mapping of a code with no row to "RW-TEAMMGR" with the marker "unmapped" (legacy AC4, BR3); they are asserted on this service's projection, not on the agent's proposal. Two points are recorded rather than smoothed over: the read is not in the Ownership Map (GAP-3085; ASM-5252), and the reference of a case this service holds no deviation for is answered as an empty list rather than a 404 (ASM-5252).

### 8. Business rules

| Rule | Route set | Codes | From state | Event | To state | What this story does with it | Source |
|---|---|---|---|---|---|---|---|
| R-DEV-02 | Deviations | X1 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER | Projects the complaint officer as the owner role of X1 | FSD S8 A2.4.3.1; TSD S8 T4 |
| R-DEV-03 | Deviations | X2, X3 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER | Projects the specialist, with Legal joining X3 for the estate claim | FSD S8 A2.4.3.1; TSD S8 T4 |
| R-DEV-04 | Deviations | X4 | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER | Projects owner role "RW-FRAUD" for X4 (legacy AC4) | Legacy BR3, AC4; TSD S8 T4 |
| R-DEV-05 | Deviations | Not specified in the source documents (GAP-3085; ASM-5255) | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER | Projected from the package at the version in force; its owner role is never written in code | TSD S8 T4 |
| R-DEV-06 | Deviations | Not specified in the source documents (GAP-3085; ASM-5255) | DEV_FLAGGED | OWNER_ASSIGNED | DEV_WITH_OWNER | Projected from the package at the version in force; its owner role is never written in code | TSD S8 T4 |
| R-DEV-01 | Deviations | X1 to X7 | ANY_STATE | DEVIATION_FLAGGED | DEV_FLAGGED | Never fired from a shadow run; the gate of AC4 keeps the raise out of the service | FSD S8 A2.2.3.1; legacy BR1 |

The two text rows of R-DEV-02 and R-DEV-03 are those of the FSD, copied character for character; R-DEV-04 to R-DEV-06 are rows of the same DEV route set (22 rules over 9 states, TSD S8 T4) whose owner-role values are published only for X4 and are otherwise read from the package with its version. The codes of R-DEV-05 and R-DEV-06 are not printed by any source read for this slice, so they are not guessed.

| ID | Rule | Source |
|---|---|---|
| BR1 | The answer is built from `deviation` in `rwb_deviation` only; no `recovery_case` row, no `v_ace_*` view and no table of another service is read, and no foreign key leaves the schema | DP-01; context pack ownership rows; TSD S8 T3.1, T3.3 |
| BR2 | The answer carries references, codes, states, dates and the owner projection, and no person name, contact value, handler identity, free-text note or document field value | Template and Rules §R7.2 (s17); TSD S8 T6.2; legacy section 11 |
| BR3 | The owner role of each code is read from the rule rows R-DEV-02 to R-DEV-06 at the package version in force; a code with no row maps to "RW-TEAMMGR" and carries the marker "unmapped" | Legacy BR3, AC4, X5; REQ-DVH-003; DP-04; ASM-B-ITG-W1-08-E1062-1 to -6 |
| BR4 | In shadow the service raises nothing: no deviation record, no `deviation_open` change, no contact stop, no clock and no event, and the gate refuses a raise that names the screening agent while the mode in force is SHADOW | Legacy BR1, AC1; agent_policy.autonomy_mode is rwb-agent's (DF-AGT-008) |
| BR5 | The codes, the actor values and the owner roles are reference data and rule rows read with their version; none of them is a constant, a default or a branch in the module | FSD S8 BR-S8-001, BR-S8-004; TSD S8 T3.2; DP-07 |
| BR6 | The interaction ledger is rwb-source-data's and the ledger of the agent's reads is written by its listener from the event: this service writes no ledger row and reads none (DP-18) | DP-18; context pack default ruling; Architecture v5 slide 13 |
| BR7 | This service publishes no event of this slice: `rwb.deviation.DeviationRaised.v1` and `rwb.deviation.DeviationCleared.v1` stay with the raise and clear steps (DP-09 as a prohibition) | DP-09; TSD S8 T5.3; legacy BR7 |
| BR8 | A read is idempotent: the same request on the same rows and the same package version answers the same values and writes nothing; the two write operations of the service are not called by the agent | Legacy AC7; TSD S8 T-A.1 |

BR1 and BR2 are property tests over the serialised answer: a synthetic personal value placed in `handler_user_id` or in a free-text column must not appear in the JSON, the log or the span attributes. BR3 is executed by `DeviationOwnerProjection`, which asks the kit for the rules and never for a table of owner roles; a build check fails on a code or an owner role in the source. BR4 is executed by `ScreeningRaiseGate` before the raise path, with the mode read on the agent contract. BR6 and BR7 are prohibitions checked by the same build: no ledger table, no Drools event, no outbox write on this slice, and no outbound call to rwb-source-data.

### 9. State transitions

None for the case and none for a deviation. This story changes no case status, raises no deviation and clears none: it reads the state of the `deviation` rows of the case and refuses a screening raise in shadow, so the state machine of the DEV route set is not entered (TSD S8 T4). `DEV_FLAGGED` and every state after it stay with the raise, routing, handling and clear steps of the Epic 2 stories of this service, and `deviation_open` is a rwb-case field that this slice never writes (ASM-5253).

| Read or step | Event | Condition | Result |
|---|---|---|---|
| The read request | The caller's identity and the case | The Case record right R is granted | The estate of the case is answered; nothing is written |
| The read request | A case this service holds no open deviation for | The right is granted | An empty list is answered; the case row is not confirmed here |
| The raise request | `raised_by` is "SCREENING_AGENT" | The mode in force is "SHADOW" | Refused with 409; no row, no event, no clock, no contact stop |
| The raise request | `raised_by` is "SCREENING_AGENT" | The mode in force is not "SHADOW" | Passed to the raise path of the Epic 2 story; this slice changes nothing of it |
| The projection | The package read answers | R-DEV-02 to R-DEV-06 are in force | Each code pairs with its owner role; a code with no row pairs with "RW-TEAMMGR" and "unmapped" |
| The projection | The package or the reference-data read does not answer | X3 | Held; 503 with MSG-GEN-006; no partial projection is served |

The run states of the screening agent — PENDING, RUNNING, TIMED_OUT, GUARDRAIL_FAILED and the review marker of a low-confidence proposal — are rwb-agent's rows and rwb-agent's transitions (RWB-P10-E1062-APP), and no state of them is written or read here.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Case record right R (TSD S8 T6.1): reads the deviation estate of a case and the owner projection, masked, in scope; holds no write right and calls no write operation |
| SY-RULES, the embedded rule kit | Evaluates R-DEV-02 to R-DEV-06 for the projection from the package in force; subject to the same checks as a person |
| rwb-deviation service identity (the service login, DP-02) | Serves the read, reads `deviation` in `rwb_deviation` and the two owner contracts of DP-04 and DP-07, and runs the raise gate; holds no grant on another schema and no `v_ace_*` grant |
| RW-COE, center of excellence analyst | Owns the sample and the evaluation (RWB-P10-E1062-APP); this story serves that work the estate it is measured on and grants it nothing of its own |
| RW-COMPLAIN, RW-SPECIAL, RW-FRAUD, RW-LEGAL, RW-TEAMMGR | The roles the projection names: they hold Case record RU or R as TSD S8 T6.1 gives it and read the same estate on their own screens; nothing is granted by this story beyond the matrix |
| RW-CASEOWN, case owner | Case record CRU: raises and clears a deviation in the Epic 2 stories, through the two write operations the Ownership Map gives the service; the screening gate never widens that right |
| RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-DATASTEW | Read run metadata or platform administration of the service, as the matrix gives it; no deviation content of their own |

The rights are the rows of TSD S8 T6.1 and the declared right of each operation in TSD S8 T-A.1 and T-A.2. DP-08 is not in this story's pattern set: the authorisation decision is rwb-access's and is consumed as the cached permission the service template already carries, so the check is stated here and not built here. The agent's identity is read only: no shared identity exists for its reads, and every read is authorised with the caller's own identity.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| DF-CAS-036 | deviation (S8, `rwb_deviation`) | id | Read, the deviation reference of the answer |
| DF-CAS-037 | deviation (S8, `rwb_deviation`) | case_id | Read, the case reference of the answer |
| DF-CAS-038 | deviation (S8, `rwb_deviation`) | deviation_code | Read, the code of each open deviation and the key of the projection |
| DF-CAS-039 | deviation (S8, `rwb_deviation`) | raised_at | Read |
| DF-CAS-040 | deviation (S8, `rwb_deviation`) | raised_by | Read, to select the screening raise in the gate |
| DF-CAS-041 | deviation (S8, `rwb_deviation`) | paused_state | Read |
| DF-CAS-043 | deviation (S8, `rwb_deviation`) | contact_stop | Read |
| DF-CAS-044 | deviation (S8, `rwb_deviation`) | cleared_at | Read, to select the rows that are still open |
| DF-CAS-045 | deviation (S8, `rwb_deviation`) | outcome | Read |
| Standard columns | deviation (S8, `rwb_deviation`) | `is_active`, `state`, `version` | Read, `state` to tell an open row from a cleared one |
| DF-REF-002 | rule_row (P7, in the package) | rule_id | Read on the package read, never as a table |
| DF-REF-010 | rule_row (P7, in the package) | owner_role | Read on the package read, never as a table |
| DF-AGT-008 | agent_policy (P10, `rwb_agent`) | autonomy_mode | Read on the rwb-agent contract, never as a table |
| DF-CAS-019 | recovery_case (P3) | deviation_open | Not read and not written: the case row is rwb-case's and the flag moves only in the raise and clear steps |
| DF-INT-001 to DF-INT-011 | interaction (P1) | id, occurred_at, channel, summary | Not read: the ledger is rwb-source-data's (DP-18) |
| DF-DOC-001 to DF-DOC-015 | document, document_field (P5) | id, document_type, field_name, field_value | Not read: the documents are rwb-document's and are read by RWB-P5-E1062-APP |

Field IDs are those of TSD S8 T3.1 and the Logical Data Model and Data Dictionary. **No write, no new table and no new column**: this story reads rows another step writes, and its one migration adds a read-only view and an index in `rwb_deviation` (DP-15). `handler_user_id` (DF-CAS-042) is deliberately not in the answer: it identifies a person and the agent does not need it (BR2).

No personal data. The answer carries identifiers, codes, states, dates, a boolean and a rule version. No name, address, contact value or identity number enters the answer, a log, a trace or a workflow input, and every fixture is synthetic.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-deviation (S8); base `/api/recovery/deviation/v1` (DP-13).

| Method | Path | Query | Answer | Access | Idempotency |
|---|---|---|---|---|---|
| GET | `/deviations` | `caseId` (required) | The open deviations of the case and the owner projection of the codes in force | Case record right R, scope applied | Idempotent read; no `Idempotency-Key` needed |

The answer is one object with two arrays. `openDeviations` carries, per row, `deviationId`, `caseId`, `deviationCode`, `state`, `raisedAt`, `raisedBy`, `contactStop`, `pausedState`, `outcome` and `clearedAt` (null while open), which are the TSD S8 T3.1 columns of `deviation` and nothing else. `ownerRoles` carries, per code of LOV-DEVIATION at the version in force, `deviationCode`, `ownerRole` and `mapped`, the outcome of R-DEV-02 to R-DEV-06 at the package version in force. Errors: 401 no Workbench identity (MSG-P4-001), 403 Case record right R absent (MSG-P4-002) or case outside the scope, 422 `caseId` absent or malformed (MSG-GEN-001), 503 a downstream of steps 4 and 5 is unavailable (MSG-GEN-006). A case with no open deviation answers both arrays, `openDeviations` empty, with 200. Screen states of SCR-06 and SCR-08, which read this answer through DP-19: empty is the empty list above; error is 503 with MSG-GEN-006; no access is 403 with MSG-P4-002; loading is Not specified in the source documents (DOR-RWB-S8-E1062-APP-10).

The Ownership Map gives S8 two operations, `POST /cases/{caseId}/deviations` and `PATCH /deviations/{deviationId}` (API-S8-001, API-S8-002), and no read, while the screening run needs the open codes of the case and rwb-agent's contract names this read as its source for them. The read is therefore declared here with a gap and an assumption (GAP-3085; ASM-5252), and the two write operations stay with the Epic 2 stories of this service.

#### 12.2 REST operations consumed

| Operation | Path | Owner | Use |
|---|---|---|---|
| The agent policy read of RWB-P10-E1062-CON (operation name Not specified in the source documents (GAP-3085; ASM-5253)) | `/api/recovery/agent/v1` | P10 rwb-agent | The autonomy mode of policy "SCREENING" at its version in force, for the raise gate; faked |
| The rule-package read in force (operation name Not specified in the source documents (GAP-3085; ASM-5254)) | `/api/recovery/decision/v1` | P7 rwb-decision | The DEV route set at its version, for R-DEV-02 to R-DEV-06 and the owner roles; faked, through the kit |
| The parameters read (operation name Not specified in the source documents (GAP-3085; ASM-5256)) | `/api/recovery/case/v1` | P3 rwb-case | The maximum number of deviations one answer carries; faked, cached |
| The reference-data read (operation name Not specified in the source documents (GAP-3085; ASM-5257)) | `/api/recovery/case/v1` | P3 rwb-case | LOV-DEVIATION and LOV-RAISED-BY at the version in force; faked, cached |

Every row is one hop with a 2 s timeout and a breaker per downstream (ADR-020). The four rows are class C dependencies in fact that the plan does not hold, because this story's C row is `RWB-P10-E1062-CON` and its H row is None; the first is the contract of the key and the other three arrive with the platform libraries of DP-04, DP-06 and DP-07 (GAP-3085; ASM-5254).

#### 12.3 Events published

None. In shadow nothing is raised, so this slice writes no outbox row and publishes nothing: `rwb.deviation.DeviationRaised.v1` (EV-06) and `rwb.deviation.DeviationCleared.v1` (EV-07) on `rwb.deviation.events.v1` belong to the raise and clear steps of this service (DP-09 as a prohibition; ASM-5258). A gate that refused a raise leaves no event behind, which is the producer-side half of legacy AC1 "no deviation record exists".

#### 12.4 Events consumed

None. This story subscribes to no topic, holds no consumer group and writes no inbox row: the estate is read on request, not on an event, and the trigger of the screening run is the agent's own. The inbox table of DP-09 is present in `rwb_deviation` for the consumers other stories of this service add.

#### 12.5 Workflows and activities

None. The read and the gate are synchronous, in the caller's thread, one hop and 2 s. `DeviationWorkflow` on queue `rwb-deviation` is the service's and belongs to the raise, pause, handling and clear steps; this slice contributes no activity to it and starts no workflow. The agent's own `AgentRunWorkflow` is rwb-agent's on queue `rwb-agent`.

#### 12.6 Schedules

None. The estate is read on request, the gate runs on the request, and the service owns no job in the ownership rows (Jobs 0). The deviation service level of R-DEV-20 is a workflow timer of the handling step, not a Temporal Schedule of this slice.

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| deviation | S8 (`rwb_deviation`) | Read only: the open rows of the case and the family of codes |
| v_open_deviation | S8 (`rwb_deviation`) | Read only view over `deviation`, created by this story's migration for the read of an open estate and its index (DP-15) |
| outbox_event | PLT library, created in `rwb_deviation` | Present for the raise and clear steps; this slice writes none of its rows |
| processed_event | PLT library, created in `rwb_deviation` | Present for the consumers of other stories; this slice writes none of its rows |
| idempotency_key | PLT library, created in `rwb_deviation` | Present for the write operations; this slice writes none of its rows |

Not owned and never read as a table: `recovery_case` and `deviation_open` (P3), the `v_ace_*` views and the interaction ledger (P1), `document` and `document_field` (P5), `agent_policy` and the agent run (P10 `rwb_agent`), `rule_row` and `decision_log_entry` (P7). No foreign key leaves `rwb_deviation`; `case_id` and `raised_by` are references, not keys across schemas (DP-01).

#### 12.8 Contract fakes

| Fake | Documents | Used by |
|---|---|---|
| RWB-P10-E1062-CON agent fake (rwb-agent contract; library version: Not specified in the source documents (DOR-RWB-S8-E1062-APP-22)) | The policy "SCREENING" at its version in force with mode "SHADOW" and floor 0.80; the same policy in a mode other than SHADOW; no answer beyond 2 s | AC4, X5, X6 |
| rwb-decision rule-package fake | The DEV route set with R-DEV-02 to R-DEV-06, "RW-FRAUD" for X4, no owner row for X7, and a registry with no version in force | AC3, X3, X4 |
| rwb-case parameters fake | The maximum number of deviations in one answer; a value absent | AC2, X3 |
| rwb-case reference-data fake | LOV-DEVIATION with X1 to X7 and LOV-RAISED-BY at the version in force; a code that has left the version in force | AC2, AC3 |
| rwb-access decision fake | A granted Case record right R for SY-AGENT, a refused decision for an identity without it, and a scope that excludes one case | AC5, X1 |
| gateway-bff composite route fake | The estate of `RW-2026-000502` as a screen sees it, in its open and cleared states | AC1, AC2 |

The fakes are test-only and are replaced by the real services in SIT. No fake carries personal data: every deviation in the fixtures is synthetic and every field of a person is absent from them.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `GET /deviations` on `/api/recovery/deviation/v1`; the agent policy, the rule package, the parameters and the reference data, each one hop with 2 s and a breaker |
| Kafka | 0 published, 0 consumed | No event of this slice: the two events of the service belong to the raise and clear steps |
| Temporal | None | No workflow, no activity and no Schedule in this slice |
| File | None | No file is read, built or delivered here |

### 13. Solution plan

**Package.** Java package `th.co.scb.ace.workbench.recovery.deviation`, module `screening-input`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `DeviationGuard` | Guard | The Case record right of `GET /deviations` from the cached decision of rwb-access, the scope check and the problem mapping of section 14 |
| `OpenDeviationReader` | Repository | Reads the open rows of `deviation` for the case in `rwb_deviation`, with the columns of §11 and no other table |
| `DeviationOwnerProjection` | Service | Reads the codes of LOV-DEVIATION at the version in force, fetches the DEV package at its version, evaluates R-DEV-02 to R-DEV-06 in the embedded kit and pairs each code with its owner role and the "unmapped" marker |
| `ScreeningInputAssembler` | Service | Builds the answer of 12.1: the open estate, the projection, the limit and the absence of personal data |
| `ScreeningRaiseGate` | Service | Reads the autonomy mode of policy "SCREENING" on the rwb-agent contract and refuses a screening raise with 409 while the mode is SHADOW, before the raise path |
| `AgentPolicyClient` | Client | The policy read of RWB-P10-E1062-CON, one hop, 2 s, breaker, cached for the request |
| `RulePackageClient` | Client | The package read of rwb-decision at its version in force, through the kit |
| `ReferenceDataClient`, `ParameterClient` | Client | LOV-DEVIATION, LOV-RAISED-BY and the answer limit, from the rwb-case contracts, cached |

**Database and migrations.** One step in the per-service Flyway sequence of `rwb_deviation` (DP-15): `V1062_1__screening_deviation_read.sql`, which creates the read-only view `v_open_deviation` over `deviation` (the open rows with their code, state, raised date, actor, contact stop, paused state, outcome and cleared date) and one index on the columns the read filters by. No business table, no column and no constraint is added, and no migration of this service touches another schema or the shared baseline. The view name is a design choice fixed by no source document (ASM-5259).

**Configuration and reference data.**

- The codes, the actor values and the owner roles are rows of LOV-DEVIATION, LOV-RAISED-BY and the DEV package at their version in force; none is a constant of the module (DP-07, DP-04).
- The maximum number of deviations one answer carries is a parameter value of rwb-case; its value is Not specified in the source documents (GAP-3085; ASM-5256).
- The policy "SCREENING", its version and its autonomy mode are rwb-agent's data and are read on its contract; this service holds no copy of them (DP-20).
- The 2 s budget, the single hop and the breaker are the platform rule of ADR-020, and the flag `rwb.deviation.screening-input` is a flag of the platform library: off means the read answers 404 to every caller and the gate refuses every screening raise with 409, while the estate of the service itself is unchanged.

**Build steps**

1. The view and its index in the service's Flyway sequence, applied on an empty `rwb_deviation` and on a loaded one (AC1, AC2, DP-15).
2. `OpenDeviationReader` with the open-row filter and the columns of §11; unit tests for AC1 and AC2.
3. `DeviationOwnerProjection` over the reference-data and package fakes, with R-DEV-02 to R-DEV-06, "RW-FRAUD" for X4 and the unmapped path; unit tests for AC3 and X4.
4. `ScreeningInputAssembler` and the operation with the guard and the scope check, the empty case and the refusal path; API tests for AC1, AC2, AC5 and X1.
5. `ScreeningRaiseGate` with the agent-policy fake, the 409 path, the not-refused path and the no-answer path; tests for AC4, X5 and X6.
6. The property test that places a synthetic personal value in `handler_user_id` and in a free-text fixture and asserts that it appears in no answer, no log line and no span attribute (BR2).
7. The build check that fails on a code, an actor value, an owner role or the marker in the source, and on any statement outside `rwb_deviation`, including a read of a `v_ace_*` view or an ACE table; this service carries no ACE field, and any ACE data it needs comes from the rwb-source-data contract (BR5, BR1, X7).
8. A contract-fake run of RWB-P10-E1062-CON, the registry, the parameters and the reference data, so the slice proves every criterion before the agent is live in DEV.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

This is a secondary slice: the metadata "Depends on (build)" stays `None` and "Contract dependencies" stays `RWB-P10-E1062-CON` exactly as the Work Package fixes them, so the platform contracts that DP-04, DP-06, DP-07, DP-09, DP-15 and DP-19 name arrive with the service template and are not written into the H row (GAP-3085; ASM-5254).

- **DP-01** keeps the whole answer inside `rwb_deviation`; a statement on any other service's schema or on a `v_ace_*` view fails the boundary test. **DP-15** puts the view and its index in the per-service Flyway sequence, never in the shared baseline.
- **DP-04** is the owner projection: the DEV package is fetched at its version in force and R-DEV-02 to R-DEV-06 are evaluated in the embedded kit, so no owner role is duplicated in a table of this service (legacy BR3). **DP-07** is the two lists, resolved at the version in force, which is what makes the projection cover exactly the codes in force. **DP-06** is the parameter read of the answer limit; no limit is a constant of the module.
- **DP-09** and **DP-18** apply as prohibitions: the library and the topic exist for the service and in shadow the read publishes nothing because nothing is raised, and the ledger stays rwb-source-data's, so the answer carries no interaction and this service writes no ledger row. Neither call notes nor documents are read here: the screening run reads them on the rwb-source-data and rwb-document contracts, and this service holds no copy of a document (GAP-1822).
- **DP-13** gives the read its base `/api/recovery/deviation/v1`, and **DP-19** is the route a screen reads the same estate through; the agent reaches the operation through the edge, one hop, and no route calls a service that calls another.
- **DP-20** is the policy read of the gate: this service is a client of the rwb-agent contract for the autonomy mode in force and never embeds the agent runtime; the platform agent contract of DP-20 (`RWB-P10-TE013-CON`) is not in the plan's C row, which holds the contract of this legacy key instead (GAP-3085; ASM-5253).

**Done when.** The tests of section 16 pass, the read answers the estate of `RW-2026-000403` and `RW-2026-000502` on the fakes with their codes and states, the projection names "RW-FRAUD" for X4 and "RW-TEAMMGR" with "unmapped" for a code without a row, a screening raise in shadow is refused with 409 and leaves no row, no event, no contact stop and no clock, an identity without the right is refused with MSG-P4-002, the migration applies cleanly on an empty `rwb_deviation`, and no statement outside the schema exists in the build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | The caller's identity holds no Case record right R (X1, AC5) | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | The `caseId` query is absent or malformed (X2) | Enter {field}. |
| MSG-GEN-006 | The package, the reference data or the agent policy does not answer inside the budget (X3, X6) | {system} is not available. Your request is queued and will be retried. |
| None | A screening raise in shadow (X5, AC4) | No message: no user is in the loop, and the agent receives 409 with the platform error envelope |

The three IDs and their text are those of the legacy and FSD message sets, copied unchanged. For MSG-P4-002, {action} names the action the caller tried — "read the deviations of this case" — and never a case fact. For MSG-GEN-006, {system} is "Rule package", "Reference data" or "Agent policy" on the three paths. Errors are RFC 9457 problem responses with `messageId`, `detail` with the placeholders filled and `instance` naming the request; the HTTP mapping is 403 for MSG-P4-002, 409 on the shadow refusal, 422 for MSG-GEN-001 and 503 for MSG-GEN-006. MSG-P10-002 and MSG-P10-003 (the empty sample and the evaluation already running) are RWB-P10-E1062-APP's and are not restated here.

### 15. Screens and states

No screen in this story. The read is a service-to-service call: the agent's tool gateway calls rwb-deviation, one hop, and no person is in the loop. No screen of the case record, the deviation queue or the review queue changes because of this slice, and the deviation screens of this service belong to its other stories (SCR-06 Raise deviation and SCR-08 Deviation queue). Screen states: SCR-06 loading is Not specified in the source documents (CG-ALL-11316), and its empty, error and no access states are those of section 12.1; SCR-08 loading is listed in Screen Specifications v1, and its empty, error and no access states are those of section 12.1 (CG-ALL-11317).

A screen that shows the same estate reaches it through the gateway-bff composite route of DP-19, which merges the deviation answer of this service with the case state of rwb-case; the route specification and the field-level masking of the composite route belong to RWB-PLT-N001-CON. The agent run metadata screen — the runs, their mode, their status and the evaluation scores — is rwb-agent's on `/api/recovery/agent/v1`, and this story serves it nothing.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-062-10 | Access: the read of AC5. The evaluation read the legacy case names belongs to RWB-P10-E1062-APP | Component | An identity holding no Case record right R calls `GET /deviations` for case RW-2026-000403; refused with 403 and MSG-P4-002; SY-AGENT is granted the same read |
| TC-E1-062-01 | AC1 and AC4 for the deviation half of the shadow run: no deviation row, `deviation_open` false, no contact stop, no event. The run itself belongs to RWB-P10-E1062-APP | Component | 200 synthetic cases with deviations; after the shadow run the read of each case and its `deviation` rows are unchanged |
| TC-E1-062-02 | No criterion here; the comparison of proposals with the labels belongs to RWB-P10-E1062-APP | Component | Sample SCREEN-S1 version 1; X6 counts 18, 2, 6 |
| TC-E1-062-03 | No criterion here for the document trigger; the run it starts is the agent's and the event is RWB-P5-E1062-APP's | End to end | Case RW-2026-000401, DEATH_CERTIFICATE document |
| TC-E1-062-04 | AC3 for the routing half: the projection names "RW-FRAUD" from R-DEV-04 for X4 and "RW-TEAMMGR" with "unmapped" for a code without a row. The proposal's own owner role belongs to RWB-P10-E1062-APP | Component | X4 on case RW-2026-000402; one code with no owner row |
| TC-E1-062-05 | No criterion here: the preceding contact is read from the ledger by the agent, which is rwb-source-data's (DP-18) | Component | Call 2026-11-25, complaint note 2026-11-27 |
| TC-E1-062-06 | No criterion here; the review marker of a low-confidence proposal belongs to RWB-P10-E1062-APP | Component | X2 proposal with confidence 0.72 |
| TC-E1-062-07 | No criterion here for the repeated event; this service writes nothing on either delivery, which AC4 asserts | Component | EV-16 for document D-1001 twice |
| TC-E1-062-08 | No criterion here; the code guardrail belongs to RWB-P10-E1062-APP | Component | Model stub returns code X9 |
| TC-E1-062-09 | No criterion here; the model timeout and the run status belong to RWB-P10-E1062-APP | NFR | Model stub silent 61 seconds |
| TC-E1-062-11 | AC2: the open rows of the case and the answer limit | Component | Case RW-2026-000502 on the gateway-bff and rwb-case fakes in open and cleared states; the answer-limit fake with the maximum and with a value absent |
| TC-E1-062-12 | Contract: the answer and the errors of GET /deviations against rwb-deviation.yaml (200, 401, 403, 422, 503) | Contract | Case RW-2026-000403 on the rwb-access fake; case identifier absent and malformed; a downstream unavailable at steps 4 and 5 |
| TC-E1-062-13 | Boundary: every statement of the read sits in rwb_deviation and reads only the tables of section 12.7 | Component | The build check; a statement on rwb_case and a statement on a v_ace_* view |
| TC-E1-062-14 | AC2: every open code of the case is in one answer, read in one call | Component | Case RW-2026-000502 with X3 open and X6 open; one call to the read |
| TC-E1-062-15 | AC6: a read with no case reference is refused with 422 and no read | Component | `caseId` absent; no case reference on the call |
| TC-E1-062-16 | AC7: a budget miss or no package version in force answers 503 with no partial answer | Component | Reference-data fake silent beyond the 2 s budget; rule-package fake with no version in force |
| TC-E1-062-17 | AC8: the policy read does not answer, so the raise is refused with 503 and never read as raise | Component | rwb-agent fake silent for policy "SCREENING"; raise request for X2 |
| TC-E1-062-18 | AC9: a statement on a recovery_case row, a rwb_case table, a v_ace_* view or another service's schema fails the build | Component | The build check run on each statement in turn |
| TC-E1-062-19 | AC13: a statement on a recovery_case row, a rwb_case table or a v_ace_* view is refused by the database grant at run time | Component | The SY-AGENT login issues a statement on recovery_case, on rwb_case and on a v_ace_* view |
| TC-E1-062-20 | AC14: the rules BR1, BR2 and BR4 to BR8 of section 8 hold on the answer, the build and the log | Component | A synthetic personal value in handler_user_id and in a free-text column; the read run twice on the same rows and package version; the build check run on the service source |
| TC-E1-062-21 | AC15: a call without a valid credential to a provided operation answers 401 | Contract | GET /deviations for case RW-2026-000403 with no credential; each further provided operation of rwb-deviation.yaml with no credential |

The ten legacy cases of RWB-E1-062 are listed in their legacy order with the Level column added, and each names the slice of behaviour this story answers: the masked estate and the shadow absence for TC-E1-062-01, the owner projection for TC-E1-062-04 and the refusal for TC-E1-062-10; every other case is the agent's and is listed with no criterion here. The legacy table publishes no level, so one is assigned per case: legacy "System" maps to Component for a single-service half and to End to end where the case crosses services, "Access" maps to Component, and the timeout case to NFR (GAP-3085; ASM-5260). The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same ID. No `-ITG` copy is written here: the same values across rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-agent are RWB-ITG-E1062-ITG's.

Volume (GAP-1833): this module states no deviation, screening or queue volume. Not specified in the source documents (GAP-1833).

### 17. Guardrails

- No business value in code: the codes, the actor values, the owner roles, the "unmapped" marker and the answer limit are rows, parameters or configuration, read with their version. A build check fails on a code, an owner role or the marker in the source.
- No personal data in the answer, an event, a workflow input or a log: identifiers, codes, states, dates, a boolean and a rule version only. `handler_user_id` is not returned, and a property test asserts that a synthetic personal value never reaches the JSON, a log line or a span attribute.
- ACE data only through the owner's contract or a `v_ace_*` view: this service holds no `v_ace_*` grant and reads no ACE table, and the answer needs no ACE product at all.
- No cross-schema read and no cross-schema key: `rwb_deviation` holds the row, `case_id` is a reference, and a statement on `rwb_case`, `rwb_agent` or `rwb_decision` fails the boundary test (DP-01).
- The ledger is not this service's: no interaction row is read, written or copied, and no ledger listener of this slice exists (DP-18).
- One event owner per fact: this slice publishes nothing, and a build that writes an outbox row for a shadow run fails the acceptance test (DP-09, BR4).
- One base, one topic, one queue, one schema and one login per service; no document names another service's base or topic as its own (DP-13, DP-14).
- The agent runtime is never embedded and never called back: this service consumes the policy read of RWB-P10-E1062-CON and calls nothing else of rwb-agent (DP-20).
- Any migration is a step in the per-service Flyway sequence of `rwb_deviation`, versioned and repeatable, and touches no other schema (DP-15).
- No retired element is reintroduced: no Quartz row, no shared job table, no monolith base and no data-lake export.

### 18. Traceability

| Requirement ID | Requirement (short) | Story element | Test cases | Feature | L3 process |
|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags (Business Requirements Program, section 5.15; FEAT-DVH-01, FEAT-AGT-08) | The open estate of the case, so the detection is measured on the deviations the case actually carries | TC-E1-062-01, TC-E1-062-11 | FEAT-DVH-01, FEAT-AGT-08 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager (FEAT-DVH-04) | The owner projection over R-DEV-02 to R-DEV-06, with "RW-TEAMMGR" and "unmapped" for a code without a row | TC-E1-062-04 | FEAT-DVH-04 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |
| REQ-DVH-007 | A complaint is matched to the contact before it (FEAT-DVH-08) | Not answered here: the ledger window is rwb-source-data's and this answer carries no interaction | TC-E1-062-05 (no criterion here) | FEAT-DVH-08 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |
| D-RCV-60 DP-01 | The row and the view are this service's, and no other service's table is read | `deviation` and `v_open_deviation` in `rwb_deviation`, the boundary test | TC-E1-062-01, TC-E1-062-10, TC-E1-062-13 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |
| D-RCV-60 DP-04 | The owner role is evaluated in the embedded kit with the package of rwb-decision | `DeviationOwnerProjection` and the package read | TC-E1-062-04 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |
| D-RCV-60 DP-13 | The read is served on the base of the service | `GET /api/recovery/deviation/v1/deviations` | TC-E1-062-01, TC-E1-062-10, TC-E1-062-12 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |
| D-RCV-60 DP-20 | The autonomy mode is read on the rwb-agent contract and the runtime is never embedded | `ScreeningRaiseGate` and `AgentPolicyClient` | TC-E1-062-01 | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) | Not specified in the source documents (DOR-RWB-S8-E1062-APP-2) |

| Legacy reference | Where it is kept |
|---|---|
| Legacy story RWB-E1-062 — the deviation estate the run reads and the shadow rule (section 2; section 4 step 3; section 11 DF-CAS-038 and DF-CAS-019; BR1, BR3; AC4; the access case) | Sections 1, 2, 4, 7, 8, 11, 16 |
| Legacy values reused — "RW-FRAUD" from R-DEV-04 for X4, "RW-TEAMMGR" and "unmapped", the policy "SCREENING" version with floor 0.80, cases RW-2026-000401 to RW-2026-000404 and RW-2026-000502, the date 2026-12-10 | Background, sections 7 to 16 |
| MSG-P4-002, MSG-GEN-001, MSG-GEN-006 | Section 14, exception paths |
| TC-E1-062-10, TC-E1-062-01 to TC-E1-062-09 | Section 16 |
| Legacy criteria AC1 to AC9 | Owned by RWB-P10-E1062-APP; not restated here (section 7) |

### 19. Out of scope

- The agent runtime, the policy "SCREENING" and its versions, the prompt "PR1", the output schema "screening-v1", the guardrail checks, the per-proposal owner resolution, the evaluation and the run states: RWB-P10-E1062-APP and the contract RWB-P10-E1062-CON.
- The documents and extracted fields the run reads, and the `DocumentStored` event that starts a run: RWB-P5-E1062-APP.
- The masking policy itself, its versions and its field list: RWB-P4-E1062-APP; this slice consumes the decision and applies it.
- Raising, routing, pausing, handling, contact stopping and clearing a deviation, and the two write operations of the service: the Epic 2 stories of this service (FEAT-DVH-01 to FEAT-DVH-06) and the Epic 7 flows.
- The deviation screens SCR-06 and SCR-08 and their states: the other stories of this service.
- The L1 live screening on one segment and the feedback of a confirmed proposal: the Epic 2 story of this key (RWB-E2-029).
- The end-to-end proof of these values across rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-agent: RWB-ITG-E1062-ITG.
- The `rwb_deviation` schema baseline, the platform migration role, the `rwb.deviation.events.v1` topics and consumer groups, the observability and the runbook of this service.
