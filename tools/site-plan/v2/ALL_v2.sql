alter table finder.plan_slot add column if not exists pri int default 2;
alter table finder.plan_slot add column if not exists why text;
alter table finder.plan_extra add column if not exists ip text;
create table if not exists finder.plan_q(code text primary key, facs text[], ord int, kind text, label text, help text, def int default 0, fdef jsonb, area text, slots text[], adds text[], maxv int default 50);
alter table finder.plan_q enable row level security;

insert into finder.plan_area(code,label,ord) values ('exits','Exits and exit routes',0),('marina','Docks, piers and slips',55)
on conflict (code) do update set label=excluded.label, ord=excluded.ord;
insert into finder.plan_slot(k,area,label,q,scope,ord) values
 ('exits.0','exits','Keep exit clear','fire exit keep clear do not block exit door','area',0),
 ('exits.1','exits','Not an exit','not an exit door','area',1),
 ('emergency.4','emergency','AED location','aed automated external defibrillator location','site',4),
 ('emergency.5','emergency','Emergency shower','emergency shower safety shower location','area',5),
 ('forklift.3','forklift','Trained forklift operators only','authorized forklift operators only trained certified','site',3),
 ('marina.0','marina','Electric shock hazard in the water','electric shock hazard water marina dock electrical current no swimming','area',0),
 ('marina.1','marina','No swimming near docks','no swimming marina dock boat slip','area',1)
on conflict (k) do update set area=excluded.area,label=excluded.label,q=excluded.q,scope=excluded.scope,ord=excluded.ord;

insert into finder.plan_fac(code,name,rx,areas,ord) values
 ('office','Office or commercial building','office|commercial building|corporate|bank|call center',array['emergency','exits','electrical','mechanical_room','roof','restricted','chemical','employee_only','visitor'],18),
 ('retail','Retail store or grocery','retail|grocery|store|supermarket|pharmacy|hardware',array['emergency','exits','employee_only','dock','racking','forklift','cold_storage','wet_floor','electrical','chemical','roof','visitor'],19),
 ('marina','Marina or boatyard','marina|boat|harbor|yacht|dock',array['marina','fuel_dispenser','fuel','electrical','wet_floor','chemical','employee_only','visitor','emergency','exits'],20)
on conflict (code) do update set name=excluded.name,rx=excluded.rx,areas=excluded.areas,ord=excluded.ord;
-- every site type gets exits right after emergency gear
update finder.plan_fac set areas = array_append(areas,'exits') where not ('exits' = any(areas));

