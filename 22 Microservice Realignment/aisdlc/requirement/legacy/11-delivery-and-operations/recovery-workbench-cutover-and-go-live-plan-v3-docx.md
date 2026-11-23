<!-- source: 11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v3.docx -->
<!-- converted: 2026-11-16 from DOCX -->

> **Source:** `11 Delivery and operations/Recovery Workbench Cutover and Go Live Plan v3.docx`  
> **Converted from:** DOCX

Recovery Workbench

Cutover and go-live plan

SCB Collections and Recovery. Henka Group, 15 November 2026

| Item | Detail |
|---|---|
| Document | Recovery Workbench cutover and go-live plan |
| Version | 2 |
| Date | 15 November 2026 |
| Prepared by | Henka Group |
| Structure | Henka word rules |

# 1. How releases go live

Each monthly release goes live in the change window agreed with SCB IT (DL34). The first release, 30 November 2026, also starts the case list. The Workbench runs no load: ACE ingests every source and the release reads the 30 SELECT-only recovery.v_ace_* views (D-RCV-35, ADR-010). The release is ready when the ACE batch is ready, so the checks in section 6 are release gates.

# 2. Sequence for each release

| When | Step | Who |
|---|---|---|
| Friday before | Go decision on the SIT and UAT exits; flags for unfinished work confirmed off | Release owner with the product owner and application owner |
| Release day minus 1 | Reference data, rules and templates for the release loaded with their valid from date | Reference data administrator |
| Release day | Deploy the tag to production in the change window | ACE team |
| Release day | Smoke test: sign-in per role, case list, one decision, one notice | QA engineers with business testers |
| Next morning | ACE batch for the business date checked in v_ace_batch_status, then the case list reconciled to the ACE account view | Data steward |
| First week | Floor support for the teams that receive real users | Business analysts, business lead |
| Four weeks after | Benefit check (G6) | Product owner |

# 3. Rehearsal

Each release is rehearsed in UAT: the deploy, the reference data load, the smoke test and the rollback. The first release is rehearsed twice.

# 4. Rollback

- Switch the feature flags for the release off.

- If a flag does not cover the fault, redeploy the previous tag.

- Reload the previous reference data versions if they changed.

- Decisions taken under the new release stay in the decision log; corrections are new entries.

- No ACE data is rolled back with the Workbench: the views read the ACE batch for the business date, and a wrong batch is corrected in ACE.

# 5. Who decides to go

The release owner in the ACE team decides with the product owner and the application owner. A severity 1 or 2 defect open without a flag stops the release.

# 6. ACE batch readiness check

The check runs on the release day before the smoke test, and again on the first morning after the release. A failed check holds the part of the release that reads ACE; the Workbench features that read no ACE data go ahead behind their flags.

| Check | Passes when | Who confirms |
|---|---|---|
| ACE additions | RWB-ACE-001 is applied in PROD and the 14 tables and 12 columns are present | ACE team lead |
| Batch complete | ace_batch_run holds a COMPLETED row for each recovery source and the business date, and v_ace_batch_status returns it | ACE ingestion owner |
| Grant in place | The view-owner role selects the 21 listed ACE tables and no other; the recovery role reads recovery.v_ace_* only and writes no ACE table | ACE DBA with SCB IT security |
| Views resolve | 16 Section A and 14 Section B views compile, and the conformance test resolves the 80 appendix fields | Data steward |
| Case list runs | JOB-02 starts on AceDataReady for the ALS business date and creates no case from an incomplete batch | QA lead with the data steward |
| Fallback agreed | If a check fails, the case list holds, the data screens stay behind their flags, and the ACE team names the recovery date | Release owner with the product owner |

# 7. First release specifics

| Item | Plan |
|---|---|
| Case list | Built from the ACE account view on the first COMPLETED ALS batch for the business date; reconciled to v_ace_account before it is shown |
| ACE views | 16 Section A views live on the day; the 14 Section B views and the 12 new ACE columns need RWB-ACE-001 (DL43, due 21 November) |
| Spreadsheets | Retired team by team under the procedure in section 8; each team keeps a read-only archive |
| Access | Administration roles only; business roles from Epic 2 (DL39) |
| Documents | Store and OCR live; bulk intake of open-case documents starts |

# 8. Tracker retirement

The 20 Excel and SharePoint trackers, 14 marked LOAD and 6 marked RETIRE in the inventory, are retired in this release, team by team. Six teams own them: TDR, DIL, LIT, NPA, DEBT_SALE and WRITE_OFF. None is loaded into the Workbench. RWB-E1-005, RWB-E1-010 and RWB-E1-012 are removed under D-RCV-35, so the Workbench provides no inventory, no load and no retirement screen: the procedure below is run by the teams and recorded in one report.

| Step | What happens | Who |
|---|---|---|
| 1 | The team manager works from the case list for two working days after the last tracker file of the team is signed off | Team manager |
| 2 | The team manager makes each tracker read-only or moves it to the read-only archive, and records the archive location | Team manager |
| 3 | The team manager confirms the retirement of each tracker, with the archive location and the date | Team manager |
| 4 | The data steward records the fields of each tracker that no data product carries, for the later epic that picks them up | Data steward |
| 5 | The Tribe lead reads the six-team report: trackers, retired, outstanding and the confirming manager for each team | Tribe lead |
| 6 | The report is filed with the release checklist on 26 November 2026; a team with an outstanding tracker is named with its tracker codes | Tribe lead with the business lead |

# 9. Open decisions

| Decision | What is needed |
|---|---|
| DL12 | Which legacy systems are kept |
| DL34 | The release window |
| DL43 | Whether the ACE team accepts RWB-ACE-001 and its 21 November date |
