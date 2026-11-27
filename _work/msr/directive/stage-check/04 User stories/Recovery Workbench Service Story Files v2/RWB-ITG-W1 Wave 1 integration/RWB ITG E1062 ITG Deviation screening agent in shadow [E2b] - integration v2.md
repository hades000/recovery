# RWB-ITG-E1062-ITG Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-E1062-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-062 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-E1062-ITG-16); the squad sizes it at refinement |
| Patterns applied | DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | Document read through the rwb-document (P5) contract; call-note read as a field of the rwb-source-data (P1) contract |
| Integration dependencies | RWB-P10-E1062-APP, RWB-S8-E1062-APP, RWB-P5-E1062-APP, RWB-P4-E1062-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to REQ-DVH-001, REQ-DVH-003, REQ-DVH-007) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-E1-062 for RWB-ITG-W1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 22 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **QA integration engineer** proving the deviation screening agent in shadow end to end on the real SIT services of the plan's integration list - rwb-agent (P10), rwb-deviation (S8), rwb-document (P5) and rwb-access (P4), with rwb-case (P3), rwb-decision (P7) and rwb-source-data (P1) as wave-1 published-contract preconditions - I want **one suite that runs the legacy screening agent over a 200-case sample and the four synthetic exception cases through the events, the tool reads, the rule package, the masking and the evaluation**, so that **the shadow behaviour, the precision and recall per deviation code, the owner role from the rule package in force, the preceding contact of a complaint, the refusal paths and the proof that nothing is raised are established on real services before wave 1 exits**.

### 2. Business rationale

A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. RWB-E1-062 put a screening agent in front of that risk and kept it in shadow: it reads the case, the interaction ledger and the documents at entry and when a document arrives, proposes a code X1 to X7 with its reasons and source references, and stores everything without raising a deviation, pausing a clock or stopping contact. The legacy story measured detection from case data, call notes and documents (REQ-DVH-001), the named owner each code would route to (REQ-DVH-003) and the contact that preceded a complaint (REQ-DVH-007). All of that lived in one module.

In the target the same behaviour is delivered by four services and proved across them. The run is a workflow of rwb-agent (P10) started by EV-01 CaseCreated from rwb-case and EV-16 DocumentStored from rwb-document; it reads the case, the ledger entries and the documents through the published contracts of their owners, masks personal values through rwb-access, evaluates the DEVIATIONS rule package with the embedded Drools kit, checks the answer against the code list of the reference-data contract and records one run row and one `rwb.agent.AgentRunCompleted.v1`. The deviation service (S8) is present in the environment and is never called, because shadow raises nothing.

The component copy is RWB-P10-E1062-APP, which builds the listener, the input assembler, the owner resolver, the rule checks and the scorer inside rwb-agent and unit-tests them against the published contracts of its neighbours. This integration story exists because the facts that make the shadow measure trustworthy cannot be proved inside one service: a run that is started by two different events on two different topics, an owner role that comes from a rule package version in force in rwb-decision, a preceding contact that comes from a ledger read in rwb-source-data, a code list that comes from rwb-case, masking tokens that come from rwb-access, and an absence - no deviation, no contact stop, no clock pause - that can only be proved by reading the case back, watching a topic and watching what was never called.

The legacy story took the ledger through a P7 `InteractionLedgerReader`, the owner role through a P3 `RuleCatalog` and `RuleEvaluator.ownerFor`, and the absence of a deviation by reading a deviation record. None of the three is a call a service may make in the target: the ledger is P1 under DP-18, the rule rows are P7 under DP-04, and S8 publishes no read operation, so the absence is proved on three observable facts instead (GAP-0371). The suite therefore carries no legacy criterion: every criterion of this story is new (D-RCV-60), written to prove the deliverable in the title on real services, and it keeps the legacy values of RWB-E1-062 - agent "SCREENING", policy "P1", prompt "PR1", mode SHADOW, timeout 60 seconds, confidence floor 0.80, output schema "screening-v1", codes X1 to X7 of LOV-DEVIATION, sample "SCREEN-S1" version 1 with 200 cases, the 30-day look-back and the 180-day ledger window - so that a reader can follow the legacy story beside it.

The only thing that is faked is the outside world: the enterprise model endpoint INT-23 is reached through a recorded stub of its OpenAPI 3.1 contract, because no suite may call a live model endpoint with real prompts and because a schema fault, a 61 second silence and a deterministic answer set are needed to reach the exception paths every run. P1, P3, P4, P5, P7, P10 and S8 are the real services on their published SIT contracts, and a run that needs a fake for any of them fails the preflight, because a fake would defeat the purpose of the run. The measures the story is read against are the legacy ones: one score row per code with precision, recall and sample size 200, and the count of proposals under review.

### 3. Preconditions

