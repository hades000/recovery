SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench build notes, the technical enablers

> **D-RCV-60.** This version applies decision D-RCV-60 and the Arch v5 target: 19 services inside ACE, one schema and login per service, Kafka with outbox and inbox, Temporal Schedules in place of Quartz, a local decision record with a central ledger, and no data lake. Each technical enabler now sits in the epic and story keys the realignment gives it. The Module line and every step of every entry stay as they are in v2, word for word, with release dates marked (tentative); the microservice change is carried in a realignment block under each Module line. RWB-TE-005 stays retired from D-RCV-36, and RWB-TE-007 is retired under D-RCV-60 with no new story. Owners follow the Ownership Map and the epic names follow Template and Rules section R5. Values the sources do not state are marked in place and listed in the gap and assumption registers (Template and Rules section R9).

> **D-RCV-36.** This version applies decision D-RCV-36. RWB-TE-005 is retired; its work moved to RWB-E1-073 (the scenario runner and the build gate) and the replacement notes sit in the Epic 1 build notes. The other technical enablers keep their existing content.

## Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| v2 | 16 November 2026 | D-RCV-36: RWB-TE-005 retired, its work moved to RWB-E1-073 and the Epic 1 build notes | Not recorded in the source |
| v3 | 22 November 2026 | D-RCV-60 microservice realignment | T3 Code / OpenCode / DeepSeek v4.1 Flash |

## Realignment map (D-RCV-60)

Every technical enabler keeps its legacy key, its title and its step text. The table gives the epic, the story keys, the target owner and the release of the new story set, from the Service Story Catalog v1 and the Ownership Map.

| Legacy key | Title | Epic (D-RCV-60) | Story keys | Service owner | Release |
|---|---|---|---|---|---|
| RWB-TE-001 | Recovery module folder and boundary test | RWB-PLT-TPL | RWB-PLT-TE001-APP; RWB-PLT-TE001-APP-2 | platform: the 19 service repositories from the template | 30 November 2026 (tentative) |
| RWB-TE-002 | Code owners for the recovery module | RWB-PLT-TPL | RWB-PLT-TE002-APP; RWB-PLT-TE002-OPS | platform: the 19 service repositories, ace-web and the architecture folder | 30 November 2026 (tentative) |
| RWB-TE-003 | Types and contract tests from the API specification | RWB-PLT-TPL | RWB-PLT-TE003-APP; RWB-PLT-TE003-APP-2 | platform: each service's own API file and client | 30 November 2026 (tentative) |
| RWB-TE-004 | Masked data in SIT and UAT | RWB-PLT-TPL; RWB-ITG-W1 | RWB-PLT-TE004-APP; RWB-ITG-TE004-ITG | rwb-source-data (P1) for the data; the loader is a tool outside the 19 services | 30 November 2026 (tentative) |
| RWB-TE-005 | (retired under D-RCV-36) | none | none; its work is RWB-E1-073 | not applicable | not applicable |
| RWB-TE-006 | Outbox and retry for outbound work | RWB-PLT-LIB; RWB-ITG-W1 | RWB-PLT-TE006-CON; RWB-PLT-TE006-APP; RWB-ITG-TE006-ITG | platform library, one copy in every service schema | 30 November 2026 (tentative) |
| RWB-TE-007 | Scheduled jobs on Quartz | retired (Template and Rules section R6) | none; dependencies point to RWB-PLT-E1071-CON | each owning service, through RWB-PLT-E1071 | not applicable |
| RWB-TE-008 | Decision log hash chain check | RWB-PLT-TPL; RWB-ITG-W1 | RWB-PLT-TE008-APP; RWB-ITG-TE008-ITG | rwb-decision (P7) for JOB-14; every service's own chain | 30 November 2026 (tentative) |
| RWB-TE-009 | Performance test harness | RWB-ITG-NFR | RWB-ITG-TE009-ITG | integration; QA team | 31 December 2026 (tentative) |
| RWB-TE-010 | Browser and accessibility tests | RWB-ITG-NFR | RWB-ITG-TE010-ITG | integration; QA team | 31 December 2026 (tentative) |
| RWB-TE-011 | PDPA lint for code, tests and logs | RWB-PLT-TPL | RWB-PLT-TE011-APP | platform; the field list is rwb-source-data's (P1) | 30 November 2026 (tentative) |
| RWB-TE-012 | Document storage containers | RWB-PLT-TPL | RWB-PLT-TE012-APP | rwb-document (P5) uses the containers | 30 November 2026 (tentative) |
| RWB-TE-013 | Agent runtime client with fallback | RWB-SVC-P10; RWB-SVC-P7; RWB-ITG-W1 | RWB-P10-TE013-CON; RWB-P10-TE013-APP; RWB-P10-TE013-OPS; RWB-P7-TE013-APP; RWB-ITG-TE013-ITG | rwb-agent (P10); rwb-decision (P7) for the ledger | 30 November 2026 (tentative) |

**How to read a realignment block.** "Delta, step by step" gives the target for the steps whose mechanism the microservice change alters. A step that is not named keeps the v2 text as the target. The story keys in the block are the specification; this document is the reading guide, as it was in v2.

Every flow step of every story in the technical enablers, written out in full so it can be followed without knowing the Workbench already. Each entry gives the step as the story states it, then what it means: who acts, what runs on its own, and what has to be built. The story remains the specification. Where the two differ, the story governs.

## RWB-TE-001 Recovery module folder and boundary test

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-PLT-TPL service template and repositories, wave 0. Stories RWB-PLT-TE001-APP (preserved, as built) and RWB-PLT-TE001-APP-2 (delta), release 30 November 2026 (tentative). Suggested owner: TechX (suggested; any team may pick up this story). The target is 19 service repositories generated from one template, each with its own schema and login, and no repository compiles another (Arch v5 slides 20, 29 and 41).

Delta, step by step:

- Step 1: the 19 module packages become 19 services. Each repository carries one Java base package `th.co.scb.ace.workbench.recovery.<short without hyphen>` (Template and Rules section R4), with its `api` and `internal` packages inside it. There is no single recovery root package any more, and the front end folder `src/modules/recovery` stays in ace-web behind the gateway-bff composite route (DP-19).
- Step 2: the module map is held per service repository and lists that service's own packages only. A service's entry also carries its schema `rwb_<short with _>`, REST base `/api/recovery/<short>/v1`, topic `rwb.<short>.events.v1` and Temporal task queue `rwb-<short>` (Ownership Map, Services).
- Step 3: ArchUnit keeps BND-4 and BND-5 inside a service. BND-1 and BND-2 point at the ACE Common and collection contracts instead of packages of one codebase, and BND-3 becomes the other service's published contract or an application event through the outbox, because the other module is now another repository with its own login (DP-01, DP-09, DP-11).
- Step 4: the front end rule becomes one rule per service: a screen reaches its owner service through the gateway-bff composite route and imports no other service's screen (DP-19; H RWB-PLT-N001-CON).
- Step 5: the guard covers each service's own base `/api/recovery/<short>/v1` and calls the rwb-access authorise contract instead of the common module's internal interface INT-34 (DP-08; H RWB-PLT-E1037-CON, C RWB-P4-E1037-CON). MSG-P4-002 is unchanged.
- Steps 6 to 8: the pipeline, the failure text and the fix are unchanged in intent. A cross-schema reference, and a Kafka record sent or consumed without the outbox and inbox library, join the rules that fail the build (RWB-PLT-TE001-APP-2).

### Step 1

**In the story.** Squad member: creates the recovery folders and packages for the 19 Workbench modules, each with an `api` package and an `internal` package.

A developer does this by hand, once. Create the back end folder ace-service/src/main/java/<ACE base package>/recovery/ and inside it one package for each of the 19 Workbench modules: dataengine, integration, casewf, access, dochub, comms, decision, payments, reporting and agent for P1 to P10, then valuation, treatment, guarantee, litigation, asset, debtsale, writeoff, deviation and partner for S1 to S9. Each module package holds two child packages. The api package holds the interfaces that other modules are allowed to call. The internal package holds the rest, which only that module may use. Add a package-info file to each one, and create the front end folder src/modules/recovery as well. Every later recovery story places its code inside these folders.

### Step 2

**In the story.** Squad member: writes the module map `architecture/recovery-modules.yaml` with each module code, its package and its published packages.

You write one file by hand at architecture/recovery-modules.yaml. For each of the 19 modules it gives the module code, its Java package, the packages that count as published, and the client libraries that module is allowed to use. A published package is one that other modules may import. The api package is published for every module, and a story that publishes from a different package, for example recovery.casewf.allocation or recovery.decision.writer, lists that package here too. The boundary test reads this file rather than holding module names in test code, so adding or renaming a module is a change to the file. The TechX tech leads own the file through code owners.

### Step 3

**In the story.** Squad member: writes RecoveryBoundaryTest with the rules BR1 to BR5, reading the module map.

You write one back end test class using ArchUnit, a library that checks dependencies between compiled classes as an ordinary unit test. It builds five rules from the module map, which it loads through ModuleMapLoader. BND-1 lets a recovery class reach the collection module only through that module's published packages. BND-2 does the same for the common module. BND-3 lets one recovery module reach another only through a package the map lists as published for it, or through an application event. BND-4 keeps a module's entities and repositories inside that module. BND-5 limits HTTP, SFTP and file transfer clients to the packages the map allows. Write one test-only fixture class per rule that breaks it, kept under src/test.

### Step 4

**In the story.** Squad member: writes the front end boundary rules for `src/modules/recovery`.

You add a dependency rule file for the front end folder src/modules/recovery, and the front end lint step applies it on every build. Two rules go in it. No file under src/modules/recovery imports anything from src/modules/collection. Imports from src/common go only through its public index file. Dependency rules work on import paths in the source, so this check needs no running application. Write a breaking fixture as well, a component under src/modules/recovery that imports a collection screen, and confirm the front end build fails with rule no-collection-import. That fixture stays in the test code and never ships.

### Step 5

**In the story.** Squad member: wires the common module access check for `/api/recovery/v1/**` through RecoveryAccessGuard.

You write RecoveryAccessGuard and attach it to every path under /api/recovery/v1/. It offers one method, require(String capabilityArea, Right right, ScopeTarget target), which calls the common module's published access check, interface INT-34. When the caller's role lacks the right, the method throws AccessDeniedException, and the service turns that into a 403 Problem response with messageCode MSG-P4-002. For this story, add a test-only controller that declares Case record R so the guard can be exercised. TC-TE-001-08 calls that endpoint as role RW-REFADM and expects the refusal. The access check inside the common module belongs to the ACE team and is not yours to write.

### Step 6

**In the story.** Pipeline: on each pull request runs the back end tests, including RecoveryBoundaryTest, and the front end dependency check.

This happens on its own once the wiring is in place. The ACE build already runs the unit test phase on every pull request, so RecoveryBoundaryTest runs there with the other back end tests, and the dependency rules run in the front end lint step. Your work is the change to the pipeline definition that makes both checks part of the pull request build, so a failure blocks the merge. The same two checks also run on every build of main. Neither check keeps state, so the answer depends only on the commit: the same commit always gives the same result, and a rerun after a failure needs no cleanup first.

### Step 7

**In the story.** Pipeline: fails the build when a rule is broken and prints the rule, the class and the class it depends on.

