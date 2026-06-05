import sys
import os
import re
import io
import psutil
import numpy as np
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QCheckBox, QTabWidget,
    QLineEdit, QTextEdit, QFrame, QSlider, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QScrollArea, QGroupBox, QFileDialog, QSizePolicy,
    QSpinBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QTimer, QRect
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont, QIcon

# ==========================================
# HEAVY AI DEPENDENCIES (Safe Import Wrapper)
# ==========================================
HEAVY_DEPS_AVAILABLE = False
try:
    import cv2
    import torch
    from PIL import Image, ImageOps, ImageFilter, ImageEnhance
    from rembg import remove
    from diffusers import StableDiffusionInpaintPipeline, StableDiffusionXLImg2ImgPipeline
    HEAVY_DEPS_AVAILABLE = True
except ImportError:
    print("Warning: Heavy AI dependencies missing. Run: pip install opencv-python torch diffusers rembg")

if HEAVY_DEPS_AVAILABLE:
    # ==========================================
    # DESIGN SUITE (From code1.txt)
    # ==========================================
    class DesignSuite:
        def __init__(self, hf_auth_token=None):
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.token = hf_auth_token
            print(f"DesignSuite initialized running on: {self.device.upper()}")

        def subject_isolator(self, input_image_path, output_image_path):
            print("[Processing] Isolating subject and removing background...")
            with open(input_image_path, 'rb') as i:
                input_data = i.read()
            output_data = remove(input_data)
            with open(output_image_path, 'wb') as o:
                o.write(output_data)
            print(f"[Success] Isolated image saved to {output_image_path}")            return output_image_path

        def context_aware_inpaint(self, image_path, mask_path, prompt, output_path):
            print("[Processing] Initializing Neural Inpainting Pipeline...")
            pipe = StableDiffusionInpaintPipeline.from_pretrained(
                "runwayml/stable-diffusion-inpainting",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            # VRAM Optimization for 8GB cards
            pipe.enable_attention_slicing() 
            init_image = Image.open(image_path).convert("RGB").resize((512, 512))
            mask_image = Image.open(mask_path).convert("RGB").resize((512, 512))
            image = pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]
            image.save(output_path)
            print(f"[Success] Inpainted asset saved to {output_path}")
            return output_path

        def super_resolution_upscaler(self, image_path, output_path, scale_factor=4):
            print(f"[Processing] Upscaling image by {scale_factor}x...")
            img = cv2.imread(image_path)
            if img is None: raise Exception("Failed to load image for upscaling.")
            width = int(img.shape[1] * scale_factor)
            height = int(img.shape[0] * scale_factor)
            dim = (width, height)
            upscaled = cv2.resize(img, dim, interpolation=cv2.INTER_CUBIC)
            cv2.imwrite(output_path, upscaled)
            print(f"[Success] High-res asset saved to {output_path}")
            return output_path

        def palette_harmonizer(self, image_path, num_colors=5):
            print("[Processing] Analyzing color frequencies...")
            img = Image.open(image_path).convert('RGB')
            img = img.resize((50, 50))
            colors = img.getcolors(2500)
            sorted_colors = sorted(colors, key=lambda x: x[0], reverse=True)
            dominant_colors = sorted_colors[:num_colors]
            hex_palette = []
            for count, rgb in dominant_colors:
                hex_code = '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])
                hex_palette.append(hex_code)
            print(f"[Success] Extracted Palette: {hex_palette}")
            return ", ".join(hex_palette)

        def style_transfer_refiner(self, base_image_path, style_prompt, output_path):
            print(f"[Processing] Remapping visual DNA to style: '{style_prompt}'...")
            pipe = StableDiffusionXLImg2ImgPipeline.from_pretrained(
                "stabilityai/stable-diffusion-xl-refiner-1.0",
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            ).to(self.device)
            # VRAM Optimization for 8GB cards            pipe.enable_attention_slicing()
            init_image = Image.open(base_image_path).convert("RGB").resize((768, 768))
            image = pipe(prompt=style_prompt, image=init_image, strength=0.3).images[0]
            image.save(output_path)
            print(f"[Success] Styled asset saved to {output_path}")
            return output_path

        def seamless_texture_tiler(self, image_path, output_path):
            print("[Processing] Transforming asset into tileable pattern...")
            img = Image.open(image_path)
            w, h = img.size
            flipped_h = ImageOps.mirror(img)
            flipped_v = ImageOps.flip(img)
            flipped_both = ImageOps.flip(flipped_h)
            seamless = Image.new('RGB', (w * 2, h * 2))
            seamless.paste(img, (0, 0))
            seamless.paste(flipped_h, (w, 0))
            seamless.paste(flipped_v, (0, h))
            seamless.paste(flipped_both, (w, h))
            seamless.save(output_path)
            print(f"[Success] Tileable pattern saved to {output_path}")
            return output_path

    # ==========================================
    # ADVANCED DESIGN EXTENSIONS (From expandedproductioncore.txt)
    # NOTE: StarVector 8B (SVG) has been removed to save VRAM.
    # ==========================================
    class AdvancedDesignExtensions:
        def __init__(self, device="cuda"):
            self.device = device if torch.cuda.is_available() else "cpu"
            print(f"AdvancedDesignExtensions initialized on: {self.device.upper()}")

        def generate_pbr_maps(self, diffuse_image_path, prefix_output_path):
            print("[Processing] Generating physical PBR surface coordinates...")
            gray = cv2.imread(diffuse_image_path, cv2.IMREAD_GRAYSCALE)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            normal_map = np.zeros((gray.shape[0], gray.shape[1], 3), dtype=np.uint8)
            dx = sobelx * 2.0
            dy = sobely * 2.0
            dz = np.ones_like(gray) * 255.0
            norm = np.sqrt(dx**2 + dy**2 + dz**2)
            normal_map[..., 0] = ((dx / norm) * 127.5 + 127.5).astype(np.uint8)
            normal_map[..., 1] = ((dy / norm) * 127.5 + 127.5).astype(np.uint8)
            normal_map[..., 2] = ((dz / norm) * 255.0).astype(np.uint8)
            cv2.imwrite(f"{prefix_output_path}_normal.png", normal_map)
            cv2.imwrite(f"{prefix_output_path}_displacement.png", gray)
            print(f"[Success] Exported print-ready PBR maps to: {prefix_output_path}_normal.png")
            return f"{prefix_output_path}_normal.png"
        def composite_layers(self, foreground_png, background_jpg, position=(0,0)):
            print("[Processing] Intersecting alpha mask transparency layers...")
            bg = Image.open(background_jpg).convert("RGBA")
            fg = Image.open(foreground_png).convert("RGBA")
            bg.paste(fg, position, fg)
            final_rgb = bg.convert("RGB")
            # Fixed hardcoded path to prevent FileNotFoundError
            output_path = os.path.join(os.path.dirname(foreground_png), "final_studio_composite.jpg")
            final_rgb.save(output_path)
            print(f"[Success] Composited artwork layer layout flattened to: {output_path}")
            return output_path


