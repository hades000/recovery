<!-- source: 04 User stories/Recovery Workbench Technical Enabler Stories v5.md -->
<!-- converted: 2026-11-16 from Markdown (copied) -->

> **Source:** `04 User stories/Recovery Workbench Technical Enabler Stories v5.md`  
> **Converted from:** Markdown (copied)

# Recovery Workbench technical enabler stories

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Stories | 13 |
| Acceptance criteria | 55 |
| Test cases | 63 |
| Modules | P1 (1), P2 (7), P3 (2), P5 (1), P7 (1), P10 (1) |

Stories with no business user: interfaces, load frameworks and platform services the Epic 1 and Epic 2 stories build on.

Each story is written for build: the business rationale, preconditions, the main flow and its exception paths, acceptance criteria in Gherkin, business rules, state transitions, authority, the fields it reads and writes with their BR Field IDs, the contract, the solution plan, messages, screens, test cases and traceability to the business requirements. Field IDs are those in the Logical Data Model and Data Dictionary, endpoints those in the API Specification, messages those in the Error and Message Standard and requirement IDs those in the Business Requirements. The same stories are also supplied one file per story, to hand to a coding agent with the module specifications.

| Key | Title | Module | Requirements | Depends on |
|---|---|---|---|---|
| RWB-TE-001 | Recovery module folder and boundary test | P2 Integration | REQ-DRI-006 | None |
| RWB-TE-002 | Code owners for the recovery module | P2 Integration | REQ-DRI-006 | RWB-TE-001 |
| RWB-TE-003 | Types and contract tests from the API specification | P2 Integration | REQ-DRI-007, REQ-ACA-003 | RWB-TE-001 |
| RWB-TE-004 | Masked data in SIT and UAT | P1 Recovery data engine | REQ-RDF-010, REQ-ACA-005 | RWB-E1-065 |
| RWB-TE-005 | Rule table test harness | P3 Case and workflow | REQ-CWC-014, REQ-CWC-013 | RWB-E1-044 |
| RWB-TE-006 | Outbox and retry for outbound work | P2 Integration | REQ-DRI-007 | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| RWB-TE-007 | Scheduled jobs on Quartz | P3 Case and workflow | REQ-CWC-007, REQ-CWC-011, REQ-RDF-007 | RWB-E1-044, RWB-E1-056 |
| RWB-TE-008 | Decision log hash chain check | P7 Decision center and log | REQ-DRI-003 | RWB-E1-008, RWB-TE-007 |
| RWB-TE-009 | Performance test harness | P2 Integration | REQ-OCC-007, REQ-WKM-002 | RWB-TE-004 |
| RWB-TE-010 | Browser and accessibility tests | P2 Integration | REQ-OCC-007, REQ-WKM-001 | RWB-TE-003 |
| RWB-TE-011 | PDPA lint for code, tests and logs | P2 Integration | REQ-RDF-010, REQ-ACA-005 | RWB-TE-001 |
| RWB-TE-012 | Document storage containers | P5 Document hub | REQ-DCM-003, REQ-DCM-002 | RWB-TE-001 |
| RWB-TE-013 | Agent runtime client with fallback | P10 Agent runtime | REQ-DRI-001, REQ-DRI-005, REQ-ACA-010 | RWB-TE-007, RWB-E1-058, RWB-E1-027 |

---

## RWB-TE-001 Recovery module folder and boundary test

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

### 1. Story

As a **squad member (RW-TRIBE)**, I want **the recovery module folder and packages in the ACE repository with a build-time boundary test**, so that **no module calls the inside of another module and no recovery code calls a system of record directly**.

### 2. Business rationale

Three teams build in one ACE service. Without a checked boundary, a change in one team's code breaks another's, and a direct call to a core system could bypass the COLLINS and file load path. The skeleton gives each Workbench module one package with a published part and an internal part, and a test in every build refuses a call into another module's internal part, a cross-module table read and a direct system call outside the integration adapters. It meets REQ-DRI-006 and applies DT08, ADR-002 and DL05 (option B from 2 November: TechX creates the recovery module in its own package). The measure is the count of boundary violations merged to main, which must stay at zero.

### 3. Preconditions

- Access to the ACE repository for the TechX squads (DL36).
- DL05 is applied as option B from 2 November 2026: TechX creates the recovery module in its own package; the ACE team applies the module boundaries for the common and collection modules later.
- The common module's published packages are named in the module map. Until the ACE team names them, the map lists `..common.api..` (assumed; DL05).
- The ACE build runs the unit test phase on every pull request.

### 4. Flow

1. Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.
2. Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.
3. Squad member: writes RecoveryBoundaryTest with the rules BR1 to BR5, reading the module map.
4. Squad member: writes the front end boundary rules for `src/modules/recovery`.
5. Squad member: wires the common module access check for `/api/recovery/v1/**` through RecoveryAccessGuard.
6. Pipeline: on each pull request runs the back end tests, including RecoveryBoundaryTest, and the front end dependency check.
7. Pipeline: fails the build when a rule is broken and prints the rule, the class and the class it depends on.
8. Squad member: fixes the call by going through the other module's `api` package or an application event, and the build passes.

### 5. Exception paths

None.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only repository access; every later story builds inside these folders |
| Negotiable | Module names and published packages are in the module map file, not in the test code |
| Valuable | The three teams can change their own module without breaking another |
| Estimable | Folders, one map file, one ArchUnit test class, one front end rule file |
| Small | Fits in one sprint with its tests |
| Testable | Each rule has a test fixture class that breaks it |

### 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | boundary rule BND-1: recovery classes depend on the collection module only through its published packages | DT08; ADR-002 |
| BR2 | boundary rule BND-2: recovery classes depend on the common module only through its published packages | DT07; DT08 |
| BR3 | boundary rule BND-3: a recovery module depends on another recovery module only through a package the module map lists as published for it, or an application event | Settled architecture; ADR-002 |
| BR4 | boundary rule BND-4: entities and repositories of a module are used only inside that module | Settled architecture: a module reads only its own tables |
| BR5 | boundary rule BND-5: only the packages the module map allows for client libraries use HTTP, SFTP or file transfer clients: `recovery.integration.adapter` (RWB-E1-007) for files, and the agent runtime client for the enterprise model endpoint INT-23 (RWB-TE-013); no recovery class calls a system of record | REQ-DRI-006; ADR-005 |
| BR6 | Module names, packages and published packages are read from the module map file, not written in the test | Principle 1 applied to build configuration |

The R-BND codes are the names of the boundary test rules in this story. They are not routing rules.

### 9. State transitions

None. This story does not change a case status. It changes the build result of a pull request from passed to failed when a rule is broken.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Create the folders, the module map and the boundary test |
| TechX tech leads (code owners, RWB-TE-002) | Approve a change to the module map or to the boundary rules |
| ACE team | Names the common and collection published packages (DL05) |
| RW-PLATADM, platform administrator | Runs the pipeline |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

No business field is read or written. The boundary test reads source and compiled classes only.

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

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

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A boundary rule is broken | Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event. |
| Build log | A package is not in the module map | package {package} is not in the module map |
| MSG-P4-002 | A role without the right calls a recovery endpoint | You cannot {action} here. Your role does not include it. |

Build log text is for developers and is not part of the message standard.

### 15. Screens and states

No screen in this story. A developer reads the result in the pull request checks and the build log.

### 16. Test cases

None.

### 17. Guardrails

- No business value in code; module names and packages are in the module map.
- No personal data in logs, tests or prompts; fixtures hold class names only.
- No read of another module's tables; this story builds the check that enforces it.
- The breaking fixtures stay in `src/test` and never ship.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 5.2 and section 7 | None | All recovery processes | None | None |

### 19. Out of scope

- Code owners for the recovery folders: RWB-TE-002.
- Types and contract tests from the API specification: RWB-TE-003.
- Boundaries inside the common and collection modules: the ACE team under DL05 option A.
- The integration adapter pattern itself: RWB-E1-007.


---

## RWB-TE-002 Code owners for the recovery module

| Item | Value |
|---|---|
| Story key | RWB-TE-002 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-006 |
| BRD section | Business Requirements Program, section 7 (constraints Built on ACE and Modular monolith) |
| L3 process | All recovery processes |
| Decision | DL37 |
| Priority | Must |
| Depends on | RWB-TE-001 |
| Status | Ready for build |

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.

### 2. Business rationale

The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.

### 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the module map exist.
- The repository host supports a code owners file (GitHub format assumed, as ACE uses GitHub Copilot under DL32).
- The teams exist in the repository host: TechX recovery tech leads and the ACE team. Names assumed until DL37 and DL36 are answered: `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`.
- The repository administrator of the ACE team can set the branch rule on main.

### 4. Flow

1. Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.
2. Squad member: adds the code owners validation step to the pull request pipeline.
3. ACE team repository administrator: sets the branch rule on main: one approval from a code owner required, stale approvals dismissed on a new commit.
4. Developer: opens a pull request that changes a recovery folder.
5. Repository host: requests review from the owning team named for each changed path.
6. Pipeline: runs the validation step; an owner that does not exist or a path that matches no file fails the check.
7. Code owner: approves; the merge is allowed once every owning team of the changed paths has approved.

### 5. Exception paths

None.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the folders from RWB-TE-001 |
| Negotiable | Team names are values in one file (DL37) |
| Valuable | No change to the recovery or common module merges without its owner |
| Estimable | One file, one pipeline step, one branch rule |
| Small | 1 point |
| Testable | Each criterion below is a pull request in a test branch |

### 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every path under the recovery back end, test and migration folders is owned by the TechX recovery tech leads | DL04 option A; DL37 |
| BR2 | The recovery front end folder and the module map file are owned by the TechX recovery tech leads | ADR-006; DL07 |
| BR3 | The common module folder is owned by the ACE team | DL04 option A; DT07 |
| BR4 | The code owners file itself is owned by both teams | DL04 |
| BR5 | The last matching pattern in the file decides the owner, so specific paths come after general ones | Repository host rule |
| BR6 | A merge to main needs one approval from a code owner of every changed path; an author's own approval does not count; a new commit dismisses approvals | ADR-008; DT11 |
| BR7 | Team names are values in the file; a change of team is a change to the file, reviewed by both teams | DL37 |

### 9. State transitions

None. This story does not change a case status. It sets the review state of a pull request: review required, approved, or dismissed on a new commit.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX recovery tech leads | Approve changes to recovery folders and the module map |
| ACE team | Approves changes to the common module and the code owners file; sets the branch rule on main |
| RW-TRIBE, tribe lead and squad members | Open pull requests; cannot satisfy a code owner review unless in the owning team |
| No Workbench capability area applies | Access is a repository right, not a Workbench role right |

### 11. Data

No business field is read or written.

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

| Item | Value |
|---|---|
| File | `.github/CODEOWNERS` at the repository root |
| Entries | `/ace-service/src/main/java/**/common/ @scb-ace/ace-team`; `/ace-service/src/main/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/test/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/main/resources/db/migration/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-web/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads`; `/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads`; `/.github/CODEOWNERS @scb-ace/ace-team @scb-ace/techx-recovery-tech-leads` |
| Branch rule on main | Require a pull request; require review from code owners; 1 approval; dismiss stale approvals; the author's approval does not count |
| Pipeline step | Code owners validation: syntax, every owner exists and has write access, every pattern matches at least one file |
| Trigger | Every pull request that changes any file |
| Idempotency | The same file and the same changed paths always request the same owners |

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Repository host | A code owner review is missing | Review required from code owners |
| Build log | An owner in the file does not exist | owner {team} not found |

No Workbench message applies; these texts come from the repository host and the pipeline.

### 15. Screens and states

No screen in this story. A developer reads the required reviewers and the merge state on the pull request page of the repository host.

### 16. Test cases

None.

### 17. Guardrails

- No business value in code; the file holds paths and team names only.
- No personal data in logs, tests or prompts; test pull requests change fixture files only.
- No read of another module's tables; the file is the review control for the boundary of RWB-TE-001.
- Team handles are teams, never single people, so absence of one person does not block a merge.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 7 | None | All recovery processes | None | None |

### 19. Out of scope

- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).


---

## RWB-TE-003 Types and contract tests from the API specification

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

### 1. Story

As a **squad member (RW-TRIBE)**, I want **server interfaces and front end types generated from the OpenAPI file, with a contract test and an access test per endpoint**, so that **the front end and the service never drift from the specification and no endpoint skips its access check**.

### 2. Business rationale

The recovery API has 79 operations specified in one OpenAPI 3.1 file. When server code, front end code and the file are kept by hand, a field renamed on one side breaks a screen in SIT, and an endpoint can ship without the capability check its specification states. Generating both sides from the file and testing every implemented operation against it in each build stops both faults before merge. It meets REQ-DRI-007, where the FSD requires every interface to have a contract test (AC-P2-001-01), and REQ-ACA-003, because each endpoint is tested against the right its specification declares from the permission matrix. The measure is the count of contract defects found in SIT, with a target of zero.

### 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the boundary test exist; the generated packages are listed in the module map as shared.
- The API specification is held in the repository at `api/recovery-api.yaml`, base path /api/recovery/v1, with x-module, x-capability and x-first-release on every operation.
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

None.

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

None. The former criteria covered development and delivery procedures and have been removed from the story set.

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

### 12. Contract

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

### 13. Solution plan

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

None.

### 17. Guardrails

- No business value in code: capability areas and rights come from the specification and the permission matrix.
- No personal data in logs, tests or prompts; fixtures are synthetic and the test report holds operation names only.
- No read of another module's tables; each module's controller implements its own generated interface.
- Generated code is never edited; a change goes into the specification.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Adapters log, retry and follow one pattern with a contract test | Business Requirements Program, section 5.2 | None | All recovery processes | None | None |
| REQ-ACA-003 | The permission matrix is the only source of what a role may do | Business Requirements Program, section 5.4 | None | All recovery processes | None | None |

### 19. Out of scope

- Contract tests for file interfaces: RWB-E1-007.
- Browser tests on the screens that use the generated client: RWB-TE-010.
- The permission matrix content: RWB-E1-037.


---

## RWB-TE-004 Masked data in SIT and UAT

| Item | Value |
|---|---|
| Story key | RWB-TE-004 |
| Epic | E1, release 30 November 2026 |
| Module | P1 Recovery data engine |
| Feature | None |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Epic 1, section 4 (REQ-RDF-010, REQ-ACA-005); Business Requirements Program, section 6.7 (NFR-045) |
| L3 process | All recovery processes |
| Decision | DL26 |
| Priority | Must |
| Depends on | RWB-E1-065 |
| Status | Ready for build |

### 1. Story

As a **Tribe lead and squad member (RW-TRIBE)**, I want **masked copies of recovery data loaded into SIT and UAT from the PII service**, so that **tests run on realistic volumes without exposing customers**.

### 2. Business rationale

SIT and UAT must show that loads, allocation, reconciliation and reports work at production volume and with production data shapes, which synthetic data does not prove. NFR-045 allows masked copies in user acceptance and forbids production data in development. The bank's PII service produces the masked copy under the Compliance masking rules; this story loads it into SIT and UAT only, refuses any copy that still holds a personal value, and keeps balances, dates and keys unchanged so counts and reconciliations behave as in production. Serves REQ-RDF-010 and REQ-ACA-005; decision DL26 sets the masking rules.

### 3. Preconditions

- RWB-E1-065 is done: the generator's personal data pattern checks and the sys_fields is_personal tags are available to the loader.
- The PII service delivers a masked extract per environment to the SIT or UAT intake container, with a manifest: extract ID, business date, masking rule version, row count and balance totals per table.
- The masking rule version in force is held in the masking rules reference table (DL26; until Compliance supplies the rules, every is_personal field is replaced by a token).
- The SIT and UAT databases hold the recovery schema at the same Flyway version as the extract.
- The platform administrator (RW-PLATADM) starts the load; squad members hold RW-TRIBE.

### 4. Flow

1. PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT.
2. Platform administrator: starts the masked copy load in the pipeline for the target environment.
3. MaskedCopyLoader: refuses to run when the target environment is DEV or PROD.
4. MaskedCopyLoader: checks the manifest: extract ID not loaded before, masking rule version equal to the version in force, schema version equal to the target.
5. MaskedCopyLoader: runs the load checks of CTL-02 on each file: business date, structure, control totals (row count and balance sum), keys.
6. MaskingVerifier: scans every column tagged is_personal for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.
7. MaskedCopyLoader: loads the files into a staging schema, checks foreign keys resolve, and swaps the staging schema for the live one in one step.
8. MaskedCopyLoader: writes the load report: extract ID, business date, masking rule version, rows and balance totals per table, check results.
9. Squad member: runs SIT or UAT tests on the masked copy.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A personal column holds a value that looks personal | Load refused in full; previous copy stays | MSG-P1-002 | AC2 |
| X2 | Row count or balance total differs from the manifest | Load refused in full; previous copy stays | MSG-P1-002 | AC3 |
| X3 | The target environment is DEV or PROD | Load refused before reading any file | MSG-P1-002 | AC4 |
| X4 | The same extract ID is loaded again | Load skipped; report shows the earlier load | None | AC5 |
| X5 | The manifest's masking rule version is not the version in force | Load refused in full | MSG-P1-002 | AC6 |
| X6 | A second load starts while one runs | Second start refused | MSG-P2-006 | AC7 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the personal data checks from RWB-E1-065 and the PII service extract; no screen |
| Negotiable | Masking rules belong to Compliance (DL26); the story fixes the checks and the load |
| Valuable | SIT and UAT run at production volume with no customer data exposed |
| Estimable | One loader, one verifier, one pipeline stage |
| Small | Finished inside two weeks with its tests |
| Testable | Each criterion runs on a test extract with a manifest |

### 7. Acceptance criteria

