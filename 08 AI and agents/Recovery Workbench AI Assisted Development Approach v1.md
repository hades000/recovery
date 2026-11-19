# Recovery Workbench: AI assisted development approach

SCB Collections and Recovery. Henka Group, 28 October 2026. Version 1.

## 1. How AI is used

The Recovery Workbench is built with AI in two parts. In both, a person owns the result.

| Part | What AI does | What a person owns |
|---|---|---|
| AI assisted delivery | Drafts stories, acceptance criteria, edge cases, test cases, UAT scripts, Thai message drafts, release notes and status packs | The analysts, QA and the product owner correct, decide and sign each one |
| AI assisted engineering | Proposes the plan for a story, writes the tests and the code, reviews pull requests first | Developers conduct the agent and read every line. Tech leads approve plans. Reviewers approve merges |

Seven working rules apply to both parts.

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files: the standards file, the story file and the plan file. Anything the agent needs is in one of the three.
3. The tests and the acceptance criteria exist before the code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found by a reviewer is written into the standards file, so the agent is told not to repeat it.
6. No personal data or production data goes into a prompt, a test or a log.
7. The unit of work is one story. Work is merged at least once a working day.

## 2. From story to production

| Step | What happens | Who | Gate |
|---|---|---|---|
| 1 Story file | AI drafts the story file from the requirement, the routing rules and the data model. The analyst corrects it and owns it | Analyst | Definition of ready |
| 2 Plan | The agent reads the story file and the standards file and writes the plan file. The tech lead approves it before any code is written | Developer with the agent; tech lead | Plan approved |
| 3 Tests | The agent writes failing tests from the acceptance criteria. The developer checks that each test asserts its criterion | Developer with the agent | Every criterion has a test |
| 4 Build | The agent writes the code in DEV with synthetic data, in small commits | Developer with the agent | Tests pass |
| 5 AI review | The review agent checks the pull request and writes a summary on it | Review agent | Summary on the pull request |
| 6 Human review and merge | The reviewer works through the review checklist and approves. The author merges behind a feature flag if the work is not finished | Reviewer; author | Nine pipeline checks pass |
| 7 Test | QA runs SIT. Business testers test during the build and in the UAT week. AI drafts the UAT scripts from the acceptance criteria | QA; business testers | SIT exit; UAT exit |
| 8 Learn | AI errors found in steps 5 to 7 go into the standards file. The weekly measures in section 10 are published | Tech lead | Standards file updated |

## 3. The standards file

The standards file is `AGENTS.md` in the root of the ACE repository, with a section for the recovery module. The agent reads it before every task. The solution architect owns it with the tech leads, and it changes by pull request like code.

### 3.1 Structure and stack

- The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
- Back end: Spring Boot (Java), Spring JPA, Spring Batch, Spring Security with method security, Quartz. Front end: React on Vite with Radix and TanStack Query. Database: PostgreSQL.
- Domain driven design, RESTful API, front end types generated from the back end.
- Cases are modeled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener, case file item.

### 3.2 The agent must

1. Put recovery code in the recovery module folder only. Change the common or collection module only where the story file names it.
2. Read every threshold, limit, timer, queue, role, template and route from its versioned reference table. Never write one as a literal in code.
3. Put a Spring Security method check on every endpoint, naming the capability area and the operation.
4. Write a decision record entry for every change to a case and every decision, with the rule ID and version used.
5. Use the names in the business glossary for classes, fields, tables and endpoints.
6. Return each validation message from the message table by its rule ID.
7. Make database changes by migration script only, one script per story.
8. Use Spring Batch and Quartz for scheduled work.
9. Use the synthetic data generator for test data.
10. Write the test before the code. A change with no test is not complete.

### 3.3 The agent must never

1. Commit a credential, key or token.
2. Call or read the inside of another module.
3. Call a system of record directly. Data arrives through COLLINS and leaves through the integration adapters.
4. Add a workflow engine, a rules engine or any new dependency.
5. Disable, skip or weaken a test.
6. Change a migration script that is already merged.
7. Put personal data in code, test fixtures, prompts or log lines.

### 3.4 What the agent reads besides the story

| File | Used for |
|---|---|
| Business glossary | Names of classes, fields and endpoints |
| Logical data model and data dictionary | Entities, fields, types and lists of values |
| Business rules and routing logic | Rule IDs, events, conditions and actions |
| Case and workflow model | Stages, milestones, tasks and sentries |
| Users, roles and permissions | Roles, permission letters and scopes |
| Error and message standard | Message IDs and wording |
| API specification | Paths, requests, responses and error codes |

### 3.5 Known AI errors

The known error list in the ACE standards file applies to the recovery module. Each new entry carries the date, the error and the rule added to section 3.2 or 3.3.

## 4. The story file

One story file per story, held in the repository next to the code it produces. The sections follow the SCB X requirement template for AI code generation: guardrails, business rules, authority, contract and functional.

| Section | Holds | SCB X section |
|---|---|---|
| Story | Story key, epic, module, the statement in the form "As a [role], I want [action], so that [result]" | Functional |
| Acceptance criteria | Each criterion as Given, When, Then, with an ID | Functional |
| Business rules | The rule IDs the story implements, with the version | Business rules |
| State transitions | From state, event, to state, for every transition the story adds | Business rules |
| Authority | Roles, permission letters, scope, and the approval level where a decision is approved | Authority |
| Contract | Objects and fields read and written, endpoints with request and response, events published and consumed | Contract |
| Validation and messages | Each validation with its rule ID and message ID | Functional |
| Screen and states | The screen, its fields and its states, where the story has a screen | Functional |
| Guardrails | What the code must not do for this story, the personal data fields touched, and the limits that apply | Guardrails |
| Test cases | One or more test cases per acceptance criterion | Functional |
| Out of scope | What a reader might expect that this story does not do | Functional |

