SCB Collections and Recovery. Henka Group, 22 November 2026.

(C) Siam Commercial Bank and Henka Pte Ltd

# Recovery Workbench

# Engineering practices

| Item | Detail |
|---|---|
| Document | Recovery Workbench engineering practices |
| Version | 6 |
| Date | 22 November 2026 |
| Supersedes | Version 5, 16 November 2026 |
| Prepared by | Henka Group |
| Applies to | The TechX recovery squads, the collection squad, the ACE team and the platform team, working in 19 Recovery services inside ACE |
| Decision | D-RCV-60: adopt Architecture v5 and realign the documents and stories |
| Status | Draft |
| Change | 6, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash |


Version 6 keeps sections 1 to 11 of version 5, with every practice, gate, test level, owner label, figure and date in them, and changes the three things the realignment needs: the code lives in one repository per service, every call starts from a published contract, and every service runs its own Flyway migrations in its own schema. The Workbench is 19 services inside ACE (ADR-013), each with one schema, one login, one REST base, one Kafka topic and one Temporal task queue (R4; ADR-014, ADR-015, ADR-016). The one service, one repository and one recovery module of version 5 are replaced by that shape, because Architecture v5 wins on source precedence (R3); the loser of the conflict is recorded (CG-B-DELIVDOC-44-1; ASM-B-DELIVDOC-44-1).

No approval of this version is recorded, so it is issued as Draft: Not specified in the source documents (CG-B-DELIVDOC-44-7; ASM-B-DELIVDOC-44-7).

# 1. The practices on one page

| Practice | Position | Status |
|---|---|---|
| Where code lives | 19 services inside ACE, one repository per service; one platform repository holds the service template, the shared libraries and the golden pipeline. The ACE front end stays one web application. | Agreed; ADR-013, RWB-PLT-TPL |
| Structure | Service boundaries by repository and schema, one schema and one login per service, checked at build time. No cross-schema join, view or foreign key. | Agreed; ADR-014 |
| Contracts | Contract first: the OpenAPI, AsyncAPI and activity-jar contract of a service is published and merged before the code that uses it, with a contract fake. | Agreed; ADR-020 |
| Migrations | A per-service Flyway sequence in the service's own schema, run by the service's own pipeline. | Agreed; ADR-021 |
| Workflow | Temporal runs the case lifecycle from Epic 3, with one parent workflow on rwb-case and a child workflow per stage on the owning service. Drools evaluates rules from versioned packages; conditions and actions are rows in a rule package. | Agreed; ADR-011, ADR-017 |
| Branching | Trunk based, one main per repository. Short-lived branches merged into main at least once a working day. | Agreed |
| Merge owner | Each squad merges into its own service repository through code owners. The platform team owns the platform repository, and the ACE team owns the release decision. | Assumed, DL04 |
| Code review | AI first-pass review, then one named human reviewer. A change in another service's contract or schema needs that service's code owner. | Proposed |
| Tests | No untested code is merged. Tests are written from the acceptance criteria before the code. Contract tests run against the published contract and its fake. | Agreed |
| Feature flags | Every unfinished or cross-service change is behind a flag. A flag that is off returns the previous code path. Flags are held in the platform library. | Agreed |
| Pipeline gates | Eleven checks before merge, on the pipeline of the service's own repository; deploy to DEV on merge, SIT on tag, UAT and production by the monthly release. | Proposed, Sprint 0 |
| Release | One production release a month, shared with the collection squad: one week of SIT, one week of UAT, business testing during the build, and every service deployed on its own image. | Agreed; dates DL34 |


Agreed: agreed by SCB IT, the ACE team, TechX and Henka. Proposed: the practice the squads use from 2 November unless the ACE team or SCB IT changes it. Assumed: the position used until the bank decides, with the decision log entry that holds the question.

# 2. Where the code lives

## 2.1 One repository per service

