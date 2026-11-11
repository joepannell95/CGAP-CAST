-- Sign Finder search v5: same results shape, much less database work per search.
-- Built for the small Supabase instance, which slows down hard once its burst credits run out.

-- 1) How many signs use each word stem. Rare words drive candidate selection, common words only help rank.
create table if not exists finder.lexdf (lexeme text primary key, ndoc int not null);
alter table finder.lexdf enable row level security;

-- Built in slices so no single statement runs long: select finder.build_lexdf(k, 6) for k in 0..5.
create or replace function finder.build_lexdf(part int, parts int) returns int
language sql volatile set search_path to 'finder', 'public' as $$
  with s as (
    select word, ndoc from ts_stat(format('select fts from finder.idx where mod(abs(hashtext(sku)), %s) = %s', parts, part))
  ), up as (
    insert into finder.lexdf as d (lexeme, ndoc) select word, ndoc from s
    on conflict (lexeme) do update set ndoc = d.ndoc + excluded.ndoc
    returning 1
  ) select count(*)::int from up;
$$;

-- 2) Search. Changes from v4:
--    - lexical candidates come from rare words and word pairs instead of every row sharing any word
--      (cuts ranked rows from ~14,000 to a few thousand on typical multi-word searches)
--    - word matches are weighted by rarity, so "auger" counts more than "room"
--    - vector channel: ef_search 150 and 150 rows (was 400), iterative scan only when filters are on
create or replace function finder.search(q text, q_emb extensions.halfvec default null, f_series text[] default null, f_sector text[] default null, f_class text[] default null, lim integer default 300)
returns table(sku text, series text, handle text, title text, subject text, phrase text, lines text, equipment text, install_point text, industries text, division text, sector text, hazard_class text, why text, img text, lex_rank real, vec_sim real, score real)
language plpgsql stable
set search_path to 'finder', 'extensions', 'public'
as $function$
declare
  lx text[]; df int[]; wt real[]; tqs tsquery[]; n int; m int; wsum real;
  tq tsquery; cq tsquery; parts text[] := '{}';
  filtered boolean := f_series is not null or f_sector is not null or f_class is not null;
begin
  begin
    select array_agg(l.w order by coalesce(d.ndoc, 0), l.w), array_agg(coalesce(d.ndoc, 0) order by coalesce(d.ndoc, 0), l.w)
      into lx, df
    from (select distinct unnest(tsvector_to_array(to_tsvector('english', q))) w) l
    left join lexdf d on d.lexeme = l.w;
    n := coalesce(array_length(lx, 1), 0);
    if n > 0 then
      select array_agg(greatest(ln(88056.0 / (1 + x)), 0.5)::real order by o) into wt from unnest(df) with ordinality u(x, o);
      select array_agg(quote_literal(x)::tsquery order by o) into tqs from unnest(lx) with ordinality u(x, o);
      select sum(x) into wsum from unnest(wt) x;
      tq := array_to_string(array(select quote_literal(x) from unnest(lx) x), ' | ')::tsquery;
      for i in 1..n loop
        if df[i] <= 4000 or n = 1 then parts := parts || quote_literal(lx[i]); end if;
      end loop;
      m := least(n, 6);
      for i in 1..m - 1 loop
        for j in i + 1..m loop
          parts := parts || ('(' || quote_literal(lx[i]) || ' & ' || quote_literal(lx[j]) || ')');
        end loop;
      end loop;
      if coalesce(array_length(parts, 1), 0) = 0 then parts := array[quote_literal(lx[1])]; end if;
      cq := array_to_string(parts, ' | ')::tsquery;
    end if;
  exception when others then tq := null; cq := null;
  end;
  perform set_config('hnsw.ef_search', '150', true);
  perform set_config('hnsw.iterative_scan', case when filtered then 'relaxed_order' else 'off' end, true);
  return query
  with cand as (
    select i.sku, i.fts, i.boost, ts_rank('{0.1,0.3,0.6,1.0}', i.fts, tq) r0
    from idx i
    where cq is not null and i.fts @@ cq
      and (f_series is null or i.series = any(f_series))
      and (f_sector is null or i.sector = any(f_sector))
      and (f_class is null or i.hazard_class = any(f_class))
    order by ts_rank('{0.1,0.3,0.6,1.0}', i.fts, tq) * (1 + i.boost) desc limit 1200
  ), lex as (
    select c.sku, (c.r0 * (1 + c.boost) * (1 + 3 * (select coalesce(sum(wt[k]), 0) from generate_subscripts(tqs, 1) k where c.fts @@ tqs[k]) / greatest(wsum, 0.001)))::real r
    from cand c order by 2 desc limit 300
  ), lexr as (select l.sku, l.r, row_number() over (order by l.r desc) rn from lex l),
  vv as (
    select v.sku, (1 - (v.embedding <=> q_emb))::real sim
    from vec v
    where q_emb is not null
      and (f_series is null or v.series = any(f_series))
      and (f_sector is null or v.sector = any(f_sector))
      and (f_class is null or v.hazard_class = any(f_class))
    order by v.embedding <=> q_emb limit 150
  ), vecr as (select v.sku, v.sim, row_number() over (order by v.sim desc) rn from vv v),
  fused as (
    select coalesce(a.sku, b.sku) fsku, a.r, b.sim, (coalesce(1.0 / (40 + a.rn), 0) + coalesce(1.0 / (40 + b.rn), 0))::real sc
    from lexr a full outer join vecr b on a.sku = b.sku
  )
  select s.sku, s.series, s.handle, s.title, s.subject, s.phrase, s.lines, s.equipment, s.install_point,
         s.industries, s.division, s.sector, s.hazard_class, s.why, s.img, f.r, f.sim,
         (f.sc * (1 + 0.6 * s.boost))::real
  from fused f join signs s on s.sku = f.fsku
  order by 18 desc limit lim;
