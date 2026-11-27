# RWB-PLT-TE002-APP Code owners for the recovery module

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

**Change log.** D-RCV-60, 26 November 2026: fixes from the deterministic build-readiness checks (X20 RWB-PLT-TE002-APP). Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

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

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X1 | A pull request changes a recovery folder and only a non owner approves | Merge stays blocked | Repository host: review required from code owners | AC1 |
| X2 | A pull request changes the common module | ACE team review required | Repository host: review required from code owners | AC2 |
| X3 | A pull request changes both recovery and common folders | Both teams must approve | Repository host: review required from code owners | AC3 |
| X4 | The author is a code owner and approves their own change | The author's approval does not count | Repository host: review required from code owners | AC5 |
| X5 | A new commit is pushed after approval | The approval is dismissed; review needed again | Repository host: review required from code owners | AC6 |
| X6 | The code owners file names an owner that does not exist | The validation step fails the build | Build log: owner not found | AC7 |
| X7 | A squad member who is not a code owner tries to satisfy the review | Merge refused | Repository host: review required from code owners | Access test TC-TE-002-08 |

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

#### 12.1 REST operations provided

None. This preserved story provides no REST operation: the as-built control is one file, one pipeline step and one branch rule, and the legacy contract table is kept word for word in the "As built (monolith)" section below.

#### 12.2 REST operations consumed

None. The story makes no REST call of its own at run time. It builds against three published contracts, and the as-built control calls none of them: `RWB-PLT-E1043-CON`, the reference-data contract of rwb-case (owner platform, epic RWB-PLT-LIB, with the service contract behind it being `RWB-P3-E1043-CON` of rwb-case); `RWB-PLT-E1044-CON`, the per-service migration contract (owner platform, epic RWB-PLT-TPL); and `RWB-PLT-N001-CON`, the gateway-bff route contract (owner edge team, epic RWB-PLT-EDGE).

#### 12.3 Events published

None. The story publishes no Kafka event; the control is a repository file, a ruleset and a pipeline job, and none of them is a producer.

#### 12.4 Events consumed

None. The story consumes no Kafka event and subscribes to no topic.

#### 12.5 Workflows and activities

None. The story runs no Temporal workflow and no activity; the validation job is a pipeline job and not a workflow.

#### 12.6 Schedules

None. The story creates no Temporal Schedule; the validation job runs on the pull request trigger of the golden pipeline.

#### 12.7 Tables owned

None. The story owns no table and no schema; it holds no data of any kind.

#### 12.8 Contract fakes

None. The story needs no fake of its own; the fakes of `RWB-PLT-E1043-CON`, `RWB-PLT-E1044-CON` and `RWB-PLT-N001-CON` are published by those contract stories for the repositories that build against them.

#### 12.9 Call-type summary (REST, Kafka, Temporal, File)

| Call type | Count | Detail |
|---|---|---|
| REST | None | The story calls no REST operation and provides none |
| Kafka | None | The story publishes no event and consumes none |
| Temporal | None | The story runs no workflow, no activity and no Schedule |
| File | None | The story writes one versioned repository file, `.github/CODEOWNERS`, and reads no file at run time |

Two external dependencies carry the target state and are not calls: RWB-PLT-TE002-OPS deploys the ownership control across the 19 service repositories and the platform repository, and RWB-PLT-TE001-APP owns the module boundary test that the review control protects. Neither is invoked by this story.

### 13. Solution plan

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

### 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Repository host | A code owner review is missing | Review required from code owners |
| Build log | An owner in the file does not exist | owner {team} not found |

No Workbench message applies; these texts come from the repository host and the pipeline.

### 15. Screens and states

No screen in this story. A developer reads the required reviewers and the merge state on the pull request page of the repository host.

### 16. Test cases

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

Only the Level cell changes from the legacy table: the legacy level `System` maps to `Component` and the legacy level `Access` maps to `End to end`. The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v8.xlsx, tab Story test cases, under the same test case ID.

### 17. Guardrails

- No business value in code: the file holds paths and team handles only, and a business value belongs to the parameters contract or the reference data and never to `.github/CODEOWNERS`.
- No personal data in logs, tests or prompts: test pull requests change fixture files only, and no repository, pipeline log or prompt carries a real account, a real party or a real document.
- No read of another schema or another service's tables: the file is a review control, and DP-15 keeps each migration folder inside the service that owns it, so an owner never approves a change to another service's schema.
- Team handles are teams, never individuals, so the absence of one person does not block a merge and no individual owner can be named in any repository.
- A code owner never approves their own change: the author's own approval does not count on any repository, as in the as-built branch rule.
- No secret, token or credential in a code owners file, a pipeline variable or a test fixture; a reference is resolved at run time by RWB-PLT-NF04-OPS.
- The common module and the gateway-bff composite routes keep their own owners (ACE team and edge team); a recovery team never approves a change to the common module or to a composite route.

### 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 7 | None | All recovery processes | None | TC-TE-002-01 to TC-TE-002-08 |

### 19. Out of scope

- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).

## As built (monolith)

#### 12. Contract

| Item | Value |
|---|---|
| File | `.github/CODEOWNERS` at the repository root |
| Entries | `/ace-service/src/main/java/**/common/ @scb-ace/ace-team`; `/ace-service/src/main/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/test/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/main/resources/db/migration/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-web/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads`; `/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads`; `/.github/CODEOWNERS @scb-ace/ace-team @scb-ace/techx-recovery-tech-leads` |
| Branch rule on main | Require a pull request; require review from code owners; 1 approval; dismiss stale approvals; the author's approval does not count |
| Pipeline step | Code owners validation: syntax, every owner exists and has write access, every pattern matches at least one file |
| Trigger | Every pull request that changes any file |
| Idempotency | The same file and the same changed paths always request the same owners |

#### 13. Solution plan

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
