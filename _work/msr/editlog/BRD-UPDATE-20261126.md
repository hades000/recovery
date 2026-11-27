# BRD update, 26 November 2026

At the user's instruction, the existing BRD files and the registers were edited in place. This overrides AGENTS.md rule 1 for this update only. The originals are kept in the session scratchpad backup.

## Files changed
- 03 Requirements and specifications/Recovery Workbench Business Requirements Program v5 (.md, .docx). The changes:
  - New section 2.1 lists all 27 measures.
  - NFR-079 and NFR-080 are added; the document now holds 80 NFRs.
  - Section 9 gains 15 open decisions: DL01, DL02, DL03, DL09, DL14, DL19, DL21, DL24, DL25, DL28, DL29, DL30, DL31, DL39 and DL40.
  - Section 12 now uses register IDs (CG-n becomes GAP-(1490+n); ASM-n becomes ASM-(2602+n)). New section 12.3 is added.
  - New section 13 lists the regulatory obligations (32).
  - New section 14 lists the audit findings (42).
  - New section 15 lists the controls (44).
  - New section 16 lists the reports (14).
  - The story code RWB-E1-069 becomes BR-E1-020, and RWB-ACE-001 becomes "the ACE DB additions (DL43)".
- Epic 1 v5 (.md, .docx):
  - Re-keyed to BR-E1-001..BR-E1-069.
  - The section 9 Stories column becomes Position.
  - Story codes removed.
- Epic 2 v3 (.md, .docx):
  - Re-keyed to BR-E2-001..BR-E2-032.
  - The section 9 Stories column becomes Position.
  - The story identifier convention is removed.
- Epics 3 to 8 v1 (.md, .docx):
  - 168 story code lists removed.
  - Story key ranges become feature counts.
  - Program citations updated from v4 to v5.
- 23 Document Gaps/Gap Register v1 (.md, .xlsx):
  - GAP-3254..GAP-3270 added.
  - GAP-1493 and GAP-1495 Closed (resolved in Program v5).
  - GAP-1515, GAP-1526, GAP-1543 and GAP-1671 set to "Duplicate of GAP-1592".
- 23 Document Gaps/Assumptions Register v1 (.md, .xlsx): ASM-5684..ASM-5689 added.

## Key map
The old story code for each new requirement ID is in BRD-UPDATE-20261126-keymap.json.

## Checks
- No RWB-E*/ACE/TE story code is left in the four BRD .md or .docx files.
- Every GAP and ASM ID cited in the BRDs exists in its register.
- The .docx files were rebuilt with the same md-to-docx logic as compat/office_write.py. Before the edits, that rebuild reproduced the previous files exactly.

## Corrected during the run
- GAP-3260 was first written as 17 measures. The source has 20 measures with a "To set" baseline or target, 13 of them with both. Corrected in the BRD and the register.
