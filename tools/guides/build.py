import json, urllib.parse
q=lambda s:'/search?q='+urllib.parse.quote_plus(s)+'&type=product'
G=[
dict(handle='construction-site-sign-checklist',f='construction',coll='construction-and-trades-signs',
 title='Construction Site Sign Checklist: Every Safety Sign a Jobsite Needs',
 seo='Construction Site Safety Sign Checklist | CGAP Safety',
 desc='A walk-through checklist of the safety signs a construction jobsite needs, from the site entrance to the crane zone, with OSHA 1926.200 basics.',
 intro='Walk your jobsite from the gate in and check off each area below. Most sites need 10 to 20 signs, and the gaps usually show up at the entrance, around overhead work and at fuel and electrical setups.',
 areas=[('Site entrance and fence line',['Hard hat area','Authorized personnel only','All visitors check in','PPE required beyond this point','No trespassing construction site']),
 ('Overhead work, cranes and lifts',['Overhead hazard','Crane swing radius','Stay clear of suspended loads','Aerial lift in use']),
 ('Excavations, trenches and fall edges',['Open excavation','Fall hazard keep back','Floor opening','Guardrail required']),
 ('Fuel, power and hot work',['No smoking flammable','Fuel storage area','High voltage keep out','Hot work area']),
 ('Job trailer and first aid',['First aid station','Fire extinguisher','Emergency contact numbers','Eye wash station'])],
 rules=['OSHA 1926.200 covers accident prevention signs on construction sites. DANGER signs mark immediate hazards and CAUTION signs mark potential hazards.','Signs must be visible when work is going on and removed or covered once the hazard is gone.','Use signs alongside barricades and training, not in place of them.'],
 faq=[('How many signs does a small jobsite need?','Most small residential and light commercial sites need 10 to 20. Start with the entrance, PPE, overhead and fall hazard signs, then add fuel and electrical signs where they apply.'),('Are aluminum signs better than plastic on a jobsite?','Aluminum holds up to weather, sun and being moved from site to site, and it can be screwed or zip tied to fence and posts.')]),
dict(handle='warehouse-safety-sign-checklist',f='warehouse',coll='warehouses-and-logistics-signs',
 title='Warehouse Safety Sign Checklist: Signs Every Warehouse and Distribution Center Needs',
 seo='Warehouse Safety Sign Checklist | CGAP Safety',
 desc='Checklist of the warehouse safety signs you need for forklift traffic, loading docks, racking, battery charging and exits, with OSHA basics.',
 intro='Warehouses mix people and forklifts in tight space, so most signs go where those two meet. Walk the building in this order and check off what you already have.',
 areas=[('Forklift traffic and aisles',['Forklift traffic','Pedestrians stay in walkway','Stop look both ways','Speed limit forklift']),
 ('Loading docks',['Open dock edge fall hazard','Chock wheels','Dock plate keep clear','Trailer must be secured']),
 ('Racking and storage',['Do not climb racking','Maximum load rack','Keep aisles clear','Heavy items low']),
 ('Battery charging and maintenance',['Battery charging area','No smoking','Eye wash station','Lead acid battery']),
 ('Exits and fire equipment',['Fire extinguisher','Do not block exit','Keep clear electrical panel','Emergency exit'])],
 rules=['OSHA 1910.178 covers forklifts, and 1910.176 requires aisles and passageways be kept clear and marked where mechanical handling equipment is used.','Exit routes must be marked under 1910.37, and electrical panels need clear working space under 1910.303.','Battery charging areas need ventilation, fire protection and eyewash access where battery acid is handled.'],
 faq=[('Where should forklift signs go?','At every aisle end, pedestrian crossing, blind corner and doorway where forklifts and people share space.'),('Do loading docks need their own signs?','Yes. Dock edges, dock plates and trailer restraint rules are some of the most common warehouse injury spots.')]),
dict(handle='manufacturing-plant-sign-checklist',f='mfg',coll='manufacturing-and-industrial-signs',
 title='Manufacturing Plant Sign Checklist: Safety Signs for the Production Floor',
 seo='Manufacturing Plant Safety Sign Checklist | CGAP Safety',
 desc='Checklist of manufacturing plant safety signs for machines, lockout, PPE zones, chemicals, compressed air and electrical rooms, with OSHA basics.',
 intro='A production floor needs signs at each machine, each PPE zone change and each place energy is stored. Use this list area by area.',
 areas=[('Machines and moving parts',['Moving parts keep hands clear','Pinch point','Machine guard must be in place','Authorized operators only']),
 ('Lockout and maintenance',['Lockout tagout required','Do not operate','Energy isolation point','Stored energy']),
 ('PPE zones',['Hearing protection required','Safety glasses required','Steel toe boots required','Respirator required']),
 ('Chemicals and compressed gas',['Flammable storage','Corrosive','Compressed gas cylinders','Hazardous waste']),
 ('Electrical and utility rooms',['High voltage','Arc flash','Authorized personnel only','Keep clear electrical panel'])],
 rules=['OSHA 1910.145 sets the sign classes: DANGER for immediate hazards, CAUTION for potential hazards, and safety instruction signs for general practices.','Lockout tagout under 1910.147 requires energy control procedures. Signs remind workers but do not replace locks and tags.','Machine guarding is required under 1910.212. A sign never substitutes for a missing guard.'],
 faq=[('What color should machine warning signs be?','Use DANGER (red) where contact would cause serious injury right away, and CAUTION (yellow) for potential hazards like pinch points.'),('Do PPE signs need to be at every entrance?','Post them at each entrance to a zone where the PPE requirement changes, so people see it before they walk in.')]),
dict(handle='restaurant-kitchen-sign-checklist',f='kitchen',coll='restaurants-and-bars-signs',
 title='Restaurant Kitchen Sign Checklist: Safety and Health Signs for Commercial Kitchens',
 seo='Restaurant Kitchen Safety Sign Checklist | CGAP Safety',
 desc='Checklist of commercial kitchen signs: handwashing, hot surfaces, fryers, walk-in coolers, chemicals, gas shutoff and fire suppression.',
 intro='Health inspectors and new hires both look for the same handful of kitchen signs. Go station by station and check off what is already posted.',
 areas=[('Handwashing and food safety',['Employees must wash hands','Hand sink only','Raw meat storage','Allergen awareness']),
 ('Cooking line',['Hot surface','Fryer hot oil','Hood fire suppression','Knife safety']),
 ('Walk-in cooler and freezer',['Walk in cooler','Keep door closed','Inside release','Slippery floor']),
 ('Dish area and chemicals',['Chemical storage','Do not mix chemicals','Eye wash station','Wet floor']),
 ('Gas, fire and exits',['Gas shut off','Fire extinguisher','Class K extinguisher','Do not block exit'])],
 rules=['Most state food codes require a handwashing sign at every hand sink used by food employees. Check your local health department code for exact wording.','Class K extinguishers are required for cooking with combustible oils and fats under NFPA 10, and a placard near the hood helps staff use it right.','Chemical containers need labels under OSHA 1910.1200 (HazCom), and a storage sign keeps chemicals away from food.'],
 faq=[('Is a handwashing sign required?','In most states, yes, at each hand sink employees use. The exact rule comes from your state food code.'),('What signs do walk-in coolers need?','A keep door closed sign outside, and an inside release or emergency exit sign inside so nobody gets trapped.')]),
dict(handle='farm-safety-sign-checklist',f='farm',coll='agriculture-and-farms-signs',
 title='Farm Safety Sign Checklist: Signs for Barns, Grain Bins, Livestock and Equipment',
 seo='Farm Safety Sign Checklist | CGAP Safety',
 desc='Checklist of farm safety signs for grain bins, livestock pens, chemicals, fuel tanks, equipment sheds and visitor entrances.',
 intro='Farms have hazards most visitors never think about: grain bins, bulls, chemicals and running equipment. Work through the property in this order.',
 areas=[('Farm entrance and visitors',['No trespassing private property','Farm equipment crossing','Visitors check in','Biosecurity no entry']),
 ('Grain bins and silos',['Grain bin engulfment','Confined space','Do not enter bin while unloading','Lockout auger']),
 ('Livestock',['Beware of bull','Keep gate closed','Electric fence','Livestock handling area']),
 ('Chemicals and fuel',['Pesticide storage','No smoking fuel','Anhydrous ammonia','Restricted entry interval']),
 ('Shop and equipment',['PTO shaft hazard','Moving parts','Hearing protection','Fire extinguisher'])],
 rules=['Grain handling rules in OSHA 1910.272 cover bin entry, and engulfment is one of the top causes of farm deaths.','The EPA Worker Protection Standard requires posting for certain pesticide applications and restricted entry intervals.','Fuel storage areas should be posted no smoking and kept clear of ignition sources.'],
 faq=[('Do family farms need safety signs?','OSHA rules mostly cover farms with hired workers, but signs at grain bins, bulls and chemicals protect family, visitors and delivery drivers too.'),('Which farm signs matter most?','Grain bin engulfment, livestock and chemical storage signs prevent the most serious injuries.')]),
]
def html(g):
    h=[f"<p>{g['intro']}</p>",f'<p><a href="/pages/site-sign-plan?f={g["f"]}" style="display:inline-block;background:#e8792b;color:#fff;padding:10px 18px;border-radius:4px;text-decoration:none;font-weight:bold">Plan my site for free</a></p>']
    for i,(a,signs) in enumerate(g['areas'],1):
        h.append(f'<h2>{i}. {a}</h2><ul>'+''.join(f'<li>&#9744; <a href="{q(s)}">{s} sign</a></li>' for s in signs)+'</ul>')
    h.append('<h2>Rules worth knowing</h2><ul>'+''.join(f'<li>{r}</li>' for r in g['rules'])+'</ul>')
    h.append('<p><em>This checklist is a starting point, not legal advice. Check the OSHA standard and your local code for your exact situation.</em></p>')
    h.append('<h2>Common questions</h2>'+''.join(f'<h3>{a}</h3><p>{b}</p>' for a,b in g['faq']))
    h.append(f'<h2>Shop the signs</h2><p>Browse every sign in <a href="/collections/{g["coll"]}">this collection</a>, or let the <a href="/pages/site-sign-plan?f={g["f"]}">site sign planner</a> build the full list for you. All CGAP signs are 8x12 rust-resistant aluminum, pre-drilled and made in the USA.</p>')
    return ''.join(h)
out=[{'handle':g['handle'],'title':g['title'],'body':html(g),'seo':g['seo'],'desc':g['desc']} for g in G]
json.dump(out,open('guides.json','w'))
for o in out: print(o['handle'],len(o['body']), '—' in o['body'])
