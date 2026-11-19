# Spec gate review 12: RWB-E1-042 (RUN_ID `INC-003-epic-1-RWB-E1-042`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-042-SPEC-014` |
| Gate | Specification gate, re-review of revision 13 (remediation run 11) |
| Artifacts under review | `specify/spec.md` revision 13 (1302 lines, file 2026-11-18 06:01:50), `assumptions.md` (A-01 to A-56), `document-gaps.md` (E1042-SP-DG-01 to -18), `shared-updates.md` (revision 13), `compliance-validation.md` (revision 13), `gate-response.md` (Rounds 1-11), `agent-run-log.md` (runs 1-11). No `contracts/` folder (spec §20 explains why) |
| Compared with | `review/spec-gate-review-11.md` (`REVIEW-RWB-E1-042-SPEC-013`: Lows 163, plan inputs 1-3); revision 12 snapshots `specify/*.run11.md`. All seven files were diffed in full |
| Run decisions | D-RUN-07 to D-RUN-21, `AI-SDLC-BUILD-LOG.md` decisions table lines 41-44. The build-log triage row of 2026-11-18T05:57:05 (line 318) sends revision 13 after finding 163, asks for the E43S re-baseline, and states "one further Low-only round allowed". D-RUN-18 to D-RUN-21 are orchestrator decisions, not ratified; ratification is OPEN-050 in `aisdlc/docs/open-items.md` |
| Cross-story spec read | RWB-E1-043 spec ("E43S"): revision 8 (`spec.run8.md`, file `spec.md` 2026-11-18 05:45:08) as read in run 11; revision 9 (`spec.md`, 05:58:43) checked for the names and IDs this spec consumes; E43S `shared-updates.md` R6, R24, R32, R33 and `document-gaps.md` GAP-51, GAP-57 spot-checked |
| Rules | `compliance-reviewer.md`; `.github/rules/specification-execution-gates.md`; `pdlc.md`; GitHub Flavored Markdown tables extension (escaped pipes in cells) |
| Repository | Read only; not changed by this review |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18 |
| Supersedes | `REVIEW-RWB-E1-042-SPEC-013` for revision 13. Review 11 stays as history |

## Status

**PASS** (0 Critical, 0 High, 0 Medium, 0 Low)

Finding 163 is fixed on all four items, and revision 13 changes nothing else that carries a
requirement. The diff against `spec.run11.md` (revision 12) is 25 insertions and 10 deletions: revision
provenance, the E43S citation re-baseline, S-37, §12.14 R11-1 to R11-3 and the revision-history
paragraph. No SPEC row, §6 coverage row, TC row, CLAR row, open-item count or test count changed:
27 SPEC rows, 46 TC rows and 28 CLAR rows (25 OPEN, 1 RESOLVED, 2 SETTLED) remain. Open items stay 25,
none blocking.

## 1. Finding 163: verification

| Item | Review-11 fix required | Verdict | Evidence in revision 13 |
|---|---|---|---|
| 163 (a) | Write the pipe as an escaped pipe or the word "pipe" in the finding-161 self-check row | **Fixed** | `compliance-validation.md` line 91 now ends "checked by a scan for joined rows (two pipe characters in a row) and blank lines inside tables". It has no pipe inside a code span. The scripted scan of the seven current files finds no unescaped pipe inside a code span, no `\|\|`, no table row with a cell count different from its header, and no table block without a separator |
| 163 (b) | Change "§18" to "§15" in `gate-response.md` Round 10 | **Fixed** | `gate-response.md` line 339 reads "§15 TC-03/TC-04". `spec.md` line 1067 is `## 15. Test scenarios`; line 1159 is `## 18. Out of scope` |
| 163 (c) | Insert a comma or "and" after "Round 8 SPEC-010" | **Fixed** | `gate-response.md` line 3 reads "Round 8 SPEC-010, Round 9 SPEC-011 ... Round 10 SPEC-012 and Round 11 SPEC-013" |
| 163 (d) | Update the snapshot and round ranges in the self-check | **Fixed** | `compliance-validation.md` line 106 reads "`*.run2.md` to `*.run11.md` taken before each revision's edits"; line 107 reads "Rounds 3 to 11". The last run is run 11; the last snapshot is `*.run11.md` |
| Optional | Put row 39's decisions in numeric order | Not applied | `shared-updates.md` row 39 still lists D-RUN-18, D-RUN-20 ("rev 11, below") and D-RUN-19. Review 11 called this cosmetic and optional; the inserted "(rev 11, below)" prevents the miscount the original order caused. Not a finding |

The changed rows in `compliance-validation.md` (94-97) and `gate-response.md` (345-357) accurately
describe these fixes. The self-check's claim of a scripted table check is true: a repeat scan of the
seven files returns no finding.

## 2. Revision 13 scope: layout and citations only

