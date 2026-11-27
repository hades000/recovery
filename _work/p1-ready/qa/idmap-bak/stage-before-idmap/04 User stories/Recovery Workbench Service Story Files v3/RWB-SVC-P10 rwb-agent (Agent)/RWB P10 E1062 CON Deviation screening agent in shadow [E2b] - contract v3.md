# RWB-P10-E1062-CON Deviation screening agent in shadow [E2b]

SCB Collections and Recovery. Henka Group, 27 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-E1062-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Contract version | v1 (base `/api/recovery/agent/v1`); the ledger read is consumed from `rwb-source-data.yaml` 5.1.0 (API Specification v7) |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Size | Not specified in the source documents (DOR-RWB-P10-E1062-CON-16); the squad sizes it at refinement |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-062 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP04, DP06, DP07, DP09, DP13, DP15, DP18, DP19, DP20 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-007, FR-P10-012, FR-P10-013, FR-P10-014) |
| Status | Draft (directive resolutions) |
| Readiness decisions | RD-P1-004, RD-P1-005, RD-P1-007, RD-P1-023, RD-P1-064, RD-P1-072 |

**Version 3 changes.**

- RD-P1-064, RD-P1-072: Backfill the published Test Cases v9 cross-references.
- RD-P1-005, RD-P1-007, RD-P1-023, RD-P1-064, RD-P1-072: Use the paged case interaction read with masked summaries, access-only logging and the interim X1 check.
- The ledger read is aligned to `rwb-source-data.yaml` 5.1.0: case uuid in the path, wire names, paging, masking and error answers (RD-P1-007, with RD-P1-023, RD-P1-005 and RD-P1-004; findings 1 to 3).
- The contract states that it appends nothing to the ledger, and what a later append must carry (finding 4).
- AC11 added for the ledger read (finding 5); how a complaint is identified for X1 is pending, NEW-GAP-F10-02 (finding 6).

**Change log.** D-RCV-60, 27 November 2026: D-RCV-60 P1 developer readiness (RD-P1 register).

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-062 for rwb-agent. This is the contract slice of the legacy key: the screening run-start and run-read operations that replace the in-process orchestrator call and the legacy admin paths on the base `/api/recovery/agent/v1` (DP-13, DP-20), the screening proposal payload that replaces the `screening-v1` object of the legacy section 12, the three event payloads that turn EV-28 and the two new run facts into CloudEvents on `rwb.agent.events.v1` (DP-09), the four consumed contracts of rwb-case, rwb-deviation, rwb-source-data and rwb-document plus the rule-model read of the embedded kit (DP-04, DP-18), the tables of schema `rwb_agent` the shapes sit on (DP-01), the Flyway ownership of the review count (DP-15), the gateway-bff route in front of the reads (DP-19), and the fakes. It does not restate the whole rwb-agent contract, whose baseline is RWB-P10-E1058-CON, and it builds no business behaviour. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 31 cross-document, 2 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the rwb-agent side of the deviation screening agent fixed as a contract on Day 1: the run-start and run-read operations on the base `/api/recovery/agent/v1`, the screening proposal payload with its code, confidence, reason, source reference and owner role, the three event payloads on `rwb.agent.events.v1` for a run started, a run completed and a proposal raised, the consumed shapes of rwb-case, rwb-deviation, rwb-source-data and rwb-document and the rule-model read of the embedded kit, with the fakes that answer each of them**, so that **RWB-P10-E1062-APP, RWB-S8-E1062-APP, RWB-P5-E1062-APP, RWB-P4-E1062-APP and RWB-ITG-E1062-ITG build against one agreed, testable shape without waiting for the screening runtime to be complete**.

### 2. Business rationale

The legacy key RWB-E1-062 was written against a single deployment: the screening listener called an in-process orchestrator, the case, the interaction ledger, the documents and the rule catalog were read through in-process interfaces (`CaseQueryService`, `InteractionLedgerReader.list`, `DocumentQueryService.listByCase` and `getFields`, `RuleEvaluator.ownerFor`), the agent tables, the run and the evaluation lived in the same schema, and the two admin paths were served on the legacy monolith base (legacy section 12). In the target every one of those is a boundary: the orchestrator becomes a run-start operation on the service's own base (DP-20, DP-13; ADR-020), the ledger becomes rwb-source-data's contract (DP-18), the deviation read becomes S8's contract, the rule rows become a package the embedded kit fetches from the rwb-decision registry (DP-04; ADR-017), the run facts become events on the service's own topic (DP-09; ADR-015), and the run and its proposals become rows of schema `rwb_agent` (DP-01; ADR-014).

Contract-first only works if the seam is written down once. The seam here is small and load-bearing: two operations whose answer carries the run and its proposals so that the app story, the integration story and the screens of the deviation module need no change of shape; one proposal payload that keeps every legacy member — code, reasons, source references, the preceding contact of X1, the owner role and the confidence — and carries no personal data; three event payloads that carry facts only; and one fetched package shape that keeps the owner role a data value of rwb-decision.

If the shape is agreed and faked on Day 1, four teams move at once. The app story of this key builds the listener, the input assembler, the rule adapter, the guardrail and the scorer against these fakes; the S8 and P5 sibling stories build the deviation record and the document read against the same names; the integration story proves the same values across the real services; and every reader of a screening run reads one shape. Without it, each caller invents its own answer, the legacy members drift, and the score that decides the L1 segment stops matching the run that produced it.

