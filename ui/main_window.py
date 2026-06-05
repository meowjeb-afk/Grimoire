import sys
import os
import io
import gc
import re
import psutil
import numpy as np
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QFrame, QTabWidget, QFileDialog, QMessageBox, QSlider,
    QTableWidget, QTableWidgetItem, QGroupBox
)
from PyQt6.QtCore import Qt, QTimer, QRunnable, QThreadPool, pyqtSlot
from PyQt6.QtGui import QPixmap, QGuiApplication

# Import your modules (assumed to be available)
from core.ai_suite import DesignSuite, AdvancedDesignExtensions, HEAVY_DEPS_AVAILABLE
from core.workers import ArcaneWorker, TelemetrySampler
from ui.custom_widgets import ColorPreservingLabel, GrimoireNavButton
from ui.tabs import (
    DashboardMixin, FileAlchemyMixin, VisualAlchemyMixin, DeploymentMixin, 
    TaskViewerMixin, TuningMixin, OpticalScryingMixin, NetworkScryingMixin, 
    AutomationWeaverMixin, ClipboardGrimoireMixin
)
from incantations.optical_scrying import OpticalScrying
from incantations.network_scrying import NetworkScrying
from incantations.automation_weaver import AutomationWeaver
from incantations.clipboard_grimoire import ClipboardGrimoire
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

# --- ThreadRunnable for heavy processing ---
class ImageProcessingTask(QRunnable):
    def __init__(self, func, *args, callback=None):
        super().__init__()
        self.func = func
        self.args = args
        self.callback = callback

    @pyqtSlot()
    def run(self):
        try:
            result = self.func(*self.args)
            if self.callback:
                self.callback(result)
        except Exception as e:
            print(f"Error in thread: {e}")

