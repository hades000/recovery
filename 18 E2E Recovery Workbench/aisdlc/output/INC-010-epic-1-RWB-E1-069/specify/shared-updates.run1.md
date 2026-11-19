# Shared-file updates proposed by INC-010-epic-1-RWB-E1-069 (Technical Specifier)

Under RUN-BRIEF hard rule 3, this stage did not edit any shared file. The orchestrator applies the rows below, in the order given.

## 1. `aisdlc/requirement/Traceability_Matrix.md`

### Replace row 010

| 010 | `RWB-E1-069` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-010-epic-1-RWB-E1-069/specify/spec.md` | Specified 17 Nov 2026: SPEC-RWB-E1-069-001..016; sources `REQ-RDF-002`, `REQ-DRI-006`, D-RCV-35 U4; spec gate per `review/spec-gate-review.md` |

### Add SPEC rows

| SPEC ID | Story | Upstream | AC / BR | Test |
|---|---|---|---|---|
| SPEC-RWB-E1-069-001 | RWB-E1-069 | REQ-RDF-002; FR-RWB-013 | AC1; §4 step 2 | TC-E1-069-01 |
| SPEC-RWB-E1-069-002 | RWB-E1-069 | REQ-RDF-002; FR-RWB-013 | BR6; BR3 | TC-E1-069-02, -06 |
| SPEC-RWB-E1-069-003 | RWB-E1-069 | REQ-RDF-002; D-RCV-35 U4 | AC1, BR1, BR6 | TC-E1-069-01, -06 |
| SPEC-RWB-E1-069-004 | RWB-E1-069 | REQ-DRI-006; D-RCV-35 U4; ADR-010 | AC2, BR2, BR3 | TC-E1-069-02 |
| SPEC-RWB-E1-069-005 | RWB-E1-069 | REQ-RDF-002; DL43 | AC3, BR9 | TC-E1-069-03 |
| SPEC-RWB-E1-069-006 | RWB-E1-069 | REQ-RDF-002; DL43 | AC3, BR1 | TC-E1-069-03 |
| SPEC-RWB-E1-069-007 | RWB-E1-069 | D-RCV-35 U3/U4 | AC1, AC7, BR7 | TC-E1-069-07 |
| SPEC-RWB-E1-069-008 | RWB-E1-069 | REQ-DRI-006; D-RCV-35 U4 | AC1, AC4, AC5, BR4, BR5 | TC-E1-069-01, -04, -05 |
| SPEC-RWB-E1-069-009 | RWB-E1-069 | REQ-DRI-006; ADR-010 | AC2, BR2, BR3 | TC-E1-069-02 |
| SPEC-RWB-E1-069-010 | RWB-E1-069 | REQ-RDF-002 | AC5, AC6, BR5 | TC-E1-069-05, -06 |
| SPEC-RWB-E1-069-011 | RWB-E1-069 | D-RCV-35 U3 | AC7, BR4, BR7 | TC-E1-069-07 |
| SPEC-RWB-E1-069-012 | RWB-E1-069 | REQ-DRI-006; audit A-02 | AC8, BR8 | TC-E1-069-08 |
| SPEC-RWB-E1-069-013 | RWB-E1-069 | REQ-DRI-006 | AC8, BR8 | TC-E1-069-08 |
| SPEC-RWB-E1-069-014 | RWB-E1-069 | D-RCV-35 §3.2/§8.2; D-RCV-28 | AC1, AC3 (enabler) | lint unit test |
| SPEC-RWB-E1-069-015 | RWB-E1-069 | REQ-RDF-002 | AC1–AC3 (local stand-in) | TC-E1-069-01..03 |
| SPEC-RWB-E1-069-016 | RWB-E1-069 | REQ-DRI-006 | BR8 (A-02 regression) | TC-E1-069-08 |

## 2. `aisdlc/docs/open-items.md` (proposed new items; the orchestrator assigns the numbers)

| Proposed | Item | Owner (per source) | Evidence |
|---|---|---|---|
| OI-069-A | Confirm that the ACE DBA revokes USAGE on schema `public` from PUBLIC in DEV, SIT and PROD. The exact AC2 message "permission denied for schema public" depends on it. | ACE DBA / ACE team lead | DG-L13; RWB-ACE-001 §12 step 4 |
| OI-069-B | The RWB-ACE-001 Appendix A maps the 12 new columns into Section A view columns that ACE Source Views v1 does not contain. Decide whether to version the Tier Map or the Source Views file. | Data architect, recovery tech lead | DG-L07 |
| OI-069-C | RWB-ACE-001 AC4 ("14 new tables and no other table") conflicts with its §10 and §12 ("21 listed tables"). | ACE team lead | DG-L08 |
| OI-069-D | Confirm the merge gate for the Section B migration. It merges after RWB-ACE-001 is deployed, because the stage cannot be "skipped" under `outOfOrder(false)`. | Recovery tech lead | DG-L20 |
| OI-069-E | Align Environment and Deployment Design v4 (lines 124 and 126), Security and Access Design v4 and the ACE Source Views v1 comments with story BR3 and §3. The points are role creation, "no write on any recovery table" and the `ALL TABLES` grant. | Solution architect | DG-L09, DG-L10, DG-L11 |

## 3. `aisdlc/DOCUMENT-GAPS.md` (proposed rows; the full evidence is in `specify/document-gaps.md`)

| Proposed | Gap | Blocker? |
|---|---|---|
| DG-INC010-01 | RWB-ACE-001 is an external dependency for Section B (DL43, 2026-11-21) | No |
| DG-INC010-02 | Extension tables: V0001 (story §4, E1-001, Physical Schema v6) vs V0002 (AC1, §12, §13) | No |
| DG-INC010-03 | D-RCV-28 lint (one file per key, `${recoverySchema}` only, no GRANT) vs D-RCV-35 §3.2/§8.2 | No |
| DG-INC010-04 | Story §13 step 7 "skip V0003" vs `outOfOrder(false)` | No |
| DG-INC010-05 | README "Local vs target": "V0001-V0003 from RWB-E1-001" vs story v7 | No |
| DG-INC010-06 | backend-context §4.2 extension-table names vs story and Physical Schema v6 | No |

## 4. `aisdlc/docs/increments/INDEX.md` and increment card INC-010

- **INDEX row 010:** set the status to "Specified" and the spec column to the spec-gate result in `review/spec-gate-review.md`.
- **Card status:** Specification "SUCCESS 2026-11-17"; Compliance review per the gate file.

## 5. `README.md` "Decisions taken while setting this up" (proposed item 8, local deviation)

- **Proposed item 8:** in reference mode, `20-grants.sql.inc` grants `ace_view_owner` SELECT on all `public` tables and USAGE and CREATE on `recovery`. This is broader than RWB-E1-069 BR2. Flyway mode follows the named grants in V0002 and V0003 (ASM-008).
- **Correction to "Local vs target":** V0002 and V0003 belong to RWB-E1-069, not to RWB-E1-001 (DG-L18).
