# RWB-P7-TE013-APP Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-013 for `rwb-decision` — the decision-record half of an agent step: the ledger entry that names the rule and its version, the agent and model versions, the recommendation with its confidence, the applied result and the fallback with its reason, keyed by the step key, chained, read on the two decision-log reads and countable into the fallback rate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P7-TE013-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-TE013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P7-AR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-TE013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-005, FR-P7-006, FR-P7-007, FR-P7-008, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-029) |
| Status | Draft (realignment v1) |

### 1. Story

As an **internal audit reader (RW-AUDIT) of the agent steps and of the decision service itself**, I want **the decision-record entry of every agent step held in the central ledger of `rwb-decision` — naming the rule ID and rule version the client applied, the agent version of the legacy form "INTAKE@P1/PR1", the model version, the recommendation with its confidence, the applied result, and `fallback` true with its reason TIMED_OUT, SCHEMA or NO_POLICY in the actions, linked to the agent run by its id, keyed by the idempotency key built from the step key so a repeated step yields one entry, chained to the entry before it, readable on the two decision-log reads and countable into the fallback rate** — so that **every agent answer that a case step used or refused is explainable afterwards by the rule, the versions and the recommendation it came from, and a step whose decision cannot be recorded does not act at all**.

Inside `rwb-decision` this is the decision-record half of the legacy story RWB-TE-013:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- One deliverable and nothing else: the decision-record entry of an agent step. It takes one record of one agent step, checks it against the ledger schema — the decision code is a value of LOV-DECISION, the rule ID carries its rule version, the agent version carries its policy and prompt versions in the legacy form, the inputs reference and the decided time are present — links it to the chain with the hash of the entry before it, holds it under the idempotency key built from the step key, writes the inbox row in the same transaction, and serves it back on `GET /decision-log` and `GET /decision-log/{entryId}`.
- The record is produced by the calling step through the local decision-record library of DP-03 in the calling service's own schema, in the step's own transaction and before the step acts; the library publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` from its outbox, and this service collects it into the central ledger. A write that fails therefore stops the step: the step does not act, the answer is MSG-P7-003 and an incident is raised under R-UNI-39.
- The entry holds the applied result as `final_call` — the next state of the rule result the client applied — and the agent answer only as `recommendation` with the confidence the guardrail checked: null in SHADOW, the checked answer in L1, and never the applied result. It carries the fallback in its actions — `fallback` true and the reason TIMED_OUT, SCHEMA or NO_POLICY, or `fallback` false — with the id of the agent run where a run exists. The key set of that payload and the decision code of an agent step are Not specified in the source documents (GAP-2417; ASM-4025); the legacy mapping of RWB-TE-013 section 12 is carried unchanged.
- The entry is hash chained: `prev_hash` is the `entry_hash` of the entry before it, `entry_hash` is the SHA-256 of its canonical form, `chain_seq` is never reused, and the nightly chain check JOB-14 covers it (NFR-035; FSD P7 v3 A2.1.4.2 and A2.1.4.4). The fallback rate is countable from the same rows, because the agent version is on every entry that had one and the fallback fact is in its actions; the operation and parameter names of the measure are Not specified in the source documents (GAP-2424; ASM-4032) and the measure definition is `rwb-reporting`'s.

Not this story, and said so once here, in section 6 and in section 19: the client itself — the interface, the autonomy mode, the shadow and L1 behaviour, the orchestrator call, the timeout, the policy read, the guardrail checks, the agent run, the prompt and the model registry — is RWB-P10-TE013-CON and RWB-P10-TE013-APP of `rwb-agent` (P10), with the run platform of RWB-E1-058 and the operations side of RWB-P10-TE013-OPS; the screens are the screen slices of `rwb-decision` and of `rwb-agent`; and the cross-service proof of the rule-first order, the 60 second budget, the three fallbacks and the record before the action is RWB-ITG-TE013-ITG, which reads back the P7 half this story builds. This story writes no `agent_run`, no `agent_policy` and no `agent_prompt` row and reads none of them.

The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-2420; ASM-4028); this story uses the phrase "the `rwb-decision` login (DP-02)" and never the shared monolith login.

The legacy facts are carried unchanged: one entry per agent step; the rule ID and version of the rule result; the agent version "<agent>@<policy>/<prompt>" with "INTAKE@P1/PR1"; the decision code carried by the calling step and never a constant; the recommendation, null in SHADOW and the checked answer with confidence 0.91 in L1; `final_call` from `ruleResult.toState`, "RESUME_STATE"; the three fallback reasons TIMED_OUT, SCHEMA and NO_POLICY; the link to the run by its id; the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" as the key of the record and the run; the refusal of the whole action when the record cannot be written (MSG-P7-003, R-UNI-39); and one entry for a repeated key (R-UNI-40).

The path this file stands at held an earlier artefact of the same story key from the superseded Work Package B-P7-05; it is replaced here in full and its citations, which named rows no register holds, are gone (GAP-2423; ASM-4031).

### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The legacy client put every agent call behind one interface, and the entry it wrote was the only place where the rule, the agent, the prompt and the model versions met. In the target that entry is still the proof, but it is written twice over: once locally by the calling service, in its own schema and in the same transaction as its state change, and once centrally, when `rwb-decision` collects it into the ledger on `rwb.decision-record.v1` (Architecture v5 slides 20 and 28; ADR-022). The central entry is what an auditor searches, what the chain seals and what the reports read.

The measure that decides whether an agent stays live is the fallback rate, and the legacy story sets it at below 10 percent per month (RWB-TE-013 section 2). It is measured from these entries: how often the agent did not answer, failed its guardrail or had no policy, against how often an agent step ran at all. A rate that cannot be reconstructed from stored entries is an opinion. This story makes the rate reconstructible without a second store, because the agent version and the fallback fact sit on the same row as the rule version and the applied result.

The realignment changes the mechanism, not the business rule:

1. The `DecisionLogWriter` of the monolith becomes the local decision-record library and the shared topic of DP-03, and the central ledger of this service: the record is written where the decision is taken and sealed where it is searched, which is the difference between a distributed transaction on every step and one local commit (Architecture v5 slide 28). The legacy line "the client publishes none" is superseded by that topic (GAP-2422; ASM-4030).
2. The decision code becomes a value of LOV-DECISION read with the version in force (DP-07), so a new code or sub-decision is a row and not a release.
3. The events become CloudEvents with an outbox on the producer and an inbox here (DP-09), so a redelivery writes no second entry and consumes no second chain sequence.
4. The scheduled work stays with its owner through the workflow kit (DP-10): the ledger copy is continuous ingest on Kafka and not a Schedule, and the chain check JOB-14 at 02:00 belongs to the store slice.
5. Every path is on the owner's base `/api/recovery/decision/v1` (DP-13), the migration is in the per-service Flyway sequence (DP-15), and the two reads are reached through the gateway-bff composite route of the decision-log screen (DP-19).
6. The agent is reached only through the contract of `rwb-agent` (DP-20): the agent version label, the model version and the fallback vocabulary are the contract's, and this story records them rather than deriving them. The contract is published with its fake, and this story is built against that contract and that fake until RWB-P10-TE013-CON lands.

This story carries the decision-record half of REQ-DRI-001 (the record names the rule, model, agent and prompt versions, the inputs, the recommendation, the actions and the outcome), the whole of REQ-DRI-005 (no action proceeds if its entry cannot be written) and the record-side reading of REQ-ACA-010 (the identities that write and read the ledger are checked like people). It supports NFR-033, NFR-034, NFR-035 and NFR-078, and it is the stored fact behind the agent fallback rate.

### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P10-TE013-CON | The published `rwb-agent` contract of DP-20 and its fake: the agent code, the policy version, the prompt version, the model version, the autonomy mode of the step, the run id, the run status and the fallback with its reason. It is not written yet; this story is built against the published DP-20 contract row and its fake, and every criterion of section 7 runs against that fake (ASM-4027) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the record shape, its canonical form and SHA-256, the append inside the caller's transaction, the outbox row and the `DecisionRecorded` event |
| RWB-P7-E1008-APP | The `decision_log_entry` baseline in `rwb_decision`: the append-only trigger and grants, the canonical form and the chain of `prev_hash`, `entry_hash` and `chain_seq`, the chain verifier and JOB-14. This story rebuilds none of it |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` contract (DP-07): LOV-DECISION with D1 to D9 and their sub-decisions and X1 to X7, read with the version in force |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents 1.0 (DP-09): the inbox row of a consumed event, its dedupe and the retry and dead-letter behaviour |
| RWB-PLT-E1072-CON, RWB-PLT-E1071-CON | The embedded Drools kit and the Temporal workflow kit (DP-04, DP-10), held as baselines only: the rule ID and version arrive inside the record, and this story registers no workflow and no Schedule |
| RWB-PLT-E1044-CON, RWB-PLT-N001-CON | The per-service Flyway sequence (DP-15) and the gateway-bff composite route of the two reads (DP-19); this story adds no route |

