from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
a = 'return 0 if code in EDGE + ("ALL", "PLT") else SVC[code]["wave"]'
b = 'return 0 if code in EDGE + ("ALL", "PLT", "NOTSPEC") else SVC[code]["wave"]'
assert a in t
p.write_text(t.replace(a, b), encoding="utf-8")
print("ok")
