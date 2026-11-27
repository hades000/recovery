# RWB-PLT-E1072-CON Drools runtime and rule package store - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split (rework) of RWB-E1-072. The rules kit contract — the published interfaces, the fetched model shape, the version-in-force rule, the refusal and the kit fake — is published on Day 1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (20 resolved, 66 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1072-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-072 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Size | Not sized in this story; the squad sizes it at refinement |
| Contract version | v1 (published by this story) |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P7-E1073-CON (governance contract, C) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-020) |
| Status | Draft (directive resolutions) |

### 1. Story

As a **consumer of the embedded rules kit**, I want **the kit contract — the four published interfaces, the shape of the model fetched from rwb-decision, the version-in-force rule, the refusal and a working fake — published on Day 1**, so that **every service can build and test its `EvaluateRules` activity, and every contract test can run, before a single approved model exists in rwb-decision**.

This is the contract slice of the split (rework) of legacy key RWB-E1-072 under epic RWB-PLT-LIB (Template and Rules §R6). The legacy story published four interfaces inside the module and declared its own endpoint for the store; this story publishes the same interfaces as the platform kit contract, adds the shape of the model that now arrives over a contract instead of from a local table, and freezes the refusal. It publishes:

- `RuleEvaluator`, `RuleResult`, `RuleCatalog` and `RuleRow`, as the legacy story published them, with the same method signatures and the same result fields, and with the rule that no KieBase, KieSession or other Drools type crosses them (Temporal and Drools design slides 11 and 16).
- The fetched model shape: package code, package version label, checksum, the ordered rows of the version, and the catalog projection of each row — action text, owner role, timer spec and outputs — as the payload of `GET /api/recovery/decision/v1/rule-models/{n}/{v}` on rwb-decision (Architecture v5 slides 14 and 27).
- The version-in-force rule: the version is chosen at evaluation time from the caller's business date and the valid-from and valid-to dates, never from the system clock, and the chosen label is returned and recorded (D-RCV-36 T7).
- The refusal: `NoPackageInForce`, a checked exception carrying the message identifier MSG-P3-027 and the package code, non-retryable in the activity (Temporal and Drools design slide 28).
- The inputs the kit depends on: the parameter `drools.kiebase.cache.max`, with the default of 20, through the parameters contract of rwb-case, and the event `RulePackageInForce` on `rwb.decision.events.v1` through an inbox.
- The versioning and compatibility rule of the contract, and a kit fake that answers all four interfaces and every example of this document.

The kit is platform, not one of the 19 services: it has no `rwb_<short>` schema, no topic of its own, no task queue and no REST base. Its two consumed operations belong to rwb-decision (P7) and rwb-case (P3), and the store it no longer owns stays with rwb-decision under the Ownership Map ruling. The story has no build dependency and starts on Day 1.

### 2. Business rationale

The legacy story could assume the model was a row in the same database and the evaluator was in the same process, so the shape of what the evaluator reads was never a contract. After the split the model arrives over a service boundary and is embedded in 19 processes, which means the shape, the checksum rule and the refusal have to be agreed before any service writes its activity — otherwise each service either wraps a different assumption about the payload or, worse, reads the store directly, which the schema-per-service rule forbids (DP-01).

The contract is also what makes the audit promise of Architecture v5 slide 27 achievable at all. "Every answer names the version used" only holds if the result carries the package code, the version label and the rule ID in a fixed shape, if the version in force is derived from a date the caller passes, and if a missing version is a refusal rather than a default decision. Writing those three things down, with the message identifier MSG-P3-027 kept unchanged from the legacy build, keeps the decision record and the governance report readable across the migration.

Finally, the fake is the Day-1 unblocker. The governance stories of rwb-decision produce the first approved models later in the wave; with the kit fake and the model fake, all 19 services and the integration harness can build and test their `EvaluateRules` activity against the same documents, and the contract test that pins them runs in every build (Template and Rules §R5.4, class C).

### 3. Preconditions

