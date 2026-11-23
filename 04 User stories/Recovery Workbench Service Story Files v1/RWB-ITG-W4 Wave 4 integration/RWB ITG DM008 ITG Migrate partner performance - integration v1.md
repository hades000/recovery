# RWB-ITG-DM008-ITG Migrate partner performance

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-DM008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W4 |
| Wave | 4 |
| Business epic | EP08 |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-DM-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP05, DP15, DP19 |
| Parallel lane | L-ITG-W4 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-DM008-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (no FR mapped to no REQ IDs) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-DM-008 for the wave 4 cutover reconciliation harness. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **data steward**, I want **a repeatable wave 4 cutover reconciliation harness that proves every business key on the migrated partner, partner user and partner instruction records resolves through rwb-source-data's data-product contract and lists every orphan with its reason and two owners, against the owning services' published contracts and their fakes**, so that **panel status and performance continue across cutover from the first day after it**.

This story builds the harness and the evidence, and nothing else. The real firms, their users and their instructions are loaded by P1's own cutover migration on its own Flyway sequence (DP-15), and the reconciliation that produces the breaks is RWB-P1-DM008-APP's. The story is a test package and is not part of any deployed service: it builds no production endpoint, no table, no workflow, no schedule and no screen; it reads the owning services' published contracts, asserts what they answer, and writes one report per business date.

### 2. Business rationale

A panel firm served on the first day with a partner_code, an identity_ref or an instruction case that resolves to no row loses the panel status and the performance that the recovery process routes on. The panel offers work to a firm that the record no longer evidences, the instruction moves with a case that nobody can open, and the score behind the ranking points at a firm the ACE views do not hold. The failure is quiet: the cutover load can report a clean run while the keys it wrote point at rows that the views do not hold, and a break that nobody lists is a silent data loss that surfaces weeks later as a misplaced instruction or a wrong panel measure. DL25 puts zero tolerance on that, so the migrated partner, partner user and partner instruction records are proven before the cutover is called done, and every orphan is on a list with a reason and two owners.

The harness is decoupled the way the services are. ACE data is read only through rwb-source-data's data-product contract (DP-05), never from another service's schema and never by a direct view read (DP-01); the panel firms and their instructions are read from rwb-partner, which owns partner, partner_user and partner_instruction; the case behind an instruction is read from rwb-case, which owns recovery_case; the cutover load runs on P1's own Flyway sequence (DP-15); where a screen exists the path is the gateway-bff composite route (DP-19), and the legacy story names the SCR-45 Data quality console, which this harness neither builds nor calls, so it renders no screen; every call is one hop on `/api/recovery/<short>/v1` with a 2 s budget (DP-11). It carries REQ-RDF-007, REQ-RDF-008 and DL25 into evidence rather than restating them.

### 3. Preconditions

- The published contracts of S9 rwb-partner (partners and instructions), P3 rwb-case (case), P1 rwb-source-data (DP01, DP02, freshness and the JOB-04 rerun) and P4 rwb-access (authorise) are in the contract registry, and a stub set is generated from each one.
- The data product catalog holds DP01 Account and arrears and DP02 Customer and party, each with one system of record, so person_key and account_key have one named owner before a key is resolved (FSD P1 v3, A2.2).
- The cutover load of P1's own Flyway sequence (DP-15) has run in SIT for the business date under test, or the stub of §12.8 answers in its place on Day 1.
- RWB-P1-DM008-APP owns the reconciliation and the break list; until it lands, the reconciliation extract fixture stands in for its output.
- The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, and the pass or fail gate with its seeding set: Not specified in the source documents (GAP-0448; ASM-0640).
- The synthetic firm, the synthetic users, the synthetic instruction, the field values and the business date are held in the fixture as data, not written in code.
- No build dependency. Day 1, with the stubs in place from the first run; the one wait is RWB-P1-DM008-APP, which replaces its stub and never blocks the lane.

### 4. Flow

