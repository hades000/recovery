# RWB-ITG-DM011-ITG Migrate scores and route economics

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM011-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-DM011-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-011 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves the route each open case carries and the route economics baseline survive cutover, that each measure snapshot keeps its dimension, its value and its baseline flag, and that no COLLINS score is copied because the score, its estimate and its route are read from ACE, against the owning services' published contracts and their fakes**, so that **the baseline and the route history survive cutover while every business key on a migrated record is proven against its ACE view row and every orphan is on a list with a reason and two owners**.

This story builds the harness and the evidence, and nothing else. The real records are migrated by RWB-P1-DM011-APP on P1's own Flyway sequence (DP-15), and the reconciliation that produces the breaks is that story's too. This harness depends on it only as an I dependency and its stub answers until it lands. The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes a report per business date.

### 2. Business rationale

The route a case carries and the route economics baseline behind it are what the bank uses to argue, months later, that a case was worked on the path the policy required and at the return the models expected. If the route code, the route state or the baseline flag of a snapshot is lost in cutover, the case opens on the wrong path, the return on the route cannot be defended to the committee, and the measure that steering reads for the day is a number with no baseline behind it. The failure is quiet as well: a case list that loads clean and reconciles to nothing still looks like a successful cutover until an officer tries to work the case, and a score that was copied instead of read starts to disagree with ACE on the first COLLINS model refresh.

