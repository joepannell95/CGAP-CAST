import postgres from 'npm:postgres@3.4.4';
const sql = postgres(Deno.env.get('SUPABASE_DB_URL')!, { max: 3, prepare: false });
let _model: any = null;
const model = () => (_model ??= new Supabase.ai.Session('gte-small'));

const ALLOWED = [/^https:\/\/(www\.)?cgapindustries\.com$/, /^https:\/\/[a-z0-9-]+\.myshopify\.com$/, /^https:\/\/[a-z0-9-]+\.shopifypreview\.com$/, /^https:\/\/.*\.shopify\.com$/];
function cors(origin: string | null) {
  const ok = origin && ALLOWED.some((r) => r.test(origin));
  return { 'Access-Control-Allow-Origin': ok ? origin! : 'https://cgapindustries.com', 'Access-Control-Allow-Methods': 'GET, POST, OPTIONS', 'Access-Control-Allow-Headers': 'content-type', 'Vary': 'Origin' };
}

const SYN: Record<string, string> = {
  restaurant: 'kitchen food service', diner: 'kitchen', cafeteria: 'kitchen food service', bakery: 'oven mixer dough',
  loto: 'lockout tagout', 'lock out': 'lockout', forklift: 'forklift lift truck powered industrial truck', 'lift truck': 'forklift',
  warehouse: 'warehouse dock racking', 'loading dock': 'dock leveler trailer', garage: 'vehicle lift service bay',
  farm: 'farm barn livestock grain', barn: 'livestock barn', silo: 'grain bin silo', hospital: 'hospital patient clinical',
  clinic: 'clinic exam', lab: 'laboratory', school: 'school classroom campus',
  electrical: 'electrical panel arc flash voltage', 'arc flash': 'arc flash electrical panel', chemical: 'chemical corrosive storage',
  ppe: 'ppe protective equipment', 'hard hat': 'head protection hard hat', 'eye wash': 'eyewash', eyewash: 'eyewash emergency shower',
  'confined space': 'confined space permit entry', fiber: 'fiber optic splice',
  telecom: 'telecom outside plant tower', pole: 'utility pole', solar: 'solar photovoltaic inverter', battery: 'battery charging',
  'car wash': 'car wash bay', 'gas station': 'fuel dispenser', brewery: 'brewery brewhouse fermenter', winery: 'winery fermentation',
  'data center': 'data center server', airport: 'airport ramp aircraft', marina: 'marina dock boat', pool: 'pool chemical',
  sawmill: 'sawmill log saw', 'machine shop': 'lathe mill grinder machine', welding: 'welding weld hot work', crane: 'crane hoist rigging',
  dairy: 'dairy milking parlor milk', church: 'church sanctuary', hotel: 'hotel housekeeping laundry', gym: 'fitness center',
};
function expand(q: string) {
  const lq = q.toLowerCase(); const add: string[] = [];
  for (const [k, v] of Object.entries(SYN)) if (new RegExp('\\b' + k + 's?\\b').test(lq)) add.push(v);
  return add.length ? q + ' ' + add.join(' ') : q;
}
const SERIES: [RegExp, string][] = [[/\bdanger\b/i, 'DANGER'], [/\bwarning\b/i, 'WARNING'], [/\bcaution\b/i, 'CAUTION'], [/\bnotice\b/i, 'NOTICE'], [/\bsafety first\b|\binstruction/i, 'SAFETY FIRST']];
const GENERIC = new Set(['station', 'stations', 'facilities', 'facility', 'systems', 'commercial', 'services', 'plants', 'manufacturing', 'processing', 'maintenance', 'specialty', 'industrial', 'shops', 'centers', 'sites', 'rooms', 'storage', 'handling', 'equipment', 'production', 'research', 'primary', 'repair', 'trades', 'yards', 'branches', 'public', 'direct', 'refining', 'filling', 'mills', 'products', 'goods', 'mechanical', 'parks']);
let SECTORS: { sector: string; words: string[] }[] = [];
async function sectors() {
  if (!SECTORS.length) {
    const rows = await sql`select distinct sector from finder.tree where sector is not null and sector <> ''` as any;
    SECTORS = rows.map((r: any) => ({ sector: r.sector, words: (r.sector.toLowerCase().match(/[a-z]+/g) || []).filter((w: string) => w.length > 3 && !GENERIC.has(w)) }));
  }
  return SECTORS;
}
const STOP = new Set(['and', 'the', 'for', 'with', 'our', 'sign', 'signs', 'safety', 'area', 'room', 'of', 'in', 'a', 'to', 'on', 'at', 'we', 'have', 'need', 'my', 'shop', 'near']);
function tokens(q: string) { return q.toLowerCase().match(/[a-z0-9]+/g)?.filter((t) => t.length > 2 && !STOP.has(t)) ?? []; }
const stem = (t: string) => t.replace(/(ing|ers|es|s|ed)$/, '');
function stemHit(text: string, t: string) { const s = stem(t); return s.length > 2 && text.toLowerCase().includes(s); }