- The governance side is fixed: rwb-decision governs rule models — authoring, tests, four-eyes approval, effective dating and one-call rollback — and keeps the central decision ledger (Architecture v5 slides 27 and 41; Temporal and Drools design slide 15).
- The model fetch is named by Architecture v5 slides 14 and 27 and by Temporal and Drools design slide 15 as `GET /rule-models/{n}/{v}`, served by rwb-decision, the owner of the operation, under /api/recovery/decision/v1 by the naming rule of Template and Rules §R4; API Specification v5 must still carry the path. The phase-1 package format is the XLS decision table compiled to DRL, with DMN 1.6 as the later target.
- The store tables — `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` — are rwb-decision's under the Ownership Map ruling; this contract declares no table and no migration.
- The KIE runtime libraries are the approved set only: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support; no KIE Server, no Business Central and no KJAR (legacy section 3, T3).
- The parameters contract of rwb-case serves `drools.kiebase.cache.max`, whose documented default is 20 (DP-06; legacy section 3).
- The event catalogue fixes `RulePackageInForce` as an event of rwb-decision on `rwb.decision.events.v1` (Architecture v5 slides 14, 42 and 43).
- The local decision-record library and its topic are the caller's, not the kit's: `rwb.decision-record.v1` carries `DecisionRecorded` (DP-03; Architecture v5 slide 28).
- The naming rule of Template and Rules §R4 applies to the services this contract points at, not to the kit; the kit declares no path of its own.
- No approval is required to publish a Draft contract: the surface is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

### 4. Flow

