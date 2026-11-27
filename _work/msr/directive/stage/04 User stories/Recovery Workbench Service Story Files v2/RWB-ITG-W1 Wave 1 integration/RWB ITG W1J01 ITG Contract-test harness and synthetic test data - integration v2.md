# RWB-ITG-W1J01-ITG Contract-test harness and synthetic test data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-W1J01-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | NEW |
| Release | None (new story) |
| Legacy key | W1J01 |
| Legacy disposition | New |
| Build status | Not started |
| Size | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-16); the squad sizes it at refinement |
| Patterns applied | None |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-ITG-W1J01-CON |
| Contract version | /v1 (the path version of each operation in section 12.2) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: new integration harness story for the wave 1 build gate and the wave 1 fixture set. It turns the engineering standards of Architecture v5 slides 11, 20, 29 and 46 into one test project outside the 19 services: OpenAPI 3.1, AsyncAPI 3.0 and activity contract checks in every build, Temporal replay of five recorded histories, Testcontainers Kafka and PostgreSQL, a per-schema boundary test, and a deterministic synthetic set generated from a seed and a business date and loaded only through the owners' published operations into the DEV sandbox. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (13 resolved, 12 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **member of the QA team**, I want **one contract-test harness that checks every published OpenAPI 3.1 document, every AsyncAPI 3.0 document and every activity and workflow contract jar of the wave 1 services in every build, replays the recorded Temporal histories, proves the Kafka and PostgreSQL round trip and the schema boundary on Testcontainers, and generates, loads and resets one synthetic test data set through the owners' published operations in the DEV sandbox**, so that **each wave 1 ITG suite starts on Day 1 from the fixture set it already names as its precondition, and a contract drift, a breaking event change, a non-deterministic workflow change, a cross-schema reference, a mismatched fixture or a production value fails the build in the pipeline instead of the wave release in test**.

This story builds the harness, the fixture set and the gate. It builds no production screen, endpoint, event, workflow, Schedule or table, and it owns no table. The behaviour it checks is owned by the wave 1 services and by the platform stories; the harness only pins their published contracts, drives their published operations, reads their published answers and records what happened.

The harness exists because the standard is explicit. Architecture v5 slide 11 says that every service publishes its contracts before code and that contract tests run in every build. Slide 20 says every service comes from the template with contract tests, outbox relay, inbox, Temporal worker and codec. Slide 46 answers how the 19 services are tested as a set: contract tests per API, event and activity (OpenAPI, AsyncAPI, contract jars), Temporal replay tests, Testcontainers for Kafka and PostgreSQL, and the daily journey smoke. This story builds the first three of those and the fixture set; the journey smoke is the sibling harness story RWB-ITG-W1J02-ITG.

The wave 1 ITG suites already name this harness as a precondition. RWB-ITG-E1018-ITG seeds the ACE batch rows and the synthetic accounts, customers and relations of the RWB-ITG-W1J01-ITG set, and its exception path X8 fails the run as a fixture fault when the set or its ACE batch fixture is missing. The same precondition runs through the other wave 1 suites of the epic: E1018, E1030, E1031, E1032, E1034, E1037, E1039, E1046, E1049, E1050, E1052, E1054, E1057, E1058, E1067 and TE013. This story makes that precondition real and repeatable, once, for all of them.

The harness stories are also what give the QA team its Day 1 work (Template and Rules §R5.7 rule 6). W1J01 is the wave 1 counterpart of W2J01 and, like it, needs no build dependency: the contracts and the fixture classes are enough to start.

### 2. Business rationale

A service can pass its own tests and still break the wave, because what the wave sells is a set of contracts: a screen reads a case through rwb-case, a workflow calls an activity on another owner's queue, and an event leaves one schema and enters another. None of those edges is tested by the service that owns only one end of it. Today the first place a drift shows up is a SIT run, and the cost of finding it there is a re-plan of the wave. The harness moves that discovery into the build, which is the only place where a contract change is still cheap.

The fixture side is the same argument from the other end. Sixteen wave 1 suites need a known data set, and each of them describes the same classes of data: ACE batch rows, accounts, customers and persons, cases, queues with their members and caps, users and roles, templates, documents, feature flags and rule packages. Without one generated set, each suite grows its own seed, the sets disagree, and a failure has to be attributed first to the fixture and only then to the service. One deterministic set, generated from a seed and a business date and loaded only through the owners' published operations, makes a repeated run comparable and a failure attributable.

Three requirements sit directly on this story. NFR-045 forbids production data in development and allows masked copies only in user acceptance, so the development set is synthetic by rule and the harness refuses any other environment. NFR-054 requires the build pipeline to block a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency, so the same gate that runs the contract checks runs the pipeline scan. RWB-E1-065 asks for a sandbox database that holds the ACE schema, the ACE views and synthetic recovery data, so a developer can build and test before the ACE additions and the real data are available; the fixture set is what fills and resets that sandbox.

The harness is also the cheapest place to hold the wave entry check. The alternative is a manual check per suite, which proves the fixture once for one person on one morning and leaves no evidence. The report this harness produces is keyed by build, holds one line per checked element, names the owner, the element and the contract version, and holds the pass or fail the pipeline reads.

### 3. Preconditions

