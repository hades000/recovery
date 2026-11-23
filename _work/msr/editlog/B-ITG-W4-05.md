# Edit log B-ITG-W4-05

WP: `_work/msr/wp/B-ITG-W4-05.md`, epic RWB-ITG-W4, wave 4 integration, legacy keys RWB-E6-028 to RWB-E6-032.
Decision: D-RCV-60. Run date: 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What was done

Five wave 4 integration stories were written, one per legacy key, each in the 19-section template of Template and Rules v1 §R7 with the 20 metadata rows of §R7.1. Each fanout slice ran as its own subagent with one legacy key; nothing was merged across slices, and each slice wrote only its own story, its own fragment and its own two candidate rows.

The five candidate row files were then merged, one row per story, into the two WP registers. No master file, no catalogue and no numbering was touched (numbering stays a step D1 task).

- RWB-E6-028 → RWB-ITG-E6028-ITG: six ACs, all new under D-RCV-60 (the WP assigns no legacy AC to this slice), six `-ITG` test cases from TC-E6-028-01 to TC-E6-028-06, ten consumed operations across S7, P7, P3, S6, P1 and P4, the approval → escalation → sale → lot journey. The S6 hop is the debt sale route's own published lot operation.
- RWB-E6-029 → RWB-ITG-E6029-ITG: legacy AC1 verbatim plus five new ACs, four `-ITG` test cases, seven consumed operations, the panel and terms read back as data, DP08 beside the owner.
- RWB-E6-030 → RWB-ITG-E6030-ITG: legacy AC1 verbatim plus five new ACs, four `-ITG` test cases, six consumed operations, the version in force, DP-07 list values through the rwb-case reference-data contract, and the version boundary at an issued instruction.
- RWB-E6-031 → RWB-ITG-E6031-ITG: legacy AC1 verbatim plus six new ACs, four `-ITG` test cases, eight consumed operations, the scorecard pick proved against DP08 and DP11 with the freshness gate of VR-S9-003-1.
- RWB-E6-032 → RWB-ITG-E6032-ITG: legacy AC1 verbatim plus five new ACs, four `-ITG` test cases, five consumed operations, the override standing beside the scorecard pick with the reason recorded.

## Files written

- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6028 ITG Sell a post charge-off population - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6029 ITG Onboard a partner and set terms - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6030 ITG Hold the partner panel and fee schedule as data - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6031 ITG Allocate work by measured return - integration v1.md
- 04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6032 ITG Override an allocation with a reason - integration v1.md
- _work/msr/fragments/RWB-ITG-E6028-ITG.json
- _work/msr/fragments/RWB-ITG-E6029-ITG.json
- _work/msr/fragments/RWB-ITG-E6030-ITG.json
- _work/msr/fragments/RWB-ITG-E6031-ITG.json
- _work/msr/fragments/RWB-ITG-E6032-ITG.json
- _work/msr/gaps/B-ITG-W4-05.jsonl
- _work/msr/assumptions/B-ITG-W4-05.jsonl
- _work/msr/editlog/B-ITG-W4-05.md

## Register rows

- Candidate gap rows written: 5 (one per story). Gap ids: GAP-0458, GAP-0459, GAP-0460, GAP-0461, GAP-0462. All are type Missing, severity P2, needed_by_wave 4, owner role Integration lead.
- Candidate assumption rows written: 5 (one per story, one default each). Assumption ids: ASM-0650, ASM-0651, ASM-0652, ASM-0653, ASM-0654. All confidence Medium.
- Everything else is copied from a source and is not a gap: the release date stays 30 April 2027 and is marked (tentative); no date was raised as a gap.

## Corrections made during the check pass

- RWB-ITG-E6028-ITG: the two approval operations were rewritten onto rwb-decision's own base, `/api/recovery/decision/v1/approvals` and `/api/recovery/decision/v1/approvals/{approvalId}/approve`, in §4, §7, §12.2, §12.8 and §15 and in the fragment, because the Ownership Map places approvals under P7 rwb-decision and not on a base of their own.
- RWB-ITG-E6032-ITG: AC5 now overrides the placement from the override partner back to the scorecard pick, so the refusal reads coherently as "nothing changed" against the instruction that answered the override partner.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-05 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, no findings.
- Extra, against the same file set: C01, C06, C07, C08, C09, C14, C15, C16, C17, C20 PASS. C04, C10, C11 and C19 report run-wide findings only (story files other WPs have not written yet, and their edit logs), none of them in this WP's outputs.
- Local cross-checks: every path in §12.2 resolves to an Ownership Map operation with that owner; every MSG, R-, REQ-, FEAT-, DF- and LOV id cited exists in the extracts; the AC ids in each file match its fragment; every fragment test case and consumed operation appears in its story; the five slice files are inside the WP "Write only" list.
