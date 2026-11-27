# RWB-PLT-E1072-APP Drools runtime and rule package store

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split (rework) of RWB-E1-072. The embedded Drools runtime becomes the shared rules kit of every service, the rule package store stays with rwb-decision, and the legacy criteria AC1 to AC7 are carried whole. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-E1072-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1072-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-072 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP06, DP07, DP11, DP13, DP14, DP15, DP19 |
| Parallel lane | L-PLT-LIB-I |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1072-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1047-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015, FR-PLT-016, FR-PLT-017, FR-PLT-018, FR-PLT-020) |
| Status | Draft (realignment v1) |

### 1. Story

As a **service team building the EvaluateRules activity of its own service**, I want **the embedded rules kit to fetch the approved model version of a package from rwb-decision, verify it, build it once and answer with the rule and the version that decided**, so that **all 19 services decide by the same evaluator, keep the last good model when a new one fails to load, and every decision record names the rule and the package version behind it, with no shared rule server on the hot path**.

This is the split (rework) slice of legacy key RWB-E1-072 under epic RWB-PLT-LIB (Template and Rules §R6). No legacy section is copied word for word and no delta copy of an as-built story is made: the microservice change for this legacy key is described here, and the legacy criteria AC1 to AC7 are carried in section 7. The change from the legacy story:

- **Runtime placement.** The KIE runtime stops being the runtime of one module inside a single application and becomes a shared library embedded in every service (Architecture v5 slide 27; Temporal and Drools design slides 11 and 12). The library is the only place that holds a KieBase; no caller receives a KieBase, a KieSession or any Drools type.
- **Store.** `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` stay with rwb-decision (P7) under the Ownership Map ruling, together with authoring, the load checks, the at-least-50-scenario gate, four-eyes approval, effective dating and one-call rollback. The kit owns no table and keeps only an in-memory cache (DP-01).
- **Model fetch.** The kit asks rwb-decision for the approved model of a package version over REST, verifies the checksum before the model may be used, and swaps it in atomically; a model that fails to load leaves the last good model in force (Architecture v5 slides 14 and 27; Temporal and Drools design slide 15).
- **Catalog.** The catalog projection — action text, owner role, timer spec and outputs — comes with the fetched model, so the kit never reads `rule_row` and no service reads another service's table (DP-01, DP-04).
- **Cache.** One KieBase per package version, built once, held in an LRU cache bounded by `drools.kiebase.cache.max`, which is read through the parameters contract and is not a code constant (DP-06; legacy BR7).
- **Evaluation.** The evaluator runs only inside an activity, under 300 ms, and the package version is chosen at evaluation time from the caller's business date, never from the system clock (Temporal and Drools design slides 14, 15 and 27).
- **Decision record.** The caller writes the rule ID and the package version through the local decision-record library and its topic `rwb.decision-record.v1`; the kit never writes a ledger of its own (DP-03; Architecture v5 slide 28).
- **Left with the governance story.** The read authorities of section 10 keep their meaning, but the package list endpoint, the upload, the approval and the rollback are the rwb-decision governance stories, not this one.

The kit is platform, not one of the 19 services: it has no `rwb_<short>` schema, no `rwb.<short>.events.v1` topic of its own, no `rwb-<short>` task queue and no REST base of its own. It is a library that runs inside each service's own process and inside that service's own Temporal worker (Architecture v5 slide 20).

### 2. Business rationale

The legacy story put the Drools runtime and the rule package store in one module and served every engine from it, which worked only because the whole module was one application with one database session. After the split there are 19 services, each with its own schema, its own worker and its own release, and the rules must still behave identically everywhere, so two things have to hold at once: an answer must be the same wherever it is asked, and every answer must name the model version that produced it.

Architecture v5 answers both by moving evaluation into the owning service and keeping governance central: the approved model is copied to each service, loaded inside an activity, verified against its checksum and swapped atomically, while the last good model keeps running if a new one fails (slide 27). That removes the shared rule server from the hot path — a single evaluator that every decision depends on would be a single point of failure for 283 to 318 thousand evaluations a month against a target under 300 ms — and it keeps the audit promise, because the model name and version go into the decision record (slides 27 and 28).

This story is the kit itself, and it is the only story that has to exist before any service can evaluate a rule: 14 of the 19 services own at least one package, and every one of them calls the same interfaces. Without it each service would either invent its own evaluator, and the same rows would behave differently in two engines, or read `rule_row` directly, which the schema-per-service rule forbids (DP-01). The legacy measures become the kit's acceptance ground: the AC1 to AC7 answers of RWB-E1-072 must still hold, now with the model fetched over a contract instead of read from a local table.

### 3. Preconditions

