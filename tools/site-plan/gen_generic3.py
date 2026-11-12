import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (67,"NOTICE",["PUBLIC WATER SYSTEM","AUTHORIZED PERSONNEL","ONLY","REPORT TAMPERING"],"Public Water System Authorized Personnel Only","Report Tampering","","On well house, booster station and tank site gates and doors","Keeps the public out of drinking water facilities and asks people to report tampering"),
 (68,"WARNING",["PUMPS START","AUTOMATICALLY","WITHOUT WARNING","LOCK OUT BEFORE SERVICING"],"Pumps Start Automatically","Lock Out Before Servicing","","On pump rooms, well houses and pump control panels","Warns that pumps can start on level, pressure or remote signals"),
 (69,"WARNING",["GENERATOR STARTS","AUTOMATICALLY","WITHOUT WARNING"],"Generator Starts Automatically","Without Warning","","On standby generators and generator enclosures","Warns that the generator can start on power loss or a test signal"),
 (70,"NOTICE",["GOGGLES, FACE SHIELD","AND GLOVES REQUIRED","WHEN HANDLING","CHEMICALS"],"Chemical Handling PPE Required","Goggles, Face Shield and Gloves","","At chemical feed rooms, fill stations and unloading pads","Sets the PPE rule for anyone handling treatment chemicals"),
 (71,"NOTICE",["WASTEWATER","TREATMENT PLANT","AUTHORIZED PERSONNEL ONLY","VISITORS CHECK IN AT OFFICE"],"Wastewater Treatment Plant Entrance","Visitors Check In at Office","","At the plant gate and main entrance","Limits plant access and routes visitors and drivers to the office"),
 (72,"NOTICE",["WATER","TREATMENT PLANT","AUTHORIZED PERSONNEL ONLY","VISITORS CHECK IN AT OFFICE"],"Water Treatment Plant Entrance","Visitors Check In at Office","","At the plant gate and main entrance","Limits plant access and routes visitors and drivers to the office"),
 (73,"WARNING",["RAW SEWAGE","BIOHAZARD","WASH HANDS BEFORE","EATING OR DRINKING"],"Raw Sewage Biohazard","Wash Hands Before Eating","","At headworks, lagoons, lift stations and sludge areas","Reminds workers that sewage carries disease and to wash up"),
 (74,"DANGER",["WASTEWATER LAGOON","NO TRESPASSING","NO SWIMMING OR FISHING"],"Wastewater Lagoon No Trespassing","No Swimming or Fishing","","On lagoon fences and gates","Keeps the public away from lagoons and out of the water"),
 (75,"DANGER",["WATER TOWER","NO CLIMBING","AUTHORIZED PERSONNEL ONLY"],"Water Tower No Climbing","Authorized Personnel Only","","On the tower leg, ladder cage and site fence","Keeps unauthorized climbers off the tower"),
 (76,"DANGER",["CHEMICAL FEED ROOM","CORROSIVE AND TOXIC","CHEMICALS","AUTHORIZED OPERATORS ONLY"],"Chemical Feed Room","Authorized Operators Only","","On chemical feed and storage room doors","Limits chemical room entry to trained operators"),
 (77,"DANGER",["SEWER GAS","HYDROGEN SULFIDE (H2S)","CAN KILL WITHOUT WARNING","CARRY A GAS MONITOR"],"Sewer Gas Hydrogen Sulfide","Carry a Gas Monitor","","At lift stations, wet wells, manholes and headworks","Warns of toxic sewer gas and requires a gas monitor"),
 (78,"DANGER",["PERMIT-REQUIRED","CONFINED SPACE","DO NOT ENTER"],"Permit-Required Confined Space","Do Not Enter","","On vaults, wet wells, tanks, pits and manholes","Marks permit spaces so no one enters without a permit"),
]
FOR = "for Water and Wastewater Utilities"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P3.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for n,h,L,subj,act,slot,inst,purp in S:
        reads = " / ".join(L)
        title = f"{h} {subj} Sign, {act}, {FOR}, 8x12 Rust-Resistant Aluminum Sign by CGAP Safety"
        r = dict(sku=f"CGAP-GEN{n:03d}-812", division="G0", division_label="Water & Wastewater", sector_label="Water & Wastewater",
                 subseries="Water and wastewater site kits", header=h, subject=subj, space=inst, required_action=act, buyer="Water and wastewater operators, utility managers and public works directors",
                 purpose=purp, install_point=inst, title=title, slot=slot,
                 bullet1=f"CLEAR MESSAGE: Reads {reads}. Bold, plain wording people read at a glance.",
                 bullet2=f"WHERE IT GOES: {purp}. Suggested location: {inst.lower()}.",
                 bullet3="ALUMINUM FORMAT: One 8x12 inch sign printed on premium .065 inch rust-resistant aluminum, pre-drilled in all four corners.",
                 bullet4="INDOOR AND OUTDOOR USE: Indoor and outdoor rated with CGAP Safety's five-year outdoor warranty.",
                 bullet5="PRINTED IN MISSISSIPPI: Manufactured in-house in Amory, Mississippi by CGAP Safety. See The Gap, Close The Gap.",
                 description=f"This {subj.lower()} sign is a sign for water and wastewater utilities, treatment plants and pump stations. Printed wording: \"{reads}.\" {purp}. Suggested installation point: {inst.lower()}. The sign measures 8x12 inches on .065 inch rust-resistant aluminum with UV-resistant print and four pre-drilled holes.",
                 keywords=f"{subj.lower()} sign, {h.lower()} sign, workplace safety sign, facility safety sign, 8x12 aluminum sign, metal safety sign")
        for i in range(4): r[f"line{i+1}"] = L[i] if i < len(L) else ""
        w.writerow(r)
print(len(S))
