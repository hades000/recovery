# RWB-P6-E1073-APP Rule authoring, validation, test scenarios, approval and rollback in Drools

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P6-E1073-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-comms |
| Service epic | RWB-SVC-P6 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-073 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP10, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-P6-J |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P3-E1073-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md (no FR mapped to REQ-CWC-013, REQ-CWC-014, REQ-DRI-004, REQ-CWC-008) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-073 for rwb-comms. Rule governance (authoring, the load checks, the 50-scenario gate, four-eyes approval, effective dating, one-call rollback and the central decision ledger) is central in rwb-decision (P7) and the authoring of the ALLOCATION package stays with rwb-case (P3); this story carries only the local copy and the evaluation of the package rwb-comms is assigned: the model fetched on `RulePackageInForce` through `GET /rule-models/{n}/{v}`, the SHA-256 verified, the KieBase compiled and swapped in atomically in the embedded Drools kit under the 300 ms budget, the package scenario set re-run locally, the last good copy kept on any failure and the version stamped on every answer. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-P6-E1073-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **rwb-comms service identity (the SY-RULES evaluator inside rwb-comms)**, I want **the approved version of the rule package this service is assigned fetched from rwb-decision when `RulePackageInForce` arrives, its SHA-256 checksum verified, the KieBase compiled and swapped in as one step from a registry that holds at most 20 versions, the package's scenario set re-run locally through the same evaluator, the evaluated copy kept with its version and checksum, and a registry rollback followed on the next event**, so that **the rules that drive the notices of this service run inside the service inside the 300 ms budget, a version that fails the checksum or a scenario never reaches a decision, and every answer names the package code, the version and the rule ID that decided it**.

### 2. Business rationale

Collection and recovery rules live in procedure documents, and audit found the procedure not followed because the rules were not in the system (CTL-08). RWB-E1-073 carries the control to Drools in the monolith: the workbook is the source of the decision table, the engine compiles it, a scenario set gates the load, Risk signs it, the version takes effect on its date and a rollback takes one call. The measure the legacy story sets is unchanged: every version in force has a passing scenario set and a checksum, and a wrong version leaves production in one call.

In the target the key splits along the service boundary and this story carries one slice of it. Architecture v5 slide 27 puts governance centrally in rwb-decision (authoring, test scenarios, four-eyes approval, effective dating, audit of every version) and evaluation locally in the one service that owns each model, which loads the model, verifies the checksum and swaps it atomically, keeping the last good model if a new one fails to load, so no shared rule server sits on the hot path. The Temporal and Drools design fixes the mechanics: the version stores its workbook, generated DRL and SHA-256 (slide 15); `GET /rule-models/{n}/{v}` fetches the model, the checksum is verified and the model swapped in (slide 15); `KieBaseRegistry` holds one KieBase per package version with an LRU of 20 and never recompiles per call (slide 16); first match decides with the rule ID written on the decision record (slide 16); evaluation runs only inside a Temporal activity (slide 14). The integration story draws the boundary this story must respect: rwb-case owns the authoring, the ALLOCATION evaluation and its local copy, rwb-decision owns the registry, the four-eyes approval, the effective date and the central decision ledger, rwb-integration owns its own local copy, and rwb-comms owns "the local copy and the evaluation of the package each service is assigned" (RWB-ITG-E1073-ITG section 10).

So this story is the rwb-comms side of DP-04 and of R-UNI-38 and it authors, approves, dry-runs and rolls back nothing. It writes and reads only schema `rwb_comms` (DP-01, DP-15), it calls one operation of rwb-decision for the model and no operation that changes the registry, it reads its parameters and its reference data through rwb-case (DP-06, DP-07), it runs inside an activity on queue `rwb-comms` (DP-10), it writes the local decision record and publishes `DecisionRecorded` on the shared topic of its owner (DP-03), and its screens come later through gateway-bff (DP-19). It serves REQ-CWC-013 (a validated load with a version and a one-call rollback, here seen from the consumer), REQ-CWC-014 (the scenario set gates the version before it decides anything), REQ-DRI-004 (records use versioned rules) and REQ-CWC-008 (the package always has a default row, so a local scenario set can never pass without one).

The split of the legacy key is recorded in section 19. Nothing in this story may be read as a licence to author, approve, dry-run or roll back a package: those are rwb-decision's, and the ALLOCATION evaluation on the case is rwb-case's.

### 3. Preconditions

- The embedded Drools kit of DP-04 is in the rwb-comms release: the compiler, the KieBase registry with `drools.kiebase.cache.max` (20) slots, one `RuleEvaluator`, and the `EvaluateRules` and `RecordAndApply` activities on queue `rwb-comms` (Arch v5 slide 27; Temporal and Drools design slides 14, 15 and 16). The DP table adds `H RWB-PLT-E1072-CON` for the kit while the plan sets "Depends on (build)" to None; the missing H row is carried as a gap and the kit is read as a platform prerequisite of the wave-0 train (GAP-1218; ASM-2172).
- rwb-decision serves the model fetch `GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` for an APPROVED or an IN_FORCE version, with the model and its SHA-256 checksum. The operation is named on Architecture v5 slides 14 and 27 as `GET /rule-models/{n}/{v}` and is in neither the Ownership Map nor API Specification v4, so its path segments, its request fields and its response fields are Not specified in the source documents (GAP-1217; ASM-2171).
- The plan's contract dependency RWB-P3-E1073-CON is published for this story and is built against as a contract. The DP-04 row of §R5.5 names `H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON` instead; the conflict is recorded and the given list is followed (GAP-1215; ASM-2172).
- The topic `rwb.decision.events.v1` exists with its retry and `.dlt` topics and rwb-comms consumes `rwb.decision.RulePackageInForce.v1` from it, deduped in its own inbox (Arch v5 slides 20 and 43 row 30; DP-14).
- The parameters `rules.testcases.min` (50) and `drools.kiebase.cache.max` (20) are in force in the rwb-case catalog and are read through the parameters contract of rwb-case, never written in code (RWB-E1-042 as at 16 November 2026; DP-06). The parameter codes are the legacy names and the read path is Not specified in the source documents (GAP-1214; ASM-2175).
- The package code this service is assigned, its version labels and its target queues are reference data read through the reference-data contract of rwb-case (DP-07). No source read here names the package of rwb-comms, so the story is built and tested on the legacy ALLOCATION fixtures `ALLOCATION`, `ALLOC-2026.11`, `ALLOC-2026.12`, `ALLOC-2026.13` and `TRF-2026.11` as synthetic test data (GAP-1216; ASM-2170).
- Schema `rwb_comms` and the rwb-comms login exist (DP-01, DP-02). The login name is allocated by the platform database story and is not fixed here.
- The local copy, the inbox, the outbox and the local decision record have their rows in `rwb_comms`; the table name and the columns of the local copy are Not specified in the source documents (GAP-1214; ASM-2173).
- The 300 ms budget is NFR-011 (a rule evaluation completes in under 300 milliseconds at the 95th percentile) and the client budget of every consumed call is 2 s (DP-11, ADR-020).
- The release date 30 November 2026 is tentative; a date is not a condition of this story. The story carries no build dependency and is Day 1 by the lane rule (§R5.7).

