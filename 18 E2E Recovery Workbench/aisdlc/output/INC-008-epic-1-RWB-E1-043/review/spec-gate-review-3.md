# Spec gate review, round 3: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-003` |
| Gate | Specification gate, round 3 (Compliance Reviewer, bounded review) |
| Artefacts reviewed | `specify/spec.md` revision 3 (2026-11-18 00:45), `assumptions.md` (A-01..A-40), `document-gaps.md` (GAP-01..GAP-44), `shared-updates.md` revision 3 (§3.1, §3.2, R1..R23), `compliance-validation.md` revision 3, `contracts/backend-apis.json` revision 3, `contracts/frontend-integrations.json`, `gate-response.md` (§6), `agent-run-log.md`. The `*.run2.*` files were used as the audit trail only. |
| Previous round | `review/spec-gate-review-2.md` (`REVIEW-RWB-E1-043-SPEC-002`, FAIL: 0 High, 4 Medium, 7 Low, G2-R01..G2-R05) |
| Sources checked | Story files v7: RWB-E1-043, RWB-E1-001, -019, -028, -037, -064; API Specification v4.0.0 (load, approve, rollback operations and response sets); Error and Message Standard v4 (MSG-P1-002/003/004/007/011, MSG-P3-027, MSG-GEN-001/002/004); Physical Schema v6 (Reference data permission seed, role list, LOV-REF-TABLE); Users, Roles and Permissions v4 (Reference data column); Decision Log v10 (D-RCV-11, D-RCV-28, D-RCV-29); RWB-TE-001 spec v4 and its gate round 5 (SPEC-022(d), shared updates SU-02, SU-08); RWB-E1-042 spec revision 5 (00:51) and revision 4 (`spec.run3.md`) with its `review/spec-gate-review-3.md` (finding 129); RWB-E1-001 spec revision 2 and its `review/spec-gate-review-2.md` (findings 014, 016, 017, 022, 023); `AI-SDLC-BUILD-LOG.md` (D-RUN-07..D-RUN-16, triage entries to 00:50). |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-07..D-RUN-15, the round-1 and round-2 triage entries, the RWB-E1-001
addendum and the GAP-38 correction were given by the orchestrator, Claude Code, an AI agent. They are
not human decisions and not human acceptance, and this review does not treat them as such. D-RUN-16 was
set by the engagement lead in chat; it concerns model and effort choice and does not bear on this spec.
Revision 3 attributes the rulings correctly: spec §0 and §Owner acceptance (lines 844-862) list D-RUN-08,
-10, -11, -12 and the 2026-11-18 triage as "not ratified"; `compliance-validation.md` §1 and §3,
`shared-updates.md` §3.1 item 1 and §3.2, `agent-run-log.md` remediation run 2 and `gate-response.md` §6
say the same; A-31's revision-2 acceptance wording is gone; open item R1 asks the engagement lead for
ratification. No text found in any artefact presents a D-RUN entry or the 2026-11-18 triage as human or
ratified.

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 1 | Blocks the handoff to the Implementation Planner |
| Medium | 1 | Blocks the handoff to the Implementation Planner |
| Low | 5 | Visible; human disposition required |

Every round-2 finding (120-130) and every round-2 gap (G2-R01..G2-R05) is resolved in the files, not
only in `gate-response.md`. The handler contract in SPEC-025 and `shared-updates.md` §3.1 is now
specific enough for RWB-E1-001 to write its handler. Two new problems block the handoff. The first
(131, High) comes from a source that changed under this revision: RWB-TE-001 v4 (order 2, gate passed
at 00:39) removes the `platform` package and fixes the module direction P3 → P4, and RWB-E1-042 has
been rebased onto it (revision 5, 00:51). This spec still builds on `platform.api` and has P4 calling P3,
which with the rebased names is a module cycle. The second (132, Medium) is the timing of `apply`: the
handler writes its tables at approval, whatever the `validFrom`.

## Round-2 findings: resolution check

