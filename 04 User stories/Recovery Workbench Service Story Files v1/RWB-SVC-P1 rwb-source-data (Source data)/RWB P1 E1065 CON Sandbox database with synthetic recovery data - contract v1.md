# RWB-P1-E1065-CON Sandbox database with synthetic recovery data

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P1-E1065-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-source-data |
| Service epic | RWB-SVC-P1 |
| Wave | 1 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-065 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP05, DP07, DP13, DP15, DP19 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P1 rwb-source-data v1.md (FR-P1-001, FR-P1-006, FR-P1-007, FR-P1-008, FR-P1-010, FR-P1-012, FR-P1-013, FR-P1-024, FR-P1-025, FR-P1-029, FR-P1-030) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: split from RWB-E1-065 for rwb-source-data. The sandbox of the legacy story becomes a build tool of this service, so its interface is published as a contract before the tool is written: the stage contract (trigger, inputs, outputs, idempotency key, restart behaviour), the seed profile schema, the database and role contract for `rwb_sandbox` with schema `public`, schema `recovery` and schema `rwb_source_data`, the failure contract and the four fixtures that stand in for the neighbouring stories (DP-01, DP-05, DP-07, DP-15; Architecture v5 slides 8, 15, 29 and 41). The nine legacy acceptance criteria stay with RWB-P1-E1065-APP; this story owns the six contract criteria only. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **the published contract baseline of the sandbox build of rwb-source-data: the stage document that fixes its trigger, its inputs, its outputs, its idempotency key and its restart behaviour, the seed profile schema whose every value is data, the database and role contract of `rwb_sandbox` with its three schemas and its read-only role, the failure contract that fails closed and keeps the previous sandbox, the four fixtures that stand in for the ACE head and the two neighbouring stories, and the nine contract tables of section 12**, so that **the generator, the verifier, the ACE database work and the contract tests can be built in parallel on Day 1 against a fixed, testable interface instead of a description in a pipeline script**.

This is the contract slice of legacy RWB-E1-065. It delivers:

- the stage contract document, which describes the sandbox build as a pipeline stage interface and nothing else;
- the seed profile schema: seed, the three volumes, the shape count, the list-of-values source and the personal-data pattern rule, every value an override;
- the database and role contract: database `rwb_sandbox`, build database `rwb_sandbox_next`, schemas `public`, `recovery` and `rwb_source_data`, the read-only role `rwb_sandbox_read`, DEV only, no production data;
- the failure contract, with the four named checks of the legacy exception paths X1, X3, X4 and X6 and the fail-closed rule;
- the four fixtures and fakes, and the drift rule that fails a build when a fixture leaves the contract;
- the nine contract tables of section 12, each with its owner from the Ownership Map.

It builds nothing: no generator, no verifier, no migration, no database. It defines the interface those artefacts must satisfy, and the app story, the ACE DB story and the tests of this legacy key read it.

### 2. Business rationale

Contract-first is the decoupling decision of the target (DP-11, ADR-020), and a build tool is no exception. The sandbox of the legacy story was described inside a pipeline stage and a solution plan, so nothing could be tested until the stage existed: the customer of the stage was the pipeline, and the definition of "built" was an observation, not an assertion. In the target the sandbox belongs to rwb-source-data (Architecture v5 slides 8, 15 and 41), three stories touch it — the generator, the ACE database objects and the tests — and the contract of the stage is what keeps them apart.

Fixing the interface first buys four things. The ACE DB story can build `rwb_sandbox` and its role against the names and grants in the contract instead of against a script. The app story can build the generator against the seed profile schema and the four fixtures instead of against the DEV database. The contract tests of this story fail on a drift between a fixture and the document before any of that code exists. And the four failure checks of the legacy story become assertions with names, so a failed build is a contract breach rather than a pipeline observation. Serves REQ-RDF-001 (the 14 data products with one system of record and one owner) and REQ-RDF-010 (no personal data outside its permitted use).

### 3. Preconditions

