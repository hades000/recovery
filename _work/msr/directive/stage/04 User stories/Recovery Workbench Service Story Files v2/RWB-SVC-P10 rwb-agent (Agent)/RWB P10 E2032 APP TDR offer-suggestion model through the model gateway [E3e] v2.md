# RWB-P10-E2032-APP TDR offer-suggestion model through the model gateway [E3e]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E2032-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 2 |
| Size | Set by the squad at refinement |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-032 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Contract version | API Specification v5, rwb-agent.yaml, path /api/recovery/agent/v1 |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP19 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP |
| Depends on (build) | RWB-P10-E2032-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON, RWB-P10-E1058-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E2004-CON, RWB-P7-E1027-CON, P4 authorise call contract: Not specified in the source documents (GAP-2404) |
| Integration dependencies | None |
| External dependencies | RWB-P10-E2032-INF |
| Build dependencies not done | RWB-P10-E1058-APP and RWB-P10-E2032-INF are not done yet |
| Open decisions | DL33 is open; its assumptions are ASM-0135, ASM-0140 and ASM-0890 |
| Model existence (GAP-1463) | The TDR offer-suggestion model is conditional on its existence (priority Could). Restructure operations officer with the TDR team confirms it; the date the answer is needed is Not specified in the source documents (GAP-1463) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-032 for rwb-agent. The suggestion stays with the service that owns the agent rows and the model gateway: the in-process `ModelSuggestionClient.suggestOffer` becomes one published operation under `/api/recovery/agent/v1` (DP-11, DP-13), the run and the policy are rows of `rwb_agent` (DP-01), the decision log write becomes the local decision-record library plus the shared topic `rwb.decision-record.v1` (DP-03), the account, the arrears and the payments come through rwb-source-data's contract instead of the `recovery` tables (DP-05), the parameters and the lists come through the rwb-case contracts (DP-06, DP-07), the run completion is published as EV-28 through the outbox (DP-09), and the admin reads and SCR-14 are reached through the gateway-bff route (DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E2032-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 22 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **restructuring officer (RW-RESTRUCT)**, I want **the TDR team's offer-suggestion model called through the model gateway by the agent service so the treatment record carries its suggestion when the model exists**, so that **one gateway serves every model the Workbench uses, every suggestion is recorded with its model version, and the officer still decides the offer in every case**.

### 2. Business rationale

The legacy story RWB-E2-032 gave the restructuring officer one suggestion on the treatment record: the TDR team's offer-suggestion model is reached through the model gateway, its answer appears on SCR-14 with the model code and version, and one decision log entry and one agent run row hold what was suggested next to what was offered (FEAT-AGT-10; FSD P10 v3 A2.10; REQ-CHO-006, REQ-DRI-001). If the model is not in service the gateway returns no suggestion and the officer works as today, so the capability ships with the policy in mode OFF.

In the target the model, its policy and its run belong to rwb-agent. Arch v5 slide 41 gives the service the agent policies, the prompts, the runs, the guardrails and the evaluations in schema `rwb_agent`, and slide 16 gives it the Temporal workflow `AgentRunWorkflow` with a 60-second budget and then the rule result, the topic `rwb.agent.events.v1` with `AgentRunCompleted`, and the Enterprise AI private endpoint (INT-23) as its only outside call. That shape decides the story. The suggestion is no longer a Java interface inside the monolith: it is one REST operation of rwb-agent on the base `/api/recovery/agent/v1`, called by the treatment service with one hop and a client budget (DP-11, DP-13), so the treatment service can be built, released and tested without the agent service.

The facts the model reads are not this service's either. The account balance, the total balance, the days past due, the interest rate and the payments of the last 12 months are ACE data, read through rwb-source-data's contract and never from a `recovery` table or a `v_ace_*` view of this schema (DP-05; ADR-010). The treatment, its case and its type belong to rwb-treatment, and the case facts to rwb-case. The parameters and the list values — the reference data of LOV-AGENT, LOV-AUTONOMY and LOV-AGENT-RUN — are read through the rwb-case contracts (DP-06, DP-07). What stays inside the service is the whole of the run: the policy version in force, the mode, the timeout, the schema reference, the guardrail, the run row and the suggestion itself.

Two writes complete the target shape. The decision log entry becomes a local decision record written by the library of RWB-PLT-E1027-CON in the same transaction as the run row, relayed from the outbox as `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` to the central ledger of rwb-decision (DP-03; ADR-022). The run completion becomes EV-28 `AgentRunCompleted` on `rwb.agent.events.v1` as a CloudEvents 1.0 message with no account number or customer name (DP-09; Arch v5 slide 43). Both leave through the outbox, so a suggestion is never returned for a run that was not published and a record is never announced for a run that was not committed.

This story owns all eight legacy criteria of RWB-E2-032 — AC1 to AC8 — and copies them word for word in section 7, each with the origin tag of its legacy criterion. AC9 to AC15 are new and test only the microservice change of the title: the operation on the agent base, the run and the policy in `rwb_agent`, the record on the shared topic, EV-28 through the outbox, the facts through the owner contracts, the parameters and the lists, and the two waits of the call. The legacy story carries the requirement IDs REQ-CHO-006 and REQ-DRI-001, and section 18 traces both.

### 3. Preconditions

- RWB-P10-E1058-APP is done: the agent runtime exists in `rwb_agent` with `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_evaluation_run`, `agent_evaluation`, `agent_feedback` and `agent_alert`, and the two admin reads of TSD P10 v2 T-A answer (TSD P10 v2 T3.1; RWB-P10-E1058-APP owns the schema and the baseline migration).
- RWB-P10-E2032-CON is published: the shape of the suggestion operation, the decision-record mapping, the EV-28 payload and the fakes of section 12.8. This story builds against it and never restates it.
- RWB-PLT-E1027-CON is published: the local decision-record library, the record shape and the shared topic `rwb.decision-record.v1` with its CloudEvents 1.0 envelope (DP-03).
- RWB-PLT-TE006-CON is published: the outbox and retry library, the relay from the outbox to the topic and the inbox dedupe (DP-09).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published with their client libraries: the parameter contract and the reference-data contract of rwb-case (DP-06, DP-07), consumed against RWB-P3-E1042-CON and RWB-P3-E1043-CON.
- RWB-PLT-N001-CON is published: the gateway-bff composite route contract and its stub for the admin reads and SCR-14 (DP-19).
- The treatment read is available against its fake: RWB-P3-E2004-CON is the contract baseline for the treatment entity in the plan, and the runtime treatment and its type belong to rwb-treatment (S2) per Arch v5 slide 41. Which of the two answers the read at run time is Not specified in the source documents (GAP-0633; ASM-0979).
- A policy row exists for agent "TDR_OFFER". Until the TDR team deploys the model it has mode "OFF" and review date 2027-02-28 (assumed; DL33). When deployed, a new version with mode "L1", the model code and version, the output schema "tdr-offer-v1" and timeout 60 seconds is loaded by RW-COE and approved by RW-RISK.
- The lists of TSD P10 v2 T3.2 are in force as reference data of rwb-case: LOV-AGENT (INTAKE, SCREENING, LEGAL_DOC, EXTRACT, TDR_OFFER), LOV-AUTONOMY (OFF, SHADOW, L1) and LOV-AGENT-RUN (ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR, DISABLED). The service holds no copy of a list in code (DP-07).
- The account, the arrears and the payments are reachable through rwb-source-data's contract: `principal_outstanding`, `total_balance`, `days_past_due`, `interest_rate`, `payment_date` and `payment_amount` (DF-ACC-009, DF-ACE-020, DF-ACE-018, DF-ACE-025, DF-ACE-045, DF-ACE-046). The operation and the product path are Not specified in the source documents (GAP-0633; ASM-0980).
- The private endpoint of Enterprise AI (INT-23) is reachable from the pods over HTTPS: host, port and certificate are Not specified in the source documents (GAP-0633; ASM-0988) and are provisioned by RWB-P10-E2032-INF.
- The login is the rwb-agent login (DP-02) on schema `rwb_agent`; its name is Not specified in the source documents (GAP-0633; ASM-0976).
- This story is in lane L-P10-A and starts after RWB-P10-E1058-APP, the in-lane story it waits for (§R5.7).

