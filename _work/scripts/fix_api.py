import io

p = r'05 Technical architecture\Recovery Workbench API Specification v3.yaml'
t = io.open(p, encoding='utf-8').read()
old = """        primaryCustomerId:
          type: string
          format: uuid
          description: The borrower the case is opened for"""
new = """        primaryPersonKey:
          type: string
          description: The ACE person_key of the borrower the case is opened for; held as a business key with no foreign key into ACE"""
assert old in t
t = t.replace(old, new).replace('      - primaryCustomerId\n', '      - primaryPersonKey\n')
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('yaml updated', t.count('primaryPersonKey'), t.count('primaryCustomerId'))

p = r'05 Technical architecture\Recovery Workbench API Specification v3.html'
t = io.open(p, encoding='utf-8').read()
old = '<tr data-g="Case"><td class="">Case</td><td class="code">primaryCustomerId</td><td class="">string (uuid)</td><td class="">Yes</td><td class=""></td><td class="">The borrower the case is opened for</td></tr>'
new = '<tr data-g="Case"><td class="">Case</td><td class="code">primaryPersonKey</td><td class="">string</td><td class="">Yes</td><td class=""></td><td class="">The ACE person_key of the borrower the case is opened for; held as a business key with no foreign key into ACE</td></tr>'
assert old in t
t = t.replace(old, new)
io.open(p, 'w', encoding='utf-8', newline='\n').write(t)
print('html updated', t.count('primaryPersonKey'), t.count('primaryCustomerId'))
