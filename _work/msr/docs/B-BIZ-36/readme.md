SCB Collections and Recovery. Henka Group, 22 November 2026.
(C) Siam Commercial Bank and Henka Pte Ltd

Recovery Workbench Feature List v5

Next version of Recovery Workbench Feature List v4.xlsx. Decision D-RCV-60 microservice realignment: the four sheets are carried over unchanged in their order and content, two columns are added from the Microservice Ownership Map v1, and every release date is marked (tentative).

Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.

## Change log
v5, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash
## What changed in v5

1. Features sheet: two columns are added at the end, O "Service (D-RCV-60)" and P "Service epic (D-RCV-60)", filled on all 378 rows from the Microservice Ownership Map v1 Services sheet. O carries the service code and short name as the map writes them ("P1 rwb-source-data"); P carries the service epic of Template and Rules R4 and R5.1 ("RWB-SVC-P1"). The service wave is not a column; the wave of each service is in the Counts note below.
2. Features sheet: the Release column (L) keeps every date character for character and adds " (tentative)", under R1 U7 and root rule 10.
3. By module sheet: the same two columns are added at the end, H and I, on the 19 module rows. The Total row stays empty.
4. By epic sheet: the Release column keeps every date character for character and adds " (tentative)".
5. Key sheet: two rows are added, one for each new column, inside the Column group.
6. Read me: this sheet is new. It carries the header of Template and Rules R8.1, this change log and the notes below, and it is the first sheet.

## What did not change

1. All 378 feature rows stay in the same order with every Feature ID, module code, module name, class, feature name, "What it does", primary role, other roles, L1 processes, systems, epic, story keys and "Depends on" unchanged. No feature is added, rewritten, renamed, re-scoped or deleted in this version.
2. The note row of the Features sheet still reads "368 live features in 19 modules across eight epics. Ten retired features remain listed. Two new features (FEAT-RDF-25, 26) cover the ACE read path and the ACE additions. Class is User, Admin, System or Retired - ACE ingestion; filter on Epic or Module." word for word, with its counts of 368 live and 10 retired.
3. The ten retired features keep the class "Retired - ACE ingestion" and stay listed for traceability.
4. Story keys are the legacy keys of the source (A1, W1, B17, E2b, C7, N8, N9, O3, O13 and the rest). The new story IDs of R5.2 (RWB-<scope>-<legacy>-<work type>) are not written into this workbook; the Service Story Catalog and the story files carry them.
5. The By module and By epic counts stay live formulas over the Features sheet (COUNTIFS on Features columns B, D and K). The two appended columns sit outside every formula range, so both sheets still calculate.
6. The Features, By module, By epic and Key sheets keep their order, their titles, their second note row, their autofilter and their freeze point.

## Counts

Features: 378 rows (368 live and 10 retired) with 2 appended columns at O and P, 756 appended cells. By service: P3 52, P7 35, P4 30, S5 25, P1 23, P5 22, S4 22, P6 21, S8 19, S2 18, P10 16, S6 16, S7 16, S9 15, S1 12, P8 11, P9 10, S3 8, P2 7; total 378.

By epic: E1 120, E2 77, E4 50, E6 37, E3 31, E5 26, E8 19, E7 18; total 378.

Release: 378 cells on the Features sheet and 8 cells on the By epic sheet keep their date and add "(tentative)". The eight dates are 30 Nov 2026, 31 Dec 2026, 31 Jan 2027, 28 Feb 2027, 31 Mar 2027, 30 Apr 2027, 31 May 2027 and 30 Jun 2027, unchanged.

Waves: the service wave is taken from the Ownership Map: wave 1 for P1, P2, P3, P4, P5, P6, P7, P9, P10; wave 2 for P8, S2, S5, S8; wave 3 for S1, S3, S4, S6; wave 4 for S7, S9. The business-epic wave follows W-MAP: E1 wave 1; E2 and E3 wave 2; E4 and E5 wave 3; E6, E7 and E8 wave 4.

Structure: 4 source sheets kept, 1 sheet added ("Read me", first); 2 columns added on 2 sheets; 2 new Key rows.

## Open points

CG-B-BIZ-36-1 to CG-B-BIZ-36-8 and ASM-B-BIZ-36-1 to ASM-B-BIZ-36-8 in the Gap Register and Assumptions Register: the module-to-service mapping and the 13 module names that differ from the service names; the single recovery schema of FEAT-RDF-01; the ten interaction-ledger features listed in module P7; the two decision-log lake copies and the reporting feature on story A14; the seven other features that name the data lake; the nine features that name the Quartz scheduler; the missing wave column and the 17 service-and-epic pairs that disagree; and the two feature-flag features listed in P3.

Release dates are tentative and unchanged. The last release is 30 June 2027, inside the eight months of R1 U7. No date is raised as a gap.