- The wave 1 services P1, P2, P3, P4, P5, P6, P7, P9 and P10 have published their OpenAPI 3.1 documents and their AsyncAPI 3.0 documents with their JSON Schema subjects in the registry, and their activity and workflow interfaces in a contract jar (Architecture v5 slide 11).
- The contract registry, its address and its compatibility rule (BACKWARD) are available to the build, and every document carries a version the report can name.
- The DEV sandbox of RWB-E1-065 exists with the ACE schema, the ACE views and synthetic recovery data, and the 19 Recovery schemas with one login each (Architecture v5 slide 29; ADR-014).
- A Kafka container and a PostgreSQL container are available to the run through Testcontainers, with the owner's outbox and inbox objects created in the service schema under test (Architecture v5 slides 20, 22 and 29; DP-09).
- Recorded histories exist for CaseWorkflow (P3 rwb-case), DailyCaseRun (P3 rwb-case), DocumentIntakeWorkflow (P5 rwb-document), AgentRunWorkflow (P10 rwb-agent) and NoticeDispatchWorkflow (P6 rwb-comms), taken from a run of the same build (Architecture v5 slides 14, 16, 17 and 25).
- The wave 1 ITG suites that consume the set are known by their fixture classes, and their named fixtures are the classes of AC5.
- The seed, the business date and the identifiers of the synthetic set are Not specified in the source documents (GAP-0384; ASM-0558); under ASM-0558 the set is deterministic from a seed and a business date and its volumes and identifiers follow the fixtures the wave 1 ITG stories already name.
- The harness repository, its environment, its namespace and the pipeline stage it runs in are Not specified in the source documents (GAP-0384; ASM-0557).
- The tooling beyond the standards that Architecture v5 names, the fixture lifecycle and reset, the gate thresholds and the report format are Not specified in the source documents (GAP-0384; ASM-0557).
- No build dependency. The harness is Day 1 by rule (Template and Rules §R5.7): it checks the contracts as they are published and builds the fixture set against them, so a missing document is a red check on Day 1 and not a reason to wait.

### 4. Flow

1. Pipeline: starts the harness as a stage of every build, reads the pinned contract versions and the environment from configuration, and refuses to run against any environment other than the DEV sandbox (NFR-045).
2. Harness: reads from the registry the OpenAPI 3.1 document of each wave 1 service and the operation list of the build; a registry operation with no document is a red check and not a skip.
3. ContractRunner: compares every wave 1 operation against its document on path, method, request schema, response schema, status codes and RFC 9457 problem details, and records the contract version it checked (AC1).
4. EventContractProbe: compares every event schema subject against its AsyncAPI 3.0 document and its JSON Schema on the CloudEvents 1.0 binary envelope, the key caseId, IDs and facts only, the absence of a personal data field and BACKWARD compatibility, and records the event and its version (AC2).
5. ContractRunner: compares every published activity and workflow interface in the contract jars against the implementation of its owner, then ReplayRunner replays the recorded histories of CaseWorkflow, DailyCaseRun, DocumentIntakeWorkflow, AgentRunWorkflow and NoticeDispatchWorkflow and compares the decisions each replay reaches with the decisions the history holds (AC3).
6. ContainerRoundTrip: starts a Kafka container and a PostgreSQL container, drives an event from the owner's outbox through the topic into the consumer's inbox, asserts the dedupe of a duplicate delivery, and runs the per-schema boundary test that fails on any cross-schema reference, view or foreign key, including a foreign key into ACE (AC4).
7. FixtureGenerator: builds the synthetic set from the seed and the business date held as configuration, covering the classes of AC5, and asserts that no value comes from a production source (AC5).
8. FixtureGenerator: builds the set a second time from the same seed and business date, compares the two sets key for key and field for field, and fails when they differ (AC5).
9. FixtureLoader: loads every class through the owner's published operation of section 12.2 and never through a schema write, asserts that a repeat load is idempotent, and asserts that the same account, customer, person, case, queue and template keep their identifiers on the repeat (AC6).
10. Harness: runs a preflight of the fixture classes those suites name against the loaded set and asserts that each class they name is present and carries the identifiers the set gave it.
11. FixtureReset: returns the sandbox to its fixture state after the run, names every class it cleared, and fails the run when any row it created remains.
12. ReportWriter: writes one report keyed by build, with one line per checked element naming the owner, the element, the contract version and the result, and publishes the WireMock stub set generated from the pinned contracts (AC7).
13. Pipeline: fails the build when any contract, replay, boundary, fixture or scan check is red, and names the red element in its own summary so the owner sees it without opening the report.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | An operation answers a shape its published OpenAPI document does not allow | The check fails on the operation of the named owner, the report holds the path, the method, the schema difference and both contract versions, and the build fails | None | TC-W1J01-01-ITG | AC1 |
| X2 | A registry operation has no published document, or its document carries no version | The check fails and names the owner and the operation; a missing document is never treated as a pass | None | TC-W1J01-01-ITG | AC1 |
| X3 | An event schema changes in a way the registry does not accept as BACKWARD compatible | The subject is refused, the check fails and names the owner, the event and the version, and the build fails | None | TC-W1J01-02-ITG | AC2 |
| X4 | A workflow change makes a recorded history replay non-deterministically | The replay fails and names the workflow, the history and the event at which the replay diverged from the recorded one | None | TC-W1J01-03-ITG | AC3 |
| X5 | A schema carries a cross-schema reference, view or foreign key, including a foreign key into ACE | The boundary test fails and names the schema, the object and the reference; the build fails | None | TC-W1J01-04-ITG | AC4 |
| X6 | A fixture class of AC5 is missing from the set, or its identifiers do not match the ones the run names | The run fails as a fixture fault, names the class and the identifier, and substitutes no value | None | TC-W1J01-06-ITG | AC5 |
| X7 | The target environment is anything other than the DEV sandbox, or a value in the set looks like production or personal data | The run is refused before a single owner operation is called, and the report names the environment or the class and the value position, never the value | None | TC-W1J01-07-ITG | AC6 |
| X8 | A repeat load is not idempotent, or the reset leaves a row behind | The run fails and names the class, the operation and the count of rows it created twice or left behind | None | TC-W1J01-08-ITG | AC6 |
| X9 | The pipeline scan finds a secret, personal data in code, tests or logs, or an unapproved dependency | The scan fails the same build as the contract checks and names the file and the rule; the build fails (NFR-054) | None | TC-W1J01-09-ITG | AC7 |

