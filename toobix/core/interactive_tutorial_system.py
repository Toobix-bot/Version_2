"""
Toobix Interactive Tutorial System
Interaktive Tutorials und Guided Tours für komplette Systembeherrschung
"""
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, asdict, field
from enum import Enum
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TutorialType(Enum):
    """Tutorial-Typen"""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    FEATURE_SPECIFIC = "feature_specific"
    TROUBLESHOOTING = "troubleshooting"

class StepType(Enum):
    """Schritt-Typen"""
    EXPLANATION = "explanation"
    ACTION = "action"
    INTERACTION = "interaction"
    VERIFICATION = "verification"
    QUIZ = "quiz"

@dataclass
class TutorialStep:
    """Einzelner Tutorial-Schritt"""
    step_id: str
    title: str
    description: str
    step_type: StepType
    content: str
    
    # UI-Anweisungen
    highlight_element: Optional[str] = None
    tooltip_position: str = "bottom"
    arrow_direction: str = "down"
    
    # Interaktions-Daten
    required_action: Optional[str] = None
    verification_criteria: Optional[Dict[str, Any]] = None
    quiz_question: Optional[str] = None
    quiz_options: Optional[List[str]] = None
    quiz_correct_answer: Optional[int] = None
    
    # Media
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    audio_path: Optional[str] = None
    
    # Navigation
    auto_advance: bool = False
    auto_advance_delay: float = 3.0
    skippable: bool = True
    
    # Erfolgsmessung
    success_criteria: Optional[Dict[str, Any]] = None
    hints: List[str] = field(default_factory=list)

@dataclass
class Tutorial:
    """Tutorial-Definition"""
    tutorial_id: str
    title: str
    description: str
    tutorial_type: TutorialType
    estimated_duration: int  # Minuten
    difficulty_level: int  # 1-5
    prerequisites: List[str]
    learning_objectives: List[str]
    steps: List[TutorialStep]
    
    # Metadaten
    author: str = "Toobix Team"
    version: str = "1.0"
    last_updated: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    
    # Konfiguration
    allow_skip_steps: bool = True
    show_progress: bool = True
    track_completion: bool = True

@dataclass
class TutorialProgress:
    """Tutorial-Fortschritt"""
    tutorial_id: str
    user_id: str
    started_at: datetime
    current_step: int
    completed_steps: List[str]
    skipped_steps: List[str]
    completion_status: str  # not_started, in_progress, completed, abandoned
    completion_percentage: float
    time_spent: float  # Sekunden
    last_activity: datetime
    quiz_scores: Dict[str, int] = field(default_factory=dict)