### 4. Flow

1. The treatment service asks rwb-agent for a suggestion for a treatment. The request is one hop on the base `/api/recovery/agent/v1`, with the case ID and the treatment ID in the body and the idempotency key `TDR_OFFER:<treatmentId>` (DP-11, DP-13; legacy section 12).
2. SuggestionController validates the request and reads the treatment through the rwb-treatment contract: its type, its case and its state. A treatment whose type is not "RESTRUCTURE" ends here with no call and no suggestion (BR6; AC8).
3. TdrSuggestionService reads the policy version of agent "TDR_OFFER" in force for the business date from `agent_policy` in `rwb_agent`: `policy_version`, `model_code`, `model_version`, `output_schema_ref`, `autonomy_mode`, `timeout_seconds`, `confidence_floor` and `review_date`. A version whose `autonomy_mode` is "OFF" returns no suggestion and makes no call, and no run row and no record are written (AC2).
4. The step looks up the idempotency key on `agent_run`. A run already exists for the key: its stored suggestion and its `decision_log_id` are returned and no second model call is made (R-UNI-40; AC7).
5. TdrInputAssembler builds the masked inputs. The account facts and the 12 months of payments come through the rwb-source-data contract with one hop and a 2 s client budget; the case facts come through rwb-case; the customer name, the account number and every personal field are masked before the model call, and the masked snapshot is kept as the inputs reference (DP-05; AC12).
6. ModelGatewayClient calls the Enterprise AI private endpoint (INT-23) with the model code, the masked inputs and the output schema "tdr-offer-v1", bounded by `timeout_seconds` of the policy version in force — 60 seconds for the versions of this story (NFR-010; BR1).
7. GuardrailChecker tests the answer against "tdr-offer-v1": installments 1 to 360, monthly amount above 0, interest rate 0 to 30, confidence. An answer outside the schema ends the run in status "GUARDRAIL_FAILED" with check "SCHEMA" and no suggestion (AC5).
8. RecordAndApply runs in one `rwb_agent` transaction: it writes the `agent_run` row with the agent code, the policy and model versions, the autonomy mode, the case and subject, the idempotency key, the status, the fallback flag, the guardrail result, the output, the confidence, the latency, the cost and `run_at`; it writes the local decision record with decision "D5" and final call "SUGGESTION_RECORDED" and stores its reference in `agent_run.decision_log_id`; and it inserts the outbox rows of the two events. A failed record write rolls the whole transaction back (DP-03; R-UNI-39; AC6).
9. The outbox relay publishes `rwb.decision.DecisionRecorded.v1` on `rwb.decision-record.v1` and `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1`, both as CloudEvents 1.0 messages keyed by the case ID, with no account number or customer name (DP-09; AC11). rwb-decision seals the record into the central ledger; the run completion is read by rwb-decision, rwb-document and rwb-deviation (Arch v5 slide 43).
10. The operation answers with the eight members of the legacy `OfferSuggestion` record: `agentRunId`, `decisionLogEntryId`, `modelCode`, `modelVersion`, `installments`, `monthlyAmountThb`, `interestRate` and `confidence` (legacy section 12; AC9).
11. The restructuring officer sees the suggestion on SCR-14 with the model code and the model version, or MSG-P10-007 when there is none. The panel is served by the gateway-bff composite route, which calls the agent read and merges the answer, and the browser calls no service directly (DP-19; AC14).
12. A rerun for the same treatment hits the idempotency key, returns the stored answer and writes nothing: no second run row, no second record, no second event, and the hit is counted once (R-UNI-40).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The model is not in service (mode OFF) | No call, no run row and no decision record; the treatment shows the message | MSG-P10-007 | AC2 |
| X2 | The model does not answer within 60 seconds | The call is ended at the policy timeout; the run holds status "TIMED_OUT" with fallback true; no suggestion and no record; the treatment continues (R-UNI-32) | MSG-P10-007 | AC4, AC15 |
| X3 | The answer fails the output schema "tdr-offer-v1" | The run holds status "GUARDRAIL_FAILED" with check "SCHEMA"; no suggestion and no record | MSG-P10-007 | AC5 |
| X4 | The decision record cannot be written | The transaction rolls back; no suggestion is returned and the caller receives the refusal; the run row is not kept with a decision link (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same treatment asks again | The first suggestion and its decision record reference return from the run row; no second model call, no second record and no second event | None to a user | AC7, AC12 |
| X6 | The treatment type is not "RESTRUCTURE" | No call and no suggestion; nothing is written | None to a user | AC8 |
| X7 | A role without the right reads the agent runs | Refused; nothing is returned and nothing is written | MSG-P4-002 | AC14 |
| X8 | The rwb-source-data contract answers an error or facts older than the business date | No suggestion and no record; the run is kept with the reason of the read and the freshness of the facts; no value is defaulted | MSG-P10-007 | AC12 |
| X9 | The model gateway answers a 4xx or a 5xx | The run holds status "MODEL_ERROR" with fallback true; no suggestion and no record; the caller receives MSG-P10-007 | MSG-P10-007 | AC15 |
| X10 | The outbox relay is down after a committed transaction | The run row and the record stay committed and the outbox rows are relayed when the sender succeeds; no event is lost and no event is published twice (R-UNI-33, R-UNI-35) | None to a user | AC11 |
| X11 | The reference value of the mode or of a run status is outside its list | The value is refused as a configuration error, the run is not written with an invented value and the version is named | None to a user | AC13 |

X1 to X6 are the legacy exception paths of RWB-E2-032 carried onto the service; X7 is the legacy access path of TC-E2-032-09; X8 to X11 are the failures that appear when the call, the facts and the record cross a boundary. X4 keeps the legacy wording: the caller receives `DecisionNotRecordedException` and MSG-P7-003, so the treatment service needs no change.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds after RWB-P10-E1058-APP in lane L-P10-A against the published contracts RWB-P10-E2032-CON, RWB-PLT-E1027-CON, RWB-PLT-TE006-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON and RWB-PLT-N001-CON and the fakes of section 12.8; the four C dependencies are built against their fakes and block nothing (§R5.4) |
| Negotiable | The request and answer field names, the record mapping, the event payload and the route are agreed in RWB-P10-E2032-CON; the policy values, the schema limits and the review date are data |
| Valuable | Puts a recorded, versioned suggestion on the treatment record through one gateway and one service, with no second integration path and no AI outside rwb-agent |
| Estimable | One operation, one service, one input assembler, one gateway client, one guardrail, one run writer, one record writer and one publisher |
| Small | Under two weeks with one developer and its tests; the legacy estimate was under one week for the in-process interface |
| Testable | Each of the fifteen criteria of section 7 is one automated test on an observable: a REST answer, a stored row, a record field, an outbox row, a topic message, a masked input or a gate |

### 7. Acceptance criteria

```gherkin
Feature: TDR offer-suggestion model through the model gateway [E3e]

  Background:
    Given restructure treatment "T-1001" is open on case "RW-2026-001001"
    Given the account has principal outstanding 1,250,000.00 baht and 120 days past due

  Scenario: AC1 Exposed (legacy RWB-E2-032 AC1)
    Given the rwb-source-data contract mock returns the masked account facts and the last 12 months of payments of case "RW-2026-001001"
    Given the model deployed by the TDR team with policy "TDR_OFFER" version "P2", mode "L1" and model version "TDR-OFFER-1.0"
    When the gateway calls it
    Then the suggestion returns with 84 installments of 18,900.00 baht and model version "TDR-OFFER-1.0"
    Then one agent run row and one decision record with decision "D5", model version "TDR-OFFER-1.0" and final call "SUGGESTION_RECORDED" are written

  Scenario: AC2 Not available (legacy RWB-E2-032 AC2)
    Given the model not yet built and policy "TDR_OFFER" version "P1" with mode "OFF" and review date 2027-02-28
    When the treatment service asks for a suggestion
    Then the gateway stub returns no suggestion and makes no model call
    Then SCR-14 shows MSG-P10-007 and no decision record is written
    Then GET /admin/agent-configs shows version "P1" with review date 2027-02-28

  Scenario: AC3 Logged (legacy RWB-E2-032 AC3)
    Given the rwb-decision contract mock serves the sealed decision record of the suggestion on treatment "T-1001"
    Given a suggestion on treatment "T-1001"
    When the record is read
    Then the decision record linked to the suggestion holds model version "TDR-OFFER-1.0", the inputs reference and the suggested terms
    Then SCR-14 shows "Suggested by TDR_OFFER, version TDR-OFFER-1.0"

  Scenario: AC4 The model does not answer (legacy RWB-E2-032 AC4)
    Given the TDR model stub does not answer for 61 seconds
    When the treatment service asks for a suggestion
    Then the agent run holds status "TIMED_OUT" and fallback true
    Then no suggestion and no decision record exist and SCR-14 shows MSG-P10-007

  Scenario: AC5 An answer that fails the schema (legacy RWB-E2-032 AC5)
    Given the model returns installments -12
    When the guardrail runs
    Then the agent run holds status "GUARDRAIL_FAILED" with check "SCHEMA" and no suggestion is returned

  Scenario: AC6 The decision cannot be recorded (legacy RWB-E2-032 AC6)
    Given the decision log writer fails
    When the model answers
    Then the system returns no suggestion and the treatment service receives DecisionNotRecordedException with MSG-P7-003
    Then the agent run has no decision record ID

  Scenario: AC7 The same treatment asks twice (legacy RWB-E2-032 AC7)
    Given the rwb-treatment contract mock returns treatment "T-1001" of type "RESTRUCTURE" on case "RW-2026-001001"
    Given a suggestion was recorded for treatment "T-1001"
    When the treatment service asks again for "T-1001"
    Then the first suggestion and its decision record ID return and no second model call is made

  Scenario: AC8 Not a restructure (legacy RWB-E2-032 AC8)
    Given the rwb-treatment contract mock returns treatment "T-1002" of type "SETTLEMENT"
    Given treatment "T-1002" has type "SETTLEMENT"
    When the treatment service asks for a suggestion
    Then the system makes no model call and no suggestion returns

  Scenario: AC9 The suggestion is one operation on the agent base (new, D-RCV-60)
    Given rwb-agent is deployed on schema "rwb_agent" with the rwb-treatment, rwb-source-data and rwb-case fakes
    When the treatment service asks for a suggestion for treatment "T-1001"
    Then one operation of rwb-agent under the base /api/recovery/agent/v1 answers with agentRunId, decisionLogEntryId, modelCode, modelVersion, installments, monthlyAmountThb, interestRate and confidence
    Then the model call of up to 60 seconds runs inside rwb-agent and the caller's own budget is the 2 s client budget of DP-11, except the suggestion call itself (ASM-0978)
    Then no in-process ModelSuggestionClient exists and no caller embeds the agent runtime
    Then the treatment is read through the rwb-treatment contract and its type is read once per request

  Scenario: AC10 The run and the policy are rows of rwb_agent (new, D-RCV-60)
    Given policy "TDR_OFFER" version "P2" with mode "L1", model version "TDR-OFFER-1.0", output schema "tdr-offer-v1" and timeout 60 seconds
    When the suggestion is built for treatment "T-1001"
    Then one agent_run row holds agent_code "TDR_OFFER", agent_version, model_version "TDR-OFFER-1.0", case_id, subject_id, autonomy_mode "L1", trigger_event, idempotency_key "TDR_OFFER:<treatmentId>", status "ANSWERED", fallback false, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at and decision_log_id
    Then the policy version, the mode, the model code and version, the schema reference, the timeout, the confidence floor and the review date are read from agent_policy and never from a properties file or a constant
    Then the service writes no table and reads no table outside schema "rwb_agent", and holds no foreign key into another schema
    Then a pipeline scan finds no table name of another service in the rwb-agent sources

  Scenario: AC11 The record and EV-28 leave through the outbox (new, D-RCV-60)
    Given the run of AC10 has ended in status "ANSWERED"
    When the transaction commits and the outbox relay runs
    Then one rwb.decision.DecisionRecorded.v1 message is on rwb.decision-record.v1 and one rwb.agent.AgentRunCompleted.v1 message is on rwb.agent.events.v1
    Then both carry the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, and both are keyed by the case ID
    Then the EV-28 payload carries the run ID, agent_code, the policy version, the model version, the case ID, the outcome "ANSWERED", fallback false and run_at, and no account number, no customer name and no other personal field
    Then no message is published for a transaction that rolled back, and a repeat of the relay publishes no second message
    Then a payload that fails its registry subject is refused before the relay and routed to the .dlt topic of the agent topic

  Scenario: AC12 The facts come through the owner contracts (new, D-RCV-60)
    Given the rwb-source-data contract mock returns principal_outstanding 1,250,000.00 baht, the total balance, 120 days past due, the interest rate and the payments of the last 12 months of case "RW-2026-001001"
    When the inputs are assembled for treatment "T-1001"
    Then every account and payment field is read through the rwb-source-data contract with one hop and a 2 s client budget, and no v_ace_* view and no recovery table is read by rwb-agent
    Then the customer name, the account number and every personal field are masked before the model call, and the masked snapshot is stored as the inputs reference of the record
    Then a contract error, or facts older than the business date, give no suggestion and no record, and the run is kept with the reason and the data_as_of of the read
    Then no value is defaulted for a fact that the contract did not return

  Scenario: AC13 The parameters and the lists are read, not coded (new, D-RCV-60)
    Given the rwb-case parameter contract mock and the reference-data contract mock serve the values in force
    When the suggestion is asked for treatment "T-1001"
    Then every reference value is read through the rwb-case contracts and the service holds no copy of LOV-AGENT, LOV-AUTONOMY or LOV-AGENT-RUN in code
    Then an autonomy mode outside LOV-AUTONOMY, or a run status outside LOV-AGENT-RUN, is refused as a configuration error and no run row is written with it
    Then no threshold, schema limit or review date is written in code; all of them are rows of the policy version in force

  Scenario: AC14 The admin reads and SCR-14 are reached through the gateway-bff route (new, D-RCV-60)
    Given the gateway-bff route stub serves the two admin reads and the SCR-14 panel
    When RW-COE reads the TDR_OFFER config version and the platform administrator reads the agent runs
    Then GET /api/recovery/agent/v1/admin/agent-runs and GET /api/recovery/agent/v1/admin/agent-configs are reached through one gateway-bff hop and the answer is returned unchanged
    Then SCR-14 shows "Suggested by TDR_OFFER, version TDR-OFFER-1.0" or MSG-P10-007 as the route returns it, and no screen calls rwb-agent directly
    Given the user "U-5001" holds RW-RESTRUCT, which carries no Platform administration right
    When "U-5001" reads the agent runs through the route
    Then the call is refused with 403 and MSG-P4-002 and nothing is written

  Scenario: AC15 The two waits of the call are the policy timeout and the client budget (new, D-RCV-60)
    Given policy "TDR_OFFER" version "P2" with timeout 60 seconds and mode "L1"
    When the TDR model does not answer and the run is recorded
    Then the model call is ended at 60 seconds and the run holds status "TIMED_OUT", fallback true and the measured latency
    Then a 4xx or a 5xx answer gives status "MODEL_ERROR" with fallback true, and neither case returns a suggestion or writes a record
    Then the caller receives MSG-P10-007 and the treatment continues as R-UNI-32 requires
    Then every other REST hop of this service keeps the 2 s client budget of DP-11, and the value 60 is read from the policy row and not written in code

  Scenario: AC16 A suggestion is advice and no list is coded (new, D-RCV-60)
    Given the rwb-treatment contract mock returns treatment "T-1001" of type "RESTRUCTURE" on case "RW-2026-001001"
    When the suggestion is recorded for treatment "T-1001"
    Then no suggestion is written into an offer field or a treatment status
    Then no copy of a list of TSD P10 v2 T3.2 is held in code and every list value is read from rwb-case reference data

  Scenario: AC17 An unauthorised call and an unknown treatment are refused with 401 and 404 (new, D-RCV-60)
    Given a caller without a valid credential asks for a suggestion for treatment "T-1001"
    When the operation on /api/recovery/agent/v1 is called
    Then it answers 401 and no suggestion, agent run row or decision record is written
    When the treatment service asks for a suggestion for a treatment ID that rwb-treatment does not hold
    Then the operation answers 404 and no agent run row is written
```

**Target reading.** The policy "TDR_OFFER", its versions "P1" and "P2", the modes "OFF" and "L1", the model version "TDR-OFFER-1.0", the output schema "tdr-offer-v1", the 84 installments of 18,900.00 baht, the review date 2027-02-28, the 60 seconds, the 61 seconds of silence, installments -12, treatment "T-1001" on case "RW-2026-001001", treatment "T-1002" of type "SETTLEMENT", decision "D5", final call "SUGGESTION_RECORDED", check "SCHEMA", and the messages MSG-P10-007, MSG-P7-003 and MSG-P4-002 are the legacy values of RWB-E2-032, copied character for character, and so are the two Background lines. The scenario lines of AC1 to AC8 keep their legacy titles and every legacy Given, When and Then, and each carries the origin tag of its legacy criterion. Four of the eight carry one inserted line as their first Given, because the legacy criterion asserts a cross-service read or write that can be mocked. AC1 and AC7 insert `Given the rwb-source-data contract mock ...` and `Given the rwb-treatment contract mock ...`: the model call reads the account facts and the payments through rwb-source-data (DP-05) and the type gate reads the treatment through rwb-treatment. AC3 inserts `Given the rwb-decision contract mock ...` because the entry it reads is the record sealed by rwb-decision from the shared topic (DP-03). AC8 inserts `Given the rwb-treatment contract mock ...` because `treatment.treatment_type` is a rwb-treatment field in the target, and the legacy read of the treatment row is a call to its owner. AC2, AC4, AC5 and AC6 need none: AC2 and AC6 assert that no call and no record exist, AC4 asserts a run status after a silent stub, and AC5 asserts a schema refusal on an answer the stub already returned, so none of the four reads or writes another service. The in-process `ModelSuggestionClient.suggestOffer` and its `OfferSuggestion` record become one operation under `/api/recovery/agent/v1` (DP-11, DP-13) whose path below the base is fixed in RWB-P10-E2032-CON and is Not specified in the source documents (GAP-0633; ASM-0977). The run, the policy and the guardrail are rows and code of `rwb_agent` (DP-01). The decision log write becomes the local decision-record library plus `rwb.decision-record.v1` (DP-03) and the run completion becomes EV-28 through the outbox (DP-09). The account, the arrears and the payments come through rwb-source-data's contract and no `v_ace_*` view is granted to this login (DP-05; ADR-010; ASM-0980). The parameters and the lists come through the rwb-case contracts (DP-06, DP-07; ASM-0981). The admin reads and SCR-14 come through the gateway-bff route (DP-19; ASM-0982). The suggestion call keeps the legacy synchronous answer and therefore carries the policy timeout of 60 seconds, while DP-11's 2 s client budget applies to every other hop; the exception is recorded as ASM-0978 because no source reconciles the two waits.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The TDR model is reached only through the model gateway on the Enterprise AI private endpoint (INT-23), with the model code, the masked inputs and the output schema "tdr-offer-v1", and never by code inside the service | Legacy BR1; DL33; TSD P10 v2 T5.1; Arch v5 slide 16 |
| BR2 | Mode "OFF" returns no suggestion, makes no call and writes no run row and no record; the review date is held on the policy row | Legacy BR2; `agent_policy.autonomy_mode`, `review_date` (DF-AGT-008, DF-AGT-016) |
| BR3 | A suggestion is returned only after its decision record is written, in the same transaction as the run row | Legacy BR3; Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR4 | A timeout, a model error or a failed schema check gives no suggestion, records the fallback and lets the treatment continue | Legacy BR4; R-UNI-32; TSD P10 v2 NFR-010 |
| BR5 | One suggestion per treatment; the key is "TDR_OFFER:<treatmentId>" and a repeat returns the stored answer with no second call | Legacy BR5; R-UNI-40; DF-AGT-045 |
| BR6 | The model is called only for treatment type "RESTRUCTURE", read from the treatment's owner | Legacy BR6; `treatment.treatment_type` (DF-TRT-004) |
| BR7 | The suggestion is advice: the officer builds and submits the offer and no suggestion is written into an offer field or a treatment status | Legacy BR7; Agent catalog; R-RES-09, R-RES-10 |
| BR8 | No value a business person may change is written in code: the model code and version, the output schema, the timeout, the confidence floor, the mode and the review date are rows of the `agent_policy` version in force | BR-P10-010; FSD P10 v3 A2.10.3.1 |
| BR9 | The run writes only `rwb_agent` tables and the shared outbox; the account, the payments, the treatment and the case are read through their owners' contracts | DP-01; DP-05; ADR-010 |
| BR10 | Every event carries IDs and facts only; the masked inputs snapshot is stored as the record's inputs reference and no account number, customer name or personal field reaches a topic, a log or a workflow payload | Template and Rules §R7.2 s17; Arch v5 slides 42 and 43 |
| BR11 | The lists of TSD P10 v2 T3.2 are reference data of rwb-case and no copy of a list sits in code | DP-07; TSD P10 v2 T3.2 |
| BR12 | An operation of this service answers on the base `/api/recovery/agent/v1`, and no path of another service is declared as its own | DP-13; Arch v5 slide 41 |
| BR13 | A run completion is published once, from the outbox, after the transaction commits, and a repeat of the relay publishes nothing | DP-09; R-UNI-33; R-UNI-40 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| REQUESTED | MODE_OFF | the policy version in force has `autonomy_mode` "OFF" | NO_SUGGESTION, with no run row |
| REQUESTED | KEY_FOUND | a run exists for "TDR_OFFER:<treatmentId>" | ANSWERED, with the stored answer returned and no second call |
| REQUESTED | CALL_ANSWERED | the model answered inside the policy timeout and the answer meets "tdr-offer-v1" | ANSWERED |
| REQUESTED | CALL_SILENT | the call reached the policy timeout | TIMED_OUT, with fallback true |
| REQUESTED | MODEL_REFUSED | the gateway answered a 4xx or a 5xx | MODEL_ERROR, with fallback true |
| CALL_ANSWERED | SCHEMA_REFUSED | the answer fails the output schema | GUARDRAIL_FAILED, with check "SCHEMA" |
| ANSWERED | RECORD_COMMITTED | the run row, the record and the outbox rows commit in one transaction | ANSWERED, with `decision_log_id` set |
| ANSWERED | RECORD_FAILED | the decision record cannot be written | ROLLED_BACK, with no run row and no record |
| ANSWERED | RELAYED | the outbox relay publishes EV-28 and the record | ANSWERED, with the two events published once |

These are the states of one attempt of the suggestion and of its run row, not a case state machine. The statuses ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, TOOL_UNAVAILABLE, MODEL_ERROR and DISABLED are the values of LOV-AGENT-RUN (TSD P10 v2 T3.2), and REQUESTED, NO_SUGGESTION, ROLLED_BACK and RELAYED are steps of the operation and are not written into `agent_run.status`. **This story moves no case status and no treatment status**: `recovery_case` belongs to rwb-case, the treatment belongs to rwb-treatment, and the suggestion area of SCR-14 is read-only (BR7).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RESTRUCT | Reads the suggestion on SCR-14 (Treatment and offer R) |
| RW-CASEOWN | Reads the suggestion on SCR-14 (Treatment and offer R) |
| SY-CASEWF | Calls the suggestion operation from the treatment service over one hop |
| SY-AGENT | Reads the account, the payments and the case facts through their owners' contracts (Case record R, Treatment and offer R) |
| SY-DECLOG | Writes the local decision record and its outbox row (Decision log C) |
| RW-COE, RW-RISK | Load and approve the "TDR_OFFER" policy version (Rules and parameters C and A) |
| RW-PLATADM | Reads the agent runs of "TDR_OFFER" through the admin read (Platform administration R) |
| rwb-agent service identity | Runs the operation, writes `agent_run` and the outbox in `rwb_agent`, and calls the model gateway |

The legacy authority table is copied with its role codes. The per-service login of the service identity is the rwb-agent login (DP-02) and its name is Not specified in the source documents (GAP-0633; ASM-0976). The migration of `SY-CASEWF` from an in-process interface to a REST caller changes no right in the matrix; the right under which the treatment service calls the operation is the service identity's right on the agent contract and is agreed with rwb-access. Each call to the operation and each admin read first passes the rwb-access authorise check (DP-08).

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-TRT-001, DF-TRT-002, DF-TRT-004 | treatment (rwb-treatment, owner S2) | id, case_id, treatment_type | Read, through the rwb-treatment contract |
| DF-ACC-009, DF-ACE-018, DF-ACE-020, DF-ACE-025 | v_ace_account (owner P1) | principal_outstanding, days_past_due, total_balance, interest_rate | Read, through rwb-source-data's contract (DP-05) |
| DF-ACE-045, DF-ACE-046 | v_ace_payment (owner P1) | payment_date, payment_amount | Read, through rwb-source-data's contract (DP-05) |
| DF-AGT-001 to DF-AGT-025 | agent_policy | policy_version, model_code, model_version, output_schema_ref, autonomy_mode, confidence_floor, timeout_seconds, review_date, valid_from, valid_to, status | Read |
| DF-AGT-026 to DF-AGT-035 | agent_prompt | prompt_version, body_hash | Read, where a prompt version is named on the run |
| DF-AGT-036 to DF-AGT-060 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, decision_log_id | Write |
| DF-DEC-001 to DF-DEC-018 | decision record (local library) and decision_log_entry (rwb_decision, owner P7) | all fields, written through the decision-record library and sealed by rwb-decision | Write locally |
| DF-AGT-061 to DF-AGT-111 | agent_sample, agent_evaluation_run, agent_evaluation, agent_feedback, agent_alert | No row is written or read by this story | Not used |

Field IDs are those of the Logical Data Model and Data Dictionary v9, except DF-ACC-009, the field `principal_outstanding`, which is not in LDM v9 or Data Classification v5 (CG-ALL-2817). The run is the only row this story writes, and it is in `rwb_agent` (DP-01). The record is written by the library of RWB-PLT-E1027-CON and never into `rwb_decision` directly (DP-03). The account, the payment and the treatment facts are read through their owners' contracts and no copy is kept: the masked inputs snapshot travels inside the record as its inputs reference and holds no account number and no customer name (ASM-0983). The values of `agent_version` and `prompt_version` for agent "TDR_OFFER" are Not specified in the source documents (GAP-0633; ASM-0983); the legacy decision-log mapping fixes `agent_version` null and no prompt version applies to a model called directly through the gateway.

### 12. Contract

#### 12.1 REST operations provided

| Method | Path | Purpose | Rights |
|---|---|---|---|
| POST | `/api/recovery/agent/v1/<suggestion path>` — Not specified in the source documents (GAP-0633; ASM-0977) | Replaces `ModelSuggestionClient.suggestOffer`: one suggestion for one treatment, answered with the eight legacy `OfferSuggestion` members. The request carries the case ID, the treatment ID and the idempotency key `TDR_OFFER:<treatmentId>`; a repeat returns the stored answer (DP-11; DP-13; BR5) | Service identity of the caller (Treatment and offer R) |

The two admin reads this story uses — `GET /api/recovery/agent/v1/admin/agent-runs` and `GET /api/recovery/agent/v1/admin/agent-configs` — are provided by rwb-agent and baselined in RWB-P10-E1058-CON; this story reads them and declares no shape of its own (DP-13). Every path is on the base `/api/recovery/agent/v1` and none is served on the legacy monolith base.

#### 12.2 REST operations consumed

| Method | Path | Service | Used for | Timeout |
|---|---|---|---|---|
| GET | Not specified in the source documents (GAP-0633; ASM-0980) | rwb-source-data (P1) | The account facts and the 12 months of payments, masked before the model call (DP-05) | One hop, 2 s |
| GET | Not specified in the source documents (GAP-0633; ASM-0979) | rwb-treatment (S2) | The treatment, its case and its type (DF-TRT-001, DF-TRT-002, DF-TRT-004) | One hop, 2 s |
| GET | Not specified in the source documents (GAP-0633; ASM-0979) | rwb-case (P3) | The case facts the run names, and the parameter and reference-data values in force (DP-06, DP-07) | One hop, 2 s |
| GET | Not specified in the source documents (GAP-0633; ASM-0981) | rwb-decision (P7) | The sealed decision record of a suggestion, read back for AC3 (DP-03) | One hop, 2 s |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020). The call to the Enterprise AI private endpoint is not a REST operation between services: it is the external call of 12.9.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | agent, caseid, fallback, outcome, runid |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 owns the type and the central ledger; every service writes its own record | the record reference | record reference, decision "D5", model version, agent version null, final call "SUGGESTION_RECORDED", the suggested terms, the actions `{treatmentId, agentRunId}` |

