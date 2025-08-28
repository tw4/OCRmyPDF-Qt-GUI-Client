"""
Main Window - OCRmyPDF Qt GUI Client
"""

import os
import logging
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTreeWidget, QTreeWidgetItem, QScrollArea, QGroupBox, QFormLayout,
    QComboBox, QCheckBox, QSpinBox, QSlider, QPushButton, QFileDialog,
    QMessageBox, QMenuBar, QToolBar, QStatusBar, QLabel, QProgressBar,
    QApplication
)
from PyQt5.QtCore import Qt, pyqtSignal, QMimeData
from PyQt5.QtGui import QIcon, QDragEnterEvent, QDropEvent

from gui.settings_dialog import SettingsDialog
from gui.progress_dialog import ProgressDialog
from core.settings import AppSettings


class FileTreeWidget(QTreeWidget):
    """Custom TreeWidget with drag and drop support for PDF files."""
    
    files_dropped = pyqtSignal(list)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setHeaderLabels(['File Name', 'Status', 'Size'])
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 80)
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.toLocalFile().lower().endswith('.pdf') for url in urls):
                event.acceptProposedAction()
        
    def dropEvent(self, event: QDropEvent):
        files = [url.toLocalFile() for url in event.mimeData().urls()]
        pdf_files = [f for f in files if f.lower().endswith('.pdf')]
        if pdf_files:
            self.files_dropped.emit(pdf_files)