The test decides the build result, so no person judges it. When a rule is broken, the pipeline marks the pull request check as failed. Make the failure readable: the build log line is Rule {code} broken: {class} depends on {dependency}. Use {module}.api or an application event. ArchUnit prints the description it was given, so set each rule description to its code, BND-1 to BND-5, and let it name the class and the class it depends on. When a package is missing from the module map, the log reads package {package} is not in the module map. This log text is written for developers and does not follow the Workbench message rules.

### Step 8

**In the story.** Squad member: fixes the call by going through the other module's `api` package or an application event, and the build passes.

A developer fixes the code; the build never fixes itself. Two ways out are allowed. The first is to call the other module through a package the module map lists as published for it, for example replacing an import of recovery.decision.internal.DecisionLogRepository with the published recovery.decision.writer.DecisionLogWriter. The second is an application event, where the calling module publishes an event and the other module handles it, so neither holds a reference to the other's classes. When the problem is a new package, add it to the module map, which needs approval from a TechX tech lead. The pull request check turns green on the next pipeline run.

## RWB-TE-002 Code owners for the recovery module

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, wave 0. Stories RWB-PLT-TE002-APP (TechX suggested owner) and RWB-PLT-TE002-OPS (DevOps suggested owner), release 30 November 2026 (tentative). Repository protection now applies to each of the 19 service repositories plus ace-web, the migration folder and the architecture folder. Whether the split takes one code owners file per repository or one shared file is Not specified in the source documents (GAP-3192; ASM-5584).

Delta, step by step:

- Step 1: the recovery back end path becomes the 19 service repositories created from RWB-PLT-TPL; the recovery test, recovery migration and recovery front end folders and `architecture/recovery-modules.yaml` stay as paths. The team handles stay `@scb-ace/ace-team` for the ACE Common path and `@scb-ace/techx-recovery-tech-leads` for the recovery paths, assumed until DL37 and DL36 are answered, as in v2.
- Step 2: CodeOwnersValidation runs in the pull request build of every repository, with the same three checks and the same text `owner {team} not found`.
- Step 3: the branch rule on main is set per repository by the ACE team repository administrator, with the same settings: a pull request, review from code owners, one approval, stale approvals dismissed, the author's own approval not counted.
- Steps 4 to 7 are unchanged in intent: the host takes the owner from the last matching pattern per changed path, and the merge waits for every owning team of the changed paths.

### Step 1

**In the story.** Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.

You create one text file at the repository root, .github/CODEOWNERS. A code owners file maps a path pattern to the team that has to review changes under that path. Write the entries listed in section 12: the common module path to @scb-ace/ace-team; the recovery back end, recovery test, recovery migration and recovery front end folders and architecture/recovery-modules.yaml to @scb-ace/techx-recovery-tech-leads; and the code owners file itself to both teams. The repository host applies the last pattern that matches a changed file, so general paths come first and specific paths after them. Use team handles only, never single people, so the absence of one person does not block a merge. The team names are assumed until DL37 and DL36 are answered.

### Step 2

**In the story.** Squad member: adds the code owners validation step to the pull request pipeline.

You add one pipeline step, CodeOwnersValidation, to the pull request build. It checks three things: the syntax of the file, that every owner named in it exists in the repository host and has write access, and that every path pattern matches at least one file. A misspelled team name or a path left behind after a folder move fails the step, and the build log reads owner {team} not found. Prove the step works by pushing a branch with a wrong team name, which is test case TC-TE-002-07. The step runs automatically on every pull request that changes any file, so a broken file is caught before anyone relies on it.

### Step 3

**In the story.** ACE team repository administrator: sets the branch rule on main: one approval from a code owner required, stale approvals dismissed on a new commit.

You cannot do this part yourself. The branch rule on main is a setting of the repository host, and only the ACE team's repository administrator may change it. Ask them for it and give them the exact settings: require a pull request, require review from code owners, one approval, dismiss stale approvals, and do not count the author's own approval. A stale approval is one given before the latest commit on the branch. Without this rule the code owners file only suggests reviewers, and a merge can still happen with no owner approval. The test pull requests of section 16 run in a test branch protected by the same rule.

### Step 4

**In the story.** Developer: opens a pull request that changes a recovery folder.

A developer opens the pull request in the normal way, and there is nothing to build for this step. What matters is which files the pull request touches, because the owning team is chosen per changed path. A Java file under the recovery folder calls in the TechX recovery tech leads. A file under the common module folder calls in the ACE team. A pull request that touches one file of each calls in both teams, and the merge waits for both. The same ownership covers a recovery front end file, a file under the recovery migration folder and the module map file, which all belong to the TechX recovery tech leads.

### Step 5

**In the story.** Repository host: requests review from the owning team named for each changed path.

The repository host does this by itself as soon as the pull request opens, with no pipeline step involved. It compares every changed path against the patterns in the code owners file, takes the owner from the last pattern that matches, and adds that team as a required reviewer. Members of that team then see the request in their review queue. You write no code here. Check the behavior on a test pull request: the required reviewers shown on the pull request page are the result of the file, so a wrong team there means a wrong pattern or a wrong order of patterns, and the fix is a change to the file.

### Step 6

**In the story.** Pipeline: runs the validation step; an owner that does not exist or a path that matches no file fails the check.

This runs automatically as part of the pull request build. The validation step added earlier reports a failure in two cases. The first is an owner named in the file that does not exist in the repository host, reported as owner {team} not found. The second is a path pattern in the file that matches no file in the repository, which usually means a folder was moved or renamed and the file was not updated. Both faults sit in the code owners file, so the fix is a change to that file, and that change needs review from both owning teams. The same file and the same changed paths always ask for the same owners.

### Step 7

**In the story.** Code owner: approves; the merge is allowed once every owning team of the changed paths has approved.

A person approves, and the repository host decides when the merge may go ahead. One approval is needed from a code owner of every changed path, so a pull request that touches a recovery file and a common module file waits for a TechX tech lead and a member of the ACE team. An approval from a developer outside the owning team leaves the merge blocked, and the author's own approval does not count, even when the author is a code owner. A new commit pushed after an approval drops that approval, and the owning team has to review again. The merge opens only when every owning team has approved the current commit.

## RWB-TE-003 Types and contract tests from the API specification

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, wave 0. Stories RWB-PLT-TE003-APP (preserved, as built) and RWB-PLT-TE003-APP-2 (delta), release 30 November 2026 (tentative). Suggested owner: TechX (suggested; any team may pick up this story).

Delta, step by step:

- Step 1: the one `api/recovery-api.yaml` becomes the 19 service API files plus gateway-bff and an index (Template and Rules section R8.4). Each file is linted in its own service's build with the same recovery rule set, and the rules of BR2 are unchanged.
- Step 2: generation runs per service, into `<ACE base package>.recovery.<short>.generated.web` and `.generated.model`. The generated packages are no longer shared between modules, because each service implements only its own interfaces.
- Step 3: one generated TypeScript client per service in `ace-web/src/modules/recovery/api/generated`; screens import through gateway-bff and never call a service base directly.
- Step 4: the generation steps sit before the compile step of each service, so a removed property still stops that service compiling.
- Step 5: OperationCatalog reads the service's own file and `rwb.release` is set per service; an operation whose first release belongs to a later service wave is pending in the services that do not own it.
- Step 6: RecoveryContractTest runs per service against its own contract fakes; `contract broken` and `undocumented status` are unchanged.
- Step 7: the role and permission data are read from rwb-access, which owns `role`, `permission` and `masking_rule` (Ownership Map), instead of a seed read in place by the monolith; the security administrator still owns the content. MSG-P4-002 is unchanged.
- Step 8: one report per service, with the gateway-bff report covering the composite routes. The 79 operations of v2 stay one total, now spread across the files; how they divide between the 19 services is Not specified in the source documents (GAP-3190; ASM-5582). A failure in any service's report fails that build.

### Step 1

**In the story.** Build: lints the specification with the recovery rule set; a missing operationId, x-capability or error response fails the build.

The build does this first, with no person involved. You add a lint step and the recovery rule set for the API file at api/recovery-api.yaml. Linting here checks the OpenAPI file itself against rules, before any code is generated or run. The rules come from BR2: every operation carries an operationId, x-module, x-capability with its area and right, and x-first-release, and every error response uses the Problem schema. A file that breaks a rule fails the build at this step and names the operation, so nothing is generated from a file that is already wrong. TC-TE-003-03 proves it with an operation that has no x-capability.

### Step 2

**In the story.** Build: generates the Spring server interfaces and models from the specification.

The build generates this code, and nobody writes it by hand. Add the server generator to the build as a plugin and set it to produce Spring Boot 3 interfaces only, one interface per tag, with the output in <ACE base package>.recovery.generated.web for the interfaces and <ACE base package>.recovery.generated.model for the request and response classes. Interfaces only means the generator gives you method signatures and data classes, and your own controller implements them. The generated packages are listed in the module map as shared, so the boundary test from RWB-TE-001 allows other modules to use them. Generated code is never edited; a change goes into the specification file and the next build produces it again.

### Step 3

**In the story.** Build: generates the TypeScript types and the typed client for the front end.

The build also generates the front end side, through a generator script that runs before the type check. Its output goes to ace-web/src/modules/recovery/api/generated and holds two things: TypeScript type definitions for the schemas in the specification, and a typed fetch client for the operations. Typed means the compiler knows the fields of each request and response, so a screen that reads a field no longer in the specification fails the type check with the file and the line named. Your work is the script and its place in the build order. Screens import from the generated client rather than writing their own fetch calls and their own copies of the types.

### Step 4

**In the story.** Build: compiles the service against the generated interfaces and the front end against the generated types.

The build compiles the service against the generated interfaces and the front end against the generated types, as it already does for the rest of the code. The order is what gives the value here, because a change in the specification shows up as a compile error. When a property is added to a schema, for example warnAt on Timer, both sides receive it after generation and both still compile. When a property is removed, a controller or a screen that still uses it stops compiling. You add no code for this step. You do have to place the generation steps before both compile steps in the build definition.

### Step 5

**In the story.** Contract test: lists every operation with x-first-release at or before `rwb.release` and finds its implementing controller method.

You write OperationCatalog, which reads the specification and returns every operation with its operationId, module, capability and x-first-release value. The test then keeps the operations whose x-first-release is the release named in the build property rwb.release, which is E1 for the 30 November 2026 release (tentative), or an earlier one, and looks for the controller method that implements each of them. An operation of the current release with no controller method fails the build with {operationId} has no implementation, as getAdminJobs does. An operation first released later, such as postQueuesQueueidPlacements in E2, is listed as pending and does not fail the build. This check runs in the build.

### Step 6

**In the story.** Contract test: calls each implemented operation with its fixture and validates the request and the response against the specification.

This is an automated test in the build. Write RecoveryContractTest as a parameterized test, which means one test body that runs once for each operation in the catalog instead of a separate method per operation. For every implemented operation it sends a request built from the fixture data in ContractFixtures and validates both the request and the response against the specification: the status code, the content type and the schema of the body. A field with the wrong type fails with contract broken, the operationId and the JSON path. A status the specification does not list fails with undocumented status. Fixtures are synthetic rows in an in-memory test database.

### Step 7

**In the story.** Access test: calls each operation as a role whose permission lacks the declared right and expects 403 with messageCode MSG-P4-002.