1. Harness: loads the cutover extract fixture for business date 2026-11-30: panel firm "PART-SYN-0008" with partner_name, partner_type, panel_status, contract_end and score, its user with identity_ref "PERS-SYN-000808", role_code, valid_from and valid_to, its second user with identity_ref "PERS-SYN-000818", and the instruction "INS-SYN-0008" on case "RW-2026-000801" with instruction_type, instructed_at, due_at and its result. On Day 1, before the cutover load is in SIT, the stub of §12.8 returns the same records.
2. Harness: triggers JOB-04 reconciliation on rwb-source-data with one Idempotency-Key per business date, through `POST /api/recovery/source-data/v1/admin/jobs/JOB-04/rerun`.
3. Harness: reads the panel firms through `GET /api/recovery/partner/v1/partners` and asserts partner_code, partner_name, partner_type, panel_status, contract_end and score against the fixture.
4. Harness: reads the instructions through `GET /api/recovery/partner/v1/partner/instructions` and asserts instruction_type, instructed_at, due_at and result, and that each instruction names its case.
5. Harness: reads the case behind the instruction through `GET /api/recovery/case/v1/cases/{caseId}` and asserts the case number against the fixture.
6. Harness: resolves each business key through `GET /api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}`, person_key from identity_ref through DP02 and account_key from the instruction's case through DP01, with `GET /api/recovery/source-data/v1/data-products/freshness?product=DP01` for the business date and the load time, and names each key that does not resolve.
7. Harness: reads the break list from the reconciliation extract fixture for the business date, with one row per orphan and its reason; the legacy story states that the breaks are listed on the reconciliation extract and that there is no screen.
8. Harness: asserts that no case record is duplicated and that no settlement figure sits on a migrated instruction record or in the cutover extract, and names the instruction and the field where one does.
9. Harness: reruns JOB-04 for the same business date with the same Idempotency-Key and compares the break list and the counts of firms, partner users, instructions and break rows with the first run.
10. Harness: calls `POST /api/recovery/access/v1/authorise` as a synthetic caller with role RW-OFF and no Platform administration right, and asserts 403 with MSG-P4-002, no reconciliation run started and no break row written.
11. Harness: writes one run report per business date, keyed by story and business date, naming the contract version of each hop, whether the hop was a stub or the owner, the counts, the break rows and the five criteria.

### 5. Exception paths

| ID | Trigger | What the harness asserts | Message | ITG test case |
|---|---|---|---|---|
| X1 | A stub answers a shape the published contract does not allow | The run fails at that hop and the report names the service, the operation and the contract version; no criterion is marked passed | None | TC-DM-008-01-ITG (ITG AC1) |
| X2 | The cutover extract fixture lacks a required key on a migrated firm, user or instruction | The run fails and the report names the record and the missing field; a record without a key is never reported as reconciled | None | TC-DM-008-01-ITG (ITG AC1) |
| X3 | A key has no view row and the extract does not list it | The run fails on AC2 and the report names the firm, the key type and the key value, so a suppressed break is a failure and not a pass | None | TC-DM-008-02-ITG (ITG AC2) |
| X4 | A rerun lists the same break twice | The run fails on AC4 and the report names the two rows and the business date | None | TC-DM-008-03-ITG (ITG AC4) |
| X5 | JOB-04 is refused because the ACE batch is late | The run fails before any assertion and the report names the product, the date and the message; a stale product is never treated as an empty result | MSG-P1-001 | TC-DM-008-01-ITG (ITG AC1) |
| X6 | A caller without the Platform administration right starts a run | The run fails on AC5 and the report names the caller role and the operation; a run that started is reported as started | MSG-P4-002 (expected, and missing) | TC-DM-008-04-ITG (ITG AC5) |
| X7 | The counts the owner returns disagree with the extract | The run fails on AC4 and the report names each count and its two values | None | TC-DM-008-03-ITG (ITG AC4) |
| X8 | A case record is duplicated, or a settlement figure appears on an instruction record or in the extract | The run fails on AC1 and the report names the instruction, the field and the view that owns the value; a copied figure is never reported as a pass | None | TC-DM-008-01-ITG (ITG AC1) |

The report text is for the wave entry check and is not part of the message standard. The business messages the run touches are in section 14 and are asserted by ID and by their substituted values.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Runs against the published contracts and the stubs from Day 1; the only wait is RWB-P1-DM008-APP, and its stub answers until it lands |
| Negotiable | The fixture layout, the break-list fields, the report shape and the gate are configuration agreed at the wave entry check, not business values in code |
| Valuable | The migrated partner, partner user and partner instruction keys are proven, no case is duplicated and no settlement figure is read, and every orphan is on a list with two owners before wave 4 opens |
| Estimable | One runner, one stub set, two fixtures, one key resolver, one no-copy assertion, one break-list assertion and one report |
| Small | Fits in one sprint with its four tests |
| Testable | Each criterion runs against the stubs and again against the real owner as the I story lands |