- RWB-PLT-E1072-CON is published: the `RuleEvaluator`, `RuleResult`, `RuleCatalog` and `RuleRow` interfaces, the fetched model shape, the refusal, the versioning rule and the kit fake.
- RWB-PLT-E1027-CON is published: the local decision-record library and the topic `rwb.decision-record.v1` that carries `DecisionRecorded` (DP-03).
- RWB-PLT-E1042-CON is published: the parameters client that reads `drools.kiebase.cache.max` (DP-06).
- RWB-PLT-E1043-CON is published: the reference-data client the rule rows are checked against (DP-07).
- RWB-PLT-E1047-CON is published: the naming library the topic and event names follow (DP-14).
- RWB-PLT-E1044-CON is published: the per-service Flyway baseline the kit's own artefacts are versioned against (DP-15).
- RWB-PLT-N001-CON is published: the gateway route the Epic 8 rule administration screen will use, so the kit names no path of its own (DP-19).
- rwb-decision (P7) publishes the model fetch named on Architecture v5 slide 14, and rwb-case (P3) publishes the parameters read; both are consumed through their contract fakes only (C dependencies).
- The KIE runtime libraries are the approved set: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support; no KIE Server, no Business Central and no KJAR is used (legacy section 3, T3).
- The parameter `drools.kiebase.cache.max` is 20 in the catalog and stays the default of the kit; the value is read, never coded (legacy section 3; ASM-2469).
- The caller builds its facts from its own data: the kit reads no case table, no ACE view and no other service's table (DP-01, DP-05).
- No approval is required to start: the story is Draft (realignment v1) and builds against the published contracts and their fakes.

### 4. Flow

1. At start-up the kit loads its configuration through the parameters client: the cache bound `drools.kiebase.cache.max` and the model-fetch timeout. It builds no KieBase at start-up and reads no table.
2. The service's `RulePackageInForce` consumer receives the event on `rwb.decision.events.v1` and hands the package code and the version label to the kit, which fetches that model over REST and verifies its checksum before the cache entry may be used.
3. A caller — the `EvaluateRules` activity of any service — builds its facts object from its own data and calls `RuleEvaluator.evaluate(packageCode, facts, businessDate)`.
4. The evaluator asks the cache for the KieBase of the version in force on that date; on a miss it fetches the model, verifies the checksum, compiles it once into a KieBase and caches it, evicting the least recently used entry when the bound is reached.
5. The evaluator inserts the facts, fires the package, and the agenda listener records the Drools rule name of the one rule that fired.
6. The evaluator returns one `RuleResult` with the package code, the package version, the rule ID and the outputs; nothing else crosses the interface.
7. The caller writes the decision record with the rule ID and the package version through the decision-record library, in the same transaction as its own state change, and then applies the action.
8. A caller that needs the catalog text of a row, rather than an evaluation, calls `RuleCatalog.row(ruleId, packageVersion)`; the projection comes from the fetched model and never from `rule_row`.
9. The kit exports the operability counters — builds, cache hits, evictions, refusals and fetch latency — to the platform metrics endpoint.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No version of the package is in force on the evaluation date | `NoPackageInForce` is thrown, the caller refuses the action and writes no decision record; the activity failure is non-retryable and the case waits with an alert | MSG-P3-027 | AC3 |
| X2 | The recomputed checksum of the fetched model differs from the checksum of the version | The version is refused at load into the cache, an incident is raised, and the previous version continues to serve every evaluation | MSG-P3-027 | AC6 |
| X3 | The model fetch fails, answers a non-success status, or exceeds the 2 s timeout | The breaker records the failure, the last good model for that package keeps serving, and an incident is raised; where no model was ever loaded, X1 applies | PLT-RULES-001 | AC5 |
| X4 | The cache bound is reached | The least recently used version is evicted before the new one is built; the build counter increases and the evaluation is not slowed on the next call for a version that is still cached | None | AC5 |
| X5 | The same `RulePackageInForce` event arrives twice | The inbox dedupes by event identifier, the second delivery rebuilds nothing and the cached KieBase is reused | None | AC5 |
| X6 | The parameter `drools.kiebase.cache.max` is missing from the catalog or the read fails | The documented default 20 applies, an alert is raised on the catalog, and the cache keeps serving | PLT-RULES-002 | AC5 |
| X7 | A workflow class calls `RuleEvaluator` directly | The architecture test of the build fails and the change is rejected; Drools is reached only inside an activity | PLT-RULES-003 | Guardrail, section 17 |
| X8 | An event names a version that was already superseded when it arrived | The kit fetches and caches that version but the evaluator keeps choosing by date; no evaluation is forced onto an older version | None | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against seven platform contracts and three rwb-decision and rwb-case contracts and their fakes; reads no business table and waits for no other story in the lane |
| Negotiable | The internal build strategy, the eviction bookkeeping and the metric names are configuration; the first-match rule, the checksum rule, the version-in-force rule and the refusal are fixed |
| Valuable | Every service evaluates by the same evaluator, keeps the last good model and names the rule and the package version on every decision |
| Estimable | One library, four published interfaces, one model loader, one cache registry, one evaluator, one catalog and one agenda listener |
| Small | One sprint for the kit, the loader, the cache and the tests |
| Testable | Each criterion in section 7 is one component or integration test in section 16, run against the kit fake and the rwb-decision and rwb-case fakes |

