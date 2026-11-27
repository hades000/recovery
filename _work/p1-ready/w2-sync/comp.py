import sys,os,re
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cls.py'),encoding='utf-8').read())
def steps(block):
    out={'Given':[],'When':[],'Then':[]}; cur=None; last=None
    for line in block.split('\n'):
        s=line.strip()
        if s.startswith('# Pending') and cur: out[cur].append(s); continue
        s=re.sub(r'\s*TC: (?:to be (?:added|updated)|changed row to be restated)[^.]*\(W2-tests\)\.?','',s).strip()
        if not s or s.startswith(('```','#','@')): continue
        m=re.match(r'^(Given|When|Then|And|But|\*)\s+(.*)$',s)
        if m:
            kw=m.group(1)
            if kw in out: cur=kw
            if cur is None: continue
            out[cur].append(m.group(2).strip()); last=cur
        elif s.startswith('Examples'):
            if last: out[last].append(s)
        elif s.startswith(('|','"""')):
            if last and out[last]: out[last][-1]+=' '+s
        elif s.startswith(('Feature','Background','Scenario','Rule:')): continue
        else:
            if last and out[last] and block.find('Given')>=0 and line.startswith('      '): out[last][-1]+=' '+s
    return out
def background(k):
    sec=stories[k]['sec']
    m=re.search(r'^\s*Background:\s*$(.*?)(?=^\s*(?:@\S+\s*)?Scenario|^```)',sec,re.M|re.S)
    return steps(m.group(1))['Given'] if m else []
def compose(k,ac):
    h,body=stories[k]['acs'][ac]
    st=steps(body)
    g=background(k)+st['Given']
    return tuple('; '.join(x).replace('`','"') for x in (g,st['When'],st['Then']))
def clean_note(s):
    s=str(s)
    n=r'TC: (?:changed row to be restated|to be added|to be updated) in Test Cases v9 \(W2-tests\)'
    s=re.sub(r'\s*\('+n+r'\)','',s)
    s=re.sub(r';\s*'+n,'',s)
    s=re.sub(r'\.?\s*'+n+r'\.?','',s)
    return s.strip()
def title(k,ac):
    h=stories[k]['acs'][ac][0]
    return clean_note(re.sub(r'^\s*Scenario(?: Outline)?:\s*','',h).strip())
allrows=tcs
def covers(r): return re.findall(r'AC\d+[a-z]?',str(r[4] or ''))
def story_rows_old(k):
    return [r for r in tcs.values() if r[16] and k in [x.strip() for x in str(r[16]).split(';')]]
byk={}
for r in tcs.values():
    for x in str(r[15] or '').split(';'):
        byk.setdefault(x.strip(),[]).append(r)
def linked(k,ac):
    ids=set(back.get((k,ac),()))
    if (k,ac) in trace: ids|={x.strip() for x in str(trace[(k,ac)][3] or '').split(',')}
    return [tcs[i] for i in sorted(ids) if i in tcs]
def n(s): return re.sub(r'[\s;.`"\']+','',str(s or '')).lower()
def fits(r,k,ac):
    g,w,t=compose(k,ac)
    return n(t) in n(r[9]) and n(w) in n(r[8])

def withdrawn(k,ac):
    g,w,th=compose(k,ac)
    return not (w or th) and 'withdrawn' in title(k,ac).lower()
