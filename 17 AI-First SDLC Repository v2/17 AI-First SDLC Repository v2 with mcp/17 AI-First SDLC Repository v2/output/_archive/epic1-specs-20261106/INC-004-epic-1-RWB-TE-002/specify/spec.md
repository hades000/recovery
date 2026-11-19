# Technical Specification — RWB-TE-002 Code owners for the recovery module

| Field | Value |
|---|---|
| Story | RWB-TE-002 — Code owners for the recovery module |
| Epic / module | E1 / P2 Integration (technical enabler) |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Source requirement | `requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v5_extracted/RWB TE 002 Code owners for the recovery module v1.md`; REQ-DRI-006; BRD Program §7 |
| Upstream IDs | REQ-DRI-006; DL04 option A; DL07; DL32; DL36; DL37; ADR-006; ADR-008; DT07; DT11 |
| Status | SUCCESS |
| Prepared | 2026-11-04 |
| Author | Technical Specifier (agent run) |
| Approval | TechX recovery tech leads and ACE team (code owners); see `compliance-validation.md` |
## Change Scope Declaration
| Field | Value |
|---|---|
| Change Type | `NEW_STORY` |
| UI In Scope | `NO` — no screen, component, route, label, state or validation presentation. The developer sees the review state on the repository host's pull request page. |
| Logic In Scope | `YES` — path-to-owner mapping, review gating, stale-approval dismissal and the code-owners validation step. |
| API In Scope | `NO` — no endpoint or schema change. Repository-host branch protection is configuration, not an API of the Workbench. |
| API Impact Type | `NO_API_CHANGE` |
| Impacted Existing Nodes | ACE repository `main` branch rule; pull request pipeline; recovery back end, test, migration, front-end and module-map folders created by RWB-TE-001. |
| New Nodes Required | `YES` — `.github/CODEOWNERS`; `CodeOwnersValidation` pipeline step; branch rule on `main`. |
| Inherited Existing Behavior | Recovery folder tree and module map (RWB-TE-001); ACE repository host and team structure (DL32, DL36); merge and release practice (DL04 option A, ADR-008). |
| Frontend Changes Required | `NO` |
| Backend Changes Required | `NO` — no service code, schema or endpoint; the logic is repository-host configuration and a CI validation step. |
## Requirement-to-SPEC Logic Coverage
| REQ_REF | Requirement Logic Statement | Mapped SPEC-* | Coverage Type | Implementation Notes | Status |
|---|---|---|---|---|---|
| BR1 | Every path under the recovery back-end, test and migration folders is owned by the TechX recovery tech leads. | SPEC-RWB-TE-002-002 | DIRECT | Three entries, one per folder; owner is a team handle. | COVERED |
| BR2 | The recovery front-end folder and the module map file are owned by the TechX recovery tech leads. | SPEC-RWB-TE-002-003 | DIRECT | `ace-web/src/modules/recovery/` and `architecture/recovery-modules.yaml`. | COVERED |
| BR3 | The common module folder is owned by the ACE team. | SPEC-RWB-TE-002-004 | DIRECT | `.../common/` maps to `@scb-ace/ace-team`. | COVERED |
| BR4 | The code owners file itself is owned by both teams. | SPEC-RWB-TE-002-005 | DIRECT | Self-entry lists both teams. | COVERED |
| BR5 | The last matching pattern in the file decides the owner, so specific paths come after general ones. | SPEC-RWB-TE-002-006 | DIRECT | File order is general to specific; validation checks order. | COVERED |
| BR6 | A merge to `main` needs one approval from a code owner of every changed path; an author's own approval does not count; a new commit dismisses approvals. | SPEC-RWB-TE-002-007..009 | DIRECT | Branch rule: require PR, code-owner review, 1 approval, dismiss stale. | COVERED |
| BR7 | Team names are values in the file; a change of team is a change to the file, reviewed by both teams. | SPEC-RWB-TE-002-011 | DIRECT | Handles only in the file; no team name in code. | COVERED |
| X1 | A recovery change approved only by a non-owner. | SPEC-RWB-TE-002-007, SPEC-RWB-TE-002-012 | DIRECT | Merge stays blocked. | COVERED |
| X2 | A common module change. | SPEC-RWB-TE-002-004 | DIRECT | ACE team review required. | COVERED |
| X3 | A change across recovery and common. | SPEC-RWB-TE-002-012 | DIRECT | Both teams must approve. | COVERED |
| X4 | The author is a code owner and approves their own change. | SPEC-RWB-TE-002-008 | DIRECT | Own approval does not count. | COVERED |
| X5 | A new commit is pushed after approval. | SPEC-RWB-TE-002-009 | DIRECT | Approval dismissed; re-review. | COVERED |
| X6 | The file names an owner that does not exist. | SPEC-RWB-TE-002-010, SPEC-RWB-TE-002-014 | DIRECT | Build fails: `owner {team} not found`. | COVERED |
| X7 | A squad member outside the owning team approves. | SPEC-RWB-TE-002-012 | DIRECT | Merge refused; no Workbench endpoint, so MSG-P4-002 is not shown. | COVERED |
> **AC cleanup (4 November 2026):** all previous acceptance criteria in this story were development-process criteria and were removed from story §7. This engineering enabler has no business acceptance criteria; the coverage table above maps the business rules and exception paths only.

