# Worker brief — WP B-PLT-LIB-01 (RWB-PLT-LIB, platform shared libraries)

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Run date: 22 November 2026.
This file is the shared brief for the five per-key workers of WP `_work/msr/wp/B-PLT-LIB-01.md`. Read it fully, then your own key brief in the task prompt.

## 1. Read before writing

1. `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md` (fully, §R5.5 DP table, §R7 template, §R9 registers).
2. `_work/msr/wp/B-PLT-LIB-01.md` (the WP).
3. Your legacy story file (path in your key brief) and `_work/msr/plan/ownership.json`.
4. `22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md` (slides 11, 14, 20, 22, 28, 29, 41, 42, 43) and `22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md` (slides 16 and 28 for the decision record).
5. House-style reference stories — copy their tone, table shapes and level of detail:
   - `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT TE006 CON Outbox and retry for outbound work - contract v1.md`
   - `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT NF02 APP Shared library baseline v1.md`
   - `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-TPL Service template and repositories/RWB PLT E1044 OPS Database migrations versioned with parameterized schema names - deployment v1.md`
   - `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1027 ITG Decision log writer v1 - integration v1.md` (the division of the legacy key between PLT, the owning service and ITG).

## 2. The split this WP records

These four legacy keys are split three ways. This WP writes only the **platform library slice**:

| Legacy key | Owning-service story (owns the legacy ACs) | Integration story | This WP's slice |
|---|---|---|---|
| RWB-E1-027 | RWB-P7-E1027-APP (central ledger) | RWB-ITG-E1027-ITG | the local decision-record library |
| RWB-E1-037 | RWB-P4-E1037-APP (matrix, masking rules, scope, access log) | RWB-ITG-E1037-ITG | the access guard and masker library |
| RWB-E1-042 | RWB-P3-E1042-APP (catalog, service, endpoints) | — | the parameters client library and its build checks |
| RWB-E1-043 | RWB-P3-E1043-APP (versioned tables and service) | — | the reference-data client library |

N009 is new (Change Register: "RFC 9457 problem and Idempotency-Key helpers - interface and fake"), so its two stories own their own delivery.

**Acceptance criteria rule for this WP.** The legacy ACs of E1-027, E1-037, E1-042 and E1-043 stay with the owning-service story named above and are **not copied here**. Every AC in your files is `(new, D-RCV-60)` and tests only the library deliverable in the title. Say this once in section 2 and once under section 7, and cite the owning story by id. Do not invent business values: reuse the values the legacy story already carries (record example "RW-2026-000123", version labels "ALLOC-2026.11", matrix version "PM-2026.11", table code "EXPOSURE_BAND", parameter key "case.entry.dpd", messages MSG-P7-009, MSG-P7-003, MSG-P4-002, MSG-P4-003, MSG-P1-002, MSG-GEN-002, MSG-GEN-004, MSG-P3-027, MSG-P3-032) and nothing else.

## 3. File shape — mandatory, checked by C02, C03, C05, C13, C16, C19

```
# <Story key> <Title>

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

**Change log.** D-RCV-60, 22 November 2026: <one sentence>. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

| Item | Value |
|---|---|
| Story key | ... |
... 20 rows, exact order and exact labels as below ...
| Status | Draft (realignment v1) |

### 1. Story
### 2. Business rationale
### 3. Preconditions
### 4. Flow
### 5. Exception paths
### 6. INVEST check
### 7. Acceptance criteria
### 8. Business rules
### 9. State transitions
### 10. Authority
### 11. Data
### 12. Contract
### 13. Solution plan
### 14. Validation and messages
### 15. Screens and states
### 16. Test cases
### 17. Guardrails
### 18. Traceability
### 19. Out of scope
```

Metadata row labels, in this order and none removed: `Story key`, `Work type`, `Suggested owner`, `Service`, `Service epic`, `Wave`, `Business epic`, `Release`, `Legacy key`, `Legacy disposition`, `Build status`, `Patterns applied`, `Parallel lane`, `Ready to start`, `Depends on (build)`, `Contract dependencies`, `Integration dependencies`, `External dependencies`, `PRD reference`, `Status`.

Fixed values for every story in this WP: `Service` = `platform`; `Service epic` = `RWB-PLT-LIB`; `Wave` = `0`; `Suggested owner` = the fixed phrase of the work type (§R5.3: TechX or DevOps team, always "… (suggested; any team may pick up this story)"); `PRD reference` = `Pending (C1)`; `Status` = `Draft (realignment v1)`. Empty dependency lists are written `None`. Empty release is written `None (new story)`; a named release is written `30 November 2026 (tentative)`.

Section 12 uses `#### 12.1 REST operations provided` … `#### 12.9 Call-type summary`, all nine present, `None` plus one sentence where empty, exactly as the TE006 and NF02 references do.

Section 16 table columns: `| TC ID | Covers | Level | Data |`, Level one of Unit, Component, Contract, Integration, End to end, NFR. No `-ITG` copy belongs to this WP.

