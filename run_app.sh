#!/bin/bash
# OCRmyPDF GUI Client - Startup Script

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
else
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if icons need to be created
if [ ! -f "resources/icons/app_icon.png" ]; then
    echo "Creating application icons..."
    python create_icons.py
fi

echo "Starting OCRmyPDF GUI..."
python main.py