The Recovery Workbench is built as 19 services inside ACE. There is one repository per service, one platform repository and one front end. Each service repository holds that service's api and worker deployment, its contracts, its Flyway migrations and its configuration; the platform repository holds the service template, the shared libraries, the Helm chart and the golden pipeline (RWB-PLT-TPL, RWB-PLT-LIB).

| Code | Service | Schema | REST base | Topic | Task queue | Wave |
|---|---|---|---|---|---|---|
| P1 | rwb-source-data | rwb_source_data | /api/recovery/source-data/v1 | rwb.source-data.events.v1 | rwb-source-data | 1 |
| P2 | rwb-integration | rwb_integration | /api/recovery/integration/v1 | rwb.integration.events.v1 | rwb-integration | 1 |
| P3 | rwb-case | rwb_case | /api/recovery/case/v1 | rwb.case.events.v1 | rwb-case | 1 |
| P4 | rwb-access | rwb_access | /api/recovery/access/v1 | rwb.access.events.v1 | rwb-access | 1 |
| P5 | rwb-document | rwb_document | /api/recovery/document/v1 | rwb.document.events.v1 | rwb-document | 1 |
| P6 | rwb-comms | rwb_comms | /api/recovery/comms/v1 | rwb.comms.events.v1 | rwb-comms | 1 |
| P7 | rwb-decision | rwb_decision | /api/recovery/decision/v1 | rwb.decision.events.v1 | rwb-decision | 1 |
| P8 | rwb-payment | rwb_payment | /api/recovery/payment/v1 | rwb.payment.events.v1 | rwb-payment | 2 |
| P9 | rwb-reporting | rwb_reporting | /api/recovery/reporting/v1 | rwb.reporting.events.v1 | rwb-reporting | 1 |
| P10 | rwb-agent | rwb_agent | /api/recovery/agent/v1 | rwb.agent.events.v1 | rwb-agent | 1 |
| S1 | rwb-valuation | rwb_valuation | /api/recovery/valuation/v1 | rwb.valuation.events.v1 | rwb-valuation | 3 |
| S2 | rwb-treatment | rwb_treatment | /api/recovery/treatment/v1 | rwb.treatment.events.v1 | rwb-treatment | 2 |
| S3 | rwb-guarantee | rwb_guarantee | /api/recovery/guarantee/v1 | rwb.guarantee.events.v1 | rwb-guarantee | 3 |
| S4 | rwb-litigation | rwb_litigation | /api/recovery/litigation/v1 | rwb.litigation.events.v1 | rwb-litigation | 3 |
| S5 | rwb-asset | rwb_asset | /api/recovery/asset/v1 | rwb.asset.events.v1 | rwb-asset | 2 |
| S6 | rwb-debtsale | rwb_debtsale | /api/recovery/debtsale/v1 | rwb.debtsale.events.v1 | rwb-debtsale | 3 |
| S7 | rwb-writeoff | rwb_writeoff | /api/recovery/writeoff/v1 | rwb.writeoff.events.v1 | rwb-writeoff | 4 |
| S8 | rwb-deviation | rwb_deviation | /api/recovery/deviation/v1 | rwb.deviation.events.v1 | rwb-deviation | 2 |
| S9 | rwb-partner | rwb_partner | /api/recovery/partner/v1 | rwb.partner.events.v1 | rwb-partner | 4 |


The 19 rows are the Services sheet of the Ownership Map v1 and the service table of Template and Rules §R4. The wave is the Architecture v5 wave; the Ownership Map gives the same wave for every service.

The three modules of version 5 map onto that shape; nothing in the collection module and the common services changes.

| Module in version 5 | Where it goes | Owner |
|---|---|---|
| Common | The ACE common services, and the platform library (RWB-PLT-LIB) for the shared code and the shared tables | ACE team |
| Collection | The ACE collection service, unchanged | Collection squad |
| Recovery | The 19 Recovery services of the table above | TechX recovery squads |


