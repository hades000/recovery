# Squad current-state baseline — Recovery Workbench

| Squad / product | Prepared by | Date | Reviewed with |
|---|---|---|---|
| Recovery Workbench — TechX recovery squads, ACE team, collection squad | FDE (TBC) | 2026-11-04 | Product Owner, TechX tech leads (TBC) |

This baseline records how the squad delivers today, before the Agentic PDLC. It is built from
`Recovery Workbench Project Overview v4`, `Ways of Working and Governance v3`,
`Engineering Practices v4`, `Release Plan v3`, `Build Sequence v4`, `Test Strategy v2` and
`Risks, Assumptions, Issues and Dependencies v2`. Where a measure is not in the set, it is marked
`GAP`, not estimated.

## 1. Delivery approach

- **Method:** Kanban. Items are pulled in build-sequence order as capacity frees up; the two-week
  windows are sponsor review points, not sprint boundaries (DT04; Build Sequence v4).
- **Cadence:** continuous build; SIT and UAT take the last two weeks before each release; business
  testers work with the squads during the build; one production release at each month end, shared
  with the collection squad (Release Plan v3).
- **Gates:** six release gates — G1 design signed, G2 ready to pull, G3 SIT exit, G4 UAT exit, G5 go
  decision, G6 benefit check. A story that misses a gate stays behind its flag and moves to the next
  release.
- **Planning:** the release plan is fixed eight months ahead; Epics 1 and 2 are confirmed; Epics 3–8
  are proposed and confirmed one month ahead. What slips moves to the next epic; the release date
  does not move.
- **Consistency:** the practices are agreed by SCB IT, the ACE team, TechX and Henka. Some are
  "proposed" from 2 November and some are "assumed" until the bank decides (Engineering Practices
  §1). The baseline therefore records the intended practice, not a fully observed one.

## 2. Project and change types

| Type | Examples | Frequency / size |
|---|---|---|
| Greenfield module | The Workbench recovery module on ACE | Once, eight epics |
| Brownfield enhancement | Epic 2 ownership, timers, approvals, notices | Monthly |
| Integration | COLLINS, CCMS, SVAF, AMIS, RPS, WIN, NLEADS, partner portal | Continuous, per epic |
| Regulatory / audit change | BOT conduct, PDPA, audit findings, retention | Per finding or regulation |
| Data and reporting change | Data products, measures, Power BI, regulatory extracts | Monthly |
| Partner change | Panel, instructions, fees, scorecards, data room | E5–E7 |

## 3. Current SDLC / PDLC

```text
Demand / audit finding / regulatory change
  -> Business requirements (BRD, program and epic)
  -> Functional and technical specification (FSD/TSD per module)
  -> User stories and story files (Confluence form, INVEST, Gherkin)
  -> Build sequence and dependency plan
  -> Build in the ACE repository (trunk-based, feature flags)
  -> Unit, rule-table, integration and contract tests
  -> SIT (system, regression, NFR, accessibility)
  -> UAT (business scripts)
  -> Go decision and monthly release
  -> Operate (run books, job monitor, interface monitor, benefit check)
```

Key hand-offs and dependencies:

- Business requirements -> FSD/TSD: the module pair is the contract between the business and the
  build.
- FSD/TSD -> story files: the story file is the unit a coding agent receives.
- Story -> code: the ACE repository, module boundary, code owners and the nine pipeline checks.
- Code -> SIT/UAT: test data, masked copies, QA and business testers.
- Release -> operate: the ACE release owner, the monthly window and the run model.

## 4. Roles and ways of working

| Activity | Who performs | Who reviews / approves | Specialist input | Where work waits |
|---|---|---|---|---|
| Business requirements | Business lead / analyst | Product Owner, FDA | Risk, Compliance, Legal | Requirements approval |
| FSD/TSD | Solution architect | FDA | Security, Data, Compliance | Design and architecture approval |
| Story files | Analyst | Product Owner, tech lead | QA, business tester | Definition of ready |
| Plan | Developer with the agent | Tech lead | Solution architect | Plan approval |
| Code and tests | Developer with the agent | Named human reviewer | Tech lead, security | Pull request approval |
| SIT | QA engineer | QA lead with SCB IT | SCB IT security | SIT exit |
| UAT | Business testers | Business lead | Product owner | UAT exit |
| Release | Release owner in the ACE team | Product Owner / PM | ACE team | Go decision |
| Operate | Ops / System Manager | Product Owner | Platform administrator | Ongoing review |

The TechX squad shape is a tech lead, three back-end developers, one front-end developer and one QA
(A-09 / DL36). The ACE team owns the common module and the release decision. The collection squad
shares the notice path, contact stop and shared tasks (DL30).

## 5. Tools and workflow

| Concern | System | How information moves to the next tool |
|---|---|---|
| Requirements | This SharePoint document set; Word/Excel/PowerPoint; Markdown story files | Converted to `requirement/legacy/`; consolidated into the BRD and canonical requirements |
| Backlog | Story files and the build sequence; Jira project TBC (GAP-011) | Build sequence order; Jira import later |
| Source code | ACE repository (one service, one repository, one front end); GitLab MCP configured | Trunk-based branches named by story key; merge daily |
| Testing | JUnit, rule-table harness, Playwright, SIT/UAT environments | Test evidence under `output/<RUN_ID>/`; defects in the defect process |
| CI/CD | ACE pipeline; nine checks; monthly release | Deploy to DEV on merge; SIT on tag; UAT and production by the monthly release |
| Approvals | Decision log, delegation of authority table, six release gates | Decision log entry per decision; gate record per release |
| Operational work | Run books, job monitor, interface monitor, observability dashboards | Alerts and run books; benefit check after release |

## 6. Documentation and source of truth