Business preconditions carried from RWB-TE-013:

- Agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1", and the run of an agent step carries the agent version "INTAKE@P1/PR1" (legacy sections 3 and 7).
- Case "RW-2026-000201" is in route state "NEW" and status "New", and the calling step's rule result is rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE" (legacy background and BR2).
- The decision code of the step is a value of LOV-DECISION read with the version in force; the fixtures carry "D6", the route decision an agent step of the route agent sits in (Architecture v5 slide 3; FSD P7 v3 T3.1 DF-DEC-003). Which sub-decision an agent step writes is Not specified in the source documents (GAP-2417; ASM-4025).
- The step key is "CASEWF:RW-2026-000201:ENTRY:2026-11-30", 38 characters inside the 80 of `decision_log_entry.idempotency_key` (TSD P7 v2 T3.1 DF-DEC-031); it is the idempotency key of the record and of the run (legacy BR5, R-UNI-40).
- The business date of the scenarios is 2026-11-30, the agent answers in 2,000 ms with confidence 0.91 in L1, and the three fallback reasons of the record are TIMED_OUT, SCHEMA and NO_POLICY (legacy section 7).
- Synthetic data only: case identifiers, agent codes, version labels, rule IDs, step keys, statuses and codes, never a real account, customer or answer text (legacy section 17).
- No build dependency. This story is Day 1 by rule (Template and Rules §R5.7): a build dependency the patterns add is a platform CON story of wave 0, and the one C dependency is the published agent contract with its fake. The release date 30 November 2026 is tentative and is copied unchanged.

### 4. Flow

1. The calling step evaluates its own rule package in its own service through the embedded kit (DP-04) and builds the rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE", before any agent is asked anything (legacy flow steps 1 and 2).
2. The calling step calls the published client with the agent code "INTAKE", the case id, the decision code "D6", the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the rule result and the masked inputs, and the client reads the policy in force through the `rwb-agent` contract (DP-20).
3. The client calls the agent run of `rwb-agent` with the step key as its idempotency key and waits at most the 60 seconds of policy "P1"; in SHADOW it keeps the rule result as the applied result, in L1 it returns the checked answer with confidence 0.91 as the recommendation, and on a timeout, a failed guardrail check or no approved policy it keeps the rule result and marks the fallback true with reason TIMED_OUT, SCHEMA or NO_POLICY (R-UNI-32). None of this is built here; it is the contract this story records.
4. The calling step builds the record of the agent step through the local decision-record library (DP-03): case reference, decision code "D6", rule "R-UNI-32" and version "2026.11", agent version "INTAKE@P1/PR1", the model version the run names, inputs reference of the masked snapshot, recommendation with confidence 0.91 in L1 and null in SHADOW, `final_call` "RESUME_STATE", actions holding the run id, the mode, `fallback` and the reason, the decided time and the idempotency key "CASEWF:RW-2026-000201:ENTRY:2026-11-30".
5. The library appends the record in the calling service's own schema inside the step's transaction, writes the outbox row of `DecisionRecorded` in the same transaction and computes the record hash and its chain link. If the append fails, the transaction rolls back, the step does not act, the client raises its not-recorded condition carrying MSG-P7-003, and one incident is raised under R-UNI-39 (REQ-DRI-005; FSD P7 v3 A2.5.4.3).
6. The outbox relay of the calling service publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, CloudEvents 1.0, keyed by the case id, carrying the record (DP-09; Architecture v5 slides 20 and 42).
7. `rwb-decision` `DecisionRecordListener` consumes the event and writes the inbox row; an event ID already held appends nothing and the repeat count moves by one (DP-09, R-UNI-40).
8. `rwb-decision` `AgentStepRecordValidator` checks the record against the ledger schema: the decision code is a value of LOV-DECISION read through DP-07, the rule ID carries its rule version, the agent version is of the legacy form "<agent>@<policy>/<prompt>" as the `rwb-agent` contract defines it, the inputs reference and the decided time are present, and the idempotency key is present and at most 80 characters. A record that fails is not chained: it is answered with MSG-P7-009 naming the field, held for the retry and dead-letter path with an alert, and the ledger gains nothing (GAP-2418; ASM-4026).
9. `rwb-decision` `AgentStepLedgerAppender`, in one transaction: takes the next `chain_seq`, sets `prev_hash` to the `entry_hash` of the entry before it (64 zeros for the first), computes `entry_hash` as the SHA-256 of the canonical form, and inserts the `decision_log_entry` row with the case reference, the decision code, the rule ID and version, the agent version, the model version, the inputs reference, the recommendation, the applied result as `final_call`, the actions with the fallback and the run id, `decided_at`, the producer identity in `actor_user_id` and the step key in `idempotency_key`; the inbox row commits with it. A key already on the ledger appends nothing, because the unique key of `idempotency_key` refuses a second row and the consumer treats the event as a repeat that returns the first entry id (R-UNI-40; TSD P7 v2 T3.1 DF-DEC-031).
10. A reader with Decision log R reads the ledger: `GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000201` returns the page of the case in scope and `GET /api/recovery/decision/v1/decision-log/{entryId}` returns the entry with its rule ID, rule version, agent version, model version, inputs reference, recommendation, final call, actions, decided time, previous hash, entry hash and chain sequence (API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1).
11. JOB-14 runs the chain verifier of the store slice over the ledger; an entry whose `entry_hash` does not match its canonical form, or whose `prev_hash` is not the `entry_hash` before it, is reported to Compliance the same day and no stored byte is rewritten (NFR-035; FSD P7 v3 A2.1.4.4). Its time of day and parameters are the store slice's (GAP-2420; ASM-4028).
12. Nothing else moves: this story changes no case state, no task, no timer, no agent run, no policy, no prompt and no model. The case stays where `rwb-case` has it, and the run stays as `rwb-agent` has it.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record arrives with a decision code outside LOV-DECISION, for example "D99" | Refused before any append with MSG-P7-009 naming "decisionCode"; nothing is chained, no `chain_seq` is consumed, and the read returns no entry for the step key | MSG-P7-009 | AC8 |
| X2 | A record carries a rule ID with an empty rule version, or an agent version that is not of the form the `rwb-agent` contract defines, or no inputs reference, or no decided time | Refused with MSG-P7-009 naming the field; nothing is chained and the entry is held for the retry and dead-letter path with an alert | MSG-P7-009 | AC2 |
| X3 | The local decision-record library cannot append the record inside the step's transaction | Nothing is committed on either side: the step does not act, the ledger holds no entry, no `chain_seq` is consumed, the outbox holds no event and one incident is raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X4 | The ledger store is unavailable when the record is ingested | Nothing is appended and no entry is invented; the event stays on the topic, the consumer retries on the platform back-off and the ledger catches up | None to a user; the alert is the platform's | AC6 |
| X5 | The same step key, or the same event ID, arrives again | One entry; the repeat appends nothing, returns the first entry id and moves the repeat count by one | None to a user | AC5 |
| X6 | The reader holds no Decision log right, or the entry id is unknown | 403 with MSG-P4-002 for the right, 404 for an unknown entry id; nothing is returned and no stored row changes | MSG-P4-002 | AC7 |
| X7 | An entry does not match the chain at the nightly check | The break is reported to Compliance the same day with its `chain_seq`; no byte of the ledger is rewritten and the entry stays readable | None to a user; the report is the store slice's | AC7 |
| X8 | The fallback payload carries a reason outside TIMED_OUT, SCHEMA and NO_POLICY | The record is chained as it arrived and the reason is not translated: this service adds no reason of its own, and the vocabulary of the reasons is the `rwb-agent` contract's | None to a user | AC4 |

