/* CGAP Safety bulk order: paste or upload a list, match each line to a sign, add everything to the cart at once. */
(function () {
  var root = document.getElementById('cg-bulk'); if (!root) return;
  var API = 'https://esmwoaqemeukjrjaesby.supabase.co/functions/v1/sign-finder';
  var CUSTOM = { id: 68144025108724, price: 29.99, handle: 'custom-safety-sign-8x12-aluminum' };
  var HEADERS = ['DANGER', 'WARNING', 'CAUTION', 'NOTICE', 'SAFETY FIRST'];
  var KEY = 'cg_bulk_v1';
  var rows = [], uid = 0;
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function money(n) { return '$' + n.toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function short(t) { return String(t || '').split(/ [–-] 8x12| – |, (?:for |8x12|English)/)[0].replace(/\s+Sign$/i, '').trim(); }

  root.innerHTML =
    '<div class="box"><b>How it works:</b> paste your list below, one sign per line, with a quantity if you need more than one. ' +
    'Copy straight from Excel or Google Sheets, or upload a CSV. We match each line to a sign, you check the matches, then add everything to your cart in one click.</div>' +
    '<textarea id="cgb-in" rows="9" style="width:100%;font-size:1.5rem;padding:1rem;border:1px solid #bbb;border-radius:6px" placeholder="10 x Hard hat area\nForklift traffic, 4\nEyewash station\t2\nCGAP-GEN014-812\nDANGER Keep out confined space"></textarea>' +
    '<p style="display:flex;gap:1rem;flex-wrap:wrap;align-items:center;margin:1rem 0"><button type="button" class="btn" id="cgb-go">Match my list</button>' +
    '<label class="btn2" style="cursor:pointer">Upload CSV<input type="file" id="cgb-file" accept=".csv,.txt,.tsv" style="display:none"></label>' +
    '<a href="#" id="cgb-clear" class="note">Clear</a></p>' +
    '<div id="cgb-rows"></div><div id="cgb-bar"></div>';
  var $in = root.querySelector('#cgb-in'), $rows = root.querySelector('#cgb-rows'), $bar = root.querySelector('#cgb-bar');

  var UNITS = /^(mph|km|ft|feet|foot|lbs?|pounds?|tons?|volts?|v|kv|amps?|degrees?|%|psi|gallons?|gal|inch|in|minutes?|min|hours?|hrs?|days?|am|pm|years?|people)\b/i;
  function clean(t) { return t.replace(/^[\s\-*•·>]+/, '').replace(/["']/g, '').replace(/\s+/g, ' ').trim(); }
  function parseLine(raw) {
    var line = raw.replace(/ /g, ' ').trim(), m, qty = 1, text;
    if (!line || /^(qty|quantity|item|description|sign|signs|sku|#)([\s,\t]+(qty|quantity|description|item|sign|signs|sku))*\s*$/i.test(line)) return null;
    var cells = line.split(/\t|,(?=(?:[^"]*"[^"]*")*[^"]*$)/).map(function (c) { return c.trim(); }).filter(Boolean);
    if (cells.length > 1) {
      var n = cells.findIndex(function (c) { return /^\d{1,4}(\.0+)?$/.test(c); });
      if (n >= 0) { qty = parseInt(cells[n], 10); cells.splice(n, 1); text = clean(cells.join(' ')); return text.length > 1 ? { text: text, qty: Math.max(1, Math.min(9999, qty || 1)) } : null; }
      line = cells.join(', ');
    }
    line = line.replace(/^\d{1,3}[.)]\s+/, ''); text = line;
    if ((m = line.match(/^(\d{1,4})\s*(x|×|ea\.?|each|pcs?\.?|-|:)?\s+(.+)$/i)) && (m[2] || !UNITS.test(m[3]))) { qty = +m[1]; text = m[3]; }
    else if ((m = line.match(/^(.+?)(?:\s*[,;:(\-–]\s*|\s+[x×]\s*)(?:qty\.?\s*)?(\d{1,4})\s*(?:ea\.?|each|pcs?\.?|signs?)?\)?\s*$/i))) { qty = +m[2]; text = m[1]; }
    text = clean(text.replace(/[\s,;:(\-–]+$/, ''));
    return text && text.length > 1 ? { text: text, qty: Math.max(1, Math.min(9999, qty || 1)) } : null;
  }
  var STOP = { sign: 1, signs: 1, the: 1, a: 1, an: 1, of: 1, 'in': 1, at: 1, to: 1, and: 1, 'for': 1, on: 1, is: 1, area: 1 };
  function words(t) { return String(t || '').toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(function (w) { return w && !STOP[w]; }).map(function (w) { return w.replace(/ies$/, 'y').replace(/([^s])s$/, '$1'); }); }
  var SER = ['danger', 'warning', 'caution', 'notice', 'safety', 'first'];
  function score(q, r, i) {
    var qw = words(q).filter(function (w) { return SER.indexOf(w) < 0; }), qj = qw.join(''), sw = words(r.subject);
    if (!qw.length || !sw.length) return { rec: 0, prec: 0, s: 0 };
    var rec = qw.filter(function (w) { return sw.some(function (x) { return x === w || (w.length > 2 && x.indexOf(w) >= 0); }); }).length / qw.length;
    var prec = sw.filter(function (x) { return qw.indexOf(x) >= 0 || qj.indexOf(x) >= 0; }).length / sw.length;
    var ser = (r.series || '').toUpperCase();
    return { rec: rec, prec: prec, s: 2 * rec + prec + (0.3 - i * 0.03) + (ser && q.toUpperCase().indexOf(ser) >= 0 ? 0.4 : 0) };
  }
  var pc = {};
  function product(h) { if (!pc[h]) pc[h] = fetch('/products/' + h + '.js').then(function (r) { return r.ok ? r.json() : null; }).catch(function () { return null; }); return pc[h]; }
  function guessHeader(t) { var u = t.toUpperCase(); return HEADERS.find(function (h) { return u.indexOf(h) === 0 || u.indexOf(h + ' ') >= 0; }) || (/(fire|exit|extinguisher|eyewash|eye wash|first aid|shower)/i.test(t) ? 'SAFETY FIRST' : /(keep out|high voltage|confined|chlorine|arc flash|explosive|toxic|crush)/i.test(t) ? 'DANGER' : 'NOTICE'); }
  function stripHeader(t) { return t.replace(new RegExp('^(' + HEADERS.join('|') + ')[\\s:,-]*', 'i'), '').trim(); }

  async function match(row) {
    row.state = 'loading'; draw();
    try {
      var r = await fetch(API + '?q=' + encodeURIComponent(row.text)); var d = await r.json();
      var sku = (row.text.match(/CGAP-[A-Z0-9-]+/i) || [])[0];
      var res = (d.results || []).slice(0, 10).map(function (x, i) { var k = score(row.text, x, i); x._rec = k.rec; x._prec = k.prec; x._s = k.s + (sku && x.sku && x.sku.toUpperCase() === sku.toUpperCase() ? 9 : 0); return x; }).sort(function (a, b) { return b._s - a._s; });
      var opts = [];
      for (var i = 0; i < res.length && opts.length < 3; i++) { var p = await product(res[i].handle); if (p && p.available !== false) opts.push({ handle: res[i].handle, series: (res[i].series || '').toUpperCase(), title: res[i].subject || short(p.title), id: (p.variants.find(function (v) { return v.available; }) || p.variants[0]).id, price: p.price / 100, img: p.featured_image }); }
      row.opts = opts;
      row.pick = opts.length && (res[0]._s >= 9 || (res[0]._rec >= 0.6 && res[0]._prec >= 0.5)) ? 0 : -1;
    } catch (e) { row.opts = []; row.pick = -1; }
    if (row.pick === -1) { row.header = guessHeader(row.text); row.wording = stripHeader(row.text); }
    row.state = 'ok'; draw();
  }
  async function pool(list) { var i = 0; await Promise.all([0, 1, 2, 3].map(async function () { while (i < list.length) { await match(list[i++]); } })); save(); }
  function price(r) { return r.pick >= 0 ? r.opts[r.pick].price : CUSTOM.price; }

  function draw() {
    if (!rows.length) { $rows.innerHTML = ''; $bar.innerHTML = ''; return; }
    var h = '<ul class="sl">';
    rows.forEach(function (r) {
      h += '<li data-id="' + r.id + '"><input type="number" min="1" max="9999" value="' + r.qty + '" data-q style="width:6rem;font-size:1.5rem;padding:.4rem" aria-label="Quantity"><div style="flex:1">';
      h += '<div class="note">You entered: ' + esc(r.text) + '</div>';
      if (r.state === 'loading') h += '<div>Finding a match...</div>';
      else {
        h += '<select data-pick style="max-width:100%;font-size:1.5rem;padding:.4rem;margin:.3rem 0">';
        r.opts.forEach(function (o, i) { h += '<option value="' + i + '"' + (r.pick === i ? ' selected' : '') + '>' + esc((o.series ? o.series + ' ' : '') + o.title) + ' (' + money(o.price) + ')</option>'; });
        h += '<option value="-1"' + (r.pick === -1 ? ' selected' : '') + '>Custom sign with my wording (' + money(CUSTOM.price) + ')</option></select>';
        if (r.pick >= 0) h += ' <a href="/products/' + esc(r.opts[r.pick].handle) + '" target="_blank" class="note">View</a>';
        else h += '<div style="display:flex;gap:.6rem;flex-wrap:wrap"><select data-hdr style="font-size:1.4rem">' + HEADERS.map(function (x) { return '<option' + (x === r.header ? ' selected' : '') + '>' + x + '</option>'; }).join('') + '</select><input data-w value="' + esc(r.wording) + '" maxlength="120" style="flex:1;min-width:180px;font-size:1.4rem;padding:.3rem" aria-label="Sign wording"></div><div class="note">We will make it from your wording. <a href="/pages/custom-sign-designer" target="_blank">Preview it in the designer</a>.</div>';
      }
      h += '</div><div style="min-width:7rem;text-align:right"><b>' + (r.state === 'ok' ? money(price(r) * r.qty) : '') + '</b><br><a href="#" data-x class="note">Remove</a></div></li>';
    });
    h += '</ul>'; $rows.innerHTML = h;
    var ready = rows.filter(function (r) { return r.state === 'ok'; }), n = ready.reduce(function (a, r) { return a + r.qty; }, 0), tot = ready.reduce(function (a, r) { return a + price(r) * r.qty; }, 0);
    $bar.innerHTML = '<div class="bar"><button type="button" class="btn" id="cgb-add"' + (ready.length < rows.length || !n ? ' disabled' : '') + '>Add ' + n + ' sign' + (n === 1 ? '' : 's') + ' to cart (' + money(tot) + ')</button><span class="note">Need a quote or W-9 for a PO? <a href="/pages/government-quote">Build a PO quote</a> with this same list.</span></div>';
  }
  function save() { try { localStorage.setItem(KEY, JSON.stringify(rows.map(function (r) { return { text: r.text, qty: r.qty }; }))); } catch (e) {} }
  function start(text) {
    var list = text.split(/\r?\n/).map(parseLine).filter(Boolean).slice(0, 300);
    if (!list.length) return;
    var add = list.map(function (x) { return { id: ++uid, text: x.text, qty: x.qty, opts: [], pick: -1, state: 'loading' }; });
    rows = rows.concat(add); draw(); pool(add);
  }
  root.querySelector('#cgb-go').addEventListener('click', function () { start($in.value); $in.value = ''; });
  root.querySelector('#cgb-file').addEventListener('change', function (e) { var f = e.target.files[0]; if (!f) return; var rd = new FileReader(); rd.onload = function () { start(String(rd.result)); }; rd.readAsText(f); e.target.value = ''; });
  root.querySelector('#cgb-clear').addEventListener('click', function (e) { e.preventDefault(); rows = []; save(); draw(); });
  $rows.addEventListener('change', function (e) {
    var li = e.target.closest('li'); if (!li) return; var r = rows.find(function (x) { return x.id == li.getAttribute('data-id'); }); if (!r) return;
    if (e.target.matches('[data-q]')) r.qty = Math.max(1, Math.min(9999, parseInt(e.target.value, 10) || 1));
    if (e.target.matches('[data-pick]')) { r.pick = +e.target.value; if (r.pick === -1 && !r.wording) { r.header = guessHeader(r.text); r.wording = stripHeader(r.text); } }
    if (e.target.matches('[data-hdr]')) r.header = e.target.value;
    if (e.target.matches('[data-w]')) r.wording = e.target.value;
    save(); draw();
  });
  $rows.addEventListener('click', function (e) { if (!e.target.matches('[data-x]')) return; e.preventDefault(); var li = e.target.closest('li'); rows = rows.filter(function (x) { return x.id != li.getAttribute('data-id'); }); save(); draw(); });
  $bar.addEventListener('click', async function (e) {
    if (e.target.id !== 'cgb-add') return; var b = e.target; b.disabled = true; b.textContent = 'Adding...';
    var items = rows.map(function (r) { return r.pick >= 0 ? { id: r.opts[r.pick].id, quantity: r.qty } : { id: CUSTOM.id, quantity: r.qty, properties: { Header: r.header || 'NOTICE', Wording: r.wording || r.text, Source: 'Bulk order' } }; });
    var ok = true;
    for (var i = 0; i < items.length; i += 50) { var res = await fetch('/cart/add.js', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ items: items.slice(i, i + 50) }) }); if (!res.ok) ok = false; }
    if (ok) location.href = '/cart'; else { b.disabled = false; b.textContent = 'Some signs could not be added. Try again'; }
  });
  try { var old = JSON.parse(localStorage.getItem(KEY) || '[]'); if (old.length) { $in.value = old.map(function (o) { return o.qty + ' x ' + o.text; }).join('\n'); } } catch (e) {}
  fetch(API + '?q=__warm__').catch(function () {});
})();