A second automated test covers access. Write RecoveryAccessContractTest, also parameterized over the implemented operations. For each operation it reads the capability area and right from x-capability, picks from the permission matrix seed a role whose permission in that area lacks that right, and calls the operation as that role. The expected answer is 403, content type application/problem+json and messageCode MSG-P4-002. An operation that answers 200 instead fails the build with access not enforced, which catches an endpoint that was built without its access check. The content of the permission matrix is owned by the security administrator and loaded by RWB-E1-037, so the test reads it and never defines it.

### Step 8

**In the story.** Build: reports passed, failed and pending operations; any failure fails the build.

The build writes this report, and no person assembles it. Publish it in the build artifacts with every operation of the specification listed as passed, failed or pending, so a reader sees how far the 79 specified operations are covered. Any failure in the lint step, in a compile step, in the contract tests or in the access tests fails the whole build, so a pull request with a broken contract cannot merge. Pending entries do not fail the build. Developers read this report in the build artifacts, since the story has no screen, and the report for release E1 is what the squad checks before the release.

## RWB-TE-004 Masked data in SIT and UAT

Module: P1 Recovery data engine

**Realignment (D-RCV-60).** Stories RWB-PLT-TE004-APP (platform, RWB-PLT-TPL) and RWB-ITG-TE004-ITG (RWB-ITG-W1), release 30 November 2026 (tentative). The data belongs to the services: `sys_fields`, the extension tables and the interaction ledger are rwb-source-data's (P1), and every business table sits in the schema of its owner (Ownership Map; DP-01). The loader stays a tool outside the 19 services.

Delta, step by step:

- Steps 1 and 2 are unchanged: the PII service writes the files and the manifest, and the platform administrator (RW-PLATADM) starts the stage, which holds one advisory lock per environment under SY-DATALOAD behind the flag `rwb.dataengine.masked-copy`. Feature flags are a platform library object (Ownership Map).
- Step 3 is unchanged: the environment guard reads `rwb.maskedcopy.allowed-environments` and refuses DEV and PROD with MSG-P1-002 before any file is opened.
- Step 4: the masking rule version in force is read from rwb-access's masking policy, which owns `masking_rule` (Ownership Map), and `tools.masked_copy_load` stays in the tool's own schema `tools`.
- Step 5 is unchanged in its checks (CTL-02), now applied per service.
- Step 6: the `is_personal` tag is read through the rwb-source-data contract, which owns `sys_fields` (Ownership Map), instead of the loader opening the table; field DF-REF-105 and the three patterns are unchanged.
- Step 7: the staging object becomes one schema per service, `<schema>_next`; each service's swap runs only after the checks of all 19 services pass, one service at a time under the environment lock, so a refusal anywhere leaves every previous copy in use.
- Step 8: the load report gains one section per service, naming the service, the schema, the extract ID, the business date, the masking rule version, the rows per table and the check results.
- Step 9: the case record is read at `GET /api/recovery/case/v1/cases/{caseId}` (P3 rwb-case); the refusal of RW-REFADM with 403 and MSG-P4-002 is unchanged.

### Step 1

**In the story.** PII service: writes the masked extract files and the manifest to the intake container of SIT or UAT.

The bank's PII service does this, and it runs outside the Workbench, so none of it is yours to build. It applies the Compliance masking rules to a copy of recovery data and writes the result as files into the intake container of SIT or UAT, with a manifest beside them. The manifest holds the extract ID, the business date, the masking rule version, the row count per table and the balance totals per table. Later checks compare the files against those numbers, so a load cannot start before the manifest is there. The intake container is a property per environment, rwb.maskedcopy.intake-container, owned by the platform administrator.

### Step 2

**In the story.** Platform administrator: starts the masked copy load in the pipeline for the target environment.

A person starts this. The masked copy load is a pipeline stage for SIT and UAT, started on request by the platform administrator (RW-PLATADM), who also owns the intake containers. It is not scheduled and it is not in the production job list. Build the stage so it takes the target environment as input and holds a lock for that environment, using a database advisory lock, which is a lock held by the connection rather than on any table row. A second start for the same environment while a load is running is refused with MSG-P2-006. The job runs under the SY-DATALOAD identity, and the whole stage sits behind the feature flag rwb.dataengine.masked-copy.

### Step 3

**In the story.** MaskedCopyLoader: refuses to run when the target environment is DEV or PROD.

The job checks this first, and it runs automatically. Write the environment guard as the opening step of MaskedCopyLoader: read the deployment environment and compare it against the property rwb.maskedcopy.allowed-environments, which holds SIT,UAT. For DEV or PROD the job stops with MSG-P1-002 and the check text masked copies load only into SIT and UAT, and it opens no extract file at all. Production data in development is forbidden by NFR-045, which is why this guard runs before any file is read. TC-TE-004-04 starts the stage with the target environment set to DEV and expects that refusal with no file read.

### Step 4

**In the story.** MaskedCopyLoader: checks the manifest: extract ID not loaded before, masking rule version equal to the version in force, schema version equal to the target.

ManifestValidator does this inside the job, with no person involved. It makes three checks. The extract ID must not already appear in tools.masked_copy_load, a small table in the tool's own schema that records each load with its environment, business date, masking rule version and result; a repeat is skipped instead of loaded again, so a second run with the same extract leaves the environment as it is. The masking rule version in the manifest must equal the version in force in the masking rules reference table, for example MASK-2026.11. The schema version must equal the Flyway version of the target database. A mismatch refuses the load in full with MSG-P1-002.

### Step 5

**In the story.** MaskedCopyLoader: runs the load checks of CTL-02 on each file: business date, structure, control totals (row count and balance sum), keys.

The job runs these checks on every file of the extract, automatically. CTL-02 is the set of load checks used for every load: the business date of the file, its structure, its control totals and its keys. The control totals here are the row count and the balance sum per table, compared against the manifest. A loan_account file with 28,118 rows against a manifest of 28,119 is refused in full with MSG-P1-002 and the check text Control totals loan_account 28,118 against 28,119. A refusal at any check leaves the copy already in the environment in use. Balances, dates and keys are never masked, which is what makes these totals comparable.

### Step 6

**In the story.** MaskingVerifier: scans every column tagged is_personal for values that look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number or an email address.

MaskingVerifier runs inside the job and reuses the verifier built in RWB-E1-065, so you wire it in instead of writing the patterns again. It reads the is_personal tag of each field from sys_fields, field DF-REF-105, and scans every column that carries the tag for values that still look personal: a 13-digit number with a valid Thai national ID check digit, a Thai mobile number, or an email address. One hit refuses the whole load with MSG-P1-002 and a check text naming the table and the column, for example unmasked value in party.id_no_token. The value found is never written to the log or the report, only the table and column names.

### Step 7

**In the story.** MaskedCopyLoader: loads the files into a staging schema, checks foreign keys resolve, and swaps the staging schema for the live one in one step.

The job loads the files into the staging schema recovery_next in the target environment, then checks that every foreign key resolves. A foreign key is a column whose value has to exist as a key in another table, for example a case_party row that points at a party row, so this check proves the rows still fit together after masking. Once every check has passed, the job makes the staging schema live in one step, renaming recovery_next to recovery. Leaving that rename to the end is what keeps the previous copy in use when an earlier check fails, and a rerun then starts again from the files in the intake container.

### Step 8

**In the story.** MaskedCopyLoader: writes the load report: extract ID, business date, masking rule version, rows and balance totals per table, check results.

LoadReportWriter writes the report at the end of the job, for the pipeline to publish. It holds the extract ID, the business date, the masking rule version, the row count and balance total per table, and the result of each check. For a skipped repeat it names the earlier load and its date, which is what AC5 expects. Keep data values out of it: counts, totals and check names only, never a field value from the extract. The platform administrator and the squads read this report in the pipeline, because the story has no screen of its own.

### Step 9

**In the story.** Squad member: runs SIT or UAT tests on the masked copy.

People do this work after the load finishes. Squad members holding RW-TRIBE run the SIT or UAT tests against the masked copy with the rights of their test users. They see the copy through the normal screens, with personal fields shown as tokens or masked values. The same customer carries the same token in every table, so joins between party, case_party and loan account rows behave as they do in the extract, and counts and reconciliations match the manifest totals. One access test belongs here: a SIT test user holding RW-REFADM calls GET /api/recovery/v1/cases/{caseId} and is refused with 403 and MSG-P4-002, because that role holds no R right on Case record.

## RWB-TE-006 Outbox and retry for outbound work

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-PLT-LIB: RWB-PLT-TE006-CON and RWB-PLT-TE006-APP (wave 0), plus RWB-ITG-TE006-ITG (RWB-ITG-W1), release 30 November 2026 (tentative). The outbox, inbox and idempotency tables become library objects created in each service's own schema (Ownership Map: `outbox_event`, `outbox_delivery`, `processed_event`, `idempotency_key`, owner PLT).

Delta, step by step:

- Step 1: OutboxWriter is the shared library call, and each service publishes into its own outbox inside its own transaction. The event types of EV-01 to EV-28 keep their names; on the wire they are `rwb.<short>.<Event>.v1` on the owner's topic (DP-14).
- Step 2: one `outbox_event` row and one `outbox_delivery` row per consumer, in the calling service's own schema. The Flyway migration is that service's own sequence (DP-15; H RWB-PLT-E1044-CON); the keys, the status check and the partial index are unchanged.
- Step 3 is unchanged: the change, the event and its deliveries commit together, now inside one service's schema.
- Step 4: JOB-11 is the outbox relay in every service, every minute, with no Quartz job (Ownership Map: JOB-11, PLT, no Temporal Schedule). The batch of 200, the row lock that skips held rows and the lowest open sequence per case and consumer are unchanged.
- Step 5: the consumer is another service reached on Kafka with a CloudEvents 1.0 header, and the inbox table `processed_event` answers the first-time question in place of a shared idempotency table. The stub consumer for the tests is unchanged.
- Steps 6 and 7: RETRY_SUCCEEDED and SYSTEM_UNAVAILABLE are published to `rwb.case.events.v1` and handled by rwb-case (P3); the retry ladder and the read of the delays on each attempt are unchanged.
- Step 8: RETRY_LIMIT_REACHED publishes the same case event, and the decision record is written by the calling service in its own schema through the local decision-record library, then published as DecisionRecorded to `rwb.decision-record.v1`; rwb-decision collects it into the central ledger (DP-03; RWB-PLT-E1027-CON). The one transaction of this step covers the delivery row, the record and the outbox row.
- Step 9: the admin endpoints read across services, so their owner after the split is Not specified in the source documents (GAP-3193; ASM-5585). The rights, the page shape, 409 MSG-P2-022 and 404 are unchanged.

### Step 1

**In the story.** Business service (for example notice approval): calls OutboxWriter.publish inside its own transaction with the event type (an event from EV-01 to EV-28, or an outbound work request type such as WIN_DISPATCH), schema version, case ID, payload references, actor and idempotency key.

The calling service does this in code. No person is involved. Each business service with something to send calls OutboxWriter.publish from inside the transaction that saves its own change. A transaction is one unit of database work that either commits in full or is undone in full, and publish joins the caller's transaction instead of opening its own. The caller passes the event type, which is an event name from EV-01 to EV-28 or an outbound work request type such as WIN_DISPATCH, the schema version, the case ID, which may be empty, a payload of references and codes only, the actor reference and an idempotency key. publish gives back the event ID and throws DuplicateOutboxKeyException when that key already exists.

### Step 2

