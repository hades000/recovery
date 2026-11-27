"""Dry comparison of the audit (check role): Claude Sonnet 5.5 vs DeepSeek v4.1 Flash on the same story state.
Nothing is applied. Writes mp/compare/<story>.json with both finding lists. Usage: python -I compare_ds.py S1 S2 ..."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import esc  # noqa: E402

(esc.SCRATCH / "ocsb").mkdir(exist_ok=True)


def prompt(story, full):
    esc.FULL = full
    lint = esc.lint_findings(story)
    return (f"# Audit of {story}\n\n## Dispositions\n{esc.disp_table(story)}\n\n"
            f"## Deterministic lint findings on the story now (check each; fix the real ones)\n{lint}\n\n"
            + (f"## The whole story now\n{esc.story_text(story)}\n\n" if full else "")
            + f"## Unified diff (before -> now)\n{esc.diff_text(story)}\n")


def one(story):
    out = {}
    for name, model, full in (("sonnet", esc.SONNET, False), ("deepseek", (esc.DS, "-"), True)):
        p = prompt(story, full)
        text, cost, err = esc.call(*model, esc.AUDIT_RULES, p)
        try:
            out[name] = esc.parse(text).get("findings", []) if not err else {"error": err}
        except Exception as e:
            out[name] = {"error": f"parse: {e}"}
        out[name + "_prompt_chars"] = len(p)
    (esc.MP / "compare").mkdir(exist_ok=True)
    (esc.MP / "compare" / f"{story}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    return story, out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    with ThreadPoolExecutor(6) as ex:
        for s, o in ex.map(one, sys.argv[1:]):
            for k in ("sonnet", "deepseek"):
                v = o[k]
                print(f"== {s} {k}: " + (str(v) if isinstance(v, dict) else f"{len(v)} findings"))
                if isinstance(v, list):
                    for f in v:
                        print(f"   {f.get('ruling')} [{f.get('kind')}] {str(f.get('issue'))[:170]}")
