"""Model escalation for the directive model pass (D-RCV-60): Haiku 5.5 -> Sonnet 5.5 (medium) -> Opus 5.5.

Stages (run in this order, each after the one before has finished):
  failed     chunks Haiku failed 3 times: Sonnet (3 tries), then Opus (3 tries). No tools.
  notapplied items Haiku marked Not applied: Sonnet with read-only Read/Grep/Glob on the project; items Sonnet
             still cannot resolve, or whose apply fails 3 times, go to Opus (same tools).
  audit      per story, Sonnet audits Haiku's diff and fixes what is wrong; then Opus reviews the diff and
             Sonnet's findings and reworks anything flagged or missed.

Every session is fresh and short (claude -p, --autocompact 100k). Edits go through the same all-or-none,
exact-match rules as mpw.py. Every unit writes mp/esc/<stage>/<story>/<unit>.json (prompt size, model,
attempts, result, disposition). Later stages supersede earlier dispositions per ruling (see merged_dispositions).

Usage: python -I esc.py <stage> [--jobs N] [--stories A,B] [--limit N] [--dry-run]
Stop: create mp/STOP_ESC.
"""
import argparse, difflib, json, re, shutil, subprocess, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
MP = D / "mp"
ROOT = D.parents[2]
ESC = MP / "esc"
sys.path.insert(0, str(D))
CLAUDE = shutil.which("claude")
SCRATCH = Path(r"C:\Users\SAHILM~1\AppData\Local\Temp\claude\664128f151027658\92cee45a-713f-47f7-8fb3-fd02931135e3\scratchpad")
RULES = (D / "haiku_rules.md").read_text(encoding="utf-8")
MAXL = 140
STATUSES = ("Resolved", "Cross-document", "Not applied")
SONNET = ("claude-sonnet-5-5", "medium")
OPUS = ("claude-opus-5-5", "medium")
lock = threading.Lock()
DEADLINE = float("inf")  # set by --minutes: no new story after it; running ones finish
OPUS_NOW = False  # False: Opus steps are queued in mp/esc/opus_queue.jsonl for the Opus pass
stats = {"units": 0, "ok": 0, "escalated": 0, "failed": 0, "calls": 0, "cost": 0.0}

READ_RULES = """
Source access (read-only)
- You may use Read, Grep and Glob on the project folder to check the cited source documents. Never write.
- Keep every read small: Grep with a precise pattern and head_limit 20, or output_mode files_with_matches first;
  Read with offset and limit of at most 120 lines. Never Read a whole register, workbook export or story file.
  The registers in '23 Document Gaps' are 6 MB: only Grep them for an exact ID.
- Spreadsheets (.xlsx) cannot be read. Look for a .md export of the same document instead.
- Resolve the item only with a value you actually found; say in `note` where you found it (file and section).
  If the value is truly not in the sources, keep `Not applied` and say where you looked.
"""

AUDIT_RULES = """
You are auditing edits another model made to one user story under the programme directive (decision D-RCV-60).
You get the items, the dispositions it wrote, and the unified diff from the story before to the story now.

Check every changed line and every disposition:
- wrong: the edit is incorrect, contradicts the story or the item, breaks a table (cell count, missing '|'),
  breaks AC/TC numbering, duplicates an existing criterion, or changes text no item asked about;
- invented: a number, threshold, code, ID, role code, field name or payload that is not in the item or story
  text (it must then read 'Not specified in the source documents (<Item ID>)');
- incomplete: the item is marked Resolved but the story does not resolve it;
- wrong status: Cross-document or Not applied where a story edit was possible, or Resolved where the change
  belongs to another document;
- forbidden: dates, release dates, the Tool line, decision IDs, the change log or the Status row changed; a
  person's name; a Claude, Anthropic or other tool trailer.

Fix what you find. Reply with ONE JSON object and nothing else:
{"findings": [{"ruling": "R-..", "kind": "wrong|invented|incomplete|wrong status|forbidden|ok", "issue": "under 200 characters"}],
 "edits": [{"old": "<exact text as it is NOW>", "new": "<replacement>"}],
 "disposition": [{"ruling": "R-..", "item": "..", "status": "Resolved|Cross-document|Not applied", "section": "", "target": "", "change": "", "note": ".."}]}
- `old` must be copied exactly from the story as it is NOW: lines of the diff starting with '+' or ' ' (drop that
  one-character prefix), never from '-' lines. It must occur exactly once in the story.
- `disposition` holds only rulings whose row you change; leave it empty if all are right.
- `findings` lists only problems found (kind other than ok); an empty list means the story passes.
"""


# ------------------------------------------------------------------ helpers
def sec_ranges(lines):
    heads = [(i, l) for i, l in enumerate(lines) if re.match(r"#{2,4} ", l)]
    out = {}
    for k, (i, l) in enumerate(heads):
        m = re.match(r"#{2,4} (\d+(?:\.\d+)?)\.? ", l)
        end = heads[k + 1][0] if k + 1 < len(heads) else len(lines)
        if m:
            out[m.group(1)] = (i, end)
    return out


def story_text(story):
    return (MP / "out" / f"{story}.md").read_text(encoding="utf-8")


