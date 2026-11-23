# B-P4-05 brief — ten rwb-access stories, five legacy keys of Epic 8

Scratch brief written by the parent worker for the five subagents of WP `B-P4-05`. Not a deliverable and not listed in the edit log.

Decision: **D-RCV-60**. Tool line everywhere: **T3 Code / OpenCode / DeepSeek v4.1 Flash**. Run date: 22 November 2026.

## 0. What each subagent writes

For **one** legacy key, four to six files and nothing else:

1. `<folder>/RWB P4 E80NN APP <title> v1.md`
2. `<folder>/RWB P4 E80NN CON <title> - contract v1.md`
3. `_work/msr/fragments/RWB-P4-E80NN-APP.json`
4. `_work/msr/fragments/RWB-P4-E80NN-CON.json`
5. `_work/msr/logs/B-P4-05-E80NN-gaps.jsonl` (one combined journey gap row for the key)
6. `_work/msr/logs/B-P4-05-E80NN-assumptions.jsonl` (one row per default of the key)

The parent merges the two jsonl files into `_work/msr/gaps/B-P4-05.jsonl` and `_work/msr/assumptions/B-P4-05.jsonl`, writes the edit log and runs the checks. **Never write the shared `_work/msr/gaps/` or `_work/msr/assumptions/` files, never write another key's files, never run `run_all.py`, never edit an existing file.**

`<folder>` = `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P4 rwb-access (Access and authority)`

## 1. Model to follow

Read these two files before writing; match their shape, tone and depth:

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 AD007 APP Access log search and export v1.md`
- `.../RWB P4 AD007 CON Access log search and export - contract v1.md`

Also useful: `.../RWB P4 AD011 APP Load a rule version v1.md` (how a missing cross-service contract dependency is recorded, not invented).

## 2. File skeleton (both work types)

```
# <Story key> <Title>

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

| Item | Value |
|---|---|
| Story key | ... |
... 20 rows, §R7.1 order, none removed ...

**Change log.** D-RCV-60, 22 November 2026: split from <legacy key> for rwb-access. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

### 1. Story
...
### 19. Out of scope
```

Metadata rows, in this exact order and with these exact values (only `Story key`, `Work type`, `Patterns applied`, `Parallel lane`, `Depends on (build)`, `Contract dependencies` change per story):

| Item | Value |
|---|---|
| Story key | `<id>` |
| Work type | `APP (App development)` or `CON (Contract)` |
| Suggested owner | `TechX (suggested; any team may pick up this story)` |
| Service | `rwb-access` |
| Service epic | `RWB-SVC-P4` |
| Wave | `4` |
| Business epic | `EP08` |
| Release | `30 June 2027 (tentative)` |
| Legacy key | `RWB-E8-00N` |
| Legacy disposition | `Split (rework)` |
| Build status | `Not started` |
| Patterns applied | `DP03, DP06, DP07, DP13, DP19` (E8006) or `DP03, DP06, DP13, DP19` (E8007, E8008, E8009, E8010) |
| Parallel lane | APP: `L-P4-AZ` (E8006), `L-P4-BA` (E8007), `L-P4-BB` (E8008), `L-P4-BC` (E8009), `L-P4-BD` (E8010); CON: `CG-W4` |
| Ready to start | `Day 1` |
| Depends on (build) | APP: `RWB-P4-E80NN-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-E1043-CON, RWB-PLT-N001-CON` (E8006, five) or `RWB-P4-E80NN-CON, RWB-PLT-E1027-CON, RWB-PLT-E1042-CON, RWB-PLT-N001-CON` (E8007-E8010, four); CON: `None` |
| Contract dependencies | E8006: `RWB-P3-E1042-CON, RWB-P3-E1043-CON`; E8007-E8010: `RWB-P3-E1042-CON`; CON: `None` |
| Integration dependencies | `None` |
| External dependencies | `None` |
| PRD reference | `Pending (C1)` |
| Status | `Draft (realignment v1)` |

Every APP story is Day 1 because its build list holds only CON stories (§R5.7 rules 1 and 8). Do not add or drop an H, C, I or X value.

## 3. The 19 sections (§R7.2)

`### 1. Story` · `### 2. Business rationale` · `### 3. Preconditions` · `### 4. Flow` · `### 5. Exception paths` · `### 6. INVEST check` · `### 7. Acceptance criteria` · `### 8. Business rules` · `### 9. State transitions` · `### 10. Authority` · `### 11. Data` · `### 12. Contract` · `### 13. Solution plan` · `### 14. Validation and messages` · `### 15. Screens and states` · `### 16. Test cases` · `### 17. Guardrails` · `### 18. Traceability` · `### 19. Out of scope`

