# Recovery Workbench — intake gap report

**Run:** `INTAKE-20261116`
**Inputs:** `requirement/legacy/` (733 entries), `.github/contexts/`, `docs/brds/`, `docs/prds/`,
`docs/decisions/`
**Outputs:** `requirement/BRD_RecoveryWorkbench.md`, `requirement/RecoveryWorkbench_Requirements.md`,
`requirement/Traceability_Matrix.md`, `docs/increments/INDEX.md`
**Status:** **PASS WITH RECORDED GAPS** — the v2 baseline is consistent enough to specify and plan the
implemented stories. No Critical gap blocks the run. The four open gaps are recorded and owned.

## 1. What was consolidated

| Source | Version | What was used | Result |
|---|---|---|---|
| Lean BRD Epic 1 / Epic 2 | v3 / v2 | Problem, outcomes, scope, rules, constraints, measures | `BR-RWB-001..020` |
| Business Requirements Program | v4 | 231 programme requirements | `FR-RWB-001..020` groups |
| Business Requirements Epic 1 | v4 | Epic 1 scope and requirements | Epic 1 baseline |
| Business Requirements Epic 2 | v4 | Epic 2 scope | Epic 2 baseline |
| FSD P1–P10, S1–S9 | v6 (P3 v4) | Functional behaviour | `FR-RWB-*` detail |
| TSD P1–P10, S1–S9 | v5 (P3/P4 v3) | Technical realisation | `backend-context.md` |
| Non-Functional Specification | v3 | 78 NFRs → 10 groups | `NFR-RWB-001..010` |
| Business Rules and Routing Logic | v4 | 448 rules, 10 families | `BR-RWB-*`, `project-context.md` §14 |
| Case and Workflow Model | v5 | 10 stages, 30 milestones, 150 tasks | `FR-RWB-003..006` |
| Users, Roles and Permissions | v4 | Roles, permissions, scopes | Actors and access |
| Logical Data Model and Data Dictionary | v8 | 133 external fields, 1,366 dictionary rows | Data requirements |
| Physical Schema | v6 | 93 tables, 30 views | Data requirements |
| API Specification | v4 | REST/OpenAPI 3.1 | Integration and contracts |
| ACE DB Alignment Change Register | v1, 15 Nov 2026 | D-RCV-35, U1–U5, 30 views, 4 extension tables | Data and integration |
| Temporal and Drools Change Register | v1, 16 Nov 2026 | D-RCV-36, T1–T10, 8 packages | Workflow and rules |
| Data Load Story Removals | v2, 15 Nov 2026 | 7 stories removed, E1-007 outbound-only | Retirement register |
| Rule Story Retirements | v1, 16 Nov 2026 | E1-029, TE-005, E1-048 retired | Retirement register |
| Build Sequence Epic 1 and Epic 2 | v6, 16 Nov 2026 | 115 items, 72 Epic 1 | `docs/increments/INDEX.md` |
| Decision Log | v10 | DT01–DT22, D-RCV-29–36 | Decision register |
| Engineering Practices | v5 | Stack, branching, tests, flags | `AGENTS.md` |
| Test Strategy / Test Cases / Regression | v3 / v7 / v6 | Levels, environments, gates | `testing-standards.md` |
| RWB-E1-042 pack | 10 Nov 2026 | Migration, tests, evidence | Preserved implementation |

## 2. Gap summary

| Severity | Count | Meaning |
|---|---:|---|
| Critical | 0 | None blocks the v2 baseline. |
| High | 0 | The 15–16 November changes resolved the old High gaps. |
| Medium | 4 | Recorded; do not block specification or planning. |
| Low | 5 | Record and monitor. |

## 3. Medium gaps

### GAP-005 — Thai labels and messages are proposed

| Field | Value |
|---|---|
| Evidence | Error and Message Standard v4; DL10 still open. |
| Impact | Thai UI and message wording may change after UAT. |
| Affected | All UI stories and message assertions. |
| Owner | BA / DL10 |
| Default | English canonical; Thai draft; tests assert the message ID and placeholders, not the Thai text. |
| Status | Open; non-blocking |

### GAP-006 — Per-story approver names are not in Jira

| Field | Value |
|---|---|
| Evidence | The source set names the Product Owner and FDA; Jira per-story approval comments are not complete. |
| Impact | A gate can appear approved without a named approver. |
| Affected | All story cards. |
| Owner | Product Owner |
| Default | Source-set approval at 16 Nov 2026; the plan gate records the named approver. |
| Status | Open; non-blocking |

### GAP-007 — ACE Tier 2 ingestion is an assumption

