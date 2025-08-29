"""
Toobix Feature Verification & Setup Script
Überprüft und initialisiert alle Peace Catalyst Features
"""
import os
import sys
from pathlib import Path

def check_feature_availability():
    """Überprüft die Verfügbarkeit aller Toobix Features"""
    
    print("🔍 TOOBIX FEATURE VERIFICATION")
    print("=" * 50)
    
    # Basis-Check
    toobix_path = Path(__file__).parent / "toobix"
    if not toobix_path.exists():
        print("❌ Toobix Hauptverzeichnis nicht gefunden!")
        return False
    
    features = {
        "Core Features": {
            "ai_handler.py": toobix_path / "core" / "ai_handler.py",
            "settings.py": toobix_path / "config" / "settings.py",
            "main_window.py": toobix_path / "gui" / "main_window.py"
        },
        "Peace Catalyst (Phase 5)": {
            "peace_harmony_hub.py": toobix_path / "core" / "peace_harmony_hub.py",
            "soul_journal_engine.py": toobix_path / "core" / "soul_journal_engine.py",
            "artefakt_system.py": toobix_path / "core" / "artefakt_system.py",
            "agent_network.py": toobix_path / "core" / "agent_network.py",
            "creative_wellness_engine.py": toobix_path / "core" / "creative_wellness_engine.py"
        },
        "KI-Enhanced (Phase 3)": {
            "intelligent_context_manager.py": toobix_path / "core" / "intelligent_context_manager.py",
            "productivity_gamification.py": toobix_path / "core" / "productivity_gamification.py",
            "deep_analytics_engine.py": toobix_path / "core" / "deep_analytics_engine.py"
        },
        "GUI Components": {
            "soul_journal_gui.py": toobix_path / "gui" / "soul_journal_gui.py",
            "artefakt_system_gui.py": toobix_path / "gui" / "artefakt_system_gui.py",
            "modern_gui.py": toobix_path / "gui" / "modern_gui.py"
        }
    }
    
    all_available = True
    
    for category, files in features.items():
        print(f"\n📂 {category}:")
        for name, path in files.items():
            if path.exists():
                print(f"   ✅ {name}")
            else:
                print(f"   ❌ {name} - FEHLT!")
                all_available = False
    
    return all_available

def check_dependencies():
    """Überprüft Python-Dependencies"""
    print(f"\n🐍 PYTHON DEPENDENCIES:")
    
    required_packages = [
        "requests", "aiohttp", "tkinter", "customtkinter", 
        "speechrecognition", "pyttsx3", "python-dotenv",
        "pygame", "pillow", "matplotlib", "numpy"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == "tkinter":
                import tkinter
            elif package == "customtkinter":
                import customtkinter
            elif package == "speechrecognition":
                import speech_recognition
            elif package == "pyttsx3":
                import pyttsx3
            elif package == "python-dotenv":
                import dotenv
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - FEHLT!")
            missing_packages.append(package)
    
    return missing_packages

def check_ai_config():
    """Überprüft AI-Konfiguration"""
    print(f"\n🤖 AI CONFIGURATION:")
    
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        print("   ✅ .env Datei gefunden")
        
        # Lade Environment Variables
        from dotenv import load_dotenv
        load_dotenv(env_file)
        
        # Prüfe wichtige Settings
        ollama_model = os.getenv('OLLAMA_MODEL', 'nicht gesetzt')
        groq_key = os.getenv('GROQ_API_KEY', 'nicht gesetzt')
        groq_model = os.getenv('GROQ_MODEL', 'nicht gesetzt')
        
        print(f"   📋 Ollama Model: {ollama_model}")
        print(f"   📋 Groq Model: {groq_model}")
        print(f"   🔑 Groq API Key: {'✅ Gesetzt' if groq_key and groq_key != 'your_groq_api_key_here' and groq_key != 'nicht gesetzt' else '❌ Nicht gesetzt'}")
        
        return groq_key and groq_key != 'your_groq_api_key_here' and groq_key != 'nicht gesetzt'
    else:
        print("   ❌ .env Datei nicht gefunden!")
        print("   💡 Kopiere .env.example zu .env und setze API Keys")
        return False

def test_ai_connectivity():
    """Testet AI-Verbindungen"""
    print(f"\n🔗 AI CONNECTIVITY TEST:")
    
    # Test Ollama
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            print("   ✅ Ollama erreichbar")
        else:
            print("   ⚠️ Ollama antwortet nicht korrekt")
    except Exception as e:
        print(f"   ❌ Ollama nicht erreichbar: {e}")
    
    # Test Groq (wenn API Key gesetzt)
    if check_ai_config():
        print("   ✅ Groq API Key konfiguriert")
    else:
        print("   ⚠️ Groq API Key nicht gesetzt")

def main():
    """Hauptfunktion"""
    print("🚀 TOOBIX SETUP & VERIFICATION")
    print("=" * 50)
    
    # Feature Availability Check
    features_ok = check_feature_availability()
    
    # Dependencies Check
    missing_deps = check_dependencies()
    
    # AI Configuration Check
    ai_config_ok = check_ai_config()
    
    # AI Connectivity Test
    test_ai_connectivity()
    
    # Summary
    print(f"\n📊 ZUSAMMENFASSUNG:")
    print("=" * 30)
    
    if features_ok:
        print("✅ Alle Features verfügbar")
    else:
        print("❌ Einige Features fehlen!")
    
    if not missing_deps:
        print("✅ Alle Dependencies installiert")
    else:
        print(f"❌ Fehlende Packages: {', '.join(missing_deps)}")
        print(f"💡 Installiere mit: pip install {' '.join(missing_deps)}")
    
    if ai_config_ok:
        print("✅ AI-Konfiguration vollständig")
    else:
        print("⚠️ AI-Konfiguration unvollständig")
        print("💡 Setze GROQ_API_KEY in .env Datei")
    
    # Gesamtstatus
    overall_status = features_ok and not missing_deps and ai_config_ok
    
    print(f"\n🎯 GESAMTSTATUS: {'✅ BEREIT' if overall_status else '⚠️ SETUP ERFORDERLICH'}")
    
    if overall_status:
        print("\n🚀 Toobix kann gestartet werden mit: python main.py")
    else:
        print("\n🔧 Bitte behebe die genannten Probleme vor dem Start")

if __name__ == "__main__":
    main()
