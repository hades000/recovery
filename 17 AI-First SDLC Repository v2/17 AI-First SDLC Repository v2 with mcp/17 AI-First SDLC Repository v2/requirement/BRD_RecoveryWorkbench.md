# Recovery Workbench — business requirements document

**Document ID:** `BRD-RWB-002`
**Version:** 2.0, 16 November 2026
**Supersedes:** BRD-RWB-001 (v1, 4 November 2026)
**Source:** Lean BRD Epic 1 v3, Business Requirements Program v4, Business Requirements Epic 1 v4,
Business Requirements Epic 2 v4, Non-Functional Specification v3.
**Owner:** Product Owner (Chitchaya Muanchonchana) with the recovery tech lead (Jesniphat Pukkham).
**Status:** Approved for the v2 baseline. Open decisions are in §14.

## 0. Trace metadata

| Field | Value |
|---|---|
| Requirement IDs | `BR-RWB-001..020`, `FR-RWB-001..020`, `NFR-RWB-001..010` |
| Source IDs | `REQ-*` from the Business Requirements set; crosswalk in `RecoveryWorkbench_Requirements.md` |
| Context | `.github/contexts/project-context.md` |
| Programmes | Epic 1 Foundation 1 (72 stories), Epic 2 Foundation 2 (43 stories) |
| Out of scope | Epic 3–8 journeys; inbound source loads; Excel/SharePoint trackers |

## 1. Purpose

The Recovery Workbench gives SCB Collections and Recovery one case system from 90 days past due to
close. It replaces spreadsheets, local trackers and disconnected systems with a case list, a case
record, documents, decisions, treatments, legal and partner work, reporting and measured AI assistance.
It is the recovery module of the ACE service.

## 2. Business context

| Item | Value |
|---|---|
| Current state | Case work is split across spreadsheets, trackers, email, COLLINS extracts and several legacy systems. Source data is copied into the recovery area and reconciled by hand. |
| Pain points | Duplicate data, no single case view, slow rule changes, no decision trail, document search by memory, no measured AI. |
| Change | One ACE module; one copy of source data read through views; rules as versioned Drools packages; Temporal for long-running case workflows from Epic 3; documents in one hub; a decision log for every action. |
| Benefit | Faster case handling, lower operational risk, auditable decisions, one data truth, rule changes without a release. |

## 3. Scope

**In scope**

- Epic 1 Foundation 1 (72 items): recovery tables and ACE views, case list and record, documents,
  decision log, configuration and reference data, access, notices, baseline measures, agent shadow.
- Epic 2 Foundation 2 (43 items): treatments and plans, approvals, payments, full case record,
  communications, stage 2/3 documents, live agents, Temporal and Drools operational stories.
- Cross-cutting: parameter catalog, reference data, feature flags, migrations, data dictionary,
  synthetic and masked data, interaction ledger.

**Out of scope**

- Inbound source loads, source-copy tables, data-quality load jobs and Excel/SharePoint trackers.
  ACE ingests source data (D-RCV-35 U1/U5).
- Case lifecycle execution on Temporal before Epic 3. Epic 1 installs the platform and worker
  (D-RCV-36 T1/T2).
- `payment_match_rule` and a home-built rule loader. Payment matching is package PAYMENT_MATCH.
- `RWB-E1-036` (no story file) and the 10 removed or retired stories.
- Epic 3–8 route screens and collections processes.

## 4. Stakeholders and users

| Stakeholder | Role | Interest |
|---|---|---|
| Product Owner | Chitchaya Muanchonchana | Scope, priority, acceptance |
| Recovery tech lead / FDA | Jesniphat Pukkham | Architecture, plan, release |
| Recovery officers and leads | RW-OFFICER, RW-LEAD, RW-MGR | Daily case work |
| Risk | RW-RISK | Rule approval, high-risk treatment |
| Compliance / audit | RW-AUDIT | Decision and access evidence |
| Central operations | RW-COE | Rules and reference data |
| Platform and security admins | RW-PLATADM, RW-SECADM | Temporal, flags, break-glass |
| ACE team | ACE tech lead | Schema, views, MR review |
| Partners | RW-PARTNER | Instructed cases |
| Customers | No login | Notices, payments, treatments |

Full role model: Users, Roles and Permissions v4; context `project-context.md` §2.

## 5. Business outcomes and measures

