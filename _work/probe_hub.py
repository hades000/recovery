import re, gzip, base64, io, sys

def probe(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        html = f.read()
    print('==', path)
    print('len', len(html))
    # visible text without script bodies
    vis = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.S)
    vis = re.sub(r'<style[^>]*>.*?</style>', ' ', vis, flags=re.S)
    vis = re.sub(r'<[^>]+>', ' ', vis)
    vis = re.sub(r'\s+', ' ', vis).strip()
    print('visible:', vis[:400])
    ids = re.findall(r'<script type="application/octet-stream" id="([^"]+)"', html)
    print('payload count', len(ids), ids[:6])
    for pid in ids[:3]:
        m = re.search(r'<script type="application/octet-stream" id="' + re.escape(pid) + r'">(.*?)</script>', html, flags=re.S)
        if not m:
            continue
        try:
            raw = gzip.decompress(base64.b64decode(m.group(1)))
        except Exception as e:
            print(pid, 'decompress fail', e)
            continue
        txt = raw.decode('utf-8', 'ignore')
        print(pid, 'json len', len(txt), 'head', txt[:200].replace('\n', ' '))
        for kw in ['15 November 2026', '2 November 2026', 'D-RCV-35', 'ACE DB alignment', 'v16', 'v15']:
            print('   ', kw, txt.count(kw))

for p in sys.argv[1:]:
    probe(p)
