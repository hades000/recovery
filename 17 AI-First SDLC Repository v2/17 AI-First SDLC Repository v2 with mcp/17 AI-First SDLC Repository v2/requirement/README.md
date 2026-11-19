# Requirement corpus

| Path | Content | Status |
|---|---|---|
| `legacy/` | Converted document set v14: 01–12 plus the 14, 15, 16 change packs, the E1-042 pack and ACE schema extracts. 733 entries, 0 failures. | Canonical |
| `Context_RecoveryWorkbench.md` | Context index, CTX IDs and build decisions | Current |
| `BRD_RecoveryWorkbench.md` | Business requirements document, BR-RWB-001..020 | Current |
| `RecoveryWorkbench_Requirements.md` | Canonical functional and non-functional requirements | Current |
| `Intake_Gap_Report_RecoveryWorkbench.md` | Gaps, conflicts and resolution | Current |
| `Traceability_Matrix.md` | Business → functional → story → spec/plan/evidence | Current |

## Rules

1. `legacy/` is a converted copy; the original files stay in the twelve source folders and the change
   pack folders. Do not edit a converted file to make a story pass.
2. The map of every source file is `legacy/DOCUMENT_MAP.md`; the machine-readable version is
   `legacy/_manifest.json`.
3. A document superseded by a later version is marked `Superseded` in the map. The newest version and
   the newest change register win.
4. The 16 November 2026 baseline uses story set v7 (Epic 1), v5 (Epic 2), Physical Schema v6,
   API Specification v4, ADR v3 and Decision Log v10.
5. D-RCV-35 and D-RCV-36 are binding; D-RCV-47 is superseded.