### 4. Flow

1. rwb-comms: on start, reads the package code it is assigned and the version labels it may hold through the reference-data contract, and reads `rules.testcases.min` (50) and `drools.kiebase.cache.max` (20) through the parameters contract. No package code, version label, target queue or role is written in code (DP-06, DP-07).
2. rwb-comms: reads the local copy in `rwb_comms`; when no copy is verified it starts with no model in the registry and every evaluation that needs the package answers "no package in force" to the caller instead of inventing an answer.
3. rwb-decision: the 00:01 promote run (JOB-20) puts a version in force and publishes one `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1`, naming the package code, the version label, its SHA-256 checksum and its valid-from date (Arch v5 slides 27, 43 and 44; Temporal and Drools design slide 15).
4. rwb-comms: reads the event through the inbox `processed_event`; a CloudEvents id already processed is skipped and nothing is loaded twice.
5. rwb-comms: fetches the model through `GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` with the 2 s client budget, and reads the model, its stored checksum and its state from the answer.
6. rwb-comms: refuses the version when its state is not APPROVED at the registry, when the label is unknown, when the answer is empty, or when the version's valid-from date has not been reached; the local copy in force does not change and no KieBase is compiled.
7. rwb-comms: verifies the SHA-256 of the fetched model against the checksum named by the event and by the version. A mismatch refuses the load before any compile; the previous copy stays in the registry and in `rwb_comms`.
8. rwb-comms: compiles the KieBase from the fetched model and runs the package's scenario set — at least `rules.testcases.min` (50) scenarios stored with the version — through the same `RuleEvaluator` as production. Any failing scenario, compile error, overlap, unreachable row or a missing default row refuses the load whole.
9. rwb-comms: swaps the verified KieBase in as one step and records the local copy with its package code, version label, checksum and load time, releasing the previous copy into the LRU ring of at most 20 versions. An answer taken during the swap names either the old version or the new one, never a half-loaded model.
10. rwb-comms: marks the inbox row processed and, on any refusal, writes the local run record naming the package, the version, the failing check and the row, cell or scenario IDs, and leaves the event unprocessed so the consumer retries and the next `RulePackageInForce` repeats the attempt.
11. A capability of rwb-comms that needs a rule answer: the workflow calls the `EvaluateRules` activity on queue `rwb-comms` with the package code, the facts and the business date; the activity evaluates the verified local copy, first match, under the 300 ms budget, and returns `RuleResult` with the package code, the version, the rule ID and its outputs. Drools is never called in workflow code.
12. rwb-comms: `RecordAndApply` writes, in one transaction in `rwb_comms`, the local decision record with the rule ID and the version, the state change and the outbox row, and the local decision-record library publishes `DecisionRecorded` on `rwb.decision-record.v1` (DP-03). A failed record means nothing moves.
13. rwb-comms: when rwb-decision rolls a version back in one call and publishes one `RulePackageInForce` naming the restored version, steps 4 to 9 run again and the restored version is fetched and swapped back; a case decided under the rolled-back version keeps that version on its decision record, because open cases keep the version they were decided under (R-UNI-38).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The SHA-256 of the fetched model does not match the checksum named by the event and by the version | Load refused before any compile; the previous copy stays in use | MSG-P3-027, check checksum | AC2 |
| X2 | A scenario of the package's local set returns a different result from its expected queue or outcome | Load refused whole; the failing scenario IDs named; the compiled KieBase discarded | MSG-P3-027, check scenario | AC3 |
| X3 | The fetched model does not compile, or a row is unreachable, overlaps another or the default row is missing | Load refused whole; the row, cell or scenario named; nothing swapped | MSG-P3-027, check compile, overlap, unreachable row or default row | AC3 |
| X4 | The version state at the registry is not APPROVED, the version is REFUSED, the label is unknown, or the answer is empty | Load refused; the local copy in force unchanged | MSG-P3-027, check package state | AC4 |
| X5 | The version's valid-from date has not been reached on the evaluation business date | Load refused; the version in force stays | MSG-P3-027, check package state | AC4 |
| X6 | The registry rolls a version back | One `RulePackageInForce` names the restored version; the local copy swaps back; earlier decisions keep their version | None | AC5 |
| X7 | The model fetch answers 503, times out beyond the 2 s budget or answers nothing | No swap; the previous copy stays in use; the event stays unprocessed and the next event retries; the failure is in the local run record | MSG-GEN-006 | AC6 |
| X8 | The same `RulePackageInForce` is delivered twice | The second delivery is skipped by the inbox; nothing is loaded twice and every answer still names one version | None | AC1, TC-E1-073-10 |
| X9 | The local decision record cannot be written for an evaluation | The answer is not applied; nothing moves; an incident is raised under R-UNI-39 | MSG-P7-003 | TC-E1-073-01 (the record and the outbox row in one transaction), section 14 |
| X10 | A caller without the read right asks for the local copy or calls the model fetch | Refused at the edge and by the contract; the local copy is unchanged | MSG-P4-002 | TC-E1-073-16, TC-E1-073-20 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the published model fetch and the parameters and reference-data fakes; rwb-case, rwb-decision and rwb-integration are not touched in code, and no registry operation is implemented here |
| Negotiable | Which package this service is assigned, which rows, queues and scenarios it holds, and the cache size and scenario minimum are data or parameters; the checksum check, the load order, the refusals and the swap are fixed |
| Valuable | A rule change reaches the notices of this service as tested, approved, dated data with no release, a bad or half-loaded version can never decide anything, and a rollback is followed without a code change |
| Estimable | One model fetch client, one checksum verifier, one KieBase registry, one scenario runner, one inbox listener, one local copy row and two activities |
| Small | Fits two weeks with its tests |
| Testable | Every criterion is a component or contract test with synthetic fixtures, a Kafka fixture and a fetch fake, and every cross-service value has a named fake |

### 7. Acceptance criteria

