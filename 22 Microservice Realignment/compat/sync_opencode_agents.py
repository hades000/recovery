"""Generate OpenCode agents/commands from the AI-SDLC (HVE Core) agent sources. Never edits folder 18."""
import argparse, re, sys
from pathlib import Path
import yaml
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WS, MODEL, COMPAT, decision

DEC = decision()

TOOLS = {"read": True, "grep": True, "glob": True, "list": True, "edit": True, "write": True,
         "bash": True, "task": True, "todowrite": True, "todoread": True, "webfetch": False}
HEADER = ("You are the `{name}` OpenCode agent (model DeepSeek v4.1 Flash, run from T3 Code). "
          "Delegate only through the `task` tool, and only to: {subs}. Use `todowrite` for task lists. "
          "The AI-SDLC workspace root is `22 Microservice Realignment/aisdlc/`; every relative path in "
          "this prompt (.github/contexts, .github/rules, docs/brds, docs/prds, requirement/legacy, "
          "output/<RUN_ID>) resolves there.")
OVERLAY = """## Realignment overlay (D-RCV-53) — overrides anything above
- This run is the D-RCV-53 realignment. No human approval is required to proceed.
- Treat any missing approval or status (for example "BRD status must be Approved") as an assumption:
  append {"id":"ASM-<WP>-<n>","text":...,"why":...,"read":...,"confidence":"Medium"} to
  _work/msr/assumptions/<WP>.jsonl and continue with status Draft.
- Never ask the user a question. Never call Jira, Confluence, GitLab, Figma or the web.
- Never start a later lifecycle stage on your own. Stop only for a safety, credential or production-data issue.
- Convert .docx/.pptx/.xlsx only with: python -I "22 Microservice Realignment/compat/convert_sources.py" <file> <outdir>
- Follow ROOT AGENTS.md rules 1-14. Edit log tool line: T3 Code / OpenCode / DeepSeek v4.1 Flash."""
WORKER_BODY = """You are the realignment worker. Follow the WP file you are given exactly, top to bottom.
Read every file under "Read only" before writing. Write only the files under "Write only".
Use the template, split rules, DP table, dependency classes and Day-1 rule in
"22 Microservice Realignment/Recovery Workbench Microservice Story Template and Rules v1.md".
When the WP says "fanout: F", give each legacy story to its own task subagent (aisdlc-msr-worker),
up to F in parallel in a single message, each with the WP path and its one legacy key; then merge nothing —
each subagent writes its own files. Finish with the quick check in AGENTS.md rule 12."""
FIXES = [
    (re.compile(r"(?im)^.*claude code runtime.*$\n?"), ""),
    (re.compile(r"\bTodoWrite\b"), "todowrite"),
    (re.compile(r"\bthe Agent tool\b"), "the task tool"),
    (re.compile(r"\bAgent tool\b"), "task tool"),
    (re.compile(r"`?textutil -convert txt`?"), '`python -I "22 Microservice Realignment/compat/convert_sources.py" <file> requirement/legacy/_converted`'),
    (re.compile(r"(?i)human-started stage[^.\n]*\.?"), "Started by the realignment coordinator."),
]

def split_fm(text):
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.S)
    if not m:
        return {}, text
    return (yaml.safe_load(m.group(1)) or {}), m.group(2)

def fix(body):
    for rx, rep in FIXES:
        body = rx.sub(rep, body)
    return body

def render(name, desc, body, subs):
    fm = {"description": str(desc or name)[:900], "mode": "all", "model": MODEL, "temperature": 0.1, "tools": TOOLS}
    head = HEADER.format(name=name, subs=", ".join(subs) if subs else "aisdlc-msr-worker")
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True) + "---\n" + head + "\n\n" + fix(body).strip() + "\n\n" + OVERLAY.replace("D-RCV-53", DEC) + "\n"

def generate(src_agents, src_cmds, out_root, layout="agent"):
    adir = Path(out_root) / ".opencode" / layout
    cdir = Path(out_root) / ".opencode" / ("command" if layout == "agent" else "commands")
    adir.mkdir(parents=True, exist_ok=True); cdir.mkdir(parents=True, exist_ok=True)
    srcs = sorted(p for p in Path(src_agents).glob("*.agent.md"))
    parsed = {p: split_fm(p.read_text(encoding="utf-8")) for p in srcs}
    by_display = {str(fm.get("name", "")): "aisdlc-" + p.name[:-len(".agent.md")] for p, (fm, _) in parsed.items()}
    written = []
    for p, (fm, body) in parsed.items():
        name = "aisdlc-" + p.name[:-len(".agent.md")]
        subs = [by_display.get(a, "aisdlc-" + re.sub(r"[^a-z0-9]+", "-", a.lower()).strip("-")) for a in (fm.get("agents") or [])]
        (adir / f"{name}.md").write_text(render(name, fm.get("description"), body, subs), encoding="utf-8")
        written.append(name)
    for p in sorted(Path(src_cmds).glob("*.md")):
        fm, body = split_fm(p.read_text(encoding="utf-8"))
        name = "aisdlc-" + p.stem
        (adir / f"{name}.md").write_text(render(name, fm.get("description"), body, []), encoding="utf-8")
        cmd_fm = yaml.safe_dump({"description": str(fm.get("description", name)), "agent": name}, sort_keys=False)
        (cdir / f"{name}.md").write_text("---\n" + cmd_fm + "---\n" + fix(body).strip() + "\n", encoding="utf-8")
        written.append(name)
    (adir / "aisdlc-msr-worker.md").write_text(
        render("aisdlc-msr-worker", "Realignment worker: executes one WP file exactly.", WORKER_BODY, []), encoding="utf-8")
    written.append("aisdlc-msr-worker")
    return written

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--layout", choices=["agent", "agents"], default="agent")
    a = ap.parse_args()
    names = generate(WS / ".github" / "agents", WS / ".claude-commands", ROOT, a.layout)
    print(f"GENERATED {len(names)} agents into .opencode/{a.layout}: " + ", ".join(sorted(names)))

if __name__ == "__main__":
    main()
