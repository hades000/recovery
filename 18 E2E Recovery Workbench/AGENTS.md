# Recovery Workbench — AI engineering standards (v2)

This is the standards file the coding agent reads before every task, as defined in
`Recovery Workbench AI Assisted Development Approach v1` (section 3). It applies to the recovery
module of the ACE service and to anyone using an AI tool on this repository.

**Owner:** Solution architect with the TechX tech leads.
**Change control:** pull request, reviewed like code.
**Baseline:** document set v14, 16 November 2026. The implementation evidence from 10 November 2026
(`RWB-E1-042`, `RWB-TE-001`) is preserved; both are re-specified against this baseline.
**Source:** `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md`
and `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v5-docx.md`.

## 1. The seven working rules

1. The person who merges a change owns it, whoever or whatever wrote it.
2. The agent works from files: the standards file, the story file and the plan file. Anything the
   agent needs is in one of the three.
3. The tests and the acceptance criteria exist before the code is generated.
4. Every line that reaches production is read by a person.
5. An AI error found by a reviewer is written into this file, so the agent is told not to repeat it.
6. No personal data or production data goes into a prompt, a test or a log.
7. The unit of work is one story. Work is merged at least once a working day.

## 2. Structure and stack

- The Workbench is the recovery module of the ACE service: one service, one repository, one front end.
- Back end: Spring Boot (Java 21), Spring JPA, Spring Batch, Spring Security with method security,
  Spring Session, Spring Cloud Azure, Spring Data REST, Spring HATEOAS and Quartz.
- Front end: React on Vite with Radix and TanStack Query. Front-end types are generated from the
  back end.
- Database: PostgreSQL, schema `recovery` in the ACE database, referenced only as
  `${recoverySchema}` and fixed to `recovery` in every environment (D-RCV-28). Schema changes use
  versioned migrations, one migration per story, forward-only. Files are named
  `V<seq>__<story>_<name>.sql`, where `<seq>` is a four-digit sequence taken in merge order and line 1
  is `-- Story: <story key>`.
- Domain driven design, RESTful API, end-to-end type safety and validation.
- Cases are modelled in CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener and
  case file item. From Epic 3 the case lifecycle runs on Temporal; case data stays in the recovery
  schema (D-RCV-36, ADR-011).
- Rules are versioned data, authored as Drools XLS decision-table packages and evaluated by embedded
  Drools (D-RCV-36, ADR-012).
- Hosting: the ACE namespace on the shared ACE AKS clusters; Temporal is self-hosted in the same
  namespace.

## 3. The agent must

1. Put recovery code in the recovery module folder only. Change the common or collection module only
   where the story file names it.
2. Read every threshold, limit, timer, queue, role, template and route from its versioned reference
   table. Never write one as a literal in code.
3. Put a Spring Security method check on every endpoint, naming the capability area and the operation.
4. Write a decision record entry for every change to a case and every decision, with the rule ID and
   version used.
5. Use the names in the business glossary for classes, fields, tables and endpoints.
6. Return each validation message from the message table by its rule ID.
7. Make database changes by migration script only, one script per story. Name it
   `V<seq>__<story>_<name>.sql`; line 1 is `-- Story: <story key>`. A corrective script takes the
   next sequence, keeps the original story key and adds line 2 `-- Fix: <reason>` (D-RCV-28).
8. Use Spring Batch and Quartz for every Epic 1 and Epic 2 scheduled job. From Epic 3, use Temporal
   for the case lifecycle and its activities.
9. Use the synthetic data generator for test data.
10. Write the test before the code. A change with no test is not complete.
11. Respect module boundaries: call another module only through its published interface or an
    application event. Never read another module's tables.
12. Read ACE source data only through `recovery.v_ace_*` views. Never read or write an ACE `public`
    table directly (D-RCV-35 U4, ADR-010, BND-6).
13. Keep unfinished or cross-squad work behind a feature flag that returns the previous code path
    when off.
