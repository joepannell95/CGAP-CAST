import json, html, re, sys
sys.path.insert(0,'.')
from hubs import HUBS
H={h['handle']:h for h in HUBS}

COND={
 'mri-quench-vent-signs':(["Quench Vent","MRI Quench","Magnet Quench","Cryogen Vent","Quench Pipe","Post-Quench","Post Quench","Quench Button"],[]),
 'mri-magnetic-field-signs':(["Magnetic Field","Pacemaker","Ferromagnetic","MRI Magnet","Magnet Room","5 Gauss","Gauss Line","Magnet Is On","MRI Zone","Zone IV","MRI Scan Room","MRI Suite","NMR"],["Degauss"]),
 'electric-shock-drowning-signs':(["Shock Drowning","Marina Shore Power","Shore Power Pedestal","Dock Power","Dock Electrical","Marina Electrical","Energize the Water","Energized Water","Boat Lift Wiring","Boat Lift Electrical"],[]),
 'battery-energy-storage-signs':(["Energy Storage","BESS","Battery Storage Container","Battery Room","Thermal Runaway"],[]),
 'ev-service-high-voltage-signs':(["EV Service","Electric Vehicle","EV Battery","Hybrid Vehicle","EV Bay","EV Charging","EV Charger","High-Voltage Battery","High Voltage Battery"],[]),
 'e-bike-lithium-battery-charging-signs':(["E-Bike","E-Scooter","Lithium Battery","Lithium-Ion Battery","Battery Charging Room","Scooter Charging","Bike Charging"],[]),
 'drowning-hazard-open-water-signs':(["Drown","Deep Water","Thin Ice","Swift Water","Water Hazard","Fall Into Water","Spillway","Low Head Dam","Low-Head Dam"],[]),
 'blasting-area-signs':(["Blasting","Blast Zone","Blast Area","Blast Site","Blast Hole","Blasthole","Explosives","Detonator","Magazine Door","Magazine Perimeter","Powder Magazine","Misfire","Blast Guard","Turn Off Radio","Blasting Cap"],
   ["Abrasive","Sandblast","Shot Blast","Soda Blast","Media Blast","Dry Ice","Water Blast","Bead Blast","Grit Blast","Blast Freezer","Blast Chiller","Blast Pot","Blast Cabinet","Blast Nozzle","Blast Room","Blast Hose","Hydro Blast","Hydroblast","Ice Blast","Blast Gate","Tool Magazine","Foundries","Nailer","Stapler"]),
 'assembly-point-signs':(["Assembly Point","Assembly Area","Muster"],[]),
 'hydrogen-sulfide-h2s-signs':(["Hydrogen Sulfide","H2S"],[]),
 'ammonia-refrigeration-signs':(["Ammonia"],[]),
 'combustible-dust-signs':(["Combustible Dust","Dust Explosion","Dust Collector","Explosion Vent","Dust Cloud","Dust Can Explode","Explosive Dust"],[]),
 'oxygen-deficiency-cryogenic-signs':(["Liquid Nitrogen","Cryogenic","Asphyxia","Inert Gas","Nitrogen Purge","Low Oxygen","Oxygen-Deficient","Oxygen Deficient","Dewar","Lacks Oxygen","Lack Oxygen"],[]),
 'rf-radiation-antenna-signs':(["Antenna","RF Energy","Radio Frequency","RF Field","RF Radiation","RF Exposure","Radar"],[]),
 'grain-bin-entry-signs':(["Grain Bin","Engulf","Bin Entry","Sweep Auger","Flowing Grain","Bridged Grain","Entrapment","Grain Can Bury","Grain Leg","Bin Door"],[]),
 'chlorine-hypochlorite-signs':(["Chlorine","Hypochlorite","Chlorinat"],[]),
 'carbon-monoxide-signs':(["Carbon Monoxide"],[]),
 'carbon-dioxide-co2-signs':(["Carbon Dioxide","CO2"],[]),
 'silica-dust-signs':(["Silica"],[]),
 'hydrofluoric-acid-signs':(["Hydrofluoric","HF Acid","HF Alkylation"],[]),
}
TITLE={'drowning-hazard-open-water-signs':"Drowning Hazard and Deep Water Signs",'rf-radiation-antenna-signs':"RF and Antenna Site Signs"}
K=lambda *a:list(a)
KITS={
 'electric-shock-drowning-signs':K(("Boat dock and marina kit","/products/boat-dock-and-marina-safety-sign-kit"),("Marina and fuel dock kit, 8 signs","/products/marina-and-fuel-dock-sign-kit-8-signs"),("Port and marine sign kits","/collections/port-and-marine-sign-kits")),
 'battery-energy-storage-signs':K(("Battery energy storage container kit, 8 signs","/products/battery-energy-storage-container-sign-kit-8-signs"),("UPS and battery room kit, 8 signs","/products/ups-and-battery-room-sign-kit-8-signs"),("Battery and EV sign kits","/collections/battery-and-ev-sign-kits")),
 'ev-service-high-voltage-signs':K(("Battery and EV service kit, 8 signs","/products/battery-and-ev-service-sign-kit-8-signs"),("EV charging station kit, 8 signs","/products/ev-charging-station-sign-kit-8-signs"),("Auto shop sign kits","/collections/auto-shop-sign-kits")),
 'e-bike-lithium-battery-charging-signs':K(("Lithium battery storage and recycling kit, 8 signs","/products/lithium-battery-storage-and-recycling-sign-kit-8-signs"),("Apartment and property management kit","/products/apartment-and-property-management-safety-sign-kit"),("Facility sign kits","/collections/facility-sign-kits")),
 'drowning-hazard-open-water-signs':K(("Spillway and gates kit, 8 signs","/products/spillway-and-gates-sign-kit-8-signs"),("Public works sign kits","/collections/public-works-sign-kits"),("Dam and lock sign kits","/collections/dam-and-lock-sign-kits")),
 'blasting-area-signs':K(("Blast site kit, 8 signs","/products/blast-site-sign-kit-8-signs"),("Explosives magazine kit, 8 signs","/products/explosives-magazine-sign-kit-8-signs"),("Quarry and mine sign kits","/collections/quarry-and-mine-sign-kits")),
 'hydrogen-sulfide-h2s-signs':K(("Lift station kit, 8 signs","/products/lift-station-sign-kit-8-signs"),("Process module and H2S kit, 4 signs","/products/process-module-and-h2s-sign-kit-4-signs"),("Oil and gas sign kits","/collections/oil-and-gas-sign-kits")),
 'ammonia-refrigeration-signs':K(("Ammonia machine room kit, 8 signs","/products/ammonia-machine-room-sign-kit-8-signs"),("Ammonia valve station kit, 8 signs","/products/ammonia-valve-station-sign-kit-8-signs"),("Cold storage sign kits","/collections/cold-storage-sign-kits")),
 'combustible-dust-signs':K(("Bulk ingredient silo and dust kit, 8 signs","/products/bulk-ingredient-silo-and-dust-sign-kit-8-signs"),("Bagging and dust kit, 8 signs","/products/bagging-and-dust-sign-kit-8-signs"),("Food plant sign kits","/collections/food-plant-sign-kits")),
 'rf-radiation-antenna-signs':K(("Rooftop antenna site kit, 8 signs","/products/rooftop-antenna-site-sign-kit-8-signs"),("Tower base and compound kit, 8 signs","/products/tower-base-and-compound-sign-kit-8-signs"),("Telecom sign kits","/collections/telecom-sign-kits")),
 'grain-bin-entry-signs':K(("Grain bin kit, 8 signs","/products/farm-and-grain-grain-bin-sign-kit-8-signs"),("Grain elevator leg and pit kit, 8 signs","/products/grain-elevator-leg-and-pit-sign-kit-8-signs"),("Farm and grain sign kits","/collections/farm-and-grain-sign-kits")),
 'chlorine-hypochlorite-signs':K(("Chlorine and chemical feed room kit, 8 signs","/products/chlorine-chemical-feed-room-sign-kit-8-signs"),("Pool and spa chemical room kit, 6 signs","/products/pool-and-spa-chemical-room-sign-kit-6-signs"),("Water and wastewater kits","/collections/water-wastewater-sign-kits")),
 'carbon-monoxide-signs':K(("Boiler room kit, 8 signs","/products/boiler-room-sign-kit-8-signs"),("Generator yard kit, 8 signs","/products/generator-yard-sign-kit-8-signs"),("Mechanical room sign kits","/collections/mechanical-room-sign-kits")),
 'carbon-dioxide-co2-signs':K(("Fermentation cellar kit, 8 signs","/products/fermentation-cellar-sign-kit-8-signs"),("Kitchen gas and CO2 kit, 8 signs","/products/kitchen-gas-and-co2-sign-kit-8-signs"),("Clean agent and CO2 system kit, 8 signs","/products/clean-agent-and-co2-system-sign-kit-8-signs")),
 'silica-dust-signs':K(("Silica dust control kit, 6 signs","/products/silica-dust-control-sign-kit-6-signs"),("Stone shop sign kits","/collections/stone-shop-sign-kits"),("Construction sign kits","/collections/construction-sign-kits")),
 'hydrofluoric-acid-signs':K(("Wet bench and acid kit, 8 signs","/products/wet-bench-and-acid-sign-kit-8-signs"),("Laboratory sign kits","/collections/laboratory-sign-kits")),
}
ADDKIT={
 'loading-dock-warehouse-signs':("Warehouse loading dock kit, 8 signs","/products/warehouse-loading-dock-sign-kit-8-signs"),
 'arc-flash-signs':("Electrical switchgear room kit, 8 signs","/products/electrical-switchgear-room-sign-kit-8-signs"),
 'laser-safety-signs':("Laser and radiation lab kit, 8 signs","/products/laser-and-radiation-lab-sign-kit-8-signs"),
 'radiation-safety-signs':("Laser and radiation lab kit, 8 signs","/products/laser-and-radiation-lab-sign-kit-8-signs"),
}
REL={
 'mri-quench-vent-signs':['mri-safety-signs','mri-magnetic-field-signs','oxygen-deficiency-cryogenic-signs','radiation-safety-signs'],
 'mri-safety-signs':['mri-quench-vent-signs','mri-magnetic-field-signs','radiation-safety-signs','laser-safety-signs'],
 'mri-magnetic-field-signs':['mri-safety-signs','mri-quench-vent-signs','radiation-safety-signs','rf-radiation-antenna-signs'],
 'electric-shock-drowning-signs':['drowning-hazard-open-water-signs','arc-flash-signs','battery-energy-storage-signs'],
 'battery-energy-storage-signs':['ev-service-high-voltage-signs','e-bike-lithium-battery-charging-signs','arc-flash-signs'],
 'ev-service-high-voltage-signs':['battery-energy-storage-signs','e-bike-lithium-battery-charging-signs','arc-flash-signs','carbon-monoxide-signs'],
 'e-bike-lithium-battery-charging-signs':['battery-energy-storage-signs','ev-service-high-voltage-signs','assembly-point-signs'],
 'drowning-hazard-open-water-signs':['electric-shock-drowning-signs','confined-space-signs','chlorine-hypochlorite-signs'],
 'blasting-area-signs':['assembly-point-signs','silica-dust-signs','call-811-before-digging-signs'],
 'assembly-point-signs':['ammonia-refrigeration-signs','hydrogen-sulfide-h2s-signs','blasting-area-signs','chlorine-hypochlorite-signs'],
 'hydrogen-sulfide-h2s-signs':['confined-space-signs','oxygen-deficiency-cryogenic-signs','carbon-monoxide-signs','chlorine-hypochlorite-signs'],
 'ammonia-refrigeration-signs':['assembly-point-signs','oxygen-deficiency-cryogenic-signs','carbon-dioxide-co2-signs','loading-dock-warehouse-signs'],
 'combustible-dust-signs':['grain-bin-entry-signs','silica-dust-signs','danger-regulated-area'],
 'oxygen-deficiency-cryogenic-signs':['carbon-dioxide-co2-signs','confined-space-signs','mri-quench-vent-signs','hydrogen-sulfide-h2s-signs'],
 'rf-radiation-antenna-signs':['radiation-safety-signs','arc-flash-signs','mri-magnetic-field-signs'],
 'grain-bin-entry-signs':['combustible-dust-signs','confined-space-signs','oxygen-deficiency-cryogenic-signs'],
 'chlorine-hypochlorite-signs':['hydrogen-sulfide-h2s-signs','confined-space-signs','hydrofluoric-acid-signs','assembly-point-signs'],
 'carbon-monoxide-signs':['carbon-dioxide-co2-signs','oxygen-deficiency-cryogenic-signs','confined-space-signs'],
 'carbon-dioxide-co2-signs':['carbon-monoxide-signs','oxygen-deficiency-cryogenic-signs','ammonia-refrigeration-signs'],
 'silica-dust-signs':['danger-regulated-area','combustible-dust-signs','blasting-area-signs'],
 'hydrofluoric-acid-signs':['chlorine-hypochlorite-signs','danger-regulated-area','laser-safety-signs'],
 'call-811-before-digging-signs':['confined-space-signs','arc-flash-signs','blasting-area-signs'],
 'confined-space-signs':['hydrogen-sulfide-h2s-signs','oxygen-deficiency-cryogenic-signs','grain-bin-entry-signs','carbon-monoxide-signs'],
 'laser-safety-signs':['radiation-safety-signs','mri-safety-signs','hydrofluoric-acid-signs'],
 'danger-regulated-area':['silica-dust-signs','hydrofluoric-acid-signs','combustible-dust-signs'],
 'loading-dock-warehouse-signs':['ammonia-refrigeration-signs','battery-energy-storage-signs','assembly-point-signs'],
 'radiation-safety-signs':['laser-safety-signs','mri-safety-signs','rf-radiation-antenna-signs'],
 'arc-flash-signs':['battery-energy-storage-signs','electric-shock-drowning-signs','call-811-before-digging-signs'],
}
def t(h): return TITLE.get(h, H[h]['title'])
def guide_html(h):
    x=H[h]; o=[]
    for hd,body in x['guide']: o.append(f"<h2>{html.escape(hd)}</h2>{body}")
    kits=list(KITS.get(h,x['kits']))
    if h in ADDKIT: kits.insert(0,ADDKIT[h])
    o.append('<div class="cgap-hg__kits"><h3>Signing a whole site?</h3><p>Our kits put every sign one area needs in a single order, priced below buying the same signs one at a time.</p><ul>'+''.join(f'<li><a href="{u}">{html.escape(l)}</a></li>' for l,u in kits)+'</ul></div>')
    o.append('<h2>Common questions</h2>'+''.join(f'<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>' for q,a in x['faq']))
    if x.get('page'): o.append(f'<p class="cgap-hg__guide">Full guide: <a href="{x["page"][0]}">{html.escape(x["page"][1])}</a></p>')
    o.append('<p class="cgap-hg__related"><strong>Related hazards:</strong> '+' · '.join(f'<a href="/collections/{r}">{html.escape(t(r))}</a>' for r in REL[h])+'</p>')
    return '\n'.join(o)
