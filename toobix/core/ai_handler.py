"""
Toobix AI Handler
Verwaltet lokale (Ollama) und Cloud-KI (Groq) intelligent
"""
import json
import requests
import asyncio
import aiohttp
import time
from typing import Optional, Dict, Any
from .project_analyzer import ProjectAnalyzer
from .knowledge_base import KnowledgeBase
from .system_monitor import SystemMonitor
from .git_integration import GitManager
from .task_scheduler import TaskScheduler
from .advanced_organizer import AdvancedSystemOrganizer
from .real_system_manager import RealSystemManager
from .advanced_system_monitor import AdvancedSystemMonitor
from .git_integration_manager import GitIntegrationManager
from .intelligent_task_scheduler import IntelligentTaskScheduler
from .advanced_organizer import AdvancedSystemOrganizer

class AIHandler:
    """Intelligente KI-Verwaltung mit lokaler und Cloud-Fallback"""
    
    def __init__(self, settings):
        self.settings = settings
        self.ai_config = settings.get_ai_config()
        
        # Neue erweiterte Module
        self.project_analyzer = ProjectAnalyzer(settings)
        self.knowledge_base = KnowledgeBase(settings)
        self.system_monitor = SystemMonitor(settings)
        self.git_manager = GitManager(settings)
        self.task_scheduler = TaskScheduler(settings)
        self.advanced_organizer = AdvancedSystemOrganizer()
        self.real_system_manager = RealSystemManager()
        self.advanced_monitor = AdvancedSystemMonitor(settings)
        self.git_integration = GitIntegrationManager(settings)
        self.intelligent_scheduler = IntelligentTaskScheduler(settings)
        
        # Status-Tracking
        self.ollama_available = False
        self.groq_available = False
        
        # Performance-Tracking
        self.last_response_time = 0
        self.consecutive_failures = 0
        
        # Phase 3: KI-Enhanced Features
        try:
            from .intelligent_context_manager import IntelligentContextManager
            self.context_manager = IntelligentContextManager()
            self.context_manager.start_monitoring()
            print("🧠 Context Manager initialisiert")
        except Exception as e:
            print(f"❌ Context Manager Fehler: {e}")
            self.context_manager = None
        
        try:
            from .productivity_gamification import ProductivityGamification
            self.gamification = ProductivityGamification()
            print("🎮 Gamification initialisiert")
        except Exception as e:
            print(f"❌ Gamification Fehler: {e}")
            self.gamification = None
        
        try:
            from .deep_analytics_engine import DeepAnalyticsEngine
            self.analytics_engine = DeepAnalyticsEngine()
            print("🔬 Analytics Engine initialisiert")
        except Exception as e:
            print(f"❌ Analytics Engine Fehler: {e}")
            self.analytics_engine = None
        
        try:
            from .creative_wellness_engine import CreativeWellnessEngine
            self.wellness_engine = CreativeWellnessEngine()
            self.wellness_engine.start_wellness_monitoring()
            print("🎵 Wellness Engine initialisiert")
        except Exception as e:
            print(f"❌ Wellness Engine Fehler: {e}")
            self.wellness_engine = None
        self._check_ai_availability()
    
    def _check_ai_availability(self):
        """Prüft verfügbare KI-Services"""
        # Ollama testen
        try:
            response = requests.get(f"{self.ai_config['ollama_url']}/api/tags", timeout=3)
            if response.status_code == 200:
                self.ollama_available = True
                print(f"✅ Ollama verfügbar - Model: {self.ai_config['ollama_model']}")
            else:
                print("⚠️ Ollama nicht erreichbar")
        except Exception as e:
            print(f"⚠️ Ollama-Verbindung fehlgeschlagen: {e}")
        
        # Groq testen (wenn API Key vorhanden)
        if self.ai_config['groq_api_key']:
            self.groq_available = True
            print("✅ Groq Cloud-Backup verfügbar")
        else:
            print("ℹ️ Groq API Key nicht gesetzt - nur lokale KI verfügbar")
    
    async def get_response(self, prompt: str, context: Optional[str] = None) -> str:
        """
        Holt intelligente Antwort von bester verfügbarer KI
        
        Args:
            prompt: Benutzer-Anfrage
            context: Zusätzlicher Kontext (optional)
            
        Returns:
            AI-Antwort als String
        """
        # System-Kontext hinzufügen (Zeit, etc.)
        system_context = self._get_system_context()
        full_prompt = f"{system_context}\n\n{context}\n\n{prompt}" if context else f"{system_context}\n\n{prompt}"
        
        # Entscheidung: Lokal oder Cloud?
        use_cloud = self._should_use_cloud(full_prompt)
        
        if not use_cloud and self.ollama_available:
            # Versuche lokale KI zuerst
            response = await self._query_ollama(full_prompt)
            if response:
                return response
        
        # Fallback zu Cloud-KI
        if self.groq_available:
            response = await self._query_groq(full_prompt)
            if response:
                return response
        
        # Letzte Option: Einfache lokale Antwort
        if self.ollama_available:
            return await self._query_ollama(full_prompt, simple=True)
        
        return "Entschuldigung, ich kann momentan nicht antworten. Bitte überprüfe die KI-Verbindungen."
    
    def _get_system_context(self) -> str:
        """Erstellt System-Kontext mit aktuellen Informationen"""
        import datetime
        
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_date = now.strftime("%d.%m.%Y")
        weekday = now.strftime("%A")
        
        # Deutsche Wochentage
        weekdays_de = {
            'Monday': 'Montag', 'Tuesday': 'Dienstag', 'Wednesday': 'Mittwoch',
            'Thursday': 'Donnerstag', 'Friday': 'Freitag', 'Saturday': 'Samstag', 'Sunday': 'Sonntag'
        }
        weekday_de = weekdays_de.get(weekday, weekday)
        
        context = f"""SYSTEM KONTEXT:
Aktuelle Zeit: {current_time}
Aktuelles Datum: {current_date} ({weekday_de})
System: Windows Desktop-Assistent
Name: Toobix

VERFÜGBARE FUNKTIONEN:
- Programm-Steuerung: "öffne [programm]", "schließe [programm]"
- Datei-Suche: "finde [dateien]", "suche [pattern]"
- System-Aufräumung: "analysiere system", "räume auf", "erstelle backup"
- Zeit/Datum: Aktuelle Informationen verfügbar
- Desktop-Organisation: Dateien sortieren und organisieren"""
        
        return context
    
    def _should_use_cloud(self, prompt: str) -> bool:
        """Entscheidet ob Cloud-KI verwendet werden soll"""
        # Wenn Groq verfügbar ist, bevorzuge es für bessere Antworten
        if self.groq_available:
            return True
        
        # Längere Texte → Cloud
        if len(prompt) > self.ai_config['cloud_threshold']:
            return True
        
        # Bei häufigen lokalen Fehlern → Cloud
        if self.consecutive_failures > 2:
            return True
        
        # Komplexe Anfragen erkennen
        complex_keywords = [
            'analysiere', 'erstelle', 'programmiere', 'schreibe',
            'recherche', 'vergleiche', 'berechne', 'übersetze'
        ]
        
        if any(keyword in prompt.lower() for keyword in complex_keywords):
            return True
        
        return False
    
    async def _query_ollama(self, prompt: str, simple: bool = False) -> Optional[str]:
        """Fragt lokale Ollama-KI ab"""
        try:
            start_time = time.time()
            
            payload = {
                "model": self.ai_config['ollama_model'],
                "prompt": prompt,
                "stream": False
            }
            
            # Einfache Anfrage für Fallback
            if simple:
                payload["options"] = {"num_predict": 100, "temperature": 0.3}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ai_config['ollama_url']}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        self.last_response_time = time.time() - start_time
                        self.consecutive_failures = 0
                        
                        print(f"🤖 Ollama Antwort ({self.last_response_time:.1f}s)")
                        return result.get('response', '').strip()
        
        except Exception as e:
            self.consecutive_failures += 1
            print(f"❌ Ollama Fehler: {e}")
            return None
    
    async def _query_groq(self, prompt: str) -> Optional[str]:
        """Fragt Groq Cloud-KI ab"""
        try:
            headers = {
                "Authorization": f"Bearer {self.ai_config['groq_api_key']}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": "Du bist Toobix, ein hilfreicher deutscher AI-Desktop-Assistent. Du hilfst bei Computerproblemen, beantwortest Fragen und steuerst Windows-Programme. Antworte freundlich, kurz und präzise auf Deutsch. Wenn du Befehle ausführen sollst, erkläre was du tust."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "model": self.ai_config['groq_model'],
                "temperature": 0.7,
                "max_tokens": 500,
                "stream": False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        if 'choices' in result and len(result['choices']) > 0:
                            content = result['choices'][0]['message']['content']
                            print("☁️ Groq Cloud Antwort")
                            return content.strip()
                        else:
                            print(f"❌ Unerwartete Groq Response-Struktur: {result}")
                            return None
                    else:
                        error_text = await response.text()
                        print(f"❌ Groq HTTP Error {response.status}: {error_text}")
                        return None
        
        except Exception as e:
            print(f"❌ Groq Fehler: {e}")
            return None
    
    def get_status(self) -> Dict[str, Any]:
        """Gibt aktuellen AI-Status zurück"""
        return {
            'ollama_available': self.ollama_available,
            'groq_available': self.groq_available,
            'last_response_time': self.last_response_time,
            'consecutive_failures': self.consecutive_failures,
            'current_model': self.ai_config['ollama_model']
        }
    
    def refresh_connection(self):
        """Erneuert KI-Verbindungen"""
        print("🔄 Erneuere KI-Verbindungen...")
        self.consecutive_failures = 0
        self._check_ai_availability()