1. The contract author writes the interface document: the four interfaces with their signatures, the result fields, the refusal and the rule that no Drools type crosses them.
2. The author writes the model schema for the fetch: package code, version label, checksum, the ordered rows and the catalog projection of each row, with one worked example that uses the values of the legacy criteria — ALLOCATION, ALLOC-2026.12, ALLOC-031, MTG-BKK-CO.
3. The author writes the version-in-force rule and the refusal into the same document, and generates the version-selection example from the two legacy version labels ALLOC-2026.11 and ALLOC-2026.12 with the boundary at 2026-12-15.
4. The author writes the two consumed inputs — the cache parameter through the parameters contract and the `RulePackageInForce` event — with the consumer schema and the inbox dedupe rule.
5. The lint and schema steps run: the interface signatures validated against the legacy published interfaces, no Drools type in a published signature, the model schema validated with a non-empty ordered-row list and a mandatory checksum, the refusal carrying a message identifier, and a personal-data scan over every example.
6. The kit fake is generated from the document: it answers the four interfaces from the rwb-decision model fake, the rwb-case parameter fake and the decision-record fake, including a no-version-in-force example, a bad-checksum example and a two-version sequence.
7. The contract test runs the fake against the document on every change and fails the build when a signature, a field, the refusal or the versioning rule drifts.
8. The document and the fake are published to the contract registry at v1; RWB-PLT-E1072-APP and each consuming service pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A published signature exposes a KieBase, a KieSession or any Drools type | The lint step fails the build and the document is not published | Lint finding, no message id | AC1 |
| X2 | The model schema is published without a checksum, or with an unordered row list | The schema validation fails the build; every model version carries a checksum and an ordered row list | Lint finding, no message id | AC2 |
| X3 | A contract example carries a customer name, an account number, a national identifier or an email address | The scan rejects the example; codes and role codes only | Review finding | AC2 |
| X4 | A breaking change is made to a published interface, a result field or the refusal | The change raises v2 and marks v1 deprecated; v1 is never edited in place | Deprecation notice | AC3 |
| X5 | The refusal is published without the message identifier MSG-P3-027, or as a retryable failure | The lint step fails the build; the refusal keeps the identifier and stays non-retryable | Lint finding, no message id | AC4 |
| X6 | A value the consumers need is named by no source — the fetch response shape, the artefact coordinates, the message catalogue of a refused fetch | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1414; ASM-2470) | None; the gap stays open under GAP-1414 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and a fake; builds against nothing, reads no business data, and starts on Day 1 |
| Negotiable | Field order inside the model payload, the transport of the artefact and the example values are open until the version is frozen; the signatures, the checksum, the version-in-force rule and the refusal are fixed |
| Valuable | All 19 services and the integration harness can build and test their activity before any approved model exists |
| Estimable | Four interfaces, one model schema, one refusal, two consumed inputs, one fake and one contract test |
| Small | One sprint for the documents, the fake and the lint rules |
| Testable | Each criterion in section 7 is one schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: the embedded rules kit contract

  Background:
    Given the kit is platform, not one of the 19 services, and publishes no REST base, no topic and no queue of its own
    Given the rule package store stays with rwb-decision and the kit keeps only an in-memory cache

  Scenario: AC1 The four interfaces are published and no Drools type crosses them (new, D-RCV-60)
    Given the interface document of the kit contract
    When it is validated and linted
    Then it publishes RuleEvaluator.evaluate(String packageCode, Object facts, LocalDate onDate), RuleResult with packageCode, packageVersion, ruleId and outputs, RuleCatalog.row(String ruleId, String packageVersion) and RuleRow with ruleId, packageVersion, actionText, ownerRole, timerSpec and outputs
    Then RuleEvaluator declares NoPackageInForce as its checked refusal and no other thrown type
    Then no published signature mentions a KieBase, a KieSession, a KiePackage or any other Drools type

  Scenario: AC2 The fetched model shape is published with its checksum and its ordered rows (new, D-RCV-60)
    Given the model schema of GET /api/recovery/decision/v1/rule-models/{n}/{v} on rwb-decision
    When the schema and its example are validated
    Then the response carries packageCode, packageVersion, checksum, the ordered rows of the version and the catalog projection of each row
    Then each catalog projection carries action_text, owner_role, timer_spec and outputs, which is what RuleCatalog answers from
    Then the example uses ALLOCATION, ALLOC-2026.12, 26 ordered rows and rule ALLOC-031 with targetQueueCode "MTG-BKK-CO", and the schema declares the checksum mandatory
    Then the payload carries no workbook, no case data and no personal data

  Scenario: AC3 The version in force is chosen by the caller's date and the versioning rule is published (new, D-RCV-60)
    Given the version-in-force section of the document and the two worked examples
    When the rule is applied to 2026-12-14 and to 2026-12-15
    Then ALLOC-2026.11 is in force on 2026-12-14 and ALLOC-2026.12 on 2026-12-15, and the chosen label is returned in RuleResult
    Then the evaluation date comes from the caller and never from the system clock
    Then a published interface change raises v2 and deprecates v1, and a model version is never edited in place

  Scenario: AC4 The refusal is published with MSG-P3-027 and stays non-retryable (new, D-RCV-60)
    Given the refusal section of the document
    When it is linted against the message catalogue
    Then NoPackageInForce carries messageId MSG-P3-027 and the package code
    Then the refusal is declared non-retryable for the activity, so a workflow stops and alerts instead of retrying
    Then the document states that a missing version is never a default decision and never a silent fallback to an earlier version

  Scenario: AC5 The parameter and event inputs are published (new, D-RCV-60)
    Given the inputs section, the consumer schema and the parameters reference
    When they are validated
    Then the cache bound is read as drools.kiebase.cache.max through the parameters contract of rwb-case, with 20 as the documented default and never as a code constant
    Then rwb.decision.RulePackageInForce.v1 is consumed from rwb.decision.events.v1 through an inbox that dedupes by event identifier
    Then the payload carries the package code, the version label and the in force at, with identifiers and facts only

  Scenario: AC6 The kit fake answers the document and the contract test pins it (new, D-RCV-60)
    Given the kit fake generated from the document
    When the contract test runs it over the rwb-decision model fake, the rwb-case parameter fake and the decision-record fake
    Then it answers the four interfaces, the ALLOCATION ALLOC-2026.12 example with rule ALLOC-031, the two-version sequence, the no-version-in-force example and the bad-checksum example
    Then the signatures, the model fields, the refusal and the message identifier in the fake equal those in the document
    Then a breaking change raises v2 and marks v1 deprecated, and no consumer sees an edited v1

  Scenario: AC7 The store stays with rwb-decision and the decision record stays the caller's (new, D-RCV-60)
    Given the ownership rule of the kit and the decision-record example
    When the kit contract is validated
    Then the kit reads no rule table and no schema it does not own, and the store stays with rwb-decision
    Then the kit returns the rule ID and the package version to the caller and writes no ledger of its own

  Scenario: AC8 Every business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules table of section 8 with BR1 to BR11
    When the coverage of the rules is checked against sections 7 and 16
    Then each rule BR1 to BR11 names at least one criterion and at least one test case

  Scenario: AC9 A status change the model does not allow is refused (new, D-RCV-60)
    Given a status change that the model does not allow
    When the caller submits it to apply the state
    Then the change is refused and no state, decision record or outbox row is written
