@echo off
echo.
echo 🔐 TOOBIX API KEY SETUP
echo ========================
echo.
echo ✅ .env Datei erstellt!
echo.
echo 📝 NÄCHSTE SCHRITTE:
echo.
echo 1. Öffne die .env Datei:
echo    notepad .env
echo.
echo 2. Hole dir einen Groq API Key:
echo    https://console.groq.com/keys
echo.
echo 3. Ersetze in .env:
echo    GROQ_API_KEY=dein_groq_api_key_hier
echo    mit deinem echten Key:
echo    GROQ_API_KEY=gsk_your_real_key_here
echo.
echo 4. Speichere und schließe die Datei
echo.
echo 5. Starte Toobix:
echo    python main.py
echo.
echo 🛡️ SICHERHEIT:
echo - .env ist bereits in .gitignore geschützt
echo - Keys werden NIEMALS in Git gespeichert
echo - Nur lokal auf deinem PC verfügbar
echo.
echo Möchtest du die .env Datei jetzt öffnen? (j/n)
set /p choice=
if /i "%choice%"=="j" notepad .env
if /i "%choice%"=="y" notepad .env
echo.
echo 🚀 Fertig! Nach dem Key-Setup: python main.py
pause
