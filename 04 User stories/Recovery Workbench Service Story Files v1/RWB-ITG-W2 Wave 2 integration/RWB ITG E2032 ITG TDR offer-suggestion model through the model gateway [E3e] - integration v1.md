# RWB-ITG-E2032-ITG TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E2032-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W2 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-ITG-W2 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P3-E2004-APP, RWB-P10-E2032-APP, RWB-S2-E2032-APP, RWB-P7-E2032-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-032 for the wave 2 integration harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **a repeatable cross-service journey harness for the TDR offer-suggestion model at E3e — a restructure treatment opening, the policy in force deciding whether a suggestion is attempted, the call through the model gateway on the 60 s policy timeout, the answer checked against `tdr-offer-v1`, the D5 record written before the suggestion returns, and the suggestion read back with its model code and version, or MSG-P10-007 — with the evidence pack attached to the wave 2 release**, so that **one suggestion, one agent run and one D5 record are proven to describe the same treatment on the same model version before RWB-S2-E2032-APP, RWB-P10-E2032-APP, RWB-P7-E2032-APP and RWB-P3-E2004-APP claim Done**.

This story builds the harness, its contract fakes, its seed pack and its TDR model stub, its evidence pack and its pass or fail gate. It builds no production endpoint, no screen, no table and no migration. Nothing it writes is deployed to a service.

No single app story can prove the journey. RWB-S2-E2032-APP can prove that the treatment record exists and that a restructure treatment opens. RWB-P10-E2032-APP can prove that the policy in force is read, that the model is called through the gateway and the private endpoint, that the answer passes the `tdr-offer-v1` check and that an agent run is stored. RWB-P7-E2032-APP can prove that a D5 record is written and that the ledger read returns it. RWB-P3-E2004-APP can prove the case record and the account facts the journey reads through the case contract. The agreement between the four of them — one suggestion, one run and one D5 record describing the same treatment on the same model version, with no treatment transaction waiting on a model — is this story, and only this story.

### 2. Business rationale

RWB-E2-032 split into four app stories and this integration story. RWB-S2-E2032-APP builds the treatment record, the open restructure treatment and the suggestion area behind the treatment read. RWB-P10-E2032-APP builds the policy in force, the gateway call, the output schema check, the guardrail, the agent run and the agent-output read. RWB-P7-E2032-APP builds the D5 mapping and the ledger read. RWB-P3-E2004-APP carries the case record and the account facts the journey starts from. What no app story can prove on its own is the chain the business relies on, and the business relies on all of it at once.

The chain is this. A restructure treatment opens on the treatment service. The policy in force decides whether a suggestion is attempted at all: mode OFF makes no call and returns nothing, mode L1 attempts it. The call goes through `ModelGatewayClient` with the 60 s timeout held on the policy row, not in code. The answer is checked against `tdr-offer-v1`. The D5 record is written before the suggestion is returned, so a suggestion a reader can see always has a ledger entry behind it. The treatment screen then shows the terms with the model code and version, or MSG-P10-007 when there is no suggestion. That is the journey this harness proves.

The journey carries two requirements. A treatment record holds every offer's type, terms, approval and outcome (REQ-CHO-006): the harness asserts that the suggestion it reads back sits on the treatment record beside the officer's own offer fields and is never copied into them. Every decision records the rule, model, agent and prompt versions (REQ-DRI-001): the harness asserts that the D5 record names model version "TDR-OFFER-1.0" and the inputs reference, so a reader of the ledger can tell which model produced the recommendation that the officer saw.

The D5 decision is the anchor. Legacy section 12 gives the mapping: case_id, decision code "D5", the model version, no agent version, the masked inputs snapshot as the inputs reference, the suggestion as the recommendation, final call "SUGGESTION_RECORDED", and the treatment ID and run ID in the actions. The harness exercises that mapping across rwb-agent and rwb-decision, so a change to the mapping on either side is caught before an officer sees a suggestion that no ledger entry supports.

Architecture v5 changes the path, not the business. In the monolith the suggestion client, the run row and the decision log sat in one deployment and one schema, called in process and waited on. In the target:

- the account and the treatment come through the owning services' contracts, and the harness reads no `recovery` schema table at any point (DP-01);
- the D5 record is a local decision record published on the shared topic `rwb.decision-record.v1` and held in the ledger by rwb-decision (DP-03);
- the account facts behind the suggestion — principal outstanding, days past due, balance, interest rate and the last 12 months of payments — come through the owning service's contract, never from an ACE view the harness reads itself (DP-05);
- the policy versions, the record modes, the output schema limits and the 60 s timeout are parameters and data, loaded and seeded, never values in the harness (DP-06);
- the autonomy modes "OFF" and "L1", the run statuses, the guardrail check name, the decision code "D5" and the final call are reference data served from files (DP-07);
- the completion and the ledger write are CloudEvents observed on the owner's topic, with an outbox on the producer and an inbox on the consumer, so a duplicate never counts twice (DP-09);
- the request is one hop on the rwb-agent contract with the 2 s REST budget, the model call itself stays inside `AgentRunWorkflow` with the 60 s policy timeout, and the stored output plus the D5 record are read back through the agents' and the ledger's contracts, so no treatment transaction waits on a model (DP-11);
- every path is on the owner's base `/api/recovery/<short>/v1` (DP-13);
- the treatment screen and the journey reach the services through the gateway-bff composite route, so the harness drives the same route the screens use (DP-19).

