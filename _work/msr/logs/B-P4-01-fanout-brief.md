# B-P4-01 fanout brief (lead to subagents)

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: fanout brief for WP B-P4-01, five legacy keys. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

This brief is a work split of WP `_work/msr/wp/B-P4-01.md`. The WP remains the authority. Read it top to bottom, then read the Template and Rules v1 in full. If this brief and the WP disagree, the WP wins; tell the lead in your report.

## 1. Five keys, five owners

| Key | Stories | Sidecar gap rows | Sidecar assumption rows |
|---|---|---|---|
| RWB-E1-022 | RWB-P4-E1022-APP, RWB-P4-E1022-CON, RWB-P4-E1022-DB | `_work/msr/logs/B-P4-01-E1022-gaps.jsonl` | `_work/msr/logs/B-P4-01-E1022-assumptions.jsonl` |
| RWB-E1-037 | RWB-P4-E1037-APP, RWB-P4-E1037-CON | `_work/msr/logs/B-P4-01-E1037-gaps.jsonl` | `_work/msr/logs/B-P4-01-E1037-assumptions.jsonl` |
| RWB-E1-039 | RWB-P4-E1039-APP, RWB-P4-E1039-CON, RWB-P4-E1039-DB, RWB-P4-E1039-OPS | `_work/msr/logs/B-P4-01-E1039-gaps.jsonl` | `_work/msr/logs/B-P4-01-E1039-assumptions.jsonl` |
| RWB-E2-019 | RWB-P4-E2019-APP, RWB-P4-E2019-CON, RWB-P4-E2019-INF | `_work/msr/logs/B-P4-01-E2019-gaps.jsonl` | `_work/msr/logs/B-P4-01-E2019-assumptions.jsonl` |
| RWB-AD-001 | RWB-P4-AD001-APP, RWB-P4-AD001-CON | `_work/msr/logs/B-P4-01-AD001-gaps.jsonl` | `_work/msr/logs/B-P4-01-AD001-assumptions.jsonl` |

Write only your own key's story files, its fragments and its two sidecar row files. Do not write the shared `_work/msr/gaps/B-P4-01.jsonl`, `_work/msr/assumptions/B-P4-01.jsonl` or `_work/msr/editlog/B-P4-01.md`; the lead merges the sidecars and writes the edit log. This is the WP fanout rule "each subagent writes only that key's files and its own jsonl rows", applied through a sidecar so five agents never append to one file.

## 2. Non-negotiable format

Every story file:

1. First line `# <Story key> <Title>` exactly (title without the work-type suffix).
2. Then the two header lines:
   `SCB Collections and Recovery. Henka Group, 22 November 2026.`
   `(C) Siam Commercial Bank and Henka Pte Ltd`
3. Then `| Item | Value |` and the twenty metadata rows of Template and Rules §R7.1, in order, none removed. Values:
   - Work type: `APP (App development)`, `CON (Contract)`, `DB (ACE DB)`, `INF (Infrastructure)`, `OPS (DevOps)`.
   - Suggested owner: `TechX (suggested; any team may pick up this story)`, `ACE team (suggested; any team may pick up this story)`, `SCB IT infrastructure (suggested; any team may pick up this story)`, `DevOps team (suggested; any team may pick up this story)`.
   - Release: the JSON date plus ` (tentative)`.
   - Depends on (build) = H joined with `, ` or `None`; Contract dependencies = C; Integration dependencies = I; External dependencies = X.
   - PRD reference `Pending (C1)`; Status `Draft (realignment v1)`.
