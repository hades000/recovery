# RWB-P10-E1062-APP Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1062-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-062 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| Depends on (build) | RWB-P10-E1062-CON, RWB-PLT-E1072-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-TE013-CON, RWB-P10-E1058-APP, RWB-P10-TE013-APP |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-E1-062 for rwb-agent. The behaviour of the legacy story is unchanged and its nine criteria are carried word for word; the shadow run now lives in rwb-agent, with the run and the approved policy as rows of schema `rwb_agent` (DP-01), the owner role evaluated in the embedded Drools kit with the rule packages of rwb-decision (DP-04), the interaction ledger read from rwb-source-data instead of an in-process reader (DP-18), the parameters and the lists read from the rwb-case contracts (DP-06, DP-07), the proposals and the run facts published on `rwb.agent.events.v1` through the outbox (DP-09), the two operations served on the base `/api/recovery/agent/v1` (DP-13), the review count added by the service's own Flyway sequence (DP-15), the admin reads reached through the gateway-bff route (DP-19), and the run started through the rwb-agent contract (DP-20). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **the deviation screening agent built inside rwb-agent, in mode SHADOW: one run per case and triggering event that reads the case through the rwb-case contract, the interaction ledger through the rwb-source-data contract, the documents and their stored fields through the rwb-document contract and the open deviations through the rwb-deviation contract, evaluates R-DEV-02 to R-DEV-06 in the embedded Drools kit for the owner role of each proposed code, stores each proposal with its code, reasons, source references, preceding contact and confidence on the run in schema `rwb_agent`, publishes the run facts on `rwb.agent.events.v1` through the outbox, and scores the proposals against sample "SCREEN-S1" version 1 on the base `/api/recovery/agent/v1` behind the gateway-bff route**, so that **the Epic 2 and Epic 3 deviation flags start from an agent with measured precision and recall per deviation type — for X6 with 18 true positives, 2 false positives and 6 false negatives, precision 0.9000 and recall 0.7500 on sample size 200 — before wave 1 exits**.

### 2. Business rationale

A dispute, a death, a fraud sign or a lost contact found late means contact that should have stopped, or a case worked on the wrong route. The legacy story had the screening agent read the case, the interaction ledger and the documents at entry and when a document arrived, and propose deviations with reasons; in Epic 1 the proposals were stored only, scored against the business analysts' review and shown to nobody. It served REQ-DVH-001 (codes X1 to X7 detected from case data, call notes and documents), REQ-DVH-003 (each code routes to its named owner) and REQ-DVH-007 (a complaint matched to the contact before it).

In the legacy delivery the case, the ledger, the documents, the rule catalog and the agent tables sat in one module and one schema, the facts were read through in-process interfaces (`CaseQueryService`, `InteractionLedgerReader`, `DocumentQueryService`, `RuleEvaluator`), the rule rows were evaluated by a component of the same deployment, and the two admin paths were served on the legacy monolith base. The behaviour does not change, so the same nine criteria, the same policy values and the same sample are carried onto the service. What changes is where each fact lives and how it is reached:

- The run, the approved policy, the prompt, the sample, the evaluation run and the score rows are P10 rwb-agent, schema `rwb_agent`, and this story writes only its own (DP-01; BR8).
- The owner role of each proposed code is evaluated in the embedded Drools kit of RWB-PLT-E1072-CON, with the rule package and its rows fetched from the rwb-decision registry; the legacy in-process `RuleEvaluator` and `RuleCatalog` survive as the kit's `RuleResult` and its rule rows, never as a table of rwb-agent (DP-04; BR3).
- The interaction ledger is P1 rwb-source-data under the default ruling of §R3 and DP-18: the ledger, the call notes and the complaint notes are read through the rwb-source-data contract, never from a `recovery.interaction` table (DP-18; BR7).
- The parameters of the screen — the confidence floor 0.80, the 30-day look-back and the 180-day ledger window — and the lists LOV-DEVIATION, LOV-AGENT and LOV-AGENT-RUN are read through the rwb-case parameter and reference-data contracts (DP-06, DP-07; BR4, BR9).
- The two operations of the key are served on the base `/api/recovery/agent/v1` of rwb-agent; the legacy monolith base is retired for them (DP-13).
- The review count of the evaluation run arrives with the service's own Flyway sequence, in its own schema (DP-15).
- The run facts and each proposal leave through the outbox and inbox library as CloudEvents on `rwb.agent.events.v1`, keyed by the case (DP-09).
- RW-COE and RW-RISK reach the reads through the gateway-bff route, which is the only route a screen will use (DP-19); the run itself is started through the rwb-agent contract of RWB-P10-TE013-CON (DP-20).

The cross-service behaviour of this key — that a proposal in shadow changes nothing in rwb-deviation, that the ledger value served by P1 is the one the proposal names, and that the run is one per case and event across the P5, S8 and P10 boundaries — is proved by RWB-ITG-E1062-ITG, which is why this story carries no integration dependency (I = None) and claims none. This story builds and unit-tests its own deliverables against the published contracts and their fakes, and it owns the nine legacy acceptance criteria AC1 to AC9 and adds none: the service change of the key is stated in sections 8, 9, 12, 13 and 17 and is tested by the contract test cases of RWB-P10-E1062-CON.

### 3. Preconditions

