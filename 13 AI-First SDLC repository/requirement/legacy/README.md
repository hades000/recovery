# Legacy corpus

This is the agent-readable copy of the twelve source folders. The originals remain in the parent
directory. Nothing here overwrites them.

## What is here

| Folder | Source | Entries |
|---|---|---:|
| `01-decisions-and-governance/` | 01 Decisions and governance | 2 |
| `02-business-architecture-and-process/` | 02 Business architecture and process | 22 |
| `03-requirements-and-specifications/` | 03 Requirements and specifications | 30 |
| `04-user-stories/` | 04 User stories | 217 |
| `05-technical-architecture/` | 05 Technical architecture | 64 |
| `06-data/` | 06 Data | 17 |
| `07-screens-and-experience/` | 07 Screens and experience | 9 |
| `08-ai-and-agents/` | 08 AI and agents | 8 |
| `09-testing-and-quality/` | 09 Testing and quality | 10 |
| `10-policy-controls-and-compliance/` | 10 Policy, controls and compliance | 5 |
| `11-delivery-and-operations/` | 11 Delivery and operations | 16 |
| `12-project-communication/` | 12 Project communication | 12 |

411 entries: 256 source files and 155 archive entries. The map is `DOCUMENT_MAP.md`; the conversion
report is `_conversion-report.md`; the machine manifest is `_manifest.json`.

## Canonical rules

1. **Markdown** is preferred for narrative.
2. **XLSX** is preferred for data; every sheet also has a CSV copy under `_csv/`.
3. **DOCX** is preferred for narrative where no Markdown exists.
4. **PPTX**, **HTML** and **PDF** are references where a canonical md/xlsx/yaml exists.
5. **ZIP** is the portable archive; the extracted folder is the working copy. For Epic 1 story files,
   the zip has 79 entries and the extracted folder has 69; the zip is canonical until the folder is
   completed.
6. The highest version in the filename is the set version; the internal document version is recorded
   in `DOCUMENT_MAP.md`.
7. `docs/` copies are working copies. Edit the source here, not the copy.

## How to use it

- **Context Builder** reads the business, architecture, data, access, test, policy and AI documents.
- **Requirement Intake Consolidator** reads the BRDs, business requirements, NFRs, rules, data and
  stories.
- **Technical Specifier** reads the story file plus the FSD/TSD, data dictionary, API spec, routing
  rules and error/message standard for the story's module.
- **Implementation Planner / Builder** read the spec, the plan and the context; the code lives in the
  ACE repository, not here.

## Conversion notes

- DOCX and PPTX images are counted but not extracted. The originals are in the source folders.
- XLSX cells use cached values; formulas without a cached value are blank.
- Merged XLSX cells are filled from the top-left value for readability.
- HTML conversion keeps text and tables; styling, scripts and navigation are removed.
- The 26 MB Project Hub is indexed as reference only.
- PDF files are skipped where an HTML or SQL equivalent exists.
- The `.~lock.*` LibreOffice lock file is skipped.

## Known version gaps

- Epic 1 consolidated v7 vs story files v5 (GAP-001).
- Epic 2 consolidated v5 vs story files v4 (GAP-002).
- File name vs internal document version drift (GAP-003).
- See `requirement/Intake_Gap_Report_RecoveryWorkbench.md` for the full list.
