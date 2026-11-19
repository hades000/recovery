# Shared-file updates proposed by INC-010-epic-1-RWB-E1-069 (Technical Specifier, run 2)

Under RUN-BRIEF hard rule 3 this stage edits no shared file. The orchestrator applies the rows below after the spec gate passes. Run 1's proposals are kept in `shared-updates.run1.md` and are replaced by this file.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

### §3 Story trace: replace row 010 (columns `INC | Story | Business | Functional | Spec / plan / evidence | Status`)

| 010 | `RWB-E1-069` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` (SPEC-RWB-E1-069-001..020; sources REQ-RDF-002, REQ-DRI-006, D-RCV-35 U4; NFR-045, NFR-054 direct; NFR-039, -040 partial; NFR-042 to RWB-E1-016) | Specified (spec gate per `review/spec-gate-review-2.md`) |

### SPEC-to-test detail (for the evidence index or the run's README; it mirrors the `spec.md` test table)

| SPEC | AC / BR | Tests |
|---|---|---|
| 001 | AC1, §4 step 2 | TC-E1-069-01, T-E1-069-11 |
| 002 | BR6, BR3 | TC-E1-069-02, -06, T-E1-069-09, -10 |
| 003 | AC1, AC6, BR1 | TC-E1-069-01, -06 |
| 004 | AC2, BR2, BR3 | TC-E1-069-02 |
| 005 | AC3, BR9 | TC-E1-069-03 |
| 006 | AC3, BR1, BR2 | TC-E1-069-03, T-E1-069-14 |
| 007 | AC1, AC7, BR7 | TC-E1-069-01, -07 |
| 008 | AC1–AC5, BR3–BR5 | TC-E1-069-01..05, T-E1-069-17 |
| 009 | AC2, BR2, BR3 | TC-E1-069-02 |
| 010 | AC5, AC6, BR5 | TC-E1-069-05, -06 |
| 011 | AC7, BR4, BR7 | TC-E1-069-07 |
| 012 | AC8, BR8 | TC-E1-069-08 |
| 013 | AC8, BR8, BR9 | TC-E1-069-08, T-E1-069-12 |
| 014 | §4 step 2 (enabler for AC1, AC3) | T-E1-069-11 |
| 015 | AC1–AC3 (local stand-in), AC2.2 | TC-E1-069-01..03, T-E1-069-16 |
| 016 | BR8 (A-02 regression) | TC-E1-069-08 |
| 017 | AC1.5–1.6, AC3.2–3.3, BR2 | TC-E1-069-01, -03, T-E1-069-14 |
| 018 | AC3.4, X2 | TC-E1-069-03, T-E1-069-13 |
| 019 | §17 guardrails; NFR-039, -045, -054 | T-E1-069-15 |
| 020 | BR6 | TC-E1-069-06, T-E1-069-09, -10 |

### §6 Coverage summary

- Epic 1 stories row: "Current spec" 4 → 5 (when the round-2 gate passes).
- Add `RWB-E1-069` (INC-010) to "Current spec/plan, not built" once the plan exists; until then add a line "Current spec, no plan: `RWB-E1-069` (INC-010)".

### §7 Evidence index: add

| INC-010 `RWB-E1-069` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` | not yet | not built |

## 2. `aisdlc/docs/open-items.md` (proposed; the orchestrator assigns numbers)

