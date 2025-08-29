"""
Toobix Configuration Settings
Zentrale Konfiguration für alle Toobix-Komponenten
"""
import os
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    """Zentrale Konfigurationsklasse für Toobix"""
    
    def __init__(self):
        # .env Datei laden wenn vorhanden
        env_path = Path(__file__).parent.parent.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
        
        # === AI Konfiguration ===
        self.OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'gemma2:2b')
        self.OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
        
        # Groq Cloud-Backup - UPGRADED zu bestem verfügbaren Model
        self.GROQ_API_KEY = os.getenv('GROQ_API_KEY', '')
        self.GROQ_MODEL = os.getenv('GROQ_MODEL', 'llama-3.1-70b-versatile')  # Upgraded!
        
        # Wann Cloud-KI verwenden (reduziert für bessere Performance)
        self.CLOUD_THRESHOLD = int(os.getenv('CLOUD_THRESHOLD', '500'))
        
        # === Sprach-Konfiguration ===
        self.WAKE_WORD = os.getenv('WAKE_WORD', 'hey toobix')
        self.VOICE_LANGUAGE = os.getenv('VOICE_LANGUAGE', 'de-DE')
        self.TTS_VOICE = os.getenv('TTS_VOICE', 'de')
        self.TTS_RATE = int(os.getenv('TTS_RATE', '200'))
        
        # === GUI Konfiguration ===
        self.WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '800'))
        self.WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '600'))
        self.THEME = os.getenv('THEME', 'dark')
        
        # === Desktop Integration ===
        self.ENABLE_FILE_OPERATIONS = os.getenv('ENABLE_FILE_OPERATIONS', 'true').lower() == 'true'
        self.ENABLE_SYSTEM_CONTROL = os.getenv('ENABLE_SYSTEM_CONTROL', 'true').lower() == 'true'
        self.SAFE_MODE = os.getenv('SAFE_MODE', 'false').lower() == 'true'
        
        # === Logging ===
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        self.LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'false').lower() == 'true'
        
        # === Erweiterte Features ===
        self.AUTO_EXECUTE_COMMANDS = os.getenv('AUTO_EXECUTE_COMMANDS', 'false').lower() == 'true'
        self.SHOW_NOTIFICATIONS = os.getenv('SHOW_NOTIFICATIONS', 'true').lower() == 'true'
        
    def get_ai_config(self):
        """Gibt AI-Konfiguration zurück"""
        return {
            'ollama_model': self.OLLAMA_MODEL,
            'ollama_url': self.OLLAMA_URL,
            'groq_api_key': self.GROQ_API_KEY,
            'groq_model': self.GROQ_MODEL,
            'cloud_threshold': self.CLOUD_THRESHOLD
        }
    
    def get_speech_config(self):
        """Gibt Sprach-Konfiguration zurück"""
        return {
            'wake_word': self.WAKE_WORD,
            'language': self.VOICE_LANGUAGE,
            'tts_voice': self.TTS_VOICE,
            'tts_rate': self.TTS_RATE
        }
    
    def get_gui_config(self):
        """Gibt GUI-Konfiguration zurück"""
        return {
            'width': self.WINDOW_WIDTH,
            'height': self.WINDOW_HEIGHT,
            'theme': self.THEME
        }
    
    def is_safe_mode(self):
        """Prüft ob Safe Mode aktiv ist"""
        return self.SAFE_MODE
    
    def __str__(self):
        """String-Darstellung für Debugging"""
        return f"Toobix Settings - Model: {self.OLLAMA_MODEL}, Language: {self.VOICE_LANGUAGE}, Theme: {self.THEME}"
