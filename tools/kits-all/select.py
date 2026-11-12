import json, re, collections
from areas import MAP, SKIP, A
R = json.load(open('/tmp/allsigns.json'))
K = ["sku","series","handle","title","subject","phrase","lines","equipment","install_point","buyer","industries","division","sector","hazard_class","lens","why","img"]
rows = [dict(zip(K, r)) for r in R]
by = collections.defaultdict(list)
for r in rows:
    s = MAP.get(r['sector'], r['sector']); r['sector'] = s; by[s].append(r)

def norm(t): return re.sub(r'[^a-z0-9 ]', ' ', t.lower())
def score(r, kws):
    subj = norm(r['subject'] + ' ' + r['equipment']); ip = norm(r['install_point']); ln = norm(r['lines'])
    s = 0; strong = 0
    for k in kws:
        k = norm(k).strip()
        if not k: continue
        pat = r'\b' + re.escape(k) + (r'(s|es|ed|ing|er|ers)?\b' if len(k) <= 4 else '')
        if re.search(pat, subj): s += 3; strong += 1
        elif re.search(pat, ip): s += 2; strong += 1
        elif re.search(pat, ln): s += 1
    return s if strong else 0

out = {}; report = []
for sec, (label, buyers, areas) in A.items():
    pool = by.get(sec, [])
    used = set(); kits = []
    if len(pool) < 60:
        areas = [label + ' Facility|facility|' + ','.join(set(w for a in areas for w in a.split('|')[2].split(',')))]
        pool_all = True
    for a in areas:
        name, unit, kw = a.split('|'); kws = kw.split(',')
        tiny = len(pool) < 60
        cand = [(score(r, kws) + (1 if tiny else 0), r) for r in pool]
        cand = [c for c in cand if c[0] > 0]
        if len(cand) < 6 and len(pool) >= 60:
            div = collections.Counter(r['division'] for r in pool).most_common(1)[0][0]
            longk = [k for k in kws if len(k) >= 6]
            extra = [(score(r, longk) - 1, r) for r in rows if r['sector'] != sec and r['division'] == div]
            cand += sorted([c for c in extra if c[0] >= 2], key=lambda c: -c[0])[:40]
        cand.sort(key=lambda c: (-c[0], c[1]['sku'] in used, c[1]['series'] != 'DANGER'))
        pick = []; seen = set(); eq = collections.Counter()
        for s, r in cand:
            key = norm(r['subject'])[:28]
            if key in seen or r['sku'] in used: continue
            head = ' '.join(norm(r['subject']).split()[:2])
            if eq[r['equipment']] >= 3 or eq['h:'+head] >= 2: continue
            seen.add(key); eq[r['equipment']] += 1; eq['h:'+head] += 1; pick.append(r)
            if len(pick) >= 8: break
        n = len(pick)
        size = 8 if n >= 8 and (len(cand) >= 14 or tiny) else 6 if n >= 6 else 4 if n >= 4 else 0
        report.append((sec, name, len(cand), size))
        if not size: continue
        pick = pick[:size]
        for r in pick: used.add(r['sku'])
        kits.append({"name": name, "unit": unit, "skus": [r['sku'] for r in pick],
                     "signs": [{k: r[k] for k in ("sku","series","subject","lines","img")} for r in pick]})
    out[sec] = {"label": label, "buyers": buyers, "kits": kits}
json.dump(out, open('selection.json', 'w'))
for x in report:
    if x[3] == 0 or x[2] < 8: print('LOW', x)
print('sectors', len(out), 'kits', sum(len(v['kits']) for v in out.values()),
      collections.Counter(len(k['skus']) for v in out.values() for k in v['kits']))
print('missing sectors', [s for s in A if not by.get(s)])