def context(story, items_text):
    """The parts of the current story the items touch (same rules as mpw.py show); the whole story when FULL."""
    if FULL:
        return ("=" * 20 + " CURRENT STORY TEXT (whole story; copy 'old' text from here exactly) " + "=" * 20 + "\n"
                + story_text(story))
    lines = story_text(story).split("\n")
    rng = sec_ranges(lines)
    want = set()
    for s in re.findall(r"sections: ([^)]*)\)", items_text):
        for x in s.split(", "):
            x = x.strip()
            if re.fullmatch(r"\d+(?:\.\d+)?", x):
                want.add(x)
                if x not in rng and x.split(".")[0] in rng:
                    want.add(x.split(".")[0])
    out, shown = ["=" * 20 + " CURRENT STORY TEXT (only these parts; copy 'old' text from here exactly) " + "=" * 20], []
    first = min((a for a, _ in rng.values()), default=len(lines))
    out += [f"--- header, lines 1-{min(first, 32)} ---", "\n".join(lines[:min(first, 32)])]
    for key in sorted(want, key=lambda x: [int(p) for p in x.split(".")]):
        if key not in rng:
            continue
        a, b = rng[key]
        if any(a >= x and b <= y for x, y in shown):
            continue
        shown.append((a, b))
        seg = lines[a:b]
        out += [f"--- section {key}, lines {a + 1}-{b} ---", "\n".join(seg[:MAXL])]
        if len(seg) > MAXL:
            out.append(f"[... {len(seg) - MAXL} more lines in this section not shown]")
    quotes = re.findall(r"'([^']{12,})'", items_text) + re.findall(r"`([^`]{8,})`", items_text)
    hits = set()
    for q in quotes:
        k = q.split("...")[0].strip()[:40]
        for i, l in enumerate(lines):
            if k and k in l and not any(a <= i < b for a, b in shown):
                hits.add(i)
    for m in re.findall(r"line (\d+)", items_text):
        i = int(m) - 1
        if 0 <= i < len(lines) and not any(a <= i < b for a, b in shown):
            hits.add(i)
    if hits:
        out.append("--- other lines the items point at ---")
        out += [f"L{i + 1}: {lines[i]}" for i in sorted(hits)[:40]]
    out += ["--- all section headings ---", " | ".join(f"{k}@L{a + 1}" for k, (a, _) in rng.items())]
    return "\n".join(out)


def apply_edits(story, edits):
    """All or none, exact match once, table rows closed. Returns '' or the error."""
    f = MP / "out" / f"{story}.md"
    t = f.read_text(encoding="utf-8")
    for n, e in enumerate(edits, 1):
        old, new = e.get("old", ""), e.get("new", "")
        if not old:
            return f"EDIT {n} FAILED: empty 'old'"
        for ln in new.split("\n"):
            s = ln.strip()
            if s.startswith("|") and not s.endswith("|"):
                return f"EDIT {n} FAILED: table row does not end with '|': {s[-80:]!r}"
        k = t.count(old)
        if k != 1:
            return (f"EDIT {n} FAILED: 'old' occurs {k} times (must be exactly 1). Copy a longer exact piece of "
                    f"the current text. old starts: {old[:80]!r}")
        t = t.replace(old, new, 1)
    with lock:
        f.write_text(t, encoding="utf-8")
    return ""


def check_disp(disp, need):
    got = {d.get("ruling") for d in disp}
    if need - got:
        return f"DISPOSITION INCOMPLETE: no row for {sorted(need - got)}"
    bad = [d for d in disp if d.get("status") not in STATUSES]
    return f"BAD STATUS in {bad[0]}" if bad else ""


DS = "opencode-go/deepseek-v4.1-flash"
OC_CONFIG = D / "opencode-notools.json"
OPENCODE = shutil.which("opencode")
FULL = False  # True for DeepSeek lanes: whole story, full diff, no section or size cuts


def call_opencode(model, system, prompt, timeout=1500):
    """DeepSeek through OpenCode. No tools (config), a fresh empty folder per call, prompt on stdin.
    A reply that used any tool is rejected, and the folder must still be empty afterwards."""
    import tempfile, os
    sb = Path(tempfile.mkdtemp(prefix="ds-", dir=str(SCRATCH / "ocsb")))
    env = dict(os.environ, OPENCODE_CONFIG=str(OC_CONFIG))
    try:
        # --standalone: a private server that honours OPENCODE_CONFIG (all tools off). Without it, `run` attaches to
        # the background service, which runs in the project folder with the project config and every tool on.
        r = subprocess.run([OPENCODE, "run", "--standalone", "-m", model, "--format", "json"], input=system + "\n\n" + prompt,
                           capture_output=True, text=True, encoding="utf-8", errors="replace", cwd=str(sb),
                           timeout=timeout, env=env)
    except subprocess.TimeoutExpired:
        return None, 0.0, "timeout (a session that tries a tool hangs and times out)"
    finally:
        left = [p.name for p in sb.iterdir()] if sb.exists() else []
        shutil.rmtree(sb, ignore_errors=True)
    if left:
        return None, 0.0, f"SAFETY: the session left files in its folder: {left[:5]}"
    texts, used, tok, err = [], [], {"in": 0, "out": 0}, ""
    for l in r.stdout.splitlines():
        try:
            j = json.loads(l)
        except json.JSONDecodeError:
            continue
        p = j.get("part", {})
        if j.get("type") == "tool_use":
            used.append(p.get("tool"))
        elif j.get("type") == "text":
            texts.append(p.get("text", ""))
        elif j.get("type") == "step_finish":
            t = p.get("tokens", {})
            tok["in"] += t.get("input", 0)
            tok["out"] += t.get("output", 0)
        elif j.get("type") == "error":
            err = str(j.get("error"))[:300]
    with lock:
        stats["calls"] += 1
        stats["tokens_in"] = stats.get("tokens_in", 0) + tok["in"]
        stats["tokens_out"] = stats.get("tokens_out", 0) + tok["out"]
    if used:
        with (MP / "SAFETY-tool-use.log").open("a", encoding="utf-8") as fh:  # must stay empty; checked after each run
            fh.write(f"{time.strftime('%H:%M:%S')} tools {used}\n")
        return None, 0.0, f"SAFETY: the session tried tools {used}; reply rejected"
    if err:
        return None, 0.0, f"opencode error: {err}"
    if not texts:
        return None, 0.0, f"no text from opencode (rc {r.returncode}): {r.stderr[-300:]}"
    return "\n".join(texts), 0.0, ""


