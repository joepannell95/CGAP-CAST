"""Build the second set of 10 CGAP industry landing pages (curated areas, best sellers, FAQ)."""
import json, re, html, collections, sys

MAP = json.load(open('/home/claude/cgap/finder/sector_map.json'))
TOP = json.load(open('/home/claude/cgap/finder/top_sellers.json'))
rows = json.load(open('/home/claude/cgap/finder/signs.json'))
for r in rows:
    r['sector'] = MAP.get(r['sector'], r['sector'])

SR = {'DANGER': 1, 'WARNING': 2, 'CAUTION': 3, 'NOTICE': 4, 'SAFETY FIRST': 5}

P = [
 dict(sector='Ammonia Refrigeration & Cold Storage', handle='cold-storage-ammonia-refrigeration-safety-signs', term='cold storage', label='Cold Storage & Ammonia',
  title='Cold Storage & Ammonia Refrigeration Safety Signs',
  seo='Cold Storage & Ammonia Refrigeration Safety Signs | CGAP',
  desc='Ammonia machine room, relief valve, receiver, evaporator, blast freezer and cold dock safety signs for refrigerated warehouses. 8x12 aluminum.',
  intro=['An ammonia refrigeration system puts a toxic gas under pressure in the same building as forklift drivers, dock crews and outside contractors. The people who most need the warning are often the ones who have never been inside the machine room.',
         'These signs are written for the real parts of a cold storage plant: the machine room door and emergency shutdown, compressors and oil pots, relief valve headers, receivers and king valves, evaporators and defrost, blast cells, freezer docks and the eyewash by the coil wash. They are 8x12 aluminum, which holds up to freezer temperatures and washdown better than plastic signs that turn brittle in the cold.'],
  faq=[('What signs go on an ammonia machine room door?', 'Most plants post that the room contains ammonia and is for trained staff only, where the emergency shutdown and ventilation switches are, and what to do when the leak alarm sounds. Search "ammonia machine room" in the Sign Finder to see every option by install point.'),
       ('Will aluminum signs hold up in a freezer or blast cell?', 'Yes. Aluminum does not crack in the cold, and the print stays readable through frost and washdown.'),
       ('Do you have signs for evaporators, defrost and coil cleaning?', 'Yes, including evaporator fan guards, coil frost, defrost and coil cleaner rinse signs. Search the equipment name to see them.')],
  areas=[('Machine room and ventilation', r'machine(ry)? room|engine room|exhaust (fan|switch)|ventilation|emergency (stop|shut)', 'Entry, ventilation and emergency shutdown signs for the room that only trained staff should enter.'),
         ('Compressors and oil pots', r'compressor|oil (pot|drain|still|separator)|crankcase', 'Rotating equipment, hot discharge piping and oil draining steps.'),
         ('Relief valves and vent headers', r'relief|vent header|diffusion|purger|vent line', 'Where a release would come from and who has to stay clear.'),
         ('Receivers, vessels and king valves', r'receiver|king valve|vessel|accumulator|recirculat|surge drum|separator|pressure vessel', 'High pressure vessels and the valves that isolate the system.'),
         ('Evaporators and defrost', r'evaporator|defrost|\bcoil', 'Fans, coils and defrost cycles in the coolers and freezers.'),
         ('Leak alarms and detection', r'alarm|detector|detection|\bleak|emergency (stop|shut)', 'What everyone in the building does when the ammonia alarm goes off.'),
         ('Freezers, blast cells and docks', r'freezer|blast|spiral|\bdock|cold room|cooler door|cold store', 'Cold work areas, freezer doors and loading docks.'),
         ('Pressure tests, pump out and charging', r'pressure test|hydrostatic|pump out|charging|bleed|evacuat', 'Testing, evacuating and charging the system during service work.')]),
 dict(sector='Sawmills, Pulp & Paper', handle='sawmill-pulp-paper-mill-safety-signs', term='sawmill', label='Sawmills & Paper Mills',
  title='Sawmill, Pulp & Paper Mill Safety Signs',
  seo='Sawmill & Paper Mill Safety Signs | Kilns, Chippers | CGAP',
  desc='Log deck, debarker, head rig, chipper, dry kiln, paper machine and pulper safety signs for sawmills and pulp and paper mills. 8x12 aluminum.',
  intro=['A sawmill runs on equipment that does not forgive a slip: log decks that roll, debarkers that grab, band saws, chippers and a planer mill full of chains and sorters. A paper mill adds steam, nip points on rolls that move faster than anyone can react, and the chemicals that cook the pulp.',
         'These signs are written for those exact machines and spots, from the log yard to the dry kilns and from the pulper to the winder. Each one is 8x12 aluminum with pre-drilled holes for a guard, rail or machine frame, and it stays readable through sawdust, steam and washdown.'],
  faq=[('What safety signs does a sawmill need?', 'Start at the machines with the worst outcomes: the debarker and log deck, the head rig and saw line, the chipper and hog, and the kilns. Then add lockout reminders at each control station. The Sign Finder lists signs for each one by install point.'),
       ('Do you have signs for paper machines and winders?', 'Yes, including nip points, jog controls, lockout boards and broke chutes. Search "paper machine" to see them.'),
       ('Will these hold up to sawdust and steam?', 'Yes. They are rust-resistant aluminum with UV-stable print, and they wipe clean, so they stay readable in dusty and damp mills.')],
  areas=[('Log yards and log decks', r'\blog\b|\blogs\b|log (yard|deck|loader|crane|kicker|haul)', 'Loaders, log decks and the yard traffic around them.'),
         ('Debarkers', r'debark', 'Drum and ring debarkers, bark conveyors and the platforms above them.'),
         ('Head rig and saw line', r'head ?rig|band ?saw|saw line|carriage|edger|trimmer|gang ?saw|resaw|circular saw|saw blade', 'Band saws, carriages, edgers and trimmers on the main line.'),
         ('Chippers and hogs', r'chipper|\bhog\b|chip (van|bin|screen|pile)|bedknife', 'Chippers, hogs and the chip handling that follows them.'),
         ('Planer mill, sorters and stackers', r'planer|sorter|stacker|green chain|lumber|moulder|sticker', 'Planers, sorters, stackers and the chains between them.'),
         ('Dry kilns', r'kiln', 'Kiln doors, fans, baffles and the heat inside.'),
         ('Paper machines and winders', r'paper machine|winder|dryer|calender|\breel\b|\bnip\b|felt|wire section', 'Nip points, dryer sections, reels and winders.'),
         ('Pulpers, digesters and chemical areas', r'pulper|digester|\bpulp|black liquor|recovery boiler|bleach|chlorine dioxide|caustic|lime kiln', 'Pulpers, digesters and the chemicals used to make pulp.')]),
 dict(sector='Gas Distribution, Propane & Pipelines', handle='propane-natural-gas-pipeline-safety-signs', term='propane', label='Propane & Natural Gas',
  title='Propane, Natural Gas & Pipeline Safety Signs',
  seo='Propane & Natural Gas Pipeline Safety Signs | CGAP Safety',
  desc='Regulator station, propane bulk plant, cylinder cage, pipeline right of way, pig launcher and cathodic protection safety signs. 8x12 rust-resistant aluminum.',
  intro=['Gas utilities and propane dealers have two audiences: trained crews who need clear procedure reminders at the equipment, and the public, who need to know to stay back, not smoke and call before they dig.',
         'These signs cover regulator and meter stations, propane bulk plants and bobtail loading, cylinder exchange cages, pipeline right of way, pig launchers and receivers, cathodic protection rectifiers, odorant and leak response, and LNG and compressor stations. They are 8x12 aluminum and stand up to sun and weather on a fence, cage or skid.'],
  faq=[('What signs does a propane bulk plant need?', 'Typical postings cover no smoking or open flames, the transfer and loading area, the emergency shutoff location and who to call in an emergency. Search "propane bulk plant" to see the options by install point.'),
       ('Do you have signs for cylinder exchange cages?', 'Yes, including signs for customers and staff at the cage, the bollards and the customer lane. Search "cylinder exchange".'),
       ('Can these mount on chain link or a station fence?', 'Yes. The pre-drilled corners take zip ties, wire or bolts for fence panels, cages and skids.')],
  areas=[('Regulator and meter stations', r'regulator|\bmeter', 'Station fences, regulators, meters and filter separators.'),
         ('Propane bulk plants and loading', r'bulk (plant|tank|storage)|bobtail|propane (tank|transfer|truck|delivery|pump)|transport unload|loading rack', 'Bulk tanks, bobtail racks and transfer areas.'),
         ('Cylinder exchange and filling', r'propane cylinder|cylinder (exchange|cage|fill|valve|storage|scale)|exchange cage|\bcage\b|refill', 'Exchange cages, filling stations and cylinder storage.'),
         ('Pipeline right of way', r'pipeline|right.of.way|marker|excavat|\bdig|buried|one.?call|811', 'Markers and warnings for the public and for anyone digging.'),
         ('Pig launchers and receivers', r'\bpig', 'Closures, interlocks and pressure on launchers and receivers.'),
         ('Cathodic protection', r'cathodic|rectifier|anode|\bcp\b', 'Rectifiers, test stations and anode beds.'),
         ('Odorant and leak response', r'odor|mercaptan|\bleak|detector|gas detection', 'Odorant equipment and what to do when someone smells gas.'),
         ('LNG and compressor stations', r'\blng\b|compressor|vaporizer|boil.?off|cryogenic', 'Vaporizers, boil off compressors and cold piping.')]),
 dict(sector='Schools, Theaters & Maker Spaces', handle='school-shop-class-theater-safety-signs', term='school', label='Schools & Theaters',
  title='School Shop, Science Lab & Theater Safety Signs',
  seo='School Shop, Lab & Theater Safety Signs | CGAP Safety',
  desc='Wood shop, welding shop, laser cutter, science lab, kiln, stage rigging and gym safety signs for schools, colleges and maker spaces. 8x12 aluminum.',
  intro=['Schools put new users in front of real equipment every day: a table saw in the wood shop, a welder in ag mechanics, a laser cutter in the maker space and a fly system over the stage. The sign at the machine is often the last reminder before a student makes a mistake.',
         'These signs are written for those spots, including wood and metal shops, CNC and laser cutters, science labs and chemical storage, kiln and glass rooms, stage rigging and followspots, gyms and bleachers, and the boiler room. They are 8x12 aluminum, so they stay up and stay readable through years of classes.'],
  faq=[('What safety signs should a school wood shop have?', 'Post signs at each machine for guards, eye protection and keeping hands clear, plus reminders where students should not start a machine on their own. Search the machine name, like "table saw" or "jointer", to see the options.'),
       ('Do you have signs for theaters and stage rigging?', 'Yes, including counterweight arbors, fly rails, orchestra pit lifts, catwalks and followspots. Search "stage rigging" or "fly system".'),
       ('Are these signs good for maker spaces and libraries too?', 'Yes. Laser cutters, 3D printers, CNC routers and soldering stations all have signs written for them.')],
  areas=[('Wood shop', r'table saw|band ?saw|jointer|planer|\brouter|wood ?lathe|miter|sander|wood', 'Saws, jointers, planers and sanders.'),
         ('Metal shop and welding', r'weld|forge|grinder|metal|plasma|engine lathe|metal lathe|anvil|foundry', 'Welding booths, forges, grinders and metal lathes.'),
         ('Laser cutters, CNC and 3D printers', r'laser|\bcnc\b|3d print|solder', 'Maker space and fab lab equipment.'),
         ('Science labs and chemical storage', r'chemi|\blab\b|laborator|fume hood|eyewash|gas cylinder|bunsen', 'Chemistry rooms, fume hoods and chemical storage.'),
         ('Kilns, ceramics and glass', r'kiln|ceramic|glass|glory hole|pottery|annealer|clay', 'Kiln rooms, pottery studios and hot glass.'),
         ('Stage rigging and theater', r'rigging|\bfly\b|counterweight|batten|followspot|stage|catwalk|\btrap\b|orchestra|lineset', 'Fly systems, catwalks, pit lifts and lighting positions.'),
         ('Gyms, bleachers and athletics', r'bleacher|\bgym|weight|\btrack\b|field|pool|basketball|wrestling', 'Bleachers, weight rooms, pools and fields.'),
         ('Fire, exits and emergency gear', r'extinguisher|\bexit|eyewash|emergency|first aid|fire blanket|evacuat', 'Extinguishers, eyewash, exits and emergency stops.')]),
 dict(sector='Data Centers & Telecom', handle='data-center-server-room-safety-signs', term='data center', label='Data Centers',
  title='Data Center, Server Room & Telecom Safety Signs',
  seo='Data Center & Server Room Safety Signs | UPS, Battery | CGAP',
  desc='UPS and battery room, switchgear, generator, fire suppression, CRAH, raised floor and telecom vault safety signs for data centers. 8x12 aluminum.',
  intro=['A data center packs more stored energy into one building than most factories: UPS battery strings, switchgear, standby generators with fuel, and fire suppression systems that can discharge with people in the room. Many of the people walking the floor are vendors and contractors who do not know the site.',
         'These signs are written for the white space and the gray space: UPS rooms and battery racks, electrical rooms and PDUs, generator yards, fire suppression zones, CRAH units and cooling towers, raised floors and cable trays, fiber and laser work, and telecom vaults. They are 8x12 aluminum and mount on doors, racks, cages and walls.'],
  faq=[('What signs go on a UPS or battery room door?', 'Typical postings cover authorized personnel only, the electrical and chemical hazards from the batteries, no open flames and the PPE required inside. Search "UPS battery room" to see every option by install point.'),
       ('Do you have signs for generator yards and fuel tanks?', 'Yes, including standby generator, day tank and fuel delivery signs. Search "generator" to see them.'),
       ('Do you make signs for telecom vaults and huts?', 'Yes, including vault atmosphere testing, attendant and roadside signs. Search "telecom vault".')],
  areas=[('UPS rooms and battery strings', r'\bups\b|battery', 'UPS modules, battery racks and battery rooms.'),
         ('Electrical rooms and switchgear', r'switchgear|\bpdu\b|\brpp\b|busway|arc flash|electrical room|transformer|breaker|power panel|bus duct|\bats\b|transfer switch', 'Switchgear, PDUs, busway and electrical rooms.'),
         ('Generators and fuel', r'generator|\bfuel|day tank|belly tank', 'Standby generators, day tanks and fuel deliveries.'),
         ('Server rooms and racks', r'server|white space|hot aisle|cold aisle|rack row|cage aisle|clean agent|containment door', 'Server rooms, racks, cages and aisle containment.'),
         ('Cooling units, chillers and towers', r'\bcrah\b|\bcrac\b|chiller|cooling|hot aisle|cold aisle|condenser', 'CRAH units, chillers, cooling towers and aisle containment.'),
         ('Raised floors and cable trays', r'raised floor|floor tile|cable tray|ladder rack|overhead tray|underfloor|floor panel|perforated tile', 'Open floor tiles, overhead trays and cable work.'),
         ('Fiber, lasers and splicing', r'fiber|laser|splic', 'Fiber testing, splicing and laser light sources.'),
         ('Telecom vaults, huts and towers', r'vault|manhole|\bhut\b|telecom|cell site|tower base|central office|outside plant', 'Vaults, huts, cabinets and tower sites.')]),
 dict(sector='Batteries, Energy Storage & EV', handle='lithium-battery-energy-storage-ev-safety-signs', term='battery', label='Batteries & EV',
  title='Lithium Battery, Energy Storage & EV Safety Signs',
  seo='Lithium Battery, BESS & EV Charging Safety Signs | CGAP',
  desc='E-bike charging, lithium battery storage, BESS, battery room, EV service and damaged battery signs for apartments, shops and energy storage. 8x12 aluminum.',
  intro=['Lithium batteries are now in every apartment hallway, shop and parking garage, and a damaged or badly charged battery can go into thermal runaway with almost no warning. Our e-bike charging and lithium battery storage signs are among the most ordered signs we make.',
         'This page covers the whole range: e-bike and scooter charging rules, lithium battery storage, battery energy storage systems (BESS), lead-acid battery rooms and forklift charging, EV service bays and high voltage work, EV chargers, damaged battery quarantine, and battery recycling and cell manufacturing. Every sign is 8x12 aluminum, a better choice than plastic near heat and chargers.'],
  faq=[('Where should an e-bike charging sign go?', 'Post them wherever tenants or staff might charge a battery indoors: building entrances, hallways, stairwells, bike rooms and garages. Search "e-bike charging" to see the options.'),
       ('Do you have signs for battery energy storage systems?', 'Yes, including BESS container doors, high voltage and authorized personnel signs. Search "BESS" or "energy storage".'),
       ('What signs does an EV service bay need?', 'Typical postings cover high voltage work in progress, keeping untrained staff clear and the battery disconnect steps. Search "EV service" to see them.')],
  areas=[('E-bike and lithium battery charging', r'e-?bike|scooter|lithium|charging prohibited', 'Charging rules for apartments, garages, shops and offices.'),
         ('Battery energy storage systems (BESS)', r'\bbess\b|energy storage|\bess\b', 'BESS containers, cabinets and the fence around them.'),
         ('Battery rooms and forklift charging', r'battery room|lead.?acid|forklift (battery|charging)|battery (watering|charging|charger|changer)|electrolyte|hydrogen|charging area', 'Lead-acid rooms, watering stations and charging areas.'),
         ('EV service and high voltage', r'\bev\b|high.?voltage|electric vehicle|orange cable|hybrid', 'Service bays where high voltage packs are worked on.'),
         ('EV chargers', r'charger|charging station|dc fast|\bevse\b|charging cable', 'Public and fleet charging stations.'),
         ('Damaged battery quarantine', r'damaged|quarantine|thermal runaway|isolation|containment|swollen', 'Holding areas for damaged, swollen or recalled batteries.'),
         ('Battery recycling and disassembly', r'recycl|shred|disassembl|sorting|black mass', 'Pack teardown, shredding and sorting lines.'),
         ('Cell manufacturing and testing', r'formation|cycler|test chamber|\bcells?\b|dry room|grading|electrode', 'Formation, test chambers and cell production.')]),
 dict(sector='Venues, Parks & Attractions', handle='park-shooting-range-venue-safety-signs', term='park', label='Parks, Ranges & Venues',
  title='Park, Shooting Range, Lake & Venue Safety Signs',
  seo='Park, Gun Range & Lake Safety Signs | Venues | CGAP Safety',
  desc='Gun range, hunting area, deep water, reservoir, algae, ride, stage rigging, pool and lightning safety signs for parks, ranges and venues. 8x12 aluminum.',
  intro=['Parks, ranges and venues are full of people who have never been there before. A Gun Range sign at the gate, a Deep Water Drop Off sign at the shoreline and a lightning warning at the field do more than any rule sheet, because they stand right where the hazard is.',
         'This page covers shooting ranges and hunting land, lakes, reservoirs and ponds, rides and attractions, stage rigging and arenas, pools and water parks, animal exhibits, and weather and wildfire warnings. Every sign is 8x12 rust-resistant aluminum with UV-stable print, made to live outside.'],
  faq=[('What signs should a shooting range post?', 'Typical postings are a live fire warning at every entrance, hearing and eye protection reminders at the firing line and keep out signs on the perimeter. Search "gun range" or "shooting" to see the options.'),
       ('Do you have signs for lakes and ponds?', 'Yes, including deep water drop off, unstable bank edge and toxic blue-green algae warnings. Search "deep water" or "algae".'),
       ('Will these signs fade outside?', 'They are printed with UV-stable inks on rust-resistant aluminum, built for posts, fences and gates in full sun.')],
  areas=[('Shooting ranges and hunting land', r'gun range|shooting|firing range|live fire|hunting|archery|skeet|bullet trap|range target|target carrier', 'Live fire warnings, firing lines and range perimeters.', dict(any=True, exclude=r'blast|alignment|aircraft')),
         ('Lakes, reservoirs and ponds', r'reservoir|deep water|drop.?off|algae|\bswim|\blake|\bpond|drown|bank edge|shore', 'Shorelines, swimming areas and water quality warnings.'),
         ('Rides and attractions', r'\bride|coaster|zip ?line|attraction|kart|bumper|trampoline', 'Ride entrances, queues and maintenance areas.'),
         ('Stage rigging and arenas', r'rigging|counterweight|\bfly\b|truss|stage|orchestra|catwalk|arena|stadium', 'Rigging, catwalks, pit lifts and overhead loads.'),
         ('Pools and water parks', r'\bpool|wave|\bslide|splash', 'Pools, wave pools, slides and splash pads.'),
         ('Zoos and animal areas', r'animal|aviary|\bzoo|keeper|exhibit', 'Keeper areas, gates and animal exhibits.'),
         ('Weather and wildfire', r'lightning|wildfire|storm|fire risk|fire danger|heat illness|severe weather', 'Lightning, storm and wildfire warnings.'),
         ('Mechanical and maintenance areas', r'hydraulic|\bhoist|maintenance|winch|cable reel', 'Hydraulic units, hoists and back-of-house work.')]),
 dict(sector='Chemical Plants & Handling', handle='chemical-plant-storage-safety-signs', term='chemical', label='Chemical Plants',
  title='Chemical Plant & Chemical Storage Safety Signs',
  seo='Chemical Plant & Chemical Storage Safety Signs | CGAP',
  desc='Acid, caustic, chlorine, ammonia, regulated area, solvent storage, reactor, tank car unloading and hazardous waste safety signs. 8x12 rust-resistant aluminum.',
  intro=['Chemical hazards are specific. A sign that just says "Chemicals" does not tell anyone that a regulated area needs an entry log, that a reactor cannot be restarted with the agitator off, or that a tank car has to be chocked and grounded before the hose goes on.',
         'These signs are written for each chemical and each step: acids and corrosives, toxic gases like chlorine and ammonia, OSHA regulated areas such as methylene chloride and benzene, flammable solvent storage, reactors and process vessels, tank car and tank truck unloading, line breaking, and hazardous waste and spill response. They are 8x12 rust-resistant aluminum.'],
  faq=[('Do you have signs for OSHA regulated areas?', 'Yes, including methylene chloride, benzene, cadmium and other regulated area signs, plus entry log signs. Search the chemical name to see them.'),
       ('Which signs go in a chemical storage room?', 'Typical postings name the hazard stored there, separate incompatible chemicals, list the PPE required and show where the eyewash and spill kit are. Search "chemical storage" to see the options.'),
       ('Do you sell signs for individual chemicals?', 'Yes. Many signs are written for one chemical, such as hydrofluoric acid, chlorine, caustic soda or methylene chloride. Search the chemical name to find them.')],
  areas=[('Acids and corrosives', r'\bacid|caustic|corrosive|hydrofluoric|sulfuric|hydrochloric|nitric|sodium hydroxide', 'Acid and caustic storage, transfer and splash zones.'),
         ('Toxic gases', r'chlorine|ammonia|\bh2s\b|hydrogen sulfide|phosgene|toxic|cyanide', 'Chlorine, ammonia and other toxic gas areas.'),
         ('OSHA regulated areas', r'regulated area|benzene|methylene|formaldehyde|cadmium|arsenic|acrylonitrile|butadiene|ethylene oxide', 'Regulated areas, entry logs and exposure limits.'),
         ('Flammable solvents and storage', r'flammable|solvent|chemical storage|storage cabinet|blending', 'Solvent rooms, flammable storage and blending.'),
         ('Reactors and process vessels', r'reactor|kettle|vessel|agitator|column|\bstill\b', 'Reactors, kettles, agitators and columns.'),
         ('Tank car and tank truck unloading', r'unload|tank car|railcar|tank truck|\btote', 'Rail and truck unloading spots.'),
         ('Line breaking and piping', r'line break|piping|\bpipe|\bhose|flange', 'Opening lines, process piping and hoses.'),
         ('Hazardous waste and spills', r'\bwaste|spill|filter cake', 'Waste storage, drums and spill response.')]),
 dict(sector='Waste & Recycling', handle='waste-recycling-transfer-station-safety-signs', term='recycling', label='Waste & Recycling',
  title='Waste, Recycling & Transfer Station Safety Signs',
  seo='Waste & Recycling Facility Safety Signs | Balers, MRF | CGAP',
  desc='Baler, compactor, MRF sort line, tipping floor, scale house, landfill and battery sorting safety signs for waste and recycling facilities. 8x12 aluminum.',
  intro=['Waste and recycling sites mix heavy equipment, moving conveyors, the public and loads nobody has looked inside. A tipping floor with a loader backing up, a baler that can restart and a lithium battery hidden in a load of cardboard are everyday hazards here.',
         'These signs are written for the parts of a site where people get hurt: balers and compactors, MRF sort lines and screens, tipping floors and push walls, scale houses and public drop-off areas, landfill working faces, shredders, collection trucks and containers, and battery and hazardous waste sorting. They are 8x12 aluminum and hold up to dust, washdown and weather.'],
  faq=[('What signs does a baler or compactor need?', 'Typical postings cover lockout before clearing a jam, keeping hands out of the chamber, who is allowed to run it and the restart hazard. Search "baler" or "compactor" to see every option by install point.'),
       ('Do you have signs for scale houses and public drop-off areas?', 'Yes, including scale house, customer lane and keep clear of equipment signs. Search "scale house" or "drop-off".'),
       ('Do you make signs for battery sorting and hazardous waste?', 'Yes. Lead Acid Battery Sorting is one of the most ordered signs in this industry, and there are signs for lithium batteries, cylinders and other loads that should never go in a compactor. Search "battery sorting".')],
  areas=[('Balers and compactors', r'baler|compactor|\bbale', 'Chambers, rams and jam clearing on balers and compactors.'),
         ('MRF sort lines and screens', r'sort(ing)? (line|belt|station|conveyor|cabin|room)|pre-?sort|picking|optical|disc screen|star screen|trommel|\bmrf\b|occ screen|screen deck', 'Pre-sort, picking stations, screens and optical sorters.'),
         ('Tipping floors and push walls', r'tipping|push wall|tip floor|transfer (floor|station)|floor loader|wheel loader', 'Loaders, trucks and people on the tipping floor.'),
         ('Scale houses and public drop-off', r'\bscale|drop.?off|customer|public|convenience|residential', 'Scale houses, customer lanes and public drop-off areas.'),
         ('Landfill working face and gas', r'landfill|working face|leachate|landfill gas|\bflare|methane|compactor wheel', 'The working face, leachate and landfill gas systems.'),
         ('Shredders and grinders', r'shredder|grinder|crusher|granulator|tub grinder', 'Shredders, tub grinders and granulators.'),
         ('Battery and hazardous waste sorting', r'battery|hazardous|lithium|propane|cylinder|household hazardous|e-?waste', 'Batteries, cylinders and household hazardous waste.'),
         ('Collection trucks and containers', r'packer|roll.?off|dumpster|cart tipper|container tilter|refuse truck|garbage truck|collection truck|side loader|rear loader|front loader', 'Packer trucks, roll-offs, containers and hoppers.')]),
 dict(sector='Mining, Quarries & Asphalt', handle='mining-quarry-asphalt-plant-safety-signs', term='quarry', label='Mining & Quarries',
  title='Mining, Quarry & Asphalt Plant Safety Signs',
  seo='Mining, Quarry & Asphalt Plant Safety Signs | CGAP Safety',
  desc='Blasting, crusher, conveyor, screen, haul road, highwall, stockpile and asphalt plant safety signs for mines, quarries and aggregate pits. 8x12 aluminum.',
  intro=['Quarries and mines move more material per hour than almost any other industry, and the equipment does not stop for anyone: crushers, conveyors, screens, haul trucks that cannot see a pickup, and stockpiles that can bury a person who walks too close.',
         'These signs are written for those spots, from the blasting area and the highwall to the primary crusher, conveyors and screens, stockpiles and reclaim tunnels, haul roads, asphalt plants and underground work. They are 8x12 rust-resistant aluminum made for dust, rain and vibration.'],
  faq=[('What signs should go at a quarry entrance?', 'Typical postings cover blasting warnings, hard hat and high visibility requirements, haul truck right of way and checking in at the office. Search "blasting" or "haul road" to see the options.'),
       ('Do you have signs for crushers and conveyors?', 'Yes, including lockout before clearing a jam, pinch points, belt cleaning and staying off the conveyor. Search "crusher" or "conveyor".'),
       ('Do you make signs for asphalt plants?', 'Yes, including hot mix silos, drum dryers, burners, liquid asphalt tanks and truck load out. Search "asphalt plant".')],
  areas=[('Blasting and explosives', r'\bblasting\b|blast (area|guard|zone|site|warning|signal)|explosive|detonat|powder magazine|misfire|blasthole|shot ?fir', 'Blast areas, magazines, guards and all clear signals.', dict(any=True, exclude=r'abrasive|sand ?blast|blast tube|air blast|shot ?blast|blast (freezer|chiller|cell|room|cabinet|pot|chamber)|pyro|firework|stage|show')),
         ('Crushers', r'crusher|\bjaw\b|cone|impactor|primary', 'Primary, secondary and portable crushers.'),
         ('Conveyors and screens', r'conveyor|screen|\bbelt|tail pulley|head pulley|idler|stacker', 'Belts, pulleys, screens and radial stackers.'),
         ('Stockpiles and reclaim tunnels', r'stockpile|reclaim|surge pile|feeder|hopper|\bbin\b|batching', 'Stockpiles, reclaim tunnels, feeders and hoppers.'),
         ('Haul roads and mobile equipment', r'\bhaul|haul truck|loader|dozer|\bberm|road', 'Haul roads, berms and blind spots around big equipment.'),
         ('The pit: drilling, faces and scales', r'highwall|bench edge|quarry|stockpile face|ground control|loose rock|rock ?fall|drill', 'Drilling, stockpile faces, truck scales and the wheel wash.'),
         ('Asphalt plants', r'asphalt|hot mix|drum dryer|baghouse|burner|\bsilo', 'Drum dryers, burners, silos and liquid asphalt tanks.'),
         ('Underground work', r'underground|jackhammer|tunnel|mine shaft|portal|roof bolt|\bmine\b', 'Shafts, tunnels, portals and drilling underground.')]),
]