The edge is two repositories of its own: gateway-bff, with the Redis session store and the composite routes, and the partner gateway in the DMZ (R4; DP-19). The ACE front end stays one web application with a recovery folder; a screen calls gateway-bff, which calls each owning service directly, in parallel, and never chains calls (DL07; ADR-019).

The naming of the 19 service repositories, their group in the bank source control and the provisioning of the empty repositories are not stated in any source read for this document: Not specified in the source documents (CG-B-DELIVDOC-44-3; ASM-B-DELIVDOC-44-3). Until they are stated, a repository takes the service name of the table above.

## 2.2 Boundary rules

- A service calls another service only through that service's published contract, through an event, through a Temporal activity or child workflow on the owner's task queue, or through a Nexus operation. It never imports another service's code and never calls its inside.

- Each service owns its schema, its login and its Flyway history. Another service reads its data only through its contract or through the events it publishes. There is no cross-schema join, view or foreign key; a service holds the other service's ID (ADR-014).

- Only rwb-source-data reads the 30 read-only v_ace_* views of schema recovery; no other service has a grant on them.

- A boundary test runs in the build of every service and fails it on any cross-schema reference or any import of another service's code.

- Front end types are generated from the OpenAPI contract of the owning service by code. They are not written by hand or by an AI tool.

- Names follow the business glossary, so one concept has one name in the model, the code and the conversation.

## 2.3 Technology

| Layer | Technology, as ACE runs it today |
|---|---|
| Back end | Spring Boot (Java) with Spring JPA, Spring Batch, Spring Security with method security and OAuth, Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz |
| Front end | React on Vite with Radix and TanStack Query |
| Database | PostgreSQL, one schema and one login per service, PgBouncer pool per login, statement timeout 5 s |
| Migrations | Flyway, one sequence per service in the service's own schema, run by the service's own pipeline |
| Contracts | OpenAPI 3.1 for REST, AsyncAPI 3.0 with the JSON Schema registry for events, a contract jar for the Temporal activity and workflow interfaces, a file manifest |
| Events | Kafka over TLS, CloudEvents 1.0 in binary mode, transactional outbox and inbox in each service, retry topics at 1, 10 and 60 minutes and a dead-letter topic |
| Workflow | Temporal 1.30 or later, namespace rwb-recovery, one task queue per service rwb-<short>, Worker Versioning, payload codec |
| Rules | Drools embedded in each service, rule packages and the registry in rwb-decision, no KIE Server, Business Central or KJAR |
| Data in | COLLINS on Databricks by ETL batch: UDP, SCBPDM, core bank batch, EFS and AAL. No real time feed today |
| Identity and logs | Entra ID, the bank IAM, PII Kafka, audit log and SOC log |
| Design patterns | Domain driven design, RESTful API, end-to-end type safety and validation |
| Hosting | ACE namespace on the shared ACE AKS clusters; one Helm chart and one golden pipeline for every service; about 38 small deployments at rest, one api and one worker per service |


## 2.4 Contract first

- Every service publishes its contracts before its code: OpenAPI 3.1 for REST with /v1 in the path, RFC 9457 problem details and an Idempotency-Key on every POST; AsyncAPI 3.0 per topic with the JSON Schema registry in BACKWARD compatibility; a contract jar for its Temporal activity and workflow interfaces; a file manifest where it exchanges files (ADR-020; Architecture v5 slide 11).

- The contract of a service is merged into that service's repository before the application story that uses it, together with a contract fake. That is the CON story of the service, it is always Day 1, and it has no build dependency (Template and Rules §R5.4, §R5.7).

- A consumer builds against the published contract and its fake. A contract dependency never blocks a build; only a build dependency inside the same service, or on a platform contract story, does (§R5.4).

- One hop only, 2 s timeout, GET retried once with jitter, a circuit breaker and a bulkhead per downstream, and no call chain deeper than one (Architecture v5 slide 11).

- Contract tests run in every build of the owner and of every consumer. A change that is not backward compatible takes a new version in the path and an ADR; a field is only removed after every consumer has stopped reading it.