| Hunk in `spec.run11.md` -> `spec.md` | Reason | Requirement change |
|---|---|---|
| Front matter `revision`, `previous` | Revision provenance | None |
| `Supersedes` row | Adds revision 12 to the history | None |
| Path note for "E43S" | Revision 8, read in run 11, by ID; R11-1 added to the plan-time checks | None |
| S-22 | Re-baselines every E43S ID it cites on revision 8; records GAP-57, R24, R32, R33, E42S | Citation only |
| S-37 | Adds review 11 as source | Citation only |
| §4.3 first seam row | "E43S revision 6 GAP-57" -> "E43S GAP-57, revisions 6 to 8"; "E43S revision 6 (on disk, not yet gated)" -> "E43S revision 8 ... not yet past its gate", with TC-HD-02 added | Citation only |
| §10.2 | "E43S revision 4 SPEC-003, SPEC-025 L13" -> "E43S SPEC-003 and SPEC-025 row L13, revisions 4 to 8" | Citation only |
| §12.14 heading, R9-1, R10-1 | Extends the review range to review 11 and records the revision 8 read | Plan inputs only |
| §12.14 R11-1 to R11-3 | Three review-11 plan inputs | Plan inputs only |
| Revision-history paragraph | Records revision 13 | History only |

The diff contains no change to a SPEC statement, a coverage row, a test case, a clarification row,
an assumption's substance, an open item or a document-gap row. The companion-file diffs are limited to
their titles and history lines, the 163 fixes, the E43S re-baseline in A-28, A-48, A-51 and
`shared-updates.md` rows 32, 39 and 91, and the status revision numbers. `document-gaps.md` changes only
its title and history line. No earlier finding's fix was removed or weakened:

- 161: the Change Scope Declaration heading is on its own line; S-34 to S-37 are contiguous table rows;
  TC-03 and TC-04 are separate rows; the split self-check rows stay split.
- 162: row 39 says "all made by the orchestrator" and "if any of them changes"; the run log cites the
  orchestrator's message; A-33 is in run-log step 3; the "Gate (run 9)" section exists.
- 159, 155, 151, 156, 157, 144, 143 and the earlier findings: their SPEC, §12.11, §12.2 and test text
  is unchanged. The only changed plan-input rows are R9-1 and R10-1, and they change citations, not
  requirements.

## 3. E43S re-baseline

| Check | Result | Evidence |
|---|---|---|
| Cites the revision it read | Yes | `spec.md` line 28, S-22 (line 58) and A-28 cite revision 8 and the 05:45:08 file time, read in run 11 |
| Every cited E43S ID exists in revision 8 | Yes | `SPEC-RWB-E1-043-003`, -018, -020, -025 (row L13), -026, -027, -029, -030; `TC-PB-01`, `TC-FL-01`, `TC-HD-02`; `GAP-51`, `GAP-57`; `R24`, `R32`, `R33`; `A-15`, `A-26`: each found in `spec.run8.md` / `shared-updates.run8.md` |
| No E43S line-number citation remains in `spec.md` | Yes | A scan for "E43S" plus "line <n>" finds only S-10 (the RWB-E1-043 story file) and RWB-E1-043 story line cites in CLAR-022; no E43S line cite |
| The request to E43S is accurate | Yes | `shared-updates.md` row 91 identifies E43S revision 8's source row E42S (baselined on this spec's revision 10) and its line cites "§4.3 line 145", "§12.12 T-2, line 959" and "line 106", all of which exist in `spec.run8.md`, and asks for a re-read at revision 13 with section/row ID cites |
| E43S's `PARAMETER` route is unchanged | Yes | Revision 8 has `ParameterLoadBranch`, SPEC-026, SPEC-030 and TC-HD-02; GAP-57 is settled by D-RUN-20; the spec's §4.3, A-51 and TC-22 describe that route |
| Revision in force at plan time | Noted, not a finding | E43S revision 9 is on disk at 05:58:43 and is baselined on this spec's revision 12; it keeps every name this spec consumes (`ParameterLoadHandler`, `ParameterLoadResult`, `ParameterKeys`, `ParameterService`, `BusinessDateProvider`, `CatalogParameterReader`). Revision 13's citation to revision 8 is a true record of what run 11 read, and R11-1 re-checks the revision in force at plan time. No E43S file is changed by this stage |

## 4. D-RUN-18 to D-RUN-21