- RWB-P10-E1058-APP is done: the agent platform, the orchestrator, the model gateway client, the prompt and policy store, the sample and configuration operations and the admin run read exist in rwb-agent, and a run can be made in mode SHADOW.
- RWB-P10-TE013-APP is done: the agent runtime client of the platform (DP-20) is in force, so the run is started through the rwb-agent contract and no caller embeds the runtime.
- RWB-P10-E1062-CON is baselined: the run-start and run-read operations, the screening proposal payload, the three event payloads and the fakes of section 12 exist as a document with its own test cases.
- RWB-PLT-E1072-CON is published: the embedded Drools kit with the KieBase registry, the `RuleResult` with `packageCode`, `packageVersion`, `ruleId` and the outputs, and the first-match semantics. RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library. RWB-PLT-E1044-CON is published: the per-service Flyway sequence with parameterized schema names. RWB-PLT-TE006-CON is published: the outbox and inbox envelope, the relay and the `.dlt` rule. RWB-PLT-N001-CON is published: the gateway-bff route contract and its stub.
- The `rwb_agent` schema baseline exists with the standard record columns and the Flyway history table of the service; the six agent tables of this story are the ones of TSD P10 v2 T3.1 and are created by the P10 migrations of RWB-P10-E1058-APP and this story's own.
- The rwb-case contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON are published: the parameters contract for the confidence floor, the look-back and the ledger window, and `GET /api/recovery/case/v1/admin/lists/{listCode}` for LOV-DEVIATION, LOV-AGENT and LOV-AGENT-RUN. The case read `GET /api/recovery/case/v1/cases/{caseId}` is published by the same owner.
- The rwb-document contract is published: `GET /api/recovery/document/v1/cases/{caseId}/documents` and `GET /api/recovery/document/v1/documents/{documentId}` with the stored `document_field` values.
- The rwb-deviation contract is published: `GET /api/recovery/deviation/v1/deviations` with the case as query, so a code already open on the case is not proposed again. The rwb-source-data contract is published for the interaction ledger. Both are read by this story and raised by nobody: in shadow no deviation record, no contact stop and no clock change is made (BR1).
- Agent "SCREENING" has policy version "P1" approved with mode SHADOW, timeout 60 seconds, confidence floor 0.80, the allowed tools read_case, read_interactions, read_documents and read_document_fields, and output schema "screening-v1" with codes from LOV-DEVIATION (X1 to X7); prompt version "PR1" is approved, and both are read as versions through the configuration operations of RWB-P10-E1058-APP.
- Policy version "P1" holds the 30-day look-back of BR4 and the 180-day ledger window of the input assembler; both are values of the approved policy row read through the parameters contract and appear nowhere in the source (BR4, ASM-0880).
- Rule rows R-DEV-02 to R-DEV-06 are loaded in the rwb-decision registry and are in force for the rule package the kit fetches, so the owner role of each code is data (BR3).
- Labelled sample "SCREEN-S1" version 1 is loaded through the sample operation of RWB-P10-E1058-APP: the business analysts' review of 200 Epic 1 cases, one row per case and code with expected value Y or N.
- The service identity SY-AGENT holds the case, document and ledger reads of section 12.2, so each read is answered under the same role check as a person; the refusals of MSG-P4-002 are proved through the platform guard.
- The login of this service is the rwb-agent login: Not specified in the source documents (GAP-0614; ASM-0878).
- The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. SY-CASEWF writes EV-01 CaseCreated for a new case, or P5 writes EV-16 DocumentStored for a document on an open case; both arrive on their owner's topic and are consumed by the screening listener of RWB-P10-E1058-APP's inbox (AC1, AC3).
2. The listener calls the orchestrator for agent "SCREENING" with the run key "SCREENING:<caseId>:<eventId>" and the idempotency key of the same value (AC3, AC7).
3. The run row is written in `rwb_agent` with agent "SCREENING", the policy version "P1", the prompt version "PR1", the model version, the case, the trigger event, the autonomy mode "SHADOW" and the idempotency key, and `rwb.agent.AgentRunStarted.v1` is inserted in the outbox in the same transaction (DP-09; BR8).
4. ScreeningInputAssembler reads its inputs through their owners' contracts: the case facts, the open deviations, the ledger entries of the last 180 days, and the documents and their stored fields (DP-01, DP-18; AC1, AC5).
5. Personal fields are masked before the model call: the ledger summary, the party fields and the stored field values leave the service only masked, and the prompt carries no national ID number, name or account number (BR7; section 17).
6. ResolveOwnerRole evaluates R-DEV-02 to R-DEV-06 in the embedded Drools kit for each proposed code and takes the owner role from the `RuleResult` outputs; a code with no row in the package maps to RW-TEAMMGR and is marked "unmapped" (DP-04; AC4).
7. CallModelGateway calls agent "SCREENING" in mode "SHADOW" with the masked inputs and the output schema "screening-v1", inside the 60-second policy budget of the run and never as a REST budget of a caller (AC8, AC9).
8. CheckScreeningGuardrail checks the answer: every code is in X1 to X7, every proposal carries reasons, source references and a confidence, and an X1 proposal names the latest interaction of the 30 days before the complaint; a check that fails ends the run GUARDRAIL_FAILED with fallback true and the check code (AC5, AC8).
9. Each proposal is stored on the run with its code, reasons, source references, preceding contact reference, owner role, confidence and the marker "review" when its confidence is below the floor 0.80 (AC1, AC4, AC6).
10. RecordScreeningRun writes the run status, the guardrail result, the confidence, the latency, the tokens, the cost and the output in the same transaction as its outbox rows; nothing in rwb-deviation, rwb-case or the contact path is written (BR1; AC1).
11. PublishScreeningEvents inserts `rwb.agent.ScreeningProposalRaised.v1` per proposal and `rwb.agent.AgentRunCompleted.v1` for the run in the outbox, keyed by the case, and the relay publishes them to `rwb.agent.events.v1` (DP-09; BR6).
12. A repeat of the same event ID leaves one run for the case and event, returns the stored run and counts the repeat; the inbox dedupes on the event ID (R-UNI-40; AC7).
13. RW-COE starts the evaluation of "SCREENING" on sample "SCREEN-S1" version 1 through the evaluation operation of RWB-P10-E1060-CON, which belongs to that story and is not re-declared here (ASM-0886).
14. ScreeningScorer compares the proposals at or above the floor with the labels and writes one score row per code X1 to X7 with sample size 200, the true positives, the false positives, the false negatives, precision and recall at four decimals, and the count of review proposals on the run; X6 with 18, 2 and 6 gives precision 0.9000 and recall 0.7500 (AC2; BR5).
15. RW-COE reads the run through `GET /api/recovery/agent/v1/agent-runs/{runId}` and the scores through the evaluation read, both reached through the gateway-bff route in front of the path, one hop each, so a screen never calls rwb-agent directly (DP-19).
16. No user-facing endpoint returns a proposal in this story, and the run changes no case field, no deviation record and no contact stop: it writes only the tables of `rwb_agent` (BR1, BR8; AC1).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The answer has a code outside X1 to X7 | Check SCHEMA fails; run GUARDRAIL_FAILED; fallback true | None to a user | AC8 |
| X2 | A proposal is below the confidence floor 0.80 | Stored with marker "review"; scored separately | None to a user | AC6 |
| X3 | An X1 proposal names no preceding contact while the ledger holds one in the 30 days before | Check SCHEMA_RULE fails for that proposal | None to a user | AC5 |
| X4 | The same event arrives twice | One run per case and event (R-UNI-40) | None to a user | AC7 |
| X5 | A proposed code has no owner row in R-DEV-02 to R-DEV-06 | Owner role stored as RW-TEAMMGR and the proposal marked "unmapped" | None to a user | AC4 |
| X6 | The agent times out | Run TIMED_OUT, counted, not retried | None to a user | AC9 |
| X7 | A role without the right | Refused with 403 | MSG-P4-002 | TC-E1-062-10 |
| X8 | A consumed contract of section 12.2 does not answer inside its 2 s budget | The run ends TOOL_UNAVAILABLE with fallback true, no proposal is raised for the case and event, the failure is counted on the run, and the run is not retried for that event | None to a user | TC-P10-E1062-CON-05 |
| X9 | The rwb-decision registry answers no rule package version for R-DEV-02 to R-DEV-06, or the checksum of the fetched package does not verify against the kit | The run ends TOOL_UNAVAILABLE with fallback true and the reason names the package, the proposal keeps no owner role, and nothing is written outside `rwb_agent` | None to a user | TC-P10-E1062-CON-05 |