**In the story.** OutboxWriter: writes one outbox_event row with the next case sequence, and one outbox_delivery row per consumer listed for the event type.

Automatic, inside the caller's transaction. OutboxWriter inserts one outbox_event row with the event type, schema version, case ID, case sequence, idempotency key, payload, actor reference and occurred time. case_seq is the case's highest sequence plus 1, taken under a lock on the case's latest outbox row so two writers cannot claim the same number. OutboxWriter then asks ConsumerCatalog which consumers take that event type and inserts one outbox_delivery row for each, with status PENDING and attempt count 0. Your work is the Flyway migration for the two tables with UNIQUE on idempotency_key, UNIQUE on case_id and case_seq, UNIQUE on event_id and consumer, the status CHECK, and the partial index on next_attempt_at for open deliveries.

### Step 3

**In the story.** Database: commits the change, the event and its deliveries together, or none of them.

The database does this at commit time, with no code of yours running at that moment. Because publish joined the caller's transaction, the business change, the outbox_event row and every outbox_delivery row reach the database in one commit. When the business work fails after publish and the transaction is rolled back, no event and no delivery exist for that item, so the sender has nothing to send. To hold that guarantee, keep publish out of a separate transaction and out of any after-commit hook, which is what BR1 asks for: no event without the change, and no change without the event. Test a commit and a rollback, which is build step 2 of section 13.

### Step 4

**In the story.** JOB-11 Outbox sender (event step): every minute selects due deliveries with a row lock that skips rows another instance holds, oldest case sequence first, taking only the lowest open sequence per case and consumer.

A Quartz job does this, not a person. JOB-11 already runs every minute for outbound files, and this story adds an event step beside that one. OutboxRepository selects outbox_delivery rows whose status is PENDING or RETRYING and whose next_attempt_at is at or before now, up to the batch size of 200 per run. The select takes a row lock and skips rows another instance already holds, so two running instances share the work and no delivery is picked up twice. Rows are ordered by case sequence, oldest first, and only the lowest open sequence per case and consumer is taken. That ordering keeps events for one case reaching each consumer in the order they were written, and holds later events back while an earlier one is failing.

### Step 5

**In the story.** OutboxSender: calls the consumer with the event header (event ID, idempotency key, schema version, occurred time, actor) and payload; each consumer checks the key through IdempotencyGuard (RWB-E1-007) before it acts.

Automatic. For each locked delivery, OutboxSender calls OutboxConsumer.consume on the consumer named in the row and passes an EventHeader with the event ID, the idempotency key, the schema version, the occurred time and the actor, together with the payload. The consumer answers OK or FAILED with a code. Delivery is at least once, so the same call can arrive twice, for example after an instance stops part way. Each consumer therefore calls IdempotencyGuard.firstTime with its own consumer name and the key, and acts only when the answer is true, meaning it has not handled that key before. The consumers themselves belong to other stories, so build a stub consumer that fails on demand for the tests.

### Step 6

**In the story.** OutboxSender: on success marks the delivery DELIVERED; when the delivery had failed before and the consumer holds a case step, raises RETRY_SUCCEEDED for the case (R-UNI-35).

Automatic, inside the sender. On an OK answer, set the outbox_delivery row to DELIVERED, fill delivered_at and leave attempt_count at the number of attempts made. Then check two things: whether this delivery had already failed at least once, and whether the consumer list marks the consumer as holding the case step, which means the case was paused while waiting for it. When both hold, call CaseEvents.raise for the case with event code RETRY_SUCCEEDED, and R-UNI-35 returns the case from RETRY_QUEUE to the state it paused in. For a consumer that does not hold the case step, such as ledger or reporting-feed, mark the delivery and leave the case route state alone.

### Step 7

**In the story.** OutboxSender: on a failure adds 1 to the attempt count and sets the next attempt from the retry settings; on the first failure of a consumer that holds a case step, raises SYSTEM_UNAVAILABLE for the case (R-UNI-33).

Automatic. On a FAILED answer, add one to attempt_count, keep the code in last_error_code, set the status to RETRYING and work out next_attempt_at from the retry settings that ConsumerCatalog reads from rwb.integration.outbox.retry, which hold 3 retries at 1, 5 and 15 minutes after the previous attempt. Read those delays for each attempt rather than once at service start, because a change in the configuration service has to apply to the next attempt. On the first failure of this delivery, and only for a consumer that holds the case step, call CaseEvents.raise with SYSTEM_UNAVAILABLE, which moves the case to RETRY_QUEUE by R-UNI-33 so the person waiting on that case can see why it stopped.

### Step 8

**In the story.** OutboxSender: when the retries are used, sets the delivery to EXCEPTION, raises task RESOLVE_OUTBOX_DELIVERY for the consumer's owner role on the case and, for a consumer that holds a case step, raises RETRY_LIMIT_REACHED (R-UNI-36), which writes the decision log entry; all in one transaction.

Automatic, after the last retry fails. Set the delivery to EXCEPTION, then call TaskApi.raiseTask for the case with task code RESOLVE_OUTBOX_DELIVERY and the owner role named for that consumer, and keep the task ID it returns in task_id. For a consumer that holds the case step, also raise RETRY_LIMIT_REACHED, which moves the case to EXCEPTION_QUEUE by R-UNI-36 and writes the decision log entry through the P7 writer. Wrap all of it in one transaction. When the decision log write fails, everything is undone: the delivery stays RETRYING for the next run, MSG-P7-003 goes to the job log, and R-UNI-39 raises an incident. An event with no case gets EXCEPTION and an alert, with no task and no case event.

### Step 9

**In the story.** Platform administrator: reads exception deliveries (GET /admin/outbox/deliveries) and, once the consumer is fixed, sends one again (POST /admin/outbox/deliveries/{deliveryId}/resend).

A person does this, the platform administrator, once the consumer behind the failures works again. Build OutboxAdminController with both endpoints. The GET takes status, consumer, eventType, from, to, page and size, returns a page of OutboxDelivery items without the payload, and needs Platform administration right R. The POST needs right U, sets the delivery to PENDING with attempt count 0 and due at the next run, answers 200 with MSG-GEN-005, and is written to the ACE audit log with the user and the time. A delivery that is not in EXCEPTION is refused with 409 and MSG-P2-022, which also covers a second call on a delivery already set back to PENDING. A delivery that cannot be found gives 404.

## RWB-TE-007 Scheduled jobs on Quartz

Module: P3 Case and workflow

> **Retired (D-RCV-60).** RWB-TE-007 is retired, as Template and Rules section R6 sets out: there is no new story, and every dependency on TE-007 points to RWB-PLT-E1071-CON. Quartz, its cluster job store and the shared job tables are replaced by Temporal Schedules in the owning service (Arch v5 slide 44). The nine steps stay in this document, word for word, so the as-built notes remain traceable; the table below gives the target for each step (ASM-5581). The mechanism this section describes is out of date against Arch v5 slide 44 (GAP-3189).

| Step | v2 mechanism | Target under D-RCV-60 |
|---|---|---|
| 1 | DailyJobTrigger on LoadCompleted and on the completion of JOB-02 | AceDataReady (EV-26) starts DailyCaseRun in rwb-case; JOB-03 is a step of that run and JOB-04 an event-triggered workflow in rwb-source-data (Ownership Map: JOB-03 P3, JOB-04 P1) |
| 2 | JOB-05 Timer check every 5 minutes on cron in Asia/Bangkok | retired: durable timers inside each workflow, and no 5-minute timer check (Ownership Map: JOB-05, PLT) |
| 3 | Quartz cluster lock over one shared job store | one task queue per service, `rwb-<short>`, with the Schedule overlap policy that keeps one run at a time |
| 4 | job run log, JobRunRecorder.lastSucceeded, SKIPPED | the run record is the workflow history of the Schedule; a successful run for the business date answers the same question |
| 5 | dependsOn, WAITING and MSG-P3-031 | unchanged in intent, with the dependency an event or a completed child workflow |
| 6 | JobRunRecorder.start and finish, read on SCR-44 | workflow history of the Schedule plus the job monitor RWB-PLT-E1056-OPS; `/admin/jobs` in the owning service (DP-13) |
| 7 | CatchUpOnStart capped by `jobs.catch-up.max-dates` | the Schedule's catch-up window, capped the same way; the values come through the parameters contract of rwb-case (DP-06; H RWB-PLT-E1042-CON, C RWB-P3-E1042-CON) |
| 8 | DeadlineWatcher at 07:00 | a second Schedule in rwb-case; the alert route RWB-PLT-E1056-OPS is unchanged |
| 9 | SCR-44 and `POST /admin/jobs/{jobId}/rerun` | per-service admin jobs endpoint under the owner's base (DP-13); 409 MSG-GEN-004, 403 MSG-P4-002 and 404 unchanged |

### Step 1

**In the story.** Scheduler: on LoadCompleted for business date D, and on completion of JOB-02 for D, fires JOB-03 Morning allocation and JOB-04 Daily reconciliation for D.

No person triggers the daily runs. Build DailyJobTrigger as a listener on two signals: LoadCompleted (EV-26), which JOB-01 publishes with the business date when the COLLINS load passes its checks, and the completion of JOB-02 case creation for that same date. When both have happened for business date D, it schedules JOB-03 Morning allocation and JOB-04 Daily reconciliation for D on the Quartz scheduler. The date is passed into the job, because a job body never works out its own business date from the clock (section 17). JOB-03 has to finish by 07:00. JOB-01 and JOB-02 belong to P1 and are out of scope here, so treat them as signals you listen for.

### Step 2

**In the story.** Scheduler: fires JOB-05 Timer check every 5 minutes on cron `0 0/5 * * * ?` in Asia/Bangkok.

Automatic and time-based. RecoveryJobRegistry schedules JOB-05 Timer check with the cron expression 0 0/5 * * * ? in the Asia/Bangkok zone. A cron expression is a schedule written as fields for second, minute, hour, day, month and weekday, and this one fires at second 0 of every fifth minute. Take the expression from jobs.timer-check.cron in the configuration service rather than writing it into the code. The idempotency key of JOB-05 is its fire time slot rather than a business date. Its misfire instruction is to do nothing, so a fire missed while the service was down is never repeated, and the next run picks up the timers that are due by then.

### Step 3

**In the story.** Job runner: takes the cluster lock so only one instance runs a job at a time.

The scheduler does this, with no code of yours running at the moment of locking. The ACE service runs on more than one instance, and all of them share one Quartz job store in PostgreSQL with isClustered set to true. The job store hands each fire to a single instance, so the same job does not run twice. BusinessDateJobRunner carries @DisallowConcurrentExecution, which holds back a second run of the same job while one is still going, and requestsRecovery, which lets another instance pick the job up when the instance running it stops. That pair gives AC4, where a JOB-05 run of 7 minutes delays the 10:05 fire, and AC8, where ACE-2 takes over inside the 20 second check-in interval.

### Step 4

**In the story.** Job runner: checks the job run log for job and business date; if a successful run exists, records the skip and stops.

Automatic, as the first check inside BusinessDateJobRunner. Call JobRunRecorder.lastSucceeded with the job ID and the business date. When it answers with a run, do no work: write a SKIPPED entry to the P1 job run log and return. This is what makes a repeated fire for a date that already succeeded harmless, so JOB-03 allocates no case a second time. The job bodies are also idempotent for their business date (BR8), meaning a second run for the same date leaves the same result, and this check keeps them from being called at all. The job run log belongs to the P1 job monitor of RWB-E1-056 and is reached only through JobRunRecorder, never by reading its tables.

