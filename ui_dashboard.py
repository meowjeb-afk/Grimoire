import sys
import json
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox, QTabWidget, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt
from incantations import file_alchemy, asset_summoner, workspace_stasis, updater_scryer, purge_debloat

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Dashboard")
        self.setFixedSize(550, 450)
        
        # Core Tabs Architecture
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_tuning_tab() # Added Tuning Layer
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

    def init_tuning_tab(self):
        """NEW PANEL: Controls system maintenance, software scrying, and debloating routines."""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(10)
        
        layout.addWidget(QLabel("System Scryer Output Status:"))
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        self.console_out.setPlaceholderText("Scan outputs will manifest here...")
        layout.addWidget(self.console_out)
        
        # Action Grid Layout
        btn_layout = QHBoxLayout()
        btn_scan = QPushButton("Scan for App Updates")
        btn_update = QPushButton("Cast Global Upgrades")
        btn_layout.addWidget(btn_scan)
        btn_layout.addWidget(btn_update)
        layout.addLayout(btn_layout)
        
        debloat_layout = QHBoxLayout()
        btn_telemetry = QPushButton("Banish Telemetry")
        btn_bloat = QPushButton("Purge Bloatware")
        debloat_layout.addWidget(btn_telemetry)
        debloat_layout.addWidget(btn_bloat)
        layout.addLayout(debloat_layout)
        
        # UI Event Routing Connections
        btn_scan.clicked.connect(lambda: self.console_out.setText(updater_scryer.scan_for_updates()))
        btn_update.clicked.connect(lambda: self.console_out.setText(updater_scryer.cast_all_upgrades()))
        btn_telemetry.clicked.connect(lambda: self.console_out.setText(purge_debloat.banish_telemetry()))
        btn_bloat.clicked.connect(lambda: self.console_out.setText(purge_debloat.purge_bloatware()))
        
        self.tabs.addTab(page, "Arcane Tuning")

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
            QTextEdit { background-color: #1c1c24; color: #00ffcc; border: 1px solid #333344; font-family: 'Consolas'; font-size: 12px; }
            QPushButton { background-color: #00ffcc; color: #111116; font-weight: bold; border-radius: 5px; padding: 8px; }
            QPushButton:hover { background-color: #00ccaa; }
        """)
