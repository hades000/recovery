# Edit log - WP B-TECH-03 (Technical Specifications by Module v6)

Decision: D-RCV-60 microservice realignment. Tool: T3 Code / OpenCode / DeepSeek v4.1 Flash.
Date: 22 November 2026.

## Files written

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P1 Recovery data engine v4.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P2 Integration v4.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P3 Case and workflow v4.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P4 Access and administration v4.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P5 Document hub v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P6 Communications v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P7 Decision center and log v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P8 Payments and posting v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P9 Reporting v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD P10 Agent runtime v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S1 Valuation and route v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S2 TDR, settlement and deed in lieu v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S3 Guarantees and guarantors v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S4 Litigation and enforcement v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S5 Assets and auction v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S6 Debt sale v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S7 Write-off and recovery v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S8 Deviation handling v3.md`

- `05 Technical architecture/Recovery Workbench Technical Specifications by Module v6/Recovery Workbench TSD S9 Partner management v3.md`

- `_work/msr/gaps/B-TECH-03.jsonl`

- `_work/msr/assumptions/B-TECH-03.jsonl`

- `_work/msr/editlog/B-TECH-03.md`

Scratch, in `_work/msr/docs/B-TECH-03/`: `data.json` (the per-service contract data read from the
published OpenAPI and AsyncAPI files), `content.py` (the authored per-module contract content), `build.py`
(the writer that assembles each next version from its source), `registers.py` (the gap and assumption rows).

## What was done

The family `05 Technical architecture/Recovery Workbench Technical Specifications by Module v5` was copied
to `... v6` with `compat/office_write.py copy`. No source file was edited: every file that changes got its
next version inside the new folder, and the 20 unchanged historical files of the family were carried over
by the copy (P1 v2 and v3, P2 v3, P3 v3, P4 v3, and the v2 file of each of the other 15 modules).

1. **Header and change log.** Lines 1 and 2 of every new file are the header of Template and Rules R8.1.
   Document control adds the version, the date 22 November 2026, Supersedes, Decision, a Status note and the
   change-log row `4, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1
   Flash` (version 3 in the fifteen files whose next version is 3). The two files that keep a version history
   (P2) get the row `4, 22 November 2026, D-RCV-60 microservice realignment` in that table, and P1 gets a
   `Changes in version 4` table above its existing `Changes in version 3`. The related-documents table gains
   one row for the Microservice Ownership Map v1.
2. **Every section, ID, number and date kept.** T1 to T8, appendix T-A and T-B, the RBAC matrix, the NFR
   table, the traceability table, the LOVs, every API and field ID (API-S1-001, DF-COL-018, REQ-…, NFR-049,
   INT-21), every figure and every date of the source are present in the new version. The document dates of
   the superseded versions are kept in the Supersedes row and, for P2, in the version history.
3. **T0 Service added to all 20 modules.** T0.1 service identity (service, epic `RWB-SVC-<code>`, wave,
   schema, login, REST base, topic, event naming, namespace and queue, Java package, edge, contract
   artefacts, the two suggested owners of R5.3); T0.2 what the service owns, with the tables of the Ownership
   Map, the operations of appendix T-A and the published OpenAPI file, the events, the workflows and the jobs,
   each with a count; T0.3 the decoupling patterns of R5.5 that apply, quoting the line of the specification
   that carries the legacy marker; T0.4 what the service is not. Every owner is the Ownership Map owner.
4. **T5.2 rewritten as contracts.** T5.2.1 lists the provided REST operations with their `operationId` as
   published in `Recovery Workbench API Specification v5/<service>.yaml`, then the workflows, schedules,
   files and views provided, then the events published with the consumers of the Arch v5 catalogue. T5.2.2
   lists the consumed REST, Temporal, Nexus, SQL and file contracts with the provider service and the failure
   path, then the events consumed. T5.2.3 is the call-type summary with the counts. T5.3 restates the events
   with the EV numbers of the Arch v5 catalogue and names the events that have no number or no AsyncAPI
   operation instead of inventing one.
5. **The rest of the realignment.** T1 is restated for one service of 19 (one repository, one pipeline, one
   schema and login, screens through gateway-bff) and keeps its scope list word for word. The Jobs and
   Published-interface rows of T2 are restated for Temporal, the platform outbox and the contract set, with
   P1 and P2 handled explicitly (Quartz, the data lake publish and JOB-13). T3 gains the ownership note of
   the service and names the objects that the Ownership Map places elsewhere. T6.2 adds the authorise
   contract (DP-08), and for P4 states that it is the provider. Appendix T-A.1 carries the per-service base of
   DP-13 and a note that the published operation is the contract.
6. **Release dates.** No module specification states a release date, so no `(tentative)` mark was needed and
   no date was raised as a gap.
7. **Checks.** `python -I "22 Microservice Realignment/checks/run_all.py" --wp B-TECH-03 --quick` was run
   until it passed: C02, C03 and C05 (story-file checks, no story file in this WP), C12 (no person name, no
   email address), C13 (no issue-tracker reference), C18 (no write outside the WP list, no legacy file
   changed).

## Registers

- Gap rows: 9 (`GAP-1991` to `GAP-1999`); severity P2 4, P3 5; type Conflict 4, Missing 3,
  Ambiguous 2.
- Assumption rows: 9 (`ASM-3217` to `ASM-3225`); confidence High 4, Medium 5.
- No gap row raises a date and no value is invented: every missing value carries the R9 placeholder with its
  gap and assumption IDs.

## Not done, by rule

- No approval was sought and none is recorded; all 20 files are Draft.
- No master file was written, no register was numbered, and no other document was edited.
- T2.2 to T2.5 of P3 keep their version 3 text; the ownership conflict they carry is stated in the T2 note
  and in `GAP-1993` instead of being rewritten here.
