# RWB-ITG-DM005-ITG Migrate contact and promises

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM005-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-DM-005 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-DM005-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-005 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated contact and promise records resolves to its ACE view row, that the EFS history is read and never copied, and that every orphan is listed for the data steward and the ACE team, against the owning services' published contracts and their fakes**, so that **no promise a customer made is lost at cutover while the EFS history itself is read from ACE**.

This story builds a test harness and its evidence only. Legacy AC1 and AC2 are proved here; legacy AC3, the cut-over sign-off, stays with RWB-P1-DM005-APP, which also owns the rwb-source-data code, the REC-05 step, the per-service Flyway sequence that carries the cutover load (DP-15) and every migration write. The harness seeds nothing by hand: on Day 1 the stub set of section 12.8 returns the migrated records, and in SIT the cutover load of rwb-source-data's own Flyway sequence provides them, so a passed run means the owner's contract and its data are right and not that the harness wrote a row.

### 2. Business rationale

A promise date or a promise amount that disappears at cutover cannot be recovered afterwards: the customer keeps a commitment the bank no longer sees, the arrears strategy runs on a wrong date, and the officer opens the next call with no record of what was agreed. The second risk is the opposite one. If the EFS history is copied into the Workbench instead of read from the ACE views, the two stores drift and the bank holds a personal-data copy it cannot defend under a retention rule it does not own. The third is a contact point whose contact key has no ACE row: an orphan used anyway is a contact attempt on a record nobody can trace.

That is why the legacy criterion carries zero tolerance. DL25 sets zero tolerance for reconciliation breaks on the migrated data, and REQ-RDF-007 and REQ-RDF-008 require that every business key resolves to its ACE row and that every break is listed for the data product owner. The cutover is decoupled the way the target is: the harness reads the migrated records through rwb-source-data's contract and never a table (DP-05), the cutover load is the owner's own per-service Flyway sequence (DP-15), the evidence is the harness's own report and not a screen, every call is one hop with a 2 s budget (DP-11), and JOB-04 is triggered through the owner's rerun operation because it is an event-triggered workflow in rwb-source-data and not a shared job table.

The EFS history stays where ACE put it. DL29 keeps twelve months of it, read through v_ace_efs_action, so the Workbench holds the promise the customer made to us and ACE holds the contact history that was always ACE's, and no copy of either drifts.

### 3. Preconditions

- The rwb-source-data contract is published with the data product record reads of DP02 and DP05, the freshness read, the JOB-04 rerun operation and the interaction read, and a WireMock stub set is generated from it.
- The P3 rwb-case contract is published with the case read, and its stub set is generated from it.
- The data product catalog holds DP02 Customer and party and DP05 Contact and promises with ACE named as the system of record, and DP05 names v_ace_efs_action, v_ace_efs_action_code and v_ace_efs_assignment as the ACE reads (FSD P1 v3).
- RWB-P1-DM005-APP is the integration dependency and is not required on Day 1: until it lands the harness runs against the stub set, and the run report says so. In SIT the cutover load of rwb-source-data's own Flyway sequence (DP-15) has carried the migrated contact and promise records for the business date under test.
- The harness environment and its base hosts, the synthetic cutover extract fixture and its field layout, the reconciliation extract format and its retention, the pass or fail gate and the data seeding set are: Not specified in the source documents (GAP-0445; ASM-0637).
- The harness runs in SIT only, with a report per business date, and it opens no schema and no ACE view: Not specified in the source documents (GAP-0445; ASM-0637).
- No build dependency. Day 1, with the fakes in place from the first run, and the stub replaced by the real owner as RWB-P1-DM005-APP lands.

### 4. Flow

