# RWB-PLT-NF01-OPS Repository and pipeline baseline

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-NF01-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | NF |
| Release | None (new story) |
| Legacy key | NF-01 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | None |
| Parallel lane | L-PLT-TPL-B |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-PLT-NF01-OPS-16); the squad sizes it at refinement |
| Depends on (build) | None |
| Contract dependencies | None. This story publishes no contract and has no contract story or CON dependency; it builds against no contract version, and its only version marker is the /v1 path of BR4 |
| Integration dependencies | None |
| External dependencies | None |
| Assumptions | ASM-B-PLT-TPL-01-NF01-1 to ASM-B-PLT-TPL-01-NF01-5 (repository layout, branch policy, toolchain and template version scheme are treated as values of the template until the wave 0 entry check confirms them) |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: platform story for legacy NF-01 (moved, no impact), repository and pipeline baseline — one repository per service created from the platform template with the standard layout, one pinned template version and one shared set of pipeline gates, with the legacy NF-01 story text absent from the source set, so the baseline is derived from Arch v5 slides 4, 20, 29, 33, 38 and 41 and NFR-045, NFR-052 and NFR-054. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-NF01-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (10 resolved, 6 cross-document, 1 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **one repository per service created from the platform template, with the standard layout, the same eight pipeline gates for every service and every repository pinning the same template version**, so that **each of the 19 services starts on Day 1 with its own code, release and owner and the same quality bar, and no repository can carry another service's schema or data, a secret, or production data**.

### 2. Business rationale

The target is 19 deployable services, and Arch v5 states the rule that makes them worth splitting: "one deployable service per BA module, so that each capability has its own code, release, owner, contract, schema, topic and task queue" (slide 4). Slide 33 fixes the shape every one of the 19 shares — an API deployment with 2 fixed copies and a worker deployment scaled by KEDA on its own task queue, over its own schema in the ACE database — and slide 41 gives the same naming for all 19: schema `rwb_<name>`, REST under `/api/recovery/<name>/v1`, topic `rwb.<name>.events.v1`, task queue `rwb-<name>` in the namespace `rwb-recovery`. Slide 20 says every service is "built from one template (Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, contract tests)" and exposes `/health` and `/metrics` for the platform. Slide 38 makes that template and the golden pipeline wave-0 enablers, built once before the first service exists.

A repository is where that rule either holds or leaks. If each service team starts from an empty folder, the 19 services become 19 shapes: 19 directory layouts, 19 build scripts, 19 CI files and 19 opinions about what a merge must pass. The first service then passes a contract test that the next one never runs, a migration lints in one repository and not in another, and the boundary that slide 29 enforces by grant — one login per service, no grant on any other schema — is only checked in production, after the code is written. One template with one pinned version and one shared gate set makes the shape and the gates a fact of the repository rather than a convention of the team, and it makes the boundary checkable at build time: a cross-schema reference fails before it is deployed.

The NFRs then decide what a repository may never contain. NFR-052 keeps every secret in the key store and never in code, configuration files or prompts. NFR-054 requires the build pipeline to block a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency. NFR-045 forbids production data in development and requires masked copies in user acceptance, which applies to test fixtures and seed files as much as to a database. Together they mean that a repository, its history, its logs and its test data are scanned artefacts, and that the scan belongs to the pipeline that every service inherits and not to a script that each team remembers to run.

One service, one repository is also the line the return document already carries: "the Workbench is a module of ACE: one service, one repository, one front end" (Business Requirements Program v5 §7, constraint "Built on ACE"). Applied to 19 services from Arch v5, that line yields 19 repositories, each holding one service. It is not a conflict: the count of services changed and the rule did not.

**The legacy NF-01 story text is not in the source set.** The legacy index entry for NF-01 holds the title "Repository and pipeline baseline", the group NF and empty metadata, requirements, acceptance criteria, test cases, messages and sections; there is no story file behind it. Nothing is therefore copied from a legacy story, and no legacy acceptance criterion or test case exists to preserve. The baseline above is derived from Arch v5 slides 4, 20, 29, 33, 38 and 41 and from NFR-045, NFR-052 and NFR-054, which is the order of precedence of Template and Rules §R3 for a legacy key with no story text. The exact repository layout beyond the six named folders, the branch policy and the toolchain are not in any source in the set; they are recorded as one gap (GAP-1425) and its assumptions, and every value of that kind reads Not specified in the source documents (GAP-1425; ASM-2494).

This is a Wave 0 Day-1 enabler with no build dependency. It owns the repository and the gate set. It deliberately does not own what those gates install: the Helm chart and the pipeline template are RWB-PLT-N004-OPS, the versioned migration sequence is RWB-PLT-E1044-OPS, the four environments are RWB-PLT-NF03-OPS and the secret and configuration baseline is RWB-PLT-NF04-OPS. This story fixes the repository those four stories deliver into, and the gates that run on every change to it.

### 3. Preconditions

- Wave 0 exists as a programme phase: the platform epic RWB-PLT-TPL owns this story and no service is in build, so the layout and the gate set can be fixed before the first service repository is created (Arch v5 slide 38).
- The service template exists in its first version with the application skeleton of Arch v5 slide 20 — Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, `/health` and `/metrics` — because a repository is created from it and its version is what a repository pins.
- The one pipeline template and the one Helm chart of RWB-PLT-N004-OPS exist, because the gates of this story are stages of that pipeline and the `helm` folder of the layout receives that chart; this story references them and repeats none of them.
- The versioned migration mechanism of RWB-PLT-E1044-OPS exists, because the `db/migration` folder of the layout is the per-service Flyway sequence of that story (DP-15) and its lint gate is the one that checks it.
- The secret and configuration baseline of RWB-PLT-NF04-OPS exists in its first version, because the secret and personal-data scan of a repository needs the key-reference form a configuration file must take (NFR-052).
- The source-control organisation, the CI runner, the artefact registry and the image registry of the bank are available to the programme; their names and their configuration are Not specified in the source documents (GAP-1425; ASM-2497).
- The 19-service list and the short names of Template and Rules §R4 are fixed, so that the repository inventory has 19 stable rows and a repository name can be derived from a service short name.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The exact layout inside each folder, the branch policy, the toolchain and the way the template version is raised are Not specified in the source documents (GAP-1425; ASM-2494).

### 4. Flow

1. Publish the template at a version: the application skeleton, the standard layout and the pipeline definition of this story, tagged with one template version that every consumer repository can pin.
2. Create one repository per service from the template, named for the service short name of Template and Rules §R4 so that `rwb-case`, `rwb-payment` and the other 17 are recognisable from their names, and record all 19 in one repository inventory.
3. Lay the repository out in the standard shape: `api/` and `worker/` for the two deployments of slide 33, `db/migration/` for the per-service migration sequence, `contracts/` for the OpenAPI and AsyncAPI documents the service owns, `helm/` for the chart values of RWB-PLT-N004-OPS, and `pipeline/` for the gate definitions this service runs.
4. Record the template version at the repository root in one version file, read by the pipeline on every run; a repository with no version, or with a version the template no longer publishes, fails the first stage.
5. Wire the one pipeline definition: build, unit, contract, boundary, migration lint, image scan, secret scan and personal-data scan run in the same order with the same thresholds for every service, and the definition is referenced from the template rather than copied into each repository, so that a gate is added or changed once.
6. Add the boundary test: it reads the service's own short name and schema from the configuration, refuses a SQL statement, a datasource, a grant or a join that names another service's schema, refuses a reference to another service's table, and refuses a migration file or a fixture that carries another service's objects or rows.
7. Add the content scans: a secret scan over the working tree, the full history, the build logs and the test data, an image scan of every built image, and a personal-data scan of code, tests and log fixtures, with a finding that names the file and the rule and never prints the value.
8. Fix the branch policy and the release identity: a protected default branch that only the pipeline writes to, short-lived change branches, one immutable image digest per build and one release tag per service release, so that a build is promoted by digest and not by branch name.
9. Prove the baseline on a pilot repository: create it from the template, run all eight gates green once, then break each gate in turn and confirm that each one fails the build and names its finding; record the run as the evidence, publish the template version and hand the layout to the service teams.
10. Add the upgrade path: a template change raises the template version, the inventory reports every repository that pins an older version, and a service upgrades by taking the new version in its own change and running the same eight gates, so that no repository is changed under a service team's feet.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A repository is created without a template version, or with a version the template no longer publishes | The first pipeline stage fails, names the repository and the version file, and no build artefact is produced | None | AC1 |
| X2 | A service repository is missing a folder of the standard layout, or adds a second place for the same artefact | The layout check fails and names the missing folder and the repository, so the service cannot diverge silently | None | AC1 |
| X3 | One gate is disabled, reordered or given a different threshold in one repository | The pipeline check compares the repository's gate set with the template's and fails the build, naming the gate and the difference | None | AC2 |
| X4 | A change makes a gate fail — a failing unit test, a broken contract, a lint error, a vulnerable image layer, an unapproved dependency | The pipeline stops at that gate, the later gates do not run, and the finding names the artefact and the rule | None | AC2 |
| X5 | A statement, a datasource, a grant, a join or a fixture names another service's schema or table | The boundary test fails the build and names the statement, the foreign schema and the owning service; the change never reaches an environment | None | AC3 |
| X6 | A secret, a token or a key is committed, or is present in the history | The secret scan fails the build, names the file and the commit and never prints the value, and the credential is rotated through the key store | None | AC4 |
| X7 | Production data, a production extract or a personal-data field reaches a test, a fixture or a log | The personal-data scan fails the build and names the file and the rule; the data is removed and the case goes through the ACE Common PII path | None | AC4 |
| X8 | A template change lands while 19 repositories are in service | The new version is published, the inventory lists the repositories still on the old version, and each service upgrades in its own change; nothing is pushed into a repository outside its own pipeline | None | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 19-service list of §R4, the template, the chart of RWB-PLT-N004-OPS, the migration mechanism of RWB-PLT-E1044-OPS and the key-reference form of RWB-PLT-NF04-OPS only |
| Negotiable | The names of the repositories, the branch names, the toolchain and the way the template version is raised are agreed with the platform administrator and the solution architect; the one-repository-per-service rule, the six folders, the eight gates and the version pin are fixed |
| Valuable | Gives all 19 services one shape and one quality bar from Day 1, and turns the schema boundary of Arch v5 slide 29 into a build-time failure instead of a production incident |
| Estimable | One template release, one repository inventory, one layout, one pipeline definition with eight gates and three scans, one boundary rule set and one pilot repository that proves each gate fails when broken |
| Small | Fits one sprint with the layout, the gate wiring, the boundary rule set and the pilot; the chart, the migrations, the environments and the key store belong to the other Wave 0 stories |
| Testable | Every criterion is tested against the pilot repository and the inventory, with a green run and one deliberately broken change per gate |

### 7. Acceptance criteria

```gherkin
Feature: Repository and pipeline baseline for the 19 services

  Background:
    Given the platform template at a published version
    Given the 19-service list and the short names of Template and Rules §R4
    Given the chart of RWB-PLT-N004-OPS, the migration mechanism of RWB-PLT-E1044-OPS and the key references of RWB-PLT-NF04-OPS

  Scenario: AC1 A new service repository is created from the template with the standard layout and the template version recorded (new, D-RCV-60)
    Given the platform template and its published version
    When a repository is created for a service of the 19-service list
    Then it is created from the template and not from an empty folder
    And it holds the six folders api, worker, db/migration, contracts, helm and pipeline
    And the template version it was created from is recorded in one version file at the repository root
    When the layout check runs on that repository
    Then every folder is present and the version file names a version the template publishes
    And a repository with a missing folder or no recorded version fails the check and is named

  Scenario: AC2 The pipeline baseline runs the same gates for every service and fails on each (new, D-RCV-60)
    Given the 19 service repositories and the one pipeline definition of the template
    When a change is pushed to any of them
    Then the same gates run in the same order: build, unit, contract, boundary, migration lint, image scan, secret scan and personal-data scan
    And every gate reads its thresholds from the template and not from the repository
    When a change makes one gate fail
    Then the build stops at that gate, the later gates do not run, and the finding names the artefact and the rule
    And a repository that disables, reorders or re-thresholds a gate fails the pipeline check and is named

  Scenario: AC3 The boundary test fails a cross-schema reference and no repository holds another service's schema or data (new, D-RCV-60)
    Given a service repository and the schema of that service from the 19-service list
    When a statement, a datasource, a grant or a join names another service's schema
    Then the boundary test fails the build and names the statement, the foreign schema and the owning service
    When a migration file, a fixture or a seed file carries another service's objects or rows
    Then the same test fails the build and names the file
    And no repository holds another service's schema definition, migration or data

  Scenario: AC4 No secret and no production data in the repository, history, logs or tests (new, D-RCV-60)
    Given a service repository and its full history
    When the secret scan and the personal-data scan run
    Then no secret, token, key, connection string or password is found in the tree, the history, the build logs or the test data
    And every credential is a reference resolved from the key store at deploy time
    And no production record, no production extract and no personal-data field is found in a test, a fixture or a log
    When a secret or a production record is introduced
    Then the build fails, the finding names the file and the rule and never prints the value, and the credential is rotated

  Scenario: AC5 Every service pins the same template version and a template change raises a version (new, D-RCV-60)
    Given the 19 service repositories and the template at version V
    When the inventory check runs
    Then every repository records the same template version V
    And a repository that records no version or another version is reported with its name and its version
    When the template changes in a way that affects a repository
    Then the template version is raised and published before any service takes it
    And each service takes the new version in its own change and runs the same eight gates
    And no repository is changed by a template change directly

  Scenario: AC6 Each business rule BR1 to BR9 of section 8 holds for every service repository (new, D-RCV-60)
    Given the 19 service repositories, the platform template and the rules BR1 to BR9 of section 8
    When the baseline check runs on every repository
    Then each repository is one deployable service with its own code, release, owner, contract, schema, topic and task queue (BR1)
    And each repository is built from the one template with Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, contract tests, /health and /metrics (BR2)
    And each service has an API deployment with 2 fixed copies and a worker deployment scaled by KEDA on its own task queue (BR3)
    And each service uses schema rwb_<name>, REST under /api/recovery/<name>/v1, topic rwb.<name>.events.v1 and task queue rwb-<name> in the namespace rwb-recovery (BR4)
    And the same eight gates run in the same order with the same thresholds, taken from the template (BR5)
    And no statement, datasource, grant, join, migration or fixture names another service's schema, table or data (BR6)
    And a change carrying a secret, personal data in code, tests or logs, or an unapproved dependency is blocked by the build (BR7)
    And no production data is held in a repository, a test or a log (BR8)
    And every service pins the same template version and a template change raises that version (BR9)
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One deployable service per module and one repository per service, so that each of the 19 has its own code, release, owner, contract, schema, topic and task queue | Arch v5 slide 4; Business Requirements Program v5 §7 constraint "Built on ACE" |
| BR2 | Every service is built from the one template: Spring Boot, outbox relay, inbox, Temporal worker, codec, OpenTelemetry, contract tests, `/health` and `/metrics` | Arch v5 slides 20 and 38 |
| BR3 | Every service has the same shape: an API deployment with 2 fixed copies and a worker deployment scaled by KEDA on its own task queue | Arch v5 slide 33 |
| BR4 | Every service follows the same naming: schema `rwb_<name>`, REST under `/api/recovery/<name>/v1`, topic `rwb.<name>.events.v1`, task queue `rwb-<name>` in the namespace `rwb-recovery` | Arch v5 slide 41; Template and Rules §R4 |
| BR5 | The same eight gates run for every service in the same order with the same thresholds, and the gate set is the template's and not the repository's | NFR-054; this story |
| BR6 | The boundary is checked at build time: no statement, datasource, grant, join, migration or fixture may name another service's schema, table or data | Arch v5 slide 29; Template and Rules §R5.5 DP-01 |
| BR7 | The build blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency; a credential is a key reference and never a value | NFR-052; NFR-054 |
| BR8 | No production data in a repository, a test or a log: development and test data are synthetic, and a masked copy is loaded into user acceptance only through the loading story and never committed | NFR-045 |
| BR9 | Every service pins the same template version; a template change raises the version and each service upgrades in its own change | Arch v5 slide 38; this story |

### 9. State transitions

| Repository state | Meaning | What moves it on |
|---|---|---|
| Created | The repository exists from the template with the standard layout and the version file | The layout check passes |
| Gated | The pipeline and all eight gates are wired and have run green once | The pilot run of record is attached |
| Pinned | The repository records a template version that the template publishes | The inventory check reports the version as current |
| In service | Builds are produced from it and promoted by image digest | The service's own release |
| Upgrade pending | A newer template version is published and the repository still pins the older one | The service takes the new version in its own change |
| Archived | The repository accepts no change and its pipeline is disabled | The platform administrator archives it at the end of the programme |

No case status changes in this story: these are states of a repository, not of a case, a treatment or a decision.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the template release, the repository inventory, the layout, the pipeline definition and the eight gates; changes any of them through the template repository and the pipeline only |
| Platform administrator | Approves the template version, the repository names, the branch policy, the registry configuration and the gate set; owns the protected branch setting of every repository |
| Solution architect | Approves the standard layout, the boundary rule set, the template versioning scheme and the scope of the scans |
| Tech lead of a service | Takes a template version into the service repository in the service's own change, and may not disable, reorder or re-threshold a gate |
| Security architect | Approves the secret scan, the personal-data scan, the image scan and the unapproved-dependency check, and the rule set each one applies |
| RW-PLATADM | Reads the repository inventory, the gate results and the version report, and may archive a repository; never edits a repository by hand |
| RW-AUDIT | Reads the inventory, the pilot evidence and the scan findings; writes nothing |
| RW-SECADM | Reads the secret, personal-data and image scan findings and the credential rotation record; writes nothing in the template |

The platform stories carry no service short name, schema, topic, event or task queue in the §R4 service table, because that table has 19 service rows and no platform row. Where a value of this baseline itself would need a name — the repository name of a service, the branch names, the version scheme, the toolchain — it is Not specified in the source documents (GAP-1425; ASM-2494).

### 11. Data

**What each repository holds**

| Element | Where it sits in the layout | What it is | Source | BR Field ID |
|---|---|---|---|---|
| API deployment sources | `api/` | The REST surface of the service under `/api/recovery/<name>/v1`, 2 fixed copies | Arch v5 slides 20, 33 and 41 | BR3; BR4 |
| Worker sources | `worker/` | The Temporal worker on task queue `rwb-<name>` and the Kafka consumers, scaled by KEDA | Arch v5 slides 20 and 33 | BR3 |
| Migration sequence | `db/migration/` | The per-service Flyway sequence in the service's own schema, owned by RWB-PLT-E1044-OPS | Template and Rules §R5.5 DP-15 | BR6 |
| Contracts | `contracts/` | The OpenAPI 3.1 and AsyncAPI documents the service owns, and the contract-test stubs built from them | Arch v5 slides 20 and 28 | BR2 |
| Chart values | `helm/` | The values file of the service for the one chart of RWB-PLT-N004-OPS | Arch v5 slide 38 | BR3 |
| Gate definitions | `pipeline/` | The one pipeline definition reference, the boundary rule set and the scan configuration | This story | BR5 |
| Template version | `template.version` at the root | One version, read by the pipeline on every run and reported by the inventory | This story; AC1 and AC5 | BR9 |

**What no repository holds**

| Item | Why it is excluded | Where it lives instead | BR Field ID |
|---|---|---|---|
| A secret, a token, a key, a password or a connection string | NFR-052: secrets are held in the key store and never in code, configuration files or prompts | The key store, through a key reference resolved at deploy time (RWB-PLT-NF04-OPS) | BR7 |
| Production data, a production extract or a production record | NFR-045: no production data in the development environment, masked copies in user acceptance | DEV holds synthetic data, SIT and UAT hold masked copies loaded by the loading story | BR8 |
| A personal-data field in code, a test, a fixture or a log | NFR-054: the pipeline blocks personal data in code, tests or logs | The owning service's schema, masked, with the PII path through ACE Common | BR7 |
| Another service's schema definition, migration, table or rows | Arch v5 slide 29: one login per service, no grant on another schema, no cross-schema join | The owning service's own repository | BR6 |
| A business rule value, a limit, a threshold or a reference-data row | Principle 1: these are versioned data rows, changed without a code release | The parameter and reference-data contracts of RWB-P3-E1042-CON and RWB-P3-E1043-CON | Not specified in the source documents (DOR-RWB-PLT-NF01-OPS-7) |

The baseline holds the template, the layout, the gate definitions, the boundary rule set, the scan configuration and the version file of a repository. It holds no business value, no personal data and no credential. The exact contents of each folder beyond the element above, the branch names, the toolchain and the version scheme are Not specified in the source documents (GAP-1425; ASM-2495).

### 12. Contract

This story provides no REST operation, publishes and consumes no business event, runs no workflow and no Schedule, and owns no table and no schema. It is a repository and pipeline baseline only.

#### 12.1 REST operations provided

None. The baseline exposes no REST surface of its own; a repository is read through the source-control system and the pipeline, not through an API.

#### 12.2 REST operations consumed

None. The baseline calls no service contract; the gates of the pipeline read the repository and the registries, not a Workbench API.

#### 12.3 Events published

None. The baseline publishes no business event and no platform event; a gate result is a pipeline record and not a Kafka message.

#### 12.4 Events consumed

None. The baseline subscribes to no topic; a change to a repository starts a pipeline run and not a consumer.

#### 12.5 Workflows and activities

None. The baseline starts no workflow and defines no activity; the `worker` folder it creates is the skeleton of the service's own worker, whose workflows belong to the service stories.

#### 12.6 Schedules

None. No Temporal Schedule is created, moved or paused by this story; the pipeline runs on a change and is not a Schedule.

#### 12.7 Tables owned

None. The baseline owns no table and no schema; the 19 schemas `rwb_<name>` belong to the ACE database work and the service stories, and the migration folder it lays out is filled by RWB-PLT-E1044-OPS.

#### 12.8 Contract fakes

None. The baseline runs against the template, the real source-control system and the real registries, and needs no fake: a fake gate would prove nothing about the gates every service runs.

#### 12.9 Call-type summary

None: the baseline is build-time; no REST, Kafka, Temporal or File call.

### 13. Solution plan

**Artefacts.** All paths are relative to the template repository; a new service repository is created from it and keeps the same layout.

| Path | Artefact | What it holds |
|---|---|---|
| `api/`, `worker/` | The two deployment skeletons | The API surface and the Temporal worker skeleton of Arch v5 slides 20 and 33, with `/health` and `/metrics` on the API |
| `db/migration/` | The migration sequence folder | The per-service Flyway folder that RWB-PLT-E1044-OPS fills; this story creates the folder and wires its lint gate |
| `contracts/` | The contract folder | The OpenAPI 3.1 and AsyncAPI documents of the service and the contract-test stubs built from them |
| `helm/` | The chart values folder | The values file of the service for the one chart of RWB-PLT-N004-OPS |
| `pipeline/pipeline.yaml` | The one pipeline definition | The eight gates in order, each with its thresholds as values, referenced from the template and never copied into a repository |
| `pipeline/boundary/rules.yaml` | The boundary rule set | The service's own short name and schema, the list of foreign schemas that are refused, and the rule set for a cross-schema statement, datasource, grant, join, migration and fixture |
| `pipeline/scans/config.yaml` | The scan configuration | The secret scan, the personal-data scan, the image scan and the unapproved-dependency check, each with its rule set as a value and no rule text in code |
| `pipeline/inventory/repositories.yaml` | The repository inventory | One row per service of the 19-service list: repository name, owning service, the template version it pins and its last gate result |
| `template.version` | The version file | The template version a repository was created from and pins, read by the first stage of every run |
| `pipeline/checks/layout-check` | The layout check | The six folders, the version file and the gate set compared with the template's, with a finding that names the repository and the difference |

**Pattern application.** None of the DP table applies to this story (`patterns` is empty): it introduces no legacy table, no legacy login, no legacy topic name and no legacy call. The patterns its rules serve are applied by the stories that own them: DP-15 (per-service Flyway sequence in the service's own schema) by RWB-PLT-E1044-OPS, DP-01 (the owner's schema, never another service's tables) and DP-02 (one login per service) by the ACE database stories. This story only fixes the repository in which those patterns are enforced and the gate that fails when one is broken.

**Build steps**

1. Publish the template at a version with the application skeleton of Arch v5 slide 20 and the six folders of the layout, and fix the version scheme with the solution architect.
2. Create the repository inventory with 19 rows from the 19-service list and one derived repository name per service, and agree the names with the platform administrator.
3. Create the pilot repository from the template, place the `template.version` file at its root and wire the first stage that refuses a missing or unpublished version.
4. Wire the one pipeline definition with the eight gates in order, every threshold a value of the template, and the check that compares a repository's gate set with the template's.
5. Write the boundary rule set for the pilot's own short name and schema, and add the four refusals: a foreign schema in a statement or a datasource, a grant on a foreign schema, a join across schemas, and a foreign object or row in a migration or a fixture.
6. Write the scan configuration: the secret scan over the tree, the full history, the build logs and the test data; the personal-data scan over code, tests and fixtures; the image scan of every built image; and the unapproved-dependency check.
7. Run all eight gates green on the pilot, then break each gate once in a separate change and record that each one fails the build and names its finding; keep the run as the evidence.
8. Fix the branch policy and the release identity: the protected default branch, the short-lived change branches, the immutable image digest per build and the release tag per service release.
9. Publish the inventory check that reports every repository on an older template version, and the upgrade path in which a service takes a new version in its own change and reruns the same eight gates.
10. Hand the layout, the gate set and the evidence to the service teams as the starting point of each of the 19 repositories.

**Done when.** A repository created from the template holds the six folders and records the template version; the same eight gates run in the same order for every service with the template's thresholds; each gate has been shown to fail a deliberately broken change and to name the finding; a cross-schema statement, datasource, grant, join, migration or fixture fails the boundary test; no secret and no production data is found in the tree, the history, the logs or the tests; every repository of the inventory pins the same template version; and a template change has been shown to raise the version and to reach a service only through that service's own change.

The exact layout inside each folder, the repository naming beyond the derivation from the §R4 short name, the branch policy, the toolchain and the version scheme are Not specified in the source documents (GAP-1425; ASM-2495), and each of the four is carried by its own assumption: the layout by ASM-2495, the branch policy by ASM-2496, the toolchain by ASM-2497 and the version scheme by ASM-2498.

### 14. Validation and messages

| ID | When | What is validated | Outcome |
|---|---|---|---|
| V1 | A repository is created from the template | The six folders are present, the template version is recorded and the version is one the template publishes | Creation is refused otherwise, and the missing folder or the unpublished version is named |
| V2 | A change is pushed to any repository | The gate set and its thresholds equal the template's, in the same order | The build fails and names the gate, the repository and the difference |
| V3 | Each gate runs | Build compiles and the approved dependency list holds; unit, contract and boundary tests pass; every migration lints; the image carries no critical finding; the secret and personal-data scans find nothing | The build stops at the failing gate, the later gates do not run, and the finding names the artefact and the rule |
| V4 | A statement, a datasource, a grant, a join, a migration or a fixture is read | It names only the service's own schema, and no other service's object or row | The boundary test fails the build and names the statement, the foreign schema, the owning service or the file |
| V5 | A secret scan or a personal-data scan runs | The tree, the full history, the build logs and the test data carry no secret and no production record or personal-data field | The build fails, the finding names the file and the rule and never prints the value, and the credential is rotated |
| V6 | The inventory check runs | Every repository pins the template version the template publishes, and a repository on another version is reported | The report lists the repository, its version and the current version; a build from a repository with no version is refused |
| V7 | A template change is published | The template version is raised before any service takes the change, and the change reaches a repository only through that repository's own pipeline | A template change that alters a repository directly is refused, and the inventory lists the repositories still to upgrade |

**Messages.** No message ID of the message catalogue applies to this story: the catalogue carries case, task, notice, job and access messages, and none of them describes a build or a repository finding. The baseline therefore adds no user-facing message. Every validation above is a pipeline finding addressed to the owner role of the repository, naming the repository, the gate, the artefact and the rule; a finding that should become a message waits for the catalogue to give it an ID and is not written as free text. The secret scan and the personal-data scan never print the value that was found, and the boundary test never copies a foreign row into its report. The English text of each finding of V1 to V7 is the Outcome column above; no message ID is assigned to any of them, and a finding is not a catalogue message.

### 15. Screens and states

None. This story adds no Workbench screen and no screen state. The operator surfaces are the source-control system, the pipeline and the registry, which the DevOps engineer and the platform administrator read through their own consoles and not through the Workbench. The states of section 9 are repository states and not screen states, and the only Workbench view that shows a related result is the connection-pool and service panel of the observability baseline RWB-PLT-N005-OPS, which is read-only for this story.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-NF01-OPS-01 | AC1 | Component | A pilot repository created from the template: the six folders present, the version file holding a published version, the layout check green; a repository with one folder removed and a repository with no version file each fail and are named |
| TC-PLT-NF01-OPS-02 | AC2 | End to end | One change pushed through the full pipeline: the eight gates run in the order build, unit, contract, boundary, migration lint, image scan, secret and personal-data scan with the template's thresholds; eight separate broken changes each fail at their own gate and stop the later gates; a repository that disables one gate fails the pipeline check |
| TC-PLT-NF01-OPS-03 | AC3 | Component | The boundary rule set of a service: a statement, a datasource, a grant and a join that name another service's schema each fail with the statement, the foreign schema and the owning service named; a migration and a fixture carrying a foreign object or row each fail with the file named; the service's own schema passes |
| TC-PLT-NF01-OPS-04 | AC4 | NFR | The secret scan of the tree, the full history, the build logs and the test data with no finding; a committed test credential fails the scan and is not printed; the personal-data scan of code, tests and fixtures with no finding; a production record in a fixture fails the scan; every credential resolved as a key reference at deploy time (NFR-052, NFR-054, NFR-045) |
| TC-PLT-NF01-OPS-05 | AC5 | Integration | The 19-row inventory: every repository pins the same template version and the check is green; one repository pinned to an older version is reported with its name and version; a template change raises the version, the inventory lists the repositories to upgrade, and one service takes the new version in its own change through the same eight gates |
| TC-PLT-NF01-OPS-06 | AC6 | Component | The baseline check on each of the 19 repositories: BR1 one service with its own code, release, owner, contract, schema, topic and task queue; BR2 the template build elements present; BR3 2 fixed API copies and a KEDA-scaled worker on its own task queue; BR4 the naming pattern holds; BR5 the eight gates and thresholds from the template; BR6 a foreign-schema reference fails the build; BR7 a secret or unapproved dependency blocks the build; BR8 no production data in a repository, test or log; BR9 one pinned template version on every repository |

### 17. Guardrails

- No business value in code: a gate threshold, a scan rule, a boundary rule and a template version are values of the template, and a change to any of them is a value change reviewed once and not a code change in 19 repositories.
- No secret in code, history, logs, tests or a prompt: every credential is a key reference resolved from the key store at deploy time (NFR-052), and the secret scan fails the build on a value and never prints it.
- No personal data in code, tests, fixtures or logs: the personal-data scan fails the build (NFR-054), and the only data a repository carries is synthetic.
- No production data in a repository, a test or a log: a production record or extract is refused by the personal-data scan, and the masked copy of user acceptance is loaded through the loading story and never committed (NFR-045).
- ACE data only through the owner's contract or the `v_ace_*` views: this story reads no ACE table and no service table, and the boundary test refuses a statement that names another service's schema.
- No gate bypass: a gate cannot be disabled, reordered or re-thresholded in one repository, the gate set is the template's, and the pipeline check fails a repository that tries.
- No hand change in a repository: the layout, the gate set and the version file are code in the template, a hand edit is reported by the next run, and a template change reaches a service only through that service's own change.
- One repository per service and no shared repository: a repository holds one service's code, one service's migrations and one service's values, and no second service is added to it.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| NFR-045 | No production data in the development environment, and the user acceptance environment uses masked copies | The personal-data scan of code, tests and fixtures, and the rule that a repository carries synthetic data only | TC-PLT-NF01-OPS-04 |
| NFR-052 | Secrets are held in the key store and never in code, configuration files or prompts | The key-reference form of a configuration file and the secret scan of the tree, the history, the logs and the test data | TC-PLT-NF01-OPS-04 |
| NFR-054 | The build pipeline blocks a change that carries a secret, personal data in code, tests or logs, or an unapproved dependency | The same eight gates for every service, including the secret scan, the personal-data scan and the unapproved-dependency check of the build gate | TC-PLT-NF01-OPS-02, TC-PLT-NF01-OPS-04 |
| ADR-013 | 19 services inside ACE | The one-repository-per-service rule and the 19-row repository inventory | TC-PLT-NF01-OPS-01, TC-PLT-NF01-OPS-05 |
| Arch v5 slide 4 | One deployable service per module, each with its own code, release, owner, contract, schema, topic and task queue | The repository per service and the release identity of one image digest and one release tag | TC-PLT-NF01-OPS-01, TC-PLT-NF01-OPS-05 |
| Arch v5 slides 20 and 33 | Every service from the one template with API and worker deployments, `/health` and `/metrics` | The `api/` and `worker/` folders of the layout and the template version each repository pins | TC-PLT-NF01-OPS-01 |
| Arch v5 slides 29 and 41 | One schema and one login per service, no grant on another schema; the shared naming of schema, REST base, topic and task queue | The boundary rule set and the check that no repository holds another service's schema, object or row | TC-PLT-NF01-OPS-03 |
| Arch v5 slide 38 | Wave 0 builds the service template and the golden pipeline once, and every epic adds only its services | The template version, the one pipeline definition and the upgrade path in which a service takes a new version in its own change | TC-PLT-NF01-OPS-02, TC-PLT-NF01-OPS-05 |

### 19. Out of scope

- The Helm chart itself, its templates and its versions: RWB-PLT-N004-OPS owns the chart and the pipeline template, and this story only carries their values file and the gates that run them.
- The migration files, their versions and the Flyway history: RWB-PLT-E1044-OPS owns the versioned migration mechanism, and this story only creates the `db/migration` folder and wires its lint gate.
- The four environments, their clusters, namespaces, pools and data classes: RWB-PLT-NF03-OPS owns the environment baseline, and this story produces the build that is promoted into them.
- The secret and configuration baseline, the key store client and the credential rotation: RWB-PLT-NF04-OPS owns them, and this story only fails a build on a value and never stores a secret.
- The 19 schemas, the 19 logins and their grants: RWB-PLT-NF06-DB and the ACE database stories own them; the boundary test reads the grant rule and owns no DDL.
- The shared libraries, the outbox and inbox library, the decision-record library and the workflow kit: the RWB-PLT-LIB and RWB-PLT-WF epics own them.
- The application code of each of the 19 services: the service APP stories own it, and this story delivers only the skeleton and the gates.
- The observability baseline, the dashboards and the alerts: RWB-PLT-N005-OPS owns them, and this story inherits them for the pipeline's own signals.
- The CI engine, the registries and the branch protection as infrastructure: the platform infrastructure stories own them, and this story names them only as values of the template.
- The exact layout inside each folder, the repository naming beyond the derivation from the §R4 short name, the branch names, the toolchain and the version scheme: the gap GAP-1425 and its assumptions ASM-2494 to ASM-2498, for the platform administrator and the solution architect to close before the first service repository is created as the run of record.
