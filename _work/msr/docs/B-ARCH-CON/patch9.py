from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
a = '"; ".join(sorted({LABEL.get(c, c) for p_, c, ty, i, src in PAIRS if ty == "Temporal" and i.endswith(name)}))'
b = '(lambda cs: "; ".join(sorted(cs)) if cs else "None named in the sources")({LABEL.get(c, c) for p_, c, ty, i, src in PAIRS if ty == "Temporal" and i.endswith(name)})'
assert a in t
p.write_text(t.replace(a, b), encoding="utf-8")
print("ok")
