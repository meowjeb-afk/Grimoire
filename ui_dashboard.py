import sys
import json
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QComboBox
from PyQt6.QtCore import Qt

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Dashboard")
        self.setFixedSize(450, 350)
        
        # UI Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        
        # Title Accent
        header = QLabel("GRIMOIRE AUTOMATION PANEL")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #00ffcc; font-size: 18px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(header)
        
        # Checkboxes
        self.chk_startup = QCheckBox(" Cast on Windows Startup")
        self.chk_clipboard = QCheckBox(" Enable Clipboard Alchemy (Ctrl+Shift+H)")
        self.chk_clipboard.setChecked(True)
        layout.addWidget(self.chk_startup)
        layout.addWidget(self.chk_clipboard)
        
        # Buttons
        self.btn_apply = QPushButton("Apply Active Changes")
        self.btn_apply.clicked.connect(self.save_runes)
        layout.addWidget(self.btn_apply)
        
        # Window styling (Dark Gothic / Cyan Minimalist Sheet)
        self.setStyleSheet("""
            QMainWindow { background-color: #111116; }
            QLabel { color: #ffffff; font-family: 'Segoe UI'; }
            QCheckBox { color: #e0e0e0; font-size: 13px; }
            QPushButton { 
                background-color: #00ffcc; color: #111116; 
                font-weight: bold; border-radius: 5px; padding: 8px;
            }
            QPushButton:hover { background-color: #00ccaa; }
        """)
        
    def save_runes(self):
        """Saves current GUI selections directly back to the database config JSON."""
        data = {
            "run_on_startup": self.chk_startup.isChecked(),
            "clipboard_automation": self.chk_clipboard.isChecked()
        }
        with open("database/runes.json", "w") as f:
            json.dump(data, f, indent=2)
        print("💾 Configuration saved to database/runes.json")
