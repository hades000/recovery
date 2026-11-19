# Recovery Workbench — AI-First SDLC repository

This folder is the **working repository** for the Recovery Workbench document set. It follows the
SCBX AI-First SDLC toolkit's repository contract and uses the playbook's lifecycle. The twelve
numbered folders in the parent directory remain the **source library**; this folder holds the
agent-readable corpus, the context package, the increment records and the run output.

## 1. Why this folder exists

The source set is organised by document type (decisions, business, requirements, stories, technical,
data, screens, AI, quality, policy, delivery, communication). The toolkit expects a repository
organised by lifecycle artefact:

```text
.github/        agents, rules, prompts, templates, scripts, contexts
docs/           increments, discovery, brds, prds, architecture/decisions
requirement/    legacy corpus, canonical requirements, traceability
output/         per-RUN_ID stage output
```

This folder is that contract. It does not rewrite the source documents; it converts them, indexes
them and gives the agents a stable place to read and write.

## 2. Structure

```text
13 AI-First SDLC repository/
├── .github/
│   ├── agents/ rules/ prompts/ templates/ scripts/ instructions/   # toolkit-owned
│   └── contexts/                                                   # project context
├── .vscode/mcp.json                                                # Windows toolkit path
├── AGENTS.md                                                       # Recovery Workbench standards file
├── docs/
│   ├── increments/    78 story cards (INC-001..INC-078), epics/EPIC-001, EPIC-002
│   ├── discovery/     problem, architecture, journeys, TOM, glossary, features, measures
│   ├── brds/          Lean BRDs, Business Requirements Program/E1/E2
│   ├── prds/          FSD P1–P10/S1–S9, Epics 3–8, NFR, Reporting/MI
│   └── architecture/decisions/  ADR-001-009, ADR-011, ADR-012, ACE architecture decision
├── requirement/
│   ├── legacy/        converted corpus, DOCUMENT_MAP.md, conversion report
│   ├── Context_RecoveryWorkbench.md
│   ├── BRD_RecoveryWorkbench.md
│   ├── RecoveryWorkbench_Requirements.md
│   ├── Intake_Gap_Report_RecoveryWorkbench.md
│   └── Traceability_Matrix.md
├── output/
│   ├── INC-001..INC-078/            # per-story stage output
│   └── CONTEXT-20261104/agent-run-log.md
└── tools/
    ├── convert_corpus.py
    ├── build_traceability.py
    └── build_increment_cards.py
```

## 3. How to use it

### 3.1 Read the context first

Every agent reads `.github/contexts/` before a task:

- `project-context.md` — business truth, features, rules, data, compliance, delivery, AI, gaps.
- `domain-context.md` — banking, recovery and system vocabulary.
- `frontend-context.md` — React/Vite, 53 screens, design system, accessibility.
- `backend-context.md` — Spring Boot, modules, APIs, data, integrations, security, observability.
- `testing-standards.md` — test levels, environments, gates and evidence.

### 3.2 Run the stages in order

1. **Context** — done: `output/CONTEXT-20261104/agent-run-log.md`.
2. **Intake** — done: `requirement/BRD_RecoveryWorkbench.md`,
   `requirement/RecoveryWorkbench_Requirements.md`,
   `requirement/Intake_Gap_Report_RecoveryWorkbench.md`.
3. **Specify** — Epic 1 batch written: 78 specs under `output/INC-001..INC-078`, all current and
   regated on 6 November 2026 after the decision-log rulings; see `docs/increments/INDEX.md`. The pilot is `RWB-E1-020`.
4. **Plan** — start the Implementation Planner on the approved spec.
5. **Build** — start the Implementation Builder in the ACE repository (not in this workspace).
6. **Validate** — API Tester and Functional Automation Test.
7. **Document and trace** — Technical Documenter and Traceability Manager.

Every stage is human-started. No stage runs automatically after another. Each stage emits a
`NEXT_STEP`; the human reviews the output and starts the next stage.

### 3.3 Choose the increment

- `EPIC-001` Foundation 1, release 30 November 2026. The 78 story increments are `INC-001` to
  `INC-078` and are indexed in `docs/increments/INDEX.md`.
