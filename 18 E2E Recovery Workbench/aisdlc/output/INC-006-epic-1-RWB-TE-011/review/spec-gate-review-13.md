# Spec gate review, round 13: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 13 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 12 `review/spec-gate-review-12.md` (FAIL, 0 Medium, 2 Low: SG12-01..02); round 11 `-11.md` (FAIL, 3 Low: SG11-01..03); round 10 `-10.md` (FAIL, 3 Low: SG10-01..03); rounds 1–9 and their dispositions are recorded in `-12.md` and are not re-litigated here |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018), `assumptions.md` (ASM-TE011-01..29), `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, and the run-12 consistency edits in `compliance-validation.md`, `shared-updates.md`, `document-gaps.md`, `gate-response.md`, `agent-run-log.md` |
| Direction checked | Orchestrator direction for round 13: smallest possible diff, verify the two round-12 Lows, do not open findings for style or optional wording — only a real contradiction or a false statement. It is an agent's direction under D-RUN-09, not a human decision. |
| Method | `git diff --no-index` of every live file against its `*.run12.*` copy. Character-level comparison of contract `correctiveMigration` and the ASM-TE011-26 row (prefix/suffix match, so the inserted text is exactly the stated deletion). Both contracts parsed with `JSON.parse`. Targeted greps for `placeholder table`, `or column`, the SG11-01 unit scenarios, the SG11-02 job-rules check, the SG11-03 stale-ref scenario and the coverage block. Read of SPEC-TE011-018 (d)/(e), SPEC-TE011-008 class 3, T14/T15, TS-TE011-09 and the unit rows. |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: PASS**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 0 |

The diff is the smallest this gate has seen: two lines in `spec.md` (front matter and `Status` row only), one
deleted clause inside the contract value `correctiveMigration`, one deleted sentence in ASM-TE011-26, and
status/history updates in the five process artefacts. No rule text, test case, unit scenario, table, threshold
or classification changed. Both round-12 findings are resolved; no earlier finding has reopened.

## 2. Disposition of round-12 findings

| Finding | Severity | Disposition | Evidence (checked against the artefacts, not against `gate-response.md` alone) |
|---|---|---|---|
| SG12-01 Contract and ASM-TE011-26 over-broadened the placeholder exception to a placeholder *column* | Low | **Resolved.** The over-broad text is deleted, not rewritten; no case, example or rule was added. | (1) Contract `correctiveMigration`: the only character-level difference is the deletion of `, and with a DEFAULT on a placeholder table or column a finding no corrective migration accepts`. The value still holds the correct column-placeholder sentence ("where the DEFAULT column is a placeholder, the write on the table alone is required") and the table-only exception ("the exception is a DEFAULT whose table is a placeholder, which no corrective migration accepts"). A character scan finds no remaining `placeholder table or column` in the value. (2) ASM-TE011-26: the only difference is the deletion of the sentence "the one exception is a `DEFAULT` on a placeholder table or column, which no corrective migration accepts (review SG11-01)". The row still requires the table write and, for a `DEFAULT`, `ALTER COLUMN … DROP DEFAULT`/`SET DEFAULT` "where the column is literal", and it still states "a `DEFAULT` whose table is a placeholder is a finding no corrective migration accepts". A placeholder column therefore needs the table write alone — the rule in (d). (3) SPEC-TE011-018 (d) is unchanged and still says both things: literal column → `DROP`/`SET DEFAULT`; placeholder column → "the write on `<t>` alone is required"; placeholder table → no corrective migration accepts it. (4) The SG11-01 unit row is unchanged: `… ADD COLUMN %I text DEFAULT ''<text>''` → `t`, "a write on `t` alone is accepted"; `… ALTER TABLE %I …` → "a finding no corrective migration accepts". (5) SPEC-TE011-008 class 3 and contract `fixtureMatching` still say a `DEFAULT` whose table or column is a placeholder "gives the finding"; that is the finding rule, not the acceptance rule, and it does not conflict with (d). |
| SG12-02 The spec's revision statement answered round 10 and named round 11 as next | Low | **Resolved.** The header now names the round it answers and the next round. | (1) Line 11 reads `revised: 2026-11-18 (remediation after spec gate round 12)`. (2) The `Status` row records round 12 (`review/spec-gate-review-12.md`: FAIL, 0 Critical, 0 High, 0 Medium, 2 Low; SG12-01..02), states what changed ("text-only", the deleted clause, the header), records round 11 as "all found resolved in round 12" and round 10 as "all found resolved in round 11", and ends "Next: spec gate round 13 (`review/spec-gate-review-13.md`)". (3) The counts and dispositions match `spec-gate-review-12.md` §1 and §2. (4) `compliance-validation.md` (revised after round 12; round 12 listed as FAIL, 2 Low, remediated; round 13 pending), `gate-response.md` ("Gate response — round 12"), `agent-run-log.md` ("Remediation run after spec gate round 12") and `shared-updates.md` (round 12 listed) all agree. Nothing now points at round 10 or round 11 as current. |