A record is never updated and never deleted: a wrong record is corrected by a new record that names the one it corrects in `corrects_entry_id`, so the ledger stays append only (REQ-DRI-002; TSD P7 v2 T3.1 DF-DEC-029). The entry and its inbox row are always written together. The text of MSG-P7-009 and the identifiers and texts of the not-found answer and the chain-break report are Not specified in the source documents (GAP-2418; ASM-4026).

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_decision` baseline of RWB-P7-E1008-APP, the record library of RWB-PLT-E1027-CON, the reference-data contract of DP-07 and the published `rwb-agent` contract with its fake (DP-20, RWB-P10-TE013-CON); it runs no agent, writes no agent run and changes no case |
| Negotiable | The decision codes, the fallback vocabulary, the version labels and the message texts are list, contract and message values; the story fixes only the shape of the entry, the chain, the key, the refusals and the reads |
| Valuable | Every agent step is explainable from one entry by the rule and its version, the agent and model versions, the recommendation and the applied result, and the fallback rate is countable without a second store |
| Estimable | One listener, one validator, one appender, one query service, one controller pair, one repository and one migration; it fits one sprint with its tests as the secondary slice of the legacy key |
| Small | The decision-record half only: the client, the mode, the run, the prompt, the policy and the guardrails are other stories' and named in section 19 |
| Testable | Each criterion of section 7 is one automated test against the topic fixture, the reference-data fake, the agent-contract fake and a seeded chain, with a fixed clock |

The story is an APP story with no build dependency: the platform CON stories the patterns add are wave 0 and the one contract dependency is another service's published contract with its fake, so the build is not blocked (Template and Rules §R5.4 and §R5.7 rule 2; GAP-2419; ASM-4027).

### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback — the rwb-decision decision-record entry of an agent step

  Background:
    Given the environment is SIT
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"
    Given the decision code of the step is "D6" of LOV-DECISION read with its version in force
    Given the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" is the idempotency key of the record

  Scenario: AC1 An agent step gives one entry that names the rule, its version and the applied result (new, D-RCV-60)
    Given the decision-record library wrote the record of the SHADOW step on case "RW-2026-000201" with the rule result applied and fallback false
    When rwb-decision consumes the DecisionRecorded event of that step
    Then exactly one decision_log_entry row exists with idempotency key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    Then the entry names decision code "D6", rule "R-UNI-32", rule version "2026.11" and final call "RESUME_STATE", which is the next state of the rule result the client applied
    Then the entry carries an inputs reference, decided_at, prev_hash, entry_hash and chain_seq, and no agent answer as its final call
    Then GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000201 returns that one entry for the case, read as a Decision log R holder

  Scenario: AC2 The entry names the agent and model versions of the run, and holds none when no policy is in force (new, D-RCV-60)
    Given the record of the step on case "RW-2026-000201" names agent version "INTAKE@P1/PR1" and the model version the run names
    When the record is consumed
    Then the entry and GET /api/recovery/decision/v1/decision-log/{entryId} both answer agent version "INTAKE@P1/PR1" and that model version
    Then the entry requires a rule version beside its rule ID and an agent version of the form "<agent>@<policy>/<prompt>", and a record without them is refused with MSG-P7-009 naming the field and is not chained
    Given a step on case "RW-2026-000202" ran with autonomy mode "OFF", so no agent run exists and the record carries no agent version
    When that record is consumed
    Then its entry holds no agent version and no model version, final call "RESUME_STATE" and actions fallback false

  Scenario: AC3 The recommendation carries its confidence and the applied result stays the rule result (new, D-RCV-60)
    Given the record of the step on case "RW-2026-000201" was written with autonomy mode "L1" and the agent answer with confidence 0.91 as the recommendation
    When the record is consumed
    Then the entry holds the agent answer in recommendation with confidence 0.91, final call "RESUME_STATE" and actions fallback false
    Then the final call is the rule result and never the agent answer
    Given a second record of the same case was written with autonomy mode "SHADOW" and the same answer
    When that record is consumed
    Then its entry holds no recommendation and the answer stays on the run alone

  Scenario: AC4 A fallback is true with its reason and the run id in the actions (new, D-RCV-60)
    Given three records of agent steps of case "RW-2026-000201", each with its own step key, carry actions fallback true with reason "TIMED_OUT", "SCHEMA" and "NO_POLICY"
    When the three records are consumed
    Then three entries exist with final call "RESUME_STATE", the rule result applied in every one
    Then the actions of each entry hold fallback true, its reason, and the id of the agent run where a run exists
    Then the entry with reason "NO_POLICY" holds no agent run id, because no run was made
    Then no reason is translated or added by this service and a reason outside the three is chained as it arrived

  Scenario: AC5 A repeated step key gives one entry and one chain link (new, D-RCV-60)
    Given the entry with idempotency key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" is on the ledger
    When the same record is delivered again, and then the same event id is redelivered by the topic
    Then one decision_log_entry row exists for the key, the repeat appends nothing and the repeat count moves by one
    Then the repeat returns the first entry id and the chain gains no second link and no second chain sequence
    Then a second row for the same idempotency key is refused by the unique key of the ledger

  Scenario: AC6 A record that cannot be written stops the step and leaves no entry (new, D-RCV-60)
    Given the decision-record library cannot append the record of the step on case "RW-2026-000201"
    When the agent step runs
    Then the append answers with its unavailable condition carrying MSG-P7-003 and the step does not act, because the append is inside the step's transaction
    Then case "RW-2026-000201" stays in route state "NEW", the ledger holds no entry for the step key and no chain sequence is consumed
    Then no DecisionRecorded event reaches rwb.decision-record.v1 for the step and one incident is raised under R-UNI-39
    Given the ledger store is unavailable when a delivered record is consumed
    Then nothing is appended, the event stays on the topic for the retry path and no entry is invented

  Scenario: AC7 The entry is readable on the two reads and the chain covers it (new, D-RCV-60)
    Given the entry of the step on case "RW-2026-000201" is on the ledger at chain_seq 231, after an entry at chain_seq 230
    When a Decision log R holder sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the answer carries the decision code, the rule ID and version, the agent version, the model version, the inputs reference, the recommendation, the final call, the actions, decided_at, prev_hash, entry_hash and chain_seq
    Then prev_hash equals the entry_hash of the entry at chain_seq 230 and entry_hash equals the SHA-256 of the entry's canonical form
    Then the nightly JOB-14 chain check verifies the entry and reports any break of it to Compliance the same day without rewriting a byte
    When a role without the Decision log right sends the same read, then the answer is 403 with MSG-P4-002, and an unknown entry id answers 404 with nothing returned

  Scenario: AC8 The decision code is a list value and the fallback rate is countable from the entries (new, D-RCV-60)
    Given a record for the step on case "RW-2026-000201" carries decision code "D99"
    When it is consumed
    Then it is refused with MSG-P7-009 naming "decisionCode", nothing is chained, the chain stands at its last entry and the read returns no entry for the step key
    Given 120 entries of agent version "INTAKE@P1/PR1" were decided in November 2026, of which 9 carry actions fallback true
    When the ledger is counted by agent version and month
    Then the count returns 120 agent steps and 9 fallbacks and the rate 0.0750
    Then the rate is a read of these entries and neither the measure definition nor its threshold is written in this service
```

