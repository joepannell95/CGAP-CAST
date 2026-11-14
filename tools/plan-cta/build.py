exec(open('map.py').read().split('import json')[0])
PAGES = {
 'farm-grain-feed-safety-signs':'farm','restaurant-commercial-kitchen-safety-signs':'kitchen','auto-repair-shop-safety-signs':'auto',
 'car-wash-safety-signs':'carwash','brewery-winery-safety-signs':'brewery','construction-site-safety-signs':'construction',
 'food-processing-plant-safety-signs':'mfg','oil-gas-hydrogen-safety-signs':'oil_chem','metal-fabrication-foundry-safety-signs':'mfg',
 'laboratory-biotech-pharma-safety-signs':'lab','cold-storage-ammonia-refrigeration-safety-signs':'cold','sawmill-pulp-paper-mill-safety-signs':'woodshop',
 'propane-natural-gas-pipeline-safety-signs':'oil_chem','school-shop-class-theater-safety-signs':'school','data-center-server-room-safety-signs':'datacenter',
 'lithium-battery-energy-storage-ev-safety-signs':'utility','chemical-plant-storage-safety-signs':'oil_chem','mining-quarry-asphalt-plant-safety-signs':'quarry',
 'industry-water-wastewater-utilities':'water','industry-electric-telecom-utilities':'utility','industry-healthcare-imaging-labs':'lab',
 'industry-manufacturing-industrial-plants':'mfg','industry-warehousing-logistics':'warehouse','industry-marinas-waterfront':'marina',
 'industry-property-management-multifamily':'school','park-shooting-range-venue-safety-signs':'school','industry-municipalities-public-works':'water',
 'waste-recycling-transfer-station-safety-signs':'mfg',
}
# Name overrides for pages whose audience differs from the plan's site label
PNAME = {'industry-property-management-multifamily':'an apartment complex or managed property','park-shooting-range-venue-safety-signs':'a park, range or venue',
 'industry-municipalities-public-works':'a public works or water site','waste-recycling-transfer-station-safety-signs':'a recycling or transfer station',
 'food-processing-plant-safety-signs':'a food processing plant','metal-fabrication-foundry-safety-signs':'a fab shop or foundry',
 'lithium-battery-energy-storage-ev-safety-signs':'a battery or EV charging site','propane-natural-gas-pipeline-safety-signs':'a propane or gas site',
 'school-shop-class-theater-safety-signs':'a school shop or theater'}
L=["{%- comment -%}",
"  Plan my site box. Built by tools/plan-cta/build.py; edit there.",
"  Params: key (a page handle), mode ('product' looks at product.collections). Default: collection.handle.",
"{%- endcomment -%}",
"{%- liquid","  assign pf = ''","  assign pn = ''",
"  if key != blank","    assign keys = key",
"  elsif mode == 'product'","    assign keys = ''",
"    assign s = ''",
"    for t in product.tags","      if t contains 'Sector: '","        assign s = t | remove_first: 'Sector: ' | downcase | prepend: ' ' | append: ' '","        break","      endif","    endfor",
"    if s != ''"]+open('sector_block.liquid').read().split("\n")+["    endif"]+["    if pf == ''", '      for t in product.tags', "        if t contains 'Industry: '", '          case t', "            when 'Industry: Restaurants and Bars'", "              assign pf = 'kitchen'", "            when 'Industry: Hospitals and Healthcare'", "              assign pf = 'lab'", "            when 'Industry: Labs and Research'", "              assign pf = 'lab'", "            when 'Industry: Schools and Universities'", "              assign pf = 'school'", "            when 'Industry: Apartments and Residential'", "              assign pf = 'school'", "            when 'Industry: Agriculture and Farms'", "              assign pf = 'farm'", "            when 'Industry: Automotive and Fleet'", "              assign pf = 'auto'", "            when 'Industry: Warehouses and Logistics'", "              assign pf = 'warehouse'", "            when 'Industry: Construction and Trades'", "              assign pf = 'construction'", "            when 'Industry: Manufacturing and Industrial'", "              assign pf = 'mfg'", "            when 'Industry: Food and Beverage Production'", "              assign pf = 'mfg'", "            when 'Industry: Oil Gas Mining and Chemical'", "              assign pf = 'oil_chem'", "            when 'Industry: Energy Utilities and Telecom'", "              assign pf = 'utility'", "            when 'Industry: Offices and Commercial Property'", "              assign pf = 'office'", "            when 'Industry: Retail and Personal Services'", "              assign pf = 'retail'", '          endcase', '          break', '        endif', '      endfor', '    endif']+[
"  else","    assign keys = collection.handle","  endif",
"  assign keys = keys | split: ','",
"  for k in keys","    case k"]
for code,(name,hs) in M.items():
    L.append("      when "+", ".join(f"'{h}'" for h in hs.split()))
    L.append(f"        assign pf = '{code}'"); L.append(f"        assign pn = '{name}'")
