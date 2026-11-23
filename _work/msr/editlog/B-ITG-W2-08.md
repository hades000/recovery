# B-ITG-W2-08 edit log

WP B-ITG-W2-08, RWB-ITG-W2 wave 2 integration. Decision D-RCV-60. Date 22 November 2026. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

Fanout: 5 legacy keys, one task subagent each (RWB-E2-042, RWB-E2-043, RWB-E3-006, RWB-E3-010, RWB-E3-013), each writing its own story and fragment. The parent merged the staged register rows and wrote this log.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2042 ITG Epic 2 rule packages in Drools - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E2043 ITG Temporal and Drools integration pattern and reference case workflow - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3006 ITG Calculate the plan installment - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3010 ITG Book the plan and set the schedule - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W2 Wave 2 integration/RWB ITG E3013 ITG Check encumbrance and eligibility before negotiation - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E2042-ITG.json`
- `_work/msr/fragments/RWB-ITG-E2043-ITG.json`
- `_work/msr/fragments/RWB-ITG-E3006-ITG.json`
- `_work/msr/fragments/RWB-ITG-E3010-ITG.json`
- `_work/msr/fragments/RWB-ITG-E3013-ITG.json`

## Registers

- `_work/msr/gaps/B-ITG-W2-08.jsonl`: 5 candidate gap rows, one combined row per story, ids GAP-0421, GAP-0422, GAP-0423, GAP-0424, GAP-0425. Every row is type Missing, severity P2, needed by wave 2.
- `_work/msr/assumptions/B-ITG-W2-08.jsonl`: 6 candidate assumption rows, ids ASM-0596, ASM-0597, ASM-0598, ASM-0599, ASM-0600, ASM-0601 (E3010 carries two: the harness default and the NLEADS/ALS interface detail). Confidence Medium on every row.
- Rows were staged per legacy key and merged in key order; only step D1 numbers them as GAP-nnnn and ASM-nnnn.

## What each story delivers

| Story | Legacy key | Owned legacy AC | Integration dependencies | Test cases |
|---|---|---|---|---|
| RWB-ITG-E2042-ITG | RWB-E2-042 | none, four new criteria | RWB-P3-E2042-APP, RWB-P6-E2042-APP, RWB-P4-E2042-APP, RWB-P7-E2042-APP | TC-E2-042-01-ITG to TC-E2-042-06-ITG |
| RWB-ITG-E2043-ITG | RWB-E2-043 | none, four new criteria | RWB-P3-E2043-APP, RWB-P7-E2043-APP | TC-E2-043-01-ITG to TC-E2-043-07-ITG |
| RWB-ITG-E3006-ITG | RWB-E3-006 | AC2, copied word for word | RWB-S2-E3006-APP | TC-E3-006-01-ITG to TC-E3-006-05-ITG |
| RWB-ITG-E3010-ITG | RWB-E3-010 | AC1, copied word for word | RWB-S2-E3010-APP | TC-E3-010-01-ITG to TC-E3-010-06-ITG |
| RWB-ITG-E3013-ITG | RWB-E3-013 | none, three new criteria | RWB-S2-E3013-APP, RWB-P3-E3013-APP | TC-E3-013-01-ITG to TC-E3-013-06-ITG |

Every story carries the 20 metadata rows of Template and Rules §R7.1 in order, the 19 sections of §R7.2 in order, the DP table of §R5.5 for exactly the patterns named in its metadata, and the 12.1 to 12.9 contract tables. Release dates are copied unchanged and marked tentative. No person's name, no external tool call, no master file and no legacy file was touched.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W2-08 --quick`: C02, C03, C05, C12, C13, C18 all pass, 0 findings.
- Structural review of the five stories and five fragments against the WP story lines: metadata values, heading order, AC origin tags, TC -ITG coverage, fragment key order and values, and citation resolution all match.
- Verbatim review of the two owned legacy criteria, RWB-E3-006 AC2 and RWB-E3-010 AC1: identical to the legacy text apart from the added origin tag on the Scenario line.
- No failure was left open and nothing was escalated.