DP-11 is the pattern that changed the most, and it is stated plainly here. The monolith called `ModelSuggestionClient` in process and waited for the answer inside the treatment transaction. In the target the treatment side does not call rwb-agent that way: the request is one hop on the rwb-agent contract with the 2 s REST budget, the model call stays inside `AgentRunWorkflow` with the 60 s policy timeout, and the suggestion is read back through the stored agent output and the D5 record rather than held open in the treatment transaction. That is the assumption of section 3. The start operation itself is the one open point: Architecture v5 slide 13 gives the treatment row no call to rwb-agent, slide 16 starts agent runs only from `CaseCreated` and `DocumentStored`, and the Ownership Map has no rwb-agent operation that starts a suggestion run. It is recorded as a Conflict gap (GAP-0414) and agreed between the two owners at the wave 2 entry check. Until it is published, the harness reports this journey as blocked, never as passed.

The measure is the journey evidence: for each owned criterion, one pass or fail with the treatment, the suggestion, the run, the decision record and the fallback flag captured in one report that can be re-run for any build.

### 3. Preconditions

- The wave 2 harness environment (SIT) is available with the gateway route for `/api/recovery/*`, the topic `rwb.agent.events.v1` and the shared topic `rwb.decision-record.v1`, the Temporal namespace `rwb-recovery` with the queues `rwb-agent` and `rwb-treatment`, and the private endpoint test profile that stands in for the TDR model (INT-23).
- The four integration dependencies have published their contracts, or their contract fakes stand in for them: RWB-S2-E2032-APP (rwb-treatment, the treatment record, the open restructure treatment and the suggestion area), RWB-P10-E2032-APP (rwb-agent, the policy in force, the gateway call, the output schema check and the agent run), RWB-P7-E2032-APP (rwb-decision, the D5 mapping and the ledger read) and RWB-P3-E2004-APP (rwb-case, the case record and the account facts the journey reads).
- Policy "TDR_OFFER" version "P1" is in force with mode "OFF" and review date 2027-02-28; version "P2" is in force with mode "L1", model version "TDR-OFFER-1.0", output schema "tdr-offer-v1" and timeout 60 seconds, loaded by RW-COE and approved by RW-RISK (legacy sections 3 and 7).
- Restructure treatment "T-1001" is open on case "RW-2026-001001", the account holds principal outstanding 1,250,000.00 baht and 120 days past due, and treatment "T-1002" has type "SETTLEMENT" (legacy sections 4 and 7).
- The TDR model stub answers the suggestion of 84 installments of 18,900.00 baht with model version "TDR-OFFER-1.0", stays silent for 61 seconds, and answers installments -12 — one control per scenario, never in the same run (legacy AC1, AC4, AC5). The rwb-decision fake answers unavailable for AC6 (legacy AC6).
- The feature switch `rwb.agent.tdr-suggestion` is on in the harness profile (legacy section 13).
- Synthetic cases, synthetic treatments and masking tokens only: no customer name, account number, national identifier or contact detail enters the harness, the seed pack, the events, the logs or the evidence pack (legacy section 17).
- Not specified in the source documents (GAP-0414; ASM-0589): the start operation that begins a suggestion run, the harness environment and its seeding, the TDR model stub and its 61 s and -12 controls, the OFF-policy fixture, the evidence format and retention, and the pass or fail gate.
- No build dependency. Day 1.

### 4. Flow