-- candidates for the new slots
-- (no delete: new slots have no prior candidates)
insert into finder.plan_cand(k,sku,pos,score)
select s.k, r.sku, row_number() over (partition by s.k order by r.score desc), r.score
from finder.plan_slot s cross join lateral finder.search_ids(s.q, null, null, null, null, 12) r
where s.k in ('exits.0','exits.1','emergency.4','emergency.5','forklift.3','marina.0','marina.1')
on conflict do nothing;
insert into finder.plan_card select * from finder.cards(array(select distinct sku from finder.plan_cand where sku not in (select sku from finder.plan_card) and sku not in (select sku from finder.plan_extra))) on conflict do nothing;
-- Priority 1 = cited in a code or standard, 2 = recommended, 3 = good practice
update finder.plan_slot s set pri = v.p, why = v.w from (values
 ('confined.0',1,'OSHA 1910.146 requires a danger sign, or an equally effective warning, at every permit-required confined space.'),
 ('high_voltage.0',1,'OSHA 1910.303 calls for warning signs that keep unqualified people out of rooms and enclosures with exposed live parts over 600 volts.'),
 ('high_voltage.1',2,'Keeps the public and unqualified workers out of fenced electrical yards.'),
 ('electrical.0',2,'Keeps unqualified people out of electrical rooms (OSHA 1910.303).'),
 ('electrical.1',2,'NEC 110.26 requires clear working space in front of panels. The sign keeps it from turning into storage.'),
 ('electrical.2',1,'NEC 110.16 requires an arc flash warning on panels and switchgear likely to be worked on while energized.'),
 ('arc_flash.0',1,'NEC 110.16 requires an arc flash warning on equipment likely to be worked on while energized.'),
 ('arc_flash.1',2,'NFPA 70E sets the arc flash boundary and the PPE required inside it.'),
 ('emergency.0',1,'NFPA 10 requires extinguishers to be easy to find, with signs wherever they are out of direct view.'),
 ('emergency.1',1,'ANSI Z358.1 calls for a highly visible sign at every eyewash station.'),
 ('emergency.5',1,'ANSI Z358.1 calls for a highly visible sign at every emergency shower.'),
 ('emergency.2',2,'OSHA 1910.151 requires first aid supplies to be readily available. The sign shows where.'),
 ('emergency.3',2,'Gives everyone one place to meet so a headcount is fast after an evacuation.'),
 ('emergency.4',2,'Seconds count in cardiac arrest. A sign gets the AED to the scene faster.'),
 ('battery.1',1,'OSHA 1910.178(g) prohibits smoking in battery charging areas.'),
 ('battery.2',1,'OSHA 1910.178(g) requires eye flushing at battery charging, and ANSI Z358.1 calls for a sign.'),
 ('battery.0',2,'Marks the charging area so people know hydrogen and acid may be present.'),
 ('exits.1',1,'OSHA 1910.37 requires any door that could be mistaken for an exit to be marked Not an Exit.'),
 ('exits.0',2,'OSHA 1910.37 requires exit routes to stay clear and unobstructed.'),
 ('flammable.0',1,'OSHA 1910.106 and NFPA 30 call for no smoking signs where flammable liquids are stored or used.'),
 ('flammable.1',2,'Reminds staff that flammables go back in the cabinet and the doors stay shut.'),
 ('fuel.1',1,'NFPA 30 calls for no smoking signs at fuel tanks and dispensing.'),
 ('fuel.0',2,'Engine off and no smoking while fueling cuts the ignition sources.'),
 ('fuel_dispenser.0',1,'NFPA 30A requires no smoking and stop engine warnings at fuel dispensers.'),
 ('fuel_dispenser.1',1,'NFPA 30A requires the emergency fuel shutoff to be clearly marked.'),
 ('kitchen.1',1,'NFPA 96 requires the manual pull for the hood fire suppression system to be clearly marked.'),
 ('biohazard.0',1,'OSHA 1910.1030 requires the biohazard symbol where infectious materials are kept or handled.'),
 ('radiation.0',1,'NRC rule 10 CFR 20.1902 requires posting at radiation areas.'),
 ('radiation.1',2,'The ACR MR safety guidance calls for clear warnings that the MRI magnet is always on.'),
 ('fire_supp.1',1,'NFPA 12 and NFPA 2001 call for warning signs where CO2 or clean agent systems can discharge.'),
 ('fire_supp.0',2,'Tells people the room has an automatic suppression system.'),
 ('co2.0',1,'NFPA 55 calls for CO2 warning signs at rooms with indoor CO2 storage.'),
 ('marina.0',1,'NEC 555.10 requires electric shock hazard warning signs at marinas and boatyards.'),
 ('pool.1',1,'Most state pool codes require a No Lifeguard on Duty sign where there is no lifeguard.'),
 ('ammonia.0',1,'IIAR 2 and the mechanical code require ammonia machinery room doors to be marked and restricted.'),
 ('ammonia.1',2,'Tells people what to do and where to go if ammonia leaks.'),
 ('chemical.2',2,'OSHA 1910.1200 requires safety data sheets to be readily accessible. The sign shows where they are.'),
 ('chemical.1',2,'OSHA 1910.1200 requires workers to be warned of chemical hazards where they work.'),
 ('chemical.0',2,'Limits who can get into stored chemicals.'),
 ('crane.1',2,'OSHA 1926.1425 keeps workers out from under suspended loads.'),
 ('crane.0',2,'Warns people walking under crane runways.'),
 ('grain.0',2,'OSHA 1910.272 sets strict rules before anyone enters a grain bin.'),
 ('grain.1',2,'Augers and sweeps cause many grain handling injuries. Keep hands and feet clear.'),
 ('forklift.3',2,'OSHA 1910.178(l) allows only trained and evaluated operators to drive forklifts.'),
 ('forklift.0',2,'Warns pedestrians where forklifts run.'),
 ('forklift.1',2,'Keeps foot traffic in marked walkways.'),
 ('forklift.2',2,'Makes people stop and look at blind corners and doorways.'),
 ('ppe.0',2,'OSHA 1910.132 requires the right PPE for each hazard. The sign sets the rule at the door.'),
 ('ppe.1',2,'OSHA 1910.133 requires eye protection where flying particles or chemicals are present.'),
 ('ppe.2',2,'OSHA 1910.95 requires hearing protection in high-noise areas.'),
 ('ppe.3',2,'Keeps people visible where vehicles and forklifts move.'),
 ('noise.0',2,'OSHA 1910.95 requires hearing protection in high-noise areas.'),
 ('lockout.0',2,'OSHA 1910.147 requires energy to be locked out before servicing.'),
 ('lockout.1',2,'Shows where locks and tags are kept so nobody skips lockout.'),
 ('machines.0',2,'OSHA 1910.212 requires guards on machines with moving parts.'),
 ('machines.1',2,'Warns of places where hands can be caught.'),
 ('welding.0',2,'OSHA 1910.252 requires protecting nearby workers from welding arc rays.'),
 ('welding.1',2,'NFPA 51B requires a permit before hot work outside a welding area.'),
 ('compressed_gas.0',2,'OSHA 1910.101 and CGA P-1 require cylinders to be secured so they cannot fall.'),
 ('compressed_gas.1',2,'OSHA 1910.253 requires 20 feet or a fire barrier between oxygen and fuel gas cylinders.'),
 ('h2s.0',2,'H2S can kill at low levels and deadens the sense of smell. Warn before entry.'),
 ('chlorine.0',2,'Marks where chlorine is stored so responders know what they face.'),
 ('chlorine.1',2,'Limits access to the chemical feed room.'),
 ('fall.0',2,'OSHA 1910.28 requires fall protection at unprotected edges four feet or higher.'),
 ('fall.1',2,'Warns of open edges until guardrail is in place.'),
 ('excavation.0',2,'OSHA 1926.651 requires keeping people and loads back from excavation edges.'),
 ('scaffold.0',2,'OSHA 1926.451 requires scaffolds to be inspected before each shift.'),
 ('dust.0',2,'OSHA and NFPA 652 treat combustible dust as a fire and explosion hazard.'),
 ('dust.1',2,'Removes ignition sources where dust collects.'),
 ('confined.0',1,'OSHA 1910.146 requires a danger sign, or an equally effective warning, at every permit-required confined space.'),
 ('marina.1',2,'Keeps swimmers away from docks where stray current can be in the water.'),
 ('vehicle_lift.0',2,'ANSI/ALI ALOIM requires lifts to be used only by trained operators.'),
 ('vehicle_lift.1',2,'Keeps people from standing under a raised vehicle.'),
 ('cold_storage.0',2,'Shows the inside door release so nobody gets trapped in a walk-in.'),
 ('kitchen.0',2,'Hot oil causes many kitchen burns. Warn at every fryer.'),
 ('lab.0',2,'OSHA 1910.1450 requires lab PPE suited to the hazards.'),
 ('saw.0',2,'Saw blades cause many wood shop amputations. Keep hands clear.'),
 ('conveyor.2',2,'Shows where the emergency stop is so anyone can reach it fast.'),
 ('racking.0',2,'OSHA 1910.176 requires storage to be stable. Post the rated beam load.'),
 ('visitor.0',3,'Sends every visitor to the office first.'),
 ('visitor.1',3,'Keeps the public out of work areas.'),
 ('visitor.2',3,'Gets contractors through your orientation before they start.'),
 ('employee_only.0',3,'Keeps customers out of work areas.'),
 ('boiler.1',3,'Warns of surfaces hot enough to burn.'),
 ('kitchen.2',3,'Reminds staff of guards and cut gloves at slicers.'),
 ('lab.1',3,'Keeps food and drinks out of work with chemicals or samples.'),
 ('restricted.2',3,'Keeps spills away from equipment.'),
 ('vehicles.0',3,'Warns pedestrians of yard traffic.'),
 ('vehicles.1',3,'Sets a slow speed where people and trucks mix.'),
 ('haul_road.1',3,'Sets a speed limit on site roads.'),
 ('cold_storage.1',3,'Reminds staff to gear up before going into the cold.'),
 ('racking.1',3,'Gets rack damage reported before it fails.'),
 ('livestock.0',3,'Keeps visitors away from animals.'),
 ('shop_class.1',3,'Keeps students off machines without the instructor.'),
 ('pressure_wash.1',3,'Reminds washers to wear eye and ear protection.'),
 ('saw.1',3,'Reminds operators to wear eye and ear protection at saws.'),
 ('dock.2',3,'Warns of the leveler lip and pit.'),
 ('mechanical_room.0',3,'Keeps unauthorized people out of equipment rooms.'),
 ('roof.0',3,'Limits roof access to people trained for it.'),
 ('wet_floor.0',3,'Warns of floors that stay wet.')
) v(k,p,w) where s.k = v.k;
-- Site detail questions. kind: count or yesno. slots: qty = answer. adds: qty += answer. area: area on when answer > 0, off when 0.
insert into finder.plan_q(code,facs,ord,kind,label,help,def,fdef,area,slots,adds,maxv) values
 ('ext',null,10,'count','Fire extinguishers','One sign above each extinguisher so it can be found through smoke.',4,'{"office":3,"kitchen":2,"carwash":2,"fuelstop":3,"marina":4,"mfg":8,"warehouse":8}','emergency','{emergency.0}',null,99),
 ('eye',null,11,'count','Eyewash stations','Each station gets its own sign. Count bottle stations too.',1,'{"office":0,"retail":0,"construction":0,"marina":0,"school":1}','emergency','{emergency.1}',null,50),
 ('shower',null,12,'count','Emergency showers','Drench showers near acids, caustics or battery charging.',0,'{"oil_chem":2,"lab":1,"water":1}',null,'{emergency.5}',null,20),
 ('aed',null,13,'yesno','There is an AED on site','We add an AED location sign.',0,'{"office":1,"school":1,"retail":1}',null,'{emergency.4}',null,1),
 ('panel',null,20,'count','Electrical panels and electrical rooms','Each gets authorized only, keep 36 inches clear and arc flash warnings.',2,'{"mfg":6,"warehouse":4,"datacenter":4,"utility":4,"office":2}','electrical','{electrical.0,electrical.1,electrical.2}',null,99),
 ('exits',null,30,'count','Exit doors','A keep exit clear sign on the inside of each exit door.',2,'{"warehouse":4,"mfg":4,"retail":3,"school":6}','exits','{exits.0}',null,99),
 ('notexit',null,31,'count','Doors people could mistake for an exit','Closets, stairwells and storage doors along the way out.',0,'{"office":2,"school":3,"retail":1}',null,'{exits.1}',null,50),
 ('public',null,40,'yesno','Customers or the public come on site','We add employees only signs on back-of-house doors.',0,'{"retail":1,"kitchen":1,"carwash":1,"fuelstop":1,"marina":1,"school":1,"office":1}','employee_only',null,null,1),
 ('contract',null,41,'yesno','Contractors or vendors work on site','We add a contractor check-in sign at the main entrance.',1,'{"office":0,"retail":0}',null,'{visitor.2}',null,1),
 ('spanish',null,42,'yesno','Some workers read Spanish first','We point out where bilingual custom signs help most.',0,null,null,null,null,1),
 ('forklift','{warehouse,mfg,cold,brewery,woodshop,retail}',50,'yesno','Forklifts or powered pallet jacks run here','Adds forklift traffic, walkway and trained operator signs.',1,'{"retail":0}','forklift',null,null,1),
 ('charge','{warehouse,mfg,cold,brewery,woodshop,retail}',51,'count','Battery charging spots','No smoking, eyewash and charging area signs at each.',1,'{"retail":0}','battery','{battery.0,battery.1,battery.2}',null,50),
 ('dock','{warehouse,mfg,cold,retail,brewery}',52,'count','Dock doors','Wheel chock and dock edge signs go at every door.',4,'{"retail":1,"brewery":1,"mfg":3,"warehouse":8}','dock','{dock.0,dock.1}',null,99),
 ('racks','{warehouse,retail}',53,'count','Pallet rack rows','Load limit and report damage signs at each row end.',6,'{"retail":0,"warehouse":12}','racking','{racking.0,racking.1}',null,99),
 ('machines','{mfg,woodshop,farm,auto,quarry}',60,'count','Machines with guards or moving parts','Guard, pinch point and lockout signs on each.',6,'{"farm":3,"auto":3,"quarry":4,"mfg":10}','machines','{machines.0,machines.1,machines.2,lockout.0}',null,99),
 ('welding','{mfg,auto,construction,farm}',61,'count','Welding or hot work areas','Arc ray and hot work permit signs at each.',1,'{"farm":0}','welding','{welding.0,welding.1}',null,30),
 ('cranes','{mfg,construction}',62,'count','Overhead cranes or hoists','Load and keep clear signs under each runway.',1,'{"construction":0}','crane','{crane.0,crane.1}',null,30),
 ('confined','{mfg,water,farm,oil_chem,brewery,utility,cold}',63,'count','Permit-required confined spaces','Tanks, pits, vaults, wet wells and bins. Each one needs a danger sign.',2,'{"water":4,"oil_chem":4,"brewery":2,"farm":1}','confined','{confined.0}',null,99),
 ('remote','{water}',64,'count','Lift stations or remote sites','Each gets a confined space, authorized only and electrical sign on top of the plant.',0,null,null,null,'{confined.0,visitor.1,electrical.0}',99),
 ('h2s','{water,oil_chem}',65,'yesno','H2S may be present','Adds H2S warnings at headworks, wet wells and sour service.',1,null,'h2s',null,null,1),
 ('subs','{utility}',70,'count','Substations or fenced equipment yards','High voltage keep out signs on every gate and fence side.',1,null,'high_voltage','{high_voltage.0,high_voltage.1}','{}',99),
 ('bins','{farm}',71,'count','Grain bins','Bin entry danger and auger signs at each.',3,null,'grain','{grain.0,grain.1}',null,99),
 ('livestock','{farm}',72,'yesno','Livestock on site','Adds livestock area, authorized only signs.',1,null,'livestock',null,null,1),
 ('fryers','{kitchen}',80,'count','Fryers','A hot oil warning at each fryer.',2,null,'kitchen','{kitchen.0}',null,20),
 ('hoods','{kitchen}',81,'count','Hood suppression pull stations','The manual pull must be clearly marked.',1,null,'kitchen','{kitchen.1}',null,10),
 ('walkins','{kitchen,retail,cold,brewery}',82,'count','Walk-in coolers and freezers','Inside door release and cold PPE signs at each.',2,'{"cold":4,"retail":2}','cold_storage','{cold_storage.0,cold_storage.1}',null,50),
 ('nh3','{cold}',83,'count','Ammonia machine rooms','Each needs a marked, restricted door.',1,null,'ammonia','{ammonia.0,ammonia.1}',null,10),
 ('lifts','{auto}',90,'count','Vehicle lifts','Authorized operator and stay clear signs at each lift.',4,null,'vehicle_lift','{vehicle_lift.0,vehicle_lift.1}',null,50),
 ('labs','{lab}',91,'count','Lab rooms','PPE and no food or drink signs on each lab door.',2,null,'lab','{lab.0,lab.1}',null,99),
 ('bio','{lab}',92,'yesno','Infectious or biohazard material is handled','Adds biohazard and sharps signs.',1,null,'biohazard',null,null,1),
 ('rad','{lab}',93,'yesno','X-ray, radiation or MRI on site','Adds radiation area and MRI magnet warnings.',0,null,'radiation',null,null,1),
 ('servers','{datacenter,office}',94,'count','Server rooms or network closets','Authorized access signs on each door.',2,'{"office":1}','restricted','{restricted.0,restricted.1}',null,50),
 ('agent','{datacenter}',95,'yesno','Clean agent or CO2 fire suppression','Adds do not enter after alarm warnings.',1,null,'fire_supp',null,null,1),
 ('ferm','{brewery}',96,'count','Rooms with fermenters or CO2 tanks','CO2 warning and ventilate signs at each door.',1,null,'co2','{co2.0,co2.1}',null,20),
 ('islands','{fuelstop,marina}',97,'count','Fuel pump islands','No smoking, engine off at each island.',4,'{"marina":1}','fuel_dispenser','{fuel_dispenser.0}',null,50),
 ('bays','{carwash}',98,'count','Self-serve wash bays','High pressure and PPE signs in each bay.',4,null,'pressure_wash','{pressure_wash.0,pressure_wash.1}',null,30),
 ('tunnel','{carwash}',99,'yesno','Automatic wash tunnel','Adds keep out and conveyor pinch point signs.',1,null,'car_tunnel',null,null,1),
 ('shops','{school}',100,'count','Shop or lab classrooms','Eye protection and instructor permission signs in each.',2,null,'shop_class','{shop_class.0,shop_class.1}',null,30),
 ('pool','{school}',101,'yesno','Pool on the property','Adds pool chemical storage and no lifeguard signs.',0,null,'pool',null,null,1),
 ('piers','{marina}',102,'count','Docks or piers with shore power','NEC 555.10 shock hazard signs at each dock.',3,null,'marina','{marina.0,marina.1}',null,50),
 ('trench','{construction,quarry}',103,'yesno','Open trenches or excavations','Adds keep back signs at the edges.',1,null,'excavation',null,null,1),
 ('mech','{office,school,retail,datacenter}',104,'count','Mechanical or boiler rooms','Authorized only signs on each door.',1,null,'mechanical_room','{mechanical_room.0}',null,30),
 ('roof','{office,school,retail}',105,'yesno','Roof hatch or roof access door','Adds a roof access, authorized only sign.',1,null,'roof',null,null,1)
