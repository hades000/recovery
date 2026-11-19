# Recovery Workbench — AI-First SDLC repository v2

This is the **v2 working repository** for the Recovery Workbench document set v14 (16 November 2026).
It replaces the earlier `13 AI-First SDLC repository` as the agent-readable baseline. The old
repository is left untouched so its 78 Epic 1 specifications remain readable as history.

## 1. What changed in v2

| Change | Effect |
|---|---|
| **D-RCV-35 ACE DB alignment** | The Workbench loads no source data. ACE ingests every source; the recovery module reads 30 SELECT-only `recovery.v_ace_*` views. 20 copy/load tables leave the schema; four extension tables remain. |
| **D-RCV-36 Temporal and Drools** | Case workflows run on Temporal from Epic 3; Quartz and Spring Batch keep every Epic 1–2 job. Rules are embedded Drools from versioned XLS packages. `RWB-E1-029`, `RWB-TE-005` and `RWB-E1-048` are retired; `RWB-E1-070..073`, `RWB-E2-037..043` are new. |
| **New story set** | Epic 1 v7, Epic 2 v5. 72 active Epic 1 items (62 E1 + 10 TE) and 43 Epic 2 items. Ten stories are removed or retired. |
| **Schema** | `recovery`, referenced only as `${recoverySchema}`. D-RCV-47 (schema `ace`, `rwb_` prefix) is superseded. |
| **New Claude agents** | `.claude/agents/` holds the generated Claude Code subagents from the toolkit: Context Builder/Updater, Technical Specifier, Implementation Planner, Implementation Builder, API Tester, Functional Automation Test, QA Test Case Generator, Figma Extractor, Compliance Reviewer, Technical Documenter, Traceability Manager. `.claude/commands/` holds the requirement commands. |
| **Preserved implementation** | `RWB-E1-042` (parameter catalog migration) and `RWB-TE-001` (module boundary) are preserved and re-specified/re-planned against the new baseline. `RWB-E1-044` and `RWB-E1-043` plans are preserved as historical. |

## 2. Structure

```text
17 AI-First SDLC Repository v2/
├── .claude/
│   ├── agents/           generated Claude Code subagents
│   └── commands/         brd-builder, prd-builder, backlog-builder, intake prompts
├── .github/
│   ├── agents/           canonical VS Code/Copilot agent sources
│   ├── contexts/         7 context files + manifest (CONTEXT-20261116)
│   ├── rules/ prompts/ templates/ scripts/ instructions/
├── .vscode/mcp.json
├── .mcp.json
├── AGENTS.md             engineering standards (v2)
├── CLAUDE.md             Claude Code runtime and stage discipline
├── docs/
│   ├── increments/       72 story cards, 2 epic cards, build sequence
│   ├── discovery/        project, architecture, journeys, glossary, measures
│   ├── brds/             Lean BRDs and business requirements
│   ├── prds/             FSD v6, NFR v3, Epics 3–8, ACE team stories
│   ├── architecture/     ADR-001–012 and the API style exception
│   ├── decisions/        decision register, squad decisions, two change registers
│   ├── retirements/      10 removed/retired stories
│   └── open-items.md
├── requirement/
│   ├── legacy/           converted document set v14 (733 entries, 0 failures)
│   ├── Context_RecoveryWorkbench.md
│   ├── BRD_RecoveryWorkbench.md
│   ├── RecoveryWorkbench_Requirements.md
│   ├── Intake_Gap_Report_RecoveryWorkbench.md
│   └── Traceability_Matrix.md
├── output/
│   ├── CONTEXT-20261116/              context run log and assumptions
│   ├── INC-001-epic-1-RWB-E1-044/     preserved historical spec/plan
│   ├── INC-002-epic-1-RWB-TE-001/     preserved spec/plan/implementation
│   ├── INC-003-epic-1-RWB-E1-042/     current spec/plan/implementation
│   ├── INC-008-epic-1-RWB-E1-043/     preserved historical spec/plan
│   ├── _archive/epic1-specs-20261106/ old 78 specs (history only)
│   └── EPIC1-STORY-MANIFEST.json/.md
└── tools/                              converter, builders, verifier
```

## 3. Status

| Item | Status |
|---|---|
| Corpus conversion | 733 entries, 0 failures |
| Context | `CONTEXT-20261116` READY; 7 context files + manifest |
| Intake | BRD v2, canonical requirements v2, gap report, traceability |
| Increments | 72 Epic 1 cards + 43 Epic 2 rows; 10 retirements |
| Specify | `RWB-E1-042` and `RWB-TE-001` current; old 78 archived |
| Plan | `RWB-E1-042` and `RWB-TE-001` current; `RWB-E1-044`/`E1-043` historical |
| Build | `RWB-E1-042` migration and `RWB-TE-001` boundary built; other stories not built |
| Verification | `python tools/verify_repo_v2.py` → PASS |

## 4. How to use it

1. Read `AGENTS.md`, `CLAUDE.md`, `docs/decisions/decision-register.md`,
   `docs/increments/INDEX.md` and the story card.
2. Start a stage with the matching Claude subagent (`.claude/agents/`), or the command in
   `.claude/commands/`.
3. One stage per invocation. The agent stops with `NEXT_STEP`; the human starts the next stage.
4. No question is asked in an automated context/specify/plan run. Assumptions go to the run's
   `assumptions.md`; open items go to `docs/open-items.md`.
5. Before code, read `.github/contexts/backend-context.md`/`frontend-context.md` and the relevant
   standard. Code goes to the ACE monorepo, not this repository.
6. Run `node .github/scripts/sync-claude-agents.mjs --check` after editing an `.agent.md`.
7. Run `python tools/verify_repo_v2.py` after changing the package.

## 5. Canonical sources

- `requirement/legacy/` is the converted document set; the original files stay in the twelve source
  folders and the 14/15/16/E1-042 folders.
- `requirement/legacy/DOCUMENT_MAP.md` maps every source file.
- The current set is Epic 1 story files v7, Epic 2 v5, Physical Schema v6, API Specification v4,
  ADR v3, Decision Log v10, Build Sequence v6.
- `docs/decisions/decision-register.md` is the one decision index. D-RCV-35/36 are client decisions;
  D-RCV-51/52 are the renumbered squad decisions; D-RCV-47 is superseded.

## 6. Known limits

- No live Figma; design evidence is the screen inventory and specifications.
- Thai labels and messages are draft (DL10).
- Per-story Jira keys and approver comments are incomplete.
- ACE source code is in a separate repository; implementation evidence is linked, not embedded.
- Temporal and Drools versions are pinned at build.
- The 10 removed/retired stories are not built; their old specs are history.

## 7. Toolkit reference

The agents, rules, prompts, templates and MCP servers come from `../aisdlc-toolkit-main/repo-template`
(16 November 2026). The lifecycle and gates come from `../aisdlc-playbook-main/docs`.
