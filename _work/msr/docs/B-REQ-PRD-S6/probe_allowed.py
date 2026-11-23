import sys
from pathlib import Path
sys.path.insert(0, str(Path("22 Microservice Realignment/checks").resolve()))
import importlib.util
spec = importlib.util.spec_from_file_location("run_all", "22 Microservice Realignment/checks/run_all.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
for w in m._wp_writes("B-REQ-PRD-S6"):
    print(repr(w))
