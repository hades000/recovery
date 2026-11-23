# Edit log B-PLT-DB-01 — RWB-PLT-DB (N011, NF-06)

SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Decision D-RCV-60. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## What was done

- Fanout 5: one task subagent per legacy key (N011, NF-06), each writing only that key's story file, fragment and candidate rows. NF-06 was written first; N011 appended its rows to the same two registers without touching the NF-06 rows.
- New folder `RWB-PLT-DB ACE DB schemas and logins` created for the two platform DB stories; no master and no legacy file was changed, edited or copied over.
- NF-06 (Moved, no impact) has no section text in the legacy index (title only, `chars` 0, `story_file` null), so its seven criteria and six test cases are new under D-RCV-60 and the absence is recorded as `GAP-1386`. N011 is a new key, so all six criteria are new.
- Boundary between the two stories was fixed once and is stated in both: NF06 creates the 19 empty schemas and the 19 logins with their own-schema privileges; N011 configures the 19 PgBouncer pools, creates the 19 migrator logins and builds the grant check. Neither issues the SELECT grant on the 30 `recovery.v_ace_*` views, which stays with RWB-P1-E1069-DB, and neither creates a table.
- Lead corrections after review, all inside this run's own files:
  - NF-06 AC4 asserted USAGE on schema `recovery` for `rwb_source_data`, which contradicts its own statement that the script writes no grant there and that the grant is RWB-P1-E1069-DB. AC4 is now "No login reaches schema recovery until RWB-P1-E1069-DB grants it", and the §11 attribute row and the fragment `text_first_line` were aligned.
  - NF-06 §7 AC7 cited "Arch v5 slides 20 and 11 of the Temporal design" in one phrase; split into Arch v5 slide 20 and Temporal and Drools design slide 11.
  - N011 §7 AC2 carried the placeholder inside a Given clause ("the connection cap of Not specified…"), which does not read as Gherkin; rewritten as a test value with the two ids in parentheses.
  - N011 §11: one unsourced note ("the highest-traffic service of wave 1") replaced with the slide 41 ownership phrase for `rwb_case`; the `rwb_partner` note rewritten to the partner gateway of Arch v5 slide 29.
  - N011 §12.8 had no fixture list; it now carries the four fixtures as a table like the sibling DB story. N011 §13 `pgbouncer.ini` row and §19 "tables of the 19 schemas" row were made grammatical and scoped to the per-service DB stories (NF-06 creates no table).
  - A stray test row (`{"id": "TESTROW", "title": "t"}`) that a subagent left in the gap register was removed before the register was closed.
- `patterns` is empty for both slices, so "Patterns applied" is `None`; the adjacency of DP-01, DP-02 and DP-15 is stated in the Solution plan of each story and no DP row is claimed in the metadata.

## Files written

- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-DB ACE DB schemas and logins/RWB PLT N011 DB PgBouncer pools, migrator role and grant check - ACE DB v1.md`
- `04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-DB ACE DB schemas and logins/RWB PLT NF06 DB Create the 19 rwb_  schemas and logins - ACE DB v1.md`
- `_work/msr/fragments/RWB-PLT-N011-DB.json`
- `_work/msr/fragments/RWB-PLT-NF06-DB.json`
- `_work/msr/gaps/B-PLT-DB-01.jsonl`
- `_work/msr/assumptions/B-PLT-DB-01.jsonl`
- `_work/msr/editlog/B-PLT-DB-01.md`

## Rows

- Candidate gaps: 8 rows — `GAP-1388` to `-4` (pool mode, size, cap and timeouts; migrator naming and credential; the product that delivers a per-login cap; where the check runs and how long its result is kept) and `GAP-1384` to `-4` (schema creation options; wave-0 environments and the role that runs the script; the absent legacy NF-06 text; owning login versus a separate migrator).
- Candidate assumptions: 8 rows — `ASM-2424` to `-4` and `ASM-2420` to `-4`, one per gap, all Medium confidence.
- Every citation in the two stories and the two fragments resolves to a row, and every row is cited by the story it belongs to.

## Checks run

- `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-PLT-DB-01 --quick`: C02, C03, C05, C12, C13 and C18 PASS with zero findings.
- Structural verifier over the two story files and two fragments (scratch script in the probe area, not an output): metadata rows equal Template and Rules §R7.1 and the split plan, 19 headings in order, every Scenario tagged, six and seven criteria, six test cases each, fragment keys and AC lines matching the story character for character, every citation resolved.
- Targeted C15, C16, C17 and C20 over the WP file set: PASS with zero findings.

## Failures

None.
