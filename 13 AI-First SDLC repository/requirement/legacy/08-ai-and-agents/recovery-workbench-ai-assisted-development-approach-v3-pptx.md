<!-- source: 08 AI and agents/Recovery Workbench AI Assisted Development Approach v3.pptx -->
<!-- converted: 2026-11-04 from PPTX -->

> **Source:** `08 AI and agents/Recovery Workbench AI Assisted Development Approach v3.pptx`  
> **Converted from:** PPTX

## Slide 1

SCB

COLLECTIONS AND RECOVERY TRANSFORMATION Recovery Workbench: AI assisted development approach

Henka Group, 28 October 2026 (C) Siam Commercial Bank and Henka Pte Ltd

## Slide 2

How AI is used in the build

2

AI assisted delivery AI drafts stories, acceptance criteria, edge cases, test cases, UAT scripts, Thai message drafts, release notes and status packs. Analysts, QA and the product owner correct, decide and sign each one.

AI assisted engineering AI proposes the plan for a story, writes the tests and the code, and reviews pull requests first. Developers conduct the agent and read every line. Tech leads approve plans. Reviewers approve merges.

Seven working rules 1  The person who merges a change owns it, whoever or whatever wrote it. 2  The agent works from three files: the standards file, the story file and the plan file. 3  The tests and the acceptance criteria exist before the code is generated. 4  Every line that reaches production is read by a person. 5  An AI error found by a reviewer is written into the standards file. 6  No personal data or production data in a prompt, a test or a log. 7  The unit of work is one story. Work is merged at least once a working day.

## Slide 3

From story to production

3

| Step | What happens | Who | Gate |
|---|---|---|---|
| 1 Story file | AI drafts the story file from the requirement, the routing rules and the data model. The analyst corrects and owns it | Analyst | Definition of ready |
| 2 Plan | The agent writes the plan file from the story file and the standards file. The tech lead approves it before any code | Developer with the agent; tech lead | Plan approved |
| 3 Tests | The agent writes failing tests from the acceptance criteria. The developer checks each test asserts its criterion | Developer with the agent | A test per criterion |
| 4 Build | The agent writes the code in DEV with synthetic data, in small commits | Developer with the agent | Tests pass |
| 5 AI review | The review agent checks the pull request and writes a summary on it | Review agent | Summary written |
| 6 Review and merge | The reviewer works through the checklist and approves. Unfinished work merges behind a feature flag | Reviewer; author | Nine pipeline checks |
| 7 Test | QA runs SIT. Business testers test during the build and in the UAT week, from AI-drafted scripts | QA; business testers | SIT and UAT exit |
| 8 Learn | AI errors found in steps 5 to 7 go into the standards file. The weekly measures are published | Tech lead | Standards file updated |

## Slide 4

The standards file: what the agent reads before every task

4

AGENTS.md in the root of the ACE repository, with a section for the recovery module. The solution architect owns it with the tech leads, and it changes by pull request like code.

| The agent must |
|---|
| Put recovery code in the recovery module folder only |
| Read every threshold, limit, timer, queue, role, template and route from its versioned table |
| Put a permission check on every endpoint, naming the capability area and the operation |
| Write a decision record entry for every case change and every decision |
| Use the business glossary names for classes, fields, tables and endpoints |
| Return each validation message from the message table by rule ID |
| Change the database by migration script only, one per story |
| Use Spring Batch and Quartz for scheduled work |
| Use the synthetic data generator for test data |
| Write the test before the code |

| The agent must never |
|---|
| Commit a credential, key or token |
| Call or read the inside of another module |
| Call a system of record directly; data arrives through COLLINS |
| Add a workflow engine, a rules engine or any new dependency |
| Disable, skip or weaken a test |
| Change a migration script that is already merged |
| Put personal data in code, test fixtures, prompts or log lines |

## Slide 5

The story file: one per story, in the SCB X template sections

5

