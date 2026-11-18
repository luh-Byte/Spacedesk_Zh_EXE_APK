"""Apply equal-length Chinese translations to spacedesk binaries.

Rules
-----
* Every replacement MUST have exactly the same encoded length as the original:
    - #US heap / native Win32 resources: UTF-16LE code units must match
      -> pad with U+200B (zero width space) and, if needed, trailing spaces
    - BAML streams: UTF-8 BYTES must match
      -> pad with U+200B (3 bytes each) and, if needed, trailing spaces
  Keeping the length identical means no offsets move, so the PE / .rsrc /
  BAML / #US structures stay intact.
* Each write is guarded: the original bytes at the target offset must match.
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import json, os, struct, sys, re

CONSOLE = os.path.join(SD_DIR, 'spacedeskConsole.exe')
TRAY = os.path.join(SD_DIR, 'spacedeskServiceTray.exe')
BAML_DIR = os.path.join(ROOT, 'work', 'console_baml')
INV = os.path.join(ROOT, 'work', 'inventory.json')
TABLE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'data', 'zh_table.json')
DRY = '--apply' not in sys.argv

ZWSP = '\u200b'

def pad_utf16(new, target_cu):
    """pad to exactly target_cu UTF-16 code units."""
    cur = len(new)
    if cur > target_cu:
        return None
    need = target_cu - cur
    z = min(need // 1, need)  # ZWSP counts as 1 code unit
    out = new + ZWSP * need
    return out

def pad_utf8(new, target_bytes):
    b = new.encode('utf-8')
    if len(b) > target_bytes:
        return None
    need = target_bytes - len(b)
    zw = need // 3
    rest = need - zw * 3
    out = new + ZWSP * zw + ' ' * rest
    if len(out.encode('utf-8')) != target_bytes:
        return None
    return out

def locate_baml_streams(exe_path):
    """map baml file name -> absolute file offset of its stream inside the exe"""
    data = open(exe_path, 'rb').read()
    out = {}
    for fn in sorted(os.listdir(BAML_DIR)):
        if not fn.endswith('.baml'):
            continue
        b = open(os.path.join(BAML_DIR, fn), 'rb').read()
        needle = b[:32]
        pos = data.find(needle)
        if pos < 0:
            continue
        # verify the whole stream starts here (compare 64 bytes)
        if data[pos:pos + 64] != b[:64]:
            continue
        out[fn] = pos
    return out

def main():
    table = json.load(open(TABLE, encoding='utf-8'))
    inv = json.load(open(INV, encoding='utf-8'))
    def target(f):
        fn = os.path.basename(f).lower()
        return TRAY if 'tray' in fn else CONSOLE
    streams = locate_baml_streams(CONSOLE)
    print("baml streams located:", len(streams))

    # group inventory items by translated text
    plan = []   # (file, offset, oldbytes, newbytes, label)
    missing, overflow = [], []

    for it in inv:
        src = it['src']
        zh = table.get(f"{src}::{it['text']}") or table.get(it['text'])
        if zh is None or it['text'] == '_note':
            continue
        if src in ('us', 'native'):
            target_cu = it['nchars'] if src == 'us' else it['len'] // 2
            padded = pad_utf16(zh, target_cu)
            if padded is None:
                overflow.append((it['text'], zh, src)); continue
            old = it['text'].encode('utf-16-le')
            new = padded.encode('utf-16-le')
            if len(new) != len(old):
                overflow.append((it['text'], zh, src)); continue
            plan.append((target(it['file']), it['off'], old, new, f"{src}:{it['text'][:40]}"))
        elif src == 'baml':
            target_bytes = it['len']
            padded = pad_utf8(zh, target_bytes)
            if padded is None:
                overflow.append((it['text'], zh, src)); continue
            old = it['text'].encode('utf-8')
            new = padded.encode('utf-8')
            if len(new) != len(old):
                overflow.append((it['text'], zh, src)); continue
            fn = os.path.basename(it['file'])
            base = streams.get(fn)
            if base is None:
                missing.append(it['file']); continue
            plan.append((CONSOLE, base + it['off'], old, new, f"baml:{it['text'][:40]}"))

    # ---- direct needle replacements (for strings the scanner could not reach) ----
    direct_path = os.path.join(os.path.dirname(TABLE), 'zh_direct.json')
    direct_plan = []
    if os.path.exists(direct_path):
        pairs = json.load(open(direct_path, encoding='utf-8'))
        inv_texts = {it['text'] for it in inv}
        for pr in pairs:
            old_s, new_s = pr['old'], pr['new']
            if old_s in inv_texts:
                continue
            old_b = old_s.encode('utf-16-le')
            padded = pad_utf16(new_s, len(old_s))
            if padded is None:
                print("  OVERFLOW-direct", repr(old_s), '->', repr(new_s)); continue
            new_b = padded.encode('utf-16-le')
            if len(new_b) != len(old_b):
                print("  LENMISMATCH-direct", repr(old_s)); continue
            data = open(CONSOLE, 'rb').read()
            start = 0
            hits = 0
            while True:
                i = data.find(old_b, start)
                if i < 0:
                    break
                direct_plan.append((CONSOLE, i, old_b, new_b, f"direct:{old_s[:30]}"))
                start = i + len(old_b)
                hits += 1
            if hits == 0:
                print("  MISS-direct", repr(old_s))
        print("direct writes:", len(direct_plan))

    plan.extend(direct_plan)

    # ---- direct needle replacements in UTF-8 (BAML long strings with 2-byte length prefix) ----
    u8_path = os.path.join(os.path.dirname(TABLE), 'zh_direct_u8.json')
    u8_plan = []
    if os.path.exists(u8_path):
        pairs = json.load(open(u8_path, encoding='utf-8'))
        for pr in pairs:
            old_s, new_s = pr['old'], pr['new']
            old_b = old_s.encode('utf-8')
            padded = pad_utf8(new_s, len(old_b))
            if padded is None:
                print("  OVERFLOW-u8", repr(old_s), '->', repr(new_s)); continue
            new_b = padded.encode('utf-8')
            if len(new_b) != len(old_b):
                print("  LENMISMATCH-u8", repr(old_s)); continue
            data = open(CONSOLE, 'rb').read()
            start = 0
            hits = 0
            while True:
                i = data.find(old_b, start)
                if i < 0:
                    break
                u8_plan.append((CONSOLE, i, old_b, new_b, f"u8:{old_s[:30]}"))
                start = i + len(old_b)
                hits += 1
            if hits == 0:
                print("  MISS-u8", repr(old_s))
        print("u8 writes:", len(u8_plan))
    plan.extend(u8_plan)

    # validate guards
    bad = []
    for f, off, old, new, label in plan:
        if f == CONSOLE or f == TRAY:
            data = open(f, 'rb').read()
        else:
            data = open(CONSOLE, 'rb').read()
        if data[off:off + len(old)] != old:
            bad.append((label, off))

    print(f"planned writes: {len(plan)}  guard-mismatch: {len(bad)}  overflow: {len(overflow)}  missing-stream: {len(missing)}")
    for lb in bad[:10]:
        print("  MISMATCH", lb)
    for ov in overflow[:20]:
        print("  OVERFLOW", ov[2], repr(ov[0]), "->", repr(ov[1]))

    if DRY:
        print("dry-run only; pass --apply to write")
        return

    # apply: write console then tray
    buffers = {}
    for f, off, old, new, label in plan:
        if f not in buffers:
            buffers[f] = bytearray(open(f, 'rb').read())
        if buffers[f][off:off + len(old)] != old:
            print("SKIP (changed meanwhile)", label); continue
        buffers[f][off:off + len(old)] = new
    for f, buf in buffers.items():
        open(f, 'wb').write(bytes(buf))
        print("written:", f, len(buf))

main()
