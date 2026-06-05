import sys
import os
import re
import io
import psutil
import numpy as np
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QCheckBox, QTabWidget, QLineEdit, QTextEdit, QFrame, QSlider, QMessageBox, 
    QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QSizePolicy
)
from PyQt6.QtCore import Qt

# Import local modules
from core.ai_suite import DesignSuite, AdvancedDesignExtensions, HEAVY_DEPS_AVAILABLE
from core.workers import ArcaneWorker, TelemetrySampler
from ui.custom_widgets import ColorPreservingLabel, PerformanceChart, GrimoireNavButton
from ui.tabs import DashboardMixin, FileAlchemyMixin, VisualAlchemyMixin, DeploymentMixin, TaskViewerMixin, TuningMixin
from PIL import Image, ImageOps, ImageFilter, ImageEnhance

class GrimoireMirror(QMainWindow, DashboardMixin, FileAlchemyMixin, VisualAlchemyMixin, DeploymentMixin, TaskViewerMixin, TuningMixin):
    def __init__(self):
        super().__init__()
        self.telemetry_thread = None
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.resize(1200, 850); self.setMinimumSize(900, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.logo_icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "grimoire_logo.png")
        self.logo_text_path = os.path.join(os.path.dirname(__file__), "..", "assets", "grimoire_text.png")

        self.drag_position = None; self.is_maximized = False; self.is_resizing = False
        self.resize_edge = None; self.resize_start_pos = None; self.resize_start_geo = None

        # Image editing state
        self.current_image = None; self.current_image_path = None; self.edited_image = None
        
        # Initialize AI Suites
        self.design_suite = None; self.advanced_extensions = None
        if HEAVY_DEPS_AVAILABLE:
            try:
                self.design_suite = DesignSuite()
                self.advanced_extensions = AdvancedDesignExtensions()
                print("✓ AI Design Suites loaded successfully.")
            except Exception as e:
                print(f"️ AI Design Suites failed to initialize: {e}")

        self.main_container = QWidget(); self.main_container.setObjectName("MainContainer"); self.setCentralWidget(self.main_container)
        master_vertical = QVBoxLayout(self.main_container); master_vertical.setContentsMargins(0, 0, 0, 0); master_vertical.setSpacing(0)
        self.init_custom_title_bar(master_vertical)
        content_layout = QHBoxLayout(); content_layout.setContentsMargins(0, 0, 0, 0); content_layout.setSpacing(0); master_vertical.addLayout(content_layout)
        self.init_sidebar(content_layout)
        self.workspace_stack = QTabWidget()
        if self.workspace_stack.tabBar() is not None: self.workspace_stack.tabBar().hide()
        content_layout.addWidget(self.workspace_stack, stretch=1)

        # Initialize Tabs via Mixins
        self.init_core_tab(); self.init_alchemy_tab(); self.init_visual_alchemy_tab()
        self.init_deployment_architect_tab(); self.init_task_viewer_tab(); self.init_tuning_tab()
        self.init_status_bar(master_vertical); self.apply_theme()

        self.telemetry_state = {"cpu": 0.0, "memory": 0.0, "swap": 0.0}
        self.asset_state = {"path": None, "message": "[ Waiting for Asset ]"}
        self.process_state = {"rows": []}

        self.telemetry_thread = TelemetrySampler(1.5)
        self.telemetry_thread.system_metrics_updated.connect(self.update_main_dashboard)
        self.telemetry_thread.internal_process_updated.connect(self.update_visualizer_matrix)
        self.telemetry_thread.start()

    def closeEvent(self, event):
        if self.telemetry_thread is not None: self.telemetry_thread.stop(); self.telemetry_thread.wait(1000)
        super().closeEvent(event)

    # --- Window Dragging/Resizing ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_maximized:
            edge = self.get_resize_edge(event.position().toPoint())
            if edge > 0:
                self.is_resizing = True; self.resize_edge = edge; self.resize_start_pos = event.globalPosition().toPoint(); self.resize_start_geo = self.geometry(); event.accept(); return
            widget_at_pos = self.childAt(event.position().toPoint())
            if widget_at_pos is self.title_bar or self.title_bar.isAncestorOf(widget_at_pos):
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft(); event.accept()
            else: event.ignore()
    def mouseMoveEvent(self, event):
        if not self.is_maximized: self.set_resize_cursor(self.get_resize_edge(event.position().toPoint()))
        if self.is_resizing and not self.is_maximized:
            delta = event.globalPosition().toPoint() - self.resize_start_pos; geo = self.resize_start_geo; edge = self.resize_edge
            if geo is None: return
            new_x, new_y, new_w, new_h = geo.x(), geo.y(), geo.width(), geo.height()
            if edge == 1: new_x += delta.x(); new_y += delta.y(); new_w -= delta.x(); new_h -= delta.y()
            elif edge == 2: new_y += delta.y(); new_w += delta.x(); new_h -= delta.y()
            elif edge == 3: new_x += delta.x(); new_w -= delta.x(); new_h += delta.y()
            elif edge == 4: new_w += delta.x(); new_h += delta.y()
            elif edge == 5: new_y += delta.y(); new_h -= delta.y()
            elif edge == 6: new_h += delta.y()
            elif edge == 7: new_x += delta.x(); new_w -= delta.x()
            elif edge == 8: new_w += delta.x()
            if new_w >= self.minimumWidth() and new_h >= self.minimumHeight(): self.setGeometry(new_x, new_y, new_w, new_h)
            event.accept(); return
        if event.buttons() == Qt.MouseButton.LeftButton and not self.is_maximized and hasattr(self, 'drag_position') and self.drag_position is not None:
            self.move(event.globalPosition().toPoint() - self.drag_position); event.accept()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.is_resizing = False; self.resize_edge = None; self.setCursor(Qt.CursorShape.ArrowCursor); event.accept()
    def get_resize_edge(self, pos):
        edge_size = 8; x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
        if x < edge_size and y < edge_size: return 1
        elif x > w - edge_size and y < edge_size: return 2
        elif x < edge_size and y > h - edge_size: return 3
        elif x > w - edge_size and y > h - edge_size: return 4
        elif y < edge_size: return 5
        elif y > h - edge_size: return 6
        elif x < edge_size: return 7
        elif x > w - edge_size: return 8
        return 0
    def set_resize_cursor(self, edge):
        if edge in (1, 4): self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in (2, 3): self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge in (5, 6): self.setCursor(Qt.CursorShape.SizeVerCursor)
        elif edge in (7, 8): self.setCursor(Qt.CursorShape.SizeHorCursor)
        else: self.setCursor(Qt.CursorShape.ArrowCursor)
    def toggle_maximize(self):
        if self.is_maximized: self.showNormal(); self.is_maximized = False
        else: self.showMaximized(); self.is_maximized = True

    # --- Telemetry & UI Updates ---
    def update_main_dashboard(self, cpu, mem, swap): self.telemetry_state.update({"cpu": cpu, "memory": mem, "swap": swap}); self.refresh_telemetry_view()
    
    def update_visualizer_matrix(self, data):
        # Cleaned up: Removed dead visualizer matrix update
        if data is None: data = {"processes": [], "process_count": 0}
        self.process_state["rows"] = data.get('processes', []); self.refresh_process_view()
        
    def refresh_telemetry_view(self):
        if hasattr(self, 'dashboard_stat_labels'):
            self.dashboard_stat_labels['cpu'].setText(f"{self.telemetry_state['cpu']:.1f}%")
            self.dashboard_stat_labels['memory'].setText(f"{self.telemetry_state['memory']:.1f}%")
        if hasattr(self, 'status_cpu_lbl'):
            self.status_cpu_lbl.setText(f"CPU {self.telemetry_state['cpu']:.0f}%")
            self.status_mem_lbl.setText(f"MEM {self.telemetry_state['memory']:.0f}%")
            self.status_time_lbl.setText(datetime.now().strftime("%H:%M:%S"))
    def refresh_process_view(self):
        if hasattr(self, 'process_table'): self.populate_process_table(self.process_state["rows"])
    def populate_process_table(self, processes):
        processes = sorted(processes, key=lambda item: item.get('cpu_percent', 0), reverse=True)[:25]
        self.process_table.setRowCount(len(processes))
        if not processes:
            self.process_table.setRowCount(1); empty_item = QTableWidgetItem("No active processes..."); self.process_table.setItem(0, 0, empty_item); self.process_table.setSpan(0, 0, 1, 5); return
        for row, proc in enumerate(processes):
            self.process_table.setItem(row, 0, QTableWidgetItem(str(proc.get('pid', ''))))
            self.process_table.setItem(row, 1, QTableWidgetItem(proc.get('name', '')))
            self.process_table.setItem(row, 2, QTableWidgetItem(f"{proc.get('cpu_percent', 0.0):.1f}"))
            self.process_table.setItem(row, 3, QTableWidgetItem(f"{proc.get('memory_percent', 0.0):.1f}"))
            kill_button = QPushButton("✕ Kill"); kill_button.setObjectName("KillProcessButton"); kill_button.setFixedHeight(26)
            kill_button.clicked.connect(lambda checked, pid=proc.get('pid'): self.kill_process(pid))
            self.process_table.setCellWidget(row, 4, kill_button)
    def kill_process(self, pid):
        try: proc = psutil.Process(pid); proc.terminate(); proc.wait(timeout=2); QMessageBox.information(self, "Process Control", f"PID {pid} terminated.")
        except Exception as exc: QMessageBox.warning(self, "Process Control", f"Failed: {exc}")

    # --- Title Bar & Sidebar ---
    def init_custom_title_bar(self, parent_layout):
        self.title_bar = QFrame(); self.title_bar.setObjectName("CustomTitleBar")
        title_layout = QHBoxLayout(self.title_bar); title_layout.setContentsMargins(15, 6, 12, 6); title_layout.setSpacing(8)
        window_icon_label = ColorPreservingLabel(self.logo_icon_path); window_icon_label.setFixedSize(20, 20); title_layout.addWidget(window_icon_label)
        window_title = QLabel("Grimoire Master OS Shell Extension"); window_title.setStyleSheet("color: #a397bf; font-family: 'Segoe UI'; font-weight: bold; font-size: 11px;"); title_layout.addWidget(window_title); title_layout.addStretch()
        btn_min = QPushButton("−"); btn_min.setObjectName("TitleMinButton"); btn_min.setFixedSize(28, 24); btn_min.clicked.connect(self.showMinimized); title_layout.addWidget(btn_min)
        btn_max = QPushButton("□"); btn_max.setObjectName("TitleMaxButton"); btn_max.setFixedSize(28, 24); btn_max.clicked.connect(self.toggle_maximize); title_layout.addWidget(btn_max)
        btn_close = QPushButton("✕"); btn_close.setObjectName("TitleCloseButton"); btn_close.setFixedSize(28, 24); btn_close.clicked.connect(self.close); title_layout.addWidget(btn_close)
        parent_layout.addWidget(self.title_bar)

    def init_sidebar(self, parent_layout):
        self.sidebar_frame = QFrame(); self.sidebar_frame.setObjectName("SidebarDock"); self.sidebar_frame.setFixedWidth(60)
        sidebar_layout = QVBoxLayout(self.sidebar_frame); sidebar_layout.setContentsMargins(8, 20, 8, 20); sidebar_layout.setSpacing(12)
        logo_container = QWidget(); logo_layout = QVBoxLayout(logo_container); logo_layout.setContentsMargins(0, 0, 0, 16)
        self.logo_icon_label = ColorPreservingLabel(self.logo_icon_path); self.logo_icon_label.setFixedSize(44, 44)
        logo_layout.addWidget(self.logo_icon_label, alignment=Qt.AlignmentFlag.AlignCenter); sidebar_layout.addWidget(logo_container)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setStyleSheet("color: #1f1833;"); sep.setFixedHeight(1); sidebar_layout.addWidget(sep)
        self.nav_buttons = []
        modules = [("assets/0.png", "Dashboard", 0), ("assets/1.png", "File Alchemy", 1), ("assets/2.png", "Visual Alchemy", 2), ("assets/3.png", "Deployment", 3), ("assets/4.png", "Task Viewer", 4), ("assets/5.png", "Arcane Tuning", 5)]
        for icon_path, name, index in modules:
            btn = GrimoireNavButton(icon_path, name, index, compact=True)
            if index == 0: btn.setChecked(True)
            btn.clicked.connect(self.switch_workspace_view); sidebar_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignHCenter); self.nav_buttons.append(btn)
        sidebar_layout.addStretch()
        parent_layout.addWidget(self.sidebar_frame, stretch=0)

    def switch_workspace_view(self, index):
        self.workspace_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons): btn.setChecked(i == index)

    # --- Status Bar ---
    def init_status_bar(self, parent_layout):
        self.status_bar = QFrame(); self.status_bar.setObjectName("StatusBar")
        status_layout = QHBoxLayout(self.status_bar); status_layout.setContentsMargins(16, 4, 16, 4); status_layout.setSpacing(16)
        status_dot = QLabel("●"); status_dot.setStyleSheet("color: #61ffcf; font-size: 10px;"); status_layout.addWidget(status_dot)
        status_lbl = QLabel("Grimoire Shell Active"); status_lbl.setStyleSheet("color: #645585; font-size: 10px;"); status_layout.addWidget(status_lbl); status_layout.addStretch()
        self.status_cpu_lbl = QLabel("CPU --%"); self.status_cpu_lbl.setStyleSheet("color: #7b61ff; font-size: 10px; font-family: 'Consolas'; font-weight: bold;"); status_layout.addWidget(self.status_cpu_lbl)
        self.status_mem_lbl = QLabel("MEM --%"); self.status_mem_lbl.setStyleSheet("color: #61ffcf; font-size: 10px; font-family: 'Consolas'; font-weight: bold;"); status_layout.addWidget(self.status_mem_lbl); status_layout.addStretch()
        self.status_time_lbl = QLabel("--:--:--"); self.status_time_lbl.setStyleSheet("color: #4a3e63; font-size: 10px; font-family: 'Consolas';"); status_layout.addWidget(self.status_time_lbl)
        parent_layout.addWidget(self.status_bar)

    # --- Async Worker & Helpers ---
    def cast_asynchronously(self, target_function, *args):
        # Cleaned up: Removed dead visualizer pulse trigger
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.display_output)
        self.worker.start()

    def display_output(self, text):
        if not text: return
        self.log_output(text)
        image_pattern = r"([A-Za-z]:[\\/][^\n\r]+?\.(?:png|jpg|jpeg|bmp|gif))"
        matches = re.findall(image_pattern, text, flags=re.IGNORECASE)
        for match in matches:
            normalized = os.path.normpath(match.strip('"'))
            if os.path.exists(normalized):
                self.handle_image_input(normalized)
                break

    def log_output(self, message):
        if hasattr(self, 'status_log'):
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.status_log.append(f"[{timestamp}] {message}")
            scrollbar = self.status_log.verticalScrollBar()
            if scrollbar is not None: scrollbar.setValue(scrollbar.maximum())

    def browse_for_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)")
        if file_path: self.handle_image_input(file_path)

    def handle_image_input(self, path):
        if not os.path.exists(path): self.log_output(f"✗ File not found: {path}"); return
        self.asset_state["path"] = path; self.current_image_path = path
        try:
            self.current_image = Image.open(path); self.edited_image = self.current_image.copy()
            self.log_output(f"✓ Image loaded: {os.path.basename(path)}")
        except Exception as e: self.log_output(f"✗ Error loading image: {e}"); return
        self.refresh_preview_view()
        if hasattr(self, 'txt_img_path'): self.txt_img_path.setText(path)

    def refresh_preview_view(self):
        if not hasattr(self, 'preview_window') or self.edited_image is None: return
        img_byte_arr = io.BytesIO(); self.edited_image.save(img_byte_arr, format='PNG'); img_byte_arr.seek(0)
        pixmap = QPixmap(); pixmap.loadFromData(img_byte_arr.getvalue())
        self.preview_window.setPixmap(pixmap.scaled(self.preview_window.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def save_current_image(self):
        if self.edited_image is None: QMessageBox.warning(self, "Save Error", "No image to save."); return
        default_name = "edited_image.png"
        if self.current_image_path:
            name, ext = os.path.splitext(os.path.basename(self.current_image_path)); default_name = f"{name}_edited.png"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Edited Image", default_name, "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp)")
        if file_path:
            try:
                ext = os.path.splitext(file_path)[1].lower()
                format_map = {'.png': 'PNG', '.jpg': 'JPEG', '.jpeg': 'JPEG', '.bmp': 'BMP'}
                save_format = format_map.get(ext, 'PNG')
                if save_format == 'JPEG' and self.edited_image.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', self.edited_image.size, (255, 255, 255))
                    if self.edited_image.mode == 'P': self.edited_image = self.edited_image.convert('RGBA')
                    background.paste(self.edited_image, mask=self.edited_image.split()[-1] if self.edited_image.mode == 'RGBA' else None)
                    self.edited_image = background
                self.edited_image.save(file_path, format=save_format)
                self.log_output(f"✓ Image saved: {os.path.basename(file_path)}")
            except Exception as e: QMessageBox.critical(self, "Save Error", f"Failed: {e}")

    def reset_image(self):
        if self.current_image is None: return
        self.edited_image = self.current_image.copy(); self.refresh_preview_view(); self.log_output("✓ Reset to original")

    # --- PIL Image Editing Methods ---
    def apply_grayscale(self):
        if self.edited_image is None: return
        self.edited_image = self.edited_image.convert('L').convert('RGB'); self.refresh_preview_view()
    def apply_sepia(self):
        if self.edited_image is None: return
        img_array = np.array(self.edited_image)
        sepia_matrix = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
        sepia_array = np.clip(np.dot(img_array[..., :3], sepia_matrix.T), 0, 255).astype(np.uint8)
        self.edited_image = Image.fromarray(sepia_array); self.refresh_preview_view()
    def apply_blur(self, radius=2):
        if self.edited_image is None: return
        self.edited_image = self.edited_image.filter(ImageFilter.GaussianBlur(radius=radius)); self.refresh_preview_view()
    def apply_sharpen(self, factor=1.5):
        if self.edited_image is None: return
        enhancer = ImageEnhance.Sharpness(self.edited_image); self.edited_image = enhancer.enhance(factor); self.refresh_preview_view()
    def adjust_brightness(self, value):
        if self.edited_image is None: return
        enhancer = ImageEnhance.Brightness(self.edited_image); self.edited_image = enhancer.enhance(value / 100.0); self.refresh_preview_view()
    def adjust_contrast(self, value):
        if self.edited_image is None: return
        enhancer = ImageEnhance.Contrast(self.edited_image); self.edited_image = enhancer.enhance(value / 100.0); self.refresh_preview_view()
    def rotate_image(self, angle):
        if self.edited_image is None: return
        self.edited_image = self.edited_image.rotate(-angle, expand=True); self.refresh_preview_view()
    def flip_image(self, direction='horizontal'):
        if self.edited_image is None: return
        self.edited_image = ImageOps.mirror(self.edited_image) if direction == 'horizontal' else ImageOps.flip(self.edited_image)
        self.refresh_preview_view()
    def resize_image(self, width, height, maintain_aspect=True):
        if self.edited_image is None: return
        if maintain_aspect: self.edited_image.thumbnail((width, height))
        else: self.edited_image = self.edited_image.resize((width, height), Image.Resampling.LANCZOS)
        self.refresh_preview_view()
    def invert_colors(self):
        if self.edited_image is None: return
        self.edited_image = ImageOps.invert(self.edited_image.convert('RGB')); self.refresh_preview_view()

    # --- AI Execution Methods ---
    def _get_output_path(self, suffix):
        if not self.current_image_path: return None
        name, ext = os.path.splitext(self.current_image_path); return f"{name}_{suffix}{ext}"

    def run_subject_isolator(self):
        if not self.design_suite or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        output_path = self._get_output_path("isolated.png")
        def task(): return self.design_suite.subject_isolator(self.current_image_path, output_path)
        self.cast_asynchronously(task)

    def run_upscaler(self):
        if not self.design_suite or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        output_path = self._get_output_path("upscaled.png")
        def task(): return self.design_suite.super_resolution_upscaler(self.current_image_path, output_path, scale_factor=self.spin_upscale.value())
        self.cast_asynchronously(task)

    def run_seamless_tiler(self):
        if not self.design_suite or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        output_path = self._get_output_path("seamless.png")
        def task(): return self.design_suite.seamless_texture_tiler(self.current_image_path, output_path)
        self.cast_asynchronously(task)

    def run_palette_harmonizer(self):
        if not self.design_suite or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        def task(): return self.design_suite.palette_harmonizer(self.current_image_path, num_colors=5)
        self.worker = ArcaneWorker(task)
        self.worker.manifest_complete.connect(lambda text: self.lbl_palette_output.setText(text))
        self.worker.start()

    def run_style_transfer(self):
        if not self.design_suite or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        output_path = self._get_output_path("styled.png")
        def task(): return self.design_suite.style_transfer_refiner(self.current_image_path, self.txt_style_prompt.text(), output_path)
        self.cast_asynchronously(task)

    def run_context_inpaint(self):
        if not self.design_suite or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        mask_path, _ = QFileDialog.getOpenFileName(self, "Select Black/White Mask Image", "", "Images (*.png *.jpg)")
        if not mask_path: return
        output_path = self._get_output_path("inpainted.png")
        def task(): return self.design_suite.context_aware_inpaint(self.current_image_path, mask_path, self.txt_inpaint_prompt.text(), output_path)
        self.cast_asynchronously(task)

    def run_pbr_maps(self):
        if not self.advanced_extensions or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load an image first."); return
        output_path = self._get_output_path("pbr")
        def task(): return self.advanced_extensions.generate_pbr_maps(self.current_image_path, output_path)
        self.cast_asynchronously(task)

    def browse_background_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Background Image", "", "Images (*.png *.jpg *.jpeg)")
        if file_path: self.txt_bg_path.setText(file_path)

    def run_composite_layers(self):
        if not self.advanced_extensions or not self.current_image_path: QMessageBox.warning(self, "No Image", "Load foreground image first."); return
        bg_path = self.txt_bg_path.text()
        if not bg_path or not os.path.exists(bg_path): QMessageBox.warning(self, "No Background", "Select a background image first."); return
        def task(): return self.advanced_extensions.composite_layers(self.current_image_path, bg_path, position=(0, 0))
        self.cast_asynchronously(task)

    # --- Helper Cards ---
    def create_card(self, title, subtext="Quick Actions", icon=""):
        card_frame = QFrame(); card_frame.setObjectName("DashboardCard")
        card_layout = QVBoxLayout(card_frame); card_layout.setContentsMargins(20, 18, 20, 18); card_layout.setSpacing(14)
        header_layout = QHBoxLayout()
        if icon: icon_lbl = QLabel(icon); icon_lbl.setStyleSheet("font-size: 18px; background: transparent;"); header_layout.addWidget(icon_lbl)
        title_block = QVBoxLayout(); title_block.setSpacing(2)
        title_lbl = QLabel(title); title_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #ffffff; font-family: 'Segoe UI'; background: transparent;"); title_block.addWidget(title_lbl)
        sub_lbl = QLabel(subtext); sub_lbl.setStyleSheet("font-size: 9px; color: #645585; font-family: 'Segoe UI'; background: transparent;"); title_block.addWidget(sub_lbl)
        header_layout.addLayout(title_block); header_layout.addStretch(); card_layout.addLayout(header_layout)
        sep = QFrame(); sep.setFrameShape(QFrame.Shape.HLine); sep.setStyleSheet("background-color: #251d3a; max-height: 1px;"); sep.setFixedHeight(1); card_layout.addWidget(sep)
        return card_frame, card_layout

    # --- Theme ---
    def apply_theme(self):
        self.setStyleSheet("""
            QWidget#MainContainer { background-color: #0b0813; border: 1px solid #1f1833; border-radius: 12px; }
            QFrame#CustomTitleBar { background-color: #0b0813; border-top-left-radius: 12px; border-top-right-radius: 12px; border-bottom: 1px solid #140f24; }
            QFrame#SidebarDock { background-color: #120e1f; border-right: 1px solid #1f1833; border-bottom-left-radius: 11px; }
            QPushButton#ActionButton { background-color: #211936; color: #7b61ff; font-weight: 600; border: 1px solid #322652; border-radius: 8px; padding: 8px 16px; font-family: 'Segoe UI'; font-size: 11px; }
            QPushButton#ActionButton:hover { background-color: #7b61ff; color: #ffffff; border-color: #7b61ff; }
            QPushButton#SecondaryButton { background-color: #1e1730; color: #8c7fa6; font-weight: 500; border: 1px solid #2d2349; border-radius: 6px; padding: 6px 12px; font-family: 'Segoe UI'; font-size: 10px; }
            QPushButton#SecondaryButton:hover { background-color: #251d3a; color: #a397bf; border-color: #7b61ff; }
            QPushButton#TitleMinButton, QPushButton#TitleMaxButton, QPushButton#TitleCloseButton { background-color: transparent; color: #8c7fa6; border: none; border-radius: 4px; padding: 4px; font-family: 'Segoe UI'; font-size: 14px; font-weight: bold; }
            QPushButton#TitleMinButton:hover, QPushButton#TitleMaxButton:hover { background-color: #2d2349; color: #7b61ff; }
            QPushButton#TitleCloseButton:hover { background-color: #ff4444; color: #ffffff; }
            QTabWidget::panel { background-color: #0b0813; border: none; }
            QLabel { color: #a397bf; font-family: 'Segoe UI'; font-size: 11px; background: transparent; }
            QLineEdit { background-color: #1e1730; color: #61ffcf; border: 1px solid #2d2349; border-radius: 6px; padding: 8px 12px; font-family: 'Consolas'; font-size: 11px; }
            QLineEdit:focus { border-color: #7b61ff; }
            QSpinBox { background-color: #1e1730; color: #61ffcf; border: 1px solid #2d2349; border-radius: 4px; padding: 4px; font-family: 'Consolas'; font-size: 10px; }
            QCheckBox { color: #c9bedf; font-family: 'Segoe UI'; font-size: 11px; background: transparent; spacing: 6px; }
            QCheckBox::indicator { width: 14px; height: 14px; border-radius: 3px; border: 1px solid #322652; background: #1e1730; }
            QCheckBox::indicator:checked { background: #7b61ff; border-color: #7b61ff; }
            QTableWidget { background-color: #0e0a19; color: #c9bedf; border: 1px solid #1f1833; border-radius: 8px; gridline-color: #1a1430; font-size: 10px; }
            QHeaderView::section { background-color: #171226; color: #7b61ff; padding: 8px; border: none; font-weight: bold; font-size: 10px; font-family: 'Segoe UI'; }
            
            /* Custom Scrollbars */
            QScrollArea { background-color: transparent; border: none; }
            QScrollBar:vertical { border: none; background: #0b0813; width: 8px; margin: 0; border-radius: 4px; }
            QScrollBar::handle:vertical { background: #2d2349; min-height: 30px; border-radius: 4px; margin: 2px; }
            QScrollBar::handle:vertical:hover { background: #7b61ff; }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }
        """)
