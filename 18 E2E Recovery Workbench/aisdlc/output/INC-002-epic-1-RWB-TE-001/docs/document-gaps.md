# Document gaps: RWB-TE-001 documentation stage

No **new** document-set gap was found while writing the documentation. The two conflicts below are
carried from the story's own sources; both were settled before the gates, are visible in the spec and
are documented as accepted deviations in `COMPLIANCE.md` §5. They are repeated here so the reader of
this stage sees the evidence, not as new findings.

| Local ID | Document (name, version, section) | Gap or conflict | Second source that shows it | Blocker? | Why (blocker or not) | How this stage proceeded |
|---|---|---|---|---|---|---|
| DG-DOC-01 | Story file v7, RWB-TE-001 v1, §7 AC6 | AC6 names a `no-collection-import` frontend rule. The repository has no `src/modules/collection` and the frontend uses the `@/` alias. | Decision register `aisdlc/docs/decisions/decision-register.md`, D-RCV-39 (ESLint `no-restricted-imports` allow-list); spec v4 AC6 row records the deviation | No | D-RCV-39 is the governing decision and is applied by the inherited `eslint.config.js` block; the precedence rule lets the story proceed. | Documented as accepted deviation D-RCV-39 in `COMPLIANCE.md` §5. Both AC6 import forms are in the rejected set of `importBoundary.test.ts`. |
| DG-DOC-02 | Story file v7, RWB-TE-001 v1, §7 AC3 and §14 | AC3 asks the BND-3 failure to name "boundary rule BND-3". Spring Modulith `verify()` returns its own text and no bespoke rule prefix. | Decision register `aisdlc/docs/decisions/decision-register.md`, D-RCV-42 (Modulith text accepted, 2026-11-09); spec v4 AC3 row | No | D-RCV-42 is the governing decision; the failure still names both modules and the offending type, which is what the AC3 test asserts. | Documented as accepted deviation D-RCV-42 in `COMPLIANCE.md` §5. |

## Post-gate drifts (not document gaps)

`functional-tests/report.md` FAT-OBS-01 (the spec lists `frontend/eslint.config.js` as unchanged) and
FAT-OBS-02 (18 import cases, not 15) are differences between the gated plan and the delivered code,
not conflicts inside the document set. They are recorded in `../plan/plan-addendum.md` A-1 and A-3
and were accepted by the code gate (CODE-002, CODE-008). The documentation follows the delivered
code.
