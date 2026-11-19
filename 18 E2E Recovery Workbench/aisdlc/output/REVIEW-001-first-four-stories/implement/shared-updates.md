# REVIEW-001 implement: proposed updates to shared files

The builder does not write the shared files. The orchestrator applies these.

## SU-01 `aisdlc/docs/open-items.md`: OPEN-051 (append a note)

REVIEW-001 M10: `GRANT ace_view_owner TO rwb_migrator WITH INHERIT FALSE, SET TRUE` lets `rwb_migrator`
run `SET ROLE ace_view_owner` and then SELECT every ACE `public` table. Any migration script can therefore
read ACE data. The comment in `infra/postgres/init/20-grants.sql.inc` now says so (commit `7481d15`).
No grant was changed. The decision stays open under OPEN-051.

## SU-02 `aisdlc/docs/open-items.md`: two proposed open items (Blocker: No)

- **Rollback decision code.** LOV-DECISION and API v4 define `AC-VERS` for a version approval only. No code
  exists for a version rollback. REVIEW-001 M5 records rollback decisions with `AC-VERS` (assumption A-01);
  since CG-R001-01 the record also carries the outcome (`APPROVED` or `ROLLED_BACK`), so a rollback no longer
  reads as an approval. Decision needed: a rollback code in LOV-DECISION, or confirm `AC-VERS` plus outcome.
  Proposed owner: analyst, with RWB-E1-008/-027.
- **Database-unavailable readiness message.** The Error and Message Standard has no message ID for "the
  parameter catalog cannot be read". REVIEW-001 M6 reports `database: unavailable` with no message code.
  Decision needed: add a message ID, or confirm status-only. Proposed owner: analyst.

## SU-03 `aisdlc/docs/open-items.md`: new item, ratify the REVIEW-001 H4 CODEOWNERS lines

The tech lead must ratify at the MR (same pattern as D-RUN-25 / IM-SU-04). The lines are in
`.gitlab/CODEOWNERS` `[Recovery module]`, all with owner `@scb-ace/techx-recovery-tech-leads`, which is
already in the register:

| Line | Path |
|---|---|
| 28 | `/backend/src/main/resources/access/interim-capability-grants.csv` |
| 29 | `/backend/src/main/resources/config/parameter-catalog.csv` |
| 30 | `/backend/src/test/resources/migration-lint/` |
| 31 | `/backend/src/test/resources/flyway-fixtures/` |
| 32 | `/infra/postgres/` (question: should `@scb-ace/ace-team` also own it?) |

This closes PROP-OI-4 (TE-002 security F5). The placeholder gate groups stay open under OPEN-038, unchanged.

## SU-04 `aisdlc/requirement/Traceability_Matrix.md`: tests added

| Finding | Story | Test |
|---|---|---|
| H1 | RWB-E1-042 | `ParameterConfigIT#concurrentApprovalsOfTwoLoadsForOneKeyAreSerialised`, `#rollbackRacingAnApprovalOfTheSameKeyIsSerialised` |
| H2 | RWB-E1-042 / RWB-TE-001 | `PlatformInfoControllerTest#aMissingEnvironmentFailsAtStartup`, `#anEnvironmentOutsideTheListFailsAtStartup` |
| H4 | RWB-TE-002 | `OwnershipResolverTest#addendumPathsHaveOwners` (five new paths) |
| M4, M5, CG-R001-01 | RWB-E1-042 | `ParameterLoadHandlerTest#rollbackRecordsTheDecision`, `#rollbackRecorderFailureIs503`, `#theDecisionRecordNamesTheOutcome` |
| M6 | RWB-E1-042 | `ParameterStartupCheckTest#aDatabaseOutageIsReportedAsUnavailable`, `#theSameStateIsLoggedOnce` |
| M9 | RWB-E1-042 | `ParameterCacheTest#theTtlReadDoesNotRecurse` (rewritten) |
| M11 | RWB-TE-001 | `frontend/src/auth/AuthCallback.test.tsx` |
| CONF-TE001-01 | RWB-TE-001 | `ModuleMapLoaderTest#duplicatePublishedIsRejected` |

## SU-05 Plan drift to record against INC-003 (RWB-E1-042)

`ParameterLoadRolledBack` (INC-003 `plan/plan.md:73` S-9, `plan/data-model.md:256`) was deleted by REVIEW-001
M4. Rollback now calls `VersionDecisionRecorder` (M5). Approve and rollback take per-(key, environment)
advisory locks (H1), taken in ascending order of the lock key (CG-R001-02). The recorder port takes the decision outcome
(CG-R001-01). `rwb.environment` has no default (H2).

## SU-06 `AI-SDLC-BUILD-LOG.md`: entry

REVIEW-001 implement: 15 review findings (H1-H4, M1, M4-M6, M9-M11, L1-L3, L9) and 2 TE-001 confirmation-gate
findings (CONF-TE001-01, -02) fixed on `fix/REVIEW-001-post-merge-review`, one commit per finding (red/green
pairs for H1, H2, M5, M6 and CONF-TE001-01). Code gate remediation: CG-R001-01 (red/green), -02 to -05.
Evidence is in `aisdlc/output/REVIEW-001-first-four-stories/implement/`.
Playwright is not run (orchestrator, after merge).

## SU-07 `AGENTS.md` §11 candidate (for the human owner)

2026-11-19: an e2e test navigated to the target page after sign-in, which hid a callback bug (REVIEW-001 M11).
Proposed rule for §4: "Never add a navigation, retry or wait to an e2e test to get past an unexplained
application state; find the cause or assert the state."

## SU-08 `aisdlc/INDEX.md`

Add `aisdlc/output/REVIEW-001-first-four-stories/implement/` (README, deviations, shared-updates, red/green
logs, final logs).
