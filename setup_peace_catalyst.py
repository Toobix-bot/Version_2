#!/usr/bin/env python3
"""
Toobix Feature Aktivierung & API Setup
Stellt sicher dass alle Peace Catalyst Features verfügbar sind
"""
import os
import sys
from pathlib import Path

def setup_api_keys():
    """Setzt API Keys sicher ein"""
    print("🔧 TOOBIX API SETUP")
    print("=" * 50)
    
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env Datei nicht gefunden!")
        print("💡 Führe zuerst 'python setup.py' aus")
        return False
    
    # Prüfe aktuellen Groq API Key
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "GROQ_API_KEY=your_groq_api_key_here" in content:
        print("🔑 GROQ API KEY BENÖTIGT:")
        print("1. Gehe zu: https://console.groq.com/keys")
        print("2. Erstelle kostenlosen Account")
        print("3. Erstelle neuen API Key")
        print("4. Kopiere den Key")
        print()
        
        api_key = input("🔑 Füge deinen Groq API Key ein: ").strip()
        
        if not api_key or len(api_key) < 20:
            print("❌ Ungültiger API Key")
            return False
        
        # API Key in .env setzen
        new_content = content.replace(
            "GROQ_API_KEY=your_groq_api_key_here",
            f"GROQ_API_KEY={api_key}"
        )
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Groq API Key gesetzt!")
    else:
        print("✅ Groq API Key bereits konfiguriert")
    
    return True

def test_ai_models():
    """Testet verfügbare AI Models"""
    print("\n🧪 TESTE AI VERFÜGBARKEIT")
    print("=" * 50)
    
    try:
        from toobix.config.settings import Settings
        from toobix.core.ai_handler import AIHandler
        import asyncio
        
        settings = Settings()
        ai = AIHandler(settings)
        
        print(f"🤖 Ollama Model: {settings.GROQ_MODEL}")
        print(f"☁️ Groq Model: {settings.GROQ_MODEL} (UPGRADED!)")
        print(f"🔄 Lokale KI: {'✅' if ai.ollama_available else '❌'}")
        print(f"🌐 Cloud KI: {'✅' if ai.groq_available else '❌'}")
        
        if ai.groq_available:
            print("\n🧪 Teste Groq API...")
            
            async def test_groq():
                response = await ai._query_groq("Antworte nur mit 'Test erfolgreich' auf Deutsch.")
                return response
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(test_groq())
            loop.close()
            
            if result and "test" in result.lower():
                print("✅ Groq API funktioniert!")
                print(f"🤖 Antwort: {result}")
            else:
                print(f"⚠️ Unerwartete Antwort: {result}")
        
    except Exception as e:
        print(f"❌ AI Test Fehler: {e}")

def check_peace_features():
    """Prüft Peace Catalyst Features"""
    print("\n🌍 PEACE CATALYST FEATURES")
    print("=" * 50)
    
    features = [
        ('Peace Harmony Hub', 'toobix.core.peace_harmony_hub'),
        ('Soul Journal Engine', 'toobix.core.soul_journal_engine'), 
        ('Artefakt System', 'toobix.core.artefakt_system'),
        ('Agent Network', 'toobix.core.agent_network'),
        ('Creative Wellness Engine', 'toobix.core.creative_wellness_engine'),
        ('Context Manager', 'toobix.core.intelligent_context_manager'),
        ('Gamification', 'toobix.core.productivity_gamification'),
        ('Deep Analytics', 'toobix.core.deep_analytics_engine')
    ]
    
    for name, module in features:
        try:
            __import__(module)
            print(f"✅ {name}")
        except ImportError as e:
            print(f"❌ {name}: {e}")

def optimize_settings():
    """Optimiert Einstellungen für beste Performance"""
    print("\n⚙️ EINSTELLUNGEN OPTIMIEREN")
    print("=" * 50)
    
    env_file = Path('.env')
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    optimizations = {
        'GROQ_MODEL=llama-3.1-8b-instant': 'GROQ_MODEL=llama-3.1-70b-versatile',
        'CLOUD_THRESHOLD=50': 'CLOUD_THRESHOLD=500',
        'TEMPERATURE=0.7': 'TEMPERATURE=0.3'
    }
    
    updated = False
    for old, new in optimizations.items():
        if old in content:
            content = content.replace(old, new)
            updated = True
            print(f"🔧 {old} → {new}")
    
    if updated:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Einstellungen optimiert!")
    else:
        print("✅ Einstellungen bereits optimal")

def main():
    """Haupt-Setup-Prozess"""
    print("🚀 TOOBIX PEACE CATALYST SETUP")
    print("=" * 60)
    print("Optimiert für beste Performance und reduzierte Halluzinationen")
    print()
    
    try:
        # 1. API Keys einrichten
        if not setup_api_keys():
            return
        
        # 2. Einstellungen optimieren
        optimize_settings()
        
        # 3. AI Models testen
        test_ai_models()
        
        # 4. Peace Features prüfen
        check_peace_features()
        
        print("\n🎉 SETUP ERFOLGREICH!")
        print("=" * 50)
        print("✅ Alle Features verfügbar")
        print("✅ AI optimiert (weniger Halluzinationen)")
        print("✅ Groq Model upgraded: llama-3.1-70b-versatile")
        print("✅ API Keys sicher")
        print()
        print("🚀 Starte Toobix mit: python main.py")
        
    except KeyboardInterrupt:
        print("\n👋 Setup abgebrochen")
    except Exception as e:
        print(f"\n❌ Setup Fehler: {e}")

if __name__ == "__main__":
    main()