### 4.1 Example

```
Story key   RWB-E1-022
Epic        1    Module  Access and authority
Story       As a bank user, I want my Workbench roles resolved when I sign in,
            so that I see only the cases and fields my roles allow.

Acceptance criteria
AC1  Given a user in the Entra ID group for RW-CASEOWN
     When they sign in with multi-factor authentication
     Then the session carries RW-CASEOWN, scope "own" and the case owner masking rule,
     and the first screen names the role and the scope.
AC2  Given a user in no Workbench group
     When they sign in
     Then the session is refused with message MSG-ACA-002
     and an access.refused entry is written to the access log.
AC3  Given a user in the groups for RW-SECADM and RW-CASEOWN
     When they sign in
     Then the session is refused, an incident is raised to the security administrator,
     and the refusal is logged.

Business rules   BR-ACA-003, BR-ACA-004, BR-ACA-005, SOD-ACA-001
Authority        Any signed-in user. No permission letter is checked before roles resolve.
Contract         Reads: roles table, Entra ID group mapping, scope rules, masking rules
                 (versions in force). Writes: session, access log entry.
Guardrails       No local credential. No fallback sign-in when Entra ID is unavailable.
                 The user's name and staff ID are the only personal data fields written to the log.
Test cases       TC-ACA-001 to TC-ACA-006
Out of scope     Granting a role. Grants are made in the bank IAM.
```

## 5. The plan file

The agent writes `plan.md` for each story before any code. It lists the files to add or change, the tests to write, the migration scripts, the rule tables read, and any question the story file does not answer. The tech lead approves the plan on the pull request. A plan that touches more than one module, or that the agent cannot complete without an answer, goes back to the analyst before any code is written.

## 6. The review step

| Review | Checks | Output |
|---|---|---|
| AI first pass | Bugs, security, personal data, module boundaries, the rules in section 3, and whether each acceptance criterion has a test | A summary on the pull request |
| Human review | The review checklist in the engineering practices: acceptance criteria, tests, rules as data, personal data, access, module boundaries, names, decision record | Approval or changes requested |

Every pull request carries the story key, the plan file, the coding tool used, the reviewer and the test results. Any line in production can be traced to a story, a plan and a named reviewer. A defect traced to AI-written code is tagged as such, and the standards file is updated before the fix is merged.

## 7. Quality gates

| Gate | Passes when | Owner |
|---|---|---|
| Ready | Every section of the story file is complete; each acceptance criterion can be tested; every rule ID, field and message ID exists in its source document | Analyst with the tech lead |
| Plan approved | The plan names every file, test and migration, and touches one module | Tech lead |
| Merge | The nine pipeline checks pass and a named reviewer approves | Reviewer |
| SIT exit | Every test case for the release passes in SIT | QA lead |
| UAT exit | The business testers sign the UAT scripts for the release | Business lead |
| Release | The SIT and UAT exits are met and unfinished work is behind a flag that is off | Release owner with the application owner |

## 8. AI assisted delivery

| Output | AI drafts from | Owned by |
|---|---|---|
| User stories and story files | Requirements, process flows, routing rules, data model | Analysts |
| Acceptance criteria and edge cases | Story, routing rules, deviation catalog | Analysts |
| Test cases | The 448 routing rules and the acceptance criteria | QA |
| UAT scripts | Acceptance criteria and user journeys | QA with the business testers |
| Thai message drafts | The English message table | Legal and Compliance approve |
| Release notes | Merged pull requests and their story keys | Product owner |
| Weekly status pack | Jira, the decision log and the risk list | Product owner |

## 9. Rules for AI tools

1. Only the coding tool approved for SCB code is used on the repository.
2. Agents work in DEV with synthetic data. UAT uses masked data. No production data is used in a prompt.
3. Prompts, skills and the standards file are held in the repository and reviewed like code.
4. Throwaway spikes are allowed in DEV only and are never merged.
5. A coding agent acts under the developer's own identity and holds no permission the developer does not hold.

## 10. Measures

Published every week from Jira and the pipeline. The first four weeks set the baseline, and targets are set from it.

| Measure | Definition |
|---|---|
| Cycle time | Working days from ready to merged, per story |
| Review time | Hours from pull request opened to approved |
| Rework rate | Share of pull requests changed after human review |
| Defect escape rate | Defects found in SIT or UAT per story merged |
| Test coverage | Share of changed lines covered by a test |
| AI errors recorded | New entries added to the standards file |

## 11. Who does what

| Role | Responsible for |
|---|---|
| Analyst | Story files, acceptance criteria, the ready gate |
| Tech lead | Plan approval, the standards file with the solution architect, the known error list |
| Developer | Conducting the agent, reading every line, the tests |
| Reviewer | The review checklist and the merge approval |
| QA | Test cases, SIT, the UAT scripts |
| Business testers | Testing during the build and in the UAT week |
| Solution architect | The standards file and the context documents the agent reads |
| Product owner | Story order, release notes, the weekly measures |
