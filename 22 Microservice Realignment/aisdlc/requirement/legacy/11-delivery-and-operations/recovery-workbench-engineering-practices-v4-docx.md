<!-- source: 11 Delivery and operations/Recovery Workbench Engineering Practices v4.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Engineering Practices v4.docx`  
> **Converted from:** DOCX

Recovery Workbench

Engineering practices

SCB Collections and Recovery. Henka Group, 28 October 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench engineering practices |
| Version | 3 |
| Date | 28 October 2026 |
| Prepared by | Henka Group |
| Applies to | The two TechX recovery squads, the collection squad and the ACE team, working in one ACE service |

# 1. The practices on one page

| Practice | Position | Status |
|---|---|---|
| Where code lives | One ACE service, one repository, one front end. Recovery code is in the recovery module. | Agreed |
| Structure | Modular monolith: common, collection and recovery modules by folder, with boundaries checked at build time. | Agreed |
| Workflow | Programmatic, in CMMN 1.1 terms. Conditions and actions are versioned data rows. No Temporal. | Agreed |
| Branching | Trunk based. Short-lived branches merged into main at least once a working day. | Agreed |
| Merge owner | Each squad merges into its own module through code owners. The ACE team owns the common module and the release decision. | Assumed, DL04 |
| Code review | AI first-pass review, then one named human reviewer. A change in another module's folder needs that module's code owner. | Proposed |
| Tests | No untested code is merged. Tests are written from the acceptance criteria before the code. | Agreed |
| Feature flags | Every unfinished or cross-squad change is behind a flag. A flag that is off returns the previous code path. | Agreed |
| Pipeline gates | Nine checks before merge, deploy to DEV on merge, SIT on tag, UAT and production by the monthly release. | Proposed, Sprint 0 |
| Release | One production release a month, shared with the collection squad: one week of SIT, one week of UAT, business testing during the build. | Agreed; dates DL34 |

Agreed: agreed by SCB IT, the ACE team, TechX and Henka. Proposed: the practice the squads use from 2 November unless the ACE team or SCB IT changes it. Assumed: the position used until the bank decides, with the decision log entry that holds the question.

# 2. Where the code lives

## 2.1 One service, three modules

The Recovery Workbench is built inside the ACE service. There is one service, one repository and one front end. The service is split into modules by folder.

| Module | Built by | Holds |
|---|---|---|
| Common | ACE team | The case view shared by both modules, sign-in and access checks, audit and PII logging, the shared entities (customer, account, product, collateral, asset) and shared tasks such as the TDR calculator |
| Collection | Collection squad | Phone, field, FCR and TDR work, as split under DL14 |
| Recovery | The two TechX recovery squads | Recovery case stages, tasks and screens; litigation, debt sale, NPA and write-off; the document hub; the decision record; the recovery data products |

A recovery component that the collection module also needs moves to the common module by agreement with the ACE team. Until the ACE team has moved ACE to the modular monolith, TechX builds in its own package (DL05).

## 2.2 Boundary rules

- A module calls another module only through that module's published interface or through an application event. It never calls the inside of another module.

- Each module owns its tables. Another module reads them only through the owning module's interface.

- A module boundary test runs in the build and fails it on any violation.

- Front end types are generated from the back end by code. They are not written by hand or by an AI tool.

- Names follow the business glossary, so one concept has one name in the model, the code and the conversation.

## 2.3 Technology

| Layer | Technology, as ACE runs it today |
|---|---|
| Back end | Spring Boot (Java) with Spring JPA, Spring Batch, Spring Security with method security and OAuth, Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz |
| Front end | React on Vite with Radix and TanStack Query |
| Database | PostgreSQL |
| Data in | COLLINS on Databricks by ETL batch: UDP, SCBPDM, core bank batch, EFS and AAL. No real time feed today |
| Identity and logs | Entra ID, the bank IAM, PII Kafka, audit log and SOC log |
| Design patterns | Domain driven design, RESTful API, end-to-end type safety and validation |
| Hosting | ACE namespace on the shared ACE AKS clusters |

# 3. Workflow and rules in code

- A recovery case is modeled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and case file item. The collection module uses the same terms.

- The case, its stages and its tasks are held in the database and moved by code. No workflow engine is used.

- The condition a sentry tests and the action it takes are rows in a versioned table. Code holds the behavior; data holds the choices. A change to a threshold, a timer or a route is a data load, not a code release.

- The recovery module owns its case data and its specific actions. The common case view shows the case, its stages, tasks and history, and passes common actions such as view, assign and start stage to the recovery module.

- Timers and scheduled work run on Quartz and Spring Batch. A long wait, such as a court date, is a stored due date that the scheduler checks.

- Temporal is not used. Adding it later for a self-contained automation task is a separate architecture decision with its own decision record.

# 4. Branching and merging

## 4.1 Branches

- Main is the only long-lived branch. It can be released at any time.

- Each change starts on a short branch from main. The branch name starts with the Jira story key.

- A branch is merged into main at least once a working day. Work that is not finished is merged behind a feature flag.

- The author brings main into the branch before opening a pull request.

- No fork and merge, and no long-lived feature or squad branches.

- A production fix is made on a branch from the release tag and merged back into main the same day.

## 4.2 Pull requests and merge

| Rule | Detail |
|---|---|
| Size | One story, or one part of a story that can be tested on its own |
| Description | The story key, the acceptance criteria covered and the AI first-pass review summary |
| Checks | Every pipeline check in section 7 passes before a person reviews |
| Approval | One named reviewer from the owning squad. A change in another module's folder also needs that module's code owner |
| Who merges | The author merges after approval, into their own module. A change in the common module is merged by the ACE team |
| Code owners | A code owners file maps each module folder to its owners: recovery to the TechX tech leads, collection to the collection squad, common to the ACE team |
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
| Module boundaries | Code reads another module's tables or calls inside another module |
| Names | A class, field or endpoint uses a name that is not in the business glossary |
| Logging | A decision or a change to a case is not written to the decision record |

- A review is completed the same working day it is requested.

- An error the AI tool makes that a reviewer finds is added to the repository standards file (AGENTS.md), so the tool is told not to repeat it.

- Only the coding tool approved by the CTO and SCB IT is used on SCB code (DL32). No personal data or production data goes into a prompt.

# 6. Tests

| Level | What it covers | Written by | Runs |
|---|---|---|---|
| Unit | Every service method and every rule evaluation | Developer | Every commit |
| Rule table | Each rule row against its test case ID: the event, the condition and the expected action | Developer with the analyst | Every commit |
| Integration | A module with a real PostgreSQL database | Developer | Every pull request |
| API contract | Requests and responses against the generated types | Developer | Every pull request |
| Module boundary | No call or table read across a module boundary | ACE team, once | Every pull request |
| Browser | The main path and the exception paths of each screen | QA | Every merge, once the browser test runner is in the pipeline |
| SIT | The release against the SCB test systems | QA with SCB IT | One week before each release |
| UAT | The release against the business scripts | Business testers | During the build and in the week before each release |

- The test and the acceptance criteria are written before the code is generated.

- Code with no test is not merged into main, with or without a feature flag.

- A failing test blocks the merge. A test that fails at random is fixed or removed the same day by its author.

- DEV uses synthetic data only. UAT uses masked data from the PII service. No production data reaches DEV.

# 7. Pipeline gates

| Gate | Checks | Blocks |
|---|---|---|
| 1 Build and unit tests | The service builds and every unit and rule table test passes | Merge |
| 2 Lint | Code style and the naming rules | Merge |
| 3 Secret scan | No credential, key or token in the code | Merge |
| 4 PDPA lint | No personal data in code, tests or log statements | Merge |
| 5 Container scan | No known vulnerability above the bank threshold in the image | Merge |
| 6 Module boundary | No call or table read across a module boundary | Merge |
| 7 Integration and contract tests | Modules work with the database and the generated types | Merge |
| 8 AI first-pass review | Bugs, security, PDPA and style, with a summary on the pull request | Merge |
| 9 Human approval | One named reviewer, and the code owner where another module is touched | Merge |

| Step | When | Approved by |
|---|---|---|
| Deploy to DEV | On every merge into main | Pipeline |
| Deploy to SIT | On a release tag | Tech lead |
| Deploy to UAT | After SIT exit, in the week before the release | QA lead with SCB IT |
| Deploy to production | In the monthly change window | Release owner with the application owner |
| Rollback | Switch the feature flag off first; redeploy the previous tag if a flag does not cover the fault | Release owner |
| Penetration test | Before the first production release of the recovery module, and when the security design changes | SCB IT security |

ACE has four deployment slots planned in DEV and two in SIT, so squads can test in parallel. One slot in each is available today; the rest are being provisioned (DL35).

# 8. Feature flags

A feature flag chooses between two code paths. When the flag is off, the service runs the previous code path, the same result as reverting the change. When it is on, the new path runs. A flag does not switch a feature off for users while leaving broken code running.

| Rule | Detail |
|---|---|
| When a flag is required | Any change merged before it is finished; any change another squad depends on; any change in the common module that alters behavior |
| What a flag records | Name, owner, story key, value in each environment, and the release in which it is removed |
| Where a flag is held | As configuration for each environment. Changing a value needs no code release |
| Testing | Both paths keep their tests while the flag exists |
| At release | A change that fails SIT or UAT has its flag switched off and the release goes ahead without it |
| Removal | The old path and the flag are removed in the release after the flag is switched on in production |

# 9. Release

- One production release a month, at the end of each epic, shared by the recovery and collection squads. The window is agreed with SCB IT (DL34).

- Development is continuous. Business testers work with the squads during the build (DL09), so UAT confirms work the business has already seen.

- SIT takes one week and UAT takes one week before each release.

- The release owner in the ACE team makes the go decision on the SIT and UAT exit, with the product owner and the application owner.

- A squad that is not ready does not hold the release. Its flags stay off.

# 10. Who owns each practice

| Practice | Owner | Follows it |
|---|---|---|
| Module structure and boundary test | ACE team | All squads |
| Branching and merging into the recovery module | TechX tech leads | TechX recovery squads |
| Merging into the common module and the release decision | ACE team (assumed, DL04) | All squads |
| Code review checklist | TechX QA lead with the ACE team | All reviewers |
| Pipeline gates | TechX DevOps with SCB IT | All squads |
| Feature flag list | Tech lead of each squad | All developers |
| Test levels and test data | TechX QA lead | Developers and QA |
| Repository standards file (AGENTS.md) | Solution architect with the tech leads | All developers and the coding tool |

# 11. Assumptions and gaps

| Decision log | Needed | Owner | By | Position used until answered |
|---|---|---|---|---|
| DL04 | Who owns the merge between the recovery and collection squads | K. Book | 29 Oct | Each squad merges into its own module; the ACE team owns the common module and the release decision |
| DL05 | Whether the bank or TechX creates the Workbench module | K. Pipat | 29 Oct | TechX builds in its own package from 2 November; the ACE team applies the boundaries |
| DL07 | How the front end is split into modules | K. Pipat | 31 Oct | One ACE front end with a recovery module folder |
| DL32 | The approved coding tool for TechX | CTO with SCB IT | 30 Oct | No coding tool is used on SCB code until approved |
| DL34 | The monthly production release window | SCB IT | 30 Oct | The last working week of each month |
| DL35 | The further ACE deployment slots | K. Tee | 6 Nov | One DEV and one SIT slot shared by all squads |
| DL37 | Code owner assignment in the ACE repository and the browser test runner in the pipeline, both pending in the ACE team | K. Book | 6 Nov | Tech leads review every pull request; browser tests run by QA outside the pipeline |