The same story carries the opposite risk. A COLLINS score that is copied into the Workbench at cutover becomes a second source of truth for a model output the bank does not own, and it goes stale without anybody noticing; so the score, its estimate and its route stay where ACE holds them and are read through rwb-source-data's contract every time (DP-05), and the harness asserts that nothing of the three is stored on a migrated record.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the route and its state are read from rwb-valuation, which owns the D6 route decision; the measures and their snapshots are read from rwb-reporting, which owns measures and snapshots; the case is read from rwb-case, which owns the case; the cutover load runs on P1's own Flyway sequence (DP-15); the legacy story names the SCR-45 Data quality console, which this harness neither builds nor calls, and where a screen would compose these reads the path is the gateway-bff composite route (DP-19); every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries DL25 and the zero-tolerance rule on the migrated data into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S1 rwb-valuation (the case valuation read), P9 rwb-reporting (the measures read), P3 rwb-case (the case read), P1 rwb-source-data (DP01, DP11, freshness and the JOB-04 rerun) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP11 Scores and route economics, each with one system of record, so account_key and the score row have one named owner before a key is resolved (FSD P1 v3, A2.2 and line 293).
- The cutover load of P1's own Flyway sequence (DP-15) has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM011-APP owns the migration and the reconciliation; until it lands, the cutover extract fixture and the reconciliation extract fixture stand in for its output.
- The harness environment and its base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and its retention, the pass or fail gate and the seeding set: Not specified in the source documents (GAP-0451; ASM-0643).
- The synthetic case, the synthetic keys, the synthetic route code and route state, the measure snapshot and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM011-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-12-31: open case RW-2026-001101 with route code RT-SYN-011 and route state RS-SYN-001, the account key ACC-SYN-001101 and the person key PERS-SYN-001101, one case list row for the business date, and one measure snapshot with measure_code MSR-SYN-011, definition_version 1, product_group PG-SYN-A, dimension_code DIM-SYN-A and its baseline flag. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: triggers JOB-04 reconciliation on rwb-source-data with one Idempotency-Key per business date, through `POST /api/recovery/source-data/v1/admin/jobs/JOB-04/rerun`.
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case number and that it is open.
4. Harness: reads the case through `GET /api/recovery/valuation/v1/cases/{caseId}/valuation` and asserts route code RT-SYN-011 and route state RS-SYN-001, unchanged from the fixture.
5. Harness: reads the snapshots through `GET /api/recovery/reporting/v1/reports/measures` for business date 2026-12-31 and asserts measure_code MSR-SYN-011, definition_version 1, product_group PG-SYN-A, dimension_code DIM-SYN-A and the baseline flag on the snapshot.
6. Harness: resolves each key through `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}`: DP01 for account_key ACC-SYN-001101, the case list row for the business date, and DP11 for the score row, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for the business date and the load time.
7. Harness: asserts that no COLLINS score, estimate or route is stored on a migrated record, and that the score, its estimate and its route the report quotes are the values the same DP11 read returns on that hop.
8. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan, its reason and its two owners; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen.
9. Harness: reruns JOB-04 for the same business date with the same Idempotency-Key and compares the break list and the counts of cases, case list rows and measure snapshots with the first run.
10. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002, no reconciliation run started and no break row written.
11. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the four criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-011-01-ITG (ITG AC2) |
| X2 | The cutover extract fixture lacks a required key or the route code on a migrated record | The run fails and the report names the case and the missing field; a record without a key or without a route code is never reported as reconciled | None | TC-DM-011-01-ITG (ITG AC2) |
| X3 | A key has no view row and the extract does not list it | The run fails on AC1 and the report names the case, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-011-02-ITG (ITG AC1, ITG AC3) |
| X4 | A rerun lists the same break twice | The run fails on AC4 and the report names the two rows and the business date | None | TC-DM-011-03-ITG (ITG AC4) |
| X5 | JOB-04 is refused because the ACE batch is late | The run fails before any assertion and the report names the product, the date and the message; a stale product is never treated as an empty result | MSG-P1-001 | TC-DM-011-02-ITG (ITG AC1) |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC4 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-011-04-ITG (ITG AC4) |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC4 and the report names each count and its two values | None | TC-DM-011-03-ITG (ITG AC4) |
| X8 | A migrated record or the report holds a stored COLLINS score, estimate or route | The run fails on AC3 and the report names the record, the field and the DP11 read it should have used | None | TC-DM-011-01-ITG (ITG AC3) |
| X9 | The measure snapshot loses its baseline flag, or the case loses its route code or route state | The run fails on AC2 and the report names the snapshot or the case, the field and the values it read on the two hops | None | TC-DM-011-01-ITG (ITG AC2) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM011-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The route, the route state and the baseline flag are proven to survive cutover, no COLLINS output is copied, and every orphan is on a list with a reason and two owners, before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one no-copy assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate scores and route economics - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds open case "RW-2026-001101" with route code "RT-SYN-011" and route state "RS-SYN-001"
    Given the case carries account_key "ACC-SYN-001101" and person_key "PERS-SYN-001101"
    Given the cutover extract holds one measure snapshot with measure_code "MSR-SYN-011", definition_version "1", product_group "PG-SYN-A" and dimension_code "DIM-SYN-A"
    Given the ACE views hold one row for account_key "ACC-SYN-001101" and one score row under DP11
    Given JOB-04 has run for business date "2026-12-31"

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-011 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC2 The route and the baseline flag survive cutover (new, D-RCV-60)
    Given the migrated records for business date "2026-12-31"
    When the harness reads case "RW-2026-001101" from the rwb-valuation contract and the measure snapshots from the rwb-reporting contract
    Then the case keeps route code "RT-SYN-011" and route state "RS-SYN-001"
    And the snapshot for measure_code "MSR-SYN-011" keeps definition_version "1", business_date "2026-12-31", product_group "PG-SYN-A" and dimension_code "DIM-SYN-A"
    And the snapshot keeps its value and its baseline flag
    And the run report names the route code, the route state and the baseline flag it read, with the contract version of each hop

  Scenario: AC3 A key resolves in one hop, an orphan is listed with its reason, and no COLLINS value is copied (new, D-RCV-60)
    Given the case list row for business date "2026-12-31" carries account_key "ACC-SYN-001177"
    And the ACE views hold no row for account_key "ACC-SYN-001177"
    When the harness resolves the key through the rwb-source-data data-product contract in one hop with a 2 s budget
    Then the break list holds one row for case "RW-2026-001101" with key type "ACCOUNT", key value "ACC-SYN-001177" and reason "NO_ACE_ROW"
    And the row names the owner role "RW-DATASTEW" and the ACE team as the second owner, and the run report names both
    And the score row under DP11 is read from v_ace_score on that hop
    And no COLLINS score, its estimate and its route are stored on a migrated record or in the run report

  Scenario: AC4 A repeated run is deterministic and a caller without the right is refused (new, D-RCV-60)
    Given the reconciliation for business date "2026-12-31" has run once
    And a synthetic user with role "RW-OFF" and no Platform administration right
    When JOB-04 is rerun for the same business date and the synthetic user calls the reconciliation run for the same business date
    Then the break list holds exactly one row for account_key "ACC-SYN-001177"
    And the counts of cases, case list rows and measure snapshots equal the first run
    And the run report holds one entry per business date and not one per run
    And the answer to the synthetic user is 403 with "MSG-P4-002" and no second run starts
