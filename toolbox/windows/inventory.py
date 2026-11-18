"""Inventory translatable UI strings from spacedesk binaries.

Sources:
  us     -> .NET #US heap entries inside spacedeskConsole.exe (.text section, UTF-16LE)
  baml   -> UTF-8 string records in extracted *.baml streams
  native -> Win32 MENU / DIALOG / STRING tables of spacedeskServiceTray.exe
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import pefile, json, struct, sys, os, re

console = os.path.join(SD_DIR, '原版备份', 'spacedeskConsole.exe')
tray = os.path.join(SD_DIR, '原版备份', 'spacedeskServiceTray.exe')
baml_dir = os.path.join(ROOT, 'work', 'console_baml')
out = os.path.join(ROOT, 'work', 'inventory.json')

items = []

# ---------------- 1) #US heap ----------------
pe = pefile.PE(console)
data = open(console, 'rb').read()
for sec in pe.sections:
    name = sec.Name.rstrip(b'\x00').decode()
    if name != '.text':
        continue
    raw_s, raw_len = sec.PointerToRawData, sec.SizeOfRawData
    blob = data[raw_s:raw_s + raw_len]
    i = 0
    while i < len(blob) - 1:
        if 0x20 <= blob[i] <= 0x7e and blob[i + 1] == 0:
            j = i; chars = []
            while j < len(blob) - 1 and 0x20 <= blob[j] <= 0x7e and blob[j + 1] == 0:
                chars.append(chr(blob[j])); j += 2
            s = ''.join(chars)
            if len(s) >= 2:
                # validate as a #US entry: byte(s) immediately before encode len*2+1
                need = len(s) * 2 + 1
                ok = False
                for plen in (1, 2):
                    if i - plen < 0:
                        continue
                    if plen == 1:
                        pre = blob[i - 1]
                        if pre == need:
                            ok = True
                        # continuation form for values >= 0x80
                        if pre == (need & 0x7f) | 0x80 and i - 2 >= 0 and blob[i - 2] == (need >> 7):
                            ok = True
                    else:
                        b0, b1 = blob[i - 2], blob[i - 1]
                        v = (b1 << 7) | (b0 & 0x7f) if (b0 & 0x80) else None
                        if v == need:
                            ok = True
                    if ok:
                        break
                if ok:
                    items.append({'src': 'us', 'file': console, 'off': raw_s + i,
                                  'len': len(s) * 2, 'nchars': len(s), 'text': s})
                i = j
        i += 1

# ---------------- 2) BAML ----------------
for fn in sorted(os.listdir(baml_dir)):
    if not fn.endswith('.baml'):
        continue
    pth = os.path.join(baml_dir, fn)
    b = open(pth, 'rb').read()
    for pos in range(len(b)):
        L = b[pos]
        if not (3 <= L <= 127) or pos + 1 + L > len(b):
            continue
        chunk = b[pos + 1:pos + 1 + L]
        if any(c < 0x20 for c in chunk):
            continue
        try:
            s = chunk.decode('utf-8')
        except Exception:
            continue
        if not re.fullmatch(r'[\x20-\x7e]{3,}', s):
            continue
        items.append({'src': 'baml', 'file': pth, 'off': pos + 1, 'len': L, 'text': s})

# ---------------- 3) native tray ----------------
tpe = pefile.PE(tray)
tpe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])

def rva2off(rva):
    return tpe.get_offset_from_rva(rva)

for entry in tpe.DIRECTORY_ENTRY_RESOURCE.entries:
    if entry.id not in (4, 5, 6):
        continue
    kind = {4: 'MENU', 5: 'DLG', 6: 'STRTBL'}[entry.id]
    for sub in entry.directory.entries:
        for lang in sub.directory.entries:
            d = lang.data.struct
            base = rva2off(d.OffsetToData)
            blob = tpe.get_data(d.OffsetToData, d.Size)
            if entry.id == 6:
                o = 0
                for idx in range(16):
                    if o + 2 > len(blob):
                        break
                    n = struct.unpack_from('<H', blob, o)[0]
                    if n == 0:
                        o += 2; continue
                    txt = blob[o + 2:o + 2 + n * 2].decode('utf-16-le', 'replace')
                    items.append({'src': 'native', 'kind': kind, 'file': tray, 'id': sub.id,
                                  'off': base + o + 2, 'len': n * 2, 'text': txt,
                                  'blk': sub.id, 'idx': idx})
                    o += 2 + n * 2
            else:
                s = blob.decode('utf-16-le', 'replace')
                for m in re.finditer(r'[\x20-\x7e]{2,}', s):
                    items.append({'src': 'native', 'kind': kind, 'file': tray, 'id': sub.id,
                                  'off': base + m.start() * 2, 'len': len(m.group()) * 2,
                                  'text': m.group()})

json.dump(items, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("total:", len(items), {s: sum(1 for i in items if i['src'] == s) for s in ('us', 'baml', 'native')})
print("us strings:", sum(1 for i in items if i['src'] == 'us'))
