import json,os,sys,importlib.util,re
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ProcessPoolExecutor
R={"DANGER":"render.py","WARNING":"render_w.py","CAUTION":"render_c.py","NOTICE":"render_n.py","SAFETY FIRST":"render_i.py"}
mods={}
def rmod(h):
    if h not in mods:
        sp=importlib.util.spec_from_file_location('r'+h.replace(' ',''),'/home/claude/cgap/render/'+R[h]); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); mods[h]=m
    return mods[h]
os.makedirs('signimg',exist_ok=True)
def sign(s):
    p='/home/claude/cgap-cast/signs/'+s['img']
    if os.path.exists(p): return p
    q='signimg/'+s['sku'].lower()+'.jpg'
    if not os.path.exists(q):
        lines=[l.strip() for l in s['lines'].split(' / ')]
        im=rmod(s['series']).render(lines).convert('RGB'); im.thumbnail((900,600)); im.save(q,quality=88)
    return q
OUT='/home/claude/cgap-cast/kits-all'; os.makedirs(OUT,exist_ok=True)
F=ImageFont.truetype('/home/claude/cgap/render/Anton.ttf',72)
def hero(k):
    out=f"{OUT}/{k['file']}"
    if os.path.exists(out): return
    sk=k['signs']; n=len(sk); cols={4:2,6:3,8:4,10:5}[n]; rows=(n+cols-1)//cols
    W=1600; pad=40; sw=(W-pad*(cols+1))//cols; sh=int(sw*2/3)
    hero=Image.new('RGB',(W,W),'white'); top=(W-(rows*sh+(rows-1)*pad)-110)//2
    d=ImageDraw.Draw(hero)
    for i,s in enumerate(sk):
        im=Image.open(sign(s)).convert('RGB').resize((sw,sh),Image.LANCZOS)
        x=pad+(i%cols)*(sw+pad); y=top+(i//cols)*(sh+pad)
        d.rectangle([x-3,y-3,x+sw+2,y+sh+2],outline=(210,210,210),width=3); hero.paste(im,(x,y))
    t=f"{k['display'].upper()} SIGN KIT  |  {n} SIGNS"; f=F
    while d.textlength(t,font=f)>W-80: f=ImageFont.truetype('/home/claude/cgap/render/Anton.ttf',f.size-4)
    d.text(((W-d.textlength(t,font=f))/2,top+rows*sh+(rows-1)*pad+50),t,fill=(20,20,20),font=f)
    hero.save(out,quality=82,optimize=True)
if __name__=='__main__':
    ks=json.load(open('kits_final.json'))
    lim=int(sys.argv[1]) if len(sys.argv)>1 else len(ks)
    with ProcessPoolExecutor(os.cpu_count()) as ex: list(ex.map(hero,ks[:lim],chunksize=4))
    print('done',lim)
