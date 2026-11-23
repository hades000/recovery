# RWB-P9-E8002-APP Classify, stage and re-age an account

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P9-E8002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-reporting |
| Service epic | RWB-SVC-P9 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 June 2027 (tentative) |
| Legacy key | RWB-E8-002 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP03, DP13, DP19 |
| Parallel lane | L-P9-F |
| Ready to start | Day 1 |
| Depends on (build) | RWB-P9-E8002-CON, RWB-PLT-E1027-CON, RWB-PLT-N001-CON |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P9 rwb-reporting v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

| Version | Date | Change | Tool |
|---|---|---|---|
| v1 | 22 November 2026 | D-RCV-60 realignment of RWB-E8-002 into rwb-reporting, app slice | T3 Code / OpenCode / DeepSeek v4.1 Flash |

### 1. Story

As a **risk and model risk officer**, I want **the rwb-reporting classification and re-ageing step that applies the rule version in force to every open account, recomputes the reported stage, route and age band when the rule version or an upstream reclassification changes, and writes one local decision record with the rule version**, so that **the measures come from the decision log instead of a hand count, and a segment that changed is reported with the version that produced it**.

The service owns the measure definitions, the snapshot rows and the publish row. The case facts arrive on events, the rule version arrives on the rwb-decision read, and the result lands in the `measure_snapshot` dimension rows and in the local decision record. Nothing of another service is read as a table.

- base `/api/recovery/reporting/v1`, schema `rwb_reporting`, topic `rwb.reporting.events.v1`, queue `rwb-reporting` in namespace `rwb-recovery`, package `th.co.scb.ace.workbench.recovery.reporting` (DP-13);
- the reported classification of an open account is its stage, its route and its age band under the rule version in force (FSD P9 A2.10, BR-P9-010);
- the record of each change is one entry of the local decision-record library on `rwb.decision-record.v1`, written before the rows it explains (DP-03);
- the re-aged values are the STAGE, AGE_BAND and ROUTE dimension rows that the one measure read of the service already returns, read on SCR-37 through the gateway-bff composite route (DP-19).

Not here: the published declarations and the fakes (RWB-P9-E8002-CON); the case-side recompute of the segment, the route reopen and the gate re-run of rule R-UNI-22, which stay with rwb-case; the measure set, the steering data set and the benefit tracking of the same service; the regulatory returns of FEAT-RPT-07.

### 2. Business rationale

Measures are counted by hand from spreadsheets at month end (FSD P9 A1.3), and the count only reconciles when every account sits in the stage and the age band the rule version actually puts it in. TSD P9 NFR-065 requires the business measures per decision to be produced from the decision log and not from a separate count, and the legacy story already says the measures come from the decision log. This story makes the classification a versioned, recorded fact: the reported rows carry the definition version in force, and one decision record per changed account carries the rule id and the rule version that moved it.

In the microservice layout the reported classification is not a new store. The service already owns the dimension columns of `measure_snapshot` (DF-RPT-046, DF-RPT-047) and the lists LOV-MEASURE-DIM and LOV-MEASURE-UNIT, so the re-age writes rows into the table the measures already read and invents no measure code, no table and no column. The value is read on the per-service base (DP-13) and reached through the gateway-bff composite route (DP-19); the change leaves through the local library on `rwb.decision-record.v1` (DP-03), which is what makes AC1 traceable to its rule version.

Two conflicts are recorded rather than smoothed over. Rule R-UNI-22 assigns "recompute the segment, re-run the gates" to the Workbench, while the legacy story sits in module P9 Reporting; this story reports the re-aged classification and leaves the case-side recompute where the rule puts it (GAP-2586; ASM-4281). And the legacy integration points "ALS and GL, Workbench" describe in-process and upstream calls that a service may not make; the facts arrive on events and the upstream re-age has no event name in the sources (GAP-2585; ASM-4277).

### 3. Preconditions