14. Keep every source and resource file in UTF-8, and test Thai message text by its exact value.
15. When a check reads shared rows and a write depends on it, lock every row or key the check reads,
    not only the rows being written, and cover the race with a concurrency test.
16. Give every narrow check a failing fixture that no broader check also reports, so removing the
    narrow check turns a test red.

## 4. The agent must never

1. Commit a credential, key or token.
2. Call or read the inside of another module.
3. Call a system of record directly. ACE ingests source data; the Workbench reads the views. Outbound
   data leaves through the integration adapters.
4. Add a workflow engine other than Temporal, a rules engine other than embedded Drools, or any other
   new dependency. Temporal and embedded Drools are allowed only as ADR-011 and ADR-012 define them.
5. Disable, skip or weaken a test.
6. Change a migration script that is already merged.
7. Put personal data in code, test fixtures, prompts or log lines.
8. Write business values, thresholds or routes as literals instead of reference data.
9. Rebuild an inbound source load, a tracker, `rule_row` loader, `payment_match_rule` table or a
   home-built workflow engine. D-RCV-35 and D-RCV-36 removed them.
10. Present inferred behaviour as an approved requirement. Mark gaps and record an open item; do not
    ask the user a question in an automated stage.
11. Give the setting that names the running environment (DEV, SIT, UAT, PROD) a default value. A missing or
    invalid value stops the service at startup.
12. Name a tool or model in a commit trailer, merge message or log row other than the one that
    produced the change.

## 5. What the agent reads besides the story

| File | Used for |
|---|---|
| `aisdlc/.github/contexts/project-context.md` | Business truth, actors, features, rules, decisions |
| `aisdlc/.github/contexts/backend-context.md` | Modules, API, data, views, Flyway, Temporal, Drools |
| `aisdlc/.github/contexts/frontend-context.md` | Screens, design system, states, accessibility |
| `aisdlc/.github/contexts/testing-standards.md` | Test levels, data, gates, evidence |
| `aisdlc/.github/contexts/backend-standards.md` / `aisdlc/.github/contexts/frontend-standards.md` | Coding standards |
| Business glossary | Names of classes, fields and endpoints |
| Logical data model and data dictionary | Entities, fields, types and lists of values |
| Business rules and routing logic | Rule IDs, events, conditions and actions |
| Case and workflow model | Stages, milestones, tasks and sentries |
| Users, roles and permissions | Roles, permission letters and scopes |
| Error and message standard | Message IDs and wording |
| API specification | Paths, requests, responses and error codes |
| Non-functional specification | Targets and test evidence |
| Test strategy | Levels, environments and gates |
| Personal data protection design | PDPA classification, masking and retention |

## 6. Story file

One story file per story, held next to the code it produces. The sections follow the SCB X
requirement template for AI code generation: guardrails, business rules, authority, contract and
functional.

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

A story with no business ACs is accepted on its business rules and test cases (D-RCV-16).

## 7. Plan file

The agent writes `plan.md` for each story before any code. It lists the files to add or change, the
tests to write, the migration scripts, the rule tables read, and any question the story file does not
answer. In this repository, an unanswered question is recorded in the plan's `Assumptions` section,
not asked interactively. The tech lead approves the plan on the pull request. A plan that touches more
than one module, or that the agent cannot complete without a decision it cannot default, goes back to
the analyst before any code is written.

## 8. Review and merge

| Review | Checks | Output |
|---|---|---|
| AI first pass | Bugs, security, personal data, module boundaries, the rules in this file, and whether each acceptance criterion has a test | A summary on the pull request |
| Human review | Acceptance criteria, tests, rules as data, personal data, access, module boundaries, names, decision record | Approval or changes requested |

Every pull request carries the story key, the plan file, the coding tool used, the reviewer and the
test results. Any line in production can be traced to a story, a plan and a named reviewer. A defect
traced to AI-written code is tagged as such, and this file is updated before the fix is merged.

## 9. Quality gates

