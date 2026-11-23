import unittest
import split_plan as sp
from common import ID_RE

def row(key, module, deps=(), be="EP01", group="E1"):
    return {"key": key, "title": f"Title {key}", "group": group, "master": "m.md", "module": module, "release": "30 November 2026",
            "business_epic": be, "deps": list(deps), "reqs": [], "acs": [], "tcs": [], "story_file": None}

class TestSplit(unittest.TestCase):
    def setUp(self):
        chain = [row(f"RWB-E1-1{i:02d}", "P3", deps=[f"RWB-E1-1{i-1:02d}"] if i else []) for i in range(7)]
        self.index = chain + [
            row("RWB-E1-014", "P9"), row("RWB-E1-042", "P3"), row("RWB-TE-001", None, group="TE", be="EP01-TE"),
            row("RWB-E1-016", "P1"), row("RWB-E1-200", "P3", deps=["RWB-E1-016", "RWB-E1-014", "RWB-TE-007"]),
            row("RWB-E1-027", "P7"), row("RWB-E1-071", "P3"), row("NF-06", None, group="NF", be="NF")]
        self.blocks = {r["key"]: "plain text" for r in self.index}
        self.blocks["RWB-E1-016"] = "Provides GET /api/recovery/v1/accounts and EV-01. Writes account_ext (W)."
        self.blocks["RWB-E1-200"] = ("Uses DecisionLogWriter.\nScenario: AC1 Create\n Given x\n Then y\n"
                                     "Scenario: AC2 Gate\n Given the ALS batch is COMPLETED\n Then z\n")
        self.own = {"tables": {"account_ext": {"owner": "P1"}}}
        self.plan = sp.build(self.index, self.blocks, self.own)
        self.s = {x["id"]: x for x in self.plan["slices"]}

    def test_ids_valid_and_unique(self):
        ids = [x["id"] for x in self.plan["slices"]]
        self.assertEqual(len(ids), len(set(ids)))
        for i in ids:
            self.assertRegex(i, ID_RE)

    def test_retire_and_preserve(self):
        self.assertEqual(self.plan["legacy"]["RWB-E1-014"]["disposition"], sp.RETIRED)
        self.assertIn("RWB-P3-E1042-APP", self.s); self.assertTrue(self.s["RWB-P3-E1042-APP"]["preserved"])
        self.assertIn("RWB-P3-E1042-CON", self.s); self.assertIn("RWB-PLT-E1042-CON", self.s)
        self.assertIn("RWB-PLT-TE001-APP", self.s); self.assertIn("RWB-PLT-TE001-APP-2", self.s)
        self.assertIn("RWB-PLT-NF06-DB", self.s)

    def test_dependency_classes(self):
        a = self.s["RWB-P3-E1200-APP"]
        self.assertIn("RWB-P1-E1016-CON", a["C"])            # other service with CON -> C
        self.assertIn("RWB-PLT-E1071-CON", a["H"])           # TE-007 redirect
        self.assertIn("RWB-PLT-E1027-CON", a["H"])           # DP-03
        self.assertNotIn("RWB-E1-014", str(a))               # dropped
        itg = self.s["RWB-ITG-E1200-ITG"]
        self.assertIn("AC2", itg["acs"]); self.assertIn("AC1", a["acs"])
        self.assertIn("RWB-P1-E1016-APP", itg["I"])
        for x in self.plan["slices"]:
            for h in x["H"]:
                t = self.s.get(h)
                self.assertTrue(t is not None, h)
                self.assertTrue(t["wt"] == "CON" or t["scope"] == x["scope"], (x["id"], h))
                self.assertFalse(t["scope"] == "PLT" and t["wt"] != "CON" and x["scope"] != "PLT", (x["id"], h))
            if x["scope"] != "ITG":
                self.assertEqual(x["I"], [])

    def test_lane_depth_and_day1(self):
        import networkx as nx
        g = nx.DiGraph()
        for x in self.plan["slices"]:
            if x["wt"] != "CON":
                g.add_node(x["id"])
                for h in x["H"]:
                    if self.s[h]["wt"] != "CON":
                        g.add_edge(h, x["id"])
        for comp in nx.weakly_connected_components(g):
            self.assertLessEqual(len(nx.dag_longest_path(g.subgraph(comp))), 4)
        for x in self.plan["slices"]:
            if x["wt"] == "CON":
                self.assertEqual(x["ready"], "Day 1"); self.assertEqual(x["H"], [])
        teams = {x["owner"] for x in self.plan["slices"] if x["ready"] == "Day 1"}
        self.assertTrue({"TechX", "ACE", "INFRA", "DEVOPS", "QA"} <= teams, teams)
        self.assertEqual(len([x for x in self.plan["slices"] if x["wt"] == "CON" and x["scope"] in sp.SVC_CODES]) >= 19, True)