This story defines the provided side of the key and the consumed side it needs, and never restates what another owner holds: the agent runtime baseline and the evaluation operations belong to RWB-P10-E1058-CON and RWB-P10-E1060-CON, the deviation record is S8's, the ledger is P1's, the case, the parameters and the lists are P3's, the documents are P5's and the rule registry is P7's (DP-01).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL), so the REST base, the topic and the event names follow the platform rule and not a local choice (§R4; DP-13).
- The CloudEvents 1.0 envelope and the platform error envelope are the platform baseline; this document narrows them where it must and says so.
- The agent runtime baseline contract of RWB-P10-E1058-CON is in force: the run resource, the policy and prompt resources, the admin run read and the error taxonomy are its elements, and this story reuses them rather than redefining them. Its task queue is `rwb-agent` and its namespace `rwb-recovery` (§R4).
- The evaluation contract of RWB-P10-E1060-CON is in force: the sample load, the evaluation start and the evaluation read carry the score rows and the review count this key's AC2 depends on, and this story restates none of them (ASM-0886).
- The embedded Drools kit of RWB-PLT-E1072-CON publishes the KieBase registry, the first-match semantics and the `RuleResult` with `packageCode`, `packageVersion`, `ruleId` and the outputs, and the rule-model read `GET /api/recovery/decision/v1/rule-models/{n}/{v}` belongs to it (DP-04).
- The outbox and retry library of RWB-PLT-TE006-CON publishes the outbox and inbox envelope, the relay and the `.dlt` rule (DP-09).
- The parameter and reference-data client libraries of RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published, and the rwb-case contracts they wrap are the ones of RWB-P3-E1042-CON and RWB-P3-E1043-CON (DP-06, DP-07).
- The rwb-deviation contract of S8, the rwb-source-data ledger contract of P1 and the rwb-document contract of P5 are named by their owners; the operation paths this document fixes where no source names them are marked with the gap and the assumption (GAP-0615; ASM-0880, ASM-0883).
- The per-service Flyway sequence of RWB-PLT-E1044-CON is in force and `V10_005__evaluation_review_count.sql` is owned by RWB-P10-E1062-APP in the rwb-agent sequence (DP-15).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1.
- The release date 30 November 2026 is tentative and is copied unchanged.
- No deviation, screening or queue volume is stated for this module: the platform figures of NFR-001, NFR-002 and NFR-011 are the only ones available and the evaluation samples are 200 and 500 cases; the deviation rate is measured in the shadow run before the wave 2 volume test is sized (GAP-1833).
- The agent's case read maps to API-P5-002 and its document read to API-P5-003, with API-P5-009 available for an extracted-field filter; the tool call field names are published by rwb-document in its AsyncAPI and OpenAPI documents (GAP-1047).
- The DocumentStored payload carries documentId, caseId, documentType, source and storedAt, and its idempotency key is the outbox event ID, and that event ID is the eventId in the agent's run key SCREENING:<caseId>:<eventId> (GAP-1048).
- SY-AGENT holds Documents R with every personal field masked, and no clear value appears in the answer, the log or the trace; the mask format and the per-role field list are published by the masking contract of rwb-access (GAP-1049).
- A stored document is served with the type on its row and is never re-typed on read; the unknown-type refusal with 422 and MSG-P5-006 applies at store time only (GAP-1050).

### 4. Flow