### 7. Acceptance criteria

```gherkin
Feature: Drools runtime and rule package store

  Background:
    Given package ALLOCATION version "ALLOC-2026.12" is in force with 26 rows
    Given the parameter drools.kiebase.cache.max is 20

  Scenario: AC1 Evaluation returns the rule and the package version (legacy RWB-E1-072 AC1)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given a mortgage case in region BKK with exposure band 3
    When SY-RULES calls RuleEvaluator.evaluate("ALLOCATION", facts, 2026-12-15)
    Then the result holds packageCode "ALLOCATION", packageVersion "ALLOC-2026.12" and ruleId "ALLOC-031"
    Then the outputs hold targetQueueCode "MTG-BKK-CO"
    Then the decision log entry carries rule ID "ALLOC-031" and rule version "ALLOC-2026.12"

  Scenario: AC2 The date picks the right version (legacy RWB-E1-072 AC2)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given version "ALLOC-2026.11" is valid from 2026-11-01 to 2026-12-14
    Given version "ALLOC-2026.12" is valid from 2026-12-15
    When the same facts are evaluated on 2026-12-14
    Then the result carries packageVersion "ALLOC-2026.11"
    When the same facts are evaluated on 2026-12-15
    Then the result carries packageVersion "ALLOC-2026.12"
    Then the evaluation date comes from the caller and not from the system clock

  Scenario: AC3 No version in force (legacy RWB-E1-072 AC3)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given no ALLOCATION version is IN_FORCE on 2026-12-20
    When SY-RULES evaluates a case for that date
    Then NoPackageInForce is thrown with MSG-P3-027 for the package in force check
    Then no decision log entry is written and the case is not moved

  Scenario: AC4 Exactly one rule fires (legacy RWB-E1-072 AC4)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given rows "ALLOC-031" and "ALLOC-032" both match the facts
    Given both rows share the activation-group ALLOCATION
    When the package fires
    Then exactly one rule fires, "ALLOC-031", with the salience from its row order
    Then the result holds one rule ID and no output of "ALLOC-032"
    When the same facts are evaluated 100 times
    Then "ALLOC-031" is the only rule that fires every time

  Scenario: AC5 The cache is reused (legacy RWB-E1-072 AC5)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given version "ALLOC-2026.12" is not in the cache
    When the evaluator runs twice with the same package version
    Then the KieBase is built once and the second call reads the cache
    Then the counter drools_kiebase_builds_total increases by one only
    Then the cache holds no more than 20 KieBases

  Scenario: AC6 Checksum mismatch (legacy RWB-E1-072 AC6)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given the recomputed SHA-256 of drl_source for "ALLOC-2026.13" differs from its checksum
    When the cache builds that version
    Then the version is refused at load into the cache with MSG-P3-027 for the checksum check
    Then no evaluation uses the version and an incident is raised to RW-PLATADM
    Then version "ALLOC-2026.12" stays in force and serves every evaluation

  Scenario: AC7 The catalog returns the row fields (legacy RWB-E1-072 AC7)
    Given the rwb-decision contract mock returns the ALLOCATION model version "ALLOC-2026.12" with 26 ordered rows, its catalog projection and its checksum
    Given row "ALLOC-031" of version "ALLOC-2026.12" has action_text "Assign to MTG-BKK-CO", owner_role "RW-CASEOWN", timer_spec "3d" and outputs {"targetQueueCode":"MTG-BKK-CO"}
    When RuleCatalog.row("ALLOC-031", "ALLOC-2026.12") is called
    Then it returns action_text, owner_role, timer_spec and outputs
    Then the read touches rule_row only and not the workbook or drl_source
```

