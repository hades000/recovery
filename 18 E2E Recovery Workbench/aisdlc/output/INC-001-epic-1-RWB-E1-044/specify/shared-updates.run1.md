# Shared updates proposed by specify: INC-001-epic-1-RWB-E1-044

The orchestrator applies these. This stage edited none of the shared files (RUN-BRIEF rule 3).

## `aisdlc/requirement/Traceability_Matrix.md`

| Story | Requirement | FR / NFR | SPEC | Spec path | Status |
|---|---|---|---|---|---|
| RWB-E1-044 | REQ-RDF-001, REQ-RDF-014 | BR-RWB-013 / FR-RWB-013; NFR-027; NFR-052 | SPEC-RWB-E1-044-001 to SPEC-RWB-E1-044-015 | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` | Specified 2026-11-17 (v14 re-baseline); replaces the 10 Nov 2026 SPEC IDs and the FR-RWB-020 trace (DG-L08) |

## `aisdlc/docs/open-items.md` (candidates)

| Candidate | Item | Owner | Source |
|---|---|---|---|
| OI-E044-A | Confirm that the AC8/X6 "failure record" is the ERROR log with MSG-P3-016, because PostgreSQL leaves no failed history row | BA / Product Owner | DG-L03, ASM-E044-02 |
| OI-E044-B | Resolve RWB-E1-069 v7 (two non-fix files, GRANTs inside migrations) against D-RCV-28 (1) and BS-2.5 before E1-069 is specified | Recovery tech lead / BA | DG-L05 |
| OI-E044-C | Align the migration sequence plan: Decision Log v10 D-RCV-28 (E1-001 = V0001) vs D-RCV-34 and Build Sequence v6 (E1-042 first) | Recovery tech lead / BA | DG-L04 |
| OI-E044-D | Carry to the ACE port: D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step (not applicable here) | Recovery tech lead | ASM-E044-09 |
| OI-E044-E | Update OPEN-018 and OPEN-036: E1-044 re-baselined on 2026-11-17 against D-RCV-35/D-RCV-28; the story v7 text is still unaligned (DG-L01, DG-L02) | Orchestrator | DG-L01, DG-L02 |

## `aisdlc/DOCUMENT-GAPS.md` (candidates)

Add DG-L01 to DG-L08 from `specify/document-gaps.md` as programme rows. None is a blocker.

## `aisdlc/docs/increments/INC-001-epic-1-RWB-E1-044.md` (card status)

Specification: SUCCESS 2026-11-17 (v14 re-baseline); spec gate result as in `review/spec-gate-review.md`.

## Repository `README.md` (note, not a shared AISDLC file)

The root README repeats "RWB-E1-001 ships V0001 to V0003" (DG-L07). The migration-folder README is corrected under SPEC-015. The root README is left to the orchestrator.
