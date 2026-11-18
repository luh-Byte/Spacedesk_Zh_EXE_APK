# -*- coding: utf-8 -*-
"""Fill the missing Simplified-Chinese resources of the spacedesk Android app.

Only user-visible text is translated. Library-internal values, preference keys,
URLs, SVG path data and motion specs are deliberately left alone so they keep
falling back to English.
"""
import os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SD_DIR = os.environ.get('SPACEDESK_DIR', r'C:\Program Files\spacedesk')
import os, re

DEC = os.path.join(ROOT, 'android', 'decoded')
ZH_DIR = os.path.join(DEC, "res", "values-zh-rCN")

# key -> Chinese value.  \n is written as a literal backslash-n escape.
T = {
    "CDS": "未能检测到任何主控端电脑",
    "CDSButtonDiscoveryOff": "点击 + 按钮手动连接",
    "a_google_play_billing_service_error_has_occurred":
        "\"出现了 Google Play 结算服务错误。\\n"
        "请确认 spacedesk 安卓版应用是从官方 Google Play 商店安装的。\\n"
        "请确认已安装最新版 Google Play 应用。\\n"
        "请确认已安装最新版 Google Play 服务。\\n"
        "请确认网络连接稳定。\"",
    "action_about": "关于",
    "action_contact_support": "技术支持",
    "action_display_audio": "音频",
    "action_display_disconnect": "断开连接",
    "action_display_max": "最大化",
    "action_display_min": "最小化",
    "action_display_osk": "键盘",
    "action_input_devices": "输入设备",
    "action_purchase_license": "授权",
    "action_settings": "设置",
    "action_view_manual": "使用手册",
    "activity_display_label_display_off": "屏幕已关闭",
    "activity_licensed_devices": "并发访问授权 (CAL) 选项",
    "annoy_bubble_text": "spacedesk — 仅供非商业用途免费使用！",
    "app_website_error_browser_missing": "无法打开浏览器：请检查设备上是否已安装浏览器。",
    "before_connecting_usb_cable_enable_usb_cable_android_option_in_spacedesk_driver_console_on_windows_primary_machine":
        "连接 USB 线缆前，请先在 Windows 主控端电脑的 spacedesk 驱动控制台中启用“USB 安卓线缆”选项。",
    "billing_error": "结算错误",
    "chkLanWifiTitle": "局域网 / WiFi",
    "chkWiFiDirectTitle": "WiFi 直连",
    "chk_show_password": "显示密码",
    "commercial_business_license": "商业授权",
    "commercial_business_price_for_each_android_device":
        "商业授权（每台安卓设备 &lt;price>）",
    "consider_switching_to_software_encoding": "建议在设置中改用软件编码。",
    "could_not_purchase_this_item_please_check_the_purchase_state":
        "无法购买此项目，请检查购买状态！",
    "description_commercial_business_license1":
        "&lt;price>，用于任意 spacedesk 主控端电脑与当前 Google Play 账号下的一台安卓设备之间的一次并发连接。",
    "description_commercial_business_license2":
        "功能与免费版相同，购买前请充分测试！",
    "disconnected_by_server": "\"\\n服务器已断开连接：\\n\\n\"",
    "discoveryConnectionText": "\"连接：\"",
    "dlgDisconnectNegBtn": "取消",
    "dlgDisconnectPosBtn": "确定",
    "dlgDisconnectText": "确定要返回主菜单吗？",
    "dlgDisconnectTitle": "正在退出投屏",
    "dlgDisplayH264DecodeFailedText":
        "\"硬件 H264 解码器解码出错。\\n"
        "建议在设置中从硬件编码改为软件编码。\\n"
        "当前会话将被断开。\"",
    "dlgDisplayH264Failed": "硬件 H264 解码器错误",
    "dlgDisplayH264InitFailedText":
        "\"硬件 H264 解码器初始化出错。\\n"
        "建议在设置中从硬件编码改为软件编码。\\n"
        "当前会话将被断开。\"",
    "dlgDisplayLicensingNavigateText": "当前会话将被断开。",
    "dlgDisplayLicensingNavigateTitle": "正在前往授权页面",
    "dlgDisplaySettingsNavigateTitle": "正在前往设置",
    "dlgInitialInfoBtn": "确定",
    "dlgInitialInfoCheckboxText": "不再显示此提示",
    "dlgInitialInfoPosButton": "确定",
    "dlgInitialInfoText":
        "\"此 spacedesk 安卓版应用只能连接到 spacedesk Windows 驱动。\\n\\n"
        "硬件加速需要 spacedesk Windows 驱动版本不低于 2.2.23。\\n\\n"
        "请从以下地址下载最新 Windows 驱动：https://www.spacedesk.net\\n\\n"
        "帮助与发行说明：https://www.spacedesk.net/documentation\"",
    "dlgInitialInfoTitle": "重要提示：",
    "dlgMsgQuitDisplaySession": "确定要退出 spacedesk 投屏会话吗？",
    "dlgProgressCancelNegBtn": "取消",
    "dlgProgressCanceledToastText": "已中止",
    "dlgTextServerRestrictionPen":
        "\"当前 Windows 电脑上的 spacedesk 驱动不支持手写笔功能。\\n"
        "请从 www.spacedesk.net 下载最新版 spacedesk 驱动！\"",
    "dlgTitleServerRestrictionMain": "服务器端不支持该功能",
    "dlg_SoftKBInput_PosBtn": "确定",
    "dlg_SoftKBInput_doNotShowAgain": "不再显示此提示",
    "dlg_add_ip_btn_neg": "取消",
    "dlg_add_ip_btn_pos": "添加",
    "dlg_add_ip_btn_pos_discovery_off": "连接",
    "dlg_add_ip_empty_list_text": "列表为空",
    "dlg_add_ip_text": "请输入主控端电脑的 IP 地址：",
    "dlg_add_ip_text_recent": "最近使用：",
    "dlg_btn_connect": "连接",
    "dlg_text_please_enter_the_password_for": "\"\\n请输入以下连接的密码：\"",
    "dlg_title_password_input": "输入密码",
    "do_you_like_spacedesk": "喜欢 spacedesk 吗？",
    "encrypted_connection_needs_business_license": "加密连接需要商业授权",
    "error_a11y_label": "错误：无效",
    "error_unspecified_on_server_side": "服务器端出现未指明错误",
    "for_purchase_description": "\"：\"",
    "fps": "\"帧率：\"",
    "free": "免费版",
    "graceful_disconnect_by_server": "服务器已正常断开连接",
    "h264_encoder_encoding_failed_on_server_side": "服务器端 H264 编码器编码失败",
    "h264_encoder_initialization_failed_on_server_side": "服务器端 H264 编码器初始化失败",
    "hostNameValidationText": "正在校验主机名…",
    "hostname": "连接到主控端电脑（服务器）",
    "hostnameDiscoveryOff": "“发现”已关闭 — 请勾选“发现”复选框以启用自动发现",
    "inconsistent_licensing": "授权不一致",
    "inconsistent_licensing_detected":
        "\"检测到授权不一致。\\n"
        "授权只能按顺序购买。\\n"
        "请查看“附加并发连接”按钮了解更多信息。\\n"
        "缺失的授权以红色箭头标示，购买后授权才能一致。\"",
    "ipValidationText": "正在校验 IP…",
    "ivInfoDlgText":
        "\"请点击已发现的主控端电脑服务器地址以进行连接。\\n\\n"
        "如果看不到所需的服务器，请点击信息按钮左侧的 + 按钮手动输入 IP 地址。\"",
    "ivInfoDlgTextDiscoveryOff":
        "\"请点击下方按钮输入主控端电脑的 IP 地址。\\n"
        "由于“发现”设置为关闭，无法自动发现任何主控端电脑！\"",
    "ivInfoDlgTitle": "提示",
    "license_description": "授权说明",
    "license_option": "授权",
    "license_status_of_device": "已签发授权：",
    "licensed_user": "授权给",
    "licensing_text_after_annoy_bubble": "可在主菜单的“授权”栏目中查看授权选项。",
    "manuallyAddingIpText": "\"\\n手动添加 IP：\"",
    "material_slider_range_end": "范围上限",
    "material_slider_range_start": "范围下限",
    "material_slider_value": "数值",
    "msgBoxDisconnectedMainMessage": "\"\\n服务器断开连接错误\\n\\n错误代码：\"",
    "msgBoxDisconnectedManuallyTitleDisconnected": "已手动断开",
    "msgBoxDisconnectedTextConFailure": "连接失败",
    "msgBoxDisconnectedTextConnectedTime": "\"\\n\\n已连接时长：\"",
    "msgBoxDisconnectedTextConnectionFailed": "连接失败！",
    "msgBoxDisconnectedTextErrorInfo": "\"\\n\\n错误信息：\"",
    "msgBoxDisconnectedTextUnableToConnect": "无法连接！",
    "msgBoxDisconnectedTitleDisconnected": "已断开",
    "mtrl_checkbox_state_description_checked": "已勾选",
    "mtrl_checkbox_state_description_indeterminate": "部分勾选",
    "mtrl_checkbox_state_description_unchecked": "未勾选",
    "mvcViewTextAutoConnectingTo": "正在自动连接到 %1$s",
    "mvcViewTextConnectingTo": "\"\\n正在连接到 \"",
    "mvcViewTextDisconnectedReconnectingTo": "已断开 — 正在重新连接到 %1$s",
    "mvcViewTextDisconnectingFrom": "\"\\n正在断开与以下设备的连接：\"",
    "mvcViewTextDisplayOFF": "已连接 — 屏幕已关闭",
    "no_memory_on_server_side": "服务器端内存不足",
    "non_commercial_private_and_academic_free": "非商业个人与教育用途（免费）",
    "prefDlgResTxtAborted": "已中止",
    "prefDlgResValidationFailedTxtBigger": "\"\\n分辨率不能大于 \"",
    "prefDlgResValidationFailedTxtEmpty": "宽度/高度不能为空",
    "prefDlgResValidationFailedTxtMultiple": "宽度/高度必须是 2 的倍数",
    "prefDlgResValidationFailedTxtNative": "（原生）",
    "prefDlgResValidationFailedTxtNumeric": "宽度/高度输入的不是数字",
    "prefDlgResValidationFailedTxtSmaller": "\"\\n分辨率不能小于 \"",
    "prefDlgResValidationFailedTxtSmallestWin81": "\"\\n请勿在 Windows 8.1 上使用该分辨率 \"",
    "prefDlgResValidationTxtChangesApplied": "已应用更改",
    "pref_description_audio": "从服务器端采集音频输入",
    "pref_description_auto_connect": "应用启动时自动连接到服务器",
    "pref_description_auto_connect_hostname": "输入用于自动连接的主机名",
    "pref_description_auto_connect_ip": "输入用于自动连接的 IP 地址",
    "pref_description_autorotation": "主控端电脑屏幕随客户端设备旋转",
    "pref_description_display_menu":
        "显示浮动菜单按钮。注意：关闭屏幕菜单时无法使用屏幕键盘！",
    "pref_description_ktm_mouse": "将触摸屏输入发送到 Windows 主控端电脑（服务器）",
    "pref_description_ktm_stylus": "将手写笔输入发送到 Windows 主控端电脑（服务器）",
    "pref_enter_autoconnect_ip_message": "请输入 IP 地址",
    "pref_header_compression": "画质 / 性能",
    "pref_header_connection": "连接",
    "pref_header_extended": "扩展",
    "pref_header_menu": "屏幕菜单",
    "pref_header_pen": "手写笔",
    "pref_header_resolution": "分辨率",
    "pref_header_rotation": "旋转",
    "pref_header_touch": "触摸屏",
    "pref_image_quality": "图像质量",
    "pref_resolution_list_btn_neg": "取消",
    "pref_resolution_list_btn_pos": "应用",
    "pref_text_extended_con_watcher_polling_period": "设置连接超时的轮询周期（毫秒）",
    "pref_text_extended_con_watcher_timeout": "设置连接超时（毫秒）",
    "pref_text_extended_encryption": "选择加密连接类型",
    "pref_text_extended_encryption_client_identity": "设置加密连接的客户端标识",
    "pref_text_extended_encryption_key": "以十六进制设置加密连接的密钥",
    "pref_text_extended_timeout_auto_connect": "设置自动连接超时（毫秒）",
    "pref_text_extended_timeout_reconnect": "设置自动重连超时（毫秒）",
    "pref_text_fps_view_enable": "在会话中显示帧率",
    "pref_text_ktm_sonarpen": "配置 SonarPen 手写笔",
    "pref_title_audio": "音频",
    "pref_title_auto_connect": "自动连接",
    "pref_title_auto_connect_hostname": "自动连接到主机名：",
    "pref_title_auto_connect_ip": "自动连接到 IP 地址：",
    "pref_title_autoconnect_type": "自动连接到…",
    "pref_title_autorotation": "自动旋转",
    "pref_title_bmp_conf": "渲染色深",
    "pref_title_color_depth": "编码色深",
    "pref_title_compression_type": "编码类型",
    "pref_title_custom_res_choose": "选择自定义分辨率",
    "pref_title_display_menu": "屏幕菜单",
    "pref_title_extended_con_watcher_polling_period": "连接超时轮询周期",
    "pref_title_extended_con_watcher_timeout": "连接超时",
    "pref_title_extended_encryption": "连接加密",
    "pref_title_extended_encryption_client_identity": "加密连接客户端标识",
    "pref_title_extended_encryption_key": "加密连接密钥",
    "pref_title_extended_timeout_auto_connect": "自动连接超时",
    "pref_title_extended_timeout_reconnect": "自动重连超时",
    "pref_title_fps": "自定义帧率",
    "pref_title_fps_view_enable": "帧率显示",
    "pref_title_ktm_mouse": "启用触摸屏控制",
    "pref_title_ktm_sonarpen": "SonarPen 手写笔",
    "pref_title_ktm_stylus": "启用手写笔控制",
    "pref_title_touch_type": "触摸输入类型",
    "purchase_for_this_device": "立即购买",
    "purchase_license": "购买",
    "purchase_license_more_info": "更多信息",
    "purchase_license_payment_not_avail_yet": "暂不支持支付方式。",
    "purchasing_was_not_successful_billing_unavailable": "购买未成功 — 结算服务不可用",
    "purchasing_was_not_successful_internal_error": "购买未成功 — 内部错误",
    "purchasing_was_not_successful_purchase_cancelled": "购买未成功 — 购买已取消",
    "purchasing_was_not_successful_service_unavailable": "购买未成功 — 服务不可用",
    "searchview_clear_text_content_description": "清除文本",
    "searchview_navigation_content_description": "返回",
    "software_decoding_only": "该分辨率不支持硬件加速",
    "sonarPenGrantPermissionNeeded": "未授予相关权限，无法使用 SonarPen",
    "sonarPenPrefCalibrate": "校准 SonarPen",
    "sonarPenPrefCancel": "取消",
    "sonarPenPrefDisable": "禁用 SonarPen",
    "sonarPenPrefEnable": "启用 SonarPen",
    "sonarPenPrefMainText":
        "spacedesk 应用支持 SonarPen 手写笔。可在下方选项中启用/禁用它、访问 SonarPen 官网或校准 SonarPen。",
    "sonarPenPrefMainTextStatusDisabled": "SonarPen 状态 — 已禁用",
    "sonarPenPrefMainTextStatusEnabled": "SonarPen 状态 — 已启用",
    "sonarPenPrefMainTextStatusEnabledCalibrated": "已校准",
    "sonarPenPrefMainTextStatusEnabledNotCalibrated": "未校准",
    "sonarPenPrefPalmRejectionDisable": "关闭手掌误触",
    "sonarPenPrefPalmRejectionEnable": "开启手掌误触",
    "sonarPenPrefReCalibrate": "重新校准 SonarPen",
    "sonarPenPrefWebsite": "SonarPen 官网",
    "sonarPenToastSonarPenDisabled": "SonarPen 已禁用",
    "sonarPenToastSonarPenEnabled": "SonarPen 已启用",
    "spResFirstElement": "分辨率…",
    "status": "状态",
    "support_google_play_store": "想支持我们的开发团队吗？欢迎在 Google Play 商店留下评价。",
    "the_license_bundles_below_are_available_for_purchase_in_correct_sequence_only":
        "仅当同一 Google Play 账号下的多台设备需要同时访问任意 spacedesk 主控端电脑时，才需要下表的附加 CAL 授权包。授权只能按顺序购买。",
    "title_activity_input_devices": "输入设备",
    "title_activity_settings": "设置",
    "toastAutoConnectHostnameNeedsDiscoveryOn": "使用主机名自动连接前，请先开启“发现”功能",
    "toastInvalidIpText": "\"\\n无效 IP — \"",
    "toastLowMemory": "设备可用内存不足，请关闭其他应用以释放内存。",
    "toastSonarPenStatusConnected": "SonarPen 已连接",
    "toastSonarPenStatusDisconnected": "SonarPen 已断开",
    "toastSonarPenStatusNotConnected": "SonarPen 未连接",
    "toastTextDisplayDisconnected": "投屏已断开",
    "toastTxtAutoConHostnameDisabled": "因自动连接主机名为空，已停用自动连接",
    "toastTxtAutoConIpDisabled": "因自动连接 IP 为空，已停用自动连接",
    "toastTxtAutoConIpNotSaved": "自动连接 IP 未保存 — 请重试",
    "toastTxtAutoConIpSaved": "自动连接 IP 已保存",
    "toastTxtDisplayConnected": "投屏已连接",
    "toastTxtInvalidIp": "IP 无效",
    "toastTxtUnableToConnect": "无法连接",
    "toastWiFiDirectDiscoveryComingSoonMsg": "WiFi 直连发现功能即将推出…",
    "toast_extended_menu_enabled": "已启用扩展设置",
    "toast_invalid_password": "密码错误！",
    "toast_password_field_cannot_be_empty": "密码不能为空！",
    "tvDiscoveryTitle": "发现",
    "tvPrefResHint":
        "\"\\n标有 (*) 的分辨率与设备屏幕比例匹配，推荐使用。\"",
    "tvTitleViewerMain": "spacedesk 查看器",
    "txtToastCongestion": "网络带宽偏低，投屏可能不稳定",
    "txtToastUsbConnectionLost": "USB 会话连接已丢失…",
    "txtToastUsbConnectionNotPossible": "无法建立 USB 连接，正在关闭会话…",
    "txtToastUsbDetached": "USB 线缆已断开！",
    "txtToastUsbDetachedSession": "USB 线缆已断开！正在关闭会话…",
    "txtToastUsbPermissionDenied": "USB 权限被拒绝，正在关闭会话…",
    "unknown_connect_to_the_internet_for_validation": "未知（请联网后校验）",
    "unknown_reason_on_server_side": "服务器端原因未知",
    "unknown_user": "当前 Google Play 账号",
    "upgrade_seach_split_word": "升级",
    "usb_session_closed_by_server": "\"\\n服务器已关闭 USB 会话：\"",
    "use_usb_cable": "使用 USB 线缆",
}

