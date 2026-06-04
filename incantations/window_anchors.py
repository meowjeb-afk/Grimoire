# File: incantations/window_anchors.py
import ctypes
import win32gui
import win32con

def pin_active_window():
    """Fetches the foreground window handle and locks it to the absolute top of the OS Z-index."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        title = win32gui.GetWindowText(hwnd)
        # SetWindowPos with HWND_TOPMOST anchors the window persistently
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return f"📌 Locked window: '{title}' to absolute top layer."
    return "❌ No active foreground window handle detected."

def unpin_active_window():
    """Releases the foreground window back to standard OS stacking behavior."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        title = win32gui.GetWindowText(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, 
                             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        return f"🔓 Released window: '{title}' back to standard layer rules."
    return "❌ No active foreground window handle detected."

def cast_window_opacity(opacity_val=180):
    """Applies a custom alpha channel transparency layer directly to the foreground window."""
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        # Pull current window styles and inject WS_EX_LAYERED bit flags
        wl = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, wl | win32con.WS_EX_LAYERED)
        # Apply layer alpha transparency attribute (0-255 scaling)
        ctypes.windll.user32.SetLayeredWindowAttributes(hwnd, 0, opacity_val, win32con.LWA_ALPHA)
        return f"🔮 Transmuted window opacity layer to value matrix: {opacity_val}/255"
    return "❌ Transparent focus shift failed."