| Outcome | Measure | Baseline | Target |
|---|---|---|---|
| One case view | Cases worked in the Workbench | 0% | 100% of Epic 1 cases at exit |
| One data truth | Source copies in the recovery area | 11 copy tables | 0 |
| Faster rule change | Days from rule approval to in force | Release cycle | Same day (valid-from) |
| Auditable decisions | Actions with a decision-log entry | Partial | 100% |
| Document findability | Documents found by case/type/date | Manual | 100% indexed |
| AI quality | Intake classification agreement | Shadow | ≥ threshold before L1 |
| Operational stability | Failed jobs per week | Unknown | < 2, with a run book |

Measure definitions: Business Measures and Targets v2; P9 baseline (D-RCV-32).

## 6. Process and case model

- CMMN 1.1 terms: case, stage, milestone, task, sentry, event listener, case file item.
- 10 stages, 30 milestones, 150 tasks, 53 event listeners, 448 sentries.
- Entry at 90 DPD; exit at close, write-off, debt sale or legal conclusion.
- Route families: restructure, settlement, legal, asset sale, debt sale, write-off, recovery.
- Queue and owner model: queue → assignment → transfer → rebalancing.
- From Epic 3, one Temporal workflow per case; case data stays in the recovery schema.

## 7. Business requirements by capability

| ID | Requirement | Capability | Epic | Priority |
|---|---|---|---|---|
| `BR-RWB-001` | One case list with case ID, owner, queue, stage and ageing | Case work | 1 | Must |
| `BR-RWB-002` | A case record with accounts, parties, documents, history and decisions | Case work | 1 | Must |
| `BR-RWB-003` | Case creation at 90 DPD with a primary account and product group | Case work | 1 | Must |
| `BR-RWB-004` | Rule-driven allocation and assignment, with manual override and reason | Case work | 1 | Must |
| `BR-RWB-005` | Transfer between queues and owners with a reason and audit | Case work | 1 | Must |
| `BR-RWB-006` | Service levels, timers, escalation and prescription dates | Case work | 1 | Must |
| `BR-RWB-007` | Document store, index, OCR, classification, extraction and review queue | Documents | 1 | Must |
| `BR-RWB-008` | Notice generation from templates and merge fields | Communications | 1 | Must |
| `BR-RWB-009` | Append-only, hash-chained decision log that blocks an action it cannot record | Decision log | 1 | Must |
| `BR-RWB-010` | Configuration service and parameter catalog with owner, type and environment | Configuration | 1 | Must |
| `BR-RWB-011` | Reference data service with versioned tables | Configuration | 1 | Must |
| `BR-RWB-012` | Access control per data product, role masking and access log | Access | 1 | Must |
| `BR-RWB-013` | Read source data only through SELECT-only ACE views | Data | 1 | Must |
| `BR-RWB-014` | Temporal platform and worker for the case lifecycle from Epic 3 | Workflow | 1 | Must |
| `BR-RWB-015` | Rule package authoring, validation, approval, effective date and rollback | Rules | 1 | Must |
| `BR-RWB-016` | Interaction ledger for every Workbench action | Audit | 1 | Must |
| `BR-RWB-017` | Baseline and steering measures | Reporting | 1–2 | Must/Should |
| `BR-RWB-018` | AI intake and extraction in shadow, with measured promotion | AI | 1–2 | Must |
| `BR-RWB-019` | Treatment, plan and approval routing | Case work | 2 | Must |
| `BR-RWB-020` | Payment matching and booking match as Drools packages | Payments | 2 | Must |

## 8. Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| `NFR-RWB-001` | Availability | 99.5% service hours; 99.9% decision log |
| `NFR-RWB-002` | Case list performance | p95 ≤ 2 s |
| `NFR-RWB-003` | Case record performance | p95 ≤ 3 s |
| `NFR-RWB-004` | Document search | p95 ≤ 2 s |
| `NFR-RWB-005` | Throughput | 45,000 cases/year; 1,500 documents/day peak |
| `NFR-RWB-006` | RPO / RTO | 15 min / 4 h (design baseline, open) |
| `NFR-RWB-007` | Security | Entra ID, MFA, method security, RBAC, audit |
| `NFR-RWB-008` | Privacy | PDPA classification, masking, no personal data in Temporal history |
| `NFR-RWB-009` | Accessibility | WCAG 2.2 AA |
| `NFR-RWB-010` | Operability | Run book, health, metrics and alerts per service |

Full targets: Non-Functional Specification v3; context `project-context.md` §7.

## 9. Data and integration

- **Data:** PostgreSQL schema `recovery`; 93 tables and 30 views; 122 `sys_objects` and 1,366
  `sys_fields`; four extension tables; 20 source-copy/load tables removed.
