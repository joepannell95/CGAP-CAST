// Relays a JSONL file hosted on GitHub raw to a Shopify staged-upload target (the session's shell cannot reach it).
// Auth: x-relay-token header checked against a SHA-256 hash.
const HASH = '9bc079193123fe943028b70d232fa5d16e45fabd29ee2b3c6df39e0df9110558';
const ALLOW_SRC = /^https:\/\/raw\.githubusercontent\.com\/joepannell95\/CGAP-CAST\//;
const ALLOW_DST = /^https:\/\/shopify-staged-uploads\.storage\.googleapis\.com\//;
async function sha(s: string) { const b = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(s)); return [...new Uint8Array(b)].map((x) => x.toString(16).padStart(2, '0')).join(''); }
Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('ok');
  if ((await sha(req.headers.get('x-relay-token') || '')) !== HASH) return new Response('forbidden', { status: 403 });
  const { src, url, params } = await req.json();
  if (!ALLOW_SRC.test(src) || !ALLOW_DST.test(url)) return new Response('bad target', { status: 400 });
  const file = await (await fetch(src)).blob();
  const fd = new FormData();
  for (const p of params as { name: string; value: string }[]) fd.append(p.name, p.value);
  fd.append('file', file, 'bulk.jsonl');
  const r = await fetch(url, { method: 'POST', body: fd });
  return new Response(JSON.stringify({ status: r.status, bytes: file.size, body: (await r.text()).slice(0, 300) }), { headers: { 'Content-Type': 'application/json' } });
});