X1 to X7 are the legacy exception paths of RWB-E1-062 carried onto the service; X8 and X9 are the failures that appear when a read leaves the service and when the rule package becomes a fetched artefact of the kit (DP-04, DP-18). X7 is not reached by a criterion of this story: it is proved by the access test case TC-E1-062-10 and by RWB-ITG-E1062-ITG across services, and the message is kept so a reader finds the legacy set complete.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the platform contracts and the published rwb-case, rwb-document, rwb-deviation, rwb-source-data and P7 registry contracts with their fakes; it waits only for the in-lane stories RWB-P10-E1058-APP, RWB-P10-TE013-APP and its own CON, and owns its own schema objects |
| Negotiable | The package layout, the component names and the internal order of the input assembler are design; the codes X1 to X7, the owner roles, the floor 0.80, the look-back of 30 days, the sample, the counts 18, 2 and 6, the precisions 0.9000 and 0.7500, the case identifiers and the message IDs are fixed by the legacy story |
| Valuable | Gives the error rate per deviation type that decides the L1 segment in the Epic 2 story of this key, before a deviation is raised for a customer |
| Estimable | Two listeners through one run, one prompt, one output schema, one rule kit adapter, one scorer and two operations |
| Small | Two weeks for one developer and one analyst, as in the legacy estimate |
| Testable | Each of the nine criteria is one automated test on an observable: a stored run, a proposal field, a guardrail code, a score row, a repeat count or a clock value that did not move |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening agent in shadow [E2b]

  Background:
    Given agent "SCREENING" has approved policy "P1" with mode "SHADOW", confidence floor 0.80 and prompt "PR1"
    Given rule rows R-DEV-02 to R-DEV-06 are in force

  Scenario: AC1 Shadow flags (legacy RWB-E1-062 AC1)
    Given the rwb-source-data contract mock returns the interaction ledger entries of the 200 cases
    Given 200 cases with their call notes and documents
    When the agent runs
    Then each run stores its proposed codes with reasons and source references in mode "SHADOW"
    Then no deviation record exists, deviation_open stays false on every case and no contact stop is set
    Then no user-facing endpoint returns a proposal

  Scenario: AC2 Compared (legacy RWB-E1-062 AC2)
    Given the business analysts' flags for the same 200 cases in sample "SCREEN-S1" version 1
    When the comparison runs
    Then one score row per code X1 to X7 holds precision, recall and sample size 200
    Then for X6 with 18 true positives, 2 false positives and 6 false negatives precision is 0.9000 and recall is 0.7500

  Scenario: AC3 A new document starts a run (legacy RWB-E1-062 AC3)
    Given open case "RW-2026-000401" receives a document of type "DEATH_CERTIFICATE"
    When EV-16 DocumentStored is processed
    Then one shadow run exists with key "SCREENING:<caseId>:<eventId>" and trigger "DocumentStored"

  Scenario: AC4 The owner role comes from the rule rows (legacy RWB-E1-062 AC4)
    Given the agent proposes X4 for case "RW-2026-000402"
    When the proposal is stored
    Then it holds owner role "RW-FRAUD" from rule R-DEV-04
    Then the system stores a proposed code with no owner row with owner role "RW-TEAMMGR" and marker "unmapped"

  Scenario: AC5 A complaint names the contact before it (legacy RWB-E1-062 AC5)
    Given the rwb-source-data contract mock returns the outbound call of 2026-11-25 on case "RW-2026-000403"
    Given case "RW-2026-000403" has an outbound call on 2026-11-25 and a complaint note on 2026-11-27
    When the agent proposes X1
    Then the proposal names the interaction of 2026-11-25 as the preceding contact
    Then an X1 proposal without a preceding contact, when one exists in the 30 days before, fails check "SCHEMA_RULE"

  Scenario: AC6 A low-confidence proposal is marked for review (legacy RWB-E1-062 AC6)
    Given the agent proposes X2 with confidence 0.72
    When the proposal is stored
    Then it holds marker "review"
    Then the evaluation counts it under "review" and not in precision or recall

  Scenario: AC7 A repeated event (legacy RWB-E1-062 AC7)
    Given EV-16 for document "D-1001" on case "RW-2026-000401" was processed
    When the same event ID arrives again
    Then one run exists for the case and event and the repeat is counted (R-UNI-40)

  Scenario: AC8 A code outside the list (legacy RWB-E1-062 AC8)
    Given the model stub returns code "X9"
    When the guardrail runs
    Then the run holds status "GUARDRAIL_FAILED", check "SCHEMA" and fallback true

  Scenario: AC9 Timeout (legacy RWB-E1-062 AC9)
    Given the model stub does not answer for 61 seconds
    When the agent runs for case "RW-2026-000404"
    Then the run holds status "TIMED_OUT" and is not retried for that event
