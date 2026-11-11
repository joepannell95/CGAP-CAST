import csv
# sku#, header, lines, subject, action phrase (title), plan slot, install point, purpose, hazard
S = [
 (44,"DANGER",["CARBON DIOXIDE","ASPHYXIATION HAZARD","LEAVE IF ALARM SOUNDS"],"CO2 Asphyxiation Hazard","Leave if Alarm Sounds","co2.0","At CO2 tanks, manifold rooms and fermentation areas","Warns that CO2 can displace oxygen in enclosed spaces"),
 (45,"WARNING",["OXYGEN DEFICIENT","AREA","VENTILATE BEFORE ENTERING"],"Oxygen Deficient Area","Ventilate Before Entering","co2.1","At doors to tank rooms and low-lying areas","Reminds people to ventilate and test the air before going in"),
 (46,"DANGER",["WASH TUNNEL","KEEP OUT","WHEN RUNNING"],"Wash Tunnel","Keep Out When Running","car_tunnel.0","At wash tunnel entrances and exits","Keeps staff and customers out of the tunnel while equipment runs"),
 (47,"CAUTION",["WASH CONVEYOR","KEEP HANDS","AND FEET CLEAR"],"Wash Conveyor","Keep Hands and Feet Clear","car_tunnel.1","Along the tunnel conveyor and rollers","Warns of rollers and chains that can catch hands and feet"),
 (48,"WARNING",["HIGH PRESSURE WATER","CAN CAUSE","SERIOUS INJURY"],"High Pressure Water","Can Cause Serious Injury","pressure_wash.0","Near pressure washers and spray bays","Warns of injury from high pressure spray"),
 (49,"NOTICE",["EYE AND HEARING","PROTECTION REQUIRED","WHILE PRESSURE WASHING"],"Pressure Washing PPE","Eye and Hearing Protection Required","pressure_wash.1","At pressure washing stations","Reminds crews to wear eye and hearing protection"),
 (50,"NOTICE",["RESTRICTED AREA","AUTHORIZED ACCESS","ONLY"],"Restricted Area","Authorized Access Only","restricted.0","On doors to controlled and secure areas","Limits entry to people with approved access"),
 (51,"NOTICE",["SERVER ROOM","AUTHORIZED","PERSONNEL ONLY"],"Server Room","Authorized Personnel Only","restricted.1","On server room and data hall doors","Keeps unauthorized people away from critical equipment"),
 (52,"NOTICE",["NO FOOD OR DRINK","IN THIS AREA"],"No Food or Drink","In This Area","restricted.2","On doors to equipment and server rooms","Keeps spills and crumbs away from sensitive equipment"),
 (53,"WARNING",["BATTERY ROOM","ACID AND HYDROGEN GAS","NO SMOKING, EYE PROTECTION"],"Battery Room","Acid and Hydrogen Gas","ups.0","On battery room doors","Warns of acid, hydrogen gas and the PPE needed"),
 (54,"DANGER",["ENERGIZED EQUIPMENT","AUTHORIZED","PERSONNEL ONLY"],"Energized Equipment","Authorized Personnel Only","ups.1","On electrical and UPS equipment rooms","Keeps unqualified people away from live equipment"),
 (55,"WARNING",["FIRE SUPPRESSION","SYSTEM","AREA PROTECTED"],"Fire Suppression System","Area Protected","fire_supp.0","At doors to rooms with gas suppression","Tells people the room has a fire suppression system"),
 (56,"DANGER",["IF ALARM SOUNDS","LEAVE AREA","DO NOT ENTER"],"Suppression Alarm","If Alarm Sounds Leave Area","fire_supp.1","Inside and outside protected rooms","Tells people to leave and stay out when the alarm sounds"),
 (57,"WARNING",["SAW BLADE","KEEP HANDS","CLEAR"],"Saw Blade","Keep Hands Clear","saw.0","On or beside saws","Warns of exposed blades that can cut"),
 (58,"NOTICE",["EYE AND HEARING","PROTECTION REQUIRED","AT SAWS"],"Saw Area PPE","Eye and Hearing Protection Required","saw.1","At saw and cutting area entrances","Reminds crews to wear eye and hearing protection around saws"),
 (59,"WARNING",["COMBUSTIBLE DUST","NO IGNITION","SOURCES"],"Combustible Dust","No Ignition Sources","dust.0","Where fine dust collects","Warns that fine dust can burn or explode"),
 (60,"DANGER",["NO SMOKING","OR OPEN FLAME"],"No Smoking or Open Flame","No Smoking","dust.1","At doors and fences around flammable areas","Keeps ignition sources away from fuel and dust"),
 (61,"DANGER",["NO SMOKING","TURN OFF ENGINE","WHILE FUELING"],"No Smoking Turn Off Engine","While Fueling","fuel_dispenser.0","On fuel pumps and dispenser islands","Reminds drivers to shut off engines and put out smoking materials"),
 (62,"NOTICE",["EMERGENCY FUEL","SHUTOFF","LOCATED HERE"],"Emergency Fuel Shutoff","Located Here","fuel_dispenser.1","Next to the emergency fuel shutoff switch","Shows where to shut off fuel pumps in an emergency"),
 (63,"DANGER",["BLASTING AREA","KEEP OUT"],"Blasting Area","Keep Out","blasting.0","At blast zone boundaries and haul road entrances","Keeps people out of active blast zones"),
 (64,"NOTICE",["QUARRY","AUTHORIZED PERSONNEL","ONLY"],"Quarry Authorized Only","Authorized Personnel Only","blasting.1","At quarry and pit entrances","Limits entry to authorized and trained people"),
 (65,"CAUTION",["HAUL TRUCKS","HAVE RIGHT","OF WAY"],"Haul Trucks Right of Way","Haul Trucks Have Right of Way","haul_road.0","Along haul roads and crossings","Reminds drivers and walkers that big trucks cannot stop quickly"),
 (66,"CAUTION",["SLOW","DRIVE SAFELY","ON SITE ROADS"],"Site Roads Drive Safely","Slow, Drive Safely","haul_road.1","At site entrances and road junctions","Sets a slow, careful pace where trucks and people share roads"),
]
FOR = "for Warehouses, Plants, Shops and Job Sites"
cols = "sku,division,division_label,sector_label,subseries,header,line1,line2,line3,line4,subject,space,required_action,buyer,purpose,install_point,title,bullet1,bullet2,bullet3,bullet4,bullet5,description,keywords,slot".split(",")
with open("GEN_P2.csv","w",newline="") as f:
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