AC1 to AC7 are the legacy criteria of RWB-E1-072, copied word for word with their origin tag, every value kept: ALLOCATION, ALLOC-2026.12, ALLOC-2026.11, ALLOC-031, ALLOC-032, MTG-BKK-CO, the 26 rows, the cache maximum 20, the dates 2026-12-14, 2026-12-15 and 2026-12-20, MSG-P3-027, the queue code, the owner role, the timer spec and the output map. The one added Given in each scenario is new and is the cross-service part: the model is fetched from rwb-decision instead of read from a local table, and the fetched model carries the same 26 ordered rows, its catalog projection and its checksum (GAP-1413; ASM-2467). AC7 asserts the catalog answer of the projection that arrived with the model; the kit performs no read against the rule package store.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One evaluator, `RuleEvaluator`, serves every service and the test runner; no service reads the model source, the workbook or a rule table directly | D-RCV-36 T3, T6; Architecture v5 slide 27; DP-04 |
| BR2 | First match: the rule set of a decision table is the package code, each row is one rule whose name is the rule ID, all rows share one activation group, salience comes from row order and the default row is last; exactly one row decides | D-RCV-36 T5; Temporal and Drools design slide 16 |
| BR3 | The package version is chosen at evaluation time from the caller's date and the valid-from and valid-to dates, returned in the result and written to the decision record | D-RCV-36 T7; Temporal and Drools design slides 14 and 15 |
| BR4 | A package version is never edited in place; a correction is a new version and a rollback moves the pointer, both in rwb-decision | D-RCV-36 T4; Temporal and Drools design slide 15 |
| BR5 | A model is usable only when the checksum of what was fetched equals the checksum of the version; the kit keeps the last good model when a new one fails to load and never falls back silently | Architecture v5 slide 27; Temporal and Drools design slide 15 |
| BR6 | The catalog projection — action text, owner role, timer spec and outputs — comes from the fetched model; the kit never reads `rule_row`, because that table is rwb-decision's | D-RCV-36 T6; Ownership Map ruling on `rule_row`; DP-01 |
| BR7 | A KieBase is built once per package version and cached; the cache is bounded by `drools.kiebase.cache.max` through the parameters contract and evicts the least recently used version | D-RCV-36 T3; REQ-DRI-010; DP-06 |
| BR8 | No package in force is a refusal (`NoPackageInForce`), never a default decision, and the activity failure is non-retryable | R-UNI-41; REQ-CWC-008; Temporal and Drools design slide 28 |
| BR9 | The decision record carries the rule ID, that is the Drools rule name, and the rule version, that is the package version label | REQ-CWC-016; DP-03 |
| BR10 | Temporal workflow code never calls the evaluator; a workflow reaches Drools only through an activity, so replays reuse the recorded answer | D-RCV-36 T7; Temporal and Drools design slides 14 and 27 |
| BR11 | No KieBase, KieSession or other Drools type crosses the published interfaces; the kit is the only holder of the runtime | Architecture v5 slide 27; Temporal and Drools design slide 11 |
| BR12 | Evaluation is local to the owning service, inside its own worker, under 300 ms, with no shared rule server on the hot path | Architecture v5 slide 27; Temporal and Drools design slide 15 |

### 9. State transitions

The kit has no business state and changes no case status. What it does have is the state of one cache entry per package version, held in memory in each service process:

| From | Event | Condition | To |
|---|---|---|---|
| ABSENT | A model is requested by version | The fetch succeeds and the checksum matches | CACHED |
| ABSENT | A model is requested by version | The fetch fails, answers a non-success status, or exceeds 2 s | ABSENT, with the last good model of the package still serving |
| ABSENT | A model is requested by version | The checksum of the fetched model differs from the version | REFUSED, with an incident raised |
| CACHED | The same version is requested again | The entry is still inside the bound | CACHED, and the entry becomes the most recently used |
| CACHED | The bound is reached and another version is built | This entry is the least recently used | EVICTED, and the next request for it builds it again |
| CACHED | `RulePackageInForce` names a newer version | The fetch succeeds and the checksum matches | The newer version is CACHED and becomes the version in force from its valid-from date; the older one stays CACHED until it is evicted |
| CACHED | `RulePackageInForce` names a newer version | The fetch fails or the checksum differs | The newer version is REFUSED, the older one stays CACHED and keeps serving |
| REFUSED | The version is corrected in rwb-decision and a new version is published | The new version passes the checksum | The new version is CACHED; the refused label is never reused |
| Any | The process restarts | None | ABSENT, because the cache is memory only and nothing is persisted |

The package version states themselves — LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK and REFUSED as governance states of rwb-decision — are the rwb-decision governance story's, and this story only reads the one in force for a date.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The platform library team (any team, per U3) | Builds, versions and publishes the kit, its interfaces and its fake |
| The service teams of the 19 services | Consume the kit inside their own `EvaluateRules` activity; raise a change request rather than fork the kit |
| The platform owner of the library | Approves a breaking change to the interfaces and freezes a version |
| RW-COE | Owns the rule content of the packages; may not change the kit |
| RW-RISK | Approves rule packages in rwb-decision; has no right in the kit |
| RW-AUDIT | Reads the decision records the callers write, with the rule ID and the package version |
| RW-PLATADM | Receives the checksum, fetch and cache incidents; operates the service metrics |
| SY-RULES | Evaluates packages and serves the catalog inside a service's activity; no endpoint right |
| SY-CASEWF | Calls the evaluator from an activity and writes the result to the decision record |
| No delegation of authority level applies | A rule evaluation is not a credit decision; the DoA table stays with rwb-access |

No personal name, no email address and no credential appears in the kit, its configuration, a log, a metric or a cache entry.

### 11. Data