1. Draft the run-start operation that replaces the in-process orchestrator call: its method, its path below the base `/api/recovery/agent/v1`, its request members, its answer resource and its refusal codes (AC1).
2. Draft the run-read operation: its path from Arch v5 slide 16, its query, its answer with the proposals, its rights, its errors and its one-hop budget (AC2).
3. Fix the screening proposal payload: the code from LOV-DEVIATION, the confidence, the reasons, the source references, the preceding contact of X1, the owner role and the marker, with no personal value in any member (AC3).
4. Declare the three events on `rwb.agent.events.v1`: the envelope, the key, the payload members taken from the `agent_run` and the proposal fields of TSD P10 v2 T3.1, the registry subject and the `.dlt` route (AC4).
5. Fix the consumed shapes: the case read, the parameter and list reads, the deviation read, the ledger read, the document read, the source-data read and the rule-model read, each with its owner, its use in the legacy criteria, its one-hop budget and the ones whose path no source names (AC5). The source-data read carries the FSD field names as source field names with no view or ACE table read; its party-flag, deceased-marker and freshness fields are confirmed with P1 before the wave 2 system test, and its call-note field with the P5 owner before the shadow screening test. The document read is a contract dependency on rwb-document, and no copy of a document is held in schema rwb_deviation.
6. Write the seven contract fakes with the answers, the errors and the timings this key's tests need (AC6).
7. Publish the nine sub-tables of section 12 and the contract tests: the operation shapes, the proposal payload, the event envelopes, the consumed shapes, the fakes and a drift test between each fake and this document (AC7).
8. Tag the baseline and hand it to RWB-P10-E1062-APP, the S8, P5 and P4 sibling stories and RWB-ITG-E1062-ITG.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the run-start request or of the answer drifts from this document: a renamed member, a retyped confidence, a dropped one of the proposal members | The contract test fails and the merge is blocked | None | AC1, AC3 |
| X2 | A run-start request arrives without the case ID, the trigger event or the idempotency key | The operation refuses the request with 422 and names the field; nothing is written | MSG-GEN-001 | AC1 |
| X3 | The proposal payload or an event payload gains a personal field | The data-steward review and the contract test refuse the payload; nothing is published | None | AC3, AC4 |
| X4 | A produced payload fails its registry subject, or the relay cannot reach the topic | The message is refused before the relay and routed to the `.dlt` topic of the agent topic with an alert | None | AC4 |
| X5 | A consumed shape drifts from its owner's published contract | The fake is corrected against the owner's document and the drift test of this document fails until they agree | None | AC5, AC6 |
| X6 | A field-level detail of a consumed operation or a payload member is missing from the source material | The element is marked with the placeholder, one gap row and one assumption row are carried, and the fake is written to the assumed shape | None | AC1, AC5, AC6 |
| X7 | The run read is asked for an unknown run, or a role without the right reads it | The operation answers 404, or 403 with MSG-P4-002, and no member of the answer leaks | MSG-P4-002 | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the agent runtime baseline, the evaluation contract, the rule kit and the rwb-case, rwb-deviation, rwb-source-data and rwb-document contracts as published |
| Negotiable | Field-level detail of the consumed operations is settled with their owners; the operation shape, the proposal payload, the event payloads and the budgets are fixed by this realignment |
| Valuable | Unblocks the app story and the three sibling stories of this key on Day 1 and gives every reader of a screening run one shape |
| Estimable | Two provided operations, six consumed reads, one proposal payload, three events, seven fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact — the schema file, the payload, the fake, the document — and never against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Deviation screening contract slice for rwb-agent

  Background:
    Given the service naming rule and the CloudEvents 1.0 envelope of the platform library are in force
    Given the agent runtime baseline contract of RWB-P10-E1058-CON is in force
    Given the outbox and inbox library and the embedded rule kit of the platform are in force

  Scenario: AC1 The run-start operation replaces the in-process orchestrator call (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When the runtime asks for a screening run for case "RW-2026-000401" with trigger event "DocumentStored", the event ID of document "D-1001" and the idempotency key "SCREENING:<caseId>:<eventId>"
    Then one operation answers with the AgentRun resource: runId, agent_code "SCREENING", case_id, trigger_event, autonomy_mode "SHADOW", policy_version "P1", prompt_version "PR1", model_version, status, fallback, idempotency_key and run_at
    Then the request carries the case ID, the trigger event, the event ID and the idempotency key, and a request without one of them is refused with 422 and MSG-GEN-001
    Then a repeat with the same idempotency key answers 409 with the stored run and writes no second row
    Then the path below the base is fixed by this document because no source names a run-start operation (GAP-0615; ASM-0879)
    Then the run status is always one of LOV-AGENT-RUN and the mode always one of LOV-AUTONOMY

  Scenario: AC2 The run read answers the run and its proposals (new, D-RCV-60)
    Given a stored run of case "RW-2026-000403" with a proposal of code "X1" at confidence 0.72 and an unmapped code
    When the run is read on GET /api/recovery/agent/v1/agent-runs/{runId}
    Then the answer carries the run facts, the guardrail result, the proposal of code "X1" with marker "review" at confidence 0.72, and the unmapped proposal with owner role "RW-TEAMMGR" and marker "unmapped"
    Then an unknown run answers 404 and a role without the right answers 403 with MSG-P4-002
    Then the read is declared once under the base /api/recovery/agent/v1 with one hop and the 2 s client budget of DP-11

  Scenario: AC3 The screening proposal payload is fixed (new, D-RCV-60)
    Given the legacy proposal object of section 12 of RWB-E1-062
    When a proposal is stored on a run of case "RW-2026-000401"
    Then it carries the code, one value of LOV-DEVIATION from X1 to X7, the confidence, the reasons, the source references, the preceding contact reference for X1, the owner role and the marker
    Then no member carries a name, a national ID number, an account number or a call-note text
    Then a code outside LOV-DEVIATION fails the schema of the payload and is never published, and the provenance of the code list is the rwb-case reference-data contract (DP-07)

  Scenario: AC4 The three events are declared on the agent topic (new, D-RCV-60)
    Given a screening run of case "RW-2026-000401" that starts, completes and raises a proposal
    When the outbox relay publishes it
    Then the message types are rwb.agent.AgentRunStarted.v1, rwb.agent.AgentRunCompleted.v1 and rwb.agent.ScreeningProposalRaised.v1 on rwb.agent.events.v1, keyed by the case ID
    Then each envelope carries the CloudEvents 1.0 attributes id, source, type, specversion, time, subject and datacontenttype, with the run ID as its subject
    Then the payloads carry the run facts and the proposal facts this document names, and no personal data
    Then AgentRunCompleted is the EV-28 of Arch v5 slide 43 and the other two are added on the same topic by this contract (GAP-0615; ASM-0884)
    Then a payload that fails the registry subject is refused before the relay and routed to the .dlt topic with an alert

  Scenario: AC5 The consumed shapes and their budgets are fixed (new, D-RCV-60)
    Given the contracts of rwb-case, rwb-deviation, rwb-source-data, rwb-document and the rule model
    When the six consumed reads of section 12.2 are reviewed
    Then each names its owner from the Ownership Map, the legacy criteria it serves and its one-hop 2 s budget
    Then the case read, the list read and the document read are the operations their owners publish, and the parameter read and the ledger read are also the operations their owners publish, while the run-start path is fixed here because no source names it (GAP-0614; GAP-0615; ASM-0879, ASM-0880, ASM-0883)
    Then the rule-model read is made by the embedded kit of RWB-PLT-E1072-CON and adds no contract dependency of this key (ASM-0881)
    Then no read names another service's table and no foreign key crosses a schema

  Scenario: AC6 The seven fakes answer every consumed shape (new, D-RCV-60)
    Given the fakes named in section 12.8
    When each consumed path, payload and error of this document is exercised
    Then rwb-case, rwb-deviation, rwb-source-data, rwb-document, the rule-model fake, the model gateway fake and the gateway-bff route stub answer it
    Then a drift between a fake and this document fails the contract test, and every fixture is synthetic

  Scenario: AC7 The nine sub-tables are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then the tables named in 12.7 are the ones the shapes sit on, no column is added by this story, and the Flyway ownership of the review count is RWB-P10-E1062-APP (ASM-0886)

  Scenario: AC8 Each business rule of section 8 is asserted by a test or a guardrail (new, D-RCV-60)
    Given the business rules BR1 to BR9 of section 8
    When the test cases of section 16 are traced to the rules
    Then each of BR1 to BR9 is asserted by a test case of section 16, and a rule that is an architecture constraint is asserted by the boundary test TC-P10-E1062-CON-09 or by a guardrail named in this story
    Then a rule with neither a test nor a guardrail fails the story review

  Scenario: AC9 A retried or timed-out screening activity writes no second run (new, D-RCV-60)
    Given a screening run of case "RW-2026-000401" with the idempotency key "SCREENING:<caseId>:<eventId>"
    When the activity of the run is retried or exceeds its timeout
    Then a retry with the same idempotency key answers 409 with the stored run and writes no second row
    Then the timeout of a consumed read is the one-hop 2 s budget of DP-11, and the timeout of the run is the policy row named in BR8, not a constant of this document

  Scenario: AC10 A consumed call that fails or does not answer leaves no proposal (new, D-RCV-60)
    Given a screening run of case "RW-2026-000401" whose consumed read of rwb-case or rwb-deviation fails or does not answer
    When the one-hop 2 s budget of that read is exceeded or the owner answers with an error
    Then the run is not completed with a proposal and no proposal is published
    Then no value is substituted for the missing answer

  Scenario: AC11 The ledger read follows the published rwb-source-data 5.1.0 shape (new, RD-P1-007)
    Given the rwb-source-data fake maps case "RW-2026-000403" to caseId "00000000-0000-4000-8000-000000000403" and holds 201 entries of that case inside the window
    When the consumer calls GET /api/recovery/source-data/v1/cases/00000000-0000-4000-8000-000000000403/interactions with "size" 200 and "page" 0, and then with "page" 1
    Then the first answer is 200 with 200 items and "total" 201, and the second is 200 with 1 item, in order of "occurredAt" and then "caseSeq"
    And every item carries "id", "occurredAt", "eventCode", "caseSeq" and "summary", and "summary" is "MASKED" for the service identity with no unmasking rule
    And a call with "RW-2026-000403" in place of the caseId is answered 400 with MSG-GEN-001
    And no POST is made to the interaction ledger and no ledger entry is written
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The screening run is one operation under `/api/recovery/agent/v1` and one answer resource; no caller embeds the agent runtime and no in-process orchestrator call survives | DP-20; DP-13; legacy section 12 | AC1, AC2; TC-P10-E1062-CON-01, TC-P10-E1062-CON-02 |
| BR2 | The proposal keeps every legacy member — code, reasons, source references, preceding contact, owner role, confidence — and carries no personal value in any of them | Legacy section 12 (the screening-v1 schema); §R7.2 s17 | AC3; TC-P10-E1062-CON-03 |
| BR3 | The run facts and the proposals leave only as CloudEvents 1.0 messages on `rwb.agent.events.v1`, keyed by the case ID, validated against their registry subject before the relay and routed to `.dlt` on failure | DP-09; DP-14; Arch v5 slides 42 and 43 | AC4; TC-P10-E1062-CON-04 |
| BR4 | A run status is always one of LOV-AGENT-RUN, a mode always one of LOV-AUTONOMY and a code always one of LOV-DEVIATION; no value outside a list in force is published or stored | TSD P10 v2 T3.2; DP-07 | AC1, AC3, AC4; TC-P10-E1062-CON-01, TC-P10-E1062-CON-03, TC-P10-E1062-CON-04 |
| BR5 | The owner role of a code is read from the rule rows of the package the kit fetches, and the contract names the member without fixing the rule content, which stays a data row of rwb-decision | DP-04; R-DEV-02 to R-DEV-06 | AC2, AC5; TC-P10-E1062-CON-02, TC-P10-E1062-CON-05 |
| BR6 | rwb-agent reads no table of another service: the case, the parameters, the lists, the deviations, the ledger, the documents and the rule package come through their owners' contracts, one hop and 2 s | DP-01; DP-06; DP-07; DP-18; DP-11 | AC5, AC10; TC-P10-E1062-CON-05, TC-P10-E1062-CON-12 |
| BR7 | The two operations belong to this key's contract; the agent runtime baseline and the evaluation operations belong to RWB-P10-E1058-CON and RWB-P10-E1060-CON and are restated, never redefined | RWB-P10-E1058-CON; RWB-P10-E1060-CON; ASM-0886 | AC8; TC-P10-E1062-CON-10; the section 17 guardrail |
| BR8 | No business value in the contract: the confidence floor, the look-back, the ledger window, the codes, the owner roles and the timeout are rows of the policy, reference and rule data, and the contract only names them | §R7.2 s17; BR-P10-001 | AC9; TC-P10-E1062-CON-11 |
| BR9 | One base and one topic per service: this contract declares `/api/recovery/agent/v1` and `rwb.agent.events.v1` for rwb-agent and never another service's path or topic as its own | DP-13; DP-14; Arch v5 slide 41 | AC1, AC4; TC-P10-E1062-CON-01, TC-P10-E1062-CON-04 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the proposal payload, the three event payloads, the six consumed shapes and the fakes are described | In review |
| In review | Consumer sign-off | The app story, the S8, P5 and P4 sibling stories and the integration story accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a query parameter or a payload field is added without removing one | Baselined |
| Baselined | Breaking change to an operation or a payload | A member of the run or the proposal, an event member or a consumed shape is removed, renamed or retyped | In review, with the owner of the affected contract |
| Baselined | Drift in a fake | A contract test fails | In review |
| Baselined | The agent runtime baseline or the evaluation contract changes a shape | RWB-P10-E1058-CON or RWB-P10-E1060-CON publishes a new shape | Baselined, aligned to that baseline |

These are the states of this document, not of a case, a deviation or a run. The run statuses themselves are those of LOV-AGENT-RUN and belong to RWB-P10-E1062-APP.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the two operations, the proposal payload, the three event payloads, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation, a payload or a budget |
| The rwb-decision owner | Owns the rule package shape and the rule-model read the kit uses, and signs off the mapping taken from its document |
| The rwb-case, rwb-deviation, rwb-source-data and rwb-document owners | Own the consumed operations and sign off the shapes taken from their documents |
| The rwb-agent app story and the S8, P5 and P4 sibling stories | Review and accept the parts they consume |
| Platform library owner | Owns the CloudEvents envelope, the error envelope, the naming rule, the outbox library and the rule kit this document reuses |
| Data steward | Confirms that no personal data field is declared in the proposal payload or in an event payload |

The identity that calls the consumed contracts is the rwb-agent service identity (DP-02); its name is Not specified in the source documents (GAP-0614; ASM-0878) and is fixed by the deployment story of the service.

The two operations are authorised through the rwb-access authorise check (DP-08).

### 11. Data

The contract declares shapes, not business values.

| Item | Content | BR Field ID |
|---|---|---|
| Run-start request | agent "SCREENING", case ID, trigger event (CaseCreated or DocumentStored), event ID, policy version "P1", prompt version "PR1", idempotency key `SCREENING:<caseId>:<eventId>` | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |
| Run answer | runId, agent_code, agent_version, model_version, case_id, autonomy_mode, trigger_event, idempotency_key, status, fallback, guardrail_result, output, confidence, latency_ms, tokens_in, tokens_out, cost_thb, run_at (the agent_run fields of TSD P10 v2 T3.1) | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |
| Proposal payload | code (LOV-DEVIATION, X1 to X7), confidence (numeric(5,4)), reasons (array of strings, masked), sourceRefs (interaction or document IDs), precedingContactId (X1 only), ownerRole (LOV-ROLE), marker ("review", "unmapped" or empty) | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |
| Refusal | the platform problem response: status, code, detail, the message ID when a business message applies | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |
| Event payloads | run started: run ID, agent_code, case_id, trigger_event, idempotency_key, autonomy_mode, policy_version, prompt_version, run_at; run completed: runid, agent, caseid, fallback, outcome (Kafka Catalog v1 EV-28); proposal raised: run ID, case_id, code, confidence, marker, owner_role, the count of source references, the preceding contact reference for X1 | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |
| Consumed shapes | the case facts, the parameter values, the three lists, the open deviations, the ledger entries, the documents and their stored fields, and the rule package with its rows | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |
| Route | the gateway-bff route in front of the two operations is a pass-through of one hop | Not specified in the source documents (DOR-RWB-P10-E1062-CON-7) |

The type and length of the reasons array and of `sourceRefs`, the member name of the preceding contact beyond the legacy wording, and the route name and path are Not specified in the source documents (GAP-0615; ASM-0880, ASM-0887); this document fixes the element names and leaves the types to the review with their owners. The run start is fixed by this contract as `POST /agent-runs` below the base (section 12.1).

### 12. Contract

#### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/agent-runs` | Start one screening run for one case and one triggering event: the request carries agent "SCREENING", the case ID, the trigger event, the event ID, policy version "P1", prompt version "PR1" and the idempotency key `SCREENING:<caseId>:<eventId>`; 202 AgentRun | Service identity SY-AGENT for the event-driven start; Rules and parameters C with scope applied for a manual start | Idempotency-Key header; a repeat answers 409 with the stored run |
| GET | `/agent-runs/{runId}` | Read one run with its status, fallback, guardrail result and proposals; 200 AgentRun | Platform administration R and Rules and parameters R, scope applied | Not applicable: the call writes nothing |

Errors: 401 no session (message ID: Not specified in the source documents (CG-ALL-2631)), 403 no right (MSG-P4-002), 404 an unknown run (message ID: Not specified in the source documents (CG-ALL-2631)), 409 a repeat that returns the stored run (message ID: Not specified in the source documents (CG-ALL-2631)), 422 a request member missing or a trigger event outside the two of this key (message ID: Not specified in the source documents (CG-ALL-2631)), 503 the store or a consumed contract unavailable (message ID: Not specified in the source documents (CG-ALL-2631)).

No source names a start operation (GAP-0615; ASM-0879): the sources name only `GET /agent-runs/{id}` on Arch v5 slide 16, so this contract fixes the run start as `POST /agent-runs` below the base, with `GET /agent-runs/{runId}` as the one run read; the path is part of the contract and carries no business value. The agent runtime baseline of RWB-P10-E1058-CON owns the policy, prompt, sample and configuration resources and the admin run read, and the evaluation operations are owned by RWB-P10-E1060-CON; this contract restates only the members this key reads and declares no admin operation of its own (ASM-0886).

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC5, and AC1 and AC4 of the app story: the case facts, the product group, the region and `deviation_open` | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | AC5: the confidence floor, the 30-day look-back and the 180-day ledger window in force | One hop, 2 s |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | AC3, AC5: LOV-DEVIATION with X1 to X7, LOV-AGENT and LOV-AGENT-RUN | One hop, 2 s |
| GET | `/api/recovery/deviation/v1/cases/{caseId}/deviations` | S8 rwb-deviation | AC5: the open deviations of the case, so a code already open is not proposed again | One hop, 2 s |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | AC5, AC11: the ledger entries of a case inside the window, as an `InteractionPage` of `rwb-source-data.yaml` 5.1.0, with their `occurredAt`, `eventCode`, `channel`, `direction`, `contactResult`, `summary` (masked by role) and `caseSeq`, and the preceding contact of X1 by its entry `id` | One hop, 2 s per page |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | AC5: the documents of the case with their stored `document_field` values | One hop, 2 s |
| GET | `/api/recovery/decision/v1/rule-models/{n}/{v}` | P7 rwb-decision | AC5 and the owner role: the rule package with R-DEV-02 to R-DEV-06, fetched and checksum-verified by the kit of RWB-PLT-E1072-CON (ASM-0881) | One hop, 2 s, through the kit |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020); the model call of up to 60 seconds happens inside the agent platform and is not a REST budget here. The rule-model read is the kit's own client and adds no contract dependency of this key.