# --- Main App Class ---
class GrimoireMirror(QMainWindow, DashboardMixin, FileAlchemyMixin, VisualAlchemyMixin, 
                     DeploymentMixin, TaskViewerMixin, TuningMixin, 
                     OpticalScryingMixin, NetworkScryingMixin, 
                     AutomationWeaverMixin, ClipboardGrimoireMixin):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.resize(1200, 850)
        self.setMinimumSize(900, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Paths
        self.logo_icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "grimoire_logo.png")
        self.logo_text_path = os.path.join(os.path.dirname(__file__), "..", "assets", "grimoire_text.png")

        # State
        self.drag_pos = None
        self.is_maximized = False
        self.is_resizing = False
        self.resize_edge = None
        self.resize_start_geo = None
        self.resize_start_pos = None

        # Image State
        self.current_image = None
        self.current_image_path = None
        self.edited_image = None
        self.image_history = []

        # Thread pool
        self.thread_pool = QThreadPool()

        # Initialize modules
        self.init_modules()

        # Setup UI
        self.init_ui()

        # Telemetry
        self.telemetry_thread = TelemetrySampler(1.5)
        self.telemetry_thread.system_metrics_updated.connect(self.update_main_dashboard)
        self.telemetry_thread.internal_process_updated.connect(self.update_visualizer_matrix)
        self.telemetry_thread.start()

        # Timer for real-time preview
        self.preview_timer = QTimer()
        self.preview_timer.timeout.connect(self.update_preview)
        self.preview_timer.start(200)

        # Dark mode
        self.is_dark_mode = True

    def init_modules(self):
        self.design_suite = None
        self.advanced_extensions = None
        if HEAVY_DEPS_AVAILABLE:
            try:
                self.design_suite = DesignSuite()
                self.advanced_extensions = AdvancedDesignExtensions()
            except Exception as e:
                print(f"AI modules load error: {e}")
        self.optical_scrying = OpticalScrying()
        self.network_scrying = NetworkScrying()
        self.automation_weaver = AutomationWeaver()
        self.clipboard_grimoire = ClipboardGrimoire(QGuiApplication.clipboard())
        self.clipboard_grimoire.history_updated.connect(self.update_clipboard_ui)

    def init_ui(self):
        # Main container
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout(self.main_widget)

        # Title bar
        self.init_title_bar()

        # Top controls (theme toggle, filters, batch)
        self.init_top_controls()

        # Content area (sidebar + tabs)
        self.content_layout = QHBoxLayout()
        self.content_layout.setContentsMargins(0,0,0,0)
        self.content_layout.setSpacing(0)

        self.init_sidebar()
        self.tabs = QTabWidget()
        self.tabs.tabBar().hide()
        self.content_layout.addWidget(self.tabs, stretch=1)

        # Initialize tabs (via mixins)
        self.init_tabs()

        self.main_layout.addLayout(self.content_layout)

        # Status bar
        self.init_status_bar()

        # Apply theme
        self.apply_theme()

    def init_title_bar(self):
        self.title_bar = QFrame()
        self.title_bar.setObjectName("CustomTitleBar")
        layout = QHBoxLayout(self.title_bar)
        layout.setContentsMargins(15,6,12,6)
        logo_lbl = ColorPreservingLabel(self.logo_icon_path)
        logo_lbl.setFixedSize(20,20)
        layout.addWidget(logo_lbl)
        title_lbl = QLabel("Grimoire Master OS Shell Extension")
        title_lbl.setStyleSheet("color:#a397bf; font-family:'Segoe UI'; font-weight:bold; font-size:11px;")
        layout.addWidget(title_lbl)
        layout.addStretch()
        btn_min = QPushButton("−")
        btn_min.setObjectName("TitleMinButton")
        btn_min.setFixedSize(28,24)
        btn_min.clicked.connect(self.showMinimized)
        layout.addWidget(btn_min)
        btn_max = QPushButton("□")
        btn_max.setObjectName("TitleMaxButton")
        btn_max.setFixedSize(28,24)
        btn_max.clicked.connect(self.toggle_maximize)
        layout.addWidget(btn_max)
        btn_close = QPushButton("✕")
        btn_close.setObjectName("TitleCloseButton")
        btn_close.setFixedSize(28,24)
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)
        self.main_layout.addWidget(self.title_bar)

    def init_top_controls(self):
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(10,10,10,10)
        layout.setSpacing(20)

        # Theme toggle
        theme_btn = QPushButton("Toggle Dark Mode")
        theme_btn.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_btn)

        # Image filters
        filters_group = QGroupBox("Image Filters")
        f_layout = QVBoxLayout()
        filters_group.setLayout(f_layout)

        # Brightness
        lbl_brightness = QLabel("Brightness")
        self.slider_brightness = QSlider(Qt.Orientation.Horizontal)
        self.slider_brightness.setRange(0,200)
        self.slider_brightness.setValue(100)
        self.slider_brightness.valueChanged.connect(self.apply_brightness)
        f_layout.addWidget(lbl_brightness)
        f_layout.addWidget(self.slider_brightness)

        # Contrast
        lbl_contrast = QLabel("Contrast")
        self.slider_contrast = QSlider(Qt.Orientation.Horizontal)
        self.slider_contrast.setRange(0,200)
        self.slider_contrast.setValue(100)
        self.slider_contrast.valueChanged.connect(self.apply_contrast)
        f_layout.addWidget(lbl_contrast)
        f_layout.addWidget(self.slider_contrast)

        # Sharpness
        lbl_sharpness = QLabel("Sharpness")
        self.slider_sharpness = QSlider(Qt.Orientation.Horizontal)
        self.slider_sharpness.setRange(0,300)
        self.slider_sharpness.setValue(150)
        self.slider_sharpness.valueChanged.connect(self.apply_sharpen)
        f_layout.addWidget(lbl_sharpness)
        f_layout.addWidget(self.slider_sharpness)

        # Batch convert button
        batch_btn = QPushButton("Batch Convert to Grayscale")
        batch_btn.clicked.connect(self.batch_convert_grayscale)
        f_layout.addWidget(batch_btn)

        layout.addWidget(filters_group)

        self.main_layout.addWidget(container)

    def init_sidebar(self):
        self.sidebar = QFrame()
        self.sidebar.setObjectName("SidebarDock")
        self.sidebar.setFixedWidth(60)
        layout = QVBoxLayout(self.sidebar)
        layout.setContentsMargins(8,20,8,20)
        layout.setSpacing(12)

        logo_widget = QWidget()
        logo_layout = QVBoxLayout(logo_widget)
        logo_layout.setContentsMargins(0,0,0,16)
        logo_lbl = ColorPreservingLabel(self.logo_icon_path)
        logo_lbl.setFixedSize(44,44)
        logo_layout.addWidget(logo_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_widget)

        # Navigation buttons
        self.nav_buttons = []
        modules = [("assets/0.png","Dashboard",0), ("assets/1.png","File Alchemy",1), ("assets/2.png","Visual Alchemy",2),
                   ("assets/3.png","Deployment",3), ("assets/4.png","Task Viewer",4), ("assets/5.png","Arcane Tuning",5),
                   ("assets/6.png","Optical Scrying",6), ("assets/7.png","Network Scrying",7),
                   ("assets/8.png","Automation",8), ("assets/9.png","Clipboard",9)]
        for icon_path, name, idx in modules:
            btn = GrimoireNavButton(icon_path, name, idx, True)
            if idx == 0: btn.setChecked(True)
            btn.clicked.connect(lambda checked, i=idx: self.switch_workspace(i))
            layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter)
            self.nav_buttons.append(btn)

        layout.addStretch()
        self.content_layout.addWidget(self.sidebar)

    def switch_workspace(self, index):
        self.tabs.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i==index)

    def init_status_bar(self):
        self.status_bar = QFrame()
        self.status_bar.setObjectName("StatusBar")
        layout = QHBoxLayout(self.status_bar)
        layout.setContentsMargins(16,4,16,4)
        layout.setSpacing(16)
        lbl_dot = QLabel("●")
        lbl_dot.setStyleSheet("color: #61ffcf; font-size: 10px;")
        layout.addWidget(lbl_dot)
        lbl_status = QLabel("Grimoire Shell Active")
        lbl_status.setStyleSheet("color: #645585; font-size: 10px;")
        layout.addWidget(lbl_status)
        layout.addStretch()
        self.lbl_cpu = QLabel("CPU --%")
        self.lbl_mem = QLabel("MEM --%")
        self.lbl_time = QLabel("--:--:--")
        self.lbl_cpu.setStyleSheet("color: #7b61ff; font-family: 'Consolas'; font-weight: bold; font-size: 10px;")
        self.lbl_mem.setStyleSheet("color: #61ffcf; font-family: 'Consolas'; font-weight: bold; font-size: 10px;")
        self.lbl_time.setStyleSheet("color: #4a3e63; font-family: 'Consolas'; font-size: 10px;")
        layout.addWidget(self.lbl_cpu)
        layout.addWidget(self.lbl_mem)
        layout.addWidget(self.lbl_time)
        self.main_layout.addWidget(self.status_bar)

    # --- Update Telemetry ---
    def update_main_dashboard(self, cpu, mem, swap):
        self.telemetry_state = {"cpu": cpu, "memory": mem, "swap": swap}
        self.lbl_cpu.setText(f"CPU {cpu:.0f}%")
        self.lbl_mem.setText(f"MEM {mem:.0f}%")
        self.lbl_time.setText(datetime.now().strftime("%H:%M:%S"))

    def update_visualizer_matrix(self, data):
        # placeholder for process list update
        pass

    def update_preview(self):
        if self.edited_image:
            buf = io.BytesIO()
            self.edited_image.save(buf, format='PNG')
            buf.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        gc.collect()

    # --- Main tab init (via mixins) ---
    def init_tabs(self):
        # Assume mixins add their tabs
        # For demo, add a placeholder tab
        self.dashboard_tab = QWidget()
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        # Add more tabs as needed

        # For image preview, add a label
        self.preview_label = QLabel()
        self.preview_label.setFixedSize(400, 300)
        layout = QVBoxLayout(self.dashboard_tab)
        layout.addWidget(self.preview_label)

    # --- Title bar ---
    def toggle_maximize(self):
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
        else:
            self.showMaximized()
            self.is_maximized = True

    # --- Theme toggle ---
    def toggle_theme(self):
        self.is_dark_mode = not getattr(self, 'is_dark_mode', True)
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QWidget#MainContainer { background-color: #0b0813; border: 1px solid #1f1833; border-radius: 12px; }
                QFrame#CustomTitleBar { background-color: #0b0813; border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: 1px solid #140f24; }
                QFrame#SidebarDock { background-color: #120e1f; border-right: 1px solid #1f1833; border-bottom-left-radius: 11px; }
                QPushButton#TitleMinButton, QPushButton#TitleMaxButton, QPushButton#TitleCloseButton { background-color: transparent; color: #8c7fa6; border: none; border-radius: 4px; padding: 4px; font-family: 'Segoe UI'; font-size: 14px; font-weight: bold; }
                QPushButton#TitleMinButton:hover, QPushButton#TitleMaxButton:hover { background-color: #2d2349; color: #7b61ff; }
                QPushButton#TitleCloseButton:hover { background-color: #ff4444; color: #fff; }
                QTabWidget::panel { background-color: #0b0813; border: none; }
                QLabel { color: #a397bf; font-family: 'Segoe UI'; font-size: 11px; }
                QLineEdit { background-color: #1e1730; color: #61ffcf; border: 1px solid #2d2349; border-radius: 6px; padding: 8px 12px; font-family: 'Consolas'; font-size: 11px; }
                QSlider::groove:horizontal { height: 8px; background: #2d2349; border-radius: 4px; }
                QSlider::handle:horizontal { background: #7b61ff; width: 16px; margin: -4px 0; border-radius: 8px; }
                QGroupBox { color: #a397bf; font-weight: bold; }
            """)
        else:
            # Light theme styles
            self.setStyleSheet("")

    # --- Image editing ---
    def save_state(self):
        if self.edited_image:
            self.image_history.append(self.edited_image.copy())

    def undo(self):
        if len(self.image_history) > 1:
            self.image_history.pop()
            self.edited_image = self.image_history[-1].copy()
            self.update_preview()

    def handle_image_input(self, path):
        if not os.path.exists(path):
            self.log_output(f"File not found: {path}")
            return
        self.asset_path = path
        self.current_image_path = path
        try:
            self.current_image = Image.open(path)
            self.edited_image = self.current_image.copy()
            self.image_history = [self.edited_image.copy()]
            self.log_output(f"Loaded: {os.path.basename(path)}")
        except Exception as e:
            self.log_output(f"Error loading image: {e}")
            return
        self.update_preview()

    def update_preview(self):
        if self.edited_image:
            buf = io.BytesIO()
            self.edited_image.save(buf, format='PNG')
            buf.seek(0)
            pixmap = QPixmap()
            pixmap.loadFromData(buf.getvalue())
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        gc.collect()

    def apply_brightness(self):
        val = self.slider_brightness.value()
        self.save_state()
        enhancer = ImageEnhance.Brightness(self.current_image if self.current_image else self.edited_image)
        self.edited_image = enhancer.enhance(val / 100.0)

    def apply_contrast(self):
        val = self.slider_contrast.value()
        self.save_state()
        enhancer = ImageEnhance.Contrast(self.current_image if self.current_image else self.edited_image)
        self.edited_image = enhancer.enhance(val / 100.0)

    def apply_sharpen(self):
        val = self.slider_sharpness.value()
        self.save_state()
        enhancer = ImageEnhance.Sharpness(self.edited_image)
        self.edited_image = enhancer.enhance(val / 100.0)

    def batch_convert_grayscale(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Images", "", "Images (*.png *.jpg *.jpeg)")
        for f in files:
            try:
                img = Image.open(f).convert('L')
                save_path = os.path.splitext(f)[0] + "_grayscale.png"
                img.save(save_path)
                self.log_output(f"Converted {f} -> {save_path}")
            except Exception as e:
                self.log_output(f"Error: {e}")

    def run_heavy_task(self, func, *args, callback=None):
        task = ImageProcessingTask(func, *args, callback=callback)
        self.thread_pool.start(task)

    # Add your AI or heavy tasks similar to previous pattern, using run_heavy_task

# --- Main ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())