1. Harness: takes the run lock for the environment and records the build ID, the business date and the versions of the four contracts it is about to exercise.
2. Harness: seeds case "RW-2026-001001", the account facts (principal outstanding 1,250,000.00 baht, 120 days past due), restructure treatment "T-1001", settlement treatment "T-1002", and both policy versions — "TDR_OFFER" P1 mode OFF with review date 2027-02-28, and P2 mode L1 with model version "TDR-OFFER-1.0", output schema "tdr-offer-v1" and timeout 60 seconds.
3. Harness: calls the P4 session operation against the rwb-access fake and records the role, the scope and the rights the journey runs under.
4. Harness: subscribes to `rwb.agent.events.v1` and the shared topic `rwb.decision-record.v1` with its own consumer group before the treatment is opened, so the run window starts before the call.
5. Harness: opens the restructure treatment through `POST /api/recovery/treatment/v1/cases/{caseId}/treatments`, or lets the rwb-treatment fake accept it where RWB-S2-E2032-APP has not landed, and records which of the two paths was used.
6. Harness: waits for `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` inside the run window, or reads the stored output through `GET /api/recovery/agent/v1/cases/{caseId}/agent-outputs` when the event has not arrived inside the window, and records which of the two paths proved the run.
7. Harness: reads the run through `GET /api/recovery/agent/v1/admin/agent-runs` and records the status, agent code, model version, autonomy mode, idempotency key, fallback flag, guardrail result and decision log id.
8. Harness: reads the treatment through `GET /api/recovery/treatment/v1/treatments/{treatmentId}` and asserts the suggestion of 84 installments of 18,900.00 baht with model code "TDR_OFFER" and model version "TDR-OFFER-1.0", or MSG-P10-007 in the suggestion area, and that the offer fields are untouched.
9. Harness: reads `GET /api/recovery/decision/v1/decision-log` and asserts one D5 record with the model version, the inputs reference and the suggested terms, before the decision log id on the run row is asserted against it.
10. Harness: repeats step 5 for the same treatment and asserts that the first suggestion and its decision record id return and that no second run exists for the key "TDR_OFFER:<treatmentId>".
11. Harness: runs the OFF policy, the 61 s silence, the installments -12 answer, the decision-log failure and the settlement treatment as separate scenarios against the same contracts, and records the message and the run status of each.
12. Harness: writes the per-scenario evidence into one run report keyed by story key and business date, evaluates the gate, attaches the report to the wave 2 release record, releases the lock and restores the seed.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model is not in service (mode OFF) | No call and no decision record; the treatment read carries the message in the suggestion area | MSG-P10-007 | AC2 |
| X2 | The model does not answer within 60 seconds | The run holds status "TIMED_OUT"; no suggestion and no D5 record; the treatment continues (R-UNI-32) | MSG-P10-007 | AC4 |
| X3 | The answer fails the output schema | The run holds status "GUARDRAIL_FAILED"; no suggestion is returned | MSG-P10-007 | AC5 |
| X4 | The decision log write fails | No suggestion is returned; the run is kept without a decision link and the incident is raised under R-UNI-39 by the service, not by the harness | MSG-P7-003 | AC6 |
| X5 | The same treatment asks again | The first suggestion and its decision record id return; no second call is made (R-UNI-40) | None to a user | AC7 |
| X6 | The treatment type is not RESTRUCTURE | No call, no suggestion and no run | None to a user | AC8 |
| X7 | A role without the right reads the agent runs | The read answers 403 | MSG-P4-002 | AC9 |
| X8 | The seed pack cannot be loaded (case not seeded, policy version absent, treatment type missing, stub control off) | The run refuses to start and names the missing seed item; no scenario is reported | None | All |
| X9 | The start operation of the Conflict gap is not published | The journey is reported blocked and no scenario is reported as passed | None | AC1 |
| X10 | The evidence pack cannot be attached to the release record | The run is marked failed and the local evidence file is kept for rerun | None | All |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the four published contracts or their fakes, the policy fixtures, the TDR model stub and the private endpoint test profile; it builds no service feature and has no build dependency |
| Negotiable | The scenarios, the seeded values, the policy versions, the timeout, the schema limits and the stub controls are data files, never code |
| Valuable | The offer-suggestion journey is proven once across four services, with the D5 record and the model version in the same evidence as the suggestion |
| Estimable | One journey runner, one fake set, one fixture pack, three assertion helpers, one evidence collector, one gate |
| Small | Fits in one sprint with its tests |
| Testable | Each owned criterion has a fixed Given, When and Then and a recorded pass or fail in the report |

