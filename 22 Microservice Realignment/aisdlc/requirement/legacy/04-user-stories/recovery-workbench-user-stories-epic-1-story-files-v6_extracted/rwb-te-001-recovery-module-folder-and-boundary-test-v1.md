<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB TE 001 Recovery module folder and boundary test v1.md -->
<!-- converted: 2026-11-16 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v6.zip!RWB TE 001 Recovery module folder and boundary test v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-001 Recovery module folder and boundary test

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


| Item | Value |
|---|---|
| Story key | RWB-TE-001 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraint Modular monolith) and section 5.2 |
| L3 process | All recovery processes |
| Decision | DL05 |
| Priority | Must |
| Depends on | None |
| Status | Ready for build |

## 1. Story

As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.

## 2. Business rationale

Three teams build in one ACE service. Without a checked boundary, a change in one team's code breaks another's, and a direct call to a core system could bypass the COLLINS and file load path. The skeleton gives each Workbench module one package with a published part and an internal part, and a test in every build refuses a call into another module's internal part, a cross-module table read and a direct system call outside the integration adapters. It meets REQ-DRI-006 and applies DT08, ADR-002 and DL05 (option B from 2 November: TechX creates the recovery module in its own package). The measure is the count of boundary violations merged to main, which must stay at zero.

## 3. Preconditions

- Access to the ACE repository for the TechX squads (DL36).
- DL05 is applied as option B from 2 November 2026: TechX creates the recovery module in its own package; the ACE team applies the module boundaries for the common and collection modules later.
- The common module's published packages are named in the module map. Until the ACE team names them, the map lists `..common.api..` (assumed; DL05).
- The ACE build runs the unit test phase on every pull request.

## 4. Flow

1. Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
2. Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.
3. Squad member: writes RecoveryBoundaryTest with the rules BR1 to BR5, reading the module map.
4. Squad member: writes the front end boundary rules for `src/modules/recovery`.
5. Squad member: wires the common module access check for `/api/recovery/v1/**` through RecoveryAccessGuard.
6. Pipeline: on each pull request runs the back end tests, including RecoveryBoundaryTest, and the front end dependency check.
7. Pipeline: fails the build when a rule is broken and prints the rule, the class and the class it depends on.
8. Squad member: fixes the call by going through the other module's `api` package or an application event, and the build passes.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A recovery class imports a collection module internal class | Build fails with the rule and both class names | Build log: boundary rule BND-1 broken | AC1 |
| X2 | A recovery module class imports another recovery module's internal class | Build fails | Build log: boundary rule BND-3 broken | AC3 |
| X3 | A class uses another module's entity or repository | Build fails | Build log: boundary rule BND-4 broken | AC4 |
| X4 | A class outside the integration adapters uses an HTTP or SFTP client | Build fails | Build log: boundary rule BND-5 broken | AC5 |
| X5 | A recovery screen imports a collection screen | Front end build fails | Build log: rule no-collection-import broken | AC6 |
| X6 | A new package is not in the module map | Build fails | Build log: package not in module map | AC7 |
| X7 | A request reaches a recovery endpoint from a role without the right | 403 through the common module access check | MSG-P4-002 | Access test TC-TE-001-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only repository access; every later story builds inside these folders |
| Negotiable | Module names and published packages are in the module map file, not in the test code |
| Valuable | The three teams can change their own module without breaking another |
| Estimable | Folders, one map file, one ArchUnit test class, one front end rule file |
| Small | Fits in one sprint with its tests |
| Testable | Each rule has a test fixture class that breaks it |

## 7. Acceptance criteria