- RWB-P10-E1062-APP is done: rwb-agent (P10) is deployed with the screening listener, the input assembler, the owner resolver, the rule checks, the scorer, output schema "screening-v1" and the admin operations of section 12.2, and it runs AgentRunWorkflow on queue `rwb-agent`.
- RWB-S8-E1062-APP is done: rwb-deviation (S8) is deployed, its topic `rwb.deviation.events.v1` exists with its retry and `.dlt` topics, and its POST and PATCH operations are published and idle for this run.
- RWB-P5-E1062-APP is done: rwb-document (P5) serves the document list and the single document read of section 12.2 and writes EV-16 DocumentStored.
- RWB-P4-E1062-APP is done: rwb-access (P4) serves the session read, the authorise contract and the masking tokens of section 12.2.
- The wave-1 published contracts the run needs are preconditions, not integration dependencies: P3 rwb-case (case read and reference data), P7 rwb-decision (rule package registry) and P1 rwb-source-data (interaction ledger) are deployed and their operations of section 12.2 answer in SIT.
- Agent policy "SCREENING" version "P1" is approved: mode SHADOW, timeout 60 seconds, confidence floor 0.80, output schema "screening-v1" with codes from LOV-DEVIATION, and prompt "SCREENING" version "PR1" is approved.
- Rule rows R-DEV-02 to R-DEV-06 are in the DEVIATIONS package in force in P7, with R-DEV-04 naming owner role RW-FRAUD for X4 (ASM-0520).
- The reference list LOV-DEVIATION of P3 holds X1 to X7 and its version in force is readable (ASM-0521).
- Labeled sample "SCREEN-S1" version 1 exists: the business analysts' review of 200 cases of Epic 1, one row per case and code with expected value Y or N.
- No deviation, screening or queue volume is stated for this module (GAP-1833): the platform figures are NFR-001 (23,600 open cases at go-live, 3,110 new a month), NFR-002 (about 370 staff online of 914) and NFR-011 (300 milliseconds per rule evaluation), and the agent evaluation samples are 200 and 500 cases; no module volume is asserted.
- The interaction ledger of P1 answers for the synthetic cases with the 180-day window and a masked summary, and the 30-day look-back of X1 is held in the policy (ASM-0519).
- The INT-23 model stub is deployed with its OpenAPI 3.1 document, its deterministic answer set for the 200-case run, its schema fault (code X9), its 61 second silence and its confidence 0.72 answer.
- The harness RWB-ITG-W1J01-ITG is available with the synthetic case and document set, the synthetic identities, and the topic, queue and namespace wiring of wave 1.
- The SIT environment is available with Temporal namespace `rwb-recovery`, queue `rwb-agent`, the topics `rwb.case.events.v1`, `rwb.document.events.v1`, `rwb.agent.events.v1` and `rwb.deviation.events.v1`, and the schema registry.
- No production data is read, copied or connected to; every case number, borrower, national ID number, mobile number, name, account number and identity used by the run is synthetic.
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. QA integration engineer: runs the preflight, which reads the OpenAPI documents of P1, P3, P4, P5, P7, P10 and S8 and the AsyncAPI documents of the four topics, and fails before any assertion if a path, a field, a status code or an event schema has drifted; it also confirms that no fake is configured for any service and that a schema connection does not exist in the suite.
2. Harness: reads agent policy "SCREENING" version "P1" and prompt version "PR1" through `GET /api/recovery/agent/v1/admin/agent-configs` and asserts mode SHADOW, timeout 60 seconds, confidence floor 0.80 and output schema "screening-v1" (AC15).
3. Harness: reads the DEVIATIONS package version in force through `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` and the code list LOV-DEVIATION through `GET /api/recovery/case/v1/admin/lists/{listCode}`; it records the two versions against the run and asserts that neither the suite nor P10 holds a code or an owner role in code (AC4, AC11).
4. Harness: seeds the four synthetic cases RW-2026-000401, RW-2026-000402, RW-2026-000403 and RW-2026-000404 with their call notes and documents through the W1J01 set, including document D-1001 of type DEATH_CERTIFICATE on case RW-2026-000401 and, on case RW-2026-000403, an outbound call on 2026-11-25 and a complaint note on 2026-11-27 inside the 180-day ledger window (AC3, AC5, AC10).
5. Harness: publishes the 200 cases of the sample as EV-01 CaseCreated and their documents as EV-16 DocumentStored, and asserts that each event enters the P10 inbox and starts AgentRunWorkflow on queue `rwb-agent` with key "SCREENING:<caseId>:<eventId>" and the trigger of its event (AC3, AC15).
6. Harness: asserts that each run of the 200 cases stores its proposed codes with reasons, source references and confidence in mode "SHADOW", and that no proposal appears on any user-facing endpoint (AC1).
7. Harness: reads the interactions of case RW-2026-000403 through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` with the 180-day window, asserts the masked summary in the captured model request, and asserts that P10 made no call to a P7 ledger reader and read no interaction table (AC10).
8. Harness: asserts the owner role on each stored proposal against the DEVIATIONS package version in force - X4 with owner role RW-FRAUD from R-DEV-04 - and the owner role RW-TEAMMGR with marker "unmapped" for a code with no owner row (AC4).
9. Harness: asserts that the X1 proposal on case RW-2026-000403 names the interaction of 2026-11-25 as the preceding contact inside the 30-day look-back, and that an X1 proposal without a preceding contact, while one exists in that window, fails check "SCHEMA_RULE" (AC5).
10. Harness: asserts that the X2 proposal with confidence 0.72 is stored with marker "review" and is counted under review and not in precision or recall (AC6).
11. Harness: replays EV-16 for document D-1001 on case RW-2026-000401 with the same event ID and asserts one run for the case and event, with the repeat counted (R-UNI-40) (AC7).
12. Harness: loads labeled sample "SCREEN-S1" version 1 with 200 labeled cases through `POST /api/recovery/agent/v1/admin/agent-samples`, starts the evaluation through `POST /api/recovery/agent/v1/admin/agent-evaluations`, polls `GET /api/recovery/agent/v1/admin/agent-evaluations` to status "DONE", and reads the score rows: one row per code X1 to X7 with precision, recall and sample size 200, X6 holding 0.9000 and 0.7500 (AC2, AC6).
13. Harness, exception paths: switches the INT-23 stub to the schema fault (code X9) and to the 61 second silence in turn, and asserts GUARDRAIL_FAILED with check "SCHEMA" and fallback true, and TIMED_OUT for case RW-2026-000404 with no retry for that event (AC8, AC9).
14. Harness, absence: reads case RW-2026-000401 back through `GET /api/recovery/case/v1/cases/{caseId}` and asserts deviation_open false; consumes `rwb.deviation.events.v1` for the whole run window and asserts that no `rwb.deviation.DeviationRaised.v1` appears; and asserts from the S8 request log of the gateway that the POST and PATCH operations were never called (AC1, AC12).
15. Harness, masking and refusals: seeds the synthetic national ID number, phone number, name and account number on case RW-2026-000403, captures the model request at the stub, and scans the request body, the run row, `rwb.agent.AgentRunCompleted.v1` and the application log; then calls `GET /api/recovery/agent/v1/admin/agent-evaluations` as synthetic user RW-CASEOWN, confirms its rights on `GET /api/recovery/access/v1/me/session`, and asserts 403 with MSG-P4-002 (AC13, AC14).
16. Harness: asserts that no service reached P10 by REST during the run, cleans up the synthetic cases, the sample, the evaluation run and the stub deployment, and writes the evidence report with one verdict per test case (AC15).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer has a code outside X1 to X7 | Check SCHEMA fails; run GUARDRAIL_FAILED; fallback true; nothing is proposed | None to a user | AC8 |
| X2 | A proposal is below the confidence floor 0.80 | Stored with marker "review"; counted under review and scored separately | None to a user | AC6 |
| X3 | An X1 proposal names no preceding contact while the ledger holds one in the 30 days before | Check SCHEMA_RULE fails for that proposal | None to a user | AC5 |
| X4 | The same event arrives twice | One run per case and event (R-UNI-40), the repeat counted | None to a user | AC7 |
| X5 | A proposed code has no owner row in R-DEV-02 to R-DEV-06 | Owner role stored as RW-TEAMMGR and the proposal marked "unmapped" | None to a user | AC4 |
| X6 | The agent times out at 60 seconds | Run TIMED_OUT, counted, not retried for that event | None to a user | AC9 |
| X7 | A role without Rules and parameters R calls the evaluation read | Refused with 403, nothing changes | MSG-P4-002 | AC13 |
| X8 | A shadow run calls an S8 operation or publishes a deviation event | The run fails: shadow raises nothing, so a call to S8 is a defect and not a behaviour | None | AC12 |
| X9 | A consumed contract drifts from the published one (path, field, status or event schema) | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |
| X10 | A fake is configured for P1, P3, P4, P5, P7, P10 or S8 | The preflight refuses the run: only INT-23, the clock and the fixture set may stand outside the services | None | AC16 |
| X11 | The INT-23 stub drifts from its OpenAPI 3.1 document | The preflight fails on the stub contract test, so no assertion is made against an endpoint that no longer matches | None | AC8, AC9 |
| X12 | The W1J01 synthetic set, the sample or an identity it carries is missing or does not match the run | The run fails as a fixture fault and names the missing element; no production value is substituted | None | AC1, AC3, AC13 |
| X13 | A suite step tries to read a service schema directly | The step does not exist: the suite is built with no client for a service schema, and the pipeline scan fails any change that adds one | None | AC17 |
| X14 | A code of the reference list LOV-DEVIATION is missing, or the list version cannot be read | The run fails the schema check with the code-list version named, and no proposal is accepted against an unread list | None | AC11 |
| X15 | The DEVIATIONS package in force cannot be read, or its version does not match the rules the run used | The run stops before the first proposal and names the package version it expected | None | AC4, AC11 |
| X16 | A proposal is exposed on a user-facing endpoint | The suite fails AC1: no case owner or handler may see a proposal in shadow | None | AC1 |

X1 to X7 are the legacy exception paths of RWB-E1-062 carried onto the real services; X8 to X16 are the failures that only appear when the run leaves one service.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The suite is a module of its own and reuses the harness RWB-ITG-W1J01-ITG; it needs the four integration dependencies and the published contracts of P1, P3, P4, P5, P7, P10 and S8, not their source code, and it owns no schema, no table and no operation |
| Negotiable | The fixture composition, the poll interval, the report layout and the stub control names are configuration; the agent, the policy and prompt versions, the mode, the timeout, the floor, the code list, the owner roles, the sample and the cases are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: an event-started run on two topics, a ledger read and a masking boundary, an owner role from the package in force, a code list from its owner, precision and recall per code, a repeated event, and an absence proved on three facts |
| Estimable | One suite module, one stub control, one fixture builder, seven contract probes, one evaluation driver, one absence probe and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a REST response, a Kafka event, a run row read through the contract, a score row, a captured model request, a log scan or a request log of the gateway |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent in shadow [E2b], proven across the wave 1 services

  Background:
    Given agent "SCREENING" has approved policy "P1" with mode "SHADOW", timeout 60 seconds, confidence floor 0.80 and prompt "PR1"
    Given rule rows R-DEV-02 to R-DEV-06 are in force in the DEVIATIONS package of rwb-decision
    Given the codes X1 to X7 are in force in reference list "LOV-DEVIATION"
    Given all involved services are deployed in SIT with their published contracts and SY-AGENT holds Case record R, Documents R, Rules and parameters R, Reference data R and Decision log C
    Given the RWB-ITG-W1J01-ITG synthetic set is loaded and no production value is used

  Scenario: AC1 Shadow flags raise no deviation and set no contact stop (new, D-RCV-60)
    Given 200 cases with their call notes and documents
    When the agent runs for each of the 200 cases
    Then each run stores its proposed codes with reasons and source references in mode "SHADOW"
    Then no deviation record exists, deviation_open stays false on every case and no contact stop is set
    Then no user-facing endpoint returns a proposal

  Scenario: AC2 Precision and recall per code on the 200-case sample (new, D-RCV-60)
    Given the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1
    When the comparison runs
    Then one score row per code X1 to X7 holds precision, recall and sample size 200
    Then for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500

  Scenario: AC3 A new document starts a shadow run (new, D-RCV-60)
    Given open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE"
    When EV-16 DocumentStored is processed
    Then one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored"

  Scenario: AC4 The owner role comes from the rule package in force (new, D-RCV-60)
    Given the agent proposes X4 for case "RW-2026-000402"
    When the proposal is stored
    Then it holds owner role "RW-FRAUD" from rule R-DEV-04 read from the DEVIATIONS package in force
    Then a proposed code with no owner row is stored with owner role "RW-TEAMMGR" and marker "unmapped"

  Scenario: AC5 A complaint names the contact before it (new, D-RCV-60)
    Given case "RW-2026-000403" has an outbound call on 2026-11-25 and a complaint note on 2026-11-27
    When the agent proposes X1
    Then the proposal names the interaction of 2026-11-25 as the preceding contact
    Then an X1 proposal without a preceding contact, when one exists in the 30 days before, fails check "SCHEMA_RULE"

  Scenario: AC6 A low-confidence proposal is marked for review (new, D-RCV-60)
    Given the agent proposes X2 with confidence 0.72
    When the proposal is stored
    Then it holds marker "review"
    Then the evaluation counts it under "review" and not in precision or recall

  Scenario: AC7 A repeated event has no further effect (new, D-RCV-60)
    Given EV-16 for document "D-1001" on case "RW-2026-000401" was processed
    When the same event ID arrives again
    Then one run exists for the case and event and the repeat is counted (R-UNI-40)

  Scenario: AC8 A code outside the list fails the schema check (new, D-RCV-60)
    Given the model stub returns code "X9"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED", check "SCHEMA" and fallback true

  Scenario: AC9 A timeout ends the run and is not retried (new, D-RCV-60)
    Given the model stub does not answer for 61 seconds
    When the agent runs for case "RW-2026-000404"
    Then the run holds status "TIMED_OUT" and is not retried for that event

  Scenario: AC10 The ledger is read through P1 with a masked summary (new, D-RCV-60)
    Given case "RW-2026-000403" has interactions inside the 180-day ledger window
    When P10 assembles the input of the run
    Then P10 reads the interactions through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` with the 180-day window
    Then the summary of each interaction is masked before the model call
    Then P10 calls no P7 ledger reader and reads no interaction table

  Scenario: AC11 The codes come from the reference-data contract (new, D-RCV-60)
    Given the codes X1 to X7 are in force in reference list "LOV-DEVIATION"
    When the run is prepared
    Then the codes are read through `GET /api/recovery/case/v1/admin/lists/{listCode}` and the run records the code-list version in force
    Then no code is written in P10 or in the suite

  Scenario: AC12 The absence of a deviation is proved on three facts (new, D-RCV-60)
    Given a shadow run ended for case "RW-2026-000401"
    When the absence of a deviation is proved
    Then `GET /api/recovery/case/v1/cases/{caseId}` returns deviation_open false
    Then no `rwb.deviation.DeviationRaised.v1` appears on `rwb.deviation.events.v1`
    Then the S8 POST and PATCH operations were never called

  Scenario: AC13 A role without the right is refused (new, D-RCV-60)
    Given synthetic user "RW-CASEOWN" holds no Rules and parameters R and the suite confirms it on `GET /api/recovery/access/v1/me/session`
    When "RW-CASEOWN" calls `GET /api/recovery/agent/v1/admin/agent-evaluations`
    Then the call is refused with 403 and MSG-P4-002
    Then no evaluation run and no score row is created

  Scenario: AC14 No personal value in the request, the run, the event or the log (new, D-RCV-60)
    Given case "RW-2026-000403" carries a synthetic national ID number, phone number, name and account number on its call notes and documents
    When the run is executed and its artefacts are scanned
    Then the request body holds the masking tokens returned by P4
    Then the request body, the run row, `rwb.agent.AgentRunCompleted.v1` and the application log hold no national ID number, phone number, name or account number

  Scenario: AC15 The run is AgentRunWorkflow on rwb-agent, started by the events (new, D-RCV-60)
    Given EV-01 CaseCreated on `rwb.case.events.v1` and EV-16 DocumentStored on `rwb.document.events.v1` are delivered
    When P10 processes them
    Then each event enters the inbox of P10 once and starts one AgentRunWorkflow on queue "rwb-agent" in namespace "rwb-recovery"
    Then the run names policy "P1" and prompt "PR1"
    Then the number of REST calls to P10 by any service is 0

  Scenario: AC16 A fake for a service refuses the run (new, D-RCV-60)
    Given a fake is configured for one of P1, P3, P4, P5, P7, P10 or S8
    When the preflight runs
    Then the preflight refuses the run
    Then only INT-23, the clock and the fixture set may stand outside the services

  Scenario: AC17 A suite step cannot read a service schema directly (new, D-RCV-60)
    Given a suite step that reads a service schema directly is added
    When the pipeline scan runs
    Then the pipeline scan fails the change and the suite holds no client for a service schema

  Scenario: AC18 A run outside SIT is refused and no production value is read (new, D-RCV-60)
    Given the suite is started outside SIT
    When the preflight runs
    Then the suite refuses to start
    Then no production value is read, copied or connected to and every case, identity and personal value of the run is synthetic
