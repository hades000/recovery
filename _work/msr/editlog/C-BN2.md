# C-BN2 edit log

Work package: C-BN2 — Recovery Workbench Build Notes Epic 2, next version.
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Agent: aisdlc-msr-worker. Fanout: 0 (no subagent used; the WP sets fanout: 0).

## Files written

- `04 User stories/Recovery Workbench Build Notes Epic 2 v4.md`
- `_work/msr/gaps/C-BN2.jsonl`
- `_work/msr/assumptions/C-BN2.jsonl`
- `_work/msr/editlog/C-BN2.md`

Scratch builders and probes in `_work/msr/docs/C-BN2/` (input of the writer, not deliverables): `gen.py`, `registers.py`, `probe_api.py`, `probe_flags.py`, `probe_struct.py`, `probe_keys.py`, `probe_lines.py`, `probe_q.py`, `diff.py`.

No source file was edited. `04 User stories/Recovery Workbench Build Notes Epic 2 v3.md` and every other read-only input are unchanged; the v4 file sits beside v3.

## Register rows

| Register | Rows | IDs |
|---|---|---|
| Gaps (`_work/msr/gaps/C-BN2.jsonl`) | 14 | GAP-3175 to GAP-3188 |
| Assumptions (`_work/msr/assumptions/C-BN2.jsonl`) | 14 | ASM-5567 to ASM-5580 |

Counts: **14 CG rows, 14 ASM rows**. All 28 rows are cited in the document, in the "Gaps and assumptions of this version" table and where each applies; no citation in the document lacks a row, and no row is uncited (check C17 passes).

## What this version is

The v3 build notes are 42 stories of Epic 2, each with its steps written out in full, and 2185 lines of text. The realignment does not rewrite the steps. It changes what the 19-service target changes, and keeps everything else word for word:

1. Two header lines (Template and Rules R8.1), a metadata table and a change log with the v4 row "4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash". The v3 row is kept in the log with its 16 November 2026 date.
2. A front section, "How to read this version (D-RCV-60)": the 19 services with schema, login, REST base, topic and task queue; the mapping of the four legacy service identities; the mechanisms replaced, each with its DP row and register row; the lanes and Day 1 statement.
3. Per story: the module line rewritten to name the primary service and the other services of the new story set, then a realignment block with the primary service, service epic, wave, business epic, release (tentative), schema, login, REST base, topic, task queue, Java package, new stories, lanes and patterns, then a short note on what the target changes in that story.
4. Mechanism edits inside the steps, 45 literal edits, 19 API-base rewrites and 5 package renames (see below).
5. A closing "Realignment map by service and lane" table of 42 rows, a "Sources of this version" table and the gap and assumption table.

Verified unchanged: 42 story keys and titles in their source order, 330 `### Step n` headings, every AC-visible number and date of the source (for example 2026-12-14, 2026-12-15, 2026-12-31 23:59, 2,400,000.00, 12,500.00, 0.8500, 174 scenarios, 62/58/54 Tests tabs), all TC-E2-xxx-nn, MSG-xxx-nnn, LOV-xxx, RWB-E1/E2/TE identifiers and every locked artefact reference.

## Method

`gen.py` reads v3, applies a list of literal replacements where every replacement asserts its own occurrence count before it is applied, rewrites the 42 module lines, inserts the 42 realignment blocks and notes, and writes v4. If a count differs the build stops, so no edit can apply twice, apply nowhere, or land in a second place. A closing assertion checks that every source line survives in the output except the 30 distinct module-line strings it rewrote and the three superseded header lines. That is why the diff of v3 against v4 shows only insertions and the listed edits.

The per-story values are not typed by hand: the primary service, the patterns and the new stories come from `_work/msr/plan/split_plan.json` block legacy, and the lanes, wave, business epic, release and story IDs from the Service Story Catalog v1 Stories sheet. The service, schema, login, REST base, topic and task queue come from the Ownership Map Services sheet, and the job, event and table owners from its Jobs, Events, Workflows and activities, and Tables sheets.

