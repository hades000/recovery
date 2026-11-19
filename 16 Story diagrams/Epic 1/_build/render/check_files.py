"""Load every .excalidraw through Excalidraw's own restore() and report."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
OUT = HERE.parent.parent
TEMPLATE = HERE / "render_template.html"

JS = """
async (data) => {
  const m = await import("https://esm.sh/@excalidraw/excalidraw@0.17.6?bundle");
  const Exc = m.default || m;
  try {
    const restored = await Exc.restore(data, null, null);
    return { ok: true, n: restored.elements.length };
  } catch (e) {
    return { ok: false, err: String(e) };
  }
}
"""

files = sorted(OUT.glob("*.excalidraw"))
bad = 0
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(TEMPLATE.as_uri())
    page.wait_for_function("window.__moduleReady === true", timeout=60000)
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        result = page.evaluate(JS, data)
        if result["ok"]:
            print(f"OK   {path.name}  ({result['n']} elements)")
        else:
            bad += 1
            print(f"FAIL {path.name}: {result['err'][:200]}")
    browser.close()

print(f"\n{len(files) - bad} loaded, {bad} failed")
raise SystemExit(1 if bad else 0)
