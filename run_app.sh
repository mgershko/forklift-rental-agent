#!/bin/bash

# Create and activate virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment (different command based on OS)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download DejaVu fonts for PDF generation
echo "Setting up fonts for PDF generation..."
mkdir -p fonts
cd fonts
# Download DejaVu fonts if they don't exist
if [ ! -f "DejaVuSansCondensed.ttf" ]; then
    echo "Downloading DejaVu fonts..."
    curl -L -o dejavu.zip https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip/download
    unzip dejavu.zip
    cp dejavu-fonts-ttf*/ttf/DejaVuSansCondensed*.ttf .
    rm -rf dejavu-fonts-ttf*
    rm dejavu.zip
fi
cd ..

# Copy fonts to the right location for FPDF
mkdir -p src/fonts
cp fonts/DejaVuSansCondensed*.ttf src/fonts/

# Run the application
echo "Starting Streamlit application..."
streamlit run app.py

# Note: The virtual environment will be deactivated when the terminal is closed