### 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion model through the model gateway [E3e]

  Background:
    Given restructure treatment "T-1001" is open on case "RW-2026-001001"
    Given the account has principal outstanding 1,250,000.00 baht and 120 days past due

  Scenario: AC1 The suggestion is exposed with its model version (new, D-RCV-60)
    Given policy "TDR_OFFER" version "P2" with mode "L1", model version "TDR-OFFER-1.0", output schema "tdr-offer-v1" and timeout 60 seconds
    When the harness opens restructure treatment "T-1001" and the run completes
    Then `GET /api/recovery/treatment/v1/treatments/{treatmentId}` returns the suggestion of 84 installments of 18,900.00 baht with model version "TDR-OFFER-1.0"
    Then one agent run row and one decision record exist with decision "D5", model version "TDR-OFFER-1.0" and final call "SUGGESTION_RECORDED"
    Then the evidence records that the run ended on the model answer and not on the rule fallback

  Scenario: AC2 The model is not in service (new, D-RCV-60)
    Given policy "TDR_OFFER" version "P1" with mode "OFF" and review date 2027-02-28
    When the harness opens restructure treatment "T-1001"
    Then no model call is made, no suggestion returns and no decision record is written
    Then `GET /api/recovery/treatment/v1/treatments/{treatmentId}` answers MSG-P10-007 in the suggestion area
    Then `GET /api/recovery/agent/v1/admin/agent-configs` shows version "P1" with mode "OFF" and review date 2027-02-28

  Scenario: AC3 The suggestion is logged before it is returned (new, D-RCV-60)
    Given a suggestion was recorded for treatment "T-1001"
    When the harness reads the decision record and the treatment
    Then the D5 record holds model version "TDR-OFFER-1.0", the inputs reference and the suggested terms
    Then the treatment read shows "Suggested by TDR_OFFER, version TDR-OFFER-1.0"
    Then the decision log id on the run row and the id read from the ledger are the same

  Scenario: AC4 The model does not answer (new, D-RCV-60)
    Given the TDR model stub does not answer for 61 seconds
    When the harness opens restructure treatment "T-1001"
    Then the agent run holds status "TIMED_OUT" and fallback true
    Then no suggestion and no decision record exist and the treatment read answers MSG-P10-007

  Scenario: AC5 An answer that fails the schema (new, D-RCV-60)
    Given the TDR model stub returns installments -12
    When the guardrail runs
    Then the agent run holds status "GUARDRAIL_FAILED" with check "SCHEMA" and no suggestion is returned

  Scenario: AC6 The decision cannot be recorded (new, D-RCV-60)
    Given the rwb-decision fake answers unavailable
    When the model answers for treatment "T-1001"
    Then no suggestion is returned and the treatment read answers MSG-P7-003
    Then the agent run holds no decision log id

  Scenario: AC7 The same treatment asks twice (new, D-RCV-60)
    Given a suggestion was recorded for treatment "T-1001" with one decision record
    When the harness opens restructure treatment "T-1001" a second time
    Then the first suggestion and its decision record id return
    Then no second run exists for the key "TDR_OFFER:<treatmentId>"

  Scenario: AC8 Not a restructure (new, D-RCV-60)
    Given treatment "T-1002" has type "SETTLEMENT"
    When the harness opens it
    Then no model call is made and no suggestion returns
    Then no agent run exists for it

  Scenario: AC9 A role without the right reads the runs (new, D-RCV-60)
    Given a test user holds role RW-PHONECOL with Case record R only
    When the user requests `GET /api/recovery/agent/v1/admin/agent-runs`
    Then the answer is 403 with MSG-P4-002