| Decision | How revision 13 applies it | Attribution and ratification |
|---|---|---|
| D-RUN-18 | §4.3 business-date seam may be filled by a P3 -> P1 read; the reference-load handler SPI is P4 `access.api`; no P1 -> P3 edge. A-50; S-14 | "made by the orchestrator, Claude Code, pending ratification by the tech lead"; S-14, A-50. No human acceptance recorded |
| D-RUN-19 | `access.api.CatalogParameterReader` is the only read path for P1, P2 and P4; implemented in P3 `casewf.config`; P3 callers keep `casewf.config.api`; no P1, P2 or P4 -> P3 edge. SPEC-026, §12.1, §12.2, TC-46 | S-14, A-52; "same maker, ratification open". No ratification recorded |
| D-RUN-20 | The P4 SPI is for handlers outside P3; `PARAMETER` is served by RWB-E1-043's dispatcher branch calling `casewf.config.api`; no `PARAMETER` SPI bean. §4.3, SPEC-021, A-51, TC-22 | S-14, CLAR-027, `shared-updates.md` rows 32, 39; "settled by D-RUN-20 (orchestrator); pending tech-lead ratification (OPEN-050)" |
| D-RUN-21 | "Touches one module" means the ACE module, recovery; the P3 + P4 plan does not go back to the analyst under AGENTS §7; the common and collection modules are untouched. CLAR-025, A-33, R7-3, R8-3, R9-3 | S-14, CLAR-025; "settled by D-RUN-21 (orchestrator); pending tech-lead ratification (OPEN-050)". No analyst or tech-lead approval claimed |

The spec treats none of the four as ratified and repeats the OPEN-050 dependency in S-14, §12.1,
§12.2, CLAR-025, CLAR-027 and R9-3/R11-3. This is correct.

## 5. Whole-spec re-read

| Check | Result |
|---|---|
| Story v7 RWB-E1-042 §1-§19 -> SPEC | 7 BRs, 11 ACs, 10 exception paths, 10 flow steps, 5 preconditions, 3 transitions, authority, 5 contract items, 7 story messages plus MSG-P4-001, and 4 guardrails are mapped: 57 of 57 rules, no gap. TC-01 to TC-46 cover them; TC-12 is Blocked by RWB-E1-022/RWB-E1-037 with a stated exit |
| Story messages | MSG-P3-032, MSG-GEN-002, MSG-P1-002, MSG-GEN-001, MSG-P7-002, MSG-P3-015 and MSG-P4-002 are in §10.3 with Standard v4 lines; MSG-P7-003, MSG-GEN-004 and MSG-P4-001/-003 are the additional messages the flow needs |
| Document set | Physical Schema v6 lines 1386-1434 (tables), 4345-4346 (`is_personal`), API v4 `getAdminParameters`/`postAdminReferenceLoads`/approve/rollback and `E503`, Error and Message Standard v4 lines 68-208, Users, Roles and Permissions v4 lines 73-110, Decision Log v10 / D-RCV-28, D-RCV-36 §3.1, Personal Data Inventory v4 lines 676-677. Spot checks agree with the spec; no new conflict |
| Required spec structure | `## Change Scope Declaration` (all ten fields), `## Requirement-to-SPEC Logic Coverage` (six columns, 57 rules), user intent (§3), triggers and preconditions (§4.1-4.2), field matrix (§7), status matrix (§8), exceptional cases (§9), API assessment (§11), `## Unit Test Applicability` (frontend and backend rows), `## Clarification Log`, and the §20 reporting block are all present with the exact required heading text |
| Unit-test applicability and 80% | Frontend: NO, both NOT_APPLICABLE, with evidence (story v7 §15; no OpenAPI change). Backend: YES, REQUIRED, one `BUNDLE` rule with LINE, INSTRUCTION, BRANCH and METHOD each at 0.80, from `test` data, outside `check` (D-RCV-40, TE1S SPEC-020); the plan lists unit tests for every changed class; the generator exception is recorded and its output is covered by TC-42/26/27. Planned, not measured, which is correct at this stage |
| Migration and data | One `V<seq>__rwb_e1_042_parameter_catalog_and_seed.sql`, no number fixed (D-RUN-07), `${recoverySchema}` only, guarded DDL, seed of 19 catalog rows and 40 value rows, drift check TC-27, no `public` read (D-RCV-35) |
| Module boundaries | P3 `casewf.config` -> P4 `access.api`; `CatalogParameterReaderImpl` in P3; P4 types do not refer to P3; no P1, P2 or P4 -> P3 edge; the `config.api` map entry and T-TE001-14 expected sets are extended, not relaxed (D-RUN-19, D-RUN-20, TE1S SPEC-004/022, TC-45) |
| Security, personal data, audit, secrets | Method check on the only exposed endpoint (SPEC-020); author, approver and audit UUIDs treated as staff identifiers, never logged or returned (SPEC-027); AC-VERS recorder inside the approval transaction (SPEC-019); secrets listed, never stored or served (SPEC-010); the 503 status-only Problem promises no retry (SPEC-025, E7) |
| Clarification and gaps | 28 CLAR rows: 25 OPEN, CLAR-020 RESOLVED, CLAR-025 and CLAR-027 SETTLED only by unratified orchestrator decisions; 18 document gaps E1042-SP-DG-01 to -18, 0 blockers; E1042-SP-DG-16 stays open |
| Revision 13 limited to layout and citations | Confirmed by the full diff: no requirement, test, clarification, assumption substance, open item or gap changed; no earlier finding reopened |

