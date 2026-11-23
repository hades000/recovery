from pathlib import Path
for p in [r"03 Requirements and specifications/Recovery Workbench Business Requirements Epic 1 v5.md",
          r"05 Technical architecture/Recovery Workbench Architecture Decision Records v4.md"]:
    b = Path(p).read_bytes()
    print(p, "CRLF:", b.count(b"\r\n"), "LF-only:", b.count(b"\n") - b.count(b"\r\n"))
