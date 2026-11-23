# Edit log — WP B-ITG-W1-10 (RWB-ITG-W1, legacy RWB-E1-073, RWB-TE-004, RWB-TE-006, RWB-TE-008, RWB-TE-013)

Decision D-RCV-60. Date 22 November 2026.
Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG E1073 ITG Rule authoring, validation, test scenarios, approval and rollback in Drools - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG TE004 ITG Masked data in SIT and UAT - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG TE006 ITG Outbox and retry for outbound work - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG TE008 ITG Decision log hash chain check - integration v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-ITG-W1 Wave 1 integration/RWB ITG TE013 ITG Agent runtime client with fallback - integration v1.md`
- `_work/msr/fragments/RWB-ITG-E1073-ITG.json`
- `_work/msr/fragments/RWB-ITG-TE004-ITG.json`
- `_work/msr/fragments/RWB-ITG-TE006-ITG.json`
- `_work/msr/fragments/RWB-ITG-TE008-ITG.json`
- `_work/msr/fragments/RWB-ITG-TE013-ITG.json`
- `_work/msr/gaps/B-ITG-W1-10.jsonl`
- `_work/msr/assumptions/B-ITG-W1-10.jsonl`
- `_work/msr/editlog/B-ITG-W1-10.md`

## Counts

| Register | Rows | Ids |
|---|---|---|
| Gaps (CG) | 5 | GAP-0383, GAP-0379, GAP-0382, GAP-0380, GAP-0381 |
| Assumptions (ASM) | 10 | ASM-0555, -2; ASM-0547, -2; ASM-0553, -2; ASM-0549, -2; ASM-0551, -2 |

One combined gap row per story and one or two assumption rows per story, as the WP asks; every CG and ASM id cited in a story or a fragment has a row, and every row is cited.

## Work done

1. Five workers ran in parallel, one per legacy key (fanout 5). Each wrote only its own story file and fragment and appended its own rows to the two shared registers in one atomic append; both registers re-read and every line parsed.
2. Every story has the two §R8.1 header lines, a change-log paragraph naming D-RCV-60 and the tool line, the 20 metadata rows of §R7.1 in order, the 19 section headings of §R7.2 in order, `#### 12.1` to `#### 12.9`, the `patterns` list of the WP in "Patterns applied", a §13 Pattern application table with one row per DP, an I list that matches the WP and no H, C or X dependency (`acs` is empty for all five, so each story writes 5-6 new criteria tagged `(new, D-RCV-60)` and no legacy AC).
3. Section 16 keeps every legacy TC id of the WP with the `-ITG` suffix (20 + 8 + 13 + 9 + 10) and adds the new `TC-ITG-<compact>-nn` rows for the new criteria; each table carries the Level column and a note naming the APP story that owns the legacy AC numbers (checked against `_work/msr/plan/split_plan.json`).
4. Fragment `acs` normalised to the new criteria with `origin` "new, D-RCV-60" and `text_first_line` copied from the story, so all five fragments carry their own criteria (the run's fragments use both shapes; the origin tag keeps new and legacy entries apart).
5. Three section 16 notes corrected after the merge so the named owner matches `split_plan.json`: RWB-E1-073 legacy AC1-AC15 belong to RWB-P3-E1073-APP (not to the four APP stories); RWB-TE-008 to RWB-PLT-TE008-APP (not RWB-P7-E1008-APP); RWB-TE-013 to RWB-P10-TE013-APP (RWB-P7-TE013-APP owns none).
6. The four story narratives describe only the integration deliverable of the microservice change for each legacy key: central rule governance in rwb-decision with local evaluation (E1-073), the masked copy across the 19 schemas (TE-004), the outbox and inbox library with Kafka retry topics and DLT across services (TE-006), the 02:00 chain check over the ledger and the local chains after JOB-13 became continuous ingest (TE-008), and the agent client against rwb-agent with the 60 s fallback and the decision record (TE-013).
7. No file outside the WP "Write only" list was written; no legacy file was touched.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-ITG-W1-10 --quick` — C02 PASS, C03 PASS, C05 PASS, C12 PASS, C13 PASS, C18 PASS (0 findings, exit 0).

Also run on the same file set: C06 PASS, C07 PASS, C11 WARN (no finding for these five keys), C15 PASS, C16 PASS, C17 PASS, C20 PASS. C19 names only `_work/msr/editlog/B-ITG-W1-10.md` as missing before this file was written, and no other B-ITG-W1-10 finding.

## Failures

None.
