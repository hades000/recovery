# RWB-P10-E1059-APP Case intake agent in shadow [E1b]

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1059-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Size | Set by the squad at refinement (DOR-RWB-P10-E1059-APP-16) |
| Legacy key | RWB-E1-059 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP09, DP11, DP13, DP15, DP19, DP20 |
| Readiness decisions | RD-P1-005, RD-P1-041, RD-P1-062 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| Depends on (build) | RWB-P10-E1059-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-TE013-CON, RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P3-E1030-CON, RWB-P5-E1053-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-024, FR-P10-025) |
| Status | Draft (directive resolutions) |

**Version 3 changes** (D-RCV-60 P1 developer readiness, RD-P1 register).

- RD-P1-062: Define the missing data date and fail-closed age handling for never-stamped inputs.
- The consumed freshness read carries status `LOADED` / `STALE` from the stamp in use and the never-stamped answer (RD-P1-005, RD-P1-041); the fake serves all three. Never-stamped input persists `data_as_of` null.

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-059 for rwb-agent. The behaviour of the legacy story is unchanged - the intake agent still builds a case file summary and the gap flags for every new Epic 1 case in shadow and is still scored against the business analysts' review of the same 200 cases - and what changes is service placement only: the run tables move into schema `rwb_agent` (DP-01), the run is started through the agent runtime contract of RWB-P10-TE013 (DP-20) from the CaseCreated event instead of an in-process listener, the ACE account, appraisal, contact and freshness facts are read through the rwb-source-data contract instead of `v_ace_*` (DP-05), the case and party facts, the parameters and the reference lists are read through the rwb-case contracts (DP-06, DP-07), the run completion is published as `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` through the outbox and consumed through the inbox (DP-09), the parameters that decide the run are read through the client library (DP-06), the two evaluation operations stay on the base `/api/recovery/agent/v1` (DP-13) and are baselined in the platform contract of RWB-P10-E1058-CON, the run key index arrives with the service's own migration `V10_004__intake_run_key.sql` (DP-15), and the reads reach the service through the gateway-bff route (DP-19). The legacy decision log write is dropped in shadow mode, so no decision record is written by a shadow run (DP-03 applies to the run record only through the platform library). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P10-E1059-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (22 resolved, 18 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60 P1 developer readiness (RD-P1 register), 27 November 2026: version 3, as listed under Version 3 changes.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the case intake agent to build a case file summary and flag gaps for every new Epic 1 case in shadow mode inside rwb-agent - the shadow run started from the CaseCreated event through the agent runtime contract, its summary and gap flags stored in agent_run in schema `rwb_agent`, its inputs read through the rwb-source-data, rwb-case and rwb-document contracts as SY-AGENT, and its completion published as `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`**, so that **the agent is scored against the business analysts' review before any case owner sees its output**.

### 2. Business rationale

A case owner who takes over a case at day 90 reads every account, document and appraisal to find what is missing before deciding the next step. The intake agent prepares that summary and the list of gaps. In Epic 1 it runs in shadow only: its output is stored, compared with the business analysts' review of the same 200 cases and shown to nobody, so the step to autonomy level 1 in RWB-E2-028 is decided on a measured agreement rate. Inputs are masked before the model call (REQ-ACA-005) and the agent reads data as SY-AGENT (REQ-ACA-010).

In the legacy delivery the listener, the assembler, the scorer, the output schema and the run rows sat in one module and one schema, the case, the accounts, the valuations and the contact points were read through in-process query services, the case creation event was a row of the same schema, the run completion was an application event written by the same deployment, and the evaluation was started on a path of the monolith. The behaviour is unchanged, so the disposition is Split (rework): the legacy story is not preserved word for word, and its behaviour is carried onto the service. What changes is where each fact lives and how it is reached:

- The case, the parties, its accounts and the queues are P3 rwb-case, schema `rwb_case`, and are read only through the P3 contracts; the legacy in-process `CaseQueryService` becomes the two reads of the case contract and the case creation event (DP-01, DP-11; BR9).
- The ACE account facts, the appraisals, the contact points and the business-date completeness that sets `data_as_of` are P1 rwb-source-data and are read through its contract, never through `recovery.v_ace_*` views of the service (DP-05; BR9).
- The documents and their stored fields are P5 rwb-document and are read through its contract as SY-AGENT (DP-01; BR9).
- The run rows - agent_run, agent_sample, agent_evaluation_run and agent_evaluation - are P10 rwb-agent, schema `rwb_agent`, and this story writes them and no others (DP-01; BR10).
- The approved policy and prompt versions, the gap types of the output schema, the timeout, the confidence floor and the allowed tools stay rows of agent_policy and agent_prompt, read at run time through the parameters contract and the configuration read and never written in code (DP-06; BR8).
- The run is started through the agent runtime contract of RWB-P10-TE013 on the CaseCreated event, with the 60 second policy budget, instead of a listener inside the monolith (DP-20; BR7).
- The run completion is one CloudEvents 1.0 message on the service's own topic, inserted in the outbox in the same transaction as the run row and deduplicated by the consumers' inbox (DP-09; BR7).
- The evaluation operations are served on the base `/api/recovery/agent/v1`, and the legacy monolith base is retired for them (DP-13).
- The run key index arrives with the service's own Flyway sequence, in its own schema (DP-15; AC3, AC6).
- RW-COE and RW-RISK reach the reads through the gateway-bff route, which is the only route a screen will use (DP-19).

The cross-service behaviour of this key - that a case created by rwb-case, with its ACE facts and its documents, produces one shadow run and no change in force, and that the same 200 cases produce one complete evaluation - is proved by the integration copy of this key and by the harness RWB-ITG-W1J01-ITG, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes, and it owns seven of the eight legacy acceptance criteria, AC1, AC2, AC3, AC4, AC6, AC7 and AC8. The legacy criterion AC5 belongs to the integration slice of this key, RWB-ITG-E1059-ITG, and is not reconstructed here; the gap GAP-0610 records it.

### 3. Preconditions

- RWB-P10-E1058-APP is done: the agent platform, the orchestrator, the model gateway client, the prompt and policy store, the guardrail and the admin configuration operations exist in rwb-agent, agent "INTAKE" exists, and a run can be made in mode SHADOW.
- RWB-P10-TE013-APP is done: the agent runtime client with fallback exists in rwb-agent, so a run is started, read and given its 60 second budget through one contract.
- RWB-P10-E1059-CON is published: the two run operations this key needs on `/api/recovery/agent/v1`, the intake answer shape "intake-summary-v1", the `rwb.agent.AgentRunCompleted.v1` payload and the five contract fakes, so this story builds against a fixed shape and its fakes from Day 1.
- RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON are published: the decision-record library (used by the platform's run record and not by a shadow run), the parameters client library, the reference-data client library, the outbox and inbox library with its retry and `.dlt` rule, the per-service Flyway sequence with parameterized schema names, and the gateway-bff route contract with its stub.
- The `rwb_agent` schema baseline exists with the standard record columns and the Flyway history table of the service, and the four run tables of this story are created by the P10 migrations of RWB-P10-E1058-APP; this story adds one index migration only.
- The rwb-case contracts of RWB-P3-E1030-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the case creation event `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` with its case, party and account reads; the parameters contract; and `GET /api/recovery/case/v1/admin/lists/{listCode}` for the reference lists the agent needs. This story builds against those contracts and their fakes and never reads `rwb_case`.
- The rwb-source-data contract is available for the ACE reads (`POST`/`GET` tool operations of section 12.2, one hop, 2 s) and returns the account facts, the appraisals, the contact points and the business-date completeness stamp, so `data_as_of` comes from the owner and not from a view (DP-05).
- The rwb-document contract of RWB-P5-E1053-CON is published: `GET /api/recovery/document/v1/cases/{caseId}/documents` returns the documents of a case with their type and review status. This story builds against that contract and its fake (ASM-0864).
- The rwb-access contract is available for the right check: `POST /api/recovery/access/v1/authorise` granting Rules and parameters C to RW-COE and R to RW-RISK and refusing a role without the right.
- Approved agent_policy "INTAKE" version "P1" with autonomy_mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_accounts, read_documents, read_valuations, read_contact_points, and output schema "intake-summary-v1".
- Approved agent_prompt "INTAKE" version "PR1".
- The output schema lists the gap types as data: MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT, STALE_INPUT.
- Labeled sample "INTAKE-S1" version 1 is loaded by RW-COE: the business analysts' review of 200 Epic 1 cases, one row per case and gap type with expected value Y or N.
- The login of this service is the rwb-agent login: Not specified in the source documents (GAP-0610; ASM-0861).
- The release date 30 November 2026 is tentative and is copied unchanged.
- Contract version fixed: this story builds against version 5.0.0 (info.version in API Specification v5) of the rwb-agent, rwb-case, rwb-source-data, rwb-document and rwb-access contracts, on their `/v1` base paths.

### 4. Flow

1. rwb-case creates case "RW-2026-000301", writes the row in `rwb_case` and inserts `rwb.case.CaseCreated.v1` in its outbox in the same transaction; the relay publishes it to `rwb.case.events.v1` (P3; RWB-P3-E1030-CON).
2. IntakeShadowListener in rwb-agent consumes the event through its inbox, so a duplicate event ID is dropped before any work, and calls the agent runtime of RWB-P10-TE013 for agent "INTAKE" with the run key "INTAKE:<caseId>:<businessDate>" (DP-09, DP-20; AC3, AC6).
3. The runtime starts one run: it reads the case through `GET /api/recovery/case/v1/cases/{caseId}`, the accounts and parties through their case reads, the documents through the rwb-document contract, the appraisals and contact points through the rwb-source-data contract, all as SY-AGENT, and marks `data_as_of` from the freshness stamp the owner returns (DP-01, DP-05, DP-11; BR4, BR7). Per product the answer carries `status` `LOADED` or `STALE` from the stamp in use (the latest stamp row); a never-stamped product answers `businessDate` null with `status` `STALE` (rwb-source-data.yaml 5.1.0; RD-P1-005, RD-P1-041). When never stamped, store `data_as_of` null, omit `X-Data-As-Of` and show the STALE indicator. A required input-age check fails (RD-P1-062).
4. IntakeInputAssembler masks personal fields with the tokens of the mask in force and builds the request of the model gateway; no unmasked value leaves rwb-agent (BR7; REQ-ACA-005).
5. The model is called through the gateway on the private endpoint INT-23 with the output schema "intake-summary-v1" and is bounded by timeout_seconds of the policy version in force, 60 seconds (BR8; NFR-010).
6. IntakeOutputGuardrail checks the answer against the schema, the allowed tools and the confidence floor 0.80, and stores the summary and the gap flags on the agent run with mode SHADOW together with the policy version "P1", the prompt version "PR1" and the model version (AC1, AC2, AC4).
7. The run row and the `rwb.agent.AgentRunCompleted.v1` outbox row are written in one `rwb_agent` transaction and the relay publishes the event to `rwb.agent.events.v1` with the case ID as its key; no screen, no case field, no task, no queue and no decision record changes (AC1; BR1, BR2).
8. RW-COE starts the evaluation of "INTAKE" on sample "INTAKE-S1" through `POST /api/recovery/agent/v1/admin/agent-evaluations`, whose contract is baselined in RWB-P10-E1058-CON and is not re-declared here (AC8; ASM-0865).
9. The evaluator runs the agent in shadow on each of the 200 sample cases and compares each gap flag with the label, using only the labeled cases, and writes one agent_evaluation row per gap type with the agreement rate, precision, recall and sample size at four decimals (AC2, AC7; BR5).
10. RW-COE reads the scores through `GET /api/recovery/agent/v1/admin/agent-evaluations`, one hop through the gateway-bff route, and the response carries run metadata only: no summary and no gap flags reach a user-facing path in shadow mode (AC1; DP-19; section 15).
11. The run writes only the four tables of `rwb_agent`; the case, the accounts, the documents and the valuations are read through their owners' contracts and no value in force changes (BR9, BR10; section 17).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent times out or fails a guardrail on a case | Run stored with status TIMED_OUT or GUARDRAIL_FAILED; counted as a failure type; no retry for that event | None to a user | AC4 |
| X2 | The ACE batch for the day is not COMPLETE | Run proceeds; data_as_of holds the stamp business date, or null when never stamped and the agent must return gap STALE_INPUT; a run without it fails check SCHEMA_RULE | None to a user | None of this story's criteria: the legacy AC5 sits with RWB-ITG-E1059-ITG (GAP-0610) |
| X3 | The same CaseCreated event arrives twice | One run for the case and business date (R-UNI-40) | None to a user | AC6 |
| X4 | Labels cover fewer cases than the sample | Agreement is computed on labeled cases only; sample size shows the labeled count | None to a user | AC7 |
| X5 | A user endpoint is asked for shadow output | No endpoint returns the output content; GET /admin/agent-runs returns metadata only | None to a user | AC1 |
| X6 | Evaluation started on an empty sample | Refused with 422 | MSG-P10-002 | AC8 |
| X7 | A role without the right starts or reads evaluations | Refused with 403 | MSG-P4-002 | AC13; TC-E1-059-09 |
| X8 | The rwb-source-data, rwb-case or rwb-document contract does not answer inside the 2 s budget | The run stops before the model call, holds status TOOL_UNAVAILABLE with fallback true, the failure is counted, and no partial answer is stored | None to a user | AC9; BR9; section 13 |
| X9 | The policy version in force holds no value for the timeout, the floor or the allowed tools | No model call is made, the run holds status DISABLED or fails closed before the call, and the missing policy value is named on the run; no value in code is used as a default | None to a user | AC10; BR8 |
| X10 | The outbox relay cannot reach `rwb.agent.events.v1` | The run row stands and the event waits in the outbox; it is published when the topic returns, and a payload that fails its registry subject goes to the `.dlt` topic with an alert | None to a user | AC11; BR7 |
| X11 | The migration `V10_004__intake_run_key.sql` fails in the service's Flyway sequence | The new version does not start and the version in force keeps serving; no run row is written by the new build | None | AC12; BR10 |

X1 to X7 are the legacy exception paths of RWB-E1-059 carried onto the service; X8 to X11 are the failures that appear when the reads leave the service and when the schema, the policy row and the topic become the service's own responsibility. X7 is reached by criterion AC13 and proved by the access test case TC-E1-059-09, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the platform contract, the agent runtime contract, the published P1, P3, P4 and P5 contracts with their fakes and its own schema objects; it waits only for the in-lane stories RWB-P10-E1058-APP and RWB-P10-TE013-APP |
| Negotiable | The package layout, the component names and the poll of the read are design; the gap types, the agent, the policy and prompt versions, the timeout, the floor, the sample, the counts and the message IDs are fixed by the legacy story and by the policy rows |
| Valuable | Gives the measured agreement rate that decides whether the case owner gets the summary in Epic 3 |
| Estimable | One listener, one prompt, one output schema, one sample, one scorer, one migration and five contract clients; no screen |
| Small | One developer and one analyst for two weeks, as in the legacy estimate |
| Testable | Each of the seven criteria of section 7 is one automated test on an observable: a stored row, a REST answer, a failure count, an agreement rate, a schema refusal or a scan of the source |

### 7. Acceptance criteria

```gherkin
Feature: Case intake agent in shadow [E1b]

  Background:
    Given agent "INTAKE" has approved policy "P1" with mode "SHADOW" and prompt "PR1"
    Given the gap types in output schema "intake-summary-v1" are MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT

  Scenario: AC1 Shadow run (legacy RWB-E1-059 AC1)
    Given the rwb-case contract mock returns the 200 Epic 1 cases, their CaseCreated events created between 2026-11-30 and 2026-12-04, and no agent output on GET /cases/{caseId} and GET /cases/{caseId}/timeline
    Given 200 Epic 1 cases created between 2026-11-30 and 2026-12-04
    When the agent runs on each CaseCreated event
    Then 200 agent runs with mode "SHADOW" store a summary and gap flags
    Then no case field, task, queue or decision record changes
    Then GET /cases/{caseId} and GET /cases/{caseId}/timeline return no agent output
    Then GET /admin/agent-runs returns the 200 runs without the summary or the gap flags

  Scenario: AC2 Agreement rate (legacy RWB-E1-059 AC2)
    Given the business analysts' review of the same 200 cases in sample "INTAKE-S1" version 1
    When the comparison runs
    Then one score row per gap type holds the agreement rate, precision, recall and sample size 200
    Then for MISSING_DOCUMENT with 182 agreeing cases the agreement rate is 0.9100
    Then each score row holds policy "P1", prompt "PR1" and the model version

  Scenario: AC3 A new case starts one shadow run (legacy RWB-E1-059 AC3)
    Given the rwb-case contract mock returns case "RW-2026-000301" created on 2026-11-30 and its CaseCreated event
    Given case "RW-2026-000301" is created on 2026-11-30
    When EV-01 CaseCreated is processed
    Then one agent run exists with key "INTAKE:<caseId>:2026-11-30", trigger "CaseCreated" and mode "SHADOW"

  Scenario: AC4 A failed run is counted and not retried (legacy RWB-E1-059 AC4)
    Given the rwb-case contract mock returns case "RW-2026-000302" and its CaseCreated event
    Given the model stub does not answer for case "RW-2026-000302"
    When the agent runs
    Then the run holds status "TIMED_OUT" and fallback true
    Then the system makes no second run for that event
    Then the failure count for type "TIMED_OUT" on 2026-11-30 is 1

  Scenario: AC6 A repeated event has no further effect (legacy RWB-E1-059 AC6)
    Given the rwb-case contract mock returns the CaseCreated event of case "RW-2026-000301" for 2026-11-30 with one event ID
    Given EV-01 CaseCreated for case "RW-2026-000301" was processed on 2026-11-30
    When the same event arrives again with the same event ID
    Then one agent run exists for the case and date and the repeat is counted (R-UNI-40)

  Scenario: AC7 Partly labeled sample (legacy RWB-E1-059 AC7)
    Given sample "INTAKE-S1" version 2 has labels for 180 of 200 cases
    When the comparison runs
    Then each score row holds sample size 180
    Then the system lists the 20 unlabeled cases as unlabeled on the evaluation run

  Scenario: AC8 Empty sample (legacy RWB-E1-059 AC8)
    Given sample "INTAKE-S3" has no labeled rows for "INTAKE"
    When RW-COE starts the evaluation
    Then the system refuses the request with 422 and MSG-P10-002

  Scenario: AC9 Contract read stops before the model call (exception X8) (new, D-RCV-60)
    Given the rwb-source-data contract does not answer inside the 2 s budget for case "RW-2026-000301"
    When the agent runs
    Then the run holds status "TOOL_UNAVAILABLE" and fallback true, and stops before the model call
    Then no partial answer is stored and the failure is counted

  Scenario: AC10 Missing policy value stops the call (exception X9) (new, D-RCV-60)
    Given the policy version "P1" holds no value for the timeout
    When the agent runs
    Then no model call is made and the run holds status "DISABLED" or fails closed before the call
    Then the missing policy value is named on the run

  Scenario: AC11 Outbox holds the event while the topic is down (exception X10) (new, D-RCV-60)
    Given the topic "rwb.agent.events.v1" cannot be reached
    When the agent run completes
    Then the run row stands and the event waits in the outbox
    Then the event is published when the topic returns

  Scenario: AC12 A failed migration keeps the version in force (exception X11) (new, D-RCV-60)
    Given the migration "V10_004__intake_run_key.sql" fails in the service's Flyway sequence
    When the new version starts
    Then the new version does not start and the version in force keeps serving
    Then no run row is written by the new build

  Scenario: AC13 A role without the right is refused (exception X7, legacy access test) (new, D-RCV-60)
    Given a role without the right to start or read evaluations
    When it starts or reads an evaluation
    Then the system refuses the request with 403 and MSG-P4-002
```

**Target reading.** The agent, its policy and prompt versions, the gap type enum, the sample, the 200 cases and their dates 2026-11-30 to 2026-12-04, the agreement rate 0.9100 with 182 agreeing cases, the sample sizes 200 and 180, the failure type TIMED_OUT, the message IDs and the run key are the legacy values of RWB-E1-059, copied character for character. The scenario lines keep their legacy titles and every legacy Given, When and Then (in AC1 "decision log entry" now reads "decision record"), and each one carries the origin tag of its legacy criterion. Four criteria carry one inserted line as their first Given, `Given the rwb-case contract mock returns ...`, because the legacy criterion reads a case, its event or its absence across the P3 boundary: AC1 reads the case and the silence of the case reads, AC3 and AC6 read the case and its event, and AC4 reads the case of the silent model. AC2, AC7 and AC8 need none: they assert the comparison, the labeled count and the refusal of an empty sample, all inside rwb-agent. The in-process `CaseQueryService`, `DocumentQueryService` and `CollateralQueryService` of the legacy section 12 become one-hop operations of their owners behind the 2 s budget (DP-11, DP-05, DP-01), so a run row of this story is built from a value the owner served and not from a table read. The seven criteria are the legacy AC1, AC2, AC3, AC4, AC6, AC7 and AC8, and AC9 to AC15 are the story's own criteria: AC9 to AC13 for exceptions X8 to X11 and the access refusal X7, AC14 for rules BR3 and BR7 to BR11, and AC15 for a disallowed status change; the legacy AC5 is owned by the integration slice RWB-ITG-E1059-ITG and is not reconstructed here (GAP-0610).

AC14: Given the run is stored in shadow mode, When the rules BR3, BR7, BR8, BR9, BR10 and BR11 are checked, Then the gap types come from the approved output schema, no personal value reaches a log, an event or a prompt, the timeout, floor and allowed tools come from the approved policy version, no table of another service is read, only the four tables are written, and no decision record is written (BR3; BR7; BR8; BR9; BR10; BR11).

AC15: Given a run holds a status and a status change that the model does not allow is requested, When the change is requested, Then the system refuses the change and the run keeps its status.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the output is stored and never shown, and nothing on the case changes | agent_policy.autonomy_mode (DF-AGT-008) = SHADOW; legacy BR1 |
| BR2 | The agent runs once per case per business date on EV-01 CaseCreated | R-UNI-40; agent_run.idempotency_key (DF-AGT-045); legacy BR2 |
| BR3 | Gap types are the enum in the approved output schema, not code | Principle 1; agent_policy.output_schema_ref (DF-AGT-006); legacy BR3 |
| BR4 | When an input is older than the business date, the answer must include STALE_INPUT | VR-P10-003-1; MSG-P1-001 rule of the data products; legacy BR4 |
| BR5 | Agreement rate per gap type = cases where agent flag equals label / labeled cases, 4 decimals | agent_evaluation.agreement_rate (DF-AGT-094); legacy BR5 |
| BR6 | A run that times out or fails a check is not retried for the same event | R-UNI-32; agent_run.fallback (DF-AGT-047); legacy BR6 |
| BR7 | Personal fields are masked before the model call, and no personal value reaches a log, an event or a prompt | CTL-11; REQ-ACA-005; legacy BR7 |
| BR8 | The timeout 60 seconds, the confidence floor 0.80, the allowed tools and the gap types are values of the approved policy version and the output schema, read at run time; a code default is a defect and a missing value stops the call | DP-06; Principle 1; FSD P10 v3 BR-P10-003 |
| BR9 | rwb-agent reads no table of another service: the case, the parties and the accounts come through the rwb-case contracts, the ACE facts and the freshness stamp through rwb-source-data, the documents through rwb-document, and no foreign key crosses a schema | DP-01; DP-05; DP-11; Arch v5 slides 15 and 16 |
| BR10 | The story writes four tables only - agent_run, agent_sample, agent_evaluation_run and agent_evaluation - all in `rwb_agent`, and adds the run key index by its own migration in its own Flyway sequence | DP-01; DP-15; Ownership Map (P10 owns the four tables) |
| BR11 | A shadow run writes no decision record: nothing in force changes, so the record that proves a decision is not written for an answer nobody acts on | Legacy section 7 AC1 and section 12; DP-03; legacy BR1 |

### 9. State transitions

None to a case: this story does not change a case status. The state of one run of agent "INTAKE":

| From | Event | Condition | To |
|---|---|---|---|
| None | CaseCreated consumed and the run key is new | The policy version in force has mode SHADOW and its values are complete | Run row with mode SHADOW, status ANSWERED, fallback false (DF-AGT-046, DF-AGT-047) |
| None | CaseCreated consumed | A run exists for the same case and business date | No row; the repeat is counted (R-UNI-40) |
| None | CaseCreated consumed | The policy values are missing | No model call; the run is refused before the call and the missing value is named (X9) |
| ANSWERED | The guardrail passes and the floor is met | None | ANSWERED with the summary, the gap flags and the confidence stored (DF-AGT-049, DF-AGT-050) |
| None | The model does not answer inside 60 seconds | None | TIMED_OUT with fallback true, no retry for that event (AC4) |
| None | The guardrail refuses the answer | A schema, tool or floor check fails | GUARDRAIL_FAILED with fallback true and the check code in guardrail_result (DF-AGT-048) |
| None | The answer is under the confidence floor 0.80 | None | BELOW_FLOOR with fallback true |
| None | A consumed read fails inside the 2 s budget | None | TOOL_UNAVAILABLE with fallback true (X8) |

The state of one evaluation run: RUNNING to DONE, or FAILED when a sample row cannot be scored (DF-AGT-077). No state outside LOV-AGENT-RUN and LOV-EVAL-STATUS is written (TSD P10 v2 T3.2).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Reads the case, the accounts, the parties, the documents, the appraisals and the contact points through the owner contracts (Documents R, Case record R) |
| SY-CASEWF, case and workflow in rwb-case | Publishes CaseCreated; not called by this story |
| RW-COE, center of excellence analyst | Loads the labeled sample, starts the evaluation, reads the scores (Rules and parameters C) |
| RW-RISK, risk and model risk officer | Approves the policy and prompt versions and reads the scores (Rules and parameters A and R) |
| rwb-agent service identity (the rwb-agent login, DP-02) | Consumes the event, writes the four tables in `rwb_agent`, reads the P1, P3, P5 and P4 contracts, publishes the run completion |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata (Platform administration R) |
| RW-CASEOWN, case owner | Sees nothing from this story |
| rwb-access (P4) | Answers the right check `POST /api/recovery/access/v1/authorise` and refuses a role without the right with MSG-P4-002 |
| No role | Reads `rwb_case`, `rwb_source_data`, `rwb_document` or any other service's schema, reads the shadow output of a case, or changes a value in force |

The login of the service is Not specified in the source documents (GAP-0610; ASM-0861); the story names it "the rwb-agent login (DP-02)" until it is agreed. No delegation of authority level applies: the approval of the policy and prompt versions is the Rules and parameters A right, as in the legacy story.

### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, subject_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, data_as_of, run_at, evaluation_run_id | Write; the summary and the gap flags sit in output and the owner-returned business date in data_as_of |
| DF-AGT-061 to DF-AGT-069 | agent_sample | id, agent_code, sample_code, sample_version, subject_type, subject_id, label_key, expected_value, labeled_by | Read at the comparison of AC2 and AC7; loaded by RWB-P10-E1058-CON's operation |
| DF-AGT-070 to DF-AGT-085 | agent_evaluation_run | id, agent_code, sample_code, sample_version, policy_version, prompt_version, model_version, status, started_at, finished_at, requested_by, failure_counts, review_count | Write for the comparison of the intake sample |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation | id, evaluation_run_id, approach, label_key, sample_size, true_positive, false_positive, false_negative, agreement_rate, precision_value, recall_value | Write: one row per gap type, with agreement, precision, recall and sample size at four decimals |
| DF-AGT-002, DF-AGT-008, DF-AGT-011, DF-AGT-012, DF-AGT-013, DF-AGT-032, DF-AGT-033, DF-AGT-034, DF-AGT-035, DF-AGT-016 | agent_policy, agent_prompt | the values of the approved policy version "P1" and prompt version "PR1": autonomy_mode, confidence_floor 0.80, timeout_seconds 60, allowed_tools, output_schema_ref, validity dates | Read as versions through the configuration read of RWB-P10-E1058-APP; no column written |
| DF-CAS-001, DF-CAS-002, DF-CAS-003, DF-CAS-005, DF-CAS-013, DF-CAS-016, DF-CAS-017 | recovery_case (rwb_case, owner P3) | id, case_no, product_group, status, entry_date, total_outstanding_at_entry, prescription_date | Read through the rwb-case contract |
| DF-DOC-001, DF-DOC-002, DF-DOC-004, DF-DOC-008 | document (rwb_document, owner P5) | id, case_id, document_type, review_status | Read through the rwb-document contract |
| DF-ACE-191, DF-ACE-193 | valuation (rwb_source_data, owner P1) | appraised_value, appraisal_date | Read through the rwb-source-data contract |
| DF-ACE-075, DF-ACE-080 | contact point (rwb_source_data, owner P1) | contact_type, usage_code | Read through the rwb-source-data contract |
| the account fields of the ACE data product | account facts (rwb_source_data, owner P1) | the account rows of the case, as the rwb-source-data contract returns them; the field IDs are Not specified in the source documents (GAP-0610; ASM-0866) | Read through the rwb-source-data contract |
| the batch completeness stamp of the data products | data product freshness (rwb_source_data, owner P1) | the last complete business date | Read through the rwb-source-data contract, used for data_as_of |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E1-059. The tool names read_accounts, read_valuations and read_contact_points are agent operation names, not fields or entities of the Logical Data Model; the fields they return are the rows above. The agent tables are the P10 tables of schema `rwb_agent` in the Ownership Map; `recovery_case` is P3's, `document` is P5's, and the account, appraisal, contact-point and freshness rows are P1's. Every read of another service's data in this table goes through that service's contract and never through its table, and no field of agent_feedback, agent_alert, agent_policy or agent_prompt is written here (DP-01, DP-05).

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no operation of its own: the run is started by the CaseCreated event through the agent runtime contract of RWB-P10-TE013, the run read is `GET /api/recovery/agent/v1/agent-runs/{runId}` as fixed by RWB-P10-E1059-CON and baselined in RWB-P10-E1058-CON, and the sample and evaluation operations are baselined in RWB-P10-E1058-CON (ASM-0865). The base `/api/recovery/agent/v1` is the service's own and the legacy monolith base is retired for these paths (DP-13).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1, AC3 and AC4: the case facts the summary is built from, and the proof that no agent output is returned on the case read | One hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | AC1: the accounts of the case, masked before the model call | One hop, 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | AC1: the parties of the case, masked before the model call | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The reference lists the answer is validated against, in force at run time (DP-07) | One hop, 2 s |
| POST | the parameters resolve operation of the rwb-case contract — path Not specified in the source documents (GAP-0610; ASM-0865) | P3 rwb-case | The values of the policy and prompt versions in force, read at run time and never coded (DP-06) | One hop, 2 s |
| POST | the `read_accounts` tool read of the rwb-source-data contract — path Not specified in the source documents (GAP-0610; ASM-0866) | P1 rwb-source-data | AC1: the ACE account facts of the case (DP-05) | One hop, 2 s |
| POST | the `read_valuations` tool read of the rwb-source-data contract — path Not specified in the source documents (GAP-0610; ASM-0866) | P1 rwb-source-data | AC1: the appraisals and their dates (DP-05) | One hop, 2 s |
| POST | the `read_contact_points` tool read of the rwb-source-data contract — path Not specified in the source documents (GAP-0610; ASM-0866) | P1 rwb-source-data | AC1: the contact points and their usage codes (DP-05) | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The last complete business date, written to data_as_of (DP-05; ASM-0866). `status` `LOADED` / `STALE`; `businessDate` null with `STALE` when never stamped | One hop, 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | AC1: the documents of the case with their type and review status, for the MISSING_DOCUMENT flag | One hop, 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Rules and parameters right and the scope before a read, cached by the guard library | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent calls no service through another service and holds no schema client of another service. The three P3 contracts are the contract dependencies of the metadata row; the P1 reads add no dependency by DP-05, and the P5 read is a C-class contract built against its fake (ASM-0864). The model call is not a REST budget of this story: it is the INT-23 boundary of the agent platform of RWB-P10-E1058-APP with the 60 second policy timeout.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | runid, agent "INTAKE", caseid, fallback, outcome (the status of LOV-AGENT-RUN) |

One CloudEvents 1.0 message, inserted in the outbox in the same transaction as the run row and relayed by the outbox library; a payload is validated against its registry subject before the relay and a refusal goes to the `.dlt` topic with an alert (DP-09). No decision record is published by a shadow run (BR11). No personal value is carried: the payload holds IDs and facts only.

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use | Dedupe |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 | AC1, AC3, AC4 and AC6: one shadow run per new case, keyed by the case ID and the business date | Inbox on the event ID, then the run key "INTAKE:<caseId>:<businessDate>" |

The listener is idempotent on the event ID and on the run key, so a repeated event is counted and produces no second run (R-UNI-40; AC6). No other topic is consumed by this story.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | Input: agent code "INTAKE", case ID, business date, trigger "CaseCreated", idempotency key. One execution per key, with the 60 second policy budget and then the run status. Workflow ID form and duplicate-start policy: Not specified in the source documents (CG-ALL-2549) |
| BuildIntakeInputs | Activity | `rwb-agent` | Output: the masked input set, the inputs reference and data_as_of; no personal field leaves the activity |
| CallModelGateway | Activity | `rwb-agent` | Input: model code, masked inputs, output schema "intake-summary-v1", timeout. Output: the answer or the mapped status TIMED_OUT, MODEL_ERROR, TOOL_UNAVAILABLE |
| CheckGuardrail | Activity | `rwb-agent` | Input: the answer and the output schema reference. Output: the check code and the outcome, SCHEMA_RULE included |
| RecordShadowRun | Activity (workflow kit) | `rwb-agent` | Input: the run row and the outbox row; one `rwb_agent` transaction, no partial write |

The workflow name, the queue and the 60 second budget are those of Arch v5 slide 16; the activity names and their inputs and outputs are this story's and are accepted by RWB-P10-TE013-APP.

Start rule: the CaseCreated event starts one execution per run key "INTAKE:<caseId>:<businessDate>". The workflow ID form and the duplicate-start policy of AgentRunWorkflow: Not specified in the source documents (DOR-RWB-P10-E1059-APP-8).

#### 12.6 Schedules

None. The intake run is started by the CaseCreated event and the evaluation is started by RW-COE on request; the legacy Quartz entry of the evaluation does not exist in the target, and no Temporal Schedule is declared, changed or owned here.

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_run | P10 (rwb_agent) | One run of agent "INTAKE" per case and business date, with mode SHADOW, the summary and the gap flags in output, data_as_of and the status of LOV-AGENT-RUN |
| agent_sample | P10 (rwb_agent) | The labels of sample "INTAKE-S1", read at the comparison; loaded through the platform's sample operation |
| agent_evaluation_run | P10 (rwb_agent) | One evaluation of "INTAKE" against a sample version, RUNNING to DONE or FAILED, with the failure counts |
| agent_evaluation | P10 (rwb_agent) | One score row per gap type: sample_size, true_positive, false_positive, false_negative, agreement_rate, precision, recall |

rwb-agent reads no table of another service and holds no foreign key across services (DP-01). `recovery_case` is P3's, `document` is P5's and the account, appraisal, contact-point and freshness rows are P1's; all of them are read through their owners' operations. `V10_004__intake_run_key.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15; ASM-0867).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 contracts of RWB-P3-E1030-CON, RWB-P3-E1042-CON and RWB-P3-E1043-CON | The 200 Epic 1 cases created 2026-11-30 to 2026-12-04 with their CaseCreated events; case "RW-2026-000301" and case "RW-2026-000302"; the same event ID twice; the case reads that return no agent output; the lists and the policy values in force |
| rwb-source-data WireMock | The P1 tool and freshness contract | The account facts, the appraisals and their dates, the contact points and their usage codes of every case; freshness stamps with `status` `LOADED` and `STALE`, and a never-stamped answer (`businessDate` null, `status` `STALE`); a delay beyond 2 s |
| rwb-document WireMock | The P5 contract of RWB-P5-E1053-CON | The documents of a case with their type and review status; a case with no document; a delay beyond 2 s |
| rwb-access WireMock | The P4 contract | `POST /authorise` granting Rules and parameters C to RW-COE and R to RW-RISK, and refusing a role without the right |
| Model stub | The agent platform of RWB-P10-E1058-APP on the INT-23 boundary | A valid answer of "intake-summary-v1" with the four gap types; silence for 61 seconds for case "RW-2026-000302"; an answer with a missing member; an answer with a confidence under 0.80 |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the admin reads, one hop, with the query parameters preserved |

The agent model endpoint INT-23 is never called live by a test of this story: the answer is the stub of the agent platform owned by RWB-P10-E1058-APP, and no test calls a live model endpoint with real prompts. Every fixture is synthetic.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 0 provided, 10 consumed | The case, accounts and parties read, the list read and the parameter read of rwb-case; the three tool reads and the freshness read of rwb-source-data; the document read of rwb-document; the authorise call of rwb-access; one hop, 2 s each |
| Kafka | 1 published, 1 consumed | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` through the outbox, and `rwb.case.CaseCreated.v1` on `rwb.case.events.v1` through the inbox |
| Temporal | 1 workflow, 4 activities | AgentRunWorkflow with BuildIntakeInputs, CallModelGateway, CheckGuardrail and RecordShadowRun on the queue `rwb-agent` |
| File | None | No file is read or written; the sample is loaded through the platform's sample operation and the scores leave in the body of the evaluation read |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.intake`, module `intake`, Java package `th.co.scb.ace.workbench.recovery.agent.intake` inside the rwb-agent service (DP-13, §R4).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The H and C dependencies of this table are the ones in the metadata rows: the five platform contracts, RWB-PLT-N001-CON, RWB-P10-E1059-CON, RWB-P10-TE013-CON, RWB-P10-E1058-APP and RWB-P10-TE013-APP are build dependencies; the three P3 contracts and RWB-P10-TE013-CON are contract dependencies built against their fakes. DP-05 adds no dependency of its own, DP-11 sits behind DP-01 on every read (one hop, 2 s), and DP-03 is carried by the platform's run record only: a shadow run writes no decision record (BR11).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| IntakeShadowListener | Listener | Consumes `rwb.case.CaseCreated.v1` through the inbox, applies the run key and calls the agent runtime of RWB-P10-TE013 (DP-09, DP-20) |
| IntakeInputAssembler | Service | Builds the masked input set from the case, account, document, appraisal and contact-point reads and records data_as_of from the owner's freshness stamp |
| IntakeOutputGuardrail | Service | Applies the schema, the allowed tools and the floor of the policy version in force, writes guardrail_result and maps a failure to GUARDRAIL_FAILED or BELOW_FLOOR |
| IntakeOutputScorer | Service | Compares each gap flag with the label per gap type for the evaluation harness and writes the score rows (BR5) |
| intake-summary-v1.json | Rule table | The output schema with the gap type enum, versioned with the policy and read as a version, never coded |
| prompt INTAKE PR1 | Rule table | The prompt text, loaded through the configuration operation of RWB-P10-E1058-APP and approved by RW-RISK |
| CaseContractClient | Client | Calls the rwb-case reads and the parameter and list reads with one hop and the 2 s budget (DP-06, DP-07, DP-11) |
| SourceDataToolClient | Client | Calls the three tool reads and the freshness read of rwb-source-data as SY-AGENT (DP-05) |
| DocumentContractClient | Client | Calls the document read of rwb-document as SY-AGENT (DP-11) |
| AgentRunRepository | Repository | Writes and reads agent_run, agent_sample, agent_evaluation_run and agent_evaluation in `rwb_agent` only (DP-01) |

**Database and migrations**

- `V10_004__intake_run_key.sql` adds the index `ux_agent_run_intake_key ON agent_run (agent_code, idempotency_key)` in `rwb_agent`, so the repeat check of AC3 and AC6 is answered without a scan; it runs in the rwb-agent Flyway sequence after the earlier P10 migrations and touches no other schema (DP-15; ASM-0867).
- The four run tables are created in `rwb_agent` by the P10 migrations of RWB-P10-E1058-APP; this story creates no table outside its four and no foreign key across services (DP-01; BR10).

**Configuration and reference data**

- Policy version "P1" of agent "INTAKE" (mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_accounts, read_documents, read_valuations, read_contact_points, output schema "intake-summary-v1") and prompt version "PR1": loaded by RW-COE, approved by RW-RISK, read at run time through the parameters contract and the configuration read (DP-06).
- The gap type enum MISSING_DOCUMENT, NO_VALID_APPRAISAL, NO_CONTACT_POINT and STALE_INPUT is a value of the output schema version, not a constant of the source (BR3).
- Sample "INTAKE-S1" version 1 and version 2, loaded by RW-COE from the business analysts' review file through the platform's sample operation.
- The list codes read through the reference-data contract, the 2 s client budget and the token set of the mask as service configuration.
- The legacy feature flag `rwb.agent.intake-shadow` is kept as the legacy reference: off, the listener ignores CaseCreated and no run row is written.

**Build steps**

1. `V10_004__intake_run_key.sql` and the four repositories in `rwb_agent` (BR10).
2. CaseContractClient, SourceDataToolClient and DocumentContractClient against their fakes, with the 2 s budget, the SY-AGENT identity and the tool-unavailable path (AC1; X8).
3. IntakeShadowListener with the inbox dedupe and the run key, then the call to the agent runtime contract (AC3, AC6).
4. IntakeInputAssembler with the mask and a scan proving that no personal field reaches the request (AC1; BR7).
5. IntakeOutputGuardrail with the schema, tool and floor checks and the failure counts (AC4).
6. IntakeOutputScorer with a 10-case fixture of known counts, then the full 200-case sample (AC2, AC7).
7. The empty-sample refusal on the evaluation start (AC8).
8. Pipeline scans for another service's table name, for a cross-schema foreign key and for the values 60, 0.80 and the gap type names in the source (BR8, BR9).
9. gateway-bff route contract test in front of the admin reads (DP-19).

**Done when.** The nine test cases of section 16 pass, a DEV run over the 200 synthetic cases produces 200 runs in mode SHADOW and one complete evaluation with sample size 200, the migration applies cleanly on an empty `rwb_agent` schema, no policy value appears in the source, and no case field, task, queue or decision log entry has changed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-002 | Evaluation started on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |
| MSG-P1-001 | Data product stale after a late or failed load | {product} is from {date}. Today's load has not arrived. |

The three business messages MSG-P10-002, MSG-P10-003 and MSG-P4-002 are copied unchanged from RWB-E1-059; MSG-P1-001 is the freshness message of the data products, named by the legacy rule BR4 and carried by rwb-source-data (VR-P10-003-1). This story adds no message ID. Thai text for each message follows decision DL10, which stays open on the confirmed assumptions ASM-2250, ASM-2357, ASM-2377 and ASM-2863. In AC8 the {sample} value is "INTAKE-S3" and the {agent} value is "INTAKE"; in the access test the {action} value is "load a sample, start an evaluation or read the scores".

### 15. Screens and states

No screen in this story. No case owner sees the output. RW-COE reads scores through `GET /api/recovery/agent/v1/admin/agent-evaluations` and run metadata shows through `GET /api/recovery/agent/v1/admin/agent-runs`, both reached through the gateway-bff route in front of the admin path, so a screen never calls rwb-agent directly (DP-19). The agent monitor screen SCR-46 - the screen that shows runs, fallback, latency and cost per agent and comes with RWB-E2-031 - is not changed by this story, and the case screens, the review queue and the document screens belong to other stories and are out of scope. The empty, loading, error and no access states of SCR-46 are Not specified in the source documents (CG-ALL-2560). The exact path of the gateway-bff route in front of the admin reads is Not specified in the source documents (GAP-0610; ASM-0868).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-059-01 | AC1, BR1, BR11 | Component | 200 synthetic cases created 2026-11-30 to 2026-12-04; 200 runs in mode SHADOW and no change on any case read |
| TC-E1-059-02 | AC2, BR3, BR5 | Component | Sample INTAKE-S1 version 1, 182 agreeing cases for MISSING_DOCUMENT; agreement rate 0.9100 at four decimals |
| TC-E1-059-03 | AC3, BR2 | Component | Case RW-2026-000301 created 2026-11-30; one run with the key "INTAKE:<caseId>:2026-11-30", trigger "CaseCreated" and mode "SHADOW" |
| TC-E1-059-04 | AC4, BR6 | Component | Model stub silent for case RW-2026-000302; status TIMED_OUT, fallback true, failure count TIMED_OUT 1 and no second run |
| TC-E1-059-05 | AC5 (run by RWB-ITG-E1059-ITG), BR4 | Component | COMPLETED ALS row of 2026-11-28, business date 2026-11-30; carried with its legacy data only, because its criterion AC5 is owned by RWB-ITG-E1059-ITG (GAP-0610) |
| TC-E1-059-06 | AC6, BR2 | Component | The same CaseCreated event ID twice; one run for the case and date and the repeat counted |
| TC-E1-059-07 | AC7, BR5 | Component | Sample INTAKE-S1 version 2, 180 of 200 labeled; sample size 180 and the 20 unlabeled cases listed |
| TC-E1-059-08 | AC8 | Component | Sample INTAKE-S3 with no rows; 422 and MSG-P10-002 |
| TC-E1-059-09 | AC13, Access | Contract | RW-CASEOWN calls POST /admin/agent-evaluations; refused with 403 and MSG-P4-002 |
| TC-E1-059-10 | Not specified in the source documents (DOR-RWB-P10-E1059-APP-4) | Component | Boundary test of the four tables of section 12.7 (agent_run, agent_sample, agent_evaluation_run, agent_evaluation) |
| TC-E1-059-11 | AC9, BR9 | Component | rwb-source-data stub silent beyond the 2 s budget for case RW-2026-000301; status TOOL_UNAVAILABLE, fallback true, no stored answer |
| TC-E1-059-12 | AC10, BR8 | Component | Policy P1 with the timeout value removed; no model call, status DISABLED or fails closed, the missing value named on the run |
| TC-E1-059-13 | AC11, BR7 | Component | Topic rwb.agent.events.v1 unreachable; run row stands and the event waits in the outbox |
| TC-E1-059-14 | AC12, BR10 | Component | Migration V10_004__intake_run_key.sql fails; version in force keeps serving and no run row is written by the new build |
| TC-E1-059-15 | AC14; BR3, BR7, BR8, BR9, BR10, BR11 | Component | Boundary check: gap types, policy values, personal fields, reads and written tables follow the rules; no code default is used and no other service table is read |
| TC-E1-059-16 | AC15 | Component | Not specified in the source documents (NEWAC-RWB-P10-E1059-APP-AC15) |

TC-E1-059-01 to TC-E1-059-09 are the nine legacy test cases of RWB-E1-059, kept with their legacy IDs and their legacy data and in the legacy order of section 16; the legacy System level maps to Component and the legacy Access level of TC-E1-059-09 maps to Contract. TC-E1-059-05 is kept because it is one of the nine test cases of the key and its ID is carried in the register; its criterion AC5 is owned by RWB-ITG-E1059-ITG and the row is not a test this story builds. The cross-service behaviour of the key is proved by the integration copy and its `-ITG` cases, not here. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the gap types, the prompt, the timeout 60 seconds, the confidence floor 0.80, the allowed tools and the output schema are versioned rows read at run time, and a missing value stops the call instead of falling back to a default (BR8).
- No personal data in logs, tests, prompts or events: the inputs are masked with tokens before the model call, the summary holds masking tokens only, the event payload holds IDs and facts, and no test uses a real account number, name or national ID (BR7, legacy section 17).
- Data Classification and Personal Data Inventory v5 classes `agent_run.agent_version`, `agent_run.model_version`, `agent_run.status` and `agent_run.confidence` as Not personal and Internal; of these, the event carries only the status, as outcome.
- No read of another service's tables and no schema client: the case, the parties and the accounts come through the rwb-case contracts, the ACE facts and the freshness stamp through rwb-source-data, the documents through rwb-document and the right through rwb-access (DP-01, DP-05, DP-11).
- The four tables agent_run, agent_sample, agent_evaluation_run and agent_evaluation are the only tables this story writes, all in `rwb_agent`, and the run key index arrives only by `V10_004__intake_run_key.sql` (BR10, DP-15).
- The run is in shadow and changes nothing in force: it writes no case field, no task, no queue, no threshold and no decision record, and no user-facing endpoint returns its output (BR1, BR11).
- One hop and a 2 s client budget on every consumed REST call; the model budget belongs to the agent platform and is never a REST budget of this story (DP-11, ADR-020).
- The admin reads are reached through the gateway-bff route and never from a screen to the service (DP-19).
- Every payload is validated against its registry subject before the relay and a refusal is routed to `.dlt` with an alert (DP-09).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-ACA-005 | Personal data masked in every agent call | Business Requirements Program, section 5.4 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-01 |
| REQ-ACA-010 | Agents run under service identities with role checks | Business Requirements Program, section 5.4 | FEAT-AGT-03 | 06 Take over and own the case | R-UNI-32, R-UNI-40 | TC-E1-059-02, TC-E1-059-03, TC-E1-059-04, TC-E1-059-05, TC-E1-059-06, TC-E1-059-07, TC-E1-059-08, TC-E1-059-09 |
| D-RCV-60 DP-01 | The four run tables are owned by rwb-agent in schema `rwb_agent`, and the case, the documents and the ACE facts are read only through their owners' contracts | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-01, TC-E1-059-03 |
| D-RCV-60 DP-05 | The ACE account, appraisal, contact-point and freshness facts are read through the rwb-source-data contract | Template and Rules §R5.5; ADR-010 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-01 |
| D-RCV-60 DP-06 | The timeout, the floor, the allowed tools and the parameter values in force are read at run time and never coded | Template and Rules §R5.5 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-04 |
| D-RCV-60 DP-09 | The run completion is one CloudEvents message on `rwb.agent.events.v1` through the outbox, and CaseCreated is consumed through the inbox | Template and Rules §R5.5; ADR-015 | FEAT-AGT-03 | 06 Take over and own the case | R-UNI-40 | TC-E1-059-06, TC-E1-059-01 |
| D-RCV-60 DP-13 | The admin operations are served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-02, TC-E1-059-08 |
| D-RCV-60 DP-15 | The run key index arrives with the service's own migration in its own Flyway sequence | Template and Rules §R5.5; ADR-021 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-03, TC-E1-059-06 |
| D-RCV-60 DP-19 | The admin reads are reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-03 | 06 Take over and own the case | None | TC-E1-059-02 |
| D-RCV-60 DP-20 | The run is started and read through the agent runtime contract of RWB-P10-TE013 | Template and Rules §R5.5 | FEAT-AGT-03 | 06 Take over and own the case | R-UNI-32 | TC-E1-059-03, TC-E1-059-04 |
| RWB-E1-059 (legacy story) | Case intake agent in shadow [E1b]: the seven criteria AC1, AC2, AC3, AC4, AC6, AC7 and AC8 and the access test | Business Requirements Epic 1, section 3.9 | FEAT-AGT-03 | 06 Take over and own the case | None | The nine legacy test cases of section 16 |
| RWB-ITG-W1J01-ITG (harness) | The same behaviour proved across rwb-case, rwb-source-data, rwb-document and rwb-agent on the real services, with the `-ITG` test cases | Business Requirements Epic 1, section 3.9 | FEAT-AGT-03 | 06 Take over and own the case | None | The test cases of that story |

The gap GAP-0610 records the areas the sources leave open for this story - the service login, the route path in front of the reads, the placement of the legacy criterion AC5 and the P5 contract in the dependency row - and each default it raises is settled by ASM-0861 to ASM-0868.

### 19. Out of scope

- The legacy criterion AC5 and the stale-input check it asserts: owned by RWB-ITG-E1059-ITG, not owned by this story and not reconstructed here (GAP-0610).
- The cross-service behaviour of this key: the integration copy and the harness RWB-ITG-W1J01-ITG.
- The agent platform, the model gateway client, the prompt and policy store, the sample load and the evaluation operations of RWB-P10-E1058-APP, and the agent runtime client with fallback of RWB-P10-TE013.
- The evaluation report and the L1 proposal (RWB-E1-061).
- Showing the summary to the case owner (RWB-E2-028, Epic 3).
- Document classification and field extraction (RWB-E1-053, RWB-E1-060).
- The case creation and allocation in rwb-case (RWB-P3-E1030-CON), the ACE views and data products of rwb-source-data, the document store of rwb-document and the rights of rwb-access.
- The agent monitor screen SCR-46 and its dashboard (RWB-E2-031).
- The contract slice of this key (RWB-P10-E1059-CON), and the database, infrastructure and operations stories of the service: chart values, topic and queue provisioning, dashboards and the runbook.
