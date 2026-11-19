# Shared updates proposed by specify: INC-001-epic-1-RWB-E1-044 (remediation run 2)

The orchestrator applies these. This stage edited none of the shared files (RUN-BRIEF rule 3). Earlier versions are kept as `shared-updates.run1.md` (first run) and `shared-updates.run2.md` (remediation run 1). Run 2 changes: the §3 row status, OI-E044-B reworded (S14), OI-E044-I new (S15), DG-L13 added to the DOCUMENT-GAPS candidates, card status.

## `aisdlc/requirement/Traceability_Matrix.md`

**§2 Business to functional trace.** Add `RWB-E1-044` to the Stories cell of the `BR-RWB-013` / `FR-RWB-013` row:

| Business requirement | Functional group | Stories |
|---|---|---|
| `BR-RWB-013` | `FR-RWB-013` | RWB-E1-044, RWB-E1-001, RWB-E1-069, RWB-E1-064, RWB-E1-065, RWB-TE-004 |

**§3 Story trace (Epic 1).** Replace row 001, using the matrix's own columns:

| INC | Story | Business | Functional | Spec / plan / evidence | Status |
|---|---|---|---|---|---|
| 001 | `RWB-E1-044` | `BR-RWB-013` | `FR-RWB-013` | `output/INC-001-epic-1-RWB-E1-044/specify/spec.md` (SPEC-RWB-E1-044-001 to -017; sources REQ-RDF-001, REQ-RDF-014; NFR-027, NFR-052 cited by source ID) | Specified 2026-11-18 (v14 re-baseline, remediation run 2, spec v14-3); spec gate round 3 pending; replaces the 10 Nov 2026 SPEC IDs and the FR-RWB-020 trace (DG-L08) |

**NFR IDs.** NFR-027 and NFR-052 are cited by their source ID (Non-functional specification v3). The matrix lists `NFR-RWB-001..010` only as a group in §1, with no map from source NFR IDs to matrix IDs, so no matrix NFR ID is claimed.

**§7 Evidence index.** Row `INC-001 RWB-E1-044`: Spec `output/INC-001-epic-1-RWB-E1-044/specify/spec.md`; Plan `historical` until re-planned; Implementation `not built`.

## `aisdlc/docs/open-items.md` (candidates)