The ledger read (RD-P1-007 rule 2; `rwb-source-data.yaml` 5.1.0):

- Path: `caseId` is the case uuid of rwb-case, never the case number; a non-uuid value answers 400 MSG-GEN-001 (RD-P1-023). The flat `/interactions` family is not used.
- Query: `channel`, `actor` (at most 64 characters, matches `actorRef`), `from`, `to`, `page` (from 0) and `size` (default 50, maximum 200). The consumer reads every page until it holds `total` entries, so that no entry of the window is missed.
- Answer: `InteractionPage` {`items`, `page`, `size`, `total`}, the entries ordered by `occurredAt` and then `caseSeq`. the screening identity receives `summary` as `MASKED` (RD-P1-072).
- Access: Case record R on the case for the service identity SY-AGENT.
- Errors: the published Problem body; 400, 401, 403 MSG-P4-002, 404 MSG-P4-003, 422 and 503 (RD-P1-004). A refusal or a failed page is a failed consumed read under AC10.
- Writes: this contract appends nothing to the ledger. A later stage that records a case action appends through `POST /cases/{caseId}/interactions` with the `InteractionRequest` of 5.1.0, the business key `<code>-<caseNo>-<yyyyMMdd>-<actionId>` and its own decision record (RD-P1-007 rules 3, 4 and 6).

