"""Verify that native (tray) translations really landed in the patched exe."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import json

INV = os.path.join(ROOT, 'work', 'inventory.json')
TABLE = os.path.join(ROOT, 'data', 'zh_table.json')
TRAY = os.path.join(SD_DIR, 'spacedeskServiceTray.exe')

inv = json.load(open(INV, encoding="utf-8"))
table = json.load(open(TABLE, encoding="utf-8"))
data = open(TRAY, "rb").read()

ok = miss = skip = 0
for it in inv:
    if it["src"] != "native":
        continue
    zh = table.get("native::" + it["text"]) or table.get(it["text"])
    if zh is None:
        skip += 1
        continue
    needle = zh.strip("\u200b").strip().encode("utf-16-le")
    # ignore pure-ASCII results (nothing to prove)
    if all(ord(c) < 128 for c in zh):
        skip += 1
        continue
    if data.count(needle) > 0:
        ok += 1
    else:
        miss += 1
        print("MISSING in exe:", repr(it["text"]), "->", repr(zh))

print(f"native verified={ok} missing={miss} skipped(no translation/ascii)={skip}")