```gherkin
Feature: Recovery module folder and boundary test

  Background:
    Given the module map lists modules P1 to P10 and S1 to S9 with their packages
    Given the published packages are "<module>.api" and any other package the module map lists for each recovery module, and "..common.api.." for the common module

  Scenario: AC1 Boundary enforced
    Given a class "recovery.casewf.internal.SampleService" that imports "collection.internal.CollectorRepository"
    When the pipeline runs
    Then the boundary test fails the build
    Then the build log names boundary rule BND-1, "SampleService" and "CollectorRepository"

  Scenario: AC2 Published interface allowed
    Given a class "recovery.casewf.internal.SampleService" that calls an interface in "common.api"
    When the pipeline runs
    Then the build passes

  Scenario: AC3 Recovery modules meet only through their api package
    Given a class in "recovery.integration.internal" that imports "recovery.decision.internal.DecisionLogRepository"
    When the pipeline runs
    Then the build fails with boundary rule BND-3
    When the class imports the published "recovery.decision.writer.DecisionLogWriter" instead
    Then the build passes

  Scenario: AC4 A module uses only its own tables
    Given a class in "recovery.integration.internal" that uses the entity "recovery.casewf.internal.RecoveryCaseEntity"
    When the pipeline runs
    Then the build fails with boundary rule BND-4

  Scenario: AC5 No direct call to a system of record
    Given a class in "recovery.casewf.internal" that uses "java.net.http.HttpClient"
    When the pipeline runs
    Then the build fails with boundary rule BND-5
    Then the same use in "recovery.integration.adapter" passes

  Scenario: AC6 Front end boundary
    Given a component in "src/modules/recovery/caselist" that imports "src/modules/collection/worklist/WorkList"
    When the front end build runs
    Then it fails with rule no-collection-import

  Scenario: AC7 A package missing from the module map
    Given a new package "recovery.vendorx" not in the module map
    When the pipeline runs
    Then the build fails with "package recovery.vendorx is not in the module map"
```

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | boundary rule BND-1: recovery classes depend on the collection module only through its published packages | DT08; ADR-002 |
| BR2 | boundary rule BND-2: recovery classes depend on the common module only through its published packages | DT07; DT08 |
| BR3 | boundary rule BND-3: a recovery module depends on another recovery module only through a package the module map lists as published for it, or an application event | Settled architecture; ADR-002 |
| BR4 | boundary rule BND-4: entities and repositories of a module are used only inside that module | Settled architecture: a module reads only its own tables |
| BR5 | boundary rule BND-5: only the packages the module map allows for client libraries use HTTP, SFTP or file transfer clients: `recovery.integration.adapter` (RWB-E1-007) for files, and the agent runtime client for the enterprise model endpoint INT-23 (RWB-TE-013); no recovery class calls a system of record | REQ-DRI-006; ADR-005 |
| BR6 | Module names, packages and published packages are read from the module map file, not written in the test | Principle 1 applied to build configuration |

The R-BND codes are the names of the boundary test rules in this story. They are not routing rules.

## 9. State transitions

None. This story does not change a case status. It changes the build result of a pull request from passed to failed when a rule is broken.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Create the folders, the module map and the boundary test |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the module map or to the boundary rules |
| ACE team | Names the common and collection published packages (DL05) |
| RW-PLATADM, platform administrator | Runs the pipeline |
| No approval level from the delegation of authority applies | The story takes no business decision |

## 11. Data

No business field is read or written. The boundary test reads source and compiled classes only.

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Item | Value |
|---|---|
| Trigger | Every pull request build and every build of main |
| Back end check | RecoveryBoundaryTest, run in the unit test phase |
| Front end check | The dependency rules for `src/modules/recovery`, run in the front end lint step |
| Output | Pass, or fail with the rule code, the class or file and the dependency that broke it |
| Idempotency | The same commit always gives the same result |
| Restart | Rerun the pipeline; the check holds no state |

**Recovery side of the published access check**

```java
// Wired for /api/recovery/v1/**; calls the common module access check (published interface, INT-34)
void RecoveryAccessGuard.require(String capabilityArea, Right right, ScopeTarget target);
//   throws AccessDeniedException mapped to 403 Problem with messageCode MSG-P4-002
```

## 13. Solution plan

