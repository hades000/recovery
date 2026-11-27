# RWB-PLT-E2037-CON Temporal observability and run books - contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E2037-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-WF |
| Wave | 0 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-037 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP05, DP06, DP07, DP10, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Size | To be sized by the squad at refinement |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |
| Contract version | Draft (realignment v1), frozen when the consuming stories pass their contract tests |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E2-037 for the workflow platform epic; the metric names and labels, the three alert rules, the annotation, the dashboard data contract, the alert-to-run-book map and the scanner query are published on Day 1 with fakes. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (6 resolved, 27 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **consumer of the Temporal observability contract (platform and operations teams, service teams)**, I want **the metric names and labels, the three alert rules and their annotation contract, the dashboard data contract, the alert-to-run-book map contract and the scanner query contract published on Day 1 with fakes**, so that **alerts, dashboards and run books are built and tested against one frozen set**.

This is the contract story of legacy key RWB-E2-037 under epic RWB-PLT-WF. A shared engine cannot wait until the rules exist to agree what they are called, so the contract fixes in one versioned document set, before any rule is written: the metric names and their label sets, the three alert rules with their thresholds and the annotation they carry, the queries the dashboard may make and the four search attributes they may read, the alert-to-run-book map and the eight sections every run book must have, and the scanner's visibility and history query with the rule that it holds no grant on the Temporal databases.

The platform is **not one of the 19 services**. Template and Rules §R4 has no platform row, so this contract publishes names and shapes only and never a business model: no `rwb_*` schema, no `rwb.<short>.events.v1` topic and no `/api/recovery/<short>/v1` base (DP-13, DP-14). The namespace is `rwb-recovery` and the platform task queue is task queue `rwb-platform`, both fixed elsewhere and recorded here. The contract is published at status Draft (realignment v1) and is frozen when the consuming stories pass their contract tests.

The platform identity, meaning the login that runs the scanner, the task queue provisioning record and the admin base the catalogue read uses, is named by no read source: Not specified in the source documents (GAP-1445; ASM-2540). The contract therefore declares the shapes of the observability surface and leaves the identity to the Wave 0 Service Catalog, which is where the platform team fixes it once for every platform story.

### 2. Business rationale

An alert without a run book is a page nobody can act on, and a dashboard that reads a payload leaks personal data. In the monolith both facts were safe by accident: one process held the metrics, the alerts, the dashboard and the run books, so a missing run book was a review comment and a payload in a panel was a screen nobody could reach. In the target the metrics come from a shared cluster, the alerts come from a rule file that several teams may edit, the dashboard is provisioned from a repository and the run books live with the operations team (Architecture v5 slides 20, 23 and 27; Ownership Map jobs JOB-21). Nothing in that chain forces the four artefacts to agree unless a contract does.

The contract fixes the names, the labels, the four search attributes, the message annotation and the run book map before the rules exist, for three reasons. First, the rules, the panels and the run books are written by different people and tested by a pipeline, so a shared vocabulary is the only thing that lets RunbookCompletenessTest and DashboardPersonalDataCheck fail a build that drifts. Second, the personal-data boundary is a declaration, not a habit: the dashboard reads CaseId, Stage, ProductGroup and QueueCode and nothing else, and the annotation carries the workflow identifier and the hours, never a payload. Third, the scanner's read is published with its no-grant rule, so no later change turns the scan into a direct read of the Temporal databases. This meets REQ-DRI-007 (a named owner and a tested way back for every failure) and ADR-023 (observability per service, here applied to the shared platform that runs the workflows). The measure is that every contract test answers from the fakes on Day 1 and that a breaking change raises v2 instead of editing v1.

### 3. Preconditions

- The cluster and worker contracts are published: namespace `rwb-recovery` with its 30-day retention and the four Keyword search attributes, the client certificate profile and the frontend API subset (RWB-PLT-E1070-CON), and the platform worker on task queue `rwb-platform` with its build ID and SDK metrics (RWB-PLT-E1071-CON).
- The `job_catalog` contract of P2 rwb-integration exists, so the scanner's row and the alert-to-run-book map are read and written through its admin operation and never by a table read (Ownership Map: job_catalog, api `GET /admin/scheduled-jobs`).
- The monitoring stack exists in the ACE monitoring namespace: Prometheus with a scrape of the Temporal server and worker SDK metrics, Alertmanager with the platform on-call rota and the incident queue, and Grafana with a provisioned data source for Prometheus and for the Temporal visibility API.
- The run book catalog and its gate exist (RWB-PLT-E1056-OPS): the eight sections, the run book path convention and RunbookCompletenessTest.
- The parameter contract is published, so `temporal.stuck.hours` and the thresholds are values and not literals in a rule expression (RWB-PLT-E1042-CON, DP-06).
- The contract is Draft (realignment v1) until the consuming stories pass their contract tests; no approval is required to publish a Draft contract.
- The platform identity is named by no read source: Not specified in the source documents (GAP-1445; ASM-2540).

### 4. Flow

1. The contract author writes the metric contract: `workflow_stuck` by workflow type, `temporal_scanner_failures_total` and the last successful scan time, each with its type, its label set and the statement that no label holds a person or a payload field.
2. The author writes the three rule contracts: `TemporalWorkflowFailed`, `TemporalWorkflowStuck` and `TemporalScheduleToStartLatency`, each with its expression shape, its threshold as a named value, its window and its severity.
3. The author writes the annotation contract: the message identifier MSG-P3-037, the placeholders {workflowId} and {hours}, the run book path annotation and the summary text of the latency alert, which uses no message identifier.
4. The author writes the dashboard data contract: the named queries, the five panel groups and the rule that every panel reads the four search attributes CaseId, Stage, ProductGroup and QueueCode only, with no payload, history event or case field.
5. The author writes the alert-to-run-book map contract: one run book per alert, its path under `docs/operations/runbooks`, the eight sections and the gate that fails a build without them.
6. The author writes the scanner query contract: the visibility query (status RUNNING and StartTime older than the stuck window), the history summary read, the stuck test with its exclusions, the five-minute Schedule on task queue `rwb-platform` and the no-grant rule on the Temporal databases.
7. The fakes are generated from the declarations: the metric fixtures, the Alertmanager fake with the routing result and the three alert states, and the Grafana provisioning fake that answers the named queries.
8. The contract test runs the fakes against the documents on every change: every metric answered, every rule evaluated against its fixture, every panel query answered, every map entry resolved and every refusal produced.
9. The contract is published as v1 to the contract registry; the app story, the run book set and the service teams' dashboards pin the version.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A rule is declared with no entry in the alert-to-run-book map, or its run book lacks one of the eight sections | The contract test fails naming the alert and the missing section, and the version is not published | Lint finding, no message id | AC4 |
| X2 | A panel query names a person field, a payload field, a history event payload or a case field | The personal-data step fails the contract test, and the query is not published | Lint finding, no message id | AC1, AC3 |
| X3 | A failed scan publishes a zero, or the contract lets a zero stand in for a result | The contract test fails: a failed scan publishes no stuck value, raises the failure counter and marks the panel stale | Lint finding, no message id | AC1, AC3 |
| X4 | A change breaks a consumer: a renamed metric or label, a removed rule, a changed annotation placeholder or a changed map key | The change raises a new version, marks the current version deprecated, and no consumer sees an edited document | Lint finding, no message id | AC6 |
| X5 | A value the consumers need is named by no read source (the platform login, the task queue provisioning record, the admin base, the dashboard name) | The value is published as the working read of the assumption, with the placeholder where it is still open, and the gap stays open | Not specified in the source documents (GAP-1445; ASM-2540) | None (open gap GAP-1445; ASM-2540) |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Publishes documents and fakes; builds no rule, no dashboard and no scanner, reads no business data and depends on no other story |
| Negotiable | Document layout, example timestamps and the internal structure of the fakes are open until the version is frozen; the metric names, the label sets, the thresholds, the annotation, the four search attributes, the eight run book sections and the no-grant rule are fixed |
| Valuable | The app story, the run book set, the operations team and the service teams' dashboards start on Day 1 against one frozen observability contract |
| Estimable | One metric contract, three rule contracts, one annotation contract, one dashboard data contract, one map contract, one scanner query contract, three fakes and one contract test |
| Small | One sprint for the documents, the fakes and the contract test |
| Testable | Each criterion in section 7 is a schema, lint or fake assertion in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Temporal observability contract, alert-to-run-book map and scanner query

  Background:
    Given the platform is shared platform and owns no schema, no topic and no Workbench REST base
    Given the observability surface serves the workflows of namespace rwb-recovery on task queue `rwb-platform`

  Scenario: AC1 The metric contract declares the three metrics, their labels and no personal data (new, D-RCV-60)
    Given the metric contract document
    When it is validated against the metric schema
    Then it declares workflow_stuck with the label workflowType and a value that is a count of stuck executions
    Then it declares temporal_scanner_failures_total as a counter with the label reason and no case label
    Then it declares the last successful scan time as a gauge with the label taskQueue, whose value is task queue `rwb-platform`
    Then no declared label or value holds a person field, a payload field or a case field, and the contract names no name, national identifier or account number

  Scenario: AC2 The three alert rules, their thresholds and the annotation are declared (new, D-RCV-60)
    Given the rule contract document
    When it is validated
    Then it declares TemporalWorkflowFailed for an execution that closes FAILED or TIMED_OUT, with the failure window of 5 minutes and severity "page"
    Then it declares TemporalWorkflowStuck for a RUNNING execution with no progress for temporal.stuck.hours = 24, with no open timer and no activity in retry
    Then it declares TemporalScheduleToStartLatency for a p95 schedule-to-start latency above 60 seconds for 10 minutes
    Then each threshold is a named value the rule file supplies, never a literal in an expression
    Then the annotation of TemporalWorkflowFailed and TemporalWorkflowStuck carries MSG-P3-037 with {workflowId} and {hours} and the run book path
    Then the latency alert carries its own summary with the task queue and the p95 and uses no message id

  Scenario: AC3 The dashboard data contract names the queries and the four search attributes only (new, D-RCV-60)
    Given the dashboard data contract
    When every declared query is reviewed against the attribute list
    Then it names the five panel groups: volume by type and status, schedule-to-start latency by task queue, task queue backlog, stuck workflows and worker build IDs
    Then every query reads the search attributes CaseId, Stage, ProductGroup and QueueCode only
    Then no query reads a workflow input, a workflow output, a history event payload, a case field or an ACE view
    Then the contract states the two data states of every panel: current, and data stale since the last successful scan

  Scenario: AC4 The alert-to-run-book map requires one run book with the eight sections per alert (new, D-RCV-60)
    Given the alert-to-run-book map contract
    When the map is reviewed against the run book catalog
    Then every alert has exactly one run book under docs/operations/runbooks, named by its path
    Then every run book must carry the eight sections purpose, schedule, owner, dependencies, failure signs, checks, restart steps and escalation
    Then a rule with no map entry, or a map entry whose run book lacks a section, fails the gate and the version is not published
    Then no map entry names a person, and each names a role and a service identity

  Scenario: AC5 The scanner query contract declares the visibility query, the history read and the no-grant rule (new, D-RCV-60)
    Given the scanner query contract
    When it is validated against the frontend API subset
    Then it declares the visibility query as status RUNNING and StartTime older than temporal.stuck.hours on namespace rwb-recovery
    Then it declares the history summary read through GetWorkflowExecutionHistory for each candidate
    Then it declares the stuck test: no history event for the stuck window, no open timer and no activity in retry
    Then it declares the Schedule run every 5 minutes on task queue `rwb-platform` as JOB-21, with overlap policy SKIP
    Then the Schedule ID is JOB-21, overlap policy SKIP allows no overlap, catch-up after downtime is none, the Schedule is not paused on failure, the closed-run retention is Not specified in the source documents (GAP-2022), and the failed run raises the scanner alert
    Then it states that the scanner holds no grant on the Temporal databases and reads visibility and history through the frontend API over mTLS only

  Scenario: AC6 The fakes answer every contract test and a breaking change raises v2 (new, D-RCV-60)
    Given the metric fixtures, the Alertmanager fake and the Grafana provisioning fake
    When the contract test runs against the documents
    Then the metric fixtures answer every declared metric and label
    Then the Alertmanager fake answers the three rule evaluations and the routing result, and holds the alert states PENDING, FIRING and RESOLVED with their times
    Then the Grafana provisioning fake answers every declared query and refuses a query outside the four search attributes
    Then the map and the scanner query answer every assertion of AC4 and AC5
    Then a breaking change raises v2 and marks v1 deprecated, and no consumer sees an edited v1

  Scenario: AC7 A status change the model does not allow is refused (new, D-RCV-60)
    Given the alert states PENDING, FIRING and RESOLVED of the Alertmanager fake
    When a status change that the model does not allow is requested
    Then the change is refused and the alert keeps its previous state
```

The seven criteria are new and test only the contract baseline: no legacy acceptance criterion is repeated here, and every value in the declarations is the value of RWB-E2-037 or of the read sources, character for character.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The contract declares every metric name, its type and its label set, and no metric, label or value carries a person, a payload or a case field | ADR-023; Architecture v5 slides 20 and 27 |
| BR2 | The three rules are declared with their thresholds as named values: the 5-minute failure window, `temporal.stuck.hours` = 24 with no open timer and no retry, and the 60-second p95 over 10 minutes; a threshold is never a literal in an expression | RWB-PLT-E2037-APP; DP-06 |
| BR3 | The annotation contract carries MSG-P3-037 with {workflowId} and {hours} and the run book path, and no annotation carries a payload; the latency alert uses its own summary and no message id | RWB-E2-037; RWB-PLT-E2037-APP section 14 |
| BR4 | The dashboard data contract names the queries and fixes the four search attributes CaseId, Stage, ProductGroup and QueueCode as the only readable fields, with the two data states current and stale | ADR-023; Architecture v5 slide 27 |
| BR5 | Every alert has exactly one run book with the eight sections of the catalog of RWB-PLT-E1056-OPS; the map is the record and the gate fails the build when an entry is missing or incomplete | RWB-PLT-E1056-OPS |
| BR6 | The scanner query contract declares the visibility query and the history summary read through the frontend API over mTLS, and the rule that the scanner holds no grant on the Temporal databases | RWB-PLT-E1070-CON; Temporal and Drools Design slide 11 |
| BR7 | The fakes are test-only and are never deployed to SIT, UAT or PROD; they answer from the declarations, so a drift shows as a contract-test failure | Template and Rules §R7.2 section 12.8 |
| BR8 | A breaking change raises a new version and deprecates the current one; a published version is never edited in place | Template and Rules §R7.2 |

### 9. State transitions

The contract has its own lifecycle; the alert object it describes has the states of the fake. This story changes no case status.

| Object | From | Event | To |
|---|---|---|---|
| Contract | Draft | The consuming stories pass their contract tests | Published |
| Contract | Published | A consumer pins the version and the change window closes | Frozen |
| Contract | Published or Frozen | A breaking change is accepted | A new version, and the old version is Deprecated |
| Alert in the fake | None | The rule evaluates true | PENDING |
| Alert in the fake | PENDING | The condition is still true at delivery | FIRING |
| Alert in the fake | PENDING | The condition clears before delivery | RESOLVED, no page |
| Alert in the fake | FIRING | The condition clears | RESOLVED |
| Workflow in the fixtures | RUNNING | The fixture closes the execution | COMPLETED, FAILED or TIMED_OUT |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract author (any team, per U3) | Writes and versions the documents, the map, the fakes and the contract test |
| The platform owner of the Temporal layer | Approves a breaking change and a version freeze |
| The operations team | Reads the map and the run book rule, confirms the routing labels and the eight sections, raises a change request |
| The service teams of the 19 services | Read the metric, rule, dashboard and scanner declarations, confirm the workflow types they own, raise a change request |
| The ACE monitoring team | Owns Prometheus, Alertmanager and Grafana; the contract names their endpoints and never republishes them |
| No delegation of authority level applies | A platform contract is a technical artefact, not a credit decision |

No personal name, no email address and no credential appears in a document or in a fake; where a caller or a grantee must be named, the example uses a role code or a service identity only.

### 11. Data

| Item | Value | BR Field ID |
|---|---|---|
| Business data published | None. The contract publishes metric names, label names, query text, thresholds, placeholders and paths; no case, customer, account or document value appears | Not specified in the source documents (DOR-RWB-PLT-E2037-CON-7) |
| Personal data | None, and none is admitted: the dashboard queries read the four search attributes only, and no label or annotation may hold a person field | Not specified in the source documents (DOR-RWB-PLT-E2037-CON-7) |
| Data in the fakes | Synthetic workflow identifiers only, including the legacy fixtures platform-smoke-20261116, case-RW-2026-000123, case-RW-2026-000124 and case-RW-2026-000125, and synthetic metric series | Not specified in the source documents (DOR-RWB-PLT-E2037-CON-7) |
| Data held by the platform | The Temporal persistence stores of RWB-PLT-E1070; alert state in Prometheus and Alertmanager; the scanner's row and the map in job_catalog, owned by P2 rwb-integration | Not specified in the source documents (DOR-RWB-PLT-E2037-CON-7) |
| Field identifiers | None owned. The platform owns no `rwb_*` field and no ACE field; the catalogue fields DF-OPS-224 to DF-OPS-232 belong to P2 rwb-integration | Not specified in the source documents (DOR-RWB-PLT-E2037-CON-7) |
| Retention | The contract document keeps no data; the fakes are rebuilt on every build and store nothing | Not specified in the source documents (DOR-RWB-PLT-E2037-CON-7) |

### 12. Contract

#### 12.1 REST operations provided

None. The platform has no service short (Template and Rules §R4 has no platform row), so the contract publishes no path under `/api/recovery/<short>/v1` and no Workbench endpoint. What it publishes is a document set and a fake set: metric names, rule contracts, an annotation contract, a query contract and a map contract (DP-13).

#### 12.2 REST operations consumed

None. The contract itself consumes nothing; the scanner that implements its query contract reads the catalogue through `GET /api/recovery/integration/v1/admin/scheduled-jobs` in RWB-PLT-E2037-APP, one hop and a 2 s budget (DP-11), and that read is recorded there and not here.

#### 12.3 Events published

None. The platform publishes no `rwb.<short>.events.v1` topic and no event schema (DP-14); the contract declares no event and the observability surface produces metrics, alerts and catalogue rows only.

#### 12.4 Events consumed

None. The contract consumes no Kafka topic, and the scanner it describes reads the Temporal visibility and history API rather than an event stream.

#### 12.5 Workflows and activities

None owned. The contract declares the shape of the scanner run rather than a workflow: JOB-21 is a Temporal Schedule on task queue `rwb-platform` every 5 minutes, and its run is a short workflow with overlap policy SKIP, owned by RWB-PLT-E2037-APP (DP-10; Architecture v5 slide 44; Ownership Map jobs JOB-21). The contract fixes the query and the no-grant rule; the app story builds the workflow, the activities and the Schedule registration.

#### 12.6 Schedules

None registered. The contract declares the cadence of JOB-21 as every 5 minutes on task queue `rwb-platform` and records that the legacy 15-minute Quartz interval is superseded; it registers no Schedule and owns no batch window.

#### 12.7 Tables owned

None. The contract owns no `rwb_*` schema and no table; the scanner's row and the alert-to-run-book map live in `job_catalog`, owned by P2 rwb-integration and written only through its admin operation, and no migration of this story runs (DP-01, DP-15).

#### 12.8 Contract fakes

| Fake | Serves | Used by |
|---|---|---|
| Metric fixtures (this story) | Synthetic Prometheus series in the declared names and labels: `workflow_stuck` by workflow type, `temporal_scanner_failures_total`, the last successful scan time, the failed and timed-out counters and the schedule-to-start histogram | The rule and panel assertions of RWB-PLT-E2037-APP, TC-PLT-E2037-CON-01 and TC-PLT-E2037-CON-02 |
| Alertmanager fake (this story) | The alert receive endpoint, the routing result for the platform on-call rota and the incident queue, and the alert states PENDING, FIRING and RESOLVED with their times | The annotation, routing and resolve assertions of TC-PLT-E2037-CON-02 and TC-PLT-E2037-CON-06 |
| Grafana provisioning fake (this story) | The provisioning endpoint and the data-source answers for every declared query, with a refusal for a query outside the four search attributes | The query and personal-data assertions of TC-PLT-E2037-CON-03 and TC-PLT-E2037-CON-06 |

The three fakes answer from the declarations of this document and of sections 7 and 13, so a change to a declaration shows up as a contract-test failure rather than as a difference between environments. They are test-only and are never deployed to SIT, UAT or PROD.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 0 | The contract is a document set and a fake set; the platform publishes no Workbench base |
| Kafka | 0 | 0 | No topic and no event schema; an alert is not an event |
| Temporal | 0 | 0 | The contract declares the shape of the JOB-21 Schedule run and owns no workflow, no activity and no queue entry |
| File | 0 | 0 | The documents and the fakes are build artefacts, not files read at runtime |

### 13. Solution plan

**Deliverables**

| Deliverable | Form | Content |
|---|---|---|
| Metric contract | Versioned document plus schema | `workflow_stuck` by workflow type, `temporal_scanner_failures_total`, the last successful scan time, with types, label sets and the no-personal-data rule |
| Rule contracts | Versioned document plus schema, one entry per rule | The three rules, each with its expression shape, its named thresholds, its window and its severity |
| Annotation contract | Table in the document and in the rule schema | MSG-P3-037 with {workflowId} and {hours}, the run book path annotation, and the latency summary with no message id |
| Dashboard data contract | Versioned document plus query list | The five panel groups, the named queries, the four search attributes, the two data states and the refusal of a payload or case field |
| Alert-to-run-book map contract | Versioned document plus map file | One run book per alert, its path, the eight sections and the gate rule |
| Scanner query contract | Versioned document plus query file | The visibility query, the history summary read, the stuck test, the 5-minute Schedule on task queue `rwb-platform` and the no-grant rule |
| Fakes | Test-only runnable set | The metric fixtures, the Alertmanager fake and the Grafana provisioning fake |
| Contract test | Test suite in the build | Every declaration, every rule evaluation, every query, every map entry and every refusal asserted against the fakes |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

These are the Template and Rules §R5.5 rows that bear on a platform contract. DP-10 is the substantive one: the contract declares the scanner as a Temporal Schedule on task queue `rwb-platform` every 5 minutes, so no reader of the document can rebuild the legacy Quartz job on a 15-minute interval, and the workflow kit is a dependency rather than an option. DP-06 keeps the stuck window and the three thresholds as named values supplied by the rule file and the parameters contract, so the document fixes no number that a configuration change would have to edit. DP-07 keeps the severity vocabulary and the run book paths as data, so a new severity is a value and not a document version. DP-03, DP-05, DP-01, DP-13, DP-14, DP-15 and DP-19 are declared as absences: the observability path writes no decision record, reads no `rwb_*` table and no ACE view, publishes no `/api/recovery` base and no topic, runs no migration, and composes no Workbench screen. This story adds no dependency of its own: it is a CON story and starts on Day 1.

**Build steps**

1. Write the metric contract and its schema: the three metrics, their types, their label sets and the no-personal-data rule.
2. Write the three rule contracts and the annotation contract, and generate the rule table of section 7 and the map of section 13 from them so the documents and the fakes cannot drift.
3. Write the dashboard data contract: the five panel groups, the named queries and the four search attributes, with the refusal of a payload, a history event or a case field.
4. Write the alert-to-run-book map contract and the scanner query contract, including the 5-minute Schedule, the overlap policy and the no-grant rule on the Temporal databases.
5. Build the three fakes from the declarations, with synthetic metric series, the three alert states and the query answers and refusals.
6. Write the contract test and publish v1 to the contract registry; notify the app story, the run book set and the service teams, and record the version each one pins.

**Done when.** Every document validates, the rule table, the map and the query list match the documents, the three fakes answer every declaration of sections 7, 12 and 13 including the refusals, and the contract test is green on the build of this story.

### 14. Validation and messages

| ID | When | Message | Published as |
|---|---|---|---|
| MSG-P3-037 | A workflow has failed, or has not moved for the stuck window; declared in the annotation of the two rules | Workflow {workflowId} has failed or has not moved for {hours} hours. | Alert annotation |
| PLT-OBS-001 | A rule has no map entry, or its run book lacks one of the eight sections | Lint finding naming the alert and the missing section; the version is not published | Build finding |
| PLT-OBS-002 | A panel query names a person field, a payload field, a history event payload or a case field | Lint finding naming the query and the field; the query is not published | Build finding |
| PLT-OBS-003 | A failed scan publishes a zero instead of no value | Lint finding: a failed scan publishes no stuck value and marks the panel stale | Build finding |
| PLT-OBS-004 | A declaration changes in a way that breaks a consumer | The change raises v2 and deprecates v1; no consumer sees an edited document | Version notice |

MSG-P3-037 is the only message identifier this contract publishes, and it publishes it as a placeholder contract, not as text: the wording belongs to the message catalogue and is quoted here unchanged. The four platform findings are reserved identifiers for the contract test and carry no business value. The platform identity and the dashboard names are Not specified in the source documents (GAP-1445; ASM-2540) and are read from the Wave 0 Service Catalog when it is published.

### 15. Screens and states

No screen in this story, and the document set declares none: the dashboard it describes is an operational view provisioned from a repository, not a Workbench screen, and no route is added to the gateway (DP-19). The contract fixes the two data states every panel must expose, current and data stale since the last successful scan, and the three alert states of the fake, PENDING, FIRING and RESOLVED. The Workbench screens are the gateway-bff surface and the front end, and the platform adds nothing to them.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E2037-CON-01 | AC1, BR1 | Contract | The metric contract validated: `workflow_stuck` by workflow type, `temporal_scanner_failures_total` with the label reason, the last successful scan time with task queue `rwb-platform`; the no-personal-data rule |
| TC-PLT-E2037-CON-02 | AC2, BR2, BR3 | Contract | The three rule contracts: the 5-minute failure window, `temporal.stuck.hours` = 24 with no open timer and no retry, the 60-second p95 over 10 minutes; MSG-P3-037 with {workflowId} and {hours} |
| TC-PLT-E2037-CON-03 | AC3, BR4 | Contract | The dashboard data contract: five panel groups, the named queries, the four search attributes only, the two data states, the refusal of a payload or case field |
| TC-PLT-E2037-CON-04 | AC4, BR5 | Component | The alert-to-run-book map: three alerts, three run books, the eight sections, one missing section refused, no person named |
| TC-PLT-E2037-CON-05 | AC5, BR6 | Contract | The scanner query contract: status RUNNING with StartTime older than the stuck window, the history summary read, the 5-minute Schedule on task queue `rwb-platform`, the no-grant rule |
| TC-PLT-E2037-CON-06 | AC6, BR7, BR8 | Component | The metric fixtures, the Alertmanager fake with PENDING, FIRING and RESOLVED, the Grafana provisioning fake with its refusals; a breaking change raising v2 and deprecating v1 |
| TC-PLT-E2037-CON-07 | AC7 | Component | The Alertmanager fake alert states PENDING, FIRING and RESOLVED: a status change the model does not allow is refused and the alert keeps its previous state |

### 17. Guardrails

- No business value and no personal data in a document, an example or a fake: metric names, label names, thresholds, placeholders, paths and synthetic workflow identifiers only.
- The four search attributes stay CaseId, Stage, ProductGroup and QueueCode; a new attribute is a breaking change and is never added quietly.
- No annotation carries a payload or a case field; MSG-P3-037 carries the workflow identifier and the hours only.
- No service short, no schema name, no topic name and no Workbench REST base in the document set: the platform owns none of them (DP-13, DP-14).
- Every alert has exactly one run book with the eight sections, and no run book names a person.
- The scanner holds no grant on the Temporal databases; the contract states the rule, and the app story proves it (BR6).
- The fakes are test-only, hold synthetic data and are never deployed to SIT, UAT or PROD; no environment value points at one.
- The contract is versioned: a breaking change raises v2 and deprecates v1 in place of editing v1.
- Every threshold is a named value supplied by the rule file or the parameters contract; no number is baked into an expression.

### 18. Traceability

| Requirement ID | Requirement (short) | Source | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Every failure reaches a named owner and has a tested way back | Epic 2, 3.2; Program, 6.12 | TC-PLT-E2037-CON-02, TC-PLT-E2037-CON-04, TC-PLT-E2037-CON-06 |
| ADR-023 | Observability per service: metrics, alerts and dashboards are declared once and owned by the piece that produces them | Architecture v5 slides 20 and 27 | TC-PLT-E2037-CON-01, TC-PLT-E2037-CON-03 |

| Decision or source | What it fixes here |
|---|---|
| ADR-023 | Observability per service: the contract declares the metric, the rule, the query and the run book map once, and the platform owns the workflow-level view of the shared engine |
| DP-03 | The observability path writes no decision record; the local decision-record library is a template dependency and is never called by an alert, a scan or a panel |
| DP-10 | A Schedule replaces Quartz: JOB-21 is a Temporal Schedule on task queue `rwb-platform` every 5 minutes, and the legacy 15-minute interval is superseded (GAP-1446) |
| Architecture v5 slide 20 | Every service publishes its contracts before code and contract tests run in every build; the platform follows the same rule for its observability surface |
| Architecture v5 slide 23 | The workflow kit and the reusable layers: the platform publishes the contracts of the layer it owns and never the domain workflows |
| Architecture v5 slide 27 | Rules, thresholds and reference values are configuration in force, not literals; the three thresholds are named values |
| Architecture v5 slide 44 | The job map: JOB-21 stuck workflow scan, every 5 minutes, platform owner, visibility query plus alert; JOB-22 smoke workflow at 06:00 |
| Template and Rules §R7.2 section 12.8 | A contract story publishes fakes; the three fakes here are test-only and answer every declaration |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E2037-APP | App development | H consumer: builds the three rules, the Schedule-started scanner, the dashboard and the three run books against this contract and its fakes |
| RWB-PLT-E1070-CON | Contract | The namespace, the search attributes, the client certificate profile and the frontend API subset the scanner query contract uses |
| RWB-PLT-E1071-CON | Contract | The platform worker on task queue `rwb-platform`, its build ID and SDK metrics the metric contract declares |
| RWB-PLT-E1027-CON | Contract | The local decision-record library the platform worker template wires; the observability path writes no record (DP-03) |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | The parameters and reference data that supply the stuck window, the thresholds and the severity vocabulary (DP-06, DP-07) |
| RWB-PLT-E1047-CON, RWB-PLT-E1044-CON | Contract | The naming library the platform does not use and the Flyway convention this story does not run (DP-14, DP-15) |
| RWB-PLT-N001-CON | Contract | gateway-bff; the dashboard is not a Workbench screen and no route is added (DP-19) |
| RWB-PLT-E1056-OPS | DevOps | X: holds the run book catalog, the eight sections and RunbookCompletenessTest that the map contract points at |
| RWB-PLT-E2038-APP, RWB-PLT-E2038-CON | Successors of RWB-E2-038 | Out of scope: the codec server, decode and the Temporal admin audit |

### 19. Out of scope

- The three rule files, the Schedule registration, the scanner implementation, the dashboard JSON and the three run books: RWB-PLT-E2037-APP.
- The cluster, the namespace and the persistence stores: RWB-PLT-E1070-APP and RWB-PLT-E1070-CON.
- The worker, the SDK wiring and the platform task queue: RWB-PLT-E1071-APP and RWB-PLT-E1071-CON.
- The Workbench jobs' run books and the run book catalog itself: RWB-PLT-E1056-OPS; this story points at its eight sections and owns none of them.
- The platform smoke Schedule JOB-22 and its workflow.
- The codec server, decode and the Temporal admin audit: RWB-PLT-E2038-APP and RWB-PLT-E2038-CON.
- Backup, restore, zone failover, upgrade and archive: the successors of RWB-E2-039; the replay gate and build ID rollout: the successor of RWB-E2-040.
- The 19 services' own metrics, dashboards, alert rules and run books; the contract declares the platform's observability surface only.
- Workbench screens and the admin console (Epic 8); the dashboard is an operational view.
