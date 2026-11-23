from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
a = 'EDGE = ("BFF", "ACE-CMN", "ACE-DB", "EXT", "PARTNER", "REQUESTER", "NOTSPEC")'
b = 'EDGE = ("BFF", "ACE-CMN", "ACE-DB", "EXT", "PARTNER", "REQUESTER")'
assert a in t
p.write_text(t.replace(a, b), encoding="utf-8")
print("ok")
