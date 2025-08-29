"""
Toobix AI Assistant - Main Application
Ein vollständiger AI Desktop-Assistent mit lokaler und Cloud-KI
"""
import sys
import os
import asyncio
from pathlib import Path

# Add toobix to path
sys.path.append(str(Path(__file__).parent))

from toobix.core.ai_handler import AIHandler
from toobix.core.speech_engine import SpeechEngine
from toobix.core.desktop_integration import DesktopIntegration
from toobix.config.settings import Settings

class ToobixAssistant:
    """Hauptklasse für den Toobix AI-Assistenten"""
    
    def __init__(self):
        print("🚀 Toobix AI Assistant wird gestartet...")
        
        # Konfiguration laden
        self.settings = Settings()
        
        # Komponenten initialisieren
        self.ai_handler = AIHandler(self.settings)
        self.speech_engine = SpeechEngine(self.settings)
        self.desktop = DesktopIntegration()
        
        # GUI erstellen - NEUE MODERNE VERSION
        try:
            from toobix.gui.modern_gui import create_modern_gui
            self.gui = create_modern_gui(
                ai_handler=self.ai_handler,
                speech_engine=self.speech_engine,
                desktop=self.desktop,
                settings=self.settings
            )
            print("🌟 Moderne GUI aktiviert!")
        except Exception as e:
            print(f"⚠️ Fallback zur klassischen GUI: {e}")
            # Fallback zur alten GUI
            from toobix.gui.main_window import ToobixGUI
            self.gui = ToobixGUI(
                ai_handler=self.ai_handler,
                speech_engine=self.speech_engine,
                desktop=self.desktop,
                settings=self.settings
            )
        
        print("✅ Toobix ist bereit!")
    
    def run(self):
        """Startet die Hauptanwendung"""
        try:
            # GUI starten - Check welche GUI verwendet wird
            if hasattr(self.gui, 'run'):
                # Moderne GUI
                print("🌟 Starte moderne GUI...")
                self.gui.run()
            else:
                # Klassische GUI
                print("🎨 GUI gestartet - Toobix ist bereit!")
                
                # TTS nur einmal beim Start
                try:
                    self.speech_engine.speak("Toobix Optimized ist bereit!", wait=False)
                except:
                    print("🔇 TTS beim Start nicht verfügbar")
                
                self.gui.run()
            
        except KeyboardInterrupt:
            print("\n👋 Toobix wird beendet...")
        except Exception as e:
            print(f"❌ Fehler beim Starten von Toobix: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Aufräumen beim Beenden"""
        if hasattr(self, 'speech_engine'):
            self.speech_engine.stop()
        print("🔄 Toobix beendet.")

def main():
    """Haupteinstiegspunkt"""
    try:
        # Prüfe ob Ollama läuft
        print("🔍 Prüfe Systemvoraussetzungen...")
        
        toobix = ToobixAssistant()
        toobix.run()
        
    except Exception as e:
        print(f"❌ Kritischer Fehler: {e}")
        input("Drücke Enter zum Beenden...")

if __name__ == "__main__":
    main()
