| Date | File | Agent | Sections | IDs | Open questions |
|---|---|---|---|---|---|
| 15 Nov 2026 | Business Requirements Epic 1 v4.docx | W2 writer | Title, control, §1, §2, §3.1, §3.2, §4, §5, §7 | E1-003/004/006/009/051 -> ACE ingestion; E1-005/010/012, REQ-RDF-005/006 -> Cutover; +RWB-E1-069, +RWB-ACE-001; DL43 open; 60 live / 50 Must / 75 program reqs | E1-069 test count "-" until story written |
| 15 Nov 2026 | Business Requirements Program v4.docx | W2 writer | Control, §1.1, §5 intro, §5.1–5.3, §6.3, §6.5 NFR-032, §7, §9 | RDF-005/006/008 removed; 228 of 231 live; DL43 added; DL06/12/20 re-worded | none |
| 15 Nov 2026 | Epics 3 to 8 Specification v3 docx+xlsx | W2 writer | Control, integrations 2.4–5.4, E3–E6 data rows, 17 features | INT-12/13/16 into ACE; no ID changes | FEAT-VAL-05 name "Call COLLINS for return by route" no longer fits a view read (Feature List rename?); AMIS monthly ingestion may lag the holding clock |
| 15 Nov 2026 | Physical Schema v5 (verify) | Docker verifier | — | 92 tables, 30+1 views, 4 ext, 122/1,366 = LDM v7, 0 public FKs | 4 FAIL -> DM1 fix |
| 15 Nov 2026 | Information Flow v5.pptx | W2 writer | All 11 slides | DL43 slide 11; trackers via Cutover | cover thumbnail image still v4 |
| 15 Nov 2026 | API Specification v3 yaml+html | W2 writer | 7 paths, 10 schemas removed; re-keyed; /assets/{assetKey} | 137 ops, 168 schemas, info 3.0.0 | Asset.holdingStatus/holdingCostToDate no column (DM1); other docs citing /assets/{assetId} |
| 15 Nov 2026 | TSD P2 Integration v3 | W2 writer | T1, T1.1, T3, T4, T5.1, API | API-P2-013/014 retired; outbound = INT-14/19/20/25 + ACE paths INT-17/18/22/34 | LOV-INTERFACE-RUN seed (DM1) |
| 15 Nov 2026 | Security and Access v3, Environment and Deployment v3 | W2 writer | §1–§11 / §1–§8 | recovery_svc, ace_view_owner; two-migration rule | role name recovery_svc to confirm |
| 15 Nov 2026 | Target Architecture v5 docx+pptx, ACE AD v3 | fix agent | 14 defects | DL43, risk "RWB-ACE-001 late" | none |
| 15 Nov 2026 | Lean BRD v3, NFS v3, Batch v3, Event v3 | fix agent | all listed defects + NFR-032 | AsyncAPI 2.0.0; JOB-07/08 after JOB-02 | Batch xlsx C8 JOB-04 "balances against the core bank" (minor) |
| 15 Nov 2026 | Decision Log v9, Rulings v2 x2, Admin model v5 | fix agent | all listed | By owner DL43; seed table = CDM v6 | schema sys_objects 98/24 vs CDM 97/25; schema SoR wording (DM1) |
| 15 Nov 2026 | FSD P1 v3 | W2 writer | A1–A2.20 rewritten | FEAT-RDF-03..10,22 removed (IDs kept); REQ-RDF-005/006 removed; OQ-P1-01..08 | freshness before RWB-ACE-001 (decision: hard dependency via DL43, no interim view); valuation_ext stale rule owner; per-account break rows (reconciliation_result) |
| 15 Nov 2026 | FSD P2 v3, FSD P3 v3 | W2 writer | P2 outbound-only rebuild; P3 targeted | FEAT-DRI-09 removed; FEAT-CHO-10 removed; primary_person_key | MSG-P1-001 reworded "Today's data is not yet complete." -> Error and Message Standard (out-of-tracker doc); GL posting as EV-24 confirm |
