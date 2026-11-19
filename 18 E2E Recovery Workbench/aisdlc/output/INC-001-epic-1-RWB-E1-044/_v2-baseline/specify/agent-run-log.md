# Technical Specifier run log — RWB-E1-044

**Run:** `INC-001-epic-1-RWB-E1-044` (re-specification, 2026-11-09)
**Agent:** Technical Specifier (`.github/agents/specify.agent.md`)
**Status:** SPECIFIED — clarifications closed 2026-11-09; spec gate result in §6

## 1. Why re-specified

The spec in this folder was BA's 5 Nov 2026 version from the 20261109 package. It still used
`RWB_SCHEMA`/`${schema}`, `spring.flyway.*`, `recovery/src/main/resources/db/migration/recovery`, a
pipeline drift gate and `MigrationRunRecorder`, which conflict with D-RCV-03/-05/-12/-17/-18/-28 and
the OPEN-007/-013/-014 rulings applied in CTX-UPDATE-006. Git history keeps the earlier version.

## 2. Inputs read

Increment card INC-001; EPIC-001 tailoring; story file v5 (canonical, D-RCV-35); `.github/contexts/`
(backend-context §13, backend-standards BS-2, testing-standards TS-RCV-*, project-context);
`docs/decisions/INC-001-decisions.md`; `docs/open-items.md` (OPEN-018..020);
`docs/architecture/migration-merge-order-map.md`; rules (pdlc, specification-execution-gates);
`ace-monorepo` `develop` 96b0d1c6: `AppConfig.java`, `SampleModuleConfig.java`, `application.yaml`,
`build.gradle.kts`. The archived squad attempt-02 spec was consulted only as the record of the
tech-lead rulings it cites.

## 3. Classification

`NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE]`;
Frontend NO; Backend YES.

## 4. Questions and answers (2026-11-09)

| CLAR | Answer | By |
|---|---|---|
| CLAR-001 BR7 drift gate vs D-RCV-05 | A — park the environment gate; container comparison | Product Owner Chitchaya Muanchonchana (Internal PO TechX), Jira `TB0001-1205` comment 1781236 |
| CLAR-002 job monitor parts (D-RCV-12) | A — defer to the job-monitor story | As CLAR-001 |
| CLAR-003 package before RWB-TE-001 | A — create only `recovery.casewf.internal.migration` | Recovery tech lead (Jesniphat Pukkham) |
| CLAR-004 MSG-P3-016 text source | A — message ID + parameters only | Recovery tech lead (Jesniphat Pukkham) |

CLAR-005..-010 resolved from recorded decisions (see spec Clarification Log).

## 5. Status

```text
SPEC_STATUS: BLOCKED
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE]
REQUIREMENT_COVERAGE_RESULT: FAILURE [TOTAL_RULES: 7] [COVERED_RULES: 6] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 1] [CONTRADICTIONS: 1]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
SPEC_CLARIFICATION_STATUS: BLOCKED [OPEN_ITEMS: 2]
REVIEW_STATUS: NOT_RUN (spec gate runs after clarification)
NEXT_STEP: Product Owner Rajdeep Ghai answers CLAR-001 and CLAR-002 (OPEN-018); re-run /specify INC-001-epic-1-RWB-E1-044.
```

## 6. Re-run 2026-11-09 (Product Owner answers, ACE re-check)

- Recorded CLAR-001 A and CLAR-002 A (Jira `TB0001-1205` comment 1781236, 15:19, read via Jira MCP);
  updated SPEC-012, -013, coverage table, X1, flag row, T-044-02, TC-E1-044-10, contracts.
- ACE `develop` 96b0d1c6 → eedf5c75: `AppConfig.java`, `SampleModuleConfig.java`,
  `backend/build.gradle.kts`, `ModulithTest.java` unchanged; `application.yaml` +6 lines under `iam`
  only; `db-migrate` profile unchanged. Core `db/migration` now has duplicate versions 24–27:
  T-044-14 baseline rule and OPEN-025.
