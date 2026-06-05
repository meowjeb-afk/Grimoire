from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QLineEdit, QPushButton, 
    QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QCheckBox, QSlider, 
    QSpinBox, QScrollArea, QGroupBox, QFileDialog, QSizePolicy
)
from PyQt6.QtCore import Qt

class DashboardMixin:
    def init_core_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        top_bar = QHBoxLayout()
        # FIX: Logo text sizing
        page_title = self.ColorPreservingLabel(self.logo_text_path)
        page_title.setFixedHeight(40)
        page_title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        top_bar.addWidget(page_title); top_bar.addStretch(); main_layout.addLayout(top_bar)
        
        stats_row = QHBoxLayout(); stats_row.setSpacing(12); self.dashboard_stat_labels = {}
        cards_data = [("CPU Usage", "cpu", "#7b61ff", ""), ("Memory Usage", "memory", "#61ffcf", "🧠"), ("Storage Used", "storage", "#ff8c61", ""), ("Processes", "processes", "#ffd93d", "🔄")]
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
        self.performance_chart = self.PerformanceChart(); chart_layout = QVBoxLayout(); chart_layout.addWidget(self.performance_chart, stretch=1)
        chart_container = QFrame(); chart_container.setObjectName("ChartCard"); chart_container.setLayout(chart_layout); content_row.addWidget(chart_container, stretch=2)
        main_layout.addLayout(content_row, stretch=1)
        self.workspace_stack.addTab(page, "Dashboard")

class FileAlchemyMixin:
    def init_alchemy_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        header = QHBoxLayout(); page_header = QLabel("🧪 FILE ALCHEMY"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); header.addWidget(page_header); header.addStretch(); main_layout.addLayout(header)
        card_dir, layout_dir = self.create_card(" Directory Sorting Vector", "Organize files by type, date, or custom rules", "")
        path_row = QHBoxLayout(); path_lbl = QLabel("Target Path:"); path_row.addWidget(path_lbl)
        self.txt_path = QLineEdit(r"C:\Users\Public\Downloads"); path_row.addWidget(self.txt_path, stretch=1)
        btn_browse_dir = QPushButton("📁 Browse"); btn_browse_dir.setFixedWidth(90); btn_browse_dir.setObjectName("ActionButton")
        btn_browse_dir.clicked.connect(lambda: self.txt_path.setText(QFileDialog.getExistingDirectory(self, "Select Folder"))); path_row.addWidget(btn_browse_dir); layout_dir.addLayout(path_row)
        btn_run_sort = QPushButton("⚗️ Execute File Alchemy Sorting"); btn_run_sort.setObjectName("ActionButton"); layout_dir.addWidget(btn_run_sort)
        card_dir.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }"); main_layout.addWidget(card_dir); main_layout.addStretch()
        self.workspace_stack.addTab(page, "File Alchemy")
