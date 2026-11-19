# Claude Code instructions — Recovery Workbench AISDLC v2

This repository runs the SCBX AI-First SDLC Playbook for the Recovery Workbench. The shared workflow
rules are in `.github/copilot-instructions.md` and the project standards are in `AGENTS.md`.

@.github/copilot-instructions.md

## Claude Code runtime — the new AISDLC agents

The lifecycle agents are Claude Code subagents in `.claude/agents/`. They are **generated** from the
VS Code / Copilot sources in `.github/agents/*.agent.md`; edit the source, then run:

```bash
node .github/scripts/sync-claude-agents.mjs
```

Check that they are current:

```bash
node .github/scripts/sync-claude-agents.mjs --check
```

| Stage | Subagent | Display name |
|---|---|---|
| Context | `context-builder`, `context-updater` | Context Builder, Context Updater |
| Specification | `technical-specifier` | Technical Specifier |
| Planning | `implementation-planner` | Implementation Planner |
| Build | `implementation-builder` | Implementation Builder |
| Validation | `api-tester`, `functional-automation-test`, `qa-test-case-generator`, `figma-extractor` | API Tester, Functional Automation Test, QA Test Case Generator, Figma Extractor |
| Gates and close-out | `compliance-reviewer`, `technical-documenter`, `traceability-manager` | Compliance Reviewer, Technical Documenter, Traceability Manager |

The requirement commands are `.claude/commands/brd-builder.md`, `prd-builder.md`,
`backlog-builder.md`, plus the toolkit prompts `/intake-to-spec` and `/intake-to-implementation`.

The `agents` allowlist in a `.agent.md` source becomes explicit guidance in the subagent prompt.
Claude Code does not enforce a per-subagent allowlist; follow the guidance and do not widen it.

## Stage discipline

Every PDLC stage is started by a human. Invoke one lifecycle agent per stage, let it finish and report
`NEXT_STEP`, then stop. Do not start the next stage on your own, and do not chain stage agents. The
Technical Specifier, Implementation Planner and Technical Documenter invoke `compliance-reviewer` at
their gates; a Critical, High or Medium finding blocks the handoff until a human remediates and
re-reviews or explicitly accepts it. Preserve every `FAIL` status and keep all findings visible.

**No-question rule.** In an automated run (context, specify, plan), the agent does not ask the user a
question. It records an assumption in `output/<RUN_ID>/assumptions.md`, or an open item in
`docs/open-items.md`, and continues. Only a safety, credential or production-data issue stops the run.
This is a local build decision (`L-RCV-03`) and is repeated in `AGENTS.md` §10.

## Recovery Workbench: what is reused (read first)

- The repository is built from the **document set v14** (16 November 2026), not from the old
  `13 AI-First SDLC repository`. The canonical corpus is `requirement/legacy/`.
- Binding decisions are in `docs/decisions/decision-register.md`:
  - **D-RCV-35** ACE DB alignment: no inbound loads; ACE ingests source data; the Workbench reads
    `recovery.v_ace_*` views; 30 views; four extension tables; trackers leave scope.
  - **D-RCV-36** Temporal and Drools: Temporal runs the case lifecycle from Epic 3; Quartz/Spring
    Batch stay for Epic 1–2 jobs; rules are embedded Drools from versioned XLS packages; E1-029,
    TE-005 and E1-048 are retired.
  - **D-RCV-28** migration naming (`V<seq>__<story>_<name>.sql`), schema `recovery`, `${recoverySchema}`.
  - D-RCV-51/52 are the renumbered squad decisions; D-RCV-47 is superseded.
- 72 active Epic 1 stories, 43 Epic 2 stories. Ten stories are removed or retired; see
  `docs/retirements/story-retirement-register.md`.
- **Implemented and preserved:** `RWB-E1-042` (parameter catalog migration, INC-003) and
  `RWB-TE-001` (module boundary, INC-002). **Planned and preserved:** `RWB-E1-044` (INC-001) and
  `RWB-E1-043` (INC-008). The old 78 specs are archived in `output/_archive/epic1-specs-20261106/`.
