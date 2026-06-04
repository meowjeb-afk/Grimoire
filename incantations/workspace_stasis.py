import json
import win32gui
import win32process
import psutil

def get_active_window_details():
    """Reads handle arrays across active running windows."""
    windows_snapshot = []
    
    def win_enum_callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title:
                # Read bounding coordinates
                left, top, right, bottom = win32gui.GetWindowRect(hwnd)
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                
                try:
                    proc = psutil.Process(pid)
                    exe_path = proc.exe()
                    windows_snapshot.append({
                        "title": title,
                        "exe": exe_path,
                        "coords": [left, top, right - left, bottom - top]
                    })
                except Exception:
                    pass
                    
    win32gui.EnumWindows(win_enum_callback, None)
    
    # Commit details to local config
    try:
        with open("database/runes.json", "r") as f:
            config = json.load(f)
        
        config["saved_workspace_windows"] = windows_snapshot
        
        with open("database/runes.json", "w") as f:
            json.dump(config, f, indent=2)
        print("💾 Workspace snapshot sealed in runes.json")
    except Exception as e:
        print(f"Error preserving workspace stasis: {e}")