- The service template and the naming library are available (RWB-PLT-TPL, RWB-PLT-E1047-CON), so the database, schema, role and package names follow the platform rule rather than a local choice.
- The per-service Flyway sequence rule is available (RWB-PLT-E1044-CON, DP-15), so the contract names the sequence and its baseline instead of a monolith version.
- The reference-data contract of rwb-case is published (RWB-P3-E1043-CON, DP-07); where the source set of this run does not name its read path, the contract carries the placeholder and the reading of section 12.2.
- The Ownership Map is the only source for the owner of an object named in the contract; no object of another service is documented as this story's.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).
- The contract of a build tool is not described by any source document of this run, so it is read as the pipeline stage interface and its input and output profile, in the same way the legacy story described its stage in section 12. That reading, and the exact wording of the seed profile fields, are Not specified in the source documents (GAP-0502; ASM-0694).

### 4. Flow

1. Draft the stage contract: trigger, inputs, outputs, idempotency key, restart behaviour, and the one build-time read of 12.2.
2. Draft the seed profile schema and fix every field as an override, with the legacy values as the defaults (seed 20261128, 1,226 Mortgage, 1,296 Hire purchase, 290 SSME, 10 cases per shape).
3. Draft the database and role contract: database `rwb_sandbox`, build database `rwb_sandbox_next`, the three schemas, the read-only role `rwb_sandbox_read`, the DEV-only rule and the no-production-data rule.
4. Draft the failure contract: fail closed, keep the previous sandbox, and name the four failure checks with their messages.
5. Describe the four fixtures and fakes and the drift rule that fails a build.
6. Publish the nine contract tables of section 12 and check each owner against the Ownership Map.
7. Add the six contract tests of section 16.
8. Tag the baseline and hand it to RWB-P1-E1065-APP, RWB-P1-E1065-DB and the tests of this legacy key.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The stage document omits the idempotency key or the restart behaviour | The contract test fails and the baseline is not tagged | None | AC1 |
| X2 | A seed profile value is written in the generator instead of the profile | The contract test fails on the profile schema and the value is moved back into data | None | AC2 |
| X3 | The contract names a schema, a database or a role outside the three schemas and the one read-only role | The contract test fails and names the object | None | AC3 |
| X4 | The failure contract does not name one of the four checks | The contract test fails and names the missing check | None | AC4 |
| X5 | A fixture answers a shape the document does not declare, or the document declares a shape no fixture answers | The contract test fails on the drift and the merge is blocked | None | AC5 |
| X6 | One of the nine contract tables is missing or names an owner that the Ownership Map does not give | The contract test fails and names the table | None | AC6 |
| X7 | A field-level definition is missing from the source material | The field carries the placeholder, and one gap row and one assumption row are recorded for the whole story | None | AC1, AC2, AC3 |

X1 to X6 are the contract paths this story adds; X7 is the placeholder path of the run (Template and Rules §R9). This story has no run-time exception path of its own, because it has no run time: the failure behaviour of the stage it describes is the failure contract of 12.6, and it is asserted by AC4.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform libraries, the reference-data contract and the Ownership Map only |
| Negotiable | Field-level detail of the seed profile is settled with the generator; the names, the three schemas, the role and the four checks are fixed by this story |
| Valuable | Unblocks the generator, the ACE database objects and the contract tests of this legacy key on Day 1 |
| Estimable | One document, one profile schema, three contract tables of rules, four fixtures and six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact, never against a built sandbox |

### 7. Acceptance criteria