class VisualAlchemyMixin:
    def init_visual_alchemy_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        page_header = QLabel("👁️ VISUAL ALCHEMY"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold; letter-spacing: 1px; font-family: 'Segoe UI'; background: transparent;")
        main_layout.addWidget(page_header)
        content_row = QHBoxLayout(); content_row.setSpacing(16)
        
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

        # 3. Color Adjustments
        group_color = QGroupBox("🎨 Color Adjustments"); group_color.setStyleSheet(group_style); layout_color = QVBoxLayout(group_color); layout_color.setSpacing(8)
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
        blur_row = QHBoxLayout(); blur_row.addWidget(QLabel("Blur:")); self.slider_blur = QSlider(Qt.Orientation.Horizontal); self.slider_blur.setRange(0, 10); self.slider_blur.setValue(2); self.slider_blur.setFixedWidth(150); blur_row.addWidget(self.slider_blur)        self.lbl_blur = QLabel("2px"); self.lbl_blur.setFixedWidth(40); blur_row.addWidget(self.lbl_blur)
        btn_apply_blur = QPushButton("Apply"); btn_apply_blur.setFixedWidth(60); btn_apply_blur.setObjectName("ActionButton"); btn_apply_blur.clicked.connect(lambda: self.apply_blur(self.slider_blur.value())); blur_row.addWidget(btn_apply_blur)
        self.slider_blur.valueChanged.connect(lambda v: self.lbl_blur.setText(f"{v}px")); layout_effects.addLayout(blur_row)
        sharpen_row = QHBoxLayout(); sharpen_row.addWidget(QLabel("Sharpen:")); self.slider_sharpen = QSlider(Qt.Orientation.Horizontal); self.slider_sharpen.setRange(0, 200); self.slider_sharpen.setValue(100); self.slider_sharpen.setFixedWidth(150); sharpen_row.addWidget(self.slider_sharpen)
        self.lbl_sharpen = QLabel("1.0x"); self.lbl_sharpen.setFixedWidth(40); sharpen_row.addWidget(self.lbl_sharpen)
        btn_apply_sharpen = QPushButton("Apply"); btn_apply_sharpen.setFixedWidth(60); btn_apply_sharpen.setObjectName("ActionButton"); btn_apply_sharpen.clicked.connect(lambda: self.apply_sharpen(self.slider_sharpen.value() / 100.0)); sharpen_row.addWidget(btn_apply_sharpen)
        self.slider_sharpen.valueChanged.connect(lambda v: self.lbl_sharpen.setText(f"{v/100:.1f}x")); layout_effects.addLayout(sharpen_row)
        content_layout.addWidget(group_effects)

        # 5. AI & Production Suite
        group_ai_suite = QGroupBox("🤖 AI & Production Suite"); group_ai_suite.setStyleSheet(group_style); layout_ai_suite = QVBoxLayout(group_ai_suite); layout_ai_suite.setSpacing(10)
        if not self.HEAVY_DEPS_AVAILABLE or self.design_suite is None:
            ai_warning = QLabel("⚠️ AI dependencies missing. Install via: pip install opencv-python torch diffusers rembg"); ai_warning.setStyleSheet("color: #ff6b6b; font-size: 10px; background: transparent;"); ai_warning.setWordWrap(True); layout_ai_suite.addWidget(ai_warning)
        else:
            btn_isolate = QPushButton("✂️ AI Subject Isolator (Remove Background)"); btn_isolate.setObjectName("ActionButton"); btn_isolate.clicked.connect(self.run_subject_isolator); layout_ai_suite.addWidget(btn_isolate)
            upscale_row = QHBoxLayout(); upscale_row.addWidget(QLabel("AI Upscale Factor:")); self.spin_upscale = QSpinBox(); self.spin_upscale.setRange(2, 4); self.spin_upscale.setValue(2); self.spin_upscale.setFixedWidth(60); upscale_row.addWidget(self.spin_upscale)
            btn_upscale = QPushButton("⬆️ Super Resolution Upscale"); btn_upscale.setObjectName("ActionButton"); btn_upscale.clicked.connect(self.run_upscaler); upscale_row.addWidget(btn_upscale); upscale_row.addStretch(); layout_ai_suite.addLayout(upscale_row)
            btn_tiler = QPushButton("🔄 Generate Seamless Texture Tile"); btn_tiler.setObjectName("ActionButton"); btn_tiler.clicked.connect(self.run_seamless_tiler); layout_ai_suite.addWidget(btn_tiler)
            palette_row = QHBoxLayout(); btn_palette = QPushButton("🎨 Extract Color Palette"); btn_palette.setObjectName("ActionButton"); btn_palette.clicked.connect(self.run_palette_harmonizer); palette_row.addWidget(btn_palette)
            self.lbl_palette_output = QLabel("No palette extracted yet."); self.lbl_palette_output.setStyleSheet("color: #61ffcf; font-size: 10px; font-family: 'Consolas'; background: transparent;"); palette_row.addWidget(self.lbl_palette_output); palette_row.addStretch(); layout_ai_suite.addLayout(palette_row)
            style_row = QHBoxLayout(); style_row.addWidget(QLabel("Style Prompt:")); self.txt_style_prompt = QLineEdit("cyberpunk, neon lights, highly detailed"); style_row.addWidget(self.txt_style_prompt, stretch=1)
            btn_style = QPushButton("✨ Apply Style Transfer"); btn_style.setObjectName("ActionButton"); btn_style.clicked.connect(self.run_style_transfer); style_row.addWidget(btn_style); layout_ai_suite.addLayout(style_row)
            inpaint_row = QHBoxLayout(); inpaint_row.addWidget(QLabel("Inpaint Prompt:")); self.txt_inpaint_prompt = QLineEdit("a red apple"); inpaint_row.addWidget(self.txt_inpaint_prompt, stretch=1)
            btn_inpaint = QPushButton("️ Inpaint (Requires Mask)"); btn_inpaint.setObjectName("ActionButton"); btn_inpaint.clicked.connect(self.run_context_inpaint); inpaint_row.addWidget(btn_inpaint); layout_ai_suite.addLayout(inpaint_row)
        content_layout.addWidget(group_ai_suite)

        # 6. Advanced Production Core (NO SVG)
        group_advanced = QGroupBox("🎨 Advanced Production Core"); group_advanced.setStyleSheet(group_style); layout_advanced = QVBoxLayout(group_advanced); layout_advanced.setSpacing(10)
        if self.advanced_extensions is None:
            adv_warning = QLabel("⚠️ Advanced extensions unavailable."); adv_warning.setStyleSheet("color: #ff6b6b; font-size: 10px; background: transparent;"); layout_advanced.addWidget(adv_warning)
        else:
            btn_pbr = QPushButton("🗺️ Generate PBR Maps (Normal/Displacement)"); btn_pbr.setObjectName("ActionButton"); btn_pbr.clicked.connect(self.run_pbr_maps); layout_advanced.addWidget(btn_pbr)
            composite_row = QHBoxLayout(); composite_row.addWidget(QLabel("Background Image:")); self.txt_bg_path = QLineEdit(""); self.txt_bg_path.setPlaceholderText("Select background for compositing..."); composite_row.addWidget(self.txt_bg_path, stretch=1)
            btn_browse_bg = QPushButton(" Browse"); btn_browse_bg.setFixedWidth(70); btn_browse_bg.setObjectName("ActionButton"); btn_browse_bg.clicked.connect(self.browse_background_image); composite_row.addWidget(btn_browse_bg); layout_advanced.addLayout(composite_row)
            btn_composite = QPushButton("📐 Composite Layers"); btn_composite.setObjectName("ActionButton"); btn_composite.clicked.connect(self.run_composite_layers); layout_advanced.addWidget(btn_composite)
        content_layout.addWidget(group_advanced)

        # 7. Save & Export
        group_save = QGroupBox(" Save & Export"); group_save.setStyleSheet(group_style); layout_save = QVBoxLayout(group_save); layout_save.setSpacing(10)
        btn_save = QPushButton("💾 Save Edited Image"); btn_save.setObjectName("ActionButton"); btn_save.setFixedHeight(40); btn_save.clicked.connect(self.save_current_image); layout_save.addWidget(btn_save)
        btn_reset = QPushButton("🔄 Reset to Original"); btn_reset.setObjectName("SecondaryButton"); btn_reset.clicked.connect(self.reset_image); layout_save.addWidget(btn_reset)
        content_layout.addWidget(group_save)

        content_layout.addStretch(); scroll.setWidget(inner_widget); left_layout.addWidget(scroll, stretch=1)

        # RIGHT COLUMN: Preview
        right_column = QFrame(); right_column.setObjectName("AssetPreviewColumn"); right_column.setFixedWidth(350)
        right_layout = QVBoxLayout(right_column); right_layout.setContentsMargins(0, 0, 0, 0); right_layout.setSpacing(10)
        preview_header = QLabel("🖼️ ASSET PREVIEW BAY"); preview_header.setStyleSheet("color: #7b61ff; font-size: 12px; font-weight: bold; letter-spacing: 1px; background: transparent;"); right_layout.addWidget(preview_header)
        self.preview_window = QLabel(); self.preview_window.setObjectName("ImagePreviewBay"); self.preview_window.setAlignment(Qt.AlignmentFlag.AlignCenter); self.preview_window.setMinimumSize(310, 350); self.preview_window.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding); self.preview_window.setWordWrap(True); self.preview_window.setText("⬇\n\nDrag & Drop\nImage Here\n\nor use Browse")        self.preview_window.setStyleSheet("QLabel#ImagePreviewBay { background-color: #08060f; border: 2px dashed #251d3a; border-radius: 14px; color: #52476d; font-family: 'Segoe UI'; font-size: 11px; }"); self.preview_window.setAcceptDrops(True); right_layout.addWidget(self.preview_window, stretch=1)
        btn_browse_preview = QPushButton("📁 Browse File"); btn_browse_preview.setFixedHeight(36); btn_browse_preview.setObjectName("ActionButton"); btn_browse_preview.clicked.connect(self.browse_for_image); right_layout.addWidget(btn_browse_preview)
        info_label = QLabel("📋 Drop images or use Browse to load assets"); info_label.setStyleSheet("color: #645585; font-size: 9px; font-family: 'Segoe UI'; background: transparent;"); info_label.setAlignment(Qt.AlignmentFlag.AlignCenter); info_label.setWordWrap(True); right_layout.addWidget(info_label); right_layout.addStretch()
        content_row.addWidget(left_column, stretch=2); content_row.addWidget(right_column, stretch=1); main_layout.addLayout(content_row, stretch=1)

        # Status Log
        log_header = QLabel("📋 SYSTEM RESPONSE LOG"); log_header.setStyleSheet("color: #645585; font-size: 9px; font-weight: bold; letter-spacing: 1px; background: transparent;"); main_layout.addWidget(log_header)
        self.status_log = QTextEdit(); self.status_log.setReadOnly(True); self.status_log.setMaximumHeight(110); self.status_log.setPlaceholderText("Awaiting operations..."); self.status_log.setStyleSheet("QTextEdit { background-color: #0b0813; color: #61ffcf; border: 1px solid #1f1833; border-radius: 6px; font-family: 'Consolas'; font-size: 10px; padding: 8px; }"); main_layout.addWidget(self.status_log)
        self.workspace_stack.addTab(page, "Visual Alchemy")

