# How this was built

The Recovery Workbench recovery module in this repository was built with the **SCBX AI-First SDLC (AISDLC)
playbook**. The first four stories of Build Sequence v6 went through it: RWB-E1-044, RWB-TE-001, RWB-E1-042
and RWB-TE-002. Each one passed through the playbook's lifecycle agents and gates, and each step left a file
in this repository. This document explains the process, points to the evidence, and is open about what did not
go to plan.

## 1. The process

The playbook is the AISDLC v2 workspace from the document set (`17 AI-First SDLC Repository v2`). It is
installed here under `aisdlc/`, and its agent definitions are generated into `.claude/agents/`. Every story went
through the same chain of agents:

```
Technical Specifier ──spec gate──▶ Implementation Planner ──plan gate──▶ Implementation Builder
   ──▶ pre-merge ponytail and security review ──▶ API Tester ∥ Functional Automation Test
   ──▶ Technical Documenter (code gate first, then docs) ──▶ merge ──▶ Traceability
```

| Agent | What it produced for each story | Where |
|---|---|---|
| Technical Specifier | Specification with numbered SPEC items, field-level behaviour, ACs, assumptions, gaps | `aisdlc/output/<RUN_ID>/specify/` |
| Compliance Reviewer | Spec gate, plan gate and code gate reviews, each ending in a machine-readable line such as `CODE_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]` | `aisdlc/output/<RUN_ID>/review/` |
| Implementation Planner | Plan, tasks, data model, contracts, test scenarios, each file named by its exact repository path | `aisdlc/output/<RUN_ID>/plan/` |
| Implementation Builder | Code on a `feature/<KEY>-<slug>` branch, a red test commit before each green commit, coverage at or above 80% | git history; `implement/` |
| API Tester, Functional Automation Test | API contract tests, or a documented N/A with the card line quoted | `api-tests/`, `functional-tests/` |
| Technical Documenter | Runs the code gate first, then writes README, ARCHITECTURE and COMPLIANCE docs | `review/code-gate-review*.md`, `docs/` |
| Orchestrator | Starts each stage, triages each gate result, writes the shared registers, merges in build order | `AI-SDLC-BUILD-LOG.md` |

**Rules that held for the whole run:**

- **Any gate finding, a Low included, is fixed and re-gated (D-RUN-09).** No agent "accepts" a finding.
  The four stories took 29 spec gate rounds, 12 plan gate rounds and 10 code gate rounds before every gate read
  0/0/0/0.
- **Agents never stop to ask.** Unknowns become a recorded assumption, an open item
  (`aisdlc/docs/open-items.md`) or a document gap (`aisdlc/DOCUMENT-GAPS.md`, with Blocker Yes or No).
- **The document set is read only.** It was hashed before the first stage and again at the end. No document
  changed (`aisdlc/evidence/docset-integrity.md`).
- **Every timed event is a row in the build log.** Mistakes are corrected by new "Log correction" rows. Old
  rows were edited once, on 19 Nov, when the repository owner asked for some notes to be shortened; the
  log header says so, and the earlier text is in git history.

## 2. What was delivered

| Story | What it does | Gate rounds (spec / plan / code) | Merge |
|---|---|---|---|
| RWB-E1-044 | Flyway migrations for the `recovery` schema with a parameterised schema name, a migration lint, and least-privilege migrator rights | 7 / 2 / 2 | `b1d7424` |
| RWB-TE-001 | The 19 design modules inside the recovery module, with boundary tests (ArchUnit, Spring Modulith, ESLint), each with a fixture that must fail | 5 / 7 / 2 | `dc2d25b` |
| RWB-E1-042 | Central parameter catalog and service: versioned values, maker-checker approval, rollback, cache, migration `V0001` | 12 / 2 / 4 | `0b87102` |
| RWB-TE-002 | Code owners for the recovery module, with a validator and a register of owner groups | 5 / 1 / 2 | `27567ed` |

After the last merge, `scripts/dev.ps1 test`, `it` and `e2e` were green on `develop-recovery`. Test counts and
coverage per story are in section 3 of `AI-SDLC-BUILD-LOG.md`. Orders 5 to 10 were specified, and three were
planned, but they were not built: the engagement lead stopped the run after four stories (D-RUN-27).

## 3. Tools and models: what ran when

Being exact here matters more than a tidy story. Decision D-RUN-26 in the build log has the full record.

| Period | Tool and model | What it did |
|---|---|---|
| 17 Nov 23:02 to 18 Nov about 07:15 | Claude Code, Claude Opus 5.5 agents | All specifications and spec gates; RWB-TE-001 plan and plan gates; the first RWB-TE-001 build commit |
| 18 Nov 07:19 to 18:57 | **opencode, DeepSeek v4.1 Flash**, using the same agent definitions | RWB-TE-001 and RWB-E1-044 build, reviews, code gates, tests, docs and merges; RWB-E1-042 build and first code gate; several plans and plan gates |
| 18 Nov 19:26 to 19 Nov | Claude Code, Opus 5.5 agents | RWB-E1-042 code gate rounds 2 to 4 and merge; RWB-TE-002 build, reviews, gates and merge; the post-merge review |

