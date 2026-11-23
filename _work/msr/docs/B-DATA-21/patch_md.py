from pathlib import Path
p = Path("_work/msr/docs/B-DATA-21/Recovery Workbench Data Migration Approach v4.md")
s = p.read_text(encoding="utf-8")
subs = [
 ("## 9.2 The nineteen schemas\n",
  "## 9.2 The nineteen schemas\n\nVersion 3 names one recovery schema and no target table or schema of any single table, so the mapping below is new (CG-B-DATA-21-1; ASM-B-DATA-21-1).\n"),
 ("| RWB-DM-005 | Migrate contact and promises | rwb_source_data (P1), with the case key in rwb_case (P3) | RWB-P1-DM005-APP; RWB-ITG-DM005-ITG | 30 November 2026 (tentative) | interaction, contact_point_ext |",
  "| RWB-DM-005 | Migrate contact and promises | rwb_source_data (P1), with the case key in rwb_case (P3) | RWB-P1-DM005-APP; RWB-ITG-DM005-ITG | 30 November 2026 (tentative) | interaction, contact_point_ext (CG-B-DATA-21-9; ASM-B-DATA-21-9) |"),
 ("| document, document_field, document_custody, and the originals in Blob WORM |",
  "| document, document_field, document_custody, and the originals in Blob WORM (CG-B-DATA-21-8; ASM-B-DATA-21-8) |"),
 ("what changes is the schema each table lands in, and that the landing is the owner's step and not a write by rwb-source-data.",
  "what changes is the schema each table lands in, and that the landing is the owner's step and not a write by rwb-source-data; the identity that runs the load is set in section 9.1 (CG-B-DATA-21-3; ASM-B-DATA-21-3)."),
 ("RWB-P1-DM014-APP extracts and validates the set and maps each table to its owner;",
  "Version 3 loads this reference data once; the split below is new (CG-B-DATA-21-4; ASM-B-DATA-21-4). RWB-P1-DM014-APP extracts and validates the set and maps each table to its owner;"),
]
for a, b in subs:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")
print("patched")
