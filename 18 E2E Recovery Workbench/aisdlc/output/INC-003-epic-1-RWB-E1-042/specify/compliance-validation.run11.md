# Compliance validation (specifier self-check): RWB-E1-042 specification, revision 12

| Field | Value |
|---|---|
| Artifact | `output/INC-003-epic-1-RWB-E1-042/specify/spec.md` (revision 12) |
| Stage | Specify (self-check before the spec gate) |
| Prepared by | Technical Specifier (agent run), 2026-11-17; revised 2026-11-18 (remediation runs 2 to 10) |
| Responds to | `REVIEW-RWB-E1-042-SPEC-012` (`review/spec-gate-review-10.md`, findings 161-162, plan inputs 1-5); see `gate-response.md` Round 10. Earlier rounds: SPEC-004 to SPEC-011 (Rounds 2-9; Round 9 with D-RUN-20 and D-RUN-21) |
| Gate review | Compliance Reviewer, `review/spec-gate-review-11.md`, REVIEW-RWB-E1-042-SPEC-013 (this self-check is not the gate) |
| Previous versions | `compliance-validation.run10.md` (revision 11), `compliance-validation.run9.md` (revision 10), `compliance-validation.run8.md` (revision 9), `compliance-validation.run7.md` (revision 8), `compliance-validation.run6.md` (revision 7), `compliance-validation.run5.md` (revision 6), `compliance-validation.run4.md` (revision 5), `compliance-validation.run3.md` (revision 4), `compliance-validation.run2.md` (revision 3) |

This file checks the spec against the specification gates (`aisdlc/.github/rules/specification-execution-gates.md`,
"Spec Validation Checklist"), the project standards (`AGENTS.md`, `aisdlc/.github/contexts/`), the RUN-BRIEF
and the run decisions D-RUN-07 to D-RUN-19 (`AI-SDLC-BUILD-LOG.md` decisions table).

## 1. Checklist

