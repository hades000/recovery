# Edit log — WP B-ITG-W1-11 (RWB-ITG-W1, legacy W1J01, W1J02)

Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J01 ITG Contract-test harness and synthetic test data - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG W1J02 ITG Wave 1 v5 journey end to end - integration v1.md`
- `_work/msr/fragments/RWB-ITG-W1J01-ITG.json`
- `_work/msr/fragments/RWB-ITG-W1J02-ITG.json`
- `_work/msr/gaps/B-ITG-W1-11.jsonl`
- `_work/msr/assumptions/B-ITG-W1-11.jsonl`
- `_work/msr/editlog/B-ITG-W1-11.md`

## Counts

| Register | Rows | Ids |
|---|---|---|
| Gaps (CG) | 2 | GAP-0384, GAP-0385 |
| Assumptions (ASM) | 4 | ASM-0557, ASM-0558, ASM-0559, ASM-0560 |

One combined gap row per story and two assumption rows per story, as the WP asks; every CG and ASM id cited in a story or a fragment has a row, and every row is cited.

## Work done

1. Two workers ran in parallel, one per legacy key (W1J01 and W1J02; fanout 5 allowed up to five). Each worker wrote only its own story file and fragment and appended its own rows to the two shared registers with a Python append (UTF-8, no BOM); both registers were re-read and every line parsed.
2. Both stories are new integration stories: the two R§8.1 header lines, a change-log paragraph naming D-RCV-60 and the tool line, the 20 metadata rows of §R7.1 in order, the 19 section headings of §R7.2 in order, `#### 12.1` to `#### 12.9`, and "Patterns applied" None because the WP `patterns` list is empty; §13 states that no DP is applied by the harness itself.
3. W1J01 builds the wave 1 contract-test harness and the synthetic test data set: OpenAPI 3.1, AsyncAPI 3.0 and contract-jar checks in every build, five Temporal replay histories, Testcontainers Kafka/PostgreSQL, the per-schema boundary test, a deterministic synthetic set loaded and reset through owner operations only in the DEV sandbox, and the WireMock stub set for the wave 1 app and ITG stories. It has 7 new ACs and 10 new TCs with the Level column.
4. W1J02 builds the wave 1 end-to-end journey for business date 2026-11-25 across P1, P3, P4, P5, P6, P7, P9, P10 and P2: the seeded case RW-2026-000123, allocation, document intake and attach, document-received transfer, decision records, the shadow INTAKE agent run, the demand notice, the 16:00 WIN file, the 01:30 measures, the ledger, authorisation, the one-hop trace, the repeat run and the all-green wave gate. It has 5 new ACs and 11 new TCs with the Level column.
5. Both stories carry H, C, I and X as None and are Day 1 by §R5.7; both fragments carry the exact WP step-8 keys, the AC and TC lists, the consumed operations, the consumed events, the workflows exercised, `prd_ref` "Pending (C1)" and the gap and assumption ids.
6. Section 12 names only the 19 service shorts, the owner bases `/api/recovery/<short>/v1`, the topics `rwb.<short>.events.v1` and the queues `rwb-<short>`; every owner is the one the Ownership Map gives, and no operation is invented. The two open points (the P10 agent-run start path and the gateway-bff composite route path and merge order) are carried by the W1J02 gap and assumptions, not decided in the story.
7. Seven quality corrections were applied after the first review, without changing any heading, metadata row, count, fragment or register row: the W1J01 suite count (sixteen, not fifteen), the 12.2 method cells for P5, P6 and P7 so the write and read directions are both named, the P2 stub path `GET /admin/outbound-items`, the preflight wording, the W1J02 probe count (seven), the JOB-15 type (measures run) and the X6 test-case wording.
8. No file outside the WP "Write only" list was written; no legacy file was touched; the edit log itself is this file.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-11 --quick` — C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS (0 findings, exit 0).

Also run on the same file set: C06 PASS, C07 PASS, C15 PASS, C16 PASS, C17 PASS. C19 is satisfied by the two story files, the two fragments and this edit log; C20 is satisfied by the tool line above.

## Failures

None.