```

**Target reading.** The agent, its policy and prompt versions, the mode, the timeout, the confidence floor, the output schema, the codes, the sample, the four cases and the 30-day and 180-day windows are the legacy values of RWB-E1-062, copied character for character. The run is AgentRunWorkflow on queue `rwb-agent` (DP-20), started by EV-01 and EV-16 through the inbox (DP-09); the ledger read is P1 (DP-18); the codes come from the P3 reference-data contract (DP-07) and the owner role from the P7 DEVIATIONS package through the embedded Drools kit (DP-04); every call is one hop on its own base (DP-11, DP-13) with the 2 s client budget. The absence of a deviation is proved on three facts, because S8 publishes no read operation the suite may call (ASM-0523).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the screening agent raises nothing: no deviation record, no clock pause and no contact stop; S8 is never called; no rwb.deviation.DeviationRaised.v1 event is published and deviation_open stays false on the case read | agent_policy.autonomy_mode; R-DEV-01 is not fired; DP-01 |
| BR2 | A proposal carries a code from LOV-DEVIATION, reasons, source references and a confidence, and the code list is read from its owner | LOV-DEVIATION; deviation.deviation_code; DP-07 |
| BR3 | The owner role of a code is read from R-DEV-02 to R-DEV-06 of the DEVIATIONS package in force in rwb-decision (P7), evaluated through the embedded Drools kit; a code with no row maps to RW-TEAMMGR and is marked unmapped | R-DEV-02 to R-DEV-06 and R-DEV-21 (unmapped code to team manager); REQ-DVH-003; DP-04 |
| BR4 | An X1 proposal names the latest interaction in the 30 days before the complaint, read through the P1 ledger contract | REQ-DVH-007; interaction.occurred_at; DP-18 |
| BR5 | Proposals below the confidence floor are marked review and scored separately | agent_policy.confidence_floor; FEAT-DVH-08 |
| BR6 | Precision and recall per code use proposals at or above the floor against Y and N labels, with sample size 200 | agent_evaluation; REQ-DVH-001 |
| BR7 | One run per case per triggering event; the key is "SCREENING:<caseId>:<eventId>" and a repeated event is absorbed by the inbox and the key | R-UNI-40; DP-09 |
| BR8 | The run is AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`, started by the events and never by a REST call of another service | Arch v5 slide 16; DP-20 |
| BR9 | The 60 second budget belongs to the workflow, not to a REST call; every REST call of the run is one hop with a 2 s client budget | ADR-020; DP-11; NFR-010 |
| BR10 | Every fact of another service is read through its published contract: case and reference data through P3, ledger through P1, documents through P5, rule package through P7, masking and rights through P4; never a table | DP-01; DP-05; DP-06; DP-07; DP-18 |
| BR11 | Personal values are masked by P4 before any value reaches the model, and the request body, the run row, the event and the log hold masking tokens only | CTL-11; REQ-ACA-005; DP-08 |
| BR12 | Codes, owner roles, the floor, the look-back and the ledger window are data values read through a contract at run time; neither P10 nor the suite holds one in code | Principle 1; DT02 |
| BR13 | No business value is raised by a shadow run: `rwb.deviation.DeviationRaised.v1` must be absent from `rwb.deviation.events.v1` for the whole run | Arch v5 slide 15 and slide 42 (event 06); DP-09 |
| BR14 | The evaluation runs the agent in shadow on every labeled row and stores one score row per code with precision, recall and sample size; the review count is stored with the run | agent_evaluation_run; agent_evaluation; Vnnnn__evaluation_review_count.sql |
| BR15 | No personal value appears in an Api response, an event, a workflow history or the log; the run read returns ids, versions, status and measures only | Legacy section 17; Arch v5 slide 42 notes |
| BR16 | No production value is read, copied or connected to; every case, identity and personal value of the run is synthetic and the suite refuses to start outside SIT | Legacy section 17; Guardrail; AC18 |

