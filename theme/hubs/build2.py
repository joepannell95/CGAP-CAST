import json, html
# Set 2 hazard hubs. existing=True means add a title source + guide to an existing collection.
H = [
dict(handle="forklift-pedestrian-signs", title="Forklift and Pedestrian Traffic Signs",
 seo=("Forklift Safety Signs | Forklift Traffic, Pedestrian Crossing | CGAP", "Forklift traffic, pedestrian crossing, battery charging and propane change signs for warehouses, plants and docks. 8x12 aluminum, made in USA."),
 inc=["Forklift","Lift Truck","Pallet Jack","Reach Truck","Order Picker","Pedestrian Walkway","Powered Industrial Truck"], exc=[],
 intro="<p>Signs for forklift and pedestrian traffic: forklift lanes, crossings, blind corners, pedestrian walkways, battery charging and propane cylinder change areas, docks and rack aisles. An operator often cannot see a person standing close to the load, so the warning has to reach the people on foot first.</p>",
 guide=[("Where to post","<ul><li>At aisle entrances where forklifts and people share the floor.</li><li>At crossings by doors, break rooms, restrooms and time clocks, on both sides of the crossing.</li><li>At blind corners and rack ends, next to a convex mirror.</li><li>At battery charging and propane cylinder change areas.</li><li>At dock doors and dock plates.</li></ul>"),
        ("Standards to know","<p>OSHA 1910.178 covers powered industrial trucks: operator training, safe operation, and the charging and refueling areas, where smoking is prohibited. OSHA 1910.176 says permanent aisles and passageways used by mechanical handling equipment must be appropriately marked. Signs work together with floor marking, mirrors and a written traffic plan.</p>")],
 faq=[("Where should a pedestrian crossing sign go?","On both sides of the crossing facing people on foot, plus a sign facing the forklift lane so operators expect people there."),
      ("Can you add our speed limit or lane rules?","Yes. Custom signs are priced close to catalog signs.")],
 kits=[("Forklift traffic zone kit, 8 signs","/products/forklift-traffic-zone-sign-kit-8-signs"),("Forklift battery charging area kit, 8 signs","/products/forklift-battery-charging-area-sign-kit-8-signs"),("Warehouse sign kits","/collections/warehouse-sign-kits")],
 page=("/pages/forklift-safety-guide","Forklift and powered industrial truck compliance guide")),

dict(handle="cgap-safety-lockout-tagout", existing=True, id="gid://shopify/Collection/465116037364", title="Lockout/Tagout (LOTO) Signs",
 inc=["Lockout","Lock Out","Tagout","Tag Out","Zero Energy","Isolation Point","Energy Isolation"], exc=[],
 guide=[("Where lockout signs go","<ul><li>At main disconnects and every energy isolation point.</li><li>On machines with more than one energy source: electric, hydraulic, pneumatic, gravity or stored pressure.</li><li>At the lockout station where locks and tags are kept.</li><li>Where workers clear jams, clean, change blades or reach into the machine.</li></ul>"),
        ("What the standard requires","<p>OSHA 1910.147 requires written energy control procedures, training and periodic inspections. Tags must warn against hazardous conditions with a legend such as Do Not Start, Do Not Open, Do Not Close, Do Not Energize or Do Not Operate. A sign at the equipment reminds people that the procedure applies and where the isolation points are. It does not replace locks, tags or the written procedure.</p>")],
 faq=[("Is a sign the same as a lockout tag?","No. A tag goes on the isolating device during service. A sign is a permanent reminder at the equipment. Most programs use both."),
      ("Can you put our machine number or isolation points on a sign?","Yes. Custom signs are priced close to catalog signs.")],
 kits=[("Lockout points kit, 8 signs","/products/lockout-points-sign-kit-8-signs"),("Maintenance and lockout kit, 8 signs","/products/maintenance-and-lockout-sign-kit-8-signs"),("Manufacturing plant sign kits","/collections/manufacturing-plant-sign-kits")],
 page=("/pages/lockout-tagout-guide","Lockout/tagout compliance guide")),

dict(handle="pinch-point-signs", title="Pinch Point Signs",
 seo=("Pinch Point Signs | Nip Point and Crush Hazard Warnings | CGAP", "Pinch point and nip point warning signs for conveyors, rollers, doors, hatches and lift gates. 8x12 rust-resistant aluminum, made in USA."),
 inc=["Pinch Point","Pinch Hazard","Nip Point","In-Running Nip","Crush Point","Crush Hazard"], exc=[],
 intro="<p>Pinch point and nip point warnings for conveyors, rollers, gears, chains, doors, hatches, lift gates and hinged covers. Most are small, specific CAUTION signs placed right at the spot where fingers and hands get caught.</p>",
 guide=[("Where to post","<ul><li>Belt and roller nips, chain and sprocket drives.</li><li>Closing doors, gates, hatches and hinged lids.</li><li>Scissor lifts, dock levelers and lift tables.</li><li>Clamps, fixtures and presses where hands load parts.</li></ul><p>Put the sign where someone sees it from the spot where they would reach in.</p>"),
        ("Signs and guards","<p>OSHA 1910.212 requires guarding for hazards such as in-running nip points and rotating parts. A sign does not replace a guard. It marks the hazards that remain, like a door edge or a hatch lid, and reminds people not to reach past a guard.</p>")],
 faq=[("CAUTION or WARNING?","CAUTION fits minor to moderate injury such as pinched fingers. Use WARNING or DANGER where the point can crush or amputate."),
      ("Do you have a conveyor kit?","Yes. The conveyor kits cover drives, nips, crossovers and emergency stops.")],
 kits=[("Conveyor system kit, 8 signs","/products/conveyor-system-sign-kit-8-signs"),("Conveyor and sortation kit, 8 signs","/products/conveyor-and-sortation-sign-kit-8-signs"),("Manufacturing plant sign kits","/collections/manufacturing-plant-sign-kits")],
 page=("/pages/machine-guarding-guide","Machine guarding compliance guide")),

dict(handle="cgap-safety-fall-protection", existing=True, id="gid://shopify/Collection/465115152628", title="Fall Hazard & Fall Protection Signs",
 inc=["Fall Hazard","Fall Protection","Open Edge","Unprotected Edge","Floor Opening","Open Hole","Tie Off","Tie-Off","Guardrail","Leading Edge","Roof Edge","Skylight","Fall Arrest","Anchor Point"], exc=[],
 guide=[("Where to post","<ul><li>Roof access doors and hatches, and along roof edges.</li><li>Floor and roof openings and skylights.</li><li>Open-sided platforms, mezzanine gates and dock edges.</li><li>Anchor points and fall protection gear stations.</li><li>Ladder and scaffold access points.</li></ul>"),
        ("Standards to know","<p>In general industry, OSHA 1910.28 requires fall protection at 4 feet and covers holes, skylights and open-sided floors. In construction, 1926.501 sets the trigger at 6 feet. Signs mark the edge and remind people to tie off. They support guardrails, covers and personal fall arrest systems, not replace them.</p>")],
 faq=[("Can a sign be used instead of a guardrail?","No. Use signs to mark the hazard and the rule, along with the physical protection the standard calls for."),
      ("Do you make roof access signs?","Yes. Roof edge, skylight and tie-off signs are in this collection, and the roof kits bundle them.")],
 kits=[("Scaffold and fall protection kit, 8 signs","/products/scaffold-and-fall-protection-sign-kit-8-signs"),("Roof anchor and davit kit, 8 signs","/products/roof-anchor-and-davit-sign-kit-8-signs"),("Roof and rooftop equipment kit, 8 signs","/products/roof-and-rooftop-equipment-sign-kit-8-signs")],
 page=("/pages/fall-protection-compliance-guide","Fall protection compliance guide")),

dict(handle="hot-work-welding-signs", title="Hot Work and Welding Signs",
 seo=("Hot Work and Welding Signs | Hot Work Permit, Fire Watch | CGAP", "Hot work permit, fire watch, welding area and oxy-fuel cylinder signs for shops, plants and job sites. 8x12 aluminum, made in USA."),
 inc=["Hot Work","Welding","Fire Watch","Cutting Torch","Torch Cutting","Oxy-Fuel","Grinding Sparks","Hot Sparks","Brazing","Plasma Cut","Weld Spatter","Welder"], exc=[],
 intro="<p>Signs for welding, cutting, brazing and other hot work: hot work permit areas, fire watch, welding screens and curtains, oxy-fuel cylinders and the places where sparks can reach combustibles.</p>",
 guide=[("Where to post","<ul><li>Welding bays, booths and screens.</li><li>Areas where hot work needs a permit, and areas where it is not allowed.</li><li>Near combustibles, dust or flammable vapor.</li><li>Fire watch stations and extinguisher points.</li><li>Oxy-fuel cylinder storage and carts.</li></ul>"),
        ("Standards to know","<p>OSHA 1910.252 covers fire prevention for welding and cutting, including inspecting the area and authorizing the work, preferably with a written permit, and a fire watch that in many cases stays at least half an hour after the work ends. NFPA 51B is the common reference for hot work permit programs. Construction work falls under 29 CFR 1926 Subpart J.</p>")],
 faq=[("Do you make hot work permit signs?","Yes, several, and we make custom versions with your permit process or contact."),
      ("Who buys these?","Fab shops, plants, shipyards, refineries, maintenance departments and contractors.")],
 kits=[("Welding bay kit, 8 signs","/products/welding-bay-sign-kit-8-signs"),("Welding and forge lab kit, 8 signs","/products/welding-and-forge-lab-sign-kit-8-signs"),("Metal shop sign kits","/collections/metal-shop-sign-kits")],
 page=None),
]
TITLE={x['handle']:x['title'] for x in H}
TITLE.update({'cgap-safety-machine-guarding':'Machine Guarding & Moving Parts Signs','loading-dock-warehouse-signs':'Loading Dock and Warehouse Signs','combustible-dust-signs':'Combustible Dust Signs','arc-flash-signs':'Arc Flash Signs','confined-space-signs':'Confined Space Signs','battery-energy-storage-signs':'Battery Energy Storage (BESS) Signs'})
REL={
 'forklift-pedestrian-signs':['loading-dock-warehouse-signs','pinch-point-signs','battery-energy-storage-signs'],
 'cgap-safety-lockout-tagout':['pinch-point-signs','cgap-safety-machine-guarding','arc-flash-signs','confined-space-signs'],
 'pinch-point-signs':['cgap-safety-lockout-tagout','cgap-safety-machine-guarding','forklift-pedestrian-signs'],
 'cgap-safety-fall-protection':['hot-work-welding-signs','confined-space-signs','loading-dock-warehouse-signs'],
 'hot-work-welding-signs':['combustible-dust-signs','cgap-safety-fall-protection','confined-space-signs'],
}
def guide(x):
    o=[f"<h2>{html.escape(h)}</h2>{b}" for h,b in x['guide']]
    o.append('<div class="cgap-hg__kits"><h3>Signing a whole site?</h3><p>Our kits put every sign one area needs in a single order, priced below buying the same signs one at a time.</p><ul>'+''.join(f'<li><a href="{u}">{html.escape(l)}</a></li>' for l,u in x['kits'])+'</ul></div>')
    o.append('<h2>Common questions</h2>'+''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in x['faq']))
    if x.get('page'): o.append(f'<p class="cgap-hg__guide">Full guide: <a href="{x["page"][0]}">{html.escape(x["page"][1])}</a></p>')
    o.append('<p class="cgap-hg__related"><strong>Related hazards:</strong> '+' · '.join(f'<a href="/collections/{r}">{html.escape(TITLE[r])}</a>' for r in REL[x['handle']])+'</p>')
    g='\n'.join(o); assert '—' not in g and '–' not in g; return g