| Item | Value |
|---|---|
| Tables owned | None. The kit owns no schema and writes no row; `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` are rwb-decision's (section 12.7) |
| Fetched model, in memory | Package code, package version label, checksum, the ordered rows of the version and the catalog projection of each row: action text, owner role, timer spec and outputs (GAP-1413; ASM-2467) |
| Cache entry, in memory | Package code, version label, checksum, built at, last used and the KieBase reference; nothing is persisted and nothing survives a restart |
| Facts | Codes and numbers only, built by the caller from its own data; the kit adds no field and stores no fact |
| Result | Package code, package version, rule ID and outputs; codes and identifiers only |
| Catalog projection | The field set the legacy story names as the catalog: action text, owner role, timer spec and outputs, from the version's rows |
| Personal data | None. No name, no account number, no national identifier and no document content reaches the kit, its cache, its metrics or a log |
| Retention | The cache entry lives as long as the process holds it and is evicted by use; the record of a decision is the caller's, kept in its own schema and collected by rwb-decision |
| Field identifiers | None owned. The projection fields are rwb-decision's own; the caller's record fields belong to the decision-record library |

The migration that creates the store is rwb-decision's; the kit contributes no column and no table, and the only parameter it reads is `drools.kiebase.cache.max` (legacy section 11 and section 13 for the field identifiers of the legacy store).

### 12. Contract

**12.1 REST operations provided**

None. The kit is a library, not a service: it publishes Java interfaces, not an OpenAPI document, and it has no REST base of its own. The package list, the upload, the approval and the rollback endpoints the legacy story declared belong to the rwb-decision governance stories, and the Epic 8 administration screen reaches them through the gateway route of RWB-PLT-N001-CON, which is out of scope here (DP-19).

**12.2 REST operations consumed**

| Operation | Provider | Why the kit calls it | Pattern |
|---|---|---|---|
| GET /api/recovery/decision/v1/rule-models/{n}/{v} | rwb-decision (P7) | Fetches one approved model version — package code, version label, checksum, the ordered rows and the catalog projection — on `RulePackageInForce` and on a cache miss | DP-04, DP-11 |
| GET /api/recovery/case/v1/admin/parameters | rwb-case (P3) | Reads `drools.kiebase.cache.max`, so the cache bound is data and never a code constant | DP-06, DP-11 |

Two consumption rows, both one hop, with a 2 s timeout, a breaker per provider and one retry with jitter on a GET; a failing fetch never blocks an evaluation that already has a good model. The path `GET /rule-models/{n}/{v}` is named on Architecture v5 slides 14 and 27 and on Temporal and Drools design slide 15, and the response field list is the working read of ASM-2467, because no source states the shape of the returned model and the Ownership Map holds no row for the path itself (GAP-1413). The parameter read path is the parameters contract's own; the value 20 is the documented default the kit falls back to and not a decision taken here (ASM-2469).

**12.3 Events published**

None. The kit has no topic of its own: `rwb.decision-record.v1` and `DecisionRecorded` belong to the local decision-record library (RWB-PLT-E1027-CON), and the kit itself publishes nothing.

**12.4 Events consumed**

| Event | Topic | Message schema | Payload carries | Purpose |
|---|---|---|---|---|
| rwb.decision.RulePackageInForce.v1 | rwb.decision.events.v1 | RulePackageInForce | Rule package code, version label, in force at | Fetch the model, verify it, swap it in and refresh the cache entry |

One consumed message schema, through an inbox that dedupes by event identifier, keyed by the package identifier, carrying identifiers and facts only. The event catalogue names rwb-case, rwb-valuation, rwb-treatment and rwb-payment as the listed consumers of `RulePackageInForce` (Architecture v5 slide 43), while DP-04 embeds this kit in every service: the subscription of every service that holds a model is the working read recorded with GAP-1413, and no service reads another service's subscription.

**12.5 Workflows and activities**

None of its own. The kit starts no workflow, owns no task queue, has no `rwb-<short>` queue and registers no activity. It is called inside each service's own `EvaluateRules` activity, on that service's queue, and it is the activity that returns the typed result to the workflow; this is what keeps the workflow code free of Drools and replay-safe (Temporal and Drools design slides 12, 14 and 27).

**12.6 Schedules**

None. The kit owns no Schedule. The promotion of a version at 00:01 is JOB-20, a Schedule in rwb-decision, and the kit only reacts to the event that Schedule publishes (Architecture v5 slide 44).

**12.7 Tables owned**

None. The rule package store — `rule_package`, `rule_package_version`, `rule_row` and `rule_test_case` — stays with rwb-decision (P7) under the Ownership Map ruling, together with the migration that creates it, the seed of the phase-1 package codes and the load checks (Ownership Map, ASM-0069; Architecture v5 slide 41). The kit keeps only an in-memory LRU cache of built KieBases and writes no row anywhere; reading `rule_row` from a service is forbidden by DP-01 and by the schema-per-service rule of Architecture v5 slide 29.

**12.8 Contract fakes**