### 9. State transitions

The state transitions of a screening run:

| From | Event | Condition | To |
|---|---|---|---|
| None | EV-01 CaseCreated or EV-16 DocumentStored processed | The answer passes every check | ANSWERED (agent_run.status), mode SHADOW, fallback false |
| None | EV-01 or EV-16 processed | The model does not answer in 60 seconds | TIMED_OUT, no retry for that event |
| None | EV-01 or EV-16 processed | A code outside X1 to X7, or an X1 proposal without its preceding contact | GUARDRAIL_FAILED with check "SCHEMA" or "SCHEMA_RULE", fallback true |
| None | EV-01 or EV-16 processed | A proposal below confidence 0.80 | ANSWERED with marker "review" on that proposal |
| None | The same event ID arrives again | A run row already exists for the case and event | No transition; the repeat is counted (R-UNI-40) |
| None | Any shadow run | Never | No deviation record, no contact stop and no clock change: the case status is untouched |

The state transitions of an evaluation:

| From | Event | Condition | To |
|---|---|---|---|
| None | Evaluation started | Sample "SCREEN-S1" version 1 has 200 labeled cases and none is running | RUNNING (agent_evaluation_run.status) |
| RUNNING | Last sample row scored | None | DONE, with one score row per code X1 to X7 |
| None | Evaluation started by a role without the right | None | No row; 403 MSG-P4-002 |

The states the run observes across the services:

| Item | States |
|---|---|
| INT-23 stub | Deterministic answer set, schema fault (X9), silent for 61 seconds, answer at confidence 0.72 |
| Screening run | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, each with fallback true or false and mode SHADOW |
| Proposal | Accepted, or marked "review", or marked "unmapped" |
| Evaluation run | RUNNING, DONE |
| Case | deviation_open false throughout; no case status change |
| Suite run | Not started, preflight failed, running, passed, failed with the failing test case named |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the suite module, the fixtures, the stub control, the clock, the absence probe, the cleanup and the evidence report |
| RW-COE, centre of excellence analyst | Loads the sample, starts the evaluation, reads scores (Rules and parameters CRUD) |
| RW-RISK, risk officer | Reads scores and the evaluation report (Rules and parameters R) |
| RW-PLATADM, platform administrator | Reads the screening runs (Platform administration R) |
| RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read run metadata and scores (Platform administration R) |
| RW-CASEOWN, case owner | Nothing in this story; a call to the evaluation read is refused with 403 and MSG-P4-002 |
| SY-AGENT, agent platform | Reads the case and its reference data (P3), the interactions (P1) and the documents and their fields (P5); evaluates the rule package through the embedded Drools kit (P7) and masks through P4 |
| Service owner of rwb-agent (P10) | Owns the run, the workflow, the queue `rwb-agent`, the topic `rwb.agent.events.v1` and the schema `rwb_agent` |
| Service owner of rwb-deviation (S8) | Owns the deviation service and its topic; publishes no read operation and is never called in shadow |
| Service owner of rwb-document (P5) | Owns the document reads and EV-16 DocumentStored |
| Service owner of rwb-access (P4) | Owns the session read, the authorise contract and the masking tokens |
| No role | Reads a service schema directly, shows a proposal to a case owner or handler, or takes production data into the run |

Approval levels: no delegation of authority level applies. The policy, the prompt, the sample and the rule package are approved by their owners before the run; this story approves nothing.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read through the P3 contract; seeded synthetically |
| DF-CAS-003 | recovery_case | product_group | Read through the P3 contract |
| DF-CAS-012 | recovery_case | region_code | Read through the P3 contract |
| DF-CAS-019 | recovery_case | deviation_open | Read through the P3 contract, asserted false on every case |
| DF-CAS-038 | deviation | deviation_code | Not read: S8 publishes no read operation, so the absence is asserted on the case read, the topic and the unused operations |
| DF-INT-001 | interaction | id | Read through the P1 contract |
| DF-INT-004 | interaction | occurred_at | Read through the P1 contract, for the 30-day look-back and the 180-day window |
| DF-INT-005 | interaction | channel | Read through the P1 contract |
| DF-INT-011 | interaction | summary | Read through the P1 contract, masked before the model call |
| DF-DOC-001 | document | id | Read through the P5 contract |
| DF-DOC-004 | document | document_type | Read through the P5 contract |
| DF-DOC-014 | document_field | field_name | Read through the P5 contract |
| DF-DOC-015 | document_field | field_value | Read through the P5 contract, masked before the model call |
| DF-REF-002 | rule_row | rule_id | Read through the P7 package version in force (ASM-0520) |
| DF-REF-010 | rule_row | owner_role | Read through the P7 package version in force (ASM-0520) |
| DF-AGT-036 to DF-AGT-057 | agent_run | id, agent_code, agent_version, prompt_version, model_version, case_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, run_at | Written by rwb-agent; read through the P10 contract, except output, which the listing never returns |
| DF-AGT-061 to DF-AGT-069 | agent_sample | sample_code, sample_version, subject_id, label_key, expected_value | Loaded through the P10 contract; read back as counts only; owned by P10 |
| DF-AGT-070 to DF-AGT-083 | agent_evaluation_run | id, status, sample_code, sample_version, failure_counts, review_count | Written by rwb-agent; read through the P10 contract; review_count added by Vnnnn__evaluation_review_count.sql |
| DF-AGT-086 to DF-AGT-096 | agent_evaluation | evaluation_run_id, label_key, sample_size, true_positive, false_positive, false_negative, precision_value, recall_value | Written by rwb-agent; read through the P10 contract and the evaluation read |

