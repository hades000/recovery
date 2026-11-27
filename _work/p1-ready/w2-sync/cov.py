import openpyxl,sys,re,csv,glob,os,collections,pickle,hashlib
sys.stdout.reconfigure(encoding='utf-8')
W=r'C:/Users/SahilMore/Downloads/Recovery Workbench SharePoint Set v14/_work/p1-ready'
ST=W+'/stage/04 User stories/Recovery Workbench Service Story Files v3'
TC=W+'/stage/09 Testing and quality/Recovery Workbench Test Cases v9.xlsx'
RTM=W+'/stage/09 Testing and quality/Recovery Workbench Requirements Traceability Matrix v9.xlsx'
stories={}
for p in glob.glob(ST+'/*/*.md'):
    t=open(p,encoding='utf-8-sig').read()
    m=re.search(r'^# (RWB-[A-Z0-9-]+)\s',t,re.M)
    if not m: print('NO KEY',p); continue
    key=m.group(1)
    m7=re.search(r'^### 7\. .*?$(.*?)(?=^### 8\. )',t,re.M|re.S)
    sec=m7.group(1) if m7 else ''
    acs=collections.OrderedDict()
    # gherkin scenarios or other AC forms
    parts=re.split(r'^(\s*Scenario(?: Outline)?:.*)$',sec,flags=re.M)
    for i in range(1,len(parts),2):
        h=parts[i].strip()
        mm=re.search(r'\b(AC\d+[a-z]?)\b',h)
        if mm:
            body=parts[i+1].split('```')[0]
            acs[mm.group(1)]=(h,body.strip())
    fmt='gherkin'
    if not acs:
        for mm in re.finditer(r'^(?:\|\s*|[-*]\s*\**|\**)(AC\d+[a-z]?)\b(.*)$',sec,re.M):
            acs.setdefault(mm.group(1),(mm.group(0).strip(),mm.group(2)))
        fmt='other'
    stories[key]=dict(path=p,acs=acs,fmt=fmt,text=t,sec=sec,mtime=os.path.getmtime(p))
wb=openpyxl.load_workbook(TC,read_only=True)
tcs={}
dups=[]
for r in list(wb['Story test cases'].iter_rows(values_only=True))[4:]:
    if not r or not r[0]: continue
    if r[0] in tcs: dups.append(r[0])
    tcs[r[0]]=r
rtm=openpyxl.load_workbook(RTM,read_only=True)
trace={}
for r in list(rtm['Criterion trace'].iter_rows(values_only=True))[4:]:
    if r and r[0]: trace[(r[0],r[1])]=r
back=collections.defaultdict(set)
for r in csv.DictReader(open(W+'/tc-backfill.csv',encoding='utf-8-sig')):
    back[(r['story_key'],r['ac_id'])].add(r['tc_id'])
