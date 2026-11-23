# WP B-REQ-PRD-P6 — PRD P6 rwb-comms v1 (PRD Builder)
Tool rules: AGENTS.md (root) rules 1-14. Agent: aisdlc-prd-builder. fanout: 0
Read only:
- 03 Requirements and specifications BRDs (latest versions) and their converted text in _work/msr/extract/
- FSD v6 file for module P6 in _work/msr/extract/
- Arch v5 slides for rwb-comms
- converted text under _work/msr/extract/ (or convert with: python -I "22 Microservice Realignment/compat/convert_sources.py" <file> _work/msr/extract/B-REQ-PRD-P6)
- 22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md (§R1, §R3, §R5, §R8, §R9)
- _work/msr/plan/ownership.json and 22 Microservice Realignment/Recovery Workbench Microservice Ownership Map v1.xlsx
- 22 Microservice Realignment/Recovery Workbench Architecture v5 Text Extract v1.md
- 22 Microservice Realignment/Recovery Workbench Temporal and Drools Design Text Extract v1.md
- _work/msr/plan/split_plan.json ("stats" and "legacy" only)
- _work/msr/plan/ids.json
Write only:
- 03 Requirements and specifications/PRD/Recovery Workbench PRD P6 rwb-comms v1.md
- _work/msr/docs/B-REQ-PRD-P6/ (scratch)
- _work/msr/gaps/B-REQ-PRD-P6.jsonl
- _work/msr/assumptions/B-REQ-PRD-P6.jsonl
- _work/msr/editlog/B-REQ-PRD-P6.md
Do: produce the next version of each output. Keep every section, ID, number and date of the source; release dates get "(tentative)".
Change only what the realignment needs: PRD for rwb-comms: CAP-/FR-/NFR-/AC- IDs, FR-P6-nnn mapped to the FSD REQ IDs, release slicing by wave, no design beyond confirmed v5 constraints, status Draft, empty approval table. Use the Ownership Map for every owner. New decisions use the IDs in _work/msr/plan/ids.json.
First two lines are the header in Template and Rules §R8.1. Add a change-log row "<version>, 22 November 2026, D-RCV-60 microservice realignment, T3 Code / OpenCode / DeepSeek v4.1 Flash".
How to write each format (never edit the source):
- .md: write the new file directly.
- .docx: write the full text to _work/msr/docs/B-REQ-PRD-P6/<name>.md, then: python -I "22 Microservice Realignment/compat/office_write.py" md-docx "<that md>" "<output .docx>" --template "<source .docx>"
- .xlsx: python -I "22 Microservice Realignment/compat/office_write.py" copy "<source>" "<output>" ; then add sheets/rows with: python -I "22 Microservice Realignment/compat/office_write.py" xlsx-append "<output>" "<sheet>" "<rows.json>"
- .pptx: python -I "22 Microservice Realignment/compat/office_write.py" copy "<source>" "<output>" ; then python -I "22 Microservice Realignment/compat/office_write.py" pptx-append "<output>" "<slides.md>"
- folder family: python -I "22 Microservice Realignment/compat/office_write.py" copy "<source folder>" "<output folder>" ; then for each file that changes, write its next version inside the new folder.
Never invent values: placeholders and jsonl rows as Template and Rules §R9.
Finish: run python -I "22 Microservice Realignment/checks/run_all.py" --wp B-REQ-PRD-P6 --quick ; fix every failure ; write _work/msr/editlog/B-REQ-PRD-P6.md (files written, tool line T3 Code / OpenCode / DeepSeek v4.1 Flash, counts of CG and ASM rows) ; reply with the list of files written.