```gherkin
Feature: Local rule package copy and evaluation in rwb-comms

  Background:
    Given the rwb-comms schema is rwb_comms with queue rwb-comms and topic rwb.comms.events.v1
    Given the rwb-case contract mock returns the package code assigned to rwb-comms as "ALLOCATION" on the reference-data contract
    Given the local copy of package "ALLOCATION" version "ALLOC-2026.11" is verified and in use with 24 rows and its SHA-256 checksum
    Given the rwb-case contract mock returns rules.testcases.min as 50 and drools.kiebase.cache.max as 20 on the parameters contract

  Scenario: AC1 An APPROVED version is fetched, its checksum verified and the KieBase swapped in inside the 300 ms budget (new, D-RCV-60)
    Given rwb-decision publishes rwb.decision.RulePackageInForce.v1 for package "ALLOCATION" version "ALLOC-2026.12" on rwb.decision.events.v1 at 00:01 on 2026-12-15
    Given the rwb-decision contract mock returns the model of package "ALLOCATION" version "ALLOC-2026.12" in state APPROVED with 26 rows, its generated DRL and the SHA-256 checksum "9f2c...e1b4"
    When rwb-comms reads the event once through its inbox processed_event
    Then the system fetches the model through GET /api/recovery/decision/v1/rule-models/ALLOCATION/ALLOC-2026.12 with the 2 s client budget
    Then the SHA-256 of the fetched model equals "9f2c...e1b4" and the KieBase is compiled from it
    Then the 50 scenarios stored with the version run locally through the same evaluator and 50 of 50 pass
    Then the KieBase is swapped in as one step and the local copy is recorded with version "ALLOC-2026.12" and checksum "9f2c...e1b4"
    Then an answer taken at the moment of the swap names "ALLOC-2026.11" or "ALLOC-2026.12", never a partially loaded model
    Then a synthetic case with product group "MORTGAGE" and region "BKK" answers rule ID "ALLOC-014" and queue "MTG-BKK-CO" with version "ALLOC-2026.12"
    Then the evaluation completes inside the 300 ms activity budget
    When the same event is delivered a second time
    Then the inbox skips it, nothing is loaded twice and every answer still names exactly one version

  Scenario: AC2 A checksum mismatch is refused before any compile and the previous copy stays in use (new, D-RCV-60)
    Given rwb-decision publishes RulePackageInForce for package "ALLOCATION" version "ALLOC-2026.13" naming checksum "9f2c...e1b4"
    Given the rwb-decision contract mock returns the model of "ALLOC-2026.13" whose SHA-256 is "7a10...c9d2" and does not equal the checksum named by the event and by the version
    When rwb-comms fetches the model and verifies the checksum
    Then the local load is refused with MSG-P3-027 for the checksum check naming package "ALLOCATION", version "ALLOC-2026.13" and the two checksums
    Then no KieBase is compiled and no slot of the KieBase registry is replaced
    Then the local copy of "ALLOC-2026.11" stays in use with its version and checksum
    Then the next answer names "ALLOC-2026.11"

  Scenario: AC3 A scenario of the local set fails and the load is refused whole (new, D-RCV-60)
    Given the rwb-decision contract mock returns the model of package "ALLOCATION" version "ALLOC-2026.12" whose SHA-256 matches its checksum and whose DRL compiles
    Given the 50 scenarios stored with the version are re-run locally and scenarios "TA-07" and "TA-19" expect queue "MTG-BKK-CO" while the new rows return "MTG-CEN-CO"
    When the local scenario set runs
    Then the local load is refused with MSG-P3-027 for the scenario check naming "TA-07" and "TA-19"
    Then the compiled KieBase is discarded and the local copy of "ALLOC-2026.11" stays in use
    Then no decision is taken with "ALLOC-2026.12"
    Given the fetched model has no default row and a condition cell at row 14 with no value
    When the local checks run
    Then the local load is refused with MSG-P3-027 for the default row and the compile checks naming row 14 and its cell
    Then the version in force stays "ALLOC-2026.11"

  Scenario: AC4 A version that is not APPROVED, unknown or not yet effective is refused (new, D-RCV-60)
    Given the rwb-decision contract mock returns version "ALLOC-2026.12" in state LOADED and version "ALLOC-2026.14" in state REFUSED
    Given the rwb-decision contract mock returns 404 for a version label that does not exist and an empty body for a second unknown label
    Given the rwb-decision contract mock returns version "ALLOC-2026.13" in state APPROVED with valid from 2026-12-20 and the evaluation business date is 2026-12-15
    When rwb-comms asks to load each of the five versions in turn
    Then each load is refused with MSG-P3-027 for the package state check naming the package, the version and its state
    Then no KieBase is compiled from any of the five
    Then the local copy of "ALLOC-2026.11" stays in use with its version and checksum after every refusal

  Scenario: AC5 A registry rollback puts the previous version back in force on the next event and a decided case keeps its version (new, D-RCV-60)
    Given version 7, "ALLOC-2026.13", is in force in the local copy and version 6, "ALLOC-2026.12", was in force before it
    Given a case was decided under version 7 and its local decision record carries rule version "ALLOC-2026.13"
    Given rwb-decision rolls back version 7 in one call, marks it ROLLED_BACK and publishes one RulePackageInForce naming "ALLOC-2026.12" with its checksum
    When rwb-comms reads that event
    Then it fetches "ALLOC-2026.12", verifies its checksum and swaps it back in as one step inside the 300 ms budget
    Then the local copy in force is version 6, "ALLOC-2026.12"
    Then a new answer names "ALLOC-2026.12"
    Then the case decided under version 7 keeps rule version "ALLOC-2026.13" on its decision record, because open cases keep the version they were decided under (R-UNI-38)
    Then rwb-comms calls no operation that edits, approves or rolls back the registry, and the copy of a version in state ROLLED_BACK is never loaded again

  Scenario: AC6 The model fetch is unavailable, so nothing is swapped and the next event retries (new, D-RCV-60)
    Given rwb-decision publishes RulePackageInForce for package "ALLOCATION" version "ALLOC-2026.12"
    Given the rwb-decision contract mock returns 503 for the model fetch, and a second call answers beyond the 2 s client budget
    When rwb-comms reads the event and calls the model fetch
    Then the local load is refused with MSG-GEN-006 naming the model fetch of rwb-decision
    Then no KieBase is compiled and the local copy of "ALLOC-2026.11" stays in use with its version and checksum
    Then an answer taken in the meantime names "ALLOC-2026.11"
    Then the event is not marked processed in the inbox, and the failure is in the local run record
    When the next RulePackageInForce for the same package and version arrives and the fetch answers
    Then the fetch is retried, the checksum is verified and the swap completes

  Scenario: AC7 A new rule row and a new target queue are data, not code (new, D-RCV-60)
    Given the rwb-decision contract mock returns the model of package "ALLOCATION" version "ALLOC-2026.13" whose row "ALLOC-015" targets queue "MTG-UPC-CO" and whose default row "ALLOC-999" targets queue "GEN-CO"
    When the version is loaded locally and evaluated
    Then the answer names queue "MTG-UPC-CO" for the row that matches first and queue "GEN-CO" through the default row, with no code change, no rebuild and no release of rwb-comms
    Then no package code, version label, rule ID, target queue or owner role is present in the service code or in a resource file
    Then the KieBase registry holds at most 20 versions and the least recently used copy is evicted
    Then the package, the version and the rule ID on every answer are the values the local copy holds
```