The harness produces no business message of its own: every failure above is a report line naming an owner, an element and a contract version. The message catalogue is unchanged by this story, and section 14 states the position.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | A test project of its own outside the 19 services; it needs the published contracts and the DEV sandbox and waits for no app build |
| Negotiable | The seed, the business date, the volumes, the report layout and the gate thresholds are configuration agreed at the wave entry check, not values in code |
| Valuable | One wave 1 contract gate and one fixture set replace sixteen private seeds and move a drift from SIT into the build |
| Estimable | One test project, one fixture project, eleven components, ten test cases and one report |
| Small | Fits one iteration with its tests |
| Testable | Every criterion is asserted on an observable: a registry subject, a replay outcome, a container round trip, a boundary-test result, a generated set compared key for key, an owner answer and a build result |

### 7. Acceptance criteria

```gherkin
Feature: Wave 1 contract-test harness and synthetic test data

  Background:
    Given the wave 1 services P1, P2, P3, P4, P5, P6, P7, P9 and P10 have published their OpenAPI 3.1 documents, their AsyncAPI 3.0 documents with their JSON Schema subjects and their activity and workflow contract jars
    Given the harness runs in the DEV sandbox only (NFR-045)
    Given the seed and the business date of the run are configuration, and their values are Not specified in the source documents (GAP-0384; ASM-0558)

  Scenario: AC1 Every wave 1 operation is checked against its published OpenAPI 3.1 document (new, D-RCV-60)
    Given every wave 1 operation of the build has its OpenAPI 3.1 document and its version pinned in the run
    When the harness runs the OpenAPI contract tests
    Then every operation is checked on its path, its method, its request schema, its response schema, its status codes and its RFC 9457 problem details
    And each checked operation passes with the contract version recorded in the report
    When one operation's answer is changed without its document
    Then the build fails and the report names the owning service, the operation and both contract versions
    And a registry operation with no document fails the build and is never skipped

  Scenario: AC2 Every event is checked against its published AsyncAPI 3.0 document and JSON Schema (new, D-RCV-60)
    Given every wave 1 topic has its AsyncAPI 3.0 document and its JSON Schema subject in the registry
    When the harness runs the event contract tests
    Then every event is checked on the CloudEvents 1.0 binary envelope, the key caseId, IDs and facts only, the absence of a personal data field and the BACKWARD compatibility rule
    And each checked event passes with its version recorded in the report
    When a field is removed from an event schema or its type is narrowed in a way the registry does not accept
    Then the subject is refused, the build fails and the report names the owning service, the event and the version

  Scenario: AC3 Every activity contract matches its implementation and every recorded history replays to the same decisions (new, D-RCV-60)
    Given every wave 1 service publishes its activity and workflow interfaces in a contract jar
    When the harness compares the jars with the implementations and replays the recorded histories
    Then every published activity signature and every workflow interface matches the implementation of its owner
    And the recorded histories of CaseWorkflow, DailyCaseRun, DocumentIntakeWorkflow, AgentRunWorkflow and NoticeDispatchWorkflow replay to the same decisions the histories hold
    When a workflow change makes a replay non-deterministic
    Then the replay fails, the build fails, and the report names the workflow, the history and the event at which the replay diverged

  Scenario: AC4 The Kafka and PostgreSQL round trip and the per-schema boundary hold on Testcontainers (new, D-RCV-60)
    Given a Kafka container and a PostgreSQL container are started for the run with the owner's outbox and inbox in the service schema
    When the round trip test writes an event to the outbox, relays it to the topic and consumes it into the inbox
    Then the event arrives once and the duplicate delivery is deduped by the inbox with no second business effect
    When the per-schema boundary test runs over every wave 1 schema
    Then it passes on a schema that references only its own objects
    And it fails on any cross-schema reference, view or foreign key, including a foreign key into ACE, and names the schema, the object and the reference

  Scenario: AC5 The synthetic set is deterministic and holds no production or personal data (new, D-RCV-60)
    Given the seed and the business date of the run
    When the fixture generator builds the set
    Then it produces the ACE batch rows, the accounts, the customers and the persons, the cases, the queues with their members and caps, the users and roles, the templates, the documents, the feature flags and the rule packages
    And every value is synthetic, and the set holds no production row and no personal data
    When the generator builds the set a second time from the same seed and business date
    Then the two sets are the same key for key and field for field

  Scenario: AC6 The set is loaded and reset through owner operations only, in the DEV sandbox only (new, D-RCV-60)
    Given the set is generated for the DEV sandbox
    When the loader loads every class of the set
    Then each class is loaded through the owner's published operation and no schema write is used
    And a repeat load is idempotent and adds no row
    And the set is reset to its fixture state after the run and the report names every class cleared
    When a load is aimed at any environment other than the DEV sandbox
    Then it is refused before a single owner operation is called (NFR-045)

  Scenario: AC7 The harness gates every build and publishes the stub set (new, D-RCV-60)
    Given the harness runs as a stage of every build
    When a contract, replay, boundary, fixture or scan check is red
    Then the build fails and the report names the owner, the element and the contract version
    When every check is green
    Then the build passes and the report is kept with the build
    And one WireMock stub per wave 1 service is published from its pinned contract, and the stub set carries the contract versions the report names

  Scenario: AC8 Every business rule of section 8 is covered by a criterion and a test case (new, D-RCV-60)
    Given the business rules BR1 to BR12 are listed in section 8 with their sources
    When the harness is reviewed against section 8 and section 16
    Then every rule names at least one criterion and at least one test case
    When a rule in section 8 has no criterion or no test case
    Then the review fails and names the rule

  Scenario: AC9 A retried or timed-out activity replays to the decisions its history holds (new, D-RCV-60)
    Given a recorded history holds an activity that was retried or timed out
    When the harness replays the history
    Then the replay reaches the same decisions the history holds and the report names the activity and the attempt
    When a retry or a timeout would write a decision the history does not hold
    Then the replay fails, the build fails and the report names the workflow, the activity and the event

  Scenario: AC10 A consumed call that fails or does not answer is reported against its owner (new, D-RCV-60)
    Given a wave 1 service calls a wave 1 owner over REST within the 2 s budget of BR11
    When the consumed call returns a failure or does not answer within the 2 s budget
    Then the check fails, the build fails and the report names the caller, the owning service and the operation
    And the failed call is never replaced by a stub answer in a real-owner run
```

