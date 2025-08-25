# OCRmyPDF Qt GUI Client

A user-friendly Qt-based graphical interface for [OCRmyPDF](https://ocrmypdf.readthedocs.io/), making it easy to add OCR text layers to scanned PDF documents.

## Features

- **Modern Qt Interface**: Clean, responsive GUI built with PyQt5
- **Drag & Drop Support**: Simply drag PDF files into the application window
- **Batch Processing**: Process multiple PDF files simultaneously
- **Multi-language OCR**: Support for 100+ languages via Tesseract OCR
- **Advanced Settings**: Full access to OCRmyPDF's powerful features
- **Real-time Progress**: Monitor processing with detailed progress information
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### System Requirements

**Minimum Requirements:**
- **Operating System**: Windows 10, macOS 10.14, or Linux with Qt5 support
- **Architecture**: 64-bit system (strongly recommended)
- **Python**: 3.10 or newer (64-bit recommended)
- **RAM**: 2 GB (4 GB recommended for large files)
- **Storage**: 1 GB free space for temporary files

### Required System Dependencies

**IMPORTANT**: These system dependencies must be installed BEFORE running the application:

#### 1. **Python 3.10+**
- **Ubuntu/Debian**: `sudo apt update && sudo apt install python3 python3-pip python3-venv`
- **Fedora/RHEL**: `sudo dnf install python3 python3-pip`
- **macOS**: `brew install python3` or download from [python.org](https://python.org)
- **Windows**: Download from [python.org](https://python.org) (make sure to check "Add to PATH")

#### 2. **Tesseract OCR 4.1.1+** (Required)
- **Ubuntu/Debian**: `sudo apt install tesseract-ocr tesseract-osd`
- **Fedora/RHEL**: `sudo dnf install tesseract tesseract-osd`
- **macOS**: `brew install tesseract`
- **Windows**: Download from [UB-Mannheim Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)

#### 3. **Ghostscript 9.54+** (Required)
- **Ubuntu/Debian**: `sudo apt install ghostscript`
- **Fedora/RHEL**: `sudo dnf install ghostscript`
- **macOS**: `brew install ghostscript`
- **Windows**: Download from [Ghostscript Downloads](https://www.ghostscript.com/download/gsdnld.html)

#### 4. **Additional Language Support** (Optional but Recommended)
For better OCR accuracy in different languages:

**Turkish Language Pack:**
- **Ubuntu/Debian**: `sudo apt install tesseract-ocr-tur`
- **Fedora/RHEL**: `sudo dnf install tesseract-langpack-tur`
- **macOS**: `brew install tesseract-lang`
- **Windows**: Download language data files from [tessdata repository](https://github.com/tesseract-ocr/tessdata)

**Other Languages:**
- **German**: `tesseract-ocr-deu` / `tesseract-langpack-deu`
- **French**: `tesseract-ocr-fra` / `tesseract-langpack-fra`
- **Spanish**: `tesseract-ocr-spa` / `tesseract-langpack-spa`
- **Russian**: `tesseract-ocr-rus` / `tesseract-langpack-rus`

#### 5. **Optional Performance Enhancements**
- **jbig2enc** (for better PDF compression): 
  - Ubuntu/Debian: `sudo apt install jbig2enc`
  - macOS: `brew install jbig2enc`
- **pngquant** (for PNG optimization):
  - Ubuntu/Debian: `sudo apt install pngquant`
  - macOS: `brew install pngquant`
- **unpaper** (for additional cleaning options):
  - Ubuntu/Debian: `sudo apt install unpaper`
  - macOS: `brew install unpaper`

### Verification Commands

After installing dependencies, verify they are working:

```bash
# Check Python version (should be 3.10+)
python3 --version

# Check Tesseract installation
tesseract --version
tesseract --list-langs

# Check Ghostscript installation
gs --version
```

### Quick Start

1. **Clone or download this repository**
2. **Run the application using the startup script**:
   ```bash
   ./run_app.sh
   ```
   
   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python main.py
   ```

## Usage

### Launch the Application

```bash
# From command line
ocrmypdf-gui

# Or run directly
python main.py
```

### Basic Workflow

1. **Add Files**: Drag PDF files into the window or use "Add Files" button
2. **Configure Settings**: Choose OCR language and processing options
3. **Start Processing**: Click "Start Processing" to begin OCR
4. **Monitor Progress**: Watch real-time progress in the progress dialog
5. **Access Results**: Find processed files in the output directory

### Advanced Configuration

Access advanced settings through Edit → Settings:

- **OCR Languages**: Select single or multiple OCR languages
- **Page Processing**: Enable auto-rotation, deskewing, and cleaning
- **Image Quality**: Adjust DPI and compression settings
- **PDF Output**: Choose PDF/A formats and optimization levels
- **Performance**: Configure CPU threads and memory usage

## System Requirements

### Minimum Requirements
- **OS**: Windows 10, macOS 10.14, or Linux with Qt5 support
- **RAM**: 2 GB (4 GB recommended for large files)
- **Storage**: 500 MB free space
- **Python**: 3.8 or newer

### Recommended Requirements
- **RAM**: 4 GB or more for processing large PDF files
- **CPU**: Multi-core processor for parallel processing
- **Storage**: 1 GB free space for temporary files

## Supported File Formats

### Input
- PDF files (including scanned PDFs)
- Password-protected PDFs (with manual password entry)

### Output
- Standard PDF with OCR text layer
- PDF/A-1b, PDF/A-2b, PDF/A-3b (archival formats)

## Configuration

The application stores settings in platform-specific locations:

- **Windows**: `%APPDATA%\OCRmyPDF-GUI\OCRmyPDF-GUI.ini`
- **macOS**: `~/Library/Preferences/com.OCRmyPDF-GUI.OCRmyPDF-GUI.plist`
- **Linux**: `~/.config/OCRmyPDF-GUI/OCRmyPDF-GUI.conf`

## Troubleshooting

### Common Issues

**"OCRmyPDF not found" error**
```bash
pip install ocrmypdf
```

**"Tesseract not found" error**
- Ensure Tesseract is installed and added to system PATH
- Check installation: `tesseract --version`

**"Ghostscript not found" error**
- Install Ghostscript for your platform
- Check installation: `gs --version`

**Memory errors with large files**
- Reduce the number of parallel jobs in settings
- Increase system memory or use smaller files

### Enable Debug Logging

Run with verbose logging to diagnose issues:

```bash
python main.py --verbose
```

Logs are saved to `ocr_gui.log` in the application directory.

## Development

### Setup Development Environment

```bash
git clone https://github.com/your-username/ocrmypdf-gui.git
cd ocrmypdf-gui
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -e .[dev]
```

### Run Tests

```bash
pytest tests/
```

### Code Style

This project uses Black for code formatting:

```bash
black .
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Format code with Black (`black .`)
7. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
8. Push to the branch (`git push origin feature/AmazingFeature`)
9. Open a Pull Request

## License and Legal Information

This project is licensed under the **Mozilla Public License 2.0** - see the [LICENSE](LICENSE) file for full details.

### Third-Party Components

This application uses several third-party components, each with their own licenses:

- **OCRmyPDF**: Licensed under Mozilla Public License 2.0 ([Source](https://github.com/ocrmypdf/OCRmyPDF))
- **PyQt5**: Licensed under GPL v3 / Commercial License
- **Tesseract OCR**: Licensed under Apache License 2.0
- **Ghostscript**: Licensed under AGPL v3 / Commercial License
- **Pillow**: Licensed under PIL Software License

### Attribution Requirements

As required by the Mozilla Public License 2.0:
- This application is a derivative work that provides a graphical user interface for OCRmyPDF functionality
- Source code is available and governed by the MPL 2.0 license terms
- Recipients are informed that the source code is available under these license terms
- All original license notices have been preserved

### Commercial Use

- This GUI application: Free for commercial use under MPL 2.0
- OCRmyPDF: Free for commercial use under MPL 2.0
- PyQt5: Requires commercial license for commercial applications (or use GPL v3)
- Ghostscript: May require commercial license for commercial use (check AGPL v3 requirements)

Please review the individual license terms for each component before commercial deployment.

## Acknowledgments

- **[OCRmyPDF](https://ocrmypdf.readthedocs.io/)** - The powerful OCR engine that powers this GUI
- **[Tesseract OCR](https://github.com/tesseract-ocr/tesseract)** - Open source OCR engine by Google
- **[PyQt5](https://www.riverbankcomputing.com/software/pyqt/)** - The cross-platform GUI framework
- **[Ghostscript](https://www.ghostscript.com/)** - PostScript and PDF interpreter
- **The OCRmyPDF Community** - For developing and maintaining the excellent OCR processing library

## Support

- **Documentation**: [Read the Docs](https://ocrmypdf-gui.readthedocs.io)
- **Issues**: [GitHub Issues](https://github.com/your-username/ocrmypdf-gui/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/ocrmypdf-gui/discussions)

## Changelog

### Version 1.0.0 (2024-XX-XX)
- Initial release
- Basic OCR functionality with GUI
- Drag & drop support
- Multi-language OCR support
- Batch processing capabilities
- Advanced settings dialog
- Cross-platform support# OCRmyPDF-Qt-GUI-Client
