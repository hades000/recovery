import sys
from pathlib import Path
sys.path.insert(0, str(Path("22 Microservice Realignment/checks").resolve()))
sys.path.insert(0, str(Path("22 Microservice Realignment/compat").resolve()))
import run_all as R

files = [
    R.ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 APP Temporal security, codec server and admin audit v1.md",
    R.ROOT / "04 User stories/Recovery Workbench Service Story Files v1/RWB-PLT-WF Temporal workflow platform/RWB PLT E2038 CON Temporal security, codec server and admin audit - contract v1.md",
    R.WORK / "fragments/RWB-PLT-E2038-APP.json",
    R.WORK / "fragments/RWB-PLT-E2038-CON.json",
]
for name in ("C06", "C07", "C10", "C11", "C15", "C16", "C17", "C20"):
    fn = R.ALL[name]
    try:
        res = fn(files)
    except Exception as e:
        res = ("CRASH", [f"{type(e).__name__}: {e}"])
    print(name, res[0], res[1][:8])