out=[]
for x in HUBS:
    h=x['handle']; g=guide_html(h)
    assert '—' not in g and '–' not in g, h
    rec=dict(handle=h,title=t(h),existing=bool(x.get('existing')),guide=g)
    if not x.get('existing'):
        inc,exc=COND[h]
        conds=[{"productTitle":{"matchType":"ANY","relation":"CONTAINS","values":inc}}]
        if exc: conds.append({"productTitle":{"matchType":"ALL","relation":"DOES_NOT_CONTAIN","values":exc}})
        rec['input']={"title":t(h),"handle":h,"descriptionHtml":x['intro'],"seo":{"title":x['seo'][0],"description":x['seo'][1]},"sortOrder":"BEST_SELLING",
          "metafields":[{"namespace":"custom","key":"hazard_guide","type":"multi_line_text_field","value":g}],
          "sources":[{"source":{"title":t(h),"targetType":"PRODUCTS","inclusion":{"matchType":"ALL","conditions":conds}}}]}
        assert len(x['seo'][0])<=70, (h,len(x['seo'][0])); assert len(x['seo'][1])<=160,(h,len(x['seo'][1]))
    out.append(rec)
json.dump(out,open('hubs_out.json','w'),indent=1)
print(len(out), sum(1 for r in out if not r['existing']), max(len(r['guide']) for r in out))
allk=set()
for x in HUBS:
    for l,u in list(KITS.get(x['handle'],x['kits']))+([ADDKIT[x['handle']]] if x['handle'] in ADDKIT else []): allk.add(u)
print(sorted(u for u in allk if u.startswith('/products/')))