```

No legacy acceptance criterion is owned by this story: the nine above are new and test only the integration deliverable, using the legacy values of RWB-E2-032 and no other.

### 8. Business rules

| ID | Rule | Source | Proved by |
|---|---|---|---|
| BR1 | The TDR model is reached only through the model gateway on the private endpoint | DL33; integration INT-23 | AC1, AC5 |
| BR2 | Mode OFF returns no suggestion and makes no call; the review date is held on the policy row | agent_policy.autonomy_mode, review_date | AC2 |
| BR3 | A suggestion is returned only after its decision record is written | Principle 5; R-UNI-39; CTL-06 | AC3, AC6 |
| BR4 | A timeout or a failed check gives no suggestion and the treatment continues | R-UNI-32 | AC4, AC5 |
| BR5 | One suggestion per treatment; the key is "TDR_OFFER:<treatmentId>" | R-UNI-40 | AC7 |
| BR6 | The model is called only for treatment type RESTRUCTURE | treatment.treatment_type | AC8 |
| BR7 | The suggestion is advice; the officer builds and submits the offer | Agent catalogue, settlement and restructure agent; R-RES-09, R-RES-10 | AC1, AC3 |

The rules are unchanged by the split. The harness asserts them across the service boundaries and restates none of them in code: the model code, the model version, the output schema limits, the timeout, the review date and the autonomy modes are seeded data.

### 9. State transitions

None for the case and none for the treatment. This story changes no case status and no treatment status; the harness asserts that a suggestion, a timeout, a failed check or a repeat request never moves the treatment out of its draft state and never writes the suggestion into the offer fields.

The story writes an agent run and, when a suggestion returns, one decision record. The run carries the status rwb-agent gives it, and the harness asserts only the three the legacy story names: "ANSWERED" for a completed run, "TIMED_OUT" with fallback true for a run that reached the 60 s limit, and "GUARDRAIL_FAILED" with check "SCHEMA" for an answer that fails `tdr-offer-v1`.

The harness adds run states of its own only: Not started, Running, Blocked, Passed, Failed, with the latest run for a build deciding the gate. Blocked is the state of this journey while the start operation of the Conflict gap is unpublished.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT | Reads the suggestion on SCR-14 with its model code and version and builds the offer himself (Treatment and offer R) |
| RW-CASEOWN | Reads the suggestion on SCR-14 (Treatment and offer R) |
| SY-CASEWF | Calls the suggestion path from the treatment service, through the agreement recorded in section 3 |
| SY-AGENT | Reads the case and account facts and stores the run and the output (read only to the harness) |
| SY-DECLOG | Writes the D5 record the harness asserts, through rwb-decision's contract only |
| RW-COE | Loads the TDR_OFFER policy versions (Rules and parameters C) |
| RW-RISK | Approves the TDR_OFFER policy versions (Rules and parameters A) |
| Integration lead | Agrees the fake set, the TDR model stub and the run window with the four service owners |
| QA lead | Owns the seed pack, the evidence format and the pass or fail gate |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-TRT-001 | treatment | id | Read through the S2 treatment operation |
| DF-TRT-002 | treatment | case_id | Read through the S2 treatment operation |
| DF-TRT-004 | treatment | treatment_type | Read through the S2 treatment operation (AC8) |
| DF-ACC-009 | v_ace_account | principal_outstanding | Seed data; read back through the P3 case operation (DP-05) |
| DF-ACE-020 | v_ace_account | total_balance | Seed data; read back through the P3 case operation (DP-05) |
| DF-ACE-018 | v_ace_account | days_past_due | Seed data; read back through the P3 case operation (DP-05) |
| DF-ACE-025 | v_ace_account | interest_rate | Seed data; read back through the P3 case operation (DP-05) |
| DF-ACE-045 | v_ace_payment | payment_date | Seed data; read back through the P3 case operation (DP-05) |
| DF-ACE-046 | v_ace_payment | payment_amount | Seed data; read back through the P3 case operation (DP-05) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read through the P7 decision log operation; written by rwb-decision through its own contract, never by the harness |
| DF-AGT-004 | agent_policy | model_code | Read through the P10 agent-configs operation |
| DF-AGT-005 | agent_policy | model_version | Read through the P10 agent-configs operation |
| DF-AGT-006 | agent_policy | output_schema_ref | Read through the P10 agent-configs operation |
| DF-AGT-008 | agent_policy | autonomy_mode | Read through the P10 agent-configs operation |
| DF-AGT-012 | agent_policy | timeout_seconds | Read through the P10 agent-configs operation |
| DF-AGT-016 | agent_policy | review_date | Read through the P10 agent-configs operation (AC2) |
| DF-AGT-036 | agent_run | id | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-037 | agent_run | agent_code | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-040 | agent_run | model_version | Written by rwb-agent; read through the P10 agent-runs operation (AC1) |
| DF-AGT-041 | agent_run | case_id | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-042 | agent_run | subject_id | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-043 | agent_run | autonomy_mode | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-045 | agent_run | idempotency_key | Written by rwb-agent; read through the P10 agent-runs operation (AC7) |
| DF-AGT-046 | agent_run | status | Written by rwb-agent; read through the P10 agent-runs operation (AC4, AC5) |
| DF-AGT-047 | agent_run | fallback | Written by rwb-agent; read through the P10 agent-runs operation (AC4) |
| DF-AGT-048 | agent_run | guardrail_result | Written by rwb-agent; read through the P10 agent-runs operation (AC5) |
| DF-AGT-049 | agent_run | output | Written by rwb-agent; read through the P10 agent-outputs operation (AC1, AC3) |
| DF-AGT-051 | agent_run | latency_ms | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-056 | agent_run | run_at | Written by rwb-agent; read through the P10 agent-runs operation |
| DF-AGT-058 | agent_run | decision_log_id | Written by rwb-agent; read through the P10 agent-runs operation (AC3, AC6) |

The harness owns no table in any schema and no schema at all: no table, no view, no migration and no seed table is created by this story. It reads and writes only through the operations of section 12, and its own evidence holds identifiers, statuses, message ids, model versions and timestamps only, never personal data. Per-service Flyway belongs to the services under test, not to the harness, and no migration is run by this story. Field IDs are those of the Logical Data Model and Data Dictionary.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test asset in the integration pipeline and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/treatment/v1/cases/{caseId}/treatments` | S2 rwb-treatment | Opens the restructure treatment "T-1001" and the settlement treatment "T-1002"; the start point of the journey (AC1, AC2, AC4, AC5, AC6, AC7, AC8) |
| GET | `/api/recovery/treatment/v1/treatments/{treatmentId}` | S2 rwb-treatment | Reads the treatment, the suggestion area with the terms, the model code and version, or MSG-P10-007 (AC1, AC2, AC3, AC4) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the case and the seeded account facts the journey starts from (AC1) |
| GET | `/api/recovery/agent/v1/cases/{caseId}/agent-outputs` | P10 rwb-agent | Reads the stored suggestion and the run output when the completion event has not arrived inside the run window (AC1, AC3, AC4) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | Reads the run: status, agent code, model version, autonomy mode, idempotency key, fallback flag, guardrail result and decision log id (AC1, AC4, AC5, AC6, AC7, AC8, AC9) |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | Reads the TDR_OFFER version, mode and review date (AC2) |
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Asserts the D5 record, its model version, its inputs reference and the suggested terms (AC1, AC3, AC6, AC7) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s timeout, and the one POST carries an If-Match and a key per scenario; the key "TDR_OFFER:<treatmentId>" belongs to the service and is only asserted here. The treatment side has no rwb-agent operation to start the suggestion run in the target matrix — Architecture v5 slide 13 gives S2 no call to P10 and the Ownership Map has none — so the start operation is the one open point recorded as a Conflict gap (GAP-0414) and agreed as stated in section 3. The P4 session operation is called against the rwb-access fake only (12.8) and reads the role and rights under which the journey runs.

