from django.http import HttpResponse


def index(request):
    return HttpResponse("""Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Import user32.dll for mouse clicks & key detection
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Mouse {
    [DllImport("user32.dll")]
    public static extern void mouse_event(uint dwFlags, uint dx, uint dy, uint dwData, int dwExtraInfo);

    [DllImport("user32.dll")]
    public static extern short GetAsyncKeyState(int vKey);
}
"@

# Mouse event constants
$MOUSEEVENTF_LEFTDOWN = 0x02
$MOUSEEVENTF_LEFTUP   = 0x04

# Virtual key codes
$VK_K     = 0x4B
$VK_J     = 0x4A
$VK_ESC   = 0x1B

$Clicking = $false

Write-Host "Press 'K' to START clicking, 'J' to STOP, 'Esc' to EXIT."

while ($true) {
    # If K pressed -> start clicking
    if ([Mouse]::GetAsyncKeyState($VK_K) -lt 0) {
        $Clicking = $true
        Start-Sleep -Milliseconds 200  # prevent rapid toggle
        Write-Host "Clicker ON"
    }

    # If J pressed -> stop clicking
    if ([Mouse]::GetAsyncKeyState($VK_J) -lt 0) {
        $Clicking = $false
        Start-Sleep -Milliseconds 200
        Write-Host "Clicker OFF"
    }

    # If Esc pressed -> exit
    if ([Mouse]::GetAsyncKeyState($VK_ESC) -lt 0) {
        break
    }

    # Perform clicks if active
    if ($Clicking) {
        [Mouse]::mouse_event($MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        [Mouse]::mouse_event($MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        Start-Sleep -Milliseconds 1  # click speed
    } else {
        Start-Sleep -Milliseconds 10
    }
}
""")