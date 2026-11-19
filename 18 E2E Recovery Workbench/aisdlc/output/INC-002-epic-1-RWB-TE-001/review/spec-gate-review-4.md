# Spec gate review, round 4: RWB-TE-001 (INC-002-epic-1-RWB-TE-001)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-TE-001-SPEC-008` |
| Stage | Specification gate, round 4 (re-review after the round-3 text remediation of `REVIEW-RWB-TE-001-SPEC-007`) |
| Artefact | The whole set in `specify/`: `spec.md` (v4 with round-3 text), `contracts/backend-apis.json` (v4, not edited since 00:06, before round 3), `contracts/frontend-integrations.json` (unchanged), `compliance-validation.md`, `assumptions.md`, `document-gaps.md` (unchanged since 17 Nov 23:43), `shared-updates.md`, `gate-response.md` (with "Round 3"), `agent-run-log.md`. The `*.run3.md` files were used to diff the round-3 changes. |
| Reviewer | Compliance Reviewer (agent run, `.claude/agents/compliance-reviewer.md` adapted by `aisdlc/RUN-BRIEF.md`) |
| Date | 2026-11-18 |
| Baseline | Story files v7 (RWB-TE-001 v1; RWB-E1-008 v1, -022 v1, -027 v1, -039 v1, -072 v1, -073 v1), API Specification v4 (`api/recovery-api-v4.yaml`, `x-module` tags), D-RCV-11, D-RCV-36 §3.3, `aisdlc/.github/rules/pdlc.md`. Code: `backend/src` has no file newer than `review/spec-gate-review-2.md`, so the code checks of round 3 still apply. |
| Previous rounds | `review/spec-gate-review.md` (SPEC-005, FAIL H2 M4 L4), `review/spec-gate-review-2.md` (SPEC-006, FAIL L4), `review/spec-gate-review-3.md` (SPEC-007, FAIL L2) |
| MCP | Jira, Confluence, GitLab, Figma: not connected (RUN-BRIEF rule 5). `N/A`; local files used. No git run, no code edited, no other file written. |

## Status

**`FAIL`** (Low finding only; the handoff is not blocked)

| Severity | Count | IDs |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 1 | 035 |

Findings 033 and 034 are resolved. The resolutions of 019–032 still hold: round 3 changed only the text of
SPEC-022 (d), ASM-01 and SU-01/-02/-03/-09, and added SU-14. No SPEC row, test, contract, relocation row
or status count changed. The one new finding is Low and concerns the forward note SU-14. It does not touch
the TE-001 design or its tests. Under `pdlc.md` the status stays `FAIL`, the finding stays visible, and a
human must dispose of it. The orchestrator is an AI agent and cannot give that disposition (D-RUN-09).

`REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.`

## Earlier findings

### Round 3 (033–034)

| Finding | Severity | Status | Evidence |
|---|---|---|---|
| 033: ASM-01 consequences name only E1-042/E1-043 | Low | **Resolved** (one gap in the new text, finding 035) | Fix 1: SPEC-022 (d) and ASM-01 now name RWB-E1-073 (P4 `recovery.accessadmin.rulepackages` → P3 `RuleEvaluator` / `RuleCatalog`, RG3-01) and RWB-E1-039 (P4 `AccessLogWriter` → P7 `DecisionLogWriter`). ASM-01's "Effect if wrong" now says the choice "is not a neutral choice". Fix 2: SU-02's open-item text states the sink constraint and names the E1-073, E1-039 and E1-043 placements, with two outcomes (confirm P4 and place code by the direction, or name a dependency-free home). Fix 3: SU-09 withdraws "P4 `access.rulepackages`" with the reason and offers a P3 `casewf.rules` sub-package. API v4 supports that choice: every `/admin/rule-packages…` and `/admin/rule-package-versions…` operation is tagged `x-module: P3` (lines 2815–3070). SU-14 is the forward note to E1-072, E1-073 and E1-039. I re-read story v7 E1-072 line 239, E1-073 lines 317 and 321, and E1-039 lines 222–244, and the citations match. Run-log decision 15 corrects my round-3 text: API-P7-006 (E1-039 v1 line 222) lists "errors 401, 403, 503". The `MSG-P4-002` I quoted belongs to `GET /admin/access-log` (line 218). The spec's text is the accurate one. |
| 034: stale version and test-range references | Low | **Resolved** | SU-01 now gives T-TE001-01..-14, the §13 step 7 row (SPEC-012 → T-TE001-13, HV-01, SU-13) and the published-surface row (SPEC-022 (c), -025 → T-TE001-14). These match the spec Traceability table (line 308) and the T-TE001-14 row (line 279). SU-03 reads "specified v4". The title of `compliance-validation.md` reads "specification v4", and its gate row points to this file. |

