"""CGAP batch pipeline: one ChatGPT-style CSV in, everything out.

usage:
  python3 cgap_batch.py check   BATCH.csv            # QA only, writes qa report + contact sheet
  python3 cgap_batch.py render  BATCH.csv            # sign + 2 lifestyle images per row
  python3 cgap_batch.py publish BATCH.csv            # copy images to cgap-cast/signs, git push
  python3 cgap_batch.py build   BATCH.csv            # Shopify import CSV + Amazon .xlsm
  python3 cgap_batch.py all     BATCH.csv            # check, render, publish, build

Input columns (from the ChatGPT prompt): sku, division, division_label, sector_label, subseries,
header, line1..line4, subject, space, required_action, buyer, purpose, install_point, title,
bullet1..bullet5, description, keywords
"""
import csv, os, re, sys, json, glob, html, shutil, subprocess, importlib.util, collections
from multiprocessing import Pool

ROOT = "/home/claude/cgap"; REPO = "/home/claude/cgap-cast"; IMGDIR = f"{REPO}/signs"
RAW = "https://raw.githubusercontent.com/joepannell95/CGAP-CAST/main/signs/"
AMZ_TPL = "/mnt/attach/outputs/cgap5000/SIGNAGE_WARNING_W18_447.xlsm"
RENDERERS = {"DANGER": "render.py", "WARNING": "render_w.py", "CAUTION": "render_c.py",
             "NOTICE": "render_n.py", "SAFETY FIRST": "render_i.py"}
COMMODITY = re.compile(r"\b(BEWARE OF (THE )?DOG|NO SMOKING|NO VAPING|NO TRESPASSING|SMILE,? YOU'?RE ON CAMERA|WET FLOOR|"
                       r"EMERGENCY EXIT|^EXIT$|RESTROOM|SPEED LIMIT|TOW AWAY ZONE)\b")
CLAIMS = re.compile(r"osha[- ]compliant|ada[- ]compliant|guarantee[sd]? compliance|meets all|design preview", re.I)
# Words that got Amazon listings removed (trademark misuse, or read as a lithium battery product), Nov 2026
AMZ_FLAGGED = re.compile(r"magnehelic|jack rack|mower shop|staging mat|lithium|batter(y|ies) (plant|module|pack|cell)", re.I)
LINES = ("line1", "line2", "line3", "line4")

def load(p):
    rows = list(csv.DictReader(open(p, encoding="utf-8-sig")))
    for r in rows:
        r["lines"] = [r[k].strip().upper() for k in LINES if r.get(k, "").strip()]
        r["reads"] = " / ".join(r["lines"]); s = r["sku"].lower()
        r["img"] = [f"{s}.jpg", f"{s}-durability.jpg", f"{s}-mnt2.jpg"]
        r["handle"] = re.sub(r"[^a-z0-9]+", "-", f"{r['header']} {r['subject']} sign {s}".lower()).strip("-")
    return rows

def batch_name(p): return os.path.splitext(os.path.basename(p))[0]

# ---------- QA ----------
def existing_texts():
    seen = set()
    for f in glob.glob(f"{ROOT}/**/catalog_*.json", recursive=True):
        try:
            for x in json.load(open(f)): seen.add(re.sub(r"\W+", " ", " ".join(x.get("lines", []))).strip().upper())
        except Exception: pass
    return seen

