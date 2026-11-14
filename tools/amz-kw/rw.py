import json,re
c=json.load(open('../catalog_x.json'))
ACR=set("AM PM OSHA PPE EV CO2 NPO HVAC LP UV ID ADA AED CPR GFCI H2S ATM BESS CO LOTO SDS MSDS RV ATV UTV DOT EPA FAA CDL ICU ER OR MRI CT IV OK USA US TV DVD PA PIN QR CCTV WIFI 911 811 GPS".split())
SMALL=set("a an and or the of to in on at by for with from as per".split())
def tc(s,keep):
    out=[]
    for i,w in enumerate(s.split()):
        core=re.sub(r'[^A-Za-z0-9]','',w)
        if core.upper() in ACR or core in keep: out.append(w.upper() if core.upper() in ACR else w)
        elif i and w.lower() in SMALL: out.append(w.lower())
        else: out.append(w[:1].upper()+w[1:].lower())
    return ' '.join(out)
def weak(r):
    t=r['title'];a=r['action'] or ''
    if 'Room Identification' in t: return False
    return len(t)<100 or len(a.split())<=2 or a.lower() in r['subject'].lower() or bool(re.search(r'\b(Am|Pm)\b',t))
rows=[];nt=nb=0
for r in c:
    keep={w for w in re.findall(r'\b[A-Z0-9]{2,}\b',r['subject'])}
    t=None;b=list(r['bullets'])
    if weak(r):
        m=re.search(r', for ([^,]+), 8x12',r['title']); aud=m.group(1) if m else re.sub(r'\s+(Notices|Signs|Rooms|Signage)$','',r['sector_label'])
        phrase=tc(r['reads'].replace(' / ',' '),keep)
        hdr=r['header'] if r['title'].startswith(r['header']) else ''
        subj=r['subject']
        if phrase.lower().startswith(subj.lower()): mid=phrase
        else: mid=f"{subj} Sign, {phrase}"
        if not mid.endswith('Sign') and ' Sign,' not in mid: mid=f"{mid} Sign"
        t=f"{(hdr+' ') if hdr else ''}{mid}, for {aud}, 8x12 Rust-Resistant Aluminum Sign by CGAP Safety"
        t=re.sub(r'\s+',' ',t)
        if len(t)>200: t=f"{(hdr+' ') if hdr else ''}{mid}, 8x12 Rust-Resistant Aluminum Sign by CGAP Safety"
        if len(t)>200: t=None
        else: nt+=1
    if r['install'].lower()=='at the '+r['subject'].lower():
        tail=re.search(r'(Ordered by[^.]*\.)',b[2]); tail=(' '+tail.group(1)) if tail else ''
        sent=r['reads'].replace(' / ',' ').capitalize()
        sent=tc(sent,keep) if False else sent
        b[1]=f"WHY IT MATTERS: Spells out \"{r['reads'].replace(' / ',' ')}\" in bold letters people can read from across the room, so the message is clear without anyone having to ask."
        b[2]=f"WHERE TO POST IT: At eye level on the wall, door or post where people in the {r['unit'].lower()} area will see it first. Mounts with screws, rivets or zip ties through the pre-drilled corner holes.{tail}"
        nb+=1
    else: b=None
    if t or b: rows.append({'sku':r['sku'],'title':t,'bullets':b})
json.dump(rows,open('rw.json','w'))
print(len(rows),nt,nb)
import random;random.seed(3)
for x in random.sample(rows,6): print(x['title']);print('  ',x['bullets'][1] if x['bullets'] else '');print('  ',x['bullets'][2] if x['bullets'] else '')
print(max(len(x['title']) for x in rows if x['title']), sum('—' in json.dumps(x,ensure_ascii=False) for x in rows))
