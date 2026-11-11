import json, sys
sys.path.insert(0, '/home/claude/cgap/amz')
from convert import rows_to_attributes
fixed = json.load(open('/home/claude/cgap/tmfix/fixed.json'))
out = []
for sku, row in fixed.items():
    pt, attrs = rows_to_attributes(row)
    new = sku + '-R2'
    for el in attrs.get('part_number', []): el['value'] = new
    out.append({'old_sku': sku, 'sku': new, 'productType': pt, 'attributes': attrs})
json.dump(out, open('/home/claude/cgap/amz/relist12.json', 'w'))
print(len(out), 'listings;', sorted({k for o in out for k in o['attributes']})[:60])
