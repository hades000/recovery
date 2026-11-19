# Compliance validation — RWB-E1-001 specification (revision 3)

Specifier self-check before spec gate round 3. The independent gate results are in `../review/`
and are summarised in §4. The run-2 self-check is kept in `compliance-validation.run2.md`, run 1 in
`compliance-validation.run1.md`.

| Field | Value |
|---|---|
| Artifact | `output/INC-009-epic-1-RWB-E1-001/specify/spec.md` (revision 3) |
| Stage | Specification remediation run 2 (pre-gate self-check, round 3) |
| Date | 2026-11-18 |
| Checked by | Technical Specifier (agent run) |
| Cross-story basis | RWB-E1-043 revision 10 (SPEC-019, -025, -026, -027, -028, -029, -030, -031, -032; `shared-updates.md` §3, §3.1, §3.2); RWB-E1-042 revision 13 (§4.3, §10.2, §12.2, §12.3); RWB-E1-044 v14-7 (SPEC-007, SPEC-015, T-044-21); RWB-TE-001 v4 (SPEC-022 (d), SPEC-025, T-TE001-14); RWB-E1-069 SPEC-015 (a), (c) |

## 1. Specification execution gates (`.github/rules/specification-execution-gates.md`)

| Gate item | Result | Where |
|---|---|---|
| `## Change Scope Declaration` with all nine fields | PASS (plus a module-scope row for the plan gate) | spec.md |
| `## Requirement-to-SPEC Logic Coverage`; every BR, AC, exception, authority, contract, plan, guardrail, out-of-scope item and NFR mapped | PASS — 33 rows, 0 missing; 3 `COVERED (ASM)` on Blocker = Yes gaps, 0 `PARTIAL`, 1 N/A row with reasons | spec.md |
| User story intent; entry trigger and preconditions | PASS | spec.md |
| Field-level behaviour matrix; status-transition matrix | PASS | spec.md |
| Exceptional-case behaviour | PASS — X1–X8 from Story v7 plus X9–X11; X4 and X10 aligned with SPEC-013 and SPEC-019 | spec.md |
| API change assessment | PASS — `NO_API_CHANGE`; the repeat is a 409 `Problem` carrying MSG-P1-011, so no `ReferenceLoad` field is added | spec.md; `contracts/backend-apis.json` |
| `## Unit Test Applicability` | PASS — frontend NO / NOT_APPLICABLE; backend YES / REQUIRED / 80% | spec.md |
| Clarification Log and status lines | PASS — 13 entries; 2 open on Blocker = Yes gaps, 1 non-blocking open | spec.md |
| Design evidence | `NOT_REQUIRED` / `NONE` | `figma/figma_report.md` |

## 2. Standards and guardrails

