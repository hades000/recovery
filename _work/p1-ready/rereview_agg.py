import csv, glob, os, re, collections
RR = r'C:\Users\SahilMore\Downloads\RWB Story Review P1\rereview'
OUT = r'C:\Users\SahilMore\Downloads\Recovery Workbench SharePoint Set v14\_work\p1-ready\packets'
rows, verd = [], {}
for d in sorted(glob.glob(os.path.join(RR, '*'))):
    k = os.path.basename(d)
    md = glob.glob(os.path.join(d, '*review.md'))
    if md:
        t = open(md[0], encoding='utf-8', errors='replace').read()
        m = re.search(r'(NOT READY|READY WITH MINOR GAPS|READY)', t); verd[k] = m.group(1) if m else '?'
    for f in glob.glob(os.path.join(d, '*findings.csv')):
        for r in csv.DictReader(open(f, encoding='utf-8-sig')):
            r = {a.strip().lower(): (b or '').strip() for a, b in r.items() if a}
            r['story_folder'] = k; rows.append(r)
def lane(r):
    fo = r.get('fix_owner', '').lower()
    if fo.startswith('ruling'): return 'ruling'
    if fo.startswith('document'): return 'document'
    return 'story'
for r in rows: r['lane'] = lane(r)
keys = ['story_folder','gap_no','severity','type','codes','story_section','conflicts_with','suggested_fix','fix_owner','lane','evidence','known_ref']
for ln in ('ruling','document','story'):
    with open(os.path.join(OUT, f'rereview {ln} items.csv'), 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=keys, extrasaction='ignore', quoting=csv.QUOTE_ALL); w.writeheader()
        w.writerows([r for r in rows if r['lane'] == ln])
c = collections.Counter((r['lane'], r.get('severity','')) for r in rows)
print('stories', len(verd), collections.Counter(verd.values()))
print('findings', len(rows)); [print(k, v) for k, v in sorted(c.items())]
docs = collections.Counter(r.get('fix_owner','')[9:60] for r in rows if r['lane']=='document')
print('top documents:'); [print(v, k) for k, v in docs.most_common(20)]