The ten criteria are new for this harness. They restate no app criterion of any service: the criteria of the wave 1 services stay with their own stories, and the suites that consume the fixture set keep their own criteria and test cases. The harness is the wave 1 increment of one harness: each later wave extends it by pinning its contracts and generating one stub per service of that wave. As an integration story (work type ITG) it uses the same ready and done items as any other story and is judged by section 3.5 of the test strategy.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every service publishes its contracts before code, and contract tests run in every build | Architecture v5 slide 11; ADR-020 | AC7; TC-W1J01-10-ITG |
| BR2 | A REST operation follows its OpenAPI 3.1 document on path, method, request and response schema, status codes and RFC 9457 problem details, with the version in the path | Architecture v5 slide 11; ADR-020 | AC1; TC-W1J01-01-ITG |
| BR3 | An event follows its AsyncAPI 3.0 document and its JSON Schema subject: CloudEvents 1.0 binary envelope, key caseId, IDs and facts only, no personal data, BACKWARD compatibility | Architecture v5 slides 11 and 22; ADR-015; DP-09 | AC2; TC-W1J01-02-ITG |
| BR4 | Activity and workflow interfaces are published as a contract jar per service, and a caller imports only the interface and calls the owner's task queue | Architecture v5 slide 11 and slide 23; DP-12 | AC3; TC-W1J01-03-ITG |
| BR5 | Workflow code is deterministic and all I/O sits in activities, so a recorded history replays to the same decisions | Architecture v5 slide 23; Temporal and Drools Design slide 11 | AC3; TC-W1J01-03-ITG |
| BR6 | One schema and one login per service, no cross-schema join, view or foreign key, and a boundary test in every build fails on any cross-schema reference | Architecture v5 slide 29; ADR-014; DP-01 | AC4; TC-W1J01-04-ITG |
| BR7 | No production data is used in development; the development environment uses synthetic data and user acceptance uses masked copies | NFR-045 | AC5; AC6; TC-W1J01-07-ITG |
| BR8 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency | NFR-054 | AC7; TC-W1J01-09-ITG |
| BR9 | The sandbox holds the ACE schema, the ACE views and synthetic recovery data, so a developer can build and test before the ACE additions and the real data are available | RWB-E1-065 | AC5; TC-W1J01-06-ITG |
| BR10 | No action proceeds if its decision record cannot be written, and the record, the state change and the outbox row are one transaction, so a history that shows otherwise fails the replay | R-UNI-39; Architecture v5 slide 22 | AC3; TC-W1J01-03-ITG |
| BR11 | Every REST call is one hop to the owner with a 2 s budget, and no service is called through another service | ADR-020; DP-11 | AC10; TC-W1J01-13-ITG |
| BR12 | Contracts are pinned per build, and every stub and every report line names the version it was checked against | ADR-020; ADR-021 | AC7; TC-W1J01-10-ITG |

The harness implements none of these rules. It checks them against the owners and the published contracts, and it holds no business value: the seed, the business date, the volumes and the thresholds are configuration, and the rule packages and the role sets are read from their owners.

### 9. State transitions

The harness changes no case, queue, document, notice, agent-run or decision state of its own. The states it observes are the states of the harness run and of the artefacts it checks.