ARRAYS = {
    "pref_autoconnect_type_titles": ["关闭", "IP 地址", "主机名"],
    "pref_bmp_conf_titles": ["16 位（RGB 565）", "24 位（RGB 888）"],
    "pref_color_depth_titles": [
        "色彩质量高、速度慢（YUV 4.4.4）",
        "色彩质量中、速度中（YUV 4.2.2）",
        "色彩质量低、速度快（YUV 4.2.0）",
    ],
    "pref_compression_type_titles": [
        "自动选择（软件 JPEG 或硬件 H264）",
        "软件编码 MJPEG（强制）",
        "硬件编码 H264（强制）",
    ],
    "pref_extended_encryption_type_titles": ["不加密", "TLS 1.2", "TLS 1.3"],
    "pref_fps_titles": ["30 FPS", "60 FPS", "90 FPS", "120 FPS"],
    "pref_touch_type_titles": ["触摸屏（绝对定位）", "触摸板（相对定位）"],
}

# ---------------------------------------------------------------- write strings
strings_path = os.path.join(ZH_DIR, "strings.xml")
text = open(strings_path, encoding="utf-8").read()

existing = set(re.findall(r'<string name="([^"]+)"', text))
added = 0
lines = []
for k, v in T.items():
    if k in existing:
        continue
    lines.append('    <string name="%s">%s</string>' % (k, v))
    added += 1

if lines:
    text = text.replace("</resources>", "\n".join(lines) + "\n</resources>")
open(strings_path, "w", encoding="utf-8", newline="\n").write(text)
print("strings added:", added, "already present:", len(existing))

# ---------------------------------------------------------------- write arrays
arrays_out = ['<?xml version="1.0" encoding="utf-8"?>', "<resources>"]
for name, items in ARRAYS.items():
    arrays_out.append('    <string-array name="%s">' % name)
    for it in items:
        arrays_out.append("        <item>%s</item>" % it)
    arrays_out.append("    </string-array>")
arrays_out.append("</resources>")
open(os.path.join(ZH_DIR, "arrays.xml"), "w", encoding="utf-8", newline="\n").write(
    "\n".join(arrays_out) + "\n")
print("arrays written:", len(ARRAYS))