#### 12.3 Events published

None. The harness publishes no Kafka event on a production topic; the evidence goes to the release record through the pipeline.

#### 12.4 Events consumed

| Event | Topic | Owner | Use |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Closes the run window and gives the run ID, the status and the fallback flag before the output and run reads (DP-09, DP-11) |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision | Asserts that the D5 record reached the shared topic inside the run window, alongside the ledger read of 12.2 (DP-03, DP-09) |

The harness consumes with its own consumer group and never reads a producer's outbox, inbox or schema.

#### 12.5 Workflows and activities

`AgentRunWorkflow` on queue `rwb-agent` is exercised, not built: the model call sits inside the workflow with the 60 s policy timeout and then the rule result (R-UNI-32), and the harness asserts which of the two a run ended on through the status and the fallback flag (AC1, AC4). JOB-11 Outbox sender is observed on its every-minute window, so the harness knows when a produced event should have crossed the topic.

The harness starts no workflow, adds no activity and writes no schedule. The start of the run belongs to RWB-P10-E2032-APP and the treatment side to RWB-S2-E2032-APP, under the agreement recorded in section 3.

#### 12.6 Schedules

None. The harness adds no workflow and no schedule; the 60 s limit is inside `AgentRunWorkflow` and JOB-11's every-minute window is the platform's, both only observed.

#### 12.7 Tables owned

None. The harness owns no table in any schema and no schema of its own; it reads and writes through the operations of 12.2 only.

#### 12.8 Contract fakes

| Fake | Serves | Contract | What it answers |
|---|---|---|---|
| WireMock rwb-treatment | The two S2 operations of 12.2 | OpenAPI of S2 | The open restructure treatment "T-1001" and the settlement treatment "T-1002" of type "SETTLEMENT"; the suggestion area with model code "TDR_OFFER" and version "TDR-OFFER-1.0", or MSG-P10-007; the treatment state unchanged by the suggestion; keeps the request journal for the repeat assertion |
| WireMock rwb-agent | The three P10 operations of 12.2 | OpenAPI of P10 | The stored suggestion, the run with status "TIMED_OUT" and fallback true, the run with status "GUARDRAIL_FAILED" and check "SCHEMA", the run with no decision log id, the OFF policy in the configs read, and the empty run list for the settlement treatment |
| WireMock rwb-decision | `GET /api/recovery/decision/v1/decision-log` | OpenAPI of P7 | The D5 record with model version "TDR-OFFER-1.0", the inputs reference and the suggested terms; 503 for AC6 |
| WireMock rwb-case | `GET /api/recovery/case/v1/cases/{caseId}` | OpenAPI of P3 | Case "RW-2026-001001" with the seeded account facts, principal outstanding 1,250,000.00 baht and 120 days past due |
| WireMock rwb-access | The P4 session operation | OpenAPI of P4 | The role, the scope and the Treatment and offer right of the restructuring officer, and the RW-PHONECOL test user with Case record R only (MSG-P4-002) |
| TDR model stub | The model call rwb-agent makes | The INT-23 contract, not in this workspace | 84 installments of 18,900.00 baht with model version "TDR-OFFER-1.0", 61 seconds of silence for AC4, the answer with installments -12 for AC5, and masking tokens in place of identifiers |

Each fake is replaced by the real service as its integration dependency lands, without a change to the scenarios. Not specified in the source documents (GAP-0414; ASM-0589): the fake set, the TDR model stub and its 61 s and -12 controls, the OFF-policy fixture, the harness environment and seeding, the evidence format and retention, and the pass or fail gate.

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop on the owner's base with the 2 s timeout; the P4 session operation is called against the fake only and is not a production path of this story |
| Kafka | 2 events consumed on `rwb.agent.events.v1` and `rwb.decision-record.v1`; none published on a production topic |
| Temporal | Observed only: `AgentRunWorkflow` on queue `rwb-agent` with the 60 s policy timeout and the rule result behind it; no workflow, activity or schedule added |
| File | None |

### 13. Solution plan

