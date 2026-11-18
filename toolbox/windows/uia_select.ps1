param([int]$ProcId,[int]$Idx,[string]$Out)
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes, System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class W3 { [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint f);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
 [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left,Top,Right,Bottom; } }
"@
[W3]::SetProcessDPIAware() | Out-Null
$h=(Get-Process -Id $ProcId).MainWindowHandle
$root=[System.Windows.Automation.AutomationElement]::FromHandle($h)
$c=New-Object System.Windows.Automation.PropertyCondition([System.Windows.Automation.AutomationElement]::ControlTypeProperty,[System.Windows.Automation.ControlType]::TreeItem)
$it=$root.FindAll([System.Windows.Automation.TreeScope]::Descendants,$c)
$el=$it.Item($Idx)
$pats=$el.GetSupportedPatterns() | ForEach-Object { $_.ProgrammaticName }
"patterns: $($pats -join ',')"
try{ ($el.GetCurrentPattern([System.Windows.Automation.SelectionItemPattern]::Pattern)).Select(); "selected ok" } catch { "select err: $_" }
Start-Sleep -Seconds 3
$r=New-Object W3+RECT; [W3]::GetWindowRect($h,[ref]$r)|Out-Null
$w=$r.Right-$r.Left; $ht=$r.Bottom-$r.Top
$b=New-Object System.Drawing.Bitmap($w,$ht); $g=[System.Drawing.Graphics]::FromImage($b); $hdc=$g.GetHdc()
[W3]::PrintWindow($h,$hdc,2)|Out-Null; $g.ReleaseHdc($hdc); $g.Dispose()
$b.Save($Out,[System.Drawing.Imaging.ImageFormat]::Png); $b.Dispose()
"saved $Out"