## User story intent interpretation
As a **squad member (RW-TRIBE)**, I want **a code owners entry that maps every recovery folder to the TechX tech leads and the common module to the ACE team, with review by a code owner required before merge**, so that **every change in the recovery module is reviewed by its owners**.

This is a repository-governance enabler. It names the reviewing team per folder and makes the branch rule on `main` wait for that team. The integration adapter folder — the only place allowed to reach other systems — cannot change without a TechX tech lead. The story adds no screen and no service code; its evidence is the pull request history and the branch-rule configuration.
## Entry trigger and preconditions
| Item | Value |
|---|---|
| Trigger | Every pull request that changes any file; every merge to `main`. |
| Preconditions | RWB-TE-001 done (folders and map exist); the repository host supports a code owners file (GitHub assumed, DL32); the teams exist as `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`; the ACE repository administrator can set the `main` branch rule. |
| Input | Changed paths; `.github/CODEOWNERS`; repository team membership and write access; branch-rule settings. |
| Output | Required reviewers on the pull request; merge allowed only after every owning team approves; a validation result on the pull request. |
| Feature flag | None — the file and branch rule have no runtime path. |
## Field-level behaviour matrix
| Entity / artefact | Field | Prefill / source | Editable state | Constraint |
|---|---|---|---|---|
| `CODEOWNERS` entry | `pattern` | Story §12 contract | Editable by pull request | Valid repository-host pattern; last match wins |
| `CODEOWNERS` entry | `owner` | Team handle (DL37) | Editable by pull request | Team, never a person; exists and has write access |
| Branch rule | `require_pull_request` | Repository setting | Editable by repository administrator | Always on for `main` |
| Branch rule | `require_code_owner_review` | Repository setting | Editable by repository administrator | On |
| Branch rule | `required_approvals` | Repository setting | Editable by repository administrator | 1 per owning team of each changed path |
| Branch rule | `dismiss_stale_approvals` | Repository setting | Editable by repository administrator | On |
| Branch rule | `author_approval_counts` | Repository setting | Not editable | False |
| Validation output | `owner`, `pattern`, `result` | Pipeline step | Read-only | Names the owner or pattern that failed; no personal data |
## Status-transition matrix
| From | Event | Condition | To | Side effects |
|---|---|---|---|---|
| Review required | A code owner of every changed path approves | No new commit | Approved | Merge allowed |
| Review required | A non-owner approves | Owner review still missing | Review required | Merge stays blocked |
| Approved | A new commit is pushed | Stale-approval dismissal on | Review required | Previous approvals dismissed |
| Review required | The validation step finds a missing owner or an unmatched pattern | Any failure | Build failed | Merge blocked; build log names the owner or pattern |
| No case status change | — | — | — | This story does not touch `recovery_case` |
## Exceptional-case behaviour
| ID | Trigger | Behaviour | Message / event |
|---|---|---|---|
| X1 | Only a non-owner approves a recovery change | Merge stays blocked | Repository host: `Review required from code owners` |
| X2 | A common module file changes | ACE team review required | Repository host: `Review required from code owners` |
| X3 | Recovery and common files change together | Both teams must approve | Repository host: `Review required from code owners` |
| X4 | A code owner approves their own pull request | Own approval does not count | Repository host: `Review required from code owners` |
| X5 | A new commit lands after approval | Approval dismissed | Repository host: `Review required from code owners` |
| X6 | An owner handle does not exist or has no write access | Validation step fails | Build log: `owner {team} not found` |
| X7 | A squad member outside the owning team tries to satisfy review | Merge refused | Repository host; no Workbench message |
## API change assessment
| Item | Value |
|---|---|
| API Impact Type | `NO_API_CHANGE` |
| Existing endpoints used | None. The control is the repository host and the pull request pipeline. |
| Contract delta | None. |
| Backward compatibility | Not applicable to the Workbench API. Repository behaviour changes only for merges to `main`. |
| Authorization | Repository rights: team membership and write access. No Workbench capability area applies. |
| Error behaviour | Merge blocked by the repository host; validation failure on the pull request. |
| Versioning | No version change. |
## Unit Test Applicability
| Surface | Changes Required | Unit Tests | Coverage Gate | Requirement/SPEC References | Evidence and Rationale | Test Acceptance Criteria |
|---|---|---|---|---|---|---|
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No screen, component, route, state or label change; the story adds no front-end code. | Existing front-end tests stay green; no new front-end test is required. |
| Backend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No service code, schema or endpoint. The change is a repository file, a branch rule and a pipeline validation step. The behaviour is proven by six test pull requests (TC-TE-002-01..06) and the misspelt-owner test (TC-TE-002-07). | The six test pull requests show the expected reviewer and merge state; the misspelt owner fails the validation step. |
## Detailed design
### Components
| Component | Type | Responsibility |
|---|---|---|
| `CODEOWNERS` | Rule table | Path to owning team, general paths first, specific paths last. |
| `CodeOwnersValidation` | Job | Pipeline step: syntax, every owner exists and has write access, every pattern matches at least one file. |
| Branch rule on `main` | Rule table | Require pull request, require code-owner review, 1 approval, dismiss stale approvals, author approval excluded. |