```

**Target reading.** The agent "SCREENING", its policy "P1" with mode SHADOW and confidence floor 0.80, the prompt "PR1", the rule rows R-DEV-02 to R-DEV-06, the nine criteria, the sample "SCREEN-S1" version 1, the 200 cases, the counts 18, 2 and 6, the precisions 0.9000 and 0.7500, the case identifiers RW-2026-000401 to RW-2026-000404, the document "D-1001" of type "DEATH_CERTIFICATE", the code "X9", the confidence 0.72, the dates 2026-11-25 and 2026-11-27, the 30 days, the rule R-DEV-04, the owner roles RW-FRAUD and RW-TEAMMGR, the marker "unmapped", the check "SCHEMA_RULE", the 61 seconds and the run statuses GUARDRAIL_FAILED and TIMED_OUT are the legacy values of RWB-E1-062, copied character for character; every scenario line keeps its legacy title and every legacy Given, When and Then, and each carries the origin tag of its legacy criterion. Two criteria carry one inserted line as their first Given — AC1 and AC5 read the interaction ledger, which belongs to P1 rwb-source-data under DP-18, and the inserted line is the contract mock that answers it — because the ledger is the one read of those two criteria that crosses a service boundary. AC3 and AC4 read the case, the documents and the rule package, which are reached by their owners as well, and their legacy lines already name what is read, so no line is inserted and the boundary is proved by the fakes of section 12.8. The in-process `CaseQueryService`, `InteractionLedgerReader`, `DocumentQueryService.listByCase` and `getFields` and `RuleEvaluator.ownerFor` of the legacy section 12 become one-hop operations with a 2 s client budget (DP-11 behind DP-01, DP-18 and DP-04), so a proposal of this story is built from a value an owner served and never from a table read.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | In SHADOW mode the screening agent raises nothing: no deviation record, no clock pause, no contact stop, and no user-facing endpoint returns a proposal | agent_policy.autonomy_mode (DF-AGT-008); R-DEV-01 is not fired; legacy BR1 |
| BR2 | A proposal carries a code from LOV-DEVIATION, reasons, source references and a confidence | LOV-DEVIATION; deviation.deviation_code (DF-CAS-038, read through the rwb-deviation contract); legacy BR2 |
| BR3 | The owner role of a code is read from the rule rows R-DEV-02 to R-DEV-06 of the rule package the embedded kit fetches; a code with no row maps to the team manager and is marked "unmapped" | R-DEV-02, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06; REQ-DVH-003; DP-04; legacy BR3 |
| BR4 | An X1 proposal names the latest interaction in the 30 days before the complaint; the 30 days is a value of the approved policy row read through the parameters contract | REQ-DVH-007; interaction.occurred_at (DF-INT-004, read through the rwb-source-data contract); DP-06; legacy BR4 |
| BR5 | Proposals below the floor 0.80 are marked "review" and scored separately; precision and recall use the proposals at or above the floor against the Y and N labels | agent_policy.confidence_floor (DF-AGT-011); agent_evaluation (DF-AGT-090 to DF-AGT-096); legacy BR5, BR6 |
| BR6 | One run per case per triggering event, keyed "SCREENING:<caseId>:<eventId>", and the inbox dedupes on the event ID | R-UNI-40; legacy BR7; DP-09 |
| BR7 | rwb-agent reads no table of another service: the case, the ledger, the documents, the open deviations and the rule package come through their owners' contracts as SY-AGENT, and no foreign key crosses a schema | DP-01; DP-04; DP-18; Architecture v5 slide 16 |
| BR8 | The story writes six tables only — agent_run, agent_policy, agent_prompt, agent_sample, agent_evaluation_run and agent_evaluation — all in `rwb_agent`, and adds the review count by its own migration `V10_005__evaluation_review_count.sql` in its own Flyway sequence | DP-01; DP-15; Ownership Map (P10 owns the six tables) |
| BR9 | The codes X1 to X7, LOV-DEVIATION, LOV-AGENT and LOV-AGENT-RUN are read from the rwb-case reference-data contract, and a code outside the list in force is refused by the guardrail and never proposed | DP-07; ASM-0882 |
| BR10 | The run facts and each proposal are published as CloudEvents 1.0 messages on `rwb.agent.events.v1`, keyed by the case ID, in the same transaction as the run state change, and carry no personal data | DP-09; §R7.2 s17; BR7 |

### 9. State transitions

No case state transition. This story does not change a case status and raises no deviation: in shadow the rule R-DEV-01 (ANY_STATE, DEVIATION_FLAGGED, to DEV_FLAGGED) is never fired, `deviation_open` stays false and the contact stop and the clock are untouched (BR1).

The state transitions of one screening run:

| From | Event | Condition | To |
|---|---|---|---|
| None | A triggering event is consumed, or the run-start operation is called | No run exists for the same idempotency key | The run row is written and the run passes to ANSWERED when the answer passes its checks (agent_run.status, DF-AGT-046; LOV-AGENT-RUN) |
| None | A triggering event is consumed | A run exists for the same case and event ID | No second run; the stored run is returned and the repeat is counted (R-UNI-40) |
| None | A run is started | The answer fails a guardrail check | GUARDRAIL_FAILED with fallback true and the check code in guardrail_result (DF-AGT-048) |
| None | A run is started | The model does not answer inside the 60-second policy budget | TIMED_OUT with fallback true, counted, not retried for that event |
| None | A run is started | A consumed contract of section 12.2 does not answer inside its 2 s budget | TOOL_UNAVAILABLE with fallback true (X8) |
| None | A run is started | The rule package cannot be fetched or does not verify its checksum | TOOL_UNAVAILABLE with fallback true, reason naming the package (X9) |

The state transitions of the evaluation run of AC2:

| From | Event | Condition | To |
|---|---|---|---|
| None | An evaluation of "SCREENING" on "SCREEN-S1" version 1 is started through the evaluation operation of RWB-P10-E1060-CON | The sample holds labelled rows | RUNNING (agent_evaluation_run.status, DF-AGT-077) |
| RUNNING | The last label is compared and the score rows and the review count are written | None | DONE with finished_at |
| RUNNING | A run of the sample cannot be read through its owner's contract | None | FAILED with the failure count, and no score row for the case that could not be read |

Each score row of AC2 is written once per code X1 to X7 with the sample size 200 and its counts; a proposal below the floor raises the review count and is left out of precision and recall (BR5).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-AGENT, agent platform | Reads the case, the open deviations, the ledger, the documents and their stored fields through the four owner contracts, and reads the rule package through the kit (all as R) |
| SY-RULES, the embedded rule kit | Evaluates R-DEV-02 to R-DEV-06 for the owner role of a proposed code |
| RW-COE, center of excellence analyst | Loads the sample, starts the evaluation, reads the runs and the scores (Rules and parameters C and R) |
| RW-RISK, risk and model risk officer | Approves the policy and prompt versions and reads the scores (Rules and parameters A and R) |
| RW-CONDUCT, conduct and QA officer | Reads the scores and the run metadata (Rules and parameters R) |
| RW-PLATADM, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read the run metadata through the admin read (Platform administration R) |
| rwb-agent service identity (the rwb-agent login, DP-02) | Runs the screening, writes the six tables in `rwb_agent`, reads the four owner contracts and publishes the run facts and the proposals |
| rwb-deviation (S8) | Owns the deviation record, the pause and the handling; this story raises none of them in shadow and reads only its open deviations |
| rwb-source-data (P1) | Owns the interaction ledger that AC1 and AC5 read |
| No role | Reads `rwb_case`, `rwb_document`, `rwb_deviation`, `rwb_source_data` or any other service's schema, writes a deviation record in shadow, changes a case field, a contact stop or a clock, or reads production data |

The login of the service is Not specified in the source documents (GAP-0614; ASM-0878); the story names it "the rwb-agent login (DP-02)" until it is agreed. DP-08 is not in the pattern list of this key, so the story declares no rwb-access dependency: the right check is the platform guard of the service template and the legacy refusal MSG-P4-002 is proved by TC-E1-062-10.

### 11. Data

| BR Field ID | Entity (owner schema) | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (P3 `rwb_case`) | id | Read through the rwb-case contract |
| DF-CAS-003 | recovery_case (P3 `rwb_case`) | product_group | Read through the rwb-case contract |
| DF-CAS-012 | recovery_case (P3 `rwb_case`) | region_code | Read through the rwb-case contract |
| DF-CAS-019 | recovery_case (P3 `rwb_case`) | deviation_open | Read through the rwb-case contract |
| DF-CAS-038 | deviation (S8 `rwb_deviation`) | deviation_code | Read through the rwb-deviation contract (open deviations, so a code already open is not proposed again) |
| DF-INT-001 | interaction (P1 `rwb_source_data`) | id | Read through the rwb-source-data contract |
| DF-INT-004 | interaction (P1 `rwb_source_data`) | occurred_at | Read through the rwb-source-data contract |
| DF-INT-005 | interaction (P1 `rwb_source_data`) | channel | Read through the rwb-source-data contract |
| DF-INT-011 | interaction (P1 `rwb_source_data`) | summary | Read through the rwb-source-data contract (masked) |
| DF-DOC-001 | document (P5 `rwb_document`) | id | Read through the rwb-document contract |
| DF-DOC-004 | document (P5 `rwb_document`) | document_type | Read through the rwb-document contract |
| DF-DOC-014 | document_field (P5 `rwb_document`) | field_name | Read through the rwb-document contract |
| DF-DOC-015 | document_field (P5 `rwb_document`) | field_value | Read through the rwb-document contract (masked) |
| DF-REF-002 | rule_row (P7 `rwb_decision`) | rule_id | Read through the rule package the kit fetches |
| DF-REF-010 | rule_row (P7 `rwb_decision`) | owner_role | Read through the rule package the kit fetches |
| DF-AGT-036 | agent_run (P10 `rwb_agent`) | id | Write |
| DF-AGT-037 | agent_run (P10 `rwb_agent`) | agent_code | Write |
| DF-AGT-038 | agent_run (P10 `rwb_agent`) | agent_version | Write |
| DF-AGT-039 | agent_run (P10 `rwb_agent`) | prompt_version | Write |
| DF-AGT-040 | agent_run (P10 `rwb_agent`) | model_version | Write |
| DF-AGT-041 | agent_run (P10 `rwb_agent`) | case_id | Write |
| DF-AGT-042 | agent_run (P10 `rwb_agent`) | subject_id | Write |
| DF-AGT-043 | agent_run (P10 `rwb_agent`) | autonomy_mode | Write |
| DF-AGT-044 | agent_run (P10 `rwb_agent`) | trigger_event | Write |
| DF-AGT-045 | agent_run (P10 `rwb_agent`) | idempotency_key | Write |
| DF-AGT-046 | agent_run (P10 `rwb_agent`) | status | Write |
| DF-AGT-047 | agent_run (P10 `rwb_agent`) | fallback | Write |
| DF-AGT-048 | agent_run (P10 `rwb_agent`) | guardrail_result | Write |
| DF-AGT-049 | agent_run (P10 `rwb_agent`) | output | Write, including the proposals with their codes, reasons, source references, preceding contact, owner role and confidence |
| DF-AGT-050 | agent_run (P10 `rwb_agent`) | confidence | Write |
| DF-AGT-051 | agent_run (P10 `rwb_agent`) | latency_ms | Write |
| DF-AGT-052 | agent_run (P10 `rwb_agent`) | tokens_in | Write |
| DF-AGT-053 | agent_run (P10 `rwb_agent`) | tokens_out | Write |
| DF-AGT-054 | agent_run (P10 `rwb_agent`) | cost_thb | Write |
| DF-AGT-056 | agent_run (P10 `rwb_agent`) | run_at | Write |
| DF-AGT-001 to DF-AGT-025 | agent_policy (P10 `rwb_agent`) | the approved policy version "P1": autonomy_mode, confidence_floor, timeout_seconds, output_schema_ref, allowed_tools | Read as the approved version, through the configuration read of RWB-P10-E1058-APP |
| DF-AGT-026 to DF-AGT-035 | agent_prompt (P10 `rwb_agent`) | the approved prompt version "PR1" and its body hash | Read as the approved version, through the configuration read of RWB-P10-E1058-APP |
| DF-AGT-063 | agent_sample (P10 `rwb_agent`) | sample_code | Read |
| DF-AGT-064 | agent_sample (P10 `rwb_agent`) | sample_version | Read |
| DF-AGT-066 | agent_sample (P10 `rwb_agent`) | subject_id | Read |
| DF-AGT-067 | agent_sample (P10 `rwb_agent`) | label_key | Read |
| DF-AGT-068 | agent_sample (P10 `rwb_agent`) | expected_value | Read |
| DF-AGT-087 | agent_evaluation (P10 `rwb_agent`) | evaluation_run_id | Write |
| DF-AGT-089 | agent_evaluation (P10 `rwb_agent`) | label_key | Write |
| DF-AGT-090 | agent_evaluation (P10 `rwb_agent`) | sample_size | Write |
| DF-AGT-091 | agent_evaluation (P10 `rwb_agent`) | true_positive | Write |
| DF-AGT-092 | agent_evaluation (P10 `rwb_agent`) | false_positive | Write |
| DF-AGT-093 | agent_evaluation (P10 `rwb_agent`) | false_negative | Write |
| DF-AGT-095 | agent_evaluation (P10 `rwb_agent`) | precision_value | Write |
| DF-AGT-096 | agent_evaluation (P10 `rwb_agent`) | recall_value | Write |
| DF-AGT-070 | agent_evaluation_run (P10 `rwb_agent`) | id | Write |
| DF-AGT-077 | agent_evaluation_run (P10 `rwb_agent`) | status | Write |
| DF-AGT-083 | agent_evaluation_run (P10 `rwb_agent`) | failure_counts | Write |
| DF-AGT-085 | agent_evaluation_run (P10 `rwb_agent`) | review_count | Write, in the column added by `V10_005__evaluation_review_count.sql` |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-E1-062. recovery_case, deviation, interaction, document, document_field and rule_row belong to P3, S8, P1, P5 and P7 and are read only through their owners' contracts; agent_policy, agent_prompt, agent_run, agent_sample, agent_evaluation_run and agent_evaluation are the P10 tables of schema `rwb_agent` in the Ownership Map. Every read of another service's data in this table goes through that service's contract and never through its table (DP-01, DP-04, DP-18).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/agent-runs` | Start one screening run for one case and one triggering event, through the rwb-agent contract (DP-20): the request carries agent "SCREENING", the case ID, the trigger event (CaseCreated or DocumentStored), the event ID, policy version "P1", prompt version "PR1" and the idempotency key "SCREENING:<caseId>:<eventId>"; 202 AgentRun; one run per case and event | SY-AGENT service identity for the event-driven start; Rules and parameters C with scope applied for a manual start | Idempotency-Key header; a repeat returns the stored run |
| GET | `/agent-runs/{runId}` | Read one run with its status, fallback, guardrail result, the proposals with their codes, reasons, source references, preceding contact reference, owner role and confidence, and its latency and cost; 200 AgentRun | Platform administration R and Rules and parameters R, scope applied | Not applicable: the call writes nothing |