def conds(x):
    c=[{"productTitle":{"matchType":"ANY","relation":"CONTAINS","values":x['inc']}}]
    if x['exc']: c.append({"productTitle":{"matchType":"ALL","relation":"DOES_NOT_CONTAIN","values":x['exc']}})
    return {"source":{"title":x['title']+" (title match)","targetType":"PRODUCTS","inclusion":{"matchType":"ALL","conditions":c}}}
create={}; update={}
for i,x in enumerate(H):
    mf=[{"namespace":"custom","key":"hazard_guide","type":"multi_line_text_field","value":guide(x)}]
    if x.get('existing'):
        update[f'u{len(update)}']={"id":x['id'],"title":x['title'],"metafields":mf,"sourcesToCreate":[conds(x)]}
    else:
        assert len(x['seo'][0])<=70 and len(x['seo'][1])<=160, x['handle']
        create[f'c{len(create)}']={"title":x['title'],"handle":x['handle'],"descriptionHtml":x['intro'],"seo":{"title":x['seo'][0],"description":x['seo'][1]},"sortOrder":"BEST_SELLING","metafields":mf,"sources":[{"source":{"title":x['title'],"targetType":"PRODUCTS","inclusion":conds(x)['source']['inclusion']}}]}
json.dump(create,open('set2_create.json','w'),ensure_ascii=False,separators=(',',':'))
json.dump(update,open('set2_update.json','w'),ensure_ascii=False,separators=(',',':'))
print(len(open('set2_create.json').read()), len(open('set2_update.json').read()))
