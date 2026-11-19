---
title: "Implementation Plan — RWB-TE-002 Code owners for the recovery module"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
status: "SUCCESS"
---

# Implementation Plan — RWB-TE-002 Code owners for the recovery module

Design Source: NOT_REQUIRED (`UI In Scope: NO`, `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED`).

| Field | Value |
|---|---|
| Story | `RWB-TE-002` Code owners for the recovery module |
| RUN_ID | `INC-004-epic-1-RWB-TE-002` |
| Input spec | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (`SPEC-RWB-TE-002-001..012`, 7 ACs, 7 exception paths) |
| Governing decisions | D-RCV-21, D-RCV-50, D-RCV-52; L-RCV-12, L-RCV-13 |
| Baseline | Document set v14, 16 November 2026; TE-001 module map |
| Prepared | 2026-11-17, Implementation Planner (agent run) |
| Approval | Plan gate pending human; no question asked |

## Plan approval preconditions

| ID | Precondition | Owner | State | Evidence when met |
|---|---|---|---|---|
| PRE-1 | Specification approval (specification gate) | Product Owner | APPROVED for the v2 baseline 2026-11-17 | `specify/compliance-validation.md` `PASS` |
| PRE-2 | Repository host confirmed: GitHub-compatible `.github/CODEOWNERS`, branch rules and code-owner review | ACE team repository administrator | **PENDING** — `OPEN-038` | Host confirmation comment in the increment card |
| PRE-3 | Teams exist with the handles in the spec; the recovery team membership includes the tech lead and squad developers | ACE team / tech lead | **PENDING** — `OPEN-038` | Team membership export |
| PRE-4 | Pipeline token can read organisation teams and repository permission, or a service token is provisioned | ACE team repository administrator | **PENDING** — `OPEN-038` | Token scope record (no secret in the repository) |
| PRE-5 | Branch names confirmed: `main`, `develop-recovery`, `develop` | ACE team / recovery tech lead | **PENDING** — `OPEN-038` | Branch protection export |
| PRE-6 | Plan approval | Forward Deployed Architect | **PENDING HUMAN** | Approval comment in the increment card |
| PRE-7 | Task approval | Forward Deployed Engineer | **PENDING HUMAN** | Approval comment in the increment card |

`TASK-RWB-TE-002-00` checks PRE-1..PRE-7. If PRE-2..PRE-5 are not confirmed, the plan is complete but
the build does not start. This is a gate, not a question to the user.

## Change scope

| Field | Value |
|---|---|
| Change type | `NEW_STORY` |
| UI in scope | NO |
| Logic in scope | YES — review-control rules BR1–BR7; no application logic |
| API in scope | NO — `NO_API_CHANGE` |
| Frontend changes | NO |
| Backend changes | NO |
| Repository tooling | YES — CODEOWNERS, pipeline validation step, branch rules |
| Migration / database | None |
| New dependency | None; the validation step uses `git` and the repository host's CLI/API available on the runner |

## Scope

### In scope

1. `.github/CODEOWNERS` with the actual TE-001 paths, ordered general-to-specific.
2. Recovery backend/main/test/migration, front-end and module-map entries owned by the recovery team.
3. Common module main and test entries owned by the ACE team.
4. The CODEOWNERS file itself owned by both teams.
5. A pipeline validation step: syntax, owners exist and have write access, every pattern matches a file.
6. Branch rules on `main`, `develop-recovery` and `develop`: require PR, require code-owner review,
   1 approval, dismiss stale approvals, author self-approval not counted.
7. Seven test pull requests for AC1–AC7 and one access check (TC-TE-002-08).
8. Evidence pack and rollback note.

### Out of scope

- The boundary test that checks the code (RWB-TE-001).
- Code owners inside the collection module (ACE team, DL04).
- The browser test runner (RWB-TE-010).
- Workbench roles, capability areas and `MSG-P4-002`.
- Any Java, React, migration or runtime change.

## Repository tooling plan

### T-1 CODEOWNERS

| Item | Value |
|---|---|
| File | `.github/CODEOWNERS` at the repository root |
| Order | General first, specific last; the last matching pattern wins (BR5) |
| Recovery entries | `backend/src/main/java/th/co/scb/ace/demo/recovery/`, `backend/src/test/java/th/co/scb/ace/demo/recovery/`, `backend/src/main/resources/db/modulemigration/recovery/`, `frontend/src/modules/recovery/`, `backend/src/test/resources/architecture/recovery-modules.yaml` |
| Common entries | `backend/src/main/java/th/co/scb/ace/demo/common/` (the test folder is out of scope; `ASM-TE002-05`) |
| File itself | `/.github/CODEOWNERS` owned by both teams |
| Owners | `@scb-ace/techx-recovery-tech-leads`, `@scb-ace/ace-team` (values pending DL37/DL36) |

### T-2 Validation step