Field IDs are those of RWB-E1-062 and are copied unchanged. The suite owns no field and no table: it reads every row of this table through a contract of section 12 and writes only through the admin operations of rwb-agent, with synthetic values. The code list LOV-DEVIATION of P3 is the only reference data the run consumes for the codes (ASM-0521).

### 12. Contract

#### 12.1 REST operations provided

None. The suite provides no REST operation and no operation of its own. The reserved names of P2 rwb-integration - the base `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` - are not used, and no `rwb_integration` table is written. The screening run belongs to P10 rwb-agent, base `/api/recovery/agent/v1`, topic `rwb.agent.events.v1`, queue `rwb-agent` and schema `rwb_agent`.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| POST | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC2 and AC13: the start of the evaluation of "SCREENING" on sample "SCREEN-S1" and the refusal of a role without the right | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-evaluations` | P10 rwb-agent | AC2, AC6 and AC13: the evaluation run with its score rows and review count, polled to status "DONE" | 2 s |
| POST | `/api/recovery/agent/v1/admin/agent-samples` | P10 rwb-agent | AC2: the load of labeled sample "SCREEN-S1" version 1 with its 200 rows | 2 s + load time |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | AC1, AC3, AC7, AC8, AC9, AC14 and AC15: the run listing - id, agent, agentVersion, caseId, trigger, status, fallback, latencyMs and mode - with no prompt text, answer or personal field | 2 s |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | AC15: the policy version "P1" and prompt version "PR1" in force for agent "SCREENING", with mode SHADOW, timeout 60 seconds, floor 0.80 and output schema "screening-v1" | 2 s |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1, AC3 and AC12: the case facts the run reads, and deviation_open false after the run | 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC11: the codes X1 to X7 of list LOV-DEVIATION and the list version in force | 2 s |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | AC5 and AC10: the interactions of the case with the 180-day window, with occurred_at, channel and a masked summary | 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | AC1 and AC3: the documents of the case that the run reads | 2 s |
| GET | `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | AC3, AC5 and AC14: the document and its fields, masked before the model call | 2 s |
| GET | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | AC4 and AC11: the DEVIATIONS package version in force that carries R-DEV-02 to R-DEV-06 and the owner roles | 2 s |
| GET | `/api/recovery/access/v1/me/session` | P4 rwb-access | AC13: the rights of the caller, which prove that RW-CASEOWN holds no Rules and parameters R | 2 s |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | AC5, AC10 and AC14: the right check and the masking tokens that the run uses before the model call | 2 s |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the suite calls no service through another service. The 60 second model budget is not a REST budget: it belongs to AgentRunWorkflow of section 12.5. The P7 call reads the package version in force only; no rule row is written and no rule is evaluated by the suite (ASM-0520).

#### 12.3 Events published

None. The suite publishes no business event; it observes the events of the owning services, listed in 12.4.

#### 12.4 Events consumed

| Event | Topic | Owner | What the suite asserts |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` | `rwb.case.events.v1` | P3 rwb-case | EV-01 reaches the P10 inbox, starts AgentRunWorkflow for the case with the trigger "CaseCreated" and raises nothing; CloudEvents 1.0, key caseId (AC15) |
| `rwb.document.DocumentStored.v1` | `rwb.document.events.v1` | P5 rwb-document | EV-16 for document D-1001 of type DEATH_CERTIFICATE starts exactly one run with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored", and a repeat of the same event ID adds no run (AC3, AC7) |
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Exactly one event per run, in the same transaction as the run row; run ID, agent "SCREENING", the case ID, the trigger, the outcome, fallback and mode SHADOW; no personal field (AC1, AC8, AC9, AC14) |
| `rwb.deviation.DeviationRaised.v1` | `rwb.deviation.events.v1` | S8 rwb-deviation | Asserted absent for the whole run window: no shadow run may raise a deviation (AC12) |

A consumer dedupes on the event ID through its inbox (ADR-015, DP-09). The payload of each event is the owner's published schema; the suite asserts the envelope and the fields above and never the whole body of a prompt or an answer.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (observed, P10) | `rwb-agent` | One screening run: resolve the approved policy and prompt, read the case, the ledger and the documents through their contracts, mask, call the gateway with the 60 s budget, check the answer, evaluate the owner role from the package in force, record the run row and its outbox event; a timeout ends the run TIMED_OUT and is not retried (Arch v5 slide 16: "AgentRunWorkflow: 60 s, then rule result"; DP-20; ASM-0522) |

The suite starts no workflow of its own: the events start it, and the suite observes it on queue `rwb-agent` in namespace `rwb-recovery` through the Temporal visibility query, with the search attributes of the run. The tool reads and the gateway call are activities of rwb-agent and are observed through the run row and the event, not started by the suite.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The run is started by `rwb.case.CaseCreated.v1` and `rwb.document.DocumentStored.v1`, and the evaluation is started by RW-COE through `POST /api/recovery/agent/v1/admin/agent-evaluations`, so the suite triggers nothing on a cadence and starts no schedule of its own.

#### 12.7 Tables owned

None. The suite owns no table and never reads another service's schema (DP-01). The agent tables of schema `rwb_agent` are owned by P10 rwb-agent and are read through the operations of section 12.2; the case facts and the code list are read through P3, the interactions through P1, the documents through P5, the package version through P7 and the rights and masking through P4. No deviation table is read: S8 publishes no read operation and the absence is proved as in AC12 (ASM-0523).

#### 12.8 Contract fakes

None for a service contract. The only elements outside the nineteen services are:

| Stub | Purpose |
|---|---|
| INT-23 WireMock stub with its OpenAPI 3.1 contract | Stands in for the enterprise model endpoint that no suite may call with real prompts; returns the deterministic answer set for the 200-case run and holds the recorded request for the masking and ledger-summary assertions |
| Fault switch: schema | Returns code X9, outside X1 to X7, for AC8 |
| Fault switch: timeout | Makes the stub silent for 61 seconds, for AC9 |
| Clock control | Places the outbound call on 2026-11-25 and the complaint note on 2026-11-27, and moves the run date inside the 180-day ledger window and outside the 30-day look-back, for AC5 and AC10 |
| W1J01 synthetic fixture set | Supplies the 200 cases, the four synthetic cases, the documents, the identities and sample "SCREEN-S1" version 1; it is a fixture set, not a fake of a service |

P1 rwb-source-data, P3 rwb-case, P4 rwb-access, P5 rwb-document, P7 rwb-decision, P10 rwb-agent and S8 rwb-deviation are the real SIT services on their published contracts and are not faked in any path; a run configured with a fake for any of them fails the preflight (X10). The synthetic identities of the run come from the harness RWB-ITG-W1J01-ITG, not from a mock of rwb-access.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 13 | The five P10 admin and read operations, the two P3 reads, the P1 ledger read, the two P5 document reads, the P7 package read and the two P4 operations; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 4 event types observed, one asserted absent | `rwb.case.CaseCreated.v1`, `rwb.document.DocumentStored.v1` and `rwb.agent.AgentRunCompleted.v1` observed; `rwb.deviation.DeviationRaised.v1` asserted absent; CloudEvents 1.0, key caseId (DP-09) |
| Temporal | None | 1 workflow observed | AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`; the suite observes it, the events start it |
| File | None | None | No file in this story |

### 13. Solution plan