```gherkin
Feature: Sandbox build contract baseline for rwb-source-data

  Background:
    Given the service naming rule of the platform library is in force
    Given the sandbox database is "rwb_sandbox" and the build database is "rwb_sandbox_next"

  Scenario: AC1 The stage contract fixes the interface of the sandbox build (new, D-RCV-60)
    Given the stage contract document of the sandbox build is published
    When it is reviewed against the six interface elements
    Then it states the trigger: a merge to main that changes the ACE schema DDL, a migration of the service, the dictionary or the seed profile, or a manual start by RW-TRIBE or RW-PLATADM
    Then it states the inputs: the ACE DDL, the RWB-ACE-001 Tier 2 DDL fixture, the per-service baseline, the two view migrations, the dictionary rows and the seed profile
    Then it states the outputs: the database, the three schemas and the build report with the row count per table and the verifier result
    Then it states the idempotency key as the commit hash and the seed, with the same pair giving the same rows
    Then it states the restart behaviour on "rwb_sandbox_next", the rename after the verifier and the advisory lock
    Then it states the one build-time read of the reference-data contract and its 2 s timeout

  Scenario: AC2 The seed profile schema is data and every value is overridable (new, D-RCV-60)
    Given the seed profile schema of the contract
    When it is validated
    Then it declares the seed, the volume per product group, the shape count, the list-of-values source and the personal-data pattern rule
    Then no value is a constant in the generator or in the stage script
    Then the legacy defaults are recorded as the defaults and not as the only values
    Then a changed volume is a diff in the profile and needs no code change

  Scenario: AC3 The database and role contract fixes three schemas, one read-only role and DEV only (new, D-RCV-60)
    Given the database and role contract of the document
    When a reviewer checks the names against the platform naming rule
    Then the database is "rwb_sandbox" and the build database is "rwb_sandbox_next"
    Then the schemas are "public" for the ACE test double, "recovery" for the 30 read-only views and "rwb_source_data" for the service's own tables and the four extension tables
    Then the read-only role is "rwb_sandbox_read" and it holds SELECT on schema "recovery" and schema "rwb_source_data" and nothing on schema "public"
    Then the contract states that the sandbox holds synthetic data only and is never deployed to SIT, UAT or PROD
    Then the contract names the credential owner as the platform DB owner and holds no credential

  Scenario: AC4 The failure contract fails closed and names the four checks (new, D-RCV-60)
    Given the failure contract of the document
    When a build fails on any of the four checks
    Then the build fails closed before the rename, so the previous sandbox stays in use and no partial database is published
    Then the check "a table column has no sys_fields row" names the table and the column
    Then the check "a generated value breaks a constraint" names the table and the constraint
    Then the check "a generated value outside schema public matches a personal data pattern" names the table and the column
    Then the check "a second build starts while one runs" waits on the advisory lock and runs after the first
    Then every failure is reported in the pipeline result and none is answered with a user message

  Scenario: AC5 The four fixtures match the contract and drift fails the build (new, D-RCV-60)
    Given the ACE head fixture, the view fixture, the reference-data fake and the delivered-tables fixture
    When the contract tests compare each fixture with the document
    Then the ACE head fixture answers the Tier 1 tables and the Tier 2 DDL fixture answers the 14 Tier 2 tables
    Then the view fixture answers the 30 "recovery.v_ace_*" views and the three helper functions
    Then the reference-data fake answers the list-of-values read per table code, with an empty list and a timeout
    Then the delivered-tables fixture answers the baseline, the four extension tables and the read-only role
    Then a fixture that answers a shape the document does not declare fails the build
    Then a shape the document declares with no fixture to answer it fails the build

  Scenario: AC6 The nine contract tables are complete and each names its owner (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables are reviewed against the Ownership Map
    Then each of 12.1 to 12.9 is present
    Then every object named in 12.6 and 12.7 carries an owner from the Ownership Map and no other
    Then the four fixtures of 12.8 are the ones the contract tests use
    Then the summary of 12.9 agrees with 12.1 to 12.5
```