### Step 5

**In the story.** Job runner: checks the job's dependency (JOB-02 succeeded for D); if not met, records WAITING and stops.

Automatic, as the second check. Each BusinessDateJob names its dependencies through dependsOn, for example JOB-02 for JOB-03. The runner asks JobRunRecorder.lastSucceeded for each named job ID and the same business date. When one of them has not succeeded, write the run as WAITING with MSG-P3-031 naming the job that is missing, and stop without calling the body. Nothing retries from inside the runner. The run happens later, when the dependency succeeds for that date and DailyJobTrigger fires the job again, which is what AC7 asks for after JOB-02 succeeds at 08:10. The platform administrator can also start a WAITING run through POST /api/recovery/v1/admin/jobs/{jobId}/rerun.

### Step 6

**In the story.** Job runner: records the run start through the P1 job monitor, runs the job body, records the end with status SUCCEEDED or FAILED and the counts.

Automatic. Call JobRunRecorder.start with the job ID, the business date and the instance name, keep the run ID it gives back, then call run with that business date on the BusinessDateJob. The body itself comes from another story: allocation from RWB-E1-020, reconciliation from RWB-E1-011 and the timer check from RWB-E1-028. Whatever the outcome, call JobRunRecorder.finish with the run ID, the status SUCCEEDED or FAILED, and the counts the body produced. Put the finish call in a finally block, so a failure is recorded rather than lost. Those entries are what the platform administrator reads on SCR-44 with the business date and status. Logs carry job IDs, dates and counts, with no personal data.

### Step 7

**In the story.** Job runner: on service start, for each business date of a passed COLLINS load with no successful run of JOB-03 or JOB-04, runs the job for that date in date order, up to `jobs.catch-up.max-dates` dates.

Automatic at service start, in CatchUpOnStart. Find every business date whose COLLINS load passed and that has no successful run of JOB-03 or JOB-04, then run the job for each of those dates in date order, oldest first, so an outage of three days gives three runs one after another. The number of dates is capped by jobs.catch-up.max-dates, which is 5 in the configuration service. When more dates than that are missing, start no automatic run and send an alert with MSG-P3-031 naming the job and the dates, which leaves the decision to the platform administrator. Pass each date into the job body, because the body takes the date it is given.

### Step 8

**In the story.** Deadline watcher: at 07:00 checks JOB-03 for the current business date; if it has not succeeded, alerts the operations channel.

Automatic, and separate from the allocation job. DeadlineWatcher is its own Quartz job on a cron at 07:00 Asia/Bangkok, with the time taken from jobs.allocation.deadline in the configuration service. It asks JobRunRecorder.lastSucceeded for JOB-03 and the current business date. When there is no successful run, it sends an alert with MSG-P3-031 naming JOB-03, the date and 07:00 to the operations channel through the alert route of RWB-E1-056, and that alert has to arrive within 15 minutes, so by 07:15. The watcher only reports. It does not start JOB-03 itself and it does not change any run status.

### Step 9

**In the story.** Platform administrator: reads runs on SCR-44 and reruns a failed run through `POST /admin/jobs/{jobId}/rerun`.

A person does this. The platform administrator opens SCR-44 Interface and job monitor, in its Running, Failed and Complete states, and reads each run of JOB-03, JOB-04 and JOB-05 with its business date and status. The screen reads GET /api/recovery/v1/admin/jobs, which gives back id, type, businessDate, status, startedAt, endedAt and checks, and needs Platform administration right R. A rerun calls POST /api/recovery/v1/admin/jobs/{jobId}/rerun with right U and runs the job again for its own business date when that run is FAILED or WAITING. A run that already succeeded answers 409 with MSG-GEN-004 and runs nothing. A role without the right is refused with 403 and MSG-P4-002, and a run that cannot be found gives 404.

## RWB-TE-008 Decision log hash chain check

Module: P7 Decision center and log

**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, stories RWB-PLT-TE008-APP and RWB-ITG-TE008-ITG (RWB-ITG-W1), release 30 November 2026 (tentative). The check becomes a capability: one Temporal Schedule template in the workflow kit, one chain-check library in the service template, and one instance for the central ledger in rwb-decision (JOB-14: owner P7, mechanism Schedule, 02:00, Ownership Map).

Delta, step by step:

- Step 1: JOB-14 is a Temporal Schedule in rwb-decision, in namespace rwb-recovery on task queue rwb-decision; no Quartz table is written (DP-10; H RWB-PLT-E1071-CON).
- Step 2: the 01:00 copy is retired (RWB-E1-014 retired; Ownership Map: JOB-13 is continuous ingest on Kafka), so the run waits for the business date's ledger ingest to report complete instead of waiting for JOB-13. The latest start of 04:00 and the note on the run record are unchanged.
- Step 3: the end `chain_seq` is read per chain, inside the schema of the service whose instance runs; the central ledger's chain is read only through RWB-P7-E1008-CON (DP-01).
- Step 4: the canonical form is the shared local decision-record library (DP-03; RWB-PLT-E1027-CON), never a second copy.
- Step 5: the failing count and the first break are unchanged; the run reads one chain at a time and never writes to another service's table.
- Step 6: the run record is the workflow history of the Schedule, with the same fields (entries checked, last chain_seq, last entry_hash, result, first break, failing count), and not an ACE job run row.
- Steps 7 and 8: MSG-P7-007, MSG-P7-008 and MSG-P7-013 are unchanged, and a service with no chain instance is reported as not covered rather than intact.
- Step 9: the rerun is the Schedule's rerun under the owner's base, `/api/recovery/decision/v1/admin/jobs/{jobId}/rerun` (DP-13); a rerun is a new run, 409 MSG-GEN-004 and 403 MSG-P4-002 are unchanged.

### Step 1

**In the story.** Quartz: fires JOB-14 at 02:00 Asia/Bangkok for the business date of the previous day.

Quartz is the job scheduler added to the ACE service in RWB-TE-007, and it starts this run with no person involved. Add JOB-14 to it using the cron expression 0 0 2 * * ? in the Asia/Bangkok time zone. A cron expression is the schedule text the scheduler reads to work out the next fire time. Mark the job DisallowConcurrentExecution so that only one run is active at a time. Take the start time from the parameter rwb.decision.chaincheck.start rather than writing 02:00 into the code. Each firing works on the business date of the previous day, because those are the entries the check covers, so pass that date into the job and keep it on the run record.

### Step 2

**In the story.** Job (HashChainCheckJob): checks that JOB-13 for the same business date has ended; if not, waits and checks again every 5 minutes until 04:00, then runs and records that JOB-13 had not ended.

The job makes this check itself, with no operator involved. JOB-13 is the nightly decision log copy, scheduled at 01:00 in RWB-E1-014, and the check has to run after it for the same business date. Build code that looks up the JOB-13 run for that date and sees whether it has ended. When it has not, sleep and look again every five minutes, up to the latest start held in rwb.decision.chaincheck.latest-start, which is 04:00. At 04:00 begin the check anyway and write a note on the run record that JOB-13 had not ended. When JOB-13 ends earlier, start at that moment and keep its end time. Use a clock you can replace in tests, because AC6 needs fixed times.

### Step 3

**In the story.** Job: reads the highest chain_seq at the start and fixes it as the end of the run; entries appended later are checked the next night.

The job reads this value on its own at the moment it begins. chain_seq is the running sequence number on each decision log entry, and the log only grows, since RWB-E1-008 blocks updates and deletes in the database. Query the highest chain_seq once, hold it in the run, and treat it as the last entry of this run. Every entry written after that point falls outside the run and is covered the following night. Reading the end point once keeps the result stable: the count of entries checked, the last chain_seq and the last entry_hash all match the same fixed end, even while the service keeps appending entries during the time the run takes.

### Step 4

**In the story.** Job: calls HashChainVerifier over chain_seq 1 to the end in batches of 1,000, recomputing each entry_hash and checking each prev_hash.

The job calls HashChainVerifier, which already exists from RWB-E1-008. The hash chain works like this: each entry carries entry_hash, computed from the canonical form of its own fields, and prev_hash, which holds the entry_hash of the entry before it. Recompute entry_hash for every entry and compare prev_hash with the hash you computed for the preceding one. Any difference means the entry changed after it was written. Read the entries in chain_seq order through the unique index on that column, in groups of 1,000 taken from rwb.decision.chaincheck.batch-size, so that millions of entries do not load into memory at once. Use the same canonical form implementation as the store, never a second copy.

### Step 5

**In the story.** Job: counts every entry that fails and keeps the first.

The verifier from RWB-E1-008 stops at the first problem, so extend it for this job. Keep going after a failing entry, count every entry whose entry_hash or prev_hash does not match, and hold the chain_seq and entry ID of the lowest failing one as the first break. AC7 shows what this gives: with chain_seq 12,001 and 40,350 both changed, the first break is 12,001 and the failing count is 2, and one report names both entry IDs. The counting happens inside the run with no person involved. Do not repair anything and do not write to decision_log_entry; the job only reads and reports.

### Step 6

**In the story.** Job: writes the job run record with type JOB-14, business date, status and checks: entries checked, last chain_seq, last entry_hash, result, first break chain_seq and entry ID, failing count.

JobRunRecorder writes this through the scheduler interface built in RWB-TE-007, automatically at the end of the run. The record goes to the ACE job run record in the Job schema, not to a recovery table. Fill type JOB-14, the business date, status, startedAt and endedAt, and the checks block: entriesChecked, lastSeq, lastHash, result, breakSeq, breakEntryId and failingCount. Result is INTACT or BROKEN, and status is COMPLETED or FAILED. A failed run still writes what it reached, as AC3 shows with 20,000 entries checked. These records are what GET /api/recovery/v1/admin/jobs lists for the job monitor, so internal audit and the platform administrator can read any night's result.

### Step 7

**In the story.** Job: sends MSG-P7-007 to Compliance when the chain is intact, or MSG-P7-008 with an incident when it is broken.

ChainCheckReporter sends this on its own as the run ends, through the ACE notification path to the Compliance and PDPA officer group. Build it with the three messages of section 14. On an intact chain send MSG-P7-007 with the entry count and the last hash. On a break send MSG-P7-008 with the entry ID, and raise an incident at the same time; the security administrator receives that incident with Compliance. An empty log counts as intact, with count 0 and the genesis hash, so MSG-P7-007 goes out. When the run is a rerun, mark the report as a rerun. Each message needs Thai text as well as English, following DL10.

### Step 8

**In the story.** Job: on an error that stops the run, records status FAILED, alerts the platform administrator and sends MSG-P7-013 to Compliance.

This path runs by itself when the run cannot finish, for example when the database connection is lost part way. Catch the error, write the run record with status FAILED and the entries checked so far, alert the platform administrator group, and send MSG-P7-013 to Compliance with the date the chain was last confirmed. That last date comes from earlier run records, so your query has to find the most recent completed run. A failed run is never resumed from the point where it stopped. Compliance learns the same night that the check did not complete, which is why this message names the last confirmed date in place of a result.

### Step 9

**In the story.** Platform administrator: can rerun the job for the business date from the job monitor; a rerun is a new run record.

