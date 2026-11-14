import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (92,"WARNING",["ARC FLASH BOUNDARY","ARC RATED PPE","REQUIRED BEYOND","THIS POINT"],"Arc Flash Boundary PPE Required","Arc Rated PPE Required Beyond This Point","arc_flash.1","At the arc flash boundary around energized switchgear and panels","Stops unprotected workers at the arc flash boundary and sets the arc rated PPE rule"),
 (93,"NOTICE",["LAB COAT, GLOVES","AND SAFETY GLASSES","REQUIRED IN","THIS LAB"],"Lab PPE Required","Lab Coat, Gloves and Safety Glasses Required","lab.0","On each laboratory door","Sets the basic lab PPE rule at the door"),
 (94,"WARNING",["NO LIFEGUARD ON DUTY","SWIM AT YOUR OWN RISK","CHILDREN MUST BE","SUPERVISED BY AN ADULT"],"No Lifeguard on Duty","Swim at Your Own Risk","pool.1","At every pool entrance and on the pool fence","Tells swimmers no lifeguard is watching and that children need an adult"),
 (95,"NOTICE",["VEHICLE LIFT","AUTHORIZED TRAINED","OPERATORS ONLY"],"Vehicle Lift Authorized Operators Only","Trained Operators Only","vehicle_lift.0","On or beside each vehicle lift control","Limits lift use to technicians trained on that lift"),
 (96,"CAUTION",["SLIPPERY FLOOR","WATCH YOUR STEP"],"Slippery Floor","Watch Your Step","wet_floor.0","Where floors stay wet from washdown, ice or process water","Warns people to slow down where the floor is often slick"),
 (97,"DANGER",["FUEL STORAGE TANK","FLAMMABLE","NO SMOKING","OR OPEN FLAMES"],"Fuel Storage Tank No Smoking","Flammable, No Open Flames","fuel.1","On fuel storage tanks and their fences","Keeps smoking and open flames away from stored gasoline and diesel"),
]
FOR = "for Warehouses, Plants, Shops and Job Sites"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P7.csv","w",newline="") as f:
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
