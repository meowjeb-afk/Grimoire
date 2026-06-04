import sys
import os
import re
import psutil
from datetime import datetime
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QCheckBox, QTabWidget,
    QLineEdit, QTextEdit, QFrame, QSlider, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar,
    QScrollArea, QGroupBox, QFileDialog, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QPoint, QTimer, QRect
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QFont

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

class TelemetrySampler(QThread):
    system_metrics_updated = pyqtSignal(float, float, float)
    internal_process_updated = pyqtSignal(dict)

    def __init__(self, poll_interval=1.5, parent=None):
        super().__init__(parent)
        self.poll_interval = poll_interval
        self.running = True

    def gather_internal_process_stats(self):
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return {
            "processes": processes,
            "process_count": len(processes)
        }

    def run(self):
        while self.running:
            try:
                cpu = psutil.cpu_percent(interval=0.5)
                memory = psutil.virtual_memory()
                swap = psutil.swap_memory()
                internal_data = self.gather_internal_process_stats()
                self.system_metrics_updated.emit(cpu, memory.percent, swap.percent)
                self.internal_process_updated.emit(internal_data)
            except Exception:
                pass
            self.msleep(int(self.poll_interval * 1000))

    def stop(self):
        self.running = False

class GrimoireNavButton(QFrame):
    clicked = pyqtSignal(int)

    def __init__(self, icon_str, name_str, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.is_checked = False
        self.setObjectName("NavButtonContainer")
        self.setAttribute(Qt.WidgetAttribute.WA_Hover, True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 10, 14, 10)
        layout.setSpacing(10)

        self.icon_label = QLabel(icon_str)
        self.icon_label.setStyleSheet("font-size: 14px; background: transparent;")
        layout.addWidget(self.icon_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.text_label = QLabel(name_str)
        self.text_label.setStyleSheet("""
            font-family: 'Segoe UI';
            font-weight: bold;
            font-size: 11px;
            background: transparent;
        """)
        layout.addWidget(self.text_label, alignment=Qt.AlignmentFlag.AlignVCenter)

        self.text_label.hide()
        self.update_state_styling()

    def setChecked(self, checked):
        self.is_checked = checked
        if self.is_checked:
            self.text_label.show()
        else:
            self.text_label.hide()
        self.update_state_styling()

    def enterEvent(self, event):
        self.text_label.show()
        self.update_state_styling(hover=True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        if not self.is_checked:
            self.text_label.hide()
        self.update_state_styling(hover=False)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.index)
            event.accept()

    def update_state_styling(self, hover=False):
        if self.is_checked:
            self.setStyleSheet("""
                QFrame#NavButtonContainer {
                    background-color: #241b3f;
                    border-radius: 8px;
                    border-left: 3px solid #7b61ff;
                }
                QLabel { color: #7b61ff; }
            """)
        elif hover:
            self.setStyleSheet("""
                QFrame#NavButtonContainer {
                    background-color: #1a142e;
                    border-radius: 8px;
                    border-left: 3px solid #4a3e63;
                }
                QLabel { color: #ffffff; }
            """)
        else:
            self.setStyleSheet("""
                QFrame#NavButtonContainer {
                    background-color: transparent;
                    border-radius: 8px;
                    border-left: 3px solid transparent;
                }
                QLabel { color: #8c7fa6; }
            """)

class ArcaneSystemVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.angle = 0
        self.pulse = 0
        self.pulse_growing = True
        self.is_active = False
        self.load_intensity = 0.0
        self.internal_data = {"processes": [], "process_count": 0}

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)

    def set_internal_data(self, internal_data):
        if internal_data is None:
            internal_data = {"processes": [], "process_count": 0}
        self.internal_data = internal_data
        self.load_intensity = max(
            (item.get('cpu_percent', 0.0) for item in self.internal_data.get('processes', [])),
            default=0.0
        )
        self.update()

    def set_telemetry_data(self, cpu_load, memory_load, swap_load=0.0):
        self.update()

    def trigger_pulse(self):
        self.is_active = True
        self.pulse = 30

    def update_animation(self):
        speed = 1 + (self.load_intensity / 20)
        self.angle = (self.angle + int(speed)) % 360
        if self.pulse_growing:
            self.pulse += 0.2
            if self.pulse >= 12:
                self.pulse_growing = False
        else:
            self.pulse -= 0.2
            if self.pulse <= 2:
                self.pulse_growing = True
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect().adjusted(4, 4, -4, -4)
        painter.fillRect(rect, QColor("#120e1f"))

        border_pen = QPen(QColor("#1f1833"))
        border_pen.setWidth(2)
        painter.setPen(border_pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(rect, 12, 12)

        inner = rect.adjusted(10, 10, -10, -10)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#1e1730"))
        painter.drawRoundedRect(inner, 10, 10)

        painter.setPen(QColor("#a397bf"))
        painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        painter.drawText(inner.left() + 12, inner.top() + 22, "SYSTEM TELEMETRY MATRIX")

        gauge_width = inner.width() - 24
        gauge_height = 12
        base_y = inner.top() + 38

        def draw_gauge(label, value, offset, color):
            painter.setPen(QColor("#a397bf"))
            painter.setFont(QFont("Segoe UI", 8))
            painter.drawText(inner.left() + 12, base_y + offset, label)
            gauge_rect = QRect(inner.left() + 12, base_y + offset + 8, gauge_width, gauge_height)
            painter.setBrush(QColor("#251d3a"))
            painter.drawRoundedRect(gauge_rect, 6, 6)
            fill_width = int(gauge_width * max(0, min(100, value)) / 100)
            painter.setBrush(QColor(color))
            painter.drawRoundedRect(QRect(gauge_rect.left(), gauge_rect.top(), fill_width, gauge_height), 6, 6)
            painter.setPen(QColor("#ffffff"))
            painter.drawText(gauge_rect.right() - 54, gauge_rect.top() + 10, f"{value:.0f}%")

        processes = self.internal_data.get("processes", [])
        process_count = self.internal_data.get("process_count", len(processes))
        top_cpu = 0.0
        top_name = "N/A"
        if processes:
            top = max(processes, key=lambda item: item.get('cpu_percent', 0.0))
            top_cpu = top.get('cpu_percent', 0.0)
            top_name = top.get('name', '<unknown>')

        painter.setPen(QColor("#a397bf"))
        painter.setFont(QFont("Segoe UI", 8))
        painter.drawText(inner.left() + 12, base_y + 90, f"Tracked Process Count: {process_count}")
        painter.drawText(inner.left() + 12, base_y + 106, f"Most Active: {top_name} ({top_cpu:.1f}% CPU)")

        pulse_radius = 14 + int(min(40, max(0, top_cpu / 2)))
        if self.is_active or top_cpu > 5:
            pulse_color = QColor(123, 97, 255, 120 if top_cpu > 0 else 70)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(pulse_color)
            painter.drawEllipse(inner.right() - 34, inner.top() + 12, pulse_radius, pulse_radius)


class GrimoireMirror(QMainWindow):
    def __init__(self):
        super().__init__()
        self.telemetry_thread = None
        self.setWindowTitle("Grimoire Master OS Shell Extension")
        self.resize(1100, 800)
        self.setMinimumSize(900, 650)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.logo_icon_path = os.path.join(os.path.dirname(__file__), "grimoire_logo.png")
        self.logo_text_path = os.path.join(os.path.dirname(__file__), "grimoire_text.png")

        self.drag_position = QPoint()
        self.is_maximized = False
        self.is_resizing = False
        self.resize_edge = None
        self.resize_start_pos = None
        self.resize_start_geo = None

        self.main_container = QWidget()
        self.main_container.setObjectName("MainContainer")
        self.setCentralWidget(self.main_container)

        master_vertical = QVBoxLayout(self.main_container)
        master_vertical.setContentsMargins(0, 0, 0, 0)
        master_vertical.setSpacing(0)

        self.init_custom_title_bar(master_vertical)

        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        master_vertical.addLayout(content_layout)

        self.init_sidebar(content_layout)

        self.workspace_stack = QTabWidget()
        workspace_tab_bar = self.workspace_stack.tabBar()
        if workspace_tab_bar is not None:
            workspace_tab_bar.hide()
        content_layout.addWidget(self.workspace_stack, stretch=3)

        self.cpu_bar = None
        self.memory_bar = None
        self.swap_bar = None

        self.init_right_preview_panel(content_layout)

        # --- Init all tabs ---
        self.init_core_tab()
        self.init_alchemy_tab()
        self.init_visual_alchemy_tab()
        self.init_deployment_architect_tab()
        self.init_task_viewer_tab()
        self.init_tuning_tab()

        # --- Status bar at the very bottom ---
        self.init_status_bar(master_vertical)

        self.apply_theme()

        self.telemetry_state = {"cpu": 0.0, "memory": 0.0, "swap": 0.0}
        self.asset_state = {"path": None, "message": "[ Waiting for Asset ]"}
        self.process_state = {"rows": []}

        self.telemetry_thread = TelemetrySampler(1.5)
        try:
            self.telemetry_thread.system_metrics_updated.disconnect(self.update_main_dashboard)
        except TypeError:
            pass
        try:
            self.telemetry_thread.internal_process_updated.disconnect(self.update_visualizer_matrix)
        except TypeError:
            pass
        self.telemetry_thread.system_metrics_updated.connect(self.update_main_dashboard)
        self.telemetry_thread.internal_process_updated.connect(self.update_visualizer_matrix)
        self.telemetry_thread.start()

    def closeEvent(self, event):
        if self.telemetry_thread is not None:
            self.telemetry_thread.stop()
            self.telemetry_thread.wait(1000)
        super().closeEvent(event)

    # ── Window dragging / resizing (unchanged) ──────────────────────────────
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and not self.is_maximized:
            edge = self.get_resize_edge(event.position().toPoint())
            if edge > 0:
                self.is_resizing = True
                self.resize_edge = edge
                self.resize_start_pos = event.globalPosition().toPoint()
                self.resize_start_geo = self.geometry()
                event.accept()
                return
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if not self.is_maximized:
            edge = self.get_resize_edge(event.position().toPoint())
            self.set_resize_cursor(edge)
        if self.is_resizing and not self.is_maximized:
            delta = event.globalPosition().toPoint() - self.resize_start_pos
            geo = self.resize_start_geo
            edge = self.resize_edge
            if geo is None: return
            new_x, new_y, new_w, new_h = geo.x(), geo.y(), geo.width(), geo.height()
            if edge == 1:   new_x += delta.x(); new_y += delta.y(); new_w -= delta.x(); new_h -= delta.y()
            elif edge == 2: new_y += delta.y(); new_w += delta.x(); new_h -= delta.y()
            elif edge == 3: new_x += delta.x(); new_w -= delta.x(); new_h += delta.y()
            elif edge == 4: new_w += delta.x(); new_h += delta.y()
            elif edge == 5: new_y += delta.y(); new_h -= delta.y()
            elif edge == 6: new_h += delta.y()
            elif edge == 7: new_x += delta.x(); new_w -= delta.x()
            elif edge == 8: new_w += delta.x()
            if new_w >= self.minimumWidth() and new_h >= self.minimumHeight():
                self.setGeometry(new_x, new_y, new_w, new_h)
            event.accept()
            return
        if event.buttons() == Qt.MouseButton.LeftButton and not self.is_maximized:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_resizing = False
            self.resize_edge = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()

    def get_resize_edge(self, pos):
        edge_size = 8
        x, y, w, h = pos.x(), pos.y(), self.width(), self.height()
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
        if self.is_maximized:
            self.showNormal()
            self.is_maximized = False
        else:
            self.showMaximized()
            self.is_maximized = True

    # ── Telemetry callbacks ──────────────────────────────────────────────────
    def update_main_dashboard(self, cpu_load, memory_load, swap_load):
        self.telemetry_state.update({"cpu": cpu_load, "memory": memory_load, "swap": swap_load})
        self.refresh_telemetry_view()

    def update_visualizer_matrix(self, internal_data):
        if internal_data is None:
            internal_data = {"processes": [], "process_count": 0}
        if hasattr(self, 'visualizer'):
            self.visualizer.set_internal_data(internal_data)
        self.process_state["rows"] = internal_data.get('processes', [])
        self.refresh_process_view()

    def refresh_ui(self):
        self.refresh_telemetry_view()
        self.refresh_process_view()
        self.refresh_preview_view()

    def refresh_telemetry_view(self):
        if self.cpu_bar is not None and self.memory_bar is not None and self.swap_bar is not None:
            self.cpu_bar.setValue(int(self.telemetry_state["cpu"]))
            self.cpu_bar.setFormat(f"CPU: {self.telemetry_state['cpu']:.1f}%")
            self.memory_bar.setValue(int(self.telemetry_state["memory"]))
            self.memory_bar.setFormat(f"RAM: {self.telemetry_state['memory']:.1f}%")
            self.swap_bar.setValue(int(self.telemetry_state["swap"]))
            self.swap_bar.setFormat(f"Swap: {self.telemetry_state['swap']:.1f}%")
        # Update status bar
        if hasattr(self, 'status_cpu_lbl'):
            self.status_cpu_lbl.setText(f"CPU {self.telemetry_state['cpu']:.0f}%")
            self.status_mem_lbl.setText(f"MEM {self.telemetry_state['memory']:.0f}%")
            self.status_time_lbl.setText(datetime.now().strftime("%H:%M:%S"))

    def refresh_process_view(self):
        if hasattr(self, 'process_table'):
            self.populate_process_table(self.process_state["rows"])

    def populate_process_table(self, processes):
        processes = sorted(processes, key=lambda item: item.get('cpu_percent', 0), reverse=True)[:25]
        self.process_table.setRowCount(len(processes))

        if not processes:
            self.process_table.setRowCount(1)
            empty_item = QTableWidgetItem("  No active processes to display. Waiting for telemetry data...")
            empty_item.setForeground(QColor("#4a3e63"))
            empty_item.setFlags(empty_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            self.process_table.setItem(0, 0, empty_item)
            self.process_table.setSpan(0, 0, 1, 5)
            return

        for row, proc in enumerate(processes):
            pid = proc.get('pid', '')
            name = proc.get('name', '') or "<unknown>"
            cpu = proc.get('cpu_percent', 0.0)
            mem = proc.get('memory_percent', 0.0)

            self.process_table.setItem(row, 0, QTableWidgetItem(str(pid)))
            self.process_table.setItem(row, 1, QTableWidgetItem(name))
            self.process_table.setItem(row, 2, QTableWidgetItem(f"{cpu:.1f}"))
            self.process_table.setItem(row, 3, QTableWidgetItem(f"{mem:.1f}"))

            kill_button = QPushButton("✕ Kill")
            kill_button.setObjectName("KillProcessButton")
            kill_button.setFixedHeight(26)
            kill_button.clicked.connect(lambda checked, pid=pid: self.kill_process(pid))
            self.process_table.setCellWidget(row, 4, kill_button)

    def kill_selected_process(self):
        selection_model = self.process_table.selectionModel()
        if selection_model is None:
            QMessageBox.information(self, "Process Control", "Unable to access process selection.")
            return
        selected_rows = selection_model.selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Process Control", "Select a process row first.")
            return
        row = selected_rows[0].row()
        item = self.process_table.item(row, 0)
        if item is None:
            QMessageBox.information(self, "Process Control", "Unable to read the selected PID.")
            return
        selected_pid_text = item.text()
        if not selected_pid_text:
            QMessageBox.information(self, "Process Control", "Invalid PID selected.")
            return
        try:
            selected_pid = int(selected_pid_text)
        except ValueError:
            QMessageBox.information(self, "Process Control", "Selected PID is not valid.")
            return
        self.kill_process(selected_pid)

    def kill_process(self, pid):
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            proc.wait(timeout=2)
            QMessageBox.information(self, "Process Control", f"PID {pid} terminated.")
        except psutil.NoSuchProcess:
            QMessageBox.information(self, "Process Control", f"PID {pid} no longer exists.")
        except psutil.AccessDenied:
            QMessageBox.warning(self, "Process Control", f"Permission denied closing PID {pid}.")
        except Exception as exc:
            QMessageBox.warning(self, "Process Control", f"Failed to close PID {pid}: {exc}")

    # ── Title bar ────────────────────────────────────────────────────────────
    def init_custom_title_bar(self, parent_layout):
        self.title_bar = QFrame()
        self.title_bar.setObjectName("CustomTitleBar")
        title_layout = QHBoxLayout(self.title_bar)
        title_layout.setContentsMargins(15, 6, 12, 6)
        title_layout.setSpacing(8)

        window_icon_label = QLabel()
        window_icon_label.setFixedSize(20, 20)
        window_icon_label.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        try:
            if self.logo_icon_path and os.path.exists(self.logo_icon_path):
                pixmap = QPixmap(self.logo_icon_path)
                if not pixmap.isNull():
                    scaled_pixmap = pixmap.scaled(
                        20, 20,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    window_icon_label.setPixmap(scaled_pixmap)
                else:
                    window_icon_label.setText("🔮")
            else:
                window_icon_label.setText("🔮")
        except Exception:
            window_icon_label.setText("🔮")
        title_layout.addWidget(window_icon_label)

        window_title = QLabel("Grimoire Master OS Shell Extension")
        title_style = "color: #a397bf; font-family: 'Segoe UI'; font-weight: bold; font-size: 11px; letter-spacing: 0.5px;"
        window_title.setStyleSheet(title_style)
        title_layout.addWidget(window_title)
        title_layout.addStretch()

        btn_min = QPushButton("🗕")
        btn_min.setObjectName("TitleMinButton")
        btn_min.setFixedSize(28, 24)
        btn_min.clicked.connect(self.showMinimized)
        title_layout.addWidget(btn_min)

        btn_max = QPushButton("🗖")
        btn_max.setObjectName("TitleMaxButton")
        btn_max.setFixedSize(28, 24)
        btn_max.clicked.connect(self.toggle_maximize)
        title_layout.addWidget(btn_max)

        btn_close = QPushButton("🗙")
        btn_close.setObjectName("TitleCloseButton")
        btn_close.setFixedSize(28, 24)
        btn_close.clicked.connect(self.close)
        title_layout.addWidget(btn_close)

        parent_layout.addWidget(self.title_bar)

    # ── Sidebar ──────────────────────────────────────────────────────────────
    def init_sidebar(self, parent_layout):
        self.sidebar_frame = QFrame()
        self.sidebar_frame.setObjectName("SidebarDock")
        sidebar_layout = QVBoxLayout(self.sidebar_frame)
        sidebar_layout.setContentsMargins(8, 20, 8, 20)
        sidebar_layout.setSpacing(6)

        logo_container = QWidget()
        logo_layout = QVBoxLayout(logo_container)
        logo_layout.setContentsMargins(0, 0, 0, 16)
        logo_layout.setSpacing(8)

        self.logo_icon_label = QLabel()
        self.logo_icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            if self.logo_icon_path and os.path.exists(self.logo_icon_path):
                pixmap_icon = QPixmap(self.logo_icon_path)
                if not pixmap_icon.isNull():
                    scaled_pixmap = pixmap_icon.scaled(
                        80, 80,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.logo_icon_label.setPixmap(scaled_pixmap)
                else:
                    self.logo_icon_label.setText("🔮")
                    self.logo_icon_label.setStyleSheet("font-size: 32px;")
            else:
                self.logo_icon_label.setText("🔮")
                self.logo_icon_label.setStyleSheet("font-size: 32px;")
        except Exception:
            self.logo_icon_label.setText("🔮")
            self.logo_icon_label.setStyleSheet("font-size: 32px;")
        logo_layout.addWidget(self.logo_icon_label)

        self.logo_text_label = QLabel()
        self.logo_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        try:
            if self.logo_text_path and os.path.exists(self.logo_text_path):
                pixmap_text = QPixmap(self.logo_text_path)
                if not pixmap_text.isNull():
                    scaled_pixmap = pixmap_text.scaled(
                        120, 40,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.logo_text_label.setPixmap(scaled_pixmap)
                else:
                    self.logo_text_label.setText("Grimoire")
                    self.logo_text_label.setStyleSheet("""
                        font-size: 20px;
                        font-weight: bold;
                        color: #7b61ff;
                        font-family: 'Segoe UI';
                    """)
            else:
                self.logo_text_label.setText("Grimoire")
                self.logo_text_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: bold;
                    color: #7b61ff;
                    font-family: 'Segoe UI';
                """)
        except Exception:
            self.logo_text_label.setText("Grimoire")
            self.logo_text_label.setStyleSheet("""
                font-size: 20px;
                font-weight: bold;
                color: #7b61ff;
                font-family: 'Segoe UI';
            """)
        logo_layout.addWidget(self.logo_text_label)

        sidebar_layout.addWidget(logo_container)

        # Version tag under brand
        ver_label = QLabel("v2.4.1")
        ver_label.setStyleSheet("color: #3d3456; font-size: 9px; font-family: 'Consolas'; margin-bottom: 12px;")
        ver_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(ver_label)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #1f1833;")
        sep.setFixedHeight(1)
        sidebar_layout.addWidget(sep)

        self.nav_buttons = []
        modules = [
            ("📊", "Dashboard", 0),
            ("🧪", "File Alchemy", 1),
            ("👁️", "Visual Alchemy", 2),
            ("🚀", "Deployment", 3),
            ("🧠", "Task Viewer", 4),
            ("⚙️", "Arcane Tuning", 5)
        ]
        for icon, name, index in modules:
            btn = GrimoireNavButton(icon, name, index)
            if index == 0:
                btn.setChecked(True)
            btn.clicked.connect(self.switch_workspace_view)
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        # Bottom sidebar info
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #1f1833;")
        sep2.setFixedHeight(1)
        sidebar_layout.addWidget(sep2)

        sys_info = QLabel("🟢 System Online")
        sys_info.setStyleSheet("color: #61ffcf; font-size: 9px; font-family: 'Segoe UI'; padding: 4px;")
        sys_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(sys_info)

        parent_layout.addWidget(self.sidebar_frame, stretch=0)

    def switch_workspace_view(self, index):
        self.workspace_stack.setCurrentIndex(index)
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)

    # ── Right preview panel ──────────────────────────────────────────────────
    def init_right_preview_panel(self, parent_layout):
        self.right_panel_frame = QFrame()
        self.right_panel_frame.setObjectName("RightPreviewPanel")
        right_layout = QVBoxLayout(self.right_panel_frame)
        right_layout.setContentsMargins(12, 16, 12, 16)
        right_layout.setSpacing(10)

        # Header
        header = QLabel("🖼️ ASSET PREVIEW BAY")
        header.setStyleSheet("color: #7b61ff; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        right_layout.addWidget(header)

        self.preview_window = QLabel()
        self.preview_window.setObjectName("ImagePreviewBay")
        self.preview_window.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_window.setMinimumSize(220, 200)
        self.preview_window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.preview_window.setWordWrap(True)
        self.preview_window.setText("⬇\n\nDrag & Drop\nImage Here")
        self.preview_window.setStyleSheet("""
            QLabel#ImagePreviewBay {
                background-color: #08060f;
                border: 2px dashed #251d3a;
                border-radius: 14px;
                color: #52476d;
                font-family: 'Segoe UI';
                font-size: 11px;
            }
        """)
        self.preview_window.setAcceptDrops(True)
        right_layout.addWidget(self.preview_window, stretch=3)

        # Browse button under preview
        btn_browse_preview = QPushButton("📁 Browse File")
        btn_browse_preview.setFixedHeight(30)
        btn_browse_preview.clicked.connect(self.browse_for_image)
        right_layout.addWidget(btn_browse_preview)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #1f1833; max-height: 1px;")
        sep.setFixedHeight(1)
        right_layout.addWidget(sep)

        # Visualizer — let it expand to fill remaining space
        viz_header = QLabel("⚡ TELEMETRY MATRIX")
        viz_header.setStyleSheet("color: #7b61ff; font-size: 10px; font-weight: bold; letter-spacing: 1px;")
        right_layout.addWidget(viz_header)

        self.visualizer = ArcaneSystemVisualizer(self.right_panel_frame)
        right_layout.addWidget(self.visualizer, stretch=2)

        parent_layout.addWidget(self.right_panel_frame, stretch=1)

    # ── Status bar at bottom ─────────────────────────────────────────────────
    def init_status_bar(self, parent_layout):
        self.status_bar = QFrame()
        self.status_bar.setObjectName("StatusBar")
        status_layout = QHBoxLayout(self.status_bar)
        status_layout.setContentsMargins(16, 4, 16, 4)
        status_layout.setSpacing(16)

        # Left: connection status
        status_dot = QLabel("●")
        status_dot.setStyleSheet("color: #61ffcf; font-size: 10px;")
        status_layout.addWidget(status_dot)
        status_lbl = QLabel("Grimoire Shell Active")
        status_lbl.setStyleSheet("color: #645585; font-size: 10px; font-family: 'Segoe UI';")
        status_layout.addWidget(status_lbl)

        status_layout.addStretch()

        # Center: system metrics
        self.status_cpu_lbl = QLabel("CPU --%")
        self.status_cpu_lbl.setStyleSheet("color: #7b61ff; font-size: 10px; font-family: 'Consolas'; font-weight: bold;")
        status_layout.addWidget(self.status_cpu_lbl)

        self.status_mem_lbl = QLabel("MEM --%")
        self.status_mem_lbl.setStyleSheet("color: #61ffcf; font-size: 10px; font-family: 'Consolas'; font-weight: bold;")
        status_layout.addWidget(self.status_mem_lbl)

        status_layout.addStretch()

        # Right: time
        self.status_time_lbl = QLabel("--:--:--")
        self.status_time_lbl.setStyleSheet("color: #4a3e63; font-size: 10px; font-family: 'Consolas';")
        status_layout.addWidget(self.status_time_lbl)

        parent_layout.addWidget(self.status_bar)

    # ── Async worker ─────────────────────────────────────────────────────────
    def cast_asynchronously(self, target_function, *args):
        self.visualizer.trigger_pulse()
        self.worker = ArcaneWorker(target_function, *args)
        self.worker.manifest_complete.connect(self.display_output)
        self.worker.start()

    def display_output(self, text):
        if not text: return
        error_keywords = ["Error", "Targeted asset", "not found", "Failed", "Unable"]
        is_error = any(keyword in text for keyword in error_keywords)

        def find_image_path(candidate_text):
            image_pattern = r"([A-Za-z]:[\\/][^\n\r]+?\.(?:png|jpg|jpeg|bmp|gif))"
            matches = re.findall(image_pattern, candidate_text, flags=re.IGNORECASE)
            for match in matches:
                normalized = os.path.normpath(match.strip('"'))
                if os.path.exists(normalized) and normalized.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    return normalized
            return None

        asset_path = find_image_path(text)
        if asset_path:
            self.asset_state["path"] = asset_path
            self.asset_state["message"] = None
            self.refresh_preview_view()
            self.log_output(f"✓ Asset loaded: {os.path.basename(asset_path)}")
            return

        self.asset_state["path"] = None
        self.asset_state["message"] = "[ Waiting for Asset ]"
        self.refresh_preview_view()
        self.log_output(text)
        if is_error:
            QMessageBox.warning(self, "System Alert", text)

    def log_output(self, message):
        if hasattr(self, 'status_log'):
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.status_log.append(f"[{timestamp}] {message}")
            scrollbar = self.status_log.verticalScrollBar()
            if scrollbar is not None:
                scrollbar.setValue(scrollbar.maximum())

    def refresh_preview_view(self):
        if not hasattr(self, 'preview_window'): return
        if self.asset_state["path"] is not None and os.path.exists(self.asset_state["path"]):
            pixmap = QPixmap(self.asset_state["path"])
            self.preview_window.setPixmap(pixmap.scaled(
                self.preview_window.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            ))
        else:
            self.preview_window.clear()
            self.preview_window.setText(self.asset_state.get("message", "[ Waiting for Asset ]"))

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls(): event.accept()
        else: event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if files: self.handle_image_input(files[0])

    def browse_for_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif);;All Files (*)"
        )
        if file_path: self.handle_image_input(file_path)

    def handle_image_input(self, path):
        if not os.path.exists(path):
            self.log_output(f"✗ File not found: {path}")
            return
        if not path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            self.log_output(f"✗ Unsupported format: {os.path.basename(path)}")
            return
        self.asset_state["path"] = path
        self.asset_state["message"] = None
        self.refresh_preview_view()
        if hasattr(self, 'txt_img_path'):
            self.txt_img_path.setText(path)
        if hasattr(self, 'visualizer'):
            self.visualizer.is_active = False
        self.log_output(f"✓ Image loaded: {os.path.basename(path)}")

    # ── Helper: create modern statistic card ────────────────────────────────
    def create_modern_card(self, title, value="", subtitle="", icon="", color="#7b61ff"):
        """Create a modern statistics card similar to the reference design"""
        card = QFrame()
        card.setObjectName("ModernStatCard")
        card.setFixedHeight(140)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 16)
        layout.setSpacing(12)
        
        # Header row with icon and title
        header_row = QHBoxLayout()
        header_row.setSpacing(8)
        
        if icon:
            icon_label = QLabel(icon)
            icon_label.setStyleSheet(f"font-size: 20px; background: transparent;")
            header_row.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: #8c7fa6;
            font-size: 11px;
            font-family: 'Segoe UI';
            font-weight: 500;
            background: transparent;
        """)
        header_row.addWidget(title_label)
        header_row.addStretch()
        
        layout.addLayout(header_row)
        
        # Value (large, prominent)
        if value:
            value_label = QLabel(value)
            value_label.setStyleSheet(f"""
                color: {color};
                font-size: 28px;
                font-weight: bold;
                font-family: 'Segoe UI';
                background: transparent;
            """)
            layout.addWidget(value_label)
        
        # Subtitle/trend
        if subtitle:
            subtitle_label = QLabel(subtitle)
            subtitle_label.setStyleSheet("""
                color: #645585;
                font-size: 10px;
                font-family: 'Segoe UI';
                background: transparent;
            """)
            layout.addWidget(subtitle_label)
        
        layout.addStretch()
        
        return card, layout

    # ── Helper: create action card ───────────────────────────────────────────
    def create_action_card(self, title, description="", icon=""):
        """Create an action card with button"""
        card = QFrame()
        card.setObjectName("ActionCard")
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)
        
        # Icon and title
        header = QHBoxLayout()
        if icon:
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 24px; background: transparent;")
            header.addWidget(icon_lbl)
        
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("""
            color: #ffffff;
            font-size: 14px;
            font-weight: bold;
            font-family: 'Segoe UI';
            background: transparent;
        """)
        header.addWidget(title_lbl)
        header.addStretch()
        
        layout.addLayout(header)
        
        # Description
        if description:
            desc_lbl = QLabel(description)
            desc_lbl.setStyleSheet("""
                color: #8c7fa6;
                font-size: 10px;
                font-family: 'Segoe UI';
                background: transparent;
            """)
            desc_lbl.setWordWrap(True)
            layout.addWidget(desc_lbl)
        
        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #251d3a; max-height: 1px;")
        sep.setFixedHeight(1)
        layout.addWidget(sep)
        
        return card, layout

    # ── Helper: create mini progress bar ─────────────────────────────────────
    def create_mini_progress_bar(self, label, color):
        """Create a compact progress bar widget"""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # Label row
        label_row = QHBoxLayout()
        lbl = QLabel(label)
        lbl.setStyleSheet(f"color: {color}; font-size: 10px; font-weight: bold;")
        label_row.addWidget(lbl)
        label_row.addStretch()
        value_lbl = QLabel("0%")
        value_lbl.setStyleSheet("color: #8c7fa6; font-size: 10px; font-family: 'Consolas';")
        label_row.addWidget(value_lbl)
        layout.addLayout(label_row)
        
        # Progress bar
        bar = QProgressBar()
        bar.setRange(0, 100)
        bar.setValue(0)
        bar.setFormat("")
        bar.setFixedHeight(6)
        bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: #1e1730;
                border: none;
                border-radius: 3px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 3px;
            }}
        """)
        layout.addWidget(bar)
        
        return container

    # ── Legacy: create a card (deprecated, use create_action_card instead) ───
    def create_card(self, title, subtext="Quick Actions", icon=""):
        card_frame = QFrame()
        card_frame.setObjectName("DashboardCard")

        card_layout = QVBoxLayout(card_frame)
        card_layout.setContentsMargins(20, 18, 20, 18)
        card_layout.setSpacing(14)

        # Header row with icon + title + subtitle
        header_layout = QHBoxLayout()
        if icon:
            icon_lbl = QLabel(icon)
            icon_lbl.setStyleSheet("font-size: 18px; background: transparent;")
            header_layout.addWidget(icon_lbl)

        title_block = QVBoxLayout()
        title_block.setSpacing(2)
        title_lbl = QLabel(title)
        title_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #ffffff; font-family: 'Segoe UI'; background: transparent;")
        title_block.addWidget(title_lbl)
        sub_lbl = QLabel(subtext)
        sub_lbl.setStyleSheet("font-size: 9px; color: #645585; font-family: 'Segoe UI'; background: transparent;")
        title_block.addWidget(sub_lbl)
        header_layout.addLayout(title_block)
        header_layout.addStretch()

        card_layout.addLayout(header_layout)

        # Separator line under header
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #251d3a; max-height: 1px;")
        sep.setFixedHeight(1)
        card_layout.addWidget(sep)

        return card_frame, card_layout

    # ── Helper: section description label ────────────────────────────────────
    def _desc(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #645585; font-size: 10px; font-family: 'Segoe UI'; font-style: italic; background: transparent;")
        lbl.setWordWrap(True)
        return lbl

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 0 — Dashboard
    # ══════════════════════════════════════════════════════════════════════════
    def init_core_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        # Page header
        header_section = QHBoxLayout()
        page_title = QLabel("📊 Dashboard Overview")
        page_title.setStyleSheet("""
            color: #ffffff;
            font-size: 20px;
            font-weight: bold;
            font-family: 'Segoe UI';
        """)
        header_section.addWidget(page_title)
        header_section.addStretch()
        
        # Date/time badge
        time_badge = QLabel(datetime.now().strftime("%I:%M %p - %d %B %Y"))
        time_badge.setStyleSheet("""
            color: #8c7fa6;
            font-size: 11px;
            font-family: 'Segoe UI';
            padding: 4px 12px;
            background-color: #171226;
            border-radius: 6px;
        """)
        header_section.addWidget(time_badge)
        
        main_layout.addLayout(header_section)

        # Top stats row - 4 cards
        stats_row = QHBoxLayout()
        stats_row.setSpacing(14)
        
        # CPU Card
        cpu_card, cpu_layout = self.create_modern_card(
            "CPU Usage", "0%", "-2.5%", "⚡", "#7b61ff"
        )
        self.cpu_stat_card = cpu_card
        cpu_value_item = cpu_layout.itemAt(1)
        self.cpu_value_label = cpu_value_item.widget() if cpu_value_item is not None else None
        cpu_trend_item = cpu_layout.itemAt(2)
        self.cpu_trend_label = cpu_trend_item.widget() if cpu_trend_item is not None else None
        stats_row.addWidget(cpu_card, stretch=1)
        
        # Memory Card
        mem_card, mem_layout = self.create_modern_card(
            "Memory", "0%", "+1.2%", "🧠", "#61ffcf"
        )
        self.mem_stat_card = mem_card
        mem_value_item = mem_layout.itemAt(1)
        self.mem_value_label = mem_value_item.widget() if mem_value_item is not None else None
        mem_trend_item = mem_layout.itemAt(2)
        self.mem_trend_label = mem_trend_item.widget() if mem_trend_item is not None else None
        stats_row.addWidget(mem_card, stretch=1)
        
        # Processes Card
        proc_card, proc_layout = self.create_modern_card(
            "Processes", "0", "Active", "🔄", "#ff8c61"
        )
        self.proc_stat_card = proc_card
        proc_value_item = proc_layout.itemAt(1)
        self.proc_value_label = proc_value_item.widget() if proc_value_item is not None else None
        proc_trend_item = proc_layout.itemAt(2)
        self.proc_trend_label = proc_trend_item.widget() if proc_trend_item is not None else None
        stats_row.addWidget(proc_card, stretch=1)
        
        # Storage Card
        store_card, store_layout = self.create_modern_card(
            "Storage", "64%", "Used", "💾", "#ffd93d"
        )
        self.store_stat_card = store_card
        stats_row.addWidget(store_card, stretch=1)
        
        main_layout.addLayout(stats_row)

        # Middle section - Two columns
        middle_row = QHBoxLayout()
        middle_row.setSpacing(16)
        
        # Left: System Controls
        sys_card, sys_layout = self.create_action_card(
            "Windows Management",
            "System hooks and window anchors",
            "🪟"
        )
        
        self.chk_startup = QCheckBox("Initialize on System Bootup")
        self.chk_startup.setStyleSheet("color: #c9bedf; font-size: 11px; spacing: 6px;")
        sys_layout.addWidget(self.chk_startup)
        
        self.chk_clipboard = QCheckBox("Clipboard Interception Active")
        self.chk_clipboard.setChecked(True)
        self.chk_clipboard.setStyleSheet("color: #c9bedf; font-size: 11px; spacing: 6px;")
        sys_layout.addWidget(self.chk_clipboard)
        
        btn_pin = QPushButton("📌 Pin Window Always On Top")
        btn_pin.setObjectName("ActionButton")
        btn_pin.setFixedHeight(38)
        btn_pin.clicked.connect(lambda: self.cast_asynchronously(
            lambda: __import__('incantations').window_anchors.pin_active_window()
        ))
        sys_layout.addWidget(btn_pin)
        
        middle_row.addWidget(sys_card, stretch=1)
        
        # Right: Telemetry
        telem_card, telem_layout = self.create_action_card(
            "Telemetry Control",
            "Real-time system monitoring",
            "📈"
        )
        
        # Mini progress bars
        self.mini_cpu_bar = self.create_mini_progress_bar("CPU", "#7b61ff")
        telem_layout.addWidget(self.mini_cpu_bar)
        
        self.mini_mem_bar = self.create_mini_progress_bar("Memory", "#61ffcf")
        telem_layout.addWidget(self.mini_mem_bar)
        
        self.mini_swap_bar = self.create_mini_progress_bar("Swap", "#ff8c61")
        telem_layout.addWidget(self.mini_swap_bar)
        
        btn_telemetry = QPushButton("🔍 Refresh Metrics")
        btn_telemetry.setObjectName("ActionButton")
        btn_telemetry.setFixedHeight(38)
        btn_telemetry.clicked.connect(lambda: self.cast_asynchronously(
            lambda: __import__('incantations').system_monitors.get_system_metrics()
        ))
        telem_layout.addWidget(btn_telemetry)
        
        middle_row.addWidget(telem_card, stretch=1)
        
        main_layout.addLayout(middle_row)
        
        main_layout.addStretch()
        self.workspace_stack.addTab(page, "Dashboard")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 1 — File Alchemy
    # ══════════════════════════════════════════════════════════════════════════
    def init_alchemy_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        page_header = QLabel("🧪  FILE ALCHEMY")
        page_header.setStyleSheet("color: #7b61ff; font-size: 14px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI';")
        main_layout.addWidget(page_header)
        main_layout.addWidget(self._desc("Automated file sorting, transmutation, and filesystem operations."))

        # Card 1: Directory Sorting
        card_dir, layout_dir = self.create_card("Directory Sorting Vector", "Organize files by type, date, or custom rules", "📁")
        path_row = QHBoxLayout()
        path_row.addWidget(QLabel("Target Path:"))
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads")
        path_row.addWidget(self.txt_path, stretch=1)
        btn_browse_dir = QPushButton("📁 Browse")
        btn_browse_dir.setFixedWidth(90)
        btn_browse_dir.clicked.connect(lambda: self._browse_folder(self.txt_path))
        path_row.addWidget(btn_browse_dir)
        layout_dir.addLayout(path_row)

        # Sort options row
        opts_row = QHBoxLayout()
        self.chk_sort_ext = QCheckBox("By Extension")
        self.chk_sort_ext.setChecked(True)
        self.chk_sort_date = QCheckBox("By Date")
        self.chk_sort_size = QCheckBox("By Size")
        opts_row.addWidget(self.chk_sort_ext)
        opts_row.addWidget(self.chk_sort_date)
        opts_row.addWidget(self.chk_sort_size)
        opts_row.addStretch()
        layout_dir.addLayout(opts_row)

        btn_run_sort = QPushButton("⚗️  Execute File Alchemy Sorting")
        btn_run_sort.clicked.connect(lambda: self.cast_asynchronously(lambda p: __import__('incantations').file_alchemy.transmute_folder(p), self.txt_path.text()))
        layout_dir.addWidget(btn_run_sort)
        main_layout.addWidget(card_dir)

        # Card 2: Batch Rename
        card_rename, layout_rename = self.create_card("Batch Rename Engine", "Pattern-based file renaming", "✏️")
        rename_row = QHBoxLayout()
        rename_row.addWidget(QLabel("Find:"))
        self.txt_rename_find = QLineEdit("")
        rename_row.addWidget(self.txt_rename_find)
        rename_row.addWidget(QLabel("Replace:"))
        self.txt_rename_replace = QLineEdit("")
        rename_row.addWidget(self.txt_rename_replace)
        layout_rename.addLayout(rename_row)
        btn_rename = QPushButton("✏️  Execute Batch Rename")
        btn_rename.clicked.connect(lambda: self.log_output("Batch rename queued (connect to incantations)"))
        layout_rename.addWidget(btn_rename)
        main_layout.addWidget(card_rename)

        # Card 3: Duplicate Finder
        card_dup, layout_dup = self.create_card("Duplicate Finder", "Scan for redundant files", "🔍")
        layout_dup.addWidget(self._desc("Scans the target directory for files with matching hashes. Results will appear in the log."))
        btn_find_dup = QPushButton("🔍  Scan for Duplicates")
        btn_find_dup.clicked.connect(lambda: self.log_output("Duplicate scan queued (connect to incantations)"))
        layout_dup.addWidget(btn_find_dup)
        main_layout.addWidget(card_dup)

        main_layout.addStretch()
        self.workspace_stack.addTab(page, "File Alchemy")

    def _browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            line_edit.setText(folder)

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 2 — Visual Alchemy
    # ══════════════════════════════════════════════════════════════════════════
    def init_visual_alchemy_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(12)

        page_header = QLabel("👁️  VISUAL ALCHEMY")
        page_header.setStyleSheet("color: #7b61ff; font-size: 14px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI';")
        main_layout.addWidget(page_header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        inner_widget = QWidget()
        content_layout = QVBoxLayout(inner_widget)
        content_layout.setSpacing(12)

        # Visual Manipulation
        group_manip = QGroupBox("🖼️  Visual Manipulation Chamber")
        layout_manip = QVBoxLayout(group_manip)
        layout_manip.setSpacing(10)
        path_row = QHBoxLayout()
        path_row.addWidget(QLabel("Image Path:"))
        self.txt_img_path = QLineEdit(r"C:\Users\Public\Grimoire_Procedural_Logo.png")
        path_row.addWidget(self.txt_img_path, stretch=1)
        btn_browse = QPushButton("📁 Browse")
        btn_browse.setFixedWidth(90)
        btn_browse.clicked.connect(self.browse_for_image)
        path_row.addWidget(btn_browse)
        layout_manip.addLayout(path_row)

        btn_bg = QPushButton("🖼️  Erase Image Background (Transparent PNG)")
        btn_bg.clicked.connect(lambda: self.cast_asynchronously(lambda p: __import__('incantations').image_matrix.erase_background(p), self.txt_img_path.text()))
        layout_manip.addWidget(btn_bg)
        content_layout.addWidget(group_manip)

        # Giphy & Sticker Suite
        group_giphy = QGroupBox("🎭  Giphy & Sticker Suite")
        layout_giphy = QVBoxLayout(group_giphy)
        layout_giphy.setSpacing(10)
        layout_giphy.addWidget(QLabel("Giphy Query:"))
        self.txt_gif_query = QLineEdit("creepy cute sticker")
        layout_giphy.addWidget(self.txt_gif_query)
        gif_row = QHBoxLayout()
        btn_find_gif = QPushButton("🔍  Search Giphy Streams")
        btn_find_gif.clicked.connect(lambda: self.cast_asynchronously(lambda q: __import__('incantations').image_matrix.search_giphy(q), self.txt_gif_query.text()))
        gif_row.addWidget(btn_find_gif)
        btn_pack_sticker = QPushButton("🏷️  Format & Copy Sticker")
        btn_pack_sticker.clicked.connect(lambda: self.cast_asynchronously(lambda p, t: __import__('incantations').image_matrix.format_sticker_package(p, t), self.txt_img_path.text(), "discord"))
        gif_row.addWidget(btn_pack_sticker)
        layout_giphy.addLayout(gif_row)
        content_layout.addWidget(group_giphy)

        # Pixelation Modulator
        group_pixel = QGroupBox("👾  Pixelation Modulator")
        layout_pixel = QVBoxLayout(group_pixel)
        layout_pixel.setSpacing(10)
        slider_row = QHBoxLayout()
        slider_row.addWidget(QLabel("Pixel Size:"))
        self.slider_pixel = QSlider(Qt.Orientation.Horizontal)
        self.slider_pixel.setRange(2, 32)
        self.slider_pixel.setValue(8)
        slider_row.addWidget(self.slider_pixel, stretch=1)
        self.pixel_val_lbl = QLabel("8px")
        self.pixel_val_lbl.setStyleSheet("color: #7b61ff; font-family: 'Consolas'; font-weight: bold; min-width: 30px;")
        self.slider_pixel.valueChanged.connect(lambda v: self.pixel_val_lbl.setText(f"{v}px"))
        slider_row.addWidget(self.pixel_val_lbl)
        layout_pixel.addLayout(slider_row)
        btn_pixel_art = QPushButton("👾  Transmute Image to Pixel Art")
        btn_pixel_art.clicked.connect(lambda: self.cast_asynchronously(lambda p, s: __import__('incantations').image_matrix.apply_pixel_art_slider(p, s), self.txt_img_path.text(), self.slider_pixel.value()))
        layout_pixel.addWidget(btn_pixel_art)
        content_layout.addWidget(group_pixel)

        # Offline AI & Toy Forge
        group_ai = QGroupBox("🤖  Offline AI & Toy Forge")
        layout_ai = QVBoxLayout(group_ai)
        layout_ai.setSpacing(10)
        layout_ai.addWidget(QLabel("AI Prompt:"))
        self.txt_ai_prompt = QLineEdit("gothic cottagecore item plush")
        layout_ai.addWidget(self.txt_ai_prompt)
        ai_row = QHBoxLayout()
        btn_offline_ai = QPushButton("🎨  Offline AI Render (:7860)")
        btn_offline_ai.clicked.connect(lambda: self.cast_asynchronously(lambda pr: __import__('incantations').asset_summoner.local_offline_ai_forge(pr), self.txt_ai_prompt.text()))
        ai_row.addWidget(btn_offline_ai)
        btn_plush = QPushButton("🧸  To Plush")
        btn_plush.clicked.connect(lambda: self.cast_asynchronously(lambda p, m: __import__('incantations').image_matrix.transmute_to_plush_or_crochet(p, m), self.txt_img_path.text(), "plush"))
        ai_row.addWidget(btn_plush)
        btn_crochet = QPushButton("🧶  To Crochet")
        btn_crochet.clicked.connect(lambda: self.cast_asynchronously(lambda p, m: __import__('incantations').image_matrix.transmute_to_plush_or_crochet(p, m), self.txt_img_path.text(), "crochet"))
        ai_row.addWidget(btn_crochet)
        layout_ai.addLayout(ai_row)
        content_layout.addWidget(group_ai)

        content_layout.addStretch()
        scroll.setWidget(inner_widget)
        main_layout.addWidget(scroll, stretch=1)

        # Status log
        log_header = QLabel("📋 SYSTEM RESPONSE LOG")
        log_header.setStyleSheet("color: #645585; font-size: 9px; font-weight: bold; letter-spacing: 1px;")
        main_layout.addWidget(log_header)
        self.status_log = QTextEdit()
        self.status_log.setReadOnly(True)
        self.status_log.setMaximumHeight(110)
        self.status_log.setPlaceholderText("Awaiting operations...")
        self.status_log.setStyleSheet("""
            QTextEdit {
                background-color: #0b0813;
                color: #61ffcf;
                border: 1px solid #1f1833;
                border-radius: 6px;
                font-family: 'Consolas';
                font-size: 10px;
                padding: 8px;
            }
        """)
        main_layout.addWidget(self.status_log)

        self.workspace_stack.addTab(page, "Visual Alchemy")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 3 — Deployment
    # ══════════════════════════════════════════════════════════════════════════
    def init_deployment_architect_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        page_header = QLabel("🚀  DEPLOYMENT ARCHITECT")
        page_header.setStyleSheet("color: #7b61ff; font-size: 14px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI';")
        main_layout.addWidget(page_header)
        main_layout.addWidget(self._desc("System backup, restore points, and automated software deployment."))

        # Two-column layout
        two_col = QHBoxLayout()
        two_col.setSpacing(16)

        # Left: Backup & Restore
        card_rep, layout_rep = self.create_card("OS Deployment Replicator", "Backup & Restore", "🛡️")
        btn_restore = QPushButton("🛡️  Generate Safe System Restore Checkpoint")
        btn_restore.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').deep_cleaner.drop_system_restore_anchor()))
        layout_rep.addWidget(btn_restore)
        btn_export_apps = QPushButton("📋  Export Installed Software Configuration List")
        btn_export_apps.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').deep_cleaner.export_installed_software_replica()))
        layout_rep.addWidget(btn_export_apps)
        layout_rep.addStretch()
        two_col.addWidget(card_rep, stretch=1)

        # Right: Bulk Installer
        card_bulk, layout_bulk = self.create_card("Silent Bulk Installer", "Automated Deployment Loop", "📦")
        layout_bulk.addWidget(QLabel("Installation Manifest (one entry per line):"))
        self.txt_todo_replica = QTextEdit()
        self.txt_todo_replica.setPlainText("[ ] REINSTALL: GoogleChrome\n[ ] REINSTALL: VLC\n[ ] REINSTALL: Steam\n[ ] REINSTALL: Discord")
        self.txt_todo_replica.setMaximumHeight(140)
        layout_bulk.addWidget(self.txt_todo_replica)
        btn_run_bulk = QPushButton("🚀  Run Automated Silent Bulk Installer Loop")
        btn_run_bulk.clicked.connect(lambda: self.cast_asynchronously(lambda t: __import__('incantations').deep_cleaner.execute_silent_bulk_installer_exe(t), self.txt_todo_replica.toPlainText()))
        layout_bulk.addWidget(btn_run_bulk)
        two_col.addWidget(card_bulk, stretch=1)

        main_layout.addLayout(two_col)
        main_layout.addStretch()

        self.workspace_stack.addTab(page, "Deployment")

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 4 — Task Viewer
    # ══════════════════════════════════════════════════════════════════════════
    def init_task_viewer_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(12)

        page_header = QLabel("🧠  TASK VIEWER")
        page_header.setStyleSheet("color: #7b61ff; font-size: 14px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI';")
        main_layout.addWidget(page_header)

        # Toolbar row: search + filter + kill
        toolbar = QHBoxLayout()
        toolbar.setSpacing(10)

        self.txt_process_filter = QLineEdit()
        self.txt_process_filter.setPlaceholderText("🔍  Filter processes by name...")
        self.txt_process_filter.setFixedHeight(30)
        self.txt_process_filter.textChanged.connect(self._filter_processes)
        self.txt_process_filter.setStyleSheet("""
            QLineEdit {
                background-color: #1e1730; color: #a397bf; border: 1px solid #2d2349;
                border-radius: 6px; padding: 4px 10px; font-size: 11px;
            }
        """)
        toolbar.addWidget(self.txt_process_filter, stretch=1)

        self.lbl_process_count = QLabel("0 processes")
        self.lbl_process_count.setStyleSheet("color: #645585; font-size: 10px; font-family: 'Consolas';")
        toolbar.addWidget(self.lbl_process_count)

        btn_refresh = QPushButton("🔄 Refresh")
        btn_refresh.setFixedHeight(30)
        btn_refresh.setFixedWidth(90)
        btn_refresh.clicked.connect(lambda: self.refresh_process_view())
        toolbar.addWidget(btn_refresh)

        btn_kill_selected = QPushButton("✕ Kill Selected")
        btn_kill_selected.setObjectName("KillSelectedButton")
        btn_kill_selected.setFixedHeight(30)
        btn_kill_selected.setFixedWidth(110)
        btn_kill_selected.clicked.connect(self.kill_selected_process)
        toolbar.addWidget(btn_kill_selected)

        main_layout.addLayout(toolbar)

        # Process table
        self.process_table = QTableWidget(0, 5)
        self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Mem %", "Action"])
        horizontal_header = self.process_table.horizontalHeader()
        if horizontal_header is not None:
            horizontal_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            horizontal_header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
            horizontal_header.resizeSection(4, 80)
        self.process_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.process_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.process_table.setAlternatingRowColors(True)
        vertical_header = self.process_table.verticalHeader()
        if vertical_header is not None:
            vertical_header.setVisible(False)
        main_layout.addWidget(self.process_table, stretch=1)

        self.workspace_stack.addTab(page, "Task Viewer")

    def _filter_processes(self, text):
        """Simple client-side filter for the process table."""
        if not hasattr(self, 'process_table'):
            return
        filter_text = text.lower().strip()
        for row in range(self.process_table.rowCount()):
            name_item = self.process_table.item(row, 1)
            if name_item:
                match = filter_text == "" or filter_text in name_item.text().lower()
                self.process_table.setRowHidden(row, not match)

    # ══════════════════════════════════════════════════════════════════════════
    #  TAB 5 — Arcane Tuning
    # ══════════════════════════════════════════════════════════════════════════
    def init_tuning_tab(self):
        page = QWidget()
        main_layout = QVBoxLayout(page)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(16)

        page_header = QLabel("⚙️  ARCANE TUNING")
        page_header.setStyleSheet("color: #7b61ff; font-size: 14px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI';")
        main_layout.addWidget(page_header)
        main_layout.addWidget(self._desc("System policies, registry guards, and advanced configuration."))

        # Two-column
        two_col = QHBoxLayout()
        two_col.setSpacing(16)

        # Left: Registry & Policies
        card_guard, layout_guard = self.create_card("System Policy Shields", "Registry Security & Bloatware Prevention", "🔒")
        btn_policies = QPushButton("🔒  Inject Registry Policy Guards Against Auto-Bloatware")
        btn_policies.clicked.connect(lambda: self.cast_asynchronously(lambda: __import__('incantations').persistent_bans.freeze_windows_bloatware_policies()))
        layout_guard.addWidget(btn_policies)

        btn_disable_telemetry = QPushButton("📡  Disable Windows Telemetry & Tracking")
        btn_disable_telemetry.clicked.connect(lambda: self.log_output("Telemetry disable queued (connect to incantations)"))
        layout_guard.addWidget(btn_disable_telemetry)

        btn_disable_cortana = QPushButton("🤐  Disable Cortana & Search Indexing")
        btn_disable_cortana.clicked.connect(lambda: self.log_output("Cortana disable queued (connect to incantations)"))
        layout_guard.addWidget(btn_disable_cortana)
        layout_guard.addStretch()
        two_col.addWidget(card_guard, stretch=1)

        # Right: Performance & Startup
        card_perf, layout_perf = self.create_card("Performance Tuning", "Startup & Services", "⚡")

        self.chk_disable_animations = QCheckBox(" Disable Windows UI Animations")
        self.chk_disable_animations.setChecked(False)
        layout_perf.addWidget(self.chk_disable_animations)

        self.chk_disable_transparency = QCheckBox(" Disable Transparency Effects")
        layout_perf.addWidget(self.chk_disable_transparency)

        self.chk_high_perf = QCheckBox(" Set Power Plan to High Performance")
        layout_perf.addWidget(self.chk_high_perf)

        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("background-color: #251d3a; max-height: 1px;")
        sep.setFixedHeight(1)
        layout_perf.addWidget(sep)

        btn_apply_tuning = QPushButton("⚡  Apply Performance Tuning")
        btn_apply_tuning.clicked.connect(lambda: self.log_output("Performance tuning applied (connect to incantations)"))
        layout_perf.addWidget(btn_apply_tuning)
        layout_perf.addStretch()
        two_col.addWidget(card_perf, stretch=1)

        main_layout.addLayout(two_col)
        main_layout.addStretch()

        self.workspace_stack.addTab(page, "Arcane Tuning")

    # ── Theme ────────────────────────────────────────────────────────────────
    def apply_theme(self):
        self.setStyleSheet("""
            QWidget#MainContainer {
                background-color: #0b0813;
                border: 1px solid #1f1833;
                border-radius: 12px;
            }

            QFrame#CustomTitleBar {
                background-color: #0b0813;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom: 1px solid #140f24;
            }

            QFrame#SidebarDock {
                background-color: #120e1f;
                border-right: 1px solid #1f1833;
                border-bottom-left-radius: 11px;
            }

            /* Modern Stat Cards */
            QFrame#ModernStatCard {
                background-color: #171226;
                border: 1px solid #251d3a;
                border-radius: 16px;
            }
            QFrame#ModernStatCard:hover {
                border-color: #7b61ff;
                background-color: #1a1430;
            }

            /* Action Cards */
            QFrame#ActionCard {
                background-color: #171226;
                border: 1px solid #251d3a;
                border-radius: 14px;
            }
            QFrame#ActionCard:hover {
                border-color: #61ffcf;
            }

            /* Action Buttons */
            QPushButton#ActionButton {
                background-color: #211936;
                color: #7b61ff;
                font-weight: 600;
                border: 1px solid #322652;
                border-radius: 8px;
                padding: 8px 16px;
                font-family: 'Segoe UI';
                font-size: 11px;
            }
            QPushButton#ActionButton:hover {
                background-color: #7b61ff;
                color: #ffffff;
                border-color: #7b61ff;
            }

            /* Keep existing styles for other elements... */
            QTabWidget::panel { background-color: #0b0813; border: none; }

            QLabel {
                color: #a397bf;
                font-family: 'Segoe UI';
                font-size: 11px;
                background: transparent;
            }

            QCheckBox {
                color: #c9bedf;
                font-family: 'Segoe UI';
                font-size: 11px;
                background: transparent;
                spacing: 6px;
            }
            QCheckBox::indicator {
                width: 14px; height: 14px; border-radius: 3px;
                border: 1px solid #322652; background: #1e1730;
            }
            QCheckBox::indicator:checked {
                background: #7b61ff; border-color: #7b61ff;
            }

            QLineEdit {
                background-color: #1e1730;
                color: #61ffcf;
                border: 1px solid #2d2349;
                border-radius: 6px;
                padding: 8px 12px;
                font-family: 'Consolas';
                font-size: 11px;
            }
            QLineEdit:focus {
                border-color: #7b61ff;
            }

            QPushButton {
                background-color: #211936;
                color: #7b61ff;
                font-weight: bold;
                border: 1px solid #322652;
                border-radius: 8px;
                padding: 8px 16px;
                font-family: 'Segoe UI';
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #7b61ff;
                color: #ffffff;
                border-color: #7b61ff;
            }

            QProgressBar {
                background-color: #1e1730;
                color: #ffffff;
                border: 1px solid #2d2349;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background-color: #7b61ff;
                border-radius: 5px;
            }

            QTableWidget {
                background-color: #0e0a19;
                color: #c9bedf;
                border: 1px solid #1f1833;
                border-radius: 8px;
                gridline-color: #1a1430;
                font-size: 10px;
            }
            QHeaderView::section {
                background-color: #171226;
                color: #7b61ff;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 10px;
                font-family: 'Segoe UI';
            }
        """)


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = GrimoireMirror()
    window.show()
    sys.exit(app.exec())
