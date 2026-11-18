import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import xml.etree.ElementTree as ET, os, json

D = os.path.join(ROOT, 'android', 'decoded', 'res')


def load(path):
    tree = ET.parse(path)
    root = tree.getroot()
    items = {}
    order = []
    for el in root:
        tag = el.tag
        name = el.get("name")
        if tag == "string":
            items[name] = ("string", (el.text or ""), dict(el.attrib))
            order.append(name)
        elif tag == "plurals":
            vals = {i.get("quantity"): (i.text or "") for i in el}
            items[name] = ("plurals", vals, dict(el.attrib))
            order.append(name)
        elif tag == "string-array":
            vals = [(i.text or "") for i in el]
            items[name] = ("array", vals, dict(el.attrib))
            order.append(name)
    return items, order


en, en_order = load(os.path.join(D, "values", "strings.xml"))
zh_path = os.path.join(D, "values-zh-rCN", "strings.xml")
zh, zh_order = load(zh_path) if os.path.exists(zh_path) else ({}, [])

missing = [k for k in en_order if k not in zh]
print("total en:", len(en), "zh:", len(zh), "missing:", len(missing))
print("kinds:", {k: en[k][0] for k in en_order if en[k][0] != "string"})

out = []
for k in missing:
    kind, val, attrs = en[k]
    out.append({"name": k, "kind": kind, "value": val, "attrs": attrs})
json.dump(out, open(os.path.join(ROOT, 'android', 'missing_en.json'), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("written missing_en.json", len(out))

# also dump full english for reference
allout = [{"name": k, "kind": en[k][0], "value": en[k][1]} for k in en_order]
json.dump(allout, open(os.path.join(ROOT, 'android', 'all_en.json'), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("sample existing zh:")
for k in zh_order[:8]:
    print("  ", k, "=", zh[k][1])
