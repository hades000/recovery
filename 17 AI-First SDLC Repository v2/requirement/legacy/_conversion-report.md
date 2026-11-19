# Conversion report

Run: 2026-11-16

Source files and zip entries: **733**

## By conversion status

| Status | Count |
|---|---:|
| converted | 225 |
| copied | 61 |
| extracted | 432 |
| skipped | 7 |
| unsupported | 8 |

## By format

| Format | Count |
|---|---:|
| .csv | 3 |
| .docx | 74 |
| .html | 18 |
| .md | 471 |
| .pdf | 3 |
| .pptx | 28 |
| .ps1 | 2 |
| .py | 1 |
| .sh | 1 |
| .sql | 8 |
| .txt | 1 |
| .xlsx | 109 |
| .yaml | 3 |
| .zip | 11 |

## Failures

None.

## Known limits

- DOCX/PPTX images are counted but not extracted; originals remain in the source folders.
- XLSX cells use cached values; formulas without a cached value are blank.
- Merged XLSX cells are filled from the top-left value for readability.
- HTML conversion keeps text and tables; styling, scripts and navigation are removed.
- The 26 MB Project Hub is indexed as reference only and is not converted.
- PDF files are skipped where an HTML or SQL equivalent exists.

## Spot checks

Open one converted file per format and compare headings, table row counts and Thai text with the original:

- DOCX: `requirement/legacy/05-technical-architecture/...target-architecture...md`
- XLSX: `requirement/legacy/06-data/...logical-data-model...md`
- PPTX: `requirement/legacy/02-business-architecture-and-process/...business-architecture...md`
- HTML: `requirement/legacy/02-business-architecture-and-process/...business-rules-and-routing-logic...md`
- ZIP: `requirement/legacy/04-user-stories/...story-files..._extracted/`