| Gate | Passes when | Owner |
|---|---|---|
| Ready | Every section of the story file is complete; each acceptance criterion can be tested; every rule ID, field and message ID exists in its source document | Analyst with the tech lead |
| Plan approved | The plan names every file, test and migration, and touches one module | Tech lead |
| Merge | The nine pipeline checks pass and a named reviewer approves | Reviewer |
| SIT exit | Every test case for the release passes in SIT | QA lead |
| UAT exit | The business testers sign the UAT scripts for the release | Business lead |
| Release | The SIT and UAT exits are met and unfinished work is behind a flag that is off | Release owner with the application owner |

## 10. Rules for AI tools

1. Only the coding tool approved for SCB code is used on the repository.
2. Agents work in DEV with synthetic data. UAT uses masked data. No production data is used in a
   prompt.
3. Prompts, skills and this standards file are held in the repository and reviewed like code.
4. Throwaway spikes are allowed in DEV only and are never merged.
5. A coding agent acts under the developer's own identity and holds no permission the developer does
   not hold.
6. A lifecycle stage never asks the user a question during an automated run. It records an assumption
   or an open item and continues. The only stop is a safety, credential or production-data issue.

## 11. Known AI errors

The known error list in the ACE standards file applies to the recovery module. Each new entry carries
the date, the error and the rule added to section 3 or 4.

| Date | Error | Rule added |
|---|---|---|
| 2026-11-16 | No entries at the start of this repository. | — |
| 2026-11-18 | RWB-TE-001: after the module move, the Thai text of `ApiError` messages was corrupted (mojibake). Found by the pre-merge ponytail review (Must 1). | Section 3, rule 14 |
| 2026-11-18 | RWB-E1-042: the plan's table shapes did not follow Physical Schema v6, although the plan said they did. Found by the plan gate (PLAN-001, High). | No new rule. Section 5 already requires the data dictionary, and the plan gate caught it |
| 2026-11-18 | RWB-E1-042: an identical repeat of an approved parameter load returned 409 instead of the existing load. The specified case had no test. Found by code gate round 1 (CODE-001, High). | No new rule. Section 3, rule 10 already requires a test for every specified case |
| 2026-11-18 | RWB-TE-002: a root `/CODEOWNERS` could silently replace `.gitlab/CODEOWNERS`, and the security settings file had no owner. Found by the pre-merge security review (F1, F2, High). | No new rule. The ownership test now fails on both (D-RUN-25) |
| 2026-11-18 | RWB-TE-002: one test was written after its fix instead of first (DEV-09). | No new rule. Section 3, rule 10 |
| 2026-11-19 | RWB-E1-042: two different loads for one parameter could both be approved at the same moment, because each approval locked only its own rows. Found by the post-merge review REVIEW-001 (H1). | Section 3, rule 15 |
| 2026-11-19 | RWB-E1-042: `rwb.environment` defaulted to DEV, so a production pod with the variable unset would serve DEV parameter values. Found by REVIEW-001 (H2). | Section 4, rule 11 |
| 2026-11-19 | Build record: 43 commits made in opencode on DeepSeek v4.1 Flash carried `Co-Authored-By: Claude Opus 5.5` and a Claude Code session link (D-RUN-26). Found by the REVIEW-001 evidence audit (H-03). | Section 4, rule 12 |
| 2026-11-19 | RWB-E1-044: every fixture for the migration lint's literal-schema positions used a known qualifier (`public`, `recovery`) that a broader check already reported, so removing the position check left every test green. Found by the Opus 5.5 confirmation code gate (CONF-E044-01, Medium). | Section 3, rule 16 |

## 12. Measures

Published every week from Jira and the pipeline. The first four weeks set the baseline, and targets
are set from it.

| Measure | Definition |
|---|---|
| Cycle time | Working days from ready to merged, per story |
| Review time | Hours from pull request opened to approved |
| Rework rate | Share of pull requests changed after human review |
| Defect escape rate | Defects found in SIT or UAT per story merged |
| Test coverage | Share of changed lines covered by a test |
| AI errors recorded | New entries added to this standards file |
