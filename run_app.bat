@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo Setting up fonts for PDF generation...
mkdir fonts 2>nul
cd fonts

if not exist DejaVuSansCondensed.ttf (
    echo Downloading DejaVu fonts...
    powershell -Command "Invoke-WebRequest -Uri 'https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip/download' -OutFile 'dejavu.zip'"
    powershell -Command "Expand-Archive -Path 'dejavu.zip' -DestinationPath '.'"
    powershell -Command "Copy-Item -Path '.\dejavu-fonts-ttf*\ttf\DejaVuSansCondensed*.ttf' -Destination '.'"
    powershell -Command "Remove-Item -Recurse -Force 'dejavu-fonts-ttf*'"
    powershell -Command "Remove-Item -Force 'dejavu.zip'"
)
cd ..

echo Copying fonts to the correct location...
mkdir src\fonts 2>nul
copy fonts\DejaVuSansCondensed*.ttf src\fonts\

echo Starting Streamlit application...
streamlit run app.py

echo Note: The virtual environment will be deactivated when the terminal is closed
