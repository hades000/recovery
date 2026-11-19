# Compliance validation (specifier self-check): RWB-E1-042 specification, revision 5

| Field | Value |
|---|---|
| Artifact | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (revision 5) |
| Stage | Specify (self-check before the spec gate) |
| Prepared by | Technical Specifier (agent run), 2026-11-17; revised 2026-11-18 (remediation runs 2 and 3) |
| Responds to | `REVIEW-RWB-E1-042-SPEC-005` (`review/spec-gate-review-3.md`, findings 129-134, plan inputs 1-4, candidates RV3-DG-01..03); see `gate-response.md` Round 3. Earlier rounds: SPEC-004 (Round 2) |
| Gate review | Compliance Reviewer, `review/spec-gate-review-4.md`, REVIEW-RWB-E1-042-SPEC-006 (this self-check is not the gate) |
| Previous versions | `compliance-validation.run3.md` (revision 4), `compliance-validation.run2.md` (revision 3) |

This file checks the spec against the specification gates (`aisdlc/.github/rules/specification-execution-gates.md`,
"Spec Validation Checklist"), the project standards (`AGENTS.md`, `aisdlc/.github/contexts/`), the RUN-BRIEF
and the run decisions D-RUN-07 to D-RUN-13 (`AI-SDLC-BUILD-LOG.md` lines 30-36).

## 1. Checklist