| Item | States |
|---|---|
| Contract document | Published, pinned for the build, matched, drifted |
| Event schema subject | Registered, compatible, refused for a breaking change |
| Activity and workflow contract jar | Published, matched with the implementation, mismatched |
| Recorded history | Recorded, replayed to the same decisions, diverged at a named event |
| Schema boundary | Pass (own objects only), fail with the offending reference named |
| Fixture set | Not generated, generated, loaded, reset; identical on a repeat generation from the same seed and business date |
| Stub set | Not published, published from the pinned contracts, stale against a new contract version |
| Harness run | Not started, running, passed, failed with the failing element named |
| Build gate | Closed (one red check), open (every check green) |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA lead | Owns the fixture set, the seed and business date as configuration, the report format and the gate definition |
| QA integration engineer | Owns the harness code, the contract probes, the replay runner, the container tests and the stub publisher |
| Integration lead | Owns the swap of a stub for a real owner and the contract pinning per build |
| Service owners of P1, P2, P3, P4, P5, P6, P7, P9 and P10 | Own their published documents, their JSON Schema subjects, their contract jars and the behaviour a red check names |
| ACE database administrator | Owns the sandbox database, the 19 schemas and the 19 logins of the DEV sandbox |
| Platform administrator (RW-PLATADM) | Runs the harness stage, owns the pipeline and the pipeline block of NFR-054 |
| Compliance and PDPA officer (RW-COMPLY) | Owns the rule that the development set is synthetic (NFR-045) and receives a refused-set report |
| Every case role | Reads nothing through this harness; the fixture set creates their roles, it does not act as them |
| No role | Loads a class through a schema write, points the harness at an environment other than the DEV sandbox, or copies a production value into the set |

Authorisation on every owner call is answered by `POST /api/recovery/access/v1/authorise` with the synthetic roles of the set; the harness asserts the allow path and the refusal path for a role without the right.

### 11. Data

| Fixture class | Owner | Written through | Read back by | BR Field ID |
|---|---|---|---|---|
| ACE batch rows for the business date | P1 rwb-source-data | `POST /business-days/{date}/ready` opens the business date for the set | `GET /data-products/freshness`, `GET /data-products/{productCode}/records` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Accounts, customers and persons | P1 rwb-source-data | The P1 data set and the readiness call of the business date | `GET /data-products/{productCode}/records` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Interaction ledger entries | P1 rwb-source-data | `POST /cases/{caseId}/interactions` | The P1 records read and the P1 contract | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Cases | P3 rwb-case | The daily case run the business date starts | `GET /cases`, `GET /cases/{caseId}` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Queues, queue members and caps | P3 rwb-case | `POST /queues/{queueId}/placements` | `GET /queues` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Users and roles | P4 rwb-access | The role set of the set, read through the authorise answer | `POST /authorise` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Documents | P5 rwb-document | `POST /cases/{caseId}/documents` | `GET /cases/{caseId}/documents` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Templates | P6 rwb-comms | `POST /admin/templates` | `GET /admin/templates` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Rule packages | P7 rwb-decision | The package set registered for the business date | `GET /admin/rule-packages/{packageCode}/versions` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Feature flags | The platform library | The flag set of the build | The owner's published flag contract | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Measures | P9 rwb-reporting | None; read only | `GET /reports/measures` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |
| Agent runs | P10 rwb-agent | None; read only | `GET /admin/agent-runs` | Not specified in the source documents (DOR-RWB-ITG-W1J01-ITG-7) |

No field ID is defined by this story. Every class above is an entity its owner already holds in the Logical Data Model and Data Dictionary, and the harness reads and writes it only through the operation named in the row (DP-01). The composition, the volumes and the identifiers of the set are Not specified in the source documents (GAP-0384; GAP-2154; ASM-0558); under ASM-0558 they follow the fixtures the wave 1 ITG stories already name, and every value is synthetic. The seed and the business date of the set are Not specified in the source documents (GAP-2154).

The harness owns no schema and no table. The fixture set lives as generated files under the harness project and, once loaded, as rows the owners wrote in their own schemas through their own operations; the harness never opens a service schema and never inserts a row.

The harness repository, its environment and namespace, its pipeline stage, the tooling beyond the standards that Architecture v5 names, the report format and the gate thresholds are Not specified in the source documents (GAP-0384). The QA lead agrees them with the QA team, the integration lead and DevOps at the wave 1 entry check, and the stub set is pinned per build (AC7).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test project outside the 19 services: it serves no operation, opens no port a service calls and publishes no endpoint.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/business-days/{date}/ready` | P1 rwb-source-data | Opens the business date of the set, in the way the bank's Airflow DAG does (Architecture v5 slide 15) |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The freshness of the data products of the business date (AC5, AC6) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records` | P1 rwb-source-data | The seeded accounts, customers, persons and ledger entries of the set (AC5) |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The synthetic ledger entries of a case (AC5) |
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | The cases of the set for the business date (AC5) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | One seeded case, its state and its links (AC5) |
| GET | `/api/recovery/case/v1/queues` | P3 rwb-case | The queues of the set with their members and caps (AC5) |
| POST | `/api/recovery/case/v1/queues/{queueId}/placements` | P3 rwb-case | The placement of a seeded case in its queue (AC5) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The role, scope and DoA check on every owner call, including the refusal path (AC5, AC7) |
| POST, GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | The synthetic documents of a case and the read-back of the attached document (AC5) |
| GET, POST | `/api/recovery/comms/v1/admin/templates` | P6 rwb-comms | The templates of the set and their versions; the set writes a template through the same element (AC5) |
| GET, POST | `/api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions` | P7 rwb-decision | The rule packages the set registers and puts in force (AC5) |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The published measure contract the probes hold to its document (AC1) |
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | The agent-run contract the probes hold to its document, and the runs of the set (AC1, AC5) |

