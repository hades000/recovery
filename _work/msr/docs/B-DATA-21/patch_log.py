from pathlib import Path
p = Path("_work/msr/editlog/B-DATA-21.md")
s = p.read_text(encoding="utf-8")
s = s.replace("Types: 5 Missing, 3 Conflict.", "Types: 6 Missing, 3 Conflict.")
s = s.replace("Confidence High on 4 and Medium on 5.", "Confidence High on 5 and Medium on 4.")
s = s.replace("with 15 story IDs from the plan", "with 26 story IDs from the plan")
p.write_text(s, encoding="utf-8")
print("ok")