**Deliverables.** One suite module that reuses the harness RWB-ITG-W1J01-ITG: a stub control for INT-23 with its deterministic answer set and its two fault switches, a clock control, a fixture builder for the 200 cases and the four synthetic cases, a set of contract probes over P1, P3, P4, P5, P7 and P10, a ledger and masking probe, an absence probe over the case read, the deviation topic and the S8 request log, an evaluation driver, and an evidence report with one verdict per test case. No service code and no schema change: the suite builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| SuiteRunner | Test harness | Preflight against the published OpenAPI and AsyncAPI documents, run order, report and exit code |
| ModelStubControl | Test harness | Deploys the INT-23 stub from its OpenAPI 3.1 document, serves the deterministic answer set, sets the X9 and 61 s faults and exports the recorded request and the call count |
| ClockControl | Test harness | Places the call of 2026-11-25 and the complaint of 2026-11-27 and moves the run date for the 30-day and 180-day windows |
| RunProbe | Test harness | Reads a run through the admin listing and asserts trigger, key, status, fallback, mode, the policy and prompt versions, and the absence of prompt text, answer and personal field |
| LedgerProbe | Test harness | Reads the interactions through the P1 contract, asserts the 180-day window, the occurred_at ordering, the masked summary in the captured request and the absence of a P7 ledger reader |
| CodeListProbe | Test harness | Reads LOV-DEVIATION through the P3 contract, asserts X1 to X7 and the list version recorded on the run, and that no code is written in P10 or in the suite |
| OwnerProbe | Test harness | Reads the DEVIATIONS package version in force through P7 and asserts RW-FRAUD for X4 from R-DEV-04 and RW-TEAMMGR with marker "unmapped" for a code with no row |
| RuleCheckProbe | Test harness | Asserts the SCHEMA check for X9 and the SCHEMA_RULE check for an X1 proposal without its preceding contact |
| AbsenceProbe | Test harness | Asserts deviation_open false on the P3 case read, the absence of `rwb.deviation.DeviationRaised.v1` and the absence of any S8 POST or PATCH call |
| MaskingProbe | Test harness | Seeds the synthetic national ID number, phone number, name and account number, asserts the P4 masking tokens and scans the request body, the run row, the event and the application log |
| EvaluationDriver | Test harness | Loads sample "SCREEN-S1" version 1, starts the evaluation, polls it to DONE, reads one score row per code with precision, recall and sample size 200, and proves the 403 refusal of RW-CASEOWN |
| ReportWriter | Test harness | One row per test case with the evidence and the elapsed time, and the cleanup record |

**Database.** None of its own. The suite writes no service table, no schema object and no migration. Schema rwb_agent is owned by rwb-agent (P10) and is not written by this story. The only migration the run depends on is `Vnnnn__evaluation_review_count.sql` of P10, which adds review_count to agent_evaluation_run; it belongs to rwb-agent and is applied by its own sequence (DP-15). Vnnnn stands for the next number of the rwb-agent Flyway sequence V0001 to Vnnnn (Service Template Specification v1 §3), taken when rwb-agent adds the file.

**Configuration and reference data**

- The SIT endpoints of P1, P3, P4, P5, P7, P10 and S8, the four topic names of section 12.4, queue `rwb-agent`, namespace `rwb-recovery` and the schema-registry address, all as configuration.
- Agent "SCREENING", policy version "P1", prompt version "PR1", mode SHADOW, timeout 60 seconds, confidence floor 0.80, output schema "screening-v1", codes X1 to X7 of LOV-DEVIATION, sample "SCREEN-S1" version 1, the 30-day look-back and the 180-day ledger window, read through the contracts of section 12.2 and never written in the suite code (BR12).
- The synthetic cases RW-2026-000401, RW-2026-000402, RW-2026-000403 and RW-2026-000404, document D-1001 of type DEATH_CERTIFICATE, the synthetic users RW-COE, RW-RISK, RW-PLATADM and RW-CASEOWN, and the synthetic SY-AGENT identity, all from the W1J01 set.
- The 2 s client budget, the evaluation poll interval and the 60 s workflow budget.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added | Where it sits |
|---|---|---|---|---|
| DP01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none | Every read of the run is a contract call: `rwb_agent` behind P10, the ledger behind P1, the case and the list behind P3, the documents behind P5, the rules behind P7; no deviation table is read (12.7, AC12) |
| DP04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON | The DEVIATIONS package and R-DEV-02 to R-DEV-06 are evaluated inside P10 and read as a version through P7 (AC4, AC11) |
| DP06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON | The policy values of the run - floor, look-back, ledger window - are P10 policy data; the parameters the case read needs come through P3 (12.2) |
| DP07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON | The codes X1 to X7 come from LOV-DEVIATION through P3 and the list version is recorded on the run (AC11) |
| DP09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON | EV-01 and EV-16 start the run through the P10 inbox and `rwb.agent.AgentRunCompleted.v1` is written to the outbox; `rwb.deviation.DeviationRaised.v1` is asserted absent (AC3, AC7, AC15) |
| DP13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none | Every path of 12.2 sits on the base of its owner (AC10, AC11, AC12, AC13); the preflight asserts the bases |
| DP15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON | The suite owns no migration; `Vnnnn__evaluation_review_count.sql` is P10's own sequence (12.7) |
| DP18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none | The interactions of a case are read through P1 with the 180-day window and no P7 reader (AC10) |
| DP19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON | No screen in this story; no user-facing endpoint returns a proposal, and the admin reads stand in for the future monitor (AC1, section 15); SCR-46 empty, loading, error and no-access states: Not specified in the source documents (DOR-RWB-ITG-E1062-ITG-10) |
| DP20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON | The run is AgentRunWorkflow on queue `rwb-agent`, started by the events, with no REST call from another service (AC15) |

The H and C dependencies of the table stay with the service, platform and operations stories that own them; this story carries none of its own, and an integration story never becomes a build dependency of another story (Template and Rules §R5.4, §R5.7). This story publishes no contract and owns no contract fake, so no RWB-ITG-E1062-CON and no fake library version is needed; it runs against the real SIT services and builds against the contract version API Specification v5 on the /v1 paths of section 12.2. The I list names the four builds whose behaviour the run exercises: the screening agent inside rwb-agent, the deviation service that must stay untouched, the document reads and the masking and rights of rwb-access.

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Agent configuration set | Policy version "P1" (mode SHADOW, timeout 60 seconds, floor 0.80, output schema "screening-v1") and prompt version "PR1" for agent "SCREENING", read through the P10 contract | AC1 to AC15 |
| Stub answers | The deterministic answer set for the 200 cases, the X9 answer, the 61 second silence and the 0.72 confidence answer, held by ModelStubControl | AC1, AC2, AC6, AC8, AC9 |
| Synthetic case and document set | Cases RW-2026-000401, RW-2026-000402, RW-2026-000403 and RW-2026-000404, document D-1001 of type DEATH_CERTIFICATE, the call of 2026-11-25 and the complaint note of 2026-11-27, and the synthetic personal values of AC14 | AC3, AC4, AC5, AC7, AC9, AC10, AC14 |
| Sample set | Sample "SCREEN-S1" version 1 with 200 labeled cases, one row per case and code | AC1, AC2, AC6 |
| Identity set | RW-COE, RW-RISK, RW-PLATADM, RW-CASEOWN and the SY-AGENT identity with Case record R, Documents R, Rules and parameters R, Reference data R and Decision log C | AC13, AC15 |

**Build steps**

