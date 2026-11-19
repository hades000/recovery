# Conversion report

Run: 2026-11-04

Source files and zip entries: **411**

## By conversion status

| Status | Count |
|---|---:|
| converted | 133 |
| copied | 117 |
| extracted | 159 |
| skipped | 2 |

## By format

| Format | Count |
|---|---:|
| .docx | 47 |
| .html | 11 |
| .md | 270 |
| .pdf | 1 |
| .pptx | 22 |
| .sql | 1 |
| .xlsx | 54 |
| .yaml | 1 |
| .zip | 4 |

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