Fourteen operations are consumed. Where the seeder writes and reads back on the same path, the read-back is the same contract element and is exercised by the same probe, so the row names the call the seeder makes first: the interaction read on `GET /cases/{caseId}/interactions`, the document read on `GET /cases/{caseId}/documents`, the template write on `POST /admin/templates` and the package list on `GET /admin/rule-packages` belong to those same contract elements and are not counted as separate rows.

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with the 2 s client budget and the Idempotency-Key header where the operation requires one (ADR-020; DP-11; DP-13). The harness calls no service through another service.

#### 12.3 Events published

None. The harness publishes no Kafka event. It checks the owners' event contracts against their documents and drives a synthetic event on the Kafka container of the run, and it writes its report as a pipeline artefact.

#### 12.4 Events consumed

None at run time. No consumer of a live topic is started by this story: the round trip of AC4 runs on the Testcontainers Kafka with the owners' published AsyncAPI document and JSON Schema, and the journey that consumes the wave 1 topics end to end is the sibling harness story RWB-ITG-W1J02-ITG.

#### 12.5 Workflows and activities

None added. The harness starts no workflow, adds no activity and owns no task queue. It compares the published activity and workflow interfaces with their implementations and replays these recorded histories:

| Workflow | Owner and task queue | What the harness does |
|---|---|---|
| CaseWorkflow | P3 rwb-case, `rwb-case` | Compares the published interface, then replays a recorded history and compares the decisions (AC3) |
| DailyCaseRun | P3 rwb-case, `rwb-case` | Compares the published interface, then replays the history of the business date (AC3) |
| DocumentIntakeWorkflow | P5 rwb-document, `rwb-document` | Compares the published interface, then replays a recorded intake history (AC3) |
| AgentRunWorkflow | P10 rwb-agent, `rwb-agent` | Compares the published interface, then replays a recorded run history (AC3) |
| NoticeDispatchWorkflow | P6 rwb-comms, `rwb-comms` | Compares the published interface, then replays a recorded dispatch history (AC3) |

Each replay is a replay of a history recorded from the same build; a divergence names the workflow, the history and the event at which it happened (DP-12).

#### 12.6 Schedules

None added. The harness sets, changes and owns no cron, overlap policy or catch-up window. The Schedule trigger that starts DailyCaseRun (Architecture v5 slide 14) is exercised only as a recorded history of section 12.5.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01). Its fixture set is generated as files, the rows it creates are written by the owners through the operations of 12.2, and the report is a pipeline artefact. The harness never reads another owner's tables and never writes a row itself.

#### 12.8 Contract fakes

| Fake | Contract element | Use in the run |
|---|---|---|
| WireMock stub for P1 rwb-source-data | The P1 OpenAPI document: readiness, freshness and records | The fixture probes on a build where P1 is not deployed |
| WireMock stub for P2 rwb-integration | The P2 OpenAPI document, `GET /admin/outbound-items` | Keeps the wave 1 stub set complete for the suites that call P2 |
| WireMock stub for P3 rwb-case | The P3 OpenAPI document: cases and queues | The case and queue probes of AC5 |
| WireMock stub for P4 rwb-access | The P4 OpenAPI document, `POST /authorise` | The authorisation answer and its refusal path |
| WireMock stub for P5 rwb-document | The P5 OpenAPI document: case documents | The document probe of AC5 |
| WireMock stub for P6 rwb-comms | The P6 OpenAPI document: admin templates | The template probe of AC5 |
| WireMock stub for P7 rwb-decision | The P7 OpenAPI document: rule packages and versions | The rule-package probe of AC5 |
| WireMock stub for P9 rwb-reporting | The P9 OpenAPI document: reports and measures | The measure probe of AC1 |
| WireMock stub for P10 rwb-agent | The P10 OpenAPI document: agent runs | The agent-run probe of AC1 and AC5 |

One stub is generated per wave 1 service from that service's published document, and its contract version is pinned in the report and in the published stub set. The stub set is the one the app and ITG stories of the wave consume for a Day-1 build; a contract change makes the stub set stale and the run fails, so a stub pass can never be reported as a real-owner pass. The stub set's location and its publication channel are Not specified in the source documents (GAP-0384; ASM-0557).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided; 14 consumed by the seeder and the contract probes, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (AC1, AC5, AC6) |
| Kafka | None published and none consumed at run time; the round trip of AC4 runs on the Testcontainers Kafka with the owners' published AsyncAPI document and JSON Schema |
| Temporal | None added; five recorded histories replayed and every published activity and workflow contract jar compared with its implementation (AC3) |
| File | The synthetic fixtures of the set, generated by the harness as files and loaded through the owner operations; no service file exchange is read or written |

### 13. Solution plan

**Pattern application**

None. This story applies no decoupling pattern of §R5.5; its metadata Patterns applied row is None. The patterns belong to the services whose contracts it checks, and the harness holds them as assertions rather than as patterns it applies: it fails a build that shows a cross-schema read (DP-01), it drives the outbox and inbox of an owner and never a table (DP-09), it calls one owner per hop on that owner's base with the 2 s budget (DP-11, DP-13), and it checks that each owner's topic keeps the naming of its contract (DP-14).

