// amazon-sync: CGAP's private Selling Partner API bridge (Listings + Feeds).
// Secrets (set by Joseph in Supabase): AMZ_LWA_CLIENT_ID, AMZ_LWA_CLIENT_SECRET, AMZ_REFRESH_TOKEN.
// Callers must send x-sync-token; only its SHA-256 is kept here. The database holds the token in Vault and calls through pg_net.
import postgres from 'npm:postgres@3.4.4';
const sql = postgres(Deno.env.get('SUPABASE_DB_URL')!, { max: 2, prepare: false });
const env = (k: string) => Deno.env.get(k) || '';
const LWA = 'https://api.amazon.com/auth/o2/token';
const API = 'https://sellingpartnerapi-na.amazon.com';
const MP = 'ATVPDKIKX0DER';
const TOKEN_SHA256 = '52cded100bd4699e15d5a5b550a27fbb78c44cb582a8e751f4d3476f67d857fd';
async function sha256(t: string) { const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(t)); return Array.from(new Uint8Array(d), (x) => x.toString(16).padStart(2, '0')).join(''); }
const J = (o: unknown, s = 200) => new Response(JSON.stringify(o), { status: s, headers: { 'Content-Type': 'application/json' } });

let tok: { v: string; exp: number } | null = null;
async function accessToken() {
  if (tok && tok.exp > Date.now() + 60_000) return tok.v;
  const r = await fetch(LWA, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ grant_type: 'refresh_token', refresh_token: env('AMZ_REFRESH_TOKEN'), client_id: env('AMZ_LWA_CLIENT_ID'), client_secret: env('AMZ_LWA_CLIENT_SECRET') }),
  });
  const j = await r.json().catch(() => ({}));
  if (!r.ok || !j.access_token) throw new Error(`LWA ${r.status} ${j.error || ''} ${j.error_description || ''}`.trim());
  tok = { v: j.access_token, exp: Date.now() + (Number(j.expires_in) || 3600) * 1000 };
  return tok.v;
}
async function sp(method: string, path: string, body?: unknown) {
  for (let attempt = 0; attempt < 4; attempt++) {
    const r = await fetch(API + path, {
      method,
      headers: { 'x-amz-access-token': await accessToken(), 'Content-Type': 'application/json', Accept: 'application/json' },
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    if (r.status === 429 && attempt < 3) { await new Promise((res) => setTimeout(res, 1500 * (attempt + 1))); continue; }
    const text = await r.text();
    let json: any = text; try { json = JSON.parse(text); } catch (_) { /* not json */ }
    return { status: r.status, body: json };
  }
  return { status: 429, body: 'throttled' };
}
async function cfg(key: string) { const r = await sql`select value from finder.amz_config where key = ${key}`; return r[0]?.value || ''; }
const item = (sid: string, sku: string) => `/listings/2021-08-01/items/${encodeURIComponent(sid)}/${encodeURIComponent(sku)}?marketplaceIds=${MP}`;

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('ok');
  if ((await sha256(req.headers.get('x-sync-token') || '')) !== TOKEN_SHA256) return J({ ok: false, error: 'forbidden' }, 403);
  const b: any = await req.json().catch(() => ({}));
  try {
    switch (b.action) {
      case 'ping':
        return J({ ok: true, configured: { client_id: !!env('AMZ_LWA_CLIENT_ID'), client_secret: !!env('AMZ_LWA_CLIENT_SECRET'), refresh_token: !!env('AMZ_REFRESH_TOKEN') } });
      case 'auth_test': {
        await accessToken();
        const p = await sp('GET', '/sellers/v1/marketplaceParticipations');
        return J({ ok: p.status === 200, status: p.status, participations: p.body?.payload?.map((x: any) => ({ marketplace: x.marketplace?.id, name: x.marketplace?.name, store: x.storeName, participating: x.participation?.isParticipating })) ?? p.body });
      }
      case 'definition': {
        // Product type schema, saved to finder.amz_config as schema_<TYPE> for the converter.
        const pt = String(b.productType || 'SIGNAGE');
        const d = await sp('GET', `/definitions/2020-09-01/productTypes/${pt}?marketplaceIds=${MP}&requirements=LISTING&locale=en_US`);
        if (d.status !== 200) return J({ ok: false, d });
        const schema = await (await fetch(d.body.schema.link.resource)).text();
        await sql`insert into finder.amz_config (key, value) values (${'schema_' + pt}, ${schema}) on conflict (key) do update set value = excluded.value`;
        return J({ ok: true, productType: pt, version: d.body.productTypeVersion?.version, bytes: schema.length, requirements: d.body.requirements });
      }
      case 'get': {
        const r = await sp('GET', item(await cfg('seller_id'), b.sku) + `&includedData=${b.included || 'summaries,issues,offers,fulfillmentAvailability'}`);
        return J(r);
      }
      case 'put': {
        const mode = b.preview ? '&mode=VALIDATION_PREVIEW' : '';
        return J(await sp('PUT', item(await cfg('seller_id'), b.sku) + `&includedData=issues${mode}`, { productType: b.productType, requirements: b.requirements || 'LISTING', attributes: b.attributes }));
      }
      case 'patch':
        return J(await sp('PATCH', item(await cfg('seller_id'), b.sku) + '&includedData=issues', { productType: b.productType, patches: b.patches }));
      case 'delete':
        return J(await sp('DELETE', item(await cfg('seller_id'), b.sku)));
      case 'submit_feed': {
        // One JSON_LISTINGS_FEED from every queued row of a batch in finder.amz_outbox.
        const rows = await sql`select id, sku, op, product_type, payload from finder.amz_outbox where status = 'queued' and batch = ${String(b.batch)} order by id limit 9000`;
        if (!rows.length) return J({ ok: true, n: 0 });
        const sid = await cfg('seller_id');
        const feed = {
          header: { sellerId: sid, version: '2.0', issueLocale: 'en_US' },
          messages: rows.map((r: any, i: number) => (r.op === 'DELETE'
            ? { messageId: i + 1, sku: r.sku, operationType: 'DELETE' }
            : r.op === 'PATCH'
              ? { messageId: i + 1, sku: r.sku, operationType: 'PATCH', productType: r.product_type, patches: r.payload }
              : { messageId: i + 1, sku: r.sku, operationType: 'UPDATE', productType: r.product_type, requirements: 'LISTING', attributes: r.payload })),
        };
        const doc = await sp('POST', '/feeds/2021-06-30/documents', { contentType: 'application/json; charset=UTF-8' });
        if (doc.status >= 300) return J({ ok: false, step: 'document', doc });
        const up = await fetch(doc.body.url, { method: 'PUT', headers: { 'Content-Type': 'application/json; charset=UTF-8' }, body: JSON.stringify(feed) });
        if (!up.ok) return J({ ok: false, step: 'upload', status: up.status, text: (await up.text()).slice(0, 300) });
        const f = await sp('POST', '/feeds/2021-06-30/feeds', { feedType: 'JSON_LISTINGS_FEED', marketplaceIds: [MP], inputFeedDocumentId: doc.body.feedDocumentId });
        if (f.status >= 300) return J({ ok: false, step: 'feed', f });
        const ids = rows.map((r: any) => Number(r.id));
        await sql`update finder.amz_outbox o set status = 'submitted', feed_id = ${String(f.body.feedId)}, message_id = m.mid, submitted_at = now()
                  from (select unnest(${ids}::bigint[]) id, generate_series(1, ${ids.length}) mid) m where o.id = m.id`;
        return J({ ok: true, n: rows.length, feedId: f.body.feedId });
      }
      case 'feed_status': {
        const f = await sp('GET', `/feeds/2021-06-30/feeds/${encodeURIComponent(b.feedId)}`);
        if (f.body?.processingStatus !== 'DONE' || !f.body.resultFeedDocumentId) return J({ ok: true, feed: f.body });
        const d = await sp('GET', `/feeds/2021-06-30/documents/${encodeURIComponent(f.body.resultFeedDocumentId)}`);
        const res = await fetch(d.body.url);
        let buf = new Uint8Array(await res.arrayBuffer());
        if (d.body.compressionAlgorithm === 'GZIP') buf = new Uint8Array(await new Response(new Blob([buf]).stream().pipeThrough(new DecompressionStream('gzip'))).arrayBuffer());
        const report = JSON.parse(new TextDecoder().decode(buf));
        const issues: any[] = report.issues || [];
        const byMsg: Record<number, any[]> = {};
        for (const is of issues) (byMsg[is.messageId] ||= []).push({ code: is.code, severity: is.severity, message: is.message, attributes: is.attributeNames });
        const rows = await sql`select id, message_id from finder.amz_outbox where feed_id = ${String(b.feedId)}`;
        for (const r of rows as any[]) {
          const iss = byMsg[r.message_id] || [];
          const err = iss.some((x) => x.severity === 'ERROR');
          await sql`update finder.amz_outbox set status = ${err ? 'error' : 'accepted'}, result = ${sql.json(iss)}, done_at = now() where id = ${r.id}`;
        }
        return J({ ok: true, feed: f.body, summary: report.summary, errors: issues.filter((x) => x.severity === 'ERROR').length, warnings: issues.filter((x) => x.severity === 'WARNING').length });
      }
      default:
        return J({ ok: false, error: 'unknown action' }, 400);
    }
  } catch (e) {
    return J({ ok: false, error: String(e) }, 500);
  }
});
