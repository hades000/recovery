# RWB-PLT-E1044-CON Database migrations versioned with parameterized schema names

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-E1044-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01 |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-E1-044 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Patterns applied | DP01, DP05, DP06, DP07, DP13, DP14, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-005, FR-PLT-006, FR-PLT-007) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: migration contract published for the 19 services (ADR-021; DP-15; Arch v5 slides 29 and 41). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **tech lead**, I want **one published migration contract that every service follows: the file name `V<seq>__<story>_<name>.sql`, the line `-- Story: <story key>` on line 1, exactly one story key per file, the schema only as `${schema}` fed by `RWB_SCHEMA`, the default `flyway_schema_history` inside each service's own schema, one `V0001` baseline per service, forward-only in PROD, no foreign key into `public`, no cross-schema reference, one migration account per service and the migration-run record**, so that **19 teams migrate in one way and a contract test refuses a file that breaks the rule before any environment receives it**.

### 2. Business rationale

With one Flyway sequence per service (DP-15, ADR-021), the naming, the story header, the placeholder, the history table, the baseline and the forward-only rule become 19 local choices unless they are published once. Arch v5 slide 29 fixes the physical rule: one schema and one login per service, no cross-schema joins or keys, Flyway per service in its own pipeline, a boundary test in every build. This contract turns that slide into a testable artefact: a service team writes a migration against the contract and its fixture, and the contract test refuses a literal schema name, a foreign key into `public`, a missing or repeated story key, an undo file and a cross-schema reference, naming the file and the line. It is the Day-1 baseline that RWB-PLT-E1044-APP-2 builds and RWB-PLT-E1044-OPS deploys.

### 3. Preconditions

- The platform template supplies the Flyway module and the golden pipeline in which the contract test runs (RWB-PLT-TPL).
- Each of the 19 services has its own schema `rwb_<name>` and its own login in the ACE database (Arch v5 slides 29 and 41); creating them is database work outside this story.
- ADR-021 (per-service Flyway and migration ownership) is the decision in force and DP-15 is the pattern.
- The legacy build rule of RWB-E1-044 (D-RCV-28) is the starting text: `V<seq>__<story>_<name>.sql`, four-digit sequence in merge order, `-- Story: <story key>` on line 1.
- No build dependency: this story is Day 1 by rule and sits in contract group CG-W0 (Template and Rules §R5.7).

### 4. Flow

1. Draft the contract document around the nine elements: the file name, the story header, one story key per file, the placeholder, the history table, the baseline, the forward-only rule, the no-cross-schema rule and the account rule.
2. Fix the 19 parameter sets, one per service, from the schema table of section 11.
3. Publish the migration-run record shape with the P1 job view as the owner.
4. Publish the fixture set: one valid file per service and the six forbidden fixtures.
5. Publish the contract test: each fixture is run through the lint and the boundary test and the expected refusal names the file and the line.
6. State the versioning rule: an additive clarifying change keeps the version, a rule that refuses a file which passed before raises v2 and deprecates v1.
7. Review with the service teams and tag the baseline.
8. Hand the baseline to RWB-PLT-E1044-APP-2, RWB-PLT-E1044-OPS and every service pipeline.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A fixture carries a literal schema name | The contract test refuses it and names the file and the line | MSG-P3-016 | AC2 |
| X2 | A fixture declares a foreign key into `public` | The contract test refuses it and names the file and the line | MSG-P3-016 | AC2 |
| X3 | A fixture carries no story header, or two files carry the same story key | The contract test refuses it and names both files | MSG-P3-016 | AC2 |
| X4 | A fixture is an undo file `U*.sql` | The contract test refuses it and names the file | MSG-P3-016 | AC2 |
| X5 | A fixture references another service's schema | The contract test refuses it and names the file and the line | MSG-P3-016 | AC2 |
| X6 | A parameter set resolves to a schema outside the 19 values | The contract test refuses the set | MSG-P3-016 | AC3 |
| X7 | A rule change would refuse a file that passed the published version | The new rule is published as v2 and v1 is deprecated | None | AC5 |
| X8 | A contract element or a fixture value is missing from every source | The element is marked with the placeholder and one gap row is carried | None | AC1 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Reads the platform template, Arch v5 slides 29 and 41 and the legacy build rule only |
| Negotiable | The contract location and the owner of the Flyway module are open points; the nine rules are fixed |
| Valuable | Gives every service team one thing to build and one test to pass on Day 1 |
| Estimable | One document, 19 parameter sets, 25 fixtures, six contract tests |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact and the fixtures, not against a business outcome |

