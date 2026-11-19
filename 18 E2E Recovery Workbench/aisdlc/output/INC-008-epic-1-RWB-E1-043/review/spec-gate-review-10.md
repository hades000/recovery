# Spec gate review, round 10: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-010` |
| Gate | Specification gate, round 10 (Compliance Reviewer, bounded review after remediation run 9) |
| Artefacts reviewed | `specify/spec.md` revision 10 (file 2026-11-18 07:48:54), `assumptions.md` revision 10 (07:49:06, A-01..A-46, A-32 withdrawn), `document-gaps.md` revision 10 (07:39:14, GAP-01..GAP-59), `shared-updates.md` revision 10 (07:49:11, R1..R33, §3.1, §3.2), `compliance-validation.md` revision 10 (07:39:53), `contracts/backend-apis.json` revision 10 (07:45:24), `contracts/frontend-integrations.json` revision 8 (content unchanged), `gate-response.md` revision 10 (07:49:21, §13), `agent-run-log.md` (run 9, 07:45:43). `spec.run9.md` was diffed against the current spec as the audit trail. |
| Previous round | `review/spec-gate-review-9.md` (`REVIEW-RWB-E1-043-SPEC-009`, FAIL: 0 Critical, 0 High, 0 Medium, 2 Low, findings 159-160) |
| Sources checked | `AI-SDLC-BUILD-LOG.md` (file 2026-11-18 07:51:47, 350 lines at read): decisions table rows 41-44 (D-RUN-18..21), row 305 (Gate triage of 2026-11-18 05:52:36), row 335 (RWB-E1-042 round-12 PASS), row 336 (this story's round-9 FAIL), row 337 (Gate triage of 2026-11-18 07:33:17). RWB-E1-042 `specify/`: live `spec.md` revision 13 (1302 lines, file 06:01:50) and kept revision 12 `spec.run11.md` (1287 lines, file 05:57:12); `assumptions.md` (06:01:34) and `shared-updates.md` (05:59:47), both headed revision 13; `review/spec-gate-review-12.md` (PASS, 0C/0H/0M/0L). `aisdlc/docs/open-items.md` OPEN-050. Story file v7 RWB-E1-043. `AGENTS.md` §7, §9. `specification-execution-gates.md`; `pdlc.md`. All read only. |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-09, D-RUN-18..21 and the Gate triage rows of 2026-11-18 05:52:36 and
07:33:17 were given by the orchestrator (Claude Code), an AI agent. They are not human decisions,
acceptance or ratification, and this review does not treat them as such. A search of the reviewed
artefacts for ratification, acceptance, approval and "settled" wording found only disclaimers or
explicitly qualified statements. D-RUN-21, D-RUN-18 and D-RUN-20 are still qualified as unratified
with OPEN-050; no tech-lead approval is claimed.

## Status

**`SPEC_GATE: PASS`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 0 | |
| Low | 0 | |

Both round-9 findings are resolved. The revision-10 diff is citation-only: no design, SPEC, TC,
CLAR, assumption-substance, contract or validation statement changed, and no resolved finding is
reopened. No new finding is opened for citation placement or wording, per this round's terms.

## Round-9 findings: resolution check

| Round-9 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| `REVIEW-RWB-E1-043-159` (build-log line 304 vs 305) | Low | **Resolved** | Every build-log pointer in the current spec set is now a timestamp, story and stage citation. A scan of `spec.md`, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `gate-response.md`, `agent-run-log.md` and both contract files found no `AI-SDLC-BUILD-LOG.md` line number used as a pointer. The 05:52:36 row is cited in `spec.md:8`, `:52`, `:738`, `:1145`; A-24 (`assumptions.md:39`), A-46 (`:61`); GAP-57/58/59 (`document-gaps.md:87-89`); R1 (`shared-updates.md:72`), R22 (`:93`), R24 (`:95`), R32 (`:103`), R33 (`:104`); `compliance-validation.md:29, 65-66`; `gate-response.md` §11-§13; `agent-run-log.md` run-8 correction notes and run-9 section. The decisions D-RUN-18..21 are cited as "decisions table, D-RUN-xx row". `gate-response.md:417` retains "build-log line 304 vs 305" only as the finding's name in the resolution table, not as a pointer; older run sections in `agent-run-log.md` keep their line numbers with an explicit note that they are historical. The former "300-305" range is now the RWB-E1-043 rows of 2026-11-18 05:52:36 by stage. |
| `REVIEW-RWB-E1-043-160` (E1-042 cites pinned to revision 12) | Low | **Resolved** | Every RWB-E1-042 cite in the current spec set is on revision 13 by section or row ID, with no live line pointer: `spec.md:47` (E42S row), `:465` (SPEC-019 T-TE001-14), `:625-629` (SPEC-025 `PARAMETER`), `:738` (QUEUE), `:1176` (CLAR-019); A-25 (`assumptions.md:40`); GAP-50/51/57 (`document-gaps.md:80-88`); R6 (`shared-updates.md:77`), R22, R24, R29, R32; `compliance-validation.md:28, 70-72`; `contracts/backend-apis.json` `source`, `p4HandlerSpi.implementedBy` and `consumedInterfaces.basis`. The seven moved line cites are replaced by `§4.3` shared reference-load endpoint row, `§4.3` ACE business-date row, `§12.14` T-2, `§12.14` R7-1, `§12.14` R7-3, Clarification Log CLAR-025 and CLAR-027. `spec.run11.md` is named as the retained revision 12 in the E42S row, A-25 and R6. R6 records the revision-13 read by name and time and states that every name this story consumes was re-read in revision 13 and is unchanged. No live `E42S revision 10/11/12` pointer remains; the only mentions are the revision-history notes in A-25, R6 and `gate-response.md` §12. |

## Revision-10 diff: citation-only

| Check | Result |
|---|---|
| `spec.md` diff against `spec.run9.md` | Changed lines are the revision header (`:8`), previous list (`:10`), intro (`:21-24`), E42S row (`:47`), BLOG row (`:52`), Inherited Existing Behavior (`:81`), Module scope (`:84`), P2 (`:101`), three E42S row cites (`:241`, `:720`, `:1014`), SPEC-019 (`:465-466`), SPEC-025 (`:625-631`), SPEC-032 region (`:482`), the E42S §4.3 and §10.2 revision cites (`:490`, `:495`), SPEC-029 table (`:760`) and CLAR-019 (`:1176`). Every edit replaces a revision or line pointer with the revision-13 section/row ID, or bumps a revision number. No design sentence, check order, signature, threshold, message ID or scope statement is altered. |
| SPEC / TC / CLAR sets and counts | `spec.md` carries 32 full `SPEC-RWB-E1-043-001..032` IDs, 11 `TC-E1-043-01..11` IDs and 20 `CLAR-001..020` rows, the same sets as revision 9. Total matches of the SPEC/TC/CLAR/A/GAP token pattern are 627 in both revisions. The only new token in the text is `SPEC-009`, part of `REVIEW-RWB-E1-043-SPEC-009`, not a spec item. `assumptions.md` (91 unique IDs), `document-gaps.md` (106), `shared-updates.md` (117), `compliance-validation.md` (63) and `gate-response.md` (132, plus the review ID) keep the same unique ID sets; no assumption, gap or request row was added, removed or re-numbered. |
| Contract files | `backend-apis.json` changes only `revision`, `source`, `p4HandlerSpi.implementedBy` and `consumedInterfaces.basis` citation text; `frontend-integrations.json` is byte-identical to its run-9 copy. Both parse as JSON. |
| No design statement altered | The E42S row, A-25 and R6 are restructured around the same names and rules; the `§12.14 T-2` label corrects a section label that was wrong in revision 12 (T-2 sits under `§12.14` there too) without changing T-2's content. The historical line numbers in GAP-51, gate-response §12 and the older `agent-run-log.md` sections are explicitly labelled as the record of earlier reads, not as live pointers. |

## Live RWB-E1-042 revision-13 spot-check

The live `spec.md` (revision 13, 1302 lines, 06:01:50) was read at the cited locations; the kept
revision 12 `spec.run11.md` (1287 lines) was read for the same rows.

| Citation in revision 10 | Live revision-13 evidence | Verdict |
|---|---|---|
| `§4.3` later-work table, shared reference-load endpoint row | Line 148: row titled "Shared reference-load endpoint (`POST /admin/reference-loads`, ...)", containing "**Handler SPI (D-RUN-18)**" and "**`PARAMETER` route (findings 152, 155)** ... dispatcher branch ... `ParameterLoadBranch` ... implements no `access.api` type". Same row and substance in revision 12 (line 147); the only difference is citation wording. | Correct |
| `§4.3` later-work table, ACE business-date row (P3 → P1 read) | Line 154: "ACE business date (`v_ace_batch_status`) ... `BusinessDateProvider` ... a P3 → P1 read ... allowed under D-RUN-18". Identical in revision 12 (line 153). | Correct |
| `§12.2 access.api.CatalogParameterReader` with nested record `Value` (D-RUN-19), implemented in P3 `casewf.config` | Lines 605-615: interface `CatalogParameterReader` with `get(String, Class<T>, LocalDate)`, `get(String, Class<T>)` and `record Value<T>(String key, T value, int versionNo, LocalDate validFrom, String environment)`; implementation `CatalogParameterReaderImpl` in `casewf.config`. The whole `§12.2` block is identical in revisions 12 and 13. | Correct |
| `§12.14 T-2`, which adds `CatalogParameterReader` to T-TE001-14 | Line 983: "T-2 ... (rev 9) + `CatalogParameterReader` (D-RUN-19)". The row is identical in revision 12 (line 982) and sits under `§12.14` in both (heading at 961 and 960). | Correct |
| `§12.14 R7-1` and `R7-3` (module scope under D-RUN-21) | Line 1007: R7-1 `PARAMETER` dispatcher branch, flag-off result, no second load record; line 1009: R7-3 "Module scope: the P3 + P4 plan touches one ACE module (recovery), so it does not go back to the analyst under AGENTS §7 ... D-RUN-21 ... not ratified (OPEN-050)". Both rows identical in revision 12 (lines 1006 and 1008). | Correct |
| Clarification Log `CLAR-025` and `CLAR-027` | Lines 1207 and 1209: CLAR-025 records D-RUN-21 and the one-ACE-module reading, CLAR-027 records D-RUN-18/19/20 and D-RUN-20's `PARAMETER` clarification, both SETTLED by the orchestrator and pending OPEN-050. Identical in revision 12 (lines 1198 and 1200). | Correct |
| `§10.1` and `§12.2` `MessageResolver.english/thai(String messageId, Map<String, String> placeholders)` returning `String` | `§10.1` line 389 and `§12.2` lines 598-601: both methods present with those parameter types and `String` return. The `§10.1`-`§10.2` block differs from revision 12 only in the E43S citation phrase. | Correct |
| `§10.2` `ApiProblemException(HttpStatus, String messageId, Map<String, String> placeholders, String field, String detail, Throwable cause)` with `status()`, `messageId()`, `field()`, `detail()`, optional `detail`, and guards | Lines 400-405: the constructor, the four accessors, `error()` null for this form, the status/message-ID guards, and the optional `detail` rendered in place of the EN text. | Correct |
| `§12.2` `CapabilityCheck.has(...)` and `require(...)`, which throws `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", action), null)` | Lines 616-620: both method signatures. `§12.10` lines 843-851 give the exact `ApiProblemException(ApiError.NOT_PERMITTED, Map.of("action", "read parameters"), null)` form and the 403 MSG-P4-002 rendering. | Correct |
| `§4.1` "Catalog change merged" row | Line 120: trigger row "Catalog change merged", build-time key generation and checks, new key needs a migration. | Correct |
| `§12.7` recorder failure 503 MSG-P7-003; `§12.10` grants file; `§12.12` flag binding | Lines 804-807: `VersionDecisionRecorder.recorded(...)` wrapped, failure becomes MSG-P7-003 HTTP 503. Line 856: `backend/src/main/resources/access/interim-capability-grants.csv`. Lines 936-950: `@ConditionalOnProperty(prefix = "rwb.p3", name = "configservice", havingValue = "true")` and the bean table. | Correct |
| Test and spec ID sets cited | `TC-E1-042-05..07`, `-10`, `-11`, `-16..-20`, `-23`, `TC-45` all exist in revision 13; `SPEC-RWB-E1-042-005/-012/-017/-019/-020/-021/-022/-023/-025/-026` all exist (the file's set runs 001..027); CLAR-013 exists. | Correct |
| `spec.run11.md` retained revision 12; E1-042 round-12 PASS | `spec.run11.md` header: revision 12, remediation run 10; live `spec.md` header: revision 13, remediation run 11; `review/spec-gate-review-12.md` ends `SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]`; build-log row 335 records the round-12 PASS at 2026-11-18 07:32:37. | Correct |

## No resolved finding reopened

| Finding | Round | Status after revision 10 |
|---|---|---|
| 155 D-RUN-21 not applied to plan routing | 8 | Still applied: Module scope row (`spec.md:84`), A-24, R22, `CHANGE_CLASSIFICATION_SUMMARY` (`:1185`) and `compliance-validation.md:75` state the ACE-module reading and "no tech-lead approval is claimed". |
| 156 GAP-58 over-reads D-RUN-18 | 8 | Still correct: GAP-58 quotes D-RUN-18's wording and the 05:52:36 triage answer; it does not attribute an RWB-E1-019 claim to D-RUN-18 or D-RUN-20. |
| 157 Re-baseline covered only `spec.md` | 8 | Superseded in the right direction: every file now cites revision 13 by section/row, and revision 12 is named as the kept `spec.run11.md`. |
| 158 Allowance cited to a row that does not say it | 8 | Still cited to the 05:52:36 Gate triage row, which states "Each triage message allows one further Low-only round"; the line number is gone. |
| 147-154, 138-146, 131-137, 118-130 | 5-7 | No revision-10 edit changes their substance; the diff shows only citation replacements in the same paragraphs. |
| 159, 160 | 9 | Resolved above. |

## Check order, contract and count integrity

- SPEC-025 L1-L15, maker-checker, the append-only trigger, message pass-through, the 403 action texts,
  flag-off start-up and the SPI signature are unchanged from revision 9.
- Counts are unchanged: 46 assumption rows (A-01..A-46, A-32 withdrawn); 59 gaps (40 C, 19 M, 0
  blockers); 49 COVERED rows; 16 requirement lines owned elsewhere; CONTRADICTIONS 40, equal to the C
  count. `CLARIFICATION_STATUS` still reports 59 gaps and 0 blockers.
- GAP-59 remains M, Blocker = No, cites OPEN-050, and cross-references E1042-SP-DG-16 and
  RWB-TE-001 PG-04/GC-1 without claiming a new `DOCUMENT-GAPS.md` entry.
- No business value, role or threshold is a literal; no personal data, secret or production data
  appears; test codes and dates are synthetic. Frontend remains `NOT_APPLICABLE`; the 80% backend
  unit-test gate stays planned.

## Gate decision

There is no Critical, High, Medium or Low finding. Both citation defects from round 9 are fixed, and
the live RWB-E1-042 revision-13 text supports every replaced pointer. The 07:33:17 Gate triage allowed
this one further Low-only round under D-RUN-09; that triage is the orchestrator's, not a human
ratification. OPEN-050 remains open before the plan gate: D-RUN-18, D-RUN-19, D-RUN-20 and D-RUN-21
are still unratified. The spec is ready for the plan gate.

REVIEW_STATUS: PASS
REVIEW_FINDINGS: [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
ROUND_9_FINDINGS: 159 resolved; 160 resolved
G8_R01: recorded as GAP-59 (M, Blocker No); unchanged
D_RUN_21: applied to plan routing; no tech-lead approval claimed
RATIFICATION_CLAIMS: none found
DOCUMENT_GAPS_ADDED: 0
NEXT_STEP: Plan gate; OPEN-050 remains open
SPEC_GATE: PASS [CRITICAL: 0] [HIGH: 0] [MEDIUM: 0] [LOW: 0]
