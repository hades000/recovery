# RWB-PLT-TE002-OPS Code owners for the recovery module

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
| Size | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-16) |
| Depends on (build) | None |
| Contract dependencies | None |
| Contract fake library version | Not applicable: no contract dependency |
| Contract version | Not applicable: no contract dependency |
| Integration dependencies | None |
| External dependencies | None |
| PRD reference | 03 Requirements and specifications/PRD/Recovery Workbench PRD PLT Platform v1.md (FR-PLT-001, FR-PLT-002, FR-PLT-010, FR-PLT-011, FR-PLT-012, FR-PLT-013, FR-PLT-027) |
| Status | Draft (directive resolutions) |

**Change log.** D-RCV-60, 22 November 2026: delta story for RWB-TE-002 that moves the code-owner control from the one monolith repository to the 19 service repositories and the platform repository, with one CODEOWNERS file and one branch ruleset on main per repository and one code-owner validation job in the golden pipeline (Arch v5 slides 20, 29, 35 and 38; DP-07, DP-15, DP-19). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: fixes from the rulings workbook (X20 RWB-PLT-TE002-OPS). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

**Change log.** D-RCV-60, 26 November 2026: directive resolutions under the programme directive (6 resolved, 15 cross-document, 3 not applied). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story

As a **DevOps engineer**, I want **one CODEOWNERS file, one branch ruleset on main and one code-owner validation job in every one of the 19 service repositories and in the platform repository, so that every change is reviewed by the team that answers for the path and no repository is unowned**, so that **no change reaches a service repository, a migration folder, a composite route or the shared common module without the owning team's approval, and no individual is ever named as an owner**.

### 2. Business rationale

The as-built control of RWB-TE-002 is sized for one repository: seven entries in `.github/CODEOWNERS` cover the recovery back end, the tests, the migration folder, the front end, the module map and the common module, and one branch rule on main holds the merge until a code owner approves. Arch v5 replaces that shape. Slide 20 states that every service is built from one template and shared libraries and holds its own schema, its own task queue and its own release; slide 29 adds that each service has one schema, one login, its own migrations and a boundary test in every build; slide 35 denies by default and authenticates every call with a workload identity; slide 38 makes the template and the golden pipeline a wave-0 enabler built once before the first service exists. Applied to the estate, that is 19 service repositories plus the platform repository, and every one of them needs the control the single repository has today. A monolith file cannot be copied unchanged: the paths it names do not exist in a service repository, and the pattern that covered `/ace-service/src/main/java/**/recovery/` would cover 19 different services if it were copied.

Three decoupling patterns make the ownership map concrete. DP-15 puts one Flyway sequence and one migration folder in each service's own schema, so each migration folder must be covered by the owner of that service and by nobody else. DP-07 puts the reference-data client behind the reference-data contract of rwb-case, so the client wiring in a service repository belongs to that service team. DP-19 puts every screen behind a gateway-bff composite route, so the composite routes are owned by the edge team and not by any service team. Without one control per repository, a service repository can merge a change to another service's migration folder, a composite route can change without the edge team, and an individual account can stand in for a team. It supports REQ-DRI-006, because the module boundary that RWB-PLT-TE001-APP tests in every build is only as strong as the review that guards it. The measure is the share of merged pull requests in the 19 service repositories and the platform repository approved by a code owner of every changed path, which must be 100 percent, with no repository without an owner row.

### 3. Preconditions

- The repository and pipeline baseline of RWB-PLT-NF01-OPS exists: one repository per service of the 19-service list, the platform repository, and the one golden pipeline definition that every repository runs.
- The quality-gate definitions of RWB-PLT-NF05-OPS exist, because those gates are the required status checks a branch ruleset names.
- The module boundary test of RWB-PLT-TE001-APP exists and runs as a check in every repository build, because that check is the second required status check.
- The repository host supports a code owners file and a branch ruleset (GitHub format assumed, as in RWB-TE-002 under DL32), and it can require status checks by name.
- The teams exist in the repository host and have write access to their repositories; the handle convention of the as-built file is kept, one handle per owning team.
- The platform template of epic RWB-PLT-TPL defines the folder set of a service repository, so an owner table can name a folder without inventing one.
- No build dependency: the story is Day 1 by rule (Template and Rules §R5.7) and it waits for no other story to start.
- The team handles, the required-check list and its order, and the ruleset name are Not specified in the source documents (GAP-1432; ASM-2516).

### 4. Flow

