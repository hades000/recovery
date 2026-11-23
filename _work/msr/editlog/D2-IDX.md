# Edit log - WP D2-IDX (Recovery Workbench Document Index next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work package: D2-IDX. Fanout: 0.

## Files written

- `12 Project communication/Recovery Workbench Document Index v14.md`
- `_work/msr/docs/D2-IDX/build_index.py`
- `_work/msr/docs/D2-IDX/scan_editlog.py`
- `_work/msr/docs/D2-IDX/summarize.py`
- `_work/msr/docs/D2-IDX/exists.py`
- `_work/msr/docs/D2-IDX/zero.py`
- `_work/msr/docs/D2-IDX/resolve_versions.py`
- `_work/msr/docs/D2-IDX/count_stories.py`
- `_work/msr/docs/D2-IDX/editlog_files.json`
- `_work/msr/docs/D2-IDX/verify_rows.py`
- `_work/msr/docs/D2-IDX/verify_files.py`
- `_work/msr/docs/D2-IDX/verify_table.py`
- `_work/msr/docs/D2-IDX/write_registers.py`
- `_work/msr/gaps/D2-IDX.jsonl`
- `_work/msr/assumptions/D2-IDX.jsonl`
- `_work/msr/editlog/D2-IDX.md`

Scratch only (not deliverables) is the folder `_work/msr/docs/D2-IDX/`: the readers of the 541 edit
logs, the file-existence and version readers, the story-count reader, the three verifiers and the
register writer. The source index was never opened for writing; the v14 file is new.

## What was done

1. **The source was read, not copied blind.** The 134 rows of the v13 index were parsed and rewritten
   from a mapping, so the Document, What it is and Standard cells are byte-identical to the source.
   A verifier compares all 134 rows: 0 missing, 0 with changed text, 0 duplicate numbers.
2. **Every version came from the tree.** For each file named in the source, the highest version of the
   same family in the same folder was taken from the file names. 85 of the 134 rows moved to a new
   version; 49 rows keep the file they had, and each of those was checked to exist. The result agrees
   with the 85 rows D2-CTL records as continuing an existing family.
3. **Every new file of the run was read from the edit logs.** The "Files written" section of all 541
   edit logs was parsed, the 763 story files were rolled up to the 31 epic folders, and the non-story
   paths were checked against the tree. Files named in a log but absent from the tree (scratch and
   renamed drafts) are not listed. The story masters that exist at a new Markdown version without a
   workbook are listed at both versions and raised as CG-D2-IDX-1.
4. **The new sections.** "Microservice realignment" carries the decision and the counts (1,034 story
   files, 358 legacy keys, 822 service stories, 65 platform stories, 147 integration stories, 939 Day-1
   stories, 510 lanes, five team types), the 19 services with their schema, REST base, topic, task
   queue and epic copied character for character from the Ownership Map, the 31 story sets and their
   counts, one row for every document whose files changed or were added (98 rows, the same 98 the
   verifier finds), and the run material in folder 22. "Document gaps" carries 9 candidate gaps.
5. **Owners.** Every owner named in the file is taken from the Ownership Map: the 19 service codes own
   their service rows, the schema, REST base, topic and queue; the story folders follow the service or
   platform epic in their name; P3 owns parameters and reference data, P7 the rule package registry and
   P1 the interaction ledger, as the map's Rulings sheet records. No owner is invented for a document
   the map does not assign one to.
6. **Header, change log, dates.** Lines 1 and 2 are the R8.1 header. The change log holds the row
   `14, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`
   and the source row 13. No date of the source was moved and no release date is stated, so none is
   marked; the file says instead that release dates are unchanged and tentative (U7; DL48).

## Numbers kept

Every document number of the source (1 to 134) is kept with its text. Thirteen new numbers are used,
135 to 147, and none of them collides with a source number: 135 the microservice change register,
136 to 140 the service catalog, the service template specification, the service contract catalog, the
Kafka topic and event catalog and the Temporal workflow and activity catalog, 141 the integration test
plan, 142 and 143 the BRDs for Epics 3 to 8 and the 20 PRDs, 144 to 147 the story files, the service
epics, the Day-1 allocation and the service story catalog. The D-RCV-60, DL44 to DL49 and ADR-013 to
ADR-023 identifiers are the ones in `_work/msr/plan/ids.json`.

## Gaps and assumptions

- Gap candidate rows: 9 (CG-D2-IDX-1 to CG-D2-IDX-9), all P3, all documentation only.
- Assumption candidate rows: 11 (ASM-D2-IDX-1 to ASM-D2-IDX-11), confidence High except ASM-8
  (Medium).
- Every gap is paired with an assumption; ASM-10 (the BRDs and PRDs are Draft) and ASM-11 (the version
  numbers are the highest on disk) stand on their own.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp D2-IDX --quick` was run after the
build: C02, C03, C05, C12, C13 and C18 all PASS.