```

Legacy AC1 and AC3 belong to RWB-P1-DM011-APP, and the four criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated case, case list row or measure snapshot resolves to its ACE view row before the record is served | REQ-RDF-007; DL25 |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 |
| BR3 | Zero tolerance holds the publish: wave 4 does not open while one migrated record has an unresolved key | DL25 |
| BR4 | ACE data is read only through the rwb-source-data contract and the recovery.v_ace_* views behind it, and never copied | D-RCV-35; ADR-010 |
| BR5 | The COLLINS score, its estimate and its route are read from v_ace_score and are never stored on a migrated record | Legacy RWB-DM-011 AC1; D-RCV-35 (U1) |
| BR6 | An open case keeps its route code and its route state from cutover, and a measure snapshot keeps its dimension, its value and its baseline flag | Legacy RWB-DM-011 AC1; DL25 |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 |

The harness asserts these rules and changes none of them.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Route state RS-SYN-001 | Reconciliation for the business date with every key resolved | JOB-04 completes and every account_key and person_key has a DP01 or DP02 row | RS-SYN-001, unchanged |
| Route state RS-SYN-001 | Reconciliation for the business date with one orphan | account_key ACC-SYN-001177 has no DP01 row | RS-SYN-001, unchanged, and the orphan is listed |
| Route state RS-SYN-001 | A listed orphan resolves and is reconciled | A DP01 row appears for the key and JOB-04 is rerun for the same business date | The break is no longer listed; the route state is unchanged |

The harness changes no state. Every change in the table is made by the owner: S1 rwb-valuation holds the route decision and its state, P9 rwb-reporting holds the measures and their snapshots, P3 rwb-case holds the case, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a value it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Runs and reads the reconciliation for a business date; holds Platform administration R; owns the break list with the ACE team |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 and writes the reconciliation result, S1 rwb-valuation answers the route read, P9 rwb-reporting answers the measures read, P3 rwb-case holds the case, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | recovery_case | case_no, product_group, primary_person_key, status, stage_code | Read through the rwb-case contract |
| DF-RPT-001 to DF-RPT-019 | case_list_row | business_date, case_id, case_no, account_key, product_group | Read through the rwb-source-data data-product contract |
| DF-RPT-041 to DF-RPT-052 | measure_snapshot | measure_code, definition_version, business_date, product_group, dimension_code, baseline flag | Read through the rwb-reporting contract |
| Not listed in the legacy story | route decision | route code, route state | Read through the rwb-valuation contract |

Field IDs are those in the Logical Data Model and Data Dictionary v8, and the three rows above are the ones the legacy story carries. The case is P3's, the case list row is P1's daily published projection, and the measure snapshot is P9's; the harness reads each of them through its owner's contract and never from a table. The route code and the route state are named by the legacy story without a field ID, so this story asserts them as the values the rwb-valuation read returns and does not invent an identifier for them. The ACE side of the keys is DP01 Account and arrears for account_key and DP02 Customer and party for person_key, and the score, its estimate and its route are the DP11 Scores and route economics row over v_ace_score, each read through the rwb-source-data data-product contract (FSD P1 v3, lines 283, 284 and 293), never from a view and never from a table. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/valuation/v1/cases/{caseId}/valuation` | S1 rwb-valuation | The route code and the route state the case carries (AC2) |
| GET | `/api/recovery/reporting/v1/reports/measures` | P9 rwb-reporting | The measure snapshots with measure_code, definition_version, business_date, product_group, dimension_code, value and the baseline flag (AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case number and the open state of the case (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP01 account rows, the case list row and the DP11 score row that carries the score, its estimate and its route (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time of the product (AC1) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Run JOB-04 reconciliation for the business date, with one Idempotency-Key (AC1, AC4) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, the S1 read is the valuation read and the P4 refusal is the authorise operation the architecture publishes as their IN contracts (Architecture v5 slides 14 and 18), and where a screen would compose these reads the path would be the gateway-bff composite route (DP-19). The score is never read from a view by the harness; it arrives on the DP11 hop of the rwb-source-data contract (DP-05).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness triggers JOB-04 through the owner's operation, not through an event, and reads the route, the measures and the score through the same contracts rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04 reconciliation, the event-triggered reconciliation workflow on rwb-source-data (Architecture v5 slides 15 and 44), is exercised through its rerun operation. S1's RouteDecisionWorkflow and P9's measures Schedule are named here and left alone: the harness reads the route decision the workflow already recorded and the snapshot the Schedule already wrote, and it starts, signals, reschedules or changes neither of them. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. JOB-04 is event-triggered; the harness reruns it for the business date under test and sets no cron. The measures Schedule at 01:30 stays with rwb-reporting and is not touched.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the case is P3's, the case list row and the reconciliation result are P1's, the measures and snapshots are P9's, and the route decision is S1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | The three P1 operations of §12.2 | DP01 returns one row for ACC-SYN-001101 and no row for ACC-SYN-001177, the case list row carries ACC-SYN-001177 for business date 2026-12-31, DP11 returns the score row with its score, its estimate and its route, freshness returns business date 2026-12-31 with a load time, and the rerun is accepted once per Idempotency-Key |
| Stub for rwb-valuation | `GET /cases/{caseId}/valuation` | Case RW-2026-001101 with route code RT-SYN-011 and route state RS-SYN-001 |
| Stub for rwb-reporting | `GET /reports/measures` | One snapshot for measure_code MSR-SYN-011, definition_version 1, business_date 2026-12-31, product_group PG-SYN-A, dimension_code DIM-SYN-A, with its value and a baseline flag |
| Stub for rwb-case | `GET /cases/{caseId}` | The case RW-2026-001101, open, with its case number |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The case with its route code and route state, the case list row, the measure snapshot with its dimension, its value and its baseline flag, the orphan account_key ACC-SYN-001177 on the case list row, and the source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row for case RW-2026-001101 with key type ACCOUNT, key value ACC-SYN-001177, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and its base hosts, the fixture layout, the break-list fields, the extract format and its retention and the gate are Not specified in the source documents (GAP-0451; ASM-0643).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contracts |
| Temporal | None added; JOB-04 reconciliation, the event-triggered workflow on rwb-source-data, is exercised, while S1's RouteDecisionWorkflow and P9's measures Schedule are read only and left alone |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are recorded here and are not repeated in the metadata H field of this story, which stays empty as the plan requires: the platform waves deliver both contracts, and this harness carries no build dependency of its own. The one blocking relationship is the I story RWB-P1-DM011-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The five stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic case with its route code and route state, the case list row, the measure snapshot and the orphan account_key, with source and migrated_at |
| RouteAndBaselineAssertion | Service | Compares the route read and the measures read with the fixture: route code, route state, measure_code, definition_version, business_date, product_group, dimension_code, value and the baseline flag |
| KeyResolver | Service | Resolves every business key through DP01 and DP02 with the freshness read, reads the DP11 score row, and names each key that does not resolve |
| NoCopyAssertion | Service | Fails the run where a migrated record or the report holds a stored COLLINS score, estimate or route, and pins the DP11 read the report quotes |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a rerun |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic case RW-2026-001101, route code RT-SYN-011, route state RS-SYN-001, account_key ACC-SYN-001101, person_key PERS-SYN-001101, measure snapshot MSR-SYN-011 at definition_version 1 for product_group PG-SYN-A and dimension_code DIM-SYN-A, orphan account_key ACC-SYN-001177 and business date 2026-12-31. In SIT the records come from the cutover load of P1's own Flyway sequence (DP-15). The environment and its base hosts, the fixture layout, the break-list fields, the extract format and its retention, the gate and the seeding set are not specified in the source documents (GAP-0451; ASM-0643). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the five stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-12-31 (X2).
3. Build the JourneyRunner for AC1: trigger JOB-04 with one Idempotency-Key, read the case through rwb-case, resolve account_key and person_key through DP01 and DP02 with the freshness read, and list each orphan (X5).
4. Add the RouteAndBaselineAssertion for AC2: route code RT-SYN-011 and route state RS-SYN-001 from the rwb-valuation read, and measure_code, definition_version, business_date, product_group, dimension_code, value and the baseline flag from the rwb-reporting read (X9).
5. Add the NoCopyAssertion and the DP11 read for AC3: one hop with a 2 s budget, the orphan row with reason NO_ACE_ROW and both owners, and no stored score, estimate or route on a migrated record or in the report (X3, X8).
6. Add AC4: rerun JOB-04 for the same business date, assert one break row, equal counts of cases, case list rows and measure snapshots, and one report entry per business date (X4, X7).
7. Add the access path for AC4 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM011-APP when it lands, and the wave entry check holds a run report keyed by story and business date that names the route code, the route state, the baseline flag, the DP11 score read and every break with its reason and its two owners.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-P1-012 | Warning | The case list for {date} does not reconcile to ACE for {product}: a difference of {variance} accounts, {pct} percent. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text. MSG-P1-012 is asserted on the case list row of the business date, because a case list that does not reconcile is a break before any key is resolved.

### 15. Screens and states

The legacy story names SCR-45 Data quality with the states loading and breaks, and it states that the breaks are listed on the reconciliation extract. This harness builds neither the screen nor the console: the data steward and the ACE team read the extract as a file. The states the harness asserts on that extract are small.

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of cases, case list rows and measure snapshots, and no break row |
| Break | One row per orphan with the case number, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. What the wave entry check looks at instead is the run report, whose environment, layout, extract format and retention are Not specified in the source documents (GAP-0451; ASM-0643).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-011-01-ITG | AC1 (legacy, the extraction RWB-P1-DM011-APP owns); ITG AC2, ITG AC3 | Integration | The synthetic cutover extract RW-2026-001101 with route code RT-SYN-011, route state RS-SYN-001 and measure snapshot MSR-SYN-011, and no stored COLLINS value |
| TC-DM-011-02-ITG | AC2 (legacy); ITG AC1, ITG AC3 | Integration | One account_key ACC-SYN-001177 on the case list row with no view row, and the DP11 score row read on the same hop |
| TC-DM-011-03-ITG | AC3 (legacy, owned by RWB-P1-DM011-APP); ITG AC4 | Integration | Two JOB-04 runs for business date 2026-12-31 |
| TC-DM-011-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |

The Covers column names the legacy AC the copy derives from and the ITG AC it asserts; the cutover assertions of TC-DM-011-03-ITG stay with RWB-P1-DM011-APP, and the ITG copy asserts only the determinism of the rerun and the one report per business date. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic keys, the route code, the route state, the measure snapshot, the business date, the fixture contents, the break reasons and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the case comes from rwb-case, the route from rwb-valuation, the measures from rwb-reporting, and the ACE side of the keys and the score from the rwb-source-data contract (DP-01, DP-05).
- Nothing of the COLLINS score is stored: the score, its estimate and its route are read on the DP11 hop every time, and a stored copy fails the run rather than being reported as a pass.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-011 Migrate scores and route economics | Recovery Workbench Data Migration Stories v3, lines 716 to 796 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 741 to 745 | Section 7, AC1, marked (legacy RWB-DM-011 AC2) |
| Legacy AC1 and AC3, and the four legacy test cases TC-DM-011-01 to TC-DM-011-04 | The same, lines 735 to 751 and 789 to 794 | AC1 and AC3 stay with RWB-P1-DM011-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-CAS-001 to DF-CAS-055, DF-RPT-001 to DF-RPT-019, DF-RPT-041 to DF-RPT-052 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DP01 Account and arrears, DP02 Customer and party, DP11 Scores and route economics, each with one system of record | FSD P1 v3, lines 283, 284 and 293 | Sections 3, 11 and 12.2 |
| S1 rwb-valuation, its IN read `GET /cases/{id}/valuation` and the D6 route decision | Architecture v5 Text Extract v1 slides 18 and 41 | Sections 12.2 and 12.5 |
| P9 rwb-reporting, which owns measures and snapshots, with its Schedule at 01:30 | Architecture v5 Text Extract v1 slides 15 and 41 | Sections 11, 12.2 and 12.5 |
| JOB-04 Reconciliation, event-triggered on rwb-source-data | Architecture v5 Text Extract v1 slides 15, 44 and the job map | Section 12.5 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR5; sections 12.2 and 12.8 |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM011-APP: the migration, the reconciliation, the break list and legacy AC1 and AC3. The cutover load of the records into `rwb_source_data` and the schemas of the other owners is theirs, on their own Flyway sequences.
- The production code of S1 rwb-valuation, P9 rwb-reporting, P3 rwb-case and P1 rwb-source-data, and their CON, APP and DB stories: the route decision, the measures and snapshots, the case and the reconciliation are built there.
- S1's RouteDecisionWorkflow and P9's measures Schedule: named in section 12.5 and left alone; the harness reads what they already wrote.
- SCR-45 Data quality and the break console the legacy story names; the harness renders no screen and reads the reconciliation extract as a file.
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001), and the COLLINS model refresh itself.
- Platform deployment and configuration.
- The other four data migration keys of this wave.
