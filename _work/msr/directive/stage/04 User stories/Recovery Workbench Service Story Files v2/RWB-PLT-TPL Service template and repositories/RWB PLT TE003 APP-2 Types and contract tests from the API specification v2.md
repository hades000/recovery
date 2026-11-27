# RWB-PLT-TE003-APP-2 Types and contract tests from the API specification

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE003-APP-2 |
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
| Patterns applied | DP01, DP07, DP08, DP13, DP19 |
| Parallel lane | L-PLT-TPL-M |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract version | v1 (the /v1 path, e.g. /api/recovery/case/v1; OpenAPI 3.1 document) |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-019, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (directive resolutions) |
| Size | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-16) |

**Change log.** D-RCV-60, 22 November 2026: delta copy of RWB-TE-003 for the platform template, one OpenAPI 3.1 file per service plus one for gateway-bff and an index, generation and the contract test in each service's own pipeline at its own base path (Arch v5 slides 11, 13, 14 and 41; DP-01, DP-07, DP-08, DP-13, DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-TE003-APP-2). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (8 resolved, 24 cross-document, 0 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **squad member (RW-TRIBE)**, I want **one OpenAPI 3.1 file per service, generated and contract-tested in that service's own pipeline at that service's own base path, with the access test reading the authorise contract of rwb-access and composite screen operations held in the gateway-bff file**, so that **a break in one provider's contract fails only that provider's build and no screen, service or test drifts from a file it does not own**.

### 2. Business rationale

The as-built story keeps one OpenAPI 3.1 file for the whole recovery API, 79 operations under one base path, generated into a shared package and tested once in one build. Arch v5 replaces that with 19 deployable services, each with its own base path, its own contract and its own release (slides 13, 14 and 41), and with a shared gateway-bff that composes the screens and is not one of the 19 (slide 20). One file for 19 owners means one owner's edit changes every build, one generated package holds every model, and a break in a service nobody touched stops the other 18. The delta keeps the as-built mechanism and changes the unit of ownership: one file per service plus one for the gateway-bff and an index, the lint and both generators reading only that file, the contract test running at that file's base path in that service's pipeline, and the access test asking the authorise contract of rwb-access instead of reading a seed in the same repository (DP-08). It supports REQ-DRI-007, because every interface still carries its contract test, and REQ-ACA-003, because every endpoint is still tested against the right its file declares and the permission matrix holds. The measure is the count of contract defects found in SIT, with a target of zero, and the blast radius of a failed build, which is one service.

### 3. Preconditions

- RWB-PLT-TE003-APP is in build: the recovery-api lint rule set, the server and front-end generators, `OperationCatalog`, `RecoveryContractTest`, `RecoveryAccessContractTest` and `ContractFixtures` exist and stay unchanged.
- Each of the 19 services has its short name and its base path `/api/recovery/<short>/v1` (§R4; Arch v5 slide 41), and each one owns its schema `rwb_<name>` (DP-01).
- The platform template supplies the reference-data contract RWB-PLT-E1043-CON, the authorise and guard contract RWB-PLT-E1037-CON and the gateway-bff route contract RWB-PLT-N001-CON, each with its fake; this story takes no build dependency on them and is Day 1 by rule (Template and Rules §R5.7).
- The permission matrix (P4 rwb-access data) and the lists (P3 rwb-case reference data) are reachable through their contracts and their fakes, never through a table read.
- The build property `rwb.release` names the release being built: E1 for 30 November 2026.

### 4. Flow

