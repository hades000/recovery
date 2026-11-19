# Recovery Workbench — context register

**Project:** Recovery Workbench (recovery module of ACE)
**Context version:** 1.0
**Created:** 2026-11-04
**Owner:** Forward Deployed Engineer / solution architect
**Status:** Ready for intake, with the gaps listed in section 5.
**Canonical context files:** `.github/contexts/project-context.md`, `domain-context.md`,
`frontend-context.md`, `backend-context.md`, `testing-standards.md`.
**Source corpus:** `requirement/legacy/` (411 converted files and zip entries; 256 source files plus
155 archive entries). The source register is in `requirement/legacy/DOCUMENT_MAP.md`.

This register is the traceable index of the context. It does not repeat the full prose of the context
files; each CTX ID points to the owning file and the source that establishes it.

## 1. Context inventory

| Context file | What it owns | CTX ranges |
|---|---|---|
| `.github/contexts/project-context.md` | Business truth: requirements, process, rules, data, compliance, delivery, AI | CTX-BUSINESS-*, CTX-STAKEHOLDER-*, CTX-FEATURE-*, CTX-RULE-*, CTX-DATA-*, CTX-NFR-*, CTX-COMPLIANCE-*, CTX-DELIVERY-*, CTX-AI-*, CTX-CONSTRAINT-*, CTX-GAP-* |
| `.github/contexts/domain-context.md` | Industry, banking and system vocabulary | Domain glossary; no new CTX IDs |
| `.github/contexts/frontend-context.md` | Frontend stack, 53 screens, design system, accessibility, states | CTX-GAP-019, 021, 025–027 |
| `.github/contexts/backend-context.md` | Backend stack, modules, APIs, data, integrations, security, observability, resilience | CTX-TECH-*, CTX-NFR-*, CTX-GAP-020, 028–032 |
| `.github/contexts/testing-standards.md` | Test levels, environments, data, gates, evidence | Testing standards; no new CTX IDs |

## 2. CTX index

### Business

| CTX ID | Statement (short) | Source | Status |
|---|---|---|---|
| CTX-BUSINESS-001 | The Workbench owns recovery cases from 90 DPD to close for Mortgage, HP and SSME; it is the recovery module of ACE. | Project Overview §1; ADR-001 | DOCUMENTED |
| CTX-BUSINESS-002 | 42 applications, spreadsheet case lists, decisions spread across email and files, slow turnaround. | Project Overview §2 | DOCUMENTED |
| CTX-BUSINESS-003 | One case list, one owner by rule, one decision record, rules as versioned data. | Project Overview §3 | DOCUMENTED |
| CTX-BUSINESS-004 | In scope: 90 DPD to close; D6–D9; D5 after TDR go-live; X1–X7; partners, documents, decision log, ledger; ACE recovery module. | Business Requirements Program §1.1 | DOCUMENTED |
| CTX-BUSINESS-005 | Out of scope: collections before day 90 and D1–D4; dialer; core bank booking; COLLINS models; TDR calculator; partner systems; bank policy. | Business Requirements Program §1.2 | DOCUMENTED |
| CTX-BUSINESS-006 | 8 epics, monthly releases Nov 2026–Jun 2027; E1/E2 confirmed, E3–E8 proposed. | Project Overview §7; Release Plan v3 | DOCUMENTED |
| CTX-BUSINESS-007 | 2027 benefit targets: recovery 73%, litigation 6 days, DIL 12 days, restructure 5 days, debt sale 45 days, 80% manual removed, 13 audit findings, NPA cycle 1,095 days. | Project Overview §8 | DOCUMENTED |
| CTX-BUSINESS-008 | Six stages: receive, route, resolve, enforce, realise, close; return to route on cure/payment/deviation/override. | Project Overview §4 | DOCUMENTED |
| CTX-BUSINESS-009 | 19 L1, 84 L2, 247 L3 processes; Workbench runs 06–19. | Business Requirements Program §4 | DOCUMENTED |
| CTX-BUSINESS-010 | Five decision steps: gather, decide, finalise/approve, act, log. | Project Overview §5 | DOCUMENTED |
| CTX-BUSINESS-011 | Decisions D1–D9; D1–D4 on EFS, D5 on EFS/ACE, D6–D9 in the Workbench. | Business Architecture slide 7 | DOCUMENTED |
| CTX-BUSINESS-012 | Deviations X1–X7 pause the route and return the case when cleared. | Project Overview §4; Deviation Catalog | DOCUMENTED |
| CTX-BUSINESS-013 | CMMN 1.1 case model; no workflow engine. | ADR-003; Engineering Practices §3 | DOCUMENTED |
| CTX-BUSINESS-014 | State model: stage, status, route, deviation flags; one state at a time. | REQ-CWC-005; Glossary | DOCUMENTED |
| CTX-BUSINESS-015 | One case per account at 90+ DPD, not excluded; exclusion rules as data. | REQ-CWC-001, 004 | DOCUMENTED |
| CTX-BUSINESS-016 | One case per customer and product; case ID RW-YYYY-NNNNNN, never reused. | REQ-CWC-002, 003 | DOCUMENTED |
| CTX-BUSINESS-017 | Allocation and assignment by rule; first match, default row, cap, overflow. | REQ-CWC-007..009 | DOCUMENTED |
| CTX-BUSINESS-018 | Transfer rules on stage, route, timer, deviation, approval, document, payment or manual request. | REQ-CWC-010 | DOCUMENTED |
| CTX-BUSINESS-019 | Service levels, escalation and prescription dates as data. | REQ-CWC-011, 012 | DOCUMENTED |
| CTX-BUSINESS-020 | Rule load, validation, version, rollback, change log. | REQ-CWC-013, 014 | DOCUMENTED |
| CTX-BUSINESS-021 | 448 rules in 10 route sets; DMN 1.4; hit policy Unique. | Business Rules v4 | DOCUMENTED |
| CTX-BUSINESS-022 | 252 rules with a timer; 366 move to a person/partner-owned state. | Business Rules v4 | DOCUMENTED |
| CTX-BUSINESS-023 | Every allocation, assignment, transfer and timer logs rule ID and version. | REQ-CWC-016 | DOCUMENTED |
| CTX-BUSINESS-024 | A model/agent can write to a queue with the same permission checks and a versioned log. | REQ-CWC-017, 018 | DOCUMENTED |
| CTX-BUSINESS-025 | Every open case has one next action, produced by the rule, with an owner and date. | REQ-WKM-012..016 | DOCUMENTED |