on conflict (code) do update set facs=excluded.facs,ord=excluded.ord,kind=excluded.kind,label=excluded.label,help=excluded.help,def=excluded.def,fdef=excluded.fdef,area=excluded.area,slots=excluded.slots,adds=excluded.adds,maxv=excluded.maxv;
update finder.plan_extra e set ip=v.ip from (values ('CGAP-GEN001-812','Above each fire extinguisher'),('CGAP-GEN002-812','Above the first aid cabinet or kit'),('CGAP-GEN004-812','At entrances to areas requiring head protection'),('CGAP-GEN005-812','At entrances to eye protection areas'),('CGAP-GEN006-812','At entrances to high-noise areas'),('CGAP-GEN007-812','At doors and gates into vehicle or forklift areas'),('CGAP-GEN008-812','At plant and shop floor entrances'),('CGAP-GEN009-812','At site gates and main entrances'),('CGAP-GEN010-812','On doors to back-of-house and work areas'),('CGAP-GEN011-812','On or beside guarded machines'),('CGAP-GEN012-812','Next to rollers, gears and closing parts'),('CGAP-GEN013-812','On machines that need trained operators'),('CGAP-GEN014-812','At disconnects and on machines that get serviced'),('CGAP-GEN015-812','Above the lockout station or board'),('CGAP-GEN016-812','At aisle crossings and doorways into forklift areas'),('CGAP-GEN018-812','On rack end frames'),('CGAP-GEN019-812','Along conveyor lines near transfers and rollers'),('CGAP-GEN020-812','Along conveyors and at crossovers'),('CGAP-GEN021-812','Under crane runways and at bay entrances'),('CGAP-GEN022-812','In lifting and rigging areas'),('CGAP-GEN023-812','At welding bays and curtains'),('CGAP-GEN024-812','Where welding, cutting or grinding needs a permit'),('CGAP-GEN025-812','On chemical storage room doors and cages'),('CGAP-GEN026-812','Where acids, caustics and cleaners are stored or used'),('CGAP-GEN027-812','Above the SDS binder or station'),('CGAP-GEN028-812','At cylinder storage racks and carts'),('CGAP-GEN031-812','At entrances to loud equipment areas'),('CGAP-GEN033-812','At roof hatches, mezzanines and open edges'),('CGAP-GEN034-812','On roof hatches, ladders and stair doors'),('CGAP-GEN035-812','On mechanical room doors'),('CGAP-GEN036-812','On boiler room doors'),('CGAP-GEN037-812','On or near hot pipes, ovens and equipment'),('CGAP-GEN038-812','Along yard walkways and building exits'),('CGAP-GEN039-812','At yard gates and drive lanes'),('CGAP-GEN040-812','At trench and excavation edges'),('CGAP-GEN041-812','At jobsite gates and entrances'),('CGAP-GEN042-812','At freezer and cold room doors'),('CGAP-GEN043-812','On lab doors and benches'),('CGAP-GEN044-812','At CO2 tanks, manifold rooms and fermentation areas'),('CGAP-GEN045-812','At doors to tank rooms and low-lying areas'),('CGAP-GEN046-812','At wash tunnel entrances and exits'),('CGAP-GEN047-812','Along the tunnel conveyor and rollers'),('CGAP-GEN048-812','Near pressure washers and spray bays'),('CGAP-GEN049-812','At pressure washing stations'),('CGAP-GEN050-812','On doors to controlled and secure areas'),('CGAP-GEN051-812','On server room and data hall doors'),('CGAP-GEN052-812','On doors to equipment and server rooms'),('CGAP-GEN053-812','On battery room doors'),('CGAP-GEN054-812','On electrical and UPS equipment rooms'),('CGAP-GEN055-812','At doors to rooms with gas suppression'),('CGAP-GEN056-812','Inside and outside protected rooms'),('CGAP-GEN057-812','On or beside saws'),('CGAP-GEN058-812','At saw and cutting area entrances'),('CGAP-GEN059-812','Where fine dust collects'),('CGAP-GEN060-812','At doors and fences around flammable areas'),('CGAP-GEN061-812','On fuel pumps and dispenser islands'),('CGAP-GEN062-812','Next to the emergency fuel shutoff switch'),('CGAP-GEN063-812','At blast zone boundaries and haul road entrances'),('CGAP-GEN064-812','At quarry and pit entrances'),('CGAP-GEN065-812','Along haul roads and crossings'),('CGAP-GEN066-812','At site entrances and road junctions'),('CGAP-GEN067-812','On well house, booster station and tank site gates and doors'),('CGAP-GEN068-812','On pump rooms, well houses and pump control panels'),('CGAP-GEN069-812','On standby generators and generator enclosures'),('CGAP-GEN070-812','At chemical feed rooms, fill stations and unloading pads'),('CGAP-GEN071-812','At the plant gate and main entrance'),('CGAP-GEN072-812','At the plant gate and main entrance'),('CGAP-GEN073-812','At headworks, lagoons, lift stations and sludge areas'),('CGAP-GEN074-812','On lagoon fences and gates'),('CGAP-GEN075-812','On the tower leg, ladder cage and site fence'),('CGAP-GEN076-812','On chemical feed and storage room doors'),('CGAP-GEN077-812','At lift stations, wet wells, manholes and headworks'),('CGAP-GEN078-812','On vaults, wet wells, tanks, pits and manholes'),('CGAP-GEN079-812','On substation, regulator and capacitor bank gates and fences'),('CGAP-GEN080-812','On every side of the substation fence'),('CGAP-GEN081-812','On pad-mounted transformer and switchgear fences, bollards and nearby walls'),('CGAP-GEN082-812','Near pad-mounted equipment, underground risers and buried cable routes'),('CGAP-GEN083-812','On meter shop and meter test lab doors')) v(sku,ip) where e.sku=v.sku;
CREATE OR REPLACE FUNCTION finder.plan_build()
 RETURNS integer LANGUAGE plpgsql AS $function$