1. Split the single file: 19 files, one per service, one file for gateway-bff, and an index; every operation lands in exactly one file and keeps its operationId, x-module, x-capability and x-first-release unchanged.
2. Set each service file's base path to `/api/recovery/<short>/v1` and keep every error response on the Problem schema (DP-13).
3. Put the composite screen operations in the gateway-bff file only; a service file holds the operations of that service (DP-19).
4. Service pipeline: lint the service's own file with the recovery rule set; a missing operationId, x-capability or error response fails that build.
5. Service pipeline: generate the Spring server interfaces and models from that file, and the TypeScript types and typed client for the screens that read that service.
6. Service pipeline: contract test every operation of that file whose x-first-release is at or before `rwb.release`, at the service's own base path, against the same file.
7. Service pipeline: access test every implemented operation through the platform mock of RWB-PLT-E1037-CON, with a role the permission matrix does not give the declared right; expect 403 with messageCode MSG-P4-002.
8. gateway-bff pipeline: lint, generate and contract test the gateway-bff file the same way, including the composite screen operations.
9. Each pipeline publishes its own report and one aggregate report lists passed, failed and pending per service and per release, with the index refreshed for every file it holds.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An operation appears in two service files, or in none | The split check fails and names the operation and both files | Build log: operation not in exactly one file | AC1 |
| X2 | A service file loses the base path of its own service, or carries another service's base path | The lint fails the build of that service | Build log: base path not the service's own | AC2 |
| X3 | A response of one service no longer matches its own file | The contract test of that service fails and names the operation and the JSON path | Build log: contract broken | AC2, AC3 |
| X4 | Another service's build is red at the same time | It stays red for its own reason only; the two reports are separate | Build log: one report per service | AC3 |
| X5 | An operation answers 200 to a role the permission matrix gives no right | The access test fails that build | Build log: access not enforced | AC4 |
| X6 | A composite screen operation is written into a service file | The split check fails and names the operation and the gateway-bff file | Build log: composite operation in the wrong file | AC5 |
| X7 | Generated code carries a business value that the reference data holds | The build fails on the hard-coded value check | Build log: business value in generated code | AC6 |
| X8 | An operation of a later release has no implementation | Listed as pending for that service and that release; the build passes | Build log: pending | AC2 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the as-built components of RWB-PLT-TE003-APP and the 19 base paths; it reads no other story's code |
| Negotiable | The file names, the index format and the report layout are settled by the template owner; the ownership rule is fixed |
| Valuable | A contract break is found by the owner that caused it, in its own pipeline, and no other service waits |
| Estimable | A split check, a per-service pipeline wiring and three test classes wired to their own file |
| Small | Fits in one sprint with its tests, proved on two services first |
| Testable | Each criterion runs in a service pipeline against its own file and its fakes |

### 7. Acceptance criteria