- RWB-P9-E8002-CON is tagged `v1`: the one measure read with the re-aged dimension values, the four subscriptions with their consumer groups, the record element, the rule-version read and the fakes.
- A rule version of the classification and re-ageing rules is in force for the business date, with its rule rows, its stage set and its age bands; the version is a data row of its owner and never a constant (BR-P9-010).
- The case facts of the business date are on the service's read model from `rwb.case.CaseCreated.v1` (EV-01) and `rwb.case.CaseStateChanged.v1` (EV-05), which the baseline declares.
- The measures that carry a STAGE, an AGE_BAND or a ROUTE dimension are defined in `measure_definition` by the baseline measure set of RWB-E1-013; this story adds no measure code.
- The two platform contracts are available: RWB-PLT-E1027-CON (local decision record) and RWB-PLT-N001-CON (gateway-bff composite route).
- The publish row of the business date states whether the day is PUBLISHED or HELD, and the frozen baseline rows of the measure set are never rewritten.
- The caller holds Reporting R (RW-RISK, RW-BIANAL, RW-DATASTEW and the other roles of TSD P9 T6.1), or the step runs under the service identity; scope is applied to the read.
- Values that no source fixes: the name and payload of the upstream reclassification event, the member names of the rule-version read, the step name inside JOB-15 and the decision reference of the record are Not specified in the source documents (GAP-2585; ASM-4277).
- Status is Draft (realignment v1): no approval is required to build against the tag (GAP-2585; ASM-4282).

### 4. Flow

1. The classification step of the daily reporting run JOB-15 (step name Not specified in the source documents (GAP-2585; ASM-4279)) opens for the business date before the measure rows of the day are published.
2. During the day the same routine re-ages one account at once when a case state changes (EV-05) or when the upstream re-age fact arrives; the triggered path and the daily path share one component and one transaction shape.
3. System: resolves the rule version in force on the business date on the rwb-decision read — rule id, version, valid-from date, the stage set and the age bands — and stops the step where no version is in force (MSG-P3-027).
4. System: for each open account, derives the reported stage, route and age band from the case facts of the read model and the rule rows. No band, threshold, stage code or route code is written in code (BR1).
5. System: compares the derived classification with the last reported one; an account whose stage, route or age band is unchanged gets no new row and no record.
6. System: writes one local decision record per changed account through the library — FEAT-RPT-10 as the decision reference, the rule id, the rule version, the from stage, the to stage, the age band and the business date — in the same transaction as the rows it explains (DP-03).
7. System: writes the STAGE, AGE_BAND and ROUTE dimension rows of `measure_snapshot` for the business date, the product group and the definition version in force, with `value` and `case_count`.
8. System: applies the published guard of BR5 — a day that is PUBLISHED in `measure_publish` or frozen in the baseline set is never rewritten, and the change is written for the next unpublished business date with both dates in the record.
9. System: a repeat of the same event id, the same account and the same rule version writes the same rows and one record, and the inbox marks the second delivery as seen.
10. System: `GET /reports/measures` returns the re-aged dimension values of the period under the per-service base, and the gateway-bff composite route serves them on SCR-37 (DP-13, DP-19).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | No classification rule version is in force on the business date | Nothing is recomputed and nothing is recorded; the run record names the version check | MSG-P3-027 | AC1 |
| X2 | The rule-version read of rwb-decision does not answer inside 2 s, or its breaker is open | The step stops; the reported rows of the date stay as they were; the next run retries | MSG-GEN-006 | AC1 |
| X3 | The local decision record cannot be written | No row is written and nothing else changes; the account keeps its last reported classification; an incident is raised | MSG-P7-003 | AC2 |
| X4 | A case fact carries no entry date, so no age band can be derived | The account is skipped and named; every other account of the day proceeds | MSG-GEN-001 | AC1 |
| X5 | The business date is already PUBLISHED or frozen | No row is rewritten; the change is written for the next unpublished business date and the record names both dates | None | AC1 |
| X6 | A data product behind the case facts is stale for the business date | The reported rows keep their own business date and show it as stale | MSG-P1-001 | AC1 |
| X7 | The caller lacks Reporting R on the read, or lacks the step's service right | 403 with the refusal; nothing changes | MSG-P4-002 | TC-E8-002-03 |
| X8 | A component, a statement or a test reaches another `rwb_*` schema or a `v_ace_*` view | The grant refuses the statement and the boundary test fails the build | None (pipeline log) | Section 17 |

