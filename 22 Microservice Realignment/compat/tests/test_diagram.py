import json, tempfile, unittest
from pathlib import Path
import build_arch_diagram as bd

S = [{"id": "RWB-P3-E1018-CON", "title": "Case contract", "wt": "CON", "epic": "RWB-SVC-P3", "lane": "CG-W1", "wave": 1, "scope": "P3", "H": [], "C": [], "I": []},
     {"id": "RWB-P3-E1018-APP", "title": "Case app", "wt": "APP", "epic": "RWB-SVC-P3", "lane": "L-P3-A", "wave": 1, "scope": "P3", "H": ["RWB-P3-E1018-CON"], "C": ["RWB-P1-E1016-CON"], "I": []},
     {"id": "RWB-P1-E1016-CON", "title": "Source contract", "wt": "CON", "epic": "RWB-SVC-P1", "lane": "CG-W1", "wave": 1, "scope": "P1", "H": [], "C": [], "I": []}]
F = {"RWB-P3-E1018-APP": {"events_consumed": ["rwb.source-data.AccountLoaded.v1"], "ops_consumed": [], "workflows": []}}

class TestDiagram(unittest.TestCase):
    def test_build(self):
        doc = bd.build(S, F, title="T")
        els = doc["elements"]; ids = {e["id"] for e in els}
        boxes = [e for e in els if e["type"] == "rectangle" and e.get("customData", {}).get("story")]
        self.assertEqual(len(boxes), 3)
        for e in els:
            if e["type"] == "arrow":
                self.assertIn(e["startBinding"]["elementId"], ids); self.assertIn(e["endBinding"]["elementId"], ids)
        kinds = {e.get("customData", {}).get("call") for e in els if e["type"] == "arrow"}
        self.assertTrue({"H", "REST", "Kafka"} <= kinds, kinds)
        with tempfile.TemporaryDirectory() as d:
            bd.save(doc, Path(d) / "x")
            self.assertEqual(json.loads((Path(d) / "x.excalidraw").read_text(encoding="utf-8"))["type"], "excalidraw")
            self.assertTrue((Path(d) / "x.svg").read_text(encoding="utf-8").startswith("<svg"))