The seven criteria above are new and belong to this slice only; the legacy criteria of RWB-E1-073 are owned by RWB-P3-E1073-APP (AC1 to AC15) and no legacy criterion is copied here, exactly as RWB-ITG-E1073-ITG section 16 records. Every value used is copied from the legacy story or from the two design decks — the package `ALLOCATION`, the versions `ALLOC-2026.11`, `ALLOC-2026.12`, `ALLOC-2026.13` and `TRF-2026.11`, the rows `ALLOC-014`, `ALLOC-015`, `ALLOC-031`, `ALLOC-032`, `ALLOC-040`, `ALLOC-041` and `ALLOC-999`, the scenarios `TA-07` and `TA-19`, the queues `MTG-BKK-CO`, `MTG-UPC-CO`, `MTG-CEN-CO` and `GEN-CO`, 24 and 26 rows, 50 scenarios, the checksum `9f2c...e1b4` and valid from 2026-12-15 — and is used as synthetic test data because no source names the package rwb-comms is assigned (GAP-1216; ASM-2170). `Given the rwb-case contract mock returns …` and `Given the rwb-decision contract mock returns …` name the contract through which each cross-service value is stubbed, so no test reaches another service's schema.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Governance is central in rwb-decision and evaluation is local: this service loads, verifies and evaluates the version it is assigned and never authors, approves, dates or rolls back a package | Arch v5 slide 27; Temporal and Drools design slide 15; RWB-ITG-E1073-ITG section 10 |
| BR2 | On `RulePackageInForce` the service fetches the model, verifies the SHA-256 and swaps it in atomically; a failed verification keeps the last good model | Arch v5 slide 27; Temporal and Drools design slide 15; DP-04 |
| BR3 | Only an APPROVED version whose valid-from date has been reached is loaded locally; a LOADED, REFUSED, SUPERSEDED or ROLLED_BACK version and an unknown label are refused | Legacy RWB-E1-073 section 9; R-UNI-38 |
| BR4 | A load with any failed check is refused in full and the version in force does not change | Legacy RWB-E1-073 BR2; REQ-CWC-014 |
| BR5 | Before a version decides anything, its scenario set runs locally, at least `rules.testcases.min` (50) scenarios, through the same evaluator as production | Legacy RWB-E1-073 BR10; REQ-CWC-014; D-RCV-36 T4 |
| BR6 | First match: RuleSet = package code, each row is one rule whose NAME is the rule ID, rows share one activation-group, salience follows row order and the default row is last; exactly one row decides | Legacy RWB-E1-073 BR3; D-RCV-36 T5; REQ-CWC-008 |
| BR7 | The allocation package always has a default row, so a local scenario set can never pass without one | Legacy RWB-E1-073 BR4; REQ-CWC-008 |
| BR8 | A version takes effect on its valid-from date after approval, and open cases keep the version they were decided under | R-UNI-38; Legacy RWB-E1-073 BR5 |
| BR9 | The KieBase registry holds one compiled KieBase per package version with an LRU of at most 20, and a model is never recompiled per call | Temporal and Drools design slide 16; Legacy RWB-E1-073 (drools.kiebase.cache.max = 20) |
| BR10 | Evaluation runs only inside an activity, under 300 ms, and the answer names the package code, the version and the rule ID | Temporal and Drools design slides 14 and 16; Arch v5 slide 27; NFR-011 |
| BR11 | The local decision record carries the rule ID and the version and is written in the same transaction as the state change and the outbox row; a failed write means nothing moves | Temporal and Drools design slide 14; DP-03; R-UNI-39 |
| BR12 | No business value in code: the package code, the version labels, the rows, the target queues, the owner roles, the scenario minimum and the cache size are data or parameters | Legacy RWB-E1-073 section 17; DP-06; DP-07 |
| BR13 | A version in state IN_FORCE is never edited by this service; a change is a new version published by rwb-decision and a rollback moves the pointer there, never here | Legacy RWB-E1-073 section 17; R-UNI-38; RWB-ITG-E1073-ITG BR15 |
| BR14 | Every refusal of a local load is in the local run record with the package, the version, the check and the row, cell or scenario IDs, and never with a case fact or a personal value | Legacy RWB-E1-073 BR8; section 14 of this story |

### 9. State transitions

None for a case status. This story changes the state of the local copy only, and it observes the registry states without setting them:

| From | Event | Condition | To |
|---|---|---|---|
| Not loaded | `RulePackageInForce` | The fetch answers, the checksum matches and every local check passes | Verified and in use |
| Not loaded | `RulePackageInForce` | The fetch fails, the checksum does not match, a scenario fails, or the state is not APPROVED | Not loaded; the refusal is in the local run record |
| Verified and in use | `RulePackageInForce` for a newer version | The fetch answers, the checksum matches and every local check passes | Replaced as one step by the newer version; the older copy stays in the LRU ring |
| Verified and in use | `RulePackageInForce` for a newer version | Any check fails | Unchanged; the last good copy stays in use |
| In use | registry rollback, followed by one `RulePackageInForce` | The restored version fetches and passes | The restored version in use; the replaced copy is released |
| Any | A read of the local copy | Never | The same state; a read changes no row |

The registry states the local load tests against are the ones the design fixes: LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED. Only APPROVED and IN_FORCE are loadable here. The states of the local copy are the local copy's own and are not registry states; the name of each local state column is Not specified in the source documents (GAP-1214; ASM-2173).

### 10. Authority

The roles are taken from the legacy story's authority table and from the module's role matrix; no role grants itself a right, and this story implements no right check of its own.

| Who | What they may do in this story |
|---|---|
| rwb-comms service identity (the rwb-comms login, DP-02) | Reads the model fetch, the parameters and the reference data; writes the local copy, the local decision record and its own inbox and outbox rows in `rwb_comms`; calls no registry operation |
| SY-RULES | Evaluates the version in force inside the activity and answers scenarios through the same evaluator; receives the local run record of a refusal |
| SY-CASEWF | Applies the approved decision; no right over a package version and no right over the local copy |
| RW-AUDIT | Reads the version, its checksum and the local run record of this service (Rules and parameters R) |
| RW-COE | Loads a package version and calls rollback at rwb-decision (Rules and parameters CRUD); in this story only an event and a fetch reach the service |
| RW-RISK | Approves a version at rwb-decision (Rules and parameters A); may not hold RW-COE, and this story cannot approve anything |
| RW-REFADM | Prepares load files; may not approve and has no path into this story |
| RW-TRIBE | Builds and runs the build gate of rwb-decision; no production data, and no right in this service |
| No role | May load a version that is not APPROVED, edit the local copy of an in-force version, or read the local copy without Rules and parameters R |
| No delegation of authority level applies | A rule package version is not a credit decision |

