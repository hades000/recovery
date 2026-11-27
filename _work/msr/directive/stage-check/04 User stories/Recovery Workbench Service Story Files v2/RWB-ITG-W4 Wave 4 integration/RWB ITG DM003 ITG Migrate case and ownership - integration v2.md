# RWB-ITG-DM003-ITG Migrate case and ownership

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM003-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-003 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Size | Not specified in the source documents (DOR-RWB-ITG-DM003-ITG-16); the squad sizes at refinement |
| Depends on (build) | RWB-P1-DM003-APP (build dependency, not done yet; also named under Integration dependencies) |
| Contract dependencies | Not specified in the source documents (DOR-RWB-ITG-DM003-ITG-21) |
| Contract version | v1 (owner base /api/recovery/<short>/v1, section 12.2) |
| Integration dependencies | RWB-P1-DM003-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-003 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-ITG-DM003-ITG). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (16 resolved, 14 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated case and ownership records resolves to its ACE view row and lists every orphan for the data steward and the ACE team, against the owning services' published contracts and their fakes**, so that **every open case keeps its owner, its queue and its history from the first day after cutover**.

This story builds the harness and the evidence, and nothing else. The real records are loaded by P3's own cutover migration on its own Flyway sequence (DP-15), and the reconciliation that produces the breaks is RWB-P1-DM003-APP's. The story builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes a report per business date.

### 2. Business rationale

An open case served on the first day with an account_key or a person_key that resolves to no ACE row loses its owner, its queue and its history. The case list shows work that nobody can pick up, and the officer who opens it finds nothing behind the links. The failure is quiet: the cutover load can report a clean run while the keys it wrote point at rows that the ACE views do not hold, and a break that nobody lists is a silent data loss that surfaces weeks later as a misplaced case or a wrong queue measure. DL25 puts zero tolerance on that, so the migrated records are proven against the views before the cutover is called done, and every orphan is on a list with a reason and two owners.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the case, its account links and its party links are read from rwb-case, which owns recovery_case, case_account, case_party and assignment; the cutover load runs on P3's own Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and this legacy story states that no screen exists; every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries REQ-RDF-007, REQ-RDF-008 and DL25 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of P3 rwb-case (case, accounts, parties), P1 rwb-source-data (DP01, DP02, freshness and the JOB-04 rerun) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP02 Customer and party, each with one system of record, so account_key and person_key have one named owner before a key is resolved (FSD P1 v3, A2.2).
- The cutover load of P3's own Flyway sequence (DP-15) has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM003-APP owns the reconciliation and the break list; until it lands, the reconciliation extract fixture stands in for its output.
- The harness pack is agreed at the wave 4 entry check: a cutover extract fixture with case, account and party rows plus source and migrated_at; a reconciliation extract with one row per orphan and its reason; one report per business date; and a gate that fails on any unresolved key or suppressed break. The SIT environment and base hosts, the fixture layout detail, the break-list fields, the evidence retention and the data seeding set: Not specified in the source documents (GAP-0443; ASM-0635).
- The synthetic case, the synthetic keys and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM003-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30: case RW-2026-000601 with owner RW-OFF, queue MTG-BKK-CO and stage WITH_FCR_OFFICER, the account links ACC-SYN-000601 and ACC-SYN-000777, and the party link PERS-SYN-000601. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: triggers JOB-04 reconciliation on rwb-source-data with one Idempotency-Key per business date, through `POST /api/recovery/source-data/v1/admin/jobs/JOB-04/rerun`.
3. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case number, the owner RW-OFF, the queue MTG-BKK-CO and the stage WITH_FCR_OFFICER.
4. Harness: reads the links through `GET /api/recovery/case/v1/cases/{caseId}/accounts` and `GET /api/recovery/case/v1/cases/{caseId}/parties`, and asserts account_key ACC-SYN-000601 and ACC-SYN-000777 on the account links and person_key PERS-SYN-000601 on the party link.
5. Harness: resolves each key through `GET /api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` for account_key and `GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` for person_key, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for the business date and the load time.
6. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan and its reason; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen.
7. Harness: reruns JOB-04 for the same business date with the same Idempotency-Key and compares the break list and the counts of cases, account links and party links with the first run.
8. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002, no reconciliation run started and no break row written.
9. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the four criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case | Covered by |
|---|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-003-01-ITG (ITG AC1) | ITG AC1 |
| X2 | The cutover extract fixture lacks a required key on a migrated record | The run fails and the report names the case and the missing field; a record without a key is never reported as reconciled | None | TC-DM-003-01-ITG (ITG AC1) | ITG AC1 |
| X3 | A key has no view row and the extract does not list it | The run fails on AC2 and the report names the case, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-003-02-ITG (ITG AC2) | ITG AC2 |
| X4 | A rerun lists the same break twice | The run fails on AC3 and the report names the two rows and the business date | None | TC-DM-003-03-ITG (ITG AC3) | ITG AC3 |
| X5 | JOB-04 is refused because the ACE batch is late | The run fails before any assertion and the report names the product, the date and the message; a stale product is never treated as an empty result | MSG-P1-001 | TC-DM-003-01-ITG (ITG AC1) | ITG AC1 |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC4 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-003-04-ITG (ITG AC4) | ITG AC4 |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC3 and the report names each count and its two values | None | TC-DM-003-03-ITG (ITG AC3) | ITG AC3 |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM003-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The migrated case and ownership keys are proven against the ACE views, and every orphan is on a list with a reason and two owners, before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one break-list assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate case and ownership - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds open case "RW-2026-000601" with owner "RW-OFF", queue "MTG-BKK-CO" and stage "WITH_FCR_OFFICER"
    Given the case links account_key "ACC-SYN-000601" and person_key "PERS-SYN-000601"
    Given the ACE views hold one row for account_key "ACC-SYN-000601" and one row for person_key "PERS-SYN-000601"
    Given JOB-04 has run for business date "2026-11-30"

  Scenario: AC1 Reconcile the business keys (legacy RWB-DM-003 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC2 An orphan is listed with its reason and nothing is deleted (new, D-RCV-60)
    Given a migrated case_account row for case "RW-2026-000601" carries account_key "ACC-SYN-000777"
    And the ACE views hold no row for account_key "ACC-SYN-000777"
    When the harness reads the reconciliation result for business date "2026-11-30"
    Then the break list holds one row for case "RW-2026-000601" with key type "ACCOUNT" and key value "ACC-SYN-000777"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the migrated case and its links stay readable through the rwb-case contract
    And the run report names the ACE team as the second owner of the break

  Scenario: AC3 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When JOB-04 is rerun for the same business date
    Then the break list holds exactly one row for account_key "ACC-SYN-000777"
    And the counts of cases, account links and party links equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC4 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When the harness calls the reconciliation run for business date "2026-11-30"
    Then the answer is 403 with "MSG-P4-002"
    And no reconciliation run starts and no break row is written

  Scenario: AC5 Zero tolerance holds the publish (new, D-RCV-60)
    Given a migrated case_account row for case "RW-2026-000601" carries account_key "ACC-SYN-000777" with no ACE view row
    When the harness reads the wave 4 publish state for business date "2026-11-30"
    Then wave 4 does not open
    And the report names the unresolved key "ACC-SYN-000777"

  Scenario: AC6 A migrated record keeps its source and its migration date (new, D-RCV-60)
    Given a migrated case "RW-2026-000601" from the cutover extract
    When the harness reads the migrated case through the rwb-case contract
    Then the record holds source and migrated_at
    And the record holds no copy of an ACE row

  Scenario: AC7 An open case keeps its owner, its queue and its stage from cutover (new, D-RCV-60)
    Given the cutover extract holds open case "RW-2026-000601" with owner "RW-OFF", queue "MTG-BKK-CO" and stage "WITH_FCR_OFFICER"
    When the harness reads the migrated case through the rwb-case contract
    Then owner, queue and stage equal the cutover values

  Scenario: AC8 Each service applies its own Flyway sequence in its own schema (new, D-RCV-60)
    Given the P3 cutover migration runs on its own Flyway sequence (DP-15)
    When the harness runs
    Then the harness applies no Flyway migration
    And the harness owns no table and writes no row

  Scenario: AC9 ACE data is read only through its owner and never copied (new, D-RCV-60)
    Given the harness reads ACE data for account_key "ACC-SYN-000601" and person_key "PERS-SYN-000601"
    When the harness reads the ACE side of the keys
    Then the read goes through the rwb-source-data data-product contract
    And no ACE row is copied to a table

  Scenario: AC10 A consumed call that fails or does not answer holds the publish (new, D-RCV-60)
    Given the harness reads ACE data for account_key "ACC-SYN-000601" through the rwb-source-data data-product contract
    When the consumed call fails or gets no answer
    Then the run fails and the report names the service and the operation
    And no criterion is marked passed
    And wave 4 does not open
    And no ACE row is copied to a table
```

Legacy AC1 and AC3 belong to RWB-P1-DM003-APP, and the ten criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | Every business key on a migrated case, account link or party link resolves to an ACE view row before the record is served | REQ-RDF-007; DL25 | ITG AC1; TC-DM-003-01-ITG |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 | ITG AC2; TC-DM-003-02-ITG |
| BR3 | Zero tolerance holds the publish: wave 4 does not open while one migrated record has an unresolved key | DL25 | ITG AC5; TC-DM-003-05-ITG |
| BR4 | ACE data is read only through the recovery.v_ace_* views owned by rwb-source-data, and never copied | D-RCV-35; ADR-010 | ITG AC9; TC-DM-003-09-ITG |
| BR5 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | Legacy RWB-DM-003 AC1; D-RCV-35 (U1) | ITG AC6; TC-DM-003-06-ITG |
| BR6 | An open case keeps its owner, its queue and its stage from cutover | Legacy RWB-DM-003 AC1; DL25 | ITG AC7; TC-DM-003-07-ITG |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 | ITG AC8; TC-DM-003-08-ITG |

The harness asserts these rules and changes none of them. The open decision DL25 underlies BR1, BR3 and BR6; its assumptions ASM-0728, ASM-0735, ASM-0743 and ASM-2602 are confirmed by the programme directive of 26 November 2026, and this story does not close DL25.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| WITH_FCR_OFFICER | Reconciliation for the business date with every key resolved | JOB-04 completes and every account_key and person_key has a DP01 or DP02 row | WITH_FCR_OFFICER, unchanged |
| WITH_FCR_OFFICER | Reconciliation for the business date with one orphan | account_key ACC-SYN-000777 has no DP01 row | WITH_FCR_OFFICER, unchanged, and the orphan is listed |
| WITH_FCR_OFFICER | A listed orphan resolves and is reconciled | A DP01 row appears for the key and JOB-04 is rerun for the same business date | The break is no longer listed; the stage is unchanged |

The harness changes no state. Every change in the table is made by the owner: P3 rwb-case holds the case, its owner, its queue and its stage, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Runs and reads the reconciliation for a business date; holds Platform administration R; owns the break list with the ACE team |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 and writes the reconciliation result, P3 rwb-case holds the case and the links, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055 | recovery_case | case_no, owner, queue, stage_code | Read through the rwb-case contract |
| DF-CAS-024 to DF-CAS-029 | case_account | account_key, is_primary, linked_from, linked_to | Read through the rwb-case contract |
| DF-CAS-030 to DF-CAS-035 | case_party | person_key, party_role, role_from, role_to | Read through the rwb-case contract |
| DF-WRK-009 to DF-WRK-016, DF-WRK-039, DF-WRK-040 | assignment | assignee_user_id, assigned_at, ended_at | Read through the rwb-case contract |
| Standard column | recovery_case, case_account, case_party, assignment | source, migrated_at | Read through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary v9. The four tables are P3's and the harness reads them only through the rwb-case contract. The ACE side of the keys is DP01 Account and arrears for account_key and DP02 Customer and party for person_key, read through the rwb-source-data data-product contract (FSD P1 v3, lines 283 and 284), never from a view and never from a table. The harness owns no table and writes no row. Reference data: the harness reads the break reason "NO_ACE_ROW" and the key type "ACCOUNT" as values through the reference-data contracts DP-06 and DP-07; the parameters it reads are Not specified in the source documents (DOR-RWB-ITG-DM003-ITG-20).

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Run JOB-04 reconciliation for the business date, with one Idempotency-Key (AC1, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/DP01/records?caseId={caseId}` | P1 rwb-source-data | The account rows that resolve account_key (AC1, AC2) |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | The party rows that resolve person_key (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time of the product (AC1) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case number, owner, queue and stage (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}/accounts` | P3 rwb-case | The account_key links, ACC-SYN-000601 and ACC-SYN-000777 (AC1, AC2) |
| GET | `/api/recovery/case/v1/cases/{caseId}/parties` | P3 rwb-case | The person_key link, PERS-SYN-000601 (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC4) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness triggers JOB-04 through the owner's operation, not through an event, and reads the result through the same contract rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04 reconciliation, the event-triggered reconciliation workflow on rwb-source-data (Architecture v5 slides 15 and 44), is exercised through its rerun operation. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. JOB-04 is event-triggered; the harness reruns it for the business date under test and sets no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the case and the links are P3's and the reconciliation result is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | The four P1 operations of §12.2 | DP01 returns one row for ACC-SYN-000601, DP02 returns one row for PERS-SYN-000601, freshness returns business date 2026-11-30 with a load time, and the rerun is accepted once per Idempotency-Key |
| Stub for rwb-case | `GET /cases/{caseId}`, `/accounts`, `/parties` | The case RW-2026-000601 with owner RW-OFF, queue MTG-BKK-CO and stage WITH_FCR_OFFICER; the account links ACC-SYN-000601 and ACC-SYN-000777; the party link PERS-SYN-000601 |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The case, its account and party links, the orphan account_key ACC-SYN-000777 on a case_account row of the case, and the source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row for case RW-2026-000601 with key type ACCOUNT, key value ACC-SYN-000777, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment, the fixture layout, the break-list fields and the evidence retention are Not specified in the source documents (GAP-0443; ASM-0635).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 8 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contract |
| Temporal | None added; JOB-04 reconciliation, the event-triggered workflow on rwb-source-data, is exercised |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The one blocking dependency is the I story RWB-P1-DM003-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the four owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The three stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic case, its account and party links and the orphan account_key, with source and migrated_at |
| KeyResolver | Service | Resolves every business key through DP01 and DP02 with the freshness read, and names each key that does not resolve |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a rerun |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic case RW-2026-000601, owner RW-OFF, queue MTG-BKK-CO, stage WITH_FCR_OFFICER, account_key ACC-SYN-000601, person_key PERS-SYN-000601, orphan account_key ACC-SYN-000777 and business date 2026-11-30. In SIT the records come from the cutover load of P3's own Flyway sequence (DP-15). The environment, the fixture layout, the break-list fields and the evidence retention are not specified in the source documents (GAP-0443; ASM-0635). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the three stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-11-30 (X2).
3. Build the JourneyRunner for AC1: trigger JOB-04 with one Idempotency-Key, read the case and its links through rwb-case, resolve account_key and person_key through DP01 and DP02 with the freshness read, and list each orphan (X5).
4. Add the KeyResolver assertion that every key on a migrated record resolves, and that each orphan is on the list for the data steward and the ACE team (X3).
5. Add BreakListAssertion for AC2: one row for case RW-2026-000601 with key type ACCOUNT, key value ACC-SYN-000777, reason NO_ACE_ROW and owner role RW-DATASTEW, the ACE team named as second owner in the report, and the case and links still readable through the rwb-case contract.
6. Add AC3: rerun JOB-04 for the same business date, assert one break row, equal counts of cases, account links and party links, and one report entry per business date (X4, X7).
7. Add the access path for AC4 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM003-APP when it lands, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's load has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

The legacy story has no screen, and neither does this harness: the breaks are listed on the reconciliation extract, which the data steward and the ACE team read as a file. The states the harness asserts on that extract are small: empty (no break row for the business date, and the report says zero breaks), loading (the run has not finished, so no extract is read), error (the run failed, and the report names the failure as in section 5) and no access (the caller lacks the Platform administration right and the run is refused as in X6, where MSG-P4-002 is expected and missing).

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of cases, account links and party links, and no break row |
| Break | One row per orphan with the case number, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. SCR-45 states are those of Screen Specifications v1; its empty, error and no access states are Not specified in the source documents (CG-ALL-979). The SCR-45 Data quality console is not part of this legacy key: it is the screen of RWB-AD-019 and this story neither builds it nor reads it. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0443; ASM-0635).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-003-01-ITG | AC1 (legacy); ITG AC1 | Integration | Synthetic case RW-2026-000601 with DP01 and DP02 rows present |
| TC-DM-003-02-ITG | AC2 (legacy); ITG AC1, ITG AC2 | Integration | One account_key ACC-SYN-000777 with no view row |
| TC-DM-003-03-ITG | AC3 (legacy, owned by RWB-P1-DM003-APP); ITG AC3 | Integration | Two JOB-04 runs for business date 2026-11-30 |
| TC-DM-003-04-ITG | Access; ITG AC4 | Component | RW-OFF caller without Platform administration R |
| TC-DM-003-05-ITG | BR3; ITG AC5 | Integration | Migrated case_account row for RW-2026-000601 with account_key ACC-SYN-000777 and no view row |
| TC-DM-003-06-ITG | BR5; ITG AC6 | Integration | Migrated case RW-2026-000601 from the cutover extract |
| TC-DM-003-07-ITG | BR6; ITG AC7 | Integration | Open case RW-2026-000601 with owner RW-OFF, queue MTG-BKK-CO and stage WITH_FCR_OFFICER |
| TC-DM-003-08-ITG | BR7; ITG AC8 | Integration | P3 cutover migration on its own Flyway sequence (DP-15) |
| TC-DM-003-09-ITG | BR4; ITG AC9 | Integration | Synthetic keys ACC-SYN-000601 and PERS-SYN-000601 |
| TC-DM-003-10-ITG | BR3; ITG AC10 | Integration | ACE read for account_key ACC-SYN-000601 with the rwb-source-data call failing or unanswered |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx under the same legacy test case ID.

### 17. Guardrails

- No business value in code: the synthetic keys, the business date, the fixture contents, the break reasons and the report layout are data.
- No personal data in logs, fixtures or reports: every key is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the case and the links come from rwb-case and the ACE side from the rwb-source-data contract (DP-01, DP-05).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-003 Migrate case and ownership | Recovery Workbench Data Migration Stories v4, lines 49 to 128 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 74 to 78 | Section 7, AC1, marked (legacy RWB-DM-003 AC2) |
| Legacy AC1 and AC3, and the four legacy test cases TC-DM-003-01 to TC-DM-003-04 | The same, lines 68 to 85 and 118 to 125 | AC1 and AC3 stay with RWB-P1-DM003-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-CAS-001 to DF-CAS-023, DF-CAS-046 to DF-CAS-055, DF-CAS-024 to DF-CAS-029, DF-CAS-030 to DF-CAS-035, DF-WRK-009 to DF-WRK-016, DF-WRK-039, DF-WRK-040 | Logical Data Model and Data Dictionary v9 | Section 11 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4; sections 12.2 and 12.8 |
| RWB-E1-011 Reconciliation and data quality report | Epic 1 story master; Build Notes Epic 1 v7 | Section 12.5, the JOB-04 reconciliation this harness exercises; its build and its screen RWB-AD-019 are out of scope |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM003-APP: the reconciliation, the break list and legacy AC1 and AC3. The cutover load of the records into `rwb_case` is P3's own Flyway sequence.
- P3 production code and its CON, APP and DB stories: the case contract and the tables are built there.
- The SCR-45 Data quality console (RWB-AD-019).
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration.
- The other four data migration keys of this wave.
