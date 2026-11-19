# Shared updates proposed by specify: INC-001-epic-1-RWB-E1-044 (remediation run 1)

The orchestrator applies these. This stage edited none of the shared files (RUN-BRIEF rule 3). The first-run version is kept as `shared-updates.run1.md`.

## `aisdlc/requirement/Traceability_Matrix.md`

**§2 Business to functional trace.** Add `RWB-E1-044` to the Stories cell of the `BR-RWB-013` / `FR-RWB-013` row:

| Business requirement | Functional group | Stories |
|---|---|---|
| `BR-RWB-013` | `FR-RWB-013` | RWB-E1-044, RWB-E1-001, RWB-E1-069, RWB-E1-064, RWB-E1-065, RWB-TE-004 |

**§3 Story trace (Epic 1).** Replace row 001, using the matrix's own columns:

| INC | Story | Business | Functional | Spec / plan / evidence | Status |
|---|---|---|---|---|---|
| 001 | `RWB-E1-044` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` (SPEC-RWB-E1-044-001 to -017; sources REQ-RDF-001, REQ-RDF-014; NFR-027, NFR-052 cited by source ID) | Specified 2026-11-17 (v14 re-baseline, remediation run 1); spec gate round 2 pending; replaces the 10 Nov 2026 SPEC IDs and the FR-RWB-020 trace (DG-L08) |

**NFR IDs.** NFR-027 and NFR-052 are cited by their source ID (Non-functional specification v3). The matrix lists `NFR-RWB-001..010` only as a group in §1, with no map from source NFR IDs to matrix IDs, so no matrix NFR ID is claimed.

**§7 Evidence index.** Row `INC-001 RWB-E1-044`: Spec `output/INC-001-epic-1-RWB-E1-044/specify/spec.md`; Plan `historical` until re-planned; Implementation `not built`.

## `aisdlc/docs/open-items.md` (candidates)

| Candidate | Item | Owner | Source |
|---|---|---|---|
| OI-E044-A | Confirm that the AC8/X6 "failure record" is the ERROR log with MSG-P3-016 and the version, because PostgreSQL leaves no failed history row | BA / Product Owner | DG-L03, ASM-E044-02 |
| OI-E044-B | Resolve RWB-E1-069 v7 (two non-fix files, GRANTs inside migrations) against D-RCV-28 (1) and BS-2.5 before E1-069 is specified (seam SEAM-E044-02) | Recovery tech lead / BA | DG-L05 |
| OI-E044-C | The sources fix conflicting migration numbers (Decision Log v10 E1-001 = `V0001`; D-RCV-34; Build Sequence v6; story files v7). D-RUN-07 settles this repository: numbers are assigned at merge. The source documents are still unaligned | Recovery tech lead / BA | DG-L04 |
| OI-E044-D | Carry to the ACE port: D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step (not applicable here) | Recovery tech lead | ASM-E044-09 |
| OI-E044-E | Update OPEN-018 and OPEN-036: E1-044 re-baselined on 2026-11-17 against D-RCV-35/D-RCV-28. The story v7 text is still unaligned (DG-L01, DG-L02, DG-L11) | Orchestrator | DG-L01, DG-L02, DG-L11 |
| OI-E044-F | **How a recovery migration references the ACE source schema.** ADR v3 ADR-010, D-RCV-35 and Env v4 §5 need `FROM public.<table>` inside `CREATE VIEW ${recoverySchema}.v_ace_*`, and the D-RCV-28 lint shipped by E1-044 rejects it. Per the orchestrator triage, RWB-E1-069 adds the narrow exception at the lint's single extension point (`public.` only inside a `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` statement; never for foreign keys). Env v4 §5 says "Schema names are parameters", but no source names an ACE-schema placeholder; confirm the exception (or name a parameter) before RWB-E1-069 is specified | Recovery tech lead with BA | DG-L09; SPEC-016 SEAM-E044-01 |
| OI-E044-G | **No story owns the D-RCV-12 job-monitor parts of RWB-E1-044:** `MigrationRunRecorder`; `GET /admin/jobs?type=MIGRATION` with version, checksum and drift result; the SCR-44 migration-run display; AC8 "failed on the job monitor"; the story §10 read and rerun authority (RW-PLATADM, RW-DATASTEW, RW-AUDIT); TC-E1-044-10 (RW-CASEOWN refused with MSG-P4-002). D-RCV-12 names no story, and RWB-E1-056 v7 and API Specification v4 `getAdminJobs` do not carry them. Name the owning story or add them to one | BA / Product Owner | DG-L10; SPEC-017 |
| OI-E044-H | Inform RWB-TE-001: E1-044 adds a test-scope tooling class set to `recoveryCoverageReport` / `recoveryCoverageVerification` and the INSTRUCTION and METHOD limits. TE-001 adds its own directory to that wiring (D-RCV-43 (2); SEAM-E044-04) | Orchestrator (inform RWB-TE-001 planner) | SPEC-014 |

## `aisdlc/DOCUMENT-GAPS.md` (candidates)

Add DG-L01 to DG-L12 from `specify/document-gaps.md` as programme rows. None is a blocker. The rows new in this run are DG-L09 (ADR-010 views versus the D-RCV-28 lint), DG-L10 (D-RCV-12 names no receiving story), DG-L11 (refused-clean message: story v7 versus squad D-RCV-28 (4)) and DG-L12 (D-RCV-48 text names schema `ace`).

## `aisdlc/docs/increments/INC-001-epic-1-RWB-E1-044.md` (card status)

Specification: remediation run 1, 2026-11-17 (spec v14-2). Spec gate round 2 result is in `review/spec-gate-review-2.md`.

## Repository `README.md` (note, not a shared AISDLC file)

The root README repeats "RWB-E1-001 ships V0001 to V0003" (DG-L07). The migration-folder README is corrected under SPEC-015. The root README is left to the orchestrator.