### Stakeholders

| CTX ID | Statement (short) | Source | Status |
|---|---|---|---|
| CTX-STAKEHOLDER-001 | 54 roles: 37 bank, 7 partner, 4 customer, 6 non-human. | Users, Roles and Permissions v3 | DOCUMENTED |
| CTX-STAKEHOLDER-002 | 37 bank roles by group and function. | Users, Roles and Permissions v3 | DOCUMENTED |
| CTX-STAKEHOLDER-003 | 7 partner roles; LED has no login. | Users, Roles and Permissions v3 | DOCUMENTED |
| CTX-STAKEHOLDER-004 | 4 customer parties use bank channels, not a Workbench login. | Users, Roles and Permissions v3 | DOCUMENTED |
| CTX-STAKEHOLDER-005 | 6 non-human actors with service identities. | Users, Roles and Permissions v3 | DOCUMENTED |
| CTX-STAKEHOLDER-006 | Four operating groups plus control functions and committees. | TOM slide 2 | DOCUMENTED |
| CTX-STAKEHOLDER-007 | 1,234 named users; about 410 online in the busiest hour. | NFR §2 | DOCUMENTED |

### Features, rules, data, NFRs, compliance, delivery, AI

The full tables are in `.github/contexts/project-context.md` sections 4–10. The CTX IDs are:

- `CTX-FEATURE-001` to `CTX-FEATURE-020` — the 20 product capabilities (P1–P10, S1–S9, cross-cutting).
- `CTX-RULE-001` to `CTX-RULE-016` — the 16 rule families behind the 448 rows.
- `CTX-DATA-001` to `CTX-DATA-007` — the 14 data products, 108 entities, freshness, quality, retention and PDPA.
- `CTX-TECH-001` to `CTX-TECH-007` — integrations, API/event contracts, no direct system-of-record call.
- `CTX-NFR-001` to `CTX-NFR-010` — volume, response, loads, availability, resilience, audit, retention, accessibility, scale.
- `CTX-COMPLIANCE-001` to `CTX-COMPLIANCE-005` — PDPA, 42 controls, regulatory map, audit findings, retention.
- `CTX-DELIVERY-001` to `CTX-DELIVERY-007` — releases, Kanban, gates, engineering practices, squad, risks, dependencies.
- `CTX-AI-001` to `CTX-AI-006` — agents, autonomy, decision governance, model endpoint, AI-assisted delivery and engineering.
- `CTX-CONSTRAINT-001` to `CTX-CONSTRAINT-010` — architecture, workflow, rules, data, database, branching, release, partner access, data protection.
- `CTX-GAP-001` to `CTX-GAP-025` — assumptions, open decisions and evidence gaps.