| Check | Result | Evidence |
|---|---|---|
| Change classification declared (type, UI, logic, API, impact) | PASS | spec §2; §20 `CHANGE_CLASSIFICATION_RESULT` |
| Required section headings present with the exact text (finding 128) | PASS | `## Change Scope Declaration`, `## Requirement-to-SPEC Logic Coverage`, `## Unit Test Applicability`, `## Clarification Log`, each followed by "Section N." so the numbering still reads |
| Every BR, AC, exception, flow step, precondition, transition, authority, contract, message and guardrail mapped | PASS | §6: 57 rows, all COVERED; AC1-AC11 present |
| SPEC IDs unique and defined once | PASS | §5: SPEC-RWB-E1-042-001..027; no reference outside that range |
| Each SPEC item traced to a source and a test | PASS | §5 columns "Source" and "Tests"; tests TC-01..45 (TC-35..45 new in revision 5) |
| No unresolved TODO or placeholder | PASS | `<seq>` is the D-RUN-07 placeholder by rule; the §12.2 code block uses comment lines, not `{ ... }` |
| Clarification status matches the log | PASS | 25 CLAR rows: CLAR-020 RESOLVED, 24 OPEN, 0 blocking; CLAR-024, -025 added and CLAR-019 extended in revision 5; status line §20 `OPEN_ITEMS: 24` |
| Pack open items carried open (triage (e)) | PASS | CLAR-001..011; `shared-updates.md` §1 |
| Migration rule (D-RCV-28, D-RUN-07, lint) | PASS | SPEC-001; one file; `${recoverySchema}`; no number |
| Lint precondition (finding 122, D-RUN-13) | PASS | PRE-6: RWB-E1-044's identifier-only lint (E44S SPEC-007, T-044-21) must be merged; seed values not changed to suit today's lint; TC-15 "after RWB-E1-044" |
| Dependencies only on earlier stories; later work as seams (D-RUN-08) | PASS | §4.3; only RWB-E1-044 and RWB-TE-001 precede; PRE-7 (RWB-TE-001 merged; homes named); seam direction P3 → other module (A-34); access log is a seam to RWB-E1-039 (order 28), nothing built here |
| Shared reference-load endpoint owned by RWB-E1-043; published interface here (D-RUN-10, D-RUN-11) | PASS | SPEC-017, §11.2, §12.2; no controller for loads |
| Flag-off contract stated from this side (finding 119, D-RUN-11) | PASS with gap | SPEC-021, §12.12 bean table, §4.3 first seam row, E10: no `ParameterLoadHandler` bean; RWB-E1-043 uses `ObjectProvider` and refuses with 404 MSG-P4-003 (E43S SPEC-018/-026, TC-PB-01); TC-22 starts the context with the flag off; message wording unfit, gap E1042-SP-DG-10 (Blocker No); A-28 |
| Readiness on a future-dated seed (triage (f), finding 123) | PASS | SPEC-016 and §12.9: the value in force on the business date, else the generated default; every seeded key has a default, so a future seeded `valid_from` never makes readiness DOWN; cites the build log "Gate triage (late record)" item (f), timeline line 140; TC-32 |
| Single metadata source (finding 121) | PASS | SPEC-005: generated `ParameterKeys` holds every metadata column, with `all()` and `byName`; `parameter_catalog` is a DB mirror; SPEC-007 default from the generated key; drift check TC-27 with a negative fixture (A-29) |
| Recorder inside the approval transaction (finding 125) | PASS | SPEC-014 transaction rule; §12.7 steps 1-7; SPEC-019; recorder `Propagation.MANDATORY`; failure rolls back, no event (`AFTER_COMMIT`); E11; TC-29 (a), (b) |
| Recorder failure answers 503 MSG-P7-003 (finding 132) | PASS | SPEC-014, SPEC-025, E11, §8, §10.2 table, §10.3 row (Standard v4 line 208), §12.7 step 5 wrap; API v4 approve 503 `E503` (lines 6028-6029); TC-29 (b) asserts status, message ID, TH text, cause; MSG-GEN-006 conflict recorded in E1042-SP-DG-11 (Blocker No), API followed |
| 503 on GET does not promise a retry (finding 126) | PASS with gap | SPEC-025, §10.2: status-only Problem, no `messageCode`; MSG-GEN-006 not used; TC-34; CLAR-019 OPEN; gap E1042-SP-DG-11 |
| `CapabilityCheck.require` behaviour (finding 120) | PASS | SPEC-020, §12.2, §12.10: `require` throws `ApiProblemException(ApiError.NOT_PERMITTED, ...)` naming the action; `has` returns a boolean; TC-24 |
| Column definitions owner (finding 127) | PASS with gap | CLAR-022: not in this catalog; keys, grammar and row check by RWB-E1-043 (E43S SPEC-003/-029); values by each table's owner story; gap E1042-SP-DG-12 |
| Concurrent identical loads (plan input P3) | PASS | SPEC-013, E12, TC-33 |
| Module placement on RWB-TE-001's homes (finding 129) | PASS | SPEC-026, §12.1 package table: `casewf.config` / `casewf.config.api` with `@NamedInterface(name = "config.api", propagate = false)` and the map entry; `MessageResolver`, `CapabilityCheck` in `access.api`, implementations in `access.internal`; flag by `@ConditionalOnProperty` (no `RecoveryFlags` / property-record change); `ApiProblemException` constructor through `access.api`; §2, §4.2 PRE-7, §4.3, §11, §12.2, §12.10, §12.11, §12.12, TC-22, TC-24, TC-45 updated; A-01 replaced; CLAR-020 resolved; RWB-E1-043 told to import from the new packages (`shared-updates.md` §1). No `platform.api` / `platform.internal` reference remains except as history |
| `used_by` grammar (finding 130) | PASS | §7.1: `;`-separated entries, each trimmed, non-empty, ≤ 100 characters; `;` absent from every seeded value (§12.4 table, checked against the pack catalog); pack comma lists rewritten; §7.5 split on `;`; TC-41 on the real seed rows plus negative fixtures; A-35 |
| Build-check and generator coverage (finding 131) | PASS with recorded exception | §12.11, §14: check logic in test-scope `architecture.parameters`, in the TOOLING class set (E44S SPEC-014; D-RCV-43 (2); TE1S SPEC-020 (b)), `recoveryToolingCoverageVerification` 0.80 on four counters; TC-41, -43, -44 unit tests. Gradle generator: exception with reason (build-script code outside both class sets, unmeasurable from `test` data; D-RCV-40 scope), output covered by TC-42, -26, -27; A-38 |
| Missing tests (finding 133) | PASS | TC-35 (unknown loadId incl. seeded row id), TC-36 (approve after validFrom passed), TC-37 (rollback of VALIDATED / ROLLED_BACK), TC-38 (approve of APPROVED / ROLLED_BACK), TC-39 (reason 400 / 401), TC-40 (`find` hit and miss) |
| Run log title and sections (finding 134) | PASS | `agent-run-log.md` title covers revisions 3-5; run 3 and gate sections appended |
| Review-3 plan inputs 1-4 carried | PASS | §12.14 "Plan inputs" table with location and test for each: (1) own transactions, catch outside (SPEC-013, -017, §12.7, A-39); (2) ENV credential rule (SPEC-003, §7.1, TC-44); (3) rollback rebuild after commit, TTL elsewhere (SPEC-015, §12.8, TC-10); (4) handler message-ID branch in `access.internal` (§10.2, TC-30) |
| Reviewer gap candidates RV3-DG-01..03 (two citations each) | PASS | RV3-DG-01 merged into E1042-SP-DG-11 (Standard v4 lines 73, 208; API v4 lines 6028-6029); RV3-DG-02 → E1042-SP-DG-14 (story v7 line 237; RUN-BRIEF / phase0 A-01 baseline; TE1S SU-08); RV3-DG-03 → E1042-SP-DG-15 (Inventory v4 lines 676-677; Physical Schema v6 lines 4345-4346). All Blocker = No |
| Read-only and baseline literals (plan inputs P1, P2) | PASS | §12.11 HttpStatus constants and named baseline constants; SPEC-024 ENV values read through `Environment` |
| Method check on every endpoint this story exposes (AGENTS §3.3) | PASS | SPEC-020 on `GET /admin/parameters`; the load operations are not exposed here |
| No business literal in code (AGENTS §3.2, §4.8) | PASS | SPEC-004 with baseline ratchet |
| Messages by ID (AGENTS §3.6) | PASS with open item | SPEC-022; message table absent (OI-E1-042-004); the 503 is status-only by recorded decision (CLAR-019) |
| Module boundaries (AGENTS §3.11, §7) | PASS with open item | SPEC-026: P3 `casewf.config` with published `casewf.config.api`; additive P4 `access.api` seams (SU-08 (c), (d)); P3 → P4 only; two-module plan recorded as CLAR-025 / E1042-SP-DG-16 for the tech lead |
| No new dependency (AGENTS §4.4) | PASS | §12.11 hand-written tokenizer |
| No test weakened or skipped (AGENTS §4.5) | PASS | TC-12 `Blocked`, not mocked; existing tests unchanged (`RecoveryFlags` not changed, so no other module's test is touched) |
| Feature flag returns previous path when off (AGENTS §3.13) | PASS | SPEC-021; §12.12 |
| Backend unit-test applicability: 80% on four counters, outside `check` (finding 124) | PASS | §14: LINE, INSTRUCTION, BRANCH, METHOD at 0.80 (E44S SPEC-014); `recoveryCoverageVerification` and `recoveryToolingCoverageVerification` stay outside `check` (D-RCV-40 [S-24]); `test` execution data only; plan input 12 withdrawn; README note recorded as gap E1042-SP-DG-13 |
| Personal data and secrets | PASS with open item | SPEC-010, SPEC-027 (rewritten): author and approver IDs personal per Inventory v4 (protective reading over Physical Schema v6; E1042-SP-DG-15, CLAR-024); not logged, not in events, exceptions or responses; decision log only; synthetic UUIDs; ENV rows may not name credential properties (TC-44). No real name or identifier in any file of this run |
| D-RCV-35 | PASS | Workbench-owned reference data; no `public` read; no inbound load |
| D-RCV-36 | PASS | Six keys catalogued (§12.4); no Temporal or Drools call |
| Design evidence | NOT_REQUIRED | No UI (story v7 §15); §20 |
| MCP | N/A | No Jira, Confluence, GitLab or Figma MCP (RUN-BRIEF rule 5) |
| Sources cited by name, version and section, with `legacy/` path | PASS | §1 S-01..S-28 |
| No question asked | PASS | §19 header; `assumptions.md` A-01..A-39 |
| Only the stage folder written; no shared file, code, git, review file or `_v2-baseline` touched | PASS | `agent-run-log.md`; snapshots `*.run2.md` and `*.run3.md` taken before substantial edits |
| Orchestrator triage attributed to the orchestrator (Claude Code) | PASS | `gate-response.md` Round 2 §4 and Round 3 |

## 2. Residual risks (not findings)

| Risk | Handling |
|---|---|
| Interface-level tests of load, approve and rollback do not exercise HTTP | RWB-E1-043 adds HTTP tests (`shared-updates.md` §1); refusals already carry message ID and status |
| Cross-instance refresh relies on the TTL until RWB-TE-006 | Stated in FL8 and §12.8 |
| Owners, used-by and ranges of new keys are assumptions | Labelled A-07..A-10; CLAR-018 |
| RWB-TE-001 not merged when this story's branch is cut | PRE-7: the plan stops and waits; RWB-TE-001's current run changes only SU-14 (direction rule), which §4.3 follows |
| The data protection owner may classify author and approver differently | SPEC-027 is the stricter reading; a looser decision removes restrictions only |
| RWB-E1-043's parallel revision may change the flag-off refusal | A-28: E43S governs; this spec only guarantees that the bean is absent and the context starts |
| Repeat approve differs between the two stories on the shared endpoint (409 here, 200 in RWB-E1-043 §12) | Recorded by RWB-E1-043 as GAP-35; owner decision; `shared-updates.md` §4 |
| PRE-6 depends on RWB-E1-044 merging first | Build Sequence order 1; TC-15 marked "after RWB-E1-044" |

## 3. Result

```text
SELF_CHECK: PASS (0 Critical, 0 High, 0 Medium open against the checklist)
OPEN_ITEMS: 24 recorded, 0 blocking
DOCUMENT_GAPS: E1042-SP-DG-11 extended, E1042-SP-DG-14 to -16 added, 0 blockers
GATE: spec gate re-run by Compliance Reviewer -> review/spec-gate-review-4.md (REVIEW-RWB-E1-042-SPEC-006)
```
