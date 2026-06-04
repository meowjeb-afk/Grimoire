# File: ui_dashboard.py
import sys
import os
import math
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QCheckBox, QTabWidget, 
    QLineEdit, QTextEdit, QComboBox, QFrame, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush, QConicalGradient

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

class ArcaneSystemVisualizer(QWidget):
    """Custom vector-drawn visualizer replacing the plain text logger with a dynamic matrix canvas."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(150)
        self.angle = 0
        self.pulse = 0
        self.pulse_growing = True
        self.is_active = False
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def trigger_pulse(self):
        self.is_active = True
        self.pulse = 30

    def update_animation(self):
        self.angle = (self.angle + 1) % 360
        if self.pulse_growing:
            self.pulse += 0.2
            if self.pulse >= 12: self.pulse_growing = False
        else:
            self.pulse -= 0.2
            if self.pulse <= 2: self.pulse_growing = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        center_x = width // 2
        center_y = height // 2
        radius = min(center_x, center_y) - 20
        
        painter.fillRect(self.rect(), QColor("#08060f"))
        painter.setPen(QPen(QColor("#1f1833"), 1, Qt.PenStyle.DashLine))
        painter.drawEllipse(QPoint(center_x, center_y), radius, radius)
        
        painter.setPen(QPen(QColor("#2d2349"), 1, Qt.PenStyle.SolidLine))
        for i in range(3):
            r_offset = radius - (i * 20) - int(self.pulse)
            if r_offset > 0:
                painter.drawEllipse(QPoint(center_x, center_y), r_offset, r_offset)
                
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self.angle)
        
        gradient = QConicalGradient(0, 0, 0)
        gradient.setColorAt(0.0, QColor("#7b61ff"))
        gradient.setColorAt(0.5, QColor("#1e1730"))
        gradient.setColorAt(1.0, QColor("#61ffcf"))
        
        glow_pen = QPen(QBrush(gradient), 2)
        painter.setPen(glow_pen)
        painter.drawRect(-radius // 3, -radius // 3, (radius // 3) * 2, (radius // 3) * 2)
        painter.restore()
        
        core_color = QColor("#61ffcf") if self.is_active else QColor("#7b61ff")
        painter.setBrush(QBrush(core_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(QPoint(center_x, center_y), 6, 6)
        
        if self.is_active and self.angle % 5 == 0:
            self.is_active = False

class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.setFixedSize(1040, 780)
        
        # Strip native OS title bar frame
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Variables to track mouse movement for window dragging
        self.drag_position = QPoint()

        # Main Window Base Layout
        self.main_container = QWidget()
        self.main_container.setObjectName("MainContainer")
        self.setCentralWidget(self.main_container)
        
        master_vertical = QVBoxLayout(self.main_container)
        master_vertical.setContentsMargins(0, 0, 0, 0)
        master_vertical.setSpacing(0)
        
        # 1. Inject Custom Immersive Title Bar Component
        self.init_custom_title_bar(master_vertical)
        
        # 2. Main Content Split Panel (Sidebar + Workspaces + Preview)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        master_vertical.addLayout(content_layout)
        
        # Initialize Left Navigation Sidebar
        self.init_sidebar(content_layout)
        
        # Main Workspace Page Stack
        self.workspace_stack = QTabWidget()
        self.workspace_stack.tabBar().hide() # Hide default tab bar headers
        content_layout.addWidget(self.workspace_stack, stretch=3)
        
        # Initialize Right Side Real-time Image Preview Dock
        self.init_right_preview_panel(content_layout)
        
        # Initialize Individual Module Views
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_image_tab()
        self.init_creative_nexus_tab()
        self.init_deployment_architect_tab()
        self.init_tuning_tab()
        
        self.apply_theme()

    # --- Frameless Window Dragging Mathematics ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def init_custom_title_bar(self, parent_layout):
        """Constructs a beautifully stylized title bar replacing the default Windows frame layout."""
        self.title_bar = QFrame()
        self.title_bar.setObjectName("CustomTitleBar")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 6, 12, 6)
        title_layout.setSpacing(8)
        
        # Window Label / Title
        window_title = QLabel("🔮 Grimoire Master OS Shell Extension")
        title_style = "color: #a397bf; font-family: 'Segoe UI'; font-weight: bold; font-size: 11px; letter-spacing: 0.5px;"
        window_title.setStyleSheet(title_style)
        title_layout.addWidget(window_title)
        title_layout.addStretch()
        
        # Minimize Window Control Action
        btn_min = QPushButton("🗕")
        btn_min.setObjectName("TitleMinButton")
        btn_min.setFixedSize(28, 24)
        btn_min.clicked.connect(self.showMinimized)
        title_layout.addWidget(btn_min)
        
        # Close Window Control Action
        btn_close = QPushButton("🗙")
        btn_close.setObjectName("TitleCloseButton")
        btn_close.setFixedSize(28, 24)
        btn_close.clicked.connect(self.close)
        title_layout.addWidget(btn_close)
        
        parent_layout.addWidget(self.title_bar)

    def init_sidebar(self, parent_layout):
        """Builds the left vertical navigation deck."""
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarDock")
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(6)
        
        brand_label = QLabel("GRIMOIRE")
        brand_style = "font-size: 14px; font-weight: 900; color: #ffffff; padding-bottom: 20px; font-family: 'Segoe UI'; letter-spacing: 1px;"
        brand_label.setStyleSheet(brand_style)
        brand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(brand_label)
        
        self.nav_buttons = []
        modules = [
            ("Dashboard", 0),
            ("File Alchemy", 1),
            ("Visual Alchemy", 2),
            ("Creative Nexus", 3),
            ("Deployment", 4),
            ("Arcane Tuning", 5)
        ]
        
        for name, index in modules:
            btn = QPushButton(name)
            btn.setCheckable(True)
            if index == 0: btn.setChecked(True)
            btn.clicked.connect(lambda checked, idx=index: self.switch_workspace_view(idx))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)
            
        sidebar_layout.addStretch()
        
        footer_tag = QLabel("v2.4.1")
        footer_style = "color: #4a3e63; font-size: 10px; font-family: 'Consolas'; font-weight: bold;"
        footer_tag.setStyleSheet(footer_style)
        footer_tag.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(footer_tag)
        
        parent_layout.addWidget(self.sidebar_frame, stretch=0)

    def switch_workspace_view(self, index):
        self.workspace_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    def init_right_preview_panel(self, parent_layout):
        """Creates the right-hand live image display hub with integrated vector visualization."""
        self.right_panel_frame = QFrame()
        self.right_panel_frame.setObjectName("RightPreviewPanel")
        right_layout = QVBoxLayout(self.right_panel_frame)
        right_layout.setContentsMargins(15, 20, 15, 20)
        right_layout.setSpacing(10)
        
        right_layout.addWidget(QLabel("🖼️ REAL-TIME PREVIEW BAY"))
        
        self.preview_window = QLabel()
        self.preview_window.setObjectName("ImagePreviewBay")
        self.preview_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_window.setFixedSize(240, 360)
        self.preview_window.setText("[ Waiting for Asset ]")
        right_layout.addWidget(self.preview_window)
        
        # System Telemetry Vector Canvas
        right_layout.addWidget(QLabel("SYSTEM TELEMETRY MATRIX"))
        self.visualizer = ArcaneSystemVisualizer()
        right_layout.addWidget(self.visualizer)
        
        parent_layout.addWidget(self.right_panel_frame, stretch=1)

    def cast_asynchronously(self, target_function, *args):
        self.visualizer.trigger_pulse()
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.display_output)
        self.worker.start()

    def display_output(self, text):
        if "C:\\Public\\" in text and (".png" in text or ".jpg" in text):
            for word in text.split():
                if os.path.exists(word) and word.endswith((".png", ".jpg")):
                    pixmap = QPixmap(word)
                    self.preview_window.setPixmap(pixmap.scaled(self.preview_window.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def create_card(self, title, subtext="Quick Actions"):
        """Generates the soft rounded neon-obsidian layout boxes."""
        card_frame = QFrame()
        card_frame.setObjectName("DashboardCard")
        
        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(18, 18, 18, 18)
        card_layout.setSpacing(12)
        
        header_layout = QHBoxLayout()
        title_lbl = QLabel(title)
        title_style = "font-size: 14px; font-weight: bold; color: #ffffff; font-family: 'Segoe UI';"
        title_lbl.setStyleSheet(title_style)
        sub_lbl = QLabel(subtext)
        sub_style = "font-size: 10px; color: #645585; font-family: 'Segoe UI';"
        sub_lbl.setStyleSheet(sub_style)
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()
        header_layout.addWidget(sub_lbl)
        
        card_layout.addLayout(header_layout)
        return card_frame, card_layout

    def init_core_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        card_cfg, layout_cfg = self.create_card("Windows Management", "System Hooks")
        self.chk_startup = QCheckBox(" Initialize on System Bootup")
        self.chk_clipboard = QCheckBox(" Clipboard Interception Active")
        self.chk_clipboard.setChecked(True)
        layout_cfg.addWidget(self.chk_startup)
        layout_cfg.addWidget(self.chk_clipboard)
        
        btn_pin = QPushButton("Pin Target Frame to Always On Top")
        btn_pin.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').window_anchors.pin_active_window()))
        layout_cfg.addWidget(btn_pin)
        main_layout.addWidget(card_cfg)
        
        card_act, layout_act = self.create_card("Telemetry Control", "Bare-Metal Diagnostics")
        btn_telemetry = QPushButton("Query Bare-Metal Performance Metrics")
        btn_telemetry.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').system_monitors.get_system_metrics()))
        layout_act.addWidget(btn_telemetry)
        main_layout.addWidget(card_act)
        
        self.workspace_stack.addTab(page, "Dashboard")

    def init_alchemy_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        card_dir, layout_dir = self.create_card("Directory Sorting Vector", "File System")
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads")
        layout_dir.addWidget(self.txt_path)
        btn_run_sort = QPushButton("Execute File Alchemy Sorting")
        btn_run_sort.clicked.connect(lambda: self.cast_asynchronously(lambda p: __import__('incantations').file_alchemy.transmute_folder(p), self.txt_path.text()))
        layout_dir.addWidget(btn_run_sort)
        main_layout.addWidget(card_dir)
        
        self.workspace_stack.addTab(page, "File Alchemy")

    def init_image_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        card_img, layout_img = self.create_card("Visual Manipulation Chamber", "Image Matrix")
        self.txt_img_path = QLineEdit(r"C:\Users\Public\Grimoire_Procedural_Logo.png")
        layout_img.addWidget(self.txt_img_path)
        
        btn_bg = QPushButton("Erase Image Background (Transparent PNG)")
        btn_bg.clicked.connect(lambda: self.cast_asynchronously(lambda p: __import__('incantations').image_matrix.erase_background(p), self.txt_img_path.text()))
        layout_img.addWidget(btn_bg)
        main_layout.addWidget(card_img)
        
        self.workspace_stack.addTab(page, "Visual Alchemy")

    def init_creative_nexus_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        row_layout = QHBoxLayout()
        
        left_col = QVBoxLayout()
        card_gif, layout_gif = self.create_card("Giphy & Sticker Suite", "Asset Handoff")
        self.txt_gif_query = QLineEdit("creepy cute sticker")
        layout_gif.addWidget(self.txt_gif_query)
        btn_find_gif = QPushButton("🔍 Search Giphy Streams")
        btn_find_gif.clicked.connect(lambda: self.cast_asynchronously(lambda q: __import__('incantations').image_matrix.search_giphy(q), self.txt_gif_query.text()))
        layout_gif.addWidget(btn_find_gif)
        
        btn_pack_sticker = QPushButton("🏷️ Format & Copy Sticker to Clipboard")
        btn_pack_sticker.clicked.connect(lambda: self.cast_asynchronously(lambda p, t: __import__('incantations').image_matrix.format_sticker_package(p, t), self.txt_img_path.text(), "discord"))
        layout_gif.addWidget(btn_pack_sticker)
        left_col.addWidget(card_gif)
        
        card_sliders, layout_sliders = self.create_card("Pixelation Modulator", "Matrix Transformation")
        layout_sliders.addWidget(QLabel("Pixel Size Filter Scale:"))
        self.slider_pixel = QSlider(Qt.Orientation.Horizontal)
        self.slider_pixel.setRange(2, 32)
        self.slider_pixel.setValue(8)
        layout_sliders.addWidget(self.slider_pixel)
        
        btn_pixel_art = QPushButton("👾 Transmute Image to Pixel Art")
        btn_pixel_art.clicked.connect(lambda: self.cast_asynchronously(lambda p, s: __import__('incantations').image_matrix.apply_pixel_art_slider(p, s), self.txt_img_path.text(), self.slider_pixel.value()))
        layout_sliders.addWidget(btn_pixel_art)
        left_col.addWidget(card_sliders)
        row_layout.addLayout(left_col)
        
        right_col = QVBoxLayout()
        card_ai, layout_ai = self.create_card("Offline AI & Toy Forge", "Stable Diffusion Interface")
        self.txt_ai_prompt = QLineEdit("gothic cottagecore item plush")
        layout_ai.addWidget(self.txt_ai_prompt)
        
        btn_offline_ai = QPushButton("🎨 Offline AI Render (Port 7860)")
        btn_offline_ai.clicked.connect(lambda: self.cast_asynchronously(lambda pr: __import__('incantations').asset_summoner.local_offline_ai_forge(pr), self.txt_ai_prompt.text()))
        layout_ai.addWidget(btn_offline_ai)
        
        btn_plush = QPushButton("🧸 Transmute Image into Plush Toy")
        btn_plush.clicked.connect(lambda: self.cast_asynchronously(lambda p, m: __import__('incantations').image_matrix.transmute_to_plush_or_crochet(p, m), self.txt_img_path.text(), "plush"))
        layout_ai.addWidget(btn_plush)
        
        btn_crochet = QPushButton("🧶 Convert Image into Crochet Pattern Grid")
        btn_crochet.clicked.connect(lambda: self.cast_asynchronously(lambda p, m: __import__('incantations').image_matrix.transmute_to_plush_or_crochet(p, m), self.txt_img_path.text(), "crochet"))
        layout_ai.addWidget(btn_crochet)
        right_col.addWidget(card_ai)
        
        row_layout.addLayout(right_col)
        main_layout.addLayout(row_layout)
        self.workspace_stack.addTab(page, "Creative Nexus")

    def init_deployment_architect_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        card_rep, layout_rep = self.create_card("OS Deployment Replicator", "Backup & Install")
        btn_restore = QPushButton("🛡️ Generate Safe System Restore Checkpoint")
        btn_restore.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').deep_cleaner.drop_system_restore_anchor()))
        layout_rep.addWidget(btn_restore)
        
        btn_export_apps = QPushButton("📋 Export System Software Configuration List")
        btn_export_apps.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').deep_cleaner.export_installed_software_replica()))
        layout_rep.addWidget(btn_export_apps)
        
        self.txt_todo_replica = QTextEdit("[ ] REINSTALL: GoogleChrome\n[ ] REINSTALL: VLC\n[ ] REINSTALL: Steam")
        layout_rep.addWidget(self.txt_todo_replica)
        
        btn_run_bulk = QPushButton("🚀 Run Automated Silent Bulk Installer Loop")
        btn_run_bulk.clicked.connect(lambda: self.cast_asynchronously(lambda t: __import__('incantations').deep_cleaner.execute_silent_bulk_installer_exe(t), self.txt_todo_replica.toPlainText()))
        layout_rep.addWidget(btn_run_bulk)
        
        main_layout.addWidget(card_rep)
        self.workspace_stack.addTab(page, "Deployment")

    def init_tuning_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        card_guard, layout_guard = self.create_card("System Policy Shields", "Registry Security")
        btn_policies = QPushButton("🔒 Inject Registry Policy Guards Against Auto-Bloatware")
        btn_policies.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').persistent_bans.freeze_windows_bloatware_policies()))
        layout_guard.addWidget(btn_policies)
        main_layout.addWidget(card_guard)
        
        self.workspace_stack.addTab(page, "Arcane Tuning")

    def apply_theme(self):
        """Implements the deep gothic palette."""
        self.setStyleSheet("""
            QWidget#MainContainer {
                background-color: #0b0813;
                border: 1px solid #1f1833;
                border-radius: 12px;
            }
            
            /* Frameless Custom Title Bar Layout Styling */
            QFrame#CustomTitleBar {
                background-color: #0b0813;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom: 1px solid #140f24;
            }
            QPushButton#TitleMinButton, QPushButton#TitleCloseButton {
                background: transparent;
                color: #5c4e7a;
                border: none;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton#TitleMinButton:hover {
                color: #7b61ff;
                background-color: #171226;
                border-radius: 4px;
            }
            QPushButton#TitleCloseButton:hover {
                color: #ffffff;
                background-color: #ff4d4d;
                border-radius: 4px;
            }
            
            /* Left Sidebar Container Dock Layout */
            QFrame#SidebarDock {
                background-color: #120e1f;
                border-right: 1px solid #1f1833;
                border-bottom-left-radius: 11px;
            }
            QFrame#SidebarDock QPushButton {
                background-color: transparent;
                color: #8c7fa6;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-family: 'Segoe UI';
                font-weight: bold;
                font-size: 11px;
                text-align: left;
            }
            QFrame#SidebarDock QPushButton:hover {
                background-color: #1a142e;
                color: #ffffff;
            }
            QFrame#SidebarDock QPushButton:checked {
                background-color: #241b3f;
                color: #7b61ff;
                border-left: 3px solid #7b61ff;
            }
            
            /* Main Workspace Area Panels */
            QTabWidget::panel { 
                background-color: #0b0813; 
                border: none; 
            }
            
            /* Inner Card Component Containers */
            QFrame#DashboardCard { 
                background-color: #171226; 
                border: 1px solid #251d3a; 
                border-radius: 16px; 
            }
            
            /* Right Control Monitor Panel */
            QFrame#RightPreviewPanel {
                background-color: #120e1f;
                border-left: 1px solid #1f1833;
                border-bottom-right-radius: 11px;
            }
            
            QLabel { 
                color: #a397bf; 
                font-family: 'Segoe UI'; 
                font-size: 11px; 
                font-weight: bold;
            }
            QCheckBox { 
                color: #c9bedf; 
                font-family: 'Segoe UI'; 
                font-size: 11px; 
            }
            QComboBox { 
                background-color: #1e1730; 
                color: white; 
                border: 1px solid #2d2349; 
                border-radius: 6px; 
                padding: 5px; 
                font-size: 11px; 
            }
            QLineEdit { 
                background-color: #1e1730; 
                color: #61ffcf; 
                border: 1px solid #2d2349; 
                border-radius: 6px; 
                padding: 6px; 
                font-family: 'Consolas'; 
                font-size: 11px; 
            }
            QTextEdit { 
                background-color: #08060f; 
                color: #61ffcf; 
                border: 1px solid #1e1730; 
                font-family: 'Consolas'; 
                font-size: 11px; 
                border-radius: 10px; 
                padding: 8px; 
            }
            
            /* Slider Interface Tracks */
            QSlider::groove:horizontal { 
                border: 1px solid #2d2349; 
                height: 6px; 
                background: #1e1730; 
                border-radius: 3px; 
            }
            QSlider::handle:horizontal { 
                background: #7b61ff; 
                width: 14px; 
                margin: -4px 0; 
                border-radius: 7px; 
            }
            
            /* Dashboard Interactive Action Buttons */
            QPushButton { 
                background-color: #211936; 
                color: #7b61ff; 
                font-weight: bold; 
                border: 1px solid #322652; 
                border-radius: 8px; 
                padding: 8px; 
                font-family: 'Segoe UI'; 
                font-size: 11px; 
            }
            QPushButton:hover { 
                background-color: #7b61ff; 
                color: #ffffff; 
                border-color: #7b61ff;
            }
            
            /* Live Image Asset Preview Box Container */
            QLabel#ImagePreviewBay {
                background-color: #08060f; 
                border: 2px dashed #251d3a; 
                border-radius: 14px; 
                color: #52476d;
                font-family: 'Segoe UI';
                font-size: 11px;
            }
        """)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())