```gherkin
Feature: One API specification file per service, generated and tested in its own pipeline

  Background:
    Given the as-built components of RWB-PLT-TE003-APP are in build and unchanged
    Given each service has its own base path /api/recovery/<short>/v1

  Scenario: AC1 The single file becomes 19 files, a gateway-bff file and an index (new, D-RCV-60)
    Given the single OpenAPI 3.1 file with 79 operations
    When the split runs
    Then 19 service files and one gateway-bff file are produced, plus an index
    Then every operation appears in exactly one file, with its operationId, x-module, x-capability and x-first-release unchanged
    Then each service file carries the base path of its own service

  Scenario: AC2 Generation and the contract test run in the service's own pipeline (new, D-RCV-60)
    Given the file of rwb-case at base path /api/recovery/case/v1
    When the rwb-case pipeline runs with rwb.release set to E1
    Then the lint and both generators read only that file
    Then the contract test validates every implemented operation of that file at that base path
    Then the report of the pipeline lists the passed, failed and pending operations of rwb-case only

  Scenario: AC3 A break in one service fails only that service's build (new, D-RCV-60)
    Given the response schema of an operation changes in the rwb-case file and the rwb-case controller does not
    When the pipelines of rwb-case and rwb-payment both run
    Then the rwb-case build fails naming the operation and the JSON path
    Then the rwb-payment build passes and its report is unchanged

  Scenario: AC4 The access test reads the authorise contract of rwb-access (new, D-RCV-60)
    Given the platform mock of RWB-PLT-E1037-CON returns role RW-REFADM holding no Case record right
    When the access test calls each operation of the rwb-case file
    Then each operation answers 403 with application/problem+json and messageCode MSG-P4-002
    Then no role, permission or masking row is copied into the service

  Scenario: AC5 Composite screen operations are tested in the gateway-bff file (new, D-RCV-60)
    Given a composite screen operation that merges the answers of rwb-case and rwb-source-data
    When the split runs
    Then the operation appears in the gateway-bff file and in no service file
    Then the gateway-bff pipeline contract tests it against the gateway-bff file
    Then it makes one hop to each owner and calls no service that calls another

  Scenario: AC6 No business list value is hard-coded (new, D-RCV-60)
    Given an operation whose answer carries a code value held in the reference data of rwb-case
    When RWB-P3-E1043-CON removes that value
    Then the generated code and the service compile unchanged
    Then the operation returns the list from the reference-data contract and the contract test reads the same list

  Scenario: AC7 The business rules of section 8 hold in the split files and pipelines (new, D-RCV-60)
    Given the split files, the generated code and the pipeline of each service
    Then an operation appears in exactly one file, and each service file carries only its own base path (BR1, BR3)
    Then operationId, x-module, x-capability and x-first-release are kept, and every error response uses the Problem schema (BR2)
    Then the lint, the generators and the contract test of a service read only that service's own file in its own pipeline (BR4)
    Then the access test asks the authorise contract of rwb-access, and a role without the declared right is refused with 403 and MSG-P4-002 (BR5)
    Then composite screen operations appear only in the gateway-bff file and are tested there (BR6)
    Then no business list value is written in generated code or in a test (BR7)
    Then a build of one service does not depend on the file, the generated code or the build result of another service (BR8)
```

### 8. Business rules

| ID | Rule | Source | Covered by |
|---|---|---|---|
| BR1 | One OpenAPI 3.1 file per service, one for gateway-bff and one index; an operation appears in exactly one file | Arch v5 slides 13, 14 and 41; Template and Rules §R8.4 | TC-PLT-TE003-APP2-01 |
| BR2 | Every operation keeps operationId, x-module, x-capability with area and right, and x-first-release; every error response uses the Problem schema | RWB-PLT-TE003-APP BR1, BR2; API specification | TC-PLT-TE003-APP2-07 |
| BR3 | Each service file carries the base path `/api/recovery/<short>/v1` of its own service and no other service's path | Arch v5 slides 11 and 41; DP-13 | TC-PLT-TE003-APP2-02 |
| BR4 | The lint, the server generator, the front-end generator and the contract test of a service read that service's own file only, in that service's own pipeline | DP-13; Arch v5 slide 20 (one template, contract tests in every build) | TC-PLT-TE003-APP2-02 |
| BR5 | The access test asks the authorise contract of rwb-access and reads the permission matrix; a role without the declared right is refused with 403 and messageCode MSG-P4-002 | RWB-PLT-TE003-APP BR4; REQ-ACA-003; DP-08 | TC-PLT-TE003-APP2-04 |
| BR6 | Composite screen operations belong to the gateway-bff file and are tested there; no service file holds a route that composes another service | Arch v5 slide 20 notes (one hop, never a service that calls another); DP-19 | TC-PLT-TE003-APP2-05 |
| BR7 | No business list value is written in generated code or in a test; lists come from the reference-data contract of rwb-case | DP-07; RWB-PLT-TE003-APP §17 | TC-PLT-TE003-APP2-06 |
| BR8 | A build of one service never depends on the file, the generated code or the build result of another service | Arch v5 slide 20 (each service released on its own); DP-13 | TC-PLT-TE003-APP2-03 |

### 9. State transitions