| Check | Result | Evidence |
|---|---|---|
| Change classification declared (type, UI, logic, API, impact) | PASS | spec §2; §20 `CHANGE_CLASSIFICATION_RESULT` |
| Required section headings present with the exact text (finding 128) | PASS | `## Change Scope Declaration`, `## Requirement-to-SPEC Logic Coverage`, `## Unit Test Applicability`, `## Clarification Log`, each followed by "Section N." so the numbering still reads |
| Every BR, AC, exception, flow step, precondition, transition, authority, contract, message and guardrail mapped | PASS | §6: 57 rows, all COVERED; AC1-AC11 present |
| SPEC IDs unique and defined once | PASS | §5: SPEC-RWB-E1-042-001..027; no reference outside that range |
| Each SPEC item traced to a source and a test | PASS | §5 columns "Source" and "Tests"; tests TC-01..46 (TC-35..45 new in revision 5; TC-46 new in revision 9) |
| No unresolved TODO or placeholder | PASS | `<seq>` is the D-RUN-07 placeholder by rule; the §12.2 code block uses comment lines, not `{ ... }` |
| Clarification status matches the log | PASS | 28 CLAR rows: CLAR-020 RESOLVED, CLAR-027 SETTLED by D-RUN-20 (tech-lead ratification pending, `shared-updates.md` row 39), CLAR-025 SETTLED by D-RUN-21 (ratification pending, OPEN-050), 25 OPEN, 0 blocking; CLAR-027 added in revision 9, CLAR-028 (RWB-E1-037 per-table approver keys) in revision 11; status line §20 `OPEN_ITEMS: 25` |
| Pack open items carried open (triage (e)) | PASS | CLAR-001..011; `shared-updates.md` §1 |
| Migration rule (D-RCV-28, D-RUN-07, lint) | PASS | SPEC-001; one file; `${recoverySchema}`; no number |
| Lint precondition (finding 122, D-RUN-13) | PASS | PRE-6: RWB-E1-044's identifier-only lint (E44S SPEC-007, T-044-21) must be merged; seed values not changed to suit today's lint; TC-15 "after RWB-E1-044" |
| Dependencies only on earlier stories; later work as seams (D-RUN-08) | PASS | §4.3; only RWB-E1-044 and RWB-TE-001 precede; PRE-7 (RWB-TE-001 merged; homes named); seam direction P3 → other module (A-34); access log is a seam to RWB-E1-039 (order 28), nothing built here |
| Shared reference-load endpoint owned by RWB-E1-043; published interface here (D-RUN-10, D-RUN-11) | PASS | SPEC-017, §11.2, §12.2; no controller for loads |
| Flag-off contract stated from this side (finding 119, D-RUN-11) | PASS with gap | SPEC-021, §12.12 bean table, §4.3 first seam row, E10: no `ParameterLoadHandler` bean; RWB-E1-043 uses `ObjectProvider` and refuses with 404 MSG-P4-003 (E43S SPEC-018/-026, TC-PB-01); TC-22 starts the context with the flag off; message wording unfit, gap E1042-SP-DG-10 (Blocker No); A-28 |
| Readiness on a future-dated seed (triage (f), finding 123) | PASS | SPEC-016 and §12.9: the value in force on the business date, else the generated default; every seeded key has a default, so a future seeded `valid_from` never makes readiness DOWN; cites the build log "Gate triage (late record)" item (f), build log 2026-11-18T00:09:40, RWB-E1-042 Gate triage (late record); TC-32 |
| Single metadata source (finding 121) | PASS | SPEC-005: generated `ParameterKeys` holds every metadata column, with `all()` and `byName`; `parameter_catalog` is a DB mirror; SPEC-007 default from the generated key; drift check TC-27 with a negative fixture (A-29) |
| Recorder inside the approval transaction (finding 125) | PASS | SPEC-014 transaction rule; §12.7 steps 1-7; SPEC-019; recorder `Propagation.MANDATORY`; failure rolls back, no event (`AFTER_COMMIT`); E11; TC-29 (a), (b) |
| Recorder failure answers 503 MSG-P7-003 (finding 132) | PASS | SPEC-014, SPEC-025, E11, §8, §10.2 table, §10.3 row (Standard v4 line 208), §12.7 step 5 wrap; API v4 approve 503 `E503` (lines 6028-6029); TC-29 (b) asserts status, message ID, TH text, cause; MSG-GEN-006 conflict recorded in E1042-SP-DG-11 (Blocker No), API followed |
| 503 on GET does not promise a retry (finding 126) | PASS with gap | SPEC-025, §10.2: status-only Problem, no `messageCode`; MSG-GEN-006 not used; TC-34; CLAR-019 OPEN; gap E1042-SP-DG-11 |
| `CapabilityCheck.require` behaviour (finding 120) | PASS | SPEC-020, §12.2, §12.10: `require` throws `ApiProblemException(ApiError.NOT_PERMITTED, ...)` naming the action; `has` returns a boolean; TC-24 |
| Column definitions owner (finding 127) | PASS with gap | CLAR-022: not in this catalog; keys, grammar and row check by RWB-E1-043 (E43S SPEC-003/-029); values by each table's owner story; gap E1042-SP-DG-12 |
| Concurrent identical loads (plan input P3) | PASS | SPEC-013, E12, TC-33 |
| Module placement on RWB-TE-001's homes (finding 129) | PASS | SPEC-026, §12.1 package table: `casewf.config` / `casewf.config.api` with `@NamedInterface(name = "config.api", propagate = false)` and the map entry; `MessageResolver`, `CapabilityCheck` in `access.api`, implementations in `access.internal`; flag by `@ConditionalOnProperty` (no `RecoveryFlags` / property-record change); `ApiProblemException` constructor through `access.api`; §2, §4.2 PRE-7, §4.3, §11, §12.2, §12.10, §12.11, §12.12, TC-22, TC-24, TC-45 updated; A-01 replaced; CLAR-020 resolved; RWB-E1-043 told to import from the new packages (`shared-updates.md` §1). No `platform.api` / `platform.internal` reference remains except as history |
| `used_by` grammar (finding 130) | PASS | §7.1: `;`-separated entries, each trimmed, non-empty, ≤ 100 characters; `;` absent from every seeded value (§12.4 table, checked against the pack catalog); pack comma lists rewritten; §7.5 split on `;`; TC-41 on the real seed rows plus negative fixtures; A-35 |
| Build-check and generator coverage (findings 131, 143) | PASS with recorded exception | §12.11, §14: check logic in test-scope `architecture.parameters`, measured in RWB-TE-001's one combined bundle (TE1S SPEC-020 (a), (b); E44S SPEC-014 as in force): its test-output classes added to `classDirectories` of both coverage tasks, JUnit classes excluded (or already covered by TE-001's filter); no tooling task; TC-41, -43, -44 unit tests. Gradle generator: exception with reason (build-script code outside the bundle, unmeasurable from `test` data; D-RCV-40 scope), output covered by TC-42, -26, -27; A-38 |
| Missing tests (finding 133) | PASS | TC-35 (unknown loadId incl. seeded row id), TC-36 (approve after validFrom passed), TC-37 (rollback of VALIDATED / ROLLED_BACK), TC-38 (approve of APPROVED / ROLLED_BACK), TC-39 (reason 400 / 401), TC-40 (`find` hit and miss) |
| Run log title and sections (findings 134, 142) | PASS | `agent-run-log.md` title covers revisions 3-6; run 3 and run 4 sections; the "Gate (run 3)" section was added after review 4 ran (finding 142), and "Gate (run 4)" is added after review 5 returns |
| Review-3 plan inputs 1-4 carried | PASS | §12.14 "Plan inputs" table with location and test for each: (1) own transactions, catch outside (SPEC-013, -017, §12.7, A-39); (2) ENV credential rule (SPEC-003, §7.1, TC-44); (3) rollback rebuild after commit, TTL elsewhere (SPEC-015, §12.8, TC-10); (4) handler message-ID branch in `access.internal` (§10.2, TC-30) |
| Reviewer gap candidates RV3-DG-01..03 (two citations each) | PASS | RV3-DG-01 merged into E1042-SP-DG-11 (Standard v4 lines 73, 208; API v4 lines 6028-6029); RV3-DG-02 → E1042-SP-DG-14 (story v7 line 237; RUN-BRIEF / phase0 A-01 baseline; TE1S SU-08); RV3-DG-03 → E1042-SP-DG-15 (Inventory v4 lines 676-677; Physical Schema v6 lines 4345-4346). All Blocker = No |
| Read-only and baseline literals (plan inputs P1, P2) | PASS | §12.11 HttpStatus constants and named baseline constants; SPEC-024 ENV values read through `Environment` |
| Method check on every endpoint this story exposes (AGENTS §3.3) | PASS | SPEC-020 on `GET /admin/parameters`; the load operations are not exposed here |
| No business literal in code (AGENTS §3.2, §4.8) | PASS | SPEC-004 with baseline ratchet |
| Messages by ID (AGENTS §3.6) | PASS with open item | SPEC-022; message table absent (OI-E1-042-004); the 503 is status-only by recorded decision (CLAR-019) |
| Module boundaries (AGENTS §3.11, §7) | PASS with open item | SPEC-026: P3 `casewf.config` with published `casewf.config.api`; additive P4 `access.api` seams (SU-08 (c), (d)); P3 → P4 only; two-module plan recorded as CLAR-025 / E1042-SP-DG-16; revision 11: CLAR-025 settled by D-RUN-21 (one ACE module, recovery), ratification pending (OPEN-050) |
| No new dependency (AGENTS §4.4) | PASS | §12.11 hand-written tokenizer |
| No test weakened or skipped (AGENTS §4.5) | PASS | TC-12 `Blocked`, not mocked; `RecoveryFlags` not changed; the one other story's test touched, RWB-TE-001's T-TE001-14, has its expected sets **extended** (new published types and `config.api`), nothing removed or relaxed (finding 136, TC-45, A-41) |
| Feature flag returns previous path when off (AGENTS §3.13) | PASS | SPEC-021; §12.12 |
| Backend unit-test applicability: 80% on four counters, outside `check` (findings 124, 143) | PASS | §14: LINE, INSTRUCTION, BRANCH, METHOD at 0.80, one `BUNDLE` rule (TE1S SPEC-020 (a)); `recoveryCoverageVerification` stays outside `check` (D-RCV-40 [S-24]); `test` execution data only; unit tests in `test` listed; plan input 12 withdrawn; README note recorded as gap E1042-SP-DG-13 |
| E7 raised through the published exception, no P3 call to `ProblemFactory` (finding 135) | PASS | §10.2: `ApiProblemException(HttpStatus, messageId, placeholders, field, cause)` in `access.api` (TE1S SPEC-022, -024, -025); status-only form for E7; rendered by `access.internal.ApiExceptionHandler`; no TE-001 change; SPEC-022, -025, -026; TC-30 (c), TC-34 |
| Module map and T-TE001-14 extended in the same change (finding 136) | PASS | §2, §12.1, §12.12, §12.14 T-1, T-2; TC-45 expected sets; A-40 (map has no per-type field), A-41; `shared-updates.md` §4 rev 6 row |
| Logging of the new handler branch (finding 137) | PASS | §10.2, §12.13: message ID, status, `traceId`, cause class, fixed text; no cause message, stack trace or personal data (D-RUN-15, SPEC-027); TC-29 (b), TC-30, TC-34 assert the marker is absent |
| One credential-name rule (finding 138) | PASS | SPEC-003 refers to §7.1's single rule (split on `.`, substring list, case-insensitive, no allow-list); TC-44 fixtures incl. camel case; A-44 |
| TC-10 (b) testable without weakening (finding 139) | PASS | Failure forced inside the rollback's own `REQUIRES_NEW` transaction by a test `BEFORE_COMMIT` listener on `ParameterLoadRolledBack`; same assertions (rows, version, reason, no rebuild, cache v2) |
| Two-module plan routed to the analyst (finding 140) | PASS with open item | Revision 11: CLAR-025 SETTLED by D-RUN-21, pending tech-lead ratification (OPEN-050); R7-3 changed; gap E1042-SP-DG-16 kept, Blocker = No. Before: CLAR-025 OPEN to the analyst citing AGENTS §7; continued per AGENTS §10 rule 6 and L-RCV-03; no approval claimed; P4 limited to `MessageResolver` and `CapabilityCheck` (resolver methods return `String`, no third type); E1042-SP-DG-16 quote corrected |
| RWB-E1-043 calls `casewf.config.api` from P3 (finding 141) | PASS | §4.3 first seam row, §12.1, SPEC-026, `shared-updates.md` §1 row (TE1S SU-08, SU-14; build log 2026-11-18T04:55:55, RWB-E1-043 Gate triage (run 4 under D-RUN-18)) |
| Housekeeping (finding 142) | PASS | `gate-response.md` retitled for all rounds, Round 3 claims corrected, Round 4 added; run log run 4; this file's claims |
| Review-4 plan inputs 1-6 carried | PASS | §12.14 rows R4-1..R4-6 with location and test: `@Value` flag read (SPEC-021, §12.12); unit tests in `test` (§14); bean name `capabilityCheck` (§12.10); RFC 4180 load file and unquoted hash (§7.4, §12.6, TC-16); recorder flush (SPEC-019); E43S re-check (A-28) |
| Reviewer gap candidate RV4-DG-01 | PASS | E1042-SP-DG-17 with Inventory v4 lines 652-678 and 1339, 1341 and Physical Schema v6 lines 1406, 1408, 1429, 1431; Blocker = No; `created_by` / `updated_by` personal (SPEC-027, §7.3, §17, CLAR-026, A-47) |
| Published form serves its consumers (finding 144) | PASS | §10.2: optional `detail` override and constructor guards; TC-30 (d), (e); RWB-TE-003 told (`shared-updates.md` §1 rev 7 row); A-48 |
| Business-date seam adds no cycle (finding 145; D-RUN-18) | PASS | §4.3 row: P3 → P1 read allowed under D-RUN-18 (handler SPI in P4 `access.api`, so no P1 → P3 edge); TE1S SPEC-022 (d); story file v7 RWB-E1-028 flow step 3; A-50; handler SPI implemented by RWB-E1-043 for `PARAMETER` (A-51) |
| TC-29 (b) executable (finding 146) | PASS | TC-29 (b) asserts the exception and `casewf.config` logging; rendering and handler log in TC-30 (unit) and TC-34 (MockMvc); §10.2 and §15 preamble corrected |
| `parameter_value` columns complete (finding 147) | PASS | §7.3 rows `created_at`, `created_by`, `is_active`, `state`; TC-13 extended; A-49 |
| Housekeeping (finding 148) | PASS | S-14 adds D-RUN-15 (line 38), D-RUN-17 (line 40); line range here corrected; §12.14 retitled |
| Review-5 plan inputs 1-4 carried | PASS | §12.14 rows R5-1..R5-4 |
| Audit-column tests executable (finding 149) | PASS | TC-40 asserts `created_by`, `is_active`, `state`, `created_at` on loaded rows; TC-11 asserts `created_by` kept and `updated_by` = approver; TC-13 seed only |
| Housekeeping (finding 150) | PASS | §2, §14 class-set wording removed; E43S revision 4 in the header note and S-22; S-23 lines for E44S v14-7 |
| Review-6 plan inputs 1-4 carried | PASS | §12.14 rows R6-1..R6-4; TC-30 (e) extended |
| Parameter readers outside P3 (finding 151; D-RUN-19) | PASS with open item | One caller rule in SPEC-026, §12.1, GR3; `access.api.CatalogParameterReader` defined (§12.2: methods, JDK-only exceptions, no message ID, no logging), implemented in `casewf.config`; seeded `recovery.dataengine.caselist` on it (§12.4); TC-46; T-TE001-14 set extended; shared-updates R rows to RWB-E1-011, RWB-E1-037, RWB-TE-001; CLAR-027 ratification open; gap E1042-SP-DG-18 |
| One SPI route under the flag-off contract (finding 152) | PASS | §4.3: RWB-E1-043's P3 adapter only, `ObjectProvider`, 404 MSG-P4-003; `ParameterLoadHandlerImpl` implements no `access.api` type; TC-22 (b) |
| Rollback write tested (finding 153) | PASS | TC-10 (a): `updated_by` = caller, `created_by` unchanged, `version` + 1 |
| Housekeeping (finding 154) | PASS | Build-log rows cited by timestamp and stage everywhere; A-28 and §4.3 on E43S revision 4 and its 04:55:55 triage; §20 repeat removed |
| Review-7 plan inputs 1-4 carried | PASS | §12.14 R7-1..R7-4 (R7-1 reworded by finding 155) |
| `PARAMETER` route as E43S specifies it (finding 155) | PASS with open item | §4.3, A-51, `shared-updates.md` row 32 (rev 10), R7-1, TC-22 (b): dispatcher branch `ParameterLoadBranch`, not an SPI handler, no `PARAMETER` SPI bean; E43S revision 6 cited (S-22, A-28); D-RUN-18 wording difference in CLAR-027, not decided here (revision 11: settled by D-RUN-20, ratification pending) |
| Business date for readers outside P3 (finding 156) | PASS | §12.2 `get(key, type)` on the `BusinessDateProvider` date; SPEC-023; A-54; shared-updates rev 9 R row; TC-46 |
| Key-read check for `CatalogParameterReader` (finding 157) | PASS | SPEC-003: string-literal first argument is a key read, non-literal refused; §12.2; fixtures; TC-03 (b), (c); A-55 |
| Housekeeping (finding 158) | PASS | §2 rows 82, 83; A-40; T-1; §12.1 Types column; §12.12 bean row; TC-22 flag-off reader assertion; §12.4 note under the table; run log "Gate (run 7)" section |
| Review-8 plan inputs 1-4 carried | PASS | §12.14 R8-1..R8-4 |
| Reader-call recognition rule (finding 159) | PASS | §12.11 rule (1)-(6): declared reader names per file, instance and static forms, refused forms, `Map.get`/`Optional.get` not counted, getter/chain limit stated, `CatalogParameterReaderImpl` exempt by path; no new dependency; SPEC-003; TC-03 (a)-(i); A-56 |
| Housekeeping (finding 160) | PASS | E43S definition (§1 note) now revision 6 with plan-time re-check; `assumptions.md` table continuous, final newline; R8-1 wording |
| D-RUN-20 applied (CLAR-027) | PASS with open item | §4.3, S-14, CLAR-027 SETTLED pending ratification; A-51; `shared-updates.md` rows 32, 39; no ratification recorded |
| RWB-E1-037 per-table approver keys (review-9 plan input 2) | PASS with open item | CLAR-028 OPEN; `shared-updates.md` §1 open item and §4 row to RWB-E1-037 (rev 11); nothing decided |
| Review-9 plan inputs 1-4 carried | PASS | §12.14 R9-1..R9-4 |
| Layout: every table row and heading on its own line (finding 161) | PASS | §1 S-34 to S-36 inside the sources table; `## Change Scope Declaration` heading restored; TC-04 row separate; this file's rows 26 and 27 separate; `shared-updates.md` §1 and §4 rev 11 rows inside their tables; checked by a scan for joined `|` rows and blank lines inside tables |
| Wording and provenance (finding 162) | PASS | `shared-updates.md` row 39 names three decisions ("any of them"); run log cites the orchestrator's message for the extra round; run-log step 3 lists A-33; the "Gate (run 9)" section is written |
| Review-10 plan inputs 1-5 carried | PASS | §12.14 R10-1..R10-5 |
| D-RUN-21 applied (CLAR-025) | PASS with open item | §12.1 prose, CLAR-025 SETTLED pending ratification (OPEN-050), R7-3, R8-3, R9-3, S-14; A-33; E1042-SP-DG-16 kept as the definition gap, Blocker = No; no approval recorded |
| Personal data and secrets | PASS with open item | SPEC-010, SPEC-027 (rewritten): author and approver IDs personal per Inventory v4 (protective reading over Physical Schema v6; E1042-SP-DG-15, CLAR-024); not logged, not in events, exceptions or responses; decision log only; synthetic UUIDs; ENV rows may not name credential properties (TC-44). No real name or identifier in any file of this run |
| D-RCV-35 | PASS | Workbench-owned reference data; no `public` read; no inbound load |
| D-RCV-36 | PASS | Six keys catalogued (§12.4); no Temporal or Drools call |
| Design evidence | NOT_REQUIRED | No UI (story v7 §15); §20 |
| MCP | N/A | No Jira, Confluence, GitLab or Figma MCP (RUN-BRIEF rule 5) |
| Sources cited by name, version and section, with `legacy/` path | PASS | §1 S-01..S-36 |
| No question asked | PASS | §19 header; `assumptions.md` A-01..A-56 |
| Only the stage folder written; no shared file, code, git, review file or `_v2-baseline` touched | PASS | `agent-run-log.md`; snapshots `*.run2.md` to `*.run7.md` taken before substantial edits |
| Orchestrator triage attributed to the orchestrator (Claude Code) | PASS | `gate-response.md` Round 2 §4, Rounds 3 to 7 |

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
OPEN_ITEMS: 25 recorded, 0 blocking
DOCUMENT_GAPS: none added in revision 12 (E1042-SP-DG-01..18), 0 blockers
GATE: spec gate re-run by Compliance Reviewer -> review/spec-gate-review-11.md (REVIEW-RWB-E1-042-SPEC-013)
```
