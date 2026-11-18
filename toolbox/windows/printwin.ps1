Add-Type @"
using System;
using System.Text;
using System.Runtime.InteropServices;
public class PW {
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr p);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int Left, Top, Right, Bottom; }
  public delegate bool EnumProc(IntPtr h, IntPtr p);
}
"@
[PW]::SetProcessDPIAware() | Out-Null
Add-Type -AssemblyName System.Drawing

function Get-Windows([int]$procId) {
  $script:tp = $procId
  $script:list = @()
  $cb = [PW+EnumProc]{
    param($h,$p)
    $o = 0
    [PW]::GetWindowThreadProcessId($h, [ref]$o) | Out-Null
    if ($o -eq $script:tp -and [PW]::IsWindowVisible($h)) {
      $sb = New-Object System.Text.StringBuilder
      [PW]::GetWindowText($h, $sb, 256) | Out-Null
      $r = New-Object PW+RECT
      [PW]::GetWindowRect($h, [ref]$r) | Out-Null
      $script:list += [pscustomobject]@{ Handle=$h; Title=$sb.ToString(); W=($r.Right-$r.Left); H=($r.Bottom-$r.Top) }
    }
    return $true
  }
  [PW]::EnumWindows($cb, [IntPtr]::Zero) | Out-Null
  return $script:list
}

function Capture-PrintWindow([IntPtr]$h, [int]$w, [int]$ht, [string]$outFile) {
  $bmp = New-Object System.Drawing.Bitmap($w, $ht)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $hdc = $g.GetHdc()
  $ok = [PW]::PrintWindow($h, $hdc, 2)   # PW_RENDERFULLCONTENT
  $g.ReleaseHdc($hdc)
  $g.Dispose()
  $bmp.Save($outFile, [System.Drawing.Imaging.ImageFormat]::Png)
  $bmp.Dispose()
  return $ok
}
