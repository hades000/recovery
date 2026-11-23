import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import WORK, read_json, write_json

st = read_json(WORK / "status.json", {}) or {}
for wp in sys.argv[1].split(","):
    st.pop(wp.strip(), None)
    print("REQUEUED", wp.strip())
write_json(WORK / "status.json", st)
