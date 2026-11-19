# V2 rebuild report — Recovery Workbench AISDLC repository

**Built:** 16 November 2026
**From:** Recovery Workbench document set v14 (01–12, 14, 15, 16, E1-042 pack, ACE schema)
**To:** `17 AI-First SDLC Repository v2`
**Reference implementation:** `C:\Users\SahilMore\Downloads\recovery\recovery`
**Status:** Complete; verification PASS

## 1. What was asked

Build a new version of the AISDLC repository from the updated document set, keep the story work that
has already been implemented, use the new AISDLC Claude agents, run the context agents for proper
context, then run specify and planner — without asking any questions in those phases.

## 2. What was built

| Deliverable | Result |
|---|---|
| New repository | `17 AI-First SDLC Repository v2` beside the old `13 AI-First SDLC repository`; the old repository is untouched |
| Toolkit scaffold | `.github/` from the 16 Nov toolkit: 12 agents, rules, prompts, templates, scripts, instructions |
| New Claude agents | `.claude/agents/` with 12 generated subagents (Context Builder/Updater, Technical Specifier, Implementation Planner, Implementation Builder, API Tester, Functional Automation Test, QA Test Case Generator, Figma Extractor, Compliance Reviewer, Technical Documenter, Traceability Manager); `.claude/commands/` with brd-builder, prd-builder, backlog-builder and the intake prompts |
| Corpus | `requirement/legacy/` converted from the new set: 733 entries, 0 failures; 01–12 plus the 14/15/16 change packs, E1-042 pack and ACE schema |
| Context | `CONTEXT-20261116`: 7 context files + manifest + run log + 15 assumptions; feature catalogue 20/20 mapped |
| Requirements | BRD v2, canonical requirements v2, intake gap report, traceability matrix (72 story rows) |
| Decisions | One decision register; D-RCV-35/36 applied; old D-RCV-35/36 renumbered to 51/52; D-RCV-47 superseded |
| Increments | 72 Epic 1 cards + 43 Epic 2 rows + 2 epic cards + retirements |
| Specify | `RWB-E1-042` (INC-003) and `RWB-TE-001` (INC-002) current; old 78 specs archived |
| Plan | `RWB-E1-042` and `RWB-TE-001` current (19 and 22 tasks); `RWB-E1-044`/`E1-043` historical |
| Preserved implementation | E1-042 migration pack + tests + evidence; TE-001 module boundary + coverage + logs; E1-044/E1-043 specs and plans |
| Verification | `python tools/verify_repo_v2.py` → PASS |

## 3. What changed from the old repository

| Area | Old `13` repo | New `17` repo |
|---|---|---|
| Baseline | ~4–6 Nov 2026, 78 Epic 1 stories | 16 Nov 2026, 72 Epic 1 stories + 43 Epic 2 |
| Source loads | ALS/EFS/CCMS/SVAF loads, Excel/SharePoint trackers | Removed; ACE ingests, Workbench reads 30 views |
| Workflow | No workflow engine (ADR-003) | Temporal from Epic 3 (ADR-011); Quartz/Spring Batch for E1–E2 |
| Rules | Home-built decision tables (ADR-004) | Embedded Drools from versioned XLS packages (ADR-012) |
| Schema | `recovery` + `${recoverySchema}` in the old docs; squad detour to `ace`/`rwb_` | `recovery` + `${recoverySchema}`, D-RCV-47 superseded |
| Stories | 78 | 72 active; 10 removed/retired; 5 new E1, 7 new E2 |
| Agents | `.github/agents` only; `.claude/commands` | `.claude/agents` generated + commands; `sync-claude-agents.mjs --check` |
| Context | 145 CTX IDs, 4 Nov | 7 context files, new decision set, 20 features |
| Specs | 78 specs current | 2 current, 78 archived; E1-042/E1-044/E1-043 preserved |
| Plans | E1-044, TE-001, E1-043 | E1-042 and TE-001 current; E1-044/E1-043 historical |
| Questions | `questions.md` open | No-question rule; assumptions register |

## 4. Preserved implemented work