## 3. Source register

The full register with paths is in `.github/contexts/project-context.md` section 17. The primary
sources are:

| Area | Primary source |
|---|---|
| Business overview and outcomes | `docs/discovery/project-overview.md`; `docs/brds/business-requirements-program.md` |
| Epic 1 requirements | `docs/brds/business-requirements-epic-1.md` |
| Epic 2 requirements | `docs/brds/business-requirements-epic-2.md` |
| Non-functional requirements | `docs/prds/non-functional-specification.md` |
| Business rules | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-business-rules-and-routing-logic-v4-xlsx.md` |
| Case and workflow model | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-case-and-workflow-model-v5-xlsx.md` |
| Roles and permissions | `requirement/legacy/02-business-architecture-and-process/recovery-workbench-users-roles-and-permissions-v3-xlsx.md` |
| Data model | `requirement/legacy/06-data/recovery-workbench-conceptual-data-model-v5-xlsx.md`; `...logical-data-model...v6-xlsx.md` |
| API | `requirement/legacy/05-technical-architecture/recovery-workbench-api-specification-v2.yaml` |
| Architecture | `requirement/legacy/05-technical-architecture/recovery-workbench-target-architecture-v4-docx.md`; `docs/architecture/decisions/` |
| Engineering practices | `requirement/legacy/11-delivery-and-operations/recovery-workbench-engineering-practices-v4-docx.md` |
| AI standards | `AGENTS.md`; `requirement/legacy/08-ai-and-agents/recovery-workbench-ai-assisted-development-approach-v1.md` |
| Test strategy | `requirement/legacy/09-testing-and-quality/recovery-workbench-test-strategy-v2-docx.md` |
| PDPA and controls | `requirement/legacy/10-policy-controls-and-compliance/` |
| Delivery | `requirement/legacy/11-delivery-and-operations/` |
| Document index | `requirement/legacy/12-project-communication/recovery-workbench-document-index-v11.md` |

## 4. Context Builder questions and answers

The Context Builder workflow asks the questions below when the sources do not answer them. Each was
answered from the document set; the full log is `output/CONTEXT-20261104/agent-run-log.md`.

| # | Question | Answer | Source | Verification |
|---|---|---|---|---|
| 1 | Is this an existing/legacy project or greenfield? | Greenfield Workbench module inside the existing ACE platform. | ADR-001; Target Architecture §1–2 | Confirmed by three sources; no contradiction. |
| 2 | What is the planned technology stack? | Spring Boot (Java) with JPA, Batch, Security, Session, Cloud Azure, Data REST, HATEOAS and Quartz; React on Vite with Radix and TanStack Query; PostgreSQL; Entra ID, bank IAM, PII Kafka, audit/SOC logs; AKS. | Engineering Practices §2.3; AI Assisted Development Approach §3.1; Target Architecture §2 | Confirmed by three sources. |
| 3 | What are the primary sources? | The 12-folder document set, converted to Markdown; no Confluence link and no live Figma. | Document Index v11; conversion report | 256 source files mapped; 411 entries; 0 failures. |
| 4 | Who are the users and stakeholders? | 54 roles; 37 bank, 7 partner, 4 customer, 6 non-human; four operating groups plus control functions. | Users, Roles and Permissions v3; TOM slide 2 | Role count matches the source. |
| 5 | What compliance obligations apply? | Thai PDPA; BOT conduct; 42 controls; audit findings; records retention. | PDPA Design; Controls Catalog; Regulatory Map | Control count matches 42; PDPA bases proposed under DL26. |
| 6 | What is the architecture? | Modular monolith on ACE; common/collection/recovery modules; no workflow engine; CMMN 1.1; rules as data; decision log; document hub; agent runtime. | ADR-001..009; Target Architecture; Engineering Practices | ADR list matches 9 decisions. |
| 7 | What is the data architecture? | 14 data products, 108 entities, 17 subject areas, COLLINS daily batch, file loads, PostgreSQL, decision log hash chain, interaction ledger. | Conceptual Data Model v5; Logical Data Model v6; Physical Schema v4 | Counts match the source sheets. |
| 8 | What is the testing approach? | Unit 80%, rule table, integration, API contract, SIT, regression, NFR, accessibility, UAT; DEV synthetic, SIT/UAT masked. | Test Strategy v2 | Levels and environments match. |
| 9 | What is the delivery model? | Kanban, trunk-based, feature flags, monthly releases, six gates, two-week review windows. | Engineering Practices; Release Plan; Build Sequence | Six gates match; 115 build items. |
| 10 | What is the AI approach? | Agents through orchestrator/tool gateway, autonomy L0–L4, shadow then live, 60-second fallback to rules, decision log records model/agent/prompt versions. | Agent Catalog v2; AI Decision Governance v2; AI Assisted Development Approach | Agent list and autonomy levels match. |
| 11 | What is open or contradictory? | Version drift between filenames and internal versions; Epic 1 v7 vs story files v5; Epic 2 v5 vs v4; no Figma; no ACE code; Thai labels; RPO/RTO/retention; Jira keys; duplicate formats. | Document Index; Release Plan; Risks/Assumptions; conversion report | Gaps listed in section 5 and the intake gap report. |
| 12 | What is the first increment? | Epic 1, Foundation 1, release 30 Nov 2026; 67 requirements, 57 Must; 118 features; 67 stories. | Release Plan v3; Business Requirements Epic 1 v3 | Confirmed by both sources. |