X1 to X4 are the paths the legacy exception flows and FSD P9 A2.10 describe carried onto the split; X5 to X8 are the paths the microservice adds.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against RWB-P9-E8002-CON and its fakes with the two platform contracts as build dependencies; the rwb-decision rule read is a client with a fake and adds no build block |
| Negotiable | The step name, the component names and the record's decision reference are this story's choice; the rule version, the stages, the age bands and the measure codes are data of their owners |
| Valuable | A segment that changed is reported with the version that moved it, and a hand count can no longer disagree with the stage and age band of record |
| Estimable | One service, one step, one event path, one read, one record element, one write into existing columns and eight exception paths |
| Small | Fits one sprint with the contract fakes |
| Testable | Every criterion is a component or contract test over a synthetic day of events and a fixed rule version |

### 7. Acceptance criteria

```gherkin
Feature: Classify, stage and re-age an account

  Background:
    Given the base of rwb-reporting is /api/recovery/reporting/v1 and its schema is rwb_reporting
    Given the measures with a STAGE, an AGE_BAND and a ROUTE dimension are defined with a definition version in force

  Scenario: AC1 Classify, stage and re-age an account (legacy RWB-E8-002 AC1)
    Given the data and the rule version this feature needs are in place
    Given the rwb-decision contract mock returns the classification rule rows and the rule version in force for the business date
    When its trigger arrives
    Then applies the classification and re-ageing rules and recomputes the segment when they change
    Then the system writes the result to the decision log with the rule version

  Scenario: AC2 Not recorded (legacy RWB-E8-002 AC2)
    Given the decision log cannot be written
    Given the local decision-record stub returns a refused write with MSG-P7-003
    When the action is taken
    Then nothing changes and the user sees MSG-P7-003
```

AC1 and AC2 are the criteria of RWB-E8-002 and this story owns both; they are copied verbatim and each gains one inserted Given, so the part the story does not own is asserted against a fake, with every legacy word kept. The evidence that AC1 produced a classification and not a screen is the `measure_snapshot` STAGE, AGE_BAND and ROUTE rows of the business date beside the decision record that names the rule version, and the evidence that AC2 changed nothing is an unchanged row set with the refusal returned. The rule rows and the version are read on the rwb-decision declaration of section 12.2; where no published document fixes a member name, the baseline carries the placeholder (GAP-2585; ASM-4277).

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No value a business person may change is written in code; the stages, routes, age bands and their thresholds are read from the rule version in force | BR-P9-010 |
| BR2 | The reported classification of an open account is its stage, its route and its age band under the rule version of the business date | FSD P9 A2.10; R-UNI-22 |
| BR3 | A reclassification or a new rule version recomputes the reported classification of every affected open account before the day's measure rows are published | R-UNI-22; R-UNI-38 |
| BR4 | A decision taken under a version keeps that version; a recompute applies the new version from its valid-from date only | R-UNI-38 |
| BR5 | A day that is PUBLISHED or frozen is never rewritten; a late change is written for the next unpublished business date and the record names both dates | DF-RPT-051; RWB-E1-013 baseline rule |
| BR6 | Each changed account has one local record carrying the rule id and the rule version before its row changes; a failed record changes nothing | Legacy AC1 and AC2; R-UNI-39; DP-03 |
| BR7 | A data product stale after a late or failed ACE batch shows its own date and is never presented as the business date | VR-P9-010-1; MSG-P1-001 |
| BR8 | This service reads and writes only `rwb_reporting`; the case facts arrive on events and the rule version on the owner's read | DP-01; Ownership Map |
| BR9 | No personal data enters a snapshot row, an event, a workflow input or a log: account and case references, codes, dates and counts only | Guardrail 2 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| No row for the business date | EV-01, EV-05 or the upstream re-age fact | The account is open and its entry date is on or before the date | A STAGE, an AGE_BAND and a ROUTE row under the version in force, with one record |
| Rows under version A | EV-30 RulePackageInForce, or a reclassification fact | The new valid-from date is on or before the business date | The rows rewritten under version B for the same date, with one record naming A and B |
| Rows present | The same trigger replayed | The event id, the account and the version repeat | Unchanged; the same rows and no second record |
| Rows of a PUBLISHED or frozen day | A late reclassification | BR5 applies | No rewrite; new rows for the next unpublished business date, with both dates in the record |
| Any | The local record cannot be written | The chain is stopped | No change at all; MSG-P7-003 |