| Fake | Serves | Used by |
|---|---|---|
| rwb-decision rule-model fake (RWB-P7-E1073-CON) | GET /api/recovery/decision/v1/rule-models/{n}/{v}, with the checksum, the ordered rows and the catalog projection, including a bad-checksum variant and a slow variant | AC1, AC2, AC4, AC5, AC6 and AC7; the fetch-failure path X3 |
| `RulePackageInForce` event fake (rwb-decision) | The event on `rwb.decision.events.v1`, for one version and for two versions in sequence | The refresh, swap and duplicate-delivery tests X3 and X5 |
| rwb-case parameter fake (RWB-P3-E1042-CON) | GET /api/recovery/case/v1/admin/parameters, with `drools.kiebase.cache.max` = 20, a raised value and a missing value | AC5 and the parameter-failure path X6 |
| decision-record fake (RWB-PLT-E1027-CON) | The local record write and `DecisionRecorded` on `rwb.decision-record.v1` | AC1, AC3 and the one-transaction assertion |
| kit fake (RWB-PLT-E1072-CON) | The four interfaces, the refusal and the model shape, answered from the three owner fakes above | The contract test this implementation is verified against |

**12.9 Call-type summary (REST, Kafka, Temporal, File)**

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0: the kit publishes no operation | 2 consumption rows over 2 providers | OpenAPI 3.1 at the owners, one hop, 2 s timeout, breaker per provider, GET retried once with jitter |
| Kafka | 0 published | 1 consumed message schema | CloudEvents 1.0, inbox dedupe by event identifier, keyed by package identifier |
| Temporal | 0 | 0 | The kit starts no workflow and owns no queue; it runs inside the caller's activity |
| File | 0 | 0 | No file crosses the kit; the workbook stays in rwb-decision's governance path |

### 13. Solution plan

**Hardware and software change.** The Drools runtime stops being the runtime of one module and becomes an embedded library in each of the 19 services (Architecture v5 slide 27; Temporal and Drools design slides 11 and 12): every service packages the KIE libraries in its own image and builds its own KieBases in its own process, on its own worker, so there is no shared rules server to fail and no cross-service call on the decision path. Governance does not move with it: authoring, the at-least-50-scenario gate, four-eyes approval, effective dating and one-call rollback stay central in rwb-decision (P7), which owns the store, and the kit only consumes what that governance publishes. On every load the model is fetched over the contract and checksum-verified before it may be used; the KieBase is built once per version and cached LRU up to `drools.kiebase.cache.max`; evaluation happens only inside an activity and stays under 300 ms; and the catalog projection comes with the fetched model, so the kit never reads `rule_row`. The software change is therefore a move of code, not of data: the same Drools version and the same approved KIE libraries as the legacy build, packaged as a library that every service depends on, with the model arriving as a versioned contract payload instead of a row in a local table.

**Deliverables.** The kit library (evaluator, cache registry, model loader, catalog, agenda listener and refusal), the four published interfaces of RWB-PLT-E1072-CON, the `RulePackageInForce` consumer, the parameters and reference-data clients, the decision-record wiring, the operability counters, the kit fake and the architecture test that keeps Drools out of workflow code.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleModelClient | Client | Calls GET /api/recovery/decision/v1/rule-models/{n}/{v} with a 2 s timeout and a breaker; maps a failed fetch to the fetch-failure path |
| KieBaseRegistry | Service | Builds a KieBase from a fetched model once per version, verifies the checksum, caches up to `drools.kiebase.cache.max` and evicts the least recently used |
| RuleEvaluatorImpl | Service | Implements the published evaluator: version-in-force selection by the caller's date, fact insertion, fire, one result; maps no version to the refusal |
| RuleCatalogImpl | Service | Implements the published catalog over the projection of the fetched model |
| DecisionLogAgendaListener | Listener | Captures the Drools rule name of the fired rule and hands it to the evaluator |
| NoPackageInForce | Exception | The checked refusal with messageId MSG-P3-027 and the package code; a non-retryable activity failure |
| RulePackageInForceConsumer | Consumer | Consumes the event through the inbox, fetches and swaps the model, raises an incident on a refusal |
| PlatformMetrics | Instrumentation | Exports `drools_kiebase_builds_total`, the cache hits and evictions, the refusals and the fetch latency |
| Kit fake | Test double | Answers the four interfaces and the model shape from the owner fakes, for the consumers' contract tests |

**Configuration and reference data**

- `drools.kiebase.cache.max` = 20, read through the parameters contract and never coded; 20 is the documented default the kit falls back to when the catalog has no value (ASM-2469).
- The model-fetch timeout is 2 s and the breaker is per provider, as every REST call in the target (Architecture v5 slide 11).
- The KIE runtime dependency lock is the approved set only: drools-engine, drools-mvel, drools-decisiontables and drools-xml-support.
- The package format in phase 1 is the XLS decision table compiled to DRL, which is what the governance story uploads and the model fetch delivers; OMG DMN 1.6 is the later target on the same runtime (Architecture v5 slide 27; Temporal and Drools design slide 15; ASM-2468).

**Pattern application**

| DP code | legacy marker | microservice pattern | dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | this story provides the kit, so no dependency of its own is added by that row; C RWB-P7-E1073-CON for the governance contract |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

