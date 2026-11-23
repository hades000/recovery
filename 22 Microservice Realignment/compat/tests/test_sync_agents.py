import tempfile, unittest
from pathlib import Path
import yaml
import sync_opencode_agents as s

AGENT = '''---
description: "Use when: writing a spec"
name: "Technical Specifier"
tools: [read, edit, search, execute, agent]
agents: ["Compliance Reviewer"]
---
You run in the Claude Code runtime.
Use TodoWrite for tasks and the Agent tool to spawn reviewers.
'''
REV = '''---
description: "Use when: reviewing"
name: "Compliance Reviewer"
tools: [read]
---
Review it.
'''
CMD = '''---
description: AISDLC agent - BRD Builder
---
Convert .docx/.pptx with `textutil -convert txt` and continue.
Input: $ARGUMENTS
'''

class TestSync(unittest.TestCase):
    def test_generate(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            (d / "agents").mkdir(); (d / "cmds").mkdir()
            (d / "agents/specify.agent.md").write_text(AGENT, encoding="utf-8")
            (d / "agents/reviewer.agent.md").write_text(REV, encoding="utf-8")
            (d / "agents/agent-frontmatter-reference.md").write_text("ignore", encoding="utf-8")
            (d / "cmds/brd-builder.md").write_text(CMD, encoding="utf-8")
            out = s.generate(d / "agents", d / "cmds", d / "root", "agent")
            names = sorted(p.name for p in (d / "root/.opencode/agent").iterdir())
            self.assertEqual(names, ["aisdlc-brd-builder.md", "aisdlc-msr-worker.md",
                                     "aisdlc-reviewer.md", "aisdlc-specify.md"])
            txt = (d / "root/.opencode/agent/aisdlc-specify.md").read_text(encoding="utf-8")
            fm = yaml.safe_load(txt.split("---")[1])
            self.assertEqual(fm["mode"], "all")
            self.assertFalse(fm["tools"]["webfetch"])
            self.assertNotIn("Claude Code runtime", txt)
            self.assertIn("todowrite", txt)
            self.assertIn("aisdlc-reviewer", txt)
            self.assertIn("No human approval is required", txt)
            brd = (d / "root/.opencode/agent/aisdlc-brd-builder.md").read_text(encoding="utf-8")
            self.assertNotIn("textutil", brd)
            self.assertIn("convert_sources.py", brd)
            self.assertTrue((d / "root/.opencode/command/aisdlc-brd-builder.md").exists())
            self.assertIn("$ARGUMENTS", (d / "root/.opencode/command/aisdlc-brd-builder.md").read_text(encoding="utf-8"))
            self.assertEqual(len(out), 4)

if __name__ == "__main__":
    unittest.main()
