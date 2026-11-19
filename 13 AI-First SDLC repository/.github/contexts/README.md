# Project context

This folder is the context package every agent reads before a task. It was created by the Context
Builder run `CONTEXT-20261104` and is maintained by Context Updater.

| File | Owns | Read by |
|---|---|---|
| `project-context.md` | Business truth: requirements, features, rules, data, compliance, delivery, AI, gaps | Every agent |
| `domain-context.md` | Banking, recovery and system vocabulary | Every agent |
| `frontend-context.md` | React/Vite stack, 53 screens, design system, accessibility, states | Technical Specifier, Planner, Builder, Functional Test |
| `backend-context.md` | Spring Boot stack, modules, APIs, data, integrations, security, observability | Technical Specifier, Planner, Builder, API Tester |
| `testing-standards.md` | Test levels, environments, data, gates, evidence | Planner, Builder, API Tester, Functional Test, QA |

## Source register

The full register is in `project-context.md` §17. The primary sources are:

- `requirement/legacy/` — the converted corpus (411 entries).
- `docs/brds/` — the approved business requirements.
- `docs/prds/` — the FSD/TSD-level specifications.
- `docs/architecture/decisions/` — the twelve ADRs and the ACE decision.
- `docs/discovery/` — the discovery artefacts.

## Rules

1. Do not load unrelated files. Read the context file for your scope and the source documents the
   story names.
2. Context Builder creates new context only. Context Updater owns maintenance. Other agents must not
   modify context files.
3. Mark unverified statements `GAP` or `ASSUMED` and name the decision log entry.
4. No personal data, credentials or production data in context files.
5. When the source and the context conflict, the approved source wins; record a `CLAR-*` item.

## Status

`CONTEXT_CREATION_STATUS: READY` with the gaps in `project-context.md` §16. The full run log is
`output/CONTEXT-20261104/agent-run-log.md`.
