# Edit log B-ITG-W2-03

WP B-ITG-W2-03 (RWB-ITG-W2: legacy RWB-E2-012, RWB-E2-013, RWB-E2-014, RWB-E2-015, RWB-E2-016). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2012 ITG Manual transfer and reassignment screen with reason - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2013 ITG Approval routing with the delegation of authority table - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2014 ITG Approval screen for D7.1 demand and recall notices - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2015 ITG Timers, escalation and the deviation flag on the case record view - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2016 ITG Full case record view with the history timeline - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2012-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2013-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2014-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2015-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2016-ITG.json`
- `_work/msr/gaps/B-ITG-W2-03.jsonl`
- `_work/msr/assumptions/B-ITG-W2-03.jsonl`
- `_work/msr/editlog/B-ITG-W2-03.md`

## Method

- Read the Template and Rules v1 fully, the WP, the Ownership Map, the Architecture v5 and Temporal and Drools text extracts, the five legacy Epic 2 stories and the thin-story extracts (Program, Epic 1 and Epic 2 BRDs, Epics 3 to 8 Specification, Business Rules and Routing Logic).
- Fanout 5: one task subagent per legacy key (RWB-E2-012, RWB-E2-013, RWB-E2-014, RWB-E2-015, RWB-E2-016), each writing only its own story file and fragment. The parent assembled the two candidate registers and this edit log, so no parallel append could lose a row.
- AC policy: none of the five stories owns legacy ACs in the plan (`acs` is empty for every line), so each writes four new criteria tagged (new, D-RCV-60) that test only the wave 2 integration harness for its journey: the composite route through gateway-bff, the decision-record-before-state-change order, the event and outbox evidence, and failure isolation with the refusals of the legacy story. The app ACs stay with the APP stories.
- TCs: every legacy test case is carried as an ITG copy with the -ITG suffix and a Level column (System to Integration, Access to Component, Resilience to NFR). The Covers column keeps the legacy AC of the copy; the note in section 16 says so.
- Sections 12.1-12.9 are present in every story; 12.1, 12.3, 12.5, 12.6 and 12.7 are "None" because an ITG story serves no operation, publishes no event, starts no workflow, adds no schedule and owns no table. Every owner and every path in section 12 comes from the Ownership Map.
- Section 13 carries one DP row per pattern in the WP line (12, 11, 10, 9 and 8 rows) with the R5.5 text and dependency, and the paragraph that the platform H dependencies are not repeated in the metadata H list.
- Every missing value cites one placeholder pair per story. No other CG or ASM id is cited in the five story files or the five fragments.
- No issue-tracker reference, no person name, no e-mail address, no monolith API base outside an as-built section, and no service short outside the 19.

## Registers

- Candidate gap rows: 5 (GAP-0396, GAP-0397, GAP-0398, GAP-0399, GAP-0400).
- Candidate assumption rows: 5 (ASM-0571, ASM-0572, ASM-0573, ASM-0574, ASM-0575).
- One combined gap row per story and one default assumption row per story, in the Template and Rules R9 key formats. Step D1 numbers them.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-03 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Additional local validation: metadata rows and values against the WP lines; 19 section headings in order; 12.1-12.9 present with 12.1 and 12.7 "None"; four AC lines per story with the origin tag; -ITG test case count equal to the legacy TC list (15, 16, 12, 11, 12) and matching each fragment; DP row count equal to the pattern list; fragment keys complete and ops lists identical to section 12.2; no tracker word, no e-mail address and no person name.