**Deliverables.** Two projects outside the 19 services: `integration/recovery-w1/contract-tests` for the contract, replay, container, boundary and report checks, and `integration/recovery-w1/synthetic-data` for the generator, the loader and the reset.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ContractRunner | Runner | Runs the OpenAPI checks, the activity and contract-jar checks and the build stage itself, in one order, with one report and one exit code |
| SchemaRegistryProbe | Service | Holds each operation and each event subject to its document and its version, and fails a missing document instead of skipping it |
| EventContractProbe | Service | Checks the CloudEvents 1.0 binary envelope, the key caseId, IDs and facts only, the absence of a personal data field and BACKWARD compatibility |
| ReplayRunner | Service | Replays the five recorded histories and compares the decisions each replay reaches with the recorded ones |
| ContainerRoundTrip | Service | Starts the Kafka and PostgreSQL containers, drives the outbox to topic to inbox round trip and asserts the dedupe of a duplicate |
| BoundaryTest | Assertion | Fails on any cross-schema reference, view or foreign key, including a foreign key into ACE |
| FixtureGenerator | Service | Builds the set of AC5 from the seed and the business date and proves a repeat generation is identical |
| FixtureLoader | Service | Loads every class through the owner operation of 12.2, asserts idempotency and never writes a schema |
| FixtureReset | Service | Returns the sandbox to its fixture state, names every class cleared and fails the run when a row remains |
| StubPublisher | Service | Generates one WireMock stub per wave 1 service from its pinned contract and publishes the stub set |
| ReportWriter | Service | One line per checked element, naming the owner, the element, the contract version and the result, plus the build summary the pipeline reads |

**Environment and test data**

- Environment: the DEV sandbox of RWB-E1-065 only. A run against any other environment is refused before a single owner operation is called (NFR-045). The harness repository, its namespace and the pipeline stage it runs in are Not specified in the source documents (GAP-0384; ASM-0557).
- Data: the synthetic set of AC5, generated from a seed and a business date. The seed, the business date, the volumes and the identifiers are Not specified in the source documents (GAP-0384; ASM-0558); under ASM-0558 they follow the fixtures the wave 1 ITG stories name, and no production row and no personal value enters the set.
- Reset: every run starts from the fixture state and ends with the sandbox returned to it, so a repeated run is comparable element by element.
- Tooling beyond the standards of Architecture v5 is Not specified in the source documents (GAP-0384; ASM-0557): the run uses the standards the architecture names, and any addition is configuration and not a business value.

**Build steps**

1. Create the two projects and the build stage, wire the registry and the sandbox addresses as configuration, and make the stage refuse any environment other than the DEV sandbox (NFR-045).
2. Build SchemaRegistryProbe and ContractRunner for the OpenAPI checks of AC1, with the version pinning and the missing-document failure.
3. Build EventContractProbe for the AsyncAPI and JSON Schema checks of AC2, with the envelope, the key, the personal-data absence and the BACKWARD rule.
4. Build the contract-jar comparison and ReplayRunner for the five histories of AC3, and prove that a forced non-deterministic change fails the replay and names the diverging event.
5. Build ContainerRoundTrip and BoundaryTest for AC4, with the duplicate delivery, the dedupe and the cross-schema reference.
6. Build FixtureGenerator for the eleven classes of AC5 and prove that a repeat generation from the same seed and business date is identical.
7. Build FixtureLoader and FixtureReset for AC6, prove the idempotent repeat load, the owner-operation-only rule and the complete reset, and prove the refusal of any other environment.
8. Build ReportWriter and StubPublisher for AC7, publish one stub per wave 1 service from its pinned contract, and prove that one red check fails the build and names the owner, the element and the contract version.

**Pipeline block.** The gate runs the checks of sections 4 and 12 and the pipeline scan of NFR-054 in the same build. The scan blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency, and it reports on the same summary the contract checks do. The thresholds beyond all-green and the report format are Not specified in the source documents (GAP-0384; ASM-0557).

**Done when.** The ten test cases of section 16 pass; every wave 1 operation and every wave 1 event is checked against its published document with its contract version in the report; the five recorded histories replay to the same decisions; the container round trip and the boundary test pass; the synthetic set of the eleven classes is generated twice identically, loaded through owner operations only, reset after the run and refused in any environment other than the DEV sandbox; and one WireMock stub per wave 1 service is published from its pinned contract.

### 14. Validation and messages

None. This story defines no business message and no message ID, and the harness produces none. A harness failure is a report line, not a message: it names the owner, the element and the contract version, it is read in the pipeline and in the report, and it is never shown to a case officer, an approver or a customer. The message catalogue, the message IDs and their Thai text are unchanged by this story.

### 15. Screens and states

No screen in this story. The harness renders nothing and opens no page. The report is a pipeline artefact read by the QA lead, the integration lead and the owner of the element that failed, and the stub set it publishes is consumed by the app and ITG stories of the wave and not by a screen. The states the harness observes are the run, artefact and fixture states of section 9.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-W1J01-01-ITG | AC1, X1, X2 | Contract | Every wave 1 operation against its OpenAPI 3.1 document; one operation changed without its document |
| TC-W1J01-02-ITG | AC2, X3 | Contract | Every wave 1 event against its AsyncAPI 3.0 document and JSON Schema; one subject with a field removed |
| TC-W1J01-03-ITG | AC3, X4 | Component | The five recorded histories; one workflow changed non-deterministically |
| TC-W1J01-04-ITG | AC4, X5 | Component | Kafka and PostgreSQL containers, one outbox to topic to inbox round trip, one duplicate delivery, one cross-schema reference and one foreign key into ACE |
| TC-W1J01-05-ITG | AC5 | Component | The eleven fixture classes generated twice from the same seed and business date |
| TC-W1J01-06-ITG | AC5, X6 | Integration | One fixture class missing and one identifier that does not match the run |
| TC-W1J01-07-ITG | AC6, X7 | Integration | A load aimed at an environment other than the DEV sandbox, and a value that looks like production or personal data |
| TC-W1J01-08-ITG | AC6, X8 | Integration | A repeat load of the whole set, then the reset of every class |
| TC-W1J01-09-ITG | AC7, X9 | Integration | A red contract check and the pipeline scan of NFR-054 on the same build |
| TC-W1J01-10-ITG | AC7 | Component | The stub set published from the pinned contracts, compared version by version with the report |
| TC-W1J01-11-ITG | AC8 | Component | Every rule BR1 to BR12 traced to its criterion and test case; one rule with no criterion |
| TC-W1J01-12-ITG | AC9 | Component | One recorded history with a retried activity and one with a timed-out activity; one retry that would write a decision the history does not hold |
| TC-W1J01-13-ITG | AC10 | Integration | One consumed call that returns a failure and one that does not answer within the 2 s budget |

