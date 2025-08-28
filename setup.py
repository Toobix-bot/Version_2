#!/usr/bin/env python3
"""
Toobix Quick Setup
Hilft beim ersten Setup von Toobix
"""
import os
import sys
import subprocess
from pathlib import Path

def check_ollama():
    """Prüft ob Ollama installiert ist"""
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True)
        if result.returncode == 0:
            print("✅ Ollama ist installiert")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ollama ist nicht installiert!")
    print("📥 Installiere Ollama von: https://ollama.com")
    return False

def setup_ollama_model():
    """Setzt Ollama Modell auf"""
    try:
        print("📥 Lade Gemma 2B Modell...")
        result = subprocess.run(['ollama', 'pull', 'gemma2:2b'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Gemma 2B erfolgreich installiert")
            return True
        else:
            print(f"❌ Fehler beim Laden des Modells: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Fehler beim Setup: {e}")
        return False

def create_env_file():
    """Erstellt .env Datei aus Beispiel"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_file.exists():
        print("✅ .env Datei existiert bereits")
        return True
    
    if env_example.exists():
        env_example.rename(env_file)
        print("✅ .env Datei erstellt")
        print("💡 Du kannst die .env Datei bearbeiten um Einstellungen anzupassen")
        return True
    else:
        print("❌ .env.example nicht gefunden")
        return False

def main():
    print("🛠️ Toobix Setup")
    print("=" * 50)
    
    # Prüfe Python-Version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ erforderlich")
        return
    
    print(f"✅ Python {sys.version}")
    
    # Ollama prüfen
    if not check_ollama():
        print("\n❌ Setup kann nicht fortgesetzt werden ohne Ollama")
        return
    
    # .env erstellen
    create_env_file()
    
    # Ollama Modell installieren
    setup_ollama_model()
    
    print("\n🎉 Setup abgeschlossen!")
    print("\n📖 Nächste Schritte:")
    print("1. Starte Ollama: ollama serve")
    print("2. Starte Toobix: python main.py")
    print("3. Optional: Bearbeite .env für Groq API Key")

if __name__ == "__main__":
    main()