| Round-2 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 120 SPI contract | Medium | **Resolved** | SPEC-025 now states the whole contract: the interface with `keyColumns`, `repeatMessage`, `supportsRollback`, `onRolledBack`, `changeSummary`; records `ReferenceLoadFile`, `HandlerMessage`, `RowCheckFailure`, `ValidationReport`; check order L1-L14; message pass-through ("never maps them to MSG-P3-027"); the column definition is optional (A-37); repeat answers 409 with the handler's message (A-38). The `data_product` and QUEUE paragraphs match S7-001 X4-X8 and S7-019 AC4-AC5. GAP-39 (G2-R01) and GAP-44 record what the sources leave open. `backend-apis.json` `handlerContract` matches the spec. Residuals are 133 and 136. |
| 121 Dictionary owner | Medium | **Resolved** | SPEC-031 is the registry part only. RWB-E1-064 is named owner of `sys_fields` (S7-064 §3 line 42, flow step 3). GAP-37 and GAP-38 are corrected; GAP-40 (G2-R02) added; A-36 rewritten; §3.2 is the forward note to RWB-E1-064. Residual: the approver role named for `sys_fields` (135). |
| 122 Access lists | Medium | **Resolved** | SPEC-026 refuses any `rwb.refload.*` key in a PARAMETER load with 422 MSG-P1-002 before RWB-E1-042 is called; SEC-15 tests it; A-39 makes a reviewed catalog change the only path until RWB-E1-037; GAP-41 (G2-R03); A-31's acceptance claim removed. |
| 123 COVERED rows | Medium | **Resolved** | The SIT done-when row and the RW-AUDIT HTTP read row are moved to "lines built by another story"; SPEC-022 is a seam; GAP-43 (G2-R05); R10 and R18. Counts verified: 48 COVERED rows (47 DIRECT, 1 INHERITED), 15 lines owned elsewhere. |
| 124 `IF NOT EXISTS` | Low | Resolved | §3.1 item 1 drops the option and cites D-RUN-12 as an AI-orchestrator ruling, not ratified. |
| 125 Dictionary rollback | Low | Resolved | SPEC-024 and SPEC-031 state the rollback path; A-27. |
| 126 Approver area right | Low | Resolved | A-08 gives interim Reference data A to six roles (RW-RISK, RW-COE, RW-COMPLY, RW-TEAMMGR, RW-DATASTEW, RW-SECADM); SEC-17. The source conflict this creates for RW-DATASTEW is not recorded (134). |
| 127 Actor claim | Low | Resolved | `ActorIdResolver`: `oid` if a UUID, else `sub` if a UUID, else 401 (SPEC-015, A-07); SEC-16. |
| 128 E42S revision | Low | **Resolved, now superseded** | Revision 3 re-baselined on E42S revision 4 and corrected A-26. Revision 4 has since been replaced by revision 5, which moved the names this spec uses (131). |
| 129 Audit actor | Low | Resolved | GAP-42 (G2-R04) records the backend-context line 138 conflict; R9 to the DPO. |
| 130 Owner acceptance | Low | Resolved | §Owner acceptance lists the AI rulings as not ratified; R1. See "About the run rulings". |
| G2-R01..G2-R05 | — | Carried in | GAP-39..GAP-43, with "Raised by" and resolutions. Counts verified: 44 gaps (29 C, 15 M, no blocker), 40 assumptions. |

### What holds (verified)

- The quotes spot-checked are accurate:
  - S7-001 §12 (handler "the owning module provides"; repeat is a file matching "the version in force"), X4-X8, AC7-AC11, flow step 9;
  - S7-019 AC4, AC5, X1, X2, X7 and flow steps 4 and 8;
  - S7-064 §3 line 42, flow step 3, X3 and §11 (`is_personal` Read);
  - S7-037 line 46 approver keys and BR3; S7-028 lines 41 and 46;
  - E01S revision 2 SPEC-013 ("holds no column definition") and K0.
- The check order L1-L14 is consistent with S7-043 §13 step 3 (validity check, then hash, then idempotent return) and X4.
- The SPI signature, records and defaults are the same in `spec.md`, `shared-updates.md` §3.1 and `contracts/backend-apis.json`.
- Maker-checker (service rule and DB CHECK), the narrowed append-only trigger, the per-version `row_key`, and the cache serving only APPROVED versions are unchanged from round 2.
- No business value, role or threshold is a literal. Lists, definitions and the TTL are catalog keys; role grants are data.
- No personal data, secret or production data appears in any artefact. Test users are random UUIDs; log and audit lines carry no user ID or row content.
- The frontend is correctly `NOT_APPLICABLE`.

## Findings

