from pathlib import Path
p = Path(r"05 Technical architecture/Recovery Workbench Service Catalog v1.md")
t = p.read_bytes()
print(t[:80])
print("emdash ok:", "—".encode("utf-8") in t)
print("replacement chars:", t.count(b"\xef\xbf\xbd"))