class MainWindow(QMainWindow):
    """Main application window."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.settings = AppSettings()
        self.file_list = []
        
        self.setWindowTitle("OCRmyPDF GUI Client")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        
        self.setup_ui()
        self.setup_connections()
        self.load_settings()
        
    def setup_ui(self):
        """Initialize the user interface."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.create_status_bar()
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - File list
        self.file_tree = FileTreeWidget()
        self.file_tree.files_dropped.connect(self.add_files)
        splitter.addWidget(self.file_tree)
        
        # Right panel - Settings
        settings_widget = self.create_settings_panel()
        splitter.addWidget(settings_widget)
        
        # Set splitter proportions
        splitter.setSizes([600, 400])
        
    def create_menu_bar(self):
        """Create the menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('&File')
        file_menu.addAction('&Open Files', self.open_files, 'Ctrl+O')
        file_menu.addAction('Open &Folder', self.open_folder, 'Ctrl+Shift+O')
        file_menu.addSeparator()
        file_menu.addAction('&Clear List', self.clear_file_list, 'Ctrl+L')
        file_menu.addSeparator()
        file_menu.addAction('E&xit', self.close, 'Ctrl+Q')
        
        # Edit menu
        edit_menu = menubar.addMenu('&Edit')
        edit_menu.addAction('&Settings', self.show_settings, 'Ctrl+,')
        
        # View menu
        view_menu = menubar.addMenu('&View')
        view_menu.addAction('Show &Log', self.show_log)
        
        # Help menu
        help_menu = menubar.addMenu('&Help')
        help_menu.addAction('&About', self.show_about)
        
    def create_toolbar(self):
        """Create the toolbar."""
        toolbar = self.addToolBar('Main')
        toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        
        toolbar.addAction('Add Files', self.open_files)
        toolbar.addAction('Add Folder', self.open_folder)
        toolbar.addSeparator()
        toolbar.addAction('Clear List', self.clear_file_list)
        toolbar.addSeparator()
        
        # Start processing button
        self.start_button = toolbar.addAction('Start Processing', self.start_processing)
        self.start_button.setEnabled(False)
        
    def create_status_bar(self):
        """Create the status bar."""
        self.statusBar().showMessage('Ready')
        
        # File count label
        self.file_count_label = QLabel('Files: 0')
        self.statusBar().addPermanentWidget(self.file_count_label)
        
        # Total size label
        self.total_size_label = QLabel('Total: 0 MB')
        self.statusBar().addPermanentWidget(self.total_size_label)
        
    def create_settings_panel(self):
        """Create the settings panel."""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMaximumWidth(400)
        
        settings_widget = QWidget()
        scroll_area.setWidget(settings_widget)

        # sağ paneldeki griliği kaldırma
        scroll_area.setStyleSheet("QScrollArea { background: transparent; }")
        scroll_area.viewport().setStyleSheet("background: transparent;")
        settings_widget.setStyleSheet("background: transparent; QGroupBox { background: transparent; }")



        layout = QVBoxLayout(settings_widget)
        
        # OCR Settings Group
        ocr_group = QGroupBox("OCR Settings")
        ocr_layout = QFormLayout(ocr_group)
        
        # Language selection
        self.language_combo = QComboBox()
        self.language_combo.addItems(['eng', 'tur', 'fra', 'deu', 'spa', 'rus'])
        ocr_layout.addRow('Language:', self.language_combo)
        
        # Output format
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(['PDF', 'PDF/A-1b', 'PDF/A-2b', 'PDF/A-3b'])
        ocr_layout.addRow('Output Format:', self.output_format_combo)
        
        layout.addWidget(ocr_group)
        
        # Page Processing Group
        page_group = QGroupBox("Page Processing")
        page_layout = QFormLayout(page_group)
        
        self.rotate_pages_cb = QCheckBox('Auto-rotate pages')
        page_layout.addRow(self.rotate_pages_cb)
        
        self.deskew_cb = QCheckBox('Deskew pages')
        page_layout.addRow(self.deskew_cb)
        
        self.clean_cb = QCheckBox('Clean pages')
        page_layout.addRow(self.clean_cb)
        
        layout.addWidget(page_group)
        
        # Performance Group
        perf_group = QGroupBox("Performance")
        perf_layout = QFormLayout(perf_group)
        
        self.jobs_spinbox = QSpinBox()
        self.jobs_spinbox.setRange(1, os.cpu_count() or 4)
        self.jobs_spinbox.setValue(min(4, os.cpu_count() or 4))
        perf_layout.addRow('CPU Threads:', self.jobs_spinbox)
        
        layout.addWidget(perf_group)
        
        # Advanced Settings Button
        self.advanced_button = QPushButton('Advanced Settings...')
        self.advanced_button.clicked.connect(self.show_settings)
        layout.addWidget(self.advanced_button)
        
        layout.addStretch()
        
        return scroll_area
        
    def setup_connections(self):
        """Setup signal-slot connections."""
        self.language_combo.currentTextChanged.connect(self.on_settings_changed)
        self.output_format_combo.currentTextChanged.connect(self.on_settings_changed)
        self.rotate_pages_cb.toggled.connect(self.on_settings_changed)
        self.deskew_cb.toggled.connect(self.on_settings_changed)
        self.clean_cb.toggled.connect(self.on_settings_changed)
        self.jobs_spinbox.valueChanged.connect(self.on_settings_changed)
        
    def load_settings(self):
        """Load application settings."""
        # Load language
        language = self.settings.get('ocr_language', 'eng')
        index = self.language_combo.findText(language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
            
        # Load other settings
        self.output_format_combo.setCurrentText(self.settings.get('output_format', 'PDF'))
        self.rotate_pages_cb.setChecked(self.settings.get('rotate_pages', False))
        self.deskew_cb.setChecked(self.settings.get('deskew', False))
        self.clean_cb.setChecked(self.settings.get('clean', False))
        self.jobs_spinbox.setValue(self.settings.get('jobs', min(4, os.cpu_count() or 4)))
        
    def save_settings(self):
        """Save application settings."""
        self.settings.set('ocr_language', self.language_combo.currentText())
        self.settings.set('output_format', self.output_format_combo.currentText())
        self.settings.set('rotate_pages', self.rotate_pages_cb.isChecked())
        self.settings.set('deskew', self.deskew_cb.isChecked())
        self.settings.set('clean', self.clean_cb.isChecked())
        self.settings.set('jobs', self.jobs_spinbox.value())
        
    def on_settings_changed(self):
        """Handle settings changes."""
        self.save_settings()
        
    def open_files(self):
        """Open file dialog to select PDF files."""
        files, _ = QFileDialog.getOpenFileNames(
            self, 'Select PDF Files', '', 'PDF Files (*.pdf)'
        )
        if files:
            self.add_files(files)
            
    def open_folder(self):
        """Open folder dialog to select all PDF files in a folder."""
        folder = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder:
            pdf_files = []
            for filename in os.listdir(folder):
                if filename.lower().endswith('.pdf'):
                    pdf_files.append(os.path.join(folder, filename))
            
            if pdf_files:
                self.add_files(pdf_files)
            else:
                QMessageBox.information(self, 'No PDF Files', 'No PDF files found in the selected folder.')
                
    def add_files(self, files):
        """Add files to the processing list."""
        added_count = 0
        for file_path in files:
            if file_path not in self.file_list:
                self.file_list.append(file_path)
                
                # Add to tree widget
                item = QTreeWidgetItem(self.file_tree)
                item.setText(0, os.path.basename(file_path))
                item.setText(1, 'Pending')
                
                # Get file size
                try:
                    size_bytes = os.path.getsize(file_path)
                    if size_bytes >= 1024 * 1024:  # MB
                        size_mb = size_bytes / (1024 * 1024)
                        item.setText(2, f'{size_mb:.1f} MB')
                    elif size_bytes >= 1024:  # KB
                        size_kb = size_bytes / 1024
                        item.setText(2, f'{size_kb:.1f} KB')
                    else:  # Bytes
                        item.setText(2, f'{size_bytes} B')
                except OSError:
                    item.setText(2, 'N/A')
                    
                item.setData(0, Qt.UserRole, file_path)
                added_count += 1
                
        if added_count > 0:
            self.update_status()
            self.start_button.setEnabled(True)
            self.statusBar().showMessage(f'Added {added_count} files')
            
    def clear_file_list(self):
        """Clear the file list."""
        self.file_list.clear()
        self.file_tree.clear()
        self.start_button.setEnabled(False)
        self.update_status()
        self.statusBar().showMessage('File list cleared')
        
    def update_status(self):
        """Update status bar information."""
        file_count = len(self.file_list)
        self.file_count_label.setText(f'Files: {file_count}')
        
        # Calculate total size
        total_size = 0
        for file_path in self.file_list:
            try:
                total_size += os.path.getsize(file_path)
            except OSError:
                pass
                
        total_size_mb = total_size / (1024 * 1024)
        self.total_size_label.setText(f'Total: {total_size_mb:.1f} MB')
        
    def start_processing(self):
        """Start OCR processing."""
        if not self.file_list:
            QMessageBox.warning(self, 'No Files', 'Please add PDF files to process.')
            return
            
        # Get OCR options
        options = {
            'language': self.language_combo.currentText(),
            'rotate_pages': self.rotate_pages_cb.isChecked(),
            'deskew': self.deskew_cb.isChecked(),
            'clean': self.clean_cb.isChecked(),
            'jobs': self.jobs_spinbox.value(),
            'output_type': 'pdf' if self.output_format_combo.currentText() == 'PDF' else 'pdfa'
        }
        
        # Show progress dialog
        progress_dialog = ProgressDialog(self.file_list, options, self)
        progress_dialog.exec_()
        
    def show_settings(self):
        """Show advanced settings dialog."""
        dialog = SettingsDialog(self.settings, self)
        if dialog.exec_() == SettingsDialog.Accepted:
            self.load_settings()
            
    def show_log(self):
        """Show application log."""
        QMessageBox.information(self, 'Log', 'Log viewer not implemented yet.')
        
    def show_about(self):
        """Show about dialog."""
        about_text = (
            '<h3>OCRmyPDF GUI Client v1.0.0</h3>'
            '<p>A user-friendly interface for OCRmyPDF.<br/>'
            'Adds OCR text layers to scanned PDF documents.</p>'
            '<hr/>'
            '<p><b>Built with:</b></p>'
            '<ul>'
            '<li><b>OCRmyPDF</b> - The powerful OCR engine<br/>'
            '   Licensed under Mozilla Public License 2.0<br/>'
            '   <a href="https://github.com/ocrmypdf/OCRmyPDF">github.com/ocrmypdf/OCRmyPDF</a></li>'
            '<li><b>PyQt5</b> - Cross-platform GUI framework</li>'
            '<li><b>Tesseract OCR</b> - Open source OCR engine by Google</li>'
            '<li><b>Ghostscript</b> - PostScript and PDF interpreter</li>'
            '</ul>'
            '<hr/>'
            '<p><b>License:</b> Mozilla Public License 2.0</p>'
            '<p><b>Source Code:</b> Available under MPL 2.0 terms</p>'
            '<p><i>This application is a derivative work that provides a graphical '
            'user interface for OCRmyPDF functionality.</i></p>'
        )
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle('About OCRmyPDF GUI')
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
        
    def closeEvent(self, event):
        """Handle application close event."""
        self.save_settings()
        event.accept()