The commits written during the opencode period carry Claude trailers, which is wrong. Git history was not
rewritten. Instead:

- the log lists the affected commits (log correction rows of 19 Nov 00:02 and 00:11);
- the run READMEs of RWB-E1-044 and RWB-TE-001 have a Provenance section;
- AGENTS.md section 4, rule 12 now forbids naming the wrong tool or model;
- **independent Claude Opus 5.5 confirmation code gates** were run on the two stories built in opencode
  (`review/code-gate-review-confirmation.md` in INC-001 and INC-002). They found real issues, and those issues were
  fixed through the playbook and merged (section 4).

Approval of opencode as a tool, and of sending document-set content to its model provider, is open item
OPEN-053.

## 4. Review after the merges (REVIEW-001)

Before hand-over, the merged code was reviewed as a whole, not one story diff at a time. Everything is in
`aisdlc/output/REVIEW-001-first-four-stories/`.

| Review | Result | Disposition |
|---|---|---|
| Whole-codebase code-quality review (Opus 5.5, high) | 0 Critical, 4 High, 11 Medium, 11 Low | 15 fixed on a REVIEW-001 branch with tests first; 11 registered with an owner (OPEN-056). See `plan.md` |
| Evidence audit, written as a sceptical bank reviewer would read it | 10 High, 14 Medium, 9 Low evidence findings | Corrected in the log, READMEs, registers and CLAUDE.md. Human approvals cannot be written by the AI, so they stay open (OPEN-054) |
| Confirmation code gate, RWB-E1-044 | FAIL 0/0/3/6 (migration lint: two checks without a discriminating test, one position not detected, one check weaker than the inherited rule) | Fixed, then four more rounds; round 5 PASS 0/0/0/0; merged `3297584` |
| Confirmation code gate, RWB-TE-001 | FAIL 0/0/0/2 | Fixed; round 3 PASS 0/0/0/0; merged with the REVIEW-001 fixes |

The REVIEW-001 fixes went through the same chain: a builder, code gates (three rounds, the last PASS
0/0/0/0), a merge (`9c05371`), and the three suites. After the merge, `test` (447 backend tests), `it` (62)
and `e2e` (6 API tests and 3 Playwright tests) were green. `REVIEW-001-first-four-stories/README.md` gives
the final state of every finding.

**The four High code findings, in plain terms:**

1. Two different parameter loads for the same key could be approved at the same moment.
2. A missing environment setting defaulted silently to DEV.
3. The 80% coverage check was not run in CI.
4. Some sensitive paths had no code owner.

Each one is fixed with a failing test first, where a test can show the defect.

## 5. Where to look

| You want to check… | Open |
|---|---|
| The order of events, with times, and every decision | `AI-SDLC-BUILD-LOG.md` (sections 1 to 4) |
| One story from spec to merge | `aisdlc/output/<RUN_ID>/README.md` |
| Every gate result | `aisdlc/output/*/review/*-gate-review*.md`, final line of each |
| Requirement to test traceability | `aisdlc/requirement/Traceability_Matrix.md` |
| What the document set is missing | `aisdlc/DOCUMENT-GAPS.md` (DG-001 to DG-046, blockers first) |
| What still needs a human | `aisdlc/docs/open-items.md` |
| Rules the agents follow, and AI errors already found | `AGENTS.md` (section 11 lists the known AI errors) |
| How to build the next story | `NEXT-STORY-DEMO.md` |

## 6. What we would improve in the agents (small changes, same playbook)

These changes keep the playbook's stages and gates as they are. Each comes from something that cost time in
this run.

1. **Let subagents write their own report file.** Several agents returned their review as text, and the
   orchestrator had to save it. A write permission scoped to `output/<RUN_ID>/` removes that step and the
   "provenance: saved by the orchestrator" notes.
2. **Stop Low-only churn.** Some spec gates went 10 or more rounds, each finding Lows in text added the round
   before. The reviewer brief should say: after two Low-only rounds, the fix is to simplify (remove cases,
   fail closed), not to add text.
3. **Freeze an upstream spec once a dependent plan passes.** RWB-E1-042's spec kept changing while plans that
   cite it were being gated. A "frozen at revision N" line in the spec header would prevent the re-baselining.
4. **Refresh the plan when an upstream story merges.** RWB-E1-043's plan passed before its dependencies merged
   and has drifted (`NEXT-STORY-DEMO.md` D1 to D6). The planner should re-check paths against
   `develop-recovery` before the build starts.
5. **Make checkpoints part of the stage.** Usage limits stopped the agents several times. A short
   `agent-run-log.md` entry after each step made resuming possible; it should be required, not optional.
6. **Read gate counts from the gate line only.** Twice, an agent's chat summary gave counts that differed
   from its own gate file. The orchestrator brief should say to read only the `*_GATE:` line.
7. **One writer per evidence file.** Run READMEs written by one session and corrected by another drifted. The
   README should be generated from the log rows at merge.
8. **Check the environment before the suites run.** One e2e run failed because a local flag had the wrong
   value. `dev.ps1` should print and check the flags it depends on before it starts.
9. **Record the tool and model in every row.** The log's actor column names the agent but not the tool and
   model that ran it. Adding them would have made the opencode period visible without later correction rows.
