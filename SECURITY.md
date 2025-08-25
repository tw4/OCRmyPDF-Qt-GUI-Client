# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security vulnerabilities seriously. If you discover a security vulnerability in OCRmyPDF GUI Client, please report it privately.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please send an email to: [security@your-domain.com] with the following information:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** assessment
4. **Suggested fix** (if you have one)

### What to Expect

- **Acknowledgment**: We will acknowledge receipt of your report within 48 hours
- **Investigation**: We will investigate and validate the vulnerability
- **Timeline**: We aim to provide an initial response within 5 business days
- **Updates**: We will keep you informed of our progress
- **Resolution**: We will work on a fix and coordinate disclosure

### Security Considerations

This application processes PDF files and interacts with system components. Please be aware of:

#### Input Validation
- PDF files are processed using OCRmyPDF and Tesseract
- The application validates file types and extensions
- Malicious PDFs could potentially exploit underlying libraries

#### System Dependencies
- **Tesseract OCR**: Image processing component
- **Ghostscript**: PDF manipulation (note: historically had security issues)
- **PyQt5**: GUI framework
- **Python libraries**: Various PDF and image processing libraries

#### Temporary Files
- The application creates temporary files during processing
- Temporary files are cleaned up after processing
- Ensure temporary directories have appropriate permissions

#### Network Access
- The application does not make network requests by default
- No telemetry or analytics are collected
- All processing is done locally

### Best Practices for Users

1. **Keep dependencies updated**: Regularly update system dependencies
2. **Scan input files**: Be cautious with PDFs from untrusted sources
3. **Run with limited privileges**: Don't run as administrator/root unless necessary
4. **Monitor temp directories**: Ensure temp files are properly cleaned
5. **Firewall configuration**: Block unnecessary network access if desired

### Dependency Security

We monitor security advisories for:
- **OCRmyPDF**: Core OCR processing library
- **PyQt5**: GUI framework
- **Pillow**: Image processing
- **Tesseract**: OCR engine
- **Ghostscript**: PDF processing

### Reporting Security Issues in Dependencies

If you find security issues in our dependencies:

1. **OCRmyPDF**: Report to https://github.com/ocrmypdf/OCRmyPDF/security
2. **PyQt5**: Report to Riverbank Computing
3. **Other Python packages**: Report to respective maintainers
4. **System tools**: Report to your OS/distribution maintainers

### Security Updates

Security fixes will be:
- **Released promptly** after validation
- **Documented** in release notes
- **Announced** through GitHub releases
- **Tagged** with security advisory labels

### Disclosure Policy

We follow responsible disclosure:

1. **Private reporting** and investigation
2. **Coordinated disclosure** with reporters
3. **Public disclosure** after fixes are available
4. **Credit given** to reporters (if desired)

### License and Legal

This security policy is governed by the same Mozilla Public License 2.0 as the project. Reporting security vulnerabilities does not grant any special rights or create any legal obligations beyond those already present in the license.

### Contact

For security-related questions or concerns:
- **Email**: [security contact - to be added]
- **PGP Key**: [PGP key if available]

Thank you for helping keep OCRmyPDF GUI Client secure!