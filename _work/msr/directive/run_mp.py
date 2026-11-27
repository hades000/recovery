"""Parallel Haiku 5.5 model pass for the directive run (D-RCV-60).

One fresh headless Claude Code session per chunk (claude -p, model claude-haiku-5-5, no tools, no MCP,
auto-compact window 100k), so no session ever reaches the compaction limit. Stories run in parallel; the
chunks of one story run in order. mpw.py shows the chunk and applies the returned edits (all or none).
A failed apply is retried with the error (3 tries); then the chunk is recorded as Not applied.

Usage: python -I run_mp.py --jobs 12 [--stories S1,S2] [--limit N]
Stop: create mp/STOP (running chunks finish, nothing new starts). Resume: run again (done chunks are skipped).
"""
import argparse, json, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
MP = D / "mp"
RULES = D / "haiku_rules.md"
CLAUDE = shutil.which("claude")
CWD = Path(r"C:\Users\SAHILM~1\AppData\Local\Temp\claude\664128f151027658\92cee45a-713f-47f7-8fb3-fd02931135e3\scratchpad")
lock = threading.Lock()
stats = {"chunks": 0, "ok": 0, "failed": 0, "cost": 0.0, "calls": 0}


def mpw(*args):
    r = subprocess.run([sys.executable, "-I", str(D / "mpw.py"), *args], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, (r.stdout + r.stderr).strip()


def haiku(prompt):
    r = subprocess.run([CLAUDE, "-p", "--model", "claude-haiku-5-5", "--tools", "", "--strict-mcp-config",
                        "--autocompact", "100k", "--no-session-persistence", "--output-format", "json",
                        "--system-prompt-file", str(RULES)], input=prompt, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", cwd=str(CWD), timeout=600)
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, 0.0, f"no JSON from claude (rc {r.returncode}): {(r.stdout + r.stderr)[-300:]}"
    cost = float(j.get("total_cost_usd") or 0)
    if j.get("is_error"):
        return None, cost, f"claude error: {str(j.get('result'))[:300]}"
    return j.get("result") or "", cost, ""


def parse(text):
    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b < a:
        raise ValueError("no JSON object in the reply")
    return json.loads(text[a:b + 1])


def chunk_ids(story):
    show = MP / "chunks" / story
    return [c.stem for c in sorted(show.glob("c*.md")) if not (MP / "disp" / story / f"{c.stem}.jsonl").exists()]


def do_chunk(story, cid):
    rc, shown = mpw("show", story)
    if f"chunk {cid} " not in shown.split("\n", 1)[0]:
        return f"show gave another chunk: {shown[:80]}"
    log = {"story": story, "chunk": cid, "attempts": []}
    prompt, err = shown, ""
    for attempt in range(1, 4):
        if err:
            prompt = (shown + "\n\n=== YOUR PREVIOUS REPLY FAILED ===\n" + err +
                      "\nReply again with the whole corrected JSON object.")
        text, cost, cerr = haiku(prompt)
        with lock:
            stats["cost"] += cost
            stats["calls"] += 1
        if cerr:
            err = cerr
            log["attempts"].append({"error": cerr})
            time.sleep(5 * attempt)
            continue
        try:
            j = parse(text)
        except (ValueError, json.JSONDecodeError) as e:
            err = f"Your reply was not one valid JSON object: {e}"
            log["attempts"].append({"error": err})
            continue
        (MP / "tmp" / f"{story}-{cid}.json").write_text(json.dumps(j, ensure_ascii=False, indent=1), encoding="utf-8")
        rc, out = mpw("apply", story, cid)
        log["attempts"].append({"apply": out[:400]})
        if rc == 0:
            (MP / "log" / f"{story}-{cid}.json").write_text(json.dumps(log, ensure_ascii=False), encoding="utf-8")
            return ""
        err = out
    # three failures: record every item Not applied
    items = [l for l in (MP / "chunks" / story / f"{cid}.md").read_text(encoding="utf-8").splitlines()
             if l.startswith("## ") and "; ruling R-" in l]
    disp = []
    for l in items:
        iid = l.split(". ", 1)[1].split(" (", 1)[0]
        rid = l.split("; ruling ", 1)[1].split(";", 1)[0]
        disp.append({"ruling": rid, "item": iid, "status": "Not applied", "section": "", "target": "", "change": "",
                     "note": f"FAILED after 3 tries: {err[:150]}"})
    (MP / "tmp" / f"{story}-{cid}.json").write_text(json.dumps({"edits": [], "disposition": disp}, ensure_ascii=False),
                                                     encoding="utf-8")
    mpw("apply", story, cid)
    (MP / "log" / f"{story}-{cid}.json").write_text(json.dumps(log, ensure_ascii=False), encoding="utf-8")
    return f"FAILED: {err[:200]}"


def do_story(story):
    try:
        _do_story(story)
    except Exception as e:  # one story's error never stops the pool
        with lock, (MP / "run.log").open("a", encoding="utf-8") as fh:
            fh.write(f"{time.strftime('%H:%M:%S')} {story} STORY ERROR {e!r}\n")


def _do_story(story):
    for cid in chunk_ids(story):
        if (MP / "STOP").exists():
            return
        e = do_chunk(story, cid)
        with lock:
            stats["chunks"] += 1
            stats["ok" if not e else "failed"] += 1
            line = (f"{time.strftime('%H:%M:%S')} {story} {cid} {'OK' if not e else e} | done {stats['chunks']} "
                    f"ok {stats['ok']} failed {stats['failed']} calls {stats['calls']} cost ${stats['cost']:.2f}")
            print(line, flush=True)
            with (MP / "run.log").open("a", encoding="utf-8") as fh:
                fh.write(line + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--stories")
    ap.add_argument("--limit", type=int)
    a = ap.parse_args()
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    (MP / "tmp").mkdir(exist_ok=True)
    (MP / "log").mkdir(exist_ok=True)
    stories = a.stories.split(",") if a.stories else [s for s, _ in json.loads((MP / "stories.json").read_text())]
    stories = [s for s in stories if chunk_ids(s)]
    # biggest first, so the long stories do not finish last
    stories.sort(key=lambda s: -len(chunk_ids(s)))
    if a.limit:
        stories = stories[:a.limit]
    print(f"{len(stories)} stories with work left, {sum(len(chunk_ids(s)) for s in stories)} chunks, jobs {a.jobs}",
          flush=True)
    with ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(do_story, stories))
    print(f"END | {json.dumps(stats)}", flush=True)


if __name__ == "__main__":
    main()
