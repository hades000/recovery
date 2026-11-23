import json, sqlite3, statistics, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, opencode_exe, runtime, write_json

EXE = opencode_exe()
LEVELS = [4, 8, 12, 16, 20, 24, 28, 32]

def one(i, model):
    t = time.time()
    try:
        p = subprocess.run([EXE, "run", "--model", model, "--title", f"msr-probe-{i}", "Reply with exactly: OK"],
                           cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=600)
        ok = p.returncode == 0 and "OK" in p.stdout
        err = (p.stderr or "")[-300:]
    except subprocess.TimeoutExpired:
        ok, err = False, "timeout"
    return {"ok": ok, "secs": round(time.time() - t, 1), "err": err}

def ramp(model):
    results, baseline, best = {}, None, 0
    for n in LEVELS:
        with ThreadPoolExecutor(max_workers=n) as ex:
            r = list(ex.map(lambda i: one(i, model), range(n)))
        med = statistics.median(x["secs"] for x in r)
        fails = [x for x in r if not x["ok"]]
        results[n] = {"median_s": med, "fails": len(fails), "errors": [f["err"] for f in fails][:3]}
        baseline = baseline or med
        if fails or med > 3 * baseline:
            break
        best = n
        time.sleep(20)
    return best, results

def db_overlap(since):
    p = (Path.home() / ".local/share/opencode/opencode.db").as_posix()
    c = sqlite3.connect(f"file:{p}?mode=ro", uri=True)
    rows = c.execute("select id,parent_id,time_created,time_updated from session_v2 where parent_id is not null and time_created>=?",
                     (int(since * 1000),)).fetchall()
    by = {}
    for _id, par, tc, tu in rows:
        by.setdefault(par, []).append((tc, tu))
    best = 0
    for spans in by.values():
        ev = sorted([(a, 1) for a, _ in spans] + [(b, -1) for _, b in spans])
        cur = 0
        for _, d in ev:
            cur += d; best = max(best, cur)
    return best

def fanout(model, k):
    since = time.time()
    prompt = (f"Use the task tool to launch exactly {k} subagents of type general IN ONE MESSAGE (parallel). "
              f"Subagent i must reply 'done i'. Do nothing else. Then reply ALL DONE.")
    subprocess.run([EXE, "run", "--auto", "--model", model, "--title", f"msr-fanout-{k}", prompt],
                   cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=1800)
    time.sleep(5)
    try:
        return db_overlap(since)
    except Exception:
        return -1

def main():
    model = runtime()
    best, results = ramp(model)
    fan = {k: fanout(model, k) for k in (12, 20)}
    sess = max([v for v in fan.values() if v > 0] or [10])
    cap = {
        "measured_at": time.strftime("%Y-%m-%d %H:%M"),
        "model": model,
        "process_levels": results,
        "process_max": best or 4,
        "session_subagent_max": sess,
        "budget": best if best else 19,   # largest level that passed; history (19) only if the ramp failed at 4
        "fanout": min(5, sess),
        "historical": {"per_session_max": 10, "global_max": 19, "rate_limit_lines": 0},
    }
    write_json(WORK / "plan" / "capacity.json", cap)
    print("CAPACITY", json.dumps({k: cap[k] for k in ("process_max", "session_subagent_max", "budget", "fanout")}))

if __name__ == "__main__":
    main()