### High

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-131` | High | **The module placement contradicts RWB-TE-001 v4 and, with RWB-E1-042's rebased names, is a P3 ↔ P4 cycle.** (a) The spec puts the load, approve and rollback controller, dispatcher, authority and audit in P4 `access.refload`, which calls P3 `casewf.refdata.api`; `ReferenceTableCodeSource` is implemented in P4; SPEC-025 says "P4 already depends on P3". RWB-TE-001 v4 (BS6 order 2, gate round 5 PASS 00:39) fixes the opposite direction: SPEC-022(d), "P3 depends on P2 and P4", so access may not depend on casewf. Its shared update SU-08, addressed to INC-008, says a P4 → P3 call "makes a cycle" that ModulithTest rejects (D-RCV-11) and to put the controller in the P3 refdata package; S7-043 §13 also names `recovery.casewf.refdata`. No INC-008 artefact mentions SU-08. (b) The spec builds on types RWB-TE-001 removes: `platform.api.RecoveryFlags`, `platform.internal.RecoveryProperties`, `platform/interim-capability-grants.csv`, and RWB-E1-042's names "in `platform.api`" (A-25). RWB-E1-042 revision 5 (00:51) now has `ParameterLoadHandler`, `ParameterLoadResult`, `ParameterKeys`, `BusinessDateProvider` in `casewf.config.api`; `CapabilityCheck`, `MessageResolver` and `ApiProblemException` in P4 `access.api`; the grants file in `access/`; the flag bound by `@ConditionalOnProperty`. Once rebased, `casewf.refdata` must use `access.api` (P3 → P4) while `access.refload` uses `casewf.refdata.api` (P4 → P3): a cycle. (c) `VersionDecisionRecorder` is now a non-published port in `casewf.config` (E42S revision 5 line 141), so SPEC-008's call from the refdata code is a call into another module's internals. This is the same defect as RWB-E1-042 round-3 finding 129 (High). | spec.md:71, 72, 76, 236, 291, 374-375, 511, 549-550, 579; assumptions.md A-10, A-24, A-25; compliance-validation.md §2 "Module boundary", §3 ("depends on RWB-E1-042 revision 4's `platform.api` names"); backend-apis.json consumed package `platform.api`; TE-001 spec v4 SPEC-022(d), SU-02, SU-08; E42S revision 5 §12, line 141, line 507; build log 00:38 (finding 129) | SPEC-002, 008, 015, 016, 018, 019, 024, 025, 027, 030; A-10, A-24, A-25; both contracts; §3.1 item 4 import | Re-baseline on RWB-TE-001 v4 and RWB-E1-042 revision 5. Move the controller, dispatcher, authority, audit adapter and `LovReferenceTableCodes` into P3 `casewf.refdata` (internal), so no P4 → P3 edge remains; drop `ReferenceTableCodeSource` from P4. Declare `casewf.refdata.api` as the published interface in the module map. Bind the flag through `@ConditionalOnProperty` or a module record, not `RecoveryFlags`. Put the grant rows in `access/interim-capability-grants.csv`. State how AC-VERS is recorded now that `VersionDecisionRecorder` is non-published (a published port in E42S, or this story's own interim recorder), and record the change as a gap if E42S must publish it. Replace SPEC-019's rule with the TE-001 direction and update `RecoveryBoundaryTest`/ModulithTest expectations. Correct A-10, A-24, A-25, the contracts and §3.1 item 4 (`ApiProblemException` is in `access.api`). The SPI package `casewf.refdata.api` and its signature need not change. |

### Medium

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-132` | Medium | **`apply` runs at approval whatever the `validFrom`, so handler tables can show a version before it is in force, and no order rule exists.** SPEC-025 calls `apply(loadId, file, validFrom)` inside the approve transaction. L8 allows any `validFrom` on or after the business date, so a version approved today for a future date is written into the owning module's own tables (`data_product`, QUEUE, `sys_fields`) at once. The registry itself serves only the version in force (SPEC-010, S7-043 BR3), so the two disagree until the date arrives. S7-019 flow step 5 says QueueVersionApplier applies versions "on the valid from date"; S7-001 flow step 10 writes rows "with the valid from date". Approving two future versions out of order (A-18 covers only `valid_to`) leaves the handler tables on whichever was approved last. `onRolledBack` restores a version without saying which version is in force. None of this is recorded as a gap, and the contract in §3.1 does not tell RWB-E1-001 whether its tables must hold `validFrom` and read by date. | spec.md:290, 454, 491, 509-515; A-18; S7-019 flow step 5; S7-001 flow step 10; S7-043 BR3; shared-updates.md §3.1 item 2 | SPEC-025, SPEC-010, SPEC-024; §3.1, §3.2; RWB-E1-001, -019, -064 handlers | Define the timing in SPEC-025 and §3.1. Options: refuse approval of a handler-code version whose `validFrom` is later than the business date; or add an "in force" callback run by a scheduled job on the date; or require handlers to store `validFrom` and read by date, with `apply` never overwriting a later version. Define the out-of-order and rollback rule for handler tables. Record the S7-019 step 5 conflict as a gap. Add a test (future-dated approval; out-of-order approval). |