OC_API = "https://opencode.ai/inference/go/v1/chat/completions"
OC_USAGE = "https://opencode.ai/inference/go/v1/usage"
UA = "rwb-directive-review/1.0"
_KEY = None


def _api_key():
    """The OpenCode Go key, read from OpenCode's auth file on first use; kept in memory only, never logged."""
    global _KEY
    if _KEY is None:
        import os
        kf = os.environ.get("OPENCODE_GO_KEY_FILE")  # a key file delivered by the secret card
        if kf:
            _KEY = Path(kf).read_text(encoding="utf-8").strip()
        else:
            p = Path(os.path.expanduser("~/.local/share/opencode/auth.json"))
            _KEY = json.loads(p.read_text(encoding="utf-8"))["opencode-go"]["key"]
    return _KEY


def call_api(model, system, prompt, timeout=1800, session=None):
    """DeepSeek through the OpenCode Go chat-completions API: text in, text out. No tools parameter is sent, so
    the model cannot call any tool; every edit still goes through apply_edits (all or none, exact match)."""
    import urllib.request, urllib.error
    body = json.dumps({"model": model.split("/", 1)[1], "stream": False,
                       "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}]}
                      ).encode("utf-8")
    import uuid
    sid = session or f"rwb-{uuid.uuid4().hex}"  # one stable ID per conversation (its retries reuse it)
    err = ""
    for k in range(5):
        req = urllib.request.Request(OC_API, data=body, method="POST", headers={
            "Content-Type": "application/json", "Authorization": f"Bearer {_api_key()}",
            "User-Agent": UA, "x-opencode-session": sid})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                j = json.loads(r.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            err = f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:200]}"
            if e.code in (408, 409, 425, 429, 500, 502, 503, 504):
                time.sleep(15 * (k + 1))
                continue
            return None, 0.0, err
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            err = f"network: {e}"
            time.sleep(15 * (k + 1))
    else:
        return None, 0.0, err
    msg = (j.get("choices") or [{}])[0].get("message") or {}
    u = j.get("usage") or {}
    with lock:
        stats["calls"] += 1
        stats["tokens_in"] = stats.get("tokens_in", 0) + int(u.get("prompt_tokens") or 0)
        stats["tokens_out"] = stats.get("tokens_out", 0) + int(u.get("completion_tokens") or 0)
    if msg.get("tool_calls"):
        return None, 0.0, "SAFETY: the reply asked for a tool call; rejected"
    text = msg.get("content") or ""
    if not text:
        return None, 0.0, f"empty reply (finish {(j.get('choices') or [{}])[0].get('finish_reason')})"
    return text, 0.0, ""


