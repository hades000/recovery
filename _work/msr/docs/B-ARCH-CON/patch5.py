from pathlib import Path

p = Path("_work/msr/docs/B-ARCH-CON/build.py")
t = p.read_text(encoding="utf-8")
t = t.replace('["Nickname", "Every owner in this workbook comes from the Microservice Ownership Map v1"]',
              '["Ownership", "Every owner in this workbook comes from the Microservice Ownership Map v1"]')
p.write_text(t, encoding="utf-8")
print("ok")
