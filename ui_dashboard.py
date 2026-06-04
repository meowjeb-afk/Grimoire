import sys
import json
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QCheckBox, QTabWidget, 
    QLineEdit, QTextEdit, QComboBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from incantations import (
    file_alchemy, asset_summoner, workspace_stasis, 
    updater_scryer, purge_debloat, arcane_intel, 
    scry_search, void_shield, ecosystem_summoner, 
    image_matrix, system_monitors, deep_cleaner, 
    design_forge, layout_runes, browser_alchemy, desktop_dock
)

class ArcaneWorker(QThread):
    manifest_complete = pyqtSignal(str)
    def __init__(self, task_function, *args):
        super().__init__()
        self.task_function = task_function
        self.args = args
    def run(self):
        try:
            output = self.task_function(*self.args)
            self.manifest_complete.emit(str(output) if output else "Sequence completed smoothly.")
        except Exception as e:
            self.manifest_complete.emit(f"Sequence Error: {e}")

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.setFixedSize(700, 620)
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_image_tab()
        self.init_cleaner_tab()
        self.init_creative_tab()
        self.init_browser_tab()
        self.init_tuning_tab()
        self.apply_theme()

    def cast_asynchronously(self, target_function, *args):
        self.console_out.setText("🔮 Dispatched to background execution threads...")
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.console_out.setText)
        self.worker.start()

    def init_core_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        header = QLabel("SYSTEM AUTOMATION COEFFICIENTS")
        header.setStyleSheet("color: #00ffcc; font-size: 15px; font-weight: bold;")
        layout.addWidget(header)
        
        self.chk_startup = QCheckBox(" Initialize Grimoire on System Bootup")
        self.chk_clipboard = QCheckBox(" Clipboard Interception Active (Ctrl+Shift+H)")
        self.chk_clipboard.setChecked(True)
        layout.addWidget(self.chk_startup)
        layout.addWidget(self.chk_clipboard)
        
        btn_telemetry = QPushButton("Query Advanced Real-Time Hardware Telemetry")
        btn_telemetry.clicked.connect(lambda: self.cast_asynchronously(system_monitors.get_system_metrics))
        layout.addWidget(btn_telemetry)
        
        btn_sweep = QPushButton("Force kernel Memory RAM Sweeper Action")
        btn_sweep.clicked.connect(lambda: self.cast_asynchronously(system_monitors.sweep_system_ram))
        layout.addWidget(btn_sweep)
        
        self.tabs.addTab(page, "System Monitor")

    def init_alchemy_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Target Directory Path Folder Execution:"))
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads")
        layout.addWidget(self.txt_path)
        
        btn_run_sort = QPushButton("Execute File Alchemy Sorting")
        btn_run_sort.clicked.connect(lambda: self.cast_asynchronously(file_alchemy.transmute_folder, self.txt_path.text()))
        layout.addWidget(btn_run_sort)
        
        layout.addWidget(QLabel("Rapid Search File Query:"))
        self.txt_search = QLineEdit(".stl")
        layout.addWidget(self.txt_search)
        
        btn_scry_search = QPushButton("Run Rapid File Scry Search")
        btn_scry_search.clicked.connect(lambda: self.cast_asynchronously(scry_search.rapid_file_scry, self.txt_search.text()))
        layout.addWidget(btn_scry_search)
        self.tabs.addTab(page, "File Alchemy")

    def init_image_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Target Visual Asset Image Path:"))
        self.txt_img_path = QLineEdit(r"C:\Users\Public\Downloads\asset.png")
        layout.addWidget(self.txt_img_path)
        
        btn_bg = QPushButton("Erase Image Background (Produce Transparent Alpha PNG)")
        btn_bg.clicked.connect(lambda: self.cast_asynchronously(image_matrix.erase_background, self.txt_img_path.text()))
        layout.addWidget(btn_bg)
        
        btn_scale = QPushButton("Execute AI Lanczos Remaster & 2x Detail Upscale")
        btn_scale.clicked.connect(lambda: self.cast_asynchronously(image_matrix.remaster_and_upscale, self.txt_img_path.text(), 2))
        layout.addWidget(btn_scale)
        
        conv_layout = QHBoxLayout()
        conv_layout.addWidget(QLabel("Convert Asset Matrix to:"))
        self.cmb_format = QComboBox()
        self.cmb_format.addItems(["PNG", "JPEG", "WEBP", "ICO"])
        conv_layout.addWidget(self.cmb_format)
        btn_convert = QPushButton("Cast Format Conversion")
        btn_convert.clicked.connect(lambda: self.cast_asynchronously(image_matrix.convert_format, self.txt_img_path.text(), self.cmb_format.currentText()))
        conv_layout.addWidget(btn_convert)
        layout.addLayout(conv_layout)
        self.tabs.addTab(page, "Visual Alchemy")

    def init_cleaner_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        header = QLabel("DEEP OS PURGE & MAINTENANCE VECTORS")
        header.setStyleSheet("color: #ff007f; font-weight: bold;")
        layout.addWidget(header)
        
        btn_temp = QPushButton("Scrub Temp Vaults & Application Cache Residue")
        btn_temp.clicked.connect(lambda: self.cast_asynchronously(deep_cleaner.scrub_temp_vaults))
        layout.addWidget(btn_temp)
        
        btn_reg = QPushButton("Scan Registry shortcuts and Fix Missing Link Matrix Keys")
        btn_reg.clicked.connect(lambda: self.cast_asynchronously(deep_cleaner.clear_broken_registry_keys))
        layout.addWidget(btn_reg)
        
        layout.addWidget(QLabel("Aggressive Application Forced Uninstaller Tool:"))
        self.txt_uninstaller = QLineEdit("BloatedAppName")
        layout.addWidget(self.txt_uninstaller)
        btn_uninstall = QPushButton("Evict App and Purge Leftover Folders")
        btn_uninstall.clicked.connect(lambda: self.cast_asynchronously(deep_cleaner.execute_uninstaller, self.txt_uninstaller.text()))
        layout.addWidget(btn_uninstall)
        self.tabs.addTab(page, "Deep Cleaner")

    def init_creative_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        btn_palette = QPushButton("Generate Hex Color Palette (Based on Core Theme Values)")
        btn_palette.clicked.connect(lambda: self.cast_asynchronously(design_forge.generate_palette))
        layout.addWidget(btn_palette)
        
        btn_tex = QPushButton("Forge Procedural 256x256 Seamless Background Noise Texture")
        btn_tex.clicked.connect(lambda: self.cast_asynchronously(design_forge.craft_procedural_texture))
        layout.addWidget(btn_tex)
        
        btn_fav = QPushButton("Convert Target Asset Image Pathway Into production Multi-Size Favicon")
        btn_fav.clicked.connect(lambda: self.cast_asynchronously(design_forge.build_favicon, self.txt_img_path.text()))
        layout.addWidget(btn_fav)
        
        btn_fonts = QPushButton("Catalog Installed System Fonts")
        btn_fonts.clicked.connect(lambda: self.cast_asynchronously(layout_runes.scry_installed_fonts))
        layout.addWidget(btn_fonts)
        
        paper_layout = QHBoxLayout()
        paper_layout.addWidget(QLabel("Lookup Blueprint Dimensions Sheet:"))
        self.cmb_paper = QComboBox()
        self.cmb_paper.addItems(["A4", "A3", "A5", "Letter"])
        paper_layout.addWidget(self.cmb_paper)
        btn_paper = QPushButton("Get Sizing Guides")
        btn_paper.clicked.connect(lambda: self.cast_asynchronously(layout_runes.get_paper_spec, self.cmb_paper.currentText()))
        paper_layout.addWidget(btn_paper)
        layout.addLayout(paper_layout)
        
        self.tabs.addTab(page, "Design Forge")

    def init_browser_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("Global Browser Userscripts Automation Harvester Engine:"))
        self.txt_script = QLineEdit("Adblock Core")
        layout.addWidget(self.txt_script)
        
        btn_script = QPushButton("Search Open Web Repositories for Userscript Match")
        btn_script.clicked.connect(lambda: self.cast_asynchronously(browser_alchemy.search_userscripts, self.txt_script.text()))
        layout.addWidget(btn_script)
        self.tabs.addTab(page, "Browser Alchemy")

    def init_tuning_tab(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        btn_summon = QPushButton("🚀 Summon Entire Digital Workspace Ecosystem")
        btn_summon.clicked.connect(lambda: self.cast_asynchronously(ecosystem_summoner.summon_bundle))
        layout.addWidget(btn_summon)
        
        btn_dock = QPushButton("Spawn Floating SparkleDock Desktop Shortcut Bar Overlay")
        btn_dock.clicked.connect(lambda: self.cast_asynchronously(desktop_dock.summon_sparkle_dock))
        layout.addWidget(btn_dock)
        
        debloat_layout = QHBoxLayout()
        btn_telemetry = QPushButton("Banish Telemetry")
        btn_bloat = QPushButton("Purge Windows Bloat")
        debloat_layout.addWidget(btn_telemetry)
        debloat_layout.addWidget(btn_bloat)
        layout.addLayout(debloat_layout)
        
        shield_layout = QHBoxLayout()
        btn_shield_on = QPushButton("Raise Void Shield")
        btn_shield_off = QPushButton("Lower Void Shield")
        shield_layout.addWidget(btn_shield_on)
        shield_layout.addWidget(btn_shield_off)
        layout.addLayout(shield_layout)
        
        self.tabs.addTab(page, "Arcane Tuning")

    def apply_theme(self):
        # Master Console Log Module Placement Inside Interface Base Floor Frame Layout
        central_widget = self.centralWidget()
        master_layout = QVBoxLayout()
        master_layout.addWidget(self.tabs)
        
        master_layout.addWidget(QLabel("🔮 GRIMOIRE EXECUTION MATRIX LOG OUTPUT:"))
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        self.console_out.setFixedHeight(120)
        master_layout.addWidget(self.console_out)
        
        container = QWidget()
        container.setLayout(master_layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #0b090e; }
            QTabWidget::panel { background-color: #0c0a0f; border: 1px solid #1a1624; border-radius: 5px; }
            QTabBar::tab { background: #131017; color: #5c5566; padding: 8px 12px; font-weight: bold; font-family: 'Segoe UI'; font-size: 11px; border-top-left-radius: 4px; border-top-right-radius: 4px; }
            QTabBar::tab:selected { background: #0c0a0f; color: #00ffcc; border-bottom: 2px solid #00ffcc; }
            QLabel { color: #cfcad6; font-family: 'Segoe UI'; font-size: 12px; }
            QCheckBox { color: #b1a9b8; font-family: 'Segoe UI'; }
            QComboBox { background-color: #141119; color: white; border: 1px solid #282233; border-radius: 4px; padding: 3px; }
            QLineEdit { background-color: #141119; color: #00ffcc; border: 1px solid #282233; border-radius: 4px; padding: 4px; font-family: 'Consolas'; }
            QTextEdit { background-color: #050406; color: #00ffcc; border: 1px solid #1a1624; font-family: 'Consolas'; font-size: 11px; border-radius: 4px; }
            QPushButton { background-color: #15121a; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; border-radius: 4px; padding: 6px; font-family: 'Segoe UI'; }
            QPushButton:hover { background-color: #00ffcc; color: #0c0a0f; }
        """)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())
