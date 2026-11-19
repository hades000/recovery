# Spec gate review: RWB-E1-001 Recovery tables for the 14 data products

| Item | Value |
|---|---|
| RUN_ID | `INC-009-epic-1-RWB-E1-001` |
| Gate | SPEC GATE (Compliance Reviewer, round 1) |
| Reviewed | `specify/spec.md`, `compliance-validation.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `figma/figma_report.md`, `agent-run-log.md`, `evidence/` (`count_v6.py`, `lint_v6.py` re-run) |
| Instructions | `.claude/agents/compliance-reviewer.md`; `aisdlc/RUN-BRIEF.md` (paths, shared-file rules, precedence) |
| Precedence applied | D-RCV-35/36, then ADR v3, then Decision Log v10, then story files v7, then older maps and drafts |
| Excluded | README "Decisions taken while setting this up" items 1–7 (known, not re-reported) |
| Date | 17 November 2026 |

## Overall status

**STATUS: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 3 |
| Medium | 6 |
| Low | 4 |

**GATE RESULT: BLOCKED.** Three High and six Medium findings block the handoff to the Implementation
Planner until the spec is corrected and re-reviewed (`spec-gate-review-2.md`). The spec's own
`REQUIREMENT_COVERAGE_RESULT: SUCCESS [AMBIGUOUS_RULES: 0]` and the all-PASS self-check in
`compliance-validation.md` are not accepted: BR7, AC3, AC7–AC11 and X8 are marked COVERED although
the findings below show they are either not implementable as written or rest on an unrecorded
conflict.

## Sources verified by the reviewer

All paths are under `<docset>/17 AI-First SDLC Repository v2/requirement/legacy/` unless stated.

| Source | Version | Path / location | Used for |
|---|---|---|---|
| Story file RWB-E1-001 | v7 | `04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-e1-001-recovery-tables-for-the-14-data-products-v1.md` | ACs, BR1–BR9, X1–X8, §10, §12, §13 DDL and seed table |
| Physical Schema | v6 | `06-data/recovery-workbench-physical-schema-v6.sql` (6,850 lines; identical to repo `infra/postgres/schema/03-…`) | DDL, seeds, counts |
| Data Classification and Personal Data Inventory | v4 | `06-data/recovery-workbench-data-classification-and-personal-data-inventory-v4-xlsx.md` | PDPA flags |
| Decision Log | v10 | `01-decisions-and-governance/recovery-workbench-decision-log-v10-xlsx.md` lines 77, 78, 84 | D-RCV-28, -29, -36 |
| Client decisions D-RCV-35, D-RCV-36 | as held | `aisdlc/docs/decisions/` | Tier-1 precedence; CR A.5, A.7, row 18 |
| Error and Message Standard | v4 | lines 77, 78, 81, 85, 164 | MSG-P1-003/004/007/011, MSG-P4-002 |
| API specification | v4 | repo `api/recovery-api-v4.yaml` lines 3167–3240, 6022, 8832, 8980 | reference-loads, approve, `E422`, `ReferenceLoad`, `Problem` |
| Story file RWB-E1-072 | v7 | same folder as above | rule_package seed |
| RWB-E1-001 Specification Rulings / Pre-build Rulings | v2 (both Proposed) | `aisdlc/docs/decisions/` | R1–R4 |
| Parallel spec RWB-E1-043 | INC-008 | `aisdlc/output/INC-008-epic-1-RWB-E1-043/specify/` | seam ownership |
| Repo baseline | as on disk | `RecoveryFlywayConfig`, `RecoveryDatabaseIT`, `RecoveryFlags`, `application.yaml`, `infra/postgres/init/*`, migration folder README, `README.md`, `aisdlc/.github/contexts/*`, `Traceability_Matrix.md`, `open-items.md`, `decision-register.md` | build path, standards |

## Findings

### REVIEW-RWB-E1-001-001 — High — DP07 seed value does not fit `data_product.system_of_record varchar(120)`

- **Maps to:** SPEC-RWB-E1-001-004, SPEC-RWB-E1-001-006, ASM-E1001-04; AC1, AC2, AC4, AC6; FR-RWB-013.
- **Evidence:** Story v7 §13 seed table gives DP07's system of record as a 139-character value
  (begins "ACE (ingested from LIT and WIN) for the court record…"). Both Story v7 §13 DDL and PS v6
  line 820 declare `system_of_record varchar(120)`. SPEC-004 adopts `varchar(120)`; SPEC-006 seeds
  "exactly as Story v7 §13 seed table". The sys_fields `physical_type` for this column (DF-REF-074)
  also says `varchar(120)`.
- **Failure scenario:** the `data_product` INSERT raises "value too long for type character varying(120)";
  per SPEC-007 the whole migration rolls back, so AC1, AC2 and AC6 cannot pass and no schema exists.
  None of GAP-E1001-01..16 records the conflict.
- **Remediation:** record a document gap (Story v7 §13 seed vs Story v7 §13 / PS v6 DDL). Decide by
  precedence or a ruling between (a) widening the column, which changes the PS v6 DDL and the
  DF-REF-074 `physical_type` together so SPEC-009 C3 still passes, or (b) shortening the seed text
  (the Rulings v2 R4 wording is about 112 characters). State which, cite it, and add a test that every
  seed value fits its column.

### REVIEW-RWB-E1-001-002 — High — BR7 personal-data flags conflict with PDPA Inventory v4; marked COVERED with no gap

- **Maps to:** BR7, SPEC-RWB-E1-001-006 (sys_fields seed), coverage row BR7; FR-RWB-013; seam to RWB-E1-016 masking.
- **Evidence:** PS v6 seeds `is_personal = true` on 18 fields. PDPA Inventory v4 classifies 523 of
  1,366 fields as personal data, including 12 direct identifiers and 5 sensitive fields. Nine
  direct-identifier or sensitive fields are `is_personal = false` in PS v6: DF-ACE-003, DF-ACE-041,
  DF-ACE-053, DF-ACE-060, DF-ACE-061, DF-ACE-116, DF-EXT-002, DF-EXT-003, DF-EXT-004. Four fields
  are flagged true in PS v6 that the inventory classes as not personal: DF-DOC-049, DF-DOC-052,
  DF-DOC-077, DF-DOC-089. The spec's coverage row says BR7 is "Seeded from PS v6 as written" and
  COVERED; no test asserts BR7 and no gap records the conflict.
- **Failure scenario:** RWB-E1-016 masks by this flag (Story v7 BR7 and §19); direct identifiers
  would be shown unmasked in any consumer reading `v_data_dictionary.is_personal`. This is a
  customer-data-protection control (reviewer required check "Customer and account data protection";
  pdlc stop condition on PII classification).
- **Remediation:** record the conflict as a document gap with both citations; apply precedence
  (D-RCV-35 §3.3 personal-data provisions, then the PDPA design) or request a ruling from the data
  architect and DPO through an open item in `shared-updates.md`; state which source the seed follows;
  add a BR7 test (at minimum: every inventory direct identifier and sensitive field is
  `is_personal = true`). Do not mark BR7 COVERED until then.

### REVIEW-RWB-E1-001-003 — High — Handler seam has no owner; AC3, AC7–AC11 and TC-E1-001-11 are not implementable as specified

- **Maps to:** SPEC-RWB-E1-001-012, -013, -014, -015, -017; ASM-E1001-05, ASM-E1001-12; GAP-E1001-07; AC3, AC7, AC8, AC9, AC10, AC11, X4–X8; FR-RWB-013.
- **Evidence:** SPEC-013 implements `ReferenceTableHandler` (Story v7 §12) and says only the handler
  bean "is exposed to RWB-E1-043 through its published interface". The parallel RWB-E1-043 spec
  (INC-008) defines no such interface: its `document-gaps.md` GAP-08 says no handler interface exists
  and flags GAP-08 "as a likely blocker for the next story (RWB-E1-001…)"; its SPEC-002 accepts a
  table code only if it is an active LOV-REF-TABLE value (through its `ReferenceTableCodeSource` SPI)
  **and** has a column definition `refdata.columns.<code>` in `parameter_catalog` (its SPEC-003), and
  it names `data_product` as refused. Its package is `recovery.casewf.refdata`. This spec instead
  places the handler in `dataengine`, gives no column definition for `data_product`, and its
  ASM-12 adds `data_product` to LOV-REF-TABLE without addressing the column-definition rule.
  GAP-E1001-07 is Blocker = No and the coverage result reports 0 ambiguous.
- **Failure scenario:** with E1-043 built as specified, a `data_product` load is refused with
  MSG-P3-027 before any handler runs, so none of the MSG-P1-003/004/007/011 paths can be reached;
  the `dataengine` classes cannot compile against an interface that no story delivers (D-RUN-08).
- **Remediation:** either (a) own the SPI in this story with an explicit, cited basis and reconcile
  it with INC-008 (package, `ReferenceTableCodeSource`, column definition for `data_product`,
  module direction to avoid a P1/P3/P4 cycle), or (b) mark AC3, AC7–AC11 and TC-E1-001-11 BLOCKED on
  a named seam and raise GAP-E1001-07 to Blocker = Yes with a ruling request. Correct the coverage
  result accordingly.

### REVIEW-RWB-E1-001-004 — Medium — Migration ordering rules not reconciled; rule (b) contradicts SPEC-002

- **Maps to:** SPEC-RWB-E1-001-001, SPEC-RWB-E1-001-002; ASM-E1001-02; GAP-E1001-16; FR-RWB-013.
- **Evidence:** SPEC-001 rule (b) says that if another recovery migration merged first, the file
  "omits any table, index, trigger or seed row" already created. SPEC-002 says the body is PS v6
  "transformed as follows and nothing else". INC-008 (Build Sequence v6 order 8, before this story's
  order 9) creates `reference_version` and `reference_row` guarded with `CREATE TABLE IF NOT EXISTS`,
  drops PS v6 `uk_reference_row` and adds `UNIQUE (version_id, row_key)`. The squad decision
  D-RCV-34 in `aisdlc/docs/decisions/decision-register.md` line 79 assigns E1-042 V0001/V0002 and
  E1-001 V0003 against Build Sequence v4. The spec names neither, and does not list which objects
  rule (b) would omit.
- **Failure scenario:** the planner cannot tell whether V0001 creates `reference_row` with
  `uk_reference_row` (PS v6) or omits it; either choice breaks the other story's migration or
  conformance test, and the end state no longer equals SPEC-002.
- **Remediation:** record the conflict; state the order (D-RUN-07 placeholder kept), list the
  objects owned by E1-042/E1-043 that V0001 omits or must match, and amend SPEC-002's "nothing else".

### REVIEW-RWB-E1-001-005 — Medium — MSG-P1-011 repeat: mis-cited as "not an error" and not carriable without an API change

- **Maps to:** SPEC-RWB-E1-001-014, SPEC-RWB-E1-001-015; GAP-E1001-13; AC10, X7; `contracts/backend-apis.json` (NO_API_CHANGE).
- **Evidence:** SPEC-015 says the repeat "is not an error (Story v7 §12)" and returns `ReferenceLoad`
  "with the message in its response". Error and Message Standard v4 line 85 types MSG-P1-011 as
  Error. API v4 `ReferenceLoad` (line 8832) has only `id, table, validFrom, status, rows`: no message
  field. INC-008 SPEC-006 answers a repeat with 201 and the same `ReferenceLoad` body, no message.
- **Failure scenario:** AC10 ("returns MSG-P1-011") cannot be observed at the API; the
  NO_API_CHANGE claim and the contract file are inconsistent with the stated behaviour.
- **Remediation:** correct the citation; choose and cite one of: a Problem response carrying
  MSG-P1-011, an API v4 change (then the contract file must record it), or AC10 verified at handler
  level only with a recorded gap.

### REVIEW-RWB-E1-001-006 — Medium — X8 access-log requirement dropped; approval audit not traced

- **Maps to:** SPEC-RWB-E1-001-016; X8, TC-E1-001-11; §10 Authority; exceptional-case row X8.
- **Evidence:** Story v7 X8 requires that "the refusal is in the access log". The spec's X8 row and
  TC-E1-001-11 assert only 403 with MSG-P4-002. API v4 approve operation (lines 3167–3240) records the
  approval in the decision log (AC-VERS) and applies maker-checker (MSG-P7-002); the spec does not
  record these as inherited from RWB-E1-043 / RWB-E1-039 or as a seam.
- **Failure scenario:** an unauthorised catalog load leaves no access-log evidence the test can check;
  the reviewer's "audit logging for sensitive actions" check cannot be satisfied from the spec.
- **Remediation:** add the access-log assertion (or name the owning story as a seam) and record the
  approval audit and maker-checker as inherited controls with their owners.

### REVIEW-RWB-E1-001-007 — Medium — How recovery Flyway is disabled on the default local path is unspecified

- **Maps to:** SPEC-RWB-E1-001-010; ASM-E1001-07; GAP-E1001-11; AC2, AC3 (stack checks).
- **Evidence:** SPEC-010 states "on that path `rwb.flyway.enabled=false`" but names no file or
  mechanism. Repo `application.yaml` sets `rwb.flyway.enabled: true`; `docker-compose` and
  `infra/postgres/init` default `RWB_LOAD_REFERENCE_SCHEMA=true`; `RecoveryFlywayConfig` uses
  `baselineOnMigrate(true)` at version 0. The migration folder README says to switch the flag to false
  when V0001–V0003 ship, which this story does not complete.
- **Failure scenario:** after merge, `./scripts/dev.ps1 backend` runs the migration on a schema
  already built from PS v6 and fails on "relation already exists"; if Flyway is disabled instead,
  the running stack used by e2e and API Tester keeps the PS v6 `v_data_dictionary` (with
  `f.owner_role`) and PS v6 seed, so AC2 and AC3 cannot be checked there.
- **Remediation:** name the exact switch (profile, env var or property file), its default, and which
  test stage runs against which schema; record the stack limitation as a gap.

### REVIEW-RWB-E1-001-008 — Medium — Messages held in code: README decision 5 is mis-cited

- **Maps to:** ASM-E1001-06; SPEC-RWB-E1-001-015; GAP-E1001-14; AGENTS.md §3.6.
- **Evidence:** ASM-06 cites README decision 5 to hold MSG-P1-003/004/007/011 as English text in code.
  README decision 5 says story messages come from the message table. AGENTS.md §3.6 requires messages
  from the message table by rule ID. RWB-E1-042's resolver seam (OI-E1-042-004) exists and INC-008
  SPEC-020 reuses it; this spec does not.
- **Failure scenario:** literal message texts in code without a valid basis; Thai text never served
  (Thai is the default locale).
- **Remediation:** remove the mis-citation; reuse the E1-042 resolver seam as INC-008 does, or record
  the departure as a gap with a valid basis and an open item.

### REVIEW-RWB-E1-001-009 — Medium — Exclusion of the rule_package seed rests on a decision that predates it; E1-072 conflict unrecorded

- **Maps to:** ASM-E1001-03; SPEC-RWB-E1-001-002 (T5), SPEC-RWB-E1-001-003, SPEC-RWB-E1-001-006; GAP-E1001-05, GAP-E1001-16.
- **Evidence:** DL v10 D-RCV-29 (line 78) lists seeds "as held in … Physical Schema v5" and was
  ruled before D-RCV-36 (line 84), which introduced the rule_package tables (D-RCV-36 row 18:
  "Rule package codes in Phase 1: 8"). PS v6 seeds 8 `rule_package` rows. RWB-E1-072 v7 V072_1
  creates `rule_package` and `rule_package_version` itself, with standard columns, and seeds 5 codes
  with `hit_policy` FIRST_MATCH; PS v6 (adopted by SPEC-003) has no standard columns on these tables
  and `CHECK (hit_policy IN ('FIRST'))`.
- **Failure scenario:** E1-072's migration fails on the existing tables or on the CHECK; the
  exclusion of the 8 PS v6 rows has no tier-1 basis.
- **Remediation:** cite a valid basis (D-RCV-36 artefact precedence) for including or excluding the
  rows; record the E1-072 vs PS v6 table/CHECK conflict as a gap and an open item.

### REVIEW-RWB-E1-001-010 — Low — SOR grammar is spec-derived and admits invalid values

- **Maps to:** SPEC-RWB-E1-001-013 (SOR-1..4); ASM-E1001-09; BR3, BR5.
- **Evidence:** SOR-2 accepts any remainder that names "Recovery Workbench", so
  "ACE (ingested from X) and CCMS, with Recovery Workbench" passes although it names a second source of
  record outside ACE. The grammar is not in Story v7 or MSG v4; ASM-09 labels only list completeness.
- **Remediation:** label the grammar as an assumption and tighten it (closed forms per Story v7 §13
  seed values) with negative unit cases.

### REVIEW-RWB-E1-001-011 — Low — Conformance type list omits `char(n)`

- **Maps to:** SPEC-RWB-E1-001-009 (C3); AC5.
- **Evidence:** PS v6 uses `char(n)` on 9 table fields; the C3 normalisation list omits it, so the
  1,075/1,075 claim is unproven for those fields.
- **Remediation:** add `char(n)` (`character(n)` in `information_schema`) to the list.

### REVIEW-RWB-E1-001-012 — Low — `valuation_ext.valuation_key` not in the ACE link-key assertion

- **Maps to:** SPEC-RWB-E1-001-003; BR8; TC-E1-001-01.
- **Evidence:** SPEC-003 lists 16 link columns; `valuation_ext.valuation_key` is also an ACE link key
  (D-RCV-35 U3 extension table) and is not asserted.
- **Remediation:** include it or state why it is not a link key.

### REVIEW-RWB-E1-001-013 — Low — Traceability: no NFR mapping; Pre-build Rulings v2 not cited

- **Maps to:** coverage table; `Traceability_Matrix.md` row 009 (BR-RWB-013 / FR-RWB-013); NFR-RWB-001..010 (CTX-TESTING-RWB-V2).
- **Evidence:** the spec maps no NFR ID; the matrix lists NFR-RWB-001..010 for testing standards.
  RWB-E1-001 Pre-build Rulings v2 (Proposed) is not cited although Specification Rulings v2 is.
- **Remediation:** map the applicable NFR IDs (coverage gate, migration, security); cite Pre-build
  Rulings v2 or state why it does not apply.

## Verified correct (no finding)

- Counts reproduced from PS v6 by the reviewer: 93 tables (89 + 4 extension), 123 `sys_objects`,
  1,379 `sys_fields`, conformance 1,047/1,047 and 1,075/1,075, 30 views with 304 view fields, 92
  foreign keys, 112 indexes, 3 CHECK constraints, 2 append-only triggers; seeds 598 / 54 / 421; 24
  objects with NULL `data_product`; 16 listed link keys `varchar(255)` in no FK; no constraint into
  `public`; none of the 20 removed tables; no `payment_match_rule`.
- PS v6 SHA-256 and line citations (815/820, 2156, 2182, 2389, 2398, 3516, 4684, 5284, 5340, 5350,
  6131, 6823) match the file.
- `evidence/count_v6.py` and `evidence/lint_v6.py` re-run with `python -I`: results match; the lint
  flags 297 `sys_fields` string literals, confirming the need for SPEC-011.
- Decision texts D-RCV-28/29/36 and the D-RCV-36 CR A.5, A.7 and row 18 references are quoted
  correctly; AC2 rows, LOV-REFRESH values and the PS v6 permission letters (RW-REFADM CRUD,
  RW-DATASTEW RU, no role with A) are correct.
- Required spec sections are present (change scope, coverage, design, matrices, exceptions, API
  assessment, unit-test applicability, tests, guardrails, clarifications, status).
- **Unit-test gates planned:** Frontend `NOT_APPLICABLE` with scope evidence (Story v7 §15, no
  screen); Backend `REQUIRED`, 80% lines, branches, statements and functions on
  `th.co.scb.ace.demo.recovery.dataengine` and the changed lint code, with pass/fail cases per rule;
  integration tests kept separately. Meets `implementation-execution-gates.md` for a spec review.
- Figma `NOT_REQUIRED` is consistent with UI = NO.
- No personal data found in any specify artefact; test owner IDs are random UUIDs.

## Gate checklist

| Check | Result |
|---|---|
| Every requirement traced to a cited source or labelled assumption | FAIL (001, 002, 005, 008, 009, 010) |
| No invented requirement | FAIL (010 SOR grammar unlabelled) |
| Authentication and authorization | PASS for 403 path; approval right open (CLAR-009, GAP-E1001-08) |
| Customer and account data protection | FAIL (002) |
| Audit logging | FAIL (006) |
| Error contract consistency | FAIL (005) |
| Secrets and environment configuration | FAIL (007) |
| Dependencies only on earlier stories / repo (D-RUN-08) | FAIL (003, 004) |
| Migration number placeholder (D-RUN-07) | PASS |
| Unit-test 80% gates planned per surface | PASS |
| Test coverage and evidence planned | PASS, except BR7 (002) and X8 log (006) |
| No personal data | PASS |

## Blocking statement

STATUS: FAIL. Findings REVIEW-RWB-E1-001-001 to -009 (High and Medium) block the handoff to the
Implementation Planner. The Technical Specifier must correct `specify/` and record the new gaps and
open items in its own `document-gaps.md` and `shared-updates.md`; a second review round
(`spec-gate-review-2.md`) is required. The Low findings 010–013 must also be dispositioned in that
round.