end $function$;

-- 3) Answer cache: the same words and filters come back from one key lookup.
create table if not exists finder.search_cache (
  key text primary key,
  payload jsonb not null,
  quality jsonb,
  created_at timestamptz not null default now()
);
alter table finder.search_cache enable row level security;

-- Trim old answers nightly; refresh_sales also clears the cache so re-ranked top sellers show at once.
select cron.schedule('finder-cache-trim', '17 9 * * *', $$delete from finder.search_cache where created_at < now() - interval '2 days'$$);

-- 4) v6: return ids and facet fields only; display fields are fetched for the shown page alone.
--    Cuts sign-row reads per search from 300-450 to about 27, which matters when disk reads are throttled.
create or replace function finder.search_ids(q text, q_emb extensions.halfvec default null, f_series text[] default null, f_sector text[] default null, f_class text[] default null, lim integer default 300)
returns table(sku text, series text, sector text, hazard_class text, lex_rank real, vec_sim real, score real)
language plpgsql stable
set search_path to 'finder', 'extensions', 'public'
as $function$
declare
  lx text[]; df int[]; wt real[]; tqs tsquery[]; n int; m int; wsum real;
  tq tsquery; cq tsquery; parts text[] := '{}';
  filtered boolean := f_series is not null or f_sector is not null or f_class is not null;
