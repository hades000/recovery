# Edit log B-ITG-W4-06

WP: `_work/msr/wp/B-ITG-W4-06.md`
Decision: D-RCV-60
Date: 22 November 2026
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash

## Execution

- Fanout 5: one task subagent per legacy key, RWB-E6-033, RWB-E7-001, RWB-E7-002, RWB-E7-003 and RWB-E7-004, in one message.
- Each subagent wrote only its own story file and fragment. The parent merged the candidate gap and assumption rows into the WP registers and wrote this log, so no two workers appended to one file.
- RWB-E7-002 hit a transient rate limit on the first attempt; it was relaunched and completed. No work was lost or duplicated.
- One correctness fix after review: the refused caller in RWB-ITG-E7004-ITG was changed from an unsourced role code to the published `RW-OFF` role, in the flow, the AC, the authority table, the fake and the test data.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E6033 ITG Receive a partner result into the case - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7001 ITG Run X1 dispute and complaint end to end - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7002 ITG Run X2 vulnerability and hardship end to end - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7003 ITG Run X3 deceased customer end to end - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W4 Wave 4 integration/RWB ITG E7004 ITG Run X4 fraud end to end - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E6033-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7001-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7002-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7003-ITG.json`
- `_work/msr/fragments/RWB-ITG-E7004-ITG.json`
- `_work/msr/gaps/B-ITG-W4-06.jsonl`
- `_work/msr/assumptions/B-ITG-W4-06.jsonl`

## Registers

- Gap rows: 7. `GAP-0463`, `GAP-0464`, `GAP-0465`, `GAP-0466`, `GAP-0467`, `GAP-0468`, `GAP-0469`.
- Assumption rows: 7. `ASM-0655`, `ASM-0656`, `ASM-0657`, `ASM-0658`, `ASM-0659`, `ASM-0660`, `ASM-0661`.
- Two conflict rows are raised against the legacy story masters: RWB-E7-002 AC2 cites R-DEV-17 (the X6 lost-contact rule) on an X2 case, and RWB-E7-003 AC3 cites R-DEV-06 (the X6 and X7 insurance-approval rule) on an X3 case. The harness stories assert the published X2 and X3 rules instead and do not invent an approval step.
- Every other row is a Missing row for harness configuration, or the assumption that records the default taken for it. No business value is invented: the contact-limit values, the same-day cut-off, the Aric referral shape and the insurer and estate answers stay fixture or parameter data.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W4-06 --quick`: C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS, 0 findings each. Reports under `22 Microservice Realignment/checks/reports/wp-B-ITG-W4-06-*.md`.
- Additional checks run against the same file set: C06 PASS, C07 PASS, C08 PASS, C15 PASS, C16 PASS, C17 PASS, C20 PASS, 0 findings each.
- C19 was also run: it reports missing planned outputs for other, unstarted WPs (for example B-ITG-W2-06) and no finding for B-ITG-W4-06; all 11 outputs this WP plans exist and each `.md` carries the D-RCV-60 change-log row.
- No FAILED item. The legacy masters are unchanged (C18 hashes pass).