- SPEC-015 (d): RWB-TE-001 adds JaCoCo first (INC-002 plan TASK-11, `executionData` from `test`);
  E1-044 adds `recoveryIntegrationTest` execution data; fallback per D-RCV-43 (2).
- OPEN-018 Product Owner part settled; BA story-text update stays open. OPEN-025 added.
- No build or test run. Nothing committed.
- Spec gate 2026-11-09: **FAIL** — 2 Medium (REVIEW-RWB-E1-044-001 T-044-02 not run by `check`, PO
  told it runs in the build; -002 local-start path also matches core `db-migrate` step), 8 Low (-003..-010).
  Report: `output/INC-001-epic-1-RWB-E1-044/review/spec-gate-review.md`. Handoff blocked.
- Remediation 2026-11-09 per recovery tech lead: D-RCV-44 (-001), D-RCV-45 (-002), D-RCV-46 (-009) recorded;
  Low -003..-008 fixed; OPEN-026 (Docker on build agents), OPEN-027 (PO re-confirm BR7 run rule) added.
  INC-001 and EPIC-001 cards updated. Spec gate 2 run.
- Spec gate 2 2026-11-09: FAIL, Low only (-011..-015); 001–010 closed. -011 fixed by recording the result. REVIEW_GATE_WARNING emitted.

## 7. Re-run 2026-11-10 (D-RCV-47, gate 2 remediation)

- Applied D-RCV-47 (schema `ace` from the connection, prefix `rwb_`, no `${recoverySchema}`, no schema property):
  SPEC-001, -002, -004 (d), -005, -006, -007 (prefix lint), -012, -018; field matrix; X9, X10; T-044-03, -05, -12, -15;
  CLAR-005, CLAR-007; contracts CON-001/-002 rewritten.
- Gate 2: -012 card notes; -013 DEV in scope; -014 runner fail-fast and T-044-12 case; -015 to OPEN-029 (Context
  Updater with OPEN-022).
- ACE `develop` re-read at 9f450bbd: shared files unchanged, core duplicates renumbered; OPEN-025 settled.
- Registers: open-items (OPEN-025 settled, OPEN-029 added, settled table header fixed); decisions annotations on
  D-RCV-45, OPEN-003, -006, -014.
- Spec gate 3: FAIL, blocking (High -016, Medium -017, Low -018..-021). Report `review/spec-gate-review-r3.md`.
- No build or test run. Nothing committed.

## 8. Re-run 2026-11-10 (D-RCV-48, gate 3 remediation)

- Recorded D-RCV-48 (recovery tech lead): `baselineVersion("0")` + `baselineOnMigrate(true)` as `SampleModuleConfig`,
  `createSchemas(false)` explicit. Applied to SPEC-001, -002, -003, X12, status-transition matrix, BR6 row, T-044-01,
  -03, -12, -15, new T-044-16, CLAR-005, CON-001. D-RCV-47 annotated; next free number D-RCV-49 (register, CLAUDE.md).
- -018: SPEC-007 (5) prefix on every table/sequence/index identifier in any statement, catalog allow-list; T-044-05; X10; CON-002.
- -019: SPEC-007 (6) `GRANT`/`REVOKE` ban; SPEC-005 / Authorization default-privilege note; OPEN-019 same-role condition; X11.
- -020: OPEN-029 due before `/planner INC-001-epic-1-RWB-E1-044`, scope extended. -021 accepted by the recovery tech lead.
- ACE `develop` 9f450bbd re-read: `SampleModuleConfig` lines 24–27; `db/migration-env/<env>/V001.001__grant_permission.sql`.
- No build or test run. Nothing committed.
- Spec gate 4: FAIL, Low only (-022..-025), not blocking; -016..-021 closed. Report `review/spec-gate-review-r4.md`. REVIEW_GATE_WARNING emitted.
