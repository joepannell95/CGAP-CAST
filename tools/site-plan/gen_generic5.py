import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (84,"NOTICE",["NOT AN EXIT","THIS DOOR IS NOT","A WAY OUT"],"Not an Exit","This Door Is Not a Way Out","exits.1","On doors that could be mistaken for an exit","Keeps people from heading for a door that does not lead out of the building"),
 (85,"NOTICE",["FIRE EXIT","KEEP CLEAR","DO NOT BLOCK"],"Fire Exit Keep Clear","Do Not Block","exits.0","On or beside each exit door","Keeps exit doors and the path to them free of carts, pallets and storage"),
 (86,"SAFETY FIRST",["AED","AUTOMATED EXTERNAL","DEFIBRILLATOR","LOCATED HERE"],"AED Location","Defibrillator Located Here","emergency.4","Above the AED cabinet or wall mount","Gets the AED to a cardiac arrest faster by marking exactly where it hangs"),
 (87,"SAFETY FIRST",["EMERGENCY SHOWER","KEEP AREA CLEAR","FLUSH 15 MINUTES"],"Emergency Shower","Keep Area Clear","emergency.5","Above each emergency drench shower","Marks the drench shower so anyone splashed with chemicals can find it fast"),
 (88,"NOTICE",["AUTHORIZED FORKLIFT","OPERATORS ONLY","TRAINING REQUIRED"],"Authorized Forklift Operators Only","Training Required","forklift.3","At forklift parking and charging areas","Limits forklift use to trained and evaluated operators"),
 (89,"DANGER",["NO SWIMMING","NEAR DOCKS OR BOATS","ELECTRIC SHOCK","HAZARD IN WATER"],"No Swimming Near Docks","Electric Shock Hazard in Water","marina.1","On docks, piers and slip entrances","Keeps swimmers out of water where stray current from shore power can cause electric shock drowning"),
 (90,"WARNING",["POTENTIAL SHOCK HAZARD","ELECTRICAL CURRENTS","MAY BE PRESENT","IN THE WATER"],"Potential Shock Hazard","Electrical Currents May Be Present in the Water","marina.0","At the head of each dock and pier with shore power","Gives the shock hazard warning marinas and boatyards post at docks with shore power"),
]
FOR = "for Warehouses, Plants, Shops and Job Sites"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P5.csv","w",newline="") as f:
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