1. Harness: builds the run fixture and the stub set. On Day 1 the section 12.8 stubs return the migrated records; in SIT the cutover load of rwb-source-data's own Flyway sequence (DP-15) has already provided them, and the harness seeds nothing by hand.
2. Harness: triggers JOB-04 for business date 2026-11-30 through `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` on the owner's base, one hop with one Idempotency-Key, and never a Schedule or a job table of its own (DP-11).
3. Harness: reads interaction `INT-0605` and its promise facts through `GET /api/recovery/source-data/v1/cases/{caseId}/interactions` on case `RW-2026-000605`, and asserts the case, person_key `PERS-SYN-0605`, contact_key `CP-SYN-0605`, promise date 2026-12-15 and promise amount 12500 are the ones the cutover extract holds.
4. Harness: reads the case through `GET /api/recovery/case/v1/cases/{caseId}` on rwb-case and asserts the case number, stage and primary person key, so the migrated record points at a case the owner serves.
5. Harness: resolves the person key and the contact key through `GET /api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}`, and reads the promise and the EFS history through `GET /api/recovery/source-data/v1/data-products/DP05/records?caseId={caseId}` with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP05`, one hop each with a 2 s budget.
6. Harness: asserts that no EFS contact or promise row is copied. The EFS history is read from v_ace_efs_action, the DP05 record names its source and its migration date, and the interaction ledger holds no row that mirrors an EFS action.
7. Harness: reads the break list from the reconciliation extract for business date 2026-11-30, which is where the legacy story says the breaks are listed, and asserts one row for interaction `INT-0605` with key type CONTACT, key value `CP-SYN-0777`, reason `NO_ACE_ROW` and owner role `RW-DATASTEW`, and that no contact was attempted on that contact point.
8. Harness: reruns JOB-04 for the same business date with a second Idempotency-Key, then compares the counts of interactions and of their promise links with the first run and asserts the break list holds exactly one row for `CP-SYN-0777`, and that the run report holds one entry per business date and not one per run.
9. Harness: calls the reconciliation run as the RW-OFF caller and asserts 403 with MSG-P4-002, no run started and no break row written, then publishes the report of the business date with the four criteria, their assertions, the contract versions and whether each hop was a stub or the owner.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version | None | AC1, AC2 |
| X2 | The cutover extract fixture lacks a required key: case, person_key, contact_key, promise date or promise amount | The run fails before any assertion and the report names the field and the fixture row | None | AC1 |
| X3 | A key with no ACE view row is not listed on the reconciliation extract | The run fails on AC2 and AC3 and the report names the key and the business date | None | AC2, AC3 |
| X4 | A break row is listed twice after the rerun | The run fails on AC4 and the report names the break row and both run identifiers | None | AC4 |
| X5 | JOB-04 refuses to run because the DP05 freshness is late | The run is reported as not started, no break row is written, and the report names the product and its data date | MSG-P1-001 | AC1, AC2 |
| X6 | An EFS row appears in the interaction ledger as a copy | The run fails on AC1 regardless of the promise facts, and the report names the ledger row | None | AC1 |
| X7 | A caller without the Platform administration right starts a run anyway | The run fails on AC5 and the report names the caller role and the operation | MSG-P4-002 | AC5 |

The report text is for the wave entry check and is not part of the message standard. The messages in section 14 are asserted as the answers of the owning service, not produced by the harness.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against published contracts and fakes from Day 1; its only wait is RWB-P1-DM005-APP, and each criterion runs before and after it lands |
| Negotiable | The fixtures, the break-list read and the report shape are configuration and agreed at the wave entry check, not business values in code |
| Valuable | The proof that no promise is lost and no EFS history is copied at cutover, which no single service story can show |
| Estimable | One journey runner, one stub set, two fixtures, one key resolver, one break-list assertion and one report |
| Small | Fits in one sprint with its four test cases |
| Testable | Each criterion is one automated test against the fakes and again against the real owner |

### 7. Acceptance criteria

```gherkin
Feature: Migrate contact and promises - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds open promise "INT-0605" on case "RW-2026-000605" with person_key "PERS-SYN-0605", contact_key "CP-SYN-0605", promise date "2026-12-15" and promise amount "12500"
    Given the ACE EFS view holds contact history for person_key "PERS-SYN-0605"
    Given JOB-04 has run for business date "2026-11-30"

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-005 AC1)
    Given the open promises and contact notes that the legacy Workbench holds outside EFS, with their case numbers
    When the migration reads them
    Then each interaction keeps its case, its person_key, its contact_key, its promise date and its promise amount
    And no EFS contact or promise row is copied, because the history is read from v_ace_efs_action

  Scenario: AC2 Reconcile the business keys (legacy RWB-DM-005 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC3 An orphan contact key is listed and no contact is attempted (new, D-RCV-60)
    Given migrated interaction "INT-0605" carries contact_key "CP-SYN-0777"
    And the ACE contact view holds no row for contact_key "CP-SYN-0777"
    When the harness reads the reconciliation result for business date "2026-11-30"
    Then the break list holds one row for interaction "INT-0605" with key type "CONTACT" and key value "CP-SYN-0777"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And no contact is attempted on the orphan contact point
    And the interaction stays readable through the rwb-source-data contract

  Scenario: AC4 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When JOB-04 is rerun for the same business date
    Then the break list holds exactly one row for contact_key "CP-SYN-0777"
    And the counts of interactions and their promise links equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC5 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When the harness calls the reconciliation run for business date "2026-11-30"
    Then the answer is 403 with "MSG-P4-002"
    And no reconciliation run starts and no break row is written
```

Legacy AC3 belongs to RWB-P1-DM005-APP, and the five criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated contact or promise record resolves to its ACE view row, account_key and person_key included | REQ-RDF-007; DL25 |
| BR2 | Every break is listed for the data steward and the ACE team, with the key type, the key value, the reason and the owner role | REQ-RDF-008 |
| BR3 | Zero tolerance: one orphan on the migrated data is a break and is never waived | DL25 |
| BR4 | ACE data is read only through the views and the contract owned by rwb-source-data, and no service or harness reads an ACE view directly | D-RCV-35; ADR-010 |
| BR5 | The EFS history is read from v_ace_efs_action and never copied, so the Workbench holds the Workbench promise and ACE holds the EFS history | DL29; legacy RWB-DM-005 AC1 |
| BR6 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | legacy RWB-DM-005 guardrails |
| BR7 | The cutover load is the per-service Flyway sequence of the owning service and no other load path exists | DP-15 |

### 9. State transitions

The harness changes no state. The interaction keeps its promise date 2026-12-15 and its promise amount 12500 before, during and after every run, and the case keeps its stage and its primary person key. An orphan contact point stays readable through the rwb-source-data contract and is listed on the reconciliation extract; a listed orphan that later resolves to an ACE row is no longer listed, because the owner's REC-05 step resolves it and the harness only reads the result. P1 owns every state change in this story: the cutover load writes the migrated records in its own schema through its own Flyway sequence, JOB-04 writes the reconciliation result and the break rows, and rwb-case serves the case it already holds. The harness reads those states and sets none of them.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward and data product owner | Reads the break list and the run report (Platform administration R); signs the reconciliation of the business date |
| RW-COE, centre of excellence | Reads the break list and the report (Platform administration R) |
| RW-AUDIT, internal audit | Reads the break list, the report and the run evidence (Platform administration R) |
| RW-COMPLY, compliance | Reads the break list and the report (Platform administration R) |
| RW-PLATADM, platform administrator | Reads the break list and restarts the run for a business date (Platform administration R) |
| RW-SECADM, security administrator | Reads the run evidence (Platform administration R) |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real owner |
| P1 rwb-source-data identity | Serves the data product records, the freshness, the interactions and the JOB-04 rerun, and owns every migration and reconciliation write |
| P3 rwb-case identity | Serves the case, its stage and its primary person key |

No role outside the six above reads the break list: a caller with role RW-OFF and no Platform administration right is refused with MSG-P4-002. No level of the delegation of authority applies, because the harness takes no business decision.

### 11. Data

| BR Field ID | Entity | Owning schema | Field | Read or write |
|---|---|---|---|---|
| DF-CAS-001 to DF-CAS-055 | recovery_case | rwb_case (P3) | all fields, case_no, primary_person_key and stage_code included | Read through the rwb-case contract |
| DF-INT-001 to DF-INT-029 | interaction | rwb_source_data (P1) | all fields, case_id, person_key, contact_key, promise date and promise amount included | Read through the rwb-source-data contract |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | rwb_source_data (P1) | all fields, contact_key and contact_type included | Read through the rwb-source-data contract |
| Standard column | interaction, recovery_case, contact_point_ext | the owner's schema | source, migrated_at | Read through the owner's contract |

DP02 Customer and party holds v_ace_customer and v_ace_contact for the person_key and the contact_key, and DP05 Contact and promises holds v_ace_efs_action, v_ace_efs_action_code, v_ace_efs_assignment and interaction (FSD P1 v3). The harness owns no table and writes no row: it reads the records through rwb-source-data's contract and the case through rwb-case's contract (DP-01, DP-05). The EFS history is twelve months of ACE data read through the views under DL29, and the harness asserts it is read and never stored. The synthetic promise amount 12500 is the monthly instalment of the worked example in the Temporal and Drools design, used as a fixture value and not as a business parameter.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Trigger JOB-04 for the business date under test, and the rerun of AC4, each with one Idempotency-Key |
| GET | `/api/recovery/source-data/v1/data-products/DP02/records?caseId={caseId}` | P1 rwb-source-data | Resolve the person_key and the contact_key against v_ace_customer and v_ace_contact (AC2) |
| GET | `/api/recovery/source-data/v1/data-products/DP05/records?caseId={caseId}` | P1 rwb-source-data | Read the promise and the EFS history of the case (AC1, AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP05` | P1 rwb-source-data | The data date of DP05 before the run, and the late-batch refusal of X5 |
| GET | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | The migrated interaction INT-0605 and its promise date and amount (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case, its stage and its primary person key (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Role, scope and Platform administration right for every call, including the refusal of AC5 |

Every operation is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget and a circuit breaker per downstream (DP-11, DP-13). This legacy key has no screen, so no gateway-bff composite route is called: DP-19 is recorded for the wave's screen path only. No operation is invented in this story, and none of them is a table read or a view read.

#### 12.3 Events published

None. The harness publishes no Kafka event; it reads the owner's answer and writes its report to the wave record.

#### 12.4 Events consumed

None. JOB-04 is triggered through the owner's rerun operation and not by publishing AceDataReady; the event-triggered start of JOB-04 is the behaviour RWB-P1-DM005-APP owns, and the harness asserts the result and not the trigger.

#### 12.5 Workflows and activities

None added. The harness exercises the existing JOB-04 reconciliation workflow and its REC-05 step on the owner's task queue `rwb-source-data` and asserts their effects through the owner's contract; no workflow, activity or task queue is created, changed or owned by this story.

#### 12.6 Schedules

None added. JOB-04 is event-triggered in rwb-source-data, and the harness reruns it for a business date through the owner's operation, so no cron, overlap policy or catch-up window is set by this story.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); `interaction` and `contact_point_ext` are rwb-source-data's, `recovery_case` is rwb-case's, and the harness reads every one of them through the owning contract.

#### 12.8 Contract fakes

| Fake | Contract | Use in the run |
|---|---|---|
| WireMock stub for rwb-source-data | The JOB-04 rerun, the DP02 and DP05 record reads, the DP05 freshness read and the interaction read | Day-1 run of AC1 to AC5 before RWB-P1-DM005-APP is live |
| WireMock stub for rwb-case | `GET /cases/{caseId}` | Day-1 assertion on the case, its stage and its primary person key |
| WireMock stub for rwb-access | `POST /authorise` | Day-1 authorisation and the refusal path of AC5 |
| Cutover extract fixture | The synthetic extract of the open promises and contact notes held outside EFS | The migrated records the harness expects on case RW-2026-000605, with the orphan contact key CP-SYN-0777 |
| Reconciliation extract fixture | The break list of the business date | The one-row break list of AC3 and the one-row rerun of AC4 |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and its base hosts, the cutover extract fixture and its field layout, the reconciliation extract format and its retention, the pass or fail gate and the data seeding set are: Not specified in the source documents (GAP-0445; ASM-0637).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13); no screen composes this answer |
| Kafka | None published and none consumed; JOB-04 is triggered through the owner's operation |
| Temporal | None added; the JOB-04 reconciliation workflow and its REC-05 step are exercised on queue `rwb-source-data` |
| File | The cutover extract fixture and the reconciliation extract fixture, both synthetic and both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are delivered by the platform waves and are not repeated in the metadata H field of this story, which stays empty. The one blocking dependency is the I story RWB-P1-DM005-APP; until it lands the run uses the stub set and the report says so.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the five criteria in order for a business date, holds the run lock and writes one report per business date |
| StubSet | Fake | The three WireMock stubs generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic extract of the open promises and contact notes, with the case, person_key, contact_key, promise date and promise amount of the criteria and the orphan contact key |
| ContactKeyResolver | Service | Resolves the person_key and the contact_key through DP02 and reads the promise and the EFS history through DP05 with its freshness |
| BreakListAssertion | Service | Reads the reconciliation extract and asserts the break rows, their key type, their key value, their reason and their owner role |
| EvidenceReport | Service | Writes the per-run report keyed by story and business date, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real owner as RWB-P1-DM005-APP lands, on case `RW-2026-000605`, interaction `INT-0605` with person_key `PERS-SYN-0605`, contact_key `CP-SYN-0605`, promise date 2026-12-15 and promise amount 12500, the orphan contact_key `CP-SYN-0777` and business date 2026-11-30. Seeding is the cutover load of the owner's Flyway sequence, never a schema write by the harness. The environment, the fixture field layout, the extract format and the evidence retention are not specified in the source documents (GAP-0445; ASM-0637).

**Build steps**

1. Generate the three stubs from the published contracts and pin each contract version in the run report; fail the run on a version mismatch (X1).
2. Build the CutoverExtractFixture with the synthetic values of section 13 and the required-key check of X2.
3. Build the JourneyRunner for AC1: trigger JOB-04 with one Idempotency-Key, read interaction INT-0605 and the case, and assert the case, person_key, contact_key, promise date and promise amount (X2).
4. Add the ContactKeyResolver over DP02 and DP05 with the DP05 freshness read, and assert that no EFS row is in the ledger and that the source and migration date are present (X6, X5).
5. Add the BreakListAssertion for AC2 and AC3: every key resolves, and the orphan CP-SYN-0777 is listed once with key type CONTACT, reason NO_ACE_ROW and owner role RW-DATASTEW (X3).
6. Add the AC4 rerun with a second Idempotency-Key, the count comparison and the one-entry-per-business-date check (X4).
7. Add the AC5 access path through `POST /api/recovery/access/v1/authorise` with the 403 and MSG-P4-002 refusal, then the EvidenceReport and the gate, and rerun the five criteria against the real owner when RWB-P1-DM005-APP lands (X7).

**Feature switch.** None. The harness runs behind no feature switch, and it reads no flag of its own.

**Done when.** The four test cases of section 16 pass against the three stubs on Day 1 and again against RWB-P1-DM005-APP when it lands; the break list holds one row for the orphan; the rerun is deterministic; and the wave entry check holds a run report keyed by story and business date with the contract versions and whether each hop was a stub or the owner.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-001 | The DP05 freshness is late, so JOB-04 refuses the run | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | A fixture row lacks a required field | Enter {field}. |
| MSG-P4-002 | A caller without the Platform administration right asks for the run | You cannot {action} here. Your role does not include it. |

The harness produces none of these messages itself; it asserts the message the owning service returns and names the message ID in the report, so a failure points at a service and a message and not only at a date.

### 15. Screens and states

The legacy story has no screen, and the harness renders none. What the wave entry check reads instead is the reconciliation extract for the business date, whose states are these:

| State | What the extract shows |
|---|---|
| No break | No row for the business date, and the run report records the counts of interactions and promise links that were checked |
| Break | One row per orphan: the interaction, the key type, the key value, the reason NO_ACE_ROW and the owner role RW-DATASTEW |

The SCR-45 data quality console is not part of this legacy key and is not read by this harness; the breaks reach the data steward and the ACE team through the reconciliation extract the legacy story names. The extract format, its retention and the report shape are not specified in the source documents (GAP-0445; ASM-0637).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-005-01-ITG | AC1 (legacy); ITG AC1 | Integration | Open promise INT-0605 outside EFS with DP02 and DP05 rows present |
| TC-DM-005-02-ITG | AC2 (legacy); ITG AC1, ITG AC2, ITG AC3 | Integration | One contact_key CP-SYN-0777 with no view row |
| TC-DM-005-03-ITG | AC3 (legacy, owned by RWB-P1-DM005-APP); ITG AC4 | Integration | Two JOB-04 runs for business date 2026-11-30 |
| TC-DM-005-04-ITG | Access; ITG AC5 | Component | RW-OFF caller without Platform administration R |

The integration cases above are the ITG copies of the four legacy cases of the same number and carry the legacy data unchanged; the access copy keeps the legacy component level and the legacy right. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the promise dates and amounts, the reasons, the owner roles and the fixture values are data and SIT configuration, never constants of the harness.
- No personal data in logs, fixtures or reports: the contact values never appear, the fixtures are synthetic keys, and the report names identifiers and counts only.
- No cross-schema read and no direct view read: every field comes through the owning service's contract (DP-01, DP-05), and only rwb-source-data reads recovery.v_ace_* (ADR-010, D-RCV-35).
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real-service pass: the report names the contract version and whether each hop was a stub or the owner.
- The harness never runs against UAT or production, and it never seeds a migrated record, sets a break row or resolves an orphan by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script (DL25).

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-005 Migrate contact and promises | 04 User stories/Recovery Workbench Data Migration Stories v3.md | This story, sections 1 to 19 |
| Legacy AC1: "Given the open promises and contact notes that the legacy Workbench holds outside EFS, with their case numbers. When the migration reads them. Then each interaction keeps its case, its person_key, its contact_key, its promise date and its promise amount. And no EFS contact or promise row is copied, because the history is read from v_ace_efs_action." | RWB-DM-005 AC1 | AC1 above; TC-DM-005-01-ITG |
| Legacy AC2: "Given the migrated records. When the REC-05 step runs. Then every business key on a migrated record resolves to its view row, account_key and person_key included. And each orphan is listed for the data steward and the ACE team." | RWB-DM-005 AC2 | AC2 above; TC-DM-005-02-ITG |
| TC-DM-005-01, TC-DM-005-02, TC-DM-005-03, TC-DM-005-04 | RWB-DM-005 test cases | Carried as the -ITG copies of section 16 |
| DF-CAS-001 to DF-CAS-055, DF-INT-001 to DF-INT-029, DF-EXT-013 to DF-EXT-026 | Logical Data Model and Data Dictionary | Section 11 |
| DL25, zero tolerance for reconciliation breaks on migrated data | Decision Log | BR1, BR3, AC2, guardrails |
| DL29, twelve months of EFS history read from ACE | Decision Log | BR5, section 11 |
| D-RCV-35, ACE data only through the owner's views and contract | Decision Log | BR4, section 17 |
| ADR-010, only rwb-source-data reads the ACE views | Architecture Decision Records | BR4, section 12.2 |
| RWB-E1-011, the reconciliation and data quality report of JOB-04 and REC-05 | Legacy story RWB-E1-011 | Flow steps 7 and 8, AC2, AC3, AC4 |
| DP-05, DP-15, DP-19 | Template and Rules v1 §R5.5 | Section 13, metadata Patterns applied |

### 19. Out of scope

- RWB-P1-DM005-APP and the cutover load: the extract, the REC-05 step, the reconciliation result, the break rows and legacy AC3, the cut-over sign-off.
- P1 production code and its CON, APP and DB stories, and the per-service Flyway sequence that owns the load (DP-15).
- The SCR-45 data quality console (RWB-AD-019) and every screen state.
- The cutover plan, the go or no-go decision and the sign-off of the business date.
- ACE ingestion, the views themselves and the EFS history beyond twelve months (RWB-ACE-001, DL29).
- Platform configuration, the SIT environment build and the pipeline stage that runs the harness.
- The other data migration keys RWB-DM-001 to RWB-DM-004 and RWB-DM-006 onwards.
