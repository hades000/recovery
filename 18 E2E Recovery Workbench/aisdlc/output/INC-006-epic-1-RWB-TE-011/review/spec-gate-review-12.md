# Spec gate review, round 12: RWB-TE-011 PDPA lint for code, tests and logs

| Field | Value |
|---|---|
| RUN_ID | `INC-006-epic-1-RWB-TE-011` |
| Gate | Spec gate, re-review round 12 (Compliance Reviewer, independent of the author) |
| Earlier rounds | Round 1 `review/spec-gate-review.md` (FAIL, 2 Medium, 5 Low); round 2 `-2.md` (FAIL, 1 Medium, 1 Low); round 3 `-3.md` (FAIL, 2 Low); round 4 `-4.md` (FAIL, 3 Medium, 1 Low) with `document-gaps-4.md`; round 5 `-5.md` (FAIL, 1 Medium, 3 Low) with `document-gaps-5.md`; round 6 `-6.md` (FAIL, 4 Low); round 7 `-7.md` (FAIL, 1 Medium, 3 Low); round 8 `-8.md` (FAIL, 6 Low); round 9 `-9.md` (FAIL, 4 Low); round 10 `-10.md` (FAIL, 3 Low: SG10-01..03); round 11 `-11.md` (FAIL, 3 Low: SG11-01..03) |
| Reviewed | `specify/spec.md` (SPEC-TE011-001..018; body revised 18 Nov 2026 after round 11, header stale — SG12-02), `assumptions.md` (ASM-TE011-01..29), `document-gaps.md` (DGL-01..15, plus the run-11 note), `shared-updates.md` (§1–§5, including §3b), `gate-response.md` ("Gate response — round 11" and its self-check note), `compliance-validation.md`, `agent-run-log.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `evidence/`; the `*.run11.*` copies, compared with `git diff --no-index` |
| Direction checked | Orchestrator triage of round 11 (D-RUN-09; `AI-SDLC-BUILD-LOG.md` row 2026-11-18T06:00:08): fix exactly SG11-01..03, simplify rather than add cases, keep the change inside the existing rule text, re-gate as review-12. It is an agent's direction, not a human decision. D-RUN-06, -07, -08, -09 |
| Cross-story input (read only) | RWB-E1-042 spec revision 13 (`INC-003`; §12.3 step 3 still `DO` blocks testing `pg_constraint` with value lists, form not fixed); RWB-E1-043 revision 10 (`INC-008`; citation corrections only, R4 still RW-COMPLY and GAP-38 still "asked for nothing"); RWB-E1-044 v14-7 (`INC-001`, unchanged); RWB-TE-001 v4 (`INC-002`), RWB-TE-002 (`INC-004`), RWB-TE-003 (`INC-005`), RWB-E1-001 (`INC-009`) unchanged since round 11; `AGENTS.md` §3.7, §4.6; D-RCV-28, D-RCV-50, L-RCV-13 |
| Checked against | `.gitlab-ci.yml` (verified in full, 53 lines): no `workflow:` block and no `include:`; `backend-unit` (lines 10–19) and `frontend-check` (21–31) have no `rules:`; `backend-recovery-it` (34–53) has `rules:` at 45–50 whose first entry is `- changes:` (46–49: `backend/src/main/resources/db/**/*`, `backend/src/main/java/**/RecoveryFlywayConfig.java`, `infra/postgres/**/*`) with no `if:`, followed by `- if: $CI_PIPELINE_SOURCE == "schedule"` |
| Method | Diff of every changed file against its `run11` copy (67 insertions and 41 deletions in `spec.md`, 2 lines in `assumptions.md`, 3 values in the backend contract, 7/3 in `compliance-validation.md`, 27/3 in `gate-response.md`, 15/2 in `agent-run-log.md`, 4/1 in `shared-updates.md`, 3/0 in `document-gaps.md`). Then a full read of SPEC-TE011-008 class 3, SPEC-TE011-018 (d), the target-table rows and (e), SPEC-TE011-013, T14/T15, TS-TE011-09 and the unit rows, cross-read against ASM-TE011-26, -27, -29, CLAR-015 and the contract. Both contracts parsed as JSON. Greps of the 10 live files in `specify/` (backups excluded) for e-mail addresses and runs of 9 or more digits printed counts only (0 and 0). The CI claims were checked against the file itself, not accepted from the spec |
| Date | 2026-11-18 |
| Reviewer | Compliance Reviewer (agent) |

## 1. Result

**Overall status: FAIL**

| Severity | Count |
|---|---|
| Critical | 0 |
| High | 0 |
| Medium | 0 |
| Low | 2 |

**Round 11.** SG11-01, SG11-02 and SG11-03 are resolved. Each required fix was applied and was checked
against `spec.md`, the other artefacts and the real `.gitlab-ci.yml`, not against `gate-response.md`
alone. No finding from rounds 7–10 (or earlier) has reopened.

Two new Low findings remain. SG12-01 is in the run-11 text of two secondary artefacts: the backend
contract and ASM-TE011-26 over-broaden the placeholder exception to a placeholder *column*, which
contradicts SPEC-TE011-018 (d) and the new unit row (the specification itself is right). SG12-02 is
the spec's own revision statement, which run 11 did not update: it still says round 10 and names round
11 as next. Both are text-only and one-line fixes; neither changes a rule or a test.

Under D-RUN-09 a Low-only failure is fixed, not accepted, so the gate fails.

## 2. Disposition of round-11 findings

| Finding | Severity | Disposition | Evidence (checked against the artefacts, not against `gate-response.md` alone) |
|---|---|---|---|
| SG11-01 A `DEFAULT` through `EXECUTE` on a literal table had no target; wording did not match | Low | **Resolved.** All four required fixes are applied. The contract and ASM-TE011-26 over-broaden the exception; raised as SG12-01. | (1) SPEC-TE011-018 (d): "For a finding in a `DEFAULT` (FIXTURE-FIELD or FIXTURE-ID) on a literal column, C must also hold `ALTER TABLE <t> ALTER COLUMN <c> DROP DEFAULT` or `SET DEFAULT`; where the column is a placeholder, the write on `<t>` alone is required and code owners check the rest (the "Limit" bullet)". (2) The exception is stated once, for the table only: "except a `DEFAULT` whose table is a placeholder: with no table to write, no corrective migration accepts it (the table below; review SG11-01)". (3) The `(DML in procedural body)` row now takes "`ALTER TABLE <t> ADD COLUMN … DEFAULT` or `ALTER COLUMN … SET DEFAULT`" and repeats the column rule and the placeholder-table exception; "None only when no such table can be read". (4) The FIXTURE-ID `DEFAULT` row adds "where the column is literal". (5) One phrase in the lead sentence, both rows and the contract: "literal `EXECUTE` text or a `format` call with a literal format string". (6) Unit row "Corrective migration", **SG11-01**: `format('INSERT INTO t (c) VALUES (%L)', v)` → `t`; `format('ALTER TABLE t ADD COLUMN c text DEFAULT %L', v)` → `t` and C without both a write on `t` and `ALTER COLUMN c DROP DEFAULT` is not accepted; `format('ALTER TABLE t ADD COLUMN %I text DEFAULT ''<text>''', c)` → `t`, a write on `t` alone is accepted; `format('ALTER TABLE %I ADD COLUMN c text DEFAULT ''<text>''', t)` → a finding no corrective migration accepts. (7) ASM-TE011-26 and `shared-updates.md` §3b item 1 carry the rule. |
| SG11-02 GitLab does create merge request pipelines for this file; `pdpa-lint` was not in them | Low | **Resolved.** Verified against `.gitlab-ci.yml`, not the spec's word. | (1) The file has no `workflow:` and no `include:`; `backend-recovery-it`'s first `rules:` entry is `- changes:` (lines 46–49) with no `if:`, so an MR that changes the migration folder, `RecoveryFlywayConfig.java` or `infra/postgres/**/*` gets a merge request pipeline, and that pipeline holds `backend-recovery-it` only (`backend-unit` and `frontend-check` have no `rules:` and default to branch and tag pipelines). (2) The "no merge request pipeline" phrase is gone from all five live places: trigger note, SPEC-TE011-013, ASM-TE011-29, CLAR-015 and contract `trigger`. Each now states that today only `backend-recovery-it`'s `rules: changes:` creates a merge request pipeline. (3) SPEC-TE011-013 gives `pdpa-lint` `rules:` for `merge_request_event`, `$CI_COMMIT_BRANCH` and `$CI_COMMIT_TAG`, so the job is in branch, tag and merge request pipelines, and because one job carries a `merge_request_event` rule a merge request pipeline exists for every merge request. That is correct GitLab behaviour. (4) The merge request bullet is no longer conditional and uses the delete-then-non-fatal fetch and the `CI_MERGE_REQUEST_*` command. (5) The unit row "Changed-file list" adds the **Job rules (SG11-02)** configuration check for the three pipeline sources. (6) The duplicate-pipeline cost is noted in §4 (observation, not a finding). |
| SG11-03 (e) did not list the no-option case; "carries only files that met (e)" too broad; a failed fetch can read a stale ref | Low | **Resolved.** | (1) -018 (e): "Where the list is not built (a run without the option, for example a GitLab tag pipeline; on the target branch itself; on `main` or `develop`; or in a merge request into another target), (e) is not evaluated". (2) SPEC-TE011-013 and (e) limit the claim: "On a commit already merged into `changedFiles.targetBranch` (a promotion, or a release tag taken after the promotion) such a run carries only files that met (e) when they merged … A run without the option on any other commit (a tag on an unmerged story branch, or a manual run) is not a merge gate"; T15 and the ASM-29 risk column say the same. (3) The delete is stated in SPEC-TE011-013 for both the branch and the merge request bullet ("before the fetch the job deletes `refs/remotes/origin/<targetBranch>`"; "the same delete-then-non-fatal fetch"), in ASM-TE011-29, in CLAR-015 and in contract `inputs` ("a failed fetch leaves the target unresolved, exit 2, instead of resolving a stale ref"). (4) Unit row "Changed-file list", **Stale ref (SG11-03)**: a stale `refs/remotes/origin/develop-recovery` and a failing fetch → exit 2 `target branch … not found`, not a list built from the stale ref. |

**Regression check, rounds 7–10.**

| Earlier finding | Still resolved | Check |
|---|---|---|
| SG7-01 | Yes | Lint-fixture class untouched. SPEC-TE011-018 is still limited to the migration folder. |
| SG7-02 | Yes | Class-2 `DEFAULT` position and the `DO`-body rules are intact (SPEC-TE011-008 class 2 and class 3). |
| SG7-03 | Yes | Target-table table, scope sentence, changed-file list and `rwb.flyway.location` are all present. |
| SG7-04 | Yes | Counts unchanged (18 seed fields, 9 Restricted, 14 of 18, 526-field union); R4 owner RW-COMPLY. |
| SG8-01 | Yes | (d) still says "(a) to (c) and (e) still apply"; the placeholder-table exception is a new, stated case, not a removal of the no-target-table rule. |
| SG8-02 | Yes | The FIXTURE-ID `DEFAULT` row is kept and the "any other statement" examples are unchanged. |
| SG8-03 | Yes | The body catch-all is intact: "every other statement … one finding at its first line, with field `(DML in procedural body)`". |
| SG8-04 | Yes | The list is built in branch pipelines with `GIT_DEPTH: 0`; no merge base gives exit 2. The premise "no merge request pipeline" that review 8 stated is corrected; the SG8-04 fix itself holds. |
| SG8-05 | Yes | The E1-044 Flyway-fixture reading, "nothing asked of RWB-E1-044" and the test-root bound on lint-fixture roots are unchanged. |
| SG8-06 | Yes | TS-TE011-06 (i) still passes `--branch <feature branch>`. |
| SG9-01 to SG9-04 | Yes | SG9-01 (`INSERT`/`UPDATE` value takes the statement's table) and SG9-02 (class 3) are unchanged; SG9-03's decision rules are intact; SG9-04's status row and T10 wording are kept. |
| SG10-01 to SG10-03 | Yes | Tag pipeline and detached `HEAD` rules unchanged; SG10-02's body target-table content is retained in the enlarged row; SG10-03's only-`%I` limit, contract phrase, `%s`/`%L` forms, TS-09 (e) and unit Output row are unchanged. |

Spot checks on earlier rounds: 9 Restricted fields; 18 fields; 14 of 18; `infra/postgres/schema/**`;
(object, field) matching; no allow entry on a migration. The coverage block still reads
`TOTAL_RULES: 32` and `CONTRADICTIONS: 0`.

**The orchestrator's three SG9-03 tests, re-assessed.**

| Test | Met? | Evidence |
|---|---|---|
| (1) A promotion never fails for lack of a changed-file list | **Met.** | Tag pipelines pass no option (T15, TS-TE011-09 (l)). Branch pipelines on `main` and `develop` build no list, and their fetch is non-fatal. A promotion merge request targets another branch (TS-TE011-09 (h), (i), (j)). |
| (2) The rules that need the list run only where it is defined | **Met.** | (e) is evaluated only where the list is built (T11, contract). |
| (3) The behaviour on every other target is stated and tested | **Met.** | Tag/no option: T15, TS-TE011-09 (l), unit row. Detached `HEAD`/empty branch: T14, TS-TE011-09 (k), unit row. Manual/no-option run on an unmerged commit: stated not a merge gate in SPEC-TE011-013, (e), T15 and ASM-29. |

## 3. New findings

### REVIEW-TE011-SG12-01: The contract and ASM-TE011-26 say a placeholder *column* makes a corrective migration impossible, which the spec does not say (Low)

- **Affects:** `contracts/backend-apis.json` key `correctiveMigration`; `assumptions.md` ASM-TE011-26
  (first column). Not `spec.md`, which is correct.
- **Evidence:**
  1. **The spec accepts the column-placeholder case.** SPEC-TE011-018 (d): "where the column is a
     placeholder, the write on `<t>` alone is required and code owners check the rest". The unit row
     "Corrective migration", **SG11-01**, says the same in a test: `format('ALTER TABLE t ADD COLUMN %I
     text DEFAULT ''<text>''', c)` → target `t`, "and a write on `t` alone is accepted". Only a
     placeholder **table** is unaccepted: "a `DEFAULT` whose table is a placeholder is a finding no
     corrective migration accepts".
  2. **The contract contradicts itself.** The same value first says "where the DEFAULT column is a
     placeholder, the write on the table alone is required", then says "with ALTER COLUMN <c> DROP or
     SET DEFAULT where the DEFAULT column is literal, and with a DEFAULT on a placeholder table **or
     column** a finding no corrective migration accepts". The final clause of the same value is
     correct: "the exception is a DEFAULT whose **table** is a placeholder".
  3. **ASM-TE011-26 contradicts itself too.** "the one exception is a `DEFAULT` on a placeholder table
     **or column**, which no corrective migration accepts", then "A finding in a `DEFAULT` … also needs
     an `ALTER COLUMN … DROP DEFAULT` or `SET DEFAULT` where the column is literal; a `DEFAULT` whose
     **table** is a placeholder is a finding no corrective migration accepts".
  4. **Effect.** A planner or implementer reading the contract as the CLI rule would refuse a valid
     corrective migration for `format('ALTER TABLE t ADD COLUMN %I text DEFAULT ''<text>''', c)`, a
     false failure of exactly the kind SG9-03 and SG11-03 set out to remove. The spec still governs,
     and the failure is fail-closed, so the merge control is not weakened.
  5. **Cause.** The over-broad phrase is new in run 11; the earlier, correct sentences were kept
     beside it.
- **Required fix:** In the contract `correctiveMigration` and in ASM-TE011-26, say "a `DEFAULT` whose
  **table** is a placeholder" in both places, and delete "or column" from the exception. Keep the
  column-placeholder sentence as it stands ("the write on the table alone is required"). No change to
  `spec.md`, the unit row, compliance-validation or §3b is needed.

### REVIEW-TE011-SG12-02: The spec's revision statement still answers round 10 and names round 11 as next (Low)

- **Affects:** `spec.md` YAML front matter line 11 (`revised:`) and the `Status` row (line 25).
- **Evidence:**
  1. Line 11 reads `revised: 2026-11-18 (remediation after spec gate round 10)`.
  2. The `Status` row reads "Revised after spec gate round 10 (`review/spec-gate-review-10.md`: FAIL,
     0 Critical, 0 High, 0 Medium, 3 Low; SG10-01..SG10-03) … Next: spec gate round 11
     (`review/spec-gate-review-11.md`)".
  3. The body is the round-11 remediation: SPEC-TE011-013, -018 (d), (e) and the unit row cite
     **SG11-01..03**; `compliance-validation.md` says "revised 2026-11-18 after spec gate round 11";
     `agent-run-log.md` says "Spec remediated after round 11"; `gate-response.md` holds the round-11
     response marked "Re-review: round 12". The header is the only live statement that disagrees.
  4. **Effect.** A reader of `spec.md` alone cannot tell which gate round this text answers, and the
     traceability chain to the review is wrong. This is the "stale text" class of SG9-04 and SG10-03,
     in the one file run 11 did not refresh.
- **Required fix:** Update line 11 to "remediation after spec gate round 11", and update the `Status`
  row to record round 11 (FAIL, 0 Medium, 3 Low; SG11-01..03, all found resolved in round 12) and
  "Next: spec gate round 12 (`review/spec-gate-review-12.md`)". No other content change.

### Findings table

| ID | Severity | Finding | Affects | Required fix |
|---|---|---|---|---|
| SG12-01 | Low | Contract and ASM-TE011-26 over-broaden the placeholder exception to a placeholder column, contradicting SPEC-TE011-018 (d) and the unit row | contract `correctiveMigration`; ASM-TE011-26 | Say "placeholder table" only; delete "or column" in both |
| SG12-02 | Low | Spec's `revised:` and `Status` still say round 10 and "Next: round 11" while the body answers round 11 | `spec.md` front matter line 11 and `Status` row | Update to round 11 / next round 12 |

**Gap candidate:** none. Both findings concern this run's own artefacts, not a conflict in the document
set. `review/document-gaps-12.md` is not written.

## 4. Other checks

| Check | Result |
|---|---|
| Personal data in the artefacts | None found. No e-mail address and no run of 9 or more digits in the 10 live files in `specify/` (counts only printed: 0 and 0). Only synthetic values and placeholders are used (`SYN-…`, `<text>`, `<id>`, `V0003__rwb_e1_042_seed.sql`, `feature/x`, `case_note`). |
| Secrets | None. |
| Contracts | Both parse as JSON. `trigger` and `inputs` match SPEC-TE011-013 and the corrected pipeline facts; `inputs` carries the delete-then-fetch, the no-option/tag case and the "not a merge gate" limit. `correctiveMigration` carries SG12-01; its target table set matches the -018 rows otherwise. `fixtureMatching` is unchanged and matches SG10-03. `NO_API_CHANGE` is consistent. |
| Class 3 and SPEC-TE011-018 | Consistent. `%I` is a name placeholder; `%s`/`%L` in any form give the finding except as `COMMENT ON` text; `%%` is literal; a `DEFAULT` on a placeholder table or column gives the finding; a literal `DEFAULT` on a literal pair is a class-2 position. `format('ALTER TABLE t %s', v)` → finding; `format('ALTER TABLE t ADD COLUMN c text DEFAULT %L', v)` → `t` plus `DROP DEFAULT`; `format('ALTER TABLE %I ADD COLUMN c …', t)` → unaccepted. |
| SPEC-TE011-013, status matrix, T14/T15, TS-TE011-09, ASM-TE011-29, CLAR-015 | Agree on the decision rules, the tag/no-option case, the detached `HEAD` case and the stale-ref deletion. "Before any other check" for an undetermined branch is consistent with "decides first, before any git command". |
| `.gitlab-ci.yml` verified independently | The file is 53 lines with no `workflow:` and no `include:`. `backend-unit` and `frontend-check` have no `rules:`. `backend-recovery-it`'s first rule is `- changes:` with no `if:` (lines 46–49), then `- if: $CI_PIPELINE_SOURCE == "schedule"`. The spec's corrected statements are accurate for this file. |
| Pipeline rules (observation, not a finding) | The three rules are GitLab's documented duplicate-pipeline combination: every push to an open merge request's source branch produces a branch pipeline and a merge request pipeline, and both run `pdpa-lint`. The paragraph states both facts (branch pipelines on every branch push; a merge request pipeline for every merge request) and says the job runs in both; "a merge request that also changes those paths" is one example (where `backend-recovery-it` joins the merge request pipeline). The cost is a second lint run; the merge request shows its merge request pipeline, and the job is in it. Review 11's required fix (a) specified exactly these three rules, so no finding is raised; the plan may note the duplicate run. |
| Authorization and audit | Unchanged and appropriate for a build tool. `changedFiles.targetBranch` and `changedFiles.protectedBranches` are configuration under the code-owner entry (SPEC-TE011-014, -015). Running `git` reads repository metadata only: no database and no network (story §13, §17). |
| Unit Test Applicability | Compliant. The front end is `NOT_APPLICABLE` with evidence. The tool back end is `REQUIRED` at 80% on JaCoCo LINE, BRANCH, METHOD and INSTRUCTION, with coverage verification in the job. SG11-01's four scenarios and SG11-02's configuration check are in the unit rows; SG12-01 and SG12-02 are text-only and add no test. |
| Evidence | No new script. The claims rest on repository files, which the reviewer read directly: `.gitlab-ci.yml` (all 53 lines) and the specify artefacts. |
| Cross-story versions | RWB-E1-042 is now revision 13 (written 06:01). Its §12.3 step 3 still runs the 16 guards as `DO` blocks testing `pg_constraint` with value lists and still does not fix the form, so the "only `%I`" limit, the `%L` warning and §3b item 1 remain material. RWB-E1-043 is now revision 10 (written 07:37): citation corrections only, no design, SPEC, TC or CLAR change; R4 is still owned by RW-COMPLY and GAP-38 still says RWB-TE-011 "is asked for nothing". E1-044, TE-001, TE-002, TE-003 and E1-001 are unchanged since round 11 (write times 00:12–01:35). **Observation:** SRC-25 still cites E1-043 "revision 4" and the cross-story row is labelled "(8)". Revision 10 changes nothing this story relies on, so no finding; refresh the citation on the next edit. |
| Run decisions | D-RUN-06: the local merge gate runs `dev.ps1 test` on the story branch, where the list is built; a detached checkout fails closed with exit 2. D-RUN-07: no migration number is fixed. D-RUN-08: no dependency on a later story, and nothing is asked of RWB-E1-044. D-RUN-09: the round-11 direction is the orchestrator's, and no human disposition is claimed. The round-10 timestamp observation (build log 05:31:18 against 05:13 in the specification) stands unchanged and is for the orchestrator. |
| Data classification (pdlc stop condition) | The classification source, the residual risk, both RWB-E1-001 outcomes and the load-route limit are visible and unchanged. R4 (RW-COMPLY) is consistent with RWB-E1-043 revision 10. No open data-classification blocker belongs to this story. |
| Document gaps | No new document gap. DGL-01..15, Blocker = No for all, unchanged; `document-gaps.md` adds only the run-11 note. |

## 5. Gate output

```text
REVIEW_STATUS: FAIL
REVIEW_COUNTS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
ROUND_11_DISPOSITION: SG11-01 Resolved (literal-column vs placeholder-column rule; placeholder-table exception; DML row takes ADD COLUMN ... DEFAULT and SET DEFAULT; one phrase; four unit scenarios; ASM-26 and §3b aligned) with contract/ASM over-breadth in SG12-01. SG11-02 Resolved (verified against .gitlab-ci.yml: backend-recovery-it rules: changes: at 46-49 with no if; backend-unit/frontend-check no rules; pdpa-lint rules for merge_request_event, branch and tag; five places corrected; configuration check added). SG11-03 Resolved (no-option case in (e); claim limited to commits already merged; not-a-merge-gate stated; ref deleted before the non-fatal fetch in SPEC-013, ASM-29, CLAR-015 and the contract; stale-ref unit scenario)
ROUND_7_10_DISPOSITION: all remain Resolved; no regression
SG9-03_TRIAGE_TESTS: (1) met; (2) met; (3) met
NEW_FINDINGS: SG12-01 Low (contract correctiveMigration and ASM-TE011-26 say a DEFAULT on a placeholder "table or column" is accepted by no corrective migration, contradicting SPEC-TE011-018 (d) and the SG11-01 unit row, which accept the write on <t> alone when only the column is a placeholder; both texts also state the correct table-only rule, so each is self-contradictory); SG12-02 Low (spec.md line 11 and the Status row still say "remediation after spec gate round 10" and "Next: spec gate round 11" while the body answers SG11-01..03 and the sibling files say round 11 / round 12)
NEW_DOCUMENT_GAPS: none
CROSS_STORY_RWB-E1-042: Revision 13; section 12.3 step 3 unchanged in form and still carries value lists; only-%I limit still material
CROSS_STORY_RWB-E1-043: Revision 10 (citations only); R4 RW-COMPLY and GAP-38 intact; nothing asked of TE-011
CROSS_STORY_RWB-E1-044: Consistent with v14-7; nothing asked of it
CROSS_STORY_RWB-E1-001/-TE-001/-TE-002/-TE-003: Consistent; unchanged since round 11
BLOCKING: YES under D-RUN-09 (a Low-only failure is not accepted by the orchestrator; REVIEW_GATE_WARNING would otherwise apply)
NEXT_STEP: The orchestrator triages SG12-01 and SG12-02. Both are text-only, one-line fixes in the contract, ASM-TE011-26 and the spec header; no rule, test or design change is needed, and the plan gate should not start until they are fixed and re-gated. A Low that cannot be fixed goes to the engagement lead for a named human disposition under D-RUN-09.
```

SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