### 7. Acceptance criteria

```gherkin
Feature: Migrate partner performance - wave 4 cutover reconciliation harness

  Background:
    Given the synthetic cutover extract holds panel firm "PART-SYN-0008" with its panel_status, contract_end and score
    Given the firm's partner user carries identity_ref "PERS-SYN-000808" with a role_code, valid_from and valid_to
    Given the firm's instruction "INS-SYN-0008" names case "RW-2026-000801"
    Given the ACE views hold one row for person_key "PERS-SYN-000808"
    Given JOB-04 has run for business date "2026-11-30"

  Scenario: AC1 Extract the Workbench records (legacy RWB-DM-008 AC1)
    Given the legacy Workbench partner, partner user and partner instruction records at cutover
    When the migration reads them
    Then each firm keeps its panel status, its contract end and its score, each user its role and its dates, and each instruction its case and its result
    And no case record is duplicated and no settlement figure is read by the migration

  Scenario: AC2 Reconcile the business keys (legacy RWB-DM-008 AC2)
    Given the migrated records
    When the REC-05 step runs
    Then every business key on a migrated record resolves to its view row, account_key and person_key included
    And each orphan is listed for the data steward and the ACE team

  Scenario: AC3 An orphan identity_ref is listed with its reason and its two owners (new, D-RCV-60)
    Given a migrated partner_user record on firm "PART-SYN-0008" carries identity_ref "PERS-SYN-000818"
    And the ACE views hold no row for person_key "PERS-SYN-000818"
    When the harness reads the reconciliation result for business date "2026-11-30"
    Then the break list holds one row for firm "PART-SYN-0008" with key type "PERSON" and key value "PERS-SYN-000818"
    And the row names the reason "NO_ACE_ROW" and the owner role "RW-DATASTEW"
    And the migrated firm and its instructions stay readable through the rwb-partner contract
    And the run report names the ACE team as the second owner of the break

  Scenario: AC4 A repeated run is deterministic and one break is listed once (new, D-RCV-60)
    Given the reconciliation for business date "2026-11-30" has run once
    When JOB-04 is rerun for the same business date
    Then the break list holds exactly one row for identity_ref "PERS-SYN-000818"
    And the counts of firms, partner users, instructions and break rows equal the first run
    And the run report holds one entry per business date and not one per run

  Scenario: AC5 A caller without the platform administration right is refused (new, D-RCV-60)
    Given a synthetic user with role "RW-OFF" and no Platform administration right
    When the harness calls the reconciliation run for business date "2026-11-30"
    Then the answer is 403 with "MSG-P4-002"
    And no reconciliation run starts and no break row is written
```

Legacy AC3 Cut over belongs to RWB-P1-DM008-APP, and the five criteria above are the ones this ITG story owns.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every business key on a migrated firm, partner user or instruction resolves to its view row before the record is served | REQ-RDF-007; DL25 |
| BR2 | Every break is listed with a reason the data product owner can see, and no break is suppressed | REQ-RDF-008 |
| BR3 | Zero tolerance holds the publish: wave 4 does not open while one migrated record has an unresolved key | DL25 |
| BR4 | ACE data is read only through the recovery.v_ace_* views owned by rwb-source-data, and never copied | D-RCV-35; ADR-010 |
| BR5 | A migrated record keeps its source and its migration date, and never a copy of an ACE row | Legacy RWB-DM-008 guardrail; D-RCV-35 (U1) |
| BR6 | A firm keeps its panel status, its contract end and its score, each user its role and its dates, and each instruction its case and its result, with no case duplicated and no settlement figure read | Legacy RWB-DM-008 AC1; DL25 |
| BR7 | Each service applies its own Flyway sequence in its own schema | DP-15; ADR-021 |