## 5. Open questions and gaps

| ID | Gap | Owner | Needed by | Impact |
|---|---|---|---|---|
| CTX-GAP-016 | Filename versions and internal document versions disagree. | Document owner | Before requirements approval | Agents may cite the wrong version. |
| CTX-GAP-017 | Epic 1 consolidated v7 vs story files v5; 69 of 79 files in the extracted folder. | Business analyst | Before Epic 1 specification | Story-level run may use an older story. |
| CTX-GAP-018 | Epic 2 consolidated v5 vs story files v4. | Business analyst | Before Epic 2 specification | Same risk. |
| CTX-GAP-019 | No live Figma file. | Front-end lead | Before first UI story | Use local design artifacts. |
| CTX-GAP-020 | No ACE source code in this workspace. | FDE | Before build | Context is intended behaviour, not verified implementation. |
| CTX-GAP-021 | Thai labels and messages not approved (DL10). | Business lead | E2 | English first. |
| CTX-GAP-022 | RPO/RTO/availability and retention open (DL11, DL26). | Compliance / IT lead | Before NFR test plan | Targets not baselined. |
| CTX-GAP-023 | Jira project and issue keys not assigned. | Product owner | Before backlog import | Traceability uses RWB keys; Jira column blank. |
| CTX-GAP-024 | Duplicate formats and versions. | Document owner | Done | Map marks canonical/data/reference/superseded. |
| CTX-GAP-011 | RPO/RTO open (DL11). | IT lead | Before resilience test | Use ACE values. |
| CTX-GAP-012 | Retention periods open (DL26). | Compliance | Before retention build | Placeholder classes. |
| CTX-GAP-010 | Same-day interfaces not named (DL06). | Solution architect | Before integration build | Default end-of-day. |
| CTX-GAP-013 | Partner external access not live (DL03). | Architecture team | E5 | Partner portal testing limited. |
| CTX-GAP-014 | Model endpoint not approved (DL33). | CTO / Enterprise AI | E1 | Agents in shadow with rule fallback. |

## 6. Verification checklist

- [x] Every context file exists and has a stated purpose and scope.
- [x] Every business statement has a CTX ID and a source.
- [x] The feature catalogue covers all 20 product capabilities and names the evidence status.
- [x] The business rule catalogue covers the 16 rule families behind the 448 rows.
- [x] The data context covers all 14 data products and 108 entities by reference.
- [x] The NFR context covers all 10 NFR groups and the numeric targets.
- [x] The compliance context covers PDPA, 42 controls, regulatory mapping and audit findings.
- [x] The delivery context covers 8 releases, 6 gates and 115 build items.
- [x] The AI context covers agents, autonomy, decision governance and fallback.
- [x] The gaps and open decisions are listed with an owner and a needed-by date.
- [x] No personal data, credential or production data is included.
- [ ] Named approvers are confirmed. The increment cards carry `TBC` until the product owner and FDA
      name them.
- [ ] The source documents are re-issued at consistent versions. This is an intake gap, not a context
      gap.

## 7. Handoff

`NEXT_STEP: Human review of the context files, then run the Requirement Intake Consolidator on
requirement/legacy/ to produce BRD_RecoveryWorkbench.md, RecoveryWorkbench_Requirements.md and
Intake_Gap_Report_RecoveryWorkbench.md.`