### File content
The file holds the seven entries in the story contract, in this order: common module, recovery back end, recovery tests, recovery migrations, recovery front end, module map, and the file itself. Team handles are values; a team change is a reviewed edit to this file. No personal name appears.

### Data and migration
None. No database object, no Flyway migration, no reference-data row. The file is versioned with the repository.

### Rules
1. A changed path is matched against the file; the last matching pattern decides the owner (BR5).
2. The repository host requests review from every owning team of every changed path (BR6).
3. The author's own approval is excluded; a new commit dismisses stale approvals (BR6).
4. The validation step fails when the syntax is invalid, an owner does not resolve to a team with write access, or a pattern matches no file.
5. A pull request that touches both recovery and common needs both teams.

### Transaction and events
None. The repository host evaluates the rule at pull request open, review and merge. The result is idempotent for the same file and the same changed paths.

### Security and authority
| Actor | What they may do |
|---|---|
| TechX recovery tech leads | Approve recovery folders and the module map |
| ACE team | Approve the common module and the code owners file; set the `main` branch rule |
| RW-TRIBE, tribe lead, squad members | Open pull requests; cannot satisfy a code-owner review unless in the owning team |
| Repository administrator | Set and maintain the branch rule |

No Workbench capability area applies; access is a repository right, not a Workbench role right.

### Observability and operations
- The pull request page shows the required reviewers and the merge state.
- The validation step reports on every pull request that changes any file.
- The measure is the share of merged pull requests on recovery folders approved by a code owner, target 100%.
- No runtime metric, alert or run book.

### Performance
No runtime path. The validation step runs with the pull request pipeline; no numeric target is stated. A failure names the owner or pattern so the fix is direct.

### Feature flag and rollback
None. Rollback is a reviewed edit to the file or the branch rule; the previous rule can be restored by reverting the pull request.

