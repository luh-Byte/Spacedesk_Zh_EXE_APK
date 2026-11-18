import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import pefile, re, sys, struct

def wide_strings(data, minlen=3):
    out = []
    i = 0
    n = len(data)
    while i < n - 1:
        if 0x20 <= data[i] <= 0x7e and data[i+1] == 0:
            j = i
            chars = []
            while j < n-1 and (0x20 <= data[j] <= 0x7e) and data[j+1] == 0:
                chars.append(chr(data[j])); j += 2
            s = ''.join(chars)
            if len(s) >= minlen:
                out.append((i, s))
                i = j
        i += 1
    return out

def ascii_strings(data, minlen=5):
    out = []
    cur = []
    start = 0
    for i, b in enumerate(data):
        if 0x20 <= b <= 0x7e:
            if not cur: start = i
            cur.append(chr(b))
        else:
            if len(cur) >= minlen:
                out.append((start, ''.join(cur)))
            cur = []
    if len(cur) >= minlen:
        out.append((start, ''.join(cur)))
    return out

for path in sys.argv[1:]:
    pe = pefile.PE(path, fast_load=True)
    print("#" * 90)
    print("FILE:", path)
    imagebase = pe.OPTIONAL_HEADER.ImageBase
    for sec in pe.sections:
        name = sec.Name.rstrip(b'\0').decode('latin1')
        if name not in ('.text', '.rdata', '.data'):
            continue
        data = sec.get_data()
        va = imagebase + sec.VirtualAddress
        print(f"---- section {name}  size={len(data)}  va=0x{va:X}")
        for off, s in wide_strings(data):
            if len(s) < 3: continue
            print(f"  W {va+off:08X} +{off:06X} ({len(s):3d}) {s}")