begin
  begin
    select array_agg(l.w order by coalesce(d.ndoc, 0), l.w), array_agg(coalesce(d.ndoc, 0) order by coalesce(d.ndoc, 0), l.w)
      into lx, df
    from (select distinct unnest(tsvector_to_array(to_tsvector('english', q))) w) l
    left join lexdf d on d.lexeme = l.w;
    n := coalesce(array_length(lx, 1), 0);
    if n > 0 then
      select array_agg(greatest(ln(88056.0 / (1 + x)), 0.5)::real order by o) into wt from unnest(df) with ordinality u(x, o);
      select array_agg(quote_literal(x)::tsquery order by o) into tqs from unnest(lx) with ordinality u(x, o);
      select sum(x) into wsum from unnest(wt) x;
      tq := array_to_string(array(select quote_literal(x) from unnest(lx) x), ' | ')::tsquery;
      for i in 1..n loop
        if df[i] <= 4000 or n = 1 then parts := parts || quote_literal(lx[i]); end if;
      end loop;
      m := least(n, 6);
      for i in 1..m - 1 loop
        for j in i + 1..m loop
          parts := parts || ('(' || quote_literal(lx[i]) || ' & ' || quote_literal(lx[j]) || ')');
        end loop;
      end loop;
      if coalesce(array_length(parts, 1), 0) = 0 then parts := array[quote_literal(lx[1])]; end if;
      cq := array_to_string(parts, ' | ')::tsquery;
    end if;
  exception when others then tq := null; cq := null;
  end;
  perform set_config('hnsw.ef_search', '100', true);
  perform set_config('hnsw.iterative_scan', case when filtered then 'relaxed_order' else 'off' end, true);
  return query
  with cand as (
    select i.sku, i.fts, i.boost, ts_rank('{0.1,0.3,0.6,1.0}', i.fts, tq) r0
    from idx i
    where cq is not null and i.fts @@ cq
      and (f_series is null or i.series = any(f_series))
      and (f_sector is null or i.sector = any(f_sector))
      and (f_class is null or i.hazard_class = any(f_class))
    order by ts_rank('{0.1,0.3,0.6,1.0}', i.fts, tq) * (1 + i.boost) desc limit 1200
  ), lex as (
    select c.sku, (c.r0 * (1 + c.boost) * (1 + 3 * (select coalesce(sum(wt[k]), 0) from generate_subscripts(tqs, 1) k where c.fts @@ tqs[k]) / greatest(wsum, 0.001)))::real r
    from cand c order by 2 desc limit 300
  ), lexr as (select l.sku, l.r, row_number() over (order by l.r desc) rn from lex l),
  vv as (
    select v.sku, (1 - (v.embedding <=> q_emb))::real sim
    from vec v
    where q_emb is not null
      and (f_series is null or v.series = any(f_series))
      and (f_sector is null or v.sector = any(f_sector))
      and (f_class is null or v.hazard_class = any(f_class))
    order by v.embedding <=> q_emb limit 100
  ), vecr as (select v.sku, v.sim, row_number() over (order by v.sim desc) rn from vv v),
  fused as (
    select coalesce(a.sku, b.sku) fsku, a.r, b.sim, (coalesce(1.0 / (40 + a.rn), 0) + coalesce(1.0 / (40 + b.rn), 0))::real sc
    from lexr a full outer join vecr b on a.sku = b.sku
  )
  select f.fsku, i.series, i.sector, i.hazard_class, f.r, f.sim, (f.sc * (1 + 0.6 * i.boost))::real
  from fused f join idx i on i.sku = f.fsku
  order by 7 desc limit lim;
end $function$;

create or replace function finder.cards(skus text[])
returns table(sku text, series text, handle text, title text, subject text, phrase text, lines text, equipment text, install_point text, industries text, division text, sector text, hazard_class text, why text, img text)
language sql stable set search_path to 'finder', 'public' as $$
  select s.sku, s.series, s.handle, s.title, s.subject, s.phrase, s.lines, s.equipment, s.install_point, s.industries, s.division, s.sector, s.hazard_class, s.why, s.img
  from signs s where s.sku = any(skus)
$$;

select cron.schedule('finder-warm', '*/10 * * * *', $$ select pg_prewarm('finder.idx_fts'), pg_prewarm('finder.vec_hnsw'), pg_prewarm('finder.idx'), pg_prewarm('finder.idx_pkey'), pg_prewarm('finder.vec_pkey'), pg_prewarm('finder.signs_pkey'); $$);

-- 5) Suggestions: sign names that contain every typed word come first (top sellers, then shorter names),
--    then other signs that mention the words. Small name-only index kept in sync by trigger.
create table if not exists finder.subj (sku text primary key, sv tsvector not null, boost real not null default 0, len int not null default 0);
alter table finder.subj enable row level security;
insert into finder.subj (sku, sv, boost, len)
select s.sku, to_tsvector('simple', coalesce(s.subject, '')), coalesce(s.boost, 0), length(coalesce(s.subject, '')) from finder.signs s
on conflict (sku) do update set sv = excluded.sv, boost = excluded.boost, len = excluded.len;
create index if not exists subj_sv on finder.subj using gin (sv);

create or replace function finder.subj_sync() returns trigger language plpgsql set search_path to 'finder', 'public' as $$
begin
  if tg_op = 'DELETE' then delete from finder.subj where sku = old.sku; return old; end if;
  insert into finder.subj (sku, sv, boost, len) values (new.sku, to_tsvector('simple', coalesce(new.subject, '')), coalesce(new.boost, 0), length(coalesce(new.subject, '')))
  on conflict (sku) do update set sv = excluded.sv, boost = excluded.boost, len = excluded.len;
  return new;
end $$;
create or replace trigger signs_subj_sync after insert or delete or update of subject, boost on finder.signs for each row execute function finder.subj_sync();

create or replace function finder.suggest(q text, lim integer default 6)
returns table(sku text, series text, handle text, subject text, lines text, sector text, install_point text, total integer)
language plpgsql stable
set search_path to 'finder', 'public'
as $function$
declare
  w text[]; tq_and tsquery; tq_or tsquery; sq tsquery; n int; picked text[]; k int;