1. Create the suite module next to harness RWB-ITG-W1J01-ITG and wire it to the SIT endpoints, the four topics, queue `rwb-agent` and the namespace, with the contract preflight that fails on any drift and refuses a fake for P1, P3, P4, P5, P7, P10 or S8.
2. Build ModelStubControl and ClockControl over the INT-23 OpenAPI 3.1 document, with the recorded request, the call count, the deterministic answer set, the X9 and 61 s faults and the two business dates (AC5, AC8, AC9, AC10).
3. Build RunProbe and the event probe over the admin listing and the three observed events; assert the trigger, the run key, the status, fallback, mode and the two versions (AC1, AC3, AC7, AC8, AC9, AC15).
4. Build LedgerProbe: the P1 interactions read with the 180-day window, the masked summary in the captured request and the absence of a P7 ledger reader (AC5, AC10).
5. Build CodeListProbe and OwnerProbe: LOV-DEVIATION through P3 with its version, and the DEVIATIONS package version in force through P7 with RW-FRAUD from R-DEV-04 and RW-TEAMMGR "unmapped" (AC4, AC11).
6. Build RuleCheckProbe: the SCHEMA check for X9 and the SCHEMA_RULE check for the X1 proposal without its preceding contact (AC5, AC8).
7. Build MaskingProbe: seed the synthetic national ID number, phone number, name and account number, assert the P4 masking tokens, and scan the request, the run row, the event and the log (AC14).
8. Build AbsenceProbe: deviation_open false through P3, the absence of `rwb.deviation.DeviationRaised.v1`, and the S8 request log showing no POST and no PATCH call (AC1, AC12).
9. Build EvaluationDriver: the sample load, the evaluation start, the poll to DONE, one score row per code with sample size 200 and the X6 counts, the review count, and the 403 refusal of RW-CASEOWN (AC2, AC6, AC13).
10. Build ReportWriter, the cleanup of the synthetic set, the sample, the evaluation run and the stub deployment, and the evidence report; run the whole suite twice to prove that a repeated event adds no run and that no deviation event appears on either pass.

**Done when.** The eighteen test cases of section 16 pass on the real services in SIT, the eighteen criteria of section 7 are signed off against the contracts, one score row per code X1 to X7 exists with sample size 200 and X6 at 0.9000 and 0.7500, `rwb.deviation.DeviationRaised.v1` appears nowhere in the run window, the S8 operations were never called, the log scan finds no personal data, the synthetic set is cleaned up, and the evidence report names every criterion with its observable. The boundary test fails the build on any read of an ACE view or ACE table, every step is built on the rwb-source-data contract field names, and the party-flag, deceased-marker and freshness fields are confirmed with P1 before the wave 2 system test. No copy of a document is held in schema rwb_deviation.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-002 | Evaluation started on a sample with no labeled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Evaluation started while the same one is running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-E1-062 and this story adds no message ID. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. No case owner or handler sees a proposal, and no user-facing endpoint returns one in shadow. RW-COE and RW-RISK read evaluations and scores through the P10 evaluation operations of section 12.2; RW-PLATADM and the other Platform administration R holders read screening runs through `GET /api/recovery/agent/v1/admin/agent-runs`, which returns id, agent, agentVersion, caseId, trigger, status, fallback, latencyMs and mode and never a proposal body. The listing states the suite asserts through that operation are: an empty result for a case with no run, a list of runs per case and event, a second listing after a repeated event that shows the same one run, and a run in TIMED_OUT and in GUARDRAIL_FAILED. The agent monitor screen SCR-46 and its states come in RWB-E2-031 and are out of scope. Its empty, loading, error and no access states are Not specified in the source documents (CG-ALL-389), because Screen Specifications v1 does not define them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-062-01-ITG | AC1, BR1, BR13 | Integration | 200 synthetic cases with call notes and documents; every run in mode SHADOW; deviation_open false; no contact stop; no user-facing proposal; end to end on the real services |
| TC-E1-062-02-ITG | AC2, BR6, BR14 | Integration | Sample SCREEN-S1 version 1, 200 cases; one score row per code X1 to X7; X6 counts 18, 2 and 6 giving 0.9000 and 0.7500; end to end on the real services |
| TC-E1-062-03-ITG | AC3, BR7 | Integration | Case RW-2026-000401, DEATH_CERTIFICATE document, EV-16; key SCREENING:<caseId>:<eventId>, trigger DocumentStored; end to end on the real services |
| TC-E1-062-04-ITG | AC4, BR3, BR12 | Integration | X4 proposal on case RW-2026-000402, owner role RW-FRAUD from R-DEV-04; one code with no owner row giving RW-TEAMMGR and "unmapped"; end to end on the real services |
| TC-E1-062-05-ITG | AC5, BR4 | Integration | Outbound call 2026-11-25, complaint note 2026-11-27, 30-day look-back; SCHEMA_RULE failure for a proposal without the contact; end to end on the real services |
| TC-E1-062-06-ITG | AC6, BR5 | Integration | X2 proposal at confidence 0.72 against floor 0.80; marker "review"; counted under review and not in precision or recall; end to end on the real services |
| TC-E1-062-07-ITG | AC7, BR7 | Integration | EV-16 for document D-1001 on case RW-2026-000401 sent twice with the same event ID; one run, repeat counted; end to end on the real services |
| TC-E1-062-08-ITG | AC8, BR2 | Integration | Model stub returns code X9; status GUARDRAIL_FAILED, check SCHEMA, fallback true; end to end on the real services |
| TC-E1-062-09-ITG | AC9, BR9 | Integration | Model stub silent 61 seconds for case RW-2026-000404; status TIMED_OUT, no retry for that event; end to end on the real services |
| TC-E1-062-10-ITG | AC13, BR15 | Integration | RW-CASEOWN holds no Rules and parameters R, confirmed on GET /me/session; GET /admin/agent-evaluations refused with 403 and MSG-P4-002; end to end on the real services |
| TC-ITG-E1062-ITG-11 | AC10, BR4, BR10 | Integration | Case RW-2026-000403 with interactions in the 180-day window; P1 read, masked summary in the captured request, no P7 ledger reader, no interaction table |
| TC-ITG-E1062-ITG-12 | AC11, BR2, BR12 | Contract | LOV-DEVIATION through GET /admin/lists/{listCode} with its version in force; X1 to X7 recorded on the run; no code in P10 or in the suite |
| TC-ITG-E1062-ITG-13 | AC12, BR1, BR13 | End to end | Case RW-2026-000401 after a shadow run: deviation_open false on the P3 read, no rwb.deviation.DeviationRaised.v1 on the topic, no S8 POST or PATCH call in the gateway request log |
| TC-ITG-E1062-ITG-14 | AC14, BR11, BR15 | NFR | Synthetic national ID number, phone number, name and account number on case RW-2026-000403; masking tokens of P4; scan of the request body, the run row, rwb.agent.AgentRunCompleted.v1 and the application log |
| TC-ITG-E1062-ITG-15 | AC15, BR8, BR9 | End to end | EV-01 and EV-16 into the P10 inbox; AgentRunWorkflow on queue rwb-agent in namespace rwb-recovery; policy P1 and prompt PR1 on the run; no REST call from any service to P10 |
| TC-ITG-E1062-ITG-16 | AC16, BR10 | Integration | Fake configured for one of P1, P3, P4, P5, P7, P10 or S8; preflight refuses the run; only INT-23, the clock and the fixture set stand outside the services |
| TC-ITG-E1062-ITG-17 | AC17, BR10 | Contract | Suite step that reads a service schema directly; step absent, no client for a service schema, pipeline scan fails the change |
| TC-ITG-E1062-ITG-18 | AC18, BR16 | Integration | Suite started outside SIT; preflight refuses to start; no production value read, copied or connected to; every case, identity and personal value synthetic |

TC-E1-062-01-ITG to TC-E1-062-10-ITG are the copies of the legacy test cases of RWB-E1-062, kept with their legacy IDs and given the `-ITG` suffix; TC-E1-062-10-ITG carries the legacy access test onto the evaluation read. TC-ITG-E1062-ITG-11 to -15 are new (D-RCV-60): 11 carries the ledger read through P1, 12 the code list through P3, 13 the absence proved on three facts, 14 the personal-data scan across every artefact and 15 the workflow started by the events. The Level column follows Template and Rules §R7.2: the legacy System level becomes Integration, the legacy Access level becomes Integration, the code-list read is Contract, the absence and the event-started workflow are End to end, and the personal-data scan is NFR.

