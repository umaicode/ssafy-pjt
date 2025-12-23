@echo off
echo 🚀 Financial AI RAG System Setup
echo ================================

REM Check Python version
python --version

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ⚠️  Please edit .env file and add your API keys:
    echo    - OPENAI_API_KEY
    echo    - YOUTUBE_API_KEY
    echo    - NEWS_API_KEY
)

REM Create data directory
mkdir backend\data 2>nul
mkdir chroma_db 2>nul

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Edit .env file with your API keys
echo 3. Start the server: python backend\main.py
echo 4. Visit http://localhost:8000/docs for API documentation

pause
