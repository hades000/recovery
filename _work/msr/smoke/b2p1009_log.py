import pathlib
p = pathlib.Path("_work/msr/editlog/B2-P1-009.md")
t = p.read_text(encoding="utf-8")
print("sect", t.count("\u00a7"), "emdash", t.count("\u2014"), "mojibake", t.count("\u00c2"), t.count("\u00e2"))
print("---- tail ----")
print(t[-1200:])
