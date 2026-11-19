# Spec gate review, round 4: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-004` |
| Gate | Specification gate, round 4 (Compliance Reviewer, bounded review) |
| Artefacts reviewed | `specify/spec.md` revision 4 (2026-11-18 01:24), `assumptions.md` (A-01..A-44, A-32 withdrawn), `document-gaps.md` (GAP-01..GAP-53), `shared-updates.md` revision 4 (R1..R28, §3.1, §3.2), `compliance-validation.md` revision 4, `contracts/backend-apis.json` revision 4, `contracts/frontend-integrations.json` revision 3, `gate-response.md` (§7), `agent-run-log.md`. The `*.run3.*` files were used as the audit trail only. |
| Previous round | `review/spec-gate-review-3.md` (`REVIEW-RWB-E1-043-SPEC-003`, FAIL: 1 High, 1 Medium, 5 Low, G3-R01..G3-R05) |
| Sources checked | Story files v7: RWB-E1-043, RWB-E1-001, -019, -028, -064, -069; RWB-TE-001 spec v4 (SPEC-004, SPEC-022(d), SPEC-023, SPEC-025, T-TE001-14) and its shared updates SU-02, SU-08, SU-14; RWB-E1-042 spec revision 6 (`spec.md`, 01:18) and revision 5 (`spec.run4.md`), §4.3, §10.3, §11.2, §12.2, §12.5, §12.7, §12.10, §12.12, its `shared-updates.md` and `review/spec-gate-review-4.md` (findings 136, 140, 141); Data Dictionary v8 (DF-REF-028/029, DF-REF-071, DF-REF-079); Physical Schema v6 (`data_product`, `sys_fields`, `queue`, `queue_member`, Reference data seed); Users, Roles and Permissions v4; Error and Message Standard v4 (MSG-P4-002, MSG-P3-027, MSG-P7-003); API Specification v4.0.0 (`api/recovery-api-v4.yaml`, load, approve, rollback); Decision Log v10 (D-RCV-11, D-RCV-28); `ApiExceptionHandler` (forbidden path, read only). |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-07..D-RUN-15, the round-1 to round-3 triage entries, the RWB-E1-001
addendum and the GAP-38 correction were given by the orchestrator, Claude Code, an AI agent. They are
not human decisions and not human acceptance, and this review does not treat them as such. Revision 4
attributes them correctly: spec §0 and §Owner acceptance (lines 967-988) list the rulings and the
round-3 triage (including the GAP-52 rollback rule taken against the orchestrator default) as "not
ratified"; `compliance-validation.md`, `shared-updates.md` §3.1 and §3.2, `gate-response.md` §7 and
`agent-run-log.md` run 3 say the same; open item R1 asks the engagement lead for ratification. No text
found in any artefact presents a D-RUN entry or a triage as human or ratified.

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 1 | Blocks the handoff to the Implementation Planner |
| Low | 8 | Visible; must be fixed (D-RUN-09) |

Every round-3 finding (131-137) and every round-3 gap (G3-R01..G3-R05) is resolved in the files. The
module placement now follows RWB-TE-001 v4: all story code is in P3 `casewf.refdata`, the only new
cross-module edge is P3 → P4 (`access.api.ListOfValuesReader`), and no P4 → P3 edge remains. One
problem blocks the handoff (138, Medium): the effective-date rule that fixed 132 tells RWB-E1-001 and
RWB-E1-064 to store dated versions keyed by `validFrom`, but `data_product` and `sys_fields` are
current-state tables in the source schema (one row per key, no date range). The handlers cannot do
what §3.1 and §3.2 ask, so a future-dated approval would still change their values early.

## Round-3 findings: resolution check