- The contract of each service is recorded in the Service Contract Catalog v1 and in that service's API Specification file. Who approves a contract version, and where the published contract artefact is held for consumers, is not stated in any source read for this document: Not specified in the source documents (CG-B-DELIVDOC-44-5; ASM-B-DELIVDOC-44-5).

## 2.5 Per-service Flyway

- Each service runs its own Flyway sequence against its own schema, in its own pipeline, with its own history table (ADR-021; Architecture v5 slide 29).

- The first migration of a service is its V0001 baseline in its own schema. The pipeline applies the migrations before the api and the worker deployment of that service start; a failed migration stops the deployment and leaves the previous version running.

- No shared migration runner, no shared history table and no cross-schema DDL. If a service needs another service's column, it asks the owner for a contract change; it does not add a foreign key across schemas.

- Migrations are expand and contract: add the column or table, deploy the code that writes both, backfill, then remove the old shape in a later release, so a rolling deployment of two versions is safe. A destructive change takes a flag and a release.

- Every pull request runs the migrations on a real PostgreSQL in Testcontainers, on top of the current schema, and fails when a migration does not apply or when it breaks a contract test.

- The built migration of Epic 1 is kept (R6; RWB-E1-001). The split of the single recovery schema into the 19 rwb_* schemas is new work, carried by RWB-PLT-NF06-DB and the per-service DB stories. How the 92 tables and the 14 data products of the built schema are cut across the 19 schemas, and whether each V0001 baseline is generated from that cut, is not stated in any source read for this document: Not specified in the source documents (CG-B-DELIVDOC-44-2; ASM-B-DELIVDOC-44-2).

- The Ownership Map v1 gives rwb-valuation no table row, so its schema starts with its baseline migration only, and no table of its own is listed: Not specified in the source documents (CG-B-DELIVDOC-44-6; ASM-B-DELIVDOC-44-6).

- Schema recovery keeps the 30 read-only v_ace_* views; only rwb_source_data has SELECT on them, and no service migrates anything into that schema (ADR-010; R4).

# 3. Workflow and rules in code

- A recovery case is modeled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and case file item. The collection service uses the same terms.

- The case, its stages and its tasks are held in schema rwb_case and moved by a Temporal workflow from Epic 3. Case data stays the system of record in the schema of the service that owns it (ADR-011, ADR-014). CaseWorkflow on rwb-case is the parent, one per case; each stage runs as a child workflow on the queue of the service that owns the stage.

- The condition a sentry tests and the action it takes are rows in a versioned Drools rule package. Code holds the behavior; data holds the choices. A change to a threshold, a timer or a route is a rule package change through RWB-E1-073, not a code release.

- The owning service owns its case data and its specific actions. The case view shows the case, its stages, tasks and history, composed by gateway-bff from rwb-case GET /case-summary/{id} and the routes of the owning services; common actions such as view, assign and start stage are passed to the owning service.

- Timers and scheduled work run on Quartz and Spring Batch in Epics 1 and 2, which are preserved. JOB-05, the Quartz implementation of the TimerScheduler port, is retired: from Epic 3 a Temporal durable timer carries a case wait, a Temporal Schedule carries the scheduled work, and callers do not change (ADR-016).

- Temporal runs the case lifecycle from Epic 3 on the shared ACE AKS clusters, namespace rwb-recovery, one task queue per service (ADR-011). Drools is embedded in each service from versioned rule packages, with the registry and the four-eyes approval in rwb-decision (ADR-017); there is no KIE Server, Business Central or KJAR.

- Drools boundary. No Drools call is made in workflow code; a rule is evaluated only inside an activity. Workflow code uses no clock, no random source and no I/O. The workflow boundary test of every service fails the build when a workflow class calls Drools, reads the clock, uses random or performs I/O.