```

These criteria are new and test only the contract deliverable: no legacy acceptance criterion is repeated here — AC1 to AC7 of RWB-E1-072 belong to RWB-PLT-E1072-APP — and every number and identifier comes from the legacy story, Architecture v5 or the Temporal and Drools design, character for character.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | The kit publishes four interfaces and nothing else: `RuleEvaluator`, `RuleResult`, `RuleCatalog` and `RuleRow` | RWB-E1-072 section 12; Temporal and Drools design slide 16 | AC1; TC-PLT-E1072-CON-01 |
| BR2 | No KieBase, KieSession, KiePackage or other Drools type crosses a published interface; the kit is the only holder of the runtime | Temporal and Drools design slides 11 and 16 | AC1; TC-PLT-E1072-CON-01 |
| BR3 | The model payload carries the package code, the version label, the checksum, the ordered rows and the catalog projection, and the checksum is mandatory | Architecture v5 slide 27; Temporal and Drools design slide 15 | AC2; TC-PLT-E1072-CON-02 |
| BR4 | The version in force is chosen at evaluation time from the caller's date and the valid-from and valid-to dates, and the chosen label is returned | D-RCV-36 T7; Temporal and Drools design slides 14 and 15 | AC3; TC-PLT-E1072-CON-03 |
| BR5 | A missing version is the refusal `NoPackageInForce` with MSG-P3-027, non-retryable, and never a default decision | R-UNI-41; REQ-CWC-008; Temporal and Drools design slide 28 | AC4; TC-PLT-E1072-CON-03 |
| BR6 | The cache bound is read as `drools.kiebase.cache.max` through the parameters contract, with 20 as the documented default and never as a code constant | DP-06; REQ-DRI-010; legacy section 3 | AC5; TC-PLT-E1072-CON-04 |
| BR7 | `RulePackageInForce` is consumed on `rwb.decision.events.v1` through an inbox that dedupes by event identifier | DP-14; Architecture v5 slides 14 and 43 | AC5; TC-PLT-E1072-CON-04 |
| BR8 | The store stays rwb-decision's: a consumer of this contract reads no rule table and no schema it does not own | DP-01; Ownership Map ruling on `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` | AC7; TC-PLT-E1072-CON-06 |
| BR9 | A breaking change raises a new version and deprecates v1; a published interface is never edited in place | Template and Rules §R7.2; §R5.4 class C | AC3, AC6; TC-PLT-E1072-CON-03, TC-PLT-E1072-CON-05 |
| BR10 | The message identifier MSG-P3-027 is kept unchanged from the legacy build, although the store and the governance now sit with rwb-decision | asm | AC4; TC-PLT-E1072-CON-03 |
| BR11 | The decision record is the caller's: the kit returns the rule ID and the package version and writes no ledger of its own; the caller records the decision and applies the state in one RecordAndApply activity, with the decision record, the state and the outbox row in one transaction under ADR-022, and the version 3 order of WriteDecisionLogActivity then ApplyStateActivity is superseded | DP-03; Architecture v5 slide 28; ADR-022 | AC7; TC-PLT-E1072-CON-06 |

### 9. State transitions

None in this story: a document has no runtime state. Two vocabularies are fixed here, and the runtime behind them is specified in RWB-PLT-E1072-APP section 9:

| Object | State | Meaning in the contract |
|---|---|---|
| Cache entry of a version | ABSENT | No KieBase is held for that version in the service process |
| Cache entry of a version | CACHED | The model was fetched, its checksum matched and the KieBase is held inside the bound |
| Cache entry of a version | REFUSED | The checksum did not match, or the fetch failed; the version never serves an evaluation |
| Cache entry of a version | EVICTED | The bound was reached and this entry was the least recently used |
| Package version, governance | LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED | rwb-decision's states, fixed by the governance contract; this contract only reads the one in force for a date |

The governance states are named here so that the two documents agree on the vocabulary; the transitions among them, the effective dating and the rollback are the rwb-decision governance contract's business, not this story's.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the interface document, the model schema, the refusal section and the fake |
| The platform owner of the library | Approves a breaking change and freezes a version |
| The service teams of the 19 services | Consume the contract, pin the version, raise a change request rather than a private variant |
| The rwb-decision owner (P7) | Confirms the fetch path, the model fields, the version label shape and the event payload it publishes |
| The rwb-case owner (P3) | Confirms the parameters operation and the catalog entry for the cache bound |
| RW-COE | Owns the rule content of the packages; may not change the contract |
| RW-RISK | Approves rule packages in rwb-decision; has no right in the contract |
| RW-PLATADM | Receives the incidents the contract requires a service to raise |
| No delegation of authority level applies | A library contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in a document, a schema, an example or the fake. Where a caller or an operator must be named, the example uses a role code or a user identifier only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The documents publish signatures, model fields, codes, status values and message identifiers; no customer, account, case or document value appears | None owned by this contract |
| Model payload | Package code, package version label, checksum, the ordered rows of the version and the catalog projection of each row: action text, owner role, timer spec and outputs | None owned by this contract |
| Row content in an example | Rule identifiers, queue codes, role codes, a timer spec such as 3d and an output map; no business value beyond the legacy example | None owned by this contract |
| Personal data | None. No name, no email address, no account number, no national identifier and no document content in a schema, an example or the fake | None owned by this contract |
| Tables published | None. The store stays rwb-decision's and this document declares no table and no migration | None owned by this contract |
| Field identifiers | None owned. The projection fields belong to rwb-decision's own model, and the record fields to the decision-record library | None owned by this contract |
| Retention | None at the contract: a document keeps no data, and the fake holds only the examples it publishes | None owned by this contract |
| rule_package_version and artifact payload (GAP-2439) | Not specified in the source documents (GAP-2439). Physical columns are taken from the Logical Data Model and Data Dictionary at implementation | None owned by this contract |

The model payload is the one place where a rule value could leak into a contract, so the document fixes that the payload carries the approved model and its projection, and never the workbook, the case data or a personal field (Architecture v5 slides 27 and 35).

### 12. Contract

**12.1 REST operations provided**

None. The kit is a library: it publishes Java interfaces and a model schema, not an OpenAPI document, and it has no REST base of its own. The endpoint the legacy story declared for the package list belongs to rwb-decision and is published by the governance contract (RWB-P7-E1073-CON); the Epic 8 administration screen reaches it through the gateway route of RWB-PLT-N001-CON, which this contract names and does not declare (DP-19).

**12.2 REST operations consumed**

| Operation | Provider | Why the contract needs it | Pattern |
|---|---|---|---|
| GET /api/recovery/decision/v1/rule-models/{n}/{v} | rwb-decision (P7) | The source of every model the kit loads: package code, version label, checksum, the ordered rows and the catalog projection | DP-04, DP-11 |
| GET /api/recovery/case/v1/admin/parameters | rwb-case (P3) | The source of `drools.kiebase.cache.max`, so the cache bound is data and not a code constant | DP-06, DP-11 |

Two consumption rows, both one hop, with a 2 s timeout and a breaker per provider. The fetch path is named on Architecture v5 slides 14 and 27, but no source states the response shape and the Ownership Map holds no row for the path, so the field list published here is the working read of ASM-2467, recorded with GAP-1413. The value 20 published as the default of the cache bound is the legacy default, read through the parameters contract and never hard-coded (ASM-2469).

**12.3 Events published**

None. The kit has no topic, and `DecisionRecorded` on `rwb.decision-record.v1` is the local decision-record library's event, published by the caller's service, not by the kit (RWB-PLT-E1027-CON).

**12.4 Events consumed**

| Event | Topic | Message schema | Payload carries | Purpose |
|---|---|---|---|---|
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | RulePackageInForce | Rule package code, version label, in force at | Tells the kit that a model version must be fetched, verified and swapped in |

One consumed message schema, through an inbox that dedupes by event identifier, keyed by the package identifier, with identifiers and facts only. The event is rwb-decision's and is also named on Architecture v5 slide 14; the consumer list of slide 43 covers four services while DP-04 embeds the kit in every service, and every service that holds a model, rwb-asset included, subscribes to `RulePackageInForce` on `rwb.decision.events.v1` through its own inbox, as recorded with GAP-1413.

**12.5 Workflows and activities**

None. The kit owns no queue and starts no workflow. It is called inside the caller's own `EvaluateRules` activity, on that service's queue, and the contract states explicitly that a workflow class never calls `RuleEvaluator`, so replays reuse the recorded answer (Temporal and Drools design slides 12, 14 and 27).

**12.6 Schedules**

None. The promotion of a version is JOB-20, a Schedule in rwb-decision, which publishes `RulePackageInForce` at 00:01; the kit owns no Schedule and reacts only to that event (Architecture v5 slide 44; Temporal and Drools design slide 15).

**12.7 Tables owned**

None. `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay with rwb-decision (P7) under the Ownership Map ruling, with the migration and the seed of the phase-1 package codes; the kit keeps only an in-memory cache (Ownership Map, ASM-0069; Architecture v5 slide 41). This document therefore declares no table, no column and no migration, and no consumer of it may read a rule table.

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| kit fake (this story) | The four interfaces, the model shape, the refusal and every example, answered from the owner fakes below | RWB-PLT-E1072-APP, every service's activity tests, the integration harness |
| rwb-decision rule-model fake (RWB-P7-E1073-CON) | GET /api/recovery/decision/v1/rule-models/{n}/{v}, with the checksum, the ordered rows and the projection, a bad-checksum variant and a slow variant | AC2, AC3 and AC6; the fetch-failure example |
| `RulePackageInForce` event fake (rwb-decision) | The event on `rwb.decision.events.v1`, for one version and for two versions in sequence | AC5 and the two-version sequence |
| rwb-case parameter fake (RWB-P3-E1042-CON) | GET /api/recovery/case/v1/admin/parameters, with the cache bound at 20, raised and missing | AC5 |
| decision-record fake (RWB-PLT-E1027-CON) | The local record write and `DecisionRecorded` on `rwb.decision-record.v1` | AC6 |

