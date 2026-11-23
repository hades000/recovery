# Shared brief — WP B-P4-01 (RWB-SVC-P4 rwb-access, fanout 5)

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Run date 22 November 2026.
This brief is read by all five workers of WP `_work/msr/wp/B-P4-01.md`. The WP wins over this brief; this brief only fixes the shared facts so the fourteen files do not disagree.

## 1. Read before writing (in this order)

1. `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` — read fully. §R5.5 DP table, §R5.7 Day-1 rules, §R7.1 metadata rows, §R7.2 the 19 sections, §R8.1 header and change log, §R9 gap and assumption rows.
2. `_work/msr/plan/ownership.json` — every table and path owner you name.
3. `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` — slides 10, 11, 14, 20, 29, 35, 41, 44 and the catalogue slides.
4. `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md`.
5. `_work/msr/extract/Recovery Workbench Functional Specifications by Module v6/Recovery Workbench FSD P4 Access and administration v3.md`
6. `_work/msr/extract/Recovery Workbench Technical Specifications by Module v5/Recovery Workbench TSD P4 Access and administration v3.md`
7. Your legacy story file (path in your task), plus the thin extracts: `_work/msr/extract/Recovery Workbench Business Requirements Program v4.md`, `Recovery Workbench Business Requirements Epic 1 v4.md`, `Recovery Workbench Business Requirements Epic 2 v2.md`, `Recovery Workbench Epics 3 to 8 Specification v3.md`, `Recovery Workbench Business Rules and Routing Logic v4.md`. Fill order Template and Rules §R7.3.
8. Style precedent, mirror its voice, depth and table habits: `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1037 APP Role to permission matrix as data and PDPA field masking by role v1.md` and its `- contract v1.md` sibling, and `.../RWB-SVC-P4 rwb-access (Access and authority)/RWB P4 E1019 APP Roles, teams and queues as data v1.md`.

## 2. What you may write

Only:
- the story `.md` paths listed for your legacy key in your task;
- `_work/msr/fragments/<story-id>.json`, one per story;
- your two register shards `_work/msr/smoke/gap-B-P4-01-<compact>.jsonl` and `_work/msr/smoke/asm-B-P4-01-<compact>.jsonl` (`<compact>` = E1022, E1037, E1039, E2019, AD001). Never touch `_work/msr/gaps/B-P4-01.jsonl` or `_work/msr/assumptions/B-P4-01.jsonl`: the parent merges the shards. Never touch `_work/msr/editlog/B-P4-01.md`: the parent writes it.
- Nothing else. No master file, no other key's story, no legacy file edit, no new file under `04 User stories` other than your own paths.

## 3. File shape (hard requirements; the checks enforce the first three)

1. Line 1: `# <Story key> <Title>` — the exact `id` and `title` from your task JSON.
2. Then the two header lines of §R8.1 on their own lines:
   `SCB Collections and Recovery. Henka Group, 22 November 2026.`
   `(C) Siam Commercial Bank and Henka Pte Ltd`
3. Then `**Change log.** D-RCV-60, 22 November 2026: <one sentence on this slice>. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.`
4. Then the metadata table `| Item | Value |` with the 20 rows of §R7.1 in that exact order, none removed:
   Story key = `id`; Work type = `<WT> (<name>)` from §R5.3; Suggested owner = the fixed phrase of §R5.3 for that work type; Service = `rwb-access`; Service epic = `epic`; Wave = `wave`; Business epic = `business_epic`; Release = `release` + ` (tentative)`; Legacy key = `legacy`; Legacy disposition = `disposition`; Build status = `build_status`; Patterns applied = the `patterns` list, comma and space separated, as `DP01, DP03, …`; Parallel lane = `lane`; Ready to start = `ready`; Depends on (build) = `H` comma separated or `None`; Contract dependencies = `C` or `None`; Integration dependencies = `I` or `None`; External dependencies = `X` or `None`; PRD reference = `Pending (C1)`; Status = `Draft (realignment v1)`.
5. Then `### 1. Story` … `### 19. Out of scope`, the exact 19 names and order of §R7.2. Every section has real content; write `None.` only where the pattern of the precedent does.
6. Section 7 is a ```gherkin block. Every `Scenario: ACn <title>` line ends with either `(legacy RWB-…-nnn ACn)` or `(new, D-RCV-60)`. Nothing else on that line.
7. Section 16 is a table `TC ID | Covers | Level | Data`. Level is one of Unit, Component, Contract, Integration, End to end, NFR.
8. Section 12 has the nine sub-tables 12.1 to 12.9 as `#### 12.n <name>`, each written `None.` where empty.
9. Forbidden strings, anywhere: the word `Jira`, any person name, any email address, `Co-Authored-By`, `Generated with`. Say "the issue tracker" or nothing.
10. Never invent a value. Missing value → `Not specified in the source documents (CG-B-P4-01-<compact>-<n>; ASM-B-P4-01-<compact>-<n>)` and the matching shard rows.

## 4. Shared facts you must not contradict