Section 12 has exactly nine sub-tables, `#### 12.1` to `#### 12.9`, written `None` inside where empty:
12.1 REST operations provided · 12.2 REST operations consumed · 12.3 Events published · 12.4 Events consumed · 12.5 Workflows and activities · 12.6 Schedules · 12.7 Tables owned · 12.8 Contract fakes · 12.9 Call-type summary.

Section 16 table columns: `TC ID | Covers | Level | Data`. Level ∈ Unit, Component, Contract, Integration, End to end, NFR.

## 4. Acceptance criteria (§R7.2 s7, WP item 4)

- Every `Scenario:` line ends with an origin tag: `(legacy RWB-E8-00N ACn)` or `(new, D-RCV-60)`.
- AC1 and AC2 are the legacy criteria **copied word for word**; only the tag is appended to the `Scenario:` line. AC1 additionally gets one `Given the <service> contract mock returns <x>` line as its **first** line, keeping every legacy line below it unchanged.
- AC3 to AC5 (APP) and AC1 to AC6 (CON) are `(new, D-RCV-60)` and test **only** the deliverable in the title. No invented business values: use references, codes, versions, counts, dates and roles only. Where a number would be a business value, use a row reference or a count, or take the value from the source documents (the DoA design gives `L6 — THB 100m, 30% loss` and `THB 120m`; DOA-2026.11 / DOA-2027.01 / ENTRY-2027.01 / REF-2026.11 / PAR-2026.11 are document-sourced version labels you may reuse).
- Wrap the block in a ```gherkin fence; use a `Background:` with the SIT environment, the test users and their roles.

APP AC map for every key: AC1 legacy journey · AC2 legacy not-recorded · AC3 the role without the right is refused with MSG-P4-002 (this is the legacy `Access` test) · AC4 / AC5 the two new behaviours named in §B below.

CON: six new criteria — the document validates; the schemas/fields are fixed; the event or the state set is fixed; one envelope and its message IDs; the consumed operations are declared as consumed; the fakes match and carry no personal data. Adapt the third and sixth to the story.

## 5. Test cases (§R7.2 s16, WP item 5)

Keep all four legacy ids of the key: `TC-E8-00N-01` (AC1), `-02` (AC2), `-03` (AC3, legacy `Access`), `-04` (AC2, legacy `Principle 5`, Level NFR). Add `TC-E8-00N-05` (AC4) and `TC-E8-00N-06` (AC5). CON stories carry `TC-E8-00N-CON-01` to `-06`. No `-ITG` id anywhere (no ITG story is split from these keys). One closing paragraph: where the full test lives, how the legacy levels map (System→Contract, Access→Component, Resilience→NFR), and that the legacy rows are kept.

## 6. Service facts (use these exact forms)

- Service `rwb-access` (P4), schema `rwb_access`, REST base `/api/recovery/access/v1`, topic `rwb.access.events.v1` with event names `rwb.access.<Event>.v1`, Temporal task queue `rwb-access` in namespace `rwb-recovery`, Java package `th.co.scb.ace.workbench.recovery.access`.
- Own tables (ownership map): `role` (DF-REF-034 to 039), `permission` (DF-REF-040 to 044), `masking_rule` (DF-REF-198 to 204), `role_conflict` (DF-REF-205 to 211), `delegation_limit` (DF-REF-016 to 026 and 055 to 062). Platform library objects created in `rwb_access`: `outbox_event`, `processed_event`, `idempotency_key` (DP-09, ASM-A6-tables-8). The local decision-record chain of the DP-03 library (EV-08 `rwb.decision-record.DecisionRecorded.v1` on `rwb.decision-record.v1`).
- **Not ours, never read:** `lov_value`, `reference_version`, `reference_row` (P3, ASM-A6-tables-5, read through DP-07 only where the pattern list has DP07); `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` (P7, ASM-A6-tables-3); `template`, `notice`, `merge_field` (P6); `partner_user` (S9, ASM-A6-tables-6); `case`, `task`, `assignment`, `queue` (P3); `decision_log_entry` (P7 — the central ledger; this service writes the local chain only).
- Rights are `permission.letters` (C, R, U, D, A or `-`) per capability area; the areas used here are `PLATFORM_ADMINISTRATION`, `RULES_AND_PARAMETERS` and `REFERENCE_DATA` (LOV-CAPABILITY, 14 values).
- TSD P4 v3 T6.1 rights: RW-COE `CRUD` in Rules and parameters and `R` in Platform administration; RW-RISK `RA` in Rules and parameters; RW-PRODHEAD `R`; RW-PLATADM `R` and `CRUD` in Platform administration; RW-SECADM `CRUDA` in Platform administration; RW-AUDIT `R` in both; RW-COMPLY `R` and `R`; RW-REFADM `CRUD` in Reference data; RW-CASEOWN and RW-PHONECOL `R` and `-`.
- Messages you may use (do not invent text): `MSG-P4-001` You have no Recovery Workbench role. Ask your team manager to request one. · `MSG-P4-002` You cannot {action} here. Your role does not include it. · `MSG-P4-004` Emergency access is on until {time}. Every action is recorded. · `MSG-GEN-001` Enter {field}. · `MSG-GEN-004` Someone else changed this record. Reload it to see their change. · `MSG-P7-002` (author cannot approve, TSD P4 T6.3) · `MSG-P7-003` The action was not taken because the decision could not be recorded. Try again in a few minutes. · `MSG-P3-022` (change checklist item missing, TSD P4 T6.3). `MSG-P4-003` This case is not in your scope. (E8-010 legacy only.)
- Change checklist of seven items (TSD P4 T6.3, DF-REF-295): request, impact, test result, approver, load, verify, rollback plan.
- DP table rows (§R5.5) to copy into `13. Solution plan` — pattern application table, four columns `DP | Legacy marker | Microservice pattern | Dependency added`:
  - DP-03 `DecisionLogWriter, decision log` → `Local decision-record library and topic rwb.decision-record.v1` → `H RWB-PLT-E1027-CON`
  - DP-06 `Parameters, casewf.config` → `Parameters contract of rwb-case and the client library` → `H RWB-PLT-E1042-CON; C RWB-P3-E1042-CON`
  - DP-07 `Reference data, LOV` → `Reference-data contract of rwb-case` → `H RWB-PLT-E1043-CON; C RWB-P3-E1043-CON` (E8006 only)
  - DP-13 `/api/recovery/v1` → `/api/recovery/<short>/v1` → `none`
  - DP-19 `Screen, ace-web` → `gateway-bff composite route` → `H RWB-PLT-N001-CON`
- ESCAPE HATCH on ownership: where a story must call another service's operation that the WP metadata does not carry as a C dependency (P7 rule packages, P6 templates, P3 reference loads), call it through its **contract and fake** and record the missing dependency in the key's one combined gap row and in its assumption rows — exactly as `RWB P4 AD011 APP Load a rule version v1.md` does. Never add the dependency to the metadata.

## 7. Gaps and assumptions (WP item 9, §R9)

**One combined gap row per story** (the APP and the CON of a key cite the same ids):

```
{"id":"CG-B-P4-05-E80NN-101","title":"<short title>","source":"<files>","section":"<sections>","description":"<every missing value of the key, comma separated>","evidence":"<what the sources do and do not say>","type":"Missing|Conflict","area":"Contract|Data|Business rule","severity":"P2","needed_by_wave":"4","legacy_ref":"RWB-E8-00N","owner_role":"Tech lead","asm":"ASM-B-P4-05-E80NN-101","proposed":"<what the story does instead>","wp":"B-P4-05"}
```

**One assumption row per default** (2 or 3 per key), ids `ASM-B-P4-05-E80NN-101`, `-102`, `-103`:

```
{"id":"ASM-B-P4-05-E80NN-101","text":"<the default>","why":"<why a default is needed>","read":"<how it was read>","gap":"CG-B-P4-05-E80NN-101","applied_in":"<sections>","confidence":"Medium","confirm":"<who confirms it>","impact":"<what changes if wrong>","wp":"B-P4-05"}
```

Every `CG-`/`ASM-` id cited in a story file must exist in a jsonl row of this key. Cite the same gap id wherever a value is missing and write the literal placeholder `Not specified in the source documents (CG-B-P4-05-E80NN-101; ASM-B-P4-05-E80NN-10M)` with the matching ASM id. Never invent a business value or a business message text.

## 8. Fragment JSON (WP item 8)

```json
{
  "id": "...", "epic": "RWB-SVC-P4", "service": "rwb-access", "wt": "APP|CON",
  "lane": "...", "ready": "Day 1", "owner": "TechX", "business_epic": "EP08", "wave": 4,
  "release": "30 June 2027", "legacy": "RWB-E8-00N", "disposition": "Split (rework)",
  "H": [...], "C": [...], "I": [], "X": [],
  "acs": [{"id": "AC1", "origin": "legacy RWB-E8-00N AC1", "text_first_line": "Scenario: AC1 ... (legacy RWB-E8-00N AC1)"}, ...],
  "tcs": ["TC-E8-00N-01", ...],
  "reqs": ["REQ-..."],
  "ops_provided": ["GET /api/recovery/access/v1/..."],
  "ops_consumed": ["POST /api/recovery/access/v1/authorise", ...],
  "events_published": ["rwb.decision-record.DecisionRecorded.v1"],
  "events_consumed": [],
  "workflows": [],
  "prd_ref": "Pending (C1)",
  "gaps": ["CG-B-P4-05-E80NN-101"],
  "assumptions": ["ASM-B-P4-05-E80NN-101", "..."],
  "file": "04 User stories/.../RWB P4 E80NN APP <title> v1.md"
}
```

`H` and `C` are the metadata values as a list. `release` in the fragment is `30 June 2027` without the word tentative (the file carries `(tentative)`), as in the existing fragments. `tcs` is the list of the file's table. `reqs` per key: E8006 `REQ-ACA-002, REQ-ACA-003, REQ-CWC-006, REQ-ACA-013`; E8007 `REQ-CWC-013, REQ-CWC-014, REQ-DRI-010, REQ-ACA-013`; E8008 `REQ-ACA-004, REQ-DRI-010, REQ-ACA-013`; E8009 `REQ-S2-004, REQ-DRI-010, REQ-ACA-013`; E8010 `REQ-OCC-001, REQ-OCC-002, REQ-ACA-013`.

## 9. Hard prohibitions (checked)

- No name of a person anywhere, no e-mail address, no `Co-Authored-By`, no `Generated with [Claude Code]`.
- The words `Jira` and `atlassian.net` must not appear.
- `/api/recovery/v1/` must not appear (only `/api/recovery/access/v1`, `/api/recovery/case/v1`, `/api/recovery/decision/v1`, `/api/recovery/comms/v1`).
- Only these service shorts after `/api/recovery/` or `rwb.` or `queue rwb-`: access, case, decision, comms, source-data, document, reporting, agent, integration, payment, valuation, treatment, guarantee, litigation, asset, debtsale, writeoff, deviation, partner.
- Reference dates unchanged; every release date carries `(tentative)`; never raise a date as a gap.
- No git command, no network, no issue tracker, no Figma.

---

# B. The five keys

## B1. RWB-E8-006 — Run the full administration screens (FEAT-ADM-01)

Legacy: `04 User stories/Recovery Workbench User Stories Epics 3 to 8 v3.md` heading `## RWB-E8-006` (line ~15075). FSD P4 v3 A2.17. Endpoints of the legacy story: `POST /admin/reference-loads` and `POST /admin/rule-versions` — **both are other services'** now (`POST /admin/reference-loads` is P3 under ASM-A6-api-4, the rule-version paths are P7 under ASM-A6-api-3). `GET /admin/roles` is already built by `RWB-P4-E1019-APP`, `/me/session` and `/admin/access-log` likewise by other P4 stories. Do not duplicate them.

