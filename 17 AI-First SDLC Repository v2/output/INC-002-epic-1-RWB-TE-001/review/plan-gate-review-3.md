---
title: "Plan gate review 3 — RWB-TE-001"
run_id: "INC-002-epic-1-RWB-TE-001"
story: "RWB-TE-001"
jira: "TB0001-1235"
review_type: "PLAN_GATE_REVIEW (re-review, gate 3)"
reviewer: "Compliance Reviewer (subagent of Implementation Planner)"
date: "2026-11-09"
---

# Plan gate review 3 — RWB-TE-001

Scope: `output/INC-002-epic-1-RWB-TE-001/plan/` (plan.md, tasks.md, data-model.md, tests/scenarios.md, contracts/*.json), `requirement/Traceability_Matrix.md` row 141, `docs/increments/INC-002-epic-1-RWB-TE-001.md`, `docs/open-items.md` OPEN-023, against `specify/spec.md` and gate reports 1 and 2. ACE evidence read-only in `ace-monorepo/` (`develop` 96b0d1c6). Nothing was edited except this report.

Human instructions 2026-11-09 applied: PRE-1 treated as APPROVED (Chitchaya Muanchonchana, TechX PO, Jira `TB0001-1235` comment 1781003, as recorded in the card); PRE-2..PRE-4 treated as PENDING; spec gate 3 Low -001, -003, -019 and the gate 2 acceptance of the -023 regex approach not re-opened.

## Gate 2 finding disposition

| ID | Sev. | Disposition | Evidence |
|---|---|---|---|
| REVIEW-RWB-TE-001-029 | Medium | **RESOLVED** | Planner's facts checked in `ace-monorepo/`: `.gitlab-ci.yml:44` (`test`) and `:63` (`test_default_branch`) run `npm ci` at the root only; `Dockerfile:10,14,16` `WORKDIR /app`, `COPY . ./`, `RUN npm ci` (root); `jenkins/buildimage_customtag.groovy` only sets the npm registry and runs `docker build`. No other build file names `frontend/package-lock.json`. `git show --stat 6f361e4a` changes `package-lock.json` and `frontend/package-lock.json` by 58 lines each. So the root lockfile is what the build installs from. TASK-15 (`tasks.md:54`), `plan.md:98`, `:180` and `contracts/frontend-integrations.json:93` now: (1) root `npm install -D --save-exact … -w frontend`; (2) `npm install --package-lock-only --workspaces=false` in `frontend/`; blocking stop rule = root lockfile holds both 4.1.12 entries and a clean root `npm ci` succeeds; frontend lockfile sync recorded, escalated in the OPEN-023 thread, no hand edit. Reviewer check on a copy of the real `frontend/package.json` + `frontend/package-lock.json` (npm 12.2.1): step 2 with no change is a byte-identical no-op (the frontend lockfile is in sync today); after adding the two exact devDependencies, step 2 writes `node_modules/vitest` 4.1.12 and `node_modules/@vitest/coverage-v8` 4.1.12 with 518 added lines and only one changed existing line (the devDependency list). So both lockfiles will be updated as SPEC-017 lists, and the stop rule is on the lockfile CI uses, as the human asked. Making the frontend sync non-blocking is acceptable: no build step reads that file, and a failure is recorded and escalated rather than hidden. |
| REVIEW-RWB-TE-001-030 | Low | **RESOLVED** | Bare `..` is the 11th import of `forbidden.ts` in TASK-16 (`tasks.md:55`), `plan.md:194`, `:203`, T-TE001-07 (`scenarios.md:19`, "11 imports") and the contract (`frontend-integrations.json:57`). Count of listed imports is 11 in each place; `allowed.ts` stays at 7. |

## New findings

| ID | Severity | Location | Maps to | Issue | Required fix |
|---|---|---|---|---|---|
| REVIEW-RWB-TE-001-031 | Low | `plan/contracts/frontend-integrations.json:27` (`forbidden`) | SPEC-014 (ii); TASK-14, -16; REVIEW-RWB-TE-001-023 | Stale since gate 1: the contract still says the rule forbids "every import starting with ../ (any depth)". The regex in the same file (`:54`) and `plan.md:194` forbid any `..` segment anywhere (`./../x`, `./sub/../../x`, bare `..`, `@/modules/recovery/../cfsc/x`). The contract describes a narrower rule than the one built and tested. | Reword to "every import with a `..` path segment anywhere (REVIEW-RWB-TE-001-023)", keeping the rest of the sentence. |
| REVIEW-RWB-TE-001-032 | Low | `docs/increments/INC-002-epic-1-RWB-TE-001.md:103` | PRE-1; GAP-006; traceability | This round recorded the Product Owner "Backlog and specification approval" as approved (`:94`, `:152`), but `:103` still says the Product Owner gates "(intake, requirements, backlog and specification, deployment) … remain `TBC`" and "The story is in delivery at the specification stage". The card now contradicts itself and the stage is out of date (plan written, plan gate running). | Drop "backlog and specification" from the `TBC` list (or say it was approved 2026-11-09, comment 1781003) and change the stage to planning. Keep CRLF line endings. |

## Regression and consistency checks (no finding)

| Check | Result |
|---|---|
| PRE-1..PRE-4 wording | Consistent: PRE-1 APPROVED with name, date and comment 1781003 in `plan.md:30`, `tasks.md:14`, `:132`, card `:94`, `:152`, matrix row 141; PRE-2 (OPEN-023), PRE-3, PRE-4 PENDING in `plan.md:31-33`, `tasks.md:14`, `:132`, card `:152`; TASK-00 still requires all four with decision and date. Contract `preconditions` lists (`backend-apis.json:405`, `frontend-integrations.json:77`) are lists of preconditions, not statuses, so not stale. Matrix row 141 says "plan approval pending OPEN-023 and plan gate" without naming FDE task approval; acceptable summary. Only the card `:103` sentence disagrees (-032). |
| Stale text after this round | No "10 imports", old single-step `--package-lock-only`, "if `frontend/package-lock.json` is unchanged, stop" left. Only the gate 1 leftover in the contract (-031). |
| Line endings | Card 157/157 CRLF, matrix 426/426 CRLF; `git diff --stat` and `--ignore-cr-at-eol` agree (card 2/2, matrix 1/1 lines). `docs/open-items.md` stays LF, 1-line diff. No regression. |
| SPEC-RWB-TE-001-001..020 → TASK | 20/20 mapped across 21 tasks (00–20), each with verification. |
| Requirement-to-SPEC rows | 17/17 `COVERED` in `plan.md` §Requirement Logic To Task Coverage; no `BLOCKED` row. |
| `BLOCKED_BY` DAG | Re-parsed from `tasks.md`: acyclic and identical to gates 1–2 (00→01→{02,03,11,13}; 03→04→{05,06}; {03,04}→07; {06,07}→08; 07→09; {02,06}→10; {05,08,09,10,11}→12; 13→{14,15}→16→17; {12,17}→{18,19}→20). |
| Unit-test gates per surface | Backend REQUIRED: JaCoCo 80% LINE/INSTRUCTION/BRANCH/METHOD, native XML/HTML (TASK-11, -12). Frontend REQUIRED: v8 80% on four metrics, `json-summary` + `lcovonly`, 0/0 recorded as printed (TASK-15, -17). Separate rows, no combined average (TASK-19). Unit-test tasks blocked by their implementation tasks. Unchanged this round. |
| SPEC-017 wording vs evidence | SPEC-017 says of `frontend/package-lock.json` "(CI runs `npm ci`)"; ACE CI runs `npm ci` at the root only. The plan follows the evidence and still edits both lockfiles, so SPEC-017 is met; the spec's parenthetical can be corrected the next time the spec is touched (not a plan defect). |
| TASK-18 footprint if the frontend sync fails | TASK-18 (1) expects the diff to equal the plan's file tables, which include `frontend/package-lock.json`. If the non-blocking sync of TASK-15 ever produced no change, TASK-18 would show a gap; TASK-15 already says to record it, so the Builder reports rather than guesses. The reviewer's run shows step 2 does update the file, so no change needed. |
| D-RCV-36 exclusions, PII/secrets, auth/audit/KYC | Unchanged: PASS / N/A. |

## Required checks summary

| Check | Result |
|---|---|
| Authentication / authorization | N/A (D-RCV-36) |
| Customer / account data protection | PASS |
| Audit logging | N/A |
| KYC/AML/suitability/consent/approval | N/A |
| Frontend integration versioning / error contract | N/A for API; lint contract text stale (-031) |
| Secrets and environment configuration | PASS |
| Plan requirement coverage | 17/17 rows, 20/20 SPEC |
| Unit-test gates planned | PASS (both surfaces, 80%, native reports) |
| Executability | PASS (-029 resolved; TASK-15 checked against the real frontend lockfile) |
| Traceability | PASS with one stale card sentence (-032) |
| Approval preconditions | PRE-1 APPROVED (human record); PRE-2, PRE-3, PRE-4 PENDING and enforced by TASK-00 |

## Status lines

```text
REVIEW_STATUS: FAIL
REVIEW_TYPE: PLAN_GATE_REVIEW
RUN_ID: INC-002-epic-1-RWB-TE-001
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 2]
REVIEW_BLOCKING: NO [REASON: Low-only findings (REVIEW-RWB-TE-001-031 stale contract text, -032 stale card sentence)]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
NEXT_STEP: Human disposition of Low REVIEW-RWB-TE-001-031 and -032 (fix or accept). REVIEW-RWB-TE-001-029 and -030 are resolved. Plan approval still needs PRE-2 (OPEN-023, ACE tech lead), then PRE-3 (FDA plan approval) and PRE-4 (FDE task approval) recorded with dates in the increment card; TASK-00 blocks the Builder until then. This review does not start Implementation Builder.
```