def check(p):
    rows = load(p); out = f"{ROOT}/pipeline/out/{batch_name(p)}"; os.makedirs(out, exist_ok=True)
    seen = existing_texts(); issues = []; key = collections.Counter(); skus = collections.Counter(r["sku"] for r in rows)
    norm = lambda r: re.sub(r"\W+", " ", " ".join(r["lines"])).strip().upper()
    for r in rows: key[norm(r)] += 1
    for r in rows:
        bad = []
        if not re.fullmatch(r"CGAP-[A-Z0-9]+-812", r["sku"]): bad.append("sku format")
        if skus[r["sku"]] > 1: bad.append("duplicate sku")
        if r["header"] not in RENDERERS: bad.append(f"unknown header {r['header']}")
        if not 2 <= len(r["lines"]) <= 4: bad.append("needs 2-4 lines")
        if any(len(l) > 28 for l in r["lines"]): bad.append("line over 28 chars")
        if key[norm(r)] > 1: bad.append("duplicate wording in batch")
        if norm(r) in seen: bad.append("matches existing catalog")
        if COMMODITY.search(r["reads"]): bad.append("commodity wording")
        blob = " ".join(str(v) for v in r.values() if isinstance(v, str))
        if "—" in blob: bad.append("em dash")
        if CLAIMS.search(blob): bad.append("compliance claim")
        if AMZ_FLAGGED.search(blob): bad.append("word Amazon flags (trademark or battery)")
        if len(r["title"]) > 200: bad.append("title over 200")
        if not r["title"].startswith(r["header"]): bad.append("title must start with header")
        if bad: issues.append((r["sku"], r["reads"], "; ".join(bad)))
    with open(f"{out}/qa_issues.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["sku", "reads", "issues"]); w.writerows(issues)
    print(f"QA {len(rows)} rows, {len(issues)} with issues, headers {dict(collections.Counter(r['header'] for r in rows))}")
    for i in issues[:15]: print("  ", i)
    return rows, issues

# ---------- render ----------
_mods = {}
def renderer(h):
    if h not in _mods:
        sys.path.insert(0, f"{ROOT}/render"); sys.path.insert(0, f"{ROOT}/comp")
        spec = importlib.util.spec_from_file_location(f"r_{h}", f"{ROOT}/render/{RENDERERS[h]}")
        m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); _mods[h] = m
    return _mods[h]

def _work(r):
    import cv2, numpy as np
    sys.path.insert(0, f"{ROOT}/comp"); import composite_w as composite
    main, dur, mnt = [os.path.join(IMGDIR, x) for x in r["img"]]
    stamp = f"{ROOT}/pipeline/stamps/{r['img'][0]}.txt"
    if all(os.path.exists(x) for x in (main, dur, mnt, stamp)) and open(stamp).read() == r["header"] + r["reads"]: return 0
    im = renderer(r["header"]).render(r["lines"]); im.save(main, quality=86, optimize=True)
    bgr = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
    for kind, path in (("durability", dur), ("mnt2", mnt)):
        tmp = path + ".tmp.jpg"; composite.make(bgr, kind, tmp, q=95)
        x = cv2.imread(tmp); h, w = x.shape[:2]
        x = cv2.resize(x, (1200, round(h * 1200 / w)), interpolation=cv2.INTER_AREA)
        cv2.imwrite(path, x, [cv2.IMWRITE_JPEG_QUALITY, 82, cv2.IMWRITE_JPEG_OPTIMIZE, 1]); os.remove(tmp)
    open(stamp, "w").write(r["header"] + r["reads"]); return 1

def render(p):
    rows = load(p); os.makedirs(f"{ROOT}/pipeline/stamps", exist_ok=True)
    with Pool(max(1, os.cpu_count())) as pool: n = sum(pool.imap_unordered(_work, rows, chunksize=8))
    print(f"rendered {n} new of {len(rows)}"); contact(p, rows)

