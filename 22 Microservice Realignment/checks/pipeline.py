"""One run of the deterministic build-readiness pipeline (sandbox prototype, D-RCV-60).

Stages, each in its own folder under --out:
  1-check      detcheck.py on the stories (one legacy key, or every story with --all; --jobs in parallel)
  2-fixes      stories: mkfixes.py for a legacy key (every fix type, X20 last with the x20_fixes hold rules),
               or x20_fixes.py with --all (version references only: the other fix types need a legacy key)
               declog:  declog_versions.py (pointer column in the next Decision Log version)
  3-merged     one fixes.jsonl; fix IDs prefixed by stage, so they stay unique
  4-applied    apply_fixes.py: next versions of every changed file (stories, Test Cases, Decision Log)
  5-recheck    detcheck.py on the next-version stories, reading the produced workbooks;
               declog_versions.py on the next Decision Log (expects 0 rows)
Writes only under --out (outside ROOT). Never writes a project file. summary.md holds the counts and times.

Usage: python -I pipeline.py --root <ROOT> --out <dir> (--legacy RWB-E1-018 | --all) [--jobs 8]
       [--wp B-P3-01] [--date "26 November 2026"] [--note "..."] [--dry-run] [--skip-declog]
"""
import argparse, json, shutil, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = "T3 Code / OpenCode / DeepSeek v4.1 Flash"


