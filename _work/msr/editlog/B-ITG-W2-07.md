# Edit log B-ITG-W2-07

WP B-ITG-W2-07 (RWB-ITG-W2: legacy RWB-E2-034, RWB-E2-035, RWB-E2-036, RWB-E2-038, RWB-E2-041). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2034 ITG Interaction ledger on the case and from every channel - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2035 ITG Next action on the case - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2036 ITG Queue write interface for models and agents - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2038 ITG Temporal security, codec server and admin audit - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2041 ITG Rule change governance and audit report - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2034-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2035-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2036-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2038-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2041-ITG.json`
- `_work/msr/gaps/B-ITG-W2-07.jsonl`
- `_work/msr/assumptions/B-ITG-W2-07.jsonl`
- `_work/msr/editlog/B-ITG-W2-07.md`

## Method

- Read the Template and Rules v1 fully, the WP, the Ownership Map, the Architecture v5 and Temporal and Drools text extracts, the five legacy Epic 2 stories and the thin-story extracts (Program and Epic 1/Epic 2 BRDs, Epics 3 to 8 Specification, Business Rules and Routing Logic).
- Fanout 5: one task subagent per legacy key (RWB-E2-034, RWB-E2-035, RWB-E2-036, RWB-E2-038, RWB-E2-041), each writing only its own story file, fragment and the two register rows under its own CG/ASM id. The parent reviewed every file, corrected the E2036 approved-caller key and overflow fixture, the E2034 service count and the E2041 call-type row, and wrote this edit log. No parallel append lost a row.
- AC policy: E2034 owns the legacy ACs AC1-AC7 and AC9-AC11, so its story copies those ten scenarios word for word with the origin tag on the scenario line and leaves AC8 with RWB-P2-E2034-APP. E2035, E2036, E2038 and E2041 own no legacy AC in the plan, so each writes four new criteria tagged (new, D-RCV-60) that test only the wave 2 integration harness for its journey. No legacy AC is restated by a story that does not own it.
- TCs: every legacy test case in the WP line is carried as an ITG copy with the -ITG suffix and a Level column. The E2034 copies match the legacy scenario bodies after the origin tag is removed. The Covers column names the legacy AC of the copy and the ITG criterion of section 7.
- Sections 12.1-12.9 are present in every story; 12.1, 12.3, 12.5, 12.6 and 12.7 are "None" where the harness serves no operation, publishes no event, starts no workflow, adds no schedule or owns no table. Every owner, operation, topic and schema in section 12 comes from the WP naming rule or the Ownership Map.
- Section 13 carries one DP row per pattern in the WP line (13, 12, 10, 10 and 12 rows) with the R5.5 text and dependency, and states that the platform H dependencies are not repeated in the metadata H list.
- Every missing value cites one placeholder pair per story (the harness environment, seeding, evidence format and retention, and the composite route detail). No other CG or ASM id is cited in the five story files or the five fragments.
- No issue-tracker reference, no person name, no e-mail address, no monolith API base outside an as-built section, and no service short outside the 19.

## Registers

- Candidate gap rows: 5 (GAP-0416, GAP-0418, GAP-0419, GAP-0417, GAP-0420).
- Candidate assumption rows: 5 (ASM-0591, ASM-0593, ASM-0594, ASM-0592, ASM-0595).
- One combined gap row per story and one default assumption row per story, in the Template and Rules R9 key formats. Step D1 numbers them.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-07 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Additional local validation: metadata rows and values, 19 section headings in order, 12.1-12.9 present, AC origin tags, the ten E2034 scenario bodies byte-equal to the legacy after the origin tag, fragment JSON keys and lists, ownership operations and topic names, no tracker reference, no e-mail address.
