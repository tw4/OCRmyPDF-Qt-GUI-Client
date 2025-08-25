#!/usr/bin/env python3
"""
OCRmyPDF Qt GUI Client - Main Entry Point

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.

This application is a derivative work that provides a graphical user 
interface for OCRmyPDF functionality.
"""

import sys
import os
import logging
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

from gui.main_window import MainWindow


def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('ocr_gui.log'),
            logging.StreamHandler()
        ]
    )


def main():
    """Main application entry point."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # High DPI support must be set before QApplication creation
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        app = QApplication(sys.argv)
        app.setApplicationName("OCRmyPDF GUI")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("OCRmyPDF GUI")
        
        # Set application icon if available
        icon_path = os.path.join("resources", "icons", "app_icon.png")
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            
        # Load and apply stylesheet if available
        style_path = os.path.join("resources", "styles.qss")
        if os.path.exists(style_path):
            try:
                with open(style_path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                    app.setStyleSheet(stylesheet)
                    logger.info("Stylesheet loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load stylesheet: {e}")
        
        # Create and show main window
        window = MainWindow()
        window.show()
        
        logger.info("Application started successfully")
        sys.exit(app.exec_())
        
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        print(f"Error: Missing required dependency - {e}")
        print("Please install required packages using: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        print(f"Error: Application failed to start - {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()