Errors: 401 no session, 403 no right (MSG-P4-002), 404 an unknown run, 409 a repeat that returns the stored run, 422 a request member missing or a trigger event outside the two of this story, 503 the store or a consumed contract unavailable.

The path of the run start below the base is Not specified in the source documents (GAP-0615; ASM-0879): the sources name only `GET /agent-runs/{id}` on Arch v5 slide 16 and no start operation, and the path is fixed by the contract of this key and not by invention of a business value. The evaluation operations — `POST` and `GET /admin/agent-evaluations` — are provided by RWB-P10-E1060-CON and are not re-declared here (ASM-0886); the configuration operations are provided by RWB-P10-E1058-APP.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC1, AC4: the case facts — the product group, the region code and `deviation_open` (DF-CAS-001, DF-CAS-003, DF-CAS-012, DF-CAS-019) | One hop, 2 s |
| GET | The parameters contract of rwb-case for the confidence floor, the 30-day look-back and the 180-day ledger window — the operation is Not specified in the source documents (GAP-0614; ASM-0883) | P3 rwb-case | AC1, AC5, AC6: the three policy values in force, read at run time and never from code | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC1, AC8: LOV-DEVIATION with X1 to X7, LOV-AGENT and LOV-AGENT-RUN, read before an answer is checked | One hop, 2 s |
| GET | `/api/recovery/deviation/v1/deviations` | S8 rwb-deviation | AC1, AC4: the open deviations of the case, so a code already open is not proposed again (DF-CAS-038) | One hop, 2 s |
| GET | The interaction-ledger operation of rwb-source-data for the entries of a case inside a window — the operation is Not specified in the source documents (GAP-0614; ASM-0880) | P1 rwb-source-data | AC1, AC5: the ledger entries of the last 180 days with their occurred_at, channel and masked summary, and the preceding contact of an X1 proposal | One hop, 2 s |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` and `/api/recovery/document/v1/documents/{documentId}` | P5 rwb-document | AC1, AC3, AC7: the documents of the case and their stored `document_field` values, masked before the model call | One hop, 2 s |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision | AC4, AC8: the rule package version with R-DEV-02 to R-DEV-06, fetched and checksum-verified by the embedded kit of RWB-PLT-E1072-CON (DP-04) | One hop, 2 s, through the kit |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent calls no service through another service and holds no schema client of another service. The rule-model read is made by the kit of RWB-PLT-E1072-CON and adds no C row of this key (ASM-0881). The model budget belongs to the agent platform and is never a REST budget of this story.

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunStarted.v1` | `rwb.agent.events.v1` | P10 | the case ID | run ID, agent_code "SCREENING", case_id, trigger_event, idempotency_key, autonomy_mode "SHADOW", policy_version, prompt_version, run_at |
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | run ID, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, status, fallback, confidence, latency_ms, run_at |
| `rwb.agent.ScreeningProposalRaised.v1` | `rwb.agent.events.v1` | P10 | the case ID | run ID, case_id, code, confidence, marker ("review", "unmapped" or empty), owner_role, the count of source references, the preceding contact reference for X1 |

