# Remediation plan: post-merge review REVIEW-001 (first four stories)

| Field | Value |
|---|---|
| RUN_ID | `REVIEW-001-first-four-stories` |
| Input | `code-quality-review.md` (this folder) |
| Base | `develop-recovery` at `27567ed` |
| Branch | `fix/REVIEW-001-post-merge-review`, worktree `..\rwb-wt\REVIEW-001` |
| Triage by | orchestrator (Claude Code), the same way as a code-gate triage (D-RUN-09): every finding is either fixed here or registered with an owner. None is accepted |
| Builder | implementation-builder, Opus 5.5, high effort (the fixes touch RWB-E1-042, a high-risk story under D-RUN-16) |
| Gate | compliance-reviewer code gate on the branch, `review/code-gate-review.md`, `CODE_GATE:` line |

## Fixed in this run

Each fix starts with a failing test, where a test can show the defect. The only exceptions are the CI and
CODEOWNERS edits and comment-only fixes. Commits name the owning story (`RWB-E1-042: ...`) and carry
the `AISDLC-Run: REVIEW-001-first-four-stories` trailer.

| Finding | Owning story | Fix direction |
|---|---|---|
| H1 | RWB-E1-042 | In `approve` and `rollback`, take a transaction-scoped advisory lock on every (key, environment) of the load, in sorted order, before any check. Container IT: two different loads for one key, approved concurrently, give one APPROVED and one 409, and `valid_to` stays consistent. Same for rollback racing approve |
| H2 | RWB-E1-042 | Remove the `DEV` defaults for `rwb.environment` and `RWB_ENVIRONMENT`. Bind and validate the value against `DEV`/`SIT`/`UAT`/`PROD` once (the `RecoveryMigrationProperties` pattern). Startup fails on a missing or invalid value. The local `.env.example` and test config set it explicitly |
| H3 | RWB-TE-001 | `.gitlab-ci.yml` `backend-unit` runs `recoveryCoverageVerification` |
| H4 | RWB-TE-002 | `.gitlab/CODEOWNERS` lines for `access/interim-capability-grants.csv`, `config/parameter-catalog.csv`, `infra/postgres/`, `test/resources/migration-lint/` and `flyway-fixtures/`, using owners already in the register (as D-RUN-25). Placeholder group names stay open under OPEN-038 |
| M1 | RWB-E1-042 | The `changes` list of the integration job includes `casewf/config/**` and `casewf/migration/**` |
| M4 | RWB-E1-042 | Delete `ParameterLoadRolledBack` and its publish. Nothing listens to it, and the cache is already cleared after commit |
| M5 | RWB-E1-042 | Rollback calls the decision recorder, as approve does |
| M6 | RWB-E1-042 | The readiness check logs only when its state changes. A database failure is reported as unavailable, not as missing parameters |
| M9 | RWB-E1-042 | The recursion-guard test calls back into the same cache instance, so it fails if the guard is removed |
| M10 | RWB-E1-044 | Correct the comment in `20-grants.sql.inc` to say what `SET ROLE ace_view_owner` allows. The risk itself is recorded under OPEN-051 |
| M11 | hardening `e566360` | Find why the mock sign-in sometimes returns to `/recovery`. Fix the cause and remove the `goto`, or keep it with an assertion of the URL the callback lands on, and record the reason |
| L1, L2 | RWB-E1-042 | Delete the unused repository method, the unreachable product-group branch, the uncalled service methods and the defensive branches the review lists. Only where no test or spec item needs them |
| L3 | RWB-E1-042 | Correct the Javadoc of `InterimBusinessDateProvider` |
| L9 | RWB-E1-042 | The catalog generator uses the trimmed values it validated |

## Registered, not fixed in this run (owner and reason)

Each item becomes an open item in `aisdlc/docs/open-items.md`, so it is not lost.

| Finding | Why not here | Owner |
|---|---|---|
| M2 | The bounds live in catalog rows seeded by merged migration V0001. A merged migration is never edited (AGENTS 4.6), so the change needs the next migration | Next story that adds a migration touching the catalog (RWB-E1-043, V0002) |
| M3 | Cross-pod cache consistency is a design choice for the TTL. It needs an architect's decision, not a local fix | Architect; RWB-E1-042 follow-up |
| M7 | No message table with check-level wording exists in the document set (GAP-06, Error and Message Standard v4) | Document owner (client) |
| M8 | The Temporal queue names are consumed by the workflow stories. The catalog key or the code changes with them | RWB-E3 Temporal stories |
| L4, L5, L6, L7, L8, L10, L11 | Polish or older code. No defect today | Next story that touches each file |