A person does this. The platform administrator, holding RW-PLATADM, calls POST /api/recovery/v1/admin/jobs/{jobId}/rerun from the job monitor, which needs Platform administration U. Internal audit may read the run records and may not rerun, so a caller without that right gets 403 with MSG-P4-002. The rerun starts again from chain_seq 1 and writes a second run record for the same business date with rerun true, leaving the first record in place. Business date plus run number is the key, so the history shows both attempts. Return 409 with MSG-GEN-004 when a run is already active, and keep the scheduler guard so that no scheduled start begins while the rerun works.

## RWB-TE-009 Performance test harness

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-ITG-NFR, story RWB-ITG-TE009-ITG, release 31 December 2026 (tentative). Suggested owner: QA team (suggested; any team may pick up this story). The harness stays in `perf/recovery`, outside the service.

Delta, step by step:

- Steps 1 and 2 are unchanged: the release stage, the manual start by a squad member holding RW-TRIBE, the SIT lock, the refusal text and the 90 minute limit.
- Step 3: the open-case count is read at `GET /api/recovery/case/v1/cases` (P3 rwb-case); 23,600 open cases and the refusal text are unchanged.
- Step 4 is unchanged: the same roles and SIT test users, each calling through gateway-bff with the rights of its own role.
- Step 5: 410 virtual users, 10 ramp minutes, 60 steady minutes, 3 requests a minute and the MIX-2026.12 weights are unchanged; each call is one hop to the owner service with the 2 second timeout (DP-11). Which service owns each of the 7 operations of the mix is Not specified in the source documents (GAP-3191; ASM-5583).
- Steps 6 to 8 are unchanged: per-operation percentiles, throughput and error rate over the steady hour, and the exclusive 2,000 ms and 1 percent limits.
- Step 9: the reload of the masked copy is the stage of RWB-PLT-TE004-APP, which loads the 19 schemas.

### Step 1

**In the story.** Release pipeline: starts the SIT performance stage for the build, or a squad member starts it by hand.

Either the pipeline starts this or a person does. Add a performance stage to the release pipeline that runs in SIT before the UAT exit, so that a build reaches the gate without anyone asking. Also allow a squad member holding RW-TRIBE to start the same stage by hand, which is how a run happens outside a release. The build under test must already be deployed to SIT with the feature flags planned for the release, and an SIT slot must be booked, so the stage works against a known deployment. This is a pipeline stage, so it gets no entry in the job list and no Quartz schedule. The harness code sits in perf/recovery and does not ship inside the service.

### Step 2

**In the story.** Harness: takes the SIT run lock; refuses to start when another run holds it.

The harness takes the lock itself at the start of a run. Build RunLock so that only one run is active in SIT at a time: the second caller is refused with run already in progress, while the first run carries on. The reason is shared data; two loads at once on the same masked copy would make both sets of numbers meaningless. Give each run its own run ID. Release the lock when the run ends, and release it after 90 minutes at most, so a run that stops part way does not block SIT; that run is marked failed. The limit matters because a full run is 10 ramp minutes plus 60 steady minutes.

### Step 3

**In the story.** Harness: counts open cases through GET /api/recovery/v1/cases and refuses to start when fewer than 23,600 are found.

DataVolumeCheck does this automatically before any load. Call GET /api/recovery/v1/cases and count the open cases in SIT. When the count is below 23,600, refuse the run and write data volume below the test base with the count found and the base, as AC4 shows with 9,800 of 23,600. The check exists because response times depend on data volume; a screen that is fast on a small set can be slow on the real one. RWB-TE-004 loads the masked copy that holds at least 23,600 open cases, so a low count means the SIT data was not loaded or was reduced. No load starts and nothing else is reported.

### Step 4

**In the story.** Harness: signs in the test users for each role in the mix.

The harness signs in by itself, using the named SIT test users listed per role in its configuration, with Entra ID groups per DL40. The mix covers RW-CASEOWN, RW-TEAMMGR, RW-LITOFF and RW-PHONECOL, and each simulated user calls the API with the rights of its own role. That matters for the expected refusal: a RW-PHONECOL user calling postCasesCaseidTransfer gets 403 with MSG-P4-002, which the run counts as expected. Hold the sign-in tokens for the length of the run so that sign-in work does not appear in the measured steady period. Read the user list from configuration rather than writing names into the load script.

### Step 5

**In the story.** Harness: ramps to 410 virtual users over 10 minutes, then holds 60 minutes at 3 requests a minute per user, following the weights in the mix file.

The harness drives this load with no person watching. Build BusiestHourSimulation to raise the number of virtual users to 410 across 10 minutes, then hold that level for 60 minutes with each user making 3 requests a minute. A virtual user is a simulated session the script drives, and it represents one of the 370 staff and 50 partner users online in the busiest hour. Pick each request from the weights in the mix file, so with MIX-2026.12 about 30 percent are getCases and 15 percent are getCasesCaseidTimeline. The steady hour is the part that gets measured, and the ramp only brings the load up to that level. Read the user count, rate, durations and weights from configuration.

### Step 6

**In the story.** Harness: records the response time and status of each request; 403 responses on operations the mix marks as refusals count as expected.

The harness records every request as it runs. Store the operation name, the response time in milliseconds and the HTTP status of each call, with the run ID and the mix file version. Treat status 403 as expected when the mix file marks that operation as a refusal for that role, so the planned refusal of postCasesCaseidTransfer for RW-PHONECOL does not count toward the error rate. That refusal still has to answer inside the 2 second target, which is what the access test proves. Keep the ramp requests apart from the steady ones, because the percentiles and the error rate are computed on the 60 steady minutes only. Hold operation names and numbers, with no personal data.

### Step 7

**In the story.** Harness: computes the 50th, 95th and 99th percentiles, the throughput and the error rate per operation over the 60 steady minutes.

The harness computes these numbers after the steady period, with no person involved. For each of the 7 operations in the mix, work out the 50th, 95th and 99th percentile response time, the throughput and the error rate. A percentile is the time that a share of requests came in under: a 95th percentile of 1,800 ms means 95 of every 100 calls answered within 1,800 ms. Compute them for each operation on its own, because one slow operation would otherwise hide behind six fast ones. Use only the 60 steady minutes. At 410 users and 3 requests a minute that is about 73,800 requests, which is the sample the report and the gate work from.

### Step 8

**In the story.** Gate: passes when every operation's 95th percentile is under 2,000 ms and the error rate is under 1 percent; otherwise fails the stage.

PerformanceGate decides this in code, with no human judgment. It passes when every operation's 95th percentile is below 2,000 ms and the error rate over the steady period is below 1 percent. Both limits are exclusive: 2,000 ms exactly fails and 1,999 ms passes, and 740 errors in 74,000 requests is 1.0 percent and fails. A failing gate fails the release stage, and the report names the operation with its 95th percentile and the limit. Read both limits from the harness configuration so that they can change without code. Write this component first and test it against result fixtures, which are saved result files in place of live runs, so the boundary cases are quick to prove.

### Step 9

**In the story.** Harness: attaches the report to the release record with the build ID, releases the lock and triggers the reload of the masked copy.

ReportPublisher does this at the end of the run. Attach the report to the release record with the build ID and the mix file version, so that the release team can see which configuration produced the numbers. A repeated run for the same build adds another report and leaves the earlier one in place, and the gate result for that build comes from the latest run, as AC6 shows with a failed run at 10:00 and a passing run at 14:00. Then release the SIT lock so that another run may start, and trigger the reload of the masked copy, because the run wrote interaction rows through postCasesCaseidInteractions and SIT has to go back to a known set.

## RWB-TE-010 Browser and accessibility tests

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-ITG-NFR, story RWB-ITG-TE010-ITG, release 31 December 2026 (tentative). Suggested owner: QA team (suggested; any team may pick up this story).

Delta, step by step:

- Steps 1 to 9 are unchanged in intent: the stage, browsers.json, the sign-in per role, the six screens by their states by four browsers, the WCAG 2.1 A and AA scan in Thai and English, the keyboard check, the exception list, the single retry and the failing stage.
- The screens are composed by gateway-bff from the owner services (DP-19; H RWB-PLT-N001-CON), so a screen that calls a service base directly fails the front end build (RWB-PLT-TE001-APP-2).
- The MSG-P4-002 refusal on SCR-05 for RW-PHONECOL comes from rwb-access through the guard; the synthetic data set and the test users stay as v2 has them, in the stories of RWB-E1-065.

### Step 1

**In the story.** Pipeline: starts the browser stage after the front end build on each pull request, and nightly against SIT.

The pipeline starts this on its own, in two places. Add a browser stage that runs after the front end build on each pull request, so that a developer gets the result before merge, and schedule the same stage nightly against SIT. No person starts it in normal work, though a squad member holding RW-TRIBE may run it. The tests live in ace-web/e2e/recovery in TypeScript with their configuration in ace-web/e2e/recovery/config, and they do not ship inside the service, so there is no feature flag. The stage holds no state of its own, which is why a rerun is the same stage run again. The runner needs a test deployment with the synthetic data set of RWB-E1-065 and test users per role.

### Step 2

**In the story.** Runner: reads `browsers.json` and refuses to start when a listed browser is missing.

BrowserGuard does this check first, automatically, before any test. browsers.json is the configuration file that lists the browser names and versions under test: Chrome N, Chrome N-1, Edge N and Edge N-1, where N is the current major version in the runner image. Read that file and confirm each listed browser is present in the image. When one is missing, fail the stage at once with browser not available and the browser and version, as AC5 shows for Chrome N-1. A missing browser is always a failure and is never skipped, because a silent skip would let a screen ship untested on a browser the bank supports. Keep the version list in the file, never in the test code.

### Step 3

**In the story.** Runner: signs in the test user of each role in the screen list.

The runner signs in by itself, with no person at the keyboard. screens.json gives the roles for each screen, and the runner uses the SIT test user of each of those roles: RW-CASEOWN, RW-TEAMMGR, RW-PLATADM and RW-PHONECOL. Each user sees the screens with its own rights, which is what makes the refusal test real: a RW-PHONECOL user opening SCR-05 sees MSG-P4-002 and no Save control at all. Build the sign-in as a reusable step the suite calls for each role and each browser, since every browser session needs its own sign-in. Take the user list from configuration rather than writing names into the tests.

### Step 4

**In the story.** Runner: opens each main screen (SCR-02, SCR-03, SCR-04, SCR-05, SCR-07, SCR-09) in each listed state and runs its functional test on each browser.

The runner opens the screens and drives them automatically. Build ScreenSuite to work through the six main screens of screens.json, SCR-02, SCR-03, SCR-04, SCR-05, SCR-07 and SCR-09, and for each one through every state listed for it, for example SCR-03 in Loading, Read only, Editable and On hold. Run each screen's functional test on all four browsers, so the suite covers six screens by their states by four browsers. A fault on one browser alone still fails the stage, and the report names the screen, the browser version and the failed check, as AC3 shows for SCR-02 on Edge N-1. The states come from the configuration file, so adding a state needs no new test code.

### Step 5

**In the story.** Runner: runs the accessibility scan with the WCAG 2.1 A and AA rule tags on each screen and state, in Thai and in English.

AccessibilityScan runs this without a person looking at the screen. For every screen and every one of its states, run the scan engine twice, once with the English labels and once with the Thai ones, and select the rule tags for WCAG 2.1 level A and level AA. WCAG 2.1 AA is the accessibility level the bank's screens have to meet, and a rule tag is how the scan engine groups its checks, so selecting those tags runs the checks that belong to that level. Any violation gives the screen, the state, the language, the rule and the element, for example rule button-name on SCR-02 in state List. Both languages are needed because Thai text changes layout and label length.