### Low

| ID | Severity | Finding | Evidence | Fix required |
|---|---|---|---|---|
| `REVIEW-RWB-E1-043-133` | Low | RWB-E1-001 AC10 ("Given the catalog version loaded on 2026-11-30 is in force", the same file again → MSG-P1-011) can be met only when the business date equals the version's `validFrom`. L8 runs before L9: reloading with the old `validFrom` after that date answers 422 MSG-P3-027; reloading with a new `validFrom` is a new version, 201. GAP-44 and §3.1 item 7 hand the difference to the RWB-E1-001 owner and the BA but do not state these consequences, the test precondition, or whether `validate` may itself return MSG-P1-011 by comparing the content with the version in force. | spec.md:491-492; GAP-44; shared-updates.md §3.1 items 3, 7; S7-001 AC10, §12; E01S revision 2 AC10 PARTIAL, CLAR-013 | State the AC10 precondition (business date = `validFrom`) and whether a handler may raise MSG-P1-011 from `validate`; add both to GAP-44 and §3.1 item 7. |
| `REVIEW-RWB-E1-043-134` | Low | RW-DATASTEW is the `data_product` approver (A-40) and gets interim Reference data A (A-08). S7-001 §10 says RW-DATASTEW confirms the version with "Reference data U"; S7-064 line 43 also gives RW-DATASTEW U; PS6 seeds RU; API v4 approve requires A and notes A "is held by no role". The conflict between the story's U and the API's A is not recorded. | A-08, A-40; S7-001 §10, flow step 9; S7-064 line 43; PS6 Reference data seed; API v4 approve | Record the U-versus-A conflict as a gap (Blocker = No) with the access owner. |
| `REVIEW-RWB-E1-043-135` | Low | SPEC-031, A-36 and §3.2 item 2 require RWB-E1-064 to set the `sys_fields` approver list to RW-COMPLY and "the data architect's role". PS6 and Users, Roles and Permissions v4 have no such role code, and S7-064 names no approver (RW-COMPLY is inferred from TE-011 §10). RWB-E1-064 cannot seed the list without guessing. | spec.md SPEC-031; A-36; shared-updates.md §3.2 item 2; PS6 role list; S7-064 §10 | Name a role code or record the missing approver as a gap with an owner; label RW-COMPLY as inferred. |
| `REVIEW-RWB-E1-043-136` | Low | (a) L3 checks the loader list for `rwb.refload.loader.<code>` before L5 checks that `table` is present, so a load with no `table` answers 403, not the 422 MSG-GEN-001 that SPEC-015 and A-12 promise. (b) The load answers 404 (flag off, L4) and 500 (a non-Problem exception from `validate`), but API v4's load operation lists only 201, 401, 403, 409, 422 and 503. Neither difference is recorded. | spec.md:486-488, 503-507; SPEC-015; A-12; API v4 load operation (yaml line 3167) | Move the presence check for `table` before L3 (or say a missing `table` is 403 and fix SPEC-015/A-12). Record the 404 and 500 responses against API v4 as a gap. |
| `REVIEW-RWB-E1-043-137` | Low | Stale text. `gate-response.md` §§3-4 still say RWB-E1-001 owns the dictionary handler and registers its catalog keys and column definition, which §6 and §3.1 now contradict. `contracts/frontend-integrations.json` still carries revision 2. S7-019 line 38 says QUEUE_MEMBER "is added to" LOV-REF-TABLE, while the spec treats QUEUE_MEMBER as a handler code and §3.1 item 6 says no LOV change; the S7-019 line is not reconciled. | gate-response.md §§3-4; frontend-integrations.json header; S7-019 line 38; spec.md QUEUE paragraph; shared-updates.md §3.1 item 6 | Mark §§3-4 as superseded; bump the contract revision; state whether QUEUE_MEMBER needs a LOV-REF-TABLE row (a note to RWB-E1-019) or record the conflict. |

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete. L1-L14 with refusal codes; the `data_product` path is spelled out (no column definition, so L11 is skipped). | SPEC-025 table; §3.1 item 3 |
| What the handler supplies | Complete. Bean behind its own flag, `tableCode`, `keyColumns`, `validate`, `repeatMessage`, `apply`, `supportsRollback`; two catalog rows; message IDs in E42S's catalog; nothing else. | SPEC-025 "What the owning story supplies"; §3.1 item 2 |
| Message pass-through | Complete. First failure's code, placeholders and column at 422; `detail` lists all; never re-mapped; `ApiProblemException` passes through; other exceptions 500 / 409. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Defined (L9 → 409 with `repeatMessage`), with the source difference recorded (GAP-44). Consequence for AC10 not stated (133). | SPEC-025 L9; §3.1 item 7 |
| Seed rows | Complete. Exactly two CODE_LIST rows with all attributes, defaults and the migration form; no `refdata.columns.data_product`; no grants-file edit. | §3.1 item 5; A-40 |
| LOV-REF-TABLE | Complete. No change; rows to add and remove both stated as none. | §3.1 item 6 |