- Activity contract. Every service publishes a contract jar with its typed activity and workflow interfaces on its own task queue; a caller imports only the interface. A workflow change is versioned with Worker Versioning and getVersion, and the replay gate E2-040 replays recorded SIT histories on every build that changes a workflow (MSG-P3-038).

- Rule package review. RW-COE authors a rule package, RW-RISK approves it, and the author cannot approve their own package. The checksum of the workbook, the generated DRL and the approval are recorded on the rule_package_version row of schema rwb_decision.

- Rule scenario gate. RuleScenarioBuildGate runs every in-force rule package's scenarios on every build. One failed scenario blocks the merge. This is the rule test harness that replaces RWB-TE-005.

# 4. Branching and merging

## 4.1 Branches

- Main is the only long-lived branch, one main per repository. A repository can be released at any time.

- Each change starts on a short branch from main. The branch name starts with the story key.

- A branch is merged into main at least once a working day. Work that is not finished is merged behind a feature flag.

- The author brings main into the branch before opening a pull request.

- No fork and merge, and no long-lived feature or squad branches.

- A production fix is made on a branch from the release tag and merged back into main the same day.

- A contract branch is merged before the application branch of the same service: the CON story lands the contract and its fake, and the APP story then builds against them. A consumer's branch never waits for the owner's application code.

## 4.2 Pull requests and merge

| Rule | Detail |
|---|---|
| Size | One story, or one part of a story that can be tested on its own |
| Description | The story key, the acceptance criteria covered and the AI first-pass review summary |
| Checks | Every pipeline check in section 7 passes before a person reviews |
| Approval | One named reviewer from the owning squad. A change in another service's contract or schema also needs that service's code owner |
| Who merges | The author merges after approval, into their own service repository. A change in the platform repository is merged by the platform team |
| Code owners | A code owners file in each repository maps that repository, and its contract and migration folders, to its owners: each service to its squad, the platform repository to the platform team with the ACE team |
| Conflicts | A conflict between squads is settled by the two tech leads the same day. The ACE team decides if they do not agree |


Merge owner between the recovery and collection squads: the position above is assumed until the decision is taken (DL04).

# 5. Code review

Every line that reaches production is read by a person. An AI review runs first and a human reviewer decides.

| The reviewer checks | Fails when |
|---|---|
| Acceptance criteria | A criterion in the story has no test or no code that meets it |
| Tests | New behavior has no test, or a test checks nothing |
| Principle 1 | A threshold, limit, timer, queue, role, template or route is written in code instead of read from a versioned table |
| Personal data | Personal data appears in code, test data, fixtures or log lines |
| Access | An endpoint has no permission check, or the check is made in the front end only |
| Service and schema boundaries | Code reads another service's schema, imports another service's code, or adds a cross-schema foreign key |
| Contracts | A published contract changes in a way that is not backward compatible without a new version and an ADR, or a consumed contract is called without its published fake in the tests |
| Migrations | A migration runs outside the service's own Flyway sequence, drops or renames a column in the same release that stops writing it, or changes another service's schema |
| Names | A class, field or endpoint uses a name that is not in the business glossary |
| Logging | A decision or a change to a case is not written to the decision record |


- A review is completed the same working day it is requested.

- An error the AI tool makes that a reviewer finds is added to the repository standards file (AGENTS.md) of that repository, so the tool is told not to repeat it.

- Only the coding tool approved by the CTO and SCB IT is used on SCB code (DL32). No personal data or production data goes into a prompt.

# 6. Tests

