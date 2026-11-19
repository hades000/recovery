<!-- source: 04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 002 Code owners for the recovery module v1.md -->
<!-- converted: 2026-11-04 from Markdown (extracted) -->

> **Source:** `04 User stories/Recovery Workbench User Stories Epic 1 Story Files v5.zip!RWB TE 002 Code owners for the recovery module v1.md`  
> **Converted from:** Markdown (extracted)

# RWB-TE-002 Code owners for the recovery module

SCB Collections and Recovery. Henka Group, 28 October 2026.

(C) Siam Commercial Bank and Henka Pte Ltd


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

## 1. Story

As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.

## 2. Business rationale

The recovery and collection squads and the ACE team merge into one repository and one monthly release. Without named owners per folder, a change to the recovery module or to the common module can merge without the team that answers for it. The code owners file names the reviewing team per folder and the branch rule on main blocks a merge until that team approves. It supports REQ-DRI-006, because the integration adapter folder, the only place allowed to reach other systems, cannot change without a TechX tech lead, and it applies DL04 option A and DL37. The measure is the share of merged pull requests on recovery folders approved by a code owner, which must be 100 percent.

## 3. Preconditions

- RWB-TE-001 is done: the recovery folders and the module map exist.
- The repository host supports a code owners file (GitHub format assumed, as ACE uses GitHub Copilot under DL32).
- The teams exist in the repository host: TechX recovery tech leads and the ACE team. Names assumed until DL37 and DL36 are answered: `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`.
- The repository administrator of the ACE team can set the branch rule on main.

## 4. Flow

1. Squad member: writes `.github/CODEOWNERS` with the entries in BR1 to BR5, ordered so that the most specific path is last.
2. Squad member: adds the code owners validation step to the pull request pipeline.
3. ACE team repository administrator: sets the branch rule on main: one approval from a code owner required, stale approvals dismissed on a new commit.
4. Developer: opens a pull request that changes a recovery folder.
5. Repository host: requests review from the owning team named for each changed path.
6. Pipeline: runs the validation step; an owner that does not exist or a path that matches no file fails the check.
7. Code owner: approves; the merge is allowed once every owning team of the changed paths has approved.

## 5. Exception paths

| ID | Trigger | What happens | Message | Covered by |
|---|---|---|---|---|
| X7 | A squad member who is not a code owner tries to satisfy the review | Merge refused | Repository host: review required from code owners | Access test TC-TE-002-08 |

## 6. INVEST check

| Test | Result |
|---|---|
| Independent | Needs only the folders from RWB-TE-001 |
| Negotiable | Team names are values in one file (DL37) |
| Valuable | No change to the recovery or common module merges without its owner |
| Estimable | One file, one pipeline step, one branch rule |
| Small | 1 point |
| Testable | The test cases in section 16 use pull requests in a test branch |

## 7. Acceptance criteria

No business acceptance criteria. This story is an engineering enabler for Git code-owner review and merge rules; its development-process criteria were removed on 4 November 2026.

## 8. Business rules

| ID | Rule | Source |
|---|---|---|
| BR1 | Every path under the recovery back end, test and migration folders is owned by the TechX recovery tech leads | DL04 option A; DL37 |
| BR2 | The recovery front end folder and the module map file are owned by the TechX recovery tech leads | ADR-006; DL07 |
| BR3 | The common module folder is owned by the ACE team | DL04 option A; DT07 |
| BR4 | The code owners file itself is owned by both teams | DL04 |
| BR5 | The last matching pattern in the file decides the owner, so specific paths come after general ones | Repository host rule |
| BR6 | A merge to main needs one approval from a code owner of every changed path; an author's own approval does not count; a new commit dismisses approvals | ADR-008; DT11 |
| BR7 | Team names are values in the file; a change of team is a change to the file, reviewed by both teams | DL37 |

## 9. State transitions

None. This story does not change a case status. It sets the review state of a pull request: review required, approved, or dismissed on a new commit.

## 10. Authority

| Who | What they may do in this story |
|---|---|
| TechX recovery tech leads | Approve changes to recovery folders and the module map |
| ACE team | Approves changes to the common module and the code owners file; sets the branch rule on main |
| RW-TRIBE, tribe lead and squad members | Open pull requests; cannot satisfy a code owner review unless in the owning team |
| No Workbench capability area applies | Access is a repository right, not a Workbench role right |

## 11. Data

No business field is read or written.

Field IDs are those in the Logical Data Model and Data Dictionary.

## 12. Contract

| Item | Value |
|---|---|
| File | `.github/CODEOWNERS` at the repository root |
| Entries | `/ace-service/src/main/java/**/common/ @scb-ace/ace-team`; `/ace-service/src/main/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/test/java/**/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-service/src/main/resources/db/migration/recovery/ @scb-ace/techx-recovery-tech-leads`; `/ace-web/src/modules/recovery/ @scb-ace/techx-recovery-tech-leads`; `/architecture/recovery-modules.yaml @scb-ace/techx-recovery-tech-leads`; `/.github/CODEOWNERS @scb-ace/ace-team @scb-ace/techx-recovery-tech-leads` |
| Branch rule on main | Require a pull request; require review from code owners; 1 approval; dismiss stale approvals; the author's approval does not count |
| Pipeline step | Code owners validation: syntax, every owner exists and has write access, every pattern matches at least one file |
| Trigger | Every pull request that changes any file |
| Idempotency | The same file and the same changed paths always request the same owners |

## 13. Solution plan

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
2. Add the validation step to the pull request pipeline and prove it fails on a misspelt team.
3. Ask the ACE team repository administrator to set the branch rule on main (BR6).
4. Run the six test pull requests in a test branch protected by the same rule and record the result in the pull request history.

**Feature flag.** None. The file and the branch rule have no runtime path.

**Done when.** The tests in section 16 pass and the branch rule on main shows code owner review as required.

## 14. Validation and messages

| ID | When | Message |
|---|---|---|
| Repository host | A code owner review is missing | Review required from code owners |
| Build log | An owner in the file does not exist | owner {team} not found |

No Workbench message applies; these texts come from the repository host and the pipeline.

## 15. Screens and states

No screen in this story. A developer reads the required reviewers and the merge state on the pull request page of the repository host.

## 16. Test cases

| ID | Covers | Level | Data |
|---|---|---|---|
| TC-TE-002-01 | BR1, BR6 | System | Test pull request changing a recovery Java file |
| TC-TE-002-02 | BR3 | System | Test pull request changing a common module file |
| TC-TE-002-03 | BR6 | System | Test pull request changing one file of each |
| TC-TE-002-04 | BR2 | System | Front end file, migration file and the module map |
| TC-TE-002-05 | BR6 | System | Tech lead approves own pull request |
| TC-TE-002-06 | BR6 | System | New commit after approval |
| TC-TE-002-07 | BR7 | System | Misspelt team name in the file |
| TC-TE-002-08 | Access | Access | A squad member outside the owning team approves; the merge is refused. This story has no Workbench endpoint, so MSG-P4-002 is not shown |

The full test, with its Given, When and Then, is in Recovery Workbench Test Cases v5.xlsx, tab Story test cases, under the same test case ID.

## 17. Guardrails

- No business value in code; the file holds paths and team names only.
- No personal data in logs, tests or prompts; test pull requests change fixture files only.
- No read of another module's tables; the file is the review control for the boundary of RWB-TE-001.
- Team handles are teams, never single people, so absence of one person does not block a merge.

## 18. Traceability

| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Business Requirements Program, section 7 | None | All recovery processes | None | TC-TE-002-01 to TC-TE-002-08 |

## 19. Out of scope

- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).