| Check | Result | Evidence |
|---|---|---|
| Every statement cites a source (document name and version) or a labelled assumption | PASS — source table; cross-story cites by section/SPEC/row ID; D-RUN by decision ID and timestamp, never build-log line | Sources table, `ASM-E1001-01..20`, `evidence/` scripts and outputs |
| No invented requirement; business text kept verbatim | PASS — DP07 text verbatim (`ASM-E1001-13`); SOR grammars labelled (`ASM-E1001-09`); AC9 texts verbatim | SPEC-006, -013, -015 |
| Personal-data protection never weakened | PASS — protective union (526 ≥ 18 and ≥ 523); 4 PS-v6-only marks kept; marks as INSERT literals readable by the RWB-TE-011 lint; zero lint findings is an acceptance condition; the 26 unclassified fields are listed and the two staff-identifier fields named for the ruling; no load can change a mark (E1-043 SPEC-031) | SPEC-002 T10, SPEC-006, SPEC-018; `GAP-E1001-18`; `GAP-E1001-23` |
| D-RCV-28 / D-RUN-07 migration rule | PASS — number at merge; line 1; `${recoverySchema}`; forward only | SPEC-001, -002 |
| D-RUN-12 one creator per table | PASS — T8 skips 4 tables, keeps 4 `sys_objects` + **53** `sys_fields` rows (4 + 53 = 57 comment statements) | SPEC-002, -003 |
| Handler contract conforms to the earlier story (D-RUN-08, D-RUN-11, D-RUN-18, D-RUN-20) | PASS — P4 `access.api.ReferenceTableHandler` implemented; two catalog keys supplied; no column definition, no LOV row; `PARAMETER` is E1-043's dispatcher branch; no requirement left on E1-043 | SPEC-013, -017, -019; `contracts/backend-apis.json` |
| D-RUN-13 lint | PASS — inherited from E1-044 SPEC-007 / T-044-21; SPEC-011 retired | SPEC-011 |
| D-RCV-35 / ADR-010 / D-RCV-36 | PASS — no ACE read, no constraint into `public`, no `v_ace_*` view in the migration, 18 link columns, no `payment_match_rule` | SPEC-002, -003 |
| Messages from the message seam by ID (AGENTS §3.6) | PASS — E1-042 `access.api.MessageResolver`; AC9 texts asserted verbatim | SPEC-015; TC-E1-001-09 |
| Audit (Story v7 X8) | PASS — 403 + one REFUSED `REFERENCE_LOAD_AUDIT` line (E1-043 SPEC-028) + E1-039 seam | SPEC-016; TC-E1-001-11 |
| Tests not weakened (AGENTS §4.5) | PASS — `RecoveryDatabaseIT` keeps every assertion in a new mode; earlier ITs pin a Flyway target, no assertion removed; no lint rule weakened | SPEC-010, -018 |
| No personal data | PASS — synthetic UUIDs; seed has no owner user IDs; field-ID fixture only | SPEC-006, -017, -018 |
| Shared files untouched | PASS — proposed rows in `shared-updates.md` | — |
| No human approval claimed | PASS — D-RUN-18..21 labelled orchestrator (AI) decisions, ratification OPEN-050; both blocker gaps marked as needing a human ruling before build | spec.md Status, Sources, CLAR-011/-012; assumptions.md; document-gaps.md; gate-response.md |

## 3. Known risks carried to the gate