Both rows are inserted in the outbox in the same transaction as the run row and relayed with the CloudEvents 1.0 envelope (DP-09; DP-03). The account number and the customer name are never carried (BR10). Data Classification classes `agent_version` and `model_version` (decision_log_entry), `outcome` (decision_log_entry, deviation, hearing, treatment), `installments` (treatment) and `confidence` (document_field) as Customer data, Confidential, personal data, shown within the role's scope. Where one of these fields is carried or shown it is handled under that class; any further handling rule for it is Not specified in the source documents (DOR-RWB-P10-E2032-APP-11).

#### 12.4 Events consumed

None. The suggestion is asked over REST and the story reads no topic; the inbox of the outbox library is used only for the relay's own dedupe.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Purpose |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | One run of an agent or model with its 60-second budget and then the rule result; this story starts it for the suggestion |
| BuildTdrInputs | Activity | `rwb-agent` | Reads the account, the payment, the treatment and the case facts through their contracts and returns the masked inputs |
| CallModelGateway | Activity | `rwb-agent` | Calls INT-23 with the model code, the masked inputs and "tdr-offer-v1", and maps the answer, the timeout and the gateway errors |
| CheckGuardrail | Activity | `rwb-agent` | Tests the answer against the output schema and returns the check code and the outcome |
| RecordAndApply | Activity (workflow kit) | `rwb-agent` | Writes the run row, the decision record and the outbox rows in one transaction |