Section 7: a fenced ```gherkin block, `Feature: …`, a `Background:` where useful, then `  Scenario: ACn <title> (new, D-RCV-60)` with Given/When/Then lines, each criterion a vertical slice that tests only the library deliverable.

## 4. Hard prohibitions (a check fails or the run is wrong)

- No occurrence of the issue-tracker product name or of `atlassian.net` anywhere (C13).
- No person names, no email addresses (C12). Users are test ids such as `U-2101`; roles are `RW-CASEOWN`, `RW-SECADM`, `RW-REFADM`, `RW-RISK`, `RW-COE`, `RW-AUDIT`, `RW-PLATADM`, `RW-COMPLY`, `RW-LEGAL`, `RW-PHONECOL`.
- The platform library is **not** one of the 19 services and has **no short name**: never write `rwb.platform.events.v1`, `/api/recovery/platform/v1`, `queue rwb-platform`, `rwb_platform` or `th.co.scb.ace.workbench.recovery.platform` as a service identity. A package name `…recovery.platform.<area>` is the library artefact, not a service.
- Never write the old base `/api/recovery/v1/` (C16). Service paths are `/api/recovery/<short>/v1/…` with `case`, `access`, `decision`, `source-data` as the Ownership Map names them.
- Only the 19 shorts may appear in `rwb.<short>.events.v1`, `/api/recovery/<short>/v1` and `queue rwb-<short>`.
- Never edit a legacy file; write only the files your key brief lists.
- Dates unchanged and every release date marked `(tentative)`.

## 5. Decoupling patterns in section 13

Section 13 carries a `**Pattern application**` table with one row per pattern listed in `Patterns applied`, columns `| DP | Legacy marker | Microservice pattern | Dependency added |`, taking the marker text and the pattern text from §R5.5 verbatim and adding one sentence on how this story applies it. For N009, `Patterns applied` = `None` and the section says so in one sentence, like NF02 does.

The dependency column names the dependency the DP table adds. On a CON story the added dependency is written as "referred to; the consuming story carries it" and the fragment `H`/`C` stay empty. On an APP story the added `H`/`C` ids go into the fragment lists and into the metadata rows.

## 6. Fragment file

`_work/msr/fragments/<id>.json`, UTF-8, 2-space indent, keys in this order and none removed:

```json
{
  "id": "...",
  "epic": "RWB-PLT-LIB",
  "service": "platform",
  "wt": "APP",
  "lane": "...",
  "ready": "Day 1",
  "owner": "TechX",
  "business_epic": "EP01",
  "wave": 0,
  "release": "30 November 2026",
  "legacy": "RWB-E1-027",
  "disposition": "Split (rework)",
  "H": [],
  "C": [],
  "I": [],
  "X": [],
  "acs": [{"id": "AC1", "origin": "new, D-RCV-60", "text_first_line": "Given …"}],
  "tcs": ["TC-PLT-E1027-CON-01"],
  "reqs": ["REQ-DRI-004"],
  "ops_provided": [],
  "ops_consumed": [],
  "events_published": [],
  "events_consumed": [],
  "workflows": [],
  "prd_ref": "Pending (C1)",
  "gaps": ["CG-B-PLT-LIB-01-E1027-2"],
  "assumptions": ["ASM-B-PLT-LIB-01-E1027-4"],
  "file": "04 User stories/…"
}
```

`acs[].text_first_line` is the first Given/Then line of that scenario in the story file, character for character. `tcs` are the TC ids of that story. `owner` is the short owner key (`TechX` or `DEVOPS`). `release` is `""` for N009. `legacy` is `N009` for the new pair.

## 7. Registers (shard files — the parent merges them)

Write your rows only to your own shard files (never to `_work/msr/gaps/B-PLT-LIB-01.jsonl` directly):

- `_work/msr/smoke/regs/B-PLT-LIB-01-<KEY>-gaps.jsonl`
- `_work/msr/smoke/regs/B-PLT-LIB-01-<KEY>-asm.jsonl`

`<KEY>` is your key as given. One JSON object per line.

Gap row keys: `id, title, source, section, description, evidence, type, area, severity, needed_by_wave, legacy_ref, owner_role, asm, proposed, wp`. Type one of Missing, Conflict, Ambiguous, Outdated, ID collision. Severity P1, P2, P3. `wp` = `B-PLT-LIB-01`.

Assumption row keys: `id, text, why, read, gap, applied_in, confidence, confirm, impact, wp`. Confidence High, Medium or Low.

Rules: **one combined gap row per story** (all the missing values of that story in one row, described in (a), (b), (c) style as the TE006 and E1072 rows do) and **one assumption row per default you adopt**. Every `CG-…` and `ASM-…` id you cite in a story file must exist in your shard, and every row must be cited by the story it belongs to. Ids: `CG-B-PLT-LIB-01-<KEY>-<n>` and `ASM-B-PLT-LIB-01-<KEY>-<n>`, numbered from 1 within your key, in the order given in your key brief. Never use a bare `CG-B-PLT-LIB-01-<n>`.

Placeholder in files: `Not specified in the source documents (CG-B-PLT-LIB-01-<KEY>-<n>; ASM-B-PLT-LIB-01-<KEY>-<n>)`.

## 8. Self-check before you return

- The 20 metadata rows exist, in order, before `### 1.`.
- The 19 headings exist, in order, spelled as above.
- Every `Scenario: ACn` line ends with `(new, D-RCV-60)`, and the same AC ids appear in the fragment with the exact first line.
- No forbidden string of section 4 (search your files for `atlassian`, `Jira`, `platform/v1`, `rwb.platform`, `/api/recovery/v1/`).
- Every cited `CG-…`/`ASM-…` id exists in your shard and your shard rows are all cited.
- Section 12 has all nine sub-tables; section 16 has the Level column; section 18 has the requirement rows from your `reqs`.
- The file header and change-log line are present; the change-log line names D-RCV-60 and the tool line.
- Run `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-LIB-01 --quick` and report the result. Findings that name a file of another key of this WP are not yours to fix; findings on your own files must be fixed.