```gherkin
Feature: Masked data in SIT and UAT

  Background:
    Given masking rule version "MASK-2026.11" is in force
    Given extract "PII-SIT-20261120" for business date 2026-11-19 has a manifest with masking rule version "MASK-2026.11"
    Given the manifest lists 28,119 loan accounts: Mortgage 12,256, Hire purchase 12,960 and SSME 2,903, with total_balance sums per product

  Scenario: AC1 Masked copy
    Given a masked copy from the PII service
    When it is loaded into SIT
    Then every column tagged is_personal in party and contact_point holds a token or a masked value
    Then balances keep their shape: the count and the total_balance sum per product equal the manifest
    Then each party token joins to the same case_party and loan account rows as in the extract

  Scenario: AC2 A personal value left in the copy
    Given party row 4,512 of the extract holds a 13-digit value with a valid national ID check digit in id_no_token
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "unmasked value in party.id_no_token"
    Then the previous SIT copy stays in use

  Scenario: AC3 Totals that do not match the manifest
    Given the loan_account file holds 28,118 rows
    When the copy is loaded into SIT
    Then the system refuses the load in full with MSG-P1-002 and check "Control totals loan_account 28,118 against 28,119"

  Scenario: AC4 A copy aimed at DEV
    Given the target environment is DEV
    When the masked copy load starts
    Then the system refuses it with MSG-P1-002 and check "masked copies load only into SIT and UAT"
    Then the system reads no file

  Scenario: AC5 The same extract twice
    Given extract "PII-SIT-20261120" was loaded into SIT on 2026-11-20
    When it is loaded into SIT again
    Then the system skips the load and the report names the load of 2026-11-20

  Scenario: AC6 A masking rule version that is not in force
    Given a manifest with masking rule version "MASK-2026.10"
    When the copy is loaded into UAT
    Then the system refuses the load in full with MSG-P1-002 and check "masking rule version MASK-2026.10 is not in force"

  Scenario: AC7 A second load while one runs
    Given a masked copy load into SIT is running
    When a second load into SIT starts
    Then the system refuses the second load with MSG-P2-006
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | No production data in DEV; SIT and UAT use masked copies only | NFR-045; CTL-11 |
| BR2 | Every field tagged personal is masked or tokenized under the masking rules in force | Masking rules reference table; DL26; sys_fields.is_personal |
| BR3 | A copy with any personal value left in it is refused in full | CTL-11; DQ check "Refuse the load" |
| BR4 | Balances, dates and keys are not masked; counts and totals equal the manifest | CTL-02; REC-01, REC-02 |
| BR5 | The same customer gets the same token in every table, so joins hold | Mapping rule "Personal data" (s2t.txt) |
| BR6 | With no masking rule loaded, every personal field is replaced by a token | DL26 ("every personal field stays masked") |

### 9. State transitions

None. This story does not change a case status. It changes the masked copy load state in the pipeline: Running, Loaded, Refused or Skipped.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Starts the load in SIT or UAT; owns the intake containers |
| RW-COMPLY, Compliance and PDPA officer | Owns the masking rules and their version (DL26) |
| RW-TRIBE, Tribe lead and squad members | Run tests on the loaded copy with their test users' rights |
| SY-DATALOAD, data load | Identity the loader runs under in SIT and UAT |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PTY-001 to DF-PTY-012 | party | all fields | Write |
| DF-PTY-013 to DF-PTY-020 | contact_point | all fields | Write |
| DF-ACC-001 to DF-ACC-021 | loan_account | all fields | Write |
| DF-ACC-022 to DF-ACC-028 | account_payment | all fields | Write |
| DF-CAS-001 to DF-CAS-023 | recovery_case | all fields | Write |
| DF-CAS-030 to DF-CAS-035 | case_party | all fields | Write |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write |
| DF-REF-105 | sys_fields | is_personal | Read |

The other recovery tables in the extract load the same way. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Pipeline stage**

| Item | Value |
|---|---|
| Trigger | Manual start by the platform administrator for SIT or UAT after the PII service delivers an extract |
| Job name | Masked copy load, a SIT and UAT pipeline stage; not a scheduled job and not in the production job list (batch.txt) |
| Schedule | On request |
| Input | Masked extract files and manifest from the PII service in the environment's intake container |
| Output | Recovery schema in SIT or UAT replaced by the masked copy; load report with extract ID, business date, masking rule version, rows and totals per table and the check results |
| Events published | None |
| Idempotency key | Extract ID; a repeat is skipped |
| Restart behavior | Files load into staging schema `recovery_next`; the swap happens only after every check passes, so a failure leaves the previous copy |

**Endpoint used in SIT on the loaded copy**

| Method and path | Use | Authorization | Errors |
|---|---|---|---|
| GET /api/recovery/v1/cases/{caseId} | A test user reads a masked case | Case record, R, scope applied | 401 (MSG-P4-001); 403 (MSG-P4-002); 404 (MSG-P4-003); 503 |

### 13. Solution plan

- Package: folder `tools/masked-copy-loader`, Java package `recovery.tools.maskedcopy`, built as a separate build module that is not packaged into the ACE service.

| Component | Type | Responsibility |
|---|---|---|
| MaskedCopyLoader | Job | Spring Batch job: environment guard, manifest checks, file load to staging, swap |
| ManifestValidator | Service | Extract ID, masking rule version, schema version, control totals |
| MaskingVerifier | Service | Personal value patterns on every is_personal column; reuses the RWB-E1-065 verifier |
| LoadReportWriter | Service | Writes the load report for the pipeline |
| Masked copy stage | Job | Pipeline stage for SIT and UAT with a lock per environment |

- Database: no new recovery table. The stage loads into schema `recovery_next` in SIT or UAT and renames it to `recovery` after the checks; an advisory lock per environment prevents two loads at once; a small table `masked_copy_load` in the tool's own schema `tools` records extract ID, environment, business date, masking rule version and result.
- Configuration and reference data: properties `rwb.maskedcopy.allowed-environments=SIT,UAT`, `rwb.maskedcopy.intake-container` per environment (platform administrator); masking rule version from the masking rules reference table (Compliance, DL26).
- Build steps:
  1. Environment guard reading the deployment environment; refuse DEV and PROD.
  2. ManifestValidator with the extract ID check against `tools.masked_copy_load`.
  3. File load into `recovery_next` with the CTL-02 checks and the manifest totals.
  4. MaskingVerifier on every is_personal column, reusing the RWB-E1-065 patterns.
  5. Foreign key check, swap and load report.
  6. Pipeline stage with the per-environment lock.
  7. Tests for AC1 to AC7 on a test extract, and the access test in SIT.
- Feature flag: `rwb.dataengine.masked-copy`.
- Done when: the tests in section 16 pass and the first masked copy is in SIT before the Epic 1 SIT run.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P1-002 | The masked copy is refused at a check | The {source} load for {date} was refused: {check}. The previous load is still in use. |
| MSG-P2-006 | A load starts while one runs | {job} is already running. Wait for it to finish before you rerun it. |
| MSG-P4-002 | A test user without the right reads the copy | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The platform administrator and the squads read the load report in the pipeline. Test users see the masked copy through the normal SIT and UAT screens, with personal fields shown as tokens or masked values.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-004-01 | AC1, BR2, BR4, BR5 | System | Test extract PII-SIT-20261120 with 28,119 accounts |
| TC-TE-004-02 | AC2, BR3 | System | Injected value with a valid check digit in party row 4,512 |
| TC-TE-004-03 | AC3, BR4 | System | loan_account file with 28,118 rows |
| TC-TE-004-04 | AC4, BR1 | System | Target environment DEV |
| TC-TE-004-05 | AC5 | System | Extract loaded twice |
| TC-TE-004-06 | AC6, BR6 | System | Manifest with MASK-2026.10 |
| TC-TE-004-07 | AC7 | System | Two loads into SIT at once |
| TC-TE-004-08 | Access | Access | SIT test user with RW-REFADM calls GET /cases/{caseId}; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the masking rules and their version belong to Compliance; allowed environments are properties.
- No personal data in logs, tests or prompts: the load report holds counts, totals and check names, never a value; test extracts are built from synthetic data.
- No read of another module's tables at runtime: the loader is a tool outside the ACE service and runs only in SIT and UAT.
- No masked copy ever reaches DEV, and no copy is made from SIT or UAT to another environment.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Access per data product by role; personal data masked in line with PDPA | Business Requirements Epic 1, section 4; Program section 6.7 | None | All recovery processes | CTL-02, CTL-11; DL26 | TC-TE-004-01 to TC-TE-004-07 |
| REQ-ACA-005 | Personal data masked by role on every screen and agent call | Business Requirements Epic 1, section 4 | None | All recovery processes | CTL-11 | TC-TE-004-01, TC-TE-004-08 |

### 19. Out of scope

- Synthetic data in DEV (RWB-E1-065).
- The masking rule values per field and role (DL26, Compliance) and masking on screens (RWB-E1-037).
- The PII service itself, which the bank runs.
- The masked debt sale data tape (FEAT-DBS-03, Epic 5).


---

## RWB-TE-005 Rule table test harness

| Item | Value |
|---|---|
| Story key | RWB-TE-005 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | None (technical enabler) |
| Requirement IDs | REQ-CWC-014, REQ-CWC-013 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, section 5.3 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-044 |
| Status | Ready for build |

### 1. Story

As a **center of excellence analyst (RW-COE)**, I want **a harness that runs each rule row against its test case (the state, the event, the case facts and the expected result)**, so that **a rule change is tested the same way as code before it takes effect**.

### 2. Business rationale

The routing logic is 448 rules in ten route sets, held as data (ADR-004). A wrong condition or owner in one row moves every case that reaches it, and the bank has no test that proves a row does what its owner expects. Every rule row already names a test case (`rule_row.test_case_id`). This story runs those test cases on every rule load and in every build, and marks a version failed when any test fails. It meets REQ-CWC-014 and REQ-CWC-013. The measure is that every rule row in force has a passing test with its rule ID.

### 3. Preconditions

- RWB-E1-044 is done: migrations run with the parameterized schema.
- The rules component evaluates a route set as a decision table with hit policy Unique (ADR-004).
- The rule load template (RWB-E1-029) carries a Tests sheet with one test case per rule row.
- Rule rows exist with a `test_case_id` for each row (DF-REF-015, required).
- The Restructure route set is loaded in SIT with its 37 rows, R-RES-01 to R-RES-37.
- The loader holds RW-COE (Rules and parameters C).

**Work in this order.** A1 to A7 are build actions. The harness runs inside the existing rule-version load and in every build; there is no screen and no new endpoint.

| # | Developer action | What to build | Done when |
|---|---|---|---|
| A1 | Create `rule_test_case` and its repository | Write `V<seq>__rwb_te_005_rule_test_case.sql`. Create `rule_test_case` with `test_case_id`, `route_set`, `rule_version`, `rule_id`, `from_state`, `event_code`, `facts` jsonb, `expected_to_state`, `expected_owner_role`, `expected_timer_spec`, `result` and `result_detail`, with the standard columns and `UNIQUE (route_set, rule_version, test_case_id)`. Add `RuleTestCase` and `RuleTestCaseRepository`. | The migration runs clean, and a second row for the same route set, version and test case ID is refused. |
| A2 | Read the Tests sheet into test cases | Write `TestsSheetReader` to read the Tests sheet of the rule template, one test case per rule row, and store each through `RuleTestCaseRepository` with the rule ID, test case ID, from state, event, facts and the three expected values. A row that names a `test_case_id` the sheet does not hold fails the version with MSG-P3-014 naming the rule and the test case. | RES-2026.11 loads 37 rows and 37 test cases with nothing missing; version RES-2026.13 fails naming R-RES-12 and RT-RES-012. |
| A3 | Build the synthetic case file | Write `CaseFileFixtureBuilder` to turn the `facts` of a test into a synthetic case file of codes and numbers only (BR5). Refuse the test when a fact its condition needs has no value. | A test with no `break_count` fails naming `break_count`; a complete test builds a fixture with no customer, account or personal value in it. |
| A4 | Build the harness and the pass rule | Write `RuleTableHarnessImpl` implementing the published `RuleTableHarness` in `recovery.casewf.rules.harness`. Read the version's rule rows through the P4 `RuleTableReader`, evaluate the route set with the test's `from_state` and `event_code` through the shared decision-table evaluator under hit policy Unique, and apply the four-part pass rule: exactly one row hit, that row is the `rule_id` the test names, and its `to_state`, `owner_role` and `timer_spec` equal the expected values. Return one `RuleTestResult` per rule ID. | A changed to state fails R-RES-04 with expected and actual named; two hits fail naming both rule IDs; zero hits fail naming the expected rule. |
| A5 | Wire the harness into the rule-version load | In the P4 load handler behind `POST /api/recovery/v1/admin/rule-versions`, run the `rules.txt` completeness checks first, write the rule rows and test cases, then call `RuleTableHarness.run(routeSet, ruleVersion)` inside the same request and transaction. Build no new endpoint and change no contract. | A load of RES-2026.11 returns 201 after 37 passes; a version with any failing test returns 422 with each failing rule ID in `Problem.detail`. |
| A6 | Set the version state and store the result | Set the version `VALIDATED` when every test passes and `FAILED` when any fails, write `result` and `result_detail` back to each `rule_test_case` row, and keep one result set per version by updating on a rerun. A FAILED version cannot be approved or take effect. Put it behind `rwb.p3.rule-harness`: on in SIT, UAT and PROD; off in DEV only, where the load continues with a warning and the version still stays FAILED. | Running the same version twice leaves 37 results, not 74; a FAILED version is refused at approval and never takes effect. |
| A7 | Add the build gate | Add the Gradle task `ruleTests` running `RuleTableHarnessTest` as a JUnit 5 dynamic test factory: one named test per rule ID over `recovery/src/test/resources/rules/*.xlsx`, using the same `RuleTableHarnessImpl` and pass rule as the load path. | The build runs 448 named rule tests across the ten route sets, and a failing rule test fails the build with the rule ID in the build report. |

**Do not build:** the rule template, schema, overlap, unreachable row and default checks, load and rollback (RWB-E1-029); the change log and approval checklist (RWB-E1-048); the rules and parameters screen SCR-39 in Epic 8. Do not query `rule_row` directly, do not write an expected value into code and do not add a second evaluator.

**Hand-off:** the published `RuleTableHarness`, `HarnessResult` and `RuleTestResult` go to P4 and to RWB-E1-048 for the test result on the version; the `ruleTests` task goes into the pipeline for every squad; MSG-P3-014 goes to the message table.

### 4. Flow

1. Center of excellence analyst: loads a rule version through `POST /admin/rule-versions` with the rules and the Tests sheet.
2. P4 load handler: stores the rule rows and calls `RuleTableHarness.run(routeSet, ruleVersion)`.
3. Harness: reads the rule rows of the version and their test cases.
4. Harness: for each test case, builds a synthetic case file from the facts, evaluates the route set for the from state and the event, and gets the rows that hit.
5. Harness: passes the test when exactly one row hits, it is the row named by the test, and its to state, owner role and timer equal the expected values.
6. Harness: returns one result per rule ID; the load handler sets the version state to VALIDATED when every test passes, or FAILED otherwise, and writes the test result for the change log (RWB-E1-048).
7. Build pipeline: runs the same harness as a JUnit dynamic test per rule ID over the rule files in the repository.

### 5. Exception paths

None.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the rule rows and the evaluator; the load endpoint calls it |
| Negotiable | The report format can change; the pass rule is fixed |
| Valuable | A rule change cannot take effect with a row that fails its own test |
| Estimable | One harness service, one test runner, one test case table |
| Small | Fits in one sprint with its tests |
| Testable | The harness tests itself with fixture route sets |

### 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every rule row has one test case, named by its `test_case_id` | DF-REF-015; ADR-004 |
| BR2 | A test passes when exactly one row hits, it is the named row, and its to state, owner role and timer equal the expected values | rules.txt Key (hit policy Unique) |
| BR3 | A version with any failing test is FAILED and cannot be approved or take effect | REQ-CWC-014; CTL-08 |
| BR4 | The harness runs on every rule load and in every build | REQ-CWC-013; DT11 |
| BR5 | Tests use synthetic case facts only | NFR-045; NFR-054 |
| BR6 | The completeness checks of the rule set run before the tests | rules.txt Checks |

### 9. State transitions

None. This story does not change a case status. It sets the state of a rule version (standard column `rule_row.state` for the rows of the version): loaded rows move to VALIDATED when every test passes, or to FAILED.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-COE, center of excellence analyst | Loads a rule version, which runs the harness (Rules and parameters C); reads the results |
| RW-RISK, risk and model risk officer | Reads the results before approving (Rules and parameters R, A) |
| SY-RULES, rules component | Evaluates the rows inside the harness |
| RW-AUDIT, internal audit | Reads the results (Rules and parameters R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-REF-002 | rule_row | rule_id | Read |
| DF-REF-003 | rule_row | rule_version | Read |
| DF-REF-004 | rule_row | route_set | Read |
| DF-REF-005 | rule_row | from_state | Read |
| DF-REF-006 | rule_row | event_code | Read |
| DF-REF-007 | rule_row | condition_expr | Read |
| DF-REF-009 | rule_row | to_state | Read |
| DF-REF-010 | rule_row | owner_role | Read |
| DF-REF-011 | rule_row | timer_spec | Read |
| DF-REF-015 | rule_row | test_case_id | Read |
| DF-REF-186 | rule_test_case | test_case_id | Write |
| DF-REF-188 | rule_test_case | rule_version | Write |
| DF-REF-189 | rule_test_case | rule_id | Write |
| DF-REF-190 | rule_test_case | from_state | Write |
| DF-REF-191 | rule_test_case | event_code | Write |
| DF-REF-192 | rule_test_case | facts | Write |
| DF-REF-193 | rule_test_case | expected_to_state | Write |
| DF-REF-194 | rule_test_case | expected_owner_role | Write |
| DF-REF-195 | rule_test_case | expected_timer_spec | Write |
| DF-REF-196 | rule_test_case | result | Write |
| DF-REF-197 | rule_test_case | result_detail | Write |

`rule_row` is read through the P4 published interface. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**POST /api/recovery/v1/admin/rule-versions** (P4 endpoint; runs the harness)

| Item | Value |
|---|---|
| Request | multipart/form-data: `file` (the rule template with its Rules and Tests sheets), `routeSet`, `validFrom` |
| Response | 201 `RuleVersion` rows of the version; 422 when the harness fails, with a `Problem` whose `detail` lists each failing rule ID |
| Errors | 401 (MSG-P4-001); 403 no Rules and parameters C (MSG-P4-002); 409 the version already exists (MSG-GEN-004); 422 harness failure (MSG-P3-014); 503 |
| Authorization | Rules and parameters, right C |
| Idempotency | Route set, version and file hash; a repeat returns the stored result |

**GET /api/recovery/v1/admin/rule-versions?routeSet=&status=** (P4) lists versions with status VALIDATED or FAILED (Rules and parameters R).

**Published interface** (package `recovery.casewf.rules.harness.api`):

```java
public interface RuleTableHarness {
    HarnessResult run(String routeSet, String ruleVersion);
}

public record HarnessResult(String routeSet, String ruleVersion, int total, int passed,
                            List<RuleTestResult> results) {}

public record RuleTestResult(String ruleId, String testCaseId, boolean passed,
                             List<String> hitRuleIds, String expected, String actual) {}
```

**Build job.** The Gradle task `ruleTests` runs `RuleTableHarnessTest` as a JUnit 5 dynamic test factory, one test per rule ID, over `recovery/src/test/resources/rules/*.xlsx`. No events are published.

### 13. Solution plan

**Package.** `recovery.casewf.rules.harness` in the recovery module; tests in `recovery/src/test/java/recovery/casewf/rules/harness`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| RuleTableHarnessImpl | Service | Runs every test of a version through the evaluator and builds the result |
| CaseFileFixtureBuilder | Service | Builds a synthetic case file from the test facts; refuses a missing fact |
| RuleTestCaseRepository | Repository | Reads and writes `rule_test_case` |
| TestsSheetReader | Service | Reads the Tests sheet of the rule template into test cases |
| RuleTableHarnessTest | Job | The build dynamic test factory, one test per rule ID |
| RuleTableHarness | Published interface | The interface in section 12 |

**Database.** Migration `V<next>__rwb_te_005_rule_test_case.sql` creates `rule_test_case` (`id uuid PK`, `test_case_id varchar(20)`, `route_set varchar(15)`, `rule_version varchar(20)`, `rule_id varchar(20)`, `from_state varchar(60)`, `event_code varchar(60)`, `facts jsonb`, `expected_to_state varchar(60)`, `expected_owner_role varchar(20)`, `expected_timer_spec varchar(60)`, `result varchar(10)`, `result_detail varchar(1000)`, standard columns), `UNIQUE (route_set, rule_version, test_case_id)`.

**Configuration and reference data.** The Tests sheet of each rule template, prepared by the center of excellence analyst with one test case per row. The completeness checks of rules.txt Checks, run first.

**Build steps**

1. Write the migration and `RuleTestCaseRepository`.
2. Build `TestsSheetReader` and `CaseFileFixtureBuilder`; test a missing fact.
3. Build `RuleTableHarnessImpl` with the BR2 pass rule; test zero hits, two hits and a wrong to state with fixture route sets.
4. Wire it into the P4 rule version load handler; set the version state and the test result for RWB-E1-048.
5. Build `RuleTableHarnessTest` and add the `ruleTests` task to the build.
6. Run it on the 37 Restructure rows and the 448 rows in the repository.

**Feature flag.** `rwb.p3.rule-harness`. The flag cannot be off in SIT, UAT or PROD; off in DEV only, where a failed harness warns and the load continues.

**Done when.** The tests in section 16 pass, and the build runs 448 named rule tests.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-014 | One or more rule tests fail | Rule version {version} failed {count} of {total} rule tests. |
| MSG-P4-002 | A role without Rules and parameters C loads a version | You cannot {action} here. Your role does not include it. |

MSG-P3-014 is new (see Additions). It shows in the load response and the build log.

### 15. Screens and states

No screen in this story. The center of excellence analyst reads the result in the load response and on the version list; the rules and parameters screen SCR-39 shows it from Epic 8. Developers read the named rule tests in the build report.

### 16. Test cases

None.

### 17. Guardrails

- No business value in code. The expected results are data in the Tests sheet; the harness holds only the pass rule.
- No personal data in test facts, results, logs or prompts. Facts are codes and numbers.
- No read of another module's tables. Rule rows are read through the P4 interface.
- A failing harness never lets a version take effect, in any environment above DEV.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-014 | Rule loads validated against a set of test cases before they take effect | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-RES-01 to R-RES-37 | None |
| REQ-CWC-013 | A rule change goes to production with a version stamp and no code release | Business Requirements Epic 1, section 4; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-38 | None |

### 19. Out of scope

- The rule template, schema, overlap and unreachable row checks, load and rollback (RWB-E1-029).
- The change log and approval checklist (RWB-E1-048).
- The QA sample of closed decisions against the rule version applied (FEAT-ADM-08, Epic 8).


---

## RWB-TE-006 Outbox and retry for outbound work

| Item | Value |
|---|---|
| Story key | RWB-TE-006 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-DRI-007 |
| BRD section | Business Requirements Program, section 5.2 and section 6.4 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-027, RWB-E1-007 |
| Status | Ready for build |

### 1. Story

As a **squad member (RW-TRIBE)**, I want **every application event and every outbound work request written to an outbox in the same transaction as the change, and delivered to each consumer in order with retry**, so that **no outbound action is lost when a system or a consumer is down, and nothing is sent for a change that did not commit**.

### 2. Business rationale

The Workbench modules talk to each other through application events, and outbound work such as a notice for WIN starts from an event in the module that approved it. If the event is sent before the change commits, or is lost when a consumer fails, a notice is never dispatched or a ledger entry is missing, and nobody sees it. The outbox stores each event with the change, a sender delivers it to every consumer at least once in case order, retries on a schedule held as data, and moves a delivery that keeps failing to the exception queue with a task. It meets REQ-DRI-007 (retry on a defined schedule; exception queue with a task for a named owner) and NFR-025 and NFR-026. The measure is the count of outbox deliveries in the exception queue over one day, with a target of zero (FSD P2 A2.1.1).

### 3. Preconditions

- RWB-E1-044 (versioned migrations), RWB-E1-027 (decision log writer) and RWB-E1-007 (integration adapters, IdempotencyGuard and the outbound file sender) are done.
- The consumer list is loaded in the configuration service (RWB-E1-042) under rwb.integration.outbox.consumers: consumer name, the event types it takes, its owner role, and whether it holds a case step (for example the consumer "win-dispatch" of the work request WIN_DISPATCH holds the case step, owner role RW-PLATADM; assumed).
- The retry settings are loaded under rwb.integration.outbox.retry: 3 retries at 1, 5 and 15 minutes after the previous attempt (assumed; NFR-026, DL11).
- Quartz runs clustered in the ACE service; JOB-11 Outbox sender runs every minute.
- Feature flag `rwb.integration.outbox` is on.

### 4. Flow

1. Business service (for example notice approval): calls OutboxWriter.publish inside its own transaction with the event type (an event from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH), schema version, case ID, payload references, actor and idempotency key.
2. OutboxWriter: writes one outbox_event row with the next case sequence, and one outbox_delivery row per consumer listed for the event type.
3. Database: commits the change, the event and its deliveries together, or none of them.
4. JOB-11 Outbox sender (event step): every minute selects due deliveries with a row lock that skips rows another instance holds, oldest case sequence first, taking only the lowest open sequence per case and consumer.
5. OutboxSender: calls the consumer with the event header (event ID, idempotency key, schema version, occurred time, actor) and payload; each consumer checks the key through IdempotencyGuard (RWB-E1-007) before it acts.
6. OutboxSender: on success marks the delivery DELIVERED; when the delivery had failed before and the consumer holds a case step, raises RETRY_SUCCEEDED for the case (R-UNI-35).
7. OutboxSender: on a failure adds 1 to the attempt count and sets the next attempt from the retry settings; on the first failure of a consumer that holds a case step, raises SYSTEM_UNAVAILABLE for the case (R-UNI-33).
8. OutboxSender: when the retries are used, sets the delivery to EXCEPTION, raises task RESOLVE_OUTBOX_DELIVERY for the consumer's owner role on the case and, for a consumer that holds a case step, raises RETRY_LIMIT_REACHED (R-UNI-36), which writes the decision log entry; all in one transaction.
9. Platform administrator: reads exception deliveries (GET /admin/outbox/deliveries) and, once the consumer is fixed, sends one again (POST /admin/outbox/deliveries/{deliveryId}/resend).

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The business transaction rolls back | No event and no delivery exist | None | AC3 |
| X2 | A consumer fails once and then succeeds | Delivery DELIVERED on the retry; the case resumes when the consumer holds a case step (R-UNI-35) | None | AC4 |
| X3 | The same idempotency key is published twice | One event exists | None | AC5 |
| X4 | Two service instances run the sender at once | Each delivery is made once | None | AC6 |
| X5 | An earlier event for the same case and consumer is failing | Later events for that case and consumer wait | None | AC7 |
| X6 | One consumer fails and another succeeds on the same event | Each consumer's delivery has its own state | None | AC8 |
| X7 | A platform administrator sends a delivery that is not in EXCEPTION | Refused with 409 | MSG-P2-022 | AC9 |
| X8 | An event with no case fails past its limit | EXCEPTION and an alert to the platform administrator; no task, no case event | MSG-P2-001 | AC10 |
| X9 | The retry settings are changed | The next attempt uses the new delays | None | AC11 |
| X10 | The decision log cannot be written when the limit is reached | Nothing changes; the delivery stays RETRYING and is tried at the next run; incident raised (R-UNI-39) | MSG-P7-003 | Principle 5 test TC-TE-006-13 |
| X11 | A role without Platform administration U sends a delivery again | Refused with 403 | MSG-P4-002 | Access test TC-TE-006-12 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the migration tool, the decision log writer and the IdempotencyGuard of Epic 1; consumers are listed in configuration |
| Negotiable | Consumers, owners, retry counts and delays are configuration |
| Valuable | No event or outbound request is lost or sent for a change that rolled back |
| Estimable | Two tables, one writer, one sender step, two admin endpoints |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below uses a stub consumer that fails on demand |

### 7. Acceptance criteria

```gherkin
Feature: Outbox and retry for outbound work

  Background:
    Given consumer "win-dispatch" takes work request WIN_DISPATCH, holds the case step and has owner role RW-PLATADM
    Given consumers "ledger" and "reporting-feed" take CaseAllocated, CaseTransferred and CaseStateChanged, do not hold the case step and have owner role RW-PLATADM
    Given the retry settings are 3 retries at 1, 5 and 15 minutes after the previous attempt
    Given case "RW-2026-000601" has notice "NT-SYN-0601" waiting for approval

  Scenario: AC1 Sent after commit
    Given a notice approved
    When the transaction commits at 14 December 2026 10:00:00
    Then the outbox holds one WIN_DISPATCH request for case "RW-2026-000601" with one delivery for "win-dispatch"
    Then the header holds the event ID, idempotency key "WIN_DISPATCH:NT-SYN-0601", schema version 1, occurred time and actor
    Then the payload holds notice and case references only, with no name, address or identifier
    Then at the 10:01 run the sender delivers it and "win-dispatch" passes the notice to OutboundFiles.enqueue for the day's WIN file
    Then the delivery has status DELIVERED

  Scenario: AC2 Retry limit
    Given a target down for longer than the retry limit
    When "win-dispatch" fails at 10:01, 10:02, 10:07 and 10:22
    Then the system makes no fifth attempt
    Then the item moves to the exception queue: the "win-dispatch" delivery has status EXCEPTION and attempt count 4
    Then the system raises task RESOLVE_OUTBOX_DELIVERY on case "RW-2026-000601" for role RW-PLATADM
    Then event RETRY_LIMIT_REACHED moves the case to EXCEPTION_QUEUE by R-UNI-36 with one decision log entry

  Scenario: AC3 Nothing is sent for a change that did not commit
    Given the notice approval fails after OutboxWriter.publish and the transaction rolls back
    When the sender runs
    Then no event and no delivery exist for "NT-SYN-0601"

  Scenario: AC4 A retry that succeeds
    Given "win-dispatch" fails at 10:01 and the case moves to RETRY_QUEUE by R-UNI-33
    When the attempt at 10:02 succeeds
    Then the system delivers the delivery status with attempt count 2
    Then event RETRY_SUCCEEDED returns the case to the state it paused in by R-UNI-35

  Scenario: AC5 The same event is written once
    Given the approval of "NT-SYN-0601" is submitted twice with idempotency key "WIN_DISPATCH:NT-SYN-0601"
    When both transactions commit
    Then the outbox holds one event with that key
    Then the second transaction receives DuplicateOutboxKeyException and changes nothing

  Scenario: AC6 Two sender instances
    Given 200 due deliveries and two service instances
    When JOB-11 runs on both at 10:01
    Then the system makes each delivery once
    Then the delivery log holds 200 calls

  Scenario: AC7 Order per case and consumer
    Given event CaseTransferred with case sequence 11 and event CaseStateChanged with case sequence 12 for case "RW-2026-000601"
    Given the "ledger" consumer fails on sequence 11
    When the sender runs
    Then the system does not deliver sequence 12 to "ledger" until sequence 11 is DELIVERED

  Scenario: AC8 Consumers are independent
    Given event CaseAllocated for case "RW-2026-000601"
    When "ledger" fails and "reporting-feed" succeeds at 10:01
    Then the system delivers the "reporting-feed" delivery and the "ledger" delivery is RETRYING with next attempt 10:02
    Then the case route state does not change, because "ledger" does not hold the case step

  Scenario: AC9 Sending an exception delivery again
    Given delivery "OBD-SYN-0001" has status EXCEPTION
    When the platform administrator sends it again
    Then the response is 200 with message MSG-GEN-005
    Then the delivery status is PENDING with attempt count 0 and due at the next run
    When the platform administrator sends delivery "OBD-SYN-0002" with status DELIVERED again
    Then the response is 409 with message MSG-P2-022

  Scenario: AC10 An event with no case
    Given an event with no case whose only consumer fails 4 times
    When the retries are used
    Then the delivery status is EXCEPTION
    Then the system sends an alert to the platform administrator within 15 minutes
    Then no task and no case event are raised

  Scenario: AC11 Retry settings come from configuration
    Given the retry delays are changed in the configuration service to 2, 10 and 30 minutes at 09:00
    When "ledger" fails at 10:01
    Then the next attempt is due at 10:03
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | An event and its deliveries are written in the same transaction as the change: no event without the change and no change without the event | events.txt Rules, Transactions |
| BR2 | Each event carries an event ID and an idempotency key unique in the outbox; consumers drop a repeat through IdempotencyGuard | events.txt Rules, Duplicates; R-UNI-40 |
| BR3 | Delivery is at least once; each consumer has its own delivery state | events.txt Rules, Delivery |
| BR4 | Events for one case reach each consumer in the order they were written | events.txt Rules, Ordering |
| BR5 | A failed delivery is retried on the schedule; after the last retry it moves to the exception queue with a task for the consumer's owner role | events.txt Rules, Failure; NFR-026; REQ-DRI-007 |
| BR6 | For a consumer that holds a case step, the first failure raises SYSTEM_UNAVAILABLE, a later success RETRY_SUCCEEDED, and the limit RETRY_LIMIT_REACHED | R-UNI-33; R-UNI-35; R-UNI-36 |
| BR7 | Payloads hold references and codes, never personal data; the event carries its schema version | events.txt Rules, Payload and Versioning |
| BR8 | The move to the exception queue for a case does not happen unless its decision log entry is written | R-UNI-39; Principle 5; CTL-06 |
| BR9 | Consumers, owners, retry counts and delays are read from configuration | Principle 1; DL11 |

### 9. State transitions

Case status does not change. For a consumer that holds a case step, the route state changes through the universal rules; each delivery has its own status.

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | SYSTEM_UNAVAILABLE | First failed delivery to a consumer that holds the case step | RETRY_QUEUE (R-UNI-33) |
| RETRY_QUEUE | RETRY_SUCCEEDED | The retry succeeds | RESUME_STATE (R-UNI-35) |
| RETRY_QUEUE | RETRY_LIMIT_REACHED | Retries used | EXCEPTION_QUEUE (R-UNI-36) |
| Delivery PENDING or RETRYING | Consumer succeeds | None | Delivery DELIVERED |
| Delivery PENDING | Consumer fails | Retries left | Delivery RETRYING |
| Delivery RETRYING | Consumer fails | No retries left | Delivery EXCEPTION |
| Delivery EXCEPTION | Sent again by the platform administrator | None | Delivery PENDING |

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF, case workflow module | Runs the sender step, applies R-UNI-33, R-UNI-35 and R-UNI-36 and raises the task |
| SY-DECLOG, decision log writer | Writes the entry for the move to the exception queue |
| RW-PLATADM, platform administrator | Reads deliveries and sends an exception delivery again (Platform administration CRUD) |
| RW-COE, RW-DATASTEW, RW-AUDIT, RW-COMPLY | Read deliveries (Platform administration R) |
| RW-SECADM, security administrator | Reads deliveries (Platform administration CRUDA) |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

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
| DF-WRK-017 to DF-WRK-026 | task | all fields | Write, through the P3 published interface |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write, through the P3 rule step that calls the P7 writer |
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Write, through the P3 rule step |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Published interfaces**

```java
// recovery.integration.api; joins the caller's transaction
UUID OutboxWriter.publish(OutboxEvent event);
//   OutboxEvent: eventType (EV-01 to EV-28 names, or a work request type such as WIN_DISPATCH), schemaVersion, caseId (nullable), payload (references only), actorRef, idempotencyKey
//   throws DuplicateOutboxKeyException when the key exists
// Implemented by each consumer and listed under its consumer name
ConsumeResult OutboxConsumer.consume(EventHeader header, JsonNode payload);   // OK or FAILED(code)
// P3 interfaces used on failure and recovery
void CaseEvents.raise(UUID caseId, String eventCode, String reference);  // SYSTEM_UNAVAILABLE, RETRY_SUCCEEDED, RETRY_LIMIT_REACHED
UUID TaskApi.raiseTask(UUID caseId, String taskCode, String ownerRole);
// RWB-E1-007, called by each consumer before it acts
boolean IdempotencyGuard.firstTime(String consumer, String idempotencyKey);
```

**Job**

| Item | Value |
|---|---|
| Trigger | JOB-11 Outbox sender, every minute; this story adds the event step beside the outbound file step of RWB-E1-007 |
| Input | outbox_delivery rows with status PENDING or RETRYING and next_attempt_at at or before now |
| Output | Deliveries DELIVERED, RETRYING or EXCEPTION; case events; tasks; alerts |
| Events published | None of its own; it delivers EV-01 to EV-28 to their consumers |
| Idempotency key | outbox_event.idempotency_key, passed to each consumer in the header |
| Restart | Rows are locked per delivery with skip-locked selection; a delivery in flight when an instance stops is retried at its next attempt time and the consumer drops the repeat by its key |

**GET /api/recovery/v1/admin/outbox/deliveries** (new; recorded in the additions file)

| Item | Value |
|---|---|
| Query | status, consumer, eventType, from, to, page, size |
| Response 200 | OutboxDeliveryPage: items of OutboxDelivery (id, eventId, eventType, caseId, consumer, status, attemptCount, nextAttemptAt, lastErrorCode, deliveredAt, createdAt), page, size, total. The payload is not returned |
| 403 | Role lacks Platform administration R (MSG-P4-002) |
| Authorization | Platform administration, right R |
| Idempotency | Read only |

**POST /api/recovery/v1/admin/outbox/deliveries/{deliveryId}/resend** (new; recorded in the additions file)

| Item | Value |
|---|---|
| Request | None |
| Response 200 | OutboxDelivery with status PENDING and attempt count 0; message MSG-GEN-005 |
| 403 | Role lacks Platform administration U (MSG-P4-002) |
| 404 | Delivery not found (MSG-P4-003) |
| 409 | Delivery not in EXCEPTION (MSG-P2-022) |
| Authorization | Platform administration, right U; written to the ACE audit log with the user and the time |
| Idempotency | A second call finds the delivery PENDING and returns 409 |

### 13. Solution plan

**Package.** Folder `recovery/integration/outbox`, Java package `<ACE base package>.recovery.integration.outbox`; OutboxWriter and OutboxConsumer in `recovery.integration.api`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| OutboxWriter | Published interface | Writes the event and one delivery per listed consumer in the caller's transaction (BR1, BR2, BR7) |
| OutboxEventEntity, OutboxDeliveryEntity | Entity | The two new rows |
| OutboxRepository | Repository | Skip-locked selection of due deliveries in case order per consumer (BR4) |
| OutboxSender | Service | Delivery, retry scheduling, case events and exception move (BR3, BR5, BR6, BR8) |
| ConsumerCatalog | Service | Reads the consumer list and the retry settings (BR9) |
| OutboxSenderEventStep | Job | The event step of JOB-11 |
| OutboxAdminController | Controller | GET /admin/outbox/deliveries and the retry endpoint |

**Database.** Flyway migration `V<next>__create_outbox_event.sql` in the P2 migration folder creates:
- outbox_event (id uuid primary key, event_type varchar(40) not null, schema_version integer not null, case_id uuid, case_seq bigint, idempotency_key varchar(120) not null, payload jsonb not null, actor_ref varchar(64), occurred_at timestamptz not null, plus the standard columns), with `UNIQUE (idempotency_key)` and `UNIQUE (case_id, case_seq)`.
- outbox_delivery (id uuid primary key, event_id uuid not null references outbox_event, consumer varchar(60) not null, status varchar(12) not null default 'PENDING', attempt_count integer not null default 0, next_attempt_at timestamptz not null, last_error_code varchar(40), delivered_at timestamptz, task_id uuid, plus the standard columns), with `UNIQUE (event_id, consumer)`, `CHECK (status IN ('PENDING','RETRYING','DELIVERED','EXCEPTION'))` and index `ix_outbox_delivery_due ON outbox_delivery (next_attempt_at) WHERE status IN ('PENDING','RETRYING')`.
case_seq is the case's highest sequence plus 1, taken under a lock on the case's latest outbox row.

**Configuration and reference data.** rwb.integration.outbox.consumers and rwb.integration.outbox.retry (assumed values in section 3; DL11), batch size 200 per run (assumed), loaded by RW-REFADM through the configuration service; the alert route to the operations channel from RWB-E1-056.

**Build steps**

1. Write the migration and the two entities; test the unique keys (AC5).
2. Write OutboxWriter joining the caller's transaction; test commit and rollback (AC1, AC3).
3. Write OutboxRepository with skip-locked selection and order per case and consumer; test two instances (AC6), order (AC7) and independent consumers (AC8).
4. Write OutboxSender with ConsumerCatalog and a stub consumer; test retry and success (AC2, AC4, AC11).
5. Add the case events, the task and the exception move through the P3 interfaces; test the forced decision log failure.
6. Add the alert for events with no case (AC10).
7. Add OutboxSenderEventStep to JOB-11.
8. Write OutboxAdminController with the access check and the audit write (AC9 and the access test).

**Feature flag.** `rwb.integration.outbox`. Off: the event step does not run and deliveries stay PENDING; the writer still records events so nothing is lost when it is switched on.

**Done when.** The tests in section 16 pass and the JOB-11 event step shows its runs on the job monitoring of RWB-E1-056.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P2-001 | Task text when a delivery enters the exception queue (new) | {interface} did not deliver {item} after {count} attempts. It is in the exception queue. |
| MSG-P2-022 | Sending again a delivery that is not in EXCEPTION (new) | Only an item in the exception queue can be sent again. |
| MSG-GEN-005 | A delivery is queued to send again | Saved. |
| MSG-P7-003 | Decision log write failed at the exception move | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role lacks the Platform administration right | You cannot {action} here. Your role does not include it. |
| MSG-P4-003 | Delivery not found | This case is not in your scope. |

In MSG-P2-001, {interface} is the consumer name and {item} the event type and case number. Thai text for each message follows decision DL10.

### 15. Screens and states

No screen of its own in Epic 1. The task RESOLVE_OUTBOX_DELIVERY appears on SCR-09 Exception queue (states Loading and List) for the owner role, with MSG-P2-001. The platform administrator uses the two admin endpoints; SCR-44 Interface and job monitor shows the deliveries from Epic 2.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-006-01 | AC1, BR1, BR3, BR7 | System | Notice NT-SYN-0601 approved at 10:00; win-dispatch stub succeeds |
| TC-TE-006-02 | AC2, BR5, BR6, BR8 | System | win-dispatch stub fails 4 times |
| TC-TE-006-03 | AC3, BR1 | System | Approval rolled back after publish |
| TC-TE-006-04 | AC4, BR6 | System | win-dispatch stub fails once, then succeeds |
| TC-TE-006-05 | AC5, BR2 | System | Two approvals with key WIN_DISPATCH:NT-SYN-0601 |
| TC-TE-006-06 | AC6 | System | 200 due deliveries, two instances |
| TC-TE-006-07 | AC7, BR4 | System | Sequences 11 and 12, ledger stub failing on 11 |
| TC-TE-006-08 | AC8, BR3 | System | ledger fails and reporting-feed succeeds on one CaseAllocated event |
| TC-TE-006-09 | AC9 | System | Deliveries OBD-SYN-0001 in EXCEPTION and OBD-SYN-0002 DELIVERED |
| TC-TE-006-10 | AC10 | System | Event with no case, consumer failing 4 times |
| TC-TE-006-11 | AC11, BR9 | System | Retry delays changed to 2, 10 and 30 minutes before the run |
| TC-TE-006-12 | Access | Access | RW-DATASTEW sends a delivery again; refused with MSG-P4-002 |
| TC-TE-006-13 | Principle 5 | Resilience | Decision log write forced to fail at the exception move; delivery stays RETRYING; MSG-P7-003 in the job log; incident raised |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: consumers, owners, retry counts, delays and batch size are configuration.
- No personal data in logs, tests or prompts; payloads hold references and codes only, and the admin endpoint does not return the payload.
- No read of another module's tables: case events and tasks go through the P3 interfaces; the decision log through P7.
- No event or delivery is deleted; a delivery leaves the exception queue only by being sent again.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-007 | Retry on a defined schedule; exception queue with a task for a named owner | Business Requirements Program, section 5.2 and section 6.4 | None | All recovery processes | R-UNI-33, R-UNI-35, R-UNI-36, R-UNI-39, R-UNI-40 | TC-TE-006-01 to TC-TE-006-13 |

### 19. Out of scope

- Outbound files, their SFTP transfer, retry and resend, and the duplicate check by key: RWB-E1-007.
- The consumers themselves, for example the ledger listener: RWB-E1-067 and RWB-E2-034.
- The interface and job monitor screen: SCR-44 in Epic 2 and Epic 8.
- Retry values: DL11.


---

## RWB-TE-007 Scheduled jobs on Quartz

| Item | Value |
|---|---|
| Story key | RWB-TE-007 |
| Epic | E1, release 30 November 2026 |
| Module | P3 Case and workflow |
| Feature | None (technical enabler) |
| Requirement IDs | REQ-CWC-007, REQ-CWC-011, REQ-RDF-007 |
| BRD section | Business Requirements Epic 1, sections 3.3 and 4; Business Requirements Program, sections 5.1, 5.3 and 6.3 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-044, RWB-E1-056 |
| Status | Ready for build |

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **the timer check, the morning allocation run and the daily reconciliation run as Quartz jobs with a run book each**, so that **scheduled work runs once, on time and visibly, and a missed run is caught up for its business date**.

### 2. Business rationale

The morning allocation must finish by 07:00 so no new case waits for a person (JOB-03), the timer check must find every due timer every 5 minutes (JOB-05), and the reconciliation must compare the case list with the core bank every day (JOB-04). The ACE service runs on more than one instance, so without a shared schedule a job runs twice or not at all, and an outage loses a day's run. This story runs the three jobs on the clustered ACE Quartz scheduler with one run per business date, catch-up after an outage and a run book for each. It meets REQ-CWC-007, REQ-CWC-011 and REQ-RDF-007. The measure is one successful run per job per business date, and JOB-03 complete by 07:00 (NFR-013).

### 3. Preconditions

- RWB-E1-044 is done: migrations run with the parameterized schema.
- RWB-E1-056 is done: the job monitor records runs and alerts the operations channel.
- The ACE Quartz scheduler runs with a clustered JDBC job store; its `QRTZ_` tables belong to the ACE common module.
- JOB-01 COLLINS load check and intake publishes LoadCompleted (EV-26) with the business date; JOB-02 Case creation records its run per business date.
- The job bodies exist: allocation (RWB-E1-020), reconciliation (RWB-E1-011) and timer check (RWB-E1-028).
- `jobs.catch-up.max-dates` = 5 (assumed; DL11) and the 07:00 deadline for JOB-03 (NFR-013) are in the configuration service.

### 4. Flow

1. Scheduler: on LoadCompleted for business date D, and on completion of JOB-02 for D, fires JOB-03 Morning allocation and JOB-04 Daily reconciliation for D.
2. Scheduler: fires JOB-05 Timer check every 5 minutes on cron `0 0/5 * * * ?` in Asia/Bangkok.
3. Job runner: takes the cluster lock so only one instance runs a job at a time.
4. Job runner: checks the job run log for job and business date; if a successful run exists, records the skip and stops.
5. Job runner: checks the job's dependency (JOB-02 succeeded for D); if not met, records WAITING and stops.
6. Job runner: records the run start through the P1 job monitor, runs the job body, records the end with status SUCCEEDED or FAILED and the counts.
7. Job runner: on service start, for each business date of a passed COLLINS load with no successful run of JOB-03 or JOB-04, runs the job for that date in date order, up to `jobs.catch-up.max-dates` dates.
8. Deadline watcher: at 07:00 checks JOB-03 for the current business date; if it has not succeeded, alerts the operations channel.
9. Platform administrator: reads runs on SCR-44 and reruns a failed run through `POST /admin/jobs/{jobId}/rerun`.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A run for the job and business date already succeeded | The run is skipped and recorded as a skip | None | AC3 |
| X2 | A timer check run is still going when the next one is due | The next fire waits; never two at once | None | AC4 |
| X3 | More missed dates than the catch-up limit | No automatic catch-up; an alert names the dates | MSG-P3-031 | AC6 |
| X4 | JOB-02 has not succeeded for the date | JOB-03 waits and is recorded WAITING | MSG-P3-031 | AC7 |
| X5 | The instance running a job stops part way | Another instance recovers the job and runs it again for the date | None | AC8 |
| X6 | JOB-03 has not succeeded by 07:00 | Alert to the operations channel within 15 minutes | MSG-P3-031 | AC9 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the ACE scheduler and the P1 job monitor; job bodies come from their own stories |
| Negotiable | Schedules, the catch-up limit and the deadline are data |
| Valuable | Allocation, timers and reconciliation run once a day per date, even after an outage |
| Estimable | One job runner, one catch-up step, one deadline check, three job registrations |
| Small | Fits in one sprint with its tests |
| Testable | Two-instance tests against a PostgreSQL test container with a controlled clock |

### 7. Acceptance criteria

```gherkin
Feature: Scheduled jobs on Quartz

  Background:
    Given two service instances "ACE-1" and "ACE-2" share the clustered Quartz job store
    Given the COLLINS load for business date 2026-12-02 passed its checks at 05:20 and JOB-02 succeeded at 05:50

  Scenario: AC1 Runs once
    When the morning allocation is due for business date 2026-12-02
    Then JOB-03 runs once, on one of the two instances
    Then the system logs its run with job "JOB-03", business date 2026-12-02, instance, start, end, status "SUCCEEDED" and the case counts

  Scenario: AC2 Missed run
    Given both instances were down from 04:30 to 09:40 on 2026-12-02
    When the service restarts at 09:40
    Then JOB-03 and JOB-04 run for business date 2026-12-02 after JOB-02 succeeds for that date
    Then the system logs each run with MSG-P3-030 naming the job and 2026-12-02

  Scenario: AC3 Repeated run for the same date
    Given JOB-03 succeeded for business date 2026-12-02
    When JOB-03 is fired again for 2026-12-02
    Then the system allocates no case again
    Then the run log records a skip for JOB-03 and 2026-12-02

  Scenario: AC4 Timer check does not overlap
    Given a JOB-05 run that started at 10:00 takes 7 minutes
    When the 10:05 fire is due
    Then the 10:05 run starts only after the 10:00 run ends
    Then no two JOB-05 runs are in progress at the same time

  Scenario: AC5 Several missed dates
    Given COLLINS loads passed for business dates 2026-12-02, 2026-12-03 and 2026-12-04 while both instances were down
    When the service restarts on 2026-12-04 at 11:00
    Then JOB-03 runs for 2026-12-02, then 2026-12-03, then 2026-12-04
    Then the system logs each run with its business date

  Scenario: AC6 More missed dates than the limit
    Given 7 business dates with passed COLLINS loads and no JOB-03 run
    When the service restarts
    Then no automatic catch-up run starts
    Then an alert with MSG-P3-031 names JOB-03 and the 7 dates

  Scenario: AC7 Dependency not met
    Given JOB-02 failed for business date 2026-12-03
    When JOB-03 is due for 2026-12-03
    Then JOB-03 does not run and its run is recorded "WAITING" with MSG-P3-031 naming "JOB-02"
    Then when JOB-02 succeeds for 2026-12-03 at 08:10 JOB-03 runs for 2026-12-03

  Scenario: AC8 Instance stops part way
    Given JOB-04 is running for 2026-12-02 on "ACE-1"
    When "ACE-1" stops
    Then "ACE-2" runs JOB-04 again for 2026-12-02 within the cluster check-in interval of 20 seconds
    Then the run log shows one "FAILED" run on "ACE-1" and one "SUCCEEDED" run on "ACE-2"

  Scenario: AC9 Allocation late
    Given JOB-03 for 2026-12-02 has not succeeded at 07:00
    When the deadline check runs at 07:00
    Then an alert with MSG-P3-031 naming JOB-03, 2026-12-02 and 07:00 reaches the operations channel by 07:15
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Each daily job runs once per business date, on one instance | batch.txt Jobs; REQ-CWC-007 |
| BR2 | JOB-03 and JOB-04 run after JOB-02 succeeds for the same business date | batch.txt Jobs and Daily timeline |
| BR3 | JOB-03 completes by 07:00; a later completion raises an alert | NFR-013; batch.txt JOB-03 |
| BR4 | JOB-05 runs every 5 minutes and a missed fire is not repeated; the next run picks up missed timers | batch.txt JOB-05 |
| BR5 | After an outage, each missed business date runs in date order, up to the catch-up limit (assumed 5; DL11) | batch.txt "If it fails or runs late" |
| BR6 | A run for a job and business date that already succeeded has no further effect | R-UNI-40; events.txt Rules |
| BR7 | Every scheduled job has a run book, monitoring and an alert to the operations channel | NFR-067; NFR-068 |
| BR8 | Job bodies are idempotent for their business date | R-UNI-40 |

### 9. State transitions

None. This story does not change a case status. It changes job run statuses in the P1 job monitor: STARTED to SUCCEEDED or FAILED, WAITING when the dependency is not met, and SKIPPED when the date already succeeded.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Reads runs and reruns a failed run (Platform administration CRUD) |
| RW-DATASTEW, data steward | Reads runs; owns JOB-04 (Platform administration R) |
| RW-TEAMMGR, team manager | Owns JOB-03 per batch.txt; is told by the allocation summary (RWB-E1-020) |
| SY-CASEWF, case workflow module | Runs JOB-03 and JOB-05 |
| SY-DATALOAD, data load from COLLINS | Runs JOB-04 inputs from the COLLINS load |

### 11. Data

No business field. The story writes the job run log of the P1 job monitor through its published interface and uses the `QRTZ_` tables of the ACE common module. Neither is in the Logical Data Model. The job bodies read and write their own fields in their own stories.

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Jobs**

| Item | JOB-03 Morning allocation | JOB-04 Daily reconciliation | JOB-05 Timer check |
|---|---|---|---|
| Trigger | LoadCompleted (EV-26) for D and JOB-02 succeeded for D | LoadCompleted (EV-26) for D and JOB-02 succeeded for D | Cron `0 0/5 * * * ?`, Asia/Bangkok |
| Schedule | Daily after JOB-02, by 07:00 | Daily after JOB-02 | Every 5 minutes |
| Input | New cases of D | Accounts at 90 days past due in the load of D and open cases | Timers with `expires_at` or `warn_at` before now |
| Output | Cases placed and owners given (RWB-E1-020) | Reconciliation breaks (RWB-E1-011) | Warnings, escalations, timer events (RWB-E1-028) |
| Events published | CaseAllocated (EV-02), CaseAllocationFailed (EV-03), by the job body | None | TimerDue (EV-18), TimerBreached (EV-19), by the job body |
| Idempotency key | Job ID and business date | Job ID and business date | Job ID and fire time slot |
| Restart behavior | Catch-up per missed date; recovery on another instance | Catch-up per missed date; recovery on another instance | Missed fires not repeated; the next run picks up |

**GET /api/recovery/v1/admin/jobs** (P1) lists runs (`Job[]`: `id`, `type`, `businessDate`, `status`, `startedAt`, `endedAt`, `checks`). Platform administration R. Errors 401, 403 (MSG-P4-002), 503.

**POST /api/recovery/v1/admin/jobs/{jobId}/rerun** (P1) reruns a FAILED or WAITING run for its business date. Platform administration U. Errors 401, 403 (MSG-P4-002), 404 (MSG-P4-003), 409 the run already succeeded (MSG-GEN-004), 503. Idempotent: a rerun of a run that succeeded returns 409 and runs nothing.

**Published interface** (package `recovery.casewf.scheduling.api`):

```java
public interface BusinessDateJob {
    String jobId();                              // for example "JOB-03"
    List<String> dependsOn();                    // for example ["JOB-02"]
    JobOutcome run(LocalDate businessDate);      // idempotent for the business date
}

// P1 job monitor, RWB-E1-056
UUID JobRunRecorder.start(String jobId, LocalDate businessDate, String instance);
void JobRunRecorder.finish(UUID runId, String status, Map<String, Object> counts);
Optional<JobRun> JobRunRecorder.lastSucceeded(String jobId, LocalDate businessDate);
```

**Quartz configuration** (from the ACE pattern):

```properties
org.quartz.jobStore.class=org.springframework.scheduling.quartz.LocalDataSourceJobStore
org.quartz.jobStore.driverDelegateClass=org.quartz.impl.jdbcjobstore.PostgreSQLDelegate
org.quartz.jobStore.isClustered=true
org.quartz.jobStore.clusterCheckinInterval=20000
org.quartz.scheduler.instanceId=AUTO
```

### 13. Solution plan

**Package.** `recovery.casewf.scheduling` in the recovery module; run books in `recovery/docs/runbooks/JOB-03.md`, `JOB-04.md` and `JOB-05.md`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BusinessDateJobRunner | Job | Quartz job marked `@DisallowConcurrentExecution` and `requestsRecovery`; runs a `BusinessDateJob` with the skip, dependency and run log steps |
| DailyJobTrigger | Listener | Consumes LoadCompleted and the JOB-02 completion; schedules JOB-03 and JOB-04 for the date |
| CatchUpOnStart | Service | On start, finds business dates with a passed load and no successful run; runs them in order up to the limit; alerts beyond it |
| DeadlineWatcher | Job | Cron at 07:00 Asia/Bangkok; alerts when JOB-03 has not succeeded for the business date |
| RecoveryJobRegistry | Service | Schedules JOB-03, JOB-04 and JOB-05 with their triggers and misfire instructions (JOB-05: do nothing) |
| RunBookCheck | Job | Build check that each scheduled job ID has a run book with the six headings: purpose, schedule, owner, failure signs, restart steps, escalation |
| BusinessDateJob | Published interface | The interface in section 12, implemented by the job bodies of RWB-E1-020, RWB-E1-011 and RWB-E1-028 |

**Database.** No new recovery table. Uses the `QRTZ_` tables of the ACE scheduler and the P1 job run log through `JobRunRecorder`.

**Configuration and reference data.** `jobs.catch-up.max-dates` = 5 (assumed; DL11), `jobs.allocation.deadline` = 07:00, `jobs.timer-check.cron` = `0 0/5 * * * ?`, all in the configuration service, loaded by the platform administrator. Job owners from batch.txt in each run book.

**Build steps**

1. Build `BusinessDateJobRunner` with the skip and dependency checks and the run log calls; test with a fake job body.
2. Build `RecoveryJobRegistry` and schedule the three jobs; prove JOB-05 does not overlap.
3. Build `DailyJobTrigger` on LoadCompleted and the JOB-02 completion.
4. Build `CatchUpOnStart` with the date order and the limit.
5. Build `DeadlineWatcher` and the alert through the job monitor.
6. Write the three run books and `RunBookCheck`.
7. Write the two-instance tests in section 16 with a controlled clock.

**Feature flag.** `rwb.p3.quartz-jobs`. Off: the three jobs are not scheduled and the job bodies can be run only through the rerun endpoint.

**Done when.** The tests in section 16 pass, and SIT shows one SUCCEEDED run of JOB-03 and JOB-04 per business date for five days in a row with JOB-03 complete by 07:00.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P3-030 | A job ran for a date after a missed run | {job} ran for {date} after a missed run. |
| MSG-P3-031 | A job waits on a dependency, misses its deadline, or has more missed dates than the catch-up limit | {job} for {date} has not completed: {reason}. |
| MSG-P4-002 | A role without Platform administration reads or reruns a job | You cannot {action} here. Your role does not include it. |

MSG-P3-030 and MSG-P3-031 are new (see Additions). They show on SCR-44 and in the operations channel.

### 15. Screens and states

SCR-44 Interface and job monitor, states Running, Failed and Complete: the platform administrator reads each run of JOB-03, JOB-04 and JOB-05 with its business date and status and reruns a failed run. No new screen in this story.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-007-01 | AC1, BR1 | System | Two instances, business date 2026-12-02 |
| TC-TE-007-02 | AC2, BR2, BR5 | System | Outage 04:30 to 09:40 on 2026-12-02 |
| TC-TE-007-03 | AC3, BR6, BR8 | System | JOB-03 fired twice for one date |
| TC-TE-007-04 | AC4, BR4 | System | JOB-05 run of 7 minutes |
| TC-TE-007-05 | AC5, BR5 | System | Three missed business dates |
| TC-TE-007-06 | AC6, BR5 | System | Seven missed business dates |
| TC-TE-007-07 | AC7, BR2 | System | JOB-02 failed for 2026-12-03, then succeeded at 08:10 |
| TC-TE-007-08 | AC8 | System | ACE-1 stopped during JOB-04 |
| TC-TE-007-09 | AC9, BR3 | System | JOB-03 not complete at 07:00 |
| TC-TE-007-11 | Access | Access | RW-CASEOWN (no Platform administration right) calls `GET /admin/jobs`; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code. Schedules, limits and deadlines come from the configuration service.
- No personal data in job logs, run books, alerts, tests or prompts. Logs carry job IDs, dates and counts.
- No read of another module's tables. The job run log is written through the P1 interface; the Quartz tables are used only through the ACE scheduler API.
- A job body never decides its own business date from the clock; it takes the date it is given.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-CWC-007 | Every new case placed in a queue and assigned by rule | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-40 | TC-TE-007-01 to TC-TE-007-03, TC-TE-007-05 to TC-TE-007-07, TC-TE-007-09 |
| REQ-CWC-011 | Service levels held as data and a breach raises an event | Business Requirements Epic 1, section 3.3; Program, section 5.3 | None (technical enabler) | All recovery processes | R-UNI-30 | TC-TE-007-04, TC-TE-007-11 |
| REQ-RDF-007 | The case list reconciles daily to the ALS count | Business Requirements Epic 1, section 4; Program, sections 5.1 and 6.3 | None (technical enabler) | All recovery processes | CTL-01 | TC-TE-007-08 |

### 19. Out of scope

- The job bodies: allocation (RWB-E1-020), reconciliation (RWB-E1-011), timer check (RWB-E1-028).
- The COLLINS load and case creation jobs JOB-01 and JOB-02 (P1).
- Daily rebalancing JOB-06 (RWB-E1-030).
- The job monitor screen and the operations alert channel (RWB-E1-056).


---

## RWB-TE-008 Decision log hash chain check

| Item | Value |
|---|---|
| Story key | RWB-TE-008 |
| Epic | E1, release 30 November 2026 |
| Module | P7 Decision center and log |
| Feature | None |
| Requirement IDs | REQ-DRI-003 |
| BRD section | Business Requirements Epic 1, section 3.7; Business Requirements Program, sections 5.7 and 6.6 |
| L3 process | 17 Run the decision center |
| Decision | None |
| Priority | Must |
| Depends on | RWB-E1-008, RWB-TE-007 |
| Status | Ready for build |

### 1. Story

As an **internal auditor (RW-AUDIT)**, I want **a nightly job that recomputes the whole decision log hash chain, records the result with the last hash, and reports a break to Compliance the same day**, so that **a changed entry is found the day it happens and the log can be relied on in audit**.

### 2. Business rationale

The decision log is evidence only while nobody can change an entry unseen. The database refuses updates and deletes (RWB-E1-008), but a change made outside the service, for example by a database administrator, is found only by recomputing the chain. This story runs that check as JOB-14 every night after the decision log copy, records each run with its last hash, and tells Compliance of a break, an incomplete run or an intact chain. It meets REQ-DRI-003 and NFR-035 and supports control CTL-06. The measure is a daily check with a same-day report: target 100 percent of nights.

### 3. Preconditions

- RWB-E1-008 is done: HashChainVerifier, CanonicalEntryForm and ChainBreakNotifier exist.
- RWB-TE-007 is done: jobs run on Quartz in the ACE service with job run records shown by GET /admin/jobs.
- JOB-13 Decision log copy is scheduled nightly at 01:00 (RWB-E1-014).
- Parameters in the catalog: rwb.decision.chaincheck.start=02:00, rwb.decision.chaincheck.latest-start=04:00, rwb.decision.chaincheck.batch-size=1000, all Asia/Bangkok (assumed; owner RW-COMPLY).
- The Compliance and PDPA officer group and the platform administrator group are set in the ACE notification path.

### 4. Flow

1. Quartz: fires JOB-14 at 02:00 Asia/Bangkok for the business date of the previous day.
2. Job (HashChainCheckJob): checks that JOB-13 for the same business date has ended; if not, waits and checks again every 5 minutes until 04:00, then runs and records that JOB-13 had not ended.
3. Job: reads the highest chain_seq at the start and fixes it as the end of the run; entries appended later are checked the next night.
4. Job: calls HashChainVerifier over chain_seq 1 to the end in batches of 1,000, recomputing each entry_hash and checking each prev_hash.
5. Job: counts every entry that fails and keeps the first.
6. Job: writes the job run record with type JOB-14, business date, status and checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count.
7. Job: sends MSG-P7-007 to Compliance when the chain is intact, or MSG-P7-008 with an incident when it is broken.
8. Job: on an error that stops the run, records status FAILED, alerts the platform administrator and sends MSG-P7-013 to Compliance.
9. Platform administrator: can rerun the job for the business date from the job monitor; a rerun is a new run record.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | An entry does not match its hash or its prev_hash | Run result BROKEN; first break and failing count recorded; incident; Compliance told | MSG-P7-008 | AC2, AC7 |
| X2 | The run stops on an error, for example a lost database connection | Status FAILED; platform administrator alerted; Compliance told the check did not complete | MSG-P7-013 | AC3 |
| X3 | The job is rerun for the same business date | A new run record with the same checks; the report says it is a rerun; no second scheduled run starts | MSG-P7-007 or MSG-P7-008 | AC4 |
| X4 | The log is empty | Result INTACT with count 0 and the genesis hash | MSG-P7-007 | AC5 |
| X5 | JOB-13 has not ended at 02:00 | The job waits up to 04:00, then runs and records the late copy | MSG-P7-007 or MSG-P7-008 | AC6 |
| X6 | Entries are appended while the job runs | They are outside this run and are checked the next night | None | AC8 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Uses the verifier from RWB-E1-008 and the scheduler from RWB-TE-007 |
| Negotiable | Start times and batch size are parameters |
| Valuable | A changed entry is found by the morning after it is changed |
| Estimable | One Quartz job, one report, no screen |
| Small | Fits in one week with its tests |
| Testable | Each criterion below is one test in section 16 |

### 7. Acceptance criteria

```gherkin
Feature: Decision log hash chain check

  Background:
    Given the environment is SIT with the synthetic decision log
    Given JOB-13 for business date 2 December 2026 ended at 01:40 on 3 December 2026

  Scenario: AC1 Chain intact
    Given the decision log holds 48,210 entries and none has been changed
    When JOB-14 runs at 02:00 on 3 December 2026
    Then the job run record shows type "JOB-14", business date 2 December 2026, status "COMPLETED" and result "INTACT"
    Then its checks hold entries checked 48,210, last chain_seq 48,210 and that entry's entry_hash
    Then MSG-P7-007 with the count and the last hash is sent to the Compliance group

  Scenario: AC2 Break
    Given the actions of the entry with chain_seq 30,005 were changed in the SIT database with the trigger disabled
    When JOB-14 runs
    Then the run result is "BROKEN" with first break chain_seq 30,005 and its entry ID
    Then the system raises an incident and MSG-P7-008 with the entry ID is sent to the Compliance group before 08:00 on 3 December 2026

  Scenario: AC3 A run that stops is reported
    Given the database connection is closed in the test double after 20,000 entries
    When JOB-14 runs
    Then the run status is "FAILED" with entries checked 20,000
    Then the system alerts the platform administrator group
    Then the system sends MSG-P7-013 to the Compliance group with the date of the last complete check, 2 December 2026

  Scenario: AC4 A rerun gives a new record and no second scheduled run
    Given JOB-14 for business date 2 December 2026 failed at 02:20
    When test user "U-9301" holding RW-PLATADM reruns it from the job monitor at 08:30
    Then a second run record for business date 2 December 2026 is written with rerun true
    Then the system marks the report to Compliance as a rerun
    Then while the rerun is running a second start of JOB-14 is refused by the scheduler

  Scenario: AC5 An empty log is intact
    Given the decision log holds no entry
    When JOB-14 runs
    Then the result is "INTACT" with entries checked 0 and last hash of 64 zeros

  Scenario: AC6 The job waits for the decision log copy
    Given JOB-13 for business date 2 December 2026 is still running at 02:00 and ends at 02:25
    When JOB-14 fires at 02:00
    Then it starts the check at 02:25 and records the JOB-13 end time
    Then if JOB-13 has not ended by 04:00 the check starts at 04:00 with the note "JOB-13 not ended"

  Scenario: AC7 Several changed entries
    Given the entries with chain_seq 12,001 and 40,350 were changed in the SIT database
    When JOB-14 runs
    Then the first break is chain_seq 12,001 and the failing count is 2
    Then one incident and one MSG-P7-008 report name both entry IDs

  Scenario: AC8 Entries written during the run
    Given the log holds 48,210 entries when JOB-14 starts
    Given 37 entries are appended while it runs
    When the run ends
    Then entries checked is 48,210 and last chain_seq is 48,210
    Then the next night's run checks 48,247 entries
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The whole chain is recomputed every night and a break is reported to Compliance the same day | REQ-DRI-003; NFR-035; JOB-14 |
| BR2 | Each entry's entry_hash is recomputed from the canonical form and its prev_hash compared with the entry before | RWB-E1-008, BR3 and BR4 |
| BR3 | A run covers chain_seq 1 to the highest chain_seq at its start | This story |
| BR4 | JOB-14 runs after JOB-13 for the same business date, starting no later than 04:00 | batch.txt, daily timeline; parameters rwb.decision.chaincheck.* |
| BR5 | A run that does not complete is reported to Compliance with the date of the last complete check | NFR-035 |
| BR6 | Only one run of JOB-14 is active at a time; a rerun is a new run record | RWB-TE-007; job run record |
| BR7 | Start times and batch size are parameters, not code | Principle 1 |

### 9. State transitions

None. This story does not change a case status. A JOB-14 run moves from Waiting (for JOB-13) to Running, then to Completed with result INTACT or BROKEN, or to Failed.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-DECLOG Decision log writer | The job runs under this service identity and reads the log (Decision log C and read through the store) |
| RW-COMPLY Compliance and PDPA officer | Receives every report; owns the job (batch.txt) and its parameters |
| RW-AUDIT Internal audit | Reads the run records (Platform administration R); may not rerun |
| RW-PLATADM Platform administrator | Receives failure alerts; reruns the job (Platform administration U) |
| RW-SECADM Security administrator | Receives the break incident with Compliance |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Read |
| DF-DEC-028 | decision_log_entry | chain_seq | Read |
| DF-DEC-030 | decision_log_entry | actor_user_id | Read |
| DF-DEC-029 | decision_log_entry | corrects_entry_id | Read |

Field IDs are those in the Logical Data Model and Data Dictionary. The run result is written to the ACE job run record (Job schema), not to a recovery table.

### 12. Contract

| Item | Value |
|---|---|
| Trigger | Quartz cron 0 0 2 * * ? in Asia/Bangkok, after JOB-13 for the same business date |
| Job name | JOB-14 Hash chain check |
| Schedule | Nightly 02:00; latest start 04:00 |
| Input | decision_log_entry in chain_seq order, chain_seq 1 to the highest at start |
| Output | Job run record: type JOB-14, businessDate, status, startedAt, endedAt, checks (entriesChecked, lastSeq, lastHash, result, breakSeq, breakEntryId, failingCount, rerun, copyJobEndedAt); reports MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group; incident on a break |
| Events published | None from events.txt; the report goes through the ACE notification path |
| Idempotency key | Business date plus run number; a rerun adds a record and changes nothing else |
| Restart | A failed run is not resumed; a rerun starts again from chain_seq 1 |

**GET /api/recovery/v1/admin/jobs** (owned by P1): lists JOB-14 runs; Platform administration R. **POST /api/recovery/v1/admin/jobs/{jobId}/rerun** (owned by P1): reruns; Platform administration U; errors 401, 403 (MSG-P4-002), 404, 409 when a run is active (MSG-GEN-004).

### 13. Solution plan

- Package: folder `recovery/decision/log` in the recovery module; Java package `recovery.decision.log`.
- Components:

| Component | Type | Responsibility |
|---|---|---|
| HashChainCheckJob | Job | Quartz job with DisallowConcurrentExecution; waits for JOB-13; fixes the end chain_seq; runs the verifier; writes the run record |
| HashChainVerifier | Service | From RWB-E1-008; extended to count every failing entry and continue after the first |
| ChainCheckReporter | Service | Sends MSG-P7-007, MSG-P7-008 or MSG-P7-013 to the Compliance group; raises the incident on a break |
| JobRunRecorder | Service | Writes the ACE job run record through the scheduler interface of RWB-TE-007 |

- Database: reads decision_log_entry by chain_seq using its unique index; no table of its own.
- Configuration and reference data: parameters rwb.decision.chaincheck.start, latest-start and batch-size (RW-COMPLY); Compliance and platform administrator groups in the ACE notification path; job entry JOB-14 in the job catalog and its run book (RWB-E1-056).
- Build steps:
  1. Add JOB-14 to Quartz with the cron, time zone and no concurrent execution.
  2. Build the wait for JOB-13 with the 04:00 latest start; test AC6 with a fixed clock.
  3. Extend HashChainVerifier to count all failing entries; tests for AC2 and AC7.
  4. Build the run record and the fixed end chain_seq; tests for AC1, AC5 and AC8.
  5. Build ChainCheckReporter with the three messages; tests for AC1, AC2 and AC3.
  6. Test the rerun path and the concurrency guard for AC4.
  7. Run the timing check on 10 million synthetic entries against a 60 minute budget (assumed; DL11).
- Feature flag: `rwb.decision.hash-check`.
- Done when: the tests in section 16 pass and the run book for JOB-14 is in the job monitoring (RWB-E1-056).

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-007 | The chain is intact (new) | The decision log check for {date} passed: {count} entries checked. The last hash is {hash}. |
| MSG-P7-008 | The chain is broken | The decision log check for {date} found a break at entry {entryId}. Entries from that entry on cannot be relied on until Compliance reviews them. |
| MSG-P7-013 | The run did not complete (new) | The decision log check for {date} did not complete. The chain was last confirmed on {lastDate}. |
| MSG-P4-002 | Rerun without Platform administration U | You cannot {action} here. Your role does not include it. |

Thai text for each message follows DL10; proposed Thai for the new messages is in the additions file.

### 15. Screens and states

No screen in this story. Run records show on the job monitor through GET /admin/jobs (SCR-44 Interface and job monitor from Epic 2); Compliance receives each report by the ACE notification path.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-008-01 | AC1, BR1, BR2 | System | 48,210 synthetic entries, none changed |
| TC-TE-008-02 | AC2, BR1 | System | One entry changed in SIT with the trigger disabled |
| TC-TE-008-03 | AC3, BR5 | System | Connection closed after 20,000 entries |
| TC-TE-008-04 | AC4, BR6 | System | Failed run, then a rerun at 08:30 |
| TC-TE-008-05 | AC5 | System | Empty log |
| TC-TE-008-06 | AC6, BR4 | System | JOB-13 ending at 02:25; JOB-13 not ended by 04:00 |
| TC-TE-008-07 | AC7, BR2 | System | Two entries changed |
| TC-TE-008-08 | AC8, BR3 | System | 37 entries appended during the run |
| TC-TE-008-09 | Access | Access | A role without the right is refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: times and batch size are parameters.
- No personal data in logs, tests or prompts; reports name entry IDs and chain_seq only.
- No read of another module's tables; the job reads only decision_log_entry.
- The job never writes to decision_log_entry and never repairs an entry.
- One canonical form implementation, shared with the store.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-003 | Hash chain checked every day, break reported to Compliance the same day | Epic 1, 3.7 | FEAT-DRI-01 (store this job checks) | 17 Run the decision center | BR1 to BR7 | TC-TE-008-01 to TC-TE-008-09 |

### 19. Out of scope

- The store, the hash computation and the on-demand verifier (RWB-E1-008).
- The check of each entry returned by an audit query (RWB-E2-005).
- The decision log copy to the data lake (RWB-E1-014, JOB-13).
- Detecting a broken chain as a control breach through the administration screens (Epic 8, FEAT-ADM-10).


---

## RWB-TE-009 Performance test harness

| Item | Value |
|---|---|
| Story key | RWB-TE-009 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-OCC-007, REQ-WKM-002 |
| BRD section | Business Requirements Program, section 6.1 and section 6.2 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-TE-004 |
| Status | Ready for build |

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a load test at the busiest-hour volume, run in SIT before each release, that fails the release stage when a screen request is too slow**, so that **response targets are proven before users feel them**.

### 2. Business rationale

About 370 staff and 50 partner users are online in the busiest hour (NFR-002, NFR-003), and every screen must respond in under 2 seconds (NFR-008). A screen that is fast with ten testers can be slow with four hundred users on 23,600 cases. The harness runs the busiest hour on masked SIT data before each release and stops the release stage when a target is missed. It proves the response of the case record view (REQ-OCC-007) and the team manager's case list (REQ-WKM-002) under load. The measure is the 95th percentile response time per screen request in the busiest hour.

### 3. Preconditions

- RWB-TE-004 is done: SIT holds the masked copy with at least 23,600 open cases (NFR-001).
- SIT has named test users for each role in the operation mix (roles.txt key: test users before the release that gives a role real users), with Entra ID groups per DL40.
- An SIT deployment slot is booked for the run (DL35).
- The operation mix file and the pass criteria are loaded in the harness configuration: 410 virtual users at 3 requests a minute each; 95th percentile under 2,000 ms per operation; error rate under 1 percent (assumed; DL11).
- The build under test is deployed to SIT with its feature flags as planned for the release.

### 4. Flow

1. Release pipeline: starts the SIT performance stage for the build, or a squad member starts it by hand.
2. Harness: takes the SIT run lock; refuses to start when another run holds it.
3. Harness: counts open cases through GET /api/recovery/v1/cases and refuses to start when fewer than 23,600 are found.
4. Harness: signs in the test users for each role in the mix.
5. Harness: ramps to 410 virtual users over 10 minutes, then holds 60 minutes at 3 requests a minute per user, following the weights in the mix file.
6. Harness: records the response time and status of each request; 403 responses on operations the mix marks as refusals count as expected.
7. Harness: computes the 50th, 95th and 99th percentiles, the throughput and the error rate per operation over the 60 steady minutes.
8. Gate: passes when every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent; otherwise fails the stage.
9. Harness: attaches the report to the release record with the build ID, releases the lock and triggers the reload of the masked copy.

### 5. Exception paths

None.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the masked SIT data of RWB-TE-004 and a deployed build |
| Negotiable | Mix, user count and pass criteria are configuration (DL11) |
| Valuable | A slow screen is found in SIT, not by 410 users in production |
| Estimable | One load script, one mix file, one gate, one report |
| Small | Fits in one sprint with its tests |
| Testable | The gate is tested with result fixtures; the run is tested in SIT |

### 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The load is 410 concurrent users at 3 requests a minute each, the busiest hour of staff and partner users | NFR-002; NFR-003; current story value |
| BR2 | Each screen request responds under 2,000 ms at the 95th percentile; 2,000 ms fails | NFR-008; DL11 |
| BR3 | The error rate over the steady period is under 1 percent; expected 403 refusals are not errors | DL11 (assumed) |
| BR4 | The run uses at least 23,600 open cases of masked data | NFR-001; NFR-045 |
| BR5 | The operation mix, user count and limits are read from the harness configuration, never from the script | Principle 1 applied to test configuration |
| BR6 | One run at a time in SIT; the latest run for a build decides the gate | DL35 |

### 9. State transitions

None. This story does not change a case status. It changes the state of the SIT performance stage: running, passed or failed.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Start a run, change the mix file through a reviewed pull request, read reports |
| RW-PLATADM, platform administrator | Books the SIT slot and reloads the masked copy after the run |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-PHONECOL | Make the simulated requests with their own rights |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-CAS-010 | recovery_case | queue_id | Read |
| DF-WRK-001 | queue | id | Read |
| DF-INT-001 to DF-INT-013 | interaction | all fields | Write, SIT only, by postCasesCaseidInteractions |

The harness reads and writes only through the API. SIT data is reloaded from the masked copy after each run. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

| Item | Value |
|---|---|
| Trigger | The SIT performance stage of the release pipeline before the UAT exit, or a manual start |
| Operations exercised | getCases, getCasesCaseid, getCasesCaseidTimeline, getCasesCaseidInteractions, getQueuesQueueidCases, getCasesCaseidDocuments and postCasesCaseidInteractions on /api/recovery/v1; postCasesCaseidTransfer as the expected refusal for RW-PHONECOL |
| Input | Mix file, user counts and limits; the list of test users per role; case and queue IDs read at start |
| Output | Report per operation: count, 50th, 95th and 99th percentiles, throughput, errors; gate result; build ID; mix file version |
| Schedule | Ramp 10 minutes, steady 60 minutes, measured on the steady period only |
| Idempotency | Each run has its own run ID; a rerun adds a report and replaces the gate result for the build |
| Restart | A run stopped part way is marked failed; the lock is released after 90 minutes at most |

This is a pipeline stage, not a scheduled Workbench job; it has no entry in the job list.

### 13. Solution plan

**Package.** Folder `perf/recovery` in the ACE repository, Java package `<ACE base package>.recovery.perf`. Not part of the deployed service.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| BusiestHourSimulation | Job | Load script: sign-in, ramp, steady period, weighted operations |
| mix file | Rule table | Operation, weight, role, expected status |
| perf settings | Rule table | User count, request rate, durations, limits |
| DataVolumeCheck | Service | Counts open cases before the run (BR4) |
| RunLock | Service | One run at a time in SIT (BR6) |
| PerformanceGate | Service | Evaluates the result against the limits (BR2, BR3) |
| ReportPublisher | Service | Attaches the report and the gate result to the release record |

**Database.** None directly. The harness uses the API only.

**Configuration and reference data.** Mix file and settings in `perf/recovery/config` (assumed values in section 3; DL11), owned by the TechX tech leads through code owners. Test users per role from the SIT identity set (DL40).

**Build steps**

1. Write PerformanceGate with unit tests from result fixtures for the boundary and the error rate (AC2, AC3).
2. Write DataVolumeCheck and RunLock (AC4, AC5).
3. Write BusiestHourSimulation reading the mix file and the settings (AC1, AC7).
4. Add the expected refusal for RW-PHONECOL on postCasesCaseidTransfer and count 403 as expected (access test).
5. Write ReportPublisher with the build ID and the latest-run rule (AC6).
6. Add the stage to the release pipeline before the UAT exit and run it once on the Epic 2 build.

**Feature flag.** None. The harness is a pipeline stage and does not ship in the service.

**Done when.** The tests in section 16 pass and the Epic 2 release record holds a passed report for the release build.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | 95th percentile at or above the limit | target missed: {operation} {p95} ms, limit {limit} ms |
| Report | Error rate at or above the limit | error rate above limit: {rate} percent |
| Report | Not enough data | data volume below the test base: {count} of {base} |
| Report | Lock held | run already in progress |
| MSG-P4-002 | Expected refusal for a role without the right | You cannot {action} here. Your role does not include it. |

Report text is for the release team and is not part of the message standard.

### 15. Screens and states

No screen in this story. The release team reads the report attached to the release record. The screens under load are SCR-02, SCR-03, SCR-04 and SCR-07 through their API calls.

### 16. Test cases

None.

### 17. Guardrails

- No business value in code: the mix, user counts and limits are configuration.
- No personal data in logs, tests or prompts; the run uses the masked copy and the report holds operation names and numbers only.
- No read of another module's tables; the harness uses the API only.
- The harness never runs against UAT or production.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | Business Requirements Program, section 6.2 | None | All recovery processes | None | None |
| REQ-WKM-002 | Team manager sees every team queue with filters | Business Requirements Program, section 6.2 | None | All recovery processes | None | None |

### 19. Out of scope

- Masked data in SIT and UAT: RWB-TE-004.
- Batch window timing of the daily jobs (NFR-013, NFR-019): the job stories, for example RWB-TE-007.
- Agent response times (NFR-010): the P10 agent runtime stories, for example RWB-TE-013.
- Production monitoring of response times: RWB-E1-056.


---

## RWB-TE-010 Browser and accessibility tests

| Item | Value |
|---|---|
| Story key | RWB-TE-010 |
| Epic | E2, release 31 December 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-OCC-007, REQ-WKM-001 |
| BRD section | Business Requirements Program, section 6.10 and section 6.11 |
| L3 process | All recovery processes |
| Decision | DL37 |
| Priority | Must |
| Depends on | RWB-TE-003 |
| Status | Ready for build |

### 1. Story

As a **squad member (RW-TRIBE)**, I want **browser tests and an accessibility scan on the main recovery screens, on the browsers the bank supports and in Thai and English, in every pipeline run**, so that **screens work for every user on the bank's browsers**.

### 2. Business rationale

Recovery staff work on Microsoft Edge and Google Chrome, some with screen readers or keyboard only, and in Thai or English. A screen that passes on one developer's browser can fail on the previous browser version or for a keyboard user, and that is found in UAT or by users. The browser runner tests the main screens on four browsers and scans them for WCAG 2.1 AA errors in both languages before merge. It proves the case record view (REQ-OCC-007) and my queue (REQ-WKM-001) against NFR-060, NFR-061 and NFR-059. The measure is the count of accessibility and browser defects found in UAT, with a target of zero.

### 3. Preconditions

- RWB-TE-003 is done: the front end uses the generated types and client.
- The browser test runner is in the ACE pipeline before the first SIT run (DL37).
- The runner image holds Chrome and Edge at the current and previous major versions, listed in `browsers.json` (NFR-061; DL11).
- A test deployment with the synthetic data set of RWB-E1-065 and test users per role.
- Screen labels exist in Thai and English in the message and label tables (DL10; Thai labels may show "Pending" until approved).

### 4. Flow

1. Pipeline: starts the browser stage after the front end build on each pull request, and nightly against SIT.
2. Runner: reads `browsers.json` and refuses to start when a listed browser is missing.
3. Runner: signs in the test user of each role in the screen list.
4. Runner: opens each main screen (SCR-02, SCR-03, SCR-04, SCR-05, SCR-07, SCR-09) in each listed state and runs its functional test on each browser.
5. Runner: runs the accessibility scan with the WCAG 2.1 A and AA rule tags on each screen and state, in Thai and in English.
6. Runner: runs the keyboard test: every primary action is reachable and usable by keyboard with a visible focus.
7. Runner: compares each violation with the exception list; an entry past its expiry date does not excuse the violation.
8. Runner: retries a failed functional test once and lists a test that passes only on retry as flaky.
9. Pipeline: fails the stage on any violation, functional failure or missing browser, and attaches the report.

### 5. Exception paths

None.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the generated client of RWB-TE-003 and the runner of DL37 |
| Negotiable | Browser versions, screens and exceptions are configuration files |
| Valuable | Users on every bank browser and with assistive technology can use the screens |
| Estimable | One test suite, one scan helper, two configuration files |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below uses one fixture screen or one browser setting |

### 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every main screen meets WCAG 2.1 level AA; any violation tagged WCAG 2.1 A or AA fails | NFR-060 |
| BR2 | Screens work on the current and previous major versions of Microsoft Edge and Google Chrome | NFR-061 |
| BR3 | Every screen is checked in Thai and in English | NFR-059; DL10 |
| BR4 | A violation is excused only by an exception list entry with an owner and an expiry date not yet passed | Principle 1 applied to test configuration |
| BR5 | A missing browser is a failure, never a skip | DL37 |
| BR6 | A failed functional test is retried once; a pass on retry is listed as flaky | Engineering practice |
| BR7 | A role without the right sees the refusal and no control for the action | CTL-09; MSG-P4-002 |

### 9. State transitions

None. This story does not change a case status. It changes the state of the browser stage: running, passed or failed.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the stage, add screens to the list, request an exception entry |
| TechX tech leads (code owners, RWB-TE-002) | Approve changes to the screen list, the browser list and the exception list |
| Test users of RW-CASEOWN, RW-TEAMMGR, RW-PLATADM and RW-PHONECOL | Open the screens with their own rights |
| No approval level from the delegation of authority applies | The story takes no business decision |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-002 | recovery_case | case_no | Read |
| DF-CAS-005 | recovery_case | status | Read |
| DF-REF-035 | role | role_code | Read |
| DF-REF-030 | lov_value | label_en | Read |
| DF-REF-031 | lov_value | label_th | Read |

The runner reads the synthetic data through the screens only. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

| Item | Value |
|---|---|
| Trigger | The browser stage on each pull request that changes the front end; nightly against SIT |
| Input | `browsers.json`, `screens.json` (screen ID, route, states, roles, primary actions), `a11y-exceptions.json` (screen, rule, owner, expiry, reason) |
| Output | Report per screen, state, language and browser: functional result, violations with rule and element, keyboard result, flaky list |
| Scan rules | WCAG 2.1 A and AA rule tags of the scan engine |
| Idempotency | The same commit and configuration give the same result, apart from tests listed as flaky |
| Restart | Rerun the stage; it holds no state |

This is a pipeline stage, not a scheduled Workbench job.

### 13. Solution plan

**Package.** Folder `ace-web/e2e/recovery` in TypeScript; configuration in `ace-web/e2e/recovery/config`.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| screens.json | Rule table | Screens, states, roles and primary actions under test |
| browsers.json | Rule table | Browser names and versions (BR2) |
| a11y-exceptions.json | Rule table | Excused violations with owner and expiry (BR4) |
| BrowserGuard | Service | Fails the stage when a listed browser is missing (BR5) |
| ScreenSuite | Service | Functional tests per screen and state, on each browser |
| AccessibilityScan | Service | Scan per screen, state and language with the WCAG 2.1 A and AA tags (BR1, BR3) |
| KeyboardCheck | Service | Tab order and focus on each primary action |
| ReportWriter | Service | The stage report and the flaky list (BR6) |

**Database.** None.

**Configuration and reference data.** The three configuration files, owned by the TechX tech leads; browser versions as listed in the runner image (DL37, DL11); labels in Thai and English from the label tables (DL10).

**Build steps**

1. Write BrowserGuard and browsers.json; prove a missing version fails (AC5).
2. Write the functional tests for the 6 screens from screens.json on the 4 browsers (AC3).
3. Write AccessibilityScan for both languages and the missing label check (AC1, AC2, AC4, AC7).
4. Write the exception list handling with expiry (AC6).
5. Write KeyboardCheck for the primary actions (AC8).
6. Add the single retry and the flaky list (AC9).
7. Add the refusal test for RW-PHONECOL on SCR-05 (access test) and add the stage to the pipeline.

**Feature flag.** None. The tests run in the pipeline and do not ship in the service.

**Done when.** The tests in section 16 pass and the pipeline shows the browser stage on every front end pull request.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Report | A violation | accessibility violation: {screen} {state} {language} {rule} {element} |
| Report | A missing browser | browser not available: {browser} {version} |
| Report | An expired exception | exception expired: {screen} {rule} since {date} |
| Report | A raw label key | missing label: {screen} {key} |
| Report | A keyboard failure | keyboard access: {screen} action {action} |
| MSG-P4-002 | The refusal shown to a role without the right | You cannot {action} here. Your role does not include it. |

Report text is for developers and is not part of the message standard.

### 15. Screens and states

Screens under test: SCR-02 Case list (Loading, Empty, List, Filtered), SCR-03 Case record (Loading, Read only, Editable, On hold), SCR-04 Case timeline (Loading, Filtered), SCR-05 Transfer case (Form, At cap warning, Saved), SCR-07 Team queues (Loading, List) and SCR-09 Exception queue (Loading, List). Developers read the report in the pipeline.

### 16. Test cases

None.

### 17. Guardrails

- No business value in code; screens, browsers and exceptions are configuration files.
- No personal data in logs, tests or prompts; tests use the synthetic data set and screenshots in the report show synthetic data only.
- No read of another module's tables; the runner uses the screens only.
- An exception entry always has an owner and an expiry date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-OCC-007 | The case record view shows the case on one screen | Business Requirements Program, section 6.11 | None | All recovery processes | None | None |
| REQ-WKM-001 | A case owner sees their own queue with ageing and service level state | Business Requirements Program, section 6.10 and section 6.11 | None | All recovery processes | None | None |

### 19. Out of scope

- Partner portal screens and tablets (NFR-063): the partner portal stories from RWB-E2-019.
- Thai label approval: DL10.
- Response times under load: RWB-TE-009.
- Screen design and layout: DL31.


---

## RWB-TE-011 PDPA lint for code, tests and logs

| Item | Value |
|---|---|
| Story key | RWB-TE-011 |
| Epic | E1, release 30 November 2026 |
| Module | P2 Integration |
| Feature | None |
| Requirement IDs | REQ-RDF-010, REQ-ACA-005 |
| BRD section | Business Requirements Program, section 6.7 and section 6.9 |
| L3 process | All recovery processes |
| Decision | None |
| Priority | Must |
| Depends on | RWB-TE-001 |
| Status | Ready for build |

### 1. Story

As a **squad member (RW-TRIBE)**, I want **a pipeline check that finds personal data in code, test fixtures, log statements and error messages, built from the data dictionary's list of personal fields**, so that **personal data never leaks into code or logs**.

### 2. Business rationale

Party names, identifier tokens, dates of birth, contact values and interaction summaries are personal data under PDPA. A log line that prints a party, or a test fixture copied from a real record, puts that data where masking does not apply: in log stores, in build artifacts and in prompts to coding agents. The lint reads the personal fields from the data dictionary and fails the build when code, fixtures, logs or error messages carry them. It meets REQ-RDF-010 and REQ-ACA-005 (personal data masked by role, which a log line bypasses) and the target NFR-054. The measure is the count of personal data findings merged to main, which must stay at zero.

### 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the pipeline checks exist.
- The data dictionary marks each personal field (the `is_personal` column of the metadata table sys_fields in the schema, and `x-personal-data: true` in the API specification).
- Synthetic test data uses the prefix "SYN-" for every value placed in a personal field (assumed convention of RWB-E1-065).
- The masking helper of the common module is available for the rare log line that must name a record (assumed published as part of the common module's PII logging interface).

### 4. Flow

1. Build: reads the personal fields from the sys_fields seed and the API specification.
2. Build: generates the lint rule set from the field list: Java getter names, entity class names, JSON property names and TypeScript property names.
3. Lint: scans `src/main` and the front end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.
4. Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.
5. Lint: checks that each entity with a personal field excludes it from its text form.
6. Lint: compares each finding with the allow list; an entry past its expiry does not excuse the finding.
7. Pipeline: fails the build on any finding and prints the rule, the file, the line and the field, without printing the value found.

### 5. Exception paths

None.

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the pipeline of RWB-TE-001 and the dictionary seed |
| Negotiable | Patterns, the synthetic prefix and the allow list are configuration |
| Valuable | Personal data stays out of logs, artifacts and prompts |
| Estimable | One rule generator, one rule set, one allow list, one pipeline step |
| Small | Fits in one sprint with its tests |
| Testable | Each criterion below is one fixture file with one finding |

### 7. Acceptance criteria

None. The former criteria covered development and delivery procedures and have been removed from the story set.

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The personal field list is read from the data dictionary and the API specification, never written in the lint | Logical Data Model, Personal data column; API x-personal-data |
| BR2 | No log statement, string built for a log, or exception message carries a personal field or a whole personal entity | NFR-054; CTL-11 |
| BR3 | Test fixtures, seeds and end-to-end data carry only synthetic values with the prefix "SYN-" in personal fields | NFR-045; RWB-E1-065 |
| BR4 | Literals matching a Thai national identifier with a valid check digit, a Thai mobile number or an email outside the example domains fail anywhere in code or tests | NFR-054 |
| BR5 | An entity with a personal field leaves it out of its text form | CTL-11 |
| BR6 | A finding is excused only by an allow list entry with an owner, a reason and an expiry date not yet passed | Principle 1 applied to build configuration |
| BR7 | The lint never prints the value it found | REQ-ACA-005 |

### 9. State transitions

None. This story does not change a case status. It changes the build result to failed when a finding is not excused.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-TRIBE, tribe lead and squad members | Run the lint; propose an allow list entry by pull request |
| TechX tech leads (code owners, RWB-TE-002) | Approve allow list changes and rule changes |
| RW-COMPLY, Compliance and PDPA officer | Owns which fields are personal through the data dictionary (DL26) |
| No Workbench capability area applies | The lint runs in the pipeline |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-PTY-002 | party | cif_no | Read (definition) |
| DF-PTY-004 | party | first_name | Read (definition) |
| DF-PTY-005 | party | last_name | Read (definition) |
| DF-PTY-007 | party | id_no_token | Read (definition) |
| DF-PTY-008 | party | date_of_birth | Read (definition) |
| DF-PTY-010 | party | vulnerable_flag | Read (definition) |
| DF-PTY-011 | party | deceased_flag | Read (definition) |
| DF-PTY-012 | party | bankruptcy_flag | Read (definition) |
| DF-PTY-016 | contact_point | value_token | Read (definition) |
| DF-INT-011 | interaction | summary | Read (definition) |
| DF-DOC-015 | document_field | field_value | Read (definition) |

The lint reads which fields are personal; it never reads their values. Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

| Item | Value |
|---|---|
| Trigger | Every pull request and every build of main |
| Input | The sys_fields seed in the schema (is_personal), the API specification, the source and test folders, `pdpa-allow.yaml` |
| Rule set | Generated `pdpa-rules.yaml` with rules PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID |
| Output | Pass, or fail with rule, file, line and field name for each finding |
| Allow list entry | rule, path, line or pattern, owner, reason, expiry date |
| Idempotency | The same commit and dictionary give the same findings |
| Restart | Rerun the pipeline; the lint holds no state |

### 13. Solution plan

**Package.** Folder `tools/pdpa-lint` in the ACE repository; rules applied to the recovery back end and front end folders.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| PersonalFieldReader | Service | Reads the personal fields from the schema seed and the API specification (BR1) |
| RuleGenerator | Service | Writes pdpa-rules.yaml with name variants: snake case, Java getter, camel case property |
| pdpa-rules.yaml | Rule table | The generated rules (BR2 to BR5) |
| pdpa-allow.yaml | Rule table | Allow list entries with owner and expiry (BR6) |
| CheckDigitMatcher | Service | Thai national identifier check digit test for BR4 |
| PdpaLintStep | Job | Pipeline step that runs the scan and prints findings without values (BR7) |

**Database.** None. The schema seed is read as a file.

**Configuration and reference data.** The synthetic prefix "SYN-" (assumed), the example email domains, the allow list; owned by the TechX tech leads through code owners. The personal field marks are owned by Compliance (DL26).

**Build steps**

1. Write PersonalFieldReader and RuleGenerator; test that a newly marked field appears in the rules (AC5).
2. Write the log, entity, exception and text form rules for Java and TypeScript with one fixture each (AC1, AC2, AC7, AC9, AC10).
3. Write the fixture rules and CheckDigitMatcher (AC3, AC4).
4. Add the masking helper exception to the log rules (AC8).
5. Write the allow list handling with expiry (AC6).
6. Add PdpaLintStep to the pull request pipeline and confirm it prints no value.

**Feature flag.** None. A build check has no runtime path to switch off.

**Done when.** The tests in section 16 pass and the lint runs on main with zero findings.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Build log | A finding | {rule}: {file}:{line} uses personal field {field}. Remove it or use the masking helper. |
| Build log | An expired allow entry | allow entry expired: {rule} {path} since {date} |
| Repository host | An allow list change without a code owner approval | Review required from code owners |

Build log text is for developers and is not part of the message standard.

### 15. Screens and states

No screen in this story. Developers read the findings in the pull request checks.

### 16. Test cases

None.

### 17. Guardrails

- No business value in code: the personal field list comes from the dictionary; patterns and the allow list are configuration.
- No personal data in logs, tests or prompts; the lint itself prints field names only, and its own check digit fixtures are generated at run time and never stored.
- No read of another module's tables; the lint reads files only.
- An allow list entry always has an owner and an expiry date.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-RDF-010 | Personal data is masked by role in line with PDPA | Business Requirements Program, section 6.7 | None | All recovery processes | None | None |
| REQ-ACA-005 | Personal data is masked by role on every screen and in every agent call | Business Requirements Program, section 6.9 | None | All recovery processes | None | None |

### 19. Out of scope

- Secret scanning and dependency approval in the pipeline (NFR-052, NFR-054): the ACE pipeline, outside the recovery backlog.
- Masking rules by role at run time: RWB-E1-037.
- Masked data in SIT and UAT: RWB-TE-004.
- Which fields are personal and how long they are kept: DL26.


---

## RWB-TE-012 Document storage containers

| Item | Value |
|---|---|
| Story key | RWB-TE-012 |
| Epic | E1, release 30 November 2026 |
| Module | P5 Document hub |
| Feature | None |
| Requirement IDs | REQ-DCM-003, REQ-DCM-002 |
| BRD section | Business Requirements Program, section 5.5 |
| L3 process | 13 Manage documents and correspondence |
| Decision | DL27 |
| Priority | Must |
| Depends on | RWB-TE-001 |
| Status | Ready for build |

### 1. Story

As a **platform administrator**, I want **blob containers for documents, with a write-once container for legal types, reached by managed identity**, so that **legal documents cannot be overwritten**.

### 2. Business rationale

Audit findings record that evidence for decisions was incomplete or unreliable, and a notice or contract held in a shared folder can be replaced without trace. This story sets up the storage that the document store (RWB-E1-024), the intake (RWB-E1-057) and the malware scan (RWB-E1-041) write to: an intake container, a standard container with version history, a write-once container whose immutability policy refuses any overwrite or delete inside its retention period, and a quarantine container, all reached only by managed identity. It meets REQ-DCM-003 and REQ-DCM-002 and is the storage behind control CTL-12 and the storage pattern recommended under DL27.

### 3. Preconditions

- RWB-TE-001 (recovery module folder and boundary test) is done.
- The ACE storage pattern is used (DL27, option A recommended): one storage account per environment in the SCB tenant with a private endpoint.
- The managed identities RWB-DEV-SY-OCR, RWB-SIT-SY-OCR, RWB-UAT-SY-OCR and RWB-PROD-SY-OCR exist, and the ACE service has its own managed identity in each environment.
- The retention period of the write-once policy is assumed at 3,650 days (10 years), matching the class LEGAL10Y, until the bank retention schedule is supplied (DL26).
- The infrastructure pipeline of the ACE repository can apply storage templates to DEV and SIT.

### 4. Flow

1. Platform administrator: applies the infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers rwb-intake, rwb-docs, rwb-docs-legal and rwb-quarantine.
2. Template: turns on blob versioning and soft delete for rwb-docs, sets the time-based immutability policy on rwb-docs-legal (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the ACE service identity on rwb-intake, rwb-docs and rwb-docs-legal; SY-OCR on rwb-intake, rwb-docs and rwb-quarantine.
3. System: on start, StorageReadinessIndicator checks that the four containers exist and that rwb-docs-legal has its immutability policy; the document hub reports ready only if both hold.
4. Document store (RWB-E1-024): writes each file through BlobStorageAdapter with the managed identity, to rwb-docs-legal for a write-once type and to rwb-docs for any other type, at the name {caseId}/{documentId}/v{docVersion}.
5. Any client: an overwrite or delete of a blob in rwb-docs-legal is refused by the storage service; StorageErrorMapper turns the refusal into WriteOnceViolationException, which the store maps to 409 MSG-P5-002, and the attempt is written to the ACE audit log.
6. Document store: a new version is a new blob at v{n+1}; the earlier blob stays readable.
7. Platform administrator: sees the document hub readiness on SCR-44 Interface and job monitor.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | Overwrite of a write-once blob | Storage refuses; blob unchanged; attempt in the audit log | MSG-P5-002 | AC1 |
| X2 | Delete of a write-once blob | Storage refuses; blob unchanged | MSG-P5-002 | AC2 |
| X3 | Access with an account key or a shared access signature | Storage refuses | None | AC6 |
| X4 | Access by an identity with no role on the container | Storage refuses | None | AC7 |
| X5 | Access from outside the private endpoint | Storage refuses | None | AC8 |
| X6 | A container or the write-once policy is missing at start | Document hub not ready; writes refused | MSG-GEN-006 | AC9 |
| X7 | Storage does not answer within the timeout | StorageUnavailableException; callers return 503 | MSG-GEN-006 | AC10 |
| X8 | A user session reads the quarantine container | Refused | None | AC11 |
| X9 | A write to an existing blob name in rwb-docs-legal with the same content | Refused by storage; the adapter checks the hash and returns the existing blob | None | AC12 |
| X10 | A role without Documents C uploads a document | 403 | MSG-P4-002 | Access test TC-TE-012-13 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the module folder (RWB-TE-001); RWB-E1-024, RWB-E1-041 and RWB-E1-057 build on it |
| Negotiable | The retention period and the soft delete days are template parameters; container names follow the ACE naming standard |
| Valuable | A legal document cannot be changed or removed inside its retention period |
| Estimable | One infrastructure template, one container configuration class, one readiness check, one error mapper |
| Small | Settings and one small adapter layer with tests |
| Testable | Each scenario below runs against the SIT storage account |

### 7. Acceptance criteria

```gherkin
Feature: Document storage containers

  Background:
    Given the SIT storage account has containers "rwb-intake", "rwb-docs", "rwb-docs-legal" and "rwb-quarantine"
    Given "rwb-docs-legal" has a time-based immutability policy of 3650 days

  Scenario: AC1 Write-once
    Given court notice "DOC-0701" stored at "rwb-docs-legal/RW-2026-000701/DOC-0701/v1" with hash "H701"
    When a client using the ACE service managed identity tries to overwrite it
    Then storage refuses the write with "BlobImmutableDueToPolicy"
    Then the blob hash is still "H701"
    Then the attempt is in the audit log with the identity and the time
    Then DocumentStore.replaceContent for "DOC-0701" raises WriteOnceViolationException, shown as 409 with MSG-P5-002

  Scenario: AC2 Delete is refused
    Given court notice "DOC-0701" in "rwb-docs-legal"
    When a client using the ACE service managed identity tries to delete it
    Then storage refuses the delete
    Then the blob is still readable

  Scenario: AC3 A new blob in the write-once container is allowed
    Given court notice "DOC-0701" at "v1" in "rwb-docs-legal"
    When the ACE service identity writes "rwb-docs-legal/RW-2026-000701/DOC-0701/v2"
    Then the write succeeds and both "v1" and "v2" are readable

  Scenario: AC4 The standard container keeps earlier versions
    Given "rwb-docs/RW-2026-000702/DOC-0702/v1" holds an appraisal report
    When the blob is overwritten by the ACE service identity in SIT
    Then the previous blob version is still readable through blob versioning
    Then a deleted blob can be restored within the 30 days of soft delete

  Scenario: AC5 The identities hold only their roles
    Given the role assignments applied by the template in SIT
    When the assignments are listed
    Then the ACE service identity holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-docs-legal" only
    Then "RWB-SIT-SY-OCR" holds Storage Blob Data Contributor on "rwb-intake", "rwb-docs" and "rwb-quarantine" only

  Scenario: AC6 Key-based access is refused
    Given the storage account has shared key access disabled
    When a client calls "rwb-docs" with the account key or with a shared access signature
    Then storage refuses the request with "KeyBasedAuthenticationNotPermitted"

  Scenario: AC7 An identity with no role is refused
    Given managed identity "RWB-SIT-SY-AGENT" has no role on "rwb-docs-legal"
    When it tries to read "rwb-docs-legal/RW-2026-000701/DOC-0701/v1"
    Then storage refuses with "AuthorizationPermissionMismatch"

  Scenario: AC8 Public network access is refused
    Given public network access is disabled on the storage account
    When a client outside the private endpoint calls the account
    Then the system refuses the request

  Scenario: AC9 A missing immutability policy stops the document hub
    Given the immutability policy is removed from "rwb-docs-legal" in DEV
    When the service starts
    Then the readiness check reports the document hub as not ready, naming "rwb-docs-legal"
    Then an upload through POST /api/recovery/v1/cases/{caseId}/documents returns 503 with MSG-GEN-006
    Then the system writes no document row

  Scenario: AC10 Storage does not answer
    Given the storage account does not answer within 10 seconds
    When BlobStorageAdapter writes a file to "rwb-docs"
    Then it raises StorageUnavailableException after 10 seconds
    Then the upload endpoint returns 503 with MSG-GEN-006

  Scenario: AC11 The quarantine container is closed to user sessions
    Given file "Q-0001" in "rwb-quarantine"
    When the ACE service tries to read it on behalf of a case owner
    Then the system refuses the read
    Then only "RWB-SIT-SY-OCR" can write to "rwb-quarantine"

  Scenario: AC12 A repeated write of the same file is not an overwrite
    Given "rwb-docs-legal/RW-2026-000703/DOC-0703/v1" holds a file with hash "H703"
    When BlobStorageAdapter is asked to write the same file with hash "H703" to the same name
    Then the system attempts no overwrite and the existing blob reference is returned
    Then the same name with a different hash raises WriteOnceViolationException
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The write-once container refuses overwrite and delete for the retention period; the policy is locked in PROD and unlocked in DEV, SIT and UAT so test data can be removed | NFR-029; CTL-12; template parameter legalRetentionDays 3650, assumed; DL26 |
| BR2 | A change to a stored document is a new blob at the next version; earlier versions stay readable | FEAT-DCM-20; VR-P5-001-2 |
| BR3 | Storage is reached only by managed identity; account keys and shared access signatures are disabled | Story intent; CTL-09 |
| BR4 | Each identity holds a role only on the containers it needs | Least privilege; roles of SY-OCR in roles.txt (Documents CRU) |
| BR5 | The document hub reports ready only when the four containers exist and the write-once policy is in place | DL27 |
| BR6 | The standard container keeps blob versions and soft-deleted blobs for 30 days | Template parameter softDeleteDays 30, assumed; DL27 |
| BR7 | A write of identical content to an existing write-once name returns the existing blob; different content is a violation | R-UNI-40; CTL-12 |

### 9. State transitions

None. This story does not change a case status or a document status. It sets up containers, policies and role assignments.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| RW-PLATADM, platform administrator | Applies the infrastructure template and reads the readiness check (Platform administration CRUD) |
| RW-SECADM, security administrator | Reviews the role assignments on the containers (Platform administration CRUDA) |
| SY-OCR, OCR and extraction pipeline | Writes to rwb-intake, rwb-docs and rwb-quarantine with its managed identity |
| RW-CASEOWN, case owner | Uploads documents through the store, which uses the ACE service identity (Documents CRU) |
| Solution architect with Compliance | Owns DL27 |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-DOC-006 | document | storage_ref | Read (format {container}/{caseId}/{documentId}/v{docVersion}) |
| DF-DOC-010 | document | write_once | Read |
| DF-DOC-011 | document | doc_version | Read |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

No endpoint of its own. The upload endpoint POST /api/recovery/v1/cases/{caseId}/documents (RWB-E1-026, RWB-E1-024) uses these containers: Documents, right C, scope applied; 403 without the right (MSG-P4-002); 503 when storage is unavailable or the document hub is not ready (MSG-GEN-006).

**Container configuration (P5, used by BlobStorageAdapter in RWB-E1-024, QuarantineMover in RWB-E1-041 and IntakeService in RWB-E1-057)**

```java
package recovery.dochub.storage;
public interface DocumentContainers {
    BlobContainerClient intake();       // rwb.dochub.container.intake
    BlobContainerClient standard();     // rwb.dochub.container.standard
    BlobContainerClient legal();        // rwb.dochub.container.legal
    BlobContainerClient quarantine();   // rwb.dochub.container.quarantine
    StorageReadiness readiness();       // containers present, legal policy present
}
// Exceptions raised to callers: WriteOnceViolationException, StorageUnavailableException
```

### 13. Solution plan

**Package.** folder `recovery/dochub/storage`, Java package `recovery.dochub.storage`; the infrastructure template in the ACE infrastructure folder, in the format the ACE team uses.

**Components**

| Component | Type | Responsibility |
|---|---|---|
| Storage infrastructure template | Configuration | Account settings, four containers, versioning and soft delete on rwb-docs, immutability policy on rwb-docs-legal, role assignments |
| DocumentContainers | Published interface | Container clients and readiness |
| DocumentContainersConfig | Service | Builds the clients with DefaultAzureCredential restricted to managed identity, and the 10-second timeout |
| StorageReadinessIndicator | Service | BR5; joins the ACE health endpoint |
| StorageErrorMapper | Service | Maps BlobImmutableDueToPolicy and conflicts on rwb-docs-legal to WriteOnceViolationException, timeouts to StorageUnavailableException; writes the audit event for a refused overwrite or delete |
| ContentHashGuard | Service | BR7: compares the SHA-256 of an existing write-once blob before a write |

**Database**

- No table or column. storage_ref values follow {container}/{caseId}/{documentId}/v{docVersion}, within varchar(400).

**Configuration and reference data**

- Properties per environment: rwb.dochub.storage.account-url, rwb.dochub.container.intake, rwb.dochub.container.standard, rwb.dochub.container.legal, rwb.dochub.container.quarantine, rwb.dochub.storage.timeout-seconds 10.
- Template parameters: legalRetentionDays 3650 (assumed; DL26), legalPolicyLocked true in PROD only, softDeleteDays 30 (assumed; DL27).

**Build steps**

1. Write the infrastructure template with the account settings, the four containers, the policies and the role assignments; apply it in DEV and SIT.
2. Build DocumentContainersConfig with managed identity credentials only; test that key-based clients are refused.
3. Build StorageErrorMapper with the audit event; test AC1 and AC2 against SIT.
4. Build ContentHashGuard; test AC12.
5. Build StorageReadinessIndicator and wire it into the ACE health endpoint; test AC9 in DEV.
6. Run the SIT tests of section 16, including the role listing of AC5, and hand the assignment list to the security administrator.

**Feature flag:** `rwb.dochub.storage-containers`. Off: the readiness check reports not ready and every document write is refused with 503 rather than written outside the write-once container.

**Done when:** the tests in section 16 pass in SIT, the template is applied in DEV and SIT, and the security administrator has reviewed the role assignments.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P5-002 | Overwrite or delete of a write-once document | Legal documents cannot be changed. Add a new version instead. |
| MSG-GEN-006 | Storage unavailable or document hub not ready | {system} is not available. Your request is queued and will be retried. |
| MSG-P4-002 | Role without Documents C | You cannot {action} here. Your role does not include it. |

Thai text for each message follows decision DL10.

### 15. Screens and states

No screen in this story. The platform administrator sees the document hub readiness on SCR-44 Interface and job monitor. The case owner uploads on SCR-30 Case documents (RWB-E1-026).

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-012-01 | AC1, BR1 | System | Synthetic court notice in rwb-docs-legal |
| TC-TE-012-02 | AC2, BR1 | System | Delete attempt on the same blob |
| TC-TE-012-03 | AC3, BR2 | System | v2 blob for the same document |
| TC-TE-012-04 | AC4, BR6 | System | Overwrite and delete in rwb-docs in SIT |
| TC-TE-012-05 | AC5, BR4 | System | Role assignment listing in SIT |
| TC-TE-012-06 | AC6, BR3 | System | Client with account key and with a shared access signature |
| TC-TE-012-07 | AC7, BR4 | System | Managed identity RWB-SIT-SY-AGENT |
| TC-TE-012-08 | AC8, BR3 | System | Client outside the private endpoint |
| TC-TE-012-09 | AC9, BR5 | System | Policy removed in DEV |
| TC-TE-012-10 | AC10 | System | Storage stub with a 10-second timeout |
| TC-TE-012-11 | AC11, BR4 | System | File in rwb-quarantine |
| TC-TE-012-12 | AC12, BR7 | System | Same and different content to an existing write-once name |
| TC-TE-012-13 | Access | Access | RW-REFADM user (Documents -) calls POST /cases/{caseId}/documents; refused with MSG-P4-002 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the retention period, soft delete days and container names come from template parameters and properties.
- No personal data in logs, tests or prompts: blob names carry case and document IDs only, never a customer name or ID number; test files are synthetic.
- No read of another module's tables.
- No account key, connection string or shared access signature in code, configuration or the pipeline.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DCM-003 | Legal document types held in a write-once container that cannot be altered or deleted | Business Requirements Program, section 5.5 | FEAT-DCM-01 | 13 Manage documents and correspondence | R-UNI-40 | TC-TE-012-01 to TC-TE-012-03, TC-TE-012-09, TC-TE-012-12 |
| REQ-DCM-002 | The document hub is the system of record; no other store holds the authoritative copy | Business Requirements Program, section 5.5 | FEAT-DCM-19 | 13 Manage documents and correspondence | None | TC-TE-012-04 to TC-TE-012-08, TC-TE-012-10, TC-TE-012-11, TC-TE-012-13 |

### 19. Out of scope

- Choosing the container per document type and writing the document row (RWB-E1-024).
- Retention classes, archive and the retention job (RWB-E1-041, JOB-17).
- Legal hold on a case or a document (REQ-DCM-016; DL27).
- Backup and restore test of the document store (REQ-DCM-015; DL27).
- Sizing and cost of the storage (REQ-DCM-014; NFR-069).


---

## RWB-TE-013 Agent runtime client with fallback

| Item | Value |
|---|---|
| Story key | RWB-TE-013 |
| Epic | E1, release 30 November 2026 |
| Module | P10 Agent runtime |
| Feature | None |
| Requirement IDs | REQ-DRI-001, REQ-DRI-005, REQ-ACA-010 |
| BRD section | Business Requirements Epic 1, section 3.9; Business Requirements Program, sections 5.4 and 5.7 |
| L3 process | All recovery processes |
| Decision | DL33 |
| Priority | Must |
| Depends on | RWB-TE-007, RWB-E1-058, RWB-E1-027 |
| Status | Ready for build |

### 1. Story

As a **platform administrator (RW-PLATADM)**, I want **one client in the recovery module that calls the agent orchestrator, applies the autonomy mode, runs shadow mode and falls back to the rule result**, so that **agents are added to a case step without changing the case flow, and every step records what the agent did**.

### 2. Business rationale

A case step that waits on an agent with no limit stops the case, and a step that acts on an unchecked answer breaks the rule that a person decides. The client puts every agent call behind one interface: the rule result always exists, the agent answer is used only as the autonomy mode allows, and the decision log entry records the rule, agent and prompt versions and any fallback (REQ-DRI-001). If the entry cannot be written, the step does not act (REQ-DRI-005). The measure is the agent fallback rate, target below 10 percent per month.

### 3. Preconditions

- RWB-TE-007 is done: Quartz jobs and their run books exist, so a job step can call the client.
- RWB-E1-058 is done: AgentOrchestrator, agent_policy and agent_run exist.
- RWB-E1-027 is done: the P7 DecisionLogWriter interface writes entries and throws on failure.
- An approved agent_policy row exists for the agent, with autonomy_mode SHADOW or L1 and timeout_seconds 60.
- The calling module runs under its own service identity (for example SY-CASEWF) and has evaluated its rule before it calls the client.

### 4. Flow

1. Calling step (for example SY-CASEWF): evaluates its rule and builds the rule result (rule ID, rule version, next state).
2. Calling step: calls AgentStepClient.runStep with the agent code, case ID, decision code, step key and rule result.
3. Client: reads the autonomy mode from the agent policy in force; if it is OFF or the flag is off, it skips the agent.
4. Client: calls AgentOrchestrator.run with the idempotency key built from the step key and waits at most timeout_seconds.
5. Client: in SHADOW mode, keeps the rule result as the applied result and records the agent answer only.
6. Client: in L1 mode, keeps the rule result as the applied result and returns the checked agent answer as the recommendation for the person who decides.
7. Client: on a timeout or a guardrail failure, keeps the rule result and marks fallback true with the reason (R-UNI-32).
8. Client: writes one decision log entry through DecisionLogWriter with the rule ID and version, agent version, model version, recommendation and fallback, then links it to the agent run.
9. Calling step: acts on the applied result only after the entry is written.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | The agent does not answer within 60 seconds | Rule result applied; fallback true with reason TIMED_OUT; step continues | None to a user | AC2 |
| X2 | The answer fails a guardrail check | Rule result applied; fallback true with the check code | None to a user | AC4 |
| X3 | No approved policy exists for the agent on the business date | No agent call; rule result applied; fallback true with reason NO_POLICY | None to a user | AC5 |
| X4 | The decision log write fails | The step does not act; the case stays in its state; an incident is raised (R-UNI-39) | MSG-P7-003 | AC6 |
| X5 | The same step key arrives twice | One agent run and one decision log entry; the repeat returns the first outcome (R-UNI-40) | None to a user | AC7 |
| X6 | Autonomy mode OFF or flag `rwb.agent.client` off | No agent call; rule result applied; fallback false; no agent run row | None to a user | AC8 |
| X7 | A role without the right reads agent runs | Refused with 403 | MSG-P4-002 | TC-TE-013-09 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs the orchestrator (RWB-E1-058), the decision log writer (RWB-E1-027) and the job pattern (RWB-TE-007); no agent story |
| Negotiable | The mode and timeout per agent are data; the client fixes only the order: rule first, agent second, log before action |
| Valuable | Every agent from RWB-E1-059 onward plugs into case steps through this one interface |
| Estimable | One published interface, one service, one decision log mapping, no screen, no table of its own beyond one link column |
| Small | One developer, under one week with its tests |
| Testable | Each criterion is a unit or component test with a stubbed orchestrator and a stubbed decision log writer |

### 7. Acceptance criteria

```gherkin
Feature: Agent runtime client with fallback

  Background:
    Given agent "INTAKE" has approved policy "P1" with timeout 60 seconds and prompt "PR1"
    Given case "RW-2026-000201" is in route state "NEW" and status "New"
    Given the calling step has rule result rule "R-UNI-32" version "2026.11" with next state "RESUME_STATE"

  Scenario: AC1 Shadow
    Given the policy of "INTAKE" has autonomy mode "SHADOW"
    When the agent answers in 2,000 ms with a valid output
    Then the system stores the agent answer on the agent run and the rule result is the applied result
    Then one decision log entry holds agent version "INTAKE@P1/PR1", the rule ID and version, recommendation null and fallback false in actions
    Then the calling step receives the rule result and no agent output

  Scenario: AC2 No answer
    Given the agent does not answer in 60 seconds
    When the step runs
    Then the system uses the rule result and the step continues to "RESUME_STATE"
    Then the decision log entry holds actions fallback true with reason "TIMED_OUT" and the agent run ID (R-UNI-32)
    Then the agent run holds status "TIMED_OUT" and fallback true

  Scenario: AC3 Assisted mode returns the answer as a recommendation
    Given the policy of "INTAKE" has autonomy mode "L1"
    When the agent answers with confidence 0.91
    Then the rule result is the applied result
    Then the outcome returns the agent answer as the recommendation for the person who decides
    Then the decision log entry holds the agent answer in recommendation with confidence 0.91

  Scenario: AC4 A guardrail failure falls back
    Given the agent answer fails check "SCHEMA"
    When the step runs
    Then the system applies the rule result
    Then the decision log entry holds actions fallback true with reason "SCHEMA"

  Scenario: AC5 No approved policy
    Given agent "INTAKE" has no approved policy on 2026-11-30
    When the step runs on 2026-11-30
    Then the system makes no orchestrator call
    Then the system applies the rule result with fallback true and reason "NO_POLICY" in the decision log entry

  Scenario: AC6 The decision log write fails
    Given the decision log writer throws on write
    When the step runs
    Then the calling step does not act and case "RW-2026-000201" stays in "NEW"
    Then the client raises DecisionNotRecordedException carrying MSG-P7-003 and an incident is raised (R-UNI-39)
    Then the agent run stays with decision_log_id empty

  Scenario: AC7 A repeated step key
    Given the step with key "CASEWF:RW-2026-000201:ENTRY:2026-11-30" ran once
    When it runs again with the same key
    Then one agent run and one decision log entry exist for the key
    Then the second call returns the first outcome (R-UNI-40)

  Scenario: AC8 Agent switched off
    Given the policy of "INTAKE" has autonomy mode "OFF"
    When the step runs
    Then no orchestrator call and no agent run row are made
    Then the decision log entry holds agent version null and fallback false
```

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | The rule result is computed before the agent is called and is always the applied result in SHADOW and L1 | Agent catalog autonomy levels; agent_policy.autonomy_mode (New) |
| BR2 | If the agent does not answer within agent_policy.timeout_seconds (60, assumed; DL11), the rule result is used and the fallback is recorded on the decision | R-UNI-32 |
| BR3 | A step acts only after its decision log entry is written | Principle 5; R-UNI-39; CTL-06 |
| BR4 | The decision log entry holds the rule ID, rule version, agent version as "<agent>@<policy>/<prompt>", model version and the recommendation | REQ-DRI-001; decision_log_entry.agent_version |
| BR5 | The idempotency key of the agent run is the step key | R-UNI-40 |
| BR6 | The client runs under the identity of the calling module; the orchestrator runs tools as SY-AGENT | REQ-ACA-010 |

### 9. State transitions

| From | Event | Condition | To |
|---|---|---|---|
| ANY_ACTIVE | AGENT_UNAVAILABLE | The agent or the model does not answer inside the timeout (R-UNI-32) | RESUME_STATE, with the rule result applied |
| ANY_ACTIVE | DECISION_LOG_WRITE_FAILED | The entry cannot be written (R-UNI-39) | EXCEPTION_QUEUE, raised by the calling step |

The client does not change a case status itself; the calling step moves the case on the applied result.

### 10. Authority

| Who | What they may do in this story |
|---|---|
| SY-CASEWF and other calling module identities | Call AgentStepClient; write the decision log entry through P7 (Decision log C) |
| SY-AGENT | Runs the agent and its tools (read only) |
| SY-DECLOG | Writes the entry |
| RW-PLATADM, RW-COE, RW-AUDIT, RW-COMPLY, RW-DATASTEW, RW-SECADM | Read agent runs and fallbacks through GET /admin/agent-runs (Platform administration R) |

### 11. Data

| BR Field ID | Entity | Field | Read or write |
|---|---|---|---|
| DF-CAS-001 | recovery_case | id | Read |
| DF-CAS-007 | recovery_case | route_state | Read |
| DF-REF-002 | rule_row | rule_id | Read (from the rule result passed in) |
| DF-REF-003 | rule_row | rule_version | Read (from the rule result passed in) |
| DF-DEC-001 to DF-DEC-018 | decision_log_entry | all fields | Write (through the P7 DecisionLogWriter) |
| DF-AGT-008 | agent_policy | autonomy_mode | Read |
| DF-AGT-012 | agent_policy | timeout_seconds | Read |
| DF-AGT-021 | agent_policy | status | Read |
| DF-AGT-022 | agent_policy | valid_from | Read |
| DF-AGT-036 | agent_run | id | Read |
| DF-AGT-046 | agent_run | status | Read |
| DF-AGT-047 | agent_run | fallback | Read |
| DF-AGT-045 | agent_run | idempotency_key | Read |
| DF-AGT-058 | agent_run | decision_log_id | Write |

Field IDs are those in the Logical Data Model and Data Dictionary.

### 12. Contract

**Published interface**

```java
package recovery.agent.api;

public interface AgentStepClient {
    AgentStepOutcome runStep(AgentStepRequest request) throws DecisionNotRecordedException;
}

public record AgentStepRequest(String agentCode, UUID caseId, String decisionCode,
                               String stepKey, RuleResult ruleResult, Map<String, Object> inputs) {}
public record RuleResult(String ruleId, String ruleVersion, String toState, JsonNode result) {}
public record AgentStepOutcome(UUID decisionLogEntryId, RuleResult appliedResult, JsonNode recommendation,
                               boolean fallback, String fallbackReason, String autonomyMode, UUID agentRunId) {}
```

**Decision log mapping** (DecisionLogWriter.write): case_id = caseId; decision_code = decisionCode; rule_id and rule_version from ruleResult; agent_version = "<agent>@<policy_version>/<prompt_version>" or null; model_version from the run; inputs_ref = reference to the masked inputs snapshot; recommendation = agent answer in L1, null otherwise; final_call = ruleResult.toState; actions = {"agentRunId", "mode", "fallback", "fallbackReason"}.

**GET /api/recovery/v1/admin/agent-runs** (api.yaml): query agent, from, to; response AgentRun[] with fallback; errors 401, 403, 503; Platform administration R; read only.

**Events:** EV-28 AgentRunCompleted is published by the orchestrator (RWB-E1-058); the client publishes none.

**Idempotency:** stepKey, used as the agent run idempotency key and as the decision log lookup key for repeats.

### 13. Solution plan

**Package.** `src/main/java/.../recovery/agent/api/` and `.../recovery/agent/client/`, Java packages `recovery.agent.api` (interface and records) and `recovery.agent.client` (implementation).

**Components**

| Component | Type | Responsibility |
|---|---|---|
| AgentStepClient | Published interface | The only way another module calls an agent |
| AgentStepClientImpl | Service | Mode check, timed orchestrator call, fallback, decision log write, link to run |
| AutonomyModeResolver | Service | Reads the policy in force for the agent and date |
| DecisionLogMapper | Service | Builds the P7 entry from the request, the rule result and the run |
| AgentRunRepository | Repository | Sets agent_run.decision_log_id |

**Database:** reads agent_policy and agent_run; adds column decision_log_id uuid to agent_run in migration `V10_002__agent_run_decision_link.sql`. No new table.

**Configuration and reference data:** agent_policy rows (RW-COE loads, RW-RISK approves). Feature flag in the ACE flag service.

**Build steps**
1. Write the interface and records in `recovery.agent.api`, with an ArchUnit test that other modules import only this package.
2. Build AutonomyModeResolver with tests for OFF, SHADOW, L1 and no policy (AC5, AC8).
3. Build the timed call with a CompletableFuture and the policy timeout; test with a stub that sleeps 61 seconds on a fake clock (AC2).
4. Build DecisionLogMapper and the write before return; test write failure (AC1, AC3, AC6).
5. Build the idempotent repeat on the step key (AC7) and the guardrail fallback (AC4).

**Feature flag:** `rwb.agent.client`. Off: no agent call; the rule result is applied and logged with agent version null.

**Done when:** the tests in section 16 pass and the boundary test shows other modules depend only on `recovery.agent.api`.

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| MSG-P7-003 | The decision log write fails and the step does not act | The action was not taken because the decision could not be recorded. Try again in a few minutes. |
| MSG-P4-002 | Role without the right reads agent runs | You cannot {action} here. Your role does not include it. |

### 15. Screens and states

No screen in this story. A fallback shows in GET /admin/agent-runs (fallback true) and on the decision log entry of the case.

### 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-013-01 | AC1, BR1, BR4 | System | Case RW-2026-000201, mode SHADOW, answer in 2,000 ms |
| TC-TE-013-02 | AC2, BR2 | System | Orchestrator stub silent for 61 seconds |
| TC-TE-013-03 | AC3, BR1 | System | Mode L1, confidence 0.91 |
| TC-TE-013-04 | AC4 | System | Answer fails check SCHEMA |
| TC-TE-013-05 | AC5 | System | No approved policy on 2026-11-30 |
| TC-TE-013-06 | AC6, BR3 | System | Decision log writer throws |
| TC-TE-013-07 | AC7, BR5 | System | Step key CASEWF:RW-2026-000201:ENTRY:2026-11-30 twice |
| TC-TE-013-08 | AC8 | System | Mode OFF |
| TC-TE-013-09 | Access | Access | RW-CASEOWN calls GET /admin/agent-runs; refused with MSG-P4-002 |
| TC-TE-013-10 | Principle 5 | Resilience | Decision log write forced to fail during a step in SHADOW mode; step does not act; MSG-P7-003 |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: mode and timeout come from the approved agent policy.
- No personal data in logs, tests or prompts; the inputs snapshot is masked before it is referenced.
- No read of another module's tables; the decision log is written only through the P7 interface.
- The client never applies an agent answer as the case result in SHADOW or L1.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-001 | Every decision records rule, model, agent and prompt versions | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-32 | TC-TE-013-01, TC-TE-013-02, TC-TE-013-03, TC-TE-013-04 |
| REQ-DRI-005 | No action proceeds if its decision log entry cannot be written | Business Requirements Program, section 5.7 | FEAT-AGT-11 | All recovery processes | R-UNI-39 | TC-TE-013-06, TC-TE-013-10 |
| REQ-ACA-010 | Agents run under service identities with the same role checks | Business Requirements Program, section 5.4 | FEAT-AGT-01 | All recovery processes | R-UNI-40 | TC-TE-013-05, TC-TE-013-07, TC-TE-013-08, TC-TE-013-09 |

### 19. Out of scope

- The orchestrator, gateway and guardrail checker (RWB-E1-058).
- Agent answers acted on without a person (autonomy L2 and above, Epic 8, FEAT-AGT-15).
- The case steps that call the client: case intake (RWB-E2-028), deviation screening (RWB-E2-029).


---