The read right on the local copy and on the model fetch is enforced at gateway-bff and at the rwb-decision contract, not in this story; the access test cases of section 16 assert the refusal at the boundary (TC-E1-073-16, TC-E1-073-17, TC-E1-073-20). DP-08 is not among the patterns of this story, so no authorise call is made here.

### 11. Data

| BR Field ID | Entity (owner) | Field | Read or write |
|---|---|---|---|
| None | local model copy (P6, `rwb_comms`) | package code, version label, SHA-256 checksum, state, valid from, loaded at | Write; the table name and the column names are Not specified in the source documents (GAP-1214; ASM-2173) |
| DF-REF-274 to DF-REF-278 | rule_package (P7 `rwb_decision`) | all fields | Read through the model fetch only |
| DF-REF-279, DF-REF-280, DF-REF-281 | rule_package_version (P7 `rwb_decision`) | id, package_id, version_label | Read through the model fetch only |
| DF-REF-282 | rule_package_version (P7 `rwb_decision`) | status | Read through the model fetch only; decides AC4 |
| DF-REF-284, DF-REF-285 | rule_package_version (P7 `rwb_decision`) | drl_source, checksum | Read through the model fetch only; the checksum decides AC2 |
| DF-REF-286, DF-REF-287 | rule_package_version (P7 `rwb_decision`) | valid_from, valid_to | Read through the model fetch only; valid from decides AC4 |
| DF-REF-292, DF-REF-293 | rule_package_version (P7 `rwb_decision`) | test_result, dry_run_counts | Read through the model fetch only; the dry run is rwb-decision's |
| DF-REF-296 to DF-REF-298 | rule_row (P7 `rwb_decision`) | package_version_id, drools_rule_name, outputs | Read through the model fetch only; the rule ID and the outputs of an answer |
| DF-REF-185 to DF-REF-197, DF-REF-299 | rule_test_case (P7 `rwb_decision`) | all fields, package_version_id | Read through the model fetch only; the scenario set re-run locally, and how it travels in the fetch answer is Not specified in the source documents (GAP-1214; ASM-2177) |
| None | parameter_catalog, parameter_value (P3 `rwb_case`) | `rules.testcases.min` = 50, `drools.kiebase.cache.max` = 20 | Read through the parameters contract (DP-06) |
| None | reference_row, reference_version (P3 `rwb_case`) | the package code assigned to rwb-comms, the version labels it may hold, the target queues and owner roles | Read through the reference-data contract (DP-07) |
| DF-DEC-001 to DF-DEC-018 | local decision record (P6 rows in `rwb_comms`, written through the decision-record library) | rule ID, rule version, inputs reference, recommendation, outcome, decided at | Write (DP-03) |
| None | outbox_event, processed_event, idempotency_key (PLT library in `rwb_comms`) | CloudEvents id, consumer group, processed at | Write the inbox row of the event and the outbox row of `DecisionRecorded` |

Not owned and never read directly: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, `approval` and `decision_log_entry` (P7 rwb-decision), and `recovery_case` with its case fields (P3 rwb-case). The case fields the dry run reads (DF-CAS-003, DF-CAS-010, DF-CAS-012, DF-CAS-015, DF-CAS-019) are read by rwb-decision through the rwb-case contract and are not read here: this story's scenarios use synthetic facts. The schema is `rwb_comms`, its migration runs in the per-service Flyway sequence (DP-15, DP-01), and the service holds no foreign key into another schema.

### 12. Contract

#### 12.1 REST operations provided

None. This story is driven by an event and by the activities of the capabilities it serves; it adds no REST operation, no admin path and no read of the registry, and it inherits the base `/api/recovery/comms/v1` of the service (DP-13) only for the operations other stories provide.

#### 12.2 REST operations consumed

Every row is one hop on the owner's base with a 2 s timeout, a breaker per downstream and a single GET retry with jitter (DP-11, ADR-020).

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` | P7 rwb-decision | Fetch the model of a package version with its generated DRL and its SHA-256 checksum for the local load. Named `GET /rule-models/{n}/{v}` on Architecture v5 slides 14 and 27; absent from the Ownership Map and API Specification v4, so the path segments, the request fields and the response fields are Not specified in the source documents (GAP-1217; ASM-2171). Contract RWB-P7-E1073-CON under the DP-04 row of §R5.5; the plan's contract dependency row carries RWB-P3-E1073-CON (GAP-1215; ASM-2172) |
| GET | `/api/recovery/case/v1/admin/parameters` | P3 rwb-case | `rules.testcases.min` (50) and `drools.kiebase.cache.max` (20) in force on the business date, as parameters and never as code (DP-06). The parameter codes are the legacy names of RWB-E1-042 and the read path is Not specified in the source documents (GAP-1214; ASM-2175) |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The package code this service is assigned, the version labels it may hold and the target queues and owner roles, as reference data (DP-07). The list code and the field names are Not specified in the source documents (GAP-1216; ASM-2170) |

The rwb-access authorise operation is not consumed here: DP-08 is not among the patterns of this story and the read right is enforced at the edge and at the rwb-decision contract. No operation of rwb-decision that writes, approves, promotes or rolls back a version is called, so a version in state IN_FORCE has no update path from this service (BR13).

#### 12.3 Events published

| Event | Topic | Owner of the type | Key | Schema element (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | P7 rwb-decision | caseId | package code, version label, rule ID, recommendation and outcome reference, decided at; written through the local decision-record library in the same transaction as the state change and the outbox row (DP-03) |

This story publishes nothing else. It fixes no event of its own on `rwb.comms.events.v1`: DP-14 is applied as the naming rule of §R4 only, so the service's topic keeps the name `rwb.comms.events.v1` and the events of the notice and dispatch stories stay with them.

#### 12.4 Events consumed

| Event | Topic | Owner | Declared shape | Handler in this story |
|---|---|---|---|---|
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision, published by the 00:01 promote run JOB-20 | package code, version label, SHA-256 checksum, valid from | The local load of steps 4 to 10: fetch, verify, compile, run the scenario set, swap in, keep the last good copy. CloudEvents 1.0 binary mode, one event per promoted or restored version, deduped in `processed_event`, retry 1 min, 10 min, 1 h then `.dlt` |

The event payload beyond those four values is Not specified in the source documents (GAP-1214; ASM-2174). Architecture v5 slide 43 row 30 lists rwb-case, rwb-valuation, rwb-treatment and rwb-payment as the consumers of the event while slide 20 says every service refreshes its cache on `RulePackageInForce`; this story reads the slide 20 rule, which is the one that makes rwb-comms an evaluator, and the difference is carried as a conflict (GAP-1219; ASM-2174).

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `EvaluateRules` | Activity | `rwb-comms` | Input package code, facts and business date; output `RuleResult` (package code, version, rule ID, outputs). Evaluates the verified local copy, first match, inside the 300 ms budget; Drools is called in the activity and never in workflow code (Temporal and Drools design slides 14, 15 and 16; NFR-011) |
| `RecordAndApply` | Activity | `rwb-comms` | Writes the local decision record with the rule ID and the version, the state change and the outbox row in one transaction in `rwb_comms` (Temporal and Drools design slide 14; DP-03) |

No workflow is registered by this story: the workflow that calls the two activities belongs to the capability that needs the answer, and the names of the activities above are the ones the design and RWB-ITG-E1073-ITG section 12.5 fix. The Temporal workflow kit that runs the activities arrives with `H RWB-PLT-E1071-CON` in the DP-10 row, which the plan's H list does not carry (GAP-1218; ASM-2172).

#### 12.6 Schedules

None. This story registers no Schedule, no cron entry and no job row, and reads no shared scheduler table. JOB-20 rule promote at 00:01 is a Temporal Schedule in rwb-decision (Arch v5 slides 14 and 44; Ownership Map JOB-20) and reaches this service only as the `RulePackageInForce` event.

#### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| local model copy | P6 (`rwb_comms`) | The package code, version label, checksum, state, valid from and load time of the copy in use; the last good copy is kept here across a restart. The table name and its columns are Not specified in the source documents (GAP-1214; ASM-2173) |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_comms` | The outbox row of `DecisionRecorded` and the inbox row of `RulePackageInForce` (DP-03, DP-15) |
| local decision record | P6 rows in `rwb_comms`, written through the decision-record library | The rule ID and the version of every answer (DP-03) |

