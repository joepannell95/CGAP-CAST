"""Turn rows from CGAP's Amazon listing spreadsheets (the 2024+ template whose column keys look like
item_name[marketplace_id=ATVPDKIKX0DER][language_tag=en_US]#1.value) into Listings API attribute JSON.
Enumerated values are mapped with the product type schema (finder.amz_config schema_SIGNAGE) when given."""
import re, json

MP = 'ATVPDKIKX0DER'
SKIP = {'contribution_sku', 'product_type', '::record_action', 'parentage_level', 'child_parent_sku_relationship', 'variation_theme'}
KEY_RE = re.compile(r'^([a-z0-9_.:]+)((?:\[[a-z_]+=[^\]]*\])*)(.*)$')
SEL_RE = re.compile(r'\[([a-z_]+)=([^\]]*)\]')
TOK_RE = re.compile(r'#(\d+)|\.([a-z0-9_]+)')

def parse_key(k):
    m = KEY_RE.match(k)
    if not m: return None
    name, sels, rest = m.group(1), dict(SEL_RE.findall(m.group(2) or '')), m.group(3) or ''
    toks = [(int(a), None) if a else (None, b) for a, b in TOK_RE.findall(rest)]
    return name, sels, toks

def set_path(root, toks, value):
    # toks: sequence like [(1,None),(None,'length'),(None,'value')] or [(1,None),(None,'our_price'),(1,None),(None,'schedule'),(1,None),(None,'value_with_tax')]
    cur = root
    i = 0
    while i < len(toks):
        idx, field = toks[i]
        last = i == len(toks) - 1
        if field is not None:
            nxt = toks[i + 1] if not last else None
            if last:
                cur[field] = value
            elif nxt[0] is not None:  # list follows
                lst = cur.setdefault(field, [])
                while len(lst) < nxt[0]: lst.append({})
                cur = lst[nxt[0] - 1]; i += 1
            else:
                cur = cur.setdefault(field, {})
        i += 1

def rows_to_attributes(row):
    attrs = {}
    product_type = row.get('product_type#1.value') or 'SIGNAGE'
    for k, v in row.items():
        if v in (None, ''): continue
        if k == 'amzn1.volt.ca.product_id_type':
            if str(v).lower().startswith('gtin exempt'):
                attrs['supplier_declared_has_product_identifier_exemption'] = [{'value': True, 'marketplace_id': MP}]
            continue
        p = parse_key(k)
        if not p: continue
        name, sels, toks = p
        if name in SKIP or name.startswith('::'): continue
        if not toks or toks[0][0] is None: continue
        lst = attrs.setdefault(name, [])
        n = toks[0][0]
        while len(lst) < n: lst.append({})
        el = lst[n - 1]
        for sk, sv in sels.items(): el[sk] = sv
        set_path(el, toks[1:], v)
    # fixed-format fields
    for el in attrs.get('item_type_keyword', []):
        m = re.search(r'\(([^()]+)\)\s*$', str(el.get('value', '')))
        if m: el['value'] = m.group(1)
    for el in attrs.get('fulfillment_availability', []):
        if 'fulfillment_channel_code' in el: el['fulfillment_channel_code'] = 'DEFAULT'
    for el in attrs.get('list_price', []): el.setdefault('currency', 'USD')
    for el in attrs.get('purchasable_offer', []): el.setdefault('currency', 'USD'); el.setdefault('audience', 'ALL')
    for name in ('item_weight', 'item_package_weight'):
        for el in attrs.get(name, []):
            if isinstance(el.get('unit'), str): el['unit'] = el['unit'].lower()
    for name in ('item_length_width', 'item_package_dimensions'):
        for el in attrs.get(name, []):
            for d in ('length', 'width', 'height'):
                if isinstance(el.get(d), dict) and isinstance(el[d].get('unit'), str): el[d]['unit'] = el[d]['unit'].lower()
    return product_type, attrs

def coerce_with_schema(attrs, schema):
    """Map display values to schema enums and types (booleans, numbers)."""
    props = schema.get('properties', {})
    def walk(sch, val):
        if isinstance(val, dict):
            p = (sch or {}).get('properties', {})
            return {k: walk(p.get(k), v) for k, v in val.items()}
        if isinstance(val, list):
            it = (sch or {}).get('items')
            return [walk(it, v) for v in val]
        if not sch: return val
        t = sch.get('type')
        enums, names = sch.get('enum'), sch.get('enumNames')
        if enums:
            s = str(val).strip().lower()
            for i, e in enumerate(enums):
                if str(e).lower() == s or (names and i < len(names) and str(names[i]).lower() == s):
                    return e
            if t == 'boolean' or (len(enums) <= 2 and set(map(str, enums)) <= {'True', 'False', 'true', 'false'}):
                return s in ('yes', 'true', '1')
            return val
        if t == 'boolean': return str(val).strip().lower() in ('yes', 'true', '1')
        if t in ('number', 'integer') and isinstance(val, str):
            try: return int(val) if t == 'integer' else float(val)
            except ValueError: return val
        return val
    out = {}
    for name, val in attrs.items():
        out[name] = walk(props.get(name), val)
    return out

if __name__ == '__main__':
    import sys
    found = json.load(open(sys.argv[1]))
    sku = sys.argv[2]
    pt, attrs = rows_to_attributes(found[sku]['row'] if 'row' in found[sku] else found[sku])
    print(pt); print(json.dumps(attrs, indent=1)[:4000])
