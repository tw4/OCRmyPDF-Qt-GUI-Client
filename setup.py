#!/usr/bin/env python3
"""
OCRmyPDF Qt GUI Client - Setup Script
"""

from setuptools import setup, find_packages
import os


def read_requirements():
    """Read requirements from requirements.txt"""
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = []
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-'):
                requirements.append(line)
    return requirements


def read_readme():
    """Read README file"""
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "OCRmyPDF Qt GUI Client - A user-friendly interface for OCRmyPDF"


setup(
    name="ocrmypdf-gui",
    version="1.0.0",
    description="A user-friendly Qt GUI client for OCRmyPDF",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="OCRmyPDF GUI Team",
    author_email="contact@ocrmypdf-gui.org",
    url="https://github.com/tw4/OCRmyPDF-Qt-GUI-Client",
    
    packages=find_packages(),
    include_package_data=True,
    
    install_requires=read_requirements(),
    
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-qt>=4.0.0',
            'black>=22.0.0',
            'flake8>=4.0.0',
            'mypy>=0.950',
        ],
    },
    
    entry_points={
        'console_scripts': [
            'ocrmypdf-gui=main:main',
        ],
        'gui_scripts': [
            'ocrmypdf-gui-windowed=main:main',
        ],
    },
    
    package_data={
        '': [
            'resources/icons/*.png',
            'resources/icons/*.ico',
            'resources/translations/*.qm',
            'resources/*.qss',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Office/Business :: Office Suites',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Win32 (MS Windows)',
        'Environment :: MacOS X',
    ],
    
    python_requires='>=3.8',
    
    keywords='ocr pdf tesseract gui pyqt5 document-processing',
    
    project_urls={
        'Bug Reports': 'https://github.com/tw4/OCRmyPDF-Qt-GUI-Client/issues',
        'Source': 'https://github.com/tw4/OCRmyPDF-Qt-GUI-Client',
        'Documentation': 'https://github.com/tw4/OCRmyPDF-Qt-GUI-Client',
    },
    
    zip_safe=False,
)