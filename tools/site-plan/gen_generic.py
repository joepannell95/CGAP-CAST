import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (1,"NOTICE",["FIRE EXTINGUISHER","KEEP ACCESS CLEAR"],"Fire Extinguisher","Keep Access Clear","emergency.0","Above each fire extinguisher","Helps people find the extinguisher fast and keeps the path to it open"),
 (2,"SAFETY FIRST",["FIRST AID STATION","KIT AND SUPPLIES HERE"],"First Aid Station","Kit and Supplies Here","emergency.2","Above the first aid cabinet or kit","Shows where first aid supplies are kept"),
 (4,"NOTICE",["HARD HAT AREA","HEAD PROTECTION","REQUIRED"],"Hard Hat Area","Head Protection Required","ppe.0","At entrances to areas requiring head protection","Tells everyone entering that hard hats are required"),
 (5,"NOTICE",["SAFETY GLASSES","REQUIRED IN","THIS AREA"],"Safety Glasses Required","Required in This Area","ppe.1","At entrances to eye protection areas","Reminds workers and visitors to wear eye protection"),
 (6,"NOTICE",["HEARING PROTECTION","REQUIRED IN","THIS AREA"],"Hearing Protection Required","Required in This Area","ppe.2","At entrances to high-noise areas","Reminds everyone to put on hearing protection before entering"),
 (7,"NOTICE",["HIGH VISIBILITY VEST","REQUIRED BEYOND","THIS POINT"],"High-Visibility Vest Required","Required Beyond This Point","ppe.3","At doors and gates into vehicle or forklift areas","Keeps people visible where vehicles and forklifts operate"),
 (8,"NOTICE",["PPE REQUIRED","BEYOND THIS POINT","HARD HAT, GLASSES, VEST"],"PPE Required Beyond This Point","Hard Hat, Glasses, Vest","ppe.0","At plant and shop floor entrances","Sets the basic PPE rule at the door"),
 (9,"NOTICE",["ALL CONTRACTORS","MUST CHECK IN","AT THE OFFICE"],"Contractors Check In","Must Check In at the Office","visitor.2","At site gates and main entrances","Routes contractors to the office before they start work"),
 (10,"NOTICE",["EMPLOYEES ONLY","BEYOND THIS POINT"],"Employees Only","Beyond This Point","employee_only.0","On doors to back-of-house and work areas","Keeps customers and visitors out of work areas"),
 (11,"CAUTION",["KEEP GUARDS IN PLACE","DO NOT OPERATE","WITHOUT GUARDS"],"Keep Machine Guards in Place","Do Not Operate Without Guards","machines.0","On or beside guarded machines","Reminds operators that guards stay on while running"),
 (12,"CAUTION",["PINCH POINT","KEEP HANDS CLEAR"],"Pinch Point","Keep Hands Clear","machines.1","Next to rollers, gears and closing parts","Warns of places where hands can be caught"),
 (13,"NOTICE",["AUTHORIZED OPERATORS","ONLY","TRAINING REQUIRED"],"Authorized Machine Operators Only","Training Required","machines.2","On machines that need trained operators","Limits machine use to trained, authorized staff"),
 (14,"DANGER",["LOCK OUT EQUIPMENT","BEFORE SERVICING","OR CLEANING"],"Lock Out Before Servicing","Before Servicing or Cleaning","lockout.0","At disconnects and on machines that get serviced","Reminds crews to lock out energy before reaching in"),
 (15,"NOTICE",["LOCKOUT TAGOUT","STATION","LOCKS AND TAGS HERE"],"Lockout Tagout Station","Locks and Tags Here","lockout.1","Above the lockout station or board","Marks where locks, tags and hasps are kept"),
 (16,"CAUTION",["STOP","LOOK FOR FORKLIFTS","BEFORE CROSSING"],"Stop Look for Forklifts","Before Crossing","forklift.2","At aisle crossings and doorways into forklift areas","Makes people stop and look before stepping into traffic"),
 (18,"NOTICE",["REPORT ALL RACK","DAMAGE TO YOUR","SUPERVISOR"],"Report Rack Damage","Report to Your Supervisor","racking.1","On rack end frames","Gets bent uprights and beams reported before they fail"),
 (19,"CAUTION",["CONVEYOR PINCH POINTS","KEEP HANDS CLEAR"],"Conveyor Pinch Points","Keep Hands Clear","conveyor.0","Along conveyor lines near transfers and rollers","Warns of rollers and belts that can catch hands"),
 (20,"DANGER",["DO NOT CLIMB, SIT","OR RIDE ON","CONVEYOR"],"Do Not Ride Conveyor","Do Not Climb or Sit","conveyor.1","Along conveyors and at crossovers","Keeps people off moving conveyors"),
 (21,"DANGER",["OVERHEAD CRANE","STAY CLEAR OF","MOVING LOADS"],"Overhead Crane Loads","Stay Clear of Moving Loads","crane.0","Under crane runways and at bay entrances","Warns of loads moving overhead"),
 (22,"DANGER",["DO NOT STAND","UNDER SUSPENDED","LOADS"],"Suspended Loads","Do Not Stand Under Loads","crane.1","In lifting and rigging areas","Keeps people out from under lifted loads"),
 (23,"WARNING",["WELDING AREA","ARC RAYS CAN INJURE","EYES AND SKIN"],"Welding Area","Arc Rays Can Injure Eyes and Skin","welding.0","At welding bays and curtains","Warns passersby of arc flash and UV from welding"),
 (24,"NOTICE",["HOT WORK PERMIT","REQUIRED IN","THIS AREA"],"Hot Work Permit Required","Required in This Area","welding.1","Where welding, cutting or grinding needs a permit","Reminds crews to get a hot work permit first"),
 (25,"WARNING",["CHEMICAL STORAGE","AREA","AUTHORIZED PERSONNEL"],"Chemical Storage Area","Authorized Personnel","chemical.0","On chemical storage room doors and cages","Limits access to stored chemicals"),
 (26,"DANGER",["CORROSIVE","CHEMICALS","WEAR GLOVES AND GOGGLES"],"Corrosive Chemicals","Wear Gloves and Goggles","chemical.1","Where acids, caustics and cleaners are stored or used","Warns of burns and sets the PPE needed"),
 (27,"NOTICE",["SAFETY DATA SHEETS","LOCATED HERE"],"Safety Data Sheets","Located Here","chemical.2","Above the SDS binder or station","Shows where SDS are kept for everyone to find"),
 (28,"CAUTION",["COMPRESSED GAS","CYLINDERS MUST BE","SECURED UPRIGHT"],"Secure Gas Cylinders","Must Be Secured Upright","compressed_gas.0","At cylinder storage racks and carts","Keeps cylinders chained so they cannot fall"),
 (31,"CAUTION",["HIGH NOISE AREA","HEARING PROTECTION","REQUIRED"],"High Noise Area","Hearing Protection Required","noise.0","At entrances to loud equipment areas","Warns of noise levels that need ear protection"),
 (33,"WARNING",["FALL PROTECTION","REQUIRED BEYOND","THIS POINT"],"Fall Protection Required","Required Beyond This Point","fall.0","At roof hatches, mezzanines and open edges","Reminds workers to tie off past this point"),
 (34,"NOTICE",["ROOF ACCESS","AUTHORIZED","PERSONNEL ONLY"],"Roof Access","Authorized Personnel Only","roof.0","On roof hatches, ladders and stair doors","Limits roof access to authorized staff"),
 (35,"NOTICE",["MECHANICAL ROOM","AUTHORIZED","PERSONNEL ONLY"],"Mechanical Room","Authorized Personnel Only","mechanical_room.0","On mechanical room doors","Keeps unauthorized people out of equipment rooms"),
 (36,"WARNING",["BOILER ROOM","AUTHORIZED","PERSONNEL ONLY"],"Boiler Room Authorized Only","Authorized Personnel Only","boiler.0","On boiler room doors","Limits boiler room access to trained staff"),
 (37,"CAUTION",["HOT SURFACE","DO NOT TOUCH"],"Hot Surface","Do Not Touch","boiler.1","On or near hot pipes, ovens and equipment","Warns of surfaces hot enough to burn"),
 (38,"CAUTION",["WATCH FOR","MOVING VEHICLES"],"Moving Vehicles","Watch for Moving Vehicles","vehicles.0","Along yard walkways and building exits","Warns pedestrians of trucks and equipment"),
 (39,"CAUTION",["SLOW","5 MPH","IN THE YARD"],"5 MPH Yard","Slow, 5 MPH in the Yard","vehicles.1","At yard gates and drive lanes","Sets a slow speed where people and trucks mix"),
 (40,"DANGER",["OPEN EXCAVATION","KEEP BACK"],"Open Excavation","Keep Back","excavation.0","At trench and excavation edges","Keeps people back from the edge of open digs"),
 (41,"NOTICE",["CONSTRUCTION SITE","HARD HATS AND VESTS","REQUIRED"],"Construction Site PPE","Hard Hats and Vests Required","site_entry.0","At jobsite gates and entrances","Sets the PPE rule for everyone entering the site"),
 (42,"CAUTION",["FREEZER AREA","WEAR COLD WEATHER","PPE"],"Freezer Area","Wear Cold Weather PPE","cold_storage.1","At freezer and cold room doors","Reminds staff to gear up before going into the cold"),
 (43,"NOTICE",["NO FOOD OR DRINK","IN THE LAB"],"No Food or Drink in Lab","In the Lab","lab.1","On lab doors and benches","Keeps food and drinks out of work with chemicals or samples"),
]
FOR = "for Warehouses, Plants, Shops and Job Sites"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P1.csv","w",newline="") as f:
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
