"""Prove generated agents load and run under OpenCode with DeepSeek. Retries and falls back; never stops."""
import json, re, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, MODEL, VARIANT, opencode_exe, write_json, append_jsonl

EXE = opencode_exe()

def oc(args, timeout=900):
    p = subprocess.run([EXE] + args, cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout)
    return p.returncode, p.stdout, p.stderr

def agent_ids():
    rc, out, err = oc(["debug", "agents"], 120)
    i = out.find("[")
    try:
        return {a["id"] for a in json.loads(out[i:])}
    except Exception:
        return set()

def asm(text, why):
    append_jsonl(WORK / "assumptions" / "A5.jsonl", {"id": f"ASM-A5-{int(time.time()*1000)%100000}",
                 "text": text, "why": why, "read": "opencode debug agents / opencode run", "confidence": "High"})

def main():
    res = {"layout": None, "model": None, "worker": False, "brd": False, "mcp_calls": None}
    logdir = Path.home() / ".local" / "share" / "opencode" / "log"
    start_sizes = {p.name: p.stat().st_size for p in logdir.glob("*.log")} if logdir.exists() else {}
    ids = agent_ids()
    if "aisdlc-msr-worker" in ids:
        res["layout"] = "agent"
    else:
        subprocess.run([sys.executable, "-I", str(Path(__file__).parent / "sync_opencode_agents.py"), "--layout", "agents"], check=False)
        ids = agent_ids()
        res["layout"] = "agents" if "aisdlc-msr-worker" in ids else "none"
        asm(f"OpenCode agent folder is .opencode/{res['layout']}", "singular folder not loaded")
    res["agents_loaded"] = sorted(i for i in ids if i.startswith("aisdlc-"))
    target = WORK / "smoke" / "worker.txt"
    for model in [f"{MODEL}#{VARIANT}", MODEL]:
        for attempt in range(3):
            if target.exists():
                target.unlink()
            agent_args = ["--agent", "aisdlc-msr-worker"] if res["layout"] != "none" else []
            rc, out, err = oc(["run", "--auto", "--model", model] + agent_args +
                              ["Write the text OK to the file _work/msr/smoke/worker.txt and nothing else."])
            if target.exists() and "OK" in target.read_text(encoding="utf-8", errors="replace"):
                res["worker"], res["model"] = True, model
                break
            time.sleep(10 * (attempt + 1))
        if res["worker"]:
            break
    if res["model"] != f"{MODEL}#{VARIANT}":
        asm(f"Model string used: {res['model'] or MODEL}", "variant #max rejected or worker failed")
    model = res["model"] or MODEL
    write_json(WORK / "plan" / "runtime.json", {"model": model, "layout": res["layout"]})
    brief = WORK / "smoke" / "brd-brief.md"
    brief.write_text("BRD name: Smoke_Test\nFocus: one paragraph only about recovery case ownership.\n"
                     "Write to 22 Microservice Realignment/aisdlc/docs/brds/_smoke/Smoke_Test.md\n"
                     "Sections 1 and 2 only. Status Draft.\nThis is a smoke test of the agent.\n", encoding="utf-8")
    out_md = ROOT / "22 Microservice Realignment" / "aisdlc" / "docs" / "brds" / "_smoke" / "Smoke_Test.md"
    for attempt in range(3):
        oc(["run", "--auto", "--model", model, "--agent", "aisdlc-brd-builder", "--file", str(brief),
            "Follow the attached brief exactly."])
        if out_md.exists() and out_md.read_text(encoding="utf-8", errors="replace").lstrip().startswith("---"):
            res["brd"] = True
            break
    txt = ""
    for p in logdir.glob("*.log") if logdir.exists() else []:
        try:
            with open(p, "rb") as f:
                f.seek(start_sizes.get(p.name, 0))
                txt += f.read().decode("utf-8", errors="replace")
        except OSError:
            continue
    res["mcp_calls"] = len(re.findall(r"(?i)(?:tool|call)[^\n]*(?:jira_|atlassian|gitlab)", txt))
    write_json(WORK / "smoke" / "result.json", res)
    print("SMOKE", json.dumps(res))

if __name__ == "__main__":
    main()