| Round-3 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 131 Placement and cycle | High | **Resolved** | No `platform.`, `access.refload`, `RecoveryFlags` or `ReferenceTableCodeSource` remains in any artefact. Controller, dispatcher, authority, audit and registry are in `casewf.refdata.internal`; `refdata.api` is the published interface (R25 adds it to the module map). SPEC-019's dependency table shows P3 → P4 only, matching TE-001 SPEC-022(d) and SU-08. RWB-E1-042 names are taken from `casewf.config.api` and `access.api`. AC-VERS uses this story's package-private `ReferenceDecisionRecorder` with an interim logging adapter (503 MSG-P7-003 on failure), so `VersionDecisionRecorder` stays internal to `casewf.config`. The flag is bound by `@ConditionalOnProperty`, a `RefdataSettings` record and a shared `@ConditionalOnExpression` on the controller and dispatcher. Grant rows go to `access/interim-capability-grants.csv`. Residuals: 139, 143, 144. |
| 132 Apply timing | Medium | **Resolved for the registry; reopened for current-state handlers (138)** | SPEC-032 and SPEC-025 *Effective date* (lines 578-589): approval writes a dated version, reads select by business date, versions are independent so out-of-order approval is allowed, rollback only of the latest approved version (GAP-52). TC-TM-01..04 test it. The S7-019 step 5 conflict is recorded. The rule depends on handler tables that hold dated versions, which `data_product` and `sys_fields` do not (138). |
| 133 AC10 precondition | Low | Resolved | L9 (repeat) now runs before L10 (`validFrom` ≥ business date), so an identical file answers 409 with the handler's `repeatMessage` on any date; TC-RP-01. The reordering itself is not recorded against S7-043 §13 (140). |
| 134 U versus A | Low | Resolved | GAP-46 records the story's Reference data U against the API's A, with the access owner. Wording of the precedence claim: 146. |
| 135 `sys_fields` approver | Low | Resolved | GAP-47; A-36 labels RW-COMPLY as inferred from RWB-TE-011 §10; no invented role code remains. |
| 136 `table` check and responses | Low | Resolved | L3 checks `table` presence before the loader list (L4); SPEC-015 and A-12 agree; GAP-48 records the 404 and 500 responses against API v4. |
| 137 Stale text | Low | Resolved | `gate-response.md` §§3-4 marked "Superseded"; `frontend-integrations.json` is revision 3; GAP-49 records the S7-019 line 38 QUEUE_MEMBER conflict. |
| G3-R01..G3-R05 | — | Carried in | GAP-45..GAP-49, with "Raised by" and resolutions. Counts verified: 53 gaps (35 C, 18 M, no blocker), 44 assumptions (A-32 withdrawn), 49 COVERED rows (48 DIRECT, 1 INHERITED), 16 lines owned elsewhere. |

### What holds (verified)

- Module direction: P3 → P2/P4 only, as TE-001 SPEC-022(d) requires. `ListOfValuesReader` in `access.api` with interim `access.internal.LovValueReader` meets S7-043 §11 ("through the P4 published interface") for `lov_value`.
- The SPI signature (`tableCode`, `validate`, `apply(UUID, ReferenceLoadFile, LocalDate)`, `keyColumns`, `repeatMessage`, `supportsRollback`, `onRolledBack`, `changeSummary`) and records are the same in `spec.md`, `shared-updates.md` §3.1 and `contracts/backend-apis.json`.
- Check order L1-L15 with refusal codes is consistent across SPEC-025, §3.1 item 3 and the contract.
- Every message ID used (MSG-P1-002/003/004/007/011, MSG-P3-027, MSG-P4-002, MSG-P7-003, MSG-GEN-001/002/004) exists in Error and Message Standard v4 and in E42S §10.3.
- The migration is named `V<seq>__rwb_e1_043_<name>.sql` with no fixed number; line 1 is the story key.
- Maker-checker, the narrowed append-only trigger, per-version `row_key` and the cache serving only APPROVED versions are unchanged from round 3.
- No business value, role or threshold is a literal. No personal data, secret or production data appears in any artefact.
- The frontend is correctly `NOT_APPLICABLE`.

## Findings