| Item | Value |
|---|---|
| Trigger | Every pull request that changes any file |
| Checks | Parse; no empty line; no duplicate pattern; every owner exists and has write access; every pattern matches at least one tracked file |
| Failure | Non-zero exit; `owner {team} not found` or `pattern {pattern} matches no file` |
| Token | Repository token or service token held by the host; never printed, never committed; fail closed if the scope is missing |
| Runner | Linux shell with `git` and the host CLI/API already available; no new package |

### T-3 Branch rules

| Setting | Value |
|---|---|
| Branches | `main`, `develop-recovery`, `develop` |
| Require a pull request | On |
| Require review from code owners | On |
| Required approvals | 1 |
| Dismiss stale approvals on new commits | On |
| Author self-approval | Not counted |
| Conversation resolution | Existing repository policy |

## Backend plan

None. No Java package, controller, service, entity or migration. The generated packages of RWB-TE-003
are not in this story.

## Frontend plan

None. `UI In Scope: NO`; no route, component, label or i18n key. The front-end folder is only a
CODEOWNERS path. Frontend component inventory: `NOT_APPLICABLE` (0 screens); no
`frontend/components.md`.

## Integration and cross-layer

| Item | Plan |
|---|---|
| TE-001 module map | The module map is a CODEOWNERS path, owned by the recovery team; its content is unchanged. |
| ACE CI | The validation step is added to the existing pull-request pipeline; no new service. |
| Repository host | GitHub-compatible per the story; if the host is GitLab, use `.gitlab/CODEOWNERS` and protected-branch approval rules (`OPEN-038`). |
| Branch flow | The same rules apply to `main`, `develop-recovery` and `develop` so no recovery MR bypasses review. |
| Rollback | Revert the file/step in a reviewed PR; restore branch-rule settings. |

## Unit test applicability

| Surface | Changes required | Unit tests | Coverage gate | References | Evidence |
|---|---|---|---|---|---|
| Backend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No Java change. |
| Frontend | NO | NOT_APPLICABLE | NOT_APPLICABLE | — | No front-end change. |
| Repository tooling | YES | NOT_APPLICABLE | NOT_APPLICABLE | BR1–BR7; SPEC-001..012 | The change is configuration; the six system test PRs plus the access check are the evidence. |

## Requirement Logic To Task Coverage

| REQ_REF | Mapped SPEC-* | Mapped TASK-* | Coverage Type | Verification | Status |
|---|---|---|---|---|---|
| BR1 | SPEC-002 | 01, 04, 07, 11 | DIRECT_IMPLEMENTATION | Codeowners entries; TC-01/04 | COVERED |
| BR2 | SPEC-003 | 01, 07, 11 | DIRECT_IMPLEMENTATION | Codeowners entries; TC-04 | COVERED |
| BR3 | SPEC-004 | 01, 05, 11 | DIRECT_IMPLEMENTATION | Common entries; TC-02 | COVERED |
| BR4 | SPEC-005 | 01, 03, 11 | DIRECT_IMPLEMENTATION | File owned by both teams; reviewer check | COVERED |
| BR5 | SPEC-001 | 01, 10, 11 | DIRECT_IMPLEMENTATION | Order review; duplicate/pattern check | COVERED |
| BR6 | SPEC-006, -010, -011 | 03, 04, 08, 09, 12 | DIRECT_IMPLEMENTATION | Branch rules; TC-01/05/06 | COVERED |
| BR7 | SPEC-009 | 01, 03, 11 | DIRECT_IMPLEMENTATION | Handles are values; reviewed change | COVERED |
| AC1 | SPEC-002, -006, -012 | 01, 04, 12 | DIRECT_IMPLEMENTATION | TC-01 merge blocked | COVERED |
| AC2 | SPEC-004, -006 | 01, 05, 12 | DIRECT_IMPLEMENTATION | TC-02 ACE team requested | COVERED |
| AC3 | SPEC-007 | 01, 06, 12 | DIRECT_IMPLEMENTATION | TC-03 both teams | COVERED |
| AC4 | SPEC-002, -003, -012 | 01, 07, 12 | DIRECT_IMPLEMENTATION | TC-04 all three paths | COVERED |
| AC5 | SPEC-010 | 03, 08, 12 | DIRECT_IMPLEMENTATION | TC-05 self-approval blocked | COVERED |
| AC6 | SPEC-011 | 03, 09, 12 | DIRECT_IMPLEMENTATION | TC-06 approval dismissed | COVERED |
| AC7 | SPEC-008 | 02, 10, 12 | DIRECT_IMPLEMENTATION | TC-07 validation fails | COVERED |
| Flow 1–7 | SPEC-001..-009, -012 | 00–12 | DIRECT_IMPLEMENTATION | Build and test sequence | COVERED |
| X1–X7 | SPEC-006..-011 | 03–10, 12 | DIRECT_IMPLEMENTATION | Exception test PRs | COVERED |
| §12 Contract | SPEC-001..-009 | 01–03, 11 | DIRECT_IMPLEMENTATION | File, branch rule, step, trigger | COVERED |
| §17 Guardrails | SPEC-002..-009 | 01, 11, 12 | DIRECT_IMPLEMENTATION | File holds paths/teams only; no PII | COVERED |
| §19 Out of scope | SPEC-012 | 12 | DIRECT_IMPLEMENTATION | Scope note in evidence | COVERED |

