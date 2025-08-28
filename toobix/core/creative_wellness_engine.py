"""
Toobix Creative Wellness Engine
Ganzheitliche Arbeitsoptimierung mit Ambient Sounds, Meditation und Wellness-Coaching
"""
import json
import time
import random
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class WellnessSession:
    """Wellness-Session"""
    session_id: str
    type: str  # meditation, breathing, stretch, soundscape, break
    duration_minutes: float
    start_time: datetime
    end_time: Optional[datetime]
    effectiveness_rating: Optional[int]  # 1-10
    energy_before: Optional[float]
    energy_after: Optional[float]
    stress_before: Optional[float]
    stress_after: Optional[float]

@dataclass
class SoundscapeProfile:
    """Soundscape-Profil"""
    name: str
    description: str
    audio_files: List[str]
    mood: str  # focus, relax, creative, energize
    binaural_frequency: Optional[float]  # Hz
    nature_sounds: List[str]
    ambient_layers: List[str]
    intensity: str  # soft, medium, intense

@dataclass
class BiofeedbackData:
    """Biofeedback-Daten (simuliert)"""
    timestamp: datetime
    heart_rate: Optional[int]
    stress_level: float  # 0-100
    focus_level: float  # 0-100
    breathing_rate: Optional[int]
    eye_strain: float  # 0-100
    posture_score: float  # 0-100

