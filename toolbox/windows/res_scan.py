import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import pefile, sys, os, collections

TYPE_NAMES = {1:'CURSOR',2:'BITMAP',3:'ICON',4:'MENU',5:'DIALOG',6:'STRING',7:'FONTDIR',
              8:'FONT',9:'ACCELERATOR',10:'RCDATA',11:'MESSAGETABLE',12:'GROUP_CURSOR',
              14:'GROUP_ICON',16:'VERSION',17:'DLGINCLUDE',19:'PLUGPLAY',20:'VXD',
              21:'ANICURSOR',22:'ANIICON',23:'HTML',24:'MANIFEST'}

def scan(path):
    pe = pefile.PE(path, fast_load=True)
    pe.parse_data_directories(directories=[
        pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_RESOURCE']])
    print("=" * 78)
    print(path, "|", "PE32+" if pe.PE_TYPE == pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS else "PE32",
          "| sections:", [s.Name.rstrip(b'\0').decode('latin1') for s in pe.sections])
    print("has .NET CLR header:", hasattr(pe, 'DIRECTORY_ENTRY_COM_DESCRIPTOR'))
    if not hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        print("NO RESOURCES")
        return
    counts = collections.Counter()
    for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        tname = entry.name.string.decode() if entry.name else TYPE_NAMES.get(entry.id, str(entry.id))
        counts[tname] += len(entry.directory.entries)
        for sub in entry.directory.entries:
            for lang in sub.directory.entries:
                d = lang.data.struct
                print(f"  {tname:<16} id={sub.id!s:<6} lang=0x{lang.id:04X} size={d.Size:<8} raw=0x{d.OffsetToData:X}")
    print("  summary:", dict(counts))

for p in sys.argv[1:]:
    scan(p)