1. Two Blocker = Yes document gaps (`GAP-E1001-17` DP07 width, `GAP-E1001-18` `is_personal`) need a
   **human** ruling before build (the merge of this story's migration); the spec proceeds on
   `ASM-E1001-13` and `-14`. No AI triage, including this self-check or the gate review, is that ruling.
2. End-to-end catalog tests depend on RWB-E1-043 revision 10 as specified (SPEC-019) and on an approver
   with Reference data A (`OPEN-NEW-2`; E1-043 adds an interim A row as its own assumption).
3. The local switch (SPEC-010) touches E1-042, E1-043, E1-044 and E1-069 artefacts; the two stale
   E1-069 SPEC-015 points are named in OPEN-NEW-9.
4. The `data_product` handler supports no rollback (`GAP-E1001-24`); a correction waits for a later
   `validFrom` unless the BA asks for rollback.
5. Ratification of D-RUN-18..21 is open (OPEN-050); a rejection would re-open the SPI placement.

## 4. Spec gate results

### Round 1 (`../review/spec-gate-review.md`, 17 Nov 2026): `FAIL`

0 Critical, 3 High, 6 Medium, 4 Low.

| ID | Severity | Summary | Revision 2 answer (`gate-response.md`) |
|---|---|---|---|
| REVIEW-RWB-E1-001-001 | High | DP07 139 > `varchar(120)`. | Blocker gap 17; `ASM-E1001-13`; seed-fits test |
| REVIEW-RWB-E1-001-002 | High | BR7 vs PDPA Inventory v4. | Blocker gap 18; `ASM-E1001-14`; TC-14, TC-17 |
| REVIEW-RWB-E1-001-003 | High | No handler seam owner. | D-RUN-11 registry; SPEC-013, -017 (re-opened as 014) |
| REVIEW-RWB-E1-001-004 | Medium | Ordering vs E1-042/043; rule (b). | D-RUN-07, -12; T8 |
| REVIEW-RWB-E1-001-005 | Medium | MSG-P1-011 type; `ReferenceLoad`. | AC10 response gap; answered in round 2 |
| REVIEW-RWB-E1-001-006 | Medium | X8 access log and approval audit. | E1-039 seam; inherited controls |
| REVIEW-RWB-E1-001-007 | Medium | Local Flyway switch unspecified. | SPEC-010 |
| REVIEW-RWB-E1-001-008 | Medium | Messages mis-cited; resolver not reused. | SPEC-015 |
| REVIEW-RWB-E1-001-009 | Medium | `rule_package` exclusion basis. | Story v7 seed list + E1-072 v7; GAP-19 |
| REVIEW-RWB-E1-001-010 to -013 | Low | SOR label; `char(n)`; `valuation_key`; NFR/PBR v2. | F1–F3 labelled; C3; 18 link columns; NFR rows |

### Round 2 (`../review/spec-gate-review-2.md`, 18 Nov 2026): `FAIL`

**0 Critical, 1 High, 3 Medium, 7 Low.** Round-1 findings: 12 of 13 resolved; 003 returned as 014.
The reviewer found GAP-E1001-17 and -18 sound, visible and protective, and noted that both still need a
human ruling (neither the AI orchestrator's triage nor the review is that ruling). The handoff to the
Implementation Planner stays blocked until round 3 (`spec-gate-review-3.md`) passes.

| ID | Severity | Summary | Revision 3 answer (`gate-response.md` §Round 2) |
|---|---|---|---|
| REVIEW-RWB-E1-001-014 | High | Registry contract contradicts E1-043; `data_product` loads refused, so AC3 and AC7–AC11 unreachable. | Re-based on E1-043 revision 10: P4 SPI implemented, `PARAMETER` a dispatcher branch (D-RUN-20), two catalog keys supplied by this story, no column definition (L12 skipped), flag-off = 422 unknown code, 404 paths are E1-043's. New SPEC-019 states what is implemented and what E1-043 calls. No requirement left on E1-043. AC3, AC7–AC11 COVERED. |
| REVIEW-RWB-E1-001-015 | Medium | AC9 owner-role message lists role codes instead of the story's wording. | K4 `{values}` restored to "the role codes in LOV-ROLE"; both AC9 texts quoted and asserted verbatim (TC-09). |
| REVIEW-RWB-E1-001-016 | Medium | K0 required-value check overlaps K2/K3; MSG-GEN-001 could lead. | K0 split into K0-H (header) and K0-R (five columns + widths); `system_of_record` and `owner_user_id` excluded; K0 never suppresses K2/K3; TC-18/19 single-defect cases expect MSG-P1-003 as `messageCode`. |
| REVIEW-RWB-E1-001-017 | Medium | E1-043 asks unanswered; dictionary load could remove the 526 marks. | Both asks withdrawn by E1-043 rev 10 and answered here (dictionary → RWB-E1-064; LOV seed unchanged). Protective rule stated: no load changes a mark; E1-064's handler refuses it and never writes the column; approver RW-COMPLY; `GAP-E1001-23`, OPEN-NEW-7/-14. |
| REVIEW-RWB-E1-001-018 | Low | 57 vs 53 `sys_fields` rows. | 53 in all places (4 + 53 = 57 comments). |
| REVIEW-RWB-E1-001-019 | Low | `character(64)` vs `char(64)`. | DF-REF-301 `char(64)`; C3 normalises `bpchar(n)` to `char(n)`; fixture updated. |
| REVIEW-RWB-E1-001-020 | Low | Blocker gap records incomplete. | 26 fields listed in GAP-18/OPEN-NEW-7; DF-REF-288/-289 named with the reason they stay `false`; LDM v8 line 561 added to GAP-17; PDPA Design v2 line 31 and why it is not a default added to GAP-18. |
| REVIEW-RWB-E1-001-021 | Low | F3 is a value list in code. | F3 is a grammar with one optional qualifier shape and no source name; basis in `ASM-E1001-09`; negative cases kept. |
| REVIEW-RWB-E1-001-022 | Low | X8 interim refusal audit unused; GAP-22 evidence wrong. | TC-11 asserts one REFUSED `REFERENCE_LOAD_AUDIT` line; GAP-22 evidence corrected (interim line exists, no access log). |
| REVIEW-RWB-E1-001-023 | Low | Stale cross-references. | SPEC-012 names post-TE-001-v4 packages (no `platform`); E1-042 rev 13, E1-043 rev 10, E1-044 v14-7, TE-001 v4; OPEN-NEW-9 and SPEC-010 name the two E1-069 SPEC-015 points. |
| REVIEW-RWB-E1-001-024 | Low | Blocker scope and D-RUN status inconsistent. | One statement: ruling needed before build (the merge of the migration); D-RUN-07..13 and -18..21 labelled orchestrator (AI) run decisions, ratification OPEN-050. |