None. This story does not change a case status. It changes the build state of each service and of the gateway-bff: a file is linted, generated and tested in its own pipeline, and its state moves from pending to passed or failed without touching another service's state.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Change a service's file and its implementation; run that service's pipeline |
| TechX tech leads (code owners) | Approve a change to a service's file and to the index |
| RW-SECADM, security administrator | Owns the permission matrix that the access test reads through the authorise contract |
| Platform template owner | Owns the split check, the index and the aggregate report |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

No business field is read or written. The contract tests run against synthetic fixtures in an in-memory test database; the permission matrix stays in rwb-access and the lists stay in the reference data of rwb-case, read through their contracts and their fakes.

The location of the index file, the x-module value for gateway-bff operations and the report format across the 19 pipelines are Not specified in the source documents (GAP-1434; ASM-2520; ASM-2521); the defaults of this story are named in section 13. The target file names and folder, the format of the index and the generated package names are Not specified in the source documents (GAP-1433); the as-built names stay in RWB-PLT-TE003-APP section 13.

Field IDs are those in the Logical Data Model and Data Dictionary.

| Data item | Use in this story | Source |
|---|---|---|
| Business fields | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-7) | Section 11 text above |
| Test data | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-7) | Section 11 text above |
| Permission matrix | Stays in rwb-access; read through its authorise contract | DP-08 |
| Lists and code values | Stay in the reference data of rwb-case; read through its contract and fake | DP-07 |

### 12. Contract

#### 12.1 REST operations provided

None. The story provides no REST operation: it splits the specification into one file per service, one for gateway-bff and an index, and wires the generation and the tests of each file into the pipeline of its owner. The operations it governs are published by the 19 service contract stories at `/api/recovery/<short>/v1` (DP-13) and by the gateway-bff route contract RWB-PLT-N001-CON (DP-19).

#### 12.2 REST operations consumed

None at runtime. The tests consume two contracts through their fakes and write no path of their own: the authorise contract of P4 rwb-access, RWB-P4-E1037-CON, through the platform mock RWB-PLT-E1037-CON (DP-08), and the reference-data contract of P3 rwb-case, RWB-P3-E1043-CON, through the platform fixture RWB-PLT-E1043-CON (DP-07). No source document fixes the path of either one, so none is written here.

#### 12.3 Events published

None. A build check publishes no event.

#### 12.4 Events consumed

None. A build check consumes no event; the access and reference answers arrive through contract fakes, not through Kafka.

#### 12.5 Workflows and activities

None. The split check, the lint, both generators and the two test classes are pipeline steps, not Temporal workflows or activities.

#### 12.6 Schedules

None. Each service pipeline runs on every pull request and every build of main; the index and the aggregate report are refreshed by the pipeline, not by a schedule.

#### 12.7 Tables owned

None. The story owns no table: the rights it tests are P4 rwb-access data, the lists it reads are P3 rwb-case reference data, and the fixtures are synthetic rows in an in-memory test database.

#### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Platform mock of the authorise contract RWB-PLT-E1037-CON (rows of P4 rwb-access) | A role and the rights it holds, including role RW-REFADM holding no Case record right | RecoveryAccessContractTest of every service pipeline |
| Platform fixture of the reference-data contract RWB-PLT-E1043-CON (rows of P3 rwb-case) | The lists and code values a service file declares, so neither the generated code nor a test holds a business value | RecoveryContractTest and ContractFixtures |
| gateway-bff route fixture of RWB-PLT-N001-CON (shared platform) | The composite answer the screens read, built from the service answers | The gateway-bff pipeline and the front end type check |

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None at runtime; 2 consumed through fakes | Authorise contract of rwb-access (RWB-P4-E1037-CON through RWB-PLT-E1037-CON) and reference data of rwb-case (RWB-P3-E1043-CON through RWB-PLT-E1043-CON) |
| Kafka | None | No event is published or consumed |
| Temporal | None | The story is a set of pipeline steps |
| File | None | The 20 specification files and the index are read from the repository; no claim-check file is used |