| Edit group | Count | Example |
|---|---|---|
| Mechanism edits inside steps | 45 | JOB-05 and TimerDue replaced by a durable timer in TreatmentWorkflow |
| API bases to `/api/recovery/<short>/v1` (DP-13) | 31 occurrences, 19 prefixes | `/api/recovery/v1/cases` becomes `/api/recovery/case/v1/cases` |
| Package renames | 5 | `recovery.data.api` becomes `recovery.sourcedata.api` |
| Module lines rewritten | 42 | `Module: P2 Integration, with P8 Payments and posting` becomes the primary and other services of the new story set |
| Realignment blocks and notes | 42 each | service, epic, lanes, new stories and patterns per story |

## Values and their sources

- Primary service, other services, patterns, new stories: `_work/msr/plan/split_plan.json`, block legacy, rows primary, patterns and slices.
- Lanes, wave, business epic, release, story IDs: `04 User stories/Recovery Workbench Service Story Catalog v1.xlsx`, Stories sheet, filtered on the RWB-E2 legacy keys.
- Schema, login, REST base, topic, task queue: `22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx`, Services sheet (19 rows); the Java package root is Template and Rules R4.
- Job mechanism, event owner, table owner: the same workbook, Jobs, Events, Workflows and activities, and Tables sheets.
- DP rows, lanes, wave map, dependency classes, placeholder: `22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md`, sections R1, R3, R4, R5.5, R5.6, R5.7, R8.1, R9.
- Decision, ADR and decision log identifiers: `_work/msr/plan/ids.json`; this document introduces no new D-RCV, ADR or DL identifier.

## Rulings applied, with their register rows

| Ruling | Register |
|---|---|
| The four legacy service identities are read as the workload identity of the acting service | ASM-5567 |
| EV-26 is read as AceDataReady, the Arch v5 catalogue name | GAP-3175, ASM-5568 |
| JOB-nn identifiers stay; each mechanism is read as a Temporal Schedule or an event-started workflow | GAP-3184, ASM-5569 |
| The INT-19 extract and the data lake are removed; rwb-reporting publishes the rows and events | GAP-3178, ASM-5570 |
| The payment match rules are the PAYMENT_MATCH package; no payment_match_rule table | GAP-3179, GAP-3188, ASM-5571 |
| The PAYMENT_MATCH order is EXACT, then PARTIAL, then WINDOW | GAP-3180, ASM-5572 |
| partner_user is an S9 record in the rwb_partner sequence | GAP-3181, ASM-5573 |
| signature_request is a P5 record in the rwb_document sequence | GAP-3182, ASM-5574 |
| JOB-05, JOB-01 and JOB-09 are retired; durable timers and the view contract replace them | GAP-3176, GAP-3177, GAP-3183, ASM-5575 |
| The next-action check is a five-minute Temporal Schedule in rwb-case | GAP-3177, ASM-5576 |
| Configuration keys, message IDs, story IDs and JOB-nn identifiers keep their names | ASM-5577 |
| The primary service is the plan's primary; RWB-E2-023 falls back to its module line | GAP-3185, GAP-3187, ASM-5578 |
| EV-19 stays owned by rwb-case and is raised by the approval durable timer | GAP-3177, ASM-5579 |
| The story set is the 42 stories of v3 against 41 plan keys | GAP-3185, GAP-3186, ASM-5580 |

RWB-E2-023 is the one story with no plan row, so its realignment block, its lanes and its new stories carry the section R9 placeholder and cite GAP-3185 and ASM-5578. No business value, amount, date or identifier was invented anywhere else.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp C-BN2 --quick` — C02, C03, C05, C12, C13, C18 all PASS, 0 findings.

Run as well although outside the quick set: C14 (header), C16 (service names in topics, bases and queues), C17 (register rows and every citation resolved), C20 (tool line, no wrong attribution) — all PASS, 0 findings.

Self-checks: 42 story headings, 42 module lines, 42 realignment blocks, 42 map rows, 330 step headings against 330 in v3, no `/api/recovery/v1` left, no Quartz, Control-M or INT-19 left except the sentence that records their removal, no person name, no email address, no issue-tracker or web reference.

## Not done

No story file, no fragment, no register numbering (step D1), no issue-tracker, Confluence, GitLab, Figma or web access, no git commit. The document stays Draft, per run rule 9.
