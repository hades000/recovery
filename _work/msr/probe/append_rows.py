"""Append candidate gap/assumption rows for one WP to its jsonl, under a lock.

Run as: python -I "_work/msr/probe/append_rows.py" <WP> <gaps|assumptions> <rows-file.jsonl>
Rows file is a scratch file of one JSON object per line (typically _work/msr/probe/rows-<key>.jsonl).
Every row is validated as JSON before anything is written, then all rows are appended in one write.
"""
import json, os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
wp, kind, src = sys.argv[1], sys.argv[2], Path(sys.argv[3])
if kind not in ("gaps", "assumptions"):
    raise SystemExit("kind must be gaps or assumptions")
target = ROOT / "_work" / "msr" / kind / f"{wp}.jsonl"
target.parent.mkdir(parents=True, exist_ok=True)
rows = [l.strip() for l in src.read_text(encoding="utf-8").splitlines() if l.strip()]
for r in rows:
    json.loads(r)
if not target.exists():
    target.write_text("", encoding="utf-8")
lock = target.with_suffix(target.suffix + ".lock")
deadline = time.time() + 120
while True:
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.close(fd)
        break
    except FileExistsError:
        if time.time() > deadline:
            raise SystemExit(f"lock timeout: {lock}")
        time.sleep(0.2)
try:
    with open(target, "a", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(r + "\n")
finally:
    try:
        os.unlink(str(lock))
    except OSError:
        pass
print(f"appended {len(rows)} row(s) to {target}")