**Package.** Back end folder `ace-service/src/main/java/<ACE base package>/recovery/`, with one package per module: `dataengine` (P1), `integration` (P2), `casewf` (P3), `access` (P4), `dochub` (P5), `comms` (P6), `decision` (P7), `payments` (P8), `reporting` (P9), `agent` (P10), `valuation` (S1), `treatment` (S2), `guarantee` (S3), `litigation` (S4), `asset` (S5), `debtsale` (S6), `writeoff` (S7), `deviation` (S8), `partner` (S9). Each holds `api` for its published interfaces and `internal` for the rest; a story that publishes from another package, for example `recovery.casewf.allocation` (RWB-E1-020) or `recovery.decision.writer` (RWB-E1-027), lists that package as published in the module map. Front end folder `src/modules/recovery/` (ADR-006, DL07).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| recovery-modules.yaml | Rule table | Module code, package, published packages, allowed client libraries |
| RecoveryBoundaryTest | Service | ArchUnit rules boundary rule BND-1 to boundary rule BND-5 built from the module map |
| ModuleMapLoader | Service | Reads the map; fails when a recovery package is not listed (AC7) |
| Boundary fixtures | Service | Test-only classes under `src/test` that break each rule, run with the rule in expect-failure mode |
| RecoveryAccessGuard | Service | Calls the common module access check for every recovery endpoint |
| dependency rule file | Rule table | Front end rules: no import from `src/modules/collection`, imports from `src/common` only through its public index |

**Database.** None.

**Configuration and reference data.** The module map file, owned by the TechX tech leads through code owners (RWB-TE-002). The common module published package names come from the ACE team (DL05).

**Build steps**

1. Create the 19 module packages with `api` and `internal`, a package-info file each, and the front end folder.
2. Write recovery-modules.yaml and ModuleMapLoader with a test for AC7.
3. Write RecoveryBoundaryTest rules boundary rule BND-1 to boundary rule BND-5 with one breaking fixture per rule (AC1, AC3 to AC5).
4. Write the passing fixture that calls a common module published interface (AC2).
5. Add the front end dependency rules and a breaking fixture (AC6).
6. Wire RecoveryAccessGuard with a test-only controller declared Case record R and the access test.
7. Add both checks to the pull request pipeline and confirm a failing fixture blocks a merge.

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The tests in section 16 pass, and the pipeline of main shows the boundary test in its unit test report.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A boundary rule is broken | Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event. |
| Build log | A package is not in the module map | package {package} is not in the module map |
| MSG-P4-002 | A role without the right calls a recovery endpoint | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard.

## 15. Screens and states

No screen in this story. A developer reads the result in the pull request checks and the build log.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-001-01 | AC1, BR1 | System | Fixture importing a collection internal class |
| TC-TE-001-02 | AC2, BR2 | System | Fixture calling a common module published interface |
| TC-TE-001-03 | AC3, BR3 | System | Fixture importing recovery.decision.internal, then recovery.decision.writer |
| TC-TE-001-04 | AC4, BR4 | System | Fixture using another module's entity |
| TC-TE-001-05 | AC5, BR5 | System | HttpClient in casewf and in the integration adapter package |
| TC-TE-001-06 | AC6 | System | Front end fixture importing a collection component |
| TC-TE-001-07 | AC7, BR6 | System | Package recovery.vendorx not in the map |
| TC-TE-001-08 | Access | Access | RW-REFADM calls the test-only Case record R endpoint; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code; module names and packages are in the module map.
- No personal data in logs, tests or prompts; fixtures hold class names only.
- No read of another module's tables; this story builds the check that enforces it.
- The breaking fixtures stay in `src/test` and never ship.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 5.2 and section 7 | None | All recovery processes | None | TC-TE-001-01 to TC-TE-001-08 |

## 19. Out of scope

- Code owners for the recovery folders: RWB-TE-002.
- Types and contract tests from the API specification: RWB-TE-003.
- Boundaries inside the common and collection modules: the ACE team under DL05 option A.
- The integration adapter pattern itself: RWB-E1-007.
