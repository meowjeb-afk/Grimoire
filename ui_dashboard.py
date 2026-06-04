# File: ui_dashboard.py
import sys
import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QCheckBox, QTabWidget, 
    QLineEdit, QTextEdit, QComboBox, QFrame, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
from incantations import (
    file_alchemy, asset_summoner, workspace_stasis, 
    updater_scryer, purge_debloat, arcane_intel, 
    scry_search, void_shield, ecosystem_summoner, 
    image_matrix, system_monitors, deep_cleaner, 
    design_forge, layout_runes, browser_alchemy, desktop_dock,
    window_anchors, process_hunter, persistent_bans
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
        self.setFixedSize(920, 740) # Expanded canvas window boundaries for previews and sliders
        
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_image_tab()
        self.init_creative_nexus_tab() # NEW Heavy-Duty Creative Suite
        self.init_deployment_architect_tab() # NEW System Replicator Tools
        self.init_window_tab() 
        self.init_cleaner_tab()
        self.init_creative_tab()
        self.init_browser_tab()
        self.init_tuning_tab()
        self.apply_theme()

    def cast_asynchronously(self, target_function, *args):
        self.console_out.setText("🔮 Dispatched to background execution threads...")
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.display_output)
        self.worker.start()

    def display_output(self, text):
        self.console_out.setText(text)
        # Scan if output text points to a valid image file, and if so, render into preview bay
        if "C:\\Users\\Public\\" in text and (".png" in text or ".jpg" in text):
            for word in text.split():
                if os.path.exists(word) and word.endswith((".png", ".jpg")):
                    pixmap = QPixmap(word)
                    self.preview_window.setPixmap(pixmap.scaled(self.preview_window.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def create_card(self, title, pill_color="#00ffcc", text_color="#0c0a0f", fixed_width=None):
        card_frame = QFrame()
        card_frame.setObjectName("DashboardCard")
        if fixed_width: card_frame.setFixedWidth(fixed_width)
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(15, 15, 15, 15)
        card_layout.setSpacing(10)
        
        pill_header = QLabel(title)
        pill_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pill_header.setStyleSheet(f"background-color: {pill_color}; color: {text_color}; font-weight: bold; border-radius: 12px; padding: 6px 15px; font-size: 11px; text-transform: uppercase;")
        card_layout.addWidget(pill_header)
        return card_frame, card_layout

    def init_core_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        row_layout = QHBoxLayout()
        card_cfg, layout_cfg = self.create_card("Automation Coefficients", "#3a846e", "white")
        self.chk_startup = QCheckBox(" Initialize on System Bootup")
        self.chk_clipboard = QCheckBox(" Clipboard Interception Active")
        self.chk_clipboard.setChecked(True)
        layout_cfg.addWidget(self.chk_startup)
        layout_cfg.addWidget(self.chk_clipboard)
        row_layout.addWidget(card_cfg)
        
        card_act, layout_act = self.create_card("Telemetry Control", "#a13d2d", "white")
        btn_telemetry = QPushButton("Query Bare-Metal Metrics")
        btn_telemetry.clicked.connect(lambda: self.cast_asynchronously(system_monitors.get_system_metrics))
        btn_sweep = QPushButton("Force Memory RAM Sweep")
        btn_sweep.clicked.connect(lambda: self.cast_asynchronously(system_monitors.sweep_system_ram))
        layout_act.addWidget(btn_telemetry)
        layout_act.addWidget(btn_sweep)
        row_layout.addWidget(card_act)
        main_layout.addLayout(row_layout)
        self.tabs.addTab(page, "System Monitor")

    def init_alchemy_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_dir, layout_dir = self.create_card("Directory Sorting Vector", "#966a1c", "white")
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads")
        layout_dir.addWidget(self.txt_path)
        btn_run_sort = QPushButton("Execute File Alchemy Sorting")
        btn_run_sort.clicked.connect(lambda: self.cast_asynchronously(file_alchemy.transmute_folder, self.txt_path.text()))
        layout_dir.addWidget(btn_run_sort)
        main_layout.addWidget(card_dir)
        self.tabs.addTab(page, "File Alchemy")

    def init_image_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_img, layout_img = self.create_card("Visual Manipulation Chamber", "#3a846e", "white")
        self.txt_img_path = QLineEdit(r"C:\Users\Public\Grimoire_Procedural_Logo.png")
        layout_img.addWidget(self.txt_img_path)
        
        btn_bg = QPushButton("Erase Image Background (Alpha Transparent PNG)")
        btn_bg.clicked.connect(lambda: self.cast_asynchronously(image_matrix.erase_background, self.txt_img_path.text()))
        layout_img.addWidget(btn_bg)
        main_layout.addWidget(card_img)
        self.tabs.addTab(page, "Visual Alchemy")

    def init_creative_nexus_tab(self):
        """NEW CORE MATRIX PANEL: Houses the requested Giphy, Pixel, Toy, Pattern, and Offline AI parameters."""
        page = QWidget()
        main_layout = QVBoxLayout(page)
        row_layout = QHBoxLayout()
        
        # Left Control Column
        left_col = QVBoxLayout()
        
        # Giphy and Sticker Packaging Card
        card_gif, layout_gif = self.create_card("Giphy & Sticker Deployment Suite", "#143a96", "white")
        self.txt_gif_query = QLineEdit("cute gaming asset")
        layout_gif.addWidget(self.txt_gif_query)
        btn_find_gif = QPushButton("🔍 Scry Giphy Streams")
        btn_find_gif.clicked.connect(lambda: self.cast_asynchronously(image_matrix.search_giphy, self.txt_gif_query.text()))
        layout_gif.addWidget(btn_find_gif)
        
        self.cmb_sticker_plat = QComboBox()
        self.cmb_sticker_plat.addItems(["discord", "whatsapp"])
        layout_gif.addWidget(self.cmb_sticker_plat)
        btn_pack_sticker = QPushButton("🏷️ Compile Image into Sticker Package")
        btn_pack_sticker.clicked.connect(lambda: self.cast_asynchronously(image_matrix.format_sticker_package, self.txt_img_path.text(), self.cmb_sticker_plat.currentText()))
        layout_gif.addWidget(btn_pack_sticker)
        left_col.addWidget(card_gif)
        
        # Sliders Card (Pixelation & Enhancer parameters)
        card_sliders, layout_sliders = self.create_card("Pixelation & Enhancer Modulations", "#966a1c", "white")
        layout_sliders.addWidget(QLabel("Retro Pixelation Size Matrix Floor:"))
        self.slider_pixel = QSlider(Qt.Orientation.Horizontal)
        self.slider_pixel.setRange(2, 32)
        self.slider_pixel.setValue(8)
        layout_sliders.addWidget(self.slider_pixel)
        
        btn_pixel_art = QPushButton("👾 Transmute Image to Pixel Art")
        btn_pixel_art.clicked.connect(lambda: self.cast_asynchronously(image_matrix.apply_pixel_art_slider, self.txt_img_path.text(), self.slider_pixel.value()))
        layout_sliders.addWidget(btn_pixel_art)
        
        btn_enhance = QPushButton("✨ Execute Micro-Contrast Pixel Enhancer")
        btn_enhance.clicked.connect(lambda: self.cast_asynchronously(image_matrix.enhance_pixel_density, self.txt_img_path.text()))
        layout_sliders.addWidget(btn_enhance)
        left_col.addWidget(card_sliders)
        row_layout.addLayout(left_col)
        
        # Right Control Column
        right_col = QVBoxLayout()
        
        # Offline AI & Transmutations Card
        card_ai, layout_ai = self.create_card("Offline Engine & Toy Fab Chamber", "#a13d2d", "white")
        self.txt_ai_prompt = QLineEdit("adorable plush game item")
        layout_ai.addWidget(self.txt_ai_prompt)
        
        btn_offline_ai = QPushButton("🎨 Execute Offline AI Render (No Limits / WebUI Port 7860)")
        btn_offline_ai.clicked.connect(lambda: self.cast_asynchronously(asset_summoner.local_offline_ai_forge, self.txt_ai_prompt.text()))
        layout_ai.addWidget(btn_offline_ai)
        
        btn_sketch = QPushButton("📝 Sketch-to-Life Render (Img2Img Engine Map)")
        btn_sketch.clicked.connect(lambda: self.cast_asynchronously(asset_summoner.local_offline_ai_forge, "realistic master rendering", "", 20, 7.0, 512, 512, self.txt_img_path.text()))
        layout_ai.addWidget(btn_sketch)
        
        btn_plush = QPushButton("🧸 Transmute Target Image into Adorable Plush Toy")
        btn_plush.clicked.connect(lambda: self.cast_asynchronously(image_matrix.transmute_to_plush_or_crochet, self.txt_img_path.text(), "plush"))
        layout_ai.addWidget(btn_plush)
        
        btn_crochet = QPushButton("🧶 Convert Image into Crochet/Knitting Pattern Grid")
        btn_crochet.clicked.connect(lambda: self.cast_asynchronously(image_matrix.transmute_to_plush_or_crochet, self.txt_img_path.text(), "crochet"))
        layout_ai.addWidget(btn_crochet)
        right_col.addWidget(card_ai)
        
        row_layout.addLayout(right_col)
        main_layout.addLayout(row_layout)
        self.tabs.addTab(page, "Creative Nexus")

    def init_deployment_architect_tab(self):
        """NEW CONFIGURATION PANEL: Builds the automated program replica array and system anchors."""
        page = QWidget()
        main_layout = QVBoxLayout(page)
        
        card_rep, layout_rep = self.create_card("OS Deployment Replicator & Backup Anchor", "#3a846e", "white")
        btn_restore = QPushButton("🛡️ Generate System Restore Checkpoint Anchor")
        btn_restore.clicked.connect(lambda: self.cast_asynchronously(deep_cleaner.drop_system_restore_anchor))
        layout_rep.addWidget(btn_restore)
        
        btn_export_apps = QPushButton("📋 Export System Software Configuration Blueprint List")
        btn_export_apps.clicked.connect(lambda: self.cast_asynchronously(deep_cleaner.export_installed_software_replica))
        layout_rep.addWidget(btn_export_apps)
        
        layout_rep.addWidget(QLabel("Deployment To-Do Automation Array (Silent Bulk Background Installer Box):"))
        self.txt_todo_replica = QTextEdit("[ ] REINSTALL: GoogleChrome\n[ ] REINSTALL: VLC\n[ ] REINSTALL: Steam")
        layout_rep.addWidget(self.txt_todo_replica)
        
        btn_run_bulk = QPushButton("🚀 Run Automated Silent Bulk Installer Array (Compile to Pseudo-EXE Layout)")
        btn_run_bulk.clicked.connect(lambda: self.cast_asynchronously(deep_cleaner.execute_silent_bulk_installer_exe, self.txt_todo_replica.toPlainText()))
        layout_rep.addWidget(btn_run_bulk)
        
        main_layout.addWidget(card_rep)
        self.tabs.addTab(page, "Deployment Architect")

    def init_window_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_win, layout_win = self.create_card("Active Frame Overlay Controls", "#a13d2d", "white")
        btn_pin = QPushButton("Pin Current Window Frame to 'Always On Top'")
        btn_pin.clicked.connect(lambda: self.cast_asynchronously(window_anchors.pin_active_window))
        layout_win.addWidget(btn_pin)
        main_layout.addWidget(card_win)
        self.tabs.addTab(page, "Window Anchors")

    def init_cleaner_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_scrub, layout_scrub = self.create_card("Debris & Handle Scrubbers", "#143a96", "white")
        self.txt_kill = QLineEdit("Application.exe")
        layout_scrub.addWidget(self.txt_kill)
        btn_kill = QPushButton("🎯 Force Kill Stuck Process Tree")
        btn_kill.clicked.connect(lambda: self.cast_asynchronously(process_hunter.scavenge_and_kill_process, self.txt_kill.text()))
        layout_scrub.addWidget(btn_kill)
        main_layout.addWidget(card_scrub)
        self.tabs.addTab(page, "Deep Cleaner")

    def init_creative_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_forge, layout_forge = self.create_card("Asset Prompt & Logo Engineering Chambers", "#3a846e", "white")
        
        # Sizing Logo Sliders
        layout_forge.addWidget(QLabel("Vector Logo Corner Border Radiusing:"))
        self.slider_radius = QSlider(Qt.Orientation.Horizontal)
        self.slider_radius.setRange(0, 50)
        self.slider_radius.setValue(20)
        layout_forge.addWidget(self.slider_radius)
        
        self.txt_logo_text = QLineEdit("MY GAME LOGO")
        layout_forge.addWidget(self.txt_logo_text)
        
        btn_draw_logo = QPushButton("🎨 Construct Slider-Driven Procedural Graphic Template Logo")
        btn_draw_logo.clicked.connect(lambda: self.cast_asynchronously(layout_runes.draw_procedural_logo, self.txt_logo_text.text(), self.slider_radius.value()))
        layout_forge.addWidget(btn_draw_logo)
        
        # Prompt Modulator
        layout_forge.addWidget(QLabel("Base Game Asset Concept Idea Input:"))
        self.txt_game_idea = QLineEdit("magical forest moss skull")
        layout_forge.addWidget(self.txt_game_idea)
        self.cmb_game_style = QComboBox()
        self.cmb_game_style.addItems(["Pixel Art", "3D Model/Slicer", "Gothic Cute"])
        layout_forge.addWidget(self.cmb_game_style)
        
        btn_gen_prompt = QPushButton("💡 Formulate Optimized Game Asset Engine Prompt")
        btn_gen_prompt.clicked.connect(lambda: self.cast_asynchronously(asset_summoner.architect_game_asset_prompt, self.txt_game_idea.text(), self.cmb_game_style.currentText()))
        layout_forge.addWidget(btn_gen_prompt)
        
        main_layout.addWidget(card_forge)
        self.tabs.addTab(page, "Design Forge")

    def init_browser_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_web, layout_web = self.create_card("Browser Automation", "#143a96", "white")
        self.txt_script = QLineEdit("Adblock Core")
        layout_web.addWidget(self.txt_script)
        main_layout.addWidget(card_web)
        self.tabs.addTab(page, "Browser Alchemy")

    def init_tuning_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        card_guard, layout_guard = self.create_card("System Policy Shields", "#a13d2d", "white")
        btn_policies = QPushButton("🔒 Inject Explorer Registry Policy Guards")
        btn_policies.clicked.connect(lambda: self.cast_asynchronously(persistent_bans.freeze_windows_bloatware_policies))
        layout_guard.addWidget(btn_policies)
        main_layout.addWidget(card_guard)
        self.tabs.addTab(page, "Arcane Tuning")

    def apply_theme(self):
        master_layout = QHBoxLayout()
        
        # Left Side Container: App Navigation Controls and Console Logs
        left_workspace = QVBoxLayout()
        left_workspace.addWidget(self.tabs)
        
        left_workspace.addWidget(QLabel("🔮 GRIMOIRE SYSTEM LOG ACTION MONITOR OUTPUT:"))
        self.console_out = QTextEdit()
        self.console_out.setReadOnly(True)
        self.console_out.setFixedHeight(110)
        left_workspace.addWidget(self.console_out)
        master_layout.addLayout(left_workspace, stretch=3)
        
        # Right Side Container: Dedicated Real-time Image Preview Window
        right_preview_panel = QVBoxLayout()
        right_preview_panel.addWidget(QLabel("🖼️ ACTIVE LAYOUT IMAGE PREVIEW LAYER"))
        self.preview_window = QLabel()
        self.preview_window.setObjectName("ImagePreviewBay")
        self.preview_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_window.setFixedSize(260, 560)
        self.preview_window.setStyleSheet("background-color: #060507; border: 2px dashed #231e2e; border-radius: 12px; color: #5c5566;")
        self.preview_window.setText("[ No Active Asset Rendered ]")
        right_preview_panel.addWidget(self.preview_window)
        master_layout.addLayout(right_preview_panel, stretch=1)
        
        container = QWidget()
        container.setLayout(master_layout)
        self.setCentralWidget(container)

        self.setStyleSheet("""
            QMainWindow, QWidget { background-color: #0c0a0f; }
            QTabWidget::panel { background-color: #121016; border: none; }
            QFrame#DashboardCard { background-color: #16131c; border: 1px solid #231e2e; border-radius: 14px; }
            QTabBar::tab { background: #131017; color: #5c5566; padding: 7px 10px; font-weight: bold; font-family: 'Segoe UI'; font-size: 11px; border-top-left-radius: 6px; border-top-right-radius: 6px; margin-right: 2px; }
            QTabBar::tab:selected { background: #16131c; color: #00ffcc; border-bottom: 2px solid #00ffcc; }
            QLabel { color: #cfcad6; font-family: 'Segoe UI'; font-size: 11px; }
            QCheckBox { color: #b1a9b8; font-family: 'Segoe UI'; font-size: 11px; }
            QComboBox { background-color: #1a1622; color: white; border: 1px solid #282233; border-radius: 4px; padding: 3px; font-size: 11px; }
            QLineEdit { background-color: #1a1622; color: #00ffcc; border: 1px solid #282233; border-radius: 4px; padding: 4px; font-family: 'Consolas'; font-size: 11px; }
            QTextEdit { background-color: #060507; color: #00ffcc; border: 1px solid #1c1824; font-family: 'Consolas'; font-size: 11px; border-radius: 8px; padding: 5px; }
            QSlider::groove:horizontal { border: 1px solid #231e2e; height: 6px; background: #1a1622; border-radius: 3px; }
            QSlider::handle:horizontal { background: #00ffcc; width: 14px; margin: -4px 0; border-radius: 7px; }
            QPushButton { background-color: #1c1824; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; border-radius: 6px; padding: 6px; font-family: 'Segoe UI'; font-size: 11px; }
            QPushButton:hover { background-color: #00ffcc; color: #0c0a0f; }
        """)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())