| Level | What it covers | Written by | Runs |
|---|---|---|---|
| Unit | Every service method and every rule evaluation | Developer | Every commit |
| Rule scenario | Every in-force rule package's scenarios through RuleScenarioBuildGate: the event, the condition and the expected output | RW-COE with the analyst | Every build |
| Integration | One service with a real PostgreSQL database in its own schema, and Kafka and Temporal through Testcontainers | Developer | Every pull request |
| API contract | Requests and responses against the OpenAPI file, events against the AsyncAPI file and the schema registry, activities against the contract jar, and every consumed contract answered by its published fake | Developer | Every pull request |
| Service boundary | No call, import or table read across a service boundary, and no cross-schema reference | Platform team, once per service | Every pull request |
| Workflow replay | Every workflow change against the recorded SIT histories with WorkflowReplayer | Developer | Every build that changes a workflow |
| Browser | The main path and the exception paths of each screen | QA | Every merge, once the browser test runner is in the pipeline |
| SIT | The release against the SCB test systems | QA with SCB IT | One week before each release |
| UAT | The release against the business scripts | Business testers | During the build and in the week before each release |
| Migration | The service's own Flyway sequence applies to an empty schema and on top of the current schema, and the contract tests still pass afterwards | Developer with the ACE DB team | Every pull request |


- The test and the acceptance criteria are written before the code is generated.

- Code with no test is not merged into main, with or without a feature flag.

- A failing test blocks the merge. A test that fails at random is fixed or removed the same day by its author.

- DEV uses synthetic data only. UAT uses masked data from the PII service. No production data reaches DEV.

- A test never reads another service's schema. Where the real service is not deployed yet, the test uses that service's published fake, and in SIT it uses the real service once that service's wave has started.

# 7. Pipeline gates

| Gate | Checks | Blocks |
|---|---|---|
| 1 Build and unit tests | The service builds and every unit test and every rule scenario passes | Merge |
| 2 Lint | Code style and the naming rules | Merge |
| 3 Secret scan | No credential, key or token in the code | Merge |
| 4 PDPA lint | No personal data in code, tests or log statements | Merge |
| 5 Container scan | No known vulnerability above the bank threshold in the image | Merge |
| 6 Service boundary | No call, import or table read across a service boundary, and no cross-schema reference | Merge |
| 7 Integration, contract and migration tests | The service works with its own schema through its own Flyway migrations, and with the generated types from its published contracts and their fakes | Merge |
| 8 AI first-pass review | Bugs, security, PDPA and style, with a summary on the pull request | Merge |
| 9 Human approval | One named reviewer, and the code owner where another service's contract or schema is touched | Merge |
| 10 Temporal replay test gate | The workflow change replays against the recorded SIT histories with WorkflowReplayer; a non-deterministic change fails with MSG-P3-038 | Merge |
| 11 Rule scenario gate | RuleScenarioBuildGate runs every in-force rule package's scenarios on every build; one failed scenario blocks the merge | Merge |


Gates 10 and 11 cover the two engines. Gate 10 runs WorkflowReplayer against the recorded SIT histories for every workflow change and fails with MSG-P3-038 on a non-deterministic change (RWB-E2-040). Gate 11 runs RuleScenarioBuildGate for every in-force rule package on every build, whether or not the change touches a rule (RWB-E1-073). A rule package cannot be approved until its scenarios pass, and a failed scenario blocks the merge.

The eleven gates run on the pipeline of the service's own repository, built from the one golden pipeline of the platform repository. Gate 7 runs the service's own Flyway migrations and the contract tests of every contract it publishes or consumes; a change that is not backward compatible fails it (ADR-020, ADR-021).

| Step | When | Approved by |
|---|---|---|
| Deploy to DEV | On every merge into main | Pipeline |
| Deploy to SIT | On a release tag | Tech lead |
| Deploy to UAT | After SIT exit, in the week before the release | QA lead with SCB IT |
| Deploy to production | In the monthly change window | Release owner with the application owner |
| Rollback | Switch the feature flag off first; redeploy the previous tag of that service if a flag does not cover the fault | Release owner |
| Penetration test | Before the first production release of each service, and when the security design changes | SCB IT security |


ACE has four deployment slots planned in DEV and two in SIT, so squads can test in parallel. One slot in each is available today; the rest are being provisioned (DL35). With 19 services, each one an api and a worker deployment, how many of those slots a service consumes, and how a service of a later wave is given a slot, is not stated in any source read for this document: Not specified in the source documents (CG-B-DELIVDOC-44-4; ASM-B-DELIVDOC-44-4).