class DeploymentMixin:
    def init_deployment_architect_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(16)
        page_header = QLabel("🚀 DEPLOYMENT ARCHITECT"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); main_layout.addWidget(page_header)
        two_col = QHBoxLayout(); two_col.setSpacing(16)
        card_rep, layout_rep = self.create_card("OS Deployment Replicator", "Backup & Restore", "️"); card_rep.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }")
        btn_restore = QPushButton("🛡️ Generate Safe System Restore Checkpoint"); btn_restore.setObjectName("ActionButton"); layout_rep.addWidget(btn_restore); layout_rep.addStretch(); two_col.addWidget(card_rep, stretch=1)
        card_bulk, layout_bulk = self.create_card("Silent Bulk Installer", "Automated Deployment Loop", ""); card_bulk.setStyleSheet("QFrame#DashboardCard { background-color: #171226; border: 1px solid #251d3a; border-radius: 12px; }")
        self.txt_todo_replica = QTextEdit(); self.txt_todo_replica.setPlainText("[ ] REINSTALL: GoogleChrome\n[ ] REINSTALL: VLC"); self.txt_todo_replica.setMaximumHeight(140); layout_bulk.addWidget(self.txt_todo_replica)
        btn_run_bulk = QPushButton("🚀 Run Automated Silent Bulk Installer Loop"); btn_run_bulk.setObjectName("ActionButton"); layout_bulk.addWidget(btn_run_bulk); two_col.addWidget(card_bulk, stretch=1)
        main_layout.addLayout(two_col); main_layout.addStretch(); self.workspace_stack.addTab(page, "Deployment")