// Share of the shopper's words that a result actually covers (a word counts if it, or one of its synonyms, appears).
function coverage(r: any, toks: string[]) {
  if (!r) return 0;
  if (!toks.length) return 1;
  const text = [r.subject, r.title, r.phrase, r.lines, r.equipment, r.install_point, r.industries, r.sector, r.hazard_class, r.why].filter(Boolean).join(' ').toLowerCase();
  let hit = 0;
  for (const t of toks) {
    const alts = [t, ...String(SYN[t] || SYN[t.replace(/s$/, '')] || '').split(' ').filter(Boolean)];
    if (alts.some((a) => stemHit(text, a))) hit++;
  }
  return hit / toks.length;
}

function shape(r: any, toks: string[]) {
  const fields: [string, string][] = [['equipment', r.equipment], ['install point', r.install_point], ['subject', r.subject], ['industry', (r.industries || '') + ' ' + (r.sector || '')], ['hazard', (r.hazard_class || '') + ' ' + (r.why || '')]];
  const matched: string[] = []; const on: string[] = [];
  for (const t of toks) for (const [name, txt] of fields) if (txt && stemHit(txt, t)) { if (!matched.includes(t)) matched.push(t); if (!on.includes(name)) on.push(name); break; }
  return { sku: r.sku, series: r.series, handle: r.handle, title: r.title, subject: r.subject, phrase: r.phrase, lines: r.lines ? r.lines.split(' / ') : [], equipment: r.equipment, install_point: r.install_point, sector: r.sector, division: r.division, hazard_class: r.hazard_class, why: r.why, img: r.img, matched, matched_on: on, score: r.score ?? null };
}
function diversify(rows: any[]) {
  const placed: Record<string, number> = {}; const out: any[] = []; const pool = rows.map((r, i) => ({ r, s: r.score ?? 1 / (i + 1) }));
  while (pool.length) {
    let bi = 0, bv = -1;
    for (let i = 0; i < Math.min(pool.length, 40); i++) { const v = pool[i].s * Math.pow(0.82, placed[pool[i].r.series] || 0); if (v > bv) { bv = v; bi = i; } }
    const [x] = pool.splice(bi, 1); out.push(x.r); placed[x.r.series] = (placed[x.r.series] || 0) + 1;
    if (out.length % 12 === 0) for (const k in placed) placed[k] = Math.floor(placed[k] / 2);
  }
  return out;
}
function facets(rows: any[]) {
  const f: Record<string, Record<string, number>> = { series: {}, sector: {}, hazard_class: {} };
  for (const r of rows) for (const k of Object.keys(f)) if (r[k]) f[k][r[k]] = (f[k][r[k]] || 0) + 1;
  const top = (o: Record<string, number>, n: number) => Object.entries(o).sort((a, b) => b[1] - a[1]).slice(0, n).map(([value, count]) => ({ value, count }));
  return { series: top(f.series, 5), sector: top(f.sector, 12), hazard_class: top(f.hazard_class, 12) };
}
const arr = (v: any) => (Array.isArray(v) && v.length ? v.map(String) : null);
// One row per first-page search, cached or not, for the weekly search-gap report.
function logSearch(q: string, filters: any, qy: any) {
  sql`insert into finder.search_log (q, filters, results, lex_hits, top_cov, top_sim) values (${q}, ${sql.json(filters)}, ${qy.results ?? null}, ${qy.lex_hits ?? null}, ${qy.top_cov ?? null}, ${qy.top_sim ?? null})`.catch(() => {});
}