### No UI change
No screen. The developer reads the required reviewers and the merge state on the repository host's pull request page.
## Test scenarios
| ID | Covers | Level | Data | Expected |
|---|---|---|---|---|
| TC-TE-002-01 | BR1, BR6 | System | Test pull request changing a recovery Java file | TechX tech lead required; outside approval leaves merge blocked |
| TC-TE-002-02 | BR3 | System | Test pull request changing a common module file | ACE team required |
| TC-TE-002-03 | BR6 | System | One recovery file and one common file | Merge blocked until both teams approve |
| TC-TE-002-04 | BR2 | System | Front-end file, migration file and module map | TechX tech lead required for all three |
| TC-TE-002-05 | BR6 | System | Tech lead opens and approves their own pull request | Merge blocked until a second team member approves |
| TC-TE-002-06 | BR6 | System | New commit after approval | Approval dismissed; review required again |
| TC-TE-002-07 | BR7 | System | Misspelt team handle | Validation fails naming the owner |
| TC-TE-002-08 | X7 | Security | Outside squad member approves | Merge refused; no Workbench message |
## Guardrails
- No business value in code; the file holds paths and team handles only.
- No personal data in logs, tests or prompts; test pull requests change fixture files only.
- No read of another module's tables; the file is the review control for the RWB-TE-001 boundary.
- Team handles are teams, never single people, so one person's absence does not block a merge.
## Out of scope
- The boundary test that checks the code: RWB-TE-001.
- Code owners inside the collection module: the ACE team under DL04.
- The browser test runner in the pipeline: RWB-TE-010 (DL37).
## Traceability
| Requirement ID | Requirement (short) | BRD section | Feature | L3 process | Rules | Test cases |
|---|---|---|---|---|---|---|
| REQ-DRI-006 | No component calls a system of record directly | Program §7 | None | All recovery processes | None | TC-TE-002-01..TC-TE-002-08 |
## Clarification Log
| CLAR_ID | Requirement/Spec References | Question or Gap | Implementation Impact | BA/User Response | Status | Resulting SPEC-* |
|---|---|---|---|---|---|---|
| CLAR-001 | BR1–BR4, BR7; SPEC-002..005, SPEC-011 | Team handles are assumed until DL37 and DL36 are answered. | A handle change is a reviewed edit to the file; no code change. | Use `@scb-ace/techx-recovery-tech-leads` and `@scb-ace/ace-team`; confirm at DL37. | RESOLVED | SPEC-011 |
| CLAR-002 | §3; SPEC-001 | Is GitHub the repository host? | Determines the file format and branch-rule names. | Yes, assumed under DL32; the ACE repository uses GitHub. | RESOLVED | SPEC-001 |
| CLAR-003 | SPEC-010 | The migration folder may be empty before the first migration; a pattern that matches no file would fail. | A day-one failure would block every merge. | TE-001 creates the folder with a placeholder; the strict check remains. | RESOLVED | SPEC-010 |
| CLAR-004 | BR5; SPEC-006 | What happens when two patterns match? | Determines the owner when a path is covered twice. | The last matching pattern wins, as the repository host defines; the file is ordered general to specific. | RESOLVED | SPEC-006 |
| CLAR-005 | §12; SPEC-015 | Are run books and operations files owned by the tech leads? | Would extend the file beyond the story contract. | Not in this story; the file follows the seven contract entries. A later reviewed change can add them. | RESOLVED | SPEC-002, SPEC-003 |
| CLAR-006 | BR6; SPEC-008 | Does the repository host count an author's approval? | Determines whether an author's approval counts. | No; the branch rule excludes it, and a second team member is required. | RESOLVED | SPEC-008 |

`CLARIFICATION_STATUS: RESOLVED` — all six items are answered from the story, DL32/DL37 or the repository host's documented behaviour.
## Status reporting
```text
MCP_STATUS_SUMMARY: NOT_APPLICABLE — no Figma or MCP design source for this repository-governance story.
MCP_API_RESULT: NOT_APPLICABLE [API: n/a] [HTTP: n/a] [ERROR: n/a] [RETRY_AFTER: n/a] [NODE_TYPE: n/a] [CHILD_COUNT: n/a]
CHANGE_CLASSIFICATION_SUMMARY: New code-owners file, validation step and branch rule; no screen, service code or API change.
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: repository review governance only]
REQUIREMENT_COVERAGE_SUMMARY: No business acceptance criteria (story §7); all 7 business rules, 7 exception paths and the access path are mapped.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 7] [COVERED_RULES: 7] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]
NEXT_STEP: Human review of spec.md and compliance-validation.md, then start the Implementation Planner.
```
