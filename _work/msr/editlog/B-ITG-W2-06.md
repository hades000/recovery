# Edit log B-ITG-W2-06

WP B-ITG-W2-06 (RWB-ITG-W2: legacy RWB-E2-029, RWB-E2-030, RWB-E2-031, RWB-E2-032, RWB-E2-033). Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2029 ITG Deviation screening agent evaluation and L1 on one segment [E3b] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2030 ITG Legal document agent in shadow on Epic 1 data [E3c] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2031 ITG Agent monitoring dashboard v2 [E3d] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2032 ITG TDR offer-suggestion model through the model gateway [E3e] - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2033 ITG Case and queue list with status, owner and ageing - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2029-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2030-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2031-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2032-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2033-ITG.json`
- `_work/msr/gaps/B-ITG-W2-06.jsonl`
- `_work/msr/assumptions/B-ITG-W2-06.jsonl`
- `_work/msr/editlog/B-ITG-W2-06.md`

## Method

- Read the Template and Rules v1 in full, the WP, the Ownership Map, the Architecture v5 text extract (slides 13-20 and 41-44 in particular), the Temporal and Drools text extract (slides 11-16), the five legacy Epic 2 stories and the thin-story extracts used for fill order (Program BRD v4, Epic 1 v4, Epic 2 v2, Epics 3 to 8 Specification v3, Business Rules and Routing Logic v4).
- Fanout 5: one task subagent per legacy key (RWB-E2-029, RWB-E2-030, RWB-E2-031, RWB-E2-032, RWB-E2-033) in one message, each writing only its own story file and fragment. The parent merged the two candidate registers and wrote this edit log, then ran the check.
- Story shape: each of the five is the wave 2 integration harness for its legacy key. It builds no production endpoint, screen, table or migration. Sections 1 and 13 say so plainly; the harness seeds the legacy values, drives the journey through the owning services' published contracts, replaces each contract fake as its I story lands, keeps an evidence pack and applies a pass or fail gate.
- AC policy: none of the five owns a legacy acceptance criterion (the `acs` list is empty in the plan), so each writes new criteria tagged `(new, D-RCV-60)` that test only the integration deliverable, using values that already exist in the legacy story (case IDs, policy versions, sample codes, counts, amounts, thresholds, dates and message ids) and inventing none.
- TCs: every id of `tcs_legacy` is carried as an ITG copy with the `-ITG` suffix, in the WP order, with the Level column of §R7.2 s16. Journey cases are Integration; access cases are Component; the Principle 5 and resilience cases are NFR.
- Sections 12.1-12.9 are present in every story. 12.1, 12.3 and 12.7 are "None" because an ITG story provides no production operation, publishes no event and owns no table; 12.6 is "None" except E2031, where the observed drift Schedule is recorded. 12.2 names owners from the Ownership Map only, on each owner's `/api/recovery/<short>/v1` base with one hop and the 2 s timeout of DP-11.
- Patterns: every DP in the story line gets exactly one row in the section 13 table, with the "Legacy marker", "Microservice pattern" and "Dependency added" cells copied character for character from §R5.5. The platform H dependencies in that table are delivered by the platform waves and are not repeated in the metadata, which carries no build dependency for any of the five stories.
- Naming: topics `rwb.<short>.events.v1` and the shared `rwb.decision-record.v1`, events `rwb.<short>.<Event>.v1`, queues `rwb-<short>`, bases `/api/recovery/<short>/v1`. The monolith base `/api/recovery/v1` appears only in the DP-13 Legacy marker cell.
- The E2032 story records a real conflict rather than a missing value: the legacy story calls `ModelSuggestionClient` in process on rwb-agent, while Architecture v5 slide 13 gives the S2 Treatment row no call to P10, slide 16 starts agent runs only from `CaseCreated` and `DocumentStored`, and the Ownership Map has no rwb-agent operation that starts a suggestion run. The story states the resolution it assumes and reports the journey blocked, never passed, until the start operation is published.

## Registers

- Candidate gap rows: 5 (GAP-0411, GAP-0412, GAP-0413, GAP-0414, GAP-0415). One combined row per story. Four are type Missing, severity P2, each carrying the harness environment, the fixtures and model stubs, the evidence format and the gate, plus its story-specific open point (the drift Schedule landing for E2031, the OpenXML comparison and access-log assertion for E2033). One is type Conflict (E2032), carrying the treatment-to-agent start operation disagreement alongside the same missing values.
- Candidate assumption rows: 5 (ASM-0586, ASM-0587, ASM-0588, ASM-0589, ASM-0590), one default per story: SIT harness against the published contracts, each fake replaced as its I story lands, evidence a per-run report keyed by story and business date, plus the story-specific default (the drift Schedule in rwb-agent for E2031 and the one-hop start operation with the stored-output read-back for E2032).
- Every missing value in the five stories and five fragments cites only its own pair. No other CG or ASM id is cited.

## Fixes during the check

- RWB-ITG-E2029-ITG section 15 gained the placeholder pair with the screen-fixture sentence, so all five stories cite their pair in sections 3, 12.8, 13 and 15.
- RWB-ITG-E2030-ITG section 18 corrected the requirement citation to Business Requirements Epic 1 v4 section 4 and Program v4 section 5.5, where REQ-DCM-011 is actually listed.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-06 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, 0 findings each.
- Additional local validation, all clean: the 20 metadata rows in order with the values of the story line; the 19 section headings in order; 12.1-12.9 present once each; every Scenario line tagged `(new, D-RCV-60)` (9, 9, 9, 9 and 11 scenarios); every `tcs_legacy` id present with `-ITG` and equal to the fragment `tcs` in the same order; every DP row equal to §R5.5; the five fragment JSON files carry exactly the 28 required keys in order and their I, reqs, ops, events, ids and file paths match the stories; every cited CG and ASM id resolves to a row in the two registers; no tracker reference, no e-mail address, no person name, no monolith API base outside the DP-13 cell; every API base, topic and queue uses one of the 19 service shorts; each story carries the two header lines, the D-RCV-60 change-log row and the tool line.
