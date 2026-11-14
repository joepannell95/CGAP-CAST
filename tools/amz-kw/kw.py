import re,json
STOP=set("the a an and or for of to in on at by with from your you be is are this that do not no it its as up out sign signs 8x12 8×12 12x8 12 8 in x aluminum aluminium rust resistant rust-resistant uv uv-resistant pre-drilled predrilled heavy-duty heavy duty proof .040 040 cgap safety by made usa premium grade 4 6 10 or".split())
THEMES=[
(r"voltage|electric|shock|panel|generator|substation|switchgear|arc", "electrician electrical room breaker box utility power line transformer energized equipment lockout"),
(r"fire|extinguisher|flammable|fuel|hot work|weld|propane|gas cylinder|compressed gas", "fire hazard combustible gasoline diesel no smoking flame torch acetylene oxygen tank storage"),
(r"radiation|x-ray|mri|magnet|uv|laser|tanning|radioactive", "radiation area caution radiology imaging hospital clinic lab nuclear medicine trefoil"),
(r"biohazard|hazardous waste|chemical|acid|caustic|methylene|ozone|toxic|h2s|hydrogen sulfide|radon|algae", "chemical hazard corrosive poison toxic fumes ppe required hazmat msds sds storage area lab"),
(r"pool|spa|hot tub|water|drowning|basin|dock|marina|lake|pond", "pool rules swimming no lifeguard waterfront boat ramp pier beach lake house rental"),
(r"dock|warehouse|forklift|loading|battery charging|lead acid", "warehouse forklift traffic loading dock fall hazard distribution center shipping receiving"),
(r"construction|demolition|structure|blasting|jackhammer|site|roof|concrete", "construction zone hard hat area job site contractor keep out authorized personnel only"),
(r"robot|exoskeleton|3d print|extruder|machine|pinch|cell", "machine guarding moving parts pinch point automation factory manufacturing plant"),
(r"drone|uav", "drone flight area unmanned aircraft no fly zone"),
(r"battery|lithium|ess|bess|e-bike|scooter|ev ", "lithium ion battery fire charging station energy storage solar power"),
(r"range|gun|firing|hunting", "shooting range firearms target practice gun club private property"),
(r"trespass|keep out|authorized", "no trespassing private property keep out posted restricted area"),
(r"quantum|cryogenic|helium|ai |artificial|server|data", "server room data center lab research cryogenic liquid nitrogen oxygen deficiency"),
(r"mower|lawn|tree|landscap", "yard lawn care landscaping equipment"),
]
KIT="sign set bundle pack multipack variety assortment starter kit"
def kw(title, sku):
    t=title.lower()
    words=[w for w in re.findall(r"[a-z0-9][a-z0-9\-/]*",t)]
    tw=set(w.strip('-/') for w in words)
    add=[]
    for rx,s in THEMES:
        if re.search(rx,t): add+=s.split()
    if sku.startswith('CGAP-KIT') or ' kit' in t: add=KIT.split()+add
    add+="safety signs metal placard warning notice label osha ansi outdoor indoor wall mount commercial business industrial facility".split()
    out=[]; seen=set(tw)|STOP
    for w in add:
        if w not in seen: out.append(w); seen.add(w)
    s=' '.join(out)
    b=s.encode()
    while len(b)>245: s=s.rsplit(' ',1)[0]; b=s.encode()
    return s
KITX={
'APT':'landlord rental property multifamily condo hoa building maintenance pool laundry room boiler',
'AUTOSHP':'mechanic garage auto service bay vehicle lift oil change',
'BODYSHP':'collision repair spray booth paint shop respirator flammable',
'BREW':'craft beer brewhouse winery tasting room co2 confined space',
'CAMPRV':'rv campground campsite park resort cabin',
'CARWSH':'car wash bay detailing slippery floor',
'CATTLE':'ranch livestock barn corral bull horses',
'CELL':'cell tower telecom shelter rf radiation antenna',
'CHURCH':'church school facility custodian janitor maintenance',
'CONCRETE':'masonry concrete contractor cement silica dust',
'ELECJOB':'electrician contractor job site trailer arc flash',
'FARM':'farm barn tractor homestead agriculture',
'FEC':'arcade trampoline park bowling go kart amusement',
'FIBER':'fiber optic splicing telecom contractor trailer laser',
'FIRE':'firehouse fire station volunteer firefighter apparatus bay',
'FOODTRK':'food truck concession stand trailer propane hot surface',
'GASST':'gas station convenience store c-store fuel pump no smoking',
'GENSET':'generator room standby power backup diesel',
'GRAIN':'grain bin silo feed mill engulfment confined space',
'GYM':'gym fitness center weight room health club',
'HVAC':'hvac contractor refrigerant mechanical room',
'KITCHEN':'restaurant kitchen commercial kitchen food service hot surface',
'LAUNDRY':'laundromat laundry dry cleaner',
'LAWN':'landscaping lawn care mower equipment yard',
'LOGGING':'logging timber forestry chainsaw',
'MACHSHP':'machine shop cnc lathe fabrication',
'MARINA':'marina boat dock pier boat ramp fuel dock',
'MFGFLR':'manufacturing factory production floor plant',
'PARKS':'parks recreation playground city park trail',
'PLUMB':'plumbing contractor plumber shop',
'POOLPUB':'public pool splash pad aquatic center swimming',
'POULTRY':'poultry chicken house broiler farm biosecurity',
'PROPANE':'propane lpg fuel distributor bulk plant flammable gas',
'PUBWRK':'public works municipal city county yard',
'RANGE':'shooting range hunting club gun club firearms',
'RENTAL':'equipment rental yard heavy equipment',
'RETAIL':'retail store stockroom backroom receiving',
'ROOF':'roofing roofer fall protection ladder',
'SERVER':'server room data closet it network rack',
'SITE':'construction site entrance hard hat ppe jobsite',
'SOLAR':'solar panels pv array battery storage inverter',
'STORAGE':'self storage mini storage units',
'TIRE':'tire shop tire service inflation cage',
'TREE':'tree service arborist chainsaw chipper',
'TRKYARD':'truck stop fleet yard trucking terminal',
'VET':'veterinary clinic animal hospital kennel boarding',
'WAREHSE':'warehouse forklift distribution center',
'WATERTP':'water treatment wastewater plant chlorine utility',
'WOODCHP':'sawmill wood chip lumber yard',
'WOODSHP':'woodworking cabinet shop wood dust saw',
}
import sys
out=[]
for line in open('rows.tsv'):
    sku,title=line.rstrip('\n').split('\t')
    t=title
    if sku.startswith('CGAP-KIT-'): t=title+' '+KITX[sku[9:]]
    k=kw(t,sku) if not sku.startswith('CGAP-KIT-') else KIT+' safety signs metal placard warning caution danger notice osha ansi outdoor indoor wall mount commercial business'
    if sku=='CGAP-CUSTOM-SIGN-8X12': k='custom made personalized printed text logo company name '+k
    if sku.startswith('CGAP-KIT-'): k=(KITX[sku[9:]]+' '+k)
    # dedupe & cap
    seen=set();w=[]
    for x in k.split():
        if x not in seen: seen.add(x); w.append(x)
    s=' '.join(w)
    while len(s.encode())>245: s=s.rsplit(' ',1)[0]
    out.append((sku,s))
json.dump(out,open('kw_out.json','w'),indent=0)
for s,k in out[:3]+out[9:11]+out[60:62]: print(s,'|',k,len(k))
print(len(out))
