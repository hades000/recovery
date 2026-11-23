import json, sys
sys.path.insert(0, "22 Microservice Realignment/compat")
from common import SERVICES
for s in SERVICES:
    print(s["code"], s["service"], s["schema"], s["wave"])
