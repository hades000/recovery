from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
old = '''xr = [
    ["Item", "Value"],'''
new = '''xr = [
    ["SCB Collections and Recovery. Henka Group, 22 November 2026.", "(C) Siam Commercial Bank and Henka Pte Ltd"],
    ["Item", "Value"],'''
assert old in t
t = t.replace(old, new)
p.write_text(t, encoding="utf-8")
print("ok")
