import sys
import threading
import os
from PIL import Image, ImageDraw
import pystray
from PyQt6.QtWidgets import QApplication
from ui_dashboard import GrimoireMirror
from incantations import clipboard_magic

def create_tray_rune():
    """Generates a custom stylized box graphic dynamically for the Windows Tray icon."""
    image = Image.new('RGB', (64, 64), color=(17, 17, 22))
    draw = ImageDraw.Draw(image)
    draw.rectangle([18, 18, 46, 46], fill=(0, 255, 200)) # Glowing cyan core
    return image

def exit_gracefully(icon, item):
    icon.stop()
    os._exit(0)

def launch_hub():
    # 1. Initialize the GUI application layer
    app = QApplication(sys.argv)
    mirror = GrimoireMirror()
    
    # 2. Boot up the background keyboard automation listener thread
    threading.Thread(target=clipboard_magic.summon_keyboard_listener, daemon=True).start()
    
    # 3. Form the Windows System Tray menu mapping
    menu = pystray.Menu(
        pystray.MenuItem('Open Dashboard', lambda: mirror.show()),
        pystray.MenuItem('Banish (Quit)', exit_gracefully)
    )
    icon = pystray.Icon("Grimoire", create_tray_rune(), title="Grimoire Shell Extension", menu=menu)
    
    # Run Tray icon in its own thread so it does not block the main window loop
    threading.Thread(target=icon.run, daemon=True).start()
    
    mirror.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    launch_hub()