**Slice.** The administration home in `rwb-access`: one read that tells the caller, area by area, what of the administration surface they are entitled to open, and records the open in the decision log with the versions in force.

- Provided: `GET /api/recovery/access/v1/admin/home` → `AdminHome`: `areas[]` (`capabilityArea`, `letters`, `scope`, `mayOpen`), `matrixVersion`, `maskingVersion`, `listVersion`, `roleClass`, `chain`, `recordedAt`. One row per capability area in force (LOV-CAPABILITY, 14 values, read through DP-07 with the version in force); `letters` from the caller's `permission` rows, `scope` from `role.default_scope`, `mayOpen` true where the letters are not `-` and the area is not a read-only area.
- Every call appends one decision-record entry of DP-03 (the library's read code, the two versions, the caller reference, the areas answered, no case id) in the same transaction as the answer; if it cannot be written the answer is withheld with 503 and MSG-P7-003 (AC2).
- 403 with MSG-P4-002 for a caller without `PLATFORM_ADMINISTRATION` R; 401 with MSG-P4-001 for no session.
- DP-06 supplies the cache lifetime of the entitlement answer as a parameter row (`access.home.cache.ttl.seconds`), read with the version in force; flag the name as not specified.
- The "one place" is structural: the gateway-bff composite route of DP-19 composes the home from this answer plus each owner's own panel list (P3 queues and parameters, P6 templates, S9 panels, P10 autonomy), so no panel is shown that this answer does not entitle.
- Consumed: own `POST /api/recovery/access/v1/authorise`; P3 `GET /api/recovery/case/v1/admin/parameters`; P3 `GET /api/recovery/case/v1/admin/lists/{listCode}`.
- No workflow, no Schedule (JOB-18 is `RWB-P4-AD008-APP`'s), no event of its own: only `rwb.decision-record.DecisionRecorded.v1`.

**AC1 mock line:** `Given the rwb-case contract mock returns reference version "REF-2026.11" in force with LOV-CAPABILITY, LOV-SCOPE and LOV-ROLE-CLASS`.
**AC3:** a caller with RW-PHONECOL (`-` in Platform administration) calls the home and is refused 403 with MSG-P4-002, no answer and no entry.
**AC4:** the answer carries one row per area of the reference list in force, `mayOpen` true only where the caller's letters are not `-`, and `matrixVersion`, `maskingVersion`, `listVersion` on the answer; a changed matrix version changes the answer with no build.
**AC5:** every open appends exactly one entry with the caller reference, the two versions and the areas answered, and a forced write failure withholds the answer (503, MSG-P7-003).

**Defaults (2-3):** the home read and its composition (`ASM-...-101`); the cache lifetime parameter (`-102`); the record code of a home read is the library's read code (`-103`).
**Gap:** the operation, its fields, the parameter name, the entitlement rule of an area and the record code are not in the sources.

**CON.** OpenAPI 3.1 for `GET /admin/home`; `AdminHome` and `AdminHomeArea` schemas; 401/403/503 envelope with MSG-P4-001, MSG-P4-002, MSG-P7-003; consumed declarations (own authorise, P3 parameters, P3 lists); the `rwb.decision-record.DecisionRecorded.v1` declaration; five fakes (authorise, decision-record, parameters, reference-data, gateway-bff). Publisher sign-off: the APP story, `RWB-PLT-N001-CON` (SCR-43 route) and the wave 4 access journey harness.

## B2. RWB-E8-007 — Change a decision rule through the administration screens (FEAT-ADM-02)

Legacy heading `## RWB-E8-007`. FSD P4 v3 A2.18; TSD P4 v3 T4 (version states LOADED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED) and T6.3 (change checklist, checksum, author and approver, decision-log linkage). The rule registry is P7's (ASM-A6-tables-3, ASM-A6-api-3); the load gate is `RWB-P4-AD011-APP` and the approval `RWB-P4-AD012-APP` — **do not duplicate them** and do not build-depend on them.

**Slice.** The rule-change request: the administration record that binds a registry version, its test evidence and its approval into one change the screen and the audit can read.

- Provided 1: `POST /api/recovery/access/v1/admin/rule-changes` — body `packageCode`, `versionId`, `validFrom`, `reason`, `checklist` (the seven items of TSD P4 T6.3); `Idempotency-Key` required. Steps: authorise `RULES_AND_PARAMETERS` C; read the version through P7 `GET /api/recovery/decision/v1/admin/rule-packages/{packageCode}/versions`; read the test evidence through P7 `GET /api/recovery/decision/v1/admin/rule-package-versions/{versionId}/dry-run`; refuse a version not in state `LOADED` with 409 and MSG-GEN-004; refuse an incomplete checklist with 422 and MSG-P3-022 naming the missing item; append the change to the local decision-record chain (DP-03) with `changeId`, `versionLabel`, `dryRunCounts`, `testResult`, `validFrom`, the author reference and `approverRole` `RW-RISK`; answer 201 with `changeId`, `packageCode`, `versionLabel`, `testResult`, `dryRunCounts`, `validFrom`, `state` `REQUESTED`, `approverRole` and `Location`.
- Provided 2: `GET /api/recovery/access/v1/admin/rule-changes/{changeId}` — the change with its version state read through P7 (LOADED, APPROVED, IN_FORCE) and its record fields.
- The approval (`POST /admin/rule-package-versions/{versionId}/approve`) and the 00:01 promotion (JOB-20, `RulePackageInForce` EV-30) are **P7's**, out of scope; the four-eyes rule is `RW-COE` authors and `RW-RISK` approves, `MSG-P7-002` when the author tries to approve.
- Consumed: own `POST /authorise`; P3 `GET /admin/parameters`; P7 version read; P7 dry run. Published: `rwb.decision-record.DecisionRecorded.v1` only.
- No workflow, no Schedule, no own event.

**AC1 mock line:** `Given the rwb-decision contract mock returns package version "ENTRY-2027.01" in state "LOADED" with test result "PASS" and the dry-run counts`.
**AC3:** an incomplete checklist (the `verify` item missing) is refused 422 with MSG-P3-022 naming `verify`, no registry call is made for the change and no entry is written. (Covers the legacy `Access` test as the same refusal shape; add the 403 MSG-P4-002 case in the same scenario or in the exception table.)
**AC4:** a version not in `LOADED` (already `IN_FORCE`) is refused 409 with MSG-GEN-004, and the version in force still decides cases.
**AC5:** the change entry carries the version label, the dry-run counts and the test result, and answers `approverRole` `RW-RISK` with `canApprove` false for the author; the registry refuses the author's approval with MSG-P7-002.

**Defaults:** the change request is a rwb-access record with the registry consumed and faked (`-101`); the seven-item checklist is the change checklist (`-102`); the record code of an administrative change is the library's administrative-change code (`-103`).
**Gap:** the missing P7 rule-package contract dependency, the operation and its fields, the record code.

**CON.** OpenAPI for the two operations; `RuleChange`, `RuleChangeChecklist` schemas; the version state set of TSD P4 T4; the 409/422/503 envelope; consumed declarations incl. the two P7 reads as consumed; the record message; fakes (registry, parameters, decision-record, authorise, gateway-bff). State that no rule table is named as this service's.

## B3. RWB-E8-008 — Move an approval limit (FEAT-ADM-03)

Legacy heading `## RWB-E8-008`. FSD P4 v3 A2.19; TSD P4 v3 T3.1 `delegation_limit` (DF-REF-016 to 026, 055 to 062) and T6.1 (RW-COE `CRUD`, RW-RISK `RA` in Rules and parameters); Architecture v5 slides 14 and 41 (P4 owns the DoA table; `rwb.access.events.v1` carries `DoaLimitChanged`); Temporal and Drools design (DoA versions DOA-2026.11 and DOA-2027.01, `L6 — THB 100m, 30% loss`, the same case at THB 120m moving to L5). The whole-version load, its approval and its rollback are `RWB-P4-E1038-APP`'s and the lookup `GET /doa-limits` is `RWB-P4-E2013-APP`'s — **do not duplicate them**.

**Slice.** One limit moved: the change control on a single `delegation_limit` row, approved by Risk and published as `DoaLimitChanged`.

- Provided 1: `PATCH /api/recovery/access/v1/doa-limits/{delegationLimitId}` — body `principalLimit`, `lossPctLimit`, `minPricePctFmv`, `maxLossAmount`, `validFrom`, `reason`; `Idempotency-Key` required. Authorise `RULES_AND_PARAMETERS` U; write a **new** `delegation_limit` row (`limit_version` next, `state` `PENDING_APPROVAL`, `valid_from`, `version`, the author reference), leaving the row in force untouched; append the move to the local chain (DP-03) in the same transaction; answer 200/201 `moveId`, `delegationLimitId`, `limitVersion`, `state` `PENDING_APPROVAL`, `validFrom`, `approverRole` `RW-RISK`.
- Provided 2: `POST /api/recovery/access/v1/doa-limits/{delegationLimitId}/approve` — authorise `RULES_AND_PARAMETERS` A; the author cannot approve (403 with MSG-P7-002); set the pending row `IN_FORCE` from `valid_from`, set the superseded row's `valid_to` to the day before, publish `rwb.access.DoaLimitChanged.v1`, append the approval to the chain in the same transaction; answer the limit with its new version and state.
- Consumed: own `POST /authorise`; P3 `GET /admin/parameters` (the move bounds and the six-monthly review flag as parameter rows). Published: `rwb.access.DoaLimitChanged.v1` and `rwb.decision-record.DecisionRecorded.v1`.
- No workflow (the approval is synchronous and the four-eyes rule is a right, not a state); no Schedule (JOB-18 is another story's).
- Event payload: `delegationLimitId`, `limitVersion`, `decisionCode`, `approvalLevel`, `productGroup`, `effectiveFrom`, `reason`, no holder or substitute reference, no personal data.

**AC1 mock line:** `Given the rwb-case contract mock returns parameter version "PAR-2026.11" in force with the move bounds`.
**AC3:** a caller with RW-PRODHEAD (R only) patches a limit and is refused 403 with MSG-P4-002, no row and no entry.
**AC4:** a move leaves the row in force readable and the lookup answers the old limit until the approval; after the approval the new version is `IN_FORCE` from its `valid_from` and the old row carries `valid_to` the day before.
**AC5:** the author cannot approve (403, MSG-P7-002); an approval by RW-RISK publishes exactly one `rwb.access.DoaLimitChanged.v1` carrying the version, the decision code, the level, the product group and the date, and neither the holder nor the substitute reference.

**Defaults:** the move creates a new row version in `PENDING_APPROVAL`, the in-force row is superseded only on approval (`-101`); the supersede date rule (`-102`); the event payload (`-103`).
**Gap:** the operation and its fields, the missing reference-data list check for the decision codes, levels and product groups (the pattern list has no DP07 and the C list no `RWB-P3-E1043-CON`), the state set.

**CON.** OpenAPI for the two operations; `DoaLimitMove` and `DoaLimit` schemas with the TSD field names (DF-REF-016 to 026, 055 to 062); the state set `PENDING_APPROVAL`/`IN_FORCE`/`SUPERSEDED`; AsyncAPI declaration of `rwb.access.DoaLimitChanged.v1` on `rwb.access.events.v1`; the envelope; fakes (authorise, parameters, decision-record, DoA fixture DOA-2026.11/DOA-2027.01, gateway-bff).

## B4. RWB-E8-009 — Set the treatment policy by product (FEAT-ADM-04)

Legacy heading `## RWB-E8-009`. FSD P4 v3 A2.20; Program BRD `REQ-S2-004` (settlement terms inside a rule-set range, anything outside needs approval, owner Product head) and `REQ-DRI-010` (a parameter catalog holds every threshold, limit and name, versioned); TSD P4 v3 T3.2 (LOV-PRODUCT MORTGAGE, HIRE_PURCHASE, SSME, UNSECURED). Parameters and reference data are P3's (ASM-A6-tables-5, ASM-A6-api-4) and the reference-load operations belong to P3; `RWB-P4-AD009-APP` and `RWB-P4-AD010-APP` already own the load of a list version and the approval of a load in this service — **do not duplicate them**.

**Slice.** The product policy edition: a product's bands, floors and ranges enter as a file the product head uploads on the administration screen; `rwb-access` checks the right and the edition's shape, hands the file unchanged to the parameters owner and records the edition with the load id it answers.

- Provided 1: `POST /api/recovery/access/v1/admin/product-policies` — multipart `file` (the edition workbook: one sheet each for the bands, the floors and the ranges) plus query `productGroup`, `policyVersion`, `validFrom`, `reason`; `Idempotency-Key` required. Authorise `RULES_AND_PARAMETERS` C; check the three row kinds are present and the dates are ordered (422 with MSG-GEN-001 naming the part or the field); hand the file unchanged to P3 `POST /api/recovery/case/v1/admin/reference-loads` with table `product_policy` and `validFrom`; append the edition to the local chain with the returned `loadId`, `productGroup`, `policyVersion` and the version label; answer 201 `editionId`, `productGroup`, `policyVersion`, `loadId`, `state` `LOADED`, `validFrom`.
- Provided 2: `GET /api/recovery/access/v1/admin/product-policies/{productGroup}` — the editions of the product with the one in force, read through P3 `GET /api/recovery/case/v1/admin/parameters` and the load state; no values are interpreted, only the version labels and states are answered.
- Consumed: own `POST /authorise`; P3 `GET /admin/parameters`; P3 `POST /admin/reference-loads`; P3 `GET /admin/reference-loads/{loadId}` if needed (name it as consumed and flag it).
- Published: `rwb.decision-record.DecisionRecorded.v1` only. No workflow, no Schedule, no own event.
- **The rights conflict is the point of this key:** the legacy permission table gives C to RW-COE and A to RW-RISK, the FSD makes the product head primary, and TSD P4 v3 T6.1 gives RW-PRODHEAD R only. R-PREC puts the TSD above the story master, so the product head proposes (R is enough to open the screen and to upload an edition for approval), and the C letter is RW-COE's and the A letter RW-RISK's. Record this as the key's gap (`type` `Conflict`) with its assumption.

**AC1 mock line:** `Given the rwb-case contract mock returns load "LOAD-2027-000118" in state "LOADED" for product group "MORTGAGE" and version "MORT-POL-2027.01"`.
**AC3:** a caller without `RULES_AND_PARAMETERS` C is refused 403 with MSG-P4-002 and no file is read (covers the legacy `Access` test).
**AC4:** an edition missing the floors sheet, or with `validFrom` before the version in force, is refused 422 with MSG-GEN-001 naming the part or the field, and the parameters owner is not called.
**AC5:** a version that the parameters owner refuses is answered 409 with MSG-GEN-004 and nothing is recorded; the accepted edition is answered with `loadId` and `state` `LOADED` and one entry is appended carrying `productGroup`, `policyVersion` and `loadId`.

**Defaults:** the edition travels as a file through P3's reference-load contract and the values stay with P3 (`-101`); the four-eyes/rights reading of the product head (`-102`); the edition is recorded with its load id and version (`-103`).
**Gap (type Conflict):** the missing `RWB-P3-E1043-CON`/reference-load dependency, the table code `product_policy`, the operations and fields, and the rights conflict.

**CON.** OpenAPI for the two operations (multipart + read); `ProductPolicyEdition` schema with `editionId`, `productGroup`, `policyVersion`, `loadId`, `state`, `validFrom`; the state set from LOV-VERSION-STATUS (LOADED, VALIDATED, APPROVED, IN_FORCE, SUPERSEDED, ROLLED_BACK, REFUSED); the envelope; consumed declarations; fakes (reference-load, parameters, authorise, decision-record, gateway-bff).

## B5. RWB-E8-010 — Add a letter template with Compliance approval (FEAT-ADM-05)

Legacy heading `## RWB-E8-010`. FSD P4 v3 A2.21; Program BRD `REQ-OCC-001` and `REQ-OCC-002` (notices from templates approved by Legal; letter templates versioned, the approval recorded against the version); TSD P4 v3 T6.3 (author and approver, the author cannot approve, MSG-P7-002). Templates are P6 `rwb-comms`'s (ownership map `template`, API `POST /admin/templates`, `POST /admin/templates/{templateId}/approve`, `GET /admin/templates`) — this service never reads `template`, `notice` or `merge_field`.

**Slice.** The Compliance approval gate on a letter template version: the authority to approve, the four-eyes rule and the record of who approved which version, with the template itself owned by `rwb-comms`.

- Provided 1: `POST /api/recovery/access/v1/admin/template-approvals` — body `templateId`, `templateVersion`, `productGroup`, `approvalReference`, `validFrom`, `reason`; `Idempotency-Key` required. Authorise `RULES_AND_PARAMETERS` A; read the template through P6 `GET /api/recovery/comms/v1/admin/templates/{templateId}`; refuse a template not in state `DRAFT` with 409 MSG-GEN-004; refuse an approval by the version's author with 403 MSG-P7-002; hand the approval to P6 `POST /api/recovery/comms/v1/admin/templates/{templateId}/approve`; append the approval to the local chain with the template id, the version, the approving role and the time; answer 201 `approvalId`, `templateId`, `templateVersion`, `state` `APPROVED`, `approvedByRole`, `approvedAt`, `validFrom`.
- Provided 2: `GET /api/recovery/access/v1/admin/template-approvals/{templateId}` — the approvals of a template: version, state, approving **role code**, time and approval reference; never a name.
- Consumed: own `POST /authorise`; P3 `GET /admin/parameters`; P6 `GET /admin/templates/{templateId}`; P6 `POST /admin/templates/{templateId}/approve`.
- Published: `rwb.decision-record.DecisionRecorded.v1` only. No workflow, no Schedule, no own event.
- The approving role is RW-COMPLY (Compliance and PDPA officer) per the FSD role table, with RW-RISK holding A in the legacy table; record the difference in the assumption rows, not in a metadata change.

**AC1 mock line:** `Given the rwb-comms contract mock returns template "TPL-SETTLE-EN" version "3" in state "DRAFT" for product group "MORTGAGE"`.
**AC3:** a caller with RW-CASEOWN (R only) is refused 403 with MSG-P4-002 and no approval is recorded (covers the legacy `Access` test).
**AC4:** the approval of a template that is not `DRAFT`, or by the author of the version, is refused (409 MSG-GEN-004, 403 MSG-P7-002) and nothing is recorded.
**AC5:** the history answers the version, the state, the approving role code and the time for each version, no name, and the same version cannot be approved twice (`Idempotency-Key` replays the first answer).

**Defaults:** the template lives in `rwb-comms` and this story is the approval gate and the record (`-101`); the approving role and the four-eyes rule (`-102`); the history answers role codes only (`-103`).
**Gap:** the missing `RWB-P6-...` C dependency, the operations and fields, the approval-reference shape.

**CON.** OpenAPI for the two operations; `TemplateApproval` schema; the state set (DRAFT, APPROVED, WITHDRAWN as the template states, and the approval states); the envelope with MSG-P4-001, MSG-P4-002, MSG-GEN-004, MSG-P7-002, MSG-P7-003; consumed declarations for the two P6 operations; the record message; fakes (template, authorise, parameters, decision-record, gateway-bff).
