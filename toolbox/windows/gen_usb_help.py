"""Extract the long USB / Apple help texts from the pristine console exe and
build equal-length Chinese replacements, merged into work/zh_direct.json."""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import json, os

EXE = os.path.join(SD_DIR, '原版备份', 'spacedeskConsole.exe')
OUT = os.path.join(ROOT, 'data', 'zh_direct.json')
ZWSP = "\u200b"

b = open(EXE, "rb").read()


def find(text):
    needle = text.encode("utf-16-le")
    i = b.find(needle)
    assert i >= 0, text
    return i


def read_block(start_text, end_text):
    i = find(start_text)
    j = b.find(end_text.encode("utf-16-le"), i)
    assert j >= 0
    raw = b[i:j + len(end_text) * 2]
    assert len(raw) % 2 == 0
    return raw.decode("utf-16-le")


def zh_block(lines):
    return "\r\n".join(lines)


# 1) Android USB cable block
old1 = read_block("!!! ATTENTION - ANDROID USB CABLE COMPATIBILITY !!!",
                  "- Restart Windows PC.")
new1 = zh_block([
    "!!! 注意：安卓 USB 线缆兼容性 !!!",
    " ",
    "开启后会禁用其他 USB 线缆应用！",
    "关闭后可恢复其他应用！",
    " ",
    "受影响的应用：",
    "- 文件传输(USB)",
    "- 联想 SmartConnect(USB)",
    "- 联想 LINK(USB)",
    "- Duet Display(USB)",
    "- Super Display(USB)",
    "等。",
    " ",
    "安卓 USB 线缆故障处理：",
    "- 缓慢插拔 USB 线缆数次。",
    "- 重启安卓移动设备。",
    "- 重启电脑。",
])

# 2) iOS USB cable block
old2 = read_block("In case of iOS USB cable issues:",
                  "- Try original USB cable from Apple.")
new2 = zh_block([
    "苹果 USB 线缆故障处理：",
    "- 请使用苹果原装 USB 线缆。",
])

# 3) Apple service stopped block
old3 = read_block("Apple Mobile Device Service is stopped.",
                  "Please start it on Windows Services desktop app.")
new3 = zh_block([
    "Apple 移动设备服务未启动。",
    "请在 Windows 服务中启动它。",
])

# 4) Apple process stopped block
old4 = read_block("Apple Mobile Device Process is stopped.",
                  "Please open iTunes or Apple Devices app")
new4 = zh_block([
    "Apple 移动设备进程未启动。",
    "请打开 iTunes 或 Apple Devices 应用。",
])

pairs = []
existing = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else []
keep = {}
for pr in existing:
    keep[pr["old"]] = pr

for old, new in ((old1, new1), (old2, new2), (old3, new3), (old4, new4)):
    old_len = len(old)
    assert len(new) <= old_len, (len(new), old_len, new[:40])
    padded = new + ZWSP * (old_len - len(new))
    assert len(padded) == old_len
    print(f"block {old[:34]!r:<40} old={old_len} new={len(new)}")
    keep[old] = {"old": old, "new": padded}

json.dump(list(keep.values()), open(OUT, "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("pairs in zh_direct.json:", len(keep))
