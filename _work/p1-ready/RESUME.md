# Resume tracker (Codex usage limit hit at about 04:05 Bangkok; Codex resets 07:46; second Claude account resets 06:00)

Status per agent (update as notifications arrive). Replacements run on Claude Max Sonnet, continuing from staged files and the agent's own edit log.

| Agent | Status | Replacement |
|---|---|---|
| W1-contracts (API spec, contract catalog) | FAILED (limit) | W1 resume on Max Sonnet – started |
| W2-tests (Test Cases, RTM) | FAILED (limit) | W2 resume on Max Sonnet – started (plus tc-backfill.csv sync) |
| W3-messages | FAILED (limit) | 06:00 on second Claude account |
| W4-data | FAILED (limit) | W4 resume on Max Sonnet – started 04:08 |
| W5-runtime | FAILED (limit) | 06:00 on second Claude account |
| W6-registers pass 1 | DONE | pass 2 later |
| W7-platform | FAILED (limit) | 06:00 on second Claude account |
| W8-reqs-security | FAILED (limit) | 06:00 on second Claude account |
| W9-governance | FAILED (limit) | W9 resume on Max Sonnet – started 04:08 |
| S1 E1001/E1002/E1018 | FAILED (limit) | S1 resume on Max Sonnet – started |
| S2 / S2b E1011/E1013 | DONE (S2b Sol) | |
| S3 E1015 | FAILED (limit) | S3 resume on Max Sonnet – started |
| S4 E1016 | shallow; S4b Sol FAILED (limit) | 06:00 on second Claude account |
| S5 E1017/E1055 | FAILED (limit) | 06:00 on second Claude account |
| S6 E1064/E1068 | FAILED (limit) | 06:00 on second Claude account |
| S7 E1065/E1069 | FAILED (limit) | 06:00 on second Claude account |
| S8 E1066/E1067 | FAILED (limit) | 06:00 on second Claude account |
| S9 AD018/AD019 | FAILED (limit) | 06:00 on second Claude account |
| S10, S12, S13 | DONE (Sonnet) | |
| S11 E2010/ACE001 | FAILED (limit) | 06:00 on second Claude account |
| L01–L08 | DONE | |
| F01–F06 | DONE | |
| F07–F12 | running (Max Sonnet) | |
| F13–F19 | queued – paused until P1 core resumes | |

## 07:36 restart round (both Claude accounts reset; all 04:30 agents had died at the Max limit)
- Claude Max Sonnet: W2 (resume 2), W5 (resume 2), S6, S7, S8, S9 (resume 2), F19 (resume).
- Second Claude account Sonnet: W3, W7, W8 (resume 2), S4b, S5 (resume 2), S11 (resume 2), F17, F18 (resume).
- Done before the limit: W1, W4, W6 pass 1, W9, S1, S2b, S3, S10, S12, S13, L01–L08, F01–F16.
- Note: decision batch C was re-run automatically at 06:02 (batch-C.csv rewritten); the merged Decision Register v1 (02:45) remains authoritative.
- Codex back about 07:46: overflow and retries only.

## 08:20 – Codex limit again (resets 13:05); second Claude account out until 11:00
Finishing pass status:
- Done: FD4 (Sol), G8 (Sol).
- Running on Claude Max: FD1, FD2, G1, G2, G3, Decision Register v2 (Opus), G5 (retry 2).
- To restart on Claude Max as slots free, else on the second Claude account at 11:00: FD3 (log has rows), G4 (DM), G6, G7 (log has rows), G9 (dry run found 73 ITG stories, 11 need v3 copy).

## 09:00 – re-review phase
- Done: all finishing writers (FD1–FD4), all story groups (G1–G9), Decision Register v2, test reconciliation (TR), graph re-run (applied).
- Running (Max Sonnet): W6b register pass 2; re-review R1 (E1001/E1002/E1018), R2 (E1011/E1013), R3 (E1015), R4 (E1016), R5 (E1017/E1055), R6 (E1064/E1068), R7 (E1065/E1069).
- Queued re-review: R8 (E1066/E1067), R9 (AD018/AD019), R10 (E2001/E2007/E2008/E2021/E2022/E2034), R11 (E2010/ACE001), R12 (DM001–DM007), R13 (DM008–DM014).
- After W6b: python -I replace_ids.py "..\..\24 P1 Developer Readiness v1\Temp ID to register ID v2.csv" (dry, then --write).
