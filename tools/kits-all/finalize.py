import json, math, re, collections
d = json.load(open('selection.json'))
EXIST = set(l.strip() for l in open('existing_kit_handles.txt'))
RAW = "https://raw.githubusercontent.com/joepannell95/CGAP-CAST/main/kits-all/"
def price(n):
    dd = 0 if n < 4 else .10 if n < 8 else .15 if n < 12 else .20
    return math.floor(n * 29.99 * (1 - dd)) + 0.99
def slug(t): return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower().replace('&', 'and'))).strip('-')
def code(t, k=3): return ''.join(w[0] for w in re.findall(r'[A-Za-z0-9]+', t) if w.lower() not in ('and','of','the'))[:k].upper()
def title_case(u): return ' '.join(w if w.isupper() else (w if w in ('and','or','of') else w[0].upper() + w[1:]) for w in u.split())
ACR = {'cnc':'CNC','ups':'UPS','ev':'EV','bess':'BESS','mri':'MRI','smt':'SMT','esd':'ESD','mrf':'MRF','eaf':'EAF','bmu':'BMU','sx':'SX','cip':'CIP','rv':'RV','x-ray':'X-ray','ndt':'NDT','agv':'AGV','co2':'CO2','h2s':'H2S'}
def fixu(u): return ' '.join(ACR.get(w, w) for w in u.split())
def plural(u):
    w = u.split(); l = w[-1]
    if re.search(r'(s|x|ch|sh)$', l): l += 'es'
    elif re.search(r'[^aeiou]y$', l): l = l[:-1] + 'ies'
    else: l += 's'
    return ' '.join(w[:-1] + [l])
SMALL = {'and','or','of','the','a','in','at','to'}
names = collections.Counter(k['name'].lower() for v in d.values() for k in v['kits'])
EXIST_NAMES = {'restaurant kitchen','machine shop','loading dock','electrical room','battery room','crane','pump station','cold storage','car wash','tire shop','auto repair shop','grain bin','boat dock and marina','water tower','laser area','confined space','rail yard','fuel depot'}
kits = []; skus = set(); handles = set(); SC = {}
for sec, v in d.items():
    label = v['label']; scode = code(label, 4)
    while scode in SC.values(): scode = scode[:3] + chr(ord(scode[-1]) + 1) if len(scode) > 3 else scode + 'X'
    SC[sec] = scode
    for i, k in enumerate(v['kits']):
        nm = k['name']
        if names[nm.lower()] > 1 or nm.lower() in EXIST_NAMES:
            if not nm.lower().startswith(label.lower().split()[0]): nm = f"{label} {nm}"
        n = len(k['signs']); p = price(n); unit = fixu(k['unit'])
        h = f"{slug(nm)}-sign-kit-{n}-signs"
        while h in EXIST or h in handles: h = h.replace('-sign-kit', f'-{slug(label)}-sign-kit', 1)
        handles.add(h)
        sku = f"CGAP-KIT-{scode}-{code(k['name'],4)}{i+1}-{n}"
        assert sku not in skus, sku; skus.add(sku)
        subs = [s['subject'] for s in k['signs']]
        lst = ', '.join(x.lower() for x in subs[:3])
        lis = "".join(f"<li><strong>{s['series']}</strong> {s['subject']}: {s['lines']}</li>" for s in k['signs'])
        html = (f"<p>The {nm} Safety Sign Kit is every sign one {unit} needs, in one order. Built for {v['buyers']}, it covers the {lst} and more, so the whole area is signed at once instead of one sign at a time.</p>"
            f"<p><strong>How to order:</strong> set the quantity to the number of {plural(unit)} you have. Each kit ships complete and ready to hang.</p>"
            f"<h3>Signs in this kit ({n})</h3><ul>{lis}</ul><h3>Kit details</h3><ul>"
            "<li>Each sign is 8x12 inches on .065 aluminum with a rust-resistant, UV-resistant printed finish for indoor and outdoor use.</li>"
            "<li>Four pre-drilled corner holes for screws, rivets, bolts or zip ties.</li>"
            f"<li>Kit pricing works out to about ${p/n:.2f} a sign, compared with $29.99 each when bought one at a time. Order 5 or more kits for another 10% off, 10 or more for 15%, and 20 or more for 20%, in any mix.</li>"
            "<li>Printed in-house in Amory, Mississippi by CGAP Safety and backed by a five-year warranty against fading, peeling and rust.</li>"
            "<li>Purchase orders and tax-exempt orders welcome. Need a sign changed or added for your site? Request a quote and we will build it into your kit.</li></ul>"
            "<p>A sign supports your safety program; it does not replace training, lockout procedures or required permits.</p>")
        U = title_case(unit)
        title = f"{nm} Safety Sign Kit, {n} Signs for One {U}, 8x12 Rust-Resistant Aluminum, by CGAP Safety"
        tag = f"{label} Kits"
        inp = {"title": title, "handle": h, "descriptionHtml": html, "vendor": "CGAP Industries", "productType": "Safety Sign Kit", "status": "ACTIVE",
               "tags": ["CGAP Safety", "Sign Kit", tag, f"Sector: {sec}", "Made in USA", "8x12 Aluminum"],
               "seo": {"title": f"{nm} Sign Kit, {n} Signs | CGAP Safety"[:70],
                       "description": f"Every sign one {unit} needs in one order: {n} 8x12 rust-resistant aluminum signs for {v['buyers']}. Order by site count. ${p:.2f} per kit, made in USA."[:320]},
               "productOptions": [{"name": "Title", "values": [{"name": "Default Title"}]}],
               "variants": [{"optionValues": [{"optionName": "Title", "name": "Default Title"}], "price": f"{p:.2f}", "sku": sku, "inventoryPolicy": "DENY", "taxable": True,
                             "inventoryItem": {"tracked": False, "requiresShipping": True, "measurement": {"weight": {"value": round(n * 0.6 + 0.5, 1), "unit": "POUNDS"}}}}],
               "files": [{"originalSource": RAW + h + ".jpg", "contentType": "IMAGE", "alt": f"{nm} safety sign kit, {n} 8x12 aluminum signs"}]}
        kits.append({"sector": sec, "label": label, "display": nm, "file": h + ".jpg", "handle": h, "sku": sku, "signs": k['signs'], "input": inp})
json.dump(kits, open('kits_final.json', 'w'))
with open('kits_bulk.jsonl', 'w') as f:
    for k in kits: f.write(json.dumps({"productSet": k['input']}) + "\n")
print(len(kits), len(set(k['label'] for k in kits)), 'labels')
print(collections.Counter(k['label'] for k in kits).most_common(3))
for k in kits[:3] + kits[200:203]: print(k['input']['title'], '|', k['handle'], '|', k['sku'], k['input']['variants'][0]['price'])