### 7. Acceptance criteria

```gherkin
Feature: Migration contract for the 19 services

  Background:
    Given the platform template supplies the lint and the boundary test
    Given each of the 19 services has its own schema rwb_<name> and its own login

  Scenario: AC1 The migration contract is published and validates (new, D-RCV-60)
    Given the migration contract document is published
    When it is validated against the contract template of the platform library
    Then it states the file name, the story header, one story key per file, the ${schema} placeholder fed by RWB_SCHEMA, the default flyway_schema_history in the service's own schema, one V0001 baseline per service, forward-only in PROD, no foreign key into public, no cross-schema reference, the per-service migration account and the migration-run record
    Then every one of those elements is named and has an owner

  Scenario: AC2 The contract test rejects each forbidden fixture (new, D-RCV-60)
    Given the six forbidden fixtures: a literal schema name, a foreign key into public, a missing story header, a duplicate story key, an undo file and a cross-schema reference
    When the contract test runs
    Then each fixture is refused with MSG-P3-016 naming the file and the line
    Then the build fails and no environment receives the file

  Scenario: AC3 The 19 parameter sets resolve the 19 schemas (new, D-RCV-60)
    Given the 19 parameter sets of section 11, one per service
    When each set is applied to the same migration file with ${schema}
    Then the file produces objects in the schema of that set and in no other schema
    Then no file carries a literal schema name

  Scenario: AC4 The migration-run record shape is published and faked (new, D-RCV-60)
    Given the migration-run record shape of the contract
    When the P1 job view fake is asked for a migration run
    Then it answers one Job with type MIGRATION, the service, the schema, the version, the checksum, the drift result, startedAt, endedAt and a status of APPLIED or FAILED
    Then the owner of the shape is named as P1 rwb-source-data

  Scenario: AC5 A breaking change raises v2 and deprecates v1 (new, D-RCV-60)
    Given the contract published at v1
    When a rule changes so that a file which passed v1 would be refused
    Then the contract is published as v2 and v1 is marked deprecated with a removal date
    Then both versions are available to the services for the deprecation window

  Scenario: AC6 No business value and no personal data in the contract or its fixtures (new, D-RCV-60)
    Given the contract document and its 25 fixtures
    When they are scanned for business values and personal data
    Then no threshold, code list, seed row, name, address, identity number or contact point is present
    Then every fixture uses a synthetic identifier only
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | A migration file is named `V<seq>__<story>_<name>.sql`, with a four-digit sequence taken in merge order inside the service | RWB-E1-044 build rule (D-RCV-28); ADR-021 |
| BR2 | Line 1 of a migration file is `-- Story: <story key>`, and exactly one story key appears in the file | RWB-E1-044 BR3 |
| BR3 | A story key appears in the files of exactly one service; a key repeated across services is refused | ADR-021; DP-15 |
| BR4 | The schema is referenced only as `${schema}` and is fed by `RWB_SCHEMA`; a literal schema name is refused | RWB-E1-044 BR2; DP-01 |
| BR5 | The history table is the default `flyway_schema_history` inside the service's own schema; no shared history table | ADR-021; Arch v5 slide 29 |
| BR6 | Each service has one `V0001` baseline that creates its own objects and is applied once per environment | DP-15 |
| BR7 | PROD runs forward only: no clean, no undo file; a fix is a new version; an applied file is never edited | RWB-E1-044 BR4, BR5 |
| BR8 | No foreign key into `public` and no cross-schema reference in any migration; the boundary test fails the build | RWB-E1-044 BR8; Arch v5 slide 29 |
| BR9 | Each service migrates with its own account from the key store; the account is a secret reference, never a value in the contract | Arch v5 slide 29; NFR-052 |
| BR10 | A rule change that would refuse a file which passed the published version raises the contract to the next major version | Arch v5 slide 42 notes (BACKWARD compatibility) |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The nine elements and the 19 parameter sets are described | In review |
| In review | Service teams sign off | The fixtures and the six contract tests are accepted | Baselined at v1 |
| Baselined at v1 | Clarifying change | No file that passed v1 is refused | Baselined at v1 |
| Baselined at v1 | Breaking change | A file that passed v1 would be refused | Baselined at v2, v1 deprecated |
| Baselined at v2 | Deprecation window closed | The removal date is reached | v1 retired |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the platform template | Owns the contract document, the fixtures and the contract tests; tags the baseline |
| Solution architect | Approves a breaking change and the new major version |
| ACE database administrator | Confirms the 19 schema values and the per-service login rule |
| Platform library owner | Owns the Flyway module and the golden pipeline in which the contract test runs |
| Data steward | Confirms that no business value and no personal data appear in the contract or its fixtures |

The contract artefact location and the owner of the Flyway configuration module (the platform template or each service) are Not specified in the source documents (GAP-1422; ASM-2490).

### 11. Data

The contract declares rules and schema values, not business values.

| # | Service | Schema | Login |
|---|---|---|---|
| 1 | rwb-case | rwb_case | rwb_case |
| 2 | rwb-decision | rwb_decision | rwb_decision |
| 3 | rwb-access | rwb_access | rwb_access |
| 4 | rwb-deviation | rwb_deviation | rwb_deviation |
| 5 | rwb-source-data | rwb_source_data | rwb_source_data |
| 6 | rwb-reporting | rwb_reporting | rwb_reporting |
| 7 | rwb-agent | rwb_agent | rwb_agent |
| 8 | rwb-integration | rwb_integration | rwb_integration |
| 9 | rwb-document | rwb_document | rwb_document |
| 10 | rwb-comms | rwb_comms | rwb_comms |
| 11 | rwb-payment | rwb_payment | rwb_payment |
| 12 | rwb-partner | rwb_partner | rwb_partner |
| 13 | rwb-valuation | rwb_valuation | rwb_valuation |
| 14 | rwb-treatment | rwb_treatment | rwb_treatment |
| 15 | rwb-guarantee | rwb_guarantee | rwb_guarantee |
| 16 | rwb-litigation | rwb_litigation | rwb_litigation |
| 17 | rwb-asset | rwb_asset | rwb_asset |
| 18 | rwb-debtsale | rwb_debtsale | rwb_debtsale |
| 19 | rwb-writeoff | rwb_writeoff | rwb_writeoff |

The 19 schema values are those of Arch v5 slide 41 and Template and Rules §R4; the login carries the schema name, as slide 29 shows for `rwb_case`, `rwb_source_data` and `rwb_litigation`. No table is declared by the contract: the history table is Flyway's default inside each service's own schema and is not in the Logical Data Model.

### 12. Contract

#### 12.1 REST operations provided

None. This contract provides no REST operation; it defines file, schema and record rules only.

#### 12.2 REST operations consumed

None. The contract defines no runtime call: the run record is written by the deployment path of RWB-PLT-E1044-OPS against the P1 job view, and this story fixes only its shape.

#### 12.3 Events published

None. No event is published by a migration contract.

#### 12.4 Events consumed

None. No event is consumed by a migration contract.

#### 12.5 Workflows and activities

None. Migrations are not Temporal workflows or activities.

#### 12.6 Schedules

None. There is no schedule; the run is triggered by service start and by the pipeline step.

#### 12.7 Tables owned

None. The contract owns no table; Flyway creates `flyway_schema_history` inside each service's own schema.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Migration fixture of RWB-PLT-E1044-CON | 19 valid parameter sets, one per service, and 6 forbidden fixtures, each with its expected refusal and the expected file and line | Every service pipeline, RWB-PLT-E1044-APP-2, RWB-PLT-E1044-OPS |
| P1 job view fake | One `Job` with `type=MIGRATION`, the service, the schema, the version, the checksum, the drift result, `startedAt`, `endedAt` and a status of APPLIED or FAILED | RWB-PLT-E1044-APP-2, RWB-PLT-E1044-OPS, contract tests |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | The contract defines no runtime call; the run record is consumed by the deployment path |
| Kafka | None | No topic and no event in this contract |
| Temporal | None | No workflow, activity or schedule |
| File | 25 fixture files | 19 valid parameter sets and 6 forbidden fixtures, all synthetic, used by the contract test |

### 13. Solution plan

**Deliverables.** The migration contract document, the 19 parameter sets, the 25 fixtures, the six contract tests and the published run-record shape.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-14 | `rwb.p<n>.` or `rwb.casewf.` topic names | `rwb.<short>.events.v1`; naming library | H RWB-PLT-E1047-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Write the contract with the nine elements of section 4 and the 19 parameter sets of section 11.
2. Write the 19 valid fixtures, one per service, each naming the schema only as `${schema}`.
3. Write the 6 forbidden fixtures, one per refusal, each with its expected message, file and line.
4. Write the contract test that runs every fixture through the lint and the boundary test and compares the refusal with the expectation.
5. Publish the run-record shape and the P1 job view fake.
6. State the versioning rule and the deprecation window.
7. Tag the baseline and hand it to the app, deployment and service stories.

**Done when.** The contract validates, the six contract tests pass against the 25 fixtures, the 19 parameter sets resolve the 19 schemas and RWB-PLT-E1044-APP-2 and RWB-PLT-E1044-OPS have accepted the baseline.

The contract artefact location and the owner of the Flyway configuration module are Not specified in the source documents (GAP-1422; ASM-2490); the contract is written to be readable from the platform template and from each service until the point is closed.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-016 | A fixture breaks a rule, a parameter set resolves outside the 19 schemas, or a drift is found | Schema check failed in {schema}: {object}. The deployment was stopped. |
| MSG-P4-002 | A role without Platform administration R reads the migration runs | You cannot {action} here. Your role does not include it. |

MSG-P3-016 is the message of RWB-E1-044, carried unchanged. The contract test prints the rule, the file and the line before the message.

### 15. Screens and states

No screen. The contract is read by the service teams, the pipeline and the Flyway module. The run record it defines appears on SCR-44 Interface and job monitor through the P1 job view, in state Running, Failed or Complete.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-E1044-CON-01 | AC1 | Contract | The contract document validates; the nine elements are present and owned |
| TC-PLT-E1044-CON-02 | AC2 | Contract | Six forbidden fixtures, each refused with MSG-P3-016, the file and the line |
| TC-PLT-E1044-CON-03 | AC3 | Component | 19 parameter sets over one file; 19 schemas resolved, no literal schema name |
| TC-PLT-E1044-CON-04 | AC4 | Contract | The run-record shape and the P1 job view fake answer one Job with type MIGRATION |
| TC-PLT-E1044-CON-05 | AC5 | Contract | A breaking rule change publishes v2 and deprecates v1 with a removal date |
| TC-PLT-E1044-CON-06 | AC6 | Component | Scan of the document and the 25 fixtures; no business value, no personal data |

### 17. Guardrails

- No business value in the contract or its fixtures: no threshold, code list or seed row.
- No personal data in a fixture, an example or a test: synthetic identifiers only.
- The contract names the 19 schema values and no other schema; it never documents another service's tables.
- The schema is `${schema}` everywhere in a migration; a literal schema name is a defect, not a style choice.
- No foreign key into `public` and no cross-schema reference, in the rule or in a fixture.
- The contract never carries a credential: the migration account is a secret reference in the key store.
- The contract is additive within a major version; a rule that refuses a file which passed before raises a new major version.

### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-001 | Recovery data held in 14 data products in the ACE database | The 19 schema values and the per-service Flyway rule | TC-PLT-E1044-CON-01, TC-PLT-E1044-CON-03 |
| REQ-RDF-014 | Stage 2 data products exist before the first treatment goes live | One `V0001` baseline per service and the forward-only rule | TC-PLT-E1044-CON-01, TC-PLT-E1044-CON-05 |
| ADR-021 | Per-service Flyway and migration ownership | The file rule, the story header, the per-service history table and the boundary rule | TC-PLT-E1044-CON-02, TC-PLT-E1044-CON-04, TC-PLT-E1044-CON-06 |

### 19. Out of scope

- The Flyway configuration code and the per-service baselines (RWB-PLT-E1044-APP-2).
- The deployment pipeline, the drift gate, the key-store reading and the feature flag (RWB-PLT-E1044-OPS).
- The as-built monolith behaviour, kept word for word in RWB-PLT-E1044-APP.
- The creation of the 19 schemas and logins (RWB-PLT-NF06-DB) and the table definitions of each service.
- The business tables themselves and the 92-table split (RWB-PLT-NF06-DB and the per-service database stories).