| Candidate | Item | Owner | Source |
|---|---|---|---|
| OI-E044-A | Confirm that the AC8/X6 "failure record" is the ERROR log with MSG-P3-016 and the version, because PostgreSQL leaves no failed history row | BA / Product Owner | DG-L03, ASM-E044-02 |
| OI-E044-B | Resolve RWB-E1-069 v7 against the lint E1-044 ships, before E1-069 is specified (seam SEAM-E044-02). (1) Two non-fix files per key against D-RCV-28 (1) (L-KEY-DUP). (2) The Section A grants on `public` (`GRANT USAGE ON SCHEMA public …`, `GRANT SELECT ON public.account, …`, revoke from PUBLIC; D-RCV-35 U4, Env v4 §5, Physical Schema v6 grant block) against L-GRANT (BS-2.5, BS-2.6) **and** L-LITERAL-SCHEMA items 3 (bare `SCHEMA public`) and 4 (`public.` identifiers). SEAM-E044-01 does not cover grant statements; any allowance for them is decided here. One documented route keeps them out of the recovery migration: the ACE DBA applies them (RWB-ACE-001 v1 §4 flow 5; RWB-E1-069 v7 §10). Decide together with OI-E044-I | Recovery tech lead / BA | DG-L05 |
| OI-E044-C | The sources fix conflicting migration numbers (Decision Log v10 E1-001 = `V0001`; D-RCV-34; Build Sequence v6; story files v7). D-RUN-07 settles this repository: numbers are assigned at merge. The source documents are still unaligned | Recovery tech lead / BA | DG-L04 |
| OI-E044-D | Carry to the ACE port: D-RCV-45 `db-migrate` guard, H2 skip, Jenkins step (not applicable here) | Recovery tech lead | ASM-E044-09 |
| OI-E044-E | Update OPEN-018 and OPEN-036: E1-044 re-baselined on 2026-11-17 against D-RCV-35/D-RCV-28. The story v7 text is still unaligned (DG-L01, DG-L02, DG-L11) | Orchestrator | DG-L01, DG-L02, DG-L11 |
| OI-E044-F | **How a recovery migration references the ACE source schema.** ADR v3 ADR-010, D-RCV-35 and Env v4 §5 need `FROM public.<table>` inside `CREATE VIEW ${recoverySchema}.v_ace_*`, and the D-RCV-28 lint shipped by E1-044 rejects it. Per the orchestrator triage, RWB-E1-069 adds the narrow exception at the lint's single extension point (`public.` only inside a `CREATE [OR REPLACE] VIEW ${recoverySchema}.v_ace_*` statement; never for foreign keys). Env v4 §5 says "Schema names are parameters", but no source names an ACE-schema placeholder; confirm the exception (or name a parameter) before RWB-E1-069 is specified | Recovery tech lead with BA | DG-L09; SPEC-016 SEAM-E044-01 |
| OI-E044-G | **No story owns the D-RCV-12 job-monitor parts of RWB-E1-044:** `MigrationRunRecorder`; `GET /admin/jobs?type=MIGRATION` with version, checksum and drift result; the SCR-44 migration-run display; AC8 "failed on the job monitor"; the story §10 read and rerun authority (RW-PLATADM, RW-DATASTEW, RW-AUDIT); TC-E1-044-10 (RW-CASEOWN refused with MSG-P4-002). D-RCV-12 names no story, and RWB-E1-056 v7 and API Specification v4 `getAdminJobs` do not carry them. Name the owning story or add them to one | BA / Product Owner | DG-L10; SPEC-017 |
| OI-E044-I | **Who holds the privilege to grant on `public` and to set the view owner for RWB-E1-069.** RWB-E1-069 v7 §3 says the recovery migration account holds the ACE DBA role for the release window, and attributes it to RWB-E1-044. E1-044 declines it (SPEC-017; DG-L13): D-RCV-35 U3/U4 and ADR v3 ADR-010 give the migration account no privilege in `public`, and RWB-ACE-001 v1 and RWB-E1-069 v7 §10 give the grant to the ACE DBA. Align RWB-E1-069 v7 §3 with §10, and name who runs the Section A grants and the `ALTER VIEW … OWNER TO ace_view_owner`, before RWB-E1-069 is specified. The RWB-E1-069 spec must not treat the role as delivered by E1-044 (D-RUN-08) | Recovery tech lead with the ACE team lead / ACE DBA | DG-L13; SPEC-017 |
| OI-E044-H | Inform RWB-TE-001: E1-044 adds a test-scope tooling class set to `recoveryCoverageReport` / `recoveryCoverageVerification` and the INSTRUCTION and METHOD limits. TE-001 adds its own directory to that wiring (D-RCV-43 (2); SEAM-E044-04) | Orchestrator (inform RWB-TE-001 planner) | SPEC-014 |

## `aisdlc/DOCUMENT-GAPS.md` (candidates)

Add DG-L01 to DG-L13 from `specify/document-gaps.md` as programme rows. None is a blocker. New in remediation run 2: DG-L13 (RWB-E1-069 v7 §3 attributes an ACE DBA role for the migration account to RWB-E1-044, against RWB-E1-044 v7 §3/§10, RWB-E1-069 v7 §10, RWB-ACE-001 v1, ADR-010 and D-RCV-35 U3/U4); DG-L05 now names L-LITERAL-SCHEMA and cites D-RCV-35 U4. New in remediation run 1: DG-L09 (ADR-010 views versus the D-RCV-28 lint), DG-L10 (D-RCV-12 names no receiving story), DG-L11 (refused-clean message: story v7 versus squad D-RCV-28 (4)) and DG-L12 (D-RCV-48 text names schema `ace`).

## `aisdlc/docs/increments/INC-001-epic-1-RWB-E1-044.md` (card status)

Specification: remediation run 2, 2026-11-18 (spec v14-3). Spec gate round 3 result is in `review/spec-gate-review-3.md` (round 2: `review/spec-gate-review-2.md`).

## Repository `README.md` (note, not a shared AISDLC file)

The root README repeats "RWB-E1-001 ships V0001 to V0003" (DG-L07). The migration-folder README is corrected under SPEC-015. The root README is left to the orchestrator.