- Read `AGENTS.md`, `docs/decisions/decision-register.md`, `docs/open-items.md`,
  `docs/increments/INDEX.md`, `docs/increments/epics/EPIC-001-foundation-1.md` and the story card
  (`docs/increments/INC-0NN-epic-1-<story>.md`).
- Work is pulled in Build Sequence v6 order: take the next item whose dependencies are done.
- `/backlog-builder push` loads the existing stories into Jira with their keys; it does not write new
  stories. `/intake-to-spec` plays the Requirement Intake Consolidator only when a source changes.

## Requirement flow (start from business input)

Source material goes unchanged into `requirement/legacy/`. Requirement artefacts are produced in this
order; each stops for human approval before the next:

0. `/context-builder` first: builds `.github/contexts/` from the corpus and the ACE codebase.
   Gate: context readiness (FDE).
1. `/brd-builder` reads the corpus and `docs/architecture/decisions/`, writes `docs/brds/<name>.md`.
   Gate: requirements approval (Product Owner).
2. `/prd-builder` reads the approved BRD, writes `docs/prds/<name>.md`. Gate: Product Owner, FDA.
3. `/context-updater` adds the business context from the approved BRD and PRD.
4. `/backlog-builder` reads the approved PRD, writes epics and stories to `docs/backlog/`, and after
   Product Owner approval creates them in Jira. Gate: backlog approval (Product Owner).
5. Per story: `/specify` → `/planner` → `/implement` → tests → review.

Never invent business facts. Anything not in a source goes to the document's open questions or the
run's assumptions. Jira, Confluence and GitLab are reached through the MCP servers in `.mcp.json`;
credentials live outside this repository, never in it or in chat.

## Codebase: ACE monorepo

Application code lives in `ace-monorepo/` (its own git repository; this repository ignores it).
AISDLC artefacts (`.github/`, `.claude/`, `docs/`, `requirement/`, `output/`) stay at this root.

- Before any code change read `ace-monorepo/AGENTS.md`, the `AGENTS.md` of the package you touch,
  and `ace-monorepo/docs/coding-standard.md`.
- Architecture decisions: `docs/architecture/decisions/` (ADR-001–012, API style exception).
- Do not change other ACE modules. Keep edits to shared files (`build.gradle.kts`,
  `application.yaml`, security config) minimal and listed in the plan. New dependencies need plan
  approval.
- Never run against a shared database: recovery Flyway `clean` is disabled; integration tests use
  Testcontainers PostgreSQL.

### Two repositories, one story

| Artefact | Repository |
|---|---|
| Module code, tests, migrations (`th.co.scb.ace.demo.recovery`, `frontend/src/modules/recovery/`, `db/modulemigration/recovery/`) | ACE (`ace-monorepo/`), MR into `develop-recovery`, then into `develop` in batches (D-RCV-50) |
| `.claude/`, `.github/`, `CLAUDE.md`, `AGENTS.md`, `docs/`, `requirement/`, `output/` | this workspace repository |

- Implementation Builder edits only the module's paths, plus shared files that the approved plan names
  explicitly. Never copy AISDLC files into `ace-monorepo/`.
- ACE branch: `feature/<JIRA-KEY>-<slug>` from `develop-recovery`, MR into `develop-recovery`
  (D-RCV-50). Commit message: `<JIRA-KEY>: <summary>`.
- Record the ACE branch, commit SHAs and MR link in `output/<RUN_ID>/implement/` so the traceability
  matrix can link story → spec → code across the two repositories.

## Current status (16 November 2026)

| Item | Status |
|---|---|
| Corpus conversion | 733 entries, 0 failures |
| Context | `CONTEXT-20261116` READY, 7 context files + manifest |
| Intake | BRD, canonical requirements, gap report, traceability regenerated |
| Increments | 72 Epic 1 cards + 43 Epic 2 rows; 10 retirements recorded |
| Specification | `RWB-E1-042` and `RWB-TE-001` re-specified; old 78 specs archived |
| Plan | `RWB-E1-042` and `RWB-TE-001` planned; existing plans preserved for `RWB-E1-044`/`E1-043` |
| Build | `RWB-E1-042` migration and `RWB-TE-001` boundary already built; other stories not built |
| Tests | Evidence from the two implemented stories preserved; new runs are green |

Commit, push or open MRs in either repository only when the user asks.
