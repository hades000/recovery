# Edit log B-ITG-W2-04

WP B-ITG-W2-04 (RWB-ITG-W2: legacy RWB-E2-017, RWB-E2-018, RWB-E2-019, RWB-E2-021, RWB-E2-022). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2017 ITG Contract, CA and mortgage document generation screens - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2018 ITG E-signature flow for customers and the bank - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2019 ITG Partner identities through the external gateway - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2021 ITG Letter dispatch loop with proof of delivery from WIN - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2022 ITG SMS and LINE dispatch through NSS and LINE OA - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2017-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2018-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2019-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2021-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2022-ITG.json`
- `_work/msr/gaps/B-ITG-W2-04.jsonl`
- `_work/msr/assumptions/B-ITG-W2-04.jsonl`
- `_work/msr/editlog/B-ITG-W2-04.md`

## Method

- Read the Template and Rules v1 fully, the WP, the Ownership Map, the Architecture v5 and Temporal and Drools text extracts, the five legacy Epic 2 stories and the thin-story extracts (Program and Epic 1/Epic 2 BRDs, Epics 3 to 8 Specification, Business Rules and Routing Logic).
- Fanout 5: one task subagent per legacy key (RWB-E2-017, RWB-E2-018, RWB-E2-019, RWB-E2-021, RWB-E2-022), each writing only its own story file and fragment. The parent assembled the two candidate registers and this edit log.
- AC policy: E2017 and E2018 own no legacy AC in the plan, so each writes new criteria tagged (new, D-RCV-60) that test only the integration journey. E2019, E2021 and E2022 copy their owned legacy ACs verbatim with the origin tag; the remaining criteria stay with the app stories.
- TCs: every legacy test case is carried as an ITG copy with the -ITG suffix and a Level column. Corruption-free copies were diff-checked against legacy §7; the E2019/E2021/E2022 scenario bodies are byte-equal to the legacy after removing the origin tag.
- Sections 12.1-12.9 are present in every story; 12.1 and 12.7 are "None" because an ITG story builds no production API and owns no table.
- Every missing value cites one placeholder pair per story. No other CG or ASM id is cited in the five story files or the five fragments.

## Registers

- Candidate gap rows: 5 (GAP-0401, GAP-0402, GAP-0403, GAP-0404, GAP-0405).
- Candidate assumption rows: 5 (ASM-0576, ASM-0577, ASM-0578, ASM-0579, ASM-0580).
- One combined gap row per story and one default assumption row per story, in the Template and Rules §R9 key formats. Step D1 numbers them.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-04 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Re-run after the content review fixes (the E2018 read path and the E2021 state wording): same six PASS.
- Additional local validation: metadata rows and values, 19 section headings in order, 12.1-12.9 present, AC origin tags, fragment JSON keys and lists, ownership bases and topics, no tracker reference, no e-mail address.
