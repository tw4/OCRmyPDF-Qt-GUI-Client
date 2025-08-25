"""
Progress Dialog - Shows OCR processing progress
"""

import os
import logging
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar,
    QPushButton, QTextEdit, QGroupBox, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

from core.ocr_worker import OCRWorker


class ProgressDialog(QDialog):
    """Dialog to show OCR processing progress."""
    
    def __init__(self, file_list, options, parent=None):
        super().__init__(parent)
        self.logger = logging.getLogger(__name__)
        self.file_list = file_list
        self.options = options
        self.worker = None
        self.output_dir = None
        
        self.setWindowTitle("OCR Processing")
        self.setMinimumSize(600, 400)
        self.resize(700, 500)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.setup_ui()
        self.setup_output_directory()
        
    def setup_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Overall progress section
        progress_group = QGroupBox("Overall Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.overall_progress = QProgressBar()
        self.overall_progress.setRange(0, 100)
        progress_layout.addWidget(self.overall_progress)
        
        self.status_label = QLabel("Preparing to start...")
        progress_layout.addWidget(self.status_label)
        
        layout.addWidget(progress_group)
        
        # Current file section
        current_group = QGroupBox("Current File")
        current_layout = QVBoxLayout(current_group)
        
        self.current_file_label = QLabel("No file being processed")
        font = QFont()
        font.setBold(True)
        self.current_file_label.setFont(font)
        current_layout.addWidget(self.current_file_label)
        
        layout.addWidget(current_group)
        
        # Output directory section
        output_group = QGroupBox("Output Directory")
        output_layout = QHBoxLayout(output_group)
        
        self.output_dir_label = QLabel("")
        output_layout.addWidget(self.output_dir_label)
        
        self.browse_output_button = QPushButton("Browse...")
        self.browse_output_button.clicked.connect(self.browse_output_directory)
        output_layout.addWidget(self.browse_output_button)
        
        layout.addWidget(output_group)
        
        # Log section
        log_group = QGroupBox("Processing Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(150)
        self.log_text.setFont(QFont("Consolas", 8))
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.start_button = QPushButton("Start Processing")
        self.start_button.clicked.connect(self.start_processing)
        button_layout.addWidget(self.start_button)
        
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_processing)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)
        
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.close_button.setEnabled(False)
        button_layout.addWidget(self.close_button)
        
        layout.addWidget(QLabel())  # Spacer
        layout.addLayout(button_layout)
        
    def setup_output_directory(self):
        """Setup the default output directory."""
        self.output_dir = os.path.expanduser("~/Desktop/OCR_Output")
        self.output_dir_label.setText(self.output_dir)
        
    def browse_output_directory(self):
        """Browse for output directory."""
        dir_path = QFileDialog.getExistingDirectory(
            self, "Select Output Directory", self.output_dir
        )
        if dir_path:
            self.output_dir = dir_path
            self.output_dir_label.setText(dir_path)
            
    def start_processing(self):
        """Start the OCR processing."""
        if not os.path.exists(self.output_dir):
            try:
                os.makedirs(self.output_dir, exist_ok=True)
                self.log_message(f"Created output directory: {self.output_dir}")
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"Cannot create output directory: {str(e)}"
                )
                return
                
        # Update UI
        self.start_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.browse_output_button.setEnabled(False)
        
        # Create and start worker
        self.worker = OCRWorker(self.file_list, self.options, self.output_dir)
        self.worker.progress.connect(self.on_progress)
        self.worker.file_completed.connect(self.on_file_completed)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        
        self.worker.start()
        
        self.log_message(f"Starting OCR processing for {len(self.file_list)} files")
        self.log_message(f"Output directory: {self.output_dir}")
        self.log_message("=" * 50)
        
    def cancel_processing(self):
        """Cancel the OCR processing."""
        if self.worker and self.worker.isRunning():
            self.log_message("Cancelling OCR processing...")
            self.worker.cancel()
            self.cancel_button.setEnabled(False)
            
    def on_progress(self, percentage, current_file):
        """Handle progress updates."""
        self.overall_progress.setValue(percentage)
        
        if current_file:
            if current_file == "Completed":
                self.current_file_label.setText("All files processed")
                self.status_label.setText("Processing completed")
            else:
                self.current_file_label.setText(f"Processing: {current_file}")
                self.status_label.setText(f"Progress: {percentage}%")
                
    def on_file_completed(self, filename, success, message):
        """Handle file completion."""
        if success:
            self.log_message(f"✓ {filename}: {message}")
        else:
            self.log_message(f"✗ {filename}: {message}")
            
        # Auto-scroll to bottom
        self.log_text.moveCursor(self.log_text.textCursor().End)
        
    def on_finished(self):
        """Handle processing completion."""
        self.cancel_button.setEnabled(False)
        self.close_button.setEnabled(True)
        self.browse_output_button.setEnabled(True)
        
        self.log_message("=" * 50)
        self.log_message("OCR processing completed")
        
        # Show completion message
        completed_files = self.output_dir
        QMessageBox.information(
            self, "Processing Complete",
            f"OCR processing completed.\n\nProcessed files are saved in:\n{completed_files}"
        )
        
    def on_error(self, error_message):
        """Handle processing errors."""
        self.log_message(f"ERROR: {error_message}")
        
        self.cancel_button.setEnabled(False)
        self.close_button.setEnabled(True)
        self.browse_output_button.setEnabled(True)
        
        QMessageBox.critical(self, "Processing Error", error_message)
        
    def log_message(self, message):
        """Add a message to the log."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        self.log_text.append(formatted_message)
        self.logger.info(message)
        
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
        
    def closeEvent(self, event):
        """Handle dialog close event."""
        if self.worker and self.worker.isRunning():
            reply = QMessageBox.question(
                self, "OCR Processing Active",
                "OCR processing is still active. Do you want to cancel it and close?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.worker.cancel()
                self.worker.wait(3000)  # Wait up to 3 seconds
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()