import ctypes
import time
from pathlib import Path

def change_windows_wallpaper(image_path):
    """Directly communicates with the Windows API to set the desktop wallpaper."""
    path = Path(image_path)
    if not path.exists():
        print("❌ Wallpaper path invalid.")
        return
    
    # SPI_SETDESKWALLPAPER = 0x0014
    ctypes.windll.user32.SystemParametersInfoW(0x0014, 0, str(path.absolute()), 3)
    print(f"🖼️ Wallpaper woven successfully: {path.name}")

def start_ambient_cycle(wallpaper_folder, check_interval_seconds=3600):
    """Background cycle that continually transitions ambient choices."""
    folder = Path(wallpaper_folder)
    if not folder.exists():
        return
        
    while True:
        wallpapers = [f for f in folder.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
        if wallpapers:
            for wp in wallpapers:
                change_windows_wallpaper(wp)
                time.sleep(check_interval_seconds)