All three are CloudEvents 1.0 messages inserted in the outbox in the same transaction as the run row and relayed by the outbox library; a payload is validated against its registry subject before the relay and a refusal is routed to the `.dlt` topic of `rwb.agent.events.v1` with an alert (DP-09; BR10). No personal data is carried: no name, no national ID number, no account number and no call-note text (section 17). `AgentRunCompleted` is the EV-28 of Arch v5 slide 43; `AgentRunStarted` and `ScreeningProposalRaised` are added on the same topic by the contract of this key, because only the completion event is catalogued (GAP-0614; ASM-0884).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use | Rule |
|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | AC1: a new case starts one screening run in shadow | Dedupe on the event ID in the inbox; one run per case and event |
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 rwb-document | AC3, AC7: a new document on an open case starts one screening run | Dedupe on the event ID; the payload is documentId, caseId, type and source |

No other topic is consumed: the open deviations and the ledger are read through their owners' REST contracts and the rule package through the kit (Arch v5 slides 13 and 16).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | Input: agent code "SCREENING", case ID, subject ID, trigger event, event ID, idempotency key. One execution per idempotency key, the 60-second policy budget, then the rule result (R-UNI-32) |
| AssembleScreeningInputs | Activity | `rwb-agent` | Output: the masked case facts, the open deviations, the ledger entries of the window and the documents with their masked fields; no personal field leaves the activity |
| ResolveOwnerRole | Activity | `rwb-agent` | Input: the proposed codes and the rule package in force. Output: one owner role and one marker per code, from the kit's `RuleResult` (DP-04) |
| CallModelGateway | Activity | `rwb-agent` | Input: the model code, the masked inputs, the output schema "screening-v1", the timeout. Output: the answer, or the mapped status TIMED_OUT or MODEL_ERROR |
| CheckScreeningGuardrail | Activity | `rwb-agent` | Input: the answer and the schema reference. Output: the check code and the outcome, "SCHEMA" and "SCHEMA_RULE" included |
| RecordScreeningRun | Activity (workflow kit) | `rwb-agent` | Input: the run row with its proposals, and the outbox rows; one transaction, no partial write |
| PublishScreeningEvents | Activity (outbox relay) | `rwb-agent` | Input: the outbox rows of the run. Output: the three events on `rwb.agent.events.v1`, or the `.dlt` route |

The workflow name, the queue and the 60-second budget are those of Arch v5 slide 16; the activity names are this story's and are accepted by RWB-P10-E1062-CON.

#### 12.6 Schedules

None. No Temporal Schedule belongs to this story: a screening run starts from an event or from the run-start operation and never on a cadence, and the legacy Quartz scheduler of the source is retired (DP-10 is not in the pattern list of this key).

#### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_run | P10 (`rwb_agent`) | One screening run, its versions, its status, its guardrail result, its proposals and its cost; written once per case and event |
| agent_evaluation_run | P10 (`rwb_agent`) | One evaluation of "SCREENING" on "SCREEN-S1" version 1; this story adds `review_count` integer by `V10_005__evaluation_review_count.sql` |
| agent_evaluation | P10 (`rwb_agent`) | One score row per code X1 to X7: TP, FP, FN, sample size, precision and recall |
| agent_policy | P10 (`rwb_agent`) | The approved policy row "SCREENING" version "P1", read and never written here; no column added |
| agent_prompt | P10 (`rwb_agent`) | The approved prompt version "PR1", read and never written here; no column added |
| agent_sample | P10 (`rwb_agent`) | The labelled sample "SCREEN-S1" version 1, read only |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope (DP-09) |

