"""
Toobix KI Thought Stream & Auto-Insights Engine
Kontinuierlicher KI-Gedankenstrom mit automatischen Ideen und Vorschlägen
"""
import asyncio
import json
import random
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from collections import deque
import logging

# Konfiguriere Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ThoughtEntry:
    """KI-Gedanken-Eintrag"""
    timestamp: datetime
    thought_type: str  # insight, suggestion, observation, idea, warning
    content: str
    confidence: float
    context: str
    priority: str  # low, medium, high, urgent
    actionable: bool
    related_system: Optional[str] = None

@dataclass
class AutoInsight:
    """Automatische Einsicht"""
    insight_id: str
    title: str
    description: str
    insight_type: str  # productivity, system, wellness, learning
    data_points: List[str]
    recommendation: str
    impact_level: str  # low, medium, high
    implementation_effort: str  # easy, medium, complex

class KIThoughtStreamEngine:
    """
    KI Thought Stream Engine für kontinuierliche Insights und Ideen
    """
    
    def __init__(self):
        """Initialisiert KI Thought Stream Engine"""
        self.thought_stream = deque(maxlen=200)  # Letzte 200 Gedanken
        self.auto_insights = deque(maxlen=50)
        self.is_active = False
        self.stream_thread = None
        self.insight_callbacks = []
        
        # Stream-Konfiguration
        self.stream_config = {
            'thought_interval': 45,  # Sekunden zwischen Gedanken
            'insight_interval': 300,  # Sekunden zwischen Auto-Insights
            'context_awareness': True,
            'learning_mode': True,
            'creativity_level': 0.7  # 0.0 - 1.0
        }
        
        # Gedanken-Templates
        self.thought_templates = {
            'productivity': [
                "Ich bemerke, dass deine Produktivität um {time} Uhr besonders hoch ist...",
                "Basierend auf deinen Patterns könnte eine {action} jetzt hilfreich sein...",
                "Dein Energy Level zeigt {pattern} - vielleicht ist es Zeit für {suggestion}...",
                "Die Daten zeigen, dass du in {context} besonders effektiv bist..."
            ],
            'system': [
                "Das System läuft seit {uptime} - hier sind einige Optimierungsideen...",
                "Ich habe {count} Git Repositories gescannt und einige Verbesserungen entdeckt...",
                "Die Analytics zeigen interessante Patterns in deinem Arbeitsverhalten...",
                "Deine Systemressourcen könnten mit {suggestion} optimiert werden..."
            ],
            'wellness': [
                "Dein Stress Level ist {level} - Zeit für eine kleine Pause?",
                "Ich empfehle eine {activity} basierend auf deinem aktuellen Zustand...",
                "Die Biorhythmus-Daten zeigen, dass {observation}...",
                "Eine kurze Meditation könnte jetzt genau das Richtige sein..."
            ],
            'learning': [
                "Hier ist eine interessante Erkenntnis über deine Arbeitsgewohnheiten...",
                "Ich habe ein neues Pattern in deinen Daten entdeckt...",
                "Basierend auf Machine Learning Analyse: {insight}...",
                "Deine Lernkurve zeigt {trend} - das ist bemerkenswert!"
            ],
            'creative': [
                "Was wäre, wenn wir {idea} ausprobieren würden?",
                "Ich habe eine kreative Idee für {area}...",
                "Stell dir vor, wir könnten {possibility}...",
                "Eine spontane Idee: {creative_thought}..."
            ]
        }
        
        # Kontext-Abhängige Gedanken
        self.context_thoughts = {
            'programming': [
                "Code-Qualität ist nicht nur Syntax, sondern auch Eleganz...",
                "Refactoring ist wie Meditation für Entwickler...",
                "Jeder Bug ist eine Lerngelegenheit in Verkleidung...",
                "Clean Code ist ein Liebesbrief an dein zukünftiges Ich..."
            ],
            'writing': [
                "Worte sind die Bausteine der Gedanken...",
                "Schreiben ist Denken auf Papier...",
                "Jeder erste Entwurf ist ein Diamant im Rohzustand...",
                "Kreativität ist Intelligenz beim Spielen..."
            ],
            'research': [
                "Wissen ist der einzige Schatz, der sich vermehrt, wenn man ihn teilt...",
                "Forschung ist organisierte Neugier...",
                "Die besten Entdeckungen entstehen an unerwarteten Orten...",
                "Fragen sind wichtiger als Antworten..."
            ]
        }
        
        # Datenverzeichnis
        self.data_dir = Path('toobix_thought_stream')
        self.data_dir.mkdir(exist_ok=True)
        
        # Externe Datenquellen (falls verfügbar)
        self.external_systems = {}
        
        logger.info("🧠 KI Thought Stream Engine initialisiert")
    
    def start_thought_stream(self) -> None:
        """Startet kontinuierlichen Gedankenstrom"""
        if self.is_active:
            return
        
        self.is_active = True
        self.stream_thread = threading.Thread(target=self._thought_stream_loop, daemon=True)
        self.stream_thread.start()
        
        # Begrüßungsgedanke
        welcome_thought = ThoughtEntry(
            timestamp=datetime.now(),
            thought_type="insight",
            content="Hallo! Ich bin dein KI-Gedankenstrom. Ich werde kontinuierlich Ideen, Einsichten und Vorschläge für dich generieren. Du kannst meine Gedanken jederzeit einsehen!",
            confidence=1.0,
            context="system_start",
            priority="medium",
            actionable=False
        )
        self.thought_stream.append(welcome_thought)
        
        logger.info("🌊 KI Thought Stream gestartet")
    
    def stop_thought_stream(self) -> None:
        """Stoppt Gedankenstrom"""
        self.is_active = False
        
        # Abschiedsgedanke
        farewell_thought = ThoughtEntry(
            timestamp=datetime.now(),
            thought_type="observation",
            content="Thought Stream pausiert. Alle bisherigen Gedanken bleiben gespeichert und ich bin bereit, wenn du mich wieder aktivierst!",
            confidence=1.0,
            context="system_stop",
            priority="low",
            actionable=False
        )
        self.thought_stream.append(farewell_thought)
    
    def _thought_stream_loop(self) -> None:
        """Haupt-Loop für Gedankenstrom"""
        last_insight_time = time.time()
        
        while self.is_active:
            try:
                # Neuen Gedanken generieren
                thought = self._generate_thought()
                if thought:
                    self.thought_stream.append(thought)
                    self._notify_thought_callbacks(thought)
                
                # Auto-Insights generieren
                current_time = time.time()
                if current_time - last_insight_time > self.stream_config['insight_interval']:
                    insight = self._generate_auto_insight()
                    if insight:
                        self.auto_insights.append(insight)
                        last_insight_time = current_time
                
                # Warten bis zum nächsten Gedanken
                time.sleep(self.stream_config['thought_interval'])
                
            except Exception as e:
                logger.error(f"Thought Stream Fehler: {e}")
                time.sleep(60)  # Pause bei Fehlern
    
    def _generate_thought(self) -> Optional[ThoughtEntry]:
        """Generiert einen neuen Gedanken"""
        try:
            # Aktuellen Kontext ermitteln
            current_context = self._get_current_context()
            
            # Gedanken-Typ basierend auf Kontext und Zufall wählen
            thought_types = ['productivity', 'system', 'wellness', 'learning', 'creative']
            weights = self._get_thought_type_weights(current_context)
            thought_type = random.choices(thought_types, weights=weights)[0]
            
            # Template auswählen und personalisieren
            templates = self.thought_templates.get(thought_type, [])
            if not templates:
                return None
            
            template = random.choice(templates)
            content = self._personalize_thought(template, thought_type, current_context)
            
            # Gedanken-Eintrag erstellen
            thought = ThoughtEntry(
                timestamp=datetime.now(),
                thought_type=thought_type,
                content=content,
                confidence=random.uniform(0.6, 0.95),
                context=current_context,
                priority=self._determine_priority(thought_type, current_context),
                actionable=self._is_actionable(content),
                related_system=self._get_related_system(thought_type)
            )
            
            return thought
            
        except Exception as e:
            logger.error(f"Gedanken-Generierung Fehler: {e}")
            return None
    
    def _get_current_context(self) -> str:
        """Ermittelt aktuellen Arbeitskontext"""
        # Hier würde normalerweise der Context Manager abgefragt
        # Vereinfachte Implementierung basierend auf Tageszeit
        hour = datetime.now().hour
        
        if 9 <= hour <= 12:
            return "morning_productivity"
        elif 13 <= hour <= 17:
            return "afternoon_work"
        elif 18 <= hour <= 21:
            return "evening_creative"
        else:
            return "general"
    
    def _get_thought_type_weights(self, context: str) -> List[float]:
        """Ermittelt Gewichtung für Gedanken-Typen basierend auf Kontext"""
        base_weights = [0.3, 0.2, 0.2, 0.2, 0.1]  # productivity, system, wellness, learning, creative
        
        if "morning" in context:
            return [0.4, 0.2, 0.1, 0.2, 0.1]  # Mehr Produktivität am Morgen
        elif "creative" in context:
            return [0.2, 0.1, 0.2, 0.2, 0.3]  # Mehr Kreativität am Abend
        elif "afternoon" in context:
            return [0.3, 0.3, 0.2, 0.1, 0.1]  # Mehr System-fokus am Nachmittag
        
        return base_weights
    
    def _personalize_thought(self, template: str, thought_type: str, context: str) -> str:
        """Personalisiert Gedanken-Template"""
        personalizations = {
            '{time}': datetime.now().strftime('%H:%M'),
            '{date}': datetime.now().strftime('%d.%m.%Y'),
            '{context}': context.replace('_', ' '),
            '{level}': random.choice(['niedrig', 'mittel', 'hoch']),
            '{pattern}': random.choice(['interessante Trends', 'wiederkehrende Muster', 'neue Einsichten']),
            '{suggestion}': self._get_contextual_suggestion(context),
            '{action}': random.choice(['kurze Pause', 'Atemübung', 'Kontextwechsel', 'Reflexion']),
            '{activity}': random.choice(['Meditation', 'Spaziergang', 'Stretching', 'Tee trinken']),
            '{observation}': random.choice(['du bist in deiner optimalen Phase', 'eine Pause wäre vorteilhaft', 'deine Energie ist hoch']),
            '{insight}': random.choice(['deine Produktivität folgt klaren Mustern', 'bestimmte Zeiten sind für dich optimal', 'Pausen verbessern deine Leistung']),
            '{trend}': random.choice(['stetige Verbesserung', 'positive Entwicklung', 'konstante Fortschritte']),
            '{idea}': random.choice(['neue Arbeitsorganisation', 'Automatisierung', 'Wellness-Integration']),
            '{area}': random.choice(['Produktivität', 'Kreativität', 'Work-Life-Balance', 'Lernen']),
            '{possibility}': random.choice(['Aufgaben vollautomatisieren', 'perfekte Work-Life-Balance erreichen', 'Produktivität gamifizieren']),
            '{creative_thought}': random.choice(['Was wäre, wenn Arbeit wie ein Spiel wäre?', 'Künstliche Intelligenz als Kreativitäts-Partner', 'Produktivität durch Wellness steigern'])
        }
        
        content = template
        for placeholder, value in personalizations.items():
            content = content.replace(placeholder, value)
        
        return content
    
    def _get_contextual_suggestion(self, context: str) -> str:
        """Liefert kontextuelle Vorschläge"""
        suggestions = {
            'morning_productivity': random.choice(['fokussierte Deep-Work Session', 'wichtigste Aufgabe zuerst', 'Energie-optimierte Planung']),
            'afternoon_work': random.choice(['systematische Aufgaben', 'Code-Review', 'Administrative Tasks']),
            'evening_creative': random.choice(['kreative Projekte', 'Brainstorming', 'neue Ideen entwickeln']),
            'general': random.choice(['Produktivitäts-Optimierung', 'System-Check', 'Wellness-Pause'])
        }
        
        return suggestions.get(context, 'Produktivitäts-Optimierung')
    
    def _determine_priority(self, thought_type: str, context: str) -> str:
        """Bestimmt Priorität des Gedankens"""
        if thought_type == "wellness" and "stress" in context:
            return "high"
        elif thought_type == "productivity" and "morning" in context:
            return "medium"
        elif thought_type == "system" and "error" in context:
            return "urgent"
        else:
            return random.choice(['low', 'medium'])
    
    def _is_actionable(self, content: str) -> bool:
        """Prüft ob Gedanke umsetzbar ist"""
        actionable_keywords = ['empfehle', 'starte', 'probiere', 'versuche', 'mache', 'aktiviere', 'wechsle']
        return any(keyword in content.lower() for keyword in actionable_keywords)
    
    def _get_related_system(self, thought_type: str) -> Optional[str]:
        """Ermittelt verwandtes System"""
        system_mapping = {
            'productivity': 'gamification',
            'system': 'system_monitor',
            'wellness': 'wellness_engine',
            'learning': 'analytics_engine',
            'creative': 'context_manager'
        }
        
        return system_mapping.get(thought_type)
    
    def _generate_auto_insight(self) -> Optional[AutoInsight]:
        """Generiert automatische Einsicht"""
        try:
            insight_types = ['productivity', 'system', 'wellness', 'learning']
            insight_type = random.choice(insight_types)
            
            insight_generators = {
                'productivity': self._generate_productivity_insight,
                'system': self._generate_system_insight,
                'wellness': self._generate_wellness_insight,
                'learning': self._generate_learning_insight
            }
            
            generator = insight_generators.get(insight_type)
            if generator:
                return generator()
            
        except Exception as e:
            logger.error(f"Auto-Insight Generierung Fehler: {e}")
        
        return None
    
    def _generate_productivity_insight(self) -> AutoInsight:
        """Generiert Produktivitäts-Einsicht"""
        insights = [
            {
                'title': 'Optimale Arbeitszeiten identifiziert',
                'description': 'Basierend auf deinen Aktivitätsmustern sind 9-11 Uhr deine produktivsten Stunden.',
                'data_points': ['Aktivitäts-Tracking', 'Kontext-Analyse', 'Performance-Metriken'],
                'recommendation': 'Plane wichtige Deep-Work Sessions für diese Zeitfenster',
                'impact_level': 'high',
                'implementation_effort': 'easy'
            },
            {
                'title': 'Pausen-Pattern entdeckt',
                'description': 'Du bist nach 45-minütigen Arbeitssessions am effektivsten.',
                'data_points': ['Session-Dauer', 'Effizienz-Scores', 'Ermüdungs-Indikatoren'],
                'recommendation': 'Nutze die Pomodoro-Technik mit 45-min Intervallen',
                'impact_level': 'medium',
                'implementation_effort': 'easy'
            }
        ]
        
        insight_data = random.choice(insights)
        
        return AutoInsight(
            insight_id=f"productivity_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            insight_type='productivity',
            **insight_data
        )
    
    def _generate_system_insight(self) -> AutoInsight:
        """Generiert System-Einsicht"""
        insights = [
            {
                'title': 'Resource-Optimierung möglich',
                'description': 'Dein System zeigt Optimierungspotential bei Speicher-Management.',
                'data_points': ['RAM-Nutzung', 'Prozess-Analyse', 'Performance-Metriken'],
                'recommendation': 'Aktiviere automatische Speicher-Optimierung',
                'impact_level': 'medium',
                'implementation_effort': 'easy'
            },
            {
                'title': 'Git-Workflow Verbesserung',
                'description': 'Mehrere Repositories haben uncommitted Changes.',
                'data_points': ['Git-Status', 'Repository-Scan', 'Change-Tracking'],
                'recommendation': 'Aktiviere Auto-Commit für bestimmte Projekte',
                'impact_level': 'low',
                'implementation_effort': 'medium'
            }
        ]
        
        insight_data = random.choice(insights)
        
        return AutoInsight(
            insight_id=f"system_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            insight_type='system',
            **insight_data
        )
    
    def _generate_wellness_insight(self) -> AutoInsight:
        """Generiert Wellness-Einsicht"""
        insights = [
            {
                'title': 'Stress-Pattern erkannt',
                'description': 'Dein Stress-Level steigt typischerweise nach 14 Uhr an.',
                'data_points': ['Biofeedback-Simulation', 'Arbeitszeit-Tracking', 'Stress-Indikatoren'],
                'recommendation': 'Plane entspannende Aktivitäten für den Nachmittag',
                'impact_level': 'high',
                'implementation_effort': 'easy'
            },
            {
                'title': 'Meditation-Effektivität',
                'description': 'Kurze 5-minütige Meditationen zeigen die beste Wirkung für dich.',
                'data_points': ['Meditation-Sessions', 'Wellness-Tracking', 'Effektivitäts-Bewertungen'],
                'recommendation': 'Integriere regelmäßige Micro-Meditationen',
                'impact_level': 'medium',
                'implementation_effort': 'easy'
            }
        ]
        
        insight_data = random.choice(insights)
        
        return AutoInsight(
            insight_id=f"wellness_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            insight_type='wellness',
            **insight_data
        )
    
    def _generate_learning_insight(self) -> AutoInsight:
        """Generiert Lern-Einsicht"""
        insights = [
            {
                'title': 'Lern-Optimierung identifiziert',
                'description': 'Du lernst neue Konzepte am besten in 25-minütigen Blöcken.',
                'data_points': ['Lern-Sessions', 'Verständnis-Rate', 'Retention-Analyse'],
                'recommendation': 'Strukturiere Lernphasen in kurze, intensive Einheiten',
                'impact_level': 'medium',
                'implementation_effort': 'easy'
            },
            {
                'title': 'Kontext-Switch Analyse',
                'description': 'Häufige Kontext-Wechsel reduzieren deine Lern-Effektivität.',
                'data_points': ['Kontext-Tracking', 'Task-Switching', 'Focus-Metriken'],
                'recommendation': 'Verwende Focus-Modi für ungestörtes Lernen',
                'impact_level': 'high',
                'implementation_effort': 'medium'
            }
        ]
        
        insight_data = random.choice(insights)
        
        return AutoInsight(
            insight_id=f"learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            insight_type='learning',
            **insight_data
        )
    
    def _notify_thought_callbacks(self, thought: ThoughtEntry) -> None:
        """Benachrichtigt registrierte Callbacks über neue Gedanken"""
        for callback in self.insight_callbacks:
            try:
                callback(thought)
            except Exception as e:
                logger.error(f"Callback Fehler: {e}")
    
    def register_thought_callback(self, callback: Callable[[ThoughtEntry], None]) -> None:
        """Registriert Callback für neue Gedanken"""
        self.insight_callbacks.append(callback)
    
    def get_thought_stream(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Liefert aktuellen Gedankenstrom"""
        recent_thoughts = list(self.thought_stream)[-limit:]
        return [asdict(thought) for thought in recent_thoughts]
    
    def get_thoughts_by_type(self, thought_type: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Liefert Gedanken nach Typ"""
        filtered_thoughts = [
            thought for thought in self.thought_stream 
            if thought.thought_type == thought_type
        ][-limit:]
        
        return [asdict(thought) for thought in filtered_thoughts]
    
    def get_actionable_thoughts(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Liefert umsetzbare Gedanken"""
        actionable_thoughts = [
            thought for thought in self.thought_stream 
            if thought.actionable
        ][-limit:]
        
        return [asdict(thought) for thought in actionable_thoughts]
    
    def get_auto_insights(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Liefert automatische Einsichten"""
        recent_insights = list(self.auto_insights)[-limit:]
        return [asdict(insight) for insight in recent_insights]
    
    def get_thought_statistics(self) -> Dict[str, Any]:
        """Liefert Gedankenstrom-Statistiken"""
        if not self.thought_stream:
            return {'total_thoughts': 0}
        
        # Typ-Verteilung
        type_counts = {}
        priority_counts = {}
        actionable_count = 0
        
        for thought in self.thought_stream:
            type_counts[thought.thought_type] = type_counts.get(thought.thought_type, 0) + 1
            priority_counts[thought.priority] = priority_counts.get(thought.priority, 0) + 1
            if thought.actionable:
                actionable_count += 1
        
        return {
            'total_thoughts': len(self.thought_stream),
            'actionable_thoughts': actionable_count,
            'type_distribution': type_counts,
            'priority_distribution': priority_counts,
            'auto_insights': len(self.auto_insights),
            'stream_active': self.is_active,
            'last_thought_time': self.thought_stream[-1].timestamp.isoformat() if self.thought_stream else None
        }
    
    def add_external_data_source(self, source_name: str, data_getter: Callable[[], Dict[str, Any]]) -> None:
        """Fügt externe Datenquelle hinzu"""
        self.external_systems[source_name] = data_getter
    
    def inject_thought(self, content: str, thought_type: str = "user", priority: str = "medium") -> None:
        """Fügt manuellen Gedanken hinzu"""
        thought = ThoughtEntry(
            timestamp=datetime.now(),
            thought_type=thought_type,
            content=content,
            confidence=1.0,
            context="user_input",
            priority=priority,
            actionable=self._is_actionable(content)
        )
        
        self.thought_stream.append(thought)
        self._notify_thought_callbacks(thought)

if __name__ == "__main__":
    # Test der Thought Stream Engine
    thought_engine = KIThoughtStreamEngine()
    thought_engine.start_thought_stream()
    
    # Test-Gedanken hinzufügen
    thought_engine.inject_thought("Das ist ein Test-Gedanke", "test")
    
    # Stream für kurze Zeit laufen lassen
    time.sleep(5)
    
    # Gedanken anzeigen
    thoughts = thought_engine.get_thought_stream(5)
    print("Aktuelle Gedanken:", json.dumps(thoughts, indent=2, default=str))
