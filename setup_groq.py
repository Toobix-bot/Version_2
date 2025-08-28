#!/usr/bin/env python3
"""
Toobix Groq API Setup
Hilft beim Einrichten der Groq API
"""
import os
from pathlib import Path

def setup_groq_api():
    """Setzt Groq API Key in .env Datei"""
    print("🔧 Groq API Setup für Toobix")
    print("=" * 40)
    
    # .env Datei finden
    env_file = Path('.env')
    
    if not env_file.exists():
        print("❌ .env Datei nicht gefunden!")
        print("💡 Führe zuerst 'python setup.py' aus")
        return
    
    # Aktuellen API Key prüfen
    current_key = ""
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if "GROQ_API_KEY=your_groq_api_key_here" in content:
        print("🔍 Noch kein Groq API Key gesetzt")
    else:
        print("✅ Groq API Key ist bereits konfiguriert")
        response = input("🤔 Möchtest du ihn ändern? (j/n): ")
        if response.lower() not in ['j', 'y', 'ja', 'yes']:
            return
    
    print("\n📋 Groq API Key Setup:")
    print("1. Gehe zu: https://console.groq.com/keys")
    print("2. Erstelle kostenlosen Account (falls noch nicht vorhanden)")
    print("3. Erstelle neuen API Key")
    print("4. Kopiere den Key und füge ihn hier ein")
    
    print("\n" + "="*50)
    api_key = input("🔑 Füge deinen Groq API Key hier ein: ").strip()
    
    if not api_key:
        print("❌ Kein API Key eingegeben - Abbruch")
        return
    
    if len(api_key) < 20:
        print("⚠️ API Key scheint zu kurz zu sein - bist du sicher?")
        response = input("Trotzdem verwenden? (j/n): ")
        if response.lower() not in ['j', 'y', 'ja', 'yes']:
            return
    
    # .env Datei aktualisieren
    try:
        with open(env_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # API Key ersetzen
        new_content = content.replace(
            "GROQ_API_KEY=your_groq_api_key_here",
            f"GROQ_API_KEY={api_key}"
        )
        
        # Falls bereits ein anderer Key gesetzt war
        if "GROQ_API_KEY=" in content and api_key not in content:
            lines = new_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('GROQ_API_KEY='):
                    lines[i] = f"GROQ_API_KEY={api_key}"
                    break
            new_content = '\n'.join(lines)
        
        # Datei schreiben
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Groq API Key erfolgreich gesetzt!")
        print("\n🚀 Starte Toobix neu um die Änderungen zu übernehmen:")
        print("   python main.py")
        
    except Exception as e:
        print(f"❌ Fehler beim Speichern: {e}")

def test_groq_connection():
    """Testet Groq API Verbindung"""
    try:
        from toobix.config.settings import Settings
        from toobix.core.ai_handler import AIHandler
        import asyncio
        
        print("\n🧪 Teste Groq API Verbindung...")
        
        settings = Settings()
        ai_handler = AIHandler(settings)
        
        if not ai_handler.groq_available:
            print("❌ Groq nicht verfügbar - prüfe API Key")
            return
        
        # Einfache Test-Anfrage
        async def test():
            response = await ai_handler._query_groq("Sage einfach nur 'Hallo' auf Deutsch.")
            return response
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(test())
        
        if result and "hallo" in result.lower():
            print("✅ Groq API funktioniert einwandfrei!")
            print(f"🤖 Test-Antwort: {result}")
        else:
            print(f"⚠️ Unerwartete Antwort: {result}")
            
    except Exception as e:
        print(f"❌ Groq Test fehlgeschlagen: {e}")

def main():
    try:
        setup_groq_api()
        
        # Optional: Verbindung testen
        test_response = input("\n🧪 Möchtest du die Verbindung testen? (j/n): ")
        if test_response.lower() in ['j', 'y', 'ja', 'yes']:
            test_groq_connection()
            
    except KeyboardInterrupt:
        print("\n👋 Setup abgebrochen")
    except Exception as e:
        print(f"❌ Unerwarteter Fehler: {e}")

if __name__ == "__main__":
    main()