### Rounds 1 and 2 (019–032): still hold

| Finding | Still resolved? | Check made |
|---|---|---|
| 019 relocation, 030 published surface | Yes | The Relocation table, SPEC-022 (a)–(c), (e)–(h), SPEC-025 and contract `publishedTypesInitial` are unchanged (diff against `spec.run3.md`; contract mtime is before round 3). In SPEC-022 (d) the first sentence is unchanged: "`casewf.rules` → `integration.flags.api`; `casewf.admin` → `access.api`; no other". Code is unchanged since round 2. |
| 020 coverage, 024 change scope | Yes | SPEC-020, -024, the Unit Test Applicability rows and the Change Scope Declaration are unchanged. |
| 021 ACs, 025 ADR, 026 X7 | Yes | Requirement-to-SPEC and Traceability rows are unchanged. `REQUIREMENT_COVERAGE_RESULT` gives 13/13 in both files. |
| 022 BND-5, 023 BND-6 | Yes | `dochub.storage`, `clientPackages` and SPEC-003 / -021 / -026 are unchanged. |
| 027 downstream packages | Yes | SU-09 keeps the rule (move into a map module or change the map). The example that conflicted is withdrawn (033). |
| 028 identifiers | Yes | `EPIC-001` / `RWB-TE-001`; `TOTAL_RULES: 13`; `CLARIFICATION_STATUS` counts (2 open items, 9 assumptions, 1 HV) still match SU-02, SU-13, ASM-01..-09 and HV-01. SU-14 is a forward note, not an open item. |
| 029 SU-08 | Yes | SU-08 is unchanged. SU-02 now cross-refers to the E1-043 conflict it records. |
| 031 test strings, 032 step 7 | Yes | SPEC-022 (f), SPEC-012, T-TE001-06, -13 and HV-01 are unchanged. |

## New findings

### REVIEW-RWB-TE-001-035: Low. SU-14 lists only one of the three P4 → P7 edges in story v7 RWB-E1-039, so its options (a) and (b) would not remove the cycle they are offered for

- **Affects:** `shared-updates.md` SU-14 (RWB-E1-039 paragraph); to a lesser degree SPEC-022 (d), ASM-01 and SU-02, which name the same single edge.
- **Evidence:**
  - SU-14 names one edge: P4 `AccessLogWriter` calls the P7 `DecisionLogWriter`. It offers (a) P4 publishes the access event and P7 consumes it ("P7 → P4 only"), (b) move `AccessLogWriter` into P7, or (c) SU-02 names a home for the problem types that depends on no recovery module.
  - Story file v7 RWB-E1-039 v1 has two more P4 → P7 dependencies:
    1. §13 (line 244): `AccessLogQueryService` "Maps GET /admin/access-log to the P7 DecisionLogReader interface". The endpoint is P4: §13 line 239 puts it in `AccessAndAdministrationController`, and API v4 tags `getAdminAccessLog` `x-module: P4` (line 3283).
    2. §12 (lines 224–227): the published P4 interface `AccessEventPublisher` (package `recovery.access.accesslog`) is extended to `void publish(AccessEvent event) throws DecisionLogUnavailableException`. That exception is a P7 type: story v7 RWB-E1-027 v1 §12 declares it on the P7 `DecisionLogWriter` in `recovery.decision.writer` (messageId MSG-P7-003). P4's own published signature therefore imports P7. RWB-E1-022 v1 §12 (line 241) has `publish(AccessEvent event)` without it.
  - Option (a) removes only the writer call. The P4 signature and the P4 query service still depend on P7, so the P4↔P7 cycle stays whenever P7 uses a problem type. Option (b) removes the same edge only. Only option (c) covers all three edges as v7 places them. As written, the E1-039 specifier could pick (a) or (b), believe the cycle is solved, and find it only when `ModulithTest` fails.
  - `DecisionLogReader` is not defined in any story file v7. RWB-E1-008 v1 §12 lists only `append` / `verify` "inside P7", and RWB-E1-027 v1 §12 publishes only `DecisionLogWriter`. A search of `requirement/legacy/` finds the name only in E1-039 (v5–v9) and Build Notes Epic 1 v4 (line 2229). This is gap RG4-02 below.
  - Cause: my round-3 finding 033 named only the writer edge, and round 3 copied it faithfully. The omission comes from the review, not from a misreading by the specifier.