def go_usage():
    """OpenCode Go usage meters (rolling 5 h, weekly, monthly); used to stop before a limit."""
    import urllib.request
    req = urllib.request.Request(OC_USAGE, headers={"Authorization": f"Bearer {_api_key()}", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


_USAGE = {"t": 0, "ok": True, "why": ""}


def usage_ok():
    """False when an OpenCode Go meter is rate-limited or at 95% or more (checked at most every 5 minutes)."""
    if not FULL:
        return True
    if time.time() - _USAGE["t"] > 300:
        try:
            u = go_usage()["usage"]
            bad = [f"{k} {v.get('percent')}% {v.get('status')}" for k, v in u.items()
                   if v.get("status") != "ok" or (v.get("percent") or 0) >= 95]
            _USAGE.update(t=time.time(), ok=not bad, why="; ".join(bad))
            with (MP / "go-usage.log").open("a", encoding="utf-8") as fh:
                fh.write(f"{time.strftime('%H:%M:%S')} {json.dumps(u)}\n")
        except Exception as e:
            _USAGE.update(t=time.time(), why=f"usage check failed: {e}")
    return _USAGE["ok"]


def call(model, effort, system, prompt, tools=False, timeout=900):
    if model.startswith("opencode-go/"):
        return call_api(model, system, prompt)
    args = [CLAUDE, "-p", "--model", model, "--effort", effort, "--strict-mcp-config", "--autocompact", "100k",
            "--no-session-persistence", "--output-format", "json", "--append-system-prompt" if tools else
            "--system-prompt", system]
    if tools:
        if tools == "docview":  # read-only document views: Bash is allowed for docview.py only (others are denied)
            args += ["--tools", "Read,Grep,Glob,Bash", "--allowedTools", "Read", "Grep", "Glob",
                     f'Bash(python -I "{D / "docview.py"}" *)', "--max-turns", "40"]
        else:
            args += ["--tools", "Read,Grep,Glob", "--allowedTools", "Read", "Grep", "Glob", "--max-turns", "30"]
        cwd = ROOT
    else:
        args += ["--tools", ""]
        cwd = SCRATCH
    try:
        r = subprocess.run(args, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           cwd=str(cwd), timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, 0.0, "timeout"
    try:
        j = json.loads(r.stdout)
    except json.JSONDecodeError:
        return None, 0.0, f"no JSON from claude (rc {r.returncode}): {(r.stdout + r.stderr)[-300:]}"
    cost = float(j.get("total_cost_usd") or 0)
    with lock:
        stats["calls"] += 1
        stats["cost"] += cost
    if j.get("is_error") or j.get("subtype", "success") != "success":
        return None, cost, f"claude error ({j.get('subtype')}): {str(j.get('result'))[:300]}"
    return j.get("result") or "", cost, ""


def parse(text):
    a, b = text.find("{"), text.rfind("}")
    if a < 0 or b < a:
        raise ValueError("no JSON object in the reply")
    return json.loads(text[a:b + 1])


def item_blocks(story):
    """ruling -> the item's block of text from the original chunk files."""
    out = {}
    for c in sorted((MP / "chunks" / story).glob("c*.md")):
        cur = None
        for l in c.read_text(encoding="utf-8").split("\n"):
            m = re.match(r"## \d+\. (\S+) \(.*; ruling (R-\d+);", l)
            if m:
                cur = m.group(2)
                out[cur] = [l]
            elif cur and l.startswith("- "):
                out[cur].append(l)
            elif not l.strip():
                cur = None
    return {k: "\n".join(v) for k, v in out.items()}


def chunk_disp(story):
    """ruling -> (chunk id, disposition row) from the Haiku pass."""
    out = {}
    for p in sorted((MP / "disp" / story).glob("c*.jsonl")):
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.strip():
                d = json.loads(l)
                out[d["ruling"]] = (p.stem, d)
    return out


def merged_dispositions(story):
    """Final disposition per ruling: Haiku, then failed, notapplied, audit-sonnet, audit-opus (later wins)."""
    final = {r: dict(d, stage="haiku") for r, (_, d) in chunk_disp(story).items()}
    for stage in ("failed", "notapplied", "audit"):
        for p in sorted((ESC / stage / story).glob("*.json")):
            j = json.loads(p.read_text(encoding="utf-8"))
            for step in j.get("steps", []):
                if step.get("applied"):
                    for d in step.get("disposition", []):
                        if d.get("ruling") in final:
                            final[d["ruling"]] = dict(final[d["ruling"]], **d, stage=f"{stage}-{step['model']}")
    op = ESC / "opus" / f"{story}.json"
    if op.exists():
        for step in json.loads(op.read_text(encoding="utf-8")).get("steps", []):
            if step.get("applied"):
                for d in step.get("disposition", []):
                    if d.get("ruling") in final:
                        final[d["ruling"]] = dict(final[d["ruling"]], **d, stage=f"opus-{step.get('stage', '')}")
    return final


def record(stage, story, uid, rec):
    p = ESC / stage / story / f"{uid}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")


def queue_opus(stage, story, uid, reason, rulings=None):
    with lock, (ESC / "opus_queue.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"stage": stage, "story": story, "unit": uid, "reason": reason,
                             "rulings": sorted(r for r in (rulings or []) if r)}, ensure_ascii=False) + "\n")


def done(stage, story, uid):
    return (ESC / stage / story / f"{uid}.json").exists()


# ------------------------------------------------------------------ one try-loop on one model
def attempt_loop(model, effort, system, base_prompt, story, need, tools, tries=3):
    """Ask the model, apply, retry with the error. Returns a step record."""
    step = {"model": model, "effort": effort, "tries": [], "applied": False, "disposition": []}
    err = ""
    for k in range(1, tries + 1):
        prompt = base_prompt if not err else (base_prompt + "\n\n=== YOUR PREVIOUS REPLY FAILED ===\n" + err +
                                              "\nReply again with the whole corrected JSON object.")
        text, cost, cerr = call(model, effort, system, prompt, tools=tools)
        if cerr:
            err = cerr
            step["tries"].append({"error": cerr})
            time.sleep(5 * k)
            continue
        try:
            j = parse(text)
        except (ValueError, json.JSONDecodeError) as e:
            err = f"Your reply was not one valid JSON object: {e}"
            step["tries"].append({"error": err})
            continue
        disp = j.get("disposition", [])
        e = check_disp(disp, need) if need else ""
        if not e:
            e = apply_edits(story, j.get("edits", []))
        step["tries"].append({"error": e} if e else {"ok": True, "edits": len(j.get("edits", []))})
        if not e:
            step.update(applied=True, disposition=disp, edits=j.get("edits", []), findings=j.get("findings", []))
            return step
        err = e
    step["error"] = err
    return step


# ------------------------------------------------------------------ stages
def units_failed(story):
    out = []
    for cid, d in {(c, None) for c, d in chunk_disp(story).values()
                   if str(d.get("note", "")).startswith("FAILED after 3 tries")}:
        out.append((cid, cid))
    return sorted(out)


def run_failed(story, cid):
    items = (MP / "chunks" / story / f"{cid}.md").read_text(encoding="utf-8")
    need = {d["ruling"] for c, d in chunk_disp(story).values() if c == cid}
    rec = {"stage": "failed", "story": story, "unit": cid, "rulings": sorted(need), "steps": []}
    for model, effort in ((SONNET, OPUS) if OPUS_NOW else (SONNET,)):
        prompt = items + "\n" + context(story, items)
        step = attempt_loop(model, effort, RULES, prompt, story, need, tools=False)
        rec["steps"].append(step)
        if step["applied"]:
            break
    if not rec["steps"][-1]["applied"] and not OPUS_NOW:
        queue_opus("failed", story, cid, "Sonnet failed 3 tries: " + str(rec["steps"][-1].get("error", ""))[:200], need)
    record("failed", story, cid, rec)
    return rec["steps"][-1]["applied"], len(rec["steps"]) > 1