The full test, with its Given, When and Then, is held under the same test case ID in the wave 1 harness pack; its pack contents are Not specified in the source documents (GAP-0384; ASM-0557). The evidence is kept with the build it proves and past the gate that reads it, keyed by build for the harness; no retention period is asserted until the QA lead sets one. The wave gate is signed by the QA lead, with the integration lead on the report of the harness.

### 17. Guardrails

- No production data and no personal data: the set is synthetic, the harness refuses any environment other than the DEV sandbox (NFR-045), and its report and logs hold identifiers, class names, contract versions and check names only.
- No business value in code: the seed, the business date, the volumes and the thresholds are configuration; the rule packages, the roles, the queues, the caps, the templates and the flags belong to their owners and are read or seeded through their operations (DP-01).
- No cross-schema read: the boundary test fails on any cross-schema reference, view or foreign key, including a foreign key into ACE, and the harness ships with no client for a service schema (DP-01, ADR-014).
- Contracts are pinned per build, and every stub, every replay and every report line names the version it was checked against, so a stale stub set can never pass as a green build (ADR-020, ADR-021).
- The pipeline blocks a secret, personal data in code, tests or logs, or an unapproved dependency in the same build as the contract checks (NFR-054).
- The harness runs in the DEV sandbox only and never points at user acceptance, at production or at an outside system.
- The fixture set is deterministic: the same seed and business date produce the same set key for key, so a repeated run is comparable and a difference is a real difference.
- The reset is part of the run: a class left behind after the run fails it, so the next suite never starts on a mixed estate.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| NFR-045 | No production data in development, and masked copies only in user acceptance | The environment guard, the synthetic generator, the reset, the refused-set report | TC-W1J01-05-ITG, TC-W1J01-07-ITG, TC-W1J01-08-ITG |
| NFR-054 | The pipeline blocks a secret, personal data in code, tests or logs, or an unapproved dependency | The build stage, the pipeline scan, the build summary | TC-W1J01-09-ITG |
| RWB-E1-065 | A sandbox database with the ACE schema, the ACE views and synthetic recovery data | The DEV sandbox, the generated set of the eleven classes, the loader and the reset | TC-W1J01-05-ITG, TC-W1J01-06-ITG, TC-W1J01-08-ITG |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The OpenAPI checks, the 14 consumed operations, the stub set | TC-W1J01-01-ITG, TC-W1J01-10-ITG |
| ADR-021 | Per-service Flyway and migration ownership | The harness owns no schema and no migration and checks the boundary instead | TC-W1J01-04-ITG |
| DP-01 | The owner's schema, never another service's tables | The boundary test, the loader that uses owner operations only, the report | TC-W1J01-04-ITG, TC-W1J01-08-ITG |
| DP-09 | Outbox and inbox library, CloudEvents, the owner's topic | The event contract checks and the container round trip with its dedupe | TC-W1J01-02-ITG, TC-W1J01-04-ITG |
| DP-11 | REST contract with a mock, one hop, 2 s timeout | The consumed operations and the stub set generated from each contract | TC-W1J01-01-ITG, TC-W1J01-10-ITG |
| DP-13 | `/api/recovery/<short>/v1` | Every consumed operation on the owner's base | TC-W1J01-01-ITG |
| DP-14 | The owner's topic naming `rwb.<short>.events.v1` | The AsyncAPI check of each topic and its event | TC-W1J01-02-ITG |

### 19. Out of scope

- The performance harness of TE009, its load profile and its non-functional thresholds; the non-functional epic RWB-ITG-NFR.
- The Temporal platform of TE010 and E1070: the cluster, the namespace, the codec, the worker versioning and the replay service itself. This story replays histories through the platform; it builds none of it.
- The journey harness RWB-ITG-W1J02-ITG, which consumes the wave 1 topics and the set end to end. This story builds the set and the contract gate it runs on, not the journey.
- The service app stories of the wave and their own criteria, screens and test cases; the criteria of E1018, E1030, E1031, E1032, E1034, E1037, E1039, E1046, E1049, E1050, E1052, E1054, E1057, E1058, E1067 and TE013 stay with their own stories.
- The platform edge story RWB-PLT-N001-CON and the gateway-bff composite route.
- The masked copies of SIT and UAT (RWB-ITG-TE004-ITG) and the PII service that produces them; this story is the synthetic development side of NFR-045 only.
- Production data, a production namespace and any copy from production, in any form.
- The harness repository, its namespace, its pipeline stage, the tooling beyond the standards, the fixture volumes and identifiers, the reset mechanism beyond its outcome, and the gate thresholds and report format: carried as one gap and two assumptions, not decided here.