- **Read path:** 30 SELECT-only `recovery.v_ace_*` views (16 Tier 1 over ACE tables today, 14 Tier 2
  after RWB-ACE-001). No FK into `public`. BND-6 fails a build that reads a `public` table.
- **Outbound:** integration adapters, outbox, Blob storage, WIN/NSS/LINE/e-sign in Epic 2.
- **No inbound load:** ALS, EFS, CCMS, SVAF, COLLINS, NLEADS, EasyApp and Entra ID data land in ACE.
- **Migrations:** `V<seq>__<story>_<name>.sql`, contiguous, forward-only, `${recoverySchema}`.

## 10. Business rules

- 448 routing rules in ten route sets; rule IDs and versions are the audit key.
- Entry/exclusion, allocation, assignment, transfer, service level, documents, decision log, payments,
  restructure and booking are the rule families.
- Rules are versioned data. From Epic 1 they are authored as Drools XLS packages, compiled, scenario
  tested and approved by Risk; the author cannot approve.
- The decision log records the rule ID and package version for every decision.
- Full rules: Business Rules and Routing Logic v4; context `project-context.md` §14.

## 11. Compliance and controls

- PDPA: classification, masking, retention, consent where required.
- Audit: append-only decision log, access log, hash-chain check.
- Model risk: rule package approval, scenario evidence, rollback.
- AI governance: shadow mode, measured promotion, no personal data in prompts.
- Change control: PR review, named reviewer, story → plan → code trace.
- Records: 10 years for case and decision records; legal hold; e-discovery.

## 12. Delivery

- Kanban; two-week sponsor review; 115 items.
- Epic 1: 72 items, release 30 November 2026. Epic 2: 43 items, release 31 December 2026.
- Two repositories: ACE monorepo for code and migrations; this repository for AISDLC artefacts.
- Branch `feature/<JIRA-KEY>-<slug>` from `develop-recovery`; MR into `develop-recovery`; batch MR
  into `develop`.
- Implemented and preserved: `RWB-E1-042`, `RWB-TE-001`. Planned and preserved: `RWB-E1-044`,
  `RWB-E1-043`.

## 13. Risks, assumptions and dependencies

| ID | Risk / assumption | Control |
|---|---|---|
| `R-01` | ACE Tier 1 tables lag the baseline | E1-069 checks before views compile |
| `R-02` | RWB-ACE-001 Tier 2 is late | Section B views behind flags |
| `R-03` | Temporal platform is not ready | Flag off returns the previous path; Epic 1–2 jobs stay Quartz |
| `R-04` | Drools package regression | Compile + scenarios + Risk approval + rollback |
| `R-05` | Removed stories are rebuilt by habit | Retirement register and AGENTS.md §4 |
| `R-06` | AI quality below threshold | Shadow until the promotion gate |
| `R-07` | Thai messages are draft | English canonical until DL10 |
| `R-08` | Approver names are not per story | Plan gate records the named approver |

## 14. Open decisions

| ID | Open item | Owner | Default |
|---|---|---|---|
| `OPEN-005` | Thai labels and messages | BA / DL10 | English canonical, Thai draft |
| `OPEN-010` | Availability, RPO/RTO, retention | Product Owner / Compliance | NFR design baseline |
| `OPEN-016` | Per-story approver names | Product Owner | Source-set approval; plan gate names the approver |
| `OPEN-020` | Temporal version and retention | SCB IT / Compliance | Pin at build; 30 days |
| `OPEN-021` | ACE Tier 2 ingestion assumption | ACE team lead | Assume yes; reopen U1 if not |

Full register: `docs/open-items.md`.

## 15. Approval

| Gate | Name | Date | Result |
|---|---|---|---|
| Requirements approval | Chitchaya Muanchonchana (Product Owner) | 2026-11-16 | Approved for the v2 baseline |
| Architecture approval | Jesniphat Pukkham (FDA) | 2026-11-16 | Approved; ADR-001–012 |
| Context readiness | Jesniphat Pukkham (FDE) | 2026-11-16 | Ready |

## 16. Traceability summary

| Layer | Count | Document |
|---|---:|---|
| Business requirements | 20 | this BRD |
| Functional requirements | 20 groups | `RecoveryWorkbench_Requirements.md` |
| Non-functional requirements | 10 | this BRD; NFR v3 |
| Active Epic 1 stories | 72 | `docs/increments/INDEX.md` |
| Epic 2 stories | 43 | `docs/increments/epic-2-stories.md` |
| Retired / removed | 10 | `docs/retirements/story-retirement-register.md` |
| Context IDs | 38 | `.github/contexts/context-manifest.json` |
| Full matrix | — | `requirement/Traceability_Matrix.md` |
