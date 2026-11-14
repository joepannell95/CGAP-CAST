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
