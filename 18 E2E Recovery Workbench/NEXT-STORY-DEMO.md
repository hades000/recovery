# Next story demo: RWB-E1-043 Reference data service with versioned tables

This is a run-book for building the next story, Build Sequence v6 order 8, live through the AISDLC playbook.
It is written so a presenter can run it in Claude Code and stop at each human checkpoint.

## 1. Can it be built now?

**Yes, after a plan refresh.** Checked on 18 Nov 23:57 by a read-only agent against `develop-recovery` at
`27567ed` (log row "RWB-E1-043 Readiness check").

| Check | Result |
|---|---|
| Spec | PASS at spec gate round 10 (`aisdlc/output/INC-008-epic-1-RWB-E1-043/review/spec-gate-review-10.md`) |
| Plan | PASS at plan gate round 2 (`review/plan-gate-review-2.md`, `PLAN_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]`), 20 tasks |
| Dependencies | RWB-E1-044 (`b1d7424`), RWB-TE-001 (`dc2d25b`) and RWB-E1-042 (`0b87102`) are merged |
| Document gaps marked Blocker = Yes for this story | None. DG-004 and DG-005 belong to RWB-E1-001; DG-006 and DG-007 belong to RWB-TE-002 |
| Open decisions it relies on | D-RUN-10, D-RUN-11, D-RUN-18 to D-RUN-21 are orchestrator decisions not yet ratified (OPEN-050, OPEN-055). They let the build go ahead; the tech lead should ratify them at the plan checkpoint |

### Why the plan needs a refresh first (drift D1 to D6)

The plan passed its gate at 10:54 on 18 Nov, before RWB-TE-001 and RWB-E1-042 merged. The code has since
moved under it:

| ID | Drift | What the refresh must change |
|---|---|---|
| D1 | PRE-2 and PRE-4 expect only a README in `backend/src/main/resources/db/modulemigration/recovery/`, but `V0001` (RWB-E1-042) is there now | Expect V0001; this story's migration becomes the next free number (V0002) at merge (D-RUN-07) |
| D2 | The plan's path for `ApplicationYamlEnvironment` is out of date; the class is in the test-support package | Use the real path |
| D3 | `ParameterMigrationIT` asserts exactly 19 catalog rows | This story adds 38 catalog rows (spec SPEC-029). Update that count in the same commit, with a reason |
| D4 | The magic-number baseline file changed in RWB-E1-042, and `ApiExceptionHandler` (lines 50 to 51) already uses the literal `"none"` | Re-check the plan's literals against both |
| D5 | `casewf/refdata` has no `@ApplicationModule` or named-interface entry yet; the RWB-TE-001 boundary rules need one (deviation DEV-04 pattern, `ModuleMapLoaderTest#loadsTheRealMap`) | Add the package and the module-map entry as tasks |
| D6 | RWB-TE-001 set the convention for must-fail boundary fixtures (`th.co.scb.ace.boundaryfixture`) | Follow it for any new boundary fixture |

Two more inputs come from the post-merge review. The refresh should take them into account:

- REVIEW-001 M2 is registered to this story. Four numeric catalog parameters have no bounds, and V0002 should add them.
- REVIEW-001 CONF-E044-06: the migration lint rejects files over 256 KB, which matters only for RWB-E1-001.

### Gaps that block SIT, not the build

| Gap | What is missing | Effect |
|---|---|---|
| GAP-43 (E1-043 spec) | The story's "done" needs 12 tables approved before SIT exit. Their content comes from later stories, and PRODUCT, REGION and EXPOSURE_BAND have no named owner | Built and tested with synthetic loads; content approval is the client's |
| GAP-14 / GAP-46 (E1-043 spec), DG-027 | No role holds Reference data A (approve), and the data steward holds only U or RU | Interim grants file; RWB-E1-037 replaces it |
| GAP-06 (E1-043 spec), DG-029 | No message table | Messages go through the `MessageResolver` seam from RWB-E1-042 |
| PG-E1-043-04 (plan) | `parameter_catalog.description` is NOT NULL (at most 400 characters), and no source gives text for the 38 rows this story adds | Plain descriptions are written from the key names and recorded as an assumption, as RWB-E1-042 did (PA-E1-042-06). Blocker No |

When the stages are rerun they will raise any new gap in their `document-gaps.md`. The orchestrator then adds
it to `aisdlc/DOCUMENT-GAPS.md` with Blocker Yes or No. The document set is never edited.

## 2. Before the demo (about 15 minutes)

1. Open this folder in Claude Code. Check that the agents are current:
   `node aisdlc/.github/scripts/sync-claude-agents.mjs --check`
2. Start the local stack and make sure the baseline is green:
   ```powershell
   $env:JAVA_TOOL_OPTIONS="-Djdk.net.unixdomain.tmpdir=$env:USERPROFILE\.gradle\uds"
   ./scripts/dev.ps1 up
   ./scripts/dev.ps1 test
   ```
   `.env` must have `RWB_LOAD_REFERENCE_SCHEMA=true` until RWB-E1-001 is built. It must also have
   `RWB_ENVIRONMENT=DEV`, which is required after REVIEW-001 H2.