### 13. Solution plan

**Deliverables.** The split check and the split of the single file into 19 service files, one gateway-bff file and an index; the per-service pipeline wiring of the lint, the server generator, the front-end generator, the contract test and the access test; the aggregate report per service and per release.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Build steps**

1. Write the split check: every operation of the single file lands in exactly one of the 20 files and keeps its four extensions; a duplicate or a missing operation fails (AC1).
2. Produce the 19 service files with the base path `/api/recovery/<short>/v1` of each service, the gateway-bff file with the composite screen operations, and the index (AC1, AC5).
3. Wire the lint, the server generator and the front-end generator into each service's pipeline so that each reads only its own file (AC2).
4. Wire the contract test at the service's own base path and prove that a change in one file fails only that file's build (AC2, AC3).
5. Wire the access test to the platform mock of RWB-PLT-E1037-CON and the permission matrix; prove the 403 with MSG-P4-002 (AC4).
6. Wire the gateway-bff pipeline for the composite screen operations and prove no service file holds one (AC5).
7. Add the hard-coded business value check against the reference-data fixture and prove a removed code value needs no code change (AC6).
8. Publish the aggregate report and refresh the index on every merge (AC1, AC2).

**Configuration and reference data.** The build property `rwb.release` per pipeline; the platform mock of the authorise contract and the fixture of the reference-data contract; the index refreshed from the 20 files; no value of a list is written in code.

**Done when.** The six test cases of section 16 pass for two services (rwb-case and rwb-payment) and for the gateway-bff file, every service in the template lints, generates and contract-tests its own file in its own pipeline, and the aggregate report shows passed, failed and pending per service and per release.

The location of the index file, the x-module value for gateway-bff operations and the report format across the 19 pipelines are Not specified in the source documents (GAP-1434; ASM-2520; ASM-2521); the defaults applied are the ones assumed in these steps and they change no rule of section 8.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | An operation is not in exactly one file | operation {operationId} in {n} files; expected 1 |
| Build log | A service file does not carry its own base path | base path {base} is not the service's own |
| Build log | A response does not match the service's own file | contract broken: {operationId} at {path}: {reason} |
| Build log | A composite screen operation sits in a service file | composite operation {operationId} belongs to the gateway-bff file |
| Build log | Generated code or a test holds a business value | business value {value} in generated code |
| MSG-P4-002 | The expected refusal in each access test | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard. MSG-P4-002 is the message of RWB-PLT-TE003-APP, carried unchanged.

### 15. Screens and states

No screen is named and no screen state is added: this story has no new screen and no new screen state. The aggregate report is a build artefact and lists, per service and per release, the operations passed, failed and pending, with the base path of the service and the file it was tested against. A composite screen operation appears in the gateway-bff part of the report, never in a service part.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE003-APP2-01 | AC1 | Contract | The single file with 79 operations; 19 service files, one gateway-bff file and the index; no operation twice |
| TC-PLT-TE003-APP2-02 | AC2 | Contract | The rwb-case file at /api/recovery/case/v1, rwb.release E1; report of that service only |
| TC-PLT-TE003-APP2-03 | AC3 | Component | A changed response schema in the rwb-case file; the rwb-payment build and report unchanged |
| TC-PLT-TE003-APP2-04 | AC4 | Contract | RW-REFADM with no Case record right from the platform mock; 403 and MSG-P4-002 |
| TC-PLT-TE003-APP2-05 | AC5 | Contract | One composite screen operation; present once, in the gateway-bff file, tested there |
| TC-PLT-TE003-APP2-06 | AC6 | Component | A code value removed from the reference data; the generated code and the service compile unchanged |
| TC-PLT-TE003-APP2-07 | BR2 | Contract | An operation without x-module or x-first-release, and an error response not using the Problem schema; the lint of the service fails |
| TC-PLT-TE003-APP2-08 | AC7 | Not specified in the source documents (NEWAC-RWB-PLT-TE003-APP-2-AC7) | Not specified in the source documents (NEWAC-RWB-PLT-TE003-APP-2-AC7) |