### Medium

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-138` | Medium | **The effective-date contract asks RWB-E1-001 and RWB-E1-064 to store dated versions in tables that hold one current row per key.** SPEC-025 *Effective date*, the `data_product` paragraph, A-42, §3.1 items 2 and 8 and §3.2 item 6 say the handler's `apply` writes "a dated version keyed by validFrom" and reads by business date. Physical Schema v6 defines `data_product` with `UNIQUE (product_code)` and a single `valid_from` (no `valid_to`); Data Dictionary v8 marks DF-REF-071 `product_code` as UK and DF-REF-079 `valid_from` as the date the product "comes into force". `sys_fields` has `UNIQUE (field_id)` and no date column at all. Neither table can hold two versions of one key, so a handler can only overwrite the current row: approving a version dated next month changes the values in force today, which is the 132 defect for exactly the two handler codes that exist. (`queue_member` has `valid_from`/`valid_to` and no unique key, so QUEUE can be dated; `queue` keeps a `table_version`.) S7-001 flow step 10 also has `apply` write the rows at approval; that conflict with S7-043 BR3 is not recorded. | spec.md:578-589, 606-615; A-42; shared-updates.md §3.1 items 2, 8, §3.2 item 6; PS6 `data_product`, `sys_fields`, `queue_member`; DD8 DF-REF-071, DF-REF-079; S7-001 flow step 10; S7-043 BR3; S7-064 flow steps 2-3 | SPEC-025, SPEC-032; A-42; §3.1, §3.2; TC-TM tests; RWB-E1-001 and RWB-E1-064 handlers | Classify each handler code as dated (QUEUE) or current-state (`data_product`, `sys_fields`). For current-state codes define the mechanism, for example: refuse approval while `validFrom` is later than the business date (MSG-P3-027 with a stated check); or an owner job that applies the approved version on its `validFrom` (`onInForce` or the owner's scheduled job, Spring Batch/Quartz); or a schema change requested of the data owner. State the out-of-order and rollback rule for the chosen mechanism. Correct SPEC-025, A-42, §3.1 items 2 and 8 and §3.2 item 6 so they do not require a dated store the schema lacks. Add a test with a current-state test handler (future-dated approval leaves today's values unchanged). Record G4-R01 and G4-R02 as gaps. |

### Low

| ID | Severity | Finding | Evidence | Fix required |
|---|---|---|---|---|
| `REVIEW-RWB-E1-043-139` | Low | RWB-TE-001 T-TE001-14 pins the public types of every published package (SPEC-025 lists only `ApiError` and `ApiProblemException` in `access.api`) and the casewf named interfaces (`api`, `rules`, `timers`, `workflow`). This story adds the `refdata` named interface (11 public types) and `access.api.ListOfValuesReader`, so that test fails unless it is extended. Impacted Nodes and TC-BD-01 do not name it. RWB-E1-042 revision 6 extends the same test (its round-4 finding 136). | spec.md Impacted Nodes, TC-BD-01 (tests 902-958); R25; TE-001 spec v4 SPEC-025, T-TE001-14; E42S revision 6 | List T-TE001-14 as a changed test, state the extended expected sets (`refdata` interface and its types; `ListOfValuesReader` in `access.api`) and coordinate the edit with RWB-E1-042 in `shared-updates.md`. |
| `REVIEW-RWB-E1-043-140` | Low | Moving the repeat check (L9) before the `validFrom` check (L10) applies to every table code. S7-043 §13 step 3 and its flow step 3 run the validity check first, then the hash and idempotent return; X3/AC6 expect a past-dated file to be refused. With the new order an identical past-dated file answers 201/409 instead of 422. The departure is not recorded as a gap or an owner-acceptance assumption. | spec.md SPEC-025 L9-L10; A-37/A-38; S7-043 §13 step 3, flow step 3, X3, AC6; S7-001 AC10 | Record the conflict (G4-R03) and add it to §Owner acceptance as an assumption, or limit the early repeat check to handler codes that supply a `repeatMessage` and keep the story order otherwise; adjust TC-RP-01 accordingly. |
| `REVIEW-RWB-E1-043-141` | Low | GAP-51 calls the P1 ↔ P3 cycle "latent" and cites only E42S §4.3. The story files plan P3 → P1 edges directly (S7-028 flow step 3 "through the P1 interface"; S7-043 §12 has the working-day calculator read `v_ace_holiday` through the P1 query of RWB-E1-028), and S7-069 is P1. Once a P1 handler (RWB-E1-001) implements this story's P3 SPI, the cycle is certain, yet R24 sets its deadline as "before RWB-E1-001 plan". The SPI home is this story's published interface, so the decision belongs before this story's plan. | document-gaps.md GAP-51; shared-updates.md R24; S7-028 flow step 3; S7-043 §12 line 270; S7-069 module; S7-001 §12 line 222 (SPI "of P4 that P1 implements") | Add the story-file evidence to GAP-51; make the SPI home (P3 with a P1 inversion, or a neutral published package) a precondition of this story's plan gate and move R24's deadline accordingly. |
| `REVIEW-RWB-E1-043-142` | Low | `ReferenceLoadAuthority` returns `false` on refusal and the 403 is produced by the shared forbidden path, which fills MSG-P4-002's `{action}` with "do this" (`ApiExceptionHandler` line 41). SPEC-020 claims the action placeholder is filled; S7-043 §14 and E42S use `CapabilityCheck.require(..., action)`, which throws `ApiProblemException(NOT_PERMITTED, action)`. | spec.md SPEC-020, SPEC-024; MSG4 MSG-P4-002; `ApiExceptionHandler.java` line 41; E42S revision 6 `CapabilityCheck.require` | Use `require(..., action)` with a named action per operation (load, approve, roll back) from the message catalogue, and assert the `{action}` value in the SEC tests. |
| `REVIEW-RWB-E1-043-143` | Low | The registry is always present but depends on `ReferenceTableHandlers` and `LoggingReferenceDecisionRecorder`, which are `@ConditionalOnProperty` on `rwb.p3.refdata-versions`. With the flag off those beans are absent and the context fails to start, which breaks the "previous code path when off" rule (AGENTS.md §3.13). TC-FL-01 checks the 404 but not start-up. | spec.md SPEC-018, SPEC-019, SPEC-024; TC-FL-01 | Inject the conditional beans through `ObjectProvider` (or make them unconditional and gate behaviour through `RefdataSettings`); have TC-FL-01 assert that the context starts with the flag off and with only `rwb.p3.configservice` on. |
| `REVIEW-RWB-E1-043-144` | Low | The spec, A-25, R6, both contracts and `compliance-validation.md` §3 cite RWB-E1-042 revision 5, but revision 6 (01:18) existed before this revision (01:24). The names used are unchanged, but revision 6 fixes the `MessageResolver` methods (`english(...)`, `thai(...)`) and the `ApiProblemException(HttpStatus, String messageId, Map placeholders, String field, Throwable cause)` constructor that SPEC-025 and §3.1 item 4 rely on. | spec.md A-25 reference, SPEC-025; shared-updates.md R6, §3.1 item 4; backend-apis.json basis; compliance-validation.md §3; E42S revision 6 | Re-baseline the citations on revision 6 and state the `MessageResolver` methods and the `ApiProblemException` constructor used. |
| `REVIEW-RWB-E1-043-145` | Low | RWB-E1-042 `shared-updates.md` asks RWB-E1-043 to add HTTP tests for E42S TC-05..07, 10, 11, 16-20 and 23 through the shared load endpoint. This spec has only TC-PB-01, which uses a test double for the PARAMETER handler, and does not answer the request. | E42S `shared-updates.md` row 25; spec.md TC-PB-01 | Add a `recovery-it` test that runs the real `ParameterLoadHandler` through the load, approve and rollback endpoints for the listed cases, or record in `shared-updates.md` why not and who covers them. |
| `REVIEW-RWB-E1-043-146` | Low | Housekeeping. (a) A-37 still says "L11 before L12"; with the renumbering it is L12 before L13. (b) SPEC-027 (lines 671-675) and GAP-46 call S7 the "higher-precedence source", but RUN-BRIEF ranks all v7 story files at one level; the choice is settled by assumption, not by precedence. (c) `compliance-validation.md` §3 says "revision 5" for E42S (overlaps 144). | assumptions.md A-37; spec.md:671-675; GAP-46; RUN-BRIEF source order; compliance-validation.md §3 | Correct A-37; reword to "the operation owner's story, settled by assumption A-nn"; update the revision. |

## RWB-E1-001 handler contract: completeness

| Point | Judgement | Where |
|---|---|---|
| Check order | Complete. L1-L15 with refusal codes; the `data_product` path (no column definition, L12 skipped) is spelled out. | SPEC-025 table; §3.1 item 3 |
| What the handler supplies | Complete. Bean behind its own flag, `tableCode`, `keyColumns`, `validate`, `repeatMessage`, `apply`, `supportsRollback`, `changeSummary`; two catalog rows; message IDs in E42S's catalog. | SPEC-025; §3.1 item 2 |
| Message pass-through | Complete. First failure's code, placeholders and column at 422; `detail` lists all; `ApiProblemException` (from `access.api`) passes through. | SPEC-025; §3.1 item 4 |
| Repeat behaviour | Complete. L9 → 409 with `repeatMessage` on any date; AC10 precondition removed. Source-order departure not recorded (140). | SPEC-025 L9; §3.1 item 7 |
| Seed rows | Complete. Two CODE_LIST rows, `V<seq>__rwb_e1_043_<name>.sql` form, no column-definition key, no grants-file edit. | §3.1 item 5; A-40 |
| LOV-REF-TABLE | Complete. No change. | §3.1 item 6 |
| Effective date | **Not implementable as written** for `data_product` (138). | §3.1 items 2, 8 |

On the six points reviewed in round 3 the contract is complete. The effective-date rule added in this
revision cannot be met on Physical Schema v6 (138), so RWB-E1-001 should stay held until the
current-state mechanism is defined; the SPI signature is not expected to change. The SPI home (141)
should also be settled before RWB-E1-001 plans.

## Document gaps not recorded by the specify stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| G4-R01 | Physical Schema v6 `data_product` (`UNIQUE (product_code)`, `valid_from` only); Data Dictionary v8 DF-REF-071 (UK), DF-REF-079 | The product table holds one current row per product, but the versioned registry approves future-dated versions; S7-001 flow step 10 writes rows at approval | Story file v7 RWB-E1-043 BR3 (version in force by date); RWB-E1-043 spec revision 4 SPEC-025 *Effective date* | No | A design mechanism (refuse future approval, owner job on the date) works without a schema change | Finding 138 |
| G4-R02 | Physical Schema v6 `sys_fields` (`UNIQUE (field_id)`, no date column) | The dictionary table cannot hold a dated version | Story file v7 RWB-E1-064 flow steps 2-3 and 8 (`sys_field_version`); RWB-E1-043 spec revision 4 §3.2 item 6 | No | Same mechanisms as G4-R01; RWB-E1-064 owns the table | Finding 138 |
| G4-R03 | Story file v7 RWB-E1-043 §13 step 3 and flow step 3 (validity check before hash and idempotent return), X3, AC6 | A repeat of the version in force is refused on date before the repeat is seen | Story file v7 RWB-E1-001 AC10 (same file again → MSG-P1-011 while a version is in force) | No | The order can be chosen by assumption with owner acceptance | Finding 140 |

## Gate decision

The Medium finding 138 blocks the handoff to the Implementation Planner (`pdlc.md`). The Technical
Specifier should define the effective-date mechanism for current-state handler tables and correct the
contract to RWB-E1-001 and RWB-E1-064 (138), fix the Low findings 139-146 in the same run (D-RUN-09:
Low findings are fixed, not accepted), and record G4-R01..G4-R03. This gate then re-runs as
`review/spec-gate-review-5.md`. No finding needs a Blocker = Yes gap.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 1] [LOW: 8]
REVIEW_STATUS: FAIL
BLOCKING: YES (Medium finding 138 blocks the handoff to the Implementation Planner)
ROUND_3_FINDINGS: 131-137 resolved (132 reopened for current-state handler tables as 138; follow-ups 139, 140, 143, 144); G3-R01..G3-R05 carried in as GAP-45..GAP-49
RWB_E1_001_CONTRACT: COMPLETE on check order, handler supply, message pass-through, repeat, seed rows, LOV-REF-TABLE; effective-date rule not implementable on data_product (138); SPI home open (141)
DOCUMENT_GAPS_ADDED: 3 (G4-R01..G4-R03; no blocker)
NEXT_STEP: Technical Specifier remediation run 4 for REVIEW-RWB-E1-043-138..146, then spec gate round 5 (review/spec-gate-review-5.md).
```