Deno.serve(async (req) => {
  const h = cors(req.headers.get('origin'));
  if (req.method === 'OPTIONS') return new Response(null, { headers: h });
  const url = new URL(req.url);
  let p: any = {};
  if (req.method === 'POST') p = await req.json().catch(() => ({}));
  else for (const [k, v] of url.searchParams) p[k] = v.includes('|') ? v.split('|') : v;
  const json = (o: any, cache = 120) => new Response(JSON.stringify(o), { headers: { ...h, 'Content-Type': 'application/json', 'Cache-Control': `public, max-age=${cache}` } });
  try {
    const action = p.action || 'search';
    if (action === 'click') {
      // Beacon from the finder, hero and header: a shopper opened, picked or carted a result.
      const cq = String(p.q ?? '').slice(0, 300).trim();
      const sku = String(p.sku ?? '').slice(0, 80).trim();
      const kind = String(p.kind ?? 'open').replace(/[^a-z_]/g, '').slice(0, 20) || 'open';
      if (sku && cq) await sql`select finder.log_click(${cq}, ${sku}, ${kind})`.catch(() => {});
      return new Response(null, { status: 204, headers: h });
    }
    if (action === 'suggest') {
      const q = String(p.q ?? '').slice(0, 120).trim();
      if (q.length < 2) return json({ q, results: [] }, 3600);
      const rows = await sql`select * from finder.suggest(${q}, 6)`;
      return json({ q, total: rows[0]?.total ?? 0, results: rows.map((r) => ({ sku: r.sku, series: r.series, handle: r.handle, subject: r.subject, lines: r.lines ? r.lines.split(' / ') : [], sector: r.sector, install_point: r.install_point })) }, 3600);
    }
    if (action === 'tree') {
      const t = await sql`select division, sector, sum(n)::int n, json_object_agg(series, n) by_series from finder.tree group by 1,2 order by 1, 3 desc`;
      const total = (await sql`select count(*)::int n from finder.signs`)[0].n;
      return json({ total, tree: t }, 3600);
    }
    if (action === 'browse') {
      const page = Math.max(0, Number(p.page) || 0);
      const rows = await sql`select * from finder.browse(${arr([].concat(p.sector ?? []))}, ${arr([].concat(p.series ?? []))}, ${arr([].concat(p.hazard_class ?? []))}, ${page * 48}, 48)`;
      return json({ total: Number(rows[0]?.total ?? 0), page, results: rows.map((r) => shape(r, [])) }, 600);
    }
    if (action === 'similar') {
      const rows = await sql`select * from finder.similar(${String(p.sku)}, 12)`;
      return json({ results: rows.map((r) => shape(r, [])) }, 3600);
    }
    const q = String(p.q ?? '').slice(0, 300).trim();
    if (!q) return json({ q, results: [], facets: facets([]), detected: {} });
    const t0 = Date.now();
    if (q === '__warm__') { try { await model().run('warm', { mean_pool: true, normalize: true }); } catch (_) { /* model still loading */ } return json({ ok: true }, 0); }
    const fSeries = arr([].concat(p.series ?? [])); const fSector = arr([].concat(p.sector ?? [])); const fClass = arr([].concat(p.hazard_class ?? []));
    const page = Math.max(0, Math.min(20, Number(p.page) || 0));
    const filters = { series: fSeries, sector: fSector, hazard_class: fClass };
    // Keep-warm runs from the database: answer and cache, but never count as a shopper search.
    const internal = p.internal === true || p.internal === 'true' || p.internal === '1';
    // Same words and filters answered recently: one key lookup instead of a full search.
    const ckey = JSON.stringify([q.toLowerCase().replace(/\s+/g, ' '), fSeries && [...fSeries].sort(), fSector && [...fSector].sort(), fClass && [...fClass].sort(), page]);
    const hit: any[] = await sql`select payload, quality from finder.search_cache where key = ${ckey} and created_at > now() - interval '7 days'`.catch(() => []);
    if (hit.length) {
      if (internal) { try { await model().run('warm', { mean_pool: true, normalize: true }); } catch (_) { /* model still loading */ } }
      else if (page === 0) logSearch(q, filters, hit[0].quality || {});
      return json({ ...hit[0].payload, ms: Date.now() - t0, cached: true }, 300);
    }
    let emb: string | null = null;
    try { const e = await model().run(q, { mean_pool: true, normalize: true }) as number[]; emb = '[' + e.join(',') + ']'; } catch (_) { emb = null; }
    // Ranked ids plus facet fields for up to 300 matches; full card details only for the page being shown.
    const rows: any[] = await sql`select * from finder.search_ids(${expand(q)}, ${emb}::extensions.halfvec, ${fSeries}, ${fSector}, ${fClass}, 300)`;
    const toks = tokens(q);
    const lq = ' ' + q.toLowerCase().replace(/[^a-z0-9 ]/g, ' ') + ' ';
    const secs = await sectors();
    const hits = secs.map((s) => ({ s: s.sector, n: s.words.filter((w) => lq.includes(' ' + stem(w))).length })).filter((x) => x.n > 0).sort((a, b) => b.n - a.n);
    const fromResults = Object.entries(rows.slice(0, 60).reduce((a: any, r: any) => { a[r.sector] = (a[r.sector] || 0) + 1; return a; }, {})).sort((a: any, b: any) => b[1] - a[1]).filter(([, n]: any) => n >= 8).map(([s]) => s);
    const detSectors = [...new Set([...hits.map((x) => x.s), ...fromResults])].slice(0, 4);
    const ordered = diversify(rows);
    const pageRows = ordered.slice(page * 24, page * 24 + 24);
    const need = [...new Set([...pageRows, ...rows.slice(0, 3)].map((r: any) => r.sku))];
    const cards: any[] = need.length ? await sql`select * from finder.cards(${need})` : [];
    const bySku = new Map(cards.map((c: any) => [c.sku, c]));
    const full = (r: any) => ({ ...bySku.get(r.sku), score: r.score, lex_rank: r.lex_rank, vec_sim: r.vec_sim });
    let quality: any = null;
    if (page === 0) {
      // Quality signals for the weekly search-gap report.
      const sims = rows.map((r: any) => Number(r.vec_sim)).filter((x: number) => Number.isFinite(x) && x > 0);
      quality = {
        results: rows.length,
        lex_hits: rows.filter((r: any) => r.lex_rank != null).length,
        top_cov: rows.length ? Math.max(...rows.slice(0, 3).map((r: any) => coverage(full(r), toks))) : 0,
        top_sim: sims.length ? Math.max(...sims) : null,
      };
      if (!internal) logSearch(q, filters, quality);
    }
    const payload = { q, total: rows.length, page, semantic: !!emb, detected: { series: SERIES.filter(([r]) => r.test(q)).map(([, s]) => s), sectors: detSectors }, facets: facets(rows), results: pageRows.filter((r: any) => bySku.has(r.sku)).map((r: any) => shape(full(r), toks)) };
    // Only full-quality answers (with the meaning-based channel) are kept.
    if (emb) sql`insert into finder.search_cache (key, payload, quality) values (${ckey}, ${sql.json(payload)}, ${quality ? sql.json(quality) : null}) on conflict (key) do update set payload = excluded.payload, quality = excluded.quality, created_at = now()`.catch(() => {});
    return json({ ...payload, ms: Date.now() - t0 }, 300);
  } catch (e) {
    return new Response(JSON.stringify({ error: String(e) }), { status: 500, headers: { ...h, 'Content-Type': 'application/json' } });
  }
});
