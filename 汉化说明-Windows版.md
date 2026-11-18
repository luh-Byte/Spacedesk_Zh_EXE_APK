# Windows 版汉化说明

汉化对象：`spacedeskConsole.exe`（WPF 控制台，.NET Framework）、`spacedeskServiceTray.exe`（托盘，原生 Win32）
未改动：`spacedeskService.exe`（后台服务，不含界面文本）

## 原理

两个 exe 的界面文字只有两个来源：

1. `spacedeskConsole.exe` 的 `#US` 字符串堆（C# 代码里的动态文案）与 12 个 `.baml` 资源流（编译后的 XAML 静态标签）；
2. `spacedeskServiceTray.exe` 的 `MENU` / `DIALOG` / `STRINGTABLE` 资源。

本机没有 VS 与 .NET Framework 参考程序集，无法反编译重建 WPF 工程，因此采用**等长原地字节替换**：

- BAML 里的字符串按 **UTF-8 字节数**对齐；
- `#US` 堆与 Win32 资源按 **UTF-16 编码单元数**对齐；
- 差额用 U+200B 零宽空格与尾随空格补齐。

因为长度不变，所有偏移、长度字段、PE 结构、BAML 记录流都不移动，不需要重建程序，也不会引起错位或乱码。

本次共替换 **362 处**（控制台 306 处 + 托盘 56 处）。

## 已汉化范围

- 主界面：窗口标题、横幅、左侧树（控制 / 通信接口一览 / 局域网网卡 / USB 线缆驱动(安卓)(苹果) / 连接 / USB / 局域网 / 已断开 / 诊断 / 系统信息 / 第三方安全软件 / 不兼容软件产品 / 视频墙）
- 右栏：控制与设置分区、三个操作按钮、延迟输入项、状态栏、版本行
- 通信接口一览：局域网连接、USB 安卓线缆 / USB 苹果 开关及下方全部说明文字
- 系统信息 / 第三方安全软件 / 不兼容的软件产品 / 视频墙设置 / 诊断信息面板
- 托盘程序：右键菜单、通知气泡标题（「spacedesk 连接通知」）、「打开 spacedesk 驱动控制台…」按钮、各错误与警告提示串

## 仍是英文的部分

| 内容 | 原因 |
|---|---|
| `ON` / `OFF` 单选标签 | 源串只有 2 / 3 字节，放不下「开 / 关」，且两侧对称布局，保留更协调 |
| 控制面板 `New` 按钮 | BAML 里只有 3 字节，只够 1 个汉字 |
| 「状态: OK」中的 `OK` | 单字节占位，且属通用状态码 |
| 硬件与产品名 | 网卡型号、`Windows Defender`、`火绒安全软件`、`Duet Display`、`Amyuni USB 移动屏`、`MCT Desktop…` 等专有名 |
| 托盘连接气泡正文 | 「1 Connection(s) pending…」由服务端生成，本地资源中无此串 |

## 注意事项

- 补丁后 **Authenticode 签名失效**（Windows 可能提示「未知发布者」），功能不受影响。
- 升级 spacedesk 会覆盖这两个 exe，汉化随之失效；需重新打补丁，或用 `还原原版.bat` 回退。
- `spacedeskService` 服务未做任何改动。

## 安装与还原

安装：把 `windows/` 下两个 exe 复制到 spacedesk 安装目录（默认 `C:\Program Files\spacedesk`）覆盖同名文件，然后重启托盘程序。若安装在别的路径，设环境变量 `SPACEDESK_DIR` 指向该目录，脚本会优先使用它。

还原：双击 `windows/还原原版.bat`。它会结束控制台与托盘进程、从安装目录下的 `原版备份` 子目录拷回原始 exe 并重启托盘。**因此套用补丁前请先把两个原始 exe 备份到 `原版备份\`。**

## 工具链

| 文件 | 用途 |
|---|---|
| `toolbox/windows/extract_baml.py` | 从 .NET 资源集导出 12 个 `.baml` 供比对 |
| `toolbox/windows/inventory.py` | 扫描 `#US` / BAML / Win32 资源，生成全量可译串清单 `work/inventory.json` |
| `toolbox/windows/gen_usb_help.py` | 生成 USB / Apple 长段说明的等长中文块 |
| `toolbox/windows/patch.py` | 打补丁主程序：默认 dry-run 并逐条做原字节校验，`--apply` 才写入 |
| `toolbox/windows/verify_native.py` | 回读校验托盘资源中文是否真的写进 exe |
| `toolbox/windows/printwin.ps1`、`uia_select.ps1` | 抓取分层窗口截图、UI 自动化切换面板（截图用） |
| `data/zh_table.json`、`data/zh_direct.json` | 译文表（源类型 + 原文 + 中文），补丁唯一输入 |

打补丁前必须先关闭 `spacedeskConsole` 与 `spacedeskServiceTray`，并确认目录里是原始文件，否则原字节校验会不通过。

两个已知的采集盲区：`#US` 堆中 2 字节短串与 ≥128 字节长串会因前导长度前缀校验被跳过，这类串必须走 `data/zh_direct.json` 的 UTF-16 直替通道。
