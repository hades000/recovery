# Compliance validation — RWB-TE-002 specification (specifier self-check)

| Field | Value |
|---|---|
| Artefact | `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (remediation run 3, aligned to RWB-TE-001 v4) |
| Stage | Specification, self-check before the gate |
| Author | Technical Specifier (agent run), 2026-11-17; run 3 2026-11-18 |
| Gate of record | `review/spec-gate-review-4.md` (Compliance Reviewer). This file is not a gate result. |
| Previous gates | `REVIEW-RWB-TE-002-SG-2026111701` — `FAIL` 0C/2H/6M/3L; `REVIEW-RWB-TE-002-SG-2026111702` — `FAIL` 0C/0H/0M/5L (SG-012–SG-016); `REVIEW-RWB-TE-002-SG-2026111703` — `FAIL` 0C/0H/0M/1L (SG-017); responses in `gate-response.md` (Rounds 1–3) |

## 1. Checked against

- Story Files v7, RWB-TE-002 v1 (`requirement/legacy/04-user-stories/recovery-workbench-user-stories-epic-1-story-files-v7_extracted/rwb-te-002-code-owners-for-the-recovery-module-v1.md`) §1–§19.
- Engineering Practices v5 §4.2, §7, §10; AI Assisted Development Approach v1 §3, §6; Decision Log v10 DL04, DL05, DL36, DL37; Test Cases v7 row TC-TE-002-08; Story Defects v4 row 91.
- `aisdlc/docs/decisions/decision-register.md` (D-RCV-10, -19, -21, -37, -50; L-RCV-03, -12, -13); `AI-SDLC-BUILD-LOG.md` D-RUN-01, D-RUN-05.
- `aisdlc/.github/rules/specification-execution-gates.md`, `implementation-execution-gates.md`, `security-quality-standards.md`, `traceability-standards.md`, `pdlc.md`; `aisdlc/.github/contexts/testing-standards.md`, `backend-standards.md`, `backend-context.md`, `project-context.md`.
- `aisdlc/evidence/phase0-standards-audit.md` A-05, A-10; this repository's file tree on 2026-11-17 and 2026-11-18 (no git command run in this stage).
- Run 3: RWB-TE-001 spec v4 (`output/INC-002-epic-1-RWB-TE-001/specify/spec.md`, SPEC-001, -002, -006, -007, -011, -014, -015, -020, -022 and the relocation table; `assumptions.md` ASM-05; `shared-updates.md`) and its gate `review/spec-gate-review-5.md` (`PASS`); `AI-SDLC-BUILD-LOG.md` timeline 2026-11-17T23:55:06 (SG-017 triage).

## 2. Checks

| Check | Result | Evidence |
|---|---|---|
| Required spec sections present | PASS | Change Scope Declaration; Requirement-to-SPEC Logic Coverage; intent; trigger/preconditions; field matrix; status-transition matrix; exceptional cases; API assessment; Unit Test Applicability. |
| Change classification | PASS | `NEW_STORY`; UI NO; Logic YES; API NO / `NO_API_CHANGE`; Frontend NO; Backend YES (test-scope only). |
| Coverage rows have SPEC IDs and no `BLOCKED` | PASS | 38 rows (run 2 adds story §13 "Done when"); every SPEC ID is defined in the SPEC catalogue (SG-007). |
| SPEC IDs unique and defined | PASS | SPEC-RWB-TE-002-001 to -019, one catalogue row each. |
| Host-only clauses not claimed as tested | PASS | "Verification here" column; HV-01–HV-11 `OPEN — NOT_TESTED_HERE` (SG-001, pdlc.md). `TESTED_LOCALLY` means "runs in `./scripts/dev.ps1 test`" only; the CI job and its coverage gate are `DEFINED_HERE_RUN_ON_HOST`, run in a pipeline under HV-07 (SG-012). |
| Local completion state | PASS | SPEC-018 and "Local completion state (story §13)": `BUILT — ACCEPTANCE PENDING HV-01..HV-11`, never Done; OPEN-038 open, visible in the merge record as a merge condition; `PROP-OI-1` (e) moves its "Needed by" (SG-015). |
| Merge record named (SG-017) | PASS | Carrier = local merge commit message + `aisdlc/output/INC-004-epic-1-RWB-TE-002/README.md`; writer = the orchestrator at merge (D-RUN-06; triage 2026-11-17T23:55:06); exact sentence and heading; checks before and after the merge; ACE host wording kept (SPEC-017; Local completion state; `shared-updates.md` §5). |
| Aligned to RWB-TE-001 v4 | PASS | Recovery main/test directory patterns cover the 19 modules incl. `casewf`, `dochub`; no removed baseline package named; module map path equal to TE-001 v4 SPEC-002; new `[Recovery module]` lines for `ModulithTest.java` (SPEC-007), fixture root and fixture maps (SPEC-011), `frontend/eslint.config.js` (SPEC-014); UT-14 uses relocated paths; UT-26 asserts every boundary control (ASM-TE002-18). |
| Control-file and build-file ownership | PASS | V12 rejects duplicate section names without regard to case (UT-23); UT-18 asserts two sections with disjoint owners per BR4 file (SG-013). Root build files and `scripts/dev.ps1` owned in `[Pipeline gates]` (UT-25, SG-014). |
| No fixed migration number | PASS | UT-15 uses the synthetic resolver input `V9999__rwb_te_002_resolver_fixture.sql`, never written to disk (D-RUN-07, SG-016). |
| Every pattern names a path of this repository or is reserved/preconditioned | PASS | Path basis table: all exist except the common pattern (reserved, SPEC-004) and the TE-001 module map, fixture maps folder and fixture root (precondition P1; fixture root substituted at plan time, V9/UT-26 fail otherwise). |
| No invented person or team handle | PASS | Two story handles `ASSUMED`; two `@role-placeholder/…` markers for document-set roles, `PLACEHOLDER`, OPEN-038. No person, e-mail or membership list. |
| Unit-test applicability matches scope | PASS | Frontend NO / NOT_APPLICABLE with evidence; Backend YES / REQUIRED, 80% LINE, BRANCH, INSTRUCTION, METHOD on the codeowners package. |
| Positive and negative tests per rule | PASS | V1–V12 each have failing and passing cases (UT-01–UT-12, UT-23); resolver UT-13–UT-20, UT-25, UT-26; job definition UT-24. |
| Audit items A-05, A-10 | PASS | Covered or excluded with reason and receiving owner (SPEC-015, -016, -017, -019). |
| Source conflicts recorded | PASS | SP-DG-01 to SP-DG-10, none blocking; precedence applied. |
| Shared files untouched | PASS | Proposals only, in `shared-updates.md`. |
| No new dependency | PASS (with plan check) | SnakeYAML assumed present on the test compile and runtime classpaths (ASM-TE002-09); fallback named. |
| PII / secret scan of outputs | PASS | No personal data, credential, token or production data; synthetic paths and the story's synthetic typo handle only. |
| Design evidence | N/A | `DESIGN_EVIDENCE_STATUS: NOT_REQUIRED` (UI NO). |
| No question asked | PASS | L-RCV-03; eleven CLAR items settled by sources, labelled assumptions or the orchestrator's logged triage. |

## 3. Residual risks carried to the gate

| Risk | Handling |
|---|---|
| GitLab section semantics are assumed, not verified (no host). | ASM-TE002-11; HV-03, HV-08. |
| The module map, fixture maps and fixture root do not exist until RWB-TE-001 merges; the fixture root path is named by TE-001's plan. | Precondition P1; plan-time substitution; V9 and UT-26 stop signals. |
| GitLab tier for code-owner approval unknown. | ASM-TE002-15; `PROP-OI-1`. |

```text
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 38] [COVERED_RULES: 38] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: repository review control; test-scope backend code only]
SELF_CHECK: PASS — gate decision belongs to review/spec-gate-review-4.md
```
