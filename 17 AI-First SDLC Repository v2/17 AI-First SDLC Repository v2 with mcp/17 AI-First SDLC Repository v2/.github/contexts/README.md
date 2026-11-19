# Project context package

**Built:** 16 November 2026 (`CONTEXT-20261116`)
**Source:** document set v14, converted to `requirement/legacy/`
**Rule:** technical detail lives in its owning file; `project-context.md` holds business truth and
indexes the technical contexts. No file duplicates another file's inventory.

| File | Owner | Content | Status |
|---|---|---|---|
| `project-context.md` | Context Builder / Updater | Business overview, actors, scope, data requirements, compliance, delivery, AI, constraints, feature catalogue, rule catalogue, feature reconciliation, gaps, sources, agent guidance, decisions | `READY` |
| `domain-context.md` | Context Builder | Banking, recovery, ACE and platform vocabulary | `READY` |
| `frontend-context.md` | Context Builder | React/Vite, 53 screens, design system, accessibility, states | `READY` |
| `backend-context.md` | Context Builder | Spring Boot, modules, APIs, schema, views, Flyway, security, observability, Temporal/Drools | `READY` |
| `testing-standards.md` | Context Builder | Test levels, tools, data, gates, evidence, special rules | `READY` |
| `frontend-standards.md` | Context Builder | Frontend coding standards, import allow-list, accessibility | `READY` |
| `backend-standards.md` | Context Builder | Backend coding standards, migrations, API, security, batch | `READY` |

## Context IDs

| Prefix | Meaning | Count |
|---|---|---:|
| `CTX-PROJECT-*` | Project and business context | 1 |
| `CTX-BUSINESS-*` | Business statements | 1 |
| `CTX-FEAT-*` | Feature catalogue entries | 20 |
| `CTX-COMPLIANCE-*` | Compliance and controls | 1 |
| `CTX-DOMAIN-*` | Domain vocabulary | 1 |
| `CTX-BACKEND-*` | Backend context | 1 |
| `CTX-FRONTEND-*` | Frontend context | 1 |
| `CTX-TESTING-*` | Testing context | 1 |
| `CTX-BE-GAP-*` | Backend gaps | 6 |
| `CTX-FE-GAP-*` | Frontend gaps | 4 |
| `CTX-TECH-BE-*` | Backend technical facts referenced by stories | see `backend-context.md` |
| `CTX-TECH-FE-*` | Frontend technical facts referenced by stories | see `frontend-context.md` |

The machine-readable index is `context-manifest.json`.

## How downstream agents use this package

1. Read `project-context.md` for the business truth and the story's feature.
2. Read the owning technical context for implementation detail: `backend-context.md`,
   `frontend-context.md` or `testing-standards.md`.
3. Read `backend-standards.md` / `frontend-standards.md` before writing code.
4. Cite the `CTX-*` ID in the spec, plan and traceability matrix.
5. Do not copy technical inventory into `project-context.md`; link to it.

## Build notes

- Built by the Context Builder instructions in `.claude/agents/context-builder.md`; refreshed by the
  Context Updater instructions in `.claude/agents/context-updater.md`. The run is logged in
  `output/CONTEXT-20261116/agent-run-log.md`.
- No user question was asked. Ambiguities are in `project-context.md` §12 and §16 and in
  `output/CONTEXT-20261116/assumptions.md`.
- The 16 November re-baseline changed the data architecture (D-RCV-35) and the workflow/rules
  architecture (D-RCV-36). Both are applied throughout.