# 8. Feature flags

A feature flag chooses between two code paths. When the flag is off, the service runs the previous code path, the same result as reverting the change. When it is on, the new path runs. A flag does not switch a feature off for users while leaving broken code running.

| Rule | Detail |
|---|---|
| When a flag is required | Any change merged before it is finished; any change another squad depends on; any change in the platform library that alters behavior |
| What a flag records | Name, owner, story key, the service it belongs to, value in each environment, and the release in which it is removed |
| Where a flag is held | In the platform library, as configuration for each environment. Changing a value needs no code release |
| Testing | Both paths keep their tests while the flag exists |
| At release | A change that fails SIT or UAT has its flag switched off and the release goes ahead without it |
| Removal | The old path and the flag are removed in the release after the flag is switched on in production |


- The flags are library objects: feature_flag and feature_flag_change are tables of the platform library, created in every service's schema by the template, and the four admin paths are served by rwb-integration against the library (Ownership Map v1, Rulings; R3 default ruling).

- A flag is scoped to one service. A flag that has to be read by two services is a contract change, not a shared flag.

# 9. Release

- One production release a month, at the end of each epic, shared by the recovery and collection squads. The window is agreed with SCB IT (DL34).

- Development is continuous. Business testers work with the squads during the build (DL09), so UAT confirms work the business has already seen.

- SIT takes one week and UAT takes one week before each release.

- The release owner in the ACE team makes the go decision on the SIT and UAT exit, with the product owner and the application owner.

- A squad that is not ready does not hold the release. Its flags stay off.

- Each service is deployed on its own image and its own pipeline, so the release is a set of service versions, one tag per repository, recorded for the release. The release dates are unchanged from the plan and every one of them is tentative (U7; DL48).

# 10. Who owns each practice

| Practice | Owner | Follows it |
|---|---|---|
| Service structure, platform repository and boundary test | Platform team with the ACE team | All squads |
| Branching and merging into a service repository | TechX tech leads | TechX recovery squads |
| Merging into the platform repository and the release decision | ACE team (assumed, DL04) | All squads |
| Code review checklist | TechX QA lead with the ACE team | All reviewers |
| Pipeline gates and the golden pipeline | TechX DevOps with SCB IT | All squads |
| Feature flag list | Platform team, with the tech lead of each service | All developers |
| Test levels and test data | TechX QA lead | Developers and QA |
| Repository standards file (AGENTS.md), one per repository | Solution architect with the tech leads | All developers and the coding tool |
| Contracts, and the Service Contract Catalog entry of a service | The team that owns the service | All consumers of that service |
| Flyway migrations of a schema, and the schema and login of a service | ACE DB team with the team that owns the service | All developers |


Where a shared artefact lives, the Ownership Map v1 gives the owner:

| Artefact | Owner | Position |
|---|---|---|
| Parameters and reference data | P3 rwb-case | Contracts RWB-P3-E1042-CON and RWB-P3-E1043-CON; R3 default ruling |
| Case list API | P3 rwb-case | R3 default ruling |
| Rule package registry and rule models | P7 rwb-decision | ADR-017; R3 default ruling |
| Interaction ledger | P1 rwb-source-data | DP-18; R3 default ruling |
| Feature flags | Platform library | R3 default ruling; the admin paths are served by P2 rwb-integration |
| ACE data and the v_ace_* views | P1 rwb-source-data | ADR-010; the only service with SELECT on the views |


# 11. Assumptions and gaps