- Service: `rwb-access`, code P4, wave 1, epic `RWB-SVC-P4`, folder `RWB-SVC-P4 rwb-access (Access and authority)`. Schema `rwb_access`. REST base `/api/recovery/access/v1`. Topic `rwb.access.events.v1`. Events `rwb.access.AccessPolicyChanged.v1` and `rwb.access.DoALimitChanged.v1` only — invent no third event name. Temporal task queue `rwb-access` in namespace `rwb-recovery`. Java package `th.co.scb.ace.workbench.recovery.access`. One login per service (DP-02).
- P4 owns these tables and no others (Ownership Map): `role`, `permission`, `masking_rule`, `role_conflict`, `delegation_limit`. Library objects `outbox_event`, `processed_event`, `idempotency_key` are PLT objects created in `rwb_access` by the service's own DB story.
- Not P4: `decision_log_entry` and `approval` → P7 rwb-decision; `lov_value`, `reference_row`, `reference_version`, `parameter_catalog`, `parameter_value` → P3 rwb-case; `partner`, `partner_user`, `partner_instruction` → S9 rwb-partner; `rule_package`, `rule_package_version`, `rule_row`, `rule_test_case` → P7; `feature_flag`, `feature_flag_change` → PLT.
- Access log: written through the local decision-record library (DP-03) to topic `rwb.decision-record.v1`; the central ledger and its `GET /decision-log` belong to P7. P4 never writes a P7 table.
- Operations P4 provides: `POST /api/recovery/access/v1/authorise`, `GET /api/recovery/access/v1/me/permissions`, `GET /api/recovery/access/v1/doa-limits`, `GET /api/recovery/access/v1/masking-policies` (Arch v5 slide 14 names the operations; the Ownership Map has no path row, so cite the gap), plus the two Ownership Map paths `GET /api/recovery/access/v1/admin/roles` and `GET /api/recovery/access/v1/admin/access-log`.
- Sessions: staff sign-in is ACE Common (Entra ID, MFA) through gateway-bff; the session lives in the Redis store of gateway-bff (RWB-PLT-N006-INF / RWB-PLT-EDGE). P4 holds no session table, no password and no token store (ADR-010).
- Patterns: every DP in your `patterns` list appears in the §13 pattern table with its legacy marker, its microservice pattern and the dependency added by §R5.5; a DP whose dependency is not on your own H row says "referred to; the consuming story carries the dependency".
- Naming: `/api/recovery/<short>/v1`, `rwb.<short>.events.v1`, `rwb.<short>.<Event>.v1`, `rwb-<short>`, `rwb_<name>`. Only the 19 known shorts (`source-data`, `integration`, `case`, `access`, `document`, `comms`, `decision`, `payment`, `reporting`, `agent`, `valuation`, `treatment`, `guarantee`, `litigation`, `asset`, `debtsale`, `writeoff`, `deviation`, `partner`).
- Numbers, IDs, codes, versions, field ids, message ids, group names and case ids are copied character for character from the legacy story. Do not round a date, do not retitle a message, do not renumber a field.
- `preserved` is false for every story in this WP: no story copies legacy sections 1 to 11 and 14 to 19 wholesale. The legacy acceptance criteria are carried verbatim by the APP story of the key, with the origin tag; the CON, DB, INF and OPS stories carry new criteria only and their section 2 and 18 name who owns the legacy criteria and legacy test cases.

## 5. Fragment JSON

Write `_work/msr/fragments/<id>.json` with exactly these keys, in this order:
`id, epic, service, wt, lane, ready, owner, business_epic, wave, release, legacy, disposition, H, C, I, X, acs, tcs, reqs, ops_provided, ops_consumed, events_published, events_consumed, workflows, prd_ref, gaps, assumptions, file`
- `owner` is the short code (TechX, ACE, INFRA, DEVOPS, QA), not the phrase.
- `acs` is `[{"id": "AC1", "origin": "legacy RWB-E1-022 AC1" | "new, D-RCV-60", "text_first_line": "<the Given or first line of the scenario body, character for character>"}]`.
- `tcs` is the TC ids written in your section 16 table.
- `ops_provided` / `ops_consumed` hold the REST operations without their base duplication, e.g. `POST /api/recovery/access/v1/authorise`.
- `events_published` / `events_consumed` hold event names; `workflows` holds Temporal workflow or Schedule names.
- `gaps` / `assumptions` hold every id you cite in the story files of that story.
- `file` is the story path with forward slashes, exactly as your task gives it.
- Valid JSON, UTF-8, no trailing comma.

## 6. Register shards

One JSON object per line, in `_work/msr/smoke/gap-B-P4-01-<compact>.jsonl` and `_work/msr/smoke/asm-B-P4-01-<compact>.jsonl`. Ids are `CG-B-P4-01-<compact>-<n>` and `ASM-B-P4-01-<compact>-<n>`, n from 1 in the order the rows appear in the story files, one number series per legacy key shared by all its stories.
- Gap row keys, none empty: `id, title, description, type, severity` and, following §R9, also `source, section, evidence, area, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp`. `type` is one of Missing, Conflict, Ambiguous, Outdated, ID collision. `severity` is P1, P2 or P3 — a missing value that blocks a story's Done is P2. `wp` is `B-P4-01`.
- Assumption row keys, none empty: `id, text, why` and also `read, gap, applied_in, confidence, confirm, impact, wp`. `confidence` High, Medium or Low.
- One na, one row: write **one combined gap row per story** (not one per missing field) naming every missing value in that story, one `description` with (a), (b), (c) clauses, and **one assumption row per default** you apply. Every cited id must exist in your shards and no id may be cited by two keys.
- The defaults that are always assumptions here: matrix and masking versions resolve at sign-in and stay until the session ends; a role conflict refuses the session; an unmapped or inactive group gives no role; P4 caches nothing of another service's data; the access log is written locally and published to the decision topic; break-glass is time-boxed and recorded; partner identity is resolved at the partner gateway and P4 keeps no partner table.

## 7. Self-check before you return

Run `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-P4-01 --quick` and fix every finding that names one of your own files (another worker's file may still be in flight; leave those alone and note it). Also check by eye: 20 metadata rows in order, 19 headings in order, every `Scenario: ACn` line tagged, every `CG-`/`ASM-` citation present in your shard, every TC id of your section 16 present in the fragment, no forbidden string, no unknown service short, all nine sub-tables of section 12 present.

Reply with: the story files written, the fragments written, the shard paths, the number of gap rows and assumption rows, and the quick-check result for your files.
