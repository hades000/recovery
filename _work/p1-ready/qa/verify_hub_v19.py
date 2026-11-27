import base64,gzip,json,re,subprocess
from pathlib import Path
h,=Path('stage/14 Story Updates').glob('*Hub v19.html')
html=h.read_text(encoding='utf-8')
p=re.search(r'<script type="application/octet-stream" id="payload">([^<]+)</script>',html)
m=json.loads(gzip.decompress(base64.b64decode(p[1])))
js=html.split('function attr(t,name){',1)[1].split('const FAM=[];',1)[0]
doclist=[]
expected={}
for d in m['docs']:
    secs=[]
    for s in d['secs']:
        if s['h'].startswith('RWB-'):
            # The story index only reads markdown table attributes.
            secs.append({'h':s['h'],'t':'\n'.join(x for x in s['t'].splitlines() if re.match(r'^\|?\s*(Story key|Module|Release|Service|Status|Wave|Business epic|Epic|Work type|Parallel lane|Ready to start|Legacy key|Suggested owner)\s*\|',x))})
            if d.get('p1Stage') and s['h'].startswith('RWB-P1-'):
                expected[s['h'].split()[0]]=d['name']
    doclist.append({'name':d['name'],'inzip':d['inzip'],'p1Stage':d.get('p1Stage',False),'secs':secs})
assert len(expected)==62
for k in expected:
    di,si=m['ids'][k]['d']
    assert m['docs'][di]['p1Stage'] and m['docs'][di]['secs'][si]['h'].startswith(k+' ')
code='let STORIES=[]; const M={docs:'+json.dumps(doclist)+'}; function attr(t,name){'+js
code+='\nbuildStories(); const expected='+json.dumps(expected)+';'
code+="""
const p1 = STORIES.filter(s => s.k.startsWith('RWB-P1-') && expected[s.k]);
if (p1.length !== 62 || p1.some(s => s.src !== expected[s.k])) process.exitCode=1;
console.log('Indexed P1 views backed by staged v3 stories:', p1.length);
"""
r=subprocess.run(['node','-'],input=code,encoding='utf-8',check=True)
