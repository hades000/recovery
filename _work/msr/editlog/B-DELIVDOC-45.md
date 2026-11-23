# B-DELIVDOC-45 edit log — Recovery Workbench Release Plan v5

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash. Decision D-RCV-60. Run date 22 November 2026.

## Files written

- `11 Delivery and operations/Recovery Workbench Release Plan v5.xlsx`
- `_work/msr/gaps/B-DELIVDOC-45.jsonl`
- `_work/msr/assumptions/B-DELIVDOC-45.jsonl`
- `_work/msr/docs/B-DELIVDOC-45/Release Plan v5 content.md`
- `_work/msr/docs/B-DELIVDOC-45/build_v5.py`
- `_work/msr/editlog/B-DELIVDOC-45.md`

## What was done

The source `Recovery Workbench Release Plan v4.xlsx` was copied to v5 with
`compat/office_write.py copy` and the copy was then extended by
`_work/msr/docs/B-DELIVDOC-45/build_v5.py`. The source file was not edited.

- Source sheets kept with every section, ID, number and date: Releases, Modules by release,
  Gates, Calendar, Release rules. All 1,112 source cells compare equal between v4 and v5.
- New sheet `Read me` at position 1: the two §R8.1 header lines, document title, version, tool
  line, Status Draft, the change log (v4 as the source row; v5 row "22 November 2026, D-RCV-60
  microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash"), what changed and a sheet index.
- New sheet `Waves`: waves 0 to 4 with business epics, releases, tentative release dates, the
  services created in each wave, the service counts, what the wave delivers and its entry and exit.
  Wave 0 completes by the E1 go decision, 27 November 2026 (tentative); Wave 1 = E1; Wave 2 = E2 and
  E3; Wave 3 = E4 and E5; Wave 4 = E6, E7 and E8.
- New sheet `Services by release`: the 19 services from the Ownership Map v1 with their wave,
  the version 4 release text unchanged, the first release date (tentative), schema, REST base,
  Kafka topic, task queue and the suggested owners of the story types of §R5.3.
- `Gates`: gate G7 Contract published added after G1 to G6.
- `Release rules`: rules 8 to 11 added (tentative dates; the wave of each release; one creation
  per service; contract first).
- `Releases`, `Modules by release` and `Calendar`: one to four note rows appended, covering the
  tentative date, the wave of each release, the owner position and the kept monolith-era counts.
- Every release date is the v4 date, unchanged and marked tentative (DL48). No date was raised
  as a gap (Template and Rules U7). No person is named anywhere; owners are service codes and
  team types only.

## Counts

- Gap rows: 8 (`GAP-0292` to `GAP-0298`), no P1 row: four P2 and four P3.
- Assumption rows: 8 (`ASM-0382` to `ASM-0389`).
- New decisions: none beyond D-RCV-60 and DL48, which the plan uses.
- Rows numbered GAP-nnnn and ASM-nnnn: not in this work package (step D1 numbers them).

## Check run

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-DELIVDOC-45 --quick` — all six
checks pass; the report is under `22 Microservice Realignment/checks/reports/`.

## Notes

- No FAILED step. Nothing was retried three times.
- The xlsx file is not covered by checks C12 and C13 (they read .md, .json, .yaml and .sql only),
  so the workbook text was reviewed by hand for person names, e-mail addresses and issue-tracker
  references: none present.
