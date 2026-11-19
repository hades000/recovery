# Compliance validation — RWB-E1-001 specification (revision 2)

Specifier self-check before spec gate round 2. The independent gate results are in `../review/`
and are summarised in §4. Run-1 self-check kept in `compliance-validation.run1.md`.

| Field | Value |
|---|---|
| Artifact | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` (revision 2) |
| Stage | Specification remediation run 1 (pre-gate self-check, round 2) |
| Date | 2026-11-18 |
| Checked by | Technical Specifier (agent run) |

## 1. Specification execution gates (`.github/rules/specification-execution-gates.md`)

| Gate item | Result | Where |
|---|---|---|
| `## Change Scope Declaration` with all nine fields | PASS | spec.md |
| `## Requirement-to-SPEC Logic Coverage`; every BR, AC, exception, authority, contract, plan, guardrail, out-of-scope item and NFR mapped | PASS — 33 rows, 0 missing; 3 `COVERED (ASM)` on Blocker = Yes gaps, 1 `PARTIAL` (AC10), 1 N/A row with reasons | spec.md |
| User story intent; entry trigger and preconditions | PASS | spec.md |
| Field-level behaviour matrix; status-transition matrix | PASS | spec.md |
| Exceptional-case behaviour | PASS — X1–X8 from Story v7 plus X9–X11 | spec.md |
| API change assessment | PASS — `NO_API_CHANGE`; AC10 response gap routed to E1-043 / API owner, not hidden | spec.md; `contracts/backend-apis.json` |
| `## Unit Test Applicability` | PASS — frontend NO / NOT_APPLICABLE; backend YES / REQUIRED / 80% | spec.md |
| Clarification Log and status lines | PASS — 13 entries; 2 open on Blocker = Yes gaps, 2 open non-blocking | spec.md |
| Design evidence | `NOT_REQUIRED` / `NONE` | `figma/figma_report.md` |

## 2. Standards and guardrails

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source (document name and version) or a labelled assumption | PASS | Source table, `ASM-E1001-01..19`, `evidence/` scripts and outputs |
| No invented requirement; business text kept verbatim | PASS — DP07 text verbatim (`ASM-E1001-13`); SOR grammar labelled (`ASM-E1001-09`) | spec.md SPEC-006, -013 |
| Personal-data protection never weakened | PASS — protective union (526 ≥ 18 and ≥ 523); 4 PS-v6-only marks kept; marks as INSERT literals readable by the RWB-TE-011 lint; zero lint findings is an acceptance condition | SPEC-002 T10, SPEC-006, SPEC-018 |
| D-RCV-28 / D-RUN-07 migration rule | PASS — number at merge; line 1; `${recoverySchema}`; forward only | SPEC-001, -002 |
| D-RUN-12 one creator per table | PASS — T8 skips 4 tables, keeps 4 + 57 dictionary rows | SPEC-002, -003 |
| D-RUN-11 registry; D-RUN-08 seams | PASS — registration in E1-043 registry; access log seam E1-039 | SPEC-013, -016, -017 |
| D-RUN-13 lint | PASS — inherited from E1-044; SPEC-011 retired | SPEC-011 |
| D-RCV-35 / ADR-010 / D-RCV-36 | PASS — no ACE read, no constraint into `public`, no `v_ace_*` view in the migration, 18 link columns, no `payment_match_rule` | SPEC-002, -003 |
| Messages from the message seam by ID (AGENTS §3.6) | PASS — E1-042 `MessageResolver` | SPEC-015 |
| Tests not weakened (AGENTS §4.5) | PASS — `RecoveryDatabaseIT` keeps every assertion in a new mode; earlier ITs pin a Flyway target, no assertion removed; no lint rule weakened | SPEC-010, -018 |
| No personal data | PASS — synthetic UUIDs; seed has no owner user IDs; field-ID fixture only | SPEC-006, -017, -018 |
| Shared files untouched | PASS — proposed rows in `shared-updates.md` | — |

## 3. Known risks carried to the gate

1. Two Blocker = Yes document gaps (`GAP-E1001-17` DP07 width, `GAP-E1001-18` `is_personal`) need a
   human ruling before build; the spec proceeds on `ASM-E1001-13` and `-14`.