def units_notapplied(story):
    na = [(r, d) for r, (c, d) in chunk_disp(story).items() if d["status"] == "Not applied"
          and not str(d.get("note", "")).startswith("FAILED after 3 tries")]
    # failed-stage results that are still Not applied join this stage too
    for p in sorted((ESC / "failed" / story).glob("*.json")):
        j = json.loads(p.read_text(encoding="utf-8"))
        for st in j["steps"]:
            if st["applied"]:
                na += [(d["ruling"], d) for d in st["disposition"] if d["status"] == "Not applied"]
    na = sorted({r: d for r, d in na}.items())
    return [(f"u{i // 8 + 1:02d}", [r for r, _ in na[i:i + 8]]) for i in range(0, len(na), 8)]


DS_READ_RULES = """
Source excerpts
- You have no tools. The SOURCE EXCERPTS part below holds the lines of the cited source documents that contain
  the IDs and names in the items (found by a script, read-only). Use them to find the value an item needs.
- Resolve an item only with a value you actually see there or in the story; say in `note` which document and
  line or row it came from. If it is not there, keep `Not applied` and say what you looked for.
"""


def source_excerpts(items_text):
    """Deterministic read-only search of the cited sources for the IDs and names in the items."""
    import targets
    if not targets.FILES:
        targets.resolve_files()
    mm = {}
    p = MP / "targets/model_map.json"
    if p.exists():
        mm = json.loads(p.read_text(encoding="utf-8"))
    files = []
    for k in targets.normalise(" ; ".join(re.findall(r"(?:Evidence|Detail|Proposed fix|Title): ([^\n]+)", items_text))):
        f = targets.FILES.get(k) if not k.startswith("OTHER:") else str(mm.get(k[6:], {}).get("file", ""))
        if f and f not in files and (ROOT / f).is_file():
            files.append(f)
    for m in re.findall(r"(Recovery Workbench [A-Z][\w ,-]+? v\d+)(?:\.\w+)?", items_text):
        for hit in list((ROOT).glob(f"[0-9]*/**/{m}.*"))[:1]:
            rel = hit.relative_to(ROOT).as_posix()
            if rel not in files and hit.suffix.lower() in (".md", ".xlsx", ".docx", ".yaml", ".csv"):
                files.append(rel)
    toks = []
    for t in (re.findall(r"`([^`]{4,60})`", items_text) + re.findall(r"\b[A-Z][A-Z0-9]+(?:-[A-Z0-9]+)+\b", items_text)
              + re.findall(r"\b[a-z][a-z0-9]*(?:_[a-z0-9]+)+\b", items_text)
              + re.findall(r"\b[a-z]+(?:\.[a-z_]+)+\b", items_text)):
        if t not in toks and not t.startswith(("RWB-", "CG-ALL", "DOR-", "NEWAC-", "ACR-", "ASM-ALL", "R-0", "R-1",
                                               "R-2", "R-3")):
            toks.append(t)
    out = []
    for f in files[:6]:
        for t in toks[:12]:
            r = subprocess.run([sys.executable, "-I", str(D / "docview.py"), "find", f, t], capture_output=True,
                               text=True, encoding="utf-8", errors="replace")
            body = r.stdout.strip().split("\n")
            if len(body) > 2:
                out.append(f"--- {f} | search '{t}' ---\n" + "\n".join(body[1:]))
    return ("\n\n=== SOURCE EXCERPTS (read-only search of the cited documents) ===\n" + ("\n".join(out) or
            "(no lines of the cited documents contain the item IDs or names)"))


def run_notapplied(story, uid, rulings):
    blocks, cd = item_blocks(story), chunk_disp(story)
    def items_text(rs, prev):
        L = [f"# {story}: items a previous model marked Not applied", ""]
        for r in rs:
            L += [blocks.get(r, f"## {r}"), f"- Previous model's note: {prev.get(r, '')}", ""]
        return "\n".join(L)
    prev = {r: cd[r][1].get("note", "") for r in rulings if r in cd}
    sysp = RULES + (DS_READ_RULES if FULL else READ_RULES)
    src = (lambda t: source_excerpts(t)) if FULL else (lambda t: '')
    rec = {"stage": "notapplied", "story": story, "unit": uid, "rulings": rulings, "steps": []}
    txt = items_text(rulings, prev)
    step = attempt_loop(*SONNET, sysp, txt + "\n" + context(story, txt) + src(txt), story, set(rulings), tools=True)
    rec["steps"].append(step)
    left = set(rulings) if not step["applied"] else {d["ruling"] for d in step["disposition"]
                                                      if d["status"] == "Not applied"}
    if left and not OPUS_NOW:
        queue_opus("notapplied", story, uid, "still Not applied after Sonnet" if step["applied"] else
                   "Sonnet failed 3 tries: " + str(step.get("error", ""))[:200], left)
    elif left:
        if step["applied"]:
            prev.update({d["ruling"]: f"{prev.get(d['ruling'], '')} | Sonnet: {d.get('note', '')}"
                         for d in step["disposition"] if d["ruling"] in left})
        txt = items_text(sorted(left), prev)
        step2 = attempt_loop(*OPUS, sysp, txt + "\n" + context(story, txt) + src(txt), story, left, tools=True)
        rec["steps"].append(step2)
    record("notapplied", story, uid, rec)
    return any(s["applied"] for s in rec["steps"]), len(rec["steps"]) > 1


def diff_text(story):
    meta = json.loads((MP / "chunks" / story / "meta.json").read_text(encoding="utf-8"))
    a = Path(meta["input_file"]).read_text(encoding="utf-8").split("\n")
    b = story_text(story).split("\n")
    return "\n".join(difflib.unified_diff(a, b, "before", "now", n=1, lineterm=""))


