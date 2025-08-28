@echo off
echo 🚀 Toobix AI Assistant wird gestartet...
echo.

REM Prüfe ob Ollama läuft
echo 🔍 Prüfe Ollama-Verbindung...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Ollama ist nicht erreichbar!
    echo 💡 Bitte starte Ollama zuerst:
    echo    ollama serve
    echo.
    echo ⏸️  Drücke eine Taste um trotzdem fortzufahren oder Ctrl+C um abzubrechen...
    pause >nul
)

REM Starte Toobix
echo ✅ Starte Toobix...
python main.py

echo.
echo 👋 Toobix beendet.
pause
