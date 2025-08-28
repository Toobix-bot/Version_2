"""
Toobix Intelligent Context Manager
Erkennt automatisch Arbeitskontext, Stimmung und optimiert die Produktivität
"""
import time
import json
import psutil
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict, deque
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WorkSession:
    """Repräsentiert eine Arbeitssitzung"""
    start_time: datetime
    end_time: Optional[datetime]
    context_type: str
    activity_score: float
    applications_used: List[str]
    files_accessed: List[str]
    keystrokes: int
    mouse_clicks: int
    focus_duration: float
    interruptions: int

@dataclass
class ProductivityMetrics:
    """Produktivitäts-Metriken"""
    focus_score: float
    efficiency_score: float
    energy_level: float
    stress_indicators: List[str]
    optimal_break_time: datetime
    recommended_task_type: str

class IntelligentContextManager:
    """
    Intelligente Kontext-Erkennung und Produktivitäts-Optimierung
    """
    
    def __init__(self):
        """Initialisiert den Context Manager"""
        self.work_sessions = []
        self.current_session = None
        self.productivity_history = deque(maxlen=100)
        self.context_patterns = {}
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Kontext-Erkennungs-Patterns
        self.context_indicators = {
            'programming': {
                'applications': ['code.exe', 'pycharm', 'intellij', 'visual studio', 'sublime'],
                'file_types': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
                'keywords': ['def ', 'function', 'class ', 'import ', 'return', 'if ', 'for ']
            },
            'writing': {
                'applications': ['word', 'notepad', 'obsidian', 'notion', 'gdocs'],
                'file_types': ['.txt', '.md', '.docx', '.doc'],
                'keywords': ['chapter', 'abstract', 'conclusion', 'introduction']
            },
            'research': {
                'applications': ['browser', 'chrome', 'firefox', 'edge'],
                'keywords': ['google', 'stackoverflow', 'github', 'documentation', 'wiki']
            },
            'design': {
                'applications': ['photoshop', 'illustrator', 'figma', 'canva'],
                'file_types': ['.psd', '.ai', '.sketch', '.fig']
            },
            'meeting': {
                'applications': ['teams', 'zoom', 'skype', 'discord', 'slack'],
                'keywords': ['meeting', 'call', 'conference']
            }
        }
        
        # Produktivitäts-Indikatoren
        self.productivity_indicators = {
            'high_focus': {
                'min_session_duration': 25,  # Minuten
                'max_app_switches': 3,
                'min_keystrokes_per_minute': 50
            },
            'distracted': {
                'max_session_duration': 10,
                'min_app_switches': 10,
                'max_keystrokes_per_minute': 20
            }
        }
        
        # Biorhythmus-Tracking
        self.energy_patterns = defaultdict(list)
        self.optimal_work_hours = []
        
        # Datenverzeichnis
        self.data_dir = Path('toobix_intelligence')
        self.data_dir.mkdir(exist_ok=True)
        
        logger.info("🧠 Intelligent Context Manager initialisiert")
    
    def start_monitoring(self) -> None:
        """Startet kontinuierliches Monitoring"""
        if self.is_monitoring:
            return
            
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info("🎯 Context Monitoring gestartet")
    
    def stop_monitoring(self) -> None:
        """Stoppt Monitoring"""
        self.is_monitoring = False
        if self.current_session:
            self._end_current_session()
    
    def _monitor_loop(self) -> None:
        """Haupt-Monitoring-Loop"""
        while self.is_monitoring:
            try:
                self._analyze_current_context()
                self._update_productivity_metrics()
                self._check_break_recommendations()
                time.sleep(30)  # Alle 30 Sekunden prüfen
            except Exception as e:
                logger.error(f"Monitoring-Fehler: {e}")
                time.sleep(60)
    
    def _analyze_current_context(self) -> str:
        """Analysiert aktuellen Arbeitskontext"""
        try:
            # Aktive Anwendungen
            active_apps = self._get_active_applications()
            
            # Aktuelle Dateien
            recent_files = self._get_recent_files()
            
            # Kontext bestimmen
            context_scores = {}
            for context_type, indicators in self.context_indicators.items():
                score = 0
                
                # App-basierte Erkennung
                for app in active_apps:
                    if any(indicator in app.lower() for indicator in indicators.get('applications', [])):
                        score += 3
                
                # Datei-basierte Erkennung
                for file_path in recent_files:
                    file_ext = Path(file_path).suffix.lower()
                    if file_ext in indicators.get('file_types', []):
                        score += 2
                
                context_scores[context_type] = score
            
            # Besten Kontext ermitteln
            if context_scores:
                detected_context = max(context_scores, key=context_scores.get)
                if context_scores[detected_context] > 0:
                    self._update_current_session(detected_context)
                    return detected_context
            
            return 'general'
            
        except Exception as e:
            logger.error(f"Kontext-Analyse Fehler: {e}")
            return 'unknown'
    
    def _get_active_applications(self) -> List[str]:
        """Ermittelt aktive Anwendungen"""
        try:
            apps = []
            for proc in psutil.process_iter(['name']):
                try:
                    apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return list(set(apps))
        except Exception:
            return []
    
    def _get_recent_files(self) -> List[str]:
        """Ermittelt kürzlich verwendete Dateien"""
        try:
            # Vereinfachte Implementierung - kann erweitert werden
            recent_files = []
            
            # Windows Recent-Ordner
            recent_path = Path.home() / 'AppData' / 'Roaming' / 'Microsoft' / 'Windows' / 'Recent'
            if recent_path.exists():
                for file in recent_path.iterdir():
                    if file.is_file() and file.suffix == '.lnk':
                        recent_files.append(str(file))
            
            return recent_files[:20]  # Letzte 20 Dateien
        except Exception:
            return []
    
    def _update_current_session(self, context_type: str) -> None:
        """Aktualisiert aktuelle Arbeitssitzung"""
        now = datetime.now()
        
        # Neue Session starten falls nötig
        if not self.current_session or self.current_session.context_type != context_type:
            if self.current_session:
                self._end_current_session()
            
            self.current_session = WorkSession(
                start_time=now,
                end_time=None,
                context_type=context_type,
                activity_score=0.0,
                applications_used=[],
                files_accessed=[],
                keystrokes=0,
                mouse_clicks=0,
                focus_duration=0.0,
                interruptions=0
            )
    
    def _end_current_session(self) -> None:
        """Beendet aktuelle Session"""
        if self.current_session:
            self.current_session.end_time = datetime.now()
            self.work_sessions.append(self.current_session)
            self._save_session_data()
            self.current_session = None
    
    def _update_productivity_metrics(self) -> None:
        """Aktualisiert Produktivitäts-Metriken"""
        if not self.current_session:
            return
        
        try:
            # System-Metriken sammeln
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent
            
            # Aktivitäts-Score berechnen
            activity_score = self._calculate_activity_score(cpu_usage, memory_usage)
            
            # Energy Level basierend auf Tageszeit und Aktivität
            energy_level = self._estimate_energy_level()
            
            # Stress-Indikatoren
            stress_indicators = self._detect_stress_indicators()
            
            # Metriken speichern
            metrics = ProductivityMetrics(
                focus_score=activity_score,
                efficiency_score=self._calculate_efficiency_score(),
                energy_level=energy_level,
                stress_indicators=stress_indicators,
                optimal_break_time=self._predict_optimal_break_time(),
                recommended_task_type=self._recommend_task_type()
            )
            
            self.productivity_history.append({
                'timestamp': datetime.now(),
                'metrics': metrics,
                'context': self.current_session.context_type if self.current_session else 'unknown'
            })
            
        except Exception as e:
            logger.error(f"Produktivitäts-Update Fehler: {e}")
    
    def _calculate_activity_score(self, cpu_usage: float, memory_usage: float) -> float:
        """Berechnet Aktivitäts-Score"""
        # Vereinfachte Berechnung
        base_score = (cpu_usage + memory_usage) / 2
        
        # Normalisierung auf 0-100
        return min(100, max(0, base_score))
    
    def _estimate_energy_level(self) -> float:
        """Schätzt aktuelles Energy Level"""
        now = datetime.now()
        hour = now.hour
        
        # Biorhythmus-basierte Schätzung
        if 9 <= hour <= 11:  # Morgen-Peak
            base_energy = 85
        elif 14 <= hour <= 16:  # Nachmittag-Peak
            base_energy = 80
        elif 20 <= hour <= 22:  # Abend-Peak
            base_energy = 70
        elif 12 <= hour <= 14:  # Mittagstief
            base_energy = 60
        elif hour >= 23 or hour <= 6:  # Nacht
            base_energy = 30
        else:
            base_energy = 70
        
        # Arbeitszeit-Anpassung
        if self.current_session:
            session_duration = (now - self.current_session.start_time).total_seconds() / 3600
            if session_duration > 2:  # Nach 2 Stunden Arbeit
                base_energy -= min(30, session_duration * 5)
        
        return max(0, min(100, base_energy))
    
    def _detect_stress_indicators(self) -> List[str]:
        """Erkennt Stress-Indikatoren"""
        indicators = []
        
        if len(self.productivity_history) >= 3:
            recent_metrics = list(self.productivity_history)[-3:]
            
            # Sinkende Effizienz
            efficiency_trend = [m['metrics'].efficiency_score for m in recent_metrics]
            if all(efficiency_trend[i] > efficiency_trend[i+1] for i in range(len(efficiency_trend)-1)):
                indicators.append("Sinkende Effizienz")
            
            # Niedriges Energy Level
            avg_energy = sum(m['metrics'].energy_level for m in recent_metrics) / len(recent_metrics)
            if avg_energy < 40:
                indicators.append("Niedriges Energy Level")
            
            # Lange Arbeitssitzung ohne Pause
            if self.current_session:
                duration = (datetime.now() - self.current_session.start_time).total_seconds() / 3600
                if duration > 2:
                    indicators.append("Lange Sitzung ohne Pause")
        
        return indicators
    
    def _predict_optimal_break_time(self) -> datetime:
        """Vorhersage der optimalen Pausenzeit"""
        if not self.current_session:
            return datetime.now() + timedelta(minutes=30)
        
        # Basierend auf aktueller Session und Energy Level
        energy_level = self._estimate_energy_level()
        session_duration = (datetime.now() - self.current_session.start_time).total_seconds() / 60
        
        if energy_level < 50:
            # Sofortige Pause empfohlen
            return datetime.now()
        elif session_duration > 90:
            # Nach 90 Minuten Pause
            return datetime.now() + timedelta(minutes=5)
        else:
            # Normale Pomodoro-Technik
            return datetime.now() + timedelta(minutes=25 - (session_duration % 25))
    
    def _recommend_task_type(self) -> str:
        """Empfiehlt optimalen Task-Typ basierend auf aktuellem Zustand"""
        energy_level = self._estimate_energy_level()
        hour = datetime.now().hour
        
        if energy_level > 80:
            return "Komplexe kreative Aufgaben"
        elif energy_level > 60:
            return "Analytische und Programmier-Aufgaben"
        elif energy_level > 40:
            return "Routine-Aufgaben und E-Mails"
        else:
            return "Leichte Aufgaben oder Pause"
    
    def _calculate_efficiency_score(self) -> float:
        """Berechnet Effizienz-Score"""
        if not self.current_session:
            return 50.0
        
        # Vereinfachte Berechnung basierend auf Fokus-Zeit
        session_duration = (datetime.now() - self.current_session.start_time).total_seconds() / 60
        
        if session_duration < 5:
            return 30.0  # Zu kurz für Bewertung
        elif session_duration <= 25:
            return 90.0  # Optimale Pomodoro-Zeit
        elif session_duration <= 45:
            return 75.0  # Noch gut
        elif session_duration <= 90:
            return 60.0  # Länger, aber okay
        else:
            return 40.0  # Zu lang ohne Pause
    
    def _check_break_recommendations(self) -> None:
        """Prüft und sendet Pausen-Empfehlungen"""
        if not self.current_session:
            return
        
        optimal_break = self._predict_optimal_break_time()
        if optimal_break <= datetime.now():
            stress_indicators = self._detect_stress_indicators()
            if stress_indicators:
                self._send_break_notification(stress_indicators)
    
    def _send_break_notification(self, stress_indicators: List[str]) -> None:
        """Sendet Pausen-Benachrichtigung"""
        try:
            message = f"💡 Pause empfohlen!\n"
            message += f"Indikatoren: {', '.join(stress_indicators)}\n"
            message += f"Empfohlene Aktivität: {self._get_break_activity()}"
            
            logger.info(f"Break Notification: {message}")
            # Hier könnte eine GUI-Benachrichtigung integriert werden
            
        except Exception as e:
            logger.error(f"Break Notification Fehler: {e}")
    
    def _get_break_activity(self) -> str:
        """Empfiehlt Break-Aktivität"""
        energy_level = self._estimate_energy_level()
        
        activities = {
            'high': ["Kurzer Spaziergang", "Atemübungen", "Stretching"],
            'medium': ["Tee trinken", "Fenster öffnen", "Kurze Meditation"],
            'low': ["Powernap 15min", "Gesunde Snacks", "Entspannungsmusik"]
        }
        
        if energy_level > 60:
            category = 'high'
        elif energy_level > 30:
            category = 'medium'
        else:
            category = 'low'
        
        import random
        return random.choice(activities[category])
    
    def _save_session_data(self) -> None:
        """Speichert Session-Daten"""
        try:
            data_file = self.data_dir / 'work_sessions.json'
            
            # Existierende Daten laden
            sessions_data = []
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    sessions_data = json.load(f)
            
            # Neue Session hinzufügen
            if self.work_sessions:
                session = self.work_sessions[-1]
                sessions_data.append({
                    'start_time': session.start_time.isoformat(),
                    'end_time': session.end_time.isoformat() if session.end_time else None,
                    'context_type': session.context_type,
                    'activity_score': session.activity_score,
                    'focus_duration': session.focus_duration
                })
            
            # Speichern
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(sessions_data[-100:], f, indent=2)  # Nur letzte 100 Sessions
                
        except Exception as e:
            logger.error(f"Session-Speicher Fehler: {e}")
    
    def get_context_analytics(self) -> Dict[str, Any]:
        """Liefert Kontext-Analytics"""
        try:
            analytics = {
                'current_context': self.current_session.context_type if self.current_session else 'none',
                'session_duration': 0,
                'today_contexts': defaultdict(int),
                'productivity_trend': [],
                'energy_level': self._estimate_energy_level(),
                'stress_indicators': self._detect_stress_indicators(),
                'recommendations': []
            }
            
            # Session-Dauer
            if self.current_session:
                duration = (datetime.now() - self.current_session.start_time).total_seconds() / 60
                analytics['session_duration'] = round(duration, 1)
            
            # Heutige Kontexte
            today = datetime.now().date()
            for session in self.work_sessions:
                if session.start_time.date() == today:
                    analytics['today_contexts'][session.context_type] += 1
            
            # Produktivitäts-Trend
            if len(self.productivity_history) >= 5:
                recent = list(self.productivity_history)[-5:]
                analytics['productivity_trend'] = [
                    {
                        'time': entry['timestamp'].strftime('%H:%M'),
                        'focus_score': entry['metrics'].focus_score,
                        'energy_level': entry['metrics'].energy_level
                    }
                    for entry in recent
                ]
            
            # Empfehlungen
            analytics['recommendations'] = self._generate_recommendations()
            
            return analytics
            
        except Exception as e:
            logger.error(f"Analytics Fehler: {e}")
            return {'error': str(e)}
    
    def _generate_recommendations(self) -> List[str]:
        """Generiert intelligente Empfehlungen"""
        recommendations = []
        
        energy_level = self._estimate_energy_level()
        stress_indicators = self._detect_stress_indicators()
        
        # Energy-basierte Empfehlungen
        if energy_level < 40:
            recommendations.append("🔋 Niedriges Energy Level - Pause oder leichte Aufgaben empfohlen")
        elif energy_level > 80:
            recommendations.append("⚡ Hohes Energy Level - Perfekt für komplexe Aufgaben")
        
        # Stress-basierte Empfehlungen
        if "Lange Sitzung ohne Pause" in stress_indicators:
            recommendations.append("⏰ Lange Arbeitssitzung - 15min Pause einlegen")
        
        if "Sinkende Effizienz" in stress_indicators:
            recommendations.append("📉 Effizienz sinkt - Kontext wechseln oder pausieren")
        
        # Zeit-basierte Empfehlungen
        hour = datetime.now().hour
        if 12 <= hour <= 14:
            recommendations.append("🍽️ Mittagszeit - Perfekt für Pause oder leichte Aufgaben")
        elif 15 <= hour <= 17:
            recommendations.append("🎯 Nachmittags-Peak - Ideal für analytische Aufgaben")
        
        return recommendations
    
    def get_productivity_dashboard(self) -> Dict[str, Any]:
        """Liefert umfassendes Produktivitäts-Dashboard"""
        try:
            dashboard = {
                'current_status': {
                    'context': self.current_session.context_type if self.current_session else 'none',
                    'energy_level': self._estimate_energy_level(),
                    'focus_score': 0,
                    'session_duration': 0
                },
                'daily_summary': {
                    'total_work_time': 0,
                    'most_productive_context': 'unknown',
                    'focus_sessions': 0,
                    'break_recommendations_followed': 0
                },
                'insights': {
                    'peak_hours': [],
                    'context_preferences': {},
                    'productivity_patterns': []
                },
                'recommendations': self._generate_recommendations()
            }
            
            # Aktuelle Session-Daten
            if self.current_session:
                duration = (datetime.now() - self.current_session.start_time).total_seconds() / 60
                dashboard['current_status']['session_duration'] = round(duration, 1)
                dashboard['current_status']['focus_score'] = self._calculate_efficiency_score()
            
            # Tages-Zusammenfassung
            today = datetime.now().date()
            today_sessions = [s for s in self.work_sessions if s.start_time.date() == today]
            
            if today_sessions:
                total_time = sum((s.end_time - s.start_time).total_seconds() for s in today_sessions if s.end_time) / 3600
                dashboard['daily_summary']['total_work_time'] = round(total_time, 1)
                
                context_times = defaultdict(float)
                for session in today_sessions:
                    if session.end_time:
                        duration = (session.end_time - session.start_time).total_seconds() / 3600
                        context_times[session.context_type] += duration
                
                if context_times:
                    dashboard['daily_summary']['most_productive_context'] = max(context_times, key=context_times.get)
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Dashboard Fehler: {e}")
            return {'error': str(e)}

if __name__ == "__main__":
    # Test des Context Managers
    context_manager = IntelligentContextManager()
    context_manager.start_monitoring()
    
    try:
        while True:
            time.sleep(10)
            analytics = context_manager.get_context_analytics()
            print(f"Aktueller Kontext: {analytics['current_context']}")
            print(f"Energy Level: {analytics['energy_level']}")
            print(f"Empfehlungen: {analytics['recommendations']}")
            print("-" * 50)
    except KeyboardInterrupt:
        context_manager.stop_monitoring()
        print("Context Manager gestoppt")
