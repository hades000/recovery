"""Recount operations from every contract file and align index.yaml."""
import os
import re

import yaml

from ed import API, STAGE, Doc

M = ('get', 'put', 'post', 'patch', 'delete')


def count(name):
    d = yaml.safe_load(open(os.path.join(STAGE, API, name), encoding='utf-8'))
    return sum(1 for p in d['paths'].values() for m in p if m in M)


X = Doc(API + 'index.yaml')
idx = yaml.safe_load(X.text)
total = 0
for e in idx['x-document-set']:
    n = count(e['file'])
    total += n
    if n != e['operations']:
        a = X.text.index('  file: "%s"\n' % e['file'])
        b = X.text.index('  operations: ', a)
        c = X.text.index('\n', b)
        old = X.text[b:c]
        X.text = X.text[:b] + '  operations: %d' % n + X.text[c:]
        X.pending.append(('EDIT', 'x-document-set %s operations' % e['service'], old.strip(), 'operations: %d' % n,
                          'RD-P1-060;RD-P1-063', '', ''))
        print(e['file'], e['operations'], '->', n)
X.sub('  operations: %d\n  asyncapi-documents' % idx['x-totals']['operations'], '  operations: %d\n  asyncapi-documents' % total,
      'x-totals.operations', d='RD-P1-060;RD-P1-063')
print('total', total, 'was', idx['x-totals']['operations'])
X.save()
