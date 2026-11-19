import zipfile, re, os, copy, openpyxl
from xml.dom import minidom
# ---- pptx slide 8: add I33, I34
P = '06 Data/Recovery Workbench Volume and Scale Forecast v3.pptx'
z = zipfile.ZipFile(P); infos = z.infolist(); parts = {i.filename: z.read(i.filename) for i in infos}; z.close()
x = parts['ppt/slides/slide8.xml'].decode('utf8')
DO_PPTX = 'I33' not in x
if DO_PPTX:
  i = x.find('<a:t>I32</a:t>'); s = x.rfind('<a:tr ', 0, i); e = x.find('</a:tr>', i) + 7
  row = x[s:e]
  def mk(vals):
      r = row
      for old, new in zip(['I32', 'Requests per active user a minute', '3', 'Peak requests a second'], vals):
          assert r.count('<a:t>%s</a:t>' % old) == 1
          r = r.replace('<a:t>%s</a:t>' % old, '<a:t>%s</a:t>' % new)
      return r
  new = mk(['I33', 'Share of screen actions that read a v_ace_* view', '60%', 'View read load rises with it']) + \
        mk(['I34', 'View reads per screen action', '2', 'Each read is one view query'])
  x = x[:e] + new + x[e:]
  old_ext = '<a:off x="566928" y="1051560"/><a:ext cx="11064240" cy="4352544"/>'
  assert x.count(old_ext) == 1
  x = x.replace(old_ext, '<a:off x="566928" y="1051560"/><a:ext cx="11064240" cy="%d"/>' % (4352544 + 2 * 256032))
  parts['ppt/slides/slide8.xml'] = x.encode('utf8')
  minidom.parseString(parts['ppt/slides/slide8.xml'])
  with zipfile.ZipFile(P + '.tmp', 'w', zipfile.ZIP_DEFLATED) as o:
      for inf in infos: o.writestr(inf, parts[inf.filename])
  os.replace(P + '.tmp', P)
# ---- xlsx
X = '06 Data/Recovery Workbench Volume and Scale Forecast v3.xlsx'
wb = openpyxl.load_workbook(X)
R = wb['Read path']
assert 'only freshness stamp' in R['C16'].value
R['C16'] = ('data_product_load is the Workbench freshness stamp. It is sourced from ace_batch_run, '
            'read through v_ace_batch_status, which gives the ACE per-source business date.')
G = wb['ACE growth']
for r in (21, 22, 23):
    G.unmerge_cells('D%d:E%d' % (r, r))
    v = G.cell(r, 4).value
    assert v and G.cell(r, 5).value is None
    G.cell(r, 5).value = v
    src = G.cell(5, 5)
    for a in ('font', 'fill', 'border', 'alignment', 'protection'):
        setattr(G.cell(r, 5), a, copy.copy(getattr(src, a)))
    G.cell(r, 5).number_format = src.number_format
    G.cell(r, 4).value = None
wb.properties.title = 'Recovery Workbench Volume and Scale Forecast v3'
wb.save(X)
print('ok')