The kit fake answers from the owner fakes rather than from copied payloads, so a change to the rwb-decision model shows up as a contract-test failure in the kit rather than as a surprise in a service at run time.

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the kit provides interfaces, not operations | 2 consumption rows over 2 providers | OpenAPI 3.1 at the owners, one hop, 2 s timeout, breaker per provider |
| Kafka | 0 published | 1 consumed message schema | AsyncAPI 3.0, CloudEvents 1.0, inbox dedupe by event identifier, keyed by package identifier |
| Temporal | 0 | 0 | The kit starts no workflow and owns no queue |
| File | 0 | 0 | No file crosses the contract; the workbook stays in the governance path |

### 13. Solution plan

**Hardware and software change.** The contract records the move of the Drools runtime from one module's runtime to an embedded library in every service (Architecture v5 slide 27; Temporal and Drools design slides 11 and 12): the same approved KIE libraries, packaged once as a shared dependency, loaded with a model that arrives over a contract and checksum-verified before use, with the KieBase built once per version and held in an LRU cache inside each service process. Governance stays central in rwb-decision (P7), which owns the store and every state of a package version, so this contract fixes only what crosses the library boundary: the four interfaces, the model payload, the version-in-force rule, the refusal, the two inputs and the fake. Nothing here creates a shared rules server, and nothing here lets a service read `rule_row`: the catalog projection travels with the model.