1. Take the 20 repositories from the repository inventory of RWB-PLT-NF01-OPS: the 19 service repositories of the 19-service list and the platform repository.
2. Write one `.github/CODEOWNERS` file at the root of each repository, with the general paths first and the most specific path last, as BR7 of RWB-TE-002 requires.
3. Write one owner table per repository in the platform repository: the repository row, the folders it covers, the owning team handle, and the artefact that makes the folder necessary (the per-service migration folder of DP-15, the reference-data client of DP-07, the composite routes of DP-19).
4. Cover the shared folders explicitly: the common module is owned by the ACE team in every repository that carries it, and the platform template folders are owned by the platform team.
5. Apply one branch ruleset on `main` in each repository: a pull request is required, review from a code owner is required, stale approvals are dismissed on a new commit, and the author's own approval does not count.
6. Name the required status checks of that ruleset: the quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP.
7. Add one code-owner validation job to the golden pipeline: syntax, every handle exists and has write access, and every pattern matches at least one tracked file; a finding fails the build.
8. Prove the control on two repositories (one service repository and the platform repository) with a test pull request per acceptance criterion, then hand the owner table and the file to each service team, which changes only its own file.
9. Prove a team change: replace one handle with a second team handle in a test branch and show that both the old and the new owning team must approve.

### 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A repository has no CODEOWNERS file, or its file covers no folder of the template | The baseline check fails and names the repository and the folder | None (release error with an exit code and a job log line) | AC1, AC4 |
| X2 | A file names an individual account, or a handle with no write access | The validation job fails the build and names the entry; the change is not merged | owner {team} not found | AC3, AC4 |
| X3 | A pattern matches no tracked file | The validation job fails the build and names the pattern | Not specified in the source documents (GAP-1432; ASM-2515) | AC3 |
| X4 | A pull request on `main` has no code-owner approval, or only the author's own approval | The merge stays blocked | Review required from code owners | AC2 |
| X5 | A required status check is missing or failing | The ruleset blocks the merge until both required checks pass | None (the repository host reports the missing check by name) | AC2 |
| X6 | A team handle changes for a folder | The pull request requires approval from the old owning team and from the new owning team; the merge waits for both | Review required from code owners | AC5 |

### 6. INVEST check

| Test | Result |
|---|---|
| Independent | No build dependency; reads the 20 repositories of RWB-PLT-NF01-OPS, the gate names of RWB-PLT-NF05-OPS and the boundary check of RWB-PLT-TE001-APP only |
| Negotiable | The team handles, the ruleset name and the order of the required-check list are agreed with the solution architect and the platform administrator; the one-file-per-repository rule, the ruleset content and the validation rules are fixed |
| Valuable | Gives every repository the same review control on Day 1 and makes an unowned repository or an individual owner a baseline failure instead of a review finding |
| Estimable | One file and one owner table per repository for 20 rows, one ruleset per repository, one validation job in the golden pipeline; five acceptance criteria |
| Small | Fits one sprint with the templates, the job and the two test repositories |
| Testable | Every criterion is tested with a planted file, a planted handle, a planted pattern and a test pull request in a test branch |

### 7. Acceptance criteria

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

### 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | One code owners file per repository, at the root, for each of the 19 service repositories and for the platform repository | Arch v5 slides 20 and 38; RWB-PLT-NF01-OPS |
| BR2 | Every entry names a team handle and never an individual account, so the absence of one person never blocks a merge | RWB-TE-002 BR7 (DL37); Template and Rules §R5.3 |
| BR3 | The owned paths of a service repository cover its per-service migration folder (DP-15), its reference-data client (DP-07) and its own business folders; the gateway-bff composite routes (DP-19) are owned by the edge team | DP-07; DP-15; DP-19; Arch v5 slides 20 and 29 |
| BR4 | One branch ruleset on `main` per repository, named Not specified in the source documents (GAP-1432), in each of the 19 service repositories and the platform repository: a pull request is required, review from a code owner is required, stale approvals are dismissed, and the author's own approval does not count | RWB-TE-002 BR6 |
| BR5 | The required status checks of the ruleset are the quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP | RWB-PLT-NF05-OPS; RWB-PLT-TE001-APP |
| BR6 | One code-owner validation job in the golden pipeline fails the build on an unknown handle, a handle without write access, or a pattern that matches no tracked file | RWB-TE-002 BR5; Arch v5 slide 29 (checked in every build) |
| BR7 | The last matching pattern decides the owner, so specific paths come after general ones; general paths are written first in every file | RWB-TE-002 BR5 |
| BR8 | A change of team handle is a change to the file, reviewed by the old owning team and by the new owning team, and recorded in the owner table | RWB-TE-002 BR7; DL37 |

### 9. State transitions

None. This story changes no business state and no case status. It moves the review state of a pull request in each repository through review required, approved, and dismissed on a new commit, exactly as the as-built branch rule does in one repository; that is a state of a change and not a state of a case, and it carries no case status, no queue and no timer.