3. Create the story branch in its own worktree:
   `git worktree add ..\rwb-wt\RWB-E1-043 -b feature/RWB-E1-043-reference-data develop-recovery`
4. Log the start: `aisdlc/tools/log-row.ps1 -Story RWB-E1-043 -Stage 'Plan refresh' -Actor implementation-planner -Group P2 -Outcome STARTED -Note '...'`

## 3. The run, stage by stage

Each stage is one prompt. After each one, the presenter shows the output file and the gate line, then
records the human checkpoint. That record is what OPEN-054 asks for. The approver writes it themselves; the AI
does not.

| # | Stage and agent | Prompt to type in Claude Code (model Opus 5.5) | Output to show | Time |
|---|---|---|---|---|
| 1 | Plan refresh: implementation-planner (high) | "Use the implementation-planner agent. RUN_ID INC-008-epic-1-RWB-E1-043, workspace `aisdlc`, code repo `../rwb-wt/RWB-E1-043`. Read RUN-BRIEF.md. Refresh plan v1 to v2 against `develop-recovery` at its current tip: fix drift D1 to D6 and REVIEW-001 M2 as listed in NEXT-STORY-DEMO.md section 1. Back up the current files as `*.run2.*`. Then run the plan gate." | `plan/plan.md` v2, `review/plan-gate-review-3.md`, `PLAN_GATE:` line | 45 to 60 min |
| 1a | Human checkpoint: Plan approved (AGENTS.md §9) | The tech lead reads the plan and records the approval, or the changes needed, in the log or on the merge request | Log row by the tech lead | 10 min |
| 2 | Build: implementation-builder (high) | "Use the implementation-builder agent for RUN_ID INC-008-epic-1-RWB-E1-043 in worktree `../rwb-wt/RWB-E1-043`. Follow plan v2 task by task: a red commit, then a green commit, per task. Testcontainers only; do not run `dev.ps1 up`. Coverage at least 80% on all four counters. Commit trailers as in AGENTS.md." | `git log --oneline`, `implement/` red and green logs, coverage report | 3 to 4 h |
| 3 | Pre-merge review | "Run /ponytail-review and /security-review on `git diff develop-recovery...feature/RWB-E1-043-reference-data`; write them to `review/`." Send the findings back to the builder and repeat until both are clean | `review/ponytail-review.md`, `review/security-review.md` | 45 min |
| 4 | API test: api-tester (medium), and functional test: functional-automation-test (medium), in parallel | "Use the api-tester agent for RUN_ID INC-008… against the worktree" / "Use the functional-automation-test agent …" | `api-tests/report.md` (the story adds `POST /admin/reference-loads`, so the API tests apply), `functional-tests/report.md` | 45 min |
| 5 | Code gate and documentation: technical-documenter (gate high, docs medium) | "Use the technical-documenter agent for RUN_ID INC-008…. Run the Compliance Reviewer code gate first; on PASS write `docs/`." | `review/code-gate-review.md`, `CODE_GATE:` line, `docs/` | 45 min |
| 5a | Human checkpoint: merge approval | A named reviewer approves the merge | Log row by the reviewer | 10 min |
| 6 | Merge (orchestrator) | `git merge --no-ff`, rename the migration to `V0002__…`, then run `dev.ps1 test`, `it` and `e2e` on `develop-recovery` | Merge SHA, three green suites | 30 min |
| 7 | Traceability: traceability-manager (medium) | "Use the traceability-manager agent to update row 008 of `aisdlc/requirement/Traceability_Matrix.md` from spec to code to tests." | Matrix row 008 | 15 min |

**Total:** about 6 to 9 hours of agent time. For a live session, show stages 1 and 1a live. Let stage 2 run in
the background, and come back for 3 to 7. A gate FAIL is a normal part of the demo: the agent fixes the finding
and re-runs the gate (D-RUN-09). It never "accepts" a finding.

## 4. What to point out during the demo

- **Separate gates.** Each gate is a separate Compliance Reviewer run with its own file and a machine-readable
  gate line.
- **Tests first.** Every task has a red commit before its green commit (`git log`, `implement/*red*.log`).
- **Questions do not stop the build.** Agents do not ask questions. Unknowns become assumptions, open items or
  document gaps.
- **Traceable commits.** Every commit carries `AISDLC-Run`, `AISDLC-Stage` and `AISDLC-Plan` trailers.
- **The document set is not touched.** The re-hash in `aisdlc/evidence/docset-integrity.md` shows it.

## 5. Scheduling note

RWB-TE-003 (order 5) has a passed spec but no plan. Build Sequence v6 pulls it before RWB-E1-043, but
RWB-E1-043 does not depend on it. Building RWB-E1-043 first is allowed by the "Depends on" column, and should
be recorded as a decision row when the demo starts.
