<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB TE 003 Types and contract tests from the API specification v1.md -->
<!-- converted: 2026-11-04 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5/RWB TE 003 Types and contract tests from the API specification v1.md`  
> **Converted from:** Markdown (copied)

# RWB-TE-003 Types and contract tests from the API specification

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-003 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-007, REQ-ACA-003 |
| BRD section | Business Requirements Program, section 5.2 and section 5.4 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-TE-001 |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

## 2. Business rationale

The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.

## 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the boundary test exist; the generated packages are listed in the module map as shared.
- The API specification is held in the repository at `api/recovery-api.yaml`, base path /api/recovery/v1, with x-module, x-capability and x-first-release on every operation.
- The permission matrix seed (roles.txt, loaded as the role and permission tables by RWB-E1-037) is available to tests.
- The build property `rwb.release` names the release being built: E1 for 30 November 2026.

## 4. Flow

1. Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the build.
2. Build: generates the Spring server interfaces and models from the specification.
3. Build: generates the TypeScript types and the typed client for the front end.
4. Build: compiles the service against the generated interfaces and the front end against the generated types.
5. Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.
6. Contract test: calls each implemented operation with its fixture and validates the request and the response against the specification.
7. Access test: calls each operation as a role whose permission lacks the declared right and expects 403 with messageCode MSG-P4-002.
8. Build: reports passed, failed and pending operations; any failure fails the build.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X8 | A role without the right calls an operation | 403 Problem with MSG-P4-002 | MSG-P4-002 | Access test TC-TE-003-09 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the folders of RWB-TE-001 and the specification file |
| Negotiable | Generator settings are build configuration; the rules tested come from the specification |
| Valuable | Screens and services stay in step with one file; every endpoint enforces its right |
| Estimable | Two generators, one lint rule set, one parameterized test class |
| Small | Fits in one sprint with its tests |
| Testable | The test cases in section 16 use one fixture operation that breaks the rule |

## 7. Acceptance criteria

No business acceptance criteria. This story is an engineering enabler for generated types and API contract tests; its development-process criteria were removed on 4 November 2026.

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The OpenAPI file is the only source of endpoints, request and response schemas | API specification; TSD P2 appendix T-A |
| BR2 | Every operation carries operationId, x-module, x-capability with area and right, and x-first-release; every error response uses the Problem schema | API specification |
| BR3 | Every operation first in the current release or earlier has an implementation and a passing contract test | AC-P2-001-01; REQ-DRI-007 |
| BR4 | Every operation refuses a role whose permission lacks the declared right with 403 and messageCode MSG-P4-002 | REQ-ACA-003; CTL-09 |
| BR5 | Generated code is produced at build time and is not edited by hand | ADR-006 |

## 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a contract or access test fails.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Change the specification and the implementations; run the build |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the specification file |
| RW-SECADM, security administrator | Owns the permission matrix that the access tests read |
| No approval level from the delegation of authority applies | The story takes no business decision |

## 11. Data

No business field is read or written. Contract tests run against synthetic fixtures in an in-memory test database.

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

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

## 13. Solution plan

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

1. Add the lint step and the rule set; prove it fails on an operation with no x-capability.
2. Add the server generator; make one existing controller implement its generated interface.
3. Add the front end generator and the type check.
4. Write OperationCatalog and the check for current operations with no implementation.
5. Write RecoveryContractTest with the specification validator.
6. Write RecoveryAccessContractTest with role selection from the permission matrix seed, and the access test.
7. Publish the report in the build artifacts.

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The tests in section 16 pass, and the report for release E1 shows every E1 operation passed or pending with a named story.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A response does not match | contract broken: {operationId} at {path}: {reason} |
| Build log | A status is not specified | undocumented status {status} for {operationId} |
| Build log | No implementation for the current release | {operationId} has no implementation |
| Build log | An operation answers a role without the right | access not enforced for {operationId} |
| MSG-P4-002 | The expected refusal in each access test | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard.

## 15. Screens and states

No screen in this story. Developers read the report in the build artifacts.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-003-01 | BR1, BR5 | System | Specification change adding warnAt to Timer |
| TC-TE-003-02 | BR3 | System | Fixture returning text for escalationLevel |
| TC-TE-003-03 | BR2 | System | Operation with no x-capability |
| TC-TE-003-04 | BR3 | System | Fixture returning 400 not in the specification |
| TC-TE-003-05 | BR3 | System | getAdminJobs with no implementation in E1 |
| TC-TE-003-07 | BR1 | System | legalHold removed from Case |
| TC-TE-003-08 | BR4 | System | Fixture controller with no access check |
| TC-TE-003-09 | Access | Access | RW-REFADM calls getCasesCaseidTimers; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code: capability areas and rights come from the specification and the permission matrix.
- No personal data in logs, tests or prompts; fixtures are synthetic and the test report holds operation names only.
- No read of another module's tables; each module's controller implements its own generated interface.
- Generated code is never edited; a change goes into the specification.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | Business Requirements Program, section 5.2 | None | All recovery processes | None | TC-TE-003-01 to TC-TE-003-07 |
| REQ-ACA-003 | The permission matrix is the only source of what a role may do | Business Requirements Program, section 5.4 | None | All recovery processes | None | TC-TE-003-08, TC-TE-003-09 |

## 19. Out of scope

- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.