class CreativeWellnessEngine:
    """
    Wellness-Engine für ganzheitliche Arbeitsoptimierung
    """
    
    def __init__(self):
        """Initialisiert Wellness Engine"""
        self.wellness_sessions = []
        self.soundscape_profiles = {}
        self.biofeedback_history = deque(maxlen=1000)
        self.current_soundscape = None
        self.wellness_preferences = {}
        self.wellness_streaks = defaultdict(int)
        
        # Wellness-Konfiguration
        self.wellness_config = {
            'enable_binaural_beats': True,
            'nature_sounds_volume': 0.6,
            'meditation_reminder_interval': 120,  # Minuten
            'break_reminder_interval': 45,
            'stress_threshold': 70,
            'focus_threshold': 60
        }
        
        # Datenverzeichnis
        self.data_dir = Path('toobix_wellness')
        self.data_dir.mkdir(exist_ok=True)
        
        # Audio-Verzeichnis
        self.audio_dir = self.data_dir / 'audio'
        self.audio_dir.mkdir(exist_ok=True)
        
        # Initialisierung
        self._initialize_soundscape_profiles()
        self._load_wellness_data()
        
        # Monitoring-Thread
        self.monitoring_active = False
        self.monitoring_thread = None
        
        logger.info("🎵 Creative Wellness Engine initialisiert")
    
    def _initialize_soundscape_profiles(self) -> None:
        """Initialisiert Soundscape-Profile"""
        profiles = [
            {
                'name': 'Deep Focus',
                'description': 'Konzentrations-optimierte Klanglandschaft',
                'audio_files': ['focus_ambient.wav', 'subtle_white_noise.wav'],
                'mood': 'focus',
                'binaural_frequency': 40.0,  # Gamma-Wellen für Fokus
                'nature_sounds': ['gentle_rain', 'distant_thunder'],
                'ambient_layers': ['deep_bass', 'harmonic_drones'],
                'intensity': 'medium'
            },
            {
                'name': 'Creative Flow',
                'description': 'Kreativitäts-fördernde Umgebung',
                'audio_files': ['creative_ambient.wav', 'inspiring_tones.wav'],
                'mood': 'creative',
                'binaural_frequency': 8.0,  # Alpha-Wellen für Kreativität
                'nature_sounds': ['forest_birds', 'gentle_stream'],
                'ambient_layers': ['ethereal_pads', 'soft_bells'],
                'intensity': 'soft'
            },
            {
                'name': 'Energizer',
                'description': 'Energie-steigernde Soundscape',
                'audio_files': ['energy_boost.wav', 'motivational_ambient.wav'],
                'mood': 'energize',
                'binaural_frequency': 20.0,  # Beta-Wellen für Energie
                'nature_sounds': ['ocean_waves', 'morning_birds'],
                'ambient_layers': ['uplifting_synths', 'rhythmic_pulses'],
                'intensity': 'intense'
            },
            {
                'name': 'Zen Garden',
                'description': 'Entspannung und Meditation',
                'audio_files': ['zen_ambient.wav', 'meditation_bells.wav'],
                'mood': 'relax',
                'binaural_frequency': 4.0,  # Theta-Wellen für Entspannung
                'nature_sounds': ['bamboo_forest', 'zen_water'],
                'ambient_layers': ['singing_bowls', 'soft_drones'],
                'intensity': 'soft'
            },
            {
                'name': 'Nature Immersion',
                'description': 'Vollständige Natur-Erfahrung',
                'audio_files': ['nature_symphony.wav', 'forest_ambient.wav'],
                'mood': 'relax',
                'binaural_frequency': None,
                'nature_sounds': ['full_forest', 'stream_with_birds', 'wind_in_trees'],
                'ambient_layers': [],
                'intensity': 'medium'
            }
        ]
        
        for profile_data in profiles:
            profile = SoundscapeProfile(**profile_data)
            self.soundscape_profiles[profile.name] = profile
    
    def start_wellness_monitoring(self) -> None:
        """Startet Wellness-Monitoring"""
        if self.monitoring_active:
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._wellness_monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        logger.info("🔍 Wellness-Monitoring gestartet")
    
    def stop_wellness_monitoring(self) -> None:
        """Stoppt Wellness-Monitoring"""
        self.monitoring_active = False
    
    def _wellness_monitoring_loop(self) -> None:
        """Haupt-Wellness-Monitoring Loop"""
        while self.monitoring_active:
            try:
                # Biofeedback-Simulation (in echter Implementierung: Hardware-Integration)
                self._simulate_biofeedback()
                
                # Wellness-Checks
                self._check_stress_levels()
                self._check_break_needs()
                self._check_posture_reminders()
                
                # Adaptive Soundscape-Anpassung
                self._adapt_current_soundscape()
                
                time.sleep(60)  # Alle 60 Sekunden
                
            except Exception as e:
                logger.error(f"Wellness-Monitoring Fehler: {e}")
                time.sleep(120)
    
    def _simulate_biofeedback(self) -> None:
        """Simuliert Biofeedback-Daten (für Demo)"""
        # In echter Implementierung: Integration mit Wearables/Sensoren
        now = datetime.now()
        hour = now.hour
        
        # Tageszeit-basierte Simulation
        if 6 <= hour <= 9:  # Morgen
            base_stress = random.uniform(20, 40)
            base_focus = random.uniform(70, 90)
            base_energy = random.uniform(60, 85)
        elif 9 <= hour <= 12:  # Vormittag
            base_stress = random.uniform(30, 50)
            base_focus = random.uniform(80, 95)
            base_energy = random.uniform(70, 90)
        elif 12 <= hour <= 14:  # Mittagszeit
            base_stress = random.uniform(40, 60)
            base_focus = random.uniform(50, 70)
            base_energy = random.uniform(40, 60)
        elif 14 <= hour <= 17:  # Nachmittag
            base_stress = random.uniform(50, 70)
            base_focus = random.uniform(60, 80)
            base_energy = random.uniform(50, 75)
        elif 17 <= hour <= 20:  # Abend
            base_stress = random.uniform(45, 65)
            base_focus = random.uniform(55, 75)
            base_energy = random.uniform(45, 70)
        else:  # Nacht
            base_stress = random.uniform(20, 40)
            base_focus = random.uniform(30, 50)
            base_energy = random.uniform(20, 40)
        
        # Variationen hinzufügen
        stress_variation = random.uniform(-10, 10)
        focus_variation = random.uniform(-15, 15)
        
        biofeedback = BiofeedbackData(
            timestamp=now,
            heart_rate=random.randint(60, 100),
            stress_level=max(0, min(100, base_stress + stress_variation)),
            focus_level=max(0, min(100, base_focus + focus_variation)),
            breathing_rate=random.randint(12, 20),
            eye_strain=random.uniform(10, 60),
            posture_score=random.uniform(60, 95)
        )
        
        self.biofeedback_history.append(biofeedback)
    
    def _check_stress_levels(self) -> None:
        """Überprüft Stress-Level und empfiehlt Interventionen"""
        if not self.biofeedback_history:
            return
        
        recent_data = list(self.biofeedback_history)[-3:]  # Letzte 3 Messungen
        avg_stress = sum(data.stress_level for data in recent_data) / len(recent_data)
        
        if avg_stress > self.wellness_config['stress_threshold']:
            self._recommend_stress_relief()
    
    def _check_break_needs(self) -> None:
        """Überprüft ob eine Pause benötigt wird"""
        # Letzte Pause finden
        now = datetime.now()
        last_break = self._get_last_break_time()
        
        if last_break:
            time_since_break = (now - last_break).total_seconds() / 60  # Minuten
            if time_since_break > self.wellness_config['break_reminder_interval']:
                self._recommend_break()
        else:
            # Keine Pause in der Historie - empfehle eine
            self._recommend_break()
    
    def _check_posture_reminders(self) -> None:
        """Überprüft Haltungs-Erinnerungen"""
        if not self.biofeedback_history:
            return
        
        recent_posture = list(self.biofeedback_history)[-5:]
        avg_posture = sum(data.posture_score for data in recent_posture) / len(recent_posture)
        
        if avg_posture < 70:  # Schlechte Haltung
            self._recommend_posture_break()
    
    def _adapt_current_soundscape(self) -> None:
        """Passt aktuelle Soundscape an Zustand an"""
        if not self.current_soundscape or not self.biofeedback_history:
            return
        
        latest_data = self.biofeedback_history[-1]
        
        # Adaptive Anpassungen basierend auf Biofeedback
        if latest_data.stress_level > 70:
            self._suggest_relaxing_soundscape()
        elif latest_data.focus_level < 60:
            self._suggest_focus_soundscape()
        elif latest_data.focus_level > 85 and latest_data.stress_level < 40:
            # Optimaler Zustand - beibehalten
            pass
    
    def start_soundscape(self, profile_name: str) -> Dict[str, Any]:
        """Startet eine Soundscape"""
        if profile_name not in self.soundscape_profiles:
            return {'success': False, 'error': 'Profil nicht gefunden'}
        
        profile = self.soundscape_profiles[profile_name]
        self.current_soundscape = profile_name
        
        # In echter Implementierung: Audio-Player starten
        logger.info(f"🎵 Soundscape gestartet: {profile.name}")
        
        return {
            'success': True,
            'profile': asdict(profile),
            'message': f"Soundscape '{profile.name}' aktiviert",
            'binaural_frequency': profile.binaural_frequency,
            'mood': profile.mood
        }
    
    def stop_soundscape(self) -> Dict[str, Any]:
        """Stoppt aktuelle Soundscape"""
        if not self.current_soundscape:
            return {'success': False, 'message': 'Keine aktive Soundscape'}
        
        stopped_soundscape = self.current_soundscape
        self.current_soundscape = None
        
        logger.info(f"🔇 Soundscape gestoppt: {stopped_soundscape}")
        
        return {
            'success': True,
            'message': f"Soundscape '{stopped_soundscape}' gestoppt"
        }
    
    def start_meditation_session(self, type: str = 'mindfulness', duration: int = 10) -> Dict[str, Any]:
        """Startet eine Meditation-Session"""
        session_id = f"meditation_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = WellnessSession(
            session_id=session_id,
            type=f"meditation_{type}",
            duration_minutes=duration,
            start_time=datetime.now(),
            end_time=None,
            effectiveness_rating=None,
            energy_before=self._get_current_energy_level(),
            energy_after=None,
            stress_before=self._get_current_stress_level(),
            stress_after=None
        )
        
        self.wellness_sessions.append(session)
        
        # Meditation-spezifische Soundscape starten
        meditation_soundscapes = {
            'mindfulness': 'Zen Garden',
            'breathing': 'Nature Immersion',
            'body_scan': 'Deep Focus',
            'loving_kindness': 'Creative Flow'
        }
        
        soundscape = meditation_soundscapes.get(type, 'Zen Garden')
        self.start_soundscape(soundscape)
        
        logger.info(f"🧘 Meditation gestartet: {type} ({duration}min)")
        
        return {
            'success': True,
            'session_id': session_id,
            'type': type,
            'duration': duration,
            'guidance': self._get_meditation_guidance(type),
            'soundscape': soundscape
        }
    
    def end_wellness_session(self, session_id: str, effectiveness_rating: int = None) -> Dict[str, Any]:
        """Beendet eine Wellness-Session"""
        session = None
        for s in self.wellness_sessions:
            if s.session_id == session_id and s.end_time is None:
                session = s
                break
        
        if not session:
            return {'success': False, 'error': 'Session nicht gefunden'}
        
        session.end_time = datetime.now()
        session.effectiveness_rating = effectiveness_rating
        session.energy_after = self._get_current_energy_level()
        session.stress_after = self._get_current_stress_level()
        
        # Wellness-Streak aktualisieren
        session_type = session.type.split('_')[0]  # meditation, breathing, etc.
        self.wellness_streaks[session_type] += 1
        
        # Daten speichern
        self._save_wellness_data()
        
        # Erfolg bewerten
        energy_improvement = (session.energy_after or 0) - (session.energy_before or 0)
        stress_reduction = (session.stress_before or 0) - (session.stress_after or 0)
        
        logger.info(f"✅ Wellness-Session beendet: {session.type}")
        
        return {
            'success': True,
            'session_summary': {
                'duration': (session.end_time - session.start_time).total_seconds() / 60,
                'energy_improvement': energy_improvement,
                'stress_reduction': stress_reduction,
                'effectiveness_rating': effectiveness_rating
            },
            'streak': self.wellness_streaks[session_type],
            'recommendations': self._get_post_session_recommendations(session)
        }
    
    def start_breathing_exercise(self, pattern: str = '4-7-8') -> Dict[str, Any]:
        """Startet eine Atemübung"""
        session_id = f"breathing_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        breathing_patterns = {
            '4-7-8': {
                'inhale': 4,
                'hold': 7,
                'exhale': 8,
                'description': 'Entspannende 4-7-8 Atmung',
                'duration': 5
            },
            'box': {
                'inhale': 4,
                'hold': 4,
                'exhale': 4,
                'hold': 4,
                'description': 'Fokus-steigernde Box-Atmung',
                'duration': 8
            },
            'energizing': {
                'inhale': 3,
                'hold': 1,
                'exhale': 2,
                'description': 'Energie-steigernde Atmung',
                'duration': 6
            }
        }
        
        if pattern not in breathing_patterns:
            pattern = '4-7-8'
        
        pattern_config = breathing_patterns[pattern]
        
        session = WellnessSession(
            session_id=session_id,
            type=f"breathing_{pattern}",
            duration_minutes=pattern_config['duration'],
            start_time=datetime.now(),
            end_time=None,
            effectiveness_rating=None,
            energy_before=self._get_current_energy_level(),
            energy_after=None,
            stress_before=self._get_current_stress_level(),
            stress_after=None
        )
        
        self.wellness_sessions.append(session)
        
        logger.info(f"🫁 Atemübung gestartet: {pattern}")
        
        return {
            'success': True,
            'session_id': session_id,
            'pattern': pattern,
            'config': pattern_config,
            'instructions': self._get_breathing_instructions(pattern_config)
        }
    
    def _get_meditation_guidance(self, type: str) -> List[str]:
        """Liefert Meditation-Anleitung"""
        guidance = {
            'mindfulness': [
                "Setze dich bequem hin und schließe die Augen",
                "Konzentriere dich auf deinen Atem",
                "Beobachte deine Gedanken ohne sie zu bewerten",
                "Kehre sanft zum Atem zurück, wenn du abschweifst",
                "Bleibe im gegenwärtigen Moment"
            ],
            'breathing': [
                "Finde eine entspannte Position",
                "Lege eine Hand auf Brust, eine auf Bauch",
                "Atme langsam durch die Nase ein",
                "Spüre, wie sich dein Bauch hebt",
                "Atme langsam durch den Mund aus"
            ],
            'body_scan': [
                "Lege dich bequem hin",
                "Beginne bei den Zehen",
                "Spanne jeden Körperteil an und entspanne ihn",
                "Arbeite dich langsam nach oben",
                "Spüre die Entspannung in deinem ganzen Körper"
            ]
        }
        
        return guidance.get(type, guidance['mindfulness'])
    
    def _get_breathing_instructions(self, config: Dict[str, Any]) -> List[str]:
        """Liefert Atemübungs-Anweisungen"""
        instructions = [
            f"Atme {config['inhale']} Sekunden ein",
            f"Halte {config.get('hold', 0)} Sekunden an",
            f"Atme {config['exhale']} Sekunden aus"
        ]
        
        if 'hold_2' in config:
            instructions.append(f"Halte {config['hold_2']} Sekunden an")
        
        instructions.extend([
            f"Wiederhole für {config['duration']} Minuten",
            "Konzentriere dich nur auf den Atem",
            "Lass alle anderen Gedanken los"
        ])
        
        return instructions
    
    def _get_current_energy_level(self) -> float:
        """Ermittelt aktuelles Energy Level"""
        if self.biofeedback_history:
            recent_data = list(self.biofeedback_history)[-3:]
            return sum(100 - data.stress_level + data.focus_level for data in recent_data) / (2 * len(recent_data))
        return 70.0  # Default
    
    def _get_current_stress_level(self) -> float:
        """Ermittelt aktuelles Stress Level"""
        if self.biofeedback_history:
            return self.biofeedback_history[-1].stress_level
        return 50.0  # Default
    
    def _get_last_break_time(self) -> Optional[datetime]:
        """Findet letzte Pause"""
        break_sessions = [s for s in self.wellness_sessions if 'break' in s.type]
        if break_sessions:
            return max(s.start_time for s in break_sessions)
        return None
    
    def _recommend_stress_relief(self) -> None:
        """Empfiehlt Stress-Abbau"""
        recommendations = [
            "Starte eine 4-7-8 Atemübung",
            "Höre entspannende Naturklänge",
            "Mache eine 5-minütige Meditation",
            "Gehe kurz an die frische Luft",
            "Trinke ein Glas Wasser"
        ]
        
        recommendation = random.choice(recommendations)
        logger.info(f"💆 Stress-Empfehlung: {recommendation}")
    
    def _recommend_break(self) -> None:
        """Empfiehlt eine Pause"""
        break_activities = [
            "5-minütige Stretch-Pause",
            "Kurzer Spaziergang",
            "Augen-Entspannung (20-20-20 Regel)",
            "Hydrations-Pause",
            "Kurze Atemübung"
        ]
        
        activity = random.choice(break_activities)
        logger.info(f"⏰ Pausen-Empfehlung: {activity}")
    
    def _recommend_posture_break(self) -> None:
        """Empfiehlt Haltungs-Pause"""
        logger.info("🧘 Haltungs-Erinnerung: Überprüfe deine Sitzposition!")
    
    def _suggest_relaxing_soundscape(self) -> None:
        """Schlägt entspannende Soundscape vor"""
        if self.current_soundscape != 'Zen Garden':
            logger.info("🎵 Empfehlung: Wechsle zu entspannender Soundscape")
    
    def _suggest_focus_soundscape(self) -> None:
        """Schlägt Fokus-Soundscape vor"""
        if self.current_soundscape != 'Deep Focus':
            logger.info("🎯 Empfehlung: Wechsle zu Fokus-Soundscape")
    
    def _get_post_session_recommendations(self, session: WellnessSession) -> List[str]:
        """Generiert Empfehlungen nach Session"""
        recommendations = []
        
        if session.effectiveness_rating and session.effectiveness_rating >= 8:
            recommendations.append("Exzellent! Wiederhole diese Übung regelmäßig")
        elif session.effectiveness_rating and session.effectiveness_rating <= 5:
            recommendations.append("Probiere eine andere Technik oder verlängere die Session")
        
        # Energy-basierte Empfehlungen
        energy_improvement = (session.energy_after or 0) - (session.energy_before or 0)
        if energy_improvement > 10:
            recommendations.append("Großartige Energie-Steigerung! Nutze sie für wichtige Aufgaben")
        elif energy_improvement < 0:
            recommendations.append("Probiere eine energetisierende Aktivität")
        
        return recommendations
    
    def get_wellness_dashboard(self) -> Dict[str, Any]:
        """Liefert Wellness-Dashboard"""
        try:
            dashboard = {
                'current_state': {
                    'active_soundscape': self.current_soundscape,
                    'stress_level': self._get_current_stress_level(),
                    'energy_level': self._get_current_energy_level(),
                    'last_wellness_session': None
                },
                'daily_summary': {
                    'sessions_today': 0,
                    'total_wellness_time': 0,
                    'stress_reduction': 0,
                    'energy_improvement': 0
                },
                'wellness_streaks': dict(self.wellness_streaks),
                'available_soundscapes': list(self.soundscape_profiles.keys()),
                'quick_actions': self._get_quick_wellness_actions(),
                'personalized_recommendations': self._get_personalized_recommendations()
            }
            
            # Heutige Sessions
            today = datetime.now().date()
            today_sessions = [s for s in self.wellness_sessions if s.start_time.date() == today]
            
            if today_sessions:
                dashboard['daily_summary']['sessions_today'] = len(today_sessions)
                total_time = sum(
                    (s.end_time - s.start_time).total_seconds() / 60 
                    for s in today_sessions if s.end_time
                )
                dashboard['daily_summary']['total_wellness_time'] = round(total_time, 1)
                
                # Letzte Session
                latest_session = max(today_sessions, key=lambda s: s.start_time)
                dashboard['current_state']['last_wellness_session'] = {
                    'type': latest_session.type,
                    'time': latest_session.start_time.strftime('%H:%M'),
                    'duration': latest_session.duration_minutes
                }
            
            return dashboard
            
        except Exception as e:
            logger.error(f"Wellness-Dashboard Fehler: {e}")
            return {'error': str(e)}
    
    def _get_quick_wellness_actions(self) -> List[Dict[str, Any]]:
        """Liefert Quick-Actions für Wellness"""
        return [
            {
                'name': '5-Min Meditation',
                'action': 'start_meditation',
                'params': {'type': 'mindfulness', 'duration': 5},
                'icon': '🧘'
            },
            {
                'name': 'Atemübung',
                'action': 'start_breathing',
                'params': {'pattern': '4-7-8'},
                'icon': '🫁'
            },
            {
                'name': 'Fokus-Sounds',
                'action': 'start_soundscape',
                'params': {'profile': 'Deep Focus'},
                'icon': '🎵'
            },
            {
                'name': 'Energie-Boost',
                'action': 'start_soundscape',
                'params': {'profile': 'Energizer'},
                'icon': '⚡'
            }
        ]
    
    def _get_personalized_recommendations(self) -> List[str]:
        """Generiert personalisierte Empfehlungen"""
        recommendations = []
        
        # Basierend auf aktuellen Biofeedback-Daten
        if self.biofeedback_history:
            latest_data = self.biofeedback_history[-1]
            
            if latest_data.stress_level > 70:
                recommendations.append("🫁 Hoher Stress - starte eine Atemübung")
            
            if latest_data.focus_level < 60:
                recommendations.append("🎵 Niedrige Konzentration - aktiviere Fokus-Sounds")
            
            if latest_data.posture_score < 70:
                recommendations.append("🧘 Schlechte Haltung - Zeit für Stretching")
            
            if latest_data.eye_strain > 60:
                recommendations.append("👀 Augen-Entspannung mit 20-20-20 Regel")
        
        # Basierend auf Wellness-Streaks
        if not any(streak > 0 for streak in self.wellness_streaks.values()):
            recommendations.append("🌟 Starte heute deine erste Wellness-Session!")
        
        return recommendations[:3]  # Top 3 Empfehlungen
    
    def _load_wellness_data(self) -> None:
        """Lädt Wellness-Daten"""
        try:
            data_file = self.data_dir / 'wellness_data.json'
            if data_file.exists():
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Sessions laden
                    sessions_data = data.get('sessions', [])
                    for session_data in sessions_data[-50:]:  # Letzte 50 Sessions
                        try:
                            session = WellnessSession(
                                session_id=session_data['session_id'],
                                type=session_data['type'],
                                duration_minutes=session_data['duration_minutes'],
                                start_time=datetime.fromisoformat(session_data['start_time']),
                                end_time=datetime.fromisoformat(session_data['end_time']) if session_data.get('end_time') else None,
                                effectiveness_rating=session_data.get('effectiveness_rating'),
                                energy_before=session_data.get('energy_before'),
                                energy_after=session_data.get('energy_after'),
                                stress_before=session_data.get('stress_before'),
                                stress_after=session_data.get('stress_after')
                            )
                            self.wellness_sessions.append(session)
                        except Exception as e:
                            logger.error(f"Fehler beim Laden Session: {e}")
                    
                    # Streaks laden
                    self.wellness_streaks.update(data.get('streaks', {}))
                    
                    # Preferences laden
                    self.wellness_preferences.update(data.get('preferences', {}))
                    
                    logger.info(f"🎵 {len(self.wellness_sessions)} Wellness-Sessions geladen")
                    
        except Exception as e:
            logger.error(f"Fehler beim Laden Wellness-Daten: {e}")
    
    def _save_wellness_data(self) -> None:
        """Speichert Wellness-Daten"""
        try:
            data_file = self.data_dir / 'wellness_data.json'
            
            # Sessions für Speicherung vorbereiten
            sessions_data = []
            for session in self.wellness_sessions[-50:]:  # Letzte 50 Sessions
                sessions_data.append({
                    'session_id': session.session_id,
                    'type': session.type,
                    'duration_minutes': session.duration_minutes,
                    'start_time': session.start_time.isoformat(),
                    'end_time': session.end_time.isoformat() if session.end_time else None,
                    'effectiveness_rating': session.effectiveness_rating,
                    'energy_before': session.energy_before,
                    'energy_after': session.energy_after,
                    'stress_before': session.stress_before,
                    'stress_after': session.stress_after
                })
            
            data = {
                'sessions': sessions_data,
                'streaks': dict(self.wellness_streaks),
                'preferences': self.wellness_preferences,
                'last_updated': datetime.now().isoformat()
            }
            
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Fehler beim Speichern Wellness-Daten: {e}")

if __name__ == "__main__":
    # Test der Wellness Engine
    wellness = CreativeWellnessEngine()
    wellness.start_wellness_monitoring()
    
    # Test Soundscape
    result = wellness.start_soundscape('Deep Focus')
    print("Soundscape:", result)
    
    # Test Meditation
    meditation = wellness.start_meditation_session('mindfulness', 5)
    print("Meditation:", meditation)
    
    # Dashboard anzeigen
    dashboard = wellness.get_wellness_dashboard()
    print("Wellness Dashboard:", json.dumps(dashboard, indent=2, default=str))