These eight criteria are new for the `rwb-decision` slice of RWB-TE-013 and are the decision-record criteria of the key; no legacy criterion of RWB-TE-013 is owned verbatim here, because every legacy criterion reads or gives the agent answer and belongs to RWB-P10-TE013-APP, so `acs` is empty for this story. The values are the legacy values of RWB-TE-013 sections 3, 4, 7 and 12 — case `RW-2026-000201`, route state "NEW", agent "INTAKE", policy "P1", prompt "PR1", agent version `INTAKE@P1/PR1`, timeout 60 seconds, answer in 2,000 ms, confidence 0.91, rule `R-UNI-32` version `2026.11`, next state `RESUME_STATE`, decision code `D6`, the step key `CASEWF:RW-2026-000201:ENTRY:2026-11-30`, the fallback reasons `TIMED_OUT`, `SCHEMA` and `NO_POLICY`, and the business date 2026-11-30 — and no new business value is introduced. Case `RW-2026-000202` is a synthetic second case of the same series, used only where a second step key is needed because one key yields one entry; the 120 entries and 9 fallbacks of AC8 are the rate the legacy story sets below 10 percent per month (RWB-TE-013 section 2), and their operation name is the placeholder of GAP-2424.

**Target reading.** The applied result is `final_call`, always the rule result's next state, so an agent answer can never be mistaken for the decision; the recommendation is the separate field the legacy mapping gave it. The fallback and the link to the run travel in `actions`, because no column of TSD P7 v2 T3.1 holds them: `decision_log_entry` has no agent run column and no reason column, and its `actions` is the jsonb of DF-DEC-014 (GAP-2417; ASM-4025). The code in the fixtures is `D6` because the agent step of the fixture sits in the route decision, and on a step with no policy in force no policy version and no prompt version exist, so the agent version is empty — a reading the legacy story fixes only for mode OFF (legacy AC8) and which is applied to NO_POLICY too (ASM-4025).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every agent step writes exactly one decision record, and no agent step exists without its record | REQ-DRI-001; REQ-DRI-005; R-UNI-39; legacy BR3 |
| BR2 | The decision code of the step is a value of LOV-DECISION read with the version in force; it is never a constant of the code and it is never defaulted by this service | TSD P7 v2 T3.1 (DF-DEC-003); FSD P7 v3 A2.2.4.3 (AC-EXC-P7-002-05); legacy section 12; DP-07; ASM-4025 |
| BR3 | The entry names the rule ID and the rule version of the rule result the client applied, and a rule ID without its version is refused | REQ-DRI-001; TSD P7 v2 T3.1 (DF-DEC-004, DF-DEC-005); FSD P7 v3 A2.3.4.3 (AC-EXC-P7-003-01); NFR-034 |
| BR4 | The applied result is `final_call`: the next state of the rule result, "RESUME_STATE" in the fixtures, and never the agent answer | Legacy section 12 (final_call = ruleResult.toState); TSD P7 v2 T3.1 (DF-DEC-012) |
| BR5 | The recommendation is the checked agent answer with the confidence the guardrail checked in L1, and empty in SHADOW and on a fallback, where the answer stays on the run | REQ-DRI-001; TSD P7 v2 T3.1 (DF-DEC-009); legacy AC1, AC3; legacy BR1 |
| BR6 | A step that fell back holds `fallback` true and its reason TIMED_OUT, SCHEMA or NO_POLICY in the actions; a step that did not holds `fallback` false; this service translates no reason and adds none | R-UNI-32; legacy AC2, AC4, AC5, AC8; the reason vocabulary is the `rwb-agent` contract's (DP-20) |
| BR7 | The entry is linked to the agent run by its id, held with the fallback and the mode in the actions of the entry; this service never writes `agent_run.decision_log_id`, which is `rwb-agent`'s column of its own table | Legacy section 12 (actions "agentRunId", "mode", "fallback", "fallbackReason"); DP-01; ASM-4025 |
| BR8 | The idempotency key of the entry is built from the step key of the agent step, held in `decision_log_entry.idempotency_key`, unique on its own: one step key yields one entry, a repeat returns the first entry and consumes no chain sequence | R-UNI-40; TSD P7 v2 T3.1 (DF-DEC-031); FSD P7 v3 A2.2.4.3 (AC-EXC-P7-002-03); legacy BR5; legacy AC7 |
| BR9 | The record is appended inside the calling step's transaction and before the step acts; a write that fails means the step does not act, the answer is MSG-P7-003 and an incident is raised | REQ-DRI-005; R-UNI-39; FSD P7 v3 A2.5.4.3 (AC-EXC-P7-005-02); legacy BR3; CTL-06; DP-03 |
| BR10 | The entry is read only on `GET /decision-log` and `GET /decision-log/{entryId}`, under the Decision log right R and the scope of the reader; the right is `rwb-access`'s answer and this service holds no role and no scope of its own | TSD P7 v2 T6.1, T6.2 and T-A.2 (API-P7-006, API-P7-007); FSD P7 v3 A2.1.4.3 (AC-EXC-P7-001-02); legacy section 10 |
| BR11 | The entry is append only and hash chained: `entry_hash` over its canonical form, `prev_hash` equal to the entry hash before it, a `chain_seq` never reused, no update and no delete, and the nightly chain check covers it | REQ-DRI-002; REQ-DRI-003; NFR-035; FSD P7 v3 A2.1.4.1 (AC-P7-001-01) and A2.1.4.2 (AC-ALT-P7-001-01) |
| BR12 | The agent version and the fallback fact sit on the same entry, so the agent fallback rate is countable from the ledger by agent version and month without a second store | RWB-TE-013 section 2 (below 10 percent per month); ASM-4032; GAP-2424 |
| BR13 | No personal data in the entry, the event, the trail or the logs: case and run identifiers, a decision code, version labels, a final call, statuses, reasons and dates only, and the inputs reference points at a masked snapshot | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43; REQ-ACA-005 |
| BR14 | No business value in code: the decision codes, the fallback vocabulary, the agent version form and the message texts are list, contract and message rows, never constants of this service | Template and Rules §R7.2 s17; DP-07; DP-20; FSD P7 v3 BR-P7-002 |
| BR15 | The append is never gated by a feature switch and never skipped for speed: an agent step without its entry is a defect, not a degraded mode | REQ-DRI-005; R-UNI-39; legacy section 13 (the switch of the client is the client's) |
| BR16 | A record that fails the ledger schema is not chained and is never repaired by this service: it is refused with MSG-P7-009 naming the field and held on the retry and dead-letter path with an alert, and the chain stays continuous | FSD P7 v3 A2.2.4.2 (AC-ALT-P7-002-01) and A2.2.4.3; DP-09; ASM-4026 |

### 9. State transitions

The states below are the states of one decision-record entry of an agent step. The case, the agent run, the policy, the prompt and the guardrail results are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A `DecisionRecorded` event arrives for an agent step | The code is in LOV-DECISION, the rule ID carries its version, the agent version is of the contract form, the inputs reference and the decided time are present, the key is present | Appended: one row with a `chain_seq`, a `prev_hash` and an `entry_hash`, and the inbox row in the same transaction |
| Absent | A record arrives with a field outside its rule | The validation refuses it | Absent: MSG-P7-009 naming the field, held for the retry and dead-letter path with an alert, and no `chain_seq` consumed |
| Absent | The same step key or the same event ID arrives again | The unique key of the idempotency column and the inbox hold | Appended: unchanged, the first entry id returned, the repeat count moved by one |
| Absent | The record library cannot append the record inside the step's transaction | The step's transaction rolls back | Absent: the step does not act, MSG-P7-003, an incident under R-UNI-39, and no event on the topic |
| Absent | The ledger store is unavailable on consume | The consumer retries on the platform back-off | Absent: the event stays on the topic and the ledger catches up |
| Appended | A later record arrives | The chain head has moved | Appended: the new entry names the previous hash of the head |
| Appended | A wrong entry must be corrected | A person decides the correction | Appended: a new entry with `corrects_entry_id` naming the wrong one; the wrong one stays |
| Appended | Any update or delete is attempted | Through the service role or the schema owner | Appended: refused by the append-only rule, and the attempt is written to the ACE audit log |
| Appended | The nightly chain check runs | The entry hash does not match its canonical form, or its previous hash is not the hash before it | Appended: unchanged and reported to Compliance the same day; nothing is rewritten |

The final call never moves between values through an update: a different outcome is a new entry. The case stays where `rwb-case` has it, and the run, the policy and the prompt stay as `rwb-agent` has them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The `rwb-decision` service identity | Consumes `DecisionRecorded`, writes its own `decision_log_entry` row, the chain link and the inbox row, and reads no schema of another service (the `rwb-decision` login, DP-02) |
| The decision-record library identity of the calling service | Appends the local record and writes the outbox row inside the caller's transaction and publishes on `rwb.decision-record.v1` (DP-03) |
| SY-CASEWF and the other calling service identities | Write the record of their own agent step through the library; they hold the C letter of the Decision log in the TSD matrix and write nothing in `rwb_decision` directly |
| SY-AGENT | Writes the run, the policy and the prompt in `rwb_agent`; in this story it holds the C letter only and writes no ledger row |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-CASEOWN, RW-TEAMMGR and every role with Decision log R of TSD P7 v2 T6.1 | Read the entry of an agent step in scope on the two reads and take no other action |
| RW-PLATADM | Receives the incident of a failed append and operates the service; reads the ledger under Decision log R |
| No role | Updates or deletes an entry, reads `agent_run`, `agent_policy` or `agent_prompt` from this service, or reads a service schema directly |

The authorisation decision is `rwb-access`'s and is consumed as the authorise answer the reads declare; the refusal stays 403 with MSG-P4-002 and the unknown entry id 404 of TSD P7 v2 T-A.2. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-2420; ASM-4028); the story refers to "the `rwb-decision` login (DP-02)".

### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write, the case reference held as a business key with no foreign key to `rwb_case` |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, a value of LOV-DECISION — "D6" in the fixtures, never a constant |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Write, "R-UNI-32" and "2026.11" from the rule result; a rule ID with an empty version is refused |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | model_version, agent_version | Write, the model version the run names and "INTAKE@P1/PR1", empty when no policy and prompt are in force |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the reference to the masked inputs snapshot |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the checked answer with confidence 0.91 in L1; empty in SHADOW and on a fallback |
| DF-DEC-010, DF-DEC-011, DF-DEC-013, DF-DEC-015 | `decision_log_entry` | approver_user_id, approval_level, override_reason, outcome | Not written: no person approved the step, an agent step carries no delegation level, overrides no recommendation of a person and has no outcome of its own |
| DF-DEC-012 | `decision_log_entry` | final_call | Write, "RESUME_STATE", the applied rule result |
| DF-DEC-014 | `decision_log_entry` | actions | Write, the run id, the mode, `fallback` and the reason; the key set is Not specified in the source documents (GAP-2417; ASM-4025) |
| DF-DEC-016, DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | decided_at, prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on an entry that corrects an earlier one |
| DF-DEC-030, DF-DEC-031 | `decision_log_entry` | actor_user_id, idempotency_key | Write, the producer identity and "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the key built from the step key, unique on its own |
| DF-DEC-001 to DF-DEC-031 | decision record | all fields | Read through the two decision-log operations |
| (inbox) | library table in `rwb_decision` | event_id, consumer, processed_at | Write, one row per consumed event |

No row of `agent_run`, `agent_policy`, `agent_prompt`, `agent_feedback`, `agent_sample`, `agent_alert`, `agent_evaluation` or `agent_evaluation_run` is read or written here: the run facts arrive inside the record the calling service wrote, and `agent_run.decision_log_id` stays `rwb-agent`'s column (DP-01, BR7). No row of `recovery_case`, `task`, `timer`, `queue`, `parameter_*`, `reference_*` or `lov_value` is written; LOV-DECISION is read through the reference-data contract of `rwb-case` (DP-07) and `lov_value` stays P3's. The outbox of this schema is not written by this story, because the ledger is the seal and publishes nothing. Field IDs are those in the Logical Data Model and Data Dictionary v9 and TSD P7 v2 T3.1.

The model version of agent "INTAKE" is named in no source (GAP-2421; ASM-4029): the legacy story copies it from the run and asserts no literal, so the entry copies whatever the run names and the tests assert equality with the run fixture rather than a literal.

### 12. Contract

#### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two reads are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1. No write operation is exposed: the write path of the entry is DP-03's — the local decision-record library inside the calling service, its outbox and the shared topic of 12.4 — so this service provides the reads and receives the record as an event.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the ledger by case, decision, rule, approver and date, one page at a time; the page of an agent step carries its code, rule and version, agent and model version, final call, actions and decided time | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs reference, rule ID and version, agent and model version, recommendation, final call, actions, decided time, previous hash, entry hash and chain sequence | Decision log, right R, scope applied | Not applicable, read only |

The request and answer field set beyond the fields TSD P7 v2 T3.1 names is Not specified in the source documents (GAP-2417; ASM-4025). Errors: 401 no session; 403 the role holds no Decision log right (MSG-P4-002); 404 an unknown entry id; 503 the ledger was not read. Every error is an RFC 9457 problem response with `messageId` set.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION with D1 to D9 and X1 to X7 and its version in force, for the decision-code check of the ingest (DP-07); faked, one hop, 2 s |

The operation is consumed on its published contract or its fake, one hop with a 2 s timeout and a breaker (DP-11, ADR-020). The authorise answer of `rwb-access` is not a REST row of the Ownership Map: it arrives through the platform guard the reads declare, and the guard contract is not in this story's metadata rows (GAP-2419; ASM-4027). This story reads no `rwb-agent` operation at run time: the agent facts arrive inside the record, and the `rwb-agent` contract is consumed as the definition of the version label and the fallback vocabulary (DP-20).

#### 12.3 Events published

None by this story. The ledger is the seal and writes no further event (Architecture v5 slide 28). The shared topic `rwb.decision-record.v1` is P7's and the schema of its event `rwb.decision-record.DecisionRecorded.v1` is defined by this story for the consumers of Architecture v5 slide 42 — `rwb-decision` itself and `rwb-reporting`. The service topic `rwb.decision.events.v1` and its events belong to the approval and registry slices of this service, not to this one. The legacy line "the client publishes none" is superseded by that topic (GAP-2422; ASM-4030).

#### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by each of the 19 services through its local library; topic and schema owned by P7 rwb-decision | Validates the record of the agent step, appends one `decision_log_entry` per step key and one inbox row in one transaction, and publishes nothing |

The payload carries the record: entry id, case reference, decision code, rule ID and version, agent version, model version, inputs reference, recommendation, final call, actions holding the run id, the mode, `fallback` and the reason, decided time, the producer identity and the idempotency key. The field set is the record shape of RWB-PLT-E1027-CON, and its key set is Not specified in the source documents (GAP-2417; ASM-4025). CloudEvents 1.0, key caseId, no personal field, dedupe on the event id through the inbox (DP-09, ADR-015). TSD P7 v2 T5.3 names `DecisionRecorded` as a published event of the module; the Ownership Map leaves its EV number open among the three P7 events (EV-08, EV-09, EV-30), so the EV number is Not specified in the source documents (GAP-2425; ASM-4033).

#### 12.5 Workflows and activities

None. The ingest is a Kafka consumer with an inbox and a local transaction, not a workflow; the two reads are queries. `rwb-decision` holds `ApprovalWorkflow` of the workflow kit and its rule-promote Schedule for other slices of the service; this story starts no workflow, signals none, registers no activity and puts nothing on the `rwb-decision` queue in namespace `rwb-recovery`.

#### 12.6 Schedules

None registered by this story. The chain check JOB-14 is a Temporal Schedule of the decision-log store slice and covers the entries of this story; the ledger copy is continuous ingest on Kafka and not a Schedule at all (Architecture v5 slide 44). The rule-promote Schedule JOB-20 is the registry slice's. The JOB-14 time of day, its timezone and its overlap policy are the store slice's and are Not specified in the source documents for this story (GAP-2420; ASM-4028).

#### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The entry of the agent step: the code, the rule and its version, the agent and model versions, the inputs reference, the recommendation, the final call, the actions, the decided time, the two hashes and the chain sequence; written once by the ingest and read |
| inbox library table | PLT library, created in `rwb_decision` | One row per consumed event (DP-09) |
| `approval`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, outbox library table, `idempotency_key` | P7 or PLT library, created in `rwb_decision` | Not used: an agent step raises no approval, this story evaluates and serves no model, the ledger publishes nothing and the step key is held on the ledger row itself |

Not owned and never read by this story: `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_feedback`, `agent_alert`, `agent_evaluation` and `agent_evaluation_run` (P10); `recovery_case`, `task`, `timer`, `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` (P3); `role`, `permission`, `delegation_limit` and `masking_rule` (P4). No foreign key crosses a schema and no row of another service is copied (DP-01).

#### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| `rwb-agent` contract fake | RWB-P10-TE013-CON (DP-20), which is not written yet | The run of case `RW-2026-000201` with agent "INTAKE", policy "P1", prompt "PR1", agent version "INTAKE@P1/PR1", the model version, mode SHADOW, status ANSWERED and confidence 0.91; runs with status TIMED_OUT and GUARDRAIL_FAILED and their reasons; the L1 answer; the OFF step with no run; the no-policy step on 2026-11-30; the request journal for the step key, the code and the ordering |
| rwb-case reference-data fake | The P3 list read of DP-07 | LOV-DECISION with D1 to D9 and their sub-decisions and X1 to X7, with its version in force; a variant without "D99" for AC8 |
| authorise fake | The P4 cached permission decision of the reads | The allow answer on the Decision log right R and the scope for the reader of AC7; the refusal of the right for a role that holds Case record R only (GAP-2419; ASM-4027) |
| decision-record library fake | RWB-PLT-E1027-CON | The record of an agent step with its canonical form and hash, the chain link and the outbox row; a forced append failure and an unavailable condition for AC6 |
| Ledger store fixture | RWB-P7-E1008-APP | A seeded chain of 230 entries with their hashes and sequences, the append-only rule, and a chain verifier that reports the altered entry of AC7 |

Each fake is replaced by the real contract as it lands, without a change to the criteria. The `rwb-agent` fake stands only for the facts of the record, because this story calls no agent operation at run time.

#### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 1 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the P3 reference-data list read consumed, one hop with the 2 s timeout; the authorise answer arrives through the platform guard (GAP-2419) |
| Kafka | Published 0, consumed 1 event type | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, CloudEvents 1.0, key caseId, dedupe through the inbox (DP-09, DP-14) |
| Temporal | None | No workflow, no activity and no Schedule registered; JOB-14 stays with the store slice and JOB-20 with the registry slice |
| File | None | No file input and no file output; the daily ledger seal is another slice's |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger/agentstep`, Java package `th.co.scb.ace.workbench.recovery.decision.agentstep`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

How this story applies each row. **DP-01** keeps the entry in `rwb_decision` alone, the case reference an opaque key and the run facts inside the record (BR7). **DP-03** is the core: the legacy `DecisionLogWriter` becomes the local library of the calling service plus the shared topic, and this service is the collector that chains the same facts centrally. **DP-04** is carried and not used, and `C RWB-P7-E1073-CON` is this service's own contract, so it is same-service here. **DP-07** is where the decision code lives, read with the version in force (BR2). **DP-09** gives the inbox that makes a redelivery write no second entry (BR8). **DP-10** is carried and not used, because the ledger copy is continuous ingest and JOB-14 belongs to the store slice. **DP-11** is the one consumed call, one hop and 2 s. **DP-13**, **DP-15** and **DP-19** put the reads on the service base, the migration in the per-service sequence and the reads behind the composite route, and this story adds no route and serves no screen.

**DP-20** is the story's contract dependency: the agent version label, the model version and the fallback vocabulary of the entry are the `rwb-agent` contract's definitions, so the record cannot be validated without it. RWB-P10-TE013-CON is not written yet; this story is built against the published DP-20 contract row and its fake, which stands in until the contract lands (ASM-4027).

The H and C dependencies the pattern table adds — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, and C RWB-P3-E1043-CON — are not in the metadata rows of this story, which name None and RWB-P10-TE013-CON. They are recorded in GAP-2419 and ASM-4027, together with the authorise answer of `rwb-access` that no pattern of this story names. **Ready to start stays Day 1**: each H is a platform CON story of wave 0 or this service's own baseline, the one C is another service's published contract with its fake, and none of them blocks the build of an APP story (Template and Rules §R5.7 rules 2 and 8).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionRecordListener | Listener | Consumes `rwb.decision-record.DecisionRecorded.v1`, writes the inbox row, treats a held event ID as a repeat and answers the first entry id |
| AgentStepRecordValidator | Service | Reads LOV-DECISION with its version in force and checks the code, the rule version beside its rule ID, the agent version form of the `rwb-agent` contract, the inputs reference, the decided time and the key; refuses with MSG-P7-009 naming the field |
| AgentStepLedgerAppender | Service | One transaction: the next `chain_seq`, the previous hash, the entry hash over the canonical form, the `decision_log_entry` row and the inbox row, or nothing |
| AgentStepKeyGuard | Service | Builds and holds the idempotency key of the step key, refuses a second row through the unique key and returns the first entry on a repeat |
| DecisionRecordController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the guard, the scope, the page and the problem mapping for 401, 403, 404 and 503 |
| DecisionRecordQueryService | Service | The page and the single entry, with the scope filter of the authorise answer and the two hashes of the chain; it also counts entries and fallbacks by agent version and month |
| DecisionRecordRepository | Repository | `decision_log_entry` in `rwb_decision`, with the unique keys of `idempotency_key` and `chain_seq` and the indexes of the agent-step read and the count |
| ReferenceDataClient, GuardClient | Clients | The LOV-DECISION read of DP-07 and the cached authorise answer of the reads, one hop each with a 2 s timeout and a breaker |

**Database and migrations**

- Writes `decision_log_entry` and the inbox object of the library, all in schema `rwb_decision`; reads no other schema.
- The `decision_log_entry` baseline, its append-only trigger, its grants, the canonical form, the chain verifier and JOB-14 belong to the decision-log store slice of this service (legacy RWB-E1-008, RWB-P7-E1008-APP) and are not rebuilt here.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2026_11_02__declog_agent_step_profile.sql` adds the index `ix_declog_agent_step ON decision_log_entry (agent_version, decided_at DESC) WHERE agent_version IS NOT NULL` for the agent-step page and the fallback count, the expression index `ix_declog_fallback ON decision_log_entry ((actions->>'fallback')) WHERE actions ? 'fallback'`, and the check `ck_declog_agent_step_code CHECK (decision_code IS NOT NULL)`. No column is added: the fallback fact and the run id live in `actions` (ASM-4025), and the unique key of `idempotency_key` already exists on the baseline.
- No row is updated and no row is deleted by this story; the update path of the store does not exist and the delete path does not exist.

**Configuration and reference data**

- LOV-DECISION and its version in force are read through the reference-data contract of DP-07; `D6` and the sub-decisions are values of that list and never constants in code (ASM-4025).
- The fallback vocabulary TIMED_OUT, SCHEMA and NO_POLICY, the agent version form "<agent>@<policy>/<prompt>" and the model version are the `rwb-agent` contract's; this service validates the form and records the value, and translates neither (DP-20).
- The 80 character limit of the key is the column length of `idempotency_key` (DF-DEC-031) and the step key of the fixtures is 38 characters. The `rwb-decision` login of DP-02, the Flyway user, the consumer group and the environment names are configuration and their values are Not specified in the source documents (GAP-2420; ASM-4028).
- The feature switches of the client, `rwb.agent.client` among them, stay with RWB-P10-TE013-APP and are not read here: an entry that could be switched off would break R-UNI-39 (BR15).

**Build steps**

1. The migration `V2026_11_02__declog_agent_step_profile.sql` with the two indexes and the check; test that a second row for the same `idempotency_key` and for the same `chain_seq` is refused by the constraints (BR8, BR11, AC5).
2. `AgentStepRecordValidator` with the LOV-DECISION read of DP-07 and the agent version form of the `rwb-agent` contract fake; tests for AC2, AC8 and the refusals of X1 and X2.
3. `AgentStepLedgerAppender` and the chain link over the seeded ledger of 230 entries, with `AgentStepKeyGuard` and the repeat path; tests for AC1, AC5 and AC7, including the first entry with a previous hash of 64 zeros.
4. `DecisionRecordListener` with the inbox, the retry path and the dead-letter alert; tests for the redelivery of AC5 and the unavailable store of AC6.
5. `DecisionRecordController` and `DecisionRecordQueryService` with the authorise answer, the scope, the page, the 403 and 404 refusals and the fallback count by agent version and month; tests for AC7 and AC8, with 120 entries and 9 fallbacks.
6. The privacy test: the entry, the event payload and the log lines carry no name, e-mail address, mobile number, national identity number or account number, and the answer text never enters this service (AC1, AC3).

**Done when.** The ten test cases of section 16 pass, the contract tests of the `rwb-agent` fake stay green, and a SIT day shows one entry per step key with the rule and its version, agent version "INTAKE@P1/PR1", the model version of the run, final call "RESUME_STATE", the recommendation with 0.91 in L1 and `fallback` true with its reason on the three fallback steps; a chain that verifies from its first entry; no entry and no chain sequence when the record cannot be written; one entry for a repeated key; and a fallback count of 0.0750 for the month of the fixture.

### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The record cannot be written and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append condition; the client carries it to the caller |
| MSG-P7-009 | The decision code is not a value of LOV-DECISION, the rule version or the agent version is missing beside its identifier, or the inputs reference or the decided time is absent | Not specified in the source documents (GAP-2418; ASM-4026) | This story, on the validation; FSD P7 v3 A2.2.4.2 and A2.2.4.3 name only the identifier and the field |
| MSG-P4-002 | The reader holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of `rwb-access` |

MSG-P7-003 is copied unchanged from RWB-TE-013 section 14 and from FSD P7 v3 A2.2.3.1 (VR-P7-002-2); MSG-P4-002 is the platform message the authorise contract carries; MSG-P7-009 is named by FSD P7 v3 A2.2.4.2 and A2.2.4.3 and its text is written out in no source this story may read, so the placeholder stands. This story adds no message ID. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story. The decision-log query screen SCR-38 and the decision list of a case belong to the screen slices of this service, and the agent monitor SCR-46 with its fallback rate belongs to RWB-P10-TE013-APP and its dashboard slice; this story neither renders nor hides them and adds no composite route (DP-19).

| Where | State | What the reader sees |
|---|---|---|
| `GET /decision-log` | One page or an empty page | The entries of a case in scope with the decision code, the rule and its version, the agent version, the final call and the decided time; an empty page when no agent step of the case was recorded, and the read invents none |
| `GET /decision-log/{entryId}` | One entry | Code "D6", rule "R-UNI-32" version "2026.11", agent version "INTAKE@P1/PR1", the model version, the recommendation with confidence 0.91 in L1, final call "RESUME_STATE", actions with `fallback` and the run id, decided time, previous hash, entry hash and chain sequence — and, for a fallback step, actions `fallback` true with its reason |
| `GET /decision-log`, `GET /decision-log/{entryId}` | 403 or 404 | MSG-P4-002 for a role without the right, nothing for an unknown entry id |
| The step, seen from the outside | Not recorded | The step does not act and the case stays where `rwb-case` has it; this service shows nothing because it stored nothing |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-09 | AC7, BR10 | Component | A role that holds Case record R only calls the two reads; 403 with MSG-P4-002; an unknown entry id is 404 |
| TC-TE-013-01 | AC1, AC2, AC3, BR3, BR4, BR5 | Component | Case RW-2026-000201, mode SHADOW, answer in 2,000 ms, agent version INTAKE@P1/PR1; one entry with rule R-UNI-32 version 2026.11 and final call RESUME_STATE |
| TC-TE-013-02 | AC4, BR6 | Component | Agent silent for 61 seconds; actions fallback true with reason TIMED_OUT and the run id; final call RESUME_STATE |
| TC-TE-013-03 | AC3, BR5 | Contract | Mode L1, confidence 0.91; recommendation holds the answer with 0.91 and the final call stays the rule result |
| TC-TE-013-04 | AC4, BR6 | Component | An answer that fails check SCHEMA; actions fallback true with reason SCHEMA |
| TC-TE-013-05 | AC4, BR6 | Component | No approved policy on 2026-11-30; actions fallback true with reason NO_POLICY, no run id and no agent version |
| TC-TE-013-06 | AC6, BR9 | Component | The record library throws on the append; MSG-P7-003, no entry, no chain sequence, no event, an incident under R-UNI-39 |
| TC-TE-013-07 | AC5, BR8 | Contract | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice and a redelivered event id; one entry, the first entry id returned, one chain link |
| TC-TE-013-08 | AC2, BR7 | Component | Mode OFF on case RW-2026-000202; no run, no agent version and no model version on the entry, actions fallback false |
| TC-TE-013-10 | AC6, BR9, BR15 | NFR | The append forced to fail during a SHADOW step; the step does not act, MSG-P7-003, the ledger at its last entry, an incident |

The ten test-case IDs are the legacy IDs of RWB-TE-013, kept unchanged and in their legacy order: their Covers cell names the record fact each one now proves on this side of the split, because the client behaviour itself is proved in RWB-P10-TE013-APP and across services in RWB-ITG-TE013-ITG, whose copies carry the `-ITG` suffix. The legacy level System maps to Component or Contract as the rows show, Access to Component and Resilience to NFR; the full test is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the decision code, the fallback vocabulary, the agent version form and the message texts are list, contract and message rows, read or validated but never written as a constant here (BR2, BR14).
- No personal data in the entry, the event payload, the trail, the tests or the logs: case and run identifiers, a decision code, version labels, a final call, statuses, reasons and dates only; the inputs reference points at a masked snapshot and the answer text never enters this service (BR13).
- No read of another service's tables (DP-01): no `agent_run`, `agent_policy`, `agent_prompt`, `recovery_case`, `role`, `permission`, `delegation_limit` or `lov_value` row is read or copied, and the authorise answer and the list read arrive on their contracts.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all. One recorder and no mover: it changes no case status, no task, no timer, no run and no policy, so an entry can never move a case.
- An entry without its event and an event without its entry are both impossible: the record is appended inside the step's transaction before the step acts, and the ledger entry and its inbox row commit together (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist, the chain sequence is never reused, and a wrong entry is corrected by a new one naming the one it corrects (REQ-DRI-002, BR11).
- One entry per step key: the unique key of the idempotency column makes a second entry impossible and a repeat returns the first (BR8, R-UNI-40). A record that fails the schema is refused and held, never repaired and never defaulted (BR16).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` for the other slices of the service and `rwb.decision-record.v1` for the record, `rwb-decision` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own (DP-13).
- One hop and 2 s on every consumed call, with a breaker per downstream; a missing answer never produces an entry from a guessed code or a guessed version (DP-11, ADR-020). The record path is never gated by a feature switch and never skipped for speed (BR15).

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions, the inputs, the recommendation, the actions and the outcome | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.7 | FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-03; legacy FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-03, TC-TE-013-07 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.7 | FEAT-DRI-05; legacy FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, TC-TE-013-10 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Business Requirements Program, section 5.4; Business Requirements Epic 1, section 3.9 | FEAT-DRI-02; legacy FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, TC-TE-013-08, TC-TE-013-09 |

| Legacy reference | Where it is kept |
|---|---|
| One decision record per agent step, with the rule ID, rule version, agent version, model version, recommendation, applied result and fallback | Sections 1, 2, 4, 7 (AC1 to AC4), 8 (BR1 to BR7) |
| The step key as the idempotency key and one entry for a repeated step | Sections 7 (AC5), 8 (BR8), 16 (TC-TE-013-07) |
| MSG-P7-003, R-UNI-39 and the step that does not act; MSG-P4-002, the Decision log right and the scope | Sections 5 (X3, X6), 7 (AC6, AC7), 8 (BR9, BR10), 10, 14 |
| The legacy values INTAKE, P1, PR1, INTAKE@P1/PR1, RW-2026-000201, R-UNI-32 2026.11, RESUME_STATE, the step key, 60 seconds, 0.91 and 2,000 ms | Background and scenarios of section 7; section 3 |
| Legacy key RWB-TE-013, story RWB-P7-TE013-APP, contract RWB-P10-TE013-CON, test cases TC-TE-013-01 to TC-TE-013-10 and the eleven decoupling patterns | Metadata, sections 3, 12, 13 and 16 |

The other slices of the key answer the rest: RWB-P10-TE013-CON and RWB-P10-TE013-APP own the client, the mode, the shadow and L1 behaviour, the orchestrator call, the timeout, the policy and prompt versions, the guardrails, the run and the model registry; RWB-P10-TE013-OPS the operations of `rwb-agent`; RWB-E1-058 the agent platform; RWB-ITG-TE013-ITG the proof across the real services; and the store slice of `rwb-decision` (legacy RWB-E1-008) the append-only table, the chain verifier and the nightly chain check.

### 19. Out of scope

- The client itself: the published interface, the autonomy mode of the step, the SHADOW and L1 behaviour, the orchestrator call, the 60 second timeout, the policy read, the guardrail checks, the agent run and its status, the prompt, the model and its registry, the fallback decision and the fallback vocabulary — RWB-P10-TE013-CON (the contract and its fakes), RWB-P10-TE013-APP (the runtime), RWB-P10-TE013-OPS (the operations) and the agent platform of RWB-E1-058. This story records their facts and derives none of them.
- The agent policy, the prompt store, the sample and evaluation harness, the monitoring dashboard SCR-46 and the fallback rate as a published measure: `rwb-agent` (P10) and the measure definition of `rwb-reporting` (P9). This story makes the rate countable and does not define, publish or threshold it (GAP-2424; ASM-4032).
- The decision-log store of this service — the append-only trigger, its grants, the canonical form, the chain verifier and the nightly chain check: the store slice of `rwb-decision` (legacy RWB-E1-008, RWB-P7-E1008-APP) and the service baseline.
- The screens of the decision log and of the agent monitor, the approval routing, the delegation of authority, the decision center screens and the rule package registry: the screen, approval and registry slices of `rwb-decision` and of `rwb-agent`, with the gateway-bff route of RWB-PLT-N001-CON.
- The case record, the case status, the route state, the task and the timer (`rwb-case`, P3), the role, the scope, the masking policy and the authorise answer (`rwb-access`, P4), and the cross-service harness with its `-ITG` copies of the test cases (RWB-ITG-TE013-ITG).
- The DB, INF and OPS stories of this legacy key: their own stories; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability are the OPS story's. The daily ledger seal to immutable storage and the lake copy are another slice's, and the lake is removed (DP-17).

The names of the holders of a role and the parameter values of the lists are data of their owners, and no date is changed by this story: the release 30 November 2026 is copied unchanged and stays tentative.
