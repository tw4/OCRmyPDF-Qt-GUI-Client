"""
OCR Worker Thread - Handles OCRmyPDF processing in background
"""

import os
import sys
import logging
import tempfile
from PyQt5.QtCore import QThread, pyqtSignal

# Debug: print Python path and try to import ocrmypdf
def debug_import():
    logger = logging.getLogger(__name__)
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Python path: {sys.path}")
    
    try:
        import ocrmypdf
        logger.info(f"OCRmyPDF version: {ocrmypdf.__version__}")
        logger.info(f"OCRmyPDF location: {ocrmypdf.__file__}")
        return True
    except ImportError as e:
        logger.error(f"Failed to import ocrmypdf: {e}")
        return False

# Try to import OCRmyPDF
try:
    import ocrmypdf
    from ocrmypdf.exceptions import (
        PriorOcrFoundError, EncryptedPdfError, InputFileError,
        OutputFileAccessError, UnsupportedImageFormatError
    )
    OCRMYPDF_AVAILABLE = True
except ImportError as e:
    logging.getLogger(__name__).error(f"OCRmyPDF import failed: {e}")
    ocrmypdf = None
    PriorOcrFoundError = Exception
    EncryptedPdfError = Exception
    InputFileError = Exception
    OutputFileAccessError = Exception
    UnsupportedImageFormatError = Exception
    OCRMYPDF_AVAILABLE = False


class OCRWorker(QThread):
    """Worker thread for OCR processing."""
    
    # Signals
    progress = pyqtSignal(int, str)  # percentage, current_file
    file_completed = pyqtSignal(str, bool, str)  # filename, success, message
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, file_list, options, output_dir=None):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.file_list = file_list
        self.options = options
        self.output_dir = output_dir or os.path.expanduser('~/Desktop/OCR_Output')
        self.is_cancelled = False
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
    def cancel(self):
        """Cancel the OCR processing."""
        self.is_cancelled = True
        self.logger.info("OCR processing cancelled by user")
        
    def run(self):
        """Main processing loop."""
        # Debug import issues
        debug_import()
        
        if not OCRMYPDF_AVAILABLE or ocrmypdf is None:
            self.error.emit("OCRmyPDF is not installed. Please install it using: pip install ocrmypdf")
            return
            
        self.logger.info(f"Starting OCR processing for {len(self.file_list)} files")
        
        try:
            for i, input_file in enumerate(self.file_list):
                if self.is_cancelled:
                    break
                    
                # Update progress
                filename = os.path.basename(input_file)
                self.progress.emit(int(i / len(self.file_list) * 100), filename)
                
                # Process single file
                success, message = self.process_single_file(input_file)
                self.file_completed.emit(filename, success, message)
                
            # Final progress update
            if not self.is_cancelled:
                self.progress.emit(100, "Completed")
                
        except Exception as e:
            self.logger.error(f"OCR processing failed: {e}")
            self.error.emit(f"OCR processing failed: {str(e)}")
        finally:
            self.finished.emit()
            
    def process_single_file(self, input_file):
        """Process a single PDF file."""
        filename = os.path.basename(input_file)
        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(self.output_dir, f"{base_name}_ocr.pdf")
        
        # Make sure output file doesn't already exist or create unique name
        counter = 1
        original_output = output_file
        while os.path.exists(output_file):
            base_output = os.path.splitext(original_output)[0]
            output_file = f"{base_output}_{counter}.pdf"
            counter += 1
            
        try:
            self.logger.info(f"Processing {filename} -> {os.path.basename(output_file)}")
            
            # Prepare OCRmyPDF options
            ocr_options = self.prepare_ocr_options()
            
            # Run OCRmyPDF
            result = ocrmypdf.ocr(
                input_file,
                output_file,
                **ocr_options
            )
            
            self.logger.info(f"Successfully processed {filename}")
            return True, f"Successfully processed to {os.path.basename(output_file)}"
            
        except PriorOcrFoundError:
            # PDF already has OCR layer - copy with warning
            try:
                import shutil
                shutil.copy2(input_file, output_file)
                message = f"File already has OCR layer. Copied to {os.path.basename(output_file)}"
                self.logger.warning(message)
                return True, message
            except Exception as e:
                error_msg = f"File has OCR layer but copy failed: {str(e)}"
                self.logger.error(error_msg)
                return False, error_msg
                
        except EncryptedPdfError:
            error_msg = "PDF is encrypted and cannot be processed"
            self.logger.error(f"{filename}: {error_msg}")
            return False, error_msg
            
        except InputFileError:
            error_msg = "Input file not found or invalid"
            self.logger.error(f"{filename}: {error_msg}")
            return False, error_msg
            
        except OutputFileAccessError:
            error_msg = "Cannot write to output file (check permissions)"
            self.logger.error(f"{filename}: {error_msg}")
            return False, error_msg
            
        except UnsupportedImageFormatError:
            error_msg = "PDF contains unsupported image formats"
            self.logger.error(f"{filename}: {error_msg}")
            return False, error_msg
            
        except Exception as e:
            error_msg = f"OCR failed: {str(e)}"
            self.logger.error(f"{filename}: {error_msg}")
            return False, error_msg
            
    def prepare_ocr_options(self):
        """Prepare OCRmyPDF options from user settings."""
        options = {}
        
        # Language
        if self.options.get('language'):
            options['language'] = self.options['language']
            
        # Page processing options
        if self.options.get('rotate_pages'):
            options['rotate_pages'] = True
            
        if self.options.get('deskew'):
            options['deskew'] = True
            
        if self.options.get('clean'):
            options['clean'] = True
            
        # Performance options
        jobs = self.options.get('jobs', 1)
        if jobs > 1:
            options['jobs'] = jobs
            
        # Output format
        output_type = self.options.get('output_type', 'pdf')
        if output_type.startswith('pdfa'):
            options['output_type'] = 'pdfa'
            
        # Progress bar - disabled for GUI
        options['progress_bar'] = False
        
        # Additional OCR options
        options.update({
            'optimize': 1,  # Basic optimization
            'force_ocr': False,  # Don't re-OCR pages that already have text
            'skip_text': False,  # Don't skip pages with text
        })
        
        self.logger.debug(f"OCR options: {options}")
        return options