### 10. Authority

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

### 11. Data

**Value classes and their source**

| Value class | Examples | Source of the value | Where the value is held | BR Field ID |
|---|---|---|---|---|
| Repository row | A service repository of the 19-service list, and the platform repository | The repository inventory of RWB-PLT-NF01-OPS | The owner table in the platform repository | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| Path pattern | The folder of a service, its per-service migration folder, the common module folder, the composite route folder | The platform template of epic RWB-PLT-TPL and the three DPs | The code owners file of the repository, and the owner table | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| Team handle | The handle of the service team, of the ACE team, of the platform team and of the edge team | The repository host, through the handle convention of RWB-TE-002 | The code owners file only; no business value | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| Ruleset definition | Pull request required, code-owner review, stale approvals dismissed, author excluded, required checks | Template and Rules and RWB-TE-002 BR6 | The branch ruleset of each repository | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| Required-check list | The quality gates of RWB-PLT-NF05-OPS and the module boundary test of RWB-PLT-TE001-APP | The two stories that own the checks | The branch ruleset of each repository | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| Validation result | Pass or fail, the handle or pattern named, the file version | The validation job of the golden pipeline | The build record | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |

**Naming and values not in the source set**

| Value | Status | BR Field ID |
|---|---|---|
| The team handle of each of the 20 repositories | Not specified in the source documents (GAP-1432; ASM-2516) | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| The ruleset name | Not specified in the source documents (GAP-1432; ASM-2517) | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| The required-check list and its order | Not specified in the source documents (GAP-1432; ASM-2517) | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |
| The owner of the platform repository and of the template folders | Not specified in the source documents (GAP-1432; ASM-2518) | Not specified in the source documents (DOR-RWB-PLT-TE002-OPS-7) |

The control holds rule definitions, paths and team handles only. It holds no business value, no personal data and no credential: a business value belongs to the parameters contract or the reference data, a personal value belongs to the owning service, masked, and a credential is a key-store reference owned by RWB-PLT-NF04-OPS.

### 12. Contract

#### 12.1 REST operations provided

None. The story provides no REST operation; it deploys a repository file, a branch ruleset and a pipeline job, and none of them exposes a service path.

#### 12.2 REST operations consumed

None. The story calls no REST operation of its own. The contracts named by DP-07 and DP-15 are consumed by the services themselves and not by this control, and the composite routes of DP-19 are consumed by the gateway-bff; this story only makes sure an owner covers each of them.

#### 12.3 Events published

None. The story publishes no Kafka event; a validation result is a build record and a ruleset decision is a repository-host event, and neither is a business event.

#### 12.4 Events consumed

None. The story consumes no Kafka event and subscribes to no topic.

#### 12.5 Workflows and activities

None. The story runs no Temporal workflow and no activity; the validation job is a pipeline job and the review is a repository-host process.

#### 12.6 Schedules

None. The story creates no Temporal Schedule; the validation job runs on the pull request trigger and the baseline check runs on the pipeline trigger of the platform repository.

#### 12.7 Tables owned

None. The story owns no table and no schema; the owner table is a versioned file in the platform repository and not a database table.

#### 12.8 Contract fakes

None. The story needs no fake: it calls no contract at run time, and the test pull requests, the planted handle and the planted pattern are fixtures of the validation job and not contract fakes.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | The story provides no REST operation and calls none |
| Kafka | None | The story publishes no event and consumes none |
| Temporal | None | The story runs no workflow, no activity and no Schedule |
| File | 20 written, 20 read | One `.github/CODEOWNERS` file and one owner-table row per repository, written at build time and read by the repository host and the validation job |

None of the four call types crosses a service boundary: the control is repository configuration and pipeline configuration, and the service calls it guards are the ones the service stories own.

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Repository host | A code owner review is missing on a pull request of any repository, or only the author's own approval is present | Review required from code owners |
| Build log | An owner in a code owners file does not exist or has no write access | owner {team} not found |
| Build log | A pattern in a code owners file matches no tracked file | Not specified in the source documents (GAP-1432; ASM-2515) |

No Workbench message applies and no catalogue message ID is used: these texts come from the repository host and the pipeline, they are never shown to a case user, and a validation finding names the repository, the entry and the rule without repeating any value.

### 15. Screens and states

None. The story adds no Workbench screen and no screen state. The surfaces it uses are the pull request page of the repository host, which shows the required reviewers and the required checks of the ruleset, and the build record of the validation job; both are read-only for the developer and are changed only through a change to the repository or to the platform repository.

### 16. Test cases

