# A10-CTX — Update AI-SDLC workspace contexts to Arch v5

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60
Agent: aisdlc-context-updater
Date: 22 November 2026
WP: A10-CTX (fanout: 0; no subagents used)

## Files written

| # | File | Purpose |
|---|---|---|
| 1 | `22 Microservice Realignment/aisdlc/.github/contexts/realignment-v5-context.md` | New v5 context: 19 services, ownership, call types, events, jobs, Temporal, rules, data, edge, security, compliance, delivery, conflicts, sources, guidance |
| 2 | `_work/msr/gaps/A10-CTX.jsonl` | 22 candidate gap rows `GAP-0001` to `GAP-0022` |
| 3 | `_work/msr/assumptions/A10-CTX.jsonl` | 24 candidate assumption rows `ASM-0011` to `ASM-0034` |
| 4 | `_work/msr/editlog/A10-CTX.md` | This edit log |
| 5 | `_work/msr/docs/A10-CTX/notes.md` | Scratch provenance note (sources read, output counts) |
| 6 | `_work/msr/docs/A10-CTX/make_rows.py` | Scratch generator for the two jsonl files |

The workspace index `22 Microservice Realignment/aisdlc/.github/contexts/context-manifest.json` was
also updated: one `files` entry for `realignment-v5-context.md` (`CTX-REALIGN-RWB-V5`, owner Context
Updater, status READY) and `D-RCV-60` added to `decisions_applied`. The WP body directs this
("add it to context-manifest.json copy in the workspace only") although the `Write only` list does
not name it; the exception is recorded as `ASM-0034`. The manifest is an index, no context
content was changed in it, and the original AI-SDLC repository in folder 17 was not touched.

## What was done

1. Inventoried all nine files in `22 Microservice Realignment/aisdlc/.github/contexts/` and read the
   five canonical contexts, the two standards files, the README and the manifest. Each of the five
   canonical files exists and is substantive, so no missing or empty context was found and no
   `MISSING_CONTEXT_HANDOFF` is raised. They are v2 (16 November 2026) and now stale against
   D-RCV-60; that is recorded as `GAP-0019` / `ASM-0029` and left for a later context run
   because this run may not edit them.
2. Read the two text extracts cover to cover (51 + 32 slides), the Template and Rules (§R1, §R3,
   §R5, §R8, §R9), the Ownership Map workbook (9 sheets) and `ownership.json`, plus `split_plan.json`
   (`stats` and `legacy` only) and `ids.json`.
3. Wrote one new context file instead of editing the v2 files. It keeps every service code, schema,
   topic, queue, event number, job number, workflow name, ADR and DL id, volume and date of the
   sources; every release date carries "(tentative)".
4. Applied R-PREC for every conflict and used the Ownership Map for every owner: 19 services, 93
   tables, 156 endpoints (summarised by owner and by service), 30 events, 22 jobs, 15 workflows and
   71 rulings. The 15 table rulings and the API and flow rulings that a story is most likely to hit
   are tabled with their `ASM-A6-*` assumption ids.
5. Captured the v5 technical truth in the same file, within one ownership boundary per section:
   call types and contracts (§6), events (§7), jobs and the overnight chain (§8), Temporal (§9),
   rules and the decision log (§10), data (§11), edge/security/AI/compliance (§12). Front-end detail
   is explicitly `N/A` for v5 (no screen inventory or design system in the v5 sources) and stays in
   `frontend-context.md` v2 (`GAP-0017`). Test detail is recorded as v5 obligations with the
   standards-file delta flagged (`GAP-0021`).
6. Recorded 22 conflicts, gaps and ambiguities as candidate pairs, one gap row and one assumption
   row each, plus two standalone assumptions: Arch v5 treated as the target although six decisions
   are open (`ASM-0033`) and the manifest index update (`ASM-0034`).
7. Added the required change-log row to the new file:
   `3.0, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`.

## Counts

| Kind | Count | IDs |
|---|---:|---|
| Services catalogued | 19 | P1–P10, S1–S9 |
| Tables with an owner | 93 | §5.2 of the context file |
| Endpoints summarised by owner | 156 | §5.1 |
| Events catalogued | 30 | EV-01 to EV-30 |
| Jobs catalogued | 22 | JOB-01 to JOB-22 |
| Workflows catalogued | 15 | §9.2 |
| Decoupling patterns | 20 | DP-01 to DP-20 |
| Architecture decisions | 11 | ADR-013 to ADR-023 |
| Decision Log rows | 6 | D-RCV-60, DL44 to DL49 |
| Candidate gaps | 22 | `GAP-0001` .. `GAP-0022` |
| Candidate assumptions | 24 | `ASM-0011` .. `ASM-0034` |

## Conflicts carried into the registers

The full table is §14 of the new context file. The high-severity items: Temporal version 1.30+ vs
1.28.1 vs 1.29.7 (`GAP-0007`), BOT approval route under FPG 19/2560 clause 5.5
(`GAP-0010`), Kafka hosting (`GAP-0011`), the 19 schemas, logins and connection budget
(`GAP-0012`) and the ACE Common contracts (`GAP-0013`). All are P1 and gate wave 0 or
wave 1.

## Verification

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp A10-CTX --quick` — all six checks
  PASS after the edit log was written: C02, C03, C05, C12, C13, C18.
- C14 (document header), C17 (gap and assumption rows and citations) and C20 (tool line) run
  directly over the same file list: all PASS.
- C19 (planned outputs) reports no finding for A10-CTX; its findings belong to other work packages
  whose outputs are not written yet.
- JSON validity of `context-manifest.json` re-read with Python after the edit: 8 file entries.
- Both jsonl files re-read: 22 and 24 rows, ids in sequence, every gap row carries
  id/title/description/type/severity, every assumption row carries id/text/why.
- Every `CG-A10-CTX-*` and `ASM-A10-CTX-*` cited in the context file exists in a jsonl row.
- No person names, no email addresses, no issue-tracker references, no external calls.
- No file outside the WP `Write only` list was written, except the manifest index entry authorised by
  the WP body and recorded as `ASM-0034`.

## Not done, on purpose

- No gap or assumption was numbered; step D1 numbers them `GAP-nnnn` and `ASM-nnnn` and rewrites the
  citations.
- The five v2 context files, the standards files and the README were not edited (root rule 1). Their
  re-basing is `GAP-0019`; the v5 deltas they need are in the new file.
- No `.docx`, `.xlsx` or `.pptx` output was produced: this WP writes one Markdown context file, the
  registers and the edit log.
- No approval was sought; the context stands as Draft and the open decisions are assumptions.
