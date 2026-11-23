import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
wp = (ROOT / "_work/msr/wp/B-ITG-W2-01.md").read_text(encoding="utf-8")
for line in wp.splitlines():
    if line.strip().startswith('{"id"'):
        s = json.loads(line.strip())
        p = ROOT / s["file"]
        t = p.read_text(encoding="utf-8")
        sec = t.split("### 13.", 1)[1].split("### 14.", 1)[0]
        dps = re.findall(r"^\| (DP-?\d\d) ", sec, re.M)
        want = [d[:2] + "-" + d[2:] for d in s["patterns"]]
        print(s["id"], len(dps), "OK" if dps == want else "MISMATCH " + str(dps))
        # section 12 tables
        s12 = t.split("### 12.", 1)[1].split("### 13.", 1)[0]
        print("   12.x:", re.findall(r"^#### (12\.\d)", s12, re.M))
        # I row values
        me = re.search(r"\| Integration dependencies \| (.+?) \|", t)
        print("   I row:", me.group(1) if me else "MISSING")