def esc(s): return html.escape(s or '', quote=True)

def picks_for(pool, rx, used, n=4):
    c = re.compile(rx, re.I)
    hits = [r for r in pool if c.search((r.get('subject') or '') + ' ' + (r.get('equipment') or ''))]
    hits.sort(key=lambda r: (-(r.get('units', 0) > 1), -r.get('units', 0), 0 if c.search(r.get('subject') or '') else 1, SR.get(r['series'], 9), len(r.get('subject') or '')))
    out, seen_subj, seen_series = [], set(), collections.Counter()
    def ok(r):
        return r['handle'] not in used and (r.get('subject') or '').lower() not in seen_subj
    for r in hits:  # best sellers first
        if len(out) >= n or r.get('units', 0) <= 1: break
        if ok(r): out.append(r); seen_subj.add(r['subject'].lower()); seen_series[r['series']] += 1
    for rnd in range(4):  # then the most serious series, one of each before repeats
        for r in hits:
            if len(out) >= n: break
            if not ok(r) or seen_series[r['series']] > rnd: continue
            if not c.search(r.get('subject') or '') and rnd < 2: continue  # subject matches first
            out.append(r); seen_subj.add(r['subject'].lower()); seen_series[r['series']] += 1
    for r in hits:
        if len(out) >= n: break
        if ok(r): out.append(r); seen_subj.add(r['subject'].lower())
    for r in out: used.add(r['handle'])
    return hits, out