| Decision log | Needed | Owner | By | Position used until answered |
|---|---|---|---|---|
| DL04 | Who owns the merge between the recovery and collection squads | TechX tech leads with the ACE team | 29 Oct | Each squad merges into its own service repository; the platform team owns the platform repository and the ACE team owns the release decision |
| DL05 | Whether the bank or TechX creates the Workbench module | ACE team with TechX | 29 Oct | TechX builds in its own service repositories from 2 November; the ACE team applies the boundaries |
| DL07 | How the front end is split into modules | Solution architect with the TechX tech leads | 31 Oct | One ACE front end with a recovery folder, and one composite route per screen through gateway-bff |
| DL32 | The approved coding tool for TechX | CTO with SCB IT | 30 Oct | No coding tool is used on SCB code until approved |
| DL34 | The monthly production release window | SCB IT | 30 Oct | The last working week of each month |
| DL35 | The further ACE deployment slots | ACE team | 6 Nov | One DEV and one SIT slot shared by all services |
| DL37 | Code owner assignment in each repository and the browser test runner in the pipeline, both pending in the ACE team | ACE team with the TechX tech leads | 6 Nov | Tech leads review every pull request; browser tests run by QA outside the pipeline |
| DL44 | Adopt Architecture v5 | Programme architecture | 22 Nov | Adopted by D-RCV-60: 19 services inside ACE, one schema and one login per service, Kafka, Temporal, embedded Drools and no data lake |
| DL45 | Service epics plus business-epic tags | Programme delivery | 22 Nov | One epic per service, plus 7 platform and 5 integration epics; every story also carries its business epic EP01 to EP08 as a tag |
| DL46 | Soft ownership by team type | Programme delivery | 22 Nov | The owner of a story is a suggestion only; any team may pick up the story |
| DL47 | Epic 1 preservation rule | Programme delivery | 22 Nov | The six preserved Epic 1 stories keep their base ID and their content; the microservice change goes into delta stories |
| DL48 | Dates unchanged and tentative | Programme delivery | 22 Nov | Every date is copied unchanged from the plan and every release date is tentative |
| DL49 | Gap and assumption registers | Programme governance | 22 Nov | Gaps and assumptions are held in the Gap Register and the Assumptions Register in folder 23 |


The owner column of the first seven rows was a person in version 5; this version names the role, because no name of a person is written in a run document (AGENTS.md rule 4; ASM-B-DELIVDOC-44-1).

Open points of this document, each carried as a gap row and an assumption row:

- The conflict between the one service, one repository and one recovery module of version 5 and the 19 services of Architecture v5 (CG-B-DELIVDOC-44-1; ASM-B-DELIVDOC-44-1).

- The cut of the built recovery schema, 92 tables and 14 data products, across the 19 schemas, and the V0001 baseline of each service (CG-B-DELIVDOC-44-2; ASM-B-DELIVDOC-44-2).

- The names, the source-control group and the provisioning of the 19 service repositories (CG-B-DELIVDOC-44-3; ASM-B-DELIVDOC-44-3).

- The number of ACE deployment slots a service consumes, and how a service of a later wave gets one (CG-B-DELIVDOC-44-4; ASM-B-DELIVDOC-44-4).

- The approval of a contract version and the place where the published contract artefact is held (CG-B-DELIVDOC-44-5; ASM-B-DELIVDOC-44-5).

- The table of rwb-valuation, which the Ownership Map v1 leaves empty (CG-B-DELIVDOC-44-6; ASM-B-DELIVDOC-44-6).

- The approval and the status of version 6 of this document (CG-B-DELIVDOC-44-7; ASM-B-DELIVDOC-44-7).

- The change log of version 5, which the source does not carry (CG-B-DELIVDOC-44-8; ASM-B-DELIVDOC-44-8).

# 12. Change log

| Version | Date | Change | Tool |
|---|---|---|---|
| 5 | 16 November 2026 | Source version. It carries no change-log row of its own; the metadata table is its only record. | Not specified in the source documents (CG-B-DELIVDOC-44-8; ASM-B-DELIVDOC-44-8) |
| 6 | 22 November 2026 | D-RCV-60 microservice realignment: one repository per service, contract first, per-service Flyway, and every section, ID, number and date of version 5 kept. | T3 Code / OpenCode / DeepSeek v4.1 Flash |

