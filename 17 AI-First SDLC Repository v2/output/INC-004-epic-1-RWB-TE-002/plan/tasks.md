---
title: "Tasks — RWB-TE-002 Code owners for the recovery module"
run_id: "INC-004-epic-1-RWB-TE-002"
story: "RWB-TE-002"
---

# Tasks — RWB-TE-002

Design Source: NOT_REQUIRED (`UI In Scope: NO`).

Plan: `plan.md`. All paths are in the ACE repository unless they start with `output/` or `docs/`.
Task IDs are `TASK-RWB-TE-002-NN`; the short form `TASK-NN` in `plan.md` means the same task.

**Every build task is blocked by TASK-00 (plan-approval preconditions).** No application code is built;
the "build" is the CODEOWNERS file, the pipeline validation step and the branch rules.

## Task table

| TASK ID | Description | Trace (SPEC/FR/NFR) | BLOCKED_BY | Verification |
|---|---|---|---|---|
| `TASK-RWB-TE-002-00` | **Plan precondition check.** Confirm PRE-1 spec approval, PRE-2 host, PRE-3 teams, PRE-4 token scope, PRE-5 branch names, PRE-6 plan approval and PRE-7 task approval each have a decision and a date. Confirm the recovery team membership includes the tech lead and squad developers. Stop with `BLOCKED` if PRE-2..PRE-5 are unconfirmed. | SPEC-006, -012; D-RCV-21, -50; `OPEN-038` | NONE | Decisions and dates recorded in `output/INC-004-epic-1-RWB-TE-002/implement/report.md` |
| `TASK-RWB-TE-002-01` | **Write `.github/CODEOWNERS`** with the entries and order in `plan.md` §T-1: common main/test first, recovery main/test/migration/frontend/module-map next, the file itself last. Use the actual TE-001 paths; team handles as values. | SPEC-001..-005, -009; BR1–BR5, -007 | 00 | File exists; `grep -c '@scb-ace/'` = 8 (7 patterns, the file has two owners); order reviewed; no personal name |
| `TASK-RWB-TE-002-02` | **Add the `CodeOwnersValidation` step** to the pull-request pipeline. Parse comments/blank lines; reject a line with no owner or a duplicate pattern; resolve each owner with the host API; check write access; check every pattern matches at least one tracked file; fail non-zero with the exact message. | SPEC-008; BR5, -007; AC7, X6 | 00, 01 | Pipeline YAML lint; a fixture PR with a misspelt owner fails; a valid PR passes |
| `TASK-RWB-TE-002-03` | **Set the branch rules** on `main`, `develop-recovery` and `develop`: require PR; require review from code owners; 1 approval; dismiss stale approvals; author self-approval not counted. Export the settings. | SPEC-006, -010, -011; BR6; AC5, AC6 | 00 | Branch-rule export shows every setting on every branch |
| `TASK-RWB-TE-002-04` | **Test PR — recovery change (AC1).** Change a fixture file under `backend/src/main/java/th/co/scb/ace/demo/recovery/`; confirm the recovery team is requested and an outside approval leaves the merge blocked. Close the PR without merge. | SPEC-002, -006, -012; AC1, X1; TC-TE-002-01 | 01, 02, 03 | PR history shows the requested reviewer and blocked merge |
| `TASK-RWB-TE-002-05` | **Test PR — common change (AC2).** Change a fixture file under `backend/src/main/java/th/co/scb/ace/demo/common/`; confirm `@scb-ace/ace-team` is requested. Close without merge. | SPEC-004, -006; AC2, X2; TC-TE-002-02 | 01, 02, 03 | PR history shows the ACE team reviewer |
| `TASK-RWB-TE-002-06` | **Test PR — cross-module change (AC3).** Change one recovery and one common fixture file; a recovery approval leaves the merge blocked until an ACE team member approves. Close without merge. | SPEC-007; AC3, X3; TC-TE-002-03 | 01, 02, 03 | PR history shows both teams and the block |
| `TASK-RWB-TE-002-07` | **Test PR — front end, migration and module map (AC4).** Change `frontend/src/modules/recovery/` fixture, a `db/modulemigration/recovery/` fixture and `backend/src/test/resources/architecture/recovery-modules.yaml`; confirm the recovery team is requested for all three. Restore the module map if changed; close without merge. | SPEC-002, -003, -012; AC4; TC-TE-002-04 | 01, 02, 03 | PR history shows the recovery team for all three paths |
| `TASK-RWB-TE-002-08` | **Test PR — author self-approval (AC5).** Open a recovery PR as a recovery team member; attempt to approve it; confirm the merge stays blocked until a second member approves. Close without merge. | SPEC-010; AC5, X4; TC-TE-002-05 | 03 | PR history shows the self-approval not counted |
| `TASK-RWB-TE-002-09` | **Test PR — new commit (AC6).** Approve a recovery PR; push a new fixture commit; confirm the approval is dismissed and review is required again. Close without merge. | SPEC-011; AC6, X5; TC-TE-002-06 | 03 | PR history shows the dismissed approval |
| `TASK-RWB-TE-002-10` | **Test PR — missing owner (AC7).** Change the recovery owner to a misspelt handle; run the validation; confirm it fails with `owner {team} not found`; restore the file. | SPEC-008; AC7, X6; TC-TE-002-07 | 02 | Pipeline log names the missing owner; the valid file passes after restore |
| `TASK-RWB-TE-002-11` | **Access check (TC-TE-002-08).** A squad member outside the owning team approves a recovery PR; confirm the merge is refused and no Workbench `MSG-P4-002` is shown. Close without merge. | SPEC-006; AC1; TC-TE-002-08 | 01, 03 | PR history shows the refusal |
| `TASK-RWB-TE-002-12` | **Evidence, rollback note and trace.** Save the branch-rule export, the pipeline log, the test PR links and the CODEOWNERS diff under `output/INC-004-epic-1-RWB-TE-002/implement/`. Update `requirement/Traceability_Matrix.md` row 004 and the increment card. Record the rollback (revert file/step, restore branch rules). Do not commit, push or change branch rules unless the user asks. | SPEC-012; §17/§19 | 04–11 | Evidence files present; matrix row updated; rollback note present |

