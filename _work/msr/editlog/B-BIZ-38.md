# Edit log - WP B-BIZ-38 (Recovery Workbench Users Roles and Permissions next version)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026. Work pack: B-BIZ-38. Fanout: 0.

## Files written

- `02 Business architecture and process/Recovery Workbench Users Roles and Permissions v5.xlsx`
- `_work/msr/docs/B-BIZ-38/build_v5.py`
- `_work/msr/docs/B-BIZ-38/verify_v5.py`
- `_work/msr/docs/B-BIZ-38/dump.txt`
- `_work/msr/docs/B-BIZ-38/k.txt`
- `_work/msr/gaps/B-BIZ-38.jsonl`
- `_work/msr/assumptions/B-BIZ-38.jsonl`
- `_work/msr/editlog/B-BIZ-38.md`

The source text for reading was produced with the sanctioned conversion command into `_work/msr/extract/B-BIZ-38/`. The source workbook was never opened for writing: v5 is a copy of v4 made with `compat/office_write.py copy`, and every addition was then written into the copy by `build_v5.py`.

## What was done

1. **Header and change log.** The new `Read me` sheet is the first sheet. A1 and A2 are the two header lines of Template and Rules R8.1, word for word. The change-log table carries the row `5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash` and the v4 row that the Roles tab note records; the literal R8.1 row is repeated as a single line so the string is found by any reader. The sheet also states the source version, the status Draft and the tool.
2. **Authorise contract of rwb-access (new sheet 10).** Eleven tables, A1 to A11: the eight REST operations provided (the four of the contract — POST /authorise, GET /me/permissions, GET /doa-limits, GET /masking-policies — plus the four P4 administration operations of the Ownership Map), the operation consumed from ACE Common (sign-in, JWT, group to role), the two events published on rwb.access.events.v1 (AccessPolicyChanged, DoaLimitChanged) and none consumed, JOB-18 as a six-monthly Temporal Schedule, the six tables of rwb_access, the contract fake and the build rule, the call-type summary (REST, Kafka, Temporal, File), the eight-step check sequence, the refusal and failure model with the access-story messages, and the owner, contract stories, consumers, wave and readiness. Owner, table, job, event and operation names are taken from the Microservice Ownership Map v1 and Architecture v5 slides 14, 35 and 41; the 2 s timeout, the circuit breaker, the 15-minute idle timeout, the 5-minute membership refresh and the one-hop rule are quoted from the same sources.
3. **Area owners (new sheet 11).** The 14 capability areas of the Permissions tab, each with its owning service, schema, REST base, the owned tables, endpoints, events, jobs and workflows that justify the owner, and the number of roles that hold a letter in the area (42, 27, 20, 30, 31, 21, 17, 42, 38, 42, 39, 29, 36 and 6, counted from the Permissions tab). A fifteenth row gives the role, permission, conflict, masking and DoA data itself to P4 rwb-access, which is not one of the 14 areas. Two notes cover the partner and customer roles and the derived counts.
4. **Roles tab: one new column.** Column K, `Enforcing services (D-RCV-60)`, for all 54 rows. The value is P4 rwb-access plus the service of every area in which the role holds a letter on the Permissions tab, so it is derived and not invented. The seven PT-LED and CU rows hold no area and say so in words. No existing cell changes; the filter is widened to A4:K58.
5. **Access flow tab: two rows.** Review step 3 is the six-monthly JOB-18 access review list in rwb-access; Break-glass step 5 is AccessPolicyChanged, published so every service refreshes its cached permissions and DoA limits. The 15 v4 rows are untouched; the filter is widened to A4:E21.
6. **Three note rows, added after the last v4 row.** Separation of duty: the eight pairs are rows of rwb_access.role_conflict, read by the grant check and the sign-in check. Single sign-on: rwb-access resolves each Entra ID group to a role code at sign-in through ACE Common group-to-role. Systems by role: ACE and TDR data reaches a role through P1 rwb-source-data's contract or the `recovery.v_ace_*` views, never by a direct table read (DP-05).
7. **Key tab: six rows.** Column K, the Authorise contract sheet, the Area owners sheet, the tentative rule, the access check and the version v5 row. The 16 v4 rows are untouched.
8. **Every source value kept.** `verify_v5.py` compares all 2285 non-empty cells of the eight v4 sheets against v5: 0 differences, and the eight v4 sheets keep their v4 order behind the new Read me sheet.
9. **Document properties.** v4 carries a person name in Creator and Last modified by. Both are set to "Henka Group" in v5; title, subject, description and keywords carry version 5, D-RCV-60, the tool line and the Draft status. No person name and no email address appears in any cell of v5.
10. **Dates.** No date is added, changed or removed. v4 states no release date; the release labels E1 to E8 are copied unchanged and the Read me and the Key tab state that every one of them is tentative (D-RCV-60, U7). The document date is the run date, 22 November 2026.
11. **Decisions.** Only the IDs of `_work/msr/plan/ids.json` are used: D-RCV-60, the existing D-RCV-35 reference of the v4 note, DP-05, DP-07, DP-08, DP-11, R5.4 and R5.7 of the Template and Rules. No new ADR, DL or decision number is created. The contract stories cited are RWB-P4-E1037-CON and RWB-PLT-E1037-CON from `split_plan.json`, and RWB-P4-E1039-DB for the access log.

## Gaps and assumptions

- Gap rows written: 11 (`GAP-0159` to `GAP-0169`).
- Assumption rows written: 11 (`ASM-0243` to `ASM-0253`), one twin per gap.
- Severity: 4 rows P2 (CG-1, CG-2, CG-3, CG-6) and 7 rows P3 (CG-4, CG-5, CG-7, CG-8, CG-9, CG-10, CG-11). No row is P1.
- Subjects: the schema of the four authorise operations (1); the two names of the sign-in read (2); the cache lifetime and the failure rule (3); the DoA amounts (4); the masking rules (5); the partner user to role link between S9 and P4 (6); the access log table (7); the credential of the six non-human actors (8); the blank Counts tab (9); OWN/TEAM/ALL against REGION (10); no approval or status (11).
- Placeholders appear on the Read me sheet (11 open points), in the Authorise contract A1, A6, A9, A10 and A11, and in the Area owners note; each one carries its CG and ASM pair exactly as Template and Rules R9 requires.

## Checks

`python -I "22 Microservice Realignment/checks/run_all.py" --wp B-BIZ-38 --quick` was run after the files were written: C02, C03, C05, C12, C13 and C18 all PASS with zero findings. `verify_v5.py` reports 2285 source cells compared, 0 differences, the eight v4 sheets in their v4 order and every structural count as expected (54 role rows, 11 columns on Roles, 58 by 17 on Permissions, 13 rows on Separation of duty, 21 on Access flow, 54 on Single sign-on, 42 on Systems by role, 26 on Key, 15 area rows). No failure needed a fix in the document.

## Notes

- Every owner in the two new sheets is the table, endpoint, job or event owner of the Microservice Ownership Map v1; no owner is invented and none is a person.
- The ownership ruling that keeps `partner_user` with S9 while P4 keeps the internal role model is applied as written, and the open point is recorded as CG-6 rather than resolved.
- The Counts grid is left blank as v4 leaves it, because three role classes hold values that are not release numbers; the class totals of the Roles tab note are confirmed instead (ASM-9).
- `dump.txt` and `k.txt` are scratch review outputs of the two new sheets and the new column; they carry no value of their own.