The workflow name, the queue and the 60-second budget are those of Arch v5 slide 16; the activity names are this story's and are agreed in RWB-P10-E2032-CON.

The catalogue row starts AgentRunWorkflow as a child of a stage workflow for the route agent or the pricing agent, on DocumentStored (classification) or CaseCreated (screening). Neither trigger is the TDR offer-suggestion call of this story. The workflow ID form is Not specified in the source documents (CG-ALL-2821). The start rule (start or signalWithStart, and the duplicate-start policy) is Not specified in the source documents (CG-ALL-2821).

#### 12.6 Schedules

None. The suggestion is request-driven and no Temporal Schedule is created, changed or owned by this story; the Arch v5 job map names no job for an agent suggestion (slide 44).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_run | P10 (rwb_agent) | The run row of a suggestion: DF-AGT-036 to DF-AGT-060; created by the agent runtime baseline migration, not by this story |
| agent_policy | P10 (rwb_agent) | Read only here: the policy version in force and its values |
| agent_prompt | P10 (rwb_agent) | Read only here: the prompt version where the run names one |
| outbox_event, processed_event, idempotency_key | PLT library, created in rwb_agent | The outbox, inbox and idempotency envelope of DP-09 |

`decision_log_entry` is a rwb-decision table and is written only through the decision-record library (DP-01, DP-03). No table of another schema is read or written, and no foreign key crosses a schema.

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-source-data WireMock | The account and payment facts (DP-05) | The masked facts of case "RW-2026-001001" with principal outstanding 1,250,000.00 baht and 120 days past due; an error answer; facts older than the business date; an empty `interest_rate` |
| rwb-treatment WireMock | The treatment read | Treatment "T-1001" of type "RESTRUCTURE"; treatment "T-1002" of type "SETTLEMENT"; a treatment that does not exist |
| rwb-case WireMock | The case facts, the parameter contract and the reference-data contract (DP-06, DP-07) | The lists LOV-AGENT, LOV-AUTONOMY and LOV-AGENT-RUN; the parameter values in force; an answer with a mode outside LOV-AUTONOMY |
| rwb-decision WireMock | The sealed decision record read and the central ledger side (DP-03) | The sealed record of the suggestion; a record that is not found |
| Decision-record library stub | The local record and `rwb.decision-record.v1` | A committed record with its reference; a forced write failure; the outbox row and its relay |
| Model gateway stub (INT-23) | The Enterprise AI private endpoint | An answer of 84 installments of 18,900.00 baht; an answer with installments -12; silence for 61 seconds; a 4xx and a 5xx |
| gateway-bff route stub | The DP-19 route of the admin reads and SCR-14 | The merged screen answer with the suggestion or MSG-P10-007; the refusal of RW-RESTRUCT with MSG-P4-002 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | The suggestion operation on `/api/recovery/agent/v1`, and the reads of rwb-source-data, rwb-treatment, rwb-case and rwb-decision; one hop, 2 s each |
| Kafka | 2 published, 0 consumed | EV-28 on `rwb.agent.events.v1` and the record on `rwb.decision-record.v1`, both through the outbox |
| Temporal | 1 workflow, 4 activities | AgentRunWorkflow and BuildTdrInputs, CallModelGateway, CheckGuardrail and RecordAndApply on the queue `rwb-agent` |
| File | None | This story reads and writes no file; the external call is HTTPS to INT-23 and is counted under REST |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent`, module `tdr`, Java package `th.co.scb.ace.workbench.recovery.agent.tdr`; the operation, its request and answer records in `th.co.scb.ace.workbench.recovery.agent.tdr.api`. Front end: the suggestion area of SCR-14, read through the gateway-bff route.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none; C from the legacy dependency |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-11 resolves to the operation of 12.1 and to the four consumed reads, each one hop with a 2 s client budget; the suggestion call itself carries the policy timeout of 60 seconds, which is the recorded exception of ASM-0978. DP-05 resolves to the rwb-source-data contract and to no view of this service: no `v_ace_*` view is granted to the rwb-agent login (ADR-010). The treatment read is the C dependency RWB-P3-E2004-CON (the treatment entity contract baseline) against the runtime owner rwb-treatment (ASM-0979).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuggestionController | REST controller | Validates the request, declares the operation, maps errors to the problem response and answers with the eight members |
| TdrSuggestionService | Service | Mode check, idempotency, the gateway call, the guardrail, the record and the run |
| TdrInputAssembler | Service | Reads the account, the payment, the treatment and the case facts through their contracts and masks the personal fields |
| ModelGatewayClient | Client | Calls INT-23 with the model code, the masked inputs and "tdr-offer-v1", with the policy timeout and a breaker |
| GuardrailChecker | Service | Tests the answer against the output schema: installments 1 to 360, monthly amount above 0, interest rate 0 to 30, confidence |
| RunWriter | Repository | Reads `agent_policy` and `agent_prompt`, and writes and looks up `agent_run` in `rwb_agent` |
| DecisionRecordWriter | Library adapter | Writes the local decision record with decision "D5" in the same transaction (DP-03) |
| RunCompletedPublisher | Outbox adapter | Inserts the EV-28 row and the record row, and reads the relay result (DP-09) |
| TreatmentSuggestionPanel | React component | The suggestion area of SCR-14, fed by the gateway-bff route, with the suggestion or MSG-P10-007 |

**Database and migrations.** No new table and no new column in this story: `agent_run`, `agent_policy` and `agent_prompt` come from the agent runtime baseline migration of `rwb_agent` that RWB-P10-E1058-APP owns (TSD P10 v2 T3.1; ASM-0984). If the baseline does not carry a column this story needs, the script that adds it takes its number from the rwb-agent Flyway sequence; that number is Not specified in the source documents (GAP-0633; ASM-0984). One index serves the idempotency lookup and the admin read: `agent_run (idempotency_key)` and `agent_run (agent_code, run_at)`. Index names are naming-library values and not business values.

**Configuration and reference data**

- Policy versions (RW-COE): `agent_code` "TDR_OFFER", `policy_version`, `model_code`, `model_version`, `output_schema_ref` "tdr-offer-v1", `autonomy_mode`, `timeout_seconds` 60, `confidence_floor`, `review_date` and the segment fields. The P1 version has mode "OFF" and review date 2027-02-28; the P2 version is loaded when the TDR team deploys the model.
- The lists LOV-AGENT, LOV-AUTONOMY and LOV-AGENT-RUN are reference data of rwb-case, read through the reference-data contract; the service holds no copy (DP-07; ASM-0981).
- The parameter values this story reads — the feature value that switches the suggestion and the read preferences of the clients — are rows of the rwb-case parameter contract (DP-06). Which keys the service reads is Not specified in the source documents (GAP-0633; ASM-0981).
- The feature flag `rwb.agent.tdr-suggestion` is a data row of the platform feature-flag library (§R3 default ruling); off, the operation answers no suggestion with no call, as the legacy section 13 requires.

**Build steps**

1. Write the operation and its request and answer records from RWB-P10-E2032-CON, with the 2 s budget, the problem response and the idempotency key; tests for AC9.
2. Build the mode-off and the type-gate paths against the rwb-treatment fake, with no call and no write; tests for AC2 and AC8.
3. Build TdrInputAssembler against the rwb-source-data and rwb-case fakes, with the masking and the freshness rule; tests for AC1, AC12 and AC13.
4. Add the model gateway client, the schema check and the timeout and error paths against the model stub; tests for AC4, AC5 and AC15.
5. Add the record write before the answer and the run row in one transaction, with the rollback path; tests for AC6 and AC10.
6. Add the idempotent repeat: the key lookup, the stored answer and the counted hit; test for AC7.
7. Add the outbox rows and the relay, and the registry check before the relay; test for AC11.
8. Build the suggestion area of SCR-14 against the gateway-bff route stub, with the refusal path; test for AC14, and keep AC3 green through the rwb-decision fake.
9. Run the boundary scan and the two admin reads against the baseline of RWB-P10-E1058-APP; test for AC10 and AC14.

**Done when.** The tests of section 16 pass with mode "OFF" in SIT; AC1 and AC15 pass against the model stub until the TDR model is deployed; no suggestion is returned without its record; every event is published once from the outbox; and the pipeline finds no read of another service's table and no list, threshold or schema limit in code.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-007 | No suggestion: the model is not in service, the call timed out, the gateway answered an error or the schema check failed | No offer suggestion is available for this treatment. The TDR model is not in service. |
| MSG-P7-003 | The decision record cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without Platform administration reads the agent runs | You cannot {action} here. Your role does not include it. |

The three messages are the legacy messages of RWB-E2-032 and keep their wording character for character. MSG-GEN-001 (a required value is empty) and MSG-P10-001 (a configuration file fails a check) belong to the agent platform story and are not restated here. No message ID is added by this story.

### 15. Screens and states

SCR-14 Treatment record (states draft, submitted, approved, booked, broken; empty, with no suggestion: the suggestion area shows not available with MSG-P10-007; error, on a timeout, gateway error or schema failure: MSG-P10-007; no access, an action outside the role's permission: refused with MSG-P4-002; loading: Not specified in the source documents (DOR-RWB-P10-E2032-APP-10)) keeps the suggestion area in the draft state that the legacy story describes: the suggestion shown with its terms, model code and version, or not available with MSG-P10-007. The officer edits the offer fields as before and the suggestion is never copied into them. What changes is the path: the panel is served by the gateway-bff composite route, which calls the agent read on `/api/recovery/agent/v1` and merges the answer with the other services the screen needs, so the browser calls no service directly (DP-19). The route name and path, and the field order and masking of the panel, are Not specified in the source documents (GAP-0633; ASM-0982) and are agreed with the route contract RWB-PLT-N001-CON.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E2-032-09 | Access | Contract | RW-RESTRUCT calls GET /admin/agent-runs through the route; refused with MSG-P4-002 |
| TC-E2-032-01 | AC1, BR1, BR3 | Component | Treatment "T-1001", the account facts of case "RW-2026-001001", the model stub answer of 84 installments of 18,900.00 baht |
| TC-E2-032-02 | AC2, BR2 | Component | Policy "TDR_OFFER" version "P1" with mode "OFF", review date 2027-02-28 |
| TC-E2-032-03 | AC3 | Component | A suggestion recorded on "T-1001" and the sealed record served by the rwb-decision fake |
| TC-E2-032-04 | AC4, BR4 | Component | The model stub silent for 61 seconds |
| TC-E2-032-05 | AC5, BR4 | Component | An answer with installments -12 |
| TC-E2-032-06 | AC6, BR3 | Component | The decision-record library write forced to fail |
| TC-E2-032-07 | AC7, BR5 | Component | A second request for "T-1001" |
| TC-E2-032-08 | AC8, BR6 | Component | Treatment "T-1002" of type "SETTLEMENT" |
| TC-E2-032-10 | Principle 5 | Component | The record write forced to fail after the model answers; no suggestion, no run row and MSG-P7-003 |
| TC-E2-032-11 | AC9, BR12 | Contract | The operation on `/api/recovery/agent/v1` answering with the eight members; the rwb-treatment fake and the 2 s budget on the other hops |
| TC-E2-032-12 | AC10, BR8, BR9 | Component | Policy version "P2" and one run; the `agent_run` row, the `agent_policy` read and the boundary scan of the sources |
| TC-E2-032-13 | AC11, BR10, BR13 | Component | A committed run; the outbox rows, the two topic messages, the relay repeated, the registry refusal and the `.dlt` route |
| TC-E2-032-14 | AC12 | Component | The rwb-source-data fake with the facts of case "RW-2026-001001", an error answer and facts dated before the business date |
| TC-E2-032-15 | AC13 | Contract | The rwb-case parameter and reference-data fakes; a mode outside LOV-AUTONOMY and a status outside LOV-AGENT-RUN |
| TC-E2-032-16 | AC14 | Contract | The gateway-bff route stub for the two admin reads and SCR-14; the refusal of RW-RESTRUCT with MSG-P4-002 |
| TC-E2-032-17 | AC15 | NFR | The model stub silent for 61 seconds and answering a 4xx and a 5xx; the policy timeout of 60 seconds and the 2 s budget of the other hops |
| TC-E2-032-18 | §12.7 (ASM-3438) | Component | Each table of §12.7 (agent_run, agent_policy, agent_prompt and the PLT library tables) at its boundary |
| TC-E2-032-19 | AC16, BR7, BR11 | Component | Treatment "T-1001" of type "RESTRUCTURE" on case "RW-2026-001001"; rwb-treatment contract mock |
| TC-E2-032-20 | AC17 | Not specified in the source documents (NEWAC-RWB-P10-E2032-APP-AC17) | Not specified in the source documents (NEWAC-RWB-P10-E2032-APP-AC17) |

The ten legacy test cases keep their IDs, their `Covers` values and their `Data`, in the order of the split plan. Their levels map System to Component, Access to Contract and Resilience to Component, because the cross-service proof of this key is carried by the integration story of the wave. No `-ITG` copy is held here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the model code, the model version, the output schema, its limits, the timeout, the confidence floor, the mode and the review date are rows of the policy version in force (BR8; BR-P10-010).
- No account number or customer name in logs, tests, workflow payloads, prompts or events: the inputs are masked before the model call, the account number and the customer name never reach a topic or a log, the workflow payloads pass the payload codec (BR10). Fields classed Customer data, Confidential are shown only within the role's scope.
- No read of another service's tables: the account and the payments come through rwb-source-data's contract, the treatment through rwb-treatment, the case and the parameters through rwb-case, and the record is written through the P7 library; `rwb_agent` holds no foreign key into another schema (DP-01, DP-05).
- One base and one topic per service: the operation answers on `/api/recovery/agent/v1` and the events leave on `rwb.agent.events.v1` and `rwb.decision-record.v1`; no other service's path or topic is declared (DP-13, DP-14).
- The suggestion is written to no offer field, no treatment status and no case status; it is advice on the run and on the record (BR7).
- A suggestion is returned only after its record is committed, and both events are published only from the outbox (BR3, BR13).
- No value is defaulted for a fact the owner contract did not return, and no run status outside LOV-AGENT-RUN is written (BR11; X11).
- Every fixture is synthetic; no production account, payment, model answer or record is copied into a fake or a test.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CHO-006 | A treatment record holds every offer's type, terms, approval and outcome | Business Requirements Program, section 5.3 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-32, R-UNI-40 | TC-E2-032-02, TC-E2-032-04, TC-E2-032-05, TC-E2-032-07, TC-E2-032-08, TC-E2-032-14, TC-E2-032-16 |
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-032-01, TC-E2-032-03, TC-E2-032-06, TC-E2-032-09, TC-E2-032-10, TC-E2-032-12, TC-E2-032-13 |
| D-RCV-60 DP-01 | The run and the policy are rows of `rwb_agent`, and no other schema is read or written | Template and Rules §R5.5; Arch v5 slide 41 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-032-12 |
| D-RCV-60 DP-03 | The decision record is written locally before the answer and carried to the central ledger on `rwb.decision-record.v1` | Template and Rules §R5.5; ADR-022 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-39 | TC-E2-032-03, TC-E2-032-06, TC-E2-032-10, TC-E2-032-13 |
| D-RCV-60 DP-05 | The account and payment facts are read through rwb-source-data's contract and never from a table | Template and Rules §R5.5; ADR-010 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-032-01, TC-E2-032-14 |
| D-RCV-60 DP-06, DP-07 | The parameters and the list values are read through the rwb-case contracts | Template and Rules §R5.5 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-032-15 |
| D-RCV-60 DP-09 | The run completion is published as EV-28 from the outbox as a CloudEvents 1.0 message | Template and Rules §R5.5; Arch v5 slide 43 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | R-UNI-33 | TC-E2-032-13 |
| D-RCV-60 DP-11, DP-13 | The in-process interface becomes one operation on `/api/recovery/agent/v1` with one hop and a 2 s client budget | Template and Rules §R5.5; ADR-020 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-032-11, TC-E2-032-17 |
| D-RCV-60 DP-19 | The admin reads and SCR-14 are reached through the gateway-bff route | Template and Rules §R5.5; Arch v5 slide 41 | FEAT-AGT-10 | 7.3 Negotiate settlement or deed in lieu | None | TC-E2-032-16, TC-E2-032-09 |

The two requirement IDs are those of the legacy story and of the Business Requirements Program; the feature is FEAT-AGT-10 of FSD P10 v3 A2.10 and the Epics 3 to 8 specification row E2, P10. The decisions are D-RCV-60 and its patterns. No BRD section is raised as a gap: both requirement rows are published.

### 19. Out of scope

- Building or training the TDR model, which is the TDR team's and outside the Workbench (legacy section 19).
- The settlement and restructure agent proposing plan terms, shadow from Epic 2 and live from Epic 3 per the agent catalog.
- Affordability and plan calculation (ACE restructure calculator, R-RES-06).
- The agent runtime baseline, the policy and prompt load and approve operations, and the two admin reads (RWB-P10-E1058-APP, RWB-P10-E1058-CON).
- The rest of the agent runtime: the case intake, the screening and the legal document agents, the guardrail checker as a shared capability, the evaluation harness and the monitor (RWB-P10-E1058-APP, RWB-P10-E1060-APP, RWB-P10-E1063-APP).
- The change of an autonomy level and its approval (RWB-P10-E3030-APP, RWB-P10-E8004-APP).
- The contract shapes of the suggestion operation, the record mapping, the EV-28 payload and the fakes (RWB-P10-E2032-CON).
- The network path to INT-23, the topic and its retry and `.dlt` topics, the queue, the secrets and the capacity (RWB-P10-E2032-INF).
- The treatment, the case, the account data and the reference data themselves, and the rights, the scope and the masking policy (rwb-treatment, rwb-case, rwb-source-data, rwb-access).
- The central decision ledger, its sealing and its read (P7 rwb-decision).