def disp_table(story):
    blocks = item_blocks(story)
    fin = merged_dispositions(story)
    L = []
    for r, d in sorted(fin.items()):
        title = next((l[9:200] for l in blocks.get(r, "").split("\n") if l.startswith("- Title: ")), "")
        L.append(f"{r} {d.get('item')} [{d['status']}] title: {title} | section {d.get('section', '')} | "
                 f"target {d.get('target', '')} | note: {str(d.get('note', ''))[:200]}")
    return "\n".join(L)


def lint_findings(story):
    import lint
    fs = lint.lint_story(story)
    return "\n".join(f"- {f['check']} (line {f['line']}): {f['detail']}" for f in fs) or "- none"


def run_audit(story):
    rec = {"stage": "audit", "story": story, "unit": "audit", "steps": []}
    lint = lint_findings(story)
    base = (f"# Audit of {story}\n\n## Dispositions\n{disp_table(story)}\n\n"
            f"## Deterministic lint findings on the story now (check each; fix the real ones)\n{lint}\n\n"
            f"## Unified diff (before -> now)\n{diff_text(story)}\n")
    if len(base) > 250000 and not FULL:
        base = base[:250000] + "\n[diff cut at 250,000 characters]"
    s = attempt_loop(*SONNET, AUDIT_RULES, base, story, set(), tools=False)
    rec["steps"].append(s)
    findings = s.get("findings", []) if s["applied"] else [{"kind": "audit failed", "issue": s.get("error", "")}]
    base2 = (f"# Second review of {story} (you are the final reviewer)\n\nA first auditor reported these findings "
             f"and fixed what it could (its fixes are already in the diff):\n{json.dumps(findings, ensure_ascii=False)}\n"
             f"\nReview again. Rework anything the first auditor flagged but did not fix, fixed wrongly, or missed.\n"
             f"\n## Dispositions now\n{disp_table(story)}\n\n"
             f"## Deterministic lint findings on the story now (check each; fix the real ones)\n{lint_findings(story)}\n"
             f"\n## Unified diff (before -> now)\n{diff_text(story)}\n")
    if len(base2) > 250000 and not FULL:
        base2 = base2[:250000] + "\n[diff cut at 250,000 characters]"
    rec["sonnet_findings"] = len(findings)
    if not OPUS_NOW:  # every story gets the Opus review later; flagged rulings are listed
        queue_opus("audit", story, "audit", f"Sonnet findings {len(findings)}" +
                   ("" if s["applied"] else "; Sonnet audit failed"), {f.get("ruling") for f in findings})
        record("audit", story, "audit", rec)
        return s["applied"], False
    o = attempt_loop(*OPUS, AUDIT_RULES, base2, story, set(), tools=False)
    rec["steps"].append(o)
    rec["opus_findings"] = len(o.get("findings", [])) if o["applied"] else None
    record("audit", story, "audit", rec)
    return o["applied"] and s["applied"], True


# ------------------------------------------------------------------ rolling Sonnet pass
def haiku_complete(story):
    n = json.loads((MP / "chunks" / story / "meta.json").read_text(encoding="utf-8"))["chunks"]
    return len(list((MP / "disp" / story).glob("c*.jsonl"))) >= n


def verified(story):
    return (ESC / "verified" / f"{story}.json").exists()


def sonnet_story(story):
    """failed chunks -> Not applied items -> audit, all with Sonnet; Opus steps queued. Marks the story verified."""
    res = {"story": story, "failed": [], "notapplied": [], "audit": None}
    for u, _ in units_failed(story):
        if not done("failed", story, u):
            res["failed"].append(run_failed(story, u)[0])
    for u, rs in units_notapplied(story):
        if not done("notapplied", story, u):
            res["notapplied"].append(run_notapplied(story, u, rs)[0])
    if not done("audit", story, "audit"):
        res["audit"] = run_audit(story)[0]
    ok = all(res["failed"]) and all(res["notapplied"]) and res["audit"] is not False
    (ESC / "verified").mkdir(parents=True, exist_ok=True)
    (ESC / "verified" / f"{story}.json").write_text(json.dumps(dict(res, ok=ok, at=time.strftime("%H:%M:%S"))),
                                                    encoding="utf-8")
    return ok


def rolling(jobs):
    stories = [s for s, _ in json.loads((MP / "stories.json").read_text())]
    busy, errs = set(), {}
    with ThreadPoolExecutor(jobs) as ex:
        futs = {}
        while True:
            if (MP / "STOP_ESC").exists() or time.time() > DEADLINE or not usage_ok():
                if not futs:
                    break
                time.sleep(20)
                ready_ok = False
            else:
                ready_ok = True
            for f in [f for f in futs if f.done()]:
                s = futs.pop(f)
                busy.discard(s)
                try:
                    ok, msg = f.result(), ""
                except Exception as e:
                    ok, msg = False, f" ERROR {e!r}"
                    errs[s] = errs.get(s, 0) + 1
                    if errs[s] >= 3:  # give up on this story: the Opus pass takes it
                        queue_opus("story", s, "all", f"Sonnet pass raised {e!r}"[:300])
                        (ESC / "verified").mkdir(parents=True, exist_ok=True)
                        (ESC / "verified" / f"{s}.json").write_text(json.dumps({"story": s, "ok": False,
                                                                                 "error": repr(e)[:300]}), encoding="utf-8")
                with lock:
                    stats["units"] += 1
                    stats["ok" if ok else "failed"] += 1
                    nver = len(list((ESC / "verified").glob("*.json")))
                    line = (f"{time.strftime('%H:%M:%S')} sonnet {s} {'OK' if ok else 'NEEDS OPUS'}{msg} | stories "
                            f"{nver} verified, calls {stats['calls']} cost ${stats['cost']:.2f}")
                    print(line, flush=True)
                    with (MP / "esc-sonnet.log").open("a", encoding="utf-8") as fh:
                        fh.write(line + "\n")
            ready = [s for s in stories if ready_ok and s not in busy and not verified(s) and haiku_complete(s)]
            for s in ready[:max(0, jobs - len(futs))]:
                busy.add(s)
                futs[ex.submit(sonnet_story, s)] = s
            if not futs and all(verified(s) for s in stories):
                break
            time.sleep(20)
    print(f"END sonnet | {json.dumps(stats)}", flush=True)


