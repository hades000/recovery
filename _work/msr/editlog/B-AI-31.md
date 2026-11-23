# Edit log — WP B-AI-31 (Agent Catalog and Specifications v-next)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- 08 AI and agents/Recovery Workbench Agent Catalog and Specifications v3.xlsx
- _work/msr/gaps/B-AI-31.jsonl
- _work/msr/assumptions/B-AI-31.jsonl
- _work/msr/editlog/B-AI-31.md

Scratch under `_work/msr/docs/B-AI-31/` (build and verification only, not an output of the run):
`build.py` (writes the workbook) and `verify.py` (source-diff, counts, citation check).

## What was done

The source `08 AI and agents/Recovery Workbench Agent Catalog and Specifications v2.xlsx` was never
opened for writing. It was copied to v3 with `compat/office_write.py copy`, and only the copy was changed.
The change the realignment needs is one owning service per agent; nothing else of the source was touched.

1. **Read me added first.** Row 1 and row 2 are the header of Template and Rules §R8.1. Row 7 is
   `Status: Draft` (no approval is recorded in the source). Row 10 is the change-log row
   `v3, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`;
   row 11 records the source version. Rows 14 to 18 list what the version holds, then counts, then sources.
2. **The two source sheets are untouched.** `Agents` (16 rows, 10 columns) and `Decision steps` (29 rows,
   8 columns) are identical cell for cell to v2 — `verify.py` reports 0 differences in each. Every agent name,
   behaviour word, mode, run-by, model, autonomy level at go-live and target, shadow-from and live-from epic,
   step ID and first-epic value is therefore kept exactly as issued.
3. **Agents v3 (new sheet, 12 rows).** One row per agent in the order of the source sheet. The behaviour
   columns are the v2 words; the new columns are the owning service code, the service, the service name, the
   service epic `RWB-SVC-<code>`, the wave, the runtime host, the decision steps the agent serves and the basis
   of the owner.
4. **Service summary (new sheet, 12 service rows and a total).** Which service owns which agent, the count and
   the decision steps. P10 rwb-agent is listed as the runtime host of all 12 runs with no business agent; the
   total row reads 12 agents owned by 11 services.
5. **Realignment changes (new sheet, 12 rows).** One row per change with the v2 value, the v3 value, the basis
   in source precedence (R-PREC) and the gap or assumption that carries it.

## Owners

Every owner is taken from the Microservice Ownership Map v1 (`_work/msr/plan/ownership.json` and the map
workbook): services, waves, `agent_*` tables, `/admin/agent-*` endpoints and `AgentRunWorkflow`. The owning
service per agent is:

| Agent | Owning service | Basis |
|---|---|---|
| Intake agent | P5 rwb-document | Arch v5 slide 16, agent child `classify / extract run` |
| Screening agent | S8 rwb-deviation | Arch v5 slide 15, agent child `screening agent run` |
| Settlement and restructure agent | S2 rwb-treatment | Decision steps D5.2, D5.3, D6.4; FSD S2 |
| Valuation agent | S1 rwb-valuation | Decision step D6.1; S1 owns valuations (assumption ASM-0150) |
| Pricing agent | S5 rwb-asset | Decision steps D8.2, D8.3; FSD S5 R-DIS-19, R-DIS-28 |
| Route agent | S1 rwb-valuation | Arch v5 slide 18, agent child `route agent`; FSD S1 FEAT-VAL-07 |
| Guarantee claim agent | S3 rwb-guarantee | Decision step D6.5; FSD S3 R-GUA-04 |
| Reconciliation agent | P8 rwb-payment | Decision step P8; FSD P8 FEAT-PAY-02 |
| Legal document agent | S4 rwb-litigation | Decision steps D7.2, D7.4; FSD S4 R-LIT-21 |
| Debt sale agent | S6 rwb-debtsale | Decision step D8.4; FSD S6 R-DS-04 |
| Write-off agent | S7 rwb-writeoff | Decision steps D9.2, D9.3; FSD S7 R-WO-05 |
| Tracing agent | S9 rwb-partner | Decision steps X6, D7.5; FSD S9 FEAT-PRM-05 (assumption ASM-0151) |

P10 rwb-agent hosts `AgentRunWorkflow` on task queue rwb-agent (60 s, then the rule result) for all 12 agents,
per Architecture v5 slide 16 and the map's Workflows sheet. No agent is assigned to P1, P2, P3, P4, P6, P7, P9
or the platform library.

## Never edited, never invented

No source file was changed. No autonomy level, mode, model, target or epic was altered: D-RCV-60 changes the
owning service only. Two agents have no owning service named in any source (Valuation, Tracing); each is written
with the reading and the citation in the same cell, and one gap row and one assumption row carry it. The
Settlement and restructure agent is also read from its decision steps rather than a named child, and its basis
cell cites GAP-0086 and ASM-0148. Names, IDs, numbers and dates are copied character for character.
This document carries no release date, so nothing is marked `(tentative)`; the `Shadow from` and `Live from`
columns are epic numbers, not dates.

## Registers

- Gap rows written: 4 candidate rows (`GAP-0086` to `GAP-0089`) in `_work/msr/gaps/B-AI-31.jsonl`.
- Assumption rows written: 4 candidate rows (`ASM-0148` to `ASM-0151`) in
  `_work/msr/assumptions/B-AI-31.jsonl`.
- Every row is cited in the workbook and every citation resolves to a row (`verify.py` checks both directions).
- Numbering to GAP-nnnn and ASM-nnnn is left to step D1, as rule 7 and Template and Rules §R9 require.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-AI-31 --quick` — C02, C03, C05, C12, C13 and
C18 all PASS, 0 findings; rerun identical.

## Not done, by design

- No story, requirement, architecture or register master file was touched; this work package writes the agent
  catalog next version only.
- No issue tracker, wiki, repository, design tool or web call was made; no commit was created.
- No agent is added, removed or given a new autonomy level; the decision steps sheet is not renumbered.
