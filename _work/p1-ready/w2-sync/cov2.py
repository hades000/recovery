import sys,os,re,collections
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'comp.py'),encoding='utf-8').read())
def keyed(k,ac):
    return [r for r in byk.get(k,[]) if ac in re.findall(r'AC\d+[a-z]?',str(r[4]).split('—')[0]) and r[12]=='Live']
cat=collections.defaultdict(list)
for k,s in stories.items():
    for ac in s['acs']:
        need = k.startswith('RWB-P1-') or status(k,ac)!='same'
        if not need: continue
        K=keyed(k,ac); L=[r for r in linked(k,ac) if r[12]=='Live']
        rows=K or L
        if not rows: cat['no_row'].append((k,ac)); continue
        if status(k,ac)!='same' and not any(fits(r,k,ac) for r in rows+L): cat['stale'].append((k,ac,[r[0] for r in rows][:4]))
        if (k,ac) not in trace: cat['no_trace'].append((k,ac,[r[0] for r in rows]))
        if (k,ac) not in back: cat['no_back'].append((k,ac,[r[0] for r in rows]))
