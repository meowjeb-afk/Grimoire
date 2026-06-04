import sys
import json
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QTabWidget, QLineEdit
from PyQt6.QtCore import Qt
from incantations import file_alchemy, asset_summoner, workspace_stasis

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Dashboard")
        self.setFixedSize(500, 400)
        
        # Core Tabs Architecture
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.init_core_tab()
        self.init_alchemy_tab()
        self.apply_theme()

    def init_core_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(15)
        
        header = QLabel("SYSTEM CONFIGURATION")
        header.setStyleSheet("color: #00ffcc; font-size: 16px; font-weight: bold;")
        layout.addWidget(header)
        
        self.chk_startup = QCheckBox(" Execute on Windows Startup")
        self.chk_clipboard = QCheckBox(" Clipboard Interception (Ctrl+Shift+H)")
        self.chk_clipboard.setChecked(True)
        self.chk_expansion = QCheckBox(" Real-Time Text Expansion")
        self.chk_expansion.setChecked(True)
        
        layout.addWidget(self.chk_startup)
        layout.addWidget(self.chk_clipboard)
        layout.addWidget(self.chk_expansion)
        
        btn_snap = QPushButton("Freeze Current Workspace Layout")
        btn_snap.clicked.connect(workspace_stasis.get_active_window_details)
        layout.addWidget(btn_snap)
        
        btn_save = QPushButton("Commit Settings")
        btn_save.clicked.connect(self.save_settings)
        layout.addWidget(btn_save)
        
        self.tabs.addTab(page, "Core Options")

    def init_alchemy_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("Target Directory Path:"))
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads")
        layout.addWidget(self.txt_path)
        
        btn_run_sort = QPushButton("Execute File Alchemy Sorting")
        btn_run_sort.clicked.connect(lambda: file_alchemy.transmute_folder(self.txt_path.text()))
        layout.addWidget(btn_run_sort)
        
        layout.addWidget(QLabel("Harvest Assets via Tag Query:"))
        self.txt_tag = QLineEdit("gothic")
        layout.addWidget(self.txt_tag)
        
        btn_harvest = QPushButton("Summon Vector Assets")
        btn_harvest.clicked.connect(lambda: asset_summoner.summon_assets(self.txt_tag.text()))
        layout.addWidget(btn_harvest)
        
        self.tabs.addTab(page, "Manual Alchemy")

    def save_settings(self):
        try:
            with open("database/runes.json", "r") as f:
                data = json.load(f)
        except Exception:
            data = {}

        data["run_on_startup"] = self.chk_startup.isChecked()
        data["clipboard_automation"] = self.chk_clipboard.isChecked()
        data["text_expansion"] = self.chk_expansion.isChecked()
        
        with open("database/runes.json", "w") as f:
            json.dump(data, f, indent=2)
        print("💾 State updated.")

    def apply_theme(self):
        self.setStyleSheet("""
            QMainWindow, QTabWidget::panel { background-color: #121216; }
            QTabBar::tab { background: #22222b; color: #888899; padding: 8px 16px; font-weight: bold; }
            QTabBar::tab:selected { background: #121216; color: #00ffcc; border-bottom: 2px solid #00ffcc; }
            QLabel { color: #ffffff; font-family: 'Segoe UI'; font-size: 13px; }
            QCheckBox { color: #e0e0e0; }
            QLineEdit { background-color: #1c1c24; color: white; border: 1px solid #333344; border-radius: 4px; padding: 4px; }
            QPushButton { background-color: #00ffcc; color: #111116; font-weight: bold; border-radius: 5px; padding: 8px; }
            QPushButton:hover { background-color: #00ccaa; }
        """)
