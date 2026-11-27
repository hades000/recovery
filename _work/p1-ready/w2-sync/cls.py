import sys,os,re,glob,collections,pickle
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cov.py'),encoding='utf-8').read())
SET=r'C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14'
v2={}
for p in glob.glob(SET+'/04 User stories/Recovery Workbench Service Story Files v2/**/*.md',recursive=True):
    t=open(p,encoding='utf-8-sig').read()
    m=re.search(r'^# (RWB-[A-Z0-9-]+)\s',t,re.M)
    if not m: continue
    m7=re.search(r'^### 7\. .*?$(.*?)(?=^### 8\. )',t,re.M|re.S)
    sec=m7.group(1) if m7 else ''
    parts=re.split(r'^(\s*Scenario(?: Outline)?:.*)$',sec,flags=re.M)
    acs={}
    bg=parts[0]
    for i in range(1,len(parts),2):
        mm=re.search(r'\b(AC\d+[a-z]?)\b',parts[i])
        if mm: acs[mm.group(1)]=(parts[i].strip(),parts[i+1].split('```')[0].strip())
    v2[m.group(1)]=dict(acs=acs,sec=sec)
def norm(s): 
    s=re.sub(r'\((?:new|changed)[^)]*\)','',s)
    return re.sub(r'\s+',' ',s).strip().lower()
def status(k,ac):
    if k not in v2: return 'newstory'
    a=v2[k]['acs'].get(ac)
    if a is None: return 'new'
    h,b=stories[k]['acs'][ac]
    if norm(h)==norm(a[0]) and norm(b)==norm(a[1]): return 'same'
    if norm(b)==norm(a[1]): return 'title'
    return 'changed'