On the six points the contract is complete: RWB-E1-001 can write its handler without guessing. Three
things still affect it and should be settled before RWB-E1-001 is released from hold: when `apply`
runs relative to `validFrom` (132), the AC10 precondition (133), and the import package of
`ApiProblemException` after the re-placement (131; it is `access.api`). The SPI package
`casewf.refdata.api` and the signature are not expected to change under 131.

## Document gaps not recorded by the specify stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| G3-R01 | Story file v7 RWB-E1-019 flow step 5 (versions applied "on the valid from date"); story file v7 RWB-E1-001 flow step 10 | Handler tables are written at approval, not on the valid-from date | RWB-E1-043 spec revision 3 SPEC-025 (apply in the approve transaction); S7-043 BR3 | No | A timing rule can be set by design (refuse future approval, scheduled apply, or date-aware handlers) | Finding 132 |
| G3-R02 | Story file v7 RWB-E1-001 §10 (RW-DATASTEW confirms with Reference data U); story file v7 RWB-E1-064 line 43 | The story's confirm right is U; the API approve right is A, held by no role | API Specification v4.0.0 approve operation; Physical Schema v6 Reference data seed (RW-DATASTEW RU) | No | Interim A in the grants file is possible; the access owner confirms | Finding 134 |
| G3-R03 | Story file v7 RWB-E1-064 §10 (no approver named for `sys_fields`) | No source names the approver role for dictionary loads; no "data architect" role code exists | Physical Schema v6 role list; Users, Roles and Permissions v4; RWB-TE-011 §10 (RW-COMPLY owns which fields are personal) | No | RWB-E1-064 can seed RW-COMPLY on a labelled assumption | Finding 135 |
| G3-R04 | API Specification v4.0.0 load operation (responses 201, 401, 403, 409, 422, 503) | No 404 for a flag-off branch and no 500 for a handler defect | RWB-E1-043 spec revision 3 SPEC-018, SPEC-025; E42S SPEC-021 (404 MSG-P4-003 flag rule) | No | Extra responses can be documented against the API owner | Finding 136 |
| G3-R05 | Story file v7 RWB-E1-019 line 38 (QUEUE_MEMBER added to LOV-REF-TABLE) | Conflicts with QUEUE_MEMBER as a handler code and with §3.1's "no LOV change" | Physical Schema v6 LOV-REF-TABLE; RWB-E1-043 spec revision 3 QUEUE paragraph | No | Settled by a note to RWB-E1-019 | Finding 137 |

The placement conflict in 131 is between story specs (RWB-TE-001 v4 SU-08 and this spec), not between
documents; S7-043 §13 and TE-001 agree. It is carried by the finding, not as a document gap.

## Gate decision

The High finding 131 and the Medium finding 132 block the handoff to the Implementation Planner
(`pdlc.md`). The Technical Specifier should rebase the spec on RWB-TE-001 v4 and RWB-E1-042 revision 5
(131), define the apply timing (132), fix the Low findings 133-137 in the same run, and record
G3-R01..G3-R05. This gate then re-runs as `review/spec-gate-review-4.md`. No finding needs a
Blocker = Yes gap. RWB-E1-001 can conform to the handler contract on the six points reviewed; it should
stay held until 131 and 132 are settled, or proceed on the stated SPI signature, which 131 does not
change.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 1] [MEDIUM: 1] [LOW: 5]
REVIEW_STATUS: FAIL
BLOCKING: YES (High finding 131 and Medium finding 132 block the handoff to the Implementation Planner)
ROUND_2_FINDINGS: 120-130 resolved (128 superseded by 131; follow-ups 133-136); G2-R01..G2-R05 carried in as GAP-39..GAP-43
RWB_E1_001_CONTRACT: COMPLETE on check order, handler supply, message pass-through, repeat, seed rows, LOV-REF-TABLE; residuals 132, 133, 131 (import package)
DOCUMENT_GAPS_ADDED: 5 (G3-R01..G3-R05; no blocker)
NEXT_STEP: Technical Specifier remediation run 3 for REVIEW-RWB-E1-043-131..137, then spec gate round 4 (review/spec-gate-review-4.md).
```
