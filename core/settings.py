"""
Application Settings - Configuration management
"""

import os
import json
import logging
from PyQt5.QtCore import QSettings


class AppSettings:
    """Application settings manager."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = QSettings('OCRmyPDF-GUI', 'OCRmyPDF-GUI')
        
        # Default values
        self.defaults = {
            # OCR settings
            'ocr_language': 'eng',
            'tesseract_data_dir': '',
            'tesseract_psm': 3,
            'tesseract_oem': 3,
            
            # Text processing
            'skip_text': False,
            'force_ocr': False,
            'redo_ocr': False,
            
            # Image processing
            'rotate_pages': False,
            'deskew': False,
            'clean': False,
            'remove_background': False,
            
            # Image quality
            'image_dpi': 300,
            'jpeg_quality': 95,
            'png_quality': 95,
            
            # Output settings
            'output_format': 'PDF',
            'output_type': 'pdf',
            'optimize': 1,
            'output_suffix': '_ocr',
            'overwrite_files': False,
            
            # PDF metadata
            'pdf_title': '',
            'pdf_author': '',
            'pdf_subject': '',
            'pdf_keywords': '',
            
            # Performance
            'jobs': min(4, os.cpu_count() or 4),
            'memory_limit': 1000,
            
            # Advanced
            'tesseract_params': '',
            'keep_temp_files': False,
            'verbose_logging': False,
            
            # GUI settings
            'window_geometry': None,
            'window_state': None,
            'splitter_state': None,
        }
        
    def get(self, key, default=None):
        """Get a setting value."""
        if default is None:
            default = self.defaults.get(key)
            
        value = self.settings.value(key, default)
        
        # Convert string values back to proper types
        if key in ['tesseract_psm', 'tesseract_oem', 'image_dpi', 'jpeg_quality', 
                  'png_quality', 'optimize', 'jobs', 'memory_limit']:
            try:
                return int(value)
            except (ValueError, TypeError):
                return self.defaults.get(key, 0)
                
        elif key in ['skip_text', 'force_ocr', 'redo_ocr', 'rotate_pages', 'deskew',
                    'clean', 'remove_background', 'overwrite_files', 'keep_temp_files',
                    'verbose_logging']:
            if isinstance(value, str):
                return value.lower() in ('true', '1', 'yes')
            return bool(value)
            
        return value
        
    def set(self, key, value):
        """Set a setting value."""
        self.settings.setValue(key, value)
        self.logger.debug(f"Setting {key} = {value}")
        
    def clear(self):
        """Clear all settings."""
        self.settings.clear()
        self.logger.info("All settings cleared")
        
    def get_ocr_options(self):
        """Get OCR options for worker thread."""
        return {
            'language': self.get('ocr_language'),
            'rotate_pages': self.get('rotate_pages'),
            'deskew': self.get('deskew'),
            'clean': self.get('clean'),
            'remove_background': self.get('remove_background'),
            'jobs': self.get('jobs'),
            'output_type': self.get('output_type'),
            'optimize': self.get('optimize'),
            'force_ocr': self.get('force_ocr'),
            'skip_text': self.get('skip_text'),
            'redo_ocr': self.get('redo_ocr'),
            'tesseract_psm': self.get('tesseract_psm'),
            'tesseract_oem': self.get('tesseract_oem'),
            'tesseract_params': self.get('tesseract_params'),
            'image_dpi': self.get('image_dpi'),
            'jpeg_quality': self.get('jpeg_quality'),
            'png_quality': self.get('png_quality'),
            'keep_temp_files': self.get('keep_temp_files'),
            'verbose_logging': self.get('verbose_logging'),
        }
        
    def export_settings(self, filename):
        """Export settings to JSON file."""
        try:
            settings_dict = {}
            for key in self.defaults.keys():
                settings_dict[key] = self.get(key)
                
            with open(filename, 'w') as f:
                json.dump(settings_dict, f, indent=2)
                
            self.logger.info(f"Settings exported to {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to export settings: {e}")
            return False
            
    def import_settings(self, filename):
        """Import settings from JSON file."""
        try:
            with open(filename, 'r') as f:
                settings_dict = json.load(f)
                
            for key, value in settings_dict.items():
                if key in self.defaults:
                    self.set(key, value)
                    
            self.logger.info(f"Settings imported from {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import settings: {e}")
            return False