| Proposed | Item | Owner (per source) | Evidence |
|---|---|---|---|
| OI-069-A | ACE DBA preconditions in DEV, SIT and PROD: (a) migration account holds USAGE on `public`; (b) it is a member of `ace_view_owner`; (c) it owns schema `recovery` or may grant CREATE on it; (d) the ACE DBA grants USAGE on `public` and SELECT on the 21 Tier 1 tables (and the 14 Tier 2 tables with RWB-ACE-001) to `ace_view_owner`, and revokes ALL on schema `public` from PUBLIC. | ACE DBA / ACE team lead | spec P4; DG-L13, DG-L22; [E2] |
| OI-069-B | RWB-ACE-001 Appendix A maps the 12 new columns into Section A view columns that ACE Source Views v1 does not contain. Decide whether to version the Tier Map or the Source Views file. | Data architect, recovery tech lead | DG-L07 |
| OI-069-C | RWB-ACE-001 AC4 ("14 new tables and no other table") conflicts with its §10 and §12 ("21 listed tables"). | ACE team lead | DG-L08 |
| OI-069-D | Confirm the merge gate for the Section B file: it merges after RWB-ACE-001 is deployed, because it cannot be skipped under `outOfOrder(false)`. | Recovery tech lead | DG-L20 |
| OI-069-E | Align Environment and Deployment Design v4 (lines 124, 126), Security and Access Design v4 and the ACE Source Views v1 comments with story BR3 and §3 (role creation; "no write on any recovery table"; the `ALL TABLES` grant). | Solution architect | DG-L09, DG-L10, DG-L11 |
| OI-069-F | Confirm the BND-6 rulings: `PlatformInfoController`'s `information_schema` read is allowed; `information_schema.` / `pg_catalog.` qualifiers are exempt; detector (d) is case-sensitive on table identifiers. | Recovery tech lead, security | ASM-013; audit A-02 |
| OI-069-G | Correct `ace_to_date` in ACE Source Views v1 (lines 31–43) and Physical Schema v6 (lines 6141–6157) to meet BR6 and the file's own comment; accept the run-2 deviation from "verbatim" for the helper body only. | Data architect | DG-L23; ASM-012 |
| OI-069-H | Security review of the definer-rights trade-off: views run with `ace_view_owner`'s table privileges, so any ACE row-level security must be applied inside the view. | Security architect | ACE Source Views v1 lines 20–21; spec SPEC-019 |
| OI-069-I | Decide who grants `recovery_svc` DML on Workbench tables in SIT and above: story BR3 says V0001; the RWB-E1-001 spec (T7) says V0001 carries no GRANT. | Recovery tech lead with RWB-E1-001 | DG-L25 |
| OI-069-J | Align `sys_fields.is_personal` (9 DF-ACE fields in Physical Schema v6) with the Data Classification Inventory v4 (250 personal DF-ACE fields). | Data architect with RWB-E1-001 | DG-L24 |
| OI-069-K | Align story RWB-E1-069 AC5 and TC-05 (122 / 1,366 / 1,062) with Physical Schema v6 (123 / 1,379 / 1,075), and the Data Classification Inventory v4 header likewise. | Story owner (analyst), data architect | DG-L05 |

## 3. `aisdlc/DOCUMENT-GAPS.md` (proposed rows; full evidence in `specify/document-gaps.md`)

| Proposed | Gap | Blocker? |
|---|---|---|
| DG-INC010-01 | RWB-ACE-001 is an external dependency for Section B (DL43, 2026-11-21) | No |
| DG-INC010-02 | Extension tables: V0001 (story §4, E1-001, Physical Schema v6) vs V0002 (AC1, §12, §13) | No |
| DG-INC010-03 | D-RCV-28 lint (one file per key, `${recoverySchema}` only, no GRANT) vs D-RCV-35 §3.2/§8.2; resolved through SEAM-E044-01/-02 | No |
| DG-INC010-04 | Story §13 step 7 "skip V0003" vs `outOfOrder(false)` | No |
| DG-INC010-05 | README "Local versus target": "V0001-V0003 from RWB-E1-001" vs story v7 (fixed by SPEC-015) | No |
| DG-INC010-06 | backend-context §4.2 extension-table names vs story and Physical Schema v6 | No |
| DG-INC010-07 | Story §12 ACE-side grants vs D-RCV-35 §8.2, RWB-ACE-001 and story §10 (DG-L22) | No |
| DG-INC010-08 | `ace_to_date` body in ACE Source Views v1 and Physical Schema v6 raises on impossible dates, against BR6 (DG-L23) | No |
| DG-INC010-09 | `is_personal` in Physical Schema v6 vs Data Classification Inventory v4 (DG-L24) | No |
| DG-INC010-10 | `recovery_svc` DML grants in SIT+: story BR3 vs RWB-E1-001 spec T7 (DG-L25) | No |
| DG-INC010-11 | Dictionary totals: story AC5 and Inventory v4 (122/1,366/1,062) vs Physical Schema v6 and D-RCV-36 (123/1,379/1,075) (DG-L05) | No |

## 4. `aisdlc/docs/increments/INDEX.md` and increment card INC-010

- **INDEX row 010:** status "Specified"; spec column per `review/spec-gate-review-2.md`.
- **Card:** Specification "SUCCESS 2026-11-18 (run 2)"; Compliance review per the round-2 gate file.

## 5. Repository files changed by the build of this story (for the plan, not applied here)

These are part of SPEC-015 and change with the story's code, not as shared-file edits:
- `.env.example` and `docker-compose.yml`: `RWB_LOAD_REFERENCE_SCHEMA` defaults to `false`; the `.env.example` comment says reference mode needs `rwb.flyway.enabled=false`.
- `README.md` "Local versus target": Flyway mode is the default; the view files belong to RWB-E1-069; run `./scripts/dev.ps1 reset` once after the switch.
- `README.md` "Decisions taken while setting this up", proposed item 8 (local deviation): in opt-in reference mode, `20-grants.sql.inc` still grants `ace_view_owner` SELECT on all `public` tables and USAGE and CREATE on `recovery`, which is broader than BR2; Flyway mode follows the named grants (ASM-008).
- `backend/src/main/resources/db/modulemigration/recovery/README.md`: the same correction.