- **Required fix (text only, no design change in TE-001):**
  1. In SU-14's E1-039 paragraph, list all three P4 → P7 dependencies with their citations: E1-039 v1 §13 line 240 (writer); §13 line 244 with API v4 `x-module: P4` (query); §12 lines 224–227 with E1-027 v1 §12 (published signature).
  2. Say that options (a) and (b) remove only the writer edge. Either extend them (for example: a P4-owned exception type in place of `DecisionLogUnavailableException` on `AccessEventPublisher`, and the access-log query served from P7 or through a P7-published reader that does not make P4 a dependency of P7), or state that, as v7 places the code, only option (c) or a change to E1-039's placement removes the cycle.
  3. Point the E1-039 specifier to the missing `DecisionLogReader` definition (RG4-02).
  4. Optional: in SPEC-022 (d), ASM-01 and SU-02, change "P4 `AccessLogWriter` calls the P7 `DecisionLogWriter`" to "P4 code and P4's published `AccessEventPublisher` depend on P7 (writer, reader, exception type)".

## Checks performed

| Check | Result |
|---|---|
| Required spec sections and status lines (`specification-execution-gates.md`) | PASS. Sections and status lines are unchanged; counts match. |
| Change classification `NEW_STORY`, UI NO, Logic YES, API NO, `NO_API_CHANGE` | PASS. Unchanged. |
| BR1–BR6, AC1–AC7, X1–X7 against story v7 | PASS. Unchanged; `REQUIREMENT_COVERAGE_RESULT` 13/13 agreed. |
| Implementable against this repository | PASS. The design is unchanged and the code is unchanged since round 2. |
| Backend / frontend coverage scope and gates (80%, four metrics) | PASS (planned). Unchanged. |
| Authorization, authentication | N/A for new code. Unchanged from round 3. |
| Customer/account data protection, PDPA, personal data | PASS. Package and class names only; no personal data in the new text. |
| Audit logging, KYC/AML/consent | N/A. Build-time enabler. SU-14 option (a) correctly notes that E1-039's "in the caller's transaction" needs a synchronous `@EventListener`, because `@ApplicationModuleListener` runs after commit in a new transaction. That matters for the audit-write guarantee of E1-039 and E1-027 (`Propagation.MANDATORY`). |
| Secrets and environment configuration | PASS. Unchanged. |
| Frontend integration and error contract | PASS. Unchanged. |
| No-question rule, assumptions, open items | PASS. The orchestrator triage is attributed to Claude Code (an AI agent). No human decision is claimed. |
| Change control of this round | PASS. Backups `*.run3.md` exist. `contracts/` and `document-gaps.md` mtimes are before round 3. The diffs match the "Outputs changed" list in `agent-run-log.md` Round 3. |
| Downstream coordination (`shared-updates.md`) | Low (035) |
| Design evidence | `NOT_REQUIRED`, which is correct for UI In Scope NO |

