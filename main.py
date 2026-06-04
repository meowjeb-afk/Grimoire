import sys
import threading
import os
import json
from PIL import Image, ImageDraw
import pystray
from PyQt6.QtWidgets import QApplication
from ui_dashboard import GrimoireMirror
from incantations import clipboard_magic, text_expansion

def create_tray_rune():
    image = Image.new('RGB', (64, 64), color=(17, 17, 22))
    draw = ImageDraw.Draw(image)
    draw.rectangle([18, 18, 46, 46], fill=(0, 255, 200))
    return image

def exit_gracefully(icon, item):
    icon.stop()
    os._exit(0)

def launch_hub():
    app = QApplication(sys.argv)
    mirror = GrimoireMirror()
    
    # Check configurations to selectively boot modules
    try:
        with open("database/runes.json", "r") as f:
            runes = json.load(f)
    except Exception:
        runes = {"clipboard_automation": True, "text_expansion": True}

    # Thread Module 1: Clipboard Interceptor
    if runes.get("clipboard_automation", True):
        threading.Thread(target=clipboard_magic.summon_keyboard_listener, daemon=True).start()
    
    # Thread Module 2: Text Expansion Listener
    if runes.get("text_expansion", True):
        threading.Thread(target=text_expansion.register_expansions, daemon=True).start()
    
    # System Tray Hook Configuration
    menu = pystray.Menu(
        pystray.MenuItem('Open Grimoire Mirror', lambda: mirror.show()),
        pystray.MenuItem('Banish System (Quit)', exit_gracefully)
    )
    icon = pystray.Icon("Grimoire", create_tray_rune(), title="Grimoire Shell Extension", menu=menu)
    threading.Thread(target=icon.run, daemon=True).start()
    
    mirror.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_hub()
