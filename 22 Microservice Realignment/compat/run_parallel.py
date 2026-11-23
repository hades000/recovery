"""Keep the measured maximum number of DeepSeek sessions busy. Weighted budget, retry, quota guard."""
import argparse, datetime, json, re, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, WORK, opencode_exe, runtime, read_json, write_json

RATE = re.compile(r"(?i)\b429\b|rate.?limit|too many requests|overloaded|\b5\d\d\b|quota|ECONNRESET|timed? ?out")
QUOTA = re.compile(r"(?i)usage limit reached|weekly usage limit|monthly usage limit|quota exceeded|insufficient quota")
T3_CACHE = Path.home() / ".t3" / "caches" / "opencode.json"

class Budget:
    def __init__(self, cap, floor=4):
        self.cap = self.max = cap; self.floor = min(floor, cap); self.used = 0
        self.cv = threading.Condition(); self.last_err = time.time()
    def acquire(self, w):
        with self.cv:
            while self.used > 0 and self.used + w > self.cap:
                self.cv.wait(2)
            self.used += w
    def release(self, w):
        with self.cv:
            self.used -= w; self.cv.notify_all()
    def lower(self):
        with self.cv:
            self.cap = max(self.floor, self.cap - 2); self.last_err = time.time()
    def maybe_raise(self):
        with self.cv:
            if time.time() - self.last_err > 600 and self.cap < self.max:
                self.cap += 1; self.last_err = time.time(); self.cv.notify_all()

def _ts(s):
    return datetime.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp()

def quota_state(path=T3_CACHE):
    """('ok',0) | ('wait', seconds) | ('stop', resetsAt). Advisory: ignored when the cache is missing or >2 h old."""
    d = read_json(path, None)
    if not d or "usageLimits" not in d:
        return ("ok", 0)
    ul = d["usageLimits"]
    try:
        if time.time() - _ts(ul.get("checkedAt", "1970-01-01T00:00:00")) > 7200:
            return ("ok", 0)
    except Exception:
        return ("ok", 0)
    for w in ul.get("windows", []):
        if w.get("usedPercent", 0) >= 90:
            if w.get("kind") == "session":
                return ("wait", max(60, _ts(w["resetsAt"]) - time.time()))
            if w.get("usedPercent", 0) >= 95:
                return ("stop", w.get("resetsAt"))
    return ("ok", 0)

def oc_runner(item, fanout):
    msg = f"Execute WP {item['wp']}: follow the attached WP file exactly. fanout: {fanout if item.get('fanout') else 0}"
    cmd = [opencode_exe(), "run", "--auto", "--model", runtime(), "--agent", item["agent"],
           "--title", item["wp"], "--file", str(ROOT / item["file"]), msg]
    log = WORK / "logs" / f"{item['wp']}.log"
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=5400)
        out = (p.stdout or "") + "\n" + (p.stderr or "")
        rc = p.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = f"timeout {e}", 124
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"\n===== {time.strftime('%H:%M:%S')} rc={rc}\n{out[-20000:]}")
    return rc, out

def run_queue(items, cap, fanout, runner=oc_runner, base=ROOT, status_path=WORK / "status.json",
              backoff=(30, 120, 300), guard=quota_state):
    status = read_json(status_path, {}) or {}
    lock = threading.Lock()
    budget = Budget(cap)
    stop = threading.Event()

    def save():
        with lock:
            write_json(status_path, status)

    def done(item):
        return all((Path(base) / e).exists() for e in item.get("expect", []))

    def work(item):
        wp = item["wp"]
        w = min(cap, 1 + fanout) if item.get("fanout") else 1
        requeued = False
        while not stop.is_set():
            g = guard()
            if g[0] == "stop":
                stop.set(); status[wp] = {"state": "PAUSED_QUOTA", "resets": g[1]}; save(); return
            if g[0] == "wait":
                time.sleep(min(g[1], 900)); continue
            budget.acquire(w)
            try:
                status[wp] = {"state": "RUNNING", "tries": status.get(wp, {}).get("tries", 0) + 1}; save()
                rc, out = runner(item, fanout)
            finally:
                budget.release(w)
            if QUOTA.search(out or ""):
                stop.set(); status[wp] = {"state": "PAUSED_QUOTA", "resets": "provider usage window"}; save(); return
            if rc == 0 and done(item):
                status[wp] = {"state": "DONE", "tries": status[wp]["tries"]}; save(); budget.maybe_raise(); return
            tries = status[wp]["tries"]
            if RATE.search(out or "") and tries <= len(backoff):
                budget.lower(); time.sleep(backoff[tries - 1]); continue
            if not requeued:
                requeued = True; continue
            status[wp] = {"state": "FAILED", "tries": tries, "rc": rc}; save(); return

    todo = [i for i in items if status.get(i["wp"], {}).get("state") != "DONE"]
    with ThreadPoolExecutor(max_workers=max(1, cap)) as ex:
        list(ex.map(work, todo))
    return status

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queue", required=True, help="B, C, D or a queue file path")
    ap.add_argument("--max", type=int, default=None, help="override measured budget (never lower it to be safe)")
    ap.add_argument("--fanout", type=int, default=None)
    ap.add_argument("--only", default=None, help="comma list of WP ids")
    ap.add_argument("--status", default=None, help="status file to use (default _work/msr/status.json)")
    a = ap.parse_args()
    cap_info = read_json(WORK / "plan" / "capacity.json", {}) or {}
    cap = a.max or cap_info.get("budget", 19)
    hard = cap_info.get("hard_cap")
    if hard:
        cap = min(cap, int(hard))
    fan = a.fanout if a.fanout is not None else cap_info.get("fanout", 5)
    q = Path(a.queue) if a.queue.endswith(".json") else WORK / "wp" / f"queue-{a.queue}.json"
    items = json.loads(q.read_text(encoding="utf-8"))
    if a.only:
        keep = set(a.only.split(",")); items = [i for i in items if i["wp"] in keep]
    print(f"RUN queue={q.name} items={len(items)} budget={cap} fanout={fan}")
    st = run_queue(items, cap, fan, status_path=Path(a.status) if a.status else WORK / "status.json")
    counts = {}
    for i in items:
        s = st.get(i["wp"], {}).get("state", "PENDING"); counts[s] = counts.get(s, 0) + 1
    print("RESULT", json.dumps(counts))
    sys.exit(3 if counts.get("PAUSED_QUOTA") else 0)

if __name__ == "__main__":
    main()