Pending: identify the source of a complaint signal for X1, owner product owner with compliance (NEW-GAP-F10-02). Interim X1 checks run without a complaint signal from the ledger. The agent reads `summary` masked. Any unmasking rule remains Pending, owner data protection officer (NEW-GAP-F03-2). Ledger reads produce access-log entries only, with no decision record, DecisionRecorded event or interaction appended.

The deviation code and its owner role are evaluated from the rule package of rwb-decision through the embedded Drools kit, and the interactions are read through the ledger contract of rwb-source-data. In shadow, the absence of a deviation is proved by the case read of rwb-case answering `deviation_open` false. Every code and owner role stays in data (BR8). A run whose tool call fails carries the status "tool unavailable" of LOV-AGENT-RUN. The path of the source-data read of section 4 step 5 (party flag, deceased marker, freshness and call note) is Not specified in the source documents (GAP-1816).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.agent.AgentRunStarted.v1` | `rwb.agent.events.v1` | P10 | the case ID | run ID, agent_code "SCREENING", case_id, trigger_event, idempotency_key, autonomy_mode, policy_version, prompt_version, run_at |
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | P10 | the case ID | runid, agent, caseid, fallback, outcome |
| `rwb.agent.ScreeningProposalRaised.v1` | `rwb.agent.events.v1` | P10 | the case ID | run ID, case_id, code, confidence, marker, owner_role, the count of source references, the preceding contact reference for X1 |

All three are CloudEvents 1.0 messages inserted in the outbox in the same transaction as the run row and relayed by the outbox library; a payload is validated against its registry subject before the relay (DP-09; BR3). `AgentRunCompleted` is the EV-28 of Arch v5 slide 43; `AgentRunStarted` and `ScreeningProposalRaised` are added on the same topic by this contract, because the event catalogue names only the completion event (GAP-0615; ASM-0884).

#### 12.4 Events consumed

| Event | Topic | Owner of the type | Use in this contract |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | The trigger of a screening run on a new case; the payload is the case ID |
| `rwb.document.DocumentStored.v1` (EV-16) | `rwb.document.events.v1` | P5 rwb-document | The trigger of a screening run on a new document; the payload is documentId, caseId, type and source |

The screening feature flag is `rwb.agent.screening-shadow`, a data row of the platform feature-flag library; when it is off, both listeners ignore their events (ASM-0885).

Both are deduped on the event ID in the inbox, and one run exists per case and event (R-UNI-40). No other topic is consumed: the open deviations, the ledger, the case, the parameters, the lists and the documents are read through their owners' REST contracts and the rule package through the kit (Arch v5 slides 13 and 16).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (Arch v5 slide 16) | `rwb-agent` | Input: agent code "SCREENING", case ID, subject ID, trigger event, event ID, idempotency key. One execution per idempotency key, the 60-second policy budget, then the rule result. Workflow ID form: Not specified in the source documents (CG-ALL-2635). Start: CaseCreated (screening) per Temporal Catalog v1, and in this story also DocumentStored; duplicate-start policy: Not specified in the source documents (CG-ALL-2635) |
| AssembleScreeningInputs | Activity | `rwb-agent` | Output: the masked inputs and the inputs reference; no personal field leaves the activity |
| ResolveOwnerRole | Activity | `rwb-agent` | Input: the proposed codes and the package in force. Output: one owner role and one marker per code from the `RuleResult` |
| CallModelGateway | Activity | `rwb-agent` | Input: the model code, the masked inputs, the output schema "screening-v1", the timeout. Output: the answer, or the mapped status TIMED_OUT or MODEL_ERROR |
| CheckScreeningGuardrail | Activity | `rwb-agent` | Input: the answer and the schema reference. Output: the check code and the outcome, "SCHEMA" and "SCHEMA_RULE" included |
| RecordScreeningRun | Activity (workflow kit) | `rwb-agent` | Input: the run row with its proposals and the outbox rows; one transaction, no partial write |
| PublishScreeningEvents | Activity (outbox relay) | `rwb-agent` | Input: the outbox rows. Output: the three events, or the `.dlt` route |

The workflow name, the queue and the 60-second budget are those of Arch v5 slide 16; the activity names and their inputs and outputs are this story's and are accepted by RWB-P10-E1062-APP.

#### 12.6 Schedules

None. The screening run is event-driven and the Arch v5 job map names no job for it (slide 44). No Temporal Schedule is declared, changed or owned by this contract.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_run | P10 (`rwb_agent`) | The run answer and the run facts of the three event payloads; no column added |
| agent_policy | P10 (`rwb_agent`) | The values the contract names: mode, confidence floor, timeout, output schema, allowed tools, look-back and ledger window; no column added |
| agent_prompt | P10 (`rwb_agent`) | The prompt version "PR1" a run names; no column added |
| agent_sample, agent_evaluation_run, agent_evaluation | P10 (`rwb_agent`) | The sample, the evaluation run and the score rows this key's AC2 reads; `review_count` is added by `V10_005__evaluation_review_count.sql`, owned by RWB-P10-E1062-APP (ASM-0886) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The outbox, inbox and idempotency envelope (DP-09) |

`recovery_case`, `deviation`, `interaction`, `document`, `document_field` and `rule_row` are other owners' tables and are reached only through their contracts or the kit (DP-01, DP-04, DP-18). No foreign key crosses a schema and this story adds no table and no column.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-case WireMock | The cases "RW-2026-000401" to "RW-2026-000404" with their product group, region and `deviation_open`; LOV-DEVIATION with X1 to X7, LOV-AGENT and LOV-AGENT-RUN; the confidence floor 0.80, the 30-day look-back and the 180-day window; a case that does not exist; a slow answer | Contract tests, app story |
| rwb-deviation WireMock | The open deviations of the four cases; an empty answer; a deviation already open for a code; a slow answer | Contract tests, app story, S8 sibling story |
| rwb-source-data WireMock | `GET /cases/{caseId}/interactions` of `rwb-source-data.yaml` 5.1.0 as `InteractionPage`: the ledger of case "RW-2026-000403" (caseId "00000000-0000-4000-8000-000000000403") with the outbound call of 2026-11-25 and no complaint event, `summary` "MASKED"; the ledger entries of the 200 cases; a case with 201 entries for paging; an empty ledger; 400, 403 MSG-P4-002, 404 MSG-P4-003 and 503 Problem answers; an answer beyond 2 s | Contract tests, app story, integration story |
| rwb-document WireMock | The document "D-1001" of type "DEATH_CERTIFICATE" on case "RW-2026-000401"; the documents of the 200 cases with their stored fields; a document that is not found | Contract tests, app story, P5 sibling story |
| Rule-model fake | The package with R-DEV-02 to R-DEV-06 and the owner roles RW-FRAUD and RW-TEAMMGR; a package without a row for a code; a checksum that does not verify | Contract tests, app story |
| Model gateway fake (INT-23) | A valid answer for the 200 cases; the answer with code "X9"; the answer with confidence 0.72; silence for 61 seconds | Contract tests, app story, integration story |
| gateway-bff route stub | A pass-through route in front of the two operations, one hop, query and media type preserved | Contract tests, app story |

The decision-record stub, the outbox stub and the inbox stub are the platform's and are used but not declared here. Every fixture is synthetic; no production call note, document, party record or model answer is copied into a fake.

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 7 consumed | The run start and the run read provided; the case read, the parameter read, the list read, the deviation read, the ledger read, the document read and the rule-model read consumed; one hop, 2 s each |
| Kafka | 3 published, 2 consumed | `AgentRunStarted`, `AgentRunCompleted` and `ScreeningProposalRaised` on `rwb.agent.events.v1`; `CaseCreated` and `DocumentStored` consumed |
| Temporal | 1 workflow, 6 activities | AgentRunWorkflow and its six activities on the queue `rwb-agent` |
| File | None | No file is read or written; no payload travels as a claim-check file |

### 13. Solution plan

**Deliverables.** `contract/agent-run-start-operation.yaml` (the run-start operation, its request, its answer, its refusals and its budget), `contract/agent-run-read-operation.yaml` (the run read and the answer with the proposals), `contract/screening-proposal.schema.json` (the proposal payload of section 11), `contract/agent-run-events.asyncapi.yaml` (the three events on `rwb.agent.events.v1`), `contract/screening-consumed-contracts.md` (the six consumed shapes and their owners), and the seven WireMock mappings with their synthetic fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON for the app story |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON for the app story; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story |
| DP-18 | Interaction ledger | Ledger owned by rwb-source-data (default ruling) | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |
| DP-20 | Agent client | rwb-agent contract | this story is the contract the app story adds as C |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumer adds, and it declares no C row. DP-11 is the pattern of the two operations and of the six consumed reads.

**Build steps**

1. Write the run-start operation: method, path below the base, the six request members, the answer resource, the 409 repeat and the 422 member refusal with MSG-GEN-001; add a lint to the pipeline.
2. Write the run-read operation with its query, its answer with the proposals, its rights and its 404 and 403.
3. Write the proposal schema with the seven members, the LOV-DEVIATION domain and the no-personal-data rule, and the drift test against the legacy `screening-v1` schema.
4. Write the AsyncAPI document: the three messages, the envelope, the key, the registry subject and the `.dlt` route.
5. Write the consumed-contract note: each operation, its owner, the legacy criterion it serves and its budget; mark the paths no source names with the gap and the assumption.
6. Build the seven WireMock mappings and their synthetic fixtures, including the answer with code "X9", the answer at confidence 0.72 and the silence of 61 seconds.
7. Add the contract tests of section 16, including the drift test between each fake and this document.
8. Tag the baseline and collect the sign-off of the app and sibling stories of this key.

**Done when.** The five contract files validate in the pipeline, the eight contract tests pass, the seven fakes answer every consumed shape and payload, and RWB-P10-E1062-APP and the S8, P5 and P4 sibling stories have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-001 | A required member of the run-start request is empty | Enter {field}. |
| MSG-P4-002 | A role without the right reads an operation | You cannot {action} here. Your role does not include it. |
| MSG-P10-002 | The sample of the evaluation holds no labelled rows | Sample {sample} has no labeled rows for {agent}. Load the labels before you run the evaluation. |
| MSG-P10-003 | The same evaluation is already running | An evaluation of {agent} on sample {sample} is already running. Wait for it to finish. |

MSG-P10-002 and MSG-P10-003 are the legacy messages of RWB-E1-062 and keep their wording character for character; MSG-GEN-001 and MSG-P4-002 are the platform messages of an empty required field and of a missing right. This contract adds no message. The evaluation messages belong to the evaluation operation of RWB-P10-E1060-CON and are listed here only because the answer of this key's AC2 reads its score rows (ASM-0886).

### 15. Screens and states

None in this story. The contract serves the two operations indirectly: the run read feeds the monitor of the service and the integration story, and the gateway-bff route in front of the two operations is a pass-through of one hop (DP-19). The contract fixes no screen field, no order and no masking rule; the deviation screens of S8 and the document screens of P5 belong to those services. The route name and path are Not specified in the source documents (GAP-0615; ASM-0887).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-E1062-CON-01 | AC1 | Contract | The run-start operation validated against its schema: the six request members, a request missing each of them, the 409 repeat with the stored run, the 422 with MSG-GEN-001 and the path below the base |
| TC-P10-E1062-CON-02 | AC2 | Contract | The run read of case "RW-2026-000403": the run facts, the X1 proposal at confidence 0.72, the unmapped proposal with RW-TEAMMGR, an unknown run and a refused role |
| TC-P10-E1062-CON-03 | AC3 | Component | The proposal schema: the seven members, a code outside LOV-DEVIATION, the preceding contact of X1, and a scan for a name, a national ID number, an account number and a call-note text |
| TC-P10-E1062-CON-04 | AC4 | Component | The three messages for a run of "SCREENING" of case "RW-2026-000401": envelope, key, payload members, a status outside LOV-AGENT-RUN, a registry refusal and the `.dlt` route |
| TC-P10-E1062-CON-05 | AC5 | Contract | The six consumed shapes with their owners and their 2 s budget: the published paths, a slow answer and a rule package whose checksum does not verify |
| TC-P10-E1062-CON-06 | AC6 | Component | The seven fakes answering every consumed path and payload, and the drift test between each fake and this document |
| TC-P10-E1062-CON-07 | AC7 | Component | The nine sub-tables present with None where empty, each with its owner from the Ownership Map |
| TC-P10-E1062-CON-08 | AC2, AC3 | Contract | The answer of a run with a proposal at confidence 0.72 marked "review" and an unmapped code, asserted member by member against the schema of this document |
| TC-P10-E1062-CON-09 | AC7 | Component | The boundary of the tables of section 12.7: the nine sub-tables and no table or column beyond them, no foreign key across a schema, and a run row with no proposal |
| TC-P10-E1062-CON-10 | AC8 | Contract | Traceability of BR1 to BR9 against section 16, with the architecture rules checked by the boundary test TC-P10-E1062-CON-09 or by a guardrail |
| TC-P10-E1062-CON-11 | AC9 | Component | A repeated run with the same idempotency key answering 409 with the stored run, and a timeout read from the policy row named in BR8 |
| TC-P10-E1062-CON-12 | AC10 | Component | A consumed read of rwb-case or rwb-deviation that fails and one that does not answer within 2 s: no proposal published and no value substituted |
| TC-P10-E1062-CON-13 | AC11 | Component | 201 entries read in two pages of the 5.1.0 shape, a case number in the path refused with 400 MSG-GEN-001, and no ledger write |

TC-P10-E1062-CON-01 to TC-P10-E1062-CON-12 are new (D-RCV-60) and test only the deliverables of this story: the two operations, the proposal payload, the three event payloads, the six consumed shapes, the fakes and the completeness of section 12. They carry no legacy test case ID, because the legacy test cases of RWB-E1-062 belong to RWB-P10-E1062-APP and the cross-service behaviour belongs to RWB-ITG-E1062-ITG.

### 17. Guardrails

- No business value in the contract: the codes, the owner roles, the confidence floor 0.80, the look-back, the ledger window, the model version and the timeout stay rows of the policy, reference and rule data, and the contract only names them (BR8).
- No personal data in a payload, an event, an example or a fake: identifiers and facts only, the reasons are masked and the source references are IDs, never a name, a national ID number, an account number or a call-note text (BR2, BR3).
- The run members idempotency_key, agent_version, model_version, status and confidence follow the classification of their agent_run fields, Not personal and Internal (Data Classification v5, DF-AGT-045, DF-AGT-038, DF-AGT-040, DF-AGT-046, DF-AGT-050), and the owner role is read from rule_row.owner_role, Not personal and Internal (DF-REF-010); a same-named field of another table classed as personal data is not a source of this contract.
- The contract names the run operations and the agent topic as rwb-agent's and consumes every other operation and topic; a document that declares another service's path or topic as provided fails the review (DP-13, DP-14).
- The agent runtime baseline and the evaluation operations are restated, never redefined: RWB-P10-E1058-CON and RWB-P10-E1060-CON own them and a drift is corrected there (BR7).
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted (DP-09).
- rwb-agent declares no schema client of another service, and every consumed read is one hop with a 2 s budget (DP-01, DP-11).
- Every fixture is synthetic; no production account, call note, document, party record or model answer is copied into a schema, a payload or a fake.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DVH-001 | X1 to X7 detected from case data, call notes, documents and flags | The run-start and run-read operations, the proposal payload and the three event payloads | TC-P10-E1062-CON-01, TC-P10-E1062-CON-03, TC-P10-E1062-CON-04 |
| REQ-DVH-003 | Each code routes to its named owner; an unmapped code goes to the team manager | The owner role member of the proposal payload and the rule-model read through the kit | TC-P10-E1062-CON-03, TC-P10-E1062-CON-05, TC-P10-E1062-CON-08 |
| REQ-DVH-007 | A complaint is matched to the contact before it | The preceding contact member of the proposal payload and the ledger read of rwb-source-data | TC-P10-E1062-CON-03, TC-P10-E1062-CON-05 |
| D-RCV-60 DP-01 | The run and the proposals are rwb-agent's in `rwb_agent`, and every other fact is read through its owner's contract | Section 12.7 and the consumed shapes of 12.2 | TC-P10-E1062-CON-05, TC-P10-E1062-CON-07, TC-P10-E1062-CON-09 |
| D-RCV-60 DP-04 | The rule package is fetched and evaluated by the embedded Drools kit | The rule-model read and the owner role member | TC-P10-E1062-CON-05 |
| D-RCV-60 DP-09 | Outbox, inbox and CloudEvents on the owner's topic with a `.dlt` route | The AsyncAPI document of 12.3 and the `.dlt` declaration | TC-P10-E1062-CON-04, TC-P10-E1062-CON-06 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the two operations | TC-P10-E1062-CON-01, TC-P10-E1062-CON-02 |
| D-RCV-60 DP-18 | The interaction ledger is rwb-source-data's | The ledger read of 12.2 | TC-P10-E1062-CON-05 |
| D-RCV-60 DP-19 | The reads are reached through the gateway-bff route | The route stub of 12.8 and the note of 12.1 | TC-P10-E1062-CON-06 |
| D-RCV-60 DP-20 | The agent client is the rwb-agent contract | The run-start operation this document fixes for the app story | TC-P10-E1062-CON-01 |
| RWB-E1-062 (legacy story) | Deviation screening agent in shadow: the nine criteria and the access test | The proposals, the run facts and the rule rows the shapes were taken from | The twelve test cases of section 16 |
| RWB-ITG-E1062-ITG (integration copy) | The same shapes proved across the real services | Every consumed shape of 12.2 and every event of 12.3 | The test cases of that story |

The gap GAP-0615 records the areas the sources leave open for this contract — the run-start path and its request members, the member types of the proposal payload, the two added event names and payloads, the consumed paths no source names and the route name — and each default it raises is settled by ASM-0879 to ASM-0887.

### 19. Out of scope

- The implementation of the listener, the input assembler, the rule adapter, the guardrail, the scorer and the two controllers (RWB-P10-E1062-APP).
- The deviation record, the pause and the handling of a raised deviation (S8 rwb-deviation, RWB-S8-E1062-APP); in shadow this key raises none of them.
- The document intake and the stored fields (P5 rwb-document, RWB-P5-E1062-APP) and the right check of the platform guard (P4 rwb-access, RWB-P4-E1062-APP).
- The whole agent runtime contract, its policy and prompt resources and the admin run read (RWB-P10-E1058-CON), and the evaluation operations and the report (RWB-P10-E1060-CON).
- The case, the parameters, the reference data and the lists of rwb-case, the ledger of rwb-source-data and the rule registry and its sealing (P3, P1, P7).
- Any append to the interaction ledger: the shadow run records no case action (RD-P1-007).
- The topic, its retry and `.dlt` topics, the queue, the secrets, the dashboards, the alerts and the runbook of this key, which are held by its deployment and infrastructure stories.
- The member types of the reasons array and of `sourceRefs`, the type and length of the preceding contact reference and the route name and path, which are Not specified in the source documents (GAP-0615; ASM-0880, ASM-0887).

### 20. Remaining delivery steps

- Size the story at refinement (squad).
- Pin the rwb-source-data 5.1.0 fake and its path in the contract tests (platform library owner, NEW-ASM-A1).
- Grant SY-AGENT Case record R for the ledger read (security administrator).
- Settle how a complaint is identified in the ledger, NEW-GAP-F10-02 (product owner with compliance).
- Add the AC11 test case row to Test Cases v9 and the RTM (test lead).
- Mark the contract story Done with its fake published (rwb-agent contract owner).
