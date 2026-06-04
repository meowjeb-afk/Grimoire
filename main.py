import sys
import os
import ctypes
import threading
import json
from PIL import Image, ImageDraw
import pystray
from PyQt6.QtWidgets import QApplication

def enforce_admin_privileges():
    """Validates low-level security access, triggering UAC self-elevation triggers if needed."""
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        
    if not is_admin:
        print("🛡️ Insufficient operational access. Evoking Administrative Catalyst Elevation...")
        # Re-execute script under system admin credentials
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

# Enforce system privileges before loading graphics subroutines
enforce_admin_privileges()

from ui_dashboard import GrimoireMirror
from incantations import clipboard_magic, text_expansion

def create_tray_rune():
    image = Image.new('RGB', (64, 64), color=(12, 10, 15))
    draw = ImageDraw.Draw(image)
    draw.rectangle([18, 18, 46, 46], fill=(0, 255, 200))
    return image

def exit_gracefully(icon, item):
    icon.stop()
    os._exit(0)

def launch_hub():
    app = QApplication(sys.argv)
    mirror = GrimoireMirror()
    
    try:
        with open("database/runes.json", "r") as f:
            runes = json.load(f)
    except Exception:
        runes = {"clipboard_automation": True, "text_expansion": True}

    if runes.get("clipboard_automation", True):
        threading.Thread(target=clipboard_magic.summon_keyboard_listener, daemon=True).start()
    
    if runes.get("text_expansion", True):
        threading.Thread(target=text_expansion.register_expansions, daemon=True).start()
    
    menu = pystray.Menu(
        pystray.MenuItem('Open Grimoire Mirror', lambda: mirror.show()),
        pystray.MenuItem('Banish System (Quit)', exit_gracefully)
    )
    icon = pystray.Icon("Grimoire", create_tray_rune(), title="Grimoire Optimization Suite", menu=menu)
    threading.Thread(target=icon.run, daemon=True).start()
    
    mirror.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_hub()