2. End-to-end catalog tests depend on RWB-E1-043 accepting a registered handler code (OPEN-NEW-3) and
   on an approver with Reference data A (OPEN-NEW-2).
3. The local switch (SPEC-010) touches E1-042, E1-043, E1-044 and E1-069 artefacts (OPEN-NEW-9).
4. AC10's message clause is PARTIAL until OPEN-NEW-8 is decided.

## 4. Spec gate results

### Round 1 (`../review/spec-gate-review.md`, 17 Nov 2026): `FAIL`

0 Critical, 3 High, 6 Medium, 4 Low.

| ID | Severity | Summary | Revision 2 answer (`gate-response.md`) |
|---|---|---|---|
| REVIEW-RWB-E1-001-001 | High | DP07 139 > `varchar(120)`. | Blocker gap 17; `ASM-E1001-13`; seed-fits test |
| REVIEW-RWB-E1-001-002 | High | BR7 vs PDPA Inventory v4. | Blocker gap 18; `ASM-E1001-14`; TC-14, TC-17 |
| REVIEW-RWB-E1-001-003 | High | No handler seam owner. | D-RUN-11 registry; SPEC-013, -017 |
| REVIEW-RWB-E1-001-004 | Medium | Ordering vs E1-042/043; rule (b). | D-RUN-07, -12; T8 |
| REVIEW-RWB-E1-001-005 | Medium | MSG-P1-011 type; `ReferenceLoad`. | AC10 PARTIAL; GAP-13; OPEN-NEW-8 |
| REVIEW-RWB-E1-001-006 | Medium | X8 access log and approval audit. | E1-039 seam; inherited controls |
| REVIEW-RWB-E1-001-007 | Medium | Local Flyway switch unspecified. | SPEC-010 |
| REVIEW-RWB-E1-001-008 | Medium | Messages mis-cited; resolver not reused. | SPEC-015 |
| REVIEW-RWB-E1-001-009 | Medium | `rule_package` exclusion basis. | Story v7 seed list + E1-072 v7; GAP-19 |
| REVIEW-RWB-E1-001-010 to -013 | Low | SOR label; `char(n)`; `valuation_key`; NFR/PBR v2. | F1–F3 labelled; C3; 18 link columns; NFR rows |

### Round 2 (`../review/spec-gate-review-2.md`)

**`FAIL`** — 0 Critical, 1 High, 3 Medium, 7 Low. Round-1 findings: 12 of 13 resolved; 003 returns as
014. The reviewer found GAP-E1001-17 and -18 sound, visible and protective, and noted that both still
need a human ruling (neither the AI orchestrator's triage nor the review is that ruling). The handoff
to the Implementation Planner stays blocked until round 3 (`spec-gate-review-3.md`) passes.

| ID | Severity | Summary |
|---|---|---|
| REVIEW-RWB-E1-001-014 | High | Registry contract contradicts the current E1-043 spec (SPEC-003, -025, -027, -029): E1-043 needs `refdata.columns.data_product` and loader/approver keys from this story and runs generic checks before the handler, so the `data_product` loads (AC3, AC7–AC11, TC-11) cannot be reached as specified. |
| REVIEW-RWB-E1-001-015 | Medium | AC9 owner-role message lists active role codes instead of the story's "role codes in LOV-ROLE"; change not recorded. |
| REVIEW-RWB-E1-001-016 | Medium | K0 required-value check overlaps K2/K3; an empty system of record or missing owner can lead with MSG-GEN-001 instead of MSG-P1-003 (AC7, X4). |
| REVIEW-RWB-E1-001-017 | Medium | E1-043's requests to this story (dictionary handler with RW-COMPLY approver, LOV-REF-TABLE seed correction) unanswered; conflicts with E1-064 v7 `DataDictionaryLoader`; nothing stops a later dictionary load removing the 526 marks. |
| REVIEW-RWB-E1-001-018 to -024 | Low | T8 count 57 should be 53; DF-REF-301 `character(64)` vs PS v6 `char(64)`; missing citations (PDPA Design v2 pointer, 26 fields with no inventory row, LDM v8 line 561); F3 literals; E1-043 interim refusal audit log for X8; stale cross-references; blocker-stage wording and D-RUN attribution. |