class TaskViewerMixin:
    def init_task_viewer_tab(self):
        page = QWidget(); page.setStyleSheet("background-color: #0b0813;")
        main_layout = QVBoxLayout(page); main_layout.setContentsMargins(20, 16, 20, 20); main_layout.setSpacing(12)
        page_header = QLabel(" TASK VIEWER"); page_header.setStyleSheet("color: #7b61ff; font-size: 18px; font-weight: bold;"); main_layout.addWidget(page_header)
        toolbar = QHBoxLayout(); toolbar.setSpacing(10)
        self.txt_process_filter = QLineEdit(); self.txt_process_filter.setPlaceholderText("🔍 Filter processes by name..."); self.txt_process_filter.setFixedHeight(30); self.txt_process_filter.textChanged.connect(self._filter_processes); toolbar.addWidget(self.txt_process_filter, stretch=1)
        btn_refresh = QPushButton("🔄 Refresh"); btn_refresh.setFixedHeight(30); btn_refresh.setFixedWidth(90); btn_refresh.setObjectName("ActionButton"); btn_refresh.clicked.connect(lambda: self.refresh_process_view()); toolbar.addWidget(btn_refresh)
        btn_kill_selected = QPushButton("✕ Kill Selected"); btn_kill_selected.setObjectName("KillSelectedButton"); btn_kill_selected.setFixedHeight(30); btn_kill_selected.setFixedWidth(110); btn_kill_selected.clicked.connect(self.kill_selected_process); toolbar.addWidget(btn_kill_selected)
        main_layout.addLayout(toolbar)
        self.process_table = QTableWidget(0, 5); self.process_table.setHorizontalHeaderLabels(["PID", "Name", "CPU %", "Mem %", "Action"])
        if self.process_table.horizontalHeader() is not None: self.process_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.process_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows); self.process_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers); self.process_table.setAlternatingRowColors(True)
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
            try: self.kill_process(int(item.text()))            except ValueError: pass

class TuningMixin:
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