Not owned and never read directly: `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` and `decision_log_entry` (P7 rwb-decision), `recovery_case` (P3 rwb-case), and the KieBase of any other service, since each service compiles and holds its own copy.

#### 12.8 Contract fakes

| Fake | Serves | Documented answers |
|---|---|---|
| rwb-decision model-fetch WireMock | RWB-P7-E1073-CON (DP-04) | The model of `ALLOCATION` `ALLOC-2026.12` in state APPROVED with 26 rows, its generated DRL and checksum `9f2c...e1b4`; `ALLOC-2026.13` with 26 rows and 50 passing scenarios; a model whose SHA-256 does not match; a model with no default row and a condition cell with no value at row 14; a model whose scenarios `TA-07` and `TA-19` return `MTG-CEN-CO`; `ALLOC-2026.12` in state LOADED; `ALLOC-2026.14` in state REFUSED; 404 for a label that does not exist; an empty body; `ALLOC-2026.13` APPROVED with valid from 2026-12-20; 503; and a delayed answer beyond 2 s |
| rwb-case parameters WireMock | The parameters contract of rwb-case (DP-06) | `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20 in force for the business date, and a delayed answer beyond 2 s |
| rwb-case reference-data WireMock | The reference-data contract of rwb-case (DP-07) | The package code `ALLOCATION`, the version labels in force and the target queues and owner roles as rows, and a delayed answer beyond 2 s |
| Kafka fixture | `rwb.decision.events.v1` | One `rwb.decision.RulePackageInForce.v1` per promoted or restored version with the four values of 12.4, a repeated delivery of the same CloudEvents id, and a promotion with nothing to promote that publishes no event |

The fakes carry synthetic values only: no production data, no production copy and no production namespace.

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 3 | The model fetch on rwb-decision, the parameters read and the reference-data read on rwb-case; one hop, 2 s (DP-11, DP-13) |
| Kafka | 1 event type | 1 event type | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` published through the local decision-record library (DP-03); `rwb.decision.RulePackageInForce.v1` on `rwb.decision.events.v1` consumed with inbox dedupe |
| Temporal | 2 activities | None registered | `EvaluateRules` and `RecordAndApply` on queue `rwb-comms`; no workflow and no Schedule of this story |
| File | None | None | The model travels in the fetch answer; this service writes no file |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.comms`, module `rules`, Java package `th.co.scb.ace.workbench.recovery.comms.rules`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_comms`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views; this story reads neither | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

Twelve patterns are applied and every one is a row above. Three readings of that table matter for this story and are stated rather than silently resolved. First, the DP-04 row names `H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON` while the plan gives `Depends on (build) = None` and `Contract dependencies = RWB-P3-E1073-CON` with no H at all; the conflict is recorded as GAP-1215 and the story is built against the given list, so the Drools kit is treated as a wave-0 platform prerequisite and the P3 contract is the one faked (ASM-2172). Second, the H rows that DP-03, DP-04, DP-06, DP-07, DP-10, DP-14, DP-15 and DP-19 add are absent from the plan's H list, which is recorded as GAP-1218 and does not change the lane or the Day-1 start. Third, DP-14 is applied as the naming library only: it fixes `rwb.comms.events.v1`, `rwb.decision.events.v1` and the event names of §R4 and it adds no publication of this story. DP-17 is not in this story's list and is not claimed: there is no data lake in the target and this story reads no lake data. DP-05 and DP-19 are applied as boundaries — the story reads no ACE view and renders no screen.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RulePackageInForceListener | Listener | Reads `rwb.decision.RulePackageInForce.v1` through the inbox, skips a repeated CloudEvents id and starts the local load |
| ModelFetchClient | Client | Calls `GET /api/recovery/decision/v1/rule-models/{packageCode}/{versionLabel}` with the 2 s budget, the breaker and one GET retry |
| ChecksumVerifier | Service | Computes the SHA-256 of the fetched model and compares it with the checksum named by the event and by the version, before any compile |
| KieBaseRegistry | Service | Compiles one KieBase per package version and holds at most `drools.kiebase.cache.max` (20) with LRU eviction; never recompiles per call; swaps a verified KieBase in as one step |
| LocalScenarioRunner | Service | Re-runs the scenario set stored with the version, at least `rules.testcases.min` (50) scenarios, through the same `RuleEvaluator` and compares each expected queue or outcome |
| LocalCopyRepository | Repository | Reads and writes the local copy row of `rwb_comms`: package code, version label, checksum, state, valid from and load time |
| LocalLoadRefusalWriter | Service | Writes the run record of a refused load with the package, the version, the check and the row, cell or scenario IDs |
| ParameterAndReferenceReader | Service | Reads `rules.testcases.min`, `drools.kiebase.cache.max`, the package code, the version labels and the queues through the rwb-case contracts (DP-06, DP-07) |
| EvaluateRulesActivity | Activity | Evaluates the verified local copy first match and returns `RuleResult` with the package code, the version, the rule ID and its outputs, inside 300 ms |

**Database and migrations**

- Writes the local copy row, the inbox row, the outbox row and the local decision record in schema `rwb_comms`; reads no row of another schema (DP-01).
- Migration `V1073_1__local_rule_copy.sql` in the rwb-comms Flyway sequence: the local copy table with its unique key on `(package_code, version_label)` and the index on the state. The table and column names are Not specified in the source documents (GAP-1214; ASM-2173) and are fixed by the DB story of this service.
- No registry table, no rule table and no scenario table is created here: they stay in `rwb_decision` (Ownership Map rows rule_package, rule_package_version, rule_row and rule_test_case).