**Deliverables.** The interface document (the four interfaces, their signatures, the result fields and the refusal), the model schema with its example, the version-in-force section with its two worked examples, the consumer schema for `RulePackageInForce`, the parameters reference for the cache bound, the kit fake, the lint rules and the contract test. The artefact coordinates of the library — the group and the artefact name it is published under — are Not specified in the source documents (GAP-1414; ASM-2470); the contract keeps the legacy interface shapes and the Java package of the legacy story, and the coordinates come from the platform library baseline rather than from this document and are recorded on this contract at the version freeze. The refusal of a model fetch stays MSG-P3-027, unchanged and non-retryable, with its {check} and {detail}; its HTTP status codes and problem type come from rwb-decision's own document when it exists.

**Interface surface**

| Interface | Signature | Returns |
|---|---|---|
| `RuleEvaluator` | `RuleResult evaluate(String packageCode, Object facts, LocalDate onDate) throws NoPackageInForce` | One result for the one rule that fired |
| `RuleResult` | `RuleResult(String packageCode, String packageVersion, String ruleId, Map<String, Object> outputs)` | The rule and the version that decided |
| `RuleCatalog` | `RuleRow row(String ruleId, String packageVersion)` | The projection of one row of one version |
| `RuleRow` | `RuleRow(String ruleId, String packageVersion, String actionText, String ownerRole, String timerSpec, Map<String, Object> outputs)` | The catalog fields the legacy story names |
| `NoPackageInForce` | checked exception with `messageId` MSG-P3-027 and the package code | The refusal, non-retryable in the activity |

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | this story provides the kit contract, so the kit row adds no dependency of its own; C RWB-P7-E1073-CON for the governance contract |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows the legacy markers call for. DP-04 is the row this pair of stories is itself: the embedded kit is delivered by this contract and its app story, so the only added dependency left is the C row for the governance contract. DP-19 is named because the Epic 8 rule administration screen reads the models through gateway-bff; that screen is out of scope and no path of it is declared here.

**Build steps**