Every row is `COVERED`; no `BLOCKED` row. Every task maps to at least one SPEC.

## Functional Test Scenarios

| ID | Scenario | AC | Owner |
|---|---|---|---|
| T-TE002-01 | Recovery PR requests a tech lead; outside approval leaves merge blocked | AC1 | Repository host test PR |
| T-TE002-02 | Common PR requests the ACE team | AC2 | Repository host test PR |
| T-TE002-03 | Cross-module PR needs both teams | AC3 | Repository host test PR |
| T-TE002-04 | Front-end, migration and module map request the recovery team | AC4 | Repository host test PR |
| T-TE002-05 | Tech lead self-approval does not count | AC5 | Repository host test PR |
| T-TE002-06 | New commit dismisses approval | AC6 | Repository host test PR |
| T-TE002-07 | Misspelt owner fails the validation | AC7 | Pipeline test PR |
| T-TE002-08 | Outside team approval is refused | Access | Repository host test PR |

## Security, privacy and compliance

- No personal data; the file holds paths and team handles only.
- No token in the repository; the pipeline token is held by the host and never printed.
- The validation fails closed if the token cannot read teams.
- Test PRs use fixture files only; they are closed after evidence capture.
- The CODEOWNERS file is reviewed by both teams.
- No Workbench capability area or access log applies; this is a repository right.

## Risks

| ID | Risk | Mitigation |
|---|---|---|
| R-01 | Host is GitLab, not GitHub | PRE-2 confirms; use the equivalent file and protected-branch rules; `OPEN-038`. |
| R-02 | Team handle or membership differs | Handles are values; the file changes under both-team review. |
| R-03 | Validation token cannot read teams | Fail closed; provision the token at PRE-4. |
| R-04 | A recovery MR bypasses the rule on `develop-recovery` | Apply the same rule to `main`, `develop-recovery`, `develop`. |
| R-05 | A pattern matches no file after a folder move | Validation fails naming the pattern; update the file. |
| R-06 | A person leaves and blocks a merge | Team handles, never a person. |

## Out of scope

- Boundary test (TE-001), collection-module code owners, browser runner (TE-010), Workbench roles,
  endpoints, screens, migrations and runtime code.

## Assumptions

| ID | Assumption | Basis |
|---|---|---|
| `ASM-TE002-01` | GitHub-compatible host | Story §3/§12; DL37 |
| `ASM-TE002-02` | Actual TE-001 paths | RWB-TE-001; D-RCV-02/10/37 |
| `ASM-TE002-03` | Team handles and membership | D-RCV-21; DL37/DL36 |
| `ASM-TE002-04` | Branch rule on `main`, `develop-recovery`, `develop` | Story §12; D-RCV-50 |
| `ASM-TE002-05` | Common test folder out of scope; follow-up adds it once it exists | BR3; story §12; validation pattern-match rule |
| `ASM-TE002-06` | Pipeline token scope | Story §12 |
| `ASM-TE002-07` | BR4 wins over §10 | Story defect row 91 |
| `L-RCV-03` | No question asked | No-question rule |

## Status reporting

```text
PLAN_STATUS: SUCCESS
TASKS: 13
SCOPE: repository tooling only — CODEOWNERS, pipeline step, branch rules; no module code
BLOCKED_TASKS: 0 (PRE-2..PRE-5 are human gates, not blockers to plan completion)
ASSUMPTIONS: 8
NEXT_STEP: Human plan approval, then start the Implementation Builder on TASK-00..12.
```

```text
PLANNER_STATUS_SUMMARY: Plan and tasks are complete for RWB-TE-002; build is gated on the host, teams, token and branch confirmations.
PLANNER_STATUS_DETAIL: SUCCESS [REASON: one repository-tooling increment, no module code] [UNBLOCK_ACTION: approve plan and confirm OPEN-038]
PLANNER_CLARIFICATION_STATUS: READY [OPEN_ITEMS: 0] [UNBLOCK_ACTION: n/a]
PLANNER_DESIGN_SOURCE: NOT_REQUIRED [NOTE: UI NO]
PLAN_REQUIREMENT_COVERAGE_SUMMARY: All 19 spec coverage rows are mapped to tasks.
PLAN_REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 19] [TASK_COVERED_RULES: 19] [MISSING_TASK_RULES: 0] [AMBIGUOUS_TASK_RULES: 0] [CONTRADICTIONS: 0]
```