def run(step, args, times, log):
    t0 = time.time()
    r = subprocess.run([sys.executable, "-I", str(HERE / step), *map(str, args)], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    dt = time.time() - t0
    times.append((step, dt))
    last = (r.stdout.strip().splitlines() or [""])[-1]
    log.append(f"{step}: rc {r.returncode}, {dt:.1f} s: {last}")
    print(log[-1], flush=True)
    if r.returncode not in (0, 1):  # apply_fixes returns 1 when some fix FAILED: reported, not fatal
        sys.exit(f"{step} failed (rc {r.returncode}):\n{r.stderr[-2000:]}")
    return r


def load(p):
    p = Path(p)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8-sig").splitlines() if l.strip()]


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--legacy")
    g.add_argument("--all", action="store_true")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--wp", default="DET")
    ap.add_argument("--date", default="26 November 2026")
    ap.add_argument("--note", default="fixes from the deterministic build-readiness checks")
    ap.add_argument("--dry-run", action="store_true", help="plan and report, write no next-version file")
    ap.add_argument("--skip-declog", action="store_true")
    ap.add_argument("--cache", help="converted-source cache (default <out>/_cache); reused across runs")
    a = ap.parse_args(argv)
    root, out = Path(a.root).resolve(), Path(a.out).resolve()
    if out == root or root in out.parents:
        sys.exit("--out must be outside ROOT (sandbox only)")
    if out.exists() and any(out.iterdir()):
        sys.exit(f"--out {out} is not empty (never overwrite a run)")
    out.mkdir(parents=True, exist_ok=True)
    cache = Path(a.cache).resolve() if a.cache else out / "_cache"
    scope = ["--legacy", a.legacy] if a.legacy else ["--all"]
    times, log, t_all = [], [], time.time()
    sys.path.insert(0, str(HERE))
    import rwbsrc

    # 1. check
    run("detcheck.py", ["--root", root, "--cache", cache, "--out", out / "1-check", "--wp", a.wp, *scope,
                        "--jobs", a.jobs], times, log)
    # 2. fixes
    if a.legacy:
        run("mkfixes.py", ["--root", root, "--det", out / "1-check", "--out", out / "2-fixes/stories",
                           "--legacy", a.legacy], times, log)
    else:
        run("x20_fixes.py", ["--root", root, "--out", out / "2-fixes/stories", "--all"], times, log)
    if not a.skip_declog:
        run("declog_versions.py", ["--root", root, "--out", out / "2-fixes/declog", "--date", a.date,
                                   "--wp", f"{a.wp}-DLV"], times, log)
    # 3. merge
    merged = []
    for stage, p in (("S", out / "2-fixes/stories/fixes.jsonl"), ("D", out / "2-fixes/declog/fixes.jsonl")):
        for f in load(p):
            f["fix_id"] = f"{stage}-{f['fix_id']}"
            merged.append(f)
    files_by_stage = {}
    for f in merged:
        files_by_stage.setdefault(f["file"], set()).add(f["fix_id"][0])
    clash = [k for k, v in files_by_stage.items() if len(v) > 1]
    if clash:
        sys.exit(f"two fix stages edit the same file: {clash}")
    (out / "3-merged").mkdir(parents=True)
    (out / "3-merged/fixes.jsonl").write_text("".join(json.dumps(f, ensure_ascii=False) + "\n" for f in merged),
                                              encoding="utf-8")
    # 4. apply
    run("apply_fixes.py", ["--root", root, "--fixes", out / "3-merged/fixes.jsonl", "--out", out / "4-applied",
                           "--date", a.date, "--note", a.note, *(["--dry-run"] if a.dry_run else [])], times, log)
    res = load(out / "4-applied/apply_result.jsonl")
    # 5. re-check the next versions
    produced = {}
    for r in res:
        if r["status"] == "APPLIED":
            produced[r["file"]] = out / "4-applied" / Path(r["file"]).parent / r["to"]
    rc_rows = rc_dl = None
    if not a.dry_run and produced:
        stories = sorted(str(p) for f, p in produced.items() if f.endswith(".md") and rwbsrc.story_key_from_name(p.name))
        overrides = [f"{k}={produced[v]}" for k, v in rwbsrc.SOURCES.items() if v in produced]
        if stories:
            lst = out / "5-recheck/stories.txt"
            lst.parent.mkdir(parents=True, exist_ok=True)
            lst.write_text("\n".join(stories) + "\n", encoding="utf-8")
            run("detcheck.py", ["--root", root, "--cache", cache, "--out", out / "5-recheck/stories", "--wp",
                                f"{a.wp}-RE", "--story-list", lst, "--jobs", a.jobs,
                                *[x for o in overrides for x in ("--source", o)]], times, log)
            rc_rows = load(out / "5-recheck/stories/gaps.jsonl")
        dl = rwbsrc.SOURCES["declog"]
        if dl in produced:
            run("declog_versions.py", ["--root", root, "--out", out / "5-recheck/declog", "--declog", produced[dl],
                                       "--wp", f"{a.wp}-DLV-RE"], times, log)
            rc_dl = load(out / "5-recheck/declog/gaps.jsonl")
    # summary
    before = load(out / "1-check/gaps.jsonl")
    disp = load(out / "2-fixes/stories/disposition.jsonl")
    held = load(out / "2-fixes/stories/held.jsonl")
    dl_rows = load(out / "2-fixes/declog/gaps.jsonl")
    ok = sum(r["status"] == "APPLIED" for r in res)
    lines = [f"# Pipeline run ({a.wp}, {'legacy ' + a.legacy if a.legacy else 'all stories'})", "",
             f"Tool: {TOOL}. Decision D-RCV-60. {'Dry run: no next-version file written. ' if a.dry_run else ''}"
             f"Total time {time.time() - t_all:.1f} s.", "",
             "| Stage | Result |", "|---|---|",
             f"| 1 Check | {len(before)} story rows |"]
    if disp:
        from collections import Counter
        c = Counter(d["status"] for d in disp)
        lines.append(f"| 2 Fixes (stories) | {len(load(out / '2-fixes/stories/fixes.jsonl'))} fix records; "
                     + ", ".join(f"{k} {v}" for k, v in sorted(c.items())) + " |")
    else:
        lines.append(f"| 2 Fixes (stories, X20) | {len(load(out / '2-fixes/stories/fixes.jsonl'))} line fixes, "
                     f"{len(held)} lines held |")
    if not a.skip_declog:
        lines.append(f"| 2 Fixes (Decision Log) | {len(dl_rows)} decision rows cite an older version; "
                     f"{len(load(out / '2-fixes/declog/fixes.jsonl'))} fix records |")
    lines.append(f"| 4 Apply | {ok} of {len(res)} fixes applied over {len({r['file'] for r in res})} files |")
    if rc_rows is not None:
        lines.append(f"| 5 Re-check (stories) | {len(rc_rows)} rows (was {len(before)}) |")
    if rc_dl is not None:
        lines.append(f"| 5 Re-check (Decision Log) | {len(rc_dl)} rows (expected 0) |")
    lines += ["", "| Step | Seconds |", "|---|---|"] + [f"| {s} | {t:.1f} |" for s, t in times]
    lines += ["", "## Log", ""] + [f"- {l}" for l in log]
    (out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"done in {time.time() - t_all:.1f} s -> {out / 'summary.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