class InteractiveTutorialSystem:
    """
    Interactive Tutorial System für umfassende Benutzerführung
    """
    
    def __init__(self):
        """Initialisiert Interactive Tutorial System"""
        self.tutorials_file = Path('toobix_tutorials.json')
        self.progress_file = Path('toobix_tutorial_progress.json')
        
        # Tutorial-Daten
        self.tutorials = {}
        self.user_progress = {}
        self.current_tutorial = None
        self.current_step = 0
        
        # Callbacks
        self.step_callbacks = []
        self.completion_callbacks = []
        
        # Initialisiere Standard-Tutorials
        self._initialize_default_tutorials()
        
        # Lade gespeicherte Daten
        self._load_tutorials()
        self._load_progress()
        
        logger.info("📚 Interactive Tutorial System initialisiert")
    
    def _initialize_default_tutorials(self) -> None:
        """Initialisiert Standard-Tutorials"""
        self.default_tutorials = {
            # === GRUNDLAGEN TUTORIAL ===
            'basics': Tutorial(
                tutorial_id='basics',
                title='Toobix Grundlagen',
                description='Lerne die grundlegenden Funktionen von Toobix kennen',
                tutorial_type=TutorialType.BASIC,
                estimated_duration=15,
                difficulty_level=1,
                prerequisites=[],
                learning_objectives=[
                    'AI-Chat verwenden',
                    'Sprachsteuerung aktivieren',
                    'Grundlegende Navigation',
                    'Einstellungen anpassen'
                ],
                tags=['grundlagen', 'einsteiger', 'chat', 'sprache'],
                steps=[
                    TutorialStep(
                        step_id='welcome',
                        title='Willkommen bei Toobix!',
                        description='Dein intelligenter AI-Assistent',
                        step_type=StepType.EXPLANATION,
                        content='Willkommen bei Toobix, deinem revolutionären AI-Desktop-Assistenten! Toobix kombiniert modernste KI-Technologie mit intuitiver Benutzerführung, um deine Produktivität zu maximieren.',
                        image_path='tutorial_images/welcome.png',
                        auto_advance=True,
                        auto_advance_delay=5.0
                    ),
                    TutorialStep(
                        step_id='chat_interface',
                        title='AI-Chat Interface',
                        description='So verwendest du den AI-Chat',
                        step_type=StepType.INTERACTION,
                        content='Das Herzstück von Toobix ist der AI-Chat. Hier kannst du natürlich mit der KI kommunizieren. Probiere es aus, indem du eine Frage stellst!',
                        highlight_element='chat_input',
                        tooltip_position='top',
                        required_action='send_message',
                        verification_criteria={'message_sent': True},
                        hints=[
                            'Klicke in das Chat-Eingabefeld',
                            'Tippe eine Frage wie "Hallo, was kannst du?"',
                            'Drücke Enter oder klicke den Senden-Button'
                        ]
                    ),
                    TutorialStep(
                        step_id='speech_activation',
                        title='Sprachsteuerung',
                        description='Aktiviere die Sprachsteuerung',
                        step_type=StepType.ACTION,
                        content='Toobix kann auch per Sprache gesteuert werden. Sage "Toobix" um die Spracherkennung zu aktivieren, oder klicke das Mikrofon-Symbol.',
                        highlight_element='voice_button',
                        tooltip_position='bottom',
                        required_action='activate_voice',
                        verification_criteria={'voice_activated': True},
                        hints=[
                            'Klicke das Mikrofon-Symbol',
                            'Oder sage "Toobix" als Wake-Word',
                            'Das Mikrofon sollte rot leuchten wenn aktiv'
                        ]
                    ),
                    TutorialStep(
                        step_id='thought_stream',
                        title='KI Gedankenstrom',
                        description='Entdecke den kontinuierlichen KI-Gedankenstrom',
                        step_type=StepType.EXPLANATION,
                        content='Im rechten Panel siehst du den KI-Gedankenstrom. Hier generiert Toobix kontinuierlich Ideen, Einsichten und Vorschläge basierend auf deinen Aktivitäten.',
                        highlight_element='thought_stream_panel',
                        tooltip_position='left',
                        auto_advance=True,
                        auto_advance_delay=4.0
                    ),
                    TutorialStep(
                        step_id='settings_overview',
                        title='Einstellungen anpassen',
                        description='Öffne die Einstellungen',
                        step_type=StepType.INTERACTION,
                        content='Toobix ist hochgradig anpassbar. Öffne die Einstellungen um das System nach deinen Wünschen zu konfigurieren.',
                        highlight_element='settings_button',
                        tooltip_position='top',
                        required_action='open_settings',
                        verification_criteria={'settings_opened': True},
                        hints=[
                            'Klicke das Zahnrad-Symbol',
                            'Oder verwende den Shortcut Ctrl+,',
                            'Die Einstellungen öffnen sich in einem neuen Panel'
                        ]
                    ),
                    TutorialStep(
                        step_id='congratulations',
                        title='Herzlichen Glückwunsch!',
                        description='Du hast die Grundlagen gemeistert',
                        step_type=StepType.EXPLANATION,
                        content='Perfekt! Du kennst jetzt die wichtigsten Grundfunktionen von Toobix. Erkunde weitere Tutorials um das volle Potential zu entdecken.',
                        auto_advance=True,
                        auto_advance_delay=3.0
                    )
                ]
            ),
            
            # === PRODUKTIVITÄTS TUTORIAL ===
            'productivity': Tutorial(
                tutorial_id='productivity',
                title='Produktivitäts-Features',
                description='Maximiere deine Produktivität mit Toobix',
                tutorial_type=TutorialType.INTERMEDIATE,
                estimated_duration=20,
                difficulty_level=2,
                prerequisites=['basics'],
                learning_objectives=[
                    'Gamification-System nutzen',
                    'Pomodoro-Technik anwenden',
                    'Wellness-Features aktivieren',
                    'Analytics verstehen'
                ],
                tags=['produktivität', 'gamification', 'wellness', 'analytics'],
                steps=[
                    TutorialStep(
                        step_id='gamification_intro',
                        title='Produktivitäts-Gamification',
                        description='Verwandle Arbeit in ein Spiel',
                        step_type=StepType.EXPLANATION,
                        content='Toobix verwandelt deine Arbeitsroutine in ein motivierendes Spiel. Sammle Punkte, erreiche Level und erhalte Belohnungen für produktive Arbeit.',
                        highlight_element='gamification_panel'
                    ),
                    TutorialStep(
                        step_id='start_pomodoro',
                        title='Pomodoro Session starten',
                        description='Starte eine fokussierte Arbeitsession',
                        step_type=StepType.INTERACTION,
                        content='Starte eine Pomodoro-Session für hochfokussierte Arbeit. Klicke auf "Pomodoro starten" um eine 25-minütige Session zu beginnen.',
                        highlight_element='pomodoro_button',
                        required_action='start_pomodoro',
                        verification_criteria={'pomodoro_started': True}
                    ),
                    TutorialStep(
                        step_id='wellness_check',
                        title='Wellness Monitoring',
                        description='Überwache dein Wohlbefinden',
                        step_type=StepType.EXPLANATION,
                        content='Toobix überwacht automatisch dein Wellness-Level und gibt Empfehlungen für Pausen, Meditation und Entspannung.',
                        highlight_element='wellness_indicator'
                    )
                ]
            ),
            
            # === SYSTEM ADMINISTRATION ===
            'system_admin': Tutorial(
                tutorial_id='system_admin',
                title='System Administration',
                description='Erweiterte Systemverwaltung und -überwachung',
                tutorial_type=TutorialType.ADVANCED,
                estimated_duration=30,
                difficulty_level=4,
                prerequisites=['basics', 'productivity'],
                learning_objectives=[
                    'System Monitor verstehen',
                    'Git Integration nutzen',
                    'Task Scheduler konfigurieren',
                    'Performance optimieren'
                ],
                tags=['system', 'administration', 'git', 'monitoring', 'advanced'],
                steps=[
                    TutorialStep(
                        step_id='system_monitor_overview',
                        title='System Monitor',
                        description='Überwache Systemressourcen',
                        step_type=StepType.EXPLANATION,
                        content='Der System Monitor zeigt Echtzeit-Informationen über CPU, RAM, Festplatte und Netzwerk. Erkenne Performance-Probleme frühzeitig.',
                        highlight_element='system_monitor_panel'
                    ),
                    TutorialStep(
                        step_id='git_integration_setup',
                        title='Git Integration',
                        description='Konfiguriere Git Integration',
                        step_type=StepType.INTERACTION,
                        content='Toobix kann deine Git-Repositories überwachen und automatisch verwalten. Füge ein Repository hinzu um zu beginnen.',
                        highlight_element='git_add_repo_button',
                        required_action='add_git_repo',
                        verification_criteria={'git_repo_added': True}
                    )
                ]
            ),
            
            # === ERWEITERTE KI FEATURES ===
            'advanced_ai': Tutorial(
                tutorial_id='advanced_ai',
                title='Erweiterte KI Features',
                description='Nutze die volle Kraft der KI-Integration',
                tutorial_type=TutorialType.ADVANCED,
                estimated_duration=25,
                difficulty_level=3,
                prerequisites=['basics'],
                learning_objectives=[
                    'Context Manager nutzen',
                    'Thought Stream konfigurieren',
                    'Auto-Insights verstehen',
                    'KI-Modelle wechseln'
                ],
                tags=['ki', 'context', 'insights', 'modelle', 'advanced'],
                steps=[
                    TutorialStep(
                        step_id='context_awareness',
                        title='Intelligente Kontext-Erkennung',
                        description='Wie Toobix deinen Arbeitskontext versteht',
                        step_type=StepType.EXPLANATION,
                        content='Toobix analysiert kontinuierlich deinen Arbeitskontext - welche Apps du verwendest, an welchen Projekten du arbeitest, und passt die AI-Antworten entsprechend an.',
                        highlight_element='context_display'
                    ),
                    TutorialStep(
                        step_id='thought_stream_config',
                        title='Gedankenstrom konfigurieren',
                        description='Passe den KI-Gedankenstrom an',
                        step_type=StepType.INTERACTION,
                        content='Du kannst die Frequenz und Kreativität des KI-Gedankenstroms in den Einstellungen anpassen. Öffne die Gedankenstrom-Einstellungen.',
                        highlight_element='thought_stream_settings',
                        required_action='open_thought_settings',
                        verification_criteria={'thought_settings_opened': True}
                    )
                ]
            ),
            
            # === TROUBLESHOOTING ===
            'troubleshooting': Tutorial(
                tutorial_id='troubleshooting',
                title='Problembehebung',
                description='Löse häufige Probleme selbstständig',
                tutorial_type=TutorialType.TROUBLESHOOTING,
                estimated_duration=15,
                difficulty_level=2,
                prerequisites=[],
                learning_objectives=[
                    'Häufige Probleme erkennen',
                    'Selbstdiagnose durchführen',
                    'Logs interpretieren',
                    'Support kontaktieren'
                ],
                tags=['troubleshooting', 'probleme', 'diagnose', 'support'],
                steps=[
                    TutorialStep(
                        step_id='common_issues',
                        title='Häufige Probleme',
                        description='Die häufigsten Probleme und ihre Lösungen',
                        step_type=StepType.EXPLANATION,
                        content='Die meisten Probleme können schnell gelöst werden. Hier sind die häufigsten Probleme und ihre Lösungen.',
                        quiz_question='Was ist der erste Schritt bei Problemen mit der Spracherkennung?',
                        quiz_options=[
                            'Computer neu starten',
                            'Mikrofon-Einstellungen prüfen',
                            'Toobix neu installieren',
                            'Support kontaktieren'
                        ],
                        quiz_correct_answer=1
                    ),
                    TutorialStep(
                        step_id='system_diagnostics',
                        title='System-Diagnose',
                        description='Führe eine automatische Diagnose durch',
                        step_type=StepType.ACTION,
                        content='Toobix hat eine integrierte Diagnose-Funktion. Führe eine System-Diagnose durch um Probleme automatisch zu erkennen.',
                        highlight_element='diagnostics_button',
                        required_action='run_diagnostics',
                        verification_criteria={'diagnostics_completed': True}
                    )
                ]
            )
        }
    
    def _load_tutorials(self) -> None:
        """Lädt Tutorial-Definitionen"""
        if self.tutorials_file.exists():
            try:
                with open(self.tutorials_file, 'r', encoding='utf-8') as f:
                    saved_tutorials = json.load(f)
                # TODO: Custom Tutorial Loading implementieren
                logger.info("Benutzerdefinierte Tutorials geladen")
            except Exception as e:
                logger.error(f"Fehler beim Laden der Tutorials: {e}")
        
        # Verwende Standard-Tutorials
        self.tutorials = self.default_tutorials.copy()
    
    def _load_progress(self) -> None:
        """Lädt Benutzer-Fortschritt"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
                
                # Konvertiere zu TutorialProgress Objekten
                for user_id, user_tutorials in progress_data.items():
                    self.user_progress[user_id] = {}
                    for tutorial_id, progress_dict in user_tutorials.items():
                        # Konvertiere Datetime-Strings
                        progress_dict['started_at'] = datetime.fromisoformat(progress_dict['started_at'])
                        progress_dict['last_activity'] = datetime.fromisoformat(progress_dict['last_activity'])
                        
                        self.user_progress[user_id][tutorial_id] = TutorialProgress(**progress_dict)
                
                logger.info(f"Tutorial-Fortschritt geladen für {len(self.user_progress)} Benutzer")
            except Exception as e:
                logger.error(f"Fehler beim Laden des Fortschritts: {e}")
    
    def save_progress(self) -> None:
        """Speichert Benutzer-Fortschritt"""
        try:
            # Konvertiere zu JSON-serializable Format
            progress_data = {}
            for user_id, user_tutorials in self.user_progress.items():
                progress_data[user_id] = {}
                for tutorial_id, progress in user_tutorials.items():
                    progress_dict = asdict(progress)
                    # Konvertiere Datetime-Objekte
                    progress_dict['started_at'] = progress.started_at.isoformat()
                    progress_dict['last_activity'] = progress.last_activity.isoformat()
                    progress_data[user_id][tutorial_id] = progress_dict
            
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Tutorial-Fortschritt gespeichert")
        except Exception as e:
            logger.error(f"Fehler beim Speichern des Fortschritts: {e}")
    
    def start_tutorial(self, tutorial_id: str, user_id: str = "default") -> bool:
        """Startet ein Tutorial"""
        if tutorial_id not in self.tutorials:
            logger.error(f"Tutorial nicht gefunden: {tutorial_id}")
            return False
        
        tutorial = self.tutorials[tutorial_id]
        
        # Prüfe Prerequisites
        if not self._check_prerequisites(tutorial.prerequisites, user_id):
            logger.warning(f"Prerequisites nicht erfüllt für Tutorial: {tutorial_id}")
            return False
        
        # Initialisiere Progress
        if user_id not in self.user_progress:
            self.user_progress[user_id] = {}
        
        self.user_progress[user_id][tutorial_id] = TutorialProgress(
            tutorial_id=tutorial_id,
            user_id=user_id,
            started_at=datetime.now(),
            current_step=0,
            completed_steps=[],
            skipped_steps=[],
            completion_status="in_progress",
            completion_percentage=0.0,
            time_spent=0.0,
            last_activity=datetime.now()
        )
        
        # Setze aktuelles Tutorial
        self.current_tutorial = tutorial_id
        self.current_step = 0
        
        # Speichere Fortschritt
        self.save_progress()
        
        logger.info(f"Tutorial gestartet: {tutorial.title}")
        return True
    
    def next_step(self, user_id: str = "default") -> Optional[TutorialStep]:
        """Geht zum nächsten Tutorial-Schritt"""
        if not self.current_tutorial:
            return None
        
        tutorial = self.tutorials[self.current_tutorial]
        progress = self.user_progress[user_id][self.current_tutorial]
        
        if self.current_step >= len(tutorial.steps):
            # Tutorial abgeschlossen
            self._complete_tutorial(user_id)
            return None
        
        current_step = tutorial.steps[self.current_step]
        
        # Update Progress
        progress.current_step = self.current_step
        progress.last_activity = datetime.now()
        
        # Triggere Callbacks
        self._notify_step_callbacks(current_step, progress)
        
        return current_step
    
    def complete_step(self, step_id: str, user_id: str = "default", skip: bool = False) -> bool:
        """Markiert Schritt als abgeschlossen"""
        if not self.current_tutorial:
            return False
        
        progress = self.user_progress[user_id][self.current_tutorial]
        
        if skip:
            progress.skipped_steps.append(step_id)
        else:
            progress.completed_steps.append(step_id)
        
        # Update Completion Percentage
        tutorial = self.tutorials[self.current_tutorial]
        total_steps = len(tutorial.steps)
        completed_steps = len(progress.completed_steps)
        progress.completion_percentage = (completed_steps / total_steps) * 100
        
        # Nächster Schritt
        self.current_step += 1
        
        # Speichere Fortschritt
        self.save_progress()
        
        return True
    
    def _check_prerequisites(self, prerequisites: List[str], user_id: str) -> bool:
        """Prüft ob Prerequisites erfüllt sind"""
        if not prerequisites:
            return True
        
        if user_id not in self.user_progress:
            return False
        
        user_tutorials = self.user_progress[user_id]
        
        for prereq in prerequisites:
            if prereq not in user_tutorials:
                return False
            if user_tutorials[prereq].completion_status != "completed":
                return False
        
        return True
    
    def _complete_tutorial(self, user_id: str) -> None:
        """Markiert Tutorial als abgeschlossen"""
        if not self.current_tutorial:
            return
        
        progress = self.user_progress[user_id][self.current_tutorial]
        progress.completion_status = "completed"
        progress.completion_percentage = 100.0
        progress.last_activity = datetime.now()
        
        tutorial = self.tutorials[self.current_tutorial]
        
        # Triggere Completion Callbacks
        self._notify_completion_callbacks(tutorial, progress)
        
        # Reset current tutorial
        self.current_tutorial = None
        self.current_step = 0
        
        # Speichere Fortschritt
        self.save_progress()
        
        logger.info(f"Tutorial abgeschlossen: {tutorial.title}")
    
    def _notify_step_callbacks(self, step: TutorialStep, progress: TutorialProgress) -> None:
        """Benachrichtigt über Schritt-Wechsel"""
        for callback in self.step_callbacks:
            try:
                callback(step, progress)
            except Exception as e:
                logger.error(f"Step Callback Fehler: {e}")
    
    def _notify_completion_callbacks(self, tutorial: Tutorial, progress: TutorialProgress) -> None:
        """Benachrichtigt über Tutorial-Abschluss"""
        for callback in self.completion_callbacks:
            try:
                callback(tutorial, progress)
            except Exception as e:
                logger.error(f"Completion Callback Fehler: {e}")
    
    def register_step_callback(self, callback: Callable[[TutorialStep, TutorialProgress], None]) -> None:
        """Registriert Callback für Schritt-Wechsel"""
        self.step_callbacks.append(callback)
    
    def register_completion_callback(self, callback: Callable[[Tutorial, TutorialProgress], None]) -> None:
        """Registriert Callback für Tutorial-Abschluss"""
        self.completion_callbacks.append(callback)
    
    def get_available_tutorials(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """Liefert verfügbare Tutorials"""
        available = []
        
        for tutorial_id, tutorial in self.tutorials.items():
            # Prüfe Prerequisites
            can_start = self._check_prerequisites(tutorial.prerequisites, user_id)
            
            # Progress Info
            progress_info = None
            if user_id in self.user_progress and tutorial_id in self.user_progress[user_id]:
                progress = self.user_progress[user_id][tutorial_id]
                progress_info = {
                    'status': progress.completion_status,
                    'percentage': progress.completion_percentage,
                    'last_activity': progress.last_activity.isoformat()
                }
            
            tutorial_info = {
                'id': tutorial_id,
                'title': tutorial.title,
                'description': tutorial.description,
                'type': tutorial.tutorial_type.value,
                'estimated_duration': tutorial.estimated_duration,
                'difficulty_level': tutorial.difficulty_level,
                'prerequisites': tutorial.prerequisites,
                'learning_objectives': tutorial.learning_objectives,
                'tags': tutorial.tags,
                'can_start': can_start,
                'progress': progress_info
            }
            
            available.append(tutorial_info)
        
        return available
    
    def get_tutorial_by_id(self, tutorial_id: str) -> Optional[Dict[str, Any]]:
        """Liefert Tutorial-Details"""
        if tutorial_id not in self.tutorials:
            return None
        
        tutorial = self.tutorials[tutorial_id]
        return asdict(tutorial)
    
    def get_user_statistics(self, user_id: str = "default") -> Dict[str, Any]:
        """Liefert Benutzer-Statistiken"""
        if user_id not in self.user_progress:
            return {
                'total_tutorials': 0,
                'completed_tutorials': 0,
                'in_progress_tutorials': 0,
                'total_time_spent': 0,
                'completion_rate': 0.0
            }
        
        user_tutorials = self.user_progress[user_id]
        
        completed = sum(1 for progress in user_tutorials.values() 
                       if progress.completion_status == "completed")
        in_progress = sum(1 for progress in user_tutorials.values() 
                         if progress.completion_status == "in_progress")
        total_time = sum(progress.time_spent for progress in user_tutorials.values())
        
        return {
            'total_tutorials': len(user_tutorials),
            'completed_tutorials': completed,
            'in_progress_tutorials': in_progress,
            'total_time_spent': total_time,
            'completion_rate': (completed / len(user_tutorials) * 100) if user_tutorials else 0.0
        }
    
    def search_tutorials(self, query: str, tutorial_type: Optional[TutorialType] = None) -> List[Dict[str, Any]]:
        """Sucht Tutorials nach Query"""
        results = []
        query_lower = query.lower()
        
        for tutorial_id, tutorial in self.tutorials.items():
            # Type Filter
            if tutorial_type and tutorial.tutorial_type != tutorial_type:
                continue
            
            # Text Search
            search_text = f"{tutorial.title} {tutorial.description} {' '.join(tutorial.tags)} {' '.join(tutorial.learning_objectives)}".lower()
            
            if query_lower in search_text:
                results.append({
                    'id': tutorial_id,
                    'title': tutorial.title,
                    'description': tutorial.description,
                    'type': tutorial.tutorial_type.value,
                    'relevance_score': search_text.count(query_lower)
                })
        
        # Sortiere nach Relevanz
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def get_recommended_tutorials(self, user_id: str = "default") -> List[Dict[str, Any]]:
        """Liefert empfohlene Tutorials"""
        recommendations = []
        
        # Ermittle abgeschlossene Tutorials
        completed_tutorials = []
        if user_id in self.user_progress:
            completed_tutorials = [
                tutorial_id for tutorial_id, progress in self.user_progress[user_id].items()
                if progress.completion_status == "completed"
            ]
        
        # Empfehle basierend auf Prerequisites und Level
        for tutorial_id, tutorial in self.tutorials.items():
            if tutorial_id in completed_tutorials:
                continue
            
            can_start = self._check_prerequisites(tutorial.prerequisites, user_id)
            if not can_start:
                continue
            
            # Einfachere Empfehlungslogik - könnte erweitert werden
            recommendation_score = 1.0
            
            # Bonus für Einsteiger-Tutorials
            if tutorial.tutorial_type == TutorialType.BASIC:
                recommendation_score += 0.5
            
            # Bonus für kurze Tutorials
            if tutorial.estimated_duration <= 15:
                recommendation_score += 0.3
            
            recommendations.append({
                'id': tutorial_id,
                'title': tutorial.title,
                'description': tutorial.description,
                'type': tutorial.tutorial_type.value,
                'estimated_duration': tutorial.estimated_duration,
                'difficulty_level': tutorial.difficulty_level,
                'score': recommendation_score
            })
        
        # Sortiere nach Empfehlungs-Score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        
        return recommendations[:5]  # Top 5 Empfehlungen

if __name__ == "__main__":
    # Test des Interactive Tutorial Systems
    tutorial_system = InteractiveTutorialSystem()
    
    # Verfügbare Tutorials anzeigen
    available = tutorial_system.get_available_tutorials()
    print(f"Verfügbare Tutorials: {len(available)}")
    
    # Tutorial starten
    success = tutorial_system.start_tutorial('basics')
    if success:
        print("Grundlagen-Tutorial gestartet")
        
        # Ersten Schritt abrufen
        step = tutorial_system.next_step()
        if step:
            print(f"Aktueller Schritt: {step.title}")
    
    # Empfehlungen abrufen
    recommendations = tutorial_system.get_recommended_tutorials()
    print(f"Empfohlene Tutorials: {len(recommendations)}")
    
    # Statistiken abrufen
    stats = tutorial_system.get_user_statistics()
    print("Benutzer-Statistiken:", json.dumps(stats, indent=2))
