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
