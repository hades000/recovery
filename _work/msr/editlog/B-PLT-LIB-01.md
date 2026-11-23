# Edit log B-PLT-LIB-01

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Run date: 22 November 2026.

Fanout: 5. Five legacy keys, one worker each: N009, RWB-E1-027, RWB-E1-037, RWB-E1-042 and RWB-E1-043. Each worker wrote only its own key's stories and fragments and its own register shard; the parent merged the shards into the two WP registers, ran a cross-file verifier, wrote this log and ran the checks.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT N009 APP RFC 9457 problem and Idempotency-Key helpers v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT N009 CON RFC 9457 problem and Idempotency-Key helpers - interface and fake - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1027 APP Decision log writer v1 v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1027 CON Decision log writer v1 - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1037 APP Role to permission matrix as data and PDPA field masking by role v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1037 CON Role to permission matrix as data and PDPA field masking by role - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1042 APP Central configuration service and parameter catalog v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1042 CON Central configuration service and parameter catalog - contract v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1042 OPS Central configuration service and parameter catalog - deployment v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1043 APP Reference data service with versioned tables v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-LIB Shared libraries/RWB PLT E1043 CON Reference data service with versioned tables - contract v1.md`
- `_work/msr/fragments/RWB-PLT-N009-APP.json`
- `_work/msr/fragments/RWB-PLT-N009-CON.json`
- `_work/msr/fragments/RWB-PLT-E1027-APP.json`
- `_work/msr/fragments/RWB-PLT-E1027-CON.json`
- `_work/msr/fragments/RWB-PLT-E1037-APP.json`
- `_work/msr/fragments/RWB-PLT-E1037-CON.json`
- `_work/msr/fragments/RWB-PLT-E1042-APP.json`
- `_work/msr/fragments/RWB-PLT-E1042-CON.json`
- `_work/msr/fragments/RWB-PLT-E1042-OPS.json`
- `_work/msr/fragments/RWB-PLT-E1043-APP.json`
- `_work/msr/fragments/RWB-PLT-E1043-CON.json`
- `_work/msr/gaps/B-PLT-LIB-01.jsonl`
- `_work/msr/assumptions/B-PLT-LIB-01.jsonl`
- `_work/msr/editlog/B-PLT-LIB-01.md`

## Registers

- Gaps: **11 rows**, one combined row per story. `GAP-1400` and `-2`; `GAP-1402` and `-2`; `GAP-1404` and `-2`; `GAP-1406`, `-2` and `-3`; `GAP-1409` and `-2`. Every row is P2, `needed_by_wave` 0, `wp` B-PLT-LIB-01.
- Assumptions: **26 rows**. N009 has 4, E1027 has 5, E1037 has 5, E1042 has 7 and E1043 has 5. Every row is cited by the story it belongs to and every citation in the eleven story files resolves to a merged row.

## Checks

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-LIB-01 --quick` — result in the run report of `22 Microservice Realignment/checks/reports/`.
- Cross-file verifier (scratch, `_work/msr/smoke/`): the 20 metadata rows in order, the 19 section headings in order, every `Scenario: ACn` line carrying `(new, D-RCV-60)`, every fragment acceptance-criterion first line present character for character, every fragment TC id present, every `CG-`/`ASM-` citation resolving, no forbidden string, every service short known, and all nine sub-tables of section 12 present — 11 files, 0 findings.

## Notes

- The four legacy keys of this WP are the **platform-library slice** of Epic 1. The legacy acceptance criteria stay with the owning-service story — RWB-P7-E1027-APP, RWB-P4-E1037-APP, RWB-P3-E1042-APP and RWB-P3-E1043-APP — and with the integration stories RWB-ITG-E1027-ITG and RWB-ITG-E1037-ITG, exactly as those stories record. No legacy AC is copied here, so every criterion in these eleven files is tagged `(new, D-RCV-60)` and tests only the library or deployment deliverable in the title. Each story's section 2 and section 18 name the owner of the legacy ACs and cite the whole legacy test-case set.
- `preserved=false` and `delta=true` were applied as the WP records them: the E1-042 and E1-043 stories describe the microservice change only and copy no legacy section; the as-built story of those two keys is the preserved base story of the owning service epic.
- The platform library has no service short, so no `rwb.platform.events.v1`, `/api/recovery/platform/v1`, `queue rwb-platform` or platform schema is invented. Every REST path in these files belongs to an owner named in the Ownership Map: the access operations at `/api/recovery/access/v1/...` (Architecture v5 slide 14 names the operations, the Ownership Map has no path row for them, recorded in `GAP-1405`), the parameters and reference operations at `/api/recovery/case/v1/...` (P3 under the R-PREC default ruling).
- The decision record travels as `rwb.decision.DecisionRecorded.v1` by the §R4 event-name rule, on the shared topic `rwb.decision-record.v1` whose name §R4 keeps; the divergence from the ITG story's event-name spelling is recorded in `ASM-2444` and `GAP-1403` for the assembler to normalise.
- Two DP-table dependencies that the patterns add but that a library cannot build against (the Drools kit on the reference-data client, the gateway route contract on the decision-record library) are recorded as build dependencies on the CON contract only, with the reason written in the pattern row of section 13.
- No legacy file was edited, no issue-tracker or external call was made, and the scratch helper and the per-key register shards live only under `_work/msr/smoke/`.
