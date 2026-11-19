# Spec gate review, round 2: RWB-E1-043 (RUN_ID `INC-008-epic-1-RWB-E1-043`)

| Field | Value |
|---|---|
| Review ID | `REVIEW-RWB-E1-043-SPEC-002` |
| Gate | Specification gate, round 2 (Compliance Reviewer, bounded review) |
| Artefacts reviewed | `specify/spec.md` revision 2, `assumptions.md`, `document-gaps.md`, `shared-updates.md`, `compliance-validation.md`, `contracts/backend-apis.json`, `contracts/frontend-integrations.json`, `gate-response.md`, `agent-run-log.md` (all 2026-11-18). The `*.run1.*` files were used as the audit trail only. |
| Previous round | `review/spec-gate-review.md` (`REVIEW-RWB-E1-043-SPEC-001`, FAIL: 3 High, 7 Medium, 9 Low, G-R01..G-R10) |
| Sources checked | Story files v7: RWB-E1-043 (file v2), RWB-E1-001, -019, -022, -025, -037, -038, -042, -064, -069, RWB-TE-011; Decision Log v10 (D-RCV-28, D-RCV-29); API Specification v4.0.0 (load, approve, rollback, `RollbackRequest`); Error and Message Standard v4 (MSG-P1-002/003/011, MSG-P3-015, MSG-P3-027); Physical Schema v6 (`reference_version` DDL, Reference data permission seed, role seed); Build Sequence v6; RWB-E1-042 spec (revision 4, 2026-11-18, and revision 3 `spec.run2.md`); RWB-E1-001 spec revision 2 (INC-009); `AI-SDLC-BUILD-LOG.md` §1 (D-RUN-07..D-RUN-13); contexts (`backend-context.md`, `backend-standards.md`, `testing-standards.md`); rules (`pdlc.md`, `specification-execution-gates.md`); repository `backend/` (`SecurityConfig`, `ApiExceptionHandler`, `ApiError`, `RecoveryFlags`), `infra/mock-oidc/config.json`, `frontend/src/api/schema.d.ts` |
| Reviewer | Compliance Reviewer (agent run), 2026-11-18. No question asked (L-RCV-03). No file other than this review was written. |

**About the run rulings.** D-RUN-07..D-RUN-11, the round-1 triage and the dictionary-load cross-story
input were given by the orchestrator, Claude Code, an AI agent. They are not human decisions or human
acceptance, and this review does not treat them as such. The spec and its companions attribute them
correctly (spec §0, `gate-response.md` header, `document-gaps.md` header).

## Status

**`SPEC_GATE: FAIL`**

| Severity | Count | Effect |
|---|---|---|
| Critical | 0 | |
| High | 0 | |
| Medium | 4 | Blocks the handoff to the Implementation Planner |
| Low | 7 | Visible; human disposition required |

The revision is a large improvement. All three round-1 High findings are resolved, and so are the
round-1 Medium findings, with the limits noted below. Four new Medium problems block the handoff. Three
of them are about the cross-story contracts that this revision added: the handler registry, the
dictionary route and the per-table access lists. The fourth is two coverage rows that are marked
COVERED but are not built and tested by this story.

## Round-1 findings: resolution check

