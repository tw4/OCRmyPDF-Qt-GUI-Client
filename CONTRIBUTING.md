# Contributing to OCRmyPDF GUI Client

We welcome contributions to the OCRmyPDF GUI Client! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

Before contributing, please ensure you have:

1. **Python 3.10+** installed
2. **System dependencies** installed:
   - Tesseract OCR 4.1.1+
   - Ghostscript 9.54+
   - PyQt5 development libraries

3. **Development tools**:
   ```bash
   pip install black pytest pytest-qt mypy flake8
   ```

### Setting Up Development Environment

1. **Clone the repository**:
   ```bash
   git clone https://github.com/tw4/OCRmyPDF-Qt-GUI-Client.git
   cd OCRmyPDF-Qt-GUI-Client
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install in development mode with dev dependencies
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Development Guidelines

### Code Style

We use **Black** for code formatting. Please run Black on your code before submitting:

```bash
black .
```

### Code Quality

- Use **flake8** for linting:
  ```bash
  flake8 .
  ```

- Use **mypy** for type checking:
  ```bash
  mypy .
  ```

### Coding Standards

1. **Follow PEP 8** style guidelines
2. **Use type hints** where appropriate
3. **Write docstrings** for all public functions and classes
4. **Keep functions focused** and single-purpose
5. **Use meaningful variable names**

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run GUI tests (requires display)
pytest tests/test_gui.py
```

#### Writing Tests

- Place tests in the `tests/` directory
- Use pytest fixtures for setup/teardown
- Mock external dependencies (OCRmyPDF, file system)
- Test both success and failure scenarios

Example test structure:
```python
import pytest
from unittest.mock import Mock, patch
from gui.main_window import MainWindow

def test_add_files_valid_pdfs(qtbot):
    """Test adding valid PDF files to the application."""
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Test implementation here
    assert len(window.file_list) == 0  # Initial state
    # Add your test logic
```

## Contributing Workflow

### 1. Issue First

- **Check existing issues** before creating new ones
- **Create an issue** to discuss new features or significant changes
- **Use issue templates** when available

### 2. Fork and Branch

1. **Fork** the repository on GitHub
2. **Create a feature branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### 3. Make Changes

1. **Write code** following the guidelines above
2. **Add tests** for new functionality
3. **Update documentation** if needed
4. **Commit frequently** with clear messages:
   ```bash
   git commit -m "feat: add batch processing progress indicator"
   ```

### 4. Commit Message Format

Use conventional commit format:
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or modifying tests
- `chore:` - Maintenance tasks

### 5. Submit Pull Request

1. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub
3. **Fill out the PR template** completely
4. **Link related issues** using keywords (fixes #123)

## Pull Request Guidelines

### PR Requirements

- [ ] Code follows project style guidelines
- [ ] Tests pass locally
- [ ] New functionality has tests
- [ ] Documentation is updated
- [ ] Commit messages follow convention
- [ ] PR description explains the changes

### PR Review Process

1. **Automated checks** must pass (CI/CD)
2. **Code review** by maintainers
3. **Address feedback** promptly
4. **Squash merge** after approval

## Specific Contribution Areas

### Bug Fixes

1. **Reproduce the bug** with test cases
2. **Fix the issue** with minimal changes
3. **Add regression tests** to prevent recurrence
4. **Update documentation** if behavior changes

### New Features

1. **Discuss the feature** in an issue first
2. **Design the API** before implementation
3. **Implement incrementally** with tests
4. **Update user documentation**
5. **Consider backward compatibility**

### UI/UX Improvements

1. **Follow Qt design guidelines**
2. **Maintain dark theme compatibility**
3. **Test on multiple platforms** if possible
4. **Consider accessibility** requirements
5. **Get feedback** from users when possible

### Documentation

1. **Keep README.md up to date**
2. **Document new features** clearly
3. **Include code examples** where helpful
4. **Update installation instructions** as needed

## Getting Help

### Communication Channels

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Code Review**: PR comments for specific code feedback

### Resources

- **OCRmyPDF Documentation**: https://ocrmypdf.readthedocs.io/
- **PyQt5 Documentation**: https://doc.qt.io/qtforpython/
- **Python Testing**: https://docs.pytest.org/

## Recognition

Contributors will be recognized in:
- **CONTRIBUTORS.md** file
- **Release notes** for significant contributions
- **About dialog** in the application

## License

By contributing, you agree that your contributions will be licensed under the Mozilla Public License 2.0, the same license that covers the project.

Thank you for contributing to OCRmyPDF GUI Client! 🎉