The harness asserts these rules and changes none of them.

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| The panel status of the firm as migrated | Reconciliation for the business date with every key resolved | JOB-04 completes and every partner_code, identity_ref and instruction case has a DP01 or DP02 row | The same panel status, unchanged |
| The panel status of the firm as migrated | Reconciliation for the business date with one orphan | identity_ref PERS-SYN-000818 has no DP02 row | The same panel status, unchanged, and the orphan is listed |
| A panel status with a listed orphan | A listed orphan resolves and is reconciled | A DP02 row appears for the key and JOB-04 is rerun for the same business date | The break is no longer listed; the panel status is unchanged |

The harness changes no state. Every change in the table is made by the owner: S9 rwb-partner holds the firm, its users, its instructions and their results, and P1 rwb-source-data writes the reconciliation result and the break list. The harness reads, asserts and reports; a state it had set by hand would prove nothing, so the report names the owner and the operation behind every value it asserts.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-DATASTEW, data steward | Runs and reads the reconciliation for a business date; holds Platform administration R; owns the break list with the ACE team |
| RW-COE, RW-AUDIT, RW-COMPLY, RW-PLATADM, RW-SECADM | Read the same reconciliation evidence; each holds Platform administration R |
| QA lead | Owns the harness configuration, the fixtures, the report shape and the pass or fail gate |
| Integration lead | Owns the harness code, the stub set and the swap from a stub to the real service |
| The owning services' identities | P1 rwb-source-data runs JOB-04 and writes the reconciliation result, S9 rwb-partner holds the panel, the partner users, the instructions and their results, P3 rwb-case holds the case, and P4 rwb-access answers the authorisation; they make every change the harness asserts |
| No delegation of authority level applies | The harness takes no business decision; authorisation is answered by rwb-access |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PRT-001 to DF-PRT-007 | partner | partner_code, partner_name, partner_type, panel_status, contract_end, score | Read through the rwb-partner contract |
| DF-REF-212 to DF-REF-217 | partner_user | identity_ref, partner_id, role_code, valid_from, valid_to | Read from the cutover extract fixture; the identity_ref resolves through the rwb-source-data contract |
| DF-PRT-008 to DF-PRT-016 | partner_instruction | case_id, partner_id, instruction_type, instructed_at, due_at, result | Read through the rwb-partner contract |
| DF-CAS-001 to DF-CAS-055 | recovery_case | case_no, status, stage_code | Read through the rwb-case contract |
| Standard column | partner, partner_user, partner_instruction | source, migrated_at | Read through the rwb-partner contract and the cutover extract fixture |

Field IDs are those in the Logical Data Model and Data Dictionary v8. The three partner tables are S9's and the harness reads them only through the rwb-partner contract; partner_user is proven from the cutover extract fixture because the published contract of this wave exposes the panel and the instructions, and the fixture is the migrated record under test. The case is P3's and is read through the rwb-case contract. The ACE side of the keys is DP01 Account and arrears for account_key and DP02 Customer and party for person_key, read through the rwb-source-data data-product contract (FSD P1 v3, lines 283 and 284), never from a view and never from a table. The settlement figure is not on a migrated instruction record and is not read: it stays with the ACE view that owns it. The harness owns no table and writes no row.

### 12. Contract

#### 12.1 REST operations provided

None. The harness is a test runner and provides no REST operation.

#### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/partner/v1/partners` | S9 rwb-partner | partner_code, partner_name, partner_type, panel_status, contract_end and score of each panel firm (AC1, AC2) |
| GET | `/api/recovery/partner/v1/partner/instructions` | S9 rwb-partner | The instructions with their case, their dates and their result (AC1, AC3) |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The case behind an instruction (AC1) |
| GET | `/api/recovery/source-data/v1/data-products/{productCode}/records?caseId={caseId}` | P1 rwb-source-data | The DP01 and DP02 rows that resolve account_key and person_key (AC1, AC2, AC3) |
| GET | `/api/recovery/source-data/v1/data-products/freshness?product=DP01` | P1 rwb-source-data | The business date and the load time of the product (AC1) |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Run JOB-04 reconciliation for the business date, with one Idempotency-Key (AC1, AC4) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The right and the refusal path (AC5) |

Every call is one hop on the owner's base `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13). No operation is invented in this story: each path is the owner's published operation, and where a screen would compose them the path would be the gateway-bff composite route (DP-19).

#### 12.3 Events published

None. The harness publishes no Kafka event; it writes its report to the wave record.

