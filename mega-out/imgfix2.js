// IMGFIX2: put the missing sign pictures back on 2,103 live products (1,765 mega signs that show only the spec
// picture, 327 kits and 11 V216 signs with no picture). Run in a Shopify admin products tab AFTER evaluating the
// R33 driver (needs __deep, __r33Btn, __spreview, __r33Go).
//   await window.__fxBuild(2)            -> builds a 2-product test CSV in memory (live titles from the Storefront API)
//   await window.__fxOpen('IMGFIX2_TEST.csv')  -> opens Import with Overwrite ON, returns the preview text
//   await window.__r33Go()               -> clicks Import products
//   await window.__fxBuild()             -> full CSV (skips products that already show their sign first)
window.__fxSrc = 'https://raw.githubusercontent.com/joepannell95/CGAP-CAST/1f5872c/mega-out/imgfix2_full.json';
window.__fxBuild = async (limit, offset) => {
  const d = await (await fetch(window.__fxSrc)).json();
  const list = d.slice(offset || 0, limit ? (offset || 0) + limit : undefined);
  const titles = {}, now = {};
  for (let i = 0; i < list.length; i += 40) {
    const chunk = list.slice(i, i + 40);
    const q = '{' + chunk.map((p, j) => `p${j}: product(handle: ${JSON.stringify(p.h)}) { title images(first: 3) { nodes { url } } }`).join(' ') + '}';
    let j = null;
    for (let t = 0; t < 5; t++) {
      try { const r = await fetch('https://cgapindustries.com/api/2026-10/graphql.json', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ query: q }) }); j = await r.json(); if (j && j.data) break; } catch (e) { }
      await new Promise(r => setTimeout(r, 2000));
    }
    chunk.forEach((p, k) => { const n = j && j.data && j.data['p' + k]; if (n) { titles[p.h] = n.title; now[p.h] = n.images.nodes.map(x => x.url.split('/').pop().split('?')[0]); } });
  }
  const esc = s => /[",\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  const rows = ['Handle,Title,Image Src,Image Position,Image Alt Text'];
  const skipped = []; let n = 0;
  for (const p of list) {
    const t = titles[p.h];
    if (!t) { skipped.push([p.h, 'not live']); continue; }
    const stem = p.imgs[0][0].split('/').pop().replace(/\.(png|jpg)$/i, '');
    if ((now[p.h] || []).length && now[p.h][0].startsWith(stem)) { skipped.push([p.h, 'already ok']); continue; }
    p.imgs.forEach((im, idx) => rows.push([esc(p.h), idx === 0 ? esc(t) : '', esc(im[0]), String(im[1]), esc(im[2])].join(',')));
    n++;
  }
  window.__fx = { state: 'built', n, skipped, csv: rows.join('\n') + '\n', at: new Date().toISOString(), handles: list.filter(p => titles[p.h]).map(p => p.h) };
  return [n, skipped.length, skipped.slice(0, 5)];
};
window.__fxOpen = async (name) => {
  const S = ms => new Promise(r => setTimeout(r, ms));
  let inp = window.__deep().find(e => e.tagName === 'INPUT' && e.type === 'file');
  if (!inp) { window.__r33Btn('Import')?.click(); for (let k = 0; k < 20 && !inp; k++) { await S(800); inp = window.__deep().find(e => e.tagName === 'INPUT' && e.type === 'file'); } }
  if (!inp) throw 'no file input';
  const dt = new DataTransfer(); dt.items.add(new File([window.__fx.csv], name, { type: 'text/csv' }));
  inp.files = dt.files; inp.dispatchEvent(new Event('change', { bubbles: true })); inp.dispatchEvent(new Event('input', { bubbles: true }));
  await S(3000);
  const cb = window.__deep().filter(e => e.tagName === 'INPUT' && e.type === 'checkbox');
  const ov = cb.find(c => /Overwrite/i.test(c.closest('label')?.innerText || ''));
  if (!ov) throw 'no overwrite checkbox';
  if (!ov.checked) ov.click();
  await S(500);
  window.__fx.overwrite = ov.checked;
  window.__r33Btn('Upload file')?.click();
  for (let k = 0; k < 12; k++) { await S(3000); const t = window.__spreview(); if (/approximately\s+[\d,]+/i.test(t)) return t; }
  return window.__spreview();
};
'imgfix2 loaded';