The six criteria are new and prove only the contract artefacts: the stage interface, the seed profile, the database and role contract, the failure contract, the fixtures and the nine tables. No legacy criterion text is copied here; the nine legacy criteria of RWB-E1-065 are owned by RWB-P1-E1065-APP and appear in this story only as regression test cases.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One database name and one build database name per sandbox: `rwb_sandbox` and `rwb_sandbox_next`; the rename is the only publication step | DP-15; Architecture v5 slide 29 |
| BR2 | Three schemas and no more: `public` as the ACE test double, `recovery` for the 30 views and `rwb_source_data` for this service's tables and the four extension tables | DP-01, DP-02, DP-05; Architecture v5 slides 15 and 29 |
| BR3 | One read-only role, `rwb_sandbox_read`: SELECT on `recovery` and on `rwb_source_data`, nothing on `public`, no INSERT, UPDATE or DELETE anywhere | DP-02; legacy BR9 |
| BR4 | Every value of the seed profile is data: the seed, the volumes, the shape count, the list-of-values source and the personal-data pattern rule are overrides | legacy BR3, BR5; Template and Rules §R7.2 s17 |
| BR5 | The lists of values are read through the reference-data contract of rwb-case and never from a constant or a copy | DP-07 |
| BR6 | The sandbox holds synthetic data only and is DEV only; the ACE-shaped tables are a test double and are never deployed to SIT, UAT or PROD | legacy BR1, BR7; NFR-045 |
| BR7 | A build fails closed: the previous sandbox stays in use and no partial database is published | legacy §5 X1, X3, X4, X6 |
| BR8 | The stage is a release activity and not a business timer: it is not a Temporal Schedule and it is not in `job_catalog` | DP-10; Architecture v5 slide 44 |
| BR9 | The contract names only this service's objects and the ACE schema; no other service's schema, table or operation appears as this story's | DP-01; Ownership Map v1 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The six criteria are described and the nine tables are written | In review |
| In review | Consumer sign-off | The app story, the ACE DB story and the tests accept the document and the four fixtures | Baselined |
| Baselined | Additive change | A seed profile field or a fixture shape is added and every consumer still answers it | Baselined |
| Baselined | Breaking change | A database name, a schema, a role or a failure check changes | New baseline drafted |
| Baselined | Drift in a fixture | A contract test fails | In review |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-source-data | Owns the document, the profile schema and the four fixtures; tags the baseline |
| Solution architect | Approves a change to a database or schema name and a new baseline |
| ACE team lead and ACE DBA | Approve the `public` test-double rule and the Tier 2 DDL fixture |
| Platform DB owner | Owns the credential of `rwb_sandbox_read` and the DEV-only gate this contract states |
| Data steward | Confirms that the personal-data pattern rule covers every personal field and that no production value is used |
| Recovery tech lead | Owns the seed profile defaults that the contract records |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

The contract declares shapes, names and rules, not business values.