def li(r):
    return f'<li><span data-s="{esc(r["series"])}">{esc(r["series"])}</span><a href="/products/{esc(r["handle"])}">{esc(r["subject"])}</a></li>'

report, pages = [], []
for p in P:
    pool = [r for r in rows if r['sector'] == p['sector']]
    tops = [dict(series=t['s'], handle=t['h'], subject=t['t'], equipment='', install_point='', units=t['u'] + 1) for t in TOP if t['sec'] == p['sector']]
    pool_all = tops + pool
    areas_html = []
    used = set()
    sold = [t for t in tops if t['units'] > 1]
    if sum(t['units'] - 1 for t in sold) >= 5:
        best = sorted(sold, key=lambda t: -t['units'])[:4]
        areas_html.append(f'<div class="il-area il-best"><h3>Most ordered</h3><p>The signs customers in this industry order most.</p><ul>{"".join(li(r) for r in best)}</ul></div>')
    for area in p['areas']:
        label, rx, blurb = area[:3]
        opt = area[3] if len(area) > 3 else {}
        src = pool_all
        if opt.get('any'):
            ex = re.compile(opt.get('exclude', r'^$'), re.I)
            src = tops + [r for r in rows if not ex.search(r.get('subject') or '')]
        hits, chosen = picks_for(src, rx, used)
        report.append((p['handle'], label, len(hits), [c['subject'] for c in chosen]))
        if len(chosen) < 2: continue
        ip = next((h['install_point'] for h in chosen if h.get('install_point')), '')
        ip = ip.strip().rstrip('.')
        meta = f'{len(hits)} signs.' + (f' Typical spot: {esc(ip)}.' if ip else '')
        areas_html.append(f'<div class="il-area"><h3>{esc(label)}</h3><p>{esc(blurb)} {meta}</p><ul>{"".join(li(r) for r in chosen)}</ul></div>')
    faq_html = ''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p['faq'])
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]}
    body = (f'<div data-cgap-sector="{esc(p["sector"])}" data-cgap-term="{esc(p["term"])}"></div>'
            + ''.join(f'<p class="lead">{esc(t)}</p>' if i == 0 else f'<p>{esc(t)}</p>' for i, t in enumerate(p['intro']))
            + f'<h2>What to post, and where</h2><div class="il-areas">{"".join(areas_html)}</div>'
            + f'<h2>Common questions</h2><div class="il-faq">{faq_html}</div>'
            + f'<script type="application/ld+json">{json.dumps(ld)}</script>')
    for bad in ['—', '–']:
        assert bad not in body, (p['handle'], bad)
    pages.append(dict(sector=p['sector'], handle=p['handle'], label=p['label'], title=p['title'], seo=p['seo'], desc=p['desc'], body=body, n=len(pool)))
    open(f'/home/claude/cgap-cast/theme/snippets/ilp-{p["handle"]}.liquid', 'w').write(body)

json.dump(pages, open('/home/claude/cgap/finder/landing_pages2.json', 'w'))
for h, label, n, ch in report:
    flag = '  <-- THIN' if len(ch) < 2 else ('  <- few' if n < 4 else '')
    print(f'{h[:28]:28} | {label[:34]:34} | {n:4} | {"; ".join(ch)[:120]}{flag}')
for pg in pages:
    print(pg['handle'], pg['n'], len(pg['body']), len(pg['seo']), len(pg['desc']))