### Step 6

**In the story.** Runner: runs the keyboard test: every primary action is reachable and usable by keyboard with a visible focus.

KeyboardCheck runs this automatically as part of the stage. For each primary action named in screens.json, prove that the action can be reached with the Tab key, that it can be used from the keyboard, and that the focus is visible when it is reached. Focus is the browser's mark of the control that keyboard input reaches, and a user with no mouse depends on seeing it. A failure fails the stage with keyboard access, the screen and the action, as AC8 shows for Save on SCR-05. Build the check to walk the tab order rather than clicking, since a control that answers only a mouse click can pass a functional test and still block a keyboard user.

### Step 7

**In the story.** Runner: compares each violation with the exception list; an entry past its expiry date does not excuse the violation.

The runner applies the exception list itself, with no review during the run. a11y-exceptions.json holds each excused violation with the screen, the rule, an owner, an expiry date and a reason. For every violation the scan reports, look for an entry matching that screen and rule. When the entry exists and its expiry date is still ahead of the run date, the violation does not fail the stage. When the expiry has passed, the violation fails the stage and the report says exception expired with the screen, the rule and the date, as AC6 shows for color-contrast on SCR-07 in a run on 4 January 2027. Reject any file entry that has no owner or no expiry date.

### Step 8

**In the story.** Runner: retries a failed functional test once and lists a test that passes only on retry as flaky.

The runner handles the retry on its own. When a functional test fails, run that one test a second time. A test that passes on the second run goes into the flaky list of the stage report with its screen and name, for example the SCR-04 filter test. Flaky means the test gives a different result on the same code, which usually comes from a timing problem in the test rather than a defect in the screen. Only one retry is allowed, so a test that fails twice is a real failure. Build the retry around the single failing test rather than the whole suite, and keep the flaky list in ReportWriter so that the squad can see which tests need fixing.

### Step 9

**In the story.** Pipeline: fails the stage on any violation, functional failure or missing browser, and attaches the report.

The pipeline does this, with no person deciding. Fail the stage when any WCAG 2.1 A or AA violation remains after the exception list is applied, when any functional test fails on any browser, or when a listed browser is missing from the runner image. Attach the report either way, covering each screen, state, language and browser with its functional result, its violations with rule and element, the keyboard result and the flaky list. A failed stage blocks the merge of the pull request, which is the reason the stage runs before merge. Developers read that report in the pipeline, so name the screen, the state, the language and the element in plain text.

## RWB-TE-011 PDPA lint for code, tests and logs

Module: P2 Integration

**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, story RWB-PLT-TE011-APP, release 30 November 2026 (tentative). Suggested owner: TechX (suggested; any team may pick up this story).

Delta, step by step:

- Step 1: the personal field list is read from the `sys_fields` seed owned by rwb-source-data (P1, Ownership Map) and from the `x-personal-data: true` marking of the 19 service API files plus gateway-bff, instead of one specification. BR1 is unchanged.
- Step 2: the generated rules cover every service package `th.co.scb.ace.workbench.recovery.<short>` and the front end source; `pdpa-rules.yaml` and its six rules are unchanged.
- Steps 3 to 6 are unchanged, including the allow list approved by the TechX tech leads as code owners (RWB-TE-002).
- Step 7: the step runs in each repository's pull request build and on every build of main; the output format and the refusal to print a value found are unchanged.

### Step 1

**In the story.** Build: reads the personal fields from the sys_fields seed and the API specification.

No person types this list by hand. The build reads it, through the PersonalFieldReader service you write under tools/pdpa-lint. It takes two sources: the is_personal column of the sys_fields metadata seed in the schema, and the x-personal-data: true marking in the API specification. A seed here is a file of starting rows for a table, and this story adds no database access, so the lint opens the file itself. Rule BR1 says the personal field list is never written inside the lint, so when Compliance marks a new field in the dictionary the next build picks it up with no code change.

### Step 2

**In the story.** Build: generates the lint rule set from the field list: Java getter names, entity class names, JSON property names and TypeScript property names.

The build generates the rules, and nobody edits the generated file by hand. Write RuleGenerator, which turns each personal field name into the forms a developer would really write in code: the snake case name from the schema, the Java getter, the camel case property used in JSON and TypeScript, and the class name of an entity that holds such a field. It writes them to pdpa-rules.yaml, which carries the six rules listed in section 12: PDPA-LOG-FIELD, PDPA-LOG-ENTITY, PDPA-EXCEPTION, PDPA-TOSTRING, PDPA-FIXTURE-FIELD and PDPA-FIXTURE-ID. Generating the file on every run is what makes scenario AC5 work. When contract_no is marked personal, the next build already has a rule for contract_no and for getContractNo.

### Step 3

**In the story.** Lint: scans `src/main` and the front end source for log calls, string building in log calls and exception messages that use a personal field or a whole personal entity.

The scan runs on its own in the pipeline. Your work is the Java and TypeScript rules of build step 2 in section 13. They read the back end source under src/main and the front end source, and they look at every place that writes text out: a logger call, a string joined together inside a logger call, and the message given to an exception. A finding is raised when such a place uses a personal field, as in party.getFirstName() for AC1 and console.log(party.lastName) for AC7, or passes a whole personal entity object, as in a PartyEntity for AC2. An exception message built with getCifNo() is rule PDPA-EXCEPTION in AC9.

### Step 4

**In the story.** Lint: scans `src/test`, end-to-end tests, SQL seed files and JSON fixtures for literals in personal field positions that do not start with "SYN-", and for values that match a Thai national identifier with a valid check digit, a Thai mobile number or an email address outside the example domains.

This scan is also automatic. Write the fixture rules and the CheckDigitMatcher service. They read src/test, the end-to-end tests, the SQL seed files and the JSON fixtures. Two kinds of finding come out. First, a literal sitting in a personal field position that does not begin with the synthetic prefix SYN-, so last_name set to TESTNAME fails and last_name set to SYN-LAST-0001 passes, as AC4 shows. Second, a value anywhere that looks like real contact or identity data: a Thai national identifier whose check digit is valid, a Thai mobile number, or an email address outside the example domains. A check digit is an extra digit computed from the other digits, which lets the lint test a number for validity instead of counting its length.

### Step 5

**In the story.** Lint: checks that each entity with a personal field excludes it from its text form.

A rule does this for you at build time. The text form of an entity is the string the class returns when it is printed, usually from its toString method, and anything in it reaches a log line as soon as the object is printed. The rule reads each entity class that holds a personal field and checks the field is left out of that text form. When ContactPointEntity keeps value_token in its text form, the build fails with rule PDPA-TOSTRING and names value_token, which is scenario AC10 and rule BR5. Removing the field from the text form is the fix, and the masking helper remains the way to print a value when a log line has to name a record.

### Step 6

**In the story.** Lint: compares each finding with the allow list; an entry past its expiry does not excuse the finding.

The comparison is automatic, and the entries behind it are written by people. Each finding is matched against pdpa-allow.yaml, where an entry carries the rule, the path, a line or pattern, an owner, a reason and an expiry date. Only an entry whose expiry date has not passed excuses a finding. With an entry for PDPA-FIXTURE-FIELD that expires on 30 November 2026, a run on 1 December 2026 fails and prints allow entry expired with the rule, the path and the date, as AC6 and section 14 set out. Adding or changing an entry needs a pull request approved by the TechX tech leads as code owners. The repository host refuses the merge when someone else approves it.

### Step 7

**In the story.** Pipeline: fails the build on any finding and prints the rule, the file, the line and the field, without printing the value found.

The pipeline does this, on every pull request and every build of main. Write PdpaLintStep and add it to the pull request pipeline. One finding is enough to fail the build, and the output gives the rule, the file, the line and the field name in the form of section 14: the rule, then file and line, then the personal field used, then the advice to remove it or use the masking helper. The value found is never printed, which is rule BR7. The step keeps no state of its own, so the same commit with the same dictionary gives the same findings every time, and a failed run can be repeated by starting the pipeline again.

## RWB-TE-012 Document storage containers

Module: P5 Document hub

**Realignment (D-RCV-60).** Epic RWB-PLT-TPL, story RWB-PLT-TE012-APP, release 30 November 2026 (tentative). The containers are used by rwb-document (P5) only, which owns `document`, `document_custody` and `retention_rule` (Ownership Map).

Delta, step by step:

- Step 1: the infrastructure template is unchanged and still creates `rwb-intake`, `rwb-docs`, `rwb-docs-legal` and `rwb-quarantine` once per environment.
- Step 2: the Storage Blob Data Contributor role goes to the rwb-document managed identity (one login per service, DP-02) instead of a shared ACE service identity; SY-OCR and its three containers are unchanged, as are versioning, soft delete and the immutability policy.
- Step 3: StorageReadinessIndicator joins the rwb-document `/health` endpoint and reports ready only when the four containers and the `rwb-docs-legal` policy are present.
- Step 4: DocumentContainers and DocumentContainersConfig are published from rwb-document's `api` package; BlobStorageAdapter, the managed identity, the 10 second timeout and the blob name `{caseId}/{documentId}/v{docVersion}` are unchanged (DP-11, DP-02).
- Steps 5 and 6: WriteOnceViolationException, 409 MSG-P5-002 and ContentHashGuard are unchanged; the audit event for a refused overwrite goes through ACE Common.
- Step 7: SCR-44 and the platform administrator are unchanged; the readiness value is read from rwb-document.

### Step 1

**In the story.** Platform administrator: applies the infrastructure template for the environment, which sets the storage account (shared key access off, public network access off, TLS 1.2 minimum, private endpoint) and creates the containers rwb-intake, rwb-docs, rwb-docs-legal and rwb-quarantine.

A person starts this. The platform administrator applies the infrastructure template for one environment, and you write that template in the ACE infrastructure folder, in the format the ACE team already uses. It sets the storage account: shared key access off, public network access off, TLS 1.2 as the lowest version, and a private endpoint, which is the network route that keeps the account reachable only from inside the bank network. It then creates four containers, rwb-intake, rwb-docs, rwb-docs-legal and rwb-quarantine. A container is a named space inside a storage account that holds files, called blobs. Build step 1 of section 13 asks you to apply the template in DEV and SIT.

### Step 2

**In the story.** Template: turns on blob versioning and soft delete for rwb-docs, sets the time-based immutability policy on rwb-docs-legal (locked in PROD, unlocked in DEV, SIT and UAT), and assigns roles: the ACE service identity on rwb-intake, rwb-docs and rwb-docs-legal; SY-OCR on rwb-intake, rwb-docs and rwb-quarantine.

The same template carries these settings, so they apply when it runs and nobody switches them on later. For rwb-docs it turns on blob versioning, which keeps the earlier blob readable after an overwrite, and soft delete, which keeps a deleted blob restorable for the softDeleteDays parameter of 30. For rwb-docs-legal it sets a time-based immutability policy of the legalRetentionDays parameter, 3,650 days, which makes the storage service refuse any overwrite or delete inside that period. The policy is locked in PROD and unlocked in DEV, SIT and UAT so test files can be removed. It then assigns the Storage Blob Data Contributor role: the ACE service identity on rwb-intake, rwb-docs and rwb-docs-legal, and SY-OCR on rwb-intake, rwb-docs and rwb-quarantine, and nothing else, as AC5 checks.

