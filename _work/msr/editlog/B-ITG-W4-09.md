# Edit log B-ITG-W4-09 — RWB-ITG-W4: legacy W4J01

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Date 22 November 2026.
Agent: aisdlc-msr-worker. fanout: 0, so no task subagent was used.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG W4J01 ITG Wave 4 journey end to end - integration v1.md`
- `_work/msr/fragments/RWB-ITG-W4J01-ITG.json`
- `_work/msr/gaps/B-ITG-W4-09.jsonl`
- `_work/msr/assumptions/B-ITG-W4-09.jsonl`
- `_work/msr/editlog/B-ITG-W4-09.md`

No existing file was edited; the story file and the four `_work` files did not exist before this run.

## What was produced

- One story file for `RWB-ITG-W4J01-ITG` (W4J01, disposition New, business epic NEW, wave 4, lane L-ITG-W4, owner QA, Day 1): the wave 4 journey end-to-end harness and release gate. The 19 sections of Template and Rules §R7.2 are in order and the 20 metadata rows of §R7.1 are in order.
- Seven acceptance criteria, all `(new, D-RCV-60)`: AC1 the journey green on one business date, AC2 one owner and one hop with the 2 s budget, AC3 a forced failure names the hop, AC4 a repeated run reproduces the evidence with no duplicate effect, AC5 the point of no return waits for the ledger, AC6 the EP08 hardening controls (rule version stamping and hash chain), AC7 the wave gate.
- Fourteen test cases `TC-W4J01-01-ITG` to `TC-W4J01-14-ITG` with the Level column, six exception paths X1 to X6, fifteen business rules BR1 to BR15, ten traceability rows and one combined out-of-scope row per excluded item.
- Contract tables 12.1 to 12.9: 0 operations provided, 24 consumed, 0 events published, 11 consumed, no workflow, activity or Schedule owned, no table owned, ten contract fakes, and the file row read as outbound items of rwb-integration.
- Patterns applied: None. The story applies no decoupling pattern of §R5.5; it reads each owner through that owner's published contract and asserts DP-01, DP-05, DP-11, DP-13, DP-18 and DP-19 as run failures instead.
- No legacy AC and no legacy TC is owned: the legacy key W4J01 is a new integration journey key with no legacy story behind it, so §R7.3 source precedence was used only to fill values from the Arch v5 extract, the Temporal and Drools design extract, the Program BRD, the Epics 3 to 8 specification and the Business Rules and Routing Logic.

## Gaps and assumptions

- Gap rows: 1 (`GAP-0480`), one combined row for the missing harness environment, seed, fixed business date, composite route paths, evidence format and gate thresholds. Type Missing, severity P2, needed by wave 4.
- Assumption rows: 1 (`ASM-0672`), the default that the harness runs in the test environment against the stub set from Day 1, fixes the business date at 2027-04-30 with cut-off month 2027-04, seeds one synthetic portfolio through the published operations only, and writes one evidence report per run with an all-green wave gate. Confidence Medium.
- Every placeholder in the story cites both ids, and both ids exist as rows; no other placeholder id is used.
- No release date was raised as a gap and no date was changed; the story's Release row is "None (new story)" because the story JSON carries no release value, while the business dates the harness fixes are the Program release date 2027-04-30 (§8) and cut-off month 2027-04.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-09 --quick` — C02, C03, C05, C12, C13 and C18 all PASS, 0 findings.

## Notes and open points

- The wave map (§R5.6) puts EP06, EP07 and EP08 in wave 4, while Arch v5 slide 38 names epics 6 and 7 and adds S7 and S9 in the same wave. Both readings are used and neither contradicts the other, so no conflict gap was raised.
- The journey runs on two cases of one synthetic portfolio because a sold account (R-UNI-47, CASE_CLOSED_SOLD) and a written-off account (R-WO-21, POSTED, then retained) are mutually exclusive outcomes of one case; this is stated in §1 and §3 and is a harness design choice, not a business value.
- The events `AccountsTransferred` and `FileDelivered` carry no EV number in the Arch v5 event catalogue; they are cited as event catalogue A3 rows "+" and no number was invented.
- The write-off record and the deviation record have no published GET operation in the Ownership Map; the story asserts them through the case, DP13, the instruction read and the decision log and names the owning app story's own read instead of inventing a path.