1. Write the interface document with the four interfaces, the result fields and the refusal, taken from the legacy published interfaces character for character.
2. Write the model schema with the checksum mandatory and the ordered rows, and the example of ALLOCATION ALLOC-2026.12 with 26 rows and rule ALLOC-031.
3. Write the version-in-force section with the two worked examples of ALLOC-2026.11 and ALLOC-2026.12 and the boundary at 2026-12-15.
4. Write the refusal section with MSG-P3-027, the non-retryable rule and the no-default-decision rule.
5. Write the inputs section: the parameters reference for `drools.kiebase.cache.max` with the default 20, and the consumer schema for `RulePackageInForce`.
6. Add the lint rules: no Drools type in a published signature, a mandatory checksum, an ordered non-empty row list, a message identifier on the refusal, and a personal-data scan over every example.
7. Generate the kit fake over the rwb-decision model fake, the rwb-case parameter fake and the decision-record fake, and write the contract test that pins the signatures, the fields, the refusal and the message identifier.
8. Publish v1 to the contract registry, notify RWB-PLT-E1072-APP and the consuming services, and record the version they pin.

**Done when.** The documents and the schema validate, every lint rule passes, the fake answers all four interfaces and every example including the refusal and the two-version sequence, the contract test is green on the build of this story, and the four consuming services have pinned v1.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-027 | No version of the package is in force for the caller's date, or the checksum of a fetched version does not match | The rule version was refused at the {check} check: {detail}. | `NoPackageInForce`, messageId MSG-P3-027, non-retryable in the activity |
| PLT-RULES-001 | The model fetch fails, answers a non-success status or exceeds 2 s | The kit keeps the last good model and raises an incident; the title and detail text are Not specified in the source documents (GAP-1414; ASM-2470) | Incident, no user-facing text |
| PLT-RULES-004 | The fetch returns a version the caller did not ask for, or a version with no ordered rows | The version is refused with MSG-P3-027 for the checksum or schema check; the kit never builds a model from a payload that does not match the request | `NoPackageInForce`, messageId MSG-P3-027 |

For a checksum mismatch, {check} is "checksum" and {detail} names the package code and the version label only, never the DRL or a payload (legacy section 14). MSG-P4-002, the refusal of a role without the Rules and parameters right, is not republished here: it belongs to the rwb-decision governance contract, where the package list endpoint now lives. The refusal keeps the message identifier MSG-P3-027 unchanged although the store and the governance now sit with rwb-decision; no source renumbers it, and renumbering would break every decision record and every governance report that cites it (ASM-2471).

### 15. Screens and states

No screen in this story, and the contract declares none. The kit has no user interface at all: it answers inside an activity and the screens read the result through the owning service. The package list the legacy story declared and the Epic 8 rule administration screen belong to rwb-decision and to Epic 8 (FEAT-ADM-02), reached through the gateway route of RWB-PLT-N001-CON; the screen is out of scope here, and this story fixes the four cache-entry states of section 9 so that the app story's operability view has one vocabulary.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1072-CON-01 | AC1 (BR1, BR2) | Contract | The interface document validated and linted; the four signatures compared against section 13; the checked refusal; no Drools type in any published signature |
| TC-PLT-E1072-CON-02 | AC2 (BR3) | Contract | The model schema validated; the ALLOCATION ALLOC-2026.12 example with 26 ordered rows, the checksum mandatory, the ALLOC-031 projection with targetQueueCode "MTG-BKK-CO"; a personal-data scan |
| TC-PLT-E1072-CON-03 | AC3, AC4 (BR4, BR5, BR9, BR10) | Contract | The two worked examples of ALLOC-2026.11 and ALLOC-2026.12 at the 2026-12-15 boundary; the refusal carrying MSG-P3-027; the non-retryable rule; the versioning and deprecation rule |
| TC-PLT-E1072-CON-04 | AC5 (BR6, BR7) | Contract | The parameters reference for `drools.kiebase.cache.max` with the default 20; the `RulePackageInForce` consumer schema with the inbox dedupe and a payload of identifiers and facts |
| TC-PLT-E1072-CON-05 | AC6 (BR9) | Component | The kit fake over the rwb-decision model fake, the rwb-case parameter fake and the decision-record fake; all four interfaces and every example, including no-version-in-force and bad-checksum; a breaking change raises v2 and deprecates v1 |
| TC-PLT-E1072-CON-06 | AC7 (BR8, BR11) | Contract | The kit reads no rule table and no schema it does not own; the decision record carries the rule ID and package version and the kit writes no ledger of its own |
| TC-PLT-E1072-CON-07 | AC8 (BR1 to BR11) | Contract | Not specified in the source documents (NEWAC-RWB-PLT-E1072-CON-AC8) |
| TC-PLT-E1072-CON-08 | AC9 | Contract | Not specified in the source documents (NEWAC-RWB-PLT-E1072-CON-AC9) |

