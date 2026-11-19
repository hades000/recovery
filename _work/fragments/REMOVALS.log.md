# Removals log (Wave 3)

Date: 15 November 2026. Decision: D-RCV-35, Change Register v1 Appendix A. One `<KEY>.remove.json` per story in this folder.

Sources searched: the six consolidated story md files (Epic 1 v7, Epic 2 v5, Epics 3 to 8 v2, Technical Enabler Stories v5, Data Migration Stories v2, Administration Stories v2) and their xlsx Stories, Test cases and Dependencies sheets.

| Key | Title | Later home | TCs | Dependents (live) |
|---|---|---|---:|---|
| RWB-E1-003 | ALS daily extract load | ACE ingestion (RWB-ACE-001); content parked in Data Load Story Removals v1, obsolete per v2 | 15 | RWB-E1-002, RWB-E1-015, RWB-E1-058, RWB-E2-008; via feature FEAT-RDF-03: RWB-E8-002 |
| RWB-E1-004 | EFS extract load | ACE ingestion (RWB-ACE-001) | 11 | RWB-E2-001, RWB-E2-034; via feature FEAT-RDF-04: RWB-E4-039 |
| RWB-E1-005 | Excel and SharePoint inventory | Cutover plan (U5): Cutover and Go Live Plan v3, section 8 Tracker retirement | 9 | None |
| RWB-E1-006 | Data quality rules v1 | ACE ingestion checks (RWB-ACE-001); the daily gate moves into RWB-E1-015 | 10 | RWB-E1-011, RWB-E1-015 |
| RWB-E1-009 | CCMS and SVAF loads | ACE ingestion (RWB-ACE-001) | 12 | None |
| RWB-E1-010 | Excel and SharePoint loads | Cutover plan (U5): Cutover and Go Live Plan v3, section 8 Tracker retirement | 14 | None |
| RWB-E1-012 | Retire local copies | Cutover plan (U5): Cutover and Go Live Plan v3, section 8 Tracker retirement | 11 | RWB-E1-025, RWB-E1-045, RWB-E1-046 |
| RWB-E1-051 | Legacy feed jobs on ADF and Control-M | ACE ingestion (RWB-ACE-001); no ADF job remains | 7 | None |
| RWB-E2-023 | Automated EFS file load | ACE ingestion (RWB-ACE-001) | 9 | None |
| RWB-DM-001 | Migrate account and arrears | Not needed: the data is in ACE (read through recovery.v_ace_* views, RWB-E1-069) | 4 | None |
| RWB-DM-002 | Migrate customer and party | Not needed: the data is in ACE (read through recovery.v_ace_* views, RWB-E1-069) | 4 | None |

Total TCs removed: 106.

## Notes

- Dependencies between removed stories (for example RWB-E1-004 on RWB-E1-003, RWB-E1-010 on RWB-E1-005, RWB-E2-023 on RWB-E1-051) go away with the stories. They are listed under `removed_dependents` in each json.
- RWB-E1-051: TC-E1-051-02 and TC-E1-051-03 appear only in the Epic 1 v7 xlsx Test cases sheet, not in the md section. Remove both from the sheet.
- RWB-DM-001 and RWB-DM-002: the Data Migration v2 workbook has no Test cases sheet. Remove the Stories rows; the TC IDs come from the md sections.
- RWB-E4-039 and RWB-E8-002 name a removed feature (FEAT-RDF-04, FEAT-RDF-03) in Depends on, not the story key. Their agents should drop it or point to RWB-ACE-001 / RWB-E1-069.
- Text-only mentions (no Depends on row) are listed under `text_mentions` in each json. Live stories affected: RWB-E1-007 (E1-004, E1-051), RWB-E1-011 (E1-003), RWB-E1-056 (E1-051), RWB-E1-065 (E1-003, E1-004), RWB-E1-066 (E1-004), RWB-E1-002 (E1-004), RWB-E2-001 (E1-051, E2-023), RWB-E2-010 (E1-006). The summary tables at the top of Epic 1 v7.md and Epic 2 v5.md also lose the removed rows and the removed keys in their Depends on column.
- RWB-E1-007 is not removed. It survives as outbound-only adapters.
- `14 Story Updates/Recovery Workbench Data Load Story Removals v2.md` records the new homes. v1 is left unchanged.
