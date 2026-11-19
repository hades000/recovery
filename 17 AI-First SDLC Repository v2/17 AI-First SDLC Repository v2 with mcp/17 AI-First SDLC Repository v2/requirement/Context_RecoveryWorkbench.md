# Recovery Workbench — context document

**Run:** `CONTEXT-20261116`
**Version:** 2.0, 16 November 2026
**Canonical context package:** `.github/contexts/`
**Purpose:** one entry point for the context that downstream stages read. The detailed files stay in
`.github/contexts/`; this document indexes them and records the build decisions.

## 1. Context inventory

| ID | Context file | Scope | Status |
|---|---|---|---|
| `CTX-PROJECT-RWB-V2` | `.github/contexts/project-context.md` | Business truth, actors, scope, data, compliance, delivery, AI, feature/rule catalogue, coverage, gaps, sources, decisions | READY |
| `CTX-DOMAIN-RWB-V2` | `.github/contexts/domain-context.md` | Banking and recovery vocabulary | READY |
| `CTX-BACKEND-RWB-V2` | `.github/contexts/backend-context.md` | Spring Boot, modules, API, schema, views, Flyway, security, Temporal, Drools | READY |
| `CTX-FRONTEND-RWB-V2` | `.github/contexts/frontend-context.md` | React/Vite, 53 screens, design system, accessibility | READY |
| `CTX-TESTING-RWB-V2` | `.github/contexts/testing-standards.md` | Test levels, data, gates, evidence | READY |
| `CTX-BACKEND-STANDARDS-V2` | `.github/contexts/backend-standards.md` | Backend coding standards | READY |
| `CTX-FRONTEND-STANDARDS-V2` | `.github/contexts/frontend-standards.md` | Frontend coding standards | READY |

Machine-readable index: `.github/contexts/context-manifest.json`.
Run log: `output/CONTEXT-20261116/agent-run-log.md`.
Assumptions: `output/CONTEXT-20261116/assumptions.md`.

## 2. CTX index

| Prefix | Meaning | Count |
|---|---|---:|
| `CTX-PROJECT-*` | Project identity and scope | 1 |
| `CTX-BUSINESS-*` | Business statements | 1 |
| `CTX-FEAT-*` | Feature catalogue | 20 |
| `CTX-COMPLIANCE-*` | Compliance and controls | 1 |
| `CTX-DOMAIN-*` | Domain vocabulary | 1 |
| `CTX-BACKEND-*` | Backend context | 1 |
| `CTX-FRONTEND-*` | Frontend context | 1 |
| `CTX-TESTING-*` | Testing context | 1 |
| `CTX-BE-GAP-*` | Backend gaps | 6 |
| `CTX-FE-GAP-*` | Frontend gaps | 4 |
| `CTX-TECH-BE-*` | Backend technical facts | see backend context |
| `CTX-TECH-FE-*` | Frontend technical facts | see frontend context |

## 3. Source register

The full source register is `project-context.md` §17. The high-value sources:

| Source | Version |
|---|---|
| Project Overview | v4 |
| Business Architecture | v4 |
| Lean BRD Epic 1 / Epic 2 | v3 / v2 |
| Business Requirements Program / Epic 1 / Epic 2 | v4 / v4 / v4 |
| FSD P1–P10, S1–S9 | v6 (P3 v4) |
| TSD P1–P10, S1–S9 | v5 (P3/P4 v3) |
| Target Architecture | v6 |
| Architecture Decision Records | v3 |
| Logical Data Model and Data Dictionary | v8 |
| Physical Schema | v6 |
| API Specification | v4 |
| Business Rules and Routing Logic | v4 |
| Test Strategy / Test Cases / Regression Suite | v3 / v7 / v6 |
| ACE DB Alignment Change Register | v1, 15 Nov 2026 |
| Temporal and Drools Change Register | v1, 16 Nov 2026 |
| Decision Log | v10 |
| Build Sequence Epic 1 and Epic 2 | v6, 16 Nov 2026 |

## 4. Context build decisions

| ID | Decision |
|---|---|
| `L-RCV-01` | Build a new repository; do not edit the old one. |
| `L-RCV-03` | No questions in the context, specify and plan phases; record assumptions. |
| `L-RCV-04` | Preserve `RWB-E1-042` and `RWB-TE-001` as the implemented stories. |
| `L-RCV-05` | Preserve `RWB-E1-044` and `RWB-E1-043` plans as historical; mark for re-baseline. |
| `L-RCV-06` | Record the 10 removed/retired stories; do not rebuild. |
| `L-RCV-07` | Schema `recovery`, `${recoverySchema}`; D-RCV-47 is superseded. |
| `L-RCV-08` | Temporal and Drools only per ADR-011/012, behind flags. |

Full text: `docs/decisions/decision-register.md`.

## 5. Open questions and gaps

| ID | Gap | Resolution | Status |
|---|---|---|---|
| `GAP-005` | Thai labels and messages are proposed | English canonical; DL10 | Open |
| `GAP-006` | Per-story approver names | Plan gate records the named approver | Open |
| `GAP-007` | AMIS/RPS/LIT/WIN/GL/COLLINS ingestion by ACE | ACE team lead confirms; otherwise U1 reopens for that source | Open |
| `GAP-008` | Temporal version and retention | Environment Design v4 and DL26 | Open |
| `ASM-001..015` | See the assumptions register | Defaults recorded; none blocks the run | Accepted for this run |

## 6. Verification checklist

- [x] All seven context roles covered.
- [x] Business truth separated from technical detail.
- [x] Every feature has a source or an explicit gap.
- [x] Every technical context cites its source.
- [x] No personal data, credential or production data.
- [x] No blank placeholder or unexplained `TBD`.
- [x] No user question asked.
- [x] Traceability updated.

## 7. Handoff

```text
CONTEXT_CREATION_STATUS: READY
NEXT_STEP: Human review of the context package, then start the Technical Specifier on RWB-E1-042 (INC-003) and RWB-TE-001 (INC-002).
```