The lifecycle states of a row are those of the standard record columns (`state`, `is_active`, `version`) of TSD P9 T3.0 and the `published_at` column; the publish states of the day are PUBLISHED and HELD of LOV-MEASURE-PUBLISH and stay with the measure stories. No case state moves in this story: the state machine of a case is rwb-case's (TSD P9 T4).

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-RISK, risk and model risk officer | Reads the re-aged classification and the record of a date in scope (Reporting R); the role the legacy story names |
| RW-BIANAL, reporting and BI analyst | Reads the reported rows and the record, and reruns a date from the visibility view (Reporting R, CRUD on the measure set) |
| RW-DATASTEW, data steward and data product owner | Reads the reported classification and its rule version (Reporting CRU); owns the measure definitions, not the classification |
| RW-TRIBE, Tribe lead and squad members | Reads the reported classification on SCR-37 (Reporting R) |
| RW-AUDIT, internal audit | Reads the record of a date and the rule version that produced it (Reporting R) |
| Service identity of rwb-reporting | Runs the step, writes the rows and the record; holds no grant on another schema |
| Owner of rwb-decision (P7) | Owns the rule rows and the rule version this story reads; confirms the member names of the read |
| Platform team | Owns the decision-record library and the incident raised by R-UNI-39 |

The rights are the rows of TSD P9 T6.1 and nothing wider; no person is named, every duty is a role.

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-RPT-031 to DF-RPT-040 | `measure_definition` (P9) | measure_code, definition_version, data_product, unit | Read: the definition in force of the measures that carry the three dimensions |
| DF-RPT-041, DF-RPT-043, DF-RPT-044, DF-RPT-045, DF-RPT-046, DF-RPT-047, DF-RPT-048, DF-RPT-049, DF-RPT-051, DF-RPT-052 | `measure_snapshot` (P9) | id, definition_version, business_date, product_group, dimension_code, dimension_value, value, case_count, frozen, published_at | Write: the STAGE, AGE_BAND and ROUTE rows of the business date |
| DF-RPT-054, DF-RPT-055 | `measure_publish` (P9) | business_date, status | Read: whether the day is published, for BR5 |
| DF-CAS-001, DF-CAS-003, DF-CAS-005, DF-CAS-006, DF-CAS-008, DF-CAS-010, DF-CAS-013 | `recovery_case` (P3) | case id, product_group, status, stage_code, route_code, queue_id, entry_date | Read on the read model of EV-01 and EV-05; never as a table |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (P7) | decision reference, rule id, rule version, from and to stage, decided_at | Written as the local record of each change (DP-03) |
| DF-REF-001 to DF-REF-015 | `rule_row` (P7) | rule id, rule version, from state, event code, condition | Read through the rule-version read of 12.2; never as a table |
| DF-DOC-012 to DF-DOC-017 | `document_field` (P5) | the legacy Data section names this entity | Not read by this slice: documents are rwb-document's (GAP-2585; ASM-4278) |

Field IDs are those of the Logical Data Model and Data Dictionary and of TSD P9 T3.1. No table is added and no column is added: the classification rides the existing `dimension_code` and `dimension_value` columns (GAP-2585; ASM-4278). The legacy Flyway name of the module is the monolith's; the target migration, if one is needed at all, takes the next number of the `rwb_reporting` sequence.

### 12. Contract

#### 12.1 REST operations provided

Owner rwb-reporting (P9); base `/api/recovery/reporting/v1` (DP-13).