| Story | Evidence | New home | Status |
|---|---|---|---|
| `RWB-E1-042` | SQL, CSV, tests, migration output | `output/INC-003-epic-1-RWB-E1-042/implement/` | Implemented; spec/plan rebaselined |
| `RWB-TE-001` | Build logs, JaCoCo, Vitest, test results | `output/INC-002-epic-1-RWB-TE-001/implement/` | Implemented; BND-6 added in the plan |
| `RWB-E1-044` | Spec, plan, contracts, reviews | `output/INC-001-epic-1-RWB-E1-044/` | Planned; historical, re-baseline before build |
| `RWB-E1-043` | Spec, plan, contracts, reviews | `output/INC-008-epic-1-RWB-E1-043/` | Planned; historical, re-baseline before build |

## 5. Context agents run

- **Context Builder** created the seven context roles from the new corpus and the implemented code.
- **Context Updater** applied D-RCV-35 (ACE DB), D-RCV-36 (Temporal/Drools), the schema reversal, the
  72/43 story counts, the new stories and the retirement set.
- Run log: `output/CONTEXT-20261116/agent-run-log.md`.
- Assumptions: `output/CONTEXT-20261116/assumptions.md` (15 rows).
- Status: `READY`; `FEATURE_COVERAGE: 20 discovered / 20 documented / 0 unresolved`.

## 6. Specify and planner runs

| Run | Spec | Plan | Tasks | Outcome |
|---|---|---|---|---|
| `INC-003` `RWB-E1-042` | `specify/spec.md` (SPEC-001..012) | `plan/plan.md` | 18 | SUCCESS; plan gate pending human |
| `INC-002` `RWB-TE-001` | `specify/spec.md` (SPEC-001..021) | `plan/plan.md` | 21 | SUCCESS; plan gate pending human |

Both specs pass compliance (0 Critical/High/Medium) and both plans map every SPEC to a task. The
preserved implementation is the baseline; the new plans add only what the v2 baseline requires
(six parameters for E1-042, BND-6 for TE-001).

## 7. No-question handling

- `L-RCV-03` and `AGENTS.md` §10: an automated stage does not ask the user a question.
- Every ambiguity is in `output/CONTEXT-20261116/assumptions.md` or the run's `assumptions.md`.
- The specify/plan run logs record `No questions` and `CLARIFICATION_STATUS: RESOLVED [OPEN_ITEMS: 0]`.
- Open items are in `docs/open-items.md` with an owner; none blocks E1-042/TE-001.

## 8. Verification

```text
python tools/verify_repo_v2.py
Checked 17 AI-First SDLC Repository v2
Story cards: 72; traceability rows: 72; contexts: 7
PASS: structure, agents, contexts, stories, decisions, retirements, runs and evidence
```

Additional checks:

- `node .github/scripts/sync-claude-agents.mjs --check` → Claude Code files are up to date.
- `requirement/legacy/_conversion-report.md` → 733 entries, 0 failures.
- `output/INC-003.../implement/evidence/migration-test-output.txt` → migration test green.
- `output/INC-002.../implement/report.md` → TE-001 implementation green.

## 9. Open items

See `docs/open-items.md`. The four that matter to the next stage:

| ID | Item | Owner |
|---|---|---|
| `OPEN-005` | Thai labels and messages are draft | BA / DL10 |
| `OPEN-016` | Per-story approver names | Product Owner |
| `OPEN-032` | AMIS/RPS/LIT/WIN/GL/COLLINS ACE ingestion assumption | ACE team lead |
| `OPEN-034` | Temporal version and 30-day retention | SCB IT / Compliance |
| `OPEN-036` | Re-baseline E1-044/E1-043 specs and plans | Specifier / Planner |

## 10. How to continue

1. Review the context package and the two current specs/plans.
2. Approve the plan and task for `RWB-E1-042` and `RWB-TE-001`.
3. Start the Implementation Builder for the BND-6 addendum and the six parameters.
4. Pull the next item in Build Sequence v6 order whose dependencies are done (`RWB-E1-044` is next,
   after its re-baseline).
5. Do not rebuild the removed/retired stories; use `docs/retirements/story-retirement-register.md`.