declare n int;
begin
insert into finder.plan_card select * from finder.cards(array(select distinct p.sku from finder.plan_pin p where p.sku not in (select sku from finder.plan_card) and p.sku not in (select sku from finder.plan_extra))) on conflict do nothing;
delete from finder.plan_pick;
with c as (
 select pc.k, pc.sku, pc.score/nullif(max(pc.score) over (partition by pc.k),0) rel,
   (pc.sku !~ '^CGAP-[A-Z][0-9]{5}-812$')::int legacy, finder.plan_tok(cd.subject) st, lower(coalesce(cd.industries,'')) ind
 from finder.plan_cand pc join finder.plan_card cd using(sku)),
sl as (select k, area, finder.plan_tok(q||' '||label) qt from finder.plan_slot),
f as (select code, rx, areas from finder.plan_fac union all select 'any', null, array(select code from finder.plan_area)),
s as (
 select f.code fac, c.k, c.sku,
   (select count(*) from unnest(c.st) x where x = any(sl.qt))::real / greatest(cardinality(c.st),1) prec,
   (select count(*) from unnest(c.st) x where x = any(sl.qt)) hits,
   coalesce(c.rel,0) rel, c.legacy, (f.rx is not null and c.ind ~ f.rx) im
 from f join sl on sl.area = any(f.areas) join c on c.k=sl.k),