## 3. Regression check

The rule-bearing text is untouched apart from the two deletions, so a reopening could only come from those
deletions. Each was checked against the requirement it serves.

| Earlier finding | Still resolved | Check |
|---|---|---|
| SG11-01 | Yes | The four unit scenarios (`%L` value, `%L` in `ADD COLUMN … DEFAULT`, `%I` column with the table write accepted, `%I` table unaccepted) and the four rule statements in SPEC-TE011-018 (d) are unchanged. The deletion removes only the extra, wrong restriction; the table-only exception survives in the spec, the contract and ASM-TE011-26. |
| SG11-02 | Yes | SPEC-TE011-013, ASM-TE011-29, CLAR-015, T15 and the contract are untouched; the "Job rules (SG11-02)" configuration check for merge request, branch and tag pipelines is still in the unit row. |
| SG11-03 | Yes | The no-option/tag case in (e), the "only files that met (e)" limit, the delete-then-non-fatal fetch and the "Stale ref (SG11-03)" scenario are unchanged. |
| SG8-01 | Yes | (d) still says a finding with no target table is met on (d) and that "(a) to (c) and (e) still apply"; ASM-TE011-26 still says the same. |
| SG7-01..SG7-04, SG8-02..SG8-06, SG9-01..SG9-04, SG10-01..SG10-03 | Yes | `spec.md` changed only at lines 11 and 25; the class list, target-table rows, body catch-all, changed-file decisions, tag rules and output text are byte-identical to the round-12 copies. Spot checks pass: 18 seed fields / 9 Restricted / 14 of 18, `TOTAL_RULES: 32`, `CONTRADICTIONS: 0`. |

## 4. Other checks

| Check | Result |
|---|---|
| Spec diff limited to the claimed lines | Confirmed: `spec.run12.md` → `spec.md` is exactly 2 insertions and 2 deletions, lines 11 and 25 (front matter and `Status`). No body, rule or test line changed. |
| Contracts parse | Both parse as JSON. `correctiveMigration` is 2,040 characters and contains the table-only exception and the column-placeholder sentence; `fixtureMatching` is unchanged. |
| Other changed files | `assumptions.md` (ASM-TE011-26 only), `compliance-validation.md` (revision and gate list), `shared-updates.md` (two status rows), `document-gaps.md` (run-12 note), `gate-response.md` (22-line round-12 response appended), `agent-run-log.md` (15-line run-12 entry). No rule content changed in any of them; `shared-updates.md` §3b still states the table-only exception. |
| Consistency of the run-12 records | `gate-response.md` and `agent-run-log.md` describe the same two deletions and the same header change as the diff; neither adds a rule or a test. One wording observation only, no effect: `agent-run-log.md` calls `shared-updates.md` "unchanged" while its two status rows were refreshed at 07:46:59; §3b, the part that carries the rule, is unchanged, so the statement is true of the rule content and no correction is required for this gate. |
| Resolved findings | None reopened; no resolved finding depended on the deleted clauses. |
| Personal data and secrets | None in the changed lines: header text and rule text only. No e-mail address, credential or real identifier; the artefacts remain synthetic (`SYN-…`, `<text>`, `V0003__…` placeholders). |
| Unit Test Applicability | Unchanged and compliant: front end `NOT_APPLICABLE` with evidence; tool back end `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION. The round-12 fixes are text-only and add no test. |
| Document gaps | None new. DGL-01..15, Blocker = No for all, unchanged; the run-12 note adds no gap. |
| Cross-story inputs | No dependency, source or cross-story statement changed, so round 12's cross-story conclusions (E1-042 revision 13, E1-043 revision 10, E1-044 v14-7, E1-001, TE-001..003) are unaffected. |

## 5. Gate output

```text
REVIEW_STATUS: PASS
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
ROUND_12_DISPOSITION: SG12-01 Resolved (over-broad placeholder "table or column" clause deleted from contract correctiveMigration and ASM-TE011-26; column-placeholder sentence and table-only exception kept; SPEC-018 (d) and SG11-01 unit row unchanged; no case added). SG12-02 Resolved (line 11 and Status row name round 12 and next round 13; counts match review 12; sibling artefacts agree)
REGRESSION: all earlier findings remain resolved; no rule, case or test changed outside the two deletions
SPEC_DIFF: 2 lines (line 11, line 25); no other spec change
CONTRACTS: both parse as JSON; correctiveMigration and fixtureMatching consistent with SPEC-TE011-018 and class 3
NEW_FINDINGS: none
NEW_DOCUMENT_GAPS: none
NEXT_STEP: PASS. The spec gate is closed for round 13; the plan gate may start. The plan should note the duplicate branch-plus-merge-request lint run recorded as an observation in round 12.
```

SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