All eleven rows are the Template and Rules §R5.5 rows that the legacy story's markers call for. DP-04 is the row this story is itself: the kit is the embedded Drools runtime, so the H row it names is satisfied by this story and only the governance contract stays as a C dependency. DP-19 adds the gateway route only because the Epic 8 rule administration screen reads the models through gateway-bff; that screen is out of scope and no path of it is declared here.

**Build steps**

1. Publish the four interfaces and the model shape of RWB-PLT-E1072-CON in the library, and wire the kit fake from the contract's examples.
2. Build `RuleModelClient` over the rwb-decision fake: the 2 s timeout, the breaker, one retry with jitter on a GET, and the fetch-failure path X3.
3. Build `KieBaseRegistry` with checksum verification, one build per version and the LRU bound read through the parameters client; tests AC5, AC6 and X4.
4. Build `RuleEvaluatorImpl` with version selection by the caller's date and the one-result contract; tests AC1, AC2 and AC3.
5. Add the agenda listener and the activation-group behaviour; test AC4 with two matching rows and 100 repeated evaluations.
6. Build `RuleCatalogImpl` over the projection of the fetched model; test AC7.
7. Add the `RulePackageInForce` consumer with the inbox dedupe and the atomic swap; tests X3 and X5.
8. Wire the decision-record library into the caller path and assert that the record carries the rule ID and the package version, in the caller's transaction; test AC1 and AC3.
9. Add the architecture test that fails the build when a workflow class references the evaluator; test X7.
10. Measure the first and the cached evaluation against the 300 ms target and record the result in the release evidence.

**Done when.** The kit builds and passes AC1 to AC7 against the kit fake and the rwb-decision and rwb-case fakes, the cache stays inside the parameterised bound, a refused model never serves an evaluation, the last good model survives a failed fetch, the decision record carries the rule ID and the package version, and the architecture test keeps Drools out of workflow code.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-027 | No version is in force, or a checksum mismatch refuses a version | The rule version was refused at the {check} check: {detail}. | The refusal `NoPackageInForce`, non-retryable in the activity |
| PLT-RULES-001 | The model fetch fails, answers a non-success status or exceeds 2 s | An incident naming the package code and the version label only; the title and detail text are Not specified in the source documents (GAP-1413; ASM-2467) | Incident, and the last good model keeps serving |
| PLT-RULES-002 | The parameter `drools.kiebase.cache.max` is missing or unreadable | An alert on the parameters catalog; the documented default 20 applies | Alert, with the last known bound kept in memory |
| PLT-RULES-003 | A workflow class calls the evaluator, or a Drools type crosses the interfaces | The architecture test fails the build; the change is rejected before release | Build failure |

For a checksum mismatch, {check} is "checksum" and {detail} names the package code and the version label only, never the DRL, the workbook or a payload (legacy section 14). MSG-P4-002, the refusal of a role that lacks the Rules and parameters right on the package list, belongs to the rwb-decision governance story, because the endpoint moved with the store; the kit itself has no user-facing endpoint and no authorisation check of its own.

### 15. Screens and states

No screen in this story. The kit is invisible to the officer: it answers inside an activity and the screens read the result through the owning service. The legacy package list screen and the Epic 8 rule administration screen are out of scope; they read rwb-decision through the gateway route of RWB-PLT-N001-CON, and the Epic 8 screen is a later epic's story.

What the kit does expose is its operability view, per service and per package: the build counter `drools_kiebase_builds_total`, the cache hits and evictions against the bound, the refusals by package and version, the fetch latency and the age of the model in force. A refused version, a failed fetch and a missing parameter each raise an incident to RW-PLATADM; the model in force stays visible on the owning service's dashboard, so an operator can see which version is answering without reading any rule content.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E1-072-08 | Access | Component | A role without the Rules and parameters right calls the rule package list and is refused with MSG-P4-002; the check now sits with rwb-decision |
| TC-E1-072-01 | AC1, BR1, BR3, BR9 | Component | ALLOCATION version ALLOC-2026.12 from the rwb-decision fake; mortgage, BKK, exposure band 3; the queue code, the rule ID and the version in the result and in the record |
| TC-E1-072-02 | AC2, BR3 | Component | Versions ALLOC-2026.11 and ALLOC-2026.12 with the boundary at 2026-12-15; the caller's date governs, not the system clock |
| TC-E1-072-03 | AC3, BR8 | Component | No ALLOCATION version in force on 2026-12-20; the refusal with MSG-P3-027; no record written and the case not moved |
| TC-E1-072-04 | AC4, BR2 | Component | Rows ALLOC-031 and ALLOC-032 both matching, one activation group; one rule fires, and 100 repeated evaluations fire the same one |
| TC-E1-072-05 | AC5, BR7 | Integration | The same version evaluated twice against the model fake; one build, one cache read, the bound of 20; a 21st version evicts the least recently used |
| TC-E1-072-06 | AC6, BR5 | Integration | A model fake whose checksum differs for ALLOC-2026.13; the version is refused, the incident is raised, and ALLOC-2026.12 keeps serving |
| TC-E1-072-07 | AC7, BR6 | Integration | Row ALLOC-031 with action text, owner role, timer spec and outputs, answered from the fetched projection; no read against the store |

