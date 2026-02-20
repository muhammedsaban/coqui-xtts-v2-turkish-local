@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Sanal ortam bulunamadi, varsayilan python kullanilacak.
    python -m pip install -r requirements.txt
    python app.py --mode gradio
    goto :EOF
)

echo [INFO] .venv bulundu, .venv kullaniliyor.
".venv\Scripts\python.exe" -m pip install -r requirements.txt
".venv\Scripts\python.exe" app.py --mode gradio
