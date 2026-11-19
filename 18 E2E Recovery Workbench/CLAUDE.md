# Claude Code instructions: Recovery Workbench (recovery module of ACE)

This repository was built with the **SCBX AI-First SDLC (AISDLC) playbook**. Every story went through
the playbook's lifecycle agents and gates, and each step left evidence in this repository. Read this
file before you answer any question about how something was built. The narrative is in
`HOW-THIS-WAS-BUILT.md`; which tool and model ran each period is in decision D-RUN-26 of the build log.

@AGENTS.md

## Where the evidence is

| Question | Where to look |
|---|---|
| What was built, in what order, how long it took, and which decisions were made | `AI-SDLC-BUILD-LOG.md` |
| The story as given (increment card, ACs, dependencies) | `aisdlc/docs/increments/INC-0NN-epic-1-<story>.md` |
| The specification, plan, reviews and test reports for a story | `aisdlc/output/<RUN_ID>/` (start with its `README.md`) |
| The spec, plan and code gate reviews (Compliance Reviewer) | `aisdlc/output/<RUN_ID>/review/` and `specify/compliance-validation.md` |
| Where the document set is missing something or contradicts itself, and whether it blocked a story | `aisdlc/DOCUMENT-GAPS.md` |
| The source documents consulted, with a SHA-256 for each | `aisdlc/SOURCES.md` |
| Requirement to spec to code to test traceability | `aisdlc/requirement/Traceability_Matrix.md` |
| Open items raised by the agents | `aisdlc/docs/open-items.md` |
| The code for a story | `git log --grep "<STORY-KEY>"`; story-branch commits carry `AISDLC-Run`, `AISDLC-Stage` and `AISDLC-Plan` trailers (four early checkpoint commits do not parse; see the log correction of 19 Nov 00:11) |
| Proof that the document set was not changed | `aisdlc/evidence/document-set-baseline.sha256` (start), `document-set-final.sha256` (end) and `docset-integrity.md` (result) |
| The post-merge review of the four built stories and its fixes | `aisdlc/output/REVIEW-001-first-four-stories/` |
| How to run the next story (RWB-E1-043) as a demonstration | `NEXT-STORY-DEMO.md` |

The commit `Platform baseline (pre-pipeline setup)` is environment provisioning: the local stack and
module skeleton that existed before the story pipeline started. It is not a story.

## The lifecycle (one agent per stage; the orchestrator starts each stage)

```
Technical Specifier ─(Compliance Reviewer: spec gate)─▶ Implementation Planner ─(plan gate)─▶
Implementation Builder ─▶ API Tester ∥ Functional Automation Test ─▶
Technical Documenter ─(code gate)─▶ Traceability Manager
```

- Agents live in `.claude/agents/`. They are generated from `aisdlc/.github/agents/*.agent.md` by
  `node aisdlc/.github/scripts/sync-claude-agents.mjs` (`--check` verifies they are current).
- The AISDLC workspace root is `aisdlc/`. Every relative path an agent uses (`.github/contexts/`,
  `.github/rules/`, `docs/increments/`, `output/<RUN_ID>/`) resolves there.
- The code repository (the "ACE monorepo" in the agent prompts) is this repository's root.
- The converted source corpus (`requirement/legacy/`) is not copied here. It is in the document set
  folder `17 AI-First SDLC Repository v2/requirement/legacy/`. Artefacts cite sources by document
  name and version.
- Any gate finding, Low included, is fixed and re-reviewed before the next stage (D-RUN-09); none is
  "accepted" by an agent. Spec, plan and code gate rounds are kept as separate files (`*-review.md`,
  `*-review-2.md`, ...), except where a run README says rounds were appended to one file (RWB-E1-044
  code gate; the pre-merge ponytail and security reviews of every story).
- Files named `*.runN.*` are the copy of an artefact as it stood before remediation run N. They are kept
  so a reviewer can diff what each gate round changed.
- A human approval (AGENTS.md §9: plan approved, merge) is recorded only by that human. None is recorded
  for the four built stories yet (OPEN-054).
- Agents never ask questions in an automated stage. They record assumptions in the run's
  `assumptions.md` and propose open items in the run's `shared-updates.md`. Only the orchestrator writes
  the shared registers (`aisdlc/docs/open-items.md`, `DOCUMENT-GAPS.md`, `Traceability_Matrix.md`,
  `INDEX.md`) (L-RCV-03).

## Running the code

```powershell
./scripts/dev.ps1 up        # Postgres, Temporal, Azurite, mock Entra ID
./scripts/dev.ps1 backend   # Spring Boot on :8080
./scripts/dev.ps1 frontend  # Vite on :5173
./scripts/dev.ps1 test      # unit tests, boundary tests, frontend typecheck/lint/coverage
./scripts/dev.ps1 it        # Testcontainers integration tests
./scripts/dev.ps1 e2e       # API and browser e2e against the running stack
```

See `README.md` for the stack and the local stand-ins for bank services.

## Rules for any further change

- One story per branch: `feature/<KEY>-<slug>` from `develop-recovery`, with commit messages
  `<KEY>: <summary>`.
- A migration is `V<seq>__<story>_<name>.sql`, line 1 is `-- Story: <key>`, and a merged migration is never edited.
- Tests come before code. Never skip or weaken a test.
- Never put personal data in code, tests or logs.
