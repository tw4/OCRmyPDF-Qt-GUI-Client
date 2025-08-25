"""
Settings Dialog - Advanced OCR settings configuration
"""

import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QGroupBox, QFormLayout, QComboBox, QCheckBox, QSpinBox,
    QSlider, QPushButton, QLabel, QLineEdit, QTextEdit,
    QDialogButtonBox, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt


class SettingsDialog(QDialog):
    """Advanced settings dialog for OCR configuration."""
    
    def __init__(self, settings, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        
        self.setWindowTitle("Advanced OCR Settings")
        self.setMinimumSize(500, 600)
        self.resize(600, 700)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self.create_ocr_tab()
        self.create_image_tab()
        self.create_output_tab()
        self.create_advanced_tab()
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.RestoreDefaults
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.RestoreDefaults).clicked.connect(self.restore_defaults)
        
        layout.addWidget(button_box)
        
    def create_ocr_tab(self):
        """Create OCR settings tab."""
        tab = QWidget()
        self.tab_widget.addTab(tab, "OCR Settings")
        
        layout = QVBoxLayout(tab)
        
        # Language settings
        lang_group = QGroupBox("Language Settings")
        lang_layout = QFormLayout(lang_group)
        
        self.language_combo = QComboBox()
        self.populate_languages()
        lang_layout.addRow("OCR Language:", self.language_combo)
        
        self.language_dir_edit = QLineEdit()
        lang_layout.addRow("Language Data Directory:", self.language_dir_edit)
        
        browse_lang_button = QPushButton("Browse...")
        browse_lang_button.clicked.connect(self.browse_language_dir)
        lang_layout.addRow("", browse_lang_button)
        
        layout.addWidget(lang_group)
        
        # Tesseract settings
        tesseract_group = QGroupBox("Tesseract Settings")
        tesseract_layout = QFormLayout(tesseract_group)
        
        self.psm_combo = QComboBox()
        self.psm_combo.addItems([
            "0 - Orientation and script detection (OSD) only",
            "1 - Automatic page segmentation with OSD",
            "2 - Automatic page segmentation, but no OSD, or OCR",
            "3 - Fully automatic page segmentation, but no OSD",
            "4 - Assume a single column of text of variable sizes",
            "5 - Assume a single uniform block of vertically aligned text",
            "6 - Assume a single uniform block of text",
            "7 - Treat the image as a single text line",
            "8 - Treat the image as a single word",
            "9 - Treat the image as a single word in a circle",
            "10 - Treat the image as a single character",
            "11 - Sparse text. Find as much text as possible",
            "12 - Sparse text with OSD",
            "13 - Raw line. Treat the image as a single text line"
        ])
        self.psm_combo.setCurrentIndex(3)  # Default PSM 3
        tesseract_layout.addRow("Page Segmentation Mode:", self.psm_combo)
        
        self.oem_combo = QComboBox()
        self.oem_combo.addItems([
            "0 - Legacy engine only",
            "1 - Neural nets LSTM engine only",
            "2 - Legacy + LSTM engines",
            "3 - Default, based on what is available"
        ])
        self.oem_combo.setCurrentIndex(3)  # Default OEM 3
        tesseract_layout.addRow("OCR Engine Mode:", self.oem_combo)
        
        layout.addWidget(tesseract_group)
        
        # Text processing
        text_group = QGroupBox("Text Processing")
        text_layout = QFormLayout(text_group)
        
        self.skip_text_cb = QCheckBox("Skip pages that already contain text")
        text_layout.addRow(self.skip_text_cb)
        
        self.force_ocr_cb = QCheckBox("Force OCR even if text is already present")
        text_layout.addRow(self.force_ocr_cb)
        
        self.redo_ocr_cb = QCheckBox("Redo OCR on pages with existing OCR")
        text_layout.addRow(self.redo_ocr_cb)
        
        layout.addWidget(text_group)
        
        layout.addStretch()
        
    def create_image_tab(self):
        """Create image processing settings tab."""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Image Processing")
        
        layout = QVBoxLayout(tab)
        
        # Image preprocessing
        preprocess_group = QGroupBox("Image Preprocessing")
        preprocess_layout = QFormLayout(preprocess_group)
        
        self.rotate_pages_cb = QCheckBox("Auto-rotate pages")
        preprocess_layout.addRow(self.rotate_pages_cb)
        
        self.deskew_cb = QCheckBox("Deskew crooked pages")
        preprocess_layout.addRow(self.deskew_cb)
        
        self.clean_cb = QCheckBox("Clean pages before OCR")
        preprocess_layout.addRow(self.clean_cb)
        
        self.remove_background_cb = QCheckBox("Remove background")
        preprocess_layout.addRow(self.remove_background_cb)
        
        layout.addWidget(preprocess_group)
        
        # Image quality
        quality_group = QGroupBox("Image Quality")
        quality_layout = QFormLayout(quality_group)
        
        # DPI settings
        self.dpi_spinbox = QSpinBox()
        self.dpi_spinbox.setRange(72, 600)
        self.dpi_spinbox.setValue(300)
        self.dpi_spinbox.setSuffix(" DPI")
        quality_layout.addRow("Image DPI:", self.dpi_spinbox)
        
        # JPEG quality
        self.jpeg_quality_slider = QSlider(Qt.Horizontal)
        self.jpeg_quality_slider.setRange(1, 100)
        self.jpeg_quality_slider.setValue(95)
        self.jpeg_quality_label = QLabel("95%")
        self.jpeg_quality_slider.valueChanged.connect(
            lambda v: self.jpeg_quality_label.setText(f"{v}%")
        )
        
        jpeg_layout = QHBoxLayout()
        jpeg_layout.addWidget(self.jpeg_quality_slider)
        jpeg_layout.addWidget(self.jpeg_quality_label)
        quality_layout.addRow("JPEG Quality:", jpeg_layout)
        
        # PNG quality
        self.png_quality_slider = QSlider(Qt.Horizontal)
        self.png_quality_slider.setRange(1, 100)
        self.png_quality_slider.setValue(95)
        self.png_quality_label = QLabel("95%")
        self.png_quality_slider.valueChanged.connect(
            lambda v: self.png_quality_label.setText(f"{v}%")
        )
        
        png_layout = QHBoxLayout()
        png_layout.addWidget(self.png_quality_slider)
        png_layout.addWidget(self.png_quality_label)
        quality_layout.addRow("PNG Quality:", png_layout)
        
        layout.addWidget(quality_group)
        
        layout.addStretch()
        
    def create_output_tab(self):
        """Create output settings tab."""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Output")
        
        layout = QVBoxLayout(tab)
        
        # PDF settings
        pdf_group = QGroupBox("PDF Output Settings")
        pdf_layout = QFormLayout(pdf_group)
        
        self.output_type_combo = QComboBox()
        self.output_type_combo.addItems([
            "pdf - Standard PDF",
            "pdfa - PDF/A (archival format)",
            "pdfa-1 - PDF/A-1b",
            "pdfa-2 - PDF/A-2b",
            "pdfa-3 - PDF/A-3b"
        ])
        pdf_layout.addRow("Output Format:", self.output_type_combo)
        
        self.optimize_combo = QComboBox()
        self.optimize_combo.addItems([
            "0 - No optimization",
            "1 - Basic optimization",
            "2 - Advanced optimization",
            "3 - Maximum optimization"
        ])
        self.optimize_combo.setCurrentIndex(1)  # Basic optimization
        pdf_layout.addRow("Optimization Level:", self.optimize_combo)
        
        layout.addWidget(pdf_group)
        
        # Metadata
        metadata_group = QGroupBox("PDF Metadata")
        metadata_layout = QFormLayout(metadata_group)
        
        self.title_edit = QLineEdit()
        metadata_layout.addRow("Title:", self.title_edit)
        
        self.author_edit = QLineEdit()
        metadata_layout.addRow("Author:", self.author_edit)
        
        self.subject_edit = QLineEdit()
        metadata_layout.addRow("Subject:", self.subject_edit)
        
        self.keywords_edit = QLineEdit()
        metadata_layout.addRow("Keywords:", self.keywords_edit)
        
        layout.addWidget(metadata_group)
        
        # File naming
        naming_group = QGroupBox("Output File Naming")
        naming_layout = QFormLayout(naming_group)
        
        self.suffix_edit = QLineEdit("_ocr")
        naming_layout.addRow("File Suffix:", self.suffix_edit)
        
        self.overwrite_cb = QCheckBox("Overwrite existing files")
        naming_layout.addRow(self.overwrite_cb)
        
        layout.addWidget(naming_group)
        
        layout.addStretch()
        
    def create_advanced_tab(self):
        """Create advanced settings tab."""
        tab = QWidget()
        self.tab_widget.addTab(tab, "Advanced")
        
        layout = QVBoxLayout(tab)
        
        # Performance
        perf_group = QGroupBox("Performance Settings")
        perf_layout = QFormLayout(perf_group)
        
        self.jobs_spinbox = QSpinBox()
        self.jobs_spinbox.setRange(1, 16)
        self.jobs_spinbox.setValue(4)
        perf_layout.addRow("CPU Threads:", self.jobs_spinbox)
        
        self.memory_limit_spinbox = QSpinBox()
        self.memory_limit_spinbox.setRange(100, 8000)
        self.memory_limit_spinbox.setValue(1000)
        self.memory_limit_spinbox.setSuffix(" MB")
        perf_layout.addRow("Memory Limit:", self.memory_limit_spinbox)
        
        layout.addWidget(perf_group)
        
        # Custom Tesseract parameters
        tesseract_group = QGroupBox("Custom Tesseract Parameters")
        tesseract_layout = QVBoxLayout(tesseract_group)
        
        tesseract_layout.addWidget(QLabel("Additional Tesseract command-line parameters:"))
        self.tesseract_params_edit = QTextEdit()
        self.tesseract_params_edit.setMaximumHeight(80)
        self.tesseract_params_edit.setPlaceholderText("e.g., -c preserve_interword_spaces=1")
        tesseract_layout.addWidget(self.tesseract_params_edit)
        
        layout.addWidget(tesseract_group)
        
        # Debugging
        debug_group = QGroupBox("Debugging")
        debug_layout = QFormLayout(debug_group)
        
        self.keep_temp_files_cb = QCheckBox("Keep temporary files")
        debug_layout.addRow(self.keep_temp_files_cb)
        
        self.verbose_cb = QCheckBox("Verbose logging")
        debug_layout.addRow(self.verbose_cb)
        
        layout.addWidget(debug_group)
        
        layout.addStretch()
        
    def populate_languages(self):
        """Populate language combo box."""
        # Common languages supported by Tesseract
        languages = [
            ("eng", "English"),
            ("tur", "Turkish"),
            ("fra", "French"),
            ("deu", "German"),
            ("spa", "Spanish"),
            ("ita", "Italian"),
            ("por", "Portuguese"),
            ("rus", "Russian"),
            ("ara", "Arabic"),
            ("chi_sim", "Chinese Simplified"),
            ("chi_tra", "Chinese Traditional"),
            ("jpn", "Japanese"),
            ("kor", "Korean"),
            ("hin", "Hindi"),
            ("nld", "Dutch"),
            ("pol", "Polish"),
            ("swe", "Swedish"),
            ("nor", "Norwegian"),
            ("dan", "Danish"),
            ("fin", "Finnish")
        ]
        
        for code, name in languages:
            self.language_combo.addItem(f"{name} ({code})", code)
            
    def browse_language_dir(self):
        """Browse for Tesseract language data directory."""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Tesseract Language Data Directory"
        )
        if dir_path:
            self.language_dir_edit.setText(dir_path)
            
    def load_settings(self):
        """Load settings from configuration."""
        # OCR settings
        language = self.settings.get('ocr_language', 'eng')
        for i in range(self.language_combo.count()):
            if self.language_combo.itemData(i) == language:
                self.language_combo.setCurrentIndex(i)
                break
                
        self.language_dir_edit.setText(self.settings.get('tesseract_data_dir', ''))
        
        # Tesseract settings
        psm = self.settings.get('tesseract_psm', 3)
        self.psm_combo.setCurrentIndex(min(psm, self.psm_combo.count() - 1))
        
        oem = self.settings.get('tesseract_oem', 3)
        self.oem_combo.setCurrentIndex(min(oem, self.oem_combo.count() - 1))
        
        # Text processing
        self.skip_text_cb.setChecked(self.settings.get('skip_text', False))
        self.force_ocr_cb.setChecked(self.settings.get('force_ocr', False))
        self.redo_ocr_cb.setChecked(self.settings.get('redo_ocr', False))
        
        # Image processing
        self.rotate_pages_cb.setChecked(self.settings.get('rotate_pages', False))
        self.deskew_cb.setChecked(self.settings.get('deskew', False))
        self.clean_cb.setChecked(self.settings.get('clean', False))
        self.remove_background_cb.setChecked(self.settings.get('remove_background', False))
        
        # Image quality
        self.dpi_spinbox.setValue(self.settings.get('image_dpi', 300))
        self.jpeg_quality_slider.setValue(self.settings.get('jpeg_quality', 95))
        self.png_quality_slider.setValue(self.settings.get('png_quality', 95))
        
        # Output settings
        output_type = self.settings.get('output_type', 'pdf')
        for i in range(self.output_type_combo.count()):
            if self.output_type_combo.itemText(i).startswith(output_type):
                self.output_type_combo.setCurrentIndex(i)
                break
                
        optimize = self.settings.get('optimize', 1)
        self.optimize_combo.setCurrentIndex(min(optimize, self.optimize_combo.count() - 1))
        
        # Metadata
        self.title_edit.setText(self.settings.get('pdf_title', ''))
        self.author_edit.setText(self.settings.get('pdf_author', ''))
        self.subject_edit.setText(self.settings.get('pdf_subject', ''))
        self.keywords_edit.setText(self.settings.get('pdf_keywords', ''))
        
        # File naming
        self.suffix_edit.setText(self.settings.get('output_suffix', '_ocr'))
        self.overwrite_cb.setChecked(self.settings.get('overwrite_files', False))
        
        # Advanced settings
        self.jobs_spinbox.setValue(self.settings.get('jobs', 4))
        self.memory_limit_spinbox.setValue(self.settings.get('memory_limit', 1000))
        self.tesseract_params_edit.setPlainText(self.settings.get('tesseract_params', ''))
        
        # Debugging
        self.keep_temp_files_cb.setChecked(self.settings.get('keep_temp_files', False))
        self.verbose_cb.setChecked(self.settings.get('verbose_logging', False))
        
    def save_settings(self):
        """Save settings to configuration."""
        # OCR settings
        language_data = self.language_combo.currentData()
        if language_data:
            self.settings.set('ocr_language', language_data)
            
        self.settings.set('tesseract_data_dir', self.language_dir_edit.text())
        
        # Tesseract settings
        self.settings.set('tesseract_psm', self.psm_combo.currentIndex())
        self.settings.set('tesseract_oem', self.oem_combo.currentIndex())
        
        # Text processing
        self.settings.set('skip_text', self.skip_text_cb.isChecked())
        self.settings.set('force_ocr', self.force_ocr_cb.isChecked())
        self.settings.set('redo_ocr', self.redo_ocr_cb.isChecked())
        
        # Image processing
        self.settings.set('rotate_pages', self.rotate_pages_cb.isChecked())
        self.settings.set('deskew', self.deskew_cb.isChecked())
        self.settings.set('clean', self.clean_cb.isChecked())
        self.settings.set('remove_background', self.remove_background_cb.isChecked())
        
        # Image quality
        self.settings.set('image_dpi', self.dpi_spinbox.value())
        self.settings.set('jpeg_quality', self.jpeg_quality_slider.value())
        self.settings.set('png_quality', self.png_quality_slider.value())
        
        # Output settings
        output_text = self.output_type_combo.currentText()
        output_type = output_text.split(' - ')[0]
        self.settings.set('output_type', output_type)
        
        self.settings.set('optimize', self.optimize_combo.currentIndex())
        
        # Metadata
        self.settings.set('pdf_title', self.title_edit.text())
        self.settings.set('pdf_author', self.author_edit.text())
        self.settings.set('pdf_subject', self.subject_edit.text())
        self.settings.set('pdf_keywords', self.keywords_edit.text())
        
        # File naming
        self.settings.set('output_suffix', self.suffix_edit.text())
        self.settings.set('overwrite_files', self.overwrite_cb.isChecked())
        
        # Advanced settings
        self.settings.set('jobs', self.jobs_spinbox.value())
        self.settings.set('memory_limit', self.memory_limit_spinbox.value())
        self.settings.set('tesseract_params', self.tesseract_params_edit.toPlainText())
        
        # Debugging
        self.settings.set('keep_temp_files', self.keep_temp_files_cb.isChecked())
        self.settings.set('verbose_logging', self.verbose_cb.isChecked())
        
    def restore_defaults(self):
        """Restore default settings."""
        reply = QMessageBox.question(
            self, "Restore Defaults",
            "This will reset all settings to their default values. Continue?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            self.load_settings()
            
    def accept(self):
        """Accept dialog and save settings."""
        self.save_settings()
        super().accept()