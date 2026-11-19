# Shared-file updates proposed by RWB-TE-002 specify (remediation runs 1 and 2)

RUN_ID `INC-004-epic-1-RWB-TE-002`, stage `specify`, 2026-11-17. This stage edits no shared file
(RUN-BRIEF hard rule 3). The orchestrator applies these rows in order and assigns final IDs.

## 1. `aisdlc/docs/open-items.md`

| Proposal | Action | Item | Stories affected | Owner (role) | Needed by | Raised in |
|---|---|---|---|---|---|---|
| `PROP-OI-1` | Amend OPEN-038 | Add to OPEN-038: (a) replace the role placeholders `@role-placeholder/solution-architect-with-tech-leads` (Engineering Practices v5 §10, AGENTS.md owner) and `@role-placeholder/techx-devops-with-scb-it` (pipeline gates) with real group handles; (b) confirm the ACE GitLab tier offers code-owner approval on protected branches; (c) confirm the GitLab setting names in HC-01–HC-08; (d) the reserved common pattern depends on OPEN-024; (e) **(run 2, SG-015)** change OPEN-038 "Needed by" from "Before TE-002 build" to "Before TE-002 is used on the ACE host". Reason: the local build goes ahead with OPEN-038 open under L-RCV-03 (no question in an automated stage) and the orchestrator's triage for remediation run 2 (the orchestrator is Claude Code, the AI agent running this pipeline). The placeholders are acceptable at the `develop-recovery` merge only if the MR body shows OPEN-038 as open (spec "Local completion state"). | RWB-TE-002 | ACE team repository administrator / recovery tech lead | Before TE-002 is used on the ACE host | INC-004 spec SPEC-017, SPEC-018, ASM-TE002-10, -15; spec gate review 2 SG-015 |
| `PROP-OI-2` | New | Run human-verification items HV-01–HV-11 of the RWB-TE-002 spec on the ACE GitLab project after HC-01–HC-08 are applied; record MR link and result per item. Until then each item is OPEN, not passed, and RWB-TE-002 is reported as `BUILT — ACCEPTANCE PENDING HV-01..HV-11`, never Done against story §13. HV-07 includes the first run of `codeowners-validation` and its coverage gate in a pipeline. | RWB-TE-002 | ACE team repository administrator with the recovery tech lead | Before the first recovery MR merges in ACE | INC-004 spec SPEC-018 |
| `PROP-OI-3` | New | A-05 parts excluded from RWB-TE-002: a package-level AGENTS.md and a separate coding-standard file. Route to an AISDLC-HARDENING change or record as out of scope in the final report. | — | Solution architect with the tech leads (role); orchestrator | Final delivery report | INC-004 spec SPEC-019; `phase0-standards-audit.md` A-05 |

## 2. `aisdlc/DOCUMENT-GAPS.md`

Candidate rows, all non-blocking, evidence in `specify/document-gaps.md`: SP-DG-01 to SP-DG-09 (same
as review DG-01 to DG-09; add once) and SP-DG-10 (story §12 single-line BR4 entry vs BR7 "reviewed by
both teams"; suggested owner: BA, next story issue).

## 3. `aisdlc/requirement/Traceability_Matrix.md`

| Section | Change |
|---|---|
| §3 row 004 `RWB-TE-002` | Spec/plan column: `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (remediation run 2); plan to be re-run. Status: `Specified — spec gate re-review spec-gate-review-3.md; plan not started; build not started`. After build, the status is `Built — acceptance pending HV-01..HV-11`, not Done. |
| New SPEC map (or evidence index note) | `REQ-DRI-006` → `BR-RWB-013` / `FR-RWB-013` → `US-RWB-TE-002` → `SPEC-RWB-TE-002-001` … `-019`. Host-only verification items HV-01–HV-11 are not tests and carry no TEST ID until run (`PROP-OI-2`). |
| §6 coverage note | TE-002 spec is current for this repository; the v2 spec is history in `_v2-baseline/`. |

## 4. `aisdlc/docs/increments/INC-004-epic-1-RWB-TE-002.md` (card status)

| Field | Proposed value |
|---|---|
| Specification | `DRAFT → per spec-gate-review-3.md` — `output/INC-004-epic-1-RWB-TE-002/specify/spec.md` (remediation run 2, 2026-11-17) |
| Compliance review | `REVIEW-RWB-TE-002-SG-2026111701` FAIL (0C/2H/6M/3L); `REVIEW-RWB-TE-002-SG-2026111702` FAIL Low-only (0C/0H/0M/5L); re-review `spec-gate-review-3.md` |
| Contract extract | File `.gitlab/CODEOWNERS` (L-RCV-12); entries as spec SPEC-001–005, -017 |
| Done state | `Built — acceptance pending HV-01..HV-11` (spec SPEC-018); never Done until the HV items pass on the ACE host |
