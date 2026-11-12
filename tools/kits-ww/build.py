import json,os,sys,importlib.util
from PIL import Image, ImageDraw, ImageFont
exec(open('/tmp/kitdef.py').read())
comp=json.load(open('comp.json'))
R={"DANGER":"render.py","WARNING":"render_w.py","CAUTION":"render_c.py","NOTICE":"render_n.py","SAFETY FIRST":"render_i.py"}
mods={}
sys.path.insert(0,'/home/claude/cgap/render'); sys.path.insert(0,'/home/claude/cgap/comp')
def rmod(h):
    if h not in mods:
        sp=importlib.util.spec_from_file_location('r'+h.replace(' ',''),'/home/claude/cgap/render/'+R[h]); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); mods[h]=m
    return mods[h]
os.makedirs('img',exist_ok=True)
def img(sku):
    p=f'/home/claude/cgap-cast/signs/{sku.lower()}.jpg'
    if os.path.exists(p): return p
    q=f'img/{sku.lower()}.jpg'
    if not os.path.exists(q):
        c=comp[sku]; lines=[l.strip() for l in c['lines'].split(' / ')]
        rmod(c['series']).render(lines).convert('RGB').save(q,quality=88)
    return q
OUT='/home/claude/cgap-cast/kits-ww'; os.makedirs(OUT,exist_ok=True)
for code,name,buyers,place,skus in KITS:
    n=len(skus); cols=4 if n in (8,12) else (2 if n==4 else 3); rows=(n+cols-1)//cols
    W=2000; pad=50; sw=(W-pad*(cols+1))//cols; sh=int(sw*2/3)
    H=max(2000, pad*(rows+1)+sh*rows+140)
    hero=Image.new('RGB',(W,2000),'white')
    top=(2000-(rows*sh+(rows-1)*pad)-120)//2
    for i,s in enumerate(skus):
        im=Image.open(img(s)).convert('RGB').resize((sw,sh),Image.LANCZOS)
        x=pad+(i%cols)*(sw+pad); y=top+(i//cols)*(sh+pad)
        ImageDraw.Draw(hero).rectangle([x-3,y-3,x+sw+2,y+sh+2],outline=(210,210,210),width=3)
        hero.paste(im,(x,y))
    d=ImageDraw.Draw(hero)
    try: f=ImageFont.truetype('/home/claude/cgap/render/Anton.ttf',86)
    except: f=ImageFont.load_default()
    t=f"{name.upper()} SIGN KIT  |  {n} SIGNS"
    tw=d.textlength(t,font=f); y=top+rows*sh+(rows-1)*pad+60
    d.text(((W-tw)/2,y),t,fill=(20,20,20),font=f)
    hero.save(f'{OUT}/kit-ww-{code.lower()}-{n}.jpg',quality=86,optimize=True)
    print(code,n)
