# Proposed shared-file updates — INC-006-epic-1-RWB-TE-011 (plan)

This stage does not edit shared files (RUN-BRIEF rule 3). The orchestrator applies these rows in order. No ID is assigned here; other runs work in parallel. No row records a human approval or a decision on an open item.

## 1. `aisdlc/requirement/Traceability_Matrix.md`, row 006

| Field | Current | Proposed |
|---|---|---|
| Story | RWB-TE-011 | unchanged |
| Requirement | BR-RWB-013 / FR-RWB-013 | unchanged; add REQ-RDF-010, REQ-ACA-005, NFR-054 (PDPA part), NFR-045, CTL-11 |
| Spec | `output/INC-006-epic-1-RWB-TE-011/specify/spec.md` — SPEC-TE011-001..018 | unchanged; spec gate round 13 `PASS` 0/0/0/0 |
| Plan | No current plan | `output/INC-006-epic-1-RWB-TE-011/plan/plan.md` — TASK-00..TASK-34; plan gate pending |
| Test cases | TC-TE-011-01..11 | unchanged; TC-01..10 automated as ST-TE011-01..10; TC-11 `BLOCKED` (HV-01, OPEN-038) |
| Status | Specified | `Planned; plan gate pending` |
| Notes | — | `MIGRATION: NONE`; `FRONTEND: NOT_APPLICABLE`; backend tooling coverage 80% x 4 |

## 2. `aisdlc/docs/increments/INC-006-epic-1-RWB-TE-011.md`, "Card status"

| Field | Proposed |
|---|---|
| Specification | Done 17 Nov 2026 — `output/INC-006-epic-1-RWB-TE-011/specify/spec.md`; spec gate round 13 `PASS` 0/0/0/0 |
| Plan | Done 18 Nov 2026 — `output/INC-006-epic-1-RWB-TE-011/plan/plan.md`, 35 tasks TASK-00..TASK-34; plan gate pending |
| Test cases in story | 11 (TC-TE-011-01..11); TC-11 `BLOCKED` until OPEN-038 and the host exist |
| Build note | Builds only after RWB-E1-044, RWB-TE-001, RWB-E1-042, RWB-TE-002 and RWB-TE-003 are merged (TASK-00 stop rule) |

## 3. `aisdlc/docs/open-items.md`

**No new open item is proposed.** The spec-stage proposals stand as recorded in `../specify/shared-updates.md` §3:
`OPEN-NEW-TE011-1` (classification reconciliation; RW-COMPLY), `-4` (defaults confirmation), `-5` (the code-owner line; TechX tech leads), `-6` (masking helper; common module owner), `-8` (API mark alignment; API owner with RW-COMPLY). `OPEN-NEW-TE011-2`, `-3` and `-7` are withdrawn there; keep them withdrawn. Keep **RWB-E1-043 open item R4** as the single item for the `is_personal` mark route (owner RW-COMPLY) and add this story's question to it, as the spec asks.

The plan-stage silences PG-TE011-01..05 (`plan/document-gaps.md`) are specification-implementation choices, all Blocker = No; none needs an open item. If the orchestrator wants them visible, one line "PG-TE011-01..05 recorded, Blocker = No" is enough.

## 4. `aisdlc/docs/increments/INDEX.md`, row 006

| Field | Proposed |
|---|---|
| Status | `Planned; plan gate pending` |
| Plan | `output/INC-006-epic-1-RWB-TE-011/plan/plan.md` |

## 5. `aisdlc/DOCUMENT-GAPS.md`

No new document-set gap. DGL-01..15 from the specify stage stand, all Blocker = No; none is reopened. PG-TE011-01..05 are plan-stage silences, not document-set conflicts (see `plan/document-gaps.md`).

## 6. `AI-SDLC-BUILD-LOG.md` (orchestrator writes)

Suggested timeline row: `2026-11-18 | RWB-TE-011 | Plan | implementation-planner | P2 | DONE | plan.md v1: 35 tasks TASK-00..TASK-34; tool at tools/pdpa-lint with 35 main classes and 43 UT groups; 19 system scenarios plus the recorded baseline run; no migration; frontend N/A; PG-TE011-01..05 Blocker No; plan gate next`.

## 7. Notes to the orchestrator

1. **Spec header status (implementation gate).** `implementation-execution-gates.md` requires `Status: SUCCESS` in `spec.md` before build. The spec header carries the round-12 remediation text and names round 13 as next; the gate `PASS` and the coverage result are the equivalent ready state used for planning. Before the build, the spec header should read approved/closed. TASK-00 stops without it. This is a status line, not a rule change.
2. **Duplicate pipeline run.** A push to an open merge request's source branch produces a branch pipeline and a merge request pipeline, and `pdpa-lint` runs in both (GitLab's documented behaviour and the three `rules:` the spec requires). Recorded as risk R-1; the cost is one extra run per push.
3. **Git in the CI image.** The job installs `git` only when `eclipse-temurin:21-jdk` lacks it, because the changed-file list needs `git merge-base`. No `.gitlab-ci.yml` change beyond the new job.
4. **RWB-TE-002 owners.** The line `/tools/pdpa-lint/ @scb-ace/techx-recovery-tech-leads` is added to section `[Recovery module]` **in the same change as `tools/pdpa-lint/`**, never before (SPEC-TE011-014; TE-002 validator V9). Carry `OPEN-NEW-TE011-5`.
5. **RWB-E1-042 planner.** The §3b request stands: write each of the 16 step-3 constraint guards as `IF NOT EXISTS (SELECT 1 FROM pg_constraint ...) THEN ALTER TABLE ... ADD CONSTRAINT ...; END IF;` with the DDL run directly or through `EXECUTE format(...)` with a literal format string and only `%I` placeholders. The PDPA lint scans the merged file at this story's merge (SPEC-TE011-008, -018).
6. **RWB-E1-001 planner.** The §3b request stands: seed `sys_fields` as form-R1 `INSERT ... VALUES` rows with literal `field_id`, `object_name`, `field_name` and `is_personal`; no bulk `UPDATE`, `ON CONFLICT`, `INSERT ... SELECT` or `COPY` (the lint fails closed on those).
7. **RWB-E1-064** remains the owner of the load seam; RWB-E1-043 R4 (RW-COMPLY) remains the decision. This plan claims nothing about run-time loads (DGL-13).
8. **D-RUN decisions.** D-RUN-17 (TE-001 before E1-044) and D-RUN-19 are reflected in the preconditions; D-RUN-21 is cited for the one-module reading, with OPEN-050 still pending tech-lead ratification. This stage did not decide or ratify any of them.
9. **Plan gate input.** `plan/plan.md`, `plan/tasks.md`, `plan/data-model.md`, `plan/contracts/*.json`, `plan/tests/scenarios.md`, `plan/assumptions.md`, `plan/document-gaps.md` and this log are the review set. `plan/frontend/components.md` does not exist (UI In Scope NO).