| Method | Path | Purpose | Auth | Errors |
|---|---|---|---|---|
| GET | `/reports/measures` | Read the measures of a period by measure, product, route and dimension (API-P9-001), including the re-aged STAGE, AGE_BAND and ROUTE values | Reporting R, scope applied | 401; 403 MSG-P4-002; 422 MSG-GEN-003; 503 MSG-GEN-006 |

The operation, its five query parameters and its answer are the service's one provided operation and are declared by RWB-P9-E8002-CON; this story adds no path, no parameter and no member and supplies the behaviour behind the three dimension values. The legacy path of the story moves to the per-service base and keeps its operation path (DP-13).

#### 12.2 REST operations consumed

| Operation | Owner | Contract | Purpose | Timeout |
|---|---|---|---|---|
| The classification rule rows and the rule version in force for a business date, on `/api/recovery/decision/v1` | rwb-decision (P7) | declared and faked by RWB-P9-E8002-CON; member names Not specified in the source documents (GAP-2585; ASM-4277) | the rule id, the rule version, the valid-from date, the stage set and the age bands | 2 s |

One hop, on the owner's published contract, never a table. The story plan declares no C row for this read, so it is declared and faked and blocks nothing.

#### 12.3 Events published

None of the service's own. The ownership row gives rwb-reporting no event, so nothing of this key is published on `rwb.reporting.events.v1`. The one thing that leaves is the local library's record on `rwb.decision-record.v1`, one per changed account and business date, with FEAT-RPT-10 as the decision reference (DP-03).

#### 12.4 Events consumed

| Event or fact | Topic | Owner | Use |
|---|---|---|---|
| `rwb.case.CaseCreated.v1` (EV-01) | `rwb.case.events.v1` | P3 rwb-case | a new open account gets its first reported classification |
| `rwb.case.CaseStateChanged.v1` (EV-05) | `rwb.case.events.v1` | P3 rwb-case | the stage change that re-ages one account at once |
| `rwb.decision.RulePackageInForce.v1` (EV-30) | `rwb.decision.events.v1` | P7 rwb-decision | a rule version reaching its valid-from date: every open account recomputed |
| The upstream re-age and reclassification fact of the source (name Not specified in the source documents (GAP-2585; ASM-4277)) | the owner's topic, named by the catalogue | P1 rwb-source-data | the ALS re-age behind R-UNI-22 |

Dedupe is by the CloudEvents id through the inbox; the consumer groups are those of RWB-P9-E8002-CON.

#### 12.5 Workflows and activities

None. The ownership row gives rwb-reporting no workflow, and this story adds none: the classification runs inside the daily run of 12.6 and inside the service's own event handler, with no child workflow, no activity contract and no Nexus call.

#### 12.6 Schedules

| Job | Queue | When | Step |
|---|---|---|---|
| JOB-15, the daily reporting run | `rwb-reporting` | Daily at 01:30 | The classification step of section 4 before the day's rows are published; no second Schedule and no Quartz row |

The registration detail of the Schedule belongs to the platform and to the measure stories of the service; this key adds no Schedule of its own.

#### 12.7 Tables owned

| Table | Schema | Contracted use |
|---|---|---|
| `measure_snapshot` | `rwb_reporting` | the STAGE, AGE_BAND and ROUTE rows of a business date, written here beside the other measures |
| `measure_definition` | `rwb_reporting` | the definition in force of the measures that carry the three dimensions; read only here |
| `measure_publish` | `rwb_reporting` | the PUBLISHED or HELD status of the business date; read only here |
| `decision_record` | PLT library, created in `rwb_reporting` | one local record per changed account (DP-03) |