z as (select fac,k,sku, row_number() over (partition by fac,k order by (prec + 0.35*rel + case when im then 0.25 else 0 end + 0.05*legacy) desc) rn
  from s where hits>=1 and prec>=0.34)
insert into finder.plan_pick select fac,k,rn,sku from z where rn<=4;
insert into finder.plan_pick(fac,k,rn,sku)
select f.code, p.k, -1000 + case when p.fac = f.code then 0 else 100 end + p.rank, p.sku
from (select code from finder.plan_fac union all select 'any') f join finder.plan_pin p on p.fac = f.code or (p.fac = 'any' and f.code <> 'any')
on conflict (fac,k,rn) do nothing;
delete from finder.plan_pick a using finder.plan_pick b where a.fac=b.fac and a.k=b.k and a.sku=b.sku and a.rn > b.rn;
insert into finder.plan_map(id,data,updated_at) values (1, jsonb_build_object(
 'v', extract(epoch from now())::bigint,
 'facilities', (select jsonb_agg(jsonb_build_object('code',code,'name',name,'areas',areas) order by ord) from finder.plan_fac),
 'areas', (select jsonb_object_agg(a.code, jsonb_build_object('label',a.label,'ord',a.ord,'slots',(select jsonb_agg(k order by ord) from finder.plan_slot s where s.area=a.code))) from finder.plan_area a),
 'slots', (select jsonb_object_agg(k, jsonb_strip_nulls(jsonb_build_object('label',label,'scope',scope,'pri',coalesce(pri,2),'why',why))) from finder.plan_slot),
 'questions', (select coalesce(jsonb_agg(jsonb_strip_nulls(jsonb_build_object('code',code,'facs',facs,'kind',kind,'label',label,'help',help,'def',def,'fdef',fdef,'area',area,'slots',slots,'adds',adds,'max',maxv)) order by ord),'[]'::jsonb) from finder.plan_q),
 'signs', (select jsonb_object_agg(sku, x) from (
     select c.sku, jsonb_strip_nulls(jsonb_build_object('h',c.handle,'s',c.subject,'c',c.series,'p',nullif(c.install_point,''))) x from finder.plan_card c where c.sku in (select sku from finder.plan_pick)
     union all select e.sku, jsonb_strip_nulls(jsonb_build_object('h',e.handle,'s',e.subject,'c',e.series,'p',nullif(e.ip,''))) from finder.plan_extra e where e.sku in (select sku from finder.plan_pick) and e.sku not in (select sku from finder.plan_card)) u),
 'picks', (select jsonb_object_agg(fac, m) from (select fac, jsonb_object_agg(k, arr) m from (select fac,k, jsonb_agg(sku order by rn) arr from finder.plan_pick group by fac,k) q group by fac) w)
), now()) on conflict (id) do update set data=excluded.data, updated_at=now();
select count(*) into n from finder.plan_pick; return n;
end $function$;
select finder.plan_build();