4. `**Change log.** D-RCV-60, 22 November 2026: ... Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.`
5. The 19 `### n. Name` sections in order: Story, Business rationale, Preconditions, Flow, Exception paths, INVEST check, Acceptance criteria, Business rules, State transitions, Authority, Data, Contract, Solution plan, Validation and messages, Screens and states, Test cases, Guardrails, Traceability, Out of scope.
6. Section 12: all nine `#### 12.n` sub-headings, `None.` where empty. Tables have rows for the owner and use only ownership-map owners.
7. Section 16 table columns exactly `TC ID | Covers | Level | Data`; Level is one of Unit, Component, Contract, Integration, End to end, NFR.
8. Section 13 contains a "Pattern application" table with one row for every DP in the story's `patterns`, copied from §R5.5.
9. Section 7 uses a ```gherkin fenced block. Every `Scenario: ACn ...` line ends with `(legacy RWB-... ACn)` or `(new, D-RCV-60)`.

Hard language rules:
- No person's name and no e-mail address anywhere.
- Never write the word `Jira` (or `atlassian.net`). Say "the issue tracker" if you must.
- No external calls, no approvals requested, no questions. Status stays Draft.
- Never edit an existing file. Your target story files do not exist yet; if one appears, stop and report it.
- Never change a legacy file.

## 3. Acceptance criteria and test cases

- `acs` in the story JSON is the list of legacy AC IDs this APP story owns. Copy those scenarios from the legacy story **verbatim** (every Given/When/Then line, every quoted value), and only append the origin tag to the `Scenario:` line.
- If a legacy APP scenario depends on another service (case, document, partner, decision log, reference data), add **one** Given line at the top of that scenario, in the form the AD007 APP story uses:
  `Given the rwb-case contract mock returns <the exact value or answer the legacy line needs>`
  Keep every legacy line and every value. The mock is what makes the scenario testable in the P4 build; do not delete the cross-service When/Then.
- CON, DB, INF and OPS stories own no legacy AC: write 5 to 8 new ACs tagged `(new, D-RCV-60)` that test only the artefact in the headline (the contract document, the schema/grants, the network path, the deployment). Never invent a business value; if a value is missing, use the §R9 placeholder and a gap/assumption row.
- APP stories keep the legacy TC ids listed in their JSON. A TC of an AC owned by another slice is still listed and marked in `Covers`/`Data` as owned by that slice (the E1019 APP story is the model). A TC copy for integration gets `-ITG` only on the ITG story, not here.
- New ACs get new TC ids in the family `TC-<compact>-<WT>-nn` (for example `TC-E1022-CON-01`, `TC-AD001-DB-01`). Use the id style of the existing AD007 CON story.

## 4. Fragments

Write `_work/msr/fragments/<id>.json` with exactly the keys of WP item 8:
`id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file`.

- `acs` is a list of objects `{"id","origin","text_first_line"}` for **every** AC in section 7. `origin` is `legacy <legacy> ACn` or `new, D-RCV-60`; `text_first_line` is the full `Scenario: ...` line as written.
- `tcs` is the list of every TC id in section 16.
- H/C/I/X, release, lane, ready, owner, wave, business epic, legacy, disposition, service and file are copied from the story line JSON; do not "improve" them.
- `gaps` and `assumptions` are the ids you actually cite in the story. Every id must have a sidecar row.
- `ops_provided`, `ops_consumed`, `events_published`, `events_consumed`, `workflows` list the names in section 12 (empty lists allowed).

## 5. Gaps and assumptions

Every story gets at least one combined gap row and at least one assumption row, even when the gap is only a missing label. Use:
- gap id `CG-B-P4-01-<KEY>-<n>` and assumption id `ASM-B-P4-01-<KEY>-<n>`, with `<KEY>` one of E1022, E1037, E1039, E2019, AD001 and `<n>` starting at 101. A second row in the same story is 102, and so on.
- Gap keys: `id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp`.
- Assumption keys: `id, text, why, read, gap, applied_in, confidence, confirm, impact, wp`.
- `type` one of Missing, Conflict, Ambiguous, Outdated, ID collision. `severity` P1, P2 or P3. `confidence` High, Medium or Low. `wp` is `B-P4-01`.
- One combined gap row per story lists every missing value of that story; each assumption row states the default taken for one of them and names the gap id in `gap`.
- In the story, the placeholder is exactly `Not specified in the source documents (CG-...; ASM-...)`.
- Do not cite an id that has no row in your sidecars. Before you report, run a citation check.

Sidecar format: one JSON object per line, UTF-8, no BOM, no surrounding array. Append nothing to the shared files.

## 6. Naming and ownership

- Service: `rwb-access`. Schema `rwb_access`. REST base `/api/recovery/access/v1`. Topic `rwb.access.events.v1` and events `rwb.access.<Event>.v1`. Queue `rwb-access` in namespace `rwb-recovery`. Java package `th.co.scb.ace.workbench.recovery.access`.
- Shared decision-record topic `rwb.decision-record.v1`, event `rwb.decision-record.DecisionRecorded.v1` (DP-03 library).
- Owners only from `_work/msr/plan/ownership.json`:
  - P4 rwb-access: `role`, `permission`, `role_conflict`, `masking_rule`, `delegation_limit`.
  - P3 rwb-case: `lov_value`, `reference_*`, `queue`, `queue_member`, `case`, `task`, parameters and the reference-load/approve paths (`ASM-A6-api-4`).
  - P7 rwb-decision: `decision_log_entry`, rule packages.
  - S9 rwb-partner: `partner_user`, partner firms and bindings.
  - P5 rwb-document: documents.
  - P1 rwb-source-data: ACE extension tables and the source-data contract; ACE views stay in schema `recovery` and are P1's boundary.
- P4 never reads another service's tables. The only cross-service reads are contract calls with a fake (DP-11), one hop, 2 s timeout. P4's own `v_ace_*` views, where a story needs them, are DP-05 and are read by rwb-access's own login only; do not copy an ACE value into `rwb_access`.
- Do not claim `partner_user`, `lov_value`, `decision_log_entry`, `rule_package*` or the four rule tables for P4. TSD P4 v3 still lists some of them; the ownership map and its rulings win.

## 7. Per-key focus

### RWB-E1-022 (E1022)

Sources: legacy E1-022; TSD P4 v3 T3.1 (`role`, `permission`, `role_conflict`), T6.1 and T6.2; FSD P4 v3 A2.1 to A2.4 and AC-P4-001 / AC-EXC-P4-001; Arch v5 slides 13-20 and 41-44; Ownership Map rows `role`, `permission`, `role_conflict`.

- APP owns AC2, AC4, AC5, AC6, AC7, AC8, AC9 only. AC1 (SSO sign-in) and AC3 (not in group) are owned by `RWB-ITG-E1022-ITG`; do not copy them into the APP story. The APP story's background may state the sign-in context but must not claim AC1/AC3.
- CON: contract baseline for `GET /api/recovery/access/v1/admin/roles`, `GET /api/recovery/access/v1/me/session` and `POST /api/recovery/access/v1/authorise`; the Entra ID/OIDC claim shape (groups, amr), role mapping, conflict check, matrix/conflict versions, RFC 9457 envelope, message IDs MSG-P4-001/002/005/006, consumed reference-data/queue operations, fakes. `GET /admin/access-log` belongs to E1039/AD007, not here.
- DB: schema `rwb_access`, per-service login, `role` (DF-REF-034 to 039), `permission` (040 to 044), `role_conflict` (205 to 211) and `masking_rule` (198 to 204) as the service baseline that the session and masking paths read; standard record columns, keys, the `entra_group` index, Flyway sequence, PUBLIC revoke and no cross-schema grant. No `partner_user`, no `lov_value`, no `decision_log_entry`. The DB story may create `masking_rule` because E1037-APP depends on it and no other DB story in this WP owns it; say so and record the assumption.
- Likely gaps: the group naming per environment (DL40), the group-to-role refresh/leaver interval, the matrix/conflict effective-time rule (date vs timestamp), the exact OpenAPI field names, the authorise path not appearing in the ownership map (DP-08 requires it), the `role_conflict` seed values and conflict version label.

### RWB-E1-037 (E1037)

Sources: legacy E1-037 (all 13 ACs); TSD P4 v3 T3.1 (`permission`, `masking_rule`, `role`, `role_conflict`), T3.2, T6.1/T6.2; FSD P4 v3 A2.3, A2.4 and A2.5, AC-P4-003/004/005 and their exception rows; Arch v5 slides 14 and 41; ownership map `permission`, `masking_rule`.

- APP owns AC1 to AC13, all copied verbatim. Add a mock Given where the legacy When/Then crosses a service:
  - AC1 `GET /queues` and AC4/AC8 `GET /cases` and AC3 `POST /cases/{caseId}/transfer`: `Given the rwb-case contract mock returns ...` using the exact status/value of the legacy line.
  - AC6/AC10/AC13 approve: the reference-load/approve path is P3's (`ASM-A6-api-4`); mock it and keep the legacy lines.
  - AC7 decision-log store: the local DP-03 library is the store; the failure is a library failure, not a P7 call.
  - AC11 clear identity number: `Given the rwb-source-data contract mock returns ...` for `v_ace_customer`; P4 does not read `public.customer` itself.
  - AC12 case read: `Given the rwb-case contract mock returns ...`.
  - AC2, AC5, AC9 are P4's masking/validation and need no cross-service mock.
- The P4 deliverable is the permission matrix as data, the masking rule per role, the authorise/scope/masking answers and the leaver check; the load/approve UI and path stay P3's generic reference load. Say this explicitly in §1, §4 and §19, with the contract dependency `RWB-P3-E1042-CON`, `RWB-P3-E1043-CON`, `RWB-P7-E1027-CON`.
- CON: contract baseline for the role catalogue, the session/masking answer, `POST /authorise`, the matrix validation rules and the masking policy; declare the P3 reference-load/approve operations as consumed; fakes for P3 lists, P3 reference load, P7 decision-record and P1 source-data views.
- Likely gaps: the matrix file layout and row count, the approver parameter key, the masking version label, the 5-minute membership refresh value (AC8), the meaning of the clear/masked flag, the `permission` table's effective date column (TSD has no date on `permission`), the capability letter alphabet C/R/U/D/A vs CRUDA.

### RWB-E1-039 (E1039)

Sources: legacy E1-039 (all 10 ACs); TSD P4 v3 T3.1, T6.1/T6.2, API-P4-008 and API-P4-013; FSD P4 v3 A2.7 to A2.10, AC-P4-007 to AC-P4-010 and the exception rows; Arch v5 slides 14, 20, 28 and 41; ownership map `decision_log_entry` (P7) vs the local DP-03 chain.

- APP owns AC1 to AC10, copied verbatim. Add a mock Given where the legacy When/Then crosses a service:
  - AC1 case record view: `Given the rwb-case contract mock returns ...`; the P4 deliverable is the AC-READ entry.
  - AC2 `PATCH /tasks/{taskId}`: `Given the rwb-case contract mock returns ...`; the P4 deliverable is the grant and the marked entry.
  - AC3 case-list export: `Given the rwb-case contract mock returns ...`; the P4 deliverable is the AC-EXPT entry.
  - AC4 document content: `Given the rwb-document contract mock returns ...`; the P4 deliverable is the AC-READ entry before the file is returned.
  - AC8 `GET /decision-log`: `Given the rwb-decision contract mock returns ...`; the P4 deliverable is the local chain and the entry shape, and the central ledger is P7's.
  - AC7/AC9/AC10 are local DP-03/break-glass behaviour and need no service mock.
- CON: contract baseline for `POST /api/recovery/access/v1/admin/break-glass-grants`, the active-grant read (if used), the `AccessEvent`/decision-record entry shape, the local chain, the idempotency rule, the error envelope and the consumed P3/P5/P7 operations. `GET /admin/access-log` and export are AD007's; reference them, do not duplicate their contract.
- DB: the local decision-record chain table in `rwb_access` (DF-DEC-001 to 018 copy), hash-link columns, the indexes for actor/time/case/decision-code reads, the idempotency key table, the break-glass grant state (grant id, incident, area, right, scope, start/end, actor reference). No central `decision_log_entry`; that is P7's. No role/permission tables (E1022-DB owns those).
- OPS: deploy the capability: Helm values, environment configuration (break-glass window hours, retention, chain verification schedule), Kafka producer/subscription values for `rwb.decision-record.v1`, secrets/certificates, dashboards and alerts (decision-record write failure, chain break, break-glass activation), runbook and backup/restore of the local chain. The access-review Schedule is AD008's; do not claim it.
- Likely gaps: grant id format, 4-hour window (assumed), review window (1 working day, assumed), retention period, idempotency key TTL, whether `AC-SIGN` counts as an access entry, the exact AC-BGON/BGOFF codes, the chain table name, whether the local chain is one table or two, and the dashboards' thresholds.

### RWB-E2-019 (E2019)

Sources: legacy E2-019 (APP owns AC6 and AC9 only); FSD S9 and FSD P4 v3 REQ-ACA-012; TSD P4 v3 T3.1 (`role` has class PARTNER_USER) and API-P4-012; Arch v5 slides 7, 8, 17, 20, 35 and 41; Ownership Map `partner_user` (S9), `role`/`permission` (P4); the platform partner gateway story RWB-PLT-N007-INF.

- APP owns AC6 and AC9 only; copy them verbatim. AC1-AC5, AC7 and AC8 belong to `RWB-ITG-E2019-ITG`. For AC6 add `Given the rwb-partner contract mock returns ...` with the exact 404/no-data answer for the other firm's instruction; the P4 deliverable is the partner session scope and the authorise answer that makes the mock return 404. For AC9 no mock is needed; P4 rejects a bank identity on the partner route.
- The APP story is the rwb-access half: the partner role class, the partner id and `PLACED` scope in the session, the bank-identity rejection, the decision-record entry and the no-second-partner-role check. It does not own the partner firm, the instruction or the partner user row; those are S9's.
- CON: contract baseline for the partner fields of `GET /api/recovery/access/v1/me/session`, `POST /api/recovery/access/v1/authorise` for partner roles, the partner claims (issuer, identity class, partner id, role class PARTNER_USER, scope PLACED), the refusal messages, the consumed S9 partner-binding operation and the P3 reference lists, plus fakes.
- INF: the network and edge slice that lets the partner gateway reach rwb-access: DMZ-to-service mTLS route, DNS, firewall rules, ingress/WAF policy for `/api/recovery/access/v1/partner/*` or the partner-facing paths, certificate and secret ownership, rate limits, logging to SOC, and the rule that partners cannot reach any other service. Do not rebuild RWB-PLT-N007-INF; consume it.
- Likely gaps: the partner identity claim format, the partner role codes (PT-LAWFIRM, PT-VALUER, PT-AGENCY, PT-BUYER), the scope code PLACED, the S9 binding operation and its owner, the partner gateway route prefix, the certificate owner, and the rate-limit values.

### RWB-AD-001 (AD001)

Sources: `04 User stories/Recovery Workbench Administration Stories v3.md` heading RWB-AD-001 (thin, AC1-AC3, TC-AD-001-01 to 05); TSD P4 v3 T3.1 (`role.entra_group` DF-REF-039); FSD P4 v3 A2.3/A2.4 and FEAT-ADM-01; Arch v5 slides 13-14 and 41; Ownership Map `role`.

- APP owns AC1, AC2 and AC3, copied verbatim including the source wording. No cross-service mock is needed; the sign-in path is E1022-APP's and the mapping is this story's.
- The mapping is `role.entra_group` plus a version/effective-date mechanism. TSD has no validity column on `role`, so either add columns to `role` by a migration or introduce a P4-owned mapping table; do not silently invent. Record the gap and the assumption, and keep the fix in `rwb_access`.
- CON: contract baseline for the mapping read and the mapping load/effective-date rule. Prefer `GET /api/recovery/access/v1/admin/roles` (existing P4 operation) for the read and the P3 reference-load path for the load (`POST /api/recovery/case/v1/admin/reference-loads` consumed, owner P3, `ASM-A6-api-4`). Do not invent a new endpoint unless the gap/assumption says why.
- Likely gaps: the mapping version table/column, whether `role.entra_group` is unique and active-only, the environment group naming, the effective-date column, who may load/approve the mapping, and the exact endpoint path.

## 8. Self-check before you report

Run these from the workspace root; replace `<KEY>` with your key and `<files>` with your story files:

```
python -I -c "import json,glob,re,pathlib; files=[p for p in glob.glob('04 User stories/Recovery Workbench Service Story Files v1/RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 *.md') if '<KEY>' in p]; [print(p, len(re.findall(r'^### \\d+\\. ', pathlib.Path(p).read_text(encoding='utf-8'), re.M))) for p in files]"
```

Then check:
- every story has 19 `### n.` headings in order;
- the metadata rows are the twenty of §R7.1 in order;
- every `Scenario:` line has an origin tag;
- every fragment parses as JSON and has the exact key set;
- every `CG-B-P4-01-<KEY>-...` and `ASM-B-P4-01-<KEY>-...` cited in a story or fragment has a line in your two sidecars;
- every sidecar line parses as JSON and has the required keys;
- no `Jira`, no person name, no e-mail address;
- release is `(tentative)` and status is `Draft (realignment v1)`.

Do not run `run_all.py`; the lead runs it once after the merge. Report: files written, story/AC/TC counts, CG and ASM counts, any source conflict, and any target path that already existed.
