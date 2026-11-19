import sys, pymupdf
d = pymupdf.open(sys.argv[1]); out = sys.argv[2]
for i, p in enumerate(d, 1):
    p.get_pixmap(dpi=70).save(f"{out}/s{i:02d}.png")
