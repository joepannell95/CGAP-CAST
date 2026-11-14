# Ordered (fac, [substrings]) used on product pages, matched against the lowercased "Sector:" tag.
R=[('marina',['marina','boatyard','boat ramp','dock and pier','harbor','yacht','waterfront']),
('carwash',['car wash','detailing']),
('fuelstop',['gas station','truck stop','fuel station','fuel terminal','fuel island','convenience store']),
('datacenter',['data center','server room']),
('brewery',['brew','distill','winer','taproom']),
('cold',['cold storage','ammonia','freezer','refrigerated warehouse']),
('kitchen',['restaurant','kitchen','bakery','catering','food truck','cafeteria','coffee','pizza','diner','food service']),
('lab',['hospital','clinic','medical','dental','chiropract','laborator',' lab ',' labs ','pharma','veterinar','nursing','senior care','imaging','mri ','dialysis','infusion']),
('school',['school','librar','campus','college','universit','child care','daycare','preschool','apartment','condo','townhome','hoa ','property','church','playground']),
('farm',['farm','grain','feed','livestock','dairy','poultry','orchard',' ranch','agricult','vineyard','greenhouse']),
('auto',['auto ','automotive',' tire','body shop','fleet','dealership','mechanic shop','collision','diesel shop','motorcycle shop']),
('water',['wastewater','water treatment','water plant','sewer','lift station','pump station','pump house','well house','water utilit','water and']),
('utility',['electric utilit','substation','telecom','utility','solar','wind farm','wind turbine','battery','power plant','transmission','ev charging']),
('oil_chem',['oil and gas','oilfield','oil field','oil well','gas well','refiner','chemical','propane','pipeline','petro','hydrogen']),
('quarry',['quarry','mines','mining','aggregate','asphalt','gravel']),
('woodshop',['sawmill','lumber','woodwork','wood shop','pallet','timber','paper mill']),
('construction',['construction','contractor','job site','jobsite','demolition','roofing','excavat']),
('warehouse',['warehouse','distribution','logistic','loading dock','freight','fulfillment','self storage']),
('mfg',['manufactur','factory','foundry','fabricat','assembly','machine shop','processing plant','plant floor',' plants','plant ']),
('office',['office','commercial building',' bank ','credit union','coworking','city hall','courthouse']),
('retail',['retail','store','grocery','mall','salon','boutique']),]
def fac(s):
    s=' '+s.lower()+' '
    return next((c for c,ks in R if any(k in s for k in ks)),None)
