import json,re,collections
T=json.load(open('titles.json'));T.pop('ABC123',None)
for x in json.load(open('../amz-kw/rw.json')):
    if x['title']: T[x['sku']]=x['title']
TH=json.load(open('thick.json'))
RX=re.compile(r'(\b(?:8 ?[x×] ?12|12 ?[x×] ?8)(?: in| Inch)?) (Rust-Resistant |Rust-Proof )?(UV-Resistant )?Aluminum')
out={};stat=collections.Counter()
for s,t in T.items():
    if TH.get(s,[None])[0]!='.065': stat['skip_thick']+=1; continue
    if '.065' in t: stat['has']+=1; continue
    m=RX.search(t)
    if not m: stat['nomatch']+=1; continue
    size=m.group(1).replace('×','x'); uv=m.group(3) or ''
    cands=[f"{size} .065 Heavy-Duty Rust-Resistant {uv}Aluminum", f"{size} .065 Heavy-Duty Rust-Resistant Aluminum", f"{size} .065 Rust-Resistant Aluminum"]
    best=None
    for ci,c in enumerate(cands):
        for extra in [(),('Pre-Drilled ',),('Pre-Drilled ','Safety Sign','Sign')]:
            nt=t[:m.start()]+c+t[m.end():]
            if extra: 
                nt=nt.replace('Pre-Drilled ','')
                if len(extra)>1: nt=nt.replace(' Safety Sign by',' Sign by')
            nt=re.sub(r'\s+',' ',nt)
            if len(nt)<=200: best=(nt,ci,len(extra)); break
        if best: break
    if not best: stat['too_long']+=1; continue
    out[s]=best[0]; stat[f'ok_c{best[1]}_x{best[2]}']+=1
json.dump(out,open('new_titles.json','w'))
print(stat, len(out))
import random;random.seed(5)
for s in random.sample(list(out),5): print(T[s]);print(' ->',out[s])