`recovery_case`, `decision_log_entry` and `rule_row` are other owners' and are named here only as consumed answers. No foreign key leaves `rwb_reporting` and no statement reads another `rwb_*` schema or a `v_ace_*` view.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| rwb-decision rule read fake | the classification rule rows of one version for a business date, and a date with no version in force | AC1, X1, X2 |
| event harness for EV-01, EV-05 and EV-30 | one synthetic account opening, one stage change and one rule version reaching its valid-from date | AC1 |
| local decision-record stub | an accepted record with the rule id and the rule version, and a stopped chain returning MSG-P7-003 | AC1, AC2, X3 |
| rwb-reporting measure read fake | the measures of a period with the re-aged STAGE, AGE_BAND and ROUTE values and the `X-Data-As-Of` header | AC1 |
| gateway-bff composite route fake | the merged SCR-37 answer with the reported values read once | AC1, section 15 |

#### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 1 provided, 1 consumed | the measure read on `/api/recovery/reporting/v1`; the rule-version read of rwb-decision; one hop, 2 s |
| Kafka | none published, 4 consumed | EV-01, EV-05 and EV-30 plus the upstream re-age fact; the record leaves on `rwb.decision-record.v1` through the library |
| Temporal | none | the classification runs inside JOB-15 and the event handler; no domain workflow |
| File | none | no file is read or written by this key |

### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.reporting.classification`.

| Component | Type | Microservice responsibility |
|---|---|---|
| `ClassificationRunStep` | Service | steps 1, 2 and 10 of section 4: the daily step of JOB-15 and the single-account path of the event handler |
| `RuleVersionClient` | Client | the rule rows and the version in force on the rwb-decision read, with a 2 s budget and a breaker |
| `ClassificationProjection` | Service | derives the reported stage, route and age band from the case facts and the rule rows; holds no band and no threshold |
| `ReportedRowWriter` | Repository | writes the STAGE, AGE_BAND and ROUTE rows of `measure_snapshot` and applies the published guard of BR5 |
| `ChangeRecorder` | Publisher | the local record of each changed account through the library and the outbox (DP-03) |
| `ReportedMeasureView` | Service | the delta the existing measure read returns for the three dimensions |

**Database.** No new table and no new column: the write uses `measure_snapshot` as it stands, with the unique key on (measure_code, definition_version, business_date, product_group, dimension_code, dimension_value) so a repeat cannot duplicate a row. Whatever index the step needs is added by the per-service Flyway sequence in `rwb_reporting`.