### 17. Guardrails

- No business value in code or in the suite: the agent, the mode, the timeout, the confidence floor, the output schema, the codes, the owner roles, the look-back and the ledger window are read through a contract at run time (BR12).
- No personal data in logs, events, prompts, workflow inputs, fixtures or the report: call note summaries and document field values are masked before the model call, and every national ID number, phone number, name and account number is synthetic (AC14).
- Masking before the prompt: no value reaches INT-23 before rwb-access has returned its masking token for SY-AGENT, and the recorded request is scanned for personal patterns on every run (ASM-0524).
- No cross-service table read and no schema client in the suite: every fact is read through a contract of section 12.2, 12.4 or 12.5, and a pipeline scan fails any change that adds a schema connection (DP-01).
- S8 is never called in shadow: the suite asserts the absence of `rwb.deviation.DeviationRaised.v1` and of any S8 POST or PATCH call, and a run that calls S8 fails (AC12, X8).
- One hop and a 2 s client budget on every REST call, and the 60 s model budget only inside AgentRunWorkflow; the suite calls no service through another service (ADR-020, DP-11).
- The model endpoint is reached only through the gateway client of rwb-agent and only on its private endpoint; the suite reaches it only through the recorded stub of its OpenAPI 3.1 contract.
- Prompt text and model answers never appear in a response of section 12.2, in `rwb.agent.AgentRunCompleted.v1` or in the application log; the run listing returns ids, versions and measures only.
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment.
- Clean-up in the same run: the synthetic cases and documents, the sample, the evaluation run, the stub deployment and the clock control are removed or retired, and the report records what was cleaned.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | The run of section 12.5, the P3 case read, the P1 ledger read, the P5 document reads, the INT-23 stub and the score rows of the evaluation | TC-E1-062-01-ITG, TC-E1-062-02-ITG, TC-E1-062-03-ITG, TC-E1-062-06-ITG, TC-E1-062-07-ITG, TC-E1-062-08-ITG, TC-E1-062-09-ITG, TC-ITG-E1062-ITG-14 |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | The P7 package read, R-DEV-02 to R-DEV-06 in the DEVIATIONS package and the owner role on the proposal | TC-E1-062-04-ITG, TC-ITG-E1062-ITG-12 |
| REQ-DVH-007 | A complaint is matched to the contact before it | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions`, the 30-day look-back and the SCHEMA_RULE check | TC-E1-062-05-ITG, TC-ITG-E1062-ITG-11 |
| DP-01 | Owner's schema per service; no cross-service table read | `rwb_agent` behind the P10 contract; the case, ledger, document and package reads through their owners; no deviation table read | TC-E1-062-01-ITG, TC-ITG-E1062-ITG-11, TC-ITG-E1062-ITG-13 |
| DP-04 | Embedded Drools kit and rule packages from rwb-decision | The DEVIATIONS package version in force through P7 and the owner role from R-DEV-04 | TC-E1-062-04-ITG, TC-ITG-E1062-ITG-12 |
| DP-06 | Parameters contract of rwb-case | The policy values of the run and the parameters the case read needs | TC-E1-062-01-ITG |
| DP-07 | Reference-data contract of rwb-case | `GET /api/recovery/case/v1/admin/lists/{listCode}` and the code-list version recorded on the run | TC-ITG-E1062-ITG-12 |
| DP-09 | Outbox, inbox and CloudEvents | EV-01 and EV-16 into the inbox, `rwb.agent.AgentRunCompleted.v1` from the outbox and the absent `rwb.deviation.DeviationRaised.v1` | TC-E1-062-03-ITG, TC-E1-062-07-ITG, TC-ITG-E1062-ITG-15 |
| DP-13 | `/api/recovery/<short>/v1` | The bases of section 12.2: `/api/recovery/agent/v1`, `/api/recovery/case/v1`, `/api/recovery/source-data/v1`, `/api/recovery/document/v1`, `/api/recovery/decision/v1` and `/api/recovery/access/v1` | Every test case, at the preflight |
| DP-15 | Per-service Flyway and migration ownership | The suite owns no schema and no migration; `Vnnnn__evaluation_review_count.sql` is P10's own | Every test case, at the preflight |
| DP-18 | Interaction ledger owned by rwb-source-data | The P1 interactions read with the 180-day window and the masked summary | TC-ITG-E1062-ITG-11 |
| DP-19 | Screen route through gateway-bff | No screen in this story; no user-facing endpoint returns a proposal and the admin reads stand in for the future monitor | TC-E1-062-01-ITG |
| DP-20 | Agent client through the rwb-agent contract | AgentRunWorkflow on queue `rwb-agent`, started by the events, with no REST call from another service | TC-ITG-E1062-ITG-15, TC-E1-062-03-ITG |
| ASM-0519 | The interaction ledger is read through P1 with the 180-day window and no P7 ledger reader | `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` | TC-ITG-E1062-ITG-11, TC-E1-062-05-ITG |
| ASM-0520 | Rule rows and the owner role come from P7 with the embedded Drools kit, and the package version is read through P7 | `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` and the owner role on the proposal | TC-E1-062-04-ITG, TC-ITG-E1062-ITG-12 |
| ASM-0521 | LOV-DEVIATION is read through the P3 reference-data contract and the version is recorded | `GET /api/recovery/case/v1/admin/lists/{listCode}` and the code-list version on the run | TC-ITG-E1062-ITG-12, TC-E1-062-08-ITG |
| ASM-0522 | EV-01 and EV-16 reach the inbox, AgentRunWorkflow runs on rwb-agent and shadow calls no S8 | The observed AgentRunWorkflow and the two consumed events | TC-E1-062-03-ITG, TC-E1-062-07-ITG, TC-ITG-E1062-ITG-15 |
| ASM-0523 | The deviation absence is proved through P3, the absent event and the unused S8 operations | `GET /api/recovery/case/v1/cases/{caseId}`, `rwb.deviation.events.v1` and the gateway request log | TC-E1-062-01-ITG, TC-ITG-E1062-ITG-13 |
| ASM-0524 | Masking by P4 before the model call and no personal value in any artefact | The captured request at the stub, the run row, `rwb.agent.AgentRunCompleted.v1` and the log scan | TC-ITG-E1062-ITG-14, TC-E1-062-05-ITG |
| GAP-0371 | The rule-row owner lookup, the ledger read and the deviation-absence evidence are not named for the target | The P1 ledger read, the P7 package read and the three-fact absence proof of section 12 | TC-ITG-E1062-ITG-11, TC-E1-062-04-ITG, TC-ITG-E1062-ITG-13 |

### 19. Out of scope

- The application builds this run depends on: RWB-P10-E1062-APP, RWB-S8-E1062-APP, RWB-P5-E1062-APP and RWB-P4-E1062-APP.
- The contract, database, operations and infrastructure stories of the legacy key.
- Showing proposals to a case owner or handler and raising the deviation at L1 on one segment (RWB-E2-029).
- Raising, routing, pausing and clearing a deviation (RWB-E2-015, S8), and the full deviation flows of Epic 7.
- The code list, the rule rows and the policy themselves: LOV-DEVIATION, R-DEV-02 to R-DEV-06 and policy "P1" are maintained and approved by their owners, and this story only reads them.
- The monitoring dashboard, the cost alert and the agent monitor screen SCR-46 (RWB-E1-063, RWB-E2-031).
- Changing an autonomy level through a screen and drift detection (FEAT-AGT-12, FEAT-AGT-13, Epic 3).
- The choice of model endpoint: the run reads the model version of its policy and never selects an endpoint.
- The build of the harness RWB-ITG-W1J01-ITG itself, the interaction ledger build in P1, the case and reference-data build in P3, the rule registry build in P7 and the non-functional epic RWB-ITG-NFR.