**Package.** Folder `integration/recovery-agent-tdr` in the ACE repository, package `<ACE base package>.recovery.integration.agenttdr`. Not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | How this harness applies it |
|---|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | The harness holds no schema and reads no table: the treatment, the case, the run and the D5 record come through the operations of 12.2 |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON | The D5 record is read through rwb-decision and the `DecisionRecorded` event is read on the shared topic; the harness never reads a decision table |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none | The account facts behind the suggestion — principal outstanding, days past due, balance, interest rate and payments — are seeded and read back through the case contract, never from an ACE view |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The policy versions, the timeout, the output schema limits and the review date are parameter data loaded from files, never values in the harness |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The autonomy modes, the run statuses, the guardrail check name, the treatment types, the decision code "D5" and the final call are seeded reference data |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | The harness subscribes with its own consumer group and asserts the two events, never a producer's table |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) | The request is one hop on the rwb-agent contract with the 2 s budget, the model call stays inside `AgentRunWorkflow` with the 60 s policy timeout, and the suggestion is read back through the stored output and the D5 record |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 uses the owner's base, so the harness never calls a monolith base |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | The journey runs through the gateway route the treatment screen uses, on the same bases |

The platform H dependencies in the table (H RWB-PLT-E1027-CON, H RWB-PLT-E1042-CON, H RWB-PLT-E1043-CON, H RWB-PLT-TE006-CON, H RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata: the harness converges on them and has no build dependency of its own. The blocking dependencies of this story are the four I stories, which replace the fakes with real services one at a time.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the twelve flow steps for one scenario and one business date and holds the run lock |
| FakeRegistry | Configuration | WireMock mappings for rwb-treatment, rwb-agent, rwb-decision, rwb-case and rwb-access, one set per contract version, plus the TDR model stub selection |
| TdrFixturePack | Data | The case, the account facts, the two treatments, both policy versions, the stub controls and the seeded state each scenario names |
| SuggestionAssertion | Service | Compares the suggested terms, the model code, the model version, the suggestion area and MSG-P10-007 against the fixture, and asserts that the offer fields are untouched |
| DecisionRecordAssertion | Service | Checks the D5 record, its model version, its inputs reference, its suggested terms, its final call and the run's decision log id, including the case where none exists |
| IdempotencyAssertion | Service | Repeats the open for the same treatment and checks the returned suggestion, the returned decision record id and the absence of a second run for the key "TDR_OFFER:<treatmentId>" |
| EvidenceCollector | Service | Writes one report keyed by story key and business date, with the treatment, the suggestion, the run, the decision record, the message and the fallback flag |
| GateEvaluator | Service | Passes the run when every owned scenario passes and the evidence pack is attached, and reports the journey blocked when the start operation is unpublished |

**Environment and test data.** SIT, the wave 2 harness profile, one business date, one synthetic case, two synthetic treatments and masking tokens only. The seeded values are the legacy section 7 Background, the two treatments, both policy versions and the three stub controls; no other value is added. Not specified in the source documents (GAP-0414; ASM-0589): the environment, the seed pack, the evidence format and retention.

**Build steps**

1. Write the TdrFixturePack with the Background, treatments "T-1001" and "T-1002", both policy versions and the three stub controls; test that a bad seed stops the run (X8).
2. Write the FakeRegistry with the five WireMock mapping sets and the TDR model stub selection, with the policy versions, the review date and the reference data loaded from files.
3. Write JourneyRunner for AC1: open the treatment, wait for `AgentRunCompleted` or read the stored output inside the run window, then assert the suggestion and the one run.
4. Add AC3 and AC6 with the decision-record-first ordering, the run's decision log id and the 503.
5. Add AC2 with the OFF policy and the configs read, AC7 with the idempotency key and AC8 with the settlement treatment.
6. Add AC4 and AC5 with the 61 s silence and the installments -12 answer, asserting "TIMED_OUT" with fallback true and "GUARDRAIL_FAILED" with check "SCHEMA".
7. Add AC9 with the RW-PHONECOL user, then write EvidenceCollector and GateEvaluator, attach the report to the wave 2 release record and rerun the nine scenarios on the release build.

**Feature switch.** `rwb.agent.tdr-suggestion` is on in the harness profile, as the legacy story sets it. Off, the suggestion read returns no suggestion and no call is made, and the harness reports the journey as not applicable rather than as passed. The harness itself is a pipeline stage selected by the run profile, not by a business flag.

**Done when.** The tests of section 16 pass, the run report is attached to the wave 2 release record with all nine owned scenarios, and each fake has been replaced by the real service where its I story has landed in SIT. AC1 passes against the TDR model stub until the TDR model is deployed; that is the legacy done condition and it is unchanged. Until the start operation of the Conflict gap (GAP-0414) is published by both owners, this journey is reported blocked, not passed. The fixture pack and the evidence sign-off wait for the values of the rows cited in sections 3, 12.8 and 15; not specified in the source documents (GAP-0414; ASM-0589): the environment, the seed pack and the evidence format.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-007 | No suggestion: model not in service, timeout or failed check | No offer suggestion is available for this treatment. The TDR model is not in service. |
| MSG-P7-003 | Decision log write failed | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The harness asserts these messages and never rewrites them. Its own report text is for the release team and is not part of the message standard.

### 15. Screens and states

SCR-14 Treatment record, in the draft state, carries the suggestion area beside the officer's offer fields: ready (the suggested terms with model code "TDR_OFFER" and model version "TDR-OFFER-1.0" and the line "Suggested by TDR_OFFER, version TDR-OFFER-1.0"), unavailable (MSG-P10-007), and unchanged (the officer edits the offer fields as before, with the suggestion never copied into them). In the submitted, approved, booked and broken states the suggestion area shows the recorded terms and no call is made.

No screen is built by this story. The harness drives the operations behind those states and asserts all three through the contracts: the suggestion present with its model version, absent with MSG-P10-007, and the offer fields untouched. The panel and its states belong to RWB-S2-E2032-APP. Not specified in the source documents (GAP-0414; ASM-0589): the labels and the layout of the suggestion area that the harness would assert.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-032-09-ITG | AC9, Access | Component | A test user holding role RW-PHONECOL with Case record R only requests the admin agent-runs read; refused with MSG-P4-002 |
| TC-E2-032-01-ITG | AC1, BR1, BR3 | Integration | Treatment T-1001, policy TDR_OFFER P2 mode L1, stub answer 84 installments of 18,900.00 baht |
| TC-E2-032-02-ITG | AC2, BR2 | Integration | Policy TDR_OFFER P1 mode OFF, review date 2027-02-28 |
| TC-E2-032-03-ITG | AC3, BR3 | Integration | Suggestion recorded on T-1001 with one D5 record |
| TC-E2-032-04-ITG | AC4, BR4 | Integration | Stub silent for 61 seconds |
| TC-E2-032-05-ITG | AC5, BR4 | Integration | Answer with installments -12 |
| TC-E2-032-06-ITG | AC6, BR3 | Integration | Decision log writer fails after the model answers |
| TC-E2-032-07-ITG | AC7, BR5 | Integration | Second request for T-1001 under the key TDR_OFFER:<treatmentId> |
| TC-E2-032-08-ITG | AC8, BR6 | Integration | Treatment T-1002 of type SETTLEMENT |
| TC-E2-032-10-ITG | AC6, BR3, Principle 5 | NFR | Decision record write forced to fail after the model answers; no suggestion; MSG-P7-003 |

Each `-ITG` case is the journey copy of the legacy case: the Given, When and Then are those of the app stories' cases, run across the four contracts and the TDR model stub. The app stories keep the unit and component copies of the same cases; TC-E2-032-09-ITG keeps the access level of the legacy case, because a role without the right is a property of the read and not of the journey.

### 17. Guardrails

- No business value in code: the model code, the model version, the output schema limits, the 60 s timeout, the review date, the autonomy modes and the decision code are data in the seed pack, never values in the harness.
- No personal data in the model request, the events, the workflow inputs, the logs or the evidence. The inputs reference is the masked snapshot, and the seed holds synthetic cases, synthetic treatments and masking tokens only.
- No read of another service's tables and no schema of the harness's own: the account and the treatment come through the owning services' contracts, and the harness runs no migration.
- The suggestion is never written into the offer fields or the treatment status: the harness asserts that the treatment record holds what was suggested beside what was offered, and that nothing moves because a suggestion returned or failed.
- The harness never calls the model endpoint directly: the model call belongs to `AgentRunWorkflow` inside rwb-agent, and the harness only drives the stub behind it as the INT-23 test profile.
- Each fake is replaced by the real service as its I story lands; a fake that outlives its service is a defect, not a configuration.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | Business Requirements Program, section 5.3 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-32, R-UNI-40 | TC-E2-032-02-ITG, TC-E2-032-04-ITG, TC-E2-032-05-ITG, TC-E2-032-07-ITG, TC-E2-032-08-ITG |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-032-01-ITG, TC-E2-032-03-ITG, TC-E2-032-06-ITG, TC-E2-032-09-ITG, TC-E2-032-10-ITG |

### 19. Out of scope

- Building or training the TDR model: it belongs to the TDR team, outside the Workbench, and the harness sees it only through the stub and the private endpoint test profile.
- The settlement and restructure agent proposing plan terms: shadow from Epic 2 and live from Epic 3, per the agent catalogue.
- Affordability and plan calculation in the ACE restructure calculator (R-RES-06).
- Production code of any service in the journey: the operations of rwb-treatment, rwb-agent, rwb-case, rwb-decision and rwb-access, their schemas and their screens belong to their own stories.

The harness, the fakes and the evidence pack cover the four items above only as a caller or a consumer would see them; building any of them is out of scope for this story.