#### 12.4 Events consumed

None. The harness triggers JOB-04 through the owner's rerun operation, not through an event, and reads the result through the same contract rather than from a topic.

#### 12.5 Workflows and activities

None added. JOB-04 Reconciliation, the event-triggered reconciliation workflow on rwb-source-data (Architecture v5 slides 15 and 44), is exercised through its rerun operation. The S9 InstructionWorkflow (SLA timers; Act: issueInstruction, recordResult) is out of scope: it belongs to the S9 partner stories, and this harness neither starts nor asserts it. No workflow, activity or Schedule is created or changed by this story.

#### 12.6 Schedules

None. JOB-04 is event-triggered; the harness reruns it for the business date under test and sets no cron.

#### 12.7 Tables owned

None. The harness owns no schema and no table (DP-01); the firm, its users and its instructions are S9's, the case is P3's and the reconciliation result is P1's.

#### 12.8 Contract fakes

| Fake | Contract | Stubbed answer in the run |
|---|---|---|
| Stub for rwb-source-data | The three P1 operations of §12.2 | DP02 returns one row for PERS-SYN-000808, DP01 returns one row for the account_key of case RW-2026-000801, freshness returns business date 2026-11-30 with a load time, and the rerun is accepted once per Idempotency-Key |
| Stub for rwb-partner | `GET /partners`, `GET /partner/instructions` | The firm PART-SYN-0008 with its partner_name, partner_type, panel_status, contract_end and score; the instruction INS-SYN-0008 on case RW-2026-000801 with its instruction_type, instructed_at, due_at and result |
| Stub for rwb-case | `GET /cases/{caseId}` | The case RW-2026-000801 with its case_no, status and stage_code |
| Stub for rwb-access | `POST /authorise` | Allows RW-DATASTEW with Platform administration R; refuses RW-OFF with 403 and MSG-P4-002 |
| Cutover extract fixture | The migrated records of the legacy story | The firm, its two partner users with identity_ref PERS-SYN-000808 and PERS-SYN-000818, the instruction INS-SYN-0008, the orphan identity_ref on a partner_user record, and the source and migrated_at of each record |
| Reconciliation extract fixture | The break list of the reconciliation | One row for firm PART-SYN-0008 with key type PERSON, key value PERS-SYN-000818, reason NO_ACE_ROW, owner role RW-DATASTEW and the ACE team as second owner |

Each stub is generated from the published contract and its version is pinned in the run report, so a contract change shows up as a run failure and not as a silent pass. The harness environment and base hosts, the synthetic cutover extract fixture and its field layout, the break-list fields, the extract format and retention, and the pass or fail gate with its seeding set are Not specified in the source documents (GAP-0448; ASM-0640).

#### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, one hop each on `/api/recovery/<short>/v1` with a 2 s budget (DP-11, DP-13) |
| Kafka | None published and none consumed; the run is triggered by an operation and read back through the same contract |
| Temporal | None added; JOB-04 Reconciliation, the event-triggered workflow on rwb-source-data, is exercised |
| File | The cutover extract fixture and the reconciliation extract fixture, both read as files |

### 13. Solution plan

**Package.** Folder `itg/recovery`, package `th.co.scb.ace.workbench.recovery.itg`, test scope only; not part of any deployed service.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The platform H dependencies in the table above (RWB-PLT-E1044-CON and RWB-PLT-N001-CON) are recorded here and are not repeated in the metadata H field of this story, which stays empty as the plan requires. The one blocking dependency is the I story RWB-P1-DM008-APP, which replaces its stub; until it is live the run uses the stub, and a stub pass is reported as a stub pass.

**Harness components**

| Component | Type | Responsibility |
|---|---|---|
| JourneyRunner | Job | Runs the five owned criteria in order for a business date and holds the run lock |
| StubSet | Fake | The four stubs of §12.8 generated from the published contracts, with the contract version pinned |
| CutoverExtractFixture | Fixture | The synthetic firm, its two partner users, the instruction on its case, the orphan identity_ref and the source and migrated_at of each record |
| KeyResolver | Service | Resolves person_key from identity_ref through DP02 and account_key through DP01 with the freshness read, and names each key that does not resolve |
| NoCopyAssertion | Service | Asserts that no case record is duplicated and that no settlement figure sits on a migrated instruction record or in the cutover extract |
| BreakListAssertion | Service | Compares the read result with the reconciliation extract fixture: one row per orphan, its reason and its two owners, and one row only on a rerun |
| EvidenceReport | Service | Writes one report per business date keyed by story, and holds the pass or fail gate |

