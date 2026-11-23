# B-REQ-BRD-E2 edit log

Work package: B-REQ-BRD-E2 — Recovery Workbench Business Requirements Epic 2, next version (BRD Builder).
Decision: D-RCV-60 microservice realignment. Date: 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Agent: aisdlc-brd-builder. Fanout: 0 (no subagent used).

## Files written

- `03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.md`
- `03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v3.docx`
- `_work/msr/gaps/B-REQ-BRD-E2.jsonl`
- `_work/msr/assumptions/B-REQ-BRD-E2.jsonl`
- `_work/msr/editlog/B-REQ-BRD-E2.md`
- `_work/msr/docs/B-REQ-BRD-E2/Recovery Workbench Business Requirements Epic 2 v3.md`
- `_work/msr/docs/B-REQ-BRD-E2/template-base.docx`

Scratch builders in the same folder (not deliverables): `gen.py`, `patch_template.py`, `postprocess.py`, `probe.py`, `probe2.py`, `selfcheck.py`.

No source file was edited. `03 Requirements and specifications/Recovery Workbench Business Requirements Epic 2 v2.docx` and its converted extract are unchanged; the v3 pair sits beside them.

## Register rows

| Register | Rows | IDs |
|---|---|---|
| Gaps (`_work/msr/gaps/B-REQ-BRD-E2.jsonl`) | 5 | GAP-1459 to GAP-1463 |
| Assumptions (`_work/msr/assumptions/B-REQ-BRD-E2.jsonl`) | 9 | ASM-2560 to ASM-2568 |

Counts: **5 CG rows, 9 ASM rows**. Five gaps are cited in the document (5 of 5) and nine assumptions (9 of 9); no citation in the document lacks a row, and no row is uncited.

## What changed against v2

The document was generated from the converted source text, so sections 1 to 7 are the source text itself. A line-by-line diff of the source text from `# 1.` to the end against the v3 body returns exactly three differences:

1. `Epic 2, Foundation 2, releases on 31 December 2026.` becomes `... 31 December 2026 (tentative).` (rule 10, WP instruction).
2. DL03 owner cell: the individual's name becomes `Architecture lead with the architecture team` (rule 4).
3. DL09 owner cell: two individuals' names become `Business lead with the test lead` (rule 4).

Everything else is additive: the two header lines, eleven metadata rows, section 7.1, section 8 (Delivery model: 8.1 the 19 service epics, 8.2 platform and integration epics, 8.3 waves, 8.4 contract-first delivery), section 9 (requirement to service epic traceability), and section 10 (decisions adopted, approval table, change log, sources, gaps and assumptions, personal data).

Verified unchanged: 32 requirement rows, 26 Must, 5 Should, 1 Could, 71 program requirement rows, 15 beneficiary rows summing to 32, all RWB-E2, REQ-*, DL* identifiers and all dates except the tentative marking. The counts of section 1 were re-counted from section 3 and section 4 and hold.

## Values and their sources

- Service epics, service names and waves: `Recovery Workbench Microservice Ownership Map v1.xlsx`, sheet `Services` (19 rows).
- Platform epics (7), integration epics (5), wave map, work types, Day-1 and contract-first rules, story ID pattern: `Recovery Workbench Microservice Story Template and Rules v1.md` §R4, §R5.1 to §R5.3, §R5.6, §R5.7, §R8.4.
- Primary service epic, other service epics, story counts, dispositions and business epic per requirement: `_work/msr/plan/split_plan.json`, blocks `legacy` and `slices`, joined on the legacy key.
- Delegation of authority ownership (section 7.1, DL18): Ownership Map rulings, item `delegation_limit`.
- Decision, ADR and DL identifiers (section 10.1): `_work/msr/plan/ids.json` plus §R8.4.

## Method note on the .docx

`office_write.py md-docx` failed once with `KeyError: no style with name 'Heading 1'` against the source template: the template stores builtin heading styles under their display names (`Heading 1`) while the writer looks them up under the internal names (`heading 1`). Fix: a copy of the template in the scratch folder (`template-base.docx`) with only those six `w:name` values lowercased; fonts, margins and numbering are untouched. The writer then succeeded with that copy as `--template`. A second pass (`postprocess.py`) added the source document's single-line table borders, repeated header rows and bold header text to the 28 generated tables. Both passes run on the new output only.

The scratch `.md` and the delivered `.md` are identical: the scratch copy is the writer's input, and the delivered copy was copied from it before conversion.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-BRD-E2 --quick` — C02, C03, C05, C12, C13, C18 all PASS, 0 findings.

Additional self-checks: no person name, no email address, no issue-tracker reference, no backticked code in the Word output, all 14 register rows complete on the required keys, all citations resolved.

## Not done

No PRD, no story file, no register numbering (step D1), no issue-tracker, Confluence, GitLab or web access. Section 10.2 is left empty for the approvers and the document stays Draft, per run rule 9.
