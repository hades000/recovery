# Document writer brief (Phase 3)

Read `RUN_BRIEF.md` (same folder) first – its hard rules apply in full.

You own ONLY the documents named in your task. For each one:
1. Find the highest version in SET (check .md/.xlsx/.docx/.yaml/.sql/.csv and versioned folders; ignore `_work`). Copy it to STAGE at the same relative path with the next version number (`v8` → `v9`; a versioned folder is copied whole and renamed). If the staged next version already exists and your task says you own the document, continue editing it.
2. Inputs, in this order of authority:
   a. `SET\24 P1 Developer Readiness v1\Recovery Workbench P1 Decision Register v1.md` (+ .csv) – the FINAL ruling paragraph of each RD-P1 decision is binding; apply every final ruling that names one of your documents or the artefacts it holds (paths, schemas, events, workflows, tables, fields, messages, tests, roles, owners).
   b. Your findings packet `SET\_work\p1-ready\packets\<your packet> findings.csv` – the review findings that point at your documents (story_key, gap_no, conflicts_with, suggested_fix, verify_verdict). Fix every one that is real and that a decision or the sources settle. If a finding conflicts with a final ruling, the ruling wins. If it needs a value no source or ruling gives, do not invent it: log `NEW-GAP` with the text and owner role.
   c. `SET\24 P1 Developer Readiness v1\New gaps and assumptions from decisions v1.csv` – where a value is pending, write "Pending: … (temp id)" in the document.
3. Make targeted edits only (add rows, change cells, add or change paragraphs, add operations/schemas). Keep all unchanged content identical. Add one row to the document's version/change table: "vN+1 · 27 November 2026 · D-RCV-60 P1 developer readiness (RD-P1 register) · targeted edits".
   - .docx: edit with python-docx at paragraph/table-cell level; never rebuild the document. If the docx has an .md twin, edit both.
   - .xlsx: openpyxl cell edits and appended rows; preserve sheets, styles, widths, other cells. If an .md twin exists, edit both.
   - .yaml: keep valid YAML/OpenAPI 3.1 or AsyncAPI 3; validate with `python -I -c "import yaml,sys;yaml.safe_load(open(sys.argv[1],encoding='utf-8'))" <file>` after editing. If the folder holds a rendered .html of the spec, leave it and log REQUEST "regenerate html".
   - .sql: keep the file executable in order; add, don't reorder.
4. Log every edit in `SET\_work\p1-ready\editlog\<your agent name>.csv` (format in RUN_BRIEF). Log a `REQUEST` row for any change another document needs (target document in `file`).
5. Finish with a self-check: re-open each staged file, confirm each logged `after` text is present, that the version row is there, and (xlsx/yaml) that the file opens/parses. Reply with: documents staged (old → new version), number of edits per document, findings fixed vs left (with reason), NEW-GAP rows, REQUEST rows.

Time budget: about 60 minutes. Work document by document; write the edit log as you go so partial work survives.
