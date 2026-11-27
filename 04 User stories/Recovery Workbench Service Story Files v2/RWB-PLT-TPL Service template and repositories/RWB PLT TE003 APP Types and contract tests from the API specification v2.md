# RWB-PLT-TE003-APP Types and contract tests from the API specification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE003-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-003 |
| Legacy disposition | Preserved + delta |
| Build status | In build |
| Size | Not sized in the story; the squad sizes it at refinement |
| Patterns applied | DP01, DP07, DP08, DP13, DP19 |
| Parallel lane | L-PLT-TPL-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Contract version | /v1 (path version; full contract version: Not specified in the source documents (DOR-RWB-PLT-TE003-APP-23)) |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-019, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-TE-003 word for word and re-pointed at the platform template; sections 12 and 13 of the as-built story are kept under "As built (monolith)" and the microservice delta is RWB-PLT-TE003-APP-2. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-TE003-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (7 resolved, 26 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

### 2. Business rationale

The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.

### 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the boundary test exist; the generated packages are listed in the module map as shared.
- The API specification is held in the repository at `api/recovery-api.yaml`, base path /api/recovery/v1, with x-module, x-capability and x-first-release on every operation.
- Target API file layout (file names, folder, index format and per-service package names): Not specified in the source documents (GAP-1433).
- The permission matrix seed (roles.txt, loaded as the role and permission tables by RWB-E1-037) is available to tests.
- The build property `rwb.release` names the release being built: E1 for 30 November 2026.

### 4. Flow

1. Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the build.
2. Build: generates the Spring server interfaces and models from the specification.
3. Build: generates the TypeScript types and the typed client for the front end.
4. Build: compiles the service against the generated interfaces and the front end against the generated types.
5. Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.
6. Contract test: calls each implemented operation with its fixture and validates the request and the response against the specification.
7. Access test: calls each operation as a role whose permission lacks the declared right and expects 403 with messageCode MSG-P4-002.
8. Build: reports passed, failed and pending operations; any failure fails the build.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response no longer matches the specification | Contract test fails naming the operation and the JSON path | Build log: contract broken | AC2 |
| X2 | The specification breaks a lint rule | Build fails before generation | Build log: lint rule broken | AC3 |
| X3 | An operation returns a status not in its specification | Contract test fails | Build log: undocumented status | AC4 |
| X4 | An operation of the current release has no implementation | Build fails | Build log: operation has no implementation | AC5 |
| X5 | An operation of a later release has no implementation | Listed as pending; build passes | Build log: pending | AC6 |
| X6 | The front end uses a field removed from the specification | Front end type check fails | Build log: type error | AC7 |
| X7 | An operation answers 200 to a role without the declared right | Build fails | Build log: access not enforced | AC8 |
| X8 | A role without the right calls an operation | 403 Problem with MSG-P4-002 | MSG-P4-002 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the folders of RWB-TE-001 and the specification file |
| Negotiable | Generator settings are build configuration; the rules tested come from the specification |
| Valuable | Screens and services stay in step with one file; every endpoint enforces its right |
| Estimable | Two generators, one lint rule set, one parameterized test class |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below uses one fixture operation that breaks it |

### 7. Acceptance criteria

```gherkin
Feature: Types and contract tests from the API specification

  Background:
    Given the build property rwb.release is "E1"
    Given operation getCasesCaseidTimers is first in E1 with capability Case record R

  Scenario: AC1 Types generated (legacy RWB-TE-003 AC1)
    Given a change to the OpenAPI file that adds property "warnAt" to schema Timer
    When the build runs
    Then the generated server model and the front end type for Timer both hold "warnAt"
    Then the service and the front end compile against them

  Scenario: AC2 Contract broken (legacy RWB-TE-003 AC2)
    Given the implementation of getCasesCaseidTimers returns "escalationLevel" as the text "two"
    When the contract tests run
    Then the build fails
    Then the report names getCasesCaseidTimers and the path "$[0].escalationLevel"

  Scenario: AC3 The specification is checked before generation (legacy RWB-TE-003 AC3)
    Given an operation in the file with no x-capability
    When the build runs
    Then it fails at the lint step naming the operation

  Scenario: AC4 An undocumented status fails (legacy RWB-TE-003 AC4)
    Given the implementation of getCasesCaseidTimers returns 400 for an unknown case
    Given the specification lists 200, 401, 403, 404 and 503 only
    When the contract tests run
    Then the build fails with "undocumented status 400" for getCasesCaseidTimers

  Scenario: AC5 A current operation with no implementation fails (legacy RWB-TE-003 AC5)
    Given operation getAdminJobs is first in E1 and has no controller method
    When the build runs
    Then it fails with "getAdminJobs has no implementation"

  Scenario: AC6 A later operation is pending (legacy RWB-TE-003 AC6)
    Given operation postQueuesQueueidPlacements is first in E2 and has no controller method
    When the build runs for release E1
    Then the build passes
    Then the report lists postQueuesQueueidPlacements as pending

  Scenario: AC7 The front end cannot use a removed field (legacy RWB-TE-003 AC7)
    Given the file removes property "legalHold" from schema Case
    Given the case record screen reads "legalHold"
    When the front end build runs
    Then the type check fails naming the file and the line

  Scenario: AC8 An endpoint that skips its access check fails the build (legacy RWB-TE-003 AC8)
    Given the rwb-access contract mock returns RW-REFADM holding no Case record right
    Given the implementation of getCasesCaseidTimers does not call the access check
    When the access tests run with role RW-REFADM, which holds no Case record right
    Then the operation answers 200
    Then the build fails with "access not enforced" for getCasesCaseidTimers

  Scenario: AC9 A role without the right is refused with MSG-P4-002 (new, D-RCV-60)
    Given the rwb-access contract mock returns RW-REFADM holding no Case record right
    When RW-REFADM calls getCasesCaseidTimers
    Then the operation answers 403 with the Problem schema and MSG-P4-002
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The OpenAPI file is the only source of endpoints, request and response schemas | API specification; TSD P2 appendix T-A |
| BR2 | Every operation carries operationId, x-module, x-capability with area and right, and x-first-release; every error response uses the Problem schema | API specification |
| BR3 | Every operation first in the current release or earlier has an implementation and a passing contract test | AC-P2-001-01; REQ-DRI-007 |
| BR4 | Every operation refuses a role whose permission lacks the declared right with 403 and messageCode MSG-P4-002 | REQ-ACA-003; CTL-09 |
| BR5 | Generated code is produced at build time and is not edited by hand | ADR-006 |

### 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a contract or access test fails.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Change the specification and the implementations; run the build |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the specification file |
| RW-SECADM, security administrator | Owns the permission matrix that the access tests read |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

No business field is read or written. Contract tests run against synthetic fixtures in an in-memory test database.

Field IDs are those in the Logical Data Model and Data Dictionary.

| Fixture | Covers | Value in the story |
|---|---|---|
| Specification change adding warnAt to Timer | TC-TE-003-01 | Property warnAt on schema Timer |
| Fixture returning text for escalationLevel | TC-TE-003-02 | escalationLevel returned as text two |
| Operation with no x-capability | TC-TE-003-03 | Operation with no x-capability in the file |
| Fixture returning 400 not in the specification | TC-TE-003-04 | Status 400 for an unknown case; specification lists 200, 401, 403, 404 and 503 only |
| getAdminJobs with no implementation | TC-TE-003-05 | Release E1 |
| postQueuesQueueidPlacements first in E2 | TC-TE-003-06 | Release E2 |
| Property legalHold removed from Case | TC-TE-003-07 | Case screen reads legalHold |
| Fixture controller with no access check | TC-TE-003-08 | getCasesCaseidTimers |
| RW-REFADM calls getCasesCaseidTimers | TC-TE-003-09 | RW-REFADM holds no Case record right |

### 12. Contract

#### 12.1 REST operations provided

None. This story provides no REST operation of its own: it generates each service's server interfaces from that service's OpenAPI 3.1 file and tests every implemented operation against the same file, so the operations it governs are published by the 19 service contract stories under the base path `/api/recovery/<short>/v1` (DP-13). It builds against three platform contracts and two service contracts, and the Ownership Map is the only source of their owners: RWB-PLT-E1043-CON (reference data; the rows belong to P3 rwb-case under the §R5.5 DP-07 ruling and the Ownership Map entries `lov_value`, `reference_row` and `reference_version`), RWB-PLT-E1037-CON (authorise and guard; the rows belong to P4 rwb-access — `role`, `permission`, `masking_rule` and `delegation_limit`), RWB-PLT-N001-CON (gateway-bff composite route; gateway-bff is shared platform and not one of the 19 services, so the Ownership Map carries no service row for it), RWB-P3-E1043-CON (owner P3 rwb-case) and RWB-P4-E1037-CON (owner P4 rwb-access).

#### 12.2 REST operations consumed

None. The story consumes no service operation at runtime: the two service contracts above are consumed only as fakes inside the build (section 12.8), and the three platform contracts supply the guard library, the reference rows and the gateway route. No source document fixes the path of any of them, so no path is written here.

#### 12.3 Events published

None. A build check publishes no event, and the outbox is not involved.

#### 12.4 Events consumed

None. A build check consumes no event.

#### 12.5 Workflows and activities

None. The lint, the two generators and the two test classes run as build steps, not inside a Temporal workflow or activity.

#### 12.6 Schedules

None. The build runs on every pull request and every build of main; there is no schedule.

#### 12.7 Tables owned

None. The story owns no table: the permission matrix the access test reads is P4 rwb-access data, the lists and code values the contract test uses are P3 rwb-case reference data, and the fixtures are synthetic rows in an in-memory test database.

#### 12.8 Contract fakes

None. This story publishes no fake of its own: it consumes the authorise and guard fixture of RWB-PLT-E1037-CON (rows of P4 rwb-access, including role RW-REFADM holding no Case record right), the reference-data fixture of RWB-PLT-E1043-CON (rows of P3 rwb-case, so neither the fixtures nor the generated code hold a business value) and the gateway-bff route fixture of RWB-PLT-N001-CON (shared platform, built from the service answers).

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None at runtime; 2 consumed through fakes | Authorise contract of rwb-access (RWB-P4-E1037-CON through RWB-PLT-E1037-CON) and reference data of rwb-case (RWB-P3-E1043-CON through RWB-PLT-E1043-CON) |
| Kafka | None | No event is published or consumed |
| Temporal | None | The story is a build check |
| File | None | The specification files are read from the repository; no claim-check file is used |

### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**As-built component set unchanged.** The seven components of the as-built plan stay as built: the recovery-api rule set, the server generator configuration, the front end generator script, `OperationCatalog`, `RecoveryContractTest`, `RecoveryAccessContractTest` and `ContractFixtures`. This story changes none of them. The microservice delta starts in RWB-PLT-TE003-APP-2: the single OpenAPI 3.1 file becomes one file per service plus one for gateway-bff and an index, generation and the contract test run in each service's own pipeline against its own file at `/api/recovery/<short>/v1` (DP-13), the access test uses the authorise contract of rwb-access (DP-08), and composite screen operations are tested in the gateway-bff file (DP-19).

**Done when.** The nine test cases of section 16 still pass against the platform template, and the delta is delivered by RWB-PLT-TE003-APP-2. The legacy level `System` in section 16 maps to `Contract` for TC-TE-003-01 to TC-TE-003-07, and the legacy `Access` test maps to `End to end` for TC-TE-003-08 and TC-TE-003-09.

The target file layout, the index format and the per-service generated package names are Not specified in the source documents (GAP-1433; ASM-2519); this story keeps the as-built packages and generator settings exactly as built.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A response does not match | contract broken: {operationId} at {path}: {reason} |
| Build log | A status is not specified | undocumented status {status} for {operationId} |
| Build log | No implementation for the current release | {operationId} has no implementation |
| Build log | An operation answers a role without the right | access not enforced for {operationId} |
| MSG-P4-002 | The expected refusal in each access test | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard.

### 15. Screens and states

No screen in this story. Developers read the report in the build artifacts.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-003-01 | AC1, BR1, BR5 | Contract | Specification change adding warnAt to Timer |
| TC-TE-003-02 | AC2, BR3 | Contract | Fixture returning text for escalationLevel |
| TC-TE-003-03 | AC3, BR2 | Contract | Operation with no x-capability |
| TC-TE-003-04 | AC4, BR3 | Contract | Fixture returning 400 not in the specification |
| TC-TE-003-05 | AC5, BR3 | Contract | getAdminJobs with no implementation in E1 |
| TC-TE-003-06 | AC6 | Contract | postQueuesQueueidPlacements first in E2 |
| TC-TE-003-07 | AC7, BR1 | Contract | legalHold removed from Case |
| TC-TE-003-08 | AC8, BR4 | End to end | Fixture controller with no access check |
| TC-TE-003-09 | AC9, Access | End to end | RW-REFADM calls getCasesCaseidTimers; refused with MSG-P4-002 |

The legacy level `System` maps to `Contract` for TC-TE-003-01 to TC-TE-003-07 and the legacy `Access` test maps to `End to end` for TC-TE-003-08 and TC-TE-003-09; the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code or in a test: capability areas and rights come from the authorise contract of rwb-access and the permission matrix, and lists come from the reference-data contract of rwb-case (DP-07, DP-08).
- No personal data in logs, tests, prompts or report artefacts; fixtures are synthetic and the report holds operation names only.
- The OpenAPI file of a service is the only source of its operations, request and response schemas; generated code is never edited by hand, and a change goes into the file (DP-13).
- One file per service and one base path `/api/recovery/<short>/v1` per service; the story never writes a path of another service and never names a platform path.
- No read of another service's tables; the access test reads rights through the authorise contract and the reference lists through the reference-data contract (DP-01).
- Composite screen operations belong to the gateway-bff route contract, not to a service file (DP-19).
- The contract test and the access test run in the pipeline of the service that owns the file, and a failing operation fails that build.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | Business Requirements Program, section 5.2 | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2) | All recovery processes | None | TC-TE-003-01 to TC-TE-003-07 |
| REQ-ACA-003 | The permission matrix is the only source of what a role may do | Business Requirements Program, section 5.4 | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2) | All recovery processes | None | TC-TE-003-08, TC-TE-003-09 |

### 19. Out of scope

- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.

## As built (monolith)

#### 12. Contract

| Item | Value |
|---|---|
| Input | `api/recovery-api.yaml` (OpenAPI 3.1, base path /api/recovery/v1) |
| Lint | Recovery rule set for BR2, run first |
| Server generation | Spring interfaces and models, interface only, Spring Boot 3, one interface per tag, into the shared generated package listed in the module map |
| Front end generation | TypeScript types and a typed fetch client into `src/modules/recovery/api/generated` |
| Contract test | One success test per implemented operation: request and response validated against the specification, including status, content type and schema |
| Access test | One test per implemented operation: a role whose letters in the declared capability area lack the right, taken from the permission matrix seed, expects 403, `application/problem+json` and messageCode MSG-P4-002 |
| Output | A report of passed, failed and pending operations in the build artifacts |
| Trigger | Every pull request and every build of main |
| Idempotency | The same commit gives the same generated code and the same result |

#### 13. Solution plan

**Package.** Generated server code in `<ACE base package>.recovery.generated.web` and `<ACE base package>.recovery.generated.model`; tests in `ace-service/src/test/java/<ACE base path>/recovery/contract`; front end output in `ace-web/src/modules/recovery/api/generated`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| recovery-api rule set | Rule table | Lint rules for BR2 |
| Server generator configuration | Job | Build plugin settings for the Spring interfaces and models |
| Front end generator script | Job | Generates the types and the client before the type check |
| OperationCatalog | Service | Reads the operations, their release and their capability from the file |
| RecoveryContractTest | Service | Parameterized success tests with the specification validator |
| RecoveryAccessContractTest | Service | Parameterized 403 tests choosing a role without the right from the permission matrix seed |
| ContractFixtures | Repository | Synthetic fixture data per operation |

**Database.** None. Tests use an in-memory PostgreSQL-compatible test database with synthetic rows.

**Configuration and reference data.** The build property `rwb.release`; the permission matrix seed; fixture data per operation, synthetic only.

**Build steps**

1. Add the lint step and the rule set; prove it fails on an operation with no x-capability (AC3).
2. Add the server generator; make one existing controller implement its generated interface (AC1).
3. Add the front end generator and the type check (AC1, AC7).
4. Write OperationCatalog and the check for current operations with no implementation (AC5, AC6).
5. Write RecoveryContractTest with the specification validator (AC2, AC4).
6. Write RecoveryAccessContractTest with role selection from the permission matrix seed (AC8 and the access test).
7. Publish the report in the build artifacts.

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The tests in section 16 pass, and the report for release E1 shows every E1 operation passed or pending with a named story.