- The **source library** is the twelve-folder SharePoint set. It holds the approved BRDs, FSD/TSD,
  data model, API spec, rules, roles, test strategy, controls and delivery plans.
- The **agent corpus** is `requirement/legacy/` in this repository. It is a converted copy; the
  originals remain in the source folders.
- The **story file** is the unit of work for a coding agent; it sits next to the code it produces.
- The **decision log** is the source of truth for decisions; the **delegation of authority table** is
  the source of truth for approval limits.
- The **business glossary** is the source of truth for names. One concept has one name in the model,
  the code and the conversation.
- The **document index** and **document control sheet** are the register of the set. They are not
  yet reconciled to the converted corpus (GAP-003).

## 7. Existing artefacts and context

| Artefact | Owner | Current? | Usable by agents? | Location |
|---|---|---|---|---|
| Lean BRD Epic 1/2 | Business lead | Yes | Yes (Markdown copy) | `docs/brds/` |
| Business Requirements Program/E1/E2 | Product owner | Yes | Yes (Markdown copy) | `docs/brds/` |
| FSD P1–P10 / S1–S9 | Solution architect | Yes | Yes (Markdown copy) | `docs/prds/` |
| TSD P1–P10 / S1–S9 | Solution architect | Yes | Yes (Markdown copy) | `requirement/legacy/05-technical-architecture/` |
| Target Architecture / ADRs | Solution architect | Yes | Yes | `docs/architecture/decisions/` |
| Logical data model / physical schema | Data steward | Yes | Yes (Markdown + CSV + SQL) | `requirement/legacy/06-data/` |
| API specification | Solution architect | Yes | Yes (YAML) | `requirement/legacy/05-technical-architecture/` |
| Business rules / routing logic | Centre of excellence | Yes | Yes (Markdown + CSV) | `requirement/legacy/02-business-architecture-and-process/` |
| Users, roles and permissions | Security administrator | Yes | Yes (Markdown + CSV) | `requirement/legacy/02-business-architecture-and-process/` |
| Test strategy / test cases / RTM | QA lead | Yes | Yes | `requirement/legacy/09-testing-and-quality/` |
| PDPA / controls / regulatory map | Compliance | Yes | Yes | `requirement/legacy/10-policy-controls-and-compliance/` |
| Release plan / build sequence / risks | Program manager | Yes | Yes | `requirement/legacy/11-delivery-and-operations/` |
| Screen inventory / specs / design system | Front-end lead | Yes | Yes (local design evidence) | `requirement/legacy/07-screens-and-experience/` |
| Project Hub | Program manager | Yes | Reference only (26 MB app) | `requirement/legacy/12-project-communication/` |

## 8. Pain points and constraints

- **Fragmented context:** 42 applications; case facts in the core bank, EFS, LIT, CCMS, SVAF, AMIS and
  document stores; no single screen.
- **Spreadsheet work:** teams keep case lists in Excel and SharePoint; hand-overs are manual.
- **Decision evidence:** why a route was chosen, who approved it and on what figures is spread across
  emails and files; 50 audit findings and fraud cases.
- **Turnaround:** 21 days litigation, 23 days restructure, 26 days deed in lieu; NPA sales cycle 1,486
  days.
- **Data latency:** COLLINS is end-of-day; collateral, appraisals and assets are weekly or monthly
  (R-01, R-02); same-day needs are not named (DL06).
- **Delivery constraints:** one DEV and one SIT slot (R-08); cross-squad release contention (R-03);
  partner access from outside the bank takes one to three months (R-06); business testers not always
  available (R-10); Thai wording not ready (R-11); model endpoint not approved (R-12).
- **Architecture constraint:** one ACE service, one repository, one front end; modular monolith;
  programmatic workflow; no workflow engine; rules as data; no direct system-of-record call.

## 9. Team needs

- One context package the agents can read, with the business truth, the stack and the test rules in
  predictable places.
- Clearer, testable story files; every rule ID, field and message ID traceable to its source.
- Faster feedback from the pipeline and from SIT/UAT; fewer manual hand-offs.
- Stronger review and governance support: the decision log, the delegation check and the
  separation-of-duty check.
- A safe way to use agents: synthetic data in DEV, masked data in SIT/UAT, no production data in a
  prompt.

## 10. Current performance

| Measure | Current value | Source | Period |
|---|---|---|---|
| Recovery rate on NPL | 66.3% | Project Overview §8 | 2026 to date |
| Litigation turnaround | 21 days | Project Overview §8 | Current |
| Deed in lieu turnaround | 26 days | Project Overview §8 | Current |
| Restructure turnaround | 23 days | Project Overview §8 | Current |
| Debt sale turnaround | No baseline | Project Overview §8 | Current |
| NPA sales cycle | 1,486 days | Project Overview §8 | Current |
| Audit findings and fraud cases | 50 | Project Overview §8 | Current |
| Manual processes removed | Near zero | Project Overview §8 | Current |
| Lead time | GAP — not in the set | — | — |
| Cycle time | GAP — not in the set | — | — |
| Defect escape rate | GAP — not in the set | — | — |
| Rework rate | GAP — not in the set | — | — |

The first four weeks of the pilot set the delivery baseline (cycle time, review time, rework, defect
escape, coverage, AI errors). The business baseline is the 2027 target table above; the measures are
read from the decision log per decision.

## Summary

The squad has a strong document set and a clear target architecture, but the work still moves through
spreadsheets, email and manual hand-offs. The highest-value agent support is in the pre-build stages:
one context package, a canonical requirement file, per-story specifications and a traceable decision
record. The build stage is constrained by the ACE repository, the shared release window and the
monthly gate cycle; agents can help most by making the context and the specification reliable, not by
adding parallel code paths. The baseline will be measured from the pilot's first four weeks, not
assumed.