begin
  select array_agg(x) into w from (select regexp_replace(t, '[^a-z0-9]', '', 'g') x from unnest(regexp_split_to_array(lower(q), '\s+')) t) s where length(x) > 1;
  if w is null then return; end if;
  begin
    tq_and := to_tsquery('english', array_to_string(w[1:array_length(w,1)-1] || (w[array_length(w,1)] || ':*'), ' & '));
    tq_or := to_tsquery('english', array_to_string(w[1:array_length(w,1)-1] || (w[array_length(w,1)] || ':*'), ' | '));
    sq := to_tsquery('simple', array_to_string(array(select x || ':*' from unnest(w) x), ' & '));
  exception when others then return; end;
  select count(*) into n from (select 1 from idx where fts @@ tq_and limit 500) c;
  if n < 3 then tq_and := tq_or; select count(*) into n from (select 1 from idx where fts @@ tq_or limit 500) c; end if;
  select array_agg(x.sku order by x.boost desc, x.len) into picked
  from (select u.sku, u.boost, u.len from subj u where u.sv @@ sq order by u.boost desc, u.len limit lim) x;
  picked := coalesce(picked, '{}');
  k := coalesce(array_length(picked, 1), 0);
  if k < lim and tq_and is not null then
    select picked || coalesce(array_agg(t.sku order by t.r desc), '{}') into picked
    from (select i.sku, ts_rank('{0.1,0.3,0.6,1.0}', i.fts, tq_and) * (1 + 2 * i.boost) r
          from idx i where i.fts @@ tq_and and not (i.sku = any(picked)) order by r desc limit lim - k) t;
  end if;
  return query
    select s.sku, s.series, s.handle, s.subject, s.lines, s.sector, s.install_point, n
    from unnest(picked) with ordinality p(psku, o) join signs s on s.sku = p.psku order by p.o;
end $function$;

-- 6) Keep popular searches answered ahead of time. Every 4 minutes the keep-warm job runs the stalest
--    query from this list through the finder (flagged internal, so it never shows in the gap report).
--    Top shopper searches from the last 30 days are added automatically.
create table if not exists finder.warm_queries (q text primary key, last_warmed timestamptz);
alter table finder.warm_queries enable row level security;
insert into finder.warm_queries (q) values
 ('grain bin entry'), ('commercial kitchen fryers'), ('forklift battery charging'), ('lift station wet well'), ('arc flash at the panel'),
 ('grain bin roof manhole on our farm'), ('lockout on a meat grinder'), ('battery charging room for forklifts'), ('confined space at a lift station'), ('hot oil fryers in a restaurant kitchen'),
 ('commercial kitchen fryer station'), ('forklift traffic at loading dock'), ('arc flash at electrical panel'), ('dairy milking parlor'), ('car wash bay'),
 ('restaurant kitchen'), ('farm'), ('warehouse'), ('hospital'), ('school'), ('brewery'), ('winery'), ('data center'), ('sawmill'), ('cold storage'),
 ('ammonia refrigeration'), ('water treatment plant'), ('construction site'), ('mining'), ('chemical plant'), ('propane'), ('auto shop'), ('machine shop'),
 ('welding'), ('forklift'), ('loading dock'), ('lockout tagout'), ('confined space'), ('arc flash'), ('eyewash'), ('grain bin'), ('pool chemical room')
on conflict (q) do nothing;

create or replace function finder.keepwarm() returns void
language plpgsql security definer set search_path to 'finder', 'public', 'extensions'
as $$
declare nq text;
begin
  insert into finder.warm_queries (q)
  select lower(trim(l.q)) from finder.search_log l
  where not coalesce(l.internal, false) and l.at > now() - interval '30 days' and length(trim(l.q)) between 3 and 80
  group by lower(trim(l.q)) order by count(*) desc limit 20
  on conflict (q) do nothing;
  update finder.warm_queries w set last_warmed = now()
  where w.q = (select x.q from finder.warm_queries x order by x.last_warmed nulls first, x.q limit 1)
  returning w.q into nq;
  perform net.http_post(
    url := 'https://esmwoaqemeukjrjaesby.supabase.co/functions/v1/sign-finder',
    body := jsonb_build_object('q', coalesce(nq, '__warm__'), 'internal', true),
    timeout_milliseconds := 20000);
end $$;

select cron.schedule('finder-keepwarm', '*/4 * * * *', $$ select finder.keepwarm(); $$);
select cron.schedule('finder-cache-trim', '17 9 * * *', $$delete from finder.search_cache where created_at < now() - interval '7 days'$$);
