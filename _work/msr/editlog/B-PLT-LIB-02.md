# Edit log B-PLT-LIB-02

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Run date: 22 November 2026.

Fanout: 5. Four legacy keys, one worker each: RWB-E1-047, RWB-E1-072, RWB-TE-006 and NF-02. The parent merged the per-key registers, normalized the fragment acceptance-criterion first lines, applied consistency edits and ran the checks.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1047 APP Feature flags for module release with a removal date v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1047 CON Feature flags for module release with a removal date - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1072 APP Drools runtime and rule package store v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1072 CON Drools runtime and rule package store - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT TE006 APP Outbox and retry for outbound work v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT TE006 CON Outbox and retry for outbound work - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT NF02 APP Shared library baseline v1.md`
- `_work/msr/fragments/RWB-PLT-E1047-APP.json`
- `_work/msr/fragments/RWB-PLT-E1047-CON.json`
- `_work/msr/fragments/RWB-PLT-E1072-APP.json`
- `_work/msr/fragments/RWB-PLT-E1072-CON.json`
- `_work/msr/fragments/RWB-PLT-TE006-APP.json`
- `_work/msr/fragments/RWB-PLT-TE006-CON.json`
- `_work/msr/fragments/RWB-PLT-NF02-APP.json`
- `_work/msr/gaps/B-PLT-LIB-02.jsonl`
- `_work/msr/assumptions/B-PLT-LIB-02.jsonl`
- `_work/msr/editlog/B-PLT-LIB-02.md`

## Registers

- Gaps: 7 rows, one combined row per story. `GAP-1411`, `GAP-1412`, `GAP-1413`, `GAP-1414`, `GAP-1415`, `GAP-1416`, `GAP-1417`.
- Assumptions: 19 rows. E1047 has 5, E1072 has 5, TE006 has 6 and NF02 has 3. Every row is cited by its own story and every citation resolves.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-LIB-02 --quick` -> C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS.
- Targeted extra checks: C06, C07, C09, C15, C16, C17 and C20 PASS. C10 and C11 report only legacy keys owned by other, not yet executed WPs; the four keys of this WP have no missing AC and no missing TC.

## Notes

- The four stories are Split (rework) or Moved (no impact); no preserved legacy section was needed and no delta copy was made.
- The APP acceptance criteria of RWB-E1-047, RWB-E1-072 and RWB-TE-006 keep the legacy text and every legacy value; the only additions are the origin tags and the `Given the ... contract mock returns ...` line per criterion. The legacy wording of RWB-E1-047 AC4 is kept.
- The TE006 retry conflict is recorded: the Kafka retry ladder of Architecture v5 slide 22 wins over the legacy 1/5/15 minute schedule, and the legacy values remain only in the copied criteria text and in configuration.
- The platform library has no service short, so no `rwb.platform.events.v1`, `/api/recovery/platform/v1` or `queue rwb-platform` name is invented; the feature-flag paths stay exactly as the Ownership Map names them and the outbox and rules kits declare `None` for their own REST, topic and queue.
- Consistency edits after the fanout: the CON story relation tables no longer label platform contracts as build dependencies; the outbox column sets that no source defines now carry the placeholder and the gap; the E1072 mock Given sits in each acceptance criterion rather than only in the Background; the NF02 cross-references use the full story ids.
- No legacy file was edited, no issue-tracker or external call was made, and the scratch helper scripts live only under `_work/msr/smoke/`.