## Document gaps found in this review

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why | How this review proceeded |
|---|---|---|---|---|---|---|
| RG4-01 | Story file v7 RWB-E1-039 v1 §12 (`AccessEventPublisher` in P4 `recovery.access.accesslog` declares `throws DecisionLogUnavailableException`) and §13 (`AccessLogWriter` → P7 `DecisionLogWriter`; `AccessLogQueryService` → P7 `DecisionLogReader`) | P4 depends on P7 in three places. If P7 uses the shared problem types (ASM-01, P4), Spring Modulith `verify()` rejects the P4↔P7 cycle (BND-3, D-RCV-11). | Story file v7 RWB-E1-027 v1 §12 (`DecisionLogUnavailableException` on the P7 `DecisionLogWriter`, `recovery.decision.writer`); API v4 `getAdminAccessLog` `x-module: P4`; API-P7-006 errors 401/403/503 (E1-008 v1 §12) | No (for RWB-TE-001) | TE-001 builds none of these. E1-039 is later in Build Sequence v6 and must settle it under D-RUN-08. The outcome also depends on SU-02. | Reported through finding 035 (SU-14 wording). The E1-039 specifier should record it in its own `document-gaps.md`. The orchestrator may add it to `aisdlc/DOCUMENT-GAPS.md`. |
| RG4-02 | Story file v7 RWB-E1-039 v1 §13 line 244 ("the P7 DecisionLogReader interface") | The interface is used but defined in no story file. | Story file v7 RWB-E1-008 v1 §12 ("Interfaces inside P7": `append`, `verify` only); RWB-E1-027 v1 §12 (publishes `DecisionLogWriter` only) | No (for RWB-TE-001) | Not TE-001's code. | Recorded for the E1-039 / E1-008 specifiers through finding 035 fix item 3. |

RG3-01 stands as reported in round 3. API v4 tags the rule-package endpoints `x-module: P3`, which also conflicts
with E1-073 v1 §13 (P4). The E1-073 specifier can cite that conflict when applying SU-09. DG-01..DG-09 in
`specify/document-gaps.md` are unchanged, evidenced and correctly dispositioned.

## Plan inputs (not findings)

Plan inputs 1–6 of `review/spec-gate-review-3.md` still apply unchanged. Round 3 added none.

## Other observations (not findings)

- SU-09 and SU-14 could cite API v4 `x-module: P3` for the rule-package operations as a second source for the
  P3 placement. Without it the text is still correct.
- SU-14 reads E1-072 v1 line 239 ("owned by the P4 package … exposed through the published interfaces") as
  P3 → P4. The sentence also allows a reading where P3 reads P4-owned tables, which AGENTS.md §3 rule 11
  forbids. SU-14 already asks E1-072 and E1-073 to settle one owner together, and that covers both readings.
- `compliance-validation.md` §1 still says the code was "read on 17 Nov 2026". The round-2 and round-3
  checks were made on 18 Nov. The code has not changed since, so this has no effect.

## Status lines

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 1]
REVIEW_GATE_WARNING: Low-severity review failure does not automatically stop this handoff; unresolved findings may carry downstream. Human disposition required.
REQUIREMENT_COVERAGE_RESULT: SUCCESS [TOTAL_RULES: 13] [COVERED_RULES: 13] [MISSING_RULES: 0] [AMBIGUOUS_RULES: 0] [CONTRADICTIONS: 0]
CHANGE_CLASSIFICATION_RESULT: NEW_STORY [UI_IN_SCOPE: NO] [LOGIC_IN_SCOPE: YES] [API_IN_SCOPE: NO] [API_IMPACT: NO_API_CHANGE] [REASON: build-time rules and package relocation without behaviour change]
DESIGN_EVIDENCE_STATUS: NOT_REQUIRED [SOURCE: NONE] [SCREENS: 0] [UNBLOCK_ACTION: n/a]
PRIOR_FINDINGS: 033-034 RESOLVED (2 of 2); 019-032 STILL RESOLVED (14 of 14)
```
