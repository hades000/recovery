# Edit log B-TESTDOC-43

Tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash
Decision: D-RCV-60. Run date: 22 November 2026.
WP: `_work/msr/wp/B-TESTDOC-43.md` (new Integration Test Plan, first version). Fanout: 0.

## Files written

- `09 Testing and quality/Recovery Workbench Integration Test Plan v1.docx`
- `_work/msr/docs/B-TESTDOC-43/Recovery Workbench Integration Test Plan v1.md`
- `_work/msr/docs/B-TESTDOC-43/build-tpl.docx`
- `_work/msr/gaps/B-TESTDOC-43.jsonl`
- `_work/msr/assumptions/B-TESTDOC-43.jsonl`
- `_work/msr/editlog/B-TESTDOC-43.md`

Every path above is inside the WP's "Write only" block and nothing outside it was touched. The output document is new: the folder `09 Testing and quality` held no Integration Test Plan in any version and a recursive search for the family name returned nothing, so no source file was edited and no next version displaced anything. `build-tpl.docx` is the first, template-checked build of the same text and sits in the scratch folder only.

## What the document is

A new integration test plan for the 19-service target, version 1, Draft, with the two Template and Rules section R8.1 header lines first and a change-log row `1, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`. Eighteen sections: purpose and scope, test basis and precedence, services and waves, the four levels inside the plan, the harness, component tests against fakes, contract tests by call type, the four wave journeys, non-functional integration, environments and test data, entry and exit per gate, sequence and Day 1, test case inventory, defects and evidence, roles and ownership, traceability, risks, change log.

- **Waves.** Nine services in wave 1 (P1, P2, P3, P4, P5, P6, P7, P9, P10), thirteen in wave 2 (plus P8, S2, S5, S8), seventeen in wave 3 (plus S1, S3, S4, S6) and nineteen in wave 4 (plus S7, S9), with the integration epic, the business epics and the journey story of each wave. Every release date is copied unchanged and marked (tentative): 30 November 2026; 31 December 2026 and 31 January 2027; 28 February 2027 and 31 March 2027; 30 April 2027, 31 May 2027 and 30 June 2027.
- **Elements.** The harness RWB-ITG-W1J01-ITG is described by the seven criteria and the ten test cases it already holds; the four journeys RWB-ITG-W1J02-ITG, RWB-ITG-W2J01-ITG, RWB-ITG-W3J01-ITG and RWB-ITG-W4J01-ITG are described hop by hop with their own test case families; the non-functional epic RWB-ITG-NFR is described through RWB-ITG-TE009-ITG, RWB-ITG-TE010-ITG and the NFT rows of the non-functional test plan version 3. No story criterion, contract, identifier or release date was changed.
- **Owners.** Every owner is a service code of the Microservice Ownership Map v1 (P1 to P10, S1 to S9), a platform epic of Template and Rules section R5.1, or a role label. The map assigns 93 tables, 156 REST operations, 30 events, 15 workflows and 22 jobs across its 20 owner rows; the plan cites that scope and names no person.
- **Test case inventory.** 147 integration stories holding 1,416 test case identifiers, counted from section 16 of the story files: 34 contract, 144 component, 1,085 integration, 78 end to end and 75 NFR, per epic 687, 478, 46, 191 and 14.

## Document format

- **.md** written directly in the scratch folder as the full text of the document (378 lines).
- **.docx** produced from that text with `office_write.py md-docx`. The WP names a source `.docx` as the style template and no source document exists, so the sibling `09 Testing and quality/Recovery Workbench Test Strategy v3.docx` of the same family and folder was used as the formatting template; it supplies the A4 page setup, the heading and table styles and the copyright footer of the family, and its body was cleared before the new text was laid in. The result has 87 paragraphs, 21 tables and the two header lines first in the body. The template choice is recorded as a reading of this run and changes no content.
- The build was first made into the scratch folder to inspect the styles, then written directly to the output path, because `office_write.py` refuses to overwrite and the final path had to be written once.
- The template carries its own document properties, so the `.docx` was opened once, its title, subject, version and comments set to this document and this run, and saved back. The body was not touched by that pass: 87 paragraphs and 21 tables before and after.

## Register counts

- Candidate gaps: **10 rows** in `_work/msr/gaps/B-TESTDOC-43.jsonl` (GAP-2151 to -10). By type: Missing 5, Ambiguous 2, Conflict 2, and one Missing for the absent source family. By severity: P2 9, P3 1. Every row carries the 15 keys of Template and Rules section R9.
- Candidate assumptions: **13 rows** in `_work/msr/assumptions/B-TESTDOC-43.jsonl` (ASM-3450 to -13). By confidence: High 5, Medium 8. Every row carries the ten keys of section R9. Ten rows answer a gap row one to one (ASM-1 to ASM-10 against CG-1 to CG-10); three are document-level readings with no gap (Draft status, dates unchanged and tentative, owners read from the Ownership Map).
- **Count of CG rows: 10. Count of ASM rows: 13.**
- Every `CG-` and `ASM-` identifier cited in the document exists in a register row, and every register row is cited at least once in the document (checked both ways with a script). Only step D1 numbers them as GAP-nnnn and ASM-nnnn. No identifier was used outside `_work/msr/plan/ids.json`: the text uses D-RCV-60, ADR-013 to ADR-023 and DL48, which the ids file allocates.

## Two conflicts raised, not settled silently

- **GAP-2159.** The test strategy version 3 says the harness RWB-ITG-W1J01-ITG serves all four waves, while the story checks the wave 1 contracts, publishes one stub per wave 1 service and scopes its criteria to wave 1. The plan reads the story as the wave 1 increment of one harness that each later wave extends (ASM-9).
- **GAP-2160.** The wave 3 journey names rwb-partner (S9) at its instruction hop, while the Ownership Map and Template and Rules place S9 in wave 4. The plan proves that hop against the published contract served by its fake in wave 3 and proves the real-owner hop in the wave 4 journey (ASM-10).

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TESTDOC-43 --quick` — all six quick checks PASS with zero findings:

| Check | Result | Findings |
|---|---|---|
| C02 | PASS | 0 |
| C03 | PASS | 0 |
| C05 | PASS | 0 |
| C12 | PASS | 0 |
| C13 | PASS | 0 |
| C18 | PASS | 0 |

C02, C03 and C05 filter to story files and find none in this work package's file set, as expected. C12 (person names and e-mail), C13 (issue-tracker references) and C18 (write-only compliance and legacy master hashes) read the six files written here and all pass.

A wider manual pass on the same file set also ran C14, C17 and C20: all PASS. C19 reports 200 findings, every one of them a planned output of another, not yet written work package; no finding names this WP, and both of its planned outputs exist with the D-RCV-60 change-log row present. No step failed three times.

## Assumptions carried

- ASM-3460: Draft status, because no approval of this version is recorded in this run; the plan is usable for test design and gate definition and no gate is treated as signed.
- ASM-3461: every date is unchanged and tentative, and the four journey business dates (2026-11-25, 2026-12-15, 2026-12-14, 2027-04-30) are test data of their stories and not a programme calendar.
- ASM-3462: every owner is a service code or a role label, taken from the Ownership Map v1, with team types written as suggestions only.