The eight legacy test case IDs are kept with their coverage. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: package codes, rows, salience, conditions and outputs are data published by rwb-decision, and the only value the kit holds is the documented default of the cache bound.
- No personal data in the cache, a log, a metric or a trace: facts are codes and numbers, the result holds codes only, and the catalog projection is action text and role codes.
- No read of another service's tables: the model arrives over a contract, and the kit reads no case table, no ACE view and no rule table (DP-01, DP-05).
- No KieBase, KieSession or Drools type crosses the published interfaces; no caller can reach the runtime except through the evaluator.
- No workflow class calls the evaluator: Drools is reached only inside an activity, and the architecture test fails the build otherwise.
- No cache of a version whose checksum fails, no silent fallback to an earlier version, and no default decision when no version is in force.
- No second evaluator: every service and the test runner calls the same interfaces, and no service reads the model source.
- No edit of a version in place: a correction is a new version in rwb-decision and the kit follows the next `RulePackageInForce`.
- One service, one login, one schema: the kit writes nothing, so it can never widen a grant.
- A failed fetch or a refused model never takes a decision path down: the last good model keeps serving and the incident is raised.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-CWC-016 | Every workflow event logged with its rule ID and version | RWB-E1-072 section 18 (Epic 1, 3.3; Program, 5.3) | TC-E1-072-01, TC-E1-072-02, TC-E1-072-04, TC-E1-072-07 |
| REQ-DRI-001 | One record per decision with the seven field groups | RWB-E1-072 section 18 (Epic 1, 3.7) | TC-E1-072-01, TC-E1-072-02, TC-E1-072-03 |
| REQ-DRI-004 | Epic 1 records use versioned rules | RWB-E1-072 section 18 (Epic 1, 3.3; Program, 5.7) | TC-E1-072-01, TC-E1-072-02, TC-E1-072-03, TC-E1-072-07 |
| REQ-DRI-011 | Versioned tables with valid from and to, author and approver | RWB-E1-072 section 18 (Epic 1, 4; Program, 5.7) | TC-E1-072-01, TC-E1-072-02, TC-E1-072-05, TC-E1-072-06 |
| REQ-DRI-010 | The KieBase is built once per package version and cached, bounded by the cache parameter | RWB-E1-072 section 8 BR7 and section 13 | TC-E1-072-05 |
| REQ-CWC-008 | No package in force is a refusal, never a default decision | RWB-E1-072 section 8 BR9 (R-UNI-41) | TC-E1-072-03 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1072-CON | Contract | H: publishes the four interfaces, the model shape, the refusal, the versioning rule and the kit fake this story implements |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library and the topic the caller writes the rule ID and version through |
| RWB-PLT-E1042-CON | Contract | H: the parameters client that reads the cache bound |
| RWB-PLT-E1043-CON | Contract | H: the reference-data client the rule rows are checked against |
| RWB-PLT-E1047-CON | Contract | H: the naming library for the topic and event names |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway baseline the kit's artefacts are versioned against |
| RWB-PLT-N001-CON | Contract | H: the gateway route the Epic 8 rule administration screen will use; no path is declared here |
| RWB-P7-E1073-CON | Contract | C: the governance contract — upload, load checks, approval, effective dating and rollback — that produces the models this kit consumes |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the owner contracts behind the two consumed reads |
| RWB-P7-E1027-CON | Contract | C: the owner contract of the decision-record entry the central ledger collects |

### 19. Out of scope

- The published interfaces, the model shape, the refusal contract, the versioning and compatibility rule and the kit fake: RWB-PLT-E1072-CON.
- The rule package store, the migration that creates it, the seed of the phase-1 package codes, the upload, the load checks, the at-least-50-scenario gate, four-eyes approval, effective dating and one-call rollback: the rwb-decision governance stories (RWB-P7-E1073-CON and its app story).
- The package list endpoint the legacy story declared, and its read authorities: moved with the store to rwb-decision.
- The decision-record entry and the central ledger: RWB-PLT-E1027-CON and rwb-decision.
- The parameters catalog and its API: RWB-PLT-E1042-CON and rwb-case.
- The reference data and the LOV: RWB-PLT-E1043-CON and rwb-case.
- The naming library and the codec of topic names: RWB-PLT-E1047-CON.
- The per-service Flyway baseline and the schemas: RWB-PLT-E1044-CON and the DB stories.
- The gateway route and the Epic 8 rule administration screen: RWB-PLT-N001-CON and Epic 8 (FEAT-ADM-02).
- The Temporal cluster, the namespace and the worker platform: the workflow platform stories.
- The Epic 2 packages and the rest of the route sets (RESTRUCTURE, PAYMENT_MATCH, BOOKING_MATCH, UNIVERSAL and the other routing rules): their epics.
- Any rule content, any condition, any salience and any output value: owned by RW-COE in rwb-decision, never in this library.
