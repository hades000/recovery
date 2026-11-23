# Edit log B-ITG-W2-02

WP B-ITG-W2-02 (RWB-ITG-W2: legacy RWB-E2-006, RWB-E2-007, RWB-E2-008, RWB-E2-009, RWB-E2-010). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2006 ITG Credit approval pack for NLEADS - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2007 ITG Booking confirmation from the ALS load - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2008 ITG Payment matching with the missed payment event - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2009 ITG Steering dashboard v1 data set - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2010 ITG Stage 2 data products  contracts, plans and treatments - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2006-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2007-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2008-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2009-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2010-ITG.json`
- `_work/msr/gaps/B-ITG-W2-02.jsonl`
- `_work/msr/assumptions/B-ITG-W2-02.jsonl`
- `_work/msr/editlog/B-ITG-W2-02.md`

## Method

- Read the Template and Rules v1 fully, the WP, the Ownership Map, the Architecture v5 and Temporal and Drools text extracts, the five legacy Epic 2 stories and the thin-story extracts (Program, Epic 1 and Epic 2 BRDs, Epics 3 to 8 Specification, Business Rules and Routing Logic).
- Fanout 5: one task subagent per legacy key (RWB-E2-006, RWB-E2-007, RWB-E2-008, RWB-E2-009, RWB-E2-010). Each subagent wrote only its own story file, its own fragment and its own one gap and one assumption row. The E2006 and E2007 subagents were retried once after transient rate-limit and socket errors and then completed; E2008, E2009 and E2010 completed on the first pass. The parent merged nothing, verified the five outputs and wrote this edit log and no other file.
- AC policy: E2006, E2009 and E2010 own no legacy AC in the plan (`acs` is empty), so each writes four new criteria tagged `(new, D-RCV-60)` for its wave 2 integration harness. E2007 owns AC1, AC5 and AC7, and E2008 owns AC1, AC3, AC4 and AC5, so each copies exactly those legacy scenarios and tags them `(legacy <legacy> <AC>)`; a programmatic diff confirms the Given/When/Then bodies are identical to the legacy section 7, and the unowned ACs are cited only through their `-ITG` test cases.
- TCs: every legacy TC of each line is carried as an ITG copy with the `-ITG` suffix and a Level column. System maps to Integration, Access to Component, Resilience to NFR. Counts: 13, 11, 10, 10 and 9.
- Sections 12.1-12.9 are present in every story; 12.1, 12.3, 12.5, 12.6 and 12.7 are `None` because an ITG story serves no operation, publishes no event, starts no workflow, adds no schedule and owns no table. Every owner and every path in section 12 comes from the Ownership Map, with the gateway-bff composite route left to the platform edge story.
- Section 13 carries one DP row per pattern in the WP line (7, 11, 12, 9 and 8 rows) with the R5.5 text and dependency, and the paragraph that the platform H dependencies are not repeated in the metadata H list.
- Every missing value cites one placeholder pair per story. No other CG or ASM id is cited in the five story files or the five fragments.
- No issue-tracker reference, no person name, no e-mail address, no monolith API base outside an as-built section, and no service short outside the 19.

## Registers

- Candidate gap rows: 5 (GAP-0394, GAP-0395, GAP-0393, GAP-0391, GAP-0392).
- Candidate assumption rows: 5 (ASM-0569, ASM-0570, ASM-0568, ASM-0566, ASM-0567).
- One combined gap row per story and one default assumption row per story, in the Template and Rules R9 key formats. Step D1 numbers them.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-02 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Additional local validation: metadata rows and values against the WP lines; 19 section headings in order; 12.1-12.9 present with 12.1, 12.3, 12.5, 12.6 and 12.7 `None`; AC counts 4, 3, 4, 4 and 4 with the correct origin tags; legacy AC bodies identical to the legacy text for E2007 and E2008; `-ITG` test case counts equal to the legacy TC lists and matching each fragment; DP row count equal to the pattern list; fragment keys complete and ops lists identical to section 12.2 and events lists identical to section 12.4; five gap and five assumption rows with the R9 keys; no tracker word, no e-mail address and no person name.
