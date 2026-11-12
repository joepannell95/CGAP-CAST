import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (79,"DANGER",["HIGH VOLTAGE","KEEP OUT","AUTHORIZED PERSONNEL ONLY"],"High Voltage Keep Out","Authorized Personnel Only","","On substation, regulator and capacitor bank gates and fences","Keeps the public and unqualified workers away from energized electrical equipment"),
 (80,"NOTICE",["ELECTRIC SUBSTATION","NO TRESPASSING","REPORT DAMAGE OR INTRUDERS","TO YOUR ELECTRIC UTILITY"],"Electric Substation No Trespassing","Report Damage or Intruders","","On every side of the substation fence","Marks the substation as private and asks the public to report damage, open gates or intruders"),
 (81,"WARNING",["HAZARDOUS VOLTAGE INSIDE","KEEP 10 FEET CLEAR","OF CABINET DOORS","NO PLANTING OR PARKING"],"Hazardous Voltage Keep 10 Feet Clear","No Planting or Parking","","On pad-mounted transformer and switchgear fences, bollards and nearby walls","Keeps the working space in front of pad-mounted equipment clear so crews can open and operate it safely"),
 (82,"DANGER",["BURIED ELECTRIC CABLE","CALL 811","BEFORE YOU DIG"],"Buried Electric Cable Call 811","Before You Dig","","Near pad-mounted equipment, underground risers and buried cable routes","Warns diggers that underground power runs here and to call 811 before excavating"),
 (83,"NOTICE",["METER SHOP","AUTHORIZED PERSONNEL ONLY","NO VISITORS ON TEST FLOOR"],"Meter Shop Authorized Personnel Only","No Visitors on Test Floor","","On meter shop and meter test lab doors","Keeps visitors and untrained staff away from energized meter test boards"),
]
FOR = "for Electric Cooperatives and Utilities"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P4.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for n,h,L,subj,act,slot,inst,purp in S:
        reads = " / ".join(L)
        title = f"{h} {subj} Sign, {act}, {FOR}, 8x12 Rust-Resistant Aluminum Sign by CGAP Safety"
        r = dict(sku=f"CGAP-GEN{n:03d}-812", division="G0", division_label="Electric Utilities", sector_label="Electric Utilities",
                 subseries="Electric co-op site kits", header=h, subject=subj, space=inst, required_action=act, buyer="Electric cooperative operations managers, safety coordinators and substation crews",
                 purpose=purp, install_point=inst, title=title, slot=slot,
                 bullet1=f"CLEAR MESSAGE: Reads {reads}. Bold, plain wording people read at a glance.",
                 bullet2=f"WHERE IT GOES: {purp}. Suggested location: {inst.lower()}.",
                 bullet3="ALUMINUM FORMAT: One 8x12 inch sign printed on premium .065 inch rust-resistant aluminum, pre-drilled in all four corners.",
                 bullet4="INDOOR AND OUTDOOR USE: Indoor and outdoor rated with CGAP Safety's five-year outdoor warranty.",
                 bullet5="PRINTED IN MISSISSIPPI: Manufactured in-house in Amory, Mississippi by CGAP Safety. See The Gap, Close The Gap.",
                 description=f"This {subj.lower()} sign is a sign for electric cooperatives, municipal electric systems and substations. Printed wording: \"{reads}.\" {purp}. Suggested installation point: {inst.lower()}. The sign measures 8x12 inches on .065 inch rust-resistant aluminum with UV-resistant print and four pre-drilled holes.",
                 keywords=f"{subj.lower()} sign, {h.lower()} sign, workplace safety sign, facility safety sign, 8x12 aluminum sign, metal safety sign")
        for i in range(4): r[f"line{i+1}"] = L[i] if i < len(L) else ""
        w.writerow(r)
print(len(S))