def contact(p, rows, n=40):
    from PIL import Image
    out = f"{ROOT}/pipeline/out/{batch_name(p)}"; os.makedirs(out, exist_ok=True)
    tw, th, cols = 300, 200, 8; pick = rows[:: max(1, len(rows) // n)][:n]
    sheet = Image.new("RGB", (tw * cols, th * ((len(pick) + cols - 1) // cols)), "white")
    for i, r in enumerate(pick):
        im = Image.open(os.path.join(IMGDIR, r["img"][0])); im.thumbnail((tw - 6, th - 6))
        sheet.paste(im, ((i % cols) * tw + 3, (i // cols) * th + 3))
    sheet.save(f"{out}/contact_sheet.jpg", quality=80); print("contact sheet", f"{out}/contact_sheet.jpg")

# ---------- publish images ----------
def publish(p):
    rows = load(p); files = [f"signs/{x}" for r in rows for x in r["img"]]
    def g(*a): return subprocess.run(["git", "-C", REPO, *a], capture_output=True, text=True)
    for i in range(0, len(files), 500): g("add", *files[i:i + 500])
    c = g("commit", "-m", f"Add sign images for batch {batch_name(p)}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_0159dJFmxJsHQCsQQZibYUai")
    print(c.stdout.strip().splitlines()[:1] or c.stderr.strip()[:200])
    r = g("push", "origin", "HEAD:main"); print("push", r.returncode, (r.stderr or r.stdout).strip()[-200:])

# ---------- listings ----------
def esc(s): return html.escape(s or "", quote=False)
def body(r):
    b = [r.get(f"bullet{i}", "") for i in range(1, 6)]
    return (f"<p>{esc(r['description'])}</p><p>This {esc(r['header'])} sign from CGAP Safety reads: <strong>{esc(r['reads'])}</strong>.</p>"
            f"<h3>Why this sign matters</h3><p>{esc(r['purpose'])}</p><h3>Where to post it</h3><p>{esc(r['install_point'])}</p>"
            f"<h3>Who orders it</h3><p>{esc(r['buyer'])}</p>"
            "<p>Rust-resistant .065 aluminum, UV-resistant print, pre-drilled in all four corners. Made in the USA. "
            "A sign supports your site rules and procedures; it does not replace training or supervision.</p>")

HEAD = ["Handle", "Title", "Body (HTML)", "Vendor", "Product Category", "Type", "Tags", "Published", "Option1 Name", "Option1 Value",
        "Variant SKU", "Variant Grams", "Variant Inventory Tracker", "Variant Inventory Policy", "Variant Fulfillment Service",
        "Variant Price", "Variant Compare At Price", "Variant Requires Shipping", "Variant Taxable", "Image Src", "Image Position",
        "Image Alt Text", "Gift Card", "SEO Title", "SEO Description", "Variant Weight Unit", "Status"]

def build(p, price="29.99"):
    from openpyxl import load_workbook
    rows = load(p); name = batch_name(p); out = f"{ROOT}/pipeline/out/{name}"; os.makedirs(out, exist_ok=True)
    tag_batch = f"Batch {name}"
    with open(f"{out}/{name}_Shopify_Import.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=HEAD); w.writeheader()
        for r in rows:
            alt = f"{r['header']} {r['subject']} Sign 8x12"
            tags = ["CGAP Safety", r["header"].title(), "Made in USA", "8x12 Aluminum", f"Division: {r['division_label']}",
                    f"Sector: {r['sector_label']}", f"Sub-series: {r['subseries']}", tag_batch, "New Signs"]
            first = {h: "" for h in HEAD}
            first.update({"Handle": r["handle"], "Title": r["title"], "Body (HTML)": body(r), "Vendor": "CGAP Industries", "Type": "Safety Sign",
                "Tags": ", ".join(tags), "Published": "TRUE", "Option1 Name": "Title", "Option1 Value": "Default Title", "Variant SKU": r["sku"],
                "Variant Grams": "227", "Variant Inventory Policy": "deny", "Variant Fulfillment Service": "manual", "Variant Price": price,
                "Variant Requires Shipping": "TRUE", "Variant Taxable": "TRUE", "Image Src": RAW + r["img"][0], "Image Position": "1",
                "Image Alt Text": alt, "Gift Card": "FALSE", "SEO Title": f"{r['header']} {r['subject']} Sign | 8x12 Aluminum | CGAP Safety"[:70],
                "SEO Description": f"{r['header']} {r['subject']} sign reads {r['reads']}. .065 aluminum, pre-drilled, made in the USA."[:320],
                "Variant Weight Unit": "oz", "Status": "draft"})
            w.writerow(first)
            for i, suf in ((1, " indoor outdoor durability"), (2, " mounting")):
                x = {h: "" for h in HEAD}; x.update({"Handle": r["handle"], "Image Src": RAW + r["img"][i], "Image Position": str(i + 1), "Image Alt Text": alt + suf}); w.writerow(x)
    VAR = {1, 7, 20, 22, 23, 30, 31, 32, 33, 34, 35, 36, 56}
    wb0 = load_workbook(AMZ_TPL, keep_vba=True); ws0 = wb0["Template"]
    const = {c: ws0.cell(8, c).value for c in range(1, ws0.max_column + 1) if ws0.cell(8, c).value not in (None, "") and c not in VAR}
    for part in range(0, len(rows), 800):
        chunk = rows[part:part + 800]
        wb = load_workbook(AMZ_TPL, keep_vba=True); ws = wb["Template"]
        for rr in range(8, ws.max_row + 1):
            for c in range(1, ws.max_column + 1): ws.cell(rr, c).value = None
        for i, r in enumerate(chunk):
            row = 8 + i
            for c, v in const.items(): ws.cell(row, c).value = v
            ws.cell(row, 83).value = r["header"].title()
            ws.cell(row, 1).value = r["sku"]; ws.cell(row, 56).value = r["sku"]; ws.cell(row, 7).value = r["title"]
            for col, k in ((20, 0), (22, 1), (23, 2)): ws.cell(row, col).value = RAW + r["img"][k]
            ws.cell(row, 30).value = r["description"][:2000]
            for j in range(5): ws.cell(row, 31 + j).value = r.get(f"bullet{j + 1}", "")[:500]
            ws.cell(row, 36).value = r["keywords"][:250]
        q = f"{out}/{name}_Amazon_{part // 800 + 1}.xlsm"; wb.save(q)
    print("built", out, os.listdir(out))

if __name__ == "__main__":
    cmd, p = sys.argv[1], sys.argv[2]
    if cmd in ("jsonl", "upload"): pass
    if cmd in ("check", "all"):
        _, iss = check(p)
        if cmd == "all" and iss and "--force" not in sys.argv: sys.exit("QA issues found; fix or rerun with --force")
    if cmd in ("render", "all"): render(p)
    if cmd in ("publish", "all"): publish(p)
    if cmd in ("build", "all"): build(p)

# ---------- Shopify bulk (productSet JSONL for bulkOperationRunMutation) ----------
BULK_MUTATION = ("mutation call($productSet: ProductSetInput!) { productSet(input: $productSet) "
                 "{ product { id handle } userErrors { field message } } }")
def shopify_jsonl(p, price="29.99", status="DRAFT"):
    rows = load(p); name = batch_name(p); out = f"{ROOT}/pipeline/out/{name}"; os.makedirs(out, exist_ok=True)
    q = f"{out}/{name}_productSet.jsonl"
    with open(q, "w", encoding="utf-8") as f:
        for r in rows:
            alt = f"{r['header']} {r['subject']} Sign 8x12"
            tags = ["CGAP Safety", r["header"].title(), "Made in USA", "8x12 Aluminum", f"Division: {r['division_label']}",
                    f"Sector: {r['sector_label']}", f"Sub-series: {r['subseries']}", f"Batch {name}", "New Signs"]
            ps = {"title": r["title"], "handle": r["handle"], "descriptionHtml": body(r), "vendor": "CGAP Industries",
                  "productType": "Safety Sign", "status": status, "tags": tags,
                  "seo": {"title": f"{r['header']} {r['subject']} Sign | 8x12 Aluminum | CGAP Safety"[:70],
                          "description": f"{r['header']} {r['subject']} sign reads {r['reads']}. .065 aluminum, pre-drilled, made in the USA."[:320]},
                  "productOptions": [{"name": "Title", "values": [{"name": "Default Title"}]}],
                  "variants": [{"optionValues": [{"optionName": "Title", "name": "Default Title"}], "price": price, "sku": r["sku"],
                                "inventoryPolicy": "DENY", "taxable": True,
                                "inventoryItem": {"tracked": False, "requiresShipping": True, "measurement": {"weight": {"value": 8, "unit": "OUNCES"}}}}],
                  "files": [{"originalSource": RAW + r["img"][i], "contentType": "IMAGE", "alt": alt + s}
                            for i, s in ((0, ""), (1, " indoor outdoor durability"), (2, " mounting"))]}
            f.write(json.dumps({"productSet": ps}) + "\n")
    print("jsonl", q, len(rows)); return q

def upload_staged(jsonl, url, params_json):
    """POST the JSONL to the staged-upload target returned by stagedUploadsCreate."""
    params = json.loads(params_json)
    args = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", url]
    for k in params: args += ["-F", f"{k['name']}={k['value']}"]
    args += ["-F", f"file=@{jsonl}"]
    print("upload", subprocess.run(args, capture_output=True, text=True).stdout)

if __name__ == "__main__" and sys.argv[1] == "jsonl": shopify_jsonl(sys.argv[2])
if __name__ == "__main__" and sys.argv[1] == "upload": upload_staged(sys.argv[2], sys.argv[3], sys.argv[4])