| Round-1 ID | Sev | Verdict | Evidence checked |
|---|---|---|---|
| 101 Rollback dropped | High | **Resolved** | SPEC-024 builds the registry operation and the endpoint. The API v4 rollback operation (line 5004, right U, `RollbackRequest.reason`) matches. The MSG-P3-015 text matches Message Standard v4. S7-019 AC2, AC7 and X4 are reflected. TC-RB-01/02 are present. GAP-10 now names RWB-E1-019 and D-RUN-10. Moving E1-019's build step 5 here rests on an AI ruling (see 130). |
| 102 Logging vs AC3/BR7 | High | **Resolved** | SPEC-014 binds the log line to the reader, on hit and miss. TC-E1-043-03 uses two consumers that share one cache. There is no user ID or row content in the line. |
| 103 Shared endpoint | High | **Resolved** under D-RUN-10 | SPEC-026 and SPEC-030 call only `ParameterLoadHandler` (`load`, `approve`, `rollback`, `find`). The signatures match RWB-E1-042 spec revision 4 §12.1 exactly. The flag-off contract (`ObjectProvider`, 404 MSG-P4-003) agrees with E42S SPEC-021. Column definitions are loaded through the PARAMETER branch (SPEC-022, SPEC-029). GAP-24 is Blocker = No on an AI ruling (see 130). |
| 104 Rights per area | Medium | **Resolved, new defects** | Per-table lists fail closed (SPEC-027). RW-COE gets no built-in table. The list design opens a self-modification path and claims an acceptance that no human gave (122). The designated approvers lack area right A (126). |
| 105 Story lines missing | Medium | **Mostly resolved** | The §"Requirement lines built by another story" table names owners for separation of duty, SY-RULES, the DQ report and the engine part of BR6. The RW-AUDIT read row is still COVERED (123). |
| 106 Audit | Medium | **Resolved** | SPEC-028 records LOAD, APPROVE and ROLLBACK, both done and refused. The TC-11 "refusal is logged" clause is restored. RWB-E1-039 is the seam. Actor attribution is noted under 129. |
| 107 Catalog bypass | Medium | **Resolved** | SPEC-029 adds 38 rows to the catalog file with owner, type and default. E42S revision 3 line 96 (revision 4 line 106) says "A new key also needs a migration in the story that adds it". `CODE_LIST` exists in the E42S §7.1 types. TC-CAT-01 is present. |
| 108 RWB-E1-001 not told | Medium | **Resolved, one stale option** | The shared update to RWB-E1-001 cites PS6 lines 8, 1437, 1471-1483 and D-RCV-28. It still offers a `CREATE TABLE IF NOT EXISTS` option that D-RUN-12 now forbids (124). |
| 109 GAP-08 misses E1-019 | Medium | **Resolved, new defect** | GAP-08 now names `ReferenceTableCheck`, `ReferenceRollbackHandler` and `QueueVersionApplier`, and `detail` lists every failed row. The SPI drops the handler's own message IDs (120). E1-064's `DataDictionaryLoader` is missing (121). |
| 110 Security tests | Medium | **Resolved** | SEC-01..SEC-14 cover 401 on each endpoint, wrong capability, wrong table, author approval, unknown `loadId`, 503, and the cache never serving a non-approved version. The reason for not using 400 is recorded (GAP-28). |
| 111 Citation | Low | Resolved | SPEC-020 cites PACK §6.2 and OI-E1-042-004. |
| 112 Story requirement IDs | Low | Resolved | §0, coverage rows, GAP-29. |
| 113 NFR applicability | Low | Resolved | §NFR applicability covers NFR-RWB-001..010. |
| 114 Trigger exemption | Low | Resolved | SPEC-001 narrowed the exemption, A-33, TC-MG-01. |
| 115 "No CREATE" | Low | Resolved | SPEC-001 is reworded. |
| 116 Owner acceptance | Low | Resolved, incomplete | §Owner acceptance lists A-01, A-08, A-09/34, A-16, A-17, A-27, A-31, A-33. The list omits the AI rulings it relies on (130). |
| 117 Message/status gaps | Low | Resolved | GAP-27, GAP-28. |
| 118 CapabilityCheck overlap | Low | Resolved | Reuses E42S `CapabilityCheck.has` (E42S revision 4 SPEC-020). The multi-module scope is flagged for the plan gate. |
| 119 Flag-off bean | Low | Resolved | SPEC-018, A-23, TC-FL-01. |
| G-R01..G-R10 | — | Carried in | Recorded as GAP-20..GAP-29 with "Raised by" and resolutions. Counts verified: 38 gaps, 26 C and 12 M; 36 assumptions; 50 coverage rows; 14 lines owned elsewhere. |

### What holds (verified)

- Every quote spot-checked is accurate. This covers:
  - D-RCV-29 ("Later dictionary changes are reference loads through RWB-E1-043", Decision Log v10 line 78).
  - S7-037 line 46 `rwb.refload.approver.masking_rule=RW-COMPLY` and BR3; S7-038 line 43 `rwb.refload.approver.delegation_limit=RW-RISK`.
  - TE-011 §10 (RW-COMPLY "Owns which fields are personal") and §12 Input.
  - API v4 rollback (right U, `RollbackRequest`) and the approve description.
  - MSG-P3-015 wording.
  - PS6 `rollback_reason varchar(400)`.
  - E1-019 flow step 8 (RW-REFADM calls rollback) and §12 rollback contract.
  - E42S revision 4 `ParameterLoadHandler`, `CapabilityCheck.has`, `VersionDecisionRecorder` (transactional, `Propagation.MANDATORY`).