# ------------------------------------------------------------------ rolling Opus pass
def opus_done(story):
    return (ESC / "opus" / f"{story}.json").exists()


def script_fix_flags():
    """story -> flagged script fixes (from review_fixes), with the fix text."""
    fx = {}
    p = SCRATCH / "apply-v4/2-fixes/fixes.jsonl"
    for l in p.read_text(encoding="utf-8").splitlines():
        if l.strip():
            f = json.loads(l)
            fx[f["fix_id"]] = f
    by_file = {}
    for s, _ in json.loads((MP / "stories.json").read_text()):
        by_file[json.loads((MP / "chunks" / s / "meta.json").read_text(encoding="utf-8"))["project_file"]] = s
    out = {}
    q = ESC / "opus_queue.jsonl"
    for l in (q.read_text(encoding="utf-8").splitlines() if q.exists() else []):
        e = json.loads(l)
        if e["stage"] == "scriptfix" and e["unit"] in fx:
            s = by_file.get(fx[e["unit"]]["file"])
            if s:
                f = fx[e["unit"]]
                out.setdefault(s, []).append(f"- {e['unit']}: {e['reason']}\n  script changed: {f.get('old', '')[:300]!r}"
                                             f" -> {f.get('new', '')[:300]!r}")
    return out


def queue_for(story):
    q = ESC / "opus_queue.jsonl"
    return [json.loads(l) for l in (q.read_text(encoding="utf-8").splitlines() if q.exists() else [])
            if json.loads(l).get("story") == story]