| TC ID | Covers | Level | Data |
|---|---|---|---|
| TC-PLT-TE002-OPS-01 | AC1 | Contract | The 20 repositories: one `.github/CODEOWNERS` each, team handles only, the per-service migration folder and the reference-data client covered in their own repository, the composite routes covered by the edge team, the common module by the ACE team |
| TC-PLT-TE002-OPS-02 | AC2 | Integration | Two test repositories with the ruleset on `main`: a pull request without a code-owner approval, with only the author's approval, with a dismissed approval after a new commit, and with a missing and a failing required check, each blocked |
| TC-PLT-TE002-OPS-03 | AC3 | Component | Fixture files of the validation job: an unknown handle, a handle without write access, an unmatched pattern and a clean file; the three refusals and the passing run with the file version in the build record |
| TC-PLT-TE002-OPS-04 | AC4 | Component | The 20-row owner table and the baseline check: a repository without a row, a service whose file covers no folder of the template, an individual account in a file, and the clean 20-row pass |
| TC-PLT-TE002-OPS-05 | AC5 | End to end | A team change on a test branch: the old and the new owning team each approve, the merge waits for both, and the owner table records the new handle |

The as-built tests of the preserved control stay in RWB-PLT-TE002-APP section 16 under their own identifiers TC-TE-002-01 to TC-TE-002-08, and the full Given, When and Then of every case, old and new, is in Recovery Workbench Test Cases v8.xlsx under the same test case ID.

### 17. Guardrails

- No individual owner: every entry is a team handle, so no person's absence blocks a merge and no person is named in a repository file (RWB-TE-002 BR7, DL37).
- No business value in code: the file holds paths and handles only, and a threshold, a list value or a name comes from the parameters contract or the reference-data contract (DP-07).
- No personal data in logs, tests or prompts: the fixtures of the validation job are synthetic handles and patterns, and no test pull request carries a real account, a real party or a real document.
- No cross-schema ownership: a service team owns its own migration folder and never approves a change to another service's folder or schema (DP-15; Arch v5 slide 29).
- The common module and the composite routes keep their own owners: the ACE team owns the common module and the edge team owns the gateway-bff composite routes (DP-19).
- A code owner never approves their own change: the author's own approval does not count in any repository (RWB-TE-002 BR6).
- No secret, token or credential in a code owners file, a ruleset value or a pipeline variable; a credential is a key-store reference owned by RWB-PLT-NF04-OPS.
- The ruleset is applied through the platform repository and the repository settings only; no repository is edited by hand outside its own pipeline.

### 18. Traceability

| Requirement ID | Requirement (short) | Deployment element | Test cases |
|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | The code owners file and the branch ruleset of every repository, which guard the module boundary in review | TC-PLT-TE002-OPS-02, TC-PLT-TE002-OPS-05 |
| DP-07 | Reference data and lists through the reference-data contract of rwb-case | The reference-data client folder as an owner row of every service repository that reads a list | TC-PLT-TE002-OPS-01 |
| DP-15 | Per-service Flyway sequence in the service's own schema | The per-service migration folder as an owner row of its own service repository, and no cross-service owner | TC-PLT-TE002-OPS-01, TC-PLT-TE002-OPS-04 |
| DP-19 | Gateway-bff composite route for every screen | The composite route entries owned by the edge team and by no service team | TC-PLT-TE002-OPS-01 |
| Arch v5 slides 20, 29, 35 and 38 | Every service from one template with its own schema and release; one schema and one login per service with the boundary checked in every build; deny by default with a per-service identity; the template and the golden pipeline built once in wave 0 | The one-file-per-repository rule, the required boundary check, the team-only ownership and the golden-pipeline validation job | TC-PLT-TE002-OPS-01, TC-PLT-TE002-OPS-02, TC-PLT-TE002-OPS-03 |

### 19. Out of scope

- The preserved as-built control of RWB-TE-002: the single-repository code owners file, its validation step and its branch rule stay word for word in RWB-PLT-TE002-APP and are not changed by this story.
- The module boundary test itself: RWB-PLT-TE001-APP owns the test, and this story only names it as a required status check.
- The quality-gate definitions: RWB-PLT-NF05-OPS owns the gates, and this story only names them as required status checks.
- The repository layout, the pipeline stages and the build record: RWB-PLT-NF01-OPS owns the repository and pipeline baseline, and this story adds the ownership control inside it.
- The specific team names and handles: DL37 is still open, so every handle is a value of the owner table and is Not specified in the source documents (GAP-1432; ASM-2516).
- The 19 migrations and their files (RWB-PLT-E1044-OPS), the reference-data contract and its client library (RWB-PLT-E1043-CON) and the gateway-bff composite routes (RWB-PLT-N001-CON): those stories own the artefacts that the owner rows cover.