No new defect was found in the re-read. The only cosmetic residue is in the self-check's historical
cells: `compliance-validation.md` line 14 still says "D-RUN-07 to D-RUN-19", and lines 45, 74, 79, 81
and 87 name earlier E43S revisions in rows that record closed findings. These predate revision 13,
are not part of finding 163, and affect no SPEC, test, decision, open item or current-state row
(the current rows 88-98 and 106-107 are accurate). They are recorded as copy-edit residue for a later
pass, not as a gate finding.

## 6. New findings

None. No `REVIEW-RWB-E1-042-*` ID is allocated in this round; the next free ID is
`REVIEW-RWB-E1-042-164`.

| ID | Severity | Finding | Remediation |
|---|---|---|---|
| — | — | No new finding in revision 13 | — |

## 7. Document-gap candidates

None new. E1042-SP-DG-16 (the meaning of "module" in AGENTS §7) stays as recorded with Blocker = No;
D-RUN-21 settles it for this build only, pending ratification under OPEN-050. E43S GAP-59 on the
same question belongs to E43S and is consistent with it. No gap candidate is raised by revision 13.

## 8. Checks performed (compliance-reviewer.md)

| Check | Result |
|---|---|
| Authentication and authorisation | Unchanged. `GET /admin/parameters` goes through `CapabilityCheck.require` (SPEC-020); 403 MSG-P4-002; no defect |
| Customer and account data protection | Unchanged. No field, log line, event or fixture was added; author and approver IDs remain protected (SPEC-027) |
| Audit logging | Unchanged. AC-VERS is recorded inside the approval transaction (SPEC-019); no defect |
| KYC, AML, suitability, consent, approval | Out of scope beyond maker-checker (SPEC-014) |
| Frontend integration and error contract | No frontend (§13); no message ID changed; `ApiProblemException` rendering is unchanged |
| Secrets and environment configuration | Unchanged (SPEC-010, SPEC-021, TC-44, TC-46); no defect |
| AC -> requirement -> test coverage | 57 of 57 rules mapped; TC-01 to TC-46; TC-12 Blocked with an exit; no defect |
| Required spec structure | All four required headings are present with the exact text; the Change Scope Declaration has every required field; the coverage and unit-test tables have the required columns and rows |
| 80% gate per changed surface | Backend is REQUIRED with four counters at 0.80 in one `BUNDLE` rule outside `check`; frontend is `NOT_APPLICABLE` with evidence; the gate is planned, not measured |
| Migration rules (D-RCV-28, D-RUN-07) | One `V<seq>__...` file; no number fixed; `${recoverySchema}` only; no `SET search_path`, GRANT or REVOKE |
| Module boundaries (D-RUN-08, -10, -11, -18 to -21) | No new edge, type or cycle; P3 -> P4 only; `PARAMETER` is a dispatcher branch, not an SPI handler |
| Consistency with E43S | Revision 8 cited by ID; the plan re-checks the revision in force (R11-1); E43S revision 9 is noted in §3; no consumed name changed |
| Run-decision attribution and ratification | All credited to the orchestrator (Claude Code); none ratified; OPEN-050; no human acceptance recorded |
| Revision 13 limited to layout and citations | Confirmed by full diff of all seven files against `*.run11.md` |
| Personal data in this run's files | None in the revision 13 changes; test identities are synthetic UUIDs |
| MCP | None connected; N/A |

## Gate decision

```text
REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
BLOCKING: NO
EARLIER_FINDINGS: 163 resolved (a, b, c and d); 161 and 162 remain resolved; no earlier finding reopened
REGRESSIONS: none
REVISION_13_SCOPE: layout and citations only; no SPEC, CLAR, TC, assumption-substance, open-item or gap row changed; open items 25 (0 blocking); tests TC-E1-042-01 to -46
E43S: revision 8 (file 2026-11-18 05:45:08) read in run 11 and cited by ID; revision 9 on disk 05:58:43, rebound to this spec's revision 12, names unchanged; plan re-checks under R11-1
D_RUN_18_21: credited to the orchestrator (Claude Code); none ratified (OPEN-050); no human acceptance recorded
PLAN_INPUTS: 3 (R11-1 to R11-3; R10-2 to R10-5 carried)
DOCUMENT_GAP_CANDIDATES: 0
NEXT_STEP: Proceed to plan; the plan re-checks the E43S revision in force and cites D-RUN-18 to D-RUN-21 without treating them as ratified
```

SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
