# Edit log - WP B-TECH-04 (Interface Specifications next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Status: Draft, no approval recorded (ASM-3226).

## Files written

- 05 Technical architecture/Recovery Workbench Interface Specifications v4.xlsx
- _work/msr/gaps/B-TECH-04.jsonl
- _work/msr/assumptions/B-TECH-04.jsonl
- _work/msr/editlog/B-TECH-04.md

Scratch files under `_work/msr/docs/B-TECH-04/` (build and verification only, not an output of the run):
`build.py` (changes the copy, sheet by sheet) and `verify.py` (source diff, counts, header and change-log check).
The converted source text is under `_work/msr/extract/B-TECH-04/` (Interface Specifications v3 and the
Ownership Map v1).

## What was done

**Recovery Workbench Interface Specifications v4.xlsx.** The source
`05 Technical architecture/Recovery Workbench Interface Specifications v3.xlsx` was never edited. It was copied
to v4 with `compat/office_write.py copy` and only the copy was changed:

1. **Read me sheet added first.** Rows 1 and 2 are the header of Template and Rules §R8.1. Row 11 is the
   change-log row `v4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash`;
   row 12 records the source version. Rows 14 to 24 say what the version holds and give the counts, rows 26 to 32
   the sources, rows 34 to 37 the open points and the candidate row range.
2. **Interfaces sheet (23 rows, was 25).** INT-19 (data lake and Power BI) and INT-20 (COLLINS model learning)
   are removed under DP-17 and ADR-018, because Architecture v5 has no data lake. Every remaining value is the
   v3 value character for character; `verify.py` diffs the 23 rows against the source: 0 differences outside the
   intended cells. Row 3 carries the new version stamp, and row 2 now gives 23 as the count and 25 as the v3 count.
3. **Per-service owners.** Three columns are added after Owner: `Owner code`, `Owning service` and `Owner basis`,
   filled for all 23 rows from the Microservice Ownership Map v1 (sheet Services) and Architecture v5 slides 9,
   17 and 30. The source Owner column is kept, except on INT-14, INT-24 and INT-25 where it read the single
   Workbench and now names the owning service; the same is done for the generic Owner of the fix values on nine
   rows. The ownership split is: P1 rwb-source-data 14 rows, P6 rwb-comms 3, and P2, P4, P10, PLT (RWB-PLT-OBS),
   S6 and S9 one each.
4. **Field mapping sheet (82 rows).** Every mapping, table.column, tier, read path, DF-* field, type and
   transformation is unchanged; one column `Owning service` is added and the seven outbound rows that read
   `Workbench` in the Owner column now name P6 rwb-comms (4 rows) and S6 rwb-debtsale (3 rows).
   No INT-19 or INT-20 mapping exists in v3, so none is removed.
5. **Outbound checks sheet.** The three checks of v3 (layout, control totals, acknowledgement) are identical
   cell for cell.
6. **Key sheet.** The 17 v3 rows are kept, the Workbench row is read as per service, and four rows are added:
   Owner code, Owning service, Owner basis and the removed interfaces INT-19 and INT-20.
7. **Realignment changes sheet (12 rows).** One row per change with the v3 value, the v4 value, the decision,
   the pattern and the basis. No release date appears in the source, so none was added; the release line of the
   Read me states that any date written later is tentative (U7).

**Owners.** Every owner comes from the Microservice Ownership Map v1 and `_work/msr/plan/ownership.json`; the
service owner of an interface is never taken from the story masters. The Ownership Map has no row for an
interface, so each owning service is derived from the read path or the delivery path and the basis is written
into the `Owner basis` cell: ADR-010 and slide 9 for the 14 inbound rows of P1, slide 30 for INT-17, INT-18,
INT-21, INT-22, INT-24, INT-35 and INT-36, slide 17 for INT-14, INT-25 and INT-34, and slides 6 and 8 for INT-23.

**Never edited, never invented.** No source file was changed, and no value was invented: where the sources are
silent the row is left as it is and the gap and assumption rows carry the point. The open points are the
reporting output after the removal of INT-19 and INT-20 (GAP-2000), the INT-21 read path against ADR-010
(GAP-2001), the single owner of INT-34 (GAP-2002), the owner of INT-14 and INT-25 (GAP-2003
and -5), the style of INT-24 (GAP-2005), the PII topic of INT-22 (GAP-2006), the LDM v7 citation
(GAP-2007) and the consumer of INT-35 and INT-36 (GAP-2008).

**Decisions used.** D-RCV-60 with the IDs of `_work/msr/plan/ids.json`: ADR-018 (no data lake, rwb-reporting read
model), ADR-010 as cited by the source, DL44 (adopt Architecture v5), DL45 (service epics) and DL46 (soft
ownership by team type). No new ADR or DL ID was allocated by this work package.

## Counts

| Item | Value |
|---|---|
| Candidate gap rows | 9 (GAP-2000 to GAP-2008) |
| Candidate assumption rows | 12 (ASM-3226 to ASM-3237) |
| Interfaces kept | 23 of 25 (INT-19 and INT-20 removed) |
| Field mappings kept | 82 of 82 |
| Outbound checks kept | 3 of 3 |
| Key rows added | 4 |
| Realignment change rows | 12 |

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-04 --quick`: PASS (C02, C03, C05, C12,
C13, C18). `verify.py` reports PASS: 23 interfaces, 82 field mappings, 3 outbound checks, 4 key rows added,
7 outbound owner rows made per service, header lines and change-log row present, and no other cell of the source
changed.