**Configuration and reference data.** The measures and their definition versions are data rows of this service; the stages, routes and age bands belong to the rule version and are read through 12.2. The single parameter of the step is the recompute-on-version switch, whose name is assumed and not fixed by a source (GAP-2585; ASM-4279).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-03 | DecisionLogWriter, decision log | the local decision-record library and the topic `rwb.decision-record.v1`; one record per changed account before its row | H RWB-PLT-E1027-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/reporting/v1`; the one read of the service | none |
| DP-19 | Screen, ace-web | gateway-bff composite route for SCR-37 | H RWB-PLT-N001-CON |

**Build steps.** (1) Take the CON tag and build `RuleVersionClient` against its fake; test X1 and X2. (2) Build `ClassificationProjection` over the event fixtures of one synthetic day; test the re-age of AC1 with one rule version. (3) Build `ChangeRecorder` and the one-transaction rule; test AC2 and X3. (4) Build `ReportedRowWriter` and the idempotence key; test the repeat of X3 and the published guard of X5. (5) Build `ReportedMeasureView` and the SCR-37 fragment read; test the read of the re-aged values. (6) Run the boundary and grant tests of X8.

**Feature flag.** `rwb.reporting.reclassification`; off, the step writes no row and no record and the last reported classification stands.

**Done when** the tests of section 16 pass and one synthetic day produces the three dimension rows with the rule id and the rule version in the record of each changed account.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | A data product behind the case facts is stale for the business date | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P7-003 | The record of a change cannot be written | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The caller lacks Reporting R | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A field the rule rows need is missing, for example the entry date | Enter {field}. |
| MSG-GEN-006 | The rule-version read of rwb-decision is unavailable | {system} is not available. Your request is queued and will be retried. |
| MSG-P3-027 | No rule version is in force on the business date | The rule version was refused at the {check} check: {detail}. |

MSG-P1-001 is the text of VR-P9-010-1, MSG-P7-003, MSG-P4-002 and MSG-GEN-001 are the texts of the legacy story, MSG-GEN-006 is the platform text and MSG-P3-027 is the rule owner's text; each is copied unchanged and none names an account or a person.

### 15. Screens and states

No screen in this story, as the legacy story says. The reported classification is read on SCR-37 Steering dashboard through the gateway-bff composite route of RWB-PLT-N001-CON (DP-19), where this story contributes the states of the three dimensions:

| State | What the reader sees |
|---|---|
| Reported | the STAGE, AGE_BAND and ROUTE values of the latest published business date, with its `X-Data-As-Of` |
| Re-aged | the values of the later row set when a version changed, with the version in force of that date |
| Stale | the values of their own business date with MSG-P1-001, never presented as the business date |
| Held | the earlier published date beside the held reason of `measure_publish` |

The screen builds no value of its own: it renders the rows of `measure_snapshot` and their stamps.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-E8-002-01 | AC1 | Component | A synthetic day of case events, one rule version with its stage set and age bands, and the derived stage, route and age band of each open account |
| TC-E8-002-02 | AC2 | Component | The record library forced to refuse; no row and no record changed, MSG-P7-003 returned |
| TC-E8-002-03 | Access | Contract | RW-TEAMMGR reads in scope with Reporting R; a role without the right is refused with MSG-P4-002 |
| TC-E8-002-04 | Principle 5 | NFR | The record library forced to fail across ten business dates; nothing is written, nothing is published and an incident is raised |

The four legacy cases keep their IDs, their order and their intent; the contract cases are in RWB-P9-E8002-CON section 16. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID. Integration copies of these IDs end in `-ITG` and belong to the wave 4 integration story of this key.

### 17. Guardrails

- No business value in code: the stages, routes, age bands, thresholds and measure codes are data rows of their owners, read from the rule version in force.
- No personal data in a snapshot, a record, an event or a log: case and account references, codes, dates and counts only.
- ACE data only through the owner's contract: this service reads no `v_ace_*` view and no ACE table, and the case facts arrive on events.
- No table of `rwb_case`, `rwb_decision` or `rwb_document` is read or written; no cross-schema join and no shared login.
- A published or frozen day is never rewritten (BR5); a late change is a later date plus a record that names both.
- No value is recomputed twice: the inbox marks the second delivery and the unique key of the row set refuses a duplicate.

### 18. Traceability

| Item | Value |
|---|---|
| Requirement and feature | FEAT-RPT-10 Classify, stage and re-age an account, Epic 8, module P9 (FSD P9 A2.10); the FSD "Requirements served" table is empty and the legacy story names no REQ, so the feature and the rules are the trace (GAP-2585; ASM-4280) |
| Business rules | BR-P9-010; VR-P9-010-1; NFR-065; R-UNI-22, R-UNI-38, R-UNI-39 |
| Legacy criteria | AC-P9-010-01 and the two exception flows AC-EXC-P9-010-01 and AC-EXC-P9-010-02 of FSD P9 A2.10 |
| Legacy and disposition | RWB-E8-002, Split (rework); the app slice owns AC1 and AC2 |
| Test cases | TC-E8-002-01 to TC-E8-002-04 |
| Decoupling patterns | DP03, DP13, DP19 |
| Architecture decisions | ADR-013, ADR-014, ADR-015, ADR-018, ADR-019, ADR-020, ADR-021, ADR-022 |

### 19. Out of scope

- The contract baseline, its document, its fakes and its contract tests (RWB-P9-E8002-CON).
- The case-side recompute of the segment, the route reopen, the hard-gate re-run and the owner ladder of rules R-UNI-22, R-UNI-19 and R-UNI-37, which stay with rwb-case (GAP-2586; ASM-4281).
- The classification and re-ageing rule rows themselves, their authoring, test and promotion, which are the rule registry's.
- The measure set, the steering data set and the publish or hold decision of the same service (RWB-P9-E1013-APP, RWB-P9-E2009-APP).
- The benefit realisation of FEAT-RPT-06 and the regulatory returns of FEAT-RPT-07.
- Any data lake, Power BI or file path, and any Schedule of this key.