**Environment and test data.** SIT, against the stubs from Day 1 and the real services as the I story lands, on the synthetic firm PART-SYN-0008, its partner users with identity_ref PERS-SYN-000808 and PERS-SYN-000818, the instruction INS-SYN-0008 on case RW-2026-000801 and business date 2026-11-30; the panel_status, contract_end and score of the firm, the role_code, valid_from and valid_to of each user, and the instruction_type, instructed_at, due_at and result of the instruction are carried as fixture data, not as values in code. In SIT the records come from the cutover load of P1's own Flyway sequence (DP-15). The harness environment and base hosts, the fixture layout, the break-list fields, the extract format and retention, and the gate with its seeding set are Not specified in the source documents (GAP-0448; ASM-0640). The harness seeds nothing by hand and never writes a schema row.

**Build steps**

1. Generate the four stubs from the published contracts and pin each contract version in the run report; fail the run on a mismatch (X1).
2. Build the CutoverExtractFixture and the ReconciliationExtractFixture, and prove both are read for business date 2026-11-30 (X2).
3. Build the JourneyRunner for AC1: trigger JOB-04 with one Idempotency-Key, read the panel firms and the instructions through rwb-partner, read the case through rwb-case, and resolve person_key and account_key through DP02 and DP01 with the freshness read (X5).
4. Add the KeyResolver assertion that every key on a migrated firm, user or instruction resolves, and that each orphan is on the list for the data steward and the ACE team (X3).
5. Add BreakListAssertion for AC3: one row for firm PART-SYN-0008 with key type PERSON, key value PERS-SYN-000818, reason NO_ACE_ROW and owner role RW-DATASTEW, the ACE team named as second owner in the report, and the firm and its instructions still readable through the rwb-partner contract.
6. Add NoCopyAssertion for AC1: no case record is duplicated and no settlement figure sits on a migrated instruction record or in the extract, with the instruction and the field named where one does (X8).
7. Add AC4: rerun JOB-04 for the same business date, assert one break row, equal counts of firms, partner users, instructions and break rows, and one report entry per business date (X4, X7).
8. Add the access path for AC5 through `POST /api/recovery/access/v1/authorise`, then the EvidenceReport and the gate, and swap a stub for the real owner as its I story lands (X6).

**Feature switch.** None. The harness has no production flag and runs in the test environment only.

**Done when.** The tests of section 16 pass against the fakes and again against RWB-P1-DM008-APP when it lands, and the wave entry check holds a run report keyed by story and business date.

### 14. Validation and messages

| ID | Type | Message |
|---|---|---|
| MSG-P1-001 | Warning | {product} is from {date}. Today's ACE batch has not arrived. |
| MSG-GEN-001 | Error | Enter {field}. |
| MSG-P4-002 | Error | You cannot {action} here. Your role does not include it. |

The harness asserts the message ID and the substituted values on the answer it reads, and owns no message text.

### 15. Screens and states

The legacy story names the SCR-45 Data quality console with its loading and breaks states, and this harness renders no screen: the breaks are listed on the reconciliation extract, which the data steward and the ACE team read as a file. The states the harness asserts on that extract are small.

| State | What the extract holds |
|---|---|
| No break | One line for the business date with the counts of firms, partner users, instructions and break rows, and no break row |
| Break | One row per orphan with the firm, the key type, the key value, the reason, the data steward and the ACE team as owners |

The harness renders no screen. The SCR-45 Data quality console that the legacy story names is not part of this legacy key: it is the screen of RWB-AD-019 and this story neither builds it nor reads it. What the wave entry check looks at instead is the run report, whose environment, layout and retention are Not specified in the source documents (GAP-0448; ASM-0640).

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-DM-008-01-ITG | AC1 (legacy); ITG AC1 | Integration | Synthetic firm PART-SYN-0008 and its user PERS-SYN-000808 with DP01 and DP02 rows present |
| TC-DM-008-02-ITG | AC2 (legacy); ITG AC2, ITG AC3 | Integration | One identity_ref PERS-SYN-000818 with no view row |
| TC-DM-008-03-ITG | AC3 (legacy, owned by RWB-P1-DM008-APP); ITG AC4 | Integration | Two JOB-04 runs for business date 2026-11-30, with no duplicated case and no settlement figure |
| TC-DM-008-04-ITG | Access; ITG AC5 | Component | RW-OFF caller without Platform administration R |

