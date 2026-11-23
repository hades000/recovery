import tempfile, unittest
from pathlib import Path
import copy_workspace as cw

class TestCopy(unittest.TestCase):
    def test_copy_latest(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "src/.github/agents").mkdir(parents=True)
            (d / "src/.github/agents/planner.agent.md").write_text("a")
            (d / "prds").mkdir()
            for n in ["p3-case-fsd-v3.md", "p3-case-fsd-v4.md", "nfr.md"]:
                (d / "prds" / n).write_text(n)
            cw.copy_tree(d / "src/.github", d / "ws/.github")
            cw.copy_latest_md(d / "prds", d / "ws/docs/prds")
            self.assertTrue((d / "ws/.github/agents/planner.agent.md").exists())
            names = sorted(p.name for p in (d / "ws/docs/prds").iterdir())
            self.assertEqual(names, ["nfr.md", "p3-case-fsd-v4.md"])

if __name__ == "__main__":
    unittest.main()