rwb-agent reads no table of another service and holds no foreign key across services (DP-01). The case, the deviation, the interaction, the document, its fields and the rule rows are their owners' and are read through their contracts; the parameter and reference values are P3's and are read through its contracts (DP-06, DP-07). `V10_005__evaluation_review_count.sql` runs in the rwb-agent Flyway sequence of `rwb_agent` and touches no other schema (DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case WireMock | The P3 contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON | The case "RW-2026-000401" to "RW-2026-000404" with their product group, region and `deviation_open`; LOV-DEVIATION with X1 to X7, LOV-AGENT and LOV-AGENT-RUN; the confidence floor 0.80, the 30-day look-back and the 180-day window; a case that does not exist and a slow answer |
| rwb-deviation WireMock | The S8 contract | The open deviations of the four cases, an empty answer, a deviation already open for a code, and a slow answer |
| rwb-source-data WireMock | The P1 contract | The ledger of case "RW-2026-000403" with the outbound call of 2026-11-25 and the complaint note of 2026-11-27; the ledger entries of the 200 cases; an empty ledger; a ledger that answers beyond 2 s |
| rwb-document WireMock | The P5 contract | The document "D-1001" on case "RW-2026-000401" with type "DEATH_CERTIFICATE", the documents of the 200 cases, the stored `document_field` values, and a document that is not found |
| rwb-decision rule-model fake | The P7 registry through the kit of RWB-PLT-E1072-CON | The rule package with R-DEV-02 to R-DEV-06 and the owner roles RW-FRAUD and RW-TEAMMGR; a package without a row for a code; a checksum that does not verify |
| Model gateway fake (INT-23) | The Enterprise AI private endpoint through the agent platform | A valid answer for the 200 cases, the answer with code "X9", the answer with confidence 0.72, silence for 61 seconds |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the two operations, one hop, with the query and the media type preserved |

The inbox and outbox stubs and the agent platform stub are the platform's and are used but not declared here. Every fixture is synthetic; no production call note, document or party record is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 7 consumed | The run start and the run read provided; the case read, the parameter read, the list read, the deviation read, the ledger read, the document read and the rule-model read consumed; one hop, 2 s each |
| Kafka | 3 published, 2 consumed | `AgentRunStarted`, `AgentRunCompleted` and `ScreeningProposalRaised` on `rwb.agent.events.v1`; `CaseCreated` and `DocumentStored` consumed |
| Temporal | 1 workflow, 6 activities | AgentRunWorkflow and its six activities on the queue `rwb-agent` |
| File | None | No file is read or written; the sample arrives through the sample operation of RWB-P10-E1058-APP |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.screening`, module `screening`, inside the rwb-agent service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The H and C dependencies of this table are the ones in the metadata rows: the four platform contract stories, RWB-PLT-N001-CON and the in-lane stories are build dependencies, and RWB-P3-E1042-CON and RWB-P3-E1043-CON are contract dependencies built against their fakes. DP-11 sits behind DP-01, DP-04 and DP-18 on every consumed read (one hop, 2 s) and adds no dependency of its own.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ScreeningShadowListener | Listener | Consumes EV-01 and EV-16 through the inbox and calls the orchestrator with the run key "SCREENING:<caseId>:<eventId>" (AC1, AC3, AC7) |
| ScreeningRunController | Controller | The run-start and run-read operations on `/api/recovery/agent/v1`, with the 202, the 200 and the refusal codes (DP-13) |
| ScreeningInputAssembler | Service | Builds the masked inputs: the case facts, the open deviations, the ledger entries of the 180 days and the documents with their masked fields (AC1, AC5) |
| ScreeningOwnerResolver | Service | Calls the rule kit for R-DEV-02 to R-DEV-06 and adds the owner role and the "unmapped" marker to each proposal (DP-04; AC4) |
| ScreeningRuleChecks | Service | Adds the checks "SCHEMA" and "SCHEMA_RULE": the code list and the preceding contact of X1 (AC5, AC8) |
| ScreeningScorer | Service | Precision and recall per code at four decimals, and the count of review proposals (AC2, AC6) |
| CaseContractClient, DeviationContractClient, LedgerContractClient, DocumentContractClient | Client | One hop and the 2 s budget on each consumed read (DP-01, DP-18) |
| PolicyValueReader, ReferenceDataReader | Client | The confidence floor, the look-back and the ledger window through the parameters contract, and the three lists through the reference-data contract (DP-06, DP-07) |
| ScreeningRunRepository | Repository | Writes and reads agent_run, agent_evaluation_run and agent_evaluation, and reads agent_sample, agent_policy and agent_prompt in `rwb_agent` only (DP-01) |
| ScreeningEventPublisher | Library adapter | Inserts the three events in the outbox in the run's transaction and maps a registry refusal to the `.dlt` route (DP-09) |

**Database and migrations**

- `V10_005__evaluation_review_count.sql` adds the column `review_count` integer to `agent_evaluation_run` in `rwb_agent`, runs in the rwb-agent Flyway sequence after the earlier P10 migrations, and touches no other schema (DP-15; AC6, section 12.7).
- One index for the run read and the repeat check: `ix_agent_run_case_trigger ON agent_run (case_id, trigger_event, idempotency_key)`, so the one-run-per-case-and-event rule of AC7 is answered without a scan.
- No table is created outside the six of BR8 and no foreign key crosses a service (DP-01).

**Configuration and reference data**

- Policy "SCREENING" version "P1": mode SHADOW, timeout 60 seconds, confidence floor 0.80, allowed tools read_case, read_interactions, read_documents and read_document_fields, output schema "screening-v1" with codes from LOV-DEVIATION, the 30-day look-back and the 180-day ledger window; loaded by RW-COE and approved by RW-RISK, read at run time (DP-06; ASM-0880, ASM-0883).
- Prompt version "PR1" and the output schema "screening-v1", read as versions through the configuration read of RWB-P10-E1058-APP.
- LOV-DEVIATION with X1 to X7, LOV-AGENT and LOV-AGENT-RUN, in force in rwb-case and read through its reference-data contract (DP-07; ASM-0882).
- Rule rows R-DEV-02 to R-DEV-06 in the rwb-decision registry, fetched as a package version and checksum-verified by the kit (DP-04; ASM-0881).
- The legacy feature flag `rwb.agent.screening-shadow` is kept as a data row of the platform feature-flag library: off, both listeners ignore their events (ASM-0885).
- The list codes, the 2 s client budget and the run-key format as service configuration.

**Build steps**

1. Flyway migration `V10_005__evaluation_review_count.sql` and the run index in `rwb_agent` (section 12.7).
2. The four contract clients against their fakes, with the one-hop budget and the masking (AC1, AC5).
3. PolicyValueReader and ReferenceDataReader against the P3 contract fakes, with the missing-value path (ASM-0883).
4. ScreeningInputAssembler over the case, the deviations, the ledger and the documents, with masked summaries (AC1, AC5).
5. ScreeningShadowListener for both events with the inbox dedupe and the run key (AC3, AC7).
6. ScreeningOwnerResolver over the rule kit and the fetched package, with the unmapped code and the unverified checksum (AC4; X9).
7. ScreeningRuleChecks and the guardrail path for the code list and the preceding contact (AC5, AC8).
8. ScreeningScorer with the review split and the fixture of 200 cases, X6 counts 18, 2 and 6, precision 0.9000 and recall 0.7500 (AC2, AC6).
9. ScreeningRunController and ScreeningEventPublisher on `/api/recovery/agent/v1`, with the three events and the `.dlt` route (DP-13, DP-09).
10. Pipeline scans for another service's table name, for a cross-schema foreign key, for a personal field in a payload and for the values 0.80, 30 and 180 in the source (section 17).
11. gateway-bff route contract test in front of the two operations (DP-19).

**Done when.** The ten test cases of section 16 pass, the two operations answer on `/api/recovery/agent/v1`, a DEV run over 200 synthetic cases gives one score row per code with the counts of the legacy fixture, the three events reach `rwb.agent.events.v1` in the order of the run, the migration applies cleanly on an empty `rwb_agent` schema, no business value appears in the source, and no deviation record, case field, contact stop or clock has changed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P10-002 | Evaluation on an empty sample | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | Same evaluation already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |
| MSG-P4-002 | Role without the right | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-E1-062 and this story adds no message ID. In AC1 and AC5 no message reaches a user, because a shadow proposal is stored and shown to nobody; in the access test the {action} value is "start a screening run or read its scores". The evaluation messages are raised by the evaluation operation of RWB-P10-E1060-CON, which owns them (ASM-0886).

### 15. Screens and states

No screen in this story. No case owner or handler sees a proposal, and no user-facing endpoint returns one (BR1; AC1). RW-COE reads the run through `GET /api/recovery/agent/v1/agent-runs/{runId}` and the scores through the evaluation read of RWB-P10-E1060-CON; both reads are reached through the gateway-bff route in front of the path, so a screen never calls rwb-agent directly (DP-19). The agent monitor screen that shows runs, fallback, latency and cost per agent belongs to another story of this service and is not changed here, and the deviation screens of rwb-deviation belong to S8 and to RWB-S8-E1062-APP. The exact path of the gateway-bff route in front of the two operations is Not specified in the source documents (GAP-0614; ASM-0887).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-062-01 | AC1, BR1 | Component | 200 synthetic cases with call notes and documents |
| TC-E1-062-02 | AC2, BR6 | Component | Sample SCREEN-S1 version 1; X6 counts 18, 2, 6 |
| TC-E1-062-03 | AC3 | Component | Case RW-2026-000401, DEATH_CERTIFICATE document |
| TC-E1-062-04 | AC4, BR3 | Component | X4 proposal on case RW-2026-000402; one unmapped code |
| TC-E1-062-05 | AC5, BR4 | Component | Call 2026-11-25, complaint note 2026-11-27 |
| TC-E1-062-06 | AC6, BR5 | Component | X2 proposal with confidence 0.72 |
| TC-E1-062-07 | AC7, BR7 | Component | EV-16 for document D-1001 twice |
| TC-E1-062-08 | AC8, BR2 | Component | Model stub returns code X9 |
| TC-E1-062-09 | AC9 | Component | Model stub silent 61 seconds |
| TC-E1-062-10 | Access | Contract | RW-CASEOWN calls the evaluation read; refused with MSG-P4-002 |

TC-E1-062-01 to TC-E1-062-09 are the legacy test cases of RWB-E1-062, kept with their legacy IDs and their legacy data; the legacy System level maps to Component, because the in-process call it tested is now a contract read with a fake and the cross-service behaviour of the key is proved by RWB-ITG-E1062-ITG and its `-ITG` copies. TC-E1-062-10 is the legacy access case; its legacy Access level maps to Contract, because the refusal is answered by the platform guard at the edge of the service and is asserted on the contract answer. The two boundary failures X8 and X9 are proved by the contract test cases TC-P10-E1062-CON-05 of RWB-P10-E1062-CON, because they are failures of the contract seam and not of a business criterion. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the codes X1 to X7, the owner roles, the confidence floor 0.80, the 30-day look-back, the 180-day ledger window and the model version are policy, reference and rule values read at run time, and a missing value stops the run instead of falling back to a default (BR4, BR9).
- No personal data in logs, tests, prompts, events or workflow inputs: the ledger summary and the stored field values are masked before the model call, the events carry identifiers and facts only, and no prompt carries a national ID number, a name or an account number (BR7, BR10).
- No read of another service's tables and no schema client: the case through rwb-case, the open deviations through rwb-deviation, the ledger through rwb-source-data, the documents and their fields through rwb-document and the rule package through the kit (DP-01, DP-04, DP-18).
- The six tables agent_run, agent_policy, agent_prompt, agent_sample, agent_evaluation_run and agent_evaluation are the only tables this story touches, all in `rwb_agent`, and the review count arrives only by `V10_005__evaluation_review_count.sql` (BR8, DP-15).
- The screening runs in shadow and changes nothing in force: no deviation record, no contact stop, no clock, no case field, and no user-facing endpoint returns a proposal (BR1).
- One hop and a 2 s client budget on every consumed REST call; the model budget of up to 60 seconds belongs to the agent platform and is never a REST budget of this story (DP-11, ADR-020).
- Every event is a CloudEvents 1.0 message on the owner's topic, keyed by the case, validated against its registry subject before the relay and routed to `.dlt` on refusal (DP-09, DP-14).
- Every fixture is synthetic; no production account, call note, document or party record is copied into a test or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | Business Requirements Program, section 5.15 | FEAT-DVH-01, FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-40 | TC-E1-062-01, TC-E1-062-02, TC-E1-062-03, TC-E1-062-06, TC-E1-062-07, TC-E1-062-08, TC-E1-062-09, TC-E1-062-10 |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | Business Requirements Program, section 5.15 | FEAT-DVH-04 | 11 Handle customer care and deviations | R-DEV-02, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06 | TC-E1-062-04 |
| REQ-DVH-007 | A complaint is matched to the contact before it | Business Requirements Program, section 5.15 | FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-05 |
| D-RCV-60 DP-01 | The run, the policy, the sample and the scores are rwb-agent's in `rwb_agent`, and every other fact is read through its owner's contract | Business Requirements Epic 1, section 3.9; Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-E1-062-01, TC-E1-062-04 |
| D-RCV-60 DP-04 | The owner role is evaluated in the embedded Drools kit with the rule packages of rwb-decision | Template and Rules §R5.5; ADR-017 | FEAT-DVH-04, FEAT-AGT-08 | 11 Handle customer care and deviations | R-DEV-02, R-DEV-03, R-DEV-04, R-DEV-05, R-DEV-06 | TC-E1-062-04, TC-P10-E1062-CON-05 |
| D-RCV-60 DP-06 | The confidence floor and the look-back are parameter values read at run time | Template and Rules §R5.5 | FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-06, TC-P10-E1062-CON-05 |
| D-RCV-60 DP-07 | The codes and the agent lists are read from the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-DVH-01 | 11 Handle customer care and deviations | None | TC-E1-062-08, TC-P10-E1062-CON-05 |
| D-RCV-60 DP-09 | The run facts and the proposals leave through the outbox as CloudEvents on `rwb.agent.events.v1` | Template and Rules §R5.5; ADR-015 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-P10-E1062-CON-04 |
| D-RCV-60 DP-13 | The two operations are served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-P10-E1062-CON-01, TC-P10-E1062-CON-02 |
| D-RCV-60 DP-15 | The review count arrives with the service's own migration in its own Flyway sequence | Template and Rules §R5.5; ADR-021 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-E1-062-06, TC-P10-E1062-CON-01 |
| D-RCV-60 DP-18 | The interaction ledger is rwb-source-data's and is read through its contract | Template and Rules §R5.5 | FEAT-DVH-01, FEAT-DVH-08 | 11 Handle customer care and deviations | None | TC-E1-062-01, TC-E1-062-05 |
| D-RCV-60 DP-19 | The two reads are reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-P10-E1062-CON-01 |
| D-RCV-60 DP-20 | The run is started through the rwb-agent contract and no caller embeds the runtime | Template and Rules §R5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | TC-E1-062-03, TC-P10-E1062-CON-01 |
| R-UNI-40 | One effect per case and event: the repeat is counted and changes nothing | Business Requirements Program, section 5.5 | FEAT-AGT-08 | 11 Handle customer care and deviations | R-UNI-40 | TC-E1-062-07 |
| RWB-E1-062 (legacy story) | Deviation screening agent in shadow: the nine criteria AC1 to AC9 and the access test | Business Requirements Epic 1, section 3.9 | FEAT-DVH-01, FEAT-DVH-04, FEAT-DVH-08, FEAT-AGT-08 | 11 Handle customer care and deviations | None | The ten legacy test cases of section 16 |
| RWB-ITG-E1062-ITG (integration copy) | The same behaviour proved across rwb-case, rwb-deviation, rwb-source-data, rwb-document and rwb-agent on the real services, with the `-ITG` test cases | Business Requirements Epic 1, section 3.9 | FEAT-AGT-08 | 11 Handle customer care and deviations | None | The test cases of that story |

The gap GAP-0614 records the areas the sources leave open for this story — the service login, the run-start path, the operation paths of the parameters and the ledger read, the two added events, the screening feature flag, the run status of a failed tool call and the route path in front of the reads — and each default it raises is settled by ASM-0878 to ASM-0887.

### 19. Out of scope

- The cross-service behaviour of this key: RWB-ITG-E1062-ITG, and the harness RWB-ITG-W1J01-ITG.
- The contract slice of this key, the run-start and run-read operations and the event payloads as published shapes: RWB-P10-E1062-CON.
- Raising, routing, pausing, handling and clearing a deviation: S8 rwb-deviation and RWB-S8-E1062-APP. In shadow this story raises nothing.
- The document intake that stores a document and its fields: P5 rwb-document and RWB-P5-E1062-APP.
- The right check and the refusals of MSG-P4-002 as a service deliverable: P4 rwb-access and RWB-P4-E1062-APP; the platform guard applies them here.
- The agent platform, the model gateway client, the prompt and policy store, the sample and configuration operations and the evaluation harness of RWB-P10-E1058-APP and RWB-P10-E1060-APP.
- Showing proposals to an owner and raising the deviation at L1 on one segment (the Epic 2 story of this agent, FEAT-AGT-08).
- The full deviation flows of Epic 7 and the contact stop that follows a raised deviation.
- The contract, database, operations and infrastructure stories of the legacy key, and the deployment of this capability: chart values, topic and queue provisioning, dashboards and the runbook.