| Section | Holds | SCB X section |
|---|---|---|
| Story | Story key, epic, module, and the statement: As a [role], I want [action], so that [result] | Functional |
| Acceptance criteria | Each criterion as Given, When, Then, with an ID | Functional |
| Business rules | The rule IDs the story implements, with the version | Business rules |
| State transitions | From state, event and to state for every transition the story adds | Business rules |
| Authority | Roles, permission letters, scope, and the approval level where a decision is approved | Authority |
| Contract | Objects and fields read and written; endpoints with request and response; events published and consumed | Contract |
| Validation and messages | Each validation with its rule ID and message ID | Functional |
| Screen and states | The screen, its fields and its states, where the story has a screen | Functional |
| Guardrails | What the code must not do, the personal data fields touched, and the limits that apply | Guardrails |
| Test cases | One or more test cases per acceptance criterion | Functional |
| Out of scope | What a reader might expect that this story does not do | Functional |

## Slide 6

The plan file and the review step

6

The plan file The agent writes plan.md for each story before any code: files to add or change, tests, migration scripts, rule tables read, and questions the story file does not answer. The tech lead approves it on the pull request. A plan that touches two modules, or needs an answer, goes back to the analyst.

The trail behind every line Every pull request carries the story key, the plan file, the coding tool used, the reviewer and the test results. A defect traced to AI-written code is tagged, and the standards file is updated before the fix merges.

| Review | Checks |
|---|---|
| AI first pass | Bugs, security, personal data, module boundaries, the standards file rules, and a test for each acceptance criterion. Writes a summary on the pull request |
| Human review | Acceptance criteria met; tests present; rules read as data; no personal data; permission check on every endpoint; module boundaries; glossary names; decision record written |

## Slide 7

Quality gates

7

| Gate | Passes when | Owner |
|---|---|---|
| Ready | Every section of the story file is complete; each acceptance criterion can be tested; every rule ID, field and message ID exists | Analyst with the tech lead |
| Plan approved | The plan names every file, test and migration, and touches one module | Tech lead |
| Merge | The nine pipeline checks pass and a named reviewer approves | Reviewer |
| SIT exit | Every test case for the release passes in SIT | QA lead |
| UAT exit | The business testers sign the UAT scripts for the release | Business lead |
| Release | SIT and UAT exits are met, and unfinished work is behind a flag that is off | Release owner with the application owner |

## Slide 8

AI assisted delivery

8

| Output | AI drafts from | Owned by |
|---|---|---|
| User stories and story files | Requirements, process flows, routing rules, data model | Analysts |
| Acceptance criteria and edge cases | Story, routing rules, deviation catalog | Analysts |
| Test cases | The 448 routing rules and the acceptance criteria | QA |
| UAT scripts | Acceptance criteria and user journeys | QA with the business testers |
| Thai message drafts | The English message table | Legal and Compliance approve |
| Release notes | Merged pull requests and their story keys | Product owner |
| Weekly status pack | Jira, the decision log and the risk list | Product owner |

## Slide 9

Rules for AI tools, and the weekly measures

9

Rules for AI tools 1  Only the coding tool approved for SCB code is used on the repository. 2  Agents work in DEV with synthetic data. UAT uses masked data. No production data goes into a prompt. 3  Prompts, skills and the standards file are held in the repository and reviewed like code. 4  Throwaway spikes are allowed in DEV only and are never merged. 5  A coding agent acts under the developer's identity and holds no permission the developer does not hold.

Published weekly from Jira and the pipeline. The first four weeks set the baseline; targets are set from it.

| Measure | Definition |
|---|---|
| Cycle time | Working days from ready to merged, per story |
| Review time | Hours from pull request opened to approved |
| Rework rate | Share of pull requests changed after human review |
| Defect escape rate | Defects found in SIT or UAT per story merged |
| Test coverage | Share of changed lines covered by a test |
| AI errors recorded | New entries added to the standards file |

## Slide 10

Who does what

10

| Role | Responsible for |
|---|---|
| Analyst | Story files, acceptance criteria, the ready gate |
| Tech lead | Plan approval, the standards file with the solution architect, the known error list |
| Developer | Conducting the agent, reading every line, the tests |
| Reviewer | The review checklist and the merge approval |
| QA | Test cases, SIT, the UAT scripts |
| Business testers | Testing during the build and in the UAT week |
| Solution architect | The standards file and the documents the agent reads |
| Product owner | Story order, release notes, the weekly measures |
