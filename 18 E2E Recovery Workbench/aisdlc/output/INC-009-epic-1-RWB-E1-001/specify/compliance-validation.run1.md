# Compliance validation — RWB-E1-001 specification

Specifier self-check before the spec gate. The independent gate result is in
`../review/spec-gate-review.md` and is summarised in §4 once it exists.

| Field | Value |
|---|---|
| Artifact | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` |
| Stage | Specification (pre-gate self-check) |
| Date | 2026-11-17 |
| Checked by | Technical Specifier (agent run) |

## 1. Specification execution gates (`.github/rules/specification-execution-gates.md`)

| Gate item | Result | Where |
|---|---|---|
| `## Change Scope Declaration` with all nine fields | PASS | spec.md |
| `## Requirement-to-SPEC Logic Coverage` with the six columns; every BR, AC, exception, authority, contract, plan, guardrail and out-of-scope item mapped | PASS — 28 rows, 0 missing | spec.md |
| User story intent; entry trigger and preconditions | PASS | spec.md |
| Field-level behaviour matrix | PASS | spec.md |
| Status-transition matrix | PASS (schema version and catalog version; no case status) | spec.md |
| Exceptional-case behaviour | PASS — X1–X8 from Story v7 plus X9, X10 | spec.md |
| API change assessment | PASS — `NO_API_CHANGE`; contracts written | spec.md; `contracts/` |
| `## Unit Test Applicability`: frontend NO / NOT_APPLICABLE; backend YES / REQUIRED / 80% | PASS | spec.md |
| Clarification Log (CLAR-*) and status lines | PASS — 10 entries; status block present | spec.md |
| Design evidence | `NOT_REQUIRED` / `NONE` | `figma/figma_report.md` |

## 2. Standards and guardrails

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source (document name and version) or a labelled assumption | PASS | Source table and `ASM-E1001-*` in spec.md; `assumptions.md` |
| No invented requirement | PASS — departures from Story v7 are each settled by a cited higher-precedence source or labelled as an assumption | `document-gaps.md` |
| D-RCV-28 migration rule (name, line 1, `${recoverySchema}`, one file, forward only) | PASS | SPEC-001, -002 |
| D-RCV-35 / ADR-010: no ACE table read, no constraint into `public`, no `v_ace_*` view here | PASS | SPEC-002 T6, SPEC-003, SPEC-017 |
| D-RCV-36: 93-table v6, no `payment_match_rule` | PASS | SPEC-003 |
| Reference data rather than literals (AGENTS §3.2, §4.8) | PASS with note — product values come from seed/load; message texts in code per README decision 5 pattern (`ASM-E1001-06`) | SPEC-015, -017 |
| Method security on every endpoint | INHERITED — no new endpoint; E1-043 owns the check; access test TC-E1-001-11 kept | SPEC-016 |
| Tests not weakened (AGENTS §4.5) | PASS — the lint is narrowed to schema references with tests both ways; the `RecoveryDatabaseIT` baseline assertion is replaced by a stronger one, not dropped | SPEC-010, -011 |
| No personal data | PASS — synthetic UUIDs only; seed has no owner user IDs | SPEC-006, -017 |
| Existing code treated as baseline (phase0 audit A-04) | PASS — Flyway bean, lint and init scripts reused | Change Scope Declaration |
| Shared files untouched | PASS — proposed rows in `shared-updates.md` | — |

## 3. Known risks carried to the gate

1. Cross-story table collisions with E1-042, E1-043 and E1-072 migrations (`GAP-E1001-16`) need an
   orchestrator sequencing decision before build.
2. The end-to-end catalog ACs (AC3, AC7–AC11, TC-E1-001-11) depend on RWB-E1-043 publishing the handler
   seam and on an approver with Reference data A (`GAP-E1001-07`, `GAP-E1001-08`).
3. The local start and `RecoveryDatabaseIT` interim (`ASM-E1001-07`) changes an existing test's setup.

## 4. Spec gate result

Round 1 (`../review/spec-gate-review.md`, 17 Nov 2026): **`FAIL`** — 0 Critical, 3 High, 6 Medium,
4 Low. The handoff to the Implementation Planner is **blocked** until a human records remediation and a
re-review (`spec-gate-review-2.md`) passes, or explicitly accepts the findings. The self-check PASS
rows above do not override the gate.

| ID | Severity | Summary |
|---|---|---|
| REVIEW-RWB-E1-001-001 | High | DP07 system of record in Story v7 §13 is 139 characters; `system_of_record` is `varchar(120)` (PS v6 and Story v7 DDL), so the V0001 seed would fail. Verified by the specifier (139). |
| REVIEW-RWB-E1-001-002 | High | BR7 `is_personal` flags in PS v6 (18) conflict with PDPA Inventory v4; marked COVERED without a test or gap. |
| REVIEW-RWB-E1-001-003 | High | No story owns the `ReferenceTableHandler` seam; parallel INC-008 spec refuses `data_product`; AC3, AC7–AC11, TC-E1-001-11 not implementable as written, yet coverage reported SUCCESS. |
| REVIEW-RWB-E1-001-004 | Medium | Migration ordering vs E1-043 guarded tables and D-RCV-34 not reconciled; SPEC-001 rule (b) contradicts SPEC-002. |
| REVIEW-RWB-E1-001-005 | Medium | MSG-P1-011 is typed Error in MSG v4; `ReferenceLoad` has no message field, so NO_API_CHANGE is inconsistent. |
| REVIEW-RWB-E1-001-006 | Medium | Story X8 access-log requirement and approval audit not traced. |
| REVIEW-RWB-E1-001-007 | Medium | How `rwb.flyway.enabled=false` is set on the default local path is not specified. |
| REVIEW-RWB-E1-001-008 | Medium | Code-held messages mis-cite README decision 5; the E1-042 message resolver is not reused. |
| REVIEW-RWB-E1-001-009 | Medium | `rule_package` seed exclusion rests on D-RCV-29, which predates the table; E1-072 v7 conflicts not recorded. |
| REVIEW-RWB-E1-001-010 to -013 | Low | SOR grammar not labelled as assumption; `char(n)` missing from C3; `valuation_ext.valuation_key` missing from link keys; no NFR mapping and Pre-build Rulings v2 not cited. |