def opus_story(story, flags):
    """Opus reworks what Sonnet could not do, then reviews the whole story (final review)."""
    rec = {"story": story, "steps": []}
    blocks, cd = item_blocks(story), chunk_disp(story)
    fin = merged_dispositions(story)
    for e in queue_for(story):
        if e["stage"] == "failed":
            items = (MP / "chunks" / story / f"{e['unit']}.md").read_text(encoding="utf-8")
            step = attempt_loop(*OPUS, RULES, items + "\n" + context(story, items), story, set(e["rulings"]), tools=False)
            rec["steps"].append(dict(step, stage="failed", unit=e["unit"]))
        elif e["stage"] == "notapplied" and e["rulings"]:
            rs = [r for r in e["rulings"] if fin.get(r, {}).get("status") == "Not applied"]
            if not rs:
                continue
            txt = "\n".join([f"# {story}: items still Not applied after Haiku and Sonnet", ""] +
                            [blocks.get(r, f"## {r}") + f"\n- Previous notes: {fin[r].get('note', '')}\n" for r in rs])
            step = attempt_loop(*OPUS, RULES + (DS_READ_RULES if FULL else READ_RULES), txt + "\n" + context(story, txt)
                                + (source_excerpts(txt) if FULL else ""), story, set(rs), tools=True)
            rec["steps"].append(dict(step, stage="notapplied", unit=e["unit"]))
    # final review: Sonnet's findings, the flagged script fixes, lint, dispositions and the whole diff
    arec = ESC / "audit" / story / "audit.json"
    sf = []
    if arec.exists():
        a = json.loads(arec.read_text(encoding="utf-8"))
        sf = (a["steps"][0].get("findings") or []) if a.get("steps") else []
    extra = ("\n## Script fixes a reviewer flagged in this story (decide: keep, revert or correct each)\n" +
             "\n".join(flags.get(story, []))) if flags.get(story) else ""
    base = (f"# Final review of {story} (you are the final reviewer; Opus)\n\nThe first auditor (Sonnet) reported "
            f"these findings and fixed what it could (its fixes are already in the diff):\n"
            f"{json.dumps(sf, ensure_ascii=False)}\n\nReview again. Rework anything flagged but not fixed, fixed wrongly, "
            f"or missed.{extra}\n\n## Dispositions now\n{disp_table(story)}\n\n"
            f"## Deterministic lint findings on the story now (check each; fix the real ones)\n{lint_findings(story)}\n"
            f"\n## Unified diff (before -> now)\n{diff_text(story)}\n")
    if len(base) > 300000 and not FULL:
        base = base[:300000] + "\n[cut at 300,000 characters]"
    step = attempt_loop(*OPUS, AUDIT_RULES, base, story, set(), tools=False)
    rec["steps"].append(dict(step, stage="audit", unit="audit"))
    rec["opus_findings"] = len(step.get("findings", [])) if step["applied"] else None
    rec["lint_after"] = lint_findings(story)
    (ESC / "opus").mkdir(parents=True, exist_ok=True)
    (ESC / "opus" / f"{story}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    return all(s["applied"] for s in rec["steps"])


def rolling_opus(jobs):
    stories = [s for s, _ in json.loads((MP / "stories.json").read_text())]
    busy, errs = set(), {}
    with ThreadPoolExecutor(jobs) as ex:
        futs = {}
        while True:
            if (MP / "STOP_OPUS").exists() or time.time() > DEADLINE or not usage_ok():
                if not futs:
                    break
                time.sleep(20)
                ready_ok = False
            else:
                ready_ok = True
            for f in [f for f in futs if f.done()]:
                s = futs.pop(f)
                busy.discard(s)
                try:
                    ok, msg = f.result(), ""
                except Exception as e:
                    ok, msg = False, f" ERROR {e!r}"
                    errs[s] = errs.get(s, 0) + 1
                    if errs[s] >= 3:
                        (ESC / "opus").mkdir(parents=True, exist_ok=True)
                        (ESC / "opus" / f"{s}.json").write_text(json.dumps({"story": s, "error": repr(e)[:300]}),
                                                                encoding="utf-8")
                with lock:
                    n = len(list((ESC / "opus").glob("*.json")))
                    line = (f"{time.strftime('%H:%M:%S')} opus {s} {'OK' if ok else 'NOT ALL APPLIED'}{msg} | "
                            f"{n} stories reviewed, calls {stats['calls']} cost ${stats['cost']:.2f}")
                    print(line, flush=True)
                    with (MP / "esc-opus.log").open("a", encoding="utf-8") as fh:
                        fh.write(line + "\n")
            flags = script_fix_flags()
            ready = [s for s in stories if ready_ok and s not in busy and verified(s) and not opus_done(s)]
            for s in ready[:max(0, jobs - len(futs))]:
                busy.add(s)
                futs[ex.submit(opus_story, s, flags)] = s
            if not futs and all(opus_done(s) for s in stories):
                break
            time.sleep(30)
    print(f"END opus | {json.dumps(stats)}", flush=True)


# ------------------------------------------------------------------ driver
def work_list(stage, stories):
    out = []
    for s in stories:
        if stage == "failed":
            out += [(s, u, None) for u, _ in units_failed(s) if not done("failed", s, u)]
        elif stage == "notapplied":
            out += [(s, u, rs) for u, rs in units_notapplied(s) if not done("notapplied", s, u)]
        elif stage == "audit":
            if not done("audit", s, "audit"):
                out.append((s, "audit", None))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["sonnet", "opus", "failed", "notapplied", "audit"])
    ap.add_argument("--jobs", type=int, default=12)
    ap.add_argument("--stories")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--minutes", type=float, default=95)
    ap.add_argument("--backend", choices=["claude", "deepseek", "haiku"], default="claude")
    a = ap.parse_args()
    global DEADLINE, SONNET, OPUS, FULL
    DEADLINE = time.time() + a.minutes * 60
    if a.backend == "haiku":  # both roles on Claude Haiku 5.5 (claude -p, fresh short sessions, 100k auto-compact)
        SONNET, OPUS = ("claude-haiku-5-5", "medium"), ("claude-haiku-5-5", "medium")
    if a.backend == "deepseek":  # both roles on DeepSeek v4.1 Flash through OpenCode, no context limits
        SONNET, OPUS, FULL = (DS, "-"), (DS, "-"), True
        (SCRATCH / "ocsb").mkdir(exist_ok=True)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if a.stage == "sonnet":
        if a.stories:  # test on named stories (must be Haiku-complete)
            for s in a.stories.split(","):
                assert haiku_complete(s), f"{s} still has Haiku chunks"
                print(s, "OK" if sonnet_story(s) else "NEEDS OPUS", json.dumps(stats), flush=True)
            return
        return rolling(a.jobs)
    if a.stage == "opus":
        if a.stories:
            flags = script_fix_flags()
            for s in a.stories.split(","):
                assert verified(s), f"{s} is not Sonnet-verified"
                print(s, "OK" if opus_story(s, flags) else "NOT ALL APPLIED", json.dumps(stats), flush=True)
            return
        return rolling_opus(a.jobs)
    stories = a.stories.split(",") if a.stories else [s for s, _ in json.loads((MP / "stories.json").read_text())]
    work = work_list(a.stage, stories)
    if a.limit:
        work = work[:a.limit]
    print(f"{a.stage}: {len(work)} units over {len({w[0] for w in work})} stories, jobs {a.jobs}", flush=True)
    if a.dry_run:
        return
    # one story at a time per worker: group units by story so two workers never edit the same file
    by = {}
    for w in work:
        by.setdefault(w[0], []).append(w)

    def one_story(units):
        for s, u, rs in units:
            if (MP / "STOP_ESC").exists():
                return
            try:
                if a.stage == "failed":
                    ok, esc = run_failed(s, u)
                elif a.stage == "notapplied":
                    ok, esc = run_notapplied(s, u, rs)
                else:
                    ok, esc = run_audit(s)
                msg = "OK" if ok else "NOT APPLIED"
            except Exception as e:  # never stop the pool
                ok, esc, msg = False, False, f"ERROR {e!r}"
            with lock:
                stats["units"] += 1
                stats["ok" if ok else "failed"] += 1
                stats["escalated"] += bool(esc)
                line = (f"{time.strftime('%H:%M:%S')} {a.stage} {s} {u} {msg}{' (escalated)' if esc else ''} | "
                        f"units {stats['units']} ok {stats['ok']} failed {stats['failed']} escalated "
                        f"{stats['escalated']} calls {stats['calls']} cost ${stats['cost']:.2f}")
                print(line, flush=True)
                with (MP / f"esc-{a.stage}.log").open("a", encoding="utf-8") as fh:
                    fh.write(line + "\n")

    with ThreadPoolExecutor(a.jobs) as ex:
        list(ex.map(one_story, list(by.values())))
    print(f"END {a.stage} | {json.dumps(stats)}", flush=True)


if __name__ == "__main__":
    main()
