# Shared updates requested: RWB-TE-002 (run INC-004-epic-1-RWB-TE-002, docs, 18 Nov 2026)

Shared files are not written by this stage (RUN-BRIEF rule 3). Spec, plan (SU-P01..SU-P08) and implement (IM-SU-01..IM-SU-03) rows stand.

| ID | Target (owner) | Requested change | Reason |
|---|---|---|---|
| SU-DOC-TE002-01 | `aisdlc/requirement/Traceability_Matrix.md` row 004 (Traceability Manager) | Add `DOC-RWB-TE-002-001`..`-015` against their stated `SPEC-*`, `AC*`, `BR*`, `TASK-*`, `CODE-TE002-*` and UT mappings; status `BUILT — ACCEPTANCE PENDING HV-01..HV-11`. | Documentation trace |
| SU-DOC-TE002-02 | `aisdlc/docs/open-items.md` (orchestrator) | No closure. Note that the documentation was produced with OPEN-016, OPEN-024, OPEN-038, OPEN-041, OPEN-050 and proposed `PROP-OI-1`..`-4` open, and HV-01..HV-11 `OPEN — NOT_TESTED_HERE`. | No approval recorded (D-RUN-09) |
| SU-DOC-TE002-03 (done at `c740d25`, `implement/plan-addendum.md`) | Orchestrator (merge of RWB-E1-042, IM-SU-01) | When writing `implement/plan-addendum.md`, keep the docs consistent: the added line is `/backend/src/test/resources/architecture/magic-number-baseline.csv @scb-ace/techx-recovery-tech-leads` in `[Recovery module]` after the `recovery-modules.yaml` line (file becomes 56 lines). If another form is chosen (directory pattern), update `docs/README.md` §4, `ARCHITECTURE.md` §3 and `COMPLIANCE.md` §5. | DOC-DG-01 |
| SU-DOC-TE002-04 | `aisdlc/DOCUMENT-GAPS.md` (orchestrator) | Optional: add DOC-DG-01 and DOC-DG-02 (Blocker = No). | Evidence inconsistencies |
| SU-DOC-TE002-05 | `aisdlc/docs/increments/INDEX.md` (orchestrator) | Status note only: "RWB-TE-002 documentation: `output/INC-004-epic-1-RWB-TE-002/docs/`; code gate and merge not yet recorded." | Index |

No human approval or ratification is recorded or requested by this stage.
| SU-DOC-TE002-06 | `aisdlc/requirement/Traceability_Matrix.md` row 004 (Traceability Manager) | Use the final-tip figures in `implement/shared-updates.md` IM-SU-05 (35 methods; coverage 95.77/95.90/96.85/100 at `d018cf7`) in place of any `ae61b08` figure in SU-DOC-TE002-01. | Implementation builder remediation run |
