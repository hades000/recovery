import json, tempfile, threading, time, unittest
from pathlib import Path
import run_parallel as rp

class TestBudget(unittest.TestCase):
    def test_weights_never_exceed_cap(self):
        b = rp.Budget(6); peak = [0]; lock = threading.Lock()
        def job(w):
            b.acquire(w)
            with lock:
                peak[0] = max(peak[0], b.used)
            time.sleep(0.05); b.release(w)
        ts = [threading.Thread(target=job, args=(w,)) for w in [6, 1, 1, 3, 2, 6, 1]]
        [t.start() for t in ts]; [t.join() for t in ts]
        self.assertLessEqual(peak[0], 6); self.assertEqual(b.used, 0)

    def test_lower_and_raise(self):
        b = rp.Budget(10); b.lower(); self.assertEqual(b.cap, 8)
        for _ in range(10): b.lower()
        self.assertEqual(b.cap, 4)
        b.last_err -= 700; b.maybe_raise(); self.assertEqual(b.cap, 5)

class TestGuard(unittest.TestCase):
    def test_guard(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "c.json"
            now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
            p.write_text(json.dumps({"usageLimits": {"checkedAt": now, "windows": [
                {"kind": "session", "usedPercent": 95, "resetsAt": "2099-01-01T00:00:00.000Z"}]}}))
            self.assertEqual(rp.quota_state(p)[0], "wait")
            p.write_text(json.dumps({"usageLimits": {"checkedAt": now, "windows": [
                {"kind": "weekly", "usedPercent": 97, "resetsAt": "2099-01-01T00:00:00.000Z"}]}}))
            self.assertEqual(rp.quota_state(p)[0], "stop")
            self.assertEqual(rp.quota_state(Path(d) / "missing.json")[0], "ok")

class TestRun(unittest.TestCase):
    def test_retry_then_done(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d); calls = {}
            def runner(item, fan):
                calls[item["wp"]] = calls.get(item["wp"], 0) + 1
                if item["wp"] == "W2" and calls["W2"] == 1:
                    return 1, "HTTP 429 Too Many Requests"
                for e in item["expect"]:
                    (d / e).write_text("ok")
                return 0, "done"
            items = [{"wp": f"W{i}", "agent": "a", "file": "x", "fanout": i % 2 == 0, "expect": [f"o{i}.txt"]} for i in range(6)]
            st = rp.run_queue(items, cap=4, fanout=3, runner=runner, base=d, status_path=d / "s.json",
                              backoff=[0, 0, 0], guard=lambda: ("ok", 0))
            self.assertTrue(all(v["state"] == "DONE" for v in st.values()), st)
            self.assertEqual(calls["W2"], 2)
