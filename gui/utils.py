"""
GUI Utility Functions
"""

import os
import logging
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import QStandardPaths
from PyQt5.QtGui import QIcon, QPixmap


def show_error_message(parent, title, message, details=None):
    """Show an error message dialog."""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    
    if details:
        msg_box.setDetailedText(str(details))
        
    msg_box.exec_()


def show_warning_message(parent, title, message):
    """Show a warning message dialog."""
    QMessageBox.warning(parent, title, message)


def show_info_message(parent, title, message):
    """Show an information message dialog."""
    QMessageBox.information(parent, title, message)


def show_question_dialog(parent, title, message):
    """Show a yes/no question dialog."""
    reply = QMessageBox.question(
        parent, title, message,
        QMessageBox.Yes | QMessageBox.No,
        QMessageBox.No
    )
    return reply == QMessageBox.Yes


def format_file_size(size_bytes):
    """Format file size in human readable format."""
    if size_bytes == 0:
        return "0 B"
        
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024.0 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.1f} {size_names[i]}"


def get_default_output_directory():
    """Get the default output directory for processed files."""
    desktop_path = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
    output_dir = os.path.join(desktop_path, "OCR_Output")
    return output_dir


def ensure_directory_exists(directory_path):
    """Ensure a directory exists, create if necessary."""
    try:
        os.makedirs(directory_path, exist_ok=True)
        return True
    except Exception as e:
        logging.getLogger(__name__).error(f"Failed to create directory {directory_path}: {e}")
        return False


def get_unique_filename(file_path):
    """Get a unique filename by appending numbers if file exists."""
    if not os.path.exists(file_path):
        return file_path
        
    base, ext = os.path.splitext(file_path)
    counter = 1
    
    while os.path.exists(file_path):
        file_path = f"{base}_{counter}{ext}"
        counter += 1
        
    return file_path


def load_icon(icon_name, size=None):
    """Load an icon from the resources directory."""
    icon_path = os.path.join("resources", "icons", icon_name)
    
    if os.path.exists(icon_path):
        icon = QIcon(icon_path)
        if size:
            pixmap = icon.pixmap(size, size)
            return QIcon(pixmap)
        return icon
    else:
        # Return empty icon if file doesn't exist
        return QIcon()


def validate_pdf_file(file_path):
    """Basic validation to check if file is a PDF."""
    if not os.path.exists(file_path):
        return False, "File does not exist"
        
    if not file_path.lower().endswith('.pdf'):
        return False, "File is not a PDF"
        
    try:
        # Check file size
        size = os.path.getsize(file_path)
        if size == 0:
            return False, "PDF file is empty"
            
        # Basic PDF header check
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                return False, "Invalid PDF file format"
                
    except Exception as e:
        return False, f"Error reading file: {str(e)}"
        
    return True, "Valid PDF file"


def get_tesseract_languages():
    """Get list of available Tesseract languages."""
    try:
        import subprocess
        result = subprocess.run(
            ['tesseract', '--list-langs'],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            # Skip the first line which is "List of available languages (X):"
            languages = [lang.strip() for lang in lines[1:] if lang.strip()]
            return languages
        else:
            # Return common languages if tesseract command fails
            return ['eng', 'tur', 'fra', 'deu', 'spa', 'ita', 'por', 'rus']
            
    except Exception:
        # Return common languages if tesseract is not available
        return ['eng', 'tur', 'fra', 'deu', 'spa', 'ita', 'por', 'rus']


def check_dependencies():
    """Check if required dependencies are available."""
    missing_deps = []
    
    # Check OCRmyPDF
    try:
        import ocrmypdf
    except ImportError:
        missing_deps.append("ocrmypdf")
        
    # Check Tesseract
    try:
        import subprocess
        result = subprocess.run(
            ['tesseract', '--version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode != 0:
            missing_deps.append("tesseract")
    except Exception:
        missing_deps.append("tesseract")
        
    # Check Ghostscript
    try:
        import subprocess
        gs_commands = ['gs', 'gswin32c', 'gswin64c']
        gs_found = False
        
        for gs_cmd in gs_commands:
            try:
                result = subprocess.run(
                    [gs_cmd, '--version'],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    gs_found = True
                    break
            except Exception:
                continue
                
        if not gs_found:
            missing_deps.append("ghostscript")
            
    except Exception:
        missing_deps.append("ghostscript")
        
    return missing_deps


class FileProcessor:
    """Utility class for file processing operations."""
    
    @staticmethod
    def get_pdf_info(file_path):
        """Get basic information about a PDF file."""
        try:
            info = {
                'filename': os.path.basename(file_path),
                'size': os.path.getsize(file_path),
                'size_formatted': format_file_size(os.path.getsize(file_path)),
                'path': file_path,
                'valid': True,
                'error': None
            }
            
            # Try to get page count (requires PyPDF2 or similar)
            try:
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    info['pages'] = len(reader.pages)
            except Exception:
                info['pages'] = None
                
            return info
            
        except Exception as e:
            return {
                'filename': os.path.basename(file_path) if file_path else 'Unknown',
                'size': 0,
                'size_formatted': '0 B',
                'path': file_path,
                'valid': False,
                'error': str(e),
                'pages': None
            }
            
    @staticmethod
    def cleanup_temp_files(temp_dir):
        """Clean up temporary files."""
        try:
            import shutil
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
                return True
        except Exception as e:
            logging.getLogger(__name__).error(f"Failed to cleanup temp files: {e}")
            
        return False