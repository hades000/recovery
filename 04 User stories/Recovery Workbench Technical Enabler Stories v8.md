# Recovery Workbench Technical Enabler Stories v8

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60.

Realigned to the 19-service architecture (Arch v5). Each legacy story below lists its new linked stories; the full text of each new story follows. Release dates are tentative and unchanged.


## RWB-TE-001 Recovery module folder and boundary test

Legacy disposition: Preserved + delta.

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE001-APP | App development | RWB-PLT-TPL | L-PLT-TPL-J | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-PLT-TE001-APP-2 | App development | RWB-PLT-TPL | L-PLT-TPL-I | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE001-APP Recovery module folder and boundary test

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE001-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-001 |
| Legacy disposition | Preserved + delta |
| Build status | Built |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP16, DP19, DP20 |
| Parallel lane | L-PLT-TPL-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P2-E1007-CON, RWB-P10-TE013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-TE-001 word for word (sections 1 to 11, 14 to 16, 18 and 19), with the as-built contract and solution plan moved unchanged under "As built (monolith)" and sections 12, 13 and 17 written for the target; the microservice delta is RWB-PLT-TE001-APP-2. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.

##### 2. Business rationale

Three teams build in one ACE service. Without a checked boundary, a change in one team's code breaks another's, and a direct call to a core system could bypass the COLLINS and file load path. The skeleton gives each Workbench module one package with a published part and an internal part, and a test in every build refuses a call into another module's internal part, a cross-module table read and a direct system call outside the integration adapters. It meets REQ-DRI-006 and applies DT08, ADR-002 and DL05 (option B from 2 November: TechX creates the recovery module in its own package). The measure is the count of boundary violations merged to main, which must stay at zero.

##### 3. Preconditions

- Access to the ACE repository for the TechX squads (DL36).
- DL05 is applied as option B from 2 November 2026: TechX creates the recovery module in its own package; the ACE team applies the module boundaries for the common and collection modules later.
- The common module's published packages are named in the module map. Until the ACE team names them, the map lists `..common.api..` (assumed; DL05).
- The ACE build runs the unit test phase on every pull request.

##### 4. Flow

1. Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
2. Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.
3. Squad member: writes RecoveryBoundaryTest with the rules BR1 to BR5, reading the module map.
4. Squad member: writes the front end boundary rules for `src/modules/recovery`.
5. Squad member: wires the common module access check for `/api/recovery/v1/**` through RecoveryAccessGuard.
6. Pipeline: on each pull request runs the back end tests, including RecoveryBoundaryTest, and the front end dependency check.
7. Pipeline: fails the build when a rule is broken and prints the rule, the class and the class it depends on.
8. Squad member: fixes the call by going through the other module's `api` package or an application event, and the build passes.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A recovery class imports a collection module internal class | Build fails with the rule and both class names | Build log: boundary rule BND-1 broken | AC1 |
| X2 | A recovery module class imports another recovery module's internal class | Build fails | Build log: boundary rule BND-3 broken | AC3 |
| X3 | A class uses another module's entity or repository | Build fails | Build log: boundary rule BND-4 broken | AC4 |
| X4 | A class outside the integration adapters uses an HTTP or SFTP client | Build fails | Build log: boundary rule BND-5 broken | AC5 |
| X5 | A recovery screen imports a collection screen | Front end build fails | Build log: rule no-collection-import broken | AC6 |
| X6 | A new package is not in the module map | Build fails | Build log: package not in module map | AC7 |
| X7 | A request reaches a recovery endpoint from a role without the right | 403 through the common module access check | MSG-P4-002 | Access test TC-TE-001-08 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only repository access; every later story builds inside these folders |
| Negotiable | Module names and published packages are in the module map file, not in the test code |
| Valuable | The three teams can change their own module without breaking another |
| Estimable | Folders, one map file, one ArchUnit test class, one front end rule file |
| Small | Fits in one sprint with its tests |
| Testable | Each rule has a test fixture class that breaks it |

##### 7. Acceptance criteria

```gherkin
Feature: Recovery module folder and boundary test

  Background:
    Given the module map lists modules P1 to P10 and S1 to S9 with their packages
    Given the published packages are "<module>.api" and any other package the module map lists for each recovery module, and "..common.api.." for the common module

  Scenario: AC1 Boundary enforced (legacy RWB-TE-001 AC1)
    Given a class "recovery.casewf.internal.SampleService" that imports "collection.internal.CollectorRepository"
    When the pipeline runs
    Then the boundary test fails the build
    Then the build log names boundary rule BND-1, "SampleService" and "CollectorRepository"

  Scenario: AC2 Published interface allowed (legacy RWB-TE-001 AC2)
    Given a class "recovery.casewf.internal.SampleService" that calls an interface in "common.api"
    When the pipeline runs
    Then the build passes

  Scenario: AC3 Recovery modules meet only through their api package (legacy RWB-TE-001 AC3)
    Given a class in "recovery.integration.internal" that imports "recovery.decision.internal.DecisionLogRepository"
    When the pipeline runs
    Then the build fails with boundary rule BND-3
    When the class imports the published "recovery.decision.writer.DecisionLogWriter" instead
    Then the build passes

  Scenario: AC4 A module uses only its own tables (legacy RWB-TE-001 AC4)
    Given a class in "recovery.integration.internal" that uses the entity "recovery.casewf.internal.RecoveryCaseEntity"
    When the pipeline runs
    Then the build fails with boundary rule BND-4

  Scenario: AC5 No direct call to a system of record (legacy RWB-TE-001 AC5)
    Given a class in "recovery.casewf.internal" that uses "java.net.http.HttpClient"
    When the pipeline runs
    Then the build fails with boundary rule BND-5
    Then the same use in "recovery.integration.adapter" passes

  Scenario: AC6 Front end boundary (legacy RWB-TE-001 AC6)
    Given a component in "src/modules/recovery/caselist" that imports "src/modules/collection/worklist/WorkList"
    When the front end build runs
    Then it fails with rule no-collection-import

  Scenario: AC7 A package missing from the module map (legacy RWB-TE-001 AC7)
    Given a new package "recovery.vendorx" not in the module map
    When the pipeline runs
    Then the build fails with "package recovery.vendorx is not in the module map"
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | boundary rule BND-1: recovery classes depend on the collection module only through its published packages | DT08; ADR-002 |
| BR2 | boundary rule BND-2: recovery classes depend on the common module only through its published packages | DT07; DT08 |
| BR3 | boundary rule BND-3: a recovery module depends on another recovery module only through a package the module map lists as published for it, or an application event | Settled architecture; ADR-002 |
| BR4 | boundary rule BND-4: entities and repositories of a module are used only inside that module | Settled architecture: a module reads only its own tables |
| BR5 | boundary rule BND-5: only the packages the module map allows for client libraries use HTTP, SFTP or file transfer clients: `recovery.integration.adapter` (RWB-E1-007) for files, and the agent runtime client for the enterprise model endpoint INT-23 (RWB-TE-013); no recovery class calls a system of record | REQ-DRI-006; ADR-005 |
| BR6 | Module names, packages and published packages are read from the module map file, not written in the test | Principle 1 applied to build configuration |

The R-BND codes are the names of the boundary test rules in this story. They are not routing rules.

##### 9. State transitions

None. This story does not change a case status. It changes the build result of a pull request from passed to failed when a rule is broken.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Create the folders, the module map and the boundary test |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the module map or to the boundary rules |
| ACE team | Names the common and collection published packages (DL05) |
| RW-PLATADM, platform administrator | Runs the pipeline |
| No approval level from the delegation of authority applies | The story takes no business decision |

##### 11. Data

No business field is read or written. The boundary test reads source and compiled classes only.

Field IDs are those in the Logical Data Model and Data Dictionary.

##### 12. Contract

###### 12.1 REST operations provided

None. The boundary test is a build-time check and the module map is a file, so this story publishes no REST operation.

###### 12.2 REST operations consumed

None. The build reads the repository and the module map; it calls no service.

###### 12.3 Events published

None. A build check publishes no event and the outbox is not involved.

###### 12.4 Events consumed

None. A build check consumes no event.

###### 12.5 Workflows and activities

None. The checks run in the unit test phase and the front end lint step, not in a Temporal workflow or activity.

###### 12.6 Schedules

None. The checks run on every pull request and every build of main; there is no schedule.

###### 12.7 Tables owned

None. The story owns no table in any schema; the module map is a file in the repository.

###### 12.8 Contract fakes

None. The story needs no fake: its fixtures are test-only classes under `src/test` that break each rule on purpose.

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

None. This story makes no REST, Kafka, Temporal or file call; it reads source and compiled classes and the module map file only.

This preserved story builds against five platform contract stories — RWB-PLT-E1027-CON (decision-record library, owner PLT, the platform team), RWB-PLT-E1043-CON (reference data, owner PLT, the platform team), RWB-PLT-E1037-CON (authorise and guard, owner PLT, the platform team), RWB-PLT-TE006-CON (outbox and inbox, owner PLT, the platform team) and RWB-PLT-N001-CON (gateway-bff route, owner PLT, the platform team) — and against four service contract stories — RWB-P3-E1043-CON (reference data, owner P3 rwb-case), RWB-P4-E1037-CON (authorise, owner P4 rwb-access), RWB-P2-E1007-CON (integration adapters, owner P2 rwb-integration) and RWB-P10-TE013-CON (agent runtime client, owner P10 rwb-agent). Those stories publish the operations and payloads; this story adds no path of its own.

##### 13. Solution plan

**As-built component set unchanged.** The six components of the as-built plan stay as built: `recovery-modules.yaml`, `RecoveryBoundaryTest`, `ModuleMapLoader`, the boundary fixtures, `RecoveryAccessGuard` and the front-end dependency rule file. This story changes none of them, and the as-built contract and solution plan are kept word for word under "As built (monolith)".

The as-built paths stay as built for this preserved story: `architecture/recovery-modules.yaml` (section 4) and `src/modules/recovery/` (as-built section 13). Their target value in the service template and in each service repository — where the module map sits and how the front-end modules are laid out — is Not specified in the source documents (GAP-1429; ASM-2510). The per-service package map, the per-service module map and the re-pointed rules are the delta of RWB-PLT-TE001-APP-2 and are not built here.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The rules of the as-built story stay as built in this preserved copy; the ten rows above are the target form each rule takes, and the delta story RWB-PLT-TE001-APP-2 re-points the rules at them.

**Done when.** The eight test cases of section 16 still pass against the platform template, and the delta is delivered by RWB-PLT-TE001-APP-2 (one repository, one package, one module map and one schema per service).

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A boundary rule is broken | Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event. |
| Build log | A package is not in the module map | package {package} is not in the module map |
| MSG-P4-002 | A role without the right calls a recovery endpoint | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard.

##### 15. Screens and states

No screen in this story. A developer reads the result in the pull request checks and the build log.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-001-01 | AC1, BR1 | Component | Fixture importing a collection internal class |
| TC-TE-001-02 | AC2, BR2 | Component | Fixture calling a common module published interface |
| TC-TE-001-03 | AC3, BR3 | Component | Fixture importing recovery.decision.internal, then recovery.decision.writer |
| TC-TE-001-04 | AC4, BR4 | Component | Fixture using another module's entity |
| TC-TE-001-05 | AC5, BR5 | Component | HttpClient in casewf and in the integration adapter package |
| TC-TE-001-06 | AC6 | Component | Front end fixture importing a collection component |
| TC-TE-001-07 | AC7, BR6 | Component | Package recovery.vendorx not in the map |
| TC-TE-001-08 | Access | End to end | RW-REFADM calls the test-only Case record R endpoint; refused with MSG-P4-002 |

The legacy level `System` maps to Component in the target and the legacy level `Access` maps to End to end; nothing else in a row changes, and the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

##### 17. Guardrails

- No business value in code; module names, package names and published packages live in the module map, never in the test.
- No personal data in events, workflow inputs or logs; the fixtures hold class names only and the boundary test writes no payload.
- ACE data only through the owner's contract or the `v_ace_*` views; no recovery class opens a connection to an ACE table or to a system of record.
- One schema and one login per service: this preserved story reads no table at all, and the delta re-points the same rule at `rwb_<name>` (DP-01).
- Generated code is never edited; the module map, the package tree and the pipeline come from the service template, and a change is made in the template.
- The breaking fixtures stay in `src/test` and never ship.
- The rule codes BND-1 to BND-5 are the names of the boundary test rules in this story; they are not routing rules.

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 5.2 and section 7 | None | All recovery processes | None | TC-TE-001-01 to TC-TE-001-08 |

##### 19. Out of scope

- Code owners for the recovery folders: RWB-TE-002.
- Types and contract tests from the API specification: RWB-TE-003.
- Boundaries inside the common and collection modules: the ACE team under DL05 option A.
- The integration adapter pattern itself: RWB-E1-007.

#### As built (monolith)

###### 12. Contract

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

###### 13. Solution plan

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


### RWB-PLT-TE001-APP-2 Recovery module folder and boundary test

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE001-APP-2 |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-001 |
| Legacy disposition | Preserved + delta |
| Build status | Built |
| Patterns applied | DP01, DP03, DP07, DP08, DP09, DP11, DP13, DP16, DP19, DP20 |
| Parallel lane | L-PLT-TPL-I |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: delta copy of RWB-TE-001 for the 19 service repositories, one module map per service and the re-pointed boundary rules (Arch v5 slides 20, 29 and 41; DP-01, DP-03, DP-07, DP-08, DP-09, DP-11, DP-13, DP-16, DP-19, DP-20). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **each of the 19 services in its own repository generated from the service template, with one Java package and one `api` and `internal` split per service, a module map kept per service and boundary rules that refuse a cross-schema read, an internal import, a chain, a raw Kafka send and a direct system call**, so that **no service can reach inside another service or around its published contract**.

##### 2. Business rationale

The as-built story enforces the module boundaries inside one ACE service: one package tree, one recovery schema, one repository and one module map for all 19 Workbench modules. Arch v5 replaces that monolith with 19 services, each with its own repository, its own schema `rwb_<name>` and its own login (slides 20, 29 and 41), and it keeps the same promise — a build in every repository fails when a boundary is broken. Without the re-pointed rules, the same test that today forbids a cross-module read would pass in a repository that joins another service's schema, that imports another service's internal package, that calls two owner services in one request, that writes a decision record in its own table or that sends a Kafka record from the request thread. ADR-013, ADR-014 and ADR-020 are the decisions of record and DP-01, DP-03, DP-07, DP-08, DP-09, DP-11, DP-13, DP-16, DP-19 and DP-20 are the patterns. It supports REQ-DRI-006. The measure is the count of boundary violations merged to main, which must stay at zero in all 19 repositories.

##### 3. Preconditions

- The service template of RWB-PLT-TPL supplies the repository skeleton, the module map loader, the boundary test and the golden pipeline, and the repository and pipeline baseline is in place (RWB-PLT-NF01-OPS).
- The five platform contract stories are available with their fakes: RWB-PLT-E1027-CON (decision-record library), RWB-PLT-E1043-CON (reference data), RWB-PLT-E1037-CON (authorise and guard), RWB-PLT-TE006-CON (outbox and inbox) and RWB-PLT-N001-CON (gateway-bff route).
- The four service contract stories publish the typed clients and fakes this story tests against: RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P2-E1007-CON and RWB-P10-TE013-CON.
- Each of the 19 services has its own schema `rwb_<name>`, its own login and its own repository (Arch v5 slides 29 and 41; ADR-013, ADR-014).
- ADR-020 (contract-first REST, one hop, 2 s timeout) is the decision in force.
- The per-service package map is one Java package per service, `th.co.scb.ace.workbench.recovery.<short without hyphen>`, with one `api` package and one `internal` package inside it. The exact packages inside each repository are Not specified in the source documents (GAP-1429; ASM-2511).
- No build dependency: the story has no build dependency and is Day 1 by rule (Template and Rules section R5.7).

##### 4. Flow

1. Squad member: generates the 19 service repositories from the service template, one repository per service, each with the golden pipeline of RWB-PLT-NF01-OPS.
2. Squad member: creates in each repository the one Java package of its service, `th.co.scb.ace.workbench.recovery.<short without hyphen>`, with one `api` package for the published interfaces and one `internal` package for everything else.
3. Squad member: writes the module map of the service in its own repository, listing that service's module codes, packages, published packages and allowed client libraries.
4. Squad member: re-points the boundary rules at the split: no cross-schema read (DP-01), the decision-record library only (DP-03), the outbox and inbox library only (DP-09), the published REST contract or a Temporal activity and never an internal package or a chain (DP-11, DP-13), the shared clients for reference data and authorise (DP-07, DP-08), the integration adapter contract (DP-16), the gateway-bff composite route (DP-19) and the agent client (DP-20).
5. Squad member: writes the front end rule per service: a screen reaches its owner service through the gateway-bff composite route and imports no other service's screen.
6. Pipeline: on each pull request runs the back end boundary test in the unit test phase, the contract tests against the fakes and the front end dependency check.
7. Pipeline: fails the build when a rule is broken and prints the rule, the class and the class, table or path it depends on.
8. Squad member: fixes the call by going through the published contract, an application event through the outbox or a Temporal activity on the owner's queue, and the build passes.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A class in one service repository imports the `internal` package of another service | Build fails with the rule and both package names | Build log: boundary rule broken on the internal import | AC3 |
| X2 | A query, view or foreign key in `rwb_<name>` names another service's schema | Build fails with the rule, the object and the other schema | Build log: boundary rule broken on the cross-schema reference | AC2 |
| X3 | A class sends a Kafka record or consumes one without the outbox and inbox library | Build fails | Build log: boundary rule broken on the direct producer or consumer | AC4 |
| X4 | A class writes a decision record in a table of its own instead of the decision-record library | Build fails | Build log: boundary rule broken on the decision record | AC4 |
| X5 | One request calls two owner services in a chain, or the browser calls an owner service directly | Build fails | Build log: boundary rule broken on the call depth | AC3 |
| X6 | A class reads reference data or an authorise answer outside the shared client of its contract | Build fails | Build log: boundary rule broken on the shared client | AC5 |
| X7 | A class opens an SFTP or HTTP client outside the integration adapter contract, or calls the enterprise model endpoint without the agent client | Build fails | Build log: boundary rule broken on the adapter or the agent client | AC5 |
| X8 | A screen calls a service REST base directly instead of the gateway-bff composite route | Front end build fails | Build log: boundary rule broken on the composite route | AC5 |
| X9 | A package is not in the service's own module map | Build fails | Build log: package not in the module map | AC1 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the service template and the contract fakes only; it builds no business behaviour |
| Negotiable | The module map content per service is settled per service; the rules and the package pattern are fixed |
| Valuable | Each of the 19 services can change without breaking another, and the boundary is checked in every repository |
| Estimable | One template change, one module map per service, one rule set and its breaking fixtures |
| Small | Fits in one sprint, one service at a time, with its fixtures |
| Testable | Each rule has a breaking fixture that fails the build and a passing fixture that clears it |

##### 7. Acceptance criteria

```gherkin
Feature: Recovery module folder and boundary test in 19 service repositories

  Background:
    Given the service template supplies one module map loader, one boundary test and one golden pipeline
    Given each of the 19 services has its own repository, its own schema rwb_<name> and its own login

  Scenario: AC1 19 repositories from one template (new, D-RCV-60)
    Given the service template with the package pattern of section R4 of the template and rules
    When a repository is generated for each of the 19 services
    Then each repository carries one Java package "th.co.scb.ace.workbench.recovery.<short without hyphen>", for example "th.co.scb.ace.workbench.recovery.case" for rwb-case and "th.co.scb.ace.workbench.recovery.sourcedata" for rwb-source-data
    Then each package holds one "api" package and one "internal" package
    Then each repository holds its own module map for its own service only
    Then the build of each repository runs the boundary test and no repository compiles another repository's code

  Scenario: AC2 A service never reads another service's schema (new, D-RCV-60)
    Given a class in "th.co.scb.ace.workbench.recovery.case.internal" with a query that joins "rwb_payment.payment" from schema "rwb_case"
    When the boundary test runs in the build
    Then the build fails with the rule code and both objects named
    When the query holds the payment ID and calls the rwb-payment contract instead
    Then the build passes
    Then no view and no foreign key in "rwb_case" names another schema

  Scenario: AC3 A cross-service call is the published contract, one hop (new, D-RCV-60)
    Given the rwb-payment contract mock returns one payment state
    Given a class in the rwb-case repository that imports an internal class of the rwb-payment package
    When the boundary test runs
    Then the build fails on the internal import
    When the class calls the published REST contract "/api/recovery/payment/v1" through the typed client with the 2 s timeout instead
    Then the build passes
    Then a request that calls two owner services in one chain fails the build

  Scenario: AC4 Decisions and events go through the libraries (new, D-RCV-60)
    Given a class in a service repository that writes an entry to a decision-log table of its own
    When the boundary test runs
    Then the build fails, because a decision is recorded only through the decision-record library and the topic "rwb.decision-record.v1"
    When the class calls the decision-record library instead
    Then the build passes
    Given a class that sends a Kafka record from the request thread without the outbox
    Then the build fails and the record is published only through the outbox and inbox library

  Scenario: AC5 Reference data, authorise, adapters, the edge and the agent (new, D-RCV-60)
    Given the rwb-case contract mock returns one reference-data answer for the reference-data client
    Given the rwb-access contract mock returns an allow answer for the guard library
    Given a class in a service repository that reads a reference-data table of its own
    When the boundary test runs
    Then the build fails and reference data is read only through the RWB-PLT-E1043-CON client
    When the class reads through the client instead
    Then the build passes
    Given a class outside the integration adapter contract that opens an SFTP client
    Then the build fails
    Given a screen that calls a service REST base directly instead of the gateway-bff composite route
    Then the front end build fails
    Given a class that opens its own HTTP client to the enterprise model endpoint instead of the rwb-agent client
    Then the build fails
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each of the 19 services has its own repository, generated from the service template, with one Java package `th.co.scb.ace.workbench.recovery.<short without hyphen>` and one `api` and one `internal` package inside it | Template and Rules section R4; Arch v5 slide 20; ADR-013 |
| BR2 | Each service keeps its own module map in its own repository; a package that is not in the map fails the build | Legacy RWB-TE-001 BR6; Arch v5 slide 29 |
| BR3 | One schema and one login per service; a service never reads another service's schema, and a cross-schema join, view or foreign key fails the build | DP-01; Arch v5 slide 29; ADR-014 |
| BR4 | The decision-record library and the topic `rwb.decision-record.v1` are the only way to record a decision; a local decision-log table is refused | DP-03; ADR-022 |
| BR5 | The outbox and inbox library is the only way to publish or consume an event; a direct producer or consumer fails the build | DP-09; ADR-015 |
| BR6 | A cross-service call is the published REST contract `/api/recovery/<short>/v1` with a fake in the build and one hop in the request, or a Temporal activity on the owner's queue; never an internal package and never a chain | DP-11; DP-13; ADR-020 |
| BR7 | Reference data and authorise answers arrive only through the shared-library clients of RWB-PLT-E1043-CON and RWB-PLT-E1037-CON over the contracts of rwb-case and rwb-access | DP-07; DP-08 |
| BR8 | An outbound file goes only through the rwb-integration adapter contract and the enterprise model endpoint only through the rwb-agent client | DP-16; DP-20 |
| BR9 | A screen reaches a service only through the gateway-bff composite route and no screen imports another service's screen | DP-19; Arch v5 slides 11 and 20 |
| BR10 | Generated code is never edited: the repository skeleton, the module map loader, the boundary test and the pipeline come from the template | RWB-PLT-NF01-OPS; Template and Rules section R6 |

##### 9. State transitions

None. This story does not change a case status. It changes the build result of a pull request in one service repository from passed to failed when a boundary rule is broken, and the state of one repository's build has no effect on another repository's build.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Generate the repositories, write the module map and the boundary fixtures of a service |
| TechX tech leads (code owners, RWB-PLT-TE002-APP) | Approve a change to a module map or to the boundary rules |
| ACE team | Names the schema and the login of each service (Arch v5 slide 29) |
| Platform team (PLT) | Owns the service template, the module map loader and the golden pipeline |
| RW-PLATADM, platform administrator | Runs the pipeline of a repository |
| No approval level from the delegation of authority applies | The story takes no business decision |

##### 11. Data

No business field is read or written. The boundary test reads source, compiled classes, the service's own module map and the schema object list of its own schema. It reads no row of any table and no payload of any event.

Field IDs are those in the Logical Data Model and Data Dictionary. No field is added or changed here.

##### 12. Contract

###### 12.1 REST operations provided

None. The story provides no REST operation of its own; each of the 19 service REST bases `/api/recovery/<short>/v1` is published by that service's own contract story.

###### 12.2 REST operations consumed

None at runtime. The rules point the generated clients at the published contracts rather than at an internal package: the reference-data client of RWB-PLT-E1043-CON over RWB-P3-E1043-CON (owner P3 rwb-case), the guard library of RWB-PLT-E1037-CON over RWB-P4-E1037-CON (owner P4 rwb-access), the integration adapter contract of RWB-P2-E1007-CON (owner P2 rwb-integration), the agent client of RWB-P10-TE013-CON (owner P10 rwb-agent) and the gateway-bff route of RWB-PLT-N001-CON (owner PLT, the platform team). Those stories publish the operations and payloads; this story adds no path and no payload.

###### 12.3 Events published

None of its own. A service publishes on the topic of its owner, `rwb.<short>.events.v1`, through the outbox library of RWB-PLT-TE006-CON, and it publishes the shared decision record on `rwb.decision-record.v1` through the library of RWB-PLT-E1027-CON. The platform story owns neither topic and emits no event.

###### 12.4 Events consumed

None of its own. Each service consumes through its own inbox from RWB-PLT-TE006-CON, in its own consumer group, and this story only refuses a consumer that bypasses it.

###### 12.5 Workflows and activities

None. The rules are build-time checks. A cross-service step allowed by the rules is a Temporal activity on the owner's queue `rwb-<short>`, declared by that owner's contract; this story defines no workflow and no activity.

###### 12.6 Schedules

None. The checks run on every pull request and every build of main; there is no schedule.

###### 12.7 Tables owned

None. The module map is a file in the repository and every business table belongs to one of the 19 services in its own schema; the story creates no schema, no login and no table.

###### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Decision-record library fake of RWB-PLT-E1027-CON | Accepts one decision record and answers the stored record id on `rwb.decision-record.v1` | AC4 fixture and the contract test of every service |
| Outbox and inbox library fake of RWB-PLT-TE006-CON | Accepts one record for `rwb.<short>.events.v1`; answers one inbox delivery as first time or duplicate | AC4 fixture and the contract test of every service |
| Reference-data fake of RWB-PLT-E1043-CON and RWB-P3-E1043-CON | One reference-data answer for one lookup code | AC5 fixture |
| Authorise and guard fake of RWB-PLT-E1037-CON and RWB-P4-E1037-CON | One allow answer and one refuse answer for one capability area and right | AC5 fixture |
| Integration adapter fake of RWB-P2-E1007-CON | One accepted outbound file manifest and one refused manifest | AC5 fixture |
| Agent client fake of RWB-P10-TE013-CON | One completed agent run answer and one fallback answer | AC5 fixture |
| gateway-bff route fake of RWB-PLT-N001-CON | One composite route answering the owner service's published contract | AC5 fixture and the front end rule |

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed by this story | The rules keep every call on the published contract of the owner, one hop, 2 s timeout |
| Kafka | None published, none consumed by this story | The rules keep every record on the outbox and inbox library and on the owner's topic |
| Temporal | None | No workflow and no activity of its own; an activity on `rwb-<short>` is only allowed by the rule |
| File | None | No file is read or written except the module map and the sources in the repository |

##### 13. Solution plan

**Deliverables.** The repository skeleton of the service template with the one package per service and the `api` and `internal` split, the per-service module map and its loader, the re-pointed boundary rules with one breaking and one passing fixture each, the front end rule per service, and the wiring of both checks into the golden pipeline of RWB-PLT-NF01-OPS.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-16 | `recovery.integration.adapter` | rwb-integration contract | C RWB-P2-E1007-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

**Build steps**

1. Generate the 19 repositories from the service template and prove that each carries one package, one `api` and one `internal` package and its own module map (AC1).
2. Extend the module map loader to the per-service map and add one fixture package that is not in the map (AC1, X9).
3. Re-point rule BND-4 to the schema rule: a join, a view or a foreign key into another `rwb_<name>` fails the build, and the rule reads the schema list of the service's own login (AC2).
4. Add the contract rule: an import of another service's `internal` package, a chain of two owner services and a call from the browser to an owner service fail, and the published contract with its fake passes (AC3).
5. Add the library rules: a direct decision-log write, a direct Kafka producer and a direct consumer fail, and the decision-record library and the outbox and inbox library pass (AC4).
6. Add the shared-client rules: reference data, authorise, the integration adapter, the gateway-bff route and the agent client pass, and every direct read or direct client fails (AC5).
7. Wire both checks into the golden pipeline and confirm that a failing fixture blocks a merge in one repository without touching another repository's build.
8. Prove the pattern on two services (rwb-case and rwb-payment) and then generate the remaining 17 from the same template.

**Done when.** The five test cases of section 16 pass for two services and then for all 19, every repository build runs the boundary test and the front end rule, and no build produces a cross-schema reference, an internal import, a chain, a raw Kafka send, a local decision record or a direct system call.

The per-service module-map file name and the gateway-bff composite route list are Not specified in the source documents (GAP-1430; ASM-2512); the template names the map file at the root of each service repository and takes the route list from RWB-PLT-N001-CON until the point is closed.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A boundary rule is broken | Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event. |
| Build log | A package is not in the module map | package {package} is not in the module map |
| MSG-P4-002 | A role without the right calls a recovery endpoint | You cannot {action} here. Your role does not include it. |

The two build log lines carry the text of the as-built story unchanged; the code, the class and the dependency named in the text are those of the service that owns the repository. Build log text is for developers and is not part of the message standard.

##### 15. Screens and states

No new screen. A developer reads the result in the pull request checks and the build log of the repository. The front end rule adds one state to the build: a screen that calls a service REST base directly, or that imports another service's screen, turns the front end build from passed to failed. SCR-44 is not involved.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE001-APP2-01 | AC1 | Contract | 19 repositories generated from the template; one package, one `api` and one `internal` package, one module map per repository |
| TC-PLT-TE001-APP2-02 | AC2 | Component | Cross-schema fixture in `rwb_case` naming `rwb_payment`; refused, and the contract call passes |
| TC-PLT-TE001-APP2-03 | AC3 | Component | Internal import fixture, published-contract fixture and two-service chain fixture; the chain is refused |
| TC-PLT-TE001-APP2-04 | AC4 | Component | Direct decision-log write and direct Kafka send; both refused, and the library calls pass |
| TC-PLT-TE001-APP2-05 | AC5 | Component | Reference-data, guard, adapter, gateway-bff route and agent client fixtures; each direct use is refused |

The as-built tests of RWB-TE-001 stay in RWB-PLT-TE001-APP section 16 under their legacy test case IDs, and the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

##### 17. Guardrails

- No business value in code; module names, package names and published packages live in the module map of the service, never in the test (DP-01).
- No personal data in events, workflow inputs or logs; the fixtures hold class, package and schema names only and no payload.
- ACE data only through the owner's contract or the `v_ace_*` views; a service never reads an ACE table, another service's schema or a system of record.
- One schema and one login per service; a cross-schema join, view or foreign key fails the build in every repository (DP-01).
- Contract-first only: the published REST contract with its fake and one hop, or a Temporal activity on the owner's queue; never an internal package and never a chain (DP-11, DP-13).
- Decisions only through the decision-record library and events only through the outbox and inbox library (DP-03, DP-09).
- Generated code is never edited; a change is made in the service template and reaches every repository on regeneration.
- The breaking fixtures stay in `src/test` and never ship.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Boundary test in every repository; no direct client outside the adapter and the agent client | TC-PLT-TE001-APP2-05 |
| DP-01 | Owner's schema `rwb_<name>`; never read another service's tables | Cross-schema join, view and foreign key refused in every build | TC-PLT-TE001-APP2-02 |
| DP-03; DP-09 | Decision-record library and topic `rwb.decision-record.v1`; outbox and inbox library | Only library calls accepted; direct decision-log write, producer and consumer refused | TC-PLT-TE001-APP2-04 |
| DP-11; DP-13 | REST contract with mock, one hop; `/api/recovery/<short>/v1` | Published contract and one hop accepted; internal import and chain refused | TC-PLT-TE001-APP2-03 |
| DP-07; DP-08; DP-16; DP-19; DP-20 | Shared clients for reference data and authorise, the adapter contract, the gateway-bff route and the agent client | Only the contract-backed client accepted; every direct read, client or route refused | TC-PLT-TE001-APP2-05 |
| Arch v5 slide 20 | Every service built from one template and the shared libraries | 19 repositories from one template, one package and one map each | TC-PLT-TE001-APP2-01 |
| Arch v5 slide 29 | 19 schemas, one login each, no cross-schema joins or keys, boundary test in every build | Schema isolation, per-service map and the boundary test in the golden pipeline | TC-PLT-TE001-APP2-01, TC-PLT-TE001-APP2-02 |

##### 19. Out of scope

- The as-built monolith module folder and its boundary test, kept word for word in RWB-PLT-TE001-APP.
- The per-service contract stories and their published operations, payloads and fakes: RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P2-E1007-CON and RWB-P10-TE013-CON, and the platform contracts RWB-PLT-E1027-CON, RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-TE006-CON and RWB-PLT-N001-CON.
- The repository and pipeline baseline of the platform (RWB-PLT-NF01-OPS) and the pipeline template and Helm chart (RWB-PLT-N004-OPS).
- The quality gates baseline (RWB-PLT-NF05-OPS).
- The business code of each service and its own module list, which each service epic delivers in its own repository.
- The schemas, logins and grants of the 19 services (Arch v5 slide 29; ADR-014).


## RWB-TE-002 Code owners for the recovery module

Legacy disposition: Preserved + delta.

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE002-APP | App development | RWB-PLT-TPL | L-PLT-TPL-L | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-PLT-TE002-OPS | DevOps | RWB-PLT-TPL | L-PLT-TPL-K | Day 1 | DevOps team (suggested; any team may pick up this story) |

### RWB-PLT-TE002-APP Code owners for the recovery module

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE002-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-002 |
| Legacy disposition | Preserved + delta |
| Build status | Built |
| Patterns applied | DP07, DP15, DP19 |
| Parallel lane | L-PLT-TPL-L |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE002-OPS, RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-TE-002 word for word, with the legacy contract and the legacy solution plan kept in the "As built (monolith)" appendix; the target delta is delivered by RWB-PLT-TE002-OPS and the as-built controls are not changed by this story. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.

##### 2. Business rationale

The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.

##### 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the module map exist.
- The repository host supports a code owners file (GitHub format assumed, as ACE uses GitHub Copilot under DL32).
- The teams exist in the repository host: TechX recovery tech leads and the ACE team. Names assumed until DL37 and DL36 are answered: `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`.
- The repository administrator of the ACE team can set the branch rule on main.

##### 4. Flow

1. Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.
2. Squad member: adds the code owners validation step to the pull request pipeline.
3. ACE team repository administrator: sets the branch rule on main: one approval from a code owner required, stale approvals dismissed on a new commit.
4. Developer: opens a pull request that changes a recovery folder.
5. Repository host: requests review from the owning team named for each changed path.
6. Pipeline: runs the validation step; an owner that does not exist or a path that matches no file fails the check.
7. Code owner: approves; the merge is allowed once every owning team of the changed paths has approved.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A pull request changes a recovery folder and only a non owner approves | Merge stays blocked | Repository host: review required from code owners | AC1 |
| X2 | A pull request changes the common module | ACE team review required | Repository host: review required from code owners | AC2 |
| X3 | A pull request changes both recovery and common folders | Both teams must approve | Repository host: review required from code owners | AC3 |
| X4 | The author is a code owner and approves their own change | The author's approval does not count | Repository host: review required from code owners | AC5 |
| X5 | A new commit is pushed after approval | The approval is dismissed; review needed again | Repository host: review required from code owners | AC6 |
| X6 | The code owners file names an owner that does not exist | The validation step fails the build | Build log: owner not found | AC7 |
| X7 | A squad member who is not a code owner tries to satisfy the review | Merge refused | Repository host: review required from code owners | Access test TC-TE-002-08 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the folders from RWB-TE-001 |
| Negotiable | Team names are values in one file (DL37) |
| Valuable | No change to the recovery or common module merges without its owner |
| Estimable | One file, one pipeline step, one branch rule |
| Small | 1 point |
| Testable | Each criterion below is a pull request in a test branch |

##### 7. Acceptance criteria

```gherkin
Feature: Code owners for the recovery module

  Background:
    Given the code owners file maps the recovery folders to "@scb-ace/techx-recovery-tech-leads" and the common module folder to "@scb-ace/ace-team"
    Given main requires one code owner approval and dismisses stale approvals

  Scenario: AC1 Review required (legacy RWB-TE-002 AC1)
    Given a pull request that changes "ace-service/src/main/java/<ACE base path>/recovery/casewf/internal/AllocationService.java"
    When it is opened
    Then a TechX tech lead is required as reviewer
    Then an approval from a squad member outside the team leaves the merge blocked

  Scenario: AC2 A common module change needs the ACE team (legacy RWB-TE-002 AC2)
    Given a pull request that changes a file under "ace-service/src/main/java/<ACE base path>/common/"
    When it is opened
    Then "@scb-ace/ace-team" is required as reviewer

  Scenario: AC3 A change across both modules needs both teams (legacy RWB-TE-002 AC3)
    Given a pull request that changes one recovery file and one common module file
    When a TechX tech lead approves
    Then the merge stays blocked until a member of "@scb-ace/ace-team" also approves

  Scenario: AC4 Front end, migrations and the module map are covered (legacy RWB-TE-002 AC4)
    Given a pull request that changes "ace-web/src/modules/recovery/caselist/CaseListPage.tsx", a file under "ace-service/src/main/resources/db/migration/recovery/" and "architecture/recovery-modules.yaml"
    When it is opened
    Then "@scb-ace/techx-recovery-tech-leads" is required for all three

  Scenario: AC5 An author cannot approve their own change (legacy RWB-TE-002 AC5)
    Given a TechX tech lead opens a pull request on a recovery folder
    When the same tech lead approves it
    Then the merge stays blocked until a second member of the team approves

  Scenario: AC6 A new commit needs a new approval (legacy RWB-TE-002 AC6)
    Given an approved pull request on a recovery folder
    When a new commit is pushed to it
    Then the system dismisses the approval and code owner review is required again

  Scenario: AC7 An owner that does not exist fails the check (legacy RWB-TE-002 AC7)
    Given the code owners file names "@scb-ace/recovery-leads-typo" for a recovery path
    When the pipeline runs
    Then the code owners validation step fails and names the owner not found
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every path under the recovery back end, test and migration folders is owned by the TechX recovery tech leads | DL04 option A; DL37 |
| BR2 | The recovery front end folder and the module map file are owned by the TechX recovery tech leads | ADR-006; DL07 |
| BR3 | The common module folder is owned by the ACE team | DL04 option A; DT07 |
| BR4 | The code owners file itself is owned by both teams | DL04 |
| BR5 | The last matching pattern in the file decides the owner, so specific paths come after general ones | Repository host rule |
| BR6 | A merge to main needs one approval from a code owner of every changed path; an author's own approval does not count; a new commit dismisses approvals | ADR-008; DT11 |
| BR7 | Team names are values in the file; a change of team is a change to the file, reviewed by both teams | DL37 |

##### 9. State transitions

None. This story does not change a case status. It sets the review state of a pull request: review required, approved, or dismissed on a new commit.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX recovery tech leads | Approve changes to recovery folders and the module map |
| ACE team | Approves changes to the common module and the code owners file; sets the branch rule on main |
| RW-TRIBE, tribe lead and squad members | Open pull requests; cannot satisfy a code owner review unless in the owning team |
| No Workbench capability area applies | Access is a repository right, not a Workbench role right |

##### 11. Data

No business field is read or written.

Field IDs are those in the Logical Data Model and Data Dictionary.

##### 12. Contract

###### 12.1 REST operations provided

None. This preserved story provides no REST operation: the as-built control is one file, one pipeline step and one branch rule, and the legacy contract table is kept word for word in the "As built (monolith)" section below.

###### 12.2 REST operations consumed

None. The story makes no REST call of its own at run time. It builds against three published contracts, and the as-built control calls none of them: `RWB-PLT-E1043-CON`, the reference-data contract of rwb-case (owner platform, epic RWB-PLT-LIB, with the service contract behind it being `RWB-P3-E1043-CON` of rwb-case); `RWB-PLT-E1044-CON`, the per-service migration contract (owner platform, epic RWB-PLT-TPL); and `RWB-PLT-N001-CON`, the gateway-bff route contract (owner edge team, epic RWB-PLT-EDGE).

###### 12.3 Events published

None. The story publishes no Kafka event; the control is a repository file, a ruleset and a pipeline job, and none of them is a producer.

###### 12.4 Events consumed

None. The story consumes no Kafka event and subscribes to no topic.

###### 12.5 Workflows and activities

None. The story runs no Temporal workflow and no activity; the validation job is a pipeline job and not a workflow.

###### 12.6 Schedules

None. The story creates no Temporal Schedule; the validation job runs on the pull request trigger of the golden pipeline.

###### 12.7 Tables owned

None. The story owns no table and no schema; it holds no data of any kind.

###### 12.8 Contract fakes

None. The story needs no fake of its own; the fakes of `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON` and `RWB-PLT-N001-CON` are published by those contract stories for the repositories that build against them.

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | The story calls no REST operation and provides none |
| Kafka | None | The story publishes no event and consumes none |
| Temporal | None | The story runs no workflow, no activity and no Schedule |
| File | None | The story writes one versioned repository file, `.github/CODEOWNERS`, and reads no file at run time |

Two external dependencies carry the target state and are not calls: RWB-PLT-TE002-OPS deploys the ownership control across the 19 service repositories and the platform repository, and RWB-PLT-TE001-APP owns the module boundary test that the review control protects. Neither is invoked by this story.

##### 13. Solution plan

**As-built components unchanged.** The three components of the as-built plan stay exactly as built: `CODEOWNERS`, `CodeOwnersValidation` and the branch rule on main. This story changes none of them, and their plan and configuration are kept word for word in the "As built (monolith)" section below.

**Target delta.** The single-repository control is replaced in the target by one control per repository across the 19 service repositories and the platform repository. That work is RWB-PLT-TE002-OPS and nothing in this preserved story blocks it.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

DP-15 is the reason the as-built migration path `/ace-service/src/main/resources/db/migration/recovery/` has no successor as one folder: in the target every service repository carries its own migration folder and its own owner. DP-07 is the reference-data client and DP-19 the gateway-bff composite routes, so neither an owner nor a route crosses a service boundary without the owning team.

**Build steps.** None. The as-built control is built and stays built. The target build steps are in RWB-PLT-TE002-OPS.

**Done when.** The eight test cases of section 16 still pass against the as-built control, and the delta is delivered by RWB-PLT-TE002-OPS. The target value for the repository layout and for the branch ruleset of a service repository is Not specified in the source documents (GAP-1431; ASM-2514); this story keeps the as-built layout and the as-built branch rule until that point is closed.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Repository host | A code owner review is missing | Review required from code owners |
| Build log | An owner in the file does not exist | owner {team} not found |

No Workbench message applies; these texts come from the repository host and the pipeline.

##### 15. Screens and states

No screen in this story. A developer reads the required reviewers and the merge state on the pull request page of the repository host.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-002-01 | AC1, BR1, BR6 | Component | Test pull request changing a recovery Java file |
| TC-TE-002-02 | AC2, BR3 | Component | Test pull request changing a common module file |
| TC-TE-002-03 | AC3, BR6 | Component | Test pull request changing one file of each |
| TC-TE-002-04 | AC4, BR2 | Component | Front end file, migration file and the module map |
| TC-TE-002-05 | AC5, BR6 | Component | Tech lead approves own pull request |
| TC-TE-002-06 | AC6, BR6 | Component | New commit after approval |
| TC-TE-002-07 | AC7, BR7 | Component | Misspelt team name in the file |
| TC-TE-002-08 | Access | End to end | A squad member outside the owning team approves; the merge is refused. This story has no Workbench endpoint, so MSG-P4-002 is not shown |

Only the Level cell changes from the legacy table: the legacy level `System` maps to `Component` and the legacy level `Access` maps to `End to end`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

##### 17. Guardrails

- No business value in code: the file holds paths and team handles only, and a business value belongs to the parameters contract or the reference data and never to `.github/CODEOWNERS`.
- No personal data in logs, tests or prompts: test pull requests change fixture files only, and no repository, pipeline log or prompt carries a real account, a real party or a real document.
- No read of another schema or another service's tables: the file is a review control, and DP-15 keeps each migration folder inside the service that owns it, so an owner never approves a change to another service's schema.
- Team handles are teams, never individuals, so the absence of one person does not block a merge and no individual owner can be named in any repository.
- A code owner never approves their own change: the author's own approval does not count on any repository, as in the as-built branch rule.
- No secret, token or credential in a code owners file, a pipeline variable or a test fixture; a reference is resolved at run time by RWB-PLT-NF04-OPS.
- The common module and the gateway-bff composite routes keep their own owners (ACE team and edge team); a recovery team never approves a change to the common module or to a composite route.

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 7 | None | All recovery processes | None | TC-TE-002-01 to TC-TE-002-08 |

##### 19. Out of scope

- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).

#### As built (monolith)

###### 12. Contract

| Item | Value |
|---|---|
| File | `.github/CODEOWNERS` at the repository root |
| Entries | `/ace-service/src/main/java/**/common/ @scb-ace/ace-team`; `/ace-service/src/main/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/test/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/main/resources/db/migration/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-web/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads`; `/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads`; `/.github/CODEOWNERS @scb-ace/ace-team @scb-ace/techx-recovery-tech-leads` |
| Branch rule on main | Require a pull request; require review from code owners; 1 approval; dismiss stale approvals; the author's approval does not count |
| Pipeline step | Code owners validation: syntax, every owner exists and has write access, every pattern matches at least one file |
| Trigger | Every pull request that changes any file |
| Idempotency | The same file and the same changed paths always request the same owners |

###### 13. Solution plan

**Package.** Repository root: `.github/CODEOWNERS` and the pipeline definition of the ACE repository. No Java package.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| CODEOWNERS | Rule table | Path to owning team, in the order of BR5 |
| CodeOwnersValidation | Job | Pipeline step that fails on a missing owner or a pattern with no match |
| Branch rule on main | Rule table | Code owner review, one approval, stale approvals dismissed |

**Database.** None.

**Configuration and reference data.** Team names (assumed until DL37 and DL36); the folder paths from RWB-TE-001.

**Build steps**

1. Write the CODEOWNERS file with the entries in section 12, general paths first.
2. Add the validation step to the pull request pipeline and prove it fails on a misspelt team (AC7).
3. Ask the ACE team repository administrator to set the branch rule on main (BR6).
4. Run the six test pull requests in a test branch protected by the same rule (AC1 to AC6) and record the result in the pull request history.

**Feature flag.** None. The file and the branch rule have no runtime path.

**Done when.** The tests in section 16 pass and the branch rule on main shows code owner review as required.


### RWB-PLT-TE002-OPS Code owners for the recovery module

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE002-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-002 |
| Legacy disposition | Preserved + delta |
| Build status | Built |
| Patterns applied | DP07, DP15, DP19 |
| Parallel lane | L-PLT-TPL-K |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: delta story for RWB-TE-002 that moves the code-owner control from the one monolith repository to the 19 service repositories and the platform repository, with one CODEOWNERS file and one branch ruleset on main per repository and one code-owner validation job in the golden pipeline (Arch v5 slides 20, 29, 35 and 38; DP-07, DP-15, DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **DevOps engineer**, I want **one CODEOWNERS file, one branch ruleset on main and one code-owner validation job in every one of the 19 service repositories and in the platform repository, so that every change is reviewed by the team that answers for the path and no repository is unowned**, so that **no change reaches a service repository, a migration folder, a composite route or the shared common module without the owning team's approval, and no individual is ever named as an owner**.

##### 2. Business rationale

The as-built control of RWB-TE-002 is sized for one repository: seven entries in `.github/CODEOWNERS` cover the recovery back end, the tests, the migration folder, the front end, the module map and the common module, and one branch rule on main holds the merge until a code owner approves. Arch v5 replaces that shape. Slide 20 states that every service is built from one template and shared libraries and holds its own schema, its own task queue and its own release; slide 29 adds that each service has one schema, one login, its own migrations and a boundary test in every build; slide 35 denies by default and authenticates every call with a workload identity; slide 38 makes the template and the golden pipeline a wave-0 enabler built once before the first service exists. Applied to the estate, that is 19 service repositories plus the platform repository, and every one of them needs the control the single repository has today. A monolith file cannot be copied unchanged: the paths it names do not exist in a service repository, and the pattern that covered `/ace-service/src/main/java/**/recovery/` would cover 19 different services if it were copied.

Three decoupling patterns make the ownership map concrete. DP-15 puts one Flyway sequence and one migration folder in each service's own schema, so each migration folder must be covered by the owner of that service and by nobody else. DP-07 puts the reference-data client behind the reference-data contract of rwb-case, so the client wiring in a service repository belongs to that service team. DP-19 puts every screen behind a gateway-bff composite route, so the composite routes are owned by the edge team and not by any service team. Without one control per repository, a service repository can merge a change to another service's migration folder, a composite route can change without the edge team, and an individual account can stand in for a team. It supports REQ-DRI-006, because the module boundary that RWB-PLT-TE001-APP tests in every build is only as strong as the review that guards it. The measure is the share of merged pull requests in the 19 service repositories and the platform repository approved by a code owner of every changed path, which must be 100 percent, with no repository without an owner row.

##### 3. Preconditions

- The repository and pipeline baseline of RWB-PLT-NF01-OPS exists: one repository per service of the 19-service list, the platform repository, and the one golden pipeline definition that every repository runs.
- The quality-gate definitions of RWB-PLT-NF05-OPS exist, because those gates are the required status checks a branch ruleset names.
- The module boundary test of RWB-PLT-TE001-APP exists and runs as a check in every repository build, because that check is the second required status check.
- The repository host supports a code owners file and a branch ruleset (GitHub format assumed, as in RWB-TE-002 under DL32), and it can require status checks by name.
- The teams exist in the repository host and have write access to their repositories; the handle convention of the as-built file is kept, one handle per owning team.
- The platform template of epic RWB-PLT-TPL defines the folder set of a service repository, so an owner table can name a folder without inventing one.
- No build dependency: the story is Day 1 by rule (Template and Rules §R5.7) and it waits for no other story to start.
- The team handles, the required-check list and its order, and the ruleset name are Not specified in the source documents (GAP-1432; ASM-2516).

##### 4. Flow

1. Take the 20 repositories from the repository inventory of RWB-PLT-NF01-OPS: the 19 service repositories of the 19-service list and the platform repository.
2. Write one `.github/CODEOWNERS` file at the root of each repository, with the general paths first and the most specific path last, as BR7 of RWB-TE-002 requires.
3. Write one owner table per repository in the platform repository: the repository row, the folders it covers, the owning team handle, and the artefact that makes the folder necessary (the per-service migration folder of DP-15, the reference-data client of DP-07, the composite routes of DP-19).
4. Cover the shared folders explicitly: the common module is owned by the ACE team in every repository that carries it, and the platform template folders are owned by the platform team.
5. Apply one branch ruleset on `main` in each repository: a pull request is required, review from a code owner is required, stale approvals are dismissed on a new commit, and the author's own approval does not count.
6. Name the required status checks of that ruleset: the quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP.
7. Add one code-owner validation job to the golden pipeline: syntax, every handle exists and has write access, and every pattern matches at least one tracked file; a finding fails the build.
8. Prove the control on two repositories (one service repository and the platform repository) with a test pull request per acceptance criterion, then hand the owner table and the file to each service team, which changes only its own file.
9. Prove a team change: replace one handle with a second team handle in a test branch and show that both the old and the new owning team must approve.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A repository has no CODEOWNERS file, or its file covers no folder of the template | The baseline check fails and names the repository and the folder | None (release error with an exit code and a job log line) | AC1, AC4 |
| X2 | A file names an individual account, or a handle with no write access | The validation job fails the build and names the entry; the change is not merged | owner {team} not found | AC3, AC4 |
| X3 | A pattern matches no tracked file | The validation job fails the build and names the pattern | Not specified in the source documents (GAP-1432; ASM-2515) | AC3 |
| X4 | A pull request on `main` has no code-owner approval, or only the author's own approval | The merge stays blocked | Review required from code owners | AC2 |
| X5 | A required status check is missing or failing | The ruleset blocks the merge until both required checks pass | None (the repository host reports the missing check by name) | AC2 |
| X6 | A team handle changes for a folder | The pull request requires approval from the old owning team and from the new owning team; the merge waits for both | Review required from code owners | AC5 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 20 repositories of RWB-PLT-NF01-OPS, the gate names of RWB-PLT-NF05-OPS and the boundary check of RWB-PLT-TE001-APP only |
| Negotiable | The team handles, the ruleset name and the order of the required-check list are agreed with the solution architect and the platform administrator; the one-file-per-repository rule, the ruleset content and the validation rules are fixed |
| Valuable | Gives every repository the same review control on Day 1 and makes an unowned repository or an individual owner a baseline failure instead of a review finding |
| Estimable | One file and one owner table per repository for 20 rows, one ruleset per repository, one validation job in the golden pipeline; five acceptance criteria |
| Small | Fits one sprint with the templates, the job and the two test repositories |
| Testable | Every criterion is tested with a planted file, a planted handle, a planted pattern and a test pull request in a test branch |

##### 7. Acceptance criteria

```gherkin
Feature: Code owners for the 19 service repositories and the platform repository

  Background:
    Given the repository inventory of RWB-PLT-NF01-OPS with the 19 service repositories and the platform repository
    Given the quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP
    Given every entry of a code owners file names a team handle and never an individual account

  Scenario: AC1 One CODEOWNERS file per repository, and every folder of the template is covered (new, D-RCV-60)
    Given the 19 service repositories and the platform repository, each created from the service template
    When the ownership control is applied
    Then every repository has exactly one ".github/CODEOWNERS" file at its root
    Then every entry names a team handle and no individual account
    Then the per-service migration folder of DP-15 and the reference-data client of DP-07 are covered by the owner of that service in its own repository
    Then the gateway-bff composite routes of DP-19 are covered by the edge team and by no service team
    Then the common module is covered by the ACE team in every repository that carries it

  Scenario: AC2 One branch ruleset on main per repository, with the required checks (new, D-RCV-60)
    Given a repository with its code owners file
    When the branch ruleset on "main" is applied
    Then a pull request is required before merge
    Then review from a code owner of every changed path is required
    Then stale approvals are dismissed when a new commit is pushed
    Then the author's own approval does not count
    Then the required status checks are the quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP
    Then a merge stays blocked while a required check is missing or failing

  Scenario: AC3 The validation job fails on an unknown handle or on an unmatched pattern (new, D-RCV-60)
    Given the code-owner validation job of the golden pipeline
    When a code owners file names a team handle that does not exist or has no write access
    Then the job fails the build and names the handle
    When a pattern in a code owners file matches no tracked file
    Then the job fails the build and names the pattern
    When every handle exists and every pattern matches at least one file
    Then the job passes and records the file version in the build record

  Scenario: AC4 No individual owner, and an unowned service fails the baseline (new, D-RCV-60)
    Given the owner tables of the 20 repositories
    When a code owners file names an individual account instead of a team handle
    Then the baseline check fails and names the repository and the entry
    When a service of the 19-service list has no owner row, or its file covers no folder of the template
    Then the baseline check fails and names the service
    When all 20 repositories are covered and every entry is a team handle
    Then the baseline check passes and the owner table is the record of the 20 rows

  Scenario: AC5 A team change is reviewed by both teams (new, D-RCV-60)
    Given a repository whose code owners file is owned by the service team and by the platform team
    When the team handle of a folder is changed in a pull request
    Then the review is required from the old owning team and from the new owning team
    Then the merge waits until both teams approve
    Then the owner table records the new handle for that repository
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One code owners file per repository, at the root, for each of the 19 service repositories and for the platform repository | Arch v5 slides 20 and 38; RWB-PLT-NF01-OPS |
| BR2 | Every entry names a team handle and never an individual account, so the absence of one person never blocks a merge | RWB-TE-002 BR7 (DL37); Template and Rules §R5.3 |
| BR3 | The owned paths of a service repository cover its per-service migration folder (DP-15), its reference-data client (DP-07) and its own business folders; the gateway-bff composite routes (DP-19) are owned by the edge team | DP-07; DP-15; DP-19; Arch v5 slides 20 and 29 |
| BR4 | One branch ruleset on `main` per repository: a pull request is required, review from a code owner is required, stale approvals are dismissed, and the author's own approval does not count | RWB-TE-002 BR6 |
| BR5 | The required status checks of the ruleset are the quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP | RWB-PLT-NF05-OPS; RWB-PLT-TE001-APP |
| BR6 | One code-owner validation job in the golden pipeline fails the build on an unknown handle, a handle without write access, or a pattern that matches no tracked file | RWB-TE-002 BR5; Arch v5 slide 29 (checked in every build) |
| BR7 | The last matching pattern decides the owner, so specific paths come after general ones; general paths are written first in every file | RWB-TE-002 BR5 |
| BR8 | A change of team handle is a change to the file, reviewed by the old owning team and by the new owning team, and recorded in the owner table | RWB-TE-002 BR7; DL37 |

##### 9. State transitions

None. This story changes no business state and no case status. It moves the review state of a pull request in each repository through review required, approved, and dismissed on a new commit, exactly as the as-built branch rule does in one repository; that is a state of a change and not a state of a case, and it carries no case status, no queue and no timer.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns this story, the owner tables, the ruleset definition and the validation job; changes them through the platform repository only |
| Platform administrator | Owns the branch ruleset and the required-check settings of every repository, and approves the repository inventory rows |
| Solution architect | Approves the ownership model, the team-handle convention and the rule that no individual is named as an owner |
| Service team | Owns its own code owners file and its own rows in the owner table; changes only its own repository |
| ACE team | Owns the shared common module entries in every repository that carries the common module |
| Edge team | Owns the gateway-bff composite route entries of DP-19 |
| RW-AUDIT | Reads the ruleset history, the owner tables and the validation results of a release; writes nothing |

The platform stories carry no service short name, schema, topic or task queue in the §R4 service table, because that table has 19 service rows and no platform row. The team handles of the 20 repositories, the ruleset name and the order of the required-check list are Not specified in the source documents (GAP-1432; ASM-2516); the as-built handle convention is the default used until that point is closed.

##### 11. Data

**Value classes and their source**

| Value class | Examples | Source of the value | Where the value is held |
|---|---|---|---|
| Repository row | A service repository of the 19-service list, and the platform repository | The repository inventory of RWB-PLT-NF01-OPS | The owner table in the platform repository |
| Path pattern | The folder of a service, its per-service migration folder, the common module folder, the composite route folder | The platform template of epic RWB-PLT-TPL and the three DPs | The code owners file of the repository, and the owner table |
| Team handle | The handle of the service team, of the ACE team, of the platform team and of the edge team | The repository host, through the handle convention of RWB-TE-002 | The code owners file only; no business value |
| Ruleset definition | Pull request required, code-owner review, stale approvals dismissed, author excluded, required checks | Template and Rules and RWB-TE-002 BR6 | The branch ruleset of each repository |
| Required-check list | The quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP | The two stories that own the checks | The branch ruleset of each repository |
| Validation result | Pass or fail, the handle or pattern named, the file version | The validation job of the golden pipeline | The build record |

**Naming and values not in the source set**

| Value | Status |
|---|---|
| The team handle of each of the 20 repositories | Not specified in the source documents (GAP-1432; ASM-2516) |
| The ruleset name | Not specified in the source documents (GAP-1432; ASM-2517) |
| The required-check list and its order | Not specified in the source documents (GAP-1432; ASM-2517) |
| The owner of the platform repository and of the template folders | Not specified in the source documents (GAP-1432; ASM-2518) |

The control holds rule definitions, paths and team handles only. It holds no business value, no personal data and no credential: a business value belongs to the parameters contract or the reference data, a personal value belongs to the owning service, masked, and a credential is a key-store reference owned by RWB-PLT-NF04-OPS.

##### 12. Contract

###### 12.1 REST operations provided

None. The story provides no REST operation; it deploys a repository file, a branch ruleset and a pipeline job, and none of them exposes a service path.

###### 12.2 REST operations consumed

None. The story calls no REST operation of its own. The contracts named by DP-07 and DP-15 are consumed by the services themselves and not by this control, and the composite routes of DP-19 are consumed by the gateway-bff; this story only makes sure an owner covers each of them.

###### 12.3 Events published

None. The story publishes no Kafka event; a validation result is a build record and a ruleset decision is a repository-host event, and neither is a business event.

###### 12.4 Events consumed

None. The story consumes no Kafka event and subscribes to no topic.

###### 12.5 Workflows and activities

None. The story runs no Temporal workflow and no activity; the validation job is a pipeline job and the review is a repository-host process.

###### 12.6 Schedules

None. The story creates no Temporal Schedule; the validation job runs on the pull request trigger and the baseline check runs on the pipeline trigger of the platform repository.

###### 12.7 Tables owned

None. The story owns no table and no schema; the owner table is a versioned file in the platform repository and not a database table.

###### 12.8 Contract fakes

None. The story needs no fake: it calls no contract at run time, and the test pull requests, the planted handle and the planted pattern are fixtures of the validation job and not contract fakes.

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | The story provides no REST operation and calls none |
| Kafka | None | The story publishes no event and consumes none |
| Temporal | None | The story runs no workflow, no activity and no Schedule |
| File | 20 written, 20 read | One `.github/CODEOWNERS` file and one owner-table row per repository, written at build time and read by the repository host and the validation job |

None of the four call types crosses a service boundary: the control is repository configuration and pipeline configuration, and the service calls it guards are the ones the service stories own.

##### 13. Solution plan

**Artefacts.** All paths are relative to the platform repository of RWB-PLT-NF01-OPS.

| Path | Artefact | What it holds |
|---|---|---|
| `platform/ownership/owner-table.yaml` | The owner table of the 20 repositories | One row per repository: repository name, the folder set of the template, the owning team handle, and the DP artefact that folder carries (per-service migration folder, reference-data client or composite routes) |
| `platform/ownership/codeowners.template` | The code owners template | The ordered pattern list of a service repository, general paths first, with the team-handle placeholder and no individual entry |
| `platform/ownership/ruleset.template` | The branch ruleset template | Pull request required, code-owner review required, stale approvals dismissed, author excluded, and the required-check list named as a value |
| `platform/pipeline/ownership/validate` | The code-owner validation job | Syntax, handle existence and write access, and pattern-to-file match; a finding fails the build and names the handle or the pattern |
| `platform/ownership/baseline-check` | The ownership baseline check | All 20 repositories have a row and a file; no entry is an individual account; every folder of the template is covered |
| `platform/ownership/README` | The operating note | How a service team changes its own file, how a team change is reviewed by both teams, and how the owner table is raised with a template version |

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The three DPs are not code this story writes; they are the three folders whose owner the owner table must name. DP-15 makes the per-service migration folder a folder of every service repository and therefore an owner row; DP-07 makes the reference-data client a folder of every service that reads a list; DP-19 makes the composite routes a folder of the edge repository and not of a service repository.

**Build steps**

1. Write the owner table with 20 rows from the repository inventory, and name for each row the folder set of the template and the owning team handle.
2. Write the code owners template with the ordered pattern list, general paths first, and the team-handle placeholder; prove it produces one valid file for a service repository and one for the platform repository.
3. Write the branch ruleset template with the four merge controls and the required-check list, and apply it to `main` of the two test repositories.
4. Write the validation job and prove the three refusals with fixtures: an unknown handle, a handle without write access, and a pattern that matches no file.
5. Write the baseline check and prove it fails on a repository without a row, a service whose file covers no folder, and a file that names an individual account.
6. Prove the two required checks: a pull request with a failing quality gate of RWB-PLT-NF05-OPS stays blocked, and one with a failing module boundary test of RWB-PLT-TE001-APP stays blocked.
7. Prove a team change on a test branch: both the old and the new owning team must approve before the merge.
8. Hand the template, the owner table row and the file to each of the 19 service teams and to the platform team, and record the hand-over in the owner table.

**Done when.** All 20 repositories carry one code owners file, one branch ruleset on `main` and one validation job; the validation job fails on an unknown handle, a handle without write access and an unmatched pattern and passes on a clean file; the baseline check fails on an unowned service and on an individual owner and passes on the 20 rows; and a team change on a test branch needs the approval of both teams.

The team handle of each repository, the ruleset name and the required-check list and its order are Not specified in the source documents (GAP-1432; ASM-2516). The ruleset name and the required-check list are ASM-2517, and the owner of the platform repository and of the template folders is ASM-2518.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Repository host | A code owner review is missing on a pull request of any repository, or only the author's own approval is present | Review required from code owners |
| Build log | An owner in a code owners file does not exist or has no write access | owner {team} not found |
| Build log | A pattern in a code owners file matches no tracked file | Not specified in the source documents (GAP-1432; ASM-2515) |

No Workbench message applies and no catalogue message ID is used: these texts come from the repository host and the pipeline, they are never shown to a case user, and a validation finding names the repository, the entry and the rule without repeating any value.

##### 15. Screens and states

None. The story adds no Workbench screen and no screen state. The surfaces it uses are the pull request page of the repository host, which shows the required reviewers and the required checks of the ruleset, and the build record of the validation job; both are read-only for the developer and are changed only through a change to the repository or to the platform repository.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE002-OPS-01 | AC1 | Contract | The 20 repositories: one `.github/CODEOWNERS` each, team handles only, the per-service migration folder and the reference-data client covered in their own repository, the composite routes covered by the edge team, the common module by the ACE team |
| TC-PLT-TE002-OPS-02 | AC2 | Integration | Two test repositories with the ruleset on `main`: a pull request without a code-owner approval, with only the author's approval, with a dismissed approval after a new commit, and with a missing and a failing required check, each blocked |
| TC-PLT-TE002-OPS-03 | AC3 | Component | Fixture files of the validation job: an unknown handle, a handle without write access, an unmatched pattern and a clean file; the three refusals and the passing run with the file version in the build record |
| TC-PLT-TE002-OPS-04 | AC4 | Component | The 20-row owner table and the baseline check: a repository without a row, a service whose file covers no folder of the template, an individual account in a file, and the clean 20-row pass |
| TC-PLT-TE002-OPS-05 | AC5 | End to end | A team change on a test branch: the old and the new owning team each approve, the merge waits for both, and the owner table records the new handle |

The as-built tests of the preserved control stay in RWB-PLT-TE002-APP section 16 under their own identifiers TC-TE-002-01 to TC-TE-002-08, and the full Given, When and Then of every case, old and new, is in Recovery Workbench Test Cases v7.xlsx under the same test case ID.

##### 17. Guardrails

- No individual owner: every entry is a team handle, so no person's absence blocks a merge and no person is named in a repository file (RWB-TE-002 BR7, DL37).
- No business value in code: the file holds paths and handles only, and a threshold, a list value or a name comes from the parameters contract or the reference-data contract (DP-07).
- No personal data in logs, tests or prompts: the fixtures of the validation job are synthetic handles and patterns, and no test pull request carries a real account, a real party or a real document.
- No cross-schema ownership: a service team owns its own migration folder and never approves a change to another service's folder or schema (DP-15; Arch v5 slide 29).
- The common module and the composite routes keep their own owners: the ACE team owns the common module and the edge team owns the gateway-bff composite routes (DP-19).
- A code owner never approves their own change: the author's own approval does not count in any repository (RWB-TE-002 BR6).
- No secret, token or credential in a code owners file, a ruleset value or a pipeline variable; a credential is a key-store reference owned by RWB-PLT-NF04-OPS.
- The ruleset is applied through the platform repository and the repository settings only; no repository is edited by hand outside its own pipeline.

##### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | The code owners file and the branch ruleset of every repository, which guard the module boundary in review | TC-PLT-TE002-OPS-02, TC-PLT-TE002-OPS-05 |
| DP-07 | Reference data and lists through the reference-data contract of rwb-case | The reference-data client folder as an owner row of every service repository that reads a list | TC-PLT-TE002-OPS-01 |
| DP-15 | Per-service Flyway sequence in the service's own schema | The per-service migration folder as an owner row of its own service repository, and no cross-service owner | TC-PLT-TE002-OPS-01, TC-PLT-TE002-OPS-04 |
| DP-19 | Gateway-bff composite route for every screen | The composite route entries owned by the edge team and by no service team | TC-PLT-TE002-OPS-01 |
| Arch v5 slides 20, 29, 35 and 38 | Every service from one template with its own schema and release; one schema and one login per service with the boundary checked in every build; deny by default with a per-service identity; the template and the golden pipeline built once in wave 0 | The one-file-per-repository rule, the required boundary check, the team-only ownership and the golden-pipeline validation job | TC-PLT-TE002-OPS-01, TC-PLT-TE002-OPS-02, TC-PLT-TE002-OPS-03 |

##### 19. Out of scope

- The preserved as-built control of RWB-TE-002: the single-repository code owners file, its validation step and its branch rule stay word for word in RWB-PLT-TE002-APP and are not changed by this story.
- The module boundary test itself: RWB-PLT-TE001-APP owns the test, and this story only names it as a required status check.
- The quality-gate definitions: RWB-PLT-NF05-OPS owns the gates, and this story only names them as required status checks.
- The repository layout, the pipeline stages and the build record: RWB-PLT-NF01-OPS owns the repository and pipeline baseline, and this story adds the ownership control inside it.
- The specific team names and handles: DL37 is still open, so every handle is a value of the owner table and is Not specified in the source documents (GAP-1432; ASM-2516).
- The 19 migrations and their files (RWB-PLT-E1044-OPS), the reference-data contract and its client library (RWB-PLT-E1043-CON) and the gateway-bff composite routes (RWB-PLT-N001-CON): those stories own the artefacts that the owner rows cover.


## RWB-TE-003 Types and contract tests from the API specification

Legacy disposition: Preserved + delta.

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE003-APP | App development | RWB-PLT-TPL | L-PLT-TPL-N | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-PLT-TE003-APP-2 | App development | RWB-PLT-TPL | L-PLT-TPL-M | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE003-APP Types and contract tests from the API specification

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
| Patterns applied | DP01, DP07, DP08, DP13, DP19 |
| Parallel lane | L-PLT-TPL-N |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-019, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: preserved from RWB-TE-003 word for word and re-pointed at the platform template; sections 12 and 13 of the as-built story are kept under "As built (monolith)" and the microservice delta is RWB-PLT-TE003-APP-2. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

##### 2. Business rationale

The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.

##### 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the boundary test exist; the generated packages are listed in the module map as shared.
- The API specification is held in the repository at `api/recovery-api.yaml`, base path /api/recovery/v1, with x-module, x-capability and x-first-release on every operation.
- The permission matrix seed (roles.txt, loaded as the role and permission tables by RWB-E1-037) is available to tests.
- The build property `rwb.release` names the release being built: E1 for 30 November 2026.

##### 4. Flow

1. Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the build.
2. Build: generates the Spring server interfaces and models from the specification.
3. Build: generates the TypeScript types and the typed client for the front end.
4. Build: compiles the service against the generated interfaces and the front end against the generated types.
5. Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.
6. Contract test: calls each implemented operation with its fixture and validates the request and the response against the specification.
7. Access test: calls each operation as a role whose permission lacks the declared right and expects 403 with messageCode MSG-P4-002.
8. Build: reports passed, failed and pending operations; any failure fails the build.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A response no longer matches the specification | Contract test fails naming the operation and the JSON path | Build log: contract broken | AC2 |
| X2 | The specification breaks a lint rule | Build fails before generation | Build log: lint rule broken | AC3 |
| X3 | An operation returns a status not in its specification | Contract test fails | Build log: undocumented status | AC4 |
| X4 | An operation of the current release has no implementation | Build fails | Build log: operation has no implementation | AC5 |
| X5 | An operation of a later release has no implementation | Listed as pending; build passes | Build log: pending | AC6 |
| X6 | The front end uses a field removed from the specification | Front end type check fails | Build log: type error | AC7 |
| X7 | An operation answers 200 to a role without the declared right | Build fails | Build log: access not enforced | AC8 |
| X8 | A role without the right calls an operation | 403 Problem with MSG-P4-002 | MSG-P4-002 | Access test TC-TE-003-09 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the folders of RWB-TE-001 and the specification file |
| Negotiable | Generator settings are build configuration; the rules tested come from the specification |
| Valuable | Screens and services stay in step with one file; every endpoint enforces its right |
| Estimable | Two generators, one lint rule set, one parameterized test class |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below uses one fixture operation that breaks it |

##### 7. Acceptance criteria

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
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The OpenAPI file is the only source of endpoints, request and response schemas | API specification; TSD P2 appendix T-A |
| BR2 | Every operation carries operationId, x-module, x-capability with area and right, and x-first-release; every error response uses the Problem schema | API specification |
| BR3 | Every operation first in the current release or earlier has an implementation and a passing contract test | AC-P2-001-01; REQ-DRI-007 |
| BR4 | Every operation refuses a role whose permission lacks the declared right with 403 and messageCode MSG-P4-002 | REQ-ACA-003; CTL-09 |
| BR5 | Generated code is produced at build time and is not edited by hand | ADR-006 |

##### 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a contract or access test fails.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Change the specification and the implementations; run the build |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the specification file |
| RW-SECADM, security administrator | Owns the permission matrix that the access tests read |
| No approval level from the delegation of authority applies | The story takes no business decision |

##### 11. Data

No business field is read or written. Contract tests run against synthetic fixtures in an in-memory test database.

Field IDs are those in the Logical Data Model and Data Dictionary.

##### 12. Contract

###### 12.1 REST operations provided

None. This story provides no REST operation of its own: it generates each service's server interfaces from that service's OpenAPI 3.1 file and tests every implemented operation against the same file, so the operations it governs are published by the 19 service contract stories under the base path `/api/recovery/<short>/v1` (DP-13). It builds against three platform contracts and two service contracts, and the Ownership Map is the only source of their owners: RWB-PLT-E1043-CON (reference data; the rows belong to P3 rwb-case under the §R5.5 DP-07 ruling and the Ownership Map entries `lov_value`, `reference_row` and `reference_version`), RWB-PLT-E1037-CON (authorise and guard; the rows belong to P4 rwb-access — `role`, `permission`, `masking_rule` and `delegation_limit`), RWB-PLT-N001-CON (gateway-bff composite route; gateway-bff is shared platform and not one of the 19 services, so the Ownership Map carries no service row for it), RWB-P3-E1043-CON (owner P3 rwb-case) and RWB-P4-E1037-CON (owner P4 rwb-access).

###### 12.2 REST operations consumed

None. The story consumes no service operation at runtime: the two service contracts above are consumed only as fakes inside the build (section 12.8), and the three platform contracts supply the guard library, the reference rows and the gateway route. No source document fixes the path of any of them, so no path is written here.

###### 12.3 Events published

None. A build check publishes no event, and the outbox is not involved.

###### 12.4 Events consumed

None. A build check consumes no event.

###### 12.5 Workflows and activities

None. The lint, the two generators and the two test classes run as build steps, not inside a Temporal workflow or activity.

###### 12.6 Schedules

None. The build runs on every pull request and every build of main; there is no schedule.

###### 12.7 Tables owned

None. The story owns no table: the permission matrix the access test reads is P4 rwb-access data, the lists and code values the contract test uses are P3 rwb-case reference data, and the fixtures are synthetic rows in an in-memory test database.

###### 12.8 Contract fakes

None. This story publishes no fake of its own: it consumes the authorise and guard fixture of RWB-PLT-E1037-CON (rows of P4 rwb-access, including role RW-REFADM holding no Case record right), the reference-data fixture of RWB-PLT-E1043-CON (rows of P3 rwb-case, so neither the fixtures nor the generated code hold a business value) and the gateway-bff route fixture of RWB-PLT-N001-CON (shared platform, built from the service answers).

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None at runtime; 2 consumed through fakes | Authorise contract of rwb-access (RWB-P4-E1037-CON through RWB-PLT-E1037-CON) and reference data of rwb-case (RWB-P3-E1043-CON through RWB-PLT-E1043-CON) |
| Kafka | None | No event is published or consumed |
| Temporal | None | The story is a build check |
| File | None | The specification files are read from the repository; no claim-check file is used |

##### 13. Solution plan

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

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A response does not match | contract broken: {operationId} at {path}: {reason} |
| Build log | A status is not specified | undocumented status {status} for {operationId} |
| Build log | No implementation for the current release | {operationId} has no implementation |
| Build log | An operation answers a role without the right | access not enforced for {operationId} |
| MSG-P4-002 | The expected refusal in each access test | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard.

##### 15. Screens and states

No screen in this story. Developers read the report in the build artifacts.

##### 16. Test cases

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
| TC-TE-003-09 | Access | End to end | RW-REFADM calls getCasesCaseidTimers; refused with MSG-P4-002 |

The legacy level `System` maps to `Contract` for TC-TE-003-01 to TC-TE-003-07 and the legacy `Access` test maps to `End to end` for TC-TE-003-08 and TC-TE-003-09; the full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

##### 17. Guardrails

- No business value in code or in a test: capability areas and rights come from the authorise contract of rwb-access and the permission matrix, and lists come from the reference-data contract of rwb-case (DP-07, DP-08).
- No personal data in logs, tests, prompts or report artefacts; fixtures are synthetic and the report holds operation names only.
- The OpenAPI file of a service is the only source of its operations, request and response schemas; generated code is never edited by hand, and a change goes into the file (DP-13).
- One file per service and one base path `/api/recovery/<short>/v1` per service; the story never writes a path of another service and never names a platform path.
- No read of another service's tables; the access test reads rights through the authorise contract and the reference lists through the reference-data contract (DP-01).
- Composite screen operations belong to the gateway-bff route contract, not to a service file (DP-19).
- The contract test and the access test run in the pipeline of the service that owns the file, and a failing operation fails that build.

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | Business Requirements Program, section 5.2 | None | All recovery processes | None | TC-TE-003-01 to TC-TE-003-07 |
| REQ-ACA-003 | The permission matrix is the only source of what a role may do | Business Requirements Program, section 5.4 | None | All recovery processes | None | TC-TE-003-08, TC-TE-003-09 |

##### 19. Out of scope

- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.

#### As built (monolith)

###### 12. Contract

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

###### 13. Solution plan

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


### RWB-PLT-TE003-APP-2 Types and contract tests from the API specification

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
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-019, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: delta copy of RWB-TE-003 for the platform template, one OpenAPI 3.1 file per service plus one for gateway-bff and an index, generation and the contract test in each service's own pipeline at its own base path (Arch v5 slides 11, 13, 14 and 41; DP-01, DP-07, DP-08, DP-13, DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **one OpenAPI 3.1 file per service, generated and contract-tested in that service's own pipeline at that service's own base path, with the access test reading the authorise contract of rwb-access and composite screen operations held in the gateway-bff file**, so that **a break in one provider's contract fails only that provider's build and no screen, service or test drifts from a file it does not own**.

##### 2. Business rationale

The as-built story keeps one OpenAPI 3.1 file for the whole recovery API, 79 operations under one base path, generated into a shared package and tested once in one build. Arch v5 replaces that with 19 deployable services, each with its own base path, its own contract and its own release (slides 13, 14 and 41), and with a shared gateway-bff that composes the screens and is not one of the 19 (slide 20). One file for 19 owners means one owner's edit changes every build, one generated package holds every model, and a break in a service nobody touched stops the other 18. The delta keeps the as-built mechanism and changes the unit of ownership: one file per service plus one for the gateway-bff and an index, the lint and both generators reading only that file, the contract test running at that file's base path in that service's pipeline, and the access test asking the authorise contract of rwb-access instead of reading a seed in the same repository (DP-08). It supports REQ-DRI-007, because every interface still carries its contract test, and REQ-ACA-003, because every endpoint is still tested against the right its file declares and the permission matrix holds. The measure is the count of contract defects found in SIT, with a target of zero, and the blast radius of a failed build, which is one service.

##### 3. Preconditions

- RWB-PLT-TE003-APP is in build: the recovery-api lint rule set, the server and front-end generators, `OperationCatalog`, `RecoveryContractTest`, `RecoveryAccessContractTest` and `ContractFixtures` exist and stay unchanged.
- Each of the 19 services has its short name and its base path `/api/recovery/<short>/v1` (§R4; Arch v5 slide 41), and each one owns its schema `rwb_<name>` (DP-01).
- The platform template supplies the reference-data contract RWB-PLT-E1043-CON, the authorise and guard contract RWB-PLT-E1037-CON and the gateway-bff route contract RWB-PLT-N001-CON, each with its fake; this story takes no build dependency on them and is Day 1 by rule (Template and Rules §R5.7).
- The permission matrix (P4 rwb-access data) and the lists (P3 rwb-case reference data) are reachable through their contracts and their fakes, never through a table read.
- The build property `rwb.release` names the release being built: E1 for 30 November 2026.

##### 4. Flow

1. Split the single file: 19 files, one per service, one file for gateway-bff, and an index; every operation lands in exactly one file and keeps its operationId, x-module, x-capability and x-first-release unchanged.
2. Set each service file's base path to `/api/recovery/<short>/v1` and keep every error response on the Problem schema (DP-13).
3. Put the composite screen operations in the gateway-bff file only; a service file holds the operations of that service (DP-19).
4. Service pipeline: lint the service's own file with the recovery rule set; a missing operationId, x-capability or error response fails that build.
5. Service pipeline: generate the Spring server interfaces and models from that file, and the TypeScript types and typed client for the screens that read that service.
6. Service pipeline: contract test every operation of that file whose x-first-release is at or before `rwb.release`, at the service's own base path, against the same file.
7. Service pipeline: access test every implemented operation through the platform mock of RWB-PLT-E1037-CON, with a role the permission matrix does not give the declared right; expect 403 with messageCode MSG-P4-002.
8. gateway-bff pipeline: lint, generate and contract test the gateway-bff file the same way, including the composite screen operations.
9. Each pipeline publishes its own report and one aggregate report lists passed, failed and pending per service and per release, with the index refreshed for every file it holds.

##### 5. Exception paths

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

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the as-built components of RWB-PLT-TE003-APP and the 19 base paths; it reads no other story's code |
| Negotiable | The file names, the index format and the report layout are settled by the template owner; the ownership rule is fixed |
| Valuable | A contract break is found by the owner that caused it, in its own pipeline, and no other service waits |
| Estimable | A split check, a per-service pipeline wiring and three test classes wired to their own file |
| Small | Fits in one sprint with its tests, proved on two services first |
| Testable | Each criterion runs in a service pipeline against its own file and its fakes |

##### 7. Acceptance criteria

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
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One OpenAPI 3.1 file per service, one for gateway-bff and one index; an operation appears in exactly one file | Arch v5 slides 13, 14 and 41; Template and Rules §R8.4 |
| BR2 | Every operation keeps operationId, x-module, x-capability with area and right, and x-first-release; every error response uses the Problem schema | RWB-PLT-TE003-APP BR1, BR2; API specification |
| BR3 | Each service file carries the base path `/api/recovery/<short>/v1` of its own service and no other service's path | Arch v5 slides 11 and 41; DP-13 |
| BR4 | The lint, the server generator, the front-end generator and the contract test of a service read that service's own file only, in that service's own pipeline | DP-13; Arch v5 slide 20 (one template, contract tests in every build) |
| BR5 | The access test asks the authorise contract of rwb-access and reads the permission matrix; a role without the declared right is refused with 403 and messageCode MSG-P4-002 | RWB-PLT-TE003-APP BR4; REQ-ACA-003; DP-08 |
| BR6 | Composite screen operations belong to the gateway-bff file and are tested there; no service file holds a route that composes another service | Arch v5 slide 20 notes (one hop, never a service that calls another); DP-19 |
| BR7 | No business list value is written in generated code or in a test; lists come from the reference-data contract of rwb-case | DP-07; RWB-PLT-TE003-APP §17 |
| BR8 | A build of one service never depends on the file, the generated code or the build result of another service | Arch v5 slide 20 (each service released on its own); DP-13 |

##### 9. State transitions

None. This story does not change a case status. It changes the build state of each service and of the gateway-bff: a file is linted, generated and tested in its own pipeline, and its state moves from pending to passed or failed without touching another service's state.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Change a service's file and its implementation; run that service's pipeline |
| TechX tech leads (code owners) | Approve a change to a service's file and to the index |
| RW-SECADM, security administrator | Owns the permission matrix that the access test reads through the authorise contract |
| Platform template owner | Owns the split check, the index and the aggregate report |
| No approval level from the delegation of authority applies | The story takes no business decision |

##### 11. Data

No business field is read or written. The contract tests run against synthetic fixtures in an in-memory test database; the permission matrix stays in rwb-access and the lists stay in the reference data of rwb-case, read through their contracts and their fakes.

The location of the index file, the x-module value for gateway-bff operations and the report format across the 19 pipelines are Not specified in the source documents (GAP-1434; ASM-2520; ASM-2521); the defaults of this story are named in section 13.

Field IDs are those in the Logical Data Model and Data Dictionary.

##### 12. Contract

###### 12.1 REST operations provided

None. The story provides no REST operation: it splits the specification into one file per service, one for gateway-bff and an index, and wires the generation and the tests of each file into the pipeline of its owner. The operations it governs are published by the 19 service contract stories at `/api/recovery/<short>/v1` (DP-13) and by the gateway-bff route contract RWB-PLT-N001-CON (DP-19).

###### 12.2 REST operations consumed

None at runtime. The tests consume two contracts through their fakes and write no path of their own: the authorise contract of P4 rwb-access, RWB-P4-E1037-CON, through the platform mock RWB-PLT-E1037-CON (DP-08), and the reference-data contract of P3 rwb-case, RWB-P3-E1043-CON, through the platform fixture RWB-PLT-E1043-CON (DP-07). No source document fixes the path of either one, so none is written here.

###### 12.3 Events published

None. A build check publishes no event.

###### 12.4 Events consumed

None. A build check consumes no event; the access and reference answers arrive through contract fakes, not through Kafka.

###### 12.5 Workflows and activities

None. The split check, the lint, both generators and the two test classes are pipeline steps, not Temporal workflows or activities.

###### 12.6 Schedules

None. Each service pipeline runs on every pull request and every build of main; the index and the aggregate report are refreshed by the pipeline, not by a schedule.

###### 12.7 Tables owned

None. The story owns no table: the rights it tests are P4 rwb-access data, the lists it reads are P3 rwb-case reference data, and the fixtures are synthetic rows in an in-memory test database.

###### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Platform mock of the authorise contract RWB-PLT-E1037-CON (rows of P4 rwb-access) | A role and the rights it holds, including role RW-REFADM holding no Case record right | RecoveryAccessContractTest of every service pipeline |
| Platform fixture of the reference-data contract RWB-PLT-E1043-CON (rows of P3 rwb-case) | The lists and code values a service file declares, so neither the generated code nor a test holds a business value | RecoveryContractTest and ContractFixtures |
| gateway-bff route fixture of RWB-PLT-N001-CON (shared platform) | The composite answer the screens read, built from the service answers | The gateway-bff pipeline and the front end type check |

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None at runtime; 2 consumed through fakes | Authorise contract of rwb-access (RWB-P4-E1037-CON through RWB-PLT-E1037-CON) and reference data of rwb-case (RWB-P3-E1043-CON through RWB-PLT-E1043-CON) |
| Kafka | None | No event is published or consumed |
| Temporal | None | The story is a set of pipeline steps |
| File | None | The 20 specification files and the index are read from the repository; no claim-check file is used |

##### 13. Solution plan

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

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | An operation is not in exactly one file | operation {operationId} in {n} files; expected 1 |
| Build log | A service file does not carry its own base path | base path {base} is not the service's own |
| Build log | A response does not match the service's own file | contract broken: {operationId} at {path}: {reason} |
| Build log | A composite screen operation sits in a service file | composite operation {operationId} belongs to the gateway-bff file |
| Build log | Generated code or a test holds a business value | business value {value} in generated code |
| MSG-P4-002 | The expected refusal in each access test | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard. MSG-P4-002 is the message of RWB-PLT-TE003-APP, carried unchanged.

##### 15. Screens and states

No new screen. The aggregate report is a build artefact and lists, per service and per release, the operations passed, failed and pending, with the base path of the service and the file it was tested against. A composite screen operation appears in the gateway-bff part of the report, never in a service part.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE003-APP2-01 | AC1 | Contract | The single file with 79 operations; 19 service files, one gateway-bff file and the index; no operation twice |
| TC-PLT-TE003-APP2-02 | AC2 | Contract | The rwb-case file at /api/recovery/case/v1, rwb.release E1; report of that service only |
| TC-PLT-TE003-APP2-03 | AC3 | Component | A changed response schema in the rwb-case file; the rwb-payment build and report unchanged |
| TC-PLT-TE003-APP2-04 | AC4 | Contract | RW-REFADM with no Case record right from the platform mock; 403 and MSG-P4-002 |
| TC-PLT-TE003-APP2-05 | AC5 | Contract | One composite screen operation; present once, in the gateway-bff file, tested there |
| TC-PLT-TE003-APP2-06 | AC6 | Component | A code value removed from the reference data; the generated code and the service compile unchanged |

The as-built tests of this legacy key, with their Given, When and Then, stay in RWB-PLT-TE003-APP section 16 and in Recovery Workbench Test Cases v7.xlsx under the same test case ID.

##### 17. Guardrails

- One file per service, one base path `/api/recovery/<short>/v1`, one pipeline; a service never reads, generates from or tests another service's file (DP-13).
- The OpenAPI file of a service is the only source of its operations, request and response schemas; generated code is never edited by hand (DP-01).
- No business value in generated code or in a test: rights come from the authorise contract of rwb-access and lists from the reference-data contract of rwb-case (DP-07, DP-08).
- No personal data in logs, tests, generated artefacts or report rows; fixtures are synthetic and the report holds operation names and base paths only.
- No read of another service's tables; the permission matrix and the reference data are reached through their contracts and fakes, never by a schema read (DP-01).
- Composite screen operations belong to the gateway-bff file and are tested there; no service file composes another service (DP-19).
- A build of one service never waits for, or is failed by, the file or the build of another service.
- The index and the aggregate report are produced by the pipeline from the files; neither is edited by hand.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | One contract test per service file, running at that service's own base path | TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-03 |
| REQ-ACA-003 | The permission matrix is the only source of what a role may do | Access test through the authorise contract of rwb-access and the permission matrix; 403 and MSG-P4-002 | TC-PLT-TE003-APP2-04 |
| DP-01 | Owner's schema `rwb_<name>`; never read another service's tables | Each service generated and tested against its own file and its own model; no schema read in a test | TC-PLT-TE003-APP2-02 |
| DP-07 | Reference-data contract of rwb-case | Lists and code values read through RWB-P3-E1043-CON and its fixture; no business value in code | TC-PLT-TE003-APP2-06 |
| DP-08 | Authorise contract of rwb-access and the guard library | Platform mock RWB-PLT-E1037-CON; refusal with 403 and MSG-P4-002 | TC-PLT-TE003-APP2-04 |
| DP-13 | `/api/recovery/<short>/v1` | One file and one base path per service, tested in its own pipeline | TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-02 |
| DP-19 | gateway-bff composite route | Composite screen operations in the gateway-bff file, tested there | TC-PLT-TE003-APP2-05 |
| Arch v5 slide 11 | OpenAPI 3.1 with `/v1` in the path, contract tests in every build | Per-service file, lint and contract test in each pipeline | TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-02 |
| Arch v5 slide 13 | One hop from the edge to the owner it needs | Composite operations tested in the gateway-bff file; no service calls a service | TC-PLT-TE003-APP2-05 |
| Arch v5 slide 14 | rwb-case and rwb-access contracts, the case and access answers | Case file at `/api/recovery/case/v1`; authorise through rwb-access | TC-PLT-TE003-APP2-02, TC-PLT-TE003-APP2-04 |
| Arch v5 slide 41 | 19 services, one base path, one schema and one login each | 19 files, one base path each, one pipeline each | TC-PLT-TE003-APP2-01, TC-PLT-TE003-APP2-03 |

##### 19. Out of scope

- The preserved as-built generator and its packages, kept word for word in RWB-PLT-TE003-APP section 13 and in its "As built (monolith)" appendix.
- The per-service contract stories of each service epic, which own the operations, the request and response schemas and the fakes of their own file.
- The gateway route contract and its fakes: RWB-PLT-N001-CON.
- The permission matrix content: RWB-E1-037 in the legacy numbering.
- Contract tests for file interfaces: RWB-E1-007 in the legacy numbering.
- The build runner, the pipeline template and the deployment of a service (RWB-PLT-N004-OPS, RWB-PLT-NF01-OPS).


## RWB-TE-004 Masked data in SIT and UAT

Legacy disposition: Split (rework).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE004-APP | App development | RWB-PLT-TPL | L-PLT-TPL-O | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-ITG-TE004-ITG | Integration | RWB-ITG-W1 | L-ITG-W1 | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE004-APP Masked data in SIT and UAT
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE004-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP13, DP19 |
| Parallel lane | L-PLT-TPL-O |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P1-E1065-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-TE-004 for the 19-schema target. The legacy acceptance criteria are kept word for word and re-pointed: the masked copy no longer refills the single `recovery` schema, it loads one staging schema per service and swaps the schema of each of the 19 services, and every legacy value is unchanged (masking rule version "MASK-2026.11", extract "PII-SIT-20261120", business date 2026-11-19, 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903). The legacy endpoint table is rewritten to the per-service base path. The integration copy of the same legacy key is RWB-ITG-TE004-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **platform administrator (RW-PLATADM)** and a **squad member (RW-TRIBE)**, I want **the masked copy that the PII service delivers for SIT or UAT loaded into the 19 `rwb_<name>` schemas of the ACE database — per environment, one staging schema per service (`<schema>_next`), every as-built check kept and applied to every service, the swap of each service's staging schema for that service's live schema only after the checks of all 19 services pass, and a load report per service that names the service, the schema, the extract ID, the business date, the masking rule version and the row counts — instead of one `recovery` schema refilled and swapped as a whole**, so that **SIT and UAT run at production volume and with production data shapes on the schema-per-service estate that will run them, no customer value is exposed, and one refused or missing service never leaves the estate half loaded**.

The rework keeps the loader and the checks of RWB-TE-004 and changes the object of the load. The legacy story hands one flat extract to one `recovery` schema, puts it in `recovery_next` and renames that schema in one step; the target has 19 schemas with one login each and no grant across them (Arch v5 slide 29), so the loader has to resolve each table of the extract to the schema of the service that owns it, stage it there, verify it there and swap it there. The legacy loader was never built (the legacy story is Ready for build, this story is Not started), so nothing built is changed and no as-built code is discarded; the legacy acceptance criteria and their values are carried unchanged and re-pointed, the legacy endpoint table is rewritten to the per-service base path a test user actually reads through gateway-bff, and the personal-data field list is read through the owner's contract instead of from a tag table the loader reads directly.

##### 2. Business rationale

Masked copies are the only way SIT and UAT can run at production volume with production data shapes. Synthetic data proves the code path, not the volume, the skew or the shape of a real record, and NFR-045 allows masked copies in user acceptance while it forbids production data in development ("Synthetic in development, masked in user acceptance"; Proposed, owner Solution architect). The bank's PII service produces the masked copy under the Compliance masking rules, and this story is the load that puts it into SIT and UAT: it refuses any copy that still holds a personal value, keeps dates, keys and row counts unchanged so counts and reconciliations behave as in production, and lets no copy near DEV. It serves REQ-RDF-010 (access to each data product controlled per role, personal data masked by role in line with PDPA) and REQ-ACA-005 (personal data masked by role on every screen and in every agent call), both Must and owned by Compliance, and it is governed by DL26, the Compliance decision on retention and masking that fixes which fields are masked for which role and keeps every personal field masked while the rules carry no values.

The change the rework carries is the object of the load. In the monolith the whole estate is one `recovery` schema: one file set, one `recovery_next` staging schema, one rename, one report. Arch v5 replaces that with 19 schemas `rwb_<name>`, one login each, no grant on another schema and no cross-schema join, view or foreign key (slide 29); slide 41 gives every schema an owner and its first API path, and slide 20 gives every service its own block of tables plus outbox and inbox. A table therefore belongs to exactly one service, and the loader can no longer treat the extract as one bundle. That changes the loader in five ways. The staging object becomes a schema per service rather than one schema. The foreign-key check can only pass inside a single schema, because a key that crosses a schema is forbidden and a service holds another service's ID and asks the owner through its contract. The masking verifier must scan every `is_personal` field in every schema, not the two tables the legacy story happened to name, or a new personal column in a new service is outside the check by construction. The swap becomes one swap per service, and it may only run after the checks of all 19 services pass, so a refusal anywhere leaves the previous copy in place everywhere and the estate is never mixed. And the report becomes per service, because the platform administrator and the squads need to know which schema holds which extract, at which business date and under which masking rule version.

The 19 schemas, their logins and their grants are database work outside this story (RWB-PLT-NF06-DB and the per-service DB stories). What this story owns is the decision of which table goes where, taken from the Ownership Map and from the per-service database stories, and the proof that the copy is complete, masked, consistent and refused in full when any one service fails.

##### 3. Preconditions

- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case and its client library (DP-07). The lists the load compares against — the environment lists and the product groups the manifest totals are counted by — are reference rows read through it and never values in code.
- **RWB-PLT-E1037-CON** is published: the authorise contract of rwb-access and the guard library (DP-08). The load runs under its own identity and is authorised through it, and the masking policy that a test user's read is subject to is that service's policy.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The SIT and UAT endpoint a test user reads on the loaded copy is the per-service base path behind that route; the load provides no route of its own.
- The **two service CON dependencies of the run** are published: **RWB-P3-E1043-CON**, the rwb-case contract behind the reference data (DP-07), and **RWB-P4-E1037-CON**, the rwb-access contract behind the authorise call (DP-08). Both are consumed as published contracts and their fakes, so neither blocks the build (Template and Rules §R5.4, C).
- **RWB-P1-E1065-CON** is published: the rwb-source-data contract behind the personal-data field registry and the `is_personal` tags, which the plan gives to the sandbox and synthetic data story (the legacy RWB-E1-065). The field list the verifier scans comes through that contract; the registry operation itself is a gap and no path is invented for it here.
- The PII service delivers a masked extract per environment to the SIT or UAT intake container, with a manifest: extract ID, business date, masking rule version, and the row count per table, with the case accounts counted per product.
- The 19 schemas `rwb_<name>` and their 19 logins exist in SIT and UAT at the same Flyway version as the extract (Arch v5 slide 29), each with the grant on its own schema only.
- The masking rule version in force is the Compliance-owned version (DL26); until Compliance supplies the rules, every `is_personal` field is replaced by a token.
- The platform administrator (RW-PLATADM) starts the load; squad members hold RW-TRIBE; the load itself runs under the data-load identity SY-DATALOAD.
- The per-service staging schema naming, the per-service extract layout, the personal-data field registry operation and the tool schema name are Not specified in the source documents (GAP-1435; ASM-2522); they are applied as the working defaults of section 13 and are closed by the solution architect before the load is published.

##### 4. Flow

1. PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT, the manifest naming the row count per table and the case accounts per product.
2. Platform administrator: starts the masked copy load in the pipeline for the target environment; the start takes the per-environment lock or is refused if the lock is held.
3. MaskedCopyLoader: refuses to run when the target environment is not SIT or UAT (DEV and PROD are refused), before any file is read.
4. MaskedCopyLoader: preflight over the schema set: every service named in the manifest resolves to an existing schema at the extract's schema version, every service of the 19 has its schema, and no schema is present that the extract does not name. A new service with no schema, or a missing schema, fails the run here, before any file is read.
5. ManifestValidator: checks the extract ID against `tools.masked_copy_load` (a repeat is skipped), the masking rule version against the version in force, the schema version against the target, and the control totals of the manifest.
6. MaskedCopyLoader: resolves each table of the extract to the code of the service that owns it, from the Ownership Map and the per-service database stories, and loads each service's tables into that service's own staging schema `<schema>_next` under the service's staging grant, never writing into a second service's schema.
7. MaskedCopyLoader: runs the load checks of CTL-02 per file and per service — business date, structure, control totals (row count per table and per product) and keys — and checks that the foreign keys resolve inside each staging schema.
8. MaskingVerifier: scans every column tagged `is_personal`, in every one of the 19 staging schemas, for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address. The tag source is the personal-data field list read through the rwb-source-data contract.
9. MaskedCopyLoader: holds every swap until the checks of all 19 services have passed; on success, PerServiceSchemaSwap swaps each service's `<schema>_next` for that service's live schema, one service at a time under the environment lock.
10. LoadReportWriter: writes the load report and the `tools.masked_copy_load` row per service: the service, the schema, the extract ID, the business date, the masking rule version, the rows per table and the check results.
11. Squad member: runs SIT or UAT tests on the masked copy, reading the case through the per-service base path behind gateway-bff and the authorise call of rwb-access.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A personal column holds a value that looks personal | Load refused in full in every one of the 19 schemas; previous copy stays in use in all of them | MSG-P1-002 | AC2 |
| X2 | Row count differs from the manifest | Load refused in full; previous copy stays | MSG-P1-002 | AC3 |
| X3 | The target environment is DEV or PROD | Load refused before reading any file | MSG-P1-002 | AC4 |
| X4 | The same extract ID is loaded again | Load skipped; report shows the earlier load | None | AC5 |
| X5 | The manifest's masking rule version is not the version in force | Load refused in full | MSG-P1-002 | AC6 |
| X6 | A second load starts while one runs | Second start refused by the per-environment lock | MSG-P2-006 | AC7 |
| X7 | A service's checks fail after the other services have passed | No service is swapped; every staging schema of the run is discarded and every previous copy stays in use | MSG-P1-002 | AC8 |
| X8 | A service appears in the extract with no schema in the environment, or a schema of the 19 is missing | Preflight fails the run before any file is read; no staging schema is written and no swap happens | MSG-P1-002 | AC8 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three platform contracts, the two service contracts of the run and the rwb-source-data contract of the field list; the reader path is reached through gateway-bff, so no service has to be built first; no screen |
| Negotiable | The staging suffix, the swap order, the tool schema and the per-service layout are working defaults recorded as assumptions; the checks, the environment guard and the swap-after-all-checks rule are fixed by NFR-045, DL26 and Arch v5 slide 29 |
| Valuable | SIT and UAT run at production volume with no customer data exposed, on the 19-schema estate that will run them, and one refused service cannot leave the estate half loaded |
| Estimable | One tool module, four service classes, one per-service swap, one environment lock, one report writer and the configuration of the 19 schemas |
| Small | Fits in one sprint with its tests, on a test extract with a manifest |
| Testable | Each criterion runs on a test extract with a manifest against throwaway staging schemas, with the two contract fakes of section 12.8 |

##### 7. Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with row counts per product

  Scenario: AC1 Masked copy (legacy RWB-TE-004 AC1)
    Given a masked copy from the PII service
    When it is loaded into SIT
    Then every column tagged is_personal in interaction and document_field holds a token or a masked value
    Then the row counts keep their shape: the count per table and per product equals the manifest
    Then each person key joins to the same case_party and case_account rows as in the extract

  Scenario: AC2 A personal value left in the copy (legacy RWB-TE-004 AC2)
    Given interaction row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in summary
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in interaction.summary"
    Then the previous SIT copy stays in use

  Scenario: AC3 Totals that do not match the manifest (legacy RWB-TE-004 AC3)
    Given the case_account file holds 28,118 rows
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals case_account 28,118 against 28,119"

  Scenario: AC4 A copy aimed at DEV (legacy RWB-TE-004 AC4)
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file

  Scenario: AC5 The same extract twice (legacy RWB-TE-004 AC5)
    Given extract "PII-SIT-20261120" was loaded into SIT on 2026-11-20
    When it is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20

  Scenario: AC6 A masking rule version that is not in force (legacy RWB-TE-004 AC6)
    Given a manifest with masking rule version "MASK-2026.10"
    When the copy is loaded into UAT
    Then the system refuses the load in full with MSG-P1-002 and check "masking rule version MASK-2026.10 is not in force"

  Scenario: AC7 A second load while one runs (legacy RWB-TE-004 AC7)
    Given a masked copy load into SIT is running
    When a second load into SIT starts
    Then the system refuses the second load with MSG-P2-006

  Scenario: AC8 One staging schema per service and the swap only after every service passes (new, D-RCV-60)
    Given the manifest names each service it carries data for, with the row counts per table
    Given the 19 schemas rwb_<name> exist in SIT at the extract's schema version
    When the masked copy load starts for SIT
    Then MaskedCopyLoader resolves each table to the schema of the service that owns it and loads it into that service's staging schema <schema>_next
    Then it runs the environment guard, the extract-ID and masking-rule checks, the control totals, the masking verifier over every is_personal field and the foreign-key resolution for every service
    Then no staging schema is swapped while any service's checks are still open
    When the checks of every service have passed
    Then PerServiceSchemaSwap swaps each service's staging schema for that service's live schema, one service at a time under the environment lock
    Then the load report names the service, the schema, the extract ID, the business date, the masking rule version and the row counts
    When one service's checks fail, or the extract names a service with no schema, or a schema of the 19 is missing
    Then no service is swapped and every previous copy stays in use, and a missing schema fails the run before any file is read with MSG-P1-002
```

**Note on the criteria.** AC1 to AC7 are the legacy criteria of RWB-TE-004, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed, and the checks they name are kept as the legacy story specified them. AC8 is the only new criterion and it carries no business value: it tests the per-service staging and the swap-after-all-checks rule of the 19-schema target. The publisher of the extract is still the PII service, which is an outside system and not a contract of this estate.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only | NFR-045; CTL-11 |
| BR2 | Every field tagged personal is masked or tokenized under the masking rules in force; the tag source is the personal-data field list read through the rwb-source-data contract, and the verifier scans every `is_personal` field in every one of the 19 schemas, not the two tables of the legacy story | Masking rules (Compliance, DL26); DP-05; this story |
| BR3 | A copy with any personal value left in it is refused in full, in every schema of the run | CTL-11; DQ check "Refuse the load" |
| BR4 | Dates and keys are not masked; counts equal the manifest per table and per product | CTL-02; REC-01, REC-02 |
| BR5 | The same customer gets the same token in every table and in every schema, so joins hold; a token crosses a schema only through the owner's contract, never through a join | Mapping rule "Personal data" (s2t.txt); DP-01 |
| BR6 | With no masking rule loaded, every personal field is replaced by a token | DL26 ("every personal field stays masked") |
| BR7 | One staging schema per service, named `<schema>_next`; every check of the as-built story runs per service; the swap of a service's staging schema may run only after the checks of all 19 services pass, one service at a time under the environment lock; on any failure the previous copy stays in place everywhere and the estate is never mixed | Arch v5 slide 29; this story (ASM-2522, ASM-2523) |

##### 9. State transitions

The case status does not change in this story. The states below are the load, the schema in the run and the copy of the environment.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | Platform administrator starts the load | Environment is SIT or UAT and the lock is taken | Preflight |
| Preflight | Schema set does not match the extract | A service with no schema, or a missing schema, or an extract with no service | Refused (no file read, no staging schema written) |
| Preflight | Environment is DEV or PROD | None | Refused (no file read) |
| Preflight | Manifest check fails | Extract ID already loaded, masking rule version not in force, schema version differs | Refused |
| Preflight | Preflight passes | None | Running |
| Running | Files load into the per-service staging schema | The service's staging grant holds | Staging |
| Staging | Control totals, keys and foreign keys pass for that service | None | Checks passed (for that service) |
| Checks passed | Another service's checks are open | None | Held (no swap) |
| Checks passed | The checks of every service have passed | None | Swapping |
| Swapping | The service's `<schema>_next` is renamed to its live schema | None | Swapped (per service) |
| Swapping | A swap fails | None | Refused in the run; the remaining services are not swapped and the previous copy is restored from the retained one |
| Any state before Swapping | Any check fails | None | Refused; staging schemas discarded; previous copy in use everywhere |
| Preflight | The extract ID is already loaded | None | Skipped (report names the earlier load) |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Starts the load in SIT or UAT, owns the intake containers, reads the load report per service and reruns a refused run |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules and their version (DL26); reads the verifier result of a run |
| RW-TRIBE, Tribe lead and squad members | Run tests on the loaded copy with their test users' rights, through the per-service base path behind gateway-bff |
| SY-DATALOAD, data load | The identity the loader runs under in SIT and UAT; holds the staging grant on the schemas of the run and writes no live schema outside the swap |
| ACE database administrator | Owns the 19 schemas, the 19 logins and the staging schemas of each environment; not a Workbench role |
| No role | May run a copy in DEV or PROD, read another service's schema, swap one service's schema on its own, or copy a masked extract from SIT or UAT to another environment |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-024 to DF-CAS-029 | case_account | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-DOC-012 to DF-DOC-017 | document_field | all fields | Write |
| DF-EXT-001 to DF-EXT-012 | party_ext | all fields | Write |
| DF-EXT-013 to DF-EXT-026 | contact_point_ext | all fields | Write |
| DF-REF-105 | sys_fields | is_personal | Read |

The other recovery tables in the extract load the same way. Field IDs are those in the Logical Data Model and Data Dictionary.

Each table above now lives in the schema of the service that owns it, per the Ownership Map: `recovery_case`, `case_account` and `case_party` in `rwb_case` (P3 rwb-case, Arch v5 slide 41); `interaction`, `party_ext`, `contact_point_ext` and `sys_fields` in `rwb_source_data` (P1 rwb-source-data, the ledger and the extension tables under the R-PREC default ruling and DP-18); `document_field` in `rwb_document` (P5 rwb-document). The `Write` rows above are writes into that service's staging schema of the run and, after the swap, into its live schema; no row is written into a second service's schema and no foreign key crosses a schema (DP-01; Arch v5 slide 29). The `is_personal` read is now a read of the personal-data field list through the rwb-source-data contract, and `sys_fields.is_personal` in `rwb_source_data` is the tag source behind that list, never a table the loader opens directly.

The per-service staging schema naming, the layout of the extract per service, the operation that returns the personal-data field list and the name of the tool schema are Not specified in the source documents (GAP-1435; ASM-2522), and the tool schema and the field-list default are ASM-2524. The loader takes the working defaults of section 13 until the gap closes.

##### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it has no REST base, no topic, no task queue and no schema of its own, and none is invented for it.

###### 12.1 REST operations provided

None. The loader is a tool outside the ACE services and provides no REST operation; the platform administrator starts it in the pipeline and reads its report there. The reserved platform names of the naming rule — a platform REST base, a platform event topic and a platform task queue — are not used by this story.

###### 12.2 REST operations consumed

| Method | Path | Owner | Ownership Map row | Use |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | `GET /cases/{caseId}` | The masked case a SIT or UAT test user reads on the loaded copy, with its parties and accounts, to prove that the load left the joins intact (AC1) |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | `POST /authorise` | The right, the scope and the masking policy of the identity that starts the load and of the test user who reads the copy; a role without the right is refused with MSG-P4-002 (AC1) |

Both calls are one hop to the owning service on that service's own base, with the 2 s client budget (DP-11, DP-13). The test user's case read is reached through the gateway-bff composite route (DP-19).

Three contract dependencies are named and consumed as published contracts, not as paths of this story:

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1043-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1043-CON`, epic RWB-PLT-LIB) | The environment lists and the product groups the manifest totals are counted by (DP-07) |
| `RWB-P4-E1037-CON` | P4 rwb-access (the platform contract behind it is `RWB-PLT-E1037-CON`, epic RWB-PLT-LIB) | The authorise envelope, the error contract and the masking policy of the reader and of the load identity (DP-08) |
| `RWB-P1-E1065-CON` | P1 rwb-source-data | The personal-data field registry and the `is_personal` tags the verifier scans; the registry operation is a gap and no path is invented for it (GAP-1435; ASM-2524) |

No path, version or payload of a contract is repeated here; they belong to the contract stories that publish them.

###### 12.3 Events published

None. The load is a pipeline tool and publishes no business event; a run, a refusal and a swap are recorded in `tools.masked_copy_load` and in the report, and nothing is produced on a Kafka topic.

###### 12.4 Events consumed

None. The load waits on no topic: it is synchronous in the pipeline, its result is its own run row, and the reader assertions are made through the two operations of 12.2.

###### 12.5 Workflows and activities

None. No Temporal workflow, activity or Nexus operation is started or awaited; the load is a batch tool of the SIT and UAT pipeline and not a service worker, and it starts nothing on a service task queue.

###### 12.6 Schedules

None. The masked copy load is a manual pipeline stage started by the platform administrator for SIT or UAT after the PII service delivers an extract; it is not a scheduled job and not in the production job list, and it creates no Temporal Schedule.

###### 12.7 Tables owned

| Table | Schema | Owner | Note |
|---|---|---|---|
| `masked_copy_load` | `tools` | the loader (outside the 19 services) | One row per run and per service: extract ID, environment, business date, masking rule version, service, schema, row counts, check results and result. The schema name is the working default ASM-2524 (GAP-1435) |

The tool schema sits outside the 19 service schemas and is not one of them; the loader owns no business table, and it writes no service table except through the per-service swap of a staging schema that it filled.

###### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case case read fake | `RWB-P3-E1043-CON` behind `GET /api/recovery/case/v1/cases/{caseId}` | One masked case with its parties and accounts and the environment lists and product groups the manifest totals are counted by (AC1, TC-TE-004-01, TC-TE-004-08) |
| rwb-access authorise fake | `RWB-P4-E1037-CON` behind `POST /api/recovery/access/v1/authorise` | The case right granted to RW-TRIBE and to the load identity, the masking policy in force, and a refusal with MSG-P4-002 for a role without the right (AC1, TC-TE-004-08) |

The PII service is an outside system that supplies a file: it is not a contract of this estate and is not faked.

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 2 consumed | The case read of rwb-case and the authorise call of rwb-access, one hop each, 2 s (DP-11, DP-13); none provided |
| Kafka | None | No event is published or consumed by the load |
| Temporal | None | The load is a pipeline tool, not a workflow or an activity |
| File | 1 | The masked extract and its manifest, read from the SIT or UAT intake container |

##### 13. Solution plan

**Deliverables.** The tool module `tools/masked-copy-loader`, Java package `recovery.tools.maskedcopy`, built as a separate build module that is not packaged into any ACE service (the legacy packaging is kept); the per-service staging and swap; the table-to-schema resolution from the Ownership Map; the load report; and the pipeline stage with the per-environment lock.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| MaskedCopyLoader | Job | Spring Batch job: environment guard, schema-set preflight, table-to-schema resolution, file load into one staging schema per service, checks, and the hand-off to the swap (BR1, BR2, BR7) |
| ManifestValidator | Service | Extract ID against `tools.masked_copy_load`, masking rule version against the version in force, schema version against the target, control totals per table and per product (BR4) |
| MaskingVerifier | Service | Personal value patterns over every `is_personal` field in every staging schema, with the field list read through the rwb-source-data contract (BR2, BR3) |
| LoadReportWriter | Service | Writes the load report and the `tools.masked_copy_load` row per service (BR7) |
| PerServiceSchemaSwap | Job | Swaps `<schema>_next` for the live schema of one service, only after every service's checks pass, one service at a time in the configured order, and restores from the retained previous copy if a swap fails (BR7) |
| EnvironmentLock | Service | One advisory lock per environment, so a second load cannot start and two swapper instances cannot run (BR7) |

**Database.** No new business table. The stage fills `<schema>_next` for each service of the run, checks the foreign keys inside that schema, and renames the staging schema to the live schema of the service after every service's checks pass; an advisory lock per environment prevents two loads at once; the tool table `tools.masked_copy_load` in schema `tools` records the extract ID, the environment, the business date, the masking rule version, the service, the schema, the row counts and the result. The schema `tools` is outside the 19 service schemas and is the working default ASM-2524 (GAP-1435; ASM-2522).

**Configuration and reference data.**

- `rwb.maskedcopy.allowed-environments=SIT,UAT`.
- `rwb.maskedcopy.intake-container` per environment, owned by the platform administrator.
- `rwb.maskedcopy.schemas`: the 19 schema names and the service code of each, used by the preflight and the swap order.
- `rwb.maskedcopy.staging-suffix=_next`, the working default of ASM-2522.
- `rwb.maskedcopy.swap-order`, the working default of ASM-2523.
- `rwb.maskedcopy.tool-schema=tools` and `rwb.maskedcopy.tool-table=masked_copy_load`, the working default of ASM-2524.
- The masking rule version and the allowed environment and product-group lists, read as reference rows (DP-07); the masking rule version comes from the Compliance-owned rules (DL26) and is never a value in code.
- The personal-data field list, read through the rwb-source-data contract (RWB-P1-E1065-CON); the registry operation is the gap of GAP-1435.
- Feature flag: `rwb.dataengine.masked-copy`, unchanged from the legacy story.

**Build steps**

1. Environment guard reading the deployment environment: refuse anything that is not SIT or UAT, before any file is read.
2. Schema-set preflight over `rwb.maskedcopy.schemas` and the manifest: a service with no schema, a missing schema and an extract naming no known service each fail the run here.
3. ManifestValidator with the extract ID check against `tools.masked_copy_load`, the masking rule version check and the schema-version check.
4. Table-to-schema resolution from the Ownership Map and the per-service database stories, and the file load into `<schema>_next` with the CTL-02 checks and the manifest totals.
5. MaskingVerifier over every `is_personal` field of every staging schema, with the field list from the rwb-source-data contract and the patterns of the as-built verifier.
6. Foreign-key resolution inside each staging schema, then the hold until every service has passed.
7. PerServiceSchemaSwap with the configured order and the environment lock, the retained previous copy and the restore path of a failed swap.
8. LoadReportWriter and the `tools.masked_copy_load` row per service.
9. Tests for AC1 to AC8 on a test extract, with the two contract fakes, and the reader test of a SIT test user through the per-service base path behind gateway-bff.

**Done when.** The nine test cases of section 16 pass, the checks of the as-built story are exercised per service on a test extract, a failure in one service leaves every previous copy in place, and the first masked copy of the 19 schemas is in SIT before the Epic 1 SIT run.

The per-service staging name, the extract layout per service, the field-list operation and the tool schema name are Not specified in the source documents (GAP-1435; ASM-2522); the swap order and the lock are ASM-2523 and the tool schema and field-list default are ASM-2524.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The masked copy is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P2-006 | A load starts while one runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | A test user without the right reads the copy | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-TE-004 and this story adds no message text. In MSG-P1-002 the {source}, {date} and {check} of a per-service refusal name the service, the business date and the check; the check names the schema and the table of the service that failed. Thai text for each message follows decision DL10.

##### 15. Screens and states

No screen in this story, and no new screen state. The platform administrator and the squads read the load report in the pipeline, and a test user sees the masked copy through the normal SIT and UAT screens, which reach a service through the gateway-bff composite route (DP-19) and the per-service base path (DP-13), with personal fields shown as tokens or masked values under the masking policy of rwb-access (DP-08).

The load report is the surface of this story: one section per service, with the service, the schema, the extract ID, the business date, the masking rule version, the rows per table, the control totals, the verifier result and the swap result, and never a value from the copy.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-004-01 | AC1, BR2, BR4, BR5 | Component | Test extract PII-SIT-20261120 with 28,119 accounts |
| TC-TE-004-02 | AC2, BR3 | Component | Injected value with a valid check digit in interaction row 4,512 |
| TC-TE-004-03 | AC3, BR4 | Component | case_account file with 28,118 rows |
| TC-TE-004-04 | AC4, BR1 | Component | Target environment DEV |
| TC-TE-004-05 | AC5 | Component | Extract loaded twice |
| TC-TE-004-06 | AC6, BR6 | Component | Manifest with MASK-2026.10 |
| TC-TE-004-07 | AC7 | Component | Two loads into SIT at once |
| TC-TE-004-08 | Access | End to end | SIT test user with RW-REFADM calls GET /cases/{caseId}; refused with MSG-P4-002 |
| TC-PLT-TE004-APP-09 | AC8, BR7 | Integration | The 19 schemas of SIT at the extract's version with one staging schema per service; one service's checks failed, then a service named by the extract with no schema and a missing schema |

The eight legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the loader and verifier checks TC-TE-004-01 to TC-TE-004-07 become Component, and the legacy Access row TC-TE-004-08 becomes End to end. TC-PLT-TE004-APP-09 is the new row for AC8. The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same TC ID.

##### 17. Guardrails

- No business value in code: the masking rules and their version belong to Compliance (DL26), the allowed environments are properties, and the lists the totals are counted by are reference rows read through the contract of rwb-case (DP-07).
- No personal data in logs, reports, tests or prompts: the load report and the `tools.masked_copy_load` row hold counts, totals, schema names and check names, never a value; test extracts are built from masked or synthetic data.
- ACE data only through the owner's contract or the `v_ace_*` views (DP-05): the loader reads the masked extract as a file, takes no ACE table directly, and where it needs ACE-sourced data it reads through the rwb-source-data contract.
- No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.
- No read of another service's schema and no cross-schema key: the loader resolves each table to one owning schema, writes only that schema's staging schema, and asks any other owner through its contract (DP-01).
- The tool never writes a live service schema outside the swap: a live schema changes only when PerServiceSchemaSwap renames into it after every service's checks have passed, and never row by row.
- The tool stays outside the ACE services and never becomes a runtime dependency of a service; it runs only in SIT and UAT (the legacy guardrail, kept).
- One refusal refuses the estate: a failure in any service means no swap anywhere and every previous copy stays in use.

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, section 4; Program section 6.7 | None | All recovery processes | CTL-02, CTL-11; DL26 | TC-TE-004-01 to TC-TE-004-07, TC-PLT-TE004-APP-09 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Epic 1, section 4 | None | All recovery processes | CTL-11 | TC-TE-004-01, TC-TE-004-08, TC-PLT-TE004-APP-09 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | Each table of the extract goes into the schema of the service that owns it, and no second service's schema is read or written | TC-TE-004-01, TC-PLT-TE004-APP-09 |
| DP-05 | Template and Rules §R5.5; Arch v5 slides 29 and 41 | No ACE table is read directly; the personal-data field list comes through the rwb-source-data contract and the ACE views behind it | TC-TE-004-01, TC-TE-004-02 |
| DP-07 | Template and Rules §R5.5 | The environment lists and the product groups the manifest totals are counted by are read through the reference-data contract of rwb-case | TC-TE-004-01, TC-TE-004-03 |
| DP-08 | Template and Rules §R5.5; Arch v5 slides 14 and 35 | The load identity and the reading test user are authorised through the authorise contract of rwb-access, and a role without the right is refused with MSG-P4-002 | TC-TE-004-08 |
| DP-13 | Template and Rules §R5.5 | The endpoint a test user reads on the loaded copy is the per-service base path, not the monolith base; the load adds no path | TC-TE-004-08 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 20 | The test user reaches the case through the gateway-bff composite route, and the load provides no route of its own | TC-TE-004-08, TC-PLT-TE004-APP-09 |
| Arch v5 slide 29 | One login and one schema per service, no grant across schemas, no cross-schema keys, boundary test in every build | The per-service staging schema, the inside-a-schema foreign-key check and the swap-after-all-checks rule | TC-PLT-TE004-APP-09 |
| Arch v5 slide 35 | Personal data stays in the owning service, masked; deny by default | Every `is_personal` field of every staging schema is verified before any swap, and the copy never leaves SIT or UAT | TC-TE-004-02, TC-PLT-TE004-APP-09 |
| Arch v5 slides 20 and 41 | Each service writes its own schema, plus outbox and inbox; one owner per schema and its first path | The table-to-schema resolution and the per-service report | TC-PLT-TE004-APP-09 |
| NFR-045 | Synthetic in development, masked in user acceptance | The environment guard before any file is read, and no copy from SIT or UAT to another environment | TC-TE-004-04, TC-PLT-TE004-APP-09 |
| DL26 | The masking rules and their version are Compliance's | The version in force is compared with the manifest and is never a value in code; with no rule loaded every personal field is a token | TC-TE-004-06 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON | Contract | H: the reference-data contract, the authorise contract and the gateway-bff route contract this story builds against |
| RWB-P3-E1043-CON, RWB-P4-E1037-CON, RWB-P1-E1065-CON | Contract | C: the two service contracts consumed at run time and the source-data contract behind the personal-data field list |
| RWB-ITG-TE004-ITG | Integration | The integration copy of RWB-TE-004; it exercises this loader across the 19 schemas and owns none of it |
| RWB-PLT-NF06-DB and the per-service DB stories | DB | Related work outside this story: the 19 schemas, the 19 logins and the staging schemas of each environment |

##### 19. Out of scope

- Synthetic data in DEV (RWB-E1-065 in the legacy numbering; RWB-P1-E1065-CON and the P1 stories behind it).
- The content of the masking rules, the values masked per field and per role, and their retention periods: Compliance owns them under DL26.
- Masking on the screens and the masking policy of a reader: rwb-access (P4) owns them, and `RWB-P4-E1037-CON` publishes the contract.
- The PII service itself, which the bank runs, and its extract contract, which is outside the source set.
- The masked debt sale data tape (FEAT-DBS-03, Epic 5).
- The integration copy of this legacy key, RWB-ITG-TE004-ITG, which exercises the loader end to end across the 19 schemas.
- The 19 schemas, the 19 logins and their grants: RWB-PLT-NF06-DB and the per-service database stories.
- The contents of `RWB-PLT-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1043-CON`, `RWB-P4-E1037-CON` and `RWB-P1-E1065-CON`; this story builds against them and adds no path.


### RWB-ITG-TE004-ITG Masked data in SIT and UAT — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-TE-004 for the wave-1 integration epic. The monolith loader that refilled one `recovery` schema becomes a tool outside the ACE services that fills the 19 per-service schemas of the ACE database table by table, verifies every `is_personal` column in every schema before a single-step staging swap, and records its run in its own `tools.masked_copy_load` table; the reader path is the case contract of rwb-case with the masking policy of rwb-access, and no service reads another service's tables (DP-01, DP-08). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE004-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-004 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP13, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P1-E1065-APP, RWB-PLT-TE004-APP, RWB-P1-E1069-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

##### 1. Story

As a **QA integration engineer**, I want **the masked copy of RWB-TE-004 loaded and verified across the 19 per-service schemas of the ACE database in SIT and UAT — each table filled into the schema of the service that owns it, every `is_personal` column scanned in every schema before the swap, one staging-to-live swap per environment, and the masked case read back through the contracts of rwb-case, rwb-source-data and rwb-access**, so that **SIT and UAT run at production volume and with production data shapes while no customer value is exposed, and the masked copy is proven on the schema-per-service estate that will run it rather than on the single `recovery` schema of the monolith**.

##### 2. Business rationale

SIT and UAT must show that loads, allocation, reconciliation and reports work at production volume and with production data shapes, which synthetic data does not prove. NFR-045 allows masked copies in user acceptance and forbids production data in development; the bank's PII service produces the masked copy under the Compliance masking rules, and RWB-TE-004 loads it into SIT and UAT only, refuses any copy that still holds a personal value, and keeps dates, keys and row counts unchanged so counts and reconciliations behave as in production.

In the target the store is no longer one `recovery` schema. The ACE database holds one schema and one login per service, with no cross-schema joins, views or foreign keys, and a boundary test in every build fails on any cross-schema reference (Arch v5 slides 29 and 41, ADR-014). The masked copy therefore lands table by table in 19 schemas `rwb_<name>`, each table in the schema of the service that owns it (DP-01), and the property the legacy story called "the same token joins" is no longer a join inside one schema: it is proven through each service's own contract — a case read on rwb-case, a customer and an account read on rwb-source-data — with the masking applied by rwb-access on the reader path (DP-08). The loader stays outside the ACE services, as the legacy story already required, and is a tool with its own `tools.masked_copy_load` table, so it never becomes a service that reads service schemas at runtime.

None of that is proven by any single service story. A table that lands in the wrong schema, a schema that is swapped while another is refused, a verifier that stops at the first schema, a mask that does not apply to the reader, and a copy that reaches DEV are all failures that only appear across the 19 schemas and the four contracts. This story builds and runs that proof in SIT and UAT, and it publishes no operation of its own.

##### 3. Preconditions

- The ACE database holds the 19 Recovery schemas with one login each: `rwb_case`, `rwb_decision`, `rwb_access`, `rwb_deviation`, `rwb_valuation`, `rwb_treatment`, `rwb_guarantee`, `rwb_litigation`, `rwb_asset`, `rwb_debtsale`, `rwb_writeoff`, `rwb_document`, `rwb_comms`, `rwb_payment`, `rwb_partner`, `rwb_integration`, `rwb_source_data`, `rwb_reporting` and `rwb_agent`, each at the same Flyway version as the extract (Arch v5 slide 29; RWB-PLT-NF06-DB and the per-service DB stories).
- Each service login holds grants on its own schema only and no grant on any other schema, so a table written into the wrong schema is refused by the database and not only by the tool (Arch v5 slide 29; RWB-P1-E1069-APP for the boundary rule).
- RWB-PLT-TE004-APP is done: the masked-copy loader, the manifest validator, the masking verifier and the load-report writer exist as a build module outside the ACE service, with properties `rwb.maskedcopy.allowed-environments=SIT,UAT` and `rwb.maskedcopy.intake-container` per environment.
- RWB-P1-E1065-APP is done: the `is_personal` tags in `sys_fields` and the personal-data patterns of the synthetic-data verifier are available to the loader (DP-05, `sys_fields` is P1's).
- RWB-P1-E1069-APP is done: the ACE view contract, the boundary test and the data-dictionary surface exist, and the four extension tables `party_ext`, `contact_point_ext`, `account_ext` and `valuation_ext` are in P1's schema (DP-05).
- The PII service delivers the masked extract per environment to the SIT or UAT intake container with a manifest: extract ID, business date, masking rule version and row count per table. The PII service is outside the source set and outside this story; its extract contract is Not specified in the source documents (GAP-0379; ASM-0547).
- The extract in hand is "PII-SIT-20261120" for business date 2026-11-19, with masking rule version "MASK-2026.11" in force (RWB-TE-004 sections 7 and 16).
- rwb-access answers the authorise call and holds the test roles used by SIT and UAT, with their masking policy rows in `masking_rule` (P4) and their letters as data (DP-08).
- The environment lists, the product groups and the masking reference rows are reference data read through rwb-case's reference-data contract, never values in the loader (DP-07).
- The table-to-schema map is Not specified in the source documents (GAP-0379; ASM-0547); under ASM-0547 the loader builds it from the Ownership Map and the per-service DB stories.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The integration run is written on Day 1 against the three integration stories and is run when they are in SIT; a fake is never used in their place.

##### 4. Flow

1. Pipeline: reads the target environment, the intake container and the service list from configuration, and refuses to start when the environment is not SIT or UAT.
2. Harness: runs the preflight of section 13 — the 19 schemas and logins exist at the extract's Flyway version, the loader module is present, the reference lists resolve through the rwb-case contract, and P4 answers the authorise call; a missing element stops the run before any file is read.
3. Loader: reads the manifest and checks the extract ID against `tools.masked_copy_load`, the masking rule version against the version in force, and the schema version against every target schema.
4. Loader: runs the CTL-02 load checks on each file — business date, structure, control totals (row count per table), keys — with the manifest's 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903.
5. Loader: builds its table-to-schema map from the Ownership Map and the per-service DB stories (ASM-0547): `recovery_case`, `case_account` and `case_party` into `rwb_case`; `interaction`, `party_ext`, `contact_point_ext`, `account_ext`, `valuation_ext`, `sys_fields` and the other P1 tables into `rwb_source_data`; `document_field` and the other document tables into `rwb_document`; and every remaining table into the schema of its owner.
6. Loader: loads the files into a staging schema per target schema in one run, checks that the foreign keys resolve inside each schema, and holds the swap until every schema has passed.
7. MaskingVerifier: scans every column tagged `is_personal` in every one of the 19 staging schemas — not only `interaction` and `document_field` — for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.
8. Pipeline: on a verifier or load failure in any one schema, refuses the whole load, leaves the previous copy in every schema and reports the schema and the check that failed.
9. Loader: on success, swaps the staging schema for the live schema in one step per environment and writes the run to `tools.masked_copy_load`: extract ID, environment, business date, masking rule version, rows per table per schema and check results.
10. Harness: reads the masked case back through `GET /api/recovery/case/v1/cases/{caseId}` as a SIT test user of RW-TRIBE, with the authorise call of rwb-access in between, and reads the customer and the account of that case on rwb-source-data.
11. Harness: asserts that the same person token observed on the case read is the one on the customer read and the account read, that no service read touched another service's tables, and that no `is_personal` value in any schema is clear.
12. Harness: repeats the load of extract "PII-SIT-20261120" and asserts the skip with the earlier load named, starts a second load while the first runs and asserts the refusal with MSG-P2-006, and confirms the DEV guard before reading any file.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A personal column holds a value that looks personal in any of the 19 schemas | Load refused in full; the previous copy stays in every schema; the report names the schema, the table and the column | MSG-P1-002 | AC2 |
| X2 | Row count differs from the manifest in one schema | Load refused in full; the previous copy stays in every schema; the report names the schema and the check | MSG-P1-002 | AC3 |
| X3 | The target environment is DEV or PROD | Load refused before reading any file | MSG-P1-002 | AC5 |
| X4 | The same extract ID is loaded again | Load skipped; the report shows the earlier load from `tools.masked_copy_load` | None | AC1 |
| X5 | The manifest's masking rule version is not the version in force | Load refused in full | MSG-P1-002 | AC1 |
| X6 | A second load starts while one runs in the same environment | Second start refused by the per-environment lock | MSG-P2-006 | AC1 |
| X7 | A table maps to no owning schema, or to two schemas | Preflight stops the run; no schema is loaded and no swap happens | None | AC3 |
| X8 | A reader without the case right calls the masked case | rwb-access refuses the authorise call and the read answers 403 | MSG-P4-002 | AC5 |
| X9 | A service tries to read another service's tables | The database refuses the statement, and the boundary test of RWB-P1-E1069-APP fails the build | None | AC4 |

X1 to X6 are the exception paths of the legacy story carried onto the 19 schemas; X7 and X9 are the schema-per-service paths the monolith did not have (DP-01); X8 is the reader path of DP-08 in testable form.

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the loader module, the 19 schemas, the extract and the four contracts, and it owns no schema and no service code |
| Negotiable | Fixture size, wait intervals, report layout and check order are configuration; the masking rule version, the extract ID, the business date, the counts and the message IDs are fixed by the legacy story |
| Valuable | Proves across 19 schemas and four contracts what no single service story can prove: every table in its owner's schema, every personal column verified, one swap, all-or-nothing failure, no cross-schema read |
| Estimable | One test project, five test classes, three fixtures, one fault step, one repeat and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a row per schema, a run row in `tools.masked_copy_load`, a refusal, a response and a boundary-test result |

##### 7. Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT, proven across the 19 per-service schemas

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with row counts per product
    Given the 19 per-service schemas of the ACE database exist with one login each

  Scenario: AC1 One run fills every table into its owner's schema and swaps once per environment (new, D-RCV-60)
    Given the loader maps each manifest table to its owning schema from the Ownership Map and the per-service DB stories
    When the masked copy is loaded into SIT
    Then recovery_case, case_account and case_party land in rwb_case, interaction, party_ext, contact_point_ext, account_ext and valuation_ext land in rwb_source_data, document_field lands in rwb_document, and every other table lands in the schema of its owner
    Then the count per table and per product equals the manifest: case_account 28,119 against Mortgage 12,256, Hire purchase 12,960 and SSME 2,903
    Then no table is written into a schema whose login has no grant on it, and the loads of the 19 schemas are held in staging until every schema has passed
    Then the staging schemas are swapped for the live schemas in one step and the run is recorded in tools.masked_copy_load with extract ID, environment, business date, masking rule version and rows per table per schema
    When extract "PII-SIT-20261120" is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20 from tools.masked_copy_load
    When a second load into SIT starts while one runs
    Then the system refuses the second start with MSG-P2-006 and the first load is unaffected

  Scenario: AC2 Every is_personal column in every schema is verified before the swap (new, D-RCV-60)
    Given interaction row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in summary
    When the copy is verified before the swap in SIT
    Then the verifier scans every column tagged is_personal in all 19 staging schemas, including sys_fields.is_personal as the tag source
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in interaction.summary"
    Then the report names the schema rwb_source_data, the table interaction, the column summary and the row 4,512
    Then the previous SIT copy stays in use in every one of the 19 schemas and no schema is swapped

  Scenario: AC3 A failure in any one schema refuses the load in all 19 schemas (new, D-RCV-60)
    Given the case_account file holds 28,118 rows while the manifest lists 28,119
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals case_account 28,118 against 28,119"
    Then the report names the schema rwb_case and the check, and no other schema reports success
    Then the previous SIT copy stays in use in every one of the 19 schemas, including the 18 schemas whose own files passed
    When the load is retried with the corrected file
    Then the whole load runs again from the preflight and no staging schema of the refused run is reused

  Scenario: AC4 The same token joins through the contracts, never through a cross-schema join (new, D-RCV-60)
    Given the masked copy is loaded in UAT
    When a test user reads the case through GET /api/recovery/case/v1/cases/{caseId}
    Then the case read returns the case with its parties and accounts, and each person reference is a token, not a clear value
    When the same test user reads the customer through GET /api/recovery/source-data/v1/customers/{id} with the person reference of that case
    And reads the account through GET /api/recovery/source-data/v1/accounts/{id} with the account reference of that case
    Then the token returned on the case read is the token returned on the customer read and on the account read
    Then every read is one hop to the owning service and no service read another service's tables
    Then the boundary test of RWB-P1-E1069-APP passes, and a query that joins rwb_case to rwb_source_data is refused by the database and by the build

  Scenario: AC5 SIT and UAT only, and the mask holds on the reader path (new, D-RCV-60)
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file and writes no schema
    Given the masked copy is loaded in UAT and masking rule version "MASK-2026.11" is in force
    When a test user of RW-TRIBE reads a masked case through the gateway-bff composite route to GET /api/recovery/case/v1/cases/{caseId}
    Then rwb-access answers the authorise call and the masking policy of rwb-access masks every is_personal field of the response
    Then no national ID number, Thai mobile number or email address is present in the response, and the freshness read of GET /api/recovery/source-data/v1/data-products/freshness names the business date 2026-11-19
    When test user "U-6104" holds a role without the case right and calls the same path
    Then rwb-access refuses and the answer is 403 with MSG-P4-002
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only | NFR-045; CTL-11 |
| BR2 | Every field tagged personal is masked or tokenized under the masking rules in force | Masking rules reference table; DL26; `sys_fields.is_personal` |
| BR3 | A copy with any personal value left in it is refused in full | CTL-11; DQ check "Refuse the load" |
| BR4 | Dates and keys are not masked; counts equal the manifest | CTL-02; REC-01, REC-02 |
| BR5 | The same customer gets the same token in every table and every schema, so the contracts return one token | Mapping rule "Personal data" (s2t.txt); RWB-TE-004 BR5 |
| BR6 | With no masking rule loaded, every personal field is replaced by a token | DL26 ("every personal field stays masked") |
| BR7 | One schema and one login per service; a table is written only into its owner's schema, and no service reads another service's tables, views or foreign keys | Arch v5 slides 29 and 41; ADR-014; DP-01 |
| BR8 | The loader is a tool outside the ACE services, runs only in SIT and UAT, loads into staging and swaps in one step, and records the run in its own `tools.masked_copy_load` table | RWB-TE-004 section 13; DP-01 |
| BR9 | A failure in any one of the 19 schemas refuses the whole load and leaves the previous copy in every schema | This story; ASM-0548 |
| BR10 | A reader sees the masked case through the owner's contract with the masking policy of rwb-access applied; no service applies the mask by reading another service's masking table | DP-08; Arch v5 slides 14 and 41 |

##### 9. State transitions

None for a case status. This story changes no case status; it changes the state of the masked copy load in the pipeline.

| Item | States |
|---|---|
| Load run | Not started, preflight, running, verifying, swapped, refused, skipped |
| Schema in the run | Staging, verified, swapped; on any failure, discarded and the previous live schema untouched |
| Masked copy of an environment | Previous copy in use, new copy in staging, new copy in use; never a mixed estate |
| `tools.masked_copy_load` row | Written once per run: Loaded, Refused or Skipped, with the check results |
| Extract ID | Unseen, loaded, or already loaded (a repeat is skipped) |
| Boundary test | Pass (no cross-schema reference), or fail with the offending reference named |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| QA integration engineer | Owns the harness, the fixtures, the fault step and the run report |
| Platform administrator (RW-PLATADM) | Starts the load in SIT or UAT; owns the intake containers and the environment lock |
| Compliance and PDPA officer (RW-COMPLY) | Owns the masking rules and their version (DL26) and receives a refused-load report |
| Tribe lead and squad members (RW-TRIBE) | Run SIT and UAT tests on the masked copy with their test users' rights |
| Data load identity (SY-DATALOAD) | The identity the loader runs under in SIT and UAT; grants on the staging schemas of the run only |
| Service teams (P1, P3, P4 and each per-service DB story) | Own their schema, their grants, their contract and the tables the loader fills |
| ACE database administrator | Owns the 19 schemas, the 19 logins and the staging schemas of each environment |
| No role | May read another service's tables, run a copy in DEV or PROD, or swap one schema on its own |

The fault step of AC2 and AC3 runs on a test extract in SIT only; it injects a value into the extract file before the load and never writes to a service schema directly.

##### 11. Data

| BR Field ID | Entity | Schema (owner) | Field | Read or write |
|---|---|---|---|---|
| DF-CAS-001 to DF-CAS-023 | `recovery_case` | `rwb_case` (P3) | all fields | Write (staging), read |
| DF-CAS-024 to DF-CAS-029 | `case_account` | `rwb_case` (P3) | all fields | Write (staging), read |
| DF-CAS-030 to DF-CAS-035 | `case_party` | `rwb_case` (P3) | all fields | Write (staging), read |
| DF-INT-001 to DF-INT-013 | `interaction` | `rwb_source_data` (P1) | all fields | Write (staging), read |
| DF-DOC-012 to DF-DOC-017 | `document_field` | `rwb_document` (P5) | all fields | Write (staging), read |
| DF-EXT-001 to DF-EXT-012 | `party_ext` | `rwb_source_data` (P1) | all fields | Write (staging), read |
| DF-EXT-013 to DF-EXT-026 | `contact_point_ext` | `rwb_source_data` (P1) | all fields | Write (staging), read |
| DF-REF-105 | `sys_fields` | `rwb_source_data` (P1) | `is_personal` | Read |
| DF-REF-101 to DF-REF-104 | `reference_row`, `reference_version` | `rwb_case` (P3) | list code, value, version | Read (through the contract) |
| Not stated in RWB-TE-004 | `masking_rule` | `rwb_access` (P4) | rule version in force | Read (through the contract) |
| None | `tool_run` in schema `tools` | the loader (outside the 19 services) | extract ID, environment, business date, masking rule version, result | Write, read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-004; `account_ext` and `valuation_ext` are P1's four extension tables and load the same way (DP-05), and the field IDs of the extract's remaining tables are the table's own dictionary entries.

The per-schema table list the loader must fill is Not specified in the source documents (GAP-0379; ASM-0547). The manifest is per table and not per owning service, no source maps the tables of the extract to the 19 schemas, and the PII service's extract contract is outside the source set. Under ASM-0547 the loader builds the table-to-schema map from the Ownership Map and the per-service DB stories, and every table of the extract resolves to exactly one schema.

The harness owns no schema and no table of a service. It writes tables only through the loader in SIT and UAT staging schemas, reads them back through the four contracts of section 12.2, and records its own run in `tools.masked_copy_load`.

##### 12. Contract

###### 12.1 REST operations provided

None. The harness is a test project and the loader a tool outside the ACE services; neither provides a REST operation, and the names reserved for P2 rwb-integration — `/api/recovery/integration/v1`, the topic `rwb.integration.events.v1`, the queue `rwb-integration` and the schema `rwb_integration` — are not used by this story.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | The masked case read of a SIT or UAT test user: parties, accounts and tokens |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The case right and the masking policy check of the reader, and the refusal of a role without the right |
| GET | `/api/recovery/source-data/v1/customers/{id}` | P1 rwb-source-data | The customer reference of the case, with the token |
| GET | `/api/recovery/source-data/v1/accounts/{id}` | P1 rwb-source-data | The account reference of the case, with the owner token |
| GET | `/api/recovery/source-data/v1/data-products/freshness` | P1 rwb-source-data | The freshness of the loaded copy, business date 2026-11-19 |
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | The environment lists, the product groups and the masking reference rows (DP-07) |

Every call is one hop to the owning service on its own base with the 2 s client budget (DP-11, DP-13); the harness calls no service through another service. The reader reaches the case through the gateway-bff composite route (DP-19).

The table-to-schema map and the PII extract contract are Not specified in the source documents (GAP-0379; ASM-0547); the map is held as configuration of the loader (ASM-0547) and no operation of the PII service is called by this story.

###### 12.3 Events published

None. The loader is a tool outside the services and publishes no business event; the run is recorded in `tools.masked_copy_load`, and no event is produced for a load, a swap or a refusal.

###### 12.4 Events consumed

None. The harness waits on no topic: the load is synchronous in the pipeline, its result is the `tools.masked_copy_load` row, and the reader assertions are made against the contracts of 12.2. The case and source-data events that other stories assert are out of scope here.

###### 12.5 Workflows and activities

None. No Temporal workflow, activity or Nexus operation is started or awaited: the loader is a batch tool of the pipeline and not a service worker, and the two service task queues it would otherwise use — `rwb-case` and `rwb-source-data` — are exercised only through their REST contracts.

###### 12.6 Schedules

None. The masked copy load is a manual pipeline stage started by the platform administrator for SIT or UAT and is not a scheduled job and not in the production job list (RWB-TE-004 section 12). It is not registered in `rwb-integration` and no Schedule is created or moved.

###### 12.7 Tables owned

None. The harness owns no table and no schema. The loader's own run table `tools.masked_copy_load` lives in schema `tools`, outside the 19 service schemas, and is P1's tool table (RWB-PLT-TE004-APP); `rwb_integration` is not written by this story.

###### 12.8 Contract fakes

None. This is the integration level: the real P3, P1 and P4 services, the real ACE schemas and the real extract replace the contract fakes of the app stories. The PII service is an outside system that supplies a file; it is not faked and not called over a service contract.

###### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6 | The case read, the authorise call, the customer and account reads, the freshness read and the reference-list read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | None | The loader publishes no event and the harness listens to no topic |
| Temporal | None | None | No workflow, no activity, no Schedule; `rwb-case` and `rwb-source-data` are called over REST only |
| File | None | 1 file set per environment | The masked extract files and their manifest from the PII service in the SIT or UAT intake container |

##### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/masked-copy`, with the five test classes `MultiSchemaLoadIT`, `PersonalColumnScanIT`, `AllOrNothingIT`, `TokenThroughContractsIT` and `EnvironmentAndReaderIT`, the extract fixtures, the fault step and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| SchemaMap | Configuration | The table-to-schema map from the Ownership Map and the per-service DB stories (ASM-0547) |
| LoadDriver | Service | Starts the loader for the environment and reads the `tools.masked_copy_load` row of the run |
| SchemaProbe | Service | Asserts the row counts, the keys and the grants of each of the 19 schemas against the manifest |
| PersonalColumnScan | Service | Injects the value of interaction row 4,512 into the test extract, runs the verifier and asserts the refusal and the untouched schemas |
| AllOrNothingProbe | Service | Cuts the case_account file to 28,118 rows, asserts the refusal in all 19 schemas and the retry from the preflight |
| TokenProbe | Service | Compares the token of the case read with the customer read and the account read, and asserts that no cross-schema query is possible |
| ReaderProbe | Service | Calls the case path as RW-TRIBE and as a role without the right, through the authorise call, and asserts the masking and MSG-P4-002 |
| ReportWriter | Service | One row per test case, with the schema, the table, the check and the evidence |

**Database.** None of its own. The loader writes the staging schemas of the run and `tools.masked_copy_load`; the harness writes nothing into a service schema and never reads one directly (DP-01).

**Configuration and reference data**

- The environment, the intake container, the 19 schema names and the loader module, all as configuration.
- The table-to-schema map (ASM-0547) and the manifest of extract "PII-SIT-20261120".
- The masking rule version "MASK-2026.11", read as reference data through the rwb-case contract (DP-07), with the authoritative rows in `masking_rule` (P4).
- The product groups Mortgage, Hire purchase and SSME and the environment lists, read through the same contract.
- The 2 s client budget, the per-environment lock and the report layout.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, `account_ext` | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C and X dependencies the DPs name stay with the service, platform and operations stories this harness proves; this story carries no H, C or X dependency and its I list names the three stories whose behaviour it exercises (Template and Rules §R5.4: I never blocks a build).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Masked extract SIT | Extract "PII-SIT-20261120", business date 2026-11-19, MASK-2026.11, 28,119 case accounts: Mortgage 12,256, Hire purchase 12,960, SSME 2,903 | AC1, AC3, TC-TE-004-01-ITG, TC-TE-004-03-ITG |
| Injected personal value | The same extract with a 13-digit value with a valid check digit in `interaction.summary` row 4,512 | AC2, TC-TE-004-02-ITG |
| Short case_account file | The same extract with 28,118 rows in the case_account file | AC3, TC-TE-004-03-ITG |
| Second copy of the extract | The same extract ID delivered twice, and a second start while one runs | AC1, TC-TE-004-05-ITG, TC-TE-004-07-ITG |
| Masking rule versions | Manifests with MASK-2026.11 and MASK-2026.10 | AC1, TC-TE-004-06-ITG |
| Role set | RW-TRIBE and a test role without the case right, test user "U-6104" | AC5, TC-TE-004-08-ITG |

**Run order.** Preflight; the DEV guard (AC5, first part); the SIT load of the full extract with the schema probes (AC1); the repeat and the second start (AC1); the injected value (AC2); the short file and the retry (AC3); the UAT load and the token reads through the three contracts (AC4); the reader checks as RW-TRIBE and as the role without the right (AC5); cleanup of the staging schemas of failed runs. A failing step stops the run and the report names the criterion, the schema, the check and the evidence.

**Done when.** The 13 test cases of section 16 pass, extract "PII-SIT-20261120" is loaded in SIT and in UAT with 28,119 case accounts and one `tools.masked_copy_load` row per environment, the verifier has scanned every `is_personal` column in all 19 schemas, a failure in one schema has refused the whole load with the previous copy intact in all 19, and the token of the case read matches the customer and account reads with no cross-schema query possible.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The masked copy is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P2-006 | A load starts while one runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | A test user without the right reads the copy | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-TE-004; the story adds no message text. Report lines of the harness are for developers and are not part of the message standard. Thai text for each message follows decision DL10.

##### 15. Screens and states

No screen in this story, and the harness renders nothing. The platform administrator and the squads read the load report in the pipeline, and a test user sees the masked copy through the normal SIT and UAT screens, which reach the case through the gateway-bff composite route and the case contract of rwb-case (DP-19). Personal fields appear as tokens or masked values on those screens, with the mask applied by rwb-access (DP-08). The states the harness observes are the load, schema and copy states of section 9.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-004-01-ITG | legacy AC1, BR2, BR4, BR5 | Integration | Masked extract PII-SIT-20261120 with 28,119 case accounts, loaded into the 19 schemas of SIT |
| TC-TE-004-02-ITG | legacy AC2, BR3 | Integration | Injected value with a valid check digit in interaction row 4,512 of the test extract |
| TC-TE-004-03-ITG | legacy AC3, BR4 | Integration | case_account file with 28,118 rows against the manifest's 28,119 |
| TC-TE-004-04-ITG | legacy AC4, BR1 | Integration | Target environment DEV, with the loader pointed at the SIT intake container |
| TC-TE-004-05-ITG | legacy AC5 | Integration | Extract PII-SIT-20261120 loaded into SIT twice |
| TC-TE-004-06-ITG | legacy AC6, BR6 | Integration | Manifest with MASK-2026.10 against MASK-2026.11 in force |
| TC-TE-004-07-ITG | legacy AC7 | Integration | Two loads into SIT at once, on the per-environment lock |
| TC-TE-004-08-ITG | legacy Access, BR10 | Integration | SIT test user "U-6104" with a role without the case right; 403 with MSG-P4-002 |
| TC-ITG-TE004-01 | AC1, BR4, BR7, BR8 | Integration | One run over the 19 schemas: table-to-schema map, manifest totals, one swap per environment and the tools.masked_copy_load row |
| TC-ITG-TE004-02 | AC2, BR2, BR3 | Integration | Every is_personal column in all 19 schemas scanned; interaction row 4,512 refused with MSG-P1-002 |
| TC-ITG-TE004-03 | AC3, BR3, BR9 | End to end | case_account at 28,118 rows; the whole load refused and the previous copy intact in all 19 schemas, then the retry |
| TC-ITG-TE004-04 | AC4, BR5, BR7 | Integration | Case, customer and account reads compared for one token; the boundary test and a refused cross-schema join |
| TC-ITG-TE004-05 | AC5, BR1, BR10 | End to end | DEV guard refused before any file; UAT reader masked through the gateway-bff route and the authorise call |

The legacy acceptance criteria of RWB-TE-004 are owned by RWB-PLT-TE004-APP, the app story of the same legacy key, and are re-exercised here end to end across the 19 schemas; the legacy test case IDs are kept as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC5 carry TC-ITG-TE004-01 to TC-ITG-TE004-05.

##### 17. Guardrails

- No business value in code: the masking rules and their version belong to Compliance, the allowed environments are properties, and the product groups and environment lists are reference data read through the rwb-case contract (DP-07).
- No personal data in logs, events, workflow inputs, fixtures or the report: the run record holds counts, totals, schema names and check names, never a value, and the test extracts are built from masked or synthetic data.
- Each table is written only into its owner's schema and no service reads another service's tables, views or foreign keys (DP-01); the boundary test is part of the run and a cross-schema reference fails it (RWB-P1-E1069-APP).
- The loader stays a tool outside the ACE services and never becomes a runtime dependency of a service; it runs only in SIT and UAT, and no copy is made from SIT or UAT to another environment.
- One swap per environment, and never a partial estate: a failure in any schema refuses the whole load and leaves the previous copy in every schema (BR9, ASM-0548).
- The verifier scans every `is_personal` column in every schema before the swap — not the two tables the legacy story named — so a new personal column in a new service is covered by construction (ASM-0548).
- The mask is applied by rwb-access on the reader path and is asserted on the contract response, never by reading `masking_rule` from a service schema (DP-08).
- The harness never uses production data and never points at a production namespace.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | The 19 schemas and logins, `tools.masked_copy_load`, the case read and the authorise call, the reference-list read | TC-TE-004-01-ITG, TC-TE-004-04-ITG, TC-ITG-TE004-01, TC-ITG-TE004-03, TC-ITG-TE004-05 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | `masking_rule` (P4) through the authorise call, the case read and the gateway-bff composite route, the customer and account reads | TC-TE-004-02-ITG, TC-TE-004-08-ITG, TC-ITG-TE004-02, TC-ITG-TE004-04, TC-ITG-TE004-05 |

##### 19. Out of scope

- The masked-copy loader, its manifest validator, its masking verifier and its load-report writer (RWB-PLT-TE004-APP); this story exercises them and owns none of them.
- The 19 schemas, the 19 logins and their grants (RWB-PLT-NF06-DB and the per-service DB stories).
- The ACE view contract, the extension tables and the boundary test (RWB-P1-E1069-APP); this story exercises the boundary rule and owns none of it.
- The `is_personal` tags and the synthetic-data patterns (RWB-P1-E1065-APP).
- The masking policy, the roles and the authorise decision (RWB-P4-E1037-APP); the case contract and its reference data (RWB-P3-CON stories); the customer, account and freshness contracts (RWB-P1-CON stories).
- The PII service, which the bank runs and which produces the extract and its manifest; its extract contract is outside the source set (GAP-0379) and no external dependency is carried for it.
- The masking rule values per field and per role (DL26, Compliance) and masking on the screens themselves (RWB-E1-037).
- Synthetic data in DEV (RWB-E1-065) and the masked debt sale data tape (FEAT-DBS-03, Epic 5).


## RWB-TE-006 Outbox and retry for outbound work

Legacy disposition: Split (rework).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE006-CON | Contract | RWB-PLT-LIB | CG-W0 | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-PLT-TE006-APP | App development | RWB-PLT-LIB | L-PLT-LIB-J | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-ITG-TE006-ITG | Integration | RWB-ITG-W1 | L-ITG-W1 | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE006-CON Outbox and retry for outbound work

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: contract slice split from RWB-TE-006 for the platform library RWB-PLT-LIB. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE006-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | CG-W0 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

##### 1. Story

As a **tech lead**, I want **the published contract of the outbox and inbox library — the `OutboxWriter`, `OutboxConsumer` and `IdempotencyGuard` interfaces with their exceptions, the DDL contract of the four library tables that every service creates in its own schema, the CloudEvents 1.0 envelope and the caseId key, the inbox dedupe rule, the retry and dead-letter contract with its alert rule, the versioning and compatibility rule, and the fakes — instead of the monolith's single `recovery` schema outbox and its in-process consumer interface**, so that **all 19 services build their events against one published contract from Day 1, no service hand-writes an outbox, inbox or idempotency table, and every consumer can be built and tested before the producer exists** (Template and Rules §R6, DP-09).

##### 2. Business rationale

In the monolith the outbox was two tables in the one `recovery` schema and the consumer was a Java interface implemented in the same process (legacy section 12). Under Arch v5 each of the 19 services writes its own schema and its own Flyway sequence, publishes to its own topic and consumes through its own consumer group (Arch v5 slides 11, 20, 22, 29). The library therefore becomes a contract before it becomes code: the three interfaces fix the transaction boundary and the failure shape, the DDL contract fixes the four table shapes each service applies in its own schema, and the envelope and dedupe rules fix what travels on the wire.

This contract is the DP-09 dependency of every service CON and APP story. Publishing it on Day 1 lets a service build its outbox row, its inbox and its consumer against a frozen interface and a fake, while the producer of the event it consumes may still be two waves away. It also carries the two rules that keep the split honest: the library joins the caller's transaction and never opens its own, and it raises no case event, no task and no decision record on another service's behalf.

The retry contract is the Kafka retry-topic ladder of 1 min, 10 min and 1 h and then the dead-letter topic with an alert and a replay tool (Arch v5 slides 11 and 22). The legacy 3 retries at 1, 5 and 15 minutes is the lower-ranked source and is kept only in the preserved criteria of the APP story and exercised through configuration; the conflict is recorded in GAP-1416 with its assumptions.

It supports REQ-DRI-007 and the two non-functional targets of the legacy story: no event is lost, and every delivery is retried on a defined schedule and ends in an exception path with an owner.

##### 3. Preconditions

- The platform library has an artifact name, a version scheme and a publication channel in the service template; the channel itself is Not specified in the source documents (GAP-1416; ASM-2475).
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions, so the DDL contract is applied by each service's own sequence in its own schema (DP-15).
- RWB-PLT-E1027-CON is published: the local decision-record library and topic `rwb.decision-record.v1`, which the contract refers to and does not duplicate (DP-03).
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters and reference-data clients that carry the recipient list and the retry windows (DP-06, DP-07).
- The Kafka platform of RWB-PLT-EVT provides one event topic per service, its three retry topics and its dead-letter topic, and the schema registry in BACKWARD mode; the contract refers to those names and does not provision them.
- The Ownership Map ruling stands: the four tables are owned by PLT and created in each service's own schema, not once in an rwb-integration schema. The per-service table list that a DB story applies is Not specified in the source documents (GAP-1416; ASM-2475).
- No build dependency: the contract is Day 1 by rule (Template and Rules §R5.7).

##### 4. Flow

1. Fix the three interfaces: `OutboxWriter.publish`, `OutboxConsumer.consume` and `IdempotencyGuard.firstTime`, with their input and output types and their exceptions.
2. Fix the transaction rule in the interface documentation: a call joins the caller's transaction, opens none, and throws before any write when the key exists.
3. Fix the DDL contract of the four tables, with the keys, the checks, the indexes and the standard columns, as one template that each service applies in its own schema.
4. Fix the envelope: CloudEvents 1.0 in binary mode, `ce_specversion` 1.0, `ce_id`, `ce_type` as the event name with its schema version, `ce_source` as the owning service, `ce_subject`, `ce_time`, the W3C trace header and the caseId record key.
5. Fix the inbox rule: the consumer records `ce_id` with its consumer group in `processed_event` in the same transaction as its own change, and a repeated `ce_id` has no second effect.
6. Fix the retry and dead-letter contract: the three retry windows, the dead-letter topic, exactly one alert per dead-letter record, the replay tool as the recovery path and the rule that the library raises no case event, no task and no decision record.
7. Fix the versioning rule: major version 1 of the interfaces and the envelope, backward-compatible event schemas in the registry, and a breaking change as a new major version and a new `ce_type`.
8. Publish the fake of the three interfaces and the fixture set, and wire the contract tests into the build of every service that depends on the library.
9. Publish the contract document with the nine tables of section 12 and hand it to every service CON story as the DP-09 dependency.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A service implements the writer outside its own transaction | The contract test fails and the build is refused; no partial publish is accepted | None | AC1 |
| X2 | A service creates the tables in another service's schema | The boundary test fails on the cross-schema reference and the build is refused | None | AC2 |
| X3 | An event body does not validate against the registry | The relay refuses to publish and the delivery keeps its state with the error code | None | AC3 |
| X4 | The same `ce_id` is delivered twice | The inbox drops the second delivery and the consumer answers OK | None | AC4 |
| X5 | A record fails the third retry | The record goes to the dead-letter topic and one alert is raised; the replay tool is the recovery path | None | AC5 |
| X6 | A schema change breaks a consumer | The registry refuses the change in BACKWARD mode and a new major version and `ce_type` are required | None | AC6 |
| X7 | A service hand-writes an outbox table instead of applying the template | The drift check against the DDL contract fails and the build is refused | None | AC2, AC6 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; the contract refers to the platform, the case and the decision contracts by name only |
| Negotiable | The artifact channel and the fixture set are agreed with the platform team; the interfaces, the table shapes, the envelope and the retry windows are fixed by the target architecture |
| Valuable | Unblocks every service CON and APP story that publishes or consumes an event, from Day 1 |
| Estimable | Three interfaces, one DDL template, one envelope rule, one dedupe rule, one retry contract and the fakes |
| Small | Fits two weeks with its contract tests |
| Testable | Every criterion below is a contract test that the build of a consuming service runs |

##### 7. Acceptance criteria

```gherkin
Feature: Outbox and inbox library contract

  Background:
    Given the platform library contract document is published with major version 1
    Given the 19 services have one schema and one login each

  Scenario: AC1 The three interfaces are published and stable (new, D-RCV-60)
    Given the contract jar of the platform library is published
    When a service compiles against it
    Then OutboxWriter.publish(OutboxEvent event) returns a UUID and joins the caller's transaction
    Then OutboxEvent carries eventType, schemaVersion, caseId, payload, actorRef and idempotencyKey
    Then publish throws DuplicateOutboxKeyException when the idempotency key already exists
    Then OutboxConsumer.consume(EventHeader header, JsonNode payload) returns OK or FAILED with a code
    Then IdempotencyGuard.firstTime(String consumer, String idempotencyKey) returns a boolean
    Then no method opens its own transaction and no method calls another service

  Scenario: AC2 The DDL contract creates four tables in each service schema (new, D-RCV-60)
    Given the DDL template of the library
    When a service applies it through its own Flyway sequence
    Then it creates outbox_event, outbox_delivery, processed_event and idempotency_key in that service's own schema
    Then outbox_event carries the unique key on idempotency_key and the unique key on (case_id, case_seq)
    Then outbox_delivery carries the unique key on (event_id, consumer), the status check on PENDING, RETRYING, DELIVERED and EXCEPTION and the due index on next_attempt_at
    Then processed_event carries the unique key on ce_id and the consumer group
    Then idempotency_key carries the unique key on scope and key with the stored response
    Then no table names another service's schema and no key crosses a schema boundary

  Scenario: AC3 The envelope and the record key are fixed (new, D-RCV-60)
    Given a record the relay is about to publish
    When it is published to the owning service's topic rwb.<short>.events.v1
    Then the CloudEvents 1.0 binary-mode headers ce_specversion 1.0, ce_id, ce_type, ce_source, ce_subject and ce_time are set
    Then ce_type is the event name rwb.<short>.<Event>.v1
    Then ce_source is the owning service
    Then the record key is caseId and the traceparent header carries the W3C trace context
    Then the body is validated against the registry before publish and carries IDs and facts only
    Then the producer is idempotent with acks=all and the schema compatibility is BACKWARD

  Scenario: AC4 The inbox dedupe and the idempotency rule are fixed (new, D-RCV-60)
    Given a consumer that subscribes to an event of another service
    When the same ce_id arrives twice
    Then the consumer records it in processed_event in the same transaction as its own change
    Then the second delivery has no second effect and answers OK
    When a caller publishes with an idempotency key that already exists
    Then one event exists and the second call throws DuplicateOutboxKeyException

  Scenario: AC5 The retry and dead-letter contract is fixed (new, D-RCV-60)
    Given a consumer that fails
    When the first, the second and the third attempt fail
    Then the record moves through the retry topics at 1 min, 10 min and 1 h
    Then after the third retry the record goes to the dead-letter topic and exactly one alert is raised to the platform administrator
    Then the replay tool is the recovery path of a dead-letter record
    Then the library raises no case event, no task and no decision record of its own

  Scenario: AC6 Versioning, compatibility and the fake (new, D-RCV-60)
    Given the contract declares major version 1 of the interfaces and the envelope
    When an event schema changes
    Then a backward-compatible change is accepted by the registry and the ce_type version stays the same
    Then a breaking change needs a new major version and a new ce_type
    Then the library fake answers OutboxWriter, OutboxConsumer and IdempotencyGuard for the contract test of every service
    Then the contract test of each consuming service runs against the published jar and fails on any drift from section 12
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The outbox row and its deliveries are written in the caller's transaction and the caller's schema: no event without the change and no change without the event | events.txt Rules, Transactions; DP-01; DP-09 |
| BR2 | The event carries a CloudEvents id and an idempotency key unique in the caller's outbox; a consumer drops a repeat through its inbox `processed_event` or `IdempotencyGuard` | events.txt Rules, Duplicates; R-UNI-40; Arch v5 slides 11 and 22 |
| BR3 | Delivery is at least once; each recipient has its own consumer group and its own delivery state | events.txt Rules, Delivery; Arch v5 slide 21 |
| BR4 | Events for one case reach each recipient in the order they were written, through the caseId record key | events.txt Rules, Ordering; Arch v5 slide 21 |
| BR5 | A failed record climbs the retry topics at 1 min, 10 min and 1 h and then goes to the dead-letter topic with one alert and the replay tool | Arch v5 slides 11 and 22; NFR-026; REQ-DRI-007 |
| BR6 | The library raises no case event, no task and no decision record; the consumer's owning service does that through its own contract | R-UNI-33; R-UNI-35; R-UNI-36; GAP-1416 |
| BR7 | Payloads hold references and codes and never personal data; the event carries its schema version and the envelope its trace context | events.txt Rules, Payload and Versioning |
| BR8 | A contract change is backward compatible in the registry, and a breaking change is a new major version with a migration note | Arch v5 slide 11 |
| BR9 | The recipient list, the owners and the retry windows are configuration behind the published interfaces, never values in the library code | Principle 1; DL11 |

##### 9. State transitions

The contract fixes the delivery states and their legal moves; no case status is held by the library.

| From | Event | Condition | To |
|---|---|---|---|
| Contract version 1 | A backward-compatible change | The registry accepts the schema and the envelope is unchanged | Contract version 1, new schema minor version |
| Contract version 1 | A breaking change | An interface, a table shape or an envelope attribute changes | Contract version 2 with a migration note |
| Delivery PENDING | Publish acknowledged | None | Delivery DELIVERED |
| Delivery PENDING | Recipient or broker fails | Retries left | Delivery RETRYING in the retry topic of the window |
| Delivery RETRYING | Recipient fails | No retries left | Record in the dead-letter topic |
| Event in the dead-letter topic | Replay through the replay tool | None | Delivered again under the same `ce_id`, dropped where already processed |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform library team, owning the template | Owns the interfaces, the DDL template, the envelope rule and the fakes; publishes version 1 and later versions |
| The owning service of each consumer | Implements `OutboxConsumer` and `IdempotencyGuard` under its own consumer name and raises its own case events, task and decision record |
| Platform team | Owns the retry-topic and dead-letter settings, the alert and the replay tool that the contract refers to |
| ACE data team | Owns the per-service schema, login and grants that the DDL contract assumes |
| No approval level from the delegation of authority applies | The contract takes no business decision |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-189 to DF-OPS-197 | outbox_event | all fields, fixed by the DDL contract | Write, in the caller's schema |
| DF-OPS-198 to DF-OPS-206 | outbox_delivery | all fields, fixed by the DDL contract | Write, in the caller's schema |
| DF-DEC-001 to DF-DEC-018 | decision_record (local library) | all fields | Not held by this contract; written by the owning service |
| DF-CAS-001 | recovery_case | id | Read only as the envelope subject and the record key, through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary. `processed_event` and `idempotency_key` have no field ID of their own in the source; they are library objects owned by PLT and created in each service's schema. The `outbox_event` and `outbox_delivery` columns are fixed by DF-OPS-189 to DF-OPS-206; the column set of `processed_event` and `idempotency_key` is Not specified in the source documents and is published as the working read (GAP-1416; ASM-2475).

##### 12. Contract

###### 12.1 REST operations provided

None — the library has no REST surface. The admin read and resend operations belong to P2 rwb-integration in the Ownership Map.

###### 12.2 REST operations consumed

None — the library joins the caller's transaction and calls no service.

###### 12.3 Events published

None of its own — the contract fixes the envelope and the key for the records that the caller's schema relays to `rwb.<short>.events.v1`; the library publishes no event type of its own.

###### 12.4 Events consumed

None of its own — the contract fixes the inbox rule for the events each service subscribes to under its own consumer group in its own `processed_event` table.

###### 12.5 Workflows and activities

None — the contract defines no workflow and no activity; the relay is a background worker in each service (plain code, no Temporal Schedule).

###### 12.6 Schedules

None — the contract states that the legacy Quartz JOB-11 sender becomes a continuous per-service outbox relay and not a Temporal Schedule (GAP-1416; ASM-2476).

###### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| outbox_event | PLT | Contract shape of the published fact; unique key on `idempotency_key` and on `(case_id, case_seq)` |
| outbox_delivery | PLT | Contract shape of one event and recipient; unique key on `(event_id, consumer)`, status check and due index |
| processed_event | PLT | Contract shape of the inbox; unique key on `ce_id` and the consumer group |
| idempotency_key | PLT | Contract shape of the stored response per scope and key |

Each service applies the same template in its own schema under its own login, through its own Flyway sequence; the library does not create a schema, a login or a table in another service's schema (DP-01, DP-15). The `outbox_event` and `outbox_delivery` shapes carry DF-OPS-189 to DF-OPS-206; the column set of `processed_event` and `idempotency_key` is the working read of this contract, because no source defines it (GAP-1416; ASM-2475).

###### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Library interface fake | `OutboxWriter`, `OutboxConsumer`, `IdempotencyGuard` | A writer that records the call and throws `DuplicateOutboxKeyException` on a repeated key; a consumer that answers OK or FAILED on demand; a guard that answers first time or not |
| Registry fake | The schema registry | BACKWARD mode with one accept and one refusal fixture |
| Kafka retry and dead-letter fake | The three retry topics and the dead-letter topic | A record that fails three times and lands in the dead-letter topic with one alert |
| rwb-case case-event and task fake | The P3 contract | Task code RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM; RETRY_LIMIT_REACHED and RETRY_SUCCEEDED accepted |

###### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed | The contract adds no path and calls no service |
| Kafka | None published and none consumed by the library itself | The contract fixes the envelope, the caseId key, the three retry topics and the dead-letter topic for the records each service relays |
| Temporal | None | No workflow, no activity and no Schedule |
| File | None | No file is read or written; an outbound file is a claim-check call through the rwb-integration contract |

##### 13. Solution plan

**Package.** Shared library contract artifact of the platform, the three interfaces in `th.co.scb.ace.workbench.recovery.platform.api`, the DDL template as a resource, the envelope and dedupe rules in the contract document; the implementation is the APP story of this legacy key.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The contract fixes that each service applies the four tables in its own schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the contract hands the record to the owning service and does not write it | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the recipient list and the retry windows are parameters behind the interface | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the recipient and event-type lists are reference rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. This story is the contract of that library | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the legacy Quartz JOB-11 sender becomes a continuous per-service outbox relay, not a Temporal Schedule | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the recipient is reached through its published contract or its topic, never in process | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the contract states that the library adds no path and the admin path belongs to P2 | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the DDL contract is applied by each service's own sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route; the admin screen is out of scope | H RWB-PLT-N001-CON |

**Hardware and software change.** The contract moves the outbox, inbox and idempotency tables from one set in the monolith's `recovery` schema to a library template that every service applies in its own schema; it fixes the publish path as each owner's topic with CloudEvents 1.0 and an idempotent producer; it fixes retry as the Kafka retry-topic ladder and the dead-letter topic with an alert and a replay tool; and it fixes that the case-step and decision-record effects stay in the owning service's code through its contracts. No new hardware is implied: the relay runs in each service's own pods on the existing AKS cluster and the tables sit in the existing ACE PostgreSQL server.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `OutboxWriter` | Published interface | One method with its `OutboxEvent` input and its `DuplicateOutboxKeyException`; joins the caller's transaction |
| `OutboxConsumer` | Published interface | One method with the `EventHeader` and the payload, returning `ConsumeResult` OK or FAILED with a code |
| `IdempotencyGuard` | Published interface | One method answering whether a consumer has already acted on a key |
| OutboxDdlTemplate | Resource | The DDL contract of the four tables, keys, checks and indexes |
| EnvelopeSpecification | Document | The CloudEvents 1.0 binary-mode attribute set, the caseId key, the trace header and the `ce_type` shape |
| InboxSpecification | Document | The dedupe rule against `processed_event` in the consumer's own transaction |
| RetrySpecification | Document | The three retry windows, the dead-letter topic, the one-alert rule and the replay path |
| Library fake and fixtures | Test asset | The three interfaces and the fixture set used by every consuming service |

**Build steps**

1. Write the three interfaces and the exception types; run the compile and drift test of a sample service (AC1).
2. Write the DDL template and apply it twice, in two throwaway schemas, to prove the reusability and the absence of cross-schema references (AC2).
3. Write the envelope specification and the registry check; test the headers, the key and one accepted and one refused schema (AC3).
4. Write the inbox specification and the idempotency rule; test a repeated `ce_id` and a repeated key (AC4).
5. Write the retry and dead-letter specification with the one-alert rule and the replay path; test the three windows and the dead-letter landing (AC5).
6. Publish the fake and wire the contract test into the build of the dependent services; test the drift refusal (AC6).
7. Publish the contract document with the tables of section 12 and record the version and the compatibility rule.

**Done when.** The six criteria pass as contract tests, the tables of section 12 are complete and name their owner from the Ownership Map, and the APP story of this legacy key builds against the published jar.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-GEN-005 | A delivery is queued to send again through the P2 admin API | Saved. |
| MSG-P2-022 | Resending a delivery that is not in EXCEPTION, through the P2 admin API | Only an item in the exception queue can be sent again. |
| MSG-P7-003 | The owning service cannot write its decision record at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the Platform administration right calls the P2 admin API | You cannot {action} here. Your role does not include it. |

The library itself raises no user-facing message; these are the messages of the operations that the contract refers to, unchanged from the legacy story. Thai text for each message follows decision DL10.

##### 15. Screens and states

No screen of its own. The contract has no user interface: the admin read and resend screen and SCR-44 Interface and job monitor belong to P2 and Epic 2, and the library adds no route and no state to any screen (DP-19).

##### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE006-CON-01 | AC1 | Contract | A sample service compiles against the jar; a writer in its own transaction and a writer that opens its own transaction |
| TC-PLT-TE006-CON-02 | AC2 | Component | The template applied in two throwaway schemas; the unique keys, the status check and the due index asserted |
| TC-PLT-TE006-CON-03 | AC3, AC5 | Contract | One record published with the full CloudEvents header set, one schema accepted and one refused, three failed attempts and a dead-letter landing with one alert |
| TC-PLT-TE006-CON-04 | AC4 | Component | The same `ce_id` twice and the same idempotency key twice |
| TC-PLT-TE006-CON-05 | AC6 | Contract | A backward-compatible change accepted, a breaking change refused, and the drift test against the published jar |

##### 17. Guardrails

- No business value in the contract: the recipient list, the owners and the retry windows are configuration behind the interfaces.
- No personal data in the envelope, in a fixture or in a log; the body carries references and codes only.
- No cross-schema reference in the DDL template and no foreign key across services; the boundary test fails the build.
- The contract states that the library raises no case event, no task and no decision record of its own.
- A published version is never edited in place; a breaking change is a new major version with a migration note.

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Business Requirements Program, section 5.2 and section 6.4 | None | All recovery processes | R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40 | TC-PLT-TE006-CON-01 to TC-PLT-TE006-CON-05 |

##### 19. Out of scope

- The implementation of the writer, the consumer, the relay and the DDL template: the APP story of this legacy key.
- The Kafka topics, the retry topics, the dead-letter topic and the registry themselves: RWB-PLT-EVT.
- The admin read and resend API and its screen: P2 rwb-integration, SCR-44 and Epic 2.
- The decision-record library and the central ledger: RWB-PLT-E1027-CON and RWB-P7-E1027-CON.
- The per-service schema, login and grants: RWB-PLT-DB.
- The retry values as a business decision: DL11, and the conflict recorded in GAP-1416.


### RWB-PLT-TE006-APP Outbox and retry for outbound work

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-006 for the platform library RWB-PLT-LIB. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE006-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-LIB |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-PLT-LIB-J |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-TE006-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON, RWB-P2-E1007-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

##### 1. Story

As a **platform library engineer**, I want **the outbox, inbox and idempotency library that all 19 services use from the service template — an `OutboxWriter` that writes the event and one delivery row per listed recipient in the caller's own transaction, inside the caller's `rwb_<short>` schema under the caller's own login, an `OutboxConsumer` with an inbox that drops a repeated delivery, a continuous per-service outbox relay that publishes to the owning service's Kafka topic with the CloudEvents 1.0 envelope and an idempotent producer, and a retry path carried by the Kafka retry topics and the dead-letter topic with an alert and a replay tool — instead of the monolith's single `recovery` schema tables, its shared Quartz sender JOB-11 and its in-process consumer call**, so that **no outbound fact is lost when a service, Kafka or a recipient is down, nothing is sent for a change that did not commit, and every service's outbox, inbox and idempotency rows live in its own schema with its own owner** (Template and Rules §R6, DP-09, DP-01).

##### 2. Business rationale

The Workbench modules talk to each other through application events, and outbound work such as a notice for WIN starts from an event in the module that approved it. In the monolith one outbox table sat in the single `recovery` schema, one clustered Quartz job, JOB-11, delivered the rows to consumers and one decision log writer recorded the move to the exception queue. Under Arch v5 the same guarantee has to hold when there are 19 services, 19 schemas and 19 logins: the outbox row must be written in the same transaction and in the same schema as the change it describes, because a service may not read or write another service's tables (DP-01), and the delivery has to cross a Kafka topic instead of an in-process call (DP-09, DP-11).

This story is that library, and it is the DP-09 dependency of every service CON and APP story in waves 1 to 4. It keeps the four properties the legacy story measured — written with the change, delivered at least once, ordered per case and per recipient, retried on a defined schedule and moved to an exception path with a task for a named owner (REQ-DRI-007) — and it adds the four that only a microservice shape needs: the event leaves through the owner's own topic with a CloudEvents 1.0 envelope and an idempotent producer; each consumer deduplicates through an inbox table in its own schema; a failed delivery climbs the Kafka retry-topic ladder and ends in the dead-letter topic with an alert and a replay tool; and the case-step events and the decision record stay in the code of the service that owns the case step, reached through its published contract, because the library may not raise a case event or write a decision record on another service's behalf.

The retry schedule is the one point where the two sources disagree. The legacy story holds the retry settings as configuration with 3 retries at 1, 5 and 15 minutes; Arch v5 slide 22 and slide 11 fix the Kafka retry topics at 1 min, 10 min and 1 h and then the dead-letter topic. §R3 R-PREC puts the Arch v5 catalogue slides first, so the Kafka ladder wins and the legacy values are kept only in the preserved criteria text and exercised through the configuration of section 13; the conflict is recorded in GAP-1415 with its assumptions.

The measure is unchanged: the count of outbox deliveries that reach the exception or dead-letter path over one day, with a target of zero.

##### 3. Preconditions

- RWB-PLT-TE006-CON is published (this story's contract deliverable): the `OutboxWriter`, `OutboxConsumer` and `IdempotencyGuard` interfaces, the DDL contract of the four library tables, the CloudEvents 1.0 envelope and the caseId key, the inbox dedupe rule, the retry and dead-letter contract, the versioning rule and the fakes.
- RWB-PLT-E1044-CON is published: the per-service Flyway sequence and migration conventions (DP-15), so the library DDL template is applied by each service in its own schema and not by one shared migration.
- RWB-PLT-E1027-CON is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). RWB-P7-E1027-CON publishes the central ledger contract behind it.
- RWB-PLT-E1042-CON and RWB-PLT-E1043-CON are published: the parameters client library and the reference-data client library (DP-06, DP-07); RWB-P3-E1042-CON and RWB-P3-E1043-CON publish the rwb-case contracts behind them.
- RWB-PLT-E1071-CON is published: the Temporal workflow kit in namespace `rwb-recovery`, so a service can still choose an event-started workflow where one is warranted (DP-10).
- RWB-PLT-N001-CON is published: the gateway-bff composite route (DP-19); the admin screen itself is out of scope.
- RWB-P2-E1007-CON is published: the rwb-integration contract, so the outbound file path that a consumer such as "win-dispatch" calls is a published contract and not an in-process call.
- The ACE Kafka platform is provisioned with one event topic per service, its three retry topics and its dead-letter topic, and the schema registry is in BACKWARD mode (Arch v5 slides 11, 21, 22). The retention, partition and replication settings are the platform settings, not values of this story.
- The four table names `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` are owned by the platform library and created in every service schema under the Ownership Map ruling; which per-service database story applies each copy is Not specified in the source documents (GAP-1415; ASM-2473).
- The exception path of a delivery that keeps failing has no single owner in the sources: the legacy story raises a task and a case event in the same step as the move, while in the target the case-step event and the task belong to the service that owns the case step and the dead-letter path belongs to Kafka and the platform team (GAP-1415; ASM-2474).

##### 4. Flow

1. A business service (for example the notice approval in rwb-comms) calls `OutboxWriter.publish` inside its own transaction with the event type (an event of the EV catalogue such as CaseAllocated, or an outbound work request type such as WIN_DISPATCH), the schema version, the case ID where there is one, payload references, the actor reference and the idempotency key.
2. `OutboxWriter` writes one `outbox_event` row into the caller's own schema, under the caller's own login, with the next case sequence for that case, and one `outbox_delivery` row per recipient listed for the event type.
3. The caller's transaction commits the change, the event and its deliveries together, or none of them.
4. The per-service outbox relay (legacy JOB-11, now a continuous background worker in each service, not a Schedule) selects due deliveries with a skip-locked selection, oldest case sequence first, taking only the lowest open sequence per case and recipient.
5. The relay builds the CloudEvents 1.0 envelope in binary mode (`ce_specversion` 1.0, `ce_id`, `ce_type`, `ce_source`, `ce_subject`, `ce_time`), uses the case ID as the record key so one case's events stay in order on one partition, copies the W3C trace context and validates the body against the registry before it publishes.
6. The relay publishes with an idempotent producer and acks=all to the owning service's topic `rwb.<short>.events.v1` and marks the delivery DELIVERED on the broker acknowledgement; if Kafka is down the rows wait in the outbox and nothing is lost.
7. Each consumer records `ce_id` in `processed_event` in its own schema, in the same transaction as its own change, and drops a delivery it has already processed; `IdempotencyGuard.firstTime` answers the same question for a consumer that keeps its own key table.
8. A consumer that fails is redelivered by the Kafka retry topics at 1 min, 10 min and 1 h; a record that fails the third retry goes to the dead-letter topic and raises one alert to the platform administrator.
9. The owning service of the case step raises its own case events (SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED) and its own task through its own contract, and its own decision-record library writes the entry in the same transaction; the library itself raises no case event, no task and no decision record.
10. A record that is not in EXCEPTION is not resent: the resend operation belongs to the admin API of P2 rwb-integration, and a replay of the dead-letter topic is the recovery path of the platform team.
11. The relay records its runs and counts (due, delivered, retrying, dead-lettered) on the platform observability path so that the delivery count in the exception path can be measured daily.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The business transaction rolls back | No event and no delivery exist | None | AC3 |
| X2 | A recipient fails once and then succeeds | The delivery is DELIVERED on the retry; the owning service resumes the case when the recipient holds the case step (R-UNI-35) | None | AC4 |
| X3 | The same idempotency key is published twice | One event exists; the second call throws `DuplicateOutboxKeyException` and changes nothing | None | AC5 |
| X4 | Two relay instances run at once | The skip-locked selection makes each delivery once | None | AC6 |
| X5 | An earlier event for the same case and recipient is failing | Later events for that case and recipient wait behind it | None | AC7 |
| X6 | One recipient fails and another succeeds on the same event | Each recipient's delivery has its own state | None | AC8 |
| X7 | A delivery that is not in EXCEPTION is resent | Refused with 409 by the P2 admin API | MSG-P2-022 | AC9 |
| X8 | An event with no case fails past its retries | The record goes to the dead-letter topic and one alert goes to the platform administrator; the owning service raises no task and no case event | MSG-P2-001 | AC10 |
| X9 | The retry settings are changed | The next attempt uses the new windows; the Kafka ladder is applied through the configuration of section 13 | None | AC11 |
| X10 | The decision record cannot be written when the limit is reached | Nothing changes; the delivery stays RETRYING and is attempted at the next window; an incident is raised (R-UNI-39) | MSG-P7-003 | TC-TE-006-13 |
| X11 | A role without Platform administration U resends a delivery | Refused with 403 by the P2 admin API | MSG-P4-002 | TC-TE-006-12 |
| X12 | Kafka is down | The rows stay PENDING in the outbox of the caller's schema and are published when the broker returns; nothing is lost (Arch v5 slides 22 and 34) | None | AC1, AC6 |
| X13 | The relay instance stops with deliveries in flight | The rows keep their state; a delivery in flight is attempted again at its next window and the consumer drops the repeat through its inbox | None | AC6, AC8 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the library CON story and the platform contract stories; the case step, the decision record and the admin API are reached through their contract fakes, so no other service has to be built first |
| Negotiable | Recipients, owners, retry windows and batch size are configuration; the four tables, the envelope and the key are the published contract and are not negotiated per service |
| Valuable | Gives all 19 services one outbox, inbox and idempotency implementation on Day 1 and removes the shared Quartz sender and the single-schema tables from every service plan |
| Estimable | Four tables, one writer, one consumer, one relay, one DDL template and the fakes |
| Small | Fits one sprint with its tests |
| Testable | Each criterion below uses a stub consumer that fails on demand and the contract fakes of section 12.8 |

##### 7. Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work

  Background:
    Given consumer "win-dispatch" takes work request WIN_DISPATCH, holds the case step and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged, do not hold the case step and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 Sent after commit (legacy RWB-TE-006 AC1)
    Given a notice approved
    When the transaction commits at 14 December 2026 10:00:00
    Then the outbox holds one WIN_DISPATCH request for case "RW-2026-000601" with one delivery for "win-dispatch"
    Then the header holds the event ID, idempotency key "WIN_DISPATCH:NT-SYN-0601", schema version 1, occurred time and actor
    Then the payload holds notice and case references only, with no name, address or identifier
    Then at the 10:01 run the sender delivers it and "win-dispatch" passes the notice to OutboundFiles.enqueue for the day's WIN file
    Then the delivery has status DELIVERED

  Scenario: AC2 Retry limit (legacy RWB-TE-006 AC2)
    Given the rwb-case contract mock returns task code "RESOLVE_OUTBOX_DELIVERY" with owner role "RW-PLATADM" for case "RW-2026-000601" and event RETRY_LIMIT_REACHED accepted for that case
    Given a target down for longer than the retry limit
    When "win-dispatch" fails at 10:01, 10:02, 10:07 and 10:22
    Then the system makes no fifth attempt
    Then the item moves to the exception queue: the "win-dispatch" delivery has status EXCEPTION and attempt count 4
    Then the system raises task RESOLVE_OUTBOX_DELIVERY on case "RW-2026-000601" for role RW-PLATADM
    Then event RETRY_LIMIT_REACHED moves the case to EXCEPTION_QUEUE by R-UNI-36 with one decision log entry

  Scenario: AC3 Nothing is sent for a change that did not commit (legacy RWB-TE-006 AC3)
    Given the notice approval fails after OutboxWriter.publish and the transaction rolls back
    When the sender runs
    Then no event and no delivery exist for "NT-SYN-0601"

  Scenario: AC4 A retry that succeeds (legacy RWB-TE-006 AC4)
    Given the rwb-case contract mock returns route state RESUME_STATE for case "RW-2026-000601" when RETRY_SUCCEEDED is raised
    Given "win-dispatch" fails at 10:01 and the case moves to RETRY_QUEUE by R-UNI-33
    When the attempt at 10:02 succeeds
    Then the system delivers the delivery status with attempt count 2
    Then event RETRY_SUCCEEDED returns the case to the state it paused in by R-UNI-35

  Scenario: AC5 The same event is written once (legacy RWB-TE-006 AC5)
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the outbox holds one event with that key
    Then the second transaction receives DuplicateOutboxKeyException and changes nothing

  Scenario: AC6 Two sender instances (legacy RWB-TE-006 AC6)
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then the system makes each delivery once
    Then the delivery log holds 200 calls

  Scenario: AC7 Order per case and consumer (legacy RWB-TE-006 AC7)
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the sender runs
    Then the system does not deliver sequence 12 to "ledger" until sequence 11 is DELIVERED

  Scenario: AC8 Consumers are independent (legacy RWB-TE-006 AC8)
    Given event CaseAllocated for case "RW-2026-000601"
    When "ledger" fails and "reporting-feed" succeeds at 10:01
    Then the system delivers the "reporting-feed" delivery and the "ledger" delivery is RETRYING with next attempt 10:02
    Then the case route state does not change, because "ledger" does not hold the case step

  Scenario: AC9 Sending an exception delivery again (legacy RWB-TE-006 AC9)
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator sends it again
    Then the response is 200 with message MSG-GEN-005
    Then the delivery status is PENDING with attempt count 0 and due at the next run
    When the platform administrator sends delivery "OBD-SYN-0002" with status DELIVERED again
    Then the response is 409 with message MSG-P2-022

  Scenario: AC10 An event with no case (legacy RWB-TE-006 AC10)
    Given an event with no case whose only consumer fails 4 times
    When the retries are used
    Then the delivery status is EXCEPTION
    Then the system sends an alert to the platform administrator within 15 minutes
    Then no task and no case event are raised

  Scenario: AC11 Retry settings come from configuration (legacy RWB-TE-006 AC11)
    Given the retry delays are changed in the configuration service to 2, 10 and 30 minutes at 09:00
    When "ledger" fails at 10:01
    Then the next attempt is due at 10:03
```

**Note on the retry times.** The retry times in AC2 and AC4 are the legacy values, copied unchanged. The target retry ladder is the Kafka retry topics 1 min / 10 min / 1 h and then the dead-letter topic (Architecture v5 slide 22); the conflict is recorded in the gap (GAP-1415), and the criteria are tested with those windows through the configuration of section 13. The only additions to the criteria are the origin tag on each Scenario line and one `Given the rwb-case contract mock returns ...` line in AC2 and AC4, where the case step is mocked; no legacy line was changed or dropped.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction and the same schema as the change, under that service's own login: no event without the change and no change without the event | events.txt Rules, Transactions; DP-01; DP-09 |
| BR2 | Each event carries a CloudEvents id and an idempotency key unique in the caller's outbox; a second publish with the same key throws `DuplicateOutboxKeyException`, and a repeated delivery is dropped in the consumer's inbox `processed_event` or by `IdempotencyGuard` | events.txt Rules, Duplicates; R-UNI-40; Arch v5 slides 11 and 22 |
| BR3 | Delivery is at least once; each recipient has its own delivery state and its own consumer group | events.txt Rules, Delivery; Arch v5 slide 21 |
| BR4 | Events for one case reach each recipient in the order they were written: the record key is the case ID, so one case's events share one partition | events.txt Rules, Ordering; Arch v5 slides 21 and 22 |
| BR5 | A failed delivery climbs the retry topics at 1 min, 10 min and 1 h; after the third retry it goes to the dead-letter topic with one alert and the replay tool as the recovery path | Arch v5 slides 11, 22 and 34; NFR-026; REQ-DRI-007 |
| BR6 | The case-step effects belong to the service that owns the case step: the first failure raises SYSTEM_UNAVAILABLE, a later success RETRY_SUCCEEDED and the limit RETRY_LIMIT_REACHED through that service's own contract, never from the library | R-UNI-33; R-UNI-35; R-UNI-36; GAP-1415 |
| BR7 | The envelope carries `ce_specversion` 1.0, the event type with its schema version, the source as the owning service, the subject and the trace context; payloads hold references and codes, never personal data | events.txt Rules, Payload and Versioning; Arch v5 slides 11 and 22 |
| BR8 | Nothing moves when the decision record cannot be written: the record, the state change and the outbox row are one transaction (R-UNI-39) | R-UNI-39; Arch v5 slide 28; Temporal and Drools Design slide 28 |
| BR9 | Recipients, owners, retry windows and the batch size are configuration, read through the parameters client, never values in the code | Principle 1; DL11; DP-06 |

##### 9. State transitions

The case status does not change in this story. For a recipient that holds a case step, the route state changes through that service's universal rules, and each delivery has its own status inside the caller's schema.

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed delivery to a recipient that holds the case step, raised by the owning service | RETRY_QUEUE (R-UNI-33) |
| RETRY_QUEUE | RETRY_SUCCEEDED | The retry succeeds, raised by the owning service | RESUME_STATE (R-UNI-35) |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Retries used, raised by the owning service | EXCEPTION_QUEUE (R-UNI-36) |
| Delivery PENDING or RETRYING | Broker acknowledgement | None | Delivery DELIVERED |
| Delivery PENDING | Recipient fails | Retries left | Delivery RETRYING in the retry topic of the window |
| Delivery RETRYING | Recipient fails | No retries left | Record in the dead-letter topic; delivery EXCEPTION where the consumer reports the failure back |
| Delivery EXCEPTION | Resent through the P2 admin API | None | Delivery PENDING |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| Platform library team, owning the template | Publishes the interfaces, the DDL template, the envelope rule and the fakes; changes them only through the library contract story |
| The owning service of each consumer | Raises its own case events, its own task and its own decision record through its own contract |
| RW-PLATADM, platform administrator | Reads deliveries and resends an exception delivery through the admin API of P2, which this library does not provide |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries through the admin API of P2 |
| RW-SECADM, security administrator | Reads deliveries through the admin API of P2 |
| Platform team | Receives the dead-letter alert, holds the replay tool and owns the Kafka topic settings |
| No approval level from the delegation of authority applies | The library takes no business decision |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-189 | outbox_event | id | Write |
| DF-OPS-190 | outbox_event | event_type | Write |
| DF-OPS-191 | outbox_event | schema_version | Write |
| DF-OPS-192 | outbox_event | case_id | Write |
| DF-OPS-193 | outbox_event | case_seq | Write |
| DF-OPS-194 | outbox_event | idempotency_key | Write |
| DF-OPS-195 | outbox_event | payload | Write |
| DF-OPS-196 | outbox_event | actor_ref | Write |
| DF-OPS-197 | outbox_event | occurred_at | Write |
| DF-OPS-198 | outbox_delivery | id | Write |
| DF-OPS-199 | outbox_delivery | event_id | Write |
| DF-OPS-200 | outbox_delivery | consumer | Write |
| DF-OPS-201 | outbox_delivery | status | Write |
| DF-OPS-202 | outbox_delivery | attempt_count | Write |
| DF-OPS-203 | outbox_delivery | next_attempt_at | Write |
| DF-OPS-204 | outbox_delivery | last_error_code | Write |
| DF-OPS-205 | outbox_delivery | delivered_at | Write |
| DF-OPS-206 | outbox_delivery | task_id | Write |
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write, through the owning service's contract |
| DF-DEC-001 to DF-DEC-018 | decision_record (local library) | all fields | Write, through the local record library of the owning service |
| DF-CAS-001 | recovery_case | id | Read, through the rwb-case contract |

Field IDs are those in the Logical Data Model and Data Dictionary. The four library tables and the `processed_event` and `idempotency_key` columns have no field ID of their own in the source; they are the same objects the Ownership Map assigns to PLT, created in each service's own schema (GAP-1415; ASM-2472). No copy of another service's row is written.

##### 12. Contract

###### 12.1 REST operations provided

None — the admin read and resend API `GET /admin/outbox/deliveries` and `POST /admin/outbox/deliveries/{deliveryId}/resend` belongs to P2 rwb-integration in the Ownership Map, and the library publishes no REST surface of its own.

###### 12.2 REST operations consumed

None — the library joins the caller's transaction and calls no service.

###### 12.3 Events published

None — the caller's events are relayed to the owning service's `rwb.<short>.events.v1`; the library publishes no event of its own.

###### 12.4 Events consumed

None — the inbox receives the owning service's subscribed events, under that service's own consumer group and in that service's own `processed_event` table.

###### 12.5 Workflows and activities

None — the relay is a plain background worker in each service, not a workflow, and it starts no activity.

###### 12.6 Schedules

None — the relay is a continuous background worker, not a Schedule; the legacy Quartz JOB-11 trigger every minute does not become a Temporal Schedule (GAP-1415; ASM-2473).

###### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| outbox_event | PLT | One row per published fact, in the caller's own schema; unique key on `idempotency_key` and on `(case_id, case_seq)` |
| outbox_delivery | PLT | One row per event and recipient, in the caller's own schema; unique key on `(event_id, consumer)` and a due index on `next_attempt_at` |
| processed_event | PLT | The inbox of each consumer, in the consumer's own schema; unique key on the CloudEvents id and the consumer group |
| idempotency_key | PLT | The stored response per scope and key for a repeated command, in the caller's own schema |

The four tables are library objects created by the library DDL template in each service's own schema, under the Ownership Map ruling; they are not created once in an rwb-integration schema. No table of another service is read and no key crosses a schema boundary (DP-01, DP-15).

###### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| rwb-case case-event and task fake | The P3 case-step contract behind `CaseEvents.raise` and `TaskApi.raiseTask` | Task code RESOLVE_OUTBOX_DELIVERY for role RW-PLATADM on case RW-2026-000601; RETRY_LIMIT_REACHED accepted; route state RESUME_STATE on RETRY_SUCCEEDED (AC2, AC4) |
| rwb-decision decision-record fake | The P7 ledger contract behind the local record library | One decision log entry for the move to EXCEPTION_QUEUE (AC2, TC-TE-006-13) |
| Owning-service recipient fakes | The consumer side of each event type | A recipient stub that succeeds on demand and fails on demand, with the consumer names "win-dispatch", "ledger" and "reporting-feed" (AC1 to AC11) |
| rwb-integration admin API fake | The P2 contract behind the read and resend operations | An EXCEPTION delivery OBD-SYN-0001 and a DELIVERED delivery OBD-SYN-0002 (AC9) |

###### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, none consumed | The library adds no REST surface; the admin API is provided by P2 |
| Kafka | None published and none consumed by the library itself | The caller's records are relayed to the owning service's `rwb.<short>.events.v1` with the CloudEvents 1.0 envelope and the caseId key, through the three retry topics and the dead-letter topic |
| Temporal | None | The relay is a background worker; a service that needs a workflow for its own step uses the workflow kit |
| File | None | The library writes and reads no file; an outbound file is a claim-check call through the rwb-integration contract |

##### 13. Solution plan

**Package.** Shared library artifact of the platform, Java package `th.co.scb.ace.workbench.recovery.platform.outbox`; the three published interfaces sit in `th.co.scb.ace.workbench.recovery.platform.api`; the DDL template is a resource of the library, applied by each service's own Flyway sequence.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables. The outbox, inbox and idempotency rows are written in the caller's own schema | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1`; the record is written by the owning service in its own transaction, not by the relay | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library; the recipient list and the retry windows are parameters | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case; the recipient and event-type lists are reference rows | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents. This story is that library | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit; the legacy Quartz JOB-11 sender becomes a continuous per-service outbox relay, not a Temporal Schedule | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout; the recipient is reached through its published contract or its topic, never in process | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1`; the library adds no path of its own and every admin path belongs to P2 | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema; the library DDL template is applied by each service's own sequence | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route; the admin screen that reads and resends deliveries is out of scope | H RWB-PLT-N001-CON |

**Hardware and software change.** The outbox, inbox and idempotency tables are library objects created in every service schema, not one set of tables in a P2 schema; the relay publishes to each owner's topic with CloudEvents 1.0 and an idempotent producer; retry is the Kafka retry-topic ladder and the dead-letter topic with an alert and a replay tool; and the case-step and decision-record effects stay in the owning service's code through its contracts. No new hardware is added: the relay runs in each service's own pods on the existing AKS cluster and the tables sit in the existing ACE PostgreSQL server under each service's own login, replacing the shared Quartz sender and the single `recovery` schema tables.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| `OutboxWriter` | Published interface | Writes the event and one delivery per listed recipient in the caller's transaction (BR1, BR2, BR7) |
| `OutboxConsumer` | Published interface | Consumes one delivery and returns OK or FAILED with a code; the caller implements it under its consumer name |
| `IdempotencyGuard` | Published interface | Answers whether a consumer has already acted on a key (BR2) |
| OutboxEventEntity, OutboxDeliveryEntity, ProcessedEventEntity, IdempotencyKeyEntity | Entity | The four rows, mapped into the caller's schema |
| OutboxRepository | Repository | Skip-locked selection of due deliveries in case order per recipient (BR4) |
| OutboxRelay | Service | Continuous per-service relay: selection, envelope, publish, mark delivered, retry topic and dead-letter path (BR3, BR5) |
| ConsumerCatalog | Service | Reads the recipient list, the event types per recipient and the retry windows through the parameters and reference contracts (BR9) |
| EnvelopeFactory | Service | Builds the CloudEvents 1.0 binary-mode envelope, the caseId key and the trace headers (BR7) |
| OutboxDdlTemplate | Resource | The DDL contract of the four tables, applied by each service's own Flyway sequence (DP-15) |

**Database.** The library DDL template creates, in whichever schema applies it:
- `outbox_event` (id uuid primary key, event_type varchar(40) not null, schema_version integer not null, case_id uuid, case_seq bigint, idempotency_key varchar(120) not null, payload jsonb not null, actor_ref varchar(64), occurred_at timestamptz not null, plus the standard columns), with `UNIQUE (idempotency_key)` and `UNIQUE (case_id, case_seq)`.
- `outbox_delivery` (id uuid primary key, event_id uuid not null references outbox_event, consumer varchar(60) not null, status varchar(12) not null default 'PENDING', attempt_count integer not null default 0, next_attempt_at timestamptz not null, last_error_code varchar(40), delivered_at timestamptz, task_id uuid, plus the standard columns), with `UNIQUE (event_id, consumer)`, `CHECK (status IN ('PENDING','RETRYING','DELIVERED','EXCEPTION'))` and index `ix_outbox_delivery_due ON outbox_delivery (next_attempt_at) WHERE status IN ('PENDING','RETRYING')`.
- `processed_event` (id uuid primary key, ce_id varchar(64) not null, consumer_group varchar(60) not null, processed_at timestamptz not null, plus the standard columns), with `UNIQUE (ce_id, consumer_group)`.
- `idempotency_key` (id uuid primary key, scope varchar(60) not null, key varchar(120) not null, stored_response jsonb, created_at timestamptz not null, plus the standard columns), with `UNIQUE (scope, key)`.

`case_seq` is the case's highest sequence plus 1, taken under a lock on the case's latest outbox row in the same schema. No table references a table of another service. The `outbox_event` and `outbox_delivery` columns above are the legacy DDL and its field identifiers DF-OPS-189 to DF-OPS-206; the `processed_event` and `idempotency_key` column sets are the working read of this run, because no source defines them (GAP-1415; ASM-2473).

**Configuration and reference data.** The recipient list and the retry windows are parameters read through the parameters client (DP-06) and the reference-data client (DP-07), held by rwb-case: recipient name, the event types it takes, its owner role and whether it holds a case step; the retry windows of the ladder (1 min, 10 min, 1 h) and the batch size. The legacy values 3 retries at 1, 5 and 15 minutes stay in the AC text only and are exercised through this configuration (GAP-1415; ASM-2472). The alert route to the platform team and the replay tool are the platform observability and Kafka runbook items.

**Build steps**

1. Publish the three interfaces and their exceptions from the CON story; test that no method opens its own transaction.
2. Write the DDL template and the four entities; test the unique keys and the due index in a throwaway schema (AC5, AC6).
3. Write `OutboxWriter` joining the caller's transaction; test commit and rollback (AC1, AC3).
4. Write `OutboxRepository` with the skip-locked selection and the order per case and recipient; test two relay instances (AC6), order (AC7) and independent recipients (AC8).
5. Write `EnvelopeFactory` and the idempotent producer; test the headers, the caseId key, the trace header and the registry validation (AC1).
6. Write `OutboxConsumer` and the inbox; test the duplicate drop and the `IdempotencyGuard` path (AC5, AC8).
7. Write `OutboxRelay` with `ConsumerCatalog`; test the retry windows, a success after a failure and a configuration change (AC2, AC4, AC11).
8. Add the dead-letter alert, the counts and the replay note (AC10).
9. Hand the case-step events, the task and the decision record to the owning services as a contract test, and prove the library raises none of them (AC2, AC4).
10. Run the contract tests of section 12.8 against the fakes and prove that the library adds no REST surface (AC9).

**Feature flag.** One flag per service, read as a parameter; off, the relay does not publish and the deliveries stay PENDING while the writer still records the events, so nothing is lost when it is switched on.

**Done when.** The tests in section 16 pass, the contract tests of the CON story pass against the fakes, and the relay counts of every service appear on the platform observability path.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | Text when a delivery enters the exception path (new) | {interface} did not deliver {item} after {count} attempts. It is in the exception queue. |
| MSG-P2-022 | Resending a delivery that is not in EXCEPTION (new) | Only an item in the exception queue can be sent again. |
| MSG-GEN-005 | A delivery is queued to send again | Saved. |
| MSG-P7-003 | Decision record write failed at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role lacks the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Delivery not found | This case is not in your scope. |

In MSG-P2-001, {interface} is the recipient name and {item} the event type and case number. Thai text for each message follows decision DL10.

##### 15. Screens and states

No screen of its own. The task that an owning service raises on a failed case step appears on SCR-09 Exception queue (states Loading and List) for the owner role, with MSG-P2-001, and the owning service owns that display. The platform administrator reads and resends deliveries through the admin API that P2 rwb-integration provides; SCR-44 Interface and job monitor shows the deliveries from Epic 2. The library adds no screen and no route (DP-19).

##### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-006-13 | AC2, BR8 | NFR | Decision record write forced to fail at the exception move; the delivery stays RETRYING; MSG-P7-003 in the relay log; incident raised |
| TC-TE-006-12 | Access | Component | RW-DATASTEW resends a delivery through the P2 admin API; refused with MSG-P4-002 |
| TC-TE-006-01 | AC1, BR1, BR3, BR7 | Component | Notice NT-SYN-0601 approved at 10:00; win-dispatch stub succeeds; the envelope and the caseId key are asserted |
| TC-TE-006-02 | AC2, BR5, BR6 | Component | win-dispatch stub fails 4 times through the retry topics and the dead-letter topic |
| TC-TE-006-03 | AC3, BR1 | Component | Approval rolled back after publish |
| TC-TE-006-04 | AC4, BR6 | Component | win-dispatch stub fails once, then succeeds |
| TC-TE-006-05 | AC5, BR2 | Component | Two approvals with key WIN_DISPATCH:NT-SYN-0601 |
| TC-TE-006-06 | AC6, BR3 | Component | 200 due deliveries, two relay instances |
| TC-TE-006-07 | AC7, BR4 | Integration | Sequences 11 and 12, ledger stub failing on 11, one partition key caseId |
| TC-TE-006-08 | AC8, BR3 | Component | ledger fails and reporting-feed succeeds on one CaseAllocated event |
| TC-TE-006-09 | AC9 | Component | Deliveries OBD-SYN-0001 in EXCEPTION and OBD-SYN-0002 DELIVERED |
| TC-TE-006-10 | AC10 | Component | Event with no case, consumer failing 4 times, one dead-letter alert |
| TC-TE-006-11 | AC11, BR9 | Component | Retry windows changed in configuration before the run |

The legacy test case ids are kept with their level mapped to the target shape: Access becomes Component, Principle 5 and Resilience become NFR, and System becomes Component or Integration. The full test, with its Given, When and Then, is carried into the next Test Cases version under the same id.

##### 17. Guardrails

- No business value in code: recipients, owners, retry windows and batch size are configuration read through the parameters and reference contracts.
- No personal data in logs, events, tests or prompts; payloads hold references and codes only, and the envelope carries IDs and facts.
- No read of another service's tables and no cross-schema key: the outbox, the inbox and the idempotency rows are written in the caller's own schema, and case events, tasks and decision records go through their owners' contracts.
- No event and no delivery is deleted; a record leaves the exception path only by a resend through the P2 admin API or a replay of the dead-letter topic.
- The library raises no case event, no task and no decision record of its own.

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Business Requirements Program, section 5.2 and section 6.4 | None | All recovery processes | R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40 | TC-TE-006-01 to TC-TE-006-13 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-TE006-CON | Contract | H: publishes the interfaces, the DDL template, the envelope, the dedupe and retry rules and the fakes this story implements |
| RWB-PLT-E1027-CON | Contract | H: the local decision-record library the owning service writes through |
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON | Contract | H: the parameters and reference-data clients for the recipient list and the retry windows |
| RWB-PLT-E1071-CON | Contract | H: the workflow kit for a service that needs an event-started workflow |
| RWB-PLT-E1044-CON | Contract | H: the per-service Flyway sequence that applies the DDL template |
| RWB-PLT-N001-CON | Contract | H: the gateway route; the admin screen is out of scope |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1027-CON, RWB-P2-E1007-CON | Contract | C: the owner contracts behind the parameters, the reference data, the decision record and the outbound file path |
| RWB-PLT-EVT | Platform epic | X: the event platform stories provision the topics, the retry topics, the dead-letter topic and the registry |

##### 19. Out of scope

- Outbound files, their SFTP transfer, retry and resend, and the duplicate check by key: RWB-P2-E1007-CON and the P2 stories behind it.
- The recipients themselves, for example the ledger listener: the owning service stories of each consumer.
- The interface and job monitor screen and the admin read and resend screen: SCR-44 in Epic 2 and Epic 8, and the admin API of P2 rwb-integration.
- The Kafka topic settings, the ACLs, the retry topics and the dead-letter topic themselves: RWB-PLT-EVT.
- The decision-record library and the central ledger: RWB-PLT-E1027-CON and RWB-P7-E1027-CON.
- The retry values as a business decision: DL11, and the conflict recorded in GAP-1415.


### RWB-ITG-TE006-ITG Outbox and retry for outbound work — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-006 for the wave-1 integration epic. The monolith outbox with one in-process consumer call becomes the outbox and inbox library of the platform, one owner topic per service, CloudEvents 1.0 on Kafka with retry topics and a `.dlt`, the case effects as Temporal signals on `rwb-case`, the move to the exception queue as a decision record on `rwb.decision-record.v1`, and the WIN dispatch as the `deliverFile` step of rwb-integration; this story builds and runs the harness that proves that path across services and topics. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE006-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-006 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP09, DP10, DP11, DP13, DP15, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P2-E1007-APP, RWB-PLT-TE006-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-009, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-021, FR-PLT-022, FR-PLT-023, FR-PLT-024, FR-PLT-025, FR-PLT-026, FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

##### 1. Story

As a **tech lead**, I want **the outbox and inbox library of the platform exercised end to end across the wave-1 services: every service writing its event and one delivery per consumer in its own schema inside the caller's transaction, the relay of each service publishing CloudEvents 1.0 to that service's own topic keyed caseId, every consumer deduping through its inbox, a failing consumer walking the retry topics to the `.dlt` with an alert, and the case effects and the exception task arriving in rwb-case and the decision record in rwb-decision**, so that **no outbound action is lost or sent twice when a system or a consumer is down, and the retry, ordering, dedupe and exception behaviour is proven on the services and topics that will run it rather than on one service's in-process stand-in**.

##### 2. Business rationale

The legacy story protects the Workbench with one transactional outbox in the integration module, a sender that calls each consumer directly in process, and case events raised through a published P3 interface (RWB-TE-006 sections 4 and 12). If the event is sent before the change commits, or is lost when a consumer fails, a notice is never dispatched or a ledger entry is missing, and nobody sees it; the measure is the count of outbox deliveries in the exception queue over one day, with a target of zero (FSD P2 A2.1.1). REQ-DRI-007 asks for retry on a defined schedule and an exception queue with a task for a named owner.

In the target nothing of that path stays inside one process. Every service is built from the template with its own schema, its own relay and its own topic (Arch v5 slides 20 and 41), so the tables `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key` are library objects created in each service schema (DP-09, ASM-0074), and rwb-integration owns no table of another service. Delivery is a Kafka publish in CloudEvents 1.0 binary mode with the case ID as the key, retry topics at 1 minute, 10 minutes and 1 hour, and a `.dlt` with an alert (Arch v5 slide 11); the consumers dedupe through their own inbox. The case effects that the legacy story raised in process become signals and activities on `rwb-case` through CaseWorkflow, one hop on the owner's queue and never a REST call chain (DP-11, DP-12; Temporal design slides 11 and 14), and the move of a case to the exception queue writes its decision record through `rwb.decision-record.v1` owned by rwb-decision (DP-03). The outbound work request WIN_DISPATCH is no longer an internal adapter: it is the daily WIN file that rwb-comms opens at 16:00 and rwb-integration delivers with its `deliverFile` activity (Arch v5 slides 16 and 44, JOB-10). A local outbox that commits alone, an event without a subscriber, a duplicate acted on twice, a poison message with no dead letter, a case left in the retry queue and a decision that moves a case without its record are all failures that only appear across services; this story builds and runs the harness that proves them together, and it publishes no operation, owns no table and adds no business rule of its own.

##### 3. Preconditions

- The nine wave-1 services are deployed in DEV and SIT, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- Every wave-1 schema holds the library objects of DP-09 created by its own DB story: `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key`, with the unique key on `outbox_event.idempotency_key` and the unique key on `(event_id, consumer)` in `outbox_delivery` (ASM-0074; RWB-PLT-TE006-APP and the DB story of each service).
- The topic of each service exists with its retry topics and `.dlt` topic — `rwb.comms.events.v1`, `rwb.case.events.v1`, `rwb.integration.events.v1`, `rwb.decision-record.v1` and the topics of the other wave-1 services in the fixture path — with the JSON Schema registry in BACKWARD mode (Arch v5 slide 11; RWB-PLT-EVT).
- The relay JOB-11 runs in every service every minute and is part of the service template (Arch v5 slides 20 and 44; ownership ruling ASM-0063, so it is not a Temporal Schedule).
- Queue `rwb-case` is registered in namespace `rwb-recovery`, and CaseWorkflow is deployed with its signals on `rwb-case` (RWB-P3-E1018-APP, RWB-PLT-E1071-CON).
- rwb-integration is deployed with the `deliverFile` activity and the 16:00 WIN window of JOB-10 (Arch v5 slides 16 and 44; RWB-P2-E1007-APP; ownership ruling ASM-0062).
- rwb-decision consumes `rwb.decision-record.v1` and holds the central ledger; the decision-record library is available to every service (DP-03; RWB-PLT-E1027-CON).
- rwb-access answers `POST /api/recovery/access/v1/authorise` and holds the test roles RW-PLATADM, RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY and RW-SECADM with their Platform administration letters (RWB-P4-E1008-APP; Arch v5 slide 14).
- The consumer list per event type and the retry settings are read as parameters through the rwb-case parameters contract, and the event types and delivery statuses as reference data through the rwb-case reference-data contract; no value is written in harness code (DP-06, DP-07).
- The mapping from the legacy case events to the signals and activities of `rwb-case`, the service that raises RESOLVE_OUTBOX_DELIVERY, the retry delays, the `.dlt` alert route and the consumer list per event type are Not specified in the source documents (GAP-0382; ASM-0553; ASM-0554).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the platform library and rwb-integration and is run when they are in DEV; a fake is never used in their place.

##### 4. Flow

1. Harness: reads the service list, the topic list, the consumer list, the retry settings and the queue names from configuration, and runs the preflight of section 13; a missing library table in a service schema, a missing topic, retry topic or `.dlt`, a missing relay or a missing queue stops the run before any test.
2. Harness: drives one real state change in rwb-comms on synthetic case "RW-2026-000601" with notice "NT-SYN-0601" approved, through the service's own write path, and reads the case back through `GET /api/recovery/case/v1/cases/{caseId}` (DP-11, DP-13).
3. Service: writes the state change, the `outbox_event` row and one `outbox_delivery` row per configured consumer in one transaction in its own schema; a failed transaction leaves none of the three (BR1).
4. Relay: JOB-11 in that service selects the due deliveries in case order with a skip-locked read, publishes one CloudEvents 1.0 event in binary mode on the owner topic with key "RW-2026-000601" and `acks=all`, and marks the delivery DELIVERED on the broker acknowledgement (BR3, BR4, BR9).
5. Harness: reads the topic with its own consumer group and asserts one event per change, the envelope (`ce_id`, `ce_source`, `ce_type`, `ce_schemaurl`, `ce_time`, `ce_idempotencykey`) and a payload of case and notice references only (BR7).
6. rwb-integration: the `win-dispatch` consumer of work request WIN_DISPATCH resolves to the `deliverFile` activity on queue `rwb-integration`; the file run opens in the 16:00 WIN window of JOB-10 and publishes `rwb.integration.FileDelivered.v1` on `rwb.integration.events.v1` (BR9, BR10).
7. Consumers: each consumer records the CloudEvents id in its own `processed_event` before it acts, so a repeated delivery changes nothing (BR2, BR6).
8. Harness: makes one consumer fail on demand and reads the delivery back through `GET /api/recovery/integration/v1/admin/outbox/deliveries`; the retry chain of the topic and the relay schedule advance the delivery RETRYING, then DELIVERED, or to EXCEPTION with the attempt count of the legacy fixtures (BR5).
9. rwb-case: on the first failure of a consumer that holds a case step CaseWorkflow receives SYSTEM_UNAVAILABLE, on a later success RETRY_SUCCEEDED, and at the limit RETRY_LIMIT_REACHED; rwb-decision receives the record of the move to the exception queue on `rwb.decision-record.v1`, and `RESOLVE_OUTBOX_DELIVERY` appears in the task list of the consumer's owner role (BR6, BR8, BR10).
10. Harness: as RW-PLATADM, resends an EXCEPTION delivery through `POST /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend`, and repeats the call as a role without Platform administration U through the rwb-access check (BR5).
11. Harness: reconciles the counts — one change, one event, one delivery per consumer, one effect per consumer, one record per move to the exception queue — and writes the run report.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The business transaction rolls back | No event and no delivery exist in the service schema | None | AC1 |
| X2 | The same idempotency key is published twice | One event exists; the second transaction receives DuplicateOutboxKeyException and changes nothing | None | AC4 |
| X3 | The same event is delivered twice to a consumer | The consumer inbox `processed_event` ignores the second delivery; one effect exists | None | AC4 |
| X4 | A consumer fails once and then succeeds | The delivery is DELIVERED on the retry and the case resumes by R-UNI-35 | None | AC3 |
| X5 | The retries are used | The delivery is EXCEPTION; RESOLVE_OUTBOX_DELIVERY is raised for the consumer's owner role; RETRY_LIMIT_REACHED moves the case by R-UNI-36; MSG-P2-001 is the task text | MSG-P2-001 | AC3 |
| X6 | The decision record cannot be written at the exception move | Nothing changes; the delivery stays RETRYING and is tried at the next run; an incident is raised (R-UNI-39) and the caller sees MSG-P7-003 | MSG-P7-003 | AC3 |
| X7 | An earlier event for the same case and consumer is failing | Later events for that case and consumer wait on the topic and on the relay | None | AC5 |
| X8 | Two relay instances run at once | Each delivery is published once; the consumer drops a repeat by its key | None | AC5 |
| X9 | An event with no case reaches the `.dlt` | EXCEPTION and an alert to the platform administrator; no task and no case event | MSG-P2-001 | AC6 |
| X10 | A delivery that is not in EXCEPTION is resent | Refused with 409 | MSG-P2-022 | AC6 |
| X11 | A role without Platform administration U resends a delivery | Refused with 403 after the rwb-access check | MSG-P4-002 | AC6 |
| X12 | The delivery ID does not exist | The read answers 404 | MSG-P4-003 | AC6 |

X1 to X8 are the exception paths of the legacy story carried onto the real services and topics; X9 to X12 are the dead-letter, resend and access paths the Kafka and platform shape adds. The alert route of X9 is Not specified in the source documents (GAP-0382; ASM-0553).

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the platform library, the wave-1 services, the topics and the `rwb-case` and `rwb-integration` workers, and it owns no schema and no table |
| Negotiable | Fixture counts, wait intervals and report layout are configuration; consumer names, case, notice, deliveries, sequences, keys, messages and statuses are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: one event per change, one delivery per consumer, one effect per consumer, order per case, a dead letter with an alert, a case effect and a record at the limit |
| Estimable | One harness project, six test classes, five fixtures, one forced failure per consumer and one resend pair |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a row, an event, a delivery state, a signal outcome, a task, a record, a response |

##### 7. Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work, proven across the wave-1 services and topics

  Background:
    Given the environment is DEV with synthetic data
    Given the nine wave-1 services run with their own schemas, logins, topics and relays
    Given every service schema holds outbox_event, outbox_delivery, processed_event and idempotency_key from the platform library
    Given consumer "win-dispatch" takes work request WIN_DISPATCH and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 The event and its deliveries commit or roll back with the caller's transaction (new, D-RCV-60)
    Given the approval of "NT-SYN-0601" in rwb-comms writes work request WIN_DISPATCH for case "RW-2026-000601"
    When the transaction commits at 14 December 2026 10:00:00
    Then rwb_comms holds one outbox_event with event type WIN_DISPATCH, schema version 1, case ID, the next case sequence and idempotency key "WIN_DISPATCH:NT-SYN-0601"
    Then rwb_comms holds one outbox_delivery per configured consumer, each with status PENDING and attempt count 0
    Then no other service schema holds a row of that change and no service reads another service's outbox tables
    When a second approval writes the same event and its transaction rolls back after the write
    Then no outbox_event and no outbox_delivery exist for that attempt
    Then the harness finds no event for that attempt on any topic

  Scenario: AC2 One CloudEvents event per delivery on the owner's topic, and the WIN step is a file through rwb-integration (new, D-RCV-60)
    Given the relay of rwb-comms runs at 10:01
    When it publishes the due deliveries of case "RW-2026-000601"
    Then exactly one CloudEvents 1.0 event in binary mode is on rwb.comms.events.v1 with key "RW-2026-000601" and acks=all
    Then the harness consumer group reads ce_id, ce_source, ce_type, ce_schemaurl, ce_time and ce_idempotencykey "WIN_DISPATCH:NT-SYN-0601"
    Then the payload holds the case and notice references and codes only, with no name, address or identifier
    Then the delivery to "win-dispatch" is DELIVERED and the consumer resolves to the deliverFile activity on queue rwb-integration
    Then the file run opens inside the 16:00 WIN window of JOB-10 and rwb.integration.FileDelivered.v1 is on rwb.integration.events.v1
    Then no in-process adapter call exists between the producer and the consumer, and the harness fails the run if one is found

  Scenario: AC3 The case effects arrive as Temporal signals on rwb-case, and the limit writes the decision record (new, D-RCV-60)
    Given the consumer "win-dispatch" fails at 10:01
    Then CaseWorkflow receives SYSTEM_UNAVAILABLE by R-UNI-33 and the case moves to RETRY_QUEUE
    When the attempt at 10:02 succeeds
    Then the delivery is DELIVERED with attempt count 2 and CaseWorkflow receives RETRY_SUCCEEDED, which returns the case to the state it paused in by R-UNI-35
    Given the consumer fails at 10:02, 10:07 and 10:22 as well
    Then the relay makes no fifth attempt
    Then the delivery to "win-dispatch" is EXCEPTION with attempt count 4
    Then task RESOLVE_OUTBOX_DELIVERY is raised in rwb-case on case "RW-2026-000601" for the owner role named in the consumer configuration, with text MSG-P2-001
    Then CaseWorkflow receives RETRY_LIMIT_REACHED and the case moves to EXCEPTION_QUEUE by R-UNI-36
    Then rwb.decision-record.DecisionRecorded.v1 is on rwb.decision-record.v1 and rwb_decision holds one entry for the move, so the move and its record commit together (R-UNI-39)
    When the decision record cannot be written at the exception move
    Then nothing changes, the delivery stays RETRYING and is tried at the next run, the caller sees MSG-P7-003 and an incident is raised

  Scenario: AC4 One event per key and one effect per consumer, whatever the delivery count (new, D-RCV-60)
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the producer schema holds one outbox_event with that key and the second transaction changes nothing
    Given the same event is delivered to a consumer twice
    When the consumer handles both deliveries
    Then its processed_event holds the CloudEvents id once and the effect exists once
    Then the harness reads one event on the topic and one effect per consumer for the change (R-UNI-40)
    When the harness counts the messages on the retry topics for that event
    Then no message is duplicated by a second publish of the same outbox_event

  Scenario: AC5 Order per case and consumer, and one delivery each across two relay instances (new, D-RCV-60)
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the relay runs
    Then sequence 12 is not delivered to "ledger" until sequence 11 is DELIVERED
    Then the order holds per case and consumer only, so "reporting-feed" reads its own deliveries in its own order
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then each delivery is published once and the consumer group log holds 200 events for the 200 deliveries
    Then two deliveries of one event to two consumers keep their own state, so a failure of "ledger" leaves "reporting-feed" DELIVERED and "ledger" RETRYING with the next attempt at 10:02

  Scenario: AC6 The exception queue is worked through the P2 admin surface and the P4 right check (new, D-RCV-60)
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator resends it through POST /api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend
    Then the response is 200 with message MSG-GEN-005
    Then its status is PENDING with attempt count 0 and it is due at the next run
    When the platform administrator resends delivery "OBD-SYN-0002" with status DELIVERED
    Then the response is 409 with message MSG-P2-022
    When a test user holding only RW-DATASTEW resends a delivery
    Then rwb-access refuses the Platform administration U check and the answer is 403 with MSG-P4-002
    When a delivery ID that does not exist is read
    Then the answer is 404 with MSG-P4-003
    Given an event with no case whose only consumer fails 4 times
    Then the delivery reaches the .dlt topic of the owner, its status is EXCEPTION and an alert reaches the platform administrator
    Then no task and no case event are raised for that event
```

The mapping from the legacy case events to the signals and activities of `rwb-case`, and the service that raises the `RESOLVE_OUTBOX_DELIVERY` task, are Not specified in the source documents (GAP-0382; ASM-0553); the retry delays and the `.dlt` alert route are Not specified in the source documents (GAP-0382; ASM-0553); the consumer list per event type across services is Not specified in the source documents (GAP-0382; ASM-0554). The legacy acceptance criteria that these scenarios re-exercise are owned by RWB-PLT-TE006-APP and are named in section 16.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction as the change, in the producer's own schema: no event without the change and no change without the event | RWB-TE-006 BR1; DP-01; DP-09; Arch v5 slide 11 |
| BR2 | Each event carries a CloudEvents id and an idempotency key unique in the producer's outbox; a consumer drops a repeat through its inbox `processed_event` | RWB-TE-006 BR2; R-UNI-40; Arch v5 slide 11 |
| BR3 | Delivery is at least once and each consumer has its own delivery state, advanced by the relay on the acknowledgement of an `acks=all` publish | RWB-TE-006 BR3; Arch v5 slide 11 |
| BR4 | Events for one case reach each consumer in the order they were written; the key is the case ID, the relay reads due deliveries in case order with a skip-locked selection, and a failing event holds later events for that case and consumer | RWB-TE-006 BR4; Arch v5 slide 11 (key caseId, order per case) |
| BR5 | A failed delivery is retried on the configured schedule and, when the retries are used, the delivery is EXCEPTION and the item is worked from the exception queue; the retry delays, the counts and the alert route are data, not code | RWB-TE-006 BR5; NFR-026; REQ-DRI-007; GAP-0382 |
| BR6 | For a consumer that holds a case step, the first failure raises SYSTEM_UNAVAILABLE, a later success RETRY_SUCCEEDED and the limit RETRY_LIMIT_REACHED, all as signals on CaseWorkflow in rwb-case; the exception task RESOLVE_OUTBOX_DELIVERY is raised in rwb-case for the owner role in the consumer configuration | RWB-TE-006 BR6; R-UNI-33; R-UNI-35; R-UNI-36; ASM-0553 |
| BR7 | Payloads hold references and codes, never personal data, and every event carries its schema version in the registry | RWB-TE-006 BR7; Arch v5 slide 11 |
| BR8 | A case does not move to the exception queue unless its decision record is written; a refused record leaves the delivery RETRYING and raises an incident | R-UNI-39; CTL-06; DP-03 |
| BR9 | Every event travels on the producer's own topic `rwb.<short>.events.v1` in the CloudEvents 1.0 envelope, binary mode, key caseId, with the retry topics at 1 minute, 10 minutes and 1 hour and a `.dlt` with an alert; no service publishes another service's topic | Arch v5 slides 11 and 20; DP-09; Template and Rules §R4 |
| BR10 | The outbound work request WIN_DISPATCH is delivered as the daily WIN file by the `deliverFile` activity of rwb-integration inside the 16:00 window of JOB-10, not by an in-process adapter | Arch v5 slides 16 and 44; ASM-0062; DP-16 |
| BR11 | The consumer list, the retry settings and the case-step flag of a consumer are parameters read through the rwb-case parameters contract, and the event types and delivery statuses are reference data read through its reference-data contract | RWB-TE-006 BR9; DP-06; DP-07 |

##### 9. State transitions

No case status changes because of this story; it drives and asserts. The states it observes:

| Item | States |
|---|---|
| Delivery | PENDING (written, not yet published or not yet published successfully), RETRYING (a publish or a consumer failed with attempts left), DELIVERED (the broker acknowledged the publish with `acks=all`), EXCEPTION (the retries are used or the event reached the `.dlt`) |
| Delivery after a resend | EXCEPTION becomes PENDING with attempt count 0 and is due at the next relay run |
| Relay run | Idle, running (skip-locked selection of due deliveries), or stopped by the feature flag, in which case deliveries stay PENDING |
| Consumer | Received, deduplicated through `processed_event`, acted on once, retried through the retry topic, or dead-lettered |
| Case route state, observed through rwb-case | ANY_ACTIVE to RETRY_QUEUE on SYSTEM_UNAVAILABLE (R-UNI-33); RETRY_QUEUE to the state it paused in on RETRY_SUCCEEDED (R-UNI-35); RETRY_QUEUE to EXCEPTION_QUEUE on RETRY_LIMIT_REACHED (R-UNI-36) |
| Exception task | Raised for the consumer's owner role, open, then closed when the item is worked |
| Harness run | Not started, running, passed, failed with the failing criterion named |

| From | Event or cause | Condition | To |
|---|---|---|---|
| PENDING | Relay publishes | Broker acknowledges | DELIVERED |
| PENDING | Publish or consumer fails | Attempts left | RETRYING |
| RETRYING | Retry succeeds | None | DELIVERED |
| RETRYING | Retry fails | No attempts left | EXCEPTION |
| EXCEPTION | Platform administrator resends | None | PENDING (attempt count 0) |
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed delivery to a consumer that holds the case step | RETRY_QUEUE (R-UNI-33) |
| RETRY_QUEUE | RETRY_SUCCEEDED | The retry succeeds | The state it paused in (R-UNI-35) |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | The retries are used and the decision record is written | EXCEPTION_QUEUE (R-UNI-36) |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the forced failures and the run report |
| Platform library owner (RWB-PLT-TE006-CON, RWB-PLT-TE006-APP) | Owns the outbox, inbox and idempotency objects, the delivery statuses, the retry scheduling and the relay |
| Wave-1 service teams | Own their schema, their topic, their relay instance and their consumers |
| rwb-integration owner (RWB-P2-E1007-APP) | Owns the `deliverFile` activity, the file run and the two admin endpoints of the Ownership Map |
| rwb-case owner | Owns CaseWorkflow, the three signals, the exception task and the case route state |
| rwb-decision owner | Owns the decision record, the shared topic and the ledger entry |
| rwb-access owner | Owns the Platform administration right check and the refusals |
| RW-PLATADM Platform administrator | Reads deliveries and resends an EXCEPTION delivery (Platform administration CRUD) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries (Platform administration R) |
| RW-SECADM Security administrator | Reads deliveries (Platform administration CRUDA) |
| No role | Updates or deletes an event or a delivery |

The harness acts only through the services' own write paths, the topics and the admin and access endpoints; it never writes a service schema directly. The forced failures of AC3, AC5 and AC6 run on the synthetic data set in DEV and SIT only and are switched off in UAT and production.

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-OPS-189 to DF-OPS-197 | `outbox_event` (each service schema) | id, event_type, schema_version, case_id, case_seq, idempotency_key, payload, actor_ref, occurred_at | Write by the owner; read by the harness through the admin read |
| DF-OPS-198 to DF-OPS-206 | `outbox_delivery` (each service schema) | id, event_id, consumer, status, attempt_count, next_attempt_at, last_error_code, delivered_at, task_id | Write by the owner; read by the harness through the admin read |
| None | `processed_event` (each consumer schema) | event id, consumer group, processed at | Write by the consumer; read by the harness through the consumer's own probe |
| None | `idempotency_key` (each service schema) | key, stored response, created at | Write by the owner; asserted on the duplicate path of AC4 |
| DF-WRK-017 to DF-WRK-026 | `task` (rwb_case) | all fields | Write through the P3 contract; read as RW-PLATADM through `GET /api/recovery/case/v1/me/tasks` |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (the owner schema) and `decision_log_entry` (rwb_decision) | all fields | Write through the DP-03 library and the P7 ingest; read through the decision read |
| DF-CAS-001 | `recovery_case` (rwb_case) | id | Read |
| DF-CAS-007 | `recovery_case` (rwb_case) | route_state | Write through the P3 rule step; read through the case read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-006. The harness owns no schema, no table and no field: it reads the delivery rows through the P2 admin read, the case and task rows through the P3 contract, the decision record through the P7 read, and it observes the topics with its own consumer group.

The library tables are created in every service schema by that service's DB story under ASM-0074, not in `rwb_integration` alone; the delivery attempt count that reaches 4 in AC3 and the retry delays are Not specified in the source documents (GAP-0382; ASM-0553).

##### 12. Contract

###### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/integration/v1/admin/outbox/deliveries` | P2 rwb-integration | Reads the delivery rows of the run by status, consumer, event type and date; the payload is not returned |
| POST | `/api/recovery/integration/v1/admin/outbox/deliveries/{deliveryId}/resend` | P2 rwb-integration | Resends an EXCEPTION delivery as RW-PLATADM, and the refusals of AC6 |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | Platform administration R, U and CRUDA checks for every reader and for the resend |
| POST | `/api/recovery/case/v1/cases/{caseId}/actions` | P3 rwb-case | The case command that a consumer's case step applies, used to drive the fixture change |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Reads the route state RETRY_QUEUE, RESUME_STATE or EXCEPTION_QUEUE after a signal |
| GET | `/api/recovery/case/v1/me/tasks` | P3 rwb-case | Finds the open RESOLVE_OUTBOX_DELIVERY task and its owner role |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service. The admin read is P2's by the Ownership Map; that it serves the delivery rows of every service through the library admin contract is Not specified in the source documents (GAP-0382; ASM-0554).

###### 12.3 Events published

None. The harness publishes no business event of its own; every event asserted in this story is produced by a wave-1 service and is listed in 12.4.

###### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.comms.NoticeGenerated.v1` | `rwb.comms.events.v1` | P6 rwb-comms | CloudEvents 1.0 binary mode, key caseId, exactly one event per approval; the harness group reads it to prove the producer side of AC1 and AC2 |
| `rwb.integration.FileDelivered.v1`, `rwb.integration.FileFailed.v1` | `rwb.integration.events.v1` | P2 rwb-integration | The WIN file step of the `win-dispatch` consumer; a failed file publishes FileFailed and is retried inside the workflow |
| `rwb.case.CaseAllocated.v1`, `rwb.case.CaseTransferred.v1`, `rwb.case.CaseStateChanged.v1` | `rwb.case.events.v1` | P3 rwb-case | Order per case and consumer, key caseId; the "ledger" and "reporting-feed" fixtures read them for AC5 |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | P7 rwb-decision (produced by every service) | One event per append; the harness reads the record of the move to the exception queue |

The consumer list per event type across services is Not specified in the source documents (GAP-0382; ASM-0554); under that assumption "win-dispatch" resolves to the rwb-integration file step, "ledger" to rwb-source-data's interaction ledger and "reporting-feed" to the rwb-reporting projections, and each fixture subscribes with its own consumer group. Every consumer dedupes on the CloudEvents id through `processed_event` and walks the retry topics at 1 minute, 10 minutes and 1 hour before the `.dlt` (Arch v5 slide 11).

###### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| CaseWorkflow | Workflow | `rwb-case` | Workflow ID is the case ID; signals SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED and RETRY_LIMIT_REACHED with the case ID and the consumer reference; the harness reads the resulting route state through the case read |
| deliverFile | Activity | `rwb-integration` | Input the manifest of the WIN file (fileId, batchId, sha256, record count); output the file run; idempotent on fileId; runs inside the 16:00 window of JOB-10 |
| `outboxRelay` (JOB-11) | Relay, not a Temporal workflow | Every service | Publishes the due `outbox_event` rows to the owner topic and advances the delivery state; part of the service template |

The signal names and the task code are the legacy ones; that they are delivered as Temporal signals on `rwb-case` rather than through the legacy published interface is Not specified in the source documents (GAP-0382; ASM-0553).

###### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| `winFileWindow` | Daily at 16:00, Airflow file window with the rwb-comms notice run and the `deliverFile` step of rwb-integration | JOB-10, owned by rwb-comms with rwb-integration performing the delivery (ASM-0062) | JOB-10 WIN notices |
| `outboxRelay` | Every minute in every service | JOB-11, part of the service template and not a Temporal Schedule (ASM-0063) | JOB-11 Outbox sender |

###### 12.7 Tables owned

None. The harness owns no table. The tables it exercises belong to each service schema and to rwb_case, rwb_decision and the platform library, and are listed in section 11 with their owners. The outbox, inbox and idempotency tables are library objects created in every service schema under ASM-0074, and the consumer list per event type is Not specified in the source documents (GAP-0382; ASM-0554).

###### 12.8 Contract fakes

None. This is the integration level: the real platform library, the real services, the real topics and the real `rwb-case` and `rwb-integration` workers replace the contract fakes of RWB-PLT-TE006-APP and RWB-P2-E1007-APP.

###### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6 | Two admin outbox calls, the authorise call, one case command, one case read and the task read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 7 event types on 4 topics | `rwb.comms.events.v1`, `rwb.integration.events.v1`, `rwb.case.events.v1` and `rwb.decision-record.v1`; key caseId, CloudEvents 1.0 binary, retry topics and `.dlt` |
| Temporal | None | 1 workflow, 1 activity, 3 signals | CaseWorkflow on `rwb-case` with SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED and RETRY_LIMIT_REACHED; `deliverFile` on `rwb-integration` |
| File | None | 1 file step | The daily WIN file inside the 16:00 window (JOB-10), claim-check manifest with fileId, batchId, sha256 and record count |

##### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/outbox`, with the six test classes `TransactionalOutboxIT`, `RelayAndTopicIT`, `CaseEffectIT`, `DedupeIT`, `OrderAndConcurrencyIT` and `ExceptionQueueIT`, the fixture files, the forced-failure double and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| TopicProbe | Service | Consumes each topic with its own consumer group and asserts one event per change, the key, the envelope, the payload and the schema version |
| DeliveryProbe | Service | Reads the delivery rows through the P2 admin read and asserts status, attempt count and next attempt |
| ConsumerDouble | Service | A configurable consumer that fails on demand, holds or does not hold the case step, and counts the deliveries it sees |
| CaseEffectProbe | Service | Reads the case route state and the task list and asserts the three signals and the open exception task |
| DecisionProbe | Service | Reads `rwb.decision-record.v1` and the decision read and asserts one record per move to the exception queue |
| FileStepProbe | Service | Asserts that the `win-dispatch` consumer produced a `deliverFile` run inside the 16:00 window and a FileDelivered event |
| ResidualAdapterScanner | Service | Reads the service interfaces, the module list and the deployment descriptors and fails on an in-process consumer call or a copied adapter |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The library tables are created by each service's DB story in its own schema; the harness reads them only through the P2 admin read and the P3 and P7 contracts.

**Configuration and reference data**

- The service list, the topic list with the retry and `.dlt` topics, the consumer group names, the queue names and the namespace.
- The consumer list per event type with the owner role and the case-step flag, read as parameters through the rwb-case parameters contract (DP-06).
- The retry settings (3 retries at 1, 5 and 15 minutes in DEV, a data value), the batch size of 200 and the wait intervals.
- The event types and the delivery statuses PENDING, RETRYING, DELIVERED and EXCEPTION, read as reference data through the rwb-case reference-data contract (DP-07).
- The synthetic case "RW-2026-000601", the notice "NT-SYN-0601", the deliveries "OBD-SYN-0001" and "OBD-SYN-0002" and the sequences 11 and 12.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H and C dependencies the DPs name — DP-09 with H RWB-PLT-TE006-CON, DP-06 and DP-07 with their C entries, DP-10, DP-15 and DP-19 with their platform H entries — stay with the platform and service stories this harness proves; this story carries no H, C or X dependency, and its I list names the two stories whose behaviour it exercises, RWB-P2-E1007-APP for the file step and RWB-PLT-TE006-APP for the library (Template and Rules §R5.4 and §R5.5).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Notice approval | Case "RW-2026-000601" with notice "NT-SYN-0601" approved in rwb-comms, one WIN_DISPATCH event, one delivery per consumer | AC1, AC2, TC-TE-006-01-ITG |
| Failing consumer | "win-dispatch" failing at 10:01, 10:02, 10:07 and 10:22, and a second variant failing once then succeeding | AC3, TC-TE-006-02-ITG, TC-TE-006-04-ITG |
| Rolled-back approval | The same approval with the transaction rolled back after the outbox write | AC1, TC-TE-006-03-ITG |
| Duplicate key and duplicate delivery | Two approvals with key "WIN_DISPATCH:NT-SYN-0601" and one event delivered twice to one consumer | AC4, TC-TE-006-05-ITG |
| 200 due deliveries | 200 due deliveries and two relay instances over one producer schema | AC5, TC-TE-006-06-ITG |
| Sequences 11 and 12 | CaseTransferred at sequence 11 and CaseStateChanged at sequence 12 with "ledger" failing on 11 | AC5, TC-TE-006-07-ITG, TC-TE-006-08-ITG |
| Resend pair | "OBD-SYN-0001" in EXCEPTION and "OBD-SYN-0002" in DELIVERED, plus a delivery ID that does not exist | AC6, TC-TE-006-09-ITG |
| Event with no case | An event without a case ID whose only consumer fails 4 times | AC6, TC-TE-006-10-ITG |
| Retry change | The retry delays changed to 2, 10 and 30 minutes before the run | AC3, TC-TE-006-11-ITG |
| Role set | RW-PLATADM, RW-DATASTEW and RW-COE with their Platform administration letters | AC6, TC-TE-006-12-ITG |
| Forced decision failure | The decision record refused at the exception move | AC3, TC-TE-006-13-ITG |

**Run order.** Preflight; one approval and its deliveries (AC1); the relay, the topic read and the file step (AC2); the forced failures, the three signals, the task and the decision record (AC3); the duplicate key and the duplicate delivery (AC4); order and the 200 deliveries (AC5); the resend pair, the `.dlt`, the role refusals and the 404 (AC6); the residual-adapter scan; cleanup of the DEV fixtures. A failing step stops the run and the report names the criterion, the service, the topic and the evidence.

**Done when.** The 19 test cases of section 16 pass on the real services in DEV and SIT, every change yields one event and one delivery per consumer, the order holds per case and consumer on the 200-delivery and two-sequence fixtures, the `.dlt` and its alert appear, the three signals change the case route state as R-UNI-33, R-UNI-35 and R-UNI-36 require, RESOLVE_OUTBOX_DELIVERY is open for the configured owner role, one decision record exists per move to the exception queue, and the residual-adapter scan finds no in-process consumer call.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | Task text when a delivery enters the exception queue | {interface} did not deliver {item} after {count} attempts. It is in the exception queue. |
| MSG-P2-022 | Resending a delivery that is not in EXCEPTION | Only an item in the exception queue can be sent again. |
| MSG-GEN-005 | A delivery is queued to send again | Saved. |
| MSG-P7-003 | The decision record cannot be written at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | The role lacks the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | The delivery or the case is not in the caller's scope | This case is not in your scope. |

The six texts are copied unchanged from RWB-TE-006 and section 14 of that story; this story adds no message text. Report lines of the harness are for developers and are not part of the message standard. In MSG-P2-001, {interface} is the consumer name and {item} the event type and case number.

##### 15. Screens and states

No screen in this story, and the harness renders nothing: it calls the admin, case, task and access endpoints and reads the topics directly. The task RESOLVE_OUTBOX_DELIVERY appears on SCR-09 Exception queue with MSG-P2-001 for the owner role when the case is in the exception queue, and the deliveries appear on SCR-44 Interface and job monitor; both screens belong to their own stories and are out of scope here. The states the harness observes are the delivery, relay, consumer, case route and run states of section 9.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-006-01-ITG | legacy AC1, BR1, BR3, BR7 | Integration | Notice NT-SYN-0601 approved at 10:00; the real `deliverFile` step replaces the stub |
| TC-TE-006-02-ITG | legacy AC2, BR5, BR6, BR8 | Integration | "win-dispatch" failing four times; the task, the record and RETRY_LIMIT_REACHED |
| TC-TE-006-03-ITG | legacy AC3, BR1 | Integration | The approval rolled back after the publish |
| TC-TE-006-04-ITG | legacy AC4, BR6 | Integration | "win-dispatch" failing once, then succeeding |
| TC-TE-006-05-ITG | legacy AC5, BR2 | Integration | Two approvals with key WIN_DISPATCH:NT-SYN-0601 |
| TC-TE-006-06-ITG | legacy AC6 | Integration | 200 due deliveries, two relay instances |
| TC-TE-006-07-ITG | legacy AC7, BR4 | Integration | Sequences 11 and 12, "ledger" failing on 11 |
| TC-TE-006-08-ITG | legacy AC8, BR3 | Integration | "ledger" fails and "reporting-feed" succeeds on one CaseAllocated event |
| TC-TE-006-09-ITG | legacy AC9 | Integration | Deliveries OBD-SYN-0001 in EXCEPTION and OBD-SYN-0002 in DELIVERED |
| TC-TE-006-10-ITG | legacy AC10 | Integration | An event with no case and a consumer failing four times; the alert |
| TC-TE-006-11-ITG | legacy AC11, BR11 | Integration | Retry delays changed to 2, 10 and 30 minutes before the run, read from the parameters contract |
| TC-TE-006-12-ITG | Access | Integration | RW-DATASTEW resends a delivery and is refused with MSG-P4-002 after the rwb-access check |
| TC-TE-006-13-ITG | Principle 5 | Integration | The decision record forced to fail at the exception move; the delivery stays RETRYING; MSG-P7-003 in the log; the incident |
| TC-ITG-TE006-01 | AC1, BR1 | Integration | One approval and one rolled-back approval in rwb_comms; two consumers |
| TC-ITG-TE006-02 | AC2, BR7, BR9, BR10 | End to end | One event on the owner topic and the `deliverFile` run inside the 16:00 window |
| TC-ITG-TE006-03 | AC3, BR5, BR6, BR8 | End to end | One consumer failing four times, one failing once; the three signals, the task and the record |
| TC-ITG-TE006-04 | AC4, BR2 | Integration | A duplicate idempotency key and a duplicate delivery to one consumer |
| TC-ITG-TE006-05 | AC5, BR4 | Integration | Sequences 11 and 12; 200 due deliveries on two relay instances |
| TC-ITG-TE006-06 | AC6, BR5 | Component | The resend pair, the missing delivery, the `.dlt` alert and the role refusal |

The legacy acceptance criteria of RWB-TE-006 are owned by RWB-PLT-TE006-APP, so the Covers cell of a legacy copy names those legacy AC numbers and not the criteria of this story; the legacy test case IDs are kept as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC6 carry TC-ITG-TE006-01 to TC-ITG-TE006-06.

##### 17. Guardrails

- No business value in code: the consumer list, the owner roles, the case-step flags, the retry counts and delays, the batch size and the alert route are parameters and reference data (DP-06, DP-07); the harness reads them through the rwb-case contracts.
- No personal data in events, workflow inputs, logs, fixtures or the report: case IDs, notice references, event IDs, delivery IDs, consumer names and codes only, and the admin read does not return the payload.
- Each service writes only its own schema and reads no other service's tables (DP-01); the harness reads the deliveries through the P2 admin read and the case and task through the P3 contract, and it never joins two schemas.
- No event and no delivery is deleted; a delivery leaves the exception queue only by being resent, and a correction of an event is a new event.
- One topic per service and one event type per business fact (BR9): a service that publishes another service's topic, or a producer that skips its outbox, fails the run.
- The retry topics and the `.dlt` are part of every topic's contract (BR9); a topic without them, or a dead letter with no alert, fails the preflight.
- No in-process consumer call and no copied adapter survives (BR10, DP-16); the residual-adapter scan is a regression test, not a one-off check.
- The harness never uses production data and never points at a production namespace; its forced failures exist only in DEV and SIT.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | `outbox_event`, `outbox_delivery` and `processed_event` in every service schema; the owner topics with their retry topics and `.dlt`; the relay JOB-11; the CaseWorkflow signals of `rwb-case`; RESOLVE_OUTBOX_DELIVERY; the `rwb.decision-record.v1` record of the move; the P2 admin resend | TC-TE-006-01-ITG to TC-TE-006-13-ITG, TC-ITG-TE006-01 to TC-ITG-TE006-06 |

The rules of the requirement are R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39 and R-UNI-40, as in RWB-TE-006 section 18.

##### 19. Out of scope

- The library itself: the contract of `outbox_event`, `outbox_delivery`, `processed_event` and `idempotency_key`, the statuses, the retry scheduling and the relay as code (RWB-PLT-TE006-CON, RWB-PLT-TE006-APP).
- The schema, the grants and the indexes of the four library tables in each service schema (each service's DB story; RWB-PLT-TE006-DB).
- The two admin endpoints in rwb-integration and their access checks (P2 by the Ownership Map; RWB-P2-E1007-APP).
- The consumers themselves — rwb-comms notices, the rwb-source-data ledger, the rwb-reporting projections, the rwb-case signals and the rwb-decision ingest — which this story exercises and owns none of.
- The topic provisioning, the retry and `.dlt` topics, the schema registry and the alert route (RWB-PLT-EVT and the operations stories).
- The `deliverFile` activity, the file run and the 16:00 WIN window (RWB-P2-E1007-APP, RWB-E2 outbound file stories).
- The SCR-09 exception queue and SCR-44 interface and job monitor screens (their own stories).
- The retry values, the alert routing and the consumer list as approved business data (DL11; GAP-0382).


## RWB-TE-007 Scheduled jobs on Quartz

Legacy disposition: Retired (D-RCV-60).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|

## RWB-TE-008 Decision log hash chain check

Legacy disposition: Split (rework).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE008-APP | App development | RWB-PLT-TPL | L-PLT-TPL-P | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-ITG-TE008-ITG | Integration | RWB-ITG-W1 | L-ITG-W1 | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE008-APP Decision log hash chain check
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE008-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP10, DP13, DP17, DP19 |
| Parallel lane | L-PLT-TPL-P |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1008-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-TE-008 for the 19-schema target. The decision log is no longer one central table: each of the 19 services writes its decision record in its own schema `rwb_<name>` in the same transaction as the state change, hash-links it to the record before, and publishes `DecisionRecorded` through its outbox, and rwb-decision ingests it into the central ledger and seals a daily fingerprint in write-once storage. The chain check therefore becomes a template capability — one reusable Temporal Schedule template in the workflow kit and one chain-check library in the service template, applied to every service's own local chain, with one instance for the central ledger — and Quartz JOB-14 becomes a Temporal Schedule owned by rwb-decision (DP-10). The data lake is removed (DP-17), so the legacy decision-log copy job is retired and the check waits for the day's ledger ingest instead of that copy. The legacy acceptance criteria are kept word for word and re-pointed, and every legacy value is unchanged (48,210 entries; chain_seq 30,005; 20,000 entries; chain_seq 12,001 and 40,350; 37 entries; 2 and 3 December 2026; 02:25; 04:00; 08:30; user U-9301). One criterion is added for the template, the per-service chain and the retired copy job, and the legacy contract table is rewritten: this platform story provides no REST operation of its own. The integration copy of the same legacy key is RWB-ITG-TE008-ITG. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As an **internal auditor (RW-AUDIT)**, I want **the hash chain of the decision log checked every night — on each service's own local chain and on the central ledger — with each run recorded against the last hash and a break, an incomplete run or an intact chain reported to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

The rework keeps the intent of RWB-TE-008 and changes the object of the check. In the monolith the decision log is one table in one `recovery` schema, one Quartz job walks it from `chain_seq` 1 to the highest value at its start, and a nightly copy to the data lake at 01:00 runs before it so that the check works on a settled copy. Arch v5 removes both assumptions: the log is written locally by each of the 19 services into its own schema in the same transaction as the state change and collected centrally by rwb-decision (slides 20 and 28), and there is no data lake at all (DP-17). A single nightly walk of one table is therefore no longer a description of the evidence.

What this story builds is the check as a capability rather than as one job: a reusable Temporal Schedule template in the workflow kit, a chain-check library in the service template, and the instance of that template that owns the central ledger in rwb-decision, which is where JOB-14 goes on the Ownership Map (owner P7, mechanism Schedule, 02:00). Every service generated from the template gets the same check over its own chain, with no new code, and the central ledger gets the one instance this story must land.

Everything a role sees or reads stays as the legacy story left it: the same roles, the same three report messages and the same refusal message, the same nightly start, the same latest start, the same batch size, the same rerun path and every legacy number. What changes is where the values come from and where the run record lives — the parameters come through the parameters contract of rwb-case, the calendar and the service list through its reference-data contract, the schedule through the workflow kit, and the run record is the workflow history of the Schedule instead of an ACE job run row.

##### 2. Business rationale

The decision log is evidence only while nobody can change an entry unseen. Each service refuses updates and deletes inside its own schema, but a change made outside the service, for example by a database administrator, is found only by recomputing the chain. This story runs that check every night after the day's ledger ingest, records each run with its last hash, and tells Compliance of a break, an incomplete run or an intact chain. It meets REQ-DRI-003 and NFR-035 and supports control CTL-06. The measure is a daily check with a same-day report: target 100 percent of nights.

The change the rework carries is the object of the check and the vehicle that runs it. Slide 28 puts the decision record inside each of the 19 services: the service writes the record and the change in one transaction, the record is chained to the one before it so gaps or edits show, rwb-decision reads the shared topic into the central ledger within 5 minutes, and a fingerprint of the ledger is sealed daily into write-once storage. Slide 20 gives every service the same block — its own schema, its own outbox and inbox, its own `decision_record` table, its own task queue and its own Schedules. Slide 29 makes the boundary hard: one login per service, grants on its own schema only, no cross-schema join and no cross-schema key, and a boundary test in every build. A chain therefore exists per service, not only centrally, and a check that reads one central table would miss a change in a service's own chain altogether. That is the reason the check becomes a template capability: the same recomputation runs inside the service that owns the chain, on its own schema, and the central ledger gets its own instance through the contract that publishes the ledger.

The vehicle changes with it. Quartz is replaced by Temporal Schedules in the owning service (DP-10; slide 44, JOB-14 owner rwb-decision, mechanism Schedule at 02:00), so the run record is the workflow history of that Schedule and no shared Quartz table is written. The data lake is removed (DP-17), so the 01:00 copy that the legacy check waits for no longer exists; the check waits instead for the day's central-ledger ingest to be reported complete, which is the signal that the ledger holds the business date's records. And the parameters are no longer values in code or in a catalog the job reads directly: they are read through the parameters contract of rwb-case (DP-06) and the calendar and service list through its reference-data contract (DP-07), so the same three legacy keys keep their values without a build to change them.

The estate this check protects is the one the 19 services write, and every service's chain is only as good as the code that computes it: one canonical-form implementation shared with the writer, which is the local decision-record library of RWB-PLT-E1027-CON (DP-03). The 19 schemas and their logins are database work outside this story. What this story owns is the check itself — its template, its library, its schedule definition, its report and its run states — and the proof that a break in any chain, a run that does not complete, or a service with no check at all is visible to Compliance the same day.

##### 3. Preconditions

- **RWB-PLT-E1071-CON** is published: the Temporal worker and SDK in the recovery module and the workflow kit that carries the Schedule templates (DP-10). The chain check is one template of that kit, not a second scheduler.
- **RWB-PLT-E1042-CON** is published: the parameters contract of rwb-case and its client library (DP-06). The three parameter keys and their values are read through it and are never values in code.
- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case and its versioned tables (DP-07). The business-date calendar and the list of the services whose chains are checked are reference rows read through it.
- **RWB-PLT-E1027-CON** is published: the local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03). The chain-check library recomputes the hash with the same canonical form that library writes, so the check and the writer cannot drift apart.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The readiness and run surface a role reads is a composite route behind gateway-bff; this story provides no route of its own.
- The **three service CON dependencies of the run** are published: **RWB-P3-E1042-CON** (parameters), **RWB-P3-E1043-CON** (reference data) and **RWB-P7-E1008-CON** (the decision log store, append-only and hash-chained, which publishes the central ledger's chain read). All three are consumed as published contracts and their fakes, so none blocks the build (Template and Rules §R5.4, C).
- rwb-decision (P7) ingests `DecisionRecorded` from `rwb.decision-record.v1` idempotently into the central ledger within 5 minutes and reports, per business date, whether the ingest for that date is complete (Arch v5 slides 20 and 28).
- Every service generated from the template writes its decision record in its own `rwb_<name>` schema in the same transaction as the state change, hash-links it to the record before, and publishes it through its outbox (Arch v5 slide 20; DP-03).
- The Compliance and PDPA officer group, the platform administrator group and the security administrator group are set in the ACE notification path, with RW-COMPLY as the owner of the three parameters.
- The schedule ID and its display name, the precise catch-up and backfill semantics of the Schedule, the completeness signal of the ledger ingest, where run records are read from, the retention of those run records and the report channel to Compliance are Not specified in the source documents (GAP-1437); the working defaults of section 13 are ASM-2528, ASM-2529 and ASM-2530.

##### 4. Flow

1. Temporal Schedule: the `ChainCheckSchedule` instance in rwb-decision fires at 02:00 Asia/Bangkok for the business date of the previous day, on the owner's task queue `rwb-decision` in namespace `rwb-recovery` (DP-10; Arch v5 slide 44, JOB-14 owner P7, time 02:00, mechanism Schedule).
2. ChainCheckRunner: reads `rwb.decision.chaincheck.start`, `rwb.decision.chaincheck.latest-start` and `rwb.decision.chaincheck.batch-size` through the parameters contract of rwb-case (DP-06), and the business-date calendar and the list of services whose chains are checked through the reference-data contract (DP-07).
3. LedgerIngestWait: holds the run until rwb-decision reports the business date's ledger ingest complete, and stops waiting at the latest start of 04:00, recording the state it saw. This replaces the wait for the retired decision-log copy job (DP-17; ASM-2529).
4. ChainStateReader: for each chain of the run, reads the highest `chain_seq` at the start and fixes it as the end of the run; entries appended later are checked the next night. A service's chain is read only by that service's own instance of the template, and the central ledger's chain only through `RWB-P7-E1008-CON` (DP-01).
5. ChainCheck: recomputes each entry's `entry_hash` from the canonical form of the shared library and compares each `prev_hash` with the entry before, over `chain_seq` 1 to the end, in batches of the configured batch size (1,000).
6. ChainCheck: counts every entry that fails and keeps the first, with its `chain_seq` and entry ID.
7. ChainCheckRunner: ends the run with the run record in the workflow history of the Schedule: type chain check, business date, chain, status, entries checked, last `chain_seq`, last `entry_hash`, result, first break `chain_seq` and entry ID, failing count, rerun, and the ingest state it waited on.
8. ChainCheckReporter: sends MSG-P7-007 to the Compliance group when the chain is intact, or MSG-P7-008 with an incident when it is broken.
9. ChainCheckReporter: on an error that stops the run, records status FAILED, alerts the platform administrator and sends MSG-P7-013 to the Compliance group.
10. Platform administrator: can rerun the check for the business date through the gateway-bff readiness view; a rerun is a new run and does not interrupt a run that is active.
11. Internal auditor: reads the run states and the last confirmed date through the gateway-bff composite route behind `RWB-PLT-N001-CON`, and never through a path of this story (DP-19).

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An entry does not match its hash or its prev_hash, in a service's local chain or in the central ledger | Run result BROKEN; first break and failing count recorded; incident; Compliance told | MSG-P7-008 | AC2, AC7 |
| X2 | The run stops on an error, for example a lost database connection | Status FAILED; platform administrator alerted; Compliance told the check did not complete | MSG-P7-013 | AC3 |
| X3 | The check is rerun for the same business date | A new run with the same checks; the report says it is a rerun; no second scheduled run starts | MSG-P7-007 or MSG-P7-008 | AC4 |
| X4 | The chain is empty | Result INTACT with count 0 and the genesis hash of 64 zeros | MSG-P7-007 | AC5 |
| X5 | The business date's ledger ingest is reported complete after 02:00 | The run waits up to 04:00, starts when the ingest completes, and records the ingest completion state it waited on where the legacy run recorded the copy end time | MSG-P7-007 or MSG-P7-008 | AC6 |
| X6 | Entries are appended while the run runs | They are outside this run and are checked the next night | None | AC8 |
| X7 | The day's ledger ingest is not complete for the business date by the latest start | The run starts at 04:00 with the note that the ingest was not complete, records the ledger portion it checked, and Compliance is told the check did not cover the whole date; the missing records stay open in the ledger | MSG-P7-013 | AC6, AC9 |
| X8 | A service generated from the template has no chain-check schedule, or a service of the reference list has no chain instance | The readiness view shows that service as not covered instead of intact; the platform administrator is alerted and Compliance is told the chain of that service was not confirmed; the coverage gap is raised to the platform team | MSG-P7-013 | AC9 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the workflow kit and the parameters, reference-data and decision-record contracts; the ledger chain read comes through a contract and its fake, so no service has to be built first; no screen |
| Negotiable | The schedule ID, the catch-up semantics, the ingest completeness signal, the run-record surface and the retention are working defaults recorded as assumptions; the three parameter values, the roles, the messages and the run states are fixed by the legacy story and NFR-035 |
| Valuable | A changed entry is found by the morning after it is changed, in whichever chain holds it, and a chain nobody checks is visible instead of silently trusted |
| Estimable | One workflow-kit template, one library in the service template, one ledger instance, one report, one readiness view, no table and no screen |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16, with the three contract fakes of section 12.8 and the schedule's own clock |

##### 7. Acceptance criteria

```gherkin
Feature: Decision log hash chain check

  Background:
    Given the environment is SIT with the synthetic decision log
    Given JOB-13 for business date 2 December 2026 ended at 01:40 on 3 December 2026

  Scenario: AC1 Chain intact (legacy RWB-TE-008 AC1)
    Given the rwb-case parameter contract mock returns rwb.decision.chaincheck.start=02:00, rwb.decision.chaincheck.latest-start=04:00 and rwb.decision.chaincheck.batch-size=1000
    Given the decision log holds 48,210 entries and none has been changed
    When JOB-14 runs at 02:00 on 3 December 2026
    Then the job run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance group

  Scenario: AC2 Break (legacy RWB-TE-008 AC2)
    Given the actions of the entry with chain_seq 30,005 were changed in the SIT database with the trigger disabled
    When JOB-14 runs
    Then the run result is "BROKEN" with first break chain_seq 30,005 and its entry ID
    Then the system raises an incident and MSG-P7-008 with the entry ID is sent to the Compliance group before 08:00 on 3 December 2026

  Scenario: AC3 A run that stops is reported (legacy RWB-TE-008 AC3)
    Given the database connection is closed in the test double after 20,000 entries
    When JOB-14 runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the system alerts the platform administrator group
    Then the system sends MSG-P7-013 to the Compliance group with the date of the last complete check, 2 December 2026

  Scenario: AC4 A rerun gives a new record and no second scheduled run (legacy RWB-TE-008 AC4)
    Given JOB-14 for business date 2 December 2026 failed at 02:20
    When test user "U-9301" holding RW-PLATADM reruns it from the job monitor at 08:30
    Then a second run record for business date 2 December 2026 is written with rerun true
    Then the system marks the report to Compliance as a rerun
    Then while the rerun is running a second start of JOB-14 is refused by the scheduler

  Scenario: AC5 An empty log is intact (legacy RWB-TE-008 AC5)
    Given the decision log holds no entry
    When JOB-14 runs
    Then the result is "INTACT" with entries checked 0 and last hash of 64 zeros

  Scenario: AC6 The job waits for the decision log copy (legacy RWB-TE-008 AC6)
    Given JOB-13 for business date 2 December 2026 is still running at 02:00 and ends at 02:25
    When JOB-14 fires at 02:00
    Then it starts the check at 02:25 and records the JOB-13 end time
    Then if JOB-13 has not ended by 04:00 the check starts at 04:00 with the note "JOB-13 not ended"

  Scenario: AC7 Several changed entries (legacy RWB-TE-008 AC7)
    Given the entries with chain_seq 12,001 and 40,350 were changed in the SIT database
    When JOB-14 runs
    Then the first break is chain_seq 12,001 and the failing count is 2
    Then one incident and one MSG-P7-008 report name both entry IDs

  Scenario: AC8 Entries written during the run (legacy RWB-TE-008 AC8)
    Given the log holds 48,210 entries when JOB-14 starts
    Given 37 entries are appended while it runs
    When the run ends
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries

  Scenario: AC9 The schedule, the per-service chain and the retired copy job (new, D-RCV-60)
    Given the ChainCheckSchedule template is in the workflow kit and the chain-check library is in the service template
    Given the rwb-case parameter contract mock returns rwb.decision.chaincheck.start=02:00, rwb.decision.chaincheck.latest-start=04:00 and rwb.decision.chaincheck.batch-size=1000
    Given the rwb-case reference-data contract mock returns the business-date calendar and the list of the 19 services
    When the schedule fires at 02:00 in Asia/Bangkok for the business date of the previous day
    Then the run starts on task queue rwb-decision as a Temporal Schedule and takes the start time, the latest start and the batch size from the parameter contract
    Then every service generated from the template recomputes its own local rwb_<name> chain through the chain-check library and reads no other service's schema
    Then the ledger instance reads the central ledger's chain through RWB-P7-E1008-CON
    Then the run waits for the business date's ledger ingest to be reported complete and waits for no copy job of the data lake
    When a chain is broken or the run does not complete
    Then ChainCheckReporter reports it to the Compliance group the same day
    Then no REST path of the monolith is called and this story provides no REST operation of its own
```

**Note on the criteria.** AC1 to AC8 are the legacy criteria of RWB-TE-008, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed. AC1 carries one extra `Given` as its first step, the parameter answer the run reads through the contract of rwb-case, and every legacy `Given`, `When` and `Then` of AC1 is kept. AC9 is the only new criterion and it carries no business value: it tests the template, the per-service chain, the ledger instance and the retired copy job of the target. JOB-13 is retired under DP-17, so the copy the legacy background and AC6 name no longer exists; the wait they describe is exercised against the business date's ledger ingest completeness signal, which is ASM-2529, and the gap of that replacement is GAP-1437.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The whole chain is recomputed every night, on every chain of the estate — each service's local `rwb_<name>` chain and the central ledger — and a break is reported to Compliance the same day | REQ-DRI-003; NFR-035; JOB-14; Arch v5 slides 20 and 28 |
| BR2 | Each entry's entry_hash is recomputed from the canonical form of the shared decision-record library and its prev_hash compared with the entry before; one canonical-form implementation is shared with the writer | Legacy RWB-E1-008, BR3 and BR4; DP-03; `RWB-PLT-E1027-CON` |
| BR3 | A run covers chain_seq 1 to the highest chain_seq of that chain at its start; entries appended later are checked the next night | This story (legacy BR3, per chain) |
| BR4 | The check runs for a business date after that date's ledger ingest is complete and starts no later than 04:00, at 02:00 by default; the three values are read through the parameters contract | Legacy batch.txt, daily timeline; parameters rwb.decision.chaincheck.*; DP-06; Arch v5 slide 44 |
| BR5 | A run that does not complete is reported to Compliance with the date of the last complete check | NFR-035 |
| BR6 | Only one run of a chain is active at a time and the Schedule never runs twice at once; a rerun is a new run and changes nothing else | Legacy RWB-TE-007; Temporal Schedule overlap policy (Arch v5 slide 44); DP-10 |
| BR7 | Start times and batch size are parameters, not code; the calendar and the list of chains are reference rows | Principle 1; DP-06; DP-07 |
| BR8 | The chain check is one capability: a single Temporal Schedule template in the workflow kit plus a chain-check library in the service template, generated into every service and applied to that service's own local chain, with one instance for the central ledger in rwb-decision; no service and no instance reads another service's chain or schema | Arch v5 slides 20, 28 and 29; DP-01, DP-03, DP-10; this story |

##### 9. State transitions

None. This story does not change a case status. A run moves from Waiting for the ledger ingest to Running, then to Completed with result INTACT or BROKEN, or to Failed, and a second start of a chain that is already running is Skipped.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The Temporal Schedule fires for the business date | None | Waiting for the ledger ingest |
| Waiting for the ledger ingest | rwb-decision reports the business date's ingest complete | Before the latest start of 04:00 | Running (the start and the ingest completion are both recorded) |
| Waiting for the ledger ingest | The latest start of 04:00 is reached | The ingest is not reported complete | Running with the note that the ingest was not complete (X7) |
| Running | Every entry of every chain of the run matches | None | Completed INTACT |
| Running | An entry does not match its hash or its prev_hash | None | Completed BROKEN (first break and failing count recorded) |
| Running | The run stops on an error | None | Failed (platform administrator alerted, Compliance told) |
| Running | A second start of the same chain is requested | A run is active | Skipped (the active run is not interrupted; the request is recorded) |
| Completed or Failed | The platform administrator reruns the business date | The earlier run has ended | Running (a new run, marked as a rerun) |
| Any state | The service has no chain-check instance | The service is on the reference list | Not covered (shown by the readiness view, X8) |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | The identity the check runs under: in the legacy one service identity that reads the log, in the target each instance runs under the login of the service that owns the chain, and the central-ledger instance reads the ledger through `RWB-P7-E1008-CON`; no instance writes an entry |
| RW-COMPLY Compliance and PDPA officer | Receives every report and the incident; owns the three parameters and their values through the parameters contract (DP-06) |
| RW-AUDIT Internal audit | Reads the run states and the last confirmed date through the gateway-bff composite route; may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts and coverage alerts; reruns a business date; reads the readiness and run surface behind gateway-bff |
| RW-SECADM Security administrator | Receives the break incident with Compliance |
| No role | May read another service's chain or schema, repair or rewrite an entry, start a second run of a chain that is running, change a parameter value in code, or reach the check through a path of the monolith |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |
| DF-DEC-028 | decision_log_entry | chain_seq | Read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The run result is written to the workflow history of the Schedule, not to a recovery table.

`decision_log_entry` now lives in `rwb_decision` (P7 rwb-decision, Ownership Map, Arch v5 slides 29 and 41), and each service's decision records live in that service's own `rwb_<name>` schema. This story reads a service's chain only inside that service's own instance of the template, under that service's own login, and it never reads across a schema boundary (DP-01; Arch v5 slide 29). The central ledger's chain is read through `RWB-P7-E1008-CON`, which is the owner's contract, not a table of the owner. The run record is the Temporal workflow history of the Schedule and its activities — status, business date, chain, entries checked, last `chain_seq`, last `entry_hash`, result, first break, failing count, rerun and the ingest state it waited on — and it is not an ACE job run row and not a table this story creates.

Where the run records are read from, how long they are kept and which retention the schedule history of the `rwb-recovery` namespace carries are Not specified in the source documents (GAP-1437); the working default of section 13 and ASM-2530 is the workflow history of the Schedule plus the gateway-bff readiness view, with no new platform table.

##### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it has no REST base, no topic, no task queue and no schema of its own, and none is invented for it. The one instance this story lands runs inside rwb-decision (P7), on that service's queue, under that service's login.

###### 12.1 REST operations provided

None. This platform story provides no REST operation, no REST base, no topic, no task queue and no schema of its own, and none is invented. The check is a Temporal Schedule and its activities, and the readiness and run surface a role reads is a gateway-bff composite route behind `RWB-PLT-N001-CON` (DP-19), owned by the gateway, not by this story.

###### 12.2 REST operations consumed

None as a path of this story: the ledger chain read and the two parameter and reference-data reads are consumed as published contracts and their fakes, and no path, version or payload of them is repeated here.

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1042-CON` (the platform contract behind it is `RWB-PLT-E1042-CON`) | P3 rwb-case | The parameter catalog: `rwb.decision.chaincheck.start`, `rwb.decision.chaincheck.latest-start` and `rwb.decision.chaincheck.batch-size`, with their values, their type and their effective dating (DP-06) |
| `RWB-P3-E1043-CON` (the platform contract behind it is `RWB-PLT-E1043-CON`) | P3 rwb-case | The business-date calendar and the list of services whose chains the run checks, with the reference-data version in force (DP-07) |
| `RWB-P7-E1008-CON` | P7 rwb-decision | The central ledger's chain as the owner publishes it: the highest `chain_seq`, the entries in `chain_seq` order with `prev_hash` and `entry_hash`, and the completeness state of the ingest for a business date (DP-01, DP-03) |

The ledger chain read is one hop to the owning service on that service's own base with the 2 s client budget (DP-11, DP-13); the path itself belongs to `RWB-P7-E1008-CON`.

###### 12.3 Events published

None. The check publishes no event: it reads chains and reports through the ACE notification path. The decision records it checks travel on the shared topic `rwb.decision-record.v1`, produced by the owning services through their outboxes and consumed by rwb-decision (Arch v5 slides 20 and 28); this story produces nothing on a topic and owns no topic.

###### 12.4 Events consumed

None. The run waits on the ledger ingest completeness state of the business date, which it reads through `RWB-P7-E1008-CON`, and not on a topic subscription; the completeness signal itself is a gap (GAP-1437; ASM-2529).

###### 12.5 Workflows and activities

| Workflow or activity | Where it runs | What it does |
|---|---|---|
| `ChainCheckWorkflow`, from the workflow-kit template `ChainCheckSchedule` | namespace `rwb-recovery`; on task queue `rwb-decision` for the ledger instance, and on each generated service's own queue for that service's instance | Wraps the run: waits for the ingest, fixes the end `chain_seq` per chain, drives the batch check, ends the run record and hands the result to the report |
| Activity `ChainCheck` | the same queue | Recomputes `entry_hash` with the shared canonical form and compares `prev_hash`, in batches of the configured size; counts every failing entry and keeps the first |
| Activity `LedgerChainRead` | the same queue | Reads the central ledger's chain and the business date's ingest completeness through `RWB-P7-E1008-CON`; used by the ledger instance only |
| Activity `ChainReport` | the same queue | Sends MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group and raises the incident on a break |

The wait of step 3 has no activity of its own: it is a durable timer in the workflow plus the ingest completeness answer read on each poll, so a run holds no worker slot while it waits.

###### 12.6 Schedules

| Item | Value |
|---|---|
| Template | `ChainCheckSchedule`, a specialisation of the workflow kit's Scheduled job template (Temporal design slide 12, layer L3; DP-10) |
| Schedule ID and display name | Not specified in the source documents (GAP-1437); `chain-check-daily` and "Daily decision log hash chain check" are the working defaults of ASM-2528 |
| Instance owner | rwb-decision (P7), per the Ownership Map row for JOB-14 and Arch v5 slide 44 (owner rwb-decision, time 02:00, mechanism Schedule) |
| Cron | `0 0 2 * * ?` in Asia/Bangkok, the legacy cron kept; the start time is read through `rwb.decision.chaincheck.start` (02:00) and is a parameter, not code |
| Latest start | 04:00, read through `rwb.decision.chaincheck.latest-start`; the run starts at the latest start and records a late or incomplete ingest |
| Batch size | 1,000, read through `rwb.decision.chaincheck.batch-size` |
| Catch-up and backfill | One business date only, as a parameter; a missed run is caught up once for the most recent business date and no run chains several missed days together; a rerun of an older business date is an explicit rerun by business date (GAP-1437; ASM-2528) |
| Overlap policy | One run at a time: a start while a run is active is skipped and the active run is not interrupted, which is the legacy DisallowConcurrentExecution carried over and the overlap policy of Arch v5 slide 44 (AC4, BR6) |
| Per-service instances | Generated with each service from the template at 02:00 in that service's own namespace queue and over that service's own chain; this story publishes the template and lands only the ledger instance |

###### 12.7 Tables owned

None. This story owns no table, creates no schema and writes no row: the run record is the workflow history of the Schedule, the ledger tables are rwb-decision's, and each service's `decision_record` table is that service's own (DP-01; Arch v5 slides 20 and 29).

###### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case parameters fake | `RWB-P3-E1042-CON` behind `RWB-PLT-E1042-CON` | `rwb.decision.chaincheck.start=02:00`, `rwb.decision.chaincheck.latest-start=04:00` and `rwb.decision.chaincheck.batch-size=1000`, with a changed latest start for the X7 case (AC1, AC6, AC9, TC-TE-008-06, TC-PLT-TE008-APP-10) |
| rwb-case reference-data fake | `RWB-P3-E1043-CON` behind `RWB-PLT-E1043-CON` | The business-date calendar with 2 December 2026 as the date of the run, a reference-data version, and the list of the 19 services; the same list with one service removed for the X8 case (AC9, TC-PLT-TE008-APP-10) |
| rwb-decision ledger fake | `RWB-P7-E1008-CON` | A chain of synthetic entries with `prev_hash` and `entry_hash`, the highest `chain_seq`, a changed entry, an empty chain, and a business date whose ingest is reported complete late and then not at all (AC1, AC2, AC5, AC6, AC7, AC9) |

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None provided, 1 contract consumed | No REST operation of this story; the ledger chain read is consumed as `RWB-P7-E1008-CON`, one hop, 2 s (DP-11, DP-13) |
| Kafka | None | The check publishes and consumes no event of its own; the records it checks travel on `rwb.decision-record.v1`, produced by the owning services, and the ledger ingest that completes them is rwb-decision's |
| Temporal | 1 Schedule, 3 activities | The `ChainCheckSchedule` template and its instance in rwb-decision, the workflow `ChainCheckWorkflow`, and the activities `ChainCheck`, `LedgerChainRead` and `ChainReport` on the owner's queue (DP-10) |
| File | None | The daily ledger fingerprint in write-once storage is rwb-decision's and is out of scope; this story writes no file |

##### 13. Solution plan

**Package.** The chain-check library goes into the service-template module that every service is generated from (`recovery-service-template`, Java package `th.co.scb.ace.workbench.recovery.template.chaincheck`), and the Schedules template goes into the workflow kit (`recovery-workflow-kit`, platform-owned, layer L3 of the Temporal layer model, Temporal design slide 12). The ledger instance is generated into rwb-decision from the same two artifacts, and this story adds no second scheduler.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | The monolith REST base | `/api/recovery/<short>/v1` | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| ChainCheckScheduleTemplate | Workflow-kit template | The reusable Schedule template: cron, latest start, batch size, catch-up and overlap policy as parameters, with no business term in its interface (BR7, BR8; DP-10) |
| ChainCheckRunner | Workflow and activity pair | Fixes the end `chain_seq` per chain, drives the batch recomputation, ends the run record in the workflow history (BR1, BR3) |
| ChainStateReader | Library | Reads one chain in `chain_seq` order inside the schema of the service the instance runs in, and the central ledger through `RWB-P7-E1008-CON`; never reads across a schema boundary (BR2, BR8; DP-01) |
| LedgerIngestWait | Workflow step | Durable timer plus the ingest completeness answer of the business date, stopping at the latest start (BR4, X5, X7) |
| ChainCheckReporter | Activity | Sends MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group and raises the incident on a break (BR1, BR5) |
| ChainCheckRunView | Read model behind gateway-bff | The readiness and run surface: per chain and business date, the last run, its result, its last `entry_hash` and the date of the last complete check; it calls the owning service through the composite route and holds no table (DP-19) |

**Database.** No new business table, no schema and no Flyway migration. The check reads an entry table that the owning service already has, and its run record is the workflow history of the Schedule; nothing is written except the report and the incident, which the ACE notification path and the incident channel own.

**Configuration and reference data.**

- `rwb.decision.chaincheck.start=02:00`, `rwb.decision.chaincheck.latest-start=04:00` and `rwb.decision.chaincheck.batch-size=1000`, read through the parameters contract of rwb-case (DP-06; `RWB-PLT-E1042-CON`, `RWB-P3-E1042-CON`) and owned by RW-COMPLY; the values are the legacy ones and are never values in code.
- The business-date calendar and the list of services whose chains are checked, read as reference rows with their version through the reference-data contract (DP-07; `RWB-PLT-E1043-CON`, `RWB-P3-E1043-CON`); the reference-data version in force is recorded with the run.
- The ledger chain and the business date's ingest completeness, read through `RWB-P7-E1008-CON`.
- The schedule parameters of the template: the schedule ID `chain-check-daily`, the display name "Daily decision log hash chain check", the catch-up rule and the overlap policy, the working defaults of ASM-2528 (GAP-1437).
- Feature flag: `rwb.decision.hash-check`, unchanged from the legacy story.

**Build steps**

1. Add the `ChainCheckSchedule` template to the workflow kit: cron, latest start, batch size, catch-up and overlap policy as parameters, one run at a time (BR6, BR7; DP-10).
2. Build ChainStateReader and the shared canonical-form call against `RWB-PLT-E1027-CON`, with the boundary rule that an instance reads only its own schema or the ledger contract (BR2, BR8; DP-01).
3. Build ChainCheckRunner and the `ChainCheck` activity with the batch walk and the fixed end `chain_seq`; tests for AC1, AC5 and AC8.
4. Build the counting of every failing entry and the first break; tests for AC2 and AC7.
5. Build LedgerIngestWait with the 04:00 latest start and the incomplete-ingest note; test AC6 and X7 against the ingest completeness fake.
6. Build ChainCheckReporter with the three messages and the incident; tests for AC1, AC2 and AC3.
7. Land the ledger instance in rwb-decision with `LedgerChainRead` on the owner's queue, and generate the per-service instance from the template in a throwaway service; test the rerun path and the concurrency guard for AC4 and the coverage case X8 for AC9.
8. Run the timing check on 10 million synthetic entries against a 60 minute budget (assumed; DL11), and record the schedule ID, the catch-up rule and the run-record retention as the open items of GAP-1437.

**Done when.** The ten test cases of section 16 pass, the template has produced a chain-check instance for the central ledger and for one generated service, a break in either chain reaches the Compliance group the same day, a run that waits on the ingest starts at the latest start and says so, a service with no instance shows as not covered, and the run book of the legacy JOB-14 has been rewritten for the Schedule and the readiness view (RWB-E1-056).

The schedule ID, the catch-up and backfill semantics, the ingest completeness signal, the run-record surface and retention, and the report channel to Compliance are Not specified in the source documents (GAP-1437); the working defaults are ASM-2528, ASM-2529 and ASM-2530, and the solution architect closes them before the template is published.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-007 | The chain is intact (new) | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. |
| MSG-P7-008 | The chain is broken | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-013 | The run did not complete (new) | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from RWB-TE-008 and this story adds no message text. In MSG-P7-007, MSG-P7-008 and MSG-P7-013 the {date} is the business date of the run and, where the run covers more than one chain, the report names the chain and the service that owns it; the entry ID and the `chain_seq` are the only identifiers reported. Thai text for each message follows DL10; the proposed Thai for the two new messages is in the additions file.

##### 15. Screens and states

No screen in this story, and no new screen state. The run states of section 9 are read on the readiness and run surface, which is a gateway-bff composite route behind `RWB-PLT-N001-CON` (DP-19) over the owner's read model and the workflow platform's visibility: per chain and business date, the last run, its result, the last `entry_hash`, the date of the last complete check, and the services that have no chain-check instance. This story invents no route, no path and no screen; the composite route and its operations belong to the gateway and to the stories that publish them.

Compliance receives each report by the ACE notification path, as in the legacy story, and never from a screen of this story.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-008-01 | AC1, BR1, BR2 | Component | 48,210 synthetic entries, none changed |
| TC-TE-008-02 | AC2, BR1 | Component | One entry changed in SIT with the trigger disabled |
| TC-TE-008-03 | AC3, BR5 | Component | Connection closed after 20,000 entries |
| TC-TE-008-04 | AC4, BR6 | Component | Failed run, then a rerun at 08:30 |
| TC-TE-008-05 | AC5 | Component | Empty log |
| TC-TE-008-06 | AC6, BR4 | Component | JOB-13 ending at 02:25; JOB-13 not ended by 04:00 |
| TC-TE-008-07 | AC7, BR2 | Component | Two entries changed |
| TC-TE-008-08 | AC8, BR3 | Component | 37 entries appended during the run |
| TC-TE-008-09 | Access | End to end | A role without the right is refused with MSG-P4-002 |
| TC-PLT-TE008-APP-10 | AC9, BR8 | Integration | The template and the library, the three contract fakes, the Schedule at 02:00, one generated service with a broken local chain, and a business date whose ledger ingest completes late and then not at all |

The nine legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the legacy System rows TC-TE-008-01 to TC-TE-008-08 become Component, and the legacy Access row TC-TE-008-09 becomes End to end. TC-PLT-TE008-APP-10 is the new row for AC9. The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same TC ID.

##### 17. Guardrails

- No business value in code: the three parameter values, the calendar and the list of chains are read through the contracts of rwb-case (DP-06, DP-07) and are owned by RW-COMPLY and the reference-data owner.
- No personal data in logs, reports, tests or prompts: the run record, the report and the incident name entry IDs, `chain_seq`, counts and hashes only, never a value of an entry.
- No read of another service's schema: an instance reads the chain of the service it runs in, and the central ledger only through `RWB-P7-E1008-CON`; a boundary test fails a cross-schema reference (DP-01).
- The check never writes to an entry table and never repairs an entry: a broken chain is reported, not corrected.
- One canonical-form implementation, shared with the decision-record library, so the writer and the check cannot drift apart (DP-03; BR2).
- The Schedule never runs twice at once: one run at a time per chain, and a second start is skipped without interrupting the active run (BR6).
- No path of the monolith is called and none is kept, and this platform story adds no REST operation, no topic and no schema of its own (DP-13).
- A chain nobody checks is a visible state: a service with no instance of the template is shown as not covered and reported, never treated as intact (X8).

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-003 | Hash chain checked every day, break reported to Compliance the same day | Business Requirements Epic 1, section 3.7; Business Requirements Program, sections 5.7 and 6.6 | FEAT-DRI-01 (the store and the ledger this check verifies) | 17 Run the decision center | BR1 to BR8 | TC-TE-008-01 to TC-TE-008-09, TC-PLT-TE008-APP-10 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | A chain is read inside the service that writes it, and the central ledger only through its owner's contract; no cross-schema read | TC-TE-008-01, TC-PLT-TE008-APP-10 |
| DP-03 | Template and Rules §R5.5; Arch v5 slides 20 and 28 | The check uses the canonical form of the local decision-record library and reads the records the services publish on `rwb.decision-record.v1` | TC-TE-008-01, TC-TE-008-02 |
| DP-06 | Template and Rules §R5.5 | The start time, the latest start and the batch size are read through the parameters contract and are never values in code | TC-TE-008-01, TC-TE-008-06, TC-PLT-TE008-APP-10 |
| DP-07 | Template and Rules §R5.5 | The business-date calendar and the list of chains are reference rows read through the reference-data contract, with a version | TC-TE-008-06, TC-PLT-TE008-APP-10 |
| DP-10 | Template and Rules §R5.5; Arch v5 slide 44; Temporal design slide 12 | Quartz JOB-14 becomes a Temporal Schedule from the workflow kit, owned by rwb-decision, 02:00 | TC-TE-008-01, TC-TE-008-04, TC-PLT-TE008-APP-10 |
| DP-13 | Template and Rules §R5.5 | No base path of the monolith remains and this story provides no REST operation of its own | TC-PLT-TE008-APP-10 |
| DP-17 | Template and Rules §R5.5; Ownership Map (JOB-13) | The data lake is removed, the decision-log copy job is retired, and the check waits for the ledger ingest completeness instead | TC-TE-008-06, TC-PLT-TE008-APP-10 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 20 | The readiness and run surface a role reads is a gateway-bff composite route, and this story provides no route of its own | TC-TE-008-09, TC-TE-008-04 |
| Arch v5 slide 20 | Every service writes its own schema plus outbox and inbox, its own `decision_record`, its own queue and its own Schedules | The check is generated into every service and runs on that service's own chain | TC-PLT-TE008-APP-10 |
| Arch v5 slide 28 | Recorded locally at once, chained, collected centrally within 5 minutes, sealed daily in write-once storage | Each chain is checked where it is written, and the ledger gets the instance that owns JOB-14 | TC-TE-008-01, TC-PLT-TE008-APP-10 |
| Arch v5 slide 29 | One schema and one login per service; no cross-schema join or key; boundary test in every build | The check reads one chain per instance and never across a schema boundary | TC-PLT-TE008-APP-10 |
| Arch v5 slide 44 | The job map: JOB-14 hash-chain check, 02:00, owner rwb-decision, mechanism Schedule; JOB-13 ingest is continuous on Kafka | The Schedule and its owner, the overlap policy, the catch-up window, and the retirement of the copy the check used to wait for | TC-TE-008-04, TC-TE-008-06, TC-PLT-TE008-APP-10 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON | Contract | H: the decision-record library, the parameters contract, the reference-data contract, the workflow kit and the gateway-bff route contract this story builds against |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON, RWB-P7-E1008-CON | Contract | C: the parameters and reference-data contracts consumed at run time, and the ledger chain read of rwb-decision |
| RWB-ITG-TE008-ITG | Integration | The integration copy of RWB-TE-008; it exercises this check across the chains and owns none of it |
| JOB-13 (retired, DP-17) | Legacy job | The decision log copy to the data lake, which no longer exists; the wait it carried is replaced by the ledger ingest completeness signal |

##### 19. Out of scope

- The store, the hash computation and the on-demand verifier: the legacy RWB-E1-008, now rwb-decision with `RWB-P7-E1008-CON`.
- The check of each entry returned by an audit query (RWB-E2-005 in the legacy numbering).
- The decision log copy to the data lake (RWB-E1-014, JOB-13), retired under DP-17.
- The central ledger ingest and the daily write-once seal: rwb-decision (P7) owns both, and this story reads the ledger's chain and its ingest completeness through the contract only.
- The broken-chain control view of the administration screens (Epic 8, FEAT-ADM-10).
- The integration copy of this legacy key, RWB-ITG-TE008-ITG, which exercises the check end to end across the chains.
- The 19 schemas, the 19 logins and their grants: RWB-PLT-NF06-DB and the per-service database stories.
- The contents of `RWB-PLT-E1027-CON`, `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON` and `RWB-P7-E1008-CON`; this story builds against them and adds no path, no topic and no table.


### RWB-ITG-TE008-ITG Decision log hash chain check — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-008 for the wave-1 integration epic. The Quartz job JOB-14 becomes a 02:00 Temporal Schedule in rwb-decision with overlap policy SKIP and a catch-up window, the wait for the nightly copy of the decision log (JOB-13) becomes a wait for the continuous Kafka ingest watermark of `rwb.decision-record.v1`, the run record names that watermark instead of a copy job end time, and the check is proved on the real central ledger and the real local chain of every wave-1 service rather than on a fake. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE008-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-008 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP06, DP07, DP10, DP13, DP17, DP19 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P7-E1008-APP, RWB-PLT-TE008-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

##### 1. Story

As a **tech lead**, I want **the nightly decision-log hash-chain check exercised end to end on the real services and the real Schedule: JOB-14 firing at 02:00 as a Temporal Schedule in rwb-decision, waiting for the continuous ingest of `rwb.decision-record.v1` to reach the producer watermark, recomputing every `entry_hash` and comparing every `prev_hash` from chain_seq 1 to the highest chain_seq at the start in the central ledger and in every wave-1 local chain, naming a break in one service's local chain and a gap between a local record and the ledger, and telling Compliance the same day**, so that **a changed entry or a missing record is found by the morning after it happens on the architecture that will run it, not on a monolith job and not on a fake**.

##### 2. Business rationale

The decision log is evidence only while nobody can change an entry unseen. The legacy story runs JOB-14 on Quartz, waits for the nightly copy of the log to the data lake (JOB-13), and reads one log in the recovery schema. In the target none of those three things exists as the legacy story describes them: each of the 19 services writes its own decision record in its own schema in the same transaction as its state change and publishes `DecisionRecorded` (Arch v5 slides 20 and 28, steps 1 and 2; Temporal design slides 11 and 14), rwb-decision collects the record into the central ledger it owns within 5 minutes (Arch v5 slide 28, step 3; ADR-022, DP-03), JOB-13 is continuous Kafka ingest rather than a 01:00 copy to a data lake (Arch v5 slide 44; DP-17, RWB-E1-014 retired), and JOB-14 is a Temporal Schedule at 02:00 with overlap policy SKIP and a catch-up window instead of a Quartz job (Arch v5 slides 14 and 44; Temporal design slide 16; DP-10). It meets REQ-DRI-003, supports control CTL-06 and is measured by one daily check with a same-day report.

Those pieces are proven by no single service story. A chain that is recomputed over the ledger alone misses a break in a service's local chain; a run that starts before the ingest has caught up reports a gap that is only lateness; a break that is found but not named, or named with a personal value, fails the audit; and a run that stops without a report leaves Compliance believing the chain was confirmed. Only the integration level, on the real services, the real topic and the real Schedule, can prove that all of them hold together.

##### 3. Preconditions

- The nine wave-1 services are deployed in DEV and SIT, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- Every wave-1 schema holds its local `decision_record` with `chain_seq`, `prev_hash`, `entry_hash` and the append-only rule, written in the same transaction as its state change (DP-03; the DB story of each service; RWB-P7-E1008-DB for rwb_decision).
- rwb-decision holds `decision_log_entry` with `chain_seq`, `prev_hash`, `entry_hash` and `corrects_entry_id`, the chain lock and the canonical form; the service role holds INSERT and SELECT and no UPDATE or DELETE grant (RWB-P7-E1008-APP, RWB-P7-E1008-DB).
- The topic `rwb.decision-record.v1` exists with its retry and `.dlt` topics, the consumer of rwb-decision ingests into the ledger within 5 minutes, and queue `rwb-decision` is registered in namespace `rwb-recovery` (RWB-PLT-EVT, RWB-PLT-WF; Arch v5 slides 20, 28 and 42; Temporal design slide 11).
- The 02:00 Schedule of JOB-14 is registered in rwb-decision by the release and can be started once by the harness through the Temporal client; the platform story of the same legacy key, RWB-PLT-TE008-APP, builds the scheduled-job and run-record parts of the check on the service template, and the rwb-decision story RWB-P7-E1008-APP builds the workflow, the ingest and the ledger.
- The run record is read through `GET /api/recovery/source-data/v1/admin/jobs` and a rerun is started through `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`, both owned by P1 rwb-source-data (Ownership Map); the Schedule itself is started by the harness with the same input the cadence uses.
- rwb-access answers the authorise call and holds the test roles RW-COMPLY, RW-AUDIT, RW-SECADM and RW-PLATADM with their Platform administration letters (RWB-P4-E1008-APP).
- The Compliance and PDPA officer group and the platform administrator group are reachable through the ACE Common notification path, and the break incident is raised with Compliance (legacy RWB-TE-008 sections 10 and 14).
- The parameters of the check are read through the parameters contract of rwb-case (DP-06) and the decision codes, outcome codes and approval levels used by the fixtures are read through its reference-data contract (DP-07), never as values in the harness code: start 02:00, latest start 04:00, batch size 1,000, all Asia/Bangkok.
- Which chains the run covers, what the ingest watermark is and where the incident and the report go across services is Not specified in the source documents (GAP-0380; ASM-0549, ASM-0550).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the two integration stories and the real Schedule, and it never substitutes a fake for a real service.

##### 4. Flow

1. Harness: reads the service list, the topic, the retry and `.dlt` topics, the queue, the namespace, the Schedule name and the two read paths from configuration, and runs the preflight of section 13; a missing local `decision_record`, ledger table, chain object, topic, retry topic, task queue or Schedule stops the run before any test.
2. Schedule: `decisionChainCheck` fires JOB-14 at 02:00 Asia/Bangkok for business date 2 December 2026, the previous day, on queue `rwb-decision`, with overlap policy SKIP and a catch-up window (Arch v5 slides 14 and 44; Temporal design slide 16).
3. Workflow (`ChainCheckWorkflow`): reads the ingest watermark of `rwb.decision-record.v1` into the ledger; if the ledger is behind the producer watermark it re-reads every 5 minutes and starts the check when the watermark is reached, and it starts at 04:00 with the note "ingest not at watermark" when the watermark is not reached by then.
4. Workflow: reads the highest `chain_seq` at the start in the central ledger and in every wave-1 local chain, and fixes each of them as the end of the run for that chain; entries appended later are checked the next night.
5. Workflow: recomputes every `entry_hash` from the canonical form and compares every `prev_hash` with the entry before, from chain_seq 1 to the highest at the start, in batches of 1,000, for the central ledger and for each wave-1 local chain.
6. Workflow: counts every entry that fails in each chain, keeps the first per chain, and names the service and the chain of each break by entry ID and chain_seq.
7. Workflow: reconciles the local records with the ledger entries by entryId and names any local record with no ledger entry as a gap, and any ledger entry with no local record as an orphan.
8. Workflow: writes the run record with type JOB-14, business date, status, the ingest watermark it started on, and its checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID per chain, failing count, gap count and rerun.
9. Workflow: sends MSG-P7-007 to the Compliance role (RW-COMPLY) when every chain is intact, or MSG-P7-008 with an incident naming the first break per chain and every gap when one is found.
10. Workflow: on an error that stops the run, records status FAILED, alerts the platform administrator group and sends MSG-P7-013 to Compliance with the date of the last complete check.
11. Platform administrator: reruns JOB-14 for the business date through `POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun`; a rerun is a new run record with rerun true and changes nothing else, and the Schedule refuses a second concurrent start by its SKIP policy.
12. Harness: reads the run record through `GET /api/recovery/source-data/v1/admin/jobs` and the entries through the two decision reads, times the incident and MSG-P7-008 from the run start, runs the 10,000,000-entry run against the 60 minute budget, reconciles one local record to one event to one ledger entry, and writes the run report.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An entry does not match its `entry_hash` or its `prev_hash`, in the ledger or in a service's local chain | The run result is BROKEN for that chain; the first break and the failing count are recorded with the service and the chain; an incident is raised and Compliance is told | MSG-P7-008 | AC2 |
| X2 | The run stops on an error, for example a lost database connection | Status FAILED with the entries checked so far; the platform administrator group is alerted; Compliance is told the check did not complete | MSG-P7-013 | AC5 |
| X3 | The job is rerun for the same business date | A new run record with the same checks and rerun true; the report says it is a rerun; the SKIP policy refuses a second concurrent start | MSG-P7-007 | AC4 |
| X4 | A chain is empty | Result INTACT with count 0 and the genesis hash of 64 zeros for that chain | MSG-P7-007 | AC1 |
| X5 | The ingest has not reached the producer watermark at 02:00 | The workflow waits, re-reading the watermark every 5 minutes, and starts at 04:00 at the latest, recording that the watermark was not reached | MSG-P7-007 or MSG-P7-008 | AC3 |
| X6 | Entries are appended while the run is in progress | They are outside this run's end chain_seq and are checked the next night | None | AC3 |
| X7 | A local record has no ledger entry because its event is still in the retry topic | The gap is named by service, entry ID and chain_seq while both chains stay INTACT; an incident is raised and the next run closes it | MSG-P7-008 | AC4 |
| X8 | A role without Platform administration U calls the rerun | rwb-access refuses through the authorise call and the rerun answers 403 | MSG-P4-002 | AC5 |

X1 to X6 are the exception paths of the legacy story carried onto the real services and the real Schedule; X7 is the cross-service gap that only the split local-record and central-ledger design can produce; X8 is the authority of the legacy story in testable form. The incident and report route across services is Not specified in the source documents (GAP-0380; ASM-0549).

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test project of its own; it needs the two integration stories and the Schedule, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, retry counts and report layout are configuration; the chain values, the message IDs, the times and the run order are fixed by the legacy story |
| Valuable | Proves across services what no single story can prove: the ledger and every local chain checked, a break named, a gap named, a stopped run reported |
| Estimable | One harness project, five test classes, four fixtures, three tamper steps, one Schedule start and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a run record, a workflow result, an incident, a message, a response code |

##### 7. Acceptance criteria

```gherkin
Feature: Decision log hash chain check, proven across the wave-1 services and the real Schedule

  Background:
    Given the environment is DEV with synthetic data
    Given the nine wave-1 services run with their own schemas and login
    Given the central ledger in rwb_decision and one local decision_record chain in each wave-1 service schema
    Given the chain starts at chain_seq 1 with prev_hash of 64 zeros in each of them

  Scenario: AC1 The 02:00 Schedule checks the ledger and every wave-1 local chain and reports an intact chain (new, D-RCV-60)
    Given the central ledger holds 48,210 entries for business date 2 December 2026, none changed
    Given every wave-1 local chain holds the entries it published on rwb.decision-record.v1, none changed
    When decisionChainCheck fires at 02:00 on 3 December 2026 on queue rwb-decision as JOB-14 with overlap policy SKIP
    Then the run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash, recomputed in batches of 1,000 from chain_seq 1
    Then every wave-1 local chain is checked from chain_seq 1 to its highest chain_seq at the start and is reported "INTACT"
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance role (RW-COMPLY)
    Then the same run over 10,000,000 synthetic entries finishes inside the 60 minute budget

  Scenario: AC2 A break in one service's local chain and two changed ledger entries are found and named (new, D-RCV-60)
    Given the actions of the record with chain_seq 30,005 in the local chain of a wave-1 service were changed in the DEV database with the trigger disabled and the trigger was restored
    Given the entries with chain_seq 12,001 and 40,350 in the central ledger were changed in the DEV database
    When decisionChainCheck runs at 02:00
    Then the first break in that local chain is chain_seq 30,005 and its entry ID, and the run record names the service and the chain
    Then the first break in the central ledger is chain_seq 12,001 and the failing count there is 2
    Then one incident is raised and MSG-P7-008 with the entry IDs is sent to the Compliance role (RW-COMPLY) before 08:00 on 3 December 2026
    Then the run record and the report name service names, chain_seq and entry IDs only, and no personal value

  Scenario: AC3 The run waits for the ingest watermark and keeps the 04:00 latest start (new, D-RCV-60)
    Given the ingest of rwb.decision-record.v1 into the ledger has not reached the producer watermark at 02:00
    When decisionChainCheck fires at 02:00
    Then the workflow re-reads the watermark every 5 minutes and starts the check when the ledger reaches it
    Then the run record names the ingest watermark and holds no copy job end time
    Then when the watermark is not reached by 04:00 the check starts at 04:00 with the note "ingest not at watermark"
    Given the ledger holds 48,210 entries when the run starts and 37 entries are ingested while it runs
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries

  Scenario: AC4 A local record with no ledger entry is found and named as a gap (new, D-RCV-60)
    Given a wave-1 service has committed a local decision_record for case "RW-2026-000123"
    Given its DecisionRecorded event is held in the retry topic, so the ledger holds no entry with that entryId
    When decisionChainCheck runs
    Then the run names the service, the entryId and its chain_seq as a gap between the local chain and the ledger
    Then both chains are reported "INTACT" and the gap is the finding
    Then an incident is raised and MSG-P7-008 is sent with that entryId
    When test user "U-9301" holding RW-PLATADM reruns JOB-14 for business date 2 December 2026 through POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun after the retry delivers the event
    Then a second run record for business date 2 December 2026 is written with rerun true and result "INTACT"
    Then the Schedule refuses a second concurrent start while the rerun is running

  Scenario: AC5 A run that stops is reported and a rerun needs the Platform administration right (new, D-RCV-60)
    Given the ledger connection is closed in the test double after 20,000 entries
    When decisionChainCheck runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the platform administrator group is alerted
    Then MSG-P7-013 is sent to the Compliance role (RW-COMPLY) with 2 December 2026 as the date of the last complete check
    When test user "U-8442" holding only RW-AUDIT calls POST /api/recovery/source-data/v1/admin/jobs/{jobId}/rerun
    Then rwb-access refuses through POST /api/recovery/access/v1/authorise and the answer is 403 with MSG-P4-002
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The whole chain is recomputed every night and a break is reported to Compliance the same day | REQ-DRI-003; NFR-035; JOB-14 |
| BR2 | Each entry's `entry_hash` is recomputed from the canonical form and its `prev_hash` compared with the entry before it | RWB-E1-008, BR3 and BR4 |
| BR3 | A run covers chain_seq 1 to the highest chain_seq at its start, in each chain it checks | This story |
| BR4 | JOB-14 runs after the ingest of `rwb.decision-record.v1` reaches the producer watermark, starting no later than 04:00, and the run record names that watermark instead of a copy job end time | Arch v5 slides 28 and 44; DP-03, DP-17; parameters `rwb.decision.chaincheck.*` |
| BR5 | A run that does not complete is reported to Compliance with the date of the last complete check | NFR-035 |
| BR6 | Only one run of JOB-14 is active at a time (overlap policy SKIP); a rerun is a new run record with rerun true | DP-10; Arch v5 slide 44 notes; legacy job run record |
| BR7 | Start times, latest start and batch size are parameters, not code | Principle 1; DP-06 |
| BR8 | Every service keeps its own local chain in its own schema and publishes `DecisionRecorded` on `rwb.decision-record.v1`; the run checks the central ledger and every wave-1 local chain and names a break against the service and the chain it belongs to | Arch v5 slides 20 and 28 steps 1 to 3; Temporal design slides 11 and 14; ASM-0549 |
| BR9 | A report names service names, entry IDs, `chain_seq` and hashes only, never a personal value | Legacy guardrails; Arch v5 slide 42 notes |
| BR10 | rwb-decision ingests the record into the central ledger within 5 minutes; there is no data lake and no nightly copy of the log, and a gap between a local record and the ledger is a finding of the check | Arch v5 slide 28, step 3 and slide 37; DP-17; RWB-E1-014 retired |
| BR11 | The check reads the ledger and each local chain through their owners' published read paths and reads no other service's tables | DP-01; Arch v5 slide 29 |

##### 9. State transitions

None for a case status. This story changes no case status of its own; it reads the chains and asserts the result.

The run, chain and ingest states the harness observes:

| Item | States |
|---|---|
| JOB-14 run | Waiting for the ingest watermark, Running, Completed with result INTACT or BROKEN, or Failed |
| Run record | One per run, with rerun false for the scheduled run and true for a rerun; never edited |
| Central ledger chain | Sequenced from chain_seq 1 (prev_hash 64 zeros) to the last chain_seq; unbroken or broken at the first entry whose `entry_hash` or `prev_hash` does not match |
| Local chain (each wave-1 service schema) | Same, in the service's own schema, from chain_seq 1 to its own last chain_seq |
| Ingest | Received, deduplicated through `processed_event`, appended, retried through the retry topic, or dead-lettered |
| Gap | A local record with no ledger entry, or a ledger entry with no local record; open until a run closes it |
| Harness run | Not started, running, passed, failed with the failing criterion and the service named |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of the integration harness | Owns the harness, the fixtures, the tamper steps and the run report |
| rwb-decision owner (RWB-P7-E1008-APP) | Owns the ledger, the ingest, `ChainCheckWorkflow` and the Schedule |
| Platform story owner (RWB-PLT-TE008-APP) | Owns the scheduled-job and run-record parts of the check built on the service template |
| Wave-1 service teams | Own their local `decision_record`, its schema objects and the publish of `DecisionRecorded` |
| rwb-source-data owner (P1) | Owns the run-record read and the rerun operation |
| rwb-access owner (P4) | Owns the Platform administration right check and the refusal |
| RW-COMPLY Compliance and PDPA officer | Receives every report; owns the check and its parameters |
| RW-AUDIT Internal audit | Reads the run records; may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts; reruns the job |
| RW-SECADM Security administrator | Receives the break incident with Compliance |
| No role | May update, delete or repair an entry of any chain |

The tamper steps of AC2 and AC3 run as the schema owner in DEV only, on the synthetic data set, and are switched off in SIT, UAT and production; each restores the trigger in the same run and asserts the restore.

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (rwb_decision) | all fields | Read |
| DF-DEC-028 | `decision_log_entry` (rwb_decision) | chain_seq | Read |
| DF-DEC-029 | `decision_log_entry` (rwb_decision) | corrects_entry_id | Read |
| DF-DEC-030 | `decision_log_entry` (rwb_decision) | actor_user_id | Read |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (each wave-1 service schema) | all fields | Read |
| DF-DEC-028 to DF-DEC-030 | `decision_record` (each wave-1 service schema) | chain_seq, corrects_entry_id, actor_user_id | Read |
| None | `processed_event` (rwb_decision and each wave-1 consumer schema) | event id, consumer group, processed at | Read |
| None | JOB-14 run record | business date, status, checks, ingest watermark, rerun | Read |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-008. The harness owns no schema, no table and no field: it reads the ledger and the local chains through their owners' read paths and starts the Schedule through the Temporal client. The run record is read through `GET /api/recovery/source-data/v1/admin/jobs` (P1) and its home is Not specified in the source documents (GAP-0380; ASM-0550); the ingest watermark that the run waits on is Not specified either (GAP-0380; ASM-0549).

##### 12. Contract

###### 12.1 REST operations provided

None. The harness is a test project and provides no REST operation; the integration service base `/api/recovery/integration/v1` and queue `rwb-integration` carry nothing new for it.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/decision/v1/decision-log` | P7 rwb-decision | Reads the entries of one case in chain order, page and size, to reconcile a local record with its ledger entry |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | Reads one entry by entry ID, with chain_seq, prevHash and entryHash, to confirm the named break |
| GET | `/api/recovery/source-data/v1/admin/jobs` | P1 rwb-source-data | Reads the JOB-14 run records, their status, checks, ingest watermark and rerun flag |
| POST | `/api/recovery/source-data/v1/admin/jobs/{jobId}/rerun` | P1 rwb-source-data | Reruns JOB-14 for the business date; 403 with MSG-P4-002 without Platform administration U |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | The Platform administration U check for the rerun and the refusal of RW-AUDIT |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget; the harness calls no service through another service.

###### 12.3 Events published

None. The harness publishes no business event; topic `rwb.integration.events.v1` is not used by this story. The event the check observes is produced by every wave-1 service and is listed in 12.4.

###### 12.4 Events consumed

| Event | Topic | Owner | Consumer contract |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by every wave-1 service; consumed by P7 rwb-decision and P9 rwb-reporting | CloudEvents 1.0 binary mode, key caseId, exactly one event per append, inbox dedupe in `processed_event`, retry 1 min, 10 min, 1 h then `.dlt`; the ingest into the ledger is the watermark the run waits on |

The harness reads the topic and the consumer offsets to compute the producer watermark; the watermark definition and the local-chain scope of the check are Not specified in the source documents (GAP-0380; ASM-0549).

###### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| `ChainCheckWorkflow` | Workflow | `rwb-decision` | Input business date, the chains to check and the ingest watermark; output per chain the count checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count, gap list and the incident reference |
| `ingestDecisionRecord` | Activity | `rwb-decision` | Input the DecisionRecorded envelope; output entry ID, chain_seq and entry_hash; idempotent on the event id through `processed_event`; its offset is the ingest watermark the run waits on |

Both are registered by the rwb-decision worker (RWB-P7-E1008-APP); this story starts them through the real Schedule and asserts their output, and it adds no workflow of its own. The scope of `ChainCheckWorkflow` over the local chains is Not specified in the source documents (GAP-0380; ASM-0549).

###### 12.6 Schedules

| Schedule | Cadence | Registration | Legacy reference |
|---|---|---|---|
| `decisionChainCheck` | Daily at 02:00 Asia/Bangkok, overlap policy SKIP, catch-up window, latest start 04:00 for the ingest watermark | Registered by the rwb-decision release; started once by the harness through the Temporal client with the same input the cadence uses | JOB-14 Hash-chain check (Quartz job in RWB-TE-008) |

###### 12.7 Tables owned

None. The harness owns no table. The tables it exercises belong to rwb_decision, to each wave-1 service schema and to the platform library, and are listed in section 11 with their owners.

###### 12.8 Contract fakes

None. This is the integration level: the real services, the real topic and the real Schedule replace the contract fakes of the app stories.

###### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 5 | Two decision reads, the run-record read, the rerun and the authorise call; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 1 event type | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` from each wave-1 service; read for the ingest watermark |
| Temporal | None | 1 workflow, 1 activity, 1 Schedule | `ChainCheckWorkflow`, `ingestDecisionRecord`; `decisionChainCheck` at 02:00 on `rwb-decision` |
| File | None | None | No file in this story; no lake copy exists (DP-17) |

##### 13. Solution plan

**Deliverables.** One test project `integration/recovery-w1/chain-check`, with the five test classes `ChainIntactIT`, `ChainBreakIT`, `IngestWatermarkIT`, `LocalLedgerGapIT` and `StoppedRunIT`, the fixture files and the run report writer.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight, run order, report and exit code |
| ChainFixtureBuilder | Service | Builds the 48,210-entry chain and the 10,000,000-entry chain deterministically through the real write path, in the ledger and in one local chain per service, with the golden canonical form |
| IngestProbe | Service | Reads `rwb.decision-record.v1` and the consumer offsets and computes the producer watermark the run waits on |
| ChainCheckDriver | Service | Starts `decisionChainCheck` once, reads the workflow result for the ledger and for each local chain, and times the incident and MSG-P7-008 from the run start |
| TamperTool | Service | DEV only: disables the trigger, changes the actions of the records with chain_seq 30,005 in one local chain and 12,001 and 40,350 in the ledger, restores the trigger and verifies the restore |
| GapDriver | Service | Holds a DecisionRecorded event in the retry topic, waits for the run to name the gap, releases the event and waits for the ingest |
| RunRecordProbe | Service | Reads the run records through the P1 admin path, asserts rerun true on the rerun and the SKIP refusal of a concurrent start |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The harness writes only through the services' own write paths, and the only direct writes are the DEV tamper steps of AC2, which restore the trigger.

**Configuration and reference data**

- The service list, the topic, the retry and `.dlt` topics, the queue, the namespace and the Schedule name, all as configuration.
- The business date 2 December 2026, the synthetic case "RW-2026-000123" and the fixture package code.
- The parameters start 02:00, latest start 04:00 and batch size 1,000, read through the rwb-case parameters contract (DP-06).
- The decision codes, outcome codes and approval levels, read through the rwb-case reference-data contract (DP-07).
- The test roles RW-COMPLY, RW-AUDIT, RW-SECADM and RW-PLATADM with their Platform administration letters, from rwb-access.
- The 08:00 same-day report limit, the 5-minute ingest target, the 60 minute budget for 10,000,000 entries and the 2 s client budget.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-17 | Data lake, INT-19, INT-20 | Removed (no data lake); reporting from events into rwb-reporting | none; a gap if the story needs lake data |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The H, C and X dependencies the DPs name (DP-03, DP-06, DP-07, DP-10, DP-19) stay with the service, platform and operations stories this harness proves; this story carries no H, C or X dependency and its I list names the two stories whose behaviour it exercises (Template and Rules §R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Chain of 48,210 entries | 48,210 synthetic entries through the real write path, in the ledger and in each local chain, first prev_hash 64 zeros | AC1, AC3, TC-TE-008-01-ITG, TC-TE-008-05-ITG |
| Tampered chains | Entry 30,005 changed in one service's local chain; entries 12,001 and 40,350 changed in the ledger, each with the trigger restored | AC2, TC-TE-008-02-ITG, TC-TE-008-07-ITG |
| Held event | One DecisionRecorded held in the retry topic after the local commit | AC4 |
| Stopped run | The ledger connection closed after 20,000 entries | AC5, TC-TE-008-03-ITG |
| Late ingest | The consumer offset behind the producer watermark at 02:00, reached at 02:25, and not reached by 04:00 | AC3, TC-TE-008-06-ITG |
| Appends during the run | 37 entries ingested while the run is in progress | AC3, TC-TE-008-08-ITG |
| Role set | RW-PLATADM, and RW-AUDIT whose Platform administration letter is "-" | AC4, AC5, TC-TE-008-09-ITG |
| Budget chain | 10,000,000 synthetic entries for the 60 minute timing check | AC1 |

**Run order.** Preflight; the intact run over 48,210 entries in the ledger and every local chain (AC1); the ingest watermark with the 04:00 latest start and the 37 appends (AC3); the tampered local chain and ledger entries, then the 02:00 run (AC2); the held event, the gap and the rerun (AC4); the stopped run and the refused rerun (AC5); the 10,000,000-entry budget run; cleanup of the DEV fixtures with every trigger confirmed restored. A failing step stops the run and the report names the criterion, the service and the evidence.

**Done when.** The 14 test cases of section 16 pass on the real services in DEV and SIT, the run at 02:00 names chain_seq 30,005 in the local chain and chain_seq 12,001 in the ledger, a gap is named by service and entry ID, the incident and MSG-P7-008 arrive before 08:00 the same day, a rerun carries rerun true, a stopped run sends MSG-P7-013, and the 10,000,000-entry run finishes inside 60 minutes.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-007 | The chain is intact | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. |
| MSG-P7-008 | The chain is broken, or a local record has no ledger entry | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-013 | The run did not complete | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

The four texts are copied unchanged from RWB-TE-008; this story adds no message text. The route of the incident and of the report to Compliance across services is Not specified in the source documents (GAP-0380; ASM-0549). Report lines of the harness are for developers and are not part of the message standard.

##### 15. Screens and states

No screen in this story, and the harness renders nothing: the run records are read through the P1 admin path and the entries through the two decision reads. The job monitor screen (SCR-44 Interface and job monitor) and the administration screens that show a broken chain as a control breach come with their own stories and are out of scope here. The states the harness observes are the run, chain, ingest and gap states of section 9.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-008-01-ITG | legacy AC1, BR1 | Integration | 48,210 synthetic entries in the ledger and in every local chain, none changed |
| TC-TE-008-02-ITG | legacy AC2, BR1 | Integration | One entry changed in DEV with the trigger disabled and the trigger restored |
| TC-TE-008-03-ITG | legacy AC3, BR5 | Integration | Connection closed after 20,000 entries |
| TC-TE-008-04-ITG | legacy AC4, BR6 | Integration | Failed run, then a rerun at 08:30 |
| TC-TE-008-05-ITG | legacy AC5 | Integration | Empty chain in the ledger and in one local chain |
| TC-TE-008-06-ITG | legacy AC6, BR4 | Integration | Ingest reached at 02:25; ingest not at the watermark by 04:00 |
| TC-TE-008-07-ITG | legacy AC7, BR2 | Integration | Two entries changed in the ledger |
| TC-TE-008-08-ITG | legacy AC8, BR3 | Integration | 37 entries ingested during the run |
| TC-TE-008-09-ITG | legacy Access, MSG-P4-002 | Integration | A role without the right is refused with MSG-P4-002 |
| TC-ITG-TE008-01 | AC1, BR1, BR8 | End to end | 48,210 entries in the ledger and in every wave-1 local chain; the 02:00 Schedule; MSG-P7-007; the 10,000,000-entry budget |
| TC-ITG-TE008-02 | AC2, BR2, BR9 | End to end | Local chain 30,005 changed; ledger 12,001 and 40,350 changed; one incident and MSG-P7-008 before 08:00, no personal value |
| TC-ITG-TE008-03 | AC3, BR4, BR10 | End to end | Watermark behind at 02:00, reached at 02:25, not reached by 04:00; 37 appends during the run; 48,247 the next night |
| TC-ITG-TE008-04 | AC4, BR6, BR10 | End to end | Held event, the named gap, the rerun with rerun true and the SKIP refusal of a concurrent start |
| TC-ITG-TE008-05 | AC5, BR5 | Integration | Connection closed after 20,000 entries; RW-AUDIT rerun refused with MSG-P4-002 |

The legacy acceptance criteria numbers in the Covers column belong to RWB-PLT-TE008-APP, the story that owns the eight legacy RWB-TE-008 criteria on the target services; the legacy test case IDs are kept here as ITG copies with the suffix `-ITG`, and the new criteria AC1 to AC5 carry TC-ITG-TE008-01 to TC-ITG-TE008-05.

##### 17. Guardrails

- No business value in code: the start time, the latest start, the batch size, the fixture sizes, the report limit and the wait intervals are configuration, and the decision codes and approval levels are reference data (DP-06, DP-07).
- No personal data in events, workflow inputs, logs, fixtures or the report: service names, entry IDs, case IDs, `chain_seq`, rule IDs and hashes only (BR9).
- Each service writes only its own schema and reads no other service's tables (DP-01); the harness reads through the published read paths, and its only direct writes are the DEV tamper steps, which are refused in SIT, UAT and production and restore the trigger.
- The check never writes to a chain and never repairs an entry; a correction is a new entry naming the one it corrects.
- One canonical form implementation serves writing and verifying; a second implementation would make a real break indistinguishable from a hash mismatch.
- One Schedule and one event type for the record: a service that publishes its own decision event on its own topic, or a second copy of the log outside the ledger, fails the run (BR10, DP-17).
- The harness never uses production data and never points at a production namespace; the incident and the report are raised in the test environment only.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-003 | Hash chain checked every day, a break reported to Compliance the same day | `decision_log_entry` and `decision_record` `prev_hash` and `entry_hash`, `ChainCheckWorkflow`, `decisionChainCheck`, MSG-P7-007, MSG-P7-008, MSG-P7-013 | TC-TE-008-01-ITG to TC-TE-008-09-ITG, TC-ITG-TE008-01, TC-ITG-TE008-02, TC-ITG-TE008-03, TC-ITG-TE008-04, TC-ITG-TE008-05 |

##### 19. Out of scope

- The store, the ingest, the ledger, `ChainCheckWorkflow` and the two decision read endpoints (RWB-P7-E1008-APP).
- The local `decision_record` of each wave-1 service and its publish of `DecisionRecorded` (the app and DB stories of each service).
- The contract and the AsyncAPI document of `rwb.decision-record.v1` (RWB-P7-E1008-CON).
- The `decision_log_entry` and `decision_record` schema design, the append-only trigger and the grants (RWB-P7-E1008-DB).
- The registration, the overlap policy and the catch-up window of the Schedule as a deployment step, and the scheduled-job and run-record parts of the check on the service template (RWB-PLT-TE008-APP).
- The Platform administration right and its refusal in rwb-access; this story exercises it and owns none of it.
- The check of each entry returned by an audit query, the Decision log query screen and the administration screens that show a broken chain as a control breach.
- The daily ledger seal to immutable storage (Arch v5 slide 14, step 4).
- The definition of the ingest watermark and the local-chain scope of the check until they are published (GAP-0380).


## RWB-TE-009 Performance test harness

Legacy disposition: Split (rework).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-ITG-TE009-ITG | Integration | RWB-ITG-NFR | L-ITG-NFR | Day 1 | QA team (suggested; any team may pick up this story) |

### RWB-ITG-TE009-ITG Performance test harness

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE009-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-ITG-NFR |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-TE-009 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP07, DP10, DP13, DP19, DP20 |
| Parallel lane | L-ITG-NFR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-030, FR-PLT-031, FR-PLT-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-TE-009 is split and reworked as the integration story RWB-ITG-TE009-ITG, the busiest-hour load harness that runs in the SIT release pipeline and gates the release stage on the per-service bases through the gateway-bff composite route. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **a busiest-hour load harness in the SIT release pipeline that exercises the screens through gateway-bff on the per-service bases and fails the release stage when a screen request is too slow**, so that **response targets are proven before users feel them**.

##### 2. Business rationale

About 370 staff and 50 partner users are online in the busiest hour (NFR-002, NFR-003) and every screen must respond in under 2 seconds (NFR-008). A screen that is fast with ten testers can be slow with 410 virtual users at 3 requests a minute each on 23,600 open cases. The harness runs the busiest hour on the SIT data set before each release and stops the release stage when a target is missed. It proves the response of the case record view (REQ-OCC-007) and the team manager's case list (REQ-WKM-002) under load. The measure is the 95th percentile response time per screen request in the busiest hour.

In the target architecture the screen request is served by the gateway-bff composite route (DP-19), and each call inside the route goes to the owner's base `/api/recovery/<short>/v1` (DP-13), not to a monolith base. The harness therefore measures the routes and the per-service bases that the real screens use, so a slow hop is visible at the same point a user would feel it.

##### 3. Preconditions

- SIT holds at least 23,600 open cases of masked data (RWB-TE-004, NFR-001).
- Named test users exist for each role in the operation mix, with Entra ID groups per role. The identity set of the test users per role is not specified in the source documents (GAP-0330; ASM-0422).
- An SIT deployment slot is booked for the run.
- The operation mix file and the pass criteria are loaded in the harness configuration: 410 virtual users at 3 requests a minute each; 95th percentile under 2,000 ms per operation; error rate under 1 percent.
- The build under test is deployed to SIT with its release feature flags as planned for the release.
- The gateway-bff composite routes and the per-service bases are reachable in SIT. The composite route specification is not specified in the source documents (GAP-0330; ASM-0422).
- No build dependency. Day 1.

##### 4. Flow

1. Release pipeline: starts the SIT performance stage for the build, or a squad member starts it by hand.
2. Harness: takes the SIT run lock and refuses to start when another run holds it.
3. Harness: counts open cases through `GET /api/recovery/case/v1/cases` and refuses to start when fewer than 23,600 are found.
4. Harness: signs in the test users for each role in the mix.
5. Harness: ramps to 410 virtual users over 10 minutes, then holds 60 minutes at 3 requests a minute per user, following the weights in the mix file.
6. Harness: records the response time and the status of each request; 403 responses on operations the mix marks as refusals count as expected.
7. Harness: computes the 50th, 95th and 99th percentiles, the throughput and the error rate per operation over the 60 steady minutes.
8. Gate: passes when every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent; otherwise it fails the stage.
9. Harness: attaches the report to the release record with the build ID, releases the lock and triggers the restore of the SIT data set.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Another run holds the SIT run lock | The run refuses to start and the stage stops before any load | run already in progress | AC5 |
| X2 | Fewer open cases than the test base | The run refuses to start and reports the count against the base | data volume below the test base: {count} of {base} | AC4 |
| X3 | A test user of a role in the mix cannot sign in | The stage fails and names the role; no load is generated for that role | None | AC1 |
| X4 | gateway-bff or a service answers 503 | The request counts as an error; the stage fails on the error rate when the limit is crossed | error rate above limit: {rate} percent | AC3 |
| X5 | An operation's 95th percentile is at or above 2,000 ms | The gate fails the stage and the report names the operation, its 95th percentile and the limit | target missed: {operation} {p95} ms, limit {limit} ms | AC2 |
| X6 | The error rate is at or above 1 percent | The gate fails the stage and the report names the operation and the rate | error rate above limit: {rate} percent | AC3 |
| X7 | A run is stopped part way | The run is marked failed and the lock is released within 90 minutes | None | AC5 |

The report text is for the release team and is not part of the message standard. MSG-P4-002 is the business message for an expected refusal, and the harness records it as an expected result, not as an error.

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the SIT data set of RWB-TE-004, a deployed build and reachable routes; no build dependency |
| Negotiable | The mix, the user count and the pass limits are configuration, never code |
| Valuable | A slow screen is found in SIT, not by the busiest hour of users in production |
| Estimable | One load script, one mix file, one gate, one report publisher |
| Small | Fits in one sprint with its tests |
| Testable | The gate is tested with result fixtures; the run is tested in SIT against the deployed services |

##### 7. Acceptance criteria

```gherkin
Feature: Busiest-hour performance harness for the recovery screens

  Background:
    Given the build under test is deployed to SIT with its release feature flags
    Given the harness configuration holds the operation mix, the user count and the pass limits
    Given the screens are reached through the gateway-bff composite routes
    Given each call uses the owner's per-service base /api/recovery/<short>/v1

  Scenario: AC1 The busiest-hour load runs at 410 virtual users and 3 requests a minute (new, D-RCV-60)
    Given the SIT performance stage starts for the build
    When the harness ramps to 410 virtual users over 10 minutes and holds for 60 minutes at 3 requests a minute per user
    Then every request follows the weights of the operation mix file
    Then the measured period is the 60 steady minutes only
    Then the operations exercised are GET /api/recovery/case/v1/cases, GET /api/recovery/case/v1/cases/{caseId}, GET /api/recovery/case/v1/cases/{caseId}/timeline, GET /api/recovery/case/v1/queues/{queueId}/cases, GET /api/recovery/document/v1/cases/{caseId}/documents, POST /api/recovery/source-data/v1/cases/{caseId}/interactions and POST /api/recovery/case/v1/cases/{caseId}/transfer as the expected refusal for RW-PHONECOL

  Scenario: AC2 The gate fails the stage when a 95th-percentile target is missed (new, D-RCV-60)
    Given the per-operation results of the steady period
    When an operation's 95th percentile is at or above 2,000 ms
    Then the gate fails the stage
    Then the report names the operation, its 95th percentile and the 2,000 ms limit
    When every operation's 95th percentile is under 2,000 ms
    Then the gate passes for that operation

  Scenario: AC3 The gate fails the stage when the error rate is at or above 1 percent (new, D-RCV-60)
    Given the per-operation results of the steady period
    When the error rate of an operation is at or above 1 percent
    Then the gate fails the stage and the report names the operation and the rate
    Then a 403 response on an operation the mix marks as a refusal is counted as expected and not as an error

  Scenario: AC4 The run refuses to start below 23,600 open cases (new, D-RCV-60)
    Given the SIT data set of masked data
    When the harness counts open cases through GET /api/recovery/case/v1/cases before the run
    Then it refuses to start when fewer than 23,600 are found and reports the count and the base
    Then it starts when 23,600 or more are found

  Scenario: AC5 One run at a time and the lock is released within 90 minutes (new, D-RCV-60)
    Given a run holds the SIT run lock
    When a second run starts
    Then it is refused with "run already in progress"
    When the first run ends or stops part way
    Then the lock is released, and in every case within 90 minutes at most
    Then a run stopped part way is marked failed

  Scenario: AC6 The report is attached to the release record (new, D-RCV-60)
    Given a finished run
    When the harness publishes the report
    Then the report carries the build ID, the mix file version and, per operation, the count, the 50th, 95th and 99th percentiles, the throughput and the errors
    Then it carries the gate result, and the latest run for a build decides the gate
    Then it holds operation names and numbers only and no personal data
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The load is 410 concurrent users at 3 requests a minute each, the busiest hour of staff and partner users | NFR-002; NFR-003 |
| BR2 | Each screen request responds under 2,000 ms at the 95th percentile; 2,000 ms fails | NFR-008 |
| BR3 | The error rate over the steady period is under 1 percent; expected 403 refusals are not errors | Legacy RWB-TE-009 BR3 |
| BR4 | The run uses at least 23,600 open cases of masked data | NFR-001; NFR-045 |
| BR5 | The operation mix, the user count and the limits are read from the harness configuration, never from the script | Legacy RWB-TE-009 BR5 |
| BR6 | One run at a time in SIT; the latest run for a build decides the gate | Legacy RWB-TE-009 BR6 |
| BR7 | Every exercised operation calls the owner's per-service base through the gateway-bff composite route | DP-13; DP-19 |
| BR8 | The 2,000 ms budget is measured at the gateway-bff response | ASM-0423 |

##### 9. State transitions

| From | To | Trigger |
|---|---|---|
| Not started | Running | The release pipeline starts the SIT performance stage for the build |
| Running | Passed | Every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent |
| Running | Failed | A limit is missed, a 503 raises the error rate, or the run is stopped part way |
| Failed | Running | A rerun for the same build, which replaces the gate result for that build |

This story changes the state of the SIT performance stage only. It never changes a case status and writes no row through any service other than the SIT interaction writes of section 11.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Start a run, change the mix file through a reviewed pull request, read reports |
| RW-PLATADM, platform administrator | Books the SIT slot and restores the SIT data set after the run |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-PHONECOL | Make the simulated requests with their own rights |
| QA lead | Owns the harness configuration: the mix file, the user count and the pass limits |
| Platform edge owner | Owns the gateway-bff route list the harness calls |
| No approval level from the delegation of authority applies | The story takes no business decision |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-WRK-001 | queue | id | Read |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write, SIT only, by `POST /api/recovery/source-data/v1/cases/{caseId}/interactions` |

The harness reads and writes only through the API: it owns no schema and reads no other service's tables (DP-01). Field IDs are those of the Logical Data Model and Data Dictionary. The SIT data set is restored after each run.

##### 12. Contract

###### 12.1 REST operations provided

None. The harness is a pipeline stage and provides no REST operation.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/case/v1/cases` | P3 rwb-case | Open-case count before the run and the case list operation of the mix |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | Case record operation (SCR-03) |
| GET | `/api/recovery/case/v1/cases/{caseId}/timeline` | P3 rwb-case | Case timeline operation (SCR-04) |
| GET | `/api/recovery/case/v1/queues/{queueId}/cases` | P3 rwb-case | Team queue operation (SCR-07) |
| GET | `/api/recovery/document/v1/cases/{caseId}/documents` | P5 rwb-document | Document list operation of the case record |
| POST | `/api/recovery/source-data/v1/cases/{caseId}/interactions` | P1 rwb-source-data | Interaction write, SIT only, from the mix |
| POST | `/api/recovery/case/v1/cases/{caseId}/transfer` | P3 rwb-case | Expected refusal for RW-PHONECOL (MSG-P4-002) |

Every operation is called through the gateway-bff composite route (DP-19) and on the owner's per-service base (DP-13).

###### 12.3 Events published

None. The harness publishes no Kafka event; the report goes to the release record through its pipeline integration.

###### 12.4 Events consumed

None.

###### 12.5 Workflows and activities

None. The harness runs as a pipeline stage and starts no Temporal workflow or activity; DP-10 is applied by keeping the harness out of the job list, so no Schedule is created.

###### 12.6 Schedules

None.

###### 12.7 Tables owned

None. The harness owns no table (DP-01); it reads and writes through the API of the owning services only.

###### 12.8 Contract fakes

None. The stage runs against the deployed SIT services and their real contracts; contract fakes are not used at this level.

###### 12.9 Call-type summary

| Call type | In this story |
|---|---|
| REST | 0 provided, 7 consumed, every call through gateway-bff on the owner's base |
| Kafka | None |
| Temporal | None |
| File | None |

##### 13. Solution plan

**Package.** Folder `perf/recovery` in the ACE repository, package `<ACE base package>.recovery.perf`. Not part of the deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BusiestHourSimulation | Job | Sign-in, ramp, steady period and weighted operations |
| mix file | Rule table | Operation, weight, role, expected status |
| perf settings | Rule table | User count, request rate, durations, limits |
| DataVolumeCheck | Service | Counts open cases before the run |
| RunLock | Service | One run at a time in SIT |
| PerformanceGate | Service | Evaluates the result against the limits |
| ReportPublisher | Service | Attaches the report and the gate result to the release record |

**Database.** None. The harness owns no schema and uses the API only.

**Configuration.** The mix file and the settings sit in `perf/recovery/config`; the test users per role come from the SIT identity set; the gateway route list comes from the platform edge.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The story carries no H, C, I or X dependency (the plan keeps them empty) because the harness runs against the deployed SIT services and their published contracts, and the DP dependencies stay with the service implementation stories; DP-10 resolves to "no Schedule" and DP-20 resolves to "the agent is not in the mix" (NFR-010 is out of scope, the P10 stories own it).

**Build steps**

1. Write PerformanceGate with unit tests from result fixtures for the 2,000 ms boundary and the error rate.
2. Write DataVolumeCheck and RunLock.
3. Write BusiestHourSimulation reading the mix file and the settings.
4. Add the expected refusal for RW-PHONECOL on the transfer operation and count 403 as expected.
5. Write ReportPublisher with the build ID and the latest-run rule.
6. Add the stage to the release pipeline before the UAT exit and run it once on the Epic 2 build.

**Done when.** The tests of section 16 pass and the Epic 2 release record holds a passed report for the release build.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | An operation's 95th percentile is at or above the limit | `target missed: {operation} {p95} ms, limit {limit} ms` |
| Report | The error rate is at or above the limit | `error rate above limit: {rate} percent` |
| Report | Not enough data for the run | `data volume below the test base: {count} of {base}` |
| Report | Another run holds the lock | `run already in progress` |
| MSG-P4-002 | Expected refusal for a role without the right | You cannot {action} here. Your role does not include it. |

The report text is for the release team and is not part of the message standard.

##### 15. Screens and states

No screen in this story; the release team reads the report attached to the release record. The screens under load are SCR-02 Case list, SCR-03 Case record, SCR-04 Case timeline and SCR-07 Team queues, each in the states listed in the browser story, and each reached through the gateway-bff composite route. The composite route specification is not specified in the source documents (GAP-0330; ASM-0422).

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ITG-TE009-ITG-01 | AC1 | NFR | Mix fixture; ramp 10 minutes and steady 60 minutes at 410 virtual users and 3 requests a minute |
| TC-ITG-TE009-ITG-02 | AC2 | NFR | Result fixture at 1,999 ms passes and at 2,000 ms fails |
| TC-ITG-TE009-ITG-03 | AC3 | NFR | Error rate 0.9 percent passes and 1.0 percent fails; an expected 403 is not counted |
| TC-ITG-TE009-ITG-04 | AC4 | Integration | 23,599 open cases refuses and 23,600 starts |
| TC-ITG-TE009-ITG-05 | AC5 | Integration | A second run is refused; the lock is released within 90 minutes after a stopped run |
| TC-ITG-TE009-ITG-06 | AC6 | Component | Report fixture with two operations and one missed target, build ID and mix version present |

##### 17. Guardrails

- No business value in code: the mix, the user counts and the limits are configuration.
- No personal data in logs, reports, tests or prompts: the run uses the SIT masked data set, and the report holds operation names and numbers only.
- No read of another service's tables: the harness uses the API only (DP-01).
- The harness never runs against UAT or production.
- An exception to a limit is never added to the script; a limit that must change is changed in the configuration through a reviewed pull request.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | GET case operations | TC-ITG-TE009-ITG-01, TC-ITG-TE009-ITG-02 |
| REQ-WKM-002 | Team manager sees every team queue with filters | GET queues/{queueId}/cases | TC-ITG-TE009-ITG-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | gateway-bff one hop and the 2,000 ms budget | TC-ITG-TE009-ITG-02 |

##### 19. Out of scope

- Masked data in SIT and UAT: RWB-TE-004.
- Batch window timing of the daily jobs: the job stories.
- Agent response times, NFR-010: the P10 agent runtime stories (DP-20).
- Production monitoring of response times: RWB-E1-056.
- UAT and production runs.
- The gateway-bff route specification: the platform edge story.


## RWB-TE-010 Browser and accessibility tests

Legacy disposition: Moved (no impact).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-ITG-TE010-ITG | Integration | RWB-ITG-NFR | L-ITG-NFR | Day 1 | QA team (suggested; any team may pick up this story) |

### RWB-ITG-TE010-ITG Browser and accessibility tests

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE010-ITG |
| Work type | ITG (Integration) |
| Suggested owner | QA team (suggested; any team may pick up this story) |
| Service | rwb-integration |
| Service epic | RWB-ITG-NFR |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 31 December 2026 (tentative) |
| Legacy key | RWB-TE-010 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP07, DP19 |
| Parallel lane | L-ITG-NFR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-030, FR-PLT-031, FR-PLT-032) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: moved from RWB-TE-010 into the RWB-ITG-NFR epic as the integration harness story for the browser and accessibility stage. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)**, I want **browser tests and an accessibility scan on the main recovery screens, on the browsers the bank supports and in Thai and English, in every pipeline run**, so that **screens work for every user on the bank's browsers**.

##### 2. Business rationale

Recovery staff work on Microsoft Edge and Google Chrome, some with screen readers or keyboard only, and in Thai or English. A screen that passes on one developer's browser can fail on the previous browser version or for a keyboard user, and that is found in UAT or by users. The browser runner tests the six main screens on four browser configurations and scans them for WCAG 2.1 AA errors in both languages before merge. It proves the case record view (REQ-OCC-007) and my queue (REQ-WKM-001) against NFR-060, NFR-061 and NFR-059. The measure is the count of accessibility and browser defects found in UAT, with a target of zero.

In the target the screens are served by the gateway-bff composite route (DP-19), and labels and reference values come from the rwb-case reference-data contract (DP-07). The stage therefore tests the same route and the same label source that production uses, not a local build of the screen.

##### 3. Preconditions

- RWB-TE-003 is done: the front end uses the generated types and client.
- The browser test runner sits in the ACE pipeline before the first SIT run.
- The runner image holds Chrome and Edge at the current and previous major versions, listed in `browsers.json` (NFR-061).
- A test deployment with the synthetic data set and test users per role.
- Screen labels exist in Thai and English in the label tables; Thai labels may show "Pending" until approved (DL10).
- The scan engine and its WCAG 2.1 A and AA rule tags are fixed in the scan profile.
- The gateway-bff route specification and the label source are not specified in the source documents (GAP-0331; ASM-0424; ASM-0425).

##### 4. Flow

1. Pipeline: starts the browser stage after the front-end build on each pull request, and nightly against SIT.
2. Runner: reads `browsers.json` and refuses to start when a listed browser is missing.
3. Runner: signs in the test user of each role in the screen list.
4. Runner: opens each main screen (SCR-02, SCR-03, SCR-04, SCR-05, SCR-07, SCR-09) in each listed state and runs its functional test on each browser.
5. Runner: runs the accessibility scan with the WCAG 2.1 A and AA rule tags on each screen and state, in Thai and in English.
6. Runner: runs the keyboard test: every primary action is reachable and usable by keyboard with a visible focus.
7. Runner: compares each violation with the exception list; an entry past its expiry date does not excuse the violation.
8. Runner: retries a failed functional test once and lists a test that passes only on retry as flaky.
9. Pipeline: fails the stage on any violation, functional failure or missing browser, and attaches the report.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A listed browser or version is missing from the runner image | The stage fails before any test runs; the report names the browser and the version | `browser not available: {browser} {version}` | AC1 |
| X2 | A WCAG 2.1 A or AA violation on a screen and state | The stage fails; the report names the screen, the state, the language, the rule and the element | `accessibility violation: {screen} {state} {language} {rule} {element}` | AC2 |
| X3 | An exception entry past its expiry date matches the violation | The violation is not excused and the stage fails; the report names the entry's expiry date | `exception expired: {screen} {rule} since {date}` | AC3 |
| X4 | A primary action is not reachable or not usable by keyboard | The stage fails; the report names the screen and the action | `keyboard access: {screen} action {action}` | AC4 |
| X5 | A screen shows a raw label key instead of a label | The stage fails; the report names the screen and the key | `missing label: {screen} {key}` | AC7 |
| X6 | A functional test fails on the first attempt and again on the single retry | The stage fails; the report holds the two attempts | None | AC6 |
| X7 | A test user whose role does not include the action opens the screen in the state that offers it | The refusal is shown and no control for the action is rendered | MSG-P4-002 | AC5 |

The report text is for developers and is not part of the message standard; only MSG-P4-002 is a business message.

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the generated client of RWB-TE-003 and the runner configuration; it reads the deployed SIT screens, so it waits for no service story of its own |
| Negotiable | Browser versions, screens, states, roles and exceptions are configuration files |
| Valuable | Users on every bank browser and with assistive technology can use the screens, and a regression is caught before merge |
| Estimable | One test suite, one scan helper, one keyboard check, one report writer and three configuration files |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion uses one fixture screen or one browser setting, and the report is the evidence |

##### 7. Acceptance criteria

```gherkin
Feature: Browser and accessibility stage for the recovery screens

  Background:
    Given the browser stage runs after the front-end build on every pull request and nightly against SIT
    Given browsers.json lists the current and previous major versions of Microsoft Edge and Google Chrome
    Given screens.json lists SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09 with their states, roles and primary actions
    Given the screens are reached through the gateway-bff composite routes

  Scenario: AC1 The functional suite passes on every listed browser and a missing browser fails the stage (new, D-RCV-60)
    Given the runner reads browsers.json
    When a listed browser or version is missing from the runner image
    Then the stage fails and the report names the browser and version
    When every listed browser is present
    Then each screen in each listed state passes its functional test on each browser

  Scenario: AC2 The WCAG 2.1 A and AA scan reports zero violations in Thai and in English (new, D-RCV-60)
    Given the accessibility scan runs with the WCAG 2.1 A and AA rule tags
    When each screen and state is scanned in Thai and in English
    Then every violation with a rule tag WCAG 2.1 A or AA fails the stage
    Then the report names the screen, the state, the language, the rule and the element

  Scenario: AC3 An exception entry excuses a violation only until its expiry date (new, D-RCV-60)
    Given an exception entry with an owner, an expiry date and a reason
    When the entry has not expired and matches the screen and the rule
    Then the violation is excused and listed in the report
    When the entry has expired
    Then the violation fails the stage and the report says "exception expired"

  Scenario: AC4 Every primary action is reachable and usable by keyboard (new, D-RCV-60)
    Given a screen and state in screens.json with its primary actions
    When the keyboard check tabs through the screen
    Then every primary action is reachable and usable with a visible focus
    Then a failure names the screen and the action

  Scenario: AC5 A role without the right sees the refusal and no control (new, D-RCV-60)
    Given a test user whose role does not include the action
    When the user opens the screen in the state that offers the action
    Then the screen shows MSG-P4-002 and no control for the action

  Scenario: AC6 A failed functional test is retried once and a pass on retry is listed as flaky (new, D-RCV-60)
    Given a functional test that fails on the first attempt
    When it passes on the single retry
    Then the stage result counts it as a pass and lists it as flaky in the report
    When it fails again
    Then the stage fails

  Scenario: AC7 A raw label key on a screen fails the stage (new, D-RCV-60)
    Given a screen rendered in Thai or in English
    When the screen shows a raw label key instead of a label
    Then the stage fails and the report names the screen and the key

  Scenario: AC8 The six main screens are covered in both languages (new, D-RCV-60)
    Given the screen list of this story
    When the stage runs
    Then SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09 are each tested in every listed state, on every listed browser and in both languages
    Then the report holds one row per screen, state, language and browser
```

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every main screen meets WCAG 2.1 level AA; any violation tagged WCAG 2.1 A or AA fails | NFR-060 |
| BR2 | Screens work on the current and previous major versions of Microsoft Edge and Google Chrome | NFR-061 |
| BR3 | Every screen is checked in Thai and in English | NFR-059 |
| BR4 | A violation is excused only by an exception list entry with an owner and an expiry date not yet passed | Principle 1 applied to test configuration |
| BR5 | A missing browser is a failure, never a skip | DL37 |
| BR6 | A failed functional test is retried once; a pass on retry is listed as flaky | Engineering practice |
| BR7 | A role without the right sees the refusal MSG-P4-002 and no control for the action | CTL-09 |
| BR8 | Labels in Thai and English are read through the rwb-case reference-data contract and screens through the gateway-bff composite route | DP-07; DP-19; ASM-0424 |

##### 9. State transitions

| From | To | Trigger |
|---|---|---|
| Not started | Running | The pipeline starts the browser stage |
| Running | Passed | No violation, no functional failure and no missing browser |
| Running | Failed | Any violation, any functional failure after the retry, or a missing browser |
| Failed | Running | Rerun of the same commit and the same configuration |

This story changes the state of the browser stage only. It never changes a case status: the runner holds no case and writes no service table.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the stage, add screens to the list, request an exception entry |
| TechX tech leads (code owners, RWB-TE-002) | Approve changes to the screen list, the browser list and the exception list |
| QA lead | Owns the runner configuration |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-PLATADM and RW-PHONECOL | Open the screens with their own rights |
| No approval level from the delegation of authority applies | The story takes no business decision |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-030 | lov_value | label_en | Read |
| DF-REF-031 | lov_value | label_th | Read |

The runner reads the synthetic data through the screens only. Labels and role codes are read through the rwb-case reference-data contract (P3, DP-07) and role codes come from rwb-access (P4). The runner owns no schema and reads no service table.

##### 12. Contract

###### 12.1 REST operations provided

None. The functional suite is a pipeline stage and provides no REST operation.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | /api/recovery/case/v1/cases | P3 rwb-case | SCR-02 Case list |
| GET | /api/recovery/case/v1/cases/{caseId} | P3 rwb-case | SCR-03 Case record |
| GET | /api/recovery/case/v1/cases/{caseId}/timeline | P3 rwb-case | SCR-04 Case timeline |
| POST | /api/recovery/case/v1/cases/{caseId}/transfer | P3 rwb-case | SCR-05 Transfer case |
| GET | /api/recovery/case/v1/queues | P3 rwb-case | SCR-07 Team queues |
| GET | /api/recovery/case/v1/queues/{queueId}/cases | P3 rwb-case | SCR-07 Team queues and SCR-09 Exception queue |

Every call goes through the gateway-bff composite route (DP-19). The runner provides no operation and calls no service directly.

###### 12.3 Events published

None.

###### 12.4 Events consumed

None.

###### 12.5 Workflows and activities

None. There is no Temporal workflow or activity; the runner is a pipeline stage.

###### 12.6 Schedules

None. The pipeline schedule starts the stage (each pull request and nightly against SIT); it is not a Temporal Schedule.

###### 12.7 Tables owned

None. The runner owns no table and reads no service table; labels and role codes arrive over the rwb-case reference-data contract.

###### 12.8 Contract fakes

None. The runner tests the deployed SIT screens and their real contracts; contract fakes are not used at this level.

###### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 6, through gateway-bff | One hop, 2 s timeout (ADR-020) |
| Kafka | None | None | The stage publishes and consumes no event |
| Temporal | None | None | No workflow, activity or schedule |
| File | None | None | The report is a pipeline artefact |

##### 13. Solution plan

**Package.** Deliverable folder `ace-web/e2e/recovery` in TypeScript, with the configuration in `ace-web/e2e/recovery/config`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| screens.json | Rule table | Screens, states, roles and primary actions |
| browsers.json | Rule table | Browser names and versions |
| a11y-exceptions.json | Rule table | Excused violations with owner and expiry |
| BrowserGuard | Service | Fails the stage when a listed browser is missing |
| ScreenSuite | Service | Functional tests per screen and state on each browser |
| AccessibilityScan | Service | Scan per screen, state and language with the WCAG 2.1 A and AA tags |
| KeyboardCheck | Service | Tab order and focus on each primary action |
| ReportWriter | Service | Stage report and flaky list |

**Database.** None.

**Configuration and reference data**

- The three configuration files: `screens.json`, `browsers.json` and `a11y-exceptions.json`, owned by the TechX tech leads.
- Browser versions as installed in the runner image.
- Labels in Thai and English through the rwb-case reference-data contract (DP-07).
- Screen routes from the gateway-bff route list (DP-19).

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

The story carries no H, C, I or X dependency because the runner runs against the deployed SIT screens and published contracts, and the DP-07 and DP-19 build dependencies stay with the screens and the platform edge.

**Build steps**

1. BrowserGuard and `browsers.json`, with a missing version failing the stage.
2. Functional tests for the six screens from `screens.json` on the four browser configurations.
3. AccessibilityScan for both languages, including the missing-label check.
4. Exception list handling with expiry.
5. KeyboardCheck for the primary actions.
6. The single retry and the flaky list.
7. The refusal test for RW-PHONECOL on SCR-05, and the stage added to the pipeline.

**Done when.** The tests in section 16 pass and the pipeline shows the browser stage on every front-end pull request.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | A violation | accessibility violation: {screen} {state} {language} {rule} {element} |
| Report | A missing browser | browser not available: {browser} {version} |
| Report | An expired exception | exception expired: {screen} {rule} since {date} |
| Report | A raw label key | missing label: {screen} {key} |
| Report | A keyboard failure | keyboard access: {screen} action {action} |
| MSG-P4-002 | The refusal shown to a role without the right | You cannot {action} here. Your role does not include it. |

Report text is for developers and is not part of the message standard. Only MSG-P4-002 is a business message, and it is unchanged from the legacy set.

##### 15. Screens and states

| Screen | States |
|---|---|
| SCR-02 Case list | Loading, Empty, List, Filtered |
| SCR-03 Case record | Loading, Read only, Editable, On hold |
| SCR-04 Case timeline | Loading, Filtered |
| SCR-05 Transfer case | Form, At cap warning, Saved |
| SCR-07 Team queues | Loading, List |
| SCR-09 Exception queue | Loading, List |

Each screen is reached through the gateway-bff composite route; the route specification is not specified in the source documents (GAP-0331; ASM-0425). Developers read the report in the pipeline.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-ITG-TE010-ITG-01 | AC1, BR2, BR5 | Integration | Four browser configurations present pass; one missing fails |
| TC-ITG-TE010-ITG-02 | AC2, BR1, BR3 | NFR | Fixture screen with one WCAG 2.1 AA violation fails in Thai and in English |
| TC-ITG-TE010-ITG-03 | AC3, BR4 | Component | Exception entry valid excuses; expired fails |
| TC-ITG-TE010-ITG-04 | AC4 | Component | Fixture screen with one primary action reachable only by mouse fails |
| TC-ITG-TE010-ITG-05 | AC5, BR7 | Component | RW-PHONECOL on SCR-05 shows MSG-P4-002 and no control |
| TC-ITG-TE010-ITG-06 | AC6, BR6 | Component | A test failing once then passing is listed flaky; failing twice fails the stage |
| TC-ITG-TE010-ITG-07 | AC7 | Component | A screen showing a raw label key fails the stage |
| TC-ITG-TE010-ITG-08 | AC8, BR1, BR3 | End to end | Six screens, their states, four browser configurations and two languages all reported |

##### 17. Guardrails

- No business value in code: screens, browsers and exceptions are configuration files.
- No personal data in logs, tests or prompts: the synthetic data set only, and screenshots show synthetic data only.
- No read of another service's tables: the runner uses the screens only.
- An exception entry always has an owner and an expiry date.
- A missing browser is never skipped and a missing label is never tolerated.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | GET case operations and SCR-03 | TC-ITG-TE010-ITG-01, TC-ITG-TE010-ITG-02 |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | GET /queues and /queues/{queueId}/cases and SCR-07 | TC-ITG-TE010-ITG-01 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | gateway-bff one hop for every screen route | TC-ITG-TE010-ITG-01 |

##### 19. Out of scope

- Partner portal screens and tablets (NFR-063): the partner portal stories.
- Thai label approval.
- Response times under load (RWB-TE-009).
- Screen design and layout.
- The gateway-bff route specification (platform edge story).


## RWB-TE-011 PDPA lint for code, tests and logs

Legacy disposition: Split (rework).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE011-APP | App development | RWB-PLT-TPL | L-PLT-TPL-Q | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE011-APP PDPA lint for code, tests and logs
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE011-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-011 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP05, DP07, DP08, DP19 |
| Parallel lane | L-PLT-TPL-Q |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P4-E1037-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-008, FR-PLT-019) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: rework of RWB-TE-011 for the 19-repository target. The legacy lint is kept as a build step and re-pointed: the PDPA step is generated once in the golden pipeline and the service template, so every repository generated from the template runs the same rule set at the same version; the personal field marks are read from one pinned dictionary version served by the reference-data contract of rwb-case instead of from a per-repository `sys_fields` seed file, and the ACE field definitions arrive only through the owner's contract or the `v_ace_*` views; the approver of an allow-list change is the code-owner role resolved through the authorise contract of rwb-access, with the repository host merge rule unchanged; and a dictionary read that does not answer fails the build closed. Every legacy value is kept unchanged: rule ids PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID; the fixture values "recovery.casewf.internal.SampleService", "customer.getFirstName()", "CustomerEntity", "idNoMasked", "TESTNAME", "SYN-LAST-0001", "v_ace_account.contract_no", "ace-service/src/test/resources/recovery/legacy-seed.sql", 30 November 2026, 1 December 2026, "src/modules/recovery/caserecord", "console.log(customer.lastName)", "No case for ", "ContactEntity"; the field names first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value; the roles RW-TRIBE and RW-COMPLY; and the TechX tech leads as code owners. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **squad member (RW-TRIBE)** and a **member of the platform team that owns the service template (TechX)**, I want **the PDPA lint delivered as one generated step of the golden pipeline and of the service template, so that every one of the 19 repositories generated from the template runs the same rule set at the same version, the personal field marks are read from one pinned dictionary version served by the reference-data contract of rwb-case, the ACE field definitions arrive only through the owner's contract or the `v_ace_*` views, and an allow-list change is approved by the role that the role-to-permission matrix of rwb-access names**, so that **personal data never reaches code, test fixtures, log statements, exception messages, build artifacts or prompts to coding agents, and any finding in any repository is explained by the one dictionary version that its build record names**.

The rework keeps the lint and changes the object it reads. In the monolith the lint reads a `sys_fields` seed file and the API specification inside one repository, generates `pdpa-rules.yaml` there, and runs once in one pipeline. The target has 19 repositories generated from one service template, each with its own `rwb_<name>` schema and its own login, and no repository may read another service's tables (Arch v5 slide 29). A rule generator copied into 19 repositories is 19 rule sets that drift; a dictionary read per repository is 19 answers to one question. The legacy lint was never built (the legacy story is Ready for build, this story is Not started), so no built code is discarded, the six rule ids and every fixture value are carried unchanged, and the change is the source of the marks, the place the step is generated, the approver of an allow-list change and the read of the release quality view.

##### 2. Business rationale

Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal field marks and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero in every repository, not only in one.

The split makes the lint a property of the estate rather than of one build. Arch v5 slide 11 makes the contract the first artefact of every service and runs contract tests in every build; slide 20 gives every service the same block from the service template and the shared libraries; slide 29 fixes one schema and one login per service with no cross-schema read and a boundary test in every build; slide 35 places personal data in the owning service, masked and encrypted, never in events or workflow payloads, with the masking rules of P4 enforced in each service, and holds the pipeline to NIST SP 800-204C and 800-204D; slide 47 records the risk "Schema rules broken over time", its impact "Hidden coupling between services", and the mitigation "Database grants per schema; boundary test in every build; review of every new grant", owned by Architecture. A lint generated once from one pinned dictionary version is how 19 builds give one answer; a lint generated per repository is how the estate re-learns the same personal field 19 times, differently.

Three moves follow. The marks become reference data: the dictionary is served by the reference-data contract of rwb-case (DP-07), `sys_fields` is owned by P1 rwb-source-data in `rwb_source_data`, and the ACE field definitions are reached only through the owner's contract or the `v_ace_*` views (DP-05, slide 29). The allow-list approval becomes an authorisation decision: the approver role comes from the role-to-permission matrix as data behind the authorise contract of rwb-access (DP-08), and the repository host still enforces the merge rule. And the release quality view a role reads — findings per repository, per gate and per dictionary version — arrives through a gateway-bff composite route (DP-19); this story provides no screen and invents no route. The folder rules and the boundary test the step plugs into stay with RWB-PLT-TE001-APP, which is tracked and does not block this build.

##### 3. Preconditions

- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case and its client library (DP-07). The dictionary version and the personal field marks are read through it and are never a value in the lint.
- **RWB-PLT-E1037-CON** is published: the authorise contract of rwb-access and the guard library (DP-08). The approver role of an allow-list change is resolved through it.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The release quality view a role reads is behind that route; this story publishes no route of its own.
- The **two service CON dependencies** are published: **RWB-P3-E1043-CON**, the rwb-case contract behind the reference data (DP-07), and **RWB-P4-E1037-CON**, the rwb-access contract behind the authorise call (DP-08). Both are consumed as published contracts and their fakes, so neither blocks the build (Template and Rules §R5.4, C).
- The service template and the golden pipeline exist, and the 19 repositories are generated from that template (Arch v5 slides 11 and 20). RWB-PLT-TE001-APP supplies the folder rules and the boundary test this step plugs into; it is tracked, not blocking.
- The dictionary marks each personal field: `is_personal` in `sys_fields` in `rwb_source_data` (P1 rwb-source-data, Ownership Map) and `x-personal-data: true` in the API specification of the owning service.
- Synthetic test data uses the prefix "SYN-" for every value placed in a personal field (assumed convention of RWB-E1-065, kept).
- The masking helper of the common module is available for the rare log line that must name a record (assumed published as part of the common module's PII logging interface, kept).
- The pinned dictionary version, the operation that serves it and the rule-set version convention are Not specified in the source documents (GAP-1436; ASM-2525), and the release quality view is Not specified in the source documents (GAP-1436; ASM-2527); both are applied as the working defaults of section 13.

##### 4. Flow

1. Service template: the golden pipeline generates the PDPA step, the rule generator and the allow-list check from one definition, so a repository created from the template receives the same step and the same rule-set version as the other 18, and no repository holds a step of its own.
2. Build start: DictionaryVersionGuard reads the pinned dictionary version through the reference-data contract of rwb-case; when the contract does not answer, the step stops here and fails the build closed.
3. PersonalFieldReader: reads the marks of that version — the `is_personal` flag and `x-personal-data` — and never a value of any field.
4. RuleGenerator: generates `pdpa-rules.yaml` from the field list, with the Java getter names, entity class names, JSON property names and TypeScript property names of each marked field.
5. Lint: scans `src/main` and the front-end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.
6. Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.
7. Lint: checks that each entity with a personal field excludes it from its text form.
8. Lint: compares each finding with `pdpa-allow.yaml`; an entry past its expiry does not excuse the finding, and an entry without an owner, a reason or an expiry is refused at load.
9. RuleSetVersionRecorder: writes the dictionary version and the rule-set version into the build record of the repository, so a rerun of the same commit against the same version gives the same findings.
10. Pipeline: fails the build on any finding and prints the rule, the file, the line and the field, without printing the value found.
11. Allow-list change: the pull request is approved by the code-owner role of the repository, resolved through the authorise contract of rwb-access; the repository host refuses the merge without that approval.
12. Release quality view: a role reads findings per repository, per gate and per dictionary version through the gateway-bff composite route of RWB-PLT-N001-CON; this story adds no screen and no route.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A log statement writes a personal field | Build fails | Build log: PDPA-LOG-FIELD | AC1 |
| X2 | A log statement writes a whole personal entity | Build fails | Build log: PDPA-LOG-ENTITY | AC2 |
| X3 | A fixture holds a valid Thai national identifier | Build fails | Build log: PDPA-FIXTURE-ID | AC3 |
| X4 | A fixture holds a value in a personal field without the synthetic prefix | Build fails | Build log: PDPA-FIXTURE-FIELD | AC4 |
| X5 | A field is newly marked personal in the pinned dictionary version | The rule set is regenerated from that version and existing uses of the field are found | Build log: PDPA-LOG-FIELD | AC5 |
| X6 | An allow list entry is past its expiry | The finding fails the build | Build log: allow entry expired | AC6 |
| X7 | A front end console or logger call writes a personal property | Build fails | Build log: PDPA-LOG-FIELD | AC7 |
| X8 | A log statement writes a field through the masking helper | Passes | None | AC8 |
| X9 | An exception message carries a personal field | Build fails | Build log: PDPA-EXCEPTION | AC9 |
| X10 | An entity's text form includes a personal field | Build fails | Build log: PDPA-TOSTRING | AC10 |
| X11 | A person outside the code owners approves an allow list change | Merge refused; the code-owner role of the repository is the only approver the authorise contract returns | Repository host: review required from code owners | Access test TC-TE-011-11 |
| X12 | The reference-data contract does not answer at pipeline time | No rule set is generated and the build fails closed instead of passing with an empty rule set; the failure names the dictionary read, not a finding | Build log: dictionary version not read | AC11 |
| X13 | A repository resolves a rule-set version other than the pinned one | The build fails and names the repository and both versions; a stale rule set never excuses a finding | Build log: rule-set version mismatch | AC11 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the three platform contracts, the two service contracts of the run and the template; the marks arrive through a contract, so no service has to be built first; no screen and no route of its own |
| Negotiable | The synthetic prefix, the example domains, the allow list and the rule-set version convention are configuration; the rule ids, the field marks and the fail-closed behaviour are fixed by NFR-054, DL26 and Arch v5 slides 11, 20, 29 and 35 |
| Valuable | Personal data stays out of logs, artifacts and prompts in all 19 repositories, and one dictionary version explains every finding |
| Estimable | One generated pipeline step, one rule generator, one rule set, one allow list, one version recorder and one dictionary guard |
| Small | Fits in one sprint with its tests, in the template and one generated repository |
| Testable | Each legacy criterion is one fixture file with one finding; the new criterion runs the generated step in the template and in a second generated repository and compares their rule-set versions |

##### 7. Acceptance criteria

```gherkin
Feature: PDPA lint for code, tests and logs

  Background:
    Given the data dictionary marks first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value as personal

  Scenario: AC1 Log statement (legacy RWB-TE-011 AC1)
    Given a log statement in "recovery.casewf.internal.SampleService" that writes customer.getFirstName()
    When the pipeline runs
    Then the PDPA lint fails the build
    Then the build log names rule PDPA-LOG-FIELD, the file, the line and field first_name, and does not print a value

  Scenario: AC2 A whole entity in a log (legacy RWB-TE-011 AC2)
    Given a log statement that writes the object "customer" of type CustomerEntity
    When the pipeline runs
    Then the build fails with rule PDPA-LOG-ENTITY

  Scenario: AC3 A national identifier in a fixture (legacy RWB-TE-011 AC3)
    Given a JSON fixture whose "idNoMasked" holds a 13-digit number with a valid check digit, generated by the test at run time
    When the pipeline runs
    Then the build fails with rule PDPA-FIXTURE-ID

  Scenario: AC4 A personal field without the synthetic prefix (legacy RWB-TE-011 AC4)
    Given a SQL seed that sets last_name to "TESTNAME"
    When the pipeline runs
    Then the build fails with rule PDPA-FIXTURE-FIELD
    Then the same seed with last_name "SYN-LAST-0001" passes

  Scenario: AC5 A field newly marked personal (legacy RWB-TE-011 AC5)
    Given the rwb-case reference-data contract mock returns the dictionary version that marks v_ace_account.contract_no as personal
    Given the dictionary marks v_ace_account.contract_no as personal in a new version
    Given a log statement writes account.getContractNo()
    When the pipeline runs
    Then the system regenerates the rule set with contract_no
    Then the build fails with rule PDPA-LOG-FIELD for contract_no

  Scenario: AC6 An expired allow list entry (legacy RWB-TE-011 AC6)
    Given the allow list excuses PDPA-FIXTURE-FIELD in "ace-service/src/test/resources/recovery/legacy-seed.sql" until 30 November 2026
    When the pipeline runs on 1 December 2026
    Then the build fails with "allow entry expired"

  Scenario: AC7 The front end (legacy RWB-TE-011 AC7)
    Given a component in "src/modules/recovery/caserecord" that calls console.log(customer.lastName)
    When the pipeline runs
    Then the build fails with rule PDPA-LOG-FIELD for lastName

  Scenario: AC8 A masked value passes (legacy RWB-TE-011 AC8)
    Given a log statement that writes the contact point through the masking helper
    When the pipeline runs
    Then the lint passes for that line

  Scenario: AC9 An exception message (legacy RWB-TE-011 AC9)
    Given code that throws an exception with message "No case for " + customer.getCifNo()
    When the pipeline runs
    Then the build fails with rule PDPA-EXCEPTION for cif_no

  Scenario: AC10 The text form of an entity (legacy RWB-TE-011 AC10)
    Given ContactEntity includes contact_value in its text form
    When the pipeline runs
    Then the build fails with rule PDPA-TOSTRING for contact_value

  Scenario: AC11 One pinned dictionary version and every one of the 19 repositories (new, D-RCV-60)
    Given the service template publishes the PDPA step and its rule set as part of the golden pipeline
    Given the 19 repositories are generated from that template
    When every one of the 19 builds runs the step
    Then every repository runs the same rule-set version, generated from one pinned reference-data version read through the rwb-case reference-data contract
    Then the lint records that dictionary version and the rule-set version in the build record of each repository
    When the dictionary version cannot be read at pipeline time
    Then the build fails closed and no repository passes with an empty rule set
    When a repository is inspected for a read of another service's schema, or of a sys_fields table it does not own
    Then no such read exists, because the marks arrive through the contract and no repository opens rwb_source_data
```

**Note on the criteria.** AC1 to AC10 are the legacy criteria of RWB-TE-011, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed. AC5 gains one `Given` line, the reference-data contract mock, because the dictionary is no longer a seed file in the repository: the marks are reference data behind the rwb-case contract, and the AC5 version that marks `v_ace_account.contract_no` as personal is answered by that mock; every legacy `Given`, `When` and `Then` of AC5 is kept as written. AC11 is the only new criterion and it names no business value: it tests that the step is generated by the service template, that all 19 repositories run the same rule-set version from one pinned dictionary version, that the version is recorded in the build record, that an unreadable dictionary fails the build closed, and that no repository reads another service's schema.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The personal field list is read from one pinned version of the data dictionary, served by the reference-data contract of rwb-case; it is never written in the lint and never copied into a repository | Logical Data Model, Personal data column; API x-personal-data; DP-07 |
| BR2 | No log statement, string built for a log, or exception message carries a personal field or a whole personal entity | NFR-054; CTL-11 |
| BR3 | Test fixtures, seeds and end-to-end data carry only synthetic values with the prefix "SYN-" in personal fields | NFR-045; RWB-E1-065 |
| BR4 | Literals matching a Thai national identifier with a valid check digit, a Thai mobile number or an email outside the example domains fail anywhere in code or tests | NFR-054 |
| BR5 | An entity with a personal field leaves it out of its text form | CTL-11 |
| BR6 | A finding is excused only by an allow list entry with an owner, a reason and an expiry date not yet passed; the change that adds or renews the entry is approved by the code-owner role of the repository, resolved through the authorise contract of rwb-access | Principle 1 applied to build configuration; DP-08 |
| BR7 | The lint never prints the value it found | REQ-ACA-005 |
| BR8 | One rule set at one version is generated from one pinned dictionary version and is inherited by every repository generated from the service template; no repository adds, edits or suppresses a rule, and the build record of each repository names the dictionary version and the rule-set version it ran | Arch v5 slides 11, 20 and 29; this story (ASM-2525) |
| BR9 | The step fails closed: a dictionary version that cannot be read, a rule set that cannot be generated or a scan that errors fails the build and never passes it with an empty rule set | Arch v5 slide 35; this story (ASM-2525) |

##### 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a finding is not excused.

| From | Event | Condition | To |
|---|---|---|---|
| Not started | The step starts | The pinned dictionary version is read through the reference-data contract | Rules generated |
| Not started | The dictionary read does not answer | None | Failed closed |
| Rules generated | The scan starts | The rule set is written at the pinned rule-set version | Scanning |
| Rules generated | The rule set is empty | None | Failed closed |
| Scanning | No finding, or every finding excused by a live allow entry | None | Passed |
| Scanning | A finding is not excused | None | Failed |
| Scanning | The scan errors | None | Failed closed |
| Failed | A fix is built | The fix removes the finding, or adds an allow entry approved by the code-owner role | Rules generated |
| Failed closed | A fix is built | The dictionary version is readable and the rule set is generated | Rules generated |
| Passed | The same commit is rebuilt against the same dictionary version | None | Passed (same findings) |

The states are states of the pipeline step and of the build result, not of a case.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the lint in their repository; propose an allow list entry by pull request |
| TechX tech leads (code owners, RWB-TE-002) | Approve allow list changes and rule changes; the approver role is the code-owner role of the repository, resolved through the authorise contract of rwb-access |
| RW-COMPLY, Compliance and PDPA officer | Owns which fields are personal through the data dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |
| RW-PLATADM, platform administrator, and a role that reads the release quality view | Read findings per repository, per gate and per dictionary version through the gateway-bff composite route of RWB-PLT-N001-CON; write no finding and change no rule set |
| No role | May merge a finding past its allow entry, read another repository's build record, or edit the rule set outside the dictionary |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-ACE-055 | v_ace_customer | cif_no | Read (definition) |
| DF-ACE-057 | v_ace_customer | first_name | Read (definition) |
| DF-ACE-058 | v_ace_customer | last_name | Read (definition) |
| DF-ACE-073 | v_ace_customer | id_no_masked | Read (definition) |
| DF-ACE-059 | v_ace_customer | date_of_birth | Read (definition) |
| DF-EXT-002 | party_ext | vulnerable | Read (definition) |
| DF-ACE-061 | v_ace_customer | deceased_flag | Read (definition) |
| DF-EXT-004 | party_ext | bankruptcy | Read (definition) |
| DF-ACE-078 | v_ace_contact | contact_value | Read (definition) |
| DF-INT-011 | interaction | summary | Read (definition) |
| DF-DOC-015 | document_field | field_value | Read (definition) |

The lint reads which fields are personal; it never reads their values. Field IDs are those in the Logical Data Model and Data Dictionary.

The marks are now reference data. `sys_fields` lives in `rwb_source_data` and is owned by P1 rwb-source-data (Ownership Map); the ACE field definitions arrive only through the owner's contract or the `v_ace_*` views (DP-05; Arch v5 slide 29), and no repository opens `rwb_source_data` or any other service's schema. `party_ext` now lives in `rwb_source_data` and `document_field` and `interaction` are owned by `rwb_document` (P5) and `rwb_source_data` (P1) respectively; the lint reads only their definitions from the dictionary and never a row of any of them, because the entity and field names it needs are metadata and not data (DP-01).

The pinned dictionary version, the operation that serves it and the rule-set version convention are Not specified in the source documents (GAP-1436; ASM-2525); the lint takes the working defaults of section 13 until the gap closes.

##### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it has no REST base, no topic, no task queue and no schema of its own, and none is invented for it. The step runs inside the pipeline of each repository it is generated into.

###### 12.1 REST operations provided

None. The lint is a build step and provides no REST operation: the platform row has no REST base, no topic, no task queue and no schema of its own, and no path is invented for it. A developer reads a finding in the pull request checks, and a role reads the release quality view through the gateway-bff composite route of RWB-PLT-N001-CON, which this story consumes and does not publish.

###### 12.2 REST operations consumed

None as a path of this story. The step calls the two contracts below at pipeline time and repeats no path, version or payload of either; the dictionary path is published by the contract story that owns it.

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1043-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1043-CON`, epic RWB-PLT-LIB) | The reference-data contract that serves the pinned dictionary version and the personal field marks the rule set is generated from (DP-07) |
| `RWB-P4-E1037-CON` | P4 rwb-access (the platform contract behind it is `RWB-PLT-E1037-CON`, epic RWB-PLT-LIB) | The authorise envelope and the approver role of an allow-list change, resolved from the role-to-permission matrix (DP-08) |

###### 12.3 Events published

None. A build step publishes no business event; a finding is a build log line and a build record row, and neither is a Kafka event.

###### 12.4 Events consumed

None. The step is synchronous: it is started by the pipeline, reads the dictionary through the contract and produces its result in the same run, and it waits on no topic.

###### 12.5 Workflows and activities

None. A build step is not a Temporal workflow or activity; it starts nothing on a service task queue and awaits no child workflow.

###### 12.6 Schedules

None. The step runs on every pull request and every build of main, not on a schedule, and it creates no Temporal Schedule.

###### 12.7 Tables owned

None. `pdpa-rules.yaml` and `pdpa-allow.yaml` are build artefacts of the repository, not tables; the marks are rows of `sys_fields` in `rwb_source_data`, owned by P1 rwb-source-data, and this story owns no table in any schema.

###### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case reference-data fake | `RWB-P3-E1043-CON` behind the reference-data contract | One pinned dictionary version that marks first_name, last_name, cif_no, id_no_masked, date_of_birth, contact_value, summary and field_value as personal, and the AC5 version that also marks v_ace_account.contract_no; no value of any field, and no answer at all for the fail-closed case (AC11) |
| rwb-access authorise fake | `RWB-P4-E1037-CON` behind the authorise contract | The code-owner role of the repository granted the approval of an allow-list change, and a squad member outside the code owners refused with the documented refusal; the story has no Workbench endpoint, so no Workbench message ID is shown (TC-TE-011-11) |

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 2 consumed | The rwb-case reference-data read of the pinned dictionary version and the marks, and the rwb-access authorise read of the approver role, one hop each at pipeline time; none provided |
| Kafka | None | No event is published or consumed by the step |
| Temporal | None | A build step is not a workflow or an activity |
| File | 3 | The generated rule set `pdpa-rules.yaml`, the allow list `pdpa-allow.yaml`, and the source, test and fixture folders the scan reads in the repository of the build |

##### 13. Solution plan

**Package.** `tools/pdpa-lint` as the one definition consumed by every repository generated from the service template (the legacy package is kept). The step and its rule set are published by the template and the golden pipeline, and a repository holds no copy it may edit.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-05 | AceSourceQuery, `v_ace_*`, account_ext | Read through rwb-source-data's contract or the service's own ACE views | none |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-08 | RecoveryAccessGuard | Authorise contract of rwb-access and the guard library | H RWB-PLT-E1037-CON; C RWB-P4-E1037-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PersonalFieldReader | Service | Reads the personal field marks of the pinned dictionary version through the reference-data contract of rwb-case (BR1) |
| RuleGenerator | Service | Writes `pdpa-rules.yaml` with name variants: snake case, Java getter, camel case property (BR2 to BR5) |
| pdpa-rules.yaml | Rule table | The generated rules, at the rule-set version derived from the dictionary version (BR8) |
| pdpa-allow.yaml | Rule table | Allow list entries with owner, reason and expiry, refused at load when one is missing (BR6) |
| CheckDigitMatcher | Service | Thai national identifier check-digit test for BR4 |
| PdpaLintStep | Job | The pipeline step generated by the template: runs the scan and prints findings without values (BR7) |
| RuleSetVersionRecorder | Service | Writes the dictionary version and the rule-set version into the build record of the repository (BR8) |
| DictionaryVersionGuard | Service | Fails the build closed when the dictionary version cannot be read or the rule set cannot be generated (BR9) |

**Database.** None. The `sys_fields` seed is no longer read as a file: the marks arrive through the reference-data contract of rwb-case, and `sys_fields` in `rwb_source_data` is behind that contract, owned by P1 rwb-source-data (DP-01, DP-05, DP-07). The dictionary version and the operation that serves it are Not specified in the source documents (GAP-1436; ASM-2525).

**Configuration and reference data.**

- `rwb.pdpa.synthetic-prefix=SYN-`, the assumed convention of RWB-E1-065, kept.
- `rwb.pdpa.example-email-domains`, the domains that a fixture may use; every other address fails BR4.
- `rwb.pdpa.allow-list=pdpa-allow.yaml`: rule, path, line or pattern, owner, reason and expiry date; owned by the TechX tech leads through code owners.
- `rwb.pdpa.dictionary-version`: the one pinned reference-data version the rule set is generated from, read through the contract and never a value in the lint.
- `rwb.pdpa.rule-set-version`: derived from the dictionary version and the generator version, so the same version always produces the same rules.
- The personal field marks are owned by Compliance (DL26); the approver role of an allow-list change is the code-owner role, read from the role-to-permission matrix behind the authorise contract (DP-08).

**Build steps**

1. Publish the step, the rule generator and the allow-list check once in the service template and the golden pipeline, and prove that a repository created from the template runs them at the same rule-set version (AC11).
2. Write DictionaryVersionGuard and PersonalFieldReader against the rwb-case reference-data fake; prove that a dictionary that does not answer fails the build closed (AC11).
3. Write RuleGenerator with the snake case, Java getter, camel case and TypeScript variants; test that a newly marked field appears in the rules (AC5).
4. Write the log, entity, exception and text-form rules for Java and TypeScript with one fixture each (AC1, AC2, AC7, AC9, AC10).
5. Write the fixture rules and CheckDigitMatcher (AC3, AC4).
6. Add the masking helper exception to the log rules (AC8), and the allow-list handling with expiry and the code-owner approval through the authorise contract (AC6).
7. Write RuleSetVersionRecorder, add the step to the pull request pipeline, and confirm it prints no value and reads no other service's schema (AC11).

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The twelve test cases of section 16 pass, the step runs from the template in every one of the 19 generated repositories at one rule-set version, a dictionary that cannot be read fails the build closed, and main shows zero findings.

The pinned dictionary version, the operation that serves it, the rule-set version convention and the release quality view are Not specified in the source documents (GAP-1436; ASM-2525; ASM-2527); the version and its fail-closed read are ASM-2525, the approver role is ASM-2526 and the release quality view is ASM-2527.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A finding | {rule}: {file}:{line} uses personal field {field}. Remove it or use the masking helper. |
| Build log | An expired allow entry | allow entry expired: {rule} {path} since {date} |
| Repository host | An allow list change without a code owner approval | Review required from code owners |
| Build log | The reference-data contract does not answer at pipeline time | dictionary version not read: {repository} at {dictionaryVersion}. No rule set was generated and the build fails closed. |

Build log text is for developers and is not part of the message standard. The fourth row is the fail-closed read of the pinned dictionary version; it prints the repository and the version it asked for, and never a value of any field.

##### 15. Screens and states

No screen in this story. Developers read the findings in the pull request checks, one line per finding with the rule, the file, the line and the field name. The release quality view — findings per repository, per gate and per dictionary version — is a gateway-bff composite route of RWB-PLT-N001-CON (DP-19); this story provides no screen, report or route of its own and invents none.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-011-11 | Access | End to end | An allow list change approved only by a squad member outside the code owners; the merge is refused. This story has no Workbench endpoint, so MSG-P4-002 is not shown |
| TC-TE-011-01 | AC1, BR2, BR7 | Component | Fixture log line with getFirstName() |
| TC-TE-011-02 | AC2, BR2 | Component | Fixture log line with a PartyEntity object |
| TC-TE-011-03 | AC3, BR4 | Component | JSON fixture with a 13-digit number with a valid check digit, made for the test |
| TC-TE-011-04 | AC4, BR3 | Component | SQL seed with and without the SYN- prefix |
| TC-TE-011-05 | AC5, BR1 | Component | Dictionary version marking contract_no personal |
| TC-TE-011-06 | AC6, BR6 | Component | Allow entry expiring 30 November 2026, run on 1 December 2026 |
| TC-TE-011-07 | AC7, BR2 | Component | Front end console.log of lastName |
| TC-TE-011-08 | AC8 | Component | Log line through the masking helper |
| TC-TE-011-09 | AC9, BR2 | Component | Exception message with getCifNo() |
| TC-TE-011-10 | AC10, BR5 | Component | ContactEntity text form with contact_value |
| TC-PLT-TE011-APP-12 | AC11 | Integration | The service template with the generated step and two repositories created from it; one pinned dictionary version read through the rwb-case fake, the same rule-set version in both build records, then a dictionary that returns no answer and a repository pinned to a different rule-set version |

The eleven legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the legacy `System` rows TC-TE-011-01 to TC-TE-011-10 become Component, and the legacy Access row TC-TE-011-11 becomes End to end. TC-PLT-TE011-APP-12 is the new row for AC11. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

##### 17. Guardrails

- No business value in code: the personal field marks come from the reference-data contract of rwb-case, and the patterns, the synthetic prefix and the allow list are configuration (DP-07).
- No personal data in logs, tests or prompts: the lint prints field names only and generates its own check-digit fixtures at run time, and no fixture or finding stores a value.
- No read of another module's or another service's tables: the step reads files and the dictionary contract, never `rwb_source_data` or any other schema, and the boundary test of RWB-PLT-TE001-APP fails a cross-schema reference before it could ship (DP-01, DP-05; Arch v5 slide 29).
- An allow-list entry always has an owner, a reason and an expiry date, and its change is approved by the code-owner role resolved through the authorise contract (DP-08).
- The rule-set version always travels with the build record, so a finding is reproduced against the dictionary version that produced it (BR8).
- The step is generated by the template and is never edited in a repository; a change to a rule is a change to the dictionary or to the template, and the build record names both versions (Arch v5 slides 11 and 20).
- The step fails closed: no answer from the dictionary, no rule set, or a scan error is a failed build and never a pass (BR9; Arch v5 slide 35).

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Personal data is masked by role in line with PDPA | Business Requirements Program, section 6.7 | None | All recovery processes | None | TC-TE-011-03 to TC-TE-011-06, TC-TE-011-11, TC-PLT-TE011-APP-12 |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call | Business Requirements Program, section 6.9 | None | All recovery processes | None | TC-TE-011-01, TC-TE-011-02, TC-TE-011-07 to TC-TE-011-10, TC-PLT-TE011-APP-12 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | The step reads no table of any service; the marks arrive through a contract, and the rule set is a build artefact of its own repository | TC-PLT-TE011-APP-12 |
| DP-05 | Template and Rules §R5.5; Arch v5 slide 29 | The ACE field definitions are reached only through rwb-source-data's contract or the `v_ace_*` views, never from a repository read of `rwb_source_data` | TC-TE-011-05, TC-PLT-TE011-APP-12 |
| DP-07 | Template and Rules §R5.5 | The dictionary version and the personal field marks are read through the reference-data contract of rwb-case | TC-TE-011-05, TC-PLT-TE011-APP-12 |
| DP-08 | Template and Rules §R5.5; Arch v5 slide 35 | The approver of an allow-list change is the code-owner role resolved through the authorise contract of rwb-access | TC-TE-011-11 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 20 | The release quality view is a gateway-bff composite route; this story provides no route of its own | TC-PLT-TE011-APP-12 |
| Arch v5 slide 11 | Every service publishes its contracts before code, and contract tests run in every build | The step and its rule set are published by the template, and the contract read of the dictionary is a contract test in every build | TC-PLT-TE011-APP-12 |
| Arch v5 slide 29 | One schema and one login per service; no cross-schema read; a boundary test in every build | The dictionary is read through the owner's contract, and no repository opens `rwb_source_data` or another service's schema | TC-PLT-TE011-APP-12 |
| Arch v5 slide 35 | Personal data stays in the owning service, masked, and the pipeline follows 800-204C and 800-204D | The step fails closed, prints no value, and the marks are masked-by-role data owned by Compliance | TC-TE-011-01, TC-TE-011-09, TC-PLT-TE011-APP-12 |
| Arch v5 slide 47 | Risk "Schema rules broken over time", mitigated by grants per schema, a boundary test in every build and review of every new grant | The step runs from the template at one version, and the allow-list approval is a reviewed role decision | TC-TE-011-11, TC-PLT-TE011-APP-12 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1043-CON, RWB-PLT-E1037-CON, RWB-PLT-N001-CON | Contract | H: the reference-data contract, the authorise contract and the gateway-bff route contract this story builds against |
| RWB-P3-E1043-CON, RWB-P4-E1037-CON | Contract | C: the two service contracts consumed at pipeline time, as published contracts and fakes |
| RWB-PLT-TE001-APP | APP | X: it owns the folder rules and the boundary test this step plugs into; tracked, not blocking |
| RWB-PLT-NF05-OPS | OPS | The gate set that hosts this step; the step is a gate member and does not define the gate set |
| RWB-PLT-NF04-OPS | OPS | The secret and personal-data gate rules that the step consumes for the pattern side; this story owns the dictionary-driven field rules only |

##### 19. Out of scope

- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054; RWB-PLT-NF05-OPS and RWB-PLT-NF04-OPS).
- Masking rules by role at run time (RWB-E1-037, delivered by RWB-P4-E1037-CON).
- Masked data in SIT and UAT (RWB-TE-004, delivered by RWB-PLT-TE004-APP).
- Which fields are personal and how long they are kept: Compliance owns them under DL26.
- The dictionary registry operation itself, and the `sys_fields` rows behind it: rwb-source-data (P1) owns them and RWB-P3-E1043-CON publishes the read path.
- The contents of `RWB-PLT-E1043-CON`, `RWB-PLT-E1037-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1043-CON` and `RWB-P4-E1037-CON`; this story builds against them and adds no path.


## RWB-TE-012 Document storage containers

Legacy disposition: Moved (no impact).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-PLT-TE012-APP | App development | RWB-PLT-TPL | L-PLT-TPL-R | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-PLT-TE012-APP Document storage containers
SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-PLT-TE012-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | platform |
| Service epic | RWB-PLT-TPL |
| Wave | 0 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-012 |
| Legacy disposition | Moved (no impact) |
| Build status | Not started |
| Patterns applied | DP01, DP06, DP07, DP10, DP11, DP13, DP19 |
| Parallel lane | L-PLT-TPL-R |
| Ready to start | Day 1 |
| Depends on (build) | RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON |
| Contract dependencies | RWB-P3-E1042-CON, RWB-P3-E1043-CON |
| Integration dependencies | None |
| External dependencies | RWB-PLT-TE001-APP |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-028, FR-PLT-029) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: RWB-TE-012 is moved with no impact, and this story is the target shape of the same storage. Every legacy rule, criterion, message and value is kept word for word: the four containers `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, blob versioning and 30 days of soft delete on `rwb-docs`, the time-based immutability policy of 3650 days locked in PROD only, managed-identity-only access with shared key access off and public network access off, the 10-second timeout, the identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR, RWB-PROD-SY-OCR and RWB-SIT-SY-AGENT, the storage error strings, MSG-P5-002, MSG-GEN-006 and MSG-P4-002, and the `rwb.dochub.*` properties with the feature flag `rwb.dochub.storage-containers`. What changes is the shape: the storage now belongs to one owner, rwb-document (P5), so the in-process `DocumentContainers` interface becomes a published, versioned contract consumed one hop with a fake and a 2 s budget, the retention period, the soft-delete days and the container names become parameters and reference rows read through the contracts of rwb-case, the retention run becomes a Temporal Schedule on the task queue `rwb-document` instead of the legacy job, and the upload path a screen calls is the per-service base path `POST /api/recovery/document/v1/cases/{caseId}/documents` behind the gateway-bff composite route. AC1 to AC12 are the legacy criteria with the origin tag added and only that path re-pointed; AC13 is the one new criterion. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one set of blob containers per environment — `rwb-intake`, `rwb-docs`, `rwb-docs-legal` with a time-based immutability policy, and `rwb-quarantine` — reached by managed identity only, published as the container contract of rwb-document with a fake, with the container names, the retention period and the soft-delete days read as parameters and reference rows, and swept by a Temporal Schedule on the task queue of rwb-document, instead of an in-process `DocumentContainers` interface reached from inside the monolith**, so that **legal documents cannot be overwritten, no service other than rwb-document holds a container client, a key or a shared access signature, and the storage is set up once for the single owner of documents with no business value in its code**.

The legacy story sets up the storage: one storage account per environment with a private endpoint, the four containers, blob versioning and soft delete on `rwb-docs`, a time-based immutability policy on `rwb-docs-legal` (locked in PROD only), managed-identity-only access, a readiness indicator that joins the health endpoint, an error mapper, a content-hash guard and the upload path that shows 409 MSG-P5-002 and 503 MSG-GEN-006. None of that behaviour is withdrawn here. What the realignment changes is who owns the storage and how the rest of the estate reaches it. Arch v5 gives documents to rwb-document (P5), which owns metadata, custody, OCR text and fields, signatures and retention, and states that documents go to Blob with WORM through rwb-document only (slides 16, 29 and 41). A container client can no longer be handed to another module, because there is no module that shares a process with it. The platform half this story owns is therefore the storage itself — the account settings, the four containers, the policies, the role assignments, the readiness check, the error mapper, the hash guard and the retention Schedule template — plus the rule that the containers are reached only through the published contract of rwb-document. No other service opens a container, no platform table reaches a container, and no screen is given a storage credential.

##### 2. Business rationale

Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. A write-once container whose immutability policy refuses any overwrite or delete inside its retention period is the control that answers this: the legal copy of a court notice stays byte-identical for its class period, and every refused attempt is visible. This story is the storage that the document store, the intake and the malware scan write to, and it meets REQ-DCM-003 (legal document types held in a write-once container that cannot be altered or deleted) and REQ-DCM-002 (the document hub is the system of record and no other store holds the authoritative copy), both of which are Must.

Arch v5 moves the storage behind one owner. Slide 29 pairs the 19 schemas with one login each and names the storage in the same breath: Blob storage with WORM holds documents and it is for rwb-document only. Slide 41 gives rwb-document the ownership of metadata, custody, OCR text and fields, signatures and retention, its schema `rwb_document`, its first API path and its task queue `rwb-document`; slide 16 spells out that the service accepts `POST /documents` and that it runs a Schedule for retention over its WORM files, and that the same service reaches rwb-agent as a tool for read extracted fields. Slide 9 draws the line for the whole estate: documents go to Blob with WORM through rwb-document only. Slide 7 places the workbench inside the ACE platform behind the shared App Gateway, so the containers are an internal resource of one service and never a path a browser reaches. Slide 20 gives every service its own block of the template — own task queue, own Schedules, `/health` and `/metrics` for the platform — and gives gateway-bff one hop to an owner with a 2 s timeout and a breaker per service.

Three consequences follow, and they are the whole target change of this story. First, a single owner means a single contract: what the monolith expressed as the in-process `DocumentContainers` interface (four container clients and a readiness value) becomes a published, versioned contract of rwb-document, consumed by any other service one hop with a fake and a 2 s budget, so no caller can hold a container handle (DP-11). Second, a single owner means the storage carries no business value: the retention period, the soft-delete days and the four container names are parameters read through the parameters contract of rwb-case and reference rows read through its reference-data contract, because the platform carries no values of its own (DP-06, DP-07). Third, the legacy job that swept retention becomes a Temporal Schedule in the owning service, on the task queue `rwb-document` in the namespace `rwb-recovery`, with an overlap policy and a catch-up window, because Arch v5 replaces shared Quartz with Schedules in the owning service and JOB-17 retention is owned by rwb-document (DP-10; slide 44). The value the bank keeps is unchanged: a legal document cannot be changed or removed inside its retention period, and the standard container keeps earlier versions and restores a deleted blob inside the soft-delete window. What changes is that the guarantee now survives the split: one service issues the credential, one service writes the blob, one contract is the only way in, and the retention run cannot be started by a service that does not own the store.

##### 3. Preconditions

- **RWB-PLT-E1042-CON** is published: the parameters contract of rwb-case and its client library (DP-06). The retention period of a retention class, the soft-delete days and the cadence of the retention Schedule are parameter values read through it and never values in code.
- **RWB-PLT-E1043-CON** is published: the reference-data contract of rwb-case (DP-07). The retention classes — the class `LEGAL10Y` that the legacy story assumes at 3,650 days — and the document types with the class of each are reference rows read through it.
- **RWB-PLT-E1071-CON** is published: the Temporal workflow kit that carries the Scheduled job template and the overlap policy and catch-up window of a Schedule (DP-10). The retention Schedule is declared through it and not built by hand.
- **RWB-PLT-N001-CON** is published: the gateway-bff composite route contract (DP-19). The staff upload and the readiness surface are reached through it; this story publishes no route of its own.
- The **two service CON dependencies** are published: **RWB-P3-E1042-CON** (the rwb-case contract behind the parameters) and **RWB-P3-E1043-CON** (the rwb-case contract behind the reference data). Both are consumed as published contracts and their fakes, so neither blocks the build (Template and Rules §R5.4, C).
- **RWB-PLT-TE001-APP** is done: the recovery module folder and the boundary test that the storage code sits in. It is external, team-type work and is tracked, not blocking.
- The ACE storage pattern is used (DL27, option A): one storage account per environment in the SCB tenant with a private endpoint, shared key access off, public network access off and TLS 1.2 minimum.
- The managed identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR and RWB-PROD-SY-OCR exist, and rwb-document has its own managed identity in each environment: the legacy ACE service identity becomes the identity of rwb-document, which is the only holder of a container role.
- The infrastructure pipeline of the service template can apply storage templates to DEV and SIT.
- The feature flag `rwb.dochub.storage-containers` is a platform-library flag, read at start.
- Whether the storage account and the four containers stay one set per environment shared by the 19 services or become one set per service when only rwb-document may reach them, the container naming standard in the target, where the retention period and the retention classes are held now that they are parameters and reference rows, the name of the retention Schedule and the exact surface the readiness is read on are Not specified in the source documents (GAP-1438; ASM-2531). They are applied as the working defaults of section 13 until the gap closes.

##### 4. Flow

1. Platform administrator: applies the storage infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine`, whose names come from the container properties and not from a literal in the template body.
2. Template: turns on blob versioning and soft delete for `rwb-docs`, sets the time-based immutability policy on `rwb-docs-legal` with the retention days read as a parameter (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the rwb-document service identity on `rwb-intake`, `rwb-docs` and `rwb-docs-legal`; SY-OCR on `rwb-intake`, `rwb-docs` and `rwb-quarantine`. No other identity receives a container role.
3. System: on start, StorageReadinessIndicator reads the parameters and the reference rows, checks that the four containers exist and that `rwb-docs-legal` has its immutability policy, and joins the result to the service health endpoint (`/health`), so the platform collects one readiness per service.
4. rwb-document: writes each file through its storage adapter with its managed identity, to `rwb-docs-legal` for a write-once type and to `rwb-docs` for any other type, at the name `{container}/{caseId}/{documentId}/v{docVersion}`.
5. Any client: an overwrite or delete of a blob in `rwb-docs-legal` is refused by the storage service; StorageErrorMapper turns the refusal into `WriteOnceViolationException`, which rwb-document maps to 409 MSG-P5-002 on its own contract, and the attempt is written to the audit log.
6. rwb-document: a new version is a new blob at `v{n+1}`; the earlier blob stays readable.
7. Platform administrator: sees the document hub readiness on the interface and job monitor surface, which gateway-bff composes from the service health (DP-19), and the case owner uploads on the case documents screen through `POST /api/recovery/document/v1/cases/{caseId}/documents` on rwb-document's per-service base.
8. RetentionScheduleTemplate: creates the retention Schedule on the task queue `rwb-document`; when it fires, the service's own worker runs the retention activity, which reads the retention class of each document type through the reference-data contract and the retention period through the parameters contract, and acts on the store it owns.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Overwrite of a write-once blob | The storage service refuses; the blob is unchanged; rwb-document records the attempt in the audit log with the identity and the time | MSG-P5-002 | AC1 |
| X2 | Delete of a write-once blob | The storage service refuses; the blob is unchanged and still readable | MSG-P5-002 | AC2 |
| X3 | Access with an account key or a shared access signature | The storage service refuses the request | None | AC6 |
| X4 | Access by an identity with no role on the container | The storage service refuses the request | None | AC7 |
| X5 | Access from outside the private endpoint | The storage service refuses the request | None | AC8 |
| X6 | A container or the write-once policy is missing at start | rwb-document reports not ready and refuses every write; the readiness names the container | MSG-GEN-006 | AC9 |
| X7 | Storage does not answer within the 10-second timeout | `StorageUnavailableException`; the caller returns 503 on rwb-document's contract | MSG-GEN-006 | AC10 |
| X8 | A user session reads the quarantine container | Refused; only SY-OCR writes there | None | AC11 |
| X9 | A write to an existing blob name in `rwb-docs-legal` with the same content | The storage service refuses; the adapter compares the hash and returns the existing blob | None | AC12 |
| X10 | A role without Documents C uploads a document | 403 on the upload path | MSG-P4-002 | Access test TC-TE-012-13 |
| X11 | The reference-data contract does not answer when the retention class of a document type is asked | The write is refused, fail closed: no container is chosen, no blob is written and no document row is created, because the class that decides the container and the period is unknown | MSG-GEN-006 | AC9, AC13 |
| X12 | The retention Schedule does not run | The readiness and the job monitor report it; no document is deleted and no policy is applied outside its period | None | AC13 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the four platform contracts, the two rwb-case contracts and the module folder (RWB-PLT-TE001-APP); the document service builds against the container contract and its fake, so no service has to be finished first; no screen |
| Negotiable | The retention period, the soft-delete days and the container names are parameters and reference rows; the Schedule's cadence and overlap policy are configuration of the Scheduled job template; the account count per environment is the recorded assumption |
| Valuable | A legal document cannot be changed or removed inside its retention period, and no service other than rwb-document can reach the containers at all |
| Estimable | One storage template, one published contract with a fake, one configuration class, one readiness indicator, one error mapper, one hash guard and one Schedule declaration |
| Small | Settings, one small adapter layer and one Schedule template with tests; no business logic |
| Testable | Each criterion below runs against the SIT storage account and the two contract fakes, with the container contract fake of rwb-document for the caller side |

##### 7. Acceptance criteria

```gherkin
Feature: Document storage containers

  Background:
    Given the SIT storage account has containers "rwb-intake", "rwb-docs", "rwb-docs-legal" and "rwb-quarantine"
    Given "rwb-docs-legal" has a time-based immutability policy of 3650 days

  Scenario: AC1 Write-once (legacy RWB-TE-012 AC1)
    Given court notice "DOC-0701" stored at "rwb-docs-legal/RW-2026-000701/DOC-0701/v1" with hash "H701"
    When a client using the ACE service managed identity tries to overwrite it
    Then storage refuses the write with "BlobImmutableDueToPolicy"
    Then the blob hash is still "H701"
    Then the attempt is in the audit log with the identity and the time
    Then DocumentStore.replaceContent for "DOC-0701" raises WriteOnceViolationException, shown as 409 with MSG-P5-002

  Scenario: AC2 Delete is refused (legacy RWB-TE-012 AC2)
    Given court notice "DOC-0701" in "rwb-docs-legal"
    When a client using the ACE service managed identity tries to delete it
    Then storage refuses the delete
    Then the blob is still readable

  Scenario: AC3 A new blob in the write-once container is allowed (legacy RWB-TE-012 AC3)
    Given court notice "DOC-0701" at "v1" in "rwb-docs-legal"
    When the ACE service identity writes "rwb-docs-legal/RW-2026-000701/DOC-0701/v2"
    Then the write succeeds and both "v1" and "v2" are readable

  Scenario: AC4 The standard container keeps earlier versions (legacy RWB-TE-012 AC4)
    Given "rwb-docs/RW-2026-000702/DOC-0702/v1" holds an appraisal report
    When the blob is overwritten by the ACE service identity in SIT
    Then the previous blob version is still readable through blob versioning
    Then a deleted blob can be restored within the 30 days of soft delete

  Scenario: AC5 The identities hold only their roles (legacy RWB-TE-012 AC5)
    Given the role assignments applied by the template in SIT
    When the assignments are listed
    Then the ACE service identity holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-docs-legal" only
    Then "RWB-SIT-SY-OCR" holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-quarantine" only

  Scenario: AC6 Key-based access is refused (legacy RWB-TE-012 AC6)
    Given the storage account has shared key access disabled
    When a client calls "rwb-docs" with the account key or with a shared access signature
    Then storage refuses the request with "KeyBasedAuthenticationNotPermitted"

  Scenario: AC7 An identity with no role is refused (legacy RWB-TE-012 AC7)
    Given managed identity "RWB-SIT-SY-AGENT" has no role on "rwb-docs-legal"
    When it tries to read "rwb-docs-legal/RW-2026-000701/DOC-0701/v1"
    Then storage refuses with "AuthorizationPermissionMismatch"

  Scenario: AC8 Public network access is refused (legacy RWB-TE-012 AC8)
    Given public network access is disabled on the storage account
    When a client outside the private endpoint calls the account
    Then the system refuses the request

  Scenario: AC9 A missing immutability policy stops the document hub (legacy RWB-TE-012 AC9)
    Given the rwb-document upload contract mock returns 503 with MSG-GEN-006 while the document hub is not ready
    Given the immutability policy is removed from "rwb-docs-legal" in DEV
    When the service starts
    Then the readiness check reports the document hub as not ready, naming "rwb-docs-legal"
    Then an upload through POST /api/recovery/document/v1/cases/{caseId}/documents returns 503 with MSG-GEN-006
    Then the system writes no document row

  Scenario: AC10 Storage does not answer (legacy RWB-TE-012 AC10)
    Given the storage account does not answer within 10 seconds
    When BlobStorageAdapter writes a file to "rwb-docs"
    Then it raises StorageUnavailableException after 10 seconds
    Then the upload endpoint returns 503 with MSG-GEN-006

  Scenario: AC11 The quarantine container is closed to user sessions (legacy RWB-TE-012 AC11)
    Given file "Q-0001" in "rwb-quarantine"
    When the ACE service tries to read it on behalf of a case owner
    Then the system refuses the read
    Then only "RWB-SIT-SY-OCR" can write to "rwb-quarantine"

  Scenario: AC12 A repeated write of the same file is not an overwrite (legacy RWB-TE-012 AC12)
    Given "rwb-docs-legal/RW-2026-000703/DOC-0703/v1" holds a file with hash "H703"
    When BlobStorageAdapter is asked to write the same file with hash "H703" to the same name
    Then the system attempts no overwrite and the existing blob reference is returned
    Then the same name with a different hash raises WriteOnceViolationException

  Scenario: AC13 One owner, one contract and a Schedule for retention (new, D-RCV-60)
    Given the rwb-document container contract is published with its fake and a 2 s client budget
    Given the four container names and the retention period are read as parameters and reference rows
    When another service needs a document
    Then it calls the rwb-document contract one hop and holds no container client of its own
    Then no service but rwb-document holds a role or a credential on "rwb-intake", "rwb-docs", "rwb-docs-legal" or "rwb-quarantine"
    When the retention run starts
    Then the run is a Temporal Schedule on task queue "rwb-document" in namespace "rwb-recovery", and its cadence is a parameter
    When a case owner uploads a document on the case documents screen
    Then the screen calls POST /api/recovery/document/v1/cases/{caseId}/documents through the gateway-bff composite route, which is the per-service base path of rwb-document
```

**Note on the criteria.** AC1 to AC12 are the legacy criteria of RWB-TE-012, copied word for word with the origin tag added to each `Scenario` line; no legacy line and no legacy value was changed, and only the upload path in AC9 is re-pointed, because the single base of the legacy service is replaced by the per-service base of the owning service. AC9 gains one `Given` line as its first `Given`: the rwb-document upload contract fake returns 503 with MSG-GEN-006 while the document hub is not ready, so the same criterion can be proved with the fake before SIT carries a broken policy. AC13 is the only new criterion and it carries no business value: it tests the container contract, the single storage owner, the parameter and reference-data read, the retention Schedule and the upload path behind gateway-bff. The storage owner is rwb-document (P5) and no business rule changed.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-once container of rwb-document refuses overwrite and delete for the retention period; the policy is locked in PROD and unlocked in DEV, SIT and UAT so test data can be removed, and the period is the parameter `legalRetentionDays` 3650 read through the parameters contract, not a literal | NFR-029; CTL-12; template parameter legalRetentionDays 3650, assumed; DL26; DP-06 |
| BR2 | A change to a stored document is a new blob at the next version; earlier versions stay readable, and the version in the name is the `doc_version` of the owning service | FEAT-DCM-20; VR-P5-001-2; Arch v5 slide 41 |
| BR3 | Storage is reached only by managed identity; account keys and shared access signatures are disabled, and the identity that writes is the managed identity of rwb-document and of SY-OCR only | Story intent; CTL-09; Arch v5 slides 20 and 29 |
| BR4 | Each identity holds a role only on the containers it needs, and the four names are container properties read at start rather than literals in code or in the pipeline | Least privilege; roles of SY-OCR in roles.txt (Documents CRU); DP-06 |
| BR5 | rwb-document reports ready only when the four containers exist and the write-once policy is in place; the readiness joins the service health endpoint the platform collects | DL27; Arch v5 slide 20 |
| BR6 | The standard container keeps blob versions and soft-deleted blobs for 30 days, and the days are a parameter (`softDeleteDays` 30) read through the parameters contract | Template parameter softDeleteDays 30, assumed; DL27; DP-06 |
| BR7 | A write of identical content to an existing write-once name returns the existing blob; different content is a violation, and the period that decides the class comes from a reference row | R-UNI-40; CTL-12; DP-07 |
| BR8 | One owner holds the store: rwb-document (P5) owns metadata, custody, OCR text and fields, signatures and retention in `rwb_document`, and the containers with WORM are reached only through its published, versioned contract, consumed one hop with a fake and a 2 s budget; no other service holds a container client, a key or a shared access signature, and no platform table reaches a container | Arch v5 slides 9, 16, 29 and 41; DP-01; DP-11; ASM-2531 |
| BR9 | The retention run is a Temporal Schedule of rwb-document on the task queue `rwb-document` in namespace `rwb-recovery`, with an overlap policy and a catch-up window from the Scheduled job template; the cadence and the period it applies are configuration and reference rows, and no shared scheduler table is used | Arch v5 slide 44 (JOB-17, monthly, 1st Sunday); Ownership Map JOB-17; DP-10; Temporal design v1 slide 12 |

##### 9. State transitions

None. This story does not change a case status or a document status. It sets up containers, policies and role assignments.

The states below are the states of the readiness of rwb-document and of the retention run, and they change no business object.

| From | Event | Condition | To |
|---|---|---|---|
| Not ready | The service starts | A container is missing, or the immutability policy on `rwb-docs-legal` is absent, or the parameters or reference rows do not answer | Not ready (the readiness names the container or the contract) |
| Not ready | The readiness check passes | The four containers exist and the policy is present | Ready |
| Not ready | A write arrives | None | Refused with 503 and MSG-GEN-006; no blob and no document row |
| Ready | A write arrives | None | Ready (the write follows the class of the document type) |
| Ready | The immutability policy is removed or lapses | None | Policy lapsed (ready drops to not ready at the next check; writes refused) |
| Policy lapsed | The platform administrator reapplies the template | The policy is locked again | Ready |
| Ready | The retention Schedule fires | The Schedule is enabled and the worker polls its queue | Retention scheduled |
| Retention scheduled | A worker of rwb-document picks the run | None | Retention running |
| Retention running | The run completes | None | Retention scheduled (waiting for the next fire) |
| Retention running | The run fails | A storage error, or the parameters or reference rows do not answer | Retention failed (reported on the job monitor; no document deleted) |
| Retention failed | The platform administrator reruns the run or the next fire starts | None | Retention scheduled |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Applies the infrastructure template, reads the readiness check on the interface and job monitor surface, and reruns a failed retention run (Platform administration CRUD) |
| RW-SECADM, security administrator | Reviews the role assignments on the containers (Platform administration CRUDA) |
| SY-OCR, OCR and extraction pipeline | Writes to `rwb-intake`, `rwb-docs` and `rwb-quarantine` with its managed identity |
| RW-CASEOWN, case owner | Uploads documents through the contract of rwb-document, which uses its own managed identity (Documents CRU) |
| Solution architect with Compliance | Owns DL27 |
| No role | May reach a container directly, hold a container key or a shared access signature, ask rwb-document for a container handle, or delete inside the immutability period; every one of these is refused, and a role without Documents C is refused with MSG-P4-002 |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-006 | document | storage_ref | Read (format {container}/{caseId}/{documentId}/v{docVersion}) |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-011 | document | doc_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

`document`, `document_field` and `document_type` live in `rwb_document`, the schema of rwb-document (P5), per the Ownership Map and Arch v5 slide 41; no other service's schema is read by this story, and no platform table reaches a container (DP-01). `storage_ref` keeps the format `{container}/{caseId}/{documentId}/v{docVersion}` within varchar(400), and the three fields above are read by the storage and the retention code; the row that holds them is written by rwb-document and not by this story. The retention class of a document type is a reference row read through the reference-data contract of rwb-case, so no class value and no period sits in this code (DP-07).

##### 12. Contract

The service row of this story is `platform`, which is not one of the 19 service rows of Template and Rules §R4: it publishes no REST base, no topic, no task queue and no schema of its own. The store it sets up belongs to rwb-document (P5), and the names below are the names of that owner.

###### 12.1 REST operations provided

None by this story. The upload path `POST /api/recovery/document/v1/cases/{caseId}/documents` (Ownership Map row `POST /cases/{caseId}/documents`, owner P5; Arch v5 slide 16 gives `POST /documents`) belongs to rwb-document and is named here only as the path its callers use; this story adds no operation, and the platform reserves no REST base of its own.

###### 12.2 REST operations consumed

None as a path of this story. The contract dependencies are consumed as published contracts and their fakes, and no path, version or payload of one is repeated here:

| Contract dependency | Owner | What this story needs from it |
|---|---|---|
| `RWB-P3-E1042-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1042-CON`, epic RWB-PLT-LIB) | The parameters that carry the retention period of a class (3650 days, or the value of the class in force), the soft-delete days (30) and the cadence of the retention Schedule (DP-06) |
| `RWB-P3-E1043-CON` | P3 rwb-case (the platform contract behind it is `RWB-PLT-E1043-CON`, epic RWB-PLT-LIB) | The retention classes as reference rows — the class `LEGAL10Y` at 3650 days and the document types with the class of each — so the container and the period are chosen from a row and not from code (DP-07) |

The published container contract of rwb-document is consumed by the other services of the estate with a fake, one hop, a 2 s budget and a breaker per service (DP-11). Its operations and payloads belong to the contract stories of rwb-document and are not repeated here; this story only requires that the contract exists, is versioned, and hands out no container client.

###### 12.3 Events published

None. This story publishes nothing on a Kafka topic: the platform carries no topic of its own, and the document events `DocumentStored` and `DocumentFieldsExtracted` on `rwb.document.events.v1` belong to rwb-document (Arch v5 slides 16 and 42).

###### 12.4 Events consumed

None. The readiness check and the retention run read contracts and their own configuration; nothing in this story waits on a topic, and a document event is not a trigger for storage setup.

###### 12.5 Workflows and activities

| Workflow or activity | Task queue | Namespace | Owner | Use |
|---|---|---|---|---|
| Retention activity of the document hub (the retention run of JOB-17) | `rwb-document` | `rwb-recovery` | P5 rwb-document | Reads the reference row of each document type and its parameters, then applies retention to the store it owns; the platform contributes the Scheduled job template and the readiness of the run, not a worker of its own |

Arch v5 slide 16 gives rwb-document a `DocumentIntakeWorkflow` and a retention Schedule, and slide 44 gives JOB-17 the owner rwb-document with the mechanism Schedule; the Ownership Map gives JOB-17 the replacement "Temporal Schedule retention in rwb-document". The worker that runs the activity is the worker of rwb-document, so no platform worker is deployed and the platform task queue is not used.

###### 12.6 Schedules

| Schedule | Decides by | Overlap policy | Catch-up window | Instance |
|---|---|---|---|---|
| The retention Schedule of rwb-document (JOB-17), whose name is Not specified in the source documents (GAP-1438; ASM-2533) and whose cadence is a parameter, with the value given by Arch v5 slide 44 at monthly, 1st Sunday | A reference row and a parameter read through the reference-data and parameters contracts, never a value in code | Skip, as the overlap policy of the Scheduled job template | Bounded, as the catch-up window of the Scheduled job template | The Schedule and its worker belong to rwb-document on the task queue `rwb-document` in namespace `rwb-recovery`; this story declares the template, not the instance |

The value of the cadence comes from the job map, and the row that decides the run is the class of each document type; both are configuration of the owning service so that a change to either needs no code change. No shared scheduler table is created and no Quartz job is registered (DP-10; Temporal design v1 slide 32, "jobs as Schedules, no Quartz").

###### 12.7 Tables owned

None. This story owns no table of its own, and it writes no service table: `document`, `document_field` and `document_type` belong to `rwb_document`, the schema of rwb-document (P5), and the storage reference they carry is read by the storage code, never written by it (Ownership Map; Arch v5 slide 41; DP-01).

###### 12.8 Contract fakes

| Fake | Serves | Documented answer used by the tests |
|---|---|---|
| rwb-case parameters fake | `RWB-P3-E1042-CON` behind `RWB-PLT-E1042-CON` | The retention period 3650 days, the soft-delete days 30 and the cadence of the retention Schedule, as the parameter values in force for the environment (AC13, TC-PLT-TE012-APP-14) |
| rwb-case reference-data fake | `RWB-P3-E1043-CON` behind `RWB-PLT-E1043-CON` | The retention class `LEGAL10Y` at 3650 days and the document types with the class of each, so the write-once container is chosen from a row (AC1, AC12, AC13) |
| rwb-document container and upload contract fake | The published, versioned contract of rwb-document (P5), consumed one hop with a 2 s budget | A container handle that is opaque to the caller and no storage credential, 503 with MSG-GEN-006 while the document hub is not ready, and 409 with MSG-P5-002 on a write-once overwrite (AC9, AC13) |

The storage account itself is not faked: AC1 to AC8, AC10, AC11 and AC12 run against the storage account of the environment, because the policy, the roles, the private endpoint and the key refusal are properties of the account and cannot be proved against a stub.

###### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | 1 consumed, 1 named as the caller's path | The container contract of rwb-document, consumed by the other services one hop with a fake and a 2 s budget (DP-11), and the upload path `POST /api/recovery/document/v1/cases/{caseId}/documents` behind gateway-bff that the staff screen calls (DP-13, DP-19); nothing provided by this story |
| Kafka | None | No event is published or consumed; the document events belong to rwb-document |
| Temporal | 1 | The retention Schedule and its activity on the task queue `rwb-document` in namespace `rwb-recovery` (DP-10; JOB-17) |
| File | 4 containers, plus claim-check content | `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` on one storage account with a private endpoint; the content a claim-check message points at is served as a link by rwb-document, never as data in the message (Arch v5 slide 11) |

##### 13. Solution plan

**Package.** `recovery/dochub/storage`, Java package `recovery.dochub.storage`, kept from the legacy story, plus the storage part of the service template: the infrastructure template fragment that every service of the 19 applies when it needs a container, and the Scheduled job declaration of the workflow kit that rwb-document reuses for its retention run. The container clients are packaged so that only the owning service can construct them; the published contract of rwb-document exposes no client type.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-06 | Parameters, casewf.config | Parameters contract of rwb-case and the client library | H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Storage infrastructure template | Configuration | Account settings, four containers, versioning and soft delete on `rwb-docs`, the immutability policy on `rwb-docs-legal` with its days read as a parameter, and the role assignments of rwb-document and SY-OCR (BR1, BR3, BR4, BR6) |
| DocumentContainers published contract | Published contract | The versioned contract of rwb-document for a document and for the storage readiness of the hub; it hands out no container client, so a caller cannot reach a blob except through the owner (BR8; DP-11) |
| DocumentContainersConfig | Service | Builds the clients with DefaultAzureCredential restricted to managed identity, with the 10-second timeout and the four container names read from configuration (BR3, BR4) |
| StorageReadinessIndicator | Service | BR5: the four containers and the immutability policy are checked at start and on the readiness probe, and the result joins the service health endpoint |
| StorageErrorMapper | Service | Maps `BlobImmutableDueToPolicy` and the conflicts on `rwb-docs-legal` to `WriteOnceViolationException`, timeouts to `StorageUnavailableException`, and writes the audit event for a refused overwrite or delete (BR1, BR7) |
| ContentHashGuard | Service | BR7: compares the SHA-256 of an existing write-once blob before a write, and returns the existing reference when the content is identical |
| RetentionScheduleTemplate | Configuration | Declares the retention run as a Temporal Schedule on the task queue `rwb-document` with the overlap policy, the catch-up window, the cadence and the class of each document type read as configuration and reference rows (BR9; DP-10) |

**Database.** No new business table, and no table of its own. `storage_ref` values follow `{container}/{caseId}/{documentId}/v{docVersion}` within varchar(400) and are held by `document` in `rwb_document`, the schema of rwb-document (P5); this story reads the three fields of section 11 and writes none of them (DP-01).

**Configuration and reference data.**

- Properties per environment: `rwb.dochub.storage.account-url`, `rwb.dochub.container.intake`, `rwb.dochub.container.standard`, `rwb.dochub.container.legal`, `rwb.dochub.container.quarantine`, `rwb.dochub.storage.timeout-seconds` 10.
- Template parameters: `legalRetentionDays` 3650 (assumed; DL26), `legalPolicyLocked` true in PROD only, `softDeleteDays` 30 (assumed; DL27). The first and the third are the parameter values read through the parameters contract of rwb-case and are kept here only as the deployed defaults of the environment (DP-06).
- Retention classes as reference rows read through the reference-data contract of rwb-case: the class `LEGAL10Y` at 3650 days and the document types with the class of each; no class and no period is a literal in the code or in the pipeline (DP-07). The cadence of the retention Schedule and its overlap policy and catch-up window are configuration of the Scheduled job template (DP-10).
- Feature flag: `rwb.dochub.storage-containers`. Off, the readiness check reports not ready and every document write is refused with 503 rather than written outside the write-once container.

**Build steps**

1. Write the infrastructure template with the account settings, the four containers whose names come from configuration, the policies and the role assignments, and the retention days read as a parameter; apply it in DEV and SIT.
2. Build DocumentContainersConfig with managed identity credentials only, and test that a key-based client and a shared access signature are refused (AC6, AC8).
3. Build StorageErrorMapper with the audit event, and test AC1 and AC2 against the storage account of SIT.
4. Build ContentHashGuard and test AC12, including the class that decides the container.
5. Build StorageReadinessIndicator, join it to the service health endpoint, and test AC9 in DEV with the immutability policy removed.
6. Publish the container contract of rwb-document with its fake: an opaque handle, a 2 s client budget, a breaker per caller, 503 MSG-GEN-006 while not ready and 409 MSG-P5-002 on a write-once overwrite; test AC13 with the two contract fakes.
7. Declare the retention Schedule through the Scheduled job template on the task queue `rwb-document`, with the cadence, the overlap policy and the catch-up window as configuration, and test that a failing run reports failed and deletes nothing.

**Done when.** The test cases of section 16 pass in SIT, the template is applied in DEV and SIT, the security administrator has reviewed the role assignments, only rwb-document holds a container role, and the retention Schedule has run once and reported on the job monitor.

The account count per environment, the container naming standard, where the retention period and the classes are held, the name of the Schedule and the readiness surface are Not specified in the source documents (GAP-1438; ASM-2531); the single set of four containers, the legacy values 3650 and 30 days, the four legacy container names and the one Schedule on the task queue `rwb-document` are ASM-2531, ASM-2532 and ASM-2533.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | Overwrite or delete of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-006 | Storage unavailable or document hub not ready | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. |

The three texts are copied unchanged from RWB-TE-012 and this story adds no message text. In MSG-GEN-006 the {system} names the document hub when the readiness is the cause and the storage when the timeout is; X11 uses the same message because a write whose class cannot be read is a write the hub cannot serve. Thai text for each message follows decision DL10.

##### 15. Screens and states

No screen in this story, and no new screen state. The platform administrator sees the readiness of the document hub on the interface and job monitor surface, which gateway-bff composes from the service health and the job state through its composite route (DP-19); the story publishes no route, and the surface names the container or the Schedule that is not healthy, never a business value. The case owner uploads on the case documents screen (SCR-30 Case documents), which calls `POST /api/recovery/document/v1/cases/{caseId}/documents` on the per-service base of rwb-document through the same composite route (DP-13). The upload response carries MSG-P5-002 at 409 when the write-once container refuses a change, MSG-GEN-006 at 503 when the storage or the hub is not ready, and MSG-P4-002 at 403 when the role holds no Documents C.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-012-01 | AC1, BR1 | Component | Synthetic court notice in rwb-docs-legal |
| TC-TE-012-02 | AC2, BR1 | Component | Delete attempt on the same blob |
| TC-TE-012-03 | AC3, BR2 | Component | v2 blob for the same document |
| TC-TE-012-04 | AC4, BR6 | Component | Overwrite and delete in rwb-docs in SIT |
| TC-TE-012-05 | AC5, BR4 | Component | Role assignment listing in SIT |
| TC-TE-012-06 | AC6, BR3 | Component | Client with account key and with a shared access signature |
| TC-TE-012-07 | AC7, BR4 | Component | Managed identity RWB-SIT-SY-AGENT |
| TC-TE-012-08 | AC8, BR3 | Component | Client outside the private endpoint |
| TC-TE-012-09 | AC9, BR5 | Component | Policy removed in DEV |
| TC-TE-012-10 | AC10 | Component | Storage stub with a 10-second timeout |
| TC-TE-012-11 | AC11, BR4 | Component | File in rwb-quarantine |
| TC-TE-012-12 | AC12, BR7 | Component | Same and different content to an existing write-once name |
| TC-TE-012-13 | Access | End to end | RW-REFADM user (Documents -) calls POST /cases/{caseId}/documents; refused with MSG-P4-002 |
| TC-PLT-TE012-APP-14 | AC13 | Integration | The container contract of rwb-document with its fake and a 2 s budget, the parameters and reference-data fakes at 3650 days, 30 days and the class LEGAL10Y, and the retention Schedule on the task queue rwb-document, once with a failed run |

The thirteen legacy test case rows keep their ID, Covers and Data cells word for word, and only the Level cell is mapped to the target shape: the legacy storage and configuration rows TC-TE-012-01 to TC-TE-012-12 become Component, and the legacy Access row TC-TE-012-13 becomes End to end. TC-PLT-TE012-APP-14 is the new row for AC13. The full test, with its Given, When and Then, stays in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same TC ID.

##### 17. Guardrails

- No business value in code: the retention period, the soft-delete days and the four container names are parameters and reference rows read through the contracts of rwb-case (DP-06, DP-07), and the cadence of the retention Schedule is configuration of the owning service.
- No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic, and the readiness and the job monitor name a container or a Schedule, never content.
- No read of another service's tables (DP-01): `document`, `document_field` and `document_type` are read in `rwb_document` and nowhere else, and no platform table reaches a container. No other service holds a container client (DP-11): a caller reaches a document through the published contract of rwb-document, one hop, 2 s, with a breaker per service, and no container client, key or shared access signature leaves the owning service.
- No account key, connection string or shared access signature in code, configuration or the pipeline; shared key access stays off and public network access stays off, and access is only the managed identity of rwb-document and of SY-OCR.
- The immutability policy is locked in PROD only, and no role may delete inside the immutability period; the test environments stay unlocked so that synthetic data can be removed.
- No shared scheduler table and no Quartz job: the retention run is a Temporal Schedule in the owning service, so a failed run is visible and deletes nothing (DP-10; Temporal design v1 slide 32).

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-003 | Legal document types held in a write-once container that cannot be altered or deleted | Business Requirements Program, section 5.5 | FEAT-DCM-01 | 13 Manage documents and correspondence | R-UNI-40 | TC-TE-012-01 to TC-TE-012-03, TC-TE-012-09, TC-TE-012-12, TC-PLT-TE012-APP-14 |
| REQ-DCM-002 | The document hub is the system of record; no other store holds the authoritative copy | Business Requirements Program, section 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | None | TC-TE-012-04 to TC-TE-012-08, TC-TE-012-10, TC-TE-012-11, TC-TE-012-13, TC-PLT-TE012-APP-14 |

| Target element | Source | What this story does with it | Test cases |
|---|---|---|---|
| DP-01 | Template and Rules §R5.5; Arch v5 slide 29 | The storage reference and the document fields are read in the schema of the owner, `rwb_document`, and no other schema is read | TC-TE-012-09, TC-PLT-TE012-APP-14 |
| DP-06 | Template and Rules §R5.5 | The retention period, the soft-delete days and the cadence are parameter values read through the parameters contract of rwb-case, never literals | TC-PLT-TE012-APP-14 |
| DP-07 | Template and Rules §R5.5 | The retention classes and the document types are reference rows read through the reference-data contract of rwb-case | TC-TE-012-01, TC-TE-012-12, TC-PLT-TE012-APP-14 |
| DP-10 | Template and Rules §R5.5; Arch v5 slide 44 | The retention run is a Temporal Schedule on the task queue `rwb-document`, with the overlap policy and catch-up window of the Scheduled job template | TC-PLT-TE012-APP-14 |
| DP-11 | Template and Rules §R5.5; Arch v5 slide 20 | The in-process `DocumentContainers` interface becomes a published contract with a fake, one hop and a 2 s budget, so no caller holds a container client | TC-PLT-TE012-APP-14 |
| DP-13 | Template and Rules §R5.5 | The upload path a screen calls is the per-service base path of rwb-document, not the legacy single base | TC-TE-012-09, TC-PLT-TE012-APP-14 |
| DP-19 | Template and Rules §R5.5; Arch v5 slide 16 | The staff upload and the readiness are reached through the gateway-bff composite route, and this story publishes no route | TC-TE-012-13, TC-PLT-TE012-APP-14 |
| Arch v5 slide 16 | rwb-document accepts `POST /documents`, runs a Schedule for retention, and keeps files in Azure Blob with WORM | The upload path of the owner and the retention Schedule of the owner | TC-PLT-TE012-APP-14 |
| Arch v5 slide 29 | Blob storage with WORM holds documents for rwb-document only; one login and one schema per service | The single owner of the containers and the refusal of a container client to any other service | TC-TE-012-04 to TC-TE-012-08, TC-PLT-TE012-APP-14 |
| Arch v5 slide 41 | P5 owns metadata, custody, OCR text and fields, signatures and retention, in `rwb_document`, with `rwb-document` as its task queue | The owner of the store, the schema of the three fields and the queue of the retention run | TC-TE-012-09, TC-PLT-TE012-APP-14 |
| Arch v5 slide 44 | JOB-17 retention, monthly on the 1st Sunday, owner rwb-document, mechanism Schedule, overlap policy skip and catch-up window | The retention Schedule, its cadence value and its instance in the owning service | TC-PLT-TE012-APP-14 |
| Arch v5 slide 9 and 7 | Documents go to Blob with WORM through rwb-document only, inside the ACE platform behind the shared App Gateway | The containers are an internal resource of one service and no browser reaches them | TC-TE-012-08, TC-PLT-TE012-APP-14 |
| Arch v5 slide 20 | Every service is built from the template with its own queue and Schedules and publishes `/health` and `/metrics`; gateway-bff makes one hop with a 2 s timeout and a breaker per service | The readiness on the health endpoint, the Schedule of the owning service and the contract budget | TC-TE-012-09, TC-PLT-TE012-APP-14 |

| Story | Work type | Relation to this story |
|---|---|---|
| RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-E1071-CON, RWB-PLT-N001-CON | Contract | H: the parameters contract, the reference-data contract, the workflow kit with the Scheduled job template, and the gateway-bff route contract this story builds against |
| RWB-P3-E1042-CON, RWB-P3-E1043-CON | Contract | C: the two rwb-case contracts consumed at run time through their fakes |
| RWB-PLT-TE001-APP | APP | X: the recovery module folder and the boundary test the storage code sits in; tracked, not blocking |
| RWB-PLT-TE004-APP | APP | The masked copy of the same storage: it loads the masked extract into the schemas of the 19 services and reads the intake container, so it depends on this template and on the owner of the store |
| The document service stories of rwb-document (P5) | APP, CON | The store itself: the document row, the container chosen per document type, the upload endpoint and its screen, the custody and the retention job on JOB-17 are owned there, and this story sets up the storage they use |

##### 19. Out of scope

- Choosing the container per document type and writing the document row: rwb-document (P5) owns both, and this story only guarantees that a container is reachable through its contract.
- Retention classes, archive and the retention job: RWB-E1-041 in the legacy numbering, and JOB-17 which becomes the retention Schedule of rwb-document; the class values are reference rows of rwb-case.
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- The backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).
- The upload endpoint and its screen: rwb-document (P5) owns `POST /api/recovery/document/v1/cases/{caseId}/documents` and SCR-30 Case documents, and this story names the path only as its caller's path.
- The storage part of RWB-PLT-TE004-APP, which is the masked copy of the same storage and is a story of its own.
- The contents of `RWB-PLT-E1042-CON`, `RWB-PLT-E1043-CON`, `RWB-PLT-E1071-CON`, `RWB-PLT-N001-CON`, `RWB-P3-E1042-CON` and `RWB-P3-E1043-CON`; this story builds against them and adds no path.


## RWB-TE-013 Agent runtime client with fallback

Legacy disposition: Split (rework).

| New story | Work type | Service epic | Lane | Ready to start | Suggested owner |
|---|---|---|---|---|---|
| RWB-P10-TE013-CON | Contract | RWB-SVC-P10 | CG-W1 | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-P10-TE013-APP | App development | RWB-SVC-P10 | L-P10-A | After RWB-P10-E1058-APP | TechX (suggested; any team may pick up this story) |
| RWB-P7-TE013-APP | App development | RWB-SVC-P7 | L-P7-AR | Day 1 | TechX (suggested; any team may pick up this story) |
| RWB-P10-TE013-OPS | DevOps | RWB-SVC-P10 | L-P10-M | Day 1 | DevOps team (suggested; any team may pick up this story) |
| RWB-ITG-TE013-ITG | Integration | RWB-ITG-W1 | L-ITG-W1 | Day 1 | TechX (suggested; any team may pick up this story) |

### RWB-P10-TE013-CON Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-TE013-CON |
| Work type | CON (Contract) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | CG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-018, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: contract slice of RWB-TE-013 for rwb-agent. The legacy key is a published Java interface inside one deployment - `AgentStepClient`, `AgentStepRequest`, `RuleResult` and `AgentStepOutcome` in package `recovery.agent.api`, an `AgentOrchestrator.run` method call, a P7 `DecisionLogWriter` of the same process and a Quartz job step of RWB-TE-007. This document fixes that seam as a contract on Day 1: two operations on `/api/recovery/agent/v1` (**DP-13**, **DP-20**), their members in the legacy names, the step key as the idempotency key, the refusal set, the record payload written by the calling step through the local decision-record library and published as EV-08 (**DP-03**, **DP-09**), the workflow and activity contract on queue `rwb-agent` (**DP-10**), the two consumed boundaries of P3 and P7 (**DP-07**, **DP-03**) with one hop and 2 s (**DP-11**), the run read restated behind the gateway-bff route (**DP-19**) and the three fakes. Tables stay in `rwb_agent` only (**DP-01**) and the migration sequence stays the service's own (**DP-15**). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **tech lead**, I want **the rwb-agent side of the agent runtime client fixed as a contract on Day 1: the `AgentStepClient` operation on `/api/recovery/agent/v1/agent-steps` with its request members - agent code, case ID, decision code, step key, rule result and masked inputs - its answer members - record reference, applied result, recommendation, fallback, fallback reason, autonomy mode and run ID - its idempotency on the step key and its refusal set 401, 403, 409, 422 and 503; the link operation that sets the record reference on the run; the record payload written through the local decision-record library in the calling step's transaction; the run read restated from the baseline; and the three contract fakes**, so that **the app story, the deployment story, the calling stories and the integration copy build against one agreed, testable seam on Day 1, a repeat of a step key can never produce a second run or a second record, and no caller is offered an orchestrator call it is not allowed to see**.

##### 2. Business rationale

The legacy key was written against objects inside the monolith: `AgentStepClient` and `AgentStepRequest` were Java types in the same deployment as their caller, `AgentOrchestrator.run` was a method call, `DecisionLogWriter` was the P7 interface of the same process, and the step arrived through a Quartz job of RWB-TE-007 (legacy sections 4, 12 and 13). In the target each is a boundary or is gone:

- The orchestrator is `AgentRunWorkflow` on the rwb-agent task queue in namespace `rwb-recovery`, with the approved policy's 60 second budget inside it (Arch v5 slide 16; DP-20).
- The published interface becomes a REST contract with a fake, one hop, under `/api/recovery/agent/v1` (DP-11, DP-13; ADR-020).
- The `DecisionLogWriter` becomes the local decision-record library: the step writes its own record in its own schema and transaction, and rwb-decision collects it into the central ledger on `rwb.decision-record.v1` (DP-03; ADR-022).
- The rule result is not a shared bean: the embedded Drools kit evaluates the package published from rwb-decision and the caller passes the result in (DP-04; ADR-017).
- The Quartz job step is retired with RWB-TE-007 and becomes a Temporal step through the workflow kit (DP-10; ADR-016).

Contract-first only works if the seam is written down once. The seam is small and load-bearing: one operation whose request and answer are the legacy records, one link operation that keeps run and record joined, one idempotency rule on a key the whole legacy story is built on (R-UNI-40), one refusal set, one record payload with no personal data, and one fake set that makes the app and the deployment testable on Day 1.

With the shape agreed and faked on Day 1, four teams move at once: RWB-P10-TE013-APP builds the mode resolution, the timed run, the fallback, the record write and the link against these fakes; every calling story of wave 1 compiles against `recovery.agent.api`; RWB-P7-E1027-CON fixes the record type the contract names; and RWB-P10-TE013-OPS deploys the operations and the wiring against the same names. Without it each caller invents its own request, the idempotency of the step key is lost at the seam, and a record with no run or a run with no record becomes normal.

This story defines the provided side of the two operations and the record payload, and never restates what another owner holds: the eleven platform operations are baselined in RWB-P10-E1058-CON, the lists are rwb-case's, the record type and ledger are rwb-decision's and the run read is the baseline's (DP-01).

##### 3. Preconditions

- The service template and naming library are available (RWB-PLT-TPL), so the REST base, the error envelope and the CloudEvents envelope follow the platform rule (§R4; DP-13, DP-14).
- The agent platform contract of RWB-P10-E1058-CON is in force: the eleven operations, the eight agent tables, the EV-28 payload, the error taxonomy and AgentRunWorkflow with its six activities, on queue `rwb-agent` in namespace `rwb-recovery`.
- RWB-PLT-E1027-CON publishes the record shape, the local write in the calling transaction and `rwb.decision-record.v1` (DP-03); RWB-PLT-E1072-CON publishes the rule-package client and the rule-result shape, with packages and versions from rwb-decision (DP-04); RWB-PLT-TE006-CON publishes the envelope, the relay, the retry topic and the `.dlt` rule (DP-09); RWB-PLT-E1071-CON publishes the namespace, the queue rule and the activity contract (DP-10).
- RWB-P3-E1043-CON is published with its client library, and LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT are the values of TSD P10 Agent runtime v2 T3.2 (DP-07).
- The record read of rwb-decision is known: `GET /api/recovery/decision/v1/decision-log/{entryId}` answers one record by its reference (DP-03).
- No build dependency: this story is Day 1 by rule (§R5.7) and sits in contract group CG-W1.
- The operation paths, the member names beyond the legacy Java record members and the refusal semantics are this document's, because no source names a run-submit operation among the eleven P10 operations: Not specified in the source documents (GAP-0620; ASM-0908).

##### 4. Flow

1. Draft the step operation that replaces the legacy `AgentStepClient.runStep` call: method, path under `/api/recovery/agent/v1`, request members, answer members, idempotency on the step key and refusals (AC1, AC2, AC3).
2. Fix the call type and the budget at the boundary: one REST hop with a fake, and the policy timeout of 60 seconds as the recorded exception to the 2 s budget of DP-11, because the run is bounded by `agent_policy.timeout_seconds` and NFR-010 allows the full wait before the rule result is used (AC1; BR4).
3. Fix the two outcomes the caller depends on: the applied result always the rule result in SHADOW and L1, the recommendation only in L1, and the fallback with its reason TIMED_OUT, SCHEMA or NO_POLICY (AC2, AC3).
4. Fix the link operation and the rule that a run holds one record reference and a different reference is refused (AC4; BR6).
5. Declare the record payload written through the local library: record reference, decision code, agent version, model version, inputs reference, final call and actions {caseId, agentRunId, mode, fallback, fallbackReason}, published as EV-08 on `rwb.decision-record.v1`, with no personal field (AC5; DP-03, DP-09).
6. Restate the run read the callers and tests use from the baseline of RWB-P10-E1058-CON and declare the gateway-bff route in front of it (AC6; DP-19).
7. Write the three fakes with their answers, refusals and timings: the decision-record library and read, the rwb-case lists and the gateway-bff route (AC6).
8. Publish the nine sub-tables of section 12 and the contract tests, and tag the baseline for the app and deployment stories.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A member of the request or the answer drifts from this document | The contract test fails and the merge is blocked | None | AC1, AC2, AC3 |
| X2 | The request carries no step key, no rule result or a member the contract does not declare | The operation refuses with 422 and names the member; no run is started | MSG-GEN-001 | AC1 |
| X3 | The contract declares an orchestrator method, a Java call or another service's table as its own | The review refuses the document: the seam is one REST hop to rwb-agent and nothing else | None | AC6 |
| X4 | A payload gains a personal field, or fails its registry subject | The data-steward review and the contract test refuse the payload; a produced message that fails is routed to `.dlt` with an alert | None | AC5 |
| X5 | The record payload drifts from the type of rwb-decision or the library shape | The contract test between this document and RWB-P7-E1027-CON fails and this document is aligned, because P7 owns the type | None | AC5 |
| X6 | A restated operation drifts from the baseline | The contract test fails on the baseline and this document is aligned, because the baseline owns it | None | AC6 |
| X7 | A member type, a page size or a timing is missing from the source material | The member carries the placeholder, one gap row and one assumption row, and the fake is written to the assumed shape | None | AC1, AC5, AC6 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the platform envelopes, the workflow kit, the outbox library, the agent platform contract, the record library and the rwb-case reference-data contract as published |
| Negotiable | Member types beyond the legacy Java types, the error detail text and the fake timings are settled with their owners; the operation set, the idempotency rule, the refusal set, the record payload and the boundary mapping are fixed by this realignment |
| Valuable | Unblocks the app, deployment, calling and integration stories of this key on Day 1 and gives every caller one shape for a step and its record |
| Estimable | Two provided operations, one restated read, one record payload, two consumed boundaries and three fakes |
| Small | Fits one sprint with the contract tests |
| Testable | Every criterion is tested against the artefact - the schema file, the payload, the fake, the document - and never against a business outcome |

##### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client contract slice for rwb-agent

  Background:
    Given the service naming rule and the platform error envelope of the platform library are in force
    Given the agent platform contract of RWB-P10-E1058-CON is in force
    Given the decision-record library of RWB-PLT-E1027-CON and the workflow kit of RWB-PLT-E1071-CON are in force

  Scenario: AC1 The AgentStepClient operation is contracted on the agent base (new, D-RCV-60)
    Given the contract file of this story and a running rwb-agent on the base /api/recovery/agent/v1
    When a calling step submits agent "INTAKE" for case "RW-2026-000201" with step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    Then one operation answers on POST /api/recovery/agent/v1/agent-steps with 200 and an AgentStepOutcome in the member names and types of this document
    Then the request declares agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result} and inputs, and a request that omits the step key or the rule result is refused with 422 and MSG-GEN-001
    Then the refusals are 401 without a session, 403 without the Rules and parameters right with MSG-P4-002, 409 for a step key whose first run is still RUNNING, 422 for a request the service cannot accept and 503 when the store, the workflow or a consumed contract is unavailable
    Then the operation is one hop under the base /api/recovery/agent/v1, and its budget is the policy timeout of 60 seconds as the recorded exception to the 2 s client budget of DP-11
    Then the call type between a calling step and rwb-agent is Not specified in the source documents (GAP-0620; ASM-0904) and RWB-ITG-TE013-ITG proves the real hop across services

  Scenario: AC2 The answer members keep the legacy outcome (new, D-RCV-60)
    Given the answer element declared in this document
    When the outcome of the step of case "RW-2026-000201" is read
    Then it carries decisionLogEntryId, appliedResult, recommendation, fallback, fallbackReason, autonomyMode and agentRunId
    Then in mode SHADOW the appliedResult is rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE", recommendation is null and fallback is false
    Then in mode L1 the appliedResult is the same rule result and recommendation carries the agent answer with confidence 0.91
    Then a run that did not answer inside 60 seconds answers fallback true with reason TIMED_OUT and the run ID
    Then a run whose answer failed a guardrail answers fallback true with the check code, and a run with no approved policy answers fallback true with reason NO_POLICY and no agentRunId
    Then every value is the legacy value of RWB-TE-013 and no member is dropped or renamed without a new version

  Scenario: AC3 The step key is the idempotency key and the repeat answers the first outcome (new, D-RCV-60)
    Given a step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" that ran once
    When the same request arrives again with the same key
    Then the operation answers the first outcome with the same agentRunId and the same decisionLogEntryId, one run row and one record exist for the key, and the repeat is counted as an idempotency hit (R-UNI-40)
    Then the key is declared as the Idempotency-Key of the operation and as the workflow ID of AgentRunWorkflow
    Then a repeat that arrives while the first run is RUNNING is refused with 409 and writes nothing

  Scenario: AC4 The link operation keeps one record per run (new, D-RCV-60)
    Given a run of agent "INTAKE" for case "RW-2026-000201" and the record the step wrote
    When the link operation is called on PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record with the record reference
    Then the answer is 200 with the run and its decision_log_id set to that reference
    Then the same reference answers the same run and writes nothing twice, a different reference is refused with 409, an unknown run answers 404 and a reference the service cannot accept answers 422
    Then the run and the record are joined by reference only, no foreign key crosses a schema and no table of another service is read

  Scenario: AC5 The record payload is declared and carries no personal field (new, D-RCV-60)
    Given a step of case "RW-2026-000201" in mode SHADOW with rule "R-UNI-32" version "2026.11"
    When the record is written through the local library
    Then the payload carries the record reference, the decision code, agent version "INTAKE@P1/PR1", the model version, the inputs reference, the final call "RESUME_STATE" and actions {caseId, agentRunId, mode, fallback, fallbackReason}
    Then it is published as rwb.decision-record.DecisionRecorded.v1 on rwb.decision-record.v1, keyed by the record reference, in the transaction of the calling step, with the retry topic and the .dlt topic of the platform
    Then rwb-decision owns the type and the central ledger, and a payload that fails its registry subject is refused before the relay and routed to .dlt with an alert
    Then no account number, customer name or personal field is declared, and no agent event is declared by this document

  Scenario: AC6 The run read is restated and the three fakes are complete (new, D-RCV-60)
    Given the contract section of this story
    When the nine sub-tables and the three fakes are reviewed
    Then each of 12.1 to 12.9 is present, names its owner from the Ownership Map and writes None where it is empty
    Then GET /api/recovery/agent/v1/admin/agent-runs with query agent, from and to answering AgentRun[] is restated from RWB-P10-E1058-CON and is declared as the baseline's, not this story's
    Then the fakes of the decision-record library and its read, of the rwb-case reference lists and of the gateway-bff route answer every consumed path and payload of this document
    Then the route in front of the run read is a pass-through of one hop and its path is Not specified in the source documents (GAP-0620; ASM-0911)
    Then a drift between a fake and this document fails the contract test, and every fixture is synthetic
```

**Target reading.** The agent "INTAKE", the policy "P1", the prompt "PR1", the case "RW-2026-000201", the rule "R-UNI-32" version "2026.11", the next state "RESUME_STATE", the timeout 60 seconds, the confidence 0.91, the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the reasons TIMED_OUT, SCHEMA and NO_POLICY and the agent version string "INTAKE@P1/PR1" are the legacy values of RWB-TE-013, copied into the contract as the fixture values of its tests; the member names of the request and the answer are the legacy `AgentStepRequest` and `AgentStepOutcome` members, renamed only into the JSON spelling this document fixes and never dropped. The six criteria are new (D-RCV-60) and test the artefact alone: the operation, its members, its refusals, its idempotency, the link, the record payload and the fakes. No criterion asserts a business outcome, which is the app story's.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The step operation is one operation under `/api/recovery/agent/v1` and is the only way a calling step reaches an agent; no caller reads `agent_run`, `agent_policy` or a record table | DP-11; DP-13; DP-20; legacy section 12 |
| BR2 | The request and the answer keep the legacy members - agentCode, caseId, decisionCode, stepKey, ruleResult, inputs; decisionLogEntryId, appliedResult, recommendation, fallback, fallbackReason, autonomyMode, agentRunId - and no member is dropped or renamed without a new version | Legacy section 12; TSD P10 Agent runtime v2 T-A.1 |
| BR3 | The step key is the idempotency key of the operation and the workflow ID of AgentRunWorkflow; a repeat answers the first outcome and writes nothing twice | R-UNI-40; legacy BR5 |
| BR4 | The budget of the step operation is the policy timeout of 60 seconds, the single recorded exception to the 2 s client budget of DP-11, and every other hop keeps 2 seconds | DP-11; NFR-010; ADR-020; ASM-0903 |
| BR5 | The answer carries the applied result, always the rule result in SHADOW and L1, and the recommendation only in L1 | Legacy BR1; `agent_policy.autonomy_mode` (DF-AGT-008) |
| BR6 | A run holds one record reference; the same reference answers the same run, a different reference is refused with 409 and the join is by reference only | R-UNI-40; DF-AGT-058; ASM-0910 |
| BR7 | The record of a step is written by that step through the local library in its own schema and transaction, and rwb-decision owns the type, the ledger and the record read | DP-03; ADR-022; RWB-P10-E1058-CON BR8 |
| BR8 | No business value in the contract: the modes, the timeout, the agent codes, the check codes and the reason codes stay rows of the policy, the reference data and the library, and the contract only names them | Template and Rules §R7.2 s17; DP-07 |
| BR9 | Every message is a CloudEvents 1.0 message on the owner's topic, keyed by the record reference, validated against its registry subject before the relay and routed to `.dlt` on failure | DP-09; DP-14; Arch v5 slide 42 |
| BR10 | One base per service: this contract declares `/api/recovery/agent/v1` and never another service's base or topic, and it restates the run read of the baseline without owning it | DP-13; Arch v5 slide 41; RWB-P10-E1058-CON |
| BR11 | The refusal set is the platform one: 401, 403, 409, 422 and 503, each with the platform problem response and the message ID where a business message applies | Platform error envelope; legacy X4, X5; ASM-0909 |

##### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Draft | Review opened | The two operations, the members, the idempotency, the record payload, the restated read and the fakes are described | In review |
| In review | Consumer sign-off | The app, deployment, calling and integration stories accept the document and the fakes | Baselined |
| Baselined | Additive change | A member, a refusal detail or a payload field is added without removing one | Baselined |
| Baselined | Breaking change | A request or answer member is removed, renamed or retyped, or the idempotency rule changes | In review, with the owner of the affected caller |
| Baselined | Drift in a fake or against the baseline | A contract test fails | In review |
| Baselined | The baseline publishes a new run-read shape, or the record type changes | RWB-P10-E1058-CON or RWB-P7-E1027-CON publishes a new version | Baselined, aligned to the owner |

These are the states of this document, not of a step, a run or a case. The step and run states - ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, NO_POLICY and the link - belong to RWB-P10-TE013-APP.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of rwb-agent | Owns the operations, the members, the idempotency rule, the record payload mapping, the document and the fakes; tags the baseline |
| Solution architect | Approves a breaking change to an operation, a member or the payload, and any change to the budget exception |
| The rwb-decision owner | Owns the record type, the central ledger, the record read and the `rwb.decision-record.v1` topic, and signs off the payload taken from the library |
| The rwb-case owner | Owns the reference lists named in the contract and signs off the list codes taken from its document |
| The app and deployment stories of this key | Review and accept the parts they consume |
| The calling stories of wave 1 | Compile against `recovery.agent.api` and its fake, and accept the request and answer shapes |
| Platform library owner | Owns the error envelope, the naming rule, the outbox library, the record library, the workflow kit and the Drools kit this document reuses |
| Data steward | Confirms that no personal data field is declared in the record payload or in the answer |

The calling identity is a calling service identity and the answering one is the rwb-agent service identity (DP-02); the rwb-agent login is Not specified in the source documents (GAP-0620; ASM-0913) and is fixed with the deployment story.

##### 11. Data

The contract declares shapes, not business values.

| Item | Content |
|---|---|
| Step request | agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result}, inputs (masked) |
| Step answer | decisionLogEntryId, appliedResult {ruleId, ruleVersion, toState, result}, recommendation, fallback, fallbackReason, autonomyMode, agentRunId |
| Link request and answer | record reference in the body; the AgentRun with decision_log_id set |
| Refusal | the platform problem response: status, code, detail, the member name or the message ID when a business message applies |
| Record payload | record reference, decision code, agent version, model version, inputs reference, final call, actions {caseId, agentRunId, mode, fallback, fallbackReason} |
| Restated run read | AgentRun[] as published by RWB-P10-E1058-CON; the members this key reads are the run ID, the agent, the agent version, the case, the status, fallback, latency and the run time |
| Idempotency | the step key as `Idempotency-Key` and as the workflow ID; the record reference as the idempotency of the link |
| Named values | LOV-AUTONOMY (OFF, SHADOW, L1), LOV-AGENT and LOV-PRODUCT through the reference-data contract; the timeout as a policy value; the check codes and reason codes as library and policy values |

The member types beyond the legacy Java types (the JSON shape of `ruleResult.result`, the map of `inputs`, the decimal scale of `confidence` and of the cost fields) and the exact detail text of each refusal are Not specified in the source documents (GAP-0620; ASM-0908); this document fixes the member names and leaves the types to the review with their owners. No table of any schema is declared as an answer source: the operations answer from `rwb_agent`, and the record is written by the caller's library into the caller's schema (DP-01, DP-03).

##### 12. Contract

###### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Rights |
|---|---|---|---|
| POST | `/agent-steps` | Run one case step through the agent and answer the legacy AgentStepOutcome; request agentCode, caseId, decisionCode, stepKey, ruleResult, inputs; 200 the outcome; idempotent on the step key | Rules and parameters C, service identity, scope applied; errors 401, 403, 409, 422, 503 |
| PUT | `/agent-runs/{runId}/decision-record` | Link one run to the decision record the calling step wrote; body the record reference; 200 the AgentRun with decision_log_id set | Rules and parameters C, service identity, scope applied; errors 401, 403, 404, 409, 422, 503 |

The run read `GET /api/recovery/agent/v1/admin/agent-runs` (API-P10-001) is provided by rwb-agent and baselined in RWB-P10-E1058-CON; that document owns its full shape and this contract restates only the members this key reads. No other operation is declared here, and no orchestration method, Java interface or table read is offered as an answer source (BR1, BR10).

###### 12.2 REST operations consumed

| Method | Path | Owner | Use in this contract |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT, checked before a mode is applied or a run row is written (DP-07) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The read-back of the record the step wrote, before the link is stored (DP-03) |

Every operation is one hop with a 2 s client budget (DP-11, ADR-020); the step operation's own budget is the policy timeout of 60 seconds (BR4). The record write is not a consumed REST operation: it is the local library of DP-03 and the topic of 12.3.

###### 12.3 Events published

| Event | Topic | Owner of the type | Key | Payload (IDs and facts only) |
|---|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` with the retry topic and the `.dlt` topic of the platform | P7 rwb-decision owns the type and the ledger; the record is written by the step through the local library | the record reference | record reference, decision code, agent version, model version, inputs reference, final call, actions {caseId, agentRunId, mode, fallback, fallbackReason} |

The event is inserted in the outbox in the same transaction as the record, by the local library, and relayed by the outbox library; the payload is validated against its registry subject before the relay (DP-09; BR9). This document declares no agent event: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` belongs to the run path of RWB-P10-E1058-APP and is unchanged here.

###### 12.4 Events consumed

None. The step operation is a request and the link operation is a write; the service subscribes to no topic for this key. The consumers of EV-08 are rwb-decision and rwb-reporting, and the EV-28 consumers are rwb-decision, rwb-document and rwb-deviation (Arch v5 slides 42 and 43); all are other owners' projections.

###### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of the baseline of RWB-P10-E1058-APP, one execution per step key with the key as workflow ID | `rwb-agent` | Input: the resolved policy and prompt, the case, the step key and the masked inputs. Output: the run row and its outcome, or the expiry that hands the rule result back |
| ResolveAutonomyMode | Activity | `rwb-agent` | Output: OFF, SHADOW, L1 or none, with the policy row in force |
| ApplyAutonomyMode | Activity | `rwb-agent` | Output: the outcome element of 12.1 |
| LinkDecisionRecord | Activity | `rwb-agent` | Output: `decision_log_id` set once, on the run and the record reference |

The workflow identity, queue and namespace are the platform rule of §R4; the three activity names are this story's and are accepted by RWB-P10-TE013-APP, and the six baseline activities of AgentRunWorkflow are RWB-P10-E1058-CON's and are not redefined.

###### 12.6 Schedules

None. This key starts no Schedule: a step is started by its caller, and the legacy dependence on the Quartz entry of RWB-TE-007 is retired under §R6 and points to the workflow kit of RWB-PLT-E1071-CON (DP-10). The contract declares no job table, job admin read or cron expression.

###### 12.7 Tables owned

| Table | Owner | Contracted use |
|---|---|---|
| agent_policy | P10 (`rwb_agent`) | The approved policy in force: mode, timeout, fallback rule, agent and prompt versions; no column added here |
| agent_run | P10 (`rwb_agent`) | The run of a step key, its status, fallback, output, confidence and `decision_log_id`; no column added here |
| agent_prompt | P10 (`rwb_agent`) | The prompt version the policy names; no column added here |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The idempotency envelope of the step key and the link (DP-09) |

No table of another service is declared and no foreign key crosses a schema (DP-01). `decision_log_entry` is P7's type and is written by the calling step in the calling service's schema through the library; `reference_version` and `reference_row` are P3's and are reached through its contract (DP-03, DP-07).

###### 12.8 Contract fakes

| Fake | Documented answer | Used by |
|---|---|---|
| Decision-record library and record-read fake (RWB-PLT-E1027-CON, RWB-P7-E1027-CON) | A written record with its reference; a record with fallback true and a reason; a record with agent version null; a 503 on write; the first record of a step key; a read-back by reference and a reference that is not found | Contract tests, app story, integration copy |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | LOV-AUTONOMY with OFF, SHADOW and L1; LOV-AGENT with INTAKE; LOV-PRODUCT; a list that is not in force; a delay beyond 2 s | Contract tests, app story |
| gateway-bff route stub (RWB-PLT-N001-CON) | A pass-through route in front of the run read, one hop, JSON media type preserved, the refusal passed through unchanged | Contract tests, app story, deployment story |

The outbox stub, the workflow kit stub, the Drools kit stub and the model stub of the baseline are the platform's and RWB-P10-E1058-APP's; they are used but not declared here. Every fixture is synthetic and holds no personal data.

###### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 restated and read by the tests, 2 consumed | The step and link operations provided; the run read restated from the baseline; the P3 lists and the P7 record read consumed, one hop and 2 s each |
| Kafka | 1 declared, 0 consumed | EV-08 on `rwb.decision-record.v1` with the retry and `.dlt` topics, written by the local library in the caller's transaction; EV-28 stays with the baseline and is not re-declared |
| Temporal | 1 workflow of the baseline, 3 activities of this story, 0 Schedules | AgentRunWorkflow on queue `rwb-agent` with ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord |
| File | None | No file is read or written and no extract exists |

##### 13. Solution plan

**Deliverables.** `contract/agent-step-client.yaml` (the two operations, their members, their rights, their refusals and their idempotency), `contract/agent-step-outcome.md` (request and answer members with the legacy names and the fixture values), `contract/agent-decision-record.asyncapi.yaml` (EV-08 on `rwb.decision-record.v1`, its envelope, key, subject and `.dlt` route), `contract/agent-run-read.md` (the run read restated), `contract/agent-client-boundaries.md` (the lists and the record read with their budgets) and the three WireMock mappings with their fixtures.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON for the app story; C RWB-P7-E1027-CON; the payload and the topic are declared here |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON for the app story; the rule result arrives in the request |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON for the app story; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON for the app story |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON for the app story |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | H RWB-P10-TE013-CON for the app story; none here |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON for the app story |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON for the app story |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON as the legacy dependency of the pattern; this document is that contract |

This story is Day 1 and holds no build dependency of its own (§R5.7): the platform contracts it names are those its consumers add, and the C rows of the key are the published contracts of rwb-case and rwb-decision. DP-20 is the pattern this document realises, so the dependency it carries is the row the app story builds against (BR1).

**Build steps**

1. Write the step operation contract: the method, the path under the base, the five request members and the seven answer members with their types, the idempotency on the step key and the refusal set.
2. Write the answer document with the legacy fixture values of AC2 and the rule that a member is removed only with a new version.
3. Write the link operation with its body, its answers 200, 404, 409 and 422 and its idempotency on the record reference.
4. Write the EV-08 AsyncAPI document: envelope, key, payload members, registry subject and `.dlt` route, with the statement that rwb-decision owns the type and the ledger.
5. Restate the run read against the baseline and declare the route in front of it.
6. Write the boundary document for the lists and the record read, with one hop and the 2 s budget, and the budget exception of the step operation.
7. Build the three WireMock mappings and their synthetic fixtures, including the 503 of the record write and the silent list read.
8. Add the contract tests of section 16, including the drift test between each fake and this document and the drift test against the baseline.
9. Tag the baseline and collect the sign-off of the app, deployment and calling stories.

**Done when.** The five contract files validate in the pipeline, the six contract tests pass, the three fakes answer every consumed path and payload, the record payload carries no personal field, and the app and deployment stories of this key have accepted the baseline.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A caller without the right calls the step operation or the link | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required request member is empty | Enter {field}. |

MSG-P7-003 and MSG-P4-002 are the legacy messages of RWB-TE-013 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field. This contract adds no message of its own.

##### 15. Screens and states

None in this story. The contract serves no screen: a fallback shows on the decision record of the case, which a Decision log R holder reads through the P7 read, and on the run read of the baseline, reached through the gateway-bff route (DP-19). The agent monitor screen SCR-46 belongs to RWB-E2-031 and the autonomy-level screen to Epic 3; the contract fixes no screen field, order or masking rule. The exact path of the route in front of the run read is Not specified in the source documents (GAP-0620; ASM-0911).

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-TE013-CON-01 | AC1, BR1, BR2, BR11 | Contract | The step operation validated against its schema: the five request members, a request with no step key refused with 422 and MSG-GEN-001, and the refusal codes 401, 403, 409, 422 and 503 |
| TC-P10-TE013-CON-02 | AC2, BR2, BR5 | Contract | The answer for case "RW-2026-000201": SHADOW with rule "R-UNI-32" version "2026.11" and recommendation null; L1 with confidence 0.91; TIMED_OUT after 60 seconds; a failed check code; NO_POLICY with no run ID |
| TC-P10-TE013-CON-03 | AC3, BR3 | Contract | Step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" twice: one run, one record and the first outcome; a repeat while RUNNING refused with 409 |
| TC-P10-TE013-CON-04 | AC4, BR6 | Contract | The link operation: 200 with the record reference, the same reference again, a different reference refused with 409, an unknown run 404 and an unacceptable reference 422 |
| TC-P10-TE013-CON-05 | AC5, BR7, BR9 | Contract | The record of a SHADOW step: agent version "INTAKE@P1/PR1", final call "RESUME_STATE", the actions, a registry refusal and the `.dlt` route |
| TC-P10-TE013-CON-06 | AC6, BR10 | Contract | The nine sub-tables with None where empty, the run read aligned to the baseline, and the three fakes answering every consumed path and payload |

The six test cases are new (D-RCV-60) and test the artefact, not the business behaviour: the legacy ten test cases stay with RWB-P10-TE013-APP, and the `-ITG` copies with RWB-ITG-TE013-ITG.

##### 17. Guardrails

- No business value in the contract: the modes, the timeout, the agent codes, the check codes and the reason codes stay rows of the policy, the reference data and the library, and the contract only names them (BR8).
- No personal data in an event, an answer, an example or a fake: identifiers and facts only, the inputs are a masked reference and every fixture is synthetic (BR9).
- The contract names the agent base as rwb-agent's and consumes every other operation; a document that declares another service's base or topic as provided fails the review (BR10).
- The record is declared as the calling step's write through the local library, never as an agent run's write (BR7).
- The record type and the ledger stay with rwb-decision; a drift between this document and RWB-P7-E1027-CON is corrected against the owner.
- The run read is restated, never redefined: the baseline RWB-P10-E1058-CON owns it.
- Every payload is validated against its registry subject before the relay, and a refusal is routed to `.dlt` and alerted (DP-09).
- The contract never names the legacy job table, its admin read or its rerun operation (DP-10).

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | The record payload of 12.3 and the answer member decisionLogEntryId | TC-P10-TE013-CON-02, TC-P10-TE013-CON-05 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | The 503 of the record write and the refusal set of the step operation | TC-P10-TE013-CON-01, TC-P10-TE013-CON-05 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | The service identity and the Rules and parameters right of both operations | TC-P10-TE013-CON-01 |
| D-RCV-60 DP-01 | The run and the policy live in `rwb_agent` and every other service's data is read through its contract | The tables of 12.7 and the consumed reads of 12.2 | TC-P10-TE013-CON-04, TC-P10-TE013-CON-06 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | EV-08, its payload and the record read | TC-P10-TE013-CON-05 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The EV-08 AsyncAPI document, its subject and its `.dlt` route | TC-P10-TE013-CON-05 |
| D-RCV-60 DP-10 | Temporal replaces Quartz | The workflow and activity contract of 12.5 and the absent Schedule of 12.6 | TC-P10-TE013-CON-06 |
| D-RCV-60 DP-11 | Contract-first REST, one hop, 2 s timeout | The two provided operations, the consumed reads and the 60 s budget exception | TC-P10-TE013-CON-01, TC-P10-TE013-CON-06 |
| D-RCV-60 DP-13 | One REST base per service | The base `/api/recovery/agent/v1` and the restated run read | TC-P10-TE013-CON-01, TC-P10-TE013-CON-06 |
| D-RCV-60 DP-20 | Agent client through the rwb-agent contract | The step operation, the link and the legacy member names | TC-P10-TE013-CON-02, TC-P10-TE013-CON-03 |
| ADR-020 | Contract-first REST, one hop, 2 s timeout | The operation shapes, the refusals and the fakes | TC-P10-TE013-CON-01, TC-P10-TE013-CON-06 |
| RWB-TE-013 (legacy story) | Agent runtime client with fallback | The members, the step key and the record mapping taken from legacy section 12 | The legacy test cases stay with RWB-P10-TE013-APP |

The gap GAP-0620 records what the sources leave open for this document - the member types, the refusal detail, the record reference and the route path - and each default it raises is settled by ASM-0908 to ASM-0911.

##### 19. Out of scope

- The implementation of the mode resolution, the timed run, the fallback, the record write and the link (RWB-P10-TE013-APP).
- The chart, the migration job, the worker, the wiring, the probes, the alerts, the route publication and the runbook (RWB-P10-TE013-OPS).
- The whole agent platform contract, the eleven operations, the eight tables and the full shape of the run read (RWB-P10-E1058-CON).
- The record library, its envelope and the topic (RWB-PLT-E1027-CON); the record type, the ledger and the record read (RWB-P7-E1027-CON).
- The embedded Drools kit and the rule-package client (RWB-PLT-E1072-CON), and the rule registry and its packages (P7 rwb-decision).
- The reference lists and their versions (P3 rwb-case).
- The agent monitor screen SCR-46 and its dashboard (RWB-E2-031), and the autonomy-level screen (Epic 3).
- The end-to-end proof across services, including the real call type between a calling step and rwb-agent (RWB-ITG-TE013-ITG).
- The case steps that call the client (RWB-E2-028, RWB-E2-029 and the other calling stories).


### RWB-P10-TE013-APP Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-TE013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P10-A |
| Ready to start | After RWB-P10-E1058-APP |
| Depends on (build) | RWB-P10-TE013-CON, RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON, RWB-PLT-N001-CON, RWB-P10-E1058-APP |
| Contract dependencies | RWB-P3-E1043-CON, RWB-P7-E1027-CON |
| Integration dependencies | None |
| External dependencies | RWB-P10-TE013-OPS |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-018, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: app slice of RWB-TE-013 for rwb-agent. In the monolith the key is one published Java interface in `recovery.agent.api`, an `AgentOrchestrator.run` call in the same JVM, a P7 `DecisionLogWriter` of the same deployment and a Quartz job step (RWB-TE-007) that brought it into a case step. The target turns each of those into a boundary: the client becomes the rwb-agent contract reached through the `recovery.agent.api` library (**DP-20**), the orchestrator becomes AgentRunWorkflow on queue `rwb-agent` (**DP-10**), the entry becomes the local decision-record library plus the topic `rwb.decision-record.v1` (**DP-03**, **DP-09**), the shared `RuleEvaluator` becomes the embedded Drools kit with packages from rwb-decision (**DP-04**), and the step and link operations are served on `/api/recovery/agent/v1` (**DP-13**) with rows in `rwb_agent` only (**DP-01**), lists from the rwb-case reference-data contract (**DP-07**), the run read behind the gateway-bff route (**DP-19**) and the one migration in the service's own Flyway sequence (**DP-15**). Every legacy value, ID, message ID, timeout, threshold and test case ID is kept. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one agent runtime client in rwb-agent - the `AgentStepClient` operation on `/api/recovery/agent/v1/agent-steps` plus the `recovery.agent.api` library that every calling step uses - that applies the autonomy mode of the approved policy in force, runs shadow mode, falls back to the rule result with reason TIMED_OUT, SCHEMA or NO_POLICY inside the 60 second budget, records the decision through the local decision-record library before the step acts, and links the run to that record**, so that **agents are added to a case step without changing the case flow, every step records what the agent did and why the rule result was applied, and no step acts on an answer whose decision could not be recorded**.

##### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The legacy client put every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001). If the entry cannot be written, the step does not act (REQ-DRI-005). The measure is the agent fallback rate, target below 10 percent per month.

In the target every element of that interface is a boundary:

- The orchestrator is rwb-agent's `AgentRunWorkflow` on its own task queue, with the approved policy's 60 second budget inside it (Arch v5 slide 16, "AgentRunWorkflow: 60 s, then rule result"; DP-20).
- The interface a caller compiles against is still `recovery.agent.api`, but it is a library over a REST contract with a fake, one hop, on the owner's base (DP-11, DP-13).
- The record is no longer one service's writer: the step writes its own record in its own schema through the shared library, and rwb-decision owns the type and collects the central ledger (DP-03).
- The rule result is not taken from a shared bean: the calling step evaluates its package through the embedded Drools kit with the packages published from rwb-decision (DP-04).
- The Quartz job step is retired with RWB-TE-007 and becomes a Temporal step of the calling service through the workflow kit (DP-10).

What does not change is the order the legacy story fixes: rule first, agent second, record before action. The seven legacy exception paths keep their triggers, reasons and messages, the eight legacy criteria are kept word for word with their origin tags, and the legacy test cases keep their IDs and data. The cross-service behaviour of this key is proved by RWB-ITG-TE013-ITG, which is why this story carries no integration dependency (I = None).

##### 3. Preconditions

- RWB-P10-E1058-APP is done: the eight agent tables exist in `rwb_agent`, AgentRunWorkflow is registered on queue `rwb-agent` with its activities, and `agent_run` holds DF-AGT-045 idempotency_key and DF-AGT-058 decision_log_id.
- RWB-P10-TE013-CON is published: the step operation, the link operation, their members, the idempotency rules, the refusal codes and the three fakes.
- RWB-PLT-E1027-CON is published (decision-record library, its outbox write in the caller's transaction and `rwb.decision-record.v1`; DP-03); RWB-PLT-E1072-CON (embedded Drools kit and rule-package client; DP-04); RWB-PLT-E1043-CON (reference-data client library; DP-07); RWB-PLT-TE006-CON (outbox and inbox library, relay and `.dlt` rule; DP-09); RWB-PLT-E1071-CON (workflow kit, namespace `rwb-recovery`; DP-10); RWB-PLT-E1044-CON (per-service Flyway sequence; DP-15); RWB-PLT-N001-CON (gateway-bff route contract and stub; DP-19).
- The `rwb_agent` baseline applies `V10_001__agent_runtime.sql`; this story's `V10_002__agent_run_decision_link.sql` applies after it in the rwb-agent sequence.
- RWB-P3-E1043-CON is published: `GET /api/recovery/case/v1/admin/lists/{listCode}` answers LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT with the version in force (DP-07). RWB-P7-E1027-CON is published: the record read by its reference and the record type and central ledger are P7's (DP-03).
- An approved `agent_policy` row exists for the agent and the business date, with autonomy_mode SHADOW, L1 or OFF, timeout_seconds 60 (legacy value; DL11) and prompt_version PR1; the mode, the timeout and the prompt version are rows of the policy and never code.
- The calling service runs under its own service identity and has evaluated its rule through the embedded Drools kit before it calls the client; rwb-agent runs under the rwb-agent login (DP-02), whose name is Not specified in the source documents (GAP-0619; ASM-0906).
- The step operation `POST /api/recovery/agent/v1/agent-steps` and the link operation `PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record` are this story's names for the two boundaries the legacy Java interface spans; no source names a run-submit operation among the eleven P10 operations (GAP-0619; ASM-0902), and the call type between a calling step and rwb-agent is Not specified in the source documents (GAP-0619; ASM-0904).
- The release date 30 November 2026 is tentative and is copied unchanged.

##### 4. Flow

1. The calling step evaluates its rule package through the embedded Drools kit with the package published from rwb-decision and builds the rule result: rule ID "R-UNI-32", rule version "2026.11" and the next state (DP-04; legacy step 1).
2. The calling step calls `AgentStepClient.runStep` with the agent code, case ID, decision code, step key and rule result; the library submits to `POST /api/recovery/agent/v1/agent-steps` with the step key as the `Idempotency-Key` and the masked inputs, one hop (DP-11, DP-20; legacy step 2).
3. rwb-agent reads the autonomy mode and the timeout of the approved policy in force from `agent_policy` in `rwb_agent`; when the mode is OFF, or the flag `rwb.agent.client` is off, it skips the agent: no AgentRunWorkflow and no run row (AC8; legacy step 3).
4. Otherwise it starts AgentRunWorkflow on queue `rwb-agent` with the step key as the workflow ID and as the run's idempotency key, and waits at most `agent_policy.timeout_seconds`: 60 seconds (AC1, AC2; DP-10; legacy step 4).
5. SHADOW: it keeps the rule result as the applied result, stores the agent answer on the run and answers recommendation null (AC1; legacy step 5).
6. L1: it keeps the rule result as the applied result and answers the checked agent answer as the recommendation for the person who decides, with its confidence, 0.91 in the fixture (AC3; legacy step 6).
7. On a timeout or a guardrail failure it keeps the rule result and marks fallback true with the reason, TIMED_OUT or the check code SCHEMA (R-UNI-32; AC2, AC4; legacy step 7).
8. The client writes one decision record through the local decision-record library, in the calling service's schema and transaction, with the rule ID and version, the agent version, the model version, the recommendation and the fallback; the library publishes EV-08 on `rwb.decision-record.v1` (DP-03, DP-09; legacy step 8).
9. The client then links the run to the record with `PUT /api/recovery/agent/v1/agent-runs/{runId}/decision-record`; rwb-agent sets `agent_run.decision_log_id` (DF-AGT-058) once: the same record answers the same run, a different record is refused with 409 (AC1, AC7; legacy step 8).
10. The calling step acts on the applied result only after the record and the link exist; if the record cannot be written it does not act, case "RW-2026-000201" stays in "NEW", the client raises `DecisionNotRecordedException` carrying MSG-P7-003, an incident is raised (R-UNI-39) and the run keeps `decision_log_id` empty (AC6; legacy step 9).
11. The same step key presented again returns the first outcome: one run row, one record and one link for the key, counted as an idempotency hit (R-UNI-40; AC7).
12. The run read `GET /api/recovery/agent/v1/admin/agent-runs` is the baseline of RWB-P10-E1058-CON and is not re-declared here; a reader reaches it through the gateway-bff route (DP-19; AC2, AC7).

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent does not answer within 60 seconds | Rule result applied; fallback true with reason TIMED_OUT; step continues | None to a user | AC2 |
| X2 | The answer fails a guardrail check | Rule result applied; fallback true with the check code | None to a user | AC4 |
| X3 | No approved policy exists for the agent on the business date | No agent call; rule result applied; fallback true with reason NO_POLICY | None to a user | AC5 |
| X4 | The decision record write fails | The step does not act; the case stays in its state; an incident is raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same step key arrives twice | One agent run, one record and one link; the repeat returns the first outcome (R-UNI-40) | None to a user | AC7 |
| X6 | Autonomy mode OFF or flag `rwb.agent.client` off | No agent call; rule result applied; fallback false; no agent run row | None to a user | AC8 |
| X7 | A role without the right reads agent runs | Refused with 403 | MSG-P4-002 | TC-TE-013-09 |
| X8 | The step operation is called with no step key or no rule result | Refused with 422 and no run is started; proved by RWB-P10-TE013-CON | MSG-GEN-001 | TC-P10-TE013-CON-01 |
| X9 | The same step key is presented while its first run is RUNNING | Refused with 409 while the run is RUNNING; answers the first outcome once the run and the record exist (R-UNI-40) | None to a user | AC7 |
| X10 | The reference-data contract does not answer inside 2 s | No mode is applied and no run is started with a guessed mode; 503 | None to a user | AC1 |
| X11 | The link is refused because the run holds a different record | The first record stands; the link is not overwritten; the mismatch is raised to the data steward | None to a user | AC7 |
| X12 | The migration `V10_002__agent_run_decision_link.sql` fails | The new version does not start; the version in force keeps serving; no run is linked | None | AC1 |

X1 to X7 are the legacy exception paths with the same triggers and messages. X8 to X12 appear when the interface becomes a contract, when the record leaves the service and when the migration owns the link column. X7 is not reached by a criterion of this story: it is proved by TC-TE-013-09 at Contract level.

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds on the platform contract stories, the published P3 and P7 contracts with their fakes and the in-lane story RWB-P10-E1058-APP; owns its two operations and its one migration |
| Negotiable | Package layout, component and activity names, member order and internal timeouts are design; the agent, policy and prompt versions, the rule and version, the case, the step key, the timeout 60, the modes, the confidence 0.91, the 2,000 ms answer, the three reasons and the two message IDs are fixed by the legacy story |
| Valuable | Every agent from RWB-E1-059 onward plugs into case steps through this one boundary, with a record written before the step acts |
| Estimable | Two operations, one client library, three activities, one migration, seven components, two contract clients and three fakes |
| Small | Under one week with its tests, as in the legacy estimate; the in-process orchestrator is replaced by the workflow start |
| Testable | Each of the eight criteria is one automated test on an observable: a stored run, a record reference, a link column, an answered outcome, a refusal or a raised exception |

##### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback

  Background:
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"

  Scenario: AC1 Shadow (legacy RWB-TE-013 AC1)
    Given the rwb-decision decision-record contract mock returns a written entry id
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the agent answers in 2,000 ms with a valid output
    Then the system stores the agent answer on the agent run and the rule result is the applied result
    Then one decision log entry holds agent version "INTAKE@P1/PR1", the rule ID and version, recommendation null and fallback false in actions
    Then the calling step receives the rule result and no agent output

  Scenario: AC2 No answer (legacy RWB-TE-013 AC2)
    Given the rwb-decision decision-record contract mock returns a written entry id with fallback true and reason "TIMED_OUT"
    Given the agent does not answer in 60 seconds
    When the step runs
    Then the system uses the rule result and the step continues to "RESUME_STATE"
    Then the decision log entry holds actions fallback true with reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC3 Assisted mode returns the answer as a recommendation (legacy RWB-TE-013 AC3)
    Given the rwb-decision decision-record contract mock returns a written entry id carrying the recommendation
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers with confidence 0.91
    Then the rule result is the applied result
    Then the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision log entry holds the agent answer in recommendation with confidence 0.91

  Scenario: AC4 A guardrail failure falls back (legacy RWB-TE-013 AC4)
    Given the rwb-decision decision-record contract mock returns a written entry id with fallback true and reason "SCHEMA"
    Given the agent answer fails check "SCHEMA"
    When the step runs
    Then the system applies the rule result
    Then the decision log entry holds actions fallback true with reason "SCHEMA"

  Scenario: AC5 No approved policy (legacy RWB-TE-013 AC5)
    Given the rwb-decision decision-record contract mock returns a written entry id with fallback true and reason "NO_POLICY"
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the system makes no orchestrator call
    Then the system applies the rule result with fallback true and reason "NO_POLICY" in the decision log entry

  Scenario: AC6 The decision log write fails (legacy RWB-TE-013 AC6)
    Given the rwb-decision decision-record contract mock returns 503 for the entry of the step
    Given the decision log writer throws on write
    When the step runs
    Then the calling step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then the agent run stays with decision_log_id empty

  Scenario: AC7 A repeated step key (legacy RWB-TE-013 AC7)
    Given the rwb-decision decision-record contract mock returns the first entry for the step key
    Given the step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" ran once
    When it runs again with the same key
    Then one agent run and one decision log entry exist for the key
    Then the second call returns the first outcome (R-UNI-40)

  Scenario: AC8 Agent switched off (legacy RWB-TE-013 AC8)
    Given the rwb-decision decision-record contract mock returns a written entry id with agent version null
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then no orchestrator call and no agent run row are made
    Then the decision log entry holds agent version null and fallback false
```

**Target reading.** The agent "INTAKE", the policy "P1", the prompt "PR1", the case "RW-2026-000201", the route state "NEW" and status "New", the rule "R-UNI-32" version "2026.11" and next state "RESUME_STATE", the timeout 60 seconds, the 2,000 ms answer, the confidence 0.91, the check code "SCHEMA", the three reasons, the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the business date 2026-11-30, the agent version string "INTAKE@P1/PR1", the empty `decision_log_id` and the two message IDs are the legacy values of RWB-TE-013, copied character for character; the eight scenario titles and every legacy Given, When and Then are kept, and each scenario carries the origin tag of its legacy criterion.

Each scenario gained exactly one inserted Given, `Given the rwb-decision decision-record contract mock returns <x>`, because every criterion ends on a decision record written across a service boundary: AC1, AC3, AC4, AC5 and AC8 read the record the local library writes, AC2 and AC4 read the fallback reason it carries, AC6 reads the refusal of the record store, and AC7 reads the first record of the step key. Nothing this service owns is mocked: the run, the policy row, the mode, the fallback, the run status and the link column are written and read in `rwb_agent` and asserted on the real store; the rwb-agent contract is never mocked in its own tests. The model endpoint INT-23 is stubbed by the baseline RWB-P10-E1058-APP, so 2,000 ms and 60 seconds of silence are fixture timings, never business values.

One legacy statement names an object the target changes hands over: AC6's "the agent run stays with decision_log_id empty" keeps the column and the assertion, and what changes is who sets it - the link operation instead of an in-process repository call. `DecisionNotRecordedException` keeps its name, its message ID MSG-P7-003 and its R-UNI-39 incident, and is now raised when the local record write in the caller's transaction fails.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule result is computed before the agent is called and is always the applied result in SHADOW and L1 | Agent catalog autonomy levels; `agent_policy.autonomy_mode` (DF-AGT-008); legacy BR1 |
| BR2 | If the agent does not answer within `agent_policy.timeout_seconds` (60, assumed; DL11), the rule result is used and the fallback is recorded on the decision | R-UNI-32; NFR-010; legacy BR2 |
| BR3 | A step acts only after its decision record and its link are written | Principle 5; R-UNI-39; CTL-06; legacy BR3 |
| BR4 | The record holds the rule ID, the rule version, the agent version as "<agent>@<policy>/<prompt>", the model version and the recommendation | REQ-DRI-001; `decision_log_entry.agent_version`; legacy BR4 |
| BR5 | The idempotency key of the agent run is the step key | R-UNI-40; DF-AGT-045; legacy BR5 |
| BR6 | The client runs under the identity of the calling module; the agent runs its tools as the rwb-agent service identity | REQ-ACA-010; legacy BR6 |
| BR7 | An agent is reached only through the step operation and AgentRunWorkflow on queue `rwb-agent`; no calling step reads `agent_run`, `agent_policy` or a record table in another schema | DP-01; DP-11; DP-20; Arch v5 slides 16 and 41 |
| BR8 | The step operation is one hop under `/api/recovery/agent/v1`; its budget is the policy timeout of 60 seconds, the recorded exception to the 2 s client budget of DP-11, and every other consumed hop keeps 2 seconds | DP-11; NFR-010; ADR-020; ASM-0903 |
| BR9 | The record of a step is written by that step through the local library in the calling service's schema and transaction, never by an agent run; rwb-decision owns the type and the central ledger | DP-03; ADR-022; RWB-P10-E1058-CON BR8 |
| BR10 | The mode, the timeout, the prompt version and the fallback rule are rows of the approved policy in force, read at run time; no mode, timeout, agent code or check code appears in code | Principle 1; DF-AGT-008, DF-AGT-012, DF-AGT-020; legacy section 17 |
| BR11 | The link between a run and a record is written once per run; the same record answers the same run and a different record is refused with 409 | R-UNI-40; DF-AGT-058 |
| BR12 | The values a mode, a run status and a product group may take are read from the rwb-case reference-data contract and never from a literal | DP-07; TSD P10 Agent runtime v2 T3.2 |

##### 9. State transitions

The state of a case step that calls the client:

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | AGENT_UNAVAILABLE | The agent or the model does not answer inside the timeout (R-UNI-32) | RESUME_STATE, with the rule result applied |
| ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | The record cannot be written (R-UNI-39) | EXCEPTION_QUEUE, raised by the calling step |

The state of one step key in `rwb_agent`:

| From | Event | Condition | To |
|---|---|---|---|
| None | The step operation arrives | No run holds the step key | RUNNING, one AgentRunWorkflow and one run row |
| None | The step operation arrives | The mode is OFF or the flag is off | No run; the outcome answers fallback false and agent version null |
| None | The step operation arrives | No approved policy for the agent and date | No run, no model call; fallback true with reason NO_POLICY |
| RUNNING | The model answers and the guardrail passes | The answer is inside the timeout | ANSWERED, fallback false, the answer stored on the run |
| RUNNING | The timeout expires | 60 seconds without an answer | TIMED_OUT, fallback true, the rule result applied |
| RUNNING | The guardrail refuses the answer | A check code fails | GUARDRAIL_FAILED, fallback true with the check code |
| ANSWERED | The link stores the record reference | The run holds no record | The run holds `decision_log_id`; the step may act |
| ANSWERED | The link is called again with the same reference | The run holds the same record | The same run is answered; no second write |
| ANSWERED | The link is called with a different reference | The run holds another record | 409; the first record stands and the mismatch is raised |

The client changes no case status itself; the calling step moves the case on the applied result, as in the legacy story.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| The calling service identity (for example the rwb-case service identity) | Calls the step operation and the link operation; writes the decision record through the local library (Decision log C) |
| The rwb-agent service identity (the rwb-agent login, DP-02) | Runs AgentRunWorkflow, reads `agent_policy`, writes `agent_run` and the link, checks the reference lists, reads the record back through P7 |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks through `GET /api/recovery/agent/v1/admin/agent-runs` (Platform administration R), under the baseline of RWB-P10-E1058-CON |
| rwb-decision (P7) | Owns the record type, the central ledger and the record read |
| rwb-case (P3) | Owns the reference lists and answers them through its contract |
| No role | Reads `rwb_case`, `rwb_decision` or another service's schema, edits an `agent_run` row outside the link, or changes a policy row outside RWB-P10-E1058-APP |

The login of the service is Not specified in the source documents (GAP-0619; ASM-0906); the story names it "the rwb-agent login (DP-02)". The approval of a policy version, its mode and its timeout is the Rules and parameters A right of RWB-P10-E1058-APP; no delegation of authority level applies here.

##### 11. Data

| BR Field ID | Entity in rwb_agent | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case (rwb_case, owner P3) | id | Read through the Case record contract and carried in the request |
| DF-CAS-007 | recovery_case (rwb_case, owner P3) | route_state | Read through the Case record contract; never read as a table |
| DF-REF-002, DF-REF-003 | rule_row (rwb_decision, owner P7) | rule_id, rule_version | Read from the rule result passed in the request, evaluated through the embedded Drools kit (DP-04) |
| DF-AGT-008, DF-AGT-012, DF-AGT-020 | agent_policy | autonomy_mode, timeout_seconds, fallback_rule | Read, for the approved policy in force on the business date |
| DF-AGT-021, DF-AGT-022 | agent_policy | status, valid_from | Read, to select the policy in force |
| DF-AGT-002, DF-AGT-003 | agent_policy | agent_code, policy_version | Read, to build the agent version string |
| DF-AGT-036, DF-AGT-045, DF-AGT-046, DF-AGT-047 | agent_run | id, idempotency_key, status, fallback | Read and write, on the run of the step key |
| DF-AGT-049, DF-AGT-050 | agent_run | output, confidence | Write, in SHADOW and L1 |
| DF-AGT-058 | agent_run | decision_log_id | Write, once per run, through the link operation |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry (owner P7, written in the calling service's schema through the library) | all fields | Write through the local decision-record library, in the calling step's transaction (DP-03) |
| DF-REF-159 to DF-REF-184 | reference_version, reference_row (rwb_case, owner P3) | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT with the version in force | Read through the reference-data contract (DP-07) |

Field IDs are those in the Logical Data Model and Data Dictionary, copied from RWB-TE-013. `agent_policy`, `agent_prompt` and `agent_run` are the P10 tables of schema `rwb_agent`. `recovery_case` and `rule_row` are never read as tables: the case is carried in the request and the rule result is passed in, as the legacy client did. The inputs snapshot is masked before it is referenced, and no personal field is stored on the run or in the record.

##### 12. Contract

###### 12.1 REST operations provided

Base `/api/recovery/agent/v1`; owner rwb-agent (P10).

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| POST | `/agent-steps` | Run one case step through the agent: resolve the mode and timeout of the approved policy in force, skip the agent when the mode is OFF or the flag is off, start AgentRunWorkflow with the step key as workflow ID, wait up to `timeout_seconds`, apply SHADOW or L1, record the fallback, answer the legacy AgentStepOutcome. Request: agentCode, caseId, decisionCode, stepKey, ruleResult {ruleId, ruleVersion, toState, result}, inputs. Answer 200: decisionLogEntryId, appliedResult, recommendation, fallback, fallbackReason, autonomyMode, agentRunId | Rules and parameters C, service identity, scope applied | The step key as the `Idempotency-Key`; a repeat answers the first outcome (R-UNI-40) |
| PUT | `/agent-runs/{runId}/decision-record` | Link one run to the record the calling step wrote: body the record reference; 200 the AgentRun with `decision_log_id` set; 404 no run; 409 the run holds a different record; 422 a reference the service cannot accept | Rules and parameters C, service identity, scope applied | The record reference; the same reference answers the same run and writes nothing twice |

Errors: 401 no session or no service identity, 403 no Rules and parameters right (MSG-P4-002), 409 a repeated step key whose first run is RUNNING or a run holding another record, 422 a request the service cannot accept (MSG-GEN-001), 503 the store, the workflow or a consumed contract unavailable. The two operations and the answer member names are fixed by RWB-P10-TE013-CON.

The run read `GET /api/recovery/agent/v1/admin/agent-runs` with query agent, from and to answering AgentRun[] (API-P10-001) is provided under the baseline of RWB-P10-E1058-CON and is not re-declared here; this story reads it only through its tests.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use | Budget |
|---|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT checked before a mode is applied or a run row is written | One hop, 2 s |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The read-back of the record the step wrote, before the link is stored | One hop, 2 s |

Every call is one hop to the owning service on its own base (DP-13) with the 2 s client budget (DP-11); rwb-agent holds no schema client of another service. The model endpoint INT-23 is called inside AgentRunWorkflow by the baseline of RWB-P10-E1058-APP and is not called by this story. The record write is not a REST call: it is the local library and the topic of 12.3 (DP-03).

###### 12.3 Events published

None by rwb-agent through this story. The record of a step is written and published by the calling step through the client library, in the calling service's own schema and transaction, as `rwb.decision-record.DecisionRecorded.v1` (EV-08) on `rwb.decision-record.v1` with the key of the record reference, and rwb-decision owns the type and the ledger (DP-03, DP-09; BR9). The payload members are fixed by RWB-P10-TE013-CON: record reference, decision code, agent version, model version, inputs reference, final call and actions {caseId, agentRunId, mode, fallback, fallbackReason}. This story declares no agent event: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` belongs to the run path of RWB-P10-E1058-APP, as the legacy story says the orchestrator publishes it and the client publishes none.

###### 12.4 Events consumed

None. The step operation is a request; the mode and the timeout are read from `rwb_agent`, and the case and the rule result are carried in the request rather than consumed as events. This story subscribes to no topic.

###### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of the baseline of RWB-P10-E1058-APP, started with the step key as workflow ID and as the run's idempotency key | `rwb-agent` | Its activities ResolveAgentConfig, GatherInputs, MaskInputs, CallModelGateway with the 60 s budget, CheckGuardrail and RecordAgentRun are unchanged; this story starts it and waits on it |
| ResolveAutonomyMode | Activity | `rwb-agent` | Output: the mode OFF, SHADOW or L1 and the policy row in force for the agent and the business date, or none |
| ApplyAutonomyMode | Activity | `rwb-agent` | Output: the AgentStepOutcome - applied result, recommendation null in SHADOW and the answer in L1, fallback, reason and mode |
| LinkDecisionRecord | Activity | `rwb-agent` | Output: `agent_run.decision_log_id` set once for the run and the record reference |

The workflow runs on the queue and in the namespace of the service (§R4). The three activity names are this story's and are accepted by RWB-P10-TE013-CON; the baseline activity names are RWB-P10-E1058-APP's and are not changed.

###### 12.6 Schedules

None. This key starts no Schedule and no job: a step is started by its caller. The legacy precondition "RWB-TE-007 is done: Quartz jobs and their run books exist" is retired under §R6, and a job step that called the client is now an event-started or scheduled workflow step of the calling service through the workflow kit of RWB-PLT-E1071-CON (DP-10). No Quartz entry, job table or job admin read is used.

###### 12.7 Tables owned

| Table | Owner | Note |
|---|---|---|
| agent_policy | P10 (`rwb_agent`) | Read for the approved policy in force: mode, timeout, fallback rule and versions; no column added |
| agent_run | P10 (`rwb_agent`) | Read and written for the run of the step key: status, fallback, output, confidence and `decision_log_id` (DF-AGT-058); no column added by this story |
| agent_prompt | P10 (`rwb_agent`) | Read for the prompt version of the policy; no column added |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | The idempotency envelope of the step key and the link (DP-09) |

No table of another service is read and no foreign key crosses a schema (DP-01). `recovery_case` is P3's, `rule_row` and `decision_log_entry` are P7's, and `reference_version` and `reference_row` are P3's; all are reached through their contracts. DF-AGT-058 is already a field of `agent_run` in TSD P10 Agent runtime v2 T3.1, so `V10_002__agent_run_decision_link.sql` guarantees the column and its index in the rwb-agent sequence and creates no table (DP-15).

###### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| Decision-record library stub of RWB-PLT-E1027-CON | The local record write and the record read-back of P7 | A written record with its reference; a record with fallback true and a reason; a record with agent version null; a 503 on write for AC6; the first record of a step key |
| rwb-case WireMock | The P3 reference-data contract of RWB-P3-E1043-CON | LOV-AUTONOMY with OFF, SHADOW and L1; LOV-AGENT with INTAKE; LOV-PRODUCT; a list not in force; a delay beyond 2 s |
| gateway-bff route stub | The DP-19 route of RWB-PLT-N001-CON | A pass-through route in front of the run read, one hop, JSON media type preserved, refusal passed through unchanged |
| Test clock and model stub of RWB-P10-E1058-APP | The 2,000 ms answer and the 60 seconds of silence of the legacy fixtures | One answer at 2,000 ms with confidence 0.91, one silence past 60 seconds, one answer failing check SCHEMA |

Every fixture is synthetic and holds no personal data. No test calls the model endpoint INT-23 directly: the two legacy timing fixtures are produced by the baseline stub of the run path.

###### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided, 1 provided by the baseline and read by the tests, 2 consumed | The step and link operations provided; the run read of the baseline used by the tests; the P3 lists and the P7 record read consumed, one hop and 2 s each |
| Kafka | None published by the service, 1 published by the calling step through the library | EV-08 on `rwb.decision-record.v1` with its retry and `.dlt` topics; EV-28 belongs to the run path of RWB-P10-E1058-APP |
| Temporal | 1 workflow of the baseline started and waited on, 3 activities of this story, 0 Schedules | AgentRunWorkflow on queue `rwb-agent` with ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord |
| File | None | No file, no extract and no export |

##### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.agent.client`, module `client`, inside rwb-agent; the published library keeps the legacy package `recovery.agent.api` for `AgentStepClient`, `AgentStepRequest`, `RuleResult` and `AgentStepOutcome`, so a calling module compiles against the same names as before.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; the packages and the registry are P7's, and the P7 contract row this key carries is RWB-P7-E1027-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency); the step operation is the recorded 60 s exception |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON as the legacy dependency of the pattern, which is an H row here because it is the service's own contract |

The H rows of this table are the rows in the metadata table; DP-11 adds no dependency of its own and sits on the two consumed reads and the provided operation, whose budget is the policy timeout (BR8; ASM-0903).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentStepClient | Published interface | The only way another module calls an agent; the legacy signature and members, unchanged |
| AgentStepClientImpl | Service | Submits the step, applies the mode and the fallback, writes the record through the library, links the run |
| AgentStepController | Controller | `POST /agent-steps` and `PUT /agent-runs/{runId}/decision-record` on `/api/recovery/agent/v1`, their refusals and idempotency (DP-13) |
| AutonomyModeResolver, ResolveAutonomyMode | Service and activity | Reads the policy in force for the agent and the business date and answers OFF, SHADOW, L1 or none (X3, X6) |
| TimedRunInvoker | Service | Starts AgentRunWorkflow with the step key and waits the policy timeout, producing TIMED_OUT on expiry (AC2; R-UNI-32) |
| ApplyAutonomyMode | Activity | Applies SHADOW and L1 to the outcome (AC1, AC3) |
| GuardrailFallbackHandler | Service | Maps a failed check code to fallback true with that code (AC4) |
| DecisionRecordWriter | Service | Writes the record through the local library in the caller's transaction and raises `DecisionNotRecordedException` with MSG-P7-003 on failure (AC1, AC6) |
| LinkDecisionRecord, AgentRunRepository | Activity and repository | Sets `agent_run.decision_log_id` once and answers 409 for a different record (AC7; BR11) |
| ReferenceDataReader, DecisionLogReadClient | Clients | Read LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT through the reference-data contract and the record back through P7 (DP-07, DP-03) |
| AgentPolicyRepository | Repository | Reads `agent_policy` and `agent_prompt` in `rwb_agent` only (DP-01) |

**Database and migrations.** `V10_002__agent_run_decision_link.sql` guarantees DF-AGT-058 on `agent_run` and its index, in `rwb_agent`, after `V10_001__agent_runtime.sql`, and creates no table (DP-15); `ix_agent_run_idempotency_key ON agent_run (idempotency_key)` serves the repeat lookup (DF-AGT-045). No new table, lake table or extract table is created.

**Configuration and reference data.** The approved `agent_policy` rows for the agents of LOV-AGENT, with autonomy_mode SHADOW, L1 or OFF, timeout_seconds 60, prompt_version PR1 and fallback_rule R-UNI-32, loaded by RW-COE and approved by RW-RISK, read at run time; LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT in force in rwb-case; the legacy flag `rwb.agent.client` kept, whose registration is the deployment's (RWB-P10-TE013-OPS); the guardrail check-code list is Not specified in the source documents (GAP-0619; ASM-0907), so the code stays a value of the guardrail result of RWB-P10-E1058-APP.

**Build steps**

1. The `recovery.agent.api` library with the legacy interface and the four records, and an ArchUnit test that other modules import only that package (DP-20).
2. `V10_002__agent_run_decision_link.sql`, the entity and AgentRunRepository in `rwb_agent` (BR11; DP-15).
3. AutonomyModeResolver with tests for OFF, SHADOW, L1 and no policy, against the reference-data fake (AC5, AC8; DP-07).
4. The timed call with a fake clock: 61 seconds of silence produces TIMED_OUT at 60 seconds and the rule result is applied (AC2; R-UNI-32).
5. DecisionRecordWriter and the write before return, with the 503 of AC6 and `DecisionNotRecordedException` carrying MSG-P7-003 (AC1, AC3, AC6; DP-03).
6. The idempotent repeat on the step key and the guardrail fallback (AC4, AC7; R-UNI-40).
7. AgentStepController with the two operations, their refusals 401, 403, 409, 422 and 503, and their idempotency (AC1, AC7; DP-13).
8. Pipeline scans: no literal of a mode, a timeout, an agent code or a check code, and no read of another service's table (BR7, BR10).
9. gateway-bff route contract test in front of the run read (AC2, AC7; DP-19).

**Done when.** The ten test cases of section 16 pass, the step operation answers on `/api/recovery/agent/v1` for the legacy fixture with the run at 2,000 ms and the record reference, a silence past 60 seconds produces TIMED_OUT with the rule result applied, a failed record write leaves case "RW-2026-000201" in "NEW" with MSG-P7-003 and `decision_log_id` empty, a repeated step key answers the first outcome with one run and one record, the boundary test shows other modules depend only on `recovery.agent.api`, and RWB-P10-TE013-OPS has deployed the capability in SIT.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right reads agent runs | You cannot {action} here. Your role does not include it. |
| MSG-GEN-001 | A required member of the step request is empty | Enter {field}. |

MSG-P7-003 and MSG-P4-002 are copied unchanged from RWB-TE-013 and keep their wording character for character; MSG-GEN-001 is the platform message of an empty required field and this story adds no message ID. Thai text for each message follows decision DL10. In AC6 the message is carried by `DecisionNotRecordedException`; in the access test the {action} value is "read agent runs".

##### 15. Screens and states

No screen in this story. A fallback shows in `GET /api/recovery/agent/v1/admin/agent-runs` (fallback true) and on the decision record of the case, which a Decision log R holder reads through the P7 read, as in the legacy story; the run read is reached through the gateway-bff route (DP-19) and its screen belongs to RWB-E2-031. The agent monitor screen SCR-46 and the autonomy-level screen are out of scope. The exact path of the route in front of the run read is Not specified in the source documents (GAP-0620; ASM-0911).

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-01 | AC1, BR1, BR4 | Component | Case RW-2026-000201, mode SHADOW, answer in 2,000 ms |
| TC-TE-013-02 | AC2, BR2 | Component | AgentRunWorkflow stub silent for 61 seconds on the fake clock; status TIMED_OUT and fallback true |
| TC-TE-013-03 | AC3, BR1 | Component | Mode L1, confidence 0.91, the answer returned as the recommendation |
| TC-TE-013-04 | AC4 | Component | Answer fails check SCHEMA; fallback true with reason SCHEMA |
| TC-TE-013-05 | AC5 | Component | No approved policy on 2026-11-30; no orchestrator call and reason NO_POLICY |
| TC-TE-013-06 | AC6, BR3 | Component | Decision record writer throws; case stays in NEW, MSG-P7-003, `decision_log_id` empty |
| TC-TE-013-07 | AC7, BR5 | Component | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice; one run, one record, the first outcome |
| TC-TE-013-08 | AC8 | Component | Mode OFF; no agent call and no run row; agent version null and fallback false |
| TC-TE-013-09 | Access | Contract | RW-CASEOWN calls GET /api/recovery/agent/v1/admin/agent-runs through the route; refused with 403 and MSG-P4-002 |
| TC-TE-013-10 | Principle 5 | NFR | Decision record write forced to fail during a step in SHADOW mode; the step does not act; MSG-P7-003 |

TC-TE-013-01 to TC-TE-013-10 are the legacy test cases of RWB-TE-013, kept with their IDs, order and data; the legacy System level maps to Component, Access to Contract because the refusal is proved through the route and the published contract, and Resilience to NFR. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same ID.

##### 17. Guardrails

- No business value in code: the mode, the timeout, the fallback rule, the prompt version and the check codes are policy and reference values read at run time (BR10; DP-07).
- No personal data in logs, tests, prompts or records: run rows, IDs, versions, times and codes only; the inputs snapshot is masked before it is referenced and every fixture is synthetic.
- No read of another module's tables and no schema client: the case and the rule result are carried in the request, the lists come through the rwb-case contract and the record through the local library and the P7 read (DP-01, DP-03, DP-07).
- The client never applies an agent answer as the case result in SHADOW or L1 (BR1).
- A step acts only after its record and its link are written; a failed write stops the step with MSG-P7-003 and never falls back to acting (BR3).
- One hop and a 2 s client budget on every consumed REST call; the step operation is the single recorded exception at the policy timeout of 60 seconds (BR8).
- The step operation and the link are idempotent on the step key and on the record reference; a repeat writes nothing twice (BR5, BR11).
- The run read is reached through the gateway-bff route and never from a screen to the service (DP-19).

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-02, TC-TE-013-03, TC-TE-013-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, TC-TE-013-10 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | Business Requirements Program, section 5.4 | FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, TC-TE-013-07, TC-TE-013-08, TC-TE-013-09 |
| D-RCV-60 DP-01 | The run and the policy live in `rwb_agent`; every other service's data is read through its contract | Template and Rules §R5.5 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-07 |
| D-RCV-60 DP-03 | The record of a step is written through the local decision-record library and collected into the ledger | Template and Rules §R5.5; ADR-022 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-01, TC-TE-013-06, TC-TE-013-10 |
| D-RCV-60 DP-04 | The rule result is evaluated through the embedded Drools kit with the packages of rwb-decision | Template and Rules §R5.5; ADR-017 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-02, TC-TE-013-03 |
| D-RCV-60 DP-07 | The autonomy, agent and product lists are read from the rwb-case reference-data contract | Template and Rules §R5.5 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-05, TC-TE-013-08 |
| D-RCV-60 DP-09 | The record leaves through the outbox library and a permanent failure goes to `.dlt` | Template and Rules §R5.5; ADR-015 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-06 |
| D-RCV-60 DP-10 | The Quartz job step of RWB-TE-007 becomes a Temporal step through the workflow kit | Template and Rules §R5.5 and §R6; ADR-016 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-02, TC-TE-013-07 |
| D-RCV-60 DP-11 | The published interface is a REST contract with a mock, one hop, with the policy timeout as its recorded exception | Template and Rules §R5.5; ADR-020 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-09 |
| D-RCV-60 DP-13 | The step and link operations are served on the base `/api/recovery/agent/v1` | Template and Rules §R5.5 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-09 |
| D-RCV-60 DP-15 | The decision link arrives with the service's own Flyway migration in its own schema | Template and Rules §R5.5; ADR-021 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-01, TC-TE-013-07 |
| D-RCV-60 DP-19 | The run read is reached through the gateway-bff route | Template and Rules §R5.5; ADR-019 | FEAT-AGT-11 | All recovery processes | None | TC-TE-013-09 |
| D-RCV-60 DP-20 | The legacy agent client becomes the rwb-agent contract and AgentRunWorkflow on queue `rwb-agent` | Template and Rules §R5.5; Arch v5 slide 16 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-02, TC-TE-013-07 |
| NFR-010 | An agent returns an answer inside its target, after which the rule result is used and the case still routes | TSD P10 Agent runtime v2 T7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-02, TC-TE-013-10 |
| RWB-TE-013 (legacy story) | Agent runtime client with fallback: the eight criteria AC1 to AC8 and the access and resilience tests | Business Requirements Epic 1, section 3.9 | FEAT-AGT-11 | All recovery processes | None | The ten legacy test cases of section 16 |
| RWB-ITG-TE013-ITG (integration copy) | The same behaviour proved across rwb-agent, rwb-decision and a real calling step, with the `-ITG` test cases | Business Requirements Epic 1, section 3.9 | FEAT-AGT-11 | All recovery processes | None | The test cases of that story |

The gap GAP-0619 records what the sources leave open for this story - the two operations the legacy interface spans, the call type, the budget of the step operation, the login and the check-code list - and each default it raises is settled by ASM-0902 to ASM-0907; the route path in front of the run read is settled by GAP-0620 and ASM-0911.

##### 19. Out of scope

- The cross-service behaviour of this key: RWB-ITG-TE013-ITG, and the harness RWB-ITG-W1J01-ITG.
- The contract of the step and link operations and the record payload as published artefacts with their fakes: RWB-P10-TE013-CON.
- The deployment of this capability - chart values, migration job, worker, reference-data and record wiring, feature switch, probes, alerts, route publication, runbook and rollback: RWB-P10-TE013-OPS.
- The agent runtime baseline: the eight agent tables, the prompt and policy store, the tool gateway, the model gateway call and the publication of EV-28: RWB-P10-E1058-APP.
- The guardrail checker and its check codes: RWB-P10-E1058-APP.
- The decision-record library, its envelope and `rwb.decision-record.v1`: RWB-PLT-E1027-CON; the record type, ledger and record read: RWB-P7-E1027-CON.
- The embedded Drools kit and the rule-package client: RWB-PLT-E1072-CON; the rule registry and package versions: P7 rwb-decision.
- The reference lists and their versions: P3 rwb-case, read through RWB-P3-E1043-CON.
- The agent monitor screen SCR-46 and its dashboard: RWB-E2-031.
- Agent answers acted on without a person (autonomy L2 and above, Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028), deviation screening (RWB-E2-029) and the other calling stories.


### RWB-P7-TE013-APP Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: split from RWB-TE-013 for `rwb-decision` — the decision-record half of an agent step: the ledger entry that names the rule and its version, the agent and model versions, the recommendation with its confidence, the applied result and the fallback with its reason, keyed by the step key, chained, read on the two decision-log reads and countable into the fallback rate. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-P7-TE013-APP |
| Work type | APP (App development) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | rwb-decision |
| Service epic | RWB-SVC-P7 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P7-AR |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | RWB-P10-TE013-CON |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P7 rwb-decision v1.md (FR-P7-001, FR-P7-005, FR-P7-006, FR-P7-007, FR-P7-008, FR-P7-009, FR-P7-010, FR-P7-011, FR-P7-029) |
| Status | Draft (realignment v1) |

##### 1. Story

As an **internal audit reader (RW-AUDIT) of the agent steps and of the decision service itself**, I want **the decision-record entry of every agent step held in the central ledger of `rwb-decision` — naming the rule ID and rule version the client applied, the agent version of the legacy form "INTAKE@P1/PR1", the model version, the recommendation with its confidence, the applied result, and `fallback` true with its reason TIMED_OUT, SCHEMA or NO_POLICY in the actions, linked to the agent run by its id, keyed by the idempotency key built from the step key so a repeated step yields one entry, chained to the entry before it, readable on the two decision-log reads and countable into the fallback rate** — so that **every agent answer that a case step used or refused is explainable afterwards by the rule, the versions and the recommendation it came from, and a step whose decision cannot be recorded does not act at all**.

Inside `rwb-decision` this is the decision-record half of the legacy story RWB-TE-013:

- Service `rwb-decision`, schema `rwb_decision`, REST base `/api/recovery/decision/v1`, topic `rwb.decision.events.v1` with event names `rwb.decision.<Event>.v1`, shared topic `rwb.decision-record.v1`, Temporal task queue `rwb-decision` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.decision`.
- One deliverable and nothing else: the decision-record entry of an agent step. It takes one record of one agent step, checks it against the ledger schema — the decision code is a value of LOV-DECISION, the rule ID carries its rule version, the agent version carries its policy and prompt versions in the legacy form, the inputs reference and the decided time are present — links it to the chain with the hash of the entry before it, holds it under the idempotency key built from the step key, writes the inbox row in the same transaction, and serves it back on `GET /decision-log` and `GET /decision-log/{entryId}`.
- The record is produced by the calling step through the local decision-record library of DP-03 in the calling service's own schema, in the step's own transaction and before the step acts; the library publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1` from its outbox, and this service collects it into the central ledger. A write that fails therefore stops the step: the step does not act, the answer is MSG-P7-003 and an incident is raised under R-UNI-39.
- The entry holds the applied result as `final_call` — the next state of the rule result the client applied — and the agent answer only as `recommendation` with the confidence the guardrail checked: null in SHADOW, the checked answer in L1, and never the applied result. It carries the fallback in its actions — `fallback` true and the reason TIMED_OUT, SCHEMA or NO_POLICY, or `fallback` false — with the id of the agent run where a run exists. The key set of that payload and the decision code of an agent step are Not specified in the source documents (GAP-2417; ASM-4025); the legacy mapping of RWB-TE-013 section 12 is carried unchanged.
- The entry is hash chained: `prev_hash` is the `entry_hash` of the entry before it, `entry_hash` is the SHA-256 of its canonical form, `chain_seq` is never reused, and the nightly chain check JOB-14 covers it (NFR-035; FSD P7 v3 A2.1.4.2 and A2.1.4.4). The fallback rate is countable from the same rows, because the agent version is on every entry that had one and the fallback fact is in its actions; the operation and parameter names of the measure are Not specified in the source documents (GAP-2424; ASM-4032) and the measure definition is `rwb-reporting`'s.

Not this story, and said so once here, in section 6 and in section 19: the client itself — the interface, the autonomy mode, the shadow and L1 behaviour, the orchestrator call, the timeout, the policy read, the guardrail checks, the agent run, the prompt and the model registry — is RWB-P10-TE013-CON and RWB-P10-TE013-APP of `rwb-agent` (P10), with the run platform of RWB-E1-058 and the operations side of RWB-P10-TE013-OPS; the screens are the screen slices of `rwb-decision` and of `rwb-agent`; and the cross-service proof of the rule-first order, the 60 second budget, the three fallbacks and the record before the action is RWB-ITG-TE013-ITG, which reads back the P7 half this story builds. This story writes no `agent_run`, no `agent_policy` and no `agent_prompt` row and reads none of them.

The database login used by the capability is the per-service login of DP-02. Its name is Not specified in the source documents (GAP-2420; ASM-4028); this story uses the phrase "the `rwb-decision` login (DP-02)" and never the shared monolith login.

The legacy facts are carried unchanged: one entry per agent step; the rule ID and version of the rule result; the agent version "<agent>@<policy>/<prompt>" with "INTAKE@P1/PR1"; the decision code carried by the calling step and never a constant; the recommendation, null in SHADOW and the checked answer with confidence 0.91 in L1; `final_call` from `ruleResult.toState`, "RESUME_STATE"; the three fallback reasons TIMED_OUT, SCHEMA and NO_POLICY; the link to the run by its id; the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" as the key of the record and the run; the refusal of the whole action when the record cannot be written (MSG-P7-003, R-UNI-39); and one entry for a repeated key (R-UNI-40).

The path this file stands at held an earlier artefact of the same story key from the superseded Work Package B-P7-05; it is replaced here in full and its citations, which named rows no register holds, are gone (GAP-2423; ASM-4031).

##### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The legacy client put every agent call behind one interface, and the entry it wrote was the only place where the rule, the agent, the prompt and the model versions met. In the target that entry is still the proof, but it is written twice over: once locally by the calling service, in its own schema and in the same transaction as its state change, and once centrally, when `rwb-decision` collects it into the ledger on `rwb.decision-record.v1` (Architecture v5 slides 20 and 28; ADR-022). The central entry is what an auditor searches, what the chain seals and what the reports read.

The measure that decides whether an agent stays live is the fallback rate, and the legacy story sets it at below 10 percent per month (RWB-TE-013 section 2). It is measured from these entries: how often the agent did not answer, failed its guardrail or had no policy, against how often an agent step ran at all. A rate that cannot be reconstructed from stored entries is an opinion. This story makes the rate reconstructible without a second store, because the agent version and the fallback fact sit on the same row as the rule version and the applied result.

The realignment changes the mechanism, not the business rule:

1. The `DecisionLogWriter` of the monolith becomes the local decision-record library and the shared topic of DP-03, and the central ledger of this service: the record is written where the decision is taken and sealed where it is searched, which is the difference between a distributed transaction on every step and one local commit (Architecture v5 slide 28). The legacy line "the client publishes none" is superseded by that topic (GAP-2422; ASM-4030).
2. The decision code becomes a value of LOV-DECISION read with the version in force (DP-07), so a new code or sub-decision is a row and not a release.
3. The events become CloudEvents with an outbox on the producer and an inbox here (DP-09), so a redelivery writes no second entry and consumes no second chain sequence.
4. The scheduled work stays with its owner through the workflow kit (DP-10): the ledger copy is continuous ingest on Kafka and not a Schedule, and the chain check JOB-14 at 02:00 belongs to the store slice.
5. Every path is on the owner's base `/api/recovery/decision/v1` (DP-13), the migration is in the per-service Flyway sequence (DP-15), and the two reads are reached through the gateway-bff composite route of the decision-log screen (DP-19).
6. The agent is reached only through the contract of `rwb-agent` (DP-20): the agent version label, the model version and the fallback vocabulary are the contract's, and this story records them rather than deriving them. The contract is published with its fake, and this story is built against that contract and that fake until RWB-P10-TE013-CON lands.

This story carries the decision-record half of REQ-DRI-001 (the record names the rule, model, agent and prompt versions, the inputs, the recommendation, the actions and the outcome), the whole of REQ-DRI-005 (no action proceeds if its entry cannot be written) and the record-side reading of REQ-ACA-010 (the identities that write and read the ledger are checked like people). It supports NFR-033, NFR-034, NFR-035 and NFR-078, and it is the stored fact behind the agent fallback rate.

##### 3. Preconditions

| Precondition | What it gives this story |
|---|---|
| RWB-P10-TE013-CON | The published `rwb-agent` contract of DP-20 and its fake: the agent code, the policy version, the prompt version, the model version, the autonomy mode of the step, the run id, the run status and the fallback with its reason. It is not written yet; this story is built against the published DP-20 contract row and its fake, and every criterion of section 7 runs against that fake (ASM-4027) |
| RWB-PLT-E1027-CON | The local decision-record library and the shared topic `rwb.decision-record.v1` (DP-03): the record shape, its canonical form and SHA-256, the append inside the caller's transaction, the outbox row and the `DecisionRecorded` event |
| RWB-P7-E1008-APP | The `decision_log_entry` baseline in `rwb_decision`: the append-only trigger and grants, the canonical form and the chain of `prev_hash`, `entry_hash` and `chain_seq`, the chain verifier and JOB-14. This story rebuilds none of it |
| RWB-PLT-E1043-CON, RWB-P3-E1043-CON | The reference-data client library and the `rwb-case` contract (DP-07): LOV-DECISION with D1 to D9 and their sub-decisions and X1 to X7, read with the version in force |
| RWB-PLT-TE006-CON | The outbox and inbox library with CloudEvents 1.0 (DP-09): the inbox row of a consumed event, its dedupe and the retry and dead-letter behaviour |
| RWB-PLT-E1072-CON, RWB-PLT-E1071-CON | The embedded Drools kit and the Temporal workflow kit (DP-04, DP-10), held as baselines only: the rule ID and version arrive inside the record, and this story registers no workflow and no Schedule |
| RWB-PLT-E1044-CON, RWB-PLT-N001-CON | The per-service Flyway sequence (DP-15) and the gateway-bff composite route of the two reads (DP-19); this story adds no route |

Business preconditions carried from RWB-TE-013:

- Agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1", and the run of an agent step carries the agent version "INTAKE@P1/PR1" (legacy sections 3 and 7).
- Case "RW-2026-000201" is in route state "NEW" and status "New", and the calling step's rule result is rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE" (legacy background and BR2).
- The decision code of the step is a value of LOV-DECISION read with the version in force; the fixtures carry "D6", the route decision an agent step of the route agent sits in (Architecture v5 slide 3; FSD P7 v3 T3.1 DF-DEC-003). Which sub-decision an agent step writes is Not specified in the source documents (GAP-2417; ASM-4025).
- The step key is "CASEWF:RW-2026-000201:ENTRY:2026-11-30", 38 characters inside the 80 of `decision_log_entry.idempotency_key` (TSD P7 v2 T3.1 DF-DEC-031); it is the idempotency key of the record and of the run (legacy BR5, R-UNI-40).
- The business date of the scenarios is 2026-11-30, the agent answers in 2,000 ms with confidence 0.91 in L1, and the three fallback reasons of the record are TIMED_OUT, SCHEMA and NO_POLICY (legacy section 7).
- Synthetic data only: case identifiers, agent codes, version labels, rule IDs, step keys, statuses and codes, never a real account, customer or answer text (legacy section 17).
- No build dependency. This story is Day 1 by rule (Template and Rules §R5.7): a build dependency the patterns add is a platform CON story of wave 0, and the one C dependency is the published agent contract with its fake. The release date 30 November 2026 is tentative and is copied unchanged.

##### 4. Flow

1. The calling step evaluates its own rule package in its own service through the embedded kit (DP-04) and builds the rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE", before any agent is asked anything (legacy flow steps 1 and 2).
2. The calling step calls the published client with the agent code "INTAKE", the case id, the decision code "D6", the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the rule result and the masked inputs, and the client reads the policy in force through the `rwb-agent` contract (DP-20).
3. The client calls the agent run of `rwb-agent` with the step key as its idempotency key and waits at most the 60 seconds of policy "P1"; in SHADOW it keeps the rule result as the applied result, in L1 it returns the checked answer with confidence 0.91 as the recommendation, and on a timeout, a failed guardrail check or no approved policy it keeps the rule result and marks the fallback true with reason TIMED_OUT, SCHEMA or NO_POLICY (R-UNI-32). None of this is built here; it is the contract this story records.
4. The calling step builds the record of the agent step through the local decision-record library (DP-03): case reference, decision code "D6", rule "R-UNI-32" and version "2026.11", agent version "INTAKE@P1/PR1", the model version the run names, inputs reference of the masked snapshot, recommendation with confidence 0.91 in L1 and null in SHADOW, `final_call` "RESUME_STATE", actions holding the run id, the mode, `fallback` and the reason, the decided time and the idempotency key "CASEWF:RW-2026-000201:ENTRY:2026-11-30".
5. The library appends the record in the calling service's own schema inside the step's transaction, writes the outbox row of `DecisionRecorded` in the same transaction and computes the record hash and its chain link. If the append fails, the transaction rolls back, the step does not act, the client raises its not-recorded condition carrying MSG-P7-003, and one incident is raised under R-UNI-39 (REQ-DRI-005; FSD P7 v3 A2.5.4.3).
6. The outbox relay of the calling service publishes `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, CloudEvents 1.0, keyed by the case id, carrying the record (DP-09; Architecture v5 slides 20 and 42).
7. `rwb-decision` `DecisionRecordListener` consumes the event and writes the inbox row; an event ID already held appends nothing and the repeat count moves by one (DP-09, R-UNI-40).
8. `rwb-decision` `AgentStepRecordValidator` checks the record against the ledger schema: the decision code is a value of LOV-DECISION read through DP-07, the rule ID carries its rule version, the agent version is of the legacy form "<agent>@<policy>/<prompt>" as the `rwb-agent` contract defines it, the inputs reference and the decided time are present, and the idempotency key is present and at most 80 characters. A record that fails is not chained: it is answered with MSG-P7-009 naming the field, held for the retry and dead-letter path with an alert, and the ledger gains nothing (GAP-2418; ASM-4026).
9. `rwb-decision` `AgentStepLedgerAppender`, in one transaction: takes the next `chain_seq`, sets `prev_hash` to the `entry_hash` of the entry before it (64 zeros for the first), computes `entry_hash` as the SHA-256 of the canonical form, and inserts the `decision_log_entry` row with the case reference, the decision code, the rule ID and version, the agent version, the model version, the inputs reference, the recommendation, the applied result as `final_call`, the actions with the fallback and the run id, `decided_at`, the producer identity in `actor_user_id` and the step key in `idempotency_key`; the inbox row commits with it. A key already on the ledger appends nothing, because the unique key of `idempotency_key` refuses a second row and the consumer treats the event as a repeat that returns the first entry id (R-UNI-40; TSD P7 v2 T3.1 DF-DEC-031).
10. A reader with Decision log R reads the ledger: `GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000201` returns the page of the case in scope and `GET /api/recovery/decision/v1/decision-log/{entryId}` returns the entry with its rule ID, rule version, agent version, model version, inputs reference, recommendation, final call, actions, decided time, previous hash, entry hash and chain sequence (API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1).
11. JOB-14 runs the chain verifier of the store slice over the ledger; an entry whose `entry_hash` does not match its canonical form, or whose `prev_hash` is not the `entry_hash` before it, is reported to Compliance the same day and no stored byte is rewritten (NFR-035; FSD P7 v3 A2.1.4.4). Its time of day and parameters are the store slice's (GAP-2420; ASM-4028).
12. Nothing else moves: this story changes no case state, no task, no timer, no agent run, no policy, no prompt and no model. The case stays where `rwb-case` has it, and the run stays as `rwb-agent` has it.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A record arrives with a decision code outside LOV-DECISION, for example "D99" | Refused before any append with MSG-P7-009 naming "decisionCode"; nothing is chained, no `chain_seq` is consumed, and the read returns no entry for the step key | MSG-P7-009 | AC8 |
| X2 | A record carries a rule ID with an empty rule version, or an agent version that is not of the form the `rwb-agent` contract defines, or no inputs reference, or no decided time | Refused with MSG-P7-009 naming the field; nothing is chained and the entry is held for the retry and dead-letter path with an alert | MSG-P7-009 | AC2 |
| X3 | The local decision-record library cannot append the record inside the step's transaction | Nothing is committed on either side: the step does not act, the ledger holds no entry, no `chain_seq` is consumed, the outbox holds no event and one incident is raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X4 | The ledger store is unavailable when the record is ingested | Nothing is appended and no entry is invented; the event stays on the topic, the consumer retries on the platform back-off and the ledger catches up | None to a user; the alert is the platform's | AC6 |
| X5 | The same step key, or the same event ID, arrives again | One entry; the repeat appends nothing, returns the first entry id and moves the repeat count by one | None to a user | AC5 |
| X6 | The reader holds no Decision log right, or the entry id is unknown | 403 with MSG-P4-002 for the right, 404 for an unknown entry id; nothing is returned and no stored row changes | MSG-P4-002 | AC7 |
| X7 | An entry does not match the chain at the nightly check | The break is reported to Compliance the same day with its `chain_seq`; no byte of the ledger is rewritten and the entry stays readable | None to a user; the report is the store slice's | AC7 |
| X8 | The fallback payload carries a reason outside TIMED_OUT, SCHEMA and NO_POLICY | The record is chained as it arrived and the reason is not translated: this service adds no reason of its own, and the vocabulary of the reasons is the `rwb-agent` contract's | None to a user | AC4 |

A record is never updated and never deleted: a wrong record is corrected by a new record that names the one it corrects in `corrects_entry_id`, so the ledger stays append only (REQ-DRI-002; TSD P7 v2 T3.1 DF-DEC-029). The entry and its inbox row are always written together. The text of MSG-P7-009 and the identifiers and texts of the not-found answer and the chain-break report are Not specified in the source documents (GAP-2418; ASM-4026).

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Builds against the `rwb_decision` baseline of RWB-P7-E1008-APP, the record library of RWB-PLT-E1027-CON, the reference-data contract of DP-07 and the published `rwb-agent` contract with its fake (DP-20, RWB-P10-TE013-CON); it runs no agent, writes no agent run and changes no case |
| Negotiable | The decision codes, the fallback vocabulary, the version labels and the message texts are list, contract and message values; the story fixes only the shape of the entry, the chain, the key, the refusals and the reads |
| Valuable | Every agent step is explainable from one entry by the rule and its version, the agent and model versions, the recommendation and the applied result, and the fallback rate is countable without a second store |
| Estimable | One listener, one validator, one appender, one query service, one controller pair, one repository and one migration; it fits one sprint with its tests as the secondary slice of the legacy key |
| Small | The decision-record half only: the client, the mode, the run, the prompt, the policy and the guardrails are other stories' and named in section 19 |
| Testable | Each criterion of section 7 is one automated test against the topic fixture, the reference-data fake, the agent-contract fake and a seeded chain, with a fixed clock |

The story is an APP story with no build dependency: the platform CON stories the patterns add are wave 0 and the one contract dependency is another service's published contract with its fake, so the build is not blocked (Template and Rules §R5.4 and §R5.7 rule 2; GAP-2419; ASM-4027).

##### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback — the rwb-decision decision-record entry of an agent step

  Background:
    Given the environment is SIT
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"
    Given the decision code of the step is "D6" of LOV-DECISION read with its version in force
    Given the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" is the idempotency key of the record

  Scenario: AC1 An agent step gives one entry that names the rule, its version and the applied result (new, D-RCV-60)
    Given the decision-record library wrote the record of the SHADOW step on case "RW-2026-000201" with the rule result applied and fallback false
    When rwb-decision consumes the DecisionRecorded event of that step
    Then exactly one decision_log_entry row exists with idempotency key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    Then the entry names decision code "D6", rule "R-UNI-32", rule version "2026.11" and final call "RESUME_STATE", which is the next state of the rule result the client applied
    Then the entry carries an inputs reference, decided_at, prev_hash, entry_hash and chain_seq, and no agent answer as its final call
    Then GET /api/recovery/decision/v1/decision-log?caseId=RW-2026-000201 returns that one entry for the case, read as a Decision log R holder

  Scenario: AC2 The entry names the agent and model versions of the run, and holds none when no policy is in force (new, D-RCV-60)
    Given the record of the step on case "RW-2026-000201" names agent version "INTAKE@P1/PR1" and the model version the run names
    When the record is consumed
    Then the entry and GET /api/recovery/decision/v1/decision-log/{entryId} both answer agent version "INTAKE@P1/PR1" and that model version
    Then the entry requires a rule version beside its rule ID and an agent version of the form "<agent>@<policy>/<prompt>", and a record without them is refused with MSG-P7-009 naming the field and is not chained
    Given a step on case "RW-2026-000202" ran with autonomy mode "OFF", so no agent run exists and the record carries no agent version
    When that record is consumed
    Then its entry holds no agent version and no model version, final call "RESUME_STATE" and actions fallback false

  Scenario: AC3 The recommendation carries its confidence and the applied result stays the rule result (new, D-RCV-60)
    Given the record of the step on case "RW-2026-000201" was written with autonomy mode "L1" and the agent answer with confidence 0.91 as the recommendation
    When the record is consumed
    Then the entry holds the agent answer in recommendation with confidence 0.91, final call "RESUME_STATE" and actions fallback false
    Then the final call is the rule result and never the agent answer
    Given a second record of the same case was written with autonomy mode "SHADOW" and the same answer
    When that record is consumed
    Then its entry holds no recommendation and the answer stays on the run alone

  Scenario: AC4 A fallback is true with its reason and the run id in the actions (new, D-RCV-60)
    Given three records of agent steps of case "RW-2026-000201", each with its own step key, carry actions fallback true with reason "TIMED_OUT", "SCHEMA" and "NO_POLICY"
    When the three records are consumed
    Then three entries exist with final call "RESUME_STATE", the rule result applied in every one
    Then the actions of each entry hold fallback true, its reason, and the id of the agent run where a run exists
    Then the entry with reason "NO_POLICY" holds no agent run id, because no run was made
    Then no reason is translated or added by this service and a reason outside the three is chained as it arrived

  Scenario: AC5 A repeated step key gives one entry and one chain link (new, D-RCV-60)
    Given the entry with idempotency key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" is on the ledger
    When the same record is delivered again, and then the same event id is redelivered by the topic
    Then one decision_log_entry row exists for the key, the repeat appends nothing and the repeat count moves by one
    Then the repeat returns the first entry id and the chain gains no second link and no second chain sequence
    Then a second row for the same idempotency key is refused by the unique key of the ledger

  Scenario: AC6 A record that cannot be written stops the step and leaves no entry (new, D-RCV-60)
    Given the decision-record library cannot append the record of the step on case "RW-2026-000201"
    When the agent step runs
    Then the append answers with its unavailable condition carrying MSG-P7-003 and the step does not act, because the append is inside the step's transaction
    Then case "RW-2026-000201" stays in route state "NEW", the ledger holds no entry for the step key and no chain sequence is consumed
    Then no DecisionRecorded event reaches rwb.decision-record.v1 for the step and one incident is raised under R-UNI-39
    Given the ledger store is unavailable when a delivered record is consumed
    Then nothing is appended, the event stays on the topic for the retry path and no entry is invented

  Scenario: AC7 The entry is readable on the two reads and the chain covers it (new, D-RCV-60)
    Given the entry of the step on case "RW-2026-000201" is on the ledger at chain_seq 231, after an entry at chain_seq 230
    When a Decision log R holder sends GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the answer carries the decision code, the rule ID and version, the agent version, the model version, the inputs reference, the recommendation, the final call, the actions, decided_at, prev_hash, entry_hash and chain_seq
    Then prev_hash equals the entry_hash of the entry at chain_seq 230 and entry_hash equals the SHA-256 of the entry's canonical form
    Then the nightly JOB-14 chain check verifies the entry and reports any break of it to Compliance the same day without rewriting a byte
    When a role without the Decision log right sends the same read, then the answer is 403 with MSG-P4-002, and an unknown entry id answers 404 with nothing returned

  Scenario: AC8 The decision code is a list value and the fallback rate is countable from the entries (new, D-RCV-60)
    Given a record for the step on case "RW-2026-000201" carries decision code "D99"
    When it is consumed
    Then it is refused with MSG-P7-009 naming "decisionCode", nothing is chained, the chain stands at its last entry and the read returns no entry for the step key
    Given 120 entries of agent version "INTAKE@P1/PR1" were decided in November 2026, of which 9 carry actions fallback true
    When the ledger is counted by agent version and month
    Then the count returns 120 agent steps and 9 fallbacks and the rate 0.0750
    Then the rate is a read of these entries and neither the measure definition nor its threshold is written in this service
```

These eight criteria are new for the `rwb-decision` slice of RWB-TE-013 and are the decision-record criteria of the key; no legacy criterion of RWB-TE-013 is owned verbatim here, because every legacy criterion reads or gives the agent answer and belongs to RWB-P10-TE013-APP, so `acs` is empty for this story. The values are the legacy values of RWB-TE-013 sections 3, 4, 7 and 12 — case `RW-2026-000201`, route state "NEW", agent "INTAKE", policy "P1", prompt "PR1", agent version `INTAKE@P1/PR1`, timeout 60 seconds, answer in 2,000 ms, confidence 0.91, rule `R-UNI-32` version `2026.11`, next state `RESUME_STATE`, decision code `D6`, the step key `CASEWF:RW-2026-000201:ENTRY:2026-11-30`, the fallback reasons `TIMED_OUT`, `SCHEMA` and `NO_POLICY`, and the business date 2026-11-30 — and no new business value is introduced. Case `RW-2026-000202` is a synthetic second case of the same series, used only where a second step key is needed because one key yields one entry; the 120 entries and 9 fallbacks of AC8 are the rate the legacy story sets below 10 percent per month (RWB-TE-013 section 2), and their operation name is the placeholder of GAP-2424.

**Target reading.** The applied result is `final_call`, always the rule result's next state, so an agent answer can never be mistaken for the decision; the recommendation is the separate field the legacy mapping gave it. The fallback and the link to the run travel in `actions`, because no column of TSD P7 v2 T3.1 holds them: `decision_log_entry` has no agent run column and no reason column, and its `actions` is the jsonb of DF-DEC-014 (GAP-2417; ASM-4025). The code in the fixtures is `D6` because the agent step of the fixture sits in the route decision, and on a step with no policy in force no policy version and no prompt version exist, so the agent version is empty — a reading the legacy story fixes only for mode OFF (legacy AC8) and which is applied to NO_POLICY too (ASM-4025).

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every agent step writes exactly one decision record, and no agent step exists without its record | REQ-DRI-001; REQ-DRI-005; R-UNI-39; legacy BR3 |
| BR2 | The decision code of the step is a value of LOV-DECISION read with the version in force; it is never a constant of the code and it is never defaulted by this service | TSD P7 v2 T3.1 (DF-DEC-003); FSD P7 v3 A2.2.4.3 (AC-EXC-P7-002-05); legacy section 12; DP-07; ASM-4025 |
| BR3 | The entry names the rule ID and the rule version of the rule result the client applied, and a rule ID without its version is refused | REQ-DRI-001; TSD P7 v2 T3.1 (DF-DEC-004, DF-DEC-005); FSD P7 v3 A2.3.4.3 (AC-EXC-P7-003-01); NFR-034 |
| BR4 | The applied result is `final_call`: the next state of the rule result, "RESUME_STATE" in the fixtures, and never the agent answer | Legacy section 12 (final_call = ruleResult.toState); TSD P7 v2 T3.1 (DF-DEC-012) |
| BR5 | The recommendation is the checked agent answer with the confidence the guardrail checked in L1, and empty in SHADOW and on a fallback, where the answer stays on the run | REQ-DRI-001; TSD P7 v2 T3.1 (DF-DEC-009); legacy AC1, AC3; legacy BR1 |
| BR6 | A step that fell back holds `fallback` true and its reason TIMED_OUT, SCHEMA or NO_POLICY in the actions; a step that did not holds `fallback` false; this service translates no reason and adds none | R-UNI-32; legacy AC2, AC4, AC5, AC8; the reason vocabulary is the `rwb-agent` contract's (DP-20) |
| BR7 | The entry is linked to the agent run by its id, held with the fallback and the mode in the actions of the entry; this service never writes `agent_run.decision_log_id`, which is `rwb-agent`'s column of its own table | Legacy section 12 (actions "agentRunId", "mode", "fallback", "fallbackReason"); DP-01; ASM-4025 |
| BR8 | The idempotency key of the entry is built from the step key of the agent step, held in `decision_log_entry.idempotency_key`, unique on its own: one step key yields one entry, a repeat returns the first entry and consumes no chain sequence | R-UNI-40; TSD P7 v2 T3.1 (DF-DEC-031); FSD P7 v3 A2.2.4.3 (AC-EXC-P7-002-03); legacy BR5; legacy AC7 |
| BR9 | The record is appended inside the calling step's transaction and before the step acts; a write that fails means the step does not act, the answer is MSG-P7-003 and an incident is raised | REQ-DRI-005; R-UNI-39; FSD P7 v3 A2.5.4.3 (AC-EXC-P7-005-02); legacy BR3; CTL-06; DP-03 |
| BR10 | The entry is read only on `GET /decision-log` and `GET /decision-log/{entryId}`, under the Decision log right R and the scope of the reader; the right is `rwb-access`'s answer and this service holds no role and no scope of its own | TSD P7 v2 T6.1, T6.2 and T-A.2 (API-P7-006, API-P7-007); FSD P7 v3 A2.1.4.3 (AC-EXC-P7-001-02); legacy section 10 |
| BR11 | The entry is append only and hash chained: `entry_hash` over its canonical form, `prev_hash` equal to the entry hash before it, a `chain_seq` never reused, no update and no delete, and the nightly chain check covers it | REQ-DRI-002; REQ-DRI-003; NFR-035; FSD P7 v3 A2.1.4.1 (AC-P7-001-01) and A2.1.4.2 (AC-ALT-P7-001-01) |
| BR12 | The agent version and the fallback fact sit on the same entry, so the agent fallback rate is countable from the ledger by agent version and month without a second store | RWB-TE-013 section 2 (below 10 percent per month); ASM-4032; GAP-2424 |
| BR13 | No personal data in the entry, the event, the trail or the logs: case and run identifiers, a decision code, version labels, a final call, statuses, reasons and dates only, and the inputs reference points at a masked snapshot | Template and Rules §R7.2 s17; Architecture v5 slides 42 and 43; REQ-ACA-005 |
| BR14 | No business value in code: the decision codes, the fallback vocabulary, the agent version form and the message texts are list, contract and message rows, never constants of this service | Template and Rules §R7.2 s17; DP-07; DP-20; FSD P7 v3 BR-P7-002 |
| BR15 | The append is never gated by a feature switch and never skipped for speed: an agent step without its entry is a defect, not a degraded mode | REQ-DRI-005; R-UNI-39; legacy section 13 (the switch of the client is the client's) |
| BR16 | A record that fails the ledger schema is not chained and is never repaired by this service: it is refused with MSG-P7-009 naming the field and held on the retry and dead-letter path with an alert, and the chain stays continuous | FSD P7 v3 A2.2.4.2 (AC-ALT-P7-002-01) and A2.2.4.3; DP-09; ASM-4026 |

##### 9. State transitions

The states below are the states of one decision-record entry of an agent step. The case, the agent run, the policy, the prompt and the guardrail results are not state of this service and are named only so the boundary is visible.

| From | Event | Condition | To |
|---|---|---|---|
| Absent | A `DecisionRecorded` event arrives for an agent step | The code is in LOV-DECISION, the rule ID carries its version, the agent version is of the contract form, the inputs reference and the decided time are present, the key is present | Appended: one row with a `chain_seq`, a `prev_hash` and an `entry_hash`, and the inbox row in the same transaction |
| Absent | A record arrives with a field outside its rule | The validation refuses it | Absent: MSG-P7-009 naming the field, held for the retry and dead-letter path with an alert, and no `chain_seq` consumed |
| Absent | The same step key or the same event ID arrives again | The unique key of the idempotency column and the inbox hold | Appended: unchanged, the first entry id returned, the repeat count moved by one |
| Absent | The record library cannot append the record inside the step's transaction | The step's transaction rolls back | Absent: the step does not act, MSG-P7-003, an incident under R-UNI-39, and no event on the topic |
| Absent | The ledger store is unavailable on consume | The consumer retries on the platform back-off | Absent: the event stays on the topic and the ledger catches up |
| Appended | A later record arrives | The chain head has moved | Appended: the new entry names the previous hash of the head |
| Appended | A wrong entry must be corrected | A person decides the correction | Appended: a new entry with `corrects_entry_id` naming the wrong one; the wrong one stays |
| Appended | Any update or delete is attempted | Through the service role or the schema owner | Appended: refused by the append-only rule, and the attempt is written to the ACE audit log |
| Appended | The nightly chain check runs | The entry hash does not match its canonical form, or its previous hash is not the hash before it | Appended: unchanged and reported to Compliance the same day; nothing is rewritten |

The final call never moves between values through an update: a different outcome is a new entry. The case stays where `rwb-case` has it, and the run, the policy and the prompt stay as `rwb-agent` has them.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| The `rwb-decision` service identity | Consumes `DecisionRecorded`, writes its own `decision_log_entry` row, the chain link and the inbox row, and reads no schema of another service (the `rwb-decision` login, DP-02) |
| The decision-record library identity of the calling service | Appends the local record and writes the outbox row inside the caller's transaction and publishes on `rwb.decision-record.v1` (DP-03) |
| SY-CASEWF and the other calling service identities | Write the record of their own agent step through the library; they hold the C letter of the Decision log in the TSD matrix and write nothing in `rwb_decision` directly |
| SY-AGENT | Writes the run, the policy and the prompt in `rwb_agent`; in this story it holds the C letter only and writes no ledger row |
| RW-AUDIT, RW-COMPLY, RW-COE, RW-CASEOWN, RW-TEAMMGR and every role with Decision log R of TSD P7 v2 T6.1 | Read the entry of an agent step in scope on the two reads and take no other action |
| RW-PLATADM | Receives the incident of a failed append and operates the service; reads the ledger under Decision log R |
| No role | Updates or deletes an entry, reads `agent_run`, `agent_policy` or `agent_prompt` from this service, or reads a service schema directly |

The authorisation decision is `rwb-access`'s and is consumed as the authorise answer the reads declare; the refusal stays 403 with MSG-P4-002 and the unknown entry id 404 of TSD P7 v2 T-A.2. The database login is per service (DP-02) and its name is Not specified in the source documents (GAP-2420; ASM-4028); the story refers to "the `rwb-decision` login (DP-02)".

##### 11. Data

| BR Field ID | Entity in `rwb_decision` | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 | `decision_log_entry` | id | Write |
| DF-DEC-002 | `decision_log_entry` | case_id | Write, the case reference held as a business key with no foreign key to `rwb_case` |
| DF-DEC-003 | `decision_log_entry` | decision_code | Write, a value of LOV-DECISION — "D6" in the fixtures, never a constant |
| DF-DEC-004, DF-DEC-005 | `decision_log_entry` | rule_id, rule_version | Write, "R-UNI-32" and "2026.11" from the rule result; a rule ID with an empty version is refused |
| DF-DEC-006, DF-DEC-007 | `decision_log_entry` | model_version, agent_version | Write, the model version the run names and "INTAKE@P1/PR1", empty when no policy and prompt are in force |
| DF-DEC-008 | `decision_log_entry` | inputs_ref | Write, the reference to the masked inputs snapshot |
| DF-DEC-009 | `decision_log_entry` | recommendation | Write, the checked answer with confidence 0.91 in L1; empty in SHADOW and on a fallback |
| DF-DEC-010, DF-DEC-011, DF-DEC-013, DF-DEC-015 | `decision_log_entry` | approver_user_id, approval_level, override_reason, outcome | Not written: no person approved the step, an agent step carries no delegation level, overrides no recommendation of a person and has no outcome of its own |
| DF-DEC-012 | `decision_log_entry` | final_call | Write, "RESUME_STATE", the applied rule result |
| DF-DEC-014 | `decision_log_entry` | actions | Write, the run id, the mode, `fallback` and the reason; the key set is Not specified in the source documents (GAP-2417; ASM-4025) |
| DF-DEC-016, DF-DEC-017, DF-DEC-018, DF-DEC-028 | `decision_log_entry` | decided_at, prev_hash, entry_hash, chain_seq | Write |
| DF-DEC-029 | `decision_log_entry` | corrects_entry_id | Write only on an entry that corrects an earlier one |
| DF-DEC-030, DF-DEC-031 | `decision_log_entry` | actor_user_id, idempotency_key | Write, the producer identity and "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the key built from the step key, unique on its own |
| DF-DEC-001 to DF-DEC-031 | decision record | all fields | Read through the two decision-log operations |
| (inbox) | library table in `rwb_decision` | event_id, consumer, processed_at | Write, one row per consumed event |

No row of `agent_run`, `agent_policy`, `agent_prompt`, `agent_feedback`, `agent_sample`, `agent_alert`, `agent_evaluation` or `agent_evaluation_run` is read or written here: the run facts arrive inside the record the calling service wrote, and `agent_run.decision_log_id` stays `rwb-agent`'s column (DP-01, BR7). No row of `recovery_case`, `task`, `timer`, `queue`, `parameter_*`, `reference_*` or `lov_value` is written; LOV-DECISION is read through the reference-data contract of `rwb-case` (DP-07) and `lov_value` stays P3's. The outbox of this schema is not written by this story, because the ledger is the seal and publishes nothing. Field IDs are those in the Logical Data Model and Data Dictionary v8 and TSD P7 v2 T3.1.

The model version of agent "INTAKE" is named in no source (GAP-2421; ASM-4029): the legacy story copies it from the run and asserts no literal, so the entry copies whatever the run names and the tests assert equality with the run fixture rather than a literal.

##### 12. Contract

###### 12.1 REST operations provided

Owner `rwb-decision` (P7); base `/api/recovery/decision/v1`. The two reads are API-P7-006 and API-P7-007 of TSD P7 v2 T-A.1. No write operation is exposed: the write path of the entry is DP-03's — the local decision-record library inside the calling service, its outbox and the shared topic of 12.4 — so this service provides the reads and receives the record as an event.

| Method | Path | Purpose | Access | Idempotency |
|---|---|---|---|---|
| GET | `/decision-log` | API-P7-006: search the ledger by case, decision, rule, approver and date, one page at a time; the page of an agent step carries its code, rule and version, agent and model version, final call, actions and decided time | Decision log, right R, scope applied | Not applicable, read only |
| GET | `/decision-log/{entryId}` | API-P7-007: read one entry with its inputs reference, rule ID and version, agent and model version, recommendation, final call, actions, decided time, previous hash, entry hash and chain sequence | Decision log, right R, scope applied | Not applicable, read only |

The request and answer field set beyond the fields TSD P7 v2 T3.1 names is Not specified in the source documents (GAP-2417; ASM-4025). Errors: 401 no session; 403 the role holds no Decision log right (MSG-P4-002); 404 an unknown entry id; 503 the ledger was not read. Every error is an RFC 9457 problem response with `messageId` set.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use in this story |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-DECISION with D1 to D9 and X1 to X7 and its version in force, for the decision-code check of the ingest (DP-07); faked, one hop, 2 s |

The operation is consumed on its published contract or its fake, one hop with a 2 s timeout and a breaker (DP-11, ADR-020). The authorise answer of `rwb-access` is not a REST row of the Ownership Map: it arrives through the platform guard the reads declare, and the guard contract is not in this story's metadata rows (GAP-2419; ASM-4027). This story reads no `rwb-agent` operation at run time: the agent facts arrive inside the record, and the `rwb-agent` contract is consumed as the definition of the version label and the fallback vocabulary (DP-20).

###### 12.3 Events published

None by this story. The ledger is the seal and writes no further event (Architecture v5 slide 28). The shared topic `rwb.decision-record.v1` is P7's and the schema of its event `rwb.decision-record.DecisionRecorded.v1` is defined by this story for the consumers of Architecture v5 slide 42 — `rwb-decision` itself and `rwb-reporting`. The service topic `rwb.decision.events.v1` and its events belong to the approval and registry slices of this service, not to this one. The legacy line "the client publishes none" is superseded by that topic (GAP-2422; ASM-4030).

###### 12.4 Events consumed

| Event | Topic | Owner | What this story does with it |
|---|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by each of the 19 services through its local library; topic and schema owned by P7 rwb-decision | Validates the record of the agent step, appends one `decision_log_entry` per step key and one inbox row in one transaction, and publishes nothing |

The payload carries the record: entry id, case reference, decision code, rule ID and version, agent version, model version, inputs reference, recommendation, final call, actions holding the run id, the mode, `fallback` and the reason, decided time, the producer identity and the idempotency key. The field set is the record shape of RWB-PLT-E1027-CON, and its key set is Not specified in the source documents (GAP-2417; ASM-4025). CloudEvents 1.0, key caseId, no personal field, dedupe on the event id through the inbox (DP-09, ADR-015). TSD P7 v2 T5.3 names `DecisionRecorded` as a published event of the module; the Ownership Map leaves its EV number open among the three P7 events (EV-08, EV-09, EV-30), so the EV number is Not specified in the source documents (GAP-2425; ASM-4033).

###### 12.5 Workflows and activities

None. The ingest is a Kafka consumer with an inbox and a local transaction, not a workflow; the two reads are queries. `rwb-decision` holds `ApprovalWorkflow` of the workflow kit and its rule-promote Schedule for other slices of the service; this story starts no workflow, signals none, registers no activity and puts nothing on the `rwb-decision` queue in namespace `rwb-recovery`.

###### 12.6 Schedules

None registered by this story. The chain check JOB-14 is a Temporal Schedule of the decision-log store slice and covers the entries of this story; the ledger copy is continuous ingest on Kafka and not a Schedule at all (Architecture v5 slide 44). The rule-promote Schedule JOB-20 is the registry slice's. The JOB-14 time of day, its timezone and its overlap policy are the store slice's and are Not specified in the source documents for this story (GAP-2420; ASM-4028).

###### 12.7 Tables owned

| Table | Owner | Use in this story |
|---|---|---|
| `decision_log_entry` | P7 (`rwb_decision`) | The entry of the agent step: the code, the rule and its version, the agent and model versions, the inputs reference, the recommendation, the final call, the actions, the decided time, the two hashes and the chain sequence; written once by the ingest and read |
| inbox library table | PLT library, created in `rwb_decision` | One row per consumed event (DP-09) |
| `approval`, `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case`, outbox library table, `idempotency_key` | P7 or PLT library, created in `rwb_decision` | Not used: an agent step raises no approval, this story evaluates and serves no model, the ledger publishes nothing and the step key is held on the ledger row itself |

Not owned and never read by this story: `agent_policy`, `agent_prompt`, `agent_run`, `agent_sample`, `agent_feedback`, `agent_alert`, `agent_evaluation` and `agent_evaluation_run` (P10); `recovery_case`, `task`, `timer`, `parameter_catalog`, `parameter_value`, `reference_row`, `reference_version` and `lov_value` (P3); `role`, `permission`, `delegation_limit` and `masking_rule` (P4). No foreign key crosses a schema and no row of another service is copied (DP-01).

###### 12.8 Contract fakes

| Fake | Serves | Stubs used by this story |
|---|---|---|
| `rwb-agent` contract fake | RWB-P10-TE013-CON (DP-20), which is not written yet | The run of case `RW-2026-000201` with agent "INTAKE", policy "P1", prompt "PR1", agent version "INTAKE@P1/PR1", the model version, mode SHADOW, status ANSWERED and confidence 0.91; runs with status TIMED_OUT and GUARDRAIL_FAILED and their reasons; the L1 answer; the OFF step with no run; the no-policy step on 2026-11-30; the request journal for the step key, the code and the ordering |
| rwb-case reference-data fake | The P3 list read of DP-07 | LOV-DECISION with D1 to D9 and their sub-decisions and X1 to X7, with its version in force; a variant without "D99" for AC8 |
| authorise fake | The P4 cached permission decision of the reads | The allow answer on the Decision log right R and the scope for the reader of AC7; the refusal of the right for a role that holds Case record R only (GAP-2419; ASM-4027) |
| decision-record library fake | RWB-PLT-E1027-CON | The record of an agent step with its canonical form and hash, the chain link and the outbox row; a forced append failure and an unavailable condition for AC6 |
| Ledger store fixture | RWB-P7-E1008-APP | A seeded chain of 230 entries with their hashes and sequences, the append-only rule, and a chain verifier that reports the altered entry of AC7 |

Each fake is replaced by the real contract as it lands, without a change to the criteria. The `rwb-agent` fake stands only for the facts of the record, because this story calls no agent operation at run time.

###### 12.9 Call-type summary

| Call type | Count in this story | Detail |
|---|---|---|
| REST | Provided 2, consumed 1 | `GET /decision-log` and `GET /decision-log/{entryId}` provided; the P3 reference-data list read consumed, one hop with the 2 s timeout; the authorise answer arrives through the platform guard (GAP-2419) |
| Kafka | Published 0, consumed 1 event type | `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, CloudEvents 1.0, key caseId, dedupe through the inbox (DP-09, DP-14) |
| Temporal | None | No workflow, no activity and no Schedule registered; JOB-14 stays with the store slice and JOB-20 with the registry slice |
| File | None | No file input and no file output; the daily ledger seal is another slice's |

##### 13. Solution plan

**Package.** `th.co.scb.ace.workbench.recovery.decision`, module `ledger/agentstep`, Java package `th.co.scb.ace.workbench.recovery.decision.agentstep`.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

How this story applies each row. **DP-01** keeps the entry in `rwb_decision` alone, the case reference an opaque key and the run facts inside the record (BR7). **DP-03** is the core: the legacy `DecisionLogWriter` becomes the local library of the calling service plus the shared topic, and this service is the collector that chains the same facts centrally. **DP-04** is carried and not used, and `C RWB-P7-E1073-CON` is this service's own contract, so it is same-service here. **DP-07** is where the decision code lives, read with the version in force (BR2). **DP-09** gives the inbox that makes a redelivery write no second entry (BR8). **DP-10** is carried and not used, because the ledger copy is continuous ingest and JOB-14 belongs to the store slice. **DP-11** is the one consumed call, one hop and 2 s. **DP-13**, **DP-15** and **DP-19** put the reads on the service base, the migration in the per-service sequence and the reads behind the composite route, and this story adds no route and serves no screen.

**DP-20** is the story's contract dependency: the agent version label, the model version and the fallback vocabulary of the entry are the `rwb-agent` contract's definitions, so the record cannot be validated without it. RWB-P10-TE013-CON is not written yet; this story is built against the published DP-20 contract row and its fake, which stands in until the contract lands (ASM-4027).

The H and C dependencies the pattern table adds — H RWB-PLT-E1027-CON, RWB-PLT-E1072-CON, RWB-PLT-E1043-CON, RWB-PLT-TE006-CON, RWB-PLT-E1071-CON, RWB-PLT-E1044-CON and RWB-PLT-N001-CON, and C RWB-P3-E1043-CON — are not in the metadata rows of this story, which name None and RWB-P10-TE013-CON. They are recorded in GAP-2419 and ASM-4027, together with the authorise answer of `rwb-access` that no pattern of this story names. **Ready to start stays Day 1**: each H is a platform CON story of wave 0 or this service's own baseline, the one C is another service's published contract with its fake, and none of them blocks the build of an APP story (Template and Rules §R5.7 rules 2 and 8).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| DecisionRecordListener | Listener | Consumes `rwb.decision-record.DecisionRecorded.v1`, writes the inbox row, treats a held event ID as a repeat and answers the first entry id |
| AgentStepRecordValidator | Service | Reads LOV-DECISION with its version in force and checks the code, the rule version beside its rule ID, the agent version form of the `rwb-agent` contract, the inputs reference, the decided time and the key; refuses with MSG-P7-009 naming the field |
| AgentStepLedgerAppender | Service | One transaction: the next `chain_seq`, the previous hash, the entry hash over the canonical form, the `decision_log_entry` row and the inbox row, or nothing |
| AgentStepKeyGuard | Service | Builds and holds the idempotency key of the step key, refuses a second row through the unique key and returns the first entry on a repeat |
| DecisionRecordController | Controller | `GET /decision-log` and `GET /decision-log/{entryId}` with the guard, the scope, the page and the problem mapping for 401, 403, 404 and 503 |
| DecisionRecordQueryService | Service | The page and the single entry, with the scope filter of the authorise answer and the two hashes of the chain; it also counts entries and fallbacks by agent version and month |
| DecisionRecordRepository | Repository | `decision_log_entry` in `rwb_decision`, with the unique keys of `idempotency_key` and `chain_seq` and the indexes of the agent-step read and the count |
| ReferenceDataClient, GuardClient | Clients | The LOV-DECISION read of DP-07 and the cached authorise answer of the reads, one hop each with a 2 s timeout and a breaker |

**Database and migrations**

- Writes `decision_log_entry` and the inbox object of the library, all in schema `rwb_decision`; reads no other schema.
- The `decision_log_entry` baseline, its append-only trigger, its grants, the canonical form, the chain verifier and JOB-14 belong to the decision-log store slice of this service (legacy RWB-E1-008, RWB-P7-E1008-APP) and are not rebuilt here.
- Migration in this story, in the per-service Flyway sequence of DP-15: `V2026_11_02__declog_agent_step_profile.sql` adds the index `ix_declog_agent_step ON decision_log_entry (agent_version, decided_at DESC) WHERE agent_version IS NOT NULL` for the agent-step page and the fallback count, the expression index `ix_declog_fallback ON decision_log_entry ((actions->>'fallback')) WHERE actions ? 'fallback'`, and the check `ck_declog_agent_step_code CHECK (decision_code IS NOT NULL)`. No column is added: the fallback fact and the run id live in `actions` (ASM-4025), and the unique key of `idempotency_key` already exists on the baseline.
- No row is updated and no row is deleted by this story; the update path of the store does not exist and the delete path does not exist.

**Configuration and reference data**

- LOV-DECISION and its version in force are read through the reference-data contract of DP-07; `D6` and the sub-decisions are values of that list and never constants in code (ASM-4025).
- The fallback vocabulary TIMED_OUT, SCHEMA and NO_POLICY, the agent version form "<agent>@<policy>/<prompt>" and the model version are the `rwb-agent` contract's; this service validates the form and records the value, and translates neither (DP-20).
- The 80 character limit of the key is the column length of `idempotency_key` (DF-DEC-031) and the step key of the fixtures is 38 characters. The `rwb-decision` login of DP-02, the Flyway user, the consumer group and the environment names are configuration and their values are Not specified in the source documents (GAP-2420; ASM-4028).
- The feature switches of the client, `rwb.agent.client` among them, stay with RWB-P10-TE013-APP and are not read here: an entry that could be switched off would break R-UNI-39 (BR15).

**Build steps**

1. The migration `V2026_11_02__declog_agent_step_profile.sql` with the two indexes and the check; test that a second row for the same `idempotency_key` and for the same `chain_seq` is refused by the constraints (BR8, BR11, AC5).
2. `AgentStepRecordValidator` with the LOV-DECISION read of DP-07 and the agent version form of the `rwb-agent` contract fake; tests for AC2, AC8 and the refusals of X1 and X2.
3. `AgentStepLedgerAppender` and the chain link over the seeded ledger of 230 entries, with `AgentStepKeyGuard` and the repeat path; tests for AC1, AC5 and AC7, including the first entry with a previous hash of 64 zeros.
4. `DecisionRecordListener` with the inbox, the retry path and the dead-letter alert; tests for the redelivery of AC5 and the unavailable store of AC6.
5. `DecisionRecordController` and `DecisionRecordQueryService` with the authorise answer, the scope, the page, the 403 and 404 refusals and the fallback count by agent version and month; tests for AC7 and AC8, with 120 entries and 9 fallbacks.
6. The privacy test: the entry, the event payload and the log lines carry no name, e-mail address, mobile number, national identity number or account number, and the answer text never enters this service (AC1, AC3).

**Done when.** The ten test cases of section 16 pass, the contract tests of the `rwb-agent` fake stay green, and a SIT day shows one entry per step key with the rule and its version, agent version "INTAKE@P1/PR1", the model version of the run, final call "RESUME_STATE", the recommendation with 0.91 in L1 and `fallback` true with its reason on the three fallback steps; a chain that verifies from its first entry; no entry and no chain sequence when the record cannot be written; one entry for a repeated key; and a fallback count of 0.0750 for the month of the fixture.

##### 14. Validation and messages

| ID | When | Message | Where it is produced |
|---|---|---|---|
| MSG-P7-003 | The record cannot be written and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. | This story, on the append condition; the client carries it to the caller |
| MSG-P7-009 | The decision code is not a value of LOV-DECISION, the rule version or the agent version is missing beside its identifier, or the inputs reference or the decided time is absent | Not specified in the source documents (GAP-2418; ASM-4026) | This story, on the validation; FSD P7 v3 A2.2.4.2 and A2.2.4.3 name only the identifier and the field |
| MSG-P4-002 | The reader holds no Decision log right | You cannot {action} here. Your role does not include it. | This story, through the authorise answer of `rwb-access` |

MSG-P7-003 is copied unchanged from RWB-TE-013 section 14 and from FSD P7 v3 A2.2.3.1 (VR-P7-002-2); MSG-P4-002 is the platform message the authorise contract carries; MSG-P7-009 is named by FSD P7 v3 A2.2.4.2 and A2.2.4.3 and its text is written out in no source this story may read, so the placeholder stands. This story adds no message ID. Thai text for each message follows decision DL10.

##### 15. Screens and states

No screen is built in this story. The decision-log query screen SCR-38 and the decision list of a case belong to the screen slices of this service, and the agent monitor SCR-46 with its fallback rate belongs to RWB-P10-TE013-APP and its dashboard slice; this story neither renders nor hides them and adds no composite route (DP-19).

| Where | State | What the reader sees |
|---|---|---|
| `GET /decision-log` | One page or an empty page | The entries of a case in scope with the decision code, the rule and its version, the agent version, the final call and the decided time; an empty page when no agent step of the case was recorded, and the read invents none |
| `GET /decision-log/{entryId}` | One entry | Code "D6", rule "R-UNI-32" version "2026.11", agent version "INTAKE@P1/PR1", the model version, the recommendation with confidence 0.91 in L1, final call "RESUME_STATE", actions with `fallback` and the run id, decided time, previous hash, entry hash and chain sequence — and, for a fallback step, actions `fallback` true with its reason |
| `GET /decision-log`, `GET /decision-log/{entryId}` | 403 or 404 | MSG-P4-002 for a role without the right, nothing for an unknown entry id |
| The step, seen from the outside | Not recorded | The step does not act and the case stays where `rwb-case` has it; this service shows nothing because it stored nothing |

The screen field list, the composite route specification and the field-level masking belong to RWB-PLT-N001-CON and to the stories that own each screen.

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-09 | AC7, BR10 | Component | A role that holds Case record R only calls the two reads; 403 with MSG-P4-002; an unknown entry id is 404 |
| TC-TE-013-01 | AC1, AC2, AC3, BR3, BR4, BR5 | Component | Case RW-2026-000201, mode SHADOW, answer in 2,000 ms, agent version INTAKE@P1/PR1; one entry with rule R-UNI-32 version 2026.11 and final call RESUME_STATE |
| TC-TE-013-02 | AC4, BR6 | Component | Agent silent for 61 seconds; actions fallback true with reason TIMED_OUT and the run id; final call RESUME_STATE |
| TC-TE-013-03 | AC3, BR5 | Contract | Mode L1, confidence 0.91; recommendation holds the answer with 0.91 and the final call stays the rule result |
| TC-TE-013-04 | AC4, BR6 | Component | An answer that fails check SCHEMA; actions fallback true with reason SCHEMA |
| TC-TE-013-05 | AC4, BR6 | Component | No approved policy on 2026-11-30; actions fallback true with reason NO_POLICY, no run id and no agent version |
| TC-TE-013-06 | AC6, BR9 | Component | The record library throws on the append; MSG-P7-003, no entry, no chain sequence, no event, an incident under R-UNI-39 |
| TC-TE-013-07 | AC5, BR8 | Contract | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice and a redelivered event id; one entry, the first entry id returned, one chain link |
| TC-TE-013-08 | AC2, BR7 | Component | Mode OFF on case RW-2026-000202; no run, no agent version and no model version on the entry, actions fallback false |
| TC-TE-013-10 | AC6, BR9, BR15 | NFR | The append forced to fail during a SHADOW step; the step does not act, MSG-P7-003, the ledger at its last entry, an incident |

The ten test-case IDs are the legacy IDs of RWB-TE-013, kept unchanged and in their legacy order: their Covers cell names the record fact each one now proves on this side of the split, because the client behaviour itself is proved in RWB-P10-TE013-APP and across services in RWB-ITG-TE013-ITG, whose copies carry the `-ITG` suffix. The legacy level System maps to Component or Contract as the rows show, Access to Component and Resilience to NFR; the full test is in Recovery Workbench Test Cases v7.xlsx, tab Story test cases, under the same test case ID.

##### 17. Guardrails

- No business value in code: the decision code, the fallback vocabulary, the agent version form and the message texts are list, contract and message rows, read or validated but never written as a constant here (BR2, BR14).
- No personal data in the entry, the event payload, the trail, the tests or the logs: case and run identifiers, a decision code, version labels, a final call, statuses, reasons and dates only; the inputs reference points at a masked snapshot and the answer text never enters this service (BR13).
- No read of another service's tables (DP-01): no `agent_run`, `agent_policy`, `agent_prompt`, `recovery_case`, `role`, `permission`, `delegation_limit` or `lov_value` row is read or copied, and the authorise answer and the list read arrive on their contracts.
- ACE data only through the owner's contract or `v_ace_*` views: this story reads no ACE data at all. One recorder and no mover: it changes no case status, no task, no timer, no run and no policy, so an entry can never move a case.
- An entry without its event and an event without its entry are both impossible: the record is appended inside the step's transaction before the step acts, and the ledger entry and its inbox row commit together (R-UNI-39).
- Append only and hash chained: no update path and no delete path exist, the chain sequence is never reused, and a wrong entry is corrected by a new one naming the one it corrects (REQ-DRI-002, BR11).
- One entry per step key: the unique key of the idempotency column makes a second entry impossible and a repeat returns the first (BR8, R-UNI-40). A record that fails the schema is refused and held, never repaired and never defaulted (BR16).
- One base, one topic, one queue: `/api/recovery/decision/v1`, `rwb.decision.events.v1` for the other slices of the service and `rwb.decision-record.v1` for the record, `rwb-decision` in namespace `rwb-recovery`; no story in this key declares another service's base or topic as its own (DP-13).
- One hop and 2 s on every consumed call, with a breaker per downstream; a missing answer never produces an entry from a guessed code or a guessed version (DP-11, ADR-020). The record path is never gated by a feature switch and never skipped for speed (BR15).

##### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions, the inputs, the recommendation, the actions and the outcome | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.7 | FEAT-DRI-01, FEAT-DRI-02, FEAT-DRI-03; legacy FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-03, TC-TE-013-07 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7; Business Requirements Epic 1, section 3.7 | FEAT-DRI-05; legacy FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, TC-TE-013-10 |
| REQ-ACA-010 | Agents run under service identities and are subject to the same role checks as people | Business Requirements Program, section 5.4; Business Requirements Epic 1, section 3.9 | FEAT-DRI-02; legacy FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, TC-TE-013-08, TC-TE-013-09 |

| Legacy reference | Where it is kept |
|---|---|
| One decision record per agent step, with the rule ID, rule version, agent version, model version, recommendation, applied result and fallback | Sections 1, 2, 4, 7 (AC1 to AC4), 8 (BR1 to BR7) |
| The step key as the idempotency key and one entry for a repeated step | Sections 7 (AC5), 8 (BR8), 16 (TC-TE-013-07) |
| MSG-P7-003, R-UNI-39 and the step that does not act; MSG-P4-002, the Decision log right and the scope | Sections 5 (X3, X6), 7 (AC6, AC7), 8 (BR9, BR10), 10, 14 |
| The legacy values INTAKE, P1, PR1, INTAKE@P1/PR1, RW-2026-000201, R-UNI-32 2026.11, RESUME_STATE, the step key, 60 seconds, 0.91 and 2,000 ms | Background and scenarios of section 7; section 3 |
| Legacy key RWB-TE-013, story RWB-P7-TE013-APP, contract RWB-P10-TE013-CON, test cases TC-TE-013-01 to TC-TE-013-10 and the eleven decoupling patterns | Metadata, sections 3, 12, 13 and 16 |

The other slices of the key answer the rest: RWB-P10-TE013-CON and RWB-P10-TE013-APP own the client, the mode, the shadow and L1 behaviour, the orchestrator call, the timeout, the policy and prompt versions, the guardrails, the run and the model registry; RWB-P10-TE013-OPS the operations of `rwb-agent`; RWB-E1-058 the agent platform; RWB-ITG-TE013-ITG the proof across the real services; and the store slice of `rwb-decision` (legacy RWB-E1-008) the append-only table, the chain verifier and the nightly chain check.

##### 19. Out of scope

- The client itself: the published interface, the autonomy mode of the step, the SHADOW and L1 behaviour, the orchestrator call, the 60 second timeout, the policy read, the guardrail checks, the agent run and its status, the prompt, the model and its registry, the fallback decision and the fallback vocabulary — RWB-P10-TE013-CON (the contract and its fakes), RWB-P10-TE013-APP (the runtime), RWB-P10-TE013-OPS (the operations) and the agent platform of RWB-E1-058. This story records their facts and derives none of them.
- The agent policy, the prompt store, the sample and evaluation harness, the monitoring dashboard SCR-46 and the fallback rate as a published measure: `rwb-agent` (P10) and the measure definition of `rwb-reporting` (P9). This story makes the rate countable and does not define, publish or threshold it (GAP-2424; ASM-4032).
- The decision-log store of this service — the append-only trigger, its grants, the canonical form, the chain verifier and the nightly chain check: the store slice of `rwb-decision` (legacy RWB-E1-008, RWB-P7-E1008-APP) and the service baseline.
- The screens of the decision log and of the agent monitor, the approval routing, the delegation of authority, the decision center screens and the rule package registry: the screen, approval and registry slices of `rwb-decision` and of `rwb-agent`, with the gateway-bff route of RWB-PLT-N001-CON.
- The case record, the case status, the route state, the task and the timer (`rwb-case`, P3), the role, the scope, the masking policy and the authorise answer (`rwb-access`, P4), and the cross-service harness with its `-ITG` copies of the test cases (RWB-ITG-TE013-ITG).
- The DB, INF and OPS stories of this legacy key: their own stories; the Helm chart, the Kafka subscription values, the metrics, the alerts and the runbook of this capability are the OPS story's. The daily ledger seal to immutable storage and the lake copy are another slice's, and the lake is removed (DP-17).

The names of the holders of a role and the parameter values of the lists are data of their owners, and no date is changed by this story: the release 30 November 2026 is copied unchanged and stays tentative.


### RWB-P10-TE013-OPS Agent runtime client with fallback

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | RWB-P10-TE013-OPS |
| Work type | OPS (DevOps) |
| Suggested owner | DevOps team (suggested; any team may pick up this story) |
| Service | rwb-agent |
| Service epic | RWB-SVC-P10 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-P10-M |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD P10 rwb-agent v1.md (FR-P10-001, FR-P10-002, FR-P10-003, FR-P10-004, FR-P10-008, FR-P10-009, FR-P10-010, FR-P10-011, FR-P10-015, FR-P10-018, FR-P10-024, FR-P10-025, FR-P10-026) |
| Status | Draft (realignment v1) |

**Change log.** D-RCV-60, 22 November 2026: deployment slice of RWB-TE-013 for rwb-agent. This story deploys the client capability of the key: the rwb-agent api and worker deployments from the service template, the pre-deploy migration job of `V10_002__agent_run_decision_link.sql` on the per-service Flyway sequence (**DP-15**), the worker on queue `rwb-agent` in namespace `rwb-recovery` with AgentRunWorkflow and the three client activities (**DP-10**, **DP-20**), the boundary wiring of the rwb-case reference lists (**DP-07**), the decision-record library with the publish right on `rwb.decision-record.v1` and its retry and `.dlt` topics (**DP-03**, **DP-09**), the approved autonomy policies and the legacy `rwb.agent.client` switch, the probes, dashboards, alerts carrying MSG-P7-003 and the fallback rate, the publication of the run read through gateway-bff (**DP-19**), the runbook, the rollback and the capacity plan. It deploys no lake artefact, no extract and no Quartz job table: the legacy dependence on RWB-TE-007 is retired under §R6. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

##### 1. Story

As a **platform engineer**, I want **rwb-agent deployed from the service template with its api and worker deployments, its `V10_002__agent_run_decision_link.sql` migration job, its probes, its Temporal worker and KEDA scaling on the `rwb-agent` task queue, the wiring of the rwb-case reference lists and of the decision-record library with the publish right on `rwb.decision-record.v1` and its retry and `.dlt` topics, the approved autonomy policies and the legacy `rwb.agent.client` switch, the dashboards and alerts that watch a fallback rate, a record write failure and a refused link, the publication of the run read through the gateway-bff route, the runbook, the rollback and the capacity plan**, so that **a calling step can reach the agent client from day one in every environment, the fallback rate and every failed decision record are visible and actionable, and an operator can restart a stuck step, a refused link or a worker backlog without reading code and without a Quartz job table that no longer exists**.

##### 2. Business rationale

The legacy story depends on a Quartz chain of RWB-TE-007 with its run books and its shared job table, an in-process orchestrator and a decision log writer of P7 inside the same deployment. In the target a service is a Helm release built by one pipeline with its own schema, login, topic rights, queue and Schedules (DP-02, DP-10, DP-15), the record is written by the calling step through a shared library into the ledger topic (DP-03), and the orchestrator is a workflow on the rwb-agent queue (DP-20). Deployment is therefore part of the capability:

- Without the worker on queue `rwb-agent` with AgentRunWorkflow and the three client activities, a submitted step would hang until its policy timeout and every step would fall back.
- Without the migration job, `agent_run.decision_log_id` is absent or unindexed and the link of a record to its run cannot be stored, so no step may act.
- Without the publish right on `rwb.decision-record.v1` and the relay, the ledger of rwb-decision falls behind the steps and an audit read of a case finds no record.
- Without the alert on a record write failure, a step that refuses to act looks like a quiet case rather than a decision that could not be recorded, and MSG-P7-003 is never seen.
- Without the route publication, the run read and its fallback column are unreachable from a screen and the fallback measure has no reader.

This story makes the capability observable and repeatable. It deploys and watches; it changes no business behaviour and holds no business value.

##### 3. Preconditions

- The service template, the chart skeleton and the pipeline are available (RWB-PLT-TPL, RWB-PLT-LIB), and the Temporal workflow kit with namespace `rwb-recovery` is in place (RWB-PLT-WF, RWB-PLT-E1071-CON).
- The Kafka event platform provisions topics with a retry topic and a `.dlt` topic (RWB-PLT-EVT, RWB-PLT-TE006-CON), and the shared topic `rwb.decision-record.v1` exists with its rights (RWB-PLT-E1027-CON).
- The ACE database administrator has created schema `rwb_agent` and the login, with rights on `rwb_agent` only (DP-02). That login is Not specified in the source documents (GAP-0621; ASM-0913).
- The platform error envelope, the message catalogue and the alert routing are in force, so an alert can carry a message ID.
- The contract baseline of RWB-P10-TE013-CON is published: the two operations, their members, their refusals, the record payload and the three fakes.
- The baseline release of RWB-P10-E1058-OPS is known and deployed, because it owns the schema baseline, the topic `rwb.agent.events.v1` and the worker that runs the six baseline activities of AgentRunWorkflow.
- RWB-P3-E1043-CON (reference lists) and RWB-P7-E1027-CON (record read) are published for the boundary wiring.
- The three environments DEV, SIT and UAT exist with the parameter scope of LOV-ENVIRONMENT.
- The chart values, replica counts, probe paths and timings, resource sizes, topic partitions, worker concurrency, alert thresholds and deployment topology are Not specified in the source documents (GAP-0621; ASM-0912, ASM-0914).
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7).

##### 4. Flow

1. The pipeline builds one image and one chart version from one commit, runs the unit, component and contract tests, scans the image and the dependencies, and publishes the chart.
2. The chart deploys the api and worker deployments with the `rwb_agent` login reference, the pre-deploy migration job of `V10_002__agent_run_decision_link.sql` after `V10_001__agent_runtime.sql`, and the probes; the job runs before the rollout is marked ready (AC1; DP-15).
3. The provisioning step checks the task queue `rwb-agent` in namespace `rwb-recovery` and the publish right of rwb-agent on the shared `rwb.decision-record.v1`, and confirms that the retry topic and the `.dlt` topic of the decision-record family are the platform's and bound to this producer; the release creates no topic and no consumer group (AC2; DP-03, DP-09).
4. The worker registers AgentRunWorkflow with its six baseline activities and the three client activities ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord on queue `rwb-agent`, with the release build ID on the version set (AC2).
5. The configuration step wires LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT through the rwb-case reference-data contract, the record read through the rwb-decision contract, and the approved `agent_policy` rows with their modes, timeouts and prompt versions; no mode, timeout, agent code or check code is written into a values file (AC3; DP-07).
6. The legacy flag `rwb.agent.client` is registered with the platform flag library, off by default in DEV and on in SIT and UAT only after the smoke step answers (AC3).
7. The dashboards are published: step submissions by outcome, fallback rate per agent and policy version against the 10 percent target, runs by status, record writes and failures, refused links, worker backlog and refused reads (AC4).
8. The alerts are wired to MSG-P7-003 for a record write failure, to the fallback rate above target, to a refused link, to a `.dlt` message on the decision-record topic and to a failed migration, each linked to one runbook entry (AC4).
9. The route publication step registers the run read `GET /api/recovery/agent/v1/admin/agent-runs` behind the gateway-bff pass-through route, one hop, and checks the health of the route target (AC5; DP-19).
10. A smoke step submits a synthetic step for case "RW-2026-000201" against the three fakes, reads the outcome and the run through the route, and checks the record write, the link, the probes and the alerts (AC5, AC6).

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The migration job of `V10_002__agent_run_decision_link.sql` fails | The deployment stays unready and the pipeline stops; no traffic to the new version and no step is linked | None | AC1 |
| X2 | The readiness probe fails after the start-up window | The pod is removed from the service and the pipeline marks the release failed | None | AC1 |
| X3 | The task queue is not registered, or the worker build ID is not on the version set | The release fails; a submitted step would otherwise wait until its policy timeout and fall back | None | AC2 |
| X4 | The publish right on `rwb.decision-record.v1` is missing, or a record lands in `.dlt` | The release fails on the missing right; a refused record is alerted with its reference and registry subject and a runbook entry is opened | None | AC2 |
| X5 | A record write fails at run time | The step does not act; the alert carries MSG-P7-003 with the step key, the agent and the business date and opens a ticket | MSG-P7-003 | AC4 |
| X6 | A link is refused with 409 because the run holds another record | The refused-link alert carries the run ID and both references and opens a ticket for the data steward; neither record is deleted | None | AC4 |
| X7 | The reference-data contract or the record read is unavailable during start-up | The readiness probe answers unready and the release is not marked ready; no step is served with a guessed mode | None | AC3 |
| X8 | The worker backlog passes its threshold on queue `rwb-agent` | KEDA scales the worker on the backlog and, if it persists, the on-call rota opens the backlog runbook entry | None | AC2 |
| X9 | The route publication fails or the route target is not healthy | The release fails and the run read stays unreachable; no partial route is left | None | AC5 |
| X10 | A role without the right reads agent runs | The refused-read count rises on the dashboard with MSG-P4-002 and never pages the on-call rota | MSG-P4-002 | AC4 |

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the chart skeleton, the platform topic provisioning, the workflow kit and the published contracts; no application code is built here |
| Negotiable | Replica counts, resource sizes, partitions, concurrency, alert thresholds and cluster topology are environment values, not story decisions |
| Valuable | Makes the client reachable and observable from day one, keeps every step's record and link deployable, and keeps the retired Quartz chain out of the release |
| Estimable | One chart, one pipeline stage, one migration job, two deployments, two probes, one provisioning check, a Schedule-free worker registration, six dashboard panels, five alert rules and six runbook entries |
| Small | Fits one sprint with the runbook and the capacity plan |
| Testable | Every criterion tests an artefact: the chart renders, the probes answer, the queue is registered, the wiring comes from contracts, the alerts fire on a synthetic condition, the route answers within 2 s |

##### 7. Acceptance criteria

```gherkin
Feature: Deployment of the rwb-agent agent runtime client capability

  Background:
    Given the service template chart and the platform pipeline are in force
    Given the target environment is SIT

  Scenario: AC1 The chart deploys the api and worker with the decision-link migration (new, D-RCV-60)
    Given the rwb-agent Helm chart and its values files
    When the chart is rendered for DEV, SIT and UAT
    Then each render succeeds with the chart version and the image digest pinned
    Then the release declares the api deployment and the worker deployment, the pre-deploy migration job of V10_002__agent_run_decision_link.sql and the platform secret references
    Then the migration job runs the per-service Flyway sequence in schema rwb_agent after V10_001__agent_runtime.sql and before the rollout is marked ready, and it creates no table
    Then agent_run holds decision_log_id and its index, and the step key index exists for the repeat lookup
    Then the release declares no Quartz job table, no job admin read and no lake artefact
    Then no replica count, resource size, timeout or mode is hard-coded in the template

  Scenario: AC2 The worker, the queue and the record topic are in place (new, D-RCV-60)
    Given the provisioning step and the worker deployment
    When a synthetic backlog is queued on rwb-agent in namespace rwb-recovery
    Then the worker polls only its own task queue with the release build ID on the version set and KEDA scales it on backlog
    Then AgentRunWorkflow, ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord are registered by the same worker
    Then the release holds the publish right on rwb.decision-record.v1 and the retry topic and the .dlt topic of the decision-record family are bound to it, with the relay interval of the outbox
    Then the release creates no topic of its own and no consumer group, and no consumer group reads a topic of another service
    Then the legacy job table and its admin read are used by nothing in the release

  Scenario: AC3 The reference lists, the record read, the policies and the feature switch are wired by contract (new, D-RCV-60)
    Given the values files and the configuration step
    When the release is rendered and started
    Then LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT are read through the rwb-case reference-data contract and the record read through the rwb-decision contract
    Then the approved agent_policy rows carry the modes OFF, SHADOW and L1, timeout_seconds 60 and the prompt version, and no mode, timeout, agent code or check code appears in a values file or in the chart template
    Then the rwb.agent.client switch is off in DEV and on in SIT and UAT only after the smoke step answers, and off starts no run and writes the record with agent version null
    Then every secret is a reference to the platform secret store, and no secret value is in the chart, the dashboards or the runbook

  Scenario: AC4 Alerts and the runbook cover the fallback rate, the record failure and the refused link (new, D-RCV-60)
    Given the published dashboards and the runbook
    When a synthetic step is replayed with a fallback, a failed record write and a refused link
    Then the fallback-rate panel carries the rate per agent and policy version against the 10 percent target
    Then the record-failure alert carries MSG-P7-003 with the step key, the agent and the business date
    Then the refused-link alert carries the run ID and both record references and opens a ticket for the data steward
    Then the .dlt alert fires on a refused record with its record reference and its registry subject
    Then the refused-read count carries MSG-P4-002 and does not page the on-call rota
    Then every alert links one runbook entry with the check, the owner role and the recovery step

  Scenario: AC5 The probes and the smoke step answer through the route (new, D-RCV-60)
    Given a running pod of the api and of the worker
    When the readiness probe is called before the migration job and the start-up window complete
    Then the pod is not marked ready
    When the readiness and liveness endpoints are called after start-up
    Then both answer healthy without a database write
    Then the smoke step submits agent "INTAKE" for case "RW-2026-000201" with step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" against the three fakes and answers the outcome within the 60 second policy budget
    Then the run is read through the gateway-bff route within the 2 s budget
    Then the route path is Not specified in the source documents (GAP-0621; ASM-0915)

  Scenario: AC6 The runbook, the rollback and the capacity plan are accepted (new, D-RCV-60)
    Given the runbook, the rollback plan and the capacity plan
    When the on-call rota walks the six entries and the rollback is rehearsed in SIT
    Then the rollback redeploys the previous chart version, re-registers no Schedule, leaves the schema at its forward-only version and leaves the publish right in place
    Then the capacity plan states the step throughput of a peak business date, the worker minimum and maximum, the queue backlog trigger and the database connection cap of the login
    Then the plan records no Quartz job window and no lake window, because both are retired or removed
    Then the deployment topology detail, the host, the SKU and the budget are Not specified in the source documents (GAP-0621; ASM-0912)
```

**Target reading.** The six criteria are new (D-RCV-60) and test only this deliverable: the chart, the migration job, the queue and topic rights, the wiring, the alerts, the probes, the route and the operations artefacts. The legacy values used in the fixtures - agent "INTAKE", the policy with timeout 60 seconds, case "RW-2026-000201", the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the modes OFF, SHADOW and L1, the 10 percent fallback target and the message IDs MSG-P7-003 and MSG-P4-002 - are copied from RWB-TE-013 and from the app story, character for character. No criterion asserts a business outcome, which is RWB-P10-TE013-APP's.

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One service, one schema, one login: the release uses the `rwb_agent` login reference and no other service's credential | DP-02; Arch v5 slide 41 |
| BR2 | The decision link arrives as a per-service Flyway sequence in schema `rwb_agent` and runs before the rollout is ready, and it creates no table | DP-15; RWB-PLT-E1044-CON |
| BR3 | The release holds the publish right on `rwb.decision-record.v1` and never creates the topic, the retry topic or the `.dlt` topic, which are the platform's and the record library's | DP-03; DP-09; RWB-PLT-E1027-CON |
| BR4 | Every topic a producer writes has a retry topic and a `.dlt` topic, and the outbox relay publishes within its interval | DP-09; Arch v5 slide 11 |
| BR5 | The worker registers AgentRunWorkflow and the three client activities on queue `rwb-agent` in namespace `rwb-recovery` and holds no Schedule of its own | DP-10; Arch v5 slides 16 and 44 |
| BR6 | No environment value is hard-coded: replica counts, resource sizes, alert thresholds, partitions, concurrency, the modes and the timeout come from values files and contracts | DP-07; Template and Rules §R7.2 s17 |
| BR7 | An alert carries a message ID where one exists, the agreed text, and links one runbook entry | Template and Rules §R7.2 s14 |
| BR8 | The release writes only schema `rwb_agent` and reads other services only through their contracts | DP-01 |
| BR9 | A refused read is counted on the dashboard and never pages the on-call rota | MSG-P4-002 |
| BR10 | The release carries no Quartz job table, no job admin read and no lake artefact; the legacy dependence on RWB-TE-007 is retired and points to the workflow kit | §R6; DP-10; DP-17; ASM-0912 |
| BR11 | The run read is published behind the gateway-bff pass-through route, one hop, and a screen never calls rwb-agent directly | DP-19; ADR-019 |
| BR12 | A record write failure is an alert with MSG-P7-003 and a ticket, so a step that correctly refused to act is never mistaken for a quiet case | R-UNI-39; legacy X4 |

##### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| Not deployed | Chart published | The image, the chart and the migration job pass the pipeline | Deploying |
| Deploying | Migration job complete and probes healthy | The schema is at the expected version, the worker has polled, the relay runs and both probes answer | Ready |
| Ready | Boundary check passed | The lists and the record read answer, and a synthetic step answers its outcome | Ready with the client live |
| Ready | Release superseded | A new chart version is promoted | Rolling |
| Rolling | All pods on the new version | The old ReplicaSet drains and the worker build ID is on the version set | Ready |
| Ready | Migration job failed, probes failed or a required right missing | The schema is not at the expected version, a probe is unready or the publish right is absent | Failed |
| Failed | Rollback | The previous chart version is redeployed and the forward-only schema stays | Ready |

The states of a step, a run and its record - RUNNING, ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, NO_POLICY and the link - are the app story's and are only watched here.

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| DevOps engineer | Owns the chart, the values files, the pipeline stages, the provisioning and route publication steps, the dashboards, the alerts and the runbook |
| Platform administrator | Owns the `rwb-recovery` namespace, the task queue, the shared topic's rights and the flag registration |
| ACE database administrator | Owns the `rwb_agent` schema, the login, its grants and the migration job approval |
| Release manager | Approves the promotion of one artefact through the environments |
| On-call operator | Runs the six runbook entries and opens an incident when a fallback rate, a record failure, a refused link or a backlog persists |
| RW-PLATADM | Re-presents a step of a business date in the running service, not in the cluster |

The per-service login name used by the chart is Not specified in the source documents (GAP-0621; ASM-0913); the chart references it through a secret reference and never a literal password.

##### 11. Data

| Item | Content |
|---|---|
| Deployment values | Image digest, chart version, replica counts, resource requests and limits, probe paths and timings, log level, feature switches, environment name |
| Schema | `rwb_agent`, migrated by the per-service Flyway sequence; the decision link and its indexes from this release and the library objects |
| Topic rights | The publish right of rwb-agent on `rwb.decision-record.v1`, with the retry topic and the `.dlt` topic of the platform and the relay interval of the outbox |
| Queue | Temporal task queue `rwb-agent` in namespace `rwb-recovery`; no Schedule |
| Policies | The approved `agent_policy` rows with autonomy_mode OFF, SHADOW and L1, timeout_seconds 60 and the prompt version, read at run time and never held as deployment values |
| Reference data | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT through the rwb-case reference-data contract |
| Dashboard series | Step submissions by outcome, fallback rate per agent and policy version, runs by status, record writes and failures, refused links, worker backlog, refused reads |
| Runbook entries | Record write failure, refused link, fallback rate breach, `.dlt` message, worker backlog, migration failure or route unavailable |
| Secrets | The `rwb_agent` login secret, the Kafka client credential and the Temporal mTLS material, all from the platform secret store |

The deployment topology detail (cluster names, node pools, replica counts, resource sizes, zone spread, ingress class, probe timings), the host, the SKU and the budget are Not specified in the source documents (GAP-0621; ASM-0912); the chart exposes them as values and this story fixes only their names and the rule that they are not hard-coded. The alert thresholds and the runbook wording are Not specified in the source documents (GAP-0621; ASM-0914). There is no lake path, no extract and no Quartz job window to document.

##### 12. Contract

###### 12.1 REST operations provided

The deployment exposes the two client operations on `/api/recovery/agent/v1`, owner rwb-agent (P10), as fixed by RWB-P10-TE013-CON: `POST /agent-steps` and `PUT /agent-runs/{runId}/decision-record`. The run read `GET /api/recovery/agent/v1/admin/agent-runs` and the other ten platform operations are served by the same release under the baseline of RWB-P10-E1058-CON and are registered on the route with this story's operations. The probes are cluster-internal and not part of the API surface.

###### 12.2 REST operations consumed

| Method | Path | Owner | Deployment need |
|---|---|---|---|
| GET | `/api/recovery/case/v1/admin/lists/{listCode}` | P3 rwb-case | LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT with their version, checked by the readiness probe and the smoke step; 2 s client budget (DP-07, DP-11) |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | The record read-back before a link is stored, checked by the smoke step |

No operation of rwb-integration is deployed here, and the model endpoint INT-23 is called inside AgentRunWorkflow by the baseline release of RWB-P10-E1058-OPS and is not wired by this story.

###### 12.3 Events published

| Event | Topic | Provisioning |
|---|---|---|
| `rwb.decision-record.DecisionRecorded.v1` (EV-08) | `rwb.decision-record.v1` | The release takes or verifies the publish right of rwb-agent and the binding of the retry topic and the `.dlt` topic of the platform; it creates no topic and no consumer group. The record is written by the calling step through the library in its own transaction, so the producer credential this release holds is the one the library uses |

No agent event is provisioned by this story: `rwb.agent.AgentRunCompleted.v1` (EV-28) on `rwb.agent.events.v1` belongs to RWB-P10-E1058-OPS and is unchanged. No lake copy and no extract event exists.

###### 12.4 Events consumed

None by this release. It creates no consumer group: the consumers of EV-08 are rwb-decision and rwb-reporting, and their groups belong to their own releases.

###### 12.5 Workflows and activities

| Name | Type | Task queue | Deployment element |
|---|---|---|---|
| AgentRunWorkflow | Workflow of the baseline, one execution per step key with the key as workflow ID | `rwb-agent` | Registered by the release worker with the release build ID on the version set |
| ResolveAutonomyMode | Activity | `rwb-agent` | Registered by the same worker; reads `agent_policy` and the P3 lists |
| ApplyAutonomyMode | Activity | `rwb-agent` | Registered by the same worker |
| LinkDecisionRecord | Activity | `rwb-agent` | Registered by the same worker; writes `decision_log_id` |
| KEDA scaling | Worker scaler | `rwb-agent` | Scales on the task-queue backlog with a minimum and a maximum from the values file |

No Schedule is registered, updated or watched by this release: a step is started by its caller.

###### 12.6 Schedules

None. The key starts no Schedule, and the legacy dependence on the Quartz entry of RWB-TE-007 is retired under §R6: the release deploys no job table, no job admin read and no cron entry, and a job step that called the client is a Temporal step of the calling service through the workflow kit of RWB-PLT-E1071-CON (DP-10).

###### 12.7 Tables owned

| Table | Owner | Deployment element |
|---|---|---|
| agent_run | P10 (`rwb_agent`) | The decision link column DF-AGT-058 and its index arrive from `V10_002__agent_run_decision_link.sql`; the table itself is the baseline's |
| agent_policy, agent_prompt | P10 (`rwb_agent`) | Created by the earlier P10 migrations; read by the mode resolution |
| outbox_event, processed_event, idempotency_key | PLT library, created in `rwb_agent` | Created by the same migration job and used by the idempotency of the step key |

No table is created by this story and no grant crosses a schema (DP-01, DP-15). `decision_log_entry` is written by the calling step in its own schema and is never created here.

###### 12.8 Contract fakes

| Fake | Deployment use |
|---|---|
| Decision-record library and record-read fake (RWB-PLT-E1027-CON, RWB-P7-E1027-CON) | Runs in the pipeline and in the SIT smoke profile so the release can start without rwb-decision, with a written record, its reference and a 503 path |
| rwb-case reference-data fake (RWB-P3-E1043-CON) | Same, answering LOV-AUTONOMY, LOV-AGENT and LOV-PRODUCT |
| gateway-bff route stub (RWB-PLT-N001-CON) | Same, a pass-through of one hop in front of the run read |

The fakes are test-only workloads; they are not deployed into UAT or production.

###### 12.9 Call-type summary

| Call type | Count | Detail |
|---|---|---|
| REST | 2 provided by this release and 11 by the baseline, 2 consumed | The step and link operations on `/api/recovery/agent/v1`; the lists and the record read consumed, one hop and 2 s each |
| Kafka | 1 published by the calling step through the library, 0 consumed | EV-08 on `rwb.decision-record.v1` with the retry and `.dlt` topics; the release holds the publish right and creates no topic |
| Temporal | 1 workflow of the baseline, 3 activities of this story, 0 Schedules | AgentRunWorkflow with ResolveAutonomyMode, ApplyAutonomyMode and LinkDecisionRecord on queue `rwb-agent`, with KEDA on backlog |
| File | None | The release carries no file, no extract and no lake credential |

##### 13. Solution plan

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON; C RWB-P7-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; the rule result is a request member |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON as the legacy dependency of the pattern |

**Artefacts**

| Artefact | Content |
|---|---|
| `helm/rwb-agent/` | Chart with the api deployment, the worker deployment, the service, the migration job, the config map, the secret references and the probes; no Schedule registration hook |
| `helm/rwb-agent/values-dev.yaml`, `values-sit.yaml`, `values-uat.yaml` | Image digest, replicas, resources, probe timings, log level, feature switches, environment name |
| Pipeline stage | Build, unit and contract tests, image and dependency scan, chart publish, promote the same artefact |
| Provisioning step | Task queue `rwb-agent` in namespace `rwb-recovery`; the publish right on `rwb.decision-record.v1` and its retry and `.dlt` bindings; no topic and no consumer group created |
| Route publication | The two client operations and the run read registered behind the gateway-bff pass-through route, one hop |
| KEDA scaling | Worker scaled on the task-queue backlog with a minimum and a maximum from the values file |
| Dashboards | Six panels: step submissions by outcome, fallback rate per agent and version, runs by status, record writes and failures, refused links, worker backlog and refused reads |
| Alerts | Five rules: MSG-P7-003 on a record failure, a fallback-rate breach, a refused link, a `.dlt` record, a failed migration or an unhealthy route |
| Runbook | Six entries: record write failure, refused link, fallback rate breach, `.dlt` message, worker backlog, migration failure or route unavailable |

**Probes.** Readiness answers healthy only when the migration is at the expected schema version, the worker has polled, the relay is running and the last read of the reference lists and of the record read answered; liveness answers healthy when the process is up and its internal loop is responsive. Neither probe writes to the database.

**Migration job.** Runs the per-service Flyway sequence for schema `rwb_agent` with the service login as a pre-deploy job with a backoff limit; `V10_002__agent_run_decision_link.sql` applies after `V10_001__agent_runtime.sql`, a failed job blocks the rollout and the release, and the sequence is forward only (DP-15).

**Alert mapping carried over from the legacy story.**

| Message ID or check | Condition | Alert | Route |
|---|---|---|---|
| MSG-P7-003 | A record write fails and a step does not act | Record-failure alert with the step key, the agent and the business date | Platform on-call and RW-PLATADM, ticket |
| None (fallback rate) | The fallback rate of an agent and policy version is above the 10 percent target | Fallback-rate alert with the agent, the version and the rate | RW-RISK and RW-COE, no page |
| None (refused link) | A link is refused because the run holds another record | Refused-link alert with the run ID and both references | Data steward, ticket |
| None (record) | A record lands in `.dlt` | `.dlt` alert with the record reference and its registry subject | Platform on-call, page |
| None (backlog) | The worker backlog passes its threshold | Backlog alert on queue `rwb-agent` | Platform on-call, page |
| MSG-P4-002 | A read without the Platform administration right | Refused-read count on the dashboard | No page |

**Capacity.** The plan states, per environment, the step submissions of a peak business date, the share that falls back, the queue backlog trigger, the worker minimum and maximum, the connection cap of the login and the relay interval. The target is the legacy measure: an answer inside the 60 second policy budget with the rule result used on expiry, and a fallback rate below 10 percent per month (FSD P10 Agent runtime v3 A2.11.1). No Quartz job window and no lake window appear in the plan.

**Rollback.** The previous chart version is redeployed; the Flyway sequence is forward only, so the link column and its index stay and no down-migration is run; the publish right on `rwb.decision-record.v1` is left in place, because removing it would stop the record of every step of a calling service; the route is republished from the previous release; and no Schedule has to be re-registered, because this release holds none. A rollback is rehearsed in SIT before UAT.

**Done when.** The chart renders in all three environments, the pipeline promotes one artefact, the probes answer, the queue, the topic right and the bindings are verified by a test, KEDA scales on backlog, the four workflows and activities are registered, the five alerts fire on synthetic conditions including the record failure with MSG-P7-003, the route answers within 2 s, the capacity plan is reviewed, the rollback is rehearsed and the six runbook entries are accepted by the on-call rota.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | A record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A read without the Platform administration right | You cannot {action} here. Your role does not include it. |

The two texts are copied unchanged from RWB-TE-013; the deployment adds the alert routing and the runbook link, never a new wording. The fallback-rate, refused-link, `.dlt` and backlog conditions have no message ID in the legacy story and keep none.

##### 15. Screens and states

The deployment serves the run read and the two client operations of RWB-P10-TE013-APP through the gateway-bff pass-through route (DP-19). The operator-facing surfaces of this story are the pipeline run view, the release view, the dashboards and the runbook. The agent monitor screen SCR-46 belongs to RWB-E2-031 and the autonomy-level screen to Epic 3, and neither is changed here. The exact path of the route is Not specified in the source documents (GAP-0621; ASM-0915).

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-P10-TE013-OPS-01 | AC1, BR2 | NFR | Chart renders for DEV, SIT and UAT with a pinned digest, the login reference and the migration job of `V10_002__agent_run_decision_link.sql` after `V10_001__agent_runtime.sql`, creating no table |
| TC-P10-TE013-OPS-02 | AC2, BR3, BR4, BR5 | NFR | Backlog scales the worker, the build ID is on the version set, the four workflows and activities are registered, the publish right and the retry and `.dlt` bindings exist, and no topic or consumer group is created |
| TC-P10-TE013-OPS-03 | AC3, BR6 | NFR | The three lists and the record read come from the contracts, the policies carry OFF, SHADOW, L1 and timeout 60, the switch off starts no run, and every secret is a reference |
| TC-P10-TE013-OPS-04 | AC4, BR7, BR12 | NFR | Five synthetic conditions raise the mapped alerts, MSG-P7-003 on the record failure, the refused link with both references, the `.dlt` record, and one runbook entry each |
| TC-P10-TE013-OPS-05 | AC5, BR11 | End to end | Probes false before the migration, true after; the smoke step for case "RW-2026-000201" answers its outcome against the three fakes and the run is read through the route within 2 s |
| TC-P10-TE013-OPS-06 | AC6, BR1, BR10 | NFR | The six runbook entries walked, the rollback rehearsed with the schema forward only and the publish right kept, and the capacity plan figures stated |

The six test cases are this story's own (D-RCV-60) and test the deployment artefacts of the legacy criteria rather than the business outcomes, which are the app story's: the legacy ids TC-TE-013-01 to TC-TE-013-10 stay with RWB-P10-TE013-APP and are not copied here. The legacy Level "System" maps to NFR for a deployment check and to End to end where the smoke step and the route answer are proved.

##### 17. Guardrails

- No business value in a values file: the modes, the timeout, the agent codes, the check codes and the lists are contract and policy values, never deployment values (DP-07).
- No personal data in logs, dashboard series, alert payloads or the runbook: run counts, IDs, dates, codes and durations only.
- No other service's table is read and no grant crosses a schema: the login holds rights on `rwb_agent` only (DP-01, DP-02).
- The release takes the publish right on the shared decision-record topic and never creates a topic, a retry topic, a `.dlt` topic or a consumer group (DP-03, DP-09).
- The release pins the image digest and the chart version; a rebuild between environments is not allowed.
- No secret is written into a values file, a chart template, a dashboard or the runbook; all secrets come from the platform secret store.
- The release deploys no Quartz job table, no job admin read and no lake artefact, and the legacy dependence on RWB-TE-007 points to the workflow kit (§R6; DP-10).
- The run read is published only through the gateway-bff route, one hop, and a screen never reaches the service (DP-19).
- A record write failure is alerted with MSG-P7-003 and never repaired by writing a record from an agent run, because the record belongs to the step (DP-03).

##### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | The record write and its publish right, and the record-failure alert | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | The MSG-P7-003 alert, its runbook entry and the ticket | TC-P10-TE013-OPS-04 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | The `rwb_agent` login reference and the refused-read count | TC-P10-TE013-OPS-03, TC-P10-TE013-OPS-04 |
| D-RCV-60 DP-03 | Local decision record plus central ledger | The publish right on `rwb.decision-record.v1` and the boundary wiring of the record read | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-03 |
| D-RCV-60 DP-09 | Kafka with outbox, inbox and CloudEvents | The retry and `.dlt` bindings, the relay interval and the `.dlt` alert | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-04 |
| D-RCV-60 DP-10 | Temporal replaces Quartz | The worker registration on queue `rwb-agent`, KEDA and the absent Schedule and job table | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-06 |
| D-RCV-60 DP-15 | Per-service Flyway and migration ownership | The migration job and the forward-only rollback | TC-P10-TE013-OPS-01, TC-P10-TE013-OPS-06 |
| D-RCV-60 DP-19 | gateway-bff composite route | The route publication and the one-hop smoke read | TC-P10-TE013-OPS-05 |
| D-RCV-60 DP-20 | Agent client through the rwb-agent contract | The two client operations and the workflow the worker registers | TC-P10-TE013-OPS-02, TC-P10-TE013-OPS-05 |
| ADR-021 | Per-service Flyway and migration ownership | The migration job and the forward-only rollback | TC-P10-TE013-OPS-01, TC-P10-TE013-OPS-06 |
| ADR-023 | Observability per service | Six dashboard panels, five alerts and six runbook entries | TC-P10-TE013-OPS-04 |
| NFR-010 | An agent returns an answer inside its target, after which the rule result is used | The 60 second policy budget of the smoke step and the fallback-rate panel | TC-P10-TE013-OPS-05 |

The gap GAP-0621 records what the sources leave open for this release - the topology and sizing, the login and secret name, the alert thresholds and runbook wording, and the route path - and each default it raises is settled by ASM-0912 to ASM-0915.

##### 19. Out of scope

- The application code of the mode resolution, the timed run, the fallback, the record write and the link (RWB-P10-TE013-APP).
- The contract documents and the fakes as published artefacts (RWB-P10-TE013-CON); this story deploys the test copies only.
- The agent platform release, its schema baseline, its topic, its model gateway wiring and its own worker activities (RWB-P10-E1058-OPS and RWB-P10-E1058-APP).
- The platform topic provisioning, the Temporal cluster, the KEDA operator and the gateway-bff implementation (RWB-PLT-EVT, RWB-PLT-WF, RWB-PLT-EDGE and RWB-PLT-OBS).
- The record library, the record type, the central ledger and the record read (RWB-PLT-E1027-CON, RWB-P7-E1027-CON).
- The reference lists of rwb-case (RWB-P3-E1043-CON) and the embedded Drools kit (RWB-PLT-E1072-CON).
- The case steps that call the client, the screen field list of the agent monitor and the autonomy-level screen (RWB-E2-028, RWB-E2-029, RWB-E2-031, Epic 3).
- The exact deployment topology, the host, the SKU, the budget, the replica counts, the resource sizes, the topic partitions, the worker concurrency, the alert thresholds and the probe timings (GAP-0621).
- Any lake artefact, extract or Quartz job table, which DP-17 and §R6 remove (GAP-0621).
- The end-to-end run of the legacy criteria AC1 to AC8 across services (RWB-ITG-TE013-ITG).


### RWB-ITG-TE013-ITG Agent runtime client with fallback — integration

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: integration slice of RWB-TE-013 for RWB-ITG-W1. The in-process AgentOrchestrator becomes rwb-agent (P10) reached through AgentRunWorkflow on queue `rwb-agent` (DP-20), the decision log writer of P7 becomes the local decision record of the calling service collected into the rwb-decision ledger on `rwb.decision-record.v1` (DP-03), the base moves to `/api/recovery/<short>/v1` (DP-13) and the run and policy reads move to the P10 admin contract. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | RWB-ITG-TE013-ITG |
| Work type | ITG (Integration) |
| Suggested owner | TechX (suggested; any team may pick up this story) |
| Service | integration |
| Service epic | RWB-ITG-W1 |
| Wave | 1 |
| Business epic | EP01-TE |
| Release | 30 November 2026 (tentative) |
| Legacy key | RWB-TE-013 |
| Legacy disposition | Split (rework) |
| Build status | Not started |
| Patterns applied | DP01, DP03, DP04, DP07, DP09, DP10, DP11, DP13, DP15, DP19, DP20 |
| Parallel lane | L-ITG-W1 |
| Ready to start | Day 1 |
| Depends on (build) | None |
| Contract dependencies | None |
| Integration dependencies | RWB-P10-TE013-APP, RWB-P7-TE013-APP |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-014, FR-PLT-015) |
| Status | Draft (realignment v1) |

##### 1. Story

As a **tech lead**, I want **the agent runtime client of `recovery.agent.api` exercised on the real wave-1 services: a calling step in its own service building the rule result first, the client starting AgentRunWorkflow on queue `rwb-agent` inside the approved 60 second budget of the agent policy, the autonomy mode SHADOW, L1 or OFF deciding what is applied, the fallback to the rule result on TIMED_OUT, SCHEMA or NO_POLICY, and one decision record written in the calling service's own schema before the step acts and collected into the rwb-decision ledger on `rwb.decision-record.v1`**, so that **an agent is added to a case step without changing the case flow, the agent answer is never the applied result in SHADOW or L1, and the step does not act at all when its decision cannot be recorded**.

##### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The legacy client put every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001); if the entry cannot be written the step does not act (REQ-DRI-005). The measure is unchanged: the agent fallback rate, target below 10 percent per month.

In the target the client is still a published library inside each calling service (`recovery.agent.api`), but the orchestrator is a service of its own: rwb-agent (P10) owns agent policies, prompts, runs, guardrails and evaluations, runs AgentRunWorkflow with the 60 second budget and then the rule result, publishes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1`, and exposes its runs through `GET /api/recovery/agent/v1/admin/agent-runs` (Arch v5 slides 16, 41 and 42 row 28; DP-20). Its tools read case facts from rwb-source-data (P1) and extracted fields from rwb-document (P5) through their published contracts as read-only calls under SY-AGENT (Arch v5 slide 16; REQ-ACA-010). And the decision record no longer lives in one place: each service writes its own record in its own schema in the same transaction as its state change, and rwb-decision collects it into the central ledger (Arch v5 slides 20 and 28; DP-03, ADR-022).

Three of the facts that make the client trustworthy cannot be proved inside one service, and no single service story owns them:

- The rule-first order is a fact about two services: the calling service must hold the rule result of its own embedded rule package (DP-04) before rwb-agent is asked anything, and the applied result must stay that rule result in SHADOW and L1 while the agent answer appears on the run with agent version "INTAKE@P1/PR1" and confidence 0.91.
- The 60 second budget is a fact about the workflow: the budget belongs to AgentRunWorkflow on queue `rwb-agent` and to the approved policy, never to a caller's REST call, and the expiry must return the rule result to the step and the reason TIMED_OUT to the record (R-UNI-32).
- The record-before-action rule is a fact about three services: the local record commits or rolls back with the step's transaction, exactly one `rwb.decision-record.DecisionRecorded.v1` reaches the shared topic, and rwb-decision holds one ledger entry that a Decision log R holder can read back. A local write that fails must leave the case in "NEW", raise DecisionNotRecordedException with MSG-P7-003 and produce no event and no ledger entry (R-UNI-39).

This integration story is those three facts proved together on real services and real contracts, with the legacy values of RWB-TE-013 kept character for character (agent "INTAKE", policy "P1", prompt "PR1", case "RW-2026-000201", route state "NEW", rule R-UNI-32 version 2026.11, timeout 60 seconds, autonomy SHADOW, L1 and OFF, answer in 2,000 ms, confidence 0.91, fallback reasons TIMED_OUT, SCHEMA and NO_POLICY, step key CASEWF:RW-2026-000201:ENTRY:2026-11-30). The component copies are RWB-P10-TE013-APP (the agent runtime and its run contract) and RWB-P7-TE013-APP (the decision-record library and the ledger read); this story builds neither and proves both.

The only thing stubbed is the outside world: the enterprise model endpoint behind the rwb-agent gateway answers through a recorded stub with a clock and two fault switches, because no suite may call a live model endpoint and the 60 second expiry and the schema failure have to be reached deterministically. The five services in the path are the real SIT services on their published contracts.

##### 3. Preconditions

- The nine wave-1 services are deployed in SIT on their published contracts, each with its own schema and login: rwb_source_data, rwb_case, rwb_access, rwb_document, rwb_comms, rwb_decision, rwb_reporting, rwb_agent and rwb_integration (Arch v5 slide 41, wave 1).
- RWB-P10-TE013-APP is done: rwb-agent is deployed with schema `rwb_agent`, `agent_policy`, `agent_prompt` and `agent_run`, the tool gateway, the run read and the two configuration operations of section 12.2, and AgentRunWorkflow is registered on queue `rwb-agent` in namespace `rwb-recovery`.
- RWB-P7-TE013-APP is done: the decision-record library is published, the calling service holds `decision_record` in its own schema with the append-only rule, and rwb-decision holds `decision_log_entry` with its ingest and the `GET /api/recovery/decision/v1/decision-log/{entryId}` read.
- The topic `rwb.decision-record.v1` exists with its retry and `.dlt` topics, and `rwb.agent.events.v1` exists the same way (RWB-PLT-EVT).
- Agent "INTAKE" has approved policy "P1" with timeout 60 seconds, autonomy mode SHADOW, L1 and OFF reachable through the P10 configuration contract, and prompt "PR1" approved (RWB-P10-TE013-APP).
- The identity SY-AGENT exists with its read rights on case facts and extracted document fields, and rwb-access holds the test roles with their Platform administration R and Decision log letters, including RW-CASEOWN without Platform administration R (RWB-P4-E1037-APP).
- The synthetic case "RW-2026-000201" exists in rwb-case in route state "NEW" and status "New", with the facts the agent tools read (RWB-P3-E1018-APP, RWB-P1-E1001-APP).
- The calling steps of the run are the real write paths of rwb-case and rwb-document through the published client library `recovery.agent.api`, with an ArchUnit boundary test that a calling service imports only that package.
- The INT-23 stub of the enterprise model endpoint is deployed with its OpenAPI 3.1 document, its 2,000 ms answer, its clock and its two fault switches.
- The call type between the client and rwb-agent is **Not specified in the source documents (GAP-0381; ASM-0551)**: this story runs on ASM-0551, the client starts AgentRunWorkflow on queue `rwb-agent` through the P10 contract and reads the run back through `GET /api/recovery/agent/v1/admin/agent-runs`.
- The guardrail check codes used by the fallback are **Not specified in the source documents (GAP-0381; ASM-0552)**: this story treats the codes the agent returns as the fallback reasons, with "SCHEMA" and "TIMED_OUT" as the two the legacy story names.
- No build dependency: this story is Day 1 by rule (Template and Rules §R5.7). The harness is written on Day 1 against the two integration dependencies and is run when they are in SIT; a fake is never used in the place of a real service.
- The release date 30 November 2026 is tentative and is copied unchanged.

##### 4. Flow

1. Harness: runs the preflight against the OpenAPI documents of P10, P7, P4 and P3 and the AsyncAPI document of `rwb.agent.events.v1`, and fails before any assertion if a path, a field, a status code or an event schema has drifted, or if a fake is configured for any of the five services.
2. Harness: seeds case "RW-2026-000201" in route state "NEW" and status "New" through the W1J01 synthetic set, and confirms through `GET /api/recovery/case/v1/cases/{caseId}` that the route state is "NEW".
3. Calling step of rwb-case: evaluates its own rule package through the embedded kit and builds the rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE" (DP-04).
4. Calling step: calls `AgentStepClient.runStep` of `recovery.agent.api` with agent "INTAKE", the case ID, the decision code, step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30", the rule result and the masked inputs.
5. Client: reads the autonomy mode of the policy in force through the P10 configuration contract; on OFF or on a switched-off flag it skips the agent and returns the rule result with fallback false and agent version null.
6. Client: starts AgentRunWorkflow on queue `rwb-agent` with the step key as the workflow ID and the idempotency key, and waits at most the 60 seconds of the policy (ASM-0551).
7. rwb-agent: resolves the approved policy "P1" and prompt "PR1", runs its tool gateway read-only calls to rwb-source-data and rwb-document as SY-AGENT, calls the model endpoint through its gateway, checks the answer, records one run row with agent version "INTAKE@P1/PR1" and publishes `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` in the same transaction (DP-09).
8. Client: in SHADOW it keeps the rule result as the applied result and records the answer on the run only; in L1 it keeps the rule result as the applied result and returns the checked answer with confidence 0.91 as the recommendation for the person who decides.
9. Client: on the 60 second expiry, on a failed guardrail check or on no approved policy, it keeps the rule result and marks the fallback true with reason TIMED_OUT, SCHEMA or NO_POLICY (R-UNI-32).
10. Client: writes one decision record through the decision-record library of RWB-P7-TE013-APP in the calling service's own schema, in the same transaction as the step's state change, with the rule ID and version, agent version "INTAKE@P1/PR1", model version, the recommendation, and actions holding the agent run ID, the mode, fallback and the fallback reason (DP-03).
11. Calling service: the outbox relay publishes exactly one `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`, keyed caseId; rwb-decision ingests it into `decision_log_entry` in rwb_decision within 5 minutes (Arch v5 slides 20 and 28).
12. Harness: reads the run through `GET /api/recovery/agent/v1/admin/agent-runs` as a Platform administration R holder, and the record through `GET /api/recovery/decision/v1/decision-log/{entryId}` as a Decision log R holder, and reconciles one run, one event and one entry per step key (R-UNI-40).
13. Harness: forces the local decision-record append to fail inside the step's transaction, confirms that the state change rolls back, that case "RW-2026-000201" stays in "NEW", that DecisionNotRecordedException carries MSG-P7-003, and that no event and no ledger entry exist (R-UNI-39).
14. Harness: repeats the same step key, and confirms one agent run, one decision record and one ledger entry, with the first outcome returned (R-UNI-40).
15. Harness: calls the run read as RW-CASEOWN, confirms the refusal comes from rwb-access through `POST /api/recovery/access/v1/authorise` and answers 403 with MSG-P4-002, cleans up the synthetic set and writes the run report.

##### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent does not answer within 60 seconds | The run ends TIMED_OUT, fallback true, the rule result is applied and the step continues to "RESUME_STATE" | None to a user | AC2 |
| X2 | The answer fails a guardrail check | The rule result is applied, fallback true with the check code the agent returns, for example "SCHEMA" | None to a user | AC4 |
| X3 | No approved policy exists for the agent on the business date | No agent call and no run row; the rule result is applied with fallback true and reason "NO_POLICY" | None to a user | AC5 |
| X4 | The decision record write fails | The step does not act, the case stays in "NEW", no event reaches the topic and no ledger entry exists; an incident is raised | MSG-P7-003 | AC3 |
| X5 | The same step key arrives twice | One agent run, one decision record and one ledger entry; the repeat returns the first outcome | None to a user | AC1 |
| X6 | The autonomy mode is OFF or the flag `rwb.agent.client` is off | No agent call and no run row; the rule result is applied with fallback false and agent version null | None to a user | AC5 |
| X7 | A role without Platform administration R reads agent runs | rwb-access refuses the authorise call and the read answers 403 | MSG-P4-002 | AC5 |
| X8 | A consumed contract drifts from the published one | The preflight fails on the contract test and the run stops before any assertion; the drift is reported against the owning service and no fake is put in its place | None | Preflight, AC1 |

X1 to X7 are the exception paths of the legacy story carried onto the real services, with the decision log entry renamed as the decision record of the calling service; X8 is the failure that only appears when the run leaves one service.

##### 6. INVEST check

| Test | Result |
|---|---|
| Independent | The harness is a test module of its own; it needs rwb-agent, rwb-decision and the published contracts of P4 and P3, not their source code, and it owns no schema and no table |
| Negotiable | Fixture size, wait intervals, poll intervals and report layout are configuration; the agent, the policy and prompt versions, the case, the rule and its version, the timeout, the modes, the confidence, the fallback reasons and the message IDs are fixed by the legacy story |
| Valuable | Proves across services what no single service story can prove: rule first, the workflow budget, the applied result in SHADOW and L1, three fallbacks, the local record with its event, the ledger entry and the record-before-action rule |
| Estimable | One harness module, six test classes, four fixtures, one fault switch pair, one transaction-failure step and one report |
| Small | Fits one sprint with the report |
| Testable | Every criterion is asserted on an observable: a response, an event, a run row, a ledger entry, a workflow status, a case state or a message ID |

##### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback, proven across the calling service, rwb-agent and rwb-decision

  Background:
    Given the SIT environment runs rwb-agent (P10), rwb-decision (P7), rwb-access (P4) and the wave-1 calling services on their published contracts
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New" in rwb-case
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"
    Given the published client library recovery.agent.api is the only agent package a calling service imports

  Scenario: AC1 The client starts AgentRunWorkflow and SHADOW keeps the rule result applied (new, D-RCV-60)
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the calling step calls the client with step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    Then AgentRunWorkflow runs on queue "rwb-agent" with the 60 second budget of policy "P1" and the step key as its workflow ID
    Then the agent answers in 2,000 ms and the run holds agent version "INTAKE@P1/PR1" and confidence 0.91
    Then the client returns the rule result as the applied result, with no agent output to the step, and fallback false
    Then GET /api/recovery/agent/v1/admin/agent-runs shows one run for case "RW-2026-000201" with fallback false, read as a Platform administration R holder
    Then no REST call from the calling service to rwb-agent exists in the trace of the step
    When the same step key is presented again
    Then one agent run and one decision record exist for the key and the repeat returns the first outcome (R-UNI-40)

  Scenario: AC2 The 60 second budget expires and the rule result is applied with TIMED_OUT (new, D-RCV-60)
    Given the agent does not answer within 60 seconds
    When the step runs
    Then the run ends at 60,000 ms with status "TIMED_OUT" and fallback true
    Then the client returns the rule result and the step continues to "RESUME_STATE"
    Then the decision record holds actions fallback true, reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then GET /api/recovery/agent/v1/admin/agent-runs shows the same run with status "TIMED_OUT" and fallback true
    Then case "RW-2026-000201" is no longer in route state "NEW" and the step's own state change is the only cause

  Scenario: AC3 One decision record is written before the step acts and collected into the ledger (new, D-RCV-60)
    Given the calling service holds its decision record in its own schema table decision_record, append only
    When the client returns the applied result
    Then the state change of the step, its decision_record row and its outbox row commit in one transaction in the calling service's schema
    Then exactly one rwb.decision-record.DecisionRecorded.v1 event is on rwb.decision-record.v1, keyed caseId
    Then rwb-decision ingests it and decision_log_entry in rwb_decision holds one entry for step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30"
    When a Decision log R holder reads GET /api/recovery/decision/v1/decision-log/{entryId}
    Then the entry holds rule "R-UNI-32" version "2026.11", agent version "INTAKE@P1/PR1" and finalCall "RESUME_STATE"
    When the decision record append fails inside the transaction
    Then the state change rolls back, the step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then no DecisionRecorded event for that step is on the topic and the ledger holds no entry for the step key

  Scenario: AC4 L1 returns the answer as a recommendation and a guardrail failure falls back (new, D-RCV-60)
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers in 2,000 ms with confidence 0.91
    Then the rule result is the applied result and the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision record holds the agent answer in recommendation with confidence 0.91 and fallback false
    When another call of the client for case "RW-2026-000201" receives an answer that fails check "SCHEMA"
    Then the run holds status "GUARDRAIL_FAILED" with check code "SCHEMA" and fallback true
    Then the applied result stays the rule result and the decision record holds reason "SCHEMA"

  Scenario: AC5 OFF and NO_POLICY make no agent call, and a role without the right is refused (new, D-RCV-60)
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then the client makes no agent call and no agent run row exists for case "RW-2026-000201"
    Then the decision record holds agent version null and fallback false
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the client makes no agent call and applies the rule result with fallback true and reason "NO_POLICY"
    When synthetic user "RW-CASEOWN" calls GET /api/recovery/agent/v1/admin/agent-runs
    Then rwb-access refuses through POST /api/recovery/access/v1/authorise and the answer is 403 with MSG-P4-002
```

**Target reading.** The agent, the policy and prompt versions, the case, the rule and its version, the timeout, the three autonomy modes, the confidence, the fallback reasons and the step key are the legacy values of RWB-TE-013, copied character for character. The in-process `AgentOrchestrator` of the legacy section 12 becomes AgentRunWorkflow on queue `rwb-agent` behind the P10 contract (DP-20), so the client starts a workflow and reads the run back through `GET /api/recovery/agent/v1/admin/agent-runs` rather than calling a Java interface; how the client reaches the workflow and what it reads when the workflow outlives the 60 second budget are Not specified in the source documents (GAP-0381; ASM-0551). The legacy `DecisionLogWriter` of P7 becomes the local decision record of the calling service collected into the rwb-decision ledger (DP-03), so AC3 asserts both the local write and the ledger entry, and the link from the run to the record is held in the record's actions rather than written into `agent_run` by the caller (ASM-0552). The guardrail check codes the agent returns are the fallback reasons, because no source set lists them (ASM-0552).

##### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule result is computed before the agent is called and is always the applied result in SHADOW and L1 | Agent catalog autonomy levels; agent_policy.autonomy_mode; DP-04 |
| BR2 | If the agent does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the rule result is used and the fallback is recorded on the decision | R-UNI-32; NFR-010; AgentRunWorkflow |
| BR3 | A step acts only after its decision record is written, in the same transaction as its state change | Principle 5; R-UNI-39; CTL-06; DP-03 |
| BR4 | The decision record holds the rule ID, the rule version, the agent version as "<agent>@<policy>/<prompt>", the model version and the recommendation | REQ-DRI-001; decision_log_entry.agent_version |
| BR5 | The idempotency key of the agent run is the step key | R-UNI-40 |
| BR6 | The client runs under the identity of the calling service; rwb-agent runs its tools as SY-AGENT, read only | REQ-ACA-010; Arch v5 slide 16 |
| BR7 | The agent is reached only through AgentRunWorkflow on queue `rwb-agent` and the P10 contract; no calling service calls rwb-agent by REST inside a step, and no caller holds the model budget | Arch v5 slides 12, 16 and 41; DP-20; ASM-0551 |
| BR8 | The 60 second budget is the workflow budget of the agent run and never a REST budget of a caller; every REST call of the harness is one hop with a 2 s client budget | ADR-020; DP-11 |
| BR9 | The run and its fallback are read through `GET /api/recovery/agent/v1/admin/agent-runs`; a caller never reads `agent_run`, `agent_policy` or `decision_log_entry` in another service's schema | DP-01; DP-11 |
| BR10 | One local decision record per step, one `DecisionRecorded` on `rwb.decision-record.v1` and one ledger entry; the record is append only and a correction is a new record naming the one it corrects | DP-03; Arch v5 slides 20 and 28; ADR-022 |
| BR11 | No business value (mode, timeout, threshold, prompt version, fallback reason text) is written in code; the client and the harness read every one of them from the approved policy through the P10 contract | Principle 1; DT02; DP-07 |
| BR12 | The agent answer is never the applied result in SHADOW or L1, and the recommendation returned to a person carries the confidence the guardrail checked | Legacy BR1 and section 17; agent_policy.autonomy_mode |

##### 9. State transitions

None of its own for a case status: the client changes no case status, and the calling step moves the case on the applied result.

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | AGENT_UNAVAILABLE | The agent or the model does not answer inside the timeout (R-UNI-32) | RESUME_STATE, with the rule result applied |
| ANY_ACTIVE | DECISION_RECORD_WRITE_FAILED | The record cannot be written (R-UNI-39) | EXCEPTION_QUEUE, raised by the calling step |

The states the harness observes across the services:

| Item | States |
|---|---|
| Agent run (`agent_run`, rwb_agent) | ANSWERED, TIMED_OUT, GUARDRAIL_FAILED, BELOW_FLOOR, each with fallback true or false |
| AgentRunWorkflow | Running while the 60 second budget holds, Completed with an answer, Completed with the rule result |
| Local decision record (`decision_record`, calling service schema) | Appended with the step's transaction; committed or rolled back with it, never present alone |
| Shared topic | No event for the step, one `DecisionRecorded`, or a retried delivery that the consumer inbox ignores |
| Ledger (`decision_log_entry`, rwb_decision) | No entry, one ingested entry, or an entry appended under the chain |
| Step and case | Step not acted and case still "NEW", or step acted and case moved on the rule result |
| Harness run | Not started, preflight failed, running, passed, failed with the failing criterion named |

##### 10. Authority

| Who | What they may do in this story |
|---|---|
| Tech lead of this harness | Owns the module, the fixtures, the fault switches, the transaction-failure step and the run report |
| Calling service teams (rwb-case, rwb-document) | Own their step, their rule result, their local decision record and the publish of DecisionRecorded |
| rwb-agent owner (RWB-P10-TE013-APP) | Owns the policies, prompts, runs, guardrails, AgentRunWorkflow, the topic `rwb.agent.events.v1` and the run and configuration reads |
| rwb-decision owner (RWB-P7-TE013-APP) | Owns the decision-record library, the ledger, the ingest and the decision-log read |
| rwb-access owner | Owns the Platform administration R and Decision log R checks and the refusal with MSG-P4-002 |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks (Platform administration R) |
| RW-AUDIT, RW-COMPLY, RW-COE and every role holding Decision log R | Read the ledger entry of the step inside their scope |
| SY-CASEWF and the other calling identities | Call the client; write the local decision record through the library |
| SY-AGENT | Runs the agent and its read-only tool calls |
| No role | Reads a service schema directly, writes `agent_run` from outside rwb-agent, or takes production data into the run |

##### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | `recovery_case` (rwb_case) | id | Read through the P3 contract; seeded synthetically |
| DF-CAS-007 | `recovery_case` (rwb_case) | route_state | Read through the P3 contract, before and after the step |
| DF-REF-002 | `rule_row` (rwb_decision) | rule_id | Read from the rule result passed in by the calling step |
| DF-REF-003 | `rule_row` (rwb_decision) | rule_version | Read from the rule result passed in by the calling step |
| DF-DEC-001 to DF-DEC-018 | `decision_record` (calling service schema) | all fields | Write (append) by the calling service; read back through the P7 read |
| DF-DEC-001 to DF-DEC-018 | `decision_log_entry` (rwb_decision) | all fields | Written by rwb-decision on ingest; read through the P7 read |
| DF-AGT-008 | `agent_policy` (rwb_agent) | autonomy_mode | Read through the P10 contract |
| DF-AGT-012 | `agent_policy` (rwb_agent) | timeout_seconds | Read through the P10 contract |
| DF-AGT-021 | `agent_policy` (rwb_agent) | status | Read through the P10 contract |
| DF-AGT-022 | `agent_policy` (rwb_agent) | valid_from | Read through the P10 contract |
| DF-AGT-036 | `agent_run` (rwb_agent) | id | Read through the P10 run read |
| DF-AGT-045 | `agent_run` (rwb_agent) | idempotency_key | Read through the P10 run read |
| DF-AGT-046 | `agent_run` (rwb_agent) | status | Read through the P10 run read |
| DF-AGT-047 | `agent_run` (rwb_agent) | fallback | Read through the P10 run read |
| DF-AGT-058 | `agent_run` (rwb_agent) | decision_log_id | Read through the P10 run read; the caller writes the run ID into the record's actions instead (ASM-0552) |

Field IDs are those in the Logical Data Model and Data Dictionary and are copied from RWB-TE-013. `agent_policy` and `agent_run` are the P10 tables of schema `rwb_agent`; `decision_log_entry` is the P7 ledger of schema `rwb_decision`; `decision_record` is the append-only local record that every calling service holds in its own schema (DP-03). The harness owns no field and no table: it reads through the operations of section 12 and writes only through the calling services' own write paths, with synthetic values.

The fallback reasons are **Not specified in the source documents (GAP-0381; ASM-0552)** beyond the three the legacy story names ("TIMED_OUT", "SCHEMA", "NO_POLICY"); the harness asserts those three and treats any other guardrail code the agent returns as the reason, without inventing one.

##### 12. Contract

###### 12.1 REST operations provided

None. The harness is a test module and provides no REST operation. The reserved names of P2 rwb-integration — base `/api/recovery/integration/v1`, topic `rwb.integration.events.v1`, queue `rwb-integration`, schema `rwb_integration` — are not used by this story.

###### 12.2 REST operations consumed

| Method | Path | Owner | Use |
|---|---|---|---|
| GET | `/api/recovery/agent/v1/admin/agent-runs` | P10 rwb-agent | AC1, AC2, AC5: the run listing of case "RW-2026-000201" with status, fallback, agentVersion and idempotency key, and the refusal of RW-CASEOWN |
| GET | `/api/recovery/agent/v1/admin/agent-configs` | P10 rwb-agent | AC1, AC4, AC5: policy "P1" and prompt "PR1" in force, the autonomy mode and the 60 second timeout, and the absence of an approved policy on 2026-11-30 |
| POST | `/api/recovery/access/v1/authorise` | P4 rwb-access | AC5: the Platform administration R check behind the run read, and its refusal |
| GET | `/api/recovery/decision/v1/decision-log/{entryId}` | P7 rwb-decision | AC3: the ledger entry of the step, read as a Decision log R holder |
| GET | `/api/recovery/case/v1/cases/{caseId}` | P3 rwb-case | AC2, AC3: route state "NEW" of case "RW-2026-000201" before the step and after the rollback |

Every call is one hop to the owning service on its own base (DP-11, DP-13) with the 2 s client budget. The 60 second budget is not a REST budget: it belongs to AgentRunWorkflow and to policy "P1" (BR8).

###### 12.3 Events published

None. The harness publishes no business event. Every event asserted in this story is produced by a calling service or by rwb-agent and is listed in 12.4.

###### 12.4 Events consumed

| Event | Topic | Owner | What the harness asserts |
|---|---|---|---|
| `rwb.agent.AgentRunCompleted.v1` | `rwb.agent.events.v1` | P10 rwb-agent | Exactly one event per run, written to the outbox in the same transaction as the run row; run ID, agent "INTAKE", the case ID, status "ANSWERED", "TIMED_OUT" or "GUARDRAIL_FAILED", fallback and agent version "INTAKE@P1/PR1"; CloudEvents 1.0, key caseId, no personal field |
| `rwb.decision-record.DecisionRecorded.v1` | `rwb.decision-record.v1` | Produced by the calling service; ledger owned by P7 rwb-decision | Exactly one event per step, keyed caseId, written to the outbox in the same transaction as the local record; carries the rule ID and version, agent version "INTAKE@P1/PR1", the mode, fallback and reason in actions, and no personal field |

A consumer dedupes on the event ID through its inbox `processed_event` (DP-09, ADR-015). The payload of the shared decision-record event is the contract of RWB-P7-TE013-APP; where a field is missing from the source set the harness asserts the envelope and the fields of 11 and 12.4 only (GAP-0381). The client's own route to the agent and its read of the run after the 60 second budget are Not specified in the source documents (GAP-0381; ASM-0551).

###### 12.5 Workflows and activities

| Name | Type | Task queue | Contract element |
|---|---|---|---|
| AgentRunWorkflow | Workflow (started by the client, P10) | `rwb-agent` | One run: resolve the approved policy and prompt, run the read-only tool calls, mask, call the model gateway with the 60 s budget, check the answer, record the run row and its outbox event; on expiry it ends and hands the rule result back (Arch v5 slide 16: "AgentRunWorkflow: 60 s, then rule result"; DP-10; DP-20) |
| Decision-record ingest of rwb-decision | Activity (observed, P7) | `rwb-decision` | Appends the record of the calling service to `decision_log_entry` within 5 minutes; owned by RWB-P7-TE013-APP and observed here through the decision-log read |

The harness starts no workflow of its own: the calling step reaches AgentRunWorkflow through the client of the platform contract, and the harness observes it through the Temporal visibility query with the step key as workflow ID (ASM-0551). The tool calls and the gateway call are activities of rwb-agent and are asserted through the run row and the event, never started by the harness.

###### 12.6 Schedules

None. No Temporal Schedule belongs to this story. The step that calls the client is started by the case flow, not on a cadence, so the harness triggers nothing on a schedule and registers none.

###### 12.7 Tables owned

None. The harness owns no table and never reads a service schema (DP-01). It exercises `agent_policy`, `agent_run` and `agent_prompt` of `rwb_agent` (owner P10), `decision_record` of the calling service's schema (owner that service, library of P7), and `decision_log_entry` of `rwb_decision` (owner P7), every one of them through a contract of section 12.

###### 12.8 Contract fakes

None for the nineteen services: rwb-agent, rwb-decision, rwb-access and rwb-case are the real SIT services on their published contracts, and a run configured with a fake for any of them fails the preflight. The only stub is outside the services:

| Stub | Purpose |
|---|---|
| INT-23 stub of the enterprise model endpoint, with its OpenAPI 3.1 contract | Stands in for the live endpoint behind the rwb-agent gateway; returns the 2,000 ms answer with confidence 0.91 for AC1, AC3 and AC4 |
| Clock | Holds the business date at 2026-11-30 for AC1, AC3 and AC5 and moves the call across the policy validity for AC5 |
| Fault switch: timeout | Makes the stub silent for 61 seconds, so the workflow budget of 60 seconds expires, for AC2 |
| Fault switch: schema | Returns an answer that fails check "SCHEMA", for AC4 |

The policy states are reached through the P10 configuration contract, never through a stub: the OFF and L1 modes are approved policy versions, and the NO_POLICY branch is reached by retiring the approved policy so that none is in force on 2026-11-30.

###### 12.9 Call-type summary

| Call type | Provided | Consumed | Notes |
|---|---|---|---|
| REST | 0 | 5 | The two P10 reads, the P4 authorise call, the P7 decision-log read and the P3 case read; one hop, 2 s (DP-11, DP-13) |
| Kafka | None | 2 event types | `rwb.agent.AgentRunCompleted.v1` on `rwb.agent.events.v1` and `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`; CloudEvents 1.0, key caseId (DP-09, DP-14) |
| Temporal | None | 1 workflow started, 1 activity observed | AgentRunWorkflow on queue `rwb-agent` in namespace `rwb-recovery`; the P7 ingest activity observed through the ledger |
| File | None | None | No file in this story |

##### 13. Solution plan

**Deliverables.** One harness module `integration/recovery-w1/agent-client`, with the six test classes `ClientContractIT`, `RuleFirstShadowIT`, `TimeoutFallbackIT`, `DecisionRecordIT`, `ModeAndGuardrailIT` and `AccessRefusalIT`, the fixture files, the fault switches and the run report writer. No service code and no schema change: the module builds nothing that a service owns.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| HarnessRunner | Runner | Preflight against the four OpenAPI documents and the AsyncAPI document, run order, report and exit code |
| PolicyFixture | Service | Loads and approves policy "P1" with timeout 60 seconds and prompt "PR1", sets the modes SHADOW, L1 and OFF, and retires the policy for the NO_POLICY branch, all through the P10 contract |
| CallerDriver | Service | Drives the real write path of rwb-case and rwb-document through `recovery.agent.api`, with the step key and the rule result of the fixture |
| WorkflowProbe | Service | Reads AgentRunWorkflow on queue `rwb-agent` through the visibility query and asserts the workflow ID, the 60 second budget, the status and the rule result handed back |
| RunProbe | Service | Reads the run through `GET /admin/agent-runs` and asserts status, fallback, agent version, confidence and the idempotency key |
| EventProbe | Service | Consumes `rwb.agent.events.v1` and `rwb.decision-record.v1` and asserts one event per run and per step, the outbox fact, the envelope and the absence of a personal field |
| RecordProbe | Service | Reads the ledger entry through `GET /api/recovery/decision/v1/decision-log/{entryId}` and compares the rule, the version, the agent version, the actions and the final call |
| TransactionFailureTool | Service | Forces the local append of `decision_record` to fail inside the step's transaction, then confirms the rollback and the refused state change |
| AccessProbe | Service | Calls the run read as RW-CASEOWN after the P4 authorise call and asserts 403 with MSG-P4-002 |
| ModelStubControl | Service | Deploys the INT-23 stub from its OpenAPI 3.1 document, sets the 2,000 ms answer, the clock and the two fault switches |
| ReportWriter | Service | One row per test case, with the evidence and the elapsed times |

**Database.** None of its own. The harness writes only through the calling services' own write paths, and its single direct write is the DEV-only transaction failure of AC3, which is refused outside DEV and SIT.

**Configuration and reference data**

- The SIT endpoints of P10, P7, P4 and P3, the topics `rwb.agent.events.v1` and `rwb.decision-record.v1`, queue `rwb-agent` and namespace `rwb-recovery`, all as configuration.
- The agent "INTAKE", the policy "P1", the prompt "PR1", the timeout 60 seconds, the confidence 0.91, the answer 2,000 ms, the three autonomy modes, case "RW-2026-000201", rule "R-UNI-32" version "2026.11", the step key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" and the business date 2026-11-30, read through the P10 contract and never written in the harness code (BR11).
- The decision codes and the reference values the fixtures use, read through the rwb-case reference-data contract (DP-07).
- The 2 s client budget, the 60 s workflow budget, the 5 minute ledger catch-up and the poll interval.

**Pattern application**

| DP | Legacy marker | Microservice pattern | Dependency added |
|---|---|---|---|
| DP-01 | `recovery.<table>` or "recovery schema" | Owner's schema `rwb_<name>`; never read another service's tables | none |
| DP-03 | DecisionLogWriter, decision log | Local decision-record library and topic `rwb.decision-record.v1` | H RWB-PLT-E1027-CON |
| DP-04 | RuleEvaluator, Drools | Embedded Drools kit; rule packages from rwb-decision | H RWB-PLT-E1072-CON; C RWB-P7-E1073-CON |
| DP-07 | Reference data, LOV | Reference-data contract of rwb-case | H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON |
| DP-09 | Application event, EV-nn, outbox | Outbox and inbox library; Kafka topic of the owner; CloudEvents | H RWB-PLT-TE006-CON |
| DP-10 | Quartz, JOB-nn | Temporal Schedule or event-started workflow through the workflow kit | H RWB-PLT-E1071-CON |
| DP-11 | In-process call, published interface | REST contract with mock; one hop; 2 s timeout | none (C from the legacy dependency) |
| DP-13 | `/api/recovery/v1` | `/api/recovery/<short>/v1` | none |
| DP-15 | V0001 baseline, migration | Per-service Flyway sequence in the service's own schema | H RWB-PLT-E1044-CON |
| DP-19 | Screen, ace-web | gateway-bff composite route | H RWB-PLT-N001-CON |
| DP-20 | Agent client | rwb-agent contract | C RWB-P10-TE013-CON |

The H/C/X dependencies the DPs name (notably DP-20 C RWB-P10-TE013-CON, DP-03, DP-04, DP-09, DP-10) stay with the service and platform stories this harness proves; this story carries no H, C or X dependency and its I list names the two stories whose behaviour it exercises (§R5.4).

**Fixtures**

| Fixture | Content | Used by |
|---|---|---|
| Policy set | Policy "P1" of agent "INTAKE" with timeout 60 seconds and prompt "PR1", approved in SHADOW, in L1 and in OFF, and retired for the NO_POLICY branch | AC1 to AC5 |
| Stub answers | The 2,000 ms answer with confidence 0.91, the 61 second silence and the answer that fails check "SCHEMA", held by ModelStubControl | AC1, AC2, AC4 |
| Synthetic case | Case "RW-2026-000201" in route state "NEW" and status "New", with a step that calls the client through the real write path of rwb-case and one through rwb-document | AC1 to AC5 |
| Rule result | Rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE", built by the calling step through the embedded kit | AC1 to AC5 |
| Role set | RW-PLATADM, RW-AUDIT and RW-COMPLY with Platform administration R, RW-COE with Decision log R, and RW-CASEOWN without Platform administration R | AC1, AC3, AC5 |

**Run order.** Preflight; policy and mode fixture; SHADOW run with the workflow and the run read (AC1); L1 and the guardrail failure (AC4); the timeout (AC2); the local record, its event and the ledger entry, then the forced transaction failure (AC3); OFF, NO_POLICY and the refused run read (AC5); cleanup of the synthetic case, the retired policy version and the stub. A failing step stops the run and the report names the criterion, the service and the evidence.

**Done when.** The fifteen test cases of section 16 pass on the real services in SIT, the five criteria of section 7 are signed off, AgentRunWorkflow is observed on queue `rwb-agent` with the 60 second budget, exactly one run, one event and one ledger entry exist per step key, the forced failure leaves case "RW-2026-000201" in "NEW" with MSG-P7-003, and the evidence report names every criterion with its observable.

##### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision record write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | A role without the right reads agent runs | You cannot {action} here. Your role does not include it. |

The two texts are copied unchanged from RWB-TE-013; this story adds no message ID. Report lines of the harness are for developers and are not part of the message standard.

##### 15. Screens and states

No screen in this story. A fallback shows in `GET /api/recovery/agent/v1/admin/agent-runs` (fallback true) and on the decision record of the case, which a Decision log R holder reads through the P7 read. The listing states the harness asserts are an empty result for a case with no run, a list of runs with id, agent, agentVersion, caseId, status, fallback and latency, and one run in each of the three statuses. The agent monitor screen SCR-46 and the autonomy-level screen come with RWB-E2-031 and Epic 3 and are out of scope; no gateway-bff composite route is exercised (DP-19).

##### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-01-ITG | legacy AC1, BR1, BR4 | Integration | Case RW-2026-000201, mode SHADOW, agent answers in 2,000 ms, agent version INTAKE@P1/PR1 |
| TC-TE-013-02-ITG | legacy AC2, BR2 | Integration | Agent silent for 61 seconds; run TIMED_OUT at 60,000 ms, fallback true, rule result applied |
| TC-TE-013-03-ITG | legacy AC3, BR1 | Integration | Mode L1, confidence 0.91, recommendation returned and recorded |
| TC-TE-013-04-ITG | legacy AC4 | Integration | Answer fails check SCHEMA; fallback true with reason SCHEMA |
| TC-TE-013-05-ITG | legacy AC5 | Integration | No approved policy on 2026-11-30; no agent call, reason NO_POLICY |
| TC-TE-013-06-ITG | legacy AC6, BR3 | Integration | Decision record write throws; step does not act; MSG-P7-003; no event and no entry |
| TC-TE-013-07-ITG | legacy AC7, BR5 | Integration | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice; one run and one record (R-UNI-40) |
| TC-TE-013-08-ITG | legacy AC8 | Integration | Mode OFF; no agent call, no run row, agent version null, fallback false |
| TC-TE-013-09-ITG | Access | Integration | RW-CASEOWN calls GET /admin/agent-runs; refused through P4 with MSG-P4-002 |
| TC-TE-013-10-ITG | Principle 5 | Integration | Decision record write forced to fail during a step in SHADOW mode; the step does not act; MSG-P7-003 |
| TC-ITG-TE013-01 | AC1, BR7, BR9 | End to end | One step in rwb-case through the client; AgentRunWorkflow observed on rwb-agent; one run read back; no direct REST from the caller |
| TC-ITG-TE013-02 | AC2, BR2, BR8 | End to end | Stub silent for 61 seconds; the workflow budget of 60 seconds expires; rule result applied; reason TIMED_OUT in the record |
| TC-ITG-TE013-03 | AC3, BR3, BR10 | Integration | One local decision_record row, one DecisionRecorded on rwb.decision-record.v1 and one ledger entry read through the P7 read; then the local append forced to fail |
| TC-ITG-TE013-04 | AC4, BR1, BR12 | Component | Mode L1 with confidence 0.91, then an answer failing check SCHEMA; applied result unchanged |
| TC-ITG-TE013-05 | AC5, BR5, BR6, BR11 | Contract | Mode OFF, no approved policy on 2026-11-30, and RW-CASEOWN refused with MSG-P4-002 |

The legacy acceptance criteria of RWB-TE-013 (AC1 to AC8 and the access and principle-5 checks of TC-TE-013-09 and TC-TE-013-10) are owned by RWB-P10-TE013-APP; RWB-P7-TE013-APP owns no legacy criterion of this key and carries the decision-record part of sections 11 and 12, and both are re-exercised here on the real services; the legacy test case IDs are kept as ITG copies with the suffix `-ITG` and their Covers cell names the legacy criterion and rule, and the five new criteria AC1 to AC5 carry TC-ITG-TE013-01 to TC-ITG-TE013-05.

##### 17. Guardrails

- No business value in code: the mode, the timeout, the prompt version, the confidence and the fallback reason text come from the approved policy through the P10 contract, and the decision codes from the rwb-case reference-data contract (DP-07).
- No personal data in events, workflow inputs, logs, fixtures or the report: case IDs, agent codes, version labels, rule IDs, step keys, statuses and codes only, and every case and identity of the run is synthetic.
- No cross-service table read: the run and the policy are read through the P10 contract, the ledger through the P7 read and the case state through the P3 read, and a pipeline scan fails any change that adds a schema connection (DP-01).
- The agent answer is never the applied result in SHADOW or L1 (BR12), and no caller holds the 60 second model budget as a REST budget (BR8).
- One decision record, one event and one ledger entry per step key: the local append is inside the caller's transaction and is the last statement before the step acts (BR3, BR10, R-UNI-39).
- The client is reached only through the published package `recovery.agent.api`, with an ArchUnit boundary test that a calling service imports nothing else of rwb-agent (DP-20).
- One hop and a 2 s client budget on every REST call of the harness; the harness calls no service through another service (ADR-020).
- No production access and no production namespace: the run is pinned to SIT with the synthetic set and refuses to start against any other environment; the transaction failure of AC3 runs in DEV and SIT only.

##### 18. Traceability

| Requirement ID | Requirement (short) | Contract element | Test cases |
|---|---|---|---|
| REQ-DRI-001 | Every decision records the rule, model, agent and prompt versions | `decision_record` in the calling service schema, `rwb.decision-record.DecisionRecorded.v1`, `decision_log_entry`, `GET /api/recovery/decision/v1/decision-log/{entryId}` | TC-TE-013-01-ITG, TC-TE-013-03-ITG, TC-ITG-TE013-03 |
| REQ-DRI-005 | No action proceeds if its decision record cannot be written | The append in the caller's transaction, DecisionNotRecordedException, MSG-P7-003 | TC-TE-013-06-ITG, TC-TE-013-10-ITG, TC-ITG-TE013-03 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | SY-AGENT tool path, `POST /api/recovery/access/v1/authorise`, MSG-P4-002 | TC-TE-013-05-ITG, TC-TE-013-07-ITG, TC-TE-013-08-ITG, TC-TE-013-09-ITG, TC-ITG-TE013-05 |
| DP-03 | Local decision record and the shared topic | `rwb.decision-record.v1`, the append-only local record, the ledger read | TC-TE-013-06-ITG, TC-ITG-TE013-03 |
| DP-04 | Embedded Drools kit and rule packages from rwb-decision | The rule result rule "R-UNI-32" version "2026.11" built before the client is called | TC-TE-013-01-ITG, TC-ITG-TE013-01 |
| DP-09 | Outbox, inbox and CloudEvents | One event per step and per run, key caseId | TC-ITG-TE013-01, TC-ITG-TE013-03 |
| DP-10 | Workflow kit and the task queue | AgentRunWorkflow on queue `rwb-agent` with the 60 second budget | TC-ITG-TE013-01, TC-ITG-TE013-02 |
| DP-11 | One hop and a 2 s timeout | The five calls of 12.2 and the preflight contract test | TC-TE-013-05-ITG, TC-ITG-TE013-05 |
| DP-13 | `/api/recovery/<short>/v1` | `/api/recovery/agent/v1`, `/api/recovery/decision/v1`, `/api/recovery/access/v1`, `/api/recovery/case/v1` | Every test case, at the preflight |
| DP-20 | Agent client through the rwb-agent contract | `recovery.agent.api` and AgentRunWorkflow on queue `rwb-agent` | TC-TE-013-01-ITG, TC-ITG-TE013-01, TC-ITG-TE013-02 |
| ASM-0551 | The client starts AgentRunWorkflow on queue `rwb-agent` through the P10 contract, treats the 60 s expiry as TIMED_OUT and reads the run and its fallback through the admin run read | AgentRunWorkflow and `GET /api/recovery/agent/v1/admin/agent-runs` | TC-ITG-TE013-01, TC-ITG-TE013-02 |
| ASM-0552 | The guardrail failure reasons are the codes the agent returns, and the link from the run to the record is held in the record's actions | The actions of the decision record and the run read | TC-TE-013-04-ITG, TC-ITG-TE013-04 |
| RWB-TE-013 (legacy story) | The client, the modes, the fallback and the record-before-action rule: AC1 to AC8 and the two checks | The five operations, the two events and the started workflow of section 12 | The fifteen test cases of section 16 |
| RWB-P10-TE013-APP (component copy) | The agent runtime of rwb-agent: policies, prompts, runs, guardrails and AgentRunWorkflow | The P10 contract and queue `rwb-agent` | TC-ITG-TE013-01, TC-ITG-TE013-02 |
| RWB-P7-TE013-APP (component copy) | The decision-record library, the local record, the ledger and its read | `decision_record`, `rwb.decision-record.v1`, `decision_log_entry`, the decision-log read | TC-ITG-TE013-03 |

##### 19. Out of scope

- The agent runtime, its tables, AgentRunWorkflow and the run and configuration reads (RWB-P10-TE013-APP), and its contract (RWB-P10-TE013-CON).
- The decision-record library, the local record, the ledger, the ingest and the decision-log read (RWB-P7-TE013-APP).
- The deployment, the topic provisioning and the queue registration (RWB-P10-TE013-OPS).
- The model endpoint and its gateway choice (DL33), the guardrail checker (RWB-E1-058 and RWB-ITG-E1058-ITG) and the masking path (RWB-E1-037).
- Agent answers acted on without a person: autonomy L2 and above (Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028) and deviation screening (RWB-E2-029); this story drives the step through the published library and owns none of it.
- The agent monitor screen SCR-46, the cost alert and the autonomy-level screen (RWB-E1-063, RWB-E2-031, Epic 3).
- Building the harness RWB-ITG-W1J01-ITG itself and the non-functional epic RWB-ITG-NFR.