| Field | Value |
|---|---|
| Evidence | D-RCV-35 §2.1 lists AMIS, RPS, LIT, WIN, GL and COLLINS scores as ACE-ingested; the ACE team lead confirms at the gate. |
| Impact | If one source is not ingested, its fields leave RWB-ACE-001 and reopen U1 for that source. |
| Affected | E1-069 Section B, E2-006/018/019/021/027. |
| Owner | ACE team lead |
| Default | Treat as ACE-ingested; Section B behind flags until RWB-ACE-001. |
| Status | Open; non-blocking |

### GAP-008 — Temporal version, retention and RPO/RTO are not pinned

| Field | Value |
|---|---|
| Evidence | ADR-011 says the version is pinned at build; DL26/OPEN-010 open. |
| Impact | Environment and backup design may change. |
| Affected | E1-070/071, E2-037–040. |
| Owner | SCB IT / Compliance |
| Default | Pin at build; 30-day closed-workflow retention; NFR design baseline. |
| Status | Open; non-blocking |

## 4. Low gaps

| ID | Gap | Default |
|---|---|---|
| `GAP-009` | Old 78 specs predate the 16 Nov baseline | Archived; only E1-042/TE-001 re-specified |
| `GAP-010` | `RWB-E1-036` has no story file | Not created; not in the build sequence |
| `GAP-011` | Some Epic 2 screens lack field-level detail | Open at Epic 2 increment |
| `GAP-012` | The exact four extension-table names need a final V0001 check | Use the ACE Data Tier Map names |
| `GAP-013` | Jira keys are not assigned to every story | Local keys are authoritative |

## 5. Source conflicts and how they were resolved

| Conflict | Resolution | Evidence |
|---|---|---|
| ADR-003/004 and DT09/DT10 say no workflow or rules engine; the 16 Nov register adopts Temporal and Drools | ADR-011/012 and D-RCV-36 supersede them | `docs/architecture/decisions/README.md` |
| D-RCV-47 puts tables in schema `ace` with `rwb_` prefix; Physical Schema v6 and E1-069 use schema `recovery` | D-RCV-35 and ADR-010 win; D-RCV-47 is marked superseded | `docs/decisions/decision-register.md` |
| Old D-RCV-35/036 IDs collide with the new client decisions | Renumbered to D-RCV-51/52 | `docs/decisions/decision-register.md` |
| Old story set v5 has 78 stories; v7 has 62 E1 + 10 TE and removes/retires 10 | Use v7 and the build sequence; archive the old specs | `docs/increments/INDEX.md` |
| D-RCV-05 says no pipeline change; D-RCV-44 says run integration tests before every MR | Both apply: no CI change; pre-MR run rule | `docs/open-items.md` |
| E1-042 pack uses `${recoverySchema}` while D-RCV-47 said `ace` | Pack is correct for the new baseline; D-RCV-47 superseded | `backend-standards.md` BS-2 |
| Payment matching rule table vs Drools package | `payment_match_rule` dropped; package `PAYMENT_MATCH` | D-RCV-36 T10 |

## 6. Canonical source decisions

| Decision | Effect |
|---|---|
| Use the newest story set (v7 Epic 1, v5 Epic 2) | 72 active Epic 1 stories; 43 Epic 2 |
| Use Physical Schema v6 | 93 tables, 30 views, `recovery` schema |
| Use API Specification v4 | API contract for the spec/plan |
| Use ADR v3 | ADR-001–012 with 003/004/005 superseded |
| Use Decision Log v10 | D-RCV-029–036 and DT01–022 |
| Use Build Sequence v6 | Order 1–72 for Epic 1 |
| Preserve the RWB-E1-042 pack | Implemented migration and evidence |
| Preserve RWB-TE-001 implementation | Module boundary and BND-1–BND-5 |
| Archive the old 78 specs | Historical only |

## 7. Impact on traceability

- The traceability matrix is rebuilt from `BR-RWB-*` → `FR-RWB-*` → `RWB-<story>` → `SPEC-*` → `TASK-*`
  → evidence.
- The 10 removed/retired stories are not mapped to new specs; they map to a retirement row.
- The old 78 specs keep their old IDs in `output/_archive/` and are not current.
- `RWB-E1-042` and `RWB-TE-001` have current `SPEC-*` and `TASK-*` IDs.
- `RWB-E1-044` and `RWB-E1-043` keep their 10 Nov specs/plans as historical with a re-baseline flag.

## 8. Recommendation

Proceed to specification and planning for `RWB-E1-042` (INC-003) and `RWB-TE-001` (INC-002). Do not
start a build for `RWB-E1-044` or `RWB-E1-043` until their plans are re-run against the `recovery`
schema and the `v_ace_*` read path. Confirm GAP-005/006/007/008 at the next Product Owner and ACE
gate; none blocks the two implemented stories.
