import json, re, shutil, openpyxl

found = json.load(open('/home/claude/cgap/tmfix/found.json'))

# phrase -> replacement, applied case-preserving to every text field
RULES = [
    (r'mower shop', 'equipment shop'),
    (r'jack rack', 'jack storage rack'),
    (r'magnehelic', 'analog'),
    (r'staging mat', 'staging pad'),
    # battery-plant signs were read as lithium battery products
    (r'lithium-ion cell plants', 'cell manufacturing plants'),
    (r'lithium-ion electrode plants', 'electrode manufacturing plants'),
    (r'battery module and pack assembly plants', 'module and pack assembly plants'),
    (r'battery slurry', 'electrode slurry'),
    (r'battery plant', 'cell plant'),
    (r'lithium-ion', 'cell'),
    (r'lithium', ''),
    (r'batteries', 'cells'),
    (r'battery', 'cell'),
]

def case_like(src, rep):
    if src.isupper(): return rep.upper()
    if src[:1].isupper():
        return ' '.join(w[:1].upper() + w[1:] for w in rep.split(' ')) if src.istitle() else rep[:1].upper() + rep[1:]
    return rep

def fix(text):
    if not isinstance(text, str): return text
    for pat, rep in RULES:
        text = re.sub(pat, lambda m: case_like(m.group(0), rep), text, flags=re.I)
    text = re.sub(r'\s{2,}', ' ', text).replace(' ,', ',').strip()
    return text

TEXT_KEYS = ('item_name', 'product_description', 'bullet_point', 'generic_keyword')
BAD = re.compile(r'(magnehelic|jack rack|mower shop|staging mat|lithium|batter)', re.I)

fixed = {}
for sku, v in found.items():
    row = dict(v['row'])
    for k in list(row):
        if k.split('[')[0] in TEXT_KEYS:
            row[k] = fix(row[k])
    # keywords: Amazon limit 250 bytes; keep words unique
    for k in row:
        if k.startswith('generic_keyword'):
            words = []
            for w in str(row[k]).split():
                if w.lower() not in [x.lower() for x in words]: words.append(w)
            row[k] = ' '.join(words)[:249].rsplit(' ', 1)[0] if len(' '.join(words)) > 249 else ' '.join(words)
    left = [k for k, val in row.items() if isinstance(val, str) and k.split('[')[0] in TEXT_KEYS and BAD.search(val)]
    assert not left, (sku, left)
    if sku in ('CGAP-C18024-812', 'CGAP-N25326-812'):
        base = 'https://raw.githubusercontent.com/joepannell95/CGAP-CAST/main/signs/' + sku.lower() + '-r2'
        for k in row:
            if k.startswith('main_product_image_locator'): row[k] = base + '.jpg'
            elif k.startswith('other_product_image_locator_2'): row[k] = base + '-durability.jpg'
            elif k.startswith('other_product_image_locator_3'): row[k] = base + '-mnt2.jpg'
    fixed[sku] = row

src = '/home/claude/cgap/notice/outputs/SIGNAGE_NOTICE_N2_800.xlsm'
out = '/home/claude/cgap/tmfix/CGAP_Amazon_Listing_Fixes_12.xlsm'
shutil.copy(src, out)
wb = openpyxl.load_workbook(out, keep_vba=True)
ws = wb['Template']
keys = [c.value for c in ws[5]]
col = {k: i + 1 for i, k in enumerate(keys) if k}
ws.delete_rows(8, ws.max_row - 7)
for i, (sku, row) in enumerate(fixed.items()):
    r = 8 + i
    for k, val in row.items():
        if k in col: ws.cell(row=r, column=col[k], value=val)
        else: print('missing column', k)
wb.save(out)
json.dump(fixed, open('/home/claude/cgap/tmfix/fixed.json', 'w'), indent=1)
for sku, row in fixed.items():
    print(sku, '|', row['item_name[marketplace_id=ATVPDKIKX0DER][language_tag=en_US]#1.value'][:100])