- Maker-checker is enforced in the service and by a DB CHECK. The per-version row key is restored. The append-only trigger is narrowed. The cache never serves a non-approved version.
- No business value, role or threshold is written as a literal. Lists, definitions and the TTL are catalog keys. Role grants are in a data file.
- The frontend is correctly `NOT_APPLICABLE`. The generated types already carry `RollbackRequest` (3 occurrences in `schema.d.ts`). The 80% backend gate on lines, statements, branches and functions is planned.
- No personal data, secret or production data is in any artefact. Test users are random UUIDs. Log and audit lines carry no user ID or row content.
- The AI-orchestrator rulings are attributed as such, and no artefact presents them as human acceptance.

## Findings

### Medium

| ID | Severity | Finding | Evidence | Affected | Fix required |
|---|---|---|---|---|---|
| `REVIEW-RWB-E1-043-120` | Medium | **The handler SPI contract conflicts with the two stories that must use it, and the conflict is not recorded.** (a) SPEC-025 runs the generic checks first for every handler code. It needs a `refdata.columns.<code>` definition and refuses the load without one, and it merges handler failures "as SPEC-003" into a 422 MSG-P3-027. SPEC-006 answers an identical repeat with a silent 201. Story v7 RWB-E1-001 §12 and X4-X7 require refused `data_product` loads to return MSG-P1-003, -004 or -007, and a repeat of the version in force to return MSG-P1-011. RWB-E1-001 AC7 expects MSG-P1-003 for a missing owner user ID, but a required-column generic check would answer MSG-P3-027 first. Story v7 RWB-E1-019 AC4 and AC5 expect MSG-P1-002 and MSG-GEN-002 from its `ReferenceTableCheck`. `RowCheckFailure.messageCode` exists, but no rule puts it into the response. (b) RWB-E1-001 spec revision 2 SPEC-013 states that "E1-043 holds no column definition for `data_product`", so its handler owns structure checks. This spec instead makes a definition and two list keys a precondition, "without them the load is refused", and passes that to RWB-E1-001 only through a shared update. As specified, `data_product` stays refused unless RWB-E1-001 changes its spec. That is close to the "refused by design" outcome that D-RUN-11 rules out. None of this is in `document-gaps.md`. | S7-001 lines 67-70, 139-162, 232; S7-019 lines 113-120; E01S SPEC-013 (spec.md ~line 381); spec.md:228-236, :449-460, :260-265; shared-updates.md:65 | SPEC-RWB-E1-043-002, -003, -006, -025; D-RUN-11; RWB-E1-001, RWB-E1-019 | Define the handler path so that the owning story's contract can be met. Make the column definition optional for a handler code: when it is absent, `validate` is the only structure check. Make the response take the message ID and placeholders of the first `RowCheckFailure`, with MSG-P3-027 only for generic failures. Let a handler supply the repeat outcome, or record why it cannot. Record the conflicts with RWB-E1-001 §12 and spec SPEC-013 and with RWB-E1-019 AC4 and AC5 as gaps. Extend TC-HD-01 and TC-HD-03 to assert a handler message ID and a `data_product` load with no column definition. |
| `REVIEW-RWB-E1-043-121` | Medium | **The dictionary route is assigned to the wrong story, and GAP-37 is contradicted by a source the spec did not read.** SPEC-031, GAP-37, A-36 and three shared updates name RWB-E1-001 as owner of the data-dictionary handler, and say "no dictionary code exists". Story v7 RWB-E1-064 (Build Sequence v6 order 13, which depends on RWB-E1-043) defines table code `sys_fields` and states that the reference data service "accepts a load for table code `sys_fields` and hands approved rows to P1". Its `DataDictionaryLoader` validates and applies the load, and it is approved through this story's approve endpoint. RWB-E1-001 spec revision 2 lists the "dictionary endpoint (E1-064)" as out of scope. RWB-E1-064 §11 also marks `sys_fields.is_personal` (DF-REF-105) as **Read**. A dictionary load in v7 therefore does not change the personal-data mark. The `is_personal` control in SPEC-031 and its open item are aimed at a write path that the owning story does not have. GAP-08 omits `DataDictionaryLoader`. RWB-E1-064 is not in the sources the remediation run read (agent-run-log). | S7-064 lines 25, 36, 42, 50, 58, 174-175, 206, 230; E01S spec.md line 153; spec.md:173, :544-568; document-gaps.md GAP-08, GAP-37; shared-updates.md:66-68; agent-run-log.md:52-56 | SPEC-RWB-E1-043-025, -031; coverage row DL10 D-RCV-29; GAP-08, GAP-37 | Read story v7 RWB-E1-064. Name it as owner of the `sys_fields` handler. Add `DataDictionaryLoader` to GAP-08. Readdress the shared updates on the handler, `changeSummary` and approver to RWB-E1-064, with RW-COMPLY and the data architect for the approver. Correct GAP-37. Restate the `is_personal` analysis against RWB-E1-064 §11, which makes it read-only through the load. Say which path, if any, can change the mark (TE-011 §10, DL26), and move the open item there. |
| `REVIEW-RWB-E1-043-122` | Medium | **The per-table access lists can be rewritten by a PARAMETER load, and A-31 claims a human acceptance that has not been given.** The loader and approver lists are PARAMETER values (`rwb.refload.*`, SPEC-027, SPEC-029). A PARAMETER load approved by any role in `rwb.refload.approver.parameter` (default RW-COE, RW-RISK) can widen any table's lists. That includes the dictionary approver list that SPEC-031 relies on for RW-COMPLY's control, and the PARAMETER list itself. So two RW-COE holders, one loading and one approving, can grant RW-COE the approval of any table. Story v7 RWB-E1-037 BR3 says "A version is approved by the role the parameter names for the table". E42S CLAR-013 leaves owner-per-key approval routing undefined. A-31 reads "Risk accepted by the access owner: a PARAMETER load can change the lists…". No human has accepted it, and the same assumption is on the owner-acceptance list. Presenting an acceptance that was not given breaks AGENTS.md §4.10 and the run brief. | assumptions.md A-31; spec.md:483-502, :515-532, :557-561; S7-037 line 192; E42S revision 4 CLAR-013 (line 876) | SPEC-RWB-E1-043-027, -029, -031; NFR-RWB-005 | Remove the acceptance wording from A-31 and record the risk as open for the access owner and Risk. Close the path, or record it as a gap with a named seam. For example: a PARAMETER load that changes any `rwb.refload.*` key needs an approver from a fixed role set that the access owner names (RW-RISK, or the key's `owner_role`). The approver list of a key must not be widened by a member of that same list alone. Add a security test, a PARAMETER load that widens `rwb.refload.approver.<code>`, with the expected outcome. |
| `REVIEW-RWB-E1-043-123` | Medium | **Two coverage rows are COVERED but are not built and tested by this story.** (1) The row "S7 §13 done-when (SIT)" (version 1 of each of the 12 tables approved in SIT) maps to SPEC-022. SPEC-022 calls this an operational task that depends on column definitions owned by other stories. Those stories are all later in Build Sequence v6: RWB-E1-038 is order 22, -019 is 25, -025 is 30, -045 is 31, -046 is 32, and -028 is 47, which mentions SERVICE_LEVEL and LEGAL_PERIOD. The spec names no owner for the PRODUCT, REGION, EXPOSURE_BAND, SERVICE_LEVEL or LEGAL_PERIOD definitions ("Seed ownership"; shared update "…"). No test is listed. (2) The row "S7 §10 RW-REFADM, RW-AUDIT reads" is COVERED by a Java method. The human read path (`GET /admin/lists`) has no owner (GAP-34). The spec's own rule is "A row is COVERED only when this story builds and tests it". | spec.md:100-101, :128, :140, :391-394, :637-645; shared-updates.md:80; Build Sequence v6 rows 22, 25, 30, 31, 32, 47 | SPEC-RWB-E1-043-011, -022; `REQUIREMENT_COVERAGE_RESULT` | Move both rows to "built by another story" or give them a partial status, with the owner and the dependency. For the SIT done-when, name an owner for each of the 12 definitions, or record the missing owners as a gap. Record that this story's done-when cannot be met until the latest content story merges, and say how this story's SIT exit is judged until then. Correct the counts in the status lines. |

### Low

| ID | Severity | Finding | Evidence | Fix required |
|---|---|---|---|---|
| `REVIEW-RWB-E1-043-124` | Low | The shared update to RWB-E1-001 still offers "create them with `CREATE TABLE IF NOT EXISTS`". D-RUN-12 (2026-11-17 23:49) says each table is created by exactly one migration, and that RWB-E1-001 does not create a table an earlier-merged story created. RWB-E1-001 spec revision 2 T8 already leaves the two tables out. The spec does not cite D-RUN-12. | shared-updates.md:64; build log line 35; E01S spec T8 (line 202) | Drop the second option. Cite D-RUN-12 as an AI-orchestrator ruling. |
| `REVIEW-RWB-E1-043-125` | Low | SPEC-031 says no dictionary change takes effect without approval by a non-author on the approver list. A rollback of a handler code is a single-person action, checked against the loader list (SPEC-024, SPEC-027). `onRolledBack` re-applies the earlier rows. The open item on removing the `is_personal` mark does not mention rollback. | spec.md:400-426, :492-494, :557-568; shared-updates.md:67 | State the rollback path in SPEC-031. Restoring an earlier approved version is not a new approval, so say so explicitly. Add rollback to the open item for RW-COMPLY. |
| `REVIEW-RWB-E1-043-126` | Low | The interim grants file gives Reference data A only to RW-RISK and RW-COE (A-08). The sources name other approvers: RW-COMPLY for the dictionary (A-36), RW-TEAMMGR for QUEUE (S7-019 flow step 4), RW-DATASTEW for `data_product` (S7-001 flow step 9) and RW-SECADM for the permission matrix (S7-037). The area check would refuse each of them until RWB-E1-037 (order 27) replaces the grants. RWB-E1-001 (order 9), RWB-E1-064 (13) and RWB-E1-019 (25) merge before that. The shared update asks only "before RWB-E1-043 SIT exit". SPEC-027's list of the PS6 seed also omits RW-COMPLY RU (PS6 line 5660). | assumptions.md A-08, A-36; shared-updates.md:71; PS6 lines 5369, 5630, 5660, 5679 | State that a story that names a new approver role adds that role's interim A grant, or that this story adds the grant. Fix the needed-by date. Complete the seed list. |
| `REVIEW-RWB-E1-043-127` | Low | A-07 parses the token `sub` as a UUID and answers 401 otherwise. This works with the local mock, whose `sub` values are UUIDs (`infra/mock-oidc/config.json`). In Microsoft Entra ID, `sub` is a pairwise opaque string; the object ID `oid` is the GUID. Revision 1's `oid` was the Entra form. As written, every admin call could answer 401 against the bank tenant in SIT. | assumptions.md A-07; `SecurityConfig` (`setPrincipalClaimName("sub")`); README environment table (SIT/UAT use the bank tenant) | Record the claim choice as an environment risk for RWB-E1-022, with a test against a non-UUID `sub`. Or take the user ID through a seam that RWB-E1-022 replaces. |
| `REVIEW-RWB-E1-043-128` | Low | The spec, A-25 and the contracts cite RWB-E1-042 spec revision 3, "spec gate not yet re-run". Revision 4 (2026-11-18 00:21) is now current. Its `ParameterKeys.byName(String key, Class<T> type)` takes two arguments, while A-26 assumes `byName(String)`. No change in behaviour was found. | spec.md §0 tag E42S; assumptions.md A-25, A-26; E42S revision 4 front matter, §12.1 | Re-baseline on revision 4 and correct A-26. |
| `REVIEW-RWB-E1-043-129` | Low | The audit events carry no actor, so a refused privileged attempt cannot be attributed until RWB-E1-039 arrives (A-30). backend-context says structured logs carry "user ID". BS-4.6 and the inventory v4 (DF-REF-166/167) treat staff IDs as personal. The conflict is not recorded. | backend-context.md line 138; backend-standards.md BS-4.4, BS-4.6; A-30; spec.md:504-513 | Record the conflict as a gap for the DPO. State how a refusal is correlated to an actor in the meantime (for example through `traceId` and the access log of the identity provider), or accept the gap explicitly. |
| `REVIEW-RWB-E1-043-130` | Low | The owner-acceptance list covers the labelled assumptions but not the AI-orchestrator rulings the spec depends on. D-RUN-10 and D-RUN-11 settle GAP-24 (Blocker = No), GAP-10 (rollback moved from RWB-E1-019's build step 5), GAP-31 and GAP-36. The dictionary cross-story input shaped SPEC-031. These are not document precedence and not human decisions, so they need human ratification before planning. | spec.md:731-737; document-gaps.md GAP-10, GAP-24, GAP-31, GAP-36; build log lines 33-34 | Add D-RUN-10, D-RUN-11 and the dictionary input to §"Owner acceptance needed before planning". Name the human owner of each: the tech lead, and the RWB-E1-019 and RWB-E1-001 owners. |

## Document gaps not recorded by the specify stage

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| G2-R01 | Story file v7 RWB-E1-001 §12 and X4-X7 (MSG-P1-003, -004, -007; repeat MSG-P1-011); Story file v7 RWB-E1-019 AC4, AC5 (MSG-P1-002, MSG-GEN-002) | Handler refusals and repeats need the owning story's message IDs; this spec's SPI answers MSG-P3-027 or a silent 201 and makes a column definition mandatory | RWB-E1-043 spec rev 2 SPEC-003, -006, -025; RWB-E1-001 spec rev 2 SPEC-013 | No | The SPI can carry handler message IDs; settled by design | Finding 120 |
| G2-R02 | Story file v7 RWB-E1-064 §3, §4, §11, §12 (`sys_fields` table code, `DataDictionaryLoader`, `is_personal` Read) | Dictionary handler owner and code exist; the spec says none exists and names RWB-E1-001 | DL10 D-RCV-29; RWB-E1-043 spec GAP-37; RWB-E1-001 spec rev 2 (dictionary endpoint out of scope) | No | Story v7 names the owner | Finding 121 |
| G2-R03 | Story file v7 RWB-E1-037 BR3 ("approved by the role the parameter names for the table") | No source says who approves a change to the `rwb.refload.*` approver keys themselves | RWB-E1-042 spec rev 4 CLAR-013 (owner routing not encoded); RWB-E1-043 spec A-31 | No | A fixed approver set can be defaulted and accepted by the access owner | Finding 122 |
| G2-R04 | Backend context v2.0 line 138 (logs carry user ID) | Conflicts with the rule that staff IDs are personal and kept out of logs | Backend standards BS-4.6; Data Classification and Personal Data Inventory v4 DF-REF-166/167 | No | Interim adapter without actor is possible; RWB-E1-039 replaces it | Finding 129 |
| G2-R05 | Story file v7 RWB-E1-043 §13 done-when (12 tables approved in SIT) | Content and column definitions come from stories built later; five tables have no named owner | Build Sequence v6 orders 22-47; story files v7 RWB-E1-028, -045 | No | SIT exit can be scheduled against the content stories | Finding 123 |

## Gate decision

The Medium findings block the handoff to the Implementation Planner (`pdlc.md`). The Technical
Specifier should revise `spec.md`, `assumptions.md`, `document-gaps.md` and `shared-updates.md` for
findings 120-123, and fix the Low findings 124-130 in the same run. This gate then re-runs as
`review/spec-gate-review-3.md`. No finding needs a Blocker = Yes gap: each can be settled from the
story files v7 or by a labelled assumption that a human owner accepts.

```text
SPEC_GATE: FAIL [CRITICAL: 0] [HIGH: 0] [MEDIUM: 4] [LOW: 7]
REVIEW_STATUS: FAIL
BLOCKING: YES (Medium findings 120-123 block the handoff to the Implementation Planner)
ROUND_1_FINDINGS: 101-119 resolved (104, 105, 108, 109, 116 with follow-ups 120-126, 130); G-R01..G-R10 carried in as GAP-20..GAP-29
DOCUMENT_GAPS_ADDED: 5 (G2-R01..G2-R05; no blocker)
NEXT_STEP: Technical Specifier remediation run 2 for REVIEW-RWB-E1-043-120..130, then spec gate round 3 (review/spec-gate-review-3.md).
```
