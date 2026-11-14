M = {
'mfg':('a manufacturing plant','manufacturing-and-industrial-signs manufacturing-plant-sign-kits metal-shop-sign-kits metal-foundry-and-fabrication-plant-signs plastics-electronics-and-assembly-plant-signs printing-sign-and-packaging-plant-signs textile-and-apparel-plant-signs additive-manufacturing-sign-kits meat-seafood-and-game-processing-signs electrical-equipment-plant-sign-kits medical-device-plant-sign-kits appliance-plant-sign-kits boat-and-rv-plant-sign-kits'),
'warehouse':('a warehouse','warehouse-and-distribution-center-signs warehouse-sign-kits warehouses-and-logistics-signs loading-dock-warehouse-signs forklift-pedestrian-signs moving-company-signs'),
'construction':('a construction site','construction-and-trades-signs construction-sign-kits highway-construction-sign-kits electrical-plumbing-and-hvac-contractor-signs'),
'farm':('a farm','agriculture agriculture-and-farms-signs aquaculture-farm-signs farm-and-grain-sign-kits grain-bin-entry-signs grain-seed-and-cotton-signs livestock-dairy-and-poultry-farm-signs orchard-farm-stand-and-market-signs'),
'kitchen':('a restaurant or kitchen','commissary-and-catering-kitchen-signs restaurant-front-of-house-signs restaurant-kitchen-signs restaurant-sign-kits restaurants-and-bars-signs bakery-coffee-roaster-and-candy-signs coffee-ice-cream-and-dessert-shop-signs food-truck-and-concession-signs bar-taproom-and-nightclub-signs'),
'auto':('an auto or fleet shop','auto-repair-and-body-shop-signs auto-shop-sign-kits automotive-and-fleet-signs car-dealership-and-used-car-lot-signs fleet-maintenance-sign-kits tire-shop-signs fleet-and-marine-sign-kits'),
'water':('a water or wastewater plant','water-wastewater-sign-kits water-and-wastewater-signs dam-and-lock-sign-kits canal-sign-kits'),
'utility':('a utility, telecom or substation site','electric-co-op-sign-kits electric-utility-and-co-op-signs energy-utilities-and-telecom-signs telecom-and-broadband-signs telecom-sign-kits utility-infrastructure-signs solar-wind-and-battery-signs wind-and-solar-sign-kits battery-energy-storage-signs'),
'lab':('a lab, hospital or clinic','clinic-and-medical-office-signs clinic-sign-kits extraction-lab-sign-kits hospital-sign-kits hospital-signs hospitals-and-healthcare-signs laboratory-sign-kits labs-and-research-signs test-lab-sign-kits veterinary-clinic-signs nursing-home-and-senior-care-signs behavioral-health-signs dental-office-signs'),
'school':('a school, campus or property','child-care-and-preschool-signs college-and-university-signs k-12-school-signs school-district-and-bus-signs school-sign-kits schools-and-universities-signs trade-culinary-and-specialty-school-signs apartments-and-residential-signs church-signs churches-and-nonprofits-signs'),
'oil_chem':('an oil, gas or chemical site','chemical-plant-and-distributor-signs chemical-plant-sign-kits chemical-storage-signs gas-and-propane-sign-kits natural-gas-and-propane-signs oil-and-gas-sign-kits oil-gas-mining-and-chemical-signs oilfield-and-well-pad-signs propane-lp-gas-signs refining-sign-kits offshore-sign-kits'),
'cold':('a cold storage site','ammonia-refrigeration-signs cold-storage-and-food-distribution-signs cold-storage-sign-kits'),
'carwash':('a car wash','car-wash-sign-kits car-wash-signs'),
'datacenter':('a data center or server room','data-center-and-server-room-signs data-center-sign-kits'),
'brewery':('a brewery, distillery or winery','brewery-and-winery-sign-kits brewery-winery-and-distillery-signs'),
'woodshop':('a sawmill or wood shop','lumber-yard-sign-kits sawmill-and-paper-mill-sign-kits wood-lumber-and-furniture-plant-signs'),
'fuelstop':('a gas station or truck stop','fuel-station-sign-kits gas-station-and-fuel-terminal-signs trucking-fleet-and-truck-stop-signs'),
'quarry':('a quarry or mine','coal-mine-sign-kits critical-minerals-sign-kits mineral-processing-sign-kits mining quarry-and-mine-sign-kits quarry-mine-and-gravel-pit-signs blasting-area-signs'),
'office':('an office or commercial building','commercial-property-and-building-signs corporate-office-and-coworking-signs law-insurance-and-real-estate-office-signs offices-and-commercial-property-signs city-hall-and-government-office-signs bank-and-credit-union-signs'),
'retail':('a retail store','retail-and-personal-services-signs retail-back-room-sign-kits retail-store-signs thrift-store-and-donation-center-signs pet-store-and-feed-store-signs repair-and-service-shop-signs'),
'marina':('a marina or boatyard','marina-dock-and-boat-signs boat-ramp-lake-and-beach-signs port-and-marine-sign-kits port-barge-and-shipyard-signs shipyard-sign-kits'),
}
import json
allh=[h for _,(n,s) in M.items() for h in s.split()]
print(len(allh), len(set(allh)))
json.dump(allh,open('handles.json','w'))
