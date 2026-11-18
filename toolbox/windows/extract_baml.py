import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import dnfile, sys, os

path, outdir = sys.argv[1], sys.argv[2]
dn = dnfile.dnPE(path)
os.makedirs(outdir, exist_ok=True)
for e in dn.net.resources:
    nm = str(e.name)
    if not nm.endswith('.g.resources'):
        continue
    d = e.data
    for ent in d.entries:
        data = ent.data if isinstance(ent.data, (bytes, bytearray)) else getattr(ent, 'value', None)
        if data is None or not isinstance(data, (bytes, bytearray)):
            print("skip", ent.name, type(ent.data)); continue
        p = os.path.join(outdir, str(ent.name).replace('/', '_'))
        with open(p, 'wb') as f:
            f.write(data)
        print(f"{str(ent.name):<48}{len(data):>8}")