### 17. Guardrails

- No Drools type crosses a published interface: the runtime stays behind the evaluator, and the lint step fails the build otherwise.
- No business value in the contract: package codes, rows, salience and outputs are rwb-decision's data, and the only number this document fixes is the documented default 20 of the cache bound.
- No personal data in a schema, an example, a fake or a log: identifiers, role codes and queue codes only, and the scan fails the build otherwise.
- No table and no migration in this contract: the store is rwb-decision's, and a consumer that reads it breaks both DP-01 and the schema-per-service rule.
- The checksum is mandatory and the row list is ordered: a model without either is refused, never built.
- A missing version is a refusal with MSG-P3-027 and never a default decision or a silent fallback.
- The kit writes no ledger: the rule ID and the package version go into the caller's decision record through the decision-record library.
- No workflow code calls the evaluator; the contract says so explicitly and the app story's architecture test enforces it.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.
- No aggregation of another service's model: each service loads only the versions of the packages it evaluates.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-CWC-016 | Every workflow event logged with its rule ID and version | RWB-E1-072 section 18 (Epic 1, 3.3; Program, 5.3) | TC-PLT-E1072-CON-01, TC-PLT-E1072-CON-02 |
| REQ-DRI-001 | One record per decision with the seven field groups | RWB-E1-072 section 18 (Epic 1, 3.7) | TC-PLT-E1072-CON-01, TC-PLT-E1072-CON-03 |
| REQ-DRI-004 | Epic 1 records use versioned rules | RWB-E1-072 section 18 (Epic 1, 3.3; Program, 5.7) | TC-PLT-E1072-CON-03 |
| REQ-DRI-011 | Versioned tables with valid from and to, author and approver | RWB-E1-072 section 18 (Epic 1, 4; Program, 5.7) | TC-PLT-E1072-CON-03, TC-PLT-E1072-CON-04 |
| REQ-DRI-010 | The KieBase is built once per package version and cached, bounded by the cache parameter | RWB-E1-072 section 8 BR7 and section 13 | TC-PLT-E1072-CON-04 |
| REQ-CWC-008 | No package in force is a refusal, never a default decision | RWB-E1-072 section 8 BR9 (R-UNI-41) | TC-PLT-E1072-CON-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1072-APP | App development | H consumer: implements the four interfaces, the loader, the cache and the evaluator against this contract and its fake |
| RWB-PLT-E1027-CON | Contract | Referenced by the app story: the local decision-record library the caller writes the rule ID and version through; also the C row of the legacy dependency. This contract adds no build dependency of its own |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | Referenced by the app story: the parameters and reference-data clients the kit calls |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON | Contract | Referenced by the app story: the naming library and the per-service Flyway baseline the kit's artefacts follow |
| RWB-PLT-N001-CON | Contract | Referenced by the app story: the gateway route the Epic 8 rule administration screen will use; no path is declared here |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the owner contracts behind the two consumed reads |
| RWB-P7-E1073-CON | Contract | C: the governance contract that produces the models and publishes the event; it also carries the package list endpoint the legacy story declared |
| RWB-P7-E1027-CON | Contract | C: the owner contract of the decision-record entry the central ledger collects |

### 19. Out of scope

- The kit implementation — the loader, the cache registry, the evaluator, the catalog and the agenda listener: RWB-PLT-E1072-APP.
- The rule package store and the governance of a version — upload, load checks, the at-least-50-scenario gate, four-eyes approval, effective dating, rollback and the package list endpoint: the rwb-decision governance stories (RWB-P7-E1073-CON and its app story).
- The decision-record entry, the central ledger and the hash chain: RWB-PLT-E1027-CON and rwb-decision.
- The parameters catalog and its API: RWB-PLT-E1042-CON and rwb-case; the reference data and the LOV: RWB-PLT-E1043-CON and rwb-case.
- The naming library and the codec of topic names: RWB-PLT-E1047-CON; the per-service Flyway baseline and the schemas: RWB-PLT-E1044-CON and the DB stories.
- The gateway route and the Epic 8 rule administration screen: RWB-PLT-N001-CON and Epic 8 (FEAT-ADM-02).
- The Temporal cluster, the namespace, the worker platform and the activity contracts of each service: the workflow platform stories and each service's own story.
- Any rule content, condition, salience or output value, and the Epic 2 packages and the rest of the route sets: rwb-decision and the epics that own them.
