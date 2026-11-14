import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (98,"WARNING",["ARC FLASH AND","SHOCK HAZARD","APPROPRIATE PPE REQUIRED","QUALIFIED PERSONS ONLY"],"Arc Flash and Shock Hazard PPE Required","Appropriate PPE Required, Qualified Persons Only","electrical.2","On electrical panels, switchboards and disconnects likely to be worked on while energized","Warns of arc flash and shock at the equipment and limits work to qualified persons in proper PPE"),
 (99,"DANGER",["SUBSTATION","HIGH VOLTAGE","AUTHORIZED PERSONNEL","ONLY, KEEP OUT"],"Substation High Voltage Keep Out","Authorized Personnel Only","high_voltage.1","On every substation gate and along the fence line","Keeps unqualified people out of the substation yard"),
]
FOR = "for Warehouses, Plants, Shops and Job Sites"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P8.csv","w",newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader()
    for n,h,L,subj,act,slot,inst,purp in S:
        reads = " / ".join(L)
        title = f"{h} {subj} Sign, {act}, {FOR}, 8x12 Rust-Resistant Aluminum Sign by CGAP Safety"
        r = dict(sku=f"CGAP-GEN{n:03d}-812", division="G0", division_label="Core Workplace Signs", sector_label="General workplace safety",
                 subseries="Site plan essentials", header=h, subject=subj, space=inst, required_action=act, buyer="Facility managers, EHS and safety teams",
                 purpose=purp, install_point=inst, title=title, slot=slot,
                 bullet1=f"CLEAR MESSAGE: Reads {reads}. Bold, plain wording people read at a glance.",
                 bullet2=f"WHERE IT GOES: {purp}. Suggested location: {inst.lower()}.",
                 bullet3="ALUMINUM FORMAT: One 8x12 inch sign printed on premium .065 inch rust-resistant aluminum, pre-drilled in all four corners.",
                 bullet4="INDOOR AND OUTDOOR USE: Indoor and outdoor rated with CGAP Safety's five-year outdoor warranty.",
                 bullet5="PRINTED IN MISSISSIPPI: Manufactured in-house in Amory, Mississippi by CGAP Safety. See The Gap, Close The Gap.",
                 description=f"This {subj.lower()} sign is a core workplace sign for warehouses, plants, shops and job sites. Printed wording: \"{reads}.\" {purp}. Suggested installation point: {inst.lower()}. The sign measures 8x12 inches on .065 inch rust-resistant aluminum with UV-resistant print and four pre-drilled holes.",
                 keywords=f"{subj.lower()} sign, {h.lower()} sign, workplace safety sign, facility safety sign, 8x12 aluminum sign, metal safety sign")
        for i in range(4): r[f"line{i+1}"] = L[i] if i < len(L) else ""
        w.writerow(r)
print(len(S))
