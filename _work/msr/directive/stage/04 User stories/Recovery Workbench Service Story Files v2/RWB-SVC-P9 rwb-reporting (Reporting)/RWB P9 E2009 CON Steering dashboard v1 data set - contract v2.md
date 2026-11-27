# RWB-P9-E2009-CON Steering dashboard v1 data set — contract

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E2009-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 2 |
| Business epic | EP02 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-E2-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP07, DP10, DP11, DP13, DP15, DP17, DP19 |
| Parallel lane | CG-W2 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-P9-E2009-CON-16) |
| Contract version | v1 (the /v1 path) |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (FR-P9-007, FR-P9-009, FR-P9-010, FR-P9-011, FR-P9-012, FR-P9-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: the contract baseline of RWB-E2-009 for rwb-reporting — the `GET /reports/measures` shape with the dimension and baseline fields, the `measure_publish` schema, the consumed declarations and their fakes, the event subscriptions with their consumer groups, the workflow registration contract of JOB-15, the error model and the message map — is published as one frozen baseline so that RWB-P9-E2009-APP and RWB-P9-E2009-OPS start on Day 1. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-P9-E2009-CON). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (21 resolved, 31 cross-document, 4 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **contract owner of the reporting service (TechX)**, I want **one published baseline for the steering dashboard data set — the shape of `GET /reports/measures`, the `measure_publish` schema, the consumed contracts with their fakes, the event subscriptions, the registration contract of JOB-15 and the message map — so that** the application story, the deployment story and the Power BI consumer build on Day 1 against a fake and no shape is decided twice.

The baseline fixes, and nothing else:

- the delta on the parent operation `GET /reports/measures` as tagged by RWB-P9-E1013-CON: `baselineValue`, the fixing of `dimension` as code and value, and the `X-Data-As-Of` freshness header, on base `/api/recovery/reporting/v1` (DP-13, R4);
- the two fields that RWB-E2-009 section 12 asks for — `dimension` (code and value) and `baselineValue` — both absent from the API Specification that the parent document inherited;
- the increments on `measure_publish` and `measure_snapshot` that the steering key needs — the unique key of one row per business date and the index by measure, date and product — with the field sets of DF-RPT-041 to DF-RPT-058 inherited from the parent and not restated (DP-01, DP-15);
- the declarations of the four consumed operations — the case facts of P3, the agent runs of RWB-P10-E1063-CON, the data-product freshness of P1 and the lists of RWB-P3-E1043-CON — and of the extract hand-over on the rwb-integration queue, each with a fake (DP-07, DP-11, DP-17);
- the subscriptions of the service — EV-01, EV-02, EV-05, EV-08, EV-10, EV-14, EV-15 and EV-28 — with their consumer groups and envelope rules, and no published event of the service's own;
- the registration contract of JOB-15 on queue `rwb-reporting` with its Schedule, so the deployment story registers one name and not two (DP-10);
- the error model and the message map, so a consumer reads one envelope.

This story writes no behaviour. The calculators, the reconciliation and the read are RWB-P9-E2009-APP; the deployment of the build is RWB-P9-E2009-OPS. Where a legacy shape has no target counterpart, the baseline states the placeholder and the gap, and no value is invented (GAP-2577; ASM-4248).

### 2. Business rationale

A split story is only as good as the contract it builds against. RWB-E2-009 was written as one screen reading six in-process interfaces and one data-lake extract; nothing in it can be built by a team that does not own the neighbour. Under D-RCV-60 the facts arrive as events and on narrow contracts with a fake each, and those shapes have to be frozen before the application and the deployment stories open — otherwise the screen, the Power BI report and the run each freeze a different shape of the same measure.

- **one baseline, three consumers.** RWB-P9-E2009-APP, RWB-P9-E2009-OPS and the Power BI report of the Reporting and BI analyst read these shapes; RWB-P9-E1013-CON stays the parent of the measure set and is not restated here.
- **the contract is testable without a neighbour.** Every declaration and every subscription carries a fake with a documented answer, so the contract tests run on Day 1 and SIT only replaces the fake with the owner.
- **nothing of the business is frozen here.** The seven measure codes, their formulas, the tolerance of DL25 and the age bands stay rows of `measure_definition`; the baseline carries their shape, never their value.

### 3. Preconditions

- The ownership rows of the service are taken as authoritative from the context pack: tables `measure_definition`, `measure_publish` and `measure_snapshot` (P9); operations `GET /reports/measures` (P9); events, none (P9); jobs JOB-15 (P9); workflows, none (P9).
- RWB-P9-E1013-CON is published as the parent baseline of the measure set: `measure_definition`, `measure_snapshot`, the `Measure` shape and the `GET /reports/measures` operation. This baseline publishes the delta of the steering key on top of it and does not restate the parent.
- The API Specification, the Event and Messaging Design, the Physical Schema and the LOV set of TSD P9 T3.2 are at their next versions and are the parents of this baseline.
- The platform contracts the patterns name — RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON — are published at their baseline versions.
- RWB-P3-E1043-CON and RWB-P10-E1063-CON are readable as drafts, so their response elements are declared from the published documents and the fakes are built from those declarations.
- Status is Draft (realignment v1): no approval is required to publish a baseline, and a consumer builds against the tagged version (GAP-2577; ASM-4248).
- The steering data set is read in rwb-deviation (S8) as a secondary serving; the canonical measure build and the measure tables stay with rwb-reporting. The seven consumed operations and their owners are published before the contract is tagged, and the load-time edge to P9 is confirmed with the P9 and S8 owners.
- The legacy message IDs and their texts stand in the message map; no new business message text is written here.

### 4. Flow

1. Take the one operation of the ownership row, place it on `/api/recovery/reporting/v1`, and write its filters, its response shape, its errors, its right and its freshness header into 12.1.
2. Add the two fields RWB-E2-009 section 12 asks for — `dimension` and `baselineValue` — to the `Measure` schema as a versioned delta on the parent document, and state where each value comes from.
3. Take the `measure_publish` and `measure_snapshot` field sets of TSD P9 T3.1 as the parent tag fixes them, add the steering key's unique key on the business date and its snapshot index, and state the no-cross-schema-key rule in 12.7.
4. Declare the four consumed operations and the extract hand-over activity with their base, their owner and their request and response elements, and record the placeholder where no published document fixes an element (12.2).
5. Declare the eight subscriptions with their topic, their consumer group and their envelope rule, and state once that the service publishes no domain event of its own (12.3, 12.4).
6. Fix the registration contract of JOB-15 — queue, namespace, workflow type, input schema, Schedule cadence, overlap policy — so the deployment story registers one name (12.5, 12.6).
7. Fix the error model: the platform problem shape, the status of each legacy message of section 14 and the rule that a refused right answers MSG-P4-002 and changes nothing.
8. Publish one fake per declaration and per subscription, each with the documented answer of 12.8, so the contract tests run without a neighbour.
9. Freeze the baseline as version `v1`, tag it and hand the tag to RWB-P9-E2009-APP and RWB-P9-E2009-OPS; any later shape change is a new version and a Change Register row.
10. Run the contract tests of section 16 against the OpenAPI document, the subscription declarations, the schema statement and the fakes, and publish the result with the tag.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A consumer sends a shape the baseline does not declare, or a period whose `from` is after `to` | The request is refused with the problem envelope and no business change | MSG-GEN-003, MSG-P4-002 | AC1, AC5 |
| X2 | A declared operation or activity has no published document behind it and the owner has not confirmed the element names | The declaration carries the placeholder and the fake answers the baseline shape; the review row stays open | None | AC3, GAP-2577 |
| X3 | A breaking change is proposed after the tag | The change opens a new version of the baseline; the tagged version stays buildable | None | AC7 |
| X4 | A fake returns an answer the baseline does not document | The contract test fails and the baseline is not tagged | None | AC6 |
| X5 | A statement of the baseline names another `rwb_*` schema, a `v_ace_*` view or a data-lake object | The schema lint fails and the baseline is not tagged | None (lint log) | AC4, section 17 |
| X6 | A consumer asks for the data lake, INT-19 or an event of this service | No such element is published; the request answers the gap row and the hand-over of 12.2 is the replacement | None | AC2, GAP-2577 |
| X7 | A subscription declaration has no consumer group or no envelope rule | The declaration is not publishable and the tag is refused | None | AC3 |

X2 and X6 are the only paths that end in an open review row; the rest are gates of the tag. No path invents a business value: the values behind the shapes are `measure_definition` rows and reference data of their owners.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs no running neighbour: every declaration and every subscription has a fake, and every shape comes from a published document or the context pack |
| Negotiable | The element names of an unpublished consumed operation and the activity names are the review baseline and may be corrected by the owner without a behaviour change |
| Valuable | The application story, the deployment story and the Power BI report build on Day 1 against one tag |
| Estimable | One operation, one shape delta, two schema increments, four consumed declarations, one activity, eight subscriptions, one registration and eleven fakes |
| Small | Fits in one sprint with its contract tests |
| Testable | Every criterion runs as a contract test at Level Contract against the documents and the fakes |

### 7. Acceptance criteria

```gherkin
Feature: The rwb-reporting contract baseline for the steering dashboard data set

  Background:
    Given service "rwb-reporting" with schema "rwb_reporting", base "/api/recovery/reporting/v1", topic "rwb.reporting.events.v1" and task queue "rwb-reporting"
    Given the ownership rows of the service: tables "measure_definition", "measure_snapshot" and "measure_publish", operation "GET /reports/measures", no event, job JOB-15 and no workflow

  Scenario: AC1 The operation carries the delta of the key with its right and its freshness header (new, D-RCV-60)
    Given the baseline document version "v1" and its parent RWB-P9-E1013-CON
    When a consumer reads the OpenAPI document of the service
    Then "GET /reports/measures" is declared on base "/api/recovery/reporting/v1" with the query parameters measure, product, route, from and to
    Then its response is a list of "Measure" with measure, product, route, period, value, dimension and baselineValue
    Then its header "X-Data-As-Of" carries the business date of the latest published day
    Then it requires the Reporting right R and applies the scope of the role
    Then a period whose from is after to is refused with status 422 and MSG-GEN-003

  Scenario: AC2 The delta on the measure set names its source and freezes no business value (new, D-RCV-60)
    Given the baseline document version "v1" and its parent RWB-P9-E1013-CON
    When the two documents are read together
    Then "dimension" carries the dimension code and the dimension value of LOV-MEASURE-DIM
    Then "baselineValue" names the frozen baseline row of 2026-11-27 as its source and adds no column to "measure_snapshot"
    Then no measure code, formula, unit, age band or tolerance appears as a value in the document, a fake or a test
    Then no element of the data lake, INT-19 or INT-20 is declared

  Scenario: AC3 The consumed declarations and the owner-queue activities are declared with a fake each (new, D-RCV-60)
    Given the baseline document version "v1"
    When a consumer reads section 12.2 and section 12.8
    Then the case facts on "/api/recovery/case/v1", the agent runs on RWB-P10-E1063-CON, the freshness on "/api/recovery/source-data/v1" and the lists on RWB-P3-E1043-CON each name their owner and their request and response elements
    Then the extract hand-over of rwb-integration names its queue and its input and output elements
    Then each declaration has one fake with a documented answer
    Then a declaration whose path or elements no published document fixes carries the placeholder and one review row

  Scenario: AC4 The schema increments are published with the parent's versioning rule (new, D-RCV-60)
    Given the baseline document version "v1" and its parent RWB-P9-E1013-CON
    When the schema statement is read and linted
    Then "measure_publish" inherits DF-RPT-053 to DF-RPT-058 and the standard record columns of TSD P9 T3.0 from the parent
    Then this baseline adds the unique key on "business_date" and the index on "status"
    Then this baseline adds the index on ("measure_code", "business_date", "product_group") to "measure_snapshot"
    Then no foreign key leaves "rwb_reporting" and no statement names another "rwb_*" schema or a "v_ace_*" view
    Then the per-service Flyway sequence, its numbering and its drift gate are declared once

  Scenario: AC5 The subscriptions are declared once and the error model and message map are published (new, D-RCV-60)
    Given the baseline document version "v1"
    When a consumer reads sections 12.3, 12.4 and 14
    Then EV-01, EV-02, EV-05, EV-08, EV-10, EV-14, EV-15 and EV-28 each name a topic, a consumer group and an envelope rule
    Then the service declares no published domain event of its own and the topic "rwb.reporting.events.v1" carries none for this key
    Then the problem envelope is declared once with its fields and its trace identifier
    Then each legacy message ID maps to one HTTP status and one envelope code, and a request without Reporting R answers MSG-P4-002

  Scenario: AC6 Every fake reproduces its documented answer (new, D-RCV-60)
    Given the baseline document version "v1"
    When the contract tests run at Level Contract
    Then each fake returns the answer documented in section 12.8 for its declared scenario
    Then each subscription fixture validates against its declared envelope
    Then a fake that answers outside its documented scenario fails the tag

  Scenario: AC7 A breaking change opens a new version and the tag stays buildable (new, D-RCV-60)
    Given the baseline is tagged "v1"
    When a consumer proposes a change to a published element
    Then the change is published as "v2" with its own document and fake
    Then the tag "v1" remains readable and the stories that cite it still build
    Then the change is recorded in the Change Register

  Scenario: AC8 Each business rule of section 8 is covered by a criterion or a boundary test (new, D-RCV-60)
    Given the baseline document version "v1"
    When the rules BR1 to BR11 of section 8 are read against sections 7 and 16
    Then each rule names the criterion or the test of section 16 that covers it
    Then a rule that is an architecture constraint is covered by a guardrail or boundary test

  Scenario: AC9 The provided operations answer 401, 403 and 404 with the problem envelope (new, D-RCV-60)
    Given the baseline document version "v1"
    When a request arrives without a valid login, without Reporting R or for an unknown resource
    Then the answer is status 401, 403 or 404 respectively
    Then the body carries the problem envelope of AC5

  Scenario: AC10 A retried or timed-out activity follows its declared policy (new, D-RCV-60)
    Given the owner-queue activities are declared with their fakes
    When an activity is retried or exceeds its timeout
    Then the retry and the timeout follow the policy declared for that activity
    Then a timed-out activity is answered with the problem envelope of AC5

  Scenario: AC11 A consumed call that fails or does not answer is reproduced by its fake (new, D-RCV-60)
    Given the consumed declarations of section 12.2 each have one fake
    When a consumed call fails or does not answer
    Then the call returns the failure answer documented in the fake for its declared scenario
    Then the failure is answered with the problem envelope of AC5
```

The eleven criteria test the baseline only. They carry no measure value, count, rate, agent name or business date of the legacy story except the field, list and event names that the context pack and TSD P9 fix; the values behind the shapes stay `measure_definition` rows and reference data (ASM-4248).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The baseline is one tagged version; a consumer builds against the tag and never against a draft element | R8.2; R5.7 rule 1 |
| BR2 | The operation set is the ownership row of the service and nothing else; an operation the context pack does not carry is not published | Context pack; GAP-2577 |
| BR3 | One base per service, `/api/recovery/reporting/v1`, and no operation outside it | DP-13, R4 |
| BR4 | The service publishes no domain event of this key; its only published event is the library's `DecisionRecorded` on the shared topic | DP-03; context pack events row |
| BR5 | One schema and one login per service; no foreign key and no statement may leave `rwb_reporting` | DP-01, DP-02 |
| BR6 | Every consumed operation and every owner-queue activity is declared with a fake; a declaration without a fake is not publishable | DP-11 |
| BR7 | No business value is frozen: measure codes, formulas, units, age bands, the tolerance of DL25 and the LOV values are read from their owners | Principle 1; DP-07 |
| BR8 | No personal data in a schema, an event fixture, a fake or a test | Section 17 |
| BR9 | No element of the data lake, INT-19 or INT-20 is declared; the published day's extract is handed to rwb-integration | DP-17 |
| BR10 | The error envelope is the platform problem shape and every legacy message ID maps to one status and one code | R7.2 s14; section 14 |
| BR11 | A breaking change is a new version and a Change Register row; a correction of an element name by its owner is a patch to the same version | R8.2; AC7 |
| BR12 | The steering dashboard data set and the report reads are served on this service's resources behind the gateway-bff route | GAP-1658 |
| BR13 | The product, route and measure filter lists are read as reference data of rwb-case at their version; no list value is frozen in this baseline | GAP-3090; BR7 |

### 9. State transitions

None of business data: this story changes no record and no publish state. The states it owns are the states of the baseline itself.

| From | Event | Condition | To |
|---|---|---|---|
| Not existing | The baseline is written and its tests pass | The tag gate of section 16 is green | `v1` Draft, tagged and handed to the consumers |
| `v1` Draft | The owner confirms or corrects an element name of a consumed declaration | The change is not breaking | `v1` patched, the review row closed |
| `v1` | A published element changes shape | A consumer cannot build against the old shape | `v2` opened; `v1` stays readable and buildable |
| `v1` | A consumer asks for an element the baseline does not declare | The row is absent, for example the data lake of INT-19 | No change; the request answers the gap row |

The version states are `Draft`, `Tagged` and `Superseded`, and only a tagged version is citable by an APP or OPS story.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| The contract owner of rwb-reporting (TechX) | Writes, tags and versions the baseline; owns the fakes and the contract tests; refuses a declaration without a published document |
| The owner of rwb-case (P3) | Confirms or corrects the case-list declaration, the reference-data lists and their fakes |
| The owner of rwb-agent (P10) | Confirms or corrects the agent-run declaration behind RWB-P10-E1063-CON and its fake |
| The owner of rwb-source-data (P1) | Confirms the freshness declaration and its fake |
| The owner of rwb-integration (P2) | Confirms the extract hand-over declaration, its queue and the file shape |
| The owner of rwb-decision (P7) | Confirms the eight subscription declarations and the shared topic `rwb.decision-record.v1` |
| The platform contract owners (PLT) | Own the shapes the baseline inherits: the record, the workflow kit, the reference-data client, the Flyway gate and the composite route |
| RW-BIANAL, RW-TRIBE, RW-PRODHEAD, RW-TEAMMGR, RW-DATASTEW | Read the baseline as consumers; hold no write right on it |

The right of the published operation is the row of TSD P9 T6.1; the baseline declares it and grants nothing.

Every REST operation is authorised through rwb-access (DP-08); the name of the authorise check is Not specified in the source documents (DOR-RWB-P9-E2009-CON-6).

Open decision DL25 (the tolerance of BR7) is still open; its assumptions ASM-0728, ASM-0735, ASM-0743 and ASM-2602 are recorded as confirmed, and the baseline freezes no tolerance value.

### 11. Data

| BR Field ID | Entity (owner) | Field | Declared as |
|---|---|---|---|
| DF-RPT-031 to DF-RPT-040 | `measure_definition` (P9) | id, measure_code, name, formula, data_product, unit, definition_version, approved_by, approved_at, valid_from | inherited from RWB-P9-E1013-CON; read by the operation |
| DF-RPT-041 to DF-RPT-052 | `measure_snapshot` (P9) | id, measure_code, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, is_baseline, frozen, published_at | inherited; `dimension_code` and `dimension_value` are the source of the `dimension` field of AC2 |
| DF-RPT-053 | `measure_publish` (P9) | id | required, uuid |
| DF-RPT-054 | `measure_publish` (P9) | business_date | required, unique across the table |
| DF-RPT-055 | `measure_publish` (P9) | status | required, from LOV-MEASURE-PUBLISH |
| DF-RPT-056 | `measure_publish` (P9) | case_list_count | required |
| DF-RPT-057 | `measure_publish` (P9) | dashboard_count | required |
| DF-RPT-058 | `measure_publish` (P9) | held_reason | optional, the reason a day was held |
| DF-CAS-001, DF-CAS-003, DF-CAS-006, DF-CAS-008, DF-CAS-010, DF-CAS-013 | `recovery_case` (P3) | case id, product group, stage, route, queue and entry date | response elements of the case-list declaration (element names: Not specified in the source documents (GAP-2577)); never a table read |
| DF-DEC-007, DF-DEC-012, DF-DEC-013 | `decision_log_entry` (P7) | agent_version, final_call, override_reason | envelope elements of EV-08 and EV-28 |

The field IDs are those of the Logical Data Model and Data Dictionary and of TSD P9 T3.1. The column sets of the three tables are those of the parent tag RWB-P9-E1013-CON; this baseline declares only the uniqueness of `business_date`, the two indexes and the shape delta, and adds no column. The legacy story asks for a `baselineValue` on the `Measure` schema; no column carries it, so it is derived from the frozen baseline rows of 2026-11-27 and the derivation is part of the declared shape, not a new column (GAP-2577; ASM-4248). No element of a payload is invented beyond the legacy lists and the envelope fields. The nine fact tables are the read model in rwb_reporting, fed from the service topics; no data lake or Power BI connection is declared (BR9). Read-model controls: measure_definition, measure_snapshot and measure_publish are owned by P9, and the publish gate holds a day whose dashboard count differs from the case-list count, the reason recorded in held_reason (DF-RPT-058); queue measures stay with P3 rwb_case and are not published here. The owner and team are keyed by ID from the events; the display name resolves behind the rwb-access masking policy, and no personal data travels on an event (BR8). The steering dashboard data set is read as this service's dashboard and measure resources through gateway-bff (GAP-1662). The wave 1 measures read GET /reports/measures is the declared operation for the harness and the catalogue; the dashboard, its filters and SCR-37 stay with RWB-P9-E2009-APP, and the connection of any reporting client to the read is an open decision for the PRD step (GAP-2570). The INT-19 extract is dropped from this slice; the freshness stamp stays on the answer for the screen refresh (schedule time Not specified in the source documents (GAP-3090)), and the Power BI data set becomes the rwb-reporting read model built from events, confirmed with the reporting owner before the wave 2 entry check (GAP-3088). The case-fact read shape and cut-off rule are Not specified in the source documents (GAP-0731); the consumed case, decision, treatment, notice and agent-run operations and the freshness check take their names, paths, payloads and errors from their owners at review, with Not specified in the source documents (GAP-2576). The agent acceptance and override rates take their basis from EV-28 and RWB-P10-E1063-CON (GAP-2576). Unsettled element names of the consumed declarations and the two owner-queue activities carry the placeholder Not specified in the source documents (GAP-2577), with one review row, and the release is gated on the contract tests and the schema lint. The gateway-bff composite steering route path and merge order, the harness repository and SIT environment, the seeded measure day, the evidence format and retention and the pass/fail gate are Not specified in the source documents (GAP-0391) and are agreed at the wave 2 entry check.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1` (DP-13); document `openapi/rwb-reporting-v1.yaml`, an increment on the document tagged by RWB-P9-E1013-CON. The operation, its filters and its access row belong to the parent; this baseline publishes the delta of the steering key and restates nothing else.

| Method | Path | Request | Response | Errors | Access | Idempotency |
|---|---|---|---|---|---|---|
| GET | `/reports/measures` | query `measure`, `product`, `route`, `from`, `to` (dates, `from` on or before `to`) | 200 `Measure[]`: measure, product, route, period, value, dimension (code and value), baselineValue; header `X-Data-As-Of` | 401, 403 (MSG-P4-002), 422 (MSG-GEN-003), 503 (MSG-GEN-006) | Reporting, right R, scope applied | Not applicable |

The delta is `baselineValue`; `dimension` is declared here as a code and a value of LOV-MEASURE-DIM, which the parent already carries as two properties, and the `X-Data-As-Of` header stays as the parent declares it (RWB-E2-009 section 12). The legacy path `monolith-base/reports/measures` moves to the per-service base and keeps its operation path. No second operation is published: a rerun of a business date is a workflow-level action of RWB-PLT-E1071-CON and not an operation of this service (GAP-2577; ASM-4248).

#### 12.2 REST operations consumed

| Operation | Base | Owner | Request | Response elements |
|---|---|---|---|---|
| The case facts of a business date (the read RWB-P3-E1013-APP declares) | `/api/recovery/case/v1` | P3 rwb-case | asOf, page | one row per case with product group, route, stage, queue, entry date, status and closed date, with the as-of time and the row count |
| The runs of an agent and version for a business date (name as above) | RWB-P10-E1063-CON | P10 rwb-agent | businessDate, agent, version | run count, accepted, overridden, latency, cost, version |
| The lists of the measures (name as above) | RWB-P3-E1043-CON | P3 rwb-case | listCode, businessDate | the active values of LOV-PRODUCT, LOV-MEASURE-UNIT, LOV-MEASURE-DIM, LOV-DATA-PRODUCT and LOV-MEASURE-PUBLISH |
| The freshness of the data products of a business date (the read RWB-P1-E1013-APP declares) | `/api/recovery/source-data/v1` | P1 rwb-source-data | asOf, product | the product, its business date and its freshness stamp |
| The extract hand-over of a published day (name and file shape as above) | activity on the queue `rwb-integration` | P2 rwb-integration | businessDate, row set, freshness stamp | accepted, delivery reference |

Every REST row is one hop with a 2 s timeout, a single GET retry with jitter and a breaker per downstream (DP-11, ADR-020). The hand-over replaces INT-19, the data lake load area, which no longer exists; the file shape Power BI reads is fixed by no source and is the review row of AC3 (DP-17).

#### 12.3 Events published

None of the service's own. The ownership row of the service carries no event, so no schema is published on `rwb.reporting.events.v1`; the topic, its `.retry` and its `.dlt` are provisioned for the service's own lifecycle messages and carry nothing for this key. The one event this service writes is the local library's `DecisionRecorded` (EV-08) on the shared topic `rwb.decision-record.v1`, whose owner is rwb-decision and whose schema is inherited and not restated (DP-03).

#### 12.4 Events consumed

| Event | Topic | Consumer group | Envelope rule | Declaration | Owning service |
|---|---|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | dedupe on the event id; order per case by the outbox sequence | caseId, caseNo, productGroup, accounts, businessDate | rwb-case (P3) |
| `rwb.case.CaseAllocated.v1` (EV-02) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | as above | caseId, queueId, ownerId, ruleId, ruleVersion | rwb-case (P3) |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | `rwb-reporting.case.v1` | as above | caseId, fromState, toState, ruleId, decisionLogEntryId | rwb-case (P3) |
| `rwb.decision.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | `rwb-reporting.decision.v1` | dedupe on the entry id | entryId, caseId, decisionCode, approver | Not specified in the source documents (DOR-RWB-P9-E2009-CON-24) |
| `rwb.treatment.TreatmentApproved.v1` (EV-10) | `rwb.treatment.events.v1` | `rwb-reporting.treatment.v1` | dedupe on the event id | treatmentId, caseId, terms | Not specified in the source documents (DOR-RWB-P9-E2009-CON-24) |
| `rwb.comms.NoticeDispatched.v1` (EV-14) | `rwb.comms.events.v1` | `rwb-reporting.notice.v1` | dedupe on the notice id and the dispatch | noticeId, barcode, sentDate | Not specified in the source documents (DOR-RWB-P9-E2009-CON-24) |
| `rwb.comms.NoticeDelivered.v1` (EV-15) | `rwb.comms.events.v1` | `rwb-reporting.notice.v1` | dedupe on the notice id and the delivery | noticeId, deliveredAt, status | Not specified in the source documents (DOR-RWB-P9-E2009-CON-24) |
| `rwb.agent.AgentRunCompleted.v1` (EV-28) | `rwb.agent.events.v1` | `rwb-reporting.agent.v1` | dedupe on the run id | runId, agent, caseId, outcome, fallback | rwb-agent (P10) |

The payload lists are the legacy lists of the Event and Messaging Design v4 and the envelope fields; the envelope elements, the subject and the schema registry naming of each subscription are Not specified in the source documents (GAP-2577; ASM-4248). The eight rows are the service's subscriptions per the connection matrix, which lists rwb-reporting as a listener of P3, S2, P6 and P10 and as a Temporal caller of P1 and P2.

#### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15; name Not specified in the source documents (GAP-2577; ASM-4248)) | Workflow, started by its Schedule | `rwb-reporting`, namespace `rwb-recovery` | input businessDate; execution id derived from the business date; retry policy of the kit |
| `checkFreshness`, `loadReadModel`, `loadAgentFacts`, `computeMeasures`, `reconcileCounts`, `publishDay` | Activities | `rwb-reporting` | the input and output element names of the components of RWB-P9-E2009-APP section 13; the retry policy of the kit |

The baseline fixes the registration contract — queue, namespace, workflow type, input schema, retry policy and the name of the Schedule — and not the internal steps a story chooses. The names are the design baseline of the split (ASM-4244).

#### 12.6 Schedules

| Schedule | Workflow | Queue | Cadence | Overlap and catch-up |
|---|---|---|---|---|
| `reportingMeasuresDaily` (JOB-15) | `reportingMeasuresDaily` for the previous business date | `rwb-reporting` | 01:30 each business day, replacing the Quartz row of the legacy story (DP-10) | one execution per business date; overlap skipped; catch-up of a missed date one by one |

The baseline declares the name, the cadence and the overlap rule; the catch-up window and the time zone are values of the environment and are declared here as the review baseline (GAP-2577; ASM-4248). No other Schedule belongs to this key.

#### 12.7 Tables owned

| Table | Owner | Key, index and delta | Columns | Note |
|---|---|---|---|---|
| `measure_publish` | P9 (`rwb_reporting`) | the parent's primary key; this key adds the unique key on `business_date` and the index on `status` | DF-RPT-053 to DF-RPT-058, inherited from the parent tag | the publish state of a business date, with both counts |
| `measure_snapshot` | P9 (`rwb_reporting`) | the parent's key; this key adds the index on (measure_code, business_date, product_group) | DF-RPT-041 to DF-RPT-052, inherited | the baseline rows of 2026-11-27 stay frozen and are read, never rewritten |
| `measure_definition` | P9 (`rwb_reporting`) | inherited from the parent | DF-RPT-031 to DF-RPT-040, inherited | read only for this key |
| `decision_record` | PLT library, created in `rwb_reporting` | hash chain per record kind, inherited | inherited | DP-03 |

The baseline declares no foreign key out of `rwb_reporting`, no grant on another schema, no read of another owner's table and no read of a `v_ace_*` view (DP-01, DP-17). The migration rule is one Flyway sequence per service, numbered in `rwb_reporting` after the parent's `V1013__measures.sql` and gated by the lint and drift gate of RWB-PLT-E1044-CON (DP-15); the monolith's `V2_009__measure_publish.sql` is not reused and its target name is Not specified in the source documents (GAP-2577; ASM-4248).

#### 12.8 Contract fakes

| Fake | Provider | Documented answer | Consumers |
|---|---|---|---|
| Reporting OpenAPI fake | rwb-reporting | the seven measures of a day with dimension and baselineValue, `X-Data-As-Of`, a 422 on a reversed period and a 403 without Reporting R | APP, OPS, gateway-bff |
| Subscription fixtures | rwb-reporting | one valid and one invalid sample per event of 12.4, with the synthetic day of AC1 to AC4 | APP, OPS |
| Case-list fake | P3 | 240 open cases at a cut-off, 140 Mortgage cases and a count of 239 for the mismatch path | APP |
| Agent-run fake | P10 (RWB-P10-E1063-CON) | 200 recommendations with 170 accepted and 30 overridden for one agent and version, and an agent with no run | APP |
| Reference-data and record fakes | P3 and PLT | the five lists with one version, and the record chain healthy and stopped | APP |
| Source-data freshness fake | P1 | a fresh and a stale data product for a business date | APP, OPS |
| Integration hand-over fake | P2 | an accepted extract with its freshness stamp and a refused hand-over | APP, OPS |
| gateway-bff route fake | PLT edge | the merged SCR-37 answer with the measures read once | APP, OPS |

Each fake is generated from its document under `contracts/fakes/`, is versioned with the baseline and is replaced by the owner in SIT without a change to a consumer. The five declaration names of 12.2 carry the placeholder until their owners confirm them (GAP-2577; ASM-4248).

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 4 consumed | `GET /reports/measures` on `/api/recovery/reporting/v1`; the case facts, the agent runs, the freshness and the reference-data lists; one hop, 2 s |
| Kafka | none published, 8 subscribed | no schema of this key on `rwb.reporting.events.v1`; the library's `DecisionRecorded` on `rwb.decision-record.v1`; EV-01, EV-02, EV-05, EV-08, EV-10, EV-14, EV-15 and EV-28 consumed |
| Temporal | 1 workflow registered, 6 activities, 1 Schedule | `reportingMeasuresDaily` on `rwb-reporting`; the P1 and P2 activities on their owners' queues |
| File | 1 out | the published day's extract, handed to rwb-integration; no file is read by this key |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting`, module `contract`; artefacts under `contracts/rwb-reporting/`: `openapi-v1.yaml`, `consumed.yaml`, `subscriptions.yaml`, `schema/rwb_reporting_steering.sql`, `messages.yaml`, `fakes/*.json`.

| Component | Type | Responsibility |
|---|---|---|
| `openapi-v1.yaml` | Document | the operation, its parameters, its `Measure` delta, its header, its errors and its examples |
| `consumed.yaml` | Document | the three declarations and the two owner-queue activities, with their owners and their review state |
| `subscriptions.yaml` | Document | the eight subscriptions, their consumer groups and their envelope rules |
| `schema/rwb_reporting_steering.sql` | Document | the `measure_publish` baseline and the snapshot index, with their keys and their no-cross-schema rule |
| `messages.yaml` | Document | the message map of section 14 |
| `fakes/` | Generator | one fake per declaration and per subscription, generated from the documents and versioned with them |
| `ContractTag` | Build step | tags the baseline and publishes the tag to the two consumer stories |

**Build steps.** (1) Write the OpenAPI increment and lint it; test AC1 and AC2. (2) Write the four declarations and the hand-over contract, and generate the fakes; test AC3. (3) Write the schema statement and pass the schema lint; test AC4. (4) Write the eight subscriptions and the message map; test AC5. (5) Run the contract tests, tag `v1` and publish the tag; test AC6 and AC7.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` | owner's schema `rwb_reporting`; no foreign key leaves it | none |
| DP-03 | DecisionLogWriter | the local record library and `rwb.decision-record.v1`, inherited shape | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | the five lists declared on the reference-data contract | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-15 | the registration contract of a Scheduled workflow | H RWB-PLT-E1071-CON |
| DP-11 | In-process call | one hop, 2 s, a fake per declaration | none |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1` | none |
| DP-15 | V0001 baseline | one Flyway sequence per service | H RWB-PLT-E1044-CON |
| DP-17 | Data lake, INT-19 | no lake; the extract is handed to rwb-integration | none; the file shape is a gap |
| DP-19 | Screen, ace-web | the composite route the read is served through | H RWB-PLT-N001-CON |

### 14. Validation and messages

| ID | When | Status and code | English text |
|---|---|---|---|
| MSG-P9-002 | The dashboard count differs from the case list | 409 on a replayed publish; the run and screen text names both counts and the date | Not specified in the source documents (DOR-RWB-P9-E2009-CON-9) |
| MSG-P1-001 | A source is stale | 503 on a read of stale data; the text carries the product and the date | Not specified in the source documents (DOR-RWB-P9-E2009-CON-9) |
| MSG-GEN-003 | Dates in the wrong order | 422 with the two field names and no value | Not specified in the source documents (DOR-RWB-P9-E2009-CON-9) |
| MSG-P4-002 | The role lacks Reporting R | 403 on the operation; nothing changes | Not specified in the source documents (DOR-RWB-P9-E2009-CON-9) |
| MSG-GEN-006 | A named system is unavailable | 503 with the system name only | Not specified in the source documents (DOR-RWB-P9-E2009-CON-9) |
| MSG-P7-003 | The local record cannot be written | 500 on the operation; the run text says nothing was changed | Not specified in the source documents (DOR-RWB-P9-E2009-CON-9) |

The envelope of every error is the platform problem shape — `type`, `title`, `status`, `detail`, `instance` and `traceId` — and carries no personal data. The texts are the legacy texts of RWB-E2-009 section 14 and of the platform, and are copied into the message map unchanged.

### 15. Screens and states

SCR-37 Steering dashboard is the only screen this key serves. The baseline declares the read that fills it — `GET /reports/measures` with the product, route and period filters and the `X-Data-As-Of` header — and the composite route the screen calls through the gateway-bff (DP-19). SCR-44 shows the run from the workflow visibility query. No other screen is served by this key.

SCR-37 states: loading as stated in Screen Specifications v1 section SCR-37; empty, error and no access are Not specified in the source documents (CG-ALL-7859).

SCR-44 states: empty, loading, error and no access are Not specified in the source documents (CG-ALL-7860).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P9-E2009-CON-01 | AC1 | Contract | the OpenAPI increment read against the ownership row of the operation |
| TC-P9-E2009-CON-02 | AC1, AC5 | Contract | a reversed period, a request without Reporting R and a request with an undeclared parameter |
| TC-P9-E2009-CON-03 | AC2 | Contract | the parent document RWB-P9-E1013-CON and the delta read together |
| TC-P9-E2009-CON-04 | AC3, AC6 | Contract | the five declarations and their generated fakes |
| TC-P9-E2009-CON-05 | AC4 | Contract | the schema statement linted for keys, indexes and cross-schema names |
| TC-P9-E2009-CON-06 | AC5 | Contract | the eight subscriptions, their groups and their envelope rules |
| TC-P9-E2009-CON-07 | AC5 | Contract | each of the six messages mapped to its status and code |
| TC-P9-E2009-CON-08 | AC6, AC7 | Contract | the tag `v1`, a proposed breaking change and the tag `v2` |
| TC-P9-E2009-CON-09 | AC4 | Contract | the unique key on business_date of measure_publish and the index on (measure_code, business_date, product_group) of measure_snapshot, each tested at its boundary |
| TC-P9-E2009-CON-10 | AC8 | Contract | BR1 to BR11 of section 8 read against sections 7 and 16 |
| TC-P9-E2009-CON-11 | AC9 | Contract | the 401, 403 and 404 answers of the provided operations |
| TC-P9-E2009-CON-12 | AC10 | Contract | a retried activity and a timed-out activity |
| TC-P9-E2009-CON-13 | AC11 | Contract | a consumed call that fails and a consumed call that does not answer |

The eight are new with D-RCV-60 and test the baseline only. Integration copies end in `-ITG` and belong to RWB-ITG-E2009-ITG; the ten legacy test cases of RWB-E2-009 stay with the criteria the APP story owns.

### 17. Guardrails

- No business value in a document, a schema, a fake or a test: the measure codes, formulas, units, age bands, the tolerance of DL25 and the LOV values are rows of their owners and appear here only as element names.
- No personal data in a schema, an event fixture or a log: a measure carries counts, rates, amounts and codes; an agent run carries an agent, a version and an outcome.
- No statement leaves `rwb_reporting`, no element of the data lake is declared, and no `v_ace_*` view is named.
- No declaration without a fake, no subscription without a consumer group and an envelope rule, no tag without the contract tests.
- The six message texts are copied, never reworded; a new text needs its owner.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-WKM-009 | Steering dashboard reports volume, ageing, route mix, turnaround and recovery against the baseline | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-OCC-12, FEAT-RPT-03, FEAT-RPT-08 | 15 Manage performance, data and AI | None; NFR-065 and NFR-066 apply | TC-P9-E2009-CON-01, TC-P9-E2009-CON-03, TC-P9-E2009-CON-06 |
| REQ-WKM-006 | Queue counts and ageing reported daily and reconciled to the case list | Business Requirements Epic 2, sections 3.9 and 4 | FEAT-RPT-08 | 15 Manage performance, data and AI | None; DL25 applies | TC-P9-E2009-CON-02, TC-P9-E2009-CON-04, TC-P9-E2009-CON-05, TC-P9-E2009-CON-07, TC-P9-E2009-CON-08, TC-P9-E2009-CON-09 |

The baseline is cited by RWB-P9-E2009-APP, RWB-P9-E2009-OPS and the Power BI report; each citation names the tag `v1`. The parent baseline RWB-P9-E1013-CON keeps the rows of the measure set, and none is restated here.



### 19. Out of scope

- The calculators, the reconciliation, the read and the run (RWB-P9-E2009-APP).
- The deployment, the topics, the consumer groups, the alerts and the runbook (RWB-P9-E2009-OPS).
- The measure set, `measure_definition`, `measure_snapshot` and the `Measure` shape of RWB-E1-013 (RWB-P9-E1013-CON and RWB-P9-E1013-APP).
- The queue and service-level measures of RWB-E1-030 and RWB-E2-011, the agent monitoring dashboard of RWB-E2-031, benefit realisation of FEAT-RPT-06 and the regulatory returns of FEAT-RPT-07.
- The platform shapes this baseline inherits — the record library, the workflow kit, the reference-data client, the Flyway gate and the composite route — which are owned by their PLT stories.