- `EPIC-002` Foundation 2, release 31 December 2026. Story increments are created when the Epic 2
  specification batch starts.

Epics 3–8 are programme-level until their increment cards are written one month ahead.

## 4. Source mapping

| Source folder | Destination | What it becomes |
|---|---|---|
| 01 Decisions and governance | `requirement/legacy/01-decisions-and-governance/`; ADR candidates | Decision log and access model |
| 02 Business architecture and process | `requirement/legacy/02-.../`; `docs/discovery/` | Discovery, glossary, features, rules, roles, data |
| 03 Requirements and specifications | `docs/brds/`, `docs/prds/`, `requirement/legacy/03-.../` | BRDs, FSDs, NFR, Epics 3–8 |
| 04 User stories | `requirement/legacy/04-user-stories/` | Story files, build notes, acceptance criteria |
| 05 Technical architecture | `requirement/legacy/05-.../`; `docs/architecture/decisions/` | TSDs, API, integrations, ADRs |
| 06 Data | `requirement/legacy/06-data/` | Data products, data dictionary, schema |
| 07 Screens and experience | `requirement/legacy/07-.../` | Screen inventory, specs, design system, messages |
| 08 AI and agents | `requirement/legacy/08-ai-and-agents/`; `AGENTS.md` | AI standards, agent catalogue, governance |
| 09 Testing and quality | `requirement/legacy/09-.../`; `testing-standards.md` | Test strategy, cases, RTM, UAT |
| 10 Policy, controls and compliance | `requirement/legacy/10-.../` | PDPA, controls, regulatory map, retention |
| 11 Delivery and operations | `requirement/legacy/11-.../`; `docs/increments/` | Release plan, build sequence, risks, dependencies |
| 12 Project communication | `requirement/legacy/12-.../`; `docs/discovery/` | Overview, stakeholder map, index, control sheet |

The full 411-entry map is `requirement/legacy/DOCUMENT_MAP.md`.

## 5. Canonical source rules

1. Markdown for narrative; xlsx for data; docx for narrative where no Markdown exists; pptx, html
   and pdf are references where a canonical md/xlsx/yaml exists.
2. The zip is the portable archive; the extracted folder is the working copy.
3. The highest version in the filename is the set version; the internal document version is recorded
   in the map.
4. `requirement/legacy/` is the canonical corpus. `docs/` copies point back to the legacy source.
5. The 26 MB Project Hub is reference only; it is not an intake source.

## 6. Status

| Item | Status |
|---|---|
| Toolkit scaffold | Done |
| Corpus conversion | 411 entries, 0 failures |
| Document map | Done |
| Context package | Done, 145 CTX IDs |
| Intake | Conditional pass, 6 High gaps |
| Increment cards | `EPIC-001` and `EPIC-002`, plus 78 Epic 1 story cards (`INC-001`–`INC-078`); approvers `TBC` |
| Technical specification | 78 Epic 1 specs written; 78 current and regated after the D-RCV-28..33 rulings of 5–6 November 2026; 0 blocked |
| Build | Ready to start: the Implementation Planner works from the regated specs; no ACE source code yet |
| API / functional tests | Blocked until the build exists |

**Epic 1 batch:** `output/VERIFICATION-20261106/epic1-batch-report.md` (regate of 2026-11-04 in `output/VERIFICATION-20261104/`)
**Story manifest:** `output/EPIC1-STORY-MANIFEST.md`

## 7. Known limits

- No live Figma; design evidence is the screen inventory, screen specifications, design system and
  prototype.
- No ACE source code; the context describes intended behaviour, not verified implementation.
- Thai labels and messages are proposed (DL10).
- Availability, RPO/RTO and retention are open (DL11, DL26).
- Jira keys are not assigned; the traceability matrix keeps the Jira column blank.
- The source documents have version drift between file names and internal versions; the map records
  both.

## 8. Toolkit reference

The agents, rules, prompts, templates and MCP servers come from `../aisdlc-toolkit-main/repo-template`.
The lifecycle, gates and project paths come from `../aisdlc-playbook-main/docs`. The playbook is the
method; this folder is the work.