for h,code in PAGES.items():
    L.append(f"      when '{h}'"); L.append(f"        assign pf = '{code}'"); L.append(f"        assign pn = '{PNAME.get(h, M[code][0])}'")
L+=["    endcase","    if pf != ''","      break","    endif","  endfor",
"  if mode == 'product' and pf != ''","    case pf"]+sum([[f"      when '{c}'", f"        assign pn = '{M[c][0]}'"] for c in M],[])+["    endcase","  endif","-%}","{%- if pf != '' -%}",
'''<div class="cgap-plan-cta{% if mode == 'product' %} cgap-plan-cta--p{% endif %}">
  <div class="cgap-plan-cta__text">
    {%- if mode == 'product' -%}
    <strong>Outfitting {{ pn }}?</strong>
    <span>Get the full sign list for the whole site, room by room, with quantities and where each sign goes. Takes about two minutes.</span>
    {%- else -%}
    <strong>Setting up {{ pn }}?</strong>
    <span>Answer a few questions and get every sign you need, room by room, with quantities and where each one goes. Takes about two minutes.</span>
    {%- endif -%}
  </div>
  <a class="cgap-plan-cta__btn" href="/pages/site-sign-plan?f={{ pf }}">Plan my site</a>
</div>
<style>
.cgap-plan-cta{display:flex;align-items:center;justify-content:space-between;gap:1.6rem;margin:1.6rem 0;padding:1.4rem 1.8rem;border:1px solid #bcd3c1;border-left:8px solid #E0731A;border-radius:6px;background:#eef4ef;max-width:84rem;box-sizing:border-box}
.cgap-plan-cta__text{display:flex;flex-direction:column;gap:.4rem;font-size:1.5rem;line-height:1.4;color:#222}
.cgap-plan-cta__text strong{font-size:1.7rem;color:#173F24}
.cgap-plan-cta__btn{flex:0 0 auto;display:inline-block;padding:1.1rem 2rem;background:#E0731A;color:#fff !important;font-weight:700;font-size:1.5rem;text-decoration:none !important;border-radius:4px;white-space:nowrap}
.cgap-plan-cta__btn:hover{background:#c4610f}
.cgap-plan-cta--p{flex-direction:column;align-items:stretch;padding:1.2rem 1.4rem}
.cgap-plan-cta--p .cgap-plan-cta__text{font-size:1.35rem}
.cgap-plan-cta--p .cgap-plan-cta__text strong{font-size:1.5rem}
.cgap-plan-cta--p .cgap-plan-cta__btn{text-align:center}
@media screen and (max-width:749px){.cgap-plan-cta{flex-direction:column;align-items:stretch}.cgap-plan-cta__btn{text-align:center}}
</style>''',"{%- endif -%}"]
open('/home/claude/cgap-cast/theme/snippets/cgap-plan-cta.liquid','w').write("\n".join(L)+"\n")
print(len("\n".join(L)))