**Configuration and reference data**

- `rules.testcases.min` = 50 and `drools.kiebase.cache.max` = 20, read as parameters on the business date (DP-06).
- The package code assigned to rwb-comms, the version labels it may hold and the target queues and owner roles, read as reference data (DP-07). None of them is written in code and none is fixed by this story (GAP-1216; ASM-2170).
- The feature flag `rwb.comms.local-rule-copy`. Off: the listener consumes and acknowledges the event without loading, no local copy is swapped, the last good copy keeps deciding and nothing else changes.
- The login is the rwb-comms login (DP-02); its name is allocated by the platform database story and is not fixed here.

**Build steps**

1. Migration `V1073_1` and `LocalCopyRepository`, with the unique key and the state index tested.
2. `ModelFetchClient` against the model-fetch fake: the APPROVED answer, 404, the empty body, 503 and the delayed answer beyond 2 s (AC1, AC4, AC6).
3. `ChecksumVerifier` before any compile, with the matching and the mismatching checksum (AC1, AC2).
4. `KieBaseRegistry` with the LRU of 20, the one-step swap and the "never recompiled per call" assertion (AC1, AC7).
5. `LocalScenarioRunner` with the 50 scenarios of a version, the failing `TA-07` and `TA-19`, the missing default row and the compile error at row 14 (AC3).
6. `RulePackageInForceListener` with the inbox skip of a repeated delivery and the unprocessed-on-refusal rule (AC1, AC6).
7. `EvaluateRulesActivity` and `RecordAndApply` on queue `rwb-comms`, with the 300 ms budget measured over 200 fixture evaluations and the one-transaction write of the record, the state change and the outbox row (AC1, AC7).
8. The rollback path: the restored version fetched and swapped back, and the decided case keeping its version (AC5).
9. `ParameterAndReferenceReader` with the parameters and reference fakes, and the assertion that no package code, version label, rule ID, queue or role appears in code or in a resource file (AC7).
10. The contract-fake run of the four fakes, so the story builds before rwb-decision and rwb-case are live.

**Done when.** The tests in section 16 pass, the local copy loads, verifies, compiles, runs its 50 scenarios and swaps in SIT on the synthetic ALLOCATION fixtures, a refused version never decides anything, the 200 fixture evaluations each complete inside 300 ms, a rollback is followed on the next event, and no package value appears in the service code.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-027 | A local load check fails | The rule version was refused at the {check} check: {detail}. |
| MSG-GEN-006 | The model fetch does not answer inside 2 s or answers 503 | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | The caller holds no Rules and parameters right for the read | You cannot {action} here. Your role does not include it. |
| MSG-P7-003 | The local decision record could not be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |

The texts are copied unchanged from RWB-E1-073 section 14 and the platform catalog; this story adds no message text. For MSG-P3-027 the {check} value is compile, schema, overlap, unreachable row, default row or scenario as the legacy story fixes it, and the local load adds the checksum and the package state; the wording of the two added values and the message prefix are Not specified in the source documents (GAP-1214; ASM-2176). The {detail} names the package, the row IDs, the cells, the scenario IDs or the two checksums, and never a case fact or a personal value. MSG-P4-002 is raised at the gateway-bff edge or by the rwb-decision contract, and MSG-P7-003 is raised by the local decision-record library. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen is built in this story, and nothing is rendered: the only surface is the activity answer and the local copy's state. SCR-39 Rules and parameters and the rule package administration screen (Epic 8, FEAT-ADM-02) are out of scope, and so is the rule change audit report of RWB-E2-041.

| Read through gateway-bff (DP-19) | What it shows for this story | State read |
|---|---|---|
| SCR-39 Rules and parameters, later epic | The version in force in this service, its checksum and its load time, read from the local copy | Verified and in use |
| The decision record view of a case | The rule ID and the version that decided it | Any, from the record |

The states this story holds are the local copy states of section 9 and the version states it tests against (LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED). The composite route, its field list, its masking rules and its timeout budget belong to RWB-PLT-N001-CON; no route and no field list is declared here.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-073-16 | AC1, AC2, BR1 | Component | A caller without the Rules and parameters read right calls the model fetch for `ALLOCATION` `ALLOC-2026.12`; refused with MSG-P4-002 and the local copy stays at `ALLOC-2026.11` |
| TC-E1-073-20 | AC4, BR3 | Component | A caller without the Rules and parameters R right reads the local copy of `ALLOCATION`; refused with MSG-P4-002 and nothing is loaded |
| TC-E1-073-01 | AC1, BR1, BR5, BR8, BR10 | Contract | `ALLOCATION` `ALLOC-2026.12` with 26 rows, 50 passing scenarios and checksum `9f2c...e1b4` |
| TC-E1-073-02 | AC3, BR6 | Component | Rows `ALLOC-031` and `ALLOC-032` at row order 12 in the local scenario set |
| TC-E1-073-03 | AC3, BR1, BR5 | Component | Scenarios `TA-07` and `TA-19` returning `MTG-CEN-CO` where `MTG-BKK-CO` is expected |
| TC-E1-073-04 | AC1, AC5, BR9, BR10 | NFR | Versions 6 and 7, `ALLOC-2026.12` and `ALLOC-2026.13`, and 200 fixture evaluations each inside the 300 ms activity budget |
| TC-E1-073-05 | AC3, BR1 | Component | Row 9 with the value `QUICK` that is not in its list |
| TC-E1-073-06 | AC3, BR1 | Component | Rows `ALLOC-040` and `ALLOC-041`, the second unreachable |
| TC-E1-073-07 | AC3, BR6, BR7 | Component | An allocation row set with no default row |
| TC-E1-073-08 | AC4, BR3 | Component | Version `ALLOC-2026.12` in state LOADED, not APPROVED |
| TC-E1-073-09 | AC5, BR13 | Component | A rollback whose earlier version the fetch cannot serve |
| TC-E1-073-10 | AC1, BR2 | Component | The same `RulePackageInForce` CloudEvents id delivered twice |
| TC-E1-073-11 | AC4, BR8 | Component | `ALLOC-2026.13` APPROVED with valid from 2026-12-20 on business date 2026-12-15 |
| TC-E1-073-12 | AC4, BR4 | Component | An empty model body in the fetch answer |
| TC-E1-073-13 | AC3, BR1, BR5 | Component | The fetched model whose condition cell `exposure_band >=` has no value at row 14 |
| TC-E1-073-14 | AC3, BR5 | Component | The fact mapping changed so `TA-07` returns `MTG-CEN-CO` and the local scenario set fails |
| TC-E1-073-15 | AC1, BR2, BR14 | Contract | The workbook `ALLOCATION-2026.12.xlsx` and its SHA-256 `9f2c...e1b4` carried by the fetch answer |
| TC-E1-073-17 | AC4, BR3 | Component | A version label the fetch answers 404 for, read locally |
| TC-E1-073-18 | AC4, BR3 | Component | Version `ALLOC-2026.14` in state REFUSED |
| TC-E1-073-19 | AC6, BR2 | NFR | The model fetch answering 503 and then beyond 2 s, the retry on the next event, and the 300 ms budget held throughout on the last good copy |