The AC column names the legacy AC the copy derives from and the ITG AC it asserts, and the full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx under the same legacy test case ID. TC-DM-008-03-ITG is the cutover copy and names RWB-P1-DM008-APP as the owner of the cutover assertions it derives from.

### 17. Guardrails

- No business value in code: the synthetic firm, users, instruction, business date, fixture contents, break reasons and report layout are data.
- No personal data in logs, fixtures or reports: identity_ref is synthetic and no customer record is read at all.
- No read of another service's schema and no direct view read: the firm, its users and its instructions come from rwb-partner, the case from rwb-case and the ACE side from the rwb-source-data contract (DP-01, DP-05).
- No settlement figure is read or copied, and no case record is duplicated by the harness.
- One hop and a 2 s budget per call, with a circuit breaker per downstream, so the harness fails where a screen would (DP-11).
- A stub pass is never reported as a real pass: the report names the contract version and whether the hop was a stub or the owner.
- The harness never runs against UAT or production, and it never writes a row by hand.
- A failing criterion is fixed in the service that owns it or reported as a gap; it is never waived in the script.

### 18. Traceability

| Item | Source | Where it lands |
|---|---|---|
| Legacy story RWB-DM-008 Migrate partner performance | Recovery Workbench Data Migration Stories v3, lines 466 to 549 | Sections 1, 3, 11 and 19 of this file |
| Legacy AC1 Extract the Workbench records, verbatim | The same, lines 485 to 489 | Section 7, AC1, marked (legacy RWB-DM-008 AC1) |
| Legacy AC2 Reconcile the business keys, verbatim | The same, lines 491 to 495 | Section 7, AC2, marked (legacy RWB-DM-008 AC2) |
| Legacy AC3 Cut over, and the four legacy test cases TC-DM-008-01 to TC-DM-008-04 | The same, lines 497 to 501 and 540 to 545 | AC3 stays with RWB-P1-DM008-APP (section 19); the four cases are copied as -ITG in section 16 |
| DF-PRT-001 to DF-PRT-007, DF-REF-212 to DF-REF-217, DF-PRT-008 to DF-PRT-016 and DF-CAS-001 to DF-CAS-055 | Logical Data Model and Data Dictionary v8 | Section 11 |
| DL25, zero tolerance on the migrated data | Decision Log, DL25 | Section 8, BR1 to BR3 |
| REQ-RDF-007 and REQ-RDF-008 | BRD Program v4 and Epic 1 v4 | Section 8, BR1 and BR2 |
| D-RCV-35 and ADR-010, ACE data only through the views | Decision Log, D-RCV-35; ADR-010 | Section 8, BR4 and BR5; sections 12.2 and 12.8 |
| Job map JOB-04 Reconciliation, owner rwb-source-data | Architecture v5 slides 15 and 44 | Section 12.5, the JOB-04 reconciliation this harness exercises; the S9 InstructionWorkflow is out of scope |
| DP-05, DP-15 and DP-19 | Template and Rules v1 §R5.5 | Section 13, pattern application |

### 19. Out of scope

- RWB-P1-DM008-APP: the extraction, the cutover and legacy AC3 Cut over, together with the REC-05 reconciliation and the break list. The cutover load of the records into rwb_partner is P1's own Flyway sequence.
- S9 rwb-partner production code and its CON, APP and DB stories: the panel, the partner users, the instructions, the results, the fees, the scorecards and the tables are built there. The S9 InstructionWorkflow and the accept, result and invoice operations are not started or asserted here.
- The partner portal and its FAPI 2.0 path through the partner gateway.
- The SCR-45 Data quality console (RWB-AD-019).
- The cutover plan, the data steward sign-off and the legacy read-only period of legacy AC3.
- ACE ingestion and the 30 views (RWB-ACE-001).
- Platform deployment and configuration.
- The other four data migration keys of this wave.