## Dependency graph

```text
00 ─► 01 ─┬─► 02 ─┬─► 04 ─┐
          │       ├─► 05 ─┤
          │       ├─► 06 ─┤
          │       ├─► 07 ─┤
          │       ├─► 10 ─┤
          │       └─► 11 ─┤
          └─► 03 ─┬─► 04 ─┤
                  ├─► 05 ─┤
                  ├─► 06 ─┤
                  ├─► 07 ─┤
                  ├─► 08 ─┤
                  ├─► 09 ─┤
                  └─► 11 ─┘
                           └─► 12
```

No cycle. TASK-04..11 run in parallel after 01–03; TASK-12 closes the evidence.

## Coverage

| SPEC | Tasks |
|---|---|
| 001 | 01 |
| 002 | 01, 04, 07 |
| 003 | 01, 07 |
| 004 | 01, 05 |
| 005 | 01 |
| 006 | 00, 03, 04, 05, 08, 09, 11 |
| 007 | 01, 06 |
| 008 | 00, 02, 10 |
| 009 | 01 |
| 010 | 03, 08 |
| 011 | 03, 09 |
| 012 | 00, 04, 07, 12 |

Every SPEC has at least one task; no orphan task.

## Pre-submit checks

| Check | Result |
|---|---|
| Every SPEC-001..012 maps to a task | YES (12/12) |
| Every task has `BLOCKED_BY` (`NONE` only for TASK-00) | YES |
| Every task has a verification method and trace links | YES |
| Every scope bullet in `plan.md` maps to a task | YES (8/8) |
| No frontend/backend implementation or unit-test task | YES (UI NO, backend NO) |
| No API task (`NO_API_CHANGE`) | YES |
| No database/migration task | YES |
| No new dependency | YES |
| `OPEN-038` carried as a precondition | YES (TASK-00) |
| No question asked | YES |
| No real PII, secret or production data | YES |