The as-built tests of this legacy key, with their Given, When and Then, stay in RWB-PLT-TE003-APP section 16 and in Recovery Workbench Test Cases v8.xlsx under the same test case ID.

### 17. Guardrails

- One file per service, one base path `/api/recovery/<short>/v1`, one pipeline; a service never reads, generates from or tests another service's file (DP-13).
- The OpenAPI file of a service is the only source of its operations, request and response schemas; generated code is never edited by hand (DP-01).
- No business value in generated code or in a test: rights come from the authorise contract of rwb-access and lists from the reference-data contract of rwb-case (DP-07, DP-08).
- No personal data in logs, tests, generated artefacts or report rows; fixtures are synthetic and the report holds operation names and base paths only.
- No read of another service's tables; the permission matrix and the reference data are reached through their contracts and fakes, never by a schema read (DP-01).
- Composite screen operations belong to the gateway-bff file and are tested there; no service file composes another service (DP-19).
- A build of one service never waits for, or is failed by, the file or the build of another service.
- The index and the aggregate report are produced by the pipeline from the files; neither is edited by hand.

### 18. Traceability

| Feature | L3 process | Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|---|---|
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | One contract test per service file, running at that service's own base path | TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-03 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | REQ-ACA-003 | The permission matrix is the only source of what a role may do | Access test through the authorise contract of rwb-access and the permission matrix; 403 and MSG-P4-002 | TC-PLT-TE003-APP2-04 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | DP-01 | Owner's schema `rwb_<name>`; never read another service's tables | Each service generated and tested against its own file and its own model; no schema read in a test | TC-PLT-TE003-APP2-02 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | DP-07 | Reference-data contract of rwb-case | Lists and code values read through RWB-P3-E1043-CON and its fixture; no business value in code | TC-PLT-TE003-APP2-06 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | DP-08 | Authorise contract of rwb-access and the guard library | Platform mock RWB-PLT-E1037-CON; refusal with 403 and MSG-P4-002 | TC-PLT-TE003-APP2-04 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | DP-13 | `/api/recovery/<short>/v1` | One file and one base path per service, tested in its own pipeline | TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-02 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | DP-19 | gateway-bff composite route | Composite screen operations in the gateway-bff file, tested there | TC-PLT-TE003-APP2-05 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Arch v5 slide 11 | OpenAPI 3.1 with `/v1` in the path, contract tests in every build | Per-service file, lint and contract test in each pipeline | TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-02 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Arch v5 slide 13 | One hop from the edge to the owner it needs | Composite operations tested in the gateway-bff file; no service calls a service | TC-PLT-TE003-APP2-05 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Arch v5 slide 14 | rwb-case and rwb-access contracts, the case and access answers | Case file at `/api/recovery/case/v1`; authorise through rwb-access | TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-04 |
| Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Not specified in the source documents (DOR-RWB-PLT-TE003-APP-2-2) | Arch v5 slide 41 | 19 services, one base path, one schema and one login each | 19 files, one base path each, one pipeline each | TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-03 |

### 19. Out of scope

- The preserved as-built generator and its packages, kept word for word in RWB-PLT-TE003-APP section 13 and in its "As built (monolith)" appendix.
- The per-service contract stories of each service epic, which own the operations, the request and response schemas and the fakes of their own file.
- The gateway route contract and its fakes: RWB-PLT-N001-CON.
- The permission matrix content: RWB-E1-037 in the legacy numbering.
- Contract tests for file interfaces: RWB-E1-007 in the legacy numbering.
- The build runner, the pipeline template and the deployment of a service (RWB-PLT-N004-OPS, RWB-PLT-NF01-OPS).