# ==========================================
# EXISTING PYQT6 UI CLASSES
# ==========================================
class ColorPreservingLabel(QLabel):
    def __init__(self, image_path=None, parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.pixmap_data = None
        if image_path and image_path.endswith(('.png', '.jpg')):
            self.pixmap_data = QPixmap(image_path)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def paintEvent(self, event):
        if self.pixmap_data and not self.pixmap_data.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            target_size = self.size()
            scaled = self.pixmap_data.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            x = (target_size.width() - scaled.width()) // 2
            y = (target_size.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)
        else:
            super().paintEvent(event)

class PerformanceChart(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ChartCard")
        self.cpu_history = [0] * 60
        self.memory_history = [0] * 60
        self.max_points = 60
        self.setMinimumHeight(200)

    def update_data(self, cpu, memory):
        self.cpu_history.pop(0); self.cpu_history.append(cpu)
        self.memory_history.pop(0); self.memory_history.append(memory)        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#171226"))
        painter.setPen(QPen(QColor("#251d3a"), 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 12, 12)
        margin = 40
        chart_rect = self.rect().adjusted(margin, 30, -margin, -30)
        if chart_rect.width() <= 0 or chart_rect.height() <= 0: return
        painter.setPen(QPen(QColor("#2d2349"), 1))
        for i in range(5):
            y = chart_rect.top() + (chart_rect.height() * i // 4)
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)
            painter.setPen(QPen(QColor("#645585")))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(margin - 30, y - 5, 25, 15, Qt.AlignmentFlag.AlignRight, str(100 - (i * 25)) + "%")
            painter.setPen(QPen(QColor("#2d2349"), 1))
        painter.setPen(QPen(QColor("#7b61ff"), 2))
        points = [QPoint(int(chart_rect.left() + (i * chart_rect.width() // (self.max_points - 1))), int(chart_rect.bottom() - (v * chart_rect.height() / 100))) for i, v in enumerate(self.cpu_history)]
        for i in range(len(points) - 1): painter.drawLine(points[i], points[i + 1])
        painter.setPen(QPen(QColor("#61ffcf"), 2))
        points = [QPoint(int(chart_rect.left() + (i * chart_rect.width() // (self.max_points - 1))), int(chart_rect.bottom() - (v * chart_rect.height() / 100))) for i, v in enumerate(self.memory_history)]
        for i in range(len(points) - 1): painter.drawLine(points[i], points[i + 1])

class ArcaneWorker(QThread):
    manifest_complete = pyqtSignal(str)
    def __init__(self, task_function, *args):
        super().__init__(); self.task_function = task_function; self.args = args
    def run(self):
        try:
            output = self.task_function(*self.args)
            self.manifest_complete.emit(str(output) if output else "Sequence completed smoothly.")
        except Exception as e:
            self.manifest_complete.emit(f"Sequence Error: {e}")

class TelemetrySampler(QThread):
    system_metrics_updated = pyqtSignal(float, float, float)
    internal_process_updated = pyqtSignal(dict)
    def __init__(self, poll_interval=1.5, parent=None):
        super().__init__(parent); self.poll_interval = poll_interval; self.running = True
    def gather_internal_process_stats(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try: processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return {"processes": processes, "process_count": len(processes)}
    def run(self):
        while self.running:            try:
                cpu = psutil.cpu_percent(interval=0.5)
                memory = psutil.virtual_memory(); swap = psutil.swap_memory()
                internal_data = self.gather_internal_process_stats()
                self.system_metrics_updated.emit(cpu, memory.percent, swap.percent)
                self.internal_process_updated.emit(internal_data)
            except Exception: pass
            self.msleep(int(self.poll_interval * 1000))
    def stop(self): self.running = False

class GrimoireNavButton(QFrame):
    clicked = pyqtSignal(int)
    def __init__(self, icon_str, name_str, index, compact=False, parent=None):
        super().__init__(parent)
        self.index = index; self.is_checked = False; self.compact = compact
        self.setObjectName("NavButtonContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        layout = QHBoxLayout(self); layout.setContentsMargins(8, 8, 8, 8); layout.setSpacing(8)
        self.icon_label = ColorPreservingLabel(); self.icon_label.setStyleSheet("background: transparent;")
        if icon_str.endswith('.png') or icon_str.endswith('.jpg'):
            self.icon_label.pixmap_data = QPixmap(icon_str); self.icon_label.setFixedSize(32 if compact else 24, 32 if compact else 24)
        else:
            self.icon_label.setText(icon_str); self.icon_label.setFixedSize(32 if compact else 24, 32 if compact else 24)
        layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.text_label = QLabel(name_str); self.text_label.setStyleSheet("font-family: 'Segoe UI'; font-weight: bold; font-size: 10px; background: transparent;")
        layout.addWidget(self.text_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        if compact: self.text_label.hide(); self.setMaximumWidth(48)
        else: self.text_label.hide()
        self.update_state_styling()

    def setChecked(self, checked):
        self.is_checked = checked
        if self.is_checked:
            self.text_label.show()
            if self.compact: self.setMaximumWidth(16777215)
        else:
            self.text_label.hide()
            if self.compact: self.setMaximumWidth(48)
        self.update_state_styling()

    def enterEvent(self, event):
        if self.compact: self.text_label.show(); self.setMaximumWidth(16777215)
        else: self.text_label.show()
        self.update_state_styling(hover=True); super().enterEvent(event)

    def leaveEvent(self, event):
        if self.compact:
            if not self.is_checked: self.text_label.hide(); self.setMaximumWidth(48)
        elif not self.is_checked: self.text_label.hide()        self.update_state_styling(hover=False); super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton: self.clicked.emit(self.index); event.accept()

    def update_state_styling(self, hover=False):
        if self.is_checked:
            self.setStyleSheet("QFrame#NavButtonContainer { background-color: #241b3f; border-radius: 8px; border-left: 3px solid #7b61ff; } QLabel { color: #7b61ff; }")
        elif hover:
            self.setStyleSheet("QFrame#NavButtonContainer { background-color: #1a142e; border-radius: 8px; border-left: 3px solid #4a3e63; } QLabel { color: #ffffff; }")
        else:
            self.setStyleSheet("QFrame#NavButtonContainer { background-color: transparent; border-radius: 8px; border-left: 3px solid transparent; } QLabel { color: #8c7fa6; }")

class ArcaneSystemVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180); self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.angle = 0; self.pulse = 0; self.pulse_growing = True; self.is_active = False; self.load_intensity = 0.0
        self.internal_data = {"processes": [], "process_count": 0}
        self.timer = QTimer(self); self.timer.timeout.connect(self.update_animation); self.timer.start(16)

    def set_internal_data(self, internal_data):
        if internal_data is None: internal_data = {"processes": [], "process_count": 0}
        self.internal_data = internal_data
        self.load_intensity = max((item.get('cpu_percent', 0.0) for item in self.internal_data.get('processes', [])), default=0.0)
        self.update()

    def trigger_pulse(self): self.is_active = True; self.pulse = 30

    def update_animation(self):
        speed = 1 + (self.load_intensity / 20); self.angle = (self.angle + int(speed)) % 360
        if self.pulse_growing:
            self.pulse += 0.2
            if self.pulse >= 12: self.pulse_growing = False
        else:
            self.pulse -= 0.2
            if self.pulse <= 2: self.pulse_growing = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self); painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect().adjusted(4, 4, -4, -4); painter.fillRect(rect, QColor("#120e1f"))
        border_pen = QPen(QColor("#1f1833")); border_pen.setWidth(2); painter.setPen(border_pen); painter.setBrush(Qt.BrushStyle.NoBrush); painter.drawRoundedRect(rect, 12, 12)
        inner = rect.adjusted(10, 10, -10, -10); painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(QColor("#1e1730")); painter.drawRoundedRect(inner, 10, 10)
        painter.setPen(QColor("#a397bf")); painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold)); painter.drawText(inner.left() + 12, inner.top() + 22, "SYSTEM TELEMETRY MATRIX")
        processes = self.internal_data.get("processes", []); process_count = self.internal_data.get("process_count", len(processes))
        top_cpu = 0.0; top_name = "N/A"
        if processes:
            top = max(processes, key=lambda item: item.get('cpu_percent', 0.0)); top_cpu = top.get('cpu_percent', 0.0); top_name = top.get('name', '<unknown>')
        painter.setPen(QColor("#a397bf")); painter.setFont(QFont("Segoe UI", 8))        painter.drawText(inner.left() + 12, inner.top() + 100, f"Tracked Process Count: {process_count}")
        painter.drawText(inner.left() + 12, inner.top() + 116, f"Most Active: {top_name} ({top_cpu:.1f}% CPU)")
        pulse_radius = 14 + int(min(40, max(0, top_cpu / 2)))
        if self.is_active or top_cpu > 5:
            pulse_color = QColor(123, 97, 255, 120 if top_cpu > 0 else 70); painter.setPen(Qt.PenStyle.NoPen); painter.setBrush(pulse_color)
            painter.drawEllipse(inner.right() - 34, inner.top() + 12, pulse_radius, pulse_radius)


# ==========================================
# MAIN APPLICATION CLASS
# ==========================================
class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.telemetry_thread = None
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.resize(1200, 850); self.setMinimumSize(900, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.logo_icon_path = os.path.join(os.path.dirname(__file__), "grimoire_logo.png")
        self.logo_text_path = os.path.join(os.path.dirname(__file__), "grimoire_text.png")

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
            except Exception as e:
                print(f"AI Suites failed to initialize: {e}")

        self.main_container = QWidget(); self.main_container.setObjectName("MainContainer"); self.setCentralWidget(self.main_container)
        master_vertical = QVBoxLayout(self.main_container); master_vertical.setContentsMargins(0, 0, 0, 0); master_vertical.setSpacing(0)
        self.init_custom_title_bar(master_vertical)
        content_layout = QHBoxLayout(); content_layout.setContentsMargins(0, 0, 0, 0); content_layout.setSpacing(0); master_vertical.addLayout(content_layout)
        self.init_sidebar(content_layout)
        self.workspace_stack = QTabWidget()
        if self.workspace_stack.tabBar() is not None: self.workspace_stack.tabBar().hide()
        content_layout.addWidget(self.workspace_stack, stretch=1)
        self.right_panel_frame = QFrame(); self.right_panel_frame.setFixedWidth(0); self.right_panel_frame.hide(); content_layout.addWidget(self.right_panel_frame, stretch=0)

        self.init_core_tab(); self.init_alchemy_tab(); self.init_visual_alchemy_tab()
        self.init_deployment_architect_tab(); self.init_task_viewer_tab(); self.init_tuning_tab()        self.workspace_stack.currentChanged.connect(self.toggle_right_panel_visibility)
        self.init_status_bar(master_vertical); self.apply_theme(); self.right_panel_frame.hide()

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

    # --- Window Dragging/Resizing (Omitted for brevity, keep your existing code) ---
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
        elif x > w - edge_size and y < edge_size: return 2        elif x < edge_size and y > h - edge_size: return 3
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
        if data is None: data = {"processes": [], "process_count": 0}
        if hasattr(self, 'visualizer'): self.visualizer.set_internal_data(data)
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
    def toggle_right_panel_visibility(self, index): self.right_panel_frame.hide()

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
        if hasattr(self, 'visualizer'): self.visualizer.trigger_pulse()
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.display_output)
        self.worker.start()
    def display_output(self, text):
        if not text: return
        self.log_output(text)
        # Check if output contains an image path to update preview
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

    def update_preview_from_pil(self): self.refresh_preview_view()

    def save_current_image(self):
        if self.edited_image is None: QMessageBox.warning(self, "Save Error", "No image to save."); return
        default_name = "edited_image.png"
        if self.current_image_path:
            name, ext = os.path.splitext(os.path.basename(self.current_image_path)); default_name = f"{name}_edited.png"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Edited Image", default_name, "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp)")
        if file_path:
            try:
                ext = os.path.splitext(file_path)[1].lower()                format_map = {'.png': 'PNG', '.jpg': 'JPEG', '.jpeg': 'JPEG', '.bmp': 'BMP'}
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
        self.edited_image = self.current_image.copy(); self.update_preview_from_pil(); self.log_output("✓ Reset to original")

    # --- PIL Image Editing Methods ---
    def apply_grayscale(self):
        if self.edited_image is None: return
        self.edited_image = self.edited_image.convert('L').convert('RGB'); self.update_preview_from_pil()
    def apply_sepia(self):
        if self.edited_image is None: return
        img_array = np.array(self.edited_image)
        sepia_matrix = np.array([[0.393, 0.769, 0.189], [0.349, 0.686, 0.168], [0.272, 0.534, 0.131]])
        sepia_array = np.clip(np.dot(img_array[..., :3], sepia_matrix.T), 0, 255).astype(np.uint8)
        self.edited_image = Image.fromarray(sepia_array); self.update_preview_from_pil()
    def apply_blur(self, radius=2):
        if self.edited_image is None: return
        self.edited_image = self.edited_image.filter(ImageFilter.GaussianBlur(radius=radius)); self.update_preview_from_pil()
    def apply_sharpen(self, factor=1.5):
        if self.edited_image is None: return
        enhancer = ImageEnhance.Sharpness(self.edited_image); self.edited_image = enhancer.enhance(factor); self.update_preview_from_pil()
    def adjust_brightness(self, value):
        if self.edited_image is None: return
        enhancer = ImageEnhance.Brightness(self.edited_image); self.edited_image = enhancer.enhance(value / 100.0); self.update_preview_from_pil()
    def adjust_contrast(self, value):
        if self.edited_image is None: return
        enhancer = ImageEnhance.Contrast(self.edited_image); self.edited_image = enhancer.enhance(value / 100.0); self.update_preview_from_pil()
    def rotate_image(self, angle):
        if self.edited_image is None: return
        self.edited_image = self.edited_image.rotate(-angle, expand=True); self.update_preview_from_pil()
    def flip_image(self, direction='horizontal'):
        if self.edited_image is None: return
        self.edited_image = ImageOps.mirror(self.edited_image) if direction == 'horizontal' else ImageOps.flip(self.edited_image)
        self.update_preview_from_pil()
    def resize_image(self, width, height, maintain_aspect=True):
        if self.edited_image is None: return
        if maintain_aspect: self.edited_image.thumbnail((width, height))
        else: self.edited_image = self.edited_image.resize((width, height), Image.Resampling.LANCZOS)
        self.update_preview_from_pil()
    def invert_colors(self):        if self.edited_image is None: return
        self.edited_image = ImageOps.invert(self.edited_image.convert('RGB')); self.update_preview_from_pil()

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
        output_path = self._get_output_path("pbr")        def task(): return self.advanced_extensions.generate_pbr_maps(self.current_image_path, output_path)
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

    # ==========================================
    # TAB INITIALIZATIONS
    # ==========================================
    def init_core_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        top_bar = QHBoxLayout()
        page_title = ColorPreservingLabel(self.logo_text_path); page_title.setFixedHeight(40)
        page_title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed) # FIXED LOGO SIZING
        top_bar.addWidget(page_title); top_bar.addStretch(); main_layout.addLayout(top_bar)
        stats_row = QHBoxLayout(); stats_row.setSpacing(12); self.dashboard_stat_labels = {}
        cards_data = [("CPU Usage", "cpu", "#7b61ff", "⚡"), ("Memory Usage", "memory", "#61ffcf", "🧠"), ("Storage Used", "storage", "#ff8c61", "💾"), ("Processes", "processes", "#ffd93d", "🔄")]
        for title, key, color, icon in cards_data:
            card = QFrame(); card.setObjectName("StatCard"); card.setMinimumHeight(120)
            card_layout = QVBoxLayout(card); card_layout.setContentsMargins(16, 12, 16, 12); card_layout.setSpacing(8)
            header = QHBoxLayout(); icon_lbl = QLabel(icon); icon_lbl.setStyleSheet("font-size: 16px; background: transparent;"); header.addWidget(icon_lbl)
            title_lbl = QLabel(title); title_lbl.setStyleSheet("color: #a397bf; font-size: 10px; background: transparent;"); header.addWidget(title_lbl); header.addStretch(); card_layout.addLayout(header)
            value_lbl = QLabel("0%"); value_lbl.setStyleSheet(f"color: {color}; font-size: 22px; font-weight: bold; background: transparent;"); card_layout.addWidget(value_lbl); self.dashboard_stat_labels[key] = value_lbl
            card_layout.addStretch(); card.setStyleSheet(f"QFrame#StatCard {{ background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 rgba(123, 97, 255, 30), stop:1 rgba(97, 255, 207, 10)); border: 1px solid #2d2349; border-radius: 12px; }}")
            stats_row.addWidget(card)
        main_layout.addLayout(stats_row)
        content_row = QHBoxLayout(); content_row.setSpacing(12)
        self.performance_chart = PerformanceChart(); chart_layout = QVBoxLayout(); chart_layout.addWidget(self.performance_chart, stretch=1)        chart_container = QFrame(); chart_container.setObjectName("ChartCard"); chart_container.setLayout(chart_layout); content_row.addWidget(chart_container, stretch=2)
        main_layout.addLayout(content_row, stretch=1)
        self.workspace_stack.addTab(page, "Dashboard")

    def init_alchemy_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        header = QHBoxLayout(); page_header = QLabel("🧪 FILE ALCHEMY"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); header.addWidget(page_header); header.addStretch(); main_layout.addLayout(header)
        card_dir, layout_dir = self.create_card("📁 Directory Sorting Vector", "Organize files by type, date, or custom rules", "")
        path_row = QHBoxLayout(); path_lbl = QLabel("Target Path:"); path_row.addWidget(path_lbl)
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads"); path_row.addWidget(self.txt_path, stretch=1)
        btn_browse_dir = QPushButton("📁 Browse"); btn_browse_dir.setFixedWidth(90); btn_browse_dir.setObjectName("ActionButton")
        btn_browse_dir.clicked.connect(lambda: self.txt_path.setText(QFileDialog.getExistingDirectory(self, "Select Folder"))); path_row.addWidget(btn_browse_dir); layout_dir.addLayout(path_row)
        btn_run_sort = QPushButton("️ Execute File Alchemy Sorting"); btn_run_sort.setObjectName("ActionButton"); layout_dir.addWidget(btn_run_sort)
        card_dir.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }"); main_layout.addWidget(card_dir); main_layout.addStretch()
        self.workspace_stack.addTab(page, "File Alchemy")

    def init_visual_alchemy_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        page_header = QLabel("👁️ VISUAL ALCHEMY"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI'; background: transparent;")
        main_layout.addWidget(page_header)
        content_row = QHBoxLayout(); content_row.setSpacing(16)
        
        # LEFT COLUMN
        left_column = QWidget(); left_layout = QVBoxLayout(left_column); left_layout.setContentsMargins(0, 0, 0, 0); left_layout.setSpacing(12)
        scroll = QScrollArea(); scroll.setWidgetResizable(True); scroll.setFrameShape(QFrame.Shape.NoFrame); scroll.setStyleSheet("background-color: transparent; border: none;")
        inner_widget = QWidget(); inner_widget.setStyleSheet("background-color: transparent;"); content_layout = QVBoxLayout(inner_widget); content_layout.setSpacing(12)
        
        group_style = """QGroupBox { color: #a397bf; font-weight: bold; border: 1px solid #251d3a; border-radius: 8px; margin-top: 8px; padding-top: 8px; background-color: #171226; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px 0 3px; }"""

        # 1. Image Loading
        group_load = QGroupBox("📂 Image Loading"); group_load.setStyleSheet(group_style); layout_load = QVBoxLayout(group_load); layout_load.setSpacing(10)
        path_row = QHBoxLayout(); path_row.addWidget(QLabel("Image Path:")); self.txt_img_path = QLineEdit(r"C:\Users\Public\Grimoire_Procedural_Logo.png"); path_row.addWidget(self.txt_img_path, stretch=1)
        btn_browse = QPushButton("📁 Browse"); btn_browse.setFixedWidth(90); btn_browse.setObjectName("ActionButton"); btn_browse.clicked.connect(self.browse_for_image); path_row.addWidget(btn_browse)
        layout_load.addLayout(path_row); content_layout.addWidget(group_load)

        # 2. Basic Transforms
        group_transform = QGroupBox("🔄 Basic Transforms"); group_transform.setStyleSheet(group_style); layout_transform = QVBoxLayout(group_transform); layout_transform.setSpacing(8)
        rotate_row = QHBoxLayout(); rotate_row.addWidget(QLabel("Rotate:")); self.spin_rotate = QSpinBox(); self.spin_rotate.setRange(-180, 180); self.spin_rotate.setValue(0); self.spin_rotate.setFixedWidth(80); rotate_row.addWidget(self.spin_rotate)
        btn_rotate = QPushButton("↻ Apply"); btn_rotate.setFixedWidth(70); btn_rotate.setObjectName("ActionButton"); btn_rotate.clicked.connect(lambda: self.rotate_image(self.spin_rotate.value())); rotate_row.addWidget(btn_rotate); rotate_row.addStretch(); layout_transform.addLayout(rotate_row)
        flip_row = QHBoxLayout(); flip_row.addWidget(QLabel("Flip:")); btn_flip_h = QPushButton("⟷ Horizontal"); btn_flip_h.setFixedWidth(100); btn_flip_h.setObjectName("ActionButton"); btn_flip_h.clicked.connect(lambda: self.flip_image('horizontal')); flip_row.addWidget(btn_flip_h)
        btn_flip_v = QPushButton("⟍ Vertical"); btn_flip_v.setFixedWidth(90); btn_flip_v.setObjectName("ActionButton"); btn_flip_v.clicked.connect(lambda: self.flip_image('vertical')); flip_row.addWidget(btn_flip_v); flip_row.addStretch(); layout_transform.addLayout(flip_row)
        resize_row = QHBoxLayout(); resize_row.addWidget(QLabel("Resize:")); self.spin_width = QSpinBox(); self.spin_width.setRange(1, 4096); self.spin_width.setValue(800); self.spin_width.setFixedWidth(70); resize_row.addWidget(self.spin_width)
        resize_row.addWidget(QLabel("×")); self.spin_height = QSpinBox(); self.spin_height.setRange(1, 4096); self.spin_height.setValue(600); self.spin_height.setFixedWidth(70); resize_row.addWidget(self.spin_height)
        self.chk_aspect = QCheckBox("Keep aspect"); self.chk_aspect.setChecked(True); resize_row.addWidget(self.chk_aspect)
        btn_resize = QPushButton("Resize"); btn_resize.setFixedWidth(70); btn_resize.setObjectName("ActionButton"); btn_resize.clicked.connect(lambda: self.resize_image(self.spin_width.value(), self.spin_height.value(), self.chk_aspect.isChecked())); resize_row.addWidget(btn_resize); resize_row.addStretch(); layout_transform.addLayout(resize_row)
        content_layout.addWidget(group_transform)

        # 3. Color Adjustments        group_color = QGroupBox("🎨 Color Adjustments"); group_color.setStyleSheet(group_style); layout_color = QVBoxLayout(group_color); layout_color.setSpacing(8)
        brightness_row = QHBoxLayout(); brightness_row.addWidget(QLabel("Brightness:")); self.slider_brightness = QSlider(Qt.Orientation.Horizontal); self.slider_brightness.setRange(0, 200); self.slider_brightness.setValue(100); self.slider_brightness.setFixedWidth(150); brightness_row.addWidget(self.slider_brightness)
        self.lbl_brightness = QLabel("100%"); self.lbl_brightness.setFixedWidth(40); brightness_row.addWidget(self.lbl_brightness)
        btn_apply_brightness = QPushButton("Apply"); btn_apply_brightness.setFixedWidth(60); btn_apply_brightness.setObjectName("ActionButton"); btn_apply_brightness.clicked.connect(lambda: self.adjust_brightness(self.slider_brightness.value())); brightness_row.addWidget(btn_apply_brightness)
        self.slider_brightness.valueChanged.connect(lambda v: self.lbl_brightness.setText(f"{v}%")); layout_color.addLayout(brightness_row)
        contrast_row = QHBoxLayout(); contrast_row.addWidget(QLabel("Contrast:")); self.slider_contrast = QSlider(Qt.Orientation.Horizontal); self.slider_contrast.setRange(0, 200); self.slider_contrast.setValue(100); self.slider_contrast.setFixedWidth(150); contrast_row.addWidget(self.slider_contrast)
        self.lbl_contrast = QLabel("100%"); self.lbl_contrast.setFixedWidth(40); contrast_row.addWidget(self.lbl_contrast)
        btn_apply_contrast = QPushButton("Apply"); btn_apply_contrast.setFixedWidth(60); btn_apply_contrast.setObjectName("ActionButton"); btn_apply_contrast.clicked.connect(lambda: self.adjust_contrast(self.slider_contrast.value())); contrast_row.addWidget(btn_apply_contrast)
        self.slider_contrast.valueChanged.connect(lambda v: self.lbl_contrast.setText(f"{v}%")); layout_color.addLayout(contrast_row)
        filter_row = QHBoxLayout(); btn_grayscale = QPushButton("⚫ Grayscale"); btn_grayscale.setObjectName("ActionButton"); btn_grayscale.clicked.connect(self.apply_grayscale); filter_row.addWidget(btn_grayscale)
        btn_sepia = QPushButton("🟤 Sepia"); btn_sepia.setObjectName("ActionButton"); btn_sepia.clicked.connect(self.apply_sepia); filter_row.addWidget(btn_sepia)
        btn_invert = QPushButton("◐ Invert"); btn_invert.setObjectName("ActionButton"); btn_invert.clicked.connect(self.invert_colors); filter_row.addWidget(btn_invert); layout_color.addLayout(filter_row)
        content_layout.addWidget(group_color)

        # 4. Effects
        group_effects = QGroupBox("✨ Effects & Filters"); group_effects.setStyleSheet(group_style); layout_effects = QVBoxLayout(group_effects); layout_effects.setSpacing(8)
        blur_row = QHBoxLayout(); blur_row.addWidget(QLabel("Blur:")); self.slider_blur = QSlider(Qt.Orientation.Horizontal); self.slider_blur.setRange(0, 10); self.slider_blur.setValue(2); self.slider_blur.setFixedWidth(150); blur_row.addWidget(self.slider_blur)
        self.lbl_blur = QLabel("2px"); self.lbl_blur.setFixedWidth(40); blur_row.addWidget(self.lbl_blur)
        btn_apply_blur = QPushButton("Apply"); btn_apply_blur.setFixedWidth(60); btn_apply_blur.setObjectName("ActionButton"); btn_apply_blur.clicked.connect(lambda: self.apply_blur(self.slider_blur.value())); blur_row.addWidget(btn_apply_blur)
        self.slider_blur.valueChanged.connect(lambda v: self.lbl_blur.setText(f"{v}px")); layout_effects.addLayout(blur_row)
        sharpen_row = QHBoxLayout(); sharpen_row.addWidget(QLabel("Sharpen:")); self.slider_sharpen = QSlider(Qt.Orientation.Horizontal); self.slider_sharpen.setRange(0, 200); self.slider_sharpen.setValue(100); self.slider_sharpen.setFixedWidth(150); sharpen_row.addWidget(self.slider_sharpen)
        self.lbl_sharpen = QLabel("1.0x"); self.lbl_sharpen.setFixedWidth(40); sharpen_row.addWidget(self.lbl_sharpen)
        btn_apply_sharpen = QPushButton("Apply"); btn_apply_sharpen.setFixedWidth(60); btn_apply_sharpen.setObjectName("ActionButton"); btn_apply_sharpen.clicked.connect(lambda: self.apply_sharpen(self.slider_sharpen.value() / 100.0)); sharpen_row.addWidget(btn_apply_sharpen)
        self.slider_sharpen.valueChanged.connect(lambda v: self.lbl_sharpen.setText(f"{v/100:.1f}x")); layout_effects.addLayout(sharpen_row)
        content_layout.addWidget(group_effects)

        # 5. AI & Production Suite (DesignSuite)
        group_ai_suite = QGroupBox("🤖 AI & Production Suite"); group_ai_suite.setStyleSheet(group_style); layout_ai_suite = QVBoxLayout(group_ai_suite); layout_ai_suite.setSpacing(10)
        if not HEAVY_DEPS_AVAILABLE or self.design_suite is None:
            ai_warning = QLabel("⚠️ AI dependencies missing. Install via: pip install opencv-python torch diffusers rembg"); ai_warning.setStyleSheet("color: #ff6b6b; font-size: 10px; background: transparent;"); ai_warning.setWordWrap(True); layout_ai_suite.addWidget(ai_warning)
        else:
            btn_isolate = QPushButton("✂️ AI Subject Isolator (Remove Background)"); btn_isolate.setObjectName("ActionButton"); btn_isolate.clicked.connect(self.run_subject_isolator); layout_ai_suite.addWidget(btn_isolate)
            upscale_row = QHBoxLayout(); upscale_row.addWidget(QLabel("AI Upscale Factor:")); self.spin_upscale = QSpinBox(); self.spin_upscale.setRange(2, 4); self.spin_upscale.setValue(2); self.spin_upscale.setFixedWidth(60); upscale_row.addWidget(self.spin_upscale)
            btn_upscale = QPushButton("️ Super Resolution Upscale"); btn_upscale.setObjectName("ActionButton"); btn_upscale.clicked.connect(self.run_upscaler); upscale_row.addWidget(btn_upscale); upscale_row.addStretch(); layout_ai_suite.addLayout(upscale_row)
            btn_tiler = QPushButton("🔄 Generate Seamless Texture Tile"); btn_tiler.setObjectName("ActionButton"); btn_tiler.clicked.connect(self.run_seamless_tiler); layout_ai_suite.addWidget(btn_tiler)
            palette_row = QHBoxLayout(); btn_palette = QPushButton("🎨 Extract Color Palette"); btn_palette.setObjectName("ActionButton"); btn_palette.clicked.connect(self.run_palette_harmonizer); palette_row.addWidget(btn_palette)
            self.lbl_palette_output = QLabel("No palette extracted yet."); self.lbl_palette_output.setStyleSheet("color: #61ffcf; font-size: 10px; font-family: 'Consolas'; background: transparent;"); palette_row.addWidget(self.lbl_palette_output); palette_row.addStretch(); layout_ai_suite.addLayout(palette_row)
            style_row = QHBoxLayout(); style_row.addWidget(QLabel("Style Prompt:")); self.txt_style_prompt = QLineEdit("cyberpunk, neon lights, highly detailed"); style_row.addWidget(self.txt_style_prompt, stretch=1)
            btn_style = QPushButton("✨ Apply Style Transfer"); btn_style.setObjectName("ActionButton"); btn_style.clicked.connect(self.run_style_transfer); style_row.addWidget(btn_style); layout_ai_suite.addLayout(style_row)
            inpaint_row = QHBoxLayout(); inpaint_row.addWidget(QLabel("Inpaint Prompt:")); self.txt_inpaint_prompt = QLineEdit("a red apple"); inpaint_row.addWidget(self.txt_inpaint_prompt, stretch=1)
            btn_inpaint = QPushButton("🖌️ Inpaint (Requires Mask)"); btn_inpaint.setObjectName("ActionButton"); btn_inpaint.clicked.connect(self.run_context_inpaint); inpaint_row.addWidget(btn_inpaint); layout_ai_suite.addLayout(inpaint_row)
        content_layout.addWidget(group_ai_suite)

        # 6. Advanced Production Core (AdvancedDesignExtensions - NO SVG)
        group_advanced = QGroupBox(" Advanced Production Core"); group_advanced.setStyleSheet(group_style); layout_advanced = QVBoxLayout(group_advanced); layout_advanced.setSpacing(10)
        if self.advanced_extensions is None:
            adv_warning = QLabel("⚠️ Advanced extensions unavailable."); adv_warning.setStyleSheet("color: #ff6b6b; font-size: 10px; background: transparent;"); layout_advanced.addWidget(adv_warning)
        else:
            btn_pbr = QPushButton("🗺️ Generate PBR Maps (Normal/Displacement)"); btn_pbr.setObjectName("ActionButton"); btn_pbr.clicked.connect(self.run_pbr_maps); layout_advanced.addWidget(btn_pbr)
            composite_row = QHBoxLayout(); composite_row.addWidget(QLabel("Background Image:")); self.txt_bg_path = QLineEdit(""); self.txt_bg_path.setPlaceholderText("Select background for compositing..."); composite_row.addWidget(self.txt_bg_path, stretch=1)            btn_browse_bg = QPushButton(" Browse"); btn_browse_bg.setFixedWidth(70); btn_browse_bg.setObjectName("ActionButton"); btn_browse_bg.clicked.connect(self.browse_background_image); composite_row.addWidget(btn_browse_bg); layout_advanced.addLayout(composite_row)
            btn_composite = QPushButton("📐 Composite Layers"); btn_composite.setObjectName("ActionButton"); btn_composite.clicked.connect(self.run_composite_layers); layout_advanced.addWidget(btn_composite)
        content_layout.addWidget(group_advanced)

        # 7. Save & Export
        group_save = QGroupBox("💾 Save & Export"); group_save.setStyleSheet(group_style); layout_save = QVBoxLayout(group_save); layout_save.setSpacing(10)
        btn_save = QPushButton("💾 Save Edited Image"); btn_save.setObjectName("ActionButton"); btn_save.setFixedHeight(40); btn_save.clicked.connect(self.save_current_image); layout_save.addWidget(btn_save)
        btn_reset = QPushButton("🔄 Reset to Original"); btn_reset.setObjectName("SecondaryButton"); btn_reset.clicked.connect(self.reset_image); layout_save.addWidget(btn_reset)
        content_layout.addWidget(group_save)

        content_layout.addStretch(); scroll.setWidget(inner_widget); left_layout.addWidget(scroll, stretch=1)

        # RIGHT COLUMN: Preview
        right_column = QFrame(); right_column.setObjectName("AssetPreviewColumn"); right_column.setFixedWidth(350)
        right_layout = QVBoxLayout(right_column); right_layout.setContentsMargins(0, 0, 0, 0); right_layout.setSpacing(10)
        preview_header = QLabel("🖼️ ASSET PREVIEW BAY"); preview_header.setStyleSheet("color: #7b61ff; font-size: 12px; font-weight: bold; letter-spacing: 1px; background: transparent;"); right_layout.addWidget(preview_header)
        self.preview_window = QLabel(); self.preview_window.setObjectName("ImagePreviewBay"); self.preview_window.setAlignment(Qt.AlignmentFlag.AlignCenter); self.preview_window.setMinimumSize(310, 350); self.preview_window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding); self.preview_window.setWordWrap(True); self.preview_window.setText("⬇\n\nDrag & Drop\nImage Here\n\nor use Browse")
        self.preview_window.setStyleSheet("QLabel#ImagePreviewBay { background-color: #08060f; border: 2px dashed #251d3a; border-radius: 14px; color: #52476d; font-family: 'Segoe UI'; font-size: 11px; }"); self.preview_window.setAcceptDrops(True); right_layout.addWidget(self.preview_window, stretch=1)
        btn_browse_preview = QPushButton("📁 Browse File"); btn_browse_preview.setFixedHeight(36); btn_browse_preview.setObjectName("ActionButton"); btn_browse_preview.clicked.connect(self.browse_for_image); right_layout.addWidget(btn_browse_preview)
        info_label = QLabel("📋 Drop images or use Browse to load assets"); info_label.setStyleSheet("color: #645585; font-size: 9px; font-family: 'Segoe UI'; background: transparent;"); info_label.setAlignment(Qt.AlignmentFlag.AlignCenter); info_label.setWordWrap(True); right_layout.addWidget(info_label); right_layout.addStretch()
        content_row.addWidget(left_column, stretch=2); content_row.addWidget(right_column, stretch=1); main_layout.addLayout(content_row, stretch=1)

        # Status Log
        log_header = QLabel("📋 SYSTEM RESPONSE LOG"); log_header.setStyleSheet("color: #645585; font-size: 9px; font-weight: bold; letter-spacing: 1px; background: transparent;"); main_layout.addWidget(log_header)
        self.status_log = QTextEdit(); self.status_log.setReadOnly(True); self.status_log.setMaximumHeight(110); self.status_log.setPlaceholderText("Awaiting operations..."); self.status_log.setStyleSheet("QTextEdit { background-color: #0b0813; color: #61ffcf; border: 1px solid #1f1833; border-radius: 6px; font-family: 'Consolas'; font-size: 10px; padding: 8px; }"); main_layout.addWidget(self.status_log)
        self.workspace_stack.addTab(page, "Visual Alchemy")

    def init_deployment_architect_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        page_header = QLabel("🚀 DEPLOYMENT ARCHITECT"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); main_layout.addWidget(page_header)
        two_col = QHBoxLayout(); two_col.setSpacing(16)
        card_rep, layout_rep = self.create_card("OS Deployment Replicator", "Backup & Restore", "🛡️"); card_rep.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }")
        btn_restore = QPushButton("🛡️ Generate Safe System Restore Checkpoint"); btn_restore.setObjectName("ActionButton"); layout_rep.addWidget(btn_restore); layout_rep.addStretch(); two_col.addWidget(card_rep, stretch=1)
        card_bulk, layout_bulk = self.create_card("Silent Bulk Installer", "Automated Deployment Loop", "📦"); card_bulk.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }")
        self.txt_todo_replica = QTextEdit(); self.txt_todo_replica.setPlainText("[ ] REINSTALL: GoogleChrome\n[ ] REINSTALL: VLC"); self.txt_todo_replica.setMaximumHeight(140); layout_bulk.addWidget(self.txt_todo_replica)
        btn_run_bulk = QPushButton("🚀 Run Automated Silent Bulk Installer Loop"); btn_run_bulk.setObjectName("ActionButton"); layout_bulk.addWidget(btn_run_bulk); two_col.addWidget(card_bulk, stretch=1)
        main_layout.addLayout(two_col); main_layout.addStretch(); self.workspace_stack.addTab(page, "Deployment")

    def init_task_viewer_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(12)
        page_header = QLabel("🧠 TASK VIEWER"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); main_layout.addWidget(page_header)
        toolbar = QHBoxLayout(); toolbar.setSpacing(10)
        self.txt_process_filter = QLineEdit(); self.txt_process_filter.setPlaceholderText("🔍 Filter processes by name..."); self.txt_process_filter.setFixedHeight(30); self.txt_process_filter.textChanged.connect(self._filter_processes); toolbar.addWidget(self.txt_process_filter, stretch=1)
        btn_refresh = QPushButton("🔄 Refresh"); btn_refresh.setFixedHeight(30); btn_refresh.setFixedWidth(90); btn_refresh.setObjectName("ActionButton"); btn_refresh.clicked.connect(lambda: self.refresh_process_view()); toolbar.addWidget(btn_refresh)
        btn_kill_selected = QPushButton(" Kill Selected"); btn_kill_selected.setObjectName("KillSelectedButton"); btn_kill_selected.setFixedHeight(30); btn_kill_selected.setFixedWidth(110); btn_kill_selected.clicked.connect(self.kill_selected_process); toolbar.addWidget(btn_kill_selected)
        main_layout.addLayout(toolbar)
        self.process_table = QTableWidget(0, 5); self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Mem %", "Action"])
        if self.process_table.horizontalHeader() is not None: self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)        self.process_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows); self.process_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); self.process_table.setAlternatingRowColors(True)
        if self.process_table.verticalHeader() is not None: self.process_table.verticalHeader().setVisible(False)
        main_layout.addWidget(self.process_table, stretch=1); self.workspace_stack.addTab(page, "Task Viewer")

    def _filter_processes(self, text):
        if not hasattr(self, 'process_table'): return
        filter_text = text.lower().strip()
        for row in range(self.process_table.rowCount()):
            name_item = self.process_table.item(row, 1)
            if name_item: self.process_table.setRowHidden(row, not (filter_text == "" or filter_text in name_item.text().lower()))

    def kill_selected_process(self):
        selection_model = self.process_table.selectionModel()
        if selection_model is None or not selection_model.selectedRows(): return
        row = selection_model.selectedRows()[0].row(); item = self.process_table.item(row, 0)
        if item: 
            try: self.kill_process(int(item.text()))
            except ValueError: pass

    def init_tuning_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        page_header = QLabel("⚙️ ARCANE TUNING"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); main_layout.addWidget(page_header)
        two_col = QHBoxLayout(); two_col.setSpacing(16)
        card_guard, layout_guard = self.create_card("System Policy Shields", "Registry Security & Bloatware Prevention", "🔒"); card_guard.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }")
        btn_policies = QPushButton("🔒 Inject Registry Policy Guards Against Auto-Bloatware"); btn_policies.setObjectName("ActionButton"); layout_guard.addWidget(btn_policies); layout_guard.addStretch(); two_col.addWidget(card_guard, stretch=1)
        card_perf, layout_perf = self.create_card("Performance Tuning", "Startup & Services", "⚡"); card_perf.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }")
        self.chk_disable_animations = QCheckBox("Disable Windows UI Animations"); self.chk_disable_animations.setStyleSheet("color: #c9bedf; font-size: 11px; background: transparent;"); layout_perf.addWidget(self.chk_disable_animations)
        btn_apply_tuning = QPushButton("⚡ Apply Performance Tuning"); btn_apply_tuning.setObjectName("ActionButton"); layout_perf.addWidget(btn_apply_tuning); layout_perf.addStretch(); two_col.addWidget(card_perf, stretch=1)
        main_layout.addLayout(two_col); main_layout.addStretch(); self.workspace_stack.addTab(page, "Arcane Tuning")

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
            QCheckBox { color: #c9bedf; font-family: 'Segoe UI'; font-size: 11px; background: transparent; spacing: 6px; }            QCheckBox::indicator { width: 14px; height: 14px; border-radius: 3px; border: 1px solid #322652; background: #1e1730; }
            QCheckBox::indicator:checked { background: #7b61ff; border-color: #7b61ff; }
            QTableWidget { background-color: #0e0a19; color: #c9bedf; border: 1px solid #1f1833; border-radius: 8px; gridline-color: #1a1430; font-size: 10px; }
            QHeaderView::section { background-color: #171226; color: #7b61ff; padding: 8px; border: none; font-weight: bold; font-size: 10px; font-family: 'Segoe UI'; }
        """)

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())