| Item | Content |
|---|---|
| Seed profile | Seed, volume per product group, shape count, list-of-values source, personal-data pattern rule; the legacy defaults are seed 20261128, 1,226 Mortgage, 1,296 Hire purchase and 290 SSME, 10 cases per shape |
| Database names | `rwb_sandbox` and `rwb_sandbox_next` |
| Schema names | `public` (ACE test double), `recovery` (the 30 views), `rwb_source_data` (this service's tables and the four extension tables) |
| Role | `rwb_sandbox_read`, read only |
| Failure checks | The table and column with no dictionary row; the value that breaks a constraint; the personal-data pattern match outside `public`; the second build on the advisory lock |
| Fixtures | The ACE head, the 30 views, the reference-data fake and the delivered tables |

The field-level definition of the seed profile (types, lengths, required flags and the exact wording of the pattern rule) is Not specified in the source documents (GAP-0502; ASM-0694); this story fixes the five elements above and leaves the field-level detail to the baseline review.

### 12. Contract

#### 12.1 REST operations provided

None. The sandbox build is a pipeline stage and publishes no operation; the read contract of the service on base `/api/recovery/source-data/v1` is RWB-P1-E1069-APP's, and this contract adds no path to it (DP-13).

#### 12.2 REST operations consumed

| Method | Path | Owner | Contracted use |
|---|---|---|---|
| GET | Not specified in the source documents (GAP-0502; ASM-0694); read as `/api/recovery/case/v1/reference-data/{tableCode}` | P3 rwb-case | The lists of values of the seed, read per table code once per build, 2 s timeout, no fallback to a constant; the fake answers a list, an empty list and a timeout |

#### 12.3 Events published

None. The topic of the service is `rwb.source-data.events.v1` with event names `rwb.source-data.<Event>.v1` (DP-14), and the two events `AceDataReady` and `AceDataLate` belong to RWB-P1-E1013-APP. A build result is published in the pipeline, not on the topic.

#### 12.4 Events consumed

None. The service consumes no event (Architecture v5 slide 15), and the stage subscribes to none.

#### 12.5 Workflows and activities

None. The stage calls no Temporal workflow and no activity; the task queue `rwb-source-data` in namespace `rwb-recovery` is not used by this contract.

#### 12.6 Schedules

**Sandbox build stage contract**

| Element | Contracted value |
|---|---|
| Stage name | Sandbox build, a DEV pipeline stage of the rwb-source-data repository |
| Trigger | Merge to main that changes the ACE schema DDL, a file under the service migration folder, the dictionary or the seed profile; manual start by RW-TRIBE or RW-PLATADM |
| Schedule kind | On trigger only; not a Temporal Schedule, not a Quartz job and not a row in `job_catalog` (BR8) |
| Inputs | The ACE schema file, the RWB-ACE-001 Tier 2 DDL fixture, the per-service baseline, the two view migrations of RWB-P1-E1069-APP, the dictionary rows and the seed profile |
| Outputs | Database `rwb_sandbox` with schema `public`, schema `recovery` and schema `rwb_source_data`, and the build report with the row count per table and the verifier result |
| Publication | The rename of `rwb_sandbox_next` to `rwb_sandbox` after the verifier passes, under one advisory lock |
| Idempotency key | Commit hash and seed; the same pair gives the same rows and counts |
| Restart behaviour | A failed run leaves the previous `rwb_sandbox` and no partial database; a second run for the same pair rebuilds both schemas and swaps them in |
| Failure checks | The four named checks of AC4 and the fail-closed rule of BR7 |
| Events | None |

#### 12.7 Tables owned

No table is created by this story. The objects the contract names, and their owners:

| Object | Schema | Owner (ownership map) | Contracted role |
|---|---|---|---|
| the sandbox database and its three schemas | database `rwb_sandbox` | P1 (this service's sandbox; the ACE DDL stays ACE's) | Named by this contract; created by RWB-P1-E1065-DB |
| the ACE-shaped test double | `public` | ACE team | A DEV test double only, synthetic rows, never deployed outside DEV |
| the 30 `v_ace_*` views and the three helper functions | `recovery` | View owner `ace_view_owner`; contract owner P1 | Created by RWB-P1-E1069-APP; seeded and asserted by the stage |
| `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext` | `rwb_source_data` | P1 | Created by RWB-P1-E1069-DB; seeded and asserted by the stage |
| this service's 13 tables, among them `case_list_row`, `interaction`, `sys_objects` and `sys_fields` | `rwb_source_data` | P1 | Created by the baseline of RWB-P1-E1001-APP; filled with synthetic rows by the stage |
| the read-only role `rwb_sandbox_read` | database | P1 (sandbox), credential by the platform DB owner | Created and granted by RWB-P1-E1065-DB; named by this contract |

#### 12.8 Contract fakes

| Fixture | Contract element | Drift rule |
|---|---|---|
| ACE head fixture | The Tier 1 tables of `public` and the 14 Tier 2 tables of the RWB-ACE-001 fixture | A tier or a table that the document does not declare fails the contract test |
| View fixture | The 30 `recovery.v_ace_*` views and the three helper functions of RWB-P1-E1069-APP | A view name that leaves the 30 fails the contract test |
| Reference-data fake | The read of 12.2, answering a list, an empty list and a timeout | A table code with no answer, or an answer shape the document does not declare, fails the contract test |
| Delivered-tables fixture | The baseline, the 13 tables, the four extension tables and the read-only role | A table or a grant the document does not declare fails the contract test |

#### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | None | 1 build-time read of the reference-data contract | 2 s timeout, no fallback; the path is settled in RWB-P3-E1043-CON |
| Kafka | None | None | The topic `rwb.source-data.events.v1` belongs to other P1 stories |
| Temporal | None | None | A pipeline stage, not a workflow |
| File | None | The DDL files and the build report | The ACE schema file and the Tier 2 fixture are inputs; the report is the output |
| SQL view | The 30 `recovery.v_ace_*` views are seeded and asserted | The ACE-shaped tables behind them | SELECT and seed only, in DEV only |

### 13. Solution plan

**Deliverables.** `contract/sandbox-stage.md` (the stage contract of 12.6), `contract/sandbox-seed-profile.yaml` (the schema of section 11 with the defaults), `contract/sandbox-database.md` (the database, schema and role contract of 12.7), `contract/sandbox-failure.md` (the four checks and the fail-closed rule), and the four fixtures of 12.8.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-01, DP-05, DP-07 and DP-15 are the subject of this contract: one schema set, one read path, one reference-data read and one sequence. DP-03, DP-04, DP-13 and DP-19 are named for completeness of the pattern set, because the generator implements them; this story fixes their names in the contract and builds none of them, and its metadata dependency list is empty by rule for a CON story.

**Build steps**

1. The stage contract with the six interface elements of AC1, written against the names of section 11.
2. The seed profile schema with every value an override, the legacy defaults recorded as defaults, and a validation fixture for a missing field.
3. The database and role contract with the three schemas, `rwb_sandbox_read` and the DEV-only rule.
4. The failure contract with the four named checks and the fail-closed rule.
5. The four fixtures, with the drift rule of 12.8.
6. The six contract tests of section 16; a drift between a fixture and the document fails the build.
7. The nine contract tables, each owner checked against the Ownership Map.
8. Baseline tag and the consumer sign-off note for the app, ACE DB and test stories.

**Done when.** The six contract tests pass, the four fixtures answer every shape the document declares, the nine tables are complete with their owners, and the app story, the ACE DB story and the tests of this legacy key have accepted the baseline.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P4-002 | A test user without the right calls the DEV service against the sandbox | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | A test user calls a sandbox case outside their scope | This case is not in your scope. |

The two texts are the legacy texts, copied unchanged, and are raised by the guard library of rwb-access on the DEV service; this contract carries them as the two business messages that apply to the sandbox and raises none of its own. The contract and drift failures are contract-test results for developers and are not part of the message standard.

### 15. Screens and states

No screen. The contract is read by the three consuming stories, whose state machines it fixes: the stage moves through Building, Published and Failed, and the baseline moves through Draft, In review and Baselined. Nothing in this contract is shown to a user of the Workbench; the sandbox is read with SQL and the export script.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P1-E1065-CON-01 | AC1 | Contract | The stage document validated against the six interface elements, including the idempotency key and the restart behaviour |
| TC-P1-E1065-CON-02 | AC2 | Contract | The seed profile schema with the legacy defaults, a changed volume and a missing field |
| TC-P1-E1065-CON-03 | AC3 | Contract | The database, schema and role names checked against the platform naming rule and the Ownership Map |
| TC-P1-E1065-CON-04 | AC4 | Contract | Each of the four failure checks fired in a fixture, and the previous sandbox checked as still in use |
| TC-P1-E1065-CON-05 | AC5 | Contract | The four fixtures compared with the document, plus one added shape and one missing shape |
| TC-P1-E1065-CON-06 | AC6 | Component | The nine contract tables reviewed against the Ownership Map and against the summary of 12.9 |
| TC-E1-065-01 | Regression evidence for legacy AC1 on the objects the contract names | End to end | The Tier 1 and 14 Tier 2 tables; the baseline and the two view migrations; seed 20261128; 2,812 cases plus shapes |
| TC-E1-065-02 | Regression evidence for legacy AC2 on the read-only role | End to end | Read-only role query, CSV export and refused UPDATE |
| TC-E1-065-03 | Regression evidence for legacy AC3 on the dictionary-driven fill | End to end | Test migration adding recovery_case.risk_tier with its dictionary row |
| TC-E1-065-04 | Regression evidence for legacy AC4 and the X1 failure check | End to end | Dictionary fixture without the DF-CAS-023 row for recovery_case.closure_reason |
| TC-E1-065-05 | Regression evidence for legacy AC5 on the idempotency key | End to end | Two builds for commit a1b2c3d and seed 20261128 |
| TC-E1-065-06 | Regression evidence for legacy AC6 and the X3 failure check | End to end | Empty LOV-PRODUCT seed |
| TC-E1-065-07 | Regression evidence for legacy AC7 and the X4 failure check | End to end | Injected 13-digit value in recovery.document_field.extracted_value; a clear value in public.customer |
| TC-E1-065-08 | Regression evidence for legacy AC8 on the exception shapes | End to end | Boundary accounts at 89 and 90 days past due in v_ace_account |
| TC-E1-065-09 | Regression evidence for legacy AC9 and the X6 failure check | End to end | Two builds started together |
| TC-E1-065-10 | Regression evidence for the access test | Component | Test user with RW-REFADM calls the case read path on the sandbox; refused with MSG-P4-002 |

The six new cases prove the contract artefacts of this story. The ten legacy cases are carried as regression evidence: their IDs are kept, their Covers and Data are carried onto the split and the legacy Covers text is qualified as regression evidence, the legacy level "System" maps to "End to end" and "Access" to "Component", and the legacy criteria themselves are owned by RWB-P1-E1065-APP. The full legacy test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in the contract: the seed, the volumes, the shape count, the list-of-values source and the pattern rule are profile data, and the contract fixes their names, not their values.
- No personal data in an example or a fixture: every value in the four fixtures is synthetic, and the pattern rule names patterns, never a real identity number.
- The contract names three schemas and one read-only role and no other schema of any service; a schema, a table or an operation of another service appears only as consumed (DP-01, DP-02).
- No credential in the contract: the credential of `rwb_sandbox_read` is held by the platform DB owner and never appears in a document, a script or a runbook.
- DEV only and synthetic only: the contract states both, and the database story enforces both with a gate.
- One hop and 2 s on the reference-data read; a slow answer fails the build closed instead of falling back to a constant (DP-11).
- A fixture that leaves the contract fails the build; a shape with no fixture fails the build.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | 14 data products, each with one system of record and one owner | The stage inputs and outputs of 12.6, the three schemas of 12.7 and the dictionary-driven fill of the seed profile | TC-P1-E1065-CON-01, TC-P1-E1065-CON-02, TC-P1-E1065-CON-06 |
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | The read-only role of 12.7, the personal-data pattern rule of the seed profile and the failure contract of 12.6 | TC-P1-E1065-CON-03, TC-P1-E1065-CON-04, TC-P1-E1065-CON-05 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-P1-E1065-APP | App development | Implements the generator and the stage this contract describes; consumes the profile schema and the four fixtures |
| RWB-P1-E1065-DB | ACE DB | Implements the database, the three schemas, the role and the grants this contract names |
| RWB-P1-E1001-APP | App development | Delivers the per-service baseline and the 13 tables that the delivered-tables fixture stands in for |
| RWB-P1-E1069-APP | App development | Delivers the 30 views and the three helper functions that the view fixture stands in for |
| RWB-P1-E1013-APP | App development | Sibling: the freshness reads and the two events of the service, which the contract names as not published here |
| RWB-P3-E1043-CON | Contract | C: the reference-data contract the one build-time read of 12.2 is taken from |
| RWB-PLT-E1044-CON, RWB-PLT-E1047-CON | Contract | The per-service Flyway sequence and the naming library the contract follows, recorded as notes in section 3 |

### 19. Out of scope

- The generator, the verifier, the export tool and the pipeline stage itself: RWB-P1-E1065-APP.
- The database `rwb_sandbox`, its three schemas, the role `rwb_sandbox_read`, the grants: RWB-P1-E1065-DB; the four extension tables: RWB-P1-E1069-DB.
- The 30 `recovery.v_ace_*` views and their helper functions: RWB-P1-E1069-APP.
- The per-service baseline, this service's 13 tables and the dictionary rows: RWB-P1-E1001-APP.
- The implementation of the reference-data contract of rwb-case: RWB-P3-E1043-CON, which this contract consumes and fakes.
- The rule packages and the decisions they take: rwb-decision (P7), consumed through the embedded kit and not defined here.
- Any change to a database name, a schema name, the read-only role or a failure check: the solution architect and the recovery tech lead, with a new baseline.
- The screens, the composite route and the DEV service: gateway-bff and the screen owners (DP-19).