### Step 3

**In the story.** System: on start, StorageReadinessIndicator checks that the four containers exist and that rwb-docs-legal has its immutability policy; the document hub reports ready only if both hold.

This runs by itself when the service starts. Build StorageReadinessIndicator and join it to the ACE health endpoint, as build step 5 says. A readiness check is the answer a module gives the platform about whether it can take work. This one asks the storage account two questions: do the four containers exist, and does rwb-docs-legal carry its immutability policy. The document hub reports ready only when both answers are yes, which is rule BR5. When the policy is missing in DEV, AC9 expects the document hub to report not ready and to name rwb-docs-legal, an upload to POST /api/recovery/v1/cases/{caseId}/documents to return 503 with MSG-GEN-006, and no document row to be written.

### Step 4

**In the story.** Document store (RWB-E1-024): writes each file through BlobStorageAdapter with the managed identity, to rwb-docs-legal for a write-once type and to rwb-docs for any other type, at the name {caseId}/{documentId}/v{docVersion}.

The document store of RWB-E1-024 writes the file, so this happens in code and not by hand. It goes through BlobStorageAdapter with a managed identity, which is an identity the platform gives the service so that no key or password is held in code or configuration. Your part in this story is the published DocumentContainers interface and DocumentContainersConfig, which builds the container clients with DefaultAzureCredential limited to managed identity and with the 10 second timeout, reading the account URL and the four container names from the properties listed in section 13. A write-once document type goes to rwb-docs-legal and any other type to rwb-docs. The blob name is {caseId}/{documentId}/v{docVersion}, and storage_ref holds the container in front of it.

### Step 5

**In the story.** Any client: an overwrite or delete of a blob in rwb-docs-legal is refused by the storage service; StorageErrorMapper turns the refusal into WriteOnceViolationException, which the store maps to 409 MSG-P5-002, and the attempt is written to the ACE audit log.

The storage service refuses the write or the delete, because the immutability policy is enforced inside the account. Any client meets that refusal, including one using the ACE service identity. Your work is StorageErrorMapper: it turns BlobImmutableDueToPolicy and conflicts on rwb-docs-legal into WriteOnceViolationException, turns a timeout into StorageUnavailableException, and writes the audit event for the refused overwrite or delete with the identity and the time, as AC1 expects. The document store turns that exception into 409 with MSG-P5-002, which tells the user that legal documents cannot be changed and that a new version should be added. The stored blob keeps its hash, so DOC-0701 in AC1 is unchanged after the attempt.

### Step 6

**In the story.** Document store: a new version is a new blob at v{n+1}; the earlier blob stays readable.

The document store does this in code. Because the write-once policy protects a name that already holds a blob, a changed document is written as a new blob at the next version number, v{n+1}, and the earlier blob stays readable. AC3 shows v1 and v2 of DOC-0701 both readable in rwb-docs-legal. Build ContentHashGuard for the case where the same name is written again: it compares the SHA-256 hash of the file with the hash of the blob already there, returns the existing blob reference when they match, and raises WriteOnceViolationException when the content differs, which is rule BR7 and scenario AC12. The doc_version field gives the number used in the blob name.

### Step 7

**In the story.** Platform administrator: sees the document hub readiness on SCR-44 Interface and job monitor.

A person reads this. The platform administrator opens SCR-44 Interface and job monitor and sees whether the document hub is ready. No screen is built here, and the monitor itself belongs to another story. What this story owes it is the readiness value from step 3, published through the ACE health endpoint, with rwb-docs-legal named when its policy is missing. The platform administrator also applies the template and holds Platform administration CRUD. The security administrator is the second person involved: build step 6 asks you to run the SIT tests, including the role listing of AC5, and hand the list of assignments over for review, which is part of the done when.

## RWB-TE-013 Agent runtime client with fallback

Module: P10 Agent runtime

**Realignment (D-RCV-60).** Epic RWB-SVC-P10 rwb-agent, wave 1: RWB-P10-TE013-CON, RWB-P10-TE013-APP and RWB-P10-TE013-OPS, release 30 November 2026 (tentative), suggested owner TechX (TechX suggested; any team may pick up this story), with DevOps for the OPS story. The central ledger side is RWB-P7-TE013-APP (RWB-SVC-P7) and the integration copy is RWB-ITG-TE013-ITG (RWB-ITG-W1).

Delta, step by step:

- Step 1 is unchanged: the calling step works out its rule result first and brings it into the call (BR1).
- Step 2: AgentStepClient, AgentStepRequest, RuleResult and AgentStepOutcome are published from the rwb-agent `api` package, `th.co.scb.ace.workbench.recovery.agent.api`, and another service depends on that contract only (DP-20; C RWB-P10-TE013-CON).
- Steps 3 to 7 are unchanged in behaviour: autonomy mode, `timeout_seconds` and the 60 second wait, SHADOW and L1, and the fallback reasons TIMED_OUT and SCHEMA. `agent_policy` and `agent_run` belong to rwb-agent (P10, Ownership Map).
- Step 8: the calling service writes its decision record in its own schema through the local decision-record library and publishes DecisionRecorded to `rwb.decision-record.v1`; rwb-decision collects it into the central ledger within 5 minutes (DP-03; RWB-P7-TE013-APP is the ledger side). The migration becomes part of rwb-agent's own Flyway sequence and `agent_run` stays in rwb_agent (DP-15).
- Step 9 is unchanged: DecisionNotRecordedException, MSG-P7-003, R-UNI-39, and `agent_run.decision_log_id` left empty when the record cannot be written.

### Step 1

**In the story.** Calling step (for example SY-CASEWF): evaluates its rule and builds the rule result (rule ID, rule version, next state).

The calling module does this before it reaches your code. A case step such as the case workflow, running under its own service identity SY-CASEWF, works out its own answer first and packs it into a rule result: the rule ID, the rule version and the next state the case should move to. The RuleResult record in section 12 is that package, with ruleId, ruleVersion, toState and the result itself as JSON. Rule BR1 fixes this order, because the rule answer has to exist before the agent is asked anything, and it stays the applied answer in both SHADOW and L1 mode. Your work in this step is publishing the record so callers can build it.

### Step 2

**In the story.** Calling step: calls AgentStepClient.runStep with the agent code, case ID, decision code, step key and rule result.

The calling module makes this call, and your job is the thing it calls. Write AgentStepClient in the package recovery.agent.api with the single method runStep, together with the records AgentStepRequest, RuleResult and AgentStepOutcome exactly as section 12 lists them. The request carries the agent code, the case ID, the decision code, the step key, the rule result and the inputs. A published interface is the one type other modules are allowed to depend on, and build step 1 asks for an ArchUnit test that proves other modules import only recovery.agent.api. The method can throw DecisionNotRecordedException, so a caller has to handle a failed decision log write.

### Step 3

**In the story.** Client: reads the autonomy mode from the agent policy in force; if it is OFF or the flag is off, it skips the agent.

The client does this by itself, inside AgentStepClientImpl. Build AutonomyModeResolver, which reads the agent policy in force for that agent and that date and takes autonomy_mode, status and valid_from from agent_policy, together with timeout_seconds. The autonomy mode says how far the agent answer may be used. When the mode is OFF, or the feature flag rwb.agent.client is off, the client makes no orchestrator call and creates no agent run row, applies the rule result, sets fallback false, and the decision log entry holds agent version null, which is scenario AC8. When no approved policy exists on the business date, the rule result is applied with fallback true and reason NO_POLICY.

### Step 4

**In the story.** Client: calls AgentOrchestrator.run with the idempotency key built from the step key and waits at most timeout_seconds.

The client makes this call on its own. Build the timed call with a CompletableFuture and the timeout from the policy, 60 seconds in the approved policy, and pass AgentOrchestrator.run an idempotency key built from the step key. Idempotent means that repeating the same call with the same key produces one run and returns the first outcome, so a step that arrives twice does not start a second agent run or write a second decision log entry, which is rule BR5 and scenario AC7. The client waits no longer than the timeout, and build step 3 asks you to test this with a stub that sleeps 61 seconds on a fake clock.

### Step 5

**In the story.** Client: in SHADOW mode, keeps the rule result as the applied result and records the agent answer only.

The client decides this with no person involved. Shadow mode means the agent runs beside the live path and its answer is recorded only, with no effect on the case. The applied result stays the rule result, the agent answer is stored on the agent run, and the outcome handed back to the calling step carries the rule result and no agent output, as AC1 requires. The decision log entry for that step holds the agent version in the form INTAKE@P1/PR1, the rule ID and version, recommendation null and fallback false in its actions. The mapping in section 12 sets recommendation to null outside L1 mode, so your mapper has to read the mode before it fills that field.

### Step 6

**In the story.** Client: in L1 mode, keeps the rule result as the applied result and returns the checked agent answer as the recommendation for the person who decides.

The client does this automatically, and a person acts on the result afterwards. In L1 mode the applied result is still the rule result, so nothing in the case moves on the agent answer. The outcome returns the checked agent answer in its recommendation field, which is the JSON the person who decides reads before making the call. The decision log entry holds that answer in recommendation together with its confidence, 0.91 in scenario AC3. The guardrails of this story say the client never applies an agent answer as the case result in SHADOW or L1, so your code keeps the applied result path and the recommendation path apart.

### Step 7

**In the story.** Client: on a timeout or a guardrail failure, keeps the rule result and marks fallback true with the reason (R-UNI-32).

The client handles this on its own. Two causes lead here: the agent does not answer inside timeout_seconds, and the answer fails a guardrail check. In both cases the client keeps the rule result as the applied result, sets fallback true, and carries the reason, TIMED_OUT for the timeout in AC2 and the check code such as SCHEMA in AC4. The step continues to the next state the rule asked for, so the case is not held up by an agent. The agent run holds status TIMED_OUT and fallback true. Rule R-UNI-32 is the source of this behavior, and the fallback rate is the measure for the story, with a target below 10 percent per month.

### Step 8

**In the story.** Client: writes one decision log entry through DecisionLogWriter with the rule ID and version, agent version, model version, recommendation and fallback, then links it to the agent run.

The client writes the entry itself, through the P7 interface and never straight into the table. Build DecisionLogMapper to fill the entry from section 12: case ID, decision code, rule ID and version from the rule result, agent version as agent, policy and prompt joined, model version from the run, the reference to the masked inputs snapshot, the recommendation, the final call from the rule result next state, and the actions holding the agent run ID, the mode, the fallback and its reason. DecisionLogWriter throws when the write fails. After the write, AgentRunRepository sets agent_run.decision_log_id. That column is added by migration V10_002__agent_run_decision_link.sql, a numbered SQL file the pipeline applies to the schema.

### Step 9

**In the story.** Calling step: acts on the applied result only after the entry is written.

The calling module waits, which is the point of the order in rule BR3: the entry is written first, the step acts second. When the write succeeds, the step moves the case on the applied result, which is always the rule result in this story. When DecisionLogWriter throws, the client raises DecisionNotRecordedException carrying MSG-P7-003, so the user reads that the action was not taken because the decision could not be recorded and can try again in a few minutes. The step takes no action, case RW-2026-000201 keeps its state in AC6, an incident is raised under R-UNI-39, and agent_run.decision_log_id is left empty.