The twenty cases are the legacy cases of this key, kept in the legacy order with their data unchanged, and their level is remapped: legacy System becomes Component or Contract, legacy Access becomes Component and is asserted on the local load and the local read refusals, and the NFR level carries the 300 ms budget of TC-E1-073-04 and TC-E1-073-19. The covers column names the legacy criterion numbers as RWB-ITG-E1073-ITG section 16 requires, because the legacy criteria AC1 to AC15 belong to RWB-P3-E1073-APP; this story's own criteria are AC1 to AC7 above and are proved by these cases on the local copy. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the package code, the version labels, the rows, the rule IDs, the target queues, the owner roles, the scenario minimum and the cache size are parameters, reference rows or the fetched model, never constants in the service (BR12; DP-06, DP-07).
- No personal data in the event, the local copy, the run record, the logs or the fixtures: package codes, version labels, row IDs, rule IDs, queues, checksums and counts only, and the scenario facts are synthetic.
- The service writes only `rwb_comms` and reads no other service's tables; the registry is read through the model fetch only (DP-01).
- The checksum is verified before any compile, and a version that fails any check never decides a case: the last good copy stays in use (BR2, BR4).
- A version in state IN_FORCE is never edited from here; the service has no write, approve, promote or rollback path to the registry (BR13).
- One evaluator serves the local scenario set and production, and a model is never recompiled per call; the registry holds at most 20 versions with LRU eviction (BR5, BR9).
- Evaluation runs only inside the activity and never in workflow code, so a replay reuses the recorded answer, and the record, the state change and the outbox row commit together or not at all (BR10, BR11; R-UNI-39).
- One hop and a 2 s timeout on every consumed call, with a breaker and a single GET retry; no call goes through another service (DP-11, ADR-020).
- The local copy is replaced as one step, so an answer names exactly one version and never a half-loaded model.
- No production data, no production copy and no production connection in any test, fixture or fake.

### 18. Traceability

| Requirement or decision | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-CWC-013 | A rule change reaches production as a validated load with a version stamp and rolls back by one call | The model fetch, the local copy with its version and checksum, `RulePackageInForce` and its rollback event | TC-E1-073-01, TC-E1-073-04, TC-E1-073-09, TC-E1-073-10, TC-E1-073-15 |
| REQ-CWC-014 | Rule loads are validated for schema, overlap, unreachable rows, a missing default and a set of test cases before they take effect | The local checksum check, the local checks and `LocalScenarioRunner` with `rules.testcases.min` | TC-E1-073-02, TC-E1-073-03, TC-E1-073-05, TC-E1-073-06, TC-E1-073-07, TC-E1-073-12, TC-E1-073-13, TC-E1-073-14 |
| REQ-DRI-004 | Epic 1 records use versioned rules | `EvaluateRules`, `RecordAndApply` and `DecisionRecorded` with the rule ID and the version | TC-E1-073-01, TC-E1-073-04, TC-E1-073-15 |
| REQ-CWC-008 | Allocation rules apply first match and always have a default | The first-match evaluation of the local copy and the default row check | TC-E1-073-07 |
| RWB-E1-073 | The legacy key whose local-copy slice this story carries | The seven criteria of section 7 and the twenty cases of section 16 | TC-E1-073-16 to TC-E1-073-20, TC-E1-073-01 to TC-E1-073-15 |
| DP-04 | Embedded Drools kit; rule packages from rwb-decision | The model fetch, `KieBaseRegistry`, `ChecksumVerifier` and the two activities | TC-E1-073-01, TC-E1-073-04, TC-E1-073-16 |
| DP-03 | Local decision record and the shared topic | The record with the rule ID and the version and `DecisionRecorded` on `rwb.decision-record.v1` | TC-E1-073-01, TC-E1-073-15 |
| DP-06, DP-07 | Parameters and reference data through rwb-case | `rules.testcases.min`, `drools.kiebase.cache.max`, the package code and the queues | TC-E1-073-01, TC-E1-073-07 |
| DP-14 | Topic and event naming | `rwb.comms.events.v1` and `rwb.decision.events.v1` as names only | TC-E1-073-01, TC-E1-073-10 |
| ADR-012, ADR-017 | Embedded Drools with a central registry; evaluation local in the owning service | The split of governance and evaluation this story implements | TC-E1-073-01, TC-E1-073-04 |
| ADR-022 | Local decision record plus central ledger | The local record and `DecisionRecorded`, with the ledger left to rwb-decision | TC-E1-073-15 |
| NFR-011 | A rule evaluation completes under 300 ms at the 95th percentile | The `EvaluateRules` activity budget | TC-E1-073-04, TC-E1-073-19 |

### 19. Out of scope

- The authoring workbook, the compile, the schema, overlap, unreachable-row, default-row and scenario checks at load, the four-eyes approval, the effective date, the promote run JOB-20, the one-call rollback and the version audit: the rwb-decision part of this legacy key, RWB-P7-E1073-APP.
- The dry run over the open cases, its counts by product, queue and rule, and the change log of a version: RWB-P7-E1073-APP, reading case fields through the rwb-case contract.
- The rule package contract published to the evaluating services, its AsyncAPI document and the model fetch implementation: the rwb-decision part, RWB-P7-E1073-APP.
- The authoring path, the ALLOCATION evaluation on the case and the local copy of rwb-case: RWB-P3-E1073-APP, with RWB-P3-E1073-CON and RWB-P3-E1073-INF.
- The local copy and the evaluation in rwb-integration: RWB-P2-E1073-APP.
- The build gate `RuleScenarioBuildGate`, the release manifest and the profile refusal: RWB-ITG-E1073-ITG, which also proves this story's local load end to end on the real services.
- The registry schema, the Flyway sequence and the grants of `rwb_decision`, and the version states as rows: RWB-P7-E1073-APP with the per-service DB stories.
- The Epic 2 packages RESTRUCTURE, PAYMENT_MATCH and BOOKING_MATCH: RWB-E2-042.
- The rules that consume the answer — notice generation, the conduct check, the contact stop and every other Epic 1 and Epic 2 rule set — which stay with their own stories and call `EvaluateRules`.
- The rule package administration screen and SCR-39 Rules and parameters: Epic 8, FEAT-ADM-02.
- The rule change audit report: RWB-E2-041.
- The central decision ledger, its hash chain and the 02:00 chain check: RWB-ITG-E1008-ITG and RWB-TE-008.
- Loading the other 448 routing rules: the later epics of